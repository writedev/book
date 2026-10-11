## Annexe D : Outils de développement utiles

Dans cette annexe, nous parlons de quelques outils de développement utiles fournis par le projet Rust. Nous allons voir le formatage automatique, les moyens rapides d’appliquer des corrections aux avertissements, un linter et l’intégration aux IDE.

### Formatage automatique avec `rustfmt`

L’outil `rustfmt` reformate votre code selon le style de code de la communauté. De nombreux projets collaboratifs utilisent `rustfmt` pour éviter les débats sur le style à employer lors de l’écriture de code Rust : tout le monde formate son code avec cet outil.

Les installations de Rust incluent `rustfmt` par défaut. Vous devriez donc déjà avoir les programmes `rustfmt` et `cargo-fmt` sur votre système. Ces deux commandes sont analogues à `rustc` et `cargo` : `rustfmt` offre un contrôle plus précis et `cargo-fmt` comprend les conventions d’un projet qui utilise Cargo. Pour formater un projet Cargo, saisissez la commande suivante :

```console
$ cargo fmt
```

L’exécution de cette commande reformate tout le code Rust de la crate actuelle. Elle ne devrait modifier que le style du code, et non sa sémantique. Pour en savoir plus sur `rustfmt`, consultez [sa documentation][rustfmt].

### Corriger votre code avec `rustfix`

L’outil `rustfix` est inclus dans les installations de Rust et peut corriger automatiquement les avertissements du compilateur lorsqu’une solution évidente au problème correspond probablement à ce que vous souhaitez. Vous avez probablement déjà vu des avertissements du compilateur. Par exemple, considérons le code suivant :

<span class="filename">Nom du fichier : src/main.rs</span>

```rust
fn main() {
    let mut x = 42;
    println!("{x}");
}
```

Ici, nous définissons la variable `x` comme mutable, mais nous ne la modifions jamais. Rust nous avertit de ce problème :

```console
$ cargo build
   Compiling myprogram v0.1.0 (file:///projects/myprogram)
warning: variable does not need to be mutable
 --> src/main.rs:2:9
  |
2 |     let mut x = 0;
  |         ----^
  |         |
  |         help: remove this `mut`
  |
  = note: `#[warn(unused_mut)]` on by default
```

L’avertissement suggère de supprimer le mot-clé `mut`. Nous pouvons appliquer automatiquement cette suggestion à l’aide de l’outil `rustfix`, en exécutant la commande `cargo fix` :

```console
$ cargo fix
    Checking myprogram v0.1.0 (file:///projects/myprogram)
      Fixing src/main.rs (1 fix)
    Finished dev [unoptimized + debuginfo] target(s) in 0.59s
```

En consultant à nouveau _src/main.rs_, nous verrons que `cargo fix` a modifié le code :

<span class="filename">Nom du fichier : src/main.rs</span>

```rust
fn main() {
    let x = 42;
    println!("{x}");
}
```

La variable `x` est désormais immuable et l’avertissement n’apparaît plus.

Vous pouvez également utiliser la commande `cargo fix` pour faire passer votre code d’une édition de Rust à une autre. Les éditions sont présentées à l’[annexe E][editions]<!--
ignore -->.

### Plus de lints avec Clippy

L’outil Clippy est un ensemble de lints qui analysent votre code afin de repérer les erreurs courantes et d’améliorer votre code Rust. Clippy est inclus dans les installations standard de Rust.

Pour exécuter les lints de Clippy sur un projet Cargo, saisissez la commande suivante :

```console
$ cargo clippy
```

Par exemple, supposons que vous écriviez un programme qui utilise une approximation d’une constante mathématique, comme pi, à l’instar de ce programme :

<Listing file-name="src/main.rs">

```rust
fn main() {
    let x = 3.1415;
    let r = 8.0;
    println!("the area of the circle is {}", x * r * r);
}
```

</Listing>

L’exécution de `cargo clippy` sur ce projet produit cette erreur :

```text
error: approximate value of `f{32, 64}::consts::PI` found
 --> src/main.rs:2:13
  |
2 |     let x = 3.1415;
  |             ^^^^^^
  |
  = note: `#[deny(clippy::approx_constant)]` on by default
  = help: consider using the constant directly
  = help: for further information visit https://rust-lang.github.io/rust-clippy/master/index.html#approx_constant
```

Cette erreur vous indique que Rust possède déjà une constante `PI` plus précise et que votre programme serait plus correct si vous utilisiez cette constante. Vous modifieriez alors votre code pour utiliser la constante `PI`.

Le code suivant ne produit aucune erreur ni aucun avertissement de Clippy :

<Listing file-name="src/main.rs">

```rust
fn main() {
    let x = std::f64::consts::PI;
    let r = 8.0;
    println!("the area of the circle is {}", x * r * r);
}
```

</Listing>

Pour en savoir plus sur Clippy, consultez [sa documentation][clippy].

### Intégration aux IDE avec `rust-analyzer`

Pour faciliter l’intégration aux IDE, la communauté Rust recommande d’utiliser [`rust-analyzer`][rust-analyzer]<!-- ignore -->. Cet outil est un ensemble d’utilitaires axés sur le compilateur qui communiquent via le [Language Server Protocol][lsp]<!--
ignore -->, une spécification permettant aux IDE et aux langages de programmation de communiquer entre eux. Différents clients peuvent utiliser `rust-analyzer`, comme [le plug-in Rust analyzer pour Visual Studio Code][vscode].

Consultez la [page d’accueil][rust-analyzer] du projet `rust-analyzer`<!-- ignore -->
pour obtenir les instructions d’installation, puis installez la prise en charge du serveur de langage dans votre IDE. Votre IDE bénéficiera alors de fonctionnalités telles que la complétion automatique, l’accès à la définition et l’affichage des erreurs dans le code.

[rustfmt]: https://github.com/rust-lang/rustfmt
[editions]: appendix-05-editions.md
[clippy]: https://github.com/rust-lang/rust-clippy
[rust-analyzer]: https://rust-analyzer.github.io
[lsp]: http://langserver.org/
[vscode]: https://marketplace.visualstudio.com/items?itemName=rust-lang.rust-analyzer