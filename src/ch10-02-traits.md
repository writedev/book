<!-- Anciennes rubriques. Ne pas supprimer ou les liens pourraient se briser. -->

<a id="traits-defining-shared-behavior"></a>

## Définir un Comportement Partagé avec des Traits

Un _trait_ définit la fonctionnalité qu'un type particulier possède et peut partager avec d'autres types. Nous pouvons utiliser des traits pour définir un comportement partagé de manière abstraite. Nous pouvons utiliser des _contraintes de trait_ pour spécifier qu'un type générique peut être n'importe quel type qui possède certains comportements.

> Remarque : Les traits sont similaires à une fonctionnalité souvent appelée _interfaces_ dans d'autres langages, bien qu'il y ait quelques différences.

### Définir un Trait

Le comportement d’un type est constitué des méthodes que nous pouvons appeler sur ce type. Différents types partagent le même comportement si nous pouvons appeler les mêmes méthodes sur tous ces types. Les définitions de trait sont un moyen de regrouper ensemble les signatures de méthodes pour définir un ensemble de comportements nécessaires à l'accomplissement d'un certain but.

Par exemple, disons que nous avons plusieurs structures qui contiennent divers types et quantités de texte : une structure `NewsArticle` qui contient une histoire d'actualité déposée dans un lieu particulier et un `SocialPost` qui peut avoir, au maximum, 280 caractères avec des métadonnées indiquant s'il s'agissait d'un nouveau post, d'un repost ou d'une réponse à un autre post.

Nous voulons créer une bibliothèque de collecte de médias nommée `aggregator` qui peut afficher des résumés de données qui pourraient être stockées dans une instance `NewsArticle` ou `SocialPost`. Pour ce faire, nous avons besoin d'un résumé de chaque type, et nous demanderons ce résumé en appelant une méthode `summarize` sur une instance. L'extrait 10-12 montre la définition d'un trait `Summary` public qui exprime ce comportement.

<Extrait numéro="10-12" nom-du-fichier="src/lib.rs" légende="Un trait `Summary` qui consiste en le comportement fourni par une méthode `summarize`">

```rust,noplayground
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-12/src/lib.rs}}
```

</Extrait>

Ici, nous déclarons un trait en utilisant le mot clé `trait` suivi du nom du trait, qui est `Summary` dans ce cas. Nous déclarons également le trait comme `pub` afin que les crates qui dépendent de cette crate puissent également utiliser ce trait, comme nous le verrons dans quelques exemples. À l'intérieur des accolades, nous déclarons les signatures des méthodes qui décrivent les comportements des types qui implémentent ce trait, qui dans ce cas est `fn summarize(&self) -> String`.

Après la signature de méthode, au lieu de fournir une implémentation dans des accolades, nous utilisons un point-virgule. Chaque type implémentant ce trait doit fournir son propre comportement personnalisé pour le corps de la méthode. Le compilateur veillera à ce que tout type ayant le trait `Summary` définisse la méthode `summarize` exactement avec cette signature.

Un trait peut avoir plusieurs méthodes dans son corps : Les signatures des méthodes sont répertoriées une par ligne, et chaque ligne se termine par un point-virgule.

### Implémenter un Trait sur un Type

Maintenant que nous avons défini les signatures souhaitées des méthodes du trait `Summary`, nous pouvons l'implémenter sur les types de notre collecteur de médias. L'extrait 10-13 montre une implementation du trait `Summary` sur la structure `NewsArticle` qui utilise le titre, l'auteur et le lieu pour créer la valeur de retour de `summarize`. Pour la structure `SocialPost`, nous définissons `summarize` comme le nom d'utilisateur suivi de l'intégralité du texte du post, en supposant que le contenu du post est déjà limité à 280 caractères.

<Extrait numéro="10-13" nom-du-fichier="src/lib.rs" légende="Implémenter le trait `Summary` sur les types `NewsArticle` et `SocialPost`">

```rust,noplayground
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-13/src/lib.rs:here}}
```

</Extrait>

Implémenter un trait sur un type est similaire à l'implémentation de méthodes ordinaires. La différence est qu'après `impl`, nous mettons le nom du trait que nous voulons implémenter, puis utilisons le mot clé `for`, et ensuite spécifions le nom du type pour lequel nous voulons implémenter le trait. Dans le bloc `impl`, nous plaçons les signatures des méthodes que la définition du trait a définies. Au lieu d'ajouter un point-virgule après chaque signature, nous utilisons des accolades et complétons le corps de la méthode avec le comportement spécifique que nous voulons que les méthodes du trait aient pour le type particulier.

Maintenant que la bibliothèque a implémenté le trait `Summary` sur `NewsArticle` et `SocialPost`, les utilisateurs de la crate peuvent appeler les méthodes du trait sur les instances de `NewsArticle` et `SocialPost` de la même manière que nous appelons des méthodes ordinaires. La seule différence est que l'utilisateur doit amener le trait dans le scope ainsi que les types. Voici un exemple de la façon dont une crate binaire pourrait utiliser notre crate de bibliothèque `aggregator` :

```rust,ignore
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-01-calling-trait-method/src/main.rs}}
```

Ce code imprime `1 new post: horse_ebooks: of course, as you probably already know, people`.

D'autres crates qui dépendent de la crate `aggregator` peuvent également amener le trait `Summary` dans le scope pour implémenter `Summary` sur leurs propres types. Une restriction à noter est que nous pouvons implémenter un trait sur un type uniquement si soit le trait soit le type, ou les deux, sont locaux à notre crate. Par exemple, nous pouvons implémenter des traits de la bibliothèque standard comme `Display` sur un type personnalisé comme `SocialPost` dans le cadre des fonctionnalités de notre crate `aggregator` car le type `SocialPost` est local à notre crate `aggregator`. Nous pouvons également implémenter `Summary` sur `Vec<T>` dans notre crate `aggregator` car le trait `Summary` est local à notre crate `aggregator`.

Mais nous ne pouvons pas implémenter des traits externes sur des types externes. Par exemple, nous ne pouvons pas implémenter le trait `Display` sur `Vec<T>` dans notre crate `aggregator`, car `Display` et `Vec<T>` sont tous deux définis dans la bibliothèque standard et ne sont pas locaux à notre crate `aggregator`. Cette restriction fait partie d'une propriété appelée _cohérence_, et plus précisément la _règle des orphelins_, ainsi nommée parce que le type parent n'est pas présent. Cette règle garantit que le code d'autres personnes ne peut pas casser votre code et vice versa. Sans cette règle, deux crates pourraient implémenter le même trait pour le même type, et Rust ne saurait pas quelle implémentation utiliser.

<!-- Anciennes rubriques. Ne pas supprimer ou les liens pourraient se briser. -->

<a id="default-implementations"></a>

### Utiliser des Implémentations par Défaut

Il est parfois utile d'avoir un comportement par défaut pour certaines ou toutes les méthodes d'un trait au lieu d'exiger des implémentations pour toutes les méthodes sur chaque type. Alors, en implémentant le trait sur un type particulier, nous pouvons conserver ou remplacer le comportement par défaut de chaque méthode.

Dans l'extrait 10-14, nous spécifions une chaîne par défaut pour la méthode `summarize` du trait `Summary` au lieu de simplement définir la signature de la méthode, comme nous l'avons fait dans l'extrait 10-12.

<Extrait numéro="10-14" nom-du-fichier="src/lib.rs" légende="Définir un trait `Summary` avec une implémentation par défaut de la méthode `summarize`">

```rust,noplayground
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-14/src/lib.rs:here}}
```

</Extrait>

Pour utiliser une implémentation par défaut pour résumer les instances de `NewsArticle`, nous spécifions un bloc `impl` vide avec `impl Summary for NewsArticle {}`.

Bien que nous ne définissions plus directement la méthode `summarize` sur `NewsArticle`, nous avons fourni une implémentation par défaut et spécifié que `NewsArticle` implémente le trait `Summary`. En conséquence, nous pouvons toujours appeler la méthode `summarize` sur une instance de `NewsArticle`, comme ceci :

```rust,ignore
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-02-calling-default-impl/src/main.rs:here}}
```

Ce code imprime `Nouvel article disponible ! (Lire plus...)`.

Créer une implémentation par défaut ne nécessite pas que nous changions quoi que ce soit sur l'implémentation de `Summary` sur `SocialPost` dans l'extrait 10-13. La raison est que la syntaxe pour remplacer une implémentation par défaut est la même que la syntaxe pour implémenter une méthode de trait qui n'a pas d'implémentation par défaut.

Les implémentations par défaut peuvent appeler d'autres méthodes dans le même trait, même si ces autres méthodes n'ont pas d'implémentation par défaut. De cette manière, un trait peut fournir beaucoup de fonctionnalité utile et ne nécessiter que des implémenteurs pour spécifier une petite partie de celle-ci. Par exemple, nous pourrions définir le trait `Summary` pour avoir une méthode `summarize_author` dont l'implémentation est requise, et ensuite définir une méthode `summarize` qui a une implémentation par défaut qui appelle la méthode `summarize_author` :

```rust,noplayground
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-03-default-impl-calls-other-methods/src/lib.rs:here}}
```

Pour utiliser cette version de `Summary`, nous devons seulement définir `summarize_author` lorsque nous implémentons le trait sur un type :

```rust,noplayground
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-03-default-impl-calls-other-methods/src/lib.rs:impl}}
```

Après avoir défini `summarize_author`, nous pouvons appeler `summarize` sur les instances de la structure `SocialPost`, et l'implémentation par défaut de `summarize` appellera la définition de `summarize_author` que nous avons fournie. Comme nous avons implémenté `summarize_author`, le trait `Summary` nous a donné le comportement de la méthode `summarize` sans que nous ayons besoin d'écrire davantage de code. Voici à quoi cela ressemble :

```rust,ignore
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-03-default-impl-calls-other-methods/src/main.rs:here}}
```

Ce code imprime `1 nouveau post : (Lire plus depuis @horse_ebooks...)`.

Notez qu'il n'est pas possible d'appeler l'implémentation par défaut à partir d'une implémentation de remplacement de cette même méthode.

<!-- Anciennes rubriques. Ne pas supprimer ou les liens pourraient se briser. -->

<a id="traits-as-parameters"></a>

### Utiliser des Traits comme Paramètres

Maintenant que vous savez comment définir et implémenter des traits, nous pouvons explorer comment utiliser des traits pour définir des fonctions qui acceptent différents types. Nous utiliserons le trait `Summary` que nous avons implémenté sur les types `NewsArticle` et `SocialPost` dans l'extrait 10-13 pour définir une fonction `notify` qui appelle la méthode `summarize` sur son paramètre `item`, qui est d'un type implémentant le trait `Summary`. Pour ce faire, nous utilisons la syntaxe `impl Trait`, comme ceci :

```rust,ignore
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-04-traits-as-parameters/src/lib.rs:here}}
```

Au lieu d'un type concret pour le paramètre `item`, nous spécifions le mot clé `impl` et le nom du trait. Ce paramètre accepte n'importe quel type qui implémente le trait spécifié. Dans le corps de `notify`, nous pouvons appeler toutes les méthodes sur `item` qui proviennent du trait `Summary`, telles que `summarize`. Nous pouvons appeler `notify` et passer n'importe quelle instance de `NewsArticle` ou `SocialPost`. Un code qui appelle la fonction avec tout autre type, comme une `String` ou un `i32`, ne compilera pas, car ces types n'implémentent pas `Summary`.

<!-- Anciennes rubriques. Ne pas supprimer ou les liens pourraient se briser. -->

<a id="fixing-the-largest-function-with-trait-bounds"></a>

#### Syntaxe de Contrainte de Trait

La syntaxe `impl Trait` fonctionne pour des cas simples mais est en réalité un sucre syntaxique pour une forme plus longue appelée _contrainte de trait_ ; cela ressemble à ceci :

```rust,ignore
pub fn notify<T: Summary>(item: &T) {
    println!("Breaking news! {}", item.summarize());
}
```

Cette forme plus longue est équivalente à l'exemple de la section précédente mais est plus verbeuse. Nous plaçons les contraintes de trait avec la déclaration du paramètre de type générique après un deux-points et à l'intérieur de crochets angulaires.

La syntaxe `impl Trait` est pratique et rend le code plus concis dans les cas simples, tandis que la syntaxe de contrainte de trait plus complète peut exprimer plus de complexité dans d'autres cas. Par exemple, nous pouvons avoir deux paramètres qui implémentent `Summary`. Le faire avec la syntaxe `impl Trait` ressemble à ceci :

```rust,ignore
pub fn notify(item1: &impl Summary, item2: &impl Summary) {
```

Utiliser `impl Trait` est approprié si nous voulons que cette fonction permette à `item1` et `item2` d'avoir des types différents (tant que les deux types implémentent `Summary`). Si nous voulons que les deux paramètres aient le même type, nous devons utiliser une contrainte de trait, comme ceci :

```rust,ignore
pub fn notify<T: Summary>(item1: &T, item2: &T) {
```

Le type générique `T` spécifié comme type des paramètres `item1` et `item2` contraint la fonction de sorte que le type concret de la valeur passée comme argument pour `item1` et `item2` doit être le même.

<!-- Anciennes rubriques. Ne pas supprimer ou les liens pourraient se briser. -->

<a id="specifying-multiple-trait-bounds-with-the--syntax"></a>

#### Plusieurs Contraintes de Trait avec la Syntaxe `+`

Nous pouvons également spécifier plus d'une contrainte de trait. Disons que nous voulons que `notify` utilise à la fois le formatage d'affichage et `summarize` sur `item` : Nous spécifions dans la définition de `notify` que `item` doit implémenter à la fois `Display` et `Summary`. Nous pouvons le faire en utilisant la syntaxe `+` :

```rust,ignore
pub fn notify(item: &(impl Summary + Display)) {
```

La syntaxe `+` est également valide avec des contraintes de trait sur des types génériques :

```rust,ignore
pub fn notify<T: Summary + Display>(item: &T) {
```

Avec ces deux contraintes de trait spécifiées, le corps de `notify` peut appeler `summarize` et utiliser `{}` pour formater `item`.

#### Contraintes de Trait Plus Claires avec des Clauses `where`

Utiliser trop de contraintes de trait a ses inconvénients. Chaque générique a ses propres contraintes de trait, donc les fonctions avec plusieurs paramètres de type générique peuvent contenir beaucoup d'informations de contrainte de trait entre le nom de la fonction et sa liste de paramètres, rendant la signature de la fonction difficile à lire. Pour cette raison, Rust a une syntaxe alternative pour spécifier des contraintes de trait à l'intérieur d'une clause `where` après la signature de la fonction. Ainsi, au lieu d'écrire ceci :

```rust,ignore
fn some_function<T: Display + Clone, U: Clone + Debug>(t: &T, u: &U) -> i32 {
```

nous pouvons utiliser une clause `where`, comme ceci :

```rust,ignore
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-07-where-clause/src/lib.rs:here}}
```

La signature de cette fonction est moins encombrée : Le nom de la fonction, la liste des paramètres et le type de retour sont proches les uns des autres, semblable à une fonction sans beaucoup de contraintes de trait.

### Retourner des Types qui Implémentent des Traits

Nous pouvons également utiliser la syntaxe `impl Trait` dans la position de retour pour retourner une valeur de type implémentant un trait, comme montré ici :

```rust,ignore
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-05-returning-impl-trait/src/lib.rs:here}}
```

En utilisant `impl Summary` pour le type de retour, nous spécifions que la fonction `returns_summarizable` retourne un type qui implémente le trait `Summary` sans nommer le type concret. Dans ce cas, `returns_summarizable` retourne un `SocialPost`, mais le code appelant cette fonction n'a pas besoin de le savoir.

La capacité à spécifier un type de retour uniquement par le trait qu'il implémente est particulièrement utile dans le contexte des closures et des itérateurs, que nous couvrirons dans le Chapitre 13. Les closures et les itérateurs créent des types que seul le compilateur connaît ou des types qui sont très longs à spécifier. La syntaxe `impl Trait` vous permet de spécifier de manière concise qu'une fonction retourne un certain type qui implémente le trait `Iterator` sans avoir besoin d'écrire un type très long.

Cependant, vous ne pouvez utiliser `impl Trait` que si vous retournez un seul type. Par exemple, ce code qui retourne soit un `NewsArticle` soit un `SocialPost` avec le type de retour spécifié comme `impl Summary` ne fonctionnerait pas :

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-06-impl-trait-returns-one-type/src/lib.rs:here}}
```

Retourner soit un `NewsArticle` soit un `SocialPost` n'est pas permis en raison des restrictions autour de la manière dont la syntaxe `impl Trait` est implémentée dans le compilateur. Nous aborderons comment écrire une fonction avec ce comportement dans la section [“Utiliser des Objets de Trait pour Abstraire sur le Comportement Partagé”][trait-objects]<!-- ignore --> du Chapitre 18.

### Utiliser des Contraintes de Trait pour Implémenter des Méthodes Conditionnellement

En utilisant une contrainte de trait avec un bloc `impl` qui utilise des paramètres de type génériques, nous pouvons implémenter des méthodes conditionnellement pour des types qui implémentent les traits spécifiés. Par exemple, le type `Pair<T>` dans l'extrait 10-15 implémente toujours la fonction `new` pour retourner une nouvelle instance de `Pair<T>` (rappelons-nous de la section [“Syntaxe des Méthodes”][methods]<!-- ignore --> du Chapitre 5 que `Self` est un alias de type pour le type du bloc `impl`, qui dans ce cas est `Pair<T>`). Mais dans le prochain bloc `impl`, `Pair<T>` n'implémente la méthode `cmp_display` que si son type interne `T` implémente le trait `PartialOrd` qui permet la comparaison _et_ le trait `Display` qui permet l'affichage.

<Extrait numéro="10-15" nom-du-fichier="src/lib.rs" légende="Implémentation conditionnelle de méthodes sur un type générique en fonction des contraintes de trait">

```rust,noplayground
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-15/src/lib.rs}}
```

</Extrait>

Nous pouvons également implémenter un trait conditionnellement pour tout type qui implémente un autre trait. Les implémentations d'un trait sur tout type qui satisfait aux contraintes de trait sont appelées _implémentations globales_ et sont largement utilisées dans la bibliothèque standard de Rust. Par exemple, la bibliothèque standard implémente le trait `ToString` sur tout type qui implémente le trait `Display`. Le bloc `impl` dans la bibliothèque standard ressemble à ce code :

```rust,ignore
impl<T: Display> ToString for T {
    // --snip--
}
```

Parce que la bibliothèque standard a cette implémentation globale, nous pouvons appeler la méthode `to_string` définie par le trait `ToString` sur tout type qui implémente le trait `Display`. Par exemple, nous pouvons transformer des entiers en leurs valeurs `String` correspondantes comme ceci, car les entiers implémentent `Display` :

```rust
let s = 3.to_string();
```

Les implémentations globales apparaissent dans la documentation du trait dans la section "Implémenteurs".

Les traits et les contraintes de trait nous permettent d'écrire du code qui utilise des paramètres de type génériques pour réduire la duplication mais également de spécifier au compilateur que nous voulons que le type générique ait un comportement particulier. Le compilateur peut ensuite utiliser les informations de contrainte de trait pour vérifier que tous les types concrets utilisés avec notre code fournissent le comportement correct. Dans les langages dynamiquement typés, nous obtiendrions une erreur à l'exécution si nous appelions une méthode sur un type qui ne définissait pas la méthode. Mais Rust déplace ces erreurs à la compilation afin que nous soyons contraints de corriger les problèmes avant que notre code puisse même s'exécuter. De plus, nous n'avons pas à écrire de code qui vérifie le comportement à l'exécution, car nous avons déjà vérifié à la compilation. Cela améliore les performances sans avoir à abandonner la flexibilité des génériques.

[trait-objects]: ch18-02-trait-objects.html#using-trait-objects-to-abstract-over-shared-behavior
[methods]: ch05-03-method-syntax.html#method-syntax