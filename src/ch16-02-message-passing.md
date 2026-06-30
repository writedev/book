<!-- Anciennes en-têtes. Ne pas supprimer ou les liens peuvent se casser. -->

<a id="using-message-passing-to-transfer-data-between-threads"></a>

## Transférer des données entre les threads avec le passage de messages

Une approche de plus en plus populaire pour garantir une concurrence sûre est le passage de messages, où les threads ou acteurs communiquent en s'envoyant des messages contenant des données. Voici l'idée dans un slogan tiré de [la documentation du langage Go](https://golang.org/doc/effective_go.html#concurrency) : « Ne communiquez pas en partageant de la mémoire ; au lieu de cela, partagez la mémoire en communiquant. »

Pour réaliser une concurrence par envoi de messages, la bibliothèque standard de Rust fournit une implémentation de canaux. Un _canal_ est un concept de programmation général par lequel les données sont envoyées d'un thread à un autre.

Vous pouvez imaginer un canal en programmation comme un canal directionnel d'eau, tel qu'un ruisseau ou une rivière. Si vous mettez quelque chose comme un canard en caoutchouc dans une rivière, il voyagera en aval jusqu'à la fin du cours d'eau.

Un canal a deux parties : un émetteur et un récepteur. La partie émettrice est l'emplacement en amont où vous mettez le canard en caoutchouc dans la rivière, et la partie réceptrice est l'endroit où le canard en caoutchouc se retrouve en aval. Une partie de votre code appelle des méthodes sur l'émetteur avec les données que vous souhaitez envoyer, et une autre partie vérifie l'extrémité réceptrice pour les messages arrivants. Un canal est dit _fermé_ si l'émetteur ou le récepteur est abandonné.

Ici, nous allons développer un programme qui a un thread pour générer des valeurs et les envoyer par un canal, et un autre thread qui recevra les valeurs et les affichera. Nous allons envoyer des valeurs simples entre threads en utilisant un canal pour illustrer cette fonctionnalité. Une fois que vous serez familiarisé avec la technique, vous pourrez utiliser des canaux pour n'importe quel thread ayant besoin de communiquer entre eux, comme un système de chat ou un système où plusieurs threads effectuent des parties d'un calcul et envoient les parties à un thread qui agrège les résultats.

Tout d'abord, dans le Listing 16-6, nous allons créer un canal sans encore l'utiliser. Notez que cela ne compilera pas encore, car Rust ne peut pas déterminer quel type de valeurs nous souhaitons envoyer par le canal.

<Listing number="16-6" file-name="src/main.rs" caption="Création d'un canal et attribution des deux parties à `tx` et `rx`">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-06/src/main.rs}}
```

</Listing>

Nous créons un nouveau canal en utilisant la fonction `mpsc::channel` ; `mpsc` signifie _multiple producer, single consumer_. En résumé, la façon dont la bibliothèque standard de Rust implémente les canaux signifie qu'un canal peut avoir plusieurs points _d'envoi_ qui produisent des valeurs mais seulement un point _de réception_ qui consomme ces valeurs. Imaginez plusieurs ruisseaux se rejoignant pour former une grande rivière : tout ce qui est envoyé dans n'importe lequel des ruisseaux se retrouvera à la fin dans cette rivière. Nous allons commencer avec un seul producteur pour l'instant, mais nous ajouterons plusieurs producteurs lorsque nous aurons fait fonctionner cet exemple.

La fonction `mpsc::channel` retourne un tuple, dont le premier élément est le point d'envoi — l'émetteur — et le deuxième élément est le point de réception — le récepteur. Les abréviations `tx` et `rx` sont traditionnellement utilisées dans de nombreux domaines pour _émetteur_ et _récepteur_, respectivement, donc nous nommons nos variables ainsi pour indiquer chaque extrémité. Nous utilisons une déclaration `let` avec un motif qui destructure les tuples ; nous discuterons de l'utilisation des motifs dans les déclarations `let` et de la destructuration au chapitre 19. Pour l'instant, sachez que l'utilisation d'une déclaration `let` de cette manière est une approche pratique pour extraire les éléments du tuple retourné par `mpsc::channel`.

Déplaçons l'extrémité émettrice dans un thread lancé et faisons-lui envoyer une chaîne afin que le thread lancé communique avec le thread principal, comme le montre le Listing 16-7. Cela ressemble à mettre un canard en caoutchouc dans la rivière en amont ou à envoyer un message de chat d'un thread à un autre.

<Listing number="16-7" file-name="src/main.rs" caption='Déplacer `tx` dans un thread lancé et envoyer `"hi"`'>

```rust
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-07/src/main.rs}}
```

</Listing>

Encore une fois, nous utilisons `thread::spawn` pour créer un nouveau thread et ensuite `move` pour déplacer `tx` dans la fermeture afin que le thread lancé possède `tx`. Le thread lancé doit posséder l'émetteur pour pouvoir envoyer des messages par le canal.

L'émetteur dispose d'une méthode `send` qui prend la valeur que nous voulons envoyer. La méthode `send` retourne un type `Result<T, E>`, donc si le récepteur a déjà été abandonné et qu'il n'y a nulle part où envoyer une valeur, l'opération d'envoi renverra une erreur. Dans cet exemple, nous appelons `unwrap` pour provoquer une panique en cas d'erreur. Mais dans une application réelle, nous devrions le gérer correctement : Revenez au chapitre 9 pour revoir les stratégies de gestion des erreurs appropriées.

Dans le Listing 16-8, nous allons récupérer la valeur depuis le récepteur dans le thread principal. Cela ressemble à récupérer le canard en caoutchouc de l'eau à la fin de la rivière ou à recevoir un message de chat.

<Listing number="16-8" file-name="src/main.rs" caption='Recevoir la valeur `"hi"` dans le thread principal et l'afficher'>

```rust
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-08/src/main.rs}}
```

</Listing>

Le récepteur dispose de deux méthodes utiles : `recv` et `try_recv`. Nous utilisons `recv`, abréviation de _receive_, qui bloquera l'exécution du thread principal et attendra qu'une valeur soit envoyée par le canal. Une fois qu'une valeur est envoyée, `recv` la retournera dans un `Result<T, E>`. Lorsque l'émetteur se ferme, `recv` renverra une erreur pour signaler qu'aucune valeur ne viendra plus.

La méthode `try_recv` ne bloque pas, mais renverra immédiatement un `Result<T, E>` : une valeur `Ok` contenant un message si un message est disponible et une valeur `Err` s'il n'y a pas de messages cette fois-ci. Utiliser `try_recv` est utile si ce thread a d'autres tâches à accomplir en attendant les messages : nous pourrions écrire une boucle qui appelle `try_recv` de temps en temps, gère un message s'il est disponible, et sinon fait d'autres travaux pendant un petit moment avant de vérifier à nouveau.

Nous avons utilisé `recv` dans cet exemple pour des raisons de simplicité ; nous n'avons pas d'autres tâches pour le thread principal à réaliser que d'attendre des messages, donc bloquer le thread principal est approprié.

Lorsque nous exécutons le code dans le Listing 16-8, nous verrons la valeur affichée depuis le thread principal :

<!-- Pas d'extraction de sortie car les modifications de cette sortie ne sont pas significatives ; les changements proviennent probablement du fait que les threads s'exécutent différemment plutôt que de changements dans le compilateur -->

```text
Got: hi
```

Parfait !

<!-- Anciennes en-têtes. Ne pas supprimer ou les liens peuvent se casser. -->

<a id="channels-and-ownership-transference"></a>

### Transfert de propriété par l'intermédiaire des canaux

Les règles de propriété jouent un rôle essentiel dans l'envoi de messages car elles vous aident à écrire un code concurrent sûr. Prévenir les erreurs dans la programmation concurrente est l'avantage de penser à la propriété tout au long de vos programmes Rust. Faisons une expérience pour montrer comment les canaux et la propriété travaillent ensemble pour prévenir les problèmes : nous allons essayer d'utiliser une valeur `val` dans le thread lancé _après_ l'avoir envoyée par le canal. Essayez de compiler le code dans le Listing 16-9 pour voir pourquoi ce code n'est pas autorisé.

<Listing number="16-9" file-name="src/main.rs" caption="Tentative d'utilisation de `val` après l'avoir envoyée par le canal">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-09/src/main.rs}}
```

</Listing>

Ici, nous essayons d'afficher `val` après l'avoir envoyée par le canal via `tx.send`. Autoriser cela serait une mauvaise idée : une fois que la valeur a été envoyée à un autre thread, ce thread pourrait la modifier ou l'abandonner avant que nous n'essayions à nouveau d'utiliser la valeur. Potentiellement, les modifications de l'autre thread pourraient causer des erreurs ou des résultats inattendus en raison de données incohérentes ou inexistantes. Cependant, Rust nous renvoie une erreur si nous essayons de compiler le code dans le Listing 16-9 :

```console
{{#include ../listings/ch16-fearless-concurrency/listing-16-09/output.txt}}
```

Notre erreur de concurrence a causé une erreur de compilation. La fonction `send` prend possession de son paramètre, et lorsque la valeur est déplacée, le récepteur en prend possession également. Cela nous empêche d'utiliser à nouveau la valeur accidentellement après l'avoir envoyée ; le système de propriété vérifie que tout est en ordre.

<!-- Anciennes en-têtes. Ne pas supprimer ou les liens peuvent se casser. -->

<a id="sending-multiple-values-and-seeing-the-receiver-waiting"></a>

### Envoyer plusieurs valeurs

Le code dans le Listing 16-8 a été compilé et exécuté, mais il ne nous a pas clairement montré que deux threads distincts communiquent entre eux par le canal.

Dans le Listing 16-10, nous avons apporté quelques modifications qui prouveront que le code dans le Listing 16-8 s'exécute de manière concurrente : le thread lancé enverra désormais plusieurs messages et fera une pause d'une seconde entre chaque message.

<Listing number="16-10" file-name="src/main.rs" caption="Envoyer plusieurs messages et faire une pause entre chacun d'eux">

```rust,noplayground
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-10/src/main.rs}}
```

</Listing>

Cette fois, le thread lancé a un vecteur de chaînes que nous voulons envoyer au thread principal. Nous les parcourons, en envoyant chacune individuellement, et faisons une pause entre chaque appel à la fonction `thread::sleep` avec une valeur `Duration` d'une seconde.

Dans le thread principal, nous n'appelons plus explicitement la fonction `recv` : au lieu de cela, nous traitons `rx` comme un itérateur. Pour chaque valeur reçue, nous l'affichons. Lorsque le canal est fermé, l'itération se termine.

Lorsque vous exécutez le code dans le Listing 16-10, vous devriez voir la sortie suivante avec une pause d'une seconde entre chaque ligne :

<!-- Pas d'extraction de sortie car les modifications de cette sortie ne sont pas significatives ; les changements proviennent probablement du fait que les threads s'exécutent différemment plutôt que de changements dans le compilateur -->

```text
Got: hi
Got: from
Got: the
Got: thread
```

Puisque nous n'avons pas de code qui pause ou retarde dans la boucle `for` dans le thread principal, nous pouvons affirmer que le thread principal attend de recevoir des valeurs du thread lancé.

<!-- Anciennes en-têtes. Ne pas supprimer ou les liens peuvent se casser. -->

<a id="creating-multiple-producers-by-cloning-the-transmitter"></a>

### Création de plusieurs producteurs

Plus tôt, nous avons mentionné que `mpsc` était un acronyme pour _multiple producer, single consumer_. Mettons `mpsc` à profit et développons le code dans le Listing 16-10 pour créer plusieurs threads qui envoient tous des valeurs au même récepteur. Nous pouvons le faire en clonant l'émetteur, comme le montre le Listing 16-11.

<Listing number="16-11" file-name="src/main.rs" caption="Envoyer plusieurs messages à partir de plusieurs producteurs">

```rust,noplayground
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-11/src/main.rs:here}}
```

</Listing>

Cette fois, avant de créer le premier thread lancé, nous appelons `clone` sur l'émetteur. Cela nous donnera un nouvel émetteur que nous pourrons transmettre au premier thread lancé. Nous passons l'émetteur original à un deuxième thread lancé. Cela nous donne deux threads, chacun envoyant des messages différents au même récepteur.

Lorsque vous exécutez le code, votre sortie devrait ressembler à ceci :

<!-- Pas d'extraction de sortie car les modifications de cette sortie ne sont pas significatives ; les changements proviennent probablement du fait que les threads s'exécutent différemment plutôt que de changements dans le compilateur -->

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

Vous pourriez voir les valeurs dans un autre ordre, en fonction de votre système. C'est ce qui rend la concurrence intéressante et difficile. Si vous expérimentez avec `thread::sleep`, en lui donnant différentes valeurs dans les différents threads, chaque exécution sera plus non déterministe et produira une sortie différente à chaque fois.

Maintenant que nous avons examiné le fonctionnement des canaux, examinons une autre méthode de concurrence.