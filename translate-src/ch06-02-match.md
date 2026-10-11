<!-- Anciennes en-têtes. Ne pas supprimer, sinon les liens risquent de ne plus fonctionner. -->

<a id="the-match-control-flow-operator"></a>

## La construction de contrôle de flux `match`

Rust dispose d’une construction de contrôle de flux extrêmement puissante appelée `match`, qui vous permet de comparer une valeur à une série de motifs, puis d’exécuter du code en fonction du motif qui correspond. Les motifs peuvent être composés de valeurs littérales, de noms de variables, de jokers et de bien d’autres éléments ; le [chapitre 19][ch19-00-patterns]<!-- ignore --> présente tous les types de motifs et leur rôle. La puissance de `match` tient à l’expressivité de ses motifs et au fait que le compilateur vérifie que tous les cas possibles sont traités.

Imaginez qu’une expression `match` fonctionne comme une machine de tri des pièces : les pièces glissent sur une rampe bordée de trous de tailles différentes, et chacune tombe dans le premier trou qu’elle rencontre et dans lequel elle peut passer. De la même manière, les valeurs sont comparées à chaque motif d’un `match` et, dès qu’une valeur « correspond » à un motif, elle est dirigée vers le bloc de code associé pour être utilisée lors de l’exécution.

Puisque nous parlons de pièces, prenons-les comme exemple avec `match` ! Nous pouvons écrire une fonction qui prend une pièce de monnaie américaine inconnue et qui, comme une machine de tri, détermine de quelle pièce il s’agit et renvoie sa valeur en cents, comme le montre la liste 6-3.

<Listing number="6-3" caption="Une énumération et une expression `match` dont les motifs sont les variantes de l’énumération">

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-03/src/main.rs:here}}
```

</Listing>

Examinons le `match` de la fonction `value_in_cents`. Tout d’abord, nous écrivons le mot-clé `match`, suivi d’une expression, qui est ici la valeur `coin`. Cela ressemble beaucoup à une expression conditionnelle utilisant `if`, mais il y a une grande différence : avec `if`, la condition doit être évaluée en une valeur booléenne, alors qu’ici, elle peut être de n’importe quel type. Dans cet exemple, le type de `coin` est l’énumération `Coin`, que nous avons définie à la première ligne.

Viennent ensuite les branches de `match`. Une branche se compose de deux parties : un motif et du code. Le motif de la première branche est la valeur `Coin::Penny`, suivie de l’opérateur `=>`, qui sépare le motif du code à exécuter. Dans ce cas, le code est simplement la valeur `1`. Chaque branche est séparée de la suivante par une virgule.

Lorsque l’expression `match` s’exécute, elle compare la valeur obtenue au motif de chaque branche, dans l’ordre. Si un motif correspond à la valeur, le code associé à ce motif est exécuté. Si le motif ne correspond pas à la valeur, l’exécution passe à la branche suivante, un peu comme dans une machine de tri des pièces. Nous pouvons avoir autant de branches que nécessaire : dans la liste 6-3, notre `match` en compte quatre.

Le code associé à chaque branche est une expression, et la valeur obtenue par l’expression de la branche correspondante est celle qui est renvoyée par l’ensemble de l’expression `match`.

En général, nous n’utilisons pas d’accolades si le code d’une branche de `match` est court, comme dans la liste 6-3, où chaque branche renvoie simplement une valeur. Si vous souhaitez exécuter plusieurs lignes de code dans une branche de `match`, vous devez utiliser des accolades ; la virgule qui suit alors la branche est facultative. Par exemple, le code suivant affiche « Lucky penny! » chaque fois que la méthode est appelée avec une valeur `Coin::Penny`, mais renvoie tout de même la dernière valeur du bloc, `1` :

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-08-match-arm-multiple-lines/src/main.rs:here}}
```

### Motifs qui lient des valeurs

Une autre caractéristique utile des branches de `match` est qu’elles peuvent se lier aux parties des valeurs qui correspondent au motif. C’est ainsi que nous pouvons extraire des valeurs des variantes d’une énumération.

Par exemple, modifions l’une de nos variantes d’énumération pour qu’elle contienne des données. De 1999 à 2008, les États-Unis ont frappé des pièces de 25 cents présentant chacune, sur l’une de leurs faces, un motif différent pour chacun des 50 États. Aucune autre pièce ne portait de motif représentant un État ; seules les pièces de 25 cents possèdent donc cette valeur supplémentaire. Nous pouvons ajouter cette information à notre `enum` en modifiant la variante `Quarter` pour qu’elle contienne une valeur `UsState`, comme nous l’avons fait dans la liste 6-4.

<Listing number="6-4" caption="Une énumération `Coin` dont la variante `Quarter` contient également une valeur `UsState`">

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-04/src/main.rs:here}}
```

</Listing>

Imaginons qu’un ami essaie de collectionner les pièces de 25 cents des 50 États. Pendant que nous trions notre petite monnaie par type de pièce, nous annonçons également le nom de l’État associé à chaque pièce de 25 cents, afin que notre ami puisse l’ajouter à sa collection s’il ne l’a pas encore.

Dans l’expression `match` de ce code, nous ajoutons au motif qui correspond aux valeurs de la variante `Coin::Quarter` une variable appelée `state`. Lorsqu’une valeur `Coin::Quarter` correspond, la variable `state` est liée à la valeur de l’État associé à cette pièce. Nous pouvons ensuite utiliser `state` dans le code de cette branche, comme ceci :

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-09-variable-in-pattern/src/main.rs:here}}
```

Si nous appelions `value_in_cents(Coin::Quarter(UsState::Alaska))`, `coin` aurait la valeur `Coin::Quarter(UsState::Alaska)`. Lorsque nous comparons cette valeur aux différentes branches de `match`, aucune ne correspond avant que nous arrivions à `Coin::Quarter(state)`. À ce moment-là, la liaison de `state` prend la valeur `UsState::Alaska`. Nous pouvons ensuite utiliser cette liaison dans l’expression `println!` et ainsi extraire la valeur interne de l’État de la variante `Quarter` de l’énumération `Coin`.

<!-- Anciennes en-têtes. Ne pas supprimer, sinon les liens risquent de ne plus fonctionner. -->

<a id="matching-with-optiont"></a>

### Le motif `match` de `Option<T>`


Dans la section précédente, nous voulions récupérer la valeur `T` interne au cas `Some` lorsque nous utilisions `Option<T>` ; nous pouvons également traiter `Option<T>` avec `match`, comme nous l’avons fait avec l’énumération `Coin` ! Au lieu de comparer des pièces, nous comparerons les variantes de `Option<T>`, mais le fonctionnement de l’expression `match` reste le même.

Imaginons que nous voulions écrire une fonction qui prend un `Option<i32>` et qui, s’il contient une valeur, lui ajoute 1. Si aucune valeur n’est présente, la fonction doit renvoyer la valeur `None` sans tenter d’effectuer d’opération.

Grâce à `match`, cette fonction est très facile à écrire et ressemblera à la liste 6-5.

<Listing number="6-5" caption="Une fonction qui utilise une expression `match` sur un `Option<i32>`">

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-05/src/main.rs:here}}
```

</Listing>

Examinons plus en détail la première exécution de `plus_one`. Lorsque nous appelons `plus_one(five)`, la variable `x` dans le corps de `plus_one` prend la valeur `Some(5)`. Nous la comparons ensuite à chaque branche de `match` :

```rust,ignore
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-05/src/main.rs:first_arm}}
```

La valeur `Some(5)` ne correspond pas au motif `None`, nous passons donc à la branche suivante :

```rust,ignore
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-05/src/main.rs:second_arm}}
```

Est-ce que `Some(5)` correspond à `Some(i)` ? Oui ! Il s’agit de la même variante. `i` est liée à la valeur contenue dans `Some`, et prend donc la valeur `5`. Le code de la branche de `match` est alors exécuté : nous ajoutons 1 à la valeur de `i` et créons une nouvelle valeur `Some` contenant le total, `6`.

Considérons maintenant le deuxième appel à `plus_one` dans la liste 6-5, où `x` vaut `None`. Nous entrons dans le `match` et comparons la valeur à la première branche :

```rust,ignore
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-05/src/main.rs:first_arm}}
```

Elle correspond ! Il n’y a aucune valeur à laquelle ajouter quelque chose, le programme s’arrête donc et renvoie la valeur `None` située à droite de `=>`. Comme la première branche correspondait, aucune autre branche n’est comparée.

Combiner `match` et les énumérations est utile dans de nombreuses situations. Vous rencontrerez souvent ce motif dans du code Rust : effectuer un `match` sur une énumération, lier une variable aux données qu’elle contient, puis exécuter du code en fonction de ces données. C’est un peu délicat au début, mais une fois que vous vous y serez habitué, vous souhaiterez pouvoir l’utiliser dans tous les langages. C’est une fonctionnalité qui plaît beaucoup aux utilisateurs.

### Les correspondances sont exhaustives

Il nous reste un autre aspect de `match` à aborder : les motifs des branches doivent couvrir toutes les possibilités. Considérez cette version de notre fonction `plus_one`, qui contient un bogue et ne compilera pas :

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-10-non-exhaustive-match/src/main.rs:here}}
```

Nous n’avons pas traité le cas `None`, ce qui entraînera un bogue. Heureusement, Rust sait détecter ce genre de bogue. Si nous essayons de compiler ce code, nous obtiendrons cette erreur :

```console
{{#include ../listings/ch06-enums-and-pattern-matching/no-listing-10-non-exhaustive-match/output.txt}}
```

Rust sait que nous n’avons pas couvert tous les cas possibles et sait même quel motif nous avons oublié ! Les correspondances en Rust sont _exhaustives_ : nous devons épuiser toutes les possibilités pour que le code soit valide. En particulier dans le cas de `Option<T>`, lorsque Rust nous empêche d’oublier de traiter explicitement le cas `None`, il nous protège contre l’hypothèse que nous disposons d’une valeur alors qu’elle pourrait être nulle, évitant ainsi l’erreur à un milliard de dollars évoquée précédemment.

### Les motifs génériques et le caractère générique `_`

Avec les énumérations, nous pouvons également effectuer des actions particulières pour quelques valeurs précises, et une action par défaut pour toutes les autres. Imaginons que nous implémentions un jeu dans lequel, si vous obtenez un 3 en lançant un dé, votre personnage ne se déplace pas, mais reçoit un nouveau chapeau élégant. Si vous obtenez un 7, votre personnage perd un chapeau élégant. Pour toutes les autres valeurs, votre personnage avance d’autant de cases sur le plateau. Voici un `match` qui met en œuvre cette logique. Le résultat du lancer de dé est codé en dur plutôt que d’être aléatoire, et les autres actions sont représentées par des fonctions sans corps, car leur implémentation sort du cadre de cet exemple :

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-15-binding-catchall/src/main.rs:here}}
```

Dans les deux premières branches, les motifs sont les valeurs littérales `3` et `7`. Pour la dernière branche, qui couvre toutes les autres valeurs possibles, le motif est la variable que nous avons choisi d’appeler `other`. Le code de la branche `other` utilise cette variable en la transmettant à la fonction `move_player`.

Ce code compile, même si nous n’avons pas énuméré toutes les valeurs possibles d’un `u8`, car le dernier motif correspond à toutes les valeurs qui ne sont pas spécifiquement indiquées. Ce motif générique répond à l’exigence selon laquelle `match` doit être exhaustif. Notez que nous devons placer la branche générique en dernier, car les motifs sont évalués dans l’ordre. Si nous avions placé cette branche plus tôt, les autres branches ne seraient jamais exécutées ; Rust nous avertit donc si nous ajoutons des branches après une branche générique !

Rust propose également un motif que nous pouvons utiliser lorsque nous souhaitons prévoir un cas générique sans _utiliser_ la valeur correspondante : `_` est un motif spécial qui correspond à n’importe quelle valeur sans s’y lier. Cela indique à Rust que nous n’allons pas utiliser cette valeur ; Rust ne nous avertira donc pas qu’une variable est inutilisée.

Modifions les règles du jeu : désormais, si vous obtenez autre chose qu’un 3 ou un 7, vous devez relancer le dé. Nous n’avons plus besoin d’utiliser la valeur générique ; nous pouvons donc remplacer la variable appelée `other` par `_` dans notre code :

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-16-underscore-catchall/src/main.rs:here}}
```

Cet exemple respecte également l’exigence d’exhaustivité, car nous ignorons explicitement toutes les autres valeurs dans la dernière branche ; nous n’avons rien oublié.

Enfin, modifions une dernière fois les règles du jeu : rien d’autre ne se passe pendant votre tour si vous obtenez autre chose qu’un 3 ou un 7. Nous pouvons exprimer cela en utilisant la valeur unitaire (le type tuple vide mentionné dans la section [« Le type tuple »][tuples]<!-- ignore -->) comme code associé à la branche `_` :

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-17-underscore-unit/src/main.rs:here}}
```

Ici, nous indiquons explicitement à Rust que nous n’allons utiliser aucune autre valeur ne correspondant pas à un motif dans une branche précédente et que nous ne souhaitons exécuter aucun code dans ce cas.

Nous aborderons plus en détail les motifs et les correspondances au [chapitre 19][ch19-00-patterns]<!-- ignore -->. Pour l’instant, nous allons passer à la syntaxe `if let`, qui peut être utile lorsque l’expression `match` est un peu trop longue.

[tuples]: ch03-02-data-types.html#the-tuple-type
[ch19-00-patterns]: ch19-00-patterns.html