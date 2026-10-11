## Un exemple de programme utilisant des structures

Pour comprendre quand nous pourrions vouloir utiliser des structures, écrivons un programme qui calcule l’aire d’un rectangle. Nous commencerons par utiliser des variables individuelles, puis nous refactoriserons le programme jusqu’à utiliser des structures.

Créons avec Cargo un nouveau projet binaire appelé _rectangles_ qui prendra la largeur et la hauteur d’un rectangle, exprimées en pixels, et calculera son aire. La liste 5-8 présente un court programme qui fait exactement cela dans le fichier _src/main.rs_ de notre projet.

<Listing number="5-8" file-name="src/main.rs" caption="Calcul de l’aire d’un rectangle dont la largeur et la hauteur sont spécifiées par des variables distinctes">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-08/src/main.rs:all}}
```

</Listing>

Exécutons maintenant ce programme avec `cargo run` :

```console
{{#include ../listings/ch05-using-structs-to-structure-related-data/listing-05-08/output.txt}}
```

Ce code parvient à calculer l’aire du rectangle en appelant la fonction `area` avec chacune de ses dimensions, mais nous pouvons rendre ce code plus clair et plus lisible.

Le problème de ce code apparaît clairement dans la signature de `area` :

```rust,ignore
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-08/src/main.rs:here}}
```

La fonction `area` est censée calculer l’aire d’un rectangle, mais la fonction que nous avons écrite possède deux paramètres, et rien dans notre programme n’indique clairement que ces paramètres sont liés. Il serait plus lisible et plus facile à gérer de regrouper la largeur et la hauteur. Nous avons déjà évoqué une façon de le faire dans la section [« Le type tuple »][the-tuple-type]<!-- ignore --> du chapitre 3 : en utilisant des tuples.

### Refactorisation avec des tuples

La liste 5-9 présente une autre version de notre programme, qui utilise des tuples.

<Listing number="5-9" file-name="src/main.rs" caption="Spécification de la largeur et de la hauteur du rectangle avec un tuple">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-09/src/main.rs}}
```

</Listing>

D’une certaine façon, ce programme est meilleur. Les tuples nous permettent d’ajouter un peu de structure, et nous ne transmettons désormais qu’un seul argument. Mais d’une autre façon, cette version est moins claire : les tuples ne nomment pas leurs éléments, nous devons donc accéder aux composants du tuple par leur indice, ce qui rend notre calcul moins évident.

Confondre la largeur et la hauteur n’aurait pas d’importance pour le calcul de l’aire, mais ce serait important si nous voulions dessiner le rectangle à l’écran ! Nous devrions nous rappeler que `width` correspond à l’indice `0` du tuple et `height` à l’indice `1`. Quelqu’un d’autre aurait encore plus de mal à comprendre et à retenir cela s’il utilisait notre code. Comme nous n’avons pas exprimé le sens de nos données dans notre code, il est désormais plus facile d’introduire des erreurs.

<!-- Old headings. Do not remove or links may break. -->

<a id="refactoring-with-structs-adding-more-meaning"></a>

### Refactorisation avec des structures

Nous utilisons des structures pour donner du sens aux données en les étiquetant. Nous pouvons transformer le tuple que nous utilisons en une structure portant un nom pour l’ensemble ainsi que des noms pour ses composants, comme le montre la liste 5-10.

<Listing number="5-10" file-name="src/main.rs" caption="Définition d’une structure `Rectangle`">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-10/src/main.rs}}
```

</Listing>

Ici, nous avons défini une structure et l’avons nommée `Rectangle`. Entre les accolades, nous avons défini les champs `width` et `height`, qui sont tous deux de type `u32`. Puis, dans `main`, nous avons créé une instance particulière de `Rectangle` dont la largeur est de `30` et la hauteur de `50`.

Notre fonction `area` est maintenant définie avec un seul paramètre, que nous avons nommé `rectangle`, dont le type est un emprunt immuable d’une instance de la structure `Rectangle`. Comme nous l’avons indiqué au chapitre 4, nous voulons emprunter la structure plutôt que d’en prendre possession. Ainsi, `main` en conserve la propriété et peut continuer à utiliser `rect1`, raison pour laquelle nous utilisons `&` dans la signature de la fonction et lors de son appel.

La fonction `area` accède aux champs `width` et `height` de l’instance `Rectangle` (notez que l’accès aux champs d’une instance empruntée d’une structure ne déplace pas les valeurs des champs, ce qui explique pourquoi on voit souvent des emprunts de structures). La signature de notre fonction `area` exprime maintenant exactement ce que nous voulons dire : calculer l’aire de `Rectangle` à l’aide de ses champs `width` et `height`. Elle indique que la largeur et la hauteur sont liées, et donne des noms descriptifs aux valeurs au lieu d’utiliser les indices `0` et `1` du tuple. C’est un gain en clarté.

<!-- Old headings. Do not remove or links may break. -->

<a id="adding-useful-functionality-with-derived-traits"></a>

### Ajouter des fonctionnalités avec des traits dérivés

Il serait utile de pouvoir afficher une instance de `Rectangle` pendant que nous déboguons notre programme et de voir les valeurs de tous ses champs. La liste 5-11 essaie d’utiliser la macro [`println!`][println]<!-- ignore --> comme nous l’avons fait dans les chapitres précédents. Cependant, cela ne fonctionnera pas.

<Listing number="5-11" file-name="src/main.rs" caption="Tentative d’affichage d’une instance de `Rectangle`">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-11/src/main.rs}}
```

</Listing>

Lorsque nous compilons ce code, nous obtenons une erreur dont le message principal est le suivant :

```text
{{#include ../listings/ch05-using-structs-to-structure-related-data/listing-05-11/output.txt:3}}
```

La macro `println!` peut effectuer de nombreux types de formatage et, par défaut, les accolades indiquent à `println!` d’utiliser un formatage appelé `Display` : une sortie destinée à être directement lue par l’utilisateur final. Les types primitifs que nous avons vus jusqu’ici implémentent `Display` par défaut, car il n’existe qu’une seule façon de vouloir afficher un `1` ou tout autre type primitif à un utilisateur. Mais, avec les structures, la façon dont `println!` doit formater la sortie est moins évidente, car les possibilités d’affichage sont plus nombreuses : veut-on des virgules ou non ? Veut-on afficher les accolades ? Tous les champs doivent-ils être affichés ? En raison de cette ambiguïté, Rust n’essaie pas de deviner ce que nous voulons, et les structures ne disposent pas d’une implémentation de `Display` à utiliser avec `println!` et l’espace réservé `{}`.

Si nous continuons à lire les erreurs, nous trouverons cette remarque utile :

```text
{{#include ../listings/ch05-using-structs-to-structure-related-data/listing-05-11/output.txt:9:10}}
```

Essayons ! L’appel de la macro `println!` ressemblera désormais à `println!("rect1 is
{rect1:?}");`. Le spécificateur `:?` entre les accolades indique à `println!` que nous voulons utiliser un format de sortie appelé `Debug`. Le trait `Debug` nous permet d’afficher notre structure d’une manière utile aux développeurs, afin que nous puissions en voir la valeur pendant que nous déboguons notre code.

Compilons le code après cette modification. Zut ! Nous obtenons toujours une erreur :

```text
{{#include ../listings/ch05-using-structs-to-structure-related-data/output-only-01-debug/output.txt:3}}
```

Mais, une fois encore, le compilateur nous donne une remarque utile :

```text
{{#include ../listings/ch05-using-structs-to-structure-related-data/output-only-01-debug/output.txt:9:10}}
```

Rust inclut bien des fonctionnalités permettant d’afficher des informations de débogage, mais nous devons explicitement choisir de les rendre disponibles pour notre structure. Pour cela, nous ajoutons l’attribut externe `#[derive(Debug)]` juste avant la définition de la structure, comme le montre la liste 5-12.

<Listing number="5-12" file-name="src/main.rs" caption="Ajout de l’attribut pour dériver le trait `Debug` et affichage de l’instance `Rectangle` avec le formatage de débogage">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-12/src/main.rs}}
```

</Listing>

Maintenant, lorsque nous exécutons le programme, nous n’obtenons aucune erreur et voyons la sortie suivante :

```console
{{#include ../listings/ch05-using-structs-to-structure-related-data/listing-05-12/output.txt}}
```

Très bien ! Le résultat n’est pas des plus jolis, mais il affiche les valeurs de tous les champs de cette instance, ce qui serait certainement utile lors du débogage. Lorsque nous avons des structures plus volumineuses, il est utile d’obtenir une sortie un peu plus facile à lire ; dans ces cas-là, nous pouvons utiliser `{:#?}` au lieu de `{:?}` dans la chaîne de `println!`. Dans cet exemple, le format `{:#?}` produira la sortie suivante :

```console
{{#include ../listings/ch05-using-structs-to-structure-related-data/output-only-02-pretty-debug/output.txt}}
```

Une autre façon d’afficher une valeur avec le format `Debug` consiste à utiliser la [macro `dbg!`][dbg]<!-- ignore -->, qui prend possession d’une expression (contrairement à `println!`, qui prend une référence), affiche le nom du fichier et le numéro de ligne où se trouve l’appel de la macro `dbg!` dans votre code ainsi que la valeur obtenue pour cette expression, puis rend la propriété de la valeur.

> Remarque : l’appel de la macro `dbg!` affiche le résultat dans le flux de la console d’erreur standard (`stderr`), contrairement à `println!`, qui l’affiche dans le flux de la sortie standard (`stdout`). Nous parlerons davantage de `stderr` et de `stdout` dans la section [« Rediriger les erreurs vers la sortie d’erreur standard » du chapitre 12][err]<!-- ignore -->.

Voici un exemple dans lequel nous nous intéressons à la valeur assignée au champ `width`, ainsi qu’à la valeur de l’ensemble de la structure dans `rect1` :

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/no-listing-05-dbg-macro/src/main.rs}}
```

Nous pouvons placer `dbg!` autour de l’expression `30 * scale` et, comme `dbg!` rend la propriété de la valeur de l’expression, le champ `width` recevra la même valeur que si l’appel à `dbg!` n’était pas présent. Nous ne voulons pas que `dbg!` prenne possession de `rect1`, donc nous utilisons une référence à `rect1` lors de l’appel suivant. Voici à quoi ressemble la sortie de cet exemple :

```console
{{#include ../listings/ch05-using-structs-to-structure-related-data/no-listing-05-dbg-macro/output.txt}}
```

Nous pouvons voir que le premier élément de la sortie provient de la ligne 10 du fichier _src/main.rs_, où nous déboguons l’expression `30 * scale`, et que sa valeur obtenue est `60` (le formatage `Debug` implémenté pour les entiers consiste à n’afficher que leur valeur). L’appel de `dbg!` à la ligne 14 de _src/main.rs_ affiche la valeur de `&rect1`, qui est la structure `Rectangle`. Cette sortie utilise le formatage `Debug` détaillé du type `Rectangle`. La macro `dbg!` peut être très utile lorsque vous cherchez à comprendre ce que fait votre code !

En plus du trait `Debug`, Rust nous fournit plusieurs traits que nous pouvons utiliser avec l’attribut `derive` pour ajouter des comportements utiles à nos types personnalisés. Ces traits et leurs comportements sont répertoriés dans [l’annexe C][app-c]<!--
ignore -->. Nous verrons au chapitre 10 comment implémenter ces traits avec un comportement personnalisé et comment créer nos propres traits. Il existe également de nombreux attributs autres que `derive` ; pour en savoir plus, consultez la section [« Attributs » de la référence Rust][attributes].

Notre fonction `area` est très spécifique : elle ne calcule que l’aire des rectangles. Il serait utile d’associer davantage ce comportement à notre structure `Rectangle`, car il ne fonctionnerait avec aucun autre type. Voyons comment poursuivre la refactorisation de ce code en transformant la fonction `area` en une méthode `area` définie sur notre type `Rectangle`.

[the-tuple-type]: ch03-02-data-types.html#the-tuple-type
[app-c]: appendix-03-derivable-traits.md
[println]: ../std/macro.println.html
[dbg]: ../std/macro.dbg.html
[err]: ch12-06-writing-to-stderr-instead-of-stdout.html
[attributes]: ../reference/attributes.html