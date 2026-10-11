## Annexe E : Les éditions

Au chapitre 1, vous avez vu que `cargo new` ajoute quelques métadonnées concernant une édition à votre fichier _Cargo.toml_. Cette annexe explique ce que cela signifie !

Le langage Rust et son compilateur suivent un cycle de publication de six semaines, ce qui signifie que les utilisateurs bénéficient d’un flux constant de nouvelles fonctionnalités. D’autres langages de programmation publient moins souvent des changements plus importants ; Rust publie des mises à jour plus modestes, mais plus fréquemment. Au bout d’un certain temps, tous ces petits changements finissent par s’accumuler. Mais d’une version à l’autre, il peut être difficile de se retourner et de se dire : « Waouh, entre Rust 1.10 et Rust 1.31, Rust a beaucoup changé ! »

Tous les trois ans environ, l’équipe Rust publie une nouvelle _édition_ de Rust. Chaque édition rassemble les fonctionnalités intégrées au langage dans un ensemble cohérent, accompagné d’une documentation et d’outils entièrement mis à jour. Les nouvelles éditions sont publiées dans le cadre du cycle habituel de six semaines.

Les éditions ont des objectifs différents selon les personnes :

- Pour les utilisateurs actifs de Rust, une nouvelle édition rassemble les changements progressifs dans un ensemble facile à comprendre.
- Pour les personnes qui n’utilisent pas Rust, une nouvelle édition signale l’arrivée d’avancées importantes, qui pourraient inciter à s’intéresser à nouveau à Rust.
- Pour les personnes qui développent Rust, une nouvelle édition fournit un point de ralliement pour l’ensemble du projet.

Au moment de la rédaction de ces lignes, quatre éditions de Rust sont disponibles : Rust 2015, Rust 2018, Rust 2021 et Rust 2024. Ce livre utilise les idiomes de l’édition Rust 2024.

La clé `edition` dans _Cargo.toml_ indique quelle édition le compilateur doit utiliser pour votre code. Si cette clé n’existe pas, Rust utilise `2015` comme valeur d’édition, par souci de compatibilité avec les versions antérieures.

Chaque projet peut choisir une édition différente de l’édition 2015, qui est celle utilisée par défaut. Les éditions peuvent contenir des changements incompatibles, comme l’ajout d’un nouveau mot-clé qui entre en conflit avec des identifiants utilisés dans le code. Toutefois, tant que vous n’optez pas pour ces changements, votre code continuera de compiler, même si vous mettez à niveau la version du compilateur Rust que vous utilisez.

Toutes les versions du compilateur Rust prennent en charge les éditions antérieures à leur publication, et elles peuvent lier ensemble des crates de toutes les éditions prises en charge. Les changements d’édition ne modifient que la manière dont le compilateur analyse initialement le code. Ainsi, si vous utilisez Rust 2015 et que l’une de vos dépendances utilise Rust 2018, votre projet compilera et pourra utiliser cette dépendance. La situation inverse, dans laquelle votre projet utilise Rust 2018 et une dépendance Rust 2015, fonctionne également.

Pour être clair : la plupart des fonctionnalités seront disponibles dans toutes les éditions. Les personnes qui utilisent n’importe quelle édition de Rust continueront de bénéficier d’améliorations à mesure que de nouvelles versions stables seront publiées. Cependant, dans certains cas, notamment lors de l’ajout de nouveaux mots-clés, certaines nouvelles fonctionnalités pourraient n’être disponibles que dans les éditions plus récentes. Vous devrez changer d’édition si vous souhaitez profiter de ces fonctionnalités.

Pour plus de détails, consultez [_The Rust Edition Guide_][edition-guide]. Cet ouvrage complet répertorie les différences entre les éditions et explique comment mettre automatiquement à niveau votre code vers une nouvelle édition à l’aide de `cargo fix`.

[edition-guide]: https://doc.rust-lang.org/stable/edition-guide