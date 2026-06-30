## Ramener des Chemins dans le Scope avec le Mot Clé `use`

Avoir à écrire les chemins pour appeler des fonctions peut sembler peu pratique et répétitif. Dans la Liste 7-7, que nous choisissions le chemin absolu ou relatif vers la fonction `add_to_waitlist`, chaque fois que nous voulions appeler `add_to_waitlist`, nous devions également spécifier `front_of_house` et `hosting`. Heureusement, il existe un moyen de simplifier ce processus : nous pouvons créer un raccourci vers un chemin avec le mot clé `use` une fois, puis utiliser le nom plus court partout ailleurs dans le scope.

Dans la Liste 7-11, nous apportons le module `crate::front_of_house::hosting` dans le scope de la fonction `eat_at_restaurant`, de sorte que nous n'ayons qu'à spécifier `hosting::add_to_waitlist` pour appeler la fonction `add_to_waitlist` dans `eat_at_restaurant`.

<Listing number="7-11" file-name="src/lib.rs" caption="Ramener un module dans le scope avec `use`">

```rust,noplayground,test_harness
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-11/src/lib.rs}}
```

</Listing>

Ajouter `use` et un chemin dans un scope est similaire à créer un lien symbolique dans le système de fichiers. En ajoutant `use crate::front_of_house::hosting` dans la racine du crate, `hosting` est maintenant un nom valide dans ce scope, comme si le module `hosting` avait été défini dans la racine du crate. Les chemins apportés dans le scope avec `use` vérifient également la confidentialité, comme tout autre chemin.

Notez que `use` ne crée le raccourci que pour le scope particulier dans lequel il se trouve. La Liste 7-12 déplace la fonction `eat_at_restaurant` dans un nouveau module enfant nommé `customer`, qui est alors un scope différent de la déclaration `use`, donc le corps de la fonction ne compilera pas.

<Listing number="7-12" file-name="src/lib.rs" caption="Une déclaration `use` ne s'applique que dans le scope où elle se trouve.">

```rust,noplayground,test_harness,does_not_compile,ignore
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-12/src/lib.rs}}
```

</Listing>

L'erreur du compilateur montre que le raccourci ne s'applique plus dans le module `customer` :

```console
{{#include ../listings/ch07-managing-growing-projects/listing-07-12/output.txt}}
```

Remarquez qu'il y a aussi un avertissement que le `use` n'est plus utilisé dans son scope ! Pour résoudre ce problème, déplacez le `use` dans le module `customer` également, ou référencez le raccourci dans le module parent avec `super::hosting` dans le module enfant `customer`.

### Créer des Chemins `use` Idiomatiques

Dans la Liste 7-11, vous vous êtes peut-être demandé pourquoi nous avons spécifié `use crate::front_of_house::hosting` puis appelé `hosting::add_to_waitlist` dans `eat_at_restaurant`, plutôt que de spécifier le chemin `use` jusqu’à la fonction `add_to_waitlist` pour obtenir le même résultat, comme dans la Liste 7-13.

<Listing number="7-13" file-name="src/lib.rs" caption="Ramener la fonction `add_to_waitlist` dans le scope avec `use`, ce qui est non-idiomatique">

```rust,noplayground,test_harness
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-13/src/lib.rs}}
```

</Listing>

Bien que les Liste 7-11 et 7-13 accomplissent la même tâche, la Liste 7-11 est la façon idiomatique de ramener une fonction dans le scope avec `use`. Ramener le module parent de la fonction dans le scope avec `use` signifie que nous devons spécifier le module parent lors de l'appel de la fonction. Spécifier le module parent lors de l'appel de la fonction clarifie que la fonction n'est pas définie localement tout en minimisant la répétition du chemin complet. Le code dans la Liste 7-13 est peu clair quant à l'endroit où `add_to_waitlist` est défini.

D'autre part, lorsque nous ramenons des structs, des enums et d'autres éléments avec `use`, il est idiomatique de spécifier le chemin complet. La Liste 7-14 montre la manière idiomatique de ramener la struct `HashMap` de la bibliothèque standard dans le scope d'un crate binaire.

<Listing number="7-14" file-name="src/main.rs" caption="Ramener `HashMap` dans le scope de manière idiomatique">

```rust
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-14/src/main.rs}}
```

</Listing>

Il n'y a pas de raison forte derrière cette idiomatique : c'est juste la convention qui a émergé, et les gens ont pris l'habitude de lire et d'écrire du code Rust de cette manière.

L'exception à cette idiomatique est si nous ramenons deux éléments ayant le même nom dans le scope avec des déclarations `use`, car Rust ne le permet pas. La Liste 7-15 montre comment ramener deux types `Result` dans le scope qui ont le même nom mais des modules parents différents, et comment y faire référence.

<Listing number="7-15" file-name="src/lib.rs" caption="Ramener deux types avec le même nom dans le même scope nécessite d'utiliser leurs modules parents.">

```rust,noplayground
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-15/src/lib.rs:here}}
```

</Listing>

Comme vous pouvez le voir, utiliser les modules parents distingue les deux types `Result`. Si nous spécifions `use std::fmt::Result` et `use std::io::Result`, nous aurions deux types `Result` dans le même scope, et Rust ne saurait pas lequel nous voulions dire lorsque nous utiliserions `Result`.

### Fournir de Nouveaux Noms avec le Mot Clé `as`

Il existe une autre solution au problème de ramener deux types du même nom dans le même scope avec `use` : après le chemin, nous pouvons spécifier `as` et un nouveau nom local, ou _alias_, pour le type. La Liste 7-16 montre une autre façon d'écrire le code de la Liste 7-15 en renommant l'un des deux types `Result` en utilisant `as`.

<Listing number="7-16" file-name="src/lib.rs" caption="Renommer un type lorsqu'il est ramené dans le scope avec le mot clé `as`">

```rust,noplayground
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-16/src/lib.rs:here}}
```

</Listing>

Dans la deuxième déclaration `use`, nous avons choisi le nouveau nom `IoResult` pour le type `std::io::Result`, qui ne rentrera pas en conflit avec le `Result` de `std::fmt` que nous avons également ramené dans le scope. Les Listes 7-15 et 7-16 sont considérées comme idiomatiques, donc le choix vous appartient !

### Ré-exporter des Noms avec `pub use`

Lorsque nous ramenons un nom dans le scope avec le mot clé `use`, le nom est privé au scope dans lequel nous l'avons importé. Pour permettre au code extérieur à ce scope de se référer à ce nom comme s'il avait été défini dans ce scope, nous pouvons combiner `pub` et `use`. Cette technique est appelée _ré-exportation_ car nous ramenons un élément dans le scope mais rendons également cet élément disponible pour d'autres à ramener dans leur scope.

La Liste 7-17 montre le code de la Liste 7-11 avec `use` dans le module racine changé en `pub use`.

<Listing number="7-17" file-name="src/lib.rs" caption="Rendre un nom disponible pour tout code à utiliser à partir d'un nouveau scope avec `pub use`">

```rust,noplayground,test_harness
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-17/src/lib.rs}}
```

</Listing>

Avant ce changement, le code externe aurait dû appeler la fonction `add_to_waitlist` en utilisant le chemin `restaurant::front_of_house::hosting::add_to_waitlist()`, ce qui aurait également nécessité que le module `front_of_house` soit marqué comme `pub`. Maintenant que ce `pub use` a ré-exporté le module `hosting` du module racine, le code externe peut utiliser le chemin `restaurant::hosting::add_to_waitlist()` à la place.

La ré-exportation est utile lorsque la structure interne de votre code est différente de la façon dont les programmeurs appelant votre code penseraient au domaine. Par exemple, dans cette métaphore de restaurant, les gens qui dirigent le restaurant pensent à "l'avant de la maison" et "l'arrière de la maison". Mais les clients visitant un restaurant ne penseront probablement pas aux parties du restaurant en ces termes. Avec `pub use`, nous pouvons écrire notre code avec une structure mais exposer une structure différente. Cela rend notre bibliothèque bien organisée pour les programmeurs travaillant sur la bibliothèque et pour les programmeurs appelant la bibliothèque. Nous examinerons un autre exemple de `pub use` et comment cela affecte la documentation de votre crate dans [“Exporter une API publique pratique”][ch14-pub-use]<!-- ignore --> au Chapitre 14.

### Utiliser des Paquets Externes

Dans le Chapitre 2, nous avons programmé un projet de jeu de devinettes qui utilisait un paquet externe appelé `rand` pour obtenir des nombres aléatoires. Pour utiliser `rand` dans notre projet, nous avons ajouté cette ligne à _Cargo.toml_ :

<!-- Lors de la mise à jour de la version de `rand` utilisée, mettez également à jour la version de `rand` utilisée dans ces fichiers pour qu'ils correspondent tous :
* ch02-00-guessing-game-tutorial.md
* ch14-03-cargo-workspaces.md
-->

<Listing file-name="Cargo.toml">

```toml
{{#include ../listings/ch02-guessing-game-tutorial/listing-02-02/Cargo.toml:9:}}
```

</Listing>

Ajouter `rand` comme dépendance dans _Cargo.toml_ dit à Cargo de télécharger le paquet `rand` et toutes les dépendances de [crates.io](https://crates.io/) et de rendre `rand` disponible pour notre projet.

Ensuite, pour ramener les définitions de `rand` dans le scope de notre paquet, nous avons ajouté une ligne `use` commençant par le nom du crate, `rand`, et énuméré les éléments que nous voulions ramener dans le scope. Rappelez-vous qu'à [“Générer un Nombre Aléatoire”][rand]<!-- ignore --> dans le Chapitre 2, nous avons ramené le trait `Rng` dans le scope et appelé la fonction `rand::thread_rng` :

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-03/src/main.rs:ch07-04}}
```

De nombreux membres de la communauté Rust ont rendu de nombreux paquets disponibles sur [crates.io](https://crates.io/), et tirer n'importe lequel d'eux dans votre paquet implique ces mêmes étapes : les lister dans le fichier _Cargo.toml_ de votre paquet et utiliser `use` pour ramener des éléments de leurs crates dans le scope.

Notez que la bibliothèque standard `std` est également un crate qui est externe à notre paquet. Étant donné que la bibliothèque standard est livrée avec le langage Rust, nous n'avons pas besoin de modifier _Cargo.toml_ pour inclure `std`. Mais nous devons nous y référer avec `use` pour ramener des éléments de là dans le scope de notre paquet. Par exemple, avec `HashMap`, nous utiliserions cette ligne :

```rust
use std::collections::HashMap;
```

Ceci est un chemin absolu commençant par `std`, le nom de la crate de la bibliothèque standard.

### Utiliser des Chemins Nests pour Nettoyer les Listes `use`

Si nous utilisons plusieurs éléments définis dans le même crate ou le même module, lister chaque élément sur sa propre ligne peut prendre beaucoup d'espace vertical dans nos fichiers. Par exemple, ces deux déclarations `use` que nous avions dans le jeu de devinettes dans la Liste 2-4 ramènent des éléments de `std` dans le scope :

<Listing file-name="src/main.rs">

```rust,ignore
{{#rustdoc_include ../listings/ch07-managing-growing-projects/no-listing-01-use-std-unnested/src/main.rs:here}}
```

</Listing>

Au lieu de cela, nous pouvons utiliser des chemins imbriqués pour ramener les mêmes éléments dans le scope en une seule ligne. Nous le faisons en spécifiant la partie commune du chemin, suivie de deux points, puis des accolades autour d'une liste des parties des chemins qui diffèrent, comme montré dans la Liste 7-18.

<Listing number="7-18" file-name="src/main.rs" caption="Spécifier un chemin imbriqué pour ramener plusieurs éléments ayant le même préfixe dans le scope">

```rust,ignore
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-18/src/main.rs:here}}
```

</Listing>

Dans des programmes plus grands, ramener de nombreux éléments dans le scope à partir du même crate ou module en utilisant des chemins imbriqués peut réduire le nombre d'instructions `use` séparées nécessaires de beaucoup !

Nous pouvons utiliser un chemin imbriqué à n'importe quel niveau d'un chemin, ce qui est utile lorsque nous combinons deux déclarations `use` qui partagent un sous-chemin. Par exemple, la Liste 7-19 montre deux déclarations `use` : l'une qui ramène `std::io` dans le scope et l'autre qui ramène `std::io::Write` dans le scope.

<Listing number="7-19" file-name="src/lib.rs" caption="Deux déclarations `use` où l'une est un sous-chemin de l'autre">

```rust,noplayground
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-19/src/lib.rs}}
```

</Listing>

La partie commune de ces deux chemins est `std::io`, et c’est le premier chemin complet. Pour fusionner ces deux chemins en une seule déclaration `use`, nous pouvons utiliser `self` dans le chemin imbriqué, comme montré dans la Liste 7-20.

<Listing number="7-20" file-name="src/lib.rs" caption="Combiner les chemins dans la Liste 7-19 en une seule déclaration `use`">

```rust,noplayground
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-20/src/lib.rs}}
```

</Listing>

Cette ligne ramène `std::io` et `std::io::Write` dans le scope.

### Importer des Éléments avec l'Opérateur Glob

Si nous voulons ramener _tous_ les éléments publics définis dans un chemin dans le scope, nous pouvons spécifier ce chemin suivi de l'opérateur glob `*` :

```rust
use std::collections::*;
```

Cette déclaration `use` ramène tous les éléments publics définis dans `std::collections` dans le scope actuel. Faites attention lorsque vous utilisez l'opérateur glob ! Le glob peut rendre plus difficile de savoir quels noms sont dans le scope et d'où provient un nom utilisé dans votre programme. De plus, si la dépendance modifie ses définitions, ce que vous avez importé change également, ce qui peut entraîner des erreurs de compilation lorsque vous mettez à jour la dépendance si celle-ci ajoute une définition portant le même nom qu'une définition de votre code dans le même scope, par exemple.

L'opérateur glob est souvent utilisé lors des tests pour ramener tout sous test dans le module `tests` ; nous en parlerons dans [“Comment Écrire des Tests”][writing-tests]<!-- ignore --> au Chapitre 11. L'opérateur glob est également parfois utilisé dans le cadre du modèle de prélude : voir [la documentation de la bibliothèque standard](../std/prelude/index.html#other-preludes)<!-- ignore --> pour plus d'informations sur ce modèle.