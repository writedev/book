## Caractéristiques des langages orientés objet

Il n'y a pas de consensus dans la communauté des programmeurs sur les fonctionnalités qu'un langage doit avoir pour être considéré comme orienté objet. Rust est influencé par de nombreux paradigmes de programmation, y compris la POO ; par exemple, nous avons exploré les caractéristiques issues de la programmation fonctionnelle dans le Chapitre 13. On peut dire que les langages POO partagent certaines caractéristiques communes, à savoir, les objets, l'encapsulation et l'héritage. Regardons ce que signifie chacune de ces caractéristiques et si Rust les prend en charge.

### Les objets contiennent des données et un comportement

Le livre _Design Patterns: Elements of Reusable Object-Oriented Software_ d'Erich Gamma, Richard Helm, Ralph Johnson et John Vlissides (Addison-Wesley, 1994), communément appelé _Le Gang des Quatre_, est un catalogue de modèles de conception orientés objet. Il définit la POO de cette manière :

> Les programmes orientés objet sont composés d’objets. Un **objet** regroupe à la fois des données et les procédures qui opèrent sur ces données. Les procédures sont généralement appelées **méthodes** ou **opérations**.

En utilisant cette définition, Rust est orienté objet : les structs et les enums contiennent des données, et les blocs `impl` fournissent des méthodes sur les structs et les enums. Même si les structs et les enums avec méthodes ne sont pas _appelés_ objets, elles fournissent la même fonctionnalité, selon la définition des objets du Gang des Quatre.

### Encapsulation qui cache les détails d'implémentation

Un autre aspect couramment associé à la POO est l'idée d'_encapsulation_, ce qui signifie que les détails d'implémentation d'un objet ne sont pas accessibles au code utilisant cet objet. Par conséquent, le seul moyen d'interagir avec un objet est à travers son API publique ; le code utilisant l'objet ne devrait pas être en mesure d'accéder aux internes de l'objet et de modifier directement les données ou le comportement. Cela permet au programmeur de changer et de refactoriser les internes d'un objet sans avoir à changer le code qui utilise l'objet.

Nous avons discuté de la manière de contrôler l'encapsulation dans le Chapitre 7 : nous pouvons utiliser le mot-clé `pub` pour décider quels modules, types, fonctions et méthodes dans notre code doivent être publics, et par défaut, tout le reste est privé. Par exemple, nous pouvons définir une struct `AveragedCollection` qui a un champ contenant un vecteur de valeurs `i32`. La struct peut également avoir un champ qui contient la moyenne des valeurs dans le vecteur, ce qui signifie que la moyenne n'a pas besoin d'être calculée à la demande chaque fois que quelqu'un en a besoin. En d'autres termes, `AveragedCollection` va mettre en cache la moyenne calculée pour nous. La liste 18-1 contient la définition de la struct `AveragedCollection`.

<Liste numéro="18-1" nom de fichier="src/lib.rs" légende="Une struct `AveragedCollection` qui maintient une liste d'entiers et la moyenne des éléments de la collection">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-01/src/lib.rs}}
```

</Liste>

La struct est marquée `pub` afin qu'un autre code puisse l'utiliser, mais les champs à l'intérieur de la struct restent privés. Cela est important dans ce cas car nous voulons nous assurer que chaque fois qu'une valeur est ajoutée ou supprimée de la liste, la moyenne est également mise à jour. Nous faisons cela en implémentant les méthodes `add`, `remove` et `average` sur la struct, comme le montre la liste 18-2.

<Liste numéro="18-2" nom de fichier="src/lib.rs" légende="Implémentations des méthodes publiques `add`, `remove` et `average` sur `AveragedCollection`">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-02/src/lib.rs:here}}
```

</Liste>

Les méthodes publiques `add`, `remove` et `average` sont les seules façons d'accéder ou de modifier les données dans une instance de `AveragedCollection`. Lorsqu'un élément est ajouté à `list` à l'aide de la méthode `add` ou supprimé à l'aide de la méthode `remove`, les implémentations de chacune appellent la méthode privée `update_average` qui gère également la mise à jour du champ `average`.

Nous laissons les champs `list` et `average` privés afin qu'il n'y ait aucun moyen pour le code externe d'ajouter ou de supprimer des éléments dans le champ `list` directement ; sinon, le champ `average` pourrait devenir désynchronisé lorsque le `list` change. La méthode `average` retourne la valeur dans le champ `average`, permettant au code externe de lire l'`average` mais pas de le modifier.

Parce que nous avons encapsulé les détails d'implémentation de la struct `AveragedCollection`, nous pouvons facilement changer des aspects, tels que la structure des données, à l'avenir. Par exemple, nous pourrions utiliser un `HashSet<i32>` au lieu d'un `Vec<i32>` pour le champ `list`. Tant que les signatures des méthodes publiques `add`, `remove` et `average` restent les mêmes, le code utilisant `AveragedCollection` n'aurait pas besoin de changer. Si nous rendions `list` public à la place, cela ne serait pas nécessairement le cas : `HashSet<i32>` et `Vec<i32>` ont des méthodes différentes pour ajouter et supprimer des éléments, donc le code externe devrait probablement changer s'il modifiait `list` directement.

Si l'encapsulation est un aspect requis pour qu'un langage soit considéré comme orienté objet, alors Rust répond à cette exigence. L'option d'utiliser `pub` ou non pour différentes parties du code permet l'encapsulation des détails d'implémentation.

### Héritage comme système de types et partage de code

_L'héritage_ est un mécanisme par lequel un objet peut hériter d'éléments de la définition d'un autre objet, acquérant ainsi les données et le comportement de l'objet parent sans que vous ayez à les redéfinir.

Si un langage doit avoir l'héritage pour être orienté objet, alors Rust n'est pas un tel langage. Il n'est pas possible de définir une struct qui hérite des champs et des implémentations de méthode de la struct parente sans utiliser un macro.

Cependant, si vous êtes habitué à avoir l'héritage dans votre boîte à outils de programmation, vous pouvez utiliser d'autres solutions dans Rust, en fonction de votre raison de recourir à l'héritage en premier lieu.

Vous choisiriez l'héritage pour deux raisons principales. La première est la réutilisation de code : vous pouvez implémenter un comportement particulier pour un type, et l'héritage vous permet de réutiliser cette implémentation pour un autre type. Vous pouvez le faire d'une manière limitée dans le code Rust en utilisant les implémentations par défaut des méthodes de trait, ce que vous avez vu dans la liste 10-14 lorsque nous avons ajouté une implémentation par défaut de la méthode `summarize` sur le trait `Summary`. Tout type implémentant le trait `Summary` aurait la méthode `summarize` disponible sans code supplémentaire. Cela est similaire à une classe parente ayant une implémentation d'une méthode et une classe enfant héritant également de l'implémentation de la méthode. Nous pouvons également remplacer l'implémentation par défaut de la méthode `summarize` lorsque nous implémentons le trait `Summary`, ce qui est similaire à une classe enfant remplaçant l'implémentation d'une méthode héritée d'une classe parente.

L'autre raison d'utiliser l'héritage concerne le système de types : permettre à un type enfant d'être utilisé aux mêmes endroits que le type parent. Cela s'appelle également _polymorphisme_, ce qui signifie que vous pouvez substituer plusieurs objets les uns aux autres à l'exécution s'ils partagent certaines caractéristiques.

> ### Polymorphisme
>
> Pour beaucoup de gens, le polymorphisme est synonyme d'héritage. Mais c'est en réalité un concept plus général qui fait référence à du code pouvant travailler avec des données de multiples types. Pour l'héritage, ces types sont généralement des sous-classes.
>
> Rust utilise plutôt des génériques pour abstraire différents types possibles et des contraintes de trait pour imposer des contraintes sur ce que ces types doivent fournir. Cela est parfois appelé _polymorphisme paramétrique borné_.

Rust a choisi un ensemble différent de compromis en ne proposant pas d'héritage. L'héritage est souvent à risque de partager plus de code que nécessaire. Les sous-classes ne devraient pas toujours partager toutes les caractéristiques de leur classe parente, mais le feront avec l'héritage. Cela peut rendre la conception d'un programme moins flexible. Cela introduit également la possibilité d'appeler des méthodes sur des sous-classes qui n'ont pas de sens ou qui provoquent des erreurs parce que les méthodes ne s'appliquent pas à la sous-classe. De plus, certains langages n'autorisent que l'_héritage simple_ (ce qui signifie qu'une sous-classe ne peut hériter que d'une seule classe), restreignant encore la flexibilité de la conception d'un programme.

Pour ces raisons, Rust adopte l'approche différente d'utiliser des objets de trait au lieu de l'héritage pour atteindre le polymorphisme à l'exécution. Voyons comment fonctionnent les objets de trait.