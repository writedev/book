# Types génériques, traits et durées de vie

Chaque langage de programmation dispose d’outils permettant de gérer efficacement la duplication de concepts. En Rust, l’un de ces outils est celui des _génériques_ : des substituts abstraits pour des types concrets ou d’autres propriétés. Nous pouvons exprimer le comportement des génériques ou la façon dont ils sont liés à d’autres génériques sans savoir ce qui les remplacera lors de la compilation et de l’exécution du code.

Les fonctions peuvent prendre des paramètres d’un type générique plutôt que d’un type concret comme `i32` ou `String`, de la même façon qu’elles prennent des paramètres dont les valeurs sont inconnues, afin d’exécuter le même code sur plusieurs valeurs concrètes. En fait, nous avons déjà utilisé des génériques au chapitre 6 avec `Option<T>`, au chapitre 8 avec `Vec<T>` et `HashMap<K, V>`, et au chapitre 9 avec `Result<T, E>`. Dans ce chapitre, vous allez découvrir comment définir vos propres types, fonctions et méthodes à l’aide de génériques !

Nous allons d’abord revoir comment extraire une fonction pour réduire la duplication de code. Nous utiliserons ensuite la même technique pour créer une fonction générique à partir de deux fonctions qui ne diffèrent que par les types de leurs paramètres. Nous expliquerons également comment utiliser des types génériques dans les définitions de structures et d’énumérations.

Ensuite, vous apprendrez à utiliser les traits pour définir un comportement de manière générique. Vous pouvez combiner des traits avec des types génériques afin de contraindre un type générique à n’accepter que les types qui possèdent un comportement particulier, plutôt que n’importe quel type.

Enfin, nous aborderons les _durées de vie_ : une forme de génériques qui fournit au compilateur des informations sur les relations entre les références. Les durées de vie nous permettent de donner au compilateur suffisamment d’informations sur les valeurs empruntées pour qu’il puisse garantir la validité des références dans davantage de situations qu’il ne le pourrait sans notre aide.

## Éliminer la duplication en extrayant une fonction

Les génériques nous permettent de remplacer des types spécifiques par un espace réservé représentant plusieurs types afin d’éliminer la duplication de code. Avant d’aborder la syntaxe des génériques, examinons d’abord comment éliminer la duplication sans utiliser de types génériques, en extrayant une fonction qui remplace des valeurs spécifiques par un espace réservé représentant plusieurs valeurs. Nous appliquerons ensuite la même technique pour extraire une fonction générique ! En examinant comment repérer du code dupliqué pouvant être extrait dans une fonction, vous commencerez à reconnaître le code dupliqué qui peut tirer parti des génériques.

Commençons par le court programme de la liste 10-1, qui trouve le plus grand nombre d’une liste.

<Listing number="10-1" file-name="src/main.rs" caption="Recherche du plus grand nombre dans une liste de nombres">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-01/src/main.rs:here}}
```

</Listing>

Nous stockons une liste d’entiers dans la variable `number_list` et plaçons une référence au premier nombre de la liste dans une variable nommée `largest`. Nous parcourons ensuite tous les nombres de la liste et, si le nombre courant est supérieur à celui stocké dans `largest`, nous remplaçons la référence dans cette variable. En revanche, si le nombre courant est inférieur ou égal au plus grand nombre rencontré jusque-là, la variable ne change pas et le code passe au nombre suivant de la liste. Après avoir examiné tous les nombres de la liste, `largest` devrait faire référence au plus grand nombre, qui est ici 100.

Nous devons maintenant trouver le plus grand nombre dans deux listes différentes. Pour ce faire, nous pouvons choisir de dupliquer le code de la liste 10-1 et d’utiliser la même logique à deux endroits différents du programme, comme le montre la liste 10-2.

<Listing number="10-2" file-name="src/main.rs" caption="Code permettant de trouver le plus grand nombre dans *deux* listes de nombres">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-02/src/main.rs}}
```

</Listing>

Bien que ce code fonctionne, dupliquer du code est fastidieux et source d’erreurs. Nous devons également penser à mettre à jour le code à plusieurs endroits lorsque nous voulons le modifier.

Pour éliminer cette duplication, nous allons créer une abstraction en définissant une fonction qui s’applique à toute liste d’entiers qui lui est transmise en paramètre. Cette solution rend notre code plus clair et nous permet d’exprimer de manière abstraite le concept de recherche du plus grand nombre dans une liste.

Dans la liste 10-3, nous extrayons le code qui trouve le plus grand nombre dans une fonction nommée `largest`. Nous appelons ensuite cette fonction pour trouver le plus grand nombre dans les deux listes de la liste 10-2. Nous pourrions également utiliser cette fonction sur toute autre liste de valeurs `i32` que nous aurions à l’avenir.

<Listing number="10-3" file-name="src/main.rs" caption="Code abstrait permettant de trouver le plus grand nombre dans deux listes">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-03/src/main.rs:here}}
```

</Listing>

La fonction `largest` possède un paramètre nommé `list`, qui représente n’importe quelle tranche concrète de valeurs `i32` que nous pourrions transmettre à la fonction. Par conséquent, lorsque nous appelons la fonction, le code s’exécute sur les valeurs spécifiques que nous lui transmettons.

En résumé, voici les étapes que nous avons suivies pour modifier le code de la liste 10-2 afin d’obtenir celui de la liste 10-3 :

1. Repérer le code dupliqué.
1. Extraire le code dupliqué dans le corps de la fonction et préciser les entrées et les valeurs de retour de ce code dans la signature de la fonction.
1. Modifier les deux occurrences du code dupliqué pour qu’elles appellent la fonction à la place.

Ensuite, nous allons suivre les mêmes étapes avec les génériques afin de réduire la duplication de code. De la même façon que le corps de la fonction peut fonctionner sur une `list` abstraite plutôt que sur des valeurs spécifiques, les génériques permettent au code de fonctionner sur des types abstraits.

Par exemple, imaginons deux fonctions : l’une qui trouve l’élément le plus grand d’une tranche de valeurs `i32`, et l’autre qui trouve l’élément le plus grand d’une tranche de valeurs `char`. Comment éliminer cette duplication ? Découvrons-le !