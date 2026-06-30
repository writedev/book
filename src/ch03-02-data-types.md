## Types de Données

Chaque valeur en Rust est d'un certain _type de données_ qui indique à Rust quel type de données est spécifié afin qu'il sache comment travailler avec ces données. Nous allons examiner deux sous-ensembles de types de données : les scalaires et les composés.

Gardez à l'esprit que Rust est un langage _typer statiquement_, ce qui signifie qu'il doit connaître les types de toutes les variables au moment de la compilation. Le compilateur peut généralement inférer quel type nous voulons utiliser en fonction de la valeur et de la manière dont nous l'utilisons. Dans les cas où de nombreux types sont possibles, par exemple lorsque nous avons converti une `String` en un type numérique en utilisant `parse` dans la section [« Comparer le Devinez au Nombre Secret »][comparing-the-guess-to-the-secret-number]<!-- ignore --> au Chapitre 2, nous devons ajouter une annotation de type, comme ceci :

```rust
let guess: u32 = "42".parse().expect("Ce n'est pas un nombre !");
```

Si nous n'ajoutons pas l'annotation de type `: u32` montrée dans le code précédent, Rust affichera l'erreur suivante, ce qui signifie que le compilateur a besoin de plus d'informations de notre part pour savoir quel type nous voulons utiliser :

```console
{{#include ../listings/ch03-common-programming-concepts/output-only-01-no-type-annotations/output.txt}}
```

Vous verrez différentes annotations de type pour d'autres types de données.

### Types Scalaires

Un type _scalaire_ représente une seule valeur. Rust a quatre types scalaires principaux : les entiers, les nombres à virgule flottante, les booléens et les caractères. Vous pouvez les reconnaître d'autres langages de programmation. Explorons comment ils fonctionnent en Rust.

#### Types Entiers

Un _entier_ est un nombre sans composante fractionnaire. Nous avons utilisé un type entier dans le Chapitre 2, le type `u32`. Cette déclaration de type indique que la valeur qui lui est associée doit être un entier non signé (les types d'entiers signés commencent par `i` au lieu de `u`) qui prend 32 bits d'espace. Le tableau 3-1 montre les types d'entiers intégrés en Rust. Nous pouvons utiliser n'importe lequel de ces variants pour déclarer le type d'une valeur entière.

<span class="caption">Tableau 3-1 : Types Entiers en Rust</span>

| Longueur  | Signé  | Non Signé |
| --------- | ------ | --------- |
| 8 bits    | `i8`   | `u8`      |
| 16 bits   | `i16`  | `u16`     |
| 32 bits   | `i32`  | `u32`     |
| 64 bits   | `i64`  | `u64`     |
| 128 bits  | `i128` | `u128`    |
| Dépendant de l'architecture | `isize` | `usize` |

Chaque variant peut être soit signé soit non signé et a une taille explicite. _Signé_ et _non signé_ se réfèrent à la possibilité que le nombre soit négatif — en d'autres termes, si le nombre doit être accompagné d'un signe (signé) ou s'il sera toujours positif et peut donc être représenté sans signe (non signé). C'est comme écrire des nombres sur papier : lorsque le signe est important, un nombre est montré avec un signe plus ou moins ; cependant, lorsqu’il est sûr de supposer que le nombre est positif, il est montré sans signe. Les nombres signés sont stockés en utilisant la représentation [complément à deux][twos-complement]<!-- ignore -->.

Chaque variant signé peut stocker des nombres de −(2<sup>n − 1</sup>) à 2<sup>n − 1</sup> − 1 inclus, où _n_ est le nombre de bits que ce variant utilise. Ainsi, un `i8` peut stocker des nombres de −(2<sup>7</sup>) à 2<sup>7</sup> − 1, ce qui équivaut à −128 à 127. Les variants non signés peuvent stocker des nombres de 0 à 2<sup>n</sup> − 1, donc un `u8` peut stocker des nombres de 0 à 2<sup>8</sup> − 1, ce qui équivaut à 0 à 255.

De plus, les types `isize` et `usize` dépendent de l'architecture de l'ordinateur sur lequel votre programme s'exécute : 64 bits si vous êtes sur une architecture 64 bits et 32 bits si vous êtes sur une architecture 32 bits.

Vous pouvez écrire des littéraux entiers dans l'une des formes montrées dans le tableau 3-2. Notez que les littéraux numériques qui peuvent être de plusieurs types numériques permettent une suffixe de type, tel que `57u8`, pour désigner le type. Les littéraux numériques peuvent également utiliser `_` comme séparateur visuel pour rendre le nombre plus facile à lire, tel que `1_000`, qui aura la même valeur que si vous aviez spécifié `1000`.

<span class="caption">Tableau 3-2 : Littéraux Entiers en Rust</span>

| Littéraux numériques  | Exemple       |
| --------------------- | ------------- |
| Décimal               | `98_222`      |
| Hexadécimal           | `0xff`        |
| Octal                 | `0o77`        |
| Binaire               | `0b1111_0000` |
| Octet (`u8` seulement)| `b'A'`        |

Alors, comment savez-vous quel type d'entier utiliser ? Si vous n'êtes pas sûr, les valeurs par défaut de Rust sont généralement de bons points de départ : Les types entiers par défaut sont `i32`. La principale situation dans laquelle vous utiliseriez `isize` ou `usize` est lors de l'indexation d'un certain type de collection.

> ##### Débordement d'entier
>
> Disons que vous avez une variable de type `u8` qui peut contenir des valeurs entre 0 et 255. Si vous essayez de modifier la variable à une valeur en dehors de cette plage, comme 256, un _débordement d'entier_ se produira, ce qui peut entraîner l'un des deux comportements. Lorsque vous compilez en mode débogage, Rust inclut des vérifications pour le débordement d'entier qui provoquent une _panique_ à l'exécution si ce comportement se produit. Rust utilise le terme _panique_ lorsqu'un programme se termine avec une erreur ; nous aborderons les panics plus en détail dans la section [« Erreurs Non Récupérables avec `panic!` »][unrecoverable-errors-with-panic]<!-- ignore --> au Chapitre 9.
>
> Lorsque vous compilez en mode de publication avec le drapeau `--release`, Rust _n'inclut pas_ de vérifications pour le débordement d'entier qui provoquent des panics. Au lieu de cela, si un débordement se produit, Rust effectue un _wrapping en complément à deux_. En résumé, les valeurs supérieures à la valeur maximale que le type peut contenir "se replient" sur le minimum des valeurs que le type peut contenir. Dans le cas d'un `u8`, la valeur 256 devient 0, la valeur 257 devient 1, et ainsi de suite. Le programme ne panique pas, mais la variable aura une valeur qui n'est probablement pas ce que vous attendiez. Compter sur le comportement de repli du débordement d'entier est considéré comme une erreur.
>
> Pour gérer explicitement la possibilité d'un débordement, vous pouvez utiliser ces familles de méthodes fournies par la bibliothèque standard pour les types numériques primitifs :
>
> - Envelopper dans tous les modes avec les méthodes `wrapping_*`, telles que `wrapping_add`.
> - Retourner la valeur `None` s'il y a un débordement avec les méthodes `checked_*`.
> - Retourner la valeur et un booléen indiquant s'il y a eu un débordement avec les méthodes `overflowing_*`.
> - Saturer aux valeurs minimum ou maximum de la valeur avec les méthodes `saturating_*`.

#### Types à Virgule Flottante

Rust a également deux types primitifs pour les _nombres à virgule flottante_, qui sont des nombres avec des points décimaux. Les types à virgule flottante de Rust sont `f32` et `f64`, qui sont de taille 32 bits et 64 bits, respectivement. Le type par défaut est `f64` car, sur des CPU modernes, il est à peu près aussi rapide que `f32` mais capable de plus de précision. Tous les types à virgule flottante sont signés.

Voici un exemple qui montre des nombres à virgule flottante en action :

<span class="filename">Nom de fichier : src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-06-floating-point/src/main.rs}}
```

Les nombres à virgule flottante sont représentés selon la norme IEEE-754.

#### Opérations Numériques

Rust prend en charge les opérations mathématiques de base que vous attendez pour tous les types de nombres : addition, soustraction, multiplication, division et reste. La division entière tronque vers zéro au nombre entier le plus proche. Le code suivant montre comment vous utiliseriez chaque opération numérique dans une instruction `let` :

<span class="filename">Nom de fichier : src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-07-numeric-operations/src/main.rs}}
```

Chaque expression dans ces instructions utilise un opérateur mathématique et évalue à une seule valeur, qui est ensuite liée à une variable. [L'Annexe B][appendix_b]<!-- ignore --> contient une liste de tous les opérateurs que Rust fournit.

#### Le Type Booléen

Comme dans la plupart des autres langages de programmation, un type booléen en Rust a deux valeurs possibles : `true` et `false`. Les booléens font un octet de taille. Le type booléen en Rust est spécifié à l'aide de `bool`. Par exemple :

<span class="filename">Nom de fichier : src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-08-boolean/src/main.rs}}
```

La principale façon d'utiliser des valeurs booléennes est à travers des conditionnelles, comme une expression `if`. Nous couvrirons comment fonctionnent les expressions `if` en Rust dans la section [« Flux de Contrôle »][control-flow]<!-- ignore -->.

#### Le Type Caractère

Le type `char` de Rust est le type alphabetique le plus primitif du langage. Voici quelques exemples de déclaration de valeurs `char` :

<span class="filename">Nom de fichier : src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-09-char/src/main.rs}}
```

Notez que nous spécifions des littéraux `char` avec des marques de citation simples, contrairement aux littéraux de chaînes qui utilisent des marques de citation doubles. Le type `char` de Rust est de 4 octets et représente une valeur scalaire Unicode, ce qui signifie qu'il peut représenter beaucoup plus que de simples caractères ASCII. Les lettres accentuées ; les caractères chinois, japonais et coréens ; les émojis ; et les espaces à largeur nulle sont tous des valeurs `char` valides en Rust. Les valeurs scalaires Unicode vont de `U+0000` à `U+D7FF` et de `U+E000` à `U+10FFFF` inclus. Cependant, un "caractère" n'est pas vraiment un concept en Unicode, donc votre intuition humaine de ce qu'est un "caractère" peut ne pas correspondre à ce qu'est un `char` en Rust. Nous discuterons de ce sujet en détail dans [« Stocker du Texte Encodé en UTF-8 avec des Chaînes »][strings]<!-- ignore --> au Chapitre 8.

### Types Composés

Les _types composés_ peuvent regrouper plusieurs valeurs en un seul type. Rust a deux types composés primitifs : les tuples et les tableaux.

#### Le Type Tuple

Un _tuple_ est une manière générale de regrouper un certain nombre de valeurs de différents types en un seul type composé. Les tuples ont une longueur fixe : Une fois déclarés, ils ne peuvent pas croître ni diminuer en taille.

Nous créons un tuple en écrivant une liste de valeurs séparées par des virgules à l'intérieur de parenthèses. Chaque position dans le tuple a un type, et les types des différentes valeurs dans le tuple n'ont pas à être les mêmes. Nous avons ajouté des annotations de type optionnelles dans cet exemple :

<span class="filename">Nom de fichier : src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-10-tuples/src/main.rs}}
```

La variable `tup` est liée à l'ensemble du tuple car un tuple est considéré comme un seul élément composé. Pour obtenir les valeurs individuelles d'un tuple, nous pouvons utiliser le pattern matching pour destructurer une valeur de tuple, comme ceci :

<span class="filename">Nom de fichier : src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-11-destructuring-tuples/src/main.rs}}
```

Ce programme crée d'abord un tuple et le lie à la variable `tup`. Il utilise ensuite un motif avec `let` pour prendre `tup` et le transformer en trois variables distinctes, `x`, `y`, et `z`. Cela s'appelle _destructuration_ car cela sépare le tuple unique en trois parties. Enfin, le programme imprime la valeur de `y`, qui est `6.4`.

Nous pouvons également accéder à un élément de tuple directement en utilisant un point (`.`) suivi de l'index de la valeur que nous voulons accéder. Par exemple :

<span class="filename">Nom de fichier : src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-12-tuple-indexing/src/main.rs}}
```

Ce programme crée le tuple `x` puis accède à chaque élément du tuple en utilisant leurs indices respectifs. Comme dans la plupart des langages de programmation, le premier indice d'un tuple est 0.

Le tuple sans aucune valeur a un nom spécial, _unité_. Cette valeur et son type correspondant sont tous deux écrits `()` et représentent une valeur vide ou un type de retour vide. Les expressions retournent implicitement la valeur d'unité si elles ne retournent aucune autre valeur.

#### Le Type Tableau

Une autre façon d'avoir une collection de plusieurs valeurs est avec un _tableau_. Contrairement à un tuple, chaque élément d'un tableau doit avoir le même type. Contrairement aux tableaux dans d'autres langages, les tableaux en Rust ont une taille fixe.

Nous écrivons les valeurs dans un tableau comme une liste séparée par des virgules à l'intérieur de crochets :

<span class="filename">Nom de fichier : src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-13-arrays/src/main.rs}}
```

Les tableaux sont utiles lorsque vous souhaitez que vos données soient allouées sur la pile, tout comme les autres types que nous avons vus jusqu'à présent, plutôt que sur le tas (nous discuterons de la pile et du tas plus en détail dans [Chapitre 4][stack-and-heap]<!-- ignore -->) ou lorsque vous souhaitez vous assurer que vous avez toujours un nombre fixe d'éléments. Un tableau n'est pas aussi flexible que le type vecteur, cependant. Un vecteur est un type de collection similaire fourni par la bibliothèque standard qui _peut_ croître ou diminuer en taille car son contenu vit sur le tas. Si vous n'êtes pas sûr d'utiliser un tableau ou un vecteur, il y a de fortes chances que vous devriez utiliser un vecteur. Le [Chapitre 8][vectors]<!-- ignore --> traite des vecteurs en détail.

Cependant, les tableaux sont plus utiles lorsque vous savez que le nombre d'éléments ne changera pas. Par exemple, si vous utilisiez les noms des mois dans un programme, vous utiliseriez probablement un tableau plutôt qu'un vecteur car vous savez qu'il contiendra toujours 12 éléments :

```rust
let months = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet",
              "Août", "Septembre", "Octobre", "Novembre", "Décembre"];
```

Vous écrivez le type d'un tableau en utilisant des crochets avec le type de chaque élément, un point-virgule, puis le nombre d'éléments dans le tableau, comme ceci :

```rust
let a: [i32; 5] = [1, 2, 3, 4, 5];
```

Ici, `i32` est le type de chaque élément. Après le point-virgule, le nombre `5` indique que le tableau contient cinq éléments.

Vous pouvez également initialiser un tableau pour contenir la même valeur pour chaque élément en spécifiant la valeur initiale, suivie d'un point-virgule, puis la longueur du tableau entre crochets, comme montré ici :

```rust
let a = [3; 5];
```

Le tableau nommé `a` contiendra `5` éléments qui seront tous initialement réglés sur la valeur `3`. C'est la même chose que d'écrire `let a = [3, 3, 3, 3, 3];` mais de manière plus concise.

<!-- Anciennes rubriques. Ne pas supprimer ou les liens pourraient casser. -->
<a id="accessing-array-elements"></a>

#### Accès aux Éléments du Tableau

Un tableau est un seul bloc de mémoire de taille connue et fixe qui peut être alloué sur la pile. Vous pouvez accéder aux éléments d'un tableau en utilisant l'indexation, comme ceci :

<span class="filename">Nom de fichier : src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-14-array-indexing/src/main.rs}}
```

Dans cet exemple, la variable nommée `first` obtiendra la valeur `1` car c'est la valeur à l'index `[0]` dans le tableau. La variable nommée `second` obtiendra la valeur `2` de l'index `[1]` dans le tableau.

#### Accès Invalide aux Éléments du Tableau

Voyons ce qui se passe si vous essayez d'accéder à un élément d'un tableau qui est au-delà de la fin du tableau. Disons que vous exécutez ce code, similaire au jeu de devinettes dans le Chapitre 2, pour obtenir un index de tableau de l'utilisateur :

<span class="filename">Nom de fichier : src/main.rs</span>

```rust,ignore,panics
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-15-invalid-array-access/src/main.rs}}
```

Ce code se compile avec succès. Si vous exécutez ce code en utilisant `cargo run` et entrez `0`, `1`, `2`, `3`, ou `4`, le programme affichera la valeur correspondante à cet index dans le tableau. Si vous entrez au lieu un nombre supérieur à la fin du tableau, comme `10`, vous verrez une sortie comme celle-ci :

```console
thread 'main' panicked at src/main.rs:19:19:
index out of bounds: the len is 5 but the index is 10
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
```

Le programme a entraîné une erreur d'exécution au moment de l'utilisation d'une valeur invalide dans l'opération d'indexation. Le programme s'est terminé avec un message d'erreur et n'a pas exécuté la dernière instruction `println!`. Lorsque vous essayez d'accéder à un élément en utilisant l'indexation, Rust vérifiera que l'index que vous avez spécifié est inférieur à la longueur du tableau. Si l'index est supérieur ou égal à la longueur, Rust panique. Cette vérification doit se faire à l'exécution, surtout dans ce cas, car le compilateur ne peut pas savoir quel valeur un utilisateur entrera lorsqu'il exécutera le code plus tard.

Ceci est un exemple des principes de sécurité de la mémoire de Rust en action. Dans de nombreux langages bas niveaux, ce type de vérification n'est pas effectué, et lorsque vous fournissez un index incorrect, une mémoire invalide peut être accessible. Rust vous protège contre ce type d'erreur en sortant immédiatement au lieu de permettre l'accès à la mémoire et de continuer. Le Chapitre 9 discute davantage de la gestion des erreurs de Rust et comment vous pouvez écrire un code lisible et sûr qui ne panique ni n'autorise l'accès à une mémoire invalide.

[comparing-the-guess-to-the-secret-number]: ch02-00-guessing-game-tutorial.html#comparing-the-guess-to-the-secret-number
[twos-complement]: https://en.wikipedia.org/wiki/Two%27s_complement
[control-flow]: ch03-05-control-flow.html#control-flow
[strings]: ch08-02-strings.html#storing-utf-8-encoded-text-with-strings
[stack-and-heap]: ch04-01-what-is-ownership.html#the-stack-and-the-heap
[vectors]: ch08-01-vectors.html
[unrecoverable-errors-with-panic]: ch09-01-unrecoverable-errors-with-panic.html
[appendix_b]: appendix-02-operators.md