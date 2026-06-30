## Un Exemple de Programme Utilisant des Structures

Pour comprendre quand nous pourrions vouloir utiliser des structures, écrivons un programme qui calcule l'aire d'un rectangle. Nous commencerons par utiliser des variables simples, puis nous refactoriserons le programme jusqu'à ce que nous utilisions des structures.

Créons un nouveau projet binaire avec Cargo appelé _rectangles_ qui prendra la largeur et la hauteur d'un rectangle spécifié en pixels et calculera l'aire de ce rectangle. La liste 5-8 montre une courte programme pour faire exactement cela dans le fichier _src/main.rs_ de notre projet.

<Listing number="5-8" file-name="src/main.rs" caption="Calcul de l'aire d'un rectangle spécifiée par des variables de largeur et de hauteur séparées">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-08/src/main.rs:all}}
```

</Listing>

Maintenant, exécutez ce programme en utilisant `cargo run` :

```console
{{#include ../listings/ch05-using-structs-to-structure-related-data/listing-05-08/output.txt}}
```

Ce code réussit à déterminer l'aire du rectangle en appelant la fonction `area` avec chaque dimension, mais nous pouvons faire plus pour rendre ce code clair et lisible.

Le problème avec ce code est évident dans la signature de `area` :

```rust,ignore
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-08/src/main.rs:here}}
```

La fonction `area` est censée calculer l'aire d'un rectangle, mais la fonction que nous avons écrite a deux paramètres, et il n'est nulle part clair que les paramètres sont liés. Il serait plus lisible et plus gérable de regrouper la largeur et la hauteur ensemble. Nous avons déjà discuté d'une façon dont nous pourrions faire cela dans la section [“Le type tuple”][the-tuple-type]<!-- ignore --> du Chapitre 3 : en utilisant des tuples.

### Refactorisation avec des Tuples

La liste 5-9 montre une autre version de notre programme qui utilise des tuples.

<Listing number="5-9" file-name="src/main.rs" caption="Spécification de la largeur et de la hauteur du rectangle avec un tuple">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-09/src/main.rs}}
```

</Listing>

D'une certaine manière, ce programme est meilleur. Les tuples nous permettent d'ajouter un peu de structure, et nous passons maintenant un seul argument. Mais d'une autre manière, cette version est moins claire : les tuples ne nomment pas leurs éléments, donc nous devons indexer les parties du tuple, rendant notre calcul moins évident.

Mélanger la largeur et la hauteur ne poserait pas de problème pour le calcul de l'aire, mais si nous voulons dessiner le rectangle à l'écran, cela aurait de l'importance ! Nous devrions garder à l'esprit que `width` est l'index du tuple `0` et que `height` est l'index du tuple `1`. Cela serait encore plus difficile à comprendre pour quelqu'un d'autre s'il devait utiliser notre code. Puisque nous n'avons pas transmis la signification de nos données dans notre code, il est maintenant plus facile d'introduire des erreurs.

### Refactorisation avec des Structures

Nous utilisons des structures pour ajouter du sens en étiquetant les données. Nous pouvons transformer le tuple que nous utilisons en une structure avec un nom pour l'ensemble ainsi que des noms pour les parties, comme montré dans la liste 5-10.

<Listing number="5-10" file-name="src/main.rs" caption="Définition d'une structure `Rectangle`">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-10/src/main.rs}}
```

</Listing>

Ici, nous avons défini une structure et l'avons nommée `Rectangle`. À l'intérieur des accolades, nous avons défini les champs de `width` et `height`, tous deux de type `u32`. Ensuite, dans `main`, nous avons créé une instance particulière de `Rectangle` ayant une largeur de `30` et une hauteur de `50`.

Notre fonction `area` est maintenant définie avec un paramètre, que nous avons nommé `rectangle`, dont le type est un emprunt immuable d'une instance de structure `Rectangle`. Comme mentionné au Chapitre 4, nous voulons emprunter la structure plutôt que d'en prendre possession. De cette manière, `main` conserve cette possession et peut continuer à utiliser `rect1`, qui est la raison pour laquelle nous utilisons `&` dans la signature de la fonction et là où nous appelons la fonction.

La fonction `area` accède aux champs `width` et `height` de l'instance `Rectangle` (notez qu'accéder aux champs d'une instance de structure empruntée ne déplace pas les valeurs des champs, c'est pourquoi vous voyez souvent des emprunts de structures). Notre signature de fonction pour `area` dit maintenant exactement ce que nous voulons dire : calculez l'aire d'un `Rectangle`, en utilisant ses champs `width` et `height`. Cela indique que la largeur et la hauteur sont liées entre elles, et cela donne des noms descriptifs aux valeurs au lieu d'utiliser les valeurs d'index du tuple `0` et `1`. Cela améliore la clarté.

### Ajout de Fonctionnalités avec des Traits Dérivés

Il serait utile de pouvoir imprimer une instance de `Rectangle` pendant que nous déboguons notre programme et voir les valeurs de tous ses champs. La liste 5-11 tente d'utiliser la macro [`println!`][println]<!-- ignore --> comme nous l'avons fait dans les chapitres précédents. Cela ne fonctionnera cependant pas.

<Listing number="5-11" file-name="src/main.rs" caption="Tentative d'imprimer une instance de `Rectangle`">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-11/src/main.rs}}
```

</Listing>

Lorsque nous compilons ce code, nous obtenons une erreur avec ce message central :

```text
{{#include ../listings/ch05-using-structs-to-structure-related-data/listing-05-11/output.txt:3}}
```

La macro `println!` peut faire de nombreux types de formatage, et par défaut, les accolades indiquent à `println!` d'utiliser un formatage connu sous le nom de `Display` : une sortie destinée à être directement consommée par l'utilisateur final. Les types primitifs que nous avons vus jusqu'à présent implémentent `Display` par défaut car il n'y a qu'une seule manière dont vous voudriez montrer un `1` ou tout autre type primitif à un utilisateur. Mais avec les structures, la manière dont `println!` doit formater la sortie est moins claire car il y a plus de possibilités d'affichage : voulez-vous des virgules ou pas ? Voulez-vous imprimer les accolades ? Tous les champs doivent-ils être affichés ? En raison de cette ambiguïté, Rust ne tente pas de deviner ce que nous voulons, et les structures n'ont pas d'implémentation fournie de `Display` à utiliser avec `println!` et le placeholder `{}`.

Si nous continuons à lire les erreurs, nous trouverons cette note utile :

```text
{{#include ../listings/ch05-using-structs-to-structure-related-data/listing-05-11/output.txt:9:10}}
```

Essayons ! L'appel à la macro `println!` ressemblera maintenant à `println!("rect1 est {rect1:?}");`. Mettre le spécificateur `:?` à l'intérieur des accolades indique à `println!` que nous voulons utiliser un format de sortie appelé `Debug`. Le trait `Debug` nous permet d'imprimer notre structure d'une manière utile pour les développeurs afin que nous puissions voir sa valeur pendant que nous déboguons notre code.

Compilez le code avec ce changement. Zut ! Nous obtenons encore une erreur :

```text
{{#include ../listings/ch05-using-structs-to-structure-related-data/output-only-01-debug/output.txt:3}}
```

Mais encore une fois, le compilateur nous donne une note utile :

```text
{{#include ../listings/ch05-using-structs-to-structure-related-data/output-only-01-debug/output.txt:9:10}}
```

Rust _dispose_ de la fonctionnalité permettant d'imprimer des informations de débogage, mais nous devons explicitement choisir d'activer cette fonctionnalité pour notre structure. Pour cela, nous ajoutons l'attribut externe `#[derive(Debug)]` juste avant la définition de la structure, comme montré dans la liste 5-12.

<Listing number="5-12" file-name="src/main.rs" caption="Ajout de l'attribut pour dériver le trait `Debug` et imprimer l'instance de `Rectangle` en utilisant un formatage de débogage">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-12/src/main.rs}}
```

</Listing>

Maintenant, lorsque nous exécutons le programme, nous n'obtiendrons plus d'erreurs, et nous verrons la sortie suivante :

```console
{{#include ../listings/ch05-using-structs-to-structure-related-data/listing-05-12/output.txt}}
```

Bien ! Ce n'est pas la sortie la plus jolie, mais elle montre les valeurs de tous les champs pour cette instance, ce qui aiderait certainement pendant le débogage. Lorsque nous avons des structures plus grandes, il est utile d'avoir une sortie un peu plus facile à lire ; dans ces cas, nous pouvons utiliser `{:#?}` au lieu de `{:?}` dans la chaîne `println!`. Dans cet exemple, utiliser le style `{:#?}` produira la sortie suivante :

```console
{{#include ../listings/ch05-using-structs-to-structure-related-data/output-only-02-pretty-debug/output.txt}}
```

Une autre façon d'imprimer une valeur en utilisant le format `Debug` est d'utiliser la macro [`dbg!`][dbg]<!-- ignore -->, qui prend possession d'une expression (contrairement à `println!`, qui prend une référence), imprime le fichier et le numéro de ligne où cet appel de la macro `dbg!` se produit dans votre code avec la valeur résultante de cette expression, et retourne la possession de la valeur.

> Remarque : Appeler la macro `dbg!` imprime dans le flux de la console d'erreurs standard (`stderr`), contrairement à `println!`, qui imprime dans le flux de sortie standard de la console (`stdout`). Nous aborderons davantage `stderr` et `stdout` dans la section [“Redirection des Erreurs vers l'Erreur Standard” du Chapitre
> 12][err]<!-- ignore -->.

Voici un exemple où nous sommes intéressés par la valeur qui est assignée au champ `width`, ainsi que par la valeur de la structure entière dans `rect1` :

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/no-listing-05-dbg-macro/src/main.rs}}
```

Nous pouvons mettre `dbg!` autour de l'expression `30 * scale` et, parce que `dbg!` retourne la possession de la valeur de l'expression, le champ `width` obtiendra la même valeur que si nous n'avions pas l'appel `dbg!` là. Nous ne voulons pas que `dbg!` prenne possession de `rect1`, donc nous utilisons une référence à `rect1` dans l'appel suivant. Voici à quoi ressemble la sortie de cet exemple :

```console
{{#include ../listings/ch05-using-structs-to-structure-related-data/no-listing-05-dbg-macro/output.txt}}
```

Nous pouvons voir que le premier bit de sortie provient de _src/main.rs_ ligne 10 où nous déboguons l'expression `30 * scale`, et sa valeur résultante est `60` (le formatage `Debug` implémenté pour les entiers consiste à imprimer uniquement leur valeur). L'appel `dbg!` à la ligne 14 de _src/main.rs_ imprime la valeur de `&rect1`, qui est la structure `Rectangle`. Cette sortie utilise le format `Debug` joli du type `Rectangle`. La macro `dbg!` peut être vraiment utile lorsque vous essayez de comprendre ce que fait votre code !

En plus du trait `Debug`, Rust a fourni un certain nombre de traits que nous pouvons utiliser avec l'attribut `derive` qui peuvent ajouter un comportement utile à nos types personnalisés. Ces traits et leurs comportements sont énumérés dans l'[Annexe C][app-c]<!-- ignore -->. Nous couvrirons comment implémenter ces traits avec un comportement personnalisé ainsi que comment créer vos propres traits au Chapitre 10. Il existe également de nombreux attributs autres que `derive` ; pour plus d'informations, voir [la section “Attributs” de la Référence Rust][attributes].

Notre fonction `area` est très spécifique : elle ne calcule que l'aire des rectangles. Il serait utile de lier ce comportement plus étroitement à notre structure `Rectangle` car elle ne fonctionnera pas avec d'autres types. Voyons comment nous pouvons continuer à refactoriser ce code en transformant la fonction `area` en une méthode `area` définie sur notre type `Rectangle`.

[the-tuple-type]: ch03-02-data-types.html#the-tuple-type
[app-c]: appendix-03-derivable-traits.md
[println]: ../std/macro.println.html
[dbg]: ../std/macro.dbg.html
[err]: ch12-06-writing-to-stderr-instead-of-stdout.html
[attributes]: ../reference/attributes.html