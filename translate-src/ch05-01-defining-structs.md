## Définir et instancier des structs

Les structs sont similaires aux tuples, discutés dans la section [« Le type Tuple »][tuples]<!-- ignore -->, en ce sens qu'ils contiennent tous deux plusieurs valeurs connexes. Comme les tuples, les éléments d'un struct peuvent être de types différents. Contrairement aux tuples, dans un struct, vous nommez chaque élément de données, ce qui rend clair ce que signifient les valeurs. L'ajout de ces noms signifie que les structs sont plus flexibles que les tuples : vous n'avez pas à vous fier à l'ordre des données pour spécifier ou accéder aux valeurs d'une instance.

Pour définir un struct, nous saisissons le mot-clé `struct` et nommons l'ensemble du struct. Le nom d'un struct doit décrire la signification des données regroupées. Ensuite, à l'intérieur des accolades, nous définissons les noms et les types des éléments de données, que nous appelons _champs_. Par exemple, la liste 5-1 montre un struct qui stocke des informations sur un compte utilisateur.

<Listing number="5-1" file-name="src/main.rs" caption="Une définition de struct `User`">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-01/src/main.rs:here}}
```

</Listing>

Pour utiliser un struct après l'avoir défini, nous créons une _instance_ de ce struct en spécifiant des valeurs concrètes pour chacun des champs. Nous créons une instance en indiquant le nom du struct, puis en ajoutant des accolades contenant des paires _`clé: valeur`_, où les clés sont les noms des champs et les valeurs sont les données que nous souhaitons stocker dans ces champs. Nous ne sommes pas tenus de spécifier les champs dans le même ordre que celui dans lequel nous les avons déclarés dans le struct. En d'autres termes, la définition du struct est comme un modèle général pour le type, et les instances le remplissent avec des données particulières pour créer des valeurs de ce type. Par exemple, nous pouvons déclarer un utilisateur particulier comme le montre la liste 5-2.

<Listing number="5-2" file-name="src/main.rs" caption="Création d'une instance du struct `User`">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-02/src/main.rs:here}}
```

</Listing>

Pour obtenir une valeur spécifique d'un struct, nous utilisons la notation par points. Par exemple, pour accéder à l'adresse e-mail de cet utilisateur, nous utilisons `user1.email`. Si l'instance est mutable, nous pouvons changer une valeur en utilisant la notation par points et en assignant à un champ particulier. La liste 5-3 montre comment changer la valeur dans le champ `email` d'une instance mutable `User`.

<Listing number="5-3" file-name="src/main.rs" caption="Changement de la valeur dans le champ `email` d'une instance `User`">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-03/src/main.rs:here}}
```

</Listing>

Notez que l'ensemble de l'instance doit être mutable ; Rust ne nous permet pas de marquer uniquement certains champs comme mutables. Comme pour toute expression, nous pouvons construire une nouvelle instance du struct comme dernière expression dans le corps de la fonction pour retourner implicitement cette nouvelle instance.

La liste 5-4 montre une fonction `build_user` qui retourne une instance `User` avec l'e-mail et le nom d'utilisateur donnés. Le champ `active` reçoit la valeur `true`, et le champ `sign_in_count` reçoit une valeur de `1`.

<Listing number="5-4" file-name="src/main.rs" caption="Une fonction `build_user` qui prend un e-mail et un nom d'utilisateur et retourne une instance `User`">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-04/src/main.rs:here}}
```

</Listing>

Il est logique de nommer les paramètres de la fonction avec le même nom que les champs du struct, mais avoir à répéter les noms des champs `email` et `username` ainsi que les variables est un peu fastidieux. Si le struct avait plus de champs, répéter chaque nom deviendrait encore plus ennuyeux. Heureusement, il existe un raccourci pratique !

### Utiliser le raccourci d'initialisation des champs

Étant donné que les noms de paramètres et les noms de champs du struct sont exactement les mêmes dans la liste 5-4, nous pouvons utiliser la syntaxe _raccourci d'initialisation des champs_ pour réécrire `build_user` afin qu'elle se comporte exactement de la même manière mais sans la répétition de `username` et `email`, comme le montre la liste 5-5.

<Listing number="5-5" file-name="src/main.rs" caption="Une fonction `build_user` qui utilise le raccourci d'initialisation des champs car les paramètres `username` et `email` ont le même nom que les champs du struct">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-05/src/main.rs:here}}
```

</Listing>

Ici, nous créons une nouvelle instance du struct `User`, qui a un champ nommé `email`. Nous voulons définir la valeur du champ `email` sur la valeur du paramètre `email` de la fonction `build_user`. Étant donné que le champ `email` et le paramètre `email` ont le même nom, nous n'avons besoin d'écrire que `email` au lieu de `email: email`.

### Créer des instances avec la syntaxe de mise à jour de struct

Il est souvent utile de créer une nouvelle instance d'un struct qui inclut la plupart des valeurs d'une autre instance du même type, mais en modifiant certaines d'entre elles. Vous pouvez le faire en utilisant la syntaxe de mise à jour de struct.

Tout d'abord, dans la liste 5-6, nous montrons comment créer une nouvelle instance `User` dans `user2` de manière classique, sans la syntaxe de mise à jour. Nous définissons une nouvelle valeur pour `email` mais utilisons sinon les mêmes valeurs que `user1` que nous avons créées dans la liste 5-2.

<Listing number="5-6" file-name="src/main.rs" caption="Création d'une nouvelle instance `User` en utilisant toutes les valeurs sauf une de `user1`">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-06/src/main.rs:here}}
```

</Listing>

En utilisant la syntaxe de mise à jour de struct, nous pouvons obtenir le même effet avec moins de code, comme le montre la liste 5-7. La syntaxe `..` spécifie que les champs restants non définis explicitement doivent avoir la même valeur que les champs de l'instance donnée.

<Listing number="5-7" file-name="src/main.rs" caption="Utilisation de la syntaxe de mise à jour de struct pour définir une nouvelle valeur `email` pour une instance `User`, tout en utilisant le reste des valeurs de `user1`">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-07/src/main.rs:here}}
```

</Listing>

Le code dans la liste 5-7 crée également une instance dans `user2` qui a une valeur différente pour `email`, mais a les mêmes valeurs pour les champs `username`, `active` et `sign_in_count` de `user1`. Le `..user1` doit venir en dernier pour spécifier que tous les champs restants doivent obtenir leurs valeurs des champs correspondants dans `user1`, mais nous pouvons choisir de spécifier des valeurs pour autant de champs que nous le souhaitons dans n'importe quel ordre, indépendamment de l'ordre des champs dans la définition du struct.

Notez que la syntaxe de mise à jour de struct utilise `=` comme une affectation ; cela est dû au fait qu'elle déplace les données, comme nous l'avons vu dans la section [« Variables et données interagissant avec Move »][move]<!-- ignore -->. Dans cet exemple, nous ne pouvons plus utiliser `user1` après avoir créé `user2` car le `String` dans le champ `username` de `user1` a été déplacé dans `user2`. Si nous avions donné à `user2` de nouvelles valeurs `String` pour `email` et `username`, et donc seulement utilisé les valeurs `active` et `sign_in_count` de `user1`, alors `user1` serait toujours valide après la création de `user2`. Les deux champs `active` et `sign_in_count` sont des types qui implémentent le trait `Copy`, donc le comportement que nous avons discuté dans la section [« Données uniquement sur la pile : Copy »][copy]<!-- ignore --> s'appliquerait. Nous pouvons également toujours utiliser `user1.email` dans cet exemple, car sa valeur n'a pas été déplacée de `user1`.

### Créer des types différents avec des tuple structs

Rust prend également en charge des structs qui ressemblent à des tuples, appelés _tuple structs_. Les tuple structs ont le sens supplémentaire que leur nom de struct fournit, mais n'ont pas de noms associés à leurs champs ; ils n'ont que les types des champs. Les tuple structs sont utiles lorsque vous souhaitez donner à l'ensemble du tuple un nom et faire de ce tuple un type différent des autres tuples, et lorsque nommer chaque champ, comme dans un struct ordinaire, serait verbeux ou redondant.

Pour définir un tuple struct, commencez par le mot-clé `struct` et le nom de struct suivi des types dans le tuple. Par exemple, ici nous définissons et utilisons deux tuple structs nommés `Color` et `Point` :

<Listing file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/no-listing-01-tuple-structs/src/main.rs}}
```

</Listing>

Notez que les valeurs `black` et `origin` sont de types différents car elles sont des instances de différents tuple structs. Chaque struct que vous définissez est son propre type, même si les champs à l'intérieur du struct peuvent avoir les mêmes types. Par exemple, une fonction qui prend un paramètre de type `Color` ne peut pas prendre un `Point` comme argument, même si les deux types sont composés de trois valeurs `i32`. Sinon, les instances de tuple struct sont similaires aux tuples en ce sens que vous pouvez les déstructurer en leurs pièces individuelles, et vous pouvez utiliser un `.` suivi de l'index pour accéder à une valeur individuelle. Contrairement aux tuples, les tuple structs exigent que vous nommiez le type du struct lorsque vous les déstructurez. Par exemple, nous écririons `let Point(x, y, z) = origin;` pour déstructurer les valeurs du point `origin` en variables nommées `x`, `y`, et `z`.

### Définir des structs de type unit-like sans champs

Vous pouvez également définir des structs qui n'ont pas de champs ! Ceux-ci sont appelés _structs de type unit-like_ car ils se comportent de manière similaire à `()`, le type unit que nous avons mentionné dans la section [« Le type Tuple »][tuples]<!-- ignore -->. Les structs de type unit-like peuvent être utiles lorsque vous devez implémenter un trait sur un type mais n'avez pas de données que vous souhaitez stocker dans le type lui-même. Nous discuterons des traits dans le chapitre 10. Voici un exemple de déclaration et d'instanciation d'un struct de type unit nommé `AlwaysEqual` :

<Listing file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/no-listing-04-unit-like-structs/src/main.rs}}
```

</Listing>

Pour définir `AlwaysEqual`, nous utilisons le mot-clé `struct`, le nom que nous voulons et ensuite un point-virgule. Pas besoin d'accolades ni de parenthèses ! Ensuite, nous pouvons obtenir une instance de `AlwaysEqual` dans la variable `subject` de manière similaire : en utilisant le nom que nous avons défini, sans aucune accolade ni parenthèse. Imaginez que plus tard nous allons implémenter un comportement pour ce type tel que chaque instance de `AlwaysEqual` est toujours égale à chaque instance de tout autre type, peut-être pour avoir un résultat connu à des fins de test. Nous n'aurions besoin d'aucune donnée pour implémenter ce comportement ! Vous verrez dans le chapitre 10 comment définir des traits et les implémenter sur n'importe quel type, y compris les structs de type unit-like.

> ### Propriété des données du struct
>
> Dans la définition du struct `User` dans la liste 5-1, nous avons utilisé le type possédé `String` plutôt que le type de tranche de chaîne `&str`. C'est un choix délibéré car nous voulons que chaque instance de ce struct possède toutes ses données et que celles-ci soient valides tant que l'ensemble du struct est valide.
>
> Il est également possible pour les structs de stocker des références à des données appartenant à autre chose, mais pour ce faire, il faut utiliser des _durées de vie_, une fonctionnalité de Rust que nous aborderons dans le chapitre 10. Les durées de vie garantissent que les données référencées par un struct sont valides aussi longtemps que le struct l’est. Supposons que vous essayez de stocker une référence dans un struct sans spécifier de durées de vie, comme ce qui suit dans *src/main.rs* ; cela ne fonctionnera pas :
>
> <Listing file-name="src/main.rs">
>
> <!-- CAN'T EXTRACT SEE https://github.com/rust-lang/mdBook/issues/1127 -->
>
> ```rust,ignore,does_not_compile
> struct User {
>     active: bool,
>     username: &str,
>     email: &str,
>     sign_in_count: u64,
> }
>
> fn main() {
>     let user1 = User {
>         active: true,
>         username: "someusername123",
>         email: "someone@example.com",
>         sign_in_count: 1,
>     };
> }
> ```
>
> </Listing>
>
> Le compilateur se plaint qu'il a besoin de spécifications de durée de vie :
>
> ```console
> $ cargo run
>    Compilation de structs v0.1.0 (file:///projects/structs)
> error[E0106]: spécificateur de durée de vie manquant
>  --> src/main.rs:3:15
>   |
> 3 |     username: &str,
>   |               ^ spécificateur de durée de vie nommé attendu
>   |
> aide : envisagez d'introduire un paramètre de durée de vie nommé
>   |
> 1 ~ struct User<'a> {
> 2 |     active: bool,
> 3 ~     username: &'a str,
>   |
>
> error[E0106]: spécificateur de durée de vie manquant
>  --> src/main.rs:4:12
>   |
> 4 |     email: &str,
>   |            ^ spécificateur de durée de vie nommé attendu
>   |
> aide : envisagez d'introduire un paramètre de durée de vie nommé
>   |
> 1 ~ struct User<'a> {
> 2 |     active: bool,
> 3 |     username: &str,
> 4 ~     email: &'a str,
>   |
>
> Pour plus d'informations sur cette erreur, essayez `rustc --explain E0106`.
> erreur : impossible de compiler `structs` (bin "structs") en raison de 2 erreurs précédentes
> ```
>
> Dans le chapitre 10, nous aborderons comment corriger ces erreurs afin que vous puissiez stocker des références dans des structs, mais pour l'instant, nous corrigerons ces erreurs en utilisant des types possédés comme `String` plutôt que des références comme `&str`.

[tuples]: ch03-02-data-types.html#the-tuple-type
[move]: ch04-01-what-is-ownership.html#variables-and-data-interacting-with-move
[copy]: ch04-01-what-is-ownership.html#stack-only-data-copy