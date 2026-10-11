## Tout assembler : futures, tâches et threads

Comme nous l’avons vu au [chapitre 16][ch16]<!-- ignore -->, les threads offrent une approche de la concurrence. Nous avons découvert une autre approche dans ce chapitre : utiliser l’asynchrone avec des futures et des streams. Si vous vous demandez quand choisir une méthode plutôt qu’une autre, la réponse est : cela dépend ! Et dans de nombreux cas, le choix ne se fait pas entre les threads _ou_ l’asynchrone, mais entre les threads _et_ l’asynchrone.

De nombreux systèmes d’exploitation proposent depuis des décennies des modèles de concurrence basés sur les threads, et de nombreux langages de programmation les prennent donc en charge. Cependant, ces modèles ne sont pas sans inconvénients. Sur de nombreux systèmes d’exploitation, chaque thread consomme une quantité considérable de mémoire. Les threads ne sont également envisageables que si votre système d’exploitation et votre matériel les prennent en charge. Contrairement aux ordinateurs de bureau et aux appareils mobiles courants, certains systèmes embarqués n’ont pas de système d’exploitation et ne disposent donc pas non plus de threads.

Le modèle asynchrone offre un ensemble différent — et, au final, complémentaire — d’avantages et d’inconvénients. Dans ce modèle, les opérations concurrentes n’ont pas besoin de leurs propres threads. Elles peuvent plutôt s’exécuter dans des tâches, comme lorsque nous avons utilisé `trpl::spawn_task` pour lancer du travail depuis une fonction synchrone dans la section consacrée aux streams. Une tâche ressemble à un thread, mais au lieu d’être gérée par le système d’exploitation, elle est gérée par du code au niveau de la bibliothèque : le runtime.

Il y a une raison pour laquelle les API permettant de lancer des threads et des tâches sont si similaires. Les threads délimitent des ensembles d’opérations synchrones ; la concurrence est possible _entre_ les threads. Les tâches délimitent des ensembles d’opérations _asynchrones_ ; la concurrence est possible à la fois _entre_ les tâches et _au sein_ de celles-ci, car une tâche peut passer d’une future à une autre dans son corps. Enfin, les futures sont l’unité de concurrence la plus fine de Rust, et chaque future peut représenter un arbre d’autres futures. Le runtime — plus précisément, son exécuteur — gère les tâches, et les tâches gèrent les futures. À cet égard, les tâches ressemblent à des threads légers gérés par le runtime, auxquels s’ajoutent des capacités qui découlent de leur gestion par un runtime plutôt que par le système d’exploitation.

Cela ne signifie pas que les tâches asynchrones sont toujours préférables aux threads (ou vice versa). La concurrence avec les threads constitue à certains égards un modèle de programmation plus simple que la concurrence avec `async`. Cela peut être un avantage ou un inconvénient. Les threads sont en quelque sorte « lancés sans se soucier de la suite » ; ils n’ont pas d’équivalent natif à une future et s’exécutent donc simplement jusqu’à leur terme, sans interruption, sauf par le système d’exploitation lui-même.

Il s’avère que les threads et les tâches fonctionnent souvent très bien ensemble, car les tâches peuvent (au moins dans certains runtimes) être déplacées d’un thread à l’autre. En fait, sous le capot, le runtime que nous utilisons — y compris les fonctions `spawn_blocking` et `spawn_task` — est multithread par défaut ! De nombreux runtimes utilisent une approche appelée _vol de travail_ pour déplacer les tâches de manière transparente d’un thread à l’autre, selon le niveau d’utilisation des threads, afin d’améliorer les performances globales du système. Cette approche nécessite en réalité des threads _et_ des tâches, et donc des futures.

Pour choisir la méthode à utiliser, gardez à l’esprit ces quelques règles générales :

- Si le travail est _fortement parallélisable_ (c’est-à-dire limité par le processeur), comme le traitement d’un grand volume de données dont chaque partie peut être traitée séparément, les threads sont un meilleur choix.
- Si le travail est _fortement concurrent_ (c’est-à-dire limité par les entrées-sorties), comme la gestion de messages provenant de nombreuses sources différentes et arrivant à des intervalles ou à des rythmes variés, l’asynchrone est un meilleur choix.

Et si vous avez besoin à la fois de parallélisme et de concurrence, vous n’avez pas à choisir entre les threads et l’asynchrone. Vous pouvez les utiliser ensemble librement, en laissant chacun faire ce qu’il fait le mieux. Par exemple, l’exemple 17-25 présente un cas assez courant de cette combinaison dans du code Rust utilisé dans le monde réel.

<Listing number="17-25" caption="Envoi de messages avec du code bloquant dans un thread et attente des messages dans un bloc asynchrone" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-25/src/main.rs:all}}
```

</Listing>

Nous commençons par créer un canal asynchrone, puis nous lançons un thread qui prend possession de l’extrémité émettrice du canal à l’aide du mot-clé `move`. Dans le thread, nous envoyons les nombres de 1 à 10, en attendant une seconde entre chaque envoi. Enfin, nous exécutons une future créée avec un bloc asynchrone transmis à `trpl::block_on`, comme nous l’avons fait tout au long du chapitre. Dans cette future, nous attendons ces messages, comme dans les autres exemples d’échange de messages que nous avons vus.

Pour revenir au scénario qui a ouvert le chapitre, imaginez que vous exécutiez un ensemble de tâches d’encodage vidéo sur un thread dédié (car l’encodage vidéo sollicite fortement le processeur), tout en informant l’interface utilisateur de la fin de ces opérations à l’aide d’un canal asynchrone. Les cas d’utilisation réels regorgent de combinaisons de ce type.

## Résumé

Ce ne sera pas la dernière fois que vous verrez de la concurrence dans ce livre. Le projet du [chapitre 21][ch21]<!-- ignore --> appliquera ces concepts à une situation plus réaliste que les exemples plus simples présentés ici et comparera plus directement la résolution de problèmes avec les threads à celle avec les tâches et les futures.

Quelle que soit l’approche choisie, Rust vous fournit les outils nécessaires pour écrire du code concurrent sûr et rapide, qu’il s’agisse d’un serveur web à haut débit ou d’un système d’exploitation embarqué.

Ensuite, nous aborderons des façons idiomatiques de modéliser les problèmes et de structurer les solutions à mesure que vos programmes Rust prennent de l’ampleur. Nous verrons également comment les idiomes de Rust se rapportent à ceux que vous connaissez peut-être en programmation orientée objet.

[ch16]: ch16-00-concurrency.html
[combining-futures]: ch17-03-more-futures.html#building-our-own-async-abstractions
[streams]: ch17-04-streams.html#composing-streams
[ch21]: ch21-00-final-project-a-web-server.html