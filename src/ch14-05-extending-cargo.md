## Étendre Cargo avec des Commandes Personnalisées

Cargo est conçu pour que vous puissiez l'étendre avec de nouvelles sous-commandes sans avoir à le modifier. Si un binaire dans votre `$PATH` s'appelle `cargo-something`, vous pouvez l'exécuter comme s'il s'agissait d'une sous-commande de Cargo en exécutant `cargo something`. Les commandes personnalisées comme celle-ci sont également répertoriées lorsque vous exécutez `cargo --list`. Pouvoir utiliser `cargo install` pour installer des extensions et les exécuter comme les outils intégrés de Cargo est un avantage très pratique du design de Cargo !

## Résumé

Partager du code avec Cargo et [crates.io](https://crates.io/)<!-- ignore --> fait partie de ce qui rend l'écosystème Rust utile pour de nombreuses tâches différentes. La bibliothèque standard de Rust est petite et stable, mais les crates sont faciles à partager, à utiliser et à améliorer sur une timeline différente de celle du langage. N'hésitez pas à partager le code qui vous est utile sur [crates.io](https://crates.io/)<!-- ignore --> ; il est probable qu'il soit utile à d'autres aussi !