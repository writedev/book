## Méthodes

Les méthodes ressemblent aux fonctions : nous les déclarons avec le mot-clé `fn` et un nom, elles peuvent avoir des paramètres et une valeur de retour, et elles contiennent du code exécuté lorsque la méthode est appelée depuis un autre endroit. Contrairement aux fonctions, les méthodes sont définies dans le contexte d’une structure (ou d’une énumération ou d’un objet trait, que nous aborderons respectivement au [chapitre 6][enums]<!-- ignore --> et au [chapitre 18][trait-objects]<!-- ignore -->), et leur premier paramètre est toujours `self`, qui représente l’instance de la structure sur laquelle la méthode est appelée.

<!-- Old headings. Do not remove or links may break. -->

<a id="defining-methods"></a>

### Syntaxe des méthodes

Modifions la fonction `area`, qui prend une instance de `Rectangle` comme paramètre, pour en faire une méthode `area` définie sur la structure `Rectangle`, comme indiqué dans la liste 5-13.

<Listing number="5-13" file-name="src/main.rs" caption="Définition d’une méthode `area` sur la structure `Rectangle`">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-13/src/main.rs}}
```

</Listing>

Pour définir la fonction dans le contexte de `Rectangle`, nous commençons par un bloc `impl` (implémentation) pour `Rectangle`. Tout ce qui se trouve dans ce bloc `impl` sera associé au type `Rectangle`. Ensuite, nous déplaçons la fonction `area` dans les accolades du bloc `impl` et remplaçons le premier paramètre (qui est aussi le seul dans ce cas) par `self` dans la signature et partout dans le corps de la fonction. Dans `main`, où nous appelions la fonction `area` en lui passant `rect1` comme argument, nous pouvons à la place utiliser la _syntaxe des méthodes_ pour appeler la méthode `area` sur notre instance de `Rectangle`. La syntaxe des méthodes vient après une instance : nous ajoutons un point, suivi du nom de la méthode, de parenthèses et de tous les arguments.

Dans la signature de `area`, nous utilisons `&self` au lieu de `rectangle: &Rectangle`. `&self` est en fait une forme abrégée de `self: &Self`. Dans un bloc `impl`, le type `Self` est un alias du type pour lequel le bloc `impl` est défini. Les méthodes doivent avoir un paramètre nommé `self` de type `Self` comme premier paramètre, c’est pourquoi Rust permet de n’écrire que le nom `self` à la place du premier paramètre. Notez que nous devons toujours mettre `&` devant la forme abrégée `self` pour indiquer que cette méthode emprunte l’instance `Self`, comme nous le faisions avec `rectangle: &Rectangle`. Les méthodes peuvent prendre possession de `self`, emprunter `self` de manière immuable, comme nous l’avons fait ici, ou emprunter `self` de manière mutable, tout comme elles peuvent le faire avec n’importe quel autre paramètre.

Nous avons choisi `&self` ici pour la même raison que nous avions utilisé `&Rectangle` dans la version avec fonction : nous ne voulons pas prendre possession de l’instance, mais simplement lire les données de la structure, sans les modifier. Si nous voulions modifier l’instance sur laquelle nous avons appelé la méthode dans le cadre de son exécution, nous utiliserions `&mut self` comme premier paramètre. Il est rare qu’une méthode prenne possession de l’instance en utilisant simplement `self` comme premier paramètre ; cette technique est généralement utilisée lorsque la méthode transforme `self` en autre chose et que vous voulez empêcher l’appelant d’utiliser l’instance d’origine après la transformation.

La principale raison d’utiliser des méthodes plutôt que des fonctions, outre le fait qu’elles fournissent une syntaxe dédiée et évitent de répéter le type de `self` dans la signature de chaque méthode, est l’organisation. Nous avons regroupé dans un bloc `impl` tout ce que nous pouvons faire avec une instance d’un type, au lieu d’obliger les futurs utilisateurs de notre code à chercher les fonctionnalités de `Rectangle` à différents endroits de la bibliothèque que nous fournissons.

Notez que nous pouvons choisir de donner à une méthode le même nom que l’un des champs de la structure. Par exemple, nous pouvons définir une méthode `width` sur `Rectangle` :

<Listing file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/no-listing-06-method-field-interaction/src/main.rs:here}}
```

</Listing>

Ici, nous choisissons de faire en sorte que la méthode `width` renvoie `true` si la valeur du champ `width` de l’instance est supérieure à `0` et `false` si cette valeur est égale à `0` : nous pouvons utiliser un champ dans une méthode du même nom à toutes sortes de fins. Dans `main`, lorsque nous faisons suivre `rect1.width` de parenthèses, Rust comprend que nous voulons parler de la méthode `width`. Sans parenthèses, Rust comprend que nous voulons parler du champ `width`.

Souvent, mais pas toujours, lorsqu’on donne à une méthode le même nom qu’à un champ, on souhaite qu’elle renvoie uniquement la valeur du champ et ne fasse rien d’autre. Ces méthodes sont appelées des _accesseurs_ (getters), et Rust ne les implémente pas automatiquement pour les champs des structures, contrairement à certains autres langages. Les accesseurs sont utiles, car vous pouvez rendre le champ privé et la méthode publique, permettant ainsi un accès en lecture seule à ce champ dans le cadre de l’API publique du type. Nous verrons ce que signifient les termes public et privé et comment rendre un champ ou une méthode public ou privé au [chapitre 7][public]<!-- ignore -->.

> ### Où est l’opérateur `->` ?
>
> En C et en C++, deux opérateurs différents sont utilisés pour appeler des méthodes : vous utilisez `.` si vous appelez une méthode directement sur l’objet et `->` si vous appelez la méthode sur un pointeur vers l’objet et devez d’abord déréférencer le pointeur. Autrement dit, si `object` est un pointeur, `object->something()` est similaire à `(*object).something()`.
>
> Rust n’a pas d’équivalent à l’opérateur `->` ; à la place, Rust dispose d’une fonctionnalité appelée _référencement et déréférencement automatiques_. L’appel de méthodes est l’un des rares cas où ce comportement s’applique dans Rust.
>
> Voici comment cela fonctionne : lorsque vous appelez une méthode avec `object.something()`, Rust ajoute automatiquement `&`, `&mut` ou `*` afin que `object` corresponde à la signature de la méthode. Autrement dit, les expressions suivantes sont équivalentes :
>
> <!-- CAN'T EXTRACT SEE BUG https://github.com/rust-lang/mdBook/issues/1127 -->
>
> ```rust
> # #[derive(Debug,Copy,Clone)]
> # struct Point {
> #     x: f64,
> #     y: f64,
> # }
> #
> # impl Point {
> #    fn distance(&self, other: &Point) -> f64 {
> #        let x_squared = f64::powi(other.x - self.x, 2);
> #        let y_squared = f64::powi(other.y - self.y, 2);
> #
> #        f64::sqrt(x_squared + y_squared)
> #    }
> # }
> # let p1 = Point { x: 0.0, y: 0.0 };
> # let p2 = Point { x: 5.0, y: 6.5 };
> p1.distance(&p2);
> (&p1).distance(&p2);
> ```
>
> La première forme est beaucoup plus claire. Ce référencement automatique fonctionne parce que les méthodes ont un récepteur bien défini : le type de `self`. Étant donné le récepteur et le nom d’une méthode, Rust peut déterminer sans ambiguïté si la méthode lit (`&self`), modifie (`&mut self`) ou consomme (`self`) l’instance. Le fait que Rust rende implicite l’emprunt des récepteurs de méthodes contribue grandement à rendre la gestion de la propriété pratique.

### Méthodes avec plusieurs paramètres

Entraînons-nous à utiliser des méthodes en implémentant une deuxième méthode sur la structure `Rectangle`. Cette fois, nous voulons qu’une instance de `Rectangle` prenne une autre instance de `Rectangle` et renvoie `true` si la deuxième `Rectangle` tient entièrement dans `self` (la première `Rectangle`) ; sinon, elle doit renvoyer `false`. Autrement dit, une fois la méthode `can_hold` définie, nous voulons pouvoir écrire le programme présenté dans la liste 5-14.

<Listing number="5-14" file-name="src/main.rs" caption="Utilisation de la méthode `can_hold`, qui reste à écrire">

```rust,ignore
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-14/src/main.rs}}
```

</Listing>

Le résultat attendu ressemblerait à ceci, car les deux dimensions de `rect2` sont inférieures à celles de `rect1`, tandis que `rect3` est plus large que `rect1` :

```text
Can rect1 hold rect2? true
Can rect1 hold rect3? false
```

Nous savons que nous voulons définir une méthode ; elle se trouvera donc dans le bloc `impl Rectangle`. La méthode s’appellera `can_hold` et prendra en paramètre un emprunt immuable d’une autre `Rectangle`. Nous pouvons déterminer le type du paramètre en examinant le code qui appelle la méthode : `rect1.can_hold(&rect2)` transmet `&rect2`, un emprunt immuable de `rect2`, une instance de `Rectangle`. Cela a du sens, car nous avons seulement besoin de lire `rect2` (et non de le modifier, ce qui nécessiterait un emprunt mutable), et nous voulons que `main` conserve la possession de `rect2` afin de pouvoir le réutiliser après l’appel de la méthode `can_hold`. La valeur de retour de `can_hold` sera un booléen, et l’implémentation vérifiera si la largeur et la hauteur de `self` sont respectivement supérieures à celles de l’autre `Rectangle`. Ajoutons la nouvelle méthode `can_hold` au bloc `impl` de la liste 5-13, comme indiqué dans la liste 5-15.

<Listing number="5-15" file-name="src/main.rs" caption="Implémentation de la méthode `can_hold` sur `Rectangle`, qui prend une autre instance de `Rectangle` comme paramètre">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-15/src/main.rs:here}}
```

</Listing>

Lorsque nous exécuterons ce code avec la fonction `main` de la liste 5-14, nous obtiendrons le résultat souhaité. Les méthodes peuvent prendre plusieurs paramètres, que nous ajoutons à la signature après le paramètre `self` ; ces paramètres fonctionnent comme ceux des fonctions.

### Fonctions associées

Toutes les fonctions définies dans un bloc `impl` sont appelées _fonctions associées_, car elles sont associées au type nommé après `impl`. Nous pouvons définir des fonctions associées qui n’ont pas `self` comme premier paramètre (et qui ne sont donc pas des méthodes), car elles n’ont pas besoin d’une instance du type pour fonctionner. Nous avons déjà utilisé une fonction de ce type : la fonction `String::from`, définie sur le type `String`.

Les fonctions associées qui ne sont pas des méthodes servent souvent de constructeurs renvoyant une nouvelle instance de la structure. Elles sont souvent nommées `new`, mais `new` n’est pas un nom spécial et n’est pas intégré au langage. Par exemple, nous pourrions choisir de fournir une fonction associée nommée `square`, qui prendrait un paramètre de dimension et l’utiliserait à la fois comme largeur et comme hauteur, ce qui faciliterait la création d’un carré `Rectangle` au lieu d’avoir à spécifier deux fois la même valeur :

<span class="filename">Nom du fichier : src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/no-listing-03-associated-functions/src/main.rs:here}}
```

Les mots-clés `Self` dans le type de retour et dans le corps de la fonction sont des alias du type qui apparaît après le mot-clé `impl`, qui est dans ce cas `Rectangle`.

Pour appeler cette fonction associée, nous utilisons la syntaxe `::` avec le nom de la structure ; `let sq = Rectangle::square(3);` en est un exemple. Cette fonction est placée dans l’espace de noms de la structure : la syntaxe `::` est utilisée à la fois pour les fonctions associées et pour les espaces de noms créés par les modules. Nous aborderons les modules au [chapitre 7][modules]<!-- ignore -->.

### Plusieurs blocs `impl`

Chaque structure peut avoir plusieurs blocs `impl`. Par exemple, la liste 5-15 est équivalente au code présenté dans la liste 5-16, où chaque méthode se trouve dans son propre bloc `impl`.

<Listing number="5-16" caption="Réécriture de la liste 5-15 à l’aide de plusieurs blocs `impl`">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-16/src/main.rs:here}}
```

</Listing>

Il n’y a aucune raison de séparer ces méthodes en plusieurs blocs `impl` ici, mais cette syntaxe est valide. Nous verrons un cas où plusieurs blocs `impl` sont utiles au chapitre 10, lorsque nous aborderons les types génériques et les traits.

## Résumé

Les structures vous permettent de créer des types personnalisés adaptés à votre domaine. Elles vous permettent de garder ensemble des éléments de données liés et de nommer chaque élément afin de clarifier votre code. Dans les blocs `impl`, vous pouvez définir des fonctions associées à votre type ; les méthodes sont une forme de fonction associée qui vous permet de définir le comportement des instances de vos structures.

Mais les structures ne sont pas le seul moyen de créer des types personnalisés : intéressons-nous à la fonctionnalité des énumérations de Rust pour ajouter un nouvel outil à votre boîte à outils.

[enums]: ch06-00-enums.html
[trait-objects]: ch18-02-trait-objects.md
[public]: ch07-03-paths-for-referring-to-an-item-in-the-module-tree.html#exposing-paths-with-the-pub-keyword
[modules]: ch07-02-defining-modules-to-control-scope-and-privacy.html