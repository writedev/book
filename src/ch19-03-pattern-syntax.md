## Syntax des motifs

Dans cette section, nous rassemblons toute la syntaxe valide dans les motifs et discutons de pourquoi et quand vous pourriez vouloir utiliser chacun d'eux.

### Correspondance des littéraux

Comme vous l'avez vu au chapitre 6, vous pouvez faire correspondre des motifs à des littéraux directement. Le code suivant donne quelques exemples :

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/no-listing-01-literals/src/main.rs:here}}
```

Ce code imprime `one` parce que la valeur de `x` est `1`. Cette syntaxe est utile lorsque vous voulez que votre code prenne une action si elle obtient une valeur concrète particulière.

### Correspondance des variables nommées

Les variables nommées sont des motifs irréfutables qui correspondent à n'importe quelle valeur, et nous les avons utilisées de nombreuses fois dans ce livre. Cependant, il y a une complication lorsque vous utilisez des variables nommées dans des expressions `match`, `if let` ou `while let`. Comme chacun de ces types d'expressions commence un nouveau scope, les variables déclarées comme faisant partie d'un motif à l'intérieur de ces expressions vont masquer celles ayant le même nom à l'extérieur des constructions, comme c'est le cas avec toutes les variables. Dans la liste 19-11, nous déclarons une variable nommée `x` avec la valeur `Some(5)` et une variable `y` avec la valeur `10`. Nous créons ensuite une expression `match` sur la valeur `x`. Regardez les motifs dans les bras du match et `println!` à la fin, et essayez de déterminer ce que le code va imprimer avant d'exécuter ce code ou de lire la suite.

<Listing number="19-11" file-name="src/main.rs" caption="Une expression `match` avec un bras qui introduit une nouvelle variable masquant une variable existante `y`">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-11/src/main.rs:here}}
```

</Listing>

Voyons ce qui se passe lorsque l'expression `match` s'exécute. Le motif dans le premier bras de match ne correspond pas à la valeur définie de `x`, donc le code continue.

Le motif dans le deuxième bras de match introduit une nouvelle variable nommée `y` qui correspondra à n'importe quelle valeur à l'intérieur d'une valeur `Some`. Comme nous sommes dans un nouveau scope à l'intérieur de l'expression `match`, cette nouvelle variable `y` n'est pas celle que nous avons déclarée au début avec la valeur `10`. Ce nouveau lien `y` correspondra à n'importe quelle valeur à l'intérieur d'un `Some`, qui est ce que nous avons dans `x`. Par conséquent, ce nouveau `y` se lie à la valeur interne du `Some` dans `x`. Cette valeur est `5`, donc l'expression pour ce bras s'exécute et imprime `Matched, y = 5`.

Si `x` avait été une valeur `None` au lieu de `Some(5)`, les motifs dans les deux premiers bras n'auraient pas correspondu, donc la valeur aurait correspondu à l'underscore. Nous n'avons pas introduit la variable `x` dans le motif du bras underscore, donc `x` dans l'expression est toujours l'`x` externe qui n'a pas été masqué. Dans ce cas hypothétique, le `match` imprimerait `Default case, x = None`.

Lorsque l'expression `match` est terminée, son scope se termine aussi, tout comme le scope de l'intérieur `y`. Le dernier `println!` produit `at the end: x = Some(5), y = 10`.

Pour créer une expression `match` qui compare les valeurs des `x` et `y` externes, plutôt que d'introduire une nouvelle variable qui masque l'existante `y`, nous devrions utiliser une garde de match conditionnelle à la place. Nous parlerons des gardes de match plus tard dans la section ["Ajout de conditionnelles avec des gardes de match"]( #adding-conditionals-with-match-guards)<!-- ignore -->.

### Correspondance de plusieurs motifs

Dans les expressions `match`, vous pouvez correspondre à plusieurs motifs en utilisant la syntaxe `|`, qui est l'opérateur _ou_ pour les motifs. Par exemple, dans le code suivant, nous faisons correspondre la valeur de `x` aux bras du match, dont le premier a une option _ou_, ce qui signifie que si la valeur de `x` correspond à l'une des valeurs de ce bras, le code de ce bras s'exécutera :

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/no-listing-02-multiple-patterns/src/main.rs:here}}
```

Ce code imprime `one or two`.

### Correspondance des intervalles de valeurs avec `..=`

La syntaxe `..=` permet de correspondre à une plage de valeurs inclusive. Dans le code suivant, lorsqu'un motif correspond à n'importe quelle des valeurs dans la plage donnée, ce bras s'exécutera :

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/no-listing-03-ranges/src/main.rs:here}}
```

Si `x` est `1`, `2`, `3`, `4` ou `5`, le premier bras correspondra. Cette syntaxe est plus pratique pour plusieurs valeurs de correspondance que d'utiliser l'opérateur `|` pour exprimer la même idée ; si nous devions utiliser `|`, nous devrions spécifier `1 | 2 | 3 | 4 | 5`. Spécifier une plage est beaucoup plus court, surtout si nous voulons correspondre, disons, à n'importe quel nombre entre 1 et 1 000 !

Le compilateur vérifie que la plage n'est pas vide au moment de la compilation, et parce que les seuls types pour lesquels Rust peut dire si une plage est vide ou non sont `char` et des valeurs numériques, les plages ne sont autorisées qu'avec des valeurs numériques ou `char`.

Voici un exemple utilisant des plages de valeurs `char` :

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/no-listing-04-ranges-of-char/src/main.rs:here}}
```

Rust peut savoir que `'c'` est dans la plage du premier motif et imprime `early ASCII letter`.

### Destructuration pour séparer les valeurs

Nous pouvons également utiliser des motifs pour destructurer des structures, des énumérations et des tuples afin d'utiliser différentes parties de ces valeurs. Passons en revue chaque valeur.

#### Structures

La liste 19-12 montre une structure `Point` avec deux champs, `x` et `y`, que nous pouvons séparer en utilisant un motif avec une instruction `let`.

<Listing number="19-12" file-name="src/main.rs" caption="Destructuration des champs d'une structure en variables séparées">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-12/src/main.rs}}
```

</Listing>

Ce code crée les variables `a` et `b` qui correspondent aux valeurs des champs `x` et `y` de la structure `p`. Cet exemple montre que les noms des variables dans le motif n'ont pas besoin de correspondre aux noms des champs de la structure. Cependant, il est courant de faire correspondre les noms de variables aux noms de champs pour faciliter la mémorisation des variables provenant de quels champs. En raison de cet usage commun, et parce que l'écriture `let Point { x: x, y: y } = p;` contient beaucoup de répétition, Rust a un raccourci pour les motifs qui correspondent aux champs des structures : vous devez seulement lister le nom du champ struct et les variables créées par le motif porteront les mêmes noms. La liste 19-13 se comporte de la même manière que le code de la liste 19-12, mais les variables créées dans le motif `let` sont `x` et `y` plutôt que `a` et `b`.

<Listing number="19-13" file-name="src/main.rs" caption="Destructuration des champs de structure en utilisant la syntaxe abrégée des champs de structure">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-13/src/main.rs}}
```

</Listing>

Ce code crée les variables `x` et `y` qui correspondent aux champs `x` et `y` de la variable `p`. Le résultat est que les variables `x` et `y` contiennent les valeurs de la structure `p`.

Nous pouvons également destructurer avec des valeurs littérales comme partie du motif de structure plutôt que de créer des variables pour tous les champs. Cela nous permet de tester certains champs pour des valeurs particulières tout en créant des variables pour destructurer les autres champs.

Dans la liste 19-14, nous avons une expression `match` qui sépare les valeurs `Point` en trois cas : des points qui se trouvent directement sur l'axe `x` (ce qui est vrai lorsque `y = 0`), sur l'axe `y` (`x = 0`), ou n'importe quel point qui n'est sur aucun des axes.

<Listing number="19-14" file-name="src/main.rs" caption="Destructuration et correspondance de valeurs littérales dans un seul motif">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-14/src/main.rs:here}}
```

</Listing>

Le premier bras correspondra à tout point qui se trouve sur l'axe `x` en spécifiant que le champ `y` correspond si sa valeur correspond au littéral `0`. Le motif crée toujours une variable `x` que nous pouvons utiliser dans le code de ce bras.

De même, le deuxième bras correspond à tout point sur l'axe `y` en spécifiant que le champ `x` correspond si sa valeur est `0` et crée une variable `y` pour la valeur du champ `y`. Le troisième bras ne spécifie aucun littéral, donc il correspond à tout autre `Point` et crée des variables pour les deux champs `x` et `y`.

Dans cet exemple, la valeur `p` correspond au deuxième bras grâce à `x` contenant un `0`, donc ce code va imprimer `On the y axis at 7`.

N'oubliez pas qu'une expression `match` arrête de vérifier des bras une fois qu'elle a trouvé le premier motif correspondant, donc même si `Point { x: 0, y: 0 }` est sur l'axe `x` et l'axe `y`, ce code imprimerait uniquement `On the x axis at 0`.

#### Énumérations

Nous avons destructuré des énumérations dans ce livre (par exemple, dans la liste 6-5 au chapitre 6), mais nous n'avons pas encore explicitement discuté que le motif pour destructurer une énumération correspond à la façon dont les données stockées dans l'énumération sont définies. À titre d'exemple, dans la liste 19-15, nous utilisons l'énumération `Message` de la liste 6-2 et écrivons un `match` avec des motifs qui vont destructurer chaque valeur interne.

<Listing number="19-15" file-name="src/main.rs" caption="Destructurer les variantes d'énumération qui contiennent différents types de valeurs">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-15/src/main.rs}}
```

</Listing>

Ce code imprimera `Change color to red 0, green 160, and blue 255`. Essayez de changer la valeur de `msg` pour voir le code des autres bras s'exécuter.

Pour des variantes d'énumération sans aucune donnée, comme `Message::Quit`, nous ne pouvons pas destructurer la valeur plus loin. Nous ne pouvons que correspondre à la valeur littérale `Message::Quit`, et aucune variable n'est dans ce motif.

Pour des variantes d'énumération de type struct, telles que `Message::Move`, nous pouvons utiliser un motif similaire à celui que nous spécifions pour faire correspondre des structures. Après le nom de la variante, nous plaçons des accolades et listons ensuite les champs avec des variables pour que nous puissions séparer les morceaux à utiliser dans le code de ce bras. Ici, nous utilisons la forme abrégée comme nous l'avons fait dans la liste 19-13.

Pour des variantes d'énumération de type tuple, comme `Message::Write` qui contient un tuple avec un élément et `Message::ChangeColor` qui contient un tuple avec trois éléments, le motif est similaire à celui que nous spécifions pour faire correspondre des tuples. Le nombre de variables dans le motif doit correspondre au nombre d'éléments dans la variante que nous faisons correspondre.

#### Structures et énumérations imbriquées

Jusqu'à présent, nos exemples ont tous correspondu à des structures ou des énumérations à un niveau de profondeur, mais la correspondance peut également fonctionner sur des éléments imbriqués ! Par exemple, nous pouvons refactoriser le code de la liste 19-15 pour prendre en charge les couleurs RGB et HSV dans le message `ChangeColor`, comme le montre la liste 19-16.

<Listing number="19-16" caption="Correspondance sur des énumérations imbriquées">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-16/src/main.rs}}
```

</Listing>

Le motif du premier bras dans l'expression `match` correspond à une variante d'énumération `Message::ChangeColor` qui contient une variante `Color::Rgb` ; ensuite, le motif se lie aux trois valeurs internes `i32`. Le motif du deuxième bras correspond également à une variante d'énumération `Message::ChangeColor`, mais l'énumération interne correspond cette fois à `Color::Hsv`. Nous pouvons spécifier ces conditions complexes dans une seule expression `match`, même si deux énumérations sont impliquées.

#### Destructuration de structures et tuples

Nous pouvons mélanger, assortir et imbriquer des motifs de destructuration de manière encore plus complexe. L'exemple suivant montre une destructuration compliquée où nous imbriquons des structures et des tuples à l'intérieur d'un tuple et destructurons toutes les valeurs primitives :

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/no-listing-05-destructuring-structs-and-tuples/src/main.rs:here}}
```

Ce code nous permet de décomposer des types complexes en leurs parties constitutives afin que nous puissions utiliser les valeurs qui nous intéressent séparément.

La destructuration avec des motifs est un moyen pratique d'utiliser des morceaux de valeurs, telles que la valeur de chaque champ d'une structure, séparément les unes des autres.

### Ignorer des valeurs dans un motif

Vous avez vu qu'il est parfois utile d'ignorer des valeurs dans un motif, comme dans le dernier bras d'un `match`, pour obtenir un catch-all qui ne fait en réalité rien mais tient compte de toutes les valeurs possibles restantes. Il existe plusieurs moyens d'ignorer des valeurs entières ou des parties de valeurs dans un motif : en utilisant le motif `_` (que vous avez vu), en utilisant le motif `_` dans un autre motif, en utilisant un nom qui commence par un underscore, ou en utilisant `..` pour ignorer les parties restantes d'une valeur. Explorons comment et pourquoi utiliser chacun de ces motifs.

#### Une valeur entière avec `_`

Nous avons utilisé l'underscore comme motif générique qui correspondra à n'importe quelle valeur mais ne se liera pas à la valeur. Ceci est particulièrement utile comme le dernier bras d'une expression `match`, mais nous pouvons également l'utiliser dans n'importe quel motif, y compris les paramètres de fonction, comme le montre la liste 19-17.

<Listing number="19-17" file-name="src/main.rs" caption="Utilisation de `_` dans une signature de fonction">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-17/src/main.rs}}
```

</Listing>

Ce code ignorera complètement la valeur `3` passée comme premier argument, et imprimera `This code only uses the y parameter: 4`.

Dans la plupart des cas où vous n'avez plus besoin d'un paramètre de fonction particulier, vous changeriez la signature afin de ne pas inclure le paramètre inutilisé. Ignorer un paramètre de fonction peut être particulièrement utile dans des cas où, par exemple, vous mettez en œuvre un trait où vous avez besoin d'une certaine signature de type mais le corps de la fonction dans votre implémentation n'a pas besoin d'un des paramètres. Vous évitez alors d'obtenir un avertissement du compilateur au sujet de paramètres de fonction inutilisés, comme vous le feriez si vous utilisiez un nom à la place.

#### Des parties d'une valeur avec un `_` imbriqué

Nous pouvons également utiliser `_` à l'intérieur d'un autre motif pour ignorer juste une partie d'une valeur, par exemple, lorsque nous voulons tester seulement une partie d'une valeur mais que nous n'avons pas besoin des autres parties dans le code correspondant que nous voulons exécuter. La liste 19-18 montre un code responsable de la gestion de la valeur d'un paramètre. Les exigences commerciales stipulent que l'utilisateur ne doit pas être autorisé à remplacer une personnalisation existante d'un paramètre mais peut le désactiver et lui donner une valeur si elle est actuellement désactivée.

<Listing number="19-18" caption="Utilisation d'un underscore dans des motifs qui correspondent aux variantes `Some` lorsque nous n'avons pas besoin d'utiliser la valeur à l'intérieur du `Some`">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-18/src/main.rs:here}}
```

</Listing>

Ce code imprimera `Can't overwrite an existing customized value` puis `setting is Some(5)`. Dans le premier bras de correspondance, nous n'avons pas besoin de faire correspondre ou d'utiliser les valeurs à l'intérieur des deux variantes `Some`, mais nous devons tester le cas lorsque `setting_value` et `new_setting_value` sont la variante `Some`. Dans ce cas, nous imprimons la raison pour laquelle `setting_value` ne change pas, et il ne sera pas modifié.

Dans tous les autres cas (si `setting_value` ou `new_setting_value` est `None`) exprimés par le motif `_` dans le deuxième bras, nous voulons permettre à `new_setting_value` de devenir `setting_value`.

Nous pouvons également utiliser des underscores en plusieurs endroits au sein d'un même motif pour ignorer des valeurs particulières. La liste 19-19 montre un exemple d'ignorance du deuxième et du quatrième éléments dans un tuple de cinq éléments.

<Listing number="19-19" caption="Ignorer plusieurs parties d'un tuple">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-19/src/main.rs:here}}
```

</Listing>

Ce code imprimera `Some numbers: 2, 8, 32`, et les valeurs `4` et `16` seront ignorées.

#### Une variable inutilisée en commençant son nom par `_`

Si vous créez une variable mais ne l'utilisez nulle part, Rust émettra généralement un avertissement car une variable inutilisée pourrait être un bug. Cependant, il est parfois utile de pouvoir créer une variable que vous n'utiliserez pas, par exemple lorsque vous prototypes ou que vous commencez tout juste un projet. Dans cette situation, vous pouvez dire à Rust de ne pas vous avertir au sujet de la variable inutilisée en commençant le nom de la variable par un underscore. Dans la liste 19-20, nous créons deux variables inutilisées, mais lorsque nous compilons ce code, nous devrions seulement obtenir un avertissement au sujet d'une d'elles.

<Listing number="19-20" file-name="src/main.rs" caption="Commencer le nom d'une variable par un underscore pour éviter d'obtenir des avertissements concernant des variables inutilisées">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-20/src/main.rs}}
```

</Listing>

Ici, nous obtenons un avertissement sur le fait de ne pas utiliser la variable `y`, mais nous ne recevons pas d'avertissement sur l'absence d'utilisation de `_x`.

Notez qu'il y a une subtilité dans la différence entre utiliser seulement `_` et utiliser un nom commençant par un underscore. La syntaxe `_x` lie toujours la valeur à la variable, alors que `_` ne lie pas du tout. Pour montrer un cas où cette distinction est importante, la liste 19-21 nous donnera une erreur.

<Listing number="19-21" caption="Une variable inutilisée commençant par un underscore lie toujours la valeur, ce qui peut prendre possession de la valeur.">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-21/src/main.rs:here}}
```

</Listing>

Nous recevrons une erreur car la valeur `s` sera toujours déplacée dans `_s`, ce qui nous empêche d'utiliser `s` à nouveau. Cependant, en utilisant l'underscore par lui-même ne lie jamais la valeur. La liste 19-22 se compilera sans aucune erreur car `s` n'est pas déplacé dans `_`.

<Listing number="19-22" caption="Utilisation d'un underscore ne lie pas la valeur.">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-22/src/main.rs:here}}
```

</Listing>

Ce code fonctionne très bien car nous ne lierons jamais `s` à quoi que ce soit ; il n'est pas déplacé.

#### Parties restantes d'une valeur avec `..`

Avec les valeurs qui ont de nombreuses parties, nous pouvons utiliser la syntaxe `..` pour utiliser des parties spécifiques et ignorer le reste, évitant ainsi d'avoir à lister des underscores pour chaque valeur ignorée. Le motif `..` ignore toutes les parties d'une valeur que nous n'avons pas explicitement correspondues dans le reste du motif. Dans la liste 19-23, nous avons une structure `Point` qui contient une coordonnée dans un espace tridimensionnel. Dans l'expression `match`, nous voulons uniquement opérer sur la coordonnée `x` et ignorer les valeurs dans les champs `y` et `z`.

<Listing number="19-23" caption="Ignorer tous les champs d'un `Point` sauf `x` en utilisant `..`">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-23/src/main.rs:here}}
```

</Listing>

Nous listons la valeur `x` puis incluons simplement le motif `..`. C'est plus rapide que de devoir lister `y: _` et `z: _`, particulièrement lorsque nous travaillons avec des structures qui ont de nombreux champs dans des situations où seulement un ou deux champs sont pertinents.

La syntaxe `..` s'étendra à autant de valeurs que nécessaire. La liste 19-24 montre comment utiliser `..` avec un tuple.

<Listing number="19-24" file-name="src/main.rs" caption="Correspondre uniquement aux première et dernière valeurs d'un tuple tout en ignorant toutes les autres valeurs">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-24/src/main.rs}}
```

</Listing>

Dans ce code, les première et dernière valeurs sont correspondantes avec `first` et `last`. Le `..` correspondra et ignorera tout ce qui se trouve au milieu.

Cependant, l'utilisation de `..` doit être sans ambiguïté. S'il n'est pas clair quelles valeurs doivent être correspondantes et lesquelles doivent être ignorées, Rust nous donnera une erreur. La liste 19-25 montre un exemple d'utilisation ambiguë de `..`, donc il ne se compilera pas.

<Listing number="19-25" file-name="src/main.rs" caption="Une tentative d'utilisation de `..` de manière ambiguë">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-25/src/main.rs}}
```

</Listing>

Lors de la compilation de cet exemple, nous avons cette erreur :

```console
{{#include ../listings/ch19-patterns-and-matching/listing-19-25/output.txt}}
```

Il est impossible pour Rust de déterminer combien de valeurs dans le tuple ignorer avant de faire correspondre une valeur avec `second` et ensuite combien d'autres valeurs ignorer par la suite. Ce code pourrait signifier que nous voulons ignorer `2`, lier `second` à `4`, puis ignorer `8`, `16`, et `32`; ou que nous voulons ignorer `2` et `4`, lier `second` à `8`, puis ignorer `16` et `32`; et ainsi de suite. Le nom de la variable `second` ne signifie rien de spécial pour Rust, donc nous obtenons une erreur de compilation car l'utilisation de `..` à deux endroits de cette manière est ambiguë.

### Ajout de conditionnelles avec des gardes de match

Une _garde de match_ est une condition `if` supplémentaire, spécifiée après le motif dans un bras d'un `match`, qui doit également correspondre pour que ce bras soit choisi. Les gardes de match sont utiles pour exprimer des idées plus complexes qu'un motif seul ne permet. Notez cependant qu'elles ne sont disponibles que dans les expressions `match`, pas dans les expressions `if let` ou `while let`.

La condition peut utiliser des variables créées dans le motif. La liste 19-26 montre un `match` où le premier bras a le motif `Some(x)` et a également une garde de match de `if x % 2 == 0` (ce qui sera `true` si le nombre est pair).

<Listing number="19-26" caption="Ajout d'une garde de match à un motif">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-26/src/main.rs:here}}
```

</Listing>

Cet exemple imprimera `The number 4 is even`. Lorsque `num` est comparé au motif dans le premier bras, il correspond parce que `Some(4)` correspond à `Some(x)`. Ensuite, la garde de match vérifie si le reste de la division de `x` par 2 est égal à 0, et comme c'est le cas, le premier bras est sélectionné.

Si `num` avait été `Some(5)` à la place, la garde de match dans le premier bras aurait été `false` parce que le reste de 5 divisé par 2 est 1, ce qui n'est pas égal à 0. Rust irait alors au deuxième bras, qui correspondrait parce que le deuxième bras n'a pas de garde de match et correspond donc à n'importe quelle variante `Some`.

Il n'y a aucun moyen d'exprimer la condition `if x % 2 == 0` dans un motif, donc la garde de match nous donne la possibilité d'exprimer cette logique. L'inconvénient de cette expressivité supplémentaire est que le compilateur ne tente pas de vérifier l'exhaustivité lorsque des expressions de garde de match sont impliquées.

Lorsque nous avons discuté de la liste 19-11, nous avons mentionné que nous pourrions utiliser des gardes de match pour résoudre notre problème d'ombrage de motif. Rappelez-vous que nous avons créé une nouvelle variable à l'intérieur du motif dans l'expression `match` au lieu d'utiliser la variable à l'extérieur du `match`. Cette nouvelle variable signifiait que nous ne pouvions pas tester la valeur de la variable externe. La liste 19-27 montre comment nous pouvons utiliser une garde de match pour résoudre ce problème.

<Listing number="19-27" caption="Utiliser une garde de match pour tester l'égalité avec une variable externe">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-27/src/main.rs}}
```

</Listing>

Ce code imprimera maintenant `Default case, x = Some(5)`. Le motif dans le deuxième bras de correspondance n'introduit pas une nouvelle variable `y` qui masquera l'`y` externe, ce qui signifie que nous pouvons utiliser le `y` externe dans la garde de match. Au lieu de spécifier le motif comme `Some(y)`, ce qui aurait masqué `y` externe, nous spécifions `Some(n)`. Cela crée une nouvelle variable `n` qui ne masque rien parce qu'il n'y a pas de variable `n` à l'extérieur du `match`.

La garde de match `if n == y` n'est pas un motif et n'introduit donc pas de nouvelles variables. Ce `y` _est_ le `y` externe plutôt qu'un nouveau `y` le masquant, et nous pouvons rechercher une valeur qui a la même valeur que l'`y` externe en comparant `n` à `y`.

Vous pouvez également utiliser l'opérateur _ou_ `|` dans une garde de match pour spécifier plusieurs motifs ; la condition de la garde de match s'appliquera à tous les motifs. La liste 19-28 montre la priorité lorsqu'on combine un motif qui utilise `|` avec une garde de match. L'élément important de cet exemple est que la garde de match `if y` s'applique à `4`, `5`, _et_ `6`, même si cela semble que `if y` ne s'applique qu'à `6`.

<Listing number="19-28" caption="Combinaison de plusieurs motifs avec une garde de match">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-28/src/main.rs:here}}
```

</Listing>

La condition de correspondance indique que le bras ne correspond que si la valeur de `x` est égale à `4`, `5` ou `6` _et_ si `y` est `true`. Lorsque ce code s'exécute, le motif du premier bras correspond parce que `x` est `4`, mais la garde de match `if y` est `false`, donc le premier bras n'est pas choisi. Le code passe ensuite au deuxième bras, qui correspond, et ce programme imprime `no`. La raison en est que la condition `if` s'applique à l'ensemble du motif `4 | 5 | 6`, et non seulement à la dernière valeur `6`. En d'autres termes, la priorité d'une garde de match par rapport à un motif se comporte comme ceci :

```text
(4 | 5 | 6) if y => ...
```

plutôt que ceci :

```text
4 | 5 | (6 if y) => ...
```

Après avoir exécuté le code, le comportement de priorité est évident : si la garde de match était appliquée uniquement à la valeur finale de la liste des valeurs spécifiées en utilisant l'opérateur `|`, le bras aurait correspondu, et le programme aurait imprimé `yes`.

### Utilisation des liaisons `@`

L'opérateur _at_ `@` nous permet de créer une variable qui contient une valeur au même moment que nous testons cette valeur pour une correspondance de motif. Dans la liste 19-29, nous voulons tester que le champ `id` d'un `Message::Hello` est dans la plage `3..=7`. Nous souhaitons également lier la valeur à la variable `id` afin de pouvoir l'utiliser dans le code associé au bras.

<Listing number="19-29" caption="Utilisation de `@` pour lier une valeur dans un motif tout en la testant">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-29/src/main.rs:here}}
```

</Listing>

Cet exemple imprimera `Found an id in range: 5`. En spécifiant `id @` avant la plage `3..=7`, nous capturons n'importe quelle valeur correspondant à la plage dans une variable nommée `id` tout en testant que la valeur correspond au motif de la plage.

Dans le deuxième bras, où nous avons seulement une plage spécifiée dans le motif, le code associé à ce bras n'a pas de variable contenant la valeur réelle du champ `id`. La valeur du champ `id` aurait pu être 10, 11 ou 12, mais le code qui accompagne ce motif ne sait pas laquelle c'est. Le code du motif n'est pas capable d'utiliser la valeur du champ `id` parce que nous n'avons pas sauvegardé la valeur `id` dans une variable.

Dans le dernier bras, où nous avons spécifié une variable sans plage, nous avons la valeur disponible à utiliser dans le code du bras dans une variable nommée `id`. La raison en est que nous avons utilisé la syntaxe abrégée du champ struct. Mais nous n'avons appliqué aucun test à la valeur du champ `id` dans ce bras, comme nous l'avons fait avec les deux premiers bras : n'importe quelle valeur correspondrait à ce motif.

L'utilisation de `@` nous permet de tester une valeur et de l'enregistrer dans une variable dans un motif.

## Résumé

Les motifs de Rust sont très utiles pour faire la distinction entre différents types de données. Lorsqu'ils sont utilisés dans des expressions `match`, Rust s'assure que vos motifs couvrent toutes les valeurs possibles, sinon votre programme ne se compilera pas. Les motifs dans les déclarations `let` et les paramètres de fonction rendent ces constructions plus utiles, permettant la destructuration des valeurs en plus petites parties et l'attribution de ces parties à des variables. Nous pouvons créer des motifs simples ou complexes pour répondre à nos besoins.

Ensuite, pour l'avant-dernier chapitre du livre, nous examinerons certains aspects avancés de divers fonctionnalités de Rust.