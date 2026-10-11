# Programmer un jeu de devinettes

Plongeons dans Rust en réalisant ensemble un projet pratique ! Ce chapitre vous présente quelques concepts courants de Rust en vous montrant comment les utiliser dans un véritable programme. Vous découvrirez `let`, `match`, les méthodes, les fonctions associées, les crates externes et bien plus encore ! Dans les chapitres suivants, nous explorerons ces idées plus en détail. Dans ce chapitre, vous vous contenterez de pratiquer les bases.

Nous allons implémenter un grand classique des exercices de programmation pour débutants : un jeu de devinettes. Voici son fonctionnement : le programme génère un entier aléatoire entre 1 et 100. Il demande ensuite au joueur de saisir une proposition. Une fois celle-ci saisie, le programme indique si elle est trop petite ou trop grande. Si la proposition est correcte, le jeu affiche un message de félicitations et se termine.

## Configuration d’un nouveau projet

Pour configurer un nouveau projet, rendez-vous dans le répertoire _projects_ que vous avez créé au chapitre 1, puis créez un nouveau projet avec Cargo, comme ceci :

```console
$ cargo new guessing_game
$ cd guessing_game
```

La première commande, `cargo new`, prend le nom du projet (`guessing_game`) comme premier argument. La seconde commande accède au répertoire du nouveau projet.

Examinez le fichier _Cargo.toml_ généré :

<!-- manual-regeneration
cd listings/ch02-guessing-game-tutorial
rm -rf no-listing-01-cargo-new
cargo new no-listing-01-cargo-new --name guessing_game
cd no-listing-01-cargo-new
cargo run > output.txt 2>&1
cd ../../..
-->

<span class="filename">Nom du fichier : Cargo.toml</span>

```toml
{{#include ../listings/ch02-guessing-game-tutorial/no-listing-01-cargo-new/Cargo.toml}}
```

Comme vous l’avez vu au chapitre 1, `cargo new` génère pour vous un programme « Hello, world! ». Examinez le fichier _src/main.rs_ :

<span class="filename">Nom du fichier : src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/no-listing-01-cargo-new/src/main.rs}}
```

Nous allons maintenant compiler ce programme « Hello, world! » et l’exécuter en une seule étape à l’aide de la commande `cargo run` :

```console
{{#include ../listings/ch02-guessing-game-tutorial/no-listing-01-cargo-new/output.txt}}
```

La commande `run` est pratique lorsque vous devez faire rapidement des essais sur un projet, comme nous le ferons dans ce jeu : vous pouvez tester chaque itération avant de passer à la suivante.

Rouvrez le fichier _src/main.rs_. Vous écrirez tout le code dans ce fichier.

## Traiter une proposition

La première partie du programme de jeu demandera une saisie à l’utilisateur, traitera cette saisie et vérifiera qu’elle est dans le format attendu. Pour commencer, nous allons permettre au joueur de saisir une proposition. Saisissez le code de la liste 2-1 dans _src/main.rs_.

<Listing number="2-1" file-name="src/main.rs" caption="Code qui récupère la proposition de l’utilisateur et l’affiche">

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-01/src/main.rs:all}}
```

</Listing>

Ce code contient beaucoup d’informations, alors examinons-le ligne par ligne. Pour obtenir la saisie de l’utilisateur et afficher ensuite le résultat, nous devons importer la bibliothèque d’entrée/sortie `io` dans la portée. La bibliothèque `io` provient de la bibliothèque standard, appelée `std` :

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-01/src/main.rs:io}}
```

Par défaut, Rust dispose d’un ensemble d’éléments définis dans la bibliothèque standard qu’il importe dans la portée de chaque programme. Cet ensemble s’appelle le _prelude_. Vous pouvez en consulter tous les éléments [dans la documentation de la bibliothèque standard][prelude].

Si un type que vous souhaitez utiliser ne figure pas dans le prelude, vous devez l’importer explicitement dans la portée à l’aide d’une instruction `use`. La bibliothèque `std::io` fournit un certain nombre de fonctionnalités utiles, notamment la possibilité d’accepter une saisie de l’utilisateur.

Comme vous l’avez vu au chapitre 1, la fonction `main` est le point d’entrée du programme :

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-01/src/main.rs:main}}
```

La syntaxe `fn` déclare une nouvelle fonction ; les parenthèses `()` indiquent qu’elle ne prend aucun paramètre ; et l’accolade ouvrante `{` marque le début du corps de la fonction.

Comme vous l’avez également appris au chapitre 1, `println!` est une macro qui affiche une chaîne à l’écran :

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-01/src/main.rs:print}}
```

Ce code affiche une invite indiquant le but du jeu et demandant à l’utilisateur de saisir une proposition.

### Stocker des valeurs dans des variables

Ensuite, nous allons créer une _variable_ pour stocker la saisie de l’utilisateur, comme ceci :

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-01/src/main.rs:string}}
```

Le programme devient intéressant ! Cette petite ligne fait beaucoup de choses. Nous utilisons l’instruction `let` pour créer la variable. En voici un autre exemple :

```rust,ignore
let apples = 5;
```

Cette ligne crée une nouvelle variable nommée `apples` et lui associe la valeur `5`. En Rust, les variables sont immuables par défaut : une fois qu’une valeur leur est attribuée, elle ne change pas. Nous étudierons ce concept en détail dans la section [« Variables et mutabilité »][variables-and-mutability]<!-- ignore --> du chapitre 3. Pour rendre une variable mutable, nous ajoutons `mut` avant son nom :

```rust,ignore
let apples = 5; // immutable
let mut bananas = 5; // mutable
```

> Remarque : la syntaxe `//` commence un commentaire qui se poursuit jusqu’à la fin de la ligne. Rust ignore tout ce qui se trouve dans les commentaires. Nous les étudierons plus en détail au [chapitre 3][comments]<!-- ignore -->.

Pour revenir au programme du jeu de devinettes, vous savez maintenant que `let mut guess` introduit une variable mutable nommée `guess`. Le signe égal (`=`) indique à Rust que nous voulons maintenant associer une valeur à cette variable. À droite du signe égal se trouve la valeur associée à `guess`, qui est le résultat de l’appel à `String::new`, une fonction qui renvoie une nouvelle instance de `String`. [`String`][string]<!-- ignore --> est un type chaîne fourni par la bibliothèque standard ; il représente du texte encodé en UTF-8 dont la taille peut augmenter.

La syntaxe `::` dans la ligne `::new` indique que `new` est une fonction associée au type `String`. Une _fonction associée_ est une fonction implémentée sur un type — ici, `String`. Cette fonction `new` crée une nouvelle chaîne vide. Vous trouverez une fonction `new` sur de nombreux types, car c’est un nom courant pour une fonction qui crée une nouvelle valeur d’un certain type.

En définitive, la ligne `let mut guess = String::new();` a créé une variable mutable qui est actuellement associée à une nouvelle instance vide de `String`. Ouf !

### Recevoir la saisie de l’utilisateur

Rappelez-vous que nous avons inclus les fonctionnalités d’entrée/sortie de la bibliothèque standard à l’aide de `use std::io;` sur la première ligne du programme. Nous allons maintenant appeler la fonction `stdin` du module `io`, ce qui nous permettra de gérer la saisie de l’utilisateur :

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-01/src/main.rs:read}}
```

Si nous n’avions pas importé le module `io` avec `use std::io;` au début du programme, nous pourrions tout de même utiliser cette fonction en écrivant l’appel ainsi : `std::io::stdin`. La fonction `stdin` renvoie une instance de [`std::io::Stdin`][iostdin]<!-- ignore -->, un type qui représente un handle vers l’entrée standard de votre terminal.

Ensuite, la ligne `.read_line(&mut guess)` appelle la méthode [`read_line`][read_line]<!-- ignore --> sur le handle de l’entrée standard pour récupérer la saisie de l’utilisateur. Nous transmettons également `&mut guess` comme argument à `read_line` pour lui indiquer dans quelle chaîne stocker la saisie de l’utilisateur. Le rôle de `read_line` est de prendre tout ce que l’utilisateur saisit dans l’entrée standard et de l’ajouter à une chaîne (sans remplacer son contenu). Nous lui transmettons donc cette chaîne comme argument. L’argument chaîne doit être mutable afin que la méthode puisse en modifier le contenu.

Le symbole `&` indique que cet argument est une _référence_ : il permet à plusieurs parties de votre code d’accéder à une même donnée sans avoir à la copier plusieurs fois en mémoire. Les références sont une fonctionnalité complexe, et l’un des grands avantages de Rust est qu’elles sont sûres et faciles à utiliser. Vous n’avez pas besoin d’en connaître tous les détails pour terminer ce programme. Pour l’instant, il vous suffit de savoir que, tout comme les variables, les références sont immuables par défaut. Vous devez donc écrire `&mut guess` plutôt que `&guess` pour rendre la référence mutable. (Le chapitre 4 expliquera les références plus en détail.)

<!-- Old headings. Do not remove or links may break. -->

<a id="handling-potential-failure-with-the-result-type"></a>

### Gérer les échecs potentiels avec `Result`

Nous travaillons toujours sur cette ligne de code. Nous abordons maintenant une troisième ligne de texte, mais notez qu’elle fait toujours partie d’une seule ligne de code logique. La partie suivante est cette méthode :

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-01/src/main.rs:expect}}
```

Nous aurions pu écrire ce code ainsi :

```rust,ignore
io::stdin().read_line(&mut guess).expect("Failed to read line");
```

Cependant, une ligne aussi longue est difficile à lire, il vaut donc mieux la découper. Il est souvent judicieux d’ajouter des retours à la ligne et des espaces pour aérer les lignes longues lorsque vous appelez une méthode avec la syntaxe `.nom_de_methode()`. Voyons maintenant ce que fait cette ligne.

Comme nous l’avons mentionné précédemment, `read_line` place tout ce que l’utilisateur saisit dans la chaîne que nous lui transmettons, mais elle renvoie également une valeur `Result`. [`Result`][result]<!-- ignore --> est une [_énumération_][enums]<!-- ignore -->, souvent appelée _enum_, c’est-à-dire un type qui peut se trouver dans plusieurs états possibles. Chacun de ces états est appelé une _variante_.

Le [chapitre 6][enums]<!-- ignore --> traitera les enums plus en détail. Ces types `Result` servent à encoder des informations sur la gestion des erreurs.

Les variantes de `Result` sont `Ok` et `Err`. La variante `Ok` indique que l’opération a réussi et contient la valeur obtenue. La variante `Err` signifie que l’opération a échoué et contient des informations sur la manière dont l’échec s’est produit ou sur sa cause.

Les valeurs du type `Result`, comme celles de tout autre type, possèdent des méthodes. Une instance de `Result` possède une [méthode `expect`][expect]<!-- ignore --> que vous pouvez appeler. Si cette instance de `Result` contient une valeur `Err`, `expect` fait planter le programme et affiche le message que vous lui avez transmis en argument. Si la méthode `read_line` renvoie un `Err`, cela résulte probablement d’une erreur provenant du système d’exploitation sous-jacent. Si cette instance de `Result` contient une valeur `Ok`, `expect` récupère la valeur qu’elle contient et vous la renvoie directement pour que vous puissiez l’utiliser. Dans ce cas, cette valeur correspond au nombre d’octets de la saisie de l’utilisateur.

Si vous n’appelez pas `expect`, le programme compilera, mais vous obtiendrez un avertissement :

```console
{{#include ../listings/ch02-guessing-game-tutorial/no-listing-02-without-expect/output.txt}}
```

Rust signale que vous n’avez pas utilisé la valeur `Result` renvoyée par `read_line`, ce qui indique que le programme n’a pas géré une erreur potentielle.

La bonne façon de supprimer cet avertissement consiste à écrire du code qui gère les erreurs. Mais dans notre cas, nous voulons simplement faire planter le programme lorsqu’un problème survient, et nous pouvons donc utiliser `expect`. Vous apprendrez à récupérer des erreurs au [chapitre 9][recover]<!-- ignore -->.

### Afficher des valeurs avec les espaces réservés de `println!`

Hormis l’accolade fermante, il ne reste qu’une ligne à examiner dans le code actuel :

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-01/src/main.rs:print_guess}}
```

Cette ligne affiche la chaîne qui contient maintenant la saisie de l’utilisateur. Les accolades `{}` constituent un espace réservé : imaginez-les comme de petites pinces de crabe qui maintiennent une valeur en place. Pour afficher la valeur d’une variable, vous pouvez placer le nom de celle-ci entre les accolades. Pour afficher le résultat de l’évaluation d’une expression, placez des accolades vides dans la chaîne de format, puis faites suivre cette chaîne d’une liste d’expressions séparées par des virgules, qui seront affichées dans chaque espace réservé vide, dans le même ordre. Voici comment afficher une variable et le résultat d’une expression dans un même appel à `println!` :

```rust
let x = 5;
let y = 10;

println!("x = {x} and y + 2 = {}", y + 2);
```

Ce code afficherait `x = 5 and y + 2 = 12`.

### Tester la première partie

Testons la première partie du jeu de devinettes. Exécutez-la avec `cargo run` :

<!-- manual-regeneration
cd listings/ch02-guessing-game-tutorial/listing-02-01/
cargo clean
cargo run
input 6 -->

```console
$ cargo run
   Compiling guessing_game v0.1.0 (file:///projects/guessing_game)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 6.44s
     Running `target/debug/guessing_game`
Guess the number!
Please input your guess.
6
You guessed: 6
```

À ce stade, la première partie du jeu est terminée : nous récupérons la saisie au clavier, puis nous l’affichons.

## Générer un nombre secret

Ensuite, nous devons générer un nombre secret que l’utilisateur devra deviner. Ce nombre doit changer à chaque partie pour que le jeu reste amusant si l’on y joue plusieurs fois. Nous utiliserons un nombre aléatoire entre 1 et 100 afin que le jeu ne soit pas trop difficile. Rust ne propose pas encore de fonctionnalité de génération de nombres aléatoires dans sa bibliothèque standard. Cependant, l’équipe Rust fournit une crate [`rand`][randcrate] qui offre cette fonctionnalité.

<!-- Old headings. Do not remove or links may break. -->
<a id="using-a-crate-to-get-more-functionality"></a>

### Ajouter des fonctionnalités avec une crate

Rappelez-vous qu’une crate est un ensemble de fichiers de code source Rust. Le projet que nous avons créé est une crate binaire, c’est-à-dire un exécutable. La crate `rand` est une crate de bibliothèque : elle contient du code destiné à être utilisé dans d’autres programmes et ne peut pas être exécutée seule.

C’est dans la gestion des crates externes que Cargo révèle tout son potentiel. Avant de pouvoir écrire du code qui utilise `rand`, nous devons modifier le fichier _Cargo.toml_ pour ajouter la crate `rand` comme dépendance. Ouvrez ce fichier et ajoutez la ligne suivante à la fin de la section `[dependencies]` créée par Cargo. Veillez à spécifier `rand` exactement comme indiqué, avec ce numéro de version, sans quoi les exemples de code de ce tutoriel pourraient ne pas fonctionner :

<!-- When updating the version of `rand` used, also update the version of
`rand` used in these files so they all match:

* ch01-01-installation.md
* ch07-04-bringing-paths-into-scope-with-the-use-keyword.md
* ch14-03-cargo-workspaces.md
-->

<span class="filename">Nom du fichier : Cargo.toml</span>

```toml
{{#include ../listings/ch02-guessing-game-tutorial/listing-02-02/Cargo.toml:8:}}
```

Dans le fichier _Cargo.toml_, tout ce qui suit un en-tête fait partie de la section correspondante jusqu’au début d’une autre section. Dans `[dependencies]`, vous indiquez à Cargo de quelles crates externes votre projet dépend et quelles versions sont requises. Ici, nous spécifions la crate `rand` avec le spécificateur de version sémantique `0.10.1`. Cargo comprend le [versionnage sémantique][semver]<!-- ignore --> (parfois appelé _SemVer_), une norme d’écriture des numéros de version. Le spécificateur `0.10.1` est en réalité un raccourci pour `^0.10.1`, ce qui signifie toute version supérieure ou égale à 0.10.1, mais inférieure à 0.11.0.

Cargo considère que ces versions ont des API publiques compatibles avec la version 0.10.1. Cette spécification garantit que vous obtiendrez la dernière version corrective qui pourra toujours compiler le code de ce chapitre. Il n’est pas garanti que les versions 0.11.0 et ultérieures possèdent la même API que celle utilisée dans les exemples suivants.

Maintenant, sans modifier le code, compilons le projet comme indiqué dans la liste 2-2.

<!-- manual-regeneration
cd listings/ch02-guessing-game-tutorial/listing-02-02/
rm Cargo.lock
cargo clean
cargo build -->

<Listing number="2-2" caption="Sortie de la commande `cargo build` après l’ajout de la crate `rand` comme dépendance">

```console
$ cargo build
    Updating crates.io index
     Locking 8 packages to latest Rust 1.96.0 compatible versions
  Downloaded rand_core v0.10.1
  Downloaded chacha20 v0.10.1
  Downloaded rand v0.10.1
  Downloaded 3 crates (162.9KiB) in 0.59s
   Compiling libc v0.2.186
   Compiling rand_core v0.10.1
   Compiling getrandom v0.4.3
   Compiling cfg-if v1.0.4
   Compiling chacha20 v0.10.1
   Compiling rand v0.10.1
   Compiling guessing_game v0.1.0 (file:///projects/guessing_game)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 2.03s
```

</Listing>

Vous verrez peut-être des numéros de version différents (mais ils seront tous compatibles avec le code grâce à SemVer !), ainsi que des lignes différentes (selon le système d’exploitation), et celles-ci pourront apparaître dans un autre ordre.

Lorsque nous ajoutons une dépendance externe, Cargo récupère dans le _registre_ les dernières versions de tout ce dont cette dépendance a besoin. Ce registre est une copie des données de [Crates.io][cratesio]. Crates.io est le site où les membres de l’écosystème Rust publient leurs projets open source pour que d’autres puissent les utiliser.

Après avoir mis à jour le registre, Cargo vérifie la section `[dependencies]` et télécharge toutes les crates qui y sont listées et qui ne le sont pas déjà. Dans notre cas, bien que nous n’ayons indiqué que `rand` comme dépendance, Cargo a également récupéré d’autres crates dont `rand` a besoin pour fonctionner. Après avoir téléchargé les crates, Rust les compile, puis compile le projet avec les dépendances disponibles.

Si vous exécutez immédiatement `cargo build` à nouveau sans rien modifier, vous n’obtiendrez aucune sortie, à l’exception de la ligne `Finished`. Cargo sait qu’il a déjà téléchargé et compilé les dépendances et que vous n’avez rien modifié à leur sujet dans votre fichier _Cargo.toml_. Il sait également que vous n’avez pas modifié votre code, et ne le recompile donc pas. N’ayant rien à faire, il se termine simplement.

Si vous ouvrez le fichier _src/main.rs_, y apportez une modification mineure, puis l’enregistrez et relancez la compilation, vous ne verrez que deux lignes :

<!-- manual-regeneration
cd listings/ch02-guessing-game-tutorial/listing-02-02/
touch src/main.rs
cargo build -->

```console
$ cargo build
   Compiling guessing_game v0.1.0 (file:///projects/guessing_game)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.13s
```

Ces lignes montrent que Cargo ne met à jour la compilation qu’en fonction de votre petite modification du fichier _src/main.rs_. Vos dépendances n’ayant pas changé, Cargo sait qu’il peut réutiliser ce qu’il a déjà téléchargé et compilé pour elles.

<!-- Old headings. Do not remove or links may break. -->
<a id="ensuring-reproducible-builds-with-the-cargo-lock-file"></a>

#### Garantir des compilations reproductibles

Cargo dispose d’un mécanisme qui vous garantit, à vous comme à toute autre personne, de pouvoir reconstruire le même artefact à chaque compilation de votre code : Cargo n’utilisera que les versions des dépendances spécifiées, à moins que vous ne lui indiquiez le contraire. Supposons, par exemple, que la version 0.10.2 de la crate `rand` sorte la semaine prochaine et qu’elle contienne une importante correction de bogue, mais également une régression qui casse votre code. Pour gérer cela, Rust crée le fichier _Cargo.lock_ lors de la première exécution de `cargo build`. Ce fichier se trouve donc maintenant dans le répertoire _guessing_game_.

Lorsque vous compilez un projet pour la première fois, Cargo détermine toutes les versions des dépendances qui répondent aux critères, puis les inscrit dans le fichier _Cargo.lock_. Lorsque vous compilerez votre projet à l’avenir, Cargo constatera que le fichier _Cargo.lock_ existe et utilisera les versions qui y sont indiquées, au lieu de refaire tout le travail de recherche des versions. Cela vous permet d’obtenir automatiquement une compilation reproductible. Autrement dit, votre projet restera en version 0.10.1 jusqu’à ce que vous procédiez explicitement à une mise à jour, grâce au fichier _Cargo.lock_. Ce fichier étant important pour garantir des compilations reproductibles, il est souvent ajouté au contrôle de version avec le reste du code du projet.

#### Mettre à jour une crate pour obtenir une nouvelle version

Si vous souhaitez mettre à jour une crate, Cargo fournit la commande `update`, qui ignore le fichier _Cargo.lock_ et recherche toutes les dernières versions correspondant aux spécifications de _Cargo.toml_. Cargo inscrit ensuite ces versions dans le fichier _Cargo.lock_. Par défaut, Cargo ne recherche que les versions supérieures à 0.10.1 et inférieures à 0.11.0. Si deux nouvelles versions de la crate `rand`, 0.10.2 et 0.999.0, ont été publiées, voici ce que vous verriez en exécutant `cargo update` :

<!-- manual-regeneration
cd listings/ch02-guessing-game-tutorial/listing-02-02/
cargo update
assuming there is a new version of rand; otherwise use another update
as a guide to creating the hypothetical output shown here -->

```console
$ cargo update
    Updating crates.io index
     Locking 1 package to latest Rust 1.96.0 compatible version
    Updating rand v0.10.1 -> v0.10.2 (available: v0.999.0)
```

Cargo ignore la version 0.999.0. À ce stade, vous remarquerez également une modification dans votre fichier _Cargo.lock_, indiquant que la version de la crate `rand` que vous utilisez maintenant est 0.10.2. Pour utiliser la version 0.999.0 de `rand`, ou n’importe quelle version de la série 0.999._x_, vous devriez plutôt modifier le fichier _Cargo.toml_ comme suit (ne faites pas cette modification, car les exemples suivants supposent que vous utilisez `rand` 0.10) :

```toml
[dependencies]
rand = "0.999.0"
```

La prochaine fois que vous exécuterez `cargo build`, Cargo mettra à jour le registre des crates disponibles et réévaluera vos exigences concernant `rand` en fonction de la nouvelle version spécifiée.

Il y a beaucoup d’autres choses à dire sur [Cargo][doccargo]<!-- ignore --> et [son écosystème][doccratesio]<!-- ignore -->. Nous en parlerons au chapitre 14, mais pour l’instant, c’est tout ce que vous devez savoir. Cargo facilite grandement la réutilisation des bibliothèques, ce qui permet aux adeptes de Rust d’écrire de plus petits projets assemblés à partir de plusieurs paquets.

### Générer un nombre aléatoire

Commençons à utiliser `rand` pour générer un nombre à deviner. L’étape suivante consiste à mettre à jour _src/main.rs_, comme indiqué dans la liste 2-3.

<Listing number="2-3" file-name="src/main.rs" caption="Ajout de code pour générer un nombre aléatoire">

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-03/src/main.rs:all}}
```

</Listing>

Tout d’abord, nous ajoutons la ligne `use rand::prelude::*;`. Le module `prelude` contient les éléments les plus couramment utilisés de la crate `rand`, et `use` rend ces éléments disponibles dans la portée de notre programme.

Ensuite, nous ajoutons deux lignes au milieu. Sur la première, nous appelons la fonction `rand::rng`, qui nous fournit le générateur de nombres aléatoires que nous allons utiliser : un générateur local au thread d’exécution actuel et initialisé à l’aide du système d’exploitation. Ensuite, nous appelons la méthode `random_range` sur ce générateur. Cette méthode est définie par le trait `RngExt`, qui fait partie du module `rand::prelude` que nous avons importé dans la portée à l’aide de l’instruction `use rand::prelude::*;`. La méthode `random_range` prend une expression de plage en argument et génère un nombre aléatoire dans cette plage. Le type d’expression de plage que nous utilisons ici prend la forme `début..=fin` et inclut les deux bornes. Nous devons donc spécifier `1..=100` pour demander un nombre entre 1 et 100.

> Remarque : vous ne saurez pas forcément quels éléments importer dans la portée, ni quelles méthodes et fonctions appeler dans une crate. Chaque crate est donc accompagnée d’une documentation qui explique comment l’utiliser. Autre fonctionnalité pratique de Cargo : la commande `cargo doc --open` génère localement la documentation fournie par toutes vos dépendances, puis l’ouvre dans votre navigateur. Si vous souhaitez découvrir d’autres fonctionnalités de la crate `rand`, par exemple, exécutez `cargo doc --open` et cliquez sur `rand` dans la barre latérale gauche.

La deuxième nouvelle ligne affiche le nombre secret. C’est utile pendant le développement du programme pour pouvoir le tester, mais nous supprimerons cette ligne dans la version finale. Ce n’est pas vraiment un jeu si le programme affiche la réponse dès son lancement !

Essayez d’exécuter le programme plusieurs fois :

<!-- manual-regeneration
cd listings/ch02-guessing-game-tutorial/listing-02-03/
cargo run
4
cargo run
5
-->

```console
$ cargo run
   Compiling guessing_game v0.1.0 (file:///projects/guessing_game)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.02s
     Running `target/debug/guessing_game`
Guess the number!
The secret number is: 7
Please input your guess.
4
You guessed: 4

$ cargo run
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.02s
     Running `target/debug/guessing_game`
Guess the number!
The secret number is: 83
Please input your guess.
5
You guessed: 5
```

Vous devriez obtenir des nombres aléatoires différents, tous compris entre 1 et 100. Si vous obtenez des avertissements, vous pouvez les ignorer sans risque. Si vous obtenez des erreurs, vérifiez que vous avez bien `rand = "0.10.1"` dans votre *Cargo.toml* : les versions futures de `rand` pourraient avoir une API différente, mais toute version de la série `0.10` devrait fonctionner avec le code de ce chapitre.

## Comparer la proposition au nombre secret

Maintenant que nous avons une saisie de l’utilisateur et un nombre aléatoire, nous pouvons les comparer. Cette étape est illustrée dans la liste 2-4. Notez que ce code ne compilera pas encore, comme nous allons l’expliquer.

<Listing number="2-4" file-name="src/main.rs" caption="Gestion des valeurs de retour possibles lors de la comparaison de deux nombres">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-04/src/main.rs:here}}
```

</Listing>

Tout d’abord, nous ajoutons une autre instruction `use`, qui importe dans la portée le type `std::cmp::Ordering` de la bibliothèque standard. Le type `Ordering` est une autre enum qui possède les variantes `Less`, `Greater` et `Equal`. Ce sont les trois résultats possibles de la comparaison de deux valeurs.

Ensuite, nous ajoutons cinq nouvelles lignes à la fin, qui utilisent le type `Ordering`. La méthode `cmp` compare deux valeurs et peut être appelée sur toute valeur comparable. Elle prend une référence vers la valeur à laquelle vous souhaitez comparer la première : ici, elle compare `guess` à `secret_number`. Elle renvoie ensuite une variante de l’enum `Ordering`, que nous avons importée dans la portée avec l’instruction `use`. Nous utilisons une expression [`match`][match]<!-- ignore --> pour décider de la suite en fonction de la variante de `Ordering` renvoyée par l’appel à `cmp` avec les valeurs `guess` et `secret_number`.

Une expression `match` est composée de _bras_. Un bras se compose d’un _motif_ à comparer et du code à exécuter si la valeur fournie à `match` correspond à ce motif. Rust prend la valeur fournie à `match` et examine les motifs de chaque bras l’un après l’autre. Les motifs et la construction `match` sont des fonctionnalités puissantes de Rust : elles permettent d’exprimer diverses situations que votre code peut rencontrer et garantissent que vous les gérez toutes. Ces fonctionnalités seront étudiées en détail respectivement aux chapitres 6 et 19.

Examinons un exemple avec l’expression `match` utilisée ici. Supposons que l’utilisateur ait proposé 50 et que le nombre secret généré aléatoirement soit 38.

Lorsque le code compare 50 à 38, la méthode `cmp` renvoie `Ordering::Greater`, car 50 est supérieur à 38. L’expression `match` reçoit la valeur `Ordering::Greater` et commence à examiner le motif de chaque bras. Elle examine le motif du premier bras, `Ordering::Less`, constate que la valeur `Ordering::Greater` ne correspond pas à `Ordering::Less`, ignore donc le code de ce bras et passe au suivant. Le motif du bras suivant est `Ordering::Greater`, qui correspond bien à `Ordering::Greater` ! Le code associé à ce bras s’exécute et affiche `Too big!` à l’écran. L’expression `match` se termine après la première correspondance : dans ce cas, elle n’examinera donc pas le dernier bras.

Cependant, le code de la liste 2-4 ne compilera pas encore. Essayons :

<!--
The error numbers in this output should be that of the code **WITHOUT** the
anchor or snip comments
-->

```console
{{#include ../listings/ch02-guessing-game-tutorial/listing-02-04/output.txt}}
```

Le cœur du message d’erreur indique qu’il y a des _types incompatibles_. Rust possède un système de types statique et strict. Il dispose toutefois aussi de l’inférence de types. Lorsque nous avons écrit `let mut guess = String::new()`, Rust a pu déduire que `guess` devait être une `String` sans nous obliger à écrire le type. En revanche, `secret_number` est un type numérique. Plusieurs types numériques de Rust peuvent représenter une valeur comprise entre 1 et 100 : `i32`, un nombre sur 32 bits ; `u32`, un nombre non signé sur 32 bits ; `i64`, un nombre sur 64 bits ; ainsi que d’autres. Sauf indication contraire, Rust utilise `i32` par défaut : `secret_number` est donc de ce type, à moins que d’autres informations de type n’amènent Rust à inférer un type numérique différent. L’erreur est due au fait que Rust ne peut pas comparer une chaîne et un type numérique.

En définitive, nous voulons convertir la `String` que le programme lit en entrée en un type numérique, afin de pouvoir la comparer numériquement au nombre secret. Pour cela, nous ajoutons cette ligne au corps de la fonction `main` :

<span class="filename">Nom du fichier : src/main.rs</span>

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/no-listing-03-convert-string-to-number/src/main.rs:here}}
```

Voici la ligne :

```rust,ignore
let guess: u32 = guess.trim().parse().expect("Please type a number!");
```

Nous créons une variable nommée `guess`. Mais attendez : le programme possède déjà une variable nommée `guess`, non ? C’est vrai, mais Rust nous permet heureusement de masquer la valeur précédente de `guess` par une nouvelle. Le _masquage_ nous permet de réutiliser le nom de variable `guess` plutôt que de devoir créer deux variables distinctes, comme `guess_str` et `guess`, par exemple. Nous étudierons cela plus en détail au [chapitre 3][shadowing]<!-- ignore -->, mais pour l’instant, sachez que cette fonctionnalité est souvent utilisée pour convertir une valeur d’un type en un autre.

Nous associons cette nouvelle variable à l’expression `guess.trim().parse()`. Dans cette expression, `guess` fait référence à la variable `guess` d’origine, qui contenait la saisie sous forme de chaîne. La méthode `trim` d’une instance de `String` élimine les espaces blancs au début et à la fin. Cette opération est nécessaire avant de convertir la chaîne en `u32`, qui ne peut contenir que des données numériques. L’utilisateur doit appuyer sur <kbd>enter</kbd> pour satisfaire `read_line` et saisir sa proposition, ce qui ajoute un caractère de nouvelle ligne à la chaîne. Par exemple, si l’utilisateur saisit <kbd>5</kbd> et appuie sur <kbd>enter</kbd>, `guess` ressemble à ceci : `5\n`. `\n` représente une « nouvelle ligne ». (Sous Windows, appuyer sur <kbd>enter</kbd> produit un retour chariot et une nouvelle ligne : `\r\n`.) La méthode `trim` élimine `\n` ou `\r\n`, ce qui ne laisse que `5`.

La [méthode `parse` des chaînes][parse]<!-- ignore --> convertit une chaîne en un autre type. Ici, nous l’utilisons pour convertir une chaîne en nombre. Nous devons indiquer à Rust le type numérique exact que nous voulons en écrivant `let guess: u32`. Les deux-points (`:`) après `guess` indiquent à Rust que nous allons préciser le type de la variable. Rust possède plusieurs types numériques intégrés ; le `u32` utilisé ici est un entier non signé sur 32 bits. C’est un bon choix par défaut pour un petit nombre positif. Vous découvrirez d’autres types numériques au [chapitre 3][integers]<!-- ignore -->.

De plus, l’annotation `u32` de cet exemple et la comparaison avec `secret_number` signifient que Rust déduira également que `secret_number` doit être de type `u32`. La comparaison portera donc maintenant sur deux valeurs du même type !

La méthode `parse` ne fonctionne que sur les caractères qui peuvent logiquement être convertis en nombres et peut donc facilement provoquer des erreurs. Si, par exemple, la chaîne contenait `A👍%`, il serait impossible de la convertir en nombre. Comme cette conversion peut échouer, la méthode `parse` renvoie un type `Result`, tout comme la méthode `read_line` (évoquée précédemment dans la section [« Gérer les échecs potentiels avec `Result` »](#handling-potential-failure-with-result)<!-- ignore -->). Nous traiterons ce `Result` de la même manière, en utilisant à nouveau la méthode `expect`. Si `parse` renvoie une variante `Err` de `Result` parce qu’elle n’a pas pu créer un nombre à partir de la chaîne, l’appel à `expect` fera planter le jeu et affichera le message que nous lui fournissons. Si `parse` parvient à convertir la chaîne en nombre, elle renverra la variante `Ok` de `Result`, et `expect` renverra le nombre que nous voulons récupérer dans la valeur `Ok`.

Exécutons maintenant le programme :

<!-- manual-regeneration
cd listings/ch02-guessing-game-tutorial/no-listing-03-convert-string-to-number/
touch src/main.rs
cargo run
  76
-->

```console
$ cargo run
   Compiling guessing_game v0.1.0 (file:///projects/guessing_game)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.26s
     Running `target/debug/guessing_game`
Guess the number!
The secret number is: 58
Please input your guess.
  76
You guessed: 76
Too big!
```

Parfait ! Même si des espaces ont été ajoutés avant la proposition, le programme a tout de même compris que l’utilisateur avait proposé 76. Exécutez le programme plusieurs fois pour vérifier son comportement selon différents types de saisie : trouvez le bon nombre, proposez un nombre trop élevé, puis un nombre trop faible.

Le jeu est presque entièrement fonctionnel, mais l’utilisateur ne peut faire qu’une seule proposition. Ajoutons une boucle pour remédier à cela !

## Autoriser plusieurs propositions à l’aide de boucles

Le mot-clé `loop` crée une boucle infinie. Nous allons ajouter une boucle pour donner aux utilisateurs plusieurs chances de deviner le nombre :

<span class="filename">Nom du fichier : src/main.rs</span>

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/no-listing-04-looping/src/main.rs:here}}
```

Comme vous pouvez le voir, nous avons placé dans une boucle tout ce qui se trouvait à partir de l’invite de saisie de la proposition. Veillez à indenter les lignes de la boucle de quatre espaces supplémentaires, puis réexécutez le programme. Il demandera désormais sans cesse une nouvelle proposition, ce qui introduit un nouveau problème : on ne dirait pas que l’utilisateur puisse quitter le jeu !

L’utilisateur peut toujours interrompre le programme à l’aide du raccourci clavier <kbd>ctrl</kbd>-<kbd>C</kbd>. Mais il existe un autre moyen d’échapper à ce monstre insatiable, comme nous l’avons mentionné lors de la discussion sur `parse` dans la section [« Comparer la proposition au nombre secret »](#comparing-the-guess-to-the-secret-number)<!-- ignore --> : si l’utilisateur saisit une réponse qui n’est pas un nombre, le programme plantera. Nous pouvons tirer parti de ce comportement pour permettre à l’utilisateur de quitter le jeu, comme illustré ici :

<!-- manual-regeneration
cd listings/ch02-guessing-game-tutorial/no-listing-04-looping/
touch src/main.rs
cargo run
(too small guess)
(too big guess)
(correct guess)
quit
-->

```console
$ cargo run
   Compiling guessing_game v0.1.0 (file:///projects/guessing_game)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.23s
     Running `target/debug/guessing_game`
Guess the number!
The secret number is: 59
Please input your guess.
45
You guessed: 45
Too small!
Please input your guess.
60
You guessed: 60
Too big!
Please input your guess.
59
You guessed: 59
You win!
Please input your guess.
quit

thread 'main' (6694925) panicked at src/main.rs:28:47:
Please type a number!: ParseIntError { kind: InvalidDigit }
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
```

Saisir `quit` termine le jeu, mais, comme vous le remarquerez, toute autre saisie qui n’est pas un nombre le fera aussi. C’est loin d’être idéal ; nous voulons également que le jeu s’arrête lorsque le bon nombre est trouvé.

### Quitter après une bonne réponse

Programmons le jeu pour qu’il se termine lorsque l’utilisateur gagne en ajoutant une instruction `break` :

<span class="filename">Nom du fichier : src/main.rs</span>

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/no-listing-05-quitting/src/main.rs:here}}
```

En ajoutant la ligne `break` après `You win!`, le programme quitte la boucle lorsque l’utilisateur trouve le nombre secret. Quitter la boucle signifie également quitter le programme, car la boucle constitue la dernière partie de `main`.

### Gérer les saisies non valides

Pour améliorer encore le comportement du jeu, faisons en sorte qu’il ignore les saisies qui ne sont pas des nombres, au lieu de faire planter le programme, afin que l’utilisateur puisse continuer à proposer des nombres. Nous pouvons le faire en modifiant la ligne où `guess` est converti d’une `String` en `u32`, comme indiqué dans la liste 2-5.

<Listing number="2-5" file-name="src/main.rs" caption="Ignorer une proposition qui n’est pas un nombre et en demander une autre au lieu de faire planter le programme">

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-05/src/main.rs:here}}
```

</Listing>

Nous remplaçons l’appel à `expect` par une expression `match` pour gérer l’erreur au lieu de faire planter le programme. Rappelez-vous que `parse` renvoie un type `Result`, qui est une enum possédant les variantes `Ok` et `Err`. Nous utilisons ici une expression `match`, comme nous l’avons fait avec le résultat `Ordering` de la méthode `cmp`.

Si `parse` parvient à convertir la chaîne en nombre, elle renvoie une valeur `Ok` qui contient le nombre obtenu. Cette valeur `Ok` correspond au motif du premier bras, et l’expression `match` renvoie simplement la valeur `num` produite par `parse` et placée dans la valeur `Ok`. Ce nombre se retrouvera à l’endroit voulu, dans la nouvelle variable `guess` que nous sommes en train de créer.

Si `parse` ne parvient pas à convertir la chaîne en nombre, elle renvoie une valeur `Err` qui contient des informations supplémentaires sur l’erreur. La valeur `Err` ne correspond pas au motif `Ok(num)` du premier bras de `match`, mais elle correspond au motif `Err(_)` du deuxième bras. Le caractère de soulignement `_` est une valeur fourre-tout : ici, nous indiquons que nous voulons correspondre à toutes les valeurs `Err`, quelles que soient les informations qu’elles contiennent. Le programme exécute donc le code du deuxième bras, `continue`, qui lui indique de passer à l’itération suivante de la boucle et de demander une autre proposition. En pratique, le programme ignore donc toutes les erreurs que `parse` pourrait rencontrer !

Tout devrait maintenant fonctionner comme prévu. Essayons :

<!-- manual-regeneration
cd listings/ch02-guessing-game-tutorial/listing-02-05/
cargo run
(too small guess)
(too big guess)
foo
(correct guess)
-->

```console
$ cargo run
   Compiling guessing_game v0.1.0 (file:///projects/guessing_game)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.13s
     Running `target/debug/guessing_game`
Guess the number!
The secret number is: 61
Please input your guess.
10
You guessed: 10
Too small!
Please input your guess.
99
You guessed: 99
Too big!
Please input your guess.
foo
Please input your guess.
61
You guessed: 61
You win!
```

Excellent ! Avec un tout petit dernier ajustement, nous allons terminer le jeu de devinettes. Rappelez-vous que le programme affiche encore le nombre secret. C’était utile pour les tests, mais cela gâche le jeu. Supprimons le `println!` qui affiche le nombre secret. La liste 2-6 présente le code final.

<Listing number="2-6" file-name="src/main.rs" caption="Code complet du jeu de devinettes">

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-06/src/main.rs}}
```

</Listing>

Vous avez maintenant créé avec succès le jeu de devinettes. Félicitations !

## Résumé

Ce projet vous a permis de découvrir de nombreux nouveaux concepts de Rust en les mettant en pratique : `let`, `match`, les fonctions, l’utilisation de crates externes et bien plus encore. Au cours des prochains chapitres, vous étudierez ces concepts plus en détail. Le chapitre 3 traite de concepts présents dans la plupart des langages de programmation, comme les variables, les types de données et les fonctions, et explique comment les utiliser en Rust. Le chapitre 4 explore la propriété, une fonctionnalité qui distingue Rust des autres langages. Le chapitre 5 aborde les structs et la syntaxe des méthodes, et le chapitre 6 explique le fonctionnement des enums.

[prelude]: ../std/prelude/index.html
[variables-and-mutability]: ch03-01-variables-and-mutability.html#variables-and-mutability
[comments]: ch03-04-comments.html
[string]: ../std/string/struct.String.html
[iostdin]: ../std/io/struct.Stdin.html
[read_line]: ../std/io/struct.Stdin.html#method.read_line
[result]: ../std/result/enum.Result.html
[enums]: ch06-00-enums.html
[expect]: ../std/result/enum.Result.html#method.expect
[recover]: ch09-02-recoverable-errors-with-result.html
[randcrate]: https://crates.io/crates/rand
[semver]: http://semver.org
[cratesio]: https://crates.io/
[doccargo]: https://doc.rust-lang.org/cargo/
[doccratesio]: https://doc.rust-lang.org/cargo/reference/publishing.html
[match]: ch06-02-match.html
[shadowing]: ch03-01-variables-and-mutability.html#shadowing
[parse]: ../std/primitive.str.html#method.parse
[integers]: ch03-02-data-types.html#integer-types