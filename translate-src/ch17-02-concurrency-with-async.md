<!-- Anciennes en-têtes. Ne pas supprimer ou les liens pourraient être cassés. -->

<a id="concurrency-with-async"></a>

## Appliquer la Concurrence avec Async

Dans cette section, nous allons appliquer async à certains des mêmes défis de concurrence que nous avons abordés avec des threads dans le Chapitre 16. Comme nous avons déjà discuté beaucoup des idées clés là-bas, dans cette section, nous nous concentrerons sur ce qui est différent entre les threads et les futurs.

Dans de nombreux cas, les API pour travailler avec la concurrence en utilisant async sont très similaires à celles des threads. Dans d'autres cas, elles finissent par être assez différentes. Même lorsque les API _ont l'air_ similaires entre les threads et async, elles ont souvent des comportements différents—et elles ont presque toujours des caractéristiques de performance différentes.

<!-- Anciennes en-têtes. Ne pas supprimer ou les liens pourraient être cassés. -->

<a id="counting"></a>

### Créer une Nouvelle Tâche avec `spawn_task`

La première opération que nous avons abordée dans la section [« Créer un Nouveau Thread avec `spawn` »][thread-spawn]<!-- ignore --> du Chapitre 16 était le comptage sur deux threads séparés. Faisons de même en utilisant async. Le crate `trpl` fournit une fonction `spawn_task` qui ressemble beaucoup à l'API `thread::spawn`, et une fonction `sleep` qui est une version async de l'API `thread::sleep`. Nous pouvons utiliser ces deux fonctions pour implémenter l'exemple de comptage, comme le montre la Liste 17-6.

<Listing number="17-6" caption="Créer une nouvelle tâche pour imprimer une chose pendant que la tâche principale imprime autre chose" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-06/src/main.rs:all}}
```

</Listing>

Comme point de départ, nous configurons notre fonction `main` avec `trpl::block_on` afin que notre fonction de niveau supérieur puisse être async.

> Remarque : À partir de ce point dans le chapitre, chaque exemple inclura ce même code d'encapsulage avec `trpl::block_on` dans `main`, nous allons donc souvent l'omettre, tout comme nous le faisons avec `main`. N'oubliez pas de l'inclure dans votre code !

Puis, nous écrivons deux boucles dans ce bloc, chacune contenant un appel à `trpl::sleep`, qui attend une demi-seconde (500 millisecondes) avant d'envoyer le prochain message. Nous mettons une boucle dans le corps d'un `trpl::spawn_task` et l'autre dans une boucle `for` de niveau supérieur. Nous ajoutons également un `await` après les appels `sleep`.

Ce code se comporte de manière similaire à l'implémentation basée sur des threads—y compris le fait que vous pouvez voir les messages apparaître dans un ordre différent dans votre propre terminal lorsque vous l'exécutez :

<!-- Pas d'extraction de la sortie car les modifications à cette sortie ne sont pas significatives ; les changements sont probablement dus à l'exécution différente des threads plutôt qu'à des modifications dans le compilateur -->

```text
salut numéro 1 de la seconde tâche !
salut numéro 1 de la première tâche !
salut numéro 2 de la première tâche !
salut numéro 2 de la seconde tâche !
salut numéro 3 de la première tâche !
salut numéro 3 de la seconde tâche !
salut numéro 4 de la première tâche !
salut numéro 4 de la seconde tâche !
salut numéro 5 de la première tâche !
```

Cette version s'arrête dès que la boucle `for` dans le corps du bloc async principal se termine, car la tâche lancée par `spawn_task` est arrêtée lorsque la fonction `main` se termine. Si vous souhaitez qu'elle s'exécute jusqu'à l'achèvement de la tâche, vous devrez utiliser un handle de jointure pour attendre que la première tâche se termine. Avec des threads, nous avons utilisé la méthode `join` pour « bloquer » jusqu'à ce que le thread ait fini de s'exécuter. Dans la Liste 17-7, nous pouvons utiliser `await` pour faire la même chose, car le handle de la tâche lui-même est un futur. Son type `Output` est un `Result`, nous le déballons également après l'avoir attendu.

<Listing number="17-7" caption="Utiliser `await` avec un handle de jointure pour exécuter une tâche jusqu'à l'achèvement" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-07/src/main.rs:handle}}
```

</Listing>

Cette version mise à jour s'exécute jusqu'à ce que _les deux_ boucles se terminent :

<!-- Pas d'extraction de la sortie car les modifications à cette sortie ne sont pas significatives ; les changements sont probablement dus à l'exécution différente des threads plutôt qu'à des modifications dans le compilateur -->

```text
salut numéro 1 de la seconde tâche !
salut numéro 1 de la première tâche !
salut numéro 2 de la première tâche !
salut numéro 2 de la seconde tâche !
salut numéro 3 de la première tâche !
salut numéro 3 de la seconde tâche !
salut numéro 4 de la première tâche !
salut numéro 4 de la seconde tâche !
salut numéro 5 de la première tâche !
salut numéro 6 de la première tâche !
salut numéro 7 de la première tâche !
salut numéro 8 de la première tâche !
salut numéro 9 de la première tâche !
```

Jusqu'à présent, il semble que async et les threads nous donnent des résultats similaires, juste avec une syntaxe différente : utiliser `await` au lieu d'appeler `join` sur le handle de jointure, et attendre les appels `sleep`.

La plus grande différence est que nous n'avons pas eu besoin de lancer un autre thread du système d'exploitation pour faire cela. En fait, nous n'avons même pas besoin d'initier une tâche ici. Comme les blocs async se compilent en futures anonymes, nous pouvons mettre chaque boucle dans un bloc async et laisser le runtime les exécuter toutes deux jusqu'à l'achèvement en utilisant la fonction `trpl::join`.

Dans la section [« Attendre que Tous les Threads Finissent »][join-handles]<!-- ignore --> du Chapitre 16, nous avons montré comment utiliser la méthode `join` sur le type `JoinHandle` retourné lors de l'appel de `std::thread::spawn`. La fonction `trpl::join` est similaire, mais pour des futurs. Lorsque vous lui donnez deux futurs, elle produit un nouveau futur unique dont la sortie est un tuple contenant la sortie de chaque futur que vous lui avez passé une fois qu'ils _deux_ se terminent. Ainsi, dans la Liste 17-8, nous utilisons `trpl::join` pour attendre que `fut1` et `fut2` se terminent. Nous ne faisons _pas_ attendre `fut1` et `fut2`, mais plutôt le nouveau futur produit par `trpl::join`. Nous ignorons la sortie, car c'est juste un tuple contenant deux valeurs unitaires.

<Listing number="17-8" caption="Utiliser `trpl::join` pour attendre deux futurs anonymes" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-08/src/main.rs:join}}
```

</Listing>

Lorsque nous exécutons cela, nous voyons les deux futurs s'exécuter jusqu'à l'achèvement :

<!-- Pas d'extraction de la sortie car les modifications à cette sortie ne sont pas significatives ; les changements sont probablement dus à l'exécution différente des threads plutôt qu'à des modifications dans le compilateur -->

```text
salut numéro 1 de la première tâche !
salut numéro 1 de la seconde tâche !
salut numéro 2 de la première tâche !
salut numéro 2 de la seconde tâche !
salut numéro 3 de la première tâche !
salut numéro 3 de la seconde tâche !
salut numéro 4 de la première tâche !
salut numéro 4 de la seconde tâche !
salut numéro 5 de la première tâche !
salut numéro 6 de la première tâche !
salut numéro 7 de la première tâche !
salut numéro 8 de la première tâche !
salut numéro 9 de la première tâche !
```

Maintenant, vous verrez le même ordre exact à chaque fois, ce qui est très différent de ce que nous avons vu avec des threads et avec `trpl::spawn_task` dans la Liste 17-7. Cela est dû au fait que la fonction `trpl::join` est _équitable_, ce qui signifie qu'elle vérifie chaque futur de manière équitable souvent, alternant entre eux, et ne permet jamais à l'un de prendre de l'avance si l'autre est prêt. Avec des threads, le système d'exploitation décide quel thread vérifier et combien de temps le laisser s'exécuter. Avec async Rust, le runtime décide quelle tâche vérifier. (En pratique, les détails se compliquent car un runtime async peut utiliser des threads du système d'exploitation en arrière-plan dans le cadre de la gestion de la concurrence, donc garantir l'équité peut demander plus de travail pour un runtime—mais c'est tout de même possible !) Les runtimes n'ont pas à garantir l'équité pour une opération donnée, et ils offrent souvent différentes API pour vous permettre de choisir si vous voulez ou non l'équité.

Essayez certaines de ces variations sur l'attente des futurs et voyez ce qu'elles font :

- Supprimez le bloc async autour de l'une ou l'autre des boucles.
- Attendez chaque bloc async immédiatement après l'avoir défini.
- Enveloppez uniquement la première boucle dans un bloc async et attendez le futur résultant après le corps de la seconde boucle.

Pour un défi supplémentaire, essayez de deviner quel sera la sortie dans chaque cas _avant_ d'exécuter le code !

<!-- Anciennes en-têtes. Ne pas supprimer ou les liens pourraient être cassés. -->

<a id="message-passing"></a>
<a id="counting-up-on-two-tasks-using-message-passing"></a>

### Envoyer des Données Entre Deux Tâches en Utilisant le Passage de Messages

Partager des données entre des futurs sera également familier : nous allons utiliser à nouveau le passage de messages, mais cette fois avec les versions async des types et des fonctions. Nous allons suivre un chemin légèrement différent de celui que nous avons emprunté dans la section [« Transférer des Données Entre des Threads avec le Passage de Messages »][message-passing-threads]<!-- ignore --> dans le Chapitre 16 pour illustrer certaines des principales différences entre la concurrence basée sur les threads et celle basée sur les futurs. Dans la Liste 17-9, nous allons commencer avec un seul bloc async—_sans_ initier une tâche séparée comme nous avons initié un thread séparé.

<Listing number="17-9" caption="Créer un canal async et assigner les deux moitiés à `tx` et `rx`" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-09/src/main.rs:channel}}
```

</Listing>

Ici, nous utilisons `trpl::channel`, une version async de l'API de canal à producteurs multiples et consommateurs uniques que nous avons utilisée avec des threads dans le Chapitre 16. La version async de l'API est seulement un peu différente de la version basée sur les threads : elle utilise un récepteur mutable plutôt qu'imutable `rx`, et sa méthode `recv` produit un futur que nous devons attendre plutôt que de produire la valeur directement. Maintenant, nous pouvons envoyer des messages de l'expéditeur au récepteur. Remarquez que nous n'avons pas besoin de lancer un thread ou même une tâche séparée ; nous avons simplement besoin d'attendre l'appel `rx.recv`.

La méthode `Receiver::recv` synchrone dans `std::mpsc::channel` bloque jusqu'à ce qu'elle reçoive un message. La méthode `trpl::Receiver::recv` ne bloque pas, car elle est async. Au lieu de bloquer, elle rend le contrôle au runtime jusqu'à ce qu'un message soit reçu ou que le côté d'envoi du canal se ferme. En revanche, nous n'attendons pas l'appel `send`, car il ne bloque pas. Il n'a pas besoin de le faire, car le canal dans lequel nous l'envoyons est illimité.

> Remarque : Parce que tout ce code async s'exécute dans un bloc async dans un appel à `trpl::block_on`, tout ce qui s'y trouve peut éviter de bloquer. Cependant, le code _en dehors_ blockera le retour de la fonction `block_on`. C'est tout l'intérêt de la fonction `trpl::block_on` : elle vous permet de _choisir_ où bloquer sur un ensemble de code async, et donc où faire la transition entre le code synchrone et async.

Remarquez deux choses à propos de cet exemple. Tout d'abord, le message arrivera tout de suite. Deuxièmement, bien que nous utilisions un futur ici, il n'y a pas encore de concurrence. Tout dans la liste se produit de manière séquentielle, tout comme cela le ferait s'il n'y avait pas de futurs impliqués.

Abordons la première partie en envoyant une série de messages et en dormant entre eux, comme le montre la Liste 17-10.

<!-- Nous ne pouvons pas tester celui-ci parce qu'il ne s'arrête jamais ! -->

<Listing number="17-10" caption="Envoyer et recevoir plusieurs messages sur le canal async et dormir avec un `await` entre chaque message" file-name="src/main.rs">

```rust,ignore
{{#rustdoc_include ../listings/ch17-async-await/listing-17-10/src/main.rs:many-messages}}
```

</Listing>

En plus d'envoyer les messages, nous devons les recevoir. Dans ce cas, comme nous savons combien de messages arrivent, nous pourrions le faire manuellement en appelant `rx.recv().await` quatre fois. Dans la vraie vie, cependant, nous attendrons généralement un nombre _inconnu_ de messages, donc nous devons continuer à attendre jusqu'à ce que nous déterminions qu'il n'y a plus de messages.

Dans la Liste 16-10, nous avons utilisé une boucle `for` pour traiter tous les éléments reçus d'un canal synchrone. Rust n'a pas encore de façon d'utiliser une boucle `for` avec une série d'items _produits de manière asynchrone_, cependant, donc nous devons utiliser une boucle que nous n'avons pas encore vue : la boucle conditionnelle `while let`. C'est la version boucle de la construction `if let` que nous avons vue dans la section [« Flux de Contrôle Concis avec `if let` et `let...else` »][if-let]<!-- ignore --> dans le Chapitre 6. La boucle continuera à s'exécuter tant que le modèle qu'elle spécifie continue à correspondre à la valeur.

L'appel `rx.recv` produit un futur, que nous attendons. Le runtime mettra la pause dans le futur jusqu'à ce qu'il soit prêt. Une fois qu'un message arrive, le futur se résoudra en `Some(message)` autant de fois qu'un message arrive. Lorsque le canal se ferme, peu importe si _des_ messages sont arrivés, le futur se résoudra plutôt en `None` pour indiquer qu'il n'y a plus de valeurs et donc que nous devrions arrêter de vérifier—c'est-à-dire, arrêter d'attendre.

La boucle `while let` regroupe tout cela. Si le résultat de l'appel `rx.recv().await` est `Some(message)`, nous avons accès au message et nous pouvons l'utiliser dans le corps de la boucle, tout comme nous pourrions le faire avec `if let`. Si le résultat est `None`, la boucle se termine. Chaque fois que la boucle se termine, elle atteint à nouveau le point d'attente, donc le runtime la met à nouveau en pause jusqu'à ce qu'un autre message arrive.

Le code envoie maintenant et reçoit avec succès tous les messages. Malheureusement, il y a encore quelques problèmes. D'une part, les messages n'arrivent pas à des intervalles de demi-seconde. Ils arrivent tous d'un coup, 2 secondes (2 000 millisecondes) après le démarrage du programme. D'autre part, ce programme ne se termine également jamais ! Au lieu de cela, il attend indéfiniment de nouveaux messages. Vous devrez le fermer en utilisant <kbd>ctrl</kbd>-<kbd>C</kbd>.

#### Le Code Dans Un Bloc Async S'exécute Linéairement

Commençons par examiner pourquoi les messages arrivent tous d'un coup après le délai complet, plutôt que d'arriver avec des délais entre chacun. Dans un bloc async donné, l'ordre dans lequel les mots-clés `await` apparaissent dans le code est aussi l'ordre dans lequel ils sont exécutés lorsque le programme s'exécute.

Il n'y a qu'un seul bloc async dans la Liste 17-10, donc tout ce qui s'y trouve s'exécute linéairement. Il n'y a toujours pas de concurrence. Tous les appels `tx.send` se produisent, entrecoupés de tous les appels `trpl::sleep` et leurs points d'attente associés. Ce n'est qu'ensuite que la boucle `while let` a l'occasion de passer par l'un des points d'attente sur les appels `recv`.

Pour obtenir le comportement que nous souhaitons, où le délai de sommeil se produit entre chaque message, nous devons mettre les opérations `tx` et `rx` dans leurs propres blocs async, comme le montre la Liste 17-11. Ensuite, le runtime peut exécuter chacune d'entre elles séparément en utilisant `trpl::join`, tout comme dans la Liste 17-8. Encore une fois, nous attendons le résultat de l'appel à `trpl::join`, pas les futurs individuels. Si nous attendions les futurs individuels en séquence, nous nous retrouverions simplement en flux séquentiel—exactement ce que nous essayons _de ne pas_ faire.

<!-- Nous ne pouvons pas tester celui-ci parce qu'il ne s'arrête jamais ! -->

<Listing number="17-11" caption="Séparer `send` et `recv` dans leurs propres blocs `async` et attendre les futurs pour ces blocs" file-name="src/main.rs">

```rust,ignore
{{#rustdoc_include ../listings/ch17-async-await/listing-17-11/src/main.rs:futures}}
```

</Listing>

Avec le code mis à jour dans la Liste 17-11, les messages sont imprimés à des intervalles de 500 millisecondes, plutôt que tous à la fois après 2 secondes.

#### Déplacer la Propriété Dans Un Bloc Async

Le programme ne se termine toujours pas, cependant, en raison de la manière dont la boucle `while let` interagit avec `trpl::join` :

- Le futur retourné par `trpl::join` ne se termine que lorsque _les deux_ futurs passés à celui-ci se sont terminés.
- Le futur `tx_fut` se termine une fois qu'il a fini de dormir après avoir envoyé le dernier message dans `vals`.
- Le futur `rx_fut` ne se termine pas tant que la boucle `while let` n'est pas terminée.
- La boucle `while let` ne se termine pas tant qu'attendre `rx.recv` ne produit pas `None`.
- Attendre `rx.recv` renverra `None` uniquement une fois que l'autre extrémité du canal est fermée.
- Le canal se fermera uniquement si nous appelons `rx.close` ou lorsque le côté expéditeur, `tx`, est abandonné.
- Nous n'appelons `rx.close` nulle part, et `tx` ne sera pas abandonné tant que le bloc async le plus extérieur passé à `trpl::block_on` ne se termine pas.
- Le bloc ne peut pas se terminer car il est bloqué sur l'achèvement de `trpl::join`, ce qui nous ramène au début de cette liste.

Pour l'instant, le bloc async où nous envoyons les messages _prend seulement_ une référence à `tx` car l'envoi d'un message ne nécessite pas la propriété, mais si nous pouvions _déplacer_ `tx` dans ce bloc async, il serait abandonné une fois ce bloc terminé. Dans la section [« Capturer des Références ou Déplacer la Propriété »][capture-or-move]<!-- ignore --> du Chapitre 13, vous avez appris à utiliser le mot-clé `move` avec des fermetures, et, comme discuté dans la section [« Utiliser des Fermetures `move` avec des Threads »][move-threads]<!-- ignore --> du Chapitre 16, nous devons souvent déplacer des données dans des fermetures lorsque nous travaillons avec des threads. La même dynamique de base s'applique aux blocs async, donc le mot-clé `move` fonctionne avec des blocs async tout comme il le fait avec des fermetures.

Dans la Liste 17-12, nous changeons le bloc utilisé pour envoyer les messages de `async` à `async move`.

<Listing number="17-12" caption="Une révision du code de la Liste 17-11 qui se ferme correctement lorsqu'elle est terminée" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-12/src/main.rs:with-move}}
```

</Listing>

Lorsque nous exécutons _cette_ version du code, elle se termine gracieusement après que le dernier message a été envoyé et reçu. Ensuite, voyons ce qui doit changer pour envoyer des données depuis plus d'un futur.

#### Joindre un Certain Nombre de Futurs avec le Macro `join!`

Ce canal async est également un canal à producteurs multiples, donc nous pouvons appeler `clone` sur `tx` si nous voulons envoyer des messages depuis plusieurs futurs, comme le montre la Liste 17-13.

<Listing number="17-13" caption="Utiliser plusieurs producteurs avec des blocs async" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-13/src/main.rs:here}}
```

</Listing>

Tout d'abord, nous clonons `tx`, créant `tx1` en dehors du premier bloc async. Nous déplaçons `tx1` dans ce bloc tout comme nous l'avons fait auparavant avec `tx`. Ensuite, plus tard, nous déplaçons le `tx` original dans un _nouveau_ bloc async, où nous envoyons plus de messages avec un léger retard. Nous avons la chance de placer ce nouveau bloc async après le bloc async pour recevoir des messages, mais il pourrait tout aussi bien aller avant. La clé est l'ordre dans lequel les futurs sont attendus, non pas dans lequel ils sont créés.

Les deux blocs async pour envoyer des messages doivent être des blocs `async move` afin que `tx` et `tx1` soient abandonnés lorsque ces blocs se terminent. Sinon, nous nous retrouverons à nouveau dans la même boucle infinie dans laquelle nous avons commencé.

Enfin, nous passons de `trpl::join` à `trpl::join!` pour gérer le futur supplémentaire : le macro `join!` attend un nombre arbitraire de futurs où nous connaissons le nombre de futurs à la compilation. Nous discuterons de l'attente d'une collection d'un nombre inconnu de futurs plus tard dans ce chapitre.

Maintenant, nous voyons tous les messages des deux futurs d'envoi, et comme les futurs d'envoi utilisent des délais légèrement différents après l'envoi, les messages sont également reçus à ces différents intervalles :

<!-- Pas d'extraction de la sortie car les modifications à cette sortie ne sont pas significatives ; les changements sont probablement dus à l'exécution différente des threads plutôt qu'à des modifications dans le compilateur -->

```text
reçu 'salut'
reçu 'plus'
reçu 'de'
reçu 'la'
reçu 'messagerie'
reçu 'futur'
reçu 'pour'
reçu 'vous'
```

Nous avons exploré comment utiliser le passage de messages pour envoyer des données entre des futurs, comment le code dans un bloc async s'exécute de manière séquentielle, comment déplacer la propriété dans un bloc async, et comment joindre plusieurs futurs. Ensuite, discutons de comment et pourquoi informer le runtime qu'il peut passer à une autre tâche.

[thread-spawn]: ch16-01-threads.html#creating-a-new-thread-with-spawn  
[join-handles]: ch16-01-threads.html#waiting-for-all-threads-to-finish  
[message-passing-threads]: ch16-02-message-passing.html  
[if-let]: ch06-03-if-let.html  
[capture-or-move]: ch13-01-closures.html#capturing-references-or-moving-ownership  
[move-threads]: ch16-01-threads.html#using-move-closures-with-threads  