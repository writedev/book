<!-- Old headings. Do not remove or links may break. -->

<a id="treating-smart-pointers-like-regular-references-with-the-deref-trait"></a>
<a id="treating-smart-pointers-like-regular-references-with-deref"></a>

## Traiter les pointeurs intelligents comme des références ordinaires

L’implémentation du trait `Deref` vous permet de personnaliser le comportement de
l’_opérateur de déréférencement_ `*` (à ne pas confondre avec l’opérateur de
multiplication ou l’opérateur glob). En implémentant `Deref` de façon à ce
qu’un pointeur intelligent puisse être traité comme une référence ordinaire,
vous pouvez écrire du code qui fonctionne sur des références et utiliser aussi
ce code avec des pointeurs intelligents.

Commençons par examiner le fonctionnement de l’opérateur de déréférencement
avec des références ordinaires. Ensuite, nous essaierons de définir un type
personnalisé qui se comporte comme `Box<T>` et verrons pourquoi l’opérateur de
déréférencement ne fonctionne pas comme avec une référence sur notre type
nouvellement défini. Nous verrons comment l’implémentation du trait `Deref`
permet aux pointeurs intelligents de fonctionner de manière similaire aux
références. Enfin, nous examinerons la fonctionnalité de coercition par
déréférencement de Rust et la façon dont elle nous permet de travailler aussi
bien avec des références qu’avec des pointeurs intelligents.

<!-- Old headings. Do not remove or links may break. -->

<a id="following-the-pointer-to-the-value-with-the-dereference-operator"></a>
<a id="following-the-pointer-to-the-value"></a>

### Suivre la référence jusqu’à la valeur

Une référence ordinaire est un type de pointeur, et l’une des façons de
concevoir un pointeur consiste à le voir comme une flèche vers une valeur
stockée ailleurs. Dans l’exemple 15-6, nous créons une référence vers une
valeur `i32`, puis nous utilisons l’opérateur de déréférencement pour suivre
cette référence jusqu’à la valeur.

<Listing number="15-6" file-name="src/main.rs" caption="Utilisation de l’opérateur de déréférencement pour suivre une référence jusqu’à une valeur `i32`">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-06/src/main.rs}}
```

</Listing>

La variable `x` contient une valeur `i32` égale à `5`. Nous définissons `y`
comme une référence à `x`. Nous pouvons affirmer que `x` est égal à `5`.
Cependant, si nous voulons faire une assertion sur la valeur de `y`, nous
devons utiliser `*y` pour suivre la référence jusqu’à la valeur qu’elle pointe
(d’où le terme _déréférencement_), afin que le compilateur puisse comparer la
valeur réelle. Une fois `y` déréférencée, nous avons accès à la valeur entière
pointée par `y` et pouvons la comparer à `5`.

Si nous essayions plutôt d’écrire `assert_eq!(5, y);`, nous obtiendrions cette
erreur de compilation :

```console
{{#include ../listings/ch15-smart-pointers/output-only-01-comparing-to-reference/output.txt}}
```

La comparaison d’un nombre et d’une référence vers un nombre n’est pas
autorisée, car il s’agit de types différents. Nous devons utiliser l’opérateur
de déréférencement pour suivre la référence jusqu’à la valeur qu’elle pointe.

### Utiliser `Box<T>` comme une référence

Nous pouvons réécrire le code de l’exemple 15-6 pour utiliser un `Box<T>` au
lieu d’une référence ; l’opérateur de déréférencement appliqué au `Box<T>`
dans l’exemple 15-7 fonctionne de la même manière que celui appliqué à la
référence dans l’exemple 15-6.

<Listing number="15-7" file-name="src/main.rs" caption="Utilisation de l’opérateur de déréférencement sur un `Box<i32>`">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-07/src/main.rs}}
```

</Listing>

La principale différence entre les exemples 15-7 et 15-6 est qu’ici, nous
définissons `y` comme une instance de boîte pointant vers une copie de la
valeur de `x`, plutôt que comme une référence pointant vers la valeur de `x`.
Dans la dernière assertion, nous pouvons utiliser l’opérateur de
déréférencement pour suivre le pointeur de la boîte, comme nous l’avons fait
lorsque `y` était une référence. Ensuite, nous examinerons ce qui est
particulier à `Box<T>` et lui permet d’utiliser l’opérateur de déréférencement,
en définissant notre propre type de boîte.

### Définir notre propre pointeur intelligent

Construisons un type enveloppe similaire au type `Box<T>` fourni par la
bibliothèque standard, afin de découvrir comment les types de pointeurs
intelligents se comportent par défaut différemment des références. Ensuite,
nous verrons comment ajouter la possibilité d’utiliser l’opérateur de
déréférencement.

> Remarque : il existe une différence importante entre le type `MyBox<T>` que
> nous allons construire et le véritable `Box<T>` : notre version ne stockera
> pas ses données sur le tas. Cet exemple porte sur `Deref`, donc
> l’emplacement de stockage réel des données est moins important que le
> comportement semblable à celui d’un pointeur.

Le type `Box<T>` est finalement défini comme une structure tuple à un élément.
L’exemple 15-8 définit donc un type `MyBox<T>` de la même manière. Nous
définirons également une fonction `new` correspondant à la fonction `new`
définie sur `Box<T>`.

<Listing number="15-8" file-name="src/main.rs" caption="Définition d’un type `MyBox<T>`">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-08/src/main.rs:here}}
```

</Listing>

Nous définissons une structure nommée `MyBox` et déclarons un paramètre
générique `T`, car nous voulons que notre type puisse contenir des valeurs de
n’importe quel type. Le type `MyBox` est une structure tuple qui comporte un
élément de type `T`. La fonction `MyBox::new` prend un paramètre de type `T` et
renvoie une instance de `MyBox` contenant la valeur transmise.

Essayons d’ajouter à l’exemple 15-8 la fonction `main` de l’exemple 15-7 et de
la modifier pour utiliser le type `MyBox<T>` que nous avons défini au lieu de
`Box<T>`. Le code de l’exemple 15-9 ne compilera pas, car Rust ne sait pas
comment déréférencer `MyBox`.

<Listing number="15-9" file-name="src/main.rs" caption="Tentative d’utiliser `MyBox<T>` comme nous utilisions les références et `Box<T>`">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-09/src/main.rs:here}}
```

</Listing>

Voici l’erreur de compilation obtenue :

```console
{{#include ../listings/ch15-smart-pointers/listing-15-09/output.txt}}
```

Notre type `MyBox<T>` ne peut pas être déréférencé, car nous n’avons pas
implémenté cette capacité pour notre type. Pour permettre le déréférencement
avec l’opérateur `*`, nous implémentons le trait `Deref`.

<!-- Old headings. Do not remove or links may break. -->

<a id="treating-a-type-like-a-reference-by-implementing-the-deref-trait"></a>

### Implémenter le trait `Deref`

Comme nous l’avons vu dans [« Implémenter un trait sur un type »][impl-trait]<!-- ignore --> au
chapitre 10, pour implémenter un trait, nous devons fournir des implémentations
pour ses méthodes obligatoires. Le trait `Deref`, fourni par la bibliothèque
standard, nous demande d’implémenter une méthode nommée `deref` qui emprunte
`self` et renvoie une référence aux données internes. L’exemple 15-10 contient
une implémentation de `Deref` à ajouter à la définition de `MyBox<T>`.

<Listing number="15-10" file-name="src/main.rs" caption="Implémentation de `Deref` sur `MyBox<T>`">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-10/src/main.rs:here}}
```

</Listing>

La syntaxe `type Target = T;` définit un type associé que le trait `Deref`
utilise. Les types associés sont une manière légèrement différente de déclarer
un paramètre générique, mais vous n’avez pas besoin de vous en préoccuper pour
l’instant ; nous les aborderons plus en détail au chapitre 20.

Nous remplissons le corps de la méthode `deref` avec `&self.0` afin qu’elle
renvoie une référence à la valeur à laquelle nous voulons accéder avec
l’opérateur `*` ; rappelez-vous, d’après [« Créer différents types avec des structures tuple »][tuple-structs]<!--
ignore --> au chapitre 5, que `.0` accède à la première valeur d’une structure
tuple. La fonction `main` de l’exemple 15-9, qui appelle `*` sur la valeur
`MyBox<T>`, compile désormais, et les assertions réussissent !

Sans le trait `Deref`, le compilateur ne peut déréférencer que les références
`&`. La méthode `deref` permet au compilateur de prendre une valeur de
n’importe quel type qui implémente `Deref`, puis d’appeler la méthode `deref`
pour obtenir une référence qu’il sait déréférencer.

Lorsque nous avons saisi `*y` dans l’exemple 15-9, Rust a en réalité exécuté
ce code en coulisses :

```rust,ignore
*(y.deref())
```

Rust remplace l’opérateur `*` par un appel à la méthode `deref`, suivi d’un
déréférencement ordinaire, afin que nous n’ayons pas à nous demander si nous
devons appeler la méthode `deref`. Cette fonctionnalité de Rust nous permet
d’écrire du code qui fonctionne de manière identique, que nous ayons une
référence ordinaire ou un type qui implémente `Deref`.

La raison pour laquelle la méthode `deref` renvoie une référence à une valeur,
et pour laquelle le déréférencement ordinaire en dehors des parenthèses dans
`*(y.deref())` reste nécessaire, tient au système de propriété. Si la méthode
`deref` renvoyait directement la valeur au lieu d’une référence vers celle-ci,
la valeur serait déplacée hors de `self`. Dans ce cas, comme dans la plupart
des cas où nous utilisons l’opérateur de déréférencement, nous ne voulons pas
prendre possession de la valeur interne de `MyBox<T>`.

Notez que l’opérateur `*` est remplacé par un appel à la méthode `deref`, puis
par un appel à l’opérateur `*`, une seule fois à chaque utilisation de `*`
dans notre code. Comme le remplacement de l’opérateur `*` ne se répète pas à
l’infini, nous obtenons des données de type `i32`, ce qui correspond au `5`
dans `assert_eq!` de l’exemple 15-9.

<!-- Old headings. Do not remove or links may break. -->

<a id="implicit-deref-coercions-with-functions-and-methods"></a>
<a id="using-deref-coercions-in-functions-and-methods"></a>

### Utiliser la coercition par déréférencement dans les fonctions et les méthodes

La _coercition par déréférencement_ convertit une référence vers un type qui
implémente le trait `Deref` en une référence vers un autre type. Par exemple,
la coercition par déréférencement peut convertir `&String` en `&str`, car
`String` implémente le trait `Deref` de façon à renvoyer `&str`. La coercition
par déréférencement est une commodité que Rust applique aux arguments des
fonctions et des méthodes, et elle ne fonctionne que sur les types qui
implémentent le trait `Deref`. Elle s’effectue automatiquement lorsque nous
transmettons en argument à une fonction ou à une méthode une référence à la
valeur d’un type donné qui ne correspond pas au type du paramètre dans la
définition de cette fonction ou de cette méthode. Une suite d’appels à la
méthode `deref` convertit le type fourni en celui attendu par le paramètre.

La coercition par déréférencement a été ajoutée à Rust afin que les
programmeurs qui écrivent des appels de fonction et de méthode n’aient pas à
ajouter autant de références et de déréférencements explicites avec `&` et
`*`. Cette fonctionnalité nous permet également d’écrire davantage de code
pouvant fonctionner aussi bien avec des références qu’avec des pointeurs
intelligents.

Pour voir la coercition par déréférencement en action, utilisons le type
`MyBox<T>` défini dans l’exemple 15-8 ainsi que l’implémentation de `Deref`
ajoutée dans l’exemple 15-10. L’exemple 15-11 montre la définition d’une
fonction dont le paramètre est une tranche de chaîne.

<Listing number="15-11" file-name="src/main.rs" caption="Une fonction `hello` dont le paramètre `name` est de type `&str`">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-11/src/main.rs:here}}
```

</Listing>

Nous pouvons appeler la fonction `hello` en lui passant une tranche de chaîne
en argument, par exemple `hello("Rust");`. La coercition par déréférencement
permet d’appeler `hello` avec une référence vers une valeur de type
`MyBox<String>`, comme le montre l’exemple 15-12.

<Listing number="15-12" file-name="src/main.rs" caption="Appel de `hello` avec une référence vers une valeur `MyBox<String>`, rendu possible par la coercition par déréférencement">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-12/src/main.rs:here}}
```

</Listing>

Ici, nous appelons la fonction `hello` avec l’argument `&m`, qui est une
référence vers une valeur `MyBox<String>`. Comme nous avons implémenté le
trait `Deref` sur `MyBox<T>` dans l’exemple 15-10, Rust peut convertir
`&MyBox<String>` en `&String` en appelant `deref`. La bibliothèque standard
fournit une implémentation de `Deref` pour `String` qui renvoie une tranche de
chaîne, comme l’indique la documentation de l’API de `Deref`. Rust appelle à
nouveau `deref` pour convertir `&String` en `&str`, ce qui correspond à la
définition de la fonction `hello`.

Si Rust n’implémentait pas la coercition par déréférencement, nous devrions
écrire le code de l’exemple 15-13 plutôt que celui de l’exemple 15-12 pour
appeler `hello` avec une valeur de type `&MyBox<String>`.

<Listing number="15-13" file-name="src/main.rs" caption="Le code que nous devrions écrire si Rust ne disposait pas de la coercition par déréférencement">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-13/src/main.rs:here}}
```

</Listing>

`(*m)` déréférence le `MyBox<String>` pour obtenir un `String`. Ensuite, `&`
et `[..]` produisent une tranche de chaîne couvrant l’intégralité du `String`,
afin de correspondre à la signature de `hello`. Sans coercition par
déréférencement, ce code est plus difficile à lire, à écrire et à comprendre,
avec tous ces symboles. La coercition par déréférencement permet à Rust
d’effectuer ces conversions automatiquement pour nous.

Lorsque le trait `Deref` est défini pour les types concernés, Rust analyse les
types et utilise `Deref::deref` autant de fois que nécessaire pour obtenir une
référence correspondant au type du paramètre. Le nombre d’appels à
`Deref::deref` à insérer est déterminé à la compilation : la coercition par
déréférencement n’entraîne donc aucun coût à l’exécution !

<!-- Old headings. Do not remove or links may break. -->

<a id="how-deref-coercion-interacts-with-mutability"></a>

### Gérer la coercition par déréférencement avec des références mutables

De même que vous pouvez utiliser le trait `Deref` pour redéfinir l’opérateur
`*` sur des références immuables, vous pouvez utiliser le trait `DerefMut`
pour redéfinir l’opérateur `*` sur des références mutables.

Rust effectue une coercition par déréférencement lorsqu’il trouve des types et
des implémentations de traits dans trois cas :

1. De `&T` vers `&U` lorsque `T: Deref<Target=U>`
2. De `&mut T` vers `&mut U` lorsque `T: DerefMut<Target=U>`
3. De `&mut T` vers `&U` lorsque `T: Deref<Target=U>`

Les deux premiers cas sont identiques, à ceci près que le second concerne la
mutabilité. Le premier cas indique que si vous avez un `&T` et que `T`
implémente `Deref` vers un type `U`, vous pouvez obtenir un `&U` de manière
transparente. Le deuxième cas indique que la même coercition par
déréférencement s’applique aux références mutables.

Le troisième cas est plus délicat : Rust peut aussi convertir une référence
mutable en une référence immuable. En revanche, l’inverse n’est _pas_
possible : les références immuables ne seront jamais converties en références
mutables. D’après les règles d’emprunt, si vous avez une référence mutable,
celle-ci doit être la seule référence vers ces données (sinon, le programme ne
compilerait pas). Convertir une référence mutable en une référence immuable ne
peut jamais enfreindre les règles d’emprunt. Convertir une référence immuable
en une référence mutable exigerait que la référence immuable initiale soit la
seule référence immuable vers ces données, mais les règles d’emprunt ne le
garantissent pas. Rust ne peut donc pas supposer qu’il est possible de
convertir une référence immuable en une référence mutable.

[impl-trait]: ch10-02-traits.html#implementing-a-trait-on-a-type
[tuple-structs]: ch05-01-defining-structs.html#creating-different-types-with-tuple-structs