# Programmer un Jeu de Devinette

Plongeons dans Rust en travaillant ensemble sur un projet pratique ! Ce chapitre vous présente quelques concepts courants de Rust en vous montrant comment les utiliser dans un programme réel. Vous découvrirez `let`, `match`, les méthodes, les fonctions associées, les crates externes, et plus encore ! Dans les chapitres suivants, nous explorerons ces idées plus en détail. Dans ce chapitre, vous allez simplement pratiquer les fondamentaux.

Nous allons mettre en œuvre un problème classique de programmation pour débutants : un jeu de devinette. Voici comment cela fonctionne : le programme générera un entier aléatoire entre 1 et 100. Il demandera ensuite au joueur d'entrer une devinette. Après qu'une devinette a été saisie, le programme indiquera si la devinette est trop basse ou trop élevée. Si la devinette est correcte, le jeu affichera un message de félicitations et se terminera.

## Configuration d'un Nouveau Projet

Pour configurer un nouveau projet, allez dans le répertoire _projects_ que vous avez créé au Chapitre 1 et créez un nouveau projet en utilisant Cargo, comme ceci :

```console
$ cargo new guessing_game
$ cd guessing_game
```

La première commande, `cargo new`, prend le nom du projet (`guessing_game`) comme premier argument. La deuxième commande change de répertoire vers le nouveau projet.

Regardez le fichier _Cargo.toml_ généré :

<span class="filename">Nom du fichier : Cargo.toml</span>

```toml
{{#include ../listings/ch02-guessing-game-tutorial/no-listing-01-cargo-new/Cargo.toml}}
```

Comme vous l'avez vu au Chapitre 1, `cargo new` génère pour vous un programme « Hello, World ! ». Consultez le fichier _src/main.rs_ :

<span class="filename">Nom du fichier : src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/no-listing-01-cargo-new/src/main.rs}}
```

Maintenant, compilons ce programme « Hello, World ! » et exécutons-le dans la même étape en utilisant la commande `cargo run` :

```console
{{#include ../listings/ch02-guessing-game-tutorial/no-listing-01-cargo-new/output.txt}}
```

La commande `run` est utile lorsque vous devez itérer rapidement sur un projet, comme nous le ferons dans ce jeu, en testant rapidement chaque itération avant de passer à la suivante.

Rouvrez le fichier _src/main.rs_. Vous allez écrire tout le code dans ce fichier.

## Traitement d'une Devinette

La première partie du programme de jeu de devinette demandera une entrée utilisateur, traitera cette entrée et vérifiera que l'entrée est dans le format attendu. Pour commencer, nous allons permettre au joueur de saisir une devinette. Entrez le code dans la Liste 2-1 dans _src/main.rs_.

<Listing number="2-1" file-name="src/main.rs" caption="Code qui obtient une devinette de l'utilisateur et l'affiche">

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-01/src/main.rs:all}}
```

</Listing>

Ce code contient beaucoup d'informations, alors examinons-le ligne par ligne. Pour obtenir une entrée utilisateur puis afficher le résultat en sortie, nous devons importer la bibliothèque d'entrée/sortie `io`. La bibliothèque `io` provient de la bibliothèque standard, appelée `std` :

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-01/src/main.rs:io}}
```

Par défaut, Rust dispose d'un ensemble d'éléments définis dans la bibliothèque standard qu'il met dans le contexte de chaque programme. Cet ensemble s'appelle le _préambule_, et vous pouvez voir tout ce qu'il contient [dans la documentation de la bibliothèque standard][prelude].

Si un type que vous souhaitez utiliser n'est pas dans le préambule, vous devez apporter ce type dans le contexte explicitement avec une déclaration `use`. L'utilisation de la bibliothèque `std::io` vous offre plusieurs fonctionnalités utiles, y compris la capacité d'accepter une entrée utilisateur.

Comme vous l'avez vu dans le Chapitre 1, la fonction `main` est le point d'entrée dans le programme :

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-01/src/main.rs:main}}
```

La syntaxe `fn` déclare une nouvelle fonction ; les parenthèses, `()`, indiquent qu'il n'y a pas de paramètres ; et l'accolade ouvrante, `{`, commence le corps de la fonction.

Comme vous l'avez également appris au Chapitre 1, `println!` est une macro qui imprime une chaîne à l'écran :

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-01/src/main.rs:print}}
```

Ce code affiche une invite indiquant de quoi il s'agit dans le jeu et demande une entrée à l'utilisateur.

### Stockage de Valeurs avec des Variables

Ensuite, nous allons créer une _variable_ pour stocker l'entrée utilisateur, comme ceci :

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-01/src/main.rs:string}}
```

Maintenant, le programme devient intéressant ! Il se passe beaucoup de choses dans cette petite ligne. Nous utilisons l'instruction `let` pour créer la variable. Voici un autre exemple :

```rust,ignore
let apples = 5;
```

Cette ligne crée une nouvelle variable nommée `apples` et l'associe à la valeur `5`. En Rust, les variables sont immuables par défaut, ce qui signifie qu'une fois que nous attribuons une valeur à la variable, celle-ci ne changera pas. Nous aborderons ce concept en détail dans la section [« Variables et Immutabilité »][variables-and-mutability]<!-- ignore --> du Chapitre 3. Pour rendre une variable mutable, nous ajoutons `mut` avant le nom de la variable :

```rust,ignore
let apples = 5; // immuable
let mut bananas = 5; // mutable
```

> Remarque : La syntaxe `//` commence un commentaire qui se poursuit jusqu'à la fin de la ligne. Rust ignore tout ce qui se trouve dans les commentaires. Nous allons discuter des commentaires plus en détail dans [le Chapitre 3][comments]<!-- ignore -->.

Revenant au programme de jeu de devinette, vous savez maintenant que `let mut guess` introduira une variable mutable nommée `guess`. Le signe égal (`=`) dit à Rust que nous voulons lier quelque chose à la variable maintenant. À droite du signe égal se trouve la valeur à laquelle `guess` est lié, qui est le résultat de l'appel à `String::new`, une fonction qui retourne une nouvelle instance d'une `String`. [`String`][string]<!-- ignore --> est un type de chaîne fourni par la bibliothèque standard qui est un morceau de texte mutable, encodé en UTF-8.

La syntaxe `::` dans la ligne `::new` indique que `new` est une fonction associée du type `String`. Une _fonction associée_ est une fonction qui est implémentée sur un type, dans ce cas `String`. Cette fonction `new` crée une nouvelle chaîne vide. Vous trouverez une fonction `new` sur de nombreux types car c'est un nom courant pour une fonction qui crée une nouvelle valeur d'un certain type.

Pour faire court, la ligne `let mut guess = String::new();` a créé une variable mutable qui est actuellement associée à une nouvelle instance vide d'une `String`. Ouf !

### Réception de l'Entrée Utilisateur

Rappelez-vous que nous avons inclus la fonctionnalité d'entrée/sortie de la bibliothèque standard avec `use std::io;` au début du programme. Maintenant, nous allons appeler la fonction `stdin` du module `io`, qui nous permettra de gérer l'entrée utilisateur :

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-01/src/main.rs:read}}
```

Si nous n'avions pas importé le module `io` avec `use std::io;` au début du programme, nous pourrions toujours utiliser la fonction en écrivant cet appel de fonction sous la forme `std::io::stdin`. La fonction `stdin` retourne une instance de [`std::io::Stdin`][iostdin]<!-- ignore -->, qui est un type représentant un accès à l'entrée standard de votre terminal.

Ensuite, la ligne `.read_line(&mut guess)` appelle la méthode [`read_line`][read_line]<!-- ignore --> sur l'accès à l'entrée standard pour obtenir une entrée de l'utilisateur. Nous passons également `&mut guess` comme argument à `read_line` pour indiquer dans quelle chaîne stocker l'entrée utilisateur. La tâche complète de `read_line` est de prendre tout ce que l'utilisateur tape dans l'entrée standard et de l'ajouter à une chaîne (sans écraser son contenu), donc nous passons cette chaîne comme argument. L'argument de chaîne doit être mutable afin que la méthode puisse changer le contenu de la chaîne.

Le `&` indique que cet argument est une _référence_, ce qui vous donne un moyen de laisser plusieurs parties de votre code accéder à une même donnée sans avoir besoin de copier cette donnée en mémoire plusieurs fois. Les références sont une fonctionnalité complexe, et l'un des principaux avantages de Rust est la sécurité et la facilité d'utilisation des références. Vous n'avez pas besoin de connaître beaucoup de détails là-dessus pour terminer ce programme. Pour l'instant, tout ce que vous devez savoir, c'est que, comme les variables, les références sont immuables par défaut. Donc, vous devez écrire `&mut guess` plutôt que `&guess` pour le rendre mutable. (Le Chapitre 4 expliquera les références plus en détail.)

### Gestion de la Potentielle Échec avec le Type `Result`

Nous travaillons toujours sur cette ligne de code. Nous parlons maintenant d'une troisième ligne de texte, mais notez qu'il s'agit toujours d'une seule ligne logique de code. La prochaine partie est cette méthode :

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-01/src/main.rs:expect}}
```

Nous aurions pu écrire ce code comme suit :

```rust,ignore
io::stdin().read_line(&mut guess).expect("Échec de la lecture de la ligne");
```

Cependant, une longue ligne est difficile à lire, donc il est préférable de la diviser. Il est souvent judicieux d'introduire une nouvelle ligne et d'autres espaces pour aider à séparer les lignes longues lorsque vous appelez une méthode avec la syntaxe `.method_name()`. Maintenant, discutons de ce que cette ligne fait.

Comme mentionné précédemment, `read_line` met ce que l'utilisateur entre dans la chaîne que nous lui passons, mais il retourne également une valeur `Result`. [`Result`][result]<!-- ignore --> est une [_énumération_][enums]<!-- ignore -->, souvent appelée _enum_, qui est un type qui peut être dans l'un de plusieurs états possibles. Nous appelons chaque état possible un _variant_.

Le Chapitre 6 abordera les enums en détail. Le but de ces types `Result` est d'encoder des informations sur la gestion des erreurs.

Les variantes de `Result` sont `Ok` et `Err`. La variante `Ok` indique que l'opération a réussi et contient la valeur générée avec succès. La variante `Err` signifie que l'opération a échoué et contient des informations sur la manière dont ou pourquoi l'opération a échoué.

Les valeurs de type `Result`, comme les valeurs de n'importe quel type, ont des méthodes définies sur elles. Une instance de `Result` a une méthode [`expect`][expect]<!-- ignore --> que vous pouvez appeler. Si cette instance de `Result` est une valeur `Err`, `expect` fera planter le programme et affichera le message que vous avez transmis en argument à `expect`. Si la méthode `read_line` retourne une `Err`, cela pourrait probablement être le résultat d'une erreur venant du système d'exploitation sous-jacent. Si cette instance de `Result` est une valeur `Ok`, `expect` prendra la valeur de retour que `Ok` contient et vous renverra juste cette valeur pour que vous puissiez l'utiliser. Dans ce cas, cette valeur est le nombre d'octets dans l'entrée de l'utilisateur.

Si vous n'appelez pas `expect`, le programme se compilera, mais vous obtiendrez un avertissement :

```console
{{#include ../listings/ch02-guessing-game-tutorial/no-listing-02-without-expect/output.txt}}
```

Rust prévient que vous n'avez pas utilisé la valeur `Result` retournée par `read_line`, indiquant que le programme n'a pas géré une possible erreur.

La bonne manière de supprimer l'avertissement est d'écrire réellement du code de gestion des erreurs, mais dans notre cas, nous voulons simplement faire planter ce programme lorsqu'un problème survient, donc nous pouvons utiliser `expect`. Vous apprendrez à récupérer des erreurs dans [le Chapitre 9][recover]<!-- ignore -->.

### Impression des Valeurs avec les Espaces réservés de `println!`

À part l'accolade fermante, il y a encore une ligne à discuter dans le code jusqu'à présent :

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-01/src/main.rs:print_guess}}
```

Cette ligne imprime la chaîne qui contient maintenant l'entrée de l'utilisateur. L'ensemble d'accolades `{}` est un espace réservé : Pensez à `{}` comme à de petites pinces de crabe qui tiennent une valeur en place. Lors de l'impression de la valeur d'une variable, le nom de la variable peut aller à l'intérieur des accolades. Lors de l'impression du résultat de l'évaluation d'une expression, placez des accolades vides dans la chaîne de format, puis suivez la chaîne de format avec une liste d'expressions séparées par des virgules à imprimer dans chaque espace réservé en accolades vide dans le même ordre. Imprimer une variable et le résultat d'une expression dans un seul appel à `println!` ressemblerait à ceci :

```rust
let x = 5;
let y = 10;

println!("x = {x} et y + 2 = {}", y + 2);
```

Ce code afficherait `x = 5 et y + 2 = 12`.

### Test de la Première Partie

Testons la première partie du jeu de devinette. Exécutez-le en utilisant `cargo run` :

```console
$ cargo run
   Compiling guessing_game v0.1.0 (file:///projects/guessing_game)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 6.44s
     Running `target/debug/guessing_game`
Devinez le nombre !
Veuillez saisir votre devinette.
6
Vous avez deviné : 6
```

À ce stade, la première partie du jeu est terminée : nous obtenons une entrée du clavier et l'affichons.

## Génération d'un Nombre Secret

Ensuite, nous devons générer un nombre secret que l'utilisateur essaiera de deviner. Le nombre secret doit être différent à chaque fois pour que le jeu soit amusant à jouer plus d'une fois. Nous utiliserons un nombre aléatoire entre 1 et 100 afin que le jeu ne soit pas trop difficile. Rust n'inclut pas encore la fonctionnalité de génération de nombres aléatoires dans sa bibliothèque standard. Cependant, l'équipe Rust fournit une crate [`rand`][randcrate] avec cette fonctionnalité.

### Augmenter la Fonctionnalité avec une Crate

Rappelez-vous qu'une crate est une collection de fichiers source Rust. Le projet que nous avons construit est une crate binaire, qui est exécutable. La crate `rand` est une crate de bibliothèque, qui contient du code destiné à être utilisé dans d'autres programmes et ne peut pas être exécutée seule.

La coordination des crates externes par Cargo est là où Cargo brille vraiment. Avant de pouvoir écrire du code qui utilise `rand`, nous devons modifier le fichier _Cargo.toml_ pour inclure la crate `rand` comme dépendance. Ouvrez ce fichier maintenant et ajoutez la ligne suivante en bas, sous l'en-tête `[dependencies]` que Cargo a créé pour vous. Assurez-vous de spécifier `rand` exactement comme nous l'avons ici, avec ce numéro de version, sinon les exemples de code de ce tutoriel peuvent ne pas fonctionner :

<span class="filename">Nom du fichier : Cargo.toml</span>

```toml
{{#include ../listings/ch02-guessing-game-tutorial/listing-02-02/Cargo.toml:8:}}
```

Dans le fichier _Cargo.toml_, tout ce qui suit un en-tête fait partie de cette section qui se poursuit jusqu'à ce qu'un autre en-tête commence. Dans `[dependencies]`, vous dites à Cargo quelles crates externes votre projet nécessite et quelles versions de ces crates vous exigez. Dans ce cas, nous spécifions la crate `rand` avec le spécificateur de version sémantique `0.8.5`. Cargo comprend [la version sémantique][semver]<!-- ignore --> (parfois appelée _SemVer_), qui est une norme pour la rédaction de numéros de version. Le spécificateur `0.8.5` est en réalité une abréviation de `^0.8.5`, ce qui signifie toute version qui est au moins 0.8.5 mais inférieure à 0.9.0.

Cargo considère que ces versions ont des API publiques compatibles avec la version 0.8.5, et cette spécification garantit que vous obtiendrez la dernière version de correctif qui se compilera avec le code de ce chapitre. Toute version 0.9.0 ou supérieure n'est pas garantie d'avoir la même API que ce que les exemples suivants utilisent.

Maintenant, sans changer de code, construisons le projet, comme montré dans la Liste 2-2.

<Listing number="2-2" caption="La sortie de l'exécution de `cargo build` après avoir ajouté la crate `rand` comme dépendance">

```console
$ cargo build
  Updating crates.io index
   Locking 15 packages to latest Rust 1.85.0 compatible versions
    Adding rand v0.8.5 (available: v0.9.0)
 Compiling proc-macro2 v1.0.93
 Compiling unicode-ident v1.0.17
 Compiling libc v0.2.170
 Compiling cfg-if v1.0.0
 Compiling byteorder v1.5.0
 Compiling getrandom v0.2.15
 Compiling rand_core v0.6.4
 Compiling quote v1.0.38
 Compiling syn v2.0.98
 Compiling zerocopy-derive v0.7.35
 Compiling zerocopy v0.7.35
 Compiling ppv-lite86 v0.2.20
 Compiling rand_chacha v0.3.1
 Compiling rand v0.8.5
 Compiling guessing_game v0.1.0 (file:///projects/guessing_game)
  Finished `dev` profile [unoptimized + debuginfo] target(s) in 2.48s
```
</Listing>

Vous pourriez voir des numéros de version différents (mais ils seront tous compatibles avec le code, grâce à SemVer !) et des lignes différentes (en fonction du système d'exploitation), et les lignes peuvent être dans un ordre différent.

Lorsque nous incluons une dépendance externe, Cargo télécharge les dernières versions de tout ce dont cette dépendance a besoin à partir du _registre_, qui est une copie des données de [Crates.io][cratesio]. Crates.io est l'endroit où les personnes de l'écosystème Rust publient leurs projets Rust open source pour que d'autres puissent les utiliser.

Après la mise à jour du registre, Cargo vérifie la section `[dependencies]` et télécharge toutes les crates listées qui ne sont pas déjà téléchargées. Dans ce cas, bien que nous n'ayons listé que `rand` comme dépendance, Cargo a également téléchargé d'autres crates dont `rand` dépend pour fonctionner. Après avoir téléchargé les crates, Rust les compile, puis compile le projet avec les dépendances disponibles.

Si vous exécutez immédiatement `cargo build` à nouveau sans apporter de modifications, vous ne verrez aucune sortie à part la ligne `Finished`. Cargo sait qu'il a déjà téléchargé et compilé les dépendances, et vous n'avez rien changé à leur sujet dans votre fichier _Cargo.toml_. Cargo sait également que vous n'avez rien modifié dans votre code, donc il ne le recompilera pas non plus. Avec rien à faire, il se termine simplement.

Si vous ouvrez le fichier _src/main.rs_, effectuez un changement trivial, puis sauvegardez-le et construisez à nouveau, vous ne verrez que deux lignes de sortie :

```console
$ cargo build
   Compiling guessing_game v0.1.0 (file:///projects/guessing_game)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.13s
```

Ces lignes montrent que Cargo n'update que la construction avec votre petit changement dans le fichier _src/main.rs_. Vos dépendances n'ont pas changé, donc Cargo sait qu'il peut réutiliser ce qu'il a déjà téléchargé et compilé pour celles-ci.

#### Assurer des Constructions Reproductibles

Cargo dispose d'un mécanisme qui garantit que vous pouvez reconstruire le même artefact chaque fois que vous ou quelqu'un d'autre construit votre code : Cargo n'utilisera que les versions des dépendances que vous avez spécifiées jusqu'à ce que vous indiquiez le contraire. Par exemple, disons que la semaine prochaine, la version 0.8.6 de la crate `rand` sort, et que cette version contient un correctif important, mais elle contient également une régression qui brisera votre code. Pour gérer cela, Rust crée le fichier _Cargo.lock_ la première fois que vous exécutez `cargo build`, donc nous avons maintenant cela dans le répertoire _guessing_game_.

Lorsque vous construisez un projet pour la première fois, Cargo détermine toutes les versions des dépendances qui correspondent aux critères et écrit ensuite celles-ci dans le fichier _Cargo.lock_. Lorsque vous construisez votre projet à l'avenir, Cargo verra que le fichier _Cargo.lock_ existe et n'utilisera que les versions spécifiées dans ce fichier plutôt que de faire tout le travail de détermination des versions à nouveau. Cela vous permet d'avoir automatiquement une construction reproductible. En d'autres termes, votre projet restera à 0.8.5 jusqu'à ce que vous décidiez explicitement de le mettre à niveau, grâce au fichier _Cargo.lock_. Étant donné que le fichier _Cargo.lock_ est important pour des constructions reproductibles, il est souvent intégré dans le contrôle de source avec le reste du code de votre projet.

#### Mise à Jour d'une Crate pour Obtenir une Nouvelle Version

Lorsque vous _voulez_ mettre à jour une crate, Cargo fournit la commande `update`, qui ignorera le fichier _Cargo.lock_ et déterminera toutes les dernière versions qui correspondent à vos spécifications dans _Cargo.toml_. Cargo écrira ensuite ces versions dans le fichier _Cargo.lock_. Sinon, par défaut, Cargo ne recherchera que les versions supérieures à 0.8.5 et inférieures à 0.9.0. Si la crate `rand` a publié les deux nouvelles versions 0.8.6 et 0.999.0, vous verriez ce qui suit si vous exécutiez `cargo update` :

```console
$ cargo update
    Updating crates.io index
     Locking 1 package to latest Rust 1.85.0 compatible version
    Updating rand v0.8.5 -> v0.8.6 (available: v0.999.0)
```

Cargo ignore la version 0.999.0. À ce stade, vous remarqueriez également un changement dans votre fichier _Cargo.lock_ notifiant que la version de la crate `rand` que vous utilisez maintenant est 0.8.6. Pour utiliser la version 0.999.0 de `rand` ou toute version de la série 0.999._x_, vous devrez mettre à jour le fichier _Cargo.toml_ pour ressembler à ceci à la place (ne faites pas réellement ce changement car les exemples suivants supposent que vous utilisez `rand` 0.8) :

```toml
[dependencies]
rand = "0.999.0"
```

La prochaine fois que vous exécuterez `cargo build`, Cargo mettra à jour le registre des crates disponibles et réévaluera vos exigences `rand` selon la nouvelle version que vous avez spécifiée.

Il y a beaucoup plus de choses à dire sur [Cargo][doccargo]<!-- ignore --> et [son écosystème][doccratesio]<!-- ignore -->, que nous aborderons dans le Chapitre 14, mais pour l'instant, c'est tout ce que vous devez savoir. Cargo facilite vraiment la réutilisation des bibliothèques, permettant aux Rustaceans d'écrire de plus petits projets réunis à partir d'un certain nombre de paquets.

### Génération d'un Nombre Aléatoire

Commençons à utiliser `rand` pour générer un nombre à deviner. La prochaine étape consiste à mettre à jour _src/main.rs_, comme montré dans la Liste 2-3.

<Listing number="2-3" file-name="src/main.rs" caption="Ajout de code pour générer un nombre aléatoire">

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-03/src/main.rs:all}}
```

</Listing>

Tout d'abord, nous ajoutons la ligne `use rand::Rng;`. Le trait `Rng` définit des méthodes que les générateurs de nombres aléatoires implémentent, et ce trait doit être dans le contexte pour que nous puissions utiliser ces méthodes. Le Chapitre 10 abordera les traits en détail.

Ensuite, nous ajoutons deux lignes au milieu. Dans la première ligne, nous appelons la fonction `rand::thread_rng` qui nous donne le générateur de nombres aléatoires particulier que nous allons utiliser : un qui est local au thread d'exécution actuel et est initialisé par le système d'exploitation. Ensuite, nous appelons la méthode `gen_range` sur le générateur de nombres aléatoires. Cette méthode est définie par le trait `Rng` que nous avons introduit dans le contexte avec l'instruction `use rand::Rng;`. La méthode `gen_range` prend une expression de plage comme argument et génère un nombre aléatoire dans cette plage. Le type d'expression de plage que nous utilisons ici prend la forme `start..=end` et est inclusif sur les bornes inférieure et supérieure, donc nous devons spécifier `1..=100` pour demander un nombre entre 1 et 100.

> Remarque : Vous ne saurez pas juste quels traits utiliser ni quelles méthodes et fonctions appeler à partir d'une crate, donc chaque crate a une documentation avec des instructions pour l'utiliser. Une autre fonctionnalité intéressante de Cargo est que l'exécution de la commande `cargo doc --open` compilera la documentation fournie par toutes vos dépendances localement et l'ouvrira dans votre navigateur. Si vous êtes intéressé par d'autres fonctionnalités de la crate `rand`, par exemple, exécutez `cargo doc --open` et cliquez sur `rand` dans la barre latérale à gauche.

La deuxième nouvelle ligne imprime le nombre secret. Cela est utile pendant que nous développons le programme pour pouvoir le tester, mais nous allons la supprimer dans la version finale. Ce n'est pas vraiment un jeu si le programme affiche la réponse dès le départ !

Essayez d'exécuter le programme plusieurs fois :

```console
$ cargo run
   Compiling guessing_game v0.1.0 (file:///projects/guessing_game)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.02s
     Running `target/debug/guessing_game`
Devinez le nombre !
Le nombre secret est : 7
Veuillez saisir votre devinette.
4
Vous avez deviné : 4

$ cargo run
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.02s
     Running `target/debug/guessing_game`
Devinez le nombre !
Le nombre secret est : 83
Veuillez saisir votre devinette.
5
Vous avez deviné : 5
```

Vous devriez obtenir des nombres aléatoires différents, et ils devraient tous être des nombres compris entre 1 et 100. Excellent travail !

## Comparaison de la Devinette avec le Nombre Secret

Maintenant que nous avons une entrée utilisateur et un nombre aléatoire, nous pouvons les comparer. Cette étape est montrée dans la Liste 2-4. Notez que ce code ne compilera pas encore, comme nous allons l'expliquer.

<Listing number="2-4" file-name="src/main.rs" caption="Gestion des valeurs de retour possibles de la comparaison de deux nombres">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-04/src/main.rs:here}}
```

</Listing>

Tout d'abord, nous ajoutons une autre déclaration `use`, amenant un type appelé `std::cmp::Ordering` dans le contexte de la bibliothèque standard. Le type `Ordering` est un autre enum et a les variantes `Less`, `Greater` et `Equal`. Ce sont les trois résultats qui sont possibles lorsque vous comparez deux valeurs.

Ensuite, nous ajoutons cinq nouvelles lignes en bas qui utilisent le type `Ordering`. La méthode `cmp` compare deux valeurs et peut être appelée sur n'importe quoi pouvant être comparé. Elle prend une référence à ce que vous voulez comparer avec : Ici, elle compare `guess` au `secret_number`. Ensuite, elle retourne une variante de l'énumération `Ordering` que nous avons introduite dans le contexte avec la déclaration `use`. Nous utilisons une expression [`match`][match]<!-- ignore --> pour décider quoi faire ensuite en fonction de quelle variante d'`Ordering` a été retournée par l'appel à `cmp` avec les valeurs dans `guess` et `secret_number`.

Une expression `match` est composée de _bras_. Un bras consiste en un _modèle_ à faire correspondre et le code qui doit être exécuté si la valeur donnée au `match` correspond au modèle de ce bras. Rust prend la valeur donnée au `match` et examine chaque modèle de bras à tour de rôle. Les modèles et la construction `match` sont des fonctionnalités puissantes de Rust : Ils vous permettent d'exprimer une variété de situations que votre code pourrait rencontrer, et ils s'assurent que vous les traitez toutes. Ces caractéristiques seront couvertes en détail dans le Chapitre 6 et le Chapitre 19, respectivement.

Examinons un exemple avec l'expression `match` que nous utilisons ici. Disons que l'utilisateur a deviné 50 et que le nombre secret généré aléatoirement cette fois est 38.

Lorsque le code compare 50 à 38, la méthode `cmp` renverra `Ordering::Greater` car 50 est supérieur à 38. L'expression `match` obtient la valeur `Ordering::Greater` et commence à vérifier chaque modèle de bras. Il examine le modèle du premier bras, `Ordering::Less`, et voit que la valeur `Ordering::Greater` ne correspond pas à `Ordering::Less`, donc il ignore le code dans ce bras et passe au bras suivant. Le modèle du bras suivant est `Ordering::Greater`, qui _correspond_ à `Ordering::Greater` ! Le code associé dans ce bras s'exécutera et affichera `Trop grand !` à l'écran. L'expression `match` se termine après le premier match réussi, donc elle ne regardera pas le dernier bras dans ce scénario.

Cependant, le code de la Liste 2-4 ne compilera pas encore. Essayons :

```console
{{#include ../listings/ch02-guessing-game-tutorial/listing-02-04/output.txt}}
```

Le cœur de l'erreur indique qu'il y a des _types incompatibles_. Rust a un système de types fort et statique. Cependant, il a aussi une inférence de type. Lorsque nous avons écrit `let mut guess = String::new()`, Rust a pu inférer que `guess` devait être une `String` et ne nous a pas fait écrire le type. Le `secret_number`, en revanche, est un type numérique. Plusieurs types numériques de Rust peuvent avoir une valeur entre 1 et 100 : `i32`, un nombre de 32 bits ; `u32`, un nombre entier de 32 bits non signé ; `i64`, un nombre de 64 bits ; ainsi que d'autres. Sauf indication contraire, Rust par défaut considère un `i32`, qui est le type de `secret_number` à moins que vous n'ajoutiez des informations de type ailleurs qui amèneraient Rust à inférer un type numérique différent. La raison de l'erreur est que Rust ne peut pas comparer une chaîne et un type numérique.

En fin de compte, nous voulons convertir la `String` que le programme lit comme entrée en un type numérique afin que nous puissions la comparer numériquement au nombre secret. Nous le faisons en ajoutant cette ligne dans le corps de la fonction `main` :

<span class="filename">Nom du fichier : src/main.rs</span>

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/no-listing-03-convert-string-to-number/src/main.rs:here}}
```

La ligne est :

```rust,ignore
let guess: u32 = guess.trim().parse().expect("Veuillez taper un nombre !");
```

Nous créons une variable nommée `guess`. Mais attendez, le programme n'a-t-il pas déjà une variable nommée `guess` ? Oui, mais heureusement Rust nous permet d'ombrelle la valeur précédente de `guess` avec une nouvelle. _L'ombrelle_ nous permet de réutiliser le nom de la variable `guess` sans nous forcer à créer deux variables uniques, comme `guess_str` et `guess`, par exemple. Nous aborderons cela plus en détail dans [le Chapitre 3][shadowing]<!-- ignore -->, mais pour l'instant, sachez que cette fonctionnalité est souvent utilisée lorsque vous souhaitez convertir une valeur d'un type à un autre type.

Nous lions cette nouvelle variable à l'expression `guess.trim().parse()`. Le `guess` dans l'expression fait référence à l'original variable `guess` qui contenait l'entrée sous forme de chaîne. La méthode `trim` sur une instance de `String` éliminera tout espace blanc au début et à la fin, ce que nous devons faire avant de pouvoir convertir la chaîne en un `u32`, qui ne peut contenir que des données numériques. L'utilisateur doit appuyer sur <kbd>enter</kbd> pour satisfaire `read_line` et entrer sa devinette, ce qui ajoute un caractère de nouvelle ligne à la chaîne. Par exemple, si l'utilisateur tape <kbd>5</kbd> et appuie sur <kbd>enter</kbd>, `guess` ressemble à ceci : `5\n`. Le `\n` représente « nouvelle ligne ». (Sous Windows, appuyer sur <kbd>enter</kbd> entraîne un retour chariot et une nouvelle ligne, `\r\n`.) La méthode `trim` élimine `\n` ou `\r\n`, ne laissant que `5`.

La méthode [`parse` sur les chaînes][parse]<!-- ignore --> convertit une chaîne en un autre type. Ici, nous l'utilisons pour convertir d'une chaîne à un nombre. Nous devons dire à Rust quel type numérique nous voulons exactement en utilisant `let guess: u32`. Le deux-points (`:`) après `guess` indique à Rust que nous allons annoter le type de la variable. Rust a quelques types numériques intégrés ; le `u32` vu ici est un entier non signé de 32 bits. C'est un bon choix par défaut pour un petit nombre positif. Vous en apprendrez davantage sur d'autres types numériques dans [le Chapitre 3][integers]<!-- ignore -->.

De plus, l'annotation `u32` dans cet exemple de programme et la comparaison avec `secret_number` signifie que Rust inférera également que `secret_number` devrait être un `u32`. Donc, maintenant la comparaison se fera entre deux valeurs du même type !

La méthode `parse` ne fonctionnera que sur des caractères qui peuvent logiquement être convertis en nombres et peut donc facilement causer des erreurs. Si, par exemple, la chaîne contenait `A👍%`, il n'y aurait aucun moyen de la convertir en un nombre. Parce que cela peut échouer, la méthode `parse` retourne un type `Result`, tout comme la méthode `read_line` (discutée plus tôt dans [« Gestion de la Potentielle Échec avec le Type `Result` »](#handling-potential-failure-with-the-result-type)<!-- ignore -->). Nous traiterons ce `Result` de la même manière en utilisant encore une fois la méthode `expect`. Si `parse` retourne une variante `Err` du type `Result` parce qu'il ne pouvait pas créer un nombre à partir de la chaîne, l'appel à `expect` fera planter le jeu et imprimera le message que nous lui donnons. Si `parse` peut réussir à convertir la chaîne en un nombre, il renverra la variante `Ok` du `Result`, et `expect` renverra le nombre que nous voulons à partir de la valeur `Ok`.

Exécutons maintenant le programme :

```console
$ cargo run
   Compiling guessing_game v0.1.0 (file:///projects/guessing_game)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.26s
     Running `target/debug/guessing_game`
Devinez le nombre !
Le nombre secret est : 58
Veuillez saisir votre devinette.
  76
Vous avez deviné : 76
Trop grand !
```

Super ! Même si des espaces ont été ajoutés avant la devinette, le programme a tout de même compris que l'utilisateur a deviné 76. Exécutez le programme quelques fois pour vérifier le comportement différent avec différents types d'entrées : devinez le nombre correctement, devinez un nombre qui est trop élevé et devinez un nombre qui est trop bas.

Nous avons presque tout le jeu en place maintenant, mais l'utilisateur ne peut faire qu'une seule devinette. Changeons cela en ajoutant une boucle !

## Autoriser Plusieurs Devinettes avec des Boucles

Le mot-clé `loop` crée une boucle infinie. Nous allons ajouter une boucle pour donner aux utilisateurs plus de chances de deviner le nombre :

<span class="filename">Nom du fichier : src/main.rs</span>

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/no-listing-04-looping/src/main.rs:here}}
```

Comme vous pouvez le voir, nous avons déplacé tout le prompt d'entrée de devinette et après dans une boucle. Assurez-vous d'indentationz les lignes à l'intérieur de la boucle de quatre espaces supplémentaires chacune et exécutez le programme à nouveau. Le programme demandera maintenant une autre devinette pour toujours, ce qui introduit en réalité un nouveau problème. Il ne semble pas que l'utilisateur puisse quitter !

L'utilisateur pourrait toujours interrompre le programme en utilisant le raccourci clavier <kbd>ctrl</kbd>-<kbd>C</kbd>. Mais il y a une autre manière d'échapper à ce monstre insatiable, comme mentionné dans la discussion sur `parse` dans [« Comparaison de la Devinette avec le Nombre Secret »](#comparing-the-guess-to-the-secret-number)<!-- ignore --> : Si l'utilisateur saisit une réponse non numérique, le programme plantera. Nous pouvons tirer parti de cela pour permettre à l'utilisateur de quitter, comme ici :

```console
$ cargo run
   Compiling guessing_game v0.1.0 (file:///projects/guessing_game)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.23s
     Running `target/debug/guessing_game`
Devinez le nombre !
Le nombre secret est : 59
Veuillez saisir votre devinette.
45
Vous avez deviné : 45
Trop petit !
Veuillez saisir votre devinette.
60
Vous avez deviné : 60
Trop grand !
Veuillez saisir votre devinette.
59
Vous avez deviné : 59
Vous gagnez !
Veuillez saisir votre devinette.
quitter

thread 'main' panicked at src/main.rs:28:47:
Veuillez taper un nombre !: ParseIntError { kind: InvalidDigit }
note : exécutez avec le variable d'environnement `RUST_BACKTRACE=1` pour afficher une trace de retour
```

En tapant `quitter`, le jeu se terminera, mais comme vous le noterez, il en sera de même si vous entrez toute autre entrée non numérique. Ce n'est pas optimal, pour le moins ; nous voulons également que le jeu s'arrête lorsque le nombre correct est deviné.

### Quitter Après une Devinette Correcte

Programmons le jeu pour qu'il quitte lorsque l'utilisateur gagne en ajoutant une instruction `break` :

<span class="filename">Nom du fichier : src/main.rs</span>

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/no-listing-05-quitting/src/main.rs:here}}
```

Ajouter la ligne `break` après `Vous gagnez !` fait sortir le programme de la boucle lorsque l'utilisateur devine correctement le nombre secret. Quitter la boucle signifie également quitter le programme, car la boucle est la dernière partie de `main`.

### Gestion des Entrées Invalides

Pour affiner encore plus le comportement du jeu, plutôt que de faire planter le programme lorsque l'utilisateur saisit une non-nombre, faisons en sorte que le jeu ignore un non-nombre afin que l'utilisateur puisse continuer à deviner. Nous pouvons le faire en modifiant la ligne où `guess` est converti d'une `String` à un `u32`, comme montré dans la Liste 2-5.

<Listing number="2-5" file-name="src/main.rs" caption="Ignorer une devinette non numérique et demander une autre devinette au lieu de faire planter le programme">

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-05/src/main.rs:here}}
```

</Listing>

Nous passons d'un appel `expect` à une expression `match` pour passer de l'échec à la gestion de l'erreur. Rappelez-vous que `parse` retourne un type `Result` et `Result` est un enum qui a les variantes `Ok` et `Err`. Nous utilisons ici une expression `match`, comme nous l'avons fait avec le résultat `Ordering` de la méthode `cmp`.

Si `parse` est capable de transformer la chaîne en un nombre, il renverra une valeur `Ok` contenant le nombre résultant. Cette valeur `Ok` correspondra au modèle du premier bras, et l'expression `match` retournera directement la valeur `num` que `parse` a produite et qui se trouve à l'intérieur de la valeur `Ok`. Ce nombre se retrouvera là où nous le voulons dans la nouvelle variable `guess` que nous sommes en train de créer.

Si `parse` ne parvient _pas_ à transformer la chaîne en nombre, il renverra une valeur `Err` contenant plus d'informations sur l'erreur. La valeur `Err` ne correspond pas au modèle `Ok(num)` dans le premier bras de `match`, mais elle correspond au modèle `Err(_)` dans le deuxième bras. Le souligné (_) est une valeur attrape-tout ; dans cet exemple, nous disons que nous voulons correspondre à toutes les valeurs `Err`, peu importe les informations qu'elles ont en elles. Ainsi, le programme exécutera le code du deuxième bras, `continue`, qui indique au programme de passer à l'itération suivante de la boucle et de demander une autre devinette. Ainsi, en gros, le programme ignore toutes les erreurs que `parse` pourrait rencontrer !

Maintenant, tout dans le programme devrait fonctionner comme prévu. Essayons :

```console
$ cargo run
   Compiling guessing_game v0.1.0 (file:///projects/guessing_game)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.13s
     Running `target/debug/guessing_game`
Devinez le nombre !
Le nombre secret est : 61
Veuillez saisir votre devinette.
10
Vous avez deviné : 10
Trop petit !
Veuillez saisir votre devinette.
99
Vous avez deviné : 99
Trop grand !
Veuillez saisir votre devinette.
foo
Veuillez saisir votre devinette.
61
Vous avez deviné : 61
Vous gagnez !
```

Génial ! Avec un petit dernier ajustement, nous allons terminer le jeu de devinette. Rappelez-vous que le programme imprime toujours le nombre secret. Cela a bien fonctionné pour les tests, mais cela ruine le jeu. Supprimons le `println!` qui affiche le nombre secret. La Liste 2-6 montre le code final.

<Listing number="2-6" file-name="src/main.rs" caption="Code complet du jeu de devinette">

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-06/src/main.rs}}
```

</Listing>

À ce stade, vous avez réussi à construire le jeu de devinette. Félicitations !

## Résumé

Ce projet a été une manière pratique d'introduire de nombreux nouveaux concepts de Rust : `let`, `match`, les fonctions, l'utilisation de crates externes, et plus encore. Dans les chapitres suivants, vous apprendrez ces concepts en détail. Le Chapitre 3 aborde des concepts que la plupart des langages de programmation ont, tels que des variables, des types de données et des fonctions, et montre comment les utiliser en Rust. Le Chapitre 4 explore la possession, une caractéristique qui rend Rust différent des autres langages. Le Chapitre 5 discute des structures et de la syntaxe des méthodes, et le Chapitre 6 explique comment fonctionnent les enums.

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
