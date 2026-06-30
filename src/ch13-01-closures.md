<!-- Anciennes titres. Ne pas supprimer sinon les liens peuvent être cassés. -->

<a id="closures-anonymous-functions-that-can-capture-their-environment"></a>
<a id="closures-anonymous-functions-that-can-capture-their-environment"></a>

## Fermetures

Les fermetures de Rust sont des fonctions anonymes que vous pouvez enregistrer dans une variable ou passer comme arguments à d'autres fonctions. Vous pouvez créer la fermeture à un endroit et ensuite l'appeler ailleurs pour l'évaluer dans un contexte différent. Contrairement aux fonctions, les fermetures peuvent capturer des valeurs du scope dans lequel elles sont définies. Nous allons démontrer comment ces caractéristiques des fermetures permettent la réutilisation de code et la personnalisation du comportement.

<!-- Anciennes titres. Ne pas supprimer sinon les liens peuvent être cassés. -->

<a id="creating-an-abstraction-of-behavior-with-closures"></a>
<a id="refactoring-using-functions"></a>
<a id="refactoring-with-closures-to-store-code"></a>
<a id="capturing-the-environment-with-closures"></a>

### Capturer l'environnement

Nous allons d'abord examiner comment nous pouvons utiliser des fermetures pour capturer des valeurs de l'environnement dans lequel elles sont définies pour une utilisation ultérieure. Voici le scénario : De temps en temps, notre entreprise de T-shirts offre un t-shirt exclusif en édition limitée à quelqu'un sur notre liste de diffusion en tant que promotion. Les personnes sur la liste de diffusion peuvent éventuellement ajouter leur couleur préférée à leur profil. Si la personne choisie pour un t-shirt gratuit a spécifié sa couleur préférée, elle reçoit un t-shirt de cette couleur. Si la personne n'a pas précisé de couleur préférée, elle reçoit la couleur que l'entreprise a actuellement en plus grande quantité.

Il existe de nombreuses façons de mettre cela en œuvre. Pour cet exemple, nous allons utiliser une énumération appelée `ShirtColor` qui a les variantes `Red` et `Blue` (limitant le nombre de couleurs disponibles pour des raisons de simplicité). Nous représentons l'inventaire de l'entreprise avec une structure `Inventory` qui a un champ nommé `shirts` contenant un `Vec<ShirtColor>` représentant les couleurs de t-shirts actuellement en stock. La méthode `giveaway` définie sur `Inventory` obtient la préférence de couleur de t-shirt optionnelle du gagnant du t-shirt gratuit, et elle renvoie la couleur de t-shirt que la personne recevra. Ce dispositif est illustré dans l'Listing 13-1.

<Listing number="13-1" file-name="src/main.rs" caption="Situation de cadeau de l'entreprise de T-shirts">

```rust,noplayground
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-01/src/main.rs}}
```

</Listing>

Le `store` défini dans `main` a deux t-shirts bleus et un t-shirt rouge restants à distribuer pour cette promotion en édition limitée. Nous appelons la méthode `giveaway` pour un utilisateur avec une préférence pour un t-shirt rouge et un utilisateur sans préférence.

Encore une fois, ce code pourrait être mis en œuvre de nombreuses manières, et ici, pour se concentrer sur les fermetures, nous nous sommes en tenus à des concepts que vous avez déjà appris, sauf pour le corps de la méthode `giveaway` qui utilise une fermeture. Dans la méthode `giveaway`, nous obtenons la préférence de l'utilisateur comme paramètre de type `Option<ShirtColor>` et appelons la méthode `unwrap_or_else` sur `user_preference`. La méthode [`unwrap_or_else` sur `Option<T>`][unwrap-or-else]<!-- ignore --> est définie par la bibliothèque standard. Elle prend un argument : une fermeture sans arguments qui renvoie une valeur `T` (le même type stocké dans la variante `Some` de l' `Option<T>`, dans ce cas `ShirtColor`). Si l' `Option<T>` est la variante `Some`, `unwrap_or_else` renvoie la valeur de l'intérieur du `Some`. Si l' `Option<T>` est la variante `None`, `unwrap_or_else` appelle la fermeture et renvoie la valeur retournée par la fermeture.

Nous spécifions l'expression de fermeture `|| self.most_stocked()` comme argument de `unwrap_or_else`. C'est une fermeture qui ne prend pas de paramètres elle-même (si la fermeture avait des paramètres, ils apparaîtraient entre les deux barres verticales). Le corps de la fermeture appelle `self.most_stocked()`. Nous définissons la fermeture ici, et l'implémentation de `unwrap_or_else` évaluera la fermeture plus tard si le résultat est nécessaire.

L'exécution de ce code imprime ce qui suit :

```console
{{#include ../listings/ch13-functional-features/listing-13-01/output.txt}}
```

Un aspect intéressant ici est que nous avons passé une fermeture qui appelle `self.most_stocked()` sur l'instance `Inventory` actuelle. La bibliothèque standard n'a pas besoin de connaître quoi que ce soit sur les types `Inventory` ou `ShirtColor` que nous avons définis, ni la logique que nous voulons utiliser dans ce scénario. La fermeture capture une référence immuable à l'instance `Inventory` `self` et la passe avec le code que nous spécifions à la méthode `unwrap_or_else`. Les fonctions, en revanche, ne peuvent pas capturer leur environnement de cette manière.

<!-- Anciennes titres. Ne pas supprimer sinon les liens peuvent être cassés. -->

<a id="closure-type-inference-and-annotation"></a>

### Inférence et annotation des types de fermeture

Il existe d'autres différences entre les fonctions et les fermetures. Les fermetures ne nécessitent généralement pas que vous annotiez les types des paramètres ou de la valeur de retour comme le font les fonctions `fn`. Les annotations de type sont requises sur les fonctions parce que les types font partie d'une interface explicite exposée à vos utilisateurs. La définition rigide de cette interface est importante pour garantir que tout le monde s'accorde sur les types de valeurs qu'une fonction utilise et renvoie. Les fermetures, en revanche, ne sont pas utilisées dans une interface exposée de cette manière : elles sont stockées dans des variables et utilisent sans les nommer et les exposer aux utilisateurs de notre bibliothèque.

Les fermetures sont généralement courtes et pertinentes uniquement dans un contexte étroit plutôt que dans un scénario arbitraire. Dans ces contextes limités, le compilateur peut inférer les types des paramètres et le type de retour, de manière similaire à la façon dont il peut inférer les types de la plupart des variables (il existe des cas rares où le compilateur a également besoin d'annotations de type pour les fermetures).

Comme pour les variables, nous pouvons ajouter des annotations de type si nous voulons augmenter l'explicité et la clarté au prix d'être plus verbeux que ce qui est strictement nécessaire. Annoter les types d'une fermeture ressemblerait à la définition montrée dans l'Listing 13-2. Dans cet exemple, nous définissons une fermeture et la stockons dans une variable plutôt que de la définir à l'endroit où nous la passons en argument, comme nous l'avons fait dans l'Listing 13-1.

<Listing number="13-2" file-name="src/main.rs" caption="Ajout d'annotations de type optionnelles des paramètres et des types de valeurs de retour dans la fermeture">

```rust
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-02/src/main.rs:here}}
```

</Listing>

Avec les annotations de type ajoutées, la syntaxe des fermetures ressemble un peu plus à la syntaxe des fonctions. Ici, nous définissons une fonction qui ajoute 1 à son paramètre et une fermeture qui a le même comportement, pour comparaison. Nous avons ajouté quelques espaces pour aligner les parties pertinentes. Cela illustre comment la syntaxe de fermeture est similaire à la syntaxe de fonction, sauf pour l'utilisation de barres verticales et le montant de syntaxe qui est facultatif :

```rust,ignore
fn  add_one_v1   (x: u32) -> u32 { x + 1 }
let add_one_v2 = |x: u32| -> u32 { x + 1 };
let add_one_v3 = |x|             { x + 1 };
let add_one_v4 = |x|               x + 1  ;
```

La première ligne montre une définition de fonction et la deuxième ligne montre une définition de fermeture entièrement annotée. Dans la troisième ligne, nous supprimons les annotations de type de la définition de la fermeture. Dans la quatrième ligne, nous supprimons les crochets, qui sont facultatifs parce que le corps de la fermeture ne contient qu'une seule expression. Ce sont toutes des définitions valides qui produiront le même comportement lorsqu'elles seront appelées. Les lignes `add_one_v3` et `add_one_v4` nécessitent que les fermetures soient évaluées pour pouvoir être compilées, car les types seront inférés de leur utilisation. C'est similaire à `let v = Vec::new();` nécessitant soit des annotations de type, soit des valeurs de quelque type que ce soit pour être insérées dans le `Vec` afin que Rust puisse inférer le type.

Pour les définitions de fermetures, le compilateur inférera un type concret pour chacun de leurs paramètres et pour leur valeur de retour. Par exemple, l'Listing 13-3 montre la définition d'une courte fermeture qui renvoie simplement la valeur qu'elle reçoit en paramètre. Cette fermeture n'est pas très utile sauf dans le cadre de cet exemple. Notez que nous n'avons ajouté aucune annotation de type à la définition. Puisqu'il n'y a pas d'annotations de type, nous pouvons appeler la fermeture avec n'importe quel type, ce que nous avons fait ici avec `String` la première fois. Si nous essayons ensuite d'appeler `example_closure` avec un entier, nous obtiendrons une erreur.

<Listing number="13-3" file-name="src/main.rs" caption="Tentative d'appel d'une fermeture dont les types sont inférés avec deux types différents">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-03/src/main.rs:here}}
```

</Listing>

Le compilateur nous donne cette erreur :

```console
{{#include ../listings/ch13-functional-features/listing-13-03/output.txt}}
```

La première fois que nous appelons `example_closure` avec la valeur `String`, le compilateur infère le type de `x` et le type de retour de la fermeture comme étant `String`. Ces types sont ensuite verrouillés dans la fermeture dans `example_closure`, et nous obtenons une erreur de type lorsque nous essayons d'utiliser un type différent avec la même fermeture.

### Capturer des références ou déplacer la propriété

Les fermetures peuvent capturer des valeurs de leur environnement de trois manières, qui correspondent directement aux trois manières qu'une fonction peut prendre un paramètre : emprunter de manière immuable, emprunter de manière mutable et prendre la propriété. La fermeture décidera laquelle de ces méthodes utiliser en fonction de ce que fait le corps de la fonction avec les valeurs capturées.

Dans l'Listing 13-4, nous définissons une fermeture qui capture une référence immuable au vecteur nommé `list` parce qu'elle a seulement besoin d'une référence immuable pour imprimer la valeur.

<Listing number="13-4" file-name="src/main.rs" caption="Définir et appeler une fermeture qui capture une référence immuable">

```rust
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-04/src/main.rs}}
```

</Listing>

Cet exemple illustre également qu'une variable peut se lier à une définition de fermeture, et nous pouvons appeler plus tard la fermeture en utilisant le nom de la variable et des parenthèses comme si le nom de la variable était un nom de fonction.

Puisque nous pouvons avoir plusieurs références immuables à `list` en même temps, `list` est toujours accessible à partir du code avant la définition de la fermeture, après la définition de la fermeture mais avant l'appel de la fermeture, et après l'appel de la fermeture. Ce code compile, s'exécute et imprime :

```console
{{#include ../listings/ch13-functional-features/listing-13-04/output.txt}}
```

Ensuite, dans l'Listing 13-5, nous changeons le corps de la fermeture de sorte qu'il ajoute un élément au vecteur `list`. La fermeture capture maintenant une référence mutable.

<Listing number="13-5" file-name="src/main.rs" caption="Définir et appeler une fermeture qui capture une référence mutable">

```rust
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-05/src/main.rs}}
```

</Listing>

Ce code compile, s'exécute et imprime :

```console
{{#include ../listings/ch13-functional-features/listing-13-05/output.txt}}
```

Notez qu'il n'y a plus de `println!` entre la définition et l'appel de la fermeture `borrows_mutably` : Lorsque `borrows_mutably` est défini, il capture une référence mutable à `list`. Nous n'utilisons plus la fermeture après l'appel de la fermeture, donc l'emprunt mutable se termine. Entre la définition de la fermeture et l'appel de la fermeture, un emprunt immuable pour imprimer n'est pas autorisé, car aucun autre emprunt n'est autorisé lorsqu'il y a un emprunt mutable. Essayez d'ajouter un `println!` à cet endroit pour voir quel message d'erreur vous recevez !

Si vous voulez forcer la fermeture à prendre possession des valeurs qu'elle utilise dans l'environnement, même si le corps de la fermeture n'a pas strictement besoin de la propriété, vous pouvez utiliser le mot-clé `move` avant la liste des paramètres.

Cette technique est principalement utile lors du passage d'une fermeture à un nouveau thread pour déplacer les données afin qu'elles soient possédées par le nouveau thread. Nous aborderons les threads et pourquoi vous voudriez les utiliser en détail dans le Chapitre 16 lorsque nous parlerons de la concurrence, mais pour l'instant, explorons brièvement la création d'un nouveau thread utilisant une fermeture qui nécessite le mot-clé `move`. L'Listing 13-6 montre l'Listing 13-4 modifié pour imprimer le vecteur dans un nouveau thread plutôt que dans le thread principal.

<Listing number="13-6" file-name="src/main.rs" caption="Utilisation de `move` pour forcer la fermeture du thread à prendre possession de `list`">

```rust
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-06/src/main.rs}}
```

</Listing>

Nous lançons un nouveau thread, donnant au thread une fermeture à exécuter en tant qu'argument. Le corps de la fermeture imprime la liste. Dans l'Listing 13-4, la fermeture ne capturait que `list` en utilisant une référence immuable, car c'est le minimum d'accès à `list` nécessaire pour l'imprimer. Dans cet exemple, même si le corps de la fermeture n'a toujours besoin que d'une référence immuable, nous devons spécifier que `list` doit être déplacé dans la fermeture en mettant le mot clé `move` au début de la définition de la fermeture. Si le thread principal effectuait plus d'opérations avant d'appeler `join` sur le nouveau thread, le nouveau thread pourrait se terminer avant que le reste du thread principal ne se termine, ou le thread principal pourrait finir en premier. Si le thread principal conservait la propriété de `list` mais se terminait avant le nouveau thread et abandonnait `list`, la référence immuable dans le thread deviendrait invalide. Par conséquent, le compilateur exige que `list` soit déplacé dans la fermeture remise au nouveau thread afin que la référence reste valide. Essayez de retirer le mot-clé `move` ou d'utiliser `list` dans le thread principal après la définition de la fermeture pour voir quelles erreurs de compilation vous recevez !

<!-- Anciennes titres. Ne pas supprimer sinon les liens peuvent être cassés. -->

<a id="storing-closures-using-generic-parameters-and-the-fn-traits"></a>
<a id="limitations-of-the-cacher-implementation"></a>
<a id="moving-captured-values-out-of-the-closure-and-the-fn-traits"></a>
<a id="moving-captured-values-out-of-closures-and-the-fn-traits"></a>

### Déplacer des valeurs capturées hors des fermetures

Une fois qu'une fermeture a capturé une référence ou a capturé la propriété d'une valeur de l'environnement où la fermeture est définie (affectant ainsi ce qui, le cas échéant, est déplacé _dans_ la fermeture), le code du corps de la fermeture définit ce qui arrive aux références ou aux valeurs lorsque la fermeture est évaluée ultérieurement (affectant ainsi ce qui, le cas échéant, est déplacé _hors_ de la fermeture).

Le corps d'une fermeture peut faire l'une des actions suivantes : déplacer une valeur capturée hors de la fermeture, muter la valeur capturée, ni déplacer ni muter la valeur, ou ne rien capturer du tout de l'environnement.

La manière dont une fermeture capture et gère les valeurs de l'environnement affecte quels traits la fermeture implémente, et les traits sont la façon dont les fonctions et les structures peuvent spécifier quels types de fermetures elles peuvent utiliser. Les fermetures implémenteront automatiquement un, deux ou tous les trois de ces traits `Fn`, de manière additive, en fonction de la manière dont le corps de la fermeture gère les valeurs :

* `FnOnce` s'applique aux fermetures qui peuvent être appelées une fois. Toutes les fermetures implémentent au moins ce trait car toutes les fermetures peuvent être appelées. Une fermeture qui déplace des valeurs capturées hors de son corps n'implémentera que `FnOnce` et aucun des autres traits `Fn` car elle ne peut être appelée qu'une fois.
* `FnMut` s'applique aux fermetures qui ne déplacent pas des valeurs capturées hors de leur corps mais peuvent muter les valeurs capturées. Ces fermetures peuvent être appelées plus d'une fois.
* `Fn` s'applique aux fermetures qui ne déplacent pas des valeurs capturées hors de leur corps et ne mutent pas les valeurs capturées, ainsi qu'aux fermetures qui ne capturent rien de leur environnement. Ces fermetures peuvent être appelées plusieurs fois sans muter leur environnement, ce qui est important dans des cas où une fermeture doit être appelée plusieurs fois simultanément.

Regardons la définition de la méthode `unwrap_or_else` sur `Option<T>` que nous avons utilisée dans l'Listing 13-1 :

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

Rappelez-vous que `T` est le type générique représentant le type de la valeur dans la variante `Some` d'un `Option`. Ce type `T` est également le type de retour de la fonction `unwrap_or_else` : Le code qui appelle `unwrap_or_else` sur un `Option<String>`, par exemple, obtiendra une `String`.

Ensuite, remarquez que la fonction `unwrap_or_else` a le paramètre de type générique supplémentaire `F`. Le type `F` est le type du paramètre nommé `f`, qui est la fermeture que nous fournissons lors de l'appel de `unwrap_or_else`.

La contrainte de trait spécifiée sur le type générique `F` est `FnOnce() -> T`, ce qui signifie que `F` doit pouvoir être appelé une fois, ne prendre aucun argument et retourner un `T`. L'utilisation de `FnOnce` dans la contrainte de trait exprime la condition selon laquelle `unwrap_or_else` n'appellera `f` qu'une seule fois. Dans le corps de `unwrap_or_else`, nous pouvons voir que si l' `Option` est `Some`, `f` ne sera pas appelée. Si l' `Option` est `None`, `f` sera appelée une fois. Étant donné que toutes les fermetures implémentent `FnOnce`, `unwrap_or_else` accepte les trois types de fermetures et est aussi flexible que possible.

> Remarque : Si ce que nous voulons faire ne nécessite pas de capturer une valeur de l'environnement, nous pouvons utiliser le nom d'une fonction plutôt qu'une fermeture là où nous avons besoin de quelque chose qui implémente l'un des traits `Fn`. Par exemple, sur une valeur `Option<Vec<T>>`, nous pourrions appeler `unwrap_or_else(Vec::new)` pour obtenir un nouveau vecteur vide si la valeur est `None`. Le compilateur implémente automatiquement le(s) trait(s) `Fn` applicables pour une définition de fonction.

Maintenant, examinons la méthode de la bibliothèque standard `sort_by_key`, définie sur les tranches, pour voir comment cela diffère de `unwrap_or_else` et pourquoi `sort_by_key` utilise `FnMut` au lieu de `FnOnce` pour la contrainte de trait. La fermeture reçoit un argument sous la forme d'une référence à l'élément actuel dans la tranche considérée, et elle renvoie une valeur de type `K` qui peut être ordonnée. Cette fonction est utile lorsque vous souhaitez trier une tranche par un attribut particulier de chaque élément. Dans l'Listing 13-7, nous avons une liste d'instances `Rectangle`, et nous utilisons `sort_by_key` pour les ordonner par leur attribut `width` du plus bas au plus haut.

<Listing number="13-7" file-name="src/main.rs" caption="Utilisation de `sort_by_key` pour ordonner des rectangles par largeur">

```rust
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-07/src/main.rs}}
```

</Listing>

Ce code imprime :

```console
{{#include ../listings/ch13-functional-features/listing-13-07/output.txt}}
```

La raison pour laquelle `sort_by_key` est défini pour prendre une fermeture `FnMut` est qu'il appelle la fermeture plusieurs fois : une fois pour chaque élément dans la tranche. La fermeture `|r| r.width` ne capture, ne muta ni ne déplace rien de son environnement, donc elle satisfait les exigences de contrainte de trait.

En revanche, l'Listing 13-8 montre un exemple d'une fermeture qui n'implémente que le trait `FnOnce`, parce qu'elle déplace une valeur de l'environnement. Le compilateur ne nous laissera pas utiliser cette fermeture avec `sort_by_key`.

<Listing number="13-8" file-name="src/main.rs" caption="Tentative d'utiliser une fermeture `FnOnce` avec `sort_by_key`">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-08/src/main.rs}}
```

</Listing>

C'est un moyen compliqué et trompeur (qui ne fonctionne pas) d'essayer de compter le nombre de fois que `sort_by_key` appelle la fermeture lors du tri de `list`. Ce code tente de compter cela en ajoutant `value`—une `String` provenant de l'environnement de la fermeture—dans le vecteur `sort_operations`. La fermeture capture `value` puis déplace `value` hors de la fermeture en cédant la propriété de `value` au vecteur `sort_operations`. Cette fermeture ne peut être appelée qu'une fois ; essayer de l'appeler une seconde fois ne fonctionnerait pas, car `value` ne serait plus dans l'environnement pour être poussé dans `sort_operations` à nouveau ! Par conséquent, cette fermeture n'implémente que `FnOnce`. Lorsque nous essayons de compiler ce code, nous obtenons cette erreur indiquant que `value` ne peut pas être déplacée hors de la fermeture car la fermeture doit implémenter `FnMut` :

```console
{{#include ../listings/ch13-functional-features/listing-13-08/output.txt}}
```

L'erreur pointe vers la ligne dans le corps de la fermeture qui déplace `value` hors de l'environnement. Pour résoudre cela, nous devons changer le corps de la fermeture pour qu'il ne déplace pas de valeurs hors de l'environnement. Garder un compteur dans l'environnement et incrémenter sa valeur dans le corps de la fermeture est un moyen plus simple de compter le nombre de fois que la fermeture est appelée. La fermeture dans l'Listing 13-9 fonctionne avec `sort_by_key` car elle ne capture qu'une référence mutable au compteur `num_sort_operations` et peut donc être appelée plus d'une fois.

<Listing number="13-9" file-name="src/main.rs" caption="Utiliser une fermeture `FnMut` avec `sort_by_key` est autorisé.">

```rust
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-09/src/main.rs}}
```

</Listing>

Les traits `Fn` sont importants lors de la définition ou de l'utilisation de fonctions ou de types qui utilisent des fermetures. Dans la section suivante, nous discuterons des itérateurs. De nombreuses méthodes d'itérateur prennent des arguments de fermeture, alors gardez ces détails sur les fermetures à l'esprit lorsque nous continuons !

[unwrap-or-else]: ../std/option/enum.Option.html#method.unwrap_or_else