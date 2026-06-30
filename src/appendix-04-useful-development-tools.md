## Annexe D : Outils de Développement Utiles

Dans cette annexe, nous parlons de quelques outils de développement utiles fournis par le projet Rust. Nous allons examiner le formatage automatique, des moyens rapides d'appliquer des corrections de warnings, un linter et l'intégration avec des IDE.

### Formatage Automatique avec `rustfmt`

L'outil `rustfmt` reformate votre code selon le style de code de la communauté. De nombreux projets collaboratifs utilisent `rustfmt` pour éviter des débats sur le style à utiliser lors de l'écriture de Rust : Tout le monde formate son code en utilisant l'outil.

Les installations de Rust comprennent `rustfmt` par défaut, donc vous devriez déjà avoir les programmes `rustfmt` et `cargo-fmt` sur votre système. Ces deux commandes sont analogues à `rustc` et `cargo` en ce sens que `rustfmt` permet un contrôle plus précis et `cargo-fmt` comprend les conventions d'un projet utilisant Cargo. Pour formater un projet Cargo, entrez la commande suivante :

```console
$ cargo fmt
```

L'exécution de cette commande reformate tout le code Rust dans le crate actuel. Cela ne devrait changer que le style de code, pas la sémantique du code. Pour plus d'informations sur `rustfmt`, voir [sa documentation][rustfmt].

### Corrigez Votre Code avec `rustfix`

L'outil `rustfix` est inclus avec les installations de Rust et peut corriger automatiquement les avertissements du compilateur qui ont une manière claire de corriger le problème, ce qui est probablement ce que vous souhaitez. Vous avez probablement déjà vu des avertissements du compilateur. Par exemple, considérons ce code :

<span class="filename">Nom du fichier : src/main.rs</span>

```rust
fn main() {
    let mut x = 42;
    println!("{x}");
}
```

Ici, nous définissons la variable `x` comme mutable, mais nous ne la modifions jamais en réalité. Rust nous en avertit :

```console
$ cargo build
   Compilation de myprogram v0.1.0 (file:///projects/myprogram)
avertissement : la variable n'a pas besoin d'être mutable
 --> src/main.rs:2:9
  |
2 |     let mut x = 0;
  |         ----^
  |         |
  |         aide : retirez ce `mut`
  |
  = note : `#[warn(unused_mut)]` par défaut
```

L'avertissement suggère de retirer le mot clé `mut`. Nous pouvons appliquer automatiquement cette suggestion en utilisant l'outil `rustfix` en exécutant la commande `cargo fix` :

```console
$ cargo fix
    Vérification de myprogram v0.1.0 (file:///projects/myprogram)
      Correction de src/main.rs (1 correction)
    Terminé dev [non optimisé + information de débogage] cibles en 0.59s
```

Lorsque nous regardons à nouveau _src/main.rs_, nous verrons que `cargo fix` a modifié le code :

<span class="filename">Nom du fichier : src/main.rs</span>

```rust
fn main() {
    let x = 42;
    println!("{x}");
}
```

La variable `x` est maintenant immuable, et l'avertissement n'apparaît plus.

Vous pouvez également utiliser la commande `cargo fix` pour faire évoluer votre code entre différentes éditions de Rust. Les éditions sont couvertes dans [l'Annexe E][editions]<!-- ignore -->.

### Plus de Lints avec Clippy

L'outil Clippy est une collection de lints pour analyser votre code afin de détecter des erreurs courantes et améliorer votre code Rust. Clippy est inclus dans les installations standard de Rust.

Pour exécuter les lints de Clippy sur n'importe quel projet Cargo, entrez la commande suivante :

```console
$ cargo clippy
```

Par exemple, disons que vous écrivez un programme qui utilise une approximation d'une constante mathématique, comme pi, comme le fait ce programme :

<Listing file-name="src/main.rs">

```rust
fn main() {
    let x = 3.1415;
    let r = 8.0;
    println!("l'aire du cercle est {}", x * r * r);
}
```

</Listing>

L'exécution de `cargo clippy` sur ce projet se traduit par cette erreur :

```text
erreur : valeur approximative de `f{32, 64}::consts::PI` trouvée
 --> src/main.rs:2:13
  |
2 |     let x = 3.1415;
  |             ^^^^^^
  |
  = note : `#[deny(clippy::approx_constant)]` par défaut
  = aide : envisagez d'utiliser la constante directement
  = aide : pour plus d'informations, visitez https://rust-lang.github.io/rust-clippy/master/index.html#approx_constant
```

Cette erreur vous informe que Rust a déjà une constante `PI` plus précise définie, et que votre programme serait plus correct si vous utilisiez cette constante. Vous modifieriez alors votre code pour utiliser la constante `PI`.

Le code suivant ne produit aucune erreur ou avertissement de la part de Clippy :

<Listing file-name="src/main.rs">

```rust
fn main() {
    let x = std::f64::consts::PI;
    let r = 8.0;
    println!("l'aire du cercle est {}", x * r * r);
}
```

</Listing>

Pour plus d'informations sur Clippy, voir [sa documentation][clippy].

### Intégration d'IDE à l'aide de `rust-analyzer`

Pour faciliter l'intégration d'IDE, la communauté Rust recommande d'utiliser [`rust-analyzer`][rust-analyzer]<!-- ignore -->. Cet outil est un ensemble d'utilitaires centrés sur le compilateur qui communiquent via le [Language Server Protocol][lsp]<!-- ignore -->, qui est une spécification pour que les IDE et les langages de programmation communiquent entre eux. Différents clients peuvent utiliser `rust-analyzer`, comme [le plug-in Rust analyzer pour Visual Studio Code][vscode].

Visitez la [page d'accueil du projet `rust-analyzer`][rust-analyzer]<!-- ignore --> pour les instructions d'installation, puis installez le support du serveur de langue dans votre IDE particulier. Votre IDE gagnera des fonctionnalités telles que l'autocomplétion, le saut à la définition et les erreurs en ligne.

[rustfmt]: https://github.com/rust-lang/rustfmt
[editions]: appendix-05-editions.md
[clippy]: https://github.com/rust-lang/rust-clippy
[rust-analyzer]: https://rust-analyzer.github.io
[lsp]: http://langserver.org/
[vscode]: https://marketplace.visualstudio.com/items?itemName=rust-lang.rust-analyzer