## Réfutabilité : Si un motif peut ne pas correspondre

Les motifs se présentent sous deux formes : réfutables et irréfutables. Les motifs qui correspondent à toute valeur possible passée sont _irréfutables_. Un exemple serait `x` dans l'instruction `let x = 5;` car `x` correspond à tout et ne peut donc pas échouer à correspondre. Les motifs qui peuvent échouer à correspondre pour certaines valeurs possibles sont _réfutables_. Un exemple serait `Some(x)` dans l'expression `if let Some(x) = a_value` car si la valeur de la variable `a_value` est `None` plutôt que `Some`, le motif `Some(x)` ne correspondra pas.

Les paramètres de fonction, les instructions `let` et les boucles `for` ne peuvent accepter que des motifs irréfutables car le programme ne peut rien faire de significatif lorsque les valeurs ne correspondent pas. Les expressions `if let` et `while let` ainsi que l'instruction `let...else` acceptent des motifs réfutables et irréfutables, mais le compilateur avertit contre les motifs irréfutables car, par définition, ils sont destinés à gérer les échecs possibles : La fonctionnalité d'une condition repose sur sa capacité à fonctionner différemment selon le succès ou l'échec.

En général, vous ne devriez pas avoir à vous soucier de la distinction entre motifs réfutables et irréfutables ; néanmoins, vous devez être familiarisé avec le concept de réfutabilité afin de pouvoir réagir lorsque vous le voyez dans un message d'erreur. Dans ces cas, vous devrez changer soit le motif, soit la construction avec laquelle vous utilisez le motif, en fonction du comportement attendu du code.

Examinons un exemple de ce qui se passe lorsque nous essayons d'utiliser un motif réfutable là où Rust exige un motif irréfutable et vice versa. La liste 19-8 montre une instruction `let`, mais pour le motif, nous avons spécifié `Some(x)`, un motif réfutable. Comme vous pouvez vous y attendre, ce code ne compilera pas.

<Listing number="19-8" caption="Tentative d'utilisation d'un motif réfutable avec `let`">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-08/src/main.rs:here}}
```

</Listing>

Si `some_option_value` était une valeur `None`, elle échouerait à correspondre au motif `Some(x)`, ce qui signifie que le motif est réfutable. Cependant, l'instruction `let` ne peut accepter qu'un motif irréfutable car il n'y a rien de valide que le code puisse faire avec une valeur `None`. Au moment de la compilation, Rust se plaindra que nous avons essayé d'utiliser un motif réfutable là où un motif irréfutable est requis :

```console
{{#include ../listings/ch19-patterns-and-matching/listing-19-08/output.txt}}
```

Parce que nous n'avons pas couvert (et ne pouvions pas couvrir !) toutes les valeurs valides avec le motif `Some(x)`, Rust produit à juste titre une erreur de compilation.

Si nous avons un motif réfutable là où un motif irréfutable est nécessaire, nous pouvons le corriger en changeant le code qui utilise le motif : Au lieu d'utiliser `let`, nous pouvons utiliser `let...else`. Ensuite, si le motif ne correspond pas, le code dans les accolades gérera la valeur. La liste 19-9 montre comment corriger le code de la liste 19-8.

<Listing number="19-9" caption="Utilisation de `let...else` et d'un bloc avec des motifs réfutables au lieu de `let`">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-09/src/main.rs:here}}
```

</Listing>

Nous avons donné une issue au code ! Ce code est parfaitement valide, bien que cela signifie que nous ne pouvons pas utiliser un motif irréfutable sans recevoir d'avertissement. Si nous donnons à `let...else` un motif qui correspondra toujours, comme `x`, comme montré dans la liste 19-10, le compilateur donnera un avertissement.

<Listing number="19-10" caption="Tentative d'utilisation d'un motif irréfutable avec `let...else`">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-10/src/main.rs:here}}
```

</Listing>

Rust se plaint qu'il n'a pas de sens d'utiliser `let...else` avec un motif irréfutable :

```console
{{#include ../listings/ch19-patterns-and-matching/listing-19-10/output.txt}}
```

Pour cette raison, les branches `match` doivent utiliser des motifs réfutables, sauf pour la dernière branche, qui doit correspondre à toutes les valeurs restantes avec un motif irréfutable. Rust nous permet d'utiliser un motif irréfutable dans un `match` avec une seule branche, mais cette syntaxe n'est pas particulièrement utile et pourrait être remplacée par une instruction `let` plus simple.

Maintenant que vous savez où utiliser des motifs et la différence entre motifs réfutables et irréfutables, examinons toute la syntaxe que nous pouvons utiliser pour créer des motifs.