## Personnalisation des Builds avec des Profils de Release

En Rust, les _profils de release_ sont des profils préconfigurés et personnalisables avec différentes configurations qui permettent à un programmeur d'avoir plus de contrôle sur diverses options de compilation du code. Chaque profil est configuré indépendamment des autres.

Cargo a deux profils principaux : le profil `dev` que Cargo utilise lorsque vous exécutez `cargo build`, et le profil `release` que Cargo utilise lorsque vous exécutez `cargo build --release`. Le profil `dev` est défini avec de bonnes valeurs par défaut pour le développement, et le profil `release` a de bonnes valeurs par défaut pour les builds de release.

Ces noms de profils peuvent vous sembler familiers à partir de la sortie de vos builds :

```console
$ cargo build
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.00s
$ cargo build --release
    Finished `release` profile [optimized] target(s) in 0.32s
```

Les `dev` et `release` sont les différents profils utilisés par le compilateur.

Cargo a des paramètres par défaut pour chacun des profils qui s'appliquent lorsque vous n'avez pas explicitement ajouté de sections `[profile.*]` dans le fichier _Cargo.toml_ de votre projet. En ajoutant des sections `[profile.*]` pour tout profil que vous souhaitez personnaliser, vous remplacez tout sous-ensemble des paramètres par défaut. Par exemple, voici les valeurs par défaut pour le paramètre `opt-level` pour les profils `dev` et `release` :

<span class="filename">Nom de fichier : Cargo.toml</span>

```toml
[profile.dev]
opt-level = 0

[profile.release]
opt-level = 3
```

Le paramètre `opt-level` contrôle le nombre d'optimisations que Rust appliquera à votre code, avec une plage de 0 à 3. Appliquer plus d'optimisations prolonge le temps de compilation, donc si vous êtes en développement et que vous compilez votre code souvent, vous voudrez moins d'optimisations pour compenser une compilation plus rapide même si le code résultant s'exécute plus lentement. Le `opt-level` par défaut pour `dev` est donc `0`. Lorsque vous êtes prêt à libérer votre code, il est préférable de passer plus de temps en compilation. Vous ne compilerez en mode release qu'une seule fois, mais vous exécuterez le programme compilé plusieurs fois, donc le mode release échange un temps de compilation plus long contre un code qui s'exécute plus rapidement. C'est pourquoi le `opt-level` par défaut pour le profil `release` est `3`.

Vous pouvez remplacer un paramètre par défaut en ajoutant une valeur différente pour celui-ci dans _Cargo.toml_. Par exemple, si nous voulons utiliser le niveau d'optimisation 1 dans le profil de développement, nous pouvons ajouter ces deux lignes dans le fichier _Cargo.toml_ de notre projet :

<span class="filename">Nom de fichier : Cargo.toml</span>

```toml
[profile.dev]
opt-level = 1
```

Ce code remplace le paramètre par défaut de `0`. Maintenant, lorsque nous exécutons `cargo build`, Cargo utilisera les valeurs par défaut pour le profil `dev` plus notre personnalisation pour `opt-level`. Comme nous avons défini `opt-level` à `1`, Cargo appliquera plus d'optimisations que le paramètre par défaut, mais pas autant que dans un build de release.

Pour la liste complète des options de configuration et des valeurs par défaut pour chaque profil, consultez [la documentation de Cargo](https://doc.rust-lang.org/cargo/reference/profiles.html).