## Erreurs irrécupérables avec `panic!`

Parfois, des choses mauvaises se produisent dans votre code, et il n'y a rien que vous puissiez y faire. Dans ces cas, Rust dispose de la macro `panic!`. Il existe deux façons de provoquer un panic en pratique : en faisant une action qui amène notre code à paniquer (comme accéder à un tableau au-delà de la fin) ou en appelant explicitement la macro `panic!`. Dans les deux cas, nous provoquons un panic dans notre programme. Par défaut, ces panics imprimeront un message d'échec, dérouleront la pile, nettoieront la pile et quitteront. Via une variable d'environnement, vous pouvez également faire en sorte que Rust affiche la pile d'appels lorsqu'un panic se produit pour faciliter le suivi de la source du panic.

> ### Dérouler la pile ou interrompre en réponse à un panic
>
> Par défaut, lorsqu'un panic se produit, le programme commence à _dérouler_, ce qui signifie que Rust remonte la pile et nettoie les données de chaque fonction rencontrée. Cependant, remonter et nettoyer demande beaucoup de travail. Rust vous permet donc de choisir l'alternative d'_interrompre_ immédiatement, ce qui termine le programme sans nettoyage.
>
> La mémoire que le programme utilisait devra alors être nettoyée par le système d'exploitation. Si, dans votre projet, vous avez besoin de rendre le binaire résultant aussi petit que possible, vous pouvez passer du déroulement à l'interruption lors d'un panic en ajoutant `panic = 'abort'` dans les sections `[profile]` appropriées de votre fichier _Cargo.toml_. Par exemple, si vous souhaitez interrompre lors d'un panic en mode release, ajoutez ceci :
>
> ```toml
> [profile.release]
> panic = 'abort'
> ```

Essayons d'appeler `panic!` dans un programme simple :

<Listing file-name="src/main.rs">

```rust,should_panic,panics
{{#rustdoc_include ../listings/ch09-error-handling/no-listing-01-panic/src/main.rs}}
```

</Listing>

Lorsque vous exécutez le programme, vous verrez quelque chose comme ceci :

```console
{{#include ../listings/ch09-error-handling/no-listing-01-panic/output.txt}}
```

L'appel à `panic!` provoque le message d'erreur contenu dans les deux dernières lignes. La première ligne montre notre message de panic et l'endroit dans notre code source où le panic s'est produit : _src/main.rs:2:5_ indique qu'il s'agit de la deuxième ligne, du cinquième caractère de notre fichier _src/main.rs_.

Dans ce cas, la ligne indiquée fait partie de notre code, et si nous allons à cette ligne, nous voyons l'appel de la macro `panic!`. Dans d'autres cas, l'appel à `panic!` pourrait se trouver dans du code que notre code appelle, et le nom de fichier et le numéro de ligne rapportés par le message d'erreur seront ceux du code d'un tiers où la macro `panic!` est appelée, et non la ligne de notre code qui a finalement conduit à l'appel à `panic!`.

<a id="using-a-panic-backtrace"></a>

Nous pouvons utiliser la backtrace des fonctions dont l'appel à `panic!` provient pour déterminer la partie de notre code qui cause le problème. Pour comprendre comment utiliser une backtrace de `panic!`, regardons un autre exemple et voyons à quoi cela ressemble lorsqu'un appel à `panic!` provient d'une bibliothèque à cause d'un bug dans notre code au lieu de venir de notre code appelant directement la macro. La Listing 9-1 contient un code qui tente d'accéder à un index dans un vecteur au-delà de la plage des index valides.

<Listing number="9-1" file-name="src/main.rs" caption="Tentative d'accès à un élément au-delà de la fin d'un vecteur, ce qui entraînera un appel à `panic!`">

```rust,should_panic,panics
{{#rustdoc_include ../listings/ch09-error-handling/listing-09-01/src/main.rs}}
```

</Listing>

Ici, nous tentons d'accéder au 100e élément de notre vecteur (qui se trouve à l'index 99 car l'indexation commence à zéro), mais le vecteur n'a que trois éléments. Dans cette situation, Rust va paniquer. L'utilisation de `[]` est censée renvoyer un élément, mais si vous passez un index invalide, il n'y a aucun élément que Rust pourrait renvoyer ici qui serait correct.

En C, essayer de lire au-delà de la fin d'une structure de données est un comportement indéfini. Vous pouvez obtenir ce qui se trouve à l'emplacement en mémoire qui correspondrait à cet élément dans la structure de données, même si la mémoire n'appartient pas à cette structure. Cela s'appelle un _buffer overread_ et peut conduire à des vulnérabilités de sécurité si un attaquant parvient à manipuler l'index de manière à lire des données qu'il ne devrait pas pouvoir lire, stockées après la structure de données.

Pour protéger votre programme de ce type de vulnérabilité, si vous essayez de lire un élément à un index qui n'existe pas, Rust arrêtera l'exécution et refusera de continuer. Essayons et voyons :

```console
{{#include ../listings/ch09-error-handling/listing-09-01/output.txt}}
```

Cette erreur pointe vers la ligne 4 de notre _main.rs_ où nous tentons d'accéder à l'index 99 du vecteur dans `v`.

La ligne `note:` nous indique que nous pouvons définir la variable d'environnement `RUST_BACKTRACE` pour obtenir une backtrace de ce qui s'est passé exactement pour causer l'erreur. Une _backtrace_ est une liste de toutes les fonctions qui ont été appelées pour arriver à ce point. Les backtraces dans Rust fonctionnent comme dans d'autres langages : la clé pour lire la backtrace est de partir du haut et de lire jusqu'à ce que vous voyiez des fichiers que vous avez écrits. C'est l'endroit où le problème a pris naissance. Les lignes au-dessus de cet endroit sont du code appelé par votre code ; les lignes en dessous sont du code qui a appelé votre code. Ces lignes avant et après peuvent inclure du code Rust de base, du code de la bibliothèque standard ou des crates que vous utilisez. Essayons d'obtenir une backtrace en définissant la variable d'environnement `RUST_BACKTRACE` sur n'importe quelle valeur sauf `0`. La Listing 9-2 montre une sortie similaire à celle que vous verrez.

<Listing number="9-2" caption="La backtrace générée par un appel à `panic!` affichée lorsque la variable d'environnement `RUST_BACKTRACE` est définie">

```console
$ RUST_BACKTRACE=1 cargo run
thread 'main' panicked at src/main.rs:4:6:
index out of bounds: the len is 3 but the index is 99
stack backtrace:
   0: rust_begin_unwind
             at /rustc/4d91de4e48198da2e33413efdcd9cd2cc0c46688/library/std/src/panicking.rs:692:5
   1: core::panicking::panic_fmt
             at /rustc/4d91de4e48198da2e33413efdcd9cd2cc0c46688/library/core/src/panicking.rs:75:14
   2: core::panicking::panic_bounds_check
             at /rustc/4d91de4e48198da2e33413efdcd9cd2cc0c46688/library/core/src/panicking.rs:273:5
   3: <usize as core::slice::index::SliceIndex<[T]>>::index
             at file:///home/.rustup/toolchains/1.85/lib/rustlib/src/rust/library/core/src/slice/index.rs:274:10
   4: core::slice::index::<impl core::ops::index::Index<I> for [T]>::index
             at file:///home/.rustup/toolchains/1.85/lib/rustlib/src/rust/library/core/src/slice/index.rs:16:9
   5: <alloc::vec::Vec<T,A> as core::ops::index::Index<I>>::index
             at file:///home/.rustup/toolchains/1.85/lib/rustlib/src/rust/library/alloc/src/vec/mod.rs:3361:9
   6: panic::main
             at ./src/main.rs:4:6
   7: core::ops::function::FnOnce::call_once
             at file:///home/.rustup/toolchains/1.85/lib/rustlib/src/rust/library/core/src/ops/function.rs:250:5
note: Some details are omitted, run with `RUST_BACKTRACE=full` for a verbose backtrace.
```

</Listing>

C'est beaucoup de sorties ! La sortie exacte que vous voyez peut être différente selon votre système d'exploitation et votre version de Rust. Pour obtenir des backtraces avec ces informations, les symboles de débogage doivent être activés. Les symboles de débogage sont activés par défaut lors de l'utilisation de `cargo build` ou `cargo run` sans le drapeau `--release`, comme nous l'avons fait ici.

Dans la sortie de la Listing 9-2, la ligne 6 de la backtrace pointe vers la ligne de notre projet qui cause le problème : la ligne 4 de _src/main.rs_. Si nous ne voulons pas que notre programme panique, nous devrions commencer notre enquête à l'emplacement indiqué par la première ligne mentionnant un fichier que nous avons écrit. Dans la Listing 9-1, où nous avons délibérément écrit un code qui provoquerait un panic, la solution pour éviter le panic est de ne pas demander un élément au-delà de la plage des index du vecteur. Lorsque votre code panique à l'avenir, vous devrez déterminer quelle action le code effectue avec quelles valeurs pour provoquer le panic et ce que le code devrait faire à la place.

Nous reviendrons à `panic!` et aux moments où nous devrions et ne devrions pas utiliser `panic!` pour gérer les conditions d'erreur dans la section ["À `panic!` ou pas à `panic!`"]<!-- ignore --> plus loin dans ce chapitre. Ensuite, nous examinerons comment récupérer d'une erreur à l'aide de `Result`.