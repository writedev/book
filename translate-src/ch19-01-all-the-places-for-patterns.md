## Tous les endroits où les motifs peuvent être utilisés

Les motifs apparaissent à plusieurs endroits en Rust, et vous en avez déjà utilisé beaucoup sans vous en rendre compte ! Cette section présente tous les endroits où les motifs sont valides.

### Bras de `match`

Comme nous l’avons vu au chapitre 6, nous utilisons des motifs dans les bras des expressions `match`. Formellement, les expressions `match` sont définies par le mot-clé `match`, une valeur à comparer et un ou plusieurs bras de correspondance, chacun constitué d’un motif et d’une expression à exécuter si la valeur correspond au motif de ce bras, comme ceci :

<!--
  Manually formatted rather than using Markdown intentionally: Markdown does not
  support italicizing code in the body of a block like this!
-->

<pre><code>match <em>VALEUR</em> {
    <em>MOTIF</em> => <em>EXPRESSION</em>,
    <em>MOTIF</em> => <em>EXPRESSION</em>,
    <em>MOTIF</em> => <em>EXPRESSION</em>,
}</code></pre>

Par exemple, voici l’expression `match` de la liste 6-5, qui compare une valeur `Option<i32>` dans la variable `x` :

```rust,ignore
match x {
    None => None,
    Some(i) => Some(i + 1),
}
```

Les motifs de cette expression `match` sont `None` et `Some(i)`, situés à gauche de chaque flèche.

Les expressions `match` doivent être exhaustives, c’est-à-dire qu’elles doivent prendre en compte toutes les possibilités pour la valeur comparée. Pour vous assurer d’avoir couvert tous les cas, vous pouvez utiliser un motif fourre-tout dans le dernier bras : par exemple, un nom de variable qui correspond à n’importe quelle valeur ne peut jamais échouer et couvre donc tous les cas restants.

Le motif particulier `_` correspond à tout, mais ne lie aucune variable. Il est donc souvent utilisé dans le dernier bras d’un `match`. Par exemple, le motif `_` peut être utile lorsque vous souhaitez ignorer toute valeur qui n’est pas explicitement spécifiée. Nous verrons plus en détail le motif `_` dans la section [« Ignorer des valeurs dans un motif »][ignoring-values-in-a-pattern]<!-- ignore -->, plus loin dans ce chapitre.

### Instructions `let`

Avant ce chapitre, nous avions seulement parlé explicitement de l’utilisation des motifs avec `match` et `if let`, mais, en réalité, nous avons aussi utilisé des motifs à d’autres endroits, notamment dans les instructions `let`. Prenons par exemple cette simple affectation de variable avec `let` :

```rust
let x = 5;
```

Chaque fois que vous avez utilisé une instruction `let` de cette manière, vous avez utilisé des motifs, même si vous ne vous en êtes peut-être pas rendu compte ! Plus formellement, une instruction `let` se présente ainsi :

<!--
  Manually formatted rather than using Markdown intentionally: Markdown does not
  support italicizing code in the body of a block like this!
-->

<pre>
<code>let <em>MOTIF</em> = <em>EXPRESSION</em>;</code>
</pre>

Dans une instruction comme `let x = 5;`, où un nom de variable occupe la place du MOTIF, ce nom est simplement une forme particulièrement simple de motif. Rust compare l’expression au motif et affecte les noms qu’il trouve. Ainsi, dans l’exemple `let x = 5;`, `x` est un motif qui signifie « lier à la variable `x` ce qui correspond ici ». Comme le nom `x` constitue à lui seul tout le motif, celui-ci signifie en pratique « tout lier à la variable `x`, quelle que soit la valeur ».

Pour mieux comprendre l’aspect de correspondance de motifs de `let`, examinons la liste 19-1, qui utilise un motif avec `let` pour déstructurer un tuple.

<Listing number="19-1" caption="Utiliser un motif pour déstructurer un tuple et créer trois variables à la fois">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-01/src/main.rs:here}}
```

</Listing>

Ici, nous comparons un tuple à un motif. Rust compare la valeur `(1, 2, 3)` au motif `(x, y, z)` et constate que la valeur correspond au motif — autrement dit, il constate que les deux ont le même nombre d’éléments — puis lie `1` à `x`, `2` à `y` et `3` à `z`. Vous pouvez considérer ce motif de tuple comme un emboîtement de trois motifs de variable individuels.

Si le nombre d’éléments du motif ne correspond pas au nombre d’éléments du tuple, le type global ne correspondra pas et nous obtiendrons une erreur du compilateur. Par exemple, la liste 19-2 montre une tentative de déstructurer un tuple de trois éléments en deux variables, ce qui ne fonctionne pas.

<Listing number="19-2" caption="Construire incorrectement un motif dont les variables ne correspondent pas au nombre d’éléments du tuple">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-02/src/main.rs:here}}
```

</Listing>

La compilation de ce code produit cette erreur de type :

```console
{{#include ../listings/ch19-patterns-and-matching/listing-19-02/output.txt}}
```

Pour corriger l’erreur, nous pourrions ignorer une ou plusieurs valeurs du tuple à l’aide de `_` ou de `..`, comme vous le verrez dans la section [« Ignorer des valeurs dans un motif »][ignoring-values-in-a-pattern]<!-- ignore -->. Si le problème vient du fait que le motif contient trop de variables, il faut faire correspondre les types en supprimant des variables, de sorte que leur nombre soit égal au nombre d’éléments du tuple.

### Expressions conditionnelles `if let`

Au chapitre 6, nous avons vu comment utiliser principalement les expressions `if let` comme une manière plus concise d’écrire l’équivalent d’un `match` qui ne traite qu’un seul cas. Une expression `if let` peut également comporter un `else` correspondant, qui contient le code à exécuter si le motif de `if let` ne correspond pas.

La liste 19-3 montre qu’il est également possible de combiner des expressions `if let`, `else if` et `else if let`. Cela nous donne plus de souplesse qu’une expression `match`, dans laquelle nous ne pouvons comparer les motifs qu’à une seule valeur. De plus, Rust n’exige pas que les conditions d’une série de bras `if let`, `else if` et `else if let` soient liées entre elles.

Le code de la liste 19-3 détermine la couleur d’arrière-plan à utiliser en effectuant plusieurs vérifications. Pour cet exemple, nous avons créé des variables contenant des valeurs codées en dur qu’un vrai programme pourrait recevoir de l’utilisateur.

<Listing number="19-3" file-name="src/main.rs" caption="Combiner `if let`, `else if`, `else if let` et `else`">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-03/src/main.rs}}
```

</Listing>

Si l’utilisateur indique sa couleur préférée, cette couleur est utilisée pour l’arrière-plan. Si aucune couleur préférée n’est indiquée et que nous sommes mardi, l’arrière-plan est vert. Sinon, si l’utilisateur indique son âge sous forme de chaîne et que nous parvenons à l’analyser comme un nombre, la couleur est violette ou orange selon la valeur de ce nombre. Si aucune de ces conditions ne s’applique, l’arrière-plan est bleu.

Cette structure conditionnelle nous permet de gérer des exigences complexes. Avec les valeurs codées en dur que nous avons ici, cet exemple affichera `Using purple as the background color`.

Vous pouvez constater que `if let` peut aussi introduire de nouvelles variables qui masquent des variables existantes, tout comme les bras de `match` : la ligne `if let Ok(age) = age` introduit une nouvelle variable `age` contenant la valeur à l’intérieur de la variante `Ok`, et masque ainsi la variable `age` existante. Nous devons donc placer la condition `if age > 30` à l’intérieur de ce bloc : nous ne pouvons pas combiner ces deux conditions dans `if let Ok(age) = age && age > 30`. La nouvelle variable `age` que nous voulons comparer à 30 n’est disponible qu’à partir du début de la nouvelle portée, délimitée par l’accolade ouvrante.

L’inconvénient des expressions `if let` est que le compilateur ne vérifie pas leur exhaustivité, contrairement aux expressions `match`. Si nous omettions le dernier bloc `else` et ne traitions donc pas certains cas, le compilateur ne nous avertirait pas de cette possible erreur logique.

### Boucles conditionnelles `while let`

De construction semblable à `if let`, la boucle conditionnelle `while let` permet à une boucle `while` de s’exécuter tant qu’un motif continue de correspondre. Dans la liste 19-4, nous montrons une boucle `while let` qui attend des messages envoyés entre des threads, mais qui vérifie ici un `Result` plutôt qu’un `Option`.

<Listing number="19-4" caption="Utiliser une boucle `while let` pour afficher des valeurs tant que `rx.recv()` renvoie `Ok`">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-04/src/main.rs:here}}
```

</Listing>

Cet exemple affiche `1`, puis `2`, puis `3`. La méthode `recv` récupère le premier message du côté récepteur du canal et renvoie un `Ok(value)`. Lorsque nous avons découvert `recv` au chapitre 16, nous avons directement propagé l’erreur ou avons utilisé la méthode comme un itérateur dans une boucle `for`. Cependant, comme le montre la liste 19-4, nous pouvons aussi utiliser `while let`, car la méthode `recv` renvoie un `Ok` chaque fois qu’un message arrive, tant que l’émetteur existe, puis produit un `Err` lorsque le côté émetteur se déconnecte.

### Boucles `for`

Dans une boucle `for`, la valeur qui suit directement le mot-clé `for` est un motif. Par exemple, dans `for x in y`, `x` est le motif. La liste 19-5 montre comment utiliser un motif dans une boucle `for` pour déstructurer, ou séparer, un tuple dans le cadre de la boucle.

<Listing number="19-5" caption="Utiliser un motif dans une boucle `for` pour déstructurer un tuple">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-05/src/main.rs:here}}
```

</Listing>

Le code de la liste 19-5 affiche :

```console
{{#include ../listings/ch19-patterns-and-matching/listing-19-05/output.txt}}
```

Nous adaptons un itérateur avec la méthode `enumerate` pour qu’il produise une valeur et l’indice correspondant, réunis dans un tuple. La première valeur produite est le tuple `(0, 'a')`. Lorsque cette valeur correspond au motif `(index, value)`, `index` vaut `0` et `value` vaut `'a'`, ce qui affiche la première ligne de la sortie.

### Paramètres de fonction

Les paramètres de fonction peuvent également être des motifs. Le code de la liste 19-6, qui déclare une fonction nommée `foo` prenant un paramètre nommé `x` de type `i32`, devrait maintenant vous sembler familier.

<Listing number="19-6" caption="Signature de fonction utilisant des motifs dans ses paramètres">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-06/src/main.rs:here}}
```

</Listing>

La partie `x` est un motif ! Comme avec `let`, nous pourrions comparer un tuple au motif dans les arguments d’une fonction. La liste 19-7 sépare les valeurs d’un tuple que nous passons à une fonction.

<Listing number="19-7" file-name="src/main.rs" caption="Fonction dont les paramètres déstructurent un tuple">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-07/src/main.rs}}
```

</Listing>

Ce code affiche `Current location: (3, 5)`. Les valeurs `&(3, 5)` correspondent au motif `&(x, y)`, donc `x` vaut `3` et `y` vaut `5`.

Nous pouvons également utiliser des motifs dans les listes de paramètres des fermetures, comme dans celles des fonctions, car les fermetures ressemblent aux fonctions, comme nous l’avons vu au chapitre 13.

Vous avez maintenant vu plusieurs façons d’utiliser des motifs, mais ceux-ci ne fonctionnent pas de la même manière partout où ils peuvent être employés. À certains endroits, les motifs doivent être irréfutables ; dans d’autres circonstances, ils peuvent être réfutables. Nous allons maintenant examiner ces deux concepts.

[ignoring-values-in-a-pattern]: ch19-03-pattern-syntax.html#ignoring-values-in-a-pattern