## Implémentation d'un Modèle de Conception Orientée Objet

Le _modèle d'état_ est un modèle de conception orientée objet. Le principe de ce modèle est que nous définissons un ensemble d'états qu'une valeur peut avoir en interne. Les états sont représentés par un ensemble d'__objets d'état__, et le comportement de la valeur change en fonction de son état. Nous allons travailler sur un exemple d'une structure de publication de blog qui a un champ pour contenir son état, qui sera un objet d'état du groupe "brouillon", "révision" ou "publié".

Les objets d'état partagent une fonctionnalité : en Rust, bien sûr, nous utilisons des structures et des traits plutôt que des objets et de l'héritage. Chaque objet d'état est responsable de son propre comportement et de la détermination des moments où il doit changer en un autre état. La valeur qui détient un objet d'état ne connaît rien des différents comportements des états ou des moments où elle doit passer d'un état à un autre.

L'avantage d'utiliser le modèle d'état est que lorsque les exigences métier du programme changent, nous n'aurons pas besoin de modifier le code de la valeur tenant l'état ni le code qui utilise cette valeur. Nous n'aurons qu'à mettre à jour le code à l'intérieur d'un des objets d'état pour changer ses règles ou peut-être ajouter davantage d'objets d'état.

Tout d'abord, nous allons implémenter le modèle d'état de manière plus traditionnelle orientée objet. Ensuite, nous utiliserons une approche qui est un peu plus naturelle en Rust. Plongeons-nous pour implémenter de manière progressive un flux de travail de publication de blog en utilisant le modèle d'état.

La fonctionnalité finale ressemblera à ceci :

1. Une publication de blog commence comme un brouillon vide.
2. Lorsque le brouillon est terminé, une révision de la publication est demandée.
3. Lorsque la publication est approuvée, elle est publiée.
4. Seules les publications de blog publiées renvoient du contenu à imprimer, de sorte que les publications non approuvées ne puissent pas être publiées accidentellement.

Toute autre modification tentée sur une publication ne devrait avoir aucun effet. Par exemple, si nous essayons d'approuver une publication de blog en brouillon avant d'avoir demandé une révision, la publication devrait rester un brouillon non publié.

### Tentative de Style Orienté Objet Traditionnel

Il existe une infinité de manières de structurer le code pour résoudre le même problème, chacune avec des compromis différents. L'implémentation de cette section est plus dans un style orienté objet traditionnel, qui est possible à écrire en Rust, mais ne tire pas parti de certaines forces de Rust. Plus tard, nous démontrerons une solution différente qui utilise toujours le modèle de conception orientée objet mais qui est structurée d'une manière qui pourrait sembler moins familière aux programmeurs ayant de l'expérience orientée objet. Nous comparerons les deux solutions pour expérimenter les compromis de la conception du code Rust différemment de celui dans d'autres langages.

L'énumération 18-11 montre ce flux de travail sous forme de code : C'est un exemple d'utilisation de l'API que nous allons implémenter dans une bibliothèque nommée `blog`. Cela ne compilera pas encore car nous n'avons pas implémenté le crate `blog`.

Nous voulons permettre à l'utilisateur de créer une nouvelle publication de blog en brouillon avec `Post::new`. Nous voulons permettre d'ajouter du texte à la publication. Si nous essayons d'obtenir le contenu de la publication immédiatement, avant approbation, nous ne devrions obtenir aucun texte car la publication est toujours un brouillon. Nous avons ajouté `assert_eq!` dans le code à des fins de démonstration. Un excellent test unitaire pour cela serait d'affirmer qu'une publication de blog en brouillon renvoie une chaîne vide depuis la méthode `content`, mais nous n'allons pas écrire de tests pour cet exemple.

Ensuite, nous voulons activer une demande de révision de la publication, et nous voulons que `content` renvoie une chaîne vide pendant l'attente de la révision. Lorsque la publication reçoit l'approbation, elle doit être publiée, ce qui signifie que le texte de la publication sera retourné lorsque `content` sera appelé.

Notez que le seul type avec lequel nous interagissons depuis le crate est le type `Post`. Ce type utilisera le modèle d'état et contiendra une valeur qui sera un des trois objets d'état représentant les divers états dans lesquels une publication peut être : brouillon, révision ou publiée. Changer d'un état à un autre sera géré en interne au sein du type `Post`. Les états changent en réponse aux méthodes appelées par les utilisateurs de notre bibliothèque sur l'instance `Post`, mais ils n'ont pas à gérer directement les changements d'état. De plus, les utilisateurs ne peuvent pas se tromper avec les états, comme publier une publication avant qu'elle ait été révisée.

### Définition de `Post` et Création d'une Nouvelle Instance

Commençons l'implémentation de la bibliothèque ! Nous savons que nous avons besoin d'une structure `Post` publique qui contienne du contenu, nous commencerons donc par la définition de la structure et une fonction publique `new` associée pour créer une instance de `Post`. Nous allons également créer un trait privé `State` qui définira le comportement que tous les objets d'état pour un `Post` doivent avoir.

Ensuite, `Post` contiendra un objet trait de `Box<dyn State>` à l'intérieur d'un `Option<T>` dans un champ privé nommé `state` pour contenir l'objet d'état. Vous verrez pourquoi l'`Option<T>` est nécessaire dans un instant.

Le trait `State` définit le comportement partagé par différents états de publication. Les objets d'état sont `Draft`, `PendingReview` et `Published`, et tous implémenteront le trait `State`. Pour l'instant, le trait n'a pas de méthodes, et nous allons commencer par définir juste l'état `Draft` car c'est l'état dans lequel nous voulons qu'une publication commence.

Lorsque nous créons un nouveau `Post`, nous définissons son champ `state` sur une valeur `Some` qui contient une `Box` pointant vers une nouvelle instance de la structure `Draft`. Cela garantit que chaque fois que nous créons une nouvelle instance de `Post`, elle commencera par un brouillon. Étant donné que le champ `state` de `Post` est privé, il n'est pas possible de créer un `Post` dans un autre état ! Dans la fonction `Post::new`, nous initialisons le champ `content` à une nouvelle `String` vide.

#### Stockage du Texte du Contenu du Post

Nous avons vu dans l'énumération 18-11 que nous voulons pouvoir appeler une méthode nommée `add_text` et y passer un `&str` qui sera ensuite ajouté en tant que texte de contenu de la publication de blog. Nous implémentons cela comme une méthode, plutôt que d'exposer le champ `content` en tant que `pub`, afin que plus tard nous puissions implémenter une méthode qui contrôlera comment les données du champ `content` sont lues. La méthode `add_text` est assez simple, ajoutons donc l'implémentation dans l'énumération 18-13 au bloc `impl Post`.

La méthode `add_text` prend une référence mutable sur `self` car nous modifions l'instance de `Post` sur laquelle nous appelons `add_text`. Nous appelons ensuite `push_str` sur la `String` dans `content` et passons l'argument `text` à ajouter au `content` sauvegardé. Ce comportement ne dépend pas de l'état dans lequel se trouve la publication, il ne fait donc pas partie du modèle d'état. La méthode `add_text` n'interagit pas du tout avec le champ `state`, mais elle fait partie du comportement que nous voulons prendre en charge.

#### Garantie Que le Contenu d'une Publication de Brouillon Est Vide

Même après avoir appelé `add_text` et ajouté du contenu à notre publication, nous voulons que la méthode `content` renvoie toujours une tranche de chaîne vide car la publication est encore dans l'état de brouillon, comme le montre le premier `assert_eq!` dans l'énumération 18-11. Pour l'instant, implémentons la méthode `content` avec la chose la plus simple qui remplira cette exigence : renvoyer toujours une tranche de chaîne vide. Nous changerons cela plus tard une fois que nous aurons implémenté la possibilité de changer l'état d'une publication afin qu'elle puisse être publiée. Jusqu'à présent, les publications ne peuvent être que dans l'état de brouillon, donc le contenu de la publication doit toujours être vide. L'énumération 18-14 montre cette implémentation de substitution.

Avec cette méthode `content` ajoutée, tout dans l'énumération 18-11 jusqu'au premier `assert_eq!` fonctionne comme prévu.

#### Demande d'une Révision, Ce Qui Change l'État de la Publication

Ensuite, nous devons ajouter une fonctionnalité pour demander une révision d'une publication, ce qui devrait changer son état de `Draft` à `PendingReview`. L'énumération 18-15 montre ce code.

Nous donnons à `Post` une méthode publique nommée `request_review` qui prendra une référence mutable sur `self`. Ensuite, nous appelons une méthode interne `request_review` sur l'état actuel de `Post`, et cette seconde méthode `request_review` consomme l'état actuel et renvoie un nouvel état.

Nous ajoutons la méthode `request_review` au trait `State` ; tous les types qui implémentent le trait devront maintenant implémenter la méthode `request_review`. Notez que plutôt que d'avoir `self`, `&self` ou `&mut self` comme premier paramètre de la méthode, nous avons `self: Box<Self>`. Cette syntaxe signifie que la méthode n'est valide que lorsqu'elle est appelée sur une `Box` détenant le type. Cette syntaxe prend possession de `Box<Self>`, invalidant l'ancien état afin que la valeur d'état de `Post` puisse se transformer en un nouvel état.

Pour consommer l'ancien état, la méthode `request_review` doit prendre possession de la valeur d'état. C'est ici que l'`Option` dans le champ `state` de `Post` entre en jeu : nous appelons la méthode `take` pour retirer la valeur `Some` du champ `state` et laisser un `None` à sa place, car Rust ne nous permet pas d'avoir des champs non peuplés dans les structures. Cela nous permet de déplacer la valeur `state` hors de `Post` plutôt que de l'emprunter. Ensuite, nous allons définir la valeur de `state` de la publication sur le résultat de cette opération.

Nous devons temporairement définir `state` sur `None` plutôt que de le définir directement avec du code comme `self.state = self.state.request_review();` pour obtenir la possession de la valeur `state`. Cela garantit que `Post` ne peut pas utiliser la valeur `state` ancienne après que nous l'ayons transformée en un nouvel état.

La méthode `request_review` sur `Draft` renvoie une nouvelle instance, empaquetée, d'une nouvelle structure `PendingReview`, qui représente l'état lorsqu'une publication est en attente de révision. La structure `PendingReview` implémente également la méthode `request_review`, mais ne fait aucune transformation. Au contraire, elle se renvoie elle-même car lorsqu'on demande une révision sur une publication déjà dans l'état `PendingReview`, elle doit rester dans l'état `PendingReview`.

Nous pouvons maintenant commencer à voir les avantages du modèle d'état : La méthode `request_review` sur `Post` est la même peu importe sa valeur `state`. Chaque état est responsable de ses propres règles.

Nous laisserons la méthode `content` sur `Post` telle quelle, revenant à une tranche de chaîne vide. Nous pouvons maintenant avoir une `Post` dans l'état `PendingReview` ainsi que dans l'état `Draft`, mais nous voulons le même comportement dans l'état `PendingReview`. L'énumération 18-11 fonctionne maintenant jusqu'au deuxième appel `assert_eq!` !

#### Ajout de `approve` pour Changer le Comportement de `content`

La méthode `approve` sera similaire à la méthode `request_review` : elle définira `state` à la valeur que l'état actuel indique qu'il devrait avoir lorsque cet état est approuvé, comme illustré dans l'énumération 18-16.

Nous ajoutons la méthode `approve` au trait `State` et ajoutons une nouvelle structure qui implémente `State`, l'état `Published`.

De manière similaire à la façon dont la méthode `request_review` fonctionne sur `PendingReview`, si nous appelons la méthode `approve` sur un `Draft`, cela n'aura aucun effet car `approve` renverra `self`. Lorsque nous appelons `approve` sur `PendingReview`, elle renvoie une nouvelle instance, empaquetée, de la structure `Published`. La structure `Published` implémente le trait `State`, et pour les méthodes `request_review` et `approve`, elle renvoie elle-même car la publication doit rester dans l'état `Published` dans ces cas.

Maintenant, nous devons mettre à jour la méthode `content` sur `Post`. Nous voulons que la valeur renvoyée par `content` dépende de l'état actuel du `Post`, nous allons donc faire en sorte que le `Post` délègue à une méthode `content` définie sur son `state`, comme montré dans l'énumération 18-17.

Parce que l'objectif est de garder toutes ces règles à l'intérieur des structures qui implémentent `State`, nous appelons une méthode `content` sur la valeur dans `state` et passons l'instance de publication (c'est-à-dire `self`) comme argument. Ensuite, nous retournons la valeur renvoyée par l'utilisation de la méthode `content` sur la valeur `state`.

Nous appelons la méthode `as_ref` sur l'`Option` car nous voulons une référence à la valeur à l'intérieur de l'`Option` plutôt qu'à la possession de la valeur. Étant donné que `state` est un `Option<Box<dyn State>>`, lorsque nous appelons `as_ref`, un `Option<&Box<dyn State>>` est renvoyé. Si nous n'appelions pas `as_ref`, nous obtiendrions une erreur car nous ne pouvons pas déplacer `state` hors du `&self` emprunté du paramètre de fonction.

Nous appelons ensuite la méthode `unwrap`, que nous savons ne panique jamais car nous savons que les méthodes sur `Post` garantissent que `state` contiendra toujours une valeur `Some` lorsque ces méthodes sont terminées. C'est l'un des cas dont nous avons parlé dans la section [« Lorsque vous avez plus d'informations que le compilateur »](ch09-03-to-panic-or-not-to-panic.html#cases-in-which-you-have-more-information-than-the-compiler) du chapitre 9 lorsque nous savons qu'une valeur `None` n'est jamais possible, même si le compilateur n'est pas en mesure de comprendre cela.

À ce stade, lorsque nous appelons `content` sur le `&Box<dyn State>`, la coercition deref prendra effet sur le `&` et le `Box` de sorte que la méthode `content` sera finalement appelée sur le type qui implémente le trait `State`. Cela signifie que nous devons ajouter `content` à la définition du trait `State`, et c'est là que nous allons mettre la logique pour quel contenu retourner selon quel état nous avons, comme montré dans l'énumération 18-18.

Nous ajoutons une implémentation par défaut pour la méthode `content` qui renvoie une tranche de chaîne vide. Cela signifie que nous n'avons pas besoin d'implémenter `content` sur les structures `Draft` et `PendingReview`. La structure `Published` remplacera la méthode `content` et renverra la valeur dans `post.content`. Bien que pratique, avoir la méthode `content` sur `State` déterminant le contenu du `Post` brouille les frontières entre la responsabilité de `State` et celle de `Post`.

Notez que nous avons besoin d'annotations de durée de vie sur cette méthode, comme nous en avons discuté dans le chapitre 10. Nous prenons une référence à un `post` comme argument et retournons une référence à une partie de ce `post`, donc la durée de vie de la référence retour est liée à la durée de vie de l'argument `post`.

Et nous avons terminé : tout dans l'énumération 18-11 fonctionne maintenant ! Nous avons implémenté le modèle d'état avec les règles du flux de travail des publications de blog. La logique liée aux règles vit dans les objets d'état plutôt que d'être éparpillée dans `Post`.

> ### Pourquoi Pas Un Enum ?
>
> Vous vous êtes peut-être demandé pourquoi nous n'avons pas utilisé un enum avec les différents états de publication possibles comme variantes. C'est certainement une solution possible ; essayez-la et comparez les résultats finaux pour voir ce que vous préférez ! Un inconvénient de l'utilisation d'un enum est que chaque endroit qui vérifie la valeur de l'enum aura besoin d'une expression `match` ou similaire pour gérer chaque variante possible. Cela pourrait devenir plus répétitif que cette solution d'objet trait.

#### Évaluation du Modèle d'État

Nous avons montré que Rust est capable de mettre en œuvre le modèle d'état orienté objet pour encapsuler les différents types de comportement qu'une publication devrait avoir dans chaque état. Les méthodes sur `Post` ne connaissent rien des divers comportements. Grâce à la façon dont nous avons organisé le code, nous devons regarder en seulement un endroit pour connaître les différentes manières dont une publication publiée peut se comporter : l'implémentation du trait `State` sur la structure `Published`.

Si nous devions créer une implémentation alternative qui n'utiliserait pas le modèle d'état, nous pourrions plutôt utiliser des expressions `match` dans les méthodes sur `Post` ou même dans le code `main` qui vérifie l'état de la publication et change le comportement en ces endroits. Cela signifierait que nous devrions regarder à plusieurs endroits pour comprendre toutes les implications d'une publication étant dans l'état publié.

Avec le modèle d'état, les méthodes de `Post` et les endroits où nous utilisons `Post` n'ont pas besoin d'expressions `match`, et pour ajouter un nouvel état, nous n'aurions qu'à ajouter une nouvelle structure et implémenter les méthodes de trait sur cette structure unique à un endroit.

L'implémentation utilisant le modèle d'état est facile à étendre pour ajouter plus de fonctionnalités. Pour constater la simplicité de la maintenance du code qui utilise le modèle d'état, essayez certaines de ces suggestions :

- Ajoutez une méthode `reject` qui change l'état de la publication de `PendingReview` à `Draft`.
- Exigez deux appels à `approve` avant que l'état puisse être changé en `Published`.
- Autorisez les utilisateurs à ajouter du contenu de texte uniquement lorsqu'une publication est dans l'état `Draft`. Indice : laissez l'objet d'état responsable de ce qui pourrait changer concernant le contenu, mais pas responsable de la modification du `Post`.

Un inconvénient du modèle d'état est qu'en raison des transitions d'état, certains des états sont couplés entre eux. Si nous ajoutons un autre état entre `PendingReview` et `Published`, tel que `Scheduled`, nous devrions modifier le code dans `PendingReview` pour passer à `Scheduled` à la place. Cela coûterait moins cher si `PendingReview` n'avait pas besoin de changer avec l'ajout d'un nouvel état, mais cela signifierait passer à un autre modèle de conception.

Un autre inconvénient est que nous avons dupliqué une certaine logique. Pour éliminer une partie de la duplication, nous pourrions essayer de créer des implémentations par défaut pour les méthodes `request_review` et `approve` sur le trait `State` qui renvoient `self`. Cependant, cela ne fonctionnerait pas : en utilisant `State` comme un objet trait, le trait ne sait pas quel sera exactement le `self` concret, donc le type de retour n'est pas connu à la compilation. (C'est l'une des règles de compatibilité dynamiques mentionnées précédemment.)

D'autres duplications incluent les implémentations similaires des méthodes `request_review` et `approve` sur `Post`. Les deux méthodes utilisent `Option::take` avec le champ `state` de `Post`, et si `state` est `Some`, elles délèguent à l'implémentation de la même méthode de la valeur enveloppée et définissent la nouvelle valeur du champ `state` sur le résultat. Si nous avions beaucoup de méthodes sur `Post` qui suivaient ce modèle, nous pourrions envisager de définir une macro pour éliminer la répétition (voir la section [« Macros »](ch20-05-macros.html#macros) dans le chapitre 20).

En implémentant le modèle d'état exactement comme il est défini pour les langages orientés objet, nous ne tirons pas autant parti des forces de Rust que nous pourrions. Regardons quelques changements que nous pouvons apporter au crate `blog` pour transformer des états et des transitions invalides en erreurs de compilation.

### Encodage des États et Comportement comme Types

Nous allons vous montrer comment repenser le modèle d'état pour obtenir un ensemble différent de compromis. Plutôt que d'encapsuler complètement les états et les transitions afin qu'un code externe n'en ait pas connaissance, nous allons encoder les états dans différents types. Par conséquent, le système de vérification de types de Rust empêchera toute tentative d'utiliser des publications en brouillon là où seules des publications publiées sont autorisées en émettant une erreur de compilateur.

Considérons la première partie de `main` dans l'énumération 18-11 :

Nous habilitons toujours la création de nouvelles publications en brouillon en utilisant `Post::new` et la possibilité d'ajouter du texte au contenu de la publication. Mais au lieu d'avoir une méthode `content` sur une publication en brouillon qui renvoie une chaîne vide, nous allons faire en sorte que les publications en brouillon n'aient pas du tout la méthode `content`. De cette façon, si nous essayons d'obtenir le contenu d'une publication en brouillon, nous obtiendrons une erreur de compilation nous indiquant que la méthode n'existe pas. Ainsi, il sera impossible pour nous d'afficher accidentellement le contenu d'une publication en brouillon en production.

Les publications en brouillon n'ont donc pas leur contenu disponible pour affichage. Toute tentative de contourner ces contraintes aboutira à une erreur de compilation.

### Implémentation des Transitions en Transformations en Différents Types

Alors, comment obtenir une publication publiée ? Nous voulons faire respecter la règle qu'une publication en brouillon doit être révisée et approuvée avant de pouvoir être publiée. Une publication en attente de révision ne devrait toujours pas afficher de contenu. Implémentons ces contraintes en ajoutant une autre structure, `PendingReviewPost`, en définissant la méthode `request_review` sur `DraftPost` pour renvoyer un `PendingReviewPost` et en définissant une méthode `approve` sur `PendingReviewPost` pour renvoyer un `Post`.

La méthode `request_review` et la méthode `approve` prennent possession de `self`, consommant ainsi les instances de `DraftPost` et de `PendingReviewPost` et les transformant en `PendingReviewPost` et en une publication `Post`, respectivement. De cette façon, nous n'aurons pas d'anciennes instances de `DraftPost` après avoir appelé `request_review` sur elles, et vice versa. La structure `PendingReviewPost` n'a pas de méthode `content` définie, donc tenter de lire son contenu entraîne une erreur de compilation, tout comme pour `DraftPost`. Étant donné que la seule façon d'obtenir une instance de `Post` publiée, qui a une méthode `content` définie, est d'appeler la méthode `approve` sur un `PendingReviewPost`, et la seule façon d'obtenir un `PendingReviewPost` est d'appeler la méthode `request_review` sur un `DraftPost`, nous avons maintenant encodé le flux de travail des publications de blog dans le système de types.

Mais nous devons également apporter quelques petites modifications à `main`. Les méthodes `request_review` et `approve` renvoient de nouvelles instances au lieu de modifier la structure sur laquelle elles sont appelées, donc nous devons ajouter plus d'assignations de masquerade `let post =` pour sauvegarder les instances retournées. Nous ne pouvons également pas avoir les assertions concernant le contenu des publications en brouillon et en attente de révision comme étant des chaînes vides, ni nous n'en avons besoin : nous ne pouvons plus compiler de code qui essaie d'utiliser le contenu de publications dans ces états.

Le code mis à jour dans `main` est montré dans l'énumération 18-21.

Les changements que nous avons dû apporter à `main` pour réaffecter `post` signifient que cette implémentation ne suit plus tout à fait le modèle d'état orienté objet : Les transformations entre les états ne sont plus entièrement encapsulées au sein de l'implémentation `Post`. Cependant, notre gain est que les états invalides sont maintenant impossibles grâce au système de types et à la vérification des types qui se produit à la compilation ! Cela garantit que certains bugs, tels que l'affichage du contenu d'une publication non publiée, seront découverts avant qu'ils ne parviennent à la production.

Essayez les tâches suggérées au début de cette section sur le crate `blog` tel qu'il est après l'énumération 18-21 pour voir ce que vous pensez de la conception de cette version du code. Notez que certaines des tâches peuvent déjà être complétées dans ce design.

Nous avons vu que même si Rust est capable d'implémenter des modèles de conception orientés objet, d'autres modèles, comme l'encodage de l'état dans le système de types, sont également disponibles en Rust. Ces modèles présentent différents compromis. Bien que vous soyez peut-être très familier avec les modèles orientés objet, repenser le problème pour tirer parti des fonctionnalités de Rust peut offrir des avantages, tels que la prévention de certains bugs à la compilation. Les modèles orientés objet ne seront pas toujours la meilleure solution en Rust en raison de certaines caractéristiques, comme la propriété, que les langages orientés objet n'ont pas.

## Résumé

Peu importe que vous pensiez que Rust est un langage orienté objet après avoir lu ce chapitre, vous savez maintenant que vous pouvez utiliser des objets trait pour obtenir certaines fonctionnalités orientées objet en Rust. Le dispatch dynamique peut donner à votre code une certaine flexibilité en échange d'une légère perte de performance à l'exécution. Vous pouvez utiliser cette flexibilité pour implémenter des modèles orientés objet qui peuvent aider à la maintenabilité de votre code. Rust a également d'autres fonctionnalités, comme la propriété, qui ne sont pas présentes dans les langages orientés objet. Un modèle orienté objet ne sera pas toujours le meilleur moyen de tirer parti des forces de Rust, mais c'est une option disponible.

Ensuite, nous examinerons les modèles, qui sont une autre des fonctionnalités de Rust permettant une grande flexibilité. Nous les avons examinés brièvement tout au long du livre mais nous n'avons pas encore vu leur pleine capacité. Allons-y !