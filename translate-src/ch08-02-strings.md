## Stocker du texte encodé en UTF-8 avec des chaînes

Nous avons parlé des chaînes au chapitre 4, mais nous allons maintenant les examiner plus en détail.
Les nouveaux adeptes de Rust se heurtent souvent aux chaînes pour trois raisons principales : Rust a tendance à exposer les erreurs possibles, les chaînes sont une structure de données plus complexe que ne le pensent de nombreux programmeurs, et il y a l’UTF-8. Ces facteurs se combinent d’une manière qui peut sembler difficile lorsqu’on vient d’autres langages de programmation.

Nous abordons les chaînes dans le contexte des collections, car elles sont implémentées comme une collection d’octets, à laquelle s’ajoutent des méthodes offrant des fonctionnalités utiles lorsque ces octets sont interprétés comme du texte. Dans cette section, nous parlerons des opérations sur `String` que l’on retrouve dans tous les types de collections, comme la création, la mise à jour et la lecture. Nous verrons également en quoi `String` diffère des autres collections, à savoir comment les différences entre l’interprétation des données `String` par les humains et par les ordinateurs compliquent l’indexation d’une `String`.

<!-- Old headings. Do not remove or links may break. -->

<a id="what-is-a-string"></a>

### Définir les chaînes

Commençons par définir ce que nous entendons par le terme _chaîne_. Rust ne possède qu’un seul type de chaîne dans son langage de base : la tranche de chaîne `str`, que l’on rencontre généralement sous sa forme empruntée, `&str`. Au chapitre 4, nous avons parlé des tranches de chaîne, qui sont des références à des données de chaîne encodées en UTF-8 et stockées ailleurs. Les littéraux de chaîne, par exemple, sont stockés dans le binaire du programme et sont donc des tranches de chaîne.

Le type `String`, fourni par la bibliothèque standard de Rust plutôt que défini dans le langage de base, est un type de chaîne extensible, modifiable, possédé et encodé en UTF-8. Lorsque les adeptes de Rust parlent de « chaînes » en Rust, ils peuvent désigner aussi bien le type `String` que le type de tranche de chaîne `&str`, et pas seulement l’un de ces types. Bien que cette section porte principalement sur `String`, les deux types sont largement utilisés dans la bibliothèque standard de Rust, et `String` comme les tranches de chaîne sont encodés en UTF-8.

### Créer une nouvelle chaîne

Bon nombre des opérations disponibles avec `Vec<T>` le sont également avec `String`, car `String` est en fait implémenté comme un wrapper autour d’un vecteur d’octets, assorti de quelques garanties, restrictions et fonctionnalités supplémentaires. La fonction `new`, qui crée une instance, est un exemple de fonction qui fonctionne de la même manière avec `Vec<T>` et `String`, comme le montre le Listing 8-11.

<Listing number="8-11" caption="Créer une nouvelle `String` vide">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-11/src/main.rs:here}}
```

</Listing>

Cette ligne crée une nouvelle chaîne vide appelée `s`, dans laquelle nous pouvons ensuite charger des données. Souvent, nous avons des données initiales avec lesquelles nous voulons commencer la chaîne. Pour cela, nous utilisons la méthode `to_string`, disponible sur tout type qui implémente le trait `Display`, comme c’est le cas des littéraux de chaîne. Le Listing 8-12 présente deux exemples.

<Listing number="8-12" caption="Utiliser la méthode `to_string` pour créer une `String` à partir d’un littéral de chaîne">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-12/src/main.rs:here}}
```

</Listing>

Ce code crée une chaîne contenant `initial contents`.

Nous pouvons également utiliser la fonction `String::from` pour créer une `String` à partir d’un littéral de chaîne. Le code du Listing 8-13 est équivalent à celui du Listing 8-12 qui utilise `to_string`.

<Listing number="8-13" caption="Utiliser la fonction `String::from` pour créer une `String` à partir d’un littéral de chaîne">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-13/src/main.rs:here}}
```

</Listing>

Comme les chaînes servent à de nombreuses choses, nous pouvons utiliser de nombreuses API génériques différentes pour les manipuler, ce qui nous offre beaucoup de possibilités. Certaines peuvent sembler redondantes, mais chacune a son utilité ! Dans ce cas, `String::from` et `to_string` font la même chose ; le choix entre les deux relève donc du style et de la lisibilité.

N’oubliez pas que les chaînes sont encodées en UTF-8 : nous pouvons donc y inclure n’importe quelle donnée correctement encodée, comme le montre le Listing 8-14.

<Listing number="8-14" caption="Stocker des salutations dans différentes langues au sein de chaînes">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-14/src/main.rs:here}}
```

</Listing>

Toutes ces valeurs sont des `String` valides.

### Mettre à jour une chaîne

Une `String` peut augmenter de taille et son contenu peut changer, tout comme le contenu d’un `Vec<T>`, si vous y ajoutez davantage de données. De plus, vous pouvez utiliser facilement l’opérateur `+` ou la macro `format!` pour concaténer des valeurs `String`.

<!-- Old headings. Do not remove or links may break. -->

<a id="appending-to-a-string-with-push_str-and-push"></a>

#### Ajouter avec `push_str` ou `push`

Nous pouvons agrandir une `String` à l’aide de la méthode `push_str`, qui ajoute une tranche de chaîne, comme le montre le Listing 8-15.

<Listing number="8-15" caption="Ajouter une tranche de chaîne à une `String` à l’aide de la méthode `push_str`">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-15/src/main.rs:here}}
```

</Listing>

Après ces deux lignes, `s` contiendra `foobar`. La méthode `push_str` prend une tranche de chaîne afin de ne pas nécessairement prendre possession du paramètre. Par exemple, dans le code du Listing 8-16, nous voulons pouvoir utiliser `s2` après avoir ajouté son contenu à `s1`.

<Listing number="8-16" caption="Utiliser une tranche de chaîne après avoir ajouté son contenu à une `String`">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-16/src/main.rs:here}}
```

</Listing>

Si la méthode `push_str` prenait possession de `s2`, nous ne pourrions pas afficher sa valeur sur la dernière ligne. Cependant, ce code fonctionne comme prévu !

La méthode `push` prend un seul caractère en paramètre et l’ajoute à la `String`. Le Listing 8-17 ajoute la lettre _l_ à une `String` à l’aide de la méthode `push`.

<Listing number="8-17" caption="Ajouter un caractère à une valeur `String` à l’aide de `push`">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-17/src/main.rs:here}}
```

</Listing>

Ainsi, `s` contiendra `lol`.

<!-- Old headings. Do not remove or links may break. -->

<a id="concatenation-with-the--operator-or-the-format-macro"></a>

#### Concaténer avec `+` ou `format!`

Souvent, vous voudrez combiner deux chaînes existantes. Une façon de le faire consiste à utiliser l’opérateur `+`, comme le montre le Listing 8-18.

<Listing number="8-18" caption="Utiliser l’opérateur `+` pour combiner deux valeurs `String` en une nouvelle valeur `String`">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-18/src/main.rs:here}}
```

</Listing>

La chaîne `s3` contiendra `Hello, world!`. Si `s1` n’est plus valide après l’addition et si nous avons utilisé une référence à `s2`, c’est en raison de la signature de la méthode appelée lorsque nous utilisons l’opérateur `+`. L’opérateur `+` utilise la méthode `add`, dont la signature ressemble à ceci :

```rust,ignore
fn add(self, s: &str) -> String {
```

Dans la bibliothèque standard, vous verrez que `add` est défini à l’aide de types génériques et de types associés. Ici, nous avons remplacé ceux-ci par des types concrets, comme cela se produit lorsque nous appelons cette méthode avec des valeurs `String`. Nous parlerons des génériques au chapitre 10. Cette signature nous donne les indices nécessaires pour comprendre les aspects délicats de l’opérateur `+`.

Tout d’abord, `s2` est précédé d’un `&`, ce qui signifie que nous ajoutons une référence à la deuxième chaîne à la première chaîne. Cela vient du paramètre `s` de la fonction `add` : nous pouvons uniquement ajouter une tranche de chaîne à une `String` ; nous ne pouvons pas additionner deux valeurs `String`. Mais attendez : le type de `&s2` est `&String`, et non `&str`, comme l’indique le deuxième paramètre de `add`. Alors, pourquoi le Listing 8-18 compile-t-il ?

La raison pour laquelle nous pouvons utiliser `&s2` dans l’appel à `add` est que le compilateur peut convertir l’argument `&String` en `&str`. Lorsque nous appelons la méthode `add`, Rust utilise une coercition par déréférencement qui transforme ici `&s2` en `&s2[..]`. Nous étudierons plus en détail la coercition par déréférencement au chapitre 15. Comme `add` ne prend pas possession du paramètre `s`, `s2` reste une `String` valide après cette opération.

Ensuite, nous pouvons voir dans la signature que `add` prend possession de `self`, car `self` n’est _pas_ précédé d’un `&`. Cela signifie que `s1` dans le Listing 8-18 sera déplacé dans l’appel à `add` et ne sera plus valide après cela. Ainsi, même si `let s3 = s1 + &s2;` semble copier les deux chaînes pour en créer une nouvelle, cette instruction prend en réalité possession de `s1`, ajoute une copie du contenu de `s2`, puis renvoie la possession du résultat. En d’autres termes, on pourrait croire qu’elle effectue beaucoup de copies, mais ce n’est pas le cas : l’implémentation est plus efficace qu’une copie.

Si nous devons concaténer plusieurs chaînes, le comportement de l’opérateur `+` devient difficile à manier :

```rust
{{#rustdoc_include ../listings/ch08-common-collections/no-listing-01-concat-multiple-strings/src/main.rs:here}}
```

À ce stade, `s` vaudra `tic-tac-toe`. Avec tous les caractères `+` et `"`, il est difficile de comprendre ce qui se passe. Pour combiner des chaînes de manière plus complexe, nous pouvons plutôt utiliser la macro `format!` :

```rust
{{#rustdoc_include ../listings/ch08-common-collections/no-listing-02-format/src/main.rs:here}}
```

Ce code affecte également la valeur `tic-tac-toe` à `s`. La macro `format!` fonctionne comme `println!`, mais au lieu d’afficher le résultat à l’écran, elle renvoie une `String` contenant ce résultat. La version du code qui utilise `format!` est beaucoup plus facile à lire, et le code généré par la macro `format!` utilise des références, de sorte que cet appel ne prend possession d’aucun de ses paramètres.

### Indexer des chaînes

Dans de nombreux autres langages de programmation, accéder à des caractères individuels d’une chaîne en les désignant par leur indice est une opération valide et courante. Cependant, si vous tentez d’accéder à des parties d’une `String` à l’aide de la syntaxe d’indexation en Rust, vous obtiendrez une erreur. Considérez le code invalide du Listing 8-19.

<Listing number="8-19" caption="Tentative d’utilisation de la syntaxe d’indexation avec une `String`">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-19/src/main.rs:here}}
```

</Listing>

Ce code provoquera l’erreur suivante :

```console
{{#include ../listings/ch08-common-collections/listing-08-19/output.txt}}
```

L’erreur est explicite : les chaînes Rust ne prennent pas en charge l’indexation. Mais pourquoi ? Pour répondre à cette question, nous devons parler de la manière dont Rust stocke les chaînes en mémoire.

#### Représentation interne

Une `String` est un wrapper autour d’un `Vec<u8>`. Examinons quelques-unes des chaînes d’exemple correctement encodées en UTF-8 du Listing 8-14. Tout d’abord, celle-ci :

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-14/src/main.rs:spanish}}
```

Dans ce cas, `len` vaudra `4`, ce qui signifie que le vecteur qui stocke la chaîne `"Hola"` fait 4 octets. Chacune de ces lettres occupe 1 octet lorsqu’elle est encodée en UTF-8. La ligne suivante pourrait toutefois vous surprendre (notez que cette chaîne commence par la lettre cyrillique majuscule _Ze_, et non par le chiffre 3) :

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-14/src/main.rs:russian}}
```

Si l’on vous demandait quelle est la longueur de cette chaîne, vous répondriez peut-être 12. En réalité, Rust répond 24 : c’est le nombre d’octets nécessaires pour encoder « Здравствуйте » en UTF-8, car chaque valeur scalaire Unicode de cette chaîne occupe 2 octets. Par conséquent, un indice dans les octets de la chaîne ne correspondra pas toujours à une valeur scalaire Unicode valide. Pour le montrer, considérons ce code Rust invalide :

```rust,ignore,does_not_compile
let hello = "Здравствуйте";
let answer = &hello[0];
```

Vous savez déjà que `answer` ne sera pas `З`, la première lettre. En UTF-8, le premier octet de `З` vaut `208` et le deuxième `151` ; on pourrait donc penser que `answer` devrait être `208`, mais `208` n’est pas un caractère valide à lui seul. Renvoyer `208` n’est probablement pas ce que souhaiterait un utilisateur qui demande la première lettre de cette chaîne ; pourtant, c’est la seule donnée dont dispose Rust à l’indice d’octet 0. En général, les utilisateurs ne veulent pas que la valeur de l’octet leur soit renvoyée, même si la chaîne ne contient que des lettres latines : si `&"hi"[0]` était un code valide renvoyant la valeur de l’octet, il renverrait `104`, et non `h`.

La réponse est donc que, pour éviter de renvoyer une valeur inattendue et de provoquer des bogues qui pourraient ne pas être détectés immédiatement, Rust ne compile pas du tout ce code et prévient les malentendus dès le début du processus de développement.

<!-- Old headings. Do not remove or links may break. -->

<a id="bytes-and-scalar-values-and-grapheme-clusters-oh-my"></a>

#### Octets, valeurs scalaires et grappes de graphèmes

Un autre aspect de l’UTF-8 est qu’il existe en réalité trois façons pertinentes d’examiner les chaînes du point de vue de Rust : comme des octets, des valeurs scalaires et des grappes de graphèmes (ce qui se rapproche le plus de ce que nous appelons des _lettres_).

Si nous examinons le mot hindi « नमस्ते », écrit en devanagari, il est stocké sous la forme d’un vecteur de valeurs `u8` qui ressemble à ceci :

```text
[224, 164, 168, 224, 164, 174, 224, 164, 184, 224, 165, 141, 224, 164, 164,
224, 165, 135]
```

Cela représente 18 octets, ce qui correspond à la façon dont les ordinateurs stockent finalement ces données. Si nous les examinons comme des valeurs scalaires Unicode, qui correspondent au type `char` de Rust, ces octets ressemblent à ceci :

```text
['न', 'म', 'स', '्', 'त', 'े']
```

Il y a ici six valeurs `char`, mais la quatrième et la sixième ne sont pas des lettres : ce sont des signes diacritiques qui n’ont pas de sens isolément. Enfin, si nous les examinons comme des grappes de graphèmes, nous obtenons ce qu’une personne appellerait les quatre lettres qui composent le mot hindi :

```text
["न", "म", "स्", "ते"]
```

Rust fournit différentes façons d’interpréter les données brutes des chaînes stockées par les ordinateurs, afin que chaque programme puisse choisir l’interprétation dont il a besoin, quelle que soit la langue humaine utilisée dans les données.

Une dernière raison pour laquelle Rust ne nous permet pas d’indexer une `String` pour en obtenir un caractère est que les opérations d’indexation sont censées avoir un temps d’exécution constant (O(1)). Or, il est impossible de garantir cette performance avec une `String`, car Rust devrait parcourir son contenu depuis le début jusqu’à l’indice afin de déterminer le nombre de caractères valides.

### Découper des chaînes

Indexer une chaîne est souvent une mauvaise idée, car le type de retour de l’opération d’indexation d’une chaîne n’est pas évident : une valeur d’octet, un caractère, une grappe de graphèmes ou une tranche de chaîne. Si vous avez vraiment besoin d’utiliser des indices pour créer des tranches de chaîne, Rust vous demande donc d’être plus précis.

Au lieu d’utiliser `[]` avec un seul nombre pour indexer la chaîne, vous pouvez utiliser `[]` avec une plage afin de créer une tranche de chaîne contenant certains octets :

```rust
let hello = "Здравствуйте";

let s = &hello[0..4];
```

Ici, `s` sera un `&str` contenant les 4 premiers octets de la chaîne. Nous avons indiqué précédemment que chacun de ces caractères occupait 2 octets, ce qui signifie que `s` vaudra `Зд`.

Si nous essayions de découper seulement une partie des octets d’un caractère, par exemple avec `&hello[0..1]`, Rust déclencherait une panique à l’exécution, comme lorsqu’on accède à un indice invalide dans un vecteur :

```console
{{#include ../listings/ch08-common-collections/output-only-01-not-char-boundary/output.txt}}
```

Soyez prudent lorsque vous créez des tranches de chaîne à l’aide de plages, car cela peut faire planter votre programme.

<!-- Old headings. Do not remove or links may break. -->

<a id="methods-for-iterating-over-strings"></a>

### Parcourir des chaînes

La meilleure façon de manipuler des fragments de chaînes est de préciser si vous voulez obtenir des caractères ou des octets. Pour obtenir les valeurs scalaires Unicode individuelles, utilisez la méthode `chars`. Appeler `chars` sur « Зд » sépare et renvoie deux valeurs de type `char`, et vous pouvez parcourir le résultat pour accéder à chaque élément :

```rust
for c in "Зд".chars() {
    println!("{c}");
}
```

Ce code affichera ce qui suit :

```text
З
д
```

La méthode `bytes`, quant à elle, renvoie chaque octet brut, ce qui peut convenir à votre domaine :

```rust
for b in "Зд".bytes() {
    println!("{b}");
}
```

Ce code affichera les 4 octets qui composent cette chaîne :

```text
208
151
208
180
```

N’oubliez toutefois pas que les valeurs scalaires Unicode valides peuvent être composées de plusieurs octets.

Obtenir des grappes de graphèmes à partir de chaînes, comme celles de l’écriture devanagari, est complexe ; cette fonctionnalité n’est donc pas fournie par la bibliothèque standard. Des crates sont disponibles sur [crates.io](https://crates.io/)<!-- ignore --> si vous avez besoin de cette fonctionnalité.

<!-- Old headings. Do not remove or links may break. -->

<a id="strings-are-not-so-simple"></a>

### Gérer la complexité des chaînes

En résumé, les chaînes sont complexes. Les différents langages de programmation font des choix différents quant à la manière de présenter cette complexité au programmeur. Rust a choisi de faire du traitement correct des données `String` le comportement par défaut de tous les programmes Rust, ce qui signifie que les programmeurs doivent réfléchir davantage au traitement des données UTF-8 dès le départ. Ce compromis expose davantage la complexité des chaînes que ne le font d’autres langages de programmation, mais il vous évite d’avoir à gérer plus tard dans le cycle de développement des erreurs impliquant des caractères non ASCII.

La bonne nouvelle, c’est que la bibliothèque standard offre de nombreuses fonctionnalités fondées sur les types `String` et `&str` pour vous aider à gérer correctement ces situations complexes. N’hésitez pas à consulter la documentation pour découvrir des méthodes utiles comme `contains`, qui permet de rechercher dans une chaîne, et `replace`, qui permet de remplacer des parties d’une chaîne par une autre chaîne.

Passons à quelque chose d’un peu moins complexe : les tables de hachage !