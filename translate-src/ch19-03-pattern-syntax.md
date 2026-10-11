## Syntaxe des motifs

Dans cette section, nous rassemblons toute la syntaxe valide dans les motifs et expliquons pourquoi et quand vous pourriez vouloir utiliser chacune de ses formes.

### Correspondance avec des littéraux

Comme vous l’avez vu au chapitre 6, vous pouvez directement faire correspondre des motifs à des littéraux. Le code suivant en donne quelques exemples :

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/no-listing-01-literals/src/main.rs:here}}
```

Ce code affiche `one` parce que la valeur de `x` est `1`. Cette syntaxe est utile lorsque vous voulez que votre code effectue une action s’il reçoit une valeur concrète particulière.

### Correspondance avec des variables nommées

Les variables nommées sont des motifs irréfutables qui correspondent à n’importe quelle valeur, et nous en avons utilisé de nombreuses fois dans ce livre. Toutefois, il y a une complication lorsque vous utilisez des variables nommées dans des expressions `match`, `if let` ou `while let`. Comme chacun de ces types d’expressions crée une nouvelle portée, les variables déclarées dans un motif au sein de ces expressions masquent celles qui portent le même nom en dehors de ces constructions, comme c’est le cas pour toutes les variables. Dans la liste 19-11, nous déclarons une variable nommée `x` dont la valeur est `Some(5)` et une variable `y` dont la valeur est `10`. Nous créons ensuite une expression `match` sur la valeur de `x`. Examinez les motifs dans les bras de `match` et le `println!` à la fin, puis essayez de déterminer ce que le code affichera avant de l’exécuter ou de poursuivre votre lecture.

<Listing number="19-11" file-name="src/main.rs" caption="Une expression `match` avec un bras qui introduit une nouvelle variable masquant une variable `y` existante">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-11/src/main.rs:here}}
```

</Listing>

Voyons ce qui se passe lors de l’exécution de l’expression `match`. Le motif du premier bras ne correspond pas à la valeur de `x`, donc le code continue.

Le motif du deuxième bras introduit une nouvelle variable nommée `y`, qui correspondra à n’importe quelle valeur contenue dans une valeur `Some`. Comme nous sommes dans une nouvelle portée à l’intérieur de l’expression `match`, il s’agit d’une nouvelle variable `y`, et non de la variable `y` déclarée au début avec la valeur `10`. Cette nouvelle liaison `y` correspondra à n’importe quelle valeur contenue dans un `Some`, ce qui est le cas de `x`. Par conséquent, cette nouvelle liaison `y` prend la valeur interne du `Some` de `x`. Cette valeur est `5`, donc l’expression de ce bras s’exécute et affiche `Matched, y = 5`.

Si `x` avait été une valeur `None` plutôt que `Some(5)`, les motifs des deux premiers bras n’auraient pas correspondu, et la valeur aurait correspondu au trait de soulignement. Nous n’avons pas introduit la variable `x` dans le motif du bras avec le trait de soulignement, donc `x` dans l’expression désigne toujours la variable `x` externe, qui n’a pas été masquée. Dans ce cas hypothétique, `match` afficherait `Default case, x = None`.

Lorsque l’expression `match` se termine, sa portée prend fin, tout comme celle du `y` interne. Le dernier `println!` affiche `at the end: x = Some(5), y = 10`.

Pour créer une expression `match` qui compare les valeurs du `x` et du `y` externes, plutôt que d’introduire une nouvelle variable masquant la variable `y` existante, nous devrions utiliser une condition de garde de motif. Nous parlerons des gardes de motif plus loin, dans la section [« Ajouter des conditions avec les gardes de motif »](#adding-conditionals-with-match-guards)<!-- ignore -->.

<!-- Old headings. Do not remove or links may break. -->
<a id="multiple-patterns"></a>

### Correspondance avec plusieurs motifs

Dans les expressions `match`, vous pouvez faire correspondre plusieurs motifs à l’aide de la syntaxe `|`, qui est l’opérateur _ou_ des motifs. Par exemple, dans le code suivant, nous comparons la valeur de `x` aux bras de `match`. Le premier comporte une option _ou_, ce qui signifie que si la valeur de `x` correspond à l’une ou l’autre des valeurs de ce bras, son code s’exécutera :

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/no-listing-02-multiple-patterns/src/main.rs:here}}
```

Ce code affiche `one or two`.

### Correspondance avec des plages de valeurs grâce à `..=`

La syntaxe `..=` permet de faire correspondre une plage de valeurs inclusive. Dans le code suivant, si un motif correspond à l’une des valeurs de la plage donnée, son bras s’exécute :

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/no-listing-03-ranges/src/main.rs:here}}
```

Si `x` vaut `1`, `2`, `3`, `4` ou `5`, le premier bras correspondra. Cette syntaxe est plus pratique que l’opérateur `|` pour exprimer la même idée avec plusieurs valeurs à faire correspondre ; avec `|`, il faudrait écrire `1 | 2 | 3 | 4 | 5`. Une plage est beaucoup plus concise, surtout si nous voulons faire correspondre, par exemple, n’importe quel nombre entre 1 et 1 000 !

Le compilateur vérifie à la compilation que la plage n’est pas vide. Comme les seuls types pour lesquels Rust peut déterminer si une plage est vide sont `char` et les types numériques, les plages ne sont autorisées qu’avec des valeurs numériques ou de type `char`.

Voici un exemple utilisant des plages de valeurs `char` :

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/no-listing-04-ranges-of-char/src/main.rs:here}}
```

Rust peut déterminer que `'c'` se trouve dans la plage du premier motif et affiche `early ASCII letter`.

### Déstructurer pour décomposer des valeurs

Nous pouvons également utiliser des motifs pour déstructurer des structs, des enums et des tuples afin d’utiliser différentes parties de ces valeurs. Examinons chacun de ces types de valeurs.

<!-- Old headings. Do not remove or links may break. -->

<a id="destructuring-structs"></a>

#### Structs

La liste 19-12 présente un struct `Point` avec deux champs, `x` et `y`, que nous pouvons décomposer à l’aide d’un motif dans une instruction `let`.

<Listing number="19-12" file-name="src/main.rs" caption="Déstructurer les champs d’un struct en variables distinctes">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-12/src/main.rs}}
```

</Listing>

Ce code crée les variables `a` et `b`, qui correspondent aux valeurs des champs `x` et `y` du struct `p`. Cet exemple montre que les noms des variables dans le motif n’ont pas besoin de correspondre aux noms des champs du struct. Toutefois, il est courant de faire correspondre les noms des variables à ceux des champs pour mieux se souvenir de quels champs proviennent les variables. En raison de cet usage courant, et parce que l’écriture de `let Point { x: x, y: y } = p;` comporte beaucoup de répétitions, Rust propose une syntaxe abrégée pour les motifs qui correspondent aux champs d’un struct : il suffit d’indiquer le nom du champ, et les variables créées à partir du motif porteront les mêmes noms. La liste 19-13 se comporte comme le code de la liste 19-12, mais les variables créées dans le motif `let` sont `x` et `y` plutôt que `a` et `b`.

<Listing number="19-13" file-name="src/main.rs" caption="Déstructurer les champs d’un struct à l’aide de la syntaxe abrégée des champs">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-13/src/main.rs}}
```

</Listing>

Ce code crée les variables `x` et `y`, qui correspondent aux champs `x` et `y` de la variable `p`. Ainsi, les variables `x` et `y` contiennent les valeurs du struct `p`.

Nous pouvons également déstructurer en utilisant des valeurs littérales dans le motif du struct, plutôt que de créer des variables pour tous les champs. Cela nous permet de vérifier que certains champs ont des valeurs particulières tout en créant des variables pour déstructurer les autres champs.

Dans la liste 19-14, nous avons une expression `match` qui répartit les valeurs `Point` en trois cas : les points situés directement sur l’axe `x` (c’est-à-dire lorsque `y = 0`), sur l’axe `y` (`x = 0`) ou sur aucun des deux axes.

<Listing number="19-14" file-name="src/main.rs" caption="Déstructurer et faire correspondre des valeurs littérales dans un même motif">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-14/src/main.rs:here}}
```

</Listing>

Le premier bras correspondra à tout point situé sur l’axe `x`, en indiquant que le champ `y` correspond si sa valeur correspond au littéral `0`. Le motif crée tout de même une variable `x` que nous pouvons utiliser dans le code de ce bras.

De la même façon, le deuxième bras correspond à tout point situé sur l’axe `y`, en indiquant que le champ `x` correspond si sa valeur est `0`, et crée une variable `y` pour la valeur du champ `y`. Le troisième bras ne précise aucun littéral : il correspond donc à tout autre `Point` et crée des variables pour les champs `x` et `y`.

Dans cet exemple, la valeur `p` correspond au deuxième bras puisque `x` contient un `0` ; ce code affichera donc `On the y axis at 7`.

N’oubliez pas qu’une expression `match` cesse d’examiner les bras dès qu’elle a trouvé le premier motif correspondant. Ainsi, même si `Point { x: 0, y: 0 }` se trouve à la fois sur l’axe `x` et sur l’axe `y`, ce code n’afficherait que `On the x axis at 0`.

<!-- Old headings. Do not remove or links may break. -->

<a id="destructuring-enums"></a>

#### Enums

Nous avons déstructuré des enums dans ce livre (par exemple, dans la liste 6-5 du chapitre 6), mais nous n’avons pas encore expliqué explicitement que le motif utilisé pour déstructurer un enum correspond à la façon dont les données qu’il contient sont définies. Par exemple, dans la liste 19-15, nous utilisons l’enum `Message` de la liste 6-2 et écrivons une expression `match` avec des motifs qui déstructurent chaque valeur interne.

<Listing number="19-15" file-name="src/main.rs" caption="Déstructurer des variantes d’enum contenant différents types de valeurs">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-15/src/main.rs}}
```

</Listing>

Ce code affichera `Change color to red 0, green 160, and blue 255`. Essayez de modifier la valeur de `msg` pour voir le code des autres bras s’exécuter.

Pour les variantes d’enum sans données, comme `Message::Quit`, nous ne pouvons pas déstructurer davantage la valeur. Nous pouvons seulement faire correspondre la valeur littérale `Message::Quit`, et ce motif ne contient aucune variable.

Pour les variantes d’enum semblables à des structs, comme `Message::Move`, nous pouvons utiliser un motif similaire à celui que nous utilisons pour faire correspondre des structs. Après le nom de la variante, nous plaçons des accolades, puis nous listons les champs avec des variables afin de décomposer les éléments à utiliser dans le code de ce bras. Ici, nous utilisons la forme abrégée, comme dans la liste 19-13.

Pour les variantes d’enum semblables à des tuples, comme `Message::Write` qui contient un tuple avec un élément, et `Message::ChangeColor` qui contient un tuple avec trois éléments, le motif est similaire à celui utilisé pour faire correspondre des tuples. Le nombre de variables dans le motif doit correspondre au nombre d’éléments de la variante que nous comparons.

<!-- Old headings. Do not remove or links may break. -->

<a id="destructuring-nested-structs-and-enums"></a>

#### Structs et enums imbriqués

Jusqu’ici, tous nos exemples faisaient correspondre des structs ou des enums imbriqués sur un seul niveau, mais la correspondance peut aussi s’appliquer à des éléments imbriqués ! Par exemple, nous pouvons refactoriser le code de la liste 19-15 pour prendre en charge les couleurs RGB et HSV dans le message `ChangeColor`, comme le montre la liste 19-16.

<Listing number="19-16" caption="Faire correspondre des enums imbriqués">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-16/src/main.rs}}
```

</Listing>

Le motif du premier bras de l’expression `match` correspond à une variante `Message::ChangeColor` qui contient une variante `Color::Rgb` ; le motif lie ensuite les trois valeurs `i32` internes. Le motif du deuxième bras correspond également à une variante `Message::ChangeColor`, mais l’enum interne correspond plutôt à `Color::Hsv`. Nous pouvons indiquer ces conditions complexes dans une seule expression `match`, même si deux enums sont impliqués.

<!-- Old headings. Do not remove or links may break. -->

<a id="destructuring-structs-and-tuples"></a>

#### Structs et tuples

Nous pouvons combiner, faire correspondre et imbriquer des motifs de déstructuration de façons encore plus complexes. L’exemple suivant montre une déstructuration compliquée dans laquelle nous imbriquons des structs et des tuples au sein d’un tuple et déstructurons toutes les valeurs primitives :

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/no-listing-05-destructuring-structs-and-tuples/src/main.rs:here}}
```

Ce code nous permet de décomposer des types complexes en leurs éléments constitutifs, afin de pouvoir utiliser séparément les valeurs qui nous intéressent.

La déstructuration à l’aide de motifs est un moyen pratique d’utiliser séparément des parties de valeurs, comme la valeur de chaque champ d’un struct.

### Ignorer des valeurs dans un motif

Vous avez vu qu’il est parfois utile d’ignorer des valeurs dans un motif, par exemple dans le dernier bras d’une expression `match`, pour créer un motif fourre-tout qui ne fait rien, mais prend en compte toutes les autres valeurs possibles. Il existe plusieurs façons d’ignorer des valeurs entières ou certaines parties de valeurs dans un motif : utiliser le motif `_` (que vous avez déjà vu), utiliser le motif `_` dans un autre motif, utiliser un nom commençant par un trait de soulignement, ou utiliser `..` pour ignorer les éléments restants d’une valeur. Voyons comment et pourquoi utiliser chacune de ces formes.

<!-- Old headings. Do not remove or links may break. -->

<a id="ignoring-an-entire-value-with-_"></a>

#### Une valeur entière avec `_`

Nous avons utilisé le trait de soulignement comme motif joker, qui correspond à n’importe quelle valeur sans la lier. Cela est particulièrement utile comme dernier bras d’une expression `match`, mais nous pouvons aussi l’utiliser dans n’importe quel motif, y compris dans les paramètres de fonctions, comme le montre la liste 19-17.

<Listing number="19-17" file-name="src/main.rs" caption="Utiliser `_` dans la signature d’une fonction">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-17/src/main.rs}}
```

</Listing>

Ce code ignore complètement la valeur `3` passée comme premier argument et affiche `This code only uses the y parameter: 4`.

Dans la plupart des cas, lorsque vous n’avez plus besoin d’un paramètre particulier d’une fonction, vous devriez modifier sa signature pour qu’elle n’inclue plus ce paramètre inutilisé. Ignorer un paramètre de fonction peut être particulièrement utile, par exemple, lorsque vous implémentez un trait qui exige une signature de type précise, mais que le corps de la fonction dans votre implémentation n’a pas besoin de l’un des paramètres. Vous évitez ainsi de recevoir un avertissement du compilateur concernant les paramètres inutilisés, contrairement à ce qui se passerait si vous utilisiez un nom.

<!-- Old headings. Do not remove or links may break. -->

<a id="ignoring-parts-of-a-value-with-a-nested-_"></a>

#### Des parties d’une valeur avec un `_` imbriqué

Nous pouvons également utiliser `_` dans un autre motif pour ignorer seulement une partie d’une valeur, par exemple lorsque nous voulons vérifier une partie d’une valeur, mais que les autres parties ne nous sont pas utiles dans le code correspondant. La liste 19-18 présente du code qui gère la valeur d’un paramètre. Les exigences métier sont les suivantes : l’utilisateur ne doit pas pouvoir remplacer une personnalisation existante d’un paramètre, mais doit pouvoir annuler le paramètre et lui attribuer une valeur s’il n’est pas encore défini.

<Listing number="19-18" caption="Utiliser un trait de soulignement dans des motifs qui correspondent à des variantes `Some` lorsque la valeur contenue dans `Some` ne nous est pas utile">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-18/src/main.rs:here}}
```

</Listing>

Ce code affiche `Can't overwrite an existing customized value`, puis `setting is Some(5)`. Dans le premier bras de `match`, nous n’avons pas besoin de faire correspondre ou d’utiliser les valeurs contenues dans l’une ou l’autre des variantes `Some`, mais nous devons vérifier que `setting_value` et `new_setting_value` sont des variantes `Some`. Dans ce cas, nous affichons la raison pour laquelle `setting_value` n’est pas modifiée.

Dans tous les autres cas (si `setting_value` ou `new_setting_value` vaut `None`), représentés par le motif `_` dans le deuxième bras, nous voulons que `new_setting_value` devienne `setting_value`.

Nous pouvons également utiliser des traits de soulignement à plusieurs endroits dans un même motif pour ignorer certaines valeurs. La liste 19-19 présente un exemple où les deuxième et quatrième valeurs d’un tuple de cinq éléments sont ignorées.

<Listing number="19-19" caption="Ignorer plusieurs éléments d’un tuple">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-19/src/main.rs:here}}
```

</Listing>

Ce code affiche `Some numbers: 2, 8, 32`, et les valeurs `4` et `16` sont ignorées.

<!-- Old headings. Do not remove or links may break. -->

<a id="ignoring-an-unused-variable-by-starting-its-name-with-_"></a>

#### Une variable inutilisée dont le nom commence par `_`

Si vous créez une variable sans l’utiliser, Rust émet généralement un avertissement, car une variable inutilisée pourrait signaler un bug. Toutefois, il est parfois utile de pouvoir créer une variable que vous n’utiliserez pas encore, par exemple lorsque vous prototypez ou démarrez un projet. Dans ce cas, vous pouvez indiquer à Rust de ne pas émettre d’avertissement concernant la variable inutilisée en faisant commencer son nom par un trait de soulignement. Dans la liste 19-20, nous créons deux variables inutilisées, mais lorsque nous compilons ce code, nous ne devrions recevoir un avertissement que pour l’une d’elles.

<Listing number="19-20" file-name="src/main.rs" caption="Faire commencer le nom d’une variable par un trait de soulignement pour éviter les avertissements concernant les variables inutilisées">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-20/src/main.rs}}
```

</Listing>

Ici, nous recevons un avertissement parce que la variable `y` n’est pas utilisée, mais nous n’en recevons pas pour `_x`.

Notez qu’il existe une différence subtile entre utiliser uniquement `_` et utiliser un nom qui commence par un trait de soulignement. La syntaxe `_x` lie toujours la valeur à la variable, alors que `_` ne la lie pas du tout. Pour montrer un cas où cette distinction a de l’importance, la liste 19-21 nous présente une erreur.

<Listing number="19-21" caption="Une variable inutilisée dont le nom commence par un trait de soulignement lie toujours la valeur, ce qui peut en prendre possession.">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-21/src/main.rs:here}}
```

</Listing>

Nous recevrons une erreur, car la valeur `s` sera tout de même déplacée dans `_s`, ce qui nous empêchera d’utiliser `s` à nouveau. En revanche, le trait de soulignement utilisé seul ne lie jamais la valeur. La liste 19-22 compile sans erreur, car `s` n’est pas déplacée dans `_`.

<Listing number="19-22" caption="Utiliser un trait de soulignement ne lie pas la valeur.">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-22/src/main.rs:here}}
```

</Listing>

Ce code fonctionne parfaitement, car nous ne lions jamais `s` à quoi que ce soit ; elle n’est pas déplacée.

<a id="ignoring-remaining-parts-of-a-value-with-"></a>

#### Les éléments restants d’une valeur avec `..`

Pour les valeurs qui contiennent de nombreux éléments, nous pouvons utiliser la syntaxe `..` afin de conserver certains éléments et d’ignorer le reste, sans devoir indiquer un trait de soulignement pour chaque valeur ignorée. Le motif `..` ignore les éléments d’une valeur auxquels nous n’avons pas explicitement fait correspondre le reste du motif. Dans la liste 19-23, nous avons un struct `Point` qui représente des coordonnées dans un espace tridimensionnel. Dans l’expression `match`, nous voulons traiter uniquement la coordonnée `x` et ignorer les valeurs des champs `y` et `z`.

<Listing number="19-23" caption="Ignorer tous les champs d’un `Point`, sauf `x`, à l’aide de `..`">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-23/src/main.rs}}
```

</Listing>

Nous indiquons la valeur `x`, puis nous ajoutons simplement le motif `..`. C’est plus rapide que de devoir écrire `y: _` et `z: _`, en particulier avec des structs qui possèdent de nombreux champs lorsque seuls un ou deux champs sont pertinents.

La syntaxe `..` s’étend au nombre d’éléments nécessaire. La liste 19-24 montre comment utiliser `..` avec un tuple.

<Listing number="19-24" file-name="src/main.rs" caption="Faire correspondre uniquement la première et la dernière valeur d’un tuple et ignorer toutes les autres">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-24/src/main.rs}}
```

</Listing>

Dans ce code, les première et dernière valeurs sont associées à `first` et `last`. Le motif `..` correspond à tout ce qui se trouve au milieu et l’ignore.

Toutefois, l’utilisation de `..` doit être dépourvue d’ambiguïté. Si les valeurs à faire correspondre et celles à ignorer ne sont pas clairement identifiables, Rust nous renverra une erreur. La liste 19-25 présente un exemple d’utilisation ambiguë de `..` ; il ne compilera donc pas.

<Listing number="19-25" file-name="src/main.rs" caption="Tentative d’utiliser `..` de manière ambiguë">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-25/src/main.rs}}
```

</Listing>

Lorsque nous compilons cet exemple, nous obtenons cette erreur :

```console
{{#include ../listings/ch19-patterns-and-matching/listing-19-25/output.txt}}
```

Rust ne peut pas déterminer combien de valeurs du tuple ignorer avant de faire correspondre une valeur à `second`, ni combien de valeurs ignorer ensuite. Ce code pourrait signifier que nous voulons ignorer `2`, associer `second` à `4`, puis ignorer `8`, `16` et `32` ; ou ignorer `2` et `4`, associer `second` à `8`, puis ignorer `16` et `32` ; et ainsi de suite. Le nom de variable `second` n’a rien de particulier pour Rust : nous obtenons donc une erreur du compilateur, car l’utilisation de `..` à deux endroits de cette façon est ambiguë.

<!-- Old headings. Do not remove or links may break. -->

<a id="extra-conditionals-with-match-guards"></a>

### Ajouter des conditions avec les gardes de motif

Une _garde de motif_ est une condition `if` supplémentaire, spécifiée après le motif dans un bras de `match`, qui doit également être vérifiée pour que ce bras soit sélectionné. Les gardes de motif sont utiles pour exprimer des idées plus complexes que ce qu’un motif seul permet. Notez toutefois qu’elles ne sont disponibles que dans les expressions `match`, et non dans les expressions `if let` ou `while let`.

La condition peut utiliser les variables créées dans le motif. La liste 19-26 présente un `match` dont le premier bras comporte le motif `Some(x)` ainsi qu’une garde de motif `if x % 2 == 0` (qui vaut `true` si le nombre est pair).

<Listing number="19-26" caption="Ajouter une garde de motif à un motif">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-26/src/main.rs:here}}
```

</Listing>

Cet exemple affiche `The number 4 is even`. Lorsque `num` est comparé au motif du premier bras, il correspond, car `Some(4)` correspond à `Some(x)`. La garde de motif vérifie ensuite si le reste de la division de `x` par 2 est égal à 0. Comme c’est le cas, le premier bras est sélectionné.

Si `num` avait été `Some(5)`, la garde de motif du premier bras aurait valu `false`, car le reste de la division de 5 par 2 est 1, ce qui n’est pas égal à 0. Rust serait alors passé au deuxième bras, qui aurait correspondu, car il n’a pas de garde de motif et correspond donc à n’importe quelle variante `Some`.

Il n’existe aucun moyen d’exprimer la condition `if x % 2 == 0` dans un motif ; la garde de motif nous permet donc d’exprimer cette logique. L’inconvénient de cette expressivité supplémentaire est que le compilateur ne vérifie pas l’exhaustivité lorsque des gardes de motif sont utilisées.

À propos de la liste 19-11, nous avons indiqué que nous pouvions utiliser des gardes de motif pour résoudre notre problème de masquage. Rappelez-vous que nous avions créé une nouvelle variable dans le motif de l’expression `match` au lieu d’utiliser la variable située à l’extérieur de `match`. Cette nouvelle variable nous empêchait de vérifier la valeur de la variable externe. La liste 19-27 montre comment utiliser une garde de motif pour résoudre ce problème.

<Listing number="19-27" file-name="src/main.rs" caption="Utiliser une garde de motif pour vérifier l’égalité avec une variable externe">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-27/src/main.rs}}
```

</Listing>

Ce code affichera maintenant `Default case, x = Some(5)`. Le motif du deuxième bras de `match` n’introduit pas de nouvelle variable `y` qui masquerait le `y` externe ; nous pouvons donc utiliser le `y` externe dans la garde de motif. Au lieu de spécifier le motif `Some(y)`, ce qui aurait masqué le `y` externe, nous spécifions `Some(n)`. Cela crée une nouvelle variable `n` qui ne masque rien, car aucune variable `n` n’existe en dehors de `match`.

La garde de motif `if n == y` n’est pas un motif et n’introduit donc pas de nouvelle variable. Ce `y` est bien le `y` externe, et non un nouveau `y` qui le masquerait. Nous pouvons rechercher une valeur égale à celle du `y` externe en comparant `n` à `y`.

Vous pouvez également utiliser l’opérateur _ou_ `|` dans une garde de motif pour spécifier plusieurs motifs ; la condition de la garde s’appliquera à tous les motifs. La liste 19-28 montre la priorité lors de la combinaison d’un motif utilisant `|` avec une garde de motif. L’élément important de cet exemple est que la garde de motif `if y` s’applique à `4`, `5` _et_ `6`, même si l’on pourrait croire que `if y` ne s’applique qu’à `6`.

<Listing number="19-28" caption="Combiner plusieurs motifs avec une garde de motif">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-28/src/main.rs:here}}
```

</Listing>

La condition de correspondance indique que le bras ne correspond que si la valeur de `x` est égale à `4`, `5` ou `6` _et_ si `y` vaut `true`. À l’exécution de ce code, le motif du premier bras correspond, car `x` vaut `4`, mais la garde de motif `if y` vaut `false` ; le premier bras n’est donc pas sélectionné. Le code passe au deuxième bras, qui correspond, et le programme affiche `no`. La raison est que la condition `if` s’applique à l’ensemble du motif `4 | 5 | 6`, et non uniquement à la dernière valeur `6`. Autrement dit, la priorité de la garde de motif par rapport au motif fonctionne ainsi :

```text
(4 | 5 | 6) if y => ...
```

et non ainsi :

```text
4 | 5 | (6 if y) => ...
```

Après l’exécution du code, la priorité devient évidente : si la garde de motif ne s’appliquait qu’à la dernière valeur de la liste de valeurs indiquées avec l’opérateur `|`, le bras aurait correspondu et le programme aurait affiché `yes`.

<!-- Old headings. Do not remove or links may break. -->

<a id="-bindings"></a>

### Utiliser des liaisons `@`

L’opérateur _at_ `@` nous permet de créer une variable qui contient une valeur tout en vérifiant si cette valeur correspond à un motif. Dans la liste 19-29, nous voulons vérifier que le champ `id` d’un `Message::Hello` se trouve dans la plage `3..=7`. Nous voulons également lier cette valeur à la variable `id` afin de pouvoir l’utiliser dans le code associé au bras.

<Listing number="19-29" caption="Utiliser `@` pour lier une valeur dans un motif tout en la vérifiant">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-29/src/main.rs:here}}
```

</Listing>

Cet exemple affiche `Found an id in range: 5`. En spécifiant `id @` avant la plage `3..=7`, nous capturons dans une variable nommée `id` toute valeur correspondant à la plage, tout en vérifiant qu’elle correspond bien au motif de plage.

Dans le deuxième bras, où le motif ne spécifie qu’une plage, le code associé ne dispose d’aucune variable contenant la valeur réelle du champ `id`. La valeur du champ `id` pourrait être 10, 11 ou 12, mais le code associé à ce motif ne sait pas laquelle. Le code du motif ne peut pas utiliser la valeur du champ `id`, car nous ne l’avons pas enregistrée dans une variable.

Dans le dernier bras, où nous avons spécifié une variable sans plage, nous disposons bien de la valeur dans une variable nommée `id`, que nous pouvons utiliser dans le code du bras. Cela est dû à l’utilisation de la syntaxe abrégée des champs de struct. Mais, contrairement aux deux premiers bras, nous n’avons appliqué aucun test à la valeur du champ `id` dans ce bras : n’importe quelle valeur correspond à ce motif.

`@` nous permet de vérifier une valeur et de l’enregistrer dans une variable au sein d’un seul motif.

## Résumé

Les motifs de Rust sont très utiles pour distinguer différents types de données. Lorsqu’ils sont utilisés dans des expressions `match`, Rust s’assure que vos motifs couvrent toutes les valeurs possibles ; dans le cas contraire, votre programme ne compilera pas. Les motifs dans les instructions `let` et les paramètres de fonctions rendent ces constructions plus utiles, car ils permettent de déstructurer des valeurs en parties plus petites et d’associer celles-ci à des variables. Nous pouvons créer des motifs simples ou complexes selon nos besoins.

Dans le prochain chapitre, l’avant-dernier du livre, nous examinerons quelques aspects avancés de plusieurs fonctionnalités de Rust.