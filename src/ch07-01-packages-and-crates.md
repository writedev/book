## Paquets et Caissons

Les premières parties du système de modules que nous allons aborder sont les paquets et les caissons.

Un _caisson_ est la plus petite quantité de code que le compilateur Rust considère à la fois. Même si vous exécutez `rustc` plutôt que `cargo` et passez un seul fichier source (comme nous l'avons fait au tout début dans [« Les bases du programme Rust »][basics]<!-- ignore --> dans le Chapitre 1), le compilateur considère ce fichier comme un caisson. Les caissons peuvent contenir des modules, et les modules peuvent être définis dans d'autres fichiers qui sont compilés avec le caisson, comme nous le verrons dans les sections à venir.

Un caisson peut se présenter sous l'une des deux formes : un caisson binaire ou un caisson de bibliothèque. Les _caissons binaires_ sont des programmes que vous pouvez compiler en un exécutable que vous pouvez exécuter, tel qu'un programme en ligne de commande ou un serveur. Chacun doit avoir une fonction appelée `main` qui définit ce qui se passe lorsque l'exécutable s'exécute. Tous les caissons que nous avons créés jusqu'à présent ont été des caissons binaires.

Les _caissons de bibliothèque_ n'ont pas de fonction `main` et ne se compilent pas en un exécutable. Au lieu de cela, ils définissent des fonctionnalités destinées à être partagées avec plusieurs projets. Par exemple, le caisson `rand` que nous avons utilisé dans [Chapitre 2][rand]<!-- ignore --> fournit des fonctionnalités qui génèrent des nombres aléatoires. La plupart du temps, lorsque les Rustaciens disent « caisson », ils font référence à un caisson de bibliothèque, et ils utilisent « caisson » de manière interchangeable avec le concept général de programmation d'une « bibliothèque ».

La _racine de caisson_ est un fichier source dont le compilateur Rust part et qui constitue le module racine de votre caisson (nous expliquerons les modules en profondeur dans [« Contrôler la portée et la confidentialité avec des modules »][modules]<!-- ignore -->).

Un _paquet_ est un ensemble d'un ou plusieurs caissons qui fournit un ensemble de fonctionnalités. Un paquet contient un fichier _Cargo.toml_ qui décrit comment construire ces caissons. Cargo est en fait un paquet qui contient le caisson binaire pour l'outil en ligne de commande que vous avez utilisé pour construire votre code. Le paquet Cargo contient également un caisson de bibliothèque dont dépend le caisson binaire. D'autres projets peuvent dépendre du caisson de bibliothèque Cargo pour utiliser la même logique que l'outil en ligne de commande Cargo utilise.

Un paquet peut contenir autant de caissons binaires que vous le souhaitez, mais au maximum un seul caisson de bibliothèque. Un paquet doit contenir au moins un caisson, qu'il s'agisse d'un caisson de bibliothèque ou binaire.

Examinons ce qui se passe lorsque nous créons un paquet. D'abord, nous entrons la commande `cargo new my-project` :

```console
$ cargo new my-project
     Créé le paquet binaire (application) `my-project`
$ ls my-project
Cargo.toml
src
$ ls my-project/src
main.rs
```

Après avoir exécuté `cargo new my-project`, nous utilisons `ls` pour voir ce que Cargo crée. Dans le répertoire _my-project_, il y a un fichier _Cargo.toml_, ce qui nous donne un paquet. Il y a également un répertoire _src_ qui contient _main.rs_. Ouvrez _Cargo.toml_ dans votre éditeur de texte et notez qu'il n'y a aucune mention de _src/main.rs_. Cargo suit une convention selon laquelle _src/main.rs_ est la racine du caisson d'un caisson binaire portant le même nom que le paquet. De même, Cargo sait que si le répertoire du paquet contient _src/lib.rs_, le paquet contient un caisson de bibliothèque portant le même nom que le paquet, et _src/lib.rs_ est sa racine de caisson. Cargo transmet les fichiers racine de caisson à `rustc` pour construire la bibliothèque ou le binaire.

Ici, nous avons un paquet qui ne contient que _src/main.rs_, ce qui signifie qu'il ne contient qu'un caisson binaire nommé `my-project`. Si un paquet contient _src/main.rs_ et _src/lib.rs_, il a deux caissons : un binaire et une bibliothèque, tous deux portant le même nom que le paquet. Un paquet peut avoir plusieurs caissons binaires en plaçant des fichiers dans le répertoire _src/bin_ : chaque fichier sera un caisson binaire distinct.

[basics]: ch01-02-hello-world.html#rust-program-basics
[modules]: ch07-02-defining-modules-to-control-scope-and-privacy.html
[rand]: ch02-00-guessing-game-tutorial.html#generating-a-random-number