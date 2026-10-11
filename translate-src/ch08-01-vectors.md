## Stocker des listes de valeurs avec des vecteurs

Le premier type de collection que nous allons examiner est `Vec<T>`, également appelé vecteur. Les vecteurs vous permettent de stocker plusieurs valeurs dans une seule structure de données qui place toutes les valeurs les unes à côté des autres en mémoire. Les vecteurs ne peuvent stocker que des valeurs du même type. Ils sont utiles lorsque vous avez une liste d’éléments, comme les lignes de texte d’un fichier ou les prix des articles dans un panier.

### Créer un nouveau vecteur

Pour créer un nouveau vecteur vide, nous appelons la fonction `Vec::new`, comme indiqué dans l’exemple 8-1.

<Listing number="8-1" caption="Créer un nouveau vecteur vide pour contenir des valeurs de type `i32`">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-01/src/main.rs:here}}
```

</Listing>

Notez que nous avons ajouté une annotation de type ici. Comme nous n’insérons aucune valeur dans ce vecteur, Rust ne sait pas quel type d’éléments nous avons l’intention d’y stocker. C’est un point important. Les vecteurs sont implémentés à l’aide de génériques ; nous verrons au chapitre 10 comment utiliser les génériques avec vos propres types. Pour l’instant, sachez que le type `Vec<T>` fourni par la bibliothèque standard peut contenir n’importe quel type. Lorsque nous créons un vecteur destiné à contenir un type précis, nous pouvons spécifier ce type entre chevrons. Dans l’exemple 8-1, nous avons indiqué à Rust que `Vec<T>` dans `v` contiendra des éléments de type `i32`.

Le plus souvent, vous créerez un `Vec<T>` avec des valeurs initiales, et Rust déduira le type de valeur que vous souhaitez stocker. Vous aurez donc rarement besoin d’ajouter cette annotation de type. Rust fournit la macro pratique `vec!`, qui crée un nouveau vecteur contenant les valeurs que vous lui donnez. L’exemple 8-2 crée un nouveau `Vec<i32>` contenant les valeurs `1`, `2` et `3`. Le type entier est `i32`, car c’est le type entier par défaut, comme nous l’avons vu dans la section [« Types de données »][data-types]<!-- ignore --> du chapitre 3.

<Listing number="8-2" caption="Créer un nouveau vecteur contenant des valeurs">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-02/src/main.rs:here}}
```

</Listing>

Comme nous avons fourni des valeurs initiales de type `i32`, Rust peut déduire que le type de `v` est `Vec<i32>` ; l’annotation de type n’est donc pas nécessaire. Voyons maintenant comment modifier un vecteur.

### Mettre à jour un vecteur

Pour créer un vecteur puis y ajouter des éléments, nous pouvons utiliser la méthode `push`, comme indiqué dans l’exemple 8-3.

<Listing number="8-3" caption="Utiliser la méthode `push` pour ajouter des valeurs à un vecteur">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-03/src/main.rs:here}}
```

</Listing>

Comme pour toute variable, si nous voulons pouvoir modifier sa valeur, nous devons la rendre mutable à l’aide du mot-clé `mut`, comme nous l’avons vu au chapitre 3. Les nombres que nous plaçons dans le vecteur sont tous de type `i32`, et Rust le déduit à partir des données ; nous n’avons donc pas besoin de l’annotation `Vec<i32>`.

### Lire les éléments d’un vecteur

Il existe deux façons de référencer une valeur stockée dans un vecteur : utiliser un index ou la méthode `get`. Dans les exemples suivants, nous avons annoté les types des valeurs renvoyées par ces fonctions pour plus de clarté.

L’exemple 8-4 présente les deux méthodes permettant d’accéder à une valeur dans un vecteur : la syntaxe d’indexation et la méthode `get`.

<Listing number="8-4" caption="Utiliser la syntaxe d’indexation et la méthode `get` pour accéder à un élément d’un vecteur">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-04/src/main.rs:here}}
```

</Listing>

Notez quelques détails. Nous utilisons l’index `2` pour obtenir le troisième élément, car les vecteurs sont indexés par des nombres à partir de zéro. L’utilisation de `&` et de `[]` nous donne une référence à l’élément situé à cet index. Lorsque nous utilisons la méthode `get` en lui passant l’index comme argument, nous obtenons un `Option<&T>` que nous pouvons utiliser avec `match`.

Rust propose ces deux façons de référencer un élément afin que vous puissiez choisir le comportement du programme lorsque vous essayez d’utiliser un index qui se trouve en dehors de la plage des éléments existants. Voyons, par exemple, ce qui se passe lorsque nous avons un vecteur de cinq éléments et que nous essayons ensuite d’accéder à l’élément situé à l’index 100 avec chacune de ces méthodes, comme indiqué dans l’exemple 8-5.

<Listing number="8-5" caption="Tenter d’accéder à l’élément situé à l’index 100 dans un vecteur contenant cinq éléments">

```rust,should_panic,panics
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-05/src/main.rs:here}}
```

</Listing>

Lorsque nous exécutons ce code, la première méthode `[]` provoque une panique du programme, car elle référence un élément inexistant. Cette méthode convient particulièrement si vous voulez que votre programme s’arrête lorsqu’on tente d’accéder à un élément situé après la fin du vecteur.

Lorsque la méthode `get` reçoit un index situé en dehors du vecteur, elle renvoie `None` sans provoquer de panique. Vous utiliseriez cette méthode si l’accès à un élément en dehors de la plage du vecteur peut se produire occasionnellement dans des circonstances normales. Votre code devra alors gérer le cas où il reçoit `Some(&element)` ou `None`, comme nous l’avons vu au chapitre 6. Par exemple, l’index peut provenir d’un nombre saisi par une personne. Si elle saisit accidentellement un nombre trop grand et que le programme reçoit une valeur `None`, vous pouvez lui indiquer combien d’éléments contient le vecteur actuel et lui donner une nouvelle chance de saisir une valeur valide. Ce serait plus convivial que de faire planter le programme à cause d’une faute de frappe !

Lorsque le programme dispose d’une référence valide, l’emprunteur vérifie le respect des règles de propriété et d’emprunt (présentées au chapitre 4) afin de garantir que cette référence et toute autre référence au contenu du vecteur restent valides. Rappelez-vous la règle selon laquelle vous ne pouvez pas avoir de références mutables et immutables dans une même portée. Cette règle s’applique dans l’exemple 8-6, où nous conservons une référence immuable au premier élément d’un vecteur et essayons d’ajouter un élément à la fin. Ce programme ne fonctionnera pas si nous essayons également de référencer cet élément plus tard dans la fonction.

<Listing number="8-6" caption="Tenter d’ajouter un élément à un vecteur tout en conservant une référence à un élément">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-06/src/main.rs:here}}
```

</Listing>

La compilation de ce code produira l’erreur suivante :

```console
{{#include ../listings/ch08-common-collections/listing-08-06/output.txt}}
```

Le code de l’exemple 8-6 peut sembler devoir fonctionner : pourquoi une référence au premier élément serait-elle affectée par des modifications à la fin du vecteur ? Cette erreur est due au fonctionnement des vecteurs : comme les vecteurs placent les valeurs les unes à côté des autres en mémoire, l’ajout d’un nouvel élément à la fin du vecteur peut nécessiter l’allocation d’une nouvelle zone mémoire et la copie des anciens éléments dans ce nouvel espace, s’il n’y a pas assez de place pour placer tous les éléments côte à côte à l’endroit où le vecteur est actuellement stocké. Dans ce cas, la référence au premier élément pointerait vers une zone mémoire désallouée. Les règles d’emprunt empêchent les programmes de se retrouver dans cette situation.

> Remarque : pour en savoir plus sur les détails d’implémentation du type `Vec<T>`, consultez [« The Rustonomicon »][nomicon].

### Parcourir les valeurs d’un vecteur

Pour accéder successivement à chaque élément d’un vecteur, nous parcourrions tous les éléments plutôt que d’utiliser des index pour y accéder un par un. L’exemple 8-7 montre comment utiliser une boucle `for` pour obtenir des références immuables à chaque élément d’un vecteur de valeurs `i32` et les afficher.

<Listing number="8-7" caption="Afficher chaque élément d’un vecteur en parcourant les éléments avec une boucle `for`">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-07/src/main.rs:here}}
```

</Listing>

Nous pouvons également parcourir les références mutables à chaque élément d’un vecteur mutable afin de modifier tous les éléments. La boucle `for` de l’exemple 8-8 ajoute `50` à chaque élément.

<Listing number="8-8" caption="Parcourir les références mutables aux éléments d’un vecteur">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-08/src/main.rs:here}}
```

</Listing>

Pour modifier la valeur vers laquelle pointe la référence mutable, nous devons utiliser l’opérateur de déréférencement `*` afin d’accéder à la valeur de `i` avant de pouvoir utiliser l’opérateur `+=`. Nous parlerons davantage de l’opérateur de déréférencement dans la section [« Suivre le pointeur jusqu’à la valeur avec l’opérateur de déréférencement »][deref]<!-- ignore --> du chapitre 15.

Parcourir un vecteur, qu’il soit immuable ou mutable, est sûr grâce aux règles de l’emprunteur. Si nous essayions d’insérer ou de supprimer des éléments dans le corps des boucles `for` des exemples 8-7 et 8-8, nous obtiendrions une erreur de compilation similaire à celle produite par le code de l’exemple 8-6. La référence au vecteur détenue par la boucle `for` empêche toute modification simultanée du vecteur entier.

### Utiliser une énumération pour stocker plusieurs types

Les vecteurs ne peuvent stocker que des valeurs d’un même type. Cela peut être gênant ; il existe bel et bien des cas où il est nécessaire de stocker une liste d’éléments de types différents. Heureusement, les variantes d’une énumération sont définies sous un même type d’énumération. Ainsi, lorsque nous avons besoin d’un type pour représenter des éléments de types différents, nous pouvons définir et utiliser une énumération !

Par exemple, supposons que nous voulions récupérer les valeurs d’une ligne d’un tableur dont certaines colonnes contiennent des entiers, d’autres des nombres à virgule flottante et d’autres encore des chaînes de caractères. Nous pouvons définir une énumération dont les variantes contiendront les différents types de valeurs. Toutes les variantes de l’énumération seront alors considérées comme ayant le même type : celui de l’énumération. Nous pouvons ensuite créer un vecteur pour contenir cette énumération et, par conséquent, des valeurs de types différents. L’exemple 8-9 illustre cette approche.

<Listing number="8-9" caption="Définir une énumération pour stocker des valeurs de types différents dans un même vecteur">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-09/src/main.rs:here}}
```

</Listing>

Rust doit connaître les types qui seront présents dans le vecteur au moment de la compilation afin de savoir exactement quelle quantité de mémoire sur le tas sera nécessaire pour stocker chaque élément. Nous devons également préciser quels types sont autorisés dans ce vecteur. Si Rust autorisait un vecteur à contenir n’importe quel type, il serait possible qu’un ou plusieurs de ces types provoquent des erreurs lors des opérations effectuées sur les éléments du vecteur. L’utilisation d’une énumération associée à une expression `match` permet à Rust de s’assurer à la compilation que tous les cas possibles sont traités, comme nous l’avons vu au chapitre 6.

Si vous ne connaissez pas l’ensemble exhaustif des types que le programme recevra à l’exécution pour les stocker dans un vecteur, la technique de l’énumération ne fonctionnera pas. Vous pouvez alors utiliser un objet de trait, que nous verrons au chapitre 18.

Maintenant que nous avons abordé quelques-unes des façons les plus courantes d’utiliser les vecteurs, n’oubliez pas de consulter [la documentation de l’API][vec-api]<!-- ignore --> pour découvrir les nombreuses méthodes utiles définies sur `Vec<T>` par la bibliothèque standard. Par exemple, en plus de `push`, une méthode `pop` supprime et renvoie le dernier élément.

### La suppression d’un vecteur supprime ses éléments

Comme toute autre `struct`, un vecteur est libéré lorsqu’il sort de portée, comme indiqué dans l’exemple 8-10.

<Listing number="8-10" caption="Montrer à quel moment le vecteur et ses éléments sont supprimés">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-10/src/main.rs:here}}
```

</Listing>

Lorsque le vecteur est supprimé, tout son contenu l’est également, ce qui signifie que les entiers qu’il contient sont libérés. L’emprunteur garantit que les références au contenu d’un vecteur ne sont utilisées que tant que le vecteur lui-même est valide.

Passons maintenant au type de collection suivant : `String` !

[data-types]: ch03-02-data-types.html#data-types
[nomicon]: ../nomicon/vec/vec.html
[vec-api]: ../std/vec/struct.Vec.html
[deref]: ch15-02-deref.html#following-the-pointer-to-the-value-with-the-dereference-operator