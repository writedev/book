## Chemins pour désigner un élément dans l’arborescence des modules

Pour indiquer à Rust où trouver un élément dans une arborescence de modules, nous utilisons un chemin, comme lorsque nous parcourons un système de fichiers. Pour appeler une fonction, nous devons connaître son chemin.

Un chemin peut prendre deux formes :

- Un _chemin absolu_ est le chemin complet qui part de la racine d’une caisse ; pour le code d’une caisse externe, le chemin absolu commence par le nom de la caisse, et pour le code de la caisse actuelle, il commence par le littéral `crate`.
- Un _chemin relatif_ part du module actuel et utilise `self`, `super` ou un identifiant du module actuel.

Les chemins absolus comme relatifs sont suivis d’un ou de plusieurs identifiants séparés par des doubles deux-points (`::`).

Revenons à la liste 7-1 et supposons que nous voulions appeler la fonction `add_to_waitlist`. Cela revient à demander : quel est le chemin de la fonction `add_to_waitlist` ? La liste 7-3 reprend la liste 7-1 en supprimant certains modules et fonctions.

Nous allons présenter deux façons d’appeler la fonction `add_to_waitlist` depuis une nouvelle fonction, `eat_at_restaurant`, définie à la racine de la caisse. Ces chemins sont corrects, mais il reste un autre problème qui empêchera cet exemple de compiler tel quel. Nous expliquerons pourquoi dans un instant.

La fonction `eat_at_restaurant` fait partie de l’API publique de notre caisse de bibliothèque, nous la marquons donc avec le mot-clé `pub`. Dans la section [« Exposer des chemins avec le mot-clé `pub` »][pub]<!-- ignore -->, nous expliquerons `pub` plus en détail.

<Listing number="7-3" file-name="src/lib.rs" caption="Appeler la fonction `add_to_waitlist` à l’aide de chemins absolus et relatifs">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-03/src/lib.rs}}
```

</Listing>

La première fois que nous appelons la fonction `add_to_waitlist` dans `eat_at_restaurant`, nous utilisons un chemin absolu. La fonction `add_to_waitlist` est définie dans la même caisse que `eat_at_restaurant`, ce qui signifie que nous pouvons utiliser le mot-clé `crate` pour commencer un chemin absolu. Nous indiquons ensuite chacun des modules successifs jusqu’à arriver à `add_to_waitlist`. Imaginez un système de fichiers ayant la même structure : nous préciserions le chemin `/front_of_house/hosting/add_to_waitlist` pour exécuter le programme `add_to_waitlist` ; utiliser le nom `crate` pour partir de la racine de la caisse revient à utiliser `/` pour partir de la racine du système de fichiers dans votre interpréteur de commandes.

La deuxième fois que nous appelons `add_to_waitlist` dans `eat_at_restaurant`, nous utilisons un chemin relatif. Le chemin commence par `front_of_house`, le nom du module défini au même niveau de l’arborescence des modules que `eat_at_restaurant`. L’équivalent dans un système de fichiers serait d’utiliser le chemin `front_of_house/hosting/add_to_waitlist`. Commencer par un nom de module signifie que le chemin est relatif.

Choisir d’utiliser un chemin relatif ou absolu est une décision qui dépend de votre projet et de la probabilité que vous déplaciez le code qui définit un élément séparément du code qui l’utilise, ou avec celui-ci. Par exemple, si nous déplacions le module `front_of_house` et la fonction `eat_at_restaurant` dans un module nommé `customer_experience`, nous devrions mettre à jour le chemin absolu vers `add_to_waitlist`, mais le chemin relatif resterait valide. En revanche, si nous déplacions séparément la fonction `eat_at_restaurant` dans un module nommé `dining`, le chemin absolu vers l’appel de `add_to_waitlist` resterait le même, mais le chemin relatif devrait être mis à jour. En général, nous préférons indiquer des chemins absolus, car il est plus probable que nous souhaitions déplacer indépendamment les définitions de code et les appels aux éléments.

Essayons de compiler la liste 7-3 pour découvrir pourquoi elle ne compile pas encore ! Les erreurs obtenues sont présentées dans la liste 7-4.

<Listing number="7-4" caption="Erreurs du compilateur lors de la compilation du code de la liste 7-3">

```console
{{#include ../listings/ch07-managing-growing-projects/listing-07-03/output.txt}}
```

</Listing>

Les messages d’erreur indiquent que le module `hosting` est privé. Autrement dit, les chemins vers le module `hosting` et la fonction `add_to_waitlist` sont corrects, mais Rust ne nous permet pas de les utiliser, car nous n’avons pas accès aux parties privées. Dans Rust, tous les éléments (fonctions, méthodes, structures, énumérations, modules et constantes) sont privés pour leurs modules parents par défaut. Pour rendre privé un élément comme une fonction ou une structure, vous le placez dans un module.

Les éléments d’un module parent ne peuvent pas utiliser les éléments privés des modules enfants, mais les éléments des modules enfants peuvent utiliser ceux de leurs modules ancêtres. En effet, les modules enfants encapsulent et masquent leurs détails d’implémentation, mais ils peuvent voir le contexte dans lequel ils sont définis. Pour poursuivre notre métaphore, imaginez que les règles de confidentialité sont semblables à l’arrière-boutique d’un restaurant : ce qui s’y passe est privé pour les clients du restaurant, mais les responsables de l’arrière-boutique peuvent tout voir et tout faire dans le restaurant qu’ils gèrent.

Rust a choisi de faire fonctionner ainsi le système de modules afin que les détails d’implémentation internes soient masqués par défaut. Vous savez ainsi quelles parties du code interne vous pouvez modifier sans casser le code externe. Cependant, Rust vous permet d’exposer des parties du code des modules enfants aux modules ancêtres externes en utilisant le mot-clé `pub` pour rendre un élément public.

### Exposer des chemins avec le mot-clé `pub`

Revenons à l’erreur de la liste 7-4, qui nous indiquait que le module `hosting` est privé. Nous voulons que la fonction `eat_at_restaurant` du module parent puisse accéder à la fonction `add_to_waitlist` du module enfant ; nous marquons donc le module `hosting` avec le mot-clé `pub`, comme indiqué dans la liste 7-5.

<Listing number="7-5" file-name="src/lib.rs" caption="Déclarer le module `hosting` comme `pub` pour l’utiliser depuis `eat_at_restaurant`">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-05/src/lib.rs:here}}
```

</Listing>

Malheureusement, le code de la liste 7-5 génère toujours des erreurs du compilateur, comme le montre la liste 7-6.

<Listing number="7-6" caption="Erreurs du compilateur lors de la compilation du code de la liste 7-5">

```console
{{#include ../listings/ch07-managing-growing-projects/listing-07-05/output.txt}}
```

</Listing>

Que s’est-il passé ? Ajouter le mot-clé `pub` devant `mod hosting` rend le module public. Grâce à cette modification, si nous pouvons accéder à `front_of_house`, nous pouvons accéder à `hosting`. Mais le _contenu_ de `hosting` reste privé ; rendre le module public ne rend pas son contenu public. Le mot-clé `pub` appliqué à un module permet uniquement au code de ses modules ancêtres de le désigner, et non d’accéder à son code interne. Comme les modules sont des conteneurs, nous ne pouvons pas faire grand-chose en rendant uniquement le module public ; nous devons aller plus loin et choisir de rendre publics un ou plusieurs éléments du module.

Les erreurs de la liste 7-6 indiquent que la fonction `add_to_waitlist` est privée. Les règles de confidentialité s’appliquent également aux structures, aux énumérations, aux fonctions et aux méthodes, ainsi qu’aux modules.

Rendons également publique la fonction `add_to_waitlist` en ajoutant le mot-clé `pub` avant sa définition, comme dans la liste 7-7.

<Listing number="7-7" file-name="src/lib.rs" caption="Ajouter le mot-clé `pub` à `mod hosting` et à `fn add_to_waitlist` nous permet d’appeler la fonction depuis `eat_at_restaurant`.">

```rust,noplayground,test_harness
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-07/src/lib.rs:here}}
```

</Listing>

Le code compile maintenant ! Pour comprendre pourquoi l’ajout du mot-clé `pub` nous permet d’utiliser ces chemins dans `eat_at_restaurant` au regard des règles de confidentialité, examinons les chemins absolus et relatifs.

Dans le chemin absolu, nous commençons par `crate`, la racine de l’arborescence des modules de notre caisse. Le module `front_of_house` est défini à la racine de la caisse. Bien que `front_of_house` ne soit pas public, la fonction `eat_at_restaurant` étant définie dans le même module que `front_of_house` (c’est-à-dire que `eat_at_restaurant` et `front_of_house` sont des éléments frères), nous pouvons désigner `front_of_house` depuis `eat_at_restaurant`. Vient ensuite le module `hosting`, marqué avec `pub`. Nous pouvons accéder au module parent de `hosting`, et donc accéder à `hosting`. Enfin, la fonction `add_to_waitlist` est marquée avec `pub`, et nous pouvons accéder à son module parent ; cet appel de fonction fonctionne donc !

Dans le chemin relatif, la logique est la même que pour le chemin absolu, à l’exception de la première étape : au lieu de partir de la racine de la caisse, le chemin part de `front_of_house`. Le module `front_of_house` est défini dans le même module que `eat_at_restaurant`, le chemin relatif qui part du module où `eat_at_restaurant` est défini fonctionne donc. Ensuite, comme `hosting` et `add_to_waitlist` sont marqués avec `pub`, le reste du chemin fonctionne et cet appel de fonction est valide !

Si vous prévoyez de partager votre caisse de bibliothèque afin que d’autres projets puissent utiliser votre code, votre API publique constitue le contrat qui définit la façon dont les utilisateurs de votre caisse peuvent interagir avec votre code. De nombreux aspects doivent être pris en compte pour gérer les modifications de votre API publique et faciliter la dépendance des autres à votre caisse. Ces considérations dépassent le cadre de ce livre ; si ce sujet vous intéresse, consultez [les recommandations de l’API Rust][api-guidelines].

> #### Bonnes pratiques pour les paquets comprenant un exécutable et une bibliothèque
>
> Nous avons indiqué qu’un paquet peut contenir à la fois une racine de caisse exécutable _src/main.rs_ et une racine de caisse de bibliothèque _src/lib.rs_, et que les deux caisses portent par défaut le nom du paquet. En général, les paquets qui suivent ce modèle, avec une caisse de bibliothèque et une caisse exécutable, ne contiennent dans la caisse exécutable que le code nécessaire pour lancer un exécutable qui appelle le code défini dans la caisse de bibliothèque. Ainsi, d’autres projets peuvent tirer parti de la majeure partie des fonctionnalités offertes par le paquet, puisque le code de la caisse de bibliothèque peut être partagé.
>
> L’arborescence des modules doit être définie dans _src/lib.rs_. Les éléments publics peuvent ensuite être utilisés dans la caisse exécutable en commençant les chemins par le nom du paquet. La caisse exécutable utilise la caisse de bibliothèque comme le ferait une caisse entièrement externe : elle ne peut utiliser que l’API publique. Cela vous aide à concevoir une bonne API ; vous n’en êtes pas seulement l’auteur, vous en êtes aussi l’utilisateur !
>
> Dans le [chapitre 12][ch12]<!-- ignore -->, nous présenterons cette pratique d’organisation avec un programme en ligne de commande qui contiendra à la fois une caisse exécutable et une caisse de bibliothèque.

### Commencer les chemins relatifs par `super`

Nous pouvons construire des chemins relatifs qui commencent dans le module parent, plutôt que dans le module actuel ou à la racine de la caisse, en utilisant `super` au début du chemin. Cela revient à commencer un chemin de système de fichiers par la syntaxe `..`, qui signifie remonter au répertoire parent. Utiliser `super` nous permet de désigner un élément dont nous savons qu’il se trouve dans le module parent, ce qui peut faciliter la réorganisation de l’arborescence des modules lorsque le module est étroitement lié à son parent, mais que celui-ci pourrait un jour être déplacé ailleurs dans l’arborescence.

Considérons le code de la liste 7-8, qui illustre le cas où un chef corrige une commande incorrecte et l’apporte lui-même au client. La fonction `fix_incorrect_order`, définie dans le module `back_of_house`, appelle la fonction `deliver_order`, définie dans le module parent, en indiquant le chemin vers `deliver_order` qui commence par `super`.

<Listing number="7-8" file-name="src/lib.rs" caption="Appeler une fonction à l’aide d’un chemin relatif commençant par `super`">

```rust,noplayground,test_harness
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-08/src/lib.rs}}
```

</Listing>

La fonction `fix_incorrect_order` se trouve dans le module `back_of_house`, nous pouvons donc utiliser `super` pour remonter au module parent de `back_of_house`, qui est ici `crate`, la racine. À partir de là, nous recherchons `deliver_order` et la trouvons. C’est réussi ! Nous pensons que le module `back_of_house` et la fonction `deliver_order` conserveront probablement leur relation et seront déplacés ensemble si nous décidons de réorganiser l’arborescence des modules de la caisse. Nous avons donc utilisé `super` afin d’avoir moins d’endroits à mettre à jour dans le code à l’avenir si ce code est déplacé vers un autre module.

### Rendre publiques les structures et les énumérations

Nous pouvons également utiliser `pub` pour déclarer des structures et des énumérations publiques, mais l’utilisation de `pub` avec les structures et les énumérations comporte quelques particularités supplémentaires. Si nous plaçons `pub` avant la définition d’une structure, nous rendons la structure publique, mais ses champs restent privés. Nous pouvons décider au cas par cas de rendre chaque champ public ou non. Dans la liste 7-9, nous avons défini une structure publique `back_of_house::Breakfast` avec un champ public `toast` et un champ privé `seasonal_fruit`. Cela représente le cas d’un restaurant où le client peut choisir le type de pain servi avec un repas, mais où le chef choisit le fruit qui accompagne le repas en fonction des fruits de saison et des stocks. Les fruits disponibles changent rapidement ; les clients ne peuvent donc pas choisir le fruit ni même savoir quel fruit ils recevront.

<Listing number="7-9" file-name="src/lib.rs" caption="Une structure avec des champs publics et des champs privés">

```rust,noplayground
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-09/src/lib.rs}}
```

</Listing>

Comme le champ `toast` de la structure `back_of_house::Breakfast` est public, nous pouvons lire et écrire dans ce champ depuis `eat_at_restaurant` en utilisant la notation avec un point. Notez que nous ne pouvons pas utiliser le champ `seasonal_fruit` dans `eat_at_restaurant`, car `seasonal_fruit` est privé. Essayez de décommenter la ligne qui modifie la valeur du champ `seasonal_fruit` pour voir l’erreur obtenue !

Notez également que, puisque `back_of_house::Breakfast` possède un champ privé, la structure doit fournir une fonction associée publique qui construit une instance de `Breakfast` (nous l’avons appelée `summer` ici). Si `Breakfast` ne possédait pas une telle fonction, nous ne pourrions pas créer d’instance de `Breakfast` dans `eat_at_restaurant`, car nous ne pourrions pas définir la valeur du champ privé `seasonal_fruit` dans `eat_at_restaurant`.

En revanche, si nous rendons une énumération publique, toutes ses variantes le deviennent également. Il suffit de placer `pub` avant le mot-clé `enum`, comme le montre la liste 7-10.

<Listing number="7-10" file-name="src/lib.rs" caption="Déclarer une énumération publique rend toutes ses variantes publiques.">

```rust,noplayground
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-10/src/lib.rs}}
```

</Listing>

Comme nous avons rendu l’énumération `Appetizer` publique, nous pouvons utiliser les variantes `Soup` et `Salad` dans `eat_at_restaurant`.

Les énumérations ne sont pas très utiles si leurs variantes ne sont pas publiques ; il serait fastidieux de devoir annoter chaque variante d’énumération avec `pub` dans tous les cas, c’est pourquoi les variantes d’énumération sont publiques par défaut. Les structures sont souvent utiles même lorsque leurs champs ne sont pas publics ; les champs des structures suivent donc la règle générale selon laquelle tout est privé par défaut, sauf indication contraire avec `pub`.

Il nous reste une autre situation impliquant `pub` à aborder, qui constitue également la dernière fonctionnalité de notre système de modules : le mot-clé `use`. Nous allons d’abord traiter `use` à part, puis montrer comment combiner `pub` et `use`.

[pub]: ch07-03-paths-for-referring-to-an-item-in-the-module-tree.html#exposing-paths-with-the-pub-keyword
[api-guidelines]: https://rust-lang.github.io/api-guidelines/
[ch12]: ch12-00-an-io-project.html