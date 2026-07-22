## Méthodes

Les méthodes sont similaires aux fonctions : nous les déclarons avec le mot-clé `fn` et un nom, elles peuvent avoir des paramètres et une valeur de retour, et elles contiennent du code qui est exécuté lorsque la méthode est appelée d'ailleurs. Contrairement aux fonctions, les méthodes sont définies dans le contexte d'une structure (ou d'un énum ou d'un objet trait, que nous couvrirons dans [Chapitre 6][enums]<!-- ignore --> et [Chapitre 18][trait-objects]<!-- ignore -->, respectivement), et leur premier paramètre est toujours `self`, qui représente l'instance de la structure sur laquelle la méthode est appelée.

### Syntaxe de Méthode

Changeons la fonction `area` qui avait une instance de `Rectangle` comme paramètre et faisons-en une méthode `area` définie sur la structure `Rectangle`, comme montré dans l'Extrait 5-13.

<Extrait number="5-13" file-name="src/main.rs" caption="Définition d'une méthode `area` sur la structure `Rectangle`">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-13/src/main.rs}}
```

</Extrait>

Pour définir la fonction dans le contexte de `Rectangle`, nous commençons un bloc `impl` (implémentation) pour `Rectangle`. Tout ce qui se trouve dans ce bloc `impl` sera associé au type `Rectangle`. Ensuite, nous déplaçons la fonction `area` à l'intérieur des accolades `impl` et changeons le premier (et dans ce cas, le seul) paramètre pour qu'il soit `self` dans la signature et partout dans le corps. Dans `main`, où nous avons appelé la fonction `area` et passé `rect1` comme argument, nous pouvons à la place utiliser la _syntax de méthode_ pour appeler la méthode `area` sur notre instance de `Rectangle`. La syntaxe de méthode va après une instance : nous ajoutons un point suivi du nom de la méthode, des parenthèses et de tout argument.

Dans la signature pour `area`, nous utilisons `&self` au lieu de `rectangle: &Rectangle`. Le `&self` est en fait une abréviation pour `self: &Self`. Dans un bloc `impl`, le type `Self` est un alias pour le type que le bloc `impl` défend. Les méthodes doivent avoir un paramètre nommé `self` de type `Self` pour leur premier paramètre, donc Rust vous permet d'abréger cela avec seulement le nom `self` dans l'emplacement du premier paramètre. Notez que nous devons toujours utiliser le `&` devant l'abréviation `self` pour indiquer que cette méthode emprunte l'instance `Self`, tout comme nous l'avons fait dans `rectangle: &Rectangle`. Les méthodes peuvent prendre possession de `self`, emprunter `self` de manière immuable, comme nous l'avons fait ici, ou emprunter `self` de manière mutable, tout comme elles peuvent le faire pour tout autre paramètre.

Nous avons choisi `&self` ici pour la même raison pour laquelle nous avons utilisé `&Rectangle` dans la version fonction : nous ne voulons pas prendre possession, et nous voulons juste lire les données dans la structure, pas écrire à l'intérieur. Si nous voulions changer l'instance sur laquelle nous avons appelé la méthode dans le cadre de ce que fait la méthode, nous utiliserions `&mut self` comme premier paramètre. Avoir une méthode qui prend possession de l'instance en utilisant simplement `self` comme premier paramètre est rare ; cette technique est généralement utilisée lorsque la méthode transforme `self` en autre chose et que vous voulez empêcher l'appelant d'utiliser l'instance originale après la transformation.

La raison principale d'utiliser des méthodes au lieu de fonctions, en plus de fournir une syntaxe de méthode et de ne pas avoir à répéter le type de `self` dans la signature de chaque méthode, est l'organisation. Nous avons mis toutes les choses que nous pouvons faire avec une instance d'un type dans un bloc `impl` au lieu de faire chercher à l'utilisateur futur de notre code les capacités de `Rectangle` à divers endroits dans la bibliothèque que nous fournissons.

Notez que nous pouvons choisir de donner à une méthode le même nom qu'un des champs de la structure. Par exemple, nous pouvons définir une méthode sur `Rectangle` qui s'appelle aussi `width` :

<Extrait file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/no-listing-06-method-field-interaction/src/main.rs:here}}
```

</Extrait>

Ici, nous choisissons de faire en sorte que la méthode `width` retourne `true` si la valeur dans le champ `width` de l'instance est supérieure à `0` et `false` si la valeur est `0` : nous pouvons utiliser un champ dans une méthode du même nom à toute fin. Dans `main`, lorsque nous suivons `rect1.width` de parenthèses, Rust sait que nous parlons de la méthode `width`. Lorsque nous n'utilisons pas de parenthèses, Rust sait que nous parlons du champ `width`.

Souvent, mais pas toujours, lorsque nous donnons à une méthode le même nom qu'un champ, nous voulons qu'elle retourne simplement la valeur dans le champ et ne fasse rien d'autre. Les méthodes comme celle-ci sont appelées _getters_, et Rust ne les implémente pas automatiquement pour les champs de structure comme le font certaines autres langues. Les getters sont utiles car vous pouvez rendre le champ privé mais la méthode publique et ainsi activer un accès en lecture seule à ce champ dans le cadre de l'API publique du type. Nous aborderons ce que sont public et privé et comment désigner un champ ou une méthode comme public ou privé dans [Chapitre 7][public]<!-- ignore -->.

> ### Où est l'opérateur `->` ?
>
> En C et C++, deux opérateurs différents sont utilisés pour appeler des méthodes : vous utilisez `.` si vous appelez une méthode sur l'objet directement et `->` si vous appelez la méthode sur un pointeur vers l'objet et devez d'abord déréférencer le pointeur. En d'autres termes, si `object` est un pointeur, `object->something()` est similaire à `(*object).something()`.
>
> Rust n'a pas d'équivalent à l'opérateur `->` ; à la place, Rust a une fonctionnalité appelée _référencement et déréférencement automatiques_. Appeler des méthodes est l'un des rares endroits en Rust avec ce comportement.
>
> Voici comment cela fonctionne : lorsque vous appelez une méthode avec `object.something()`, Rust ajoute automatiquement `&`, `&mut`, ou `*` afin que `object` corresponde à la signature de la méthode. En d'autres termes, les éléments suivants sont équivalents :
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
> La première semble beaucoup plus claire. Ce comportement de référencement automatique fonctionne parce que les méthodes ont un récepteur clair : le type de `self`. Étant donné le récepteur et le nom d'une méthode, Rust peut déterminer définitivement si la méthode lis ( `&self`), modifie ( `&mut self`), ou consomme ( `self`). Le fait que Rust rend l'emprunt implicite pour les récepteurs de méthode est une partie importante de la réalisation pratique de la propriété.

### Méthodes avec Plus de Paramètres

Pratiquons l'utilisation des méthodes en implémentant une seconde méthode sur la structure `Rectangle`. Cette fois, nous voulons qu'une instance de `Rectangle` prenne une autre instance de `Rectangle` et retourne `true` si le second `Rectangle` peut tenir complètement dans `self` (le premier `Rectangle`) ; sinon, elle doit retourner `false`. C'est-à-dire qu'une fois que nous avons défini la méthode `can_hold`, nous voulons pouvoir écrire le programme montré dans l'Extrait 5-14.

<Extrait number="5-14" file-name="src/main.rs" caption="Utilisation de la méthode `can_hold` encore non écrite">

```rust,ignore
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-14/src/main.rs}}
```

</Extrait>

La sortie attendue ressemblerait à ce qui suit, car les deux dimensions de `rect2` sont plus petites que les dimensions de `rect1`, mais `rect3` est plus large que `rect1` :

```text
Est-ce que rect1 peut contenir rect2 ? vrai
Est-ce que rect1 peut contenir rect3 ? faux
```

Nous savons que nous voulons définir une méthode, donc elle sera dans le bloc `impl Rectangle`. Le nom de la méthode sera `can_hold`, et elle prendra un emprunt immuable d'un autre `Rectangle` comme paramètre. Nous pouvons déterminer le type du paramètre en regardant le code qui appelle la méthode : `rect1.can_hold(&rect2)` passe `&rect2`, qui est un emprunt immuable vers `rect2`, une instance de `Rectangle`. Cela a du sens parce que nous n'avons besoin que de lire `rect2` (plutôt que d'écrire, ce qui signifierait que nous aurions besoin d'un emprunt mutable), et nous voulons que `main` conserve la possession de `rect2` afin que nous puissions l'utiliser à nouveau après avoir appelé la méthode `can_hold`. La valeur de retour de `can_hold` sera un Boolean, et l'implémentation vérifiera si la largeur et la hauteur de `self` sont supérieures à la largeur et à la hauteur de l'autre `Rectangle`, respectivement. Ajoutons la nouvelle méthode `can_hold` au bloc `impl` de l'Extrait 5-13, montré dans l'Extrait 5-15.

<Extrait number="5-15" file-name="src/main.rs" caption="Implémentation de la méthode `can_hold` sur `Rectangle` qui prend une autre instance `Rectangle` comme paramètre">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-15/src/main.rs:here}}
```

</Extrait>

Lorsque nous exécutons ce code avec la fonction `main` de l'Extrait 5-14, nous obtiendrons notre sortie désirée. Les méthodes peuvent prendre plusieurs paramètres que nous ajoutons à la signature après le paramètre `self`, et ces paramètres fonctionnent de la même manière que les paramètres dans les fonctions.

### Fonctions Associées

Toutes les fonctions définies dans un bloc `impl` sont appelées _fonctions associées_ car elles sont associées au type nommé après le `impl`. Nous pouvons définir des fonctions associées qui n'ont pas `self` comme premier paramètre (et donc ne sont pas des méthodes) car elles n'ont pas besoin d'une instance du type pour fonctionner. Nous avons déjà utilisé une fonction comme celle-ci : la fonction `String::from` qui est définie sur le type `String`.

Les fonctions associées qui ne sont pas des méthodes sont souvent utilisées pour des constructeurs qui retourneront une nouvelle instance de la structure. Celles-ci sont souvent appelées `new`, mais `new` n'est pas un nom spécial et n'est pas intégré dans le langage. Par exemple, nous pourrions choisir de fournir une fonction associée nommée `square` qui aurait un paramètre de dimension et utiliserait cela comme largeur et hauteur, facilitant ainsi la création d'un `Rectangle` carré plutôt que de devoir spécifier la même valeur deux fois :

<span class="filename">Nom de fichier : src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/no-listing-03-associated-functions/src/main.rs:here}}
```

Les mots-clés `Self` dans le type de retour et dans le corps de la fonction sont des alias pour le type qui apparaît après le mot-clé `impl`, qui dans ce cas est `Rectangle`.

Pour appeler cette fonction associée, nous utilisons la syntaxe `::` avec le nom de la structure ; `let sq = Rectangle::square(3);` en est un exemple. Cette fonction est dans le namespace de la structure : la syntaxe `::` est utilisée à la fois pour les fonctions associées et les namespaces créés par les modules. Nous aborderons les modules dans [Chapitre 7][modules]<!-- ignore -->.

### Multiples Blocs `impl`

Chaque structure peut avoir plusieurs blocs `impl`. Par exemple, l'Extrait 5-15 est équivalent au code montré dans l'Extrait 5-16, qui a chaque méthode dans son propre bloc `impl`.

<Extrait number="5-16" caption="Réécriture de l'Extrait 5-15 utilisant plusieurs blocs `impl`">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-16/src/main.rs:here}}
```

</Extrait>

Il n'y a aucune raison de séparer ces méthodes en plusieurs blocs `impl` ici, mais cette syntaxe est valide. Nous verrons un cas dans lequel plusieurs blocs `impl` sont utiles au Chapitre 10, lorsque nous discuterons des types génériques et des traits.

## Résumé

Les structures vous permettent de créer des types personnalisés qui ont du sens pour votre domaine. En utilisant des structures, vous pouvez garder des morceaux de données associés connectés entre eux et nommer chaque pièce pour rendre votre code clair. Dans les blocs `impl`, vous pouvez définir des fonctions qui sont associées à votre type, et les méthodes sont une sorte de fonction associée qui vous permettent de spécifier le comportement que les instances de vos structures ont.

Mais les structures ne sont pas le seul moyen de créer des types personnalisés : tournons-nous vers la fonctionnalité enum de Rust pour ajouter un autre outil à votre boîte à outils.

[enums]: ch06-00-enums.html
[trait-objects]: ch18-02-trait-objects.md
[public]: ch07-03-paths-for-referring-to-an-item-in-the-module-tree.html#exposing-paths-with-the-pub-keyword
[modules]: ch07-02-defining-modules-to-control-scope-and-privacy.html