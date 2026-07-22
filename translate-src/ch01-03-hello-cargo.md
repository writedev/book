## Bonjour, Cargo !

Cargo est le système de build et le gestionnaire de paquets de Rust. La plupart des Rustaceans utilisent cet outil pour gérer leurs projets Rust, car Cargo s'occupe de nombreuses tâches pour vous, comme la compilation de votre code, le téléchargement des bibliothèques dont dépend votre code, et la compilation de ces bibliothèques. (Nous appelons les bibliothèques dont votre code a besoin des _dépendances_.)

Les programmes Rust les plus simples, comme celui que nous avons écrit jusqu'à présent, n'ont pas de dépendances. Si nous avions construit le projet "Hello, world !" avec Cargo, il utiliserait uniquement la partie de Cargo qui gère la compilation de votre code. Au fur et à mesure que vous écrivez des programmes Rust plus complexes, vous ajouterez des dépendances, et si vous commencez un projet en utilisant Cargo, l'ajout de dépendances sera beaucoup plus facile.

Étant donné que la grande majorité des projets Rust utilisent Cargo, le reste de ce livre suppose que vous utilisez également Cargo. Cargo est installé avec Rust si vous avez utilisé les installateurs officiels discutés dans la section [“Installation”][installation]<!-- ignore -->. Si vous avez installé Rust par d'autres moyens, vérifiez si Cargo est installé en entrant ce qui suit dans votre terminal :

```console
$ cargo --version
```

Si vous voyez un numéro de version, vous l'avez ! Si vous voyez une erreur, comme `commande introuvable`, consultez la documentation de votre méthode d'installation pour déterminer comment installer Cargo séparément.

### Création d'un Projet avec Cargo

Créons un nouveau projet en utilisant Cargo et examinons comment il diffère de notre projet original "Hello, world !". Retournez dans votre répertoire _projects_ (ou là où vous avez décidé de stocker votre code). Ensuite, sur n'importe quel système d'exploitation, exécutez ce qui suit :

```console
$ cargo new hello_cargo
$ cd hello_cargo
```

La première commande crée un nouveau répertoire et un projet appelé _hello_cargo_. Nous avons nommé notre projet _hello_cargo_, et Cargo crée ses fichiers dans un répertoire du même nom.

Accédez au répertoire _hello_cargo_ et listez les fichiers. Vous verrez que Cargo a généré deux fichiers et un répertoire pour nous : un fichier _Cargo.toml_ et un répertoire _src_ avec un fichier _main.rs_ à l'intérieur.

Il a également initialisé un nouveau dépôt Git avec un fichier _.gitignore_. Les fichiers Git ne seront pas générés si vous exécutez `cargo new` au sein d'un dépôt Git existant ; vous pouvez contourner ce comportement en utilisant `cargo new --vcs=git`.

> Note : Git est un système de contrôle de version courant. Vous pouvez changer `cargo new` pour utiliser un autre système de contrôle de version ou pas de système de contrôle de version en utilisant le paramètre `--vcs`. Exécutez `cargo new --help` pour voir les options disponibles.

Ouvrez _Cargo.toml_ dans votre éditeur de texte de votre choix. Il devrait ressembler au code dans la Liste 1-2.

<Listing number="1-2" file-name="Cargo.toml" caption="Contenu de *Cargo.toml* généré par `cargo new`">

```toml
[package]
name = "hello_cargo"
version = "0.1.0"
edition = "2024"

[dependencies]
```

</Listing>

Ce fichier est au format [_TOML_][toml]<!-- ignore --> (_Tom's Obvious, Minimal Language_), qui est le format de configuration de Cargo.

La première ligne, `[package]`, est un en-tête de section qui indique que les déclarations suivantes configurent un paquet. Au fur et à mesure que nous ajoutons plus d'informations à ce fichier, nous ajouterons d'autres sections.

Les trois lignes suivantes définissent les informations de configuration dont Cargo a besoin pour compiler votre programme : le nom, la version et l'édition de Rust à utiliser. Nous parlerons de la clé `edition` dans [Annexe E][appendix-e]<!-- ignore -->.

La dernière ligne, `[dependencies]`, est le début d'une section où vous pouvez lister les dépendances de votre projet. En Rust, les paquets de code sont appelés des _crates_. Nous n'aurons pas besoin d'autres crates pour ce projet, mais nous le ferons dans le premier projet du Chapitre 2, donc nous utiliserons cette section des dépendances à ce moment-là.

Maintenant, ouvrez _src/main.rs_ et jetez un œil :

<span class="filename">Nom de fichier : src/main.rs</span>

```rust
fn main() {
    println!("Hello, world!");
}
```

Cargo a généré un programme "Hello, world !" pour vous, tout comme celui que nous avons écrit dans la Liste 1-1 ! Jusqu'à présent, les différences entre notre projet et le projet généré par Cargo sont que Cargo a placé le code dans le répertoire _src_, et nous avons un fichier de configuration _Cargo.toml_ dans le répertoire supérieur.

Cargo s'attend à ce que vos fichiers source se trouvent dans le répertoire _src_. Le répertoire de projet de niveau supérieur est destiné aux fichiers README, aux informations de licence, aux fichiers de configuration et à tout ce qui n'est pas lié à votre code. Utiliser Cargo vous aide à organiser vos projets. Il y a une place pour chaque chose, et chaque chose est à sa place.

Si vous avez commencé un projet qui n'utilise pas Cargo, comme nous l'avons fait avec le projet "Hello, world !", vous pouvez le convertir en un projet qui utilise Cargo. Déplacez le code du projet dans le répertoire _src_ et créez un fichier _Cargo.toml_ approprié. Un moyen facile d'obtenir ce fichier _Cargo.toml_ est d'exécuter `cargo init`, qui le créera automatiquement pour vous.

### Compilation et Exécution d'un Projet Cargo

Regardons maintenant ce qui change lorsque nous compilons et exécutons le programme "Hello, world !" avec Cargo ! Depuis votre répertoire _hello_cargo_, compilez votre projet en entrant la commande suivante :

```console
$ cargo build
   Compiling hello_cargo v0.1.0 (file:///projects/hello_cargo)
    Finished dev [unoptimized + debuginfo] target(s) in 2.85 secs
```

Cette commande crée un fichier exécutable dans _target/debug/hello_cargo_ (ou _target\debug\hello_cargo.exe_ sur Windows) plutôt que dans votre répertoire actuel. Comme la compilation par défaut est une compilation de débogage, Cargo place le binaire dans un répertoire nommé _debug_. Vous pouvez exécuter l'exécutable avec cette commande :

```console
$ ./target/debug/hello_cargo # ou .\target\debug\hello_cargo.exe sur Windows
Hello, world!
```

Si tout va bien, `Hello, world !` devrait s'afficher dans le terminal. L'exécution de `cargo build` pour la première fois fait également que Cargo crée un nouveau fichier au niveau supérieur : _Cargo.lock_. Ce fichier garde la trace des versions exactes des dépendances dans votre projet. Ce projet n'ayant pas de dépendances, le fichier est un peu sparse. Vous n'aurez jamais besoin de modifier ce fichier manuellement ; Cargo gère son contenu pour vous.

Nous venons de compiler un projet avec `cargo build` et de l'exécuter avec `./target/debug/hello_cargo`, mais nous pouvons également utiliser `cargo run` pour compiler le code et exécuter l'exécutable résultant en une seule commande :

```console
$ cargo run
    Finished dev [unoptimized + debuginfo] target(s) in 0.0 secs
     Running `target/debug/hello_cargo`
Hello, world!
```

Utiliser `cargo run` est plus pratique que d'avoir à se souvenir d'exécuter `cargo build` puis d'utiliser tout le chemin vers le binaire, donc la plupart des développeurs utilisent `cargo run`.

Remarquez que cette fois, nous n'avons pas vu de sortie indiquant que Cargo compilait `hello_cargo`. Cargo a compris que les fichiers n'avaient pas changé, donc il n'a pas reconstruit mais a simplement exécuté le binaire. Si vous aviez modifié votre code source, Cargo aurait reconstruit le projet avant de l'exécuter, et vous auriez vu cette sortie :

```console
$ cargo run
   Compiling hello_cargo v0.1.0 (file:///projects/hello_cargo)
    Finished dev [unoptimized + debuginfo] target(s) in 0.33 secs
     Running `target/debug/hello_cargo`
Hello, world!
```

Cargo fournit également une commande appelée `cargo check`. Cette commande vérifie rapidement votre code pour s'assurer qu'il se compile mais ne produit pas d'exécutable :

```console
$ cargo check
   Checking hello_cargo v0.1.0 (file:///projects/hello_cargo)
    Finished dev [unoptimized + debuginfo] target(s) in 0.32 secs
```

Pourquoi ne voudriez-vous pas un exécutable ? Souvent, `cargo check` est beaucoup plus rapide que `cargo build` car il saute l'étape de production d'un exécutable. Si vous vérifiez continuellement votre travail tout en écrivant le code, utiliser `cargo check` accélérera le processus en vous informant si votre projet se compile toujours ! Par conséquent, de nombreux Rustaceans exécutent `cargo check` périodiquement en écrivant leur programme pour s'assurer qu'il se compile. Ensuite, ils exécutent `cargo build` quand ils sont prêts à utiliser l'exécutable.

Récapitulons ce que nous avons appris jusqu'à présent sur Cargo :

- Nous pouvons créer un projet en utilisant `cargo new`.
- Nous pouvons compiler un projet en utilisant `cargo build`.
- Nous pouvons compiler et exécuter un projet en une seule étape en utilisant `cargo run`.
- Nous pouvons compiler un projet sans produire de binaire pour vérifier les erreurs en utilisant `cargo check`.
- Au lieu de sauvegarder le résultat de la compilation dans le même répertoire que notre code, Cargo le stocke dans le répertoire _target/debug_.

Un avantage supplémentaire de l'utilisation de Cargo est que les commandes sont les mêmes peu importe le système d'exploitation sur lequel vous travaillez. Ainsi, à ce stade, nous ne fournirons plus d'instructions spécifiques pour Linux et macOS par rapport à Windows.

### Compilation pour la Version Finale

Lorsque votre projet est enfin prêt pour la sortie, vous pouvez utiliser `cargo build --release` pour le compiler avec des optimisations. Cette commande créera un exécutable dans _target/release_ au lieu de _target/debug_. Les optimisations rendent votre code Rust plus rapide, mais les activer allonge le temps nécessaire à la compilation. C'est pourquoi il existe deux profils différents : un pour le développement, lorsque vous souhaitez reconstruire rapidement et souvent, et un autre pour construire le programme final que vous donnerez à un utilisateur, qui ne sera pas reconstruit plusieurs fois et qui s'exécutera aussi rapidement que possible. Si vous testez le temps d'exécution de votre code, assurez-vous d'exécuter `cargo build --release` et de faire des benchmarks avec l'exécutable dans _target/release_.

<!-- Ancien titres. Ne pas supprimer ou les liens pourraient se casser. -->
<a id="cargo-as-convention"></a>

### Tirer Parti des Conventions de Cargo

Avec des projets simples, Cargo ne fournit pas beaucoup de valeur par rapport à l'utilisation de `rustc`, mais il prouvera sa valeur à mesure que vos programmes deviendront plus complexes. Une fois que les programmes grandissent en plusieurs fichiers ou nécessitent une dépendance, il est beaucoup plus facile de laisser Cargo coordonner la compilation.

Bien que le projet `hello_cargo` soit simple, il utilise déjà beaucoup des outils réels que vous utiliserez dans le reste de votre carrière Rust. En fait, pour travailler sur des projets existants, vous pouvez utiliser les commandes suivantes pour récupérer le code avec Git, changer dans le répertoire de ce projet, et le compiler :

```console
$ git clone example.org/someproject
$ cd someproject
$ cargo build
```

Pour plus d'informations sur Cargo, consultez [sa documentation][cargo].

## Résumé

Vous êtes déjà bien parti dans votre parcours Rust ! Dans ce chapitre, vous avez appris à :

- Installer la dernière version stable de Rust en utilisant `rustup`.
- Mettre à jour vers une nouvelle version de Rust.
- Ouvrir la documentation localement installée.
- Écrire et exécuter un programme "Hello, world !" en utilisant `rustc` directement.
- Créer et exécuter un nouveau projet en utilisant les conventions de Cargo.

C'est un excellent moment pour construire un programme plus conséquent afin de vous habituer à lire et écrire du code Rust. Donc, dans le Chapitre 2, nous construirons un programme de jeu de devinette. Si vous préférez commencer par apprendre comment fonctionnent les concepts de programmation courants en Rust, consultez le Chapitre 3 puis revenez au Chapitre 2.

[installation]: ch01-01-installation.html#installation
[toml]: https://toml.io
[appendix-e]: appendix-05-editions.html
[cargo]: https://doc.rust-lang.org/cargo/