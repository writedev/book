<!-- Anciens titres. Ne pas supprimer, sous peine de rompre les liens. -->

<a id="extensible-concurrency-with-the-sync-and-send-traits"></a>
<a id="extensible-concurrency-with-the-send-and-sync-traits"></a>

## Une concurrence extensible avec `Send` et `Sync`

Fait intéressant, presque toutes les fonctionnalités de concurrence dont nous avons parlé jusqu’ici dans ce chapitre font partie de la bibliothèque standard, et non du langage. Vos possibilités de gestion de la concurrence ne se limitent ni au langage ni à la bibliothèque standard : vous pouvez écrire vos propres fonctionnalités de concurrence ou utiliser celles écrites par d’autres.

Cependant, parmi les concepts clés de la concurrence intégrés au langage plutôt qu’à la bibliothèque standard figurent les traits `std::marker` `Send` et `Sync`.

<!-- Anciens titres. Ne pas supprimer, sous peine de rompre les liens. -->

<a id="allowing-transference-of-ownership-between-threads-with-send"></a>

### Transférer la propriété entre les threads

Le trait marqueur `Send` indique que la propriété des valeurs d’un type qui implémente `Send` peut être transférée entre des threads. Presque tous les types Rust implémentent `Send`, mais il existe quelques exceptions, notamment `Rc<T>` : ce type ne peut pas implémenter `Send`, car si vous cloniez une valeur `Rc<T>` et tentiez de transférer la propriété du clone à un autre thread, les deux threads pourraient mettre à jour le compteur de références en même temps. C’est pourquoi `Rc<T>` est conçu pour les situations à thread unique dans lesquelles vous ne voulez pas subir la pénalité de performances liée à la sécurité des threads.

Le système de types et les bornes de traits de Rust garantissent donc que vous ne pouvez jamais envoyer accidentellement une valeur `Rc<T>` entre des threads de manière non sécurisée. Lorsque nous avons essayé de le faire dans l’exemple 16-14, nous avons obtenu l’erreur `` le trait `Send` n’est pas implémenté pour `Rc<Mutex<i32>>` ``. Lorsque nous sommes passés à `Arc<T>`, qui implémente `Send`, le code a été compilé.

Tout type composé uniquement de types `Send` est automatiquement marqué comme `Send` également. Presque tous les types primitifs implémentent `Send`, à l’exception des pointeurs bruts, dont nous parlerons au chapitre 20.

<!-- Anciens titres. Ne pas supprimer, sous peine de rompre les liens. -->

<a id="allowing-access-from-multiple-threads-with-sync"></a>

### Accéder aux données depuis plusieurs threads

Le trait marqueur `Sync` indique que le type qui implémente `Sync` peut être référencé sans risque depuis plusieurs threads. Autrement dit, un type `T` implémente `Sync` si `&T` (une référence immuable vers `T`) implémente `Send`, ce qui signifie que la référence peut être envoyée sans risque à un autre thread. Comme pour `Send`, tous les types primitifs implémentent `Sync`, et les types composés uniquement de types qui implémentent `Sync` implémentent eux aussi `Sync`.

Le pointeur intelligent `Rc<T>` n’implémente pas non plus `Sync`, pour les mêmes raisons qu’il n’implémente pas `Send`. Le type `RefCell<T>` (dont nous avons parlé au chapitre 15) ainsi que la famille des types `Cell<T>` apparentés n’implémentent pas `Sync`. La vérification des emprunts que `RefCell<T>` effectue à l’exécution n’est pas sûre pour les threads. Le pointeur intelligent `Mutex<T>` implémente `Sync` et peut être utilisé pour partager l’accès entre plusieurs threads, comme vous l’avez vu dans [« Accès partagé à `Mutex<T>` »][shared-access]<!-- ignore -->.

### Implémenter `Send` et `Sync` manuellement n’est pas sûr

Puisque les types composés uniquement d’autres types qui implémentent les traits `Send` et `Sync` implémentent automatiquement `Send` et `Sync`, nous n’avons pas à implémenter ces traits manuellement. En tant que traits marqueurs, ils n’ont même aucune méthode à implémenter. Ils servent uniquement à faire respecter les invariants liés à la concurrence.

L’implémentation manuelle de ces traits implique l’écriture de code Rust non sécurisé. Nous parlerons de l’utilisation du code Rust non sécurisé au chapitre 20 ; pour l’instant, l’essentiel à retenir est que la création de nouveaux types concurrents qui ne sont pas composés d’éléments `Send` et `Sync` exige une réflexion approfondie afin de préserver les garanties de sécurité. [« Le Rustonomicon »][nomicon] fournit davantage d’informations sur ces garanties et sur la manière de les préserver.

## Résumé

Ce n’est pas la dernière fois que vous verrez la concurrence dans ce livre : le chapitre suivant se concentre sur la programmation asynchrone, et le projet du chapitre 21 mettra en pratique les concepts de ce chapitre dans une situation plus réaliste que les petits exemples présentés ici.

Comme nous l’avons mentionné précédemment, puisque très peu des mécanismes de gestion de la concurrence de Rust font partie du langage, de nombreuses solutions de concurrence sont implémentées sous forme de crates. Elles évoluent plus rapidement que la bibliothèque standard ; pensez donc à chercher en ligne les crates les plus récentes et les plus avancées à utiliser dans les situations multithread.

La bibliothèque standard de Rust fournit des canaux pour la transmission de messages ainsi que des types de pointeurs intelligents, tels que `Mutex<T>` et `Arc<T>`, qui peuvent être utilisés sans risque dans des contextes concurrents. Le système de types et le vérificateur d’emprunts garantissent que le code utilisant ces solutions ne provoquera ni courses de données ni références invalides. Une fois votre code compilé, vous pouvez être assuré qu’il s’exécutera sans problème sur plusieurs threads, sans les bugs difficiles à détecter qui sont fréquents dans d’autres langages. La programmation concurrente n’est plus un concept à craindre : lancez-vous et rendez vos programmes concurrents sans crainte !

[shared-access]: ch16-03-shared-state.html#shared-access-to-mutext
[nomicon]: ../nomicon/index.html