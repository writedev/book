<!-- Old headings. Do not remove or links may break. -->

<a id="using-message-passing-to-transfer-data-between-threads"></a>

## Transférer des données entre threads par passage de messages

Une approche de plus en plus populaire pour garantir la concurrence sûre est le passage de messages, où des threads ou des acteurs communiquent en s’envoyant des messages contenant des données. Voici l’idée résumée dans un slogan tiré de [la documentation du langage Go](https://golang.org/doc/effective_go.html#concurrency) :
« Ne communiquez pas en partageant de la mémoire ; partagez plutôt la mémoire en communiquant. »

Pour permettre la concurrence par envoi de messages, la bibliothèque standard de Rust fournit une implémentation des canaux. Un _canal_ est un concept général de programmation qui permet d’envoyer des données d’un thread à un autre.

On peut imaginer un canal en programmation comme un cours d’eau à sens unique, tel qu’un ruisseau ou une rivière. Si vous y déposez quelque chose comme un canard en plastique, il suivra le courant jusqu’à l’extrémité du cours d’eau.

Un canal comporte deux parties : un émetteur et un récepteur. La partie émetteur est l’endroit en amont où vous déposez le canard en plastique dans la rivière, et la partie récepteur est l’endroit où le canard arrive en aval. Une partie de votre code appelle des méthodes sur l’émetteur avec les données que vous souhaitez envoyer, et une autre partie vérifie l’extrémité réceptrice pour voir si des messages sont arrivés. On dit qu’un canal est _fermé_ si l’une ou l’autre de ses parties, l’émetteur ou le récepteur, est abandonnée.

Nous allons ici élaborer un programme dans lequel un thread génère des valeurs et les envoie par un canal, tandis qu’un autre thread les reçoit et les affiche. Nous allons envoyer des valeurs simples entre les threads au moyen d’un canal afin d’illustrer cette fonctionnalité. Une fois la technique maîtrisée, vous pourrez utiliser des canaux pour tous les threads qui doivent communiquer entre eux, par exemple dans un système de clavardage ou dans un système où plusieurs threads effectuent chacun une partie d’un calcul et envoient leurs résultats à un thread qui les regroupe.

Tout d’abord, dans la liste 16-6, nous allons créer un canal sans rien en faire. Notez que ce code ne compilera pas encore, car Rust ne peut pas déterminer le type des valeurs que nous voulons envoyer par le canal.

<Listing number="16-6" file-name="src/main.rs" caption="Créer un canal et affecter ses deux parties à `tx` et `rx`">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-06/src/main.rs}}
```

</Listing>

Nous créons un nouveau canal à l’aide de la fonction `mpsc::channel` ; `mpsc` signifie _multiple producer, single consumer_ (plusieurs producteurs, un seul consommateur). En bref, l’implémentation des canaux de la bibliothèque standard de Rust permet à un canal d’avoir plusieurs extrémités _d’envoi_ qui produisent des valeurs, mais une seule extrémité _de réception_ qui les consomme. Imaginez plusieurs ruisseaux qui se rejoignent pour former une grande rivière : tout ce qui est envoyé par l’un de ces ruisseaux finira dans la rivière en aval. Nous allons commencer par un seul producteur, mais nous en ajouterons plusieurs une fois cet exemple fonctionnel.

La fonction `mpsc::channel` renvoie un tuple dont le premier élément est l’extrémité d’envoi — l’émetteur — et le second, l’extrémité de réception — le récepteur. Dans de nombreux domaines, les abréviations `tx` et `rx` sont traditionnellement utilisées pour _transmitter_ (émetteur) et _receiver_ (récepteur), respectivement. Nous nommons donc nos variables ainsi pour désigner chaque extrémité. Nous utilisons une instruction `let` avec un motif qui déstructure le tuple ; nous aborderons les motifs dans les instructions `let` et la déstructuration au chapitre 19. Pour l’instant, retenez qu’utiliser une instruction `let` de cette manière est une façon pratique d’extraire les éléments du tuple renvoyé par `mpsc::channel`.

Déplaçons l’extrémité émettrice dans un thread lancé et faisons-lui envoyer une chaîne de caractères afin que le thread lancé communique avec le thread principal, comme l’illustre la liste 16-7. C’est comme déposer un canard en plastique dans la rivière en amont ou envoyer un message de clavardage d’un thread à un autre.

<Listing number="16-7" file-name="src/main.rs" caption='Déplacer `tx` dans un thread lancé et envoyer `"hi"`'>

```rust
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-07/src/main.rs}}
```

</Listing>

Encore une fois, nous utilisons `thread::spawn` pour créer un nouveau thread, puis `move` pour déplacer `tx` dans la fermeture afin que le thread lancé en soit propriétaire. Le thread lancé doit être propriétaire de l’émetteur pour pouvoir envoyer des messages par le canal.

L’émetteur possède une méthode `send` qui prend la valeur que nous voulons envoyer. La méthode `send` renvoie un type `Result<T, E>`. Ainsi, si le récepteur a déjà été abandonné et qu’il n’y a aucun destinataire auquel envoyer une valeur, l’opération d’envoi renverra une erreur. Dans cet exemple, nous appelons `unwrap` pour déclencher une panique en cas d’erreur. Dans une vraie application, nous la traiterions correctement : reportez-vous au chapitre 9 pour revoir les stratégies de gestion appropriée des erreurs.

Dans la liste 16-8, nous allons récupérer la valeur depuis le récepteur dans le thread principal. C’est comme récupérer le canard en plastique dans l’eau au bout de la rivière ou recevoir un message de clavardage.

<Listing number="16-8" file-name="src/main.rs" caption='Recevoir la valeur `"hi"` dans le thread principal et l’afficher'>

```rust
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-08/src/main.rs}}
```

</Listing>

Le récepteur possède deux méthodes utiles : `recv` et `try_recv`. Nous utilisons `recv`, abréviation de _receive_ (recevoir), qui bloque l’exécution du thread principal et attend qu’une valeur soit envoyée par le canal. Une fois qu’une valeur a été envoyée, `recv` la renvoie dans un `Result<T, E>`. Lorsque l’émetteur se ferme, `recv` renvoie une erreur pour signaler qu’aucune autre valeur ne sera envoyée.

La méthode `try_recv` ne bloque pas ; elle renvoie immédiatement un `Result<T, E>` : une valeur `Ok` contenant un message si l’un d’eux est disponible, et une valeur `Err` s’il n’y a aucun message pour le moment. `try_recv` est utile si ce thread a d’autres tâches à effectuer en attendant des messages : nous pourrions écrire une boucle qui appelle `try_recv` de temps en temps, traite un message s’il y en a un, et effectue sinon une autre tâche pendant un moment avant de vérifier à nouveau.

Nous avons utilisé `recv` dans cet exemple par souci de simplicité ; le thread principal n’a rien d’autre à faire que d’attendre des messages, il est donc approprié de le bloquer.

Lorsque nous exécutons le code de la liste 16-8, nous voyons la valeur affichée depuis le thread principal :

<!-- Not extracting output because changes to this output aren't significant;
the changes are likely to be due to the threads running differently rather than
changes in the compiler -->

```text
Got: hi
```

Parfait !

<!-- Old headings. Do not remove or links may break. -->

<a id="channels-and-ownership-transference"></a>

### Transférer la propriété par les canaux

Les règles de propriété jouent un rôle essentiel dans l’envoi de messages, car elles vous aident à écrire du code sûr et concurrent. Penser à la propriété dans l’ensemble de vos programmes Rust permet d’éviter les erreurs de programmation concurrente. Faisons une expérience pour montrer comment les canaux et la propriété fonctionnent ensemble afin d’éviter les problèmes : nous allons essayer d’utiliser une valeur `val` dans le thread lancé _après_ l’avoir envoyée par le canal. Essayez de compiler le code de la liste 16-9 pour comprendre pourquoi il n’est pas autorisé.

<Listing number="16-9" file-name="src/main.rs" caption="Tenter d’utiliser `val` après l’avoir envoyée par le canal">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-09/src/main.rs}}
```

</Listing>

Ici, nous essayons d’afficher `val` après l’avoir envoyée par le canal au moyen de `tx.send`. Autoriser cela serait une mauvaise idée : une fois la valeur envoyée à un autre thread, celui-ci pourrait la modifier ou l’abandonner avant que nous essayions de l’utiliser à nouveau. Les modifications de l’autre thread pourraient alors provoquer des erreurs ou des résultats inattendus en raison de données incohérentes ou inexistantes. Cependant, Rust renvoie une erreur si nous essayons de compiler le code de la liste 16-9 :

```console
{{#include ../listings/ch16-fearless-concurrency/listing-16-09/output.txt}}
```

Notre erreur de programmation concurrente a provoqué une erreur à la compilation. La fonction `send` prend possession de son paramètre et, lorsque la valeur est déplacée, le récepteur en devient propriétaire. Cela nous empêche de réutiliser accidentellement la valeur après l’avoir envoyée ; le système de propriété vérifie que tout est correct.

<!-- Old headings. Do not remove or links may break. -->

<a id="sending-multiple-values-and-seeing-the-receiver-waiting"></a>

### Envoyer plusieurs valeurs

Le code de la liste 16-8 a compilé et s’est exécuté, mais il ne montrait pas clairement que deux threads distincts communiquaient par le canal.

Dans la liste 16-10, nous avons apporté quelques modifications qui démontreront que le code de la liste 16-8 s’exécute de manière concurrente : le thread lancé va maintenant envoyer plusieurs messages et marquer une pause d’une seconde entre chacun d’eux.

<Listing number="16-10" file-name="src/main.rs" caption="Envoyer plusieurs messages et marquer une pause entre chacun d’eux">

```rust,noplayground
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-10/src/main.rs}}
```

</Listing>

Cette fois, le thread lancé contient un vecteur de chaînes de caractères que nous voulons envoyer au thread principal. Nous parcourons ce vecteur, envoyons chaque chaîne séparément et marquons une pause entre chaque en appelant la fonction `thread::sleep` avec une valeur `Duration` d’une seconde.

Dans le thread principal, nous n’appelons plus explicitement la fonction `recv` ; nous traitons plutôt `rx` comme un itérateur. Nous affichons chaque valeur reçue. Lorsque le canal est fermé, l’itération prend fin.

Lorsque vous exécutez le code de la liste 16-10, vous devriez voir la sortie suivante, avec une pause d’une seconde entre chaque ligne :

<!-- Not extracting output because changes to this output aren't significant;
the changes are likely to be due to the threads running differently rather than
changes in the compiler -->

```text
Got: hi
Got: from
Got: the
Got: thread
```

Comme il n’y a aucune instruction qui marque une pause ou introduit un délai dans la boucle `for` du thread principal, nous pouvons constater que le thread principal attend de recevoir des valeurs du thread lancé.

<!-- Old headings. Do not remove or links may break. -->

<a id="creating-multiple-producers-by-cloning-the-transmitter"></a>

### Créer plusieurs producteurs

Nous avons indiqué précédemment que `mpsc` était l’acronyme de _multiple producer, single consumer_ (plusieurs producteurs, un seul consommateur). Utilisons `mpsc` et développons le code de la liste 16-10 pour créer plusieurs threads qui envoient tous des valeurs au même récepteur. Nous pouvons le faire en clonant l’émetteur, comme l’illustre la liste 16-11.

<Listing number="16-11" file-name="src/main.rs" caption="Envoyer plusieurs messages depuis plusieurs producteurs">

```rust,noplayground
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-11/src/main.rs:here}}
```

</Listing>

Cette fois, avant de créer le premier thread lancé, nous appelons `clone` sur l’émetteur. Cela nous fournit un nouvel émetteur que nous pouvons transmettre au premier thread lancé. Nous transmettons l’émetteur d’origine à un second thread lancé. Nous avons ainsi deux threads qui envoient chacun des messages différents au même récepteur.

Lorsque vous exécutez le code, la sortie devrait ressembler à ceci :

<!-- Not extracting output because changes to this output aren't significant;
the changes are likely to be due to the threads running differently rather than
changes in the compiler -->

```text
Got: hi
Got: more
Got: from
Got: messages
Got: for
Got: the
Got: thread
Got: you
```

Les valeurs peuvent apparaître dans un autre ordre, selon votre système. C’est ce qui rend la programmation concurrente intéressante, mais aussi difficile. Si vous faites des essais avec `thread::sleep` en lui donnant des durées différentes dans chaque thread, chaque exécution sera encore moins déterministe et produira une sortie différente.

Maintenant que nous avons vu le fonctionnement des canaux, examinons une autre méthode de programmation concurrente.