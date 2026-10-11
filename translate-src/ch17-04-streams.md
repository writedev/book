<!-- Anciennes en-têtes. Ne pas supprimer, sinon les liens risquent de ne plus fonctionner. -->

<a id="streams"></a>

## Flux : futures en séquence

Rappelez-vous comment nous avons utilisé le récepteur de notre canal asynchrone plus tôt dans ce chapitre, dans la section [« Passage de messages »][17-02-messages]<!-- ignore -->. La méthode asynchrone `recv` produit une séquence d’éléments au fil du temps. C’est un exemple d’un modèle beaucoup plus général appelé _flux_. De nombreux concepts se représentent naturellement sous forme de flux : des éléments qui deviennent disponibles dans une file d’attente, des blocs de données récupérés progressivement dans le système de fichiers lorsque l’ensemble des données est trop volumineux pour tenir dans la mémoire de l’ordinateur, ou encore des données qui arrivent au fil du temps sur le réseau. Puisque les flux sont des futures, nous pouvons les utiliser avec tout autre type de future et les combiner de façon intéressante. Par exemple, nous pouvons regrouper des événements pour éviter de déclencher trop d’appels réseau, définir des délais d’expiration pour des séquences d’opérations de longue durée ou limiter la fréquence des événements de l’interface utilisateur pour éviter d’effectuer du travail inutile.

Nous avons vu une séquence d’éléments au chapitre 13, lorsque nous avons étudié le trait Iterator dans la section [« Le trait `Iterator` et la méthode `next` »][iterator-trait]<!--
ignore -->, mais il existe deux différences entre les itérateurs et le récepteur du canal asynchrone. La première concerne le temps : les itérateurs sont synchrones, tandis que le récepteur du canal est asynchrone. La deuxième différence concerne l’API. Lorsque nous utilisons directement `Iterator`, nous appelons sa méthode synchrone `next`. Avec le flux `trpl::Receiver` en particulier, nous avons plutôt appelé une méthode asynchrone `recv`. Autrement, ces API se ressemblent beaucoup, et ce n’est pas un hasard. Un flux est une forme asynchrone d’itération. Toutefois, alors que `trpl::Receiver` attend spécifiquement de recevoir des messages, l’API de flux à usage général est bien plus large : elle fournit l’élément suivant comme le fait `Iterator`, mais de manière asynchrone.

La ressemblance entre les itérateurs et les flux en Rust signifie que nous pouvons en fait créer un flux à partir de n’importe quel itérateur. Comme pour un itérateur, nous pouvons travailler avec un flux en appelant sa méthode `next`, puis en attendant son résultat, comme dans la liste 17-21, qui ne compilera pas encore.

<Listing number="17-21" caption="Créer un flux à partir d’un itérateur et afficher ses valeurs" file-name="src/main.rs">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch17-async-await/listing-17-21/src/main.rs:stream}}
```

</Listing>

Nous commençons par un tableau de nombres, que nous convertissons en itérateur, puis nous appelons `map` pour doubler toutes les valeurs. Nous convertissons ensuite l’itérateur en flux à l’aide de la fonction `trpl::stream_from_iter`. Enfin, nous parcourons les éléments du flux au fur et à mesure de leur arrivée à l’aide de la boucle `while let`.

Malheureusement, lorsque nous essayons d’exécuter le code, il ne compile pas et signale qu’aucune méthode `next` n’est disponible :

<!-- manual-regeneration
cd listings/ch17-async-await/listing-17-21
cargo build
copy only the error output
-->

```text
error[E0599]: no method named `next` found for struct `tokio_stream::iter::Iter` in the current scope
  --> src/main.rs:10:40
   |
10 |         while let Some(value) = stream.next().await {
   |                                        ^^^^
   |
   = help: items from traits can only be used if the trait is in scope
help: the following traits which provide `next` are implemented but not in scope; perhaps you want to import one of them
   |
1  + use crate::trpl::StreamExt;
   |
1  + use futures_util::stream::stream::StreamExt;
   |
1  + use std::iter::Iterator;
   |
1  + use std::str::pattern::Searcher;
   |
help: there is a method `try_next` with a similar name
   |
10 |         while let Some(value) = stream.try_next().await {
   |                                        ~~~~~~~~
```

Comme l’explique ce résultat, l’erreur du compilateur vient du fait que le trait approprié doit être dans la portée pour que nous puissions utiliser la méthode `next`. Au vu de notre discussion jusqu’ici, vous pourriez raisonnablement penser que ce trait est `Stream`, mais il s’agit en réalité de `StreamExt`. Abréviation de _extension_, `Ext` est un modèle courant dans la communauté Rust pour étendre un trait à l’aide d’un autre.

Le trait `Stream` définit une interface de bas niveau qui combine essentiellement les traits `Iterator` et `Future`. `StreamExt` fournit un ensemble d’API de plus haut niveau par-dessus `Stream`, notamment la méthode `next` ainsi que d’autres méthodes utilitaires similaires à celles du trait `Iterator`. `Stream` et `StreamExt` ne font pas encore partie de la bibliothèque standard de Rust, mais la plupart des crates de l’écosystème proposent des définitions similaires.

Pour corriger l’erreur du compilateur, il suffit d’ajouter une instruction `use` pour `trpl::StreamExt`, comme dans la liste 17-22.

<Listing number="17-22" caption="Utiliser correctement un itérateur comme base d’un flux" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-22/src/main.rs:all}}
```

</Listing>

Une fois tous ces éléments réunis, ce code fonctionne comme nous le souhaitons ! De plus, maintenant que `StreamExt` est dans la portée, nous pouvons utiliser toutes ses méthodes utilitaires, comme avec les itérateurs.

[17-02-messages]: ch17-02-concurrency-with-async.html#message-passing
[iterator-trait]: ch13-02-iterators.html#the-iterator-trait-and-the-next-method