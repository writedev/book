## Espaces de travail Cargo

Au chapitre 12, nous avons créé un paquet qui comprenait une caisse binaire et une caisse bibliothèque. À mesure que votre projet se développe, vous pourriez constater que la caisse bibliothèque continue de grossir et vouloir diviser davantage votre paquet en plusieurs caisses bibliothèque. Cargo propose une fonctionnalité appelée _espaces de travail_ qui peut aider à gérer plusieurs paquets apparentés développés en parallèle.

### Créer un espace de travail

Un _espace de travail_ est un ensemble de paquets qui partagent le même fichier _Cargo.lock_ et le même répertoire de sortie. Créons un projet à l’aide d’un espace de travail — nous utiliserons du code trivial pour pouvoir nous concentrer sur la structure de l’espace de travail. Il existe plusieurs façons de structurer un espace de travail ; nous allons donc simplement présenter une méthode courante. Notre espace de travail contiendra un binaire et deux bibliothèques. Le binaire, qui fournira la fonctionnalité principale, dépendra des deux bibliothèques. L’une fournira une fonction `add_one` et l’autre, une fonction `add_two`. Ces trois caisses feront partie du même espace de travail. Commençons par créer un nouveau répertoire pour l’espace de travail :

```console
$ mkdir add
$ cd add
```

Ensuite, dans le répertoire _add_, nous créons le fichier _Cargo.toml_ qui configurera tout l’espace de travail. Ce fichier ne comportera pas de section `[package]`. Il commencera plutôt par une section `[workspace]` qui nous permettra d’ajouter des membres à l’espace de travail. Nous veillons également à utiliser la version la plus récente et la plus performante de l’algorithme de résolution de Cargo dans notre espace de travail, en définissant la valeur de `resolver` sur `"3"` :

<span class="filename">Nom du fichier : Cargo.toml</span>

```toml
{{#include ../listings/ch14-more-about-cargo/no-listing-01-workspace/add/Cargo.toml}}
```

Ensuite, nous allons créer la caisse binaire `adder` en exécutant `cargo new` dans le répertoire _add_ :

<!-- manual-regeneration
cd listings/ch14-more-about-cargo/output-only-01-adder-crate/add
remove `members = ["adder"]` from Cargo.toml
rm -rf adder
cargo new adder
copy output below
-->

```console
$ cargo new adder
     Created binary (application) `adder` package
      Adding `adder` as member of workspace at `file:///projects/add`
```

L’exécution de `cargo new` dans un espace de travail ajoute également automatiquement le paquet créé à la clé `members` de la définition `[workspace]` dans le fichier _Cargo.toml_ de l’espace de travail, comme ceci :

```toml
{{#include ../listings/ch14-more-about-cargo/output-only-01-adder-crate/add/Cargo.toml}}
```

À ce stade, nous pouvons compiler l’espace de travail en exécutant `cargo build`. Les fichiers de votre répertoire _add_ devraient ressembler à ceci :

```text
├── Cargo.lock
├── Cargo.toml
├── adder
│   ├── Cargo.toml
│   └── src
│       └── main.rs
└── target
```

L’espace de travail possède un seul répertoire _target_ à son niveau supérieur, dans lequel seront placés les artefacts compilés ; le paquet `adder` n’a pas son propre répertoire _target_. Même si nous exécutons `cargo build` depuis le répertoire _adder_, les artefacts compilés se retrouveront dans _add/target_ plutôt que dans _add/adder/target_. Cargo organise ainsi le répertoire _target_ d’un espace de travail, car les caisses d’un espace de travail sont censées dépendre les unes des autres. Si chaque caisse avait son propre répertoire _target_, chacune devrait recompiler toutes les autres caisses de l’espace de travail pour placer les artefacts dans son propre répertoire _target_. En partageant un seul répertoire _target_, les caisses peuvent éviter les compilations inutiles.

### Créer le deuxième paquet de l’espace de travail

Ensuite, créons un autre paquet membre de l’espace de travail et appelons-le `add_one`. Générons une nouvelle caisse bibliothèque nommée `add_one` :

<!-- manual-regeneration
cd listings/ch14-more-about-cargo/output-only-02-add-one/add
remove `"add_one"` from `members` list in Cargo.toml
rm -rf add_one
cargo new add_one --lib
copy output below
-->

```console
$ cargo new add_one --lib
     Created library `add_one` package
      Adding `add_one` as member of workspace at `file:///projects/add`
```

Le fichier _Cargo.toml_ de niveau supérieur inclura maintenant le chemin _add_one_ dans la liste `members` :

<span class="filename">Nom du fichier : Cargo.toml</span>

```toml
{{#include ../listings/ch14-more-about-cargo/no-listing-02-workspace-with-two-crates/add/Cargo.toml}}
```

Votre répertoire _add_ devrait maintenant contenir les répertoires et fichiers suivants :

```text
├── Cargo.lock
├── Cargo.toml
├── add_one
│   ├── Cargo.toml
│   └── src
│       └── lib.rs
├── adder
│   ├── Cargo.toml
│   └── src
│       └── main.rs
└── target
```

Dans le fichier _add_one/src/lib.rs_, ajoutons une fonction `add_one` :

<span class="filename">Nom du fichier : add_one/src/lib.rs</span>

```rust,noplayground
{{#rustdoc_include ../listings/ch14-more-about-cargo/no-listing-02-workspace-with-two-crates/add/add_one/src/lib.rs}}
```

Nous pouvons maintenant faire dépendre le paquet `adder`, qui contient notre binaire, du paquet `add_one`, qui contient notre bibliothèque. Nous devons d’abord ajouter une dépendance de chemin vers `add_one` dans _adder/Cargo.toml_.

<span class="filename">Nom du fichier : adder/Cargo.toml</span>

```toml
{{#include ../listings/ch14-more-about-cargo/no-listing-02-workspace-with-two-crates/add/adder/Cargo.toml:6:7}}
```

Cargo ne suppose pas que les caisses d’un espace de travail dépendront les unes des autres ; nous devons donc préciser explicitement les relations de dépendance.

Ensuite, utilisons la fonction `add_one` (de la caisse `add_one`) dans la caisse `adder`. Ouvrez le fichier _adder/src/main.rs_ et modifiez la fonction `main` pour qu’elle appelle la fonction `add_one`, comme dans la liste 14-7.

<Listing number="14-7" file-name="adder/src/main.rs" caption="Utilisation de la caisse bibliothèque `add_one` depuis la caisse `adder`">

```rust,ignore
{{#rustdoc_include ../listings/ch14-more-about-cargo/listing-14-07/add/adder/src/main.rs}}
```

</Listing>

Compilons l’espace de travail en exécutant `cargo build` dans le répertoire _add_ de niveau supérieur !

<!-- manual-regeneration
cd listings/ch14-more-about-cargo/listing-14-07/add
cargo build
copy output below; the output updating script doesn't handle subdirectories in paths properly
-->

```console
$ cargo build
   Compiling add_one v0.1.0 (file:///projects/add/add_one)
   Compiling adder v0.1.0 (file:///projects/add/adder)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.22s
```

Pour exécuter la caisse binaire depuis le répertoire _add_, nous pouvons préciser le paquet de l’espace de travail à exécuter en utilisant l’argument `-p`, suivi du nom du paquet, avec `cargo run` :

<!-- manual-regeneration
cd listings/ch14-more-about-cargo/listing-14-07/add
cargo run -p adder
copy output below; the output updating script doesn't handle subdirectories in paths properly
-->

```console
$ cargo run -p adder
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.00s
     Running `target/debug/adder`
Hello, world! 10 plus one is 11!
```

Cela exécute le code dans _adder/src/main.rs_, qui dépend de la caisse `add_one`.

<!-- Old headings. Do not remove or links may break. -->

<a id="depending-on-an-external-package-in-a-workspace"></a>

### Dépendre d’un paquet externe

Remarquez que l’espace de travail ne possède qu’un seul fichier _Cargo.lock_ à son niveau supérieur, au lieu d’un fichier _Cargo.lock_ dans le répertoire de chaque caisse. Cela garantit que toutes les caisses utilisent les mêmes versions de toutes les dépendances. Si nous ajoutons le paquet `rand` aux fichiers _adder/Cargo.toml_ et _add_one/Cargo.toml_, Cargo résoudra les deux dépendances vers une seule version de `rand` et l’enregistrera dans l’unique fichier _Cargo.lock_. Le fait que toutes les caisses de l’espace de travail utilisent les mêmes dépendances garantit leur compatibilité mutuelle. Ajoutons la caisse `rand` à la section `[dependencies]` du fichier _add_one/Cargo.toml_ afin de pouvoir utiliser la caisse `rand` dans la caisse `add_one` :

<!-- When updating the version of `rand` used, also update the version of
`rand` used in these files so they all match:

* ch01-01-installation.md
* ch02-00-guessing-game-tutorial.md
* ch07-04-bringing-paths-into-scope-with-the-use-keyword.md
-->

<span class="filename">Nom du fichier : add_one/Cargo.toml</span>

```toml
{{#include ../listings/ch14-more-about-cargo/no-listing-03-workspace-with-external-dependency/add/add_one/Cargo.toml:6:7}}
```

Nous pouvons maintenant ajouter `use rand;` au fichier _add_one/src/lib.rs_ ; la compilation de tout l’espace de travail en exécutant `cargo build` dans le répertoire _add_ téléchargera et compilera la caisse `rand`. Nous obtiendrons un avertissement, car nous ne faisons pas référence à la caisse `rand` que nous avons importée dans la portée :

<!-- manual-regeneration
cd listings/ch14-more-about-cargo/no-listing-03-workspace-with-external-dependency/add
cargo build
copy output below; the output updating script doesn't handle subdirectories in paths properly
-->

```console
$ cargo build
    Updating crates.io index
  Downloaded rand v0.10.1
   --snip--
   Compiling rand v0.10.1
   Compiling add_one v0.1.0 (file:///projects/add/add_one)
warning: unused import: `rand`
 --> add_one/src/lib.rs:1:5
  |
1 | use rand;
  |     ^^^^
  |
  = note: `#[warn(unused_imports)]` (part of `#[warn(unused)]`) on by default

warning: `add_one` (lib) generated 1 warning (run `cargo fix --lib -p add_one` to apply 1 suggestion)
   Compiling adder v0.1.0 (file:///projects/add/adder)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.95s
```

Le fichier _Cargo.lock_ de niveau supérieur contient maintenant des informations sur la dépendance de `add_one` à `rand`. Toutefois, même si `rand` est utilisée quelque part dans l’espace de travail, nous ne pouvons pas l’utiliser dans les autres caisses de l’espace de travail, à moins de l’ajouter également à leurs fichiers _Cargo.toml_. Par exemple, si nous ajoutons `use rand;` au fichier _adder/src/main.rs_ du paquet `adder`, nous obtiendrons une erreur :

<!-- manual-regeneration
cd listings/ch14-more-about-cargo/output-only-03-use-rand/add
cargo build
copy output below; the output updating script doesn't handle subdirectories in paths properly
-->

```console
$ cargo build
  --snip--
   Compiling adder v0.1.0 (file:///projects/add/adder)
error[E0432]: unresolved import `rand`
 --> adder/src/main.rs:2:5
  |
2 | use rand;
  |     ^^^^ no external crate `rand`
```

Pour corriger cela, modifiez le fichier _Cargo.toml_ du paquet `adder` et indiquez que `rand` est également une dépendance pour celui-ci. La compilation du paquet `adder` ajoutera `rand` à la liste de ses dépendances dans _Cargo.lock_, mais aucune copie supplémentaire de `rand` ne sera téléchargée. Cargo veillera à ce que chaque caisse de chaque paquet de l’espace de travail utilisant le paquet `rand` utilise la même version, tant qu’elles spécifient des versions compatibles de `rand`. Cela nous permet d’économiser de l’espace et garantit la compatibilité des caisses de l’espace de travail.

Si les caisses de l’espace de travail spécifient des versions incompatibles d’une même dépendance, Cargo résoudra chacune d’elles, tout en essayant de résoudre le moins de versions possible.

### Ajouter un test à un espace de travail

Pour une autre amélioration, ajoutons un test de la fonction `add_one::add_one` dans la caisse `add_one` :

<span class="filename">Nom du fichier : add_one/src/lib.rs</span>

```rust,noplayground
{{#rustdoc_include ../listings/ch14-more-about-cargo/no-listing-04-workspace-with-tests/add/add_one/src/lib.rs}}
```

Exécutez maintenant `cargo test` dans le répertoire _add_ de niveau supérieur. L’exécution de `cargo test` dans un espace de travail structuré comme celui-ci lancera les tests de toutes les caisses de l’espace de travail :

<!-- manual-regeneration
cd listings/ch14-more-about-cargo/no-listing-04-workspace-with-tests/add
cargo test
copy output below; the output updating script doesn't handle subdirectories in
paths properly
-->

```console
$ cargo test
   Compiling add_one v0.1.0 (file:///projects/add/add_one)
   Compiling adder v0.1.0 (file:///projects/add/adder)
    Finished `test` profile [unoptimized + debuginfo] target(s) in 0.20s
     Running unittests src/lib.rs (target/debug/deps/add_one-93c49ee75dc46543)

running 1 test
test tests::it_works ... ok

test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

     Running unittests src/main.rs (target/debug/deps/adder-3a47283c568d2b6a)

running 0 tests

test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

   Doc-tests add_one

running 0 tests

test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s
```

La première partie de la sortie montre que le test `it_works` de la caisse `add_one` a réussi. La partie suivante indique qu’aucun test n’a été trouvé dans la caisse `adder`, puis la dernière partie montre qu’aucun test de documentation n’a été trouvé dans la caisse `add_one`.

Nous pouvons également lancer les tests d’une caisse particulière de l’espace de travail depuis le répertoire de niveau supérieur en utilisant l’indicateur `-p` et en précisant le nom de la caisse à tester :

<!-- manual-regeneration
cd listings/ch14-more-about-cargo/no-listing-04-workspace-with-tests/add
cargo test -p add_one
copy output below; the output updating script doesn't handle subdirectories in paths properly
-->

```console
$ cargo test -p add_one
    Finished `test` profile [unoptimized + debuginfo] target(s) in 0.00s
     Running unittests src/lib.rs (target/debug/deps/add_one-93c49ee75dc46543)

running 1 test
test tests::it_works ... ok

test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

   Doc-tests add_one

running 0 tests

test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s
```

Cette sortie montre que `cargo test` n’a exécuté que les tests de la caisse `add_one` et n’a pas exécuté ceux de la caisse `adder`.

Si vous publiez les caisses de l’espace de travail sur [crates.io](https://crates.io/)<!-- ignore -->, chaque caisse devra être publiée séparément. Comme avec `cargo test`, nous pouvons publier une caisse particulière de notre espace de travail en utilisant l’indicateur `-p` et en indiquant le nom de la caisse à publier.

Pour vous exercer davantage, ajoutez une caisse `add_two` à cet espace de travail, de la même manière que la caisse `add_one` !

À mesure que votre projet grandit, envisagez d’utiliser un espace de travail : cela vous permet de travailler avec des composants plus petits et plus faciles à comprendre qu’un gros bloc de code. De plus, conserver les caisses dans un espace de travail peut faciliter leur coordination si elles sont souvent modifiées en même temps.