## Implémenter un patron de conception orienté objet

Le _patron d’état_ est un patron de conception orienté objet. Son principe est de définir un ensemble d’états qu’une valeur peut avoir en interne. Ces états sont représentés par un ensemble d’_objets d’état_, et le comportement de la valeur change en fonction de son état. Nous allons étudier l’exemple d’une structure représentant un article de blog, qui possède un champ contenant son état, lequel sera un objet d’état parmi « brouillon », « en attente de révision » ou « publié ».

Les objets d’état partagent des fonctionnalités : en Rust, bien sûr, nous utilisons des structures et des traits plutôt que des objets et de l’héritage. Chaque objet d’état est responsable de son propre comportement et détermine quand il doit passer à un autre état. La valeur qui contient un objet d’état ne connaît rien des différents comportements des états ni des moments où les transitions doivent avoir lieu.

L’avantage du patron d’état est que, lorsque les exigences métier du programme changent, nous n’avons pas besoin de modifier le code de la valeur qui contient l’état ni celui qui utilise cette valeur. Il suffit de mettre à jour le code à l’intérieur de l’un des objets d’état pour en modifier les règles, ou éventuellement d’ajouter d’autres objets d’état.

Nous allons d’abord implémenter le patron d’état de manière plus traditionnelle, orientée objet. Puis nous utiliserons une approche un peu plus naturelle en Rust. Voyons comment implémenter progressivement un flux de travail pour un article de blog à l’aide du patron d’état.

Le résultat final aura le fonctionnement suivant :

1. Un article de blog commence sous la forme d’un brouillon vide.
1. Lorsque le brouillon est terminé, une révision de l’article est demandée.
1. Lorsque l’article est approuvé, il est publié.
1. Seuls les articles de blog publiés renvoient leur contenu à afficher, afin que les articles non approuvés ne puissent pas être publiés par accident.

Toute autre modification tentée sur un article devrait être sans effet. Par exemple, si nous essayons d’approuver un article de blog à l’état de brouillon avant d’en avoir demandé la révision, l’article doit rester un brouillon non publié.

<!-- Old headings. Do not remove or links may break. -->

<a id="a-traditional-object-oriented-attempt"></a>

### Essayer un style traditionnel orienté objet

Il existe une infinité de façons de structurer du code pour résoudre un même problème, chacune présentant des compromis différents. L’implémentation de cette section adopte un style plutôt traditionnel orienté objet, qu’il est possible d’écrire en Rust, mais qui ne tire pas parti de certains des atouts de Rust. Plus loin, nous présenterons une autre solution qui utilise toujours le patron de conception orienté objet, mais qui est structurée d’une manière qui semblera peut-être moins familière aux personnes ayant une expérience de la programmation orientée objet. Nous comparerons les deux solutions afin d’examiner les compromis liés à la conception de code Rust différemment du code écrit dans d’autres langages.

La liste 18-11 présente ce flux de travail sous forme de code : il s’agit d’un exemple d’utilisation de l’API que nous allons implémenter dans une crate de bibliothèque nommée `blog`. Ce code ne compilera pas encore, car nous n’avons pas implémenté la crate `blog`.

<Listing number="18-11" file-name="src/main.rs" caption="Code illustrant le comportement souhaité de notre crate `blog`">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch18-oop/listing-18-11/src/main.rs:all}}
```

</Listing>

Nous voulons permettre à l’utilisateur de créer un nouvel article de blog à l’état de brouillon avec `Post::new`. Nous voulons pouvoir ajouter du texte à l’article de blog. Si nous essayons d’obtenir immédiatement le contenu de l’article, avant son approbation, nous ne devrions obtenir aucun texte, car l’article est encore à l’état de brouillon. Nous avons ajouté `assert_eq!` dans le code à des fins de démonstration. Un excellent test unitaire consisterait à vérifier qu’un article de blog à l’état de brouillon renvoie une chaîne vide depuis la méthode `content`, mais nous n’allons pas écrire de tests pour cet exemple.

Ensuite, nous voulons permettre de demander la révision de l’article, et nous voulons que `content` renvoie une chaîne vide pendant cette révision. Lorsque l’article est approuvé, il doit être publié, c’est-à-dire que son texte sera renvoyé lors de l’appel à `content`.

Remarquez que le seul type avec lequel nous interagissons dans la crate est le type `Post`. Ce type utilisera le patron d’état et contiendra une valeur qui sera l’un des trois objets d’état représentant les différents états possibles d’un article : brouillon, en attente de révision ou publié. Le type `Post` gérera en interne le passage d’un état à l’autre. Les états changent en réponse aux méthodes appelées par les utilisateurs de notre bibliothèque sur l’instance `Post`, mais ces derniers n’ont pas à gérer directement les changements d’état. De plus, les utilisateurs ne peuvent pas commettre d’erreur concernant les états, par exemple en publiant un article avant qu’il ait été révisé.

<!-- Old headings. Do not remove or links may break. -->

<a id="defining-post-and-creating-a-new-instance-in-the-draft-state"></a>

#### Définir `Post` et créer une nouvelle instance

Commençons l’implémentation de la bibliothèque ! Nous savons qu’il nous faut une structure publique `Post` qui contient du contenu. Nous allons donc commencer par définir cette structure et une fonction publique associée `new` pour créer une instance de `Post`, comme illustré dans la liste 18-12. Nous allons également créer un trait privé `State` qui définira le comportement que tous les objets d’état d’un `Post` doivent avoir.

Ensuite, `Post` contiendra un objet trait `Box<dyn State>` dans un `Option<T>`, dans un champ privé nommé `state`, afin de contenir l’objet d’état. Vous verrez bientôt pourquoi `Option<T>` est nécessaire.

<Listing number="18-12" file-name="src/lib.rs" caption="Définition d’une structure `Post` et d’une fonction `new` qui crée une nouvelle instance de `Post`, d’un trait `State` et d’une structure `Draft`">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-12/src/lib.rs}}
```

</Listing>

Le trait `State` définit le comportement partagé par les différents états d’un article. Les objets d’état sont `Draft`, `PendingReview` et `Published`, et ils implémenteront tous le trait `State`. Pour l’instant, le trait ne contient aucune méthode, et nous allons commencer par définir uniquement l’état `Draft`, car c’est l’état dans lequel nous voulons qu’un article commence.

Lorsque nous créons un nouveau `Post`, nous attribuons à son champ `state` une valeur `Some` contenant une `Box`. Cette `Box` pointe vers une nouvelle instance de la structure `Draft`. Ainsi, chaque fois que nous créons une nouvelle instance de `Post`, elle commence à l’état de brouillon. Comme le champ `state` de `Post` est privé, il est impossible de créer un `Post` dans un autre état ! Dans la fonction `Post::new`, nous définissons le champ `content` sur une nouvelle `String` vide.

#### Stocker le texte du contenu de l’article

Nous avons vu dans la liste 18-11 que nous voulons pouvoir appeler une méthode nommée `add_text` et lui transmettre un `&str`, qui sera ensuite ajouté au contenu textuel de l’article de blog. Nous implémentons cela sous forme de méthode, plutôt que d’exposer le champ `content` en tant que `pub`, afin de pouvoir ultérieurement implémenter une méthode qui contrôlera la lecture des données du champ `content`. La méthode `add_text` est assez simple ; ajoutons donc son implémentation au bloc `impl Post` dans la liste 18-13.

<Listing number="18-13" file-name="src/lib.rs" caption="Implémentation de la méthode `add_text` pour ajouter du texte au champ `content` d’un article">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-13/src/lib.rs:here}}
```

</Listing>

La méthode `add_text` prend une référence mutable à `self`, car nous modifions l’instance de `Post` sur laquelle nous l’appelons. Nous appelons ensuite `push_str` sur la `String` de `content` et lui transmettons l’argument `text` à ajouter au contenu enregistré. Ce comportement ne dépend pas de l’état de l’article : il ne fait donc pas partie du patron d’état. La méthode `add_text` n’interagit pas du tout avec le champ `state`, mais elle fait partie du comportement que nous voulons prendre en charge.

<!-- Old headings. Do not remove or links may break. -->

<a id="ensuring-the-content-of-a-draft-post-is-empty"></a>

#### Garantir que le contenu d’un article à l’état de brouillon est vide

Même après avoir appelé `add_text` et ajouté du contenu à notre article, nous voulons que la méthode `content` renvoie une tranche de chaîne vide, car l’article est toujours à l’état de brouillon, comme le montre le premier `assert_eq!` de la liste 18-11. Pour l’instant, implémentons la méthode `content` de la manière la plus simple qui réponde à cette exigence : elle renverra toujours une tranche de chaîne vide. Nous modifierons cela plus tard, lorsque nous implémenterons la possibilité de changer l’état d’un article afin de pouvoir le publier. Jusqu’ici, les articles ne peuvent être qu’à l’état de brouillon ; leur contenu doit donc toujours être vide. La liste 18-14 présente cette implémentation provisoire.

<Listing number="18-14" file-name="src/lib.rs" caption="Ajout d’une implémentation provisoire de la méthode `content` sur `Post`, qui renvoie toujours une tranche de chaîne vide">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-14/src/lib.rs:here}}
```

</Listing>

Avec cette méthode `content`, tout fonctionne comme prévu dans la liste 18-11 jusqu’au premier `assert_eq!` inclus.

<!-- Old headings. Do not remove or links may break. -->

<a id="requesting-a-review-of-the-post-changes-its-state"></a>
<a id="requesting-a-review-changes-the-posts-state"></a>

#### Demander une révision, ce qui change l’état de l’article

Ensuite, nous devons ajouter la fonctionnalité permettant de demander la révision d’un article, ce qui doit faire passer son état de `Draft` à `PendingReview`. La liste 18-15 présente ce code.

<Listing number="18-15" file-name="src/lib.rs" caption="Implémentation des méthodes `request_review` sur `Post` et sur le trait `State`">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-15/src/lib.rs:here}}
```

</Listing>

Nous ajoutons à `Post` une méthode publique nommée `request_review`, qui prend une référence mutable à `self`. Nous appelons ensuite une méthode interne `request_review` sur l’état actuel de `Post`. Cette seconde méthode `request_review` consomme l’état actuel et renvoie un nouvel état.

Nous ajoutons la méthode `request_review` au trait `State` ; tous les types qui implémentent ce trait devront désormais implémenter cette méthode. Remarquez qu’au lieu d’utiliser `self`, `&self` ou `&mut self` comme premier paramètre de la méthode, nous utilisons `self: Box<Self>`. Cette syntaxe signifie que la méthode ne peut être appelée que sur une `Box` contenant le type. Elle prend possession de `Box<Self>`, invalidant l’ancien état afin que la valeur d’état de `Post` puisse être transformée en un nouvel état.

Pour consommer l’ancien état, la méthode `request_review` doit prendre possession de la valeur d’état. C’est là qu’intervient le `Option` du champ `state` de `Post` : nous appelons la méthode `take` pour extraire la valeur `Some` du champ `state` et la remplacer par `None`, car Rust ne nous permet pas d’avoir des champs non initialisés dans les structures. Cela nous permet de déplacer la valeur `state` hors de `Post` plutôt que de l’emprunter. Nous attribuerons ensuite au champ `state` de l’article le résultat de cette opération.

Nous devons temporairement définir `state` sur `None`, plutôt que de lui attribuer directement une valeur avec du code comme `self.state = self.state.request_review();`, afin de prendre possession de la valeur `state`. Cela garantit que `Post` ne peut pas utiliser l’ancienne valeur `state` après l’avoir transformée en un nouvel état.

La méthode `request_review` sur `Draft` renvoie une nouvelle instance encadrée dans une `Box` de la structure `PendingReview`, qui représente l’état d’un article en attente de révision. La structure `PendingReview` implémente également la méthode `request_review`, mais celle-ci ne transforme rien. Elle renvoie plutôt l’objet lui-même, car lorsqu’on demande la révision d’un article déjà à l’état `PendingReview`, celui-ci doit y rester.

Nous commençons maintenant à voir les avantages du patron d’état : la méthode `request_review` sur `Post` est la même quelle que soit la valeur de son état `state`. Chaque état est responsable de ses propres règles.

Nous allons laisser la méthode `content` sur `Post` telle quelle, c’est-à-dire qu’elle renverra une tranche de chaîne vide. Nous pouvons désormais avoir un `Post` à l’état `PendingReview` aussi bien qu’à l’état `Draft`, mais nous voulons que le comportement reste le même à l’état `PendingReview`. La liste 18-11 fonctionne maintenant jusqu’au deuxième appel à `assert_eq!` !

<!-- Old headings. Do not remove or links may break. -->

<a id="adding-the-approve-method-that-changes-the-behavior-of-content"></a>
<a id="adding-approve-to-change-the-behavior-of-content"></a>

#### Ajouter `approve` pour modifier le comportement de `content`

La méthode `approve` sera similaire à la méthode `request_review` : elle définira `state` sur la valeur que l’état actuel indique qu’il doit prendre lorsqu’il est approuvé, comme le montre la liste 18-16.

<Listing number="18-16" file-name="src/lib.rs" caption="Implémentation de la méthode `approve` sur `Post` et sur le trait `State`">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-16/src/lib.rs:here}}
```

</Listing>

Nous ajoutons la méthode `approve` au trait `State` et une nouvelle structure qui implémente `State` : l’état `Published`.

Comme pour le fonctionnement de `request_review` sur `PendingReview`, si nous appelons la méthode `approve` sur un `Draft`, elle n’aura aucun effet, car `approve` renverra `self`. Lorsque nous appelons `approve` sur `PendingReview`, la méthode renvoie une nouvelle instance de la structure `Published` encadrée dans une `Box`. La structure `Published` implémente le trait `State` et renvoie l’objet lui-même pour les méthodes `request_review` et `approve`, car l’article doit rester à l’état `Published` dans ces cas.

Nous devons maintenant mettre à jour la méthode `content` sur `Post`. Nous voulons que la valeur renvoyée par `content` dépende de l’état actuel de `Post`. Nous allons donc déléguer à une méthode `content` définie sur son état, comme le montre la liste 18-17.

<Listing number="18-17" file-name="src/lib.rs" caption="Mise à jour de la méthode `content` sur `Post` pour déléguer à une méthode `content` sur `State`">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch18-oop/listing-18-17/src/lib.rs:here}}
```

</Listing>

Comme l’objectif est de conserver toutes ces règles à l’intérieur des structures qui implémentent `State`, nous appelons une méthode `content` sur la valeur contenue dans `state` et lui transmettons l’instance de l’article (c’est-à-dire `self`) comme argument. Nous renvoyons ensuite la valeur obtenue en utilisant la méthode `content` sur la valeur `state`.

Nous appelons la méthode `as_ref` sur `Option`, car nous voulons une référence à la valeur contenue dans `Option`, plutôt que de prendre possession de cette valeur. Comme `state` est un `Option<Box<dyn State>>`, l’appel à `as_ref` renvoie un `Option<&Box<dyn State>>`. Sans cet appel à `as_ref`, nous obtiendrions une erreur, car nous ne pouvons pas déplacer `state` hors du `&self` emprunté du paramètre de la fonction.

Nous appelons ensuite la méthode `unwrap`, qui ne pourra jamais provoquer de panique, car nous savons que les méthodes sur `Post` garantissent que `state` contiendra toujours une valeur `Some` une fois leur exécution terminée. C’est l’un des cas évoqués dans la section [« Quand vous en savez plus que le compilateur »][more-info-than-rustc]<!-- ignore --> du chapitre 9 : nous savons qu’une valeur `None` est impossible, même si le compilateur n’est pas en mesure de le comprendre.

À ce stade, lorsque nous appelons `content` sur le `&Box<dyn State>`, la coercition de déréférencement s’applique au `&` et à la `Box`, de sorte que la méthode `content` est finalement appelée sur le type qui implémente le trait `State`. Cela signifie que nous devons ajouter `content` à la définition du trait `State`, et c’est là que nous placerons la logique déterminant le contenu à renvoyer en fonction de l’état, comme le montre la liste 18-18.

<Listing number="18-18" file-name="src/lib.rs" caption="Ajout de la méthode `content` au trait `State`">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-18/src/lib.rs:here}}
```

</Listing>

Nous ajoutons une implémentation par défaut de la méthode `content` qui renvoie une tranche de chaîne vide. Cela signifie que nous n’avons pas besoin d’implémenter `content` sur les structures `Draft` et `PendingReview`. La structure `Published` remplacera l’implémentation de `content` et renverra la valeur de `post.content`. C’est pratique, mais confier à la méthode `content` de `State` la détermination du contenu de `Post` brouille la distinction entre les responsabilités de `State` et celles de `Post`.

Remarquez que nous avons besoin d’annotations de durée de vie pour cette méthode, comme nous l’avons vu au chapitre 10. Nous prenons une référence à un `post` comme argument et renvoyons une référence à une partie de ce `post` ; la durée de vie de la référence renvoyée est donc liée à celle de l’argument `post`.

Et voilà : toute la liste 18-11 fonctionne maintenant ! Nous avons implémenté le patron d’état en respectant les règles du flux de travail d’un article de blog. La logique relative à ces règles se trouve dans les objets d’état plutôt que d’être dispersée dans `Post`.

> ### Pourquoi ne pas utiliser une énumération ?
>
> Vous vous êtes peut-être demandé pourquoi nous n’avons pas utilisé une énumération dont les variantes représenteraient les différents états possibles d’un article. C’est tout à fait une solution possible ; essayez-la et comparez les résultats pour voir laquelle vous préférez ! L’inconvénient des énumérations est que chaque endroit où l’on vérifie la valeur de l’énumération doit utiliser une expression `match`, ou un mécanisme similaire, pour gérer toutes les variantes possibles. Cette solution pourrait être plus répétitive que celle utilisant un objet trait.

<!-- Old headings. Do not remove or links may break. -->

<a id="trade-offs-of-the-state-pattern"></a>

#### Évaluer le patron d’état

Nous avons montré que Rust est capable d’implémenter le patron d’état orienté objet pour encapsuler les différents comportements qu’un article doit adopter dans chaque état. Les méthodes sur `Post` ne connaissent rien des divers comportements. Grâce à l’organisation du code, il suffit de consulter un seul endroit pour connaître les différents comportements possibles d’un article publié : l’implémentation du trait `State` sur la structure `Published`.

Si nous créions une autre implémentation sans utiliser le patron d’état, nous pourrions utiliser des expressions `match` dans les méthodes sur `Post`, voire dans le code de `main`, pour vérifier l’état de l’article et modifier son comportement à ces endroits. Nous devrions alors consulter plusieurs endroits pour comprendre toutes les implications de l’état publié d’un article.

Avec le patron d’état, les méthodes sur `Post` et les endroits où nous utilisons `Post` n’ont pas besoin d’expressions `match`. Pour ajouter un nouvel état, il suffirait d’ajouter une nouvelle structure et d’implémenter les méthodes du trait sur cette structure, à un seul endroit.

L’implémentation qui utilise le patron d’état peut facilement être étendue pour ajouter des fonctionnalités. Pour constater à quel point il est facile de maintenir du code qui utilise le patron d’état, essayez quelques-unes des suggestions suivantes :

- Ajoutez une méthode `reject` qui fait repasser l’article de l’état `PendingReview` à l’état `Draft`.
- Exigez deux appels à `approve` avant que l’état puisse passer à `Published`.
- Autorisez les utilisateurs à ajouter du texte au contenu uniquement lorsque l’article est à l’état `Draft`. Indice : confiez à l’objet d’état la responsabilité de déterminer ce qui peut changer dans le contenu, mais pas celle de modifier `Post`.

L’un des inconvénients du patron d’état est que, comme les états implémentent les transitions entre eux, certains états sont couplés les uns aux autres. Si nous ajoutons un état entre `PendingReview` et `Published`, par exemple `Scheduled`, nous devrons modifier le code de `PendingReview` pour que la transition mène à `Scheduled`. Il y aurait moins de travail si l’ajout d’un nouvel état ne nécessitait pas de modifier `PendingReview`, mais cela impliquerait de passer à un autre patron de conception.

Un autre inconvénient est que nous avons dupliqué une partie de la logique. Pour éliminer une partie de cette duplication, nous pourrions essayer de définir des implémentations par défaut des méthodes `request_review` et `approve` sur le trait `State` qui renvoient `self`. Cependant, cela ne fonctionnerait pas : lorsque `State` est utilisé comme objet trait, le trait ne connaît pas précisément le type concret de `self`, et le type de retour n’est donc pas connu à la compilation. (C’est l’une des règles de compatibilité avec `dyn` évoquées précédemment.)

Il y a également une duplication entre les implémentations des méthodes `request_review` et `approve` sur `Post`, qui se ressemblent. Les deux méthodes utilisent `Option::take` avec le champ `state` de `Post` et, si `state` vaut `Some`, délèguent à la méthode du même nom implémentée par la valeur qu’elle contient, puis définissent la nouvelle valeur du champ `state` avec le résultat. Si nous avions beaucoup de méthodes sur `Post` suivant ce schéma, nous pourrions envisager de définir une macro pour éviter cette répétition (voir la section [« Macros »][macros]<!-- ignore --> du chapitre 20).

En implémentant le patron d’état exactement tel qu’il est défini pour les langages orientés objet, nous ne tirons pas pleinement parti des atouts de Rust. Voyons quelques modifications que nous pouvons apporter à la crate `blog` pour que les états et les transitions invalides deviennent des erreurs de compilation.

### Encoder les états et le comportement dans les types

Nous allons vous montrer comment repenser le patron d’état pour obtenir un ensemble différent de compromis. Au lieu d’encapsuler complètement les états et les transitions de sorte que le code externe n’en ait aucune connaissance, nous allons encoder les états dans différents types. Le système de vérification des types de Rust empêchera donc les tentatives d’utiliser des articles à l’état de brouillon là où seuls les articles publiés sont autorisés, en émettant une erreur de compilation.

Examinons la première partie de `main` dans la liste 18-11 :

<Listing file-name="src/main.rs">

```rust,ignore
{{#rustdoc_include ../listings/ch18-oop/listing-18-11/src/main.rs:here}}
```

</Listing>

Nous permettons toujours de créer de nouveaux articles à l’état de brouillon avec `Post::new` et d’ajouter du texte à leur contenu. Mais au lieu d’avoir une méthode `content` sur un article à l’état de brouillon qui renvoie une chaîne vide, nous allons faire en sorte que les articles à l’état de brouillon n’aient pas du tout de méthode `content`. Ainsi, si nous essayons d’obtenir le contenu d’un article à l’état de brouillon, nous obtiendrons une erreur de compilation indiquant que cette méthode n’existe pas. Il nous sera donc impossible d’afficher accidentellement le contenu d’un article à l’état de brouillon en production, car ce code ne compilera même pas. La liste 18-19 présente la définition des structures `Post` et `DraftPost`, ainsi que les méthodes associées.

<Listing number="18-19" file-name="src/lib.rs" caption="Un `Post` doté d’une méthode `content` et un `DraftPost` sans méthode `content`">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-19/src/lib.rs}}
```

</Listing>

Les structures `Post` et `DraftPost` possèdent toutes deux un champ privé `content` qui stocke le texte de l’article de blog. Les structures n’ont plus de champ `state`, car nous encodons désormais l’état dans les types des structures. La structure `Post` représentera un article publié et possédera une méthode `content` qui renvoie le contenu.

Nous avons toujours une fonction `Post::new`, mais au lieu de renvoyer une instance de `Post`, elle renvoie une instance de `DraftPost`. Comme `content` est privé et qu’aucune fonction ne renvoie de `Post`, il est actuellement impossible de créer une instance de `Post`.

La structure `DraftPost` possède une méthode `add_text`, qui nous permet d’ajouter du texte à `content` comme avant. Remarquez cependant que `DraftPost` ne possède pas de méthode `content` ! Le programme garantit désormais que tous les articles commencent à l’état de brouillon et que leur contenu n’est pas accessible pour affichage tant qu’ils sont dans cet état. Toute tentative de contourner ces contraintes entraînera une erreur de compilation.

<!-- Old headings. Do not remove or links may break. -->

<a id="implementing-transitions-as-transformations-into-different-types"></a>

Comment obtenir un article publié ? Nous voulons imposer la règle selon laquelle un article à l’état de brouillon doit être révisé et approuvé avant de pouvoir être publié. Un article en attente de révision ne doit toujours pas afficher son contenu. Implémentons ces contraintes en ajoutant une autre structure, `PendingReviewPost`, en définissant la méthode `request_review` sur `DraftPost` afin qu’elle renvoie un `PendingReviewPost`, et en définissant une méthode `approve` sur `PendingReviewPost` afin qu’elle renvoie un `Post`, comme le montre la liste 18-20.

<Listing number="18-20" file-name="src/lib.rs" caption="Un `PendingReviewPost` créé en appelant `request_review` sur `DraftPost`, et une méthode `approve` qui transforme un `PendingReviewPost` en `Post` publié">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-20/src/lib.rs:here}}
```

</Listing>

Les méthodes `request_review` et `approve` prennent possession de `self` et consomment donc les instances de `DraftPost` et de `PendingReviewPost` pour les transformer respectivement en `PendingReviewPost` et en `Post` publié. Ainsi, après avoir appelé `request_review` sur une instance de `DraftPost`, il ne nous en restera aucune, et ainsi de suite. La structure `PendingReviewPost` ne possède pas de méthode `content` ; toute tentative de lire son contenu entraînera donc une erreur de compilation, comme avec `DraftPost`. Comme le seul moyen d’obtenir une instance de `Post` publié dotée d’une méthode `content` est d’appeler la méthode `approve` sur un `PendingReviewPost`, et que le seul moyen d’obtenir un `PendingReviewPost` est d’appeler la méthode `request_review` sur un `DraftPost`, nous avons désormais encodé le flux de travail des articles de blog dans le système de types.

Nous devons toutefois apporter quelques petites modifications à `main`. Les méthodes `request_review` et `approve` renvoient de nouvelles instances au lieu de modifier la structure sur laquelle elles sont appelées. Nous devons donc ajouter des affectations avec masquage de variable, sous la forme `let post =`, pour enregistrer les instances renvoyées. Nous ne pouvons pas non plus conserver les assertions selon lesquelles le contenu des articles à l’état de brouillon ou en attente de révision est une chaîne vide, et nous n’en avons pas besoin : le code qui essaie d’utiliser le contenu d’articles dans ces états ne peut plus compiler. Le code mis à jour dans `main` est présenté dans la liste 18-21.

<Listing number="18-21" file-name="src/main.rs" caption="Modifications de `main` pour utiliser la nouvelle implémentation du flux de travail des articles de blog">

```rust,ignore
{{#rustdoc_include ../listings/ch18-oop/listing-18-21/src/main.rs}}
```

</Listing>

Les modifications apportées à `main` pour réaffecter `post` signifient que cette implémentation ne suit plus tout à fait le patron d’état orienté objet : les transformations entre les états ne sont plus entièrement encapsulées dans l’implémentation de `Post`. En revanche, grâce au système de types et à la vérification des types effectuée à la compilation, les états invalides sont désormais impossibles ! Ainsi, certains bogues, comme l’affichage du contenu d’un article non publié, seront détectés avant la mise en production.

Essayez les tâches proposées au début de cette section sur la crate `blog` telle qu’elle se présente après la liste 18-21, pour voir ce que vous pensez de la conception de cette version du code. Certaines tâches sont peut-être déjà réalisées dans cette conception.

Nous avons vu que, même si Rust est capable d’implémenter des patrons de conception orientés objet, d’autres patrons, comme l’encodage de l’état dans le système de types, sont également disponibles en Rust. Ces patrons présentent différents compromis. Même si les patrons orientés objet vous sont très familiers, repenser le problème pour tirer parti des fonctionnalités de Rust peut présenter des avantages, notamment celui d’éviter certains bogues à la compilation. Les patrons orientés objet ne seront pas toujours la meilleure solution en Rust, en raison de certaines fonctionnalités comme la propriété, absentes des langages orientés objet.

## Résumé

Que vous considériez ou non Rust comme un langage orienté objet après avoir lu ce chapitre, vous savez maintenant que vous pouvez utiliser des objets trait pour bénéficier de certaines fonctionnalités orientées objet en Rust. La répartition dynamique peut apporter de la souplesse à votre code, au prix d’une légère baisse des performances à l’exécution. Vous pouvez utiliser cette souplesse pour implémenter des patrons orientés objet qui favorisent la maintenabilité de votre code. Rust possède également d’autres fonctionnalités, comme la propriété, absentes des langages orientés objet. Un patron orienté objet ne sera pas toujours la meilleure façon de tirer parti des atouts de Rust, mais il reste une option possible.

Nous allons maintenant examiner les motifs, une autre fonctionnalité de Rust qui permet une grande souplesse. Nous les avons brièvement abordés tout au long du livre, mais nous n’avons pas encore vu tout ce qu’ils permettent. Allons-y !

[more-info-than-rustc]: ch09-03-to-panic-or-not-to-panic.html#cases-in-which-you-have-more-information-than-the-compiler
[macros]: ch20-05-macros.html#macros