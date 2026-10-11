## `RefCell<T>` et le modèle de mutabilité intérieure

La _mutabilité intérieure_ est un modèle de conception en Rust qui permet de modifier des données même lorsqu’il existe des références immuables vers ces données ; normalement, cette action est interdite par les règles d’emprunt. Pour modifier des données, ce modèle utilise du code `unsafe` à l’intérieur d’une structure de données afin d’assouplir les règles habituelles de Rust qui régissent la mutation et l’emprunt. Le code non sûr indique au compilateur que nous vérifions nous-mêmes les règles au lieu de compter sur lui pour le faire ; nous parlerons davantage du code non sûr au chapitre 20.

Nous pouvons utiliser des types qui suivent le modèle de mutabilité intérieure uniquement lorsque nous pouvons garantir que les règles d’emprunt seront respectées à l’exécution, même si le compilateur ne peut pas le garantir. Le code `unsafe` concerné est alors encapsulé dans une API sûre, et le type externe reste immuable.

Explorons ce concept en examinant le type `RefCell<T>`, qui suit le modèle de mutabilité intérieure.

<!-- Old headings. Do not remove or links may break. -->

<a id="enforcing-borrowing-rules-at-runtime-with-refcellt"></a>

### Appliquer les règles d’emprunt à l’exécution

Contrairement à `Rc<T>`, le type `RefCell<T>` représente une propriété unique des données qu’il contient. Alors, qu’est-ce qui distingue `RefCell<T>` d’un type comme `Box<T>` ? Rappelons les règles d’emprunt apprises au chapitre 4 :

- À un instant donné, vous pouvez avoir _soit_ une référence mutable, soit un nombre quelconque de références immuables (mais pas les deux).
- Les références doivent toujours être valides.

Avec les références et `Box<T>`, les invariants des règles d’emprunt sont appliqués à la compilation. Avec `RefCell<T>`, ces invariants sont appliqués _à l’exécution_. Avec les références, si vous enfreignez ces règles, vous obtenez une erreur du compilateur. Avec `RefCell<T>`, si vous enfreignez ces règles, votre programme panique et s’arrête.

L’avantage de vérifier les règles d’emprunt à la compilation est que les erreurs sont détectées plus tôt dans le processus de développement, et que cela n’a aucun impact sur les performances à l’exécution, puisque toute l’analyse est effectuée au préalable. Pour ces raisons, vérifier les règles d’emprunt à la compilation est le meilleur choix dans la majorité des cas, et c’est pourquoi c’est le comportement par défaut de Rust.

L’avantage de vérifier les règles d’emprunt à l’exécution est que certains scénarios sûrs pour la mémoire deviennent possibles, alors qu’ils auraient été rejetés par les vérifications à la compilation. L’analyse statique, comme celle du compilateur Rust, est par nature prudente. Certaines propriétés du code sont impossibles à détecter par analyse : l’exemple le plus célèbre est le problème de l’arrêt, qui dépasse le cadre de ce livre, mais constitue un sujet de recherche intéressant.

Comme certaines analyses sont impossibles, si le compilateur Rust ne peut pas s’assurer que le code respecte les règles de propriété, il peut rejeter un programme correct ; il se montre ainsi prudent. Si Rust acceptait un programme incorrect, les utilisateurs ne pourraient pas faire confiance aux garanties qu’il offre. En revanche, si Rust rejette un programme correct, le programmeur sera gêné, mais rien de catastrophique ne peut se produire. Le type `RefCell<T>` est utile lorsque vous êtes certain que votre code respecte les règles d’emprunt, mais que le compilateur est incapable de le comprendre et de le garantir.

Comme `Rc<T>`, `RefCell<T>` est réservé aux scénarios monothread et provoque une erreur de compilation si vous essayez de l’utiliser dans un contexte multithread. Nous verrons au chapitre 16 comment obtenir les fonctionnalités de `RefCell<T>` dans un programme multithread.

Voici un récapitulatif des raisons de choisir `Box<T>`, `Rc<T>` ou `RefCell<T>` :

- `Rc<T>` permet à plusieurs propriétaires de partager les mêmes données ; `Box<T>` et `RefCell<T>` n’ont qu’un seul propriétaire.
- `Box<T>` permet des emprunts immuables ou mutables vérifiés à la compilation ; `Rc<T>` ne permet que des emprunts immuables vérifiés à la compilation ; `RefCell<T>` permet des emprunts immuables ou mutables vérifiés à l’exécution.
- Comme `RefCell<T>` permet des emprunts mutables vérifiés à l’exécution, vous pouvez modifier la valeur à l’intérieur de `RefCell<T>` même lorsque `RefCell<T>` est immuable.

La modification de la valeur à l’intérieur d’une valeur immuable constitue le modèle de mutabilité intérieure. Examinons une situation où la mutabilité intérieure est utile et voyons comment elle est possible.

<!-- Old headings. Do not remove or links may break. -->

<a id="interior-mutability-a-mutable-borrow-to-an-immutable-value"></a>

### Utiliser la mutabilité intérieure

Les règles d’emprunt impliquent que lorsque vous avez une valeur immuable, vous ne pouvez pas l’emprunter de manière mutable. Par exemple, ce code ne compilera pas :

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch15-smart-pointers/no-listing-01-cant-borrow-immutable-as-mutable/src/main.rs}}
```

Si vous essayiez de compiler ce code, vous obtiendriez l’erreur suivante :

```console
{{#include ../listings/ch15-smart-pointers/no-listing-01-cant-borrow-immutable-as-mutable/output.txt}}
```

Il existe toutefois des situations où il serait utile qu’une valeur puisse se modifier dans ses méthodes tout en semblant immuable pour le reste du code. Le code extérieur aux méthodes de la valeur ne pourrait pas modifier celle-ci. Utiliser `RefCell<T>` est une façon d’obtenir la mutabilité intérieure, mais `RefCell<T>` ne permet pas de contourner complètement les règles d’emprunt : l’emprunteur du compilateur autorise cette mutabilité intérieure, et les règles d’emprunt sont vérifiées à l’exécution. Si vous enfreignez ces règles, vous obtiendrez une `panic!` au lieu d’une erreur du compilateur.

Étudions un exemple pratique où nous pouvons utiliser `RefCell<T>` pour modifier une valeur immuable et comprendre pourquoi cela est utile.

<!-- Old headings. Do not remove or links may break. -->

<a id="a-use-case-for-interior-mutability-mock-objects"></a>

#### Tester avec des objets simulés

Lors des tests, un programmeur utilise parfois un type à la place d’un autre afin d’observer un comportement particulier et de vérifier qu’il est correctement implémenté. Ce type de substitution est appelé une _doublure de test_. Pensez à un cascadeur au cinéma : il remplace un acteur pour réaliser une scène particulièrement périlleuse. Les doublures de test remplacent d’autres types lorsque nous exécutons des tests. Les _objets simulés_ sont des types particuliers de doublures de test qui enregistrent ce qui se passe pendant un test afin que vous puissiez vérifier que les bonnes actions ont eu lieu.

Rust n’a pas d’objets au même sens que d’autres langages, et sa bibliothèque standard ne fournit pas de fonctionnalité intégrée pour les objets simulés, contrairement à certaines autres langues. Vous pouvez toutefois créer une structure qui remplira les mêmes fonctions qu’un objet simulé.

Voici le scénario que nous allons tester : nous allons créer une bibliothèque qui compare une valeur à une valeur maximale et envoie des messages en fonction de la proximité entre la valeur actuelle et la valeur maximale. Cette bibliothèque pourrait, par exemple, servir à suivre le quota de requêtes d’API autorisées pour un utilisateur.

Notre bibliothèque ne fournira que les fonctionnalités permettant de suivre la proximité d’une valeur par rapport au maximum et de déterminer quels messages envoyer et à quel moment. Les applications qui utilisent notre bibliothèque devront fournir le mécanisme d’envoi des messages : l’application pourra afficher directement le message à l’utilisateur, envoyer un courriel ou un SMS, ou faire autre chose. La bibliothèque n’a pas besoin de connaître ce détail. Elle a seulement besoin d’un élément qui implémente un trait que nous allons fournir, appelé `Messenger`. La liste 15-20 montre le code de la bibliothèque.

<Listing number="15-20" file-name="src/lib.rs" caption="Une bibliothèque qui suit la proximité d’une valeur par rapport à une valeur maximale et avertit lorsque la valeur atteint certains seuils">

```rust,noplayground
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-20/src/lib.rs}}
```

</Listing>

Un aspect important de ce code est que le trait `Messenger` possède une méthode appelée `send`, qui prend une référence immuable à `self` et le texte du message. Ce trait constitue l’interface que notre objet simulé doit implémenter pour pouvoir être utilisé comme un véritable objet. L’autre aspect important est que nous voulons tester le comportement de la méthode `set_value` de `LimitTracker`. Nous pouvons modifier la valeur que nous transmettons au paramètre `value`, mais `set_value` ne renvoie rien sur quoi nous puissions effectuer des assertions. Nous voulons pouvoir dire que si nous créons un `LimitTracker` avec un élément qui implémente le trait `Messenger` et une valeur particulière pour `max`, le messager doit envoyer les messages appropriés lorsque nous lui transmettons différentes valeurs pour `value`.

Nous avons besoin d’un objet simulé qui, au lieu d’envoyer un courriel ou un SMS lorsque nous appelons `send`, se contente d’enregistrer les messages qu’on lui demande d’envoyer. Nous pouvons créer une nouvelle instance de l’objet simulé, créer un `LimitTracker` qui l’utilise, appeler la méthode `set_value` de `LimitTracker`, puis vérifier que l’objet simulé contient les messages attendus. La liste 15-21 montre une tentative d’implémentation d’un objet simulé à cette fin, mais l’emprunteur ne l’autorise pas.

<Listing number="15-21" file-name="src/lib.rs" caption="Tentative d’implémentation d’un `MockMessenger` rejetée par l’emprunteur">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-21/src/lib.rs:here}}
```

</Listing>

Ce code de test définit une structure `MockMessenger` dont le champ `sent_messages` contient un `Vec` de valeurs `String` pour garder une trace des messages qu’on lui demande d’envoyer. Nous définissons également une fonction associée `new` afin de créer facilement de nouvelles valeurs `MockMessenger` dont la liste de messages est vide. Nous implémentons ensuite le trait `Messenger` pour `MockMessenger`, afin de pouvoir transmettre un `MockMessenger` à un `LimitTracker`. Dans la définition de la méthode `send`, nous prenons le message transmis en paramètre et le stockons dans la liste `sent_messages` de `MockMessenger`.

Dans le test, nous vérifions ce qui se passe lorsque `LimitTracker` reçoit l’instruction de définir `value` à une valeur supérieure à 75 % de la valeur `max`. Nous créons d’abord un nouveau `MockMessenger`, dont la liste de messages est vide. Puis, nous créons un nouveau `LimitTracker` et lui donnons une référence au nouveau `MockMessenger` ainsi qu’une valeur `max` de `100`. Nous appelons la méthode `set_value` de `LimitTracker` avec la valeur `80`, qui est supérieure à 75 % de 100. Enfin, nous vérifions que la liste des messages enregistrés par `MockMessenger` en contient désormais un.

Cependant, ce test présente un problème, comme le montre l’extrait suivant :

```console
{{#include ../listings/ch15-smart-pointers/listing-15-21/output.txt}}
```

Nous ne pouvons pas modifier `MockMessenger` pour garder une trace des messages, car la méthode `send` prend une référence immuable à `self`. Nous ne pouvons pas non plus suivre la suggestion du message d’erreur et utiliser `&mut self` à la fois dans la méthode d’implémentation et dans la définition du trait. Nous ne voulons pas modifier le trait `Messenger` uniquement pour les besoins des tests. Nous devons plutôt trouver un moyen de faire fonctionner correctement notre code de test avec la conception existante.

C’est une situation où la mutabilité intérieure peut nous aider ! Nous allons stocker `sent_messages` dans un `RefCell<T>`, puis la méthode `send` pourra modifier `sent_messages` pour y stocker les messages reçus. La liste 15-22 montre à quoi cela ressemble.

<Listing number="15-22" file-name="src/lib.rs" caption="Utiliser `RefCell<T>` pour modifier une valeur intérieure alors que la valeur extérieure est considérée comme immuable">

```rust,noplayground
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-22/src/lib.rs:here}}
```

</Listing>

Le champ `sent_messages` est désormais de type `RefCell<Vec<String>>` au lieu de `Vec<String>`. Dans la fonction `new`, nous créons une nouvelle instance de `RefCell<Vec<String>>` autour du vecteur vide.

Dans l’implémentation de la méthode `send`, le premier paramètre reste un emprunt immuable de `self`, conformément à la définition du trait. Nous appelons `borrow_mut` sur le `RefCell<Vec<String>>` de `self.sent_messages` pour obtenir une référence mutable à la valeur contenue dans `RefCell<Vec<String>>`, c’est-à-dire le vecteur. Nous pouvons ensuite appeler `push` sur la référence mutable au vecteur afin de garder une trace des messages envoyés pendant le test.

La dernière modification à effectuer concerne l’assertion : pour connaître le nombre d’éléments du vecteur intérieur, nous appelons `borrow` sur le `RefCell<Vec<String>>` afin d’obtenir une référence immuable au vecteur.

Maintenant que vous avez vu comment utiliser `RefCell<T>`, examinons son fonctionnement !

<!-- Old headings. Do not remove or links may break. -->

<a id="keeping-track-of-borrows-at-runtime-with-refcellt"></a>

#### Suivre les emprunts à l’exécution

Pour créer des références immuables et mutables, nous utilisons respectivement la syntaxe `&` et `&mut`. Avec `RefCell<T>`, nous utilisons les méthodes `borrow` et `borrow_mut`, qui font partie de l’API sûre de `RefCell<T>`. La méthode `borrow` renvoie le type de pointeur intelligent `Ref<T>`, et `borrow_mut` renvoie le type de pointeur intelligent `RefMut<T>`. Les deux types implémentent `Deref`, ce qui nous permet de les traiter comme des références ordinaires.

`RefCell<T>` garde la trace du nombre de pointeurs intelligents `Ref<T>` et `RefMut<T>` actuellement actifs. Chaque fois que nous appelons `borrow`, `RefCell<T>` incrémente le nombre d’emprunts immuables actifs. Lorsqu’une valeur `Ref<T>` sort de portée, le nombre d’emprunts immuables diminue de 1. Comme avec les règles d’emprunt vérifiées à la compilation, `RefCell<T>` nous permet d’avoir plusieurs emprunts immuables ou un seul emprunt mutable à un instant donné.

Si nous essayons d’enfreindre ces règles, l’implémentation de `RefCell<T>` provoquera une panique à l’exécution au lieu d’une erreur du compilateur, comme ce serait le cas avec les références. La liste 15-23 montre une modification de l’implémentation de `send` de la liste 15-22. Nous essayons délibérément de créer deux emprunts mutables actifs dans la même portée afin d’illustrer que `RefCell<T>` nous en empêche à l’exécution.

<Listing number="15-23" file-name="src/lib.rs" caption="Créer deux références mutables dans la même portée pour constater que `RefCell<T>` provoque une panique">

```rust,ignore,panics
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-23/src/lib.rs:here}}
```

</Listing>

Nous créons une variable `one_borrow` pour le pointeur intelligent `RefMut<T>` renvoyé par `borrow_mut`. Puis, nous créons un autre emprunt mutable de la même manière dans la variable `two_borrow`. Cela crée deux références mutables dans la même portée, ce qui n’est pas autorisé. Lorsque nous exécutons les tests de notre bibliothèque, le code de la liste 15-23 compile sans erreur, mais le test échoue :

```console
{{#include ../listings/ch15-smart-pointers/listing-15-23/output.txt}}
```

Remarquez que le code a paniqué avec le message `already borrowed:
BorrowMutError`. C’est ainsi que `RefCell<T>` gère les violations des règles d’emprunt à l’exécution.

Choisir de détecter les erreurs d’emprunt à l’exécution plutôt qu’à la compilation, comme nous l’avons fait ici, signifie que vous risquez de découvrir des erreurs dans votre code plus tard dans le processus de développement, peut-être même après son déploiement en production. De plus, votre code subira une légère pénalité de performances à l’exécution, car il devra suivre les emprunts à l’exécution plutôt qu’à la compilation. Toutefois, `RefCell<T>` permet d’écrire un objet simulé capable de se modifier pour garder une trace des messages reçus, même dans un contexte où seules les valeurs immuables sont autorisées. Vous pouvez accepter les compromis liés à `RefCell<T>` afin de bénéficier de fonctionnalités plus étendues que celles offertes par les références ordinaires.

<!-- Old headings. Do not remove or links may break. -->

<a id="having-multiple-owners-of-mutable-data-by-combining-rc-t-and-ref-cell-t"></a>
<a id="allowing-multiple-owners-of-mutable-data-with-rct-and-refcellt"></a>

### Permettre à plusieurs propriétaires de partager des données mutables

Une façon courante d’utiliser `RefCell<T>` consiste à le combiner avec `Rc<T>`. Rappelons que `Rc<T>` permet à plusieurs propriétaires de partager certaines données, mais ne donne qu’un accès immuable à celles-ci. Si vous avez un `Rc<T>` qui contient un `RefCell<T>`, vous pouvez obtenir une valeur qui a plusieurs propriétaires _et_ que vous pouvez modifier !

Par exemple, rappelons l’exemple de liste chaînée cons de la liste 15-18, où nous avons utilisé `Rc<T>` pour permettre à plusieurs listes de partager la propriété d’une autre liste. Comme `Rc<T>` ne contient que des valeurs immuables, nous ne pouvons modifier aucune des valeurs de la liste une fois celles-ci créées. Ajoutons `RefCell<T>` pour pouvoir modifier les valeurs des listes. La liste 15-24 montre qu’en utilisant un `RefCell<T>` dans la définition de `Cons`, nous pouvons modifier la valeur stockée dans toutes les listes.

<Listing number="15-24" file-name="src/main.rs" caption="Utiliser `Rc<RefCell<i32>>` pour créer une `List` que nous pouvons modifier">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-24/src/main.rs}}
```

</Listing>

Nous créons une valeur qui est une instance de `Rc<RefCell<i32>>` et la stockons dans une variable nommée `value`, afin de pouvoir y accéder directement plus tard. Ensuite, nous créons dans `a` une `List` avec une variante `Cons` qui contient `value`. Nous devons cloner `value` pour que `a` et `value` soient tous deux propriétaires de la valeur intérieure `5`, au lieu de transférer la propriété de `value` à `a` ou de faire en sorte que `a` emprunte `value`.

Nous enveloppons la liste `a` dans un `Rc<T>` afin que les listes `b` et `c` puissent toutes deux faire référence à `a`, comme dans la liste 15-18.

Après avoir créé les listes `a`, `b` et `c`, nous voulons ajouter 10 à la valeur de `value`. Pour cela, nous appelons `borrow_mut` sur `value`, ce qui utilise la fonctionnalité de déréférencement automatique dont nous avons parlé dans [« Où est l’opérateur `->` ? »][wheres-the---operator]<!-- ignore --> au chapitre 5 pour déréférencer le `Rc<T>` jusqu’à la valeur intérieure `RefCell<T>`. La méthode `borrow_mut` renvoie un pointeur intelligent `RefMut<T>`, sur lequel nous utilisons l’opérateur de déréférencement pour modifier la valeur intérieure.

Lorsque nous affichons `a`, `b` et `c`, nous pouvons constater qu’ils contiennent tous la valeur modifiée `15` au lieu de `5` :

```console
{{#include ../listings/ch15-smart-pointers/listing-15-24/output.txt}}
```

Cette technique est plutôt astucieuse ! En utilisant `RefCell<T>`, nous obtenons une valeur `List` qui semble immuable. Mais nous pouvons utiliser les méthodes de `RefCell<T>` qui donnent accès à sa mutabilité intérieure pour modifier nos données lorsque nous en avons besoin. Les vérifications à l’exécution des règles d’emprunt nous protègent contre les courses de données, et il vaut parfois la peine d’échanger un peu de vitesse contre cette flexibilité dans nos structures de données. Notez que `RefCell<T>` ne fonctionne pas avec du code multithread ! `Mutex<T>` est la version de `RefCell<T>` qui est sûre pour les threads, et nous parlerons de `Mutex<T>` au chapitre 16.

[wheres-the---operator]: ch05-03-method-syntax.html#wheres-the---operator