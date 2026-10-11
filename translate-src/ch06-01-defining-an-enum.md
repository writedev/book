## Définir une énumération

Alors que les structures vous permettent de regrouper des champs et des données liés, comme `Rectangle` avec sa `width` et sa `height`, les énumérations vous permettent d’indiquer qu’une valeur appartient à un ensemble de valeurs possibles. Par exemple, nous pouvons vouloir dire que `Rectangle` appartient à un ensemble de formes possibles qui comprend également `Circle` et `Triangle`. Pour cela, Rust nous permet d’encoder ces possibilités sous forme d’énumération.

Examinons une situation que nous pourrions vouloir exprimer dans du code et voyons pourquoi les énumérations sont utiles et plus appropriées que les structures dans ce cas. Supposons que nous devions travailler avec des adresses IP. Actuellement, deux normes principales sont utilisées pour les adresses IP : la version quatre et la version six. Comme ce sont les seules possibilités d’adresse IP auxquelles notre programme sera confronté, nous pouvons _énumérer_ toutes les variantes possibles, d’où le nom d’énumération.

Toute adresse IP est soit une adresse de version quatre, soit une adresse de version six, mais pas les deux à la fois. Cette propriété des adresses IP fait de la structure de données énumération un choix approprié, car une valeur d’énumération ne peut être que l’une de ses variantes. Les adresses de version quatre et de version six restent fondamentalement des adresses IP ; elles doivent donc être traitées comme étant du même type lorsque le code gère des situations qui s’appliquent à n’importe quel type d’adresse IP.

Nous pouvons exprimer ce concept dans du code en définissant une énumération `IpAddrKind` et en listant les types d’adresses IP possibles, `V4` et `V6`. Ce sont les variantes de l’énumération :

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-01-defining-enums/src/main.rs:def}}
```

`IpAddrKind` est désormais un type de données personnalisé que nous pouvons utiliser ailleurs dans notre code.

### Valeurs d’énumération

Nous pouvons créer des instances de chacune des deux variantes de `IpAddrKind` comme ceci :

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-01-defining-enums/src/main.rs:instance}}
```

Notez que les variantes de l’énumération sont placées dans l’espace de noms de son identifiant, et que nous utilisons deux deux-points pour les séparer. Cela est utile, car les deux valeurs `IpAddrKind::V4` et `IpAddrKind::V6` sont maintenant du même type : `IpAddrKind`. Nous pouvons alors, par exemple, définir une fonction qui prend n’importe quelle valeur de type `IpAddrKind` :

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-01-defining-enums/src/main.rs:fn}}
```

Et nous pouvons appeler cette fonction avec l’une ou l’autre des variantes :

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-01-defining-enums/src/main.rs:fn_call}}
```

L’utilisation des énumérations présente encore plus d’avantages. En réfléchissant davantage à notre type d’adresse IP, nous constatons que nous n’avons pour le moment aucun moyen de stocker les _données_ de l’adresse IP proprement dite ; nous savons seulement de quel _type_ elle est. Comme vous venez d’apprendre à utiliser les structures au chapitre 5, vous pourriez être tenté de résoudre ce problème avec des structures, comme indiqué dans l’exemple 6-1.

<Listing number="6-1" caption="Stocker les données et la variante `IpAddrKind` d’une adresse IP à l’aide d’une `struct`">

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-01/src/main.rs:here}}
```

</Listing>

Ici, nous avons défini une structure `IpAddr` qui possède deux champs : un champ `kind` de type `IpAddrKind` (l’énumération que nous avons définie précédemment) et un champ `address` de type `String`. Nous avons deux instances de cette structure. La première est `home`, dont le champ `kind` a pour valeur `IpAddrKind::V4` et qui est associée aux données d’adresse `127.0.0.1`. La deuxième instance est `loopback`. Son champ `kind` a pour valeur l’autre variante de `IpAddrKind`, `V6`, et elle est associée à l’adresse `::1`. Nous avons utilisé une structure pour regrouper les valeurs `kind` et `address` ; la variante est donc maintenant associée à la valeur.

Cependant, représenter le même concept avec une simple énumération est plus concis. Au lieu d’utiliser une énumération dans une structure, nous pouvons directement associer des données à chaque variante de l’énumération. Cette nouvelle définition de l’énumération `IpAddr` indique que les variantes `V4` et `V6` auront toutes deux des valeurs `String` associées :

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-02-enum-with-data/src/main.rs:here}}
```

Nous associons directement des données à chaque variante de l’énumération ; aucune structure supplémentaire n’est donc nécessaire. Ici, il est également plus facile de voir un autre détail du fonctionnement des énumérations : le nom de chaque variante d’énumération que nous définissons devient également une fonction qui construit une instance de l’énumération. Autrement dit, `IpAddr::V4()` est un appel de fonction qui prend un argument `String` et renvoie une instance du type `IpAddr`. La définition de l’énumération nous fournit automatiquement cette fonction constructeur.

L’utilisation d’une énumération plutôt que d’une structure présente un autre avantage : chaque variante peut avoir des types et des quantités de données associées différents. Les adresses IP de version quatre comportent toujours quatre composants numériques dont les valeurs sont comprises entre 0 et 255. Si nous voulions stocker les adresses `V4` sous forme de quatre valeurs `u8`, tout en représentant les adresses `V6` par une seule valeur `String`, nous ne pourrions pas le faire avec une structure. Les énumérations gèrent facilement ce cas :

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-03-variants-with-different-data/src/main.rs:here}}
```

Nous avons présenté plusieurs façons de définir des structures de données permettant de stocker des adresses IP de version quatre et de version six. Cependant, le stockage des adresses IP et l’encodage de leur type sont si courants que [la bibliothèque standard propose une définition que nous pouvons utiliser !][IpAddr]<!-- ignore --> Voyons comment la bibliothèque standard définit `IpAddr`. Elle possède exactement la même énumération et les mêmes variantes que celles que nous avons définies et utilisées, mais elle intègre les données d’adresse dans les variantes sous la forme de deux structures différentes, définies différemment pour chaque variante :

```rust
struct Ipv4Addr {
    // --snip--
}

struct Ipv6Addr {
    // --snip--
}

enum IpAddr {
    V4(Ipv4Addr),
    V6(Ipv6Addr),
}
```

Ce code montre que vous pouvez placer n’importe quel type de données dans une variante d’énumération : des chaînes de caractères, des types numériques ou des structures, par exemple. Vous pouvez même inclure une autre énumération ! De plus, les types de la bibliothèque standard ne sont souvent pas beaucoup plus complexes que ce que vous pourriez créer vous-même.

Notez que, même si la bibliothèque standard contient une définition de `IpAddr`, nous pouvons toujours créer et utiliser notre propre définition sans conflit, car nous n’avons pas importé la définition de la bibliothèque standard dans notre portée. Nous parlerons plus en détail de l’importation de types dans une portée au chapitre 7.

Examinons une autre énumération dans l’exemple 6-2 : ses variantes intègrent une grande variété de types.

<Listing number="6-2" caption="Une énumération `Message` dont les variantes stockent chacune des valeurs de types et de quantités différents">

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-02/src/main.rs:here}}
```

</Listing>

Cette énumération comporte quatre variantes de types différents :

- `Quit` : ne lui est associée aucune donnée
- `Move` : possède des champs nommés, comme une structure
- `Write` : inclut une seule valeur `String`
- `ChangeColor` : inclut trois valeurs `i32`

Définir une énumération avec des variantes comme celles de l’exemple 6-2 revient à définir différents types de structures, à ceci près que l’énumération n’utilise pas le mot-clé `struct` et que toutes les variantes sont regroupées sous le type `Message`. Les structures suivantes pourraient contenir les mêmes données que les variantes de l’énumération précédente :

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-04-structs-similar-to-message-enum/src/main.rs:here}}
```

Cependant, si nous utilisions ces différentes structures, chacune ayant son propre type, nous ne pourrions pas définir aussi facilement une fonction qui prend n’importe lequel de ces types de messages qu’avec l’énumération `Message` de l’exemple 6-2, qui constitue un type unique.

Les énumérations et les structures ont une autre similitude : tout comme nous pouvons définir des méthodes sur les structures à l’aide de `impl`, nous pouvons également définir des méthodes sur les énumérations. Voici une méthode nommée `call` que nous pourrions définir sur notre énumération `Message` :

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-05-methods-on-enums/src/main.rs:here}}
```

Le corps de la méthode utiliserait `self` pour obtenir la valeur sur laquelle nous avons appelé la méthode. Dans cet exemple, nous avons créé une variable `m` dont la valeur est `Message::Write(String::from("hello"))` ; c’est donc ce que sera `self` dans le corps de la méthode `call` lors de l’exécution de `m.call()`.

Examinons une autre énumération de la bibliothèque standard, très courante et utile : `Option`.

<!-- Old headings. Do not remove or links may break. -->

<a id="the-option-enum-and-its-advantages-over-null-values"></a>

### L’énumération `Option`

Cette section étudie `Option`, une autre énumération définie par la bibliothèque standard. Le type `Option` encode un cas très courant dans lequel une valeur peut être présente ou absente.

Par exemple, si vous demandez le premier élément d’une liste non vide, vous obtiendrez une valeur. Si vous demandez le premier élément d’une liste vide, vous n’obtiendrez rien. Exprimer ce concept dans le système de types permet au compilateur de vérifier que vous avez traité tous les cas nécessaires ; cette fonctionnalité peut prévenir des bogues extrêmement courants dans d’autres langages de programmation.

La conception des langages de programmation est souvent envisagée en fonction des fonctionnalités qu’ils incluent, mais celles qu’ils excluent sont tout aussi importantes. Rust ne possède pas la fonctionnalité `null` que l’on trouve dans de nombreux autres langages. _Null_ est une valeur qui signifie qu’il n’y a aucune valeur. Dans les langages qui utilisent `null`, les variables peuvent toujours se trouver dans l’un de ces deux états : nulles ou non nulles.

Dans sa présentation de 2009 intitulée « Null References: The Billion Dollar Mistake », Tony Hoare, l’inventeur de `null`, a déclaré :

> Je l’appelle mon erreur à un milliard de dollars. À l’époque, je concevais le premier système de types complet pour les références dans un langage orienté objet. Mon objectif était de garantir que toute utilisation de références soit absolument sûre, grâce à des vérifications effectuées automatiquement par le compilateur. Mais je n’ai pas résisté à la tentation d’ajouter une référence nulle, simplement parce qu’elle était si facile à implémenter. Cela a entraîné d’innombrables erreurs, vulnérabilités et pannes système, qui ont probablement causé un milliard de dollars de préjudices et de dégâts au cours des quarante dernières années.

Le problème des valeurs nulles est que si vous essayez d’utiliser une valeur nulle comme si elle était non nulle, vous obtiendrez une erreur quelconque. Comme cette propriété — nul ou non nul — est omniprésente, il est extrêmement facile de commettre ce genre d’erreur.

Cependant, le concept que `null` cherche à exprimer reste utile : une valeur nulle est une valeur actuellement invalide ou absente pour une raison quelconque.

Le problème ne vient pas vraiment du concept, mais de son implémentation particulière. Ainsi, Rust n’a pas de valeurs nulles, mais possède une énumération qui permet d’encoder le concept d’une valeur présente ou absente. Cette énumération est `Option<T>`, et elle est [définie par la bibliothèque standard][option]<!-- ignore --> comme suit :

```rust
enum Option<T> {
    None,
    Some(T),
}
```

L’énumération `Option<T>` est si utile qu’elle est incluse dans le préambule ; vous n’avez pas besoin de l’importer explicitement. Ses variantes y sont également incluses : vous pouvez utiliser directement `Some` et `None` sans le préfixe `Option::`. L’énumération `Option<T>` reste une énumération ordinaire, et `Some(T)` et `None` restent des variantes de type `Option<T>`.

La syntaxe `<T>` est une fonctionnalité de Rust dont nous n’avons pas encore parlé. Il s’agit d’un paramètre de type générique, et nous aborderons les génériques plus en détail au chapitre 10. Pour le moment, il vous suffit de savoir que `<T>` signifie que la variante `Some` de l’énumération `Option` peut contenir une donnée de n’importe quel type, et que chaque type concret utilisé à la place de `T` donne à l’ensemble une valeur de type `Option<T>` différente. Voici quelques exemples d’utilisation de valeurs `Option` pour contenir des nombres et des caractères :

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-06-option-examples/src/main.rs:here}}
```

Le type de `some_number` est `Option<i32>`. Le type de `some_char` est `Option<char>`, un type différent. Rust peut déduire ces types, car nous avons indiqué une valeur dans la variante `Some`. Pour `absent_number`, Rust exige que nous annotions le type global de `Option` : le compilateur ne peut pas déduire le type que contiendrait la variante `Some` correspondante en examinant uniquement une valeur `None`. Ici, nous indiquons à Rust que nous voulons que `absent_number` soit de type `Option<i32>`.

Lorsque nous avons une valeur `Some`, nous savons qu’une valeur est présente et qu’elle est contenue dans `Some`. Lorsque nous avons une valeur `None`, cela signifie, dans un certain sens, la même chose que `null` : nous n’avons pas de valeur valide. Alors, pourquoi `Option<T>` est-il préférable à `null` ?

En bref, parce que `Option<T>` et `T` (où `T` peut être n’importe quel type) sont des types différents, le compilateur ne nous laissera pas utiliser une valeur `Option<T>` comme s’il s’agissait d’une valeur nécessairement valide. Par exemple, ce code ne sera pas compilé, car il tente d’ajouter un `i8` à un `Option<i8>` :

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-07-cant-use-option-directly/src/main.rs:here}}
```

Si nous exécutons ce code, nous obtenons un message d’erreur semblable à celui-ci :

```console
{{#include ../listings/ch06-enums-and-pattern-matching/no-listing-07-cant-use-option-directly/output.txt}}
```

C’est sévère ! En fait, ce message d’erreur signifie que Rust ne sait pas comment additionner un `i8` et un `Option<i8>`, car ce sont des types différents. Lorsque nous avons une valeur d’un type comme `i8` en Rust, le compilateur garantit que nous avons toujours une valeur valide. Nous pouvons continuer en toute confiance sans avoir à vérifier si la valeur est nulle avant de l’utiliser. Ce n’est que lorsque nous avons un `Option<i8>` (ou tout autre type de valeur avec lequel nous travaillons) que nous devons nous préoccuper de l’absence éventuelle d’une valeur, et le compilateur s’assure que nous traitons ce cas avant d’utiliser la valeur.

Autrement dit, vous devez convertir un `Option<T>` en `T` avant de pouvoir effectuer des opérations de type `T` avec cette valeur. En général, cela permet de détecter l’un des problèmes les plus courants liés à `null` : supposer qu’une valeur n’est pas nulle alors qu’elle l’est en réalité.

Éliminer le risque de supposer à tort qu’une valeur n’est pas nulle vous aide à avoir davantage confiance en votre code. Pour qu’une valeur puisse être nulle, vous devez l’autoriser explicitement en lui attribuant le type `Option<T>`. Ainsi, lorsque vous utilisez cette valeur, vous devez traiter explicitement le cas où elle est nulle. Partout où une valeur a un type qui n’est pas `Option<T>`, vous pouvez supposer sans risque que cette valeur n’est pas nulle. Il s’agit d’un choix de conception délibéré de Rust, destiné à limiter l’omniprésence de `null` et à renforcer la sûreté du code Rust.

Comment obtenir la valeur `T` d’une variante `Some` lorsque vous avez une valeur de type `Option<T>`, afin de pouvoir l’utiliser ? L’énumération `Option<T>` possède un grand nombre de méthodes utiles dans diverses situations ; vous pouvez les consulter dans [sa documentation][docs]<!-- ignore -->. Se familiariser avec les méthodes de `Option<T>` vous sera très utile dans votre apprentissage de Rust.

En général, pour utiliser une valeur `Option<T>`, vous devez écrire du code qui traite chaque variante. Il vous faut du code qui s’exécute uniquement lorsque vous avez une valeur `Some(T)` et qui peut utiliser le `T` contenu. Il vous faut un autre code qui s’exécute uniquement si vous avez une valeur `None` et qui ne dispose d’aucune valeur `T`. L’expression `match` est une construction de contrôle de flux qui permet justement cela avec les énumérations : elle exécute un code différent selon la variante de l’énumération, et ce code peut utiliser les données contenues dans la valeur correspondante.

[IpAddr]: ../std/net/enum.IpAddr.html
[option]: ../std/option/enum.Option.html
[docs]: ../std/option/enum.Option.html