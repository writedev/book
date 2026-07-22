## Stocker des listes de valeurs avec des vecteurs

Le premier type de collection que nous allons examiner est `Vec<T>`, également connu sous le nom de vecteur. Les vecteurs vous permettent de stocker plus d'une valeur dans une seule structure de données qui place toutes les valeurs les unes à côté des autres en mémoire. Les vecteurs ne peuvent stocker que des valeurs du même type. Ils sont utiles lorsque vous avez une liste d'éléments, comme les lignes de texte dans un fichier ou les prix des articles dans un panier.

### Créer un nouveau vecteur

Pour créer un nouveau vecteur vide, nous appelons la fonction `Vec::new`, comme illustré dans l'Listing 8-1.

<Listing number="8-1" caption="Création d'un nouveau vecteur vide pour contenir des valeurs de type `i32`">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-01/src/main.rs:here}}
```

</Listing>

Notez que nous avons ajouté une annotation de type ici. Comme nous n'insérons aucune valeur dans ce vecteur, Rust ne sait pas quel type d'éléments nous voulons stocker. C'est un point important. Les vecteurs sont implémentés en utilisant des génériques ; nous verrons comment utiliser des génériques avec vos propres types dans le Chapitre 10. Pour l'instant, sachez que le type `Vec<T>` fourni par la bibliothèque standard peut contenir n'importe quel type. Lorsque nous créons un vecteur pour contenir un type spécifique, nous pouvons spécifier le type entre crochets angulaires. Dans l'Listing 8-1, nous avons dit à Rust que le `Vec<T>` dans `v` contiendra des éléments de type `i32`.

Plus souvent, vous créerez un `Vec<T>` avec des valeurs initiales, et Rust inférera le type de valeur que vous souhaitez stocker, donc vous n'avez rarement besoin de faire cette annotation de type. Rust fournit de manière pratique le macro `vec!`, qui créera un nouveau vecteur contenant les valeurs que vous lui donnez. L'Listing 8-2 crée un nouveau `Vec<i32>` contenant les valeurs `1`, `2` et `3`. Le type entier est `i32` parce que c'est le type entier par défaut, comme nous l'avons discuté dans la section [“Types de données”][data-types]<!-- ignore --> du Chapitre 3.

<Listing number="8-2" caption="Création d'un nouveau vecteur contenant des valeurs">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-02/src/main.rs:here}}
```

</Listing>

Puisque nous avons donné des valeurs initiales `i32`, Rust peut inférer que le type de `v` est `Vec<i32>`, et l'annotation de type n'est pas nécessaire. Ensuite, nous allons voir comment modifier un vecteur.

### Mettre à jour un vecteur

Pour créer un vecteur puis ajouter des éléments, nous pouvons utiliser la méthode `push`, comme montré dans l'Listing 8-3.

<Listing number="8-3" caption="Utilisation de la méthode `push` pour ajouter des valeurs à un vecteur">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-03/src/main.rs:here}}
```

</Listing>

Comme pour toute variable, si nous voulons pouvoir changer sa valeur, nous devons la rendre mutable en utilisant le mot-clé `mut`, comme discuté dans le Chapitre 3. Les nombres que nous mettons à l'intérieur sont tous de type `i32`, et Rust en infère ce type à partir des données, donc nous n'avons pas besoin de l'annotation `Vec<i32>`.

### Lire des éléments des vecteurs

Il existe deux façons de référencer une valeur stockée dans un vecteur : par indexation ou en utilisant la méthode `get`. Dans les exemples suivants, nous avons annoté les types des valeurs retournées par ces fonctions pour plus de clarté.

L'Listing 8-4 montre les deux méthodes d'accès à une valeur dans un vecteur, avec la syntaxe d'indexation et la méthode `get`.

<Listing number="8-4" caption="Utilisation de la syntaxe d'indexation et de la méthode `get` pour accéder à un élément dans un vecteur">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-04/src/main.rs:here}}
```

</Listing>

Notez quelques détails ici. Nous utilisons la valeur d'index `2` pour obtenir le troisième élément parce que les vecteurs sont indexés par numéro, en commençant à zéro. L'utilisation de `&` et `[]` nous donne une référence à l'élément à la valeur d'index. Lorsque nous utilisons la méthode `get` avec l'index passé en argument, nous obtenons un `Option<&T>` que nous pouvons utiliser avec `match`.

Rust fournit ces deux façons de référencer un élément afin que vous puissiez choisir comment le programme se comporte lorsque vous essayez d'utiliser une valeur d'index en dehors de la plage des éléments existants. Par exemple, voyons ce qui se passe lorsque nous avons un vecteur de cinq éléments et que nous essayons d'accéder à un élément à l'index 100 avec chaque technique, comme montré dans l'Listing 8-5.

<Listing number="8-5" caption="Tentative d'accès à l'élément à l'index 100 dans un vecteur contenant cinq éléments">

```rust,should_panic,panics
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-05/src/main.rs:here}}
```

</Listing>

Lorsque nous exécutons ce code, la première méthode `[]` provoquera une panique du programme car elle référence un élément inexistant. Cette méthode est mieux utilisée lorsque vous souhaitez que votre programme plante s'il y a une tentative d'accès à un élément au-delà de la fin du vecteur.

Lorsque la méthode `get` reçoit un index qui est en dehors du vecteur, elle renvoie `None` sans provoquer de panique. Vous utiliseriez cette méthode si l'accès à un élément au-delà de la plage du vecteur peut se produire occasionnellement dans des circonstances normales. Votre code aura alors une logique pour gérer soit `Some(&element)`, soit `None`, comme discuté dans le Chapitre 6. Par exemple, l'index pourrait provenir d'une personne entrant un numéro. S'ils saisissent accidentellement un numéro trop grand et que le programme obtient une valeur `None`, vous pourriez dire à l'utilisateur combien d'articles se trouvent dans le vecteur actuel et lui donner une autre chance de saisir une valeur valide. Cela serait plus convivial que de faire planter le programme à cause d'une faute de frappe !

Lorsque le programme a une référence valide, le vérificateur d'emprunt applique les règles de propriété et d'emprunt (couvries dans le Chapitre 4) pour s'assurer que cette référence et toutes les autres références au contenu du vecteur restent valides. Rappelez-vous la règle qui dit que vous ne pouvez pas avoir des références mutables et immuables dans la même portée. Cette règle s'applique dans l'Listing 8-6, où nous tenons une référence immutable au premier élément dans un vecteur et essayons d'ajouter un élément à la fin. Ce programme ne fonctionnera pas si nous essayons également de référencer cet élément plus tard dans la fonction.

<Listing number="8-6" caption="Tentative d'ajout d'un élément à un vecteur tout en tenant une référence à un élément">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-06/src/main.rs:here}}
```

</Listing>

Compiler ce code entraînera cette erreur :

```console
{{#include ../listings/ch08-common-collections/listing-08-06/output.txt}}
```

Le code de l'Listing 8-6 pourrait sembler fonctionner : pourquoi une référence au premier élément devrait-elle se soucier des changements à la fin du vecteur ? Cette erreur est due à la manière dont fonctionnent les vecteurs : parce que les vecteurs placent les valeurs les unes à côté des autres en mémoire, ajouter un nouvel élément à la fin du vecteur pourrait nécessiter d'allouer de la nouvelle mémoire et de copier les anciens éléments dans le nouvel espace, s'il n'y a pas suffisamment de place pour mettre tous les éléments les uns à côté des autres où le vecteur est actuellement stocké. Dans ce cas, la référence au premier élément pointerait vers de la mémoire désallouée. Les règles d'emprunt empêchent les programmes de se retrouver dans cette situation.

> Note : Pour plus de détails sur l'implémentation du type `Vec<T>`, voir [“Le Rustonomicon”][nomicon].

### Itérer sur les valeurs dans un vecteur

Pour accéder successivement à chaque élément d'un vecteur, nous devrions itérer à travers tous les éléments plutôt que d'utiliser des indices pour accéder un par un. L'Listing 8-7 montre comment utiliser une boucle `for` pour obtenir des références immuables à chaque élément dans un vecteur de valeurs `i32` et les imprimer.

<Listing number="8-7" caption="Impression de chaque élément dans un vecteur en itérant sur les éléments avec une boucle `for`">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-07/src/main.rs:here}}
```

</Listing>

Nous pouvons également itérer sur des références mutables à chaque élément dans un vecteur mutable afin d'apporter des modifications à tous les éléments. La boucle `for` dans l'Listing 8-8 ajoutera `50` à chaque élément.

<Listing number="8-8" caption="Itération sur des références mutables aux éléments d'un vecteur">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-08/src/main.rs:here}}
```

</Listing>

Pour changer la valeur à laquelle la référence mutable fait référence, nous devons utiliser l'opérateur de déréférencement `*` pour accéder à la valeur dans `i` avant de pouvoir utiliser l'opérateur `+=`. Nous parlerons davantage de l'opérateur de déréférencement dans la section [“Suivre la référence jusqu'à la valeur”][deref]<!-- ignore --> du Chapitre 15.

Itérer sur un vecteur, que ce soit de manière immuable ou mutable, est sûr grâce aux règles du vérificateur d'emprunt. Si nous essayions d'insérer ou de retirer des éléments dans les corps des boucles `for` dans l'Listing 8-7 et l'Listing 8-8, nous obtiendrions une erreur de compilation similaire à celle que nous avons obtenue avec le code de l'Listing 8-6. La référence au vecteur que la boucle `for` détient empêche la modification simultanée de l'ensemble du vecteur.

### Utiliser un Enum pour stocker plusieurs types

Les vecteurs ne peuvent stocker que des valeurs du même type. Cela peut être inconfortable ; il existe définitivement des cas d'utilisation nécessitant de stocker une liste d'éléments de différents types. Heureusement, les variantes d'un enum sont définies sous le même type d'enum, donc lorsque nous avons besoin d'un type pour représenter des éléments de différents types, nous pouvons définir et utiliser un enum !

Par exemple, disons que nous voulons obtenir des valeurs d'une ligne dans une feuille de calcul où certaines colonnes de la ligne contiennent des entiers, certains nombres à virgule flottante et certaines chaînes. Nous pouvons définir un enum dont les variantes contiendront les différents types de valeur, et toutes les variantes de l'enum seront considérées comme le même type : celui de l'enum. Ensuite, nous pouvons créer un vecteur pour contenir cet enum et ainsi, finalement, contenir différents types. Nous avons démontré cela dans l'Listing 8-9.

<Listing number="8-9" caption="Définir un enum pour stocker des valeurs de différents types dans un vecteur">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-09/src/main.rs:here}}
```

</Listing>

Rust doit savoir quels types seront dans le vecteur à la compilation afin de déterminer exactement combien de mémoire sur le tas sera nécessaire pour stocker chaque élément. Nous devons également être explicites sur les types autorisés dans ce vecteur. Si Rust permettait à un vecteur de contenir n'importe quel type, il y aurait un risque que l'un ou plusieurs des types provoquent des erreurs avec les opérations effectuées sur les éléments du vecteur. Utiliser un enum plus une expression `match` signifie que Rust s'assurera à la compilation que chaque cas possible est géré, comme discuté dans le Chapitre 6.

Si vous ne connaissez pas l'ensemble exhaustif des types qu'un programme recevra à l'exécution pour stocker dans un vecteur, la technique de l'enum ne fonctionnera pas. À la place, vous pouvez utiliser un objet de trait, que nous traiterons dans le Chapitre 18.

Maintenant que nous avons discuté de certaines des méthodes les plus courantes d'utilisation des vecteurs, assurez-vous de consulter [la documentation de l'API][vec-api]<!-- ignore --> pour toutes les nombreuses méthodes utiles définies sur `Vec<T>` par la bibliothèque standard. Par exemple, en plus de `push`, une méthode `pop` supprime et renvoie le dernier élément.

### Supprimer un vecteur supprime ses éléments

Comme tout autre `struct`, un vecteur est libéré lorsqu'il sort de la portée, comme annoté dans l'Listing 8-10.

<Listing number="8-10" caption="Montrer où le vecteur et ses éléments sont supprimés">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-10/src/main.rs:here}}
```

</Listing>

Lorsque le vecteur est supprimé, tout son contenu est également supprimé, ce qui signifie que les entiers qu'il contient seront nettoyés. Le vérificateur d'emprunt s'assure que toutes les références aux contenus d'un vecteur ne sont utilisées que pendant que le vecteur lui-même est valide.

Passons au prochain type de collection : `String` !

[data-types]: ch03-02-data-types.html#data-types
[nomicon]: ../nomicon/vec/vec.html
[vec-api]: ../std/vec/struct.Vec.html
[deref]: ch15-02-deref.html#following-the-pointer-to-the-value-with-the-dereference-operator