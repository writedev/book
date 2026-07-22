<!-- Anciens titres. Ne pas supprimer ou les liens peuvent se briser. -->

<a id="traiter-les-pointeurs-intelligents-comme-des-références-classiques-avec-le-trait-deref"></a>
<a id="traiter-les-pointeurs-intelligents-comme-des-références-classiques-avec-deref"></a>

## Traiter les Pointeurs Intelligents Comme des Références Classiques

L'implémentation du trait `Deref` vous permet de personnaliser le comportement de l'opérateur de _déréférencement_ `*` (à ne pas confondre avec l'opérateur de multiplication ou l'opérateur glob). En implémentant `Deref` de manière à ce qu'un pointeur intelligent puisse être traité comme une référence classique, vous pouvez écrire du code qui fonctionne avec des références et utiliser ce code avec des pointeurs intelligents également.

Examinons d'abord comment l'opérateur de déréférencement fonctionne avec des références classiques. Ensuite, nous essaierons de définir un type personnalisé qui se comporte comme `Box<T>` et verrons pourquoi l'opérateur de déréférencement ne fonctionne pas comme une référence sur notre type nouvellement défini. Nous explorerons comment l'implémentation du trait `Deref` permet aux pointeurs intelligents de fonctionner de manière similaire aux références. Ensuite, nous examinerons la fonctionnalité de coercition de déréférencement de Rust et comment elle nous permet de travailler avec des références ou des pointeurs intelligents.

<!-- Anciens titres. Ne pas supprimer ou les liens peuvent se briser. -->

<a id="suivre-le-pointeur-jusqu'à-la-valeur-avec-l-opérateur-de-déréférencement"></a>
<a id="suivre-le-pointeur-jusqu'à-la-valeur"></a>

### Suivre la Référence Jusqu'à la Valeur

Une référence classique est un type de pointeur, et une manière de penser à un pointeur est comme une flèche pointant vers une valeur stockée ailleurs. Dans le Listing 15-6, nous créons une référence à une valeur `i32` puis utilisons l'opérateur de déréférencement pour suivre la référence jusqu'à la valeur.

<Listing number="15-6" file-name="src/main.rs" caption="Utilisation de l'opérateur de déréférencement pour suivre une référence à une valeur `i32`">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-06/src/main.rs}}
```

</Listing>

La variable `x` contient une valeur `i32` de `5`. Nous attribuons à `y` une référence à `x`. Nous pouvons affirmer que `x` est égal à `5`. Cependant, si nous voulons faire une affirmation sur la valeur dans `y`, nous devons utiliser `*y` pour suivre la référence à la valeur à laquelle elle pointe (d'où _déréférencer_) afin que le compilateur puisse comparer la valeur réelle. Une fois que nous déréférons `y`, nous avons accès à la valeur entière à laquelle `y` pointe que nous pouvons comparer avec `5`.

Si nous essayions d'écrire `assert_eq!(5, y);` à la place, nous obtiendrions cette erreur de compilation :

```console
{{#include ../listings/ch15-smart-pointers/output-only-01-comparing-to-reference/output.txt}}
```

Comparer un nombre et une référence à un nombre n'est pas autorisé car ce sont des types différents. Nous devons utiliser l'opérateur de déréférencement pour suivre la référence jusqu'à la valeur à laquelle elle pointe.

### Utiliser `Box<T>` Comme une Référence

Nous pouvons réécrire le code du Listing 15-6 pour utiliser un `Box<T>` au lieu d'une référence ; l'opérateur de déréférencement utilisé sur le `Box<T>` dans le Listing 15-7 fonctionne de la même manière que l'opérateur de déréférencement utilisé sur la référence dans le Listing 15-6.

<Listing number="15-7" file-name="src/main.rs" caption="Utilisation de l'opérateur de déréférencement sur un `Box<i32>`">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-07/src/main.rs}}
```

</Listing>

La principale différence entre le Listing 15-7 et le Listing 15-6 est que ici nous définissons `y` comme une instance d'une boîte pointant vers une valeur copiée de `x` plutôt qu'une référence pointant vers la valeur de `x`. Dans la dernière affirmation, nous pouvons utiliser l'opérateur de déréférencement pour suivre le pointeur de la boîte de la même manière que nous l'avons fait lorsque `y` était une référence. Ensuite, nous explorerons ce qui est spécial à propos de `Box<T>` qui nous permet d'utiliser l'opérateur de déréférencement en définissant notre propre type de boîte.

### Définir Notre Propre Pointeur Intelligent

Construisons un type de wrapper similaire au type `Box<T>` fourni par la bibliothèque standard pour expérimenter comment les types de pointeurs intelligents se comportent différemment des références par défaut. Ensuite, nous verrons comment ajouter la capacité d'utiliser l'opérateur de déréférencement.

> Remarque : Il existe une grande différence entre le type `MyBox<T>` que nous allons construire et le vrai `Box<T>` : Notre version ne stockera pas ses données sur le tas. Nous concentrons cet exemple sur `Deref`, donc l'endroit où les données sont effectivement stockées est moins important que le comportement similaire à celui d'un pointeur.

Le type `Box<T>` est finalement défini comme une structure tuple avec un élément, donc le Listing 15-8 définit un type `MyBox<T>` de la même manière. Nous définirons également une fonction `new` pour correspondre à la fonction `new` définie sur `Box<T>`.

<Listing number="15-8" file-name="src/main.rs" caption="Définir un type `MyBox<T>`">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-08/src/main.rs:here}}
```

</Listing>

Nous définissons une structure nommée `MyBox` et déclarons un paramètre générique `T` car nous voulons que notre type contienne des valeurs de n'importe quel type. Le type `MyBox` est une structure tuple avec un élément de type `T`. La fonction `MyBox::new` prend un paramètre de type `T` et retourne une instance de `MyBox` qui contient la valeur passée en.

Essayons d'ajouter la fonction `main` du Listing 15-7 au Listing 15-8 et de la modifier pour utiliser le type `MyBox<T>` que nous avons défini au lieu de `Box<T>`. Le code dans le Listing 15-9 ne se compilera pas, car Rust ne sait pas comment déréférencer `MyBox`.

<Listing number="15-9" file-name="src/main.rs" caption="Tentative d'utilisation de `MyBox<T>` de la même manière que nous avons utilisé des références et `Box<T>`">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-09/src/main.rs:here}}
```

</Listing>

Voici l'erreur de compilation résultante :

```console
{{#include ../listings/ch15-smart-pointers/listing-15-09/output.txt}}
```

Notre type `MyBox<T>` ne peut pas être déréférencé car nous n'avons pas implémenté cette capacité sur notre type. Pour activer le déréférencement avec l'opérateur `*`, nous implémentons le trait `Deref`.

<!-- Anciens titres. Ne pas supprimer ou les liens peuvent se briser. -->

<a id="traiter-un-type-comme-une-référence-en-implémentant-le-trait-deref"></a>

### Implémenter le Trait `Deref`

Comme discuté dans [« Implémenter un Trait sur un Type »][impl-trait]<!-- ignore --> dans le Chapitre 10, pour implémenter un trait, nous devons fournir des implémentations pour les méthodes requises par le trait. Le trait `Deref`, fourni par la bibliothèque standard, exige que nous implémentions une méthode nommée `deref` qui emprunte `self` et renvoie une référence aux données internes. Le Listing 15-10 contient une implémentation de `Deref` à ajouter à la définition de `MyBox<T>`.

<Listing number="15-10" file-name="src/main.rs" caption="Implémentation de `Deref` sur `MyBox<T>`">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-10/src/main.rs:here}}
```

</Listing>

La syntaxe `type Target = T;` définit un type associé pour que le trait `Deref` puisse l'utiliser. Les types associés sont une manière légèrement différente de déclarer un paramètre générique, mais vous n'avez pas besoin de vous en préoccuper pour l'instant ; nous les couvrirons plus en détail dans le Chapitre 20.

Nous remplissons le corps de la méthode `deref` avec `&self.0` de sorte que `deref` renvoie une référence à la valeur que nous souhaitons accéder avec l'opérateur `*` ; rappelons-nous que [« Créer Différents Types avec des Structures Tuple »][tuple-structs]<!-- ignore --> dans le Chapitre 5 que `.0` accède au premier élément dans une structure tuple. La fonction `main` du Listing 15-9 qui appelle `*` sur la valeur `MyBox<T>` compile maintenant, et les affirmations passent !

Sans le trait `Deref`, le compilateur ne peut déréférencer que les références `&`. La méthode `deref` donne au compilateur la capacité de prendre une valeur de n'importe quel type qui implémente `Deref` et d'appeler la méthode `deref` pour obtenir une référence qu'il sait comment déréférencer.

Lorsque nous avons saisi `*y` dans le Listing 15-9, derrière les coulisses, Rust a en réalité exécuté ce code :

```rust,ignore
*(y.deref())
```

Rust substitue l'opérateur `*` par un appel à la méthode `deref` puis un simple déréférencement afin que nous n'ayons pas à penser à savoir si nous devons appeler la méthode `deref`. Cette fonctionnalité de Rust nous permet d'écrire du code qui fonctionne de manière identique que nous ayons une référence classique ou un type qui implémente `Deref`.

La raison pour laquelle la méthode `deref` renvoie une référence à une valeur, et que le simple déréférencement en dehors des parenthèses dans `*(y.deref())` est toujours nécessaire, est liée au système de propriété. Si la méthode `deref` retournait directement la valeur au lieu d'une référence à la valeur, la valeur serait déplacée de `self`. Nous ne voulons pas prendre possession de la valeur interne à l'intérieur de `MyBox<T>` dans ce cas ou dans la plupart des cas où nous utilisons l'opérateur de déréférencement.

Remarquez que l'opérateur `*` est remplacé par un appel à la méthode `deref` et ensuite un appel à l'opérateur `*` une seule fois, chaque fois que nous utilisons un `*` dans notre code. Comme la substitution de l'opérateur `*` ne regagne pas à l'infini, nous finissons par obtenir des données de type `i32`, ce qui correspond au `5` dans `assert_eq!` dans le Listing 15-9.

<!-- Anciens titres. Ne pas supprimer ou les liens peuvent se briser. -->

<a id="coercions-implicites-deref-avec-fonctions-et-methodes"></a>
<a id="utiliser-les-coercions-deref-dans-les-fonctions-et-methodes"></a>

### Utiliser la Coercition de Déréférencement dans les Fonctions et Méthodes

La _coercition de déréférencement_ convertit une référence à un type qui implémente le trait `Deref` en une référence à un autre type. Par exemple, la coercition de déréférencement peut convertir `&String` en `&str` car `String` implémente le trait `Deref` de sorte qu'il retourne `&str`. La coercition de déréférencement est une commodité que Rust effectue sur les arguments passés à des fonctions et méthodes, et cela ne fonctionne que pour les types qui implémentent le trait `Deref`. Cela se produit automatiquement lorsque nous transmettons une référence à une valeur d'un type particulier comme argument à une fonction ou méthode qui ne correspond pas au type de paramètre dans la définition de la fonction ou méthode. Une séquence d'appels à la méthode `deref` convertit le type que nous avons fourni en le type dont le paramètre a besoin.

La coercition de déréférencement a été ajoutée à Rust afin que les programmeurs qui écrivent des appels de fonction et de méthode n'aient pas besoin d'ajouter autant de références et de déréférences explicites avec `&` et `*`. La fonctionnalité de coercition de déréférencement nous permet également d'écrire plus de code qui peut fonctionner à la fois pour des références ou des pointeurs intelligents.

Pour voir la coercion de déréférencement en action, utilisons le type `MyBox<T>` que nous avons défini dans le Listing 15-8 ainsi que l'implémentation de `Deref` que nous avons ajoutée dans le Listing 15-10. Le Listing 15-11 montre la définition d'une fonction qui a un paramètre de tranche de chaîne.

<Listing number="15-11" file-name="src/main.rs" caption="Une fonction `hello` qui a le paramètre `name` de type `&str`">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-11/src/main.rs:here}}
```

</Listing>

Nous pouvons appeler la fonction `hello` avec une tranche de chaîne comme argument, par exemple `hello("Rust");`. La coercion de déréférencement rend possible d'appeler `hello` avec une référence à une valeur de type `MyBox<String>`, comme montré dans le Listing 15-12.

<Listing number="15-12" file-name="src/main.rs" caption="Appeler `hello` avec une référence à une valeur `MyBox<String>`, ce qui fonctionne grâce à la coercion de déréférencement">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-12/src/main.rs:here}}
```

</Listing>

Ici, nous appelons la fonction `hello` avec l'argument `&m`, qui est une référence à une valeur `MyBox<String>`. Parce que nous avons implémenté le trait `Deref` sur `MyBox<T>` dans le Listing 15-10, Rust peut transformer `&MyBox<String>` en `&String` en appelant `deref`. La bibliothèque standard fournit une implémentation de `Deref` sur `String` qui renvoie une tranche de chaîne, et cela se trouve dans la documentation API de `Deref`. Rust appelle `deref` à nouveau pour transformer le `&String` en `&str`, ce qui correspond à la définition de la fonction `hello`.

Si Rust n'avait pas implémenté la coercion de déréférencement, nous aurions dû écrire le code du Listing 15-13 au lieu du code du Listing 15-12 pour appeler `hello` avec une valeur de type `&MyBox<String>`.

<Listing number="15-13" file-name="src/main.rs" caption="Le code que nous devrions écrire si Rust n’avait pas de coercion de déréférencement">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-13/src/main.rs:here}}
```

</Listing>

Le `(*m)` déréférence le `MyBox<String>` en un `String`. Ensuite, le `&` et `[..]` prennent une tranche de chaîne du `String` qui est égale à la chaîne complète pour correspondre à la signature de `hello`. Ce code sans coercions de déréférencement est plus difficile à lire, écrire et comprendre avec tous ces symboles impliqués. La coercion de déréférencement permet à Rust de gérer ces conversions automatiquement pour nous.

Lorsque le trait `Deref` est défini pour les types impliqués, Rust analysera les types et utilisera `Deref::deref` autant de fois que nécessaire pour obtenir une référence qui correspond au type du paramètre. Le nombre de fois où `Deref::deref` doit être inséré est résolu à la compilation, donc il n'y a pas de pénalité en temps d'exécution pour tirer parti de la coercion de déréférencement !

<!-- Anciens titres. Ne pas supprimer ou les liens peuvent se briser. -->

<a id="comment-la-coercition-deref-interagit-avec-la-mutabilité"></a>

### Gérer la Coercition de Déréférencement avec des Références Mutables

Tout comme vous utilisez le trait `Deref` pour remplacer l'opérateur `*` sur les références immuables, vous pouvez utiliser le trait `DerefMut` pour remplacer l'opérateur `*` sur les références mutables.

Rust effectue la coercion de déréférencement lorsqu'il trouve des types et des implémentations de traits dans trois cas :

1. De `&T` à `&U` lorsque `T : Deref<Target=U>`
2. De `&mut T` à `&mut U` lorsque `T : DerefMut<Target=U>`
3. De `&mut T` à `&U` lorsque `T : Deref<Target=U>`

Le premier et le deuxième cas sont les mêmes sauf que le second implémente la mutabilité. Le premier cas stipule que si vous avez un `&T`, et que `T` implémente `Deref` vers un certain type `U`, vous pouvez obtenir un `&U` de manière transparente. Le second cas stipule que la même coercion de déréférencement se produit pour des références mutables.

Le troisième cas est plus délicat : Rust peut également coercer une référence mutable en une référence immuable. Mais l'inverse n'est _pas_ possible : les références immuables ne seront jamais coercées en références mutables. En raison des règles d'emprunt, si vous avez une référence mutable, cette référence mutable doit être la seule référence à ces données (sinon, le programme ne compilerait pas). Convertir une référence mutable en une référence immuable ne violera jamais les règles d'emprunt. En revanche, convertir une référence immuable en une référence mutable nécessiterait que la référence immuable initiale soit la seule référence immuable à ces données, mais les règles d'emprunt ne garantissent pas cela. Par conséquent, Rust ne peut pas faire l'hypothèse que la conversion d'une référence immuable en une référence mutable est possible.

[impl-trait]: ch10-02-traits.html#implementing-a-trait-on-a-type
[tuple-structs]: ch05-01-defining-structs.html#creating-different-types-with-tuple-structs