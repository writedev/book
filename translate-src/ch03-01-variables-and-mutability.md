## Variables et mutabilité

Comme indiqué dans la section [« Stocker des valeurs avec des variables »][storing-values-with-variables]<!-- ignore -->, les variables sont immuables par défaut. C’est l’un des nombreux encouragements que Rust vous donne à écrire votre code de manière à tirer parti de la sécurité et de la facilité de concurrence qu’offre Rust. Vous avez toutefois la possibilité de rendre vos variables mutables. Voyons comment et pourquoi Rust vous encourage à privilégier l’immutabilité, et pourquoi vous pourriez parfois vouloir y renoncer.

Lorsqu’une variable est immuable, une fois qu’une valeur lui est associée, vous ne pouvez pas modifier cette valeur. Pour illustrer cela, créez un nouveau projet appelé _variables_ dans votre répertoire _projects_ à l’aide de `cargo new variables`.

Ensuite, dans votre nouveau répertoire _variables_, ouvrez _src/main.rs_ et remplacez son code par le code suivant, qui ne compilera pas encore :

<span class="filename">Fichier : src/main.rs</span>

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-01-variables-are-immutable/src/main.rs}}
```

Enregistrez et exécutez le programme avec `cargo run`. Vous devriez recevoir un message d’erreur concernant l’immutabilité, comme le montre cette sortie :

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-01-variables-are-immutable/output.txt}}
```

Cet exemple montre comment le compilateur vous aide à trouver les erreurs dans vos programmes. Les erreurs du compilateur peuvent être frustrantes, mais elles signifient simplement que votre programme ne fait pas encore en toute sécurité ce que vous souhaitez ; elles ne signifient _pas_ que vous n’êtes pas un bon programmeur ! Même les Rustacés expérimentés rencontrent des erreurs du compilateur.

Vous avez reçu le message d’erreur `` cannot assign twice to immutable variable `x` `` parce que vous avez essayé d’affecter une seconde valeur à la variable immuable `x`.

Il est important d’obtenir des erreurs à la compilation lorsque nous essayons de modifier une valeur déclarée immuable, car cette situation peut entraîner des bogues. Si une partie de notre code part du principe qu’une valeur ne changera jamais et qu’une autre partie du code modifie cette valeur, il est possible que la première partie du code ne fasse pas ce pour quoi elle a été conçue. La cause de ce type de bogue peut être difficile à retrouver après coup, surtout lorsque la seconde partie du code ne modifie la valeur que _parfois_. Le compilateur Rust garantit que lorsqu’on déclare qu’une valeur ne changera pas, elle ne changera effectivement pas : vous n’avez donc pas besoin de le vérifier vous-même. Votre code est ainsi plus facile à comprendre.

La mutabilité peut toutefois être très utile et rendre le code plus pratique à écrire. Bien que les variables soient immuables par défaut, vous pouvez les rendre mutables en ajoutant `mut` devant le nom de la variable, comme vous l’avez fait au [chapitre 2][storing-values-with-variables]<!-- ignore -->. L’ajout de `mut` indique également votre intention aux futurs lecteurs du code, en signalant que d’autres parties du code modifieront la valeur de cette variable.

Par exemple, modifions _src/main.rs_ comme suit :

<span class="filename">Fichier : src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-02-adding-mut/src/main.rs}}
```

Lorsque nous exécutons le programme maintenant, nous obtenons ceci :

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-02-adding-mut/output.txt}}
```

Lorsque `mut` est utilisé, nous pouvons modifier la valeur associée à `x`, en passant de `5` à `6`. En définitive, la décision d’utiliser ou non la mutabilité vous appartient et dépend de ce qui vous semble le plus clair dans la situation concernée.

<!-- Old headings. Do not remove or links may break. -->
<a id="constants"></a>

### Déclarer des constantes

Comme les variables immuables, les _constantes_ sont des valeurs associées à un nom et qu’il n’est pas permis de modifier, mais il existe quelques différences entre les constantes et les variables.

Tout d’abord, vous ne pouvez pas utiliser `mut` avec des constantes. Les constantes ne sont pas simplement immuables par défaut : elles le sont toujours. Vous déclarez les constantes avec le mot-clé `const` plutôt qu’avec le mot-clé `let`, et le type de la valeur _doit_ être annoté. Nous aborderons les types et les annotations de type dans la section suivante, [« Types de données »][data-types]<!-- ignore --> ; ne vous souciez donc pas des détails pour l’instant. Retenez simplement que vous devez toujours annoter le type.

Les constantes peuvent être déclarées dans n’importe quelle portée, y compris la portée globale, ce qui les rend utiles pour les valeurs que plusieurs parties du code doivent connaître.

La dernière différence est que les constantes ne peuvent recevoir qu’une expression constante, et non le résultat d’une valeur qui ne pourrait être calculée qu’à l’exécution.

Voici un exemple de déclaration de constante :

```rust
const THREE_HOURS_IN_SECONDS: u32 = 60 * 60 * 3;
```

Le nom de la constante est `THREE_HOURS_IN_SECONDS`, et sa valeur correspond au résultat de la multiplication de 60 (le nombre de secondes dans une minute) par 60 (le nombre de minutes dans une heure), puis par 3 (le nombre d’heures que nous voulons compter dans ce programme). La convention de nommage de Rust pour les constantes consiste à utiliser uniquement des majuscules, avec des traits de soulignement entre les mots. Le compilateur peut évaluer un ensemble limité d’opérations à la compilation, ce qui nous permet de choisir d’écrire cette valeur d’une manière plus facile à comprendre et à vérifier, plutôt que de donner à cette constante la valeur 10 800. Consultez la [section du Rust Reference sur l’évaluation des constantes][const-eval] pour en savoir plus sur les opérations utilisables lors de la déclaration de constantes.

Les constantes restent valides pendant toute l’exécution d’un programme, dans la portée où elles ont été déclarées. Cette propriété rend les constantes utiles pour les valeurs de votre domaine d’application que plusieurs parties du programme pourraient devoir connaître, comme le nombre maximal de points qu’un joueur peut gagner dans un jeu ou la vitesse de la lumière.

Donner un nom sous forme de constante aux valeurs codées en dur utilisées dans tout votre programme permet d’en transmettre la signification aux futurs responsables de la maintenance du code. Cela permet également de n’avoir qu’un seul endroit dans le code à modifier si la valeur codée en dur doit être mise à jour ultérieurement.

### Masquage

Comme vous l’avez vu dans le tutoriel du jeu de devinettes au [chapitre 2][comparing-the-guess-to-the-secret-number]<!-- ignore -->, vous pouvez déclarer une nouvelle variable portant le même nom qu’une variable précédente. Les Rustacés disent que la première variable est _masquée_ par la seconde : cela signifie que, lorsque vous utilisez le nom de la variable, le compilateur voit la seconde variable. En pratique, la seconde variable prend le pas sur la première et récupère toutes les utilisations de ce nom, jusqu’à ce qu’elle soit elle-même masquée ou que la portée prenne fin. Nous pouvons masquer une variable en réutilisant son nom et en répétant le mot-clé `let`, comme suit :

<span class="filename">Fichier : src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-03-shadowing/src/main.rs}}
```

Ce programme associe d’abord à `x` la valeur `5`. Ensuite, il crée une nouvelle variable `x` en répétant `let x =`, reprend la valeur d’origine et lui ajoute `1`, de sorte que la valeur de `x` soit `6`. Puis, dans une portée interne créée avec les accolades, la troisième instruction `let` masque également `x` et crée une nouvelle variable, en multipliant la valeur précédente par `2` pour donner à `x` la valeur `12`. Lorsque cette portée prend fin, le masquage interne cesse et `x` reprend la valeur `6`. Lorsque nous exécutons ce programme, il affiche ce qui suit :

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-03-shadowing/output.txt}}
```

Le masquage diffère du fait de marquer une variable avec `mut`, car nous obtenons une erreur à la compilation si nous essayons accidentellement de réaffecter une valeur à cette variable sans utiliser le mot-clé `let`. En utilisant `let`, nous pouvons effectuer quelques transformations sur une valeur, puis laisser la variable immuable une fois ces transformations terminées.

L’autre différence entre `mut` et le masquage est que, puisque nous créons en réalité une nouvelle variable lorsque nous utilisons de nouveau le mot-clé `let`, nous pouvons changer le type de la valeur tout en réutilisant le même nom. Par exemple, supposons que notre programme demande à un utilisateur d’indiquer le nombre d’espaces qu’il souhaite entre des éléments de texte en saisissant des caractères espace, et que nous voulions ensuite stocker cette saisie sous forme de nombre :

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-04-shadowing-can-change-types/src/main.rs:here}}
```

La première variable `spaces` est de type chaîne de caractères, et la seconde variable `spaces` est de type numérique. Le masquage nous évite donc d’avoir à trouver des noms différents, comme `spaces_str` et `spaces_num` ; nous pouvons plutôt réutiliser le nom plus simple `spaces`. Toutefois, si nous essayons d’utiliser `mut` pour cela, comme le montre l’exemple suivant, nous obtiendrons une erreur à la compilation :

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-05-mut-cant-change-types/src/main.rs:here}}
```

L’erreur indique que nous ne sommes pas autorisés à modifier le type d’une variable :

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-05-mut-cant-change-types/output.txt}}
```

Maintenant que nous avons vu comment fonctionnent les variables, examinons d’autres types de données qu’elles peuvent avoir.

[comparing-the-guess-to-the-secret-number]: ch02-00-guessing-game-tutorial.html#comparing-the-guess-to-the-secret-number
[data-types]: ch03-02-data-types.html#data-types
[storing-values-with-variables]: ch02-00-guessing-game-tutorial.html#storing-values-with-variables
[const-eval]: ../reference/const_eval.html