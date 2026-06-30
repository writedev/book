## Installation

La première étape consiste à installer Rust. Nous téléchargerons Rust via `rustup`, un outil en ligne de commande pour gérer les versions de Rust et les outils associés. Vous aurez besoin d'une connexion Internet pour le téléchargement.

> Remarque : Si vous préférez ne pas utiliser `rustup` pour une raison quelconque, consultez la page [Autres méthodes d'installation de Rust][otherinstall] pour plus d'options.

Les étapes suivantes installent la dernière version stable du compilateur Rust. Les garanties de stabilité de Rust assurent que tous les exemples du livre qui se compilent continueront de se compiler avec des versions Rust plus récentes. La sortie peut légèrement différer entre les versions, car Rust améliore souvent les messages d'erreur et les avertissements. En d'autres termes, toute version stable plus récente de Rust que vous installerez en suivant ces étapes devrait fonctionner comme prévu avec le contenu de ce livre.

> ### Notation en ligne de commande
>
> Dans ce chapitre et tout au long du livre, nous montrerons certaines commandes utilisées dans le terminal. Les lignes que vous devez entrer dans un terminal commencent toutes par `$`. Vous n'avez pas besoin de taper le caractère `$` ; c'est l'invite de commande affichée pour indiquer le début de chaque commande. Les lignes qui ne commencent pas par `$` montrent généralement la sortie de la commande précédente. De plus, les exemples spécifiques à PowerShell utiliseront `>` plutôt que `$`.

### Installation de `rustup` sur Linux ou macOS

Si vous utilisez Linux ou macOS, ouvrez un terminal et entrez la commande suivante :

```console
$ curl --proto '=https' --tlsv1.2 https://sh.rustup.rs -sSf | sh
```

Cette commande télécharge un script et commence l'installation de l'outil `rustup`, qui installe la dernière version stable de Rust. Il se peut que vous soyez invité à entrer votre mot de passe. Si l'installation réussit, la ligne suivante apparaîtra :

```text
Rust is installed now. Great!
```

Vous aurez également besoin d'un _linker_, qui est un programme que Rust utilise pour joindre ses sorties compilées en un seul fichier. Il est probable que vous en ayez déjà un. Si vous obtenez des erreurs de linker, vous devez installer un compilateur C, qui inclura généralement un linker. Un compilateur C est également utile car certains packages courants de Rust dépendent du code C et auront besoin d'un compilateur C.

Sur macOS, vous pouvez obtenir un compilateur C en exécutant :

```console
$ xcode-select --install
```

Les utilisateurs de Linux devraient généralement installer GCC ou Clang, selon la documentation de leur distribution. Par exemple, si vous utilisez Ubuntu, vous pouvez installer le paquet `build-essential`.

### Installation de `rustup` sur Windows

Sur Windows, allez sur [https://www.rust-lang.org/tools/install][install] et suivez les instructions pour installer Rust. À un moment donné de l'installation, il vous sera demandé d'installer Visual Studio. Cela fournit un linker et les bibliothèques natives nécessaires pour compiler des programmes. Si vous avez besoin de plus d'aide à ce sujet, consultez [https://rust-lang.github.io/rustup/installation/windows-msvc.html][msvc].

Le reste de ce livre utilise des commandes qui fonctionnent à la fois dans _cmd.exe_ et PowerShell. Si des différences spécifiques existent, nous expliquerons lesquels utiliser.

### Dépannage

Pour vérifier si vous avez bien installé Rust, ouvrez un shell et entrez cette ligne :

```console
$ rustc --version
```

Vous devriez voir le numéro de version, le hash de commit et la date de commit pour la dernière version stable qui a été publiée, au format suivant :

```text
rustc x.y.z (abcabcabc yyyy-mm-dd)
```

Si vous voyez cette information, vous avez installé Rust avec succès ! Si vous ne voyez pas cette information, vérifiez que Rust est dans votre variable système `%PATH%` comme suit.

Dans CMD Windows, utilisez :

```console
> echo %PATH%
```

Dans PowerShell, utilisez :

```powershell
> echo $env:Path
```

Sur Linux et macOS, utilisez :

```console
$ echo $PATH
```

Si tout cela est correct et que Rust ne fonctionne toujours pas, il existe plusieurs endroits où vous pouvez obtenir de l'aide. Découvrez comment entrer en contact avec d'autres Rustaceans (un surnom amusant que nous nous donnons) sur [la page de la communauté][community].

### Mise à jour et désinstallation

Une fois Rust installé via `rustup`, il est facile de mettre à jour vers une version nouvellement publiée. Depuis votre shell, exécutez le script de mise à jour suivant :

```console
$ rustup update
```

Pour désinstaller Rust et `rustup`, exécutez le script de désinstallation suivant depuis votre shell :

```console
$ rustup self uninstall
```

<!-- Ancien titres. Ne pas supprimer ou les liens peuvent cesser de fonctionner. -->
<a id="local-documentation"></a>

### Lecture de la documentation locale

L'installation de Rust inclut également une copie locale de la documentation afin que vous puissiez la lire hors ligne. Exécutez `rustup doc` pour ouvrir la documentation locale dans votre navigateur.

Chaque fois qu'un type ou une fonction est fourni par la bibliothèque standard et que vous n'êtes pas sûr de son fonctionnement ou de son utilisation, utilisez la documentation de l'interface de programmation d'application (API) pour le découvrir !

<!-- Ancien titres. Ne pas supprimer ou les liens peuvent cesser de fonctionner. -->
<a id="text-editors-and-integrated-development-environments"></a>

### Utilisation des éditeurs de texte et des IDE

Ce livre ne fait aucune supposition sur les outils que vous utilisez pour rédiger du code Rust. Presque n'importe quel éditeur de texte fera l'affaire ! Cependant, de nombreux éditeurs de texte et environnements de développement intégrés (EDI) ont un support intégré pour Rust. Vous pouvez toujours trouver une liste assez actuelle de nombreux éditeurs et EDI sur [la page des outils][tools] du site web de Rust.

### Travailler hors ligne avec ce livre

Dans plusieurs exemples, nous utiliserons des packages Rust au-delà de la bibliothèque standard. Pour traiter ces exemples, vous aurez besoin d'une connexion Internet ou d'avoir téléchargé ces dépendances à l'avance. Pour télécharger les dépendances à l'avance, vous pouvez exécuter les commandes suivantes. (Nous expliquerons ce qu'est `cargo` et ce que fait chacune de ces commandes en détail plus tard.)

```console
$ cargo new get-dependencies
$ cd get-dependencies
$ cargo add rand@0.8.5 trpl@0.2.0
```

Cela mettra en cache les téléchargements de ces packages afin que vous n'ayez pas à les télécharger plus tard. Une fois que vous avez exécuté cette commande, vous n'avez pas besoin de conserver le dossier `get-dependencies`. Si vous avez exécuté cette commande, vous pouvez utiliser le drapeau `--offline` avec toutes les commandes `cargo` dans le reste du livre pour utiliser ces versions mises en cache au lieu d'essayer d'utiliser le réseau.

[otherinstall]: https://forge.rust-lang.org/infra/other-installation-methods.html
[install]: https://www.rust-lang.org/tools/install
[msvc]: https://rust-lang.github.io/rustup/installation/windows-msvc.html
[community]: https://www.rust-lang.org/community
[tools]: https://www.rust-lang.org/tools