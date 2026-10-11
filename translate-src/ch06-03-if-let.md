## Flux de contrôle concis avec `if let` et `let...else`

La syntaxe `if let` permet de combiner `if` et `let` pour gérer des valeurs correspondant à un motif tout en ignorant les autres, de manière plus concise. Considérons le programme de la liste 6-6, qui effectue un `match` sur une valeur `Option<u8>` dans la variable `config_max`, mais ne veut exécuter du code que si la valeur est la variante `Some`.

<Listing number="6-6" caption="Un `match` qui n’exécute du code que lorsque la valeur est `Some`">

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-06/src/main.rs:here}}
```

</Listing>

Si la valeur est `Some`, nous affichons la valeur de la variante `Some` en liant cette valeur à la variable `max` dans le motif. Nous ne voulons rien faire avec la valeur `None`. Pour satisfaire l’expression `match`, nous devons ajouter `_ => ()` après avoir traité une seule variante, ce qui constitue du code passe-partout assez agaçant à ajouter.

Nous pourrions plutôt écrire cela de façon plus concise avec `if let`. Le code suivant se comporte comme le `match` de la liste 6-6 :

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-12-if-let/src/main.rs:here}}
```

La syntaxe `if let` prend un motif et une expression séparés par un signe égal. Elle fonctionne comme un `match` : l’expression est transmise au `match` et le motif en constitue le premier bras. Dans ce cas, le motif est `Some(max)`, et `max` est lié à la valeur contenue dans `Some`. Nous pouvons ensuite utiliser `max` dans le corps du bloc `if let`, comme nous l’avons fait dans le bras `match` correspondant. Le code du bloc `if let` ne s’exécute que si la valeur correspond au motif.

Utiliser `if let` signifie moins de frappe, moins d’indentation et moins de code passe-partout. Cependant, vous perdez la vérification exhaustive imposée par `match`, qui garantit que vous n’oubliez pas de traiter un cas. Le choix entre `match` et `if let` dépend de ce que vous faites dans votre situation particulière et du fait que gagner en concision constitue ou non un compromis acceptable face à la perte de la vérification exhaustive.

Autrement dit, vous pouvez considérer `if let` comme du sucre syntaxique pour un `match` qui exécute du code lorsque la valeur correspond à un motif et ignore toutes les autres valeurs.

Nous pouvons ajouter un `else` à un `if let`. Le bloc de code associé à `else` est le même que celui qui serait associé au cas `_` dans l’expression `match` équivalente à `if let` et `else`. Rappelez-vous la définition de l’énumération `Coin` dans la liste 6-4, où la variante `Quarter` contenait également une valeur `UsState`. Si nous voulions compter toutes les pièces autres que des pièces de 25 cents que nous voyons, tout en annonçant l’État correspondant à chaque pièce de 25 cents, nous pourrions utiliser une expression `match`, comme ceci :

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-13-count-and-announce-match/src/main.rs:here}}
```

Ou nous pourrions utiliser une expression `if let` et `else`, comme ceci :

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-14-count-and-announce-if-let-else/src/main.rs:here}}
```

## Rester sur le « chemin heureux » avec `let...else`

Le schéma courant consiste à effectuer un calcul lorsqu’une valeur est présente et à renvoyer une valeur par défaut dans le cas contraire. Pour reprendre notre exemple de pièces contenant une valeur `UsState`, si nous voulions dire quelque chose de drôle en fonction de l’ancienneté de l’État inscrit sur la pièce de 25 cents, nous pourrions ajouter une méthode à `UsState` pour vérifier l’âge d’un État, comme ceci :

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-07/src/main.rs:state}}
```

Ensuite, nous pourrions utiliser `if let` pour vérifier le type de pièce, en introduisant une variable `state` dans le corps de la condition, comme dans la liste 6-7.

<Listing number="6-7" caption="Vérifier si un État existait en 1900 à l’aide de conditions imbriquées dans un `if let`">

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-07/src/main.rs:describe}}
```

</Listing>

Cela fonctionne, mais le traitement est repoussé dans le corps de l’instruction `if let`. Si le traitement à effectuer est plus complexe, il peut être difficile de comprendre précisément comment les branches de premier niveau sont liées entre elles. Nous pourrions aussi tirer parti du fait que les expressions produisent une valeur, soit pour produire `state` à partir de `if let`, soit pour quitter la fonction prématurément, comme dans la liste 6-8. (Vous pourriez faire quelque chose de similaire avec un `match`.)

<Listing number="6-8" caption="Utiliser `if let` pour produire une valeur ou quitter prématurément">

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-08/src/main.rs:describe}}
```

</Listing>

Mais cette approche est assez difficile à suivre à sa manière ! Une branche de `if let` produit une valeur, tandis que l’autre quitte entièrement la fonction.

Pour exprimer plus agréablement ce schéma courant, Rust propose `let...else`. La syntaxe `let...else` prend un motif à gauche et une expression à droite, comme `if let`, mais elle ne possède pas de branche `if`, seulement une branche `else`. Si le motif correspond, elle lie la valeur correspondante dans la portée externe. Si le motif ne correspond _pas_, le programme passe au bras `else`, qui doit quitter la fonction.

Dans la liste 6-9, vous pouvez voir à quoi ressemble la liste 6-8 avec `let...else` à la place de `if let`.

<Listing number="6-9" caption="Utiliser `let...else` pour clarifier le déroulement de la fonction">

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-09/src/main.rs:describe}}
```

</Listing>

Remarquez qu’ainsi, le corps principal de la fonction reste sur le « chemin heureux », sans flux de contrôle sensiblement différent entre les deux branches, contrairement à ce qui se passait avec `if let`.

Si votre programme comporte une logique trop verbeuse pour être exprimée avec un `match`, n’oubliez pas que `if let` et `let...else` font également partie de votre boîte à outils Rust.

## Résumé

Nous avons vu comment utiliser les énumérations pour créer des types personnalisés pouvant prendre l’une des valeurs d’un ensemble énuméré. Nous avons montré comment le type `Option<T>` de la bibliothèque standard vous aide à utiliser le système de types pour éviter les erreurs. Lorsque les valeurs d’une énumération contiennent des données, vous pouvez utiliser `match` ou `if let` pour extraire et utiliser ces valeurs, selon le nombre de cas à traiter.

Vos programmes Rust peuvent désormais représenter les concepts de votre domaine à l’aide de structures et d’énumérations. Créer des types personnalisés à utiliser dans votre API garantit la sûreté des types : le compilateur s’assurera que vos fonctions ne reçoivent que des valeurs du type attendu par chacune d’elles.

Pour fournir à vos utilisateurs une API bien organisée, facile à utiliser et qui n’expose que ce dont ils ont besoin, intéressons-nous maintenant aux modules de Rust.