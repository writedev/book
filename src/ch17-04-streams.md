<!-- Anciens titres. Ne pas supprimer ou les liens risquent de ne plus fonctionner. -->

<a id="streams"></a>

## Flux : Avenir en Séquence

Rappelons comment nous avons utilisé le récepteur pour notre canal asynchrone plus tôt dans ce chapitre dans la section [“Transmission de Messages”][17-02-messages]<!-- ignore -->. La méthode asynchrone `recv` produit une séquence d'éléments au fil du temps. C'est un exemple d'un modèle beaucoup plus général connu sous le nom de _flux_. De nombreux concepts sont naturellement représentés sous forme de flux : des éléments devenant disponibles dans une file d'attente, des morceaux de données étant extraits progressivement du système de fichiers lorsque l'ensemble de données est trop volumineux pour la mémoire de l'ordinateur, ou des données arrivant par le réseau au fil du temps. Étant donné que les flux sont des futurs, nous pouvons les utiliser avec tout autre type de futur et les combiner de manière intéressante. Par exemple, nous pouvons regrouper des événements pour éviter de déclencher trop d'appels réseau, définir des délais sur des séquences d'opérations de longue durée, ou réguler les événements de l'interface utilisateur pour éviter de faire du travail inutile.

Nous avons vu une séquence d'éléments dans le chapitre 13, lorsque nous avons examiné le trait Iterator dans la section [“Le Trait Iterator et la Méthode `next`”][iterator-trait]<!-- ignore -->, mais il y a deux différences entre les itérateurs et le récepteur de canal asynchrone. La première différence est le temps : les itérateurs sont synchrones, tandis que le récepteur de canal est asynchrone. La deuxième différence est l'API. Lorsque nous travaillons directement avec `Iterator`, nous appelons sa méthode synchrone `next`. Avec le flux `trpl::Receiver` en particulier, nous avons plutôt appelé une méthode asynchrone `recv`. Sinon, ces API semblent très similaires, et cette similarité n'est pas une coïncidence. Un flux est comme une forme asynchrone d'itération. Alors que le `trpl::Receiver` attend spécifiquement de recevoir des messages, l'API de flux général est beaucoup plus vaste : elle fournit le prochain élément comme le fait `Iterator`, mais de manière asynchrone.

La similarité entre les itérateurs et les flux en Rust signifie que nous pouvons en réalité créer un flux à partir de n'importe quel itérateur. Comme avec un itérateur, nous pouvons travailler avec un flux en appelant sa méthode `next` et en attendant la sortie, comme dans l'Extrait 17-21, qui ne compilera pas encore.

<Listing number="17-21" caption="Créer un flux à partir d'un itérateur et imprimer ses valeurs" file-name="src/main.rs">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch17-async-await/listing-17-21/src/main.rs:stream}}
```

</Listing>

Nous commençons avec un tableau de nombres, que nous convertissons en un itérateur et sur lequel nous appelons `map` pour doubler toutes les valeurs. Ensuite, nous convertissons l'itérateur en un flux en utilisant la fonction `trpl::stream_from_iter`. Ensuite, nous parcourons les éléments dans le flux au fur et à mesure de leur arrivée avec la boucle `while let`.

Malheureusement, lorsque nous essayons d'exécuter le code, il ne compile pas mais indique plutôt qu'il n'y a pas de méthode `next` disponible :

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

Comme l'indique cette sortie, la raison de l'erreur du compilateur est que nous avons besoin du bon trait dans la portée pour pouvoir utiliser la méthode `next`. Étant donné notre discussion jusqu'ici, on pourrait raisonnablement s'attendre à ce que ce trait soit `Stream`, mais il s'agit en fait de `StreamExt`. Abrégé en _extension_, `Ext` est un motif courant dans la communauté Rust pour étendre un trait par un autre.

Le trait `Stream` définit une interface de bas niveau qui combine efficacement les traits `Iterator` et `Future`. `StreamExt` fournit un ensemble d'APIs de haut niveau au-dessus de `Stream`, incluant la méthode `next` ainsi que d'autres méthodes utilitaires similaires à celles fournies par le trait `Iterator`. `Stream` et `StreamExt` ne font pas encore partie de la bibliothèque standard de Rust, mais la plupart des crates de l'écosystème utilisent des définitions similaires.

La solution à l'erreur de compilation est d'ajouter une instruction `use` pour `trpl::StreamExt`, comme dans l'Extrait 17-22.

<Listing number="17-22" caption="Utiliser avec succès un itérateur comme base pour un flux" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-22/src/main.rs:all}}
```

</Listing>

Avec tous ces éléments rassemblés, ce code fonctionne comme nous le souhaitons ! De plus, maintenant que nous avons `StreamExt` dans la portée, nous pouvons utiliser toutes ses méthodes utilitaires, tout comme avec les itérateurs.

[17-02-messages]: ch17-02-concurrency-with-async.html#message-passing
[iterator-trait]: ch13-02-iterators.html#the-iterator-trait-and-the-next-method