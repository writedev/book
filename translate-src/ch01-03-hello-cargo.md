## Bonjour, Cargo !

Cargo est le système de compilation et le gestionnaire de paquets de Rust. La plupart des Rustacéens utilisent cet outil pour gérer leurs projets Rust, car Cargo s’occupe de nombreuses tâches à votre place, comme compiler votre code, télécharger les bibliothèques dont il dépend et compiler ces bibliothèques. (Nous appelons ces bibliothèques des _dépendances_.)

Les programmes Rust les plus simples, comme celui que nous avons écrit jusqu’à présent, n’ont aucune dépendance. Si nous avions créé le projet « Hello, world! » avec Cargo, nous n’aurions utilisé que la partie de Cargo chargée de compiler votre code. À mesure que vous écrirez des programmes Rust plus complexes, vous ajouterez des dépendances, et si vous démarrez un projet avec Cargo, il sera beaucoup plus facile de les ajouter.

Comme la grande majorité des projets Rust utilisent Cargo, le reste de ce livre part du principe que vous l’utilisez aussi. Cargo est installé avec Rust si vous avez utilisé les programmes d’installation officiels présentés dans la section [« Installation »][installation]<!-- ignore -->. Si vous avez installé Rust par un autre moyen, vérifiez si Cargo est installé en saisissant la commande suivante dans votre terminal :

```console
$ cargo --version
```

Si un numéro de version s’affiche, c’est bon ! Si une erreur s’affiche, comme `command
not found`, consultez la documentation correspondant à votre méthode d’installation pour savoir comment installer Cargo séparément.

### Créer un projet avec Cargo

Créons un nouveau projet avec Cargo et voyons en quoi il diffère de notre projet « Hello, world! » initial. Retournez dans votre répertoire _projects_ (ou dans le répertoire où vous avez décidé de stocker votre code). Ensuite, quel que soit votre système d’exploitation, exécutez la commande suivante :

```console
$ cargo new hello_cargo
$ cd hello_cargo
```

La première commande crée un nouveau répertoire et un projet nommé _hello_cargo_. Nous avons nommé notre projet _hello_cargo_, et Cargo crée ses fichiers dans un répertoire du même nom.

Accédez au répertoire _hello_cargo_ et affichez la liste de ses fichiers. Vous verrez que Cargo a généré deux fichiers et un répertoire : un fichier _Cargo.toml_ et un répertoire _src_ contenant un fichier _main.rs_.

Cargo a également initialisé un nouveau dépôt Git et créé un fichier _.gitignore_. Les fichiers Git ne seront pas générés si vous exécutez `cargo new` dans un dépôt Git existant ; vous pouvez modifier ce comportement en utilisant `cargo new --vcs=git`.

> Remarque : Git est un système de gestion de versions courant. Vous pouvez configurer `cargo new` pour utiliser un autre système de gestion de versions, ou aucun système, en utilisant l’option `--vcs`. Exécutez `cargo new --help` pour consulter les options disponibles.

Ouvrez _Cargo.toml_ dans l’éditeur de texte de votre choix. Son contenu devrait ressembler au code de la liste 1-2.

<Listing number="1-2" file-name="Cargo.toml" caption="Contenu de *Cargo.toml* généré par `cargo new`">

```toml
[package]
name = "hello_cargo"
version = "0.1.0"
edition = "2024"

[dependencies]
```

</Listing>

Ce fichier utilise le format [_TOML_][toml]<!-- ignore --> (_Tom’s Obvious, Minimal Language_), qui est le format de configuration de Cargo.

La première ligne, `[package]`, est un en-tête de section qui indique que les lignes suivantes configurent un paquet. Lorsque nous ajouterons des informations à ce fichier, nous ajouterons d’autres sections.

Les trois lignes suivantes définissent les informations de configuration dont Cargo a besoin pour compiler votre programme : son nom, sa version et l’édition de Rust à utiliser. Nous parlerons de la clé `edition` dans [l’annexe E][appendix-e]<!-- ignore -->.

La dernière ligne, `[dependencies]`, marque le début d’une section dans laquelle vous pouvez répertorier les dépendances de votre projet. En Rust, les paquets de code sont appelés des _crates_. Nous n’aurons besoin d’aucun autre crate pour ce projet, mais ce sera le cas pour le premier projet du chapitre 2 ; nous utiliserons donc cette section consacrée aux dépendances à ce moment-là.

Ouvrez maintenant _src/main.rs_ et regardez son contenu :

<span class="filename">Nom du fichier : src/main.rs</span>

```rust
fn main() {
    println!("Hello, world!");
}
```

Cargo a généré pour vous un programme « Hello, world! », tout comme celui que nous avons écrit dans la liste 1-1 ! Jusqu’à présent, les différences entre notre projet et celui généré par Cargo sont que Cargo a placé le code dans le répertoire _src_ et que nous avons un fichier de configuration _Cargo.toml_ dans le répertoire supérieur.

Cargo s’attend à ce que vos fichiers source se trouvent dans le répertoire _src_. Le répertoire supérieur du projet est réservé aux fichiers README, aux informations de licence, aux fichiers de configuration et à tout ce qui n’est pas lié à votre code. Cargo vous aide à organiser vos projets. Chaque chose a sa place, et tout est à sa place.

Si vous avez démarré un projet sans utiliser Cargo, comme nous l’avons fait avec le projet « Hello, world! », vous pouvez le convertir en projet Cargo. Déplacez le code du projet dans le répertoire _src_ et créez un fichier _Cargo.toml_ adapté. Pour obtenir facilement ce fichier _Cargo.toml_, vous pouvez exécuter `cargo init`, qui le créera automatiquement pour vous.

### Compiler et exécuter un projet Cargo

Voyons maintenant ce qui change lorsque nous compilons et exécutons le programme « Hello, world! » avec Cargo ! Depuis votre répertoire _hello_cargo_, compilez votre projet en saisissant la commande suivante :

```console
$ cargo build
   Compiling hello_cargo v0.1.0 (file:///projects/hello_cargo)
    Finished dev [unoptimized + debuginfo] target(s) in 2.85 secs
```

Cette commande crée un fichier exécutable dans _target/debug/hello_cargo_ (ou _target\debug\hello_cargo.exe_ sous Windows), plutôt que dans le répertoire courant. Comme la compilation par défaut est une compilation de débogage, Cargo place le binaire dans un répertoire nommé _debug_. Vous pouvez exécuter le programme avec cette commande :

```console
$ ./target/debug/hello_cargo # or .\target\debug\hello_cargo.exe on Windows
Hello, world!
```

Si tout se passe bien, `Hello, world!` devrait s’afficher dans le terminal. La première exécution de `cargo
build` amène également Cargo à créer un nouveau fichier à la racine du projet : _Cargo.lock_. Ce fichier conserve la trace des versions exactes des dépendances de votre projet. Ce projet n’a pas de dépendances, donc ce fichier est assez succinct. Vous n’aurez jamais besoin de modifier ce fichier manuellement ; Cargo gère son contenu pour vous.

Nous venons de compiler un projet avec `cargo build` et de l’exécuter avec `./target/debug/hello_cargo`, mais nous pouvons aussi utiliser `cargo run` pour compiler le code, puis exécuter le programme généré, le tout avec une seule commande :

```console
$ cargo run
    Finished dev [unoptimized + debuginfo] target(s) in 0.0 secs
     Running `target/debug/hello_cargo`
Hello, world!
```

`cargo run` est plus pratique que de devoir se souvenir d’exécuter `cargo
build`, puis de saisir le chemin complet du binaire ; c’est pourquoi la plupart des développeurs utilisent `cargo
run`.

Remarquez que cette fois, aucun message n’indique que Cargo compile `hello_cargo`. Cargo a constaté que les fichiers n’avaient pas changé, il n’a donc pas recompilé le projet et a simplement exécuté le binaire. Si vous aviez modifié votre code source, Cargo aurait recompilé le projet avant de l’exécuter, et vous auriez vu le résultat suivant :

```console
$ cargo run
   Compiling hello_cargo v0.1.0 (file:///projects/hello_cargo)
    Finished dev [unoptimized + debuginfo] target(s) in 0.33 secs
     Running `target/debug/hello_cargo`
Hello, world!
```

Cargo fournit également une commande nommée `cargo check`. Cette commande vérifie rapidement que votre code compile, sans produire de fichier exécutable :

```console
$ cargo check
   Checking hello_cargo v0.1.0 (file:///projects/hello_cargo)
    Finished dev [unoptimized + debuginfo] target(s) in 0.32 secs
```

Pourquoi ne pas vouloir produire de fichier exécutable ? Souvent, `cargo check` est beaucoup plus rapide que `cargo build`, car cette commande ignore l’étape de création du fichier exécutable. Si vous vérifiez constamment votre travail pendant que vous écrivez le code, utiliser `cargo check` accélérera la vérification de la compilation de votre projet ! C’est pourquoi de nombreux Rustacéens exécutent régulièrement `cargo check` pendant qu’ils écrivent leur programme, afin de s’assurer qu’il compile. Ensuite, ils exécutent `cargo build` lorsqu’ils sont prêts à utiliser le fichier exécutable.

Récapitulons ce que nous avons appris jusqu’à présent sur Cargo :

- Nous pouvons créer un projet avec `cargo new`.
- Nous pouvons compiler un projet avec `cargo build`.
- Nous pouvons compiler et exécuter un projet en une seule étape avec `cargo run`.
- Nous pouvons compiler un projet sans produire de binaire, afin de vérifier s’il contient des erreurs, avec `cargo check`.
- Au lieu d’enregistrer le résultat de la compilation dans le même répertoire que notre code, Cargo le stocke dans le répertoire _target/debug_.

L’utilisation de Cargo présente un autre avantage : les commandes sont les mêmes quel que soit le système d’exploitation utilisé. À partir de maintenant, nous ne donnerons donc plus d’instructions distinctes pour Linux et macOS d’une part, et Windows d’autre part.

### Compiler pour la version finale

Lorsque votre projet est prêt à être publié, vous pouvez utiliser `cargo build
--release` pour le compiler avec des optimisations. Cette commande crée un fichier exécutable dans _target/release_ plutôt que dans _target/debug_. Les optimisations accélèrent l’exécution de votre code Rust, mais leur activation allonge le temps de compilation de votre programme. C’est pourquoi il existe deux profils différents : l’un pour le développement, lorsque vous souhaitez recompiler rapidement et souvent, et l’autre pour compiler le programme final destiné à un utilisateur, que vous ne recompilerez pas continuellement et qui s’exécutera aussi vite que possible. Si vous mesurez le temps d’exécution de votre code, veillez à exécuter `cargo build --release` et à effectuer vos mesures avec le fichier exécutable du répertoire _target/release_.

<!-- Old headings. Do not remove or links may break. -->
<a id="cargo-as-convention"></a>

### Tirer parti des conventions de Cargo

Pour les projets simples, Cargo n’apporte pas beaucoup plus que l’utilisation directe de `rustc`, mais il révélera toute son utilité à mesure que vos programmes deviendront plus complexes. Lorsque les programmes comportent plusieurs fichiers ou nécessitent une dépendance, il est beaucoup plus facile de laisser Cargo coordonner la compilation.

Même si le projet `hello_cargo` est simple, il utilise déjà une grande partie des outils que vous utiliserez tout au long de votre carrière avec Rust. En fait, pour travailler sur n’importe quel projet existant, vous pouvez utiliser les commandes suivantes pour récupérer le code avec Git, accéder au répertoire du projet et le compiler :

```console
$ git clone example.org/someproject
$ cd someproject
$ cargo build
```

Pour en savoir plus sur Cargo, consultez [sa documentation][cargo].

## Résumé

Votre parcours avec Rust commence déjà très bien ! Dans ce chapitre, vous avez appris à :

- Installer la dernière version stable de Rust avec `rustup`.
- Mettre à jour Rust vers une version plus récente.
- Ouvrir la documentation installée localement.
- Écrire et exécuter directement avec `rustc` un programme « Hello, world! ».
- Créer et exécuter un nouveau projet en suivant les conventions de Cargo.

C’est le moment idéal pour créer un programme plus conséquent afin de vous familiariser avec la lecture et l’écriture de code Rust. Au chapitre 2, nous allons donc créer un jeu de devinettes. Si vous préférez commencer par découvrir le fonctionnement des concepts de programmation courants en Rust, consultez le chapitre 3, puis revenez au chapitre 2.

[installation]: ch01-01-installation.html#installation
[toml]: https://toml.io
[appendix-e]: appendix-05-editions.html
[cargo]: https://doc.rust-lang.org/cargo/