## Annexe E : Éditions

Dans le chapitre 1, vous avez vu que `cargo new` ajoute un peu de métadonnées à votre fichier _Cargo.toml_ concernant une édition. Cette annexe explique ce que cela signifie !

Le langage et le compilateur Rust ont un cycle de publication de six semaines, ce qui signifie que les utilisateurs reçoivent un flux constant de nouvelles fonctionnalités. D'autres langages de programmation publient des changements plus importants moins fréquemment ; Rust publie des mises à jour plus petites plus régulièrement. Au fil du temps, tous ces petits changements s'accumulent. Mais d'une version à l'autre, il peut être difficile de prendre du recul et de dire : "Wow, entre Rust 1.10 et Rust 1.31, Rust a beaucoup changé !"

Environ tous les trois ans, l'équipe Rust produit une nouvelle _édition_ de Rust. Chaque édition regroupe les fonctionnalités qui ont été intégrées dans un package clair avec une documentation et des outils entièrement mis à jour. Les nouvelles éditions sont publiées dans le cadre du processus de publication habituel de six semaines.

Les éditions servent différents objectifs pour différentes personnes :

- Pour les utilisateurs actifs de Rust, une nouvelle édition regroupe des changements incrémentaux dans un package facile à comprendre.
- Pour les non-utilisateurs, une nouvelle édition signale que des avancées majeures ont été réalisées, ce qui pourrait rendre Rust intéressant à nouveau.
- Pour ceux qui développent Rust, une nouvelle édition fournit un point de ralliement pour le projet dans son ensemble.

Au moment de la rédaction de ce document, quatre éditions de Rust sont disponibles : Rust 2015, Rust 2018, Rust 2021 et Rust 2024. Ce livre est écrit en utilisant les idiomes de l'édition Rust 2024.

La clé `edition` dans _Cargo.toml_ indique quelle édition le compilateur doit utiliser pour votre code. Si la clé n'existe pas, Rust utilise `2015` comme valeur d'édition pour des raisons de compatibilité rétroactive.

Chaque projet peut choisir une édition autre que l'édition par défaut de 2015. Les éditions peuvent contenir des changements incompatibles, comme l'inclusion d'un nouveau mot-clé qui entre en conflit avec des identifiants dans le code. Cependant, à moins que vous ne décidiez d'adopter ces changements, votre code continuera à se compiler même si vous mettez à jour la version du compilateur Rust que vous utilisez.

Toutes les versions du compilateur Rust prennent en charge toute édition qui existait avant la publication de ce compilateur, et elles peuvent lier des crates de n'importe quelles éditions prises en charge ensemble. Les changements d'édition n'affectent que la façon dont le compilateur analyse initialement le code. Par conséquent, si vous utilisez Rust 2015 et que l'une de vos dépendances utilise Rust 2018, votre projet se compilera et pourra utiliser cette dépendance. La situation inverse, où votre projet utilise Rust 2018 et une dépendance utilise Rust 2015, fonctionne également.

Pour être clair : La plupart des fonctionnalités seront disponibles sur toutes les éditions. Les développeurs utilisant n'importe quelle édition de Rust continueront à voir des améliorations à mesure que de nouvelles versions stables sont publiées. Cependant, dans certains cas, principalement lorsque de nouveaux mots-clés sont ajoutés, certaines nouvelles fonctionnalités pourraient n'être disponibles que dans les éditions ultérieures. Vous devrez changer d'édition si vous souhaitez profiter de telles fonctionnalités.

Pour plus de détails, consultez [_The Rust Edition Guide_][edition-guide]. C'est un livre complet qui énumère les différences entre les éditions et explique comment mettre à niveau automatiquement votre code vers une nouvelle édition via `cargo fix`.

[edition-guide]: https://doc.rust-lang.org/stable/edition-guide