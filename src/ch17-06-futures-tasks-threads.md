## Mettre le tout ensemble : Futures, Tâches et Threads

Comme nous l'avons vu dans [le Chapitre 16][ch16]<!-- ignore -->, les threads offrent une approche pour la concurrence. Nous avons vu une autre approche dans ce chapitre : l'utilisation d'async avec des futures et des streams. Si vous vous demandez quand choisir une méthode plutôt qu'une autre, la réponse est : cela dépend ! Et dans de nombreux cas, le choix n'est pas threads _ou_ async, mais plutôt threads _et_ async.

De nombreux systèmes d'exploitation fournissent des modèles de concurrence basés sur les threads depuis des décennies, et de nombreux langages de programmation les prennent en charge en conséquence. Cependant, ces modèles ne sont pas sans leurs compromis. Sur de nombreux systèmes d'exploitation, ils utilisent beaucoup de mémoire pour chaque thread. Les threads ne sont également une option que lorsque votre système d'exploitation et votre matériel les prennent en charge. Contrairement aux ordinateurs de bureau et mobiles grand public, certains systèmes embarqués n'ont pas du tout de système d'exploitation, donc ils n'ont également pas de threads.

Le modèle async offre un ensemble de compromis différent — et finalement complémentaire. Dans le modèle async, les opérations concurrentes n'exigent pas leurs propres threads. Au lieu de cela, elles peuvent s'exécuter sur des tâches, comme lorsque nous avons utilisé `trpl::spawn_task` pour démarrer du travail à partir d'une fonction synchrone dans la section streams. Une tâche est similaire à un thread, mais au lieu d'être gérée par le système d'exploitation, elle est gérée par le code au niveau de la bibliothèque : le runtime.

Il y a une raison pour laquelle les API pour lancer des threads et des tâches sont si similaires. Les threads agissent comme une frontière pour des ensembles d'opérations synchrones ; la concurrence est possible _entre_ les threads. Les tâches agissent comme une frontière pour des ensembles d'opérations _asynchrones_ ; la concurrence est possible à la fois _entre_ et _dans_ les tâches, car une tâche peut passer d'un futur à l'autre dans son corps. Enfin, les futures sont l'unité de concurrence la plus granulaire de Rust, et chaque futur peut représenter un arbre d'autres futures. Le runtime — en particulier son exécuteur — gère les tâches, et les tâches gèrent les futures. À cet égard, les tâches sont similaires à des threads légers, gérés par le runtime, avec des capacités ajoutées qui proviennent du fait qu'elles sont gérées par un runtime plutôt que par le système d'exploitation.

Cela ne signifie pas que les tâches async sont toujours meilleures que les threads (ou vice versa). La concurrence avec des threads est d'une certaine manière un modèle de programmation plus simple que la concurrence avec `async`. Cela peut être un atout ou une faiblesse. Les threads sont quelque peu « feu et oublie » ; ils n'ont pas d'équivalent natif à un futur, ils s'exécutent donc simplement jusqu'à l'achèvement sans être interrompus, sauf par le système d'exploitation lui-même.

Et il s'avère que les threads et les tâches fonctionnent souvent très bien ensemble, car les tâches peuvent (du moins dans certains runtimes) être déplacées entre les threads. En fait, en coulisse, le runtime que nous avons utilisé — y compris les fonctions `spawn_blocking` et `spawn_task` — est multithreadé par défaut ! De nombreux runtimes utilisent une approche appelée _vol par le travail_ pour déplacer les tâches de manière transparente entre les threads, en fonction de l'utilisation actuelle des threads, afin d'améliorer la performance globale du système. Cette approche nécessite en réalité à la fois des threads _et_ des tâches, et donc des futures.

Lorsque vous réfléchissez à la méthode à utiliser, considérez ces règles générales :

- Si le travail est _très parallélisable_ (c'est-à-dire lié au CPU), comme le traitement d'une quantité de données où chaque partie peut être traitée séparément, les threads sont un meilleur choix.
- Si le travail est _très concurrent_ (c'est-à-dire lié à l'I/O), comme gérer des messages provenant de différentes sources qui peuvent arriver à des intervalles ou des vitesses différentes, async est un meilleur choix.

Et si vous avez besoin à la fois de parallélisme et de concurrence, vous n'avez pas à choisir entre threads et async. Vous pouvez les utiliser ensemble librement, laissant chacun jouer le rôle qu'il maîtrise le mieux. Par exemple, la Liste 17-25 montre un exemple assez courant de ce type de mélange dans un code Rust du monde réel.

<Liste numéro="17-25" légende="Envoi de messages avec du code bloquant dans un thread et attente des messages dans un bloc async" nom-de-fichier="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-25/src/main.rs:all}}
```

</Liste>

Nous commençons par créer un canal async, puis lançons un thread qui prend possession de la partie émettrice du canal en utilisant le mot clé `move`. Au sein du thread, nous envoyons les nombres 1 à 10, en dormant une seconde entre chaque. Enfin, nous exécutons un futur créé avec un bloc async passé à `trpl::block_on`, tout comme nous l'avons fait tout au long du chapitre. Dans ce futur, nous attendons ces messages, tout comme dans les autres exemples de passage de messages que nous avons vus.

Pour revenir au scénario avec lequel nous avons ouvert le chapitre, imaginez exécuter un ensemble de tâches d'encodage vidéo en utilisant un thread dédié (car l'encodage vidéo est lié au calcul) mais en notifiant l'interface utilisateur que ces opérations sont terminées avec un canal async. Il existe d'innombrables exemples de ces types de combinaisons dans des cas d'utilisation réels.

## Résumé

Ce n'est pas la dernière fois que vous verrez la concurrence dans ce livre. Le projet dans [le Chapitre 21][ch21]<!-- ignore --> appliquera ces concepts dans une situation plus réaliste que les exemples plus simples discutés ici et comparera la résolution de problèmes avec des threads par rapport aux tâches et futures de manière plus directe.

Quelles que soient les approches que vous choisissez, Rust vous donne les outils nécessaires pour écrire du code concurrent, sûr et rapide — que ce soit pour un serveur web à haut débit ou un système d'exploitation embarqué.

Ensuite, nous aborderons les manières idiomatiques de modéliser des problèmes et de structurer des solutions à mesure que vos programmes Rust se développent. De plus, nous discuterons de la manière dont les idiomes de Rust se rapportent à ceux que vous pourriez connaître en programmation orientée objet.

[ch16]: http://localhost:3000/ch16-00-concurrency.html
[combining-futures]: ch17-03-more-futures.html#building-our-own-async-abstractions
[streams]: ch17-04-streams.html#composing-streams
[ch21]: ch21-00-final-project-a-web-server.html