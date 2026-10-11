## Macros

Nous avons utilisé des macros comme `println!` tout au long de ce livre, mais nous n’avons pas encore étudié en détail ce qu’est une macro et comment elle fonctionne. Le terme _macro_ désigne une famille de fonctionnalités de Rust : les macros déclaratives avec `macro_rules!` et trois types de macros procédurales :

- Les macros personnalisées `#[derive]`, qui indiquent le code à ajouter à l’aide de l’attribut `derive` utilisé sur les structs et les enums
- Les macros semblables à des attributs, qui définissent des attributs personnalisés pouvant être utilisés sur n’importe quel élément
- Les macros semblables à des fonctions, qui ressemblent à des appels de fonction, mais opèrent sur les jetons spécifiés comme argument

Nous allons parler de chacune d’elles à tour de rôle, mais commençons par examiner pourquoi nous avons besoin de macros alors que nous disposons déjà de fonctions.

### Différence entre les macros et les fonctions

Fondamentalement, les macros permettent d’écrire du code qui écrit d’autres codes, ce que l’on appelle la _métaprogrammation_. À l’annexe C, nous abordons l’attribut `derive`, qui génère pour vous une implémentation de différents traits. Nous avons également utilisé les macros `println!` et `vec!` tout au long de ce livre. Toutes ces macros _s’étendent_ pour produire davantage de code que celui que vous avez écrit manuellement.

La métaprogrammation est utile pour réduire la quantité de code que vous devez écrire et maintenir, ce qui est également l’un des rôles des fonctions. Toutefois, les macros ont des capacités supplémentaires dont les fonctions ne disposent pas.

La signature d’une fonction doit déclarer le nombre et le type de ses paramètres. Les macros, quant à elles, peuvent prendre un nombre variable de paramètres : nous pouvons appeler `println!("hello")` avec un argument ou `println!("hello {}", name)` avec deux arguments. De plus, les macros sont développées avant que le compilateur n’interprète le sens du code. Une macro peut donc, par exemple, implémenter un trait pour un type donné. Une fonction ne le peut pas, car elle est appelée à l’exécution et un trait doit être implémenté à la compilation.

L’inconvénient de l’implémentation d’une macro plutôt que d’une fonction est que les définitions de macros sont plus complexes que les définitions de fonctions, car vous écrivez du code Rust qui écrit du code Rust. En raison de cette indirection, les définitions de macros sont généralement plus difficiles à lire, à comprendre et à maintenir que les définitions de fonctions.

Une autre différence importante entre les macros et les fonctions est que vous devez définir les macros ou les importer dans la portée _avant_ de les appeler dans un fichier, contrairement aux fonctions, que vous pouvez définir et appeler n’importe où.

<!-- Old headings. Do not remove or links may break. -->

<a id="declarative-macros-with-macro_rules-for-general-metaprogramming"></a>

### Macros déclaratives pour la métaprogrammation générale

La forme de macro la plus utilisée dans Rust est la _macro déclarative_. On les appelle parfois aussi « macros par l’exemple », « macros `macro_rules!` » ou simplement « macros ». À la base, les macros déclaratives vous permettent d’écrire quelque chose de similaire à une expression `match` de Rust. Comme nous l’avons vu au chapitre 6, les expressions `match` sont des structures de contrôle qui prennent une expression, comparent la valeur obtenue aux motifs, puis exécutent le code associé au motif correspondant. Les macros comparent elles aussi une valeur à des motifs associés à du code particulier : dans ce cas, la valeur est le code source Rust littéral transmis à la macro ; les motifs sont comparés à la structure de ce code source ; et, lorsqu’un motif correspond, le code associé à ce motif remplace le code transmis à la macro. Tout cela se produit pendant la compilation.

Pour définir une macro, vous utilisez la construction `macro_rules!`. Voyons comment utiliser `macro_rules!` en examinant la définition de la macro `vec!`. Au chapitre 8, nous avons vu comment utiliser la macro `vec!` pour créer un nouveau vecteur contenant des valeurs données. Par exemple, la macro suivante crée un nouveau vecteur contenant trois entiers :

```rust
let v: Vec<u32> = vec![1, 2, 3];
```

Nous pourrions aussi utiliser la macro `vec!` pour créer un vecteur de deux entiers ou un vecteur de cinq tranches de chaînes de caractères. Nous ne pourrions pas utiliser une fonction pour faire la même chose, car nous ne connaîtrions pas à l’avance le nombre ni le type des valeurs.

La liste 20-35 présente une définition légèrement simplifiée de la macro `vec!`.

<Listing number="20-35" file-name="src/lib.rs" caption="Version simplifiée de la définition de la macro `vec!`">

```rust,noplayground
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-35/src/lib.rs}}
```

</Listing>

> Remarque : la définition réelle de la macro `vec!` dans la bibliothèque standard comprend du code qui préalloue la quantité de mémoire appropriée. Ce code est une optimisation que nous n’incluons pas ici afin de simplifier l’exemple.

L’annotation `#[macro_export]` indique que cette macro doit être accessible dès que la crate dans laquelle elle est définie est importée dans la portée. Sans cette annotation, il est impossible d’importer la macro dans la portée.

Nous commençons ensuite la définition de la macro avec `macro_rules!`, suivi du nom de la macro que nous définissons, _sans_ le point d’exclamation. Le nom — `vec` dans ce cas — est suivi d’accolades qui délimitent le corps de la définition de la macro.

La structure du corps de `vec!` est semblable à celle d’une expression `match`. Ici, nous avons un bras avec le motif `( $( $x:expr ),* )`, suivi de `=>` et du bloc de code associé à ce motif. Si le motif correspond, le bloc de code associé sera généré. Comme c’est le seul motif de cette macro, il n’y a qu’une seule façon valide de faire correspondre le motif ; tout autre motif entraînera une erreur. Les macros plus complexes comporteront plusieurs bras.

La syntaxe des motifs valides dans les définitions de macros diffère de celle abordée au chapitre 19, car les motifs de macros sont comparés à la structure du code Rust plutôt qu’à des valeurs. Examinons la signification des éléments du motif de la liste 20-29 ; pour connaître toute la syntaxe des motifs de macros, consultez la [référence Rust][ref].

Tout d’abord, nous utilisons des parenthèses pour englober tout le motif. Nous utilisons un signe dollar (`$`) pour déclarer une variable dans le système de macros, qui contiendra le code Rust correspondant au motif. Le signe dollar indique clairement qu’il s’agit d’une variable de macro et non d’une variable Rust ordinaire. Viennent ensuite des parenthèses qui capturent les valeurs correspondant au motif à l’intérieur des parenthèses, afin de les utiliser dans le code de remplacement. À l’intérieur de `$()`, nous trouvons `$x:expr`, qui correspond à toute expression Rust et attribue à cette expression le nom `$x`.

La virgule qui suit `$()` indique qu’une virgule littérale doit apparaître comme séparateur entre chaque occurrence du code correspondant au code dans `$()`. Le symbole `*` indique que le motif correspond à zéro ou plusieurs occurrences de ce qui précède le `*`.

Lorsque nous appelons cette macro avec `vec![1, 2, 3];`, le motif `$x` correspond trois fois aux trois expressions `1`, `2` et `3`.

Examinons maintenant le motif dans le corps du code associé à ce bras : `temp_vec.push()` à l’intérieur de `$()*` est généré pour chaque élément correspondant à `$()` dans le motif, zéro ou plusieurs fois selon le nombre de correspondances. `$x` est remplacé par chaque expression correspondante. Lorsque nous appelons cette macro avec `vec![1, 2, 3];`, le code généré qui remplace cet appel de macro est le suivant :

```rust,ignore
{
    let mut temp_vec = Vec::new();
    temp_vec.push(1);
    temp_vec.push(2);
    temp_vec.push(3);
    temp_vec
}
```

Nous avons défini une macro qui peut prendre un nombre quelconque d’arguments de n’importe quel type et générer du code créant un vecteur contenant les éléments spécifiés.

Pour en savoir plus sur l’écriture de macros, consultez la documentation en ligne ou d’autres ressources, telles que [« The Little Book of Rust Macros »][tlborm], commencé par Daniel Keep et poursuivi par Lukas Wirth.

### Macros procédurales pour générer du code à partir d’attributs

La deuxième forme de macro est la macro procédurale, qui se comporte davantage comme une fonction (et constitue un type de procédure). Les _macros procédurales_ acceptent du code en entrée, opèrent sur ce code et produisent du code en sortie, plutôt que de comparer des motifs et de remplacer le code par un autre comme le font les macros déclaratives. Il existe trois types de macros procédurales : les macros `derive` personnalisées, les macros semblables à des attributs et les macros semblables à des fonctions, qui fonctionnent toutes de manière similaire.

Lors de la création de macros procédurales, leurs définitions doivent résider dans leur propre crate, dotée d’un type de crate spécial. Cela s’explique par des raisons techniques complexes que nous espérons pouvoir éliminer à l’avenir. Dans la liste 20-36, nous montrons comment définir une macro procédurale, où `some_attribute` est un espace réservé à l’utilisation d’un type de macro particulier.

<Listing number="20-36" file-name="src/lib.rs" caption="Exemple de définition d’une macro procédurale">

```rust,ignore
use proc_macro::TokenStream;

#[some_attribute]
pub fn some_name(input: TokenStream) -> TokenStream {
}
```

</Listing>

La fonction qui définit une macro procédurale prend un `TokenStream` en entrée et produit un `TokenStream` en sortie. Le type `TokenStream` est défini par la crate `proc_macro`, fournie avec Rust, et représente une séquence de jetons. C’est le cœur de la macro : le code source sur lequel opère la macro constitue le `TokenStream` d’entrée, et le code produit par la macro constitue le `TokenStream` de sortie. La fonction est également associée à un attribut qui spécifie le type de macro procédurale que nous créons. Nous pouvons avoir plusieurs types de macros procédurales dans une même crate.

Examinons les différents types de macros procédurales. Nous allons commencer par une macro `derive` personnalisée, puis expliquer les légères différences qui distinguent les autres formes.

<!-- Old headings. Do not remove or links may break. -->

<a id="how-to-write-a-custom-derive-macro"></a>

### Macros `derive` personnalisées

Créons une crate nommée `hello_macro` qui définit un trait nommé `HelloMacro` avec une fonction associée nommée `hello_macro`. Plutôt que de demander à nos utilisateurs d’implémenter le trait `HelloMacro` pour chacun de leurs types, nous allons leur fournir une macro procédurale afin qu’ils puissent annoter leur type avec `#[derive(HelloMacro)]` et obtenir une implémentation par défaut de la fonction `hello_macro`. L’implémentation par défaut affichera `Hello, Macro! My name is TypeName!`, où `TypeName` est le nom du type pour lequel ce trait a été défini. En d’autres termes, nous allons écrire une crate qui permettra à un autre programmeur d’écrire du code comme celui de la liste 20-37 en utilisant notre crate.

<Listing number="20-37" file-name="src/main.rs" caption="Code qu’un utilisateur de notre crate pourra écrire en utilisant notre macro procédurale">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-37/src/main.rs}}
```

</Listing>

Une fois que nous aurons terminé, ce code affichera `Hello, Macro! My name is Pancakes!`. La première étape consiste à créer une nouvelle crate de bibliothèque, comme ceci :

```console
$ cargo new hello_macro --lib
```

Ensuite, dans la liste 20-38, nous allons définir le trait `HelloMacro` et sa fonction associée.

<Listing file-name="src/lib.rs" number="20-38" caption="Trait simple que nous utiliserons avec la macro `derive`">

```rust,noplayground
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-38/hello_macro/src/lib.rs}}
```

</Listing>

Nous avons un trait et sa fonction. À ce stade, l’utilisateur de notre crate pourrait implémenter le trait pour obtenir la fonctionnalité souhaitée, comme dans la liste 20-39.

<Listing number="20-39" file-name="src/main.rs" caption="À quoi ressemblerait une implémentation manuelle du trait `HelloMacro` par les utilisateurs">

```rust,ignore
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-39/pancakes/src/main.rs}}
```

</Listing>

Toutefois, ils devraient écrire le bloc d’implémentation pour chaque type qu’ils souhaitent utiliser avec `hello_macro` ; nous voulons leur éviter ce travail.

De plus, nous ne pouvons pas encore fournir à la fonction `hello_macro` une implémentation par défaut qui affiche le nom du type pour lequel le trait est implémenté : Rust ne dispose pas de capacités de réflexion et ne peut donc pas récupérer le nom du type à l’exécution. Nous avons besoin d’une macro pour générer du code à la compilation.

L’étape suivante consiste à définir la macro procédurale. Au moment de la rédaction de ce texte, les macros procédurales doivent se trouver dans leur propre crate. Cette restriction pourrait être levée à l’avenir. La convention de structuration des crates et des crates de macros est la suivante : pour une crate nommée `foo`, une crate de macro procédurale `derive` personnalisée est appelée `foo_derive`. Créons une nouvelle crate nommée `hello_macro_derive` dans notre projet `hello_macro` :

```console
$ cargo new hello_macro_derive --lib
```

Nos deux crates sont étroitement liées ; nous créons donc la crate de macros procédurales dans le répertoire de notre crate `hello_macro`. Si nous modifions la définition du trait dans `hello_macro`, nous devrons également modifier l’implémentation de la macro procédurale dans `hello_macro_derive`. Les deux crates devront être publiées séparément, et les programmeurs qui les utilisent devront les ajouter toutes deux comme dépendances et les importer toutes deux dans la portée. Nous pourrions plutôt faire de la crate `hello_macro` une dépendance de `hello_macro_derive` et réexporter le code de la macro procédurale. Toutefois, la structure que nous avons choisie permet aux programmeurs d’utiliser `hello_macro` même s’ils ne souhaitent pas bénéficier de la fonctionnalité `derive`.

Nous devons déclarer la crate `hello_macro_derive` comme crate de macro procédurale. Nous aurons également besoin des fonctionnalités des crates `syn` et `quote`, comme vous le verrez bientôt ; nous devons donc les ajouter comme dépendances. Ajoutez ce qui suit au fichier _Cargo.toml_ de `hello_macro_derive` :

<Listing file-name="hello_macro_derive/Cargo.toml">

```toml
{{#include ../listings/ch20-advanced-features/listing-20-40/hello_macro/hello_macro_derive/Cargo.toml:6:12}}
```

</Listing>

Pour commencer à définir la macro procédurale, placez le code de la liste 20-40 dans votre fichier _src/lib.rs_ de la crate `hello_macro_derive`. Notez que ce code ne compilera pas tant que nous n’aurons pas ajouté de définition pour la fonction `impl_hello_macro`.

<Listing number="20-40" file-name="hello_macro_derive/src/lib.rs" caption="Code dont la plupart des crates de macros procédurales ont besoin pour traiter du code Rust">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-40/hello_macro/hello_macro_derive/src/lib.rs}}
```

</Listing>

Remarquez que nous avons réparti le code entre la fonction `hello_macro_derive`, qui est chargée d’analyser le `TokenStream`, et la fonction `impl_hello_macro`, qui est chargée de transformer l’arbre syntaxique : cela facilite l’écriture d’une macro procédurale. Le code de la fonction externe (`hello_macro_derive` dans ce cas) sera identique pour presque toutes les crates de macros procédurales que vous rencontrerez ou créerez. Le code que vous spécifiez dans le corps de la fonction interne (`impl_hello_macro` dans ce cas) variera en fonction de l’objectif de votre macro procédurale.

Nous avons introduit trois nouvelles crates : `proc_macro`, [`syn`][syn]<!-- ignore --> et [`quote`][quote]<!-- ignore -->. La crate `proc_macro` est fournie avec Rust ; nous n’avons donc pas besoin de l’ajouter aux dépendances dans _Cargo.toml_. La crate `proc_macro` est l’API du compilateur qui nous permet de lire et de manipuler du code Rust depuis notre code.

La crate `syn` analyse du code Rust à partir d’une chaîne et le transforme en une structure de données sur laquelle nous pouvons effectuer des opérations. La crate `quote` transforme les structures de données `syn` en code Rust. Ces crates simplifient grandement l’analyse de tout type de code Rust que nous pourrions vouloir traiter : écrire un analyseur syntaxique complet pour le code Rust n’est pas une tâche simple.

La fonction `hello_macro_derive` sera appelée lorsqu’un utilisateur de notre bibliothèque spécifiera `#[derive(HelloMacro)]` sur un type. C’est possible parce que nous avons annoté ici la fonction `hello_macro_derive` avec `proc_macro_derive` et spécifié le nom `HelloMacro`, qui correspond au nom de notre trait ; c’est la convention suivie par la plupart des macros procédurales.

La fonction `hello_macro_derive` convertit d’abord `input`, qui est un `TokenStream`, en une structure de données que nous pouvons ensuite interpréter et manipuler. C’est là qu’intervient `syn`. La fonction `parse` de `syn` prend un `TokenStream` et renvoie une struct `DeriveInput` représentant le code Rust analysé. La liste 20-41 montre les parties pertinentes de la struct `DeriveInput` obtenue en analysant la chaîne `struct Pancakes;`.

<Listing number="20-41" caption="Instance de `DeriveInput` obtenue en analysant le code contenant l’attribut de macro de la liste 20-37">

```rust,ignore
DeriveInput {
    // --snip--

    ident: Ident {
        ident: "Pancakes",
        span: #0 bytes(95..103)
    },
    data: Struct(
        DataStruct {
            struct_token: Struct,
            fields: Unit,
            semi_token: Some(
                Semi
            )
        }
    )
}
```

</Listing>

Les champs de cette struct indiquent que le code Rust que nous avons analysé est une struct unitaire dont l’`ident` (_identifiant_, c’est-à-dire le nom) est `Pancakes`. Cette struct comporte d’autres champs qui décrivent toutes sortes de code Rust ; consultez la [documentation de `syn` sur `DeriveInput`][syn-docs] pour en savoir plus.

Nous allons bientôt définir la fonction `impl_hello_macro`, dans laquelle nous construirons le nouveau code Rust que nous voulons inclure. Mais avant cela, notez que la sortie de notre macro `derive` est également un `TokenStream`. Le `TokenStream` renvoyé est ajouté au code écrit par les utilisateurs de notre crate. Ainsi, lorsqu’ils compilent leur crate, ils obtiennent les fonctionnalités supplémentaires que nous fournissons dans le `TokenStream` modifié.

Vous avez peut-être remarqué que nous appelons `unwrap` pour provoquer une panique dans la fonction `hello_macro_derive` si l’appel à la fonction `syn::parse` échoue ici. Notre macro procédurale doit nécessairement déclencher une panique en cas d’erreur, car les fonctions `proc_macro_derive` doivent renvoyer un `TokenStream` plutôt qu’un `Result` pour se conformer à l’API des macros procédurales. Nous avons simplifié cet exemple en utilisant `unwrap` ; dans du code de production, vous devriez fournir des messages d’erreur plus précis sur ce qui s’est passé en utilisant `panic!` ou `expect`.

Maintenant que nous avons le code permettant de transformer le code Rust annoté, qui est un `TokenStream`, en une instance de `DeriveInput`, générons le code qui implémente le trait `HelloMacro` pour le type annoté, comme le montre la liste 20-42.

<Listing number="20-42" file-name="hello_macro_derive/src/lib.rs" caption="Implémentation du trait `HelloMacro` à l’aide du code Rust analysé">

```rust,ignore
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-42/hello_macro/hello_macro_derive/src/lib.rs:here}}
```

</Listing>

Nous obtenons une instance de la struct `Ident` contenant le nom (l’identifiant) du type annoté à l’aide de `ast.ident`. La struct de la liste 20-41 montre que, lorsque nous exécutons la fonction `impl_hello_macro` sur le code de la liste 20-37, l’`ident` obtenu aura un champ `ident` dont la valeur sera `"Pancakes"`. Ainsi, la variable `name` de la liste 20-42 contiendra une instance de la struct `Ident` qui, lorsqu’elle sera affichée, donnera la chaîne `"Pancakes"`, nom de la struct de la liste 20-37.

La macro `quote!` nous permet de définir le code Rust que nous voulons renvoyer. Le compilateur attend un résultat différent de celui produit directement par l’exécution de la macro `quote!` ; nous devons donc le convertir en `TokenStream`. Pour ce faire, nous appelons la méthode `into`, qui consomme cette représentation intermédiaire et renvoie une valeur du type `TokenStream` requis.

La macro `quote!` propose également des mécanismes de génération de modèles très pratiques : nous pouvons écrire `#name`, et `quote!` le remplacera par la valeur de la variable `name`. Vous pouvez même effectuer des répétitions, comme avec les macros ordinaires. Consultez la [documentation de la crate `quote`][quote-docs] pour une présentation détaillée.

Nous voulons que notre macro procédurale génère une implémentation de notre trait `HelloMacro` pour le type annoté par l’utilisateur, que nous pouvons obtenir avec `#name`. L’implémentation du trait contient une seule fonction, `hello_macro`, dont le corps comprend la fonctionnalité que nous voulons fournir : afficher `Hello, Macro! My name is`, puis le nom du type annoté.

La macro `stringify!` utilisée ici est intégrée à Rust. Elle prend une expression Rust, telle que `1 + 2`, et la transforme à la compilation en littéral chaîne, tel que `"1 + 2"`. Cela diffère de `format!` ou de `println!`, qui sont des macros évaluant l’expression puis transformant le résultat en `String`. Il est possible que l’entrée `#name` soit une expression à afficher littéralement ; nous utilisons donc `stringify!`. L’utilisation de `stringify!` évite également une allocation en convertissant `#name` en littéral chaîne à la compilation.

À ce stade, `cargo build` devrait se terminer avec succès dans `hello_macro` comme dans `hello_macro_derive`. Relions ces crates au code de la liste 20-37 pour voir la macro procédurale en action ! Créez un nouveau projet binaire dans votre répertoire _projects_ avec `cargo new pancakes`. Nous devons ajouter `hello_macro` et `hello_macro_derive` comme dépendances dans le fichier _Cargo.toml_ de la crate `pancakes`. Si vous publiez vos versions de `hello_macro` et `hello_macro_derive` sur [crates.io](https://crates.io/)<!-- ignore -->, elles seront des dépendances ordinaires ; sinon, vous pouvez les spécifier comme dépendances `path`, comme ceci :

```toml
{{#include ../listings/ch20-advanced-features/no-listing-21-pancakes/pancakes/Cargo.toml:6:8}}
```

Placez le code de la liste 20-37 dans _src/main.rs_, puis exécutez `cargo run` : le programme devrait afficher `Hello, Macro! My name is Pancakes!`. L’implémentation du trait `HelloMacro` fournie par la macro procédurale a été incluse sans que la crate `pancakes` ait besoin de l’implémenter ; l’attribut `#[derive(HelloMacro)]` a ajouté l’implémentation du trait.

Examinons maintenant en quoi les autres types de macros procédurales diffèrent des macros `derive` personnalisées.

### Macros semblables à des attributs

Les macros semblables à des attributs ressemblent aux macros `derive` personnalisées, mais au lieu de générer du code pour l’attribut `derive`, elles vous permettent de créer de nouveaux attributs. Elles sont également plus flexibles : `derive` ne fonctionne que sur les structs et les enums, tandis que les attributs peuvent aussi être appliqués à d’autres éléments, comme les fonctions. Voici un exemple d’utilisation d’une macro semblable à un attribut. Supposons que vous disposiez d’un attribut nommé `route` qui annote des fonctions dans un framework d’application web :

```rust,ignore
#[route(GET, "/")]
fn index() {
```

Cet attribut `#[route]` serait défini par le framework sous la forme d’une macro procédurale. La signature de la fonction définissant la macro ressemblerait à ceci :

```rust,ignore
#[proc_macro_attribute]
pub fn route(attr: TokenStream, item: TokenStream) -> TokenStream {
```

Nous avons ici deux paramètres de type `TokenStream`. Le premier correspond au contenu de l’attribut, c’est-à-dire à la partie `GET, "/"`. Le second correspond au corps de l’élément auquel l’attribut est associé : dans ce cas, `fn index() {}` ainsi que le reste du corps de la fonction.

À part cela, les macros semblables à des attributs fonctionnent comme les macros `derive` personnalisées : vous créez une crate de type `proc-macro` et implémentez une fonction qui génère le code souhaité !

### Macros semblables à des fonctions

Les macros semblables à des fonctions définissent des macros qui ressemblent à des appels de fonction. Comme les macros `macro_rules!`, elles sont plus flexibles que les fonctions ; elles peuvent, par exemple, prendre un nombre inconnu d’arguments. Toutefois, les macros `macro_rules!` ne peuvent être définies qu’à l’aide de la syntaxe semblable à une correspondance que nous avons abordée précédemment dans la section [« Macros déclaratives pour la métaprogrammation générale »][decl]<!-- ignore -->. Les macros semblables à des fonctions prennent un paramètre `TokenStream` et leur définition manipule ce `TokenStream` à l’aide de code Rust, comme le font les deux autres types de macros procédurales. Une macro `sql!` est un exemple de macro semblable à une fonction ; elle pourrait être appelée ainsi :

```rust,ignore
let sql = sql!(SELECT * FROM posts WHERE id=1);
```

Cette macro analyserait l’instruction SQL qu’elle contient et vérifierait qu’elle est syntaxiquement correcte, ce qui implique un traitement bien plus complexe que ce qu’une macro `macro_rules!` peut effectuer. La macro `sql!` serait définie ainsi :

```rust,ignore
#[proc_macro]
pub fn sql(input: TokenStream) -> TokenStream {
```

Cette définition ressemble à la signature d’une macro `derive` personnalisée : nous recevons les jetons qui se trouvent entre les parenthèses et renvoyons le code que nous voulons générer.

## Résumé

Ouf ! Vous disposez maintenant dans votre boîte à outils de fonctionnalités de Rust que vous n’utiliserez probablement pas souvent, mais vous savez qu’elles existent et dans quelles situations bien particulières elles peuvent être utiles. Nous avons présenté plusieurs sujets complexes afin que, lorsque vous les rencontrerez dans des suggestions de messages d’erreur ou dans le code d’autres personnes, vous puissiez reconnaître ces concepts et cette syntaxe. Utilisez ce chapitre comme référence pour vous guider vers des solutions.

Nous allons maintenant mettre en pratique tout ce dont nous avons parlé dans ce livre et réaliser un dernier projet !

[ref]: ../reference/macros-by-example.html
[tlborm]: https://veykril.github.io/tlborm/
[syn]: https://crates.io/crates/syn
[quote]: https://crates.io/crates/quote
[syn-docs]: https://docs.rs/syn/2.0/syn/struct.DeriveInput.html
[quote-docs]: https://docs.rs/quote
[decl]: #declarative-macros-with-macro_rules-for-general-metaprogramming