## Utilisation des Threads pour Exécuter du Code Simultanément

Dans la plupart des systèmes d'exploitation actuels, le code d'un programme exécuté s'exécute dans un _processus_, et le système d'exploitation gère plusieurs processus simultanément. Au sein d'un programme, vous pouvez également avoir des parties indépendantes qui s'exécutent simultanément. Les fonctionnalités qui exécutent ces parties indépendantes sont appelées _threads_. Par exemple, un serveur web pourrait avoir plusieurs threads afin de pouvoir répondre à plus d'une requête à la fois.

Diviser le calcul dans votre programme en plusieurs threads pour exécuter plusieurs tâches simultanément peut améliorer les performances, mais cela ajoute également de la complexité. Parce que les threads peuvent s'exécuter simultanément, il n'y a aucune garantie intrinsèque sur l'ordre dans lequel les parties de votre code sur différents threads s'exécuteront. Cela peut entraîner des problèmes, tels que :

- Conditions de concurrence, où les threads accèdent à des données ou des ressources dans un ordre incohérent
- Interblocages, où deux threads attendent l'un pour l'autre, empêchant les deux threads de continuer
- Bugs qui ne se produisent que dans certaines situations et qui sont difficiles à reproduire et à corriger de manière fiable

Rust tente d'atténuer les effets négatifs de l'utilisation des threads, mais programmer dans un contexte multithreadé nécessite toujours une réflexion attentive et exige une structure de code différente de celle des programmes s'exécutant dans un seul thread.

Les langages de programmation implémentent les threads de plusieurs manières différentes, et de nombreux systèmes d'exploitation fournissent une API que le langage de programmation peut appeler pour créer de nouveaux threads. La bibliothèque standard de Rust utilise un modèle _1:1_ d'implémentation des threads, par lequel un programme utilise un thread de système d'exploitation par thread de langage. Il existe des crates qui implémentent d'autres modèles de threading qui font des compromis différents par rapport au modèle 1:1. (Le système async de Rust, que nous verrons dans le prochain chapitre, fournit également une autre approche de la concurrence.)

### Création d'un Nouveau Thread avec `spawn`

Pour créer un nouveau thread, nous appelons la fonction `thread::spawn` et lui passons une closure (nous avons parlé des closures dans le Chapitre 13) contenant le code que nous voulons exécuter dans le nouveau thread. L'exemple dans la Liste 16-1 imprime du texte d'un thread principal et un autre texte d'un nouveau thread.

<Listing number="16-1" file-name="src/main.rs" caption="Création d'un nouveau thread pour imprimer une chose pendant que le thread principal imprime autre chose">

```rust
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-01/src/main.rs}}
```

</Listing>

Notez que lorsque le thread principal d'un programme Rust se termine, tous les threads lancés sont arrêtés, qu'ils aient ou non terminé leur exécution. La sortie de ce programme pourrait être légèrement différente à chaque fois, mais elle ressemblera à ce qui suit :

```text
salut numéro 1 du thread principal !
salut numéro 1 du thread lancé !
salut numéro 2 du thread principal !
salut numéro 2 du thread lancé !
salut numéro 3 du thread principal !
salut numéro 3 du thread lancé !
salut numéro 4 du thread principal !
salut numéro 4 du thread lancé !
salut numéro 5 du thread lancé !
```

Les appels à `thread::sleep` obligent un thread à arrêter son exécution pendant une courte durée, permettant ainsi à un autre thread de s'exécuter. Les threads prendront probablement des tours, mais ce n'est pas garanti : cela dépend de la façon dont votre système d'exploitation planifie les threads. Dans cette exécution, le thread principal a imprimé en premier, même si l'instruction d'impression du thread lancé apparaît en premier dans le code. Et bien que nous ayons dit au thread lancé d'imprimer jusqu'à ce que `i` soit `9`, il n'a atteint que `5` avant que le thread principal ne se ferme.

Si vous exécutez ce code et que vous ne voyez de sortie que du thread principal, ou que vous ne voyez aucun chevauchement, essayez d'augmenter les nombres dans les plages pour créer plus d'opportunités pour le système d'exploitation de passer d'un thread à l'autre.

### Attendre que Tous les Threads se Terminant

Le code de la Liste 16-1 non seulement arrête souvent le thread lancé prématurément en raison de la fin du thread principal, mais comme il n'y a aucune garantie sur l'ordre dans lequel les threads s'exécutent, nous ne pouvons également pas garantir que le thread lancé s'exécutera du tout !

Nous pouvons résoudre le problème du thread lancé qui ne s'exécute pas ou qui se termine prématurément en sauvegardant la valeur de retour de `thread::spawn` dans une variable. Le type de retour de `thread::spawn` est `JoinHandle<T>`. Un `JoinHandle<T>` est une valeur possédée qui, lorsque nous appelons la méthode `join` dessus, attendra que son thread se termine. La Liste 16-2 montre comment utiliser le `JoinHandle<T>` du thread que nous avons créé dans la Liste 16-1 et comment appeler `join` pour s'assurer que le thread lancé se termine avant que `main` ne quitte.

<Listing number="16-2" file-name="src/main.rs" caption="Sauvegarde d'un `JoinHandle<T>` depuis `thread::spawn` pour garantir que le thread s'exécute jusqu'à sa finition">

```rust
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-02/src/main.rs}}
```

</Listing>

Appeler `join` sur le handle bloque le thread actuellement en cours d'exécution jusqu'à ce que le thread représenté par le handle se termine. _Bloquer_ un thread signifie que ce thread est empêché de travailler ou de sortir. Parce que nous avons mis l'appel à `join` après la boucle `for` du thread principal, l'exécution de la Liste 16-2 devrait produire une sortie similaire à celle-ci :

```text
salut numéro 1 du thread principal !
salut numéro 2 du thread principal !
salut numéro 1 du thread lancé !
salut numéro 3 du thread principal !
salut numéro 2 du thread lancé !
salut numéro 4 du thread principal !
salut numéro 3 du thread lancé !
salut numéro 4 du thread lancé !
salut numéro 5 du thread lancé !
salut numéro 6 du thread lancé !
salut numéro 7 du thread lancé !
salut numéro 8 du thread lancé !
salut numéro 9 du thread lancé !
```

Les deux threads continuent à alterner, mais le thread principal attend en raison de l'appel à `handle.join()` et ne se termine pas avant que le thread lancé soit terminé.

Mais voyons ce qui se passe lorsque nous déplaçons `handle.join()` avant la boucle `for` dans `main`, comme ceci :

<Listing file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch16-fearless-concurrency/no-listing-01-join-too-early/src/main.rs}}
```

</Listing>

Le thread principal attendra que le thread lancé se termine, puis exécutera sa boucle `for`, donc la sortie ne sera plus entrelacée, comme montré ici :

```text
salut numéro 1 du thread lancé !
salut numéro 2 du thread lancé !
salut numéro 3 du thread lancé !
salut numéro 4 du thread lancé !
salut numéro 5 du thread lancé !
salut numéro 6 du thread lancé !
salut numéro 7 du thread lancé !
salut numéro 8 du thread lancé !
salut numéro 9 du thread lancé !
salut numéro 1 du thread principal !
salut numéro 2 du thread principal !
salut numéro 3 du thread principal !
salut numéro 4 du thread principal !
```

De petits détails, tels que l'endroit où `join` est appelé, peuvent affecter si oui ou non vos threads s'exécutent en même temps.

### Utilisation des Closures `move` avec des Threads

Nous utiliserons souvent le mot-clé `move` avec les closures passées à `thread::spawn` car la closure prendra alors possession des valeurs qu'elle utilise depuis l'environnement, transférant ainsi la propriété de ces valeurs d'un thread à un autre. Dans [“Capturer des Références ou Déplacer la Propriété”][capture]<!-- ignore --> au Chapitre 13, nous avons discuté de `move` dans le contexte des closures. Maintenant, nous allons nous concentrer davantage sur l'interaction entre `move` et `thread::spawn`.

Remarquez dans la Liste 16-1 que la closure que nous passons à `thread::spawn` ne prend aucun argument : nous n'utilisons aucune donnée du thread principal dans le code du thread lancé. Pour utiliser des données du thread principal dans le thread lancé, la closure du thread lancé doit capturer les valeurs dont elle a besoin. La Liste 16-3 montre une tentative de création d'un vecteur dans le thread principal et de son utilisation dans le thread lancé. Cependant, cela ne fonctionnera pas encore, comme vous le verrez dans un instant.

<Listing number="16-3" file-name="src/main.rs" caption="Tentative d'utilisation d'un vecteur créé par le thread principal dans un autre thread">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-03/src/main.rs}}
```

</Listing>

La closure utilise `v`, elle va donc capturer `v` et en faire partie de l'environnement de la closure. Parce que `thread::spawn` exécute cette closure dans un nouveau thread, nous devrions pouvoir accéder à `v` à l'intérieur de ce nouveau thread. Mais lorsque nous compilons cet exemple, nous obtenons l'erreur suivante :

```console
{{#include ../listings/ch16-fearless-concurrency/listing-16-03/output.txt}}
```

Rust _infère_ comment capturer `v`, et parce que `println!` n'a besoin que d'une référence à `v`, la closure essaie de référencer `v`. Cependant, il y a un problème : Rust ne peut pas dire combien de temps le thread lancé s'exécutera, donc il ne sait pas si la référence à `v` sera toujours valide.

La Liste 16-4 fournit un scénario qui est plus susceptible d'avoir une référence à `v` qui ne sera pas valide.

<Listing number="16-4" file-name="src/main.rs" caption="Un thread avec une closure qui tente de capturer une référence à `v` d'un thread principal qui supprime `v`">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-04/src/main.rs}}
```

</Listing>

Si Rust nous permettait d'exécuter ce code, il y a une possibilité que le thread lancé soit immédiatement mis en arrière-plan sans s'exécuter. Le thread lancé a une référence à `v` à l'intérieur, mais le thread principal supprime immédiatement `v`, utilisant la fonction `drop` que nous avons discutée au Chapitre 15. Ensuite, lorsque le thread lancé commence à s'exécuter, `v` n'est plus valide, donc une référence à celui-ci est également invalide. Oh non !

Pour corriger l'erreur de compilation dans la Liste 16-3, nous pouvons utiliser le conseil du message d'erreur :

```text
help: pour forcer la closure à prendre possession de `v` (et de toute autre variable référencée), utilisez le mot-clé `move`
  |
6 |     let handle = thread::spawn(move || {
  |                                ++++
```

En ajoutant le mot-clé `move` avant la closure, nous forçons la closure à prendre possession des valeurs qu'elle utilise plutôt que d'autoriser Rust à inférer qu'elle devrait référencer les valeurs. La modification apportée à la Liste 16-3 montrée dans la Liste 16-5 compilera et s'exécutera comme nous le souhaitons.

<Listing number="16-5" file-name="src/main.rs" caption="Utilisation du mot-clé `move` pour forcer une closure à prendre possession des valeurs qu'elle utilise">

```rust
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-05/src/main.rs}}
```

</Listing>

Nous pourrions être tentés d'essayer la même chose pour corriger le code dans la Liste 16-4 où le thread principal a appelé `drop` en utilisant une closure `move`. Cependant, cette correction ne fonctionnera pas car ce que la Liste 16-4 essaie de faire est interdit pour une raison différente. Si nous ajoutions `move` à la closure, nous déplacerions `v` dans l'environnement de la closure, et nous ne pourrions plus appeler `drop` dessus dans le thread principal. Nous obtiendrions plutôt cette erreur de compilation :

```console
{{#include ../listings/ch16-fearless-concurrency/output-only-01-move-drop/output.txt}}
```

Les règles de propriété de Rust nous ont encore sauvé ! Nous avons obtenu une erreur du code dans la Liste 16-3 parce que Rust était conservateur et ne faisait que référencer `v` pour le thread, ce qui signifiait que le thread principal pouvait théoriquement invalider la référence du thread lancé. En disant à Rust de déplacer la propriété de `v` vers le thread lancé, nous garantissons à Rust que le thread principal n'utilisera plus `v`. Si nous modifions la Liste 16-4 de la même manière, nous violons alors les règles de propriété lorsque nous essayons d'utiliser `v` dans le thread principal. Le mot-clé `move` remplace le comportement par défaut conservateur de Rust qui est de référencer ; il ne nous permet pas de violer les règles de propriété.

Maintenant que nous avons couvert ce que sont les threads et les méthodes fournies par l'API des threads, examinons quelques situations dans lesquelles nous pouvons utiliser des threads.

[capture]: ch13-01-closures.html#capturer-des-références-ou-déménager-la-propriété