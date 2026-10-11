## Concurrence à état partagé

Le passage de messages est une bonne façon de gérer la concurrence, mais ce n’est pas la seule. Une autre méthode consiste à permettre à plusieurs threads d’accéder aux mêmes données partagées. Repensons à cette partie du slogan de la documentation du langage Go : « Ne communiquez pas en partageant la mémoire. »

À quoi ressemblerait une communication par partage de mémoire ? De plus, pourquoi les adeptes du passage de messages déconseilleraient-ils le partage de mémoire ?

D’une certaine manière, les canaux de n’importe quel langage de programmation ressemblent à la propriété unique : une fois que vous avez transféré une valeur dans un canal, vous ne devriez plus utiliser cette valeur. La concurrence à mémoire partagée ressemble à la propriété multiple : plusieurs threads peuvent accéder au même emplacement mémoire au même moment. Comme vous l’avez vu au chapitre 15, où les pointeurs intelligents ont rendu possible la propriété multiple, celle-ci peut ajouter de la complexité, car il faut gérer ces différents propriétaires. Le système de types et les règles de propriété de Rust aident grandement à effectuer correctement cette gestion. Prenons les mutex, l’un des primitives de concurrence les plus courantes pour la mémoire partagée, à titre d’exemple.

<!-- Old headings. Do not remove or links may break. -->

<a id="using-mutexes-to-allow-access-to-data-from-one-thread-at-a-time"></a>

### Contrôler l’accès à l’aide de mutex

_Mutex_ est l’abréviation de _mutual exclusion_ (exclusion mutuelle) : un mutex ne permet qu’à un seul thread d’accéder à certaines données à la fois. Pour accéder aux données d’un mutex, un thread doit d’abord signaler qu’il souhaite y accéder en demandant à acquérir le verrou du mutex. Le _verrou_ est une structure de données qui fait partie du mutex et qui garde la trace du thread ayant actuellement un accès exclusif aux données. On dit donc que le mutex _protège_ les données qu’il contient au moyen de son système de verrouillage.

Les mutex ont la réputation d’être difficiles à utiliser, car il faut se rappeler deux règles :

1. Vous devez tenter d’acquérir le verrou avant d’utiliser les données.
2. Lorsque vous avez terminé d’utiliser les données protégées par le mutex, vous devez déverrouiller les données afin que d’autres threads puissent acquérir le verrou.

Pour illustrer un mutex par une métaphore du monde réel, imaginez une table ronde lors d’une conférence avec un seul microphone. Avant de prendre la parole, chaque intervenant doit demander ou signaler qu’il souhaite utiliser le microphone. Une fois le microphone en main, il peut parler aussi longtemps qu’il le souhaite, puis le passer au prochain intervenant qui demande la parole. Si un intervenant oublie de passer le microphone lorsqu’il a terminé, personne d’autre ne peut parler. Si la gestion du microphone partagé se passe mal, la table ronde ne se déroulera pas comme prévu !

Il peut être extrêmement délicat de bien gérer les mutex, ce qui explique l’enthousiasme de tant de personnes pour les canaux. Cependant, grâce au système de types et aux règles de propriété de Rust, vous ne pouvez pas vous tromper dans le verrouillage et le déverrouillage.

#### L’API de `Mutex<T>`

Pour voir comment utiliser un mutex, commençons par en utiliser un dans un contexte à thread unique, comme illustré dans l’exemple 16-12.

<Listing number="16-12" file-name="src/main.rs" caption="Exploration de l’API de `Mutex<T>` dans un contexte à thread unique, par souci de simplicité">

```rust
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-12/src/main.rs}}
```

</Listing>

Comme pour de nombreux types, nous créons un `Mutex<T>` à l’aide de la fonction associée `new`. Pour accéder aux données à l’intérieur du mutex, nous utilisons la méthode `lock` afin d’acquérir le verrou. Cet appel bloque le thread courant, qui ne peut donc effectuer aucun travail avant que son tour de détenir le verrou ne soit arrivé.

L’appel à `lock` échouerait si un autre thread détenant le verrou paniquait. Dans ce cas, personne ne pourrait jamais obtenir le verrou ; nous avons donc choisi d’utiliser `unwrap` afin que ce thread panique si nous nous trouvons dans cette situation.

Une fois le verrou acquis, nous pouvons traiter la valeur de retour, nommée `num` dans cet exemple, comme une référence mutable aux données à l’intérieur. Le système de types garantit que nous acquérons un verrou avant d’utiliser la valeur dans `m`. Le type de `m` est `Mutex<i32>`, et non `i32` ; nous _devons_ donc appeler `lock` pour pouvoir utiliser la valeur `i32`. Il nous est impossible de l’oublier : le système de types ne nous laissera pas accéder au `i32` interne autrement.

L’appel à `lock` renvoie un type nommé `MutexGuard`, enveloppé dans un `LockResult`, que nous avons traité avec l’appel à `unwrap`. Le type `MutexGuard` implémente `Deref` pour pointer vers nos données internes ; il possède également une implémentation de `Drop` qui libère automatiquement le verrou lorsque le `MutexGuard` sort de portée, ce qui se produit à la fin de la portée interne. Ainsi, nous ne risquons pas d’oublier de libérer le verrou et d’empêcher les autres threads d’utiliser le mutex, car la libération du verrou se fait automatiquement.

Après avoir libéré le verrou, nous pouvons afficher la valeur du mutex et constater que nous avons pu modifier le `i32` interne en `6`.

<!-- Old headings. Do not remove or links may break. -->

<a id="sharing-a-mutext-between-multiple-threads"></a>

#### Accès partagé à `Mutex<T>`

Essayons maintenant de partager une valeur entre plusieurs threads à l’aide de `Mutex<T>`. Nous allons créer 10 threads et faire en sorte que chacun incrémente un compteur de 1, afin que celui-ci passe de 0 à 10. L’exemple 16-13 provoquera une erreur de compilation ; nous nous en servirons pour en apprendre davantage sur l’utilisation de `Mutex<T>` et sur la façon dont Rust nous aide à l’utiliser correctement.

<Listing number="16-13" file-name="src/main.rs" caption="Dix threads qui incrémentent chacun un compteur protégé par un `Mutex<T>`">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-13/src/main.rs}}
```

</Listing>

Nous créons une variable `counter` qui contient un `i32` dans un `Mutex<T>`, comme dans l’exemple 16-12. Ensuite, nous créons 10 threads en parcourant une plage de nombres. Nous utilisons `thread::spawn` et transmettons à tous les threads la même fermeture : elle déplace le compteur dans le thread, acquiert un verrou sur le `Mutex<T>` en appelant la méthode `lock`, puis ajoute 1 à la valeur dans le mutex. Lorsqu’un thread termine l’exécution de sa fermeture, `num` sort de portée et libère le verrou, afin qu’un autre thread puisse l’acquérir.

Dans le thread principal, nous recueillons tous les handles de jonction. Puis, comme dans l’exemple 16-2, nous appelons `join` sur chaque handle pour nous assurer que tous les threads se terminent. À ce stade, le thread principal acquiert le verrou et affiche le résultat du programme.

Nous avons laissé entendre que cet exemple ne compilerait pas. Voyons maintenant pourquoi !

```console
{{#include ../listings/ch16-fearless-concurrency/listing-16-13/output.txt}}
```

Le message d’erreur indique que la valeur `counter` a été déplacée lors de l’itération précédente de la boucle. Rust nous signale que nous ne pouvons pas déplacer la propriété du verrou `counter` dans plusieurs threads. Corrigeons l’erreur du compilateur à l’aide de la méthode de propriété multiple présentée au chapitre 15.

#### Propriété multiple avec plusieurs threads

Au chapitre 15, nous avons donné une valeur à plusieurs propriétaires en utilisant le pointeur intelligent `Rc<T>` pour créer une valeur dont les références sont comptées. Faisons de même ici et voyons ce qui se passe. Dans l’exemple 16-14, nous allons envelopper le `Mutex<T>` dans un `Rc<T>` et cloner le `Rc<T>` avant de déplacer la propriété dans le thread.

<Listing number="16-14" file-name="src/main.rs" caption="Tentative d’utiliser `Rc<T>` pour permettre à plusieurs threads de posséder le `Mutex<T>`">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-14/src/main.rs}}
```

</Listing>

Une fois de plus, nous compilons le programme et obtenons… des erreurs différentes ! Le compilateur nous apprend beaucoup de choses :

```console
{{#include ../listings/ch16-fearless-concurrency/listing-16-14/output.txt}}
```

Eh bien, ce message d’erreur est très verbeux ! Voici la partie importante à retenir : `` `Rc<Mutex<i32>>` cannot be sent between threads safely ``. Le compilateur nous indique également pourquoi : `` the trait `Send` is not implemented for `Rc<Mutex<i32>>` ``. Nous parlerons de `Send` dans la section suivante : c’est l’un des traits qui garantissent que les types utilisés avec des threads sont adaptés aux situations concurrentes.

Malheureusement, `Rc<T>` ne peut pas être partagé en toute sécurité entre des threads. Lorsque `Rc<T>` gère le compteur de références, il l’incrémente à chaque appel à `clone` et le décrémente lorsque chaque clone est supprimé. Mais il n’utilise aucune primitive de concurrence pour garantir que les modifications du compteur ne puissent pas être interrompues par un autre thread. Cela pourrait entraîner des comptages erronés, des bogues subtils qui pourraient à leur tour provoquer des fuites de mémoire ou la suppression d’une valeur avant que nous en ayons terminé avec elle. Il nous faut un type exactement semblable à `Rc<T>`, mais qui modifie le compteur de références de manière sûre vis-à-vis des threads.

#### Comptage atomique des références avec `Arc<T>`

Heureusement, `Arc<T>` est un type semblable à `Rc<T>` qui peut être utilisé en toute sécurité dans des situations concurrentes. Le _a_ signifie _atomic_ (atomique) : il s’agit d’un type dont les références sont comptées de manière atomique. Les types atomiques constituent une autre sorte de primitive de concurrence que nous n’aborderons pas en détail ici. Pour en savoir plus, consultez la documentation de la bibliothèque standard pour [`std::sync::atomic`][atomic]<!-- ignore -->. À ce stade, il vous suffit de savoir que les types atomiques fonctionnent comme des types primitifs, mais qu’ils peuvent être partagés en toute sécurité entre des threads.

Vous pourriez alors vous demander pourquoi tous les types primitifs ne sont pas atomiques et pourquoi les types de la bibliothèque standard ne sont pas implémentés pour utiliser `Arc<T>` par défaut. La raison est que la sécurité entre threads a un coût en performances, que l’on ne souhaite payer que lorsque cela est vraiment nécessaire. Si vous effectuez simplement des opérations sur des valeurs au sein d’un seul thread, votre code peut s’exécuter plus rapidement s’il n’a pas à garantir les propriétés offertes par les types atomiques.

Revenons à notre exemple : `Arc<T>` et `Rc<T>` ont la même API. Nous corrigeons donc notre programme en modifiant la ligne `use`, l’appel à `new` et l’appel à `clone`. Le code de l’exemple 16-15 va enfin compiler et s’exécuter.

<Listing number="16-15" file-name="src/main.rs" caption="Utilisation d’un `Arc<T>` pour envelopper le `Mutex<T>` et partager la propriété entre plusieurs threads">

```rust
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-15/src/main.rs}}
```

</Listing>

Ce code affichera le résultat suivant :

<!-- Not extracting output because changes to this output aren't significant;
the changes are likely to be due to the threads running differently rather than
changes in the compiler -->

```text
Result: 10
```

Nous avons réussi ! Nous avons compté de 0 à 10. Cela ne semble peut-être pas très impressionnant, mais nous avons beaucoup appris sur `Mutex<T>` et la sécurité entre threads. Vous pourriez également utiliser la structure de ce programme pour effectuer des opérations plus complexes que la simple incrémentation d’un compteur. Avec cette approche, vous pouvez diviser un calcul en parties indépendantes, répartir ces parties entre plusieurs threads, puis utiliser un `Mutex<T>` pour que chaque thread mette à jour le résultat final avec sa partie.

Notez que pour des opérations numériques simples, le module [`std::sync::atomic`][atomic]<!-- ignore --> de la bibliothèque standard fournit des types plus simples que `Mutex<T>`. Ces types offrent un accès sûr, concurrent et atomique aux types primitifs. Nous avons choisi d’utiliser `Mutex<T>` avec un type primitif dans cet exemple afin de pouvoir nous concentrer sur le fonctionnement de `Mutex<T>`.

<!-- Old headings. Do not remove or links may break. -->

<a id="similarities-between-refcelltrct-and-mutextarct"></a>

### Comparaison de `RefCell<T>`/`Rc<T>` et de `Mutex<T>`/`Arc<T>`

Vous avez peut-être remarqué que `counter` est immuable, mais que nous avons pu obtenir une référence mutable à la valeur qu’il contient ; cela signifie que `Mutex<T>` fournit une mutabilité intérieure, comme la famille `Cell`. De la même manière que nous avons utilisé `RefCell<T>` au chapitre 15 pour modifier le contenu d’un `Rc<T>`, nous utilisons `Mutex<T>` pour modifier le contenu d’un `Arc<T>`.

Il faut également noter que Rust ne peut pas vous protéger contre toutes les erreurs de logique lorsque vous utilisez `Mutex<T>`. Rappelez-vous qu’au chapitre 15, l’utilisation de `Rc<T>` comportait le risque de créer des cycles de références, où deux valeurs `Rc<T>` se référencent mutuellement, provoquant des fuites de mémoire. De même, `Mutex<T>` comporte un risque d’_interblocage_. Celui-ci se produit lorsqu’une opération doit verrouiller deux ressources et que deux threads ont chacun acquis l’un des verrous, ce qui les fait attendre indéfiniment l’un après l’autre. Si les interblocages vous intéressent, essayez de créer un programme Rust qui en provoque un ; puis, étudiez les stratégies d’atténuation des interblocages pour les mutex dans n’importe quel langage et essayez de les implémenter en Rust. La documentation de l’API de la bibliothèque standard pour `Mutex<T>` et `MutexGuard` contient des informations utiles.

Nous terminerons ce chapitre en parlant des traits `Send` et `Sync` et de la façon de les utiliser avec des types personnalisés.

[atomic]: ../std/sync/atomic/index.html