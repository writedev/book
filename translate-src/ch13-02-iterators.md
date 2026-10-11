## Traiter une série d’éléments avec des itérateurs

Le motif de l’itérateur vous permet d’effectuer une tâche sur une séquence d’éléments, l’un après l’autre. Un itérateur est responsable de la logique qui consiste à parcourir chaque élément et à déterminer quand la séquence est terminée. Lorsque vous utilisez des itérateurs, vous n’avez pas à réimplémenter cette logique vous-même.

En Rust, les itérateurs sont _paresseux_, ce qui signifie qu’ils n’ont aucun effet tant que vous n’appelez pas de méthodes qui consomment l’itérateur. Par exemple, le code de la liste 13-10 crée un itérateur sur les éléments du vecteur `v1` en appelant la méthode `iter` définie sur `Vec<T>`. Ce code, à lui seul, ne fait rien d’utile.

<Listing number="13-10" file-name="src/main.rs" caption="Créer un itérateur">

```rust
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-10/src/main.rs:here}}
```

</Listing>

L’itérateur est stocké dans la variable `v1_iter`. Une fois l’itérateur créé, nous pouvons l’utiliser de différentes façons. Dans la liste 3-5, nous avons parcouru un tableau à l’aide d’une boucle `for` pour exécuter du code sur chacun de ses éléments. En interne, cela a implicitement créé puis consommé un itérateur, mais nous n’avons pas expliqué précisément comment cela fonctionnait jusqu’à présent.

Dans l’exemple de la liste 13-11, nous séparons la création de l’itérateur de son utilisation dans la boucle `for`. Lorsque la boucle `for` est appelée avec l’itérateur de `v1_iter`, chaque élément de l’itérateur est utilisé lors d’une itération de la boucle, qui affiche alors chaque valeur.

<Listing number="13-11" file-name="src/main.rs" caption="Utiliser un itérateur dans une boucle `for`">

```rust
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-11/src/main.rs:here}}
```

</Listing>

Dans les langages dont les bibliothèques standard ne fournissent pas d’itérateurs, vous écririez probablement cette même fonctionnalité en initialisant une variable à l’indice 0, en utilisant cette variable pour accéder à une valeur du vecteur, puis en l’incrémentant dans une boucle jusqu’à ce qu’elle atteigne le nombre total d’éléments du vecteur.

Les itérateurs prennent en charge toute cette logique pour vous, ce qui réduit le code répétitif susceptible de contenir des erreurs. Ils vous offrent davantage de souplesse pour appliquer la même logique à de nombreux types de séquences, et pas seulement aux structures de données auxquelles vous pouvez accéder par indice, comme les vecteurs. Voyons comment les itérateurs s’y prennent.

### Le trait `Iterator` et la méthode `next`

Tous les itérateurs implémentent un trait nommé `Iterator`, défini dans la bibliothèque standard. La définition de ce trait ressemble à ceci :

```rust
pub trait Iterator {
    type Item;

    fn next(&mut self) -> Option<Self::Item>;

    // methods with default implementations elided
}
```

Remarquez que cette définition utilise une nouvelle syntaxe : `type Item` et `Self::Item`, qui définissent un type associé à ce trait. Nous parlerons des types associés en détail au chapitre 20. Pour l’instant, il vous suffit de savoir que ce code indique que l’implémentation du trait `Iterator` exige également la définition d’un type `Item`, lequel est utilisé dans le type de retour de la méthode `next`. Autrement dit, le type `Item` est le type renvoyé par l’itérateur.

Le trait `Iterator` exige uniquement des types qui l’implémentent qu’ils définissent une méthode : `next`. Celle-ci renvoie un élément de l’itérateur à la fois, enveloppé dans `Some`, puis renvoie `None` lorsque l’itération est terminée.

Nous pouvons appeler directement la méthode `next` sur les itérateurs ; la liste 13-12 montre les valeurs renvoyées par plusieurs appels successifs à `next` sur l’itérateur créé à partir du vecteur.

<Listing number="13-12" file-name="src/lib.rs" caption="Appeler la méthode `next` sur un itérateur">

```rust,noplayground
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-12/src/lib.rs:here}}
```

</Listing>

Notez que nous avons dû rendre `v1_iter` mutable : appeler la méthode `next` sur un itérateur modifie son état interne, qui lui permet de garder une trace de sa position dans la séquence. Autrement dit, ce code _consomme_ l’itérateur, c’est-à-dire qu’il l’épuise. Chaque appel à `next` retire un élément de l’itérateur. Nous n’avons pas eu besoin de rendre `v1_iter` mutable avec une boucle `for`, car la boucle a pris possession de `v1_iter` et l’a rendu mutable en coulisses.

Notez également que les valeurs renvoyées par les appels à `next` sont des références immuables aux valeurs du vecteur. La méthode `iter` produit un itérateur sur des références immuables. Si nous voulons créer un itérateur qui prend possession de `v1` et renvoie des valeurs possédées, nous pouvons appeler `into_iter` au lieu de `iter`. De même, si nous voulons parcourir des références mutables, nous pouvons appeler `iter_mut` au lieu de `iter`.

### Méthodes qui consomment l’itérateur

Le trait `Iterator` propose un certain nombre de méthodes différentes, dont les implémentations par défaut sont fournies par la bibliothèque standard. Vous pouvez découvrir ces méthodes dans la documentation de l’API de la bibliothèque standard consacrée au trait `Iterator`. Certaines de ces méthodes font appel à la méthode `next` dans leur définition, ce qui explique pourquoi vous devez implémenter la méthode `next` lorsque vous implémentez le trait `Iterator`.

Les méthodes qui appellent `next` sont appelées _adaptateurs consommateurs_, car leur appel épuise l’itérateur. La méthode `sum`, par exemple, prend possession de l’itérateur et parcourt ses éléments en appelant `next` à plusieurs reprises, ce qui consomme l’itérateur. Au fil du parcours, elle ajoute chaque élément à un total cumulé et renvoie ce total une fois l’itération terminée. La liste 13-13 contient un test qui illustre l’utilisation de la méthode `sum`.

<Listing number="13-13" file-name="src/lib.rs" caption="Appeler la méthode `sum` pour obtenir le total de tous les éléments de l’itérateur">

```rust,noplayground
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-13/src/lib.rs:here}}
```

</Listing>

Nous ne pouvons pas utiliser `v1_iter` après l’appel à `sum`, car `sum` prend possession de l’itérateur sur lequel nous l’appelons.

### Méthodes qui produisent d’autres itérateurs

Les _adaptateurs d’itérateurs_ sont des méthodes définies sur le trait `Iterator` qui ne consomment pas l’itérateur. À la place, elles produisent de nouveaux itérateurs en modifiant un aspect de l’itérateur d’origine.

La liste 13-14 montre un exemple d’appel à la méthode d’adaptation d’itérateur `map`, qui prend une fermeture à appeler sur chaque élément au cours du parcours. La méthode `map` renvoie un nouvel itérateur qui produit les éléments modifiés. Ici, la fermeture crée un nouvel itérateur dans lequel chaque élément du vecteur est incrémenté de 1.

<Listing number="13-14" file-name="src/main.rs" caption="Appeler l’adaptateur d’itérateur `map` pour créer un nouvel itérateur">

```rust,not_desired_behavior
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-14/src/main.rs:here}}
```

</Listing>

Cependant, ce code produit un avertissement :

```console
{{#include ../listings/ch13-functional-features/listing-13-14/output.txt}}
```

Le code de la liste 13-14 ne fait rien ; la fermeture que nous avons spécifiée n’est jamais appelée. L’avertissement nous rappelle pourquoi : les adaptateurs d’itérateurs sont paresseux, et nous devons ici consommer l’itérateur.

Pour corriger cet avertissement et consommer l’itérateur, nous allons utiliser la méthode `collect`, que nous avons utilisée avec `env::args` dans la liste 12-1. Cette méthode consomme l’itérateur et rassemble les valeurs obtenues dans une structure de données de type collection.

Dans la liste 13-15, nous rassemblons dans un vecteur les résultats du parcours de l’itérateur renvoyé par l’appel à `map`. Ce vecteur contiendra chaque élément du vecteur d’origine, incrémenté de 1.

<Listing number="13-15" file-name="src/main.rs" caption="Appeler la méthode `map` pour créer un nouvel itérateur, puis la méthode `collect` pour le consommer et créer un vecteur">

```rust
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-15/src/main.rs:here}}
```

</Listing>

Comme `map` prend une fermeture, nous pouvons spécifier n’importe quelle opération à effectuer sur chaque élément. C’est un excellent exemple de la façon dont les fermetures vous permettent de personnaliser un comportement tout en réutilisant la logique de parcours fournie par le trait `Iterator`.

Vous pouvez chaîner plusieurs appels à des adaptateurs d’itérateurs pour effectuer des opérations complexes de manière lisible. Mais comme tous les itérateurs sont paresseux, vous devez appeler l’une des méthodes d’adaptation consommatrices pour obtenir des résultats des appels aux adaptateurs d’itérateurs.

<!-- Anciens titres. Ne pas supprimer, car les liens pourraient ne plus fonctionner. -->

<a id="using-closures-that-capture-their-environment"></a>

### Fermetures qui capturent leur environnement

De nombreux adaptateurs d’itérateurs prennent des fermetures comme arguments, et les fermetures que nous spécifierons couramment comme arguments de ces adaptateurs seront des fermetures qui capturent leur environnement.

Pour cet exemple, nous utiliserons la méthode `filter`, qui prend une fermeture. La fermeture reçoit un élément de l’itérateur et renvoie un `bool`. Si elle renvoie `true`, la valeur sera incluse dans l’itérateur produit par `filter`. Si elle renvoie `false`, la valeur ne sera pas incluse.

Dans la liste 13-16, nous utilisons `filter` avec une fermeture qui capture la variable `shoe_size` de son environnement pour parcourir une collection d’instances de la structure `Shoe`. Elle ne renverra que les chaussures de la pointure spécifiée.

<Listing number="13-16" file-name="src/lib.rs" caption="Utiliser la méthode `filter` avec une fermeture qui capture `shoe_size`">

```rust,noplayground
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-16/src/lib.rs}}
```

</Listing>

La fonction `shoes_in_size` prend comme paramètres un vecteur de chaussures et une pointure, et en prend possession. Elle renvoie un vecteur contenant uniquement les chaussures de la pointure spécifiée.

Dans le corps de `shoes_in_size`, nous appelons `into_iter` pour créer un itérateur qui prend possession du vecteur. Ensuite, nous appelons `filter` pour transformer cet itérateur en un nouvel itérateur qui ne contient que les éléments pour lesquels la fermeture renvoie `true`.

La fermeture capture le paramètre `shoe_size` de son environnement et compare sa valeur à la pointure de chaque chaussure, en ne conservant que celles de la pointure spécifiée. Enfin, l’appel à `collect` rassemble les valeurs renvoyées par l’itérateur adapté dans un vecteur, que la fonction renvoie.

Le test montre que lorsque nous appelons `shoes_in_size`, nous obtenons uniquement les chaussures qui ont la même pointure que celle que nous avons spécifiée.