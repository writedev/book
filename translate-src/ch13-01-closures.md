<!-- Old headings. Do not remove or links may break. -->

<a id="closures-anonymous-functions-that-can-capture-their-environment"></a>
<a id="closures-anonymous-functions-that-capture-their-environment"></a>

## Fermetures

Les fermetures de Rust sont des fonctions anonymes que vous pouvez enregistrer dans une variable ou transmettre en argument à d’autres fonctions. Vous pouvez créer la fermeture à un endroit, puis l’appeler ailleurs pour l’évaluer dans un contexte différent. Contrairement aux fonctions, les fermetures peuvent capturer des valeurs de la portée dans laquelle elles sont définies. Nous allons montrer comment ces caractéristiques des fermetures permettent de réutiliser du code et de personnaliser son comportement.

<!-- Old headings. Do not remove or links may break. -->

<a id="creating-an-abstraction-of-behavior-with-closures"></a>
<a id="refactoring-using-functions"></a>
<a id="refactoring-with-closures-to-store-code"></a>
<a id="capturing-the-environment-with-closures"></a>

### Capturer l’environnement

Nous allons d’abord examiner comment utiliser les fermetures pour capturer des valeurs de l’environnement dans lequel elles sont définies, afin de les utiliser ultérieurement. Voici le scénario : de temps à autre, notre entreprise de tee-shirts offre à une personne de sa liste de diffusion un tee-shirt exclusif en édition limitée dans le cadre d’une promotion. Les personnes inscrites sur la liste de diffusion peuvent ajouter facultativement leur couleur préférée à leur profil. Si la personne choisie pour recevoir un tee-shirt gratuit a indiqué sa couleur préférée, elle recevra un tee-shirt de cette couleur. Si elle n’a pas indiqué de couleur préférée, elle recevra la couleur dont l’entreprise a actuellement le plus grand stock.

Il existe de nombreuses façons de mettre cela en œuvre. Pour cet exemple, nous allons utiliser une énumération appelée `ShirtColor`, qui comporte les variantes `Red` et `Blue` (pour limiter le nombre de couleurs disponibles par souci de simplicité). Nous représentons le stock de l’entreprise avec une structure `Inventory` qui possède un champ nommé `shirts` contenant un `Vec<ShirtColor>` représentant les couleurs des tee-shirts actuellement en stock. La méthode `giveaway` définie sur `Inventory` récupère la préférence facultative de couleur de la personne qui gagne le tee-shirt gratuit et renvoie la couleur qu’elle recevra. Cette configuration est présentée dans le Listing 13-1.

<Listing number="13-1" file-name="src/main.rs" caption="Situation de l’offre promotionnelle de l’entreprise de tee-shirts">

```rust,noplayground
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-01/src/main.rs}}
```

</Listing>

Le `store` défini dans `main` contient encore deux tee-shirts bleus et un tee-shirt rouge à distribuer dans le cadre de cette promotion en édition limitée. Nous appelons la méthode `giveaway` pour une personne qui préfère les tee-shirts rouges et pour une personne qui n’a exprimé aucune préférence.

Encore une fois, ce code pourrait être mis en œuvre de nombreuses façons. Ici, pour nous concentrer sur les fermetures, nous nous en sommes tenus aux concepts que vous avez déjà appris, à l’exception du corps de la méthode `giveaway`, qui utilise une fermeture. Dans la méthode `giveaway`, nous récupérons la préférence de la personne sous la forme d’un paramètre de type `Option<ShirtColor>` et appelons la méthode `unwrap_or_else` sur `user_preference`. La [méthode `unwrap_or_else` de `Option<T>`][unwrap-or-else]<!-- ignore --> est définie par la bibliothèque standard. Elle prend un argument : une fermeture sans argument qui renvoie une valeur `T` (le même type que celui stocké dans la variante `Some` de `Option<T>`, dans ce cas `ShirtColor`). Si `Option<T>` est la variante `Some`, `unwrap_or_else` renvoie la valeur qu’elle contient. Si `Option<T>` est la variante `None`, `unwrap_or_else` appelle la fermeture et renvoie la valeur qu’elle produit.

Nous indiquons l’expression de fermeture `|| self.most_stocked()` comme argument de `unwrap_or_else`. Il s’agit d’une fermeture qui ne prend aucun paramètre (si elle en avait, ils apparaîtraient entre les deux barres verticales). Le corps de la fermeture appelle `self.most_stocked()`. Nous définissons la fermeture ici, et l’implémentation de `unwrap_or_else` l’évaluera plus tard si le résultat est nécessaire.

L’exécution de ce code affiche :

```console
{{#include ../listings/ch13-functional-features/listing-13-01/output.txt}}
```

Un aspect intéressant de cet exemple est que nous avons transmis une fermeture qui appelle `self.most_stocked()` sur l’instance `Inventory` actuelle. La bibliothèque standard n’avait pas besoin de connaître les types `Inventory` ou `ShirtColor` que nous avons définis, ni la logique que nous voulions utiliser dans ce scénario. La fermeture capture une référence immuable à l’instance `Inventory` `self` et la transmet, avec le code que nous avons indiqué, à la méthode `unwrap_or_else`. Les fonctions, en revanche, ne peuvent pas capturer leur environnement de cette manière.

<!-- Old headings. Do not remove or links may break. -->

<a id="closure-type-inference-and-annotation"></a>

### Inférence et annotation des types des fermetures

Il existe d’autres différences entre les fonctions et les fermetures. En général, les fermetures ne nécessitent pas l’annotation des types de leurs paramètres ni de leur valeur de retour, contrairement aux fonctions `fn`. Les annotations de type sont obligatoires pour les fonctions, car leurs types font partie d’une interface explicite exposée aux utilisateurs. Définir cette interface de manière stricte est important pour garantir que tout le monde s’accorde sur les types de valeurs qu’une fonction utilise et renvoie. Les fermetures, en revanche, ne sont pas utilisées dans une interface exposée de cette manière : elles sont stockées dans des variables et utilisées sans être nommées ni exposées aux utilisateurs de notre bibliothèque.

Les fermetures sont généralement courtes et ne sont pertinentes que dans un contexte restreint, plutôt que dans n’importe quelle situation. Dans ces contextes limités, le compilateur peut inférer les types des paramètres et le type de retour, tout comme il peut inférer les types de la plupart des variables (il arrive rarement que le compilateur ait également besoin d’annotations de type pour les fermetures).

Comme pour les variables, nous pouvons ajouter des annotations de type si nous souhaitons plus de précision et de clarté, au prix d’une syntaxe plus verbeuse que nécessaire. L’annotation des types d’une fermeture ressemblerait à la définition présentée dans le Listing 13-2. Dans cet exemple, nous définissons une fermeture et la stockons dans une variable, plutôt que de la définir à l’endroit où nous la transmettons en argument, comme nous l’avons fait dans le Listing 13-1.

<Listing number="13-2" file-name="src/main.rs" caption="Ajout d’annotations de type facultatives aux types des paramètres et de la valeur de retour de la fermeture">

```rust
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-02/src/main.rs:here}}
```

</Listing>

Avec les annotations de type, la syntaxe des fermetures ressemble davantage à celle des fonctions. Ici, nous définissons une fonction qui ajoute 1 à son paramètre et une fermeture qui a le même comportement, à titre de comparaison. Nous avons ajouté des espaces pour aligner les parties correspondantes. Cet exemple illustre la similarité entre la syntaxe des fermetures et celle des fonctions, à l’exception de l’utilisation des barres verticales et du fait que certaines parties de la syntaxe sont facultatives :

```rust,ignore
fn  add_one_v1   (x: u32) -> u32 { x + 1 }
let add_one_v2 = |x: u32| -> u32 { x + 1 };
let add_one_v3 = |x|             { x + 1 };
let add_one_v4 = |x|               x + 1  ;
```

La première ligne montre une définition de fonction et la deuxième, une définition de fermeture entièrement annotée. Dans la troisième ligne, nous supprimons les annotations de type de la définition de la fermeture. Dans la quatrième ligne, nous supprimons les accolades, qui sont facultatives puisque le corps de la fermeture ne contient qu’une seule expression. Ces définitions sont toutes valides et produisent le même comportement lorsqu’elles sont appelées. Les lignes `add_one_v3` et `add_one_v4` nécessitent que les fermetures soient évaluées pour pouvoir compiler, car les types seront inférés à partir de leur utilisation. C’est similaire à `let v = Vec::new();`, qui nécessite soit des annotations de type, soit l’insertion dans le `Vec` de valeurs d’un certain type pour que Rust puisse en inférer le type.

Pour les définitions de fermetures, le compilateur infère un type concret pour chacun de leurs paramètres et pour leur valeur de retour. Par exemple, le Listing 13-3 montre la définition d’une courte fermeture qui renvoie simplement la valeur qu’elle reçoit comme paramètre. Cette fermeture n’est pas très utile, hormis pour les besoins de cet exemple. Remarquez que nous n’avons ajouté aucune annotation de type à la définition. Comme il n’y a pas d’annotations de type, nous pouvons appeler la fermeture avec n’importe quel type, comme nous l’avons fait ici avec `String` la première fois. Si nous essayons ensuite d’appeler `example_closure` avec un entier, nous obtiendrons une erreur.

<Listing number="13-3" file-name="src/main.rs" caption="Tentative d’appel d’une fermeture dont les types sont inférés avec deux types différents">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-03/src/main.rs:here}}
```

</Listing>

Le compilateur nous renvoie cette erreur :

```console
{{#include ../listings/ch13-functional-features/listing-13-03/output.txt}}
```

La première fois que nous appelons `example_closure` avec la valeur `String`, le compilateur infère que le type de `x` et le type de retour de la fermeture sont `String`. Ces types sont alors fixés pour la fermeture dans `example_closure`, et nous obtenons une erreur de type lorsque nous essayons ensuite d’utiliser un type différent avec la même fermeture.

### Capturer des références ou transférer la propriété

Les fermetures peuvent capturer des valeurs de leur environnement de trois façons, qui correspondent directement aux trois façons dont une fonction peut prendre un paramètre : emprunter de manière immuable, emprunter de manière mutable et prendre possession. La fermeture choisit laquelle de ces façons utiliser en fonction de ce que le corps de la fonction fait avec les valeurs capturées.

Dans le Listing 13-4, nous définissons une fermeture qui capture une référence immuable au vecteur nommé `list`, car elle n’a besoin que d’une référence immuable pour afficher la valeur.

<Listing number="13-4" file-name="src/main.rs" caption="Définition et appel d’une fermeture qui capture une référence immuable">

```rust
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-04/src/main.rs}}
```

</Listing>

Cet exemple montre également qu’une variable peut être liée à une définition de fermeture, et que nous pouvons ensuite appeler la fermeture en utilisant le nom de la variable suivi de parenthèses, comme si ce nom était celui d’une fonction.

Comme nous pouvons avoir plusieurs références immuables à `list` en même temps, `list` reste accessible dans le code avant la définition de la fermeture, après sa définition mais avant son appel, et après son appel. Ce code compile, s’exécute et affiche :

```console
{{#include ../listings/ch13-functional-features/listing-13-04/output.txt}}
```

Ensuite, dans le Listing 13-5, nous modifions le corps de la fermeture afin qu’il ajoute un élément au vecteur `list`. La fermeture capture désormais une référence mutable.

<Listing number="13-5" file-name="src/main.rs" caption="Définition et appel d’une fermeture qui capture une référence mutable">

```rust
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-05/src/main.rs}}
```

</Listing>

Ce code compile, s’exécute et affiche :

```console
{{#include ../listings/ch13-functional-features/listing-13-05/output.txt}}
```

Remarquez qu’il n’y a plus de `println!` entre la définition et l’appel de la fermeture `borrows_mutably` : lorsqu’elle est définie, `borrows_mutably` capture une référence mutable à `list`. Nous n’utilisons plus la fermeture après l’avoir appelée, donc l’emprunt mutable prend fin. Entre la définition de la fermeture et son appel, un emprunt immuable pour afficher la valeur n’est pas autorisé, car aucun autre emprunt n’est permis lorsqu’il y a un emprunt mutable. Essayez d’ajouter un `println!` à cet endroit pour voir le message d’erreur obtenu !

Si vous souhaitez forcer la fermeture à prendre possession des valeurs qu’elle utilise dans l’environnement, même si son corps n’a pas strictement besoin de cette propriété, vous pouvez utiliser le mot-clé `move` avant la liste des paramètres.

Cette technique est surtout utile lorsqu’on transmet une fermeture à un nouveau thread afin de déplacer les données et qu’elles appartiennent au nouveau thread. Nous aborderons les threads et les raisons pour lesquelles vous pourriez vouloir les utiliser en détail au Chapitre 16, lorsque nous parlerons de concurrence. Pour l’instant, explorons brièvement la création d’un nouveau thread à l’aide d’une fermeture qui nécessite le mot-clé `move`. Le Listing 13-6 montre le Listing 13-4 modifié pour afficher le vecteur dans un nouveau thread plutôt que dans le thread principal.

<Listing number="13-6" file-name="src/main.rs" caption="Utilisation de `move` pour forcer la fermeture du thread à prendre possession de `list`">

```rust
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-06/src/main.rs}}
```

</Listing>

Nous créons un nouveau thread en lui transmettant une fermeture à exécuter comme argument. Le corps de la fermeture affiche la liste. Dans le Listing 13-4, la fermeture ne capturait `list` qu’à l’aide d’une référence immuable, car c’est le niveau d’accès minimal nécessaire pour l’afficher. Dans cet exemple, même si le corps de la fermeture n’a toujours besoin que d’une référence immuable, nous devons indiquer que `list` doit être déplacée dans la fermeture en plaçant le mot-clé `move` au début de sa définition. Si le thread principal effectuait d’autres opérations avant d’appeler `join` sur le nouveau thread, ce dernier pourrait se terminer avant que le reste du thread principal ne soit terminé, ou le thread principal pourrait se terminer en premier. Si le thread principal conservait la propriété de `list` mais se terminait avant le nouveau thread et supprimait `list`, la référence immuable du thread ne serait plus valide. Le compilateur exige donc que `list` soit déplacée dans la fermeture transmise au nouveau thread, afin que la référence reste valide. Essayez de supprimer le mot-clé `move` ou d’utiliser `list` dans le thread principal après la définition de la fermeture pour voir les erreurs du compilateur !

<!-- Old headings. Do not remove or links may break. -->

<a id="storing-closures-using-generic-parameters-and-the-fn-traits"></a>
<a id="limitations-of-the-cacher-implementation"></a>
<a id="moving-captured-values-out-of-the-closure-and-the-fn-traits"></a>
<a id="moving-captured-values-out-of-closures-and-the-fn-traits"></a>

### Déplacer les valeurs capturées hors des fermetures

Une fois qu’une fermeture a capturé une référence ou pris possession d’une valeur provenant de l’environnement dans lequel elle est définie (ce qui détermine si quelque chose est déplacé _dans_ la fermeture), le code du corps de la fermeture définit ce qui arrive aux références ou aux valeurs lorsque la fermeture est évaluée plus tard (ce qui détermine si quelque chose est déplacé _hors_ de la fermeture).

Le corps d’une fermeture peut faire l’une des choses suivantes : déplacer une valeur capturée hors de la fermeture, modifier la valeur capturée, ne ni déplacer ni modifier la valeur, ou ne rien capturer de l’environnement au départ.

La façon dont une fermeture capture et traite les valeurs de l’environnement détermine les traits qu’elle implémente. Les traits permettent aux fonctions et aux structures de préciser quels types de fermetures elles peuvent utiliser. Les fermetures implémentent automatiquement un, deux ou les trois traits `Fn`, de manière additive, selon la façon dont leur corps traite les valeurs :

* `FnOnce` s’applique aux fermetures qui peuvent être appelées une seule fois. Toutes les fermetures implémentent au moins ce trait, car elles peuvent toutes être appelées. Une fermeture qui déplace des valeurs capturées hors de son corps n’implémentera que `FnOnce`, et aucun des autres traits `Fn`, car elle ne peut être appelée qu’une seule fois.
* `FnMut` s’applique aux fermetures qui ne déplacent pas les valeurs capturées hors de leur corps, mais qui peuvent modifier les valeurs capturées. Ces fermetures peuvent être appelées plusieurs fois.
* `Fn` s’applique aux fermetures qui ne déplacent pas les valeurs capturées hors de leur corps et ne les modifient pas, ainsi qu’aux fermetures qui ne capturent rien de leur environnement. Ces fermetures peuvent être appelées plusieurs fois sans modifier leur environnement, ce qui est important dans des cas tels que l’appel simultané d’une fermeture à plusieurs reprises.

Examinons la définition de la méthode `unwrap_or_else` de `Option<T>`, que nous avons utilisée dans le Listing 13-1 :

```rust,ignore
impl<T> Option<T> {
    pub fn unwrap_or_else<F>(self, f: F) -> T
    where
        F: FnOnce() -> T
    {
        match self {
            Some(x) => x,
            None => f(),
        }
    }
}
```

Rappelez-vous que `T` est le type générique qui représente le type de la valeur contenue dans la variante `Some` d’un `Option`. Ce type `T` est également le type de retour de la fonction `unwrap_or_else` : le code qui appelle `unwrap_or_else` sur un `Option<String>`, par exemple, obtiendra un `String`.

Ensuite, remarquez que la fonction `unwrap_or_else` possède le paramètre de type générique supplémentaire `F`. Le type `F` est le type du paramètre nommé `f`, qui est la fermeture que nous fournissons lors de l’appel de `unwrap_or_else`.

La contrainte de trait indiquée pour le type générique `F` est `FnOnce() -> T`, ce qui signifie que `F` doit pouvoir être appelé une fois, ne prendre aucun argument et renvoyer un `T`. L’utilisation de `FnOnce` dans la contrainte de trait exprime la restriction selon laquelle `unwrap_or_else` n’appellera pas `f` plus d’une fois. Dans le corps de `unwrap_or_else`, nous voyons que si `Option` est `Some`, `f` ne sera pas appelée. Si `Option` est `None`, `f` sera appelée une fois. Comme toutes les fermetures implémentent `FnOnce`, `unwrap_or_else` accepte les trois types de fermetures et offre ainsi la plus grande flexibilité possible.

> Remarque : si l’opération souhaitée n’exige pas de capturer une valeur de l’environnement, nous pouvons utiliser le nom d’une fonction plutôt qu’une fermeture là où nous avons besoin d’un élément qui implémente l’un des traits `Fn`. Par exemple, sur une valeur `Option<Vec<T>>`, nous pourrions appeler `unwrap_or_else(Vec::new)` pour obtenir un nouveau vecteur vide si la valeur est `None`. Le compilateur implémente automatiquement le trait `Fn` qui convient pour une définition de fonction.

Examinons maintenant la méthode de la bibliothèque standard `sort_by_key`, définie sur les tranches, afin de voir en quoi elle diffère de `unwrap_or_else` et pourquoi `sort_by_key` utilise `FnMut` plutôt que `FnOnce` comme contrainte de trait. La fermeture reçoit un argument sous la forme d’une référence à l’élément courant de la tranche en cours d’examen, et renvoie une valeur de type `K` qui peut être ordonnée. Cette fonction est utile lorsque vous souhaitez trier une tranche selon un attribut particulier de chaque élément. Dans le Listing 13-7, nous avons une liste d’instances de `Rectangle` et nous utilisons `sort_by_key` pour les trier par attribut `width`, de la plus petite à la plus grande valeur.

<Listing number="13-7" file-name="src/main.rs" caption="Utilisation de `sort_by_key` pour trier des rectangles par largeur">

```rust
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-07/src/main.rs}}
```

</Listing>

Ce code affiche :

```console
{{#include ../listings/ch13-functional-features/listing-13-07/output.txt}}
```

Si `sort_by_key` est définie pour recevoir une fermeture `FnMut`, c’est parce qu’elle appelle la fermeture plusieurs fois : une fois pour chaque élément de la tranche. La fermeture `|r| r.width` ne capture, ne modifie et ne déplace rien de son environnement ; elle respecte donc les contraintes du trait.

En revanche, le Listing 13-8 montre un exemple de fermeture qui n’implémente que le trait `FnOnce`, car elle déplace une valeur hors de l’environnement. Le compilateur ne nous laissera pas utiliser cette fermeture avec `sort_by_key`.

<Listing number="13-8" file-name="src/main.rs" caption="Tentative d’utilisation d’une fermeture `FnOnce` avec `sort_by_key`">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-08/src/main.rs}}
```

</Listing>

Il s’agit d’une manière artificielle et compliquée (qui ne fonctionne pas) d’essayer de compter le nombre de fois que `sort_by_key` appelle la fermeture lorsqu’elle trie `list`. Ce code tente de faire ce comptage en ajoutant `value` — une `String` provenant de l’environnement de la fermeture — au vecteur `sort_operations`. La fermeture capture `value`, puis la déplace hors de la fermeture en transférant sa propriété au vecteur `sort_operations`. Cette fermeture ne peut être appelée qu’une fois ; une deuxième tentative ne fonctionnerait pas, car `value` ne se trouverait plus dans l’environnement pour être ajoutée à nouveau à `sort_operations` ! Cette fermeture n’implémente donc que `FnOnce`. Lorsque nous essayons de compiler ce code, nous obtenons cette erreur : `value` ne peut pas être déplacée hors de la fermeture, car celle-ci doit implémenter `FnMut` :

```console
{{#include ../listings/ch13-functional-features/listing-13-08/output.txt}}
```

L’erreur indique la ligne du corps de la fermeture qui déplace `value` hors de l’environnement. Pour corriger cela, nous devons modifier le corps de la fermeture afin qu’il ne déplace pas de valeurs hors de l’environnement. Conserver un compteur dans l’environnement et incrémenter sa valeur dans le corps de la fermeture est une manière plus simple de compter le nombre d’appels de la fermeture. La fermeture du Listing 13-9 fonctionne avec `sort_by_key`, car elle ne capture qu’une référence mutable au compteur `num_sort_operations` et peut donc être appelée plusieurs fois.

<Listing number="13-9" file-name="src/main.rs" caption="L’utilisation d’une fermeture `FnMut` avec `sort_by_key` est autorisée.">

```rust
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-09/src/main.rs}}
```

</Listing>

Les traits `Fn` sont importants lorsqu’on définit ou utilise des fonctions ou des types qui exploitent des fermetures. Dans la section suivante, nous parlerons des itérateurs. De nombreuses méthodes d’itérateur prennent des fermetures en argument ; gardez donc ces détails à l’esprit pour la suite !

[unwrap-or-else]: ../std/option/enum.Option.html#method.unwrap_or_else