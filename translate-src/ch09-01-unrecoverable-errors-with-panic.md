## Erreurs irrécupérables avec `panic!`

Parfois, de mauvaises choses se produisent dans votre code, et vous ne pouvez rien y faire. Dans ces cas-là, Rust dispose de la macro `panic!`. En pratique, il existe deux façons de provoquer une panique : effectuer une action qui fait paniquer notre code (par exemple, accéder à un tableau au-delà de sa fin) ou appeler explicitement la macro `panic!`. Dans les deux cas, nous provoquons une panique dans notre programme. Par défaut, ces paniques affichent un message d’échec, déroulent la pile, nettoient celle-ci et quittent le programme. À l’aide d’une variable d’environnement, vous pouvez également demander à Rust d’afficher la pile d’appels lorsqu’une panique se produit, afin de trouver plus facilement son origine.

> ### Déroulement de la pile ou arrêt immédiat en cas de panique
>
> Par défaut, lorsqu’une panique se produit, le programme commence à _dérouler_ la pile, ce qui signifie que Rust remonte la pile et nettoie les données de chaque fonction rencontrée. Cependant, remonter la pile et la nettoyer demande beaucoup de travail. Rust vous permet donc de choisir l’autre possibilité : l’_arrêt immédiat_, qui met fin au programme sans effectuer de nettoyage.
>
> La mémoire utilisée par le programme devra alors être nettoyée par le système d’exploitation. Si votre projet doit produire un binaire aussi petit que possible, vous pouvez remplacer le déroulement par un arrêt immédiat en cas de panique en ajoutant `panic = 'abort'` aux sections `[profile]` appropriées de votre fichier _Cargo.toml_. Par exemple, pour interrompre le programme en cas de panique en mode release, ajoutez ceci :
>
> ```toml
> [profile.release]
> panic = 'abort'
> ```

Essayons d’appeler `panic!` dans un programme simple :

<Listing file-name="src/main.rs">

```rust,should_panic,panics
{{#rustdoc_include ../listings/ch09-error-handling/no-listing-01-panic/src/main.rs}}
```

</Listing>

Lorsque vous exécutez le programme, vous verrez quelque chose comme ceci :

```console
{{#include ../listings/ch09-error-handling/no-listing-01-panic/output.txt}}
```

L’appel à `panic!` provoque le message d’erreur contenu dans les deux dernières lignes. La première ligne affiche notre message de panique ainsi que l’emplacement dans notre code source où la panique s’est produite : _src/main.rs:2:5_ indique qu’elle se trouve à la deuxième ligne, cinquième caractère de notre fichier _src/main.rs_.

Dans ce cas, la ligne indiquée fait partie de notre code et, si nous nous y rendons, nous voyons l’appel à la macro `panic!`. Dans d’autres cas, l’appel à `panic!` peut se trouver dans du code appelé par notre code, et le nom de fichier et le numéro de ligne indiqués par le message d’erreur correspondront au code de quelqu’un d’autre où la macro `panic!` est appelée, et non à la ligne de notre code qui a fini par provoquer cet appel.

<!-- Old headings. Do not remove or links may break. -->

<a id="using-a-panic-backtrace"></a>

Nous pouvons utiliser la trace d’appels des fonctions à l’origine de l’appel à `panic!` pour trouver la partie de notre code qui cause le problème. Pour comprendre comment utiliser une trace d’appels de `panic!`, examinons un autre exemple et voyons ce qui se passe lorsqu’un appel à `panic!` provient d’une bibliothèque à cause d’un bogue dans notre code, plutôt que d’un appel direct à la macro dans notre code. La Listing 9-1 présente du code qui tente d’accéder à un indice d’un vecteur au-delà de la plage des indices valides.

<Listing number="9-1" file-name="src/main.rs" caption="Tentative d’accès à un élément au-delà de la fin d’un vecteur, ce qui provoquera un appel à `panic!`">

```rust,should_panic,panics
{{#rustdoc_include ../listings/ch09-error-handling/listing-09-01/src/main.rs}}
```

</Listing>

Ici, nous tentons d’accéder au 100e élément de notre vecteur (à l’indice 99, puisque l’indexation commence à zéro), mais le vecteur ne contient que trois éléments. Dans cette situation, Rust déclenche une panique. L’opérateur `[]` est censé renvoyer un élément, mais si vous lui transmettez un indice invalide, aucun élément que Rust pourrait renvoyer ici ne serait correct.

En C, tenter de lire au-delà de la fin d’une structure de données constitue un comportement indéfini. Vous pourriez obtenir ce qui se trouve à l’emplacement mémoire correspondant à cet élément de la structure de données, même si cette mémoire n’appartient pas à cette structure. On appelle cela une _lecture excessive de tampon_ (_buffer overread_), et cela peut entraîner des vulnérabilités de sécurité si un attaquant parvient à manipuler l’indice pour lire des données auxquelles il ne devrait pas avoir accès, stockées après la structure de données.

Pour protéger votre programme contre ce type de vulnérabilité, si vous tentez de lire un élément à un indice inexistant, Rust interrompt l’exécution et refuse de continuer. Essayons pour voir :

```console
{{#include ../listings/ch09-error-handling/listing-09-01/output.txt}}
```

Cette erreur pointe vers la ligne 4 de notre fichier _main.rs_, où nous tentons d’accéder à l’indice 99 du vecteur `v`.

La ligne `note:` nous indique que nous pouvons définir la variable d’environnement `RUST_BACKTRACE` pour obtenir une trace d’appels détaillant exactement ce qui a provoqué l’erreur. Une _trace d’appels_ est une liste de toutes les fonctions appelées jusqu’à ce point. Les traces d’appels fonctionnent dans Rust comme dans d’autres langages : pour les lire, il faut commencer par le haut et poursuivre jusqu’à voir des fichiers que vous avez écrits. C’est là que le problème a pris naissance. Les lignes au-dessus de cet emplacement correspondent au code appelé par votre code ; les lignes en dessous correspondent au code qui a appelé votre code. Ces lignes avant et après peuvent inclure du code Rust de base, du code de la bibliothèque standard ou des crates que vous utilisez. Essayons d’obtenir une trace d’appels en définissant la variable d’environnement `RUST_BACKTRACE` sur n’importe quelle valeur autre que `0`. La Listing 9-2 montre un résultat semblable à celui que vous verrez.

<!-- manual-regeneration
cd listings/ch09-error-handling/listing-09-01
RUST_BACKTRACE=1 cargo run
copy the backtrace output below
check the backtrace number mentioned in the text below the listing
-->

<Listing number="9-2" caption="Trace d’appels générée par un appel à `panic!`, affichée lorsque la variable d’environnement `RUST_BACKTRACE` est définie">

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

Cela fait beaucoup de texte ! Le résultat exact que vous verrez peut varier selon votre système d’exploitation et votre version de Rust. Pour obtenir des traces d’appels contenant ces informations, les symboles de débogage doivent être activés. Ils le sont par défaut lorsque vous utilisez `cargo build` ou `cargo run` sans l’option `--release`, comme c’est le cas ici.

Dans le résultat de la Listing 9-2, la ligne 6 de la trace d’appels pointe vers la ligne de notre projet qui cause le problème : la ligne 4 de _src/main.rs_. Si nous ne voulons pas que notre programme déclenche une panique, nous devons commencer notre enquête à l’emplacement pointé par la première ligne qui mentionne un fichier que nous avons écrit. Dans la Listing 9-1, où nous avons délibérément écrit du code qui déclencherait une panique, il suffit de ne pas demander un élément au-delà de la plage des indices du vecteur pour corriger le problème. Si votre code déclenche une panique à l’avenir, vous devrez déterminer quelle action il effectue et avec quelles valeurs pour la provoquer, puis ce qu’il devrait faire à la place.

Nous reviendrons sur `panic!` et sur les situations où nous devrions ou non utiliser `panic!` pour gérer les conditions d’erreur dans la section [« `panic!` ou non »][to-panic-or-not-to-panic]<!-- ignore --> plus loin dans ce chapitre. Ensuite, nous verrons comment récupérer d’une erreur à l’aide de `Result`.

[to-panic-or-not-to-panic]: ch09-03-to-panic-or-not-to-panic.html#to-panic-or-not-to-panic