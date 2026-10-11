<!-- Old headings. Do not remove or links may break. -->

<a id="concurrency-with-async"></a>

## Appliquer la concurrence avec async

Dans cette section, nous allons appliquer async à certains des mêmes défis de concurrence que nous avons abordés avec les threads au chapitre 16. Comme nous avons déjà discuté de nombreuses idées clés à ce sujet, nous allons nous concentrer ici sur les différences entre les threads et les futures.

Dans de nombreux cas, les API permettant de gérer la concurrence avec async sont très similaires à celles qui servent à utiliser les threads. Dans d’autres cas, elles s’avèrent très différentes. Même lorsque les API _semblent_ similaires entre les threads et async, leur comportement est souvent différent — et leurs caractéristiques de performance le sont presque toujours.

<!-- Old headings. Do not remove or links may break. -->

<a id="counting"></a>

### Créer une nouvelle tâche avec `spawn_task`

La première opération abordée dans la section [« Créer un nouveau thread avec
`spawn` »][thread-spawn]<!-- ignore --> du chapitre 16 consistait à compter sur
deux threads distincts. Faisons la même chose avec async. Le crate `trpl` fournit une fonction `spawn_task` qui ressemble beaucoup à l’API `thread::spawn`, ainsi qu’une fonction `sleep` qui est une version asynchrone de l’API `thread::sleep`. Nous pouvons les utiliser ensemble pour implémenter l’exemple de comptage, comme le montre l’exemple 17-6.

<Listing number="17-6" caption="Créer une nouvelle tâche pour afficher une chose pendant que la tâche principale en affiche une autre" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-06/src/main.rs:all}}
```

</Listing>

Pour commencer, nous configurons notre fonction `main` avec `trpl::block_on` afin que notre fonction de premier niveau puisse être asynchrone.

> Remarque : À partir de maintenant et jusqu’à la fin du chapitre, chaque exemple inclura exactement ce même code d’encapsulation avec `trpl::block_on` dans `main`. Nous l’omettrons donc souvent, comme nous le faisons pour `main`. N’oubliez pas de l’inclure dans votre code !

Nous écrivons ensuite deux boucles dans ce bloc, chacune contenant un appel à `trpl::sleep`, qui attend une demi-seconde (500 millisecondes) avant d’envoyer le message suivant. Nous plaçons une boucle dans le corps d’un `trpl::spawn_task` et l’autre dans une boucle `for` de premier niveau. Nous ajoutons également un `await` après les appels à `sleep`.

Ce code se comporte de façon similaire à l’implémentation basée sur les threads — notamment en ce que vous pouvez voir les messages apparaître dans un ordre différent dans votre terminal lorsque vous l’exécutez :

<!-- Not extracting output because changes to this output aren't significant;
the changes are likely to be due to the threads running differently rather than
changes in the compiler -->

```text
hi number 1 from the second task!
hi number 1 from the first task!
hi number 2 from the first task!
hi number 2 from the second task!
hi number 3 from the first task!
hi number 3 from the second task!
hi number 4 from the first task!
hi number 4 from the second task!
hi number 5 from the first task!
```

Cette version s’arrête dès que la boucle `for` dans le corps du bloc async principal se termine, car la tâche lancée par `spawn_task` est arrêtée lorsque la fonction `main` prend fin. Si vous voulez qu’elle s’exécute jusqu’à la fin de la tâche, vous devrez utiliser un handle de jointure pour attendre la fin de la première tâche. Avec les threads, nous avons utilisé la méthode `join` pour « bloquer » jusqu’à ce que le thread ait terminé son exécution. Dans l’exemple 17-7, nous pouvons utiliser `await` pour faire la même chose, car le handle de tâche lui-même est une future. Son type `Output` est un `Result` ; nous faisons donc également un unwrap après l’avoir attendu.

<Listing number="17-7" caption="Utiliser `await` avec un handle de jointure pour exécuter une tâche jusqu’à son terme" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-07/src/main.rs:handle}}
```

</Listing>

Cette version mise à jour s’exécute jusqu’à ce que _les deux_ boucles soient terminées :

<!-- Not extracting output because changes to this output aren't significant;
the changes are likely to be due to the threads running differently rather than
changes in the compiler -->

```text
hi number 1 from the second task!
hi number 1 from the first task!
hi number 2 from the first task!
hi number 2 from the second task!
hi number 3 from the first task!
hi number 3 from the second task!
hi number 4 from the first task!
hi number 4 from the second task!
hi number 5 from the first task!
hi number 6 from the first task!
hi number 7 from the first task!
hi number 8 from the first task!
hi number 9 from the first task!
```

Jusqu’ici, async et les threads semblent produire des résultats similaires, avec une syntaxe différente : on utilise `await` au lieu d’appeler `join` sur le handle de jointure, et on attend les appels à `sleep`.

La différence la plus importante est que nous n’avons pas eu besoin de lancer un autre thread du système d’exploitation pour cela. En fait, nous n’avons même pas besoin de lancer une tâche ici. Comme les blocs async sont compilés en futures anonymes, nous pouvons placer chaque boucle dans un bloc async et laisser le runtime les exécuter toutes les deux jusqu’à leur terme à l’aide de la fonction `trpl::join`.

Dans la section [« Attendre la fin de tous les threads »][join-handles]<!-- ignore --> du chapitre 16, nous avons montré comment utiliser la méthode `join` sur le type `JoinHandle` renvoyé lorsqu’on appelle `std::thread::spawn`. La fonction `trpl::join` est similaire, mais s’applique aux futures. Lorsqu’on lui fournit deux futures, elle produit une nouvelle future unique dont la sortie est un tuple contenant la sortie de chacune des futures fournies, une fois qu’elles sont _toutes les deux_ terminées. Ainsi, dans l’exemple 17-8, nous utilisons `trpl::join` pour attendre la fin de `fut1` et de `fut2`. Nous n’attendons _pas_ `fut1` et `fut2`, mais plutôt la nouvelle future produite par `trpl::join`. Nous ignorons la sortie, car il s’agit simplement d’un tuple contenant deux valeurs unitaires.

<Listing number="17-8" caption="Utiliser `trpl::join` pour attendre deux futures anonymes" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-08/src/main.rs:join}}
```

</Listing>

Lorsque nous exécutons ce code, nous voyons les deux futures s’exécuter jusqu’à leur terme :

<!-- Not extracting output because changes to this output aren't significant;
the changes are likely to be due to the threads running differently rather than
changes in the compiler -->

```text
hi number 1 from the first task!
hi number 1 from the second task!
hi number 2 from the first task!
hi number 2 from the second task!
hi number 3 from the first task!
hi number 3 from the second task!
hi number 4 from the first task!
hi number 4 from the second task!
hi number 5 from the first task!
hi number 6 from the first task!
hi number 7 from the first task!
hi number 8 from the first task!
hi number 9 from the first task!
```

Vous remarquerez maintenant que l’ordre est exactement le même à chaque exécution, ce qui diffère beaucoup de ce que nous avons observé avec les threads et avec `trpl::spawn_task` dans l’exemple 17-7. Cela s’explique par le fait que la fonction `trpl::join` est _équitable_ : elle vérifie chaque future aussi souvent que l’autre, en alternant entre elles, et ne laisse jamais l’une prendre de l’avance si l’autre est prête. Avec les threads, le système d’exploitation décide quel thread vérifier et combien de temps le laisser s’exécuter. Avec Rust asynchrone, c’est le runtime qui décide quelle tâche vérifier. (En pratique, les détails se compliquent, car un runtime async peut utiliser des threads du système d’exploitation en arrière-plan pour gérer la concurrence ; garantir l’équité peut donc demander davantage de travail au runtime — mais cela reste possible !) Les runtimes n’ont pas à garantir l’équité pour une opération donnée, et proposent souvent différentes API pour vous laisser choisir si vous souhaitez ou non cette équité.

Essayez certaines de ces variantes d’attente des futures et observez leur comportement :

- Supprimez le bloc async autour de l’une des boucles, ou des deux.
- Attendez chaque bloc async immédiatement après l’avoir défini.
- Enveloppez uniquement la première boucle dans un bloc async et attendez la future obtenue après le corps de la deuxième boucle.

Pour relever un défi supplémentaire, essayez de déterminer quelle sera la sortie dans chaque cas _avant_ d’exécuter le code !

<!-- Old headings. Do not remove or links may break. -->

<a id="message-passing"></a>
<a id="counting-up-on-two-tasks-using-message-passing"></a>

### Envoyer des données entre deux tâches par passage de messages

Le partage de données entre futures vous sera également familier : nous allons à nouveau utiliser le passage de messages, cette fois avec des versions asynchrones des types et des fonctions. Nous allons suivre une démarche légèrement différente de celle de la section [« Transférer des données entre threads par passage de messages »][message-passing-threads]<!-- ignore --> du chapitre 16 afin d’illustrer certaines différences clés entre la concurrence basée sur les threads et celle basée sur les futures. Dans l’exemple 17-9, nous commencerons par un seul bloc async — sans lancer une tâche distincte comme nous l’avons fait pour un thread distinct.

<Listing number="17-9" caption="Créer un canal async et affecter ses deux extrémités à `tx` et `rx`" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-09/src/main.rs:channel}}
```

</Listing>

Ici, nous utilisons `trpl::channel`, une version asynchrone de l’API de canal à plusieurs producteurs et un seul consommateur que nous avons utilisée avec les threads au chapitre 16. La version asynchrone de l’API diffère légèrement de la version basée sur les threads : elle utilise un récepteur `rx` mutable plutôt qu’immuable, et sa méthode `recv` produit une future que nous devons attendre au lieu de produire directement la valeur. Nous pouvons maintenant envoyer des messages de l’émetteur au récepteur. Remarquez que nous n’avons pas besoin de lancer un thread distinct, ni même une tâche ; il nous suffit d’attendre l’appel `rx.recv`.

La méthode synchrone `Receiver::recv` de `std::mpsc::channel` bloque jusqu’à la réception d’un message. La méthode `trpl::Receiver::recv` ne bloque pas, puisqu’elle est asynchrone. Au lieu de bloquer, elle rend le contrôle au runtime jusqu’à ce qu’un message soit reçu ou que le côté émetteur du canal soit fermé. En revanche, nous n’attendons pas l’appel à `send`, car il ne bloque pas. Ce n’est pas nécessaire, car le canal dans lequel nous envoyons les messages n’est pas borné.

> Remarque : Puisque tout ce code async s’exécute dans un bloc async au sein d’un appel à `trpl::block_on`, tout ce qu’il contient peut éviter de bloquer. En revanche, le code _à l’extérieur_ de ce bloc sera bloqué jusqu’au retour de la fonction `block_on`. C’est tout l’intérêt de la fonction `trpl::block_on` : elle vous permet de _choisir_ à quel endroit bloquer sur un ensemble de code async, et donc à quel endroit passer du code synchrone au code async.

Remarquez deux choses dans cet exemple. Premièrement, le message arrivera immédiatement. Deuxièmement, bien que nous utilisions ici une future, il n’y a pas encore de concurrence. Tout se déroule dans l’ordre dans l’exemple, comme si aucune future n’intervenait.

Abordons le premier point en envoyant une série de messages et en attendant entre chaque envoi, comme le montre l’exemple 17-10.

<!-- We cannot test this one because it never stops! -->

<Listing number="17-10" caption="Envoyer et recevoir plusieurs messages sur le canal async et attendre avec `await` entre chaque message" file-name="src/main.rs">

```rust,ignore
{{#rustdoc_include ../listings/ch17-async-await/listing-17-10/src/main.rs:many-messages}}
```

</Listing>

En plus d’envoyer les messages, nous devons les recevoir. Dans ce cas, puisque nous savons combien de messages vont arriver, nous pourrions le faire manuellement en appelant `rx.recv().await` quatre fois. Dans la réalité, cependant, nous attendrons généralement un nombre _inconnu_ de messages ; nous devons donc continuer à attendre jusqu’à déterminer qu’il n’y en a plus.

Dans l’exemple 16-10, nous avons utilisé une boucle `for` pour traiter tous les éléments reçus depuis un canal synchrone. Rust ne permet pas encore d’utiliser une boucle `for` avec une série d’éléments _produits de manière asynchrone_. Nous devons donc utiliser une boucle que nous n’avons pas encore rencontrée : la boucle conditionnelle `while let`. Il s’agit de la version en boucle de la construction `if let` présentée dans la section [« Contrôle de flux concis avec `if let` et `let...else` »][if-let]<!-- ignore --> du chapitre 6. La boucle continue tant que le motif qu’elle spécifie correspond à la valeur.

L’appel `rx.recv` produit une future que nous attendons. Le runtime mettra la future en pause jusqu’à ce qu’elle soit prête. Lorsqu’un message arrive, la future renvoie `Some(message)` à chaque réception d’un message. Lorsque le canal se ferme, que des messages soient arrivés ou non, la future renvoie plutôt `None` pour indiquer qu’il n’y a plus de valeurs et que nous devons donc cesser de la sonder — c’est-à-dire cesser de l’attendre.

La boucle `while let` rassemble tous ces éléments. Si le résultat de l’appel à `rx.recv().await` est `Some(message)`, nous pouvons accéder au message et l’utiliser dans le corps de la boucle, comme avec `if let`. Si le résultat est `None`, la boucle se termine. Chaque fois que la boucle se termine, elle atteint de nouveau le point d’attente ; le runtime la met donc à nouveau en pause jusqu’à l’arrivée d’un autre message.

Le code envoie et reçoit maintenant tous les messages correctement. Malheureusement, il reste quelques problèmes. D’une part, les messages n’arrivent pas à intervalles d’une demi-seconde. Ils arrivent tous en même temps, 2 secondes (2 000 millisecondes) après le démarrage du programme. D’autre part, ce programme ne se termine jamais non plus ! Il attend indéfiniment de nouveaux messages. Vous devrez l’arrêter avec <kbd>ctrl</kbd>-<kbd>C</kbd>.

#### Le code d’un même bloc async s’exécute de façon linéaire

Commençons par examiner pourquoi les messages arrivent tous en même temps après le délai complet, au lieu d’arriver avec un délai entre chacun. Dans un bloc async donné, l’ordre d’apparition des mots-clés `await` dans le code est également l’ordre dans lequel ils sont exécutés au lancement du programme.

Il n’y a qu’un seul bloc async dans l’exemple 17-10 ; tout son contenu s’exécute donc de façon linéaire. Il n’y a toujours pas de concurrence. Tous les appels à `tx.send` sont exécutés, entrecoupés de tous les appels à `trpl::sleep` et des points d’attente associés. Ce n’est qu’ensuite que la boucle `while let` atteint les points d’attente des appels à `recv`.

Pour obtenir le comportement souhaité, où le délai d’attente se produit entre chaque message, nous devons placer les opérations `tx` et `rx` dans leurs propres blocs async, comme le montre l’exemple 17-11. Le runtime peut alors les exécuter séparément à l’aide de `trpl::join`, comme dans l’exemple 17-8. Une fois encore, nous attendons le résultat de l’appel à `trpl::join`, et non les futures individuelles. Si nous attendions les futures individuelles l’une après l’autre, nous reviendrions simplement à un déroulement séquentiel — exactement ce que nous cherchons à éviter.

<!-- We cannot test this one because it never stops! -->

<Listing number="17-11" caption="Séparer `send` et `recv` dans leurs propres blocs `async` et attendre les futures correspondantes" file-name="src/main.rs">

```rust,ignore
{{#rustdoc_include ../listings/ch17-async-await/listing-17-11/src/main.rs:futures}}
```

</Listing>

Avec le code mis à jour de l’exemple 17-11, les messages s’affichent à intervalles de 500 millisecondes, au lieu d’arriver tous d’un coup après 2 secondes.

#### Déplacer la propriété dans un bloc async

Le programme ne se termine toujours pas, à cause de l’interaction entre la boucle `while let` et `trpl::join` :

- La future renvoyée par `trpl::join` ne se termine que lorsque _les deux_ futures qui lui sont fournies sont terminées.
- La future `tx_fut` se termine une fois qu’elle a fini d’attendre après l’envoi du dernier message de `vals`.
- La future `rx_fut` ne se termine pas tant que la boucle `while let` n’est pas terminée.
- La boucle `while let` ne se termine que lorsque l’attente de `rx.recv` renvoie `None`.
- L’attente de `rx.recv` ne renvoie `None que lorsque l’autre extrémité du canal est fermée.
- Le canal ne se ferme que si nous appelons `rx.close` ou si le côté émetteur, `tx`, est supprimé.
- Nous n’appelons `rx.close` nulle part, et `tx` ne sera pas supprimé tant que le bloc async le plus externe passé à `trpl::block_on` ne se termine pas.
- Le bloc ne peut pas se terminer, car il attend la fin de `trpl::join`, ce qui nous ramène au début de cette liste.

Pour l’instant, le bloc async où nous envoyons les messages ne fait qu’_emprunter_ `tx`, car envoyer un message ne nécessite pas d’en posséder la propriété. Mais si nous pouvions _déplacer_ `tx` dans ce bloc async, il serait supprimé à la fin du bloc. Dans la section [« Capturer des références ou déplacer la propriété »][capture-or-move]<!-- ignore --> du chapitre 13, vous avez appris à utiliser le mot-clé `move` avec les fermetures et, comme nous l’avons vu dans la section [« Utiliser des fermetures `move` avec des threads »][move-threads]<!-- ignore --> du chapitre 16, nous devons souvent déplacer des données dans des fermetures lorsque nous travaillons avec des threads. Les mêmes principes s’appliquent aux blocs async, et le mot-clé `move` fonctionne donc avec eux comme avec les fermetures.

Dans l’exemple 17-12, nous remplaçons `async` par `async move` dans le bloc utilisé pour envoyer les messages.

<Listing number="17-12" caption="Révision du code de l’exemple 17-11 qui s’arrête correctement une fois terminé" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-12/src/main.rs:with-move}}
```

</Listing>

Lorsque nous exécutons _cette_ version du code, elle s’arrête correctement après l’envoi et la réception du dernier message. Voyons maintenant ce qu’il faudrait modifier pour envoyer des données depuis plusieurs futures.

#### Joindre plusieurs futures avec la macro `join!`

Ce canal async accepte également plusieurs producteurs. Nous pouvons donc appeler `clone` sur `tx` si nous voulons envoyer des messages depuis plusieurs futures, comme le montre l’exemple 17-13.

<Listing number="17-13" caption="Utiliser plusieurs producteurs avec des blocs async" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-13/src/main.rs:here}}
```

</Listing>

Nous commençons par cloner `tx`, ce qui crée `tx1` en dehors du premier bloc async. Nous déplaçons `tx1` dans ce bloc, comme nous l’avons fait précédemment avec `tx`. Ensuite, nous déplaçons le `tx` d’origine dans un _nouveau_ bloc async, où nous envoyons davantage de messages avec un délai légèrement plus long. Nous avons placé ce nouveau bloc async après celui qui reçoit les messages, mais il aurait tout aussi bien pu être placé avant. L’essentiel est l’ordre dans lequel les futures sont attendues, et non celui dans lequel elles sont créées.

Les deux blocs async qui envoient des messages doivent être des blocs `async move` afin que `tx` et `tx1` soient supprimés lorsque ces blocs se terminent. Sinon, nous retomberions dans la même boucle infinie qu’au départ.

Enfin, nous remplaçons `trpl::join` par `trpl::join!` pour gérer la future supplémentaire : la macro `join!` attend un nombre quelconque de futures dont nous connaissons le nombre à la compilation. Nous verrons plus loin dans ce chapitre comment attendre une collection contenant un nombre inconnu de futures.

Nous voyons maintenant tous les messages envoyés par les deux futures émettrices et, comme celles-ci utilisent des délais légèrement différents après chaque envoi, les messages sont également reçus à des intervalles différents :

<!-- Not extracting output because changes to this output aren't significant;
the changes are likely to be due to the threads running differently rather than
changes in the compiler -->

```text
received 'hi'
received 'more'
received 'from'
received 'the'
received 'messages'
received 'future'
received 'for'
received 'you'
```

Nous avons vu comment utiliser le passage de messages pour envoyer des données entre futures, comment le code d’un bloc async s’exécute de manière séquentielle, comment déplacer la propriété dans un bloc async et comment joindre plusieurs futures. Voyons maintenant comment et pourquoi indiquer au runtime qu’il peut passer à une autre tâche.

[thread-spawn]: ch16-01-threads.html#creating-a-new-thread-with-spawn
[join-handles]: ch16-01-threads.html#waiting-for-all-threads-to-finish
[message-passing-threads]: ch16-02-message-passing.html
[if-let]: ch06-03-if-let.html
[capture-or-move]: ch13-01-closures.html#capturing-references-or-moving-ownership
[move-threads]: ch16-01-threads.html#using-move-closures-with-threads