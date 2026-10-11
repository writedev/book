## Paquets et caisses

Les premières parties du système de modules que nous allons aborder sont les paquets et les caisses.

Une _caisse_ est la plus petite quantité de code que le compilateur Rust traite à la fois. Même si vous exécutez `rustc` plutôt que `cargo` et que vous lui transmettez un seul fichier de code source (comme nous l’avons fait dès le [« Principes de base d’un programme Rust »][basics]<!-- ignore
--> au chapitre 1), le compilateur considère ce fichier comme une caisse. Les caisses peuvent contenir des modules, et ces modules peuvent être définis dans d’autres fichiers compilés avec la caisse, comme nous le verrons dans les prochaines sections.

Une caisse peut prendre l’une de deux formes : une caisse binaire ou une caisse bibliothèque. Les _caisses binaires_ sont des programmes que vous pouvez compiler en exécutables, que vous pouvez ensuite lancer, comme un programme en ligne de commande ou un serveur. Chacune doit avoir une fonction appelée `main` qui définit ce qui se passe lorsque l’exécutable s’exécute. Toutes les caisses que nous avons créées jusqu’à présent étaient des caisses binaires.

Les _caisses bibliothèque_ n’ont pas de fonction `main` et ne sont pas compilées en exécutables. Elles définissent plutôt des fonctionnalités destinées à être partagées entre plusieurs projets. Par exemple, la caisse `rand` que nous avons utilisée au [chapitre 2][rand]<!-- ignore --> fournit des fonctionnalités permettant de générer des nombres aléatoires. La plupart du temps, lorsque les adeptes de Rust disent « caisse », ils parlent d’une caisse bibliothèque et emploient « caisse » de manière interchangeable avec le concept général de programmation de « bibliothèque ».

La _racine de caisse_ est un fichier source à partir duquel le compilateur Rust commence et qui constitue le module racine de votre caisse (nous expliquerons les modules en détail dans [« Contrôler la portée et la confidentialité avec les modules »][modules]<!-- ignore -->).

Un _paquet_ est un ensemble d’une ou de plusieurs caisses qui fournit un ensemble de fonctionnalités. Un paquet contient un fichier _Cargo.toml_ qui décrit comment construire ces caisses. Cargo est lui-même un paquet qui contient la caisse binaire de l’outil en ligne de commande que vous utilisez pour construire votre code. Le paquet Cargo contient également une caisse bibliothèque dont dépend la caisse binaire. D’autres projets peuvent dépendre de la caisse bibliothèque de Cargo pour utiliser la même logique que celle de l’outil en ligne de commande Cargo.

Un paquet peut contenir autant de caisses binaires que vous le souhaitez, mais au plus une seule caisse bibliothèque. Un paquet doit contenir au moins une caisse, qu’il s’agisse d’une caisse bibliothèque ou binaire.

Voyons ce qui se passe lorsque nous créons un paquet. Tout d’abord, nous saisissons la commande `cargo new my-project` :

```console
$ cargo new my-project
     Created binary (application) `my-project` package
$ ls my-project
Cargo.toml
src
$ ls my-project/src
main.rs
```

Après avoir exécuté `cargo new my-project`, nous utilisons `ls` pour voir ce que Cargo a créé. Dans le répertoire _my-project_, il y a un fichier _Cargo.toml_, qui nous fournit un paquet. Il y a également un répertoire _src_ qui contient _main.rs_. Ouvrez _Cargo.toml_ dans votre éditeur de texte et remarquez qu’il ne fait aucune mention de _src/main.rs_. Cargo suit une convention selon laquelle _src/main.rs_ est la racine de caisse d’une caisse binaire portant le même nom que le paquet. De même, Cargo sait que si le répertoire du paquet contient _src/lib.rs_, le paquet contient une caisse bibliothèque portant le même nom que le paquet, et que _src/lib.rs_ est sa racine de caisse. Cargo transmet les fichiers racines de caisse à `rustc` pour construire la bibliothèque ou le binaire.

Ici, nous avons un paquet qui ne contient que _src/main.rs_, ce qui signifie qu’il ne contient qu’une caisse binaire nommée `my-project`. Si un paquet contient _src/main.rs_ et _src/lib.rs_, il possède deux caisses : une binaire et une bibliothèque, toutes deux portant le même nom que le paquet. Un paquet peut avoir plusieurs caisses binaires en plaçant des fichiers dans le répertoire _src/bin_ : chaque fichier constituera une caisse binaire distincte.

[basics]: ch01-02-hello-world.html#rust-program-basics
[modules]: ch07-02-defining-modules-to-control-scope-and-privacy.html
[rand]: ch02-00-guessing-game-tutorial.html#generating-a-random-number