## Étendre Cargo avec des commandes personnalisées

Cargo est conçu pour que vous puissiez l’étendre avec de nouvelles sous-commandes sans avoir à le modifier. Si un exécutable situé dans votre `$PATH` s’appelle `cargo-something`, vous pouvez l’exécuter comme s’il s’agissait d’une sous-commande Cargo en lançant `cargo something`. Ces commandes personnalisées sont également répertoriées lorsque vous lancez `cargo --list`. Pouvoir utiliser `cargo install` pour installer des extensions, puis les lancer comme les outils Cargo intégrés, est un avantage très pratique de la conception de Cargo !

## Résumé

Partager du code avec Cargo et [crates.io](https://crates.io/)<!-- ignore --> contribue à rendre l’écosystème Rust utile pour de nombreuses tâches différentes. La bibliothèque standard de Rust est petite et stable, mais les crates sont faciles à partager, à utiliser et à améliorer selon un calendrier différent de celui du langage. N’hésitez pas à partager sur [crates.io](https://crates.io/)<!-- ignore
--> le code qui vous est utile ; il le sera probablement aussi pour quelqu’un d’autre !