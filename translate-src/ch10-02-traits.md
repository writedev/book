<!-- Anciens titres. Ne pas supprimer, car les liens risqueraient de ne plus fonctionner. -->

<a id="traits-defining-shared-behavior"></a>

## Définir un comportement partagé avec les traits

Un _trait_ définit les fonctionnalités qu’un type particulier possède et peut partager avec d’autres types. Nous pouvons utiliser les traits pour définir un comportement partagé de manière abstraite. Nous pouvons utiliser des _bornes de trait_ pour spécifier qu’un type générique peut être n’importe quel type ayant un comportement donné.

> Remarque : les traits sont similaires à une fonctionnalité souvent appelée _interfaces_ dans d’autres langages, bien qu’il existe quelques différences.

### Définir un trait

Le comportement d’un type se compose des méthodes que nous pouvons appeler sur ce type. Différents types partagent le même comportement si nous pouvons appeler les mêmes méthodes sur chacun d’eux. Les définitions de trait permettent de regrouper des signatures de méthode afin de définir un ensemble de comportements nécessaires à un objectif donné.

Par exemple, supposons que nous ayons plusieurs structs contenant différentes sortes de texte, en quantités variables : une struct `NewsArticle` qui contient un article d’actualité publié dans un endroit particulier, et une struct `SocialPost` qui peut contenir au maximum 280 caractères, ainsi que des métadonnées indiquant s’il s’agissait d’une nouvelle publication, d’une republication ou d’une réponse à une autre publication.

Nous voulons créer une crate de bibliothèque d’agrégation de médias nommée `aggregator`, capable d’afficher des résumés de données susceptibles d’être stockées dans une instance de `NewsArticle` ou de `SocialPost`. Pour cela, nous avons besoin d’un résumé pour chaque type, et nous demanderons ce résumé en appelant une méthode `summarize` sur une instance. Le Listing 10-12 montre la définition d’un trait public `Summary` qui exprime ce comportement.

<Listing number="10-12" file-name="src/lib.rs" caption="Un trait `Summary` qui se compose du comportement fourni par une méthode `summarize`">

```rust,noplayground
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-12/src/lib.rs}}
```

</Listing>

Ici, nous déclarons un trait à l’aide du mot-clé `trait`, suivi du nom du trait, qui est `Summary` dans ce cas. Nous déclarons également le trait comme `pub`, afin que les crates qui dépendent de cette crate puissent elles aussi utiliser ce trait, comme nous le verrons dans quelques exemples. Entre les accolades, nous déclarons les signatures de méthode qui décrivent les comportements des types implémentant ce trait ; dans ce cas, il s’agit de `fn summarize(&self) -> String`.

Après la signature de méthode, au lieu de fournir une implémentation entre accolades, nous utilisons un point-virgule. Chaque type qui implémente ce trait doit fournir son propre comportement pour le corps de la méthode. Le compilateur veillera à ce que tout type qui possède le trait `Summary` ait une méthode `summarize` définie avec exactement cette signature.

Un trait peut comporter plusieurs méthodes : les signatures de méthode sont énumérées une par ligne, et chaque ligne se termine par un point-virgule.

### Implémenter un trait sur un type

Maintenant que nous avons défini les signatures souhaitées des méthodes du trait `Summary`, nous pouvons l’implémenter sur les types de notre agrégateur de médias. Le Listing 10-13 montre une implémentation du trait `Summary` sur la struct `NewsArticle`, qui utilise le titre, l’auteur et le lieu pour créer la valeur de retour de `summarize`. Pour la struct `SocialPost`, nous définissons `summarize` comme le nom d’utilisateur suivi du texte intégral de la publication, en supposant que son contenu est déjà limité à 280 caractères.

<Listing number="10-13" file-name="src/lib.rs" caption="Implémentation du trait `Summary` sur les types `NewsArticle` et `SocialPost`">

```rust,noplayground
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-13/src/lib.rs:here}}
```

</Listing>

L’implémentation d’un trait sur un type est similaire à l’implémentation de méthodes ordinaires. La différence est qu’après `impl`, nous indiquons le nom du trait que nous voulons implémenter, puis nous utilisons le mot-clé `for`, suivi du nom du type sur lequel nous voulons implémenter le trait. Dans le bloc `impl`, nous plaçons les signatures de méthode définies par le trait. Au lieu d’ajouter un point-virgule après chaque signature, nous utilisons des accolades et renseignons le corps de la méthode avec le comportement spécifique que nous voulons donner aux méthodes du trait pour le type concerné.

Maintenant que la bibliothèque a implémenté le trait `Summary` sur `NewsArticle` et `SocialPost`, les utilisateurs de la crate peuvent appeler les méthodes du trait sur des instances de `NewsArticle` et de `SocialPost`, de la même façon que nous appelons des méthodes ordinaires. La seule différence est que l’utilisateur doit également importer le trait dans la portée, en plus des types. Voici un exemple d’utilisation de notre crate de bibliothèque `aggregator` par une crate binaire :

```rust,ignore
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-01-calling-trait-method/src/main.rs}}
```

Ce code affiche `1 new post: horse_ebooks: of course, as you probably already
know, people`.

Les autres crates qui dépendent de la crate `aggregator` peuvent également importer le trait `Summary` dans la portée pour implémenter `Summary` sur leurs propres types. Il faut noter une restriction : nous ne pouvons implémenter un trait sur un type que si le trait ou le type, ou les deux, sont locaux à notre crate. Par exemple, nous pouvons implémenter des traits de la bibliothèque standard comme `Display` sur un type personnalisé tel que `SocialPost`, dans le cadre des fonctionnalités de notre crate `aggregator`, car le type `SocialPost` est local à cette crate. Nous pouvons également implémenter `Summary` sur `Vec<T>` dans notre crate `aggregator`, car le trait `Summary` est local à notre crate `aggregator`.

En revanche, nous ne pouvons pas implémenter des traits externes sur des types externes. Par exemple, nous ne pouvons pas implémenter le trait `Display` sur `Vec<T>` au sein de notre crate `aggregator`, car `Display` et `Vec<T>` sont tous deux définis dans la bibliothèque standard et ne sont pas locaux à notre crate `aggregator`. Cette restriction fait partie d’une propriété appelée _cohérence_, et plus précisément de la _règle de l’orphelin_, ainsi nommée parce que le type parent n’est pas présent. Cette règle garantit que le code d’autres personnes ne peut pas casser le vôtre, et vice versa. Sans cette règle, deux crates pourraient implémenter le même trait pour le même type, et Rust ne saurait pas quelle implémentation utiliser.

<!-- Anciens titres. Ne pas supprimer, car les liens risqueraient de ne plus fonctionner. -->

<a id="default-implementations"></a>

### Utiliser des implémentations par défaut

Il est parfois utile de définir un comportement par défaut pour certaines méthodes d’un trait, voire pour toutes, plutôt que d’exiger que chaque type implémente toutes les méthodes. Ainsi, lorsque nous implémentons le trait sur un type particulier, nous pouvons conserver ou remplacer le comportement par défaut de chaque méthode.

Dans le Listing 10-14, nous spécifions une chaîne par défaut pour la méthode `summarize` du trait `Summary`, au lieu de définir uniquement la signature de la méthode, comme nous l’avons fait dans le Listing 10-12.

<Listing number="10-14" file-name="src/lib.rs" caption="Définition d’un trait `Summary` avec une implémentation par défaut de la méthode `summarize`">

```rust,noplayground
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-14/src/lib.rs:here}}
```

</Listing>

Pour utiliser une implémentation par défaut afin de résumer des instances de `NewsArticle`, nous spécifions un bloc `impl` vide avec `impl Summary for NewsArticle {}`.

Même si nous ne définissons plus directement la méthode `summarize` sur `NewsArticle`, nous avons fourni une implémentation par défaut et spécifié que `NewsArticle` implémente le trait `Summary`. Par conséquent, nous pouvons toujours appeler la méthode `summarize` sur une instance de `NewsArticle`, comme ceci :

```rust,ignore
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-02-calling-default-impl/src/main.rs:here}}
```

Ce code affiche `New article available! (Read more...)`.

La création d’une implémentation par défaut ne nécessite aucune modification de l’implémentation de `Summary` sur `SocialPost` dans le Listing 10-13. En effet, la syntaxe permettant de remplacer une implémentation par défaut est la même que celle utilisée pour implémenter une méthode de trait qui n’a pas d’implémentation par défaut.

Les implémentations par défaut peuvent appeler d’autres méthodes du même trait, même si ces autres méthodes n’ont pas d’implémentation par défaut. Ainsi, un trait peut fournir de nombreuses fonctionnalités utiles et ne demander aux personnes qui l’implémentent que d’en définir une petite partie. Par exemple, nous pourrions définir le trait `Summary` avec une méthode `summarize_author` dont l’implémentation est obligatoire, puis définir une méthode `summarize` avec une implémentation par défaut qui appelle la méthode `summarize_author` :

```rust,noplayground
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-03-default-impl-calls-other-methods/src/lib.rs:here}}
```

Pour utiliser cette version de `Summary`, il suffit de définir `summarize_author` lorsque nous implémentons le trait sur un type :

```rust,ignore
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-03-default-impl-calls-other-methods/src/lib.rs:impl}}
```

Après avoir défini `summarize_author`, nous pouvons appeler `summarize` sur des instances de la struct `SocialPost`, et l’implémentation par défaut de `summarize` appellera la définition de `summarize_author` que nous avons fournie. Comme nous avons implémenté `summarize_author`, le trait `Summary` nous a donné le comportement de la méthode `summarize` sans nous obliger à écrire davantage de code. Voici à quoi cela ressemble :

```rust,ignore
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-03-default-impl-calls-other-methods/src/main.rs:here}}
```

Ce code affiche `1 new post: (Read more from @horse_ebooks...)`.

Notez qu’il n’est pas possible d’appeler l’implémentation par défaut depuis une implémentation qui remplace cette même méthode.

<!-- Anciens titres. Ne pas supprimer, car les liens risqueraient de ne plus fonctionner. -->

<a id="traits-as-parameters"></a>

### Utiliser des traits comme paramètres

Maintenant que vous savez définir et implémenter des traits, nous pouvons voir comment les utiliser pour définir des fonctions qui acceptent de nombreux types différents. Nous allons utiliser le trait `Summary` que nous avons implémenté sur les types `NewsArticle` et `SocialPost` dans le Listing 10-13 pour définir une fonction `notify` qui appelle la méthode `summarize` sur son paramètre `item`, lequel est d’un type qui implémente le trait `Summary`. Pour cela, nous utilisons la syntaxe `impl Trait`, comme ceci :

```rust,ignore
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-04-traits-as-parameters/src/lib.rs:here}}
```

Au lieu d’indiquer un type concret pour le paramètre `item`, nous spécifions le mot-clé `impl` et le nom du trait. Ce paramètre accepte tout type qui implémente le trait spécifié. Dans le corps de `notify`, nous pouvons appeler sur `item` toutes les méthodes provenant du trait `Summary`, comme `summarize`. Nous pouvons appeler `notify` en lui passant n’importe quelle instance de `NewsArticle` ou de `SocialPost`. Le code qui appelle cette fonction avec un autre type, comme `String` ou `i32`, ne sera pas compilé, car ces types n’implémentent pas `Summary`.

<!-- Anciens titres. Ne pas supprimer, car les liens risqueraient de ne plus fonctionner. -->

<a id="fixing-the-largest-function-with-trait-bounds"></a>

#### Syntaxe des bornes de trait

La syntaxe `impl Trait` fonctionne dans les cas simples, mais elle est en réalité un raccourci syntaxique pour une forme plus longue appelée _borne de trait_, qui ressemble à ceci :

```rust,ignore
pub fn notify<T: Summary>(item: &T) {
    println!("Breaking news! {}", item.summarize());
}
```

Cette forme plus longue est équivalente à l’exemple de la section précédente, mais elle est plus verbeuse. Nous plaçons les bornes de trait après deux-points, à la suite de la déclaration du paramètre de type générique et à l’intérieur des chevrons.

La syntaxe `impl Trait` est pratique et permet d’écrire du code plus concis dans les cas simples, tandis que la syntaxe complète des bornes de trait peut exprimer davantage de complexité dans d’autres cas. Par exemple, nous pouvons avoir deux paramètres qui implémentent `Summary`. Avec la syntaxe `impl Trait`, cela donne :

```rust,ignore
pub fn notify(item1: &impl Summary, item2: &impl Summary) {
```

L’utilisation de `impl Trait` convient si nous voulons que cette fonction accepte des types différents pour `item1` et `item2` (à condition que les deux types implémentent `Summary`). Toutefois, si nous voulons imposer que les deux paramètres soient du même type, nous devons utiliser une borne de trait, comme ceci :

```rust,ignore
pub fn notify<T: Summary>(item1: &T, item2: &T) {
```

Le type générique `T`, spécifié comme type des paramètres `item1` et `item2`, contraint la fonction : le type concret de la valeur passée comme argument pour `item1` et `item2` doit être le même.

<!-- Anciens titres. Ne pas supprimer, car les liens risqueraient de ne plus fonctionner. -->

<a id="specifying-multiple-trait-bounds-with-the--syntax"></a>

#### Plusieurs bornes de trait avec la syntaxe `+`

Nous pouvons également spécifier plusieurs bornes de trait. Supposons que nous voulions que `notify` utilise le formatage d’affichage en plus de `summarize` sur `item` : nous indiquons dans la définition de `notify` que `item` doit implémenter à la fois `Display` et `Summary`. Nous pouvons le faire à l’aide de la syntaxe `+` :

```rust,ignore
pub fn notify(item: &(impl Summary + Display)) {
```

La syntaxe `+` est également valide avec des bornes de trait sur des types génériques :

```rust,ignore
pub fn notify<T: Summary + Display>(item: &T) {
```

Grâce à ces deux bornes de trait, le corps de `notify` peut appeler `summarize` et utiliser `{}` pour formater `item`.

#### Des bornes de trait plus lisibles avec les clauses `where`

L’utilisation d’un trop grand nombre de bornes de trait présente des inconvénients. Chaque type générique ayant ses propres bornes de trait, les fonctions avec plusieurs paramètres de type génériques peuvent comporter beaucoup d’informations sur les bornes de trait entre le nom de la fonction et sa liste de paramètres, ce qui rend la signature difficile à lire. C’est pourquoi Rust propose une autre syntaxe qui permet de spécifier les bornes de trait dans une clause `where`, après la signature de la fonction. Ainsi, au lieu d’écrire ceci :

```rust,ignore
fn some_function<T: Display + Clone, U: Clone + Debug>(t: &T, u: &U) -> i32 {
```

nous pouvons utiliser une clause `where`, comme ceci :

```rust,ignore
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-07-where-clause/src/lib.rs:here}}
```

La signature de cette fonction est moins encombrée : le nom de la fonction, la liste de paramètres et le type de retour sont proches les uns des autres, comme dans une fonction sans nombreuses bornes de trait.

### Renvoyer des types qui implémentent des traits

Nous pouvons également utiliser la syntaxe `impl Trait` à la position du type de retour pour renvoyer une valeur d’un type qui implémente un trait, comme ici :

```rust,ignore
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-05-returning-impl-trait/src/lib.rs:here}}
```

En utilisant `impl Summary` pour le type de retour, nous spécifions que la fonction `returns_summarizable` renvoie un type qui implémente le trait `Summary`, sans nommer le type concret. Dans ce cas, `returns_summarizable` renvoie un `SocialPost`, mais le code qui appelle cette fonction n’a pas besoin de le savoir.

La possibilité de spécifier un type de retour uniquement au moyen du trait qu’il implémente est particulièrement utile avec les fermetures et les itérateurs, que nous aborderons au chapitre 13. Les fermetures et les itérateurs créent des types que seul le compilateur connaît, ou des types très longs à spécifier. La syntaxe `impl Trait` permet de spécifier de manière concise qu’une fonction renvoie un type qui implémente le trait `Iterator`, sans devoir écrire un type très long.

Cependant, vous ne pouvez utiliser `impl Trait` que si vous renvoyez un seul type. Par exemple, ce code, qui renvoie soit un `NewsArticle`, soit un `SocialPost` avec le type de retour spécifié comme `impl Summary`, ne fonctionnerait pas :

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-06-impl-trait-returns-one-type/src/lib.rs:here}}
```

Renvoyer soit un `NewsArticle`, soit un `SocialPost` n’est pas autorisé en raison des restrictions liées à l’implémentation de la syntaxe `impl Trait` dans le compilateur. Nous verrons comment écrire une fonction ayant ce comportement dans la section [« Utiliser des objets de trait pour abstraire un comportement partagé »][trait-objects]<!-- ignore --> du chapitre 18.

### Utiliser des bornes de trait pour implémenter des méthodes sous condition

En utilisant une borne de trait avec un bloc `impl` qui utilise des paramètres de type génériques, nous pouvons implémenter des méthodes sous condition pour les types qui implémentent les traits spécifiés. Par exemple, le type `Pair<T>` du Listing 10-15 implémente toujours la fonction `new`, qui renvoie une nouvelle instance de `Pair<T>` (rappelez-vous que, dans la section [« Syntaxe des méthodes »][methods]<!-- ignore --> du chapitre 5, `Self` est un alias de type pour le type du bloc `impl`, qui est dans ce cas `Pair<T>`). Mais, dans le bloc `impl` suivant, `Pair<T>` n’implémente la méthode `cmp_display` que si son type interne `T` implémente le trait `PartialOrd`, qui permet la comparaison, _et_ le trait `Display`, qui permet l’affichage.

<Listing number="10-15" file-name="src/lib.rs" caption="Implémentation conditionnelle de méthodes sur un type générique en fonction des bornes de trait">

```rust,noplayground
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-15/src/lib.rs}}
```

</Listing>

Nous pouvons également implémenter un trait sous condition pour tout type qui implémente un autre trait. Les implémentations d’un trait sur tout type qui satisfait les bornes de trait sont appelées _implémentations globales_ et sont largement utilisées dans la bibliothèque standard Rust. Par exemple, la bibliothèque standard implémente le trait `ToString` pour tout type qui implémente le trait `Display`. Le bloc `impl` de la bibliothèque standard ressemble à ceci :

```rust,ignore
impl<T: Display> ToString for T {
    // --snip--
}
```

Grâce à cette implémentation globale dans la bibliothèque standard, nous pouvons appeler la méthode `to_string`, définie par le trait `ToString`, sur tout type qui implémente le trait `Display`. Par exemple, nous pouvons convertir des nombres entiers en leurs valeurs `String` correspondantes comme ceci, car les nombres entiers implémentent `Display` :

```rust
let s = 3.to_string();
```

Les implémentations globales apparaissent dans la documentation du trait, dans la section « Implémenteurs ».

Les traits et les bornes de trait nous permettent d’écrire du code qui utilise des paramètres de type génériques afin de réduire les duplications, tout en indiquant au compilateur que nous voulons que le type générique ait un comportement particulier. Le compilateur peut alors utiliser les informations des bornes de trait pour vérifier que tous les types concrets utilisés avec notre code fournissent le comportement attendu. Dans les langages à typage dynamique, nous obtiendrions une erreur à l’exécution si nous appelions une méthode sur un type qui ne la définit pas. Rust détecte ces erreurs à la compilation, ce qui nous oblige à corriger les problèmes avant même que notre code puisse s’exécuter. De plus, nous n’avons pas besoin d’écrire du code qui vérifie le comportement à l’exécution, puisque nous l’avons déjà vérifié à la compilation. Cela améliore les performances sans renoncer à la flexibilité des génériques.

[trait-objects]: ch18-02-trait-objects.html#using-trait-objects-to-abstract-over-shared-behavior
[methods]: ch05-03-method-syntax.html#method-syntax