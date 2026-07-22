## Le Type Slice

Les _slices_ vous permettent de référencer une séquence continue d'éléments dans une [collection](ch08-00-common-collections.md)<!-- ignore -->. Un slice est une sorte de référence, donc il n'a pas de propriété.

Voici un petit problème de programmation : Écrivez une fonction qui prend une chaîne de mots séparés par des espaces et renvoie le premier mot qu'elle trouve dans cette chaîne. Si la fonction ne trouve pas d'espace dans la chaîne, la chaîne entière doit être un mot, donc la chaîne entière doit être renvoyée.

> Remarque : Aux fins de l'introduction des slices, nous supposons uniquement l'ASCII dans cette section ; une discussion plus approfondie sur la gestion des UTF-8 se trouve dans la section [« Stockage de texte codé en UTF-8 avec des chaînes »][strings]<!-- ignore --> du Chapitre 8.

Voyons comment nous rédigerions la signature de cette fonction sans utiliser de slices, pour comprendre le problème que les slices vont résoudre :

```rust,ignore
fn premier_mot(s: &String) -> ?
```

La fonction `premier_mot` a un paramètre de type `&String`. Nous n'avons pas besoin de propriété, donc ceci est correct. (En Rust idiomatique, les fonctions ne prennent pas possession de leurs arguments à moins qu'elles n'en aient besoin, et les raisons de cela deviendront claires au fur et à mesure que nous avancerons.) Mais que devrions-nous renvoyer ? Nous n'avons pas vraiment de moyen de parler de *partie* d'une chaîne. Cependant, nous pourrions renvoyer l'index de la fin du mot, indiqué par un espace. Essayons cela, comme montré dans le Listing 4-7.

<Listing number="4-7" file-name="src/main.rs" caption="La fonction `premier_mot` qui renvoie un index d'octet dans le paramètre `String`">

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/listing-04-07/src/main.rs:here}}
```

</Listing>

Comme nous devons parcourir l'élément `String` élément par élément et vérifier si une valeur est un espace, nous allons convertir notre `String` en un tableau d'octets en utilisant la méthode `as_bytes`.

```rust,ignore
{{#rustdoc_include ../listings/ch04-understanding-ownership/listing-04-07/src/main.rs:as_bytes}}
```

Ensuite, nous créons un itérateur sur le tableau d'octets en utilisant la méthode `iter` :

```rust,ignore
{{#rustdoc_include ../listings/ch04-understanding-ownership/listing-04-07/src/main.rs:iter}}
```

Nous discuterons des iterators plus en détail dans [le Chapitre 13][ch13]<!-- ignore -->. Pour l'instant, sachez que `iter` est une méthode qui renvoie chaque élément d'une collection et que `enumerate` enveloppe le résultat de `iter` et renvoie chaque élément comme partie d'un tuple à la place. Le premier élément du tuple renvoyé par `enumerate` est l'index, et le deuxième élément est une référence à l'élément. Cela est un peu plus pratique que de calculer l'index nous-mêmes.

Parce que la méthode `enumerate` renvoie un tuple, nous pouvons utiliser des motifs pour déstructurer ce tuple. Nous aborderons les motifs plus en détail dans [le Chapitre 6][ch6]<!-- ignore -->. Dans la boucle `for`, nous spécifions un motif qui a `i` pour l'index dans le tuple et `&item` pour l'octet unique dans le tuple. Parce que nous obtenons une référence à l'élément de `.iter().enumerate()`, nous utilisons `&` dans le motif.

À l'intérieur de la boucle `for`, nous cherchons l'octet qui représente l'espace en utilisant la syntaxe littérale d'octets. Si nous trouvons un espace, nous renvoyons la position. Sinon, nous renvoyons la longueur de la chaîne en utilisant `s.len()`.

```rust,ignore
{{#rustdoc_include ../listings/ch04-understanding-ownership/listing-04-07/src/main.rs:inside_for}}
```

Nous avons maintenant un moyen de trouver l'index de la fin du premier mot dans la chaîne, mais il y a un problème. Nous renvoyons un `usize` à part, mais c'est un nombre seulement significatif dans le contexte du `&String`. En d'autres termes, comme c'est une valeur séparée de `String`, il n'y a aucune garantie qu'elle sera toujours valide à l'avenir. Considérez le programme dans le Listing 4-8 qui utilise la fonction `premier_mot` du Listing 4-7.

<Listing number="4-8" file-name="src/main.rs" caption="Stockage du résultat de l'appel à la fonction `premier_mot` puis changement du contenu de `String`">

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/listing-04-08/src/main.rs:here}}
```

</Listing>

Ce programme se compile sans erreur et le ferait également si nous utilisions `mot` après avoir appelé `s.clear()`. Comme `mot` n'est pas connecté à l'état de `s` du tout, `mot` contient toujours la valeur `5`. Nous pourrions utiliser cette valeur `5` avec la variable `s` pour essayer d'extraire le premier mot, mais ce serait un bug car le contenu de `s` a changé depuis que nous avons enregistré `5` dans `mot`.

Le fait de devoir se soucier de l'index dans `mot` se décalant par rapport aux données dans `s` est fastidieux et sujet aux erreurs ! Gérer ces indices est encore plus fragile si nous écrivons une fonction `deuxième_mot`. Sa signature devrait ressembler à ceci :

```rust,ignore
fn deuxieme_mot(s: &String) -> (usize, usize) {
```

Nous suivons maintenant un index de début _et_ de fin, et nous avons encore plus de valeurs qui ont été calculées à partir de données dans un état particulier mais ne sont pas liées à cet état. Nous avons trois variables non liées qui flottent et qui doivent rester synchronisées.

Heureusement, Rust a une solution à ce problème : les slices de chaînes.

### Slices de Chaînes

Un _slice de chaîne_ est une référence à une séquence continue des éléments d'une `String`, et il ressemble à ceci :

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-17-slice/src/main.rs:here}}
```

Plutôt qu'une référence à l'ensemble de `String`, `hello` est une référence à une portion de la `String`, spécifiée dans le morceau supplémentaire `[0..5]`. Nous créons des slices en utilisant une plage à l'intérieur de crochets en spécifiant `[index_de_début..index_de_fin]`, où _`index_de_début`_ est la première position dans le slice et _`index_de_fin`_ est un de plus que la dernière position dans le slice. En interne, la structure de données du slice stocke la position de départ et la longueur du slice, qui correspond à _`index_de_fin`_ moins _`index_de_début`_. Ainsi, dans le cas de `let monde = &s[6..11];`, `monde` serait un slice contenant un pointeur vers l'octet à l'index 6 de `s` avec une valeur de longueur de `5`.

La Figure 4-7 montre cela dans un diagramme.

<img alt="Trois tableaux : un tableau représentant les données sur la pile de s, qui pointe vers l'octet à l'index 0 dans un tableau des données de chaîne &quot;hello world&quot; sur le tas. Le troisième tableau représente les données sur la pile du slice monde, qui a une valeur de longueur de 5 et pointe vers l'octet 6 du tableau de données du tas."
src="img/trpl04-07.svg" class="center" style="width: 50%;" />

<span class="caption">Figure 4-7 : Un slice de chaîne se référant à une partie d'une `String`</span>

Avec la syntaxe de plage `..` de Rust, si vous souhaitez commencer à l'index 0, vous pouvez laisser tomber la valeur avant les deux points. En d'autres termes, ces deux expressions sont égales :

```rust
let s = String::from("hello");

let slice = &s[0..2];
let slice = &s[..2];
```

De la même manière, si votre slice comprend le dernier octet de la `String`, vous pouvez laisser tomber le nombre final. Cela signifie que ces deux expressions sont égales :

```rust
let s = String::from("hello");

let len = s.len();

let slice = &s[3..len];
let slice = &s[3..];
```

Vous pouvez également laisser tomber les deux valeurs pour obtenir un slice de l'ensemble de la chaîne. Donc, ces deux expressions sont égales :

```rust
let s = String::from("hello");

let len = s.len();

let slice = &s[0..len];
let slice = &s[..];
```

> Remarque : Les indices de plage de slice de chaînes doivent se situer à des frontières de caractères UTF-8 valides. Si vous essayez de créer un slice de chaîne au milieu d'un caractère multioctet, votre programme se terminera avec une erreur.

Avec toutes ces informations en tête, réécrivons `premier_mot` pour renvoyer un slice. Le type qui signifie « slice de chaîne » est écrit comme `&str` :

<Listing file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-18-first-word-slice/src/main.rs:here}}
```

</Listing>

Nous obtenons l'index pour la fin du mot de la même manière que nous l'avons fait dans le Listing 4-7, en cherchant la première occurrence d'un espace. Lorsque nous trouvons un espace, nous renvoyons un slice de chaîne en utilisant le début de la chaîne et l'index de l'espace comme indices de début et de fin.

Maintenant, quand nous appelons `premier_mot`, nous obtenons une seule valeur qui est liée aux données sous-jacentes. La valeur est composée d'une référence au point de départ du slice et du nombre d'éléments dans le slice.

Renvoyer un slice fonctionnerait également pour une fonction `deuxième_mot` :

```rust,ignore
fn deuxieme_mot(s: &String) -> &str {
```

Nous avons maintenant une API simple qui est beaucoup plus difficile à perturber car le compilateur s'assurera que les références dans la `String` restent valides. Rappelez-vous le bug dans le programme du Listing 4-8, lorsque nous avons obtenu l'index de la fin du premier mot mais avons ensuite vidé la chaîne afin que notre index soit invalide ? Ce code était logiquement incorrect mais n'a pas montré d'erreurs immédiates. Les problèmes apparaîtraient plus tard si nous continuions à essayer d'utiliser l'index du premier mot avec une chaîne vidée. Les slices rendent ce bug impossible et nous permettent de savoir beaucoup plus tôt que nous avons un problème avec notre code. Utiliser la version slice de `premier_mot` entraînera une erreur de compilation :

<Listing file-name="src/main.rs">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-19-slice-error/src/main.rs:here}}
```

</Listing>

Voici l'erreur du compilateur :

```console
{{#include ../listings/ch04-understanding-ownership/no-listing-19-slice-error/output.txt}}
```

Rappelez-vous des règles d'emprunt que si nous avons une référence immutable à quelque chose, nous ne pouvons pas également prendre une référence mutable. Puisque `clear` doit tronquer la `String`, il a besoin d'obtenir une référence mutable. Le `println!` après l'appel à `clear` utilise la référence dans `mot`, donc la référence immutable doit encore être active à ce moment-là. Rust interdit la référence mutable dans `clear` et la référence immutable dans `mot` d'exister en même temps, et la compilation échoue. Non seulement Rust a rendu notre API plus facile à utiliser, mais a également éliminé toute une classe d'erreurs à la compilation !

#### Les Littéraux de Chaînes comme Slices

Rappelez-vous que nous avons parlé des littéraux de chaînes étant stockés dans le binaire. Maintenant que nous savons ce qu'est un slice, nous pouvons comprendre correctement les littéraux de chaînes :

```rust
let s = "Hello, world!";
```

Le type de `s` ici est `&str` : C'est un slice pointant vers ce point spécifique du binaire. C'est aussi pourquoi les littéraux de chaînes sont immuables ; `&str` est une référence immuable.

#### Les Slices de Chaîne comme Paramètres

Savoir que vous pouvez prendre des slices de littéraux et de valeurs `String` nous mène à une amélioration supplémentaire de `premier_mot`, et c'est sa signature :

```rust,ignore
fn premier_mot(s: &String) -> &str {
```

Un Rustacean plus expérimenté écrirait plutôt la signature montrée dans le Listing 4-9 car cela nous permet d'utiliser la même fonction sur des valeurs `&String` et `&str`.

<Listing number="4-9" caption="Améliorer la fonction `premier_mot` en utilisant un slice de chaîne pour le type du paramètre `s`">

```rust,ignore
{{#rustdoc_include ../listings/ch04-understanding-ownership/listing-04-09/src/main.rs:here}}
```

</Listing>

Si nous avons un slice de chaîne, nous pouvons le passer directement. Si nous avons une `String`, nous pouvons passer un slice de la `String` ou une référence à la `String`. Cette flexibilité profite des coercitions de deref, une fonctionnalité que nous aborderons dans la section [« Utilisation des coercitions de deref dans les fonctions et méthodes »][deref-coercions]<!-- ignore --> du Chapitre 15.

Définir une fonction pour prendre un slice de chaîne plutôt qu'une référence à une `String` rend notre API plus générale et utile sans perdre aucune fonctionnalité :

<Listing file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/listing-04-09/src/main.rs:usage}}
```

</Listing>

### Autres Slices

Les slices de chaînes, comme vous pouvez l'imaginer, sont spécifiques aux chaînes. Mais il existe également un type de slice plus général. Considérons ce tableau :

```rust
let a = [1, 2, 3, 4, 5];
```

Tout comme nous pourrions vouloir référencer une partie d'une chaîne, nous pourrions vouloir référencer une partie d'un tableau. Nous le ferions comme ceci :

```rust
let a = [1, 2, 3, 4, 5];

let slice = &a[1..3];

assert_eq!(slice, &[2, 3]);
```

Ce slice a le type `&[i32]`. Il fonctionne de la même manière que les slices de chaînes, en stockant une référence au premier élément et une longueur. Vous utiliserez ce type de slice pour toutes sortes d'autres collections. Nous discuterons de ces collections en détail lorsque nous aborderons les vecteurs dans le Chapitre 8.

## Résumé

Les concepts de propriété, d'emprunt et de slices garantissent la sécurité mémoire dans les programmes Rust à la compilation. Le langage Rust vous donne un contrôle sur votre utilisation de la mémoire de la même manière que d'autres langages de programmation systèmes. Mais avoir le propriétaire des données qui nettoie automatiquement ces données lorsque le propriétaire sort du champ d'application signifie que vous n'avez pas à écrire et à déboguer du code supplémentaire pour obtenir ce contrôle.

La propriété affecte le fonctionnement de nombreuses autres parties de Rust, donc nous parlerons de ces concepts davantage tout au long du reste du livre. Passons au Chapitre 5 et voyons comment regrouper des morceaux de données ensemble dans une `struct`.