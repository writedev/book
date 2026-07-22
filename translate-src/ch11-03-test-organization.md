## Organisation des tests

Comme mentionné au début de ce chapitre, les tests sont une discipline complexe, et différentes personnes utilisent différentes terminologies et organisations. La communauté Rust pense aux tests en termes de deux catégories principales : les tests unitaires et les tests d'intégration. Les _tests unitaires_ sont petits et plus ciblés, testant un module en isolation à la fois, et peuvent tester des interfaces privées. Les _tests d'intégration_ sont entièrement externes à votre bibliothèque et utilisent votre code de la même manière que tout autre code externe, en utilisant uniquement l'interface publique et en exerçant potentiellement plusieurs modules par test.

Écrire ces deux types de tests est important pour s'assurer que les composants de votre bibliothèque fonctionnent comme vous l'attendez, séparément et ensemble.

### Tests Unitaires

Le but des tests unitaires est de tester chaque unité de code en isolation du reste du code afin de localiser rapidement où le code fonctionne et ne fonctionne pas comme prévu. Vous placerez les tests unitaires dans le répertoire _src_ dans chaque fichier avec le code qu'ils testent. La convention est de créer un module nommé `tests` dans chaque fichier pour contenir les fonctions de test et d'annoter le module avec `cfg(test)`.

#### Le module `tests` et `#[cfg(test)]`

L'annotation `#[cfg(test)]` sur le module `tests` indique à Rust de compiler et d'exécuter le code de test uniquement lorsque vous exécutez `cargo test`, et non lorsque vous exécutez `cargo build`. Cela permet de gagner du temps de compilation lorsque vous souhaitez uniquement construire la bibliothèque et économise de l'espace dans l'artefact compilé résultant car les tests ne sont pas inclus. Vous verrez que, comme les tests d'intégration vont dans un répertoire différent, ils n'ont pas besoin de l'annotation `#[cfg(test)]`. Cependant, comme les tests unitaires vont dans les mêmes fichiers que le code, vous utiliserez `#[cfg(test)]` pour spécifier qu'ils ne devraient pas être inclus dans le résultat compilé.

Rappelez-vous que lorsque nous avons généré le nouveau projet `adder` dans la première section de ce chapitre, Cargo a généré ce code pour nous :

<span class="filename">Nom de fichier : src/lib.rs</span>

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-01/src/lib.rs}}
```

Sur le module `tests` généré automatiquement, l'attribut `cfg` signifie _configuration_ et indique à Rust que l'élément suivant ne doit être inclus que si une certaine option de configuration est fournie. Dans ce cas, l'option de configuration est `test`, qui est fournie par Rust pour compiler et exécuter des tests. En utilisant l'attribut `cfg`, Cargo compile notre code de test uniquement si nous exécutons activement les tests avec `cargo test`. Cela inclut toutes les fonctions d'assistance qui pourraient se trouver dans ce module, en plus des fonctions annotées avec `#[test]`.

#### Tests des fonctions privées

Il y a un débat au sein de la communauté des tests sur la question de savoir si les fonctions privées doivent être testées directement, et d'autres langages rendent difficile, voire impossible, de tester des fonctions privées. Peu importe l'idéologie de test à laquelle vous adhérez, les règles de confidentialité de Rust vous permettent de tester des fonctions privées. Considérez le code dans la liste 11-12 avec la fonction privée `internal_adder`.

<Listing number="11-12" file-name="src/lib.rs" caption="Tester une fonction privée">

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-12/src/lib.rs}}
```

</Listing>

Notez que la fonction `internal_adder` n'est pas marquée comme `pub`. Les tests sont simplement du code Rust, et le module `tests` est juste un autre module. Comme nous l'avons discuté dans [“Chemins pour référencer un élément dans l'arbre des modules”][paths]<!-- ignore -->, les éléments des modules enfants peuvent utiliser les éléments de leurs modules ancêtres. Dans ce test, nous amenons tous les éléments appartenant au parent du module `tests` dans le scope avec `use super::*`, puis le test peut appeler `internal_adder`. Si vous ne pensez pas que les fonctions privées devraient être testées, rien dans Rust ne vous y obligera.

### Tests d'Intégration

Dans Rust, les tests d'intégration sont entièrement externes à votre bibliothèque. Ils utilisent votre bibliothèque de la même manière que n'importe quel autre code, ce qui signifie qu'ils ne peuvent appeler que les fonctions qui font partie de l'API publique de votre bibliothèque. Leur but est de tester si plusieurs parties de votre bibliothèque fonctionnent ensemble correctement. Les unités de code qui fonctionnent correctement individuellement peuvent rencontrer des problèmes lorsqu'elles sont intégrées, il est donc important d'avoir une couverture de test du code intégré. Pour créer des tests d'intégration, vous devez d'abord un répertoire _tests_.

#### Le répertoire _tests_

Nous créons un répertoire _tests_ au niveau supérieur de notre répertoire de projet, à côté de _src_. Cargo sait chercher des fichiers de tests d'intégration dans ce répertoire. Nous pouvons ensuite créer autant de fichiers de test que nous le souhaitons, et Cargo compilera chaque fichier en tant que crate individuelle.

Créons un test d'intégration. Avec le code de la liste 11-12 encore dans le fichier _src/lib.rs_, créez un répertoire _tests_ et créez un nouveau fichier nommé _tests/integration_test.rs_. Votre structure de répertoire devrait ressembler à ceci :

```text
adder
├── Cargo.lock
├── Cargo.toml
├── src
│   └── lib.rs
└── tests
    └── integration_test.rs
```

Entrez le code de la liste 11-13 dans le fichier _tests/integration_test.rs_.

<Listing number="11-13" file-name="tests/integration_test.rs" caption="Un test d'intégration d'une fonction dans la crate `adder`">

```rust,ignore
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-13/tests/integration_test.rs}}
```

</Listing>

Chaque fichier dans le répertoire _tests_ est une crate séparée, nous devons donc amener notre bibliothèque dans le scope de chaque crate de test. Pour cette raison, nous ajoutons `use adder::add_two;` en haut du code, ce que nous n'avions pas besoin de faire dans les tests unitaires.

Nous n'avons pas besoin d'annoter aucun code dans _tests/integration_test.rs_ avec `#[cfg(test)]`. Cargo traite le répertoire _tests_ de manière spéciale et compile les fichiers dans ce répertoire uniquement lorsque nous exécutons `cargo test`. Exécutez `cargo test` maintenant :

```console
{{#include ../listings/ch11-writing-automated-tests/listing-11-13/output.txt}}
```

Les trois sections de sortie incluent les tests unitaires, le test d'intégration et les tests de documentation. Notez que si un test dans une section échoue, les sections suivantes ne s'exécuteront pas. Par exemple, si un test unitaire échoue, il n'y aura pas de sortie pour les tests d'intégration et de documentation, car ces tests ne seront exécutés que si tous les tests unitaires passent.

La première section pour les tests unitaires est la même que ce que nous avons vu : une ligne pour chaque test unitaire (un nommé `internal` que nous avons ajouté dans la liste 11-12) et ensuite une ligne de résumé pour les tests unitaires.

La section des tests d'intégration commence par la ligne `Running tests/integration_test.rs`. Ensuite, il y a une ligne pour chaque fonction de test dans ce test d'intégration et une ligne de résumé pour les résultats du test d'intégration juste avant que la section `Doc-tests adder` ne commence.

Chaque fichier de test d'intégration a sa propre section, donc si nous ajoutons plus de fichiers dans le répertoire _tests_, il y aura plus de sections de tests d'intégration.

Nous pouvons toujours exécuter une fonction de test d'intégration particulière en spécifiant le nom de la fonction de test comme argument à `cargo test`. Pour exécuter tous les tests dans un fichier de test d'intégration particulier, utilisez l'argument `--test` de `cargo test` suivi du nom du fichier :

```console
{{#include ../listings/ch11-writing-automated-tests/output-only-05-single-integration/output.txt}}
```

Cette commande n'exécute que les tests dans le fichier _tests/integration_test.rs_.

#### Sous-modules dans les tests d'intégration

Au fur et à mesure que vous ajoutez plus de tests d'intégration, vous voudrez peut-être créer plus de fichiers dans le répertoire _tests_ pour mieux les organiser ; par exemple, vous pouvez regrouper les fonctions de test par la fonctionnalité qu'elles testent. Comme mentionné précédemment, chaque fichier dans le répertoire _tests_ est compilé comme sa propre crate séparée, ce qui est utile pour créer des scopes séparés afin d'imiter de plus près la façon dont les utilisateurs finaux utiliseront votre crate. Cependant, cela signifie que les fichiers dans le répertoire _tests_ ne partagent pas le même comportement que les fichiers dans _src_, comme vous l'avez appris dans le chapitre 7 concernant la manière de séparer le code en modules et en fichiers.

Le comportement différent des fichiers du répertoire _tests_ est le plus visible lorsque vous avez un ensemble de fonctions d'assistance à utiliser dans plusieurs fichiers de tests d'intégration, et que vous essayez de suivre les étapes de la section [“Séparer les modules en différents fichiers”][separating-modules-into-files]<!-- ignore --> du chapitre 7 pour les extraire dans un module commun. Par exemple, si nous créons _tests/common.rs_ et plaçons une fonction nommée `setup` à l'intérieur, nous pouvons ajouter du code à `setup` que nous souhaitons appeler depuis plusieurs fonctions de test dans plusieurs fichiers de test :

<span class="filename">Nom de fichier : tests/common.rs</span>

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-12-shared-test-code-problem/tests/common.rs}}
```

Lorsque nous exécutons à nouveau les tests, nous verrons une nouvelle section dans la sortie des tests pour le fichier _common.rs_, même si ce fichier ne contient aucune fonction de test et que nous n'avons pas appelé la fonction `setup` de nulle part :

```console
{{#include ../listings/ch11-writing-automated-tests/no-listing-12-shared-test-code-problem/output.txt}}
```

Faire apparaître `common` dans les résultats des tests avec `running 0 tests` affiché pour lui n'est pas ce que nous voulions. Nous voulions simplement partager du code avec les autres fichiers de tests d'intégration. Pour éviter que `common` n'apparaisse dans la sortie des tests, au lieu de créer _tests/common.rs_, nous créerons _tests/common/mod.rs_. Le répertoire du projet ressemble maintenant à ceci :

```text
├── Cargo.lock
├── Cargo.toml
├── src
│   └── lib.rs
└── tests
    ├── common
    │   └── mod.rs
    └── integration_test.rs
```

C'est l'ancienne convention de nommage que Rust comprend également, que nous avons mentionnée dans [“Chemins de fichiers alternatifs”][alt-paths]<!-- ignore --> dans le chapitre 7. Nommer le fichier de cette manière indique à Rust de ne pas traiter le module `common` comme un fichier de test d'intégration. Lorsque nous déplaçons le code de la fonction `setup` dans _tests/common/mod.rs_ et supprimons le fichier _tests/common.rs_, la section dans la sortie des tests n'apparaîtra plus. Les fichiers dans les sous-répertoires du répertoire _tests_ ne sont pas compilés en tant que crates séparées ni n'ont de sections dans la sortie des tests.

Après avoir créé _tests/common/mod.rs_, nous pouvons l'utiliser depuis n'importe quel fichier de test d'intégration comme un module. Voici un exemple d'appel de la fonction `setup` depuis le test `it_adds_two` dans _tests/integration_test.rs_ :

<span class="filename">Nom de fichier : tests/integration_test.rs</span>

```rust,ignore
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-13-fix-shared-test-code-problem/tests/integration_test.rs}}
```

Notez que la déclaration `mod common;` est la même que la déclaration de module que nous avons démontrée dans la liste 7-21. Ensuite, dans la fonction de test, nous pouvons appeler la fonction `common::setup()`.

#### Tests d'intégration pour les crates binaires

Si notre projet est une crate binaire qui ne contient qu'un fichier _src/main.rs_ et n'a pas de fichier _src/lib.rs_, nous ne pouvons pas créer des tests d'intégration dans le répertoire _tests_ et faire entrer les fonctions définies dans le fichier _src/main.rs_ dans le scope avec une déclaration `use`. Seules les crates de bibliothèque exposent des fonctions que d'autres crates peuvent utiliser ; les crates binaires sont faites pour être exécutées indépendamment.

C'est l'une des raisons pour lesquelles les projets Rust qui fournissent un binaire ont un fichier _src/main.rs_ simple qui appelle une logique qui se trouve dans le fichier _src/lib.rs_. En utilisant cette structure, les tests d'intégration _peuvent_ tester la crate de bibliothèque avec `use` pour rendre la fonctionnalité importante disponible. Si la fonctionnalité importante fonctionne, la petite quantité de code dans le fichier _src/main.rs_ fonctionnera également, et cette petite quantité de code n'a pas besoin d'être testée.

## Résumé

Les fonctionnalités de test de Rust fournissent un moyen de spécifier comment le code doit fonctionner pour s'assurer qu'il continue à fonctionner comme vous l'attendez, même lorsque vous apportez des modifications. Les tests unitaires exercent différentes parties d'une bibliothèque séparément et peuvent tester des détails d'implémentation privés. Les tests d'intégration vérifient que plusieurs parties de la bibliothèque fonctionnent ensemble correctement, et ils utilisent l'API publique de la bibliothèque pour tester le code de la même manière dont du code externe l'utiliserait. Même si le système de types de Rust et les règles de propriété aident à prévenir certains types de bugs, les tests sont toujours importants pour réduire les bugs logiques liés au comportement attendu de votre code.

Concentrons-nous sur les connaissances que vous avez apprises dans ce chapitre et dans les chapitres précédents pour travailler sur un projet !

[paths]: ch07-03-paths-for-referring-to-an-item-in-the-module-tree.html
[separating-modules-into-files]: ch07-05-separating-modules-into-different-files.html
[alt-paths]: ch07-05-separating-modules-into-different-files.html#alternate-file-paths