## Bonjour, le monde !

Maintenant que vous avez installé Rust, il est temps d’écrire votre premier programme Rust.
Quand on apprend un nouveau langage, il est de tradition d’écrire un petit programme qui
affiche le texte `Hello, world!` à l’écran. Nous allons donc faire de même ici !

> Remarque : Ce livre suppose que vous avez quelques notions de base de la ligne de commande. Rust n’impose
> aucune exigence particulière concernant votre éditeur, vos outils ou l’emplacement de votre code. Ainsi,
> si vous préférez utiliser un IDE plutôt que la ligne de commande, n’hésitez pas à utiliser votre IDE
> préféré. De nombreux IDE prennent désormais en charge Rust dans une certaine mesure ; consultez la
> documentation de votre IDE pour en savoir plus. L’équipe Rust s’est attachée à offrir une excellente
> prise en charge des IDE via `rust-analyzer`. Consultez l’[annexe D][devtools]<!-- ignore -->
> pour plus de détails.

<!-- Old headings. Do not remove or links may break. -->
<a id="creating-a-project-directory"></a>

### Configuration du répertoire de projet

Commencez par créer un répertoire pour stocker votre code Rust. Rust ne se soucie pas de l’emplacement
de votre code, mais pour les exercices et les projets de ce livre, nous vous suggérons de créer un
répertoire _projects_ dans votre répertoire personnel et d’y conserver tous vos projets.

Ouvrez un terminal et saisissez les commandes suivantes pour créer un répertoire _projects_,
puis un répertoire pour le projet « Hello, world! » dans le répertoire _projects_.

Sous Linux, macOS et PowerShell sous Windows, saisissez ceci :

```console
$ mkdir ~/projects
$ cd ~/projects
$ mkdir hello_world
$ cd hello_world
```

Sous Windows CMD, saisissez ceci :

```cmd
> mkdir "%USERPROFILE%\projects"
> cd /d "%USERPROFILE%\projects"
> mkdir hello_world
> cd hello_world
```

<!-- Old headings. Do not remove or links may break. -->
<a id="writing-and-running-a-rust-program"></a>

### Les bases d’un programme Rust

Ensuite, créez un nouveau fichier source et nommez-le _main.rs_. Les fichiers Rust se terminent toujours
par l’extension _.rs_. Si votre nom de fichier comporte plusieurs mots, la convention consiste à les
séparer par un trait de soulignement. Par exemple, utilisez _hello_world.rs_ plutôt que _helloworld.rs_.

Ouvrez maintenant le fichier _main.rs_ que vous venez de créer et saisissez le code de la liste 1-1.

<Listing number="1-1" file-name="main.rs" caption="Un programme qui affiche `Hello, world!`">

```rust
fn main() {
    println!("Hello, world!");
}
```

</Listing>

Enregistrez le fichier et retournez à la fenêtre de votre terminal, dans le répertoire
_~/projects/hello_world_. Sous Linux ou macOS, saisissez les commandes suivantes pour compiler et
exécuter le fichier :

```console
$ rustc main.rs
$ ./main
Hello, world!
```

Sous Windows, saisissez la commande `.\main` au lieu de `./main` :

```powershell
> rustc main.rs
> .\main
Hello, world!
```

Quel que soit votre système d’exploitation, la chaîne `Hello, world!` devrait s’afficher dans le
terminal. Si vous ne voyez pas ce résultat, consultez la section « Dépannage » de la partie
[Installation][troubleshooting]<!-- ignore --> pour savoir comment obtenir de l’aide.

Si `Hello, world!` s’est bien affiché, félicitations ! Vous avez officiellement écrit un programme Rust.
Vous êtes donc un programmeur Rust : bienvenue !

<!-- Old headings. Do not remove or links may break. -->

<a id="anatomy-of-a-rust-program"></a>

### Anatomie d’un programme Rust

Examinons en détail ce programme « Hello, world! ». Voici le premier élément du puzzle :

```rust
fn main() {

}
```

Ces lignes définissent une fonction nommée `main`. La fonction `main` est particulière : c’est toujours
le premier code exécuté dans chaque programme Rust exécutable. Ici, la première ligne déclare une
fonction nommée `main` qui ne prend aucun paramètre et ne renvoie rien. S’il y avait des paramètres,
ils se trouveraient entre les parenthèses (`()`).

Le corps de la fonction est délimité par `{}`. Rust exige des accolades autour de tous les corps de
fonction. Il est recommandé de placer l’accolade ouvrante sur la même ligne que la déclaration de
fonction, en laissant un espace entre les deux.

> Remarque : Si vous souhaitez respecter un style standard dans tous vos projets Rust, vous pouvez
> utiliser un outil de formatage automatique appelé `rustfmt` pour formater votre code selon un style
> particulier (nous en reparlerons dans l’[annexe D][devtools]<!-- ignore -->). L’équipe Rust a inclus
> cet outil dans la distribution standard de Rust, tout comme `rustc` : il devrait donc déjà être
> installé sur votre ordinateur !

Le corps de la fonction `main` contient le code suivant :

```rust
println!("Hello, world!");
```

Cette ligne fait tout le travail dans ce petit programme : elle affiche du texte à l’écran. Voici trois
détails importants à remarquer.

Premièrement, `println!` appelle une macro Rust. Si elle appelait une fonction, on l’écrirait
`println` (sans le `!`). Les macros Rust permettent d’écrire du code qui génère du code afin d’étendre
la syntaxe de Rust ; nous les étudierons plus en détail au [chapitre 20][ch20-macros]<!-- ignore -->.
Pour l’instant, retenez que le `!` signifie que vous appelez une macro plutôt qu’une fonction
ordinaire et que les macros ne suivent pas toujours les mêmes règles que les fonctions.

Deuxièmement, vous voyez la chaîne `"Hello, world!"`. Nous transmettons cette chaîne comme argument à
`println!`, qui l’affiche à l’écran.

Troisièmement, nous terminons la ligne par un point-virgule (`;`), qui indique que cette expression
est terminée et que la suivante peut commencer. La plupart des lignes de code Rust se terminent par un
point-virgule.

<!-- Old headings. Do not remove or links may break. -->
<a id="compiling-and-running-are-separate-steps"></a>

### La compilation et l’exécution sont deux étapes distinctes

Vous venez d’exécuter un programme nouvellement créé ; examinons donc chacune des étapes du processus.

Avant d’exécuter un programme Rust, vous devez le compiler à l’aide du compilateur Rust en saisissant
la commande `rustc` et en lui transmettant le nom de votre fichier source, comme ceci :

```console
$ rustc main.rs
```

Si vous connaissez C ou C++, vous remarquerez que cela ressemble à `gcc` ou `clang`. Une fois la
compilation réussie, Rust produit un exécutable binaire.

Sous Linux, macOS et PowerShell sous Windows, vous pouvez afficher l’exécutable en saisissant la
commande `ls` dans votre shell :

```console
$ ls
main  main.rs
```

Sous Linux et macOS, vous verrez deux fichiers. Avec PowerShell sous Windows, vous verrez les mêmes
trois fichiers qu’avec CMD. Avec CMD sous Windows, vous saisiriez la commande suivante :

```cmd
> dir /B %= the /B option says to only show the file names =%
main.exe
main.pdb
main.rs
```

Vous voyez ainsi le fichier de code source avec l’extension _.rs_, le fichier exécutable (_main.exe_
sous Windows, mais _main_ sur toutes les autres plateformes) et, sous Windows, un fichier contenant
des informations de débogage avec l’extension _.pdb_. Vous pouvez alors exécuter le fichier _main_
ou _main.exe_, comme ceci :

```console
$ ./main # or .\main on Windows
```

Si votre fichier _main.rs_ contient votre programme « Hello, world! », cette ligne affiche `Hello,
world!` dans votre terminal.

Si vous connaissez mieux un langage dynamique, comme Ruby, Python ou JavaScript, vous n’avez peut-être
pas l’habitude de compiler et d’exécuter un programme en deux étapes distinctes. Rust est un langage
_à compilation anticipée_ : vous pouvez compiler un programme et transmettre l’exécutable à quelqu’un
d’autre, qui pourra l’exécuter même sans avoir installé Rust. Si vous transmettez à quelqu’un un
fichier _.rb_, _.py_ ou _.js_, cette personne devra avoir installé une implémentation de Ruby, Python
ou JavaScript, respectivement. Mais avec ces langages, une seule commande suffit pour compiler et
exécuter votre programme. Tout choix de conception d’un langage implique des compromis.

La compilation avec `rustc` convient parfaitement aux programmes simples, mais à mesure que votre
projet grandit, vous voudrez gérer toutes les options et faciliter le partage de votre code. Nous
allons maintenant vous présenter l’outil Cargo, qui vous aidera à écrire des programmes Rust destinés
au monde réel.

[troubleshooting]: ch01-01-installation.html#troubleshooting
[devtools]: appendix-04-useful-development-tools.html
[ch20-macros]: ch20-05-macros.html