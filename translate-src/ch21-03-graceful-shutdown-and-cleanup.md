## Arrêt et nettoyage en douceur

Le code de la Listing 21-20 répond aux requêtes de manière asynchrone grâce à l’utilisation d’un pool de threads, comme nous le souhaitions. Nous recevons des avertissements concernant les champs `workers`, `id` et `thread`, que nous n’utilisons pas directement, ce qui nous rappelle que nous ne nettoyons rien. Lorsque nous utilisons la méthode moins élégante <kbd>ctrl</kbd>-<kbd>C</kbd> pour arrêter le thread principal, tous les autres threads s’arrêtent immédiatement eux aussi, même s’ils sont en train de traiter une requête.

Nous allons ensuite implémenter le trait `Drop` pour appeler `join` sur chacun des threads du pool, afin qu’ils puissent terminer le traitement des requêtes en cours avant de s’arrêter. Puis, nous allons implémenter un moyen d’indiquer aux threads qu’ils doivent cesser d’accepter de nouvelles requêtes et s’arrêter. Pour voir ce code en action, nous allons modifier notre serveur afin qu’il n’accepte que deux requêtes avant d’arrêter proprement son pool de threads.

Remarquons une chose au passage : rien de tout cela ne modifie les parties du code qui exécutent les closures. Tout ce qui suit serait donc identique si nous utilisions un pool de threads pour un runtime asynchrone.

### Implémenter le trait `Drop` sur `ThreadPool`

Commençons par implémenter `Drop` pour notre pool de threads. Lorsque le pool est supprimé, tous nos threads doivent être joints afin de s’assurer qu’ils terminent leur travail. La Listing 21-22 présente une première tentative d’implémentation de `Drop` ; ce code ne fonctionnera pas tout à fait pour le moment.

<Listing number="21-22" file-name="src/lib.rs" caption="Joindre chaque thread lorsque le pool de threads sort de portée">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch21-web-server/listing-21-22/src/lib.rs:here}}
```

</Listing>

Tout d’abord, nous parcourons chacun des `workers` du pool de threads. Nous utilisons `&mut` car `self` est une référence mutable et que nous devons également pouvoir modifier `worker`. Pour chaque `worker`, nous affichons un message indiquant que cette instance de `Worker` particulière s’arrête, puis nous appelons `join` sur le thread de cette instance de `Worker`. Si l’appel à `join` échoue, nous utilisons `unwrap` pour faire paniquer Rust et provoquer un arrêt brutal.

Voici l’erreur que nous obtenons lorsque nous compilons ce code :

```console
{{#include ../listings/ch21-web-server/listing-21-22/output.txt}}
```

L’erreur nous indique que nous ne pouvons pas appeler `join`, car nous n’avons qu’un emprunt mutable de chaque `worker`, alors que `join` prend possession de son argument. Pour résoudre ce problème, nous devons déplacer le thread hors de l’instance de `Worker` qui possède `thread`, afin que `join` puisse prendre possession du thread. Une façon de procéder consiste à adopter la même approche que dans la Listing 18-15. Si `Worker` contenait un `Option<thread::JoinHandle<()>>`, nous pourrions appeler la méthode `take` sur l’`Option` afin de déplacer la valeur hors de la variante `Some` et de la remplacer par une variante `None`. Autrement dit, un `Worker` en cours d’exécution aurait une variante `Some` dans `thread`, et lorsque nous voudrions nettoyer un `Worker`, nous remplacerions `Some` par `None` afin que le `Worker` n’ait plus de thread à exécuter.

Cependant, cela ne se produirait qu’au moment de supprimer le `Worker`. En contrepartie, nous devrions gérer un `Option<thread::JoinHandle<()>>` partout où nous accédons à `worker.thread`. Rust idiomatique utilise fréquemment `Option`, mais lorsque vous vous retrouvez à encapsuler dans un `Option` une valeur dont vous savez qu’elle sera toujours présente, comme solution de contournement, il est judicieux de chercher d’autres approches pour rendre votre code plus propre et moins sujet aux erreurs.

Dans ce cas, il existe une meilleure solution : la méthode `Vec::drain`. Elle accepte un paramètre de plage pour indiquer les éléments à supprimer du vecteur et renvoie un itérateur sur ces éléments. En passant la syntaxe de plage `..`, on supprime *toutes* les valeurs du vecteur.

Nous devons donc mettre à jour l’implémentation de `drop` de `ThreadPool` comme ceci :

<Listing file-name="src/lib.rs">

```rust
{{#rustdoc_include ../listings/ch21-web-server/no-listing-04-update-drop-definition/src/lib.rs:here}}
```

</Listing>

Cela résout l’erreur du compilateur et ne nécessite aucune autre modification de notre code. Notez que, comme `drop` peut être appelé pendant une panique, `unwrap` pourrait lui aussi paniquer et provoquer une double panique, ce qui ferait immédiatement planter le programme et interromprait tout nettoyage en cours. Cela convient pour un programme d’exemple, mais ce n’est pas recommandé pour du code destiné à la production.

### Signaler aux threads qu’ils doivent cesser d’écouter les tâches

Avec toutes les modifications apportées, notre code compile sans aucun avertissement. La mauvaise nouvelle, cependant, est qu’il ne fonctionne pas encore comme nous le souhaitons. La clé se trouve dans la logique des closures exécutées par les threads des instances de `Worker` : pour le moment, nous appelons `join`, mais cela n’arrêtera pas les threads, car ils exécutent une boucle infinie à la recherche de tâches. Si nous essayons de supprimer notre `ThreadPool` avec l’implémentation actuelle de `drop`, le thread principal restera bloqué indéfiniment en attendant que le premier thread se termine.

Pour résoudre ce problème, nous devons modifier l’implémentation de `drop` de `ThreadPool`, puis la boucle de `Worker`.

Tout d’abord, nous allons modifier l’implémentation de `drop` de `ThreadPool` pour supprimer explicitement `sender` avant d’attendre la fin des threads. La Listing 21-23 montre les modifications apportées à `ThreadPool` pour supprimer explicitement `sender`. Contrairement au cas du thread, nous avons ici _besoin_ d’utiliser un `Option` afin de pouvoir déplacer `sender` hors de `ThreadPool` avec `Option::take`.

<Listing number="21-23" file-name="src/lib.rs" caption="Suppression explicite de `sender` avant de joindre les threads `Worker`">

```rust,noplayground,not_desired_behavior
{{#rustdoc_include ../listings/ch21-web-server/listing-21-23/src/lib.rs:here}}
```

</Listing>

La suppression de `sender` ferme le canal, ce qui indique qu’aucun autre message ne sera envoyé. Lorsque cela se produit, tous les appels à `recv` effectués par les instances de `Worker` dans leur boucle infinie renvoient une erreur. Dans la Listing 21-24, nous modifions la boucle de `Worker` pour qu’elle se termine proprement dans ce cas, ce qui signifie que les threads se termineront lorsque l’implémentation de `drop` de `ThreadPool` appellera `join` sur eux.

<Listing number="21-24" file-name="src/lib.rs" caption="Sortie explicite de la boucle lorsque `recv` renvoie une erreur">

```rust,noplayground
{{#rustdoc_include ../listings/ch21-web-server/listing-21-24/src/lib.rs:here}}
```

</Listing>

Pour voir ce code en action, modifions `main` afin qu’il n’accepte que deux requêtes avant d’arrêter proprement le serveur, comme indiqué dans la Listing 21-25.

<Listing number="21-25" file-name="src/main.rs" caption="Arrêt du serveur après le traitement de deux requêtes, en sortant de la boucle">

```rust,ignore
{{#rustdoc_include ../listings/ch21-web-server/listing-21-25/src/main.rs:here}}
```

</Listing>

Dans un véritable serveur web, vous ne voudriez pas qu’il s’arrête après seulement deux requêtes. Ce code montre simplement que l’arrêt et le nettoyage en douceur fonctionnent correctement.

La méthode `take` est définie dans le trait `Iterator` et limite l’itération à deux éléments au maximum. `ThreadPool` sortira de portée à la fin de `main`, et l’implémentation de `drop` sera exécutée.

Démarrez le serveur avec `cargo run` et envoyez trois requêtes. La troisième requête devrait échouer, et vous devriez voir une sortie semblable à celle-ci dans votre terminal :

<!-- manual-regeneration
cd listings/ch21-web-server/listing-21-25
cargo run
curl http://127.0.0.1:7878
curl http://127.0.0.1:7878
curl http://127.0.0.1:7878
third request will error because server will have shut down
copy output below
Can't automate because the output depends on making requests
-->

```console
$ cargo run
   Compiling hello v0.1.0 (file:///projects/hello)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.41s
     Running `target/debug/hello`
Worker 0 got a job; executing.
Shutting down.
Shutting down worker 0
Worker 3 got a job; executing.
Worker 1 disconnected; shutting down.
Worker 2 disconnected; shutting down.
Worker 3 disconnected; shutting down.
Worker 0 disconnected; shutting down.
Shutting down worker 1
Shutting down worker 2
Shutting down worker 3
```

L’ordre des ID de `Worker` et des messages affichés peut varier. Les messages nous permettent de comprendre le fonctionnement du code : les instances de `Worker` 0 et 3 ont reçu les deux premières requêtes. Le serveur a cessé d’accepter les connexions après la deuxième, et l’implémentation de `Drop` sur `ThreadPool` commence à s’exécuter avant même que `Worker 3` ne commence son travail. La suppression de `sender` déconnecte toutes les instances de `Worker` et leur indique qu’elles doivent s’arrêter. Chaque instance de `Worker` affiche un message lorsqu’elle est déconnectée, puis le pool de threads appelle `join` pour attendre la fin de chaque thread `Worker`.

Remarquons un aspect intéressant de cette exécution particulière : `ThreadPool` a supprimé `sender` et, avant que le moindre `Worker` ne reçoive une erreur, nous avons essayé de joindre `Worker 0`. `Worker 0` n’avait pas encore reçu d’erreur de `recv`, le thread principal est donc resté bloqué en attendant que `Worker 0` se termine. Pendant ce temps, `Worker 3` a reçu une tâche, puis tous les threads ont reçu une erreur. Lorsque `Worker 0` s’est terminé, le thread principal a attendu la fin des autres instances de `Worker`. À ce moment-là, elles avaient toutes quitté leur boucle et s’étaient arrêtées.

Félicitations ! Nous avons terminé notre projet ; nous avons un serveur web élémentaire qui utilise un pool de threads pour répondre de manière asynchrone. Nous sommes en mesure d’arrêter proprement le serveur, ce qui nettoie tous les threads du pool.

Voici le code complet, pour référence :

<Listing file-name="src/main.rs">

```rust,ignore
{{#rustdoc_include ../listings/ch21-web-server/no-listing-07-final-code/src/main.rs}}
```

</Listing>

<Listing file-name="src/lib.rs">

```rust,noplayground
{{#rustdoc_include ../listings/ch21-web-server/no-listing-07-final-code/src/lib.rs}}
```

</Listing>

Nous pourrions aller plus loin ! Si vous souhaitez continuer à améliorer ce projet, voici quelques idées :

- Ajoutez davantage de documentation à `ThreadPool` et à ses méthodes publiques.
- Ajoutez des tests pour les fonctionnalités de la bibliothèque.
- Remplacez les appels à `unwrap` par une gestion des erreurs plus robuste.
- Utilisez `ThreadPool` pour effectuer une tâche autre que le traitement de requêtes web.
- Trouvez une crate de pool de threads sur [crates.io](https://crates.io/) et implémentez un serveur web similaire avec cette crate. Comparez ensuite son API et sa robustesse à celles du pool de threads que nous avons implémenté.

## Résumé

Bravo ! Vous êtes arrivé à la fin du livre ! Nous tenons à vous remercier de nous avoir accompagnés dans cette découverte de Rust. Vous êtes maintenant prêt à réaliser vos propres projets Rust et à contribuer aux projets d’autres personnes. Gardez à l’esprit qu’il existe une communauté accueillante d’autres Rustacéens qui seraient ravis de vous aider à relever les défis que vous rencontrerez dans votre parcours avec Rust.