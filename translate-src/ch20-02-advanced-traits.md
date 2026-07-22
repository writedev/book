## Traits Avancés

Nous avons d'abord abordé les traits dans la section [« Définir un comportement partagé avec des traits »][traits]<!-- ignore --> au chapitre 10, mais nous n'avons pas discuté des détails plus avancés. Maintenant que vous en savez davantage sur Rust, nous pouvons entrer dans le vif du sujet.

### Définir des traits avec des types associés

Les _types associés_ connectent un espace réservé de type à un trait de manière à ce que les définitions de méthodes de trait puissent utiliser ces types de remplacement dans leurs signatures. L'implémenteur d'un trait spécifiera le type concret à utiliser à la place du type de remplacement pour l'implémentation particulière. De cette manière, nous pouvons définir un trait qui utilise certains types sans avoir besoin de connaître exactement quels types sont requis jusqu'à ce que le trait soit implémenté.

Nous avons décrit la plupart des fonctionnalités avancées dans ce chapitre comme rarement nécessaires. Les types associés se situent quelque part au milieu : ils sont utilisés moins fréquemment que les fonctionnalités expliquées dans le reste du livre, mais plus couramment que beaucoup d'autres fonctionnalités discutées dans ce chapitre.

Un exemple d'un trait avec un type associé est le trait `Iterator` fourni par la bibliothèque standard. Le type associé est nommé `Item` et représente le type des valeurs que le type implémentant le trait `Iterator` est en train d'itérer. La définition du trait `Iterator` est comme indiqué dans la liste 20-13.

<Listing number="20-13" caption="La définition du trait `Iterator` qui a un type associé `Item`">

```rust,noplayground
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-13/src/lib.rs}}
```

</Listing>

Le type `Item` est un espace réservé, et la définition de la méthode `next` montre qu'elle renverra des valeurs de type `Option<Self::Item>`. Les implémenteurs du trait `Iterator` spécifieront le type concret pour `Item`, et la méthode `next` renverra une `Option` contenant une valeur de ce type concret.

Les types associés peuvent sembler similaires au concept de génériques, dans la mesure où ces derniers nous permettent de définir une fonction sans spécifier quels types elle peut gérer. Pour examiner la différence entre les deux concepts, nous allons regarder une implémentation du trait `Iterator` sur un type nommé `Counter` qui spécifie que le type `Item` est `u32` :

<Listing file-name="src/lib.rs">

```rust,ignore
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-22-iterator-on-counter/src/lib.rs:ch19}}
```

</Listing>

Cette syntaxe semble comparable à celle des génériques. Alors, pourquoi ne pas simplement définir le trait `Iterator` avec des génériques, comme montré dans la liste 20-14 ?

<Listing number="20-14" caption="Une définition hypothétique du trait `Iterator` utilisant des génériques">

```rust,noplayground
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-14/src/lib.rs}}
```

</Listing>

La différence est que lors de l'utilisation de génériques, comme dans la liste 20-14, nous devons annoter les types dans chaque implémentation ; comme nous pouvons également implémenter `Iterator<String> pour Counter` ou tout autre type, nous pourrions avoir plusieurs implémentations d'`Iterator` pour `Counter`. En d'autres termes, lorsqu'un trait a un paramètre générique, il peut être implémenté pour un type plusieurs fois, modifiant les types concrets des paramètres de type générique à chaque fois. Lorsque nous utilisons la méthode `next` sur `Counter`, nous devrions fournir des annotations de type pour indiquer quelle implémentation de `Iterator` nous voulons utiliser.

Avec des types associés, nous n'avons pas besoin d'annoter les types, car nous ne pouvons pas implémenter un trait sur un type plusieurs fois. Dans la liste 20-13 avec la définition qui utilise des types associés, nous pouvons choisir ce que sera le type de `Item` une seule fois, car il ne peut y avoir qu'un seul `impl Iterator pour Counter`. Nous n'avons pas à spécifier que nous voulons un itérateur de valeurs `u32` partout où nous appelons `next` sur `Counter`.

Les types associés font également partie du contrat du trait : les implémenteurs du trait doivent fournir un type pour se substituer à l'espace réservé de type associé. Les types associés ont souvent un nom qui décrit comment le type sera utilisé, et documenter le type associé dans la documentation de l'API est une bonne pratique.

### Utiliser des paramètres de type génériques par défaut et la surcharge d'opérateurs

Lorsque nous utilisons des paramètres de type génériques, nous pouvons spécifier un type concret par défaut pour le type générique. Cela élimine le besoin pour les implémenteurs du trait de spécifier un type concret si le type par défaut fonctionne. Vous spécifiez un type par défaut lors de la déclaration d'un type générique avec la syntaxe `<PlaceholderType=ConcreteType>`.

Un excellent exemple d'une situation où cette technique est utile est la _surcharge d'opérateurs_, dans laquelle vous personnalisez le comportement d'un opérateur (tel que `+`) dans des situations particulières.

Rust ne vous permet pas de créer vos propres opérateurs ou de surcharger des opérateurs arbitraires. Mais vous pouvez surcharger les opérations et les traits correspondants énumérés dans `std::ops` en implémentant les traits associés à l'opérateur. Par exemple, dans la liste 20-15, nous surchargeons l'opérateur `+` pour additionner deux instances de `Point`. Nous faisons cela en implémentant le trait `Add` sur une structure `Point`.

<Listing number="20-15" file-name="src/main.rs" caption="Implémentation du trait `Add` pour surcharger l'opérateur `+` pour les instances de `Point`">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-15/src/main.rs}}
```

</Listing>

La méthode `add` additionne les valeurs `x` de deux instances de `Point` et les valeurs `y` de deux instances de `Point` pour créer un nouveau `Point`. Le trait `Add` a un type associé nommé `Output` qui détermine le type retourné par la méthode `add`.

Le type générique par défaut dans ce code se trouve dans le trait `Add`. Voici sa définition :

```rust
trait Add<Rhs=Self> {
    type Output;

    fn add(self, rhs: Rhs) -> Self::Output;
}
```

Ce code devrait sembler généralement familier : un trait avec une méthode et un type associé. La nouvelle partie est `Rhs=Self` : cette syntaxe s'appelle _paramètres de type par défaut_. Le paramètre générique `Rhs` (abréviation de « côté droit ») définit le type du paramètre `rhs` dans la méthode `add`. Si nous ne spécifions pas de type concret pour `Rhs` lorsque nous implémentons le trait `Add`, le type de `Rhs` sera par défaut `Self`, qui sera le type sur lequel nous implémentons `Add`.

Lorsque nous avons implémenté `Add` pour `Point`, nous avons utilisé la valeur par défaut pour `Rhs` car nous voulions additionner deux instances de `Point`. Regardons un exemple d'implémentation du trait `Add` où nous souhaitons personnaliser le type `Rhs` au lieu d'utiliser la valeur par défaut.

Nous avons deux structures, `Millimeters` et `Meters`, contenant des valeurs dans différentes unités. Cette légère encapsulation d'un type existant dans une autre structure est connue sous le nom de _motif newtype_, que nous décrivons plus en détail dans la section [« Implémentation de traits externes avec le motif newtype »][newtype]<!-- ignore -->. Nous souhaitons additionner des valeurs en millimètres aux valeurs en mètres et nous voulons que l'implémentation de `Add` fasse la conversion correctement. Nous pouvons implémenter `Add` pour `Millimeters` avec `Meters` comme `Rhs`, comme montré dans la liste 20-16.

<Listing number="20-16" file-name="src/lib.rs" caption="Implémentation du trait `Add` sur `Millimeters` pour additionner `Millimeters` et `Meters`">

```rust,noplayground
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-16/src/lib.rs}}
```

</Listing>

Pour additionner `Millimeters` et `Meters`, nous spécifions `impl Add<Meters>` pour définir la valeur du paramètre de type `Rhs` au lieu d'utiliser la valeur par défaut de `Self`.

Vous utiliserez des paramètres de type par défaut de deux manières principales :

1. Pour étendre un type sans casser le code existant
2. Pour permettre une personnalisation dans des cas spécifiques dont la plupart des utilisateurs n'auront pas besoin

Le trait `Add` de la bibliothèque standard est un exemple du deuxième objectif : en général, vous ajouterez deux types similaires, mais le trait `Add` fournit la possibilité de personnaliser au-delà de cela. L'utilisation d'un paramètre de type par défaut dans la définition du trait `Add` signifie que vous n'avez pas à spécifier le paramètre supplémentaire la plupart du temps. En d'autres termes, un peu de code d'implémentation boilerplate n'est pas nécessaire, ce qui facilite l'utilisation du trait.

Le premier objectif est similaire au second, mais à l'inverse : si vous voulez ajouter un paramètre de type à un trait existant, vous pouvez lui donner une valeur par défaut pour permettre l'extension de la fonctionnalité du trait sans casser le code d'implémentation existant.

### Disambiguation entre des méthodes portant le même nom

Rien dans Rust n'empêche un trait d'avoir une méthode portant le même nom qu'une méthode d'un autre trait, ni Rust n'empêche d'implémenter les deux traits sur un même type. Il est également possible d'implémenter une méthode directement sur le type avec le même nom que des méthodes de traits.

Lorsque vous appelez des méthodes portant le même nom, vous devez indiquer à Rust laquelle vous souhaitez utiliser. Considérez le code de la liste 20-17 où nous avons défini deux traits, `Pilot` et `Wizard`, qui ont tous deux une méthode appelée `fly`. Nous implémentons ensuite les deux traits sur un type `Human` qui a déjà une méthode nommée `fly`. Chaque méthode `fly` fait quelque chose de différent.

<Listing number="20-17" file-name="src/main.rs" caption="Deux traits sont définis pour avoir une méthode `fly` et sont implémentés sur le type `Human`, et une méthode `fly` est implémentée sur `Human` directement.">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-17/src/main.rs:here}}
```

</Listing>

Lorsque nous appelons `fly` sur une instance de `Human`, le compilateur appelle par défaut la méthode qui est directement implémentée sur le type, comme le montre la liste 20-18.

<Listing number="20-18" file-name="src/main.rs" caption="Appel de `fly` sur une instance de `Human`">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-18/src/main.rs:here}}
```

</Listing>

L'exécution de ce code affichera `*waving arms furiously*`, montrant que Rust a appelé la méthode `fly` implémentée directement sur `Human`.

Pour appeler les méthodes `fly` du trait `Pilot` ou du trait `Wizard`, nous devons utiliser une syntaxe plus explicite pour indiquer quelle méthode `fly` nous voulons appeler. La liste 20-19 démontre cette syntaxe.

<Listing number="20-19" file-name="src/main.rs" caption="Spécifiant quelle méthode `fly` de trait nous voulons appeler">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-19/src/main.rs:here}}
```

</Listing>

Spécifier le nom du trait avant le nom de la méthode clarifie à Rust quelle implémentation de `fly` nous souhaitons appeler. Nous pourrions également écrire `Human::fly(&person)`, qui est équivalent à `person.fly()` que nous avons utilisé dans la liste 20-19, mais cela est un peu plus long à écrire si nous n'avons pas besoin de désambiguïser.

L'exécution de ce code affiche ce qui suit :

```console
{{#include ../listings/ch20-advanced-features/listing-20-19/output.txt}}
```

Parce que la méthode `fly` prend un paramètre `self`, si nous avions deux _types_ qui implémentent tous deux un _trait_, Rust pourrait déterminer quelle implémentation d'un trait utiliser en fonction du type de `self`.

Cependant, les fonctions associées qui ne sont pas des méthodes n'ont pas de paramètre `self`. Lorsqu'il y a plusieurs types ou traits définissant des fonctions non-méthodes avec le même nom de fonction, Rust ne sait pas toujours quel type vous voulez dire à moins que vous n'utilisiez une syntaxe complètement qualifiée. Par exemple, dans la liste 20-20, nous créons un trait pour un refuge pour animaux qui souhaite nommer tous les chiots "Spot". Nous créons un trait `Animal` avec une fonction non-méthode associée `baby_name`. Le trait `Animal` est implémenté pour la structure `Dog`, sur laquelle nous fournissons également une fonction non-méthode associée `baby_name` directement.

<Listing number="20-20" file-name="src/main.rs" caption="Un trait avec une fonction associée et un type avec une fonction associée du même nom qui implémente également le trait">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-20/src/main.rs}}
```

</Listing>

Nous implémentons le code pour nommer tous les chiots "Spot" dans la fonction associée `baby_name` qui est définie sur `Dog`. Le type `Dog` implémente également le trait `Animal`, qui décrit les caractéristiques que tous les animaux ont. Les chiots s'appellent en réalité "puppies", et cela est exprimé dans l'implémentation du trait `Animal` sur `Dog` dans la fonction `baby_name` associée au trait `Animal`.

Dans `main`, nous appelons la fonction `Dog::baby_name`, qui appelle directement la fonction associée définie sur `Dog`. Ce code imprime ce qui suit :

```console
{{#include ../listings/ch20-advanced-features/listing-20-20/output.txt}}
```

Cette sortie n'est pas ce que nous voulions. Nous souhaitons appeler la fonction `baby_name` qui fait partie du trait `Animal` que nous avons implémenté sur `Dog`, pour que le code imprime `Un chiot s'appelle un puppy`. La technique de spécification du nom du trait que nous avons utilisée dans la liste 20-19 ne convient pas ici ; si nous changeons `main` pour le code de la liste 20-21, nous obtiendrons une erreur de compilation.

<Listing number="20-21" file-name="src/main.rs" caption="Tentative d'appel de la fonction `baby_name` du trait `Animal`, mais Rust ne sait pas quelle implémentation utiliser">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-21/src/main.rs:here}}
```

</Listing>

Parce que `Animal::baby_name` n'a pas de paramètre `self`, et qu'il pourrait y avoir d'autres types qui implémentent le trait `Animal`, Rust ne peut pas déterminer quelle implémentation de `Animal::baby_name` nous voulons. Nous obtiendrons cette erreur du compilateur :

```console
{{#include ../listings/ch20-advanced-features/listing-20-21/output.txt}}
```

Pour désambigüiser et indiquer à Rust que nous voulons utiliser l'implémentation d'`Animal` pour `Dog` plutôt que l'implémentation d'`Animal` pour un autre type, nous devons utiliser une syntaxe complètement qualifiée. La liste 20-22 démontre comment utiliser une syntaxe complètement qualifiée.

<Listing number="20-22" file-name="src/main.rs" caption="Utilisation de la syntaxe complètement qualifiée pour spécifier que nous voulons appeler la fonction `baby_name` du trait `Animal` tel qu'implémenté sur `Dog`">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-22/src/main.rs:here}}
```

</Listing>

Nous fournissons à Rust une annotation de type dans les chevrons, ce qui indique que nous voulons appeler la méthode `baby_name` du trait `Animal` tel qu'implémenté sur `Dog` en déclarant que nous voulons traiter le type `Dog` comme un `Animal` pour cet appel de fonction. Ce code affichera désormais ce que nous voulons :

```console
{{#include ../listings/ch20-advanced-features/listing-20-22/output.txt}}
```

En général, la syntaxe complètement qualifiée est définie comme suit :

```rust,ignore
<Type as Trait>::function(receiver_if_method, next_arg, ...);
```

Pour les fonctions associées qui ne sont pas des méthodes, il n'y aurait pas de `receiver` : il n'y aurait que la liste d'autres arguments. Vous pourriez utiliser la syntaxe complètement qualifiée partout où vous appelez des fonctions ou des méthodes. Cependant, vous êtes autorisé à omettre toute partie de cette syntaxe que Rust peut déterminer à partir d'autres informations dans le programme. Vous n'avez besoin d'utiliser cette syntaxe plus verbeuse que dans les cas où il existe plusieurs implémentations utilisant le même nom et où Rust a besoin d'aide pour identifier quelle implémentation vous voulez appeler.

### Utiliser des supertraits

Parfois, vous pourriez écrire une définition de trait qui dépend d'un autre trait : pour qu'un type implémente le premier trait, vous souhaitez exiger que ce type implémente également le second trait. Vous feriez cela afin que votre définition de trait puisse utiliser les éléments associés du second trait. Le trait sur lequel votre définition de trait s'appuie est appelé un _supertrait_ de votre trait.

Par exemple, disons que nous voulons créer un trait `OutlinePrint` avec une méthode `outline_print` qui imprimera une valeur donnée formatée de manière à ce qu'elle soit encadrée par des astérisques. C'est-à-dire, étant donné une structure `Point` qui implémente le trait `Display` de la bibliothèque standard pour donner `(x, y)`, lorsque nous appelons `outline_print` sur une instance de `Point` ayant `1` pour `x` et `3` pour `y`, elle devrait imprimer ce qui suit :

```text
**********
*        *
* (1, 3) *
*        *
**********
```

Dans l'implémentation de la méthode `outline_print`, nous voulons utiliser la fonctionnalité du trait `Display`. Par conséquent, nous devons spécifier que le trait `OutlinePrint` fonctionnera uniquement pour les types qui implémentent également `Display` et fournissent la fonctionnalité dont `OutlinePrint` a besoin. Nous pouvons le faire dans la définition du trait en spécifiant `OutlinePrint: Display`. Cette technique est similaire à l'ajout d'une contrainte de trait au trait. La liste 20-23 montre une implémentation du trait `OutlinePrint`.

<Listing number="20-23" file-name="src/main.rs" caption="Implémentation du trait `OutlinePrint` qui nécessite la fonctionnalité du `Display`">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-23/src/main.rs:here}}
```

</Listing>

Parce que nous avons spécifié que `OutlinePrint` nécessite le trait `Display`, nous pouvons utiliser la fonction `to_string` qui est automatiquement implémentée pour tout type implémentant `Display`. Si nous essayons d'utiliser `to_string` sans ajouter de deux-points et spécifier le trait `Display` après le nom du trait, nous obtiendrons une erreur disant qu'aucune méthode nommée `to_string` n'a été trouvée pour le type `&Self` dans la portée actuelle.

Voyons ce qui se passe lorsque nous essayons d'implémenter `OutlinePrint` sur un type qui n'implémente pas `Display`, tel que la structure `Point` :

<Listing file-name="src/main.rs">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-02-impl-outlineprint-for-point/src/main.rs:here}}
```

</Listing>

Nous avons une erreur disant que `Display` est requis mais pas implémenté :

```console
{{#include ../listings/ch20-advanced-features/no-listing-02-impl-outlineprint-for-point/output.txt}}
```

Pour corriger cela, nous implémentons `Display` sur `Point` et satisfaisons la contrainte que `OutlinePrint` exige, comme suit :

<Listing file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-03-impl-display-for-point/src/main.rs:here}}
```

</Listing>

Ensuite, implémenter le trait `OutlinePrint` sur `Point` compilera avec succès, et nous pourrons appeler `outline_print` sur une instance de `Point` pour l'afficher dans une bordure d'astérisques.

### Implémenter des traits externes avec le motif newtype

Dans la section [« Implémenter un trait sur un type »][implementing-a-trait-on-a-type]<!-- ignore --> du chapitre 10, nous avons mentionné la règle des orphelins qui stipule que nous n'avons le droit d'implémenter un trait sur un type que si soit le trait, soit le type, ou les deux, sont locaux à notre crate. Il est possible de contourner cette restriction en utilisant le motif newtype, qui consiste à créer un nouveau type dans une structure tuple. (Nous avons couvert les structures tuple dans la section [« Créer différents types avec des structures tuple »][tuple-structs]<!-- ignore --> du chapitre 5.) La structure tuple aura un champ et sera un léger wrapper autour du type pour lequel nous souhaitons implémenter un trait. Ensuite, le type de wrapper est local à notre crate, et nous pouvons implémenter le trait sur le wrapper. _Newtype_ est un terme qui provient du langage de programmation Haskell. Il n'y a pas de pénalité de performance d'exécution pour l'utilisation de ce motif, et le type de wrapper est éludé à la compilation.

Par exemple, disons que nous voulons implémenter `Display` sur `Vec<T>`, ce que la règle des orphelins nous empêche de faire directement, car le trait `Display` et le type `Vec<T>` sont définis en dehors de notre crate. Nous pouvons créer une structure `Wrapper` qui contient une instance de `Vec<T>` ; ensuite, nous pouvons implémenter `Display` sur `Wrapper` et utiliser la valeur de `Vec<T>`, comme indiqué dans la liste 20-24.

<Listing number="20-24" file-name="src/main.rs" caption="Création d'un type `Wrapper` autour de `Vec<String>` pour implémenter `Display`">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-24/src/main.rs}}
```

</Listing>

L'implémentation de `Display` utilise `self.0` pour accéder au `Vec<T>` interne, car `Wrapper` est une structure tuple et `Vec<T>` est l'élément à l'index 0 dans le tuple. Ensuite, nous pouvons utiliser la fonctionnalité du trait `Display` sur `Wrapper`.

L'inconvénient d'utiliser cette technique est que `Wrapper` est un nouveau type, donc il n'a pas les méthodes de la valeur qu'il détient. Nous devrions implémenter toutes les méthodes de `Vec<T>` directement sur `Wrapper` de sorte que les méthodes délèguent à `self.0`, ce qui nous permettrait de traiter `Wrapper` exactement comme un `Vec<T>`. Si nous voulions que le nouveau type ait toutes les méthodes que le type interne possède, implémenter le trait `Deref` sur le `Wrapper` pour renvoyer le type interne serait une solution (nous avons discuté de l'implémentation du trait `Deref` dans la section [« Traiter les pointeurs intelligents comme des références régulières »][smart-pointer-deref]<!-- ignore --> au chapitre 15). Si nous ne voulons pas que le type `Wrapper` ait toutes les méthodes du type interne, par exemple, pour restreindre le comportement du type `Wrapper`, nous devrions implémenter manuellement uniquement les méthodes que nous voulons.

Ce motif newtype est également utile même lorsque des traits ne sont pas impliqués. Changeons de focus et examinons quelques manières avancées d'interagir avec le système de types de Rust.

[newtype]: ch20-02-advanced-traits.html#implementing-external-traits-with-the-newtype-pattern
[implementing-a-trait-on-a-type]: ch10-02-traits.html#implementing-a-trait-on-a-type
[traits]: ch10-02-traits.html
[smart-pointer-deref]: ch15-02-deref.html#treating-smart-pointers-like-regular-references
[tuple-structs]: ch05-01-defining-structs.html#creating-different-types-with-tuple-structs
