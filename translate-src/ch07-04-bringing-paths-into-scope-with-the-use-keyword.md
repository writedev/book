## Amener des chemins dans la portée avec le mot-clé `use`

Devoir écrire les chemins pour appeler des fonctions peut sembler peu pratique et répétitif. Dans la Listing 7-7, que nous choisissions le chemin absolu ou relatif à la fonction `add_to_waitlist`, chaque fois que nous voulions appeler `add_to_waitlist`, nous devions également spécifier `front_of_house` et `hosting`. Heureusement, il existe un moyen de simplifier ce processus : nous pouvons créer un raccourci vers un chemin avec le mot-clé `use` une seule fois, puis utiliser le nom plus court partout ailleurs dans la portée.

Dans la Listing 7-11, nous amenons le module `crate::front_of_house::hosting` dans la portée de la fonction `eat_at_restaurant` afin que nous n'ayons qu'à spécifier `hosting::add_to_waitlist` pour appeler la fonction `add_to_waitlist` dans `eat_at_restaurant`.

<Listing number="7-11" file-name="src/lib.rs" caption="Amener un module dans la portée avec `use`">

```rust,noplayground,test_harness
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-11/src/lib.rs}}
```

</Listing>

Ajouter `use` et un chemin dans une portée est similaire à la création d'un lien symbolique dans le système de fichiers. En ajoutant `use crate::front_of_house::hosting` dans la racine du crate, `hosting` est maintenant un nom valide dans cette portée, comme si le module `hosting` avait été défini à la racine du crate. Les chemins amenés dans la portée avec `use` respectent également la confidentialité, comme tout autre chemin.

Notez que `use` ne crée le raccourci que pour la portée particulière dans laquelle `use` se trouve. La Listing 7-12 déplace la fonction `eat_at_restaurant` dans un nouveau module enfant nommé `customer`, qui est alors une portée différente de l'instruction `use`, donc le corps de la fonction ne compilera pas.

<Listing number="7-12" file-name="src/lib.rs" caption="Une instruction `use` ne s'applique que dans la portée dans laquelle elle se trouve.">

```rust,noplayground,test_harness,does_not_compile,ignore
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-12/src/lib.rs}}
```

</Listing>

L'erreur du compilateur montre que le raccourci ne s'applique plus dans le module `customer` :

```console
{{#include ../listings/ch07-managing-growing-projects/listing-07-12/output.txt}}
```

Remarquez qu'il y a également un avertissement indiquant que `use` n'est plus utilisé dans sa portée ! Pour corriger ce problème, déplacez le `use` dans le module `customer` ou référencez le raccourci dans le module parent avec `super::hosting` dans le module enfant `customer`.

### Créer des chemins `use` idiomatiques

Dans la Listing 7-11, vous vous êtes peut-être demandé pourquoi nous avons spécifié `use crate::front_of_house::hosting` puis appelé `hosting::add_to_waitlist` dans `eat_at_restaurant`, plutôt que de spécifier le chemin `use` jusqu'à la fonction `add_to_waitlist` pour obtenir le même résultat, comme dans la Listing 7-13.

<Listing number="7-13" file-name="src/lib.rs" caption="Amener la fonction `add_to_waitlist` dans la portée avec `use`, ce qui est non idiomatique">

```rust,noplayground,test_harness
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-13/src/lib.rs}}
```

</Listing>

Bien que les Listings 7-11 et 7-13 accomplissent la même tâche, la Listing 7-11 est la manière idiomatique d'amener une fonction dans la portée avec `use`. Amener le module parent de la fonction dans la portée avec `use` signifie que nous devons spécifier le module parent lors de l'appel de la fonction. Spécifier le module parent lors de l'appel de la fonction clarifie que la fonction n'est pas définie localement tout en minimisant la répétition du chemin complet. Le code dans la Listing 7-13 n'est pas clair quant à l'endroit où `add_to_waitlist` est défini.

En revanche, lorsqu'on amène des structs, des enums et d'autres éléments avec `use`, il est idiomatique de spécifier le chemin complet. La Listing 7-14 montre la manière idiomatique d'amener la struct `HashMap` de la bibliothèque standard dans la portée d'un crate binaire.

<Listing number="7-14" file-name="src/main.rs" caption="Amener `HashMap` dans la portée de manière idiomatique">

```rust
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-14/src/main.rs}}
```

</Listing>

Il n'y a pas de raison forte derrière cet idiome : c'est juste la convention qui a émergé, et les gens se sont habitués à lire et à écrire du code Rust de cette manière.

L'exception à cet idiome est si nous amenons deux éléments ayant le même nom dans la portée avec des instructions `use`, car Rust ne le permet pas. La Listing 7-15 montre comment amener deux types `Result` ayant le même nom mais des modules parents différents, et comment les référencer.

<Listing number="7-15" file-name="src/lib.rs" caption="Amener deux types ayant le même nom dans la même portée nécessite d'utiliser leurs modules parents.">

```rust,noplayground
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-15/src/lib.rs:here}}
```

</Listing>

Comme vous pouvez le voir, l'utilisation des modules parents distingue les deux types `Result`. Si nous spécifions plutôt `use std::fmt::Result` et `use std::io::Result`, nous aurions deux types `Result` dans la même portée, et Rust ne saurait pas lequel nous voulions dire lorsque nous utiliserions `Result`.

### Fournir de nouveaux noms avec le mot-clé `as`

Il existe une autre solution au problème d'amener deux types du même nom dans la même portée avec `use` : après le chemin, nous pouvons spécifier `as` et un nouveau nom local, ou _alias_, pour le type. La Listing 7-16 montre une autre façon d'écrire le code de la Listing 7-15 en renommant l'un des deux types `Result` en utilisant `as`.

<Listing number="7-16" file-name="src/lib.rs" caption="Renommer un type lorsqu'il est amené dans la portée avec le mot-clé `as`">

```rust,noplayground
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-16/src/lib.rs:here}}
```

</Listing>

Dans la deuxième instruction `use`, nous avons choisi le nouveau nom `IoResult` pour le type `std::io::Result`, ce qui n'entrera pas en conflit avec le `Result` de `std::fmt` que nous avons également amené dans la portée. Les Listings 7-15 et 7-16 sont considérés comme idiomatiques, donc le choix vous appartient !

### Ré-exporter des noms avec `pub use`

Lorsque nous amenons un nom dans la portée avec le mot-clé `use`, le nom est privé à la portée dans laquelle nous l'avons importé. Pour permettre aux codes externes de se référer à ce nom comme s'il avait été défini dans cette portée, nous pouvons combiner `pub` et `use`. Cette technique est appelée _ré-exportation_ car nous amenons un élément dans la portée tout en rendant cet élément disponible pour d'autres afin qu'ils puissent l'amener dans leur propre portée.

La Listing 7-17 montre le code de la Listing 7-11 avec `use` dans le module racine remplacé par `pub use`.

<Listing number="7-17" file-name="src/lib.rs" caption="Rendre un nom disponible pour tout code à partir d'une nouvelle portée avec `pub use`">

```rust,noplayground,test_harness
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-17/src/lib.rs}}
```

</Listing>

Avant ce changement, le code externe devait appeler la fonction `add_to_waitlist` en utilisant le chemin `restaurant::front_of_house::hosting::add_to_waitlist()`, ce qui aurait également nécessité que le module `front_of_house` soit marqué comme `pub`. Maintenant que ce `pub use` a ré-exporté le module `hosting` depuis le module racine, le code externe peut utiliser le chemin `restaurant::hosting::add_to_waitlist()` à la place.

La ré-exportation est utile lorsque la structure interne de votre code est différente de la façon dont les programmeurs appelant votre code penseraient au domaine. Par exemple, dans cette métaphore de restaurant, les personnes gérant le restaurant pensent à "l'avant de la maison" et "l'arrière de la maison". Mais les clients visitant un restaurant ne penseront probablement pas aux parties du restaurant sous ces termes. Avec `pub use`, nous pouvons écrire notre code avec une structure mais exposer une structure différente. Cela rend notre bibliothèque bien organisée pour les programmeurs travaillant sur la bibliothèque et pour ceux appelant la bibliothèque. Nous examinerons un autre exemple de `pub use` et comment cela affecte la documentation de votre crate dans [“Exporter une API publique pratique”][ch14-pub-use]<!-- ignore --> au Chapitre 14.

### Utilisation de paquets externes

Dans le Chapitre 2, nous avons programmé un projet de jeu de devinettes qui utilisait un paquet externe appelé `rand` pour obtenir des nombres aléatoires. Pour utiliser `rand` dans notre projet, nous avons ajouté cette ligne à _Cargo.toml_ :

<!-- Lorsque vous mettez à jour la version de `rand` utilisée, mettez également à jour la version de
`rand` utilisée dans ces fichiers pour qu'ils correspondent tous :

* ch01-01-installation.md
* ch02-00-guessing-game-tutorial.md
* ch14-03-cargo-workspaces.md
-->

<Listing file-name="Cargo.toml">

```toml
{{#include ../listings/ch02-guessing-game-tutorial/listing-02-02/Cargo.toml:9:}}
```

</Listing>

Ajouter `rand` comme dépendance dans _Cargo.toml_ indique à Cargo de télécharger le paquet `rand` et toutes ses dépendances depuis [crates.io](https://crates.io/) et de rendre `rand` disponible pour notre projet.

Ensuite, pour amener les définitions de `rand` dans la portée de notre paquet, nous avons ajouté une ligne `use` en commençant par le nom du crate, `rand`, et en énumérant les éléments que nous souhaitions amener dans la portée. Rappelez-vous qu'au [“Générer un nombre aléatoire”][rand]<!-- ignore --> dans le Chapitre 2, nous avons amené des éléments dans le module `rand::prelude` dans la portée et appelé la fonction `rand::rng` :

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-03/src/main.rs:ch07-04}}
```

Les membres de la communauté Rust ont rendu de nombreux paquets disponibles sur [crates.io](https://crates.io/), et les intégrer dans votre paquet implique ces mêmes étapes : les énumérer dans le fichier _Cargo.toml_ de votre paquet et utiliser `use` pour amener des éléments de leurs crates dans la portée.

Notez que la bibliothèque standard `std` est également un crate qui est externe à notre paquet. Puisque la bibliothèque standard est livrée avec le langage Rust, nous n'avons pas besoin de modifier _Cargo.toml_ pour inclure `std`. Mais nous devons nous y référer avec `use` pour amener des éléments de là dans la portée de notre paquet. Par exemple, pour `HashMap`, nous utiliserions cette ligne :

```rust
use std::collections::HashMap;
```

Il s'agit d'un chemin absolu commençant par `std`, le nom du crate de la bibliothèque standard.

### Utilisation de chemins imbriqués pour nettoyer les listes `use`

Si nous utilisons plusieurs éléments définis dans le même crate ou le même module, lister chaque élément sur sa propre ligne peut prendre beaucoup d'espace vertical dans nos fichiers. Par exemple, ces deux instructions `use` que nous avions dans le jeu de devinettes dans la Listing 2-4 amènent des éléments de `std` dans la portée :

<Listing file-name="src/main.rs">

```rust,ignore
{{#rustdoc_include ../listings/ch07-managing-growing-projects/no-listing-01-use-std-unnested/src/main.rs:here}}
```

</Listing>

Au lieu de cela, nous pouvons utiliser des chemins imbriqués pour amener les mêmes éléments dans la portée en une seule ligne. Nous faisons cela en spécifiant la partie commune du chemin, suivie de deux points, puis des accolades autour d'une liste des parties des chemins qui diffèrent, comme montré dans la Listing 7-18.

<Listing number="7-18" file-name="src/main.rs" caption="Spécifier un chemin imbriqué pour amener plusieurs éléments avec le même préfixe dans la portée">

```rust,ignore
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-18/src/main.rs:here}}
```

</Listing>

Dans des programmes plus grands, amener de nombreux éléments dans la portée du même crate ou module en utilisant des chemins imbriqués peut réduire considérablement le nombre d'instructions `use` séparées nécessaires !

Nous pouvons utiliser un chemin imbriqué à n'importe quel niveau d'un chemin, ce qui est utile lorsque nous combinons deux instructions `use` qui partagent un sous-chemin. Par exemple, la Listing 7-19 montre deux instructions `use` : l'une amène `std::io` dans la portée et l'autre amène `std::io::Write` dans la portée.

<Listing number="7-19" file-name="src/lib.rs" caption="Deux instructions `use` où l'une est un sous-chemin de l'autre">

```rust,noplayground
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-19/src/lib.rs}}
```

</Listing>

La partie commune de ces deux chemins est `std::io`, et c'est le chemin complet. Pour fusionner ces deux chemins en une seule instruction `use`, nous pouvons utiliser `self` dans le chemin imbriqué, comme montré dans la Listing 7-20.

<Listing number="7-20" file-name="src/lib.rs" caption="Combinaison des chemins de la Listing 7-19 en une seule instruction `use`">

```rust,noplayground
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-20/src/lib.rs}}
```

</Listing>

Cette ligne amène `std::io` et `std::io::Write` dans la portée.

### Importer des éléments avec l'opérateur glob

Si nous voulons amener _tous_ les éléments publics définis dans un chemin dans la portée, nous pouvons spécifier ce chemin suivi de l'opérateur glob `*` :

```rust
use std::collections::*;
```

Cette instruction `use` amène tous les éléments publics définis dans `std::collections` dans la portée actuelle. Soyez prudent lorsque vous utilisez l'opérateur glob ! Le glob peut rendre plus difficile de savoir quels noms sont dans la portée et où un nom utilisé dans votre programme a été défini. De plus, si la dépendance change ses définitions, ce que vous avez importé change également, ce qui peut entraîner des erreurs de compilation lorsque vous mettez à jour la dépendance si celle-ci ajoute une définition avec le même nom qu'une définition de votre part dans la même portée.

L'opérateur glob est souvent utilisé lors des tests pour amener tout ce qui est sous test dans le module `tests` ; nous en parlerons dans [“Comment écrire des tests”][writing-tests]<!-- ignore --> au Chapitre 11. L'opérateur glob est également parfois utilisé dans le cadre du modèle de préambule : consultez [la documentation de la bibliothèque standard](../std/prelude/index.html#other-preludes)<!-- ignore --> pour plus d'informations sur ce modèle.

[ch14-pub-use]: ch14-02-publishing-to-crates-io.html#exporting-a-convenient-public-api
[rand]: ch02-00-guessing-game-tutorial.html#generating-a-random-number
[writing-tests]: ch11-01-writing-tests.html#how-to-write-tests