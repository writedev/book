<!-- Anciens titres. Ne pas supprimer, sinon les liens risquent de ne plus fonctionner. -->

<a id="defining-modules-to-control-scope-and-privacy"></a>

## Contrôler la portée et la confidentialité avec les modules

Dans cette section, nous parlerons des modules et d’autres éléments du système de modules, notamment des _chemins_, qui permettent de nommer des éléments ; du mot-clé `use`, qui place un chemin dans la portée ; et du mot-clé `pub`, qui rend des éléments publics. Nous aborderons également le mot-clé `as`, les paquets externes et l’opérateur glob.

### Aide-mémoire sur les modules

Avant d’entrer dans les détails des modules et des chemins, voici un bref récapitulatif du fonctionnement des modules, des chemins, du mot-clé `use` et du mot-clé `pub` dans le compilateur, ainsi que de la façon dont la plupart des développeurs organisent leur code. Nous présenterons des exemples de chacune de ces règles tout au long de ce chapitre, mais vous pourrez revenir ici pour vous rappeler le fonctionnement des modules.

- **Partir de la racine du crate** : Lors de la compilation d’un crate, le compilateur commence par chercher le code à compiler dans le fichier racine du crate (généralement _src/lib.rs_ pour un crate de bibliothèque et _src/main.rs_ pour un crate binaire).
- **Déclarer des modules** : Dans le fichier racine du crate, vous pouvez déclarer de nouveaux modules ; par exemple, vous pouvez déclarer un module « garden » avec `mod garden;`. Le compilateur cherchera le code du module aux endroits suivants :
  - Directement dans le fichier, entre accolades qui remplacent le point-virgule suivant `mod garden`
  - Dans le fichier _src/garden.rs_
  - Dans le fichier _src/garden/mod.rs_
- **Déclarer des sous-modules** : Dans tout fichier autre que la racine du crate, vous pouvez déclarer des sous-modules. Par exemple, vous pouvez déclarer `mod vegetables;` dans _src/garden.rs_. Le compilateur cherchera le code du sous-module dans le répertoire portant le nom du module parent, aux endroits suivants :
  - Directement dans le fichier, entre accolades placées après `mod vegetables` à la place du point-virgule
  - Dans le fichier _src/garden/vegetables.rs_
  - Dans le fichier _src/garden/vegetables/mod.rs_
- **Chemins vers le code des modules** : Une fois qu’un module fait partie de votre crate, vous pouvez faire référence au code de ce module depuis n’importe quel autre endroit du même crate, tant que les règles de confidentialité le permettent, en utilisant le chemin vers ce code. Par exemple, un type `Asparagus` dans le module garden vegetables se trouverait à l’adresse `crate::garden::vegetables::Asparagus`.
- **Privé ou public** : Par défaut, le code d’un module est privé par rapport à ses modules parents. Pour rendre un module public, déclarez-le avec `pub mod` au lieu de `mod`. Pour rendre également publics les éléments d’un module public, faites précéder leurs déclarations de `pub`.
- **Le mot-clé `use`** : Dans une portée, le mot-clé `use` crée des raccourcis vers des éléments afin d’éviter de répéter de longs chemins. Dans toute portée où il est possible de faire référence à `crate::garden::vegetables::Asparagus`, vous pouvez créer un raccourci avec `use crate::garden::vegetables::Asparagus;`, puis il vous suffit d’écrire `Asparagus` pour utiliser ce type dans cette portée.

Nous créons ici un crate binaire nommé `backyard` qui illustre ces règles. Le répertoire du crate, lui aussi nommé _backyard_, contient les fichiers et répertoires suivants :

```text
backyard
├── Cargo.lock
├── Cargo.toml
└── src
    ├── garden
    │   └── vegetables.rs
    ├── garden.rs
    └── main.rs
```

Dans cet exemple, le fichier racine du crate est _src/main.rs_, et il contient :

<Listing file-name="src/main.rs">

```rust,noplayground,ignore
{{#rustdoc_include ../listings/ch07-managing-growing-projects/quick-reference-example/src/main.rs}}
```

</Listing>

La ligne `pub mod garden;` indique au compilateur d’inclure le code qu’il trouve dans _src/garden.rs_, qui est le suivant :

<Listing file-name="src/garden.rs">

```rust,noplayground,ignore
{{#rustdoc_include ../listings/ch07-managing-growing-projects/quick-reference-example/src/garden.rs}}
```

</Listing>

Ici, `pub mod vegetables;` signifie que le code de _src/garden/vegetables.rs_ est lui aussi inclus. Ce code est le suivant :

```rust,noplayground,ignore
{{#rustdoc_include ../listings/ch07-managing-growing-projects/quick-reference-example/src/garden/vegetables.rs}}
```

Passons maintenant aux détails de ces règles et voyons-les en action !

### Regrouper du code apparenté dans des modules

Les _modules_ nous permettent d’organiser le code au sein d’un crate pour en faciliter la lecture et la réutilisation. Les modules nous permettent également de contrôler la _confidentialité_ des éléments, car le code d’un module est privé par défaut. Les éléments privés sont des détails d’implémentation internes qui ne sont pas accessibles de l’extérieur. Nous pouvons choisir de rendre publics les modules et les éléments qu’ils contiennent, afin que du code externe puisse les utiliser et en dépendre.

À titre d’exemple, écrivons un crate de bibliothèque qui fournit les fonctionnalités d’un restaurant. Nous définirons les signatures des fonctions, mais laisserons leurs corps vides afin de nous concentrer sur l’organisation du code plutôt que sur la mise en œuvre d’un restaurant.

Dans le secteur de la restauration, certaines parties d’un restaurant sont désignées comme étant en salle, et d’autres en cuisine. La _salle_ est l’endroit où se trouvent les clients ; elle comprend les espaces où les hôtes installent les clients, où les serveurs prennent les commandes et les paiements, et où les barmans préparent les boissons. La _cuisine_ est l’endroit où les chefs et les cuisiniers travaillent, où les plongeurs font la vaisselle et où les gestionnaires s’occupent des tâches administratives.

Pour structurer notre crate de cette façon, nous pouvons organiser ses fonctions en modules imbriqués. Créez une nouvelle bibliothèque nommée `restaurant` en exécutant `cargo new restaurant --lib`. Ensuite, saisissez le code de la liste 7-1 dans _src/lib.rs_ pour définir des modules et des signatures de fonctions ; ce code correspond à la partie salle.

<Listing number="7-1" file-name="src/lib.rs" caption="Un module `front_of_house` contenant d’autres modules, qui contiennent à leur tour des fonctions">

```rust,noplayground
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-01/src/lib.rs}}
```

</Listing>

Nous définissons un module à l’aide du mot-clé `mod`, suivi du nom du module (dans cet exemple, `front_of_house`). Le corps du module est ensuite placé entre accolades. Dans les modules, nous pouvons placer d’autres modules, comme ici avec les modules `hosting` et `serving`. Les modules peuvent également contenir des définitions d’autres éléments, tels que des structures, des énumérations, des constantes, des traits et, comme dans la liste 7-1, des fonctions.

Les modules nous permettent de regrouper des définitions apparentées et d’indiquer en quoi elles sont liées. Les programmeurs qui utilisent ce code peuvent le parcourir en fonction de ces groupes, plutôt que d’avoir à lire toutes les définitions, ce qui leur permet de trouver plus facilement celles qui les concernent. Les programmeurs qui ajoutent de nouvelles fonctionnalités à ce code sauront où les placer pour que le programme reste bien organisé.

Nous avons indiqué précédemment que _src/main.rs_ et _src/lib.rs_ sont appelés les _racines du crate_. Ils portent ce nom parce que le contenu de chacun de ces fichiers forme un module nommé `crate` à la racine de la structure des modules du crate, appelée _arborescence des modules_.

La liste 7-2 montre l’arborescence des modules correspondant à la structure de la liste 7-1.

<Listing number="7-2" caption="L’arborescence des modules pour le code de la liste 7-1">

```text
crate
 └── front_of_house
     ├── hosting
     │   ├── add_to_waitlist
     │   └── seat_at_table
     └── serving
         ├── take_order
         ├── serve_order
         └── take_payment
```

</Listing>

Cette arborescence montre que certains modules sont imbriqués dans d’autres ; par exemple, `hosting` est imbriqué dans `front_of_house`. Elle montre également que certains modules sont _frères_, c’est-à-dire qu’ils sont définis dans le même module ; `hosting` et `serving` sont des modules frères définis dans `front_of_house`. Si le module A est contenu dans le module B, nous disons que le module A est l’_enfant_ du module B et que le module B est le _parent_ du module A. Notez que toute l’arborescence des modules est enracinée sous le module implicite nommé `crate`.

L’arborescence des modules peut vous rappeler celle des répertoires du système de fichiers de votre ordinateur ; la comparaison est tout à fait appropriée ! Tout comme les répertoires d’un système de fichiers, les modules vous permettent d’organiser votre code. Et tout comme pour les fichiers d’un répertoire, nous avons besoin d’un moyen de trouver nos modules.