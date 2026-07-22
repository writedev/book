## Stockage de texte encodé en UTF-8 avec des chaînes

Nous avons parlé des chaînes dans le Chapitre 4, mais nous allons les examiner plus en profondeur maintenant. Les nouveaux Rustaceans se heurtent souvent aux chaînes pour un ensemble de trois raisons : la tendance de Rust à exposer les erreurs possibles, la complexité des chaînes par rapport à ce que beaucoup de programmeurs en pensent, et l'UTF-8. Ces facteurs se combinent de manière à sembler difficiles lorsque l'on vient d'autres langages de programmation.

Nous discutons des chaînes dans le contexte des collections parce que les chaînes sont implémentées comme une collection d'octets, plus quelques méthodes pour fournir des fonctionnalités utiles lorsque ces octets sont interprétés comme du texte. Dans cette section, nous parlerons des opérations sur `String` que chaque type de collection possède, telles que la création, la mise à jour et la lecture. Nous discuterons également des façons dont `String` est différent des autres collections, à savoir comment l'indexation dans une `String` est compliquée par les différences entre la façon dont les gens et les ordinateurs interprètent les données de type `String`.

<!-- Anciens titres. Ne pas supprimer ou les liens pourraient être cassés. -->

<a id="what-is-a-string"></a>

### Définir les chaînes

Nous allons d'abord définir ce que nous entendons par le terme _chaîne_. Rust n'a qu'un seul type de chaîne dans le langage de base, qui est la tranche de chaîne `str` que l'on voit généralement sous sa forme empruntée, `&str`. Dans le Chapitre 4, nous avons parlé des tranches de chaîne, qui sont des références à des données de chaîne encodées en UTF-8 stockées ailleurs. Les littéraux de chaîne, par exemple, sont stockés dans le binaire du programme et sont donc des tranches de chaîne.

Le type `String`, qui est fourni par la bibliothèque standard de Rust plutôt que codé dans le langage de base, est un type de chaîne encodable en UTF-8, mutable, détenu et extensible. Lorsque les Rustaceans font référence aux "chaînes" en Rust, ils peuvent se référer soit au type `String`, soit au type de tranche de chaîne `&str`, et pas seulement à l'un de ces types. Bien que cette section concerne largement `String`, les deux types sont largement utilisés dans la bibliothèque standard de Rust, et à la fois `String` et les tranches de chaîne sont encodés en UTF-8.

### Créer une nouvelle chaîne

De nombreuses opérations disponibles avec `Vec<T>` le sont également avec `String`, car `String` est en réalité implémenté comme un wrapper autour d'un vecteur d'octets avec quelques garanties, restrictions et capacités supplémentaires. Un exemple de fonction qui fonctionne de la même manière avec `Vec<T>` et `String` est la fonction `new` pour créer une instance, illustrée dans la Liste 8-11.

<Listing number="8-11" caption="Créer une nouvelle chaîne vide `String`">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-11/src/main.rs:here}}
```

</Listing>

Cette ligne crée une nouvelle chaîne vide appelée `s`, dans laquelle nous pouvons ensuite charger des données. Souvent, nous aurons des données initiales avec lesquelles nous voulons commencer la chaîne. Pour cela, nous utilisons la méthode `to_string`, qui est disponible sur tout type implémentant le trait `Display`, comme le font les littéraux de chaîne. La Liste 8-12 montre deux exemples.

<Listing number="8-12" caption="Utiliser la méthode `to_string` pour créer un `String` à partir d'un littéral de chaîne">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-12/src/main.rs:here}}
```

</Listing>

Ce code crée une chaîne contenant `contenu initial`.

Nous pouvons également utiliser la fonction `String::from` pour créer un `String` à partir d'un littéral de chaîne. Le code dans la Liste 8-13 est équivalent au code de la Liste 8-12 qui utilise `to_string`.

<Listing number="8-13" caption="Utiliser la fonction `String::from` pour créer un `String` à partir d'un littéral de chaîne">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-13/src/main.rs:here}}
```

</Listing>

Étant donné que les chaînes sont utilisées pour de nombreuses choses, nous pouvons utiliser de nombreuses API génériques différentes pour les chaînes, nous fournissant de nombreuses options. Certaines peuvent sembler redondantes, mais elles ont toutes leur place ! Dans ce cas, `String::from` et `to_string` font la même chose, donc le choix entre les deux est une question de style et de lisibilité.

N'oubliez pas que les chaînes sont encodées en UTF-8, donc nous pouvons inclure toutes les données correctement encodées, comme le montre la Liste 8-14.

<Listing number="8-14" caption="Stocker des salutations dans différentes langues dans des chaînes">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-14/src/main.rs:here}}
```

</Listing>

Tous ces éléments sont des valeurs `String` valides.

### Mettre à jour une chaîne

Une `String` peut croître en taille et son contenu peut changer, tout comme le contenu d'un `Vec<T>`, si vous ajoutez plus de données. De plus, vous pouvez facilement utiliser l'opérateur `+` ou le macro `format!` pour concaténer des valeurs `String`.

<!-- Anciens titres. Ne pas supprimer ou les liens pourraient être cassés. -->

<a id="appending-to-a-string-with-push_str-and-push"></a>

#### Ajouter avec `push_str` ou `push`

Nous pouvons agrandir une `String` en utilisant la méthode `push_str` pour ajouter une tranche de chaîne, comme montré dans la Liste 8-15.

<Listing number="8-15" caption="Ajouter une tranche de chaîne à une `String` en utilisant la méthode `push_str`">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-15/src/main.rs:here}}
```

</Listing>

Après ces deux lignes, `s` contiendra `foobar`. La méthode `push_str` prend une tranche de chaîne car nous ne voulons pas nécessairement prendre possession du paramètre. Par exemple, dans le code de la Liste 8-16, nous voulons pouvoir utiliser `s2` après avoir ajouté son contenu à `s1`.

<Listing number="8-16" caption="Utiliser une tranche de chaîne après avoir ajouté son contenu à une `String`">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-16/src/main.rs:here}}
```

</Listing>

Si la méthode `push_str` prenait possession de `s2`, nous ne pourrions pas imprimer sa valeur à la dernière ligne. Cependant, ce code fonctionne comme nous l'attendions !

La méthode `push` prend un seul caractère comme paramètre et l'ajoute à la `String`. La Liste 8-17 ajoute la lettre _l_ à une `String` en utilisant la méthode `push`.

<Listing number="8-17" caption="Ajouter un caractère à une valeur `String` en utilisant `push`">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-17/src/main.rs:here}}
```

</Listing>

En conséquence, `s` contiendra `lol`.

<!-- Anciens titres. Ne pas supprimer ou les liens pourraient être cassés. -->

<a id="concatenation-with-the--operator-or-the-format-macro"></a>

#### Concaténer avec `+` ou `format!`

Souvent, vous voudrez combiner deux chaînes existantes. Une façon de le faire est d'utiliser l'opérateur `+`, comme montré dans la Liste 8-18.

<Listing number="8-18" caption="Utiliser l'opérateur `+` pour combiner deux valeurs `String` en une nouvelle valeur `String`">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-18/src/main.rs:here}}
```

</Listing>

La chaîne `s3` contiendra `Hello, world!`. La raison pour laquelle `s1` n'est plus valide après l'addition, et la raison pour laquelle nous avons utilisé une référence à `s2`, concerne la signature de la méthode qui est appelée lorsque nous utilisons l'opérateur `+`. L'opérateur `+` utilise la méthode `add`, dont la signature ressemble à quelque chose comme ceci :

```rust,ignore
fn add(self, s: &str) -> String {
```

Dans la bibliothèque standard, vous verrez `add` défini en utilisant des génériques et des types associés. Ici, nous avons substitué des types concrets, ce qui se produit lorsque nous appelons cette méthode avec des valeurs `String`. Nous discuterons des génériques dans le Chapitre 10. Cette signature nous donne les indices dont nous avons besoin pour comprendre les points délicats de l'opérateur `+`.

Tout d'abord, `s2` a un `&`, ce qui signifie que nous ajoutons une référence de la deuxième chaîne à la première chaîne. Cela est dû au paramètre `s` dans la fonction `add` : nous ne pouvons ajouter qu'une tranche de chaîne à une `String` ; nous ne pouvons pas ajouter deux valeurs `String`. Mais attendez—le type de `&s2` est `&String`, pas `&str`, comme spécifié dans le deuxième paramètre de `add`. Alors, pourquoi la Liste 8-18 compile-t-elle ?

La raison pour laquelle nous pouvons utiliser `&s2` dans l'appel à `add`, c'est que le compilateur peut contraindre l'argument `&String` en un `&str`. Lorsque nous appelons la méthode `add`, Rust utilise une coercition de dereferencement, qui transforme ici `&s2` en `&s2[..]`. Nous discuterons de la coercition de dereferencement en profondeur dans le Chapitre 15. Comme `add` ne prend pas possession du paramètre `s`, `s2` restera une `String` valide après cette opération.

Deuxièmement, nous pouvons voir dans la signature que `add` prend possession de `self` parce que `self` n'a _pas_ de `&`. Cela signifie que `s1` dans la Liste 8-18 sera déplacé dans l'appel à `add` et ne sera plus valide après cela. Donc, bien que `let s3 = s1 + &s2;` semble que cela copiera les deux chaînes et en créerait une nouvelle, cette instruction prend en réalité possession de `s1`, ajoute une copie du contenu de `s2`, puis retourne la possession du résultat. En d'autres termes, il semble qu'il fasse beaucoup de copies, mais ce n'est pas le cas ; l'implémentation est plus efficace que la copie.

Si nous avons besoin de concaténer plusieurs chaînes, le comportement de l'opérateur `+` devient ingérable :

```rust
{{#rustdoc_include ../listings/ch08-common-collections/no-listing-01-concat-multiple-strings/src/main.rs:here}}
```

À ce stade, `s` sera `tic-tac-toe`. Avec tous les `+` et les caractères `"` présents, il est difficile de voir ce qui se passe. Pour combiner des chaînes de manière plus complexe, nous pouvons plutôt utiliser le macro `format!` :

```rust
{{#rustdoc_include ../listings/ch08-common-collections/no-listing-02-format/src/main.rs:here}}
```

Ce code définit également `s` à `tic-tac-toe`. Le macro `format!` fonctionne comme `println!`, mais au lieu d'imprimer la sortie à l'écran, il retourne une `String` avec les contenus. La version du code utilisant `format!` est beaucoup plus facile à lire, et le code généré par le macro `format!` utilise des références de sorte que cet appel ne prenne pas possession d'aucun de ses paramètres.

### Indexation dans les chaînes

Dans de nombreux autres langages de programmation, l'accès à des caractères individuels d'une chaîne par leur index est une opération valide et courante. Cependant, si vous essayez d'accéder à des parties d'une `String` en utilisant la syntaxe d'indexation en Rust, vous obtiendrez une erreur. Considérons le code invalide dans la Liste 8-19.

<Listing number="8-19" caption="Tentative d'utilisation de la syntaxe d'indexation avec une `String`">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-19/src/main.rs:here}}
```

</Listing>

Ce code générera l'erreur suivante :

```console
{{#include ../listings/ch08-common-collections/listing-08-19/output.txt}}
```

L'erreur raconte l'histoire : les chaînes Rust ne supportent pas l'indexation. Mais pourquoi pas ? Pour répondre à cette question, nous devons discuter de la façon dont Rust stocke les chaînes en mémoire.

#### Représentation interne

Une `String` est un wrapper sur un `Vec<u8>`. Regardons quelques exemples de chaînes correctement encodées en UTF-8 de la Liste 8-14. D'abord, celle-ci :

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-14/src/main.rs:spanish}}
```

Dans ce cas, `len` sera `4`, ce qui signifie que le vecteur stockant la chaîne `"Hola"` a 4 octets de long. Chacune de ces lettres prend 1 octet lorsqu'elle est encodée en UTF-8. La ligne suivante, cependant, peut vous surprendre (notez que cette chaîne commence par la lettre cyrillique majuscule _Ze_, pas le nombre 3) :

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-14/src/main.rs:russian}}
```

Si vous deviez dire combien la chaîne mesure, vous pourriez dire 12. En fait, la réponse de Rust est 24 : c'est le nombre d'octets nécessaires pour encoder "Здравствуйте" en UTF-8, car chaque valeur scalaire Unicode dans cette chaîne prend 2 octets de stockage. Par conséquent, un index dans les octets de la chaîne ne correspont pas toujours à une valeur scalaire Unicode valide. Pour démontrer, considérons ce code Rust invalide :

```rust,ignore,does_not_compile
let hello = "Здравствуйте";
let answer = &hello[0];
```

Vous savez déjà que `answer` ne sera pas `З`, la première lettre. Lorsqu'elle est encodée en UTF-8, le premier octet de `З` est `208` et le second est `151`, donc il semblerait que `answer` devrait en fait être `208`, mais `208` n'est pas un caractère valide à lui seul. Retourner `208` n'est probablement pas ce qu'un utilisateur voudrait s'il demandait la première lettre de cette chaîne ; cependant, c'est la seule donnée que Rust a à l'index d'octet 0. Les utilisateurs ne veulent généralement pas que la valeur d'octet soit retournée, même si la chaîne ne contient que des lettres latines : si `&"hi"[0]` était un code valide qui retournait la valeur d'octet, il retournerait `104`, pas `h`.

La réponse est donc que pour éviter de retourner une valeur inattendue et de provoquer des bugs qui pourraient ne pas être découverts immédiatement, Rust ne compile pas du tout ce code et empêche les malentendus dès le début du processus de développement.

<!-- Anciens titres. Ne pas supprimer ou les liens pourraient être cassés. -->

<a id="bytes-and-scalar-values-and-grapheme-clusters-oh-my"></a>

#### Octets, valeurs scalaires et clusters de graphèmes

Un autre point concernant l'UTF-8 est qu'il existe en réalité trois manières pertinentes de considérer les chaînes du point de vue de Rust : en tant qu'octets, valeurs scalaires et clusters de graphèmes (la chose la plus proche de ce que nous appellerions _lettres_).

Si nous regardons le mot hindi "नमस्ते" écrit en script devanagari, il est stocké sous forme de vecteur de valeurs `u8` qui ressemble à ceci :

```text
[224, 164, 168, 224, 164, 174, 224, 164, 184, 224, 165, 141, 224, 164, 164,
224, 165, 135]
```

C'est 18 octets et c'est ainsi que les ordinateurs stockent finalement ces données. Si nous les considérons comme des valeurs scalaires Unicode, qui sont ce que le type `char` de Rust représente, ces octets ressemblent à ceci :

```text
['न', 'म', 'स', '्', 'त', 'े']
```

Il y a six valeurs `char` ici, mais la quatrième et la sixième ne sont pas des lettres : ce sont des diacritiques qui n'ont pas de sens à elles seules. Enfin, si nous les considérons comme des clusters de graphèmes, nous obtiendrions ce que quelqu'un appellerait les quatre lettres qui composent le mot hindi :

```text
["न", "म", "स्", "ते"]
```

Rust fournit différentes façons d'interpréter les données de chaîne brutes que les ordinateurs stockent afin que chaque programme puisse choisir l'interprétation dont il a besoin, quel que soit le langage humain dans lequel les données se trouvent.

Une dernière raison pour laquelle Rust ne nous permet pas d'indexer une `String` pour obtenir un caractère est que les opérations d'indexation sont censées toujours prendre un temps constant (O(1)). Mais il n'est pas possible de garantir cette performance avec une `String`, car Rust devrait parcourir le contenu du début à l'index pour déterminer combien de caractères valides il y avait.

### Trancher des chaînes

Indexer une chaîne est souvent une mauvaise idée car il n'est pas clair quel devrait être le type de retour de l'opération d'indexation de chaîne : une valeur d'octet, un caractère, un cluster de graphème ou une tranche de chaîne. Si vous avez vraiment besoin d'utiliser des indices pour créer des tranches de chaîne, Rust vous demande donc d'être plus précis.

Plutôt que d'indexer avec `[]` avec un seul nombre, vous pouvez utiliser `[]` avec une plage pour créer une tranche de chaîne contenant des octets particuliers :

```rust
let hello = "Здравствуйте";

let s = &hello[0..4];
```

Ici, `s` sera une `&str` contenant les 4 premiers octets de la chaîne. Plus tôt, nous avons mentionné que chacun de ces caractères faisait 2 octets, ce qui signifie que `s` sera `Зд`.

Si nous devions essayer de trancher seulement une partie des octets d'un caractère avec quelque chose comme `&hello[0..1]`, Rust paniquerait à l'exécution de la même manière qu'en cas d'accès à un index invalide dans un vecteur :

```console
{{#include ../listings/ch08-common-collections/output-only-01-not-char-boundary/output.txt}}
```

Vous devez faire attention lorsque vous créez des tranches de chaîne avec des plages, car cela peut faire planter votre programme.

<!-- Anciens titres. Ne pas supprimer ou les liens pourraient être cassés. -->

<a id="methods-for-iterating-over-strings"></a>

### Itérer sur des chaînes

Le meilleur moyen d'opérer sur des morceaux de chaînes est d'être explicite sur ce que vous voulez, des caractères ou des octets. Pour des valeurs scalaires Unicode individuelles, utilisez la méthode `chars`. Appeler `chars` sur "Зд" sépare et retourne deux valeurs de type `char`, et vous pouvez itérer sur le résultat pour accéder à chaque élément :

```rust
for c in "Зд".chars() {
    println!("{c}");
}
```

Ce code imprimera ce qui suit :

```text
З
д
```

Alternativement, la méthode `bytes` retourne chaque octet brut, ce qui pourrait être approprié pour votre domaine :

```rust
for b in "Зд".bytes() {
    println!("{b}");
}
```

Ce code imprimera les 4 octets qui composent cette chaîne :

```text
208
151
208
180
```

Mais n'oubliez pas que des valeurs scalaires Unicode valides peuvent être constituées de plus d'un octet.

Obtenir des clusters de graphèmes à partir des chaînes, comme avec le script devanagari, est complexe, donc cette fonctionnalité n'est pas fournie par la bibliothèque standard. Des crates sont disponibles sur [crates.io](https://crates.io/)<!-- ignore --> si c'est la fonctionnalité dont vous avez besoin.

<!-- Anciens titres. Ne pas supprimer ou les liens pourraient être cassés. -->

<a id="strings-are-not-so-simple"></a>

### Gérer les complexités des chaînes

Pour résumer, les chaînes sont compliquées. Différents langages de programmation font des choix différents sur la manière de présenter cette complexité au programmeur. Rust a choisi de faire en sorte que le traitement correct des données `String` soit le comportement par défaut pour tous les programmes Rust, ce qui signifie que les programmeurs doivent réfléchir davantage à la gestion des données UTF-8 dès le départ. Ce compromis expose plus de la complexité des chaînes qu'il n'apparaît dans d'autres langages de programmation, mais il vous évite d'avoir à gérer des erreurs impliquant des caractères non-ASCII plus tard dans votre cycle de développement.

La bonne nouvelle est que la bibliothèque standard offre de nombreuses fonctionnalités basées sur les types `String` et `&str` pour aider à gérer correctement ces situations complexes. Assurez-vous de consulter la documentation pour des méthodes utiles telles que `contains` pour rechercher dans une chaîne et `replace` pour remplacer des parties d'une chaîne par une autre chaîne.

Passons à quelque chose d'un peu moins complexe : les tables de hachage !