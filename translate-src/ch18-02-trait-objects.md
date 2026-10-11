<!-- Old headings. Do not remove or links may break. -->

<a id="using-trait-objects-that-allow-for-values-of-different-types"></a>

## Utiliser des objets de trait pour abstraire un comportement partagé

Au chapitre 8, nous avons mentionné que l’une des limites des vecteurs est qu’ils ne peuvent stocker des éléments que d’un seul type. Nous avons créé une solution de contournement dans la liste 8-9, où nous avons défini une énumération `SpreadsheetCell` comportant des variantes capables de contenir des entiers, des nombres à virgule flottante et du texte. Cela nous permettait de stocker différents types de données dans chaque cellule tout en conservant un vecteur représentant une ligne de cellules. C’est une très bonne solution lorsque les éléments interchangeables appartiennent à un ensemble fixe de types que nous connaissons au moment de la compilation de notre code.

Cependant, nous voulons parfois permettre aux utilisateurs de notre bibliothèque d’étendre l’ensemble des types valides dans une situation donnée. Pour montrer comment y parvenir, nous allons créer un exemple d’outil d’interface graphique (GUI) qui parcourt une liste d’éléments et appelle une méthode `draw` sur chacun d’eux pour l’afficher à l’écran — une technique courante dans les outils GUI. Nous allons créer une crate de bibliothèque appelée `gui`, qui contiendra la structure d’une bibliothèque GUI. Cette crate pourrait inclure certains types utilisables, tels que `Button` ou `TextField`. De plus, les utilisateurs de `gui` voudront créer leurs propres types qui peuvent être affichés : par exemple, un programmeur pourrait ajouter une `Image`, et un autre, une `SelectBox`.

Au moment d’écrire la bibliothèque, nous ne pouvons pas connaître et définir tous les types que d’autres programmeurs pourraient vouloir créer. Mais nous savons que `gui` doit suivre de nombreuses valeurs de types différents et appeler une méthode `draw` sur chacune de ces valeurs de types différents. Il n’a pas besoin de savoir exactement ce qui se passera lorsque nous appellerons la méthode `draw`, seulement que la valeur disposera de cette méthode que nous pourrons appeler.

Dans un langage doté de l’héritage, nous pourrions définir une classe nommée `Component` qui possède une méthode nommée `draw`. Les autres classes, telles que `Button`, `Image` et `SelectBox`, hériteraient de `Component` et, par conséquent, de la méthode `draw`. Elles pourraient chacune redéfinir la méthode `draw` pour définir leur comportement personnalisé, mais l’infrastructure pourrait traiter tous les types comme s’il s’agissait d’instances de `Component` et appeler `draw` sur elles. Mais comme Rust ne dispose pas de l’héritage, nous avons besoin d’une autre façon de structurer la bibliothèque `gui` pour permettre aux utilisateurs de créer de nouveaux types compatibles avec la bibliothèque.

### Définir un trait pour un comportement commun

Pour implémenter le comportement souhaité pour `gui`, nous allons définir un trait nommé `Draw` qui aura une méthode nommée `draw`. Nous pourrons ensuite définir un vecteur qui accepte un objet de trait. Un _objet de trait_ pointe à la fois vers une instance d’un type qui implémente le trait indiqué et vers une table utilisée pour rechercher les méthodes du trait sur ce type à l’exécution. Nous créons un objet de trait en indiquant une sorte de pointeur, tel qu’une référence ou un pointeur intelligent `Box<T>`, puis le mot-clé `dyn`, et enfin le trait concerné. (Nous aborderons la raison pour laquelle les objets de trait doivent utiliser un pointeur dans [« Les types à taille dynamique et le trait `Sized` »][dynamically-sized]<!-- ignore --> au chapitre 20.) Nous pouvons utiliser des objets de trait à la place d’un type générique ou concret. Partout où nous utilisons un objet de trait, le système de types de Rust garantit à la compilation que toute valeur utilisée dans ce contexte implémentera le trait de l’objet de trait. Par conséquent, nous n’avons pas besoin de connaître tous les types possibles à la compilation.

Nous avons indiqué qu’en Rust, nous évitons d’appeler les structs et les énumérations des « objets » afin de les distinguer des objets des autres langages. Dans une struct ou une énumération, les données des champs de la struct et le comportement des blocs `impl` sont séparés, tandis que dans d’autres langages, les données et le comportement réunis en un seul concept sont souvent qualifiés d’objet. Les objets de trait diffèrent des objets des autres langages en ce que nous ne pouvons pas leur ajouter de données. Les objets de trait ne sont pas aussi généralement utiles que les objets des autres langages : leur objectif précis est de permettre l’abstraction autour d’un comportement commun.

La liste 18-3 montre comment définir un trait nommé `Draw` avec une méthode nommée `draw`.

<Listing number="18-3" file-name="src/lib.rs" caption="Définition du trait `Draw`">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-03/src/lib.rs}}
```

</Listing>

Cette syntaxe devrait vous être familière, d’après nos discussions sur la définition des traits au chapitre 10. Voici maintenant une nouvelle syntaxe : la liste 18-4 définit une struct nommée `Screen` qui contient un vecteur nommé `components`. Ce vecteur est de type `Box<dyn Draw>`, qui est un objet de trait ; il représente n’importe quel type contenu dans un `Box` qui implémente le trait `Draw`.

<Listing number="18-4" file-name="src/lib.rs" caption="Définition de la struct `Screen` avec un champ `components` contenant un vecteur d’objets de trait qui implémentent le trait `Draw`">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-04/src/lib.rs:here}}
```

</Listing>

Dans la struct `Screen`, nous allons définir une méthode nommée `run` qui appellera la méthode `draw` sur chacun de ses `components`, comme le montre la liste 18-5.

<Listing number="18-5" file-name="src/lib.rs" caption="Une méthode `run` sur `Screen` qui appelle la méthode `draw` sur chaque composant">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-05/src/lib.rs:here}}
```

</Listing>

Cette méthode fonctionne différemment de la définition d’une struct qui utilise un paramètre de type générique assorti de bornes de trait. Un paramètre de type générique ne peut être remplacé que par un seul type concret à la fois, tandis que les objets de trait permettent à plusieurs types concrets de se substituer à l’objet de trait à l’exécution. Par exemple, nous aurions pu définir la struct `Screen` avec un type générique et une borne de trait, comme dans la liste 18-6.

<Listing number="18-6" file-name="src/lib.rs" caption="Une autre implémentation de la struct `Screen` et de sa méthode `run` utilisant des types génériques et des bornes de trait">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-06/src/lib.rs:here}}
```

</Listing>

Cela nous limite à une instance de `Screen` dont la liste de composants est entièrement de type `Button` ou entièrement de type `TextField`. Si vous n’aurez jamais que des collections homogènes, il est préférable d’utiliser des types génériques et des bornes de trait, car les définitions seront monomorphisées à la compilation pour utiliser les types concrets.

En revanche, avec la méthode utilisant des objets de trait, une instance de `Screen` peut contenir un `Vec<T>` qui comprend aussi bien un `Box<Button>` qu’un `Box<TextField>`. Voyons comment cela fonctionne, puis nous parlerons des conséquences sur les performances à l’exécution.

### Implémenter le trait

Nous allons maintenant ajouter des types qui implémentent le trait `Draw`. Nous fournirons le type `Button`. Là encore, l’implémentation d’une véritable bibliothèque GUI dépasse le cadre de ce livre ; le corps de la méthode `draw` ne contiendra donc aucune implémentation utile. Pour imaginer à quoi cette implémentation pourrait ressembler, une struct `Button` pourrait comporter des champs `width`, `height` et `label`, comme le montre la liste 18-7.

<Listing number="18-7" file-name="src/lib.rs" caption="Une struct `Button` qui implémente le trait `Draw`">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-07/src/lib.rs:here}}
```

</Listing>

Les champs `width`, `height` et `label` de `Button` seront différents de ceux des autres composants ; par exemple, un type `TextField` pourrait comporter ces mêmes champs ainsi qu’un champ `placeholder`. Chacun des types que nous voulons afficher à l’écran implémentera le trait `Draw`, mais utilisera un code différent dans la méthode `draw` pour définir comment afficher ce type particulier, comme le fait ici `Button` (sans le véritable code GUI, comme nous l’avons mentionné). Le type `Button`, par exemple, pourrait avoir un bloc `impl` supplémentaire contenant des méthodes liées à ce qui se passe lorsqu’un utilisateur clique sur le bouton. Ce genre de méthodes ne s’appliquerait pas à des types comme `TextField`.

Si une personne utilisant notre bibliothèque décide d’implémenter une struct `SelectBox` comportant les champs `width`, `height` et `options`, elle implémentera également le trait `Draw` pour le type `SelectBox`, comme le montre la liste 18-8.

<Listing number="18-8" file-name="src/main.rs" caption="Une autre crate utilisant `gui` et implémentant le trait `Draw` pour une struct `SelectBox`">

```rust,ignore
{{#rustdoc_include ../listings/ch18-oop/listing-18-08/src/main.rs:here}}
```

</Listing>

L’utilisateur de notre bibliothèque peut maintenant écrire sa fonction `main` pour créer une instance de `Screen`. Il peut ajouter une `SelectBox` et un `Button` à cette instance de `Screen` en plaçant chacun dans un `Box<T>` pour en faire un objet de trait. Il peut ensuite appeler la méthode `run` sur l’instance de `Screen`, qui appellera `draw` sur chacun des composants. La liste 18-9 montre cette implémentation.

<Listing number="18-9" file-name="src/main.rs" caption="Utilisation d’objets de trait pour stocker des valeurs de différents types qui implémentent le même trait">

```rust,ignore
{{#rustdoc_include ../listings/ch18-oop/listing-18-09/src/main.rs:here}}
```

</Listing>

Lorsque nous avons écrit la bibliothèque, nous ne savions pas que quelqu’un pourrait ajouter le type `SelectBox`, mais notre implémentation de `Screen` a pu fonctionner avec ce nouveau type et l’afficher, car `SelectBox` implémente le trait `Draw`, ce qui signifie qu’il implémente la méthode `draw`.

Ce concept — qui consiste à ne s’intéresser qu’aux messages auxquels une valeur répond, plutôt qu’à son type concret — est similaire au concept de _typage canard_ dans les langages à typage dynamique : si ça marche comme un canard et que ça cancane comme un canard, alors ça doit être un canard ! Dans l’implémentation de `run` sur `Screen` de la liste 18-5, `run` n’a pas besoin de connaître le type concret de chaque composant. Elle ne vérifie pas si un composant est une instance de `Button` ou de `SelectBox` ; elle appelle simplement la méthode `draw` sur le composant. En spécifiant `Box<dyn Draw>` comme type des valeurs du vecteur `components`, nous avons défini `Screen` de manière à ce qu’il ait besoin de valeurs sur lesquelles nous pouvons appeler la méthode `draw`.

L’avantage d’utiliser des objets de trait et le système de types de Rust pour écrire du code similaire à du code utilisant le typage canard, c’est que nous n’avons jamais à vérifier à l’exécution si une valeur implémente une méthode particulière, ni à craindre de provoquer des erreurs en appelant une méthode qu’une valeur n’implémente pas. Rust ne compilera pas notre code si les valeurs n’implémentent pas les traits requis par les objets de trait.

Par exemple, la liste 18-10 montre ce qui se passe si nous essayons de créer un `Screen` dont un composant est une `String`.

<Listing number="18-10" file-name="src/main.rs" caption="Tentative d’utilisation d’un type qui n’implémente pas le trait requis par l’objet de trait">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch18-oop/listing-18-10/src/main.rs}}
```

</Listing>

Nous obtiendrons cette erreur parce que `String` n’implémente pas le trait `Draw` :

```console
{{#include ../listings/ch18-oop/listing-18-10/output.txt}}
```

Cette erreur nous indique soit que nous transmettons à `Screen` quelque chose que nous ne voulions pas lui transmettre et que nous devrions donc utiliser un autre type, soit que nous devrions implémenter `Draw` pour `String`, afin que `Screen` puisse appeler `draw` dessus.

<!-- Old headings. Do not remove or links may break. -->

<a id="trait-objects-perform-dynamic-dispatch"></a>

### Effectuer une répartition dynamique

Rappelez-vous notre discussion au chapitre 10 sur le processus de monomorphisation appliqué aux types génériques par le compilateur, dans [« Performances du code utilisant des types génériques »][performance-of-code-using-generics]<!-- ignore --> : le compilateur génère des implémentations non génériques des fonctions et des méthodes pour chaque type concret utilisé à la place d’un paramètre de type générique. Le code issu de la monomorphisation effectue une _répartition statique_, c’est-à-dire que le compilateur sait quelle méthode vous appelez à la compilation. À l’inverse, la _répartition dynamique_ est utilisée lorsque le compilateur ne peut pas déterminer à la compilation quelle méthode vous appelez. Dans les cas de répartition dynamique, le compilateur génère du code qui saura à l’exécution quelle méthode appeler.

Lorsque nous utilisons des objets de trait, Rust doit utiliser la répartition dynamique. Le compilateur ne connaît pas tous les types susceptibles d’être utilisés avec le code qui utilise des objets de trait ; il ne sait donc pas quelle méthode, implémentée pour quel type, appeler. À la place, à l’exécution, Rust utilise les pointeurs contenus dans l’objet de trait pour savoir quelle méthode appeler. Cette recherche entraîne un coût à l’exécution qui n’existe pas avec la répartition statique. La répartition dynamique empêche également le compilateur de choisir d’inliner le code d’une méthode, ce qui empêche à son tour certaines optimisations. Rust impose aussi des règles concernant les endroits où la répartition dynamique peut ou ne peut pas être utilisée, appelées _compatibilité avec `dyn`_. Ces règles dépassent le cadre de cette discussion, mais vous pouvez en apprendre davantage [dans la référence][dyn-compatibility]<!-- ignore -->. Cependant, nous avons gagné en flexibilité dans le code écrit dans la liste 18-5 et avons pu le prendre en charge dans la liste 18-9 ; c’est donc un compromis à prendre en compte.

[performance-of-code-using-generics]: ch10-01-syntax.html#performance-of-code-using-generics
[dynamically-sized]: ch20-03-advanced-types.html#dynamically-sized-types-and-the-sized-trait
[dyn-compatibility]: https://doc.rust-lang.org/reference/items/traits.html#dyn-compatibility