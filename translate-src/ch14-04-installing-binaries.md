<!-- Anciennes rubriques. Ne pas supprimer sinon les liens peuvent être rompus. -->

<a id="installing-binaries-from-cratesio-with-cargo-install"></a>

## Installation de binaires avec `cargo install`

La commande `cargo install` vous permet d'installer et d'utiliser des crates binaires localement. Cela n’est pas destiné à remplacer les packages système ; c’est une manière pratique pour les développeurs Rust d’installer des outils que d’autres ont partagés sur [crates.io](https://crates.io/)<!-- ignore -->. Notez que vous ne pouvez installer que des packages qui ont des cibles binaires. Une _cible binaire_ est le programme exécutable qui est créé si la crate a un fichier _src/main.rs_ ou un autre fichier spécifié comme binaire, contrairement à une cible de bibliothèque qui n’est pas exécutable seule mais qui est adaptée pour être incluse dans d'autres programmes. En général, les crates contiennent des informations dans le fichier README sur le fait qu'une crate est une bibliothèque, a une cible binaire, ou les deux.

Tous les binaires installés avec `cargo install` sont stockés dans le dossier _bin_ de la racine d'installation. Si vous avez installé Rust en utilisant _rustup.rs_ et que vous n'avez pas de configurations personnalisées, ce répertoire sera *$HOME/.cargo/bin*. Assurez-vous que ce répertoire se trouve dans votre `$PATH` pour pouvoir exécuter les programmes que vous avez installés avec `cargo install`.

Par exemple, dans le Chapitre 12, nous avons mentionné qu’il existe une implémentation Rust de l'outil `grep` appelée `ripgrep` pour rechercher des fichiers. Pour installer `ripgrep`, nous pouvons exécuter la commande suivante :

<!-- régénération manuelle
cargo install quelque chose que vous n'avez pas, copiez la sortie pertinente ci-dessous
-->

```console
$ cargo install ripgrep
    Mise à jour de l'index crates.io
  Téléchargement de ripgrep v14.1.1
  1 crate téléchargé (213.6 Ko) en 0.40s
  Installation de ripgrep v14.1.1
--snip--
   Compilation de grep v0.3.2
    Profil `release` terminé [optimisé + informations de débogage] cible(s) en 6.73s
  Installation de ~/.cargo/bin/rg
   Paquet `ripgrep v14.1.1` installé (exécutable `rg`)
```

L'avant-dernière ligne de la sortie montre l'emplacement et le nom du binaire installé, qui dans le cas de `ripgrep` est `rg`. Tant que le répertoire d'installation est dans votre `$PATH`, comme mentionné précédemment, vous pouvez alors exécuter `rg --help` et commencer à utiliser un outil plus rapide et plus Rustique pour rechercher des fichiers !