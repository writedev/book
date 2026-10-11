## Installation

La première étape consiste à installer Rust. Nous allons télécharger Rust à l’aide de `rustup`, un outil en ligne de commande permettant de gérer les versions de Rust et les outils associés. Vous aurez besoin d’une connexion Internet pour le téléchargement.

> Remarque : si, pour une raison quelconque, vous préférez ne pas utiliser `rustup`, consultez la page [Autres méthodes d’installation de Rust][otherinstall] pour découvrir d’autres options.

Les étapes suivantes installent la dernière version stable du compilateur Rust. Les garanties de stabilité de Rust assurent que tous les exemples du livre qui compilent continueront de compiler avec les nouvelles versions de Rust. Le résultat peut légèrement différer d’une version à l’autre, car Rust améliore souvent les messages d’erreur et les avertissements. En d’autres termes, toute version stable plus récente de Rust que vous installerez en suivant ces étapes devrait fonctionner comme prévu avec le contenu de ce livre.

> ### Notation de la ligne de commande
>
> Dans ce chapitre et dans tout le livre, nous présenterons des commandes à exécuter dans le terminal. Les lignes que vous devez saisir dans un terminal commencent toutes par `$`. Vous n’avez pas besoin de saisir le caractère `$` ; il s’agit de l’invite de commande qui indique le début de chaque commande. Les lignes qui ne commencent pas par `$` affichent généralement le résultat de la commande précédente. De plus, les exemples propres à PowerShell utiliseront `>` plutôt que `$`.

### Installation de `rustup` sous Linux ou macOS

Si vous utilisez Linux ou macOS, ouvrez un terminal et saisissez la commande suivante :

```console
$ curl --proto '=https' --tlsv1.2 https://sh.rustup.rs -sSf | sh
```

Cette commande télécharge un script et lance l’installation de l’outil `rustup`, qui installe la dernière version stable de Rust. Votre mot de passe peut vous être demandé. Si l’installation réussit, la ligne suivante s’affichera :

```text
Rust is installed now. Great!
```

Vous aurez également besoin d’un _éditeur de liens_, un programme que Rust utilise pour réunir ses fichiers compilés en un seul fichier. Il est probable que vous en ayez déjà un. Si vous rencontrez des erreurs liées à l’éditeur de liens, vous devriez installer un compilateur C, qui en comprend généralement un. Un compilateur C est également utile, car certains paquets Rust courants dépendent de code C et en auront besoin.

Sous macOS, vous pouvez obtenir un compilateur C en exécutant :

```console
$ xcode-select --install
```

Sous Linux, les utilisateurs devraient généralement installer GCC ou Clang, conformément à la documentation de leur distribution. Par exemple, si vous utilisez Ubuntu, vous pouvez installer le paquet `build-essential`.

### Installation de `rustup` sous Windows

Sous Windows, rendez-vous sur [https://www.rust-lang.org/tools/install][install]<!-- ignore
--> et suivez les instructions d’installation de Rust. À un moment de l’installation, vous serez invité à installer Visual Studio. Celui-ci fournit un éditeur de liens et les bibliothèques natives nécessaires à la compilation des programmes. Si vous avez besoin d’aide supplémentaire pour cette étape, consultez
[https://rust-lang.github.io/rustup/installation/windows-msvc.html][msvc]<!--
ignore -->.

Le reste de ce livre utilise des commandes qui fonctionnent à la fois dans _cmd.exe_ et dans PowerShell. En cas de différences particulières, nous préciserons lequel utiliser.

### Dépannage

Pour vérifier que Rust est correctement installé, ouvrez un shell et saisissez cette ligne :

```console
$ rustc --version
```

Vous devriez voir le numéro de version, le hachage du commit et la date du commit de la dernière version stable publiée, au format suivant :

```text
rustc x.y.z (abcabcabc yyyy-mm-dd)
```

Si ces informations s’affichent, Rust est correctement installé ! Dans le cas contraire, vérifiez que Rust figure dans la variable système `%PATH%`, comme suit.

Dans l’invite de commandes Windows, utilisez :

```console
> echo %PATH%
```

Dans PowerShell, utilisez :

```powershell
> echo $env:Path
```

Sous Linux et macOS, utilisez :

```console
$ echo $PATH
```

Si tout est correct et que Rust ne fonctionne toujours pas, vous pouvez obtenir de l’aide à plusieurs endroits. Découvrez comment contacter d’autres Rustacéens (le surnom un peu amusant que nous nous donnons) sur [la page de la communauté][community].

### Mise à jour et désinstallation

Une fois Rust installé à l’aide de `rustup`, il est facile de passer à une nouvelle version dès sa publication. Depuis votre shell, exécutez le script de mise à jour suivant :

```console
$ rustup update
```

Pour désinstaller Rust et `rustup`, exécutez le script de désinstallation suivant depuis votre shell :

```console
$ rustup self uninstall
```

<!-- Old headings. Do not remove or links may break. -->
<a id="local-documentation"></a>

### Consultation de la documentation locale

L’installation de Rust comprend également une copie locale de la documentation, que vous pouvez consulter hors ligne. Exécutez `rustup doc` pour ouvrir la documentation locale dans votre navigateur.

Chaque fois qu’un type ou une fonction est fourni par la bibliothèque standard et que vous ne savez pas ce qu’il fait ou comment l’utiliser, consultez la documentation de l’interface de programmation (API) pour en savoir plus !

<!-- Old headings. Do not remove or links may break. -->
<a id="text-editors-and-integrated-development-environments"></a>

### Utilisation d’éditeurs de texte et d’IDE

Ce livre ne présuppose pas quels outils vous utiliserez pour écrire du code Rust. À peu près n’importe quel éditeur de texte fera l’affaire ! Toutefois, de nombreux éditeurs de texte et environnements de développement intégrés (IDE) prennent en charge Rust. Vous trouverez toujours une liste assez récente de nombreux éditeurs et IDE sur [la page des outils][tools] du site Web de Rust.

### Utilisation de ce livre hors ligne

Dans plusieurs exemples, nous utiliserons des paquets Rust qui ne font pas partie de la bibliothèque standard. Pour réaliser ces exemples, vous devrez disposer d’une connexion Internet ou avoir téléchargé ces dépendances à l’avance. Pour les télécharger à l’avance, vous pouvez exécuter les commandes suivantes. (Nous expliquerons plus en détail ce qu’est `cargo` et le rôle de chacune de ces commandes plus loin.)

<!-- When updating the version of `rand` used, also update the version of
`rand` used in these files so they all match:

* ch02-00-guessing-game-tutorial.md
* ch07-04-bringing-paths-into-scope-with-the-use-keyword.md
* ch14-03-cargo-workspaces.md
-->

```console
$ cargo new get-dependencies
$ cd get-dependencies
$ cargo add rand@0.10.1 trpl@0.2.0
```

Cela mettra en cache les téléchargements de ces paquets, afin que vous n’ayez pas à les télécharger plus tard. Après avoir exécuté cette commande, vous n’avez pas besoin de conserver le dossier `get-dependencies`. Une fois cette commande exécutée, vous pouvez utiliser l’option `--offline` avec toutes les commandes `cargo` du reste du livre afin d’utiliser ces versions mises en cache plutôt que d’essayer d’accéder au réseau.

[otherinstall]: https://forge.rust-lang.org/infra/other-installation-methods.html
[install]: https://www.rust-lang.org/tools/install
[msvc]: https://rust-lang.github.io/rustup/installation/windows-msvc.html
[community]: https://www.rust-lang.org/community
[tools]: https://www.rust-lang.org/tools
