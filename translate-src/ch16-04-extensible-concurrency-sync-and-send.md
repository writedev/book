<!-- Anciennes en-têtes. Ne pas supprimer ou les liens peuvent être rompus. -->

<a id="extensible-concurrency-with-the-sync-and-send-traits"></a>
<a id="extensible-concurrency-with-the-send-and-sync-traits"></a>

## Concurrence extensible avec `Send` et `Sync`

Fait intéressant, presque toutes les fonctionnalités de concurrence dont nous avons parlé jusqu'à présent dans ce chapitre font partie de la bibliothèque standard, et non du langage. Vos options de gestion de la concurrence ne se limitent pas au langage ou à la bibliothèque standard ; vous pouvez écrire vos propres fonctionnalités de concurrence ou utiliser celles écrites par d'autres.

Cependant, parmi les concepts clés de la concurrence qui sont intégrés dans le langage plutôt que dans la bibliothèque standard, on trouve les traits `Send` et `Sync` de `std::marker`.

<!-- Anciennes en-têtes. Ne pas supprimer ou les liens peuvent être rompus. -->

<a id="allowing-transference-of-ownership-between-threads-with-send"></a>

### Transfert de propriété entre les threads

Le trait marqueur `Send` indique que la propriété de valeurs du type implémentant `Send` peut être transférée entre les threads. La quasi-totalité des types Rust implémente `Send`, mais il existe quelques exceptions, notamment `Rc<T>` : cela ne peut pas implémenter `Send` car si vous clonez une valeur `Rc<T>` et essayez de transférer la propriété du clone à un autre thread, les deux threads pourraient mettre à jour le compteur de références en même temps. Pour cette raison, `Rc<T>` est implémenté pour être utilisé dans des situations à thread unique où vous ne voulez pas supporter la pénalité de performance liée à la sécurité des threads.

Par conséquent, le système de types de Rust et les bornes de traits garantissent que vous ne pouvez jamais envoyer accidentellement une valeur `Rc<T>` entre les threads de manière non sécurisée. Lorsque nous avons essayé de le faire dans la Liste 16-14, nous avons obtenu l'erreur `` le trait `Send` n'est pas implémenté pour `Rc<Mutex<i32>>` ``. Lorsque nous sommes passés à `Arc<T>`, qui implémente `Send`, le code a compilé.

Tout type composé uniquement de types `Send` est automatiquement marqué comme `Send` également. Presque tous les types primitifs sont `Send`, à l'exception des pointeurs bruts, que nous aborderons au chapitre 20.

<!-- Anciennes en-têtes. Ne pas supprimer ou les liens peuvent être rompus. -->

<a id="allowing-access-from-multiple-threads-with-sync"></a>

### Accès à partir de plusieurs threads

Le trait marqueur `Sync` indique qu'il est sûr que le type implémentant `Sync` soit référencé à partir de plusieurs threads. En d'autres termes, tout type `T` implémente `Sync` si `&T` (une référence immuable à `T`) implémente `Send`, ce qui signifie que la référence peut être envoyée en toute sécurité à un autre thread. À l'instar de `Send`, tous les types primitifs implémentent `Sync`, et les types entièrement composés de types qui implémentent `Sync` implémentent également `Sync`.

Le pointeur intelligent `Rc<T>` n'implémente également pas `Sync` pour les mêmes raisons qu'il n'implémente pas `Send`. Le type `RefCell<T>` (dont nous avons parlé au chapitre 15) et la famille de types `Cell<T>` associés n'implémentent pas `Sync`. L'implémentation de la vérification d'emprunt que `RefCell<T>` effectue à l'exécution n'est pas sécurisée pour les threads. Le pointeur intelligent `Mutex<T>` implémente `Sync` et peut être utilisé pour partager un accès avec plusieurs threads, comme vous l'avez vu dans [« Accès partagé à `Mutex<T>` »][shared-access]<!-- ignorer -->.

### Implémentation manuelle de `Send` et `Sync` est non sécurisée

Parce que les types entièrement composés d'autres types qui implémentent les traits `Send` et `Sync` implémentent également automatiquement `Send` et `Sync`, nous n'avons pas besoin d'implémenter ces traits manuellement. En tant que traits marqueurs, ils n'ont même pas de méthodes à implémenter. Ils sont simplement utiles pour faire respecter les invariants liés à la concurrence.

L'implémentation manuelle de ces traits implique la mise en œuvre de code Rust non sécurisé. Nous parlerons de l'utilisation du code Rust non sécurisé au chapitre 20 ; pour l'instant, l'information importante est que la création de nouveaux types concurrents qui ne sont pas composés de parties `Send` et `Sync` nécessite une réflexion soigneuse pour respecter les garanties de sécurité. [« The Rustonomicon »][nomicon] fournit plus d'informations sur ces garanties et comment les respecter.

## Résumé

Ce n'est pas la dernière fois que vous verrez la concurrence dans ce livre : le chapitre suivant se concentre sur la programmation asynchrone, et le projet du chapitre 21 utilisera les concepts de ce chapitre dans une situation plus réaliste que les petits exemples discutés ici.

Comme mentionné plus haut, parce que très peu de la façon dont Rust gère la concurrence fait partie du langage, de nombreuses solutions de concurrence sont mises en œuvre sous forme de crates. Celles-ci évoluent plus rapidement que la bibliothèque standard, alors assurez-vous de rechercher en ligne les crates les plus récentes à utiliser dans des situations multithread.

La bibliothèque standard Rust fournit des canaux pour le passage de messages et des types de pointeurs intelligents, tels que `Mutex<T>` et `Arc<T>`, qui sont sûrs à utiliser dans des contextes concurrents. Le système de types et le vérificateur d'emprunts garantissent que le code utilisant ces solutions ne finira pas par avoir des courses de données ou des références invalides. Une fois que vous avez réussi à compiler votre code, vous pouvez être sûr qu'il s'exécutera sans problème sur plusieurs threads, sans les types de bogues difficiles à déceler courants dans d'autres langages. La programmation concurrente n'est plus un concept à craindre : allez de l'avant et rendez vos programmes concurrents, sans crainte !

[shared-access]: ch16-03-shared-state.html#shared-access-to-mutext
[nomicon]: ../nomicon/index.html