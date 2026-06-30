<!-- Old headings. Do not remove or links may break. -->

<a id="the-match-control-flow-operator"></a>

## Le Construct Contrôle de Flux `match`

Rust dispose d'un construct de contrôle de flux extrêmement puissant appelé `match` qui vous permet de comparer une valeur à une série de motifs et d'exécuter du code en fonction du motif qui correspond. Les motifs peuvent être composés de valeurs littérales, de noms de variables, de caractères généraux et bien d'autres choses ; [Chapitre 19][ch19-00-patterns]<!-- ignore --> couvre tous les types de motifs différents et leur fonctionnement. La puissance de `match` provient de l'expressivité des motifs et du fait que le compilateur vérifie que tous les cas possibles sont traités.

Considérez une expression `match` comme étant semblable à une machine de tri de pièces : les pièces glissent le long d'un rail avec des trous de tailles variées, et chaque pièce tombe à travers le premier trou dans lequel elle s'insère. De la même manière, les valeurs passent à travers chaque motif dans un `match`, et au premier motif dans lequel la valeur "s'insère", la valeur se place dans le bloc de code associé pour être utilisée durant l'exécution.

En parlant de pièces, utilisons-les comme exemple avec `match` ! Nous pouvons écrire une fonction qui prend une pièce américaine inconnue et, d'une manière similaire à la machine de comptage, détermine de quelle pièce il s'agit et renvoie sa valeur en cents, comme illustré dans la Liste 6-3.

<Liste numéro="6-3" légende="Un enum et une expression `match` qui utilise les variantes de l'enum comme motifs">

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-03/src/main.rs:here}}
```

</Liste>

Analysons le `match` dans la fonction `value_in_cents`. Tout d'abord, nous listons le mot clé `match` suivi d'une expression, qui dans ce cas est la valeur `coin`. Cela semble très similaire à une expression conditionnelle utilisée avec `if`, mais il existe une grande différence : Avec `if`, la condition doit évaluer à une valeur booléenne, mais ici, elle peut être de n'importe quel type. Le type de `coin` dans cet exemple est l'enum `Coin` que nous avons défini sur la première ligne.

Ensuite se trouvent les bras du `match`. Un bras a deux parties : un motif et du code. Le premier bras ici possède un motif qui est la valeur `Coin::Penny` et ensuite l'opérateur `=>` qui sépare le motif et le code à exécuter. Le code dans ce cas est simplement la valeur `1`. Chaque bras est séparé du suivant par une virgule.

Lorsque l'expression `match` s'exécute, elle compare la valeur résultante au motif de chaque bras, dans l'ordre. Si un motif correspond à la valeur, le code associé à ce motif est exécuté. Si ce motif ne correspond pas à la valeur, l'exécution continue vers le bras suivant, tout comme dans une machine de tri de pièces. Nous pouvons avoir autant de bras que nécessaire : dans la Liste 6-3, notre `match` a quatre bras.

Le code associé à chaque bras est une expression, et la valeur résultante de l'expression dans le bras correspondant est la valeur qui est renvoyée pour l'ensemble de l'expression `match`.

Nous n'utilisons généralement pas d'accolades si le code du bras du `match` est court, comme c'est le cas dans la Liste 6-3 où chaque bras retourne simplement une valeur. Si vous souhaitez exécuter plusieurs lignes de code dans un bras de `match`, vous devez utiliser des accolades, et la virgule suivante au bras est alors facultative. Par exemple, le code suivant affiche "Pièce porte-bonheur !" chaque fois que la méthode est appelée avec un `Coin::Penny`, mais il retourne toujours la dernière valeur du bloc, `1` :

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-08-match-arm-multiple-lines/src/main.rs:here}}
```

### Motifs Qui Lient des Valeurs

Une autre fonctionnalité utile des bras de match est qu'ils peuvent se lier aux parties des valeurs qui correspondent au motif. C'est ainsi que nous pouvons extraire des valeurs des variantes d'enum.

Par exemple, changeons une de nos variantes d'enum pour contenir des données à l'intérieur. De 1999 à 2008, les États-Unis ont frappé des quarts avec différents designs pour chacun des 50 États sur un côté. Aucune autre pièce n'a eu de designs d'État, donc seuls les quarts ont cette valeur supplémentaire. Nous pouvons ajouter cette information à notre `enum` en modifiant la variante `Quarter` pour inclure une valeur `UsState` stockée à l'intérieur, ce que nous avons fait dans la Liste 6-4.

<Liste numéro="6-4" légende="Un enum `Coin` dans lequel la variante `Quarter` contient également une valeur `UsState`">

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-04/src/main.rs:here}}
```

</Liste>

Imaginons qu'un ami essaie de collecter tous les quarts des 50 États. Pendant que nous trions notre monnaie en pièces par type, nous appellerons également le nom de l'État associé à chaque quart afin que, s'il s'agit de l'un qu'il n'a pas, il puisse l'ajouter à sa collection.

Dans l'expression `match` pour ce code, nous ajoutons une variable appelée `state` au motif qui correspond aux valeurs de la variante `Coin::Quarter`. Lorsque `Coin::Quarter` correspond, la variable `state` se liera à la valeur de l'État de ce quart. Ensuite, nous pouvons utiliser `state` dans le code pour ce bras, comme ceci :

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-09-variable-in-pattern/src/main.rs:here}}
```

Si nous appelions `value_in_cents(Coin::Quarter(UsState::Alaska))`, `coin` serait `Coin::Quarter(UsState::Alaska)`. Lorsque nous comparons cette valeur avec chacun des bras du match, aucun d'eux ne correspond jusqu'à ce que nous atteignons `Coin::Quarter(state)`. À ce moment-là, la liaison pour `state` sera la valeur `UsState::Alaska`. Nous pouvons ensuite utiliser cette liaison dans l'expression `println !`, obtenant ainsi la valeur d'État interne de la variante d'enum `Coin` pour `Quarter`.

<!-- Old headings. Do not remove or links may break. -->

<a id="matching-with-optiont"></a>

### Le Modèle `match` `Option<T>`


Dans la section précédente, nous voulions obtenir la valeur interne `T` du cas `Some` lors de l'utilisation de `Option<T>` ; nous pouvons également gérer `Option<T>` en utilisant `match`, comme nous l'avons fait avec l'enum `Coin` ! Au lieu de comparer des pièces, nous allons comparer les variantes de `Option<T>`, mais la manière dont l'expression `match` fonctionne reste la même.

Disons que nous voulons écrire une fonction qui prend un `Option<i32>` et, s'il y a une valeur à l'intérieur, ajoute 1 à cette valeur. S'il n'y a pas de valeur à l'intérieur, la fonction doit renvoyer la valeur `None` et ne pas tenter d'effectuer d'opérations.

Cette fonction est très facile à écrire, grâce à `match`, et ressemblera à la Liste 6-5.

<Liste numéro="6-5" légende="Une fonction qui utilise une expression `match` sur un `Option<i32>`">

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-05/src/main.rs:here}}
```

</Liste>

Examinons la première exécution de `plus_one` en détail. Lorsque nous appelons `plus_one(five)`, la variable `x` dans le corps de `plus_one` aura la valeur `Some(5)`. Nous la comparons ensuite à chaque bras de `match` :

```rust,ignore
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-05/src/main.rs:first_arm}}
```

La valeur `Some(5)` ne correspond pas au motif `None`, donc nous continuons au bras suivant :

```rust,ignore
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-05/src/main.rs:second_arm}}
```

Est-ce que `Some(5)` correspond à `Some(i)` ? Oui ! Nous avons la même variante. Le `i` se lie à la valeur contenue dans `Some`, donc `i` prend la valeur `5`. Le code dans le bras du match est alors exécuté, donc nous ajoutons 1 à la valeur de `i` et créons une nouvelle valeur `Some` avec notre total `6` à l'intérieur.

Considérons maintenant le deuxième appel de `plus_one` dans la Liste 6-5, où `x` est `None`. Nous entrons dans le `match` et comparons au premier bras :

```rust,ignore
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-05/src/main.rs:first_arm}}
```

Cela correspond ! Il n'y a pas de valeur à ajouter, donc le programme s'arrête et renvoie la valeur `None` à droite de `=>`. Puisque le premier bras a correspondu, aucun autre bras n'est comparé.

Combiner `match` et enums est utile dans de nombreuses situations. Vous verrez ce motif souvent dans le code Rust : `match` contre un enum, lier une variable aux données à l'intérieur, puis exécuter du code en fonction. C'est un peu délicat au début, mais une fois que vous vous y habituez, vous souhaiteriez l'avoir dans tous les langages. C'est constamment un favori parmi les utilisateurs.

### Les `match` Sont Exhaustifs

Il y a un autre aspect de `match` dont nous devons discuter : les motifs des bras doivent couvrir toutes les possibilités. Considérez cette version de notre fonction `plus_one`, qui a un bug et ne compilera pas :

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-10-non-exhaustive-match/src/main.rs:here}}
```

Nous n'avons pas traité le cas `None`, donc ce code causera un bug. Heureusement, c'est un bug que Rust sait détecter. Si nous essayons de compiler ce code, nous obtiendrons cette erreur :

```console
{{#include ../listings/ch06-enums-and-pattern-matching/no-listing-10-non-exhaustive-match/output.txt}}
```

Rust sait que nous n'avons pas couvert tous les cas possibles et sait même quel motif nous avons oublié ! Les `match` en Rust sont _exhaustifs_ : Nous devons épuiser toutes les possibilités pour que le code soit valide. Surtout dans le cas de `Option<T>`, lorsque Rust nous empêche d'oublier de traiter explicitement le cas `None`, il nous protège d'une supposition selon laquelle nous avons une valeur alors que nous pourrions avoir null, rendant ainsi impossible l'erreur milliardaire mentionnée plus tôt.

### Motifs de Captation Généraux et le Signe `_`

En utilisant des enums, nous pouvons également prendre des actions spéciales pour quelques valeurs particulières, mais pour toutes les autres valeurs, une action par défaut est utilisée. Imaginez que nous mettons en œuvre un jeu où, si vous lancez un 3, votre joueur ne se déplace pas mais reçoit plutôt un nouveau chapeau. Si vous lancez un 7, votre joueur perd un chapeau. Pour toutes les autres valeurs, votre joueur se déplace d'autant de cases sur le plateau de jeu. Voici un `match` qui met en œuvre cette logique, avec le résultat du lancé de dés codé en dur plutôt qu'une valeur aléatoire, et toute autre logique représentée par des fonctions sans corps car leur mise en œuvre est hors de portée pour cet exemple :

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-15-binding-catchall/src/main.rs:here}}
```

Pour les deux premiers bras, les motifs sont les valeurs littérales `3` et `7`. Pour le dernier bras qui couvre toutes les autres valeurs possibles, le motif est la variable que nous avons choisi de nommer `other`. Le code qui s'exécute pour le bras `other` utilise la variable en la passant à la fonction `move_player`.

Ce code compile, même si nous n'avons pas listé toutes les valeurs possibles qu'un `u8` peut avoir, car le dernier motif correspondra à toutes les valeurs non spécifiquement énumérées. Ce motif de captation générale satisfait la exigence selon laquelle `match` doit être exhaustif. Notez que nous devons placer le bras de captation générale en dernier car les motifs sont évalués dans l'ordre. Si nous avions placé le bras de captation générale plus tôt, les autres bras ne s'exécuteraient jamais, donc Rust nous avertira si nous ajoutons des bras après un motif de captation générale !

Rust dispose également d'un motif que nous pouvons utiliser lorsque nous voulons une captation générale mais ne voulons pas _utiliser_ la valeur dans le motif de captation générale : `_` est un motif spécial qui correspond à n'importe quelle valeur et ne se lie pas à cette valeur. Cela dit à Rust que nous n'allons pas utiliser la valeur, donc Rust ne nous avertira pas d'une variable inutilisée.

Changeons les règles du jeu : maintenant, si vous lancez autre chose qu'un 3 ou un 7, vous devez relancer. Nous n'avons plus besoin d'utiliser la valeur de captation générale, donc nous pouvons changer notre code pour utiliser `_` à la place de la variable nommée `other` :

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-16-underscore-catchall/src/main.rs:here}}
```

Cet exemple respecte également l'exigence d'exhaustivité car nous ignorons explicitement toutes les autres valeurs dans le dernier bras ; nous n'avons rien oublié.

Enfin, nous allons changer les règles du jeu une fois de plus pour que rien d'autre ne se passe lors de votre tour si vous obtenez autre chose qu'un 3 ou un 7. Nous pouvons exprimer cela en utilisant la valeur unité (le type tuple vide que nous avons mentionné dans la section [“Le Type Tuple”][tuples]<!-- ignore -->) comme le code qui accompagne le bras `_` :

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-17-underscore-unit/src/main.rs:here}}
```

Ici, nous disons explicitement à Rust que nous n'allons pas utiliser toute autre valeur qui ne correspond pas à un motif dans un bras antérieur, et nous ne souhaitons pas exécuter de code dans ce cas.

Il y a encore plus à propos des motifs et des correspondances que nous couvrirons dans [Chapitre 19][ch19-00-patterns]<!-- ignore -->. Pour l'instant, nous allons passer à la syntaxe `if let`, qui peut être utile dans des situations où l'expression `match` est un peu verbeuse.

[tuples]: ch03-02-data-types.html#the-tuple-type
[ch19-00-patterns]: ch19-00-patterns.html