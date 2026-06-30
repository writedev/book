<!-- Anciennes rubriques. Ne pas supprimer sinon les liens pourraient se briser. -->

<a id="using-trait-objects-that-allow-for-values-of-different-types"></a>

## Utiliser des objets de trait pour abstraire un comportement partagé

Dans le chapitre 8, nous avons mentionné qu'une des limitations des vecteurs est qu'ils ne peuvent stocker des éléments que d'un seul type. Nous avons trouvé une solution dans la liste 8-9 où nous avons défini une énumération `SpreadsheetCell` qui avait des variantes pour contenir des entiers, des flottants et du texte. Cela signifiait que nous pouvions stocker différents types de données dans chaque cellule et avoir tout de même un vecteur représentant une ligne de cellules. C'est une solution parfaitement valable lorsque nos éléments interchangeables sont un ensemble fixe de types que nous connaissons au moment où notre code est compilé.

Cependant, parfois, nous voulons que l'utilisateur de notre bibliothèque puisse étendre l'ensemble des types valides dans une situation particulière. Pour montrer comment nous pourrions y parvenir, nous allons créer un outil d'interface graphique (GUI) qui itère à travers une liste d'éléments, appelant une méthode `draw` sur chacun d'eux pour les dessiner à l'écran — une technique courante dans les outils GUI. Nous allons créer une crate de bibliothèque appelée `gui` qui contient la structure d'une bibliothèque GUI. Cette crate pourrait inclure certains types que les gens peuvent utiliser, tels que `Button` ou `TextField`. De plus, les utilisateurs de `gui` voudront créer leurs propres types qui peuvent être dessinés : par exemple, un programmeur pourrait ajouter une `Image`, et un autre pourrait ajouter un `SelectBox`.

Au moment d'écrire la bibliothèque, nous ne pouvons pas connaître et définir tous les types que d'autres programmeurs pourraient vouloir créer. Mais nous savons que `gui` doit suivre de nombreuses valeurs de différents types et qu'elle doit appeler une méthode `draw` sur chacune de ces valeurs de types différents. Il n'est pas nécessaire qu'elle sache exactement ce qui se passera lorsque nous appelons la méthode `draw`, juste que la valeur aura cette méthode disponible pour que nous l'appelions.

Pour faire cela dans un langage avec héritage, nous pourrions définir une classe nommée `Component` qui a une méthode nommée `draw`. Les autres classes, comme `Button`, `Image` et `SelectBox`, hériteraient de `Component` et hériteraient ainsi de la méthode `draw`. Elles pourraient chacune remplacer la méthode `draw` pour définir leur comportement personnalisé, mais le framework pourrait traiter tous les types comme s'ils étaient des instances de `Component` et appeler `draw` sur eux. Mais comme Rust n'a pas d'héritage, nous avons besoin d'un autre moyen de structurer la bibliothèque `gui` pour permettre aux utilisateurs de créer de nouveaux types compatibles avec la bibliothèque.

### Définir un trait pour un comportement commun

Pour mettre en œuvre le comportement que nous voulons que `gui` ait, nous allons définir un trait nommé `Draw` qui aura une méthode nommée `draw`. Ensuite, nous pouvons définir un vecteur qui prend un objet de trait. Un _objet de trait_ pointe à la fois vers une instance d'un type implémentant notre trait spécifié et une table utilisée pour rechercher les méthodes de trait sur ce type au moment de l'exécution. Nous créons un objet de trait en spécifiant une sorte de pointeur, tel qu'une référence ou un pointeur intelligent `Box<T>`, puis le mot-clé `dyn`, et ensuite en spécifiant le trait pertinent. (Nous parlerons de la raison pour laquelle les objets de trait doivent utiliser un pointeur dans [“Types Dynamiquement Dimensionnés et le Trait `Sized`][dynamically-sized]<!-- ignore --> dans le chapitre 20.) Nous pouvons utiliser des objets de trait à la place d'un type générique ou concret. Partout où nous utilisons un objet de trait, le système de types de Rust veillera à ce que, au moment de la compilation, toute valeur utilisée dans ce contexte implémente le trait de l'objet de trait. Par conséquent, nous n'avons pas besoin de connaître tous les types possibles au moment de la compilation.

Nous avons mentionné qu'en Rust, nous évitons d'appeler des structs et des enums "objets" pour les distinguer des objets d'autres langages. Dans une struct ou une énumération, les données dans les champs de struct et le comportement dans les blocs `impl` sont séparés, tandis que dans d'autres langages, les données et le comportement combinés en un seul concept sont souvent qualifiés d'objet. Les objets de trait diffèrent des objets dans d'autres langages en ce sens que nous ne pouvons pas ajouter de données à un objet de trait. Les objets de trait ne sont pas aussi généralement utiles que les objets dans d'autres langages : leur but spécifique est de permettre l'abstraction d'un comportement commun.

La liste 18-3 montre comment définir un trait nommé `Draw` avec une méthode nommée `draw`.

<Listing number="18-3" file-name="src/lib.rs" caption="Définition du trait `Draw`">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-03/src/lib.rs}}
```

</Listing>

Cette syntaxe devrait vous sembler familière suite à nos discussions sur la manière de définir des traits dans le chapitre 10. Vient ensuite une nouvelle syntaxe : la liste 18-4 définit une struct nommée `Screen` qui contient un vecteur nommé `components`. Ce vecteur est de type `Box<dyn Draw>`, qui est un objet de trait ; c'est un substitut pour tout type à l'intérieur d'une `Box` qui implémente le trait `Draw`.

<Listing number="18-4" file-name="src/lib.rs" caption="Définition de la struct `Screen` avec un champ `components` contenant un vecteur d'objets de trait qui implémentent le trait `Draw`">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-04/src/lib.rs:here}}
```

</Listing>

Sur la struct `Screen`, nous allons définir une méthode nommée `run` qui appellera la méthode `draw` sur chacun de ses `components`, comme le montre la liste 18-5.

<Listing number="18-5" file-name="src/lib.rs" caption="Une méthode `run` sur `Screen` qui appelle la méthode `draw` sur chaque composant">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-05/src/lib.rs:here}}
```

</Listing>

Cela fonctionne différemment de la définition d'une struct qui utilise un paramètre de type générique avec des limites de trait. Un paramètre de type générique ne peut être substitué qu'avec un seul type concret à la fois, tandis que les objets de trait permettent à plusieurs types concrets de remplir l'objet de trait au moment de l'exécution. Par exemple, nous aurions pu définir la struct `Screen` en utilisant un type générique et une limite de trait, comme dans la liste 18-6.

<Listing number="18-6" file-name="src/lib.rs" caption="Une implémentation alternative de la struct `Screen` et de sa méthode `run` utilisant des génériques et des limites de trait">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-06/src/lib.rs:here}}
```

</Listing>

Cela nous limite à une instance de `Screen` ayant une liste de composants tous de type `Button` ou tous de type `TextField`. Si vous n'aurez jamais que des collections homogènes, l'utilisation de génériques et de limites de trait est préférable car les définitions seront monomorphisées au moment de la compilation pour utiliser les types concrets.

D'un autre côté, avec la méthode utilisant des objets de trait, une instance de `Screen` peut contenir un `Vec<T>` contenant à la fois un `Box<Button>` et un `Box<TextField>`. Voyons comment cela fonctionne, puis nous parlerons des implications de performance à l'exécution.

### Implémentation du trait

Nous allons maintenant ajouter des types qui implémentent le trait `Draw`. Nous allons fournir le type `Button`. Encore une fois, implémenter réellement une bibliothèque GUI dépasse le cadre de ce livre, donc la méthode `draw` n'aura pas d'implémentation utile dans son corps. Pour imaginer à quoi pourrait ressembler l'implémentation, une struct `Button` pourrait avoir des champs pour `width`, `height` et `label`, comme le montre la liste 18-7.

<Listing number="18-7" file-name="src/lib.rs" caption="Une struct `Button` qui implémente le trait `Draw`">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-07/src/lib.rs:here}}
```

</Listing>

Les champs `width`, `height` et `label` sur `Button` différeront des champs sur d'autres composants ; par exemple, un type `TextField` pourrait avoir ces mêmes champs plus un champ `placeholder`. Chacun des types que nous souhaitons dessiner à l'écran implémentera le trait `Draw` mais utilisera un code différent dans la méthode `draw` pour définir comment dessiner ce type particulier, comme `Button` l'a ici (sans le code GUI réel, comme mentionné). Le type `Button`, par exemple, pourrait avoir un bloc `impl` supplémentaire contenant des méthodes liées à ce qui se passe lorsque l'utilisateur clique sur le bouton. Ces types de méthodes ne s'appliqueront pas à des types comme `TextField`.

Si quelqu'un utilisant notre bibliothèque décide d'implémenter une struct `SelectBox` qui a des champs `width`, `height` et `options`, il implémenterait également le trait `Draw` sur le type `SelectBox`, comme le montre la liste 18-8.

<Listing number="18-8" file-name="src/main.rs" caption="Une autre crate utilisant `gui` et implémentant le trait `Draw` sur une struct `SelectBox`">

```rust,ignore
{{#rustdoc_include ../listings/ch18-oop/listing-18-08/src/main.rs:here}}
```

</Listing>

L'utilisateur de notre bibliothèque peut maintenant écrire sa fonction `main` pour créer une instance de `Screen`. Il peut ajouter un `SelectBox` et un `Button` à l'instance de `Screen` en mettant chacun dans une `Box<T>` pour devenir un objet de trait. Il peut ensuite appeler la méthode `run` sur l'instance de `Screen`, qui appellera `draw` sur chacun des composants. La liste 18-9 montre cette implémentation.

<Listing number="18-9" file-name="src/main.rs" caption="Utiliser des objets de trait pour stocker des valeurs de différents types qui implémentent le même trait">

```rust,ignore
{{#rustdoc_include ../listings/ch18-oop/listing-18-09/src/main.rs:here}}
```

</Listing>

Lorsque nous avons écrit la bibliothèque, nous ne savions pas que quelqu'un pourrait ajouter le type `SelectBox`, mais notre implémentation de `Screen` a pu fonctionner sur le nouveau type et le dessiner parce que `SelectBox` implémente le trait `Draw`, ce qui signifie qu'il implémente la méthode `draw`.

Ce concept — d'être préoccupé uniquement par les messages qu'une valeur répond plutôt que par le type concret de la valeur — est similaire au concept de _duck typing_ dans les langages à typage dynamique : Si cela marche comme un canard et couine comme un canard, alors cela doit être un canard ! Dans l'implémentation de `run` sur `Screen` dans la liste 18-5, `run` n'a pas besoin de savoir quel est le type concret de chaque composant. Il ne vérifie pas si un composant est une instance d'un `Button` ou d'un `SelectBox`, il appelle simplement la méthode `draw` sur le composant. En spécifiant `Box<dyn Draw>` comme type des valeurs dans le vecteur `components`, nous avons défini `Screen` comme ayant besoin de valeurs sur lesquelles nous pouvons appeler la méthode `draw`.

L'avantage d'utiliser des objets de trait et le système de types de Rust pour écrire du code similaire à du code utilisant du duck typing est que nous n'avons jamais à vérifier si une valeur implémente une méthode particulière à l'exécution ou à nous soucier de recevoir des erreurs si une valeur n'implémente pas une méthode mais que nous l'appelons quand même. Rust ne compilera pas notre code si les valeurs n'implémentent pas les traits requis par les objets de trait.

Par exemple, la liste 18-10 montre ce qui se passe si nous essayons de créer un `Screen` avec un `String` comme composant.

<Listing number="18-10" file-name="src/main.rs" caption="Tentative d'utilisation d'un type qui n'implémente pas le trait de l'objet de trait">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch18-oop/listing-18-10/src/main.rs}}
```

</Listing>

Nous obtiendrons cette erreur parce que `String` n'implémente pas le trait `Draw` :

```console
{{#include ../listings/ch18-oop/listing-18-10/output.txt}}
```

Cette erreur nous permet de savoir soit que nous passons quelque chose à `Screen` que nous n'avions pas l'intention de passer et que nous devrions donc passer un type différent, soit que nous devrions implémenter `Draw` sur `String` afin que `Screen` puisse appeler `draw` dessus.

<!-- Anciennes rubriques. Ne pas supprimer sinon les liens pourraient se briser. -->

<a id="trait-objects-perform-dynamic-dispatch"></a>

### Effectuer un dispatch dynamique

Rappelez-vous dans [“Performance du code utilisant des génériques”][performance-of-code-using-generics]<!-- ignore --> dans le chapitre 10 notre discussion sur le processus de monomorphisation effectué par le compilateur sur les génériques : Le compilateur génère des implémentations non génériques de fonctions et de méthodes pour chaque type concret que nous utilisons à la place d'un paramètre de type générique. Le code qui résulte de la monomorphisation utilise le _dispatch statique_, qui est lorsque le compilateur sait quelle méthode vous appelez à la compilation. Cela s'oppose à _dispatch dynamique_, qui est lorsque le compilateur ne peut pas savoir à la compilation quelle méthode vous appelez. Dans les cas de dispatch dynamique, le compilateur émet un code qui, à l'exécution, saura quelle méthode appeler.

Lorsque nous utilisons des objets de trait, Rust doit utiliser le dispatch dynamique. Le compilateur ne connaît pas tous les types qui pourraient être utilisés avec le code utilisant des objets de trait, donc il ne sait pas quelle méthode implémentée sur quel type appeler. Au lieu de cela, à l'exécution, Rust utilise les pointeurs à l'intérieur de l'objet de trait pour savoir quelle méthode appeler. Cette recherche engendre un coût à l'exécution qui n'a pas lieu avec le dispatch statique. Le dispatch dynamique empêche également le compilateur de choisir d'inliner le code d'une méthode, ce qui empêche certaines optimisations, et Rust a certaines règles concernant où vous pouvez et ne pouvez pas utiliser le dispatch dynamique, appelées _compatibilité dyn_. Ces règles dépassent le cadre de cette discussion, mais vous pouvez en lire davantage [dans la référence][dyn-compatibility]<!-- ignore -->. Cependant, nous avons obtenu une flexibilité supplémentaire dans le code que nous avons écrit dans la liste 18-5 et que nous avons pu soutenir dans la liste 18-9, donc c'est un compromis à considérer.

[performance-of-code-using-generics]: ch10-01-syntax.html#performance-of-code-using-generics
[dynamically-sized]: ch20-03-advanced-types.html#dynamically-sized-types-and-the-sized-trait
[dyn-compatibility]: https://doc.rust-lang.org/reference/items/traits.html#dyn-compatibility