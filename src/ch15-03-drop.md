## Exécution de code lors du nettoyage avec le trait `Drop`

Le deuxième trait important dans le modèle de pointeur intelligent est `Drop`, qui vous permet de personnaliser ce qui se passe lorsqu'une valeur est sur le point de sortir de son contexte. Vous pouvez fournir une implémentation pour le trait `Drop` sur n'importe quel type, et ce code peut être utilisé pour libérer des ressources comme des fichiers ou des connexions réseau.

Nous introduisons `Drop` dans le contexte des pointeurs intelligents car la fonctionnalité du trait `Drop` est presque toujours utilisée lors de l'implémentation d'un pointeur intelligent. Par exemple, lorsqu'un `Box<T>` est abandonné, il libère l'espace sur le tas vers lequel la boîte pointe.

Dans certaines langues, pour certains types, le programmeur doit appeler du code pour libérer la mémoire ou les ressources chaque fois qu'il termine d'utiliser une instance de ces types. Les exemples incluent les descripteurs de fichiers, les sockets et les verrous. Si le programmeur oublie, le système peut être surchargé et se bloquer. En Rust, vous pouvez spécifier qu'un certain morceau de code doit être exécuté chaque fois qu'une valeur sort de son contexte, et le compilateur insérera ce code automatiquement. En conséquence, vous n'avez pas besoin d'être prudent en plaçant le code de nettoyage partout dans un programme dès qu'une instance d'un type particulier est terminée—vous ne perdrez toujours pas de ressources !

Vous spécifiez le code à exécuter lorsqu'une valeur sort de son contexte en implémentant le trait `Drop`. Le trait `Drop` exige que vous implémentiez une méthode nommée `drop` qui prend une référence mutable à `self`. Pour voir quand Rust appelle `drop`, implémentons `drop` avec des instructions `println!` pour l'instant.

Le listing 15-14 montre une structure `CustomSmartPointer` dont la seule fonctionnalité personnalisée est qu'elle imprimera `Dropping CustomSmartPointer!` lorsque l'instance sort de son contexte, pour montrer quand Rust exécute la méthode `drop`.

<Listing number="15-14" file-name="src/main.rs" caption="Une structure `CustomSmartPointer` qui implémente le trait `Drop` où nous mettrions notre code de nettoyage">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-14/src/main.rs}}
```

</Listing>

Le trait `Drop` est inclus dans le préambule, donc nous n'avons pas besoin de le faire entrer dans le contexte. Nous implémentons le trait `Drop` sur `CustomSmartPointer` et fournissons une implémentation pour la méthode `drop` qui appelle `println!`. Le corps de la méthode `drop` est l'endroit où vous placeriez la logique que vous souhaitez exécuter lorsqu'une instance de votre type sort de son contexte. Nous imprimons ici du texte pour démontrer visuellement quand Rust appellera `drop`.

Dans `main`, nous créons deux instances de `CustomSmartPointer` puis imprimons `CustomSmartPointers created`. À la fin de `main`, nos instances de `CustomSmartPointer` sortiront de leur contexte, et Rust appellera le code que nous avons placé dans la méthode `drop`, imprimant notre message final. Notez que nous n'avons pas besoin d'appeler la méthode `drop` explicitement.

Lorsque nous exécutons ce programme, nous verrons la sortie suivante :

```console
{{#include ../listings/ch15-smart-pointers/listing-15-14/output.txt}}
```

Rust a automatiquement appelé `drop` pour nous lorsque nos instances sont sorties de leur contexte, appelant le code que nous avons spécifié. Les variables sont abandonnées dans l'ordre inverse de leur création, donc `d` a été abandonné avant `c`. L'objectif de cet exemple est de vous donner un guide visuel sur le fonctionnement de la méthode `drop`; en général, vous spécifieriez le code de nettoyage dont votre type a besoin plutôt qu'un message d'impression.

<a id="dropping-a-value-early-with-std-mem-drop"></a>

Malheureusement, il n'est pas évident de désactiver la fonctionnalité automatique `drop`. Désactiver `drop` n'est généralement pas nécessaire ; tout l'intérêt du trait `Drop` est qu'il est géré automatiquement. Cependant, il peut arriver que vous souhaitiez nettoyer une valeur plus tôt. Un exemple est lorsque vous utilisez des pointeurs intelligents qui gèrent des verrous : vous pourriez vouloir forcer la méthode `drop` qui libère le verrou afin que d'autres codes dans le même contexte puissent acquérir le verrou. Rust ne vous permet pas d'appeler la méthode `drop` du trait `Drop` manuellement ; vous devez plutôt appeler la fonction `std::mem::drop` fournie par la bibliothèque standard si vous voulez forcer une valeur à être abandonnée avant la fin de son contexte.

Essayer d'appeler manuellement la méthode `drop` du trait `Drop` en modifiant la fonction `main` du listing 15-14 ne fonctionnera pas, comme le montre le listing 15-15.

<Listing number="15-15" file-name="src/main.rs" caption="Tentative d'appeler manuellement la méthode `drop` du trait `Drop` pour nettoyer tôt">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-15/src/main.rs:here}}
```

</Listing>

Lorsque nous essayons de compiler ce code, nous obtiendrons cette erreur :

```console
{{#include ../listings/ch15-smart-pointers/listing-15-15/output.txt}}
```

Ce message d'erreur indique que nous ne sommes pas autorisés à appeler explicitement `drop`. Le message d'erreur utilise le terme _destructeur_, qui est le terme général en programmation pour une fonction qui nettoie une instance. Un _destructeur_ est analogue à un _constructeur_, qui crée une instance. La fonction `drop` en Rust est un destructeur particulier.

Rust ne nous permet pas d'appeler `drop` explicitement, car Rust appellerait toujours automatiquement `drop` sur la valeur à la fin de `main`. Cela provoquerait une erreur de double libération car Rust essaierait de nettoyer la même valeur deux fois.

Nous ne pouvons pas désactiver l'insertion automatique de `drop` lorsque qu'une valeur sort de son contexte, et nous ne pouvons pas appeler la méthode `drop` explicitement. Donc, si nous avons besoin de forcer une valeur à être nettoyée plus tôt, nous utilisons la fonction `std::mem::drop`.

La fonction `std::mem::drop` est différente de la méthode `drop` dans le trait `Drop`. Nous l'appelons en passant en argument la valeur que nous voulons forcer à être abandonnée. La fonction est dans le préambule, donc nous pouvons modifier `main` dans le listing 15-15 pour appeler la fonction `drop`, comme le montre le listing 15-16.

<Listing number="15-16" file-name="src/main.rs" caption="Appel de `std::mem::drop` pour explicitement abandonner une valeur avant qu'elle ne sorte de son contexte">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-16/src/main.rs:here}}
```

</Listing>

L'exécution de ce code imprimera ce qui suit :

```console
{{#include ../listings/ch15-smart-pointers/listing-15-16/output.txt}}
```

Le texte ``Dropping CustomSmartPointer with data `some data`!`` est imprimé entre le texte `CustomSmartPointer created` et `CustomSmartPointer dropped before the end of main`, montrant que le code de la méthode `drop` est appelé pour abandonner `c` à ce moment-là.

Vous pouvez utiliser le code spécifié dans une implémentation du trait `Drop` de nombreuses manières pour rendre le nettoyage pratique et sûr : par exemple, vous pourriez l'utiliser pour créer votre propre allocateur de mémoire ! Avec le trait `Drop` et le système de propriété de Rust, vous n'avez pas à vous rappeler de nettoyer, car Rust le fait automatiquement.

Vous n'avez également pas à vous soucier des problèmes résultant d'un nettoyage accidentel de valeurs encore utilisées : le système de propriété qui garantit que les références sont toujours valides garantit également que `drop` est appelé une seule fois lorsque la valeur n'est plus utilisée.

Maintenant que nous avons examiné `Box<T>` et certaines des caractéristiques des pointeurs intelligents, regardons quelques autres pointeurs intelligents définis dans la bibliothèque standard.