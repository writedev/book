## Futurs et la syntaxe Async

Les éléments clés de la programmation asynchrone en Rust sont les _futurs_ et les mots-clés `async` et `await`.

Un _futur_ est une valeur qui peut ne pas être prête maintenant, mais le sera à un moment donné dans le futur. (Ce même concept apparaît dans de nombreux langages, parfois sous d'autres noms tels que _tâche_ ou _promesse_.) Rust fournit un trait `Future` comme élément de base afin que différentes opérations asynchrones puissent être mises en œuvre avec différentes structures de données mais avec une interface commune. En Rust, les futurs sont des types qui implémentent le trait `Future`. Chaque futur détient ses propres informations sur les progrès réalisés et ce que "prêt" signifie.

Vous pouvez appliquer le mot-clé `async` à des blocs et des fonctions pour spécifier qu'ils peuvent être interrompus et repris. Dans un bloc asynchrone ou une fonction asynchrone, vous pouvez utiliser le mot-clé `await` pour _attendre un futur_ (c'est-à-dire attendre qu'il devienne prêt). Tout point où vous attendez un futur dans un bloc ou une fonction asynchrone est un endroit potentiel pour que ce bloc ou cette fonction fasse une pause et reprenne. Le processus de vérification avec un futur pour voir si sa valeur est déjà disponible s'appelle _polling_.

D'autres langages, comme C# et JavaScript, utilisent également les mots-clés `async` et `await` pour la programmation asynchrone. Si vous êtes familier avec ces langages, vous remarquerez certaines différences significatives dans la façon dont Rust gère la syntaxe. C'est pour de bonnes raisons, comme nous le verrons !

Lors de l'écriture de Rust asynchrone, nous utilisons le plus souvent les mots-clés `async` et `await`. Rust les compile en code équivalent en utilisant le trait `Future`, tout comme il compile les boucles `for` en code équivalent utilisant le trait `Iterator`. Cependant, comme Rust fournit le trait `Future`, vous pouvez également l'implémenter pour vos propres types de données lorsque vous en avez besoin. Beaucoup des fonctions que nous verrons tout au long de ce chapitre retournent des types avec leurs propres implémentations de `Future`. Nous reviendrons à la définition du trait à la fin du chapitre et examinerons davantage de son fonctionnement, mais ces détails suffisent pour nous faire avancer.

Tout cela peut sembler un peu abstrait, alors écrivons notre premier programme asynchrone : un petit scraper web. Nous passerons deux URL depuis la ligne de commande, récupérerons les deux de manière concurrente et retournerons le résultat de celle qui se termine en premier. Cet exemple aura un bon nombre de nouvelles syntaxes, mais ne vous inquiétez pas - nous expliquerons tout ce que vous devez savoir au fur et à mesure.

## Notre Premier Programme Asynchrone

Pour garder le focus de ce chapitre sur l'apprentissage de l'asynchrone plutôt que sur la jonglerie des parties de l'écosystème, nous avons créé le crate `trpl` (`trpl` est l'abréviation de "The Rust Programming Language"). Il réexporte tous les types, traits et fonctions dont vous aurez besoin, principalement depuis les crates [`futures`](https://crates.io/crates/futures) et [`tokio`](https://tokio.rs). Le crate `futures` est le foyer officiel pour l'expérimentation de Rust pour le code asynchrone, et c'est réellement là que le trait `Future` a été à l'origine conçu. Tokio est le runtime asynchrone le plus utilisé en Rust aujourd'hui, en particulier pour les applications web. Il existe d'autres excellents runtimes, et ils peuvent être plus adaptés à vos besoins. Nous utilisons le crate `tokio` en arrière-plan pour `trpl` parce qu'il est bien testé et largement utilisé.

Dans certains cas, `trpl` renomme ou enveloppe également les API d'origine pour vous garder concentré sur les détails pertinents à ce chapitre. Si vous voulez comprendre ce que fait le crate, nous vous encourageons à consulter [son code source](https://github.com/rust-lang/book/tree/main/packages/trpl). Vous pourrez voir de quel crate provient chaque ré-export, et nous avons laissé des commentaires détaillés expliquant ce que fait le crate.

Créez un nouveau projet binaire nommé `hello-async` et ajoutez le crate `trpl` en tant que dépendance :

```console
$ cargo new hello-async
$ cd hello-async
$ cargo add trpl
```

Nous pouvons maintenant utiliser les différentes pièces fournies par `trpl` pour écrire notre premier programme asynchrone. Nous allons construire un petit outil de ligne de commande qui récupère deux pages web, extrait l'élément `<title>` de chacune et imprime le titre de la page qui termine tout le processus en premier.

### Définir la Fonction page_title

Commençons par écrire une fonction qui prend une URL de page comme paramètre, fait une requête et retourne le texte de l'élément `<title>` (voir l'énoncé 17-1).

<Listing number="17-1" file-name="src/main.rs" caption="Définir une fonction asynchrone pour obtenir l'élément titre d'une page HTML">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-01/src/main.rs:all}}
```

</Listing>

Tout d'abord, nous définissons une fonction nommée `page_title` et nous la marquons avec le mot-clé `async`. Ensuite, nous utilisons la fonction `trpl::get` pour récupérer l'URL passée et ajoutons le mot-clé `await` pour attendre la réponse. Pour obtenir le texte de la `response`, nous appelons sa méthode `text` et attendons à nouveau avec le mot-clé `await`. Ces deux étapes sont asynchrones. Pour la fonction `get`, nous devons attendre que le serveur renvoie la première partie de sa réponse, qui comprendra des en-têtes HTTP, des cookies, etc. et peut être livrée séparément du corps de la réponse. En particulier si le corps est très large, cela peut prendre un certain temps avant que tout n'arrive. Comme nous devons attendre pour la _totalité_ de la réponse, la méthode `text` est également asynchrone.

Nous devons explicitement attendre ces deux futurs, car les futurs en Rust sont _paresseux_ : ils ne font rien tant que vous ne leur demandez pas avec le mot-clé `await`. (En fait, Rust affichera un avertissement du compilateur si vous n'utilisez pas un futur.) Cela peut vous rappeler la discussion sur les itérateurs dans la section [« Traitement d'une série d'éléments avec des Itérateurs »](https://doc.rust-lang.org/book/ch13-02-iterators.html) du chapitre 13. Les itérateurs ne font rien à moins que vous n'appeliez leur méthode `next` — que ce soit directement ou en utilisant des boucles `for` ou des méthodes telles que `map` qui utilisent `next` en arrière-plan. De même, les futurs ne font rien à moins que vous ne leur demandiez explicitement. Cette paresse permet à Rust d'éviter d'exécuter du code asynchrone jusqu'à ce qu'il soit réellement nécessaire.

> Remarque : Cela est différent du comportement que nous avons vu lors de l'utilisation de `thread::spawn` dans la section [« Création d'un nouveau thread avec spawn »](https://doc.rust-lang.org/book/ch16-01-threads.html#creating-a-new-thread-with-spawn) du chapitre 16, où la fermeture que nous avons passée à un autre thread a commencé à s'exécuter immédiatement. C'est également différent de la façon dont de nombreux autres langages abordent l'async. Mais il est important pour Rust de pouvoir fournir ses garanties de performance, tout comme c'est le cas avec les itérateurs.

Une fois que nous avons `response_text`, nous pouvons le parser en une instance du type `Html` en utilisant `Html::parse`. Au lieu d'une chaîne brute, nous avons désormais un type de données que nous pouvons utiliser pour travailler avec le HTML comme une structure de données plus riche. En particulier, nous pouvons utiliser la méthode `select_first` pour trouver la première instance d'un sélecteur CSS donné. En passant la chaîne `"title"`, nous obtiendrons le premier élément `<title>` dans le document, s'il y en a un. Comme il se peut qu'il n'y ait aucun élément correspondant, `select_first` retourne un `Option<ElementRef>`. Enfin, nous utilisons la méthode `Option::map`, qui nous permet de travailler avec l'élément dans l'Option s'il est présent, et de ne rien faire s'il ne l'est pas. (Nous pourrions également utiliser une expression `match` ici, mais `map` est plus idiomatique.) Dans le corps de la fonction que nous fournissons à `map`, nous appelons `inner_html` sur le `title` pour obtenir son contenu, qui est une `String`. Quand tout est dit et fait, nous avons un `Option<String>`.

Remarquez que le mot-clé `await` de Rust se situe _après_ l'expression que vous attendez, pas avant. C'est-à-dire qu'il s'agit d'un mot-clé _postfix_. Cela peut différer de ce à quoi vous êtes habitué si vous avez utilisé `async` dans d'autres langages, mais en Rust, cela rend les chaînes de méthodes beaucoup plus agréables à travailler. En conséquence, nous pourrions changer le corps de `page_title` pour chaîner les appels de fonction `trpl::get` et `text` ensemble avec `await` entre eux, comme montré dans l'énoncé 17-2.

<Listing number="17-2" file-name="src/main.rs" caption="Chaînage avec le mot-clé `await`">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-02/src/main.rs:chaining}}
```

</Listing>

Avec cela, nous avons réussi à écrire notre première fonction asynchrone ! Avant d'ajouter du code dans `main` pour l'appeler, parlons un peu plus de ce que nous avons écrit et ce que cela signifie.

Lorsque Rust voit un _bloc_ marqué avec le mot-clé `async`, il le compile en un type de données unique et anonyme qui implémente le trait `Future`. Lorsque Rust voit une _fonction_ marquée avec `async`, il la compile en une fonction non asynchrone dont le corps est un bloc asynchrone. Le type de retour d'une fonction asynchrone est le type du type de données anonyme que le compilateur crée pour ce bloc asynchrone.

Ainsi, écrire `async fn` est équivalent à écrire une fonction qui retourne un _futur_ du type de retour. Pour le compilateur, une définition de fonction telle que `async fn page_title` dans l'énoncé 17-1 est à peu près équivalente à une fonction non asynchrone définie comme suit :

```rust
# extern crate trpl; // requis pour le test de mdbook
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

Passons en revue chaque partie de la version transformée :

- Elle utilise la syntaxe `impl Trait` que nous avons discutée dans le chapitre 10 dans la section [« Traits comme Paramètres »](https://doc.rust-lang.org/book/ch10-02-traits.html#traits-as-parameters).
- La valeur retournée implémente le trait `Future` avec un type associé de `Output`. Remarquez que le type `Output` est `Option<String>`, qui est le même que le type de retour original de la version `async fn` de `page_title`.
- Tout le code appelé dans le corps de la fonction originale est enveloppé dans un bloc `async move`. N'oubliez pas que les blocs sont des expressions. Ce bloc entier est l'expression retournée par la fonction.
- Ce bloc asynchrone produit une valeur du type `Option<String>`, comme décrit précédemment. Cette valeur correspond au type `Output` dans le type de retour. C'est exactement comme d'autres blocs que vous avez déjà vus.
- Le nouveau corps de fonction est un bloc `async move` en raison de la manière dont il utilise le paramètre `url`. (Nous parlerons beaucoup plus de `async` par rapport à `async move` plus loin dans le chapitre.)

Maintenant, nous pouvons appeler `page_title` dans `main`.

### Exécuter une Fonction Asynchrone avec un Runtime

Pour commencer, nous allons obtenir le titre pour une seule page, comme montré dans l'énoncé 17-3. Malheureusement, ce code ne compile pas encore.

<Listing number="17-3" file-name="src/main.rs" caption="Appel de la fonction `page_title` depuis `main` avec un argument fourni par l'utilisateur">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch17-async-await/listing-17-03/src/main.rs:main}}
```

</Listing>

Nous suivons le même schéma que nous avons utilisé pour obtenir des arguments de ligne de commande dans la section [« Acceptation des Arguments de Ligne de Commande »](https://doc.rust-lang.org/book/ch12-01-accepting-command-line-arguments.html) du chapitre 12. Ensuite, nous passons l'argument URL à `page_title` et attendons le résultat. Comme la valeur produite par le futur est un `Option<String>`, nous utilisons une expression `match` pour imprimer différents messages selon que la page avait un `<title>`.

Le seul endroit où nous pouvons utiliser le mot-clé `await` est dans des fonctions ou blocs asynchrones, et Rust ne nous permettra pas de marquer la fonction spéciale `main` comme `async`.

```text
error[E0752]: `main` function is not allowed to be `async`
 --> src/main.rs:6:1
  |
6 | async fn main() {
  | ^^^^^^^^^^^^^^^ `main` function is not allowed to be `async`
```

La raison pour laquelle `main` ne peut pas être marqué `async` est que le code asynchrone nécessite un _runtime_ : un crate Rust qui gère les détails de l'exécution du code asynchrone. La fonction `main` d'un programme peut _initialiser_ un runtime, mais ce n'est pas un runtime _lui-même_. (Nous verrons plus tard pourquoi c'est le cas.) Chaque programme Rust qui exécute du code asynchrone a au moins un endroit où il met en place un runtime pour exécuter les futurs.

La plupart des langages qui prennent en charge l'asynchrone intègrent un runtime, mais Rust ne le fait pas. Au lieu de cela, il existe de nombreux runtimes asynchrones disponibles, chacun d'eux faisant des compromis différents adaptés à l'utilisation qu'il cible. Par exemple, un serveur web à haut débit avec de nombreux cœurs de CPU et une grande quantité de RAM a des besoins très différents d'un microcontrôleur avec un seul cœur, peu de RAM et sans capacité d'allocation de tas. Les crates qui fournissent ces runtimes fournissent également souvent des versions asynchrones des fonctionnalités courantes telles que les E/S de fichiers ou réseau.

Ici, et tout au long du reste de ce chapitre, nous utiliserons la fonction `block_on` du crate `trpl`, qui prend un futur comme argument et bloque le thread actuel jusqu'à ce que ce futur s'exécute jusqu'à sa fin. En arrière-plan, appeler `block_on` met en place un runtime utilisant le crate `tokio` qui est utilisé pour exécuter le futur passé (le comportement de `block_on` du crate `trpl` est similaire aux fonctions `block_on` d'autres crates de runtime). Une fois le futur terminé, `block_on` retourne la valeur produite par le futur.

Nous pourrions passer directement le futur renvoyé par `page_title` à `block_on` et, une fois qu'il serait terminé, nous pourrions utiliser un `match` sur le `Option<String>` résultant comme nous avons essayé de le faire dans l'énoncé 17-3. Cependant, pour la plupart des exemples dans le chapitre (et la plupart du code asynchrone dans le monde réel), nous ferons plus d'un appel de fonction asynchrone, donc à la place, nous passerons un bloc `async` et attendrons explicitement le résultat de l'appel à `page_title`, comme dans l'énoncé 17-4.

<Listing number="17-4" caption="Attendre un bloc asynchrone avec `trpl::block_on`" file-name="src/main.rs">

```rust,should_panic,noplayground
{{#rustdoc_include ../listings/ch17-async-await/listing-17-04/src/main.rs:run}}
```

</Listing>

Lorsque nous exécutons ce code, nous obtenons le comportement que nous attendions initialement :

```console
$ cargo run -- "https://www.rust-lang.org"
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.05s
     Running `target/debug/async_await 'https://www.rust-lang.org'`
Le titre pour https://www.rust-lang.org était
            Rust Programming Language
```

Ouf - nous avons enfin du code asynchrone fonctionnel ! Mais avant d'ajouter le code pour faire la course entre deux sites, tournons brièvement notre attention sur le fonctionnement des futurs.

Chaque _point d'attente_ — c'est-à-dire chaque endroit où le code utilise le mot-clé `await` — représente un endroit où le contrôle est remis au runtime. Pour que cela fonctionne, Rust doit garder une trace de l'état impliqué dans le bloc asynchrone afin que le runtime puisse commencer un autre travail et revenir quand il est prêt à essayer d'avancer le premier à nouveau. C'est une machine d'état invisible, comme si vous aviez écrit une énumération comme celle-ci pour sauvegarder l'état actuel à chaque point d'attente :

```rust
{{#rustdoc_include ../listings/ch17-async-await/no-listing-state-machine/src/lib.rs:enum}}
```

Écrire le code pour passer d'un état à l'autre à la main serait ennuyeux et propice aux erreurs, surtout lorsque vous devez ajouter plus de fonctionnalités et plus d'états au code par la suite. Heureusement, le compilateur Rust crée et gère automatiquement les structures de données de la machine d'état pour le code asynchrone. Les règles normales d'emprunt et de propriété autour des structures de données s'appliquent toujours, et heureusement, le compilateur s'occupe également de vérifier cela pour nous et fournit des messages d'erreur utiles. Nous travaillerons sur quelques-uns de ceux-ci plus tard dans le chapitre.

En fin de compte, quelque chose doit exécuter cette machine d'état, et c'est précisément ce que fait un runtime. (C'est pourquoi vous pouvez rencontrer des mentions d'_exécuteurs_ en regardant les runtimes : un exécuteur est la partie d'un runtime responsable de l'exécution du code asynchrone.)

Maintenant, vous pouvez voir pourquoi le compilateur nous a empêchés de faire de `main` lui-même une fonction asynchrone dans l'énoncé 17-3. Si `main` était une fonction asynchrone, quelque chose d'autre devrait gérer la machine d'état pour quoi que ce soit que le futur `main` retourna, mais `main` est le point de départ du programme ! Au lieu de cela, nous avons appelé la fonction `trpl::block_on` dans `main` pour mettre en place un runtime et exécuter le futur retourné par le bloc `async` jusqu'à ce qu'il soit terminé.

> Remarque : Certains runtimes fournissent des macros pour que vous _puissiez_ écrire une fonction `main` asynchrone. Ces macros réécrivent `async fn main() { ... }` pour être un `fn main` normal, ce qui fait la même chose que nous avons fait à la main dans l'énoncé 17-4 : appeler une fonction qui exécute un futur jusqu'à sa complétion de la manière dont `trpl::block_on` le fait.

Mettons maintenant ces pièces ensemble et voyons comment nous pouvons écrire du code concurrent.

### Faire Concourir Deux URL

Dans l'énoncé 17-5, nous appelons `page_title` avec deux URL différentes passées depuis la ligne de commande et les faisons concourir en sélectionnant le futur qui se termine en premier.

<Listing number="17-5" caption="Appel de `page_title` pour deux URL pour voir laquelle retourne en premier" file-name="src/main.rs">

```rust,should_panic,noplayground
{{#rustdoc_include ../listings/ch17-async-await/listing-17-05/src/main.rs:all}}
```

</Listing>

Nous commençons par appeler `page_title` pour chacune des URL fournies par l'utilisateur. Nous enregistrons les futurs résultants comme `title_fut_1` et `title_fut_2`. N'oubliez pas que ceux-ci ne font rien encore, car les futurs sont paresseux et nous ne les avons pas encore attendus. Ensuite, nous passons les futurs à `trpl::select`, qui retourne une valeur pour indiquer lequel des futurs passés s'achève le premier.

> Remarque : En coulisses, `trpl::select` est construit sur une fonction `select` plus générale définie dans le crate `futures`. La fonction `select` du crate `futures` peut faire beaucoup de choses que la fonction `trpl::select` ne peut pas, mais elle a également une complexité supplémentaire que nous pouvons ignorer pour l'instant.

L'un ou l'autre futur peut légitimement "gagner", donc il n'est pas logique de retourner un `Result`. Au lieu de cela, `trpl::select` retourne un type que nous n'avons pas encore vu, `trpl::Either`. Le type `Either` est quelque peu similaire à un `Result` en ce sens qu'il a deux cas. Contrairement à `Result`, cependant, il n'y a aucune notion de succès ou d'échec intégrée dans `Either`. Au lieu de cela, il utilise `Left` et `Right` pour indiquer "l'un ou l'autre" :

```rust
enum Either<A, B> {
    Left(A),
    Right(B),
}
```

La fonction `select` retourne `Left` avec la sortie de ce futur si le premier argument gagne, et `Right` avec la sortie du deuxième futur argument si _celui-là_ gagne. Cela correspond à l'ordre dans lequel les arguments apparaissent lors de l'appel de la fonction : le premier argument est à gauche du deuxième argument.

Nous mettons également à jour `page_title` pour retourner la même URL que celle passée. De cette manière, si la page qui se termine en premier n'a pas de `<title>` que nous puissions résoudre, nous pouvons tout de même imprimer un message significatif. Avec ces informations à disposition, nous terminons en mettant à jour notre sortie `println!` pour indiquer à la fois quelle URL s'est terminée en premier et quel est, le cas échéant, le `<title>` de la page web à cette URL.

Vous avez construit un petit scraper web fonctionnel maintenant ! Choisissez quelques URL et exécutez l'outil de ligne de commande. Vous pouvez découvrir que certains sites sont constamment plus rapides que d'autres, tandis que dans d'autres cas, le site le plus rapide varie d'exécution à exécution. Plus important encore, vous avez appris les bases du travail avec les futurs, donc maintenant nous pouvons approfondir ce que nous pouvons faire avec l'asynchrone.