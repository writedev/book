## Arrêt et nettoyage en douceur

Le code dans la Liste 21-20 répond aux demandes de manière asynchrone grâce à l'utilisation d'un pool de threads, comme nous l'avions prévu. Nous obtenons quelques avertissements concernant les champs `workers`, `id` et `thread`, que nous n'utilisons pas de manière directe, nous rappelant que nous ne nettoyons rien. Lorsque nous utilisons la méthode moins élégante <kbd>ctrl</kbd>-<kbd>C</kbd> pour arrêter le thread principal, tous les autres threads sont également arrêtés immédiatement, même s'ils sont en train de traiter une demande.

Nous allons ensuite implémenter le trait `Drop` pour appeler `join` sur chacun des threads du pool afin qu'ils puissent terminer les demandes sur lesquelles ils travaillent avant de se fermer. Ensuite, nous mettrons en œuvre un moyen d'informer les threads qu'ils devraient cesser d'accepter de nouvelles demandes et se fermer. Pour voir ce code en action, nous modifierons notre serveur pour n'accepter que deux demandes avant de fermer gracieusement son pool de threads.

Une chose à noter en cours de route : rien de tout cela n'affecte les parties du code qui gèrent l'exécution des fermetures, donc tout ici serait le même si nous utilisions un pool de threads pour un runtime asynchrone.

### Implémentation du trait `Drop` sur `ThreadPool`

Commençons par implémenter `Drop` sur notre pool de threads. Lorsque le pool est supprimé, tous nos threads devraient se joindre pour s'assurer qu'ils terminent leur travail. La Liste 21-22 montre une première tentative d'implémentation de `Drop` ; ce code ne fonctionnera pas tout à fait encore.

<Listing number="21-22" file-name="src/lib.rs" caption="Rejoindre chaque thread lorsque le pool de threads sort du scope">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch21-web-server/listing-21-22/src/lib.rs:here}}
```

</Listing>

Tout d'abord, nous parcourons chacun des `workers` du pool de threads. Nous utilisons `&mut` pour cela car `self` est une référence mutable, et nous devons également pouvoir muter `worker`. Pour chaque `worker`, nous imprimons un message disant que cette instance de `Worker` se ferme, puis nous appelons `join` sur le thread de cette instance de `Worker`. Si l'appel à `join` échoue, nous utilisons `unwrap` pour faire panic sur Rust et passer à un arrêt sans grâce.

Voici l'erreur que nous obtenons lorsque nous compilons ce code :

```console
{{#include ../listings/ch21-web-server/listing-21-22/output.txt}}
```

L'erreur nous dit que nous ne pouvons pas appeler `join` car nous n'avons qu'un emprunt mutable de chaque `worker` et `join` prend la propriété de son argument. Pour résoudre ce problème, nous devons déplacer le thread hors de l'instance de `Worker` qui possède `thread` de sorte que `join` puisse consommer le thread. Une façon de le faire est de prendre la même approche que celle que nous avons adoptée dans la Liste 18-15. Si `Worker` détenait un `Option<thread::JoinHandle<()>>`, nous pourrions appeler la méthode `take` sur l'`Option` pour déplacer la valeur hors de la variante `Some` et laisser une variante `None` à sa place. En d'autres termes, un `Worker` en cours d'exécution aurait une variante `Some` dans `thread`, et lorsque nous voudrions nettoyer un `Worker`, nous remplacerions `Some` par `None` afin que le `Worker` n'ait pas de thread à exécuter.

Cependant, la _seule_ fois que cela se produirait serait lors de la suppression du `Worker`. En échange, nous devrions gérer un `Option<thread::JoinHandle<()>>` partout où nous accédions à `worker.thread`. Le Rust idiomatique utilise beaucoup `Option`, mais lorsque vous vous retrouvez à envelopper quelque chose que vous savez toujours présent dans un `Option` comme solution temporaire, il est conseillé de chercher des approches alternatives pour rendre votre code plus propre et moins sujet aux erreurs.

Dans ce cas, une meilleure alternative existe : la méthode `Vec::drain`. Elle accepte un paramètre de plage pour spécifier quels éléments retirer du vecteur et retourne un itérateur de ces éléments. Passer la syntaxe de plage `..` retirera *chaque* valeur du vecteur.

Ainsi, nous devons mettre à jour l'implémentation de `drop` du `ThreadPool` comme ceci :

<Listing file-name="src/lib.rs">

```rust
{{#rustdoc_include ../listings/ch21-web-server/no-listing-04-update-drop-definition/src/lib.rs:here}}
```

</Listing>

Cela résout l'erreur du compilateur et ne nécessite aucune autre modification dans notre code. Notez que, parce que `drop` peut être appelé lors d'un panic, le `unwrap` pourrait également provoquer un panic et entraîner un double panic, ce qui écraserait immédiatement le programme et mettrait fin à tout nettoyage en cours. Cela convient pour un programme d'exemple, mais ce n'est pas recommandé pour le code de production.

### Signaler aux threads d'arrêter d'écouter les tâches

Avec tous les changements que nous avons apportés, notre code se compile sans aucun avertissement. Cependant, la mauvaise nouvelle est que ce code ne fonctionne pas encore comme nous le souhaitons. La clé est la logique dans les fermetures exécutées par les threads des instances de `Worker` : pour le moment, nous appelons `join`, mais cela ne fermera pas les threads, car ils `loop` indéfiniment à la recherche de tâches. Si nous essayons de supprimer notre `ThreadPool` avec notre implémentation actuelle de `drop`, le thread principal se bloquera indéfiniment, attendant que le premier thread termine.

Pour corriger ce problème, nous aurons besoin d'un changement dans l'implémentation de `drop` du `ThreadPool`, puis d'un changement dans la boucle de `Worker`.

Tout d'abord, nous allons modifier l'implémentation de `drop` du `ThreadPool` pour supprimer explicitement le `sender` avant d'attendre que les threads terminent. La Liste 21-23 montre les changements apportés au `ThreadPool` pour supprimer explicitement `sender`. Contrairement au thread, ici nous _devons_ utiliser un `Option` pour pouvoir déplacer `sender` hors de `ThreadPool` avec `Option::take`.

<Listing number="21-23" file-name="src/lib.rs" caption="Suppression explicite de `sender` avant de rejoindre les threads `Worker`">

```rust,noplayground,not_desired_behavior
{{#rustdoc_include ../listings/ch21-web-server/listing-21-23/src/lib.rs:here}}
```

</Listing>

La suppression de `sender` ferme le canal, ce qui indique qu'aucun message supplémentaire ne sera envoyé. Lorsque cela se produit, tous les appels à `recv` que les instances de `Worker` effectuent dans la boucle infinie retourneront une erreur. Dans la Liste 21-24, nous modifions la boucle de `Worker` pour sortir gracieusement de la boucle dans ce cas, ce qui signifie que les threads termineront lorsque l'implémentation de `drop` du `ThreadPool` appellera `join` sur eux.

<Listing number="21-24" file-name="src/lib.rs" caption="Sortie explicite de la boucle lorsque `recv` retourne une erreur">

```rust,noplayground
{{#rustdoc_include ../listings/ch21-web-server/listing-21-24/src/lib.rs:here}}
```

</Listing>

Pour voir ce code en action, modifions `main` pour n'accepter que deux demandes avant de fermer gracieusement le serveur, comme montré dans la Liste 21-25.

<Listing number="21-25" file-name="src/main.rs" caption="Arrêt du serveur après avoir traité deux demandes en sortant de la boucle">

```rust,ignore
{{#rustdoc_include ../listings/ch21-web-server/listing-21-25/src/main.rs:here}}
```

</Listing>

Vous ne voudriez pas qu'un serveur web réel se ferme après avoir servi seulement deux demandes. Ce code sert simplement à démontrer que l'arrêt et le nettoyage en douceur fonctionnent correctement.

La méthode `take` est définie dans le trait `Iterator` et limite l'itération aux deux premiers éléments au maximum. Le `ThreadPool` sortira du scope à la fin de `main`, et l'implémentation de `drop` s'exécutera.

Démarrez le serveur avec `cargo run` et faites trois demandes. La troisième demande devrait retourner une erreur, et dans votre terminal, vous devriez voir une sortie similaire à ceci :

```console
$ cargo run
   Compilation de hello v0.1.0 (file:///projects/hello)
    Terminé avec succès le(s) target(s) [dev] en 0.41s
     Exécution de `target/debug/hello`
Le travailleur 0 a reçu un travail ; exécution.
Fermeture.
Fermeture du travailleur 0
Le travailleur 3 a reçu un travail ; exécution.
Le travailleur 1 s'est déconnecté ; fermeture.
Le travailleur 2 s'est déconnecté ; fermeture.
Le travailleur 3 s'est déconnecté ; fermeture.
Le travailleur 0 s'est déconnecté ; fermeture.
Fermeture du travailleur 1
Fermeture du travailleur 2
Fermeture du travailleur 3
```

Vous pourriez voir un ordre différent des ID de `Worker` et des messages imprimés. Nous pouvons voir comment ce code fonctionne à partir des messages : les instances de `Worker` 0 et 3 ont reçu les deux premières demandes. Le serveur a cessé d'accepter des connexions après la deuxième connexion, et l'implémentation de `Drop` sur le `ThreadPool` commence à s'exécuter avant que le `Worker 3` commence même son travail. La suppression du `sender` déconnecte tous les instances de `Worker` et leur dit de se fermer. Les instances de `Worker` impriment chacune un message lorsqu'elles se déconnectent, puis le pool de threads appelle `join` pour attendre que chaque thread de `Worker` termine.

Remarquez un aspect intéressant de cette exécution particulière : le `ThreadPool` a supprimé le `sender`, et avant qu'aucun `Worker` ne reçoive une erreur, nous avons essayé de rejoindre `Worker 0`. `Worker 0` n'avait pas encore reçu d'erreur de `recv`, donc le thread principal s'est bloqué, attendant que `Worker 0` termine. Pendant ce temps, `Worker 3` a reçu un travail et ensuite tous les threads ont reçu une erreur. Lorsque `Worker 0` a terminé, le thread principal a attendu que les autres instances de `Worker` finissent. À ce moment-là, elles avaient toutes quitté leurs boucles et s'étaient arrêtées.

Félicitations ! Nous avons maintenant terminé notre projet ; nous avons un serveur web de base qui utilise un pool de threads pour répondre de manière asynchrone. Nous sommes capables d'effectuer un arrêt et un nettoyage en douceur du serveur, ce qui nettoie tous les threads du pool.

Voici le code complet pour référence :

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

Nous pourrions faire plus ici ! Si vous souhaitez continuer à améliorer ce projet, voici quelques idées :

- Ajouter plus de documentation à `ThreadPool` et à ses méthodes publiques.
- Ajouter des tests de la fonctionnalité de la bibliothèque.
- Changer les appels à `unwrap` pour un traitement des erreurs plus robuste.
- Utiliser `ThreadPool` pour effectuer une tâche autre que de servir des demandes web.
- Trouver une crate de pool de threads sur [crates.io](https://crates.io/) et mettre en œuvre un serveur web similaire en utilisant la crate. Ensuite, comparez son API et sa robustesse à celle du pool de threads que nous avons implémenté.

## Résumé

Bien joué ! Vous êtes arrivé à la fin du livre ! Nous vous remercions de nous avoir accompagnés dans cette exploration de Rust. Vous êtes maintenant prêt à implémenter vos propres projets Rust et à aider pour les projets des autres. Gardez à l'esprit qu'il existe une communauté accueillante d'autres Rustaces qui aimerait vous aider pour tous les défis que vous rencontrerez dans votre parcours avec Rust.