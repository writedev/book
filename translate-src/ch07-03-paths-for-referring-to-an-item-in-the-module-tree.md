## Chemins pour se référer à un élément dans l'arbre des modules

Pour montrer à Rust où trouver un élément dans un arbre de modules, nous utilisons un chemin de la même manière que nous utilisons un chemin lors de la navigation dans un système de fichiers. Pour appeler une fonction, nous devons connaître son chemin.

Un chemin peut prendre deux formes :

- Un _chemin absolu_ est le chemin complet à partir de la racine d'un crate ; pour le code d'un crate externe, le chemin absolu commence par le nom du crate, et pour le code du crate courant, il commence par le littéral `crate`.
- Un _chemin relatif_ commence à partir du module courant et utilise `self`, `super`, ou un identifiant dans le module courant.

Les chemins absolus et relatifs sont suivis d'un ou plusieurs identifiants séparés par des doubles deux-points (`::`).

Revenons à la liste 7-1, disons que nous voulons appeler la fonction `add_to_waitlist`. C’est la même chose que de demander : Quel est le chemin de la fonction `add_to_waitlist` ? La liste 7-3 contient la liste 7-1 avec certains des modules et fonctions supprimés.

Nous allons montrer deux façons d'appeler la fonction `add_to_waitlist` depuis une nouvelle fonction, `eat_at_restaurant`, définie à la racine du crate. Ces chemins sont corrects, mais il reste un autre problème qui empêchera cet exemple de compiler tel quel. Nous expliquerons pourquoi un peu plus tard.

La fonction `eat_at_restaurant` fait partie de l'API publique de notre crate de bibliothèque, donc nous la marquons avec le mot-clé `pub`. Dans la section [« Exposition des chemins avec le mot-clé `pub` »][pub]<!-- ignore -->, nous entrerons dans plus de détails sur `pub`.

<Listing number="7-3" file-name="src/lib.rs" caption="Appel de la fonction `add_to_waitlist` en utilisant des chemins absolus et relatifs">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-03/src/lib.rs}}
```

</Listing>

La première fois que nous appelons la fonction `add_to_waitlist` dans `eat_at_restaurant`, nous utilisons un chemin absolu. La fonction `add_to_waitlist` est définie dans le même crate que `eat_at_restaurant`, ce qui signifie que nous pouvons utiliser le mot-clé `crate` pour commencer un chemin absolu. Nous incluons ensuite chacun des modules successifs jusqu'à ce que nous parvenions à `add_to_waitlist`. Vous pouvez imaginer un système de fichiers ayant la même structure : Nous spécifierions le chemin `/front_of_house/hosting/add_to_waitlist` pour exécuter le programme `add_to_waitlist` ; utiliser le nom du `crate` pour commencer à partir de la racine du crate est comme utiliser `/` pour commencer à partir de la racine du système de fichiers dans votre shell.

La deuxième fois que nous appelons `add_to_waitlist` dans `eat_at_restaurant`, nous utilisons un chemin relatif. Le chemin commence par `front_of_house`, le nom du module défini au même niveau de l'arbre des modules que `eat_at_restaurant`. Ici, l'équivalent dans le système de fichiers serait d'utiliser le chemin `front_of_house/hosting/add_to_waitlist`. Commencer avec un nom de module signifie que le chemin est relatif.

Le choix d'utiliser un chemin relatif ou absolu est une décision que vous prendrez en fonction de votre projet, et cela dépend de si vous êtes plus susceptible de déplacer le code de définition des éléments séparément ou ensemble avec le code qui utilise l'élément. Par exemple, si nous déplacions le module `front_of_house` et la fonction `eat_at_restaurant` dans un module nommé `customer_experience`, nous devrions mettre à jour le chemin absolu vers `add_to_waitlist`, mais le chemin relatif resterait valide. Cependant, si nous déplacions la fonction `eat_at_restaurant` séparément dans un module nommé `dining`, le chemin absolu vers l'appel de `add_to_waitlist` resterait le même, mais le chemin relatif devrait être mis à jour. En général, notre préférence est de spécifier des chemins absolus car il est plus probable que nous souhaitions déplacer indépendamment les définitions de code et les appels d'éléments.

Essayons de compiler la liste 7-3 et découvrons pourquoi elle ne compile pas encore ! Les erreurs que nous obtenons sont montrées dans la liste 7-4.

<Listing number="7-4" caption="Erreurs du compilateur lors de la construction du code dans la liste 7-3">

```console
{{#include ../listings/ch07-managing-growing-projects/listing-07-03/output.txt}}
```

</Listing>

Les messages d'erreur indiquent que le module `hosting` est privé. En d'autres termes, nous avons les chemins corrects pour le module `hosting` et la fonction `add_to_waitlist`, mais Rust ne nous permet pas de les utiliser car il n'a pas accès aux sections privées. En Rust, tous les éléments (fonctions, méthodes, structs, enums, modules et constantes) sont privés pour les modules parents par défaut. Si vous souhaitez rendre un élément, comme une fonction ou une struct, privé, vous le mettez dans un module.

Les éléments d'un module parent ne peuvent pas utiliser les éléments privés à l'intérieur des modules enfants, mais les éléments des modules enfants peuvent utiliser les éléments de leurs modules ancêtres. Cela est dû au fait que les modules enfants encapsulent et cachent leurs détails d'implémentation, mais les modules enfants peuvent voir le contexte dans lequel ils sont définis. Pour continuer avec notre métaphore, pensez aux règles de confidentialité comme étant semblables au bureau arrière d'un restaurant : Ce qui s'y passe est privé pour les clients du restaurant, mais les gestionnaires de bureau peuvent voir et faire tout dans le restaurant qu'ils exploitent.

Rust a choisi de faire fonctionner le système de modules de cette manière afin que le masquage des détails d'implémentation internes soit la norme. De cette façon, vous savez quelles parties du code interne vous pouvez modifier sans casser le code externe. Cependant, Rust vous donne la possibilité d'exposer les parties internes du code des modules enfants à des modules ancêtres externes en utilisant le mot-clé `pub` pour rendre un élément public.

### Exposition des chemins avec le mot-clé `pub`

Revenons à l'erreur de la liste 7-4 qui nous disait que le module `hosting` est privé. Nous voulons que la fonction `eat_at_restaurant` dans le module parent ait accès à la fonction `add_to_waitlist` dans le module enfant, donc nous marquons le module `hosting` avec le mot-clé `pub`, comme indiqué dans la liste 7-5.

<Listing number="7-5" file-name="src/lib.rs" caption="Déclarer le module `hosting` comme `pub` pour l'utiliser depuis `eat_at_restaurant`">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-05/src/lib.rs:here}}
```

</Listing>

Malheureusement, le code dans la liste 7-5 entraîne toujours des erreurs de compilation, comme le montre la liste 7-6.

<Listing number="7-6" caption="Erreurs du compilateur lors de la construction du code dans la liste 7-5">

```console
{{#include ../listings/ch07-managing-growing-projects/listing-07-05/output.txt}}
```

</Listing>

Que s'est-il passé ? Ajouter le mot-clé `pub` devant `mod hosting` rend le module public. Avec ce changement, si nous pouvons accéder à `front_of_house`, nous pouvons accéder à `hosting`. Mais les _contenus_ de `hosting` sont toujours privés ; rendre le module public ne rend pas son contenu public. Le mot-clé `pub` sur un module ne permet pas simplement à un code dans ses modules ancêtres de s'y référer, mais d'accéder aussi à son code interne. Comme les modules sont des conteneurs, il n'y a pas grand-chose que nous puissions faire en rendant simplement le module public ; nous devons aller plus loin et choisir de rendre un ou plusieurs des éléments à l'intérieur du module publics également.

Les erreurs dans la liste 7-6 indiquent que la fonction `add_to_waitlist` est privée. Les règles de confidentialité s'appliquent également aux structs, enums, fonctions et méthodes ainsi qu'aux modules.

Rendons également la fonction `add_to_waitlist` publique en ajoutant le mot-clé `pub` avant sa définition, comme dans la liste 7-7.

<Listing number="7-7" file-name="src/lib.rs" caption="Ajouter le mot-clé `pub` à `mod hosting` et `fn add_to_waitlist` nous permet d'appeler la fonction depuis `eat_at_restaurant`.">

```rust,noplayground,test_harness
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-07/src/lib.rs:here}}
```

</Listing>

Maintenant, le code va compiler ! Pour comprendre pourquoi l'ajout du mot-clé `pub` nous permet d'utiliser ces chemins dans `eat_at_restaurant` par rapport aux règles de confidentialité, examinons les chemins absolus et relatifs.

Dans le chemin absolu, nous commençons par `crate`, la racine de l'arbre des modules de notre crate. Le module `front_of_house` est défini à la racine du crate. Bien que `front_of_house` ne soit pas public, comme la fonction `eat_at_restaurant` est définie dans le même module que `front_of_house` (c'est-à-dire que `eat_at_restaurant` et `front_of_house` sont frères), nous pouvons faire référence à `front_of_house` depuis `eat_at_restaurant`. Ensuite, il y a le module `hosting` marqué avec `pub`. Nous pouvons accéder au module parent de `hosting`, donc nous pouvons accéder à `hosting`. Enfin, la fonction `add_to_waitlist` est marquée avec `pub`, et nous pouvons accéder à son module parent, donc cet appel de fonction fonctionne !

Dans le chemin relatif, la logique est la même que dans le chemin absolu, sauf pour la première étape : Au lieu de commencer à partir de la racine du crate, le chemin commence par `front_of_house`. Le module `front_of_house` est défini dans le même module que `eat_at_restaurant`, donc le chemin relatif commençant à partir du module dans lequel `eat_at_restaurant` est défini fonctionne. Ensuite, comme `hosting` et `add_to_waitlist` sont marqués avec `pub`, le reste du chemin fonctionne, et cet appel de fonction est valide !

Si vous prévoyez de partager votre crate de bibliothèque afin que d'autres projets puissent utiliser votre code, votre API publique est votre contrat avec les utilisateurs de votre crate qui détermine comment ils peuvent interagir avec votre code. Il y a de nombreuses considérations concernant la gestion des changements à votre API publique pour faciliter la dépendance des gens à votre crate. Ces considérations dépassent le cadre de ce livre ; si vous êtes intéressé par ce sujet, consultez [les lignes directrices de l'API Rust][api-guidelines].

> #### Meilleures pratiques pour les packages avec un binaire et une bibliothèque
>
> Nous avons mentionné qu'un package peut contenir à la fois une racine de crate binaire _src/main.rs_ ainsi qu'une racine de crate de bibliothèque _src/lib.rs_, et les deux crates auront par défaut le nom du package. Généralement, les packages avec ce modèle contenant à la fois une bibliothèque et une crate binaire n'ont juste assez de code dans la crate binaire pour commencer un exécutable qui appelle le code défini dans la crate de bibliothèque. Cela permet à d'autres projets de bénéficier de la plus grande fonctionnalité que le package fournit, car le code de la crate de bibliothèque peut être partagé.
>
> L'arbre des modules doit être défini dans _src/lib.rs_. Ensuite, tous les éléments publics peuvent être utilisés dans la crate binaire en commençant les chemins avec le nom du package. La crate binaire devient un utilisateur de la crate de bibliothèque tout comme une crate externe complètement utiliserait la crate de bibliothèque : Elle ne peut utiliser que l'API publique. Cela vous aide à concevoir une bonne API ; non seulement vous êtes l'auteur, mais vous êtes aussi un client !
>
> Dans [le Chapitre 12][ch12]<!-- ignore -->, nous démontrerons cette pratique organisationnelle avec un programme en ligne de commande qui contiendra à la fois une crate binaire et une crate de bibliothèque.

### Démarrer des chemins relatifs avec `super`

Nous pouvons construire des chemins relatifs qui commencent dans le module parent, plutôt que dans le module courant ou la racine du crate, en utilisant `super` au début du chemin. Cela ressemble à commencer un chemin de système de fichiers avec la syntaxe `..` qui signifie aller au répertoire parent. Utiliser `super` nous permet de faire référence à un élément qui, selon nous, se trouve dans le module parent, ce qui peut faciliter le réarrangement de l'arbre des modules lorsque le module est étroitement lié au parent mais que le parent pourrait être déplacé ailleurs dans l'arbre des modules un jour.

Considérons le code dans la liste 7-8 qui modélise la situation dans laquelle un chef corrige une commande incorrecte et l'apporte personnellement au client. La fonction `fix_incorrect_order` définie dans le module `back_of_house` appelle la fonction `deliver_order` définie dans le module parent en spécifiant le chemin vers `deliver_order`, en commençant par `super`.

<Listing number="7-8" file-name="src/lib.rs" caption="Appel d'une fonction en utilisant un chemin relatif commençant par `super`">

```rust,noplayground,test_harness
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-08/src/lib.rs}}
```

</Listing>

La fonction `fix_incorrect_order` se trouve dans le module `back_of_house`, donc nous pouvons utiliser `super` pour aller au module parent de `back_of_house`, qui dans ce cas est `crate`, la racine. De là, nous recherchons `deliver_order` et le trouvons. Succès ! Nous pensons que le module `back_of_house` et la fonction `deliver_order` sont susceptibles de rester dans la même relation l'un par rapport à l'autre et d'être déplacés ensemble si nous décidons de réorganiser l'arbre des modules de la crate. C'est pourquoi nous avons utilisé `super` afin d'avoir moins d'endroits à mettre à jour dans le code à l'avenir si ce code est déplacé dans un autre module.

### Rendre les structs et enums publics

Nous pouvons également utiliser `pub` pour désigner les structs et les enums comme publics, mais il y a quelques détails supplémentaires à propos de l'utilisation de `pub` avec les structs et les enums. Si nous utilisons `pub` avant une définition de struct, nous rendons la struct publique, mais les champs de la struct resteront privés. Nous pouvons rendre chaque champ public ou non au cas par cas. Dans la liste 7-9, nous avons défini une struct publique `back_of_house::Breakfast` avec un champ public `toast` mais un champ privé `seasonal_fruit`. Cela modélise le cas dans un restaurant où le client peut choisir le type de pain qui accompagne un repas, mais le chef décide quel fruit accompagne le repas en fonction de ce qui est de saison et en stock. Les fruits disponibles changent rapidement, donc les clients ne peuvent pas choisir le fruit ou même voir quel fruit ils auront.

<Listing number="7-9" file-name="src/lib.rs" caption="Une struct avec certains champs publics et certains champs privés">

```rust,noplayground
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-09/src/lib.rs}}
```

</Listing>

Parce que le champ `toast` dans la struct `back_of_house::Breakfast` est public, dans `eat_at_restaurant`, nous pouvons écrire et lire au champ `toast` en utilisant la notation par point. Notez que nous ne pouvons pas utiliser le champ `seasonal_fruit` dans `eat_at_restaurant`, car `seasonal_fruit` est privé. Essayez de décommenter la ligne modifiant la valeur du champ `seasonal_fruit` pour voir quelle erreur vous obtenez !

De plus, notez qu'en raison du champ privé `back_of_house::Breakfast`, la struct doit fournir une fonction associée publique qui construit une instance de `Breakfast` (nous l'avons nommée `summer` ici). Si `Breakfast` n'avait pas de telle fonction, nous ne pourrions pas créer une instance de `Breakfast` dans `eat_at_restaurant`, car nous ne pourrions pas définir la valeur du champ privé `seasonal_fruit` dans `eat_at_restaurant`.

En revanche, si nous rendons une enum publique, toutes ses variantes deviennent alors publiques. Nous avons seulement besoin du `pub` avant le mot-clé `enum`, comme montré dans la liste 7-10.

<Listing number="7-10" file-name="src/lib.rs" caption="Désigner une enum comme publique rend toutes ses variantes publiques.">

```rust,noplayground
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-10/src/lib.rs}}
```

</Listing>

Parce que nous avons rendu l'énumération `Appetizer` publique, nous pouvons utiliser les variantes `Soup` et `Salad` dans `eat_at_restaurant`.

Les enums ne sont pas très utiles à moins que leurs variantes soient publiques ; il serait ennuyeux d'avoir à annoter toutes les variantes d'enum avec `pub` dans chaque cas, donc la norme pour les variantes d'enum est d'être publiques. Les structs sont souvent utiles sans que leurs champs soient publics, donc les champs de struct suivent la règle générale selon laquelle tout est privé par défaut, sauf s'il est annoté avec `pub`.

Il y a une dernière situation impliquant `pub` que nous n'avons pas encore couverte, et c'est notre dernière fonctionnalité du système de modules : le mot-clé `use`. Nous allons d'abord couvrir `use` seul, puis nous montrerons comment combiner `pub` et `use`.

[pub]: ch07-03-paths-for-referring-to-an-item-in-the-module-tree.html#exposing-paths-with-the-pub-keyword
[api-guidelines]: https://rust-lang.github.io/api-guidelines/
[ch12]: ch12-00-an-io-project.html