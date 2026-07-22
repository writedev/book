# Types génériques, traits et durées de vie

Chaque langage de programmation dispose d'outils pour gérer efficacement la duplication des concepts. En Rust, l'un de ces outils est _les générics_ : des substituts abstraits pour des types concrets ou d'autres propriétés. Nous pouvons exprimer le comportement des générics ou comment ils se rapportent à d'autres générics sans savoir ce qui sera à leur place lors de la compilation et de l'exécution du code.

Les fonctions peuvent accepter des paramètres d'un certain type générique, au lieu d'un type concret tel que `i32` ou `String`, de la même manière qu'elles acceptent des paramètres avec des valeurs inconnues pour exécuter le même code sur plusieurs valeurs concrètes. En réalité, nous avons déjà utilisé des générics dans le Chapitre 6 avec `Option<T>`, dans le Chapitre 8 avec `Vec<T>` et `HashMap<K, V>`, et dans le Chapitre 9 avec `Result<T, E>`. Dans ce chapitre, vous explorerez comment définir vos propres types, fonctions et méthodes avec des générics !

Tout d'abord, nous allons revoir comment extraire une fonction pour réduire la duplication de code. Nous utiliserons ensuite la même technique pour créer une fonction générique à partir de deux fonctions qui ne diffèrent que par les types de leurs paramètres. Nous expliquerons également comment utiliser des types génériques dans les définitions de structures et d'énumérations.

Ensuite, vous découvrirez comment utiliser des traits pour définir un comportement de manière générique. Vous pouvez combiner des traits avec des types génériques pour contraindre un type générique à n'accepter que les types ayant un comportement particulier, plutôt que n'importe quel type.

Enfin, nous aborderons les _durées de vie_ : une variété de générics qui donnent au compilateur des informations sur la manière dont les références se rapportent les unes aux autres. Les durées de vie nous permettent de fournir au compilateur suffisamment d'informations sur les valeurs empruntées pour garantir que les références seront valides dans plus de situations qu'il ne pourrait le faire sans notre aide.

## Suppression de la duplication en extrayant une fonction

Les générics nous permettent de remplacer des types spécifiques par un espace réservé représentant plusieurs types pour éliminer la duplication de code. Avant de plonger dans la syntaxe des générics, examinons d'abord comment éliminer la duplication d'une manière qui n'implique pas de types génériques en extrayant une fonction qui remplace des valeurs spécifiques par un espace réservé représentant plusieurs valeurs. Ensuite, nous appliquerons la même technique pour extraire une fonction générique ! En apprenant à reconnaître le code dupliqué que vous pouvez extraire dans une fonction, vous commencerez à identifier le code dupliqué qui peut utiliser des générics.

Nous commencerons avec le court programme dans la Liste 10-1 qui trouve le plus grand nombre dans une liste.

<Listing number="10-1" file-name="src/main.rs" caption="Trouver le plus grand nombre dans une liste de nombres">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-01/src/main.rs:here}}
```

</Listing>

Nous stockons une liste d'entiers dans la variable `number_list` et plaçons une référence au premier nombre de la liste dans une variable nommée `largest`. Nous itérons ensuite à travers tous les nombres de la liste et, si le numéro actuel est supérieur au nombre stocké dans `largest`, nous remplaçons la référence dans cette variable. Cependant, si le numéro actuel est inférieur ou égal au plus grand nombre vu jusqu'à présent, la variable ne change pas et le code passe au numéro suivant de la liste. Après avoir examiné tous les nombres de la liste, `largest` devrait faire référence au plus grand nombre, qui dans ce cas est 100.

Nous avons maintenant la tâche de trouver le plus grand nombre dans deux listes différentes de nombres. Pour ce faire, nous pouvons choisir de dupliquer le code de la Liste 10-1 et d'utiliser la même logique à deux endroits différents du programme, comme le montre la Liste 10-2.

<Listing number="10-2" file-name="src/main.rs" caption="Code pour trouver le plus grand nombre dans *deux* listes de nombres">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-02/src/main.rs}}
```

</Listing>

Bien que ce code fonctionne, la duplication de code est fastidieuse et sujette aux erreurs. Nous devons également nous rappeler de mettre à jour le code à plusieurs endroits lorsque nous souhaitons le modifier.

Pour éliminer cette duplication, nous allons créer une abstraction en définissant une fonction qui opère sur n'importe quelle liste d'entiers passée en paramètre. Cette solution rend notre code plus clair et nous permet d'exprimer le concept de recherche du plus grand nombre dans une liste de manière abstraite.

Dans la Liste 10-3, nous extrayons le code qui trouve le plus grand nombre dans une fonction nommée `largest`. Ensuite, nous appelons la fonction pour trouver le plus grand nombre dans les deux listes de la Liste 10-2. Nous pourrions également utiliser la fonction sur n'importe quelle autre liste de valeurs `i32` que nous pourrions avoir à l'avenir.

<Listing number="10-3" file-name="src/main.rs" caption="Code abstrait pour trouver le plus grand nombre dans deux listes">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-03/src/main.rs:here}}
```

</Listing>

La fonction `largest` a un paramètre appelé `list`, qui représente n'importe quel tranche concrète de valeurs `i32` que nous pourrions passer à la fonction. En conséquence, lorsque nous appelons la fonction, le code s'exécute sur les valeurs spécifiques que nous passons.

En résumé, voici les étapes que nous avons suivies pour modifier le code de la Liste 10-2 à la Liste 10-3 :

1. Identifier le code dupliqué.
2. Extraire le code dupliqué dans le corps de la fonction, et spécifier les entrées et les valeurs de retour de ce code dans la signature de la fonction.
3. Mettre à jour les deux instances de code dupliqué pour appeler la fonction à la place.

Ensuite, nous utiliserons ces mêmes étapes avec des générics pour réduire la duplication de code. De la même manière que le corps de la fonction peut fonctionner sur un `list` abstrait au lieu de valeurs spécifiques, les générics permettent au code de fonctionner sur des types abstraits.

Par exemple, disons que nous avions deux fonctions : l'une qui trouve le plus grand élément dans une tranche de valeurs `i32` et l'autre qui trouve le plus grand élément dans une tranche de valeurs `char`. Comment pourrions-nous éliminer cette duplication ? Découvrons-le !