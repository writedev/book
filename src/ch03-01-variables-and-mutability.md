## Variables et Mutabilité

Comme mentionné dans la section [« Stocker des valeurs avec des variables »][storing-values-with-variables]<!-- ignore -->, par défaut, les variables sont immuables. C'est l'une des nombreuses incitations que Rust vous propose pour écrire votre code de manière à tirer parti de la sécurité et de la facilité de concurrence que Rust offre. Cependant, vous avez toujours la possibilité de rendre vos variables mutables. Explorons comment et pourquoi Rust vous encourage à privilégier l'immuabilité et pourquoi vous voudriez parfois faire le choix inverse.

Lorsqu'une variable est immuable, une fois qu'une valeur est liée à un nom, vous ne pouvez pas changer cette valeur. Pour illustrer cela, générez un nouveau projet appelé _variables_ dans votre répertoire _projects_ en utilisant `cargo new variables`.

Ensuite, dans votre nouveau répertoire _variables_, ouvrez _src/main.rs_ et remplacez son code par le code suivant, qui ne va pas encore se compiler :

<span class="filename">Nom de fichier : src/main.rs</span>

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-01-variables-are-immutable/src/main.rs}}
```

Enregistrez et exécutez le programme en utilisant `cargo run`. Vous devriez recevoir un message d’erreur concernant une erreur d’immuabilité, comme le montre cette sortie :

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-01-variables-are-immutable/output.txt}}
```

Cet exemple montre comment le compilateur vous aide à trouver des erreurs dans vos programmes. Les erreurs de compilation peuvent être frustrantes, mais elles signifient simplement que votre programme ne fait pas encore ce que vous voulez qu'il fasse en toute sécurité ; elles ne signifient _pas_ que vous n'êtes pas un bon programmeur ! Les Rustaciens expérimentés reçoivent encore des erreurs de compilation.

Vous avez reçu le message d’erreur `` impossible d'assigner deux fois à la variable immuable `x` `` parce que vous avez essayé d'assigner une deuxième valeur à la variable immuable `x`.

Il est important d'obtenir des erreurs à la compilation lorsque nous tentons de changer une valeur désignée comme immuable, car cette situation peut entraîner des bogues. Si une partie de notre code fonctionne sur l’hypothèse qu’une valeur ne changera jamais et qu’une autre partie de notre code change cette valeur, il est possible que la première partie ne fasse pas ce pour quoi elle a été conçue. La cause de ce type de bogue peut être difficile à identifier par la suite, surtout lorsque la deuxième partie du code change la valeur seulement _parfois_. Le compilateur Rust garantit que lorsque vous déclarez qu'une valeur ne changera pas, elle ne changera vraiment pas, vous n'avez donc pas à la suivre vous-même. Votre code devient ainsi plus facile à raisonner.

Mais la mutabilité peut être très utile et rendre le code plus pratique à écrire. Bien que les variables soient immuables par défaut, vous pouvez les rendre mutables en ajoutant `mut` devant le nom de la variable, comme vous l'avez fait dans [le Chapitre 2][storing-values-with-variables]<!-- ignore -->. Ajouter `mut` transmet également l'intention aux futurs lecteurs du code en indiquant que d'autres parties du code changeront la valeur de cette variable.

Par exemple, changeons _src/main.rs_ pour le suivant :

<span class="filename">Nom de fichier : src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-02-adding-mut/src/main.rs}}
```

Lorsque nous exécutons maintenant le programme, nous obtenons cela :

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-02-adding-mut/output.txt}}
```

Nous sommes autorisés à changer la valeur liée à `x` de `5` à `6` lorsque `mut` est utilisé. Au final, décider d'utiliser ou non la mutabilité vous appartient et dépend de ce que vous pensez être le plus clair dans cette situation particulière.

<!-- Anciennes rubriques. Ne pas supprimer ou les liens peuvent se rompre. -->
<a id="constants"></a>

### Déclaration de Constantes

Comme les variables immuables, les _constantes_ sont des valeurs qui sont liées à un nom et ne sont pas autorisées à changer, mais il existe quelques différences entre les constantes et les variables.

Tout d'abord, vous n'êtes pas autorisé à utiliser `mut` avec des constantes. Les constantes ne sont pas seulement immuables par défaut - elles sont toujours immuables. Vous déclarez des constantes en utilisant le mot-clé `const` au lieu du mot-clé `let`, et le type de la valeur _doit_ être annoté. Nous aborderons les types et les annotations de type dans la section suivante, [« Types de données »][data-types]<!-- ignore -->, alors ne vous inquiétez pas des détails pour l'instant. Sachez simplement que vous devez toujours annoter le type.

Les constantes peuvent être déclarées dans n'importe quel contexte, y compris le contexte global, ce qui les rend utiles pour des valeurs que de nombreuses parties du code doivent connaître.

La dernière différence est que les constantes ne peuvent être définies que par une expression constante, et non par le résultat d'une valeur qui ne pourrait être calculé qu'à l'exécution.

Voici un exemple de déclaration d’une constante :

```rust
const THREE_HOURS_IN_SECONDS: u32 = 60 * 60 * 3;
```

Le nom de la constante est `THREE_HOURS_IN_SECONDS`, et sa valeur est définie par le résultat de la multiplication de 60 (le nombre de secondes dans une minute) par 60 (le nombre de minutes dans une heure) par 3 (le nombre d'heures que nous voulons compter dans ce programme). La convention de nommage de Rust pour les constantes est d'utiliser des lettres majuscules avec des underscores entre les mots. Le compilateur est capable d'évaluer un ensemble limité d'opérations à la compilation, ce qui nous permet d'écrire cette valeur d’une manière qui est plus facile à comprendre et à vérifier, plutôt que de définir cette constante à la valeur 10 800. Consultez la section sur l'[évaluation des constantes dans la référence Rust][const-eval] pour plus d'informations sur les opérations pouvant être utilisées lors de la déclaration de constantes.

Les constantes sont valables pendant toute la durée d'exécution d'un programme, dans le contexte où elles ont été déclarées. Cette propriété rend les constantes utiles pour des valeurs dans votre domaine d'application que plusieurs parties du programme pourraient avoir besoin de connaître, comme le nombre maximum de points qu'un joueur d'un jeu peut gagner, ou la vitesse de la lumière.

Nommer les valeurs codées en dur utilisées dans l'ensemble de votre programme en tant que constantes est utile pour transmettre la signification de cette valeur aux futurs mainteneurs du code. Il est également utile d'avoir un seul endroit dans votre code que vous auriez à modifier si la valeur codée en dur devait être mise à jour à l'avenir.

### Ombre

Comme vous l'avez vu dans le tutoriel de jeu de devinettes dans [le Chapitre 2][comparing-the-guess-to-the-secret-number]<!-- ignore -->, vous pouvez déclarer une nouvelle variable avec le même nom qu'une variable précédente. Les Rustaciens disent que la première variable est _ombragée_ par la seconde, ce qui signifie que la seconde variable est ce que le compilateur verra lorsque vous utiliserez le nom de la variable. En effet, la seconde variable éclipse la première, prenant toutes les utilisations du nom de la variable pour elle-même jusqu'à ce qu'elle-même soit ombragée ou que le contexte se termine. Nous pouvons ombrager une variable en utilisant le même nom de variable et en répétant l’utilisation du mot-clé `let` comme suit :

<span class="filename">Nom de fichier : src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-03-shadowing/src/main.rs}}
```

Ce programme lie d'abord `x` à une valeur de `5`. Ensuite, il crée une nouvelle variable `x` en répétant `let x =`, prenant la valeur d'origine et ajoutant `1` afin que la valeur de `x` soit `6`. Ensuite, dans un contexte interne créé avec les accolades, la troisième déclaration `let` ombrage également `x` et crée une nouvelle variable, multipliant la valeur précédente par `2` pour donner à `x` une valeur de `12`. Lorsque ce contexte est terminé, l'ombrage intérieur s'arrête et `x` retrouve sa valeur de `6`. Lorsque nous exécutons ce programme, il affichera ce qui suit :

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-03-shadowing/output.txt}}
```

L'ombrage est différent du marquage d'une variable comme `mut` car nous obtiendrons une erreur à la compilation si nous essayons par accident de réaffecter cette variable sans utiliser le mot-clé `let`. En utilisant `let`, nous pouvons effectuer quelques transformations sur une valeur, mais la variable devient immuable après que ces transformations aient été effectuées.

L'autre différence entre `mut` et l'ombrage est que, parce que nous créons effectivement une nouvelle variable lorsque nous utilisons à nouveau le mot-clé `let`, nous pouvons changer le type de la valeur tout en réutilisant le même nom. Par exemple, disons que notre programme demande à un utilisateur de montrer combien d'espaces ils veulent entre du texte en saisissant des caractères d'espace, et ensuite nous voulons stocker cette entrée en tant que nombre :

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-04-shadowing-can-change-types/src/main.rs:here}}
```

La première variable `spaces` est de type chaîne, et la seconde variable `spaces` est de type nombre. L'ombrage nous épargne donc d'avoir à venir avec différents noms, tels que `spaces_str` et `spaces_num` ; au lieu de cela, nous pouvons réutiliser le nom plus simple `spaces`. Cependant, si nous essayons d'utiliser `mut` pour cela, comme montré ici, nous obtiendrons une erreur à la compilation :

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-05-mut-cant-change-types/src/main.rs:here}}
```

L'erreur indique que nous ne sommes pas autorisés à modifier le type d'une variable :

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-05-mut-cant-change-types/output.txt}}
```

Maintenant que nous avons exploré comment fonctionnent les variables, examinons les types de données qu'elles peuvent avoir.

[comparing-the-guess-to-the-secret-number]: ch02-00-guessing-game-tutorial.html#comparing-the-guess-to-the-secret-number
[data-types]: ch03-02-data-types.html#data-types
[storing-values-with-variables]: ch02-00-guessing-game-tutorial.html#storing-values-with-variables
[const-eval]: ../reference/const_eval.html