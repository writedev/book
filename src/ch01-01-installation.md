## Installation

La première étape consiste à installer Rust. Nous allons télécharger Rust via `rustup`, un outil en ligne de commande pour gérer les versions de Rust et les outils associés. Vous aurez besoin d'une connexion Internet pour le téléchargement.

> Note : Si vous préférez ne pas utiliser `rustup` pour une raison quelconque, veuillez consulter la
> [page des autres méthodes d'installation de Rust][otherinstall] pour plus d'options.

Les étapes suivantes installent la dernière version stable du compilateur Rust. Les garanties de stabilité de Rust assurent que tous les exemples du livre qui compilent continueront à compiler avec les versions plus récentes de Rust. La sortie peut légèrement différer entre les versions, car Rust améliore souvent les messages d'erreur et les avertissements. En d'autres termes, toute version stable plus récente de Rust que vous installez en suivant ces étapes devrait fonctionner comme prévu avec le contenu de ce livre.

> ### Notation en ligne de commande
>
> Dans ce chapitre et tout au long du livre, nous montrerons certaines commandes utilisées dans le terminal. Les lignes que vous devez entrer dans un terminal commencent toutes par `$`. Vous n'avez pas besoin de taper le caractère `$` ; c'est l'invite de ligne de commande qui indique le début de chaque commande. Les lignes qui ne commencent pas par `$` montrent généralement la sortie de la commande précédente. De plus, les exemples spécifiques à PowerShell utiliseront `>` au lieu de `$`.

### Installer `rustup` sur Linux ou macOS

Si vous utilisez Linux ou macOS, ouvrez un terminal et entrez la commande suivante :

```console
$ curl --proto '=https' --tlsv1.2 https://sh.rustup.rs -sSf | sh
```

Cette commande télécharge un script et lance l'installation de l'outil `rustup`, qui installe la dernière version stable de Rust. Il se peut que vous soyez invité à entrer votre mot de passe. Si l'installation réussit, la ligne suivante apparaîtra :

```text
Rust is installed now. Great!
```

Vous aurez également besoin d'un _linker_, qui est un programme que Rust utilise pour assembler ses sorties compilées en un seul fichier. Il est probable que vous en ayez déjà un. Si vous obtenez des erreurs de linker, vous devriez installer un compilateur C, qui comprendra généralement un linker. Un compilateur C est également utile car certains paquets Rust courants dépendent de code C et auront besoin d'un compilateur C.

Sur macOS, vous pouvez obtenir un compilateur C en exécutant :

```console
$ xcode-select --install
```

Les utilisateurs de Linux devraient généralement installer GCC ou Clang, selon la documentation de leur distribution. Par exemple, si vous utilisez Ubuntu, vous pouvez installer le paquet `build-essential`.

### Installer `rustup` sur Windows

Sur Windows, allez sur [https://www.rust-lang.org/tools/install][install] et suivez les instructions pour installer Rust. À un moment donné pendant l'installation, vous serez invité à installer Visual Studio. Cela fournit un linker et les bibliothèques natives nécessaires pour compiler des programmes. Si vous avez besoin de plus d'aide à cette étape, consultez
[https://rust-lang.github.io/rustup/installation/windows-msvc.html][msvc].

Le reste de ce livre utilise des commandes qui fonctionnent à la fois dans _cmd.exe_ et PowerShell. S'il y a des différences spécifiques, nous expliquerons lequel utiliser.

### Résolution des problèmes

Pour vérifier si Rust est installé correctement, ouvrez un shell et entrez cette ligne :

```console
$ rustc --version
```

Vous devriez voir le numéro de version, le hash de commit et la date de commit pour la dernière version stable qui a été publiée, dans le format suivant :

```text
rustc x.y.z (abcabcabc yyyy-mm-dd)
```

Si vous voyez cette information, vous avez installé Rust avec succès ! Si vous ne voyez pas cette information, vérifiez que Rust est dans votre variable système `%PATH%` comme suit.

Dans Windows CMD, utilisez :

```console
> echo %PATH%
```

Dans PowerShell, utilisez :

```powershell
> echo $env:Path
```

Dans Linux et macOS, utilisez :

```console
$ echo $PATH
```

Si tout cela est correct et que Rust ne fonctionne toujours pas, il existe plusieurs endroits où vous pouvez obtenir de l'aide. Découvrez comment entrer en contact avec d'autres Rustaceans (un surnom amusant que nous nous donnons) sur [la page communautaire][community].

### Mise à jour et désinstallation

Une fois Rust installé via `rustup`, la mise à jour vers une nouvelle version publiée est facile. Depuis votre shell, exécutez le script de mise à jour suivant :

```console
$ rustup update
```

Pour désinstaller Rust et `rustup`, exécutez le script de désinstallation suivant depuis votre shell :

```console
$ rustup self uninstall
```

<!-- Anciens titres. Ne pas supprimer ou les liens peuvent se briser. -->
<a id="local-documentation"></a>

### Lecture de la documentation locale

L'installation de Rust comprend également une copie locale de la documentation afin que vous puissiez la lire hors ligne. Exécutez `rustup doc` pour ouvrir la documentation locale dans votre navigateur.

Chaque fois qu'un type ou une fonction est fourni par la bibliothèque standard et que vous n'êtes pas sûr de son fonctionnement ou de son utilisation, utilisez la documentation de l'interface de programmation d'application (API) pour le découvrir !

<!-- Anciens titres. Ne pas supprimer ou les liens peuvent se briser. -->
<a id="text-editors-and-integrated-development-environments"></a>

### Utilisation d'éditeurs de texte et d'IDE

Ce livre ne fait aucune supposition sur les outils que vous utilisez pour écrire du code Rust. À peu près n'importe quel éditeur de texte fera l'affaire ! Cependant, de nombreux éditeurs de texte et environnements de développement intégrés (IDE) ont un support intégré pour Rust. Vous pouvez toujours trouver une liste assez à jour de nombreux éditeurs et IDE sur [la page des outils][tools] du site Rust.

### Travailler hors ligne avec ce livre

Dans plusieurs exemples, nous utiliserons des paquets Rust au-delà de la bibliothèque standard. Pour travailler à travers ces exemples, vous aurez soit besoin d'une connexion Internet, soit d'avoir téléchargé ces dépendances à l'avance. Pour télécharger les dépendances à l'avance, vous pouvez exécuter les commandes suivantes. (Nous expliquerons ce qu'est `cargo` et ce que fait chacune de ces commandes en détail plus tard.)

```console
$ cargo new get-dependencies
$ cd get-dependencies
$ cargo add rand@0.10.1 trpl@0.2.0
```

Cela va mettre en cache les téléchargements pour ces paquets afin que vous n'ayez pas besoin de les télécharger plus tard. Une fois que vous avez exécuté cette commande, vous n'avez pas besoin de conserver le dossier `get-dependencies`. Si vous avez exécuté cette commande, vous pouvez utiliser le flag `--offline` avec toutes les commandes `cargo` dans le reste du livre pour utiliser ces versions mises en cache au lieu d'essayer d'utiliser le réseau.

[otherinstall]: https://forge.rust-lang.org/infra/other-installation-methods.html
[install]: https://www.rust-lang.org/tools/install
[msvc]: https://rust-lang.github.io/rustup/installation/windows-msvc.html
[community]: https://www.rust-lang.org/community
[tools]: https://www.rust-lang.org/tools