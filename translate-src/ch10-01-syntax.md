## Types de données génériques

Nous utilisons les génériques pour créer des définitions d’éléments comme des signatures de fonctions ou des structures, que nous pouvons ensuite utiliser avec de nombreux types de données concrets différents. Commençons par voir comment définir des fonctions, des structures, des énumérations et des méthodes à l’aide de génériques. Nous verrons ensuite comment les génériques influent sur les performances du code.

### Dans les définitions de fonctions

Lorsque nous définissons une fonction qui utilise des génériques, nous plaçons les génériques dans la signature de la fonction, là où nous préciserions habituellement les types de données des paramètres et de la valeur de retour. Cela rend notre code plus flexible et offre davantage de possibilités aux appelants de notre fonction, tout en évitant la duplication de code.

Pour reprendre notre fonction `largest`, le Listing 10-4 montre deux fonctions qui recherchent toutes deux la plus grande valeur d’une tranche. Nous les combinerons ensuite en une seule fonction qui utilise des génériques.

<Listing number="10-4" file-name="src/main.rs" caption="Deux fonctions qui ne diffèrent que par leur nom et les types indiqués dans leurs signatures">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-04/src/main.rs:here}}
```

</Listing>

La fonction `largest_i32` est celle que nous avons extraite dans le Listing 10-3 et qui recherche le plus grand `i32` d’une tranche. La fonction `largest_char` recherche le plus grand `char` d’une tranche. Les corps des fonctions contiennent le même code : éliminons donc cette duplication en introduisant un paramètre de type générique dans une seule fonction.

Pour paramétrer les types dans une nouvelle fonction unique, nous devons nommer le paramètre de type, comme nous le faisons pour les paramètres de valeur d’une fonction. Vous pouvez utiliser n’importe quel identifiant comme nom de paramètre de type. Nous utiliserons toutefois `T`, car, par convention, les noms des paramètres de type en Rust sont courts, souvent réduits à une seule lettre, et suivent la convention de nommage UpperCamelCase. Abréviation de _type_, `T` est le choix par défaut de la plupart des programmeurs Rust.

Lorsque nous utilisons un paramètre dans le corps d’une fonction, nous devons déclarer son nom dans la signature afin que le compilateur sache ce que ce nom désigne. De même, lorsque nous utilisons un nom de paramètre de type dans une signature de fonction, nous devons déclarer ce nom avant de l’utiliser. Pour définir la fonction générique `largest`, nous plaçons les déclarations de noms de types entre chevrons, `<>`, entre le nom de la fonction et la liste de paramètres, comme ceci :

```rust,ignore
fn largest<T>(list: &[T]) -> &T {
```

Nous pouvons lire cette définition ainsi : « La fonction `largest` est générique sur un certain type `T`. » Cette fonction possède un paramètre nommé `list`, qui est une tranche de valeurs de type `T`. La fonction `largest` renverra une référence à une valeur de ce même type `T`.

Le Listing 10-5 présente la définition combinée de la fonction `largest`, qui utilise le type de données générique dans sa signature. Le listing montre également comment nous pouvons appeler cette fonction avec une tranche de valeurs `i32` ou `char`. Remarquez que ce code ne compile pas encore.

<Listing number="10-5" file-name="src/main.rs" caption="La fonction `largest` utilisant des paramètres de type génériques ; ce code ne compile pas encore">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-05/src/main.rs}}
```

</Listing>

Si nous compilons ce code maintenant, nous obtiendrons cette erreur :

```console
{{#include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-05/output.txt}}
```

Le texte d’aide mentionne `std::cmp::PartialOrd`, qui est un trait ; nous parlerons des traits dans la section suivante. Pour l’instant, sachez que cette erreur indique que le corps de `largest` ne fonctionnera pas pour tous les types possibles que `T` pourrait représenter. Comme nous voulons comparer des valeurs de type `T` dans le corps de la fonction, nous ne pouvons utiliser que des types dont les valeurs sont ordonnables. Pour permettre les comparaisons, la bibliothèque standard fournit le trait `std::cmp::PartialOrd`, que vous pouvez implémenter pour des types (voir l’Annexe C pour en savoir plus sur ce trait). Pour corriger le Listing 10-5, nous pouvons suivre la suggestion du texte d’aide et restreindre les types valides pour `T` à ceux qui implémentent `PartialOrd`. Le listing compilera alors, car la bibliothèque standard implémente `PartialOrd` pour `i32` et `char`.

### Dans les définitions de structures

Nous pouvons également définir des structures qui utilisent un paramètre de type générique dans un ou plusieurs champs, à l’aide de la syntaxe `<>`. Le Listing 10-6 définit une structure `Point<T>` destinée à contenir des coordonnées `x` et `y` de n’importe quel type.

<Listing number="10-6" file-name="src/main.rs" caption="Une structure `Point<T>` contenant des valeurs `x` et `y` de type `T`">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-06/src/main.rs}}
```

</Listing>

La syntaxe utilisée pour les génériques dans les définitions de structures est similaire à celle des définitions de fonctions. Nous déclarons d’abord le nom du paramètre de type entre chevrons, juste après le nom de la structure. Ensuite, nous utilisons le type générique dans la définition de la structure, là où nous aurions autrement indiqué des types de données concrets.

Notez que, comme nous n’avons utilisé qu’un seul type générique pour définir `Point<T>`, cette définition indique que la structure `Point<T>` est générique sur un certain type `T`, et que les champs `x` et `y` sont _tous deux_ de ce même type, quel qu’il soit. Si nous créons une instance de `Point<T>` avec des valeurs de types différents, comme dans le Listing 10-7, notre code ne compilera pas.

<Listing number="10-7" file-name="src/main.rs" caption="Les champs `x` et `y` doivent être du même type, car ils utilisent tous deux le même type de données générique `T`.">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-07/src/main.rs}}
```

</Listing>

Dans cet exemple, lorsque nous affectons la valeur entière `5` à `x`, nous indiquons au compilateur que le type générique `T` sera un entier pour cette instance de `Point<T>`. Ensuite, lorsque nous indiquons `4.0` pour `y`, que nous avons défini comme étant du même type que `x`, nous obtenons une erreur d’incompatibilité de types semblable à celle-ci :

```console
{{#include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-07/output.txt}}
```

Pour définir une structure `Point` où `x` et `y` sont tous deux génériques, mais peuvent être de types différents, nous pouvons utiliser plusieurs paramètres de type génériques. Par exemple, dans le Listing 10-8, nous modifions la définition de `Point` afin qu’elle soit générique sur les types `T` et `U`, où `x` est de type `T` et `y` de type `U`.

<Listing number="10-8" file-name="src/main.rs" caption="Une structure générique `Point<T, U>` sur deux types, afin que `x` et `y` puissent être des valeurs de types différents">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-08/src/main.rs}}
```

</Listing>

Toutes les instances de `Point` présentées sont maintenant autorisées ! Vous pouvez utiliser autant de paramètres de type génériques que vous le souhaitez dans une définition, mais en utiliser plus que quelques-uns rend votre code difficile à lire. Si vous constatez que votre code nécessite de nombreux types génériques, cela peut indiquer qu’il faudrait le réorganiser en éléments plus petits.

### Dans les définitions d’énumérations

Comme pour les structures, nous pouvons définir des énumérations dont les variantes contiennent des types de données génériques. Regardons à nouveau l’énumération `Option<T>` fournie par la bibliothèque standard, que nous avons utilisée au Chapitre 6 :

```rust
enum Option<T> {
    Some(T),
    None,
}
```

Cette définition devrait maintenant vous sembler plus claire. Comme vous pouvez le voir, l’énumération `Option<T>` est générique sur le type `T` et possède deux variantes : `Some`, qui contient une valeur de type `T`, et `None`, qui ne contient aucune valeur. En utilisant l’énumération `Option<T>`, nous pouvons exprimer le concept abstrait d’une valeur facultative. Et comme `Option<T>` est générique, nous pouvons utiliser cette abstraction quel que soit le type de la valeur facultative.

Les énumérations peuvent également utiliser plusieurs types génériques. La définition de l’énumération `Result` que nous avons utilisée au Chapitre 9 en est un exemple :

```rust
enum Result<T, E> {
    Ok(T),
    Err(E),
}
```

L’énumération `Result` est générique sur deux types, `T` et `E`, et possède deux variantes : `Ok`, qui contient une valeur de type `T`, et `Err`, qui contient une valeur de type `E`. Cette définition permet d’utiliser facilement l’énumération `Result` partout où une opération peut réussir (en renvoyant une valeur d’un certain type `T`) ou échouer (en renvoyant une erreur d’un certain type `E`). C’est d’ailleurs ce que nous avons utilisé pour ouvrir un fichier dans le Listing 9-3 : `T` correspondait au type `std::fs::File` lorsque le fichier s’ouvrait correctement et `E` au type `std::io::Error` lorsque des problèmes survenaient à l’ouverture du fichier.

Lorsque vous repérez dans votre code des situations où plusieurs définitions de structures ou d’énumérations ne diffèrent que par les types des valeurs qu’elles contiennent, vous pouvez éviter la duplication en utilisant des types génériques.

### Dans les définitions de méthodes

Nous pouvons implémenter des méthodes sur des structures et des énumérations (comme nous l’avons fait au Chapitre 5) et utiliser également des types génériques dans leurs définitions. Le Listing 10-9 montre la structure `Point<T>` que nous avons définie dans le Listing 10-6, avec une méthode nommée `x` implémentée pour cette structure.

<Listing number="10-9" file-name="src/main.rs" caption="Implémentation d’une méthode nommée `x` sur la structure `Point<T>`, qui renverra une référence au champ `x` de type `T`">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-09/src/main.rs}}
```

</Listing>

Ici, nous avons défini sur `Point<T>` une méthode nommée `x` qui renvoie une référence aux données du champ `x`.

Notez que nous devons déclarer `T` juste après `impl` afin de pouvoir utiliser `T` pour indiquer que nous implémentons des méthodes sur le type `Point<T>`. En déclarant `T` comme type générique après `impl`, Rust peut déterminer que le type entre chevrons dans `Point` est un type générique plutôt qu’un type concret. Nous aurions pu choisir un nom différent pour ce paramètre générique de celui déclaré dans la définition de la structure, mais il est conventionnel d’utiliser le même nom. Si vous écrivez une méthode dans un bloc `impl` qui déclare un type générique, cette méthode sera définie pour toute instance du type, quel que soit le type concret qui remplacera le type générique.

Nous pouvons également imposer des contraintes aux types génériques lorsque nous définissons des méthodes sur un type. Nous pourrions, par exemple, implémenter des méthodes uniquement pour les instances de `Point<f32>`, plutôt que pour les instances de `Point<T>` avec n’importe quel type générique. Dans le Listing 10-10, nous utilisons le type concret `f32`, ce qui signifie que nous ne déclarons aucun type après `impl`.

<Listing number="10-10" file-name="src/main.rs" caption="Un bloc `impl` qui s’applique uniquement à une structure dont le paramètre de type générique `T` a un type concret donné">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-10/src/main.rs:here}}
```

</Listing>

Ce code signifie que le type `Point<f32>` disposera d’une méthode `distance_from_origin` ; les autres instances de `Point<T>` où `T` n’est pas de type `f32` ne disposeront pas de cette méthode. Celle-ci mesure la distance entre notre point et le point de coordonnées (0.0, 0.0) et utilise des opérations mathématiques disponibles uniquement pour les nombres à virgule flottante.

Les paramètres de type génériques dans une définition de structure ne sont pas toujours les mêmes que ceux utilisés dans les signatures des méthodes de cette même structure. Le Listing 10-11 utilise les types génériques `X1` et `Y1` pour la structure `Point`, et `X2` et `Y2` pour la signature de la méthode `mixup`, afin de clarifier l’exemple. La méthode crée une nouvelle instance de `Point` avec la valeur `x` du `Point` `self` (de type `X1`) et la valeur `y` du `Point` transmis en argument (de type `Y2`).

<Listing number="10-11" file-name="src/main.rs" caption="Une méthode qui utilise des types génériques différents de ceux de la définition de sa structure">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-11/src/main.rs}}
```

</Listing>

Dans `main`, nous avons défini un `Point` dont `x` est un `i32` (de valeur `5`) et `y` un `f64` (de valeur `10.4`). La variable `p2` est une structure `Point` dont `x` est une tranche de chaîne de caractères (de valeur `"Hello"`) et `y` un `char` (de valeur `c`). Appeler `mixup` sur `p1` avec `p2` comme argument nous donne `p3`, dont `x` sera un `i32`, car `x` provient de `p1`. La variable `p3` aura un `char` pour `y`, car `y` provient de `p2`. L’appel à la macro `println!` affichera `p3.x = 5, p3.y = c`.

Cet exemple a pour but d’illustrer une situation où certains paramètres génériques sont déclarés avec `impl` et d’autres avec la définition de la méthode. Ici, les paramètres génériques `X1` et `Y1` sont déclarés après `impl`, car ils sont associés à la définition de la structure. Les paramètres génériques `X2` et `Y2` sont déclarés après `fn mixup`, car ils ne concernent que la méthode.

### Performances du code utilisant des génériques

Vous vous demandez peut-être si l’utilisation de paramètres de type génériques entraîne un coût à l’exécution. La bonne nouvelle, c’est que l’utilisation de types génériques ne ralentit pas votre programme par rapport à l’utilisation de types concrets.

Rust y parvient en monomorphisant le code qui utilise des génériques au moment de la compilation. La _monomorphisation_ consiste à transformer du code générique en code spécifique en remplaçant les types génériques par les types concrets utilisés lors de la compilation. Dans ce processus, le compilateur effectue l’inverse des étapes que nous avons suivies pour créer la fonction générique dans le Listing 10-5 : il repère tous les endroits où le code générique est appelé et génère du code pour les types concrets utilisés lors de ces appels.

Voyons comment cela fonctionne en utilisant l’énumération générique `Option<T>` de la bibliothèque standard :

```rust
let integer = Some(5);
let float = Some(5.0);
```

Lorsque Rust compile ce code, il effectue une monomorphisation. Au cours de ce processus, le compilateur lit les valeurs qui ont été utilisées dans les instances de `Option<T>` et identifie deux sortes de `Option<T>` : l’une est de type `i32` et l’autre de type `f64`. Il développe ainsi la définition générique de `Option<T>` en deux définitions spécialisées pour `i32` et `f64`, remplaçant ainsi la définition générique par ces définitions spécifiques.

La version monomorphisée du code ressemble à ceci (le compilateur utilise des noms différents des nôtres, que nous employons ici à titre d’illustration) :

<Listing file-name="src/main.rs">

```rust
enum Option_i32 {
    Some(i32),
    None,
}

enum Option_f64 {
    Some(f64),
    None,
}

fn main() {
    let integer = Option_i32::Some(5);
    let float = Option_f64::Some(5.0);
}
```

</Listing>

Le `Option<T>` générique est remplacé par les définitions spécifiques créées par le compilateur. Comme Rust compile le code générique en précisant le type de chaque instance, l’utilisation des génériques n’entraîne aucun coût à l’exécution. Lorsque le code s’exécute, il se comporte exactement comme si nous avions dupliqué chaque définition à la main. La monomorphisation rend les génériques de Rust extrêmement efficaces à l’exécution.