## Faire entrer des chemins dans la portée avec le mot-clé `use`

Écrire les chemins complets pour appeler des fonctions peut sembler peu pratique et répétitif. Dans la Listing 7-7, que nous ayons choisi le chemin absolu ou relatif vers la fonction `add_to_waitlist`, chaque fois que nous voulions appeler `add_to_waitlist`, nous devions également préciser `front_of_house` et `hosting`. Heureusement, il existe un moyen de simplifier ce processus : nous pouvons créer un raccourci vers un chemin avec le mot-clé `use`, puis utiliser le nom plus court partout ailleurs dans la portée.

Dans la Listing 7-11, nous faisons entrer le module `crate::front_of_house::hosting` dans la portée de la fonction `eat_at_restaurant`, afin de n’avoir à préciser que `hosting::add_to_waitlist` pour appeler la fonction `add_to_waitlist` dans `eat_at_restaurant`.

<Listing number="7-11" file-name="src/lib.rs" caption="Faire entrer un module dans la portée avec `use`">

```rust,noplayground,test_harness
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-11/src/lib.rs}}
```

</Listing>

Ajouter `use` et un chemin dans une portée revient à créer un lien symbolique dans le système de fichiers. En ajoutant `use crate::front_of_house::hosting` à la racine de la caisse, `hosting` devient un nom valide dans cette portée, comme si le module `hosting` avait été défini à la racine de la caisse. Les chemins introduits dans la portée avec `use` vérifient également la confidentialité, comme tous les autres chemins.

Notez que `use` ne crée un raccourci que dans la portée où il apparaît. Dans la Listing 7-12, la fonction `eat_at_restaurant` est déplacée dans un nouveau module enfant nommé `customer`, dont la portée est différente de celle de l’instruction `use` ; le corps de la fonction ne sera donc pas compilé.

<Listing number="7-12" file-name="src/lib.rs" caption="Une instruction `use` ne s’applique que dans la portée où elle se trouve.">

```rust,noplayground,test_harness,does_not_compile,ignore
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-12/src/lib.rs}}
```

</Listing>

L’erreur du compilateur indique que le raccourci ne s’applique plus dans le module `customer` :

```console
{{#include ../listings/ch07-managing-growing-projects/listing-07-12/output.txt}}
```

Notez qu’un avertissement indique également que `use` n’est plus utilisé dans sa portée ! Pour résoudre ce problème, déplacez également `use` dans le module `customer`, ou faites référence au raccourci dans le module parent avec `super::hosting` depuis le module enfant `customer`.

### Créer des chemins `use` idiomatiques

Dans la Listing 7-11, vous vous êtes peut-être demandé pourquoi nous avons indiqué `use
crate::front_of_house::hosting` puis appelé `hosting::add_to_waitlist` dans
`eat_at_restaurant`, plutôt que d’indiquer le chemin `use` jusqu’à la fonction
`add_to_waitlist` pour obtenir le même résultat, comme dans la Listing 7-13.

<Listing number="7-13" file-name="src/lib.rs" caption="Faire entrer la fonction `add_to_waitlist` dans la portée avec `use`, une pratique non idiomatique">

```rust,noplayground,test_harness
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-13/src/lib.rs}}
```

</Listing>

Bien que les Listings 7-11 et 7-13 accomplissent la même tâche, la Listing 7-11 est la manière idiomatique de faire entrer une fonction dans la portée avec `use`. Faire entrer le module parent de la fonction dans la portée avec `use` signifie que nous devons préciser le module parent lorsque nous appelons la fonction. Cela indique clairement que la fonction n’est pas définie localement, tout en réduisant au minimum la répétition du chemin complet. Le code de la Listing 7-13 ne permet pas de savoir clairement où `add_to_waitlist` est définie.

En revanche, lorsqu’on fait entrer des structures, des énumérations et d’autres éléments dans la portée avec `use`, il est idiomatique d’indiquer le chemin complet. La Listing 7-14 présente la manière idiomatique de faire entrer la structure `HashMap` de la bibliothèque standard dans la portée d’une caisse binaire.

<Listing number="7-14" file-name="src/main.rs" caption="Faire entrer `HashMap` dans la portée de manière idiomatique">

```rust
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-14/src/main.rs}}
```

</Listing>

Cette convention ne repose sur aucune raison particulière : elle s’est simplement imposée, et les gens se sont habitués à lire et à écrire du code Rust de cette manière.

Cette convention admet une exception : si nous faisons entrer dans la portée, avec des instructions `use`, deux éléments portant le même nom, ce que Rust n’autorise pas. La Listing 7-15 montre comment faire entrer dans la portée deux types `Result` portant le même nom mais provenant de modules parents différents, et comment les désigner.

<Listing number="7-15" file-name="src/lib.rs" caption="Pour faire entrer deux types portant le même nom dans une même portée, il faut utiliser leurs modules parents.">

```rust,noplayground
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-15/src/lib.rs:here}}
```

</Listing>

Comme vous pouvez le constater, utiliser les modules parents permet de distinguer les deux types `Result`. Si nous avions plutôt indiqué `use std::fmt::Result` et `use std::io::Result`, nous aurions eu deux types `Result` dans la même portée, et Rust n’aurait pas su lequel nous voulions désigner en utilisant `Result`.

### Attribuer de nouveaux noms avec le mot-clé `as`

Il existe une autre solution au problème consistant à faire entrer dans une même portée deux types portant le même nom avec `use` : après le chemin, nous pouvons indiquer `as`, suivi d’un nouveau nom local, ou _alias_, pour le type. La Listing 7-16 montre une autre manière d’écrire le code de la Listing 7-15, en renommant l’un des deux types `Result` avec `as`.

<Listing number="7-16" file-name="src/lib.rs" caption="Renommer un type lorsqu’il est introduit dans la portée avec le mot-clé `as`">

```rust,noplayground
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-16/src/lib.rs:here}}
```

</Listing>

Dans la deuxième instruction `use`, nous avons choisi le nouveau nom `IoResult` pour le type `std::io::Result`, qui n’entre donc pas en conflit avec le type `Result` de `std::fmt`, que nous avons également fait entrer dans la portée. Les Listings 7-15 et 7-16 sont toutes deux considérées comme idiomatiques : le choix vous appartient !

### Réexporter des noms avec `pub use`

Lorsque nous faisons entrer un nom dans une portée avec le mot-clé `use`, ce nom est privé dans la portée où nous l’avons importé. Pour permettre au code situé en dehors de cette portée de faire référence à ce nom comme s’il y avait été défini, nous pouvons combiner `pub` et `use`. Cette technique s’appelle la _réexportation_, car nous faisons entrer un élément dans une portée tout en le rendant accessible à d’autres, qui peuvent à leur tour le faire entrer dans leur portée.

La Listing 7-17 présente le code de la Listing 7-11, où `use` dans le module racine a été remplacé par `pub use`.

<Listing number="7-17" file-name="src/lib.rs" caption="Rendre un nom accessible à tout code depuis une nouvelle portée avec `pub use`">

```rust,noplayground,test_harness
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-17/src/lib.rs}}
```

</Listing>

Avant cette modification, le code externe devait appeler la fonction `add_to_waitlist` en utilisant le chemin
`restaurant::front_of_house::hosting::add_to_waitlist()`, ce qui aurait également nécessité que le module `front_of_house` soit marqué comme `pub`. Maintenant que ce `pub
use` a réexporté le module `hosting` depuis le module racine, le code externe peut plutôt utiliser le chemin `restaurant::hosting::add_to_waitlist()`.

La réexportation est utile lorsque la structure interne de votre code diffère de la manière dont les programmeurs qui l’utilisent envisagent le domaine concerné. Par exemple, dans la métaphore du restaurant, les personnes qui le gèrent pensent en termes de « salle » et de « cuisine ». Mais les clients qui le fréquentent ne pensent probablement pas aux différentes parties du restaurant en ces termes. Avec `pub
use`, nous pouvons écrire notre code selon une structure et en exposer une autre. Cela permet d’organiser efficacement notre bibliothèque, aussi bien pour les programmeurs qui y travaillent que pour ceux qui l’utilisent. Nous verrons un autre exemple de `pub use`, ainsi que son effet sur la documentation de votre caisse, dans [« Exporter une API publique pratique »][ch14-pub-use]<!-- ignore --> au chapitre 14.

### Utiliser des paquets externes

Au chapitre 2, nous avons programmé un jeu de devinettes qui utilisait un paquet externe appelé `rand` pour générer des nombres aléatoires. Pour utiliser `rand` dans notre projet, nous avons ajouté cette ligne à _Cargo.toml_ :

<!-- When updating the version of `rand` used, also update the version of
`rand` used in these files so they all match:

* ch01-01-installation.md
* ch02-00-guessing-game-tutorial.md
* ch14-03-cargo-workspaces.md
-->

<Listing file-name="Cargo.toml">

```toml
{{#include ../listings/ch02-guessing-game-tutorial/listing-02-02/Cargo.toml:9:}}
```

</Listing>

Ajouter `rand` comme dépendance dans _Cargo.toml_ indique à Cargo de télécharger le paquet `rand` ainsi que toutes ses dépendances depuis [crates.io](https://crates.io/) et de rendre `rand` disponible dans notre projet.

Ensuite, pour faire entrer les définitions de `rand` dans la portée de notre paquet, nous avons ajouté une ligne `use` commençant par le nom de la caisse, `rand`, suivie des éléments que nous voulions faire entrer dans la portée. Rappelez-vous qu’au chapitre 2, dans [« Générer un nombre aléatoire »][rand]<!-- ignore -->, nous avons fait entrer dans la portée des éléments du module `rand::prelude` et appelé la fonction `rand::rng` :

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-03/src/main.rs:ch07-04}}
```

Les membres de la communauté Rust ont mis de nombreux paquets à disposition sur [crates.io](https://crates.io/), et l’ajout de l’un d’eux à votre paquet suit les mêmes étapes : le répertorier dans le fichier _Cargo.toml_ de votre paquet et utiliser `use` pour faire entrer dans la portée des éléments de leurs caisses.

Notez que la bibliothèque standard `std` est également une caisse externe à notre paquet. Comme elle est fournie avec le langage Rust, nous n’avons pas besoin de modifier _Cargo.toml_ pour inclure `std`. Mais nous devons la référencer avec `use` pour faire entrer ses éléments dans la portée de notre paquet. Par exemple, pour utiliser `HashMap`, nous écririons cette ligne :

```rust
use std::collections::HashMap;
```

Il s’agit d’un chemin absolu qui commence par `std`, le nom de la caisse de la bibliothèque standard.

<!-- Old headings. Do not remove or links may break. -->

<a id="using-nested-paths-to-clean-up-large-use-lists"></a>

### Utiliser des chemins imbriqués pour simplifier les listes `use`

Si nous utilisons plusieurs éléments définis dans la même caisse ou le même module, indiquer chaque élément sur sa propre ligne peut occuper beaucoup d’espace vertical dans nos fichiers. Par exemple, ces deux instructions `use`, utilisées dans le jeu de devinettes de la Listing 2-4, font entrer des éléments de `std` dans la portée :

<Listing file-name="src/main.rs">

```rust,ignore
{{#rustdoc_include ../listings/ch07-managing-growing-projects/no-listing-01-use-std-unnested/src/main.rs:here}}
```

</Listing>

Nous pouvons plutôt utiliser des chemins imbriqués pour faire entrer ces mêmes éléments dans la portée sur une seule ligne. Pour cela, nous indiquons la partie commune du chemin, suivie de deux deux-points, puis plaçons entre accolades une liste des éléments qui diffèrent dans les chemins, comme le montre la Listing 7-18.

<Listing number="7-18" file-name="src/main.rs" caption="Indiquer un chemin imbriqué pour faire entrer dans la portée plusieurs éléments partageant le même préfixe">

```rust,ignore
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-18/src/main.rs:here}}
```

</Listing>

Dans les programmes de grande taille, utiliser des chemins imbriqués pour faire entrer dans la portée de nombreux éléments provenant de la même caisse ou du même module peut considérablement réduire le nombre d’instructions `use` distinctes nécessaires !

Nous pouvons utiliser un chemin imbriqué à n’importe quel niveau d’un chemin, ce qui est utile pour combiner deux instructions `use` qui partagent un sous-chemin. Par exemple, la Listing 7-19 présente deux instructions `use` : l’une fait entrer `std::io` dans la portée et l’autre fait entrer `std::io::Write` dans la portée.

<Listing number="7-19" file-name="src/lib.rs" caption="Deux instructions `use`, dont l’une est un sous-chemin de l’autre">

```rust,noplayground
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-19/src/lib.rs}}
```

</Listing>

La partie commune de ces deux chemins est `std::io`, qui constitue le premier chemin complet. Pour fusionner ces deux chemins en une seule instruction `use`, nous pouvons utiliser `self` dans le chemin imbriqué, comme le montre la Listing 7-20.

<Listing number="7-20" file-name="src/lib.rs" caption="Combiner les chemins de la Listing 7-19 en une seule instruction `use`">

```rust,noplayground
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-20/src/lib.rs}}
```

</Listing>

Cette ligne fait entrer `std::io` et `std::io::Write` dans la portée.

<!-- Old headings. Do not remove or links may break. -->

<a id="the-glob-operator"></a>

### Importer des éléments avec l’opérateur glob

Si nous voulons faire entrer dans la portée _tous_ les éléments publics définis dans un chemin, nous pouvons faire suivre ce chemin de l’opérateur glob `*` :

```rust
use std::collections::*;
```

Cette instruction `use` fait entrer dans la portée actuelle tous les éléments publics définis dans `std::collections`. Faites preuve de prudence lorsque vous utilisez l’opérateur glob ! Celui-ci peut rendre plus difficile l’identification des noms présents dans la portée et de l’endroit où un nom utilisé dans votre programme a été défini. De plus, si la dépendance modifie ses définitions, vos importations changent elles aussi. Lorsque vous mettez à niveau la dépendance, cela peut entraîner des erreurs de compilation si elle ajoute, par exemple, une définition portant le même nom qu’une définition de votre code dans la même portée.

L’opérateur glob est souvent utilisé lors des tests pour faire entrer dans le module `tests` tous les éléments testés ; nous en parlerons dans [« Comment écrire des tests »][writing-tests]<!-- ignore --> au chapitre 11. L’opérateur glob est également parfois utilisé dans le cadre du modèle de préambule : consultez [la documentation de la bibliothèque standard](../std/prelude/index.html#other-preludes)<!-- ignore --> pour en savoir plus sur ce modèle.

[ch14-pub-use]: ch14-02-publishing-to-crates-io.html#exporting-a-convenient-public-api
[rand]: ch02-00-guessing-game-tutorial.html#generating-a-random-number
[writing-tests]: ch11-01-writing-tests.html#how-to-write-tests