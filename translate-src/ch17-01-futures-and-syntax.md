## Futures et syntaxe async

Les éléments clés de la programmation asynchrone en Rust sont les _futures_ et les mots-clés `async` et `await` de Rust.

Un _future_ est une valeur qui n’est peut-être pas encore prête, mais qui le sera à un moment donné dans le futur. (On retrouve ce même concept dans de nombreux langages, parfois sous d’autres noms, comme _task_ ou _promise_.) Rust fournit le trait `Future` comme élément de base afin que différentes opérations asynchrones puissent être implémentées avec différentes structures de données, tout en partageant une interface commune. En Rust, les futures sont des types qui implémentent le trait `Future`. Chaque future contient ses propres informations sur la progression de l’opération et sur ce que signifie être « prêt ».

Vous pouvez appliquer le mot-clé `async` à des blocs et à des fonctions pour indiquer qu’ils peuvent être interrompus puis repris. Dans un bloc ou une fonction async, vous pouvez utiliser le mot-clé `await` pour _attendre une future_ (c’est-à-dire attendre qu’elle soit prête). Chaque endroit où vous attendez une future dans un bloc ou une fonction async est un point potentiel où ce bloc ou cette fonction peut être mis en pause, puis repris. Le processus qui consiste à vérifier auprès d’une future si sa valeur est disponible s’appelle le _polling_.

D’autres langages, comme C# et JavaScript, utilisent aussi les mots-clés `async` et `await` pour la programmation asynchrone. Si vous connaissez ces langages, vous remarquerez peut-être des différences importantes dans la façon dont Rust gère cette syntaxe. Et c’est pour une bonne raison, comme nous le verrons !

Quand nous écrivons du code Rust asynchrone, nous utilisons la plupart du temps les mots-clés `async` et `await`. Rust les compile en code équivalent utilisant le trait `Future`, tout comme il compile les boucles `for` en code équivalent utilisant le trait `Iterator`. Toutefois, comme Rust fournit le trait `Future`, vous pouvez aussi l’implémenter pour vos propres types de données si nécessaire. Bon nombre des fonctions que nous verrons dans ce chapitre renvoient des types qui ont leur propre implémentation de `Future`. Nous reviendrons sur la définition du trait à la fin du chapitre et nous étudierons plus en détail son fonctionnement, mais ces explications suffisent pour poursuivre.

Tout cela peut sembler un peu abstrait. Écrivons donc notre premier programme asynchrone : un petit outil d’extraction de pages Web. Nous lui transmettrons deux URL sur la ligne de commande, il les récupérera simultanément et renverra le résultat de celle qui se termine en premier. Cet exemple introduira pas mal de nouvelle syntaxe, mais ne vous inquiétez pas : nous expliquerons tout ce que vous devez savoir au fur et à mesure.

## Notre premier programme asynchrone

Pour que ce chapitre reste consacré à l’apprentissage de l’asynchrone plutôt qu’à la gestion des différentes composantes de l’écosystème, nous avons créé la crate `trpl` (`trpl` est l’abréviation de « The Rust Programming Language »). Elle réexporte tous les types, traits et fonctions dont vous aurez besoin, provenant principalement des crates [`futures`][futures-crate]<!-- ignore --> et [`tokio`][tokio]<!-- ignore -->. La crate `futures` est un espace officiel d’expérimentation du code asynchrone en Rust ; c’est d’ailleurs là que le trait `Future` a été conçu à l’origine. Tokio est aujourd’hui le runtime asynchrone le plus utilisé en Rust, en particulier pour les applications Web. Il existe d’autres excellents runtimes, qui pourraient mieux convenir à vos besoins. Nous utilisons la crate `tokio` en arrière-plan pour `trpl`, car elle a été largement testée et est très utilisée.

Dans certains cas, `trpl` renomme ou enveloppe également les API d’origine afin de vous aider à vous concentrer sur les détails pertinents pour ce chapitre. Si vous souhaitez comprendre ce que fait cette crate, nous vous encourageons à consulter [son code source][crate-source]. Vous pourrez voir de quelle crate provient chaque réexportation, et nous avons laissé de nombreux commentaires expliquant ce que fait la crate.

Créez un nouveau projet binaire nommé `hello-async` et ajoutez la crate `trpl` comme dépendance :

```console
$ cargo new hello-async
$ cd hello-async
$ cargo add trpl
```

Nous pouvons maintenant utiliser les différents éléments fournis par `trpl` pour écrire notre premier programme asynchrone. Nous allons créer un petit outil en ligne de commande qui récupère deux pages Web, extrait l’élément `<title>` de chacune et affiche le titre de la page dont le processus se termine en premier.

### Définir la fonction page_title

Commençons par écrire une fonction qui prend l’URL d’une page en paramètre, envoie une requête à cette URL et renvoie le texte de l’élément `<title>` (voir Listing 17-1).

<Listing number="17-1" file-name="src/main.rs" caption="Définition d’une fonction asynchrone pour récupérer l’élément title d’une page HTML">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-01/src/main.rs:all}}
```

</Listing>

Tout d’abord, nous définissons une fonction nommée `page_title` et la marquons avec le mot-clé `async`. Ensuite, nous utilisons la fonction `trpl::get` pour récupérer l’URL qui lui est transmise, puis nous ajoutons le mot-clé `await` pour attendre la réponse. Pour obtenir le texte de `response`, nous appelons sa méthode `text`, puis nous l’attendons à nouveau avec le mot-clé `await`. Ces deux étapes sont asynchrones. Pour la fonction `get`, nous devons attendre que le serveur renvoie la première partie de sa réponse, qui comprendra les en-têtes HTTP, les cookies, etc., et qui peut être transmise séparément du corps de la réponse. Il peut falloir un certain temps avant que tout le contenu arrive, surtout si le corps est très volumineux. Comme nous devons attendre que la réponse _entière_ soit arrivée, la méthode `text` est elle aussi asynchrone.

Nous devons attendre explicitement ces deux futures, car les futures en Rust sont _paresseuses_ : elles ne font rien tant que vous ne leur demandez pas d’agir avec le mot-clé `await`. (En fait, Rust affiche un avertissement du compilateur si vous n’utilisez pas une future.) Cela peut vous rappeler ce que nous avons vu sur les itérateurs dans la section [« Traiter une série d’éléments avec des itérateurs »][iterators-lazy]<!-- ignore --> du chapitre 13. Les itérateurs ne font rien tant que vous n’appelez pas leur méthode `next`, directement ou au moyen de boucles `for` ou de méthodes comme `map`, qui utilisent `next` en interne. De même, les futures ne font rien tant que vous ne leur demandez pas explicitement d’agir. Cette paresse permet à Rust d’éviter d’exécuter du code asynchrone tant que cela n’est pas réellement nécessaire.

> Remarque : ce comportement diffère de celui que nous avons observé avec `thread::spawn` dans la section [« Créer un nouveau thread avec spawn »][thread-spawn]<!-- ignore --> du chapitre 16, où la fermeture que nous avons transmise à un autre thread a commencé à s’exécuter immédiatement. Il diffère aussi de l’approche de nombreux autres langages en matière de programmation asynchrone. Mais il est important que Rust puisse offrir ses garanties de performance, tout comme c’est le cas avec les itérateurs.

Une fois que nous avons `response_text`, nous pouvons l’analyser pour obtenir une instance du type `Html` à l’aide de `Html::parse`. Au lieu d’une chaîne brute, nous avons maintenant un type de données qui nous permet de manipuler le HTML sous la forme d’une structure de données plus riche. En particulier, nous pouvons utiliser la méthode `select_first` pour trouver la première occurrence d’un sélecteur CSS donné. En lui transmettant la chaîne `"title"`, nous obtenons le premier élément `<title>` du document, s’il y en a un. Comme il se peut qu’aucun élément ne corresponde, `select_first` renvoie un `Option<ElementRef>`. Enfin, nous utilisons la méthode `Option::map`, qui nous permet de manipuler l’élément contenu dans `Option` s’il est présent, et de ne rien faire dans le cas contraire. (Nous pourrions aussi utiliser une expression `match`, mais `map` est plus idiomatique.) Dans le corps de la fonction que nous fournissons à `map`, nous appelons `inner_html` sur `title` pour en obtenir le contenu, qui est une `String`. Au final, nous obtenons un `Option<String>`.

Remarquez que le mot-clé `await` de Rust se place _après_ l’expression attendue, et non avant. C’est donc un mot-clé _postfixe_. Cela diffère peut-être de ce que vous connaissez si vous avez utilisé `async` dans d’autres langages, mais en Rust, cette disposition facilite grandement l’utilisation des chaînes de méthodes. Nous pourrions donc modifier le corps de `page_title` pour chaîner les appels aux fonctions `trpl::get` et `text`, avec `await` entre les deux, comme le montre le Listing 17-2.

<Listing number="17-2" file-name="src/main.rs" caption="Chaînage avec le mot-clé `await`">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-02/src/main.rs:chaining}}
```

</Listing>

Nous avons ainsi écrit avec succès notre première fonction asynchrone ! Avant d’ajouter du code dans `main` pour l’appeler, parlons un peu plus de ce que nous avons écrit et de ce que cela signifie.

Lorsque Rust rencontre un _bloc_ marqué avec le mot-clé `async`, il le compile en un type de données anonyme et unique qui implémente le trait `Future`. Lorsqu’il rencontre une _fonction_ marquée avec `async`, il la compile en une fonction non asynchrone dont le corps est un bloc async. Le type de retour d’une fonction async est celui du type de données anonyme que le compilateur crée pour ce bloc async.

Ainsi, écrire `async fn` équivaut à écrire une fonction qui renvoie une _future_ du type de retour. Pour le compilateur, une définition de fonction telle que `async fn page_title` dans le Listing 17-1 est à peu près équivalente à une fonction non asynchrone définie comme suit :

```rust
# extern crate trpl; // required for mdbook test
use std::future::Future;
use trpl::Html;

fn page_title(url: &str) -> impl Future<Output = Option<String>> {
    async move {
        let text = trpl::get(url).await.text().await;
        Html::parse(&text)
            .select_first("title")
            .map(|title| title.inner_html())
    }
}
```

Examinons chaque partie de cette version transformée :

- Elle utilise la syntaxe `impl Trait`, abordée au chapitre 10 dans la section [« Les traits en tant que paramètres »][impl-trait]<!-- ignore -->.
- La valeur renvoyée implémente le trait `Future` avec un type associé `Output`. Remarquez que le type `Output` est `Option<String>`, comme le type de retour original de la version `async fn` de `page_title`.
- Tout le code appelé dans le corps de la fonction originale est enveloppé dans un bloc `async move`. N’oubliez pas que les blocs sont des expressions. Ce bloc entier est l’expression renvoyée par la fonction.
- Ce bloc async produit une valeur de type `Option<String>`, comme décrit ci-dessus. Cette valeur correspond au type `Output` indiqué dans le type de retour. C’est le même principe que pour les autres blocs que vous avez déjà vus.
- Le nouveau corps de fonction est un bloc `async move` en raison de son utilisation du paramètre `url`. (Nous parlerons beaucoup plus tard dans le chapitre de la différence entre `async` et `async move`.)

Nous pouvons maintenant appeler `page_title` dans `main`.

<!-- Old headings. Do not remove or links may break. -->

<a id ="determining-a-single-pages-title"></a>

### Exécuter une fonction asynchrone avec un runtime

Pour commencer, nous allons récupérer le titre d’une seule page, comme le montre le Listing 17-3. Malheureusement, ce code ne compile pas encore.

<Listing number="17-3" file-name="src/main.rs" caption="Appel de la fonction `page_title` depuis `main` avec un argument fourni par l’utilisateur">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch17-async-await/listing-17-03/src/main.rs:main}}
```

</Listing>

Nous suivons le même modèle que celui utilisé pour récupérer les arguments de la ligne de commande dans la section [« Accepter des arguments de ligne de commande »][cli-args]<!-- ignore --> du chapitre 12. Ensuite, nous transmettons l’argument URL à `page_title` et attendons le résultat. Comme la valeur produite par la future est un `Option<String>`, nous utilisons une expression `match` pour afficher différents messages selon que la page contient ou non un élément `<title>`.

Le seul endroit où nous pouvons utiliser le mot-clé `await` est dans des fonctions ou des blocs async, et Rust ne nous permet pas de marquer la fonction spéciale `main` comme étant `async`.

<!-- manual-regeneration
cd listings/ch17-async-await/listing-17-03
cargo build
copy just the compiler error
-->

```text
error[E0752]: `main` function is not allowed to be `async`
 --> src/main.rs:6:1
  |
6 | async fn main() {
  | ^^^^^^^^^^^^^^^ `main` function is not allowed to be `async`
```

La raison pour laquelle `main` ne peut pas être marquée `async` est que le code asynchrone a besoin d’un _runtime_ : une crate Rust qui gère les détails de l’exécution du code asynchrone. La fonction `main` d’un programme peut _initialiser_ un runtime, mais elle n’est pas elle-même un runtime. (Nous verrons bientôt plus en détail pourquoi.) Tout programme Rust qui exécute du code asynchrone doit comporter au moins un endroit où il configure un runtime chargé d’exécuter les futures.

La plupart des langages prenant en charge la programmation asynchrone incluent un runtime, mais Rust n’en fournit pas. Au contraire, il existe de nombreux runtimes asynchrones différents, chacun faisant des compromis adaptés au cas d’utilisation visé. Par exemple, un serveur Web à haut débit doté de nombreux cœurs de processeur et d’une grande quantité de mémoire vive a des besoins très différents de ceux d’un microcontrôleur à cœur unique, doté de peu de mémoire vive et incapable d’allouer de la mémoire sur le tas. Les crates qui fournissent ces runtimes proposent aussi souvent des versions asynchrones de fonctionnalités courantes, comme les entrées-sorties de fichiers ou de réseau.

Ici, et dans le reste de ce chapitre, nous utiliserons la fonction `block_on` de la crate `trpl`, qui prend une future en argument et bloque le thread courant jusqu’à ce que cette future s’exécute jusqu’à son terme. En coulisses, l’appel à `block_on` configure un runtime à l’aide de la crate `tokio`, qui sert à exécuter la future transmise (le comportement de `block_on` dans la crate `trpl` est similaire à celui des fonctions `block_on` d’autres crates de runtime). Une fois la future terminée, `block_on` renvoie la valeur produite par celle-ci.

Nous pourrions transmettre directement à `block_on` la future renvoyée par `page_title` et, une fois son exécution terminée, utiliser `match` sur le `Option<String>` obtenu, comme nous avons essayé de le faire dans le Listing 17-3. Cependant, dans la plupart des exemples de ce chapitre (et dans la plupart des applications asynchrones réelles), nous ferons plus qu’un simple appel à une fonction asynchrone. Nous transmettrons donc plutôt un bloc `async` et attendrons explicitement le résultat de l’appel à `page_title`, comme dans le Listing 17-4.

<Listing number="17-4" caption="Attente d’un bloc async avec `trpl::block_on`" file-name="src/main.rs">

<!-- should_panic,noplayground because mdbook test does not pass args -->

```rust,should_panic,noplayground
{{#rustdoc_include ../listings/ch17-async-await/listing-17-04/src/main.rs:run}}
```

</Listing>

Lorsque nous exécutons ce code, nous obtenons le comportement auquel nous nous attendions au départ :

<!-- manual-regeneration
cd listings/ch17-async-await/listing-17-04
cargo build # skip all the build noise
cargo run -- "https://www.rust-lang.org"
# copy the output here
-->

```console
$ cargo run -- "https://www.rust-lang.org"
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.05s
     Running `target/debug/async_await 'https://www.rust-lang.org'`
The title for https://www.rust-lang.org was
            Rust Programming Language
```

Ouf, nous avons enfin du code asynchrone qui fonctionne ! Mais avant d’ajouter le code permettant de mettre deux sites en concurrence, revenons brièvement au fonctionnement des futures.

Chaque _point d’attente_ — c’est-à-dire chaque endroit où le code utilise le mot-clé `await` — représente un point où le contrôle est rendu au runtime. Pour que cela fonctionne, Rust doit suivre l’état du bloc async afin que le runtime puisse lancer un autre travail, puis revenir lorsque celui-ci sera prêt à essayer de faire avancer à nouveau le premier. Il s’agit d’une machine à états invisible, comme si vous aviez écrit une énumération de ce genre pour enregistrer l’état courant à chaque point d’attente :

```rust
{{#rustdoc_include ../listings/ch17-async-await/no-listing-state-machine/src/lib.rs:enum}}
```

Écrire manuellement le code permettant de passer d’un état à l’autre serait fastidieux et source d’erreurs, surtout si vous devez ensuite ajouter des fonctionnalités et des états. Heureusement, le compilateur Rust crée et gère automatiquement les structures de données de la machine à états pour le code asynchrone. Toutes les règles normales d’emprunt et de propriété applicables aux structures de données s’appliquent toujours et, heureusement, le compilateur se charge aussi de les vérifier pour nous et fournit des messages d’erreur utiles. Nous examinerons quelques-uns de ces cas plus loin dans le chapitre.

En fin de compte, quelque chose doit exécuter cette machine à états : c’est le rôle d’un runtime. (C’est pourquoi vous rencontrerez peut-être le terme _executor_ en vous renseignant sur les runtimes : un executor est la partie d’un runtime chargée d’exécuter le code asynchrone.)

Vous comprenez maintenant pourquoi le compilateur nous a empêchés de faire de `main` une fonction asynchrone dans le Listing 17-3. Si `main` était une fonction asynchrone, autre chose devrait gérer la machine à états correspondant à la future renvoyée par `main`, alors que `main` est le point de départ du programme ! À la place, nous avons appelé la fonction `trpl::block_on` dans `main` pour configurer un runtime et exécuter la future renvoyée par le bloc `async` jusqu’à son terme.

> Remarque : certains runtimes fournissent des macros qui vous _permettent_ d’écrire une fonction `main` asynchrone. Ces macros réécrivent `async fn main() { ... }` sous la forme d’un `fn main` normal, qui fait la même chose que ce que nous avons fait manuellement dans le Listing 17-4 : appeler une fonction qui exécute une future jusqu’à son terme, comme le fait `trpl::block_on`.

Assemblons maintenant ces éléments pour voir comment écrire du code concurrent.

<!-- Old headings. Do not remove or links may break. -->

<a id="racing-our-two-urls-against-each-other"></a>

### Mettre deux URL en concurrence

Dans le Listing 17-5, nous appelons `page_title` avec deux URL différentes fournies sur la ligne de commande et les mettons en concurrence en sélectionnant la future qui se termine en premier.

<Listing number="17-5" caption="Appel de `page_title` pour deux URL afin de déterminer laquelle renvoie un résultat en premier" file-name="src/main.rs">

<!-- should_panic,noplayground because mdbook does not pass args -->

```rust,should_panic,noplayground
{{#rustdoc_include ../listings/ch17-async-await/listing-17-05/src/main.rs:all}}
```

</Listing>

Nous commençons par appeler `page_title` pour chacune des URL fournies par l’utilisateur. Nous enregistrons les futures obtenues dans `title_fut_1` et `title_fut_2`. N’oubliez pas qu’elles ne font encore rien, car les futures sont paresseuses et nous ne les avons pas encore attendues. Nous transmettons ensuite les futures à `trpl::select`, qui renvoie une valeur indiquant laquelle des futures transmises s’est terminée en premier.

> Remarque : en coulisses, `trpl::select` repose sur une fonction `select` plus générale définie dans la crate `futures`. La fonction `select` de la crate `futures` peut faire beaucoup de choses que la fonction `trpl::select` ne peut pas faire, mais elle est aussi plus complexe, ce que nous pouvons laisser de côté pour le moment.

L’une ou l’autre des futures peut légitimement « gagner » ; il n’est donc pas pertinent de renvoyer un `Result`. À la place, `trpl::select` renvoie un type que nous n’avons pas encore rencontré : `trpl::Either`. Le type `Either` ressemble quelque peu à `Result`, car il comporte deux variantes. Contrairement à `Result`, toutefois, `Either` ne distingue pas intrinsèquement les succès des échecs. Il utilise plutôt `Left` et `Right` pour indiquer « l’un ou l’autre » :

```rust
enum Either<A, B> {
    Left(A),
    Right(B),
}
```

La fonction `select` renvoie `Left` avec la sortie de la première future si le premier argument l’emporte, et `Right` avec la sortie de la seconde future si c’est celle-ci qui l’emporte. Cela correspond à l’ordre des arguments lors de l’appel de la fonction : le premier argument se trouve à gauche du second.

Nous modifions également `page_title` afin qu’elle renvoie l’URL transmise. Ainsi, si la page qui répond en premier ne contient pas de `<title>` exploitable, nous pouvons tout de même afficher un message pertinent. Avec ces informations, nous terminons en modifiant la sortie de `println!` pour indiquer à la fois quelle URL a terminé en premier et quel est, le cas échéant, l’élément `<title>` de la page Web correspondante.

Vous avez maintenant créé un petit outil d’extraction de pages Web fonctionnel ! Choisissez quelques URL et exécutez l’outil en ligne de commande. Vous découvrirez peut-être que certains sites sont systématiquement plus rapides que d’autres, tandis que, dans d’autres cas, le site le plus rapide varie d’une exécution à l’autre. Plus important encore, vous avez appris les bases de l’utilisation des futures ; nous pouvons donc maintenant étudier plus en profondeur ce que l’asynchrone nous permet de faire.

[impl-trait]: ch10-02-traits.html#traits-as-parameters
[iterators-lazy]: ch13-02-iterators.html
[thread-spawn]: ch16-01-threads.html#creating-a-new-thread-with-spawn
[cli-args]: ch12-01-accepting-command-line-arguments.html

<!-- TODO: map source link version to version of Rust? -->

[crate-source]: https://github.com/rust-lang/book/tree/main/packages/trpl
[futures-crate]: https://crates.io/crates/futures
[tokio]: https://tokio.rs