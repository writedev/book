## Fonctions et fermetures avancées

Cette section explore quelques fonctionnalités avancées liées aux fonctions et aux fermetures, notamment les pointeurs de fonction et le renvoi de fermetures.

### Pointeurs de fonction

Nous avons vu comment passer des fermetures à des fonctions ; vous pouvez également passer des fonctions ordinaires à des fonctions ! Cette technique est utile lorsque vous souhaitez passer une fonction que vous avez déjà définie plutôt que de définir une nouvelle fermeture. Les fonctions sont converties en type `fn` (avec un _f_ minuscule), à ne pas confondre avec le trait de fermeture `Fn`. Le type `fn` est appelé _pointeur de fonction_. Passer des fonctions au moyen de pointeurs de fonction vous permet d’utiliser des fonctions comme arguments d’autres fonctions.

La syntaxe permettant de spécifier qu’un paramètre est un pointeur de fonction ressemble à celle des fermetures, comme le montre le listing 20-28, où nous avons défini une fonction `add_one` qui ajoute 1 à son paramètre. La fonction `do_twice` prend deux paramètres : un pointeur de fonction vers n’importe quelle fonction qui prend un paramètre `i32` et renvoie un `i32`, et une valeur `i32`. La fonction `do_twice` appelle deux fois la fonction `f`, en lui passant la valeur `arg`, puis additionne les résultats des deux appels. La fonction `main` appelle `do_twice` avec les arguments `add_one` et `5`.

<Listing number="20-28" file-name="src/main.rs" caption="Utiliser le type `fn` pour accepter un pointeur de fonction comme argument">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-28/src/main.rs}}
```

</Listing>

Ce code affiche `The answer is: 12`. Nous précisons que le paramètre `f` de `do_twice` est une fonction `fn` qui prend un paramètre de type `i32` et renvoie un `i32`. Nous pouvons ensuite appeler `f` dans le corps de `do_twice`. Dans `main`, nous pouvons passer le nom de la fonction `add_one` comme premier argument à `do_twice`.

Contrairement aux fermetures, `fn` est un type plutôt qu’un trait ; nous spécifions donc directement `fn` comme type du paramètre, au lieu de déclarer un paramètre de type générique assorti d’une borne de trait utilisant l’un des traits `Fn`.

Les pointeurs de fonction implémentent les trois traits de fermeture (`Fn`, `FnMut` et `FnOnce`), ce qui signifie que vous pouvez toujours passer un pointeur de fonction comme argument à une fonction qui attend une fermeture. Il est préférable d’écrire les fonctions avec un type générique et l’un des traits de fermeture afin qu’elles puissent accepter aussi bien des fonctions que des fermetures.

Cela dit, un cas où vous voudriez n’accepter que `fn` et pas les fermetures est celui de l’interfaçage avec du code externe qui ne prend pas en charge les fermetures : les fonctions C peuvent accepter des fonctions comme arguments, mais C ne dispose pas de fermetures.

Pour voir un exemple d’utilisation d’une fermeture définie directement ou d’une fonction nommée, examinons l’utilisation de la méthode `map` fournie par le trait `Iterator` de la bibliothèque standard. Pour utiliser la méthode `map` afin de transformer un vecteur de nombres en un vecteur de chaînes de caractères, nous pourrions utiliser une fermeture, comme dans le listing 20-29.

<Listing number="20-29" caption="Utiliser une fermeture avec la méthode `map` pour convertir des nombres en chaînes de caractères">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-29/src/main.rs:here}}
```

</Listing>

Nous pourrions aussi nommer une fonction comme argument de `map` au lieu d’utiliser une fermeture. Le listing 20-30 montre à quoi cela ressemblerait.

<Listing number="20-30" caption="Utiliser la fonction `String::to_string` avec la méthode `map` pour convertir des nombres en chaînes de caractères">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-30/src/main.rs:here}}
```

</Listing>

Remarquez que nous devons utiliser la syntaxe complète dont nous avons parlé dans la section [« Traits avancés »][advanced-traits]<!-- ignore -->, car plusieurs fonctions portent le nom `to_string`.

Ici, nous utilisons la fonction `to_string` définie dans le trait `ToString`, que la bibliothèque standard a implémenté pour tout type qui implémente `Display`.

Rappelez-vous, d’après la section [« Valeurs d’énumération »][enum-values]<!-- ignore --> du chapitre 6, que le nom de chaque variante d’énumération que nous définissons devient également une fonction d’initialisation. Nous pouvons utiliser ces fonctions d’initialisation comme des pointeurs de fonction qui implémentent les traits de fermeture, ce qui signifie que nous pouvons spécifier ces fonctions comme arguments de méthodes qui prennent des fermetures, comme le montre le listing 20-31.

<Listing number="20-31" caption="Utiliser une fonction d’initialisation d’énumération avec la méthode `map` pour créer une instance de `Status` à partir de nombres">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-31/src/main.rs:here}}
```

</Listing>

Ici, nous créons des instances `Status::Value` en utilisant chaque valeur `u32` de la plage sur laquelle `map` est appelée, grâce à la fonction d’initialisation de `Status::Value`. Certaines personnes préfèrent ce style, tandis que d’autres préfèrent utiliser des fermetures. Les deux styles produisent le même code compilé ; utilisez donc celui qui vous semble le plus clair.

### Renvoyer des fermetures

Les fermetures sont représentées par des traits, ce qui signifie que vous ne pouvez pas renvoyer directement des fermetures. Dans la plupart des cas où vous pourriez vouloir renvoyer un trait, vous pouvez plutôt utiliser le type concret qui implémente ce trait comme valeur de retour de la fonction. Toutefois, avec les fermetures, ce n’est généralement pas possible, car elles n’ont pas de type concret pouvant être renvoyé ; par exemple, vous ne pouvez pas utiliser le pointeur de fonction `fn` comme type de retour si la fermeture capture des valeurs de son environnement.

À la place, vous utiliserez généralement la syntaxe `impl Trait` présentée au chapitre 10. Vous pouvez renvoyer n’importe quel type de fonction en utilisant `Fn`, `FnOnce` et `FnMut`. Par exemple, le code du listing 20-32 se compile sans problème.

<Listing number="20-32" caption="Renvoyer une fermeture depuis une fonction avec la syntaxe `impl Trait`">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-32/src/lib.rs}}
```

</Listing>

Cependant, comme nous l’avons indiqué dans la section [« Inférence et annotation des types de fermeture »][closure-types]<!-- ignore --> du chapitre 13, chaque fermeture est également son propre type distinct. Si vous devez travailler avec plusieurs fonctions ayant la même signature, mais des implémentations différentes, vous devrez utiliser un objet de trait. Voyons ce qui se passe si vous écrivez du code comme celui du listing 20-33.

<Listing file-name="src/main.rs" number="20-33" caption="Créer un `Vec<T>` de fermetures définies par des fonctions qui renvoient des types `impl Fn`">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-33/src/main.rs}}
```

</Listing>

Nous avons ici deux fonctions, `returns_closure` et `returns_initialized_closure`, qui renvoient toutes deux `impl Fn(i32) -> i32`. Remarquez que les fermetures qu’elles renvoient sont différentes, même si elles implémentent le même type. Si nous essayons de compiler ce code, Rust nous indique que cela ne fonctionnera pas :

```text
{{#include ../listings/ch20-advanced-features/listing-20-33/output.txt}}
```

Le message d’erreur nous indique que chaque fois que nous renvoyons un `impl Trait`, Rust crée un type _opaque_ unique, dont nous ne pouvons pas voir les détails de ce que Rust construit pour nous, et dont nous ne pouvons pas non plus deviner le type que Rust générera afin de l’écrire nous-mêmes. Ainsi, même si ces fonctions renvoient des fermetures qui implémentent le même trait, `Fn(i32) -> i32`, les types opaques générés par Rust sont distincts pour chacune d’elles. (C’est similaire à la façon dont Rust produit des types concrets différents pour des blocs async distincts, même lorsqu’ils ont le même type de sortie, comme nous l’avons vu dans [« Le type `Pin` et le trait `Unpin` »][future-types]<!-- ignore --> au chapitre 17.) Nous avons déjà rencontré plusieurs fois une solution à ce problème : utiliser un objet de trait, comme dans le listing 20-34.

<Listing number="20-34" caption="Créer un `Vec<T>` de fermetures définies par des fonctions qui renvoient `Box<dyn Fn>` afin qu’elles aient le même type">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-34/src/main.rs:here}}
```

</Listing>

Ce code se compile sans problème. Pour en savoir plus sur les objets de trait, consultez la section [« Utiliser les objets de trait pour abstraire un comportement partagé »][trait-objects]<!-- ignore --> du chapitre 18.

Passons maintenant aux macros !

[advanced-traits]: ch20-02-advanced-traits.html#advanced-traits
[enum-values]: ch06-01-defining-an-enum.html#enum-values
[closure-types]: ch13-01-closures.html#closure-type-inference-and-annotation
[future-types]: ch17-03-more-futures.html
[trait-objects]: ch18-02-trait-objects.html