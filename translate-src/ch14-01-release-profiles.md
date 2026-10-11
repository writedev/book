## Personnaliser les compilations avec les profils de publication

Dans Rust, les _profils de publication_ sont des profils prédéfinis et personnalisables, avec différentes configurations qui permettent au programmeur de mieux contrôler diverses options de compilation du code. Chaque profil est configuré indépendamment des autres.

Cargo dispose de deux profils principaux : le profil `dev`, utilisé par Cargo lorsque vous exécutez `cargo
build`, et le profil `release`, utilisé par Cargo lorsque vous exécutez `cargo build
--release`. Le profil `dev` est défini avec des valeurs par défaut adaptées au développement, tandis que le profil `release` possède des valeurs par défaut adaptées aux compilations de publication.

Les noms de ces profils vous sont peut-être familiers, car ils apparaissent dans la sortie de vos compilations :

<!-- manual-regeneration
anywhere, run:
cargo build
cargo build --release
and ensure output below is accurate
-->

```console
$ cargo build
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.00s
$ cargo build --release
    Finished `release` profile [optimized] target(s) in 0.32s
```

`dev` et `release` sont les deux profils utilisés par le compilateur.

Cargo définit des paramètres par défaut pour chacun de ces profils, qui s’appliquent si vous n’avez ajouté aucune section `[profile.*]` au fichier _Cargo.toml_ de votre projet. En ajoutant des sections `[profile.*]` pour les profils que vous souhaitez personnaliser, vous pouvez remplacer n’importe quelle partie des paramètres par défaut. Par exemple, voici les valeurs par défaut du paramètre `opt-level` pour les profils `dev` et `release` :

<span class="filename">Nom du fichier : Cargo.toml</span>

```toml
[profile.dev]
opt-level = 0

[profile.release]
opt-level = 3
```

Le paramètre `opt-level` contrôle le niveau d’optimisation que Rust applique à votre code, sur une échelle de 0 à 3. Plus le niveau d’optimisation est élevé, plus la compilation est longue. Ainsi, si vous développez et compilez souvent votre code, vous préférerez moins d’optimisations afin de compiler plus rapidement, même si le code obtenu s’exécute plus lentement. La valeur par défaut de `opt-level` pour `dev` est donc `0`. Lorsque vous êtes prêt à publier votre code, il est préférable de consacrer plus de temps à la compilation. Vous ne compilerez qu’une seule fois en mode publication, mais vous exécuterez de nombreuses fois le programme compilé : ce mode échange donc un temps de compilation plus long contre un code qui s’exécute plus rapidement. C’est pourquoi la valeur par défaut de `opt-level` pour le profil `release` est `3`.

Vous pouvez remplacer un paramètre par défaut en définissant une autre valeur dans _Cargo.toml_. Par exemple, si nous voulons utiliser le niveau d’optimisation 1 dans le profil de développement, nous pouvons ajouter ces deux lignes au fichier _Cargo.toml_ de notre projet :

<span class="filename">Nom du fichier : Cargo.toml</span>

```toml
[profile.dev]
opt-level = 1
```

Ce code remplace la valeur par défaut `0`. Désormais, lorsque nous exécutons `cargo build`, Cargo utilise les paramètres par défaut du profil `dev`, auxquels s’ajoute notre personnalisation de `opt-level`. Comme nous avons défini `opt-level` sur `1`, Cargo applique davantage d’optimisations que par défaut, mais moins que pour une compilation de publication.

Pour consulter la liste complète des options de configuration et des valeurs par défaut de chaque profil, reportez-vous à la [documentation de Cargo](https://doc.rust-lang.org/cargo/reference/profiles.html).