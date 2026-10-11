<!-- Old headings. Do not remove or links may break. -->

<a id="installing-binaries-from-cratesio-with-cargo-install"></a>

## Installer des binaires avec `cargo install`

La commande `cargo install` vous permet d’installer et d’utiliser localement des crates binaires. Elle n’a pas vocation à remplacer les paquets système ; elle offre plutôt aux développeurs Rust un moyen pratique d’installer des outils partagés par d’autres sur [crates.io](https://crates.io/)<!-- ignore -->. Notez que vous ne pouvez installer que les paquets qui possèdent des cibles binaires. Une _cible binaire_ est le programme exécutable créé si la crate comporte un fichier _src/main.rs_ ou un autre fichier spécifié comme binaire, contrairement à une cible de bibliothèque, qui ne peut pas être exécutée seule, mais peut être incluse dans d’autres programmes. En général, les crates indiquent dans leur fichier README s’il s’agit d’une bibliothèque, si elles possèdent une cible binaire, ou les deux.

Tous les binaires installés avec `cargo install` sont stockés dans le dossier _bin_ de la racine d’installation. Si vous avez installé Rust à l’aide de _rustup.rs_ et que vous n’avez pas de configuration personnalisée, ce répertoire est *$HOME/.cargo/bin*. Assurez-vous que ce répertoire figure dans votre `$PATH` afin de pouvoir exécuter les programmes installés avec `cargo install`.

Par exemple, au chapitre 12, nous avons mentionné qu’il existe une implémentation en Rust de l’outil `grep`, appelée `ripgrep`, qui permet de rechercher des fichiers. Pour installer `ripgrep`, vous pouvez exécuter la commande suivante :

<!-- manual-regeneration
cargo install something you don't have, copy relevant output below
-->

```console
$ cargo install ripgrep
    Updating crates.io index
  Downloaded ripgrep v14.1.1
  Downloaded 1 crate (213.6 KB) in 0.40s
  Installing ripgrep v14.1.1
--snip--
   Compiling grep v0.3.2
    Finished `release` profile [optimized + debuginfo] target(s) in 6.73s
  Installing ~/.cargo/bin/rg
   Installed package `ripgrep v14.1.1` (executable `rg`)
```

L’avant-dernière ligne de la sortie indique l’emplacement et le nom du binaire installé, qui est `rg` dans le cas de `ripgrep`. Tant que le répertoire d’installation figure dans votre `$PATH`, comme indiqué précédemment, vous pouvez ensuite exécuter `rg --help` et commencer à utiliser un outil de recherche de fichiers plus rapide et plus « Rust » !