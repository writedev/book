## Types de données

Toute valeur en Rust est d’un certain _type de données_, qui indique à Rust quel type de données est spécifié afin qu’il sache comment les traiter. Nous allons examiner deux catégories de types de données : les types scalaires et les types composés.

Gardez à l’esprit que Rust est un langage à _typage statique_, ce qui signifie qu’il doit connaître les types de toutes les variables au moment de la compilation. Le compilateur peut généralement déduire le type que nous voulons utiliser à partir de la valeur et de la manière dont nous l’utilisons. Dans les cas où plusieurs types sont possibles, par exemple lorsque nous avons converti une `String` en type numérique à l’aide de `parse` dans la section [« Comparer la supposition au nombre secret »][comparing-the-guess-to-the-secret-number]<!-- ignore --> du chapitre 2, nous devons ajouter une annotation de type, comme ceci :

```rust
let guess: u32 = "42".parse().expect("Not a number!");
```

Si nous n’ajoutons pas l’annotation de type `: u32` présentée dans le code précédent, Rust affichera l’erreur suivante, ce qui signifie que le compilateur a besoin de davantage d’informations pour savoir quel type nous voulons utiliser :

```console
{{#include ../listings/ch03-common-programming-concepts/output-only-01-no-type-annotations/output.txt}}
```

Vous verrez d’autres annotations de type pour d’autres types de données.

### Types scalaires

Un type _scalaire_ représente une seule valeur. Rust possède quatre principaux types scalaires : les entiers, les nombres à virgule flottante, les booléens et les caractères. Vous les connaissez peut-être déjà d’autres langages de programmation. Voyons comment ils fonctionnent en Rust.

#### Types entiers

Un _entier_ est un nombre sans partie fractionnaire. Nous avons utilisé un type entier au chapitre 2, le type `u32`. Cette déclaration de type indique que la valeur qui lui est associée doit être un entier non signé (les types entiers signés commencent par `i` au lieu de `u`) occupant 32 bits. Le tableau 3-1 présente les types entiers intégrés à Rust. Nous pouvons utiliser n’importe laquelle de ces variantes pour déclarer le type d’une valeur entière.

<span class="caption">Tableau 3-1 : Types entiers en Rust</span>

| Longueur | Signé | Non signé |
| -------- | ----- | --------- |
| 8 bits   | `i8`  | `u8`      |
| 16 bits  | `i16` | `u16`     |
| 32 bits  | `i32` | `u32`     |
| 64 bits  | `i64` | `u64`     |
| 128 bits | `i128` | `u128`    |
| Dépend de l’architecture | `isize` | `usize` |

Chaque variante peut être signée ou non signée et possède une taille explicite. _Signé_ et _non signé_ indiquent si le nombre peut être négatif — autrement dit, si le nombre doit être accompagné d’un signe (signé) ou s’il sera toujours positif et peut donc être représenté sans signe (non signé). C’est comme écrire des nombres sur du papier : lorsque le signe est important, un nombre est précédé d’un signe plus ou moins ; toutefois, lorsqu’on peut supposer sans risque que le nombre est positif, il est écrit sans signe. Les nombres signés sont stockés selon la représentation en [complément à deux][twos-complement]<!-- ignore -->.

Chaque variante signée peut stocker des nombres de −(2<sup>n − 1</sup>) à 2<sup>n − 1</sup> − 1 inclus, où _n_ est le nombre de bits utilisés par cette variante. Ainsi, un `i8` peut stocker des nombres de −(2<sup>7</sup>) à 2<sup>7</sup> − 1, soit de −128 à 127. Les variantes non signées peuvent stocker des nombres de 0 à 2<sup>n</sup> − 1 ; un `u8` peut donc stocker des nombres de 0 à 2<sup>8</sup> − 1, soit de 0 à 255.

En outre, les types `isize` et `usize` dépendent de l’architecture de l’ordinateur sur lequel votre programme s’exécute : 64 bits sur une architecture 64 bits et 32 bits sur une architecture 32 bits.

Vous pouvez écrire des littéraux entiers sous l’une des formes présentées dans le tableau 3-2. Notez que les littéraux numériques pouvant correspondre à plusieurs types peuvent comporter un suffixe de type, tel que `57u8`, pour désigner leur type. Les littéraux numériques peuvent aussi utiliser `_` comme séparateur visuel afin de faciliter la lecture du nombre, par exemple `1_000`, qui a la même valeur que `1000`.

<span class="caption">Tableau 3-2 : Littéraux entiers en Rust</span>

| Littéraux numériques | Exemple       |
| -------------------- | ------------- |
| Décimal              | `98_222`      |
| Hexadécimal          | `0xff`        |
| Octal                | `0o77`        |
| Binaire              | `0b1111_0000` |
| Octet (`u8` uniquement) | `b'A'`     |

Comment savoir quel type entier utiliser ? En cas de doute, les valeurs par défaut de Rust sont généralement un bon point de départ : les types entiers sont par défaut des `i32`. On utilise principalement `isize` ou `usize` pour indexer une collection.

> ##### Débordement d’entier
>
> Supposons que vous ayez une variable de type `u8` pouvant contenir des valeurs comprises entre 0 et 255. Si vous essayez de lui attribuer une valeur en dehors de cette plage, telle que 256, un _débordement d’entier_ se produira, ce qui peut entraîner l’un de deux comportements. Lorsque vous compilez en mode débogage, Rust inclut des vérifications de débordement d’entier qui font _paniquer_ votre programme à l’exécution si un tel comportement se produit. Rust utilise le terme _panique_ lorsqu’un programme se termine avec une erreur ; nous aborderons les paniques plus en détail dans la section [« Erreurs irrécupérables avec `panic!` »][unrecoverable-errors-with-panic]<!-- ignore --> du chapitre 9.
>
> Lorsque vous compilez en mode publication avec l’indicateur `--release`, Rust n’inclut _pas_ de vérifications de débordement d’entier provoquant des paniques. À la place, en cas de débordement, Rust effectue un _retour circulaire en complément à deux_. En bref, les valeurs supérieures à la valeur maximale que le type peut contenir « reviennent » à la valeur minimale que le type peut contenir. Dans le cas d’un `u8`, la valeur 256 devient 0, la valeur 257 devient 1, et ainsi de suite. Le programme ne paniquera pas, mais la variable aura une valeur qui ne correspond probablement pas à ce que vous attendiez. Se fier au comportement de retour circulaire des débordements d’entier est considéré comme une erreur.
>
> Pour gérer explicitement la possibilité d’un débordement, vous pouvez utiliser les familles de méthodes suivantes fournies par la bibliothèque standard pour les types numériques primitifs :
>
> - Effectuer un retour circulaire dans tous les modes de compilation avec les méthodes `wrapping_*`, comme `wrapping_add`.
> - Renvoyer la valeur `None` en cas de débordement avec les méthodes `checked_*`.
> - Renvoyer la valeur ainsi qu’un booléen indiquant s’il y a eu un débordement avec les méthodes `overflowing_*`.
> - Saturer à la valeur minimale ou maximale du type avec les méthodes `saturating_*`.

#### Types à virgule flottante

Rust possède également deux types primitifs pour les _nombres à virgule flottante_, c’est-à-dire les nombres comportant une partie décimale. Les types à virgule flottante de Rust sont `f32` et `f64`, qui occupent respectivement 32 et 64 bits. Le type par défaut est `f64`, car sur les processeurs modernes, il est à peu près aussi rapide que `f32`, tout en offrant une meilleure précision. Tous les types à virgule flottante sont signés.

Voici un exemple qui montre les nombres à virgule flottante en action :

<span class="filename">Nom du fichier : src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-06-floating-point/src/main.rs}}
```

Les nombres à virgule flottante sont représentés conformément à la norme IEEE-754.

#### Opérations numériques

Rust prend en charge les opérations mathématiques de base que vous attendez pour tous les types de nombres : addition, soustraction, multiplication, division et reste. La division entière tronque le résultat vers zéro pour obtenir l’entier le plus proche. Le code suivant montre comment utiliser chaque opération numérique dans une instruction `let` :

<span class="filename">Nom du fichier : src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-07-numeric-operations/src/main.rs}}
```

Chaque expression de ces instructions utilise un opérateur mathématique et s’évalue en une seule valeur, qui est ensuite liée à une variable. L’[annexe B][appendix_b]<!-- ignore --> contient la liste de tous les opérateurs fournis par Rust.

#### Type booléen

Comme dans la plupart des autres langages de programmation, un type booléen en Rust peut prendre deux valeurs : `true` et `false`. Les booléens occupent un octet. Le type booléen en Rust est indiqué par `bool`. Par exemple :

<span class="filename">Nom du fichier : src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-08-boolean/src/main.rs}}
```

Les valeurs booléennes sont principalement utilisées dans les conditions, par exemple dans une expression `if`. Nous verrons le fonctionnement des expressions `if` en Rust dans la section [« Flux de contrôle »][control-flow]<!-- ignore -->.

#### Type caractère

Le type `char` de Rust est le type alphabétique le plus primitif du langage. Voici quelques exemples de déclaration de valeurs `char` :

<span class="filename">Nom du fichier : src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-09-char/src/main.rs}}
```

Notez que les littéraux `char` s’écrivent entre apostrophes, contrairement aux littéraux de chaîne, qui s’écrivent entre guillemets doubles. Le type `char` de Rust occupe 4 octets et représente une valeur scalaire Unicode, ce qui signifie qu’il peut représenter bien plus que de l’ASCII. Les lettres accentuées, les caractères chinois, japonais et coréens, les émojis et les espaces sans chasse sont tous des valeurs `char` valides en Rust. Les valeurs scalaires Unicode vont de `U+0000` à `U+D7FF`, puis de `U+E000` à `U+10FFFF`, bornes incluses. Cependant, la notion de « caractère » n’existe pas vraiment en Unicode ; votre intuition humaine de ce qu’est un « caractère » peut donc ne pas correspondre à ce qu’est un `char` en Rust. Nous aborderons ce sujet en détail dans la section [« Stocker du texte encodé en UTF-8 avec des chaînes »][strings]<!-- ignore --> du chapitre 8.

### Types composés

Les _types composés_ permettent de regrouper plusieurs valeurs en un seul type. Rust possède deux types composés primitifs : les tuples et les tableaux.

#### Type tuple

Un _tuple_ est une manière générale de regrouper plusieurs valeurs de types différents en un seul type composé. Les tuples ont une longueur fixe : une fois déclarés, ils ne peuvent ni grandir ni rétrécir.

Nous créons un tuple en écrivant une liste de valeurs séparées par des virgules entre parenthèses. Chaque position du tuple possède un type, et les types des différentes valeurs du tuple n’ont pas besoin d’être identiques. Nous avons ajouté des annotations de type facultatives dans cet exemple :

<span class="filename">Nom du fichier : src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-10-tuples/src/main.rs}}
```

La variable `tup` est liée au tuple entier, car un tuple est considéré comme un élément composé unique. Pour obtenir les valeurs individuelles d’un tuple, nous pouvons utiliser la correspondance de motifs afin de décomposer une valeur tuple, comme ceci :

<span class="filename">Nom du fichier : src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-11-destructuring-tuples/src/main.rs}}
```

Ce programme crée d’abord un tuple et le lie à la variable `tup`. Il utilise ensuite un motif avec `let` pour prendre `tup` et le transformer en trois variables distinctes : `x`, `y` et `z`. C’est ce qu’on appelle la _décomposition_, car elle divise le tuple unique en trois parties. Enfin, le programme affiche la valeur de `y`, qui est `6.4`.

Nous pouvons également accéder directement à un élément du tuple en utilisant un point (`.`) suivi de l’indice de la valeur à laquelle nous voulons accéder. Par exemple :

<span class="filename">Nom du fichier : src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-12-tuple-indexing/src/main.rs}}
```

Ce programme crée le tuple `x`, puis accède à chacun de ses éléments à l’aide de leurs indices respectifs. Comme dans la plupart des langages de programmation, le premier indice d’un tuple est 0.

Le tuple sans aucune valeur porte un nom spécial : _unité_. Cette valeur et son type correspondant s’écrivent tous deux `()` et représentent une valeur vide ou un type de retour vide. Les expressions renvoient implicitement la valeur unité si elles ne renvoient aucune autre valeur.

#### Type tableau

Un _tableau_ est une autre manière de regrouper plusieurs valeurs. Contrairement à un tuple, tous les éléments d’un tableau doivent être du même type. Contrairement aux tableaux de certains autres langages, les tableaux en Rust ont une longueur fixe.

Nous écrivons les valeurs d’un tableau sous la forme d’une liste séparée par des virgules entre crochets :

<span class="filename">Nom du fichier : src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-13-arrays/src/main.rs}}
```

Les tableaux sont utiles lorsque vous souhaitez que vos données soient allouées sur la pile, comme les autres types que nous avons vus jusqu’à présent, plutôt que sur le tas (nous aborderons plus en détail la pile et le tas au [chapitre 4][stack-and-heap]<!-- ignore -->), ou lorsque vous voulez vous assurer de toujours disposer d’un nombre fixe d’éléments. Les tableaux sont toutefois moins flexibles que le type vecteur. Un vecteur est un type de collection similaire fourni par la bibliothèque standard, qui peut grandir ou rétrécir, car son contenu se trouve sur le tas. Si vous ne savez pas s’il vaut mieux utiliser un tableau ou un vecteur, il y a de fortes chances que vous devriez utiliser un vecteur. Le [chapitre 8][vectors]<!-- ignore --> aborde les vecteurs plus en détail.

Les tableaux sont toutefois plus utiles lorsque vous savez que le nombre d’éléments n’aura pas besoin de changer. Par exemple, si vous utilisiez les noms des mois dans un programme, vous utiliseriez probablement un tableau plutôt qu’un vecteur, car vous savez qu’il contiendra toujours 12 éléments :

```rust
let months = ["January", "February", "March", "April", "May", "June", "July",
              "August", "September", "October", "November", "December"];
```

Vous écrivez le type d’un tableau entre crochets, avec le type de chaque élément, un point-virgule, puis le nombre d’éléments du tableau, comme ceci :

```rust
let a: [i32; 5] = [1, 2, 3, 4, 5];
```

Ici, `i32` est le type de chaque élément. Après le point-virgule, le nombre `5` indique que le tableau contient cinq éléments.

Vous pouvez aussi initialiser un tableau afin que tous ses éléments aient la même valeur en indiquant la valeur initiale, suivie d’un point-virgule, puis de la longueur du tableau entre crochets, comme ici :

```rust
let a = [3; 5];
```

Le tableau nommé `a` contiendra `5` éléments, tous initialisés à la valeur `3`. C’est équivalent à écrire `let a = [3, 3, 3, 3, 3];`, mais de manière plus concise.

<!-- Old headings. Do not remove or links may break. -->
<a id="accessing-array-elements"></a>

#### Accéder aux éléments d’un tableau

Un tableau est un bloc unique de mémoire de taille connue et fixe qui peut être alloué sur la pile. Vous pouvez accéder aux éléments d’un tableau par indexation, comme ceci :

<span class="filename">Nom du fichier : src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-14-array-indexing/src/main.rs}}
```

Dans cet exemple, la variable nommée `first` recevra la valeur `1`, car c’est la valeur à l’indice `[0]` du tableau. La variable nommée `second` recevra la valeur `2`, à l’indice `[1]` du tableau.

#### Accès invalide à un élément de tableau

Voyons ce qui se passe si vous essayez d’accéder à un élément situé au-delà de la fin du tableau. Supposons que vous exécutiez ce code, similaire au jeu de devinettes du chapitre 2, afin de récupérer un indice de tableau auprès de l’utilisateur :

<span class="filename">Nom du fichier : src/main.rs</span>

```rust,ignore,panics
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-15-invalid-array-access/src/main.rs}}
```

Ce code compile correctement. Si vous l’exécutez avec `cargo run` et saisissez `0`, `1`, `2`, `3` ou `4`, le programme affichera la valeur correspondante à cet indice dans le tableau. Si vous saisissez plutôt un nombre supérieur à la fin du tableau, comme `10`, vous verrez un résultat semblable à celui-ci :

<!-- manual-regeneration
cd listings/ch03-common-programming-concepts/no-listing-15-invalid-array-access
cargo run
10
-->

```console
thread 'main' panicked at src/main.rs:19:19:
index out of bounds: the len is 5 but the index is 10
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
```

Le programme a rencontré une erreur à l’exécution au moment d’utiliser une valeur invalide dans l’opération d’indexation. Le programme s’est terminé avec un message d’erreur et n’a pas exécuté l’instruction finale `println!`. Lorsque vous tentez d’accéder à un élément par indexation, Rust vérifie que l’indice spécifié est inférieur à la longueur du tableau. Si l’indice est supérieur ou égal à cette longueur, Rust panique. Cette vérification doit avoir lieu à l’exécution, en particulier dans ce cas, car le compilateur ne peut pas savoir à l’avance quelle valeur l’utilisateur saisira lorsqu’il exécutera le code.

C’est un exemple concret des principes de sécurité mémoire de Rust. Dans de nombreux langages de bas niveau, cette vérification n’est pas effectuée et, si vous fournissez un indice incorrect, il est possible d’accéder à une mémoire invalide. Rust vous protège contre ce type d’erreur en s’arrêtant immédiatement au lieu d’autoriser l’accès mémoire et de continuer. Le chapitre 9 aborde plus en détail la gestion des erreurs en Rust et explique comment écrire du code lisible et sûr qui ne panique pas et n’autorise pas l’accès à une mémoire invalide.

[comparing-the-guess-to-the-secret-number]: ch02-00-guessing-game-tutorial.html#comparing-the-guess-to-the-secret-number
[twos-complement]: https://en.wikipedia.org/wiki/Two%27s_complement
[control-flow]: ch03-05-control-flow.html#control-flow
[strings]: ch08-02-strings.html#storing-utf-8-encoded-text-with-strings
[stack-and-heap]: ch04-01-what-is-ownership.html#the-stack-and-the-heap
[vectors]: ch08-01-vectors.html
[unrecoverable-errors-with-panic]: ch09-01-unrecoverable-errors-with-panic.html
[appendix_b]: appendix-02-operators.md