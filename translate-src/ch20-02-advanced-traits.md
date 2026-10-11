## Traits avancés

Nous avons d’abord abordé les traits dans la section [« Définir un comportement partagé avec les traits »][traits]<!-- ignore --> du chapitre 10, mais nous n’en avons pas étudié les détails plus avancés. Maintenant que vous en savez davantage sur Rust, nous pouvons entrer dans le vif du sujet.

<!-- Anciennes rubriques. Ne pas supprimer, sinon les liens risquent de ne plus fonctionner. -->

<a id="specifying-placeholder-types-in-trait-definitions-with-associated-types"></a>
<a id="associated-types"></a>

### Définir des traits avec des types associés

Les _types associés_ relient un type de remplacement à un trait, de sorte que les définitions des méthodes du trait puissent utiliser ces types de remplacement dans leurs signatures. L’implémenteur d’un trait spécifiera le type concret qui remplacera le type de remplacement pour l’implémentation concernée. Ainsi, nous pouvons définir un trait qui utilise certains types sans avoir besoin de savoir exactement quels sont ces types avant que le trait soit implémenté.

Nous avons indiqué que la plupart des fonctionnalités avancées de ce chapitre sont rarement nécessaires. Les types associés se situent quelque part entre les deux : ils sont moins souvent utilisés que les fonctionnalités présentées dans le reste du livre, mais plus fréquemment que nombre des autres fonctionnalités abordées dans ce chapitre.

Le trait `Iterator` fourni par la bibliothèque standard est un exemple de trait avec un type associé. Ce type associé se nomme `Item` et représente le type des valeurs sur lesquelles itère le type qui implémente le trait `Iterator`. La définition du trait `Iterator` est présentée dans le Listing 20-13.

<Listing number="20-13" caption="Définition du trait `Iterator`, qui comporte un type associé `Item`">

```rust,noplayground
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-13/src/lib.rs}}
```

</Listing>

Le type `Item` est un type de remplacement, et la définition de la méthode `next` indique qu’elle renverra des valeurs de type `Option<Self::Item>`. Les implémenteurs du trait `Iterator` spécifieront le type concret de `Item`, et la méthode `next` renverra un `Option` contenant une valeur de ce type concret.

Les types associés peuvent sembler similaires aux génériques, car ces derniers nous permettent de définir une fonction sans préciser les types qu’elle peut traiter. Pour examiner la différence entre ces deux concepts, intéressons-nous à une implémentation du trait `Iterator` pour un type nommé `Counter`, qui spécifie que le type `Item` est `u32` :

<Listing file-name="src/lib.rs">

```rust,ignore
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-22-iterator-on-counter/src/lib.rs:ch19}}
```

</Listing>

Cette syntaxe semble comparable à celle des génériques. Alors, pourquoi ne pas définir le trait `Iterator` avec des génériques, comme dans le Listing 20-14 ?

<Listing number="20-14" caption="Définition hypothétique du trait `Iterator` à l’aide de génériques">

```rust,noplayground
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-14/src/lib.rs}}
```

</Listing>

La différence est que lorsqu’on utilise des génériques, comme dans le Listing 20-14, on doit annoter les types dans chaque implémentation. Comme nous pourrions aussi implémenter `Iterator<String> for Counter`, ou pour tout autre type, il pourrait y avoir plusieurs implémentations de `Iterator` pour `Counter`. Autrement dit, lorsqu’un trait comporte un paramètre générique, il peut être implémenté plusieurs fois pour un type, en modifiant les types concrets des paramètres de type génériques à chaque fois. Lorsque nous utiliserions la méthode `next` sur `Counter`, nous devrions fournir des annotations de type pour indiquer quelle implémentation de `Iterator` nous voulons utiliser.

Avec les types associés, nous n’avons pas besoin d’annoter les types, car nous ne pouvons pas implémenter plusieurs fois un trait pour un même type. Dans le Listing 20-13, avec la définition qui utilise des types associés, nous ne pouvons choisir qu’une seule fois le type de `Item`, car il ne peut y avoir qu’un seul `impl Iterator for Counter`. Nous n’avons pas à préciser que nous voulons un itérateur de valeurs `u32` chaque fois que nous appelons `next` sur `Counter`.

Les types associés font aussi partie du contrat du trait : les implémenteurs du trait doivent fournir un type qui remplace le type associé de remplacement. Les types associés ont souvent un nom qui décrit leur usage, et il est recommandé de les documenter dans la documentation de l’API.

<!-- Anciennes rubriques. Ne pas supprimer, sinon les liens risquent de ne plus fonctionner. -->

<a id="default-generic-type-parameters-and-operator-overloading"></a>

### Utiliser les paramètres de type générique par défaut et la surcharge d’opérateurs

Lorsque nous utilisons des paramètres de type génériques, nous pouvons spécifier un type concret par défaut pour le type générique. Cela évite aux implémenteurs du trait de devoir spécifier un type concret si le type par défaut convient. Pour spécifier un type par défaut, on déclare le type générique avec la syntaxe `<PlaceholderType=ConcreteType>`.

La _surcharge d’opérateurs_ est un excellent exemple de situation où cette technique est utile : elle consiste à personnaliser le comportement d’un opérateur (comme `+`) dans des situations particulières.

Rust ne permet pas de créer ses propres opérateurs ni de surcharger arbitrairement ceux qui existent. Toutefois, vous pouvez surcharger les opérations et les traits correspondants répertoriés dans `std::ops` en implémentant les traits associés à l’opérateur. Par exemple, dans le Listing 20-15, nous surchargeons l’opérateur `+` pour additionner deux instances de `Point`. Pour cela, nous implémentons le trait `Add` pour une structure `Point`.

<Listing number="20-15" file-name="src/main.rs" caption="Implémenter le trait `Add` pour surcharger l’opérateur `+` pour les instances de `Point`">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-15/src/main.rs}}
```

</Listing>

La méthode `add` additionne les valeurs `x` de deux instances de `Point` et les valeurs `y` de ces deux instances pour créer un nouveau `Point`. Le trait `Add` comporte un type associé nommé `Output`, qui détermine le type renvoyé par la méthode `add`.

Le type générique par défaut de ce code se trouve dans le trait `Add`. En voici la définition :

```rust
trait Add<Rhs=Self> {
    type Output;

    fn add(self, rhs: Rhs) -> Self::Output;
}
```

Ce code devrait vous sembler assez familier : un trait avec une méthode et un type associé. La nouveauté est `Rhs=Self` : cette syntaxe s’appelle _paramètre de type par défaut_. Le paramètre de type générique `Rhs` (abréviation de « right-hand side », soit « membre de droite ») définit le type du paramètre `rhs` de la méthode `add`. Si nous ne spécifions pas de type concret pour `Rhs` lors de l’implémentation du trait `Add`, le type de `Rhs` sera `Self` par défaut, c’est-à-dire le type pour lequel nous implémentons `Add`.

Lorsque nous avons implémenté `Add` pour `Point`, nous avons utilisé la valeur par défaut de `Rhs`, car nous voulions additionner deux instances de `Point`. Voyons maintenant un exemple d’implémentation du trait `Add` dans lequel nous voulons personnaliser le type `Rhs` au lieu d’utiliser la valeur par défaut.

Nous avons deux structures, `Millimeters` et `Meters`, qui contiennent des valeurs exprimées dans des unités différentes. Cette fine enveloppe autour d’un type existant, créée à l’aide d’une autre structure, est appelée le _patron newtype_. Nous la décrivons plus en détail dans la section [« Implémenter des traits externes avec le patron newtype »][newtype]<!-- ignore -->. Nous voulons additionner des valeurs en millimètres et des valeurs en mètres, et faire en sorte que l’implémentation de `Add` effectue correctement la conversion. Nous pouvons implémenter `Add` pour `Millimeters` en utilisant `Meters` comme type `Rhs`, comme indiqué dans le Listing 20-16.

<Listing number="20-16" file-name="src/lib.rs" caption="Implémenter le trait `Add` pour `Millimeters` afin d’additionner `Millimeters` et `Meters`">

```rust,noplayground
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-16/src/lib.rs}}
```

</Listing>

Pour additionner `Millimeters` et `Meters`, nous spécifions `impl Add<Meters>` afin de définir la valeur du paramètre de type `Rhs` au lieu d’utiliser la valeur par défaut `Self`.

Les paramètres de type par défaut s’utilisent principalement de deux façons :

1. Pour étendre un type sans casser le code existant
2. Pour permettre une personnalisation dans des cas particuliers dont la plupart des utilisateurs n’auront pas besoin

Le trait `Add` de la bibliothèque standard illustre le deuxième cas : en général, on additionne deux valeurs de même type, mais le trait `Add` permet d’aller au-delà. L’utilisation d’un paramètre de type par défaut dans la définition du trait `Add` signifie qu’il n’est pas nécessaire de spécifier le paramètre supplémentaire la plupart du temps. Autrement dit, cela évite un peu de code répétitif et facilite l’utilisation du trait.

Le premier cas est similaire au second, mais en sens inverse : si vous voulez ajouter un paramètre de type à un trait existant, vous pouvez lui donner une valeur par défaut afin d’étendre les fonctionnalités du trait sans casser le code des implémentations existantes.

<!-- Anciennes rubriques. Ne pas supprimer, sinon les liens risquent de ne plus fonctionner. -->

<a id="fully-qualified-syntax-for-disambiguation-calling-methods-with-the-same-name"></a>
<a id="disambiguating-between-methods-with-the-same-name"></a>

### Distinguer des méthodes portant le même nom

Rien n’empêche un trait Rust de comporter une méthode portant le même nom que celle d’un autre trait, et Rust ne vous empêche pas non plus d’implémenter les deux traits pour un même type. Il est également possible d’implémenter directement pour un type une méthode portant le même nom que celles de traits.

Lorsque vous appelez des méthodes portant le même nom, vous devez indiquer à Rust laquelle vous voulez utiliser. Considérez le code du Listing 20-17, où nous avons défini deux traits, `Pilot` et `Wizard`, qui comportent tous deux une méthode appelée `fly`. Nous implémentons ensuite les deux traits pour le type `Human`, qui possède déjà une méthode `fly`. Chaque méthode `fly` effectue une action différente.

<Listing number="20-17" file-name="src/main.rs" caption="Deux traits comportant une méthode `fly` sont définis et implémentés pour le type `Human`, qui possède aussi une méthode `fly` implémentée directement">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-17/src/main.rs:here}}
```

</Listing>

Lorsque nous appelons `fly` sur une instance de `Human`, le compilateur appelle par défaut la méthode implémentée directement pour le type, comme indiqué dans le Listing 20-18.

<Listing number="20-18" file-name="src/main.rs" caption="Appeler `fly` sur une instance de `Human`">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-18/src/main.rs:here}}
```

</Listing>

L’exécution de ce code affiche `*waving arms furiously*`, ce qui montre que Rust a appelé la méthode `fly` implémentée directement pour `Human`.

Pour appeler les méthodes `fly` du trait `Pilot` ou du trait `Wizard`, nous devons utiliser une syntaxe plus explicite afin de préciser celle que nous voulons. Le Listing 20-19 montre cette syntaxe.

<Listing number="20-19" file-name="src/main.rs" caption="Préciser la méthode `fly` du trait que nous voulons appeler">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-19/src/main.rs:here}}
```

</Listing>

Indiquer le nom du trait avant celui de la méthode précise à Rust quelle implémentation de `fly` nous voulons appeler. Nous pourrions aussi écrire `Human::fly(&person)`, ce qui équivaut à `person.fly()` dans le Listing 20-19, mais cette forme est un peu plus longue si nous n’avons pas besoin de lever l’ambiguïté.

L’exécution de ce code affiche :

```console
{{#include ../listings/ch20-advanced-features/listing-20-19/output.txt}}
```

Comme la méthode `fly` prend un paramètre `self`, si nous avions deux _types_ qui implémentent un même _trait_, Rust pourrait déterminer quelle implémentation du trait utiliser en fonction du type de `self`.

Cependant, les fonctions associées qui ne sont pas des méthodes n’ont pas de paramètre `self`. Lorsque plusieurs types ou traits définissent des fonctions qui ne sont pas des méthodes et portent le même nom, Rust ne sait pas toujours quel type vous voulez, à moins que vous utilisiez une syntaxe entièrement qualifiée. Par exemple, dans le Listing 20-20, nous créons un trait pour un refuge pour animaux qui veut appeler tous les chiots Spot. Nous créons un trait `Animal` avec une fonction associée qui n’est pas une méthode, `baby_name`. Le trait `Animal` est implémenté pour la structure `Dog`, qui définit également directement une fonction associée non méthode `baby_name`.

<Listing number="20-20" file-name="src/main.rs" caption="Un trait et un type qui implémentent tous deux une fonction associée portant le même nom">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-20/src/main.rs}}
```

</Listing>

Nous implémentons dans la fonction associée `baby_name` définie pour `Dog` le code qui donne le nom Spot à tous les chiots. Le type `Dog` implémente également le trait `Animal`, qui décrit les caractéristiques communes à tous les animaux. Les petits des chiens sont appelés chiots, ce qui est exprimé dans l’implémentation du trait `Animal` pour `Dog`, dans la fonction `baby_name` associée au trait `Animal`.

Dans `main`, nous appelons la fonction `Dog::baby_name`, qui appelle directement la fonction associée définie pour `Dog`. Ce code affiche :

```console
{{#include ../listings/ch20-advanced-features/listing-20-20/output.txt}}
```

Ce résultat n’est pas celui que nous souhaitions. Nous voulons appeler la fonction `baby_name` du trait `Animal` que nous avons implémenté pour `Dog`, afin que le code affiche `A baby dog is called a puppy`. La technique qui consiste à indiquer le nom du trait, utilisée dans le Listing 20-19, ne nous aide pas ici ; si nous modifions `main` pour qu’il contienne le code du Listing 20-21, nous obtiendrons une erreur de compilation.

<Listing number="20-21" file-name="src/main.rs" caption="Tentative d’appel de la fonction `baby_name` du trait `Animal`, sans que Rust sache quelle implémentation utiliser">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-21/src/main.rs:here}}
```

</Listing>

Comme `Animal::baby_name` n’a pas de paramètre `self` et que d’autres types pourraient implémenter le trait `Animal`, Rust ne peut pas déterminer quelle implémentation de `Animal::baby_name` nous voulons. Nous obtenons cette erreur du compilateur :

```console
{{#include ../listings/ch20-advanced-features/listing-20-21/output.txt}}
```

Pour lever l’ambiguïté et indiquer à Rust que nous voulons utiliser l’implémentation de `Animal` pour `Dog`, plutôt que celle de `Animal` pour un autre type, nous devons utiliser une syntaxe entièrement qualifiée. Le Listing 20-22 montre comment utiliser cette syntaxe.

<Listing number="20-22" file-name="src/main.rs" caption="Utiliser une syntaxe entièrement qualifiée pour préciser que nous voulons appeler la fonction `baby_name` du trait `Animal` telle qu’elle est implémentée pour `Dog`">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-22/src/main.rs:here}}
```

</Listing>

Nous fournissons à Rust une annotation de type entre chevrons, qui indique que nous voulons appeler la méthode `baby_name` du trait `Animal` telle qu’elle est implémentée pour `Dog`. Nous indiquons ainsi que nous voulons traiter le type `Dog` comme un `Animal` pour cet appel de fonction. Ce code affiche désormais le résultat voulu :

```console
{{#include ../listings/ch20-advanced-features/listing-20-22/output.txt}}
```

En général, la syntaxe entièrement qualifiée se définit ainsi :

```rust,ignore
<Type as Trait>::function(receiver_if_method, next_arg, ...);
```

Pour les fonctions associées qui ne sont pas des méthodes, il n’y aurait pas de `receiver` : il n’y aurait que la liste des autres arguments. Vous pourriez utiliser la syntaxe entièrement qualifiée partout où vous appelez des fonctions ou des méthodes. Toutefois, vous pouvez omettre toute partie de cette syntaxe que Rust peut déduire d’autres informations du programme. Cette syntaxe plus détaillée n’est nécessaire que lorsqu’il existe plusieurs implémentations portant le même nom et que Rust a besoin d’aide pour déterminer laquelle vous voulez appeler.

<!-- Anciennes rubriques. Ne pas supprimer, sinon les liens risquent de ne plus fonctionner. -->

<a id="using-supertraits-to-require-one-traits-functionality-within-another-trait"></a>

### Utiliser des supertraits

Il arrive que vous écriviez une définition de trait qui dépend d’un autre trait : pour qu’un type implémente le premier trait, vous voulez exiger qu’il implémente aussi le second. Vous pouvez procéder ainsi pour que la définition de votre trait puisse utiliser les éléments associés du second trait. Le trait dont dépend la définition de votre trait s’appelle un _supertrait_.

Par exemple, imaginons que nous voulions créer un trait `OutlinePrint` comportant une méthode `outline_print` qui affiche une valeur donnée dans un cadre d’astérisques. Autrement dit, si une structure `Point` implémente le trait `Display` de la bibliothèque standard pour afficher `(x, y)`, l’appel de `outline_print` sur une instance de `Point` ayant `1` pour `x` et `3` pour `y` devrait afficher :

```text
**********
*        *
* (1, 3) *
*        *
**********
```

Dans l’implémentation de la méthode `outline_print`, nous voulons utiliser les fonctionnalités du trait `Display`. Nous devons donc préciser que le trait `OutlinePrint` ne fonctionnera que pour les types qui implémentent aussi `Display` et fournissent les fonctionnalités dont `OutlinePrint` a besoin. Nous pouvons le faire dans la définition du trait en spécifiant `OutlinePrint: Display`. Cette technique s’apparente à l’ajout d’une contrainte de trait au trait. Le Listing 20-23 montre une implémentation du trait `OutlinePrint`.

<Listing number="20-23" file-name="src/main.rs" caption="Implémenter le trait `OutlinePrint`, qui requiert les fonctionnalités de `Display`">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-23/src/main.rs:here}}
```

</Listing>

Comme nous avons précisé que `OutlinePrint` requiert le trait `Display`, nous pouvons utiliser la fonction `to_string`, qui est automatiquement implémentée pour tout type implémentant `Display`. Si nous essayions d’utiliser `to_string` sans ajouter de deux-points et préciser le trait `Display` après le nom du trait, nous obtiendrions une erreur indiquant qu’aucune méthode nommée `to_string` n’a été trouvée pour le type `&Self` dans la portée actuelle.

Voyons ce qui se passe lorsque nous essayons d’implémenter `OutlinePrint` pour un type qui n’implémente pas `Display`, comme la structure `Point` :

<Listing file-name="src/main.rs">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-02-impl-outlineprint-for-point/src/main.rs:here}}
```

</Listing>

Nous obtenons une erreur indiquant que `Display` est requis, mais n’est pas implémenté :

```console
{{#include ../listings/ch20-advanced-features/no-listing-02-impl-outlineprint-for-point/output.txt}}
```

Pour résoudre ce problème, nous implémentons `Display` pour `Point` et respectons ainsi la contrainte imposée par `OutlinePrint` :

<Listing file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-03-impl-display-for-point/src/main.rs:here}}
```

</Listing>

L’implémentation du trait `OutlinePrint` pour `Point` compile alors correctement, et nous pouvons appeler `outline_print` sur une instance de `Point` pour l’afficher dans un cadre d’astérisques.

<!-- Anciennes rubriques. Ne pas supprimer, sinon les liens risquent de ne plus fonctionner. -->

<a id="using-the-newtype-pattern-to-implement-external-traits-on-external-types"></a>
<a id="using-the-newtype-pattern-to-implement-external-traits"></a>

### Implémenter des traits externes avec le patron newtype

Dans la section [« Implémenter un trait pour un type »][implementing-a-trait-on-a-type]<!--
ignore --> du chapitre 10, nous avons mentionné la règle de cohérence orpheline, qui stipule que nous ne pouvons implémenter un trait pour un type que si le trait ou le type, ou les deux, sont locaux à notre crate. Le patron newtype permet de contourner cette restriction. Il consiste à créer un nouveau type dans une structure tuple. (Nous avons vu les structures tuple dans la section [« Créer différents types avec des structures tuple »][tuple-structs]<!-- ignore --> du chapitre 5.) La structure tuple comportera un seul champ et servira de fine enveloppe autour du type pour lequel nous voulons implémenter un trait. Le type enveloppe sera alors local à notre crate, et nous pourrons implémenter le trait pour lui. Le terme _newtype_ vient du langage de programmation Haskell. Ce patron n’entraîne aucune pénalité de performance à l’exécution, et le type enveloppe est éliminé à la compilation.

Par exemple, imaginons que nous voulions implémenter `Display` pour `Vec<T>`. La règle de cohérence orpheline nous empêche de le faire directement, car le trait `Display` et le type `Vec<T>` sont définis en dehors de notre crate. Nous pouvons créer une structure `Wrapper` qui contient une instance de `Vec<T>`, puis implémenter `Display` pour `Wrapper` et utiliser la valeur `Vec<T>`, comme indiqué dans le Listing 20-24.

<Listing number="20-24" file-name="src/main.rs" caption="Créer un type `Wrapper` autour de `Vec<String>` pour implémenter `Display`">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-24/src/main.rs}}
```

</Listing>

L’implémentation de `Display` utilise `self.0` pour accéder au `Vec<T>` interne, car `Wrapper` est une structure tuple et `Vec<T>` est l’élément à l’indice 0 du tuple. Nous pouvons ensuite utiliser les fonctionnalités du trait `Display` pour `Wrapper`.

L’inconvénient de cette technique est que `Wrapper` est un nouveau type : il ne dispose donc pas des méthodes de la valeur qu’il contient. Nous devrions implémenter directement sur `Wrapper` toutes les méthodes de `Vec<T>`, en les faisant déléguer à `self.0`, ce qui nous permettrait de traiter `Wrapper` exactement comme un `Vec<T>`. Si nous voulons que le nouveau type dispose de toutes les méthodes du type interne, une solution consiste à implémenter le trait `Deref` pour `Wrapper` afin qu’il renvoie le type interne (nous avons abordé l’implémentation du trait `Deref` dans la section [« Traiter les pointeurs intelligents comme des références ordinaires »][smart-pointer-deref]<!-- ignore --> du chapitre 15). Si nous ne voulons pas que le type `Wrapper` dispose de toutes les méthodes du type interne — par exemple, pour en restreindre le comportement —, nous devons implémenter manuellement uniquement les méthodes souhaitées.

Le patron newtype est également utile même en l’absence de traits. Changeons maintenant de sujet et examinons quelques façons avancées d’interagir avec le système de types de Rust.

[newtype]: ch20-02-advanced-traits.html#implementing-external-traits-with-the-newtype-pattern
[implementing-a-trait-on-a-type]: ch10-02-traits.html#implementing-a-trait-on-a-type
[traits]: ch10-02-traits.html
[smart-pointer-deref]: ch15-02-deref.html#treating-smart-pointers-like-regular-references
[tuple-structs]: ch05-01-defining-structs.html#creating-different-types-with-tuple-structs