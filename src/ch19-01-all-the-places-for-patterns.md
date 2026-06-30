## Tous les endroits où les motifs peuvent être utilisés

Les motifs apparaissent dans de nombreux endroits en Rust, et vous les avez utilisés souvent sans vous en rendre compte ! Cette section aborde tous les endroits où les motifs sont valides.

### Bras de `match`

Comme discuté au Chapitre 6, nous utilisons des motifs dans les bras des expressions `match`. Formellement, les expressions `match` sont définies par le mot-clé `match`, une valeur à comparer, et un ou plusieurs bras de match qui consistent en un motif et une expression à exécuter si la valeur correspond au motif de ce bras, de cette manière :

<pre><code>match <em>VALEUR</em> {
    <em>MOTIF</em> => <em>EXPRESSION</em>,
    <em>MOTIF</em> => <em>EXPRESSION</em>,
    <em>MOTIF</em> => <em>EXPRESSION</em>,
}</code></pre>

Par exemple, voici l’expression `match` de l'énoncé 6-5 qui correspond à une valeur `Option<i32>` dans la variable `x` :

```rust,ignore
match x {
    None => None,
    Some(i) => Some(i + 1),
}
```

Les motifs dans cette expression `match` sont `None` et `Some(i)` à gauche de chaque flèche.

Une exigence pour les expressions `match` est qu'elles doivent être exhaustives, dans le sens où toutes les possibilités pour la valeur dans l’expression `match` doivent être prises en compte. Une façon de s'assurer que vous avez couvert toutes les possibilités est d'avoir un motif de secours pour le dernier bras : par exemple, un nom de variable qui correspond à n'importe quelle valeur ne peut jamais échouer et couvre donc tous les cas restants.

Le motif particulier `_` correspondra à n'importe quoi, mais il ne se lie jamais à une variable, il est donc souvent utilisé dans le dernier bras de match. Le motif `_` peut être utile lorsque vous souhaitez ignorer toute valeur non spécifiée, par exemple. Nous aborderons le motif `_` plus en détail dans [“Ignorer des valeurs dans un motif”][ignoring-values-in-a-pattern]<!-- ignore --> plus loin dans ce chapitre.

### Instructions `let`

Avant ce chapitre, nous avions seulement discuté de l'utilisation explicite des motifs avec `match` et `if let`, mais en réalité, nous avons également utilisé des motifs dans d'autres endroits, y compris dans les instructions `let`. Par exemple, considérez cette simple affectation de variable avec `let` :

```rust
let x = 5;
```

Chaque fois que vous avez utilisé une instruction `let` comme celle-ci, vous avez utilisé des motifs, même si vous n'en étiez pas conscient ! Plus formellement, une instruction `let` ressemble à ceci :

<pre><code>let <em>MOTIF</em> = <em>EXPRESSION</em>;</code></pre>

Dans des instructions comme `let x = 5;`, avec un nom de variable dans l'emplacement MOTIF, le nom de la variable est juste une forme particulièrement simple d'un motif. Rust compare l'expression avec le motif et assigne tous les noms qu'il trouve. Ainsi, dans l'exemple `let x = 5;`, `x` est un motif qui signifie "lier ce qui correspond ici à la variable `x`." Comme le nom `x` constitue le motif entier, ce motif signifie en effet "lier tout à la variable `x`, quelle que soit la valeur."

Pour voir plus clairement l'aspect de correspondance de motifs de `let`, considérons l'énoncé 19-1, qui utilise un motif avec `let` pour décomposer un tuple.

<Listing number="19-1" caption="Utiliser un motif pour décomposer un tuple et créer trois variables à la fois">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-01/src/main.rs:here}}
```

</Listing>

Ici, nous faisons correspondre un tuple à un motif. Rust compare la valeur `(1, 2, 3)` au motif `(x, y, z)` et voit que la valeur correspond au motif, c'est-à-dire qu'il constate que le nombre d'éléments est le même dans les deux ; ainsi, Rust lie `1` à `x`, `2` à `y` et `3` à `z`. Vous pouvez penser à ce motif de tuple comme à l'imbrication de trois motifs de variables individuels à l'intérieur.

Si le nombre d'éléments dans le motif ne correspond pas au nombre d'éléments dans le tuple, le type global ne correspondra pas et nous obtiendrons une erreur de compilation. Par exemple, l'énoncé 19-2 montre une tentative de décomposer un tuple avec trois éléments en deux variables, ce qui ne fonctionnera pas.

<Listing number="19-2" caption="Construction incorrecte d'un motif dont les variables ne correspondent pas au nombre d'éléments dans le tuple">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-02/src/main.rs:here}}
```

</Listing>

Essayer de compiler ce code entraîne cette erreur de type :

```console
{{#include ../listings/ch19-patterns-and-matching/listing-19-02/output.txt}}
```

Pour corriger l'erreur, nous pourrions ignorer une ou plusieurs valeurs dans le tuple en utilisant `_` ou `..`, comme vous le verrez dans la section [“Ignorer des valeurs dans un motif”][ignoring-values-in-a-pattern]<!-- ignore -->. Si le problème est que nous avons trop de variables dans le motif, la solution consiste à faire correspondre les types en supprimant des variables pour que le nombre de variables soit égal au nombre d'éléments dans le tuple.

### Expressions conditionnelles `if let`

Au Chapitre 6, nous avons discuté de la façon d'utiliser des expressions `if let` principalement comme une façon plus courte d'écrire l'équivalent d'un `match` qui ne correspond qu'à un seul cas. Optionnellement, `if let` peut avoir un `else` correspondant contenant du code à exécuter si le motif dans le `if let` ne correspond pas.

L'énoncé 19-3 montre qu'il est également possible de mélanger et d'associer des expressions `if let`, `else if`, et `else if let`. Ce faisant, nous avons plus de flexibilité qu'une expression `match` dans laquelle nous ne pouvons exprimer qu'une seule valeur à comparer avec les motifs. De plus, Rust ne nécessite pas que les conditions dans une série de bras `if let`, `else if`, et `else if let` soient liées entre elles.

Le code dans l'énoncé 19-3 détermine quelle couleur utiliser pour votre arrière-plan en fonction d'une série de vérifications pour plusieurs conditions. Pour cet exemple, nous avons créé des variables avec des valeurs codées en dur que un vrai programme pourrait recevoir par saisie utilisateur.

<Listing number="19-3" file-name="src/main.rs" caption="Mélanger `if let`, `else if`, `else if let`, et `else`">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-03/src/main.rs}}
```

</Listing>

Si l'utilisateur spécifie une couleur préférée, cette couleur est utilisée comme arrière-plan. Si aucune couleur préférée n'est spécifiée et qu'aujourd'hui nous sommes mardi, la couleur d'arrière-plan est verte. Sinon, si l'utilisateur spécifie son âge sous forme de chaîne et que nous pouvons l'analyser avec succès en tant que nombre, la couleur est soit violette, soit orange, selon la valeur du nombre. Si aucune de ces conditions ne s'applique, la couleur d'arrière-plan est bleue.

Cette structure conditionnelle nous permet de prendre en charge des exigences complexes. Avec les valeurs codées en dur que nous avons ici, cet exemple affichera `Utilisation de la couleur violette comme couleur d'arrière-plan`.

Vous pouvez voir que `if let` peut également introduire de nouvelles variables qui masquent les variables existantes de la même manière que les bras de `match` peuvent : La ligne `if let Ok(age) = age` introduit une nouvelle variable `age` qui contient la valeur à l'intérieur du variant `Ok`, masquant la variable `age` existante. Cela signifie que nous devons placer la condition `if age > 30` dans ce bloc : nous ne pouvons pas combiner ces deux conditions en `if let Ok(age) = age && age > 30`. Le nouvel `age` que nous souhaitons comparer à 30 n'est pas valide jusqu'à ce que le nouveau contexte commence avec la parenthèse ouvrante.

L'inconvénient d'utiliser des expressions `if let` est que le compilateur ne vérifie pas l'exhaustivité, alors qu'avec des expressions `match`, il le fait. Si nous omettons le dernier bloc `else` et que nous manquons donc de traiter certains cas, le compilateur ne nous alertera pas sur le possible bogue logique.

### Boucles conditionnelles `while let`

Similaire dans sa construction à `if let`, la boucle conditionnelle `while let` permet à une boucle `while` de s'exécuter tant qu'un motif continue de correspondre. Dans l'énoncé 19-4, nous montrons une boucle `while let` qui attend des messages envoyés entre des threads, mais dans ce cas en vérifiant un `Result` plutôt qu'un `Option`.

<Listing number="19-4" caption="Utilisation d'une boucle `while let` pour imprimer des valeurs tant que `rx.recv()` renvoie `Ok`">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-04/src/main.rs:here}}
```

</Listing>

Cet exemple affiche `1`, `2`, puis `3`. La méthode `recv` prend le premier message du côté récepteur du canal et renvoie un `Ok(value)`. Lorsque nous avons vu `recv` pour la première fois au Chapitre 16, nous avions extrait l'erreur directement, ou nous avons interagi avec elle en tant qu'itérateur en utilisant une boucle `for`. Cependant, comme le montre l'énoncé 19-4, nous pouvons également utiliser `while let`, car la méthode `recv` renvoie un `Ok` chaque fois qu'un message arrive, tant que l'expéditeur existe, puis produit un `Err` une fois que le côté expéditeur se déconnecte.

### Boucles `for`

Dans une boucle `for`, la valeur qui suit directement le mot-clé `for` est un motif. Par exemple, dans `for x in y`, `x` est le motif. L'énoncé 19-5 démontre comment utiliser un motif dans une boucle `for` pour décomposer, ou séparer, un tuple dans le cadre de la boucle `for`.

<Listing number="19-5" caption="Utiliser un motif dans une boucle `for` pour décomposer un tuple">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-05/src/main.rs:here}}
```

</Listing>

Le code dans l'énoncé 19-5 imprimera ce qui suit :

```console
{{#include ../listings/ch19-patterns-and-matching/listing-19-05/output.txt}}
```

Nous adaptons un itérateur à l'aide de la méthode `enumerate`, de sorte qu'il produise une valeur et l'index pour cette valeur, placés dans un tuple. La première valeur produite est le tuple `(0, 'a')`. Lorsque cette valeur est mise en correspondance avec le motif `(index, value)`, `index` sera `0` et `value` sera `'a'`, imprimant la première ligne de la sortie.

### Paramètres de fonction

Les paramètres de fonction peuvent également être des motifs. Le code dans l'énoncé 19-6, qui déclare une fonction nommée `foo` prenant un paramètre nommé `x` de type `i32`, devrait maintenant vous sembler familier.

<Listing number="19-6" caption="Une signature de fonction utilisant des motifs dans les paramètres">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-06/src/main.rs:here}}
```

</Listing>

La partie `x` est un motif ! Comme nous l'avons fait avec `let`, nous pourrions également faire correspondre un tuple dans les arguments d'une fonction avec le motif. L'énoncé 19-7 divise les valeurs dans un tuple alors que nous le passons à une fonction.

<Listing number="19-7" file-name="src/main.rs" caption="Une fonction avec des paramètres qui décomposent un tuple">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-07/src/main.rs}}
```

</Listing>

Ce code affiche `Emplacement actuel : (3, 5)`. Les valeurs `&(3, 5)` correspondent au motif `&(x, y)`, donc `x` est la valeur `3` et `y` est la valeur `5`.

Nous pouvons également utiliser des motifs dans les listes de paramètres de fermeture de la même manière que dans les listes de paramètres de fonction, car les fermetures sont similaires aux fonctions, comme discuté au Chapitre 13.

À ce stade, vous avez vu plusieurs façons d'utiliser des motifs, mais les motifs ne fonctionnent pas de la même manière dans tous les endroits où nous pouvons les utiliser. Dans certains cas, les motifs doivent être irrécusables ; dans d'autres circonstances, ils peuvent être récusables. Nous discuterons de ces deux concepts ensuite.

[ignoring-values-in-a-pattern]: ch19-03-pattern-syntax.html#ignoring-values-in-a-pattern