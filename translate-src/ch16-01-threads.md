## Utiliser des threads pour exécuter du code simultanément

Dans la plupart des systèmes d’exploitation actuels, le code d’un programme exécuté s’exécute dans un _processus_, et le système d’exploitation gère plusieurs processus à la fois. Au sein d’un programme, vous pouvez également avoir des parties indépendantes qui s’exécutent simultanément. Les fonctionnalités qui exécutent ces parties indépendantes sont appelées des _threads_. Par exemple, un serveur web peut utiliser plusieurs threads afin de répondre à plusieurs requêtes à la fois.

Répartir les calculs de votre programme sur plusieurs threads pour exécuter plusieurs tâches en même temps peut améliorer les performances, mais cela ajoute aussi de la complexité. Comme les threads peuvent s’exécuter simultanément, il n’y a aucune garantie inhérente quant à l’ordre dans lequel les parties de votre code exécutées sur des threads différents s’exécuteront. Cela peut entraîner des problèmes tels que :

- Des conditions de concurrence, dans lesquelles les threads accèdent aux données ou aux ressources dans un ordre incohérent
- Des interblocages, dans lesquels deux threads s’attendent mutuellement, empêchant les deux de continuer
- Des bogues qui ne surviennent que dans certaines situations et qu’il est difficile de reproduire et de corriger de manière fiable

Rust tente d’atténuer les effets négatifs liés à l’utilisation des threads, mais programmer dans un contexte multithread demande toujours une réflexion approfondie et nécessite une structure de code différente de celle des programmes exécutés sur un seul thread.

Les langages de programmation implémentent les threads de différentes façons, et de nombreux systèmes d’exploitation fournissent une API que le langage de programmation peut appeler pour créer de nouveaux threads. La bibliothèque standard de Rust utilise un modèle d’implémentation des threads _1:1_, dans lequel un programme utilise un thread du système d’exploitation pour chaque thread du langage. Il existe des crates qui implémentent d’autres modèles de threads, avec des compromis différents de ceux du modèle 1:1. (Le système asynchrone de Rust, que nous verrons au chapitre suivant, offre également une autre approche de la concurrence.)

### Créer un thread avec `spawn`

Pour créer un thread, nous appelons la fonction `thread::spawn` et lui transmettons une fermeture (nous avons parlé des fermetures au chapitre 13) contenant le code que nous voulons exécuter dans le nouveau thread. L’exemple de la Listing 16-1 affiche du texte depuis le thread principal et d’autres textes depuis un nouveau thread.

<Listing number="16-1" file-name="src/main.rs" caption="Créer un nouveau thread pour afficher une chose pendant que le thread principal en affiche une autre">

```rust
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-01/src/main.rs}}
```

</Listing>

Notez que lorsque le thread principal d’un programme Rust se termine, tous les threads lancés sont arrêtés, qu’ils aient terminé leur exécution ou non. La sortie de ce programme peut varier légèrement à chaque exécution, mais elle ressemblera à ce qui suit :

<!-- Not extracting output because changes to this output aren't significant;
the changes are likely to be due to the threads running differently rather than
changes in the compiler -->

```text
hi number 1 from the main thread!
hi number 1 from the spawned thread!
hi number 2 from the main thread!
hi number 2 from the spawned thread!
hi number 3 from the main thread!
hi number 3 from the spawned thread!
hi number 4 from the main thread!
hi number 4 from the spawned thread!
hi number 5 from the spawned thread!
```

Les appels à `thread::sleep` forcent un thread à suspendre son exécution pendant un court instant, ce qui permet à un autre thread de s’exécuter. Les threads alterneront probablement, mais cela n’est pas garanti : tout dépend de la façon dont votre système d’exploitation planifie les threads. Dans cette exécution, le thread principal a affiché du texte en premier, même si l’instruction d’affichage du thread lancé apparaît plus tôt dans le code. Et bien que nous ayons demandé au thread lancé d’afficher du texte jusqu’à ce que `i` atteigne `9`, il n’est arrivé qu’à `5` avant que le thread principal ne s’arrête.

Si vous exécutez ce code et ne voyez que la sortie du thread principal, ou ne constatez aucun chevauchement, essayez d’augmenter les nombres dans les plages afin de donner au système d’exploitation davantage d’occasions de basculer entre les threads.

<!-- Old headings. Do not remove or links may break. -->

<a id="waiting-for-all-threads-to-finish-using-join-handles"></a>

### Attendre la fin de tous les threads

Le code de la Listing 16-1 arrête non seulement prématurément le thread lancé la plupart du temps, à cause de la fin du thread principal, mais comme l’ordre d’exécution des threads n’est pas garanti, nous ne pouvons pas non plus garantir que le thread lancé s’exécutera !

Nous pouvons résoudre le problème du thread lancé qui ne s’exécute pas ou qui se termine prématurément en enregistrant la valeur de retour de `thread::spawn` dans une variable. Le type de retour de `thread::spawn` est `JoinHandle<T>`. Un `JoinHandle<T>` est une valeur possédée qui, lorsque nous appelons sa méthode `join`, attend la fin de son thread. La Listing 16-2 montre comment utiliser le `JoinHandle<T>` du thread créé dans la Listing 16-1 et comment appeler `join` pour s’assurer que le thread lancé se termine avant que `main` ne se termine.

<Listing number="16-2" file-name="src/main.rs" caption="Enregistrer un `JoinHandle<T>` renvoyé par `thread::spawn` pour garantir que le thread s’exécute jusqu’à son terme">

```rust
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-02/src/main.rs}}
```

</Listing>

Appeler `join` sur la poignée bloque le thread en cours d’exécution jusqu’à ce que le thread représenté par la poignée se termine. _Bloquer_ un thread signifie l’empêcher d’effectuer du travail ou de se terminer. Comme nous avons placé l’appel à `join` après la boucle `for` du thread principal, l’exécution de la Listing 16-2 devrait produire une sortie semblable à celle-ci :

<!-- Not extracting output because changes to this output aren't significant;
the changes are likely to be due to the threads running differently rather than
changes in the compiler -->

```text
hi number 1 from the main thread!
hi number 2 from the main thread!
hi number 1 from the spawned thread!
hi number 3 from the main thread!
hi number 2 from the spawned thread!
hi number 4 from the main thread!
hi number 3 from the spawned thread!
hi number 4 from the spawned thread!
hi number 5 from the spawned thread!
hi number 6 from the spawned thread!
hi number 7 from the spawned thread!
hi number 8 from the spawned thread!
hi number 9 from the spawned thread!
```

Les deux threads continuent d’alterner, mais le thread principal attend à cause de l’appel à `handle.join()` et ne se termine pas avant la fin du thread lancé.

Voyons maintenant ce qui se passe si nous déplaçons `handle.join()` avant la boucle `for` dans `main`, comme ceci :

<Listing file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch16-fearless-concurrency/no-listing-01-join-too-early/src/main.rs}}
```

</Listing>

Le thread principal attendra que le thread lancé se termine, puis exécutera sa boucle `for`. La sortie ne sera donc plus entrelacée, comme le montre l’exemple suivant :

<!-- Not extracting output because changes to this output aren't significant;
the changes are likely to be due to the threads running differently rather than
changes in the compiler -->

```text
hi number 1 from the spawned thread!
hi number 2 from the spawned thread!
hi number 3 from the spawned thread!
hi number 4 from the spawned thread!
hi number 5 from the spawned thread!
hi number 6 from the spawned thread!
hi number 7 from the spawned thread!
hi number 8 from the spawned thread!
hi number 9 from the spawned thread!
hi number 1 from the main thread!
hi number 2 from the main thread!
hi number 3 from the main thread!
hi number 4 from the main thread!
```

De petits détails, comme l’endroit où `join` est appelé, peuvent déterminer si vos threads s’exécutent ou non en même temps.

### Utiliser des fermetures `move` avec des threads

Nous utiliserons souvent le mot-clé `move` avec les fermetures transmises à `thread::spawn`, car la fermeture prend alors possession des valeurs qu’elle utilise dans son environnement, transférant ainsi la propriété de ces valeurs d’un thread à un autre. Dans [« Capturer des références ou transférer la propriété »][capture]<!-- ignore
--> au chapitre 13, nous avons parlé de `move` dans le contexte des fermetures. Nous allons maintenant nous concentrer davantage sur l’interaction entre `move` et `thread::spawn`.

Remarquez, dans la Listing 16-1, que la fermeture transmise à `thread::spawn` ne prend aucun argument : nous n’utilisons aucune donnée du thread principal dans le code du thread lancé. Pour utiliser des données du thread principal dans le thread lancé, la fermeture de ce dernier doit capturer les valeurs dont elle a besoin. La Listing 16-3 montre une tentative de création d’un vecteur dans le thread principal et de son utilisation dans le thread lancé. Cependant, cela ne fonctionnera pas encore, comme vous allez le voir.

<Listing number="16-3" file-name="src/main.rs" caption="Tenter d’utiliser dans un autre thread un vecteur créé par le thread principal">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-03/src/main.rs}}
```

</Listing>

La fermeture utilise `v`, elle va donc capturer `v` et l’intégrer à son environnement. Comme `thread::spawn` exécute cette fermeture dans un nouveau thread, nous devrions pouvoir accéder à `v` dans ce nouveau thread. Mais lorsque nous compilons cet exemple, nous obtenons l’erreur suivante :

```console
{{#include ../listings/ch16-fearless-concurrency/listing-16-03/output.txt}}
```

Rust _déduit_ comment capturer `v` et, comme `println!` n’a besoin que d’une référence à `v`, la fermeture tente d’emprunter `v`. Cependant, cela pose un problème : Rust ne peut pas savoir combien de temps le thread lancé s’exécutera, et ne sait donc pas si la référence à `v` sera toujours valide.

La Listing 16-4 présente un scénario dans lequel la référence à `v` risque davantage de ne pas être valide.

<Listing number="16-4" file-name="src/main.rs" caption="Un thread dont la fermeture tente de capturer une référence à `v` depuis un thread principal qui supprime `v`">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-04/src/main.rs}}
```

</Listing>

Si Rust nous autorisait à exécuter ce code, il serait possible que le thread lancé soit immédiatement relégué à l’arrière-plan sans s’exécuter du tout. Le thread lancé contient une référence à `v`, mais le thread principal supprime immédiatement `v` à l’aide de la fonction `drop`, dont nous avons parlé au chapitre 15. Ainsi, lorsque le thread lancé commence à s’exécuter, `v` n’est plus valide, et sa référence ne l’est pas non plus. Oh non !

Pour corriger l’erreur du compilateur dans la Listing 16-3, nous pouvons suivre le conseil du message d’erreur :

<!-- manual-regeneration
after automatic regeneration, look at listings/ch16-fearless-concurrency/listing-16-03/output.txt and copy the relevant part
-->

```text
help: to force the closure to take ownership of `v` (and any other referenced variables), use the `move` keyword
  |
6 |     let handle = thread::spawn(move || {
  |                                ++++
```

En ajoutant le mot-clé `move` avant la fermeture, nous la forçons à prendre possession des valeurs qu’elle utilise, au lieu de laisser Rust déduire qu’elle doit les emprunter. La modification de la Listing 16-3 présentée dans la Listing 16-5 compilera et s’exécutera comme prévu.

<Listing number="16-5" file-name="src/main.rs" caption="Utiliser le mot-clé `move` pour forcer une fermeture à prendre possession des valeurs qu’elle utilise">

```rust
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-05/src/main.rs}}
```

</Listing>

Nous pourrions être tentés d’essayer la même chose pour corriger le code de la Listing 16-4, dans lequel le thread principal appelle `drop`, en utilisant une fermeture `move`. Cependant, cette correction ne fonctionnera pas, car ce que la Listing 16-4 tente de faire est interdit pour une autre raison. Si nous ajoutions `move` à la fermeture, nous déplacerions `v` dans l’environnement de la fermeture et ne pourrions plus appeler `drop` dessus dans le thread principal. Nous obtiendrions alors cette erreur du compilateur :

```console
{{#include ../listings/ch16-fearless-concurrency/output-only-01-move-drop/output.txt}}
```

Les règles de propriété de Rust nous ont encore sauvés ! Nous avons obtenu une erreur avec le code de la Listing 16-3 parce que Rust se montrait prudent et n’empruntait `v` que pour le thread, ce qui signifiait que le thread principal pouvait, en théorie, invalider la référence du thread lancé. En indiquant à Rust de transférer la propriété de `v` au thread lancé, nous lui garantissons que le thread principal n’utilisera plus `v`. Si nous modifions la Listing 16-4 de la même manière, nous enfreignons alors les règles de propriété en essayant d’utiliser `v` dans le thread principal. Le mot-clé `move` remplace le comportement prudent par défaut de Rust, qui consiste à emprunter les valeurs ; il ne nous permet pas d’enfreindre les règles de propriété.

Maintenant que nous avons vu ce que sont les threads et les méthodes fournies par l’API des threads, examinons quelques situations dans lesquelles nous pouvons utiliser des threads.

[capture]: ch13-01-closures.html#capturing-references-or-moving-ownership