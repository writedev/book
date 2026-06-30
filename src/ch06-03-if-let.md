## Flux de contrôle concis avec `if let` et `let...else`

La syntaxe `if let` vous permet de combiner `if` et `let` de manière moins verbeuse pour gérer des valeurs qui correspondent à un motif tout en ignorant les autres. Considérez le programme dans la Liste 6-6 qui correspond à une valeur `Option<u8>` dans la variable `config_max`, mais qui ne veut exécuter du code que si la valeur est la variante `Some`.

<Liste numéro="6-6" légende="Un `match` qui ne se préoccupe que d'exécuter du code lorsque la valeur est `Some`">

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-06/src/main.rs:here}}
```

</Liste>

Si la valeur est `Some`, nous affichons la valeur de la variante `Some` en liant la valeur à la variable `max` dans le motif. Nous ne voulons rien faire avec la valeur `None`. Pour satisfaire l'expression `match`, nous devons ajouter `_ =>
()` après avoir traité une seule variante, ce qui est un code d’entête ennuyeux à ajouter.

Au lieu de cela, nous pourrions écrire cela de manière plus courte en utilisant `if let`. Le code suivant se comporte de la même manière que le `match` dans la Liste 6-6 :

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-12-if-let/src/main.rs:here}}
```

La syntaxe `if let` prend un motif et une expression séparés par un signe égal. Cela fonctionne de la même manière qu'un `match`, où l'expression est donnée au `match` et le motif est son premier bras. Dans ce cas, le motif est `Some(max)`, et le `max` est lié à la valeur à l'intérieur du `Some`. Nous pouvons ensuite utiliser `max` dans le corps du bloc `if let` de la même manière que nous avons utilisé `max` dans le bras `match` correspondant. Le code dans le bloc `if let` ne s'exécute que si la valeur correspond au motif.

Utiliser `if let` signifie moins de saisie, moins d'indentation et moins de code d’entête. Cependant, vous perdez la vérification exhaustive que `match` impose, ce qui garantit que vous ne négligez aucun cas. Le choix entre `match` et `if let` dépend de ce que vous faites dans votre situation particulière et si gagner en concision est un compromis approprié pour perdre la vérification exhaustive.

En d'autres termes, vous pouvez considérer `if let` comme du sucre syntaxique pour un `match` qui exécute du code lorsque la valeur correspond à un motif et ignore ensuite toutes les autres valeurs.

Nous pouvons inclure un `else` avec un `if let`. Le bloc de code qui va avec le `else` est le même que celui qui irait avec le cas `_` dans l'expression `match` qui est équivalente au `if let` et `else`. Rappelons la définition de l'énumération `Coin` dans la Liste 6-4, où la variante `Quarter` contient également une valeur `UsState`. Si nous voulions compter tous les autres types de pièces que nous voyons tout en annonçant l'état des quarts, nous pourrions le faire avec une expression `match`, comme ceci :

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-13-count-and-announce-match/src/main.rs:here}}
```

Ou nous pourrions utiliser une expression `if let` et `else`, comme ceci :

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-14-count-and-announce-if-let-else/src/main.rs:here}}
```

## Rester sur le "Chemin Heureux" avec `let...else`

Le schéma courant consiste à effectuer un calcul lorsqu'une valeur est présente et à renvoyer une valeur par défaut sinon. Poursuivant avec notre exemple de pièces contenant une valeur `UsState`, si nous voulions dire quelque chose de drôle en fonction de l'âge de l'état sur le quart, nous pourrions introduire une méthode sur `UsState` pour vérifier l'âge d'un état, comme suit :

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-07/src/main.rs:state}}
```

Puis, nous pourrions utiliser `if let` pour correspondre au type de pièce, introduisant une variable `state` dans le corps de la condition, comme dans la Liste 6-7.

<Liste numéro="6-7" légende="Vérifier si un état existait en 1900 en utilisant des conditionnels imbriqués à l'intérieur d'un `if let`">

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-07/src/main.rs:describe}}
```

</Liste>

Cela fait le travail, mais cela a déplacé la charge de travail dans le corps de l'instruction `if let`, et si le travail à effectuer est plus compliqué, il peut être difficile de suivre exactement comment les branches de niveau supérieur se rapportent. Nous pourrions également tirer parti du fait que les expressions produisent une valeur soit pour produire le `state` de `if let`, soit pour retourner tôt, comme dans la Liste 6-8. (Vous pourriez faire quelque chose de similaire avec un `match`, aussi.)

<Liste numéro="6-8" légende="Utiliser `if let` pour produire une valeur ou retourner tôt">

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-08/src/main.rs:describe}}
```

</Liste>

C'est un peu ennuyeux à suivre à sa manière, cependant ! Une branche de l'`if let` produit une valeur, et l'autre retourne complètement de la fonction.

Pour rendre ce schéma courant plus agréable à exprimer, Rust a `let...else`. La syntaxe `let...else` prend un motif sur le côté gauche et une expression sur le droit, très similaire à `if let`, mais elle n'a pas de branche `if`, seulement une branche `else`. Si le motif correspond, il liera la valeur du motif dans la portée extérieure. Si le motif ne correspond pas, le programme passera dans le bras `else`, qui doit retourner de la fonction.

Dans la Liste 6-9, vous pouvez voir à quoi ressemble la Liste 6-8 en utilisant `let...else` à la place de `if let`.

<Liste numéro="6-9" légende="Utiliser `let...else` pour clarifier le flux à travers la fonction">

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-09/src/main.rs:describe}}
```

</Liste>

Remarquez que cela reste sur le "chemin heureux" dans le corps principal de la fonction de cette manière, sans avoir un flux de contrôle significativement différent pour deux branches comme le faisait `if let`.

Si vous avez une situation dans laquelle votre programme a une logique trop verbeuse pour être exprimée à l'aide d'un `match`, rappelez-vous que `if let` et `let...else` sont également dans votre boîte à outils Rust.

## Résumé

Nous avons maintenant couvert comment utiliser des énumérations pour créer des types personnalisés qui peuvent être l’un d’un ensemble de valeurs énumérées. Nous avons montré comment le type `Option<T>` de la bibliothèque standard vous aide à utiliser le système de types pour prévenir les erreurs. Lorsque les valeurs d'énumération contiennent des données, vous pouvez utiliser `match` ou `if let` pour extraire et utiliser ces valeurs, selon le nombre de cas que vous devez gérer.

Vos programmes Rust peuvent maintenant exprimer des concepts dans votre domaine en utilisant des structures et des énumérations. Créer des types personnalisés à utiliser dans votre API garantit la sécurité des types : le compilateur s'assurera que vos fonctions ne reçoivent que des valeurs du type que chaque fonction attend.

Pour fournir une API bien organisée à vos utilisateurs qui est simple à utiliser et n'expose que ce dont vos utilisateurs auront besoin, tournons-nous maintenant vers les modules de Rust.