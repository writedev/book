## Concurrence par état partagé

Le passage de messages est un bon moyen de gérer la concurrence, mais ce n'est pas la seule méthode. Une autre méthode consisterait à permettre à plusieurs threads d'accéder aux mêmes données partagées. Considérons à nouveau cette partie du slogan de la documentation du langage Go : « Ne communiquez pas en partageant la mémoire. »

À quoi ressemblerait la communication par partage de mémoire ? De plus, pourquoi les passionnés du passage de messages mettraient-ils en garde contre l'utilisation du partage de mémoire ?

D'une certaine manière, les canaux dans n'importe quel langage de programmation sont similaires à la propriété unique, car une fois que vous transférez une valeur à travers un canal, vous ne devez plus utiliser cette valeur. La concurrence par mémoire partagée ressemble à une propriété multiple : plusieurs threads peuvent accéder au même emplacement mémoire en même temps. Comme vous l'avez vu dans le Chapitre 15, où les pointeurs intelligents rendirent la propriété multiple possible, celle-ci peut ajouter de la complexité car ces différents propriétaires doivent être gérés. Le système de types de Rust et ses règles de propriété aident grandement à assurer cette gestion. Pour un exemple, examinons les mutex, l'une des primitives de concurrence les plus courantes pour la mémoire partagée.

<a id="using-mutexes-to-allow-access-to-data-from-one-thread-at-a-time"></a>

### Contrôle d'accès avec des Mutex

Le _mutex_ est une abréviation de _mutual exclusion_, ce qui signifie qu'un mutex permet à un seul thread d'accéder à certaines données à tout moment. Pour accéder aux données dans un mutex, un thread doit d'abord signaler qu'il souhaite accéder en demandant à acquérir le verrou du mutex. Le _verrou_ est une structure de données qui fait partie du mutex et qui garde la trace de qui a actuellement l'accès exclusif aux données. Par conséquent, le mutex est décrit comme _gardant_ les données qu'il détient via le système de verrouillage.

Les mutex ont une réputation d'être difficiles à utiliser car vous devez vous souvenir de deux règles :

1. Vous devez tenter d'acquérir le verrou avant d'utiliser les données.
2. Lorsque vous avez terminé avec les données que le mutex protège, vous devez déverrouiller les données afin que d'autres threads puissent acquérir le verrou.

Pour une métaphore réaliste d'un mutex, imaginez une table ronde lors d'une conférence avec un seul microphone. Avant qu'un participant puisse parler, il doit demander ou signaler qu'il souhaite utiliser le microphone. Lorsqu'il obtient le microphone, il peut parler aussi longtemps qu'il le souhaite, puis le passer au prochain participant qui souhaite prendre la parole. Si un participant oublie de passer le microphone lorsqu'il a terminé, personne d'autre ne peut parler. Si la gestion du microphone partagé tourne mal, le panel ne fonctionnera pas comme prévu !

La gestion des mutex peut être incroyablement délicate à bien faire, c'est pourquoi tant de personnes sont enthousiastes à propos des canaux. Cependant, grâce au système de types de Rust et à ses règles de propriété, vous ne pouvez pas vous tromper dans le verrouillage et le déverrouillage.

#### L'API de `Mutex<T>`

Comme exemple d'utilisation d'un mutex, commençons par l'utiliser dans un contexte à thread unique, comme le montre la Liste 16-12.

<Listing number="16-12" file-name="src/main.rs" caption="Exploration de l'API de `Mutex<T>` dans un contexte à thread unique pour plus de simplicité">

```rust
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-12/src/main.rs}}
```

</Listing>

Comme avec de nombreux types, nous créons un `Mutex<T>` en utilisant la fonction associée `new`. Pour accéder aux données à l'intérieur du mutex, nous utilisons la méthode `lock` pour acquérir le verrou. Cet appel bloquera le thread courant afin qu'il ne puisse pas effectuer de travail jusqu'à ce que ce soit notre tour d'avoir le verrou.

L'appel à `lock` échouerait si un autre thread tenant le verrou avait paniqué. Dans ce cas, personne ne pourrait jamais obtenir le verrou, nous avons donc choisi de `unwrap` et de faire paniquer ce thread si nous étions dans cette situation.

Après avoir acquis le verrou, nous pouvons traiter la valeur de retour, nommée `num` dans ce cas, comme une référence mutable aux données à l'intérieur. Le système de types garantit que nous acquérons un verrou avant d'utiliser la valeur dans `m`. Le type de `m` est `Mutex<i32>`, pas `i32`, donc nous _devons_ appeler `lock` pour pouvoir utiliser la valeur `i32`. Nous ne pouvons pas l'oublier ; le système de types ne nous permettra pas d'accéder au `i32` interne autrement.

L'appel à `lock` retourne un type appelé `MutexGuard`, enveloppé dans un `LockResult` que nous avons géré avec l'appel à `unwrap`. Le type `MutexGuard` implémente `Deref` pour pointer vers nos données internes ; ce type a également une implémentation de `Drop` qui libère automatiquement le verrou lorsqu'un `MutexGuard` sort de la portée, ce qui se produit à la fin de la portée interne. En conséquence, nous ne risquons pas d'oublier de libérer le verrou et de bloquer l'utilisation du mutex par d'autres threads, car la libération du verrou se produit automatiquement.

Après avoir relâché le verrou, nous pouvons imprimer la valeur du mutex et voir que nous avons pu changer le `i32` interne à `6`.

<a id="sharing-a-mutext-between-multiple-threads"></a>

#### Accès partagé à `Mutex<T>`

Essayons maintenant de partager une valeur entre plusieurs threads en utilisant `Mutex<T>`. Nous allons créer 10 threads et faire en sorte qu'ils incrémentent chacun une valeur compteur de 1, afin que le compteur passe de 0 à 10. L'exemple dans la Liste 16-13 générera une erreur de compilation, et nous utiliserons cette erreur pour en apprendre davantage sur l'utilisation de `Mutex<T>` et comment Rust nous aide à l'utiliser correctement.

<Listing number="16-13" file-name="src/main.rs" caption="Dix threads, chacun incrémentant un compteur protégé par un `Mutex<T>`">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-13/src/main.rs}}
```

</Listing>

Nous créons une variable `counter` pour contenir un `i32` à l'intérieur d'un `Mutex<T>`, comme nous l'avons fait dans la Liste 16-12. Ensuite, nous créons 10 threads en itérant sur une plage de nombres. Nous utilisons `thread::spawn` et donnons à tous les threads la même fermeture : une qui déplace le compteur dans le thread, acquiert un verrou sur le `Mutex<T>` en appelant la méthode `lock`, puis ajoute 1 à la valeur dans le mutex. Lorsqu'un thread termine l'exécution de sa fermeture, `num` sortira de la portée et libérera le verrou afin qu'un autre thread puisse l'acquérir.

Dans le thread principal, nous collectons tous les poignées de join. Puis, comme nous l'avons fait dans la Liste 16-2, nous appelons `join` sur chaque poignée pour nous assurer que tous les threads finissent. À ce moment-là, le thread principal acquérera le verrou et imprimera le résultat de ce programme.

Nous avions indiqué que cet exemple ne se compilerait pas. Voyons maintenant pourquoi !

```console
{{#include ../listings/ch16-fearless-concurrency/listing-16-13/output.txt}}
```

Le message d'erreur indique que la valeur de `counter` a été déplacée dans l'itération précédente de la boucle. Rust nous dit que nous ne pouvons pas transférer la propriété du verrou `counter` dans plusieurs threads. Corrigeons l'erreur de compilation avec la méthode de propriété multiple que nous avons discutée dans le Chapitre 15.

#### Propriété multiple avec plusieurs threads

Dans le Chapitre 15, nous avons donné une valeur à plusieurs propriétaires en utilisant le pointeur intelligent `Rc<T>` pour créer une valeur comptabilisée par référence. Faisons de même ici et voyons ce qui se passe. Nous allons envelopper le `Mutex<T>` dans un `Rc<T>` dans la Liste 16-14 et cloner le `Rc<T>` avant de déplacer la propriété vers le thread.

<Listing number="16-14" file-name="src/main.rs" caption="Tentative d'utilisation de `Rc<T>` pour permettre à plusieurs threads de posséder le `Mutex<T>`">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-14/src/main.rs}}
```

</Listing>

Encore une fois, nous compilons et obtenons... des erreurs différentes ! Le compilateur nous enseigne beaucoup :

```console
{{#include ../listings/ch16-fearless-concurrency/listing-16-14/output.txt}}
```

Wow, ce message d'erreur est très verbeux ! Voici la partie importante à retenir : `` `Rc<Mutex<i32>>` ne peut pas être envoyé entre threads en toute sécurité ``. Le compilateur nous dit également la raison : `` le trait `Send` n'est pas implémenté pour `Rc<Mutex<i32>>` ``. Nous parlerons de `Send` dans la section suivante : c'est l'un des traits qui garantissent que les types que nous utilisons avec des threads sont destinés à être utilisés dans des situations concurrentes.

Malheureusement, `Rc<T>` n'est pas sûr à partager entre threads. Lorsque `Rc<T>` gère le comptage des références, il ajoute au compte pour chaque appel à `clone` et soustrait du compte lorsque chaque clone est supprimé. Mais il n'utilise aucun primitive de concurrence pour s'assurer que les modifications apportées au compte ne peuvent pas être interrompues par un autre thread. Cela pourrait conduire à des comptes incorrects — des bogues subtils qui pourraient à leur tour entraîner des fuites de mémoire ou une valeur étant supprimée avant que nous ayons terminé avec elle. Ce dont nous avons besoin est un type qui ressemble exactement à `Rc<T>`, mais qui modifie les changements au compte de référence de manière thread-safe.

#### Compte de références atomique avec `Arc<T>`

Heureusement, `Arc<T>` _est_ un type comme `Rc<T>` qui est sûr à utiliser dans des situations concurrentes. Le _a_ signifie _atomique_, c'est-à-dire que c'est un type _compté par référence de manière atomique_. Les atomes sont un type supplémentaire de primitive de concurrence que nous ne couvrirons pas en détail ici : consultez la documentation de la bibliothèque standard pour [`std::sync::atomic`][atomic]<!-- ignore --> pour plus de détails. À ce stade, vous devez simplement savoir que les atomiques fonctionnent comme des types primitifs, mais sont sûrs à partager entre threads.

Vous pourriez alors vous demander pourquoi tous les types primitifs ne sont pas atomiques et pourquoi les types de la bibliothèque standard ne sont pas implémentés pour utiliser `Arc<T>` par défaut. La raison est que la sécurité des threads entraîne une pénalité de performance que vous ne voulez payer que lorsque c'est réellement nécessaire. Si vous effectuez simplement des opérations sur des valeurs dans un seul thread, votre code peut s'exécuter plus rapidement s'il n'a pas à appliquer les garanties fournies par les atomiques.

Revenons à notre exemple : `Arc<T>` et `Rc<T>` ont la même API, donc nous corrigeons notre programme en changeant la ligne `use`, l'appel à `new` et l'appel à `clone`. Le code dans la Liste 16-15 se compilera enfin et s'exécutera.

<Listing number="16-15" file-name="src/main.rs" caption="Utilisation d'un `Arc<T>` pour envelopper le `Mutex<T>` afin de pouvoir partager la propriété entre plusieurs threads">

```rust
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-15/src/main.rs}}
```

</Listing>

Ce code affichera ce qui suit :

```text
Résultat : 10
```

Nous l'avons fait ! Nous avons compté de 0 à 10, ce qui peut ne pas sembler très impressionnant, mais cela nous a beaucoup appris sur `Mutex<T>` et la sécurité des threads. Vous pourriez également utiliser la structure de ce programme pour effectuer des opérations plus compliquées que simplement incrémenter un compteur. En utilisant cette stratégie, vous pouvez diviser un calcul en parties indépendantes, répartir ces parties entre les threads, puis utiliser un `Mutex<T>` pour permettre à chaque thread de mettre à jour le résultat final avec sa partie.

Notez que si vous effectuez des opérations numériques simples, il existe des types plus simples que les types `Mutex<T>` fournis par le [module `std::sync::atomic` de la bibliothèque standard][atomic]<!-- ignore -->. Ces types fournissent un accès atomique, sûr et concurrent aux types primitifs. Nous avons choisi d'utiliser `Mutex<T>` avec un type primitif pour cet exemple afin de pouvoir nous concentrer sur le fonctionnement de `Mutex<T>`.

<a id="similarities-between-refcelltrct-and-mutextarct"></a>

### Comparaison de `RefCell<T>`/`Rc<T>` et `Mutex<T>`/`Arc<T>`

Vous avez peut-être remarqué que `counter` est immuable mais que nous pouvions obtenir une référence mutable à la valeur à l'intérieur ; cela signifie que `Mutex<T>` fournit une mutabilité intérieure, tout comme la famille `Cell`. De la même manière que nous avons utilisé `RefCell<T>` dans le Chapitre 15 pour nous permettre de modifier le contenu à l'intérieur d'un `Rc<T>`, nous utilisons `Mutex<T>` pour modifier le contenu à l'intérieur d'un `Arc<T>`.

Un autre détail à noter est que Rust ne peut pas vous protéger de tous les types d'erreurs logiques lorsque vous utilisez `Mutex<T>`. Rappelez-vous du Chapitre 15 que l'utilisation de `Rc<T>` comportait le risque de créer des cycles de référence, où deux valeurs `Rc<T>` se réfèrent l'une à l'autre, provoquant ainsi des fuites de mémoire. De même, `Mutex<T>` comporte le risque de créer des _interblocages_. Ceux-ci se produisent lorsqu'une opération doit verrouiller deux ressources et que deux threads ont chacun acquis l'un des verrous, les amenant à s'attendre mutuellement indéfiniment. Si vous êtes intéressé par les interblocages, essayez de créer un programme Rust qui a un interblocage ; ensuite, recherchez les stratégies d'atténuation des interblocages pour les mutex dans n'importe quel langage et essayez de les mettre en œuvre en Rust. La documentation de l'API de la bibliothèque standard pour `Mutex<T>` et `MutexGuard` offre des informations utiles.

Nous terminerons ce chapitre en parlant des traits `Send` et `Sync` et comment nous pouvons les utiliser avec des types personnalisés.

[atomic]: ../std/sync/atomic/index.html