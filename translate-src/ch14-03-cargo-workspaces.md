## Espaces de travail Cargo

Dans le Chapitre 12, nous avons construit un paquet incluant un crate binaire et un crate de bibliothèque. Au fur et à mesure que votre projet se développe, vous pourriez constater que le crate de bibliothèque continue de grossir et que vous souhaitez diviser davantage votre paquet en plusieurs crates de bibliothèque. Cargo offre une fonctionnalité appelée _espaces de travail_ qui peut aider à gérer plusieurs paquets connexes développés en tandem.

### Création d'un espace de travail

Un _espace de travail_ est un ensemble de paquets qui partagent le même _Cargo.lock_ et répertoire de sortie. Créons un projet utilisant un espace de travail—nous utiliserons un code trivial afin de pouvoir nous concentrer sur la structure de l'espace de travail. Il existe plusieurs manières de structurer un espace de travail, donc nous allons simplement montrer une manière courante. Nous aurons un espace de travail contenant un binaire et deux bibliothèques. Le binaire, qui fournira la fonctionnalité principale, dépendra des deux bibliothèques. Une bibliothèque fournira une fonction `add_one` et l'autre une fonction `add_two`. Ces trois crates feront partie du même espace de travail. Nous commencerons par créer un nouveau répertoire pour l'espace de travail :

```console
$ mkdir add
$ cd add
```

Ensuite, dans le répertoire _add_, nous créons le fichier _Cargo.toml_ qui configurera l'ensemble de l'espace de travail. Ce fichier n'aura pas de section `[package]`. Au lieu de cela, il commencera par une section `[workspace]` qui nous permettra d'ajouter des membres à l'espace de travail. Nous veillons également à utiliser la dernière et la meilleure version de l'algorithme de résolution de Cargo dans notre espace de travail en définissant la valeur `resolver` sur `"3"` :

<span class="filename">Nom du fichier : Cargo.toml</span>

```toml
{{#include ../listings/ch14-more-about-cargo/no-listing-01-workspace/add/Cargo.toml}}
```

Ensuite, nous créerons le crate binaire `adder` en exécutant `cargo new` dans le répertoire _add_ :

```console
$ cargo new adder
     Created binary (application) `adder` package
      Adding `adder` as member of workspace at `file:///projects/add`
```

Exécuter `cargo new` à l'intérieur d'un espace de travail ajoute automatiquement le nouveau paquet à la clé `members` dans la définition `[workspace]` dans le _Cargo.toml_ de l'espace de travail, comme ceci :

```toml
{{#include ../listings/ch14-more-about-cargo/output-only-01-adder-crate/add/Cargo.toml}}
```

À ce stade, nous pouvons construire l'espace de travail en exécutant `cargo build`. Les fichiers dans votre répertoire _add_ devraient ressembler à ceci :

```text
├── Cargo.lock
├── Cargo.toml
├── adder
│   ├── Cargo.toml
│   └── src
│       └── main.rs
└── target
```

L'espace de travail a un répertoire _target_ au niveau supérieur dans lequel les artefacts compilés seront placés ; le paquet `adder` n'a pas son propre répertoire _target_. Même si nous devions exécuter `cargo build` depuis l'intérieur du répertoire _adder_, les artefacts compilés se retrouveraient toujours dans _add/target_ plutôt que dans _add/adder/target_. Cargo structure le répertoire _target_ dans un espace de travail de cette manière parce que les crates dans un espace de travail sont censées dépendre les unes des autres. Si chaque crate avait son propre répertoire _target_, chaque crate devrait recompiler chacune des autres crates dans l'espace de travail pour placer les artefacts dans son propre répertoire _target_. En partageant un seul répertoire _target_, les crates peuvent éviter des reconstructions inutiles.

### Création du deuxième paquet dans l'espace de travail

Ensuite, créons un autre paquet membre dans l'espace de travail et appelons-le `add_one`. Générons un nouveau crate de bibliothèque nommé `add_one` :

```console
$ cargo new add_one --lib
     Created library `add_one` package
      Adding `add_one` as member of workspace at `file:///projects/add`
```

Le _Cargo.toml_ de niveau supérieur inclura maintenant le chemin _add_one_ dans la liste `members` :

<span class="filename">Nom du fichier : Cargo.toml</span>

```toml
{{#include ../listings/ch14-more-about-cargo/no-listing-02-workspace-with-two-crates/add/Cargo.toml}}
```

Votre répertoire _add_ devrait maintenant avoir ces répertoires et fichiers :

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

Nous pouvons maintenant faire en sorte que le paquet `adder` avec notre binaire dépende du paquet `add_one` qui contient notre bibliothèque. Tout d'abord, nous devrons ajouter une dépendance de chemin sur `add_one` au _adder/Cargo.toml_.

<span class="filename">Nom du fichier : adder/Cargo.toml</span>

```toml
{{#include ../listings/ch14-more-about-cargo/no-listing-02-workspace-with-two-crates/add/adder/Cargo.toml:6:7}}
```

Cargo ne suppose pas que les crates dans un espace de travail dépendront les unes des autres, donc nous devons être explicites sur les relations de dépendance.

Ensuite, utilisons la fonction `add_one` (du crate `add_one`) dans le crate `adder`. Ouvrons le fichier _adder/src/main.rs_ et modifions la fonction `main` pour appeler la fonction `add_one`, comme dans la Listing 14-7.

<Listing number="14-7" file-name="adder/src/main.rs" caption="Utilisation de la bibliothèque crate `add_one` depuis le crate `adder`">

```rust,ignore
{{#rustdoc_include ../listings/ch14-more-about-cargo/listing-14-07/add/adder/src/main.rs}}
```

</Listing>

Construisons l'espace de travail en exécutant `cargo build` dans le répertoire de niveau supérieur _add_ !

```console
$ cargo build
   Compiling add_one v0.1.0 (file:///projects/add/add_one)
   Compiling adder v0.1.0 (file:///projects/add/adder)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.22s
```

Pour exécuter le crate binaire depuis le répertoire _add_, nous pouvons spécifier quel paquet de l'espace de travail nous voulons exécuter en utilisant l'argument `-p` et le nom du paquet avec `cargo run` :

```console
$ cargo run -p adder
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.00s
     Running `target/debug/adder`
Hello, world! 10 plus one is 11!
```

Cela exécute le code dans _adder/src/main.rs_, qui dépend du crate `add_one`.

### Dépendre d'un paquet externe dans un espace de travail

Remarquez que l'espace de travail a seulement un fichier _Cargo.lock_ au niveau supérieur, au lieu d'avoir un _Cargo.lock_ dans chaque répertoire de crate. Cela garantit que toutes les crates utilisent la même version de toutes les dépendances. Si nous ajoutons le paquet `rand` aux fichiers _adder/Cargo.toml_ et _add_one/Cargo.toml_, Cargo résoudra les deux à une version de `rand` et l'enregistrera dans le fichier _Cargo.lock_. Faire en sorte que toutes les crates dans l'espace de travail utilisent les mêmes dépendances signifie que les crates seront toujours compatibles entre elles. Ajoutons le crate `rand` à la section `[dependencies]` dans le fichier _add_one/Cargo.toml_ afin que nous puissions l'utiliser dans le crate `add_one` :

<span class="filename">Nom du fichier : add_one/Cargo.toml</span>

```toml
{{#include ../listings/ch14-more-about-cargo/no-listing-03-workspace-with-external-dependency/add/add_one/Cargo.toml:6:7}}
```

Nous pouvons maintenant ajouter `use rand;` dans le fichier _add_one/src/lib.rs_, et la construction de l'ensemble de l'espace de travail en exécutant `cargo build` dans le répertoire _add_ ramènera et compilera le crate `rand`. Nous recevrons un avertissement car nous ne faisons pas référence au `rand` que nous avons importé :

```console
$ cargo build
    Updating crates.io index
  Downloaded rand v0.8.5
   --snip--
   Compiling rand v0.8.5
   Compiling add_one v0.1.0 (file:///projects/add/add_one)
warning: unused import: `rand`
 --> add_one/src/lib.rs:1:5
  |
1 | use rand;
  |     ^^^^
  |
  = note: `#[warn(unused_imports)]` on by default

warning: `add_one` (lib) generated 1 warning (run `cargo fix --lib -p add_one` to apply 1 suggestion)
   Compiling adder v0.1.0 (file:///projects/add/adder)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.95s
```

Le fichier _Cargo.lock_ de niveau supérieur contient désormais des informations sur la dépendance de `add_one` sur `rand`. Cependant, même si `rand` est utilisé quelque part dans l'espace de travail, nous ne pouvons pas l'utiliser dans d'autres crates de l'espace de travail à moins d'ajouter `rand` à leurs fichiers _Cargo.toml_ également. Par exemple, si nous ajoutons `use rand;` au fichier _adder/src/main.rs_ pour le paquet `adder`, nous obtiendrons une erreur :

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

Pour corriger cela, éditez le fichier _Cargo.toml_ pour le paquet `adder` et indiquez que `rand` est également une dépendance pour lui. Construire le paquet `adder` ajoutera `rand` à la liste des dépendances pour `adder` dans _Cargo.lock_, mais aucune copie supplémentaire de `rand` ne sera téléchargée. Cargo s'assurera que chaque crate dans chaque paquet dans l'espace de travail utilisant le paquet `rand` utilisera la même version tant qu'elles spécifient des versions compatibles de `rand`, économisant de l'espace et garantissant que les crates dans l'espace de travail seront compatibles entre elles.

Si les crates dans l'espace de travail spécifient des versions incompatibles de la même dépendance, Cargo les résoudra chacune mais essaiera toujours de résoudre le moins de versions possible.

### Ajout d'un test à un espace de travail

Pour une autre amélioration, ajoutons un test de la fonction `add_one::add_one` dans le crate `add_one` :

<span class="filename">Nom du fichier : add_one/src/lib.rs</span>

```rust,noplayground
{{#rustdoc_include ../listings/ch14-more-about-cargo/no-listing-04-workspace-with-tests/add/add_one/src/lib.rs}}
```

Maintenant exécutez `cargo test` dans le répertoire de niveau supérieur _add_. Exécuter `cargo test` dans un espace de travail structuré comme celui-ci exécutera les tests pour toutes les crates de l'espace de travail :

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

La première section de la sortie montre que le test `it_works` dans le crate `add_one` a réussi. La section suivante montre que zéro tests ont été trouvés dans le crate `adder`, et puis la dernière section montre que zéro tests de documentation ont été trouvés dans le crate `add_one`.

Nous pouvons également exécuter des tests pour un crate particulier dans un espace de travail depuis le répertoire de niveau supérieur en utilisant le drapeau `-p` et en spécifiant le nom du crate que nous voulons tester :

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

Cette sortie montre que `cargo test` n'a exécuté que les tests pour le crate `add_one` et n'a pas exécuté les tests du crate `adder`.

Si vous publiez les crates dans l'espace de travail sur
[crates.io](https://crates.io/), chaque crate dans l'espace de travail devra être publiée séparément. Comme `cargo test`, nous pouvons publier un crate particulier dans notre espace de travail en utilisant le drapeau `-p` et en spécifiant le nom du crate que nous voulons publier.

Pour un exercice supplémentaire, ajoutez un crate `add_two` à cet espace de travail de manière similaire au crate `add_one` !

Au fur et à mesure que votre projet grandit, envisagez d'utiliser un espace de travail : cela vous permet de travailler avec des composants plus petits et plus faciles à comprendre qu'un gros bloc de code. De plus, garder les crates dans un espace de travail peut faciliter la coordination entre les crates qui sont souvent modifiées en même temps.