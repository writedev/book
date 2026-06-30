## Utilisation de `Box<T>` pour Pointer vers des Données sur le Tas

Le pointeur intelligent le plus simple est une boîte, dont le type est écrit `Box<T>`. Les _boîtes_ permettent de stocker des données sur le tas plutôt que sur la pile. Ce qui reste sur la pile est le pointeur vers les données du tas. Consultez le Chapitre 4 pour revoir la différence entre la pile et le tas.

Les boîtes n'ont pas de surcharge de performance, à part le fait de stocker leurs données sur le tas au lieu de la pile. Mais elles n'ont pas non plus beaucoup de capacités supplémentaires. Vous les utiliserez le plus souvent dans ces situations :

- Lorsque vous avez un type dont la taille ne peut pas être connue à la compilation, et que vous souhaitez utiliser une valeur de ce type dans un contexte qui nécessite une taille exacte
- Lorsque vous avez une grande quantité de données, et que vous souhaitez transférer la propriété tout en vous assurant que les données ne seront pas copiées lorsque vous le ferez
- Lorsque vous souhaitez posséder une valeur et que vous vous souciez seulement du fait qu'elle soit d'un type qui implémente un trait particulier plutôt que d'un type spécifique

Nous démontrerons la première situation dans [“Activer les Types Récursifs avec des Boîtes”](#enabling-recursive-types-with-boxes). Dans le deuxième cas, le transfert de propriété d'une grande quantité de données peut prendre beaucoup de temps, car les données sont copiées sur la pile. Pour améliorer les performances dans cette situation, nous pouvons stocker la grande quantité de données sur le tas dans une boîte. Ensuite, seule une petite quantité de données de pointeur est copiée sur la pile, tandis que les données auxquelles elle fait référence restent en un seul endroit sur le tas. Le troisième cas est connu sous le nom d'_objet de trait_ et [“Utiliser des Objets de Trait pour Abstraire le Comportement Partagé”][trait-objects] dans le Chapitre 18 est consacré à ce sujet. Donc, ce que vous apprenez ici sera appliqué à nouveau dans cette section !

### Stockage des Données sur le Tas

Avant de discuter du cas d'utilisation du stockage sur le tas pour `Box<T>`, nous allons couvrir la syntaxe et comment interagir avec les valeurs stockées dans une `Box<T>`.

La Liste 15-1 montre comment utiliser une boîte pour stocker une valeur `i32` sur le tas.

<Liste numéro="15-1" nom-de-fichier="src/main.rs" légende="Stockage d'une valeur `i32` sur le tas en utilisant une boîte">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-01/src/main.rs}}
```

</Liste>

Nous définissons la variable `b` pour avoir la valeur d'une `Box` qui pointe vers la valeur `5`, qui est allouée sur le tas. Ce programme imprimera `b = 5` ; dans ce cas, nous pouvons accéder aux données dans la boîte de la même manière que si ces données étaient sur la pile. Tout comme toute valeur possédée, lorsqu'une boîte sort de son contexte, comme `b` à la fin de `main`, elle sera désallouée. La désallocation se produit à la fois pour la boîte (stockée sur la pile) et pour les données auxquelles elle pointe (stockées sur le tas).

Mettre une seule valeur sur le tas n'est pas très utile, donc vous n'utiliserez pas souvent les boîtes de cette manière. Avoir des valeurs comme un seul `i32` sur la pile, où elles sont stockées par défaut, est plus approprié dans la majorité des situations. Regardons un cas où les boîtes nous permettent de définir des types que nous ne pourrions pas définir si nous n'avions pas de boîtes.

### Activation des Types Récursifs avec des Boîtes

Une valeur d'un _type récursif_ peut contenir une autre valeur du même type comme partie de celle-ci. Les types récursifs posent un problème parce que Rust doit savoir à la compilation combien d'espace un type occupe. Cependant, l'imbrication des valeurs de types récursifs pourrait théoriquement continuer indéfiniment, donc Rust ne peut pas savoir combien d'espace la valeur nécessite. Comme les boîtes ont une taille connue, nous pouvons activer les types récursifs en insérant une boîte dans la définition du type récursif.

En guise d'exemple d'un type récursif, explorons la liste cons. C'est un type de données que l'on trouve couramment dans les langages de programmation fonctionnelle. Le type de liste cons que nous allons définir est simple sauf pour la récursion ; par conséquent, les concepts dans l'exemple avec lequel nous allons travailler seront utiles chaque fois que vous vous retrouverez dans des situations plus complexes impliquant des types récursifs.

#### Compréhension de la Liste Cons

Une _liste cons_ est une structure de données qui vient du langage de programmation Lisp et de ses dialectes, composée de paires imbriquées, et est la version Lisp d'une liste chaînée. Son nom vient de la fonction `cons` (abréviation de _construction de fonction_) dans Lisp qui construit une nouvelle paire à partir de ses deux arguments. En appelant `cons` sur une paire comprenant une valeur et une autre paire, nous pouvons construire des listes cons composées de paires récursives.

Par exemple, voici une représentation en pseudocode d'une liste cons contenant la liste `1, 2, 3` avec chaque paire entre parenthèses :

```text
(1, (2, (3, Nil)))
```

Chaque élément d'une liste cons contient deux éléments : la valeur de l'élément courant et celle de l'élément suivant. Le dernier élément de la liste ne contient qu'une valeur appelée `Nil` sans élément suivant. Une liste cons est produite en appelant récursivement la fonction `cons`. Le nom canonique pour désigner le cas de base de la récursion est `Nil`. Notez que cela ne correspond pas au concept de "null" ou "nil" discuté dans le Chapitre 6, qui est une valeur invalide ou absente.

La liste cons n'est pas une structure de données couramment utilisée dans Rust. La plupart du temps lorsque vous avez une liste d'éléments dans Rust, `Vec<T>` est un meilleur choix à utiliser. D'autres types de données récursifs plus complexes _sont_ utiles dans diverses situations, mais en commençant par la liste cons dans ce chapitre, nous pouvons explorer comment les boîtes nous permettent de définir un type de données récursives sans trop de distraction.

La Liste 15-2 contient une définition d'énumération pour une liste cons. Notez que ce code ne compilera pas encore, car le type `List` n'a pas de taille connue, ce que nous allons démontrer.

<Liste numéro="15-2" nom-de-fichier="src/main.rs" légende="La première tentative de définition d'une énumération pour représenter une structure de données liste cons de valeurs `i32`">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-02/src/main.rs:here}}
```

</Liste>

> Remarque : Nous mettons en œuvre une liste cons qui ne contient que des valeurs `i32` pour les besoins de cet exemple. Nous aurions pu l'implémenter en utilisant des génériques, comme nous en avons discuté dans le Chapitre 10, pour définir un type de liste cons qui pourrait stocker des valeurs de n'importe quel type.

Utiliser le type `List` pour stocker la liste `1, 2, 3` ressemblerait au code de la Liste 15-3.

<Liste numéro="15-3" nom-de-fichier="src/main.rs" légende="Utilisation de l'énumération `List` pour stocker la liste `1, 2, 3`">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-03/src/main.rs:here}}
```

</Liste>

La première valeur `Cons` contient `1` et une autre valeur `List`. Cette valeur `List` est une autre valeur `Cons` qui contient `2` et une autre valeur `List`. Cette valeur `List` est une valeur `Cons` qui contient `3` et une valeur `List`, qui est enfin `Nil`, la variante non-récursive qui signale la fin de la liste.

Si nous essayons de compiler le code dans la Liste 15-3, nous obtiendrons l'erreur montrée dans la Liste 15-4.

<Liste numéro="15-4" légende="L'erreur que nous recevons lors de la tentative de définition d'une énumération récursive">

```console
{{#include ../listings/ch15-smart-pointers/listing-15-03/output.txt}}
```

</Liste>

L'erreur indique que ce type "a une taille infinie". La raison est que nous avons défini `List` avec une variante qui est récursive : elle contient directement une autre valeur de lui-même. En conséquence, Rust ne peut pas déterminer combien d'espace il lui faut pour stocker une valeur `List`. Décomposons pourquoi nous obtenons cette erreur. Tout d'abord, nous allons examiner comment Rust décide de l'espace à allouer pour une valeur d'un type non récursif.

#### Calcul de la Taille d'un Type non Récursif

Rappelez-vous l'énumération `Message` que nous avons définie dans la Liste 6-2 lorsque nous avons discuté des définitions d'énumérations dans le Chapitre 6 :

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-02/src/main.rs:here}}
```

Pour déterminer quel espace allouer pour une valeur `Message`, Rust passe en revue chacune des variantes pour voir quelle variante nécessite le plus d'espace. Rust constate que `Message::Quit` n'a besoin d'aucun espace, `Message::Move` a besoin d'assez d'espace pour stocker deux valeurs `i32`, et ainsi de suite. Comme une seule variante sera utilisée, le plus d'espace requis pour une valeur `Message` sera l'espace qu'il faudrait pour stocker le plus grand de ses variantes.

Contrastez cela avec ce qui se passe lorsque Rust essaie de déterminer combien d'espace un type récursif comme l'énumération `List` dans la Liste 15-2 nécessite. Le compilateur commence par examiner la variante `Cons`, qui contient une valeur de type `i32` et une valeur de type `List`. Par conséquent, `Cons` a besoin d'un espace égal à la taille d'un `i32` plus la taille d'un `List`. Pour déterminer combien de mémoire le type `List` nécessite, le compilateur examine les variantes, en commençant par la variante `Cons`. La variante `Cons` contient une valeur de type `i32` et une valeur de type `List`, et ce processus continue indéfiniment, comme indiqué dans la Figure 15-1.

<img alt="Une liste Cons infinie : un rectangle étiqueté 'Cons' divisé en deux rectangles plus petits. Le premier rectangle plus petit porte l'étiquette 'i32', et le deuxième rectangle plus petit porte l'étiquette 'Cons' et une version plus petite du rectangle extérieur 'Cons'. Les rectangles 'Cons' continuent à contenir des versions de plus en plus petites d'eux-mêmes jusqu'à ce que le plus petit rectangle confortablement dimensionné contienne un symbole d'infinité, indiquant que cette répétition se poursuit éternellement." src="img/trpl15-01.svg" class="center" style="width: 50%;" />

<span class="caption">Figure 15-1 : Une `List` infinie composée de variantes `Cons` infinies</span>

#### Obtenir un Type Récursif avec une Taille Connue

Parce que Rust ne peut pas déterminer combien d'espace allouer pour les types définis de manière récursive, le compilateur donne une erreur avec cette suggestion utile :

```text
help: insérer une indirection (par exemple, un `Box`, `Rc`, ou `&`) pour briser le cycle
  |
2 |     Cons(i32, Box<List>),
  |               ++++    +
```

Dans cette suggestion, _indirection_ signifie qu'au lieu de stocker une valeur directement, nous devrions modifier la structure de données pour stocker la valeur de manière indirecte en stockant un pointeur vers la valeur à la place.

Comme un `Box<T>` est un pointeur, Rust sait toujours combien d'espace un `Box<T>` nécessite : la taille d'un pointeur ne change pas en fonction de la quantité de données qu'il pointe. Cela signifie que nous pouvons mettre un `Box<T>` dans la variante `Cons` au lieu d'une autre valeur `List` directement. Le `Box<T>` pointera vers la prochaine valeur `List` qui sera sur le tas plutôt qu'à l'intérieur de la variante `Cons`. Conceptuellement, nous avons toujours une liste, créée avec des listes contenant d'autres listes, mais cette implémentation ressemble maintenant plus à placer les éléments côte à côte plutôt qu'à l'intérieur les uns des autres.

Nous pouvons modifier la définition de l'énumération `List` dans la Liste 15-2 et l'utilisation de `List` dans la Liste 15-3 avec le code de la Liste 15-5, qui compilera.

<Liste numéro="15-5" nom-de-fichier="src/main.rs" légende="La définition de `List` qui utilise `Box<T>` afin d'avoir une taille connue">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-05/src/main.rs}}
```

</Liste>

La variante `Cons` nécessite la taille d'un `i32` plus l'espace pour stocker les données de pointeur de la boîte. La variante `Nil` ne stocke aucune valeur, donc elle a besoin de moins d'espace sur la pile que la variante `Cons`. Nous savons maintenant que toute valeur `List` prendra la taille d'un `i32` plus la taille des données de pointeur d'une boîte. En utilisant une boîte, nous avons brisé la chaîne récursive infinie, donc le compilateur peut déterminer la taille nécessaire pour stocker une valeur `List`. La Figure 15-2 montre à quoi ressemble maintenant la variante `Cons`.

<img alt="Un rectangle étiqueté 'Cons' divisé en deux rectangles plus petits. Le premier rectangle plus petit porte l'étiquette 'i32', et le deuxième rectangle plus petit porte l'étiquette 'Box' avec un rectangle intérieur contenant l'étiquette 'usize', représentant la taille finie des données de pointeur de la boîte." src="img/trpl15-02.svg" class="center" />

<span class="caption">Figure 15-2 : Une `List` qui n'a pas une taille infinie, car `Cons` contient un `Box`</span>

Les boîtes fournissent seulement l'indirection et l'allocation sur le tas ; elles n'ont pas d'autres capacités spéciales, comme celles que nous verrons avec les autres types de pointeurs intelligents. Elles n'ont également pas la surcharge de performance que ces capacités spéciales impliquent, donc elles peuvent être utiles dans des cas comme la liste cons où l'indirection est la seule fonctionnalité dont nous avons besoin. Nous examinerons d'autres cas d'utilisation pour les boîtes dans le Chapitre 18.

Le type `Box<T>` est un pointeur intelligent car il implémente le trait `Deref`, ce qui permet aux valeurs `Box<T>` d'être traitées comme des références. Lorsqu'une valeur `Box<T>` sort de son contexte, les données du tas auxquelles la boîte pointe sont également nettoyées en raison de l'implémentation du trait `Drop`. Ces deux traits seront encore plus importants pour la fonctionnalité fournie par les autres types de pointeurs intelligents dont nous discuterons dans le reste de ce chapitre. Explorons ces deux traits plus en détail.

[trait-objects]: ch18-02-trait-objects.html#using-trait-objects-to-abstract-over-shared-behavior