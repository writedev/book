## Types de données génériques

Nous utilisons les génériques pour créer des définitions pour des éléments comme les signatures de fonction ou les structures, que nous pouvons ensuite utiliser avec de nombreux types de données concrets différents. Regardons d'abord comment définir des fonctions, structures, énumérations et méthodes en utilisant des génériques. Ensuite, nous discuterons de la manière dont les génériques affectent la performance du code.

### Dans les définitions de fonctions

Lors de la définition d'une fonction qui utilise des génériques, nous plaçons les génériques dans la signature de la fonction là où nous spécifions généralement les types de données des paramètres et de la valeur de retour. Cela rend notre code plus flexible et fournit plus de fonctionnalités aux appelants de notre fonction tout en empêchant la duplication de code.

En poursuivant avec notre fonction `largest`, l'illustration 10-4 montre deux fonctions qui trouvent toutes deux la valeur la plus grande dans un tableau. Nous allons ensuite combiner ces deux fonctions en une seule qui utilise des génériques.

<Illustration numéro="10-4" nom de fichier="src/main.rs" légende="Deux fonctions qui diffèrent seulement par leurs noms et les types dans leurs signatures">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-04/src/main.rs:here}}
```

</Illustration>

La fonction `largest_i32` est celle que nous avons extraite dans l'illustration 10-3 qui trouve le plus grand `i32` dans un tableau. La fonction `largest_char` trouve le plus grand `char` dans un tableau. Les corps des fonctions contiennent le même code, éliminons donc la duplication en introduisant un paramètre de type générique dans une seule fonction.

Pour paramétrer les types dans une nouvelle fonction, nous devons nommer le paramètre de type, tout comme nous le faisons pour les paramètres de valeur d'une fonction. Vous pouvez utiliser n'importe quel identifiant comme nom de paramètre de type. Mais nous utiliserons `T` car, par convention, les noms de paramètres de type en Rust sont courts, souvent juste une lettre, et la convention de nommage des types en Rust est UpperCamelCase. Abrégé pour _type_, `T` est le choix par défaut de la plupart des programmeurs Rust.

Lorsque nous utilisons un paramètre dans le corps de la fonction, nous devons déclarer le nom du paramètre dans la signature afin que le compilateur sache ce que ce nom signifie. De même, lorsque nous utilisons un nom de paramètre de type dans une signature de fonction, nous devons déclarer le nom du paramètre de type avant de l'utiliser. Pour définir la fonction générique `largest`, nous plaçons les déclarations de noms de type à l'intérieur des chevrons, `<>`, entre le nom de la fonction et la liste des paramètres, comme ceci :

```rust,ignore
fn largest<T>(list: &[T]) -> &T {
```

Nous lisons cette définition comme "La fonction `largest` est générique sur un certain type `T`." Cette fonction a un paramètre nommé `list`, qui est un tableau de valeurs de type `T`. La fonction `largest` renverra une référence à une valeur du même type `T`.

L'illustration 10-5 montre la définition combinée de la fonction `largest` utilisant le type de données générique dans sa signature. L'illustration montre également comment nous pouvons appeler la fonction avec soit un tableau de valeurs `i32`, soit des valeurs `char`. Notez que ce code ne compilera pas encore.

<Illustration numéro="10-5" nom de fichier="src/main.rs" légende="La fonction `largest` utilisant des paramètres de type génériques ; cela ne compile pas encore">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-05/src/main.rs}}
```

</Illustration>

Si nous compilons ce code maintenant, nous obtiendrons cette erreur :

```console
{{#include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-05/output.txt}}
```

Le texte d'aide mentionne `std::cmp::PartialOrd`, qui est un trait, et nous allons parler des traits dans la section suivante. Pour l'instant, sachez que cette erreur indique que le corps de `largest` ne fonctionnera pas pour tous les types possibles que `T` pourrait être. Étant donné que nous voulons comparer des valeurs de type `T` dans le corps, nous ne pouvons utiliser que des types dont les valeurs peuvent être ordonnées. Pour permettre les comparaisons, la bibliothèque standard a le trait `std::cmp::PartialOrd` que vous pouvez implémenter sur des types (voir l'Annexe C pour plus d'informations sur ce trait). Pour corriger l'illustration 10-5, nous pouvons suivre la suggestion du texte d'aide et restreindre les types valides pour `T` uniquement à ceux qui implémentent `PartialOrd`. L'illustration compilera alors, car la bibliothèque standard implémente `PartialOrd` sur `i32` et `char`.

### Dans les définitions de structures

Nous pouvons également définir des structures pour utiliser un paramètre de type générique dans un ou plusieurs champs en utilisant la syntaxe `<>`. L'illustration 10-6 définit une structure `Point<T>` pour contenir des valeurs de coordonnée `x` et `y` de n'importe quel type.

<Illustration numéro="10-6" nom de fichier="src/main.rs" légende="Une structure `Point<T>` qui contient des valeurs `x` et `y` de type `T`">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-06/src/main.rs}}
```

</Illustration>

La syntaxe pour utiliser des génériques dans les définitions de structures est similaire à celle utilisée dans les définitions de fonctions. Tout d'abord, nous déclarons le nom du paramètre de type à l'intérieur des chevrons juste après le nom de la structure. Ensuite, nous utilisons le type générique dans la définition de la structure là où nous spécifierions autrement des types de données concrets.

Notez que, comme nous avons utilisé un seul type générique pour définir `Point<T>`, cette définition dit que la structure `Point<T>` est générique sur un certain type `T`, et les champs `x` et `y` sont _tous deux_ de ce même type, quel que soit ce type. Si nous créons une instance de `Point<T>` qui a des valeurs de types différents, comme dans l'illustration 10-7, notre code ne compilera pas.

<Illustration numéro="10-7" nom de fichier="src/main.rs" légende="Les champs `x` et `y` doivent être du même type car les deux ont le même type de données générique `T`.">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-07/src/main.rs}}
```

</Illustration>

Dans cet exemple, lorsque nous assignons la valeur entière `5` à `x`, nous informons le compilateur que le type générique `T` sera un entier pour cette instance de `Point<T>`. Ensuite, lorsque nous spécifions `4.0` pour `y`, que nous avons défini pour avoir le même type que `x`, nous obtiendrons une erreur de type de correspondance comme ceci :

```console
{{#include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-07/output.txt}}
```

Pour définir une structure `Point` où `x` et `y` sont tous deux génériques mais peuvent avoir des types différents, nous pouvons utiliser plusieurs paramètres de type générique. Par exemple, dans l'illustration 10-8, nous changeons la définition de `Point` pour être générique sur les types `T` et `U` où `x` est de type `T` et `y` est de type `U`.

<Illustration numéro="10-8" nom de fichier="src/main.rs" légende="Une `Point<T, U>` générique sur deux types afin que `x` et `y` puissent être des valeurs de types différents">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-08/src/main.rs}}
```

</Illustration>

Maintenant, toutes les instances de `Point` montrées sont autorisées ! Vous pouvez utiliser autant de paramètres de type générique dans une définition que vous le souhaitez, mais en utiliser plus d'un certain nombre rend votre code difficile à lire. Si vous trouvez que vous avez besoin de nombreux types génériques dans votre code, cela pourrait indiquer que votre code a besoin d'une restructuration en petites parties.

### Dans les définitions d'énumérations

Comme nous l'avons fait avec les structures, nous pouvons définir des énumérations pour contenir des types de données génériques dans leurs variantes. Jetons un autre coup d'œil à l'énumération `Option<T>` que la bibliothèque standard fournit, que nous avons utilisée dans le chapitre 6 :

```rust
enum Option<T> {
    Some(T),
    None,
}
```

Cette définition devrait maintenant avoir plus de sens pour vous. Comme vous pouvez le voir, l'énumération `Option<T>` est générique sur le type `T` et a deux variantes : `Some`, qui contient une valeur de type `T`, et une variante `None` qui ne contient aucune valeur. En utilisant l'énumération `Option<T>`, nous pouvons exprimer le concept abstrait d'une valeur optionnelle, et comme `Option<T>` est générique, nous pouvons utiliser cette abstraction peu importe le type de la valeur optionnelle.

Les énumérations peuvent également utiliser plusieurs types génériques. La définition de l'énumération `Result` que nous avons utilisée dans le chapitre 9 est un exemple :

```rust
enum Result<T, E> {
    Ok(T),
    Err(E),
}
```

L'énumération `Result` est générique sur deux types, `T` et `E`, et a deux variantes : `Ok`, qui contient une valeur de type `T`, et `Err`, qui contient une valeur de type `E`. Cette définition rend pratique l'utilisation de l'énumération `Result` partout où nous avons une opération qui peut réussir (retourner une valeur d'un certain type `T`) ou échouer (retourner une erreur d'un certain type `E`). En fait, c'est ce que nous avons utilisé pour ouvrir un fichier dans l'illustration 9-3, où `T` a été rempli avec le type `std::fs::File` lorsque le fichier a été ouvert avec succès et `E` a été rempli avec le type `std::io::Error` lorsqu'il y a eu des problèmes d'ouverture du fichier.

Lorsque vous reconnaissez des situations dans votre code avec plusieurs définitions de structures ou d'énumérations qui ne diffèrent que par les types de valeurs qu'elles contiennent, vous pouvez éviter la duplication en utilisant des types génériques à la place.

### Dans les définitions de méthodes

Nous pouvons implémenter des méthodes sur des structures et des énumérations (comme nous l'avons fait dans le chapitre 5) et utiliser des types génériques dans leurs définitions également. L'illustration 10-9 montre la structure `Point<T>` que nous avons définie dans l'illustration 10-6 avec une méthode nommée `x` implémentée sur elle.

<Illustration numéro="10-9" nom de fichier="src/main.rs" légende="Implémentation d'une méthode nommée `x` sur la structure `Point<T>` qui renverra une référence au champ `x` de type `T`">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-09/src/main.rs}}
```

</Illustration>

Ici, nous avons défini une méthode nommée `x` sur `Point<T>` qui renvoie une référence aux données dans le champ `x`.

Notez que nous devons déclarer `T` juste après `impl` afin que nous puissions utiliser `T` pour spécifier que nous implémentons des méthodes sur le type `Point<T>`. En déclarant `T` comme un type générique après `impl`, Rust peut identifier que le type dans les chevrons dans `Point` est un type générique plutôt qu'un type concret. Nous aurions pu choisir un nom différent pour ce paramètre générique que le paramètre générique déclaré dans la définition de la structure, mais utiliser le même nom est conventionnel. Si vous écrivez une méthode à l'intérieur d'un `impl` qui déclare un type générique, cette méthode sera définie sur n'importe quelle instance du type, peu importe quel type concret finit par remplacer le type générique.

Nous pouvons également spécifier des contraintes sur les types génériques lors de la définition de méthodes sur le type. Nous pourrions, par exemple, implémenter des méthodes uniquement sur des instances de `Point<f32>` plutôt que sur des instances de `Point<T>` avec n'importe quel type générique. Dans l'illustration 10-10, nous utilisons le type concret `f32`, ce qui signifie que nous ne déclarons aucun type après `impl`.

<Illustration numéro="10-10" nom de fichier="src/main.rs" légende="Un bloc `impl` qui ne s'applique qu'à une structure avec un type concret particulier pour le paramètre de type générique `T`">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-10/src/main.rs:here}}
```

</Illustration>

Ce code signifie que le type `Point<f32>` aura une méthode `distance_from_origin` ; d'autres instances de `Point<T>` où `T` n'est pas de type `f32` n'auront pas cette méthode définie. La méthode mesure à quelle distance notre point est du point aux coordonnées (0.0, 0.0) et utilise des opérations mathématiques qui ne sont disponibles que pour les types flottants.

Les paramètres de type générique dans une définition de structure ne sont pas toujours les mêmes que ceux que vous utilisez dans les signatures de méthode de cette même structure. L'illustration 10-11 utilise les types génériques `X1` et `Y1` pour la structure `Point` et `X2` et `Y2` pour la signature de la méthode `mixup` afin de rendre l'exemple plus clair. La méthode crée une nouvelle instance de `Point` avec la valeur `x` du `Point` lui-même (de type `X1`) et la valeur `y` du `Point` passé (de type `Y2`).

<Illustration numéro="10-11" nom de fichier="src/main.rs" légende="Une méthode qui utilise des types génériques différents de ceux de la définition de sa structure">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-11/src/main.rs}}
```

</Illustration>

Dans `main`, nous avons défini un `Point` qui a un `i32` pour `x` (avec la valeur `5`) et un `f64` pour `y` (avec la valeur `10.4`). La variable `p2` est une structure `Point` qui a un segment de chaîne pour `x` (avec la valeur `"Hello"`) et un `char` pour `y` (avec la valeur `c`). Appeler `mixup` sur `p1` avec l'argument `p2` nous donne `p3`, qui aura un `i32` pour `x` parce que `x` provient de `p1`. La variable `p3` aura un `char` pour `y` parce que `y` provient de `p2`. L'appel de macro `println!` affichera `p3.x = 5, p3.y = c`.

Le but de cet exemple est de démontrer une situation dans laquelle certains paramètres génériques sont déclarés avec `impl` et certains sont déclarés avec la définition de méthode. Ici, les paramètres génériques `X1` et `Y1` sont déclarés après `impl` car ils sont associés à la définition de la structure. Les paramètres génériques `X2` et `Y2` sont déclarés après `fn mixup` car ils ne sont pertinents que pour la méthode.

### Performance du code utilisant des génériques

Vous vous demandez peut-être s'il y a un coût d'exécution associé à l'utilisation de paramètres de type générique. La bonne nouvelle est que l'utilisation de types génériques ne ralentira pas votre programme plus qu'il ne le ferait avec des types concrets.

Rust accomplit cela en pratiquant la monomorphisation du code utilisant des génériques à la compilation. La _monomorphisation_ est le processus de transformation du code générique en code spécifique en remplissant les types concrets qui sont utilisés lors de la compilation. Dans ce processus, le compilateur effectue l'opération inverse des étapes que nous avons utilisées pour créer la fonction générique dans l'illustration 10-5 : le compilateur examine tous les endroits où le code générique est appelé et génère du code pour les types concrets avec lesquels le code générique est appelé.

Examinons comment cela fonctionne en utilisant l'énumération générique `Option<T>` de la bibliothèque standard :

```rust
let integer = Some(5);
let float = Some(5.0);
```

Lorsque Rust compile ce code, il effectue la monomorphisation. Au cours de ce processus, le compilateur lit les valeurs qui ont été utilisées dans les instances d'`Option<T>` et identifie deux types d'`Option<T>` : un est `i32` et l'autre est `f64`. En conséquence, il développe la définition générique d'`Option<T>` en deux définitions spécialisées pour `i32` et `f64`, remplaçant ainsi la définition générique par les spécifiques.

La version monomorphisée du code ressemble à ce qui suit (le compilateur utilise des noms différents de ceux que nous utilisons ici pour illustration) :

<Illustration nom de fichier="src/main.rs">

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

</Illustration>

L'énumération générique `Option<T>` est remplacée par les définitions spécifiques créées par le compilateur. Parce que Rust compile le code générique en code qui spécifie le type dans chaque instance, nous n'avons aucun coût d'exécution pour l'utilisation des génériques. Lorsque le code s'exécute, il fonctionne exactement comme s'il avait été duplicable pour chaque définition à la main. Le processus de monomorphisation rend les génériques de Rust extrêmement efficaces à l'exécution.