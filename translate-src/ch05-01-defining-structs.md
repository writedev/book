## Définir et instancier des structures

Les structures sont similaires aux tuples, abordés dans la section [« Le type tuple »][tuples]<!--
ignore -->, car les deux permettent de regrouper plusieurs valeurs liées. Comme
les tuples, les éléments d’une structure peuvent être de types différents.
Contrairement aux tuples, dans une structure, vous nommez chaque élément de
donnée afin d’indiquer clairement ce que signifient les valeurs. Ces noms
rendent les structures plus flexibles que les tuples : vous n’avez pas à vous
fier à l’ordre des données pour spécifier ou accéder aux valeurs d’une
instance.

Pour définir une structure, nous utilisons le mot-clé `struct` et donnons un
nom à la structure entière. Le nom d’une structure doit décrire l’importance
des éléments de données regroupés. Ensuite, entre accolades, nous définissons
les noms et les types des éléments de données, que nous appelons des _champs_.
Par exemple, le Listing 5-1 montre une structure qui stocke des informations
sur un compte utilisateur.

<Listing number="5-1" file-name="src/main.rs" caption="Définition d’une structure `User`">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-01/src/main.rs:here}}
```

</Listing>

Pour utiliser une structure après l’avoir définie, nous créons une _instance_
de cette structure en indiquant des valeurs concrètes pour chacun de ses
champs. Nous créons une instance en indiquant le nom de la structure, puis en
ajoutant des accolades contenant des paires _`clé : valeur`_, où les clés
sont les noms des champs et les valeurs sont les données que nous voulons y
stocker. Nous ne sommes pas obligés de spécifier les champs dans le même ordre
que celui dans lequel nous les avons déclarés dans la structure. Autrement
dit, la définition de la structure est comme un modèle général pour le type, et
les instances remplissent ce modèle avec des données particulières afin de
créer des valeurs de ce type. Par exemple, nous pouvons déclarer un utilisateur
particulier comme indiqué dans le Listing 5-2.

<Listing number="5-2" file-name="src/main.rs" caption="Création d’une instance de la structure `User`">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-02/src/main.rs:here}}
```

</Listing>

Pour obtenir une valeur précise d’une structure, nous utilisons la notation
avec un point. Par exemple, pour accéder à l’adresse e-mail de cet utilisateur,
nous utilisons `user1.email`. Si l’instance est modifiable, nous pouvons
changer une valeur en utilisant la notation avec un point et en affectant une
valeur à un champ particulier. Le Listing 5-3 montre comment modifier la valeur
du champ `email` d’une instance `User` modifiable.

<Listing number="5-3" file-name="src/main.rs" caption="Modification de la valeur du champ `email` d’une instance `User`">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-03/src/main.rs:here}}
```

</Listing>

Notez que l’instance entière doit être modifiable ; Rust ne nous permet pas de
ne marquer que certains champs comme modifiables. Comme pour toute expression,
nous pouvons construire une nouvelle instance de la structure comme dernière
expression du corps d’une fonction afin de renvoyer implicitement cette
nouvelle instance.

Le Listing 5-4 montre une fonction `build_user` qui renvoie une instance
`User` avec l’adresse e-mail et le nom d’utilisateur donnés. Le champ `active`
prend la valeur `true`, et le champ `sign_in_count` prend la valeur `1`.

<Listing number="5-4" file-name="src/main.rs" caption="Une fonction `build_user` qui prend une adresse e-mail et un nom d’utilisateur et renvoie une instance `User`">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-04/src/main.rs:here}}
```

</Listing>

Il est logique de donner aux paramètres de la fonction le même nom que les
champs de la structure, mais devoir répéter les noms des champs `email` et
`username`, ainsi que les variables correspondantes, est un peu fastidieux. Si
la structure comportait davantage de champs, répéter chaque nom deviendrait
encore plus pénible. Heureusement, il existe une abréviation pratique !

<!-- Old headings. Do not remove or links may break. -->

<a id="using-the-field-init-shorthand-when-variables-and-fields-have-the-same-name"></a>

### Utiliser l’abréviation d’initialisation des champs

Comme les noms des paramètres et ceux des champs de la structure sont
exactement les mêmes dans le Listing 5-4, nous pouvons utiliser la syntaxe
d’_abréviation d’initialisation des champs_ pour réécrire `build_user` de façon
à ce qu’elle se comporte exactement de la même manière, sans répéter
`username` et `email`, comme indiqué dans le Listing 5-5.

<Listing number="5-5" file-name="src/main.rs" caption="Une fonction `build_user` qui utilise l’abréviation d’initialisation des champs, car les paramètres `username` et `email` portent le même nom que les champs de la structure">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-05/src/main.rs:here}}
```

</Listing>

Ici, nous créons une nouvelle instance de la structure `User`, qui possède un
champ nommé `email`. Nous voulons définir la valeur du champ `email` sur la
valeur du paramètre `email` de la fonction `build_user`. Comme le champ
`email` et le paramètre `email` portent le même nom, il suffit d’écrire
`email` au lieu de `email: email`.

<!-- Old headings. Do not remove or links may break. -->

<a id="creating-instances-from-other-instances-with-struct-update-syntax"></a>

### Créer des instances avec la syntaxe de mise à jour des structures

Il est souvent utile de créer une nouvelle instance d’une structure qui
reprend la plupart des valeurs d’une autre instance du même type, tout en en
modifiant certaines. Vous pouvez le faire avec la syntaxe de mise à jour des
structures.

Pour commencer, le Listing 5-6 montre comment créer une nouvelle instance
`User` dans `user2` de la manière habituelle, sans utiliser la syntaxe de mise
à jour. Nous définissons une nouvelle valeur pour `email`, mais utilisons par
ailleurs les mêmes valeurs que celles de `user1`, créée dans le Listing 5-2.

<Listing number="5-6" file-name="src/main.rs" caption="Création d’une nouvelle instance `User` en reprenant toutes les valeurs de `user1`, à l’exception d’une seule">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-06/src/main.rs:here}}
```

</Listing>

Avec la syntaxe de mise à jour des structures, nous pouvons obtenir le même
résultat avec moins de code, comme le montre le Listing 5-7. La syntaxe `..`
indique que les champs restants qui ne sont pas explicitement définis doivent
avoir la même valeur que les champs de l’instance indiquée.

<Listing number="5-7" file-name="src/main.rs" caption="Utilisation de la syntaxe de mise à jour des structures pour définir une nouvelle valeur `email` pour une instance `User` tout en reprenant les autres valeurs de `user1`">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-07/src/main.rs:here}}
```

</Listing>

Le code du Listing 5-7 crée aussi dans `user2` une instance dont la valeur de
`email` est différente, mais qui reprend de `user1` les mêmes valeurs pour les
champs `username`, `active` et `sign_in_count`. `..user1` doit apparaître en
dernier pour indiquer que tous les champs restants doivent prendre leurs
valeurs dans les champs correspondants de `user1`, mais nous pouvons choisir
de spécifier autant de champs que nous le souhaitons, dans n’importe quel
ordre, quel que soit l’ordre des champs dans la définition de la structure.

Notez que la syntaxe de mise à jour des structures utilise `=` comme une
affectation ; c’est parce qu’elle déplace les données, comme nous l’avons vu
dans la section [« Variables et données interagissent avec le déplacement »][move]<!-- ignore -->. Dans cet exemple, nous ne pouvons plus utiliser
`user1` après avoir créé `user2`, car la `String` du champ `username` de
`user1` a été déplacée dans `user2`. Si nous avions attribué de nouvelles
valeurs `String` à `email` et à `username` de `user2`, et n’avions donc utilisé
que les valeurs `active` et `sign_in_count` de `user1`, alors `user1` serait
toujours valide après la création de `user2`. `active` et `sign_in_count` sont
tous deux des types qui implémentent le trait `Copy`, donc le comportement
présenté dans la section [« Données stockées uniquement sur la pile : Copy »][copy]<!-- ignore --> s’appliquerait. Nous pouvons également encore utiliser
`user1.email` dans cet exemple, car sa valeur n’a pas été déplacée hors de
`user1`.

<!-- Old headings. Do not remove or links may break. -->

<a id="using-tuple-structs-without-named-fields-to-create-different-types"></a>

### Créer différents types avec des structures-tuples

Rust prend également en charge des structures qui ressemblent à des tuples,
appelées _structures-tuples_. Les structures-tuples bénéficient de la
signification apportée par le nom de la structure, mais leurs champs n’ont pas
de noms associés ; ils ont simplement des types. Les structures-tuples sont
utiles lorsque vous voulez donner un nom à l’ensemble du tuple et en faire un
type différent des autres tuples, ou lorsque nommer chaque champ comme dans
une structure classique serait verbeux ou redondant.

Pour définir une structure-tuple, commencez par le mot-clé `struct` et le nom
de la structure, suivis des types du tuple. Par exemple, nous définissons et
utilisons ici deux structures-tuples nommées `Color` et `Point` :

<Listing file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/no-listing-01-tuple-structs/src/main.rs}}
```

</Listing>

Notez que les valeurs `black` et `origin` sont de types différents, car elles
sont des instances de structures-tuples différentes. Chaque structure que vous
définissez constitue son propre type, même si les champs qu’elle contient
peuvent avoir les mêmes types. Par exemple, une fonction qui prend un paramètre
de type `Color` ne peut pas accepter un `Point` comme argument, même si les
deux types sont composés de trois valeurs `i32`. Par ailleurs, les instances
de structures-tuples sont similaires aux tuples : vous pouvez les décomposer
en leurs éléments individuels et utiliser un `.` suivi de l’indice pour
accéder à une valeur. Contrairement aux tuples, les structures-tuples vous
obligent à nommer le type de la structure lorsque vous les décomposez. Par
exemple, nous écririons `let Point(x, y, z) = origin;` pour décomposer les
valeurs du point `origin` en variables nommées `x`, `y` et `z`.

<!-- Old headings. Do not remove or links may break. -->

<a id="unit-like-structs-without-any-fields"></a>

### Définir des structures sans champs

Vous pouvez également définir des structures qui ne comportent aucun champ !
On les appelle des _structures unitaires_, car elles se comportent de manière
similaire à `()`, le type unité mentionné dans la section [« Le type tuple »][tuples]<!-- ignore -->. Les structures unitaires peuvent être utiles
lorsque vous devez implémenter un trait sur un type, mais que vous n’avez
aucune donnée à stocker dans le type lui-même. Nous aborderons les traits au
chapitre 10. Voici un exemple de déclaration et d’instanciation d’une structure
unitaire nommée `AlwaysEqual` :

<Listing file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/no-listing-04-unit-like-structs/src/main.rs}}
```

</Listing>

Pour définir `AlwaysEqual`, nous utilisons le mot-clé `struct`, le nom voulu,
puis un point-virgule. Pas besoin d’accolades ni de parenthèses ! Ensuite, nous
pouvons obtenir une instance de `AlwaysEqual` dans la variable `subject` de
manière similaire : en utilisant le nom que nous avons défini, sans accolades
ni parenthèses. Imaginez que nous implémentions plus tard un comportement pour
ce type, de sorte que chaque instance de `AlwaysEqual` soit toujours égale à
toute instance de n’importe quel autre type, par exemple afin d’obtenir un
résultat connu à des fins de test. Nous n’aurions besoin d’aucune donnée pour
implémenter ce comportement ! Vous verrez au chapitre 10 comment définir des
traits et les implémenter sur n’importe quel type, y compris les structures
unitaires.

> ### Propriété des données d’une structure
>
> Dans la définition de la structure `User` du Listing 5-1, nous avons utilisé
> le type possédé `String` plutôt que le type de tranche de chaîne `&str`.
> C’est un choix délibéré, car nous voulons que chaque instance de cette
> structure possède toutes ses données, et que ces données restent valides
> aussi longtemps que la structure entière est valide.
>
> Il est également possible pour les structures de stocker des références à
> des données appartenant à autre chose, mais cela nécessite d’utiliser des
> _durées de vie_, une fonctionnalité de Rust que nous aborderons au chapitre
> 10. Les durées de vie garantissent que les données référencées par une
> structure restent valides aussi longtemps que la structure. Supposons que
> vous essayiez de stocker une référence dans une structure sans spécifier de
> durée de vie, comme ci-dessous dans *src/main.rs* ; cela ne fonctionnera
> pas :
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
> Le compilateur signalera qu’il a besoin de spécificateurs de durée de vie :
>
> ```console
> $ cargo run
>    Compiling structs v0.1.0 (file:///projects/structs)
> error[E0106]: missing lifetime specifier
>  --> src/main.rs:3:15
>   |
> 3 |     username: &str,
>   |               ^ expected named lifetime parameter
>   |
> help: consider introducing a named lifetime parameter
>   |
> 1 ~ struct User<'a> {
> 2 |     active: bool,
> 3 ~     username: &'a str,
>   |
>
> error[E0106]: missing lifetime specifier
>  --> src/main.rs:4:12
>   |
> 4 |     email: &str,
>   |            ^ expected named lifetime parameter
>   |
> help: consider introducing a named lifetime parameter
>   |
> 1 ~ struct User<'a> {
> 2 |     active: bool,
> 3 |     username: &str,
> 4 ~     email: &'a str,
>   |
>
> For more information about this error, try `rustc --explain E0106`.
> error: could not compile `structs` (bin "structs") due to 2 previous errors
> ```
>
> Au chapitre 10, nous verrons comment corriger ces erreurs afin que vous
> puissiez stocker des références dans des structures. Pour l’instant, nous
> corrigerons ce genre d’erreurs en utilisant des types possédés comme `String`
> plutôt que des références comme `&str`.

<!-- manual-regeneration
for the error above
after running update-rustc.sh:
pbcopy < listings/ch05-using-structs-to-structure-related-data/no-listing-02-reference-in-struct/output.txt
paste above
add `> ` before every line -->

[tuples]: ch03-02-data-types.html#the-tuple-type
[move]: ch04-01-what-is-ownership.html#variables-and-data-interacting-with-move
[copy]: ch04-01-what-is-ownership.html#stack-only-data-copy