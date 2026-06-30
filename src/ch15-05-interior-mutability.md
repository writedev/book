## `RefCell<T>` et le motif de mutabilité intérieure

La _mutabilité intérieure_ est un motif de conception en Rust qui permet de modifier des données même lorsqu'il existe des références immuables à ces données ; normalement, cette action est interdite par les règles d'emprunt. Pour modifier les données, le motif utilise du code `unsafe` à l'intérieur d'une structure de données pour plier les règles habituelles de Rust qui régissent la mutation et l'emprunt. Le code `unsafe` indique au compilateur que nous vérifions les règles manuellement au lieu de compter sur le compilateur pour les vérifier pour nous ; nous discuterons du code `unsafe` plus en détail dans le Chapitre 20.

Nous pouvons utiliser des types qui appliquent le motif de mutabilité intérieure uniquement lorsque nous pouvons garantir que les règles d'emprunt seront respectées à l'exécution, même si le compilateur ne peut pas le garantir. Le code `unsafe` impliqué est ensuite encapsulé dans une API sûre, et le type extérieur reste immuable.

Explorons ce concept en examinant le type `RefCell<T>` qui suit le motif de mutabilité intérieure.

### Enforcement des règles d'emprunt à l'exécution

Contrairement à `Rc<T>`, le type `RefCell<T>` représente une possession unique des données qu'il contient. Qu'est-ce qui rend `RefCell<T>` différent d'un type comme `Box<T>` ? Rappelons les règles d'emprunt que vous avez apprises au Chapitre 4 :

- À tout moment, vous pouvez avoir _soit_ une référence mutable, soit un nombre quelconque de références immuables (mais pas les deux).
- Les références doivent toujours être valides.

Avec les références et `Box<T>`, les invariants des règles d'emprunt sont appliqués à la compilation. Avec `RefCell<T>`, ces invariants sont appliqués _à l'exécution_. Avec les références, si vous enfreignez ces règles, vous obtiendrez une erreur de compilation. Avec `RefCell<T>`, si vous enfreignez ces règles, votre programme panique et se termine.

Les avantages de vérifier les règles d'emprunt à la compilation sont que les erreurs seront détectées plus tôt dans le processus de développement, et il n'y a aucun impact sur les performances à l'exécution, car toute l'analyse est effectuée au préalable. Pour ces raisons, vérifier les règles d'emprunt à la compilation est le meilleur choix dans la majorité des cas, c'est pourquoi c'est le comportement par défaut en Rust.

L'avantage de vérifier les règles d'emprunt à l'exécution est que certains scénarios sûrs en mémoire sont alors autorisés, où ils auraient été interdits par les vérifications à la compilation. L'analyse statique, comme le compilateur Rust, est intrinsèquement conservatrice. Certaines propriétés du code sont impossibles à détecter en analysant le code : l'exemple le plus célèbre est le problème de l'arrêt, qui dépasse le cadre de ce livre mais reste un sujet de recherche intéressant.

Parce que certaines analyses sont impossibles, si le compilateur Rust ne peut pas s'assurer que le code respecte les règles de possession, il peut rejeter un programme correct ; de cette manière, il est conservateur. Si Rust acceptait un programme incorrect, les utilisateurs ne pourraient pas faire confiance aux garanties que Rust offre. Cependant, si Rust rejette un programme correct, le programmeur sera gêné, mais rien de catastrophique ne pourra se produire. Le type `RefCell<T>` est utile lorsque vous êtes sûr que votre code respecte les règles d'emprunt mais que le compilateur n'est pas capable de comprendre et garantir cela.

Semblable à `Rc<T>`, `RefCell<T>` n'est à utiliser que dans des scénarios à thread unique et vous obtiendrez une erreur de compilation si vous essayez de l'utiliser dans un contexte multithread. Nous parlerons de la façon d'obtenir la fonctionnalité de `RefCell<T>` dans un programme multithread au Chapitre 16.

Voici un récapitulatif des raisons de choisir `Box<T>`, `Rc<T>`, ou `RefCell<T>` :

- `Rc<T>` permet plusieurs propriétaires des mêmes données ; `Box<T>` et `RefCell<T>` n'ont qu'un seul propriétaire.
- `Box<T>` autorise les emprunts immuables ou mutables vérifiés à la compilation ; `Rc<T>` autorise uniquement les emprunts immuables vérifiés à la compilation ; `RefCell<T>` permet les emprunts immuables ou mutables vérifiés à l'exécution.
- Parce que `RefCell<T>` permet les emprunts mutables vérifiés à l'exécution, vous pouvez modifier la valeur à l'intérieur d'un `RefCell<T>` même lorsque ce dernier est immuable.

Modifier la valeur à l'intérieur d'une valeur immuable est le motif de mutabilité intérieure. Regardons une situation dans laquelle la mutabilité intérieure est utile et examinons comment cela est possible.

### Utiliser la mutabilité intérieure

Une conséquence des règles d'emprunt est que lorsque vous avez une valeur immuable, vous ne pouvez pas l'emprunter de manière mutable. Par exemple, ce code ne compilera pas :

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch15-smart-pointers/no-listing-01-cant-borrow-immutable-as-mutable/src/main.rs}}
```

Si vous essayez de compiler ce code, vous obtiendrez l'erreur suivante :

```console
{{#include ../listings/ch15-smart-pointers/no-listing-01-cant-borrow-immutable-as-mutable/output.txt}}
```

Cependant, il y a des situations où il serait utile qu'une valeur puisse se modifier elle-même dans ses méthodes tout en apparaissant immuable pour le reste du code. Le code en dehors des méthodes de la valeur ne pourrait pas modifier la valeur. Utiliser `RefCell<T>` est un moyen d'obtenir la capacité de mutabilité intérieure, mais `RefCell<T>` ne contourne pas complètement les règles d'emprunt : le vérificateur d'emprunt dans le compilateur permet cette mutabilité intérieure, et les règles d'emprunt sont vérifiées à l'exécution plutôt qu'à la compilation. Si vous enfreignez les règles, vous obtiendrez un `panic!` au lieu d'une erreur de compilation.

Travaillons sur un exemple pratique où nous pouvons utiliser `RefCell<T>` pour modifier une valeur immuable et voir pourquoi cela est utile.

#### Tester avec des objets fictifs

Parfois, lors des tests, un programmeur utilisera un type à la place d'un autre type, afin d'observer un comportement particulier et d'affirmer qu'il est correctement implémenté. Ce type de substitut est appelé un _double de test_. Pensez-y comme un cascadeur dans le cinéma, où une personne remplace un acteur pour réaliser une scène particulièrement délicate. Les doubles de test remplacent d'autres types lorsque nous exécutons des tests. Les _objets fictifs_ sont des types spécifiques de doubles de test qui enregistrent ce qui se passe pendant un test afin que vous puissiez affirmer que les bonnes actions ont eu lieu.

Rust n'a pas d'objets au sens où d'autres langages ont des objets, et Rust n'a pas de fonctionnalité d'objet fictif intégrée dans la bibliothèque standard comme certains autres langages. Cependant, vous pouvez certainement créer une structure qui servira les mêmes objectifs qu'un objet fictif.

Voici le scénario que nous allons tester : Nous allons créer une bibliothèque qui suit une valeur par rapport à une valeur maximum et envoie des messages en fonction de la proximité de la valeur courante à la valeur maximum. Cette bibliothèque pourrait être utilisée pour suivre le quota d'un utilisateur pour le nombre d'appels API autorisés à effectuer, par exemple.

Notre bibliothèque ne fournira que la fonctionnalité de suivi de la proximité par rapport à la valeur maximum et des messages à quel moment. Les applications qui utilisent notre bibliothèque seront censées fournir le mécanisme d'envoi des messages : l'application pourrait afficher le message à l'utilisateur directement, envoyer un e-mail, envoyer un message texte ou faire autre chose. La bibliothèque n'a pas besoin de connaître ce détail. Tout ce dont elle a besoin, c'est quelque chose qui implémente un trait que nous fournirons, appelé `Messenger`. La liste 15-20 montre le code de la bibliothèque.

Voici une partie importante de ce code : le trait `Messenger` a une méthode appelée `send` qui prend une référence immuable à `self` et le texte du message. Ce trait est l'interface que notre objet fictif doit implémenter afin qu'il puisse être utilisé de la même manière qu'un véritable objet. L'autre partie importante est que nous voulons tester le comportement de la méthode `set_value` sur le `LimitTracker`. Nous pouvons changer ce que nous passons comme paramètre `value`, mais `set_value` ne retourne rien sur quoi nous pourrions faire des assertions. Nous voulons être capables de dire que si nous créons un `LimitTracker` avec quelque chose qui implémente le trait `Messenger` et une valeur particulière pour `max`, le messager est informé d'envoyer les messages appropriés lorsque nous passons différents nombres pour `value`.

Nous avons besoin d'un objet fictif qui, au lieu d'envoyer un e-mail ou un message texte lorsque nous appelons `send`, gardera seulement la trace des messages qu'il est informé d'envoyer. Nous pouvons créer une nouvelle instance d'objet fictif, créer un `LimitTracker` qui utilise l'objet fictif, appeler la méthode `set_value` sur `LimitTracker`, puis vérifier que l'objet fictif a les messages que nous attendions. La liste 15-21 montre une tentative d'implémentation d'un objet fictif pour faire exactement cela, mais le vérificateur d'emprunt ne le permettra pas.

Ce code de test définit une structure `MockMessenger` qui a un champ `sent_messages` avec un `Vec` de valeurs `String` pour garder la trace des messages qu'il est informé d'envoyer. Nous définissons également une fonction associée `new` pour faciliter la création de nouvelles valeurs `MockMessenger` qui commencent avec une liste vide de messages. Nous implémentons ensuite le trait `Messenger` pour `MockMessenger` afin que nous puissions donner un `MockMessenger` à un `LimitTracker`. Dans la définition de la méthode `send`, nous prenons le message passé en paramètre et le stockons dans la liste de `sent_messages` de `MockMessenger`.

Dans le test, nous testons ce qui se passe lorsque le `LimitTracker` est informé de définir `value` à quelque chose qui est plus de 75 pour cent de la valeur `max`. D'abord, nous créons un nouveau `MockMessenger`, qui commencera avec une liste vide de messages. Ensuite, nous créons un nouveau `LimitTracker` et lui donnons une référence au nouveau `MockMessenger` et une valeur `max` de `100`. Nous appelons la méthode `set_value` sur `LimitTracker` avec une valeur de `80`, qui est plus de 75 pour cent de 100. Ensuite, nous affirmons que la liste de messages que `MockMessenger` garde doit maintenant avoir un message en elle.

Cependant, il y a un problème avec ce test, comme le montre ici :

Nous ne pouvons pas modifier le `MockMessenger` pour garder la trace des messages, car la méthode `send` prend une référence immuable à `self`. Nous ne pouvons également pas suivre la suggestion du message d'erreur de utiliser `&mut self` dans la méthode `impl` et la définition du trait. Nous ne voulons pas changer le trait `Messenger` uniquement pour le besoin du test. Au lieu de cela, nous devons trouver un moyen de faire fonctionner notre code de test correctement avec notre conception existante.

C'est une situation dans laquelle la mutabilité intérieure peut aider ! Nous allons stocker les `sent_messages` dans un `RefCell<T>`, et ensuite la méthode `send` pourra modifier `sent_messages` pour stocker les messages que nous avons vus. La liste 15-22 montre à quoi cela ressemble.

Le champ `sent_messages` est maintenant de type `RefCell<Vec<String>>` au lieu de `Vec<String>`. Dans la fonction `new`, nous créons une nouvelle instance de `RefCell<Vec<String>>` autour du vecteur vide.

Pour l'implémentation de la méthode `send`, le premier paramètre est toujours un emprunt immuable de `self`, ce qui correspond à la définition du trait. Nous appelons `borrow_mut` sur `RefCell<Vec<String>>` dans `self.sent_messages` pour obtenir une référence mutable à la valeur à l'intérieur du `RefCell<Vec<String>>`, qui est le vecteur. Ensuite, nous pouvons appeler `push` sur la référence mutable du vecteur pour garder la trace des messages envoyés pendant le test.

La dernière modification que nous devons effectuer est dans l'assertion : pour voir combien d'éléments sont dans le vecteur intérieur, nous appelons `borrow` sur `RefCell<Vec<String>>` pour obtenir une référence immuable au vecteur.

Maintenant que vous avez vu comment utiliser `RefCell<T>`, creusons dans la façon dont cela fonctionne !

#### Suivre les emprunts à l'exécution avec `RefCell<T>`

Lorsque nous créons des références immuables et mutables, nous utilisons respectivement la syntaxe `&` et `&mut`. Avec `RefCell<T>`, nous utilisons les méthodes `borrow` et `borrow_mut`, qui font partie de l'API sûre qui appartient à `RefCell<T>`. La méthode `borrow` retourne le type de pointeur intelligent `Ref<T>`, et `borrow_mut` retourne le type de pointeur intelligent `RefMut<T>`. Les deux types implémentent `Deref`, nous pouvons donc les traiter comme des références ordinaires.

Le `RefCell<T>` garde la trace du nombre de pointeurs intelligents `Ref<T>` et `RefMut<T>` qui sont actuellement actifs. Chaque fois que nous appelons `borrow`, le `RefCell<T>` augmente son compteur de combien d'emprunts immuables sont actifs. Lorsque la valeur d'un `Ref<T>` sort de la portée, le compteur des emprunts immuables diminue de 1. Tout comme les règles d'emprunt à la compilation, `RefCell<T>` nous permet d'avoir plusieurs emprunts immuables ou un emprunt mutable à tout moment.

Si nous essayons de violer ces règles, au lieu d’obtenir une erreur de compilation comme nous le ferions avec des références, l'implémentation de `RefCell<T>` va paniquer à l'exécution. La liste 15-23 montre une modification de l'implémentation de `send` dans la liste 15-22. Nous essayons délibérément de créer deux emprunts mutables actifs pour la même portée afin d'illustrer que `RefCell<T>` nous empêche de le faire à l'exécution.

Nous créons une variable `one_borrow` pour le pointeur intelligent `RefMut<T>` retourné par `borrow_mut`. Ensuite, nous créons un autre emprunt mutable de la même manière dans la variable `two_borrow`. Cela crée deux références mutables dans la même portée, ce qui n'est pas autorisé. Lorsque nous exécutons les tests pour notre bibliothèque, le code de la liste 15-23 se compile sans erreurs, mais le test échouera :

Remarquez que le code a paniqué avec le message `already borrowed: BorrowMutError`. C'est ainsi que `RefCell<T>` gère les violations des règles d'emprunt à l'exécution.

Choisir de capturer les erreurs d'emprunt à l'exécution plutôt qu'à la compilation, comme nous l'avons fait ici, signifie que vous pourriez potentiellement découvrir des erreurs dans votre code plus tard dans le processus de développement : peut-être pas avant que votre code ne soit déployé en production. De plus, votre code subirait une petite pénalité de performance à l'exécution en raison du suivi des emprunts à l'exécution plutôt qu'à la compilation. Cependant, utiliser `RefCell<T>` rend possible l'écriture d'un objet fictif qui peut se modifier pour garder la trace des messages qu'il a vus tout en étant utilisé dans un contexte où seules des valeurs immuables sont autorisées. Vous pouvez utiliser `RefCell<T>` malgré ses compromis pour obtenir plus de fonctionnalités que les références ordinaires n'offrent.

### Autoriser plusieurs propriétaires de données mutables

Une façon courante d'utiliser `RefCell<T>` est en combinaison avec `Rc<T>`. Rappelons que `Rc<T>` vous permet d'avoir plusieurs propriétaires de certaines données, mais il ne donne qu'un accès immuable à ces données. Si vous avez un `Rc<T>` qui contient un `RefCell<T>`, vous pouvez obtenir une valeur qui peut avoir plusieurs propriétaires _et_ que vous pouvez modifier !

Par exemple, rappelons l'exemple de la liste cons de la liste 15-18 où nous avons utilisé `Rc<T>` pour permettre à plusieurs listes de partager la propriété d'une autre liste. Comme `Rc<T>` ne contient que des valeurs immuables, nous ne pouvons pas changer aucune des valeurs dans la liste une fois que nous les avons créées. Ajoutons `RefCell<T>` pour sa capacité à modifier les valeurs dans les listes. La liste 15-24 montre qu'en utilisant un `RefCell<T>` dans la définition de `Cons`, nous pouvons modifier la valeur stockée dans toutes les listes.

Nous créons une valeur qui est une instance de `Rc<RefCell<i32>>` et la stockons dans une variable nommée `value` afin de pouvoir y accéder directement plus tard. Ensuite, nous créons une `List` dans `a` avec un variant `Cons` qui contient `value`. Nous devons cloner `value` afin que `a` et `value` aient la propriété de la valeur intérieure `5`, plutôt que de transférer la propriété de `value` vers `a` ou que `a` ne fasse qu'un emprunt depuis `value`.

Nous plaçons la liste `a` dans un `Rc<T>` afin que lorsque nous créons les listes `b` et `c`, elles puissent toutes deux référencer `a`, ce que nous avons fait dans la liste 15-18.

Après avoir créé les listes dans `a`, `b`, et `c`, nous voulons ajouter 10 à la valeur dans `value`. Nous faisons cela en appelant `borrow_mut` sur `value`, ce qui utilise la fonctionnalité de déréférencement automatique que nous avons discutée dans le Chapitre 5 pour déréférencer le `Rc<T>` vers la valeur intérieure `RefCell<T>`. La méthode `borrow_mut` retourne un pointeur intelligent `RefMut<T>`, et nous utilisons l'opérateur de déréférencement dessus et changeons la valeur intérieure.

Lorsque nous imprimons `a`, `b`, et `c`, nous pouvons voir qu'elles ont toutes la valeur modifiée de `15` plutôt que `5` :

Cette technique est plutôt intéressante ! En utilisant `RefCell<T>`, nous avons une valeur `List` extérieurement immuable. Mais nous pouvons utiliser les méthodes sur `RefCell<T>` qui fournissent un accès à sa mutabilité intérieure afin de modifier nos données lorsque nous en avons besoin. Les vérifications à l'exécution des règles d'emprunt nous protègent des conditions de concurrence, et il vaut parfois la peine de troquer un peu de vitesse pour cette flexibilité dans nos structures de données. Remarque : `RefCell<T>` ne fonctionne pas pour le code multithreadé ! `Mutex<T>` est la version sécurisée par les threads de `RefCell<T>` et nous discuterons de `Mutex<T>` au Chapitre 16.