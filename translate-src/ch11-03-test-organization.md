## Organisation des tests

Comme nous l’avons mentionné au début du chapitre, les tests sont une discipline complexe, et différentes personnes utilisent une terminologie et une organisation différentes. La communauté Rust distingue deux grandes catégories de tests : les tests unitaires et les tests d’intégration. Les _tests unitaires_ sont petits et plus ciblés : ils testent un module à la fois, de manière isolée, et peuvent tester des interfaces privées. Les _tests d’intégration_ sont entièrement externes à votre bibliothèque et utilisent votre code comme le ferait tout autre code externe, en n’utilisant que l’interface publique et en pouvant faire intervenir plusieurs modules par test.

Il est important d’écrire ces deux types de tests pour s’assurer que les différentes parties de votre bibliothèque fonctionnent comme prévu, séparément et ensemble.

### Tests unitaires

Les tests unitaires ont pour but de tester chaque unité de code indépendamment du reste afin de déterminer rapidement où le code fonctionne ou ne fonctionne pas comme prévu. Vous placerez les tests unitaires dans le répertoire _src_, dans chaque fichier contenant le code qu’ils testent. La convention consiste à créer un module nommé `tests` dans chaque fichier pour contenir les fonctions de test, et à annoter ce module avec `cfg(test)`.

#### Le module `tests` et `#[cfg(test)]`

L’annotation `#[cfg(test)]` sur le module `tests` indique à Rust de compiler et d’exécuter le code de test uniquement lorsque vous lancez `cargo test`, et non lorsque vous lancez `cargo build`. Cela permet de réduire le temps de compilation lorsque vous souhaitez seulement compiler la bibliothèque, ainsi que l’espace occupé par l’artefact compilé, car les tests n’y sont pas inclus. Vous verrez que les tests d’intégration se trouvent dans un répertoire différent et n’ont donc pas besoin de l’annotation `#[cfg(test)]`. Cependant, comme les tests unitaires se trouvent dans les mêmes fichiers que le code, vous utiliserez `#[cfg(test)]` pour indiquer qu’ils ne doivent pas être inclus dans le résultat compilé.

Rappelez-vous que lorsque nous avons généré le nouveau projet `adder` dans la première section de ce chapitre, Cargo a généré le code suivant :

<span class="filename">Nom du fichier : src/lib.rs</span>

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-01/src/lib.rs}}
```

Dans le module `tests` généré automatiquement, l’attribut `cfg` signifie _configuration_ et indique à Rust que l’élément suivant ne doit être inclus que si une certaine option de configuration est définie. Dans ce cas, l’option de configuration est `test`, fournie par Rust pour compiler et exécuter les tests. Grâce à l’attribut `cfg`, Cargo ne compile notre code de test que si nous lançons explicitement les tests avec `cargo test`. Cela inclut toutes les fonctions auxiliaires qui pourraient se trouver dans ce module, en plus des fonctions annotées avec `#[test]`.

<!-- Old headings. Do not remove or links may break. -->

<a id="testing-private-functions"></a>

#### Tests des fonctions privées

La communauté des tests débat de la question de savoir s’il faut tester directement les fonctions privées, et d’autres langages rendent difficile, voire impossible, le test des fonctions privées. Quelle que soit l’approche des tests que vous adoptez, les règles de confidentialité de Rust vous permettent de tester les fonctions privées. Considérez le code de la liste 11-12, qui contient la fonction privée `internal_adder`.

<Listing number="11-12" file-name="src/lib.rs" caption="Tester une fonction privée">

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-12/src/lib.rs}}
```

</Listing>

Notez que la fonction `internal_adder` n’est pas marquée comme `pub`. Les tests ne sont que du code Rust, et le module `tests` n’est qu’un autre module. Comme nous l’avons vu dans [« Chemins pour référencer un élément dans l’arborescence des modules »][paths]<!-- ignore -->, les éléments des modules enfants peuvent utiliser les éléments de leurs modules ancêtres. Dans ce test, nous faisons entrer dans la portée tous les éléments appartenant au parent du module `tests` avec `use super::*`, puis le test peut appeler `internal_adder`. Si vous estimez que les fonctions privées ne devraient pas être testées, rien dans Rust ne vous y contraindra.

### Tests d’intégration

En Rust, les tests d’intégration sont entièrement externes à votre bibliothèque. Ils utilisent votre bibliothèque comme le ferait n’importe quel autre code, ce qui signifie qu’ils ne peuvent appeler que les fonctions faisant partie de l’API publique de votre bibliothèque. Leur but est de vérifier que plusieurs parties de votre bibliothèque fonctionnent correctement ensemble. Des unités de code qui fonctionnent correctement séparément peuvent poser problème une fois intégrées ; il est donc également important de couvrir le code intégré par des tests. Pour créer des tests d’intégration, vous devez d’abord créer un répertoire _tests_.

#### Le répertoire _tests_

Nous créons un répertoire _tests_ à la racine du répertoire de notre projet, à côté de _src_. Cargo sait qu’il doit rechercher les fichiers de test d’intégration dans ce répertoire. Nous pouvons ensuite créer autant de fichiers de test que nous le souhaitons, et Cargo compilera chacun d’eux comme une crate distincte.

Créons un test d’intégration. En laissant le code de la liste 11-12 dans le fichier _src/lib.rs_, créez un répertoire _tests_, puis un fichier nommé _tests/integration_test.rs_. Votre structure de répertoires devrait ressembler à ceci :

```text
adder
├── Cargo.lock
├── Cargo.toml
├── src
│   └── lib.rs
└── tests
    └── integration_test.rs
```

Saisissez le code de la liste 11-13 dans le fichier _tests/integration_test.rs_.

<Listing number="11-13" file-name="tests/integration_test.rs" caption="Test d’intégration d’une fonction de la crate `adder`">

```rust,ignore
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-13/tests/integration_test.rs}}
```

</Listing>

Chaque fichier du répertoire _tests_ est une crate distincte ; nous devons donc faire entrer notre bibliothèque dans la portée de chaque crate de test. Pour cette raison, nous ajoutons `use adder::add_two;` en haut du code, ce qui n’était pas nécessaire dans les tests unitaires.

Nous n’avons pas besoin d’annoter du code dans _tests/integration_test.rs_ avec `#[cfg(test)]`. Cargo traite le répertoire _tests_ de manière particulière et ne compile les fichiers qui s’y trouvent que lorsque nous lançons `cargo test`. Lancez maintenant `cargo test` :

```console
{{#include ../listings/ch11-writing-automated-tests/listing-11-13/output.txt}}
```

Les trois sections de la sortie comprennent les tests unitaires, le test d’intégration et les tests de documentation. Notez que si un test échoue dans une section, les sections suivantes ne sont pas exécutées. Par exemple, si un test unitaire échoue, aucune sortie ne sera affichée pour les tests d’intégration et de documentation, car ces tests ne seront exécutés que si tous les tests unitaires réussissent.

La première section, consacrée aux tests unitaires, est identique à ce que nous avons vu jusqu’à présent : une ligne pour chaque test unitaire (dont un test nommé `internal`, que nous avons ajouté dans la liste 11-12), puis une ligne récapitulative pour les tests unitaires.

La section des tests d’intégration commence par la ligne `Running
tests/integration_test.rs`. Vient ensuite une ligne pour chaque fonction de test de ce test d’intégration, puis une ligne récapitulative des résultats du test d’intégration, juste avant le début de la section `Doc-tests adder`.

Chaque fichier de test d’intégration a sa propre section. Si nous ajoutons d’autres fichiers dans le répertoire _tests_, d’autres sections de tests d’intégration apparaîtront.

Nous pouvons toujours exécuter une fonction de test d’intégration spécifique en indiquant son nom comme argument de `cargo test`. Pour exécuter tous les tests d’un fichier de test d’intégration donné, utilisez l’argument `--test` de `cargo test`, suivi du nom du fichier :

```console
{{#include ../listings/ch11-writing-automated-tests/output-only-05-single-integration/output.txt}}
```

Cette commande n’exécute que les tests du fichier _tests/integration_test.rs_.

#### Sous-modules dans les tests d’intégration

À mesure que vous ajoutez des tests d’intégration, vous souhaiterez peut-être créer d’autres fichiers dans le répertoire _tests_ pour mieux les organiser ; par exemple, vous pouvez regrouper les fonctions de test selon les fonctionnalités qu’elles testent. Comme indiqué précédemment, chaque fichier du répertoire _tests_ est compilé comme une crate distincte, ce qui est utile pour créer des portées séparées et reproduire plus fidèlement la manière dont les utilisateurs finaux utiliseront votre crate. Cependant, cela signifie que les fichiers du répertoire _tests_ ne se comportent pas comme ceux de _src_, comme vous l’avez appris au chapitre 7 en découvrant comment séparer le code en modules et en fichiers.

La différence de comportement des fichiers du répertoire _tests_ est particulièrement visible lorsque vous disposez d’un ensemble de fonctions auxiliaires à utiliser dans plusieurs fichiers de test d’intégration et que vous essayez de suivre les étapes de la section [« Séparer les modules dans différents fichiers »][separating-modules-into-files]<!-- ignore --> du chapitre 7 pour les extraire dans un module commun. Par exemple, si nous créons _tests/common.rs_ et y plaçons une fonction nommée `setup`, nous pouvons ajouter du code à `setup` que nous souhaitons appeler depuis plusieurs fonctions de test réparties dans plusieurs fichiers de test :

<span class="filename">Nom du fichier : tests/common.rs</span>

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-12-shared-test-code-problem/tests/common.rs}}
```

Lorsque nous relançons les tests, nous voyons une nouvelle section dans la sortie des tests pour le fichier _common.rs_, même si ce fichier ne contient aucune fonction de test et que nous n’avons appelé la fonction `setup` nulle part :

```console
{{#include ../listings/ch11-writing-automated-tests/no-listing-12-shared-test-code-problem/output.txt}}
```

La présence de `common` dans les résultats des tests, avec l’indication `running 0 tests`, n’est pas ce que nous souhaitions. Nous voulions simplement partager du code avec les autres fichiers de test d’intégration. Pour éviter que `common` apparaisse dans la sortie des tests, nous allons créer _tests/common/mod.rs_ au lieu de _tests/common.rs_. Le répertoire du projet ressemble maintenant à ceci :

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

Il s’agit de l’ancienne convention de nommage que Rust comprend également, et que nous avons mentionnée dans la section [« Chemins de fichiers alternatifs »][alt-paths]<!-- ignore --> du chapitre 7. Nommer le fichier de cette manière indique à Rust qu’il ne doit pas traiter le module `common` comme un fichier de test d’intégration. Lorsque nous déplaçons le code de la fonction `setup` dans _tests/common/mod.rs_ et supprimons le fichier _tests/common.rs_, la section correspondante n’apparaît plus dans la sortie des tests. Les fichiers des sous-répertoires du répertoire _tests_ ne sont pas compilés comme des crates distinctes et n’ont pas de section dans la sortie des tests.

Après avoir créé _tests/common/mod.rs_, nous pouvons l’utiliser comme module depuis n’importe quel fichier de test d’intégration. Voici un exemple d’appel à la fonction `setup` depuis le test `it_adds_two` dans _tests/integration_test.rs_ :

<span class="filename">Nom du fichier : tests/integration_test.rs</span>

```rust,ignore
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-13-fix-shared-test-code-problem/tests/integration_test.rs}}
```

Notez que la déclaration `mod common;` est identique à celle que nous avons présentée dans la liste 7-21. Ensuite, dans la fonction de test, nous pouvons appeler la fonction `common::setup()`.

#### Tests d’intégration pour les crates binaires

Si notre projet est une crate binaire qui ne contient qu’un fichier _src/main.rs_ et ne possède pas de fichier _src/lib.rs_, nous ne pouvons pas créer de tests d’intégration dans le répertoire _tests_ et faire entrer dans la portée, à l’aide d’une instruction `use`, les fonctions définies dans le fichier _src/main.rs_. Seules les crates de bibliothèque exposent des fonctions utilisables par d’autres crates ; les crates binaires sont destinées à être exécutées de manière autonome.

C’est l’une des raisons pour lesquelles les projets Rust qui fournissent un exécutable ont un fichier _src/main.rs_ simple, qui appelle la logique contenue dans le fichier _src/lib.rs_. Avec cette structure, les tests d’intégration _peuvent_ tester la crate de bibliothèque en utilisant `use` pour rendre accessibles les fonctionnalités importantes. Si les fonctionnalités importantes fonctionnent, le petit volume de code du fichier _src/main.rs_ fonctionnera également, et il n’est pas nécessaire de tester ce code.

## Résumé

Les fonctionnalités de test de Rust permettent de spécifier le comportement attendu du code afin de s’assurer qu’il continue à fonctionner comme prévu, même lorsque vous le modifiez. Les tests unitaires exercent séparément différentes parties d’une bibliothèque et peuvent tester des détails d’implémentation privés. Les tests d’intégration vérifient que plusieurs parties de la bibliothèque fonctionnent correctement ensemble et utilisent l’API publique de la bibliothèque pour tester le code de la même manière que le ferait du code externe. Même si le système de types et les règles de propriété de Rust contribuent à prévenir certains types de bogues, les tests restent importants pour réduire les bogues logiques liés au comportement attendu de votre code.

Mettons à profit les connaissances acquises dans ce chapitre et les chapitres précédents pour travailler sur un projet !

[paths]: ch07-03-paths-for-referring-to-an-item-in-the-module-tree.html
[separating-modules-into-files]: ch07-05-separating-modules-into-different-files.html
[alt-paths]: ch07-05-separating-modules-into-different-files.html#alternate-file-paths