<!-- Old headings. Do not remove or links may break. -->

<a id="digging-into-the-traits-for-async"></a>

## Un Regard Plus Approfondi sur les Traits pour Async

Tout au long du chapitre, nous avons utilisé les traits `Future`, `Stream` et `StreamExt` de différentes manières. Jusqu’à présent, nous avons évité de nous plonger trop profondément dans les détails de leur fonctionnement ou de la façon dont ils s'articulent, ce qui est généralement suffisant pour votre travail quotidien en Rust. Cependant, il peut arriver que vous rencontriez des situations où il est nécessaire de comprendre quelques détails supplémentaires de ces traits, ainsi que du type `Pin` et du trait `Unpin`. Dans cette section, nous allons explorer ces concepts juste assez pour vous aider dans ces scénarios, tout en laissant l’immersion _vraiment_ approfondie pour d'autres documentations.

<!-- Old headings. Do not remove or links may break. -->

<a id="future"></a>

### Le Trait `Future`

Commençons par un examen plus approfondi de la manière dont le trait `Future` fonctionne. Voici comment Rust le définit :

```rust
use std::pin::Pin;
use std::task::{Context, Poll};

pub trait Future {
    type Output;

    fn poll(self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<Self::Output>;
}
```

Cette définition de trait inclut plusieurs nouveaux types et également une syntaxe que nous n'avons pas encore vue, alors examinons la définition pièce par pièce.

Tout d'abord, le type associé `Output` de `Future` indique ce à quoi le futur se résout. Cela est analogue au type associé `Item` pour le trait `Iterator`. Deuxièmement, `Future` a la méthode `poll`, qui prend une référence `Pin` spéciale pour son paramètre `self` et une référence mutable au type `Context`, et retourne un `Poll<Self::Output>`. Nous parlerons plus en détail de `Pin` et de `Context` dans un instant. Pour l’instant, concentrons-nous sur ce que la méthode retourne, le type `Poll` :

```rust
pub enum Poll<T> {
    Ready(T),
    Pending,
}
```

Ce type `Poll` est similaire à un `Option`. Il a une variante qui a une valeur, `Ready(T)`, et une qui n’a pas, `Pending`. Cependant, `Poll` signifie quelque chose de très différent de `Option` ! La variante `Pending` indique que le futur doit encore accomplir un travail, donc l'appelant devra vérifier à nouveau plus tard. La variante `Ready` indique que le `Future` a terminé son travail et que la valeur `T` est disponible.

> Remarque : Il est rare d'avoir besoin d'appeler `poll` directement, mais si vous devez le faire, gardez à l'esprit qu'avec la plupart des futurs, l'appelant ne doit pas rappeler `poll` après que le futur ait retourné `Ready`. De nombreux futurs provoqueront une panique s'ils sont consultés à nouveau après être devenus prêts. Les futurs qui sont sans danger à poller à nouveau le diront explicitement dans leur documentation. Cela est similaire à la façon dont `Iterator::next` se comporte.

Lorsque vous voyez du code utilisant `await`, Rust le compile en interne en code qui appelle `poll`. Si vous regardez à nouveau la Listing 17-4, où nous avons imprimé le titre de la page pour une URL unique une fois qu'elle a été résolue, Rust le compile en quelque chose comme ceci (bien que ce ne soit pas exactement le cas) :

```rust,ignore
match page_title(url).poll() {
    Ready(page_title) => match page_title {
        Some(title) => println!("Le titre pour {url} était {title}"),
        None => println!("{url} n'avait pas de titre"),
    }
    Pending => {
        // Mais que mettons ici ?
    }
}
```

Que devons-nous faire lorsque le futur est toujours `Pending` ? Nous avons besoin d'un moyen d'essayer encore, encore et encore, jusqu'à ce que le futur soit enfin prêt. En d'autres termes, nous avons besoin d'une boucle :

```rust,ignore
let mut page_title_fut = page_title(url);
loop {
    match page_title_fut.poll() {
        Ready(value) => match page_title {
            Some(title) => println!("Le titre pour {url} était {title}"),
            None => println!("{url} n'avait pas de titre"),
        }
        Pending => {
            // continuer
        }
    }
}
```

Cependant, si Rust le compilait exactement en ce code, chaque `await` serait bloquant—exactement l'opposé de ce que nous souhaitions ! Au lieu de cela, Rust veille à ce que la boucle puisse céder le contrôle à quelque chose qui peut suspendre le travail sur ce futur pour travailler sur d'autres futurs, puis vérifier à nouveau ce dernier plus tard. Comme nous l'avons vu, cela est géré par un runtime async, et ce travail de planification et de coordination est l'un de ses principaux rôles.

Dans la section [“Envoyer des données entre deux tâches en utilisant le passage de messages”][message-passing]<!-- ignore -->, nous avons décrit l'attente sur `rx.recv`. L'appel `recv` retourne un futur, et attendre ce futur le poll. Nous avons noté qu'un runtime mettra le futur en pause jusqu'à ce qu'il soit prêt avec soit `Some(message)`, soit `None` lorsque le canal est fermé. Avec notre compréhension plus approfondie du trait `Future`, et spécifiquement de `Future::poll`, nous pouvons voir comment cela fonctionne. Le runtime sait que le futur n'est pas prêt lorsqu'il retourne `Poll::Pending`. À l'inverse, le runtime sait que le futur _est_ prêt et l'avance lorsque `poll` retourne `Poll::Ready(Some(message))` ou `Poll::Ready(None)`.

Les détails exacts de la façon dont un runtime fait cela sont au-delà de la portée de ce livre, mais l'essentiel est de voir les mécanismes de base des futurs : un runtime _poll_ chaque futur dont il est responsable, remettant le futur en sommeil lorsqu'il n'est pas encore prêt.

<!-- Old headings. Do not remove or links may break. -->

<a id="pinning-and-the-pin-and-unpin-traits"></a>
<a id="the-pin-and-unpin-traits"></a>

### Le Type `Pin` et le Trait `Unpin`

Dans la Listing 17-13, nous avons utilisé le macro `trpl::join!` pour attendre trois futurs. Cependant, il est courant d'avoir une collection comme un vecteur contenant un certain nombre de futurs qui ne seront pas connus jusqu'à l'exécution. Changeons la Listing 17-13 pour le code de la Listing 17-23 qui place les trois futurs dans un vecteur et appelle la fonction `trpl::join_all` à la place, qui ne compilera pas encore.

<Listing number="17-23" caption="Attendre des futurs dans une collection"  file-name="src/main.rs">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch17-async-await/listing-17-23/src/main.rs:here}}
```

</Listing>

Nous avons mis chaque futur dans un `Box` pour les transformer en _objets trait_, tout comme nous l’avons fait dans la section “Retourner des erreurs de `run`” au chapitre 12. (Nous allons traiter des objets trait en détail au chapitre 18.) L'utilisation d'objets trait nous permet de traiter chacun des futurs anonymes produits par ces types comme étant du même type, car tous implémentent le trait `Future`.

Cela pourrait être surprenant. Après tout, aucun des blocs async ne retourne quoi que ce soit, donc chacun produit un `Future<Output = ()>`. Rappelez-vous que `Future` est un trait, et que le compilateur crée une énumération unique pour chaque bloc async, même s'ils ont des types de sortie identiques. Tout comme vous ne pouvez pas mettre deux structures manuscrites différentes dans un `Vec`, vous ne pouvez pas mélanger des énumérations générées par le compilateur.

Ensuite, nous passons la collection de futurs à la fonction `trpl::join_all` et attendons le résultat. Cependant, cela ne compile pas ; voici la partie pertinente des messages d'erreur.

```text
error[E0277]: `dyn Future<Output = ()>` cannot be unpinned
  --> src/main.rs:48:33
   |
48 |         trpl::join_all(futures).await;
   |                                 ^^^^^ le trait `Unpin` n'est pas implémenté pour `dyn Future<Output = ()>`
   |
   = note: envisagez d'utiliser le macro `pin!`
           envisagez d'utiliser `Box::pin` si vous avez besoin d'accéder à la valeur épinglée en dehors du contexte actuel
   = note: requis pour que `Box<dyn Future<Output = ()>>` implémente `Future`
note: requis par une contrainte dans`futures_util::future::join_all::JoinAll`
  --> file:///home/.cargo/registry/src/index.crates.io-1949cf8c6b5b557f/futures-util-0.3.30/src/future/join_all.rs:29:8
   |
27 | pub struct JoinAll<F>
   |            ------- requis par une contrainte dans cette structure
28 | where
29 |     F: Future,
   |        ^^^^^^ requis par cette contrainte dans `JoinAll`
```

La note dans ce message d'erreur nous dit que nous devrions utiliser le macro `pin!` pour _épingle_ les valeurs, ce qui signifie les mettre à l'intérieur du type `Pin` qui garantit que les valeurs ne seront pas déplacées en mémoire. Le message d'erreur indique que l'épinglage est requis parce que `dyn Future<Output = ()>` doit implémenter le trait `Unpin` et qu'il ne le fait actuellement pas.

La fonction `trpl::join_all` retourne une structure appelée `JoinAll`. Cette structure est générique sur un type `F`, qui est contraint d'implémenter le trait `Future`. Attendre directement un futur avec `await` épingle implicitement le futur. C'est pourquoi nous n'avons pas besoin d'utiliser `pin!` partout où nous voulons attendre des futurs.

Cependant, nous n'attendons pas directement un futur ici. Au lieu de cela, nous construisons un nouveau futur, `JoinAll`, en passant une collection de futurs à la fonction `join_all`. La signature pour `join_all` exige que les types des éléments de la collection implémentent tous le trait `Future`, et `Box<T>` implémente `Future` uniquement si le `T` qu'il enveloppe est un futur qui implémente le trait `Unpin`.

C'est beaucoup à digérer ! Pour vraiment comprendre cela, plongeons un peu plus dans la manière dont le trait `Future` fonctionne réellement, en particulier autour de l'épinglage. Regardez à nouveau la définition du trait `Future` :

```rust
use std::pin::Pin;
use std::task::{Context, Poll};

pub trait Future {
    type Output;

    // Méthode requise
    fn poll(self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<Self::Output>;
}
```

Le paramètre `cx` et son type `Context` sont la clé de la façon dont un runtime sait réellement quand vérifier un futur donné tout en restant paresseux. Encore une fois, les détails de la façon dont cela fonctionne sont au-delà de la portée de ce chapitre, et vous n’avez généralement besoin d'y penser que lors de l’écriture d’une implémentation personnalisée de `Future`. Nous nous concentrerons plutôt sur le type pour `self`, car c’est la première fois que nous voyons une méthode où `self` a une annotation de type. Une annotation de type pour `self` fonctionne comme des annotations de type pour d'autres paramètres de fonction, mais avec deux différences clés :

- Cela indique à Rust quel type `self` doit être pour que la méthode soit appelée.
- Ce ne peut pas être n'importe quel type. Il est restreint au type sur lequel la méthode est implémentée, une référence ou un pointeur intelligent à ce type, ou un `Pin` enveloppant une référence à ce type.

Nous en verrons plus sur cette syntaxe au [Chapitre 18][ch-18]<!-- ignore -->. Pour l’instant, il suffit de savoir que si nous voulons poll un futur pour vérifier s'il est `Pending` ou `Ready(Output)`, nous avons besoin d'une référence mutable encapsulée dans `Pin` pour ce type.

`Pin` est un wrapper pour des types semblables à des pointeurs tels que `&`, `&mut`, `Box` et `Rc`. (Techniquement, `Pin` fonctionne avec des types qui implémentent les traits `Deref` ou `DerefMut`, mais cela équivaut effectivement à travailler uniquement avec des références et des pointeurs intelligents.) `Pin` n'est pas un pointeur en soi et n'a pas de comportement propre comme `Rc` et `Arc` avec le comptage de références ; c'est simplement un outil que le compilateur peut utiliser pour faire respecter des contraintes sur l'utilisation des pointeurs.

Se rappeler que `await` est mis en œuvre en appelant `poll` commence à expliquer le message d'erreur que nous avons vu plus tôt, mais c'était en termes de `Unpin`, pas de `Pin`. Alors comment `Pin` est-il lié à `Unpin`, et pourquoi le `Future` a-t-il besoin que `self` soit dans un type `Pin` pour appeler `poll` ?

Rappelez-vous plus tôt dans ce chapitre qu'une série de points d'attente dans un futur est compilée en une machine à états, et le compilateur s'assure que cette machine à états suit toutes les règles normales de sécurité de Rust, y compris le prêt et la propriété. Pour faire fonctionner cela, Rust examine quelles données sont nécessaires entre un point d'attente donné et soit le prochain point d'attente soit la fin du bloc asynchrone. Il crée alors un variant correspondant dans la machine à états compilée. Chaque variant obtient l'accès dont il a besoin aux données qui seront utilisées dans cette section du code source, que ce soit en prenant possession de ces données ou en obtenant une référence mutable ou immuable à celles-ci.

Ça va jusqu'ici : si nous nous trompons sur la propriété ou les références dans un bloc async donné, le vérificateur de prêts nous le dira. Lorsque nous voulons déplacer le futur qui correspond à ce bloc—comme le déplacer dans un `Vec` pour le passer à `join_all`—les choses deviennent plus compliquées.

Lorsque nous déplaçons un futur—que ce soit en le poussant dans une structure de données à utiliser comme un itérateur avec `join_all` ou en le retournant d'une fonction—cela signifie en fait déplacer la machine à états que Rust crée pour nous. Et contrairement à la plupart des autres types en Rust, les futurs que Rust crée pour les blocs async peuvent se retrouver avec des références à eux-mêmes dans les champs de n'importe quel variant donné, comme montré dans l'illustration simplifiée de la Figure 17-4.

<figure>

<img alt="Un tableau à une colonne et trois lignes représentant un futur, fut1, qui a des valeurs de données 0 et 1 dans les deux premières lignes et une flèche pointant de la troisième ligne vers la deuxième ligne, représentant une référence interne au sein du futur." src="img/trpl17-04.svg" class="center" />

<figcaption>Figure 17-4 : Un type de données auto-référentiel</figcaption>

</figure>

Cependant, par défaut, tout objet qui a une référence à lui-même est dangereux à déplacer, car les références pointent toujours vers l'adresse mémoire réelle de ce à quoi elles se réfèrent (voir Figure 17-5). Si vous déplacez la structure de données elle-même, ces références internes resteront pointées vers l'ancienne adresse. Cependant, cette localisation mémoire est maintenant invalide. D'une part, sa valeur ne sera pas mise à jour lorsque vous apporterez des modifications à la structure de données. D'autre part—chose plus importante—l'ordinateur est maintenant libre de réutiliser cette mémoire à d'autres fins ! Vous pourriez vous retrouver à lire des données complètement non liées plus tard.

<figure>

<img alt="Deux tableaux, décrivant deux futurs, fut1 et fut2, chacun ayant une colonne et trois lignes, représentant le résultat d'avoir déplacé un futur de fut1 vers fut2. Le premier, fut1, est grisé, avec un point d'interrogation dans chaque index, représentant une mémoire inconnue. Le second, fut2, a 0 et 1 dans les première et deuxième lignes et une flèche pointant de sa troisième ligne vers la deuxième ligne de fut1, représentant un pointeur qui fait référence à l'ancienne localisation en mémoire du futur avant qu'il ne soit déplacé." src="img/trpl17-05.svg" class="center" />

<figcaption>Figure 17-5 : Le résultat dangereux de déplacer un type de données auto-référentiel</figcaption>

</figure>

Théoriquement, le compilateur Rust pourrait essayer de mettre à jour chaque référence à un objet chaque fois qu'il est déplacé, mais cela pourrait ajouter beaucoup de surcharge de performance, surtout si un tout un réseau de références doit être mis à jour. Si nous pouvions plutôt nous assurer que la structure de données en question _ne bouge pas en mémoire_, nous n'aurions pas besoin de mettre à jour des références. C'est précisément pourquoi le vérificateur de prêts de Rust est là : dans du code sûr, il vous empêche de déplacer tout élément ayant une référence active vers lui.

`Pin` s'appuie sur ça pour nous donner la garantie exacte dont nous avons besoin. Lorsque nous _épinglons_ une valeur en enveloppant un pointeur vers cette valeur dans `Pin`, elle ne peut plus être déplacée. Ainsi, si vous avez `Pin<Box<SomeType>>`, vous épinglez en fait la valeur `SomeType`, _pas_ le pointeur `Box`. La Figure 17-6 illustre ce processus.

<figure>

<img alt="Trois boîtes disposées côte à côte. La première est étiquetée ‘Pin’, la seconde ‘b1’, et la troisième ‘pinned’. Dans ‘pinned’ se trouve un tableau étiqueté ‘fut’, avec une seule colonne ; il représente un futur avec des cellules pour chaque partie de la structure de données. Sa première cellule contient la valeur ‘0’, sa deuxième cellule a une flèche qui en sort et pointe vers la quatrième et dernière cellule, qui a la valeur ‘1’, et la troisième cellule a des lignes en pointillé et une ellipse pour indiquer qu'il peut y avoir d'autres parties à la structure de données. Dans l'ensemble, le tableau ‘fut’ représente un futur qui est auto-référentiel. Une flèche sort de la boîte étiquetée ‘Pin’, traverse la boîte étiquetée ‘b1’ et se termine dans la boîte ‘pinned’ au tableau ‘fut’." src="img/trpl17-06.svg" class="center" />

<figcaption>Figure 17-6 : Épingler un `Box` qui pointe vers un type futur auto-référentiel</figcaption>

</figure>

En fait, le pointeur `Box` peut toujours se déplacer librement. Rappelez-vous : nous nous soucions de nous assurer que les données finalement référencées restent à leur place. Si un pointeur se déplace, _mais que les données auxquelles il fait référence_ restent au même endroit, comme dans la Figure 17-7, il n'y a pas de problème potentiel. (Comme exercice indépendant, consultez la documentation concernant les types ainsi que le module `std::pin` et essayez de déterminer comment vous feriez cela avec un `Pin` enveloppant un `Box`.) L'essentiel est que le type auto-référentiel lui-même ne peut pas bouger, car il est toujours épinglé.

<figure>

<img alt="Quatre boîtes disposées dans trois colonnes approximatives, identiques au diagramme précédent avec un changement dans la deuxième colonne. Maintenant, il y a deux boîtes dans la deuxième colonne, étiquetées ‘b1’ et ‘b2’, ‘b1’ est grisée, et la flèche de ‘Pin’ passe par ‘b2’ au lieu de ‘b1’, indiquant que le pointeur a déménagé de ‘b1’ à ‘b2’, mais les données dans ‘pinned’ n'ont pas bougé." src="img/trpl17-07.svg" class="center" />

<figcaption>Figure 17-7 : Déplacer un `Box` qui pointe vers un type futur auto-référentiel</figcaption>

</figure>

Cependant, la plupart des types peuvent être déplacés sans danger, même s'ils se trouvent derrière un pointeur `Pin`. Nous n'avons besoin de penser à l'épinglage que lorsque des éléments ont des références internes. Des valeurs primitives telles que des nombres et des booléens sont sécuritaires car elles n'ont évidemment pas de références internes. La plupart des types avec lesquels vous travaillez normalement en Rust n'en ont pas non plus. Vous pouvez, par exemple, déplacer un `Vec` sans vous inquiéter. Étant donné ce que nous avons vu jusqu'à présent, si vous avez un `Pin<Vec<String>>`, vous devrez effectuer toutes les opérations par le biais des API sûres mais restrictives fournies par `Pin`, même si un `Vec<String>` est toujours sûr à déplacer s'il n'y a pas d'autres références vers celui-ci. Nous avons besoin d'un moyen d'indiquer au compilateur qu'il est acceptable de déplacer des éléments dans des cas comme celui-ci—et c'est là que `Unpin` entre en jeu.

`Unpin` est un trait marqueur, similaire aux traits `Send` et `Sync` que nous avons vus au chapitre 16, et donc n'a aucune fonctionnalité propre. Les traits marqueurs n’existent que pour indiquer au compilateur qu'il est sûr d'utiliser le type implémentant un trait donné dans un contexte particulier. `Unpin` informe le compilateur qu'un type donné ne nécessite _pas_ de respecter des garanties concernant la sécurité de son déplacement.

<!--
  Le `<code>` en ligne dans le bloc suivant est pour permettre le `<em>` en ligne à l'intérieur, faisant correspondre ce que NoStarch fait stylistiquement, et en soulignant dans le texte ici que c'est quelque chose de distinct d'un type normal.
-->

Tout comme avec `Send` et `Sync`, le compilateur implémente `Unpin` automatiquement pour tous les types où il peut prouver que c'est sans danger. Un cas particulier, encore une fois similaire à `Send` et `Sync`, est lorsque `Unpin` _n'est pas_ implémenté pour un type. La notation pour cela est <code>impl !Unpin pour <em>SomeType</em></code>, où <code><em>SomeType</em></code> est le nom d'un type qui _doit_ respecter ces garanties pour être sûr chaque fois qu'un pointeur vers ce type est utilisé dans un `Pin`.

En d'autres termes, il y a deux choses à garder à l'esprit sur la relation entre `Pin` et `Unpin`. Premièrement, `Unpin` est le cas “normal”, et `!Unpin` est le cas particulier. Deuxièmement, qu'un type implémente `Unpin` ou `!Unpin` _n'a d'importance que lorsque vous utilisez un pointeur épinglé vers ce type comme <code>Pin<&mut <em>SomeType</em>></code>.

Pour rendre cela concret, pensez à un `String` : il a une longueur et les caractères Unicode qui le composent. Nous pouvons envelopper un `String` dans `Pin`, comme vu dans la Figure 17-8. Cependant, `String` implémente automatiquement `Unpin`, tout comme la plupart des autres types en Rust.

<figure>

<img alt="Une boîte étiquetée ‘Pin’ à gauche avec une flèche allant de celle-ci à une boîte étiquetée ‘String’ à droite. La boîte ‘String’ contient les données 5usize, représentant la longueur de la chaîne, et les lettres ‘h’, ‘e’, ‘l’, ‘l’ et ‘o’ représentant les caractères de la chaîne ‘hello’ stockés dans cette instance de String. Un rectangle en pointillé entoure la boîte String et son étiquette, mais pas la boîte Pin." src="img/trpl17-08.svg" class="center" />

<figcaption>Figure 17-8 : Épingler un `String` ; la ligne en pointillé indique que le `String` implémente le trait `Unpin` et qu'il n'est donc pas épinglé</figcaption>

</figure>

En conséquence, nous pouvons faire des choses qui seraient illégales si `String` implémentait `!Unpin` à la place, comme remplacer une chaîne par une autre au même endroit en mémoire comme dans la Figure 17-9. Cela ne viole pas le contrat de `Pin`, car `String` n'a pas de références internes qui rendent son déplacement dangereux. C'est précisément pour cela qu'il implémente `Unpin` plutôt que `!Unpin`.

<figure>

<img alt="Les mêmes données de chaîne ‘hello’ de l'exemple précédent, maintenant étiquetées ‘s1’ et grises. La boîte ‘Pin’ de l'exemple précédent pointe maintenant vers une autre instance de String, étiquetée ‘s2’, qui est valide, a une longueur de 7usize et contient les caractères de la chaîne ‘goodbye’. s2 est entourée d'un rectangle en pointillé car elle implémente également le trait Unpin." src="img/trpl17-09.svg" class="center" />

<figcaption>Figure 17-9 : Remplacer le `String` par un `String` entièrement différent en mémoire</figcaption>

</figure>

Maintenant, nous savons suffisamment pour comprendre les erreurs rapportées pour cet appel  `join_all` de la Listing 17-23. Nous avons initialement essayé de déplacer les futurs produits par des blocs async dans un `Vec<Box<dyn Future<Output = ()>>>`, mais comme nous l'avons vu, ces futurs peuvent avoir des références internes, donc ils n'implémentent pas automatiquement `Unpin`. Une fois que nous les avons épinglés, nous pouvons passer le type résultant `Pin` dans le `Vec`, en étant confiants que les données sous-jacentes dans les futurs ne seront _pas_ déplacées. La Listing 17-24 montre comment corriger le code en appelant le macro `pin!` où chacun des trois futurs est défini et en ajustant le type d'objet trait.

<Listing number="17-24" caption="Épingler les futurs pour permettre leur déplacement dans le vecteur">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-24/src/main.rs:here}}
```

</Listing>

Cet exemple compile maintenant et s'exécute, et nous pourrions ajouter ou retirer des futurs du vecteur à l'exécution et les rejoindre tous.

`Pin` et `Unpin` sont principalement importants pour construire des bibliothèques de bas niveau, ou lorsque vous construisez un runtime lui-même, plutôt que pour du code Rust quotidien. Lorsque vous voyez ces traits dans les messages d'erreur, cependant, vous aurez maintenant une meilleure idée de comment corriger votre code !

> Remarque : Cette combinaison de `Pin` et `Unpin` permet de mettre en œuvre en toute sécurité toute une classe de types complexes en Rust qui autrement seraient difficiles à gérer en raison de leur nature auto-référentielle. Les types nécessitant `Pin` apparaissent le plus souvent dans le Rust asynchrone aujourd'hui, mais de temps en temps, vous pourriez les voir dans d'autres contextes aussi.
>
> Les spécificités de la façon dont `Pin` et `Unpin` fonctionnent, et les règles qu'ils doivent respecter, sont couvertes de manière exhaustive dans la documentation de l'API pour `std::pin`, donc si vous êtes intéressé à en apprendre plus, c'est un excellent point de départ.
>
> Si vous souhaitez comprendre comment les choses fonctionnent en détail sous le capot, consultez les chapitres [2][under-the-hood]<!-- ignore --> et [4][pinning]<!-- ignore --> de [_Programmation Asynchrone en Rust_][async-book].

### Le Trait `Stream`

Maintenant que vous avez une compréhension plus approfondie des traits `Future`, `Pin` et `Unpin`, nous pouvons diriger notre attention vers le trait `Stream`. Comme vous l'avez appris plus tôt dans le chapitre, les flux sont similaires aux itérateurs asynchrones. Contrairement à `Iterator` et `Future`, cependant, `Stream` n'a pas de définition dans la bibliothèque standard à l'heure actuelle, mais il existe une définition très courante provenant du crate `futures` utilisée dans tout l'écosystème.

Repassons en revue les définitions des traits `Iterator` et `Future` avant de voir comment un trait `Stream` pourrait les fusionner ensemble. À partir de `Iterator`, nous avons l'idée d'une séquence : sa méthode `next` fournit un `Option<Self::Item>`. À partir de `Future`, nous avons l'idée de préparation dans le temps : sa méthode `poll` fournit un `Poll<Self::Output>`. Pour représenter une séquence d'éléments qui deviennent disponibles au fil du temps, nous définissons un trait `Stream` qui combine ces fonctionnalités :

```rust
use std::pin::Pin;
use std::task::{Context, Poll};

trait Stream {
    type Item;

    fn poll_next(
        self: Pin<&mut Self>,
        cx: &mut Context<'_>
    ) -> Poll<Option<Self::Item>>;
}
```

Le trait `Stream` définit un type associé appelé `Item` pour le type des éléments produits par le flux. Cela est similaire à `Iterator`, où il peut y avoir zéro à plusieurs éléments, et contrairement à `Future`, où il y a toujours une seule `Output`, même si c'est le type unité `()`.

`Stream` définit également une méthode pour obtenir ces éléments. Nous l'appelons `poll_next`, pour clarifier qu'elle poll de la même manière que `Future::poll` et produit une séquence d'éléments de la même manière que `Iterator::next`. Son type de retour combine `Poll` avec `Option`. Le type extérieur est `Poll`, car il doit être vérifié pour sa préparation, tout comme un futur. Le type intérieur est `Option`, car il doit signaler s'il y a d'autres messages, tout comme un itérateur.

Quelque chose de très similaire à cette définition finira probablement par faire partie de la bibliothèque standard de Rust. En attendant, cela fait partie de la boîte à outils de la plupart des runtimes, donc vous pouvez vous y fier, et tout ce que nous aborderons ensuite devrait généralement s'appliquer !

Dans les exemples que nous avons vus dans la section [“Flux : Futurs en Séquence”][streams]<!-- ignore -->, cependant, nous n'avons pas utilisé `poll_next` _ou_ `Stream`, mais avons plutôt utilisé `next` et `StreamExt`. Nous _pourrions_ travailler directement en fonction de l'API `poll_next` en écrivant à la main nos propres machines à états `Stream`, bien sûr, tout comme nous _pourrions_ travailler avec des futurs directement via leur méthode `poll`. Utiliser `await` est beaucoup plus agréable, cependant, et le trait `StreamExt` fournit la méthode `next` pour que nous puissions faire cela :

```rust
{{#rustdoc_include ../listings/ch17-async-await/no-listing-stream-ext/src/lib.rs:here}}
```

> Remarque : La définition réelle que nous avons utilisée plus tôt dans le chapitre semble légèrement différente de cela, car elle prend en charge les versions de Rust qui ne supportaient pas encore l'utilisation de fonctions async dans les traits. Par conséquent, elle ressemble à ceci :
>
> ```rust,ignore
> fn next(&mut self) -> Next<'_, Self> where Self: Unpin;
> ```
>
> Ce type `Next` est une `struct` qui implémente `Future` et nous permet de nommer la durée de la référence à `self` avec `Next<'_, Self>`, afin que `await` puisse fonctionner avec cette méthode.

Le trait `StreamExt` est également le foyer de toutes les méthodes intéressantes utilisables avec les flux. `StreamExt` est automatiquement implémenté pour chaque type qui implémente `Stream`, mais ces traits sont définis séparément pour permettre à la communauté d'itérer sur des APIs de commodité sans affecter la trait de base.

Dans la version de `StreamExt` utilisée dans le crate `trpl`, le trait ne définit pas seulement la méthode `next` mais fournit également une implémentation par défaut de `next` qui gère correctement les détails de l'appel à `Stream::poll_next`. Cela signifie que même lorsque vous devez écrire votre propre type de données de streaming, vous _n'avez_ qu'à implémenter `Stream`, et ensuite quiconque utilise votre type de données peut automatiquement utiliser `StreamExt` et ses méthodes avec celui-ci.

C'est tout ce que nous allons couvrir pour les détails de bas niveau sur ces traits. Pour conclure, considérons comment les futurs (y compris les flux), les tâches et les threads s'articulent ! 

[message-passing]: ch17-02-concurrency-with-async.md#sending-data-between-two-tasks-using-message-passing
[ch-18]: ch18-00-oop.html
[async-book]: https://rust-lang.github.io/async-book/
[under-the-hood]: https://rust-lang.github.io/async-book/02_execution/01_chapter.html
[pinning]: https://rust-lang.github.io/async-book/04_pinning/01_chapter.html
[first-async]: ch17-01-futures-and-syntax.html#our-first-async-program
[any-number-futures]: ch17-03-more-futures.html#working-with-any-number-of-futures
[streams]: ch17-04-streams.html