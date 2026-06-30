## Les cycles de référence peuvent provoquer des fuites de mémoire

Les garanties de sécurité mémoire de Rust rendent difficile, mais pas impossible, la création accidentelle de mémoire qui n'est jamais libérée (connue sous le nom de _fuite de mémoire_). Empêcher complètement les fuites de mémoire n'est pas l'une des garanties de Rust, ce qui signifie que les fuites de mémoire sont sûres en Rust. Nous pouvons observer que Rust permet les fuites de mémoire en utilisant `Rc<T>` et `RefCell<T>` : il est possible de créer des références où les éléments se réfèrent mutuellement dans un cycle. Cela crée des fuites de mémoire car le compteur de références de chaque élément dans le cycle n'atteindra jamais 0, et les valeurs ne seront jamais libérées.

### Création d'un cycle de référence

Examinons comment un cycle de référence pourrait se produire et comment l'éviter, en commençant par la définition de l'énumération `List` et une méthode `tail` dans la liste 15-25.

<Listing number="15-25" file-name="src/main.rs" caption="Une définition de liste cons qui contient un `RefCell<T>` afin que nous puissions modifier ce à quoi un variant `Cons` se réfère.">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-25/src/main.rs:here}}
```

</Listing>

Nous utilisons une autre variation de la définition de `List` de la liste 15-5. Le deuxième élément dans le variant `Cons` est maintenant `RefCell<Rc<List>>`, ce qui signifie qu'au lieu de pouvoir modifier la valeur `i32` comme nous l'avons fait dans la liste 15-24, nous souhaitons modifier la valeur `List` à laquelle un variant `Cons` pointe. Nous ajoutons également une méthode `tail` pour faciliter l'accès au deuxième élément si nous avons un variant `Cons`.

Dans la liste 15-26, nous ajoutons une fonction `main` qui utilise les définitions de la liste 15-25. Ce code crée une liste dans `a` et une liste dans `b` qui pointe vers la liste dans `a`. Ensuite, il modifie la liste dans `a` pour pointer vers `b`, créant ainsi un cycle de référence. Il y a des déclarations `println!` tout au long de ce processus pour montrer quels sont les compteurs de références à divers moments.

<Listing number="15-26" file-name="src/main.rs" caption="Création d'un cycle de référence de deux valeurs `List` pointant l'une vers l'autre.">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-26/src/main.rs:here}}
```

</Listing>

Nous créons une instance `Rc<List>` contenant une valeur `List` dans la variable `a` avec une liste initiale de `5, Nil`. Nous créons ensuite une instance `Rc<List>` contenant une autre valeur `List` dans la variable `b` qui contient la valeur `10` et pointe vers la liste dans `a`.

Nous modifions `a` pour qu'elle pointe vers `b` au lieu de `Nil`, créant ainsi un cycle. Nous faisons cela en utilisant la méthode `tail` pour obtenir une référence au `RefCell<Rc<List>>` dans `a`, que nous mettons dans la variable `link`. Ensuite, nous utilisons la méthode `borrow_mut` sur le `RefCell<Rc<List>>` pour changer la valeur interne d'un `Rc<List>` contenant une valeur `Nil` à l'`Rc<List>` dans `b`.

Lorsque nous exécutons ce code, en laissant le dernier `println!` commenté pour le moment, nous obtiendrons cette sortie :

```console
{{#include ../listings/ch15-smart-pointers/listing-15-26/output.txt}}
```

Le compteur de référence des instances `Rc<List>` dans `a` et `b` est de 2 après que nous avons changé la liste dans `a` pour pointer vers `b`. À la fin de `main`, Rust libère la variable `b`, ce qui diminue le compteur de référence de l'instance `Rc<List>` dans `b` de 2 à 1. La mémoire que `Rc<List>` a dans le tas ne sera pas libérée à ce stade car son compteur de référence est de 1, pas 0. Ensuite, Rust libère `a`, ce qui diminue également le compteur de référence de l'instance `Rc<List>` dans `a` de 2 à 1. La mémoire de cette instance ne peut pas être libérée non plus, car l'autre instance `Rc<List>` y fait toujours référence. La mémoire allouée à la liste restera non collectée pour toujours. Pour visualiser ce cycle de référence, nous avons créé le diagramme dans la figure 15-4.

<img alt="Un rectangle étiqueté 'a' qui pointe vers un rectangle contenant l'entier 5. Un rectangle étiqueté 'b' qui pointe vers un rectangle contenant l'entier 10. Le rectangle contenant 5 pointe vers le rectangle contenant 10, et le rectangle contenant 10 pointe également vers le rectangle contenant 5, créant un cycle." src="img/trpl15-04.svg" class="center" />

<span class="caption">Figure 15-4 : Un cycle de référence des listes `a` et `b` se pointant mutuellement</span>

Si vous décommentez le dernier `println!` et exécutez le programme, Rust essaiera d'imprimer ce cycle avec `a` pointant vers `b` pointant vers `a`, et ainsi de suite, jusqu'à un dépassement de pile.

Comparé à un programme du monde réel, les conséquences de la création d'un cycle de référence dans cet exemple ne sont pas très graves : juste après avoir créé le cycle de référence, le programme se termine. Cependant, si un programme plus complexe alloue beaucoup de mémoire dans un cycle et y reste pendant longtemps, le programme utiliserait plus de mémoire que nécessaire et pourrait submerger le système, provoquant une pénurie de mémoire disponible.

Créer des cycles de référence n'est pas facile, mais ce n'est pas impossible non plus. Si vous avez des valeurs `RefCell<T>` qui contiennent des valeurs `Rc<T>` ou des combinaisons imbriquées similaires de types avec mutabilité intérieure et comptage de références, vous devez vous assurer que vous ne créez pas de cycles ; vous ne pouvez pas compter sur Rust pour les attraper. Créer un cycle de référence serait un bug logique dans votre programme que vous devriez minimiser à l'aide de tests automatisés, de revues de code et d'autres pratiques de développement logiciel.

Une autre solution pour éviter les cycles de référence consiste à réorganiser vos structures de données de manière à ce que certaines références expriment la propriété et d'autres ne le fassent pas. En conséquence, vous pouvez avoir des cycles composés de certaines relations de propriété et de certaines relations non-propriétaires, et seules les relations de propriété affectent que qu'une valeur puisse être libérée ou non. Dans la liste 15-25, nous voulons toujours que les variantes `Cons` possèdent leur liste, donc la réorganisation de la structure de données n'est pas possible. Voyons un exemple utilisant des graphes composés de nœuds parents et enfants pour voir quand les relations non-propriétaires constituent un moyen approprié d'éviter les cycles de référence.

### Prévention des cycles de référence en utilisant `Weak<T>`

Jusqu'à présent, nous avons démontré que l'appel à `Rc::clone` augmente le `strong_count` d'une instance `Rc<T>`, et une instance `Rc<T>` n'est nettoyée que si son `strong_count` est 0. Vous pouvez également créer une référence faible au valeur d'une instance `Rc<T>` en appelant `Rc::downgrade` et en transmettant une référence à l'`Rc<T>`. Les *références fortes* sont comment vous pouvez partager la propriété d'une instance `Rc<T>`. Les *références faibles* n'expriment pas une relation de propriété, et leur nombre n'affecte pas quand une instance `Rc<T>` est nettoyée. Elles ne provoqueront pas de cycle de référence, car tout cycle impliquant des références faibles sera rompu une fois que le compteur de références fortes des valeurs impliquées est 0.

Lorsque vous appelez `Rc::downgrade`, vous obtenez un pointeur intelligent de type `Weak<T>`. Au lieu d'augmenter le `strong_count` dans l'instance `Rc<T>` de 1, l'appel à `Rc::downgrade` augmente le `weak_count` de 1. Le type `Rc<T>` utilise `weak_count` pour garder une trace du nombre de références `Weak<T>` existantes, de manière similaire à `strong_count`. La différence est que le `weak_count` n'a pas besoin d'être 0 pour que l'instance `Rc<T>` soit nettoyée.

Puisque la valeur que référence `Weak<T>` pourrait avoir été supprimée, pour faire quoi que ce soit avec la valeur à laquelle un `Weak<T>` pointe, vous devez vous assurer que la valeur existe toujours. Faites-le en appelant la méthode `upgrade` sur une instance `Weak<T>`, qui retournera un `Option<Rc<T>>`. Vous obtiendrez un résultat de `Some` si la valeur `Rc<T>` n'a pas encore été supprimée et un résultat de `None` si la valeur `Rc<T>` a été supprimée. Comme `upgrade` retourne un `Option<Rc<T>>`, Rust veillera à ce que le cas de `Some` et le cas de `None` soient gérés, et il n'y aura pas de pointeur invalide.

Par exemple, au lieu d'utiliser une liste dont les éléments ne connaissent que l'élément suivant, nous allons créer un arbre dont les éléments connaissent leurs éléments enfants _et_ leurs éléments parents.

#### Création d'une structure de données en arbre

Pour commencer, nous allons construire un arbre avec des nœuds qui connaissent leurs nœuds enfants. Nous allons créer une structure nommée `Node` qui contient sa propre valeur `i32` ainsi que des références à ses valeurs de nœud enfant :

<span class="filename">Nom de fichier : src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-27/src/main.rs:here}}
```

Nous voulons qu'un `Node` possède ses enfants, et nous voulons partager cette propriété avec des variables pour que nous puissions accéder à chaque `Node` dans l'arbre directement. Pour cela, nous définissons les éléments de `Vec<T>` comme des valeurs de type `Rc<Node>`. Nous voulons également modifier quels nœuds sont enfants d'un autre nœud, donc nous avons un `RefCell<T>` dans `children` autour du `Vec<Rc<Node>>`.

Ensuite, nous utiliserons notre définition de structure et créerons une instance de `Node` nommée `leaf` avec la valeur `3` et sans enfants, et une autre instance nommée `branch` avec la valeur `5` et `leaf` comme l'un de ses enfants, comme montré dans la liste 15-27.

<Listing number="15-27" file-name="src/main.rs" caption="Création d'un nœud `leaf` sans enfants et d'un nœud `branch` avec `leaf` comme l'un de ses enfants.">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-27/src/main.rs:there}}
```

</Listing>

Nous clonons l'`Rc<Node>` dans `leaf` et stockons cela dans `branch`, ce qui signifie que le `Node` dans `leaf` a maintenant deux propriétaires : `leaf` et `branch`. Nous pouvons passer de `branch` à `leaf` via `branch.children`, mais il n'y a aucun moyen de passer de `leaf` à `branch`. La raison en est que `leaf` n'a aucune référence à `branch` et ne sait pas qu'ils sont liés. Nous voulons que `leaf` sache que `branch` est son parent. Nous allons faire cela ensuite.

#### Ajout d'une référence d'un enfant à son parent

Pour rendre le nœud enfant conscient de son parent, nous devons ajouter un champ `parent` à notre définition de structure `Node`. Le problème est de décider quel devrait être le type de `parent`. Nous savons qu'il ne peut pas contenir un `Rc<T>`, car cela créerait un cycle de référence avec `leaf.parent` pointant vers `branch` et `branch.children` pointant vers `leaf`, ce qui empêcherait leurs valeurs `strong_count` d'atteindre 0.

En repensant aux relations d'une autre manière, un nœud parent devrait posséder ses enfants : si un nœud parent est supprimé, ses nœuds enfants devraient également l'être. Cependant, un enfant ne devrait pas posséder son parent : si nous supprimons un nœud enfant, le parent doit toujours exister. C'est un cas pour des références faibles !

Ainsi, au lieu de `Rc<T>`, nous ferons en sorte que le type de `parent` utilise `Weak<T>`, spécifiquement un `RefCell<Weak<Node>>`. Maintenant, notre définition de structure `Node` ressemble à ceci :

<span class="filename">Nom de fichier : src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-28/src/main.rs:here}}
```

Un nœud sera capable de se référer à son nœud parent mais ne possède pas ce parent. Dans la liste 15-28, nous mettons à jour `main` pour utiliser cette nouvelle définition afin que le nœud `leaf` ait un moyen de se référer à son parent, `branch`.

<Listing number="15-28" file-name="src/main.rs" caption="Un nœud `leaf` avec une référence faible à son nœud parent, `branch`.">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-28/src/main.rs:there}}
```

</Listing>

Créer le nœud `leaf` ressemble à ce qui a été fait dans la liste 15-27, à l'exception du champ `parent` : `leaf` commence sans parent, donc nous créons une nouvelle instance de référence `Weak<Node>` vide.

À ce stade, lorsque nous essayons d'obtenir une référence au parent de `leaf` en utilisant la méthode `upgrade`, nous obtenons une valeur `None`. Nous voyons cela dans la sortie de la première déclaration `println!` :

```text
leaf parent = None
```

Lorsque nous créons le nœud `branch`, il aura également un nouveau champ `Weak<Node>` référence dans `parent`, car `branch` n'a pas de nœud parent. Nous avons toujours `leaf` comme l'un des enfants de `branch`. Une fois que nous avons l'instance de `Node` dans `branch`, nous pouvons modifier `leaf` pour lui donner une référence `Weak<Node>` à son parent. Nous utilisons la méthode `borrow_mut` sur le `RefCell<Weak<Node>>` dans le champ `parent` de `leaf`, puis nous utilisons la fonction `Rc::downgrade` pour créer une référence `Weak<Node>` à `branch` à partir de l'`Rc<Node>` dans `branch`.

Lorsque nous imprimons à nouveau le parent de `leaf`, cette fois, nous obtiendrons une variante `Some` contenant `branch` : maintenant, `leaf` peut accéder à son parent ! Lorsque nous imprimons `leaf`, nous évitons également le cycle qui a finalement entraîné un dépassement de pile comme nous l'avions dans la liste 15-26 ; les références `Weak<Node>` sont imprimées sous la forme `(Weak)` :

```text
leaf parent = Some(Node { value: 5, parent: RefCell { value: (Weak) },
children: RefCell { value: [Node { value: 3, parent: RefCell { value: (Weak) },
children: RefCell { value: [] } }] } })
```

L'absence d'une sortie infinie indique que ce code n'a pas créé de cycle de référence. Nous pouvons également le constater en examinant les valeurs que nous obtenons en appelant `Rc::strong_count` et `Rc::weak_count`.

#### Visualisation des changements de `strong_count` et `weak_count`

Examinons comment les valeurs `strong_count` et `weak_count` des instances `Rc<Node>` changent en créant une nouvelle portée interne et en déplaçant la création de `branch` dans cette portée. Ainsi, nous pouvons voir ce qui se passe lors de la création de `branch` puis de sa suppression lorsqu'elle sort de la portée. Les modifications sont présentées dans la liste 15-29.

<Listing number="15-29" file-name="src/main.rs" caption="Création de `branch` dans une portée interne et examen des compteurs de références fortes et faibles. ">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-29/src/main.rs:here}}
```

</Listing>

Après la création de `leaf`, son `Rc<Node>` a un compteur fort de 1 et un compteur faible de 0. Dans la portée interne, nous créons `branch` et l'associons à `leaf`, à quel moment, lorsque nous imprimons les compteurs, l'`Rc<Node>` dans `branch` aura un compteur fort de 1 et un compteur faible de 1 (pour `leaf.parent` pointant vers `branch` avec un `Weak<Node>`). Lorsque nous imprimons les compteurs dans `leaf`, nous verrons qu'il aura un compteur fort de 2, car `branch` a maintenant un clone du `Rc<Node>` de `leaf` stocké dans `branch.children`, mais aura toujours un compteur faible de 0.

Lorsque la portée interne se termine, `branch` sort de la portée et le compteur fort de l'`Rc<Node>` diminue à 0, donc son `Node` est libéré. Le compteur faible de 1 de `leaf.parent` n'a pas d'incidence sur la libération de `Node`, donc nous n'avons pas de fuites de mémoire !

Si nous essayons d'accéder au parent de `leaf` après la fin de la portée, nous obtiendrons à nouveau `None`. À la fin du programme, l'`Rc<Node>` dans `leaf` a un compteur fort de 1 et un compteur faible de 0, car la variable `leaf` est à nouveau la seule référence à l'`Rc<Node>`.

Toute la logique qui gère les comptes et la libération des valeurs est intégrée dans `Rc<T>` et `Weak<T>` et leurs implémentations du trait `Drop`. En spécifiant que la relation d'un enfant à son parent doit être une référence `Weak<T>` dans la définition de `Node`, vous pouvez avoir des nœuds parents pointant vers des nœuds enfants et vice versa sans créer de cycle de référence et de fuites de mémoire.

## Résumé

Ce chapitre a couvert comment utiliser des pointeurs intelligents pour garantir des choses différentes et faire des compromis par rapport à ceux que Rust fait par défaut avec des références régulières. Le type `Box<T>` a une taille connue et pointe vers des données allouées sur le tas. Le type `Rc<T>` garde une trace du nombre de références à des données sur le tas afin que ces données puissent avoir plusieurs propriétaires. Le type `RefCell<T>` avec sa mutabilité intérieure nous donne un type que nous pouvons utiliser lorsque nous avons besoin d'un type immuable mais que nous devons modifier une valeur interne de ce type ; il impose également les règles d'emprunt à l'exécution plutôt qu'à la compilation.

Nous avons également discuté des traits `Deref` et `Drop`, qui permettent une grande partie de la fonctionnalité des pointeurs intelligents. Nous avons exploré les cycles de référence qui peuvent causer des fuites de mémoire et comment les éviter en utilisant `Weak<T>`.

Si ce chapitre vous a intéressé et que vous souhaitez implémenter vos propres pointeurs intelligents, consultez [« The Rustonomicon »][nomicon] pour plus d'informations utiles.

Nous aborderons ensuite la concurrence en Rust. Vous apprendrez même plusieurs nouveaux pointeurs intelligents.

[nomicon]: ../nomicon/index.html