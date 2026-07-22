## Comment Écrire des Tests

_Les tests_ sont des fonctions Rust qui vérifient que le code non-test est fonctionnel comme prévu. Les corps des fonctions de test effectuent typiquement ces trois actions :

- Mettre en place des données ou un état nécessaires.
- Exécuter le code que vous souhaitez tester.
- Affirmer que les résultats correspondent à vos attentes.

Examinons les fonctionnalités que Rust fournit spécifiquement pour écrire des tests qui accomplissent ces actions, notamment l'attribut `test`, quelques macros et l'attribut `should_panic`.

<!-- Anciennes rubriques. Ne pas supprimer ou les liens peuvent être rompus. -->

<a id="anatomie-dune-fonction-de-test"></a>

### Structuration des Fonctions de Test

À son plus simple, un test en Rust est une fonction annotée avec l'attribut `test`. Les attributs sont des métadonnées au sujet de morceaux de code Rust ; un exemple est l'attribut `derive` que nous avons utilisé avec des structures au Chapitre 5. Pour transformer une fonction en fonction de test, ajoutez `#[test]` sur la ligne avant `fn`. Lorsque vous exécutez vos tests avec la commande `cargo test`, Rust construit un binaire de test qui exécute les fonctions annotées et rapporte si chaque fonction de test a réussi ou échoué.

Chaque fois que nous créons un nouveau projet de bibliothèque avec Cargo, un module de test avec une fonction de test est automatiquement généré pour nous. Ce module vous donne un modèle pour écrire vos tests afin que vous n'ayez pas à consulter la structure et la syntaxe exactes chaque fois que vous démarrez un nouveau projet. Vous pouvez ajouter autant de fonctions de test supplémentaires et autant de modules de test que vous le souhaitez !

Nous allons explorer certains aspects du fonctionnement des tests en expérimentant avec le test modèle avant de réellement tester du code. Ensuite, nous écrirons des tests du monde réel qui appellent une partie du code que nous avons écrite et affirment que son comportement est correct.

Créons un nouveau projet de bibliothèque appelé `adder` qui ajoutera deux nombres :

```console
$ cargo new adder --lib
     Projet de bibliothèque `adder` créé
$ cd adder
```

Le contenu du fichier _src/lib.rs_ dans votre bibliothèque `adder` devrait ressembler à l'Listing 11-1.

<Listing number="11-1" file-name="src/lib.rs" caption="Le code généré automatiquement par `cargo new`">

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-01/src/lib.rs}}
```

</Listing>

Le fichier commence avec une fonction `add` d'exemple afin que nous ayons quelque chose à tester.

Pour l'instant, concentrons-nous uniquement sur la fonction `it_works`. Notez l'annotation `#[test]` : cet attribut indique qu'il s'agit d'une fonction de test, afin que le coureur de tests sache traiter cette fonction comme un test. Nous pourrions également avoir des fonctions non-test dans le module `tests` pour aider à configurer des scénarios communs ou effectuer des opérations communes, nous devons donc toujours indiquer quelles fonctions sont des tests.

Le corps de la fonction d'exemple utilise la macro `assert_eq!` pour affirmer que `result`, qui contient le résultat de l'appel à `add` avec 2 et 2, est égal à 4. Cette assertion sert d'exemple du format d'un test typique. Exécutons-le pour voir que ce test réussit.

La commande `cargo test` exécute tous les tests de notre projet, comme montré dans l'Listing 11-2.

<Listing number="11-2" caption="La sortie de l'exécution du test généré automatiquement">

```console
{{#include ../listings/ch11-writing-automated-tests/listing-11-01/output.txt}}
```

</Listing>

Cargo a compilé et exécuté le test. Nous voyons la ligne `running 1 test`. La ligne suivante montre le nom de la fonction de test générée, appelée `tests::it_works`, et que le résultat de l'exécution de ce test est `ok`. Le résumé général `test result: ok.` signifie que tous les tests ont réussi, et la portion qui lit `1 passed; 0 failed` totalise le nombre de tests réussis ou échoués.

Il est possible de marquer un test comme ignoré pour qu'il ne soit pas exécuté dans une instance particulière ; nous couvrirons cela dans la section [« Ignorer les tests sauf demande spécifique »][ignoring]<!-- ignore --> plus tard dans ce chapitre. Comme nous ne l'avons pas fait ici, le résumé montre `0 ignored`. Nous pouvons également passer un argument à la commande `cargo test` pour exécuter uniquement les tests dont le nom correspond à une chaîne ; cela s'appelle le _filtrage_, et nous le couvrirons dans la section [« Exécuter un sous-ensemble de tests par nom »][subset]<!-- ignore -->. Ici, nous n'avons pas filtré les tests exécutés, donc la fin du résumé montre `0 filtered out`.

La statistique `0 measured` est pour les tests de référence qui mesurent les performances. Les tests de référence sont, à l'heure actuelle, uniquement disponibles dans Rust nightly. Consultez [la documentation sur les tests de référence][bench] pour en savoir plus.

La partie suivante de la sortie des tests qui commence par `Doc-tests adder` est pour les résultats de tout test de documentation. Nous n'avons pas encore de tests de documentation, mais Rust peut compiler tous les exemples de code qui apparaissent dans notre documentation API. Cette fonctionnalité aide à garder vos docs et votre code synchronisés ! Nous discuterons de la façon d'écrire des tests de documentation dans la section [« Commentaires de documentation comme tests »][doc-comments]<!-- ignore --> du Chapitre 14. Pour l'instant, nous allons ignorer la sortie `Doc-tests`.

Commençons à personnaliser le test selon nos besoins. Tout d'abord, changez le nom de la fonction `it_works` en un autre nom, tel que `exploration`, comme ceci :

<span class="filename">Nom de fichier: src/lib.rs</span>

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-01-changing-test-name/src/lib.rs}}
```

Ensuite, exécutez à nouveau `cargo test`. La sortie montre maintenant `exploration` au lieu de `it_works` :

```console
{{#include ../listings/ch11-writing-automated-tests/no-listing-01-changing-test-name/output.txt}}
```

Nous ajouterons un autre test, mais cette fois nous ferons un test qui échoue ! Les tests échouent lorsque quelque chose dans la fonction de test panique. Chaque test est exécuté dans un nouveau thread, et lorsque le thread principal constate qu'un thread de test est mort, le test est marqué comme échoué. Au Chapitre 9, nous avons abordé la façon dont le moyen le plus simple de provoquer une panique est d'appeler la macro `panic!`. Saisissez le nouveau test sous la forme d'une fonction nommée `another`, de sorte que votre fichier _src/lib.rs_ ressemble à l'Listing 11-3.

<Listing number="11-3" file-name="src/lib.rs" caption="Ajout d'un second test qui échouera parce que nous appelons la macro `panic!`">

```rust,panics,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-03/src/lib.rs}}
```

</Listing>

Exécutez à nouveau les tests en utilisant `cargo test`. La sortie devrait ressembler à l'Listing 11-4, qui montre que notre test `exploration` a réussi et que `another` a échoué.

<Listing number="11-4" caption="Résultats des tests lorsque un test réussit et un autre échoue">

```console
{{#include ../listings/ch11-writing-automated-tests/listing-11-03/output.txt}}
```

</Listing>

Au lieu de `ok`, la ligne `test tests::another` montre `FAILED`. Deux nouvelles sections apparaissent entre les résultats individuels et le résumé : la première affiche la raison détaillée de chaque échec de test. Dans ce cas, nous obtenons les détails que `tests::another` a échoué parce qu'il a paniqué avec le message `Make this test fail` à la ligne 17 dans le fichier _src/lib.rs_. La section suivante ne liste que les noms de tous les tests échoués, ce qui est utile lorsqu'il y a beaucoup de tests et beaucoup de sorties détaillées d'échec de tests. Nous pouvons utiliser le nom d'un test échoué pour exécuter uniquement ce test afin de le déboguer plus facilement ; nous parlerons davantage des moyens d'exécuter des tests dans la section [« Contrôler la manière dont les tests sont exécutés »][controlling-how-tests-are-run]<!-- ignore -->.

La ligne de résumé s'affiche à la fin : Globalement, notre résultat de test est `FAILED`. Nous avons eu un test réussi et un test échoué.

Maintenant que vous avez vu à quoi ressemblent les résultats des tests dans différentes situations, examinons quelques macros autres que `panic!` qui sont utiles dans les tests.

<!-- Anciennes rubriques. Ne pas supprimer ou les liens peuvent être rompus. -->

<a id="verification-des-resultats-avec-la-macro-assert"></a>

### Vérification des Résultats avec `assert!`

La macro `assert!`, fournie par la bibliothèque standard, est utile lorsque vous souhaitez vous assurer qu'une certaine condition dans un test évalue à `true`. Nous donnons à la macro `assert!` un argument qui évalue à un booléen. Si la valeur est `true`, rien ne se passe et le test réussit. Si la valeur est `false`, la macro `assert!` appelle `panic!` pour provoquer l'échec du test. Utiliser la macro `assert!` nous aide à vérifier que notre code fonctionne comme nous l'intendons.

Au Chapitre 5, dans l'Listing 5-15, nous avons utilisé une structure `Rectangle` et une méthode `can_hold`, qui sont répétées ici dans l'Listing 11-5. Mettons ce code dans le fichier _src/lib.rs_ puis écrivons quelques tests pour celui-ci en utilisant la macro `assert!`.

<Listing number="11-5" file-name="src/lib.rs" caption="La structure `Rectangle` et sa méthode `can_hold` du Chapitre 5">

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-05/src/lib.rs}}
```

</Listing>

La méthode `can_hold` retourne un booléen, ce qui en fait un cas parfait pour la macro `assert!`. Dans l'Listing 11-6, nous écrivons un test qui teste la méthode `can_hold` en créant une instance de `Rectangle` ayant une largeur de 8 et une hauteur de 7 et en affirmant qu'elle peut contenir une autre instance de `Rectangle` ayant une largeur de 5 et une hauteur de 1.

<Listing number="11-6" file-name="src/lib.rs" caption="Un test pour `can_hold` qui vérifie si un rectangle plus grand peut effectivement contenir un rectangle plus petit">

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-06/src/lib.rs:here}}
```

</Listing>

Notez la ligne `use super::*;` à l'intérieur du module `tests`. Le module `tests` est un module ordinaire qui suit les règles de visibilité habituelles que nous avons abordées au Chapitre 7 dans la section [« Chemins pour se référer à un élément dans l'arbre des modules »][paths-for-referring-to-an-item-in-the-module-tree]<!-- ignore -->. Étant donné que le module `tests` est un module interne, nous devons amener le code sous test dans le module externe dans le champ d'application du module interne. Nous utilisons un glob ici, donc tout ce que nous définissons dans le module externe est disponible pour ce module `tests`.

Nous avons nommé notre test `larger_can_hold_smaller`, et nous avons créé les deux instances de `Rectangle` dont nous avons besoin. Ensuite, nous avons appelé la macro `assert!` et lui avons passé le résultat de l'appel à `larger.can_hold(&smaller)`. Cette expression est censée retourner `true`, donc notre test devrait réussir. Découvrons !

```console
{{#include ../listings/ch11-writing-automated-tests/listing-11-06/output.txt}}
```

Cela réussit ! Ajoutons un autre test, cette fois en affirmant qu'un rectangle plus petit ne peut pas contenir un rectangle plus grand :

<span class="filename">Nom de fichier: src/lib.rs</span>

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-02-adding-another-rectangle-test/src/lib.rs:here}}
```

Comme le résultat correct de la fonction `can_hold` dans ce cas est `false`, nous devons négativer ce résultat avant de le passer à la macro `assert!`. En conséquence, notre test réussira si `can_hold` retourne `false` :

```console
{{#include ../listings/ch11-writing-automated-tests/no-listing-02-adding-another-rectangle-test/output.txt}}
```

Deux tests qui réussissent ! Maintenant, voyons ce qui arrive à nos résultats de tests lorsque nous introduisons un bug dans notre code. Nous allons changer l'implémentation de la méthode `can_hold` en remplaçant le signe supérieur (`>`) par un signe inférieur (`<`) lorsqu'elle compare les largeurs :

```rust,not_desired_behavior,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-03-introducing-a-bug/src/lib.rs:here}}
```

Exécuter les tests produit maintenant le résultat suivant :

```console
{{#include ../listings/ch11-writing-automated-tests/no-listing-03-introducing-a-bug/output.txt}}
```

Nos tests ont détecté le bug ! Comme `larger.width` est `8` et `smaller.width` est `5`, la comparaison des largeurs dans `can_hold` retourne désormais `false` : 8 n'est pas inférieur à 5.

<!-- Anciennes rubriques. Ne pas supprimer ou les liens peuvent être rompus. -->

<a id="test-d'equality-avec-les-macros-assert_eq-et-assert_ne"></a>

### Tester l'Égalité avec `assert_eq!` et `assert_ne!`

Une façon courante de vérifier la fonctionnalité est de tester l'égalité entre le résultat du code soumis au test et la valeur que vous attendiez que le code retourne. Vous pourriez le faire en utilisant la macro `assert!` et en lui passant une expression utilisant l'opérateur `==`. Cependant, comme c'est un test si courant, la bibliothèque standard fournit une paire de macros—`assert_eq!` et `assert_ne!`—pour effectuer ce test plus commodément. Ces macros comparent respectivement deux arguments pour l'égalité ou l'inégalité. Elles imprimeront également les deux valeurs si l'assertion échoue, ce qui facilite la compréhension de _pourquoi_ le test a échoué ; à l'inverse, la macro `assert!` indique uniquement qu'elle a reçu une valeur `false` pour l'expression `==`, sans imprimer les valeurs qui ont conduit à la valeur `false`.

Dans l'Listing 11-7, nous écrivons une fonction nommée `add_two` qui ajoute `2` à son paramètre, puis nous testons cette fonction en utilisant la macro `assert_eq!`.

<Listing number="11-7" file-name="src/lib.rs" caption="Tester la fonction `add_two` en utilisant la macro `assert_eq!`">

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-07/src/lib.rs}}
```

</Listing>

Vérifions si cela passe !

```console
{{#include ../listings/ch11-writing-automated-tests/listing-11-07/output.txt}}
```

Nous créons une variable nommée `result` qui conserve le résultat de l'appel à `add_two(2)`. Ensuite, nous passons `result` et `4` comme arguments à la macro `assert_eq!`. La ligne de sortie pour ce test est `test tests::it_adds_two ... ok`, et le texte `ok` indique que notre test a réussi !

Introduisons un bug dans notre code pour voir à quoi ressemble `assert_eq!` lorsqu'il échoue. Changez l'implémentation de la fonction `add_two` pour ajouter `3` à la place :

```rust,not_desired_behavior,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-04-bug-in-add-two/src/lib.rs:here}}
```

Exécutez à nouveau les tests :

```console
{{#include ../listings/ch11-writing-automated-tests/no-listing-04-bug-in-add-two/output.txt}}
```

Nos tests ont détecté le bug ! Le test `tests::it_adds_two` a échoué, et le message nous indique que l'assertion qui a échoué était `left == right` et quels sont les valeurs de `left` et `right`. Ce message nous aide à démarrer le débogage : l'argument `left`, là où nous avions le résultat de l'appel à `add_two(2)`, était `5`, mais l'argument `right` était `4`. Vous pouvez imaginer que cela serait particulièrement utile lorsque nous avons beaucoup de tests en cours.

Notez que dans certaines langues et framework de test, les paramètres des fonctions d'assertion d'égalité sont appelés `expected` et `actual`, et l'ordre dans lequel nous spécifions les arguments est important. Cependant, en Rust, ils sont appelés `left` et `right`, et l'ordre dans lequel nous spécifions la valeur que nous attendons et celle que le code produit n’a pas d'importance. Nous pourrions écrire l'assertion dans ce test comme `assert_eq!(4, result)`, ce qui donnerait le même message d'échec qui affiche `` l'assertion `left == right` a échoué ``.

La macro `assert_ne!` passera si les deux valeurs que nous lui donnons ne sont pas égales et échouera si elles sont égales. Cette macro est particulièrement utile pour les cas où nous ne sommes pas sûr de ce qu'une valeur _sera_, mais nous savons ce que la valeur _ne devrait pas_ être. Par exemple, si nous testons une fonction qui est garantie de modifier son entrée d'une manière ou d'une autre, mais la manière dont l'entrée est modifiée dépend du jour de la semaine où nous exécutons nos tests, la meilleure chose à affirmer pourrait être que la sortie de la fonction n'est pas égale à l'entrée.

En coulisse, les macros `assert_eq!` et `assert_ne!` utilisent respectivement les opérateurs `==` et `!=`. Lorsque les assertions échouent, ces macros impriment leurs arguments en utilisant un formatage de débogage, ce qui signifie que les valeurs comparées doivent implémenter les traits `PartialEq` et `Debug`. Tous les types primitifs et la plupart des types de la bibliothèque standard implémentent ces traits. Pour les structures et énumérations que vous définissez vous-même, vous devrez implémenter `PartialEq` pour affirmer l'égalité de ces types. Vous devrez également implémenter `Debug` pour imprimer les valeurs lorsque l'assertion échoue. Étant donné que les deux traits sont des traits dérivables, comme mentionné dans l'Listing 5-12 au Chapitre 5, cela se fait généralement aussi simplement que d'ajouter l'annotation `#[derive(PartialEq, Debug)]` à votre définition de structure ou d'énumération. Consultez l'Appendice C, [« Traits dérivables »][derivable-traits]<!-- ignore --> pour plus de détails sur ces traits dérivables et d'autres.

### Ajout de Messages d'Échec Personnalisés

Vous pouvez également ajouter un message personnalisé à imprimer avec le message d'échec comme arguments optionnels aux macros `assert!`, `assert_eq!`, et `assert_ne!`. Tous les arguments spécifiés après les arguments requis sont transmis à la macro `format!` (discutée dans [« Concaténer avec `+` ou `format!` »][concatenating]<!-- ignore --> au Chapitre 8), ainsi vous pouvez passer une chaîne de format contenant des espaces réservés `{}` et des valeurs à insérer dans ces espaces réservés. Les messages personnalisés sont utiles pour documenter ce que signifie une assertion ; lorsqu'un test échoue, vous aurez une meilleure idée du problème dans le code.

Par exemple, supposons que nous avons une fonction qui salue les gens par leur nom et que nous voulons tester que le nom que nous passons à la fonction apparaît dans la sortie :

<span class="filename">Nom de fichier: src/lib.rs</span>

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-05-greeter/src/lib.rs}}
```

Les exigences pour ce programme n'ont pas encore été convenues, et nous sommes assez sûrs que le texte `Hello` au début de la salutation changera. Nous avons décidé que nous ne voulons pas avoir à mettre à jour le test lorsque les exigences changent, donc au lieu de vérifier l'égalité exacte avec la valeur retournée par la fonction `greeting`, nous allons seulement affirmer que la sortie contient le texte du paramètre d'entrée.

Maintenant, introduisons un bug dans ce code en modifiant `greeting` pour exclure `name` afin de voir à quoi ressemble l'échec de test par défaut :

```rust,not_desired_behavior,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-06-greeter-with-bug/src/lib.rs:here}}
```

Exécuter ce test produit le résultat suivant :

```console
{{#include ../listings/ch11-writing-automated-tests/no-listing-06-greeter-with-bug/output.txt}}
```

Ce résultat indique simplement que l'assertion a échoué et à quelle ligne se trouve l'assertion. Un message d'échec plus utile imprimerait la valeur de la fonction `greeting`. Ajoutons un message d'échec personnalisé composé d'une chaîne de format avec un espace réservé rempli par la valeur réelle que nous avons obtenue à partir de la fonction `greeting` :

```rust,ignore
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-07-custom-failure-message/src/lib.rs:here}}
```

Maintenant, lorsque nous exécutons le test, nous obtiendrons un message d'erreur plus informatif :

```console
{{#include ../listings/ch11-writing-automated-tests/no-listing-07-custom-failure-message/output.txt}}
```

Nous pouvons voir la valeur que nous avons réellement obtenue dans la sortie du test, ce qui nous aiderait à déboguer ce qui s'est passé par rapport à ce que nous attendions.

### Vérification des Paniques avec `should_panic`

En plus de vérifier les valeurs de retour, il est important de vérifier que notre code gère les conditions d'erreur comme nous le prévoyons. Par exemple, considérons le type `Guess` que nous avons créé au Chapitre 9, Listing 9-13. D'autres codes qui utilisent `Guess` dépendent de la garantie que les instances de `Guess` ne contiendront que des valeurs entre 1 et 100. Nous pouvons écrire un test qui s'assure qu'une tentative de créer une instance de `Guess` avec une valeur en dehors de cette plage panique.

Nous le faisons en ajoutant l'attribut `should_panic` à notre fonction de test. Le test réussit si le code à l'intérieur de la fonction panique ; le test échoue si le code à l'intérieur de la fonction ne panique pas.

L'Listing 11-8 montre un test qui vérifie que les conditions d'erreur de `Guess::new` se produisent lorsque nous nous y attendons.

<Listing number="11-8" file-name="src/lib.rs" caption="Tester qu'une condition provoquera un `panic!`">

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-08/src/lib.rs}}
```

</Listing>

Nous plaçons l'attribut `#[should_panic]` après l'attribut `#[test]` et avant la fonction de test à laquelle il s'applique. Voyons le résultat lorsque ce test réussit :

```console
{{#include ../listings/ch11-writing-automated-tests/listing-11-08/output.txt}}
```

Ça a l'air bien ! Maintenant introduisons un bug dans notre code en supprimant la condition que la fonction `new` panique si la valeur est supérieure à 100 :

```rust,not_desired_behavior,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-08-guess-with-bug/src/lib.rs:here}}
```

Lorsque nous exécutons le test dans l'Listing 11-8, il échouera :

```console
{{#include ../listings/ch11-writing-automated-tests/no-listing-08-guess-with-bug/output.txt}}
```

Nous n'obtenons pas de message très utile dans ce cas, mais lorsque nous regardons la fonction de test, nous voyons qu'elle est annotée avec `#[should_panic]`. Le défaillance que nous avons reçue signifie que le code dans la fonction de test n'a pas causé de panique.

Les tests qui utilisent `should_panic` peuvent être imprécis. Un test `should_panic` réussirait même si le test paniquait pour une autre raison que celle que nous attendions. Pour rendre les tests `should_panic` plus précis, nous pouvons ajouter un paramètre `expected` facultatif à l'attribut `should_panic`. Le système de test s'assurera que le message d'échec contient le texte fourni. Par exemple, considérons le code modifié pour `Guess` dans l'Listing 11-9 où la fonction `new` panique avec différents messages selon que la valeur est trop petite ou trop grande.

<Listing number="11-9" file-name="src/lib.rs" caption="Tester un `panic!` avec un message de panique contenant une sous-chaîne spécifiée">

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-09/src/lib.rs:here}}
```

</Listing>

Ce test réussira car la valeur que nous avons placée dans le paramètre `expected` de l'attribut `should_panic` est une sous-chaîne du message avec lequel la fonction `Guess::new` panique. Nous aurions pu spécifier l'intégralité du message de panique que nous attendons, qui dans ce cas serait `Guess value must be less than or equal to 100, got 200`. Ce que vous choisissez de spécifier dépend de la quantité de message de panique qui est unique ou dynamique et de la précision que vous souhaitez que votre test ait. Dans ce cas, une sous-chaîne du message de panique est suffisante pour garantir que le code dans la fonction de test exécute le cas `else if value > 100`.

Pour voir ce qui se passe lorsqu'un test `should_panic` ayant un message `expected` échoue, introduisons à nouveau un bug dans notre code en échangeant les corps des blocs `if value < 1` et `else if value > 100` :

```rust,ignore,not_desired_behavior
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-09-guess-with-panic-msg-bug/src/lib.rs:here}}
```

Cette fois, lorsque nous exécutons le test `should_panic`, il échouera :

```console
{{#include ../listings/ch11-writing-automated-tests/no-listing-09-guess-with-panic-msg-bug/output.txt}}
```

Le message d'échec indique que ce test a bien paniqué comme nous nous y attendions, mais le message de panique n'incluait pas la chaîne attendue `less than or equal to 100`. Le message de panique que nous avons obtenu dans ce cas était `Guess value must be greater than or equal to 1, got 200`. Maintenant nous pouvons commencer à comprendre où se trouve notre bug !

### Utilisation de `Result<T, E>` dans les Tests

Tous nos tests jusqu'à présent ont paniqué quand ils échouaient. Nous pouvons également écrire des tests qui utilisent `Result<T, E>` ! Voici le test de l'Listing 11-1, réécrit pour utiliser `Result<T, E>` et retourner un `Err` au lieu de paniquer :

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-10-result-in-tests/src/lib.rs:here}}
```

La fonction `it_works` a maintenant le type de retour `Result<(), String>`. Dans le corps de la fonction, plutôt que d'appeler la macro `assert_eq!`, nous retournons `Ok(())` lorsque le test réussit et un `Err` avec une `String` à l'intérieur lorsque le test échoue.

Écrire des tests de manière à ce qu'ils retournent un `Result<T, E>` vous permet d'utiliser l'opérateur point d'interrogation dans le corps des tests, ce qui peut être un moyen pratique d'écrire des tests qui devraient échouer si une opération dans ceux-ci retourne un variant `Err`.

Vous ne pouvez pas utiliser l'annotation `#[should_panic]` sur des tests qui utilisent `Result<T, E>`. Pour affirmer qu'une opération retourne un variant `Err`, _n'utilisez pas_ l'opérateur point d'interrogation sur la valeur `Result<T, E>`. Utilisez plutôt `assert!(value.is_err())`.

Maintenant que vous connaissez plusieurs manières d'écrire des tests, examinons ce qui se passe lorsque nous exécutons nos tests et explorons les différentes options que nous pouvons utiliser avec `cargo test`.

[concatenating]: ch08-02-strings.html#concatenating-with--or-format
[bench]: ../unstable-book/library-features/test.html
[ignoring]: ch11-02-running-tests.html#ignoring-tests-unless-specifically-requested
[subset]: ch11-02-running-tests.html#running-a-subset-of-tests-by-name
[controlling-how-tests-are-run]: ch11-02-running-tests.html#controlling-how-tests-are-run
[derivable-traits]: appendix-03-derivable-traits.html
[doc-comments]: ch14-02-publishing-to-crates-io.html#documentation-comments-as-tests
[paths-for-referring-to-an-item-in-the-module-tree]: ch07-03-paths-for-referring-to-an-item-in-the-module-tree.html