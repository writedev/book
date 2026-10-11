## Caractéristiques des langages orientés objet

La communauté de la programmation ne s’accorde pas sur les caractéristiques qu’un langage doit posséder pour être considéré comme orienté objet. Rust est influencé par de nombreux paradigmes de programmation, notamment la programmation orientée objet ; par exemple, nous avons exploré au chapitre 13 les caractéristiques issues de la programmation fonctionnelle. On peut soutenir que les langages orientés objet partagent certaines caractéristiques communes, à savoir les objets, l’encapsulation et l’héritage. Voyons ce que signifie chacune de ces caractéristiques et si Rust la prend en charge.

### Les objets contiennent des données et un comportement

Le livre _Design Patterns: Elements of Reusable Object-Oriented Software_ d’Erich Gamma, Richard Helm, Ralph Johnson et John Vlissides (Addison-Wesley, 1994), communément appelé _le livre du Gang of Four_, est un recueil de patrons de conception orientés objet. Il définit la programmation orientée objet ainsi :

> Les programmes orientés objet sont constitués d’objets. Un **objet** regroupe à la fois des données et les procédures qui agissent sur ces données. Ces procédures sont généralement appelées **méthodes** ou **opérations**.

Selon cette définition, Rust est orienté objet : les structures et les énumérations contiennent des données, et les blocs `impl` fournissent des méthodes pour les structures et les énumérations. Même si les structures et les énumérations dotées de méthodes ne sont pas appelées des _objets_, elles fournissent les mêmes fonctionnalités, selon la définition des objets du Gang of Four.

### L’encapsulation masque les détails d’implémentation

Un autre aspect couramment associé à la programmation orientée objet est la notion d’_encapsulation_, qui signifie que les détails d’implémentation d’un objet ne sont pas accessibles au code qui utilise cet objet. Par conséquent, la seule façon d’interagir avec un objet est de passer par son API publique ; le code qui utilise l’objet ne devrait pas pouvoir accéder à ses composants internes et modifier directement ses données ou son comportement. Cela permet au programmeur de modifier et de remanier les composants internes d’un objet sans avoir à changer le code qui l’utilise.

Nous avons vu au chapitre 7 comment contrôler l’encapsulation : nous pouvons utiliser le mot-clé `pub` pour décider quels modules, types, fonctions et méthodes de notre code doivent être publics ; par défaut, tout le reste est privé. Par exemple, nous pouvons définir une structure `AveragedCollection` qui comporte un champ contenant un vecteur de valeurs `i32`. La structure peut également avoir un champ qui contient la moyenne des valeurs du vecteur, ce qui signifie qu’il n’est pas nécessaire de calculer la moyenne à la demande chaque fois que quelqu’un en a besoin. Autrement dit, `AveragedCollection` mettra en cache la moyenne calculée pour nous. La liste 18-1 présente la définition de la structure `AveragedCollection`.

<Listing number="18-1" file-name="src/lib.rs" caption="Une structure `AveragedCollection` qui conserve une liste d’entiers et la moyenne des éléments de la collection">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-01/src/lib.rs}}
```

</Listing>

La structure est marquée `pub` afin que d’autres codes puissent l’utiliser, mais ses champs restent privés. C’est important dans ce cas, car nous voulons garantir que la moyenne est également mise à jour chaque fois qu’une valeur est ajoutée à la liste ou en est retirée. Pour cela, nous implémentons les méthodes `add`, `remove` et `average` sur la structure, comme indiqué dans la liste 18-2.

<Listing number="18-2" file-name="src/lib.rs" caption="Implémentations des méthodes publiques `add`, `remove` et `average` sur `AveragedCollection`">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-02/src/lib.rs:here}}
```

</Listing>

Les méthodes publiques `add`, `remove` et `average` sont les seuls moyens d’accéder aux données d’une instance de `AveragedCollection` ou de les modifier. Lorsqu’un élément est ajouté à `list` à l’aide de la méthode `add` ou supprimé à l’aide de la méthode `remove`, chaque implémentation appelle la méthode privée `update_average`, qui met également à jour le champ `average`.

Nous laissons les champs `list` et `average` privés afin que le code externe ne puisse pas ajouter ou supprimer directement des éléments du champ `list` ; sinon, le champ `average` risquerait de ne plus correspondre au contenu de `list` lorsque celui-ci change. La méthode `average` renvoie la valeur du champ `average`, ce qui permet au code externe de la lire sans pouvoir la modifier.

Comme nous avons encapsulé les détails d’implémentation de la structure `AveragedCollection`, nous pouvons facilement en modifier certains aspects, comme la structure de données, à l’avenir. Nous pourrions, par exemple, utiliser un `HashSet<i32>` au lieu d’un `Vec<i32>` pour le champ `list`. Tant que les signatures des méthodes publiques `add`, `remove` et `average` restent identiques, le code qui utilise `AveragedCollection` n’aura pas besoin de changer. Si nous rendions plutôt `list` public, ce ne serait pas nécessairement le cas : `HashSet<i32>` et `Vec<i32>` n’ont pas les mêmes méthodes pour ajouter et supprimer des éléments, si bien que le code externe devrait probablement changer s’il modifiait directement `list`.

Si l’encapsulation est une caractéristique indispensable pour qu’un langage soit considéré comme orienté objet, alors Rust remplit cette condition. La possibilité d’utiliser ou non `pub` pour différentes parties du code permet d’encapsuler les détails d’implémentation.

### L’héritage comme système de types et comme partage de code

L’_héritage_ est un mécanisme par lequel un objet peut hériter d’éléments de la définition d’un autre objet, obtenant ainsi les données et le comportement de l’objet parent sans que vous ayez à les définir de nouveau.

Si un langage doit prendre en charge l’héritage pour être considéré comme orienté objet, alors Rust n’est pas un tel langage. Il n’existe aucun moyen de définir une structure qui hérite des champs et des implémentations de méthodes de la structure parente sans utiliser une macro.

Cependant, si vous avez l’habitude d’avoir l’héritage dans votre boîte à outils de programmation, vous pouvez utiliser d’autres solutions en Rust, selon la raison pour laquelle vous souhaitez recourir à l’héritage.

Vous choisiriez l’héritage pour deux raisons principales. La première est la réutilisation du code : vous pouvez implémenter un comportement particulier pour un type, et l’héritage vous permet de réutiliser cette implémentation pour un autre type. Le code Rust permet de le faire de façon limitée au moyen d’implémentations par défaut de méthodes de trait, comme vous l’avez vu dans la liste 10-14 lorsque nous avons ajouté une implémentation par défaut de la méthode `summarize` au trait `Summary`. Tout type qui implémente le trait `Summary` dispose de la méthode `summarize` sans qu’aucun code supplémentaire soit nécessaire. C’est comparable à une classe parente qui implémente une méthode et à une classe enfant qui en hérite, disposant ainsi de la même implémentation. Nous pouvons également remplacer l’implémentation par défaut de la méthode `summarize` lorsque nous implémentons le trait `Summary`, ce qui est comparable à une classe enfant qui remplace l’implémentation d’une méthode héritée d’une classe parente.

L’autre raison d’utiliser l’héritage concerne le système de types : il permet d’utiliser un type enfant aux mêmes endroits que le type parent. C’est également ce qu’on appelle le _polymorphisme_, c’est-à-dire la possibilité de substituer plusieurs objets les uns aux autres à l’exécution s’ils partagent certaines caractéristiques.

> ### Polymorphisme
>
> Pour beaucoup de gens, le polymorphisme est synonyme d’héritage. Mais il s’agit en réalité d’un concept plus général, qui désigne du code capable de fonctionner avec des données de plusieurs types. Dans le cas de l’héritage, ces types sont généralement des sous-classes.
>
> Rust utilise plutôt les génériques pour abstraire différents types possibles et les bornes de traits pour imposer des contraintes sur ce que ces types doivent fournir. On parle parfois de _polymorphisme paramétrique borné_.

En n’offrant pas l’héritage, Rust a choisi un ensemble de compromis différent. L’héritage risque souvent d’entraîner un partage de code plus important que nécessaire. Les sous-classes ne devraient pas toujours partager toutes les caractéristiques de leur classe parente, mais l’héritage les y contraint. Cela peut rendre la conception d’un programme moins flexible. L’héritage permet également d’appeler des méthodes sur des sous-classes alors qu’elles n’ont pas de sens ou qu’elles provoquent des erreurs, parce qu’elles ne s’appliquent pas à la sous-classe. En outre, certains langages n’autorisent que l’_héritage simple_ (c’est-à-dire qu’une sous-classe ne peut hériter que d’une seule classe), ce qui limite encore davantage la flexibilité de la conception d’un programme.

Pour ces raisons, Rust adopte une approche différente et utilise des objets de trait plutôt que l’héritage pour obtenir le polymorphisme à l’exécution. Voyons comment fonctionnent les objets de trait.