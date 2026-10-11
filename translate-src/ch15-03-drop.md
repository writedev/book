## Exécuter du code lors du nettoyage avec le trait `Drop`

Le deuxième trait important pour le modèle des pointeurs intelligents est `Drop`. Il vous permet de personnaliser ce qui se passe lorsqu’une valeur est sur le point de sortir de sa portée. Vous pouvez fournir une implémentation du trait `Drop` pour n’importe quel type, et ce code peut servir à libérer des ressources, comme des fichiers ou des connexions réseau.

Nous présentons `Drop` dans le contexte des pointeurs intelligents, car les fonctionnalités du trait `Drop` sont presque toujours utilisées lors de l’implémentation d’un pointeur intelligent. Par exemple, lorsqu’un `Box<T>` est détruit, il libère l’espace sur le tas vers lequel pointe la boîte.

Dans certains langages, pour certains types, le programmeur doit appeler du code pour libérer la mémoire ou les ressources chaque fois qu’il a fini d’utiliser une instance de ces types. C’est le cas, par exemple, des descripteurs de fichiers, des sockets et des verrous. Si le programmeur oublie de le faire, le système risque d’être surchargé et de planter. En Rust, vous pouvez indiquer qu’un morceau de code donné doit être exécuté chaque fois qu’une valeur sort de sa portée, et le compilateur insérera automatiquement ce code. Ainsi, vous n’avez pas à vous soucier de placer du code de nettoyage partout dans un programme dès qu’une instance d’un type donné n’est plus utilisée : vous ne laisserez malgré tout aucune ressource non libérée !

Vous indiquez le code à exécuter lorsqu’une valeur sort de sa portée en implémentant le trait `Drop`. Ce trait vous demande d’implémenter une méthode nommée `drop`, qui prend une référence mutable à `self`. Pour voir quand Rust appelle `drop`, implémentons pour l’instant `drop` avec des instructions `println!`.

La liste 15-14 présente une structure `CustomSmartPointer`, dont la seule fonctionnalité personnalisée consiste à afficher `Dropping CustomSmartPointer!` lorsque l’instance sort de sa portée, afin de montrer quand Rust exécute la méthode `drop`.

<Listing number="15-14" file-name="src/main.rs" caption="Une structure `CustomSmartPointer` qui implémente le trait `Drop`, dans lequel nous placerions notre code de nettoyage">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-14/src/main.rs}}
```

</Listing>

Le trait `Drop` est inclus dans le préambule, nous n’avons donc pas besoin de l’importer dans la portée. Nous implémentons le trait `Drop` pour `CustomSmartPointer` et fournissons une implémentation de la méthode `drop` qui appelle `println!`. C’est dans le corps de la méthode `drop` que vous placeriez toute logique que vous souhaitez exécuter lorsqu’une instance de votre type sort de sa portée. Ici, nous affichons du texte pour montrer visuellement quand Rust appelle `drop`.

Dans `main`, nous créons deux instances de `CustomSmartPointer`, puis affichons `CustomSmartPointers created`. À la fin de `main`, nos instances de `CustomSmartPointer` sortiront de leur portée, et Rust exécutera le code que nous avons placé dans la méthode `drop`, qui affichera notre dernier message. Remarquez que nous n’avons pas eu besoin d’appeler explicitement la méthode `drop`.

Lorsque nous exécutons ce programme, nous obtenons le résultat suivant :

```console
{{#include ../listings/ch15-smart-pointers/listing-15-14/output.txt}}
```

Rust a automatiquement appelé `drop` pour nous lorsque nos instances sont sorties de leur portée, en exécutant le code que nous avions indiqué. Les variables sont détruites dans l’ordre inverse de leur création : `d` a donc été détruite avant `c`. Cet exemple a pour but de vous montrer visuellement le fonctionnement de la méthode `drop` ; en général, vous indiqueriez le code de nettoyage que votre type doit exécuter plutôt qu’un message à afficher.

<!-- Old headings. Do not remove or links may break. -->

<a id="dropping-a-value-early-with-std-mem-drop"></a>

Malheureusement, il n’est pas simple de désactiver la fonctionnalité automatique de `drop`. Il n’est généralement pas nécessaire de désactiver `drop` : tout l’intérêt du trait `Drop` est que le nettoyage est pris en charge automatiquement. Il peut toutefois arriver que vous souhaitiez nettoyer une valeur plus tôt. C’est notamment le cas lorsque vous utilisez des pointeurs intelligents qui gèrent des verrous : vous pouvez vouloir forcer l’appel de la méthode `drop` qui libère le verrou, afin que d’autres portions de code dans la même portée puissent l’acquérir. Rust ne vous permet pas d’appeler manuellement la méthode `drop` du trait `Drop` ; à la place, si vous souhaitez forcer la destruction d’une valeur avant la fin de sa portée, vous devez appeler la fonction `std::mem::drop` fournie par la bibliothèque standard.

Tenter d’appeler manuellement la méthode `drop` du trait `Drop` en modifiant la fonction `main` de la liste 15-14 ne fonctionnera pas, comme le montre la liste 15-15.

<Listing number="15-15" file-name="src/main.rs" caption="Tentative d’appel manuel de la méthode `drop` du trait `Drop` pour effectuer un nettoyage anticipé">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-15/src/main.rs:here}}
```

</Listing>

Lorsque nous essayons de compiler ce code, nous obtenons l’erreur suivante :

```console
{{#include ../listings/ch15-smart-pointers/listing-15-15/output.txt}}
```

Ce message d’erreur indique que nous n’avons pas le droit d’appeler explicitement `drop`. Il utilise le terme _destructeur_, qui est le terme général en programmation désignant une fonction qui nettoie une instance. Un _destructeur_ est l’équivalent d’un _constructeur_, qui crée une instance. La fonction `drop` en Rust est un destructeur particulier.

Rust ne nous permet pas d’appeler explicitement `drop`, car Rust appellerait tout de même automatiquement `drop` sur la valeur à la fin de `main`. Cela provoquerait une erreur de double libération, car Rust tenterait de nettoyer deux fois la même valeur.

Nous ne pouvons ni désactiver l’insertion automatique de `drop` lorsqu’une valeur sort de sa portée, ni appeler explicitement la méthode `drop`. Ainsi, si nous devons forcer le nettoyage anticipé d’une valeur, nous utilisons la fonction `std::mem::drop`.

La fonction `std::mem::drop` est différente de la méthode `drop` du trait `Drop`. Nous l’appelons en lui passant en argument la valeur que nous voulons détruire de force. Cette fonction se trouve dans le préambule ; nous pouvons donc modifier `main` dans la liste 15-15 pour appeler la fonction `drop`, comme le montre la liste 15-16.

<Listing number="15-16" file-name="src/main.rs" caption="Appel de `std::mem::drop` pour détruire explicitement une valeur avant qu’elle ne sorte de sa portée">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-16/src/main.rs:here}}
```

</Listing>

L’exécution de ce code affiche le résultat suivant :

```console
{{#include ../listings/ch15-smart-pointers/listing-15-16/output.txt}}
```

Le texte ``Dropping CustomSmartPointer with data `some data`!`` s’affiche entre les textes `CustomSmartPointer created` et `CustomSmartPointer dropped before the end of main`, ce qui montre que le code de la méthode `drop` est appelé pour détruire `c` à ce moment-là.

Vous pouvez utiliser le code défini dans une implémentation du trait `Drop` de nombreuses façons pour faciliter et sécuriser le nettoyage. Vous pourriez, par exemple, l’utiliser pour créer votre propre allocateur de mémoire ! Grâce au trait `Drop` et au système de propriété de Rust, vous n’avez pas à vous souvenir de nettoyer les ressources, car Rust s’en charge automatiquement.

Vous n’avez pas non plus à vous soucier des problèmes qui pourraient survenir si vous nettoyiez accidentellement des valeurs encore utilisées : le système de propriété, qui garantit la validité des références, veille également à ce que `drop` ne soit appelé qu’une seule fois, lorsque la valeur n’est plus utilisée.

Maintenant que nous avons examiné `Box<T>` et certaines caractéristiques des pointeurs intelligents, étudions quelques autres pointeurs intelligents définis dans la bibliothèque standard.