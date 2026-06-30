## Fonctions avancées et fermetures

Cette section explore certaines fonctionnalités avancées liées aux fonctions et aux fermetures, y compris les pointeurs de fonction et le retour de fermetures.

### Pointeurs de fonction

Nous avons parlé de la façon de passer des fermetures aux fonctions ; vous pouvez également passer des fonctions régulières aux fonctions ! Cette technique est utile lorsque vous souhaitez passer une fonction que vous avez déjà définie plutôt que de définir une nouvelle fermeture. Les fonctions se coercent au type `fn` (avec un _f_ en minuscule), à ne pas confondre avec le trait de fermeture `Fn`. Le type `fn` est appelé un _pointeur de fonction_. Passer des fonctions avec des pointeurs de fonction vous permettra d'utiliser des fonctions comme arguments d'autres fonctions.

La syntaxe pour spécifier qu'un paramètre est un pointeur de fonction est similaire à celle des fermetures, comme indiqué dans la liste 20-28, où nous avons défini une fonction `add_one` qui ajoute 1 à son paramètre. La fonction `do_twice` prend deux paramètres : un pointeur de fonction vers n'importe quelle fonction qui prend un paramètre `i32` et retourne un `i32`, et une valeur `i32`. La fonction `do_twice` appelle la fonction `f` deux fois, lui passant la valeur `arg`, puis additionne les deux résultats d'appel de fonction. La fonction `main` appelle `do_twice` avec les arguments `add_one` et `5`.

<Listing number="20-28" file-name="src/main.rs" caption="Utilisation du type `fn` pour accepter un pointeur de fonction comme argument">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-28/src/main.rs}}
```

</Listing>

Ce code affiche `La réponse est : 12`. Nous précisons que le paramètre `f` dans `do_twice` est un `fn` qui prend un paramètre de type `i32` et retourne un `i32`. Nous pouvons ensuite appeler `f` dans le corps de `do_twice`. Dans `main`, nous pouvons passer le nom de la fonction `add_one` comme premier argument à `do_twice`.

Contrairement aux fermetures, `fn` est un type plutôt qu'un trait, donc nous spécifions `fn` comme type de paramètre directement au lieu de déclarer un paramètre de type générique avec l'un des traits `Fn` comme contrainte de trait.

Les pointeurs de fonction implémentent les trois traits de fermeture (`Fn`, `FnMut`, et `FnOnce`), ce qui signifie que vous pouvez toujours passer un pointeur de fonction comme argument pour une fonction qui attend une fermeture. Il est préférable d'écrire des fonctions en utilisant un type générique et l'un des traits de fermeture afin que vos fonctions puissent accepter soit des fonctions, soit des fermetures.

Cela dit, un exemple de situation où vous souhaiteriez uniquement accepter `fn` et non des fermetures est lors de l'interface avec un code externe qui n'a pas de fermetures : les fonctions C peuvent accepter des fonctions en tant qu'arguments, mais C n'a pas de fermetures.

Comme exemple de l'endroit où vous pourriez utiliser soit une fermeture définie en ligne, soit une fonction nommée, examinons une utilisation de la méthode `map` fournie par le trait `Iterator` dans la bibliothèque standard. Pour utiliser la méthode `map` pour transformer un vecteur de nombres en un vecteur de chaînes, nous pourrions utiliser une fermeture, comme dans la liste 20-29.

<Listing number="20-29" caption="Utilisation d'une fermeture avec la méthode `map` pour convertir des nombres en chaînes">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-29/src/main.rs:here}}
```

</Listing>

Ou nous pourrions nommer une fonction comme argument de `map` plutôt que d'utiliser la fermeture. La liste 20-30 montre à quoi cela ressemblerait.

<Listing number="20-30" caption="Utilisation de la fonction `String::to_string` avec la méthode `map` pour convertir des nombres en chaînes">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-30/src/main.rs:here}}
```

</Listing>

Notez que nous devons utiliser la syntaxe entièrement qualifiée dont nous avons parlé dans la section [“Traits avancés”][advanced-traits]<!-- ignore --> car plusieurs fonctions appelées `to_string` sont disponibles.

Ici, nous utilisons la fonction `to_string` définie dans le trait `ToString`, que la bibliothèque standard a implémentée pour tout type qui implémente `Display`.

Rappelons-nous de la section [“Valeurs Enum”][enum-values]<!-- ignore --> du Chapitre 6 que le nom de chaque variante d'énumération que nous définissons devient également une fonction d'initialisation. Nous pouvons utiliser ces fonctions d'initialisation comme pointeurs de fonction qui implémentent les traits de fermeture, ce qui signifie que nous pouvons spécifier les fonctions d'initialisation comme arguments pour les méthodes qui prennent des fermetures, comme le montre la liste 20-31.

<Listing number="20-31" caption="Utilisation d'un initialiseur d'énumération avec la méthode `map` pour créer une instance `Status` à partir de nombres">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-31/src/main.rs:here}}
```

</Listing>

Ici, nous créons des instances `Status::Value` en utilisant chaque valeur `u32` dans la plage sur laquelle `map` est appelé en utilisant la fonction d'initialisation de `Status::Value`. Certaines personnes préfèrent ce style et d'autres préfèrent utiliser des fermetures. Ils se compilent en le même code, donc utilisez le style qui vous semble le plus clair.

### Retourner des fermetures

Les fermetures sont représentées par des traits, ce qui signifie que vous ne pouvez pas retourner des fermetures directement. Dans la plupart des cas où vous pourriez vouloir retourner un trait, vous pouvez plutôt utiliser le type concret qui implémente le trait comme valeur de retour de la fonction. Cependant, vous ne pouvez généralement pas faire cela avec des fermetures car elles n'ont pas de type concret qui est retournable ; vous n'avez pas le droit d'utiliser le pointeur de fonction `fn` comme type de retour si la fermeture capture des valeurs de son environnement, par exemple.

Au lieu de cela, vous utiliserez normalement la syntaxe `impl Trait` que nous avons apprise dans le Chapitre 10. Vous pouvez retourner tout type de fonction, en utilisant `Fn`, `FnOnce`, et `FnMut`. Par exemple, le code dans la liste 20-32 se compilera très bien.

<Listing number="20-32" caption="Retourner une fermeture d'une fonction en utilisant la syntaxe `impl Trait`">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-32/src/lib.rs}}
```

</Listing>

Cependant, comme nous l'avons noté dans la section [“Inférence et annotation des types de fermetures”][closure-types]<!-- ignore --> du Chapitre 13, chaque fermeture est également son propre type distinct. Si vous devez travailler avec plusieurs fonctions qui ont la même signature mais des implémentations différentes, vous devrez utiliser un objet de trait pour elles. Considérez ce qui se passe si vous écrivez du code comme celui montré dans la liste 20-33.

<Listing file-name="src/main.rs" number="20-33" caption="Créer un `Vec<T>` de fermetures définies par des fonctions qui retournent des types `impl Fn`">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-33/src/main.rs}}
```

</Listing>

Ici, nous avons deux fonctions, `returns_closure` et `returns_initialized_closure`, qui retournent toutes deux `impl Fn(i32) -> i32`. Remarquez que les fermetures qu'elles retournent sont différentes, même si elles implémentent le même type. Si nous essayons de compiler cela, Rust nous informe que cela ne fonctionnera pas :

```text
{{#include ../listings/ch20-advanced-features/listing-20-33/output.txt}}
```

Le message d'erreur nous indique que chaque fois que nous retournons un `impl Trait`, Rust crée un type _opaque_ unique, un type dont nous ne pouvons pas voir les détails de ce que Rust construit pour nous, ni deviner le type que Rust générera pour nous. Donc, même si ces fonctions retournent des fermetures qui implémentent le même trait, `Fn(i32) -> i32`, les types opaques que Rust génère pour chacun sont distincts. (C'est similaire à la façon dont Rust produit des types concrets différents pour des blocs asynchrones distincts, même s'ils ont le même type de sortie, comme nous l'avons vu dans la section [“Le type `Pin` et le trait `Unpin`”][future-types]<!-- ignore --> du Chapitre 17.) Nous avons vu une solution à ce problème plusieurs fois maintenant : nous pouvons utiliser un objet de trait, comme dans la liste 20-34.

<Listing number="20-34" caption="Créer un `Vec<T>` de fermetures définies par des fonctions qui retournent `Box<dyn Fn>` afin qu'elles aient le même type">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-34/src/main.rs:here}}
```

</Listing>

Ce code se compilera très bien. Pour plus d'informations sur les objets de trait, consultez la section [“Utiliser des objets de trait pour abstraire le comportement partagé”][trait-objects]<!-- ignore --> du Chapitre 18.

Ensuite, regardons les macros !

[advanced-traits]: ch20-02-advanced-traits.html#advanced-traits  
[enum-values]: ch06-01-defining-an-enum.html#enum-values  
[closure-types]: ch13-01-closures.html#closure-type-inference-and-annotation  
[future-types]: ch17-03-more-futures.html  
[trait-objects]: ch18-02-trait-objects.html  
