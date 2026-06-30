## Macros

Nous avons utilisé des macros comme `println!` tout au long de ce livre, mais nous n'avons pas encore pleinement exploré ce qu'est une macro et comment elle fonctionne. Le terme _macro_ fait référence à une famille de fonctionnalités en Rust : des macros déclaratives avec `macro_rules!` et trois types de macros procédurales :

- Des macros personnalisées `#[derive]` qui spécifient le code ajouté avec l'attribut `derive` utilisé sur les structures et les énumérations
- Des macros ressemblant à des attributs qui définissent des attributs personnalisés utilisables sur n'importe quel élément
- Des macros ressemblant à des fonctions qui ressemblent à des appels de fonction mais opèrent sur les tokens spécifiés comme argument

Nous allons parler de chacune d'elles à tour de rôle, mais d'abord, examinons pourquoi nous avons besoin de macros alors que nous avons déjà des fonctions.

### La différence entre les macros et les fonctions

Fondamentalement, les macros sont un moyen d'écrire du code qui écrit d'autres codes, ce qu'on appelle _la métaprogrammation_. Dans l'Annexe C, nous discutons de l'attribut `derive`, qui génère une implémentation de divers traits pour vous. Nous avons également utilisé les macros `println!` et `vec!` tout au long du livre. Toutes ces macros _s'étendent_ pour produire plus de code que le code que vous avez écrit manuellement.

La métaprogrammation est utile pour réduire la quantité de code que vous devez écrire et maintenir, ce qui est également l'un des rôles des fonctions. Cependant, les macros ont des pouvoirs supplémentaires que les fonctions n'ont pas.

Une signature de fonction doit déclarer le nombre et le type de paramètres que la fonction possède. Les macros, en revanche, peuvent prendre un nombre variable de paramètres : nous pouvons appeler `println!("hello")` avec un argument ou `println!("hello {}", name)` avec deux arguments. De plus, les macros sont étendues avant que le compilateur n'interprète la signification du code, donc une macro peut, par exemple, implémenter un trait sur un type donné. Une fonction ne le peut pas, car elle est appelée à l'exécution et un trait doit être implémenté au moment de la compilation.

L'inconvénient de l'implémentation d'une macro plutôt que d'une fonction est que les définitions de macros sont plus complexes que les définitions de fonctions car vous écrivez du code Rust qui écrit du code Rust. En raison de cette indirection, les définitions de macros sont généralement plus difficiles à lire, comprendre et maintenir que les définitions de fonctions.

Une autre différence importante entre les macros et les fonctions est que vous devez définir des macros ou les mettre dans le champ d'application _avant_ de les appeler dans un fichier, contrairement aux fonctions que vous pouvez définir n'importe où et appeler n'importe où.

### Macros déclaratives pour la métaprogrammation générale

La forme de macro la plus largement utilisée en Rust est la _macro déclarative_. Celles-ci sont également parfois appelées « macros par exemple », « macros `macro_rules!` » ou simplement « macros ». Au cœur des macros déclaratives, vous pouvez écrire quelque chose de similaire à une expression `match` en Rust. Comme discuté dans le chapitre 6, les expressions `match` sont des structures de contrôle qui prennent une expression, comparent la valeur résultante de l'expression à des motifs, puis exécutent le code associé au motif correspondant. Les macros comparent également une valeur à des motifs associés à un certain code : dans cette situation, la valeur est le code source littéral Rust passé à la macro ; les motifs sont comparés à la structure de ce code source ; et le code associé à chaque motif, lorsqu'il est trouvé, remplace le code passé à la macro. Tout cela se produit pendant la compilation.

Pour définir une macro, vous utilisez la construction `macro_rules!`. Explorons comment utiliser `macro_rules!` en regardant comment la macro `vec!` est définie. Le chapitre 8 a couvert comment nous pouvons utiliser la macro `vec!` pour créer un nouveau vecteur avec des valeurs particulières. Par exemple, la macro suivante crée un nouveau vecteur contenant trois entiers :

```rust
let v: Vec<u32> = vec![1, 2, 3];
```

Nous pourrions également utiliser la macro `vec!` pour créer un vecteur de deux entiers ou un vecteur de cinq tranches de chaînes. Nous ne pourrions pas utiliser une fonction pour faire cela car nous ne saurions pas le nombre ou le type de valeurs à l'avance.

La liste 20-35 montre une définition légèrement simplifiée de la macro `vec!`.

> **Remarque :** La définition réelle de la macro `vec!` dans la bibliothèque standard comprend du code pour pré-allouer la bonne quantité de mémoire à l'avance. Ce code est une optimisation que nous n'incluons pas ici pour simplifier l'exemple.

L’annotation `#[macro_export]` indique que cette macro doit être mise à disposition chaque fois que le crate dans lequel la macro est définie est amené dans le champ d’application. Sans cette annotation, la macro ne peut pas être mise à disposition.

Nous commençons ensuite la définition de la macro avec `macro_rules!` et le nom de la macro que nous définissons _sans_ le point d'exclamation. Le nom, dans ce cas `vec`, est suivi de accolades dénotant le corps de la définition de la macro.

La structure dans le corps de `vec!` est similaire à la structure d'une expression `match`. Ici, nous avons un bras avec le motif `( $( $x:expr ),* )`, suivi de `=>` et du bloc de code associé à ce motif. Si le motif correspond, le bloc de code associé sera émis. Étant donné que c'est le seul motif dans cette macro, il n'y a qu'une seule façon valide de correspondre ; tout autre motif entraînera une erreur. Des macros plus complexes auront plus d'un bras.

La syntaxe de motif valide dans les définitions de macros est différente de la syntaxe de motif couverte au chapitre 19 car les motifs de macros sont comparés à la structure de code Rust plutôt qu'à des valeurs. Examinons ce que signifient les morceaux de motif dans la liste 20-29 ; pour toute la syntaxe de motif de macro, voir la [Référence Rust](../reference/macros-by-example.html).

D'abord, nous utilisons un ensemble de parenthèses pour englober l'ensemble du motif. Nous utilisons un signe dollar (`$`) pour déclarer une variable dans le système de macros qui contiendra le code Rust correspondant au motif. Le signe dollar rend clair qu'il s'agit d'une variable de macro, par opposition à une variable Rust ordinaire. Ensuite, vient un ensemble de parenthèses qui capture les valeurs correspondant au motif à l'intérieur des parenthèses pour utilisation dans le code de remplacement. À l'intérieur de `$()` se trouve `$x:expr`, qui correspond à toute expression Rust et donne à l'expression le nom `$x`.

La virgule suivant `$()` indique qu'un caractère de séparation littéral de virgule doit apparaître entre chaque instance du code qui correspond au code dans `$()`. Le `*` spécifie que le motif correspond à zéro ou plusieurs instances de ce qui précède le `*`.

Lorsque nous appelons cette macro avec `vec![1, 2, 3];`, le motif `$x` correspond trois fois avec les trois expressions `1`, `2` et `3`.

Maintenant, examinons le motif dans le corps du code associé à ce bras : `temp_vec.push()` dans `$()*` est généré pour chaque partie qui correspond à `$()` dans le motif zéro ou plusieurs fois selon le nombre de fois où le motif correspond. Le `$x` est remplacé par chaque expression correspondante. Lorsque nous appelons cette macro avec `vec![1, 2, 3];`, le code généré qui remplace cet appel de macro sera le suivant :

```rust,ignore
{
    let mut temp_vec = Vec::new();
    temp_vec.push(1);
    temp_vec.push(2);
    temp_vec.push(3);
    temp_vec
}
```

Nous avons défini une macro qui peut prendre un nombre quelconque d'arguments de n'importe quel type et peut générer du code pour créer un vecteur contenant les éléments spécifiés.

Pour en savoir plus sur la façon d'écrire des macros, consultez la documentation en ligne ou d'autres ressources, comme [“The Little Book of Rust Macros”](https://veykril.github.io/tlborm/) rédigé par Daniel Keep et continué par Lukas Wirth.

### Macros procédurales pour générer du code à partir d'attributs

La deuxième forme de macros est la macro procédurale, qui agit davantage comme une fonction (et est un type de procédure). Les _macros procédurales_ acceptent un certain code en entrée, opèrent sur ce code et produisent du code en sortie plutôt que de correspondre à des motifs et de remplacer le code par d'autres codes comme le font les macros déclaratives. Les trois types de macros procédurales sont : custom `derive`, semblables à des attributs et semblables à des fonctions, et tous fonctionnent de manière similaire.

Lors de la création de macros procédurales, les définitions doivent résider dans leur propre crate avec un type de crate spécial. Cela pour des raisons techniques complexes que nous espérons éliminer à l'avenir. Dans la liste 20-36, nous montrons comment définir une macro procédurale, où `some_attribute` est un espace réservé pour utiliser une variété spécifique de macro.

La fonction qui définit une macro procédurale prend un `TokenStream` comme entrée et produit un `TokenStream` comme sortie. Le type `TokenStream` est défini par la crate `proc_macro` qui est incluse avec Rust et représente une séquence de tokens. C'est le cœur de la macro : le code source sur lequel la macro opère constitue le `TokenStream` d'entrée, et le code que la macro produit est le `TokenStream` de sortie. La fonction a également un attribut qui lui est attaché spécifiant quel type de macro procédurale nous créons. Nous pouvons avoir plusieurs types de macros procédurales dans la même crate.

Examinons les différents types de macros procédurales. Commençons par une macro `derive` personnalisée, puis expliquons les petites dissimilarités qui rendent les autres formes différentes.

### Macros `derive` personnalisées

Créons une crate nommée `hello_macro` qui définit un trait nommé `HelloMacro` avec une fonction associée nommée `hello_macro`. Plutôt que de faire en sorte que nos utilisateurs implémentent le trait `HelloMacro` pour chacun de leurs types, nous allons fournir une macro procédurale afin que les utilisateurs puissent annoter leur type avec `#[derive(HelloMacro)]` pour obtenir une implémentation par défaut de la fonction `hello_macro`. L'implémentation par défaut affichera `Hello, Macro! My name is TypeName!` où `TypeName` est le nom du type sur lequel ce trait a été défini. En d'autres termes, nous allons écrire un crate qui permet à un autre programmeur d'écrire du code comme dans la liste 20-37 en utilisant notre crate.

Ce code affichera `Hello, Macro! My name is Pancakes!` lorsque nous aurons terminé. La première étape consiste à créer une nouvelle crate de bibliothèque, comme ceci :

```console
$ cargo new hello_macro --lib
```

Ensuite, dans la liste 20-38, nous allons définir le trait `HelloMacro` et sa fonction associée.

Nous avons un trait et sa fonction. À ce stade, notre utilisateur de crate pourrait implémenter le trait pour obtenir la fonctionnalité souhaitée, comme dans la liste 20-39.

Cependant, il lui faudrait écrire le bloc d'implémentation pour chaque type qu'il voulait utiliser avec `hello_macro` ; nous voulons les épargner de ce travail.

De plus, nous ne pouvons pas encore fournir à la fonction `hello_macro` une implémentation par défaut qui affichera le nom du type sur lequel le trait est implémenté : Rust n'a pas de capacités de réflexion, donc il ne peut pas rechercher le nom du type à l'exécution. Nous avons besoin d'une macro pour générer du code à la compilation.

L'étape suivante consiste à définir la macro procédurale. Au moment de la rédaction de ce texte, les macros procédurales doivent se trouver dans leur propre crate. Éventuellement, cette restriction pourrait être levée. La convention pour structurer les crates et les crates de macro est la suivante : Pour une crate nommée `foo`, une crate de macro procédurale `derive` est appelée `foo_derive`. Commençons une nouvelle crate appelée `hello_macro_derive` à l'intérieur de notre projet `hello_macro` :

```console
$ cargo new hello_macro_derive --lib
```

Nos deux crates sont étroitement liées, nous créons donc la crate de macro procédurale à l'intérieur du répertoire de notre crate `hello_macro`. Si nous changeons la définition du trait dans `hello_macro`, nous devrons également changer l'implémentation de la macro procédurale dans `hello_macro_derive`. Les deux crates devront être publiées séparément, et les programmeurs utilisant ces crates devront ajouter les deux comme dépendances et les amener toutes deux dans le champ d’application. Nous pourrions plutôt faire en sorte que la crate `hello_macro` utilise `hello_macro_derive` comme dépendance et réexporte le code de la macro procédurale. Cependant, la manière dont nous avons structuré le projet permet aux programmeurs d'utiliser `hello_macro` même s'ils ne souhaitent pas la fonctionnalité `derive`.

Nous devons déclarer la crate `hello_macro_derive` comme une crate de macro procédurale. Nous aurons également besoin de fonctionnalités des crates `syn` et `quote`, comme vous le verrez dans un instant, il est donc nécessaire de les ajouter comme dépendances. Ajoutez ce qui suit au fichier _Cargo.toml_ pour `hello_macro_derive` :

Pour commencer à définir la macro procédurale, placez le code de la liste 20-40 dans votre fichier _src/lib.rs_ pour la crate `hello_macro_derive`. Notez que ce code ne compiles pas tant que nous n'ajoutons pas une définition pour la fonction `impl_hello_macro`.

Remarquez que nous avons divisé le code en deux fonctions : `hello_macro_derive`, qui est responsable de l'analyse du `TokenStream`, et `impl_hello_macro`, qui est responsable de la transformation de l'arbre de syntaxe : Cela rend l'écriture d'une macro procédurale plus pratique. Le code dans la fonction externe (`hello_macro_derive` dans ce cas) sera le même pour presque toutes les crates de macros procédurales que vous verrez ou créerez. Le code que vous spécifiez dans le corps de la fonction interne (`impl_hello_macro` dans ce cas) sera différent en fonction du but de votre macro procédurale.

Nous avons introduit trois nouvelles crates : `proc_macro`, [`syn`](https://crates.io/crates/syn)<!-- ignore -->, et [`quote`](https://crates.io/crates/quote)<!-- ignore -->. La crate `proc_macro` est livrée avec Rust, donc nous n'avons pas besoin de l'ajouter aux dépendances dans _Cargo.toml_. La crate `proc_macro` est l'API du compilateur qui nous permet de lire et de manipuler le code Rust depuis notre code.

La crate `syn` analyse le code Rust d'une chaîne dans une structure de données sur laquelle nous pouvons effectuer des opérations. La crate `quote` transforme les structures de données `syn` en code Rust. Ces crates rendent beaucoup plus simple l'analyse de tout type de code Rust que nous pourrions vouloir traiter : Écrire un analyseur complet pour le code Rust n'est pas une tâche simple.

La fonction `hello_macro_derive` sera appelée lorsqu'un utilisateur de notre bibliothèque spécifie `#[derive(HelloMacro)]` sur un type. Cela est possible car nous avons annoté la fonction `hello_macro_derive` ici avec `proc_macro_derive` et spécifié le nom `HelloMacro`, qui correspond au nom de notre trait ; c'est la convention suivie par la plupart des macros procédurales.

La fonction `hello_macro_derive` convertit d'abord l'`input` d'un `TokenStream` en une structure de données que nous pouvons ensuite interpréter et sur laquelle nous pouvons effectuer des opérations. C'est là qu'intervient `syn`. La fonction `parse` dans `syn` prend un `TokenStream` et renvoie une structure `DeriveInput` représentant le code Rust analysé. La liste 20-41 montre les parties pertinentes de la structure `DeriveInput` que nous obtenons en analysant la chaîne de code `struct Pancakes;`.

Les champs de cette structure montrent que le code Rust que nous avons analysé est une structure unitaire avec l'`ident` (identifiant, signifiant le nom) de `Pancakes`. Il y a plus de champs dans cette structure pour décrire toutes sortes de code Rust ; consultez la [documentation `syn` pour `DeriveInput`](https://docs.rs/syn/2.0/syn/struct.DeriveInput.html) pour plus d'informations.

Bientôt nous définirons la fonction `impl_hello_macro`, qui est l'endroit où nous construirons le nouveau code Rust que nous voulons inclure. Mais avant cela, notez que la sortie pour notre macro `derive` est également un `TokenStream`. Le `TokenStream` retourné est ajouté au code que nos utilisateurs de crate écrivent, donc lorsque leur crate est compilée, ils obtiendront la fonctionnalité supplémentaire que nous fournissons dans le `TokenStream` modifié.

Vous avez peut-être remarqué que nous appelons `unwrap` pour provoquer un panic de la fonction `hello_macro_derive` si l'appel à la fonction `syn::parse` échoue ici. Il est nécessaire que notre macro procédurale panique en cas d'erreurs car les fonctions `proc_macro_derive` doivent retourner un `TokenStream` plutôt qu'un `Result` pour se conformer à l'API de la macro procédurale. Nous avons simplifié cet exemple en utilisant `unwrap` ; dans le code de production, vous devriez fournir des messages d'erreur plus spécifiques sur ce qui n'a pas fonctionné en utilisant `panic!` ou `expect`.

Maintenant que nous avons le code pour transformer le code Rust annoté d'un `TokenStream` en une instance `DeriveInput`, générons le code qui implémente le trait `HelloMacro` sur le type annoté, comme montré dans la liste 20-42.

Nous obtenons une instance de structure `Ident` contenant le nom (identifiant) du type annoté en utilisant `ast.ident`. La structure dans la liste 20-41 montre qu'en exécutant la fonction `impl_hello_macro` sur le code de la liste 20-37, l'`ident` que nous obtenirons aura le champ `ident` avec une valeur de `"Pancakes"`. Ainsi, la variable `name` dans la liste 20-42 contiendra une instance de structure `Ident` qui, lorsqu'elle est imprimée, sera la chaîne `"Pancakes"`, le nom de la structure dans la liste 20-37.

La macro `quote!` nous permet de définir le code Rust que nous voulons retourner. Le compilateur s'attend à quelque chose de différent du résultat direct de l'exécution de la macro `quote!`, donc nous devons le convertir en un `TokenStream`. Nous faisons cela en appelant la méthode `into`, qui consomme cette représentation intermédiaire et renvoie une valeur du type `TokenStream` requis.

La macro `quote!` fournit également de très bons mécanismes de templating : nous pouvons entrer `#name`, et `quote!` le remplacera par la valeur de la variable `name`. Vous pouvez même faire des répétitions de manière similaire à la façon dont les macros ordinaires fonctionnent. Consultez la [documentation de la crate `quote`](https://docs.rs/quote) pour une introduction approfondie.

Nous voulons que notre macro procédurale génère une implémentation de notre trait `HelloMacro` pour le type que l'utilisateur a annoté, ce que nous pouvons obtenir en utilisant `#name`. L'implémentation du trait a une seule fonction `hello_macro`, dont le corps contient la fonctionnalité que nous souhaitons fournir : imprimer `Hello, Macro! My name is` et ensuite le nom du type annoté.

La macro `stringify!` utilisée ici est intégrée dans Rust. Elle prend une expression Rust, comme `1 + 2`, et à la compilation, la transforme en une chaîne littérale, comme `"1 + 2"`. Cela est différent de `format!` ou `println!`, qui sont des macros qui évaluent l'expression puis transforment le résultat en un `String`. Il est possible que l'entrée `#name` puisse être une expression à imprimer littéralement, donc nous utilisons `stringify!`. L'utilisation de `stringify!` permet également d'économiser une allocation en convertissant `#name` en chaîne littérale au moment de la compilation.

À ce stade, `cargo build` devrait être complété avec succès dans les deux `hello_macro` et `hello_macro_derive`. Connectons ces crates au code de la liste 20-37 pour voir la macro procédurale en action ! Créez un nouveau projet binaire dans votre répertoire _projects_ en utilisant `cargo new pancakes`. Nous devons ajouter `hello_macro` et `hello_macro_derive` comme dépendances dans le _Cargo.toml_ de la crate `pancakes`. Si vous publiez vos versions de `hello_macro` et `hello_macro_derive` sur [crates.io](https://crates.io/)<!-- ignore -->, elles seraient des dépendances normales ; sinon, vous pouvez les spécifier comme dépendances `path` comme suit :

Mettez le code de la liste 20-37 dans _src/main.rs_, et exécutez `cargo run` : il devrait afficher `Hello, Macro! My name is Pancakes!`. L'implémentation du trait `HelloMacro` depuis la macro procédurale a été incluse sans que la crate `pancakes` ait besoin de l'implémenter ; le `#[derive(HelloMacro)]` a ajouté l'implémentation du trait.

Ensuite, explorons comment les autres types de macros procédurales diffèrent des macros `derive` personnalisées. 

### Macros ressemblant à des attributs

Les macros ressemblant à des attributs sont similaires aux macros `derive` personnalisées, mais au lieu de générer du code pour l'attribut `derive`, elles permettent de créer de nouveaux attributs. Elles sont également plus flexibles : `derive` ne fonctionne que pour les structures et les énumérations ; les attributs peuvent être appliqués à d'autres éléments également, comme des fonctions. Voici un exemple d'utilisation d'une macro ressemblant à un attribut. Supposons que vous ayez un attribut nommé `route` qui annoterait des fonctions lorsque vous utilisez un framework d'application web :

```rust,ignore
#[route(GET, "/")]
fn index() {
```

Cet attribut `#[route]` serait défini par le framework en tant que macro procédurale. La signature de la fonction de définition de la macro ressemblerait à ceci :

```rust,ignore
#[proc_macro_attribute]
pub fn route(attr: TokenStream, item: TokenStream) -> TokenStream {
```

Ici, nous avons deux paramètres de type `TokenStream`. Le premier est pour le contenu de l'attribut : la partie `GET, "/"`. Le second est le corps de l'élément auquel l'attribut est attaché : dans ce cas, `fn index() {}` et le reste du corps de la fonction.

Mis à part cela, les macros ressemblant à des attributs fonctionnent de la même manière que les macros `derive` personnalisées : Vous créez une crate avec le type de crate `proc-macro` et implémentez une fonction qui génère le code que vous souhaitez !

### Macros ressemblant à des fonctions

Les macros ressemblant à des fonctions définissent des macros qui ressemblent à des appels de fonction. De manière similaire aux macros `macro_rules!`, elles sont plus flexibles que les fonctions ; par exemple, elles peuvent prendre un nombre inconnu d'arguments. Cependant, les macros `macro_rules!` ne peuvent être définies qu'à l'aide de la syntaxe ressemblant à `match` dont nous avons discuté dans la section [“Macros déclaratives pour la métaprogrammation générale”](#declarative-macros-with-macro_rules-for-general-metaprogramming) plus tôt. Les macros ressemblant à des fonctions prennent un paramètre `TokenStream`, et leur définition manipule ce `TokenStream` en utilisant du code Rust comme le font les deux autres types de macros procédurales. Un exemple de macro ressemblant à une fonction est une macro `sql!` qui pourrait être appelée comme suit :

```rust,ignore
let sql = sql!(SELECT * FROM posts WHERE id=1);
```

Cette macro analyserait l'instruction SQL à l'intérieur et vérifierait qu'elle est syntaxiquement correcte, ce qui est un traitement beaucoup plus complexe qu'une macro `macro_rules!` peut faire. La macro `sql!` serait définie comme ceci :

```rust,ignore
#[proc_macro]
pub fn sql(input: TokenStream) -> TokenStream {
```

Cette définition est similaire à la signature de la macro `derive` personnalisée : nous recevons les tokens qui se trouvent à l'intérieur des parenthèses et retournons le code que nous voulions générer.

## Résumé

Ouf ! Maintenant, vous avez quelques fonctions Rust dans votre boîte à outils que vous n'utiliserez probablement pas souvent, mais vous saurez qu'elles sont disponibles dans des circonstances très particulières. Nous avons introduit plusieurs sujets complexes afin que lorsque vous les rencontrerez dans des suggestions de messages d'erreur ou dans le code d'autres personnes, vous serez en mesure de reconnaître ces concepts et cette syntaxe. Utilisez ce chapitre comme référence pour vous guider vers des solutions.

Ensuite, nous allons mettre en pratique tout ce dont nous avons discuté tout au long du livre et réaliser un dernier projet !