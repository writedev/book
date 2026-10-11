## Comment écrire des tests

Les _tests_ sont des fonctions Rust qui vérifient que le code qui n’est pas destiné aux tests fonctionne comme prévu. Le corps des fonctions de test effectue généralement les trois actions suivantes :

- Préparer les données ou l’état nécessaires.
- Exécuter le code que vous souhaitez tester.
- Vérifier que les résultats correspondent à vos attentes.

Examinons les fonctionnalités que Rust fournit spécialement pour écrire des tests qui effectuent ces actions, notamment l’attribut `test`, quelques macros et l’attribut `should_panic`.

<!-- Old headings. Do not remove or links may break. -->

<a id="the-anatomy-of-a-test-function"></a>

### Structurer les fonctions de test

Dans sa forme la plus simple, un test en Rust est une fonction annotée avec l’attribut `test`. Les attributs sont des métadonnées associées à des éléments de code Rust ; l’attribut `derive`, que nous avons utilisé avec les structures au chapitre 5, en est un exemple. Pour transformer une fonction en fonction de test, ajoutez `#[test]` sur la ligne précédant `fn`. Lorsque vous exécutez vos tests avec la commande `cargo test`, Rust crée un exécutable de test qui lance les fonctions annotées et indique si chacune d’elles réussit ou échoue.

Chaque fois que nous créons un nouveau projet de bibliothèque avec Cargo, un module de test contenant une fonction de test est automatiquement généré. Ce module vous fournit un modèle pour écrire vos tests, afin que vous n’ayez pas à rechercher la structure et la syntaxe exactes chaque fois que vous démarrez un nouveau projet. Vous pouvez ajouter autant de fonctions de test et de modules de test que vous le souhaitez !

Nous allons découvrir certains aspects du fonctionnement des tests en expérimentant avec le test modèle avant de tester du code. Ensuite, nous écrirons des tests concrets qui appellent du code que nous avons écrit et vérifient que son comportement est correct.

Créons un nouveau projet de bibliothèque appelé `adder` qui additionnera deux nombres :

```console
$ cargo new adder --lib
     Created library `adder` project
$ cd adder
```

Le contenu du fichier _src/lib.rs_ de votre bibliothèque `adder` devrait ressembler à celui de la liste 11-1.

<Listing number="11-1" file-name="src/lib.rs" caption="Le code généré automatiquement par `cargo new`">

<!-- manual-regeneration
cd listings/ch11-writing-automated-tests
rm -rf listing-11-01
cargo new listing-11-01 --lib --name adder
cd listing-11-01
echo "$ cargo test" > output.txt
RUSTFLAGS="-A unused_variables -A dead_code" RUST_TEST_THREADS=1 cargo test >> output.txt 2>&1
git diff output.txt # commit any relevant changes; discard irrelevant ones
cd ../../..
-->

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-01/src/lib.rs}}
```

</Listing>

Le fichier commence par un exemple de fonction `add`, afin que nous ayons quelque chose à tester.

Pour l’instant, concentrons-nous uniquement sur la fonction `it_works`. Remarquez l’annotation `#[test]` : cet attribut indique qu’il s’agit d’une fonction de test, afin que le lanceur de tests sache qu’il doit la traiter comme telle. Le module `tests` peut également contenir des fonctions qui ne sont pas des tests, pour nous aider à préparer des scénarios courants ou à effectuer des opérations courantes ; nous devons donc toujours indiquer quelles fonctions sont des tests.

Le corps de la fonction d’exemple utilise la macro `assert_eq!` pour vérifier que `result`, qui contient le résultat de l’appel à `add` avec 2 et 2, est égal à 4. Cette assertion illustre la forme habituelle d’un test. Exécutons-la pour vérifier que le test réussit.

La commande `cargo test` exécute tous les tests de notre projet, comme le montre la liste 11-2.

<Listing number="11-2" caption="La sortie de l’exécution du test généré automatiquement">

```console
{{#include ../listings/ch11-writing-automated-tests/listing-11-01/output.txt}}
```

</Listing>

Cargo a compilé et exécuté le test. Nous voyons la ligne `running 1 test`. La ligne suivante indique le nom de la fonction de test générée, `tests::it_works`, et précise que le résultat de son exécution est `ok`. Le résumé général `test result: ok.` signifie que tous les tests ont réussi, et la partie `1 passed; 0 failed` donne le nombre total de tests réussis ou échoués.

Il est possible d’ignorer un test afin qu’il ne soit pas exécuté lors d’une exécution donnée ; nous aborderons ce sujet plus loin dans ce chapitre, dans la section [« Ignorer les tests sauf demande explicite »][ignoring]<!-- ignore -->. Comme nous ne l’avons pas fait ici, le résumé indique `0 ignored`. Nous pouvons également transmettre un argument à la commande `cargo test` pour n’exécuter que les tests dont le nom correspond à une chaîne de caractères ; cette opération s’appelle le _filtrage_, et nous l’aborderons dans la section [« Exécuter un sous-ensemble de tests par nom »][subset]<!-- ignore -->. Ici, nous n’avons pas filtré les tests exécutés ; la fin du résumé indique donc `0 filtered out`.

La statistique `0 measured` concerne les tests de performance, qui mesurent les performances. Au moment de la rédaction, les tests de performance ne sont disponibles que dans Rust nightly. Consultez [la documentation sur les tests de performance][bench] pour en savoir plus.

La partie suivante de la sortie, qui commence par `Doc-tests adder`, concerne les résultats des tests de documentation. Nous n’en avons pas encore, mais Rust peut compiler les exemples de code qui apparaissent dans la documentation de notre API. Cette fonctionnalité permet de garder votre documentation et votre code synchronisés ! Nous expliquerons comment écrire des tests de documentation dans la section [« Les commentaires de documentation comme tests »][doc-comments]<!-- ignore --> du chapitre 14. Pour l’instant, nous ignorerons la sortie `Doc-tests`.

Commençons à adapter le test à nos besoins. Tout d’abord, remplacez le nom de la fonction `it_works` par un autre nom, comme `exploration`, de la manière suivante :

<span class="filename">Nom du fichier : src/lib.rs</span>

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-01-changing-test-name/src/lib.rs}}
```

Ensuite, exécutez à nouveau `cargo test`. La sortie affiche maintenant `exploration` au lieu de `it_works` :

```console
{{#include ../listings/ch11-writing-automated-tests/no-listing-01-changing-test-name/output.txt}}
```

Ajoutons maintenant un autre test, mais cette fois, créons-en un qui échoue ! Les tests échouent lorsqu’un élément de la fonction de test provoque une panique. Chaque test est exécuté dans un nouveau thread, et lorsque le thread principal constate qu’un thread de test s’est arrêté, le test est marqué comme ayant échoué. Au chapitre 9, nous avons vu que la façon la plus simple de provoquer une panique est d’appeler la macro `panic!`. Ajoutez le nouveau test sous la forme d’une fonction nommée `another`, afin que votre fichier _src/lib.rs_ ressemble à la liste 11-3.

<Listing number="11-3" file-name="src/lib.rs" caption="Ajout d’un second test qui échouera, car nous appelons la macro `panic!`">

```rust,panics,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-03/src/lib.rs}}
```

</Listing>

Exécutez à nouveau les tests avec `cargo test`. La sortie devrait ressembler à celle de la liste 11-4, qui montre que notre test `exploration` a réussi et que `another` a échoué.

<Listing number="11-4" caption="Résultats des tests lorsqu’un test réussit et qu’un autre échoue">

```console
{{#include ../listings/ch11-writing-automated-tests/listing-11-03/output.txt}}
```

</Listing>

<!-- manual-regeneration
rg panicked listings/ch11-writing-automated-tests/listing-11-03/output.txt
check the line number of the panic matches the line number in the following paragraph
 -->

Au lieu de `ok`, la ligne `test tests::another` affiche `FAILED`. Deux nouvelles sections apparaissent entre les résultats individuels et le résumé : la première détaille la raison de l’échec de chaque test. Dans ce cas, nous apprenons que `tests::another` a échoué parce qu’il a provoqué une panique avec le message `Make this test fail` à la ligne 17 du fichier _src/lib.rs_. La section suivante ne répertorie que les noms des tests qui ont échoué, ce qui est utile lorsque de nombreux tests échouent et que leurs sorties détaillées sont nombreuses. Nous pouvons utiliser le nom d’un test ayant échoué pour n’exécuter que celui-ci et faciliter le débogage ; nous parlerons plus en détail des façons d’exécuter les tests dans la section [« Contrôler l’exécution des tests »][controlling-how-tests-are-run]<!-- ignore -->.

La ligne de résumé apparaît à la fin : dans l’ensemble, le résultat de nos tests est `FAILED`. Un test a réussi et un test a échoué.

Maintenant que vous avez vu à quoi ressemblent les résultats des tests dans différents cas, examinons quelques macros autres que `panic!` qui sont utiles dans les tests.

<!-- Old headings. Do not remove or links may break. -->

<a id="checking-results-with-the-assert-macro"></a>

### Vérifier les résultats avec `assert!`

La macro `assert!`, fournie par la bibliothèque standard, est utile lorsque vous souhaitez vous assurer qu’une condition donnée dans un test s’évalue à `true`. Nous lui transmettons un argument qui s’évalue en une valeur booléenne. Si cette valeur est `true`, rien ne se passe et le test réussit. Si elle est `false`, la macro `assert!` appelle `panic!` pour provoquer l’échec du test. L’utilisation de la macro `assert!` nous aide à vérifier que notre code fonctionne comme prévu.

Au chapitre 5, dans la liste 5-15, nous avons utilisé une structure `Rectangle` et une méthode `can_hold`, que nous reprenons ici dans la liste 11-5. Plaçons ce code dans le fichier _src/lib.rs_, puis écrivons quelques tests à l’aide de la macro `assert!`.

<Listing number="11-5" file-name="src/lib.rs" caption="La structure `Rectangle` et sa méthode `can_hold` du chapitre 5">

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-05/src/lib.rs}}
```

</Listing>

La méthode `can_hold` renvoie une valeur booléenne ; elle se prête donc parfaitement à l’utilisation de la macro `assert!`. Dans la liste 11-6, nous écrivons un test qui vérifie la méthode `can_hold` en créant une instance de `Rectangle` d’une largeur de 8 et d’une hauteur de 7, puis en vérifiant qu’elle peut contenir une autre instance de `Rectangle` d’une largeur de 5 et d’une hauteur de 1.

<Listing number="11-6" file-name="src/lib.rs" caption="Un test de `can_hold` qui vérifie qu’un rectangle plus grand peut effectivement contenir un rectangle plus petit">

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-06/src/lib.rs:here}}
```

</Listing>

Remarquez la ligne `use super::*;` dans le module `tests`. Le module `tests` est un module ordinaire qui suit les règles de visibilité habituelles, abordées au chapitre 7 dans la section [« Chemins permettant de désigner un élément dans l’arborescence des modules »][paths-for-referring-to-an-item-in-the-module-tree]<!-- ignore -->. Comme le module `tests` est un module interne, nous devons rendre le code testé, qui se trouve dans le module externe, accessible dans le module interne. Nous utilisons ici une importation globale ; tout ce que nous définissons dans le module externe est donc accessible depuis ce module `tests`.

Nous avons nommé notre test `larger_can_hold_smaller` et créé les deux instances de `Rectangle` dont nous avons besoin. Ensuite, nous avons appelé la macro `assert!` en lui transmettant le résultat de l’appel à `larger.can_hold(&smaller)`. Cette expression est censée renvoyer `true` ; notre test devrait donc réussir. Vérifions cela !

```console
{{#include ../listings/ch11-writing-automated-tests/listing-11-06/output.txt}}
```

Le test réussit ! Ajoutons-en un autre, qui vérifie cette fois qu’un rectangle plus petit ne peut pas contenir un rectangle plus grand :

<span class="filename">Nom du fichier : src/lib.rs</span>

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-02-adding-another-rectangle-test/src/lib.rs:here}}
```

Comme le résultat correct de la fonction `can_hold` est `false` dans ce cas, nous devons nier ce résultat avant de le transmettre à la macro `assert!`. Notre test réussira donc si `can_hold` renvoie `false` :

```console
{{#include ../listings/ch11-writing-automated-tests/no-listing-02-adding-another-rectangle-test/output.txt}}
```

Deux tests réussis ! Voyons maintenant ce qui arrive aux résultats de nos tests lorsque nous introduisons un bogue dans notre code. Nous allons modifier l’implémentation de la méthode `can_hold` en remplaçant le signe supérieur à (`>`) par un signe inférieur à (`<`) lors de la comparaison des largeurs :

```rust,not_desired_behavior,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-03-introducing-a-bug/src/lib.rs:here}}
```

L’exécution des tests produit maintenant le résultat suivant :

```console
{{#include ../listings/ch11-writing-automated-tests/no-listing-03-introducing-a-bug/output.txt}}
```

Nos tests ont détecté le bogue ! Comme `larger.width` vaut `8` et `smaller.width` vaut `5`, la comparaison des largeurs dans `can_hold` renvoie maintenant `false` : 8 n’est pas inférieur à 5.

<!-- Old headings. Do not remove or links may break. -->

<a id="testing-equality-with-the-assert_eq-and-assert_ne-macros"></a>

### Tester l’égalité avec `assert_eq!` et `assert_ne!`

Une façon courante de vérifier le fonctionnement consiste à tester l’égalité entre le résultat du code testé et la valeur que l’on s’attend à obtenir. On pourrait le faire à l’aide de la macro `assert!` en lui transmettant une expression utilisant l’opérateur `==`. Cependant, ce type de test est si courant que la bibliothèque standard fournit deux macros, `assert_eq!` et `assert_ne!`, qui permettent d’effectuer cette vérification plus facilement. Ces macros comparent respectivement deux arguments afin de vérifier leur égalité ou leur inégalité. Elles affichent également les deux valeurs si l’assertion échoue, ce qui permet de mieux comprendre _pourquoi_ le test a échoué ; à l’inverse, la macro `assert!` indique seulement que l’expression `==` a renvoyé `false`, sans afficher les valeurs à l’origine de ce résultat.

Dans la liste 11-7, nous écrivons une fonction nommée `add_two` qui ajoute `2` à son paramètre, puis nous testons cette fonction à l’aide de la macro `assert_eq!`.

<Listing number="11-7" file-name="src/lib.rs" caption="Tester la fonction `add_two` à l’aide de la macro `assert_eq!`">

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-07/src/lib.rs}}
```

</Listing>

Vérifions que le test réussit !

```console
{{#include ../listings/ch11-writing-automated-tests/listing-11-07/output.txt}}
```

Nous créons une variable nommée `result` qui contient le résultat de l’appel à `add_two(2)`. Puis nous transmettons `result` et `4` comme arguments à la macro `assert_eq!`. La ligne de sortie de ce test est `test tests::it_adds_two ... ok`, et le texte `ok` indique que notre test a réussi !

Introduisons un bogue dans notre code pour voir à quoi ressemble `assert_eq!` lorsqu’un test échoue. Modifiez l’implémentation de la fonction `add_two` pour qu’elle ajoute plutôt `3` :

```rust,not_desired_behavior,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-04-bug-in-add-two/src/lib.rs:here}}
```

Exécutez à nouveau les tests :

```console
{{#include ../listings/ch11-writing-automated-tests/no-listing-04-bug-in-add-two/output.txt}}
```

Notre test a détecté le bogue ! Le test `tests::it_adds_two` a échoué, et le message nous indique que l’assertion qui a échoué était `left == right`, ainsi que les valeurs de `left` et `right`. Ce message nous aide à commencer le débogage : l’argument `left`, qui contenait le résultat de l’appel à `add_two(2)`, valait `5`, tandis que l’argument `right` valait `4`. On peut imaginer à quel point cela serait utile si nous avions beaucoup de tests.

Notez que, dans certains langages et frameworks de test, les paramètres des fonctions d’assertion d’égalité s’appellent `expected` et `actual`, et que l’ordre dans lequel on spécifie les arguments est important. En Rust, toutefois, ils s’appellent `left` et `right`, et l’ordre dans lequel on indique la valeur attendue et celle produite par le code n’a pas d’importance. Nous pourrions écrire l’assertion de ce test sous la forme `assert_eq!(4, result)`, ce qui produirait le même message d’échec affichant `` assertion `left == right` failed ``.

La macro `assert_ne!` réussit si les deux valeurs que nous lui transmettons sont différentes et échoue si elles sont égales. Elle est surtout utile lorsqu’on ne sait pas quelle sera la valeur, mais que l’on sait avec certitude ce qu’elle ne _doit pas_ être. Par exemple, si nous testons une fonction qui garantit de modifier son entrée d’une manière ou d’une autre, mais que la façon dont cette entrée est modifiée dépend du jour de la semaine où nous exécutons les tests, il peut être préférable de vérifier que la sortie de la fonction n’est pas égale à l’entrée.

En interne, les macros `assert_eq!` et `assert_ne!` utilisent respectivement les opérateurs `==` et `!=`. Lorsque les assertions échouent, ces macros affichent leurs arguments en utilisant le formatage de débogage ; les valeurs comparées doivent donc implémenter les traits `PartialEq` et `Debug`. Tous les types primitifs et la plupart des types de la bibliothèque standard implémentent ces traits. Pour les structures et les énumérations que vous définissez vous-même, vous devrez implémenter `PartialEq` pour vérifier l’égalité de ces types. Vous devrez également implémenter `Debug` pour afficher les valeurs en cas d’échec de l’assertion. Comme ces deux traits peuvent être dérivés, comme nous l’avons mentionné dans la liste 5-12 au chapitre 5, il suffit généralement d’ajouter l’annotation `#[derive(PartialEq, Debug)]` à la définition de votre structure ou de votre énumération. Consultez l’annexe C, [« Traits pouvant être dérivés »][derivable-traits]<!-- ignore -->, pour en savoir plus sur ces traits et sur les autres traits pouvant être dérivés.

### Ajouter des messages d’échec personnalisés

Vous pouvez également ajouter un message personnalisé à afficher en cas d’échec en transmettant des arguments facultatifs aux macros `assert!`, `assert_eq!` et `assert_ne!`. Tous les arguments spécifiés après les arguments obligatoires sont transmis à la macro `format!` (abordée dans la section [« Concaténation avec `+` ou `format!` »][concatenating]<!--
ignore --> au chapitre 8). Vous pouvez donc transmettre une chaîne de format contenant des espaces réservés `{}` et les valeurs à y insérer. Les messages personnalisés sont utiles pour expliquer le sens d’une assertion ; si un test échoue, vous comprendrez mieux quel est le problème dans le code.

Par exemple, supposons que nous ayons une fonction qui salue les gens par leur nom et que nous souhaitions vérifier que le nom transmis à la fonction apparaît dans le résultat :

<span class="filename">Nom du fichier : src/lib.rs</span>

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-05-greeter/src/lib.rs}}
```

Les exigences de ce programme n’ont pas encore été convenues, et nous sommes presque certains que le texte `Hello` au début du message de salutation va changer. Nous avons décidé de ne pas vouloir mettre à jour le test à chaque changement des exigences ; au lieu de vérifier l’égalité exacte avec la valeur renvoyée par la fonction `greeting`, nous allons simplement vérifier que la sortie contient le texte du paramètre d’entrée.

Introduisons maintenant un bogue dans ce code en modifiant `greeting` pour qu’elle n’inclue pas `name`, afin de voir à quoi ressemble le message d’échec par défaut :

```rust,not_desired_behavior,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-06-greeter-with-bug/src/lib.rs:here}}
```

L’exécution de ce test produit le résultat suivant :

```console
{{#include ../listings/ch11-writing-automated-tests/no-listing-06-greeter-with-bug/output.txt}}
```

Ce résultat indique seulement que l’assertion a échoué et à quelle ligne elle se trouve. Un message d’échec plus utile afficherait la valeur renvoyée par la fonction `greeting`. Ajoutons un message d’échec personnalisé, composé d’une chaîne de format contenant un espace réservé rempli avec la valeur effectivement obtenue de la fonction `greeting` :

```rust,ignore
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-07-custom-failure-message/src/lib.rs:here}}
```

Lorsque nous exécuterons le test, nous obtiendrons maintenant un message d’erreur plus informatif :

```console
{{#include ../listings/ch11-writing-automated-tests/no-listing-07-custom-failure-message/output.txt}}
```

Nous pouvons voir dans la sortie du test la valeur réellement obtenue, ce qui nous aidera à comprendre ce qui s’est passé plutôt que ce que nous nous attendions à voir.

### Vérifier les paniques avec `should_panic`

En plus de vérifier les valeurs renvoyées, il est important de vérifier que notre code gère les erreurs comme prévu. Prenons, par exemple, le type `Guess` que nous avons créé au chapitre 9, dans la liste 9-13. Le code qui utilise `Guess` s’appuie sur la garantie que les instances de `Guess` ne contiennent que des valeurs comprises entre 1 et 100. Nous pouvons écrire un test qui vérifie que la tentative de créer une instance de `Guess` avec une valeur en dehors de cette plage provoque une panique.

Pour cela, nous ajoutons l’attribut `should_panic` à notre fonction de test. Le test réussit si le code de la fonction provoque une panique ; il échoue si le code ne provoque pas de panique.

La liste 11-8 présente un test qui vérifie que les conditions d’erreur de `Guess::new` se produisent lorsque nous l’attendons.

<Listing number="11-8" file-name="src/lib.rs" caption="Vérifier qu’une condition provoque un `panic!`">

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-08/src/lib.rs}}
```

</Listing>

Nous plaçons l’attribut `#[should_panic]` après l’attribut `#[test]` et avant la fonction de test à laquelle il s’applique. Voyons le résultat lorsque ce test réussit :

```console
{{#include ../listings/ch11-writing-automated-tests/listing-11-08/output.txt}}
```

Tout semble correct ! Introduisons maintenant un bogue dans notre code en supprimant la condition selon laquelle la fonction `new` provoque une panique si la valeur est supérieure à 100 :

```rust,not_desired_behavior,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-08-guess-with-bug/src/lib.rs:here}}
```

Lorsque nous exécutons le test de la liste 11-8, il échoue :

```console
{{#include ../listings/ch11-writing-automated-tests/no-listing-08-guess-with-bug/output.txt}}
```

Dans ce cas, le message n’est pas très utile, mais en examinant la fonction de test, nous voyons qu’elle est annotée avec `#[should_panic]`. L’échec signifie que le code de la fonction de test n’a pas provoqué de panique.

Les tests qui utilisent `should_panic` peuvent manquer de précision. Un test `should_panic` réussirait même si la panique était provoquée pour une raison différente de celle attendue. Pour rendre ces tests plus précis, nous pouvons ajouter un paramètre facultatif `expected` à l’attribut `should_panic`. Le banc d’essai vérifiera alors que le message d’échec contient le texte fourni. Prenons, par exemple, le code modifié de `Guess` dans la liste 11-9, où la fonction `new` provoque une panique avec des messages différents selon que la valeur est trop petite ou trop grande.

<Listing number="11-9" file-name="src/lib.rs" caption="Vérifier qu’un `panic!` survient avec un message contenant une sous-chaîne spécifiée">

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-09/src/lib.rs:here}}
```

</Listing>

Ce test réussira, car la valeur que nous avons placée dans le paramètre `expected` de l’attribut `should_panic` est une sous-chaîne du message provoqué par la panique de la fonction `Guess::new`. Nous aurions pu indiquer le message de panique complet attendu, qui serait dans ce cas `Guess value must be less than or equal to 100, got 200`. Le choix dépend de la part du message de panique qui est unique ou variable, ainsi que du degré de précision souhaité pour le test. Ici, une sous-chaîne du message de panique suffit à vérifier que le code de la fonction de test exécute le cas `else if value > 100`.

Pour voir ce qui se passe lorsqu’un test `should_panic` avec un message `expected` échoue, introduisons à nouveau un bogue dans notre code en permutant les corps des blocs `if value < 1` et `else if value > 100` :

```rust,ignore,not_desired_behavior
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-09-guess-with-panic-msg-bug/src/lib.rs:here}}
```

Cette fois, lorsque nous exécuterons le test `should_panic`, il échouera :

```console
{{#include ../listings/ch11-writing-automated-tests/no-listing-09-guess-with-panic-msg-bug/output.txt}}
```

Le message d’échec indique que ce test a bien provoqué une panique, comme prévu, mais que le message de panique ne contenait pas la chaîne attendue `less than or equal to 100`. Le message de panique obtenu était `Guess value must be greater than or equal to 1, got 200`. Nous pouvons maintenant chercher l’origine de notre bogue !

### Utiliser `Result<T, E>` dans les tests

Jusqu’à présent, tous nos tests provoquaient une panique en cas d’échec. Nous pouvons aussi écrire des tests qui utilisent `Result<T, E>` ! Voici le test de la liste 11-1, réécrit pour utiliser `Result<T, E>` et renvoyer un `Err` au lieu de provoquer une panique :

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-10-result-in-tests/src/lib.rs:here}}
```

La fonction `it_works` a maintenant le type de retour `Result<(), String>`. Dans le corps de la fonction, au lieu d’appeler la macro `assert_eq!`, nous renvoyons `Ok(())` lorsque le test réussit et un `Err` contenant une `String` lorsqu’il échoue.

Écrire des tests qui renvoient un `Result<T, E>` vous permet d’utiliser l’opérateur point d’interrogation dans leur corps. Cela peut être pratique pour écrire des tests qui doivent échouer si une opération quelconque renvoie une variante `Err`.

Vous ne pouvez pas utiliser l’annotation `#[should_panic]` sur les tests qui utilisent `Result<T, E>`. Pour vérifier qu’une opération renvoie une variante `Err`, _n’utilisez pas_ l’opérateur point d’interrogation sur la valeur `Result<T, E>`. Utilisez plutôt `assert!(value.is_err())`.

Maintenant que vous connaissez plusieurs façons d’écrire des tests, examinons ce qui se passe lorsque nous les exécutons et découvrons les différentes options que nous pouvons utiliser avec `cargo test`.

[concatenating]: ch08-02-strings.html#concatenating-with--or-format
[bench]: ../unstable-book/library-features/test.html
[ignoring]: ch11-02-running-tests.html#ignoring-tests-unless-specifically-requested
[subset]: ch11-02-running-tests.html#running-a-subset-of-tests-by-name
[controlling-how-tests-are-run]: ch11-02-running-tests.html#controlling-how-tests-are-run
[derivable-traits]: appendix-03-derivable-traits.html
[doc-comments]: ch14-02-publishing-to-crates-io.html#documentation-comments-as-tests
[paths-for-referring-to-an-item-in-the-module-tree]: ch07-03-paths-for-referring-to-an-item-in-the-module-tree.html