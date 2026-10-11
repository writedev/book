## Réfutabilité : possibilité qu’un motif échoue à correspondre

Les motifs se répartissent en deux catégories : réfutables et irréfutables. Les motifs qui correspondent à n’importe quelle valeur possible sont _irréfutables_. `x` dans l’instruction `let x = 5;` en est un exemple, car `x` correspond à tout et ne peut donc pas échouer à correspondre. Les motifs qui peuvent échouer à correspondre pour certaines valeurs sont _réfutables_. `Some(x)` dans l’expression `if let Some(x) = a_value` en est un exemple : si la valeur de la variable `a_value` est `None` plutôt que `Some`, le motif `Some(x)` ne correspondra pas.

Les paramètres de fonction, les instructions `let` et les boucles `for` n’acceptent que des motifs irréfutables, car le programme ne peut rien faire de pertinent lorsque les valeurs ne correspondent pas. Les expressions `if let` et `while let`, ainsi que l’instruction `let...else`, acceptent les motifs réfutables et irréfutables, mais le compilateur met en garde contre les motifs irréfutables car, par définition, ces constructions sont destinées à gérer des échecs possibles : une condition est utile parce qu’elle permet d’agir différemment selon qu’elle réussit ou échoue.

En général, vous ne devriez pas avoir à vous préoccuper de la distinction entre les motifs réfutables et irréfutables. Vous devez toutefois connaître le concept de réfutabilité afin de savoir comment réagir lorsque vous le rencontrez dans un message d’erreur. Dans ce cas, vous devrez modifier soit le motif, soit la construction avec laquelle vous l’utilisez, selon le comportement attendu du code.

Examinons un exemple de ce qui se passe lorsque nous essayons d’utiliser un motif réfutable là où Rust exige un motif irréfutable, et inversement. La liste 19-8 montre une instruction `let` dans laquelle nous avons spécifié le motif réfutable `Some(x)`. Comme vous pouvez vous y attendre, ce code ne compilera pas.

<Listing number="19-8" caption="Tentative d’utilisation d’un motif réfutable avec `let`">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-08/src/main.rs:here}}
```

</Listing>

Si `some_option_value` avait la valeur `None`, il ne correspondrait pas au motif `Some(x)`, ce qui signifie que ce motif est réfutable. Cependant, l’instruction `let` n’accepte que les motifs irréfutables, car le code ne peut rien faire de valide avec une valeur `None`. À la compilation, Rust signalera que nous avons essayé d’utiliser un motif réfutable là où un motif irréfutable est requis :

```console
{{#include ../listings/ch19-patterns-and-matching/listing-19-08/output.txt}}
```

Comme le motif `Some(x)` ne couvre pas (et ne pouvait pas couvrir !) toutes les valeurs valides, Rust produit à juste titre une erreur de compilation.

Si nous utilisons un motif réfutable là où un motif irréfutable est nécessaire, nous pouvons corriger le problème en modifiant le code qui utilise le motif : au lieu d’utiliser `let`, nous pouvons utiliser `let...else`. Ainsi, si le motif ne correspond pas, le code entre accolades traitera la valeur. La liste 19-9 montre comment corriger le code de la liste 19-8.

<Listing number="19-9" caption="Utilisation de `let...else` et d’un bloc avec des motifs réfutables à la place de `let`">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-09/src/main.rs:here}}
```

</Listing>

Nous avons prévu une issue pour le code ! Celui-ci est parfaitement valide, même si cela signifie que nous ne pouvons pas utiliser de motif irréfutable sans recevoir un avertissement. Si nous donnons à `let...else` un motif qui correspondra toujours, comme `x`, illustré dans la liste 19-10, le compilateur émettra un avertissement.

<Listing number="19-10" caption="Tentative d’utilisation d’un motif irréfutable avec `let...else`">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-10/src/main.rs:here}}
```

</Listing>

Rust signale qu’il n’est pas logique d’utiliser `let...else` avec un motif irréfutable, car le bloc `else` ne sera jamais exécuté :

```console
{{#include ../listings/ch19-patterns-and-matching/listing-19-10/output.txt}}
```

Pour cette raison, les bras de `match` doivent utiliser des motifs réfutables, à l’exception du dernier bras, qui doit correspondre à toutes les valeurs restantes à l’aide d’un motif irréfutable. Rust nous permet d’utiliser un motif irréfutable dans un `match` ne comportant qu’un seul bras, mais cette syntaxe n’est pas particulièrement utile et pourrait être remplacée par une simple instruction `let`.

Maintenant que vous savez où utiliser les motifs et connaissez la différence entre les motifs réfutables et irréfutables, passons en revue toute la syntaxe que nous pouvons utiliser pour créer des motifs.