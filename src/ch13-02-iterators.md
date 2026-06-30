## Traitement d'une série d'éléments avec des itérateurs

Le modèle d'itérateur vous permet d'exécuter une tâche sur une séquence d'éléments à tour de rôle. Un itérateur est responsable de la logique d'itération sur chaque élément et de la détermination de quand la séquence est terminée. Lorsque vous utilisez des itérateurs, vous n'avez pas à réimplémenter cette logique vous-même.

En Rust, les itérateurs sont _paresseux_, ce qui signifie qu'ils n'ont aucun effet tant que vous n'appelez pas des méthodes qui consomment l'itérateur pour l'utiliser. Par exemple, le code dans la Liste 13-10 crée un itérateur sur les éléments du vecteur `v1` en appelant la méthode `iter` définie sur `Vec<T>`. Ce code, en lui-même, ne fait rien d'utile.

<Listing number="13-10" file-name="src/main.rs" caption="Création d'un itérateur">

```rust
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-10/src/main.rs:here}}
```

</Listing>

L'itérateur est stocké dans la variable `v1_iter`. Une fois que nous avons créé un itérateur, nous pouvons l'utiliser de différentes manières. Dans la Liste 3-5, nous avons itéré sur un tableau en utilisant une boucle `for` pour exécuter du code sur chacun de ses éléments. Sous le capot, cela a implicitement créé puis consommé un itérateur, mais nous avons négligé de voir comment cela fonctionne jusqu'à présent.

Dans l'exemple de la Liste 13-11, nous séparons la création de l'itérateur de l'utilisation de l'itérateur dans la boucle `for`. Lorsque la boucle `for` est appelée en utilisant l'itérateur dans `v1_iter`, chaque élément de l'itérateur est utilisé lors d'une itération de la boucle, ce qui imprime chaque valeur.

<Listing number="13-11" file-name="src/main.rs" caption="Utilisation d'un itérateur dans une boucle `for`">

```rust
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-11/src/main.rs:here}}
```

</Listing>

Dans des langages qui n'ont pas d'itérateurs fournis par leurs bibliothèques standard, vous écririez probablement cette même fonctionnalité en commençant une variable à l'index 0, en utilisant cette variable pour indexer dans le vecteur afin d'obtenir une valeur, et en incrémentant la valeur de la variable dans une boucle jusqu'à atteindre le nombre total d'éléments dans le vecteur.

Les itérateurs gèrent toute cette logique pour vous, réduisant le code répétitif que vous pourriez potentiellement mal gérer. Les itérateurs vous donnent plus de flexibilité pour utiliser la même logique avec de nombreux types de séquences, pas seulement des structures de données que vous pouvez indexer, comme des vecteurs. Examinons comment les itérateurs font cela.

### Le Trait `Iterator` et la Méthode `next`

Tous les itérateurs implémentent un trait nommé `Iterator` qui est défini dans la bibliothèque standard. La définition du trait ressemble à ceci :

```rust
pub trait Iterator {
    type Item;

    fn next(&mut self) -> Option<Self::Item>;

    // méthodes avec implémentations par défaut élidées
}
```

Remarquez que cette définition utilise une nouvelle syntaxe : `type Item` et `Self::Item`, qui définissent un type associé avec ce trait. Nous parlerons des types associés en profondeur au Chapitre 20. Pour l'instant, tout ce que vous devez savoir est que ce code indique que l'implémentation du trait `Iterator` nécessite que vous définissiez également un type `Item`, et ce type `Item` est utilisé dans le type de retour de la méthode `next`. En d'autres termes, le type `Item` sera le type retourné par l'itérateur.

Le trait `Iterator` ne requiert que les implémenteurs définissent une méthode : la méthode `next`, qui retourne un élément de l'itérateur à la fois, encapsulé dans `Some`, et, lorsque l'itération est terminée, retourne `None`.

Nous pouvons appeler la méthode `next` sur des itérateurs directement ; la Liste 13-12 illustre les valeurs retournées par des appels répétés à `next` sur l'itérateur créé à partir du vecteur.

<Listing number="13-12" file-name="src/lib.rs" caption="Appel de la méthode `next` sur un itérateur">

```rust,noplayground
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-12/src/lib.rs:here}}
```

</Listing>

Notez que nous avons dû rendre `v1_iter` mutable : appeler la méthode `next` sur un itérateur modifie l'état interne que l'itérateur utilise pour suivre sa position dans la séquence. En d'autres termes, ce code _consomme_, ou utilise, l'itérateur. Chaque appel à `next` consomme un élément de l'itérateur. Nous n'avons pas eu besoin de rendre `v1_iter` mutable lorsque nous avons utilisé une boucle `for`, car la boucle a pris possession de `v1_iter` et l'a rendue mutable en arrière-plan.

Notez également que les valeurs que nous obtenons des appels à `next` sont des références immuables aux valeurs dans le vecteur. La méthode `iter` produit un itérateur sur des références immuables. Si nous voulons créer un itérateur qui prend possession de `v1` et retourne des valeurs possédées, nous pouvons appeler `into_iter` au lieu de `iter`. De même, si nous voulons itérer sur des références mutables, nous pouvons appeler `iter_mut` au lieu de `iter`.

### Méthodes Qui Consomment l'Itérateur

Le trait `Iterator` a un certain nombre de méthodes différentes avec des implémentations par défaut fournies par la bibliothèque standard ; vous pouvez en savoir plus sur ces méthodes en consultant la documentation de l'API de la bibliothèque standard pour le trait `Iterator`. Certaines de ces méthodes appellent la méthode `next` dans leur définition, ce qui est la raison pour laquelle vous êtes tenu d'implémenter la méthode `next` lorsque vous implémentez le trait `Iterator`.

Les méthodes qui appellent `next` sont appelées _adaptateurs consommateurs_ parce qu'appeler ces méthodes utilise l'itérateur. Un exemple est la méthode `sum`, qui prend possession de l'itérateur et parcourt les éléments en appelant répétitivement `next`, consommant ainsi l'itérateur. Au fur et à mesure qu'il parcourt, il ajoute chaque élément à un total courant et retourne le total lorsque l'itération est complète. La Liste 13-13 a un test illustrant une utilisation de la méthode `sum`.

<Listing number="13-13" file-name="src/lib.rs" caption="Appel de la méthode `sum` pour obtenir le total de tous les éléments de l'itérateur">

```rust,noplayground
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-13/src/lib.rs:here}}
```

</Listing>

Nous ne pouvons pas utiliser `v1_iter` après l'appel à `sum`, car `sum` prend possession de l'itérateur sur lequel nous l'appelons.

### Méthodes Qui Produisent D'autres Itérateurs

Les _adaptateurs d'itérateur_ sont des méthodes définies sur le trait `Iterator` qui ne consomment pas l'itérateur. Au lieu de cela, elles produisent différents itérateurs en modifiant certains aspects de l'itérateur original.

La Liste 13-14 montre un exemple d'appel de la méthode d'adaptateur d'itérateur `map`, qui prend une fermeture à appeler sur chaque élément pendant que les éléments sont itérés. La méthode `map` retourne un nouvel itérateur qui produit les éléments modifiés. La fermeture ici crée un nouvel itérateur dans lequel chaque élément du vecteur sera incrémenté de 1.

<Listing number="13-14" file-name="src/main.rs" caption="Appel de la méthode d'adaptateur `map` pour créer un nouvel itérateur">

```rust,not_desired_behavior
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-14/src/main.rs:here}}
```

</Listing>

Cependant, ce code produit un avertissement :

```console
{{#include ../listings/ch13-functional-features/listing-13-14/output.txt}}
```

Le code de la Liste 13-14 ne fait rien ; la fermeture que nous avons spécifiée n'est jamais appelée. L'avertissement nous rappelle pourquoi : les adaptateurs d'itérateur sont paresseux, et nous devons consommer l'itérateur ici.

Pour corriger cet avertissement et consommer l'itérateur, nous utiliserons la méthode `collect`, que nous avons utilisée avec `env::args` dans la Liste 12-1. Cette méthode consomme l'itérateur et collecte les valeurs résultantes dans un type de données de collection.

Dans la Liste 13-15, nous collectons les résultats de l'itération sur l'itérateur retourné par l'appel à `map` dans un vecteur. Ce vecteur finira par contenir chaque élément du vecteur original, incrémenté de 1.

<Listing number="13-15" file-name="src/main.rs" caption="Appel de la méthode `map` pour créer un nouvel itérateur, puis appel de la méthode `collect` pour consommer le nouvel itérateur et créer un vecteur">

```rust
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-15/src/main.rs:here}}
```

</Listing>

Parce que `map` prend une fermeture, nous pouvons spécifier n'importe quelle opération que nous voulons effectuer sur chaque élément. C'est un excellent exemple de la façon dont les fermetures vous permettent de personnaliser un certain comportement tout en réutilisant le comportement d'itération que le trait `Iterator` fournit.

Vous pouvez enchaîner plusieurs appels aux adaptateurs d'itérateurs pour réaliser des actions complexes de manière lisible. Mais comme tous les itérateurs sont paresseux, vous devez appeler l'une des méthodes d'adaptateur consommateurs pour obtenir des résultats des appels aux adaptateurs d'itérateurs.

### Fermetures Qui Capturent Leur Environnement

De nombreux adaptateurs d'itérateurs prennent des fermetures en arguments, et couramment les fermetures que nous spécifierons comme arguments aux adaptateurs d'itérateurs seront des fermetures qui capturent leur environnement.

Pour cet exemple, nous utiliserons la méthode `filter` qui prend une fermeture. La fermeture reçoit un élément de l'itérateur et retourne un `bool`. Si la fermeture retourne `true`, la valeur sera incluse dans l'itération produite par `filter`. Si la fermeture retourne `false`, la valeur ne sera pas incluse.

Dans la Liste 13-16, nous utilisons `filter` avec une fermeture qui capture la variable `shoe_size` de son environnement pour itérer sur une collection d'instances de la structure `Shoe`. Elle ne retournera que les chaussures de la taille spécifiée.

<Listing number="13-16" file-name="src/lib.rs" caption="Utilisation de la méthode `filter` avec une fermeture qui capture `shoe_size`">

```rust,noplayground
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-16/src/lib.rs}}
```

</Listing>

La fonction `shoes_in_size` prend possession d'un vecteur de chaussures et d'une taille de chaussure comme paramètres. Elle retourne un vecteur contenant uniquement des chaussures de la taille spécifiée.

Dans le corps de `shoes_in_size`, nous appelons `into_iter` pour créer un itérateur qui prend possession du vecteur. Ensuite, nous appelons `filter` pour adapter cet itérateur en un nouvel itérateur qui ne contient que les éléments pour lesquels la fermeture retourne `true`.

La fermeture capture le paramètre `shoe_size` de l'environnement et compare la valeur avec la taille de chaque chaussure, ne gardant que les chaussures de la taille spécifiée. Enfin, l'appel à `collect` rassemble les valeurs retournées par l'itérateur adapté dans un vecteur qui est retourné par la fonction.

Le test montre que lorsque nous appelons `shoes_in_size`, nous ne récupérons que des chaussures ayant la même taille que la valeur que nous avons spécifiée.