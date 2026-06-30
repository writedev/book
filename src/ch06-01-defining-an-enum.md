## Définir un Enum

Alors que les structures vous offrent un moyen de regrouper des champs et des données connexes, comme un `Rectangle` avec sa `largeur` et sa `hauteur`, les enums vous permettent d'indiquer qu'une valeur est l'une d'un ensemble de valeurs possibles. Par exemple, nous pourrions vouloir dire que `Rectangle` est l'un des types de formes possibles qui comprend également `Cercle` et `Triangle`. Pour cela, Rust nous permet d'encoder ces possibilités sous la forme d'un enum.

Examinons une situation que nous pourrions souhaiter exprimer en code et voyons pourquoi les enums sont utiles et plus appropriés que les structures dans ce cas. Disons que nous devons travailler avec des adresses IP. Actuellement, deux normes majeures sont utilisées pour les adresses IP : version quatre et version six. Étant donné que ce sont les seules possibilités pour une adresse IP que notre programme rencontrera, nous pouvons _énumérer_ tous les variants possibles, d'où le nom énumération.

Une adresse IP peut être soit une adresse version quatre, soit une adresse version six, mais pas les deux en même temps. Cette propriété des adresses IP rend la structure de données enum appropriée car une valeur enum ne peut être qu'un de ses variants. Les adresses version quatre et version six sont toujours fondamentalement des adresses IP, donc elles doivent être traitées comme le même type lorsque le code gère des situations qui s'appliquent à tout type d'adresse IP.

Nous pouvons exprimer ce concept en code en définissant une énumération `IpAddrKind` et en énumérant les types possibles qu'une adresse IP peut être, `V4` et `V6`. Ce sont les variants de l'enum :

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-01-defining-enums/src/main.rs:def}}
```

`IpAddrKind` est maintenant un type de données personnalisé que nous pouvons utiliser ailleurs dans notre code.

### Valeurs Enum

Nous pouvons créer des instances de chacun des deux variants de `IpAddrKind` comme ceci :

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-01-defining-enums/src/main.rs:instance}}
```

Notez que les variants de l'enum sont "namespacés" sous son identifiant, et nous utilisons un double deux-points pour séparer les deux. Ceci est utile car maintenant les deux valeurs `IpAddrKind::V4` et `IpAddrKind::V6` sont du même type : `IpAddrKind`. Nous pouvons alors, par exemple, définir une fonction qui prend n'importe quel `IpAddrKind` :

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-01-defining-enums/src/main.rs:fn}}
```

Et nous pouvons appeler cette fonction avec l'un ou l'autre variant :

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-01-defining-enums/src/main.rs:fn_call}}
```

Utiliser des enums a encore plus d'avantages. En réfléchissant davantage à notre type d'adresse IP, pour le moment nous n'avons pas de moyen de stocker les données réelles de l'adresse IP ; nous savons seulement de quel _type_ il s'agit. Étant donné que vous avez appris sur les structures dans le Chapitre 5, vous pourriez être tenté d'aborder ce problème avec des structures comme montré dans la Liste 6-1.

<Liste numéro="6-1" légende="Stocker les données et le variant `IpAddrKind` d'une adresse IP à l'aide d'une `struct`">

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-01/src/main.rs:here}}
```

</Liste>

Ici, nous avons défini une structure `IpAddr` qui a deux champs : un champ `kind` qui est de type `IpAddrKind` (l'enum que nous avons défini précédemment) et un champ `address` de type `String`. Nous avons deux instances de cette structure. La première est `home`, et elle a la valeur `IpAddrKind::V4` comme son `kind` avec des données d'adresse associées de `127.0.0.1`. La seconde instance est `loopback`. Elle a l'autre variant de `IpAddrKind` comme sa valeur de `kind`, `V6`, et a l'adresse `::1` associée à elle. Nous avons utilisé une structure pour regrouper les valeurs `kind` et `address`, donc maintenant le variant est associé à la valeur.

Cependant, représenter le même concept en utilisant juste un enum est plus concis : Plutôt qu'un enum à l'intérieur d'une structure, nous pouvons mettre directement des données dans chaque variant de l'enum. Cette nouvelle définition de l'enum `IpAddr` dit que les variants `V4` et `V6` auront des valeurs `String` associées :

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-02-enum-with-data/src/main.rs:here}}
```

Nous attachons des données directement à chaque variant de l'enum, donc il n'est pas nécessaire d'avoir une structure supplémentaire. Ici, il est également plus facile de voir un autre détail de la façon dont les enums fonctionnent : Le nom de chaque variant d'enum que nous définissons devient également une fonction qui construit une instance de l'enum. C'est-à-dire que `IpAddr::V4()` est un appel de fonction qui prend un argument `String` et retourne une instance du type `IpAddr`. Nous obtenons automatiquement cette fonction constructeur en définissant l'enum.

Il y a un autre avantage à utiliser un enum plutôt qu'une structure : Chaque variant peut avoir des types et des quantités de données associées différents. Les adresses IP version quatre auront toujours quatre composants numériques qui auront des valeurs entre 0 et 255. Si nous voulions stocker des adresses `V4` comme quatre valeurs `u8` mais que nous voulions toujours exprimer des adresses `V6` comme une valeur `String`, nous ne pourrions pas le faire avec une structure. Les enums gèrent ce cas avec aisance :

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-03-variants-with-different-data/src/main.rs:here}}
```

Nous avons montré plusieurs façons différentes de définir des structures de données pour stocker les adresses IP version quatre et version six. Cependant, il s'avère que vouloir stocker des adresses IP et encoder quel type elles sont est si courant que [la bibliothèque standard a une définition que nous pouvons utiliser !][IpAddr]<!-- ignore --> Regardons comment la bibliothèque standard définit `IpAddr`. Il a l'exact enum et variants que nous avons définis et utilisés, mais il incorpore les données d'adresse à l'intérieur des variants sous la forme de deux structures différentes, qui sont définies différemment pour chaque variant :

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

Ce code illustre que vous pouvez mettre n'importe quel type de données à l'intérieur d'un variant d'enum : chaînes, types numériques ou structures, par exemple. Vous pouvez même inclure un autre enum ! De plus, les types de la bibliothèque standard ne sont souvent pas beaucoup plus compliqués que ce que vous pourriez concevoir.

Notez que même si la bibliothèque standard contient une définition pour `IpAddr`, nous pouvons toujours créer et utiliser notre propre définition sans conflit car nous n'avons pas introduit la définition de la bibliothèque standard dans notre portée. Nous parlerons plus de l'introduction de types dans la portée dans le Chapitre 7.

Examinons un autre exemple d'un enum dans la Liste 6-2 : Celui-ci a une grande variété de types intégrés dans ses variants.

<Liste numéro="6-2" légende="Un enum `Message` dont les variants stockent chacun différentes quantités et types de valeurs">

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-02/src/main.rs:here}}
```

</Liste>

Cet enum a quatre variants avec des types différents :

- `Quit` : N'a aucune donnée associée
- `Move` : A des champs nommés, comme une structure
- `Write` : Inclut une seule `String`
- `ChangeColor` : Inclut trois valeurs `i32`

Définir un enum avec des variants comme ceux de la Liste 6-2 est similaire à définir différents types de définitions de structures, sauf que l'enum n'utilise pas le mot clé `struct` et que tous les variants sont regroupés sous le type `Message`. Les structures suivantes pourraient contenir les mêmes données que celles que les précédents variants d'enum tiennent :

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-04-structs-similar-to-message-enum/src/main.rs:here}}
```

Mais si nous utilisions les différentes structures, chacune ayant son propre type, nous ne pourrions pas aussi facilement définir une fonction pour prendre l'un de ces types de messages que nous pourrions avec l'enum `Message` défini dans la Liste 6-2, qui est un type unique.

Il y a une autre similitude entre les enums et les structures : Tout comme nous pouvons définir des méthodes sur les structures à l'aide de `impl`, nous pouvons également définir des méthodes sur les enums. Voici une méthode nommée `call` que nous pourrions définir sur notre enum `Message` :

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-05-methods-on-enums/src/main.rs:here}}
```

Le corps de la méthode utiliserait `self` pour obtenir la valeur sur laquelle nous avons appelé la méthode. Dans cet exemple, nous avons créé une variable `m` qui a la valeur `Message::Write(String::from("hello"))`, et c'est ce que `self` sera dans le corps de la méthode `call` lorsque `m.call()` s'exécutera.

Regardons un autre enum dans la bibliothèque standard qui est très courant et utile : `Option`.

### L'Enum `Option`

Cette section explore une étude de cas de `Option`, qui est un autre enum défini par la bibliothèque standard. Le type `Option` encode le scénario très courant dans lequel une valeur peut être quelque chose, ou elle peut être rien.

Par exemple, si vous demandez le premier élément d'une liste non vide, vous obtiendrez une valeur. Si vous demandez le premier élément d'une liste vide, vous n'obtiendrez rien. Exprimer ce concept en termes de système de type signifie que le compilateur peut vérifier si vous avez géré tous les cas que vous devriez gérer ; cette fonctionnalité peut prévenir des bogues qui sont extrêmement courants dans d'autres langages de programmation.

La conception de langages de programmation est souvent pensée en termes de quelles fonctionnalités vous incluez, mais les fonctionnalités que vous excluez sont également importantes. Rust n'a pas la fonctionnalité nulle que de nombreux autres langages ont. _Null_ est une valeur qui signifie qu'il n'y a pas de valeur présente. Dans les langages avec null, les variables peuvent toujours être dans l'un de deux états : nul ou non nul.

Dans sa présentation de 2009 "Null References: The Billion Dollar Mistake", Tony Hoare, l'inventeur de null, a déclaré :

> Je l'appelle mon erreur à un milliard de dollars. À ce moment-là, je concevais le premier système de types complet pour les références dans un langage orienté objet. Mon objectif était de garantir que toutes les utilisations de références soient absolument sûres, avec des vérifications effectuées automatiquement par le compilateur. Mais je n'ai pas pu résister à la tentation de mettre en place une référence nulle, simplement parce que c'était si facile à implémenter. Cela a conduit à d'innombrables erreurs, vulnérabilités et pannes de système, qui ont probablement causé un milliard de dollars de douleur et de dégâts au cours des quarante dernières années.

Le problème avec les valeurs nulles est que si vous essayez d'utiliser une valeur nulle comme une valeur non nulle, vous obtiendrez une sorte d'erreur. Parce que cette propriété nul ou non nul est omniprésente, il est extrêmement facile de commettre ce genre d'erreur.

Cependant, le concept que null essaie d'exprimer est toujours utile : Un null est une valeur qui est actuellement invalide ou absente pour une raison quelconque.

Le problème n'est pas vraiment avec le concept mais avec la mise en œuvre particulière. En tant que tel, Rust n'a pas de nulls, mais il a un enum qui peut encoder le concept d'une valeur étant présente ou absente. Cet enum est `Option<T>`, et il est [défini par la bibliothèque standard][option]<!-- ignore --> comme suit :

```rust
enum Option<T> {
    None,
    Some(T),
}
```

L'enum `Option<T>` est si utile qu'il est même inclus dans le préambule ; vous n'avez pas besoin de l'introduire dans votre portée explicitement. Ses variants sont également inclus dans le préambule : Vous pouvez utiliser `Some` et `None` directement sans le préfixe `Option::`. L'enum `Option<T>` est toujours juste un enum régulier, et `Some(T)` et `None` sont toujours des variants de type `Option<T>`.

La syntaxe `<T>` est une fonctionnalité de Rust que nous n'avons pas encore abordée. C'est un paramètre de type générique, et nous couvrirons les génériques plus en détail dans le Chapitre 10. Pour l'instant, tout ce que vous devez savoir, c'est que `<T>` signifie que le variant `Some` de l'enum `Option` peut contenir un morceau de données de n'importe quel type, et que chaque type concret qui est utilisé à la place de `T` rend le type global `Option<T>` d'un type différent. Voici quelques exemples d'utilisation des valeurs `Option` pour contenir des types numériques et des types de caractères :

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-06-option-examples/src/main.rs:here}}
```

Le type de `some_number` est `Option<i32>`. Le type de `some_char` est `Option<char>`, qui est un type différent. Rust peut inférer ces types car nous avons spécifié une valeur à l'intérieur du variant `Some`. Pour `absent_number`, Rust exige que nous annotions le type d'ensemble `Option` : Le compilateur ne peut pas inférer le type que le variant `Some` correspondant contiendra en regardant uniquement une valeur `None`. Ici, nous disons à Rust que nous voulons que `absent_number` soit de type `Option<i32>`.

Lorsque nous avons une valeur `Some`, nous savons qu'une valeur est présente, et la valeur est contenue dans le `Some`. Lorsque nous avons une valeur `None`, dans un sens, cela signifie la même chose que null : nous n'avons pas de valeur valide. Alors, pourquoi avoir `Option<T>` est-il meilleur que d'avoir null ?

En résumé, parce que `Option<T>` et `T` (où `T` peut être n'importe quel type) sont des types différents, le compilateur ne nous permettra pas d'utiliser une valeur `Option<T>` comme si c'était définitivement une valeur valide. Par exemple, ce code ne compilera pas, car il essaie d'ajouter un `i8` à un `Option<i8>` :

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-07-cant-use-option-directly/src/main.rs:here}}
```

Si nous exécutons ce code, nous obtenons un message d'erreur comme celui-ci :

```console
{{#include ../listings/ch06-enums-and-pattern-matching/no-listing-07-cant-use-option-directly/output.txt}}
```

Intense ! En effet, ce message d'erreur signifie que Rust ne comprend pas comment ajouter un `i8` et un `Option<i8>`, car ce sont des types différents. Lorsque nous avons une valeur d'un type comme `i8` en Rust, le compilateur s'assurera que nous avons toujours une valeur valide. Nous pouvons procéder avec confiance sans devoir vérifier si la valeur est nulle avant d'utiliser cette valeur. Ce n'est que lorsque nous avons un `Option<i8>` (ou tout autre type de valeur avec lequel nous travaillons) que nous devons nous soucier de ne pas avoir de valeur, et le compilateur s'assurera que nous gérons ce cas avant d'utiliser la valeur.

En d'autres termes, vous devez convertir un `Option<T>` en `T` avant de pouvoir effectuer des opérations `T` avec cela. En général, cela aide à attraper l'un des problèmes les plus courants avec null : supposer que quelque chose n'est pas nul alors qu'il l'est effectivement.

Éliminer le risque de supposer incorrectement une valeur non nulle vous aide à être plus sûr de votre code. Afin d'avoir une valeur qui peut éventuellement être nulle, vous devez explicitement opter pour cela en faisant le type de cette valeur `Option<T>`. Ensuite, lorsque vous utilisez cette valeur, vous êtes obligé de gérer explicitement le cas lorsque la valeur est nulle. Partout où une valeur a un type qui n'est pas un `Option<T>`, vous _pouvez_ supposer en toute sécurité que la valeur n'est pas nulle. C'était une décision de conception délibérée pour Rust de limiter la diffusion du null et d'augmenter la sécurité du code Rust.

Alors, comment obtenir la valeur `T` d'un variant `Some` lorsque vous avez une valeur de type `Option<T>` pour que vous puissiez utiliser cette valeur ? L'enum `Option<T>` a un grand nombre de méthodes qui sont utiles dans une variété de situations ; vous pouvez les consulter dans [sa documentation][docs]<!-- ignore -->. Devenir familier avec les méthodes sur `Option<T>` sera extrêmement utile dans votre parcours avec Rust.

En général, afin d'utiliser une valeur `Option<T>`, vous voulez avoir du code qui gérera chaque variant. Vous voulez un code qui s'exécutera uniquement lorsque vous avez une valeur `Some(T)`, et ce code est autorisé à utiliser le `T` interne. Vous voulez un autre code qui s'exécutera uniquement si vous disposez d'une valeur `None`, et ce code n'a pas de valeur `T` disponible. L'expression `match` est une structure de flux de contrôle qui fait exactement cela lorsqu'elle est utilisée avec des enums : Elle exécutera différents codes selon le variant de l'enum qu'elle possède, et ce code peut utiliser les données à l'intérieur de la valeur correspondante.

[IpAddr]: ../std/net/enum.IpAddr.html
[option]: ../std/option/enum.Option.html
[docs]: ../std/option/enum.Option.html