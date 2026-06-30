## Erreurs récupérables avec `Result`

La plupart des erreurs ne sont pas assez graves pour nécessiter l'arrêt total du programme. Parfois, lorsqu'une fonction échoue, c'est pour une raison que vous pouvez facilement interpréter et à laquelle vous pouvez répondre. Par exemple, si vous essayez d'ouvrir un fichier et que cette opération échoue parce que le fichier n'existe pas, vous pourriez vouloir créer le fichier au lieu de terminer le processus.

Rappelez-vous de la section [« Gestion des échecs potentiels avec `Result` »](handle_failure) dans le Chapitre 2, où l'énumération `Result` est définie comme ayant deux variantes, `Ok` et `Err`, comme suit :

```rust
enum Result<T, E> {
    Ok(T),
    Err(E),
}
```

`T` et `E` sont des paramètres de type génériques : nous discuterons des génériques plus en détail dans le Chapitre 10. Ce que vous devez savoir maintenant, c'est que `T` représente le type de la valeur qui sera retournée en cas de succès dans la variante `Ok`, et `E` représente le type de l'erreur qui sera retournée en cas d'échec dans la variante `Err`. Parce que `Result` a ces paramètres de type génériques, nous pouvons utiliser le type `Result` et les fonctions qui y sont définies dans de nombreuses situations différentes où la valeur de succès et la valeur d'erreur que nous voulons retourner peuvent différer.

Appelons une fonction qui retourne une valeur `Result` parce que la fonction pourrait échouer. Dans la Liste 9-3, nous essayons d'ouvrir un fichier.

<Listing number="9-3" file-name="src/main.rs" caption="Ouverture d'un fichier">

```rust
{{#rustdoc_include ../listings/ch09-error-handling/listing-09-03/src/main.rs}}
```

</Listing>

Le type de retour de `File::open` est un `Result<T, E>`. Le paramètre générique `T` a été rempli par l'implémentation de `File::open` avec le type de la valeur de succès, `std::fs::File`, qui est un handle de fichier. Le type de `E` utilisé dans la valeur d'erreur est `std::io::Error`. Ce type de retour signifie que l'appel à `File::open` pourrait réussir et retourner un handle de fichier que nous pouvons lire ou écrire. L'appel de fonction pourrait également échouer : par exemple, le fichier pourrait ne pas exister, ou nous pourrions ne pas avoir la permission d'accéder au fichier. La fonction `File::open` doit avoir un moyen de nous dire si elle a réussi ou échoué tout en nous donnant soit le handle de fichier, soit des informations sur l'erreur. Ces informations sont exactement ce que l'énumération `Result` transmet.

Dans le cas où `File::open` réussit, la valeur dans la variable `greeting_file_result` sera une instance d'`Ok` contenant un handle de fichier. Dans le cas où elle échoue, la valeur dans `greeting_file_result` sera une instance d'`Err` contenant plus d'informations sur le type d'erreur qui s'est produite.

Nous devons ajouter au code dans la Liste 9-3 pour prendre différentes actions selon la valeur que retourne `File::open`. La Liste 9-4 montre une manière de gérer le `Result` en utilisant un outil de base, l'expression `match` que nous avons discutée dans le Chapitre 6.

<Listing number="9-4" file-name="src/main.rs" caption="Utilisation d'une expression `match` pour gérer les variantes `Result` qui pourraient être retournées">

```rust,should_panic
{{#rustdoc_include ../listings/ch09-error-handling/listing-09-04/src/main.rs}}
```

</Listing>

Notez que, comme l'énumération `Option`, l'énumération `Result` et ses variantes ont été mises en portée par le préambule, donc nous n'avons pas besoin de préciser `Result::` avant les variantes `Ok` et `Err` dans les bras du `match`.

Lorsque le résultat est `Ok`, ce code retournera la valeur interne `file` de la variante `Ok`, et nous assignons ensuite cette valeur de handle de fichier à la variable `greeting_file`. Après le `match`, nous pouvons utiliser le handle de fichier pour lire ou écrire.

L'autre bras du `match` gère le cas où nous obtenons une valeur `Err` de `File::open`. Dans cet exemple, nous avons choisi d'appeler la macro `panic!`. Si aucun fichier nommé _hello.txt_ n'est présent dans notre répertoire actuel et que nous exécutons ce code, nous verrons la sortie suivante de la macro `panic!` :

```console
{{#include ../listings/ch09-error-handling/listing-09-04/output.txt}}
```

Comme d'habitude, cette sortie nous indique exactement ce qui s'est mal passé.

### Correspondance sur différentes erreurs

Le code dans la Liste 9-4 `panic!` peu importe pourquoi `File::open` a échoué. Cependant, nous voulons prendre des actions différentes pour des raisons d'échec différentes. Si `File::open` a échoué parce que le fichier n'existe pas, nous voulons créer le fichier et retourner le handle au nouveau fichier. Si `File::open` échoue pour une autre raison — par exemple, parce que nous n'avions pas la permission d'ouvrir le fichier — nous voulons aussi que le code `panic!` de la même manière qu'il l'a fait dans la Liste 9-4. Pour cela, nous ajoutons une expression `match` interne, montrée dans la Liste 9-5.

<Listing number="9-5" file-name="src/main.rs" caption="Gestion des différents types d'erreurs de différentes manières">

```rust,ignore
{{#rustdoc_include ../listings/ch09-error-handling/listing-09-05/src/main.rs}}
```

</Listing>

Le type de la valeur que retourne `File::open` à l'intérieur de la variante `Err` est `io::Error`, qui est une struct fournie par la bibliothèque стандарт. Cette struct a une méthode, `kind`, que nous pouvons appeler pour obtenir une valeur `io::ErrorKind`. L'énumération `io::ErrorKind` est fournie par la bibliothèque standard et contient des variantes représentant les différents genres d'erreurs qui peuvent résulter d'une opération `io`. La variante que nous voulons utiliser est `ErrorKind::NotFound`, qui indique que le fichier que nous essayons d'ouvrir n'existe pas encore. Donc, nous faisons une correspondance sur `greeting_file_result`, mais nous avons également une correspondance interne sur `error.kind()`.

La condition que nous voulons vérifier dans le `match` interne est de savoir si la valeur retournée par `error.kind()` est la variante `NotFound` de l'énumération `ErrorKind`. Si c'est le cas, nous essayons de créer le fichier avec `File::create`. Cependant, parce que `File::create` pourrait aussi échouer, nous avons besoin d'un deuxième bras dans l'expression `match` interne. Lorsque le fichier ne peut pas être créé, un message d'erreur différent est imprimé. Le deuxième bras du `match` externe reste le même, donc le programme panique pour toute erreur autre que l'erreur de fichier manquant.

> #### Alternatives à l'utilisation de `match` avec `Result<T, E>`
>
> Cela fait beaucoup de `match` ! L'expression `match` est très utile mais également très primitive. Dans le Chapitre 13, vous apprendrez à propos des closures, qui sont utilisées avec de nombreuses méthodes définies sur `Result<T, E>`. Ces méthodes peuvent être plus concises que l'utilisation de `match` lors de la gestion des valeurs `Result<T, E>` dans votre code.
>
> Par exemple, voici une autre manière d'écrire la même logique que celle montrée dans la Liste 9-5, cette fois en utilisant des closures et la méthode `unwrap_or_else` :
>
> ```rust,ignore
> use std::fs::File;
> use std::io::ErrorKind;
>
> fn main() {
>     let greeting_file = File::open("hello.txt").unwrap_or_else(|error| {
>         if error.kind() == ErrorKind::NotFound {
>             File::create("hello.txt").unwrap_or_else(|error| {
>                 panic!("Problème lors de la création du fichier : {error:?}");
>             })
>         } else {
>             panic!("Problème lors de l'ouverture du fichier : {error:?}");
>         }
>     });
> }
> ```
>
> Bien que ce code ait le même comportement que la Liste 9-5, il ne contient aucune expression `match` et est plus lisible. Revenez à cet exemple après avoir lu le Chapitre 13 et consultez la documentation de la méthode `unwrap_or_else` dans la bibliothèque standard. De nombreuses autres méthodes peuvent nettoyer d'énormes expressions `match` imbriquées lorsque vous traitez des erreurs.

#### Raccourcis pour panic en cas d'erreur

Utiliser `match` fonctionne assez bien, mais cela peut être un peu verbeux et ne communique pas toujours clairement l'intention. Le type `Result<T, E>` a de nombreuses méthodes d'assistance définies pour effectuer diverses tâches plus spécifiques. La méthode `unwrap` est une méthode raccourcie implémentée comme l'expression `match` que nous avons écrite dans la Liste 9-4. Si la valeur `Result` est la variante `Ok`, `unwrap` renverra la valeur à l'intérieur de `Ok`. Si le `Result` est la variante `Err`, `unwrap` appellera la macro `panic!` pour nous. Voici un exemple d'utilisation de `unwrap` :

<Listing file-name="src/main.rs">

```rust,should_panic
{{#rustdoc_include ../listings/ch09-error-handling/no-listing-04-unwrap/src/main.rs}}
```

</Listing>

Si nous exécutons ce code sans un fichier _hello.txt_, nous verrons un message d'erreur de l'appel à `panic!` que la méthode `unwrap` fait :

```text
thread 'main' panicked at src/main.rs:4:49:
appel de `Result::unwrap()` sur une valeur `Err` : Os { code : 2, kind : NotFound, message : "Aucun fichier ou répertoire de ce type" }
```

De même, la méthode `expect` nous permet également de choisir le message d'erreur de `panic!`. Utiliser `expect` à la place de `unwrap` et fournir de bons messages d'erreur peut transmettre votre intention et faciliter la recherche de source d'un panic. La syntaxe de `expect` ressemble à ceci :

<Listing file-name="src/main.rs">

```rust,should_panic
{{#rustdoc_include ../listings/ch09-error-handling/no-listing-05-expect/src/main.rs}}
```

</Listing>

Nous utilisons `expect` de la même manière que `unwrap` : pour renvoyer le handle de fichier ou appeler la macro `panic!`. Le message d'erreur utilisé par `expect` dans son appel à `panic!` sera le paramètre que nous passons à `expect`, plutôt que le message `panic!` par défaut que `unwrap` utilise. Voici à quoi cela ressemble :

```text
thread 'main' panicked at src/main.rs:5:10:
hello.txt devrait être inclus dans ce projet : Os { code : 2, kind : NotFound, message : "Aucun fichier ou répertoire de ce type" }
```

Dans du code de qualité production, la plupart des Rustacéens choisissent `expect` plutôt qu'`unwrap` et donnent plus de contexte sur pourquoi l'opération est censée toujours réussir. De cette manière, si vos hypothèses s'avèrent fausses, vous disposez de plus d'informations à utiliser pour le débogage.

### Propagation des erreurs

Lorsque l'implémentation d'une fonction appelle quelque chose qui pourrait échouer, au lieu de gérer l'erreur au sein de la fonction elle-même, vous pouvez retourner l'erreur au code appelant afin qu'il puisse décider quoi faire. Cela s'appelle la _propagation_ de l'erreur et cela donne plus de contrôle au code appelant, où il pourrait y avoir plus d'informations ou de logique dictant comment l'erreur devrait être gérée que ce que vous avez disponible dans le contexte de votre code.

Par exemple, la Liste 9-6 montre une fonction qui lit un nom d'utilisateur à partir d'un fichier. Si le fichier n'existe pas ou ne peut pas être lu, cette fonction retournera ces erreurs au code qui a appelé la fonction.

<Listing number="9-6" file-name="src/main.rs" caption="Une fonction qui retourne des erreurs au code appelant en utilisant `match`">

```rust
{{#include ../listings/ch09-error-handling/listing-09-06/src/main.rs:here}}
```

</Listing>

Cette fonction peut être écrite d'une manière beaucoup plus courte, mais nous allons commencer par faire beaucoup manuellement afin d'explorer la gestion des erreurs ; à la fin, nous montrerons la méthode plus courte. Commençons par examiner le type de retour de la fonction : `Result<String, io::Error>`. Cela signifie que la fonction retourne une valeur du type `Result<T, E>`, où le paramètre générique `T` a été rempli avec le type concret `String` et le type générique `E` a été rempli avec le type concret `io::Error`.

Si cette fonction réussit sans problèmes, le code qui appelle cette fonction recevra une valeur `Ok` contenant un `String` — le `username` que cette fonction a lu à partir du fichier. Si cette fonction rencontre des problèmes, le code appelant recevra une valeur `Err` contenant une instance de `io::Error` qui contient plus d'informations sur les problèmes rencontrés. Nous avons choisi `io::Error` comme type de retour de cette fonction parce que c'est en fait le type de la valeur d'erreur retournée par les deux opérations que nous appelons dans le corps de cette fonction qui pourraient échouer : la fonction `File::open` et la méthode `read_to_string`.

Le corps de la fonction commence par appeler la fonction `File::open`. Ensuite, nous gérons la valeur `Result` avec un `match` similaire à celui de la Liste 9-4. Si `File::open` réussit, le handle de fichier dans la variable de motif `file` devient la valeur de la variable mutable `username_file` et la fonction continue. Dans le cas `Err`, au lieu d'appeler `panic!`, nous utilisons le mot-clé `return` pour sortir immédiatement de la fonction et passer la valeur d'erreur de `File::open`, maintenant dans la variable de motif `e`, au code appelant comme valeur d'erreur de cette fonction.

Ainsi, si nous avons un handle de fichier dans `username_file`, la fonction crée alors une nouvelle `String` dans la variable `username` et appelle la méthode `read_to_string` sur le handle de fichier dans `username_file` pour lire le contenu du fichier dans `username`. La méthode `read_to_string` retourne également un `Result` car elle pourrait échouer, même si `File::open` a réussi. Donc, nous avons besoin d'un autre `match` pour gérer ce `Result` : si `read_to_string` réussit, alors notre fonction a réussi et nous retournons le nom d'utilisateur du fichier qui se trouve maintenant dans `username` enveloppé dans un `Ok`. Si `read_to_string` échoue, nous retournons la valeur d'erreur de la même manière que nous avons retourné la valeur d'erreur dans le `match` qui a géré la valeur de retour de `File::open`. Cependant, nous n'avons pas besoin de dire explicitement `return`, car c'est la dernière expression dans la fonction.

Le code qui appelle ce code gérera alors soit l'obtention d'une valeur `Ok` qui contient un nom d'utilisateur, soit d'une valeur `Err` qui contient un `io::Error`. C'est au code appelant de décider quoi faire avec ces valeurs. Si le code appelant obtient une valeur `Err`, il pourrait appeler `panic!` et faire planter le programme, utiliser un nom d'utilisateur par défaut, ou rechercher le nom d'utilisateur d'une autre source que d'un fichier, par exemple. Nous n'avons pas assez d'informations sur ce que le code appelant essaie réellement de faire, donc nous propagons toutes les informations de succès ou d'erreur vers le haut pour qu'il puisse les gérer de manière appropriée.

Ce schéma de propagation des erreurs est si courant en Rust que Rust fournit l'opérateur point d'interrogation `?` pour faciliter cela.

#### L'opérateur `?` comme raccourci

La Liste 9-7 montre une implémentation de `read_username_from_file` qui a la même fonctionnalité que dans la Liste 9-6, mais cette implémentation utilise l'opérateur `?`.

<Listing number="9-7" file-name="src/main.rs" caption="Une fonction qui retourne des erreurs au code appelant en utilisant l'opérateur `?`">

```rust
{{#include ../listings/ch09-error-handling/listing-09-07/src/main.rs:here}}
```

</Listing>

Le `?` placé après une valeur `Result` est défini pour fonctionner presque de la même manière que les expressions `match` que nous avons définies pour gérer les valeurs `Result` dans la Liste 9-6. Si la valeur du `Result` est un `Ok`, la valeur à l'intérieur de l'`Ok` sera retournée de cette expression, et le programme continuera. Si la valeur est un `Err`, l'`Err` sera retourné depuis toute la fonction comme si nous avions utilisé le mot-clé `return` afin que la valeur d'erreur soit propagée au code appelant.

Il y a une différence entre ce que fait l'expression `match` de la Liste 9-6 et ce que fait l'opérateur `?` : les valeurs d'erreur sur lesquelles l'opérateur `?` est appelé passent par la fonction `from`, définie dans le trait `From` de la bibliothèque standard, qui est utilisée pour convertir des valeurs d'un type à un autre. Lorsque l'opérateur `?` appelle la fonction `from`, le type d'erreur reçu est converti en le type d'erreur défini dans le type de retour de la fonction actuelle. Cela est utile lorsqu'une fonction retourne un type d'erreur représentant toutes les manières dont une fonction pourrait échouer, même si certaines parties pourraient échouer pour de nombreuses raisons différentes.

Par exemple, nous pourrions changer la fonction `read_username_from_file` de la Liste 9-7 pour retourner un type d'erreur personnalisé nommé `OurError` que nous définissons. Si nous définissons également `impl From<io::Error> for OurError` pour construire une instance d'`OurError` à partir d'un `io::Error`, alors les appels opérateurs `?` dans le corps de `read_username_from_file` appeleront `from` et convertiront les types d'erreur sans avoir besoin d'ajouter plus de code à la fonction.

Dans le contexte de la Liste 9-7, le `?` à la fin de l'appel à `File::open` retournera la valeur à l'intérieur d'un `Ok` vers la variable `username_file`. Si une erreur se produit, l'opérateur `?` retournera immédiatement de toute la fonction et donnera toute valeur `Err` au code appelant. La même chose s'applique au `?` à la fin de l'appel à `read_to_string`.

L'opérateur `?` élimine beaucoup de code répétitif et rend l'implémentation de cette fonction plus simple. Nous pourrions même raccourcir davantage ce code en chaînant les appels de méthode immédiatement après le `?`, comme montré dans la Liste 9-8.

<Listing number="9-8" file-name="src/main.rs" caption="Chaînage des appels de méthode après l'opérateur `?`">

```rust
{{#include ../listings/ch09-error-handling/listing-09-08/src/main.rs:here}}
```

</Listing>

Nous avons déplacé la création de la nouvelle `String` dans `username` au début de la fonction ; cette partie n'a pas changé. Au lieu de créer une variable `username_file`, nous avons chaîné l'appel à `read_to_string` directement sur le résultat de `File::open("hello.txt")?`. Nous avons toujours un `?` à la fin de l'appel à `read_to_string`, et nous retournons toujours une valeur `Ok` contenant `username` lorsque à la fois `File::open` et `read_to_string` réussissent plutôt que de retourner des erreurs. La fonctionnalité est de nouveau la même que dans la Liste 9-6 et la Liste 9-7 ; c'est juste une manière différente et plus ergonomique de l'écrire.

La Liste 9-9 montre une manière de rendre cela encore plus court en utilisant `fs::read_to_string`.

<Listing number="9-9" file-name="src/main.rs" caption="Utilisation de `fs::read_to_string` au lieu d'ouvrir puis de lire le fichier">

```rust
{{#include ../listings/ch09-error-handling/listing-09-09/src/main.rs:here}}
```

</Listing>

Lire un fichier dans une chaîne est une opération assez courante, donc la bibliothèque standard fournit la fonction pratique `fs::read_to_string` qui ouvre le fichier, crée une nouvelle `String`, lit le contenu du fichier, met les contenus dans cette `String`, et la retourne. Bien sûr, utiliser `fs::read_to_string` ne nous donne pas l'occasion d'expliquer toute la gestion des erreurs, donc nous l'avons fait de la manière plus longue d'abord.

#### Où utiliser l'opérateur `?`

L'opérateur `?` ne peut être utilisé que dans des fonctions dont le type de retour est compatible avec la valeur sur laquelle le `?` est utilisé. C'est parce que l'opérateur `?` est défini pour effectuer un retour anticipé d'une valeur hors de la fonction, de la même manière que l'expression `match` que nous avons définie dans la Liste 9-6. Dans la Liste 9-6, le `match` utilisait une valeur `Result`, et le bras du retour anticipé retournait une valeur `Err(e)`. Le type de retour de la fonction doit être un `Result` pour qu'il soit compatible avec ce `return`.

Dans la Liste 9-10, examinons l'erreur que nous obtiendrons si nous utilisons l'opérateur `?` dans une fonction `main` avec un type de retour qui est incompatible avec le type de la valeur sur laquelle nous utilisons `?`.

<Listing number="9-10" file-name="src/main.rs" caption="Tentative d'utilisation du `?` dans la fonction `main` qui retourne `()` ne compilera pas.">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch09-error-handling/listing-09-10/src/main.rs}}
```

</Listing>

Ce code ouvre un fichier, ce qui pourrait échouer. L'opérateur `?` suit la valeur `Result` retournée par `File::open`, mais cette fonction `main` a le type de retour de `()`, et non de `Result`. Lorsque nous compilons ce code, nous recevons le message d'erreur suivant :

```console
{{#include ../listings/ch09-error-handling/listing-09-10/output.txt}}
```

Cette erreur indique que nous ne sommes autorisés à utiliser l'opérateur `?` que dans une fonction qui retourne un `Result`, un `Option` ou un autre type qui implémente `FromResidual`.

Pour corriger l'erreur, vous avez deux choix. Un choix est de changer le type de retour de votre fonction pour qu'il soit compatible avec la valeur que vous utilisez sur `?` tant que vous n'avez pas de restrictions empêchant cela. L'autre choix est d'utiliser un `match` ou l'une des méthodes `Result<T, E>` pour gérer le `Result<T, E>` de toute manière appropriée.

Le message d'erreur a également mentionné que le `?` peut être utilisé avec des valeurs `Option<T>` également. Comme avec l'utilisation du `?` sur `Result`, vous ne pouvez utiliser le `?` sur `Option` que dans une fonction qui retourne une `Option`. Le comportement de l'opérateur `?` lorsqu'il est appelé sur un `Option<T>` est similaire à son comportement lorsqu'il est appelé sur un `Result<T, E>` : si la valeur est `None`, le `None` sera retourné de manière anticipée depuis la fonction à ce point. Si la valeur est `Some`, la valeur à l'intérieur du `Some` est la valeur résultante de l'expression, et la fonction continuera. La Liste 9-11 présente un exemple d'une fonction qui trouve le dernier caractère de la première ligne dans le texte donné.

<Listing number="9-11" caption="Utilisation de l'opérateur `?` sur une valeur `Option<T>`">

```rust
{{#rustdoc_include ../listings/ch09-error-handling/listing-09-11/src/main.rs:here}}
```

</Listing>

Cette fonction retourne `Option<char>` parce qu'il est possible qu'il y ait un caractère là, mais il est également possible qu'il n'y en ait pas. Ce code prend l'argument de tranche de chaîne `text` et appelle la méthode `lines` dessus, qui retourne un itérateur sur les lignes de la chaîne. Comme cette fonction veut examiner la première ligne, elle appelle `next` sur l'itérateur pour obtenir la première valeur de l'itérateur. Si `text` est la chaîne vide, cet appel à `next` retournera `None`, auquel cas nous utilisons `?` pour arrêter et retourner `None` depuis `last_char_of_first_line`. Si `text` n'est pas la chaîne vide, `next` retournera une valeur `Some` contenant une tranche de chaîne de la première ligne dans `text`.

Le `?` extrait la tranche de chaîne, et nous pouvons appeler `chars` sur cette tranche de chaîne pour obtenir un itérateur de ses caractères. Nous sommes intéressés par le dernier caractère de cette première ligne, donc nous appelons `last` pour retourner le dernier élément de l'itérateur. C'est un `Option` parce qu'il est possible que la première ligne soit la chaîne vide ; par exemple, si `text` commence par une ligne blanche mais contient des caractères sur d'autres lignes, comme dans `"\nhi"`. Cependant, s’il y a un dernier caractère sur la première ligne, il sera retourné dans la variante `Some`. L'opérateur `?` au milieu nous donne un moyen concis d'exprimer cette logique, permettant d'implémenter la fonction en une seule ligne. Si nous ne pouvions pas utiliser l'opérateur `?` sur `Option`, nous devrions implémenter cette logique à l'aide de plusieurs appels de méthode ou d'une expression `match`.

Notez que vous pouvez utiliser l'opérateur `?` sur un `Result` dans une fonction qui retourne un `Result`, et vous pouvez utiliser l'opérateur `?` sur une `Option` dans une fonction qui retourne une `Option`, mais vous ne pouvez pas les mélanger. L'opérateur `?` ne convertira pas automatiquement un `Result` en un `Option` ou vice versa ; dans ces cas, vous pouvez utiliser des méthodes comme la méthode `ok` sur `Result` ou la méthode `ok_or` sur `Option` pour effectuer la conversion explicitement.

Jusqu'à présent, toutes les fonctions `main` que nous avons utilisées retournent `()`. La fonction `main` est spéciale parce qu'elle est le point d'entrée et de sortie d'un programme exécutable, et il existe des restrictions quant à ce que son type de retour peut être pour que le programme se comporte comme prévu.

Heureusement, `main` peut également retourner un `Result<(), E>`. La Liste 9-12 contient le code provenant de la Liste 9-10, mais nous avons changé le type de retour de `main` pour être `Result<(), Box<dyn Error>>` et ajouté une valeur de retour `Ok(())` à la fin. Ce code va maintenant se compiler.

<Listing number="9-12" file-name="src/main.rs" caption="Changement de `main` pour retourner `Result<(), E>` permet l'utilisation de l'opérateur `?` sur les valeurs `Result`.">

```rust,ignore
{{#rustdoc_include ../listings/ch09-error-handling/listing-09-12/src/main.rs}}
```

</Listing>

Le type `Box<dyn Error>` est un objet de trait, dont nous parlerons dans [« Utilisation des objets de trait pour abstraire sur le comportement partagé »](trait-objects) dans le Chapitre 18. Pour le moment, vous pouvez lire `Box<dyn Error>` comme signifiant « une sorte d'erreur ». Utiliser `?` sur une valeur `Result` dans une fonction `main` avec le type d'erreur `Box<dyn Error>` est autorisé parce qu'il permet à n'importe quelle valeur `Err` d'être retournée de manière anticipée. Même si le corps de cette fonction `main` ne retournera que des erreurs de type `std::io::Error`, en spécifiant `Box<dyn Error>`, cette signature continuera à être correcte même si plus de code retournant d'autres erreurs est ajouté au corps de `main`.

Lorsqu'une fonction `main` retourne un `Result<(), E>`, l'exécutable sortira avec une valeur de `0` si `main` retourne `Ok(())` et sortira avec une valeur non nulle si `main` retourne une valeur `Err`. Les exécutables écrits en C retournent des entiers lorsqu'ils sortent : Les programmes qui réussissent sortent le nombre entier `0`, et les programmes qui rencontrent des erreurs retournent un entier autre que `0`. Rust retourne également des entiers à partir des exécutables pour être compatible avec cette convention.

La fonction `main` peut retourner n'importe quel type qui implémente [le trait `std::process::Termination`](termination), qui contient une fonction `report` qui retourne un `ExitCode`. Consultez la documentation de la bibliothèque standard pour plus d'informations sur l'implémentation du trait `Termination` pour vos propres types.

Maintenant que nous avons discuté des détails concernant l'appel à `panic!` ou le retour de `Result`, retournons au sujet de la façon de décider lequel est approprié à utiliser dans quels cas.

[handle_failure]: ch02-00-guessing-game-tutorial.html#handling-potential-failure-with-result
[trait-objects]: ch18-02-trait-objects.html#using-trait-objects-to-abstract-over-shared-behavior
[termination]: ../std/process/trait.Termination.html