## Bonjour, Monde !

Maintenant que vous avez installé Rust, il est temps d'écrire votre premier programme en Rust. Il est traditionnel d'écrire un petit programme qui affiche le texte `Bonjour, monde !` à l'écran lorsque l'on apprend un nouveau langage, nous allons faire de même ici !

> Remarque : Ce livre suppose une familiarité de base avec la ligne de commande. Rust n'impose pas de demandes spécifiques concernant votre éditeur, vos outils ou l'emplacement de votre code. Donc, si vous préférez utiliser un IDE plutôt que la ligne de commande, n'hésitez pas à utiliser votre IDE préféré. De nombreux IDE supportent désormais Rust ; consultez la documentation de l'IDE pour plus de détails. L'équipe Rust s'est concentrée sur la possibilité d'un excellent support IDE via `rust-analyzer`. Consultez [l'Annexe D][devtools]<!-- ignore --> pour plus de détails.

<!-- Anciens titres. Ne pas supprimer ou les liens peuvent être rompus. -->
<a id="creating-a-project-directory"></a>

### Configuration du Répertoire du Projet

Vous allez commencer par créer un répertoire pour stocker votre code Rust. Peu importe pour Rust où se trouve votre code, mais pour les exercices et projets de ce livre, nous vous suggérons de créer un répertoire _projects_ dans votre répertoire personnel et de garder tous vos projets là-bas.

Ouvrez un terminal et entrez les commandes suivantes pour créer un répertoire _projects_ et un répertoire pour le projet "Bonjour, monde !" dans le répertoire _projects_.

Pour Linux, macOS et PowerShell sur Windows, entrez ceci :

```console
$ mkdir ~/projects
$ cd ~/projects
$ mkdir hello_world
$ cd hello_world
```

Pour Windows CMD, entrez ceci :

```cmd
> mkdir "%USERPROFILE%\projects"
> cd /d "%USERPROFILE%\projects"
> mkdir hello_world
> cd hello_world
```

<!-- Anciens titres. Ne pas supprimer ou les liens peuvent être rompus. -->
<a id="writing-and-running-a-rust-program"></a>

### Les Bases d'un Programme en Rust

Ensuite, créez un nouveau fichier source et appelez-le _main.rs_. Les fichiers Rust se terminent toujours par l'extension _.rs_. Si vous utilisez plus d'un mot dans le nom de votre fichier, la convention est d'utiliser un underscore pour les séparer. Par exemple, utilisez _hello_world.rs_ plutôt que _helloworld.rs_.

Ouvrez maintenant le fichier _main.rs_ que vous venez de créer et entrez le code de la liste 1-1.

<Listing number="1-1" file-name="main.rs" caption="Un programme qui imprime `Bonjour, monde !`">

```rust
fn main() {
    println!("Bonjour, monde !");
}
```

</Listing>

Enregistrez le fichier et retournez à votre fenêtre de terminal dans le répertoire _~/projects/hello_world_. Sur Linux ou macOS, entrez les commandes suivantes pour compiler et exécuter le fichier :

```console
$ rustc main.rs
$ ./main
Bonjour, monde !
```

Sur Windows, entrez la commande `.\main` au lieu de `./main` :

```powershell
> rustc main.rs
> .\main
Bonjour, monde !
```

Peu importe votre système d'exploitation, la chaîne `Bonjour, monde !` devrait s'afficher dans le terminal. Si vous ne voyez pas cette sortie, consultez la partie [“Dépannage”][troubleshooting]<!-- ignore --> de la section Installation pour des moyens d'obtenir de l'aide.

Si `Bonjour, monde !` s'est affiché, félicitations ! Vous avez officiellement écrit un programme en Rust. Cela fait de vous un programmeur Rust—bienvenue !

<!-- Anciens titres. Ne pas supprimer ou les liens peuvent être rompus. -->

<a id="anatomy-of-a-rust-program"></a>

### L'Anatomie d'un Programme en Rust

Passons en revue ce programme "Bonjour, monde !" en détail. Voici le premier élément du puzzle :

```rust
fn main() {

}
```

Ces lignes définissent une fonction nommée `main`. La fonction `main` est spéciale : elle est toujours le premier code qui s'exécute dans chaque programme Rust exécutable. Ici, la première ligne déclare une fonction nommée `main` qui n'a pas de paramètres et ne retourne rien. S'il y avait des paramètres, ils iraient à l'intérieur des parenthèses (`()`).

Le corps de la fonction est encadré par `{}`. Rust exige des accolades autour de tous les corps de fonction. Il est de bon ton de placer l'accolade ouvrante sur la même ligne que la déclaration de la fonction, en ajoutant un espace entre les deux.

> Remarque : Si vous souhaitez respecter un style standard dans tous vos projets Rust, vous pouvez utiliser un outil de formatage automatique appelé `rustfmt` pour formater votre code dans un style particulier (plus d'informations sur `rustfmt` dans [l'Annexe D][devtools]<!-- ignore -->). L'équipe Rust a inclus cet outil avec la distribution standard de Rust, tout comme `rustc`, donc il doit déjà être installé sur votre ordinateur !

Le corps de la fonction `main` contient le code suivant :

```rust
println!("Bonjour, monde !");
```

Cette ligne réalise tout le travail dans ce petit programme : elle affiche du texte à l'écran. Trois détails importants sont à noter ici.

Tout d'abord, `println!` appelle une macro Rust. Si elle avait appelé une fonction à la place, cela aurait été écrit comme `println` (sans le `!`). Les macros Rust sont un moyen d'écrire du code qui génère du code pour étendre la syntaxe de Rust, et nous en discuterons plus en détail dans [Chapitre 20][ch20-macros]<!-- ignore -->. Pour l'instant, vous devez juste savoir qu'utiliser un `!` signifie que vous appelez une macro au lieu d'une fonction normale et que les macros ne suivent pas toujours les mêmes règles que les fonctions.

Deuxièmement, vous voyez la chaîne `"Bonjour, monde !"`. Nous passons cette chaîne comme argument à `println!`, et la chaîne est affichée à l'écran.

Troisièmement, nous terminons la ligne par un point-virgule (`;`), ce qui indique que cette expression est terminée et que la suivante est prête à commencer. La plupart des lignes de code Rust se terminent par un point-virgule.

<!-- Anciens titres. Ne pas supprimer ou les liens peuvent être rompus. -->
<a id="compiling-and-running-are-separate-steps"></a>

### La Compilation et l'Exécution

Vous venez de lancer un programme nouvellement créé, examinons donc chaque étape du processus.

Avant d'exécuter un programme Rust, vous devez le compiler en utilisant le compilateur Rust en entrant la commande `rustc` et en passant le nom de votre fichier source, comme ceci :

```console
$ rustc main.rs
```

Si vous avez un bagage en C ou C++, vous remarquerez que c'est similaire à `gcc` ou `clang`. Après une compilation réussie, Rust génère un exécutable binaire.

Sur Linux, macOS et PowerShell sur Windows, vous pouvez voir l'exécutable en entrant la commande `ls` dans votre shell :

```console
$ ls
main  main.rs
```

Sur Linux et macOS, vous verrez deux fichiers. Avec PowerShell sur Windows, vous verrez les mêmes trois fichiers que vous verriez avec CMD. Avec CMD sur Windows, vous entreriez ce qui suit :

```cmd
> dir /B %= l'option /B dit d'afficher uniquement les noms de fichiers =%
main.exe
main.pdb
main.rs
```

Cela montre le fichier de code source avec l'extension _.rs_, le fichier exécutable (_main.exe_ sur Windows, mais _main_ sur toutes les autres plates-formes), et, lorsque vous utilisez Windows, un fichier contenant des informations de débogage avec l'extension _.pdb_. À partir de là, vous exécutez le fichier _main_ ou _main.exe_, comme ceci :

```console
$ ./main # ou .\main sur Windows
```

Si votre _main.rs_ est votre programme "Bonjour, monde !", cette ligne affichera `Bonjour, monde !` dans votre terminal.

Si vous êtes plus familier avec un langage dynamique, tel que Ruby, Python ou JavaScript, vous pourriez ne pas être habitué à compiler et à exécuter un programme en tant qu'étapes séparées. Rust est un langage compilé _à l'avance_, ce qui signifie que vous pouvez compiler un programme et donner l'exécutable à quelqu'un d'autre, et ils peuvent l'exécuter même sans avoir Rust installé. Si vous donnez à quelqu'un un fichier _.rb_, _.py_ ou _.js_, ils doivent avoir une implémentation de Ruby, Python ou JavaScript installée (respectivement). Mais dans ces langages, vous n'avez besoin que d'une seule commande pour compiler et exécuter votre programme. Tout cela est une question de compromis dans la conception des langages.

Compiler simplement avec `rustc` est suffisant pour des programmes simples, mais à mesure que votre projet grandit, vous voudrez gérer toutes les options et faciliter le partage de votre code. Ensuite, nous vous introduirons à l'outil Cargo, qui vous aidera à écrire de véritables programmes Rust.

[troubleshooting]: ch01-01-installation.html#troubleshooting
[devtools]: appendix-04-useful-development-tools.html
[ch20-macros]: ch20-05-macros.html