## Acceptation des Arguments de Commande

Créons un nouveau projet avec, comme toujours, `cargo new`. Nous allons appeler notre projet `minigrep` pour le distinguer de l'outil `grep` que vous pourriez déjà avoir sur votre système :

```console
$ cargo new minigrep
     Projet binaire (application) `minigrep` créé
$ cd minigrep
```

La première tâche consiste à faire en sorte que `minigrep` accepte ses deux arguments de ligne de commande : le chemin du fichier et une chaîne à rechercher. C'est-à-dire, nous voulons pouvoir exécuter notre programme avec `cargo run`, deux tirets pour indiquer que les arguments suivants sont pour notre programme plutôt que pour `cargo`, une chaîne à rechercher et un chemin vers un fichier à rechercher, comme ceci :

```console
$ cargo run -- searchstring exemple-filename.txt
```

Pour l'instant, le programme généré par `cargo new` ne peut pas traiter les arguments que nous lui fournissons. Certaines bibliothèques existantes sur [crates.io](https://crates.io/) peuvent aider à écrire un programme qui accepte des arguments de ligne de commande, mais comme vous êtes en train d'apprendre ce concept, mettons en œuvre cette capacité nous-mêmes.

### Lecture des Valeurs d'Argument

Pour permettre à `minigrep` de lire les valeurs des arguments de ligne de commande que nous lui passons, nous aurons besoin de la fonction `std::env::args` fournie dans la bibliothèque standard de Rust. Cette fonction renvoie un itérateur des arguments de ligne de commande passés à `minigrep`. Nous couvrirons les itérateurs en détail dans [Chapitre 13][ch13]<!-- ignore -->. Pour l'instant, vous devez juste connaître deux détails sur les itérateurs : Les itérateurs produisent une série de valeurs, et nous pouvons appeler la méthode `collect` sur un itérateur pour le transformer en une collection, comme un vecteur, qui contient tous les éléments produits par l'itérateur.

Le code dans la Liste 12-1 permet à votre programme `minigrep` de lire tous les arguments de ligne de commande qui lui sont passés, puis de rassembler les valeurs dans un vecteur.

<Listing number="12-1" file-name="src/main.rs" caption="Collecte des arguments de ligne de commande dans un vecteur et impression des résultats">

```rust
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-01/src/main.rs}}
```

</Listing>

Tout d'abord, nous mettons le module `std::env` à portée avec une instruction `use` afin que nous puissions utiliser sa fonction `args`. Remarquez que la fonction `std::env::args` est imbriquée dans deux niveaux de modules. Comme nous en avons discuté dans [Chapitre 7][ch7-idiomatic-use]<!-- ignore -->, dans les cas où la fonction souhaitée est imbriquée dans plus d'un module, nous avons choisi de mettre le module parent à portée plutôt que la fonction. Ce faisant, nous pouvons facilement utiliser d'autres fonctions de `std::env`. C'est également moins ambigu que d'ajouter `use std::env::args` et d'appeler ensuite la fonction simplement avec `args`, car `args` pourrait facilement être confondu avec une fonction définie dans le module actuel.

> ### La Fonction `args` et l'Unicode Invalide
>
> Notez que `std::env::args` panique si un argument contient de l'Unicode invalide. Si votre programme doit accepter des arguments contenant de l'Unicode invalide, utilisez `std::env::args_os` à la place. Cette fonction renvoie un itérateur qui produit des valeurs `OsString` plutôt que des valeurs `String`. Nous avons choisi d'utiliser `std::env::args` ici pour plus de simplicité, car les valeurs `OsString` diffèrent selon la plateforme et sont plus complexes à manipuler que les valeurs `String`.

Sur la première ligne de `main`, nous appelons `env::args`, et nous utilisons immédiatement `collect` pour transformer l'itérateur en un vecteur contenant toutes les valeurs produites par l'itérateur. Nous pouvons utiliser la fonction `collect` pour créer de nombreux types de collections, c'est pourquoi nous annotons explicitement le type de `args` pour spécifier que nous voulons un vecteur de chaînes. Bien que vous n'ayez que rarement besoin d'annoter des types en Rust, `collect` est une fonction que vous devez souvent annoter parce que Rust n'est pas capable d'inférer le type de collection que vous voulez.

Enfin, nous imprimons le vecteur en utilisant la macro de débogage. Essayons d'exécuter le code d'abord sans arguments, puis avec deux arguments :

```console
{{#include ../listings/ch12-an-io-project/listing-12-01/output.txt}}
```

```console
{{#include ../listings/ch12-an-io-project/output-only-01-with-args/output.txt}}
```

Remarquez que la première valeur du vecteur est `"target/debug/minigrep"`, qui est le nom de notre binaire. Cela correspond au comportement de la liste des arguments en C, permettant aux programmes d'utiliser le nom par lequel ils ont été invoqués lors de leur exécution. Il est souvent pratique d'avoir accès au nom du programme au cas où vous voudriez l'imprimer dans des messages ou modifier le comportement du programme en fonction de l'alias de ligne de commande utilisé pour invoquer le programme. Mais aux fins de ce chapitre, nous l'ignorerons et ne conserverons que les deux arguments dont nous avons besoin.

### Enregistrement des Valeurs d'Argument dans des Variables

Le programme est actuellement capable d'accéder aux valeurs spécifiées en tant qu'arguments de ligne de commande. Nous devons maintenant enregistrer les valeurs des deux arguments dans des variables afin que nous puissions utiliser ces valeurs tout au long du reste du programme. Nous faisons cela dans la Liste 12-2.

<Listing number="12-2" file-name="src/main.rs" caption="Création de variables pour contenir l'argument de requête et l'argument de chemin de fichier">

```rust,should_panic,noplayground
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-02/src/main.rs}}
```

</Listing>

Comme nous l'avons vu lorsque nous avons imprimé le vecteur, le nom du programme occupe la première valeur du vecteur à `args[0]`, donc nous commençons les arguments à l'index 1. Le premier argument que `minigrep` prend est la chaîne que nous recherchons, donc nous mettons une référence au premier argument dans la variable `query`. Le deuxième argument sera le chemin du fichier, nous mettons donc une référence au deuxième argument dans la variable `file_path`.

Nous imprimons temporairement les valeurs de ces variables pour prouver que le code fonctionne comme prévu. Exécutons à nouveau ce programme avec les arguments `test` et `sample.txt` :

```console
{{#include ../listings/ch12-an-io-project/listing-12-02/output.txt}}
```

Super, le programme fonctionne ! Les valeurs des arguments dont nous avons besoin sont enregistrées dans les bonnes variables. Plus tard, nous ajouterons un peu de gestion des erreurs pour traiter certaines situations erronées potentielles, comme lorsque l'utilisateur ne fournit aucun argument ; pour l'instant, nous allons ignorer cette situation et travailler sur l'ajout des capacités de lecture de fichiers à la place.

[ch13]: ch13-00-functional-features.html
[ch7-idiomatic-use]: ch07-04-bringing-paths-into-scope-with-the-use-keyword.html#creating-idiomatic-use-paths