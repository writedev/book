<!-- Anciennes en-têtes. Ne pas supprimer ou les liens peuvent se briser. -->

<a id="defining-modules-to-control-scope-and-privacy"></a>

## Contrôler la portée et la confidentialité avec des modules

Dans cette section, nous allons parler des modules et d'autres parties du système de modules, à savoir les _chemins_, qui permettent de nommer les éléments ; le mot-clé `use` qui fait entrer un chemin dans la portée ; et le mot-clé `pub` pour rendre les éléments publics. Nous aborderons également le mot-clé `as`, les packages externes et l'opérateur glob.

### Fiche de triche sur les modules

Avant d'entrer dans les détails des modules et des chemins, nous fournissons ici une référence rapide sur le fonctionnement des modules, des chemins, du mot-clé `use` et du mot-clé `pub` dans le compilateur, et sur la façon dont la plupart des développeurs organisent leur code. Nous présenterons des exemples de chacune de ces règles tout au long de ce chapitre, mais c'est un excellent endroit pour se référer comme rappel du fonctionnement des modules.

- **Partir de la racine du crate** : Lors de la compilation d'un crate, le compilateur commence par rechercher dans le fichier racine du crate (généralement _src/lib.rs_ pour un crate de bibliothèque et _src/main.rs_ pour un crate binaire) le code à compiler.
- **Déclaration des modules** : Dans le fichier racine du crate, vous pouvez déclarer de nouveaux modules ; par exemple, vous déclarez un module « garden » avec `mod garden;`. Le compilateur recherchera le code du module à ces endroits :
  - En ligne, à l'intérieur d'accolades qui remplacent le point-virgule suivant `mod garden`
  - Dans le fichier _src/garden.rs_
  - Dans le fichier _src/garden/mod.rs_
- **Déclaration des sous-modules** : Dans tout fichier autre que le fichier racine du crate, vous pouvez déclarer des sous-modules. Par exemple, vous pourriez déclarer `mod vegetables;` dans _src/garden.rs_. Le compilateur recherchera le code de la sous-module dans le répertoire nommé d'après le module parent à ces endroits :
  - En ligne, directement après `mod vegetables`, à l'intérieur d'accolades au lieu du point-virgule
  - Dans le fichier _src/garden/vegetables.rs_
  - Dans le fichier _src/garden/vegetables/mod.rs_
- **Chemins vers le code dans les modules** : Une fois qu'un module fait partie de votre crate, vous pouvez faire référence au code de ce module depuis n'importe où dans ce même crate, tant que les règles de confidentialité le permettent, en utilisant le chemin vers le code. Par exemple, un type `Asperge` dans le module des vegetables du garden se trouverait à `crate::garden::vegetables::Asperge`.
- **Privé vs. public** : Le code à l'intérieur d'un module est privé de ses modules parents par défaut. Pour rendre un module public, déclarez-le avec `pub mod` au lieu de `mod`. Pour rendre les éléments d'un module public également publics, utilisez `pub` avant leurs déclarations.
- **Le mot-clé `use`** : À l'intérieur d'une portée, le mot-clé `use` crée des raccourcis vers des éléments pour réduire la répétition de longs chemins. Dans toute portée qui peut faire référence à `crate::garden::vegetables::Asperge`, vous pouvez créer un raccourci avec `use crate::garden::vegetables::Asperge;`, et à partir de là, vous n'avez besoin d'écrire que `Asperge` pour utiliser ce type dans la portée.

Ici, nous créons un crate binaire nommé `garden` qui illustre ces règles. Le répertoire du crate, également nommé _garden_, contient ces fichiers et répertoires :

```text
garden
├── Cargo.lock
├── Cargo.toml
└── src
    ├── garden
    │   └── vegetables.rs
    ├── garden.rs
    └── main.rs
```

Le fichier racine du crate dans ce cas est _src/main.rs_, et il contient :

<Listing file-name="src/main.rs">

```rust,noplayground,ignore
{{#rustdoc_include ../listings/ch07-managing-growing-projects/quick-reference-example/src/main.rs}}
```

</Listing>

La ligne `pub mod garden;` indique au compilateur d'inclure le code qu'il trouve dans _src/garden.rs_, qui est :

<Listing file-name="src/garden.rs">

```rust,noplayground,ignore
{{#rustdoc_include ../listings/ch07-managing-growing-projects/quick-reference-example/src/garden.rs}}
```

</Listing>

Ici, `pub mod vegetables;` signifie que le code dans _src/garden/vegetables.rs_ est inclus aussi. Ce code est :

```rust,noplayground,ignore
{{#rustdoc_include ../listings/ch07-managing-growing-projects/quick-reference-example/src/garden/vegetables.rs}}
```

Maintenant, entrons dans les détails de ces règles et démontrons-les en action !

### Regrouper le code connexe dans des modules

_Les modules_ nous permettent d'organiser le code à l'intérieur d'un crate pour une meilleure lisibilité et réutilisation. Les modules nous permettent également de contrôler la _confidentialité_ des éléments car le code à l'intérieur d'un module est privé par défaut. Les éléments privés sont des détails d'implémentation internes non disponibles pour un usage extérieur. Nous pouvons choisir de rendre les modules et les éléments qui y sont inclus publics, ce qui les expose pour permettre à un code externe de les utiliser et d'en dépendre.

Par exemple, écrivons un crate de bibliothèque qui fournit la fonctionnalité d'un restaurant. Nous définirons les signatures des fonctions mais laisserons leurs corps vides pour nous concentrer sur l'organisation du code plutôt que sur l'implémentation d'un restaurant.

Dans l'industrie de la restauration, certaines parties d'un restaurant sont appelées avant de salle et d'autres arrière de salle. _Avant de salle_ est l'endroit où se trouvent les clients ; cela englobe les lieux où les hôtes placent les clients, les serveurs prennent des commandes et des paiements, et les barmans préparent des boissons. _Arrière de salle_ est l'endroit où les chefs et les cuisiniers travaillent dans la cuisine, les plongeurs nettoient, et les managers effectuent des tâches administratives.

Pour structurer notre crate de cette manière, nous pouvons organiser ses fonctions en modules imbriqués. Créez une nouvelle bibliothèque nommée `restaurant` en exécutant `cargo new restaurant --lib`. Ensuite, entrez le code dans la Liste 7-1 dans _src/lib.rs_ pour définir quelques modules et signatures de fonction ; ce code est la section avant de salle.

<Listing number="7-1" file-name="src/lib.rs" caption="Un module `avant_de_salle` contenant d'autres modules qui contiennent ensuite des fonctions">

```rust,noplayground
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-01/src/lib.rs}}
```

</Listing>

Nous définissons un module avec le mot-clé `mod` suivi du nom du module (dans ce cas, `avant_de_salle`). Le corps du module va ensuite à l'intérieur d'accolades. À l'intérieur des modules, nous pouvons placer d'autres modules, comme dans ce cas avec les modules `accueil` et `service`. Les modules peuvent également contenir des définitions d'autres éléments, tels que des structures, des énumérations, des constantes, des traits, et comme dans la Liste 7-1, des fonctions.

En utilisant des modules, nous pouvons regrouper des définitions connexes et nommer leur raison de relation. Les programmeurs utilisant ce code peuvent naviguer dans le code en se basant sur les groupes plutôt qu'en ayant à lire toutes les définitions, facilitant ainsi la recherche des définitions pertinentes pour eux. Les programmeurs ajoutant de nouvelles fonctionnalités à ce code sauraient où placer le code pour maintenir l'organisation du programme.

Auparavant, nous avons mentionné que _src/main.rs_ et _src/lib.rs_ sont appelés _racines du crate_. La raison de leur nom est que le contenu de l'un ou l'autre de ces deux fichiers forme un module nommé `crate` à la racine de la structure de modules du crate, appelée l'_arbre des modules_.

La Liste 7-2 montre l'arbre des modules pour la structure de la Liste 7-1.

<Listing number="7-2" caption="L'arbre des modules pour le code de la Liste 7-1">

```text
crate
 └── avant_de_salle
     ├── accueil
     │   ├── ajouter_à_la_liste_d'attente
     │   └── placer_à_la_table
     └── service
         ├── prendre_commande
         ├── servir_commande
         └── prendre_paiement
```

</Listing>

Cet arbre montre comment certains modules s'imbriquent dans d'autres modules ; par exemple, `accueil` s'imbrique dans `avant_de_salle`. L'arbre montre également que certains modules sont des _cousins_, ce qui signifie qu'ils sont définis dans le même module ; `accueil` et `service` sont des cousins définis dans `avant_de_salle`. Si le module A est contenu dans le module B, nous disons que le module A est le _child_ du module B et que le module B est le _parent_ du module A. Remarquez que l'ensemble de l'arbre des modules est ancré sous le module implicite nommé `crate`.

L'arbre des modules pourrait vous rappeler l'arbre des répertoires de votre système d'exploitation ; c'est une comparaison très pertinente ! Tout comme les répertoires dans un système de fichiers, vous utilisez des modules pour organiser votre code. Et tout comme les fichiers dans un répertoire, nous avons besoin d'un moyen de trouver nos modules.
