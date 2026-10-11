## Erreurs récupérables avec `Result`

La plupart des erreurs ne sont pas suffisamment graves pour nécessiter l’arrêt complet du programme.
Parfois, lorsqu’une fonction échoue, c’est pour une raison que vous pouvez facilement interpréter
et à laquelle vous pouvez réagir. Par exemple, si vous essayez d’ouvrir un fichier et que cette opération échoue
parce que le fichier n’existe pas, vous pourriez vouloir créer le fichier plutôt que
de terminer le processus.

Rappelez-vous que, dans [« Gérer les échecs potentiels avec `Result` »][handle_failure]<!--
ignore --> au chapitre 2, nous avons vu que l’énumération `Result` est définie avec deux
variantes, `Ok` et `Err`, comme suit :

```rust
enum Result<T, E> {
    Ok(T),
    Err(E),
}
```

`T` et `E` sont des paramètres de type génériques : nous parlerons des génériques plus en
détail au chapitre 10. Pour l’instant, il suffit de savoir que `T` représente
le type de la valeur renvoyée en cas de réussite dans la variante `Ok`, et que `E`
représente le type de l’erreur renvoyée en cas d’échec dans la variante `Err`. Comme `Result` possède ces paramètres de type
génériques, nous pouvons utiliser le type `Result` et les fonctions qui lui sont associées
dans de nombreuses situations où les valeurs de réussite et d’erreur que nous voulons
renvoyer peuvent différer.

Appelons une fonction qui renvoie une valeur `Result` parce qu’elle peut échouer. Dans le Listing 9-3, nous essayons d’ouvrir un fichier.

<Listing number="9-3" file-name="src/main.rs" caption="Ouvrir un fichier">

```rust
{{#rustdoc_include ../listings/ch09-error-handling/listing-09-03/src/main.rs}}
```

</Listing>

Le type de retour de `File::open` est `Result<T, E>`. Le paramètre générique `T`
a été remplacé par l’implémentation de `File::open` par le type de la
valeur de réussite, `std::fs::File`, qui est un descripteur de fichier. Le type de `E` utilisé pour
la valeur d’erreur est `std::io::Error`. Ce type de retour signifie que l’appel à
`File::open` peut réussir et renvoyer un descripteur de fichier depuis lequel nous pouvons lire ou
dans lequel nous pouvons écrire. L’appel de fonction peut aussi échouer : par exemple, le fichier peut ne
pas exister, ou nous ne sommes peut-être pas autorisés à y accéder. La fonction `File::open`
doit pouvoir nous indiquer si elle a réussi ou échoué tout en nous fournissant le descripteur de fichier ou les informations d’erreur. C’est précisément ce que transmet l’énumération `Result`.

Si `File::open` réussit, la valeur de la variable
`greeting_file_result` sera une instance de `Ok` contenant un descripteur de fichier.
En cas d’échec, la valeur de `greeting_file_result` sera une instance de `Err` contenant davantage d’informations sur le type d’erreur survenue.

Nous devons compléter le code du Listing 9-3 pour effectuer différentes actions selon
la valeur renvoyée par `File::open`. Le Listing 9-4 présente une façon de gérer
`Result` à l’aide d’un outil de base : l’expression `match`, dont nous avons parlé au
chapitre 6.

<Listing number="9-4" file-name="src/main.rs" caption="Utiliser une expression `match` pour gérer les variantes `Result` susceptibles d’être renvoyées">

```rust,should_panic
{{#rustdoc_include ../listings/ch09-error-handling/listing-09-04/src/main.rs}}
```

</Listing>

Notez que, comme l’énumération `Option`, l’énumération `Result` et ses variantes ont été
introduites dans la portée par le prélude ; nous n’avons donc pas besoin de préciser `Result::`
avant les variantes `Ok` et `Err` dans les branches de `match`.

Lorsque le résultat est `Ok`, ce code renvoie la valeur interne `file` de la variante `Ok`, puis nous affectons cette valeur de descripteur de fichier à la variable
`greeting_file`. Après l’expression `match`, nous pouvons utiliser le descripteur de fichier pour lire ou écrire.

L’autre branche de `match` gère le cas où nous obtenons une valeur `Err` de
`File::open`. Dans cet exemple, nous avons choisi d’appeler la macro `panic!`. S’il n’y a pas de fichier nommé _hello.txt_ dans le répertoire courant et que nous exécutons ce code, nous verrons la sortie suivante de la macro `panic!` :

```console
{{#include ../listings/ch09-error-handling/listing-09-04/output.txt}}
```

Comme d’habitude, cette sortie nous indique exactement ce qui s’est mal passé.

### Gérer différents types d’erreurs

Le code du Listing 9-4 appelle `panic!` quelle que soit la raison de l’échec de `File::open`.
Cependant, nous voulons effectuer différentes actions selon la raison de l’échec. Si
`File::open` a échoué parce que le fichier n’existe pas, nous voulons créer le fichier
et renvoyer le descripteur du nouveau fichier. Si `File::open` a échoué pour une autre raison, par exemple parce que nous n’avions pas l’autorisation d’ouvrir le fichier, nous voulons toujours que le code appelle `panic!` de la même façon que dans le Listing 9-4. Pour cela, nous ajoutons une expression `match` imbriquée, présentée dans le Listing 9-5.

<Listing number="9-5" file-name="src/main.rs" caption="Gérer différemment différents types d’erreurs">

<!-- ignore this test because otherwise it creates hello.txt which causes other
tests to fail lol -->

```rust,ignore
{{#rustdoc_include ../listings/ch09-error-handling/listing-09-05/src/main.rs}}
```

</Listing>

Le type de la valeur renvoyée par `File::open` dans la variante `Err` est
`io::Error`, une structure fournie par la bibliothèque standard. Cette structure
possède une méthode, `kind`, que nous pouvons appeler pour obtenir une valeur `io::ErrorKind`. L’énumération `io::ErrorKind` est fournie par la bibliothèque standard et possède des variantes représentant les différents types d’erreurs susceptibles de résulter d’une opération d’`io`. La variante que nous voulons utiliser est `ErrorKind::NotFound`, qui indique que le fichier que nous essayons d’ouvrir n’existe pas encore. Nous utilisons donc une expression `match` sur
`greeting_file_result`, mais aussi une expression `match` imbriquée sur `error.kind()`.

La condition que nous voulons vérifier dans l’expression `match` imbriquée est de savoir si la valeur renvoyée par `error.kind()` est la variante `NotFound` de l’énumération `ErrorKind`. Si c’est le cas,
nous essayons de créer le fichier avec `File::create`. Toutefois, comme `File::create` peut aussi échouer, nous avons besoin d’une deuxième branche dans l’expression `match` imbriquée. Lorsque le fichier ne peut pas être créé, un message d’erreur différent s’affiche. La deuxième branche de l’expression `match` externe reste inchangée ; le programme panique donc pour toute erreur autre que l’absence du fichier.

> #### Alternatives à l’utilisation de `match` avec `Result<T, E>`
>
> Ça fait beaucoup d’expressions `match` ! L’expression `match` est très utile, mais aussi très
> élémentaire. Au chapitre 13, vous découvrirez les fermetures, qui sont utilisées
> avec de nombreuses méthodes définies sur `Result<T, E>`. Ces méthodes peuvent être plus
> concises que l’utilisation de `match` pour gérer les valeurs `Result<T, E>` dans votre code.
>
> Par exemple, voici une autre façon d’écrire la même logique que dans le Listing
> 9-5, cette fois en utilisant des fermetures et la méthode `unwrap_or_else` :
>
> <!-- CAN'T EXTRACT SEE https://github.com/rust-lang/mdBook/issues/1127 -->
>
> ```rust,ignore
> use std::fs::File;
> use std::io::ErrorKind;
>
> fn main() {
>     let greeting_file = File::open("hello.txt").unwrap_or_else(|error| {
>         if error.kind() == ErrorKind::NotFound {
>             File::create("hello.txt").unwrap_or_else(|error| {
>                 panic!("Problem creating the file: {error:?}");
>             })
>         } else {
>             panic!("Problem opening the file: {error:?}");
>         }
>     });
> }
> ```
>
> Bien que ce code ait le même comportement que celui du Listing 9-5, il ne contient
> aucune expression `match` et est plus facile à lire. Revenez à cet exemple
> après avoir lu le chapitre 13 et consultez la méthode `unwrap_or_else` dans la
> documentation de la bibliothèque standard. De nombreuses autres méthodes de ce type permettent d’alléger les expressions `match` imbriquées et volumineuses utilisées lors de la gestion des erreurs.

<!-- Old headings. Do not remove or links may break. -->

<a id="shortcuts-for-panic-on-error-unwrap-and-expect"></a>

#### Raccourcis pour paniquer en cas d’erreur

L’utilisation de `match` fonctionne suffisamment bien, mais elle peut être un peu verbeuse et ne communique pas toujours clairement l’intention. Le type `Result<T, E>` possède de nombreuses méthodes utilitaires définies pour effectuer diverses tâches plus spécifiques. La méthode `unwrap` est un raccourci implémenté exactement comme l’expression `match` que nous avons écrite dans le Listing 9-4. Si la valeur `Result` est la variante `Ok`, `unwrap` renvoie la valeur contenue dans `Ok`. Si `Result` est la variante `Err`, `unwrap` appelle la macro `panic!` à notre place. Voici un exemple d’utilisation de `unwrap` :

<Listing file-name="src/main.rs">

```rust,should_panic
{{#rustdoc_include ../listings/ch09-error-handling/no-listing-04-unwrap/src/main.rs}}
```

</Listing>

Si nous exécutons ce code sans fichier _hello.txt_, nous verrons un message d’erreur provenant de l’appel à `panic!` effectué par la méthode `unwrap` :

<!-- manual-regeneration
cd listings/ch09-error-handling/no-listing-04-unwrap
cargo run
copy and paste relevant text
-->

```text
thread 'main' panicked at src/main.rs:4:49:
called `Result::unwrap()` on an `Err` value: Os { code: 2, kind: NotFound, message: "No such file or directory" }
```

De même, la méthode `expect` nous permet également de choisir le message d’erreur de `panic!`. Utiliser `expect` plutôt que `unwrap` et fournir de bons messages d’erreur peut communiquer votre intention et faciliter la recherche de l’origine d’une panique. La syntaxe de `expect` est la suivante :

<Listing file-name="src/main.rs">

```rust,should_panic
{{#rustdoc_include ../listings/ch09-error-handling/no-listing-05-expect/src/main.rs}}
```

</Listing>

Nous utilisons `expect` de la même manière que `unwrap` : pour renvoyer le descripteur de fichier ou appeler la macro `panic!`. Le message d’erreur utilisé par `expect` dans son appel à `panic!` est le paramètre que nous transmettons à `expect`, plutôt que le message par défaut de `panic!` utilisé par `unwrap`. Voici ce que cela donne :

<!-- manual-regeneration
cd listings/ch09-error-handling/no-listing-05-expect
cargo run
copy and paste relevant text
-->

```text
thread 'main' panicked at src/main.rs:5:10:
hello.txt should be included in this project: Os { code: 2, kind: NotFound, message: "No such file or directory" }
```

Dans du code de qualité production, la plupart des Rustacéens préfèrent `expect` à
`unwrap` et donnent davantage de contexte sur les raisons pour lesquelles l’opération est censée toujours réussir. Ainsi, si vos hypothèses se révèlent un jour erronées, vous disposez de plus d’informations pour déboguer.

### Propager les erreurs

Lorsqu’une implémentation de fonction appelle quelque chose qui peut échouer, au lieu de
gérer l’erreur au sein même de la fonction, vous pouvez renvoyer l’erreur au code appelant afin qu’il puisse décider quoi faire. On appelle cela _propager_
l’erreur. Cela donne davantage de contrôle au code appelant, qui dispose peut-être de plus
d’informations ou d’une logique permettant de déterminer comment l’erreur doit être gérée que ce qui est disponible dans le contexte de votre code.

Par exemple, le Listing 9-6 montre une fonction qui lit un nom d’utilisateur depuis un fichier. Si
le fichier n’existe pas ou ne peut pas être lu, cette fonction renverra ces erreurs au code qui l’a appelée.

<Listing number="9-6" file-name="src/main.rs" caption="Une fonction qui renvoie les erreurs au code appelant à l’aide de `match`">

<!-- Deliberately not using rustdoc_include here; the `main` function in the
file panics. We do want to include it for reader experimentation purposes, but
don't want to include it for rustdoc testing purposes. -->

```rust
{{#include ../listings/ch09-error-handling/listing-09-06/src/main.rs:here}}
```

</Listing>

Cette fonction peut s’écrire de façon bien plus concise, mais nous allons commencer par écrire beaucoup de choses manuellement afin d’explorer la gestion des erreurs ; à la fin,
nous présenterons la version plus courte. Commençons par examiner le type de retour de la fonction :
`Result<String, io::Error>`. Cela signifie que la fonction renvoie une
valeur de type `Result<T, E>`, où le paramètre générique `T` a été remplacé par le type concret `String` et le type générique `E` par le type concret `io::Error`.

Si cette fonction réussit sans problème, le code qui l’appelle recevra une valeur `Ok` contenant une `String` : le `username` que cette fonction a lu dans le fichier. Si cette fonction rencontre un problème, le code appelant recevra une valeur `Err` contenant une instance de `io::Error`, qui fournit davantage d’informations sur la nature du problème. Nous avons choisi `io::Error` comme type de retour de cette fonction parce que c’est le type de la valeur d’erreur renvoyée par les deux opérations appelées dans le corps de cette fonction et susceptibles d’échouer : la fonction `File::open` et la méthode `read_to_string`.

Le corps de la fonction commence par appeler la fonction `File::open`. Nous gérons ensuite la valeur `Result` avec une expression `match` similaire à celle du Listing 9-4.
Si `File::open` réussit, le descripteur de fichier de la variable de motif `file`
devient la valeur de la variable mutable `username_file`, et la fonction continue. Dans le cas `Err`, au lieu d’appeler `panic!`, nous utilisons le mot-clé `return` pour quitter immédiatement la fonction et transmettre au code appelant la valeur d’erreur de `File::open`, désormais dans la variable de motif `e`, comme valeur d’erreur de cette fonction.

Ainsi, si `username_file` contient un descripteur de fichier, la fonction crée ensuite une nouvelle `String` dans la variable `username` et appelle la méthode `read_to_string` sur le descripteur de fichier contenu dans `username_file` pour lire le contenu du fichier dans `username`. La méthode `read_to_string` renvoie également un `Result`, car elle peut échouer, même si `File::open` a réussi. Nous avons donc besoin d’une autre expression `match` pour gérer ce `Result` : si `read_to_string` réussit, notre fonction a réussi et nous renvoyons le nom d’utilisateur lu dans le fichier, maintenant contenu dans `username`, enveloppé dans un `Ok`. Si `read_to_string` échoue, nous renvoyons la valeur d’erreur de la même façon que nous avons renvoyé la valeur d’erreur dans l’expression `match` qui gérait la valeur de retour de `File::open`. Toutefois, nous n’avons pas besoin d’écrire explicitement `return`, car il s’agit de la dernière expression de la fonction.

Le code qui appelle cette fonction gérera ensuite l’obtention d’une valeur `Ok` contenant un nom d’utilisateur ou d’une valeur `Err` contenant une `io::Error`. C’est au code appelant de décider quoi faire de ces valeurs. S’il reçoit une valeur `Err`, il peut appeler `panic!` et faire planter le programme, utiliser un nom d’utilisateur par défaut ou, par exemple, rechercher le nom d’utilisateur ailleurs que dans un fichier. Nous ne disposons pas d’assez d’informations sur ce que le code appelant cherche réellement à faire ; nous propageons donc toutes les informations de réussite ou d’erreur afin qu’il puisse les traiter comme il convient.

Ce modèle de propagation des erreurs est si courant en Rust que le langage fournit l’opérateur point d’interrogation `?` pour simplifier cette opération.

<!-- Old headings. Do not remove or links may break. -->

<a id="a-shortcut-for-propagating-errors-the--operator"></a>

#### L’opérateur `?`, un raccourci pour propager les erreurs

Le Listing 9-7 montre une implémentation de `read_username_from_file` qui offre les mêmes fonctionnalités que celle du Listing 9-6, mais qui utilise l’opérateur `?`.

<Listing number="9-7" file-name="src/main.rs" caption="Une fonction qui renvoie les erreurs au code appelant à l’aide de l’opérateur `?`">

<!-- Deliberately not using rustdoc_include here; the `main` function in the
file panics. We do want to include it for reader experimentation purposes, but
don't want to include it for rustdoc testing purposes. -->

```rust
{{#include ../listings/ch09-error-handling/listing-09-07/src/main.rs:here}}
```

</Listing>

L’opérateur `?` placé après une valeur `Result` est défini pour fonctionner presque de la même manière que les expressions `match` que nous avons écrites pour gérer les valeurs `Result` dans le Listing 9-6. Si la valeur de `Result` est un `Ok`, la valeur contenue dans `Ok` est renvoyée par cette expression, et le programme continue. Si la valeur est un `Err`, le `Err` est renvoyé par la fonction entière, comme si nous avions utilisé le mot-clé `return`, de sorte que la valeur d’erreur est propagée au code appelant.

Il existe une différence entre le comportement de l’expression `match` du Listing 9-6 et celui de l’opérateur `?` : les valeurs d’erreur sur lesquelles l’opérateur `?` est appliqué passent par la fonction `from`, définie dans le trait `From` de la bibliothèque standard, qui sert à convertir des valeurs d’un type à un autre.
Lorsque l’opérateur `?` appelle la fonction `from`, le type de l’erreur reçue est converti en type d’erreur défini dans le type de retour de la fonction courante. Cela est utile lorsqu’une fonction renvoie un seul type d’erreur pour représenter toutes les façons dont elle peut échouer, même si certaines parties peuvent échouer pour de nombreuses raisons différentes.

Par exemple, nous pourrions modifier la fonction `read_username_from_file` du Listing
9-7 pour qu’elle renvoie un type d’erreur personnalisé nommé `OurError`, que nous définirions. Si nous définissons également `impl From<io::Error> for OurError` pour construire une instance de `OurError` à partir d’une `io::Error`, les appels à l’opérateur `?` dans le corps de `read_username_from_file` appelleront `from` et convertiront les types d’erreur sans qu’il soit nécessaire d’ajouter du code à la fonction.

Dans le contexte du Listing 9-7, le `?` à la fin de l’appel à `File::open` renverra la valeur contenue dans un `Ok` à la variable `username_file`. Si une erreur se produit, l’opérateur `?` quittera immédiatement la fonction entière et transmettra toute valeur `Err` au code appelant. Il en va de même pour le `?` à la fin de l’appel à `read_to_string`.

L’opérateur `?` élimine beaucoup de code répétitif et simplifie l’implémentation de cette fonction. Nous pourrions même raccourcir encore ce code en enchaînant les appels de méthode immédiatement après le `?`, comme le montre le Listing 9-8.

<Listing number="9-8" file-name="src/main.rs" caption="Enchaîner des appels de méthode après l’opérateur `?`">

<!-- Deliberately not using rustdoc_include here; the `main` function in the
file panics. We do want to include it for reader experimentation purposes, but
don't want to include it for rustdoc testing purposes. -->

```rust
{{#include ../listings/ch09-error-handling/listing-09-08/src/main.rs:here}}
```

</Listing>

Nous avons déplacé la création de la nouvelle `String` dans `username` au début de la fonction ; cette partie n’a pas changé. Au lieu de créer une variable `username_file`, nous avons enchaîné l’appel à `read_to_string` directement sur le résultat de `File::open("hello.txt")?`. Nous avons toujours un `?` à la fin de l’appel à `read_to_string`, et nous renvoyons toujours une valeur `Ok` contenant `username` lorsque `File::open` et `read_to_string` réussissent, plutôt que de renvoyer des erreurs. Le comportement est toujours identique à celui des Listings 9-6 et 9-7 ; seule la manière de l’écrire est différente et plus ergonomique.

Le Listing 9-9 montre comment raccourcir encore ce code à l’aide de `fs::read_to_string`.

<Listing number="9-9" file-name="src/main.rs" caption="Utiliser `fs::read_to_string` plutôt que d’ouvrir puis de lire le fichier">

<!-- Deliberately not using rustdoc_include here; the `main` function in the
file panics. We do want to include it for reader experimentation purposes, but
don't want to include it for rustdoc testing purposes. -->

```rust
{{#include ../listings/ch09-error-handling/listing-09-09/src/main.rs:here}}
```

</Listing>

Lire un fichier dans une chaîne est une opération assez courante, c’est pourquoi la bibliothèque standard fournit la fonction pratique `fs::read_to_string`, qui ouvre le fichier, crée une nouvelle `String`, lit le contenu du fichier, place ce contenu dans cette `String` et la renvoie. Bien sûr, utiliser `fs::read_to_string` ne nous permettrait pas d’expliquer toute la gestion des erreurs ; nous avons donc commencé par la méthode plus longue.

<!-- Old headings. Do not remove or links may break. -->

<a id="where-the--operator-can-be-used"></a>

#### Où utiliser l’opérateur `?`

L’opérateur `?` ne peut être utilisé que dans les fonctions dont le type de retour est compatible avec la valeur sur laquelle il est appliqué. En effet, l’opérateur `?` est défini pour effectuer un retour anticipé d’une valeur hors de la fonction, de la même manière que l’expression `match` que nous avons définie dans le Listing 9-6. Dans le Listing 9-6, l’expression `match` utilisait une valeur `Result`, et la branche de retour anticipé renvoyait une valeur `Err(e)`. Le type de retour de la fonction doit donc être un `Result` pour être compatible avec ce `return`.

Dans le Listing 9-10, examinons l’erreur obtenue si nous utilisons l’opérateur `?` dans une fonction `main` dont le type de retour est incompatible avec le type de la valeur sur laquelle nous l’appliquons.

<Listing number="9-10" file-name="src/main.rs" caption="Tenter d’utiliser `?` dans la fonction `main`, qui renvoie `()`, ne compile pas.">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch09-error-handling/listing-09-10/src/main.rs}}
```

</Listing>

Ce code ouvre un fichier, ce qui peut échouer. L’opérateur `?` suit la valeur `Result` renvoyée par `File::open`, mais cette fonction `main` a le type de retour `()`, et non `Result`. Lorsque nous compilons ce code, nous obtenons le message d’erreur suivant :

```console
{{#include ../listings/ch09-error-handling/listing-09-10/output.txt}}
```

Cette erreur indique que nous ne pouvons utiliser l’opérateur `?` que dans une fonction qui renvoie `Result`, `Option` ou un autre type qui implémente `FromResidual`.

Pour corriger l’erreur, vous avez deux possibilités. La première consiste à modifier le type de retour de votre fonction pour qu’il soit compatible avec la valeur sur laquelle vous utilisez l’opérateur `?`, à condition qu’aucune contrainte ne vous en empêche. L’autre possibilité consiste à utiliser une expression `match` ou l’une des méthodes de `Result<T, E>` pour gérer `Result<T, E>` de la manière appropriée.

Le message d’erreur indique également que `?` peut être utilisé avec des valeurs `Option<T>`. Comme pour `Result`, vous ne pouvez utiliser `?` sur `Option` que dans une fonction qui renvoie un `Option`. Le comportement de l’opérateur `?` lorsqu’il est appliqué à un `Option<T>` est semblable à celui qu’il a lorsqu’il est appliqué à un `Result<T, E>` : si la valeur est `None`, `None` est renvoyé immédiatement par la fonction à cet endroit. Si la valeur est `Some`, la valeur contenue dans `Some` devient le résultat de l’expression, et la fonction continue. Le Listing 9-11 présente un exemple de fonction qui trouve le dernier caractère de la première ligne du texte donné.

<Listing number="9-11" caption="Utiliser l’opérateur `?` sur une valeur `Option<T>`">

```rust
{{#rustdoc_include ../listings/ch09-error-handling/listing-09-11/src/main.rs:here}}
```

</Listing>

Cette fonction renvoie `Option<char>` parce qu’il est possible qu’un caractère se trouve à cet endroit, mais aussi qu’il n’y en ait pas. Ce code prend l’argument de tranche de chaîne `text` et appelle sa méthode `lines`, qui renvoie un itérateur sur les lignes de la chaîne. Comme cette fonction veut examiner la première ligne, elle appelle `next` sur l’itérateur pour en obtenir la première valeur. Si `text` est une chaîne vide, cet appel à `next` renverra `None` ; nous utilisons alors `?` pour arrêter la fonction et renvoyer `None` depuis `last_char_of_first_line`. Si `text` n’est pas une chaîne vide, `next` renverra une valeur `Some` contenant une tranche de chaîne correspondant à la première ligne de `text`.

`?` extrait la tranche de chaîne, et nous pouvons appeler `chars` sur celle-ci pour obtenir un itérateur sur ses caractères. Nous nous intéressons au dernier caractère de cette première ligne ; nous appelons donc `last` pour renvoyer le dernier élément de l’itérateur. Il s’agit d’un `Option`, car la première ligne peut être une chaîne vide, par exemple si `text` commence par une ligne vide mais contient des caractères sur les lignes suivantes, comme dans `"\nhi"`. Toutefois, si la première ligne contient un dernier caractère, celui-ci sera renvoyé dans la variante `Some`. L’opérateur `?` au milieu de l’expression permet d’exprimer cette logique de manière concise et de définir la fonction sur une seule ligne. Si nous ne pouvions pas utiliser l’opérateur `?` sur `Option`, nous devrions implémenter cette logique à l’aide de davantage d’appels de méthode ou d’une expression `match`.

Notez que vous pouvez utiliser l’opérateur `?` sur un `Result` dans une fonction qui renvoie un `Result`, et sur un `Option` dans une fonction qui renvoie un `Option`, mais vous ne pouvez pas mélanger les deux. L’opérateur `?` ne convertit pas automatiquement un `Result` en `Option`, ni l’inverse ; dans ces cas, vous pouvez utiliser des méthodes comme `ok` sur `Result` ou `ok_or` sur `Option` pour effectuer explicitement la conversion.

Jusqu’à présent, toutes les fonctions `main` que nous avons utilisées renvoyaient `()`. La fonction `main` est particulière, car elle constitue le point d’entrée et de sortie d’un programme exécutable, et son type de retour est soumis à des restrictions pour que le programme se comporte comme prévu.

Heureusement, `main` peut aussi renvoyer un `Result<(), E>`. Le Listing 9-12 reprend le code du Listing 9-10, mais nous avons modifié le type de retour de `main` en `Result<(), Box<dyn Error>>` et ajouté une valeur de retour `Ok(())` à la fin. Ce code compile désormais.

<Listing number="9-12" file-name="src/main.rs" caption="Modifier `main` pour qu’elle renvoie `Result<(), E>` permet d’utiliser l’opérateur `?` sur des valeurs `Result`.">

```rust,ignore
{{#rustdoc_include ../listings/ch09-error-handling/listing-09-12/src/main.rs}}
```

</Listing>

Le type `Box<dyn Error>` est un objet trait, dont nous parlerons dans [« Utiliser des objets trait pour abstraire un comportement partagé »][trait-objects]<!-- ignore -->
au chapitre 18. Pour l’instant, vous pouvez comprendre `Box<dyn Error>` comme « n’importe quel type d’erreur ». Utiliser `?` sur une valeur `Result` dans une fonction `main` dont le type d’erreur est `Box<dyn Error>` est autorisé, car cela permet de renvoyer immédiatement n’importe quelle valeur `Err`. Même si le corps de cette fonction `main` ne renvoie que des erreurs de type `std::io::Error`, en spécifiant `Box<dyn Error>`, cette signature restera correcte si du code renvoyant d’autres erreurs est ajouté au corps de `main`.

Lorsqu’une fonction `main` renvoie un `Result<(), E>`, l’exécutable se termine avec la valeur `0` si `main` renvoie `Ok(())`, et avec une valeur différente de zéro si `main` renvoie une valeur `Err`. Les exécutables écrits en C renvoient des entiers à leur terminaison : les programmes qui se terminent correctement renvoient l’entier `0`, et ceux qui échouent renvoient un entier différent de `0`. Rust renvoie également des entiers à la terminaison des exécutables afin de respecter cette convention.

La fonction `main` peut renvoyer n’importe quel type qui implémente [le trait `std::process::Termination`][termination]<!-- ignore -->, qui contient une fonction `report` renvoyant un `ExitCode`. Consultez la documentation de la bibliothèque standard pour en savoir davantage sur l’implémentation du trait `Termination` pour vos propres types.

Maintenant que nous avons examiné en détail les appels à `panic!` et le renvoi de `Result`, revenons à la question de savoir comment choisir la solution appropriée selon les cas.

[handle_failure]: ch02-00-guessing-game-tutorial.html#handling-potential-failure-with-result
[trait-objects]: ch18-02-trait-objects.html#using-trait-objects-to-abstract-over-shared-behavior
[termination]: ../std/process/trait.Termination.html