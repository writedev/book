## Contrôle du flux

La possibilité d’exécuter du code en fonction du fait qu’une condition soit `true`, ainsi que celle de répéter du code tant qu’une condition est `true`, constituent des éléments de base dans la plupart des langages de programmation. Les constructions les plus courantes permettant de contrôler le flux d’exécution du code Rust sont les expressions `if` et les boucles.

### Expressions `if`

Une expression `if` permet de répartir le code en fonction de conditions. Vous fournissez une condition, puis indiquez : « Si cette condition est satisfaite, exécutez ce bloc de code. Si elle ne l’est pas, n’exécutez pas ce bloc de code. »

Créez un nouveau projet appelé _branches_ dans votre répertoire _projects_ pour explorer l’expression `if`. Dans le fichier _src/main.rs_, saisissez ce qui suit :

<span class="filename">Nom du fichier : src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-26-if-true/src/main.rs}}
```

Toutes les expressions `if` commencent par le mot-clé `if`, suivi d’une condition. Ici, la condition vérifie si la variable `number` a une valeur inférieure à 5. Nous plaçons le bloc de code à exécuter si la condition est `true` juste après la condition, entre accolades. Les blocs de code associés aux conditions dans les expressions `if` sont parfois appelés des _branches_, tout comme celles des expressions `match` dont nous avons parlé dans la section [« Comparer la supposition au nombre secret »][comparing-the-guess-to-the-secret-number]<!--
ignore --> du chapitre 2.

Nous pouvons également inclure une expression `else`, ce que nous avons choisi de faire ici, afin de fournir au programme un autre bloc de code à exécuter si la condition vaut `false`. Si vous ne fournissez pas d’expression `else` et que la condition vaut `false`, le programme ignore simplement le bloc `if` et passe à la suite du code.

Essayez d’exécuter ce code ; vous devriez obtenir la sortie suivante :

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-26-if-true/output.txt}}
```

Essayons de remplacer la valeur de `number` par une valeur qui rend la condition `false` pour voir ce qui se passe :

```rust,ignore
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-27-if-false/src/main.rs:here}}
```

Exécutez de nouveau le programme et observez la sortie :

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-27-if-false/output.txt}}
```

Il convient également de noter que la condition de ce code _doit_ être un `bool`. Si la condition n’est pas un `bool`, nous obtiendrons une erreur. Par exemple, essayez d’exécuter le code suivant :

<span class="filename">Nom du fichier : src/main.rs</span>

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-28-if-condition-must-be-bool/src/main.rs}}
```

Cette fois, la condition `if` donne la valeur `3`, et Rust renvoie une erreur :

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-28-if-condition-must-be-bool/output.txt}}
```

L’erreur indique que Rust attendait un `bool`, mais a obtenu un entier. Contrairement à des langages comme Ruby et JavaScript, Rust ne tente pas automatiquement de convertir les types non booléens en valeurs booléennes. Vous devez être explicite et toujours fournir un booléen comme condition à `if`. Par exemple, si nous voulons que le bloc de code `if` s’exécute uniquement lorsqu’un nombre n’est pas égal à `0`, nous pouvons remplacer l’expression `if` par ce qui suit :

<span class="filename">Nom du fichier : src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-29-if-not-equal-0/src/main.rs}}
```

L’exécution de ce code affichera `number was something other than zero`.

#### Gérer plusieurs conditions avec `else if`

Vous pouvez utiliser plusieurs conditions en combinant `if` et `else` dans une expression `else if`. Par exemple :

<span class="filename">Nom du fichier : src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-30-else-if/src/main.rs}}
```

Ce programme peut suivre quatre chemins différents. Après l’avoir exécuté, vous devriez obtenir la sortie suivante :

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-30-else-if/output.txt}}
```

Lors de l’exécution de ce programme, chaque expression `if` est vérifiée à tour de rôle, et le premier bloc dont la condition vaut `true` est exécuté. Notez que, même si 6 est divisible par 2, nous ne voyons pas la sortie `number is divisible by 2`, ni le texte `number is not divisible by 4, 3, or 2` du bloc `else`. En effet, Rust n’exécute que le bloc associé à la première condition qui vaut `true` et, dès qu’il en trouve une, il ne vérifie même pas les autres.

L’utilisation d’un trop grand nombre d’expressions `else if` peut encombrer votre code. Si vous en avez plusieurs, vous voudrez peut-être le remanier. Le chapitre 6 présente une puissante construction de branchement de Rust appelée `match`, qui convient à ces cas.

#### Utiliser `if` dans une instruction `let`

Comme `if` est une expression, nous pouvons l’utiliser à droite d’une instruction `let` pour affecter son résultat à une variable, comme dans la liste 3-2.

<Listing number="3-2" file-name="src/main.rs" caption="Affecter le résultat d’une expression `if` à une variable">

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/listing-03-02/src/main.rs}}
```

</Listing>

La variable `number` sera liée à une valeur en fonction du résultat de l’expression `if`. Exécutez ce code pour voir ce qui se passe :

```console
{{#include ../listings/ch03-common-programming-concepts/listing-03-02/output.txt}}
```

N’oubliez pas que les blocs de code évaluent leur dernière expression et que les nombres seuls sont également des expressions. Dans ce cas, la valeur de l’expression `if` entière dépend du bloc de code qui est exécuté. Cela signifie que les valeurs susceptibles d’être renvoyées par chaque branche de `if` doivent être du même type ; dans la liste 3-2, les résultats des branches `if` et `else` étaient tous deux des entiers `i32`. Si les types ne correspondent pas, comme dans l’exemple suivant, nous obtiendrons une erreur :

<span class="filename">Nom du fichier : src/main.rs</span>

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-31-arms-must-return-same-type/src/main.rs}}
```

Lorsque nous tenterons de compiler ce code, nous obtiendrons une erreur. Les branches `if` et `else` ont des types de valeur incompatibles, et Rust indique précisément où trouver le problème dans le programme :

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-31-arms-must-return-same-type/output.txt}}
```

L’expression du bloc `if` donne un entier, et celle du bloc `else` donne une chaîne de caractères. Cela ne fonctionnera pas, car les variables doivent avoir un type unique et Rust doit savoir avec certitude, à la compilation, quel est le type de la variable `number`. Connaître le type de `number` permet au compilateur de vérifier que ce type est valide partout où nous utilisons `number`. Rust ne pourrait pas le faire si le type de `number` n’était déterminé qu’à l’exécution ; le compilateur serait plus complexe et offrirait moins de garanties sur le code s’il devait suivre plusieurs types hypothétiques pour chaque variable.

### Répéter du code avec des boucles

Il est souvent utile d’exécuter un bloc de code plusieurs fois. Pour cela, Rust fournit plusieurs _boucles_, qui exécutent le code de leur corps jusqu’à la fin, puis reprennent immédiatement au début. Pour expérimenter avec les boucles, créons un nouveau projet appelé _loops_.

Rust propose trois types de boucles : `loop`, `while` et `for`. Essayons-les une à une.

#### Répéter du code avec `loop`

Le mot-clé `loop` indique à Rust d’exécuter un bloc de code en boucle, indéfiniment ou jusqu’à ce que vous lui indiquiez explicitement de s’arrêter.

Par exemple, modifiez le fichier _src/main.rs_ de votre répertoire _loops_ pour qu’il ressemble à ceci :

<span class="filename">Nom du fichier : src/main.rs</span>

```rust,ignore
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-32-loop/src/main.rs}}
```

Lorsque nous exécutons ce programme, `again!` s’affiche en continu jusqu’à ce que nous arrêtions le programme manuellement. La plupart des terminaux prennent en charge le raccourci clavier <kbd>ctrl</kbd>-<kbd>C</kbd> pour interrompre un programme coincé dans une boucle sans fin. Essayez :

<!-- manual-regeneration
cd listings/ch03-common-programming-concepts/no-listing-32-loop
cargo run
CTRL-C
-->

```console
$ cargo run
   Compiling loops v0.1.0 (file:///projects/loops)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.08s
     Running `target/debug/loops`
again!
again!
again!
again!
^Cagain!
```

Le symbole `^C` représente l’endroit où vous avez appuyé sur <kbd>ctrl</kbd>-<kbd>C</kbd>.

Le mot `again!` peut apparaître ou non après `^C`, selon l’endroit où se trouvait le code dans la boucle lorsqu’il a reçu le signal d’interruption.

Heureusement, Rust fournit également un moyen de sortir d’une boucle à l’aide du code. Vous pouvez placer le mot-clé `break` dans la boucle pour indiquer au programme quand arrêter son exécution. Rappelez-vous que nous l’avons utilisé dans le jeu de devinettes, dans la section [« Quitter après une bonne supposition »][quitting-after-a-correct-guess]<!-- ignore
--> du chapitre 2, pour quitter le programme lorsque l’utilisateur gagnait en devinant le bon nombre.

Nous avons également utilisé `continue` dans le jeu de devinettes. Dans une boucle, ce mot-clé indique au programme d’ignorer le reste du code de cette itération et de passer à l’itération suivante.

#### Renvoyer des valeurs depuis des boucles

L’une des utilisations de `loop` consiste à réessayer une opération susceptible d’échouer, comme vérifier si un thread a terminé son travail. Vous pouvez également avoir besoin de transmettre le résultat de cette opération au reste de votre code, en sortant de la boucle. Pour cela, vous pouvez ajouter la valeur que vous voulez renvoyer après l’expression `break` qui arrête la boucle ; cette valeur sera renvoyée par la boucle et pourra être utilisée, comme dans l’exemple suivant :

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-33-return-value-from-loop/src/main.rs}}
```

Avant la boucle, nous déclarons une variable nommée `counter` et l’initialisons à `0`. Puis nous déclarons une variable nommée `result` pour contenir la valeur renvoyée par la boucle. À chaque itération, nous ajoutons `1` à la variable `counter`, puis vérifions si `counter` est égal à `10`. Lorsque c’est le cas, nous utilisons le mot-clé `break` avec la valeur `counter * 2`. Après la boucle, nous utilisons un point-virgule pour terminer l’instruction qui affecte la valeur à `result`. Enfin, nous affichons la valeur de `result`, qui est ici `20`.

Vous pouvez également utiliser `return` à l’intérieur d’une boucle. Alors que `break` ne quitte que la boucle en cours, `return` quitte toujours la fonction en cours.

<!-- Old headings. Do not remove or links may break. -->
<a id="loop-labels-to-disambiguate-between-multiple-loops"></a>

#### Distinguer les boucles à l’aide d’étiquettes

Si vous imbriquez des boucles, `break` et `continue` s’appliquent à la boucle la plus interne à cet endroit. Vous pouvez, si vous le souhaitez, attribuer une _étiquette de boucle_ à une boucle, puis l’utiliser avec `break` ou `continue` pour indiquer que ces mots-clés s’appliquent à la boucle étiquetée plutôt qu’à la boucle la plus interne. Les étiquettes de boucle doivent commencer par une apostrophe. Voici un exemple avec deux boucles imbriquées :

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-32-5-loop-labels/src/main.rs}}
```

La boucle externe porte l’étiquette `'counting_up` et compte de 0 à 2. La boucle interne, sans étiquette, compte à rebours de 10 à 9. Le premier `break` qui ne précise pas d’étiquette ne quitte que la boucle interne. L’instruction `break
'counting_up;` quitte la boucle externe. Ce code affiche :

```console
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-32-5-loop-labels/output.txt}}
```

<!-- Old headings. Do not remove or links may break. -->
<a id="conditional-loops-with-while"></a>

#### Simplifier les boucles conditionnelles avec `while`

Un programme doit souvent évaluer une condition dans une boucle. Tant que la condition vaut `true`, la boucle s’exécute. Lorsque la condition cesse de valoir `true`, le programme appelle `break` pour arrêter la boucle. Il est possible d’implémenter ce comportement à l’aide d’une combinaison de `loop`, `if`, `else` et `break` ; vous pouvez essayer dès maintenant dans un programme, si vous le souhaitez. Toutefois, ce modèle est si courant que Rust possède une construction intégrée pour le mettre en œuvre : la boucle `while`. Dans la liste 3-3, nous utilisons `while` pour exécuter le programme trois fois, en comptant à rebours à chaque fois, puis, après la boucle, pour afficher un message et quitter.

<Listing number="3-3" file-name="src/main.rs" caption="Utiliser une boucle `while` pour exécuter du code tant qu’une condition vaut `true`">

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/listing-03-03/src/main.rs}}
```

</Listing>

Cette construction évite une grande partie de l’imbrication nécessaire avec `loop`, `if`, `else` et `break`, et rend le code plus clair. Tant qu’une condition vaut `true`, le code s’exécute ; sinon, la boucle se termine.

#### Parcourir une collection avec `for`

Vous pouvez choisir d’utiliser la construction `while` pour parcourir les éléments d’une collection, comme un tableau. Par exemple, la boucle de la liste 3-4 affiche chaque élément du tableau `a`.

<Listing number="3-4" file-name="src/main.rs" caption="Parcourir chaque élément d’une collection à l’aide d’une boucle `while`">

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/listing-03-04/src/main.rs}}
```

</Listing>

Ici, le code parcourt les éléments du tableau en comptant vers le haut. Il commence à l’indice `0`, puis boucle jusqu’à atteindre le dernier indice du tableau (c’est-à-dire jusqu’à ce que `index < 5` ne soit plus `true`). L’exécution de ce code affichera chaque élément du tableau :

```console
{{#include ../listings/ch03-common-programming-concepts/listing-03-04/output.txt}}
```

Les cinq valeurs du tableau apparaissent dans le terminal, comme prévu. Même si `index` atteint la valeur `5` à un moment donné, la boucle s’arrête avant d’essayer de récupérer une sixième valeur du tableau.

Cependant, cette approche est sujette aux erreurs ; nous pourrions provoquer une panique si la valeur de l’indice ou la condition de test est incorrecte. Par exemple, si vous modifiez la définition du tableau `a` pour qu’il contienne quatre éléments, mais oubliez de mettre à jour la condition `while index < 4`, le code provoquera une panique. Cette approche est également lente, car le compilateur ajoute du code à l’exécution pour vérifier, à chaque itération, si l’indice se trouve dans les limites du tableau.

Une solution plus concise consiste à utiliser une boucle `for` pour exécuter du code sur chaque élément d’une collection. Une boucle `for` ressemble au code de la liste 3-5.

<Listing number="3-5" file-name="src/main.rs" caption="Parcourir chaque élément d’une collection à l’aide d’une boucle `for`">

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/listing-03-05/src/main.rs}}
```

</Listing>

Lorsque nous exécuterons ce code, nous obtiendrons la même sortie que dans la liste 3-4. Plus important encore, nous avons rendu le code plus sûr et éliminé le risque de bogues susceptibles de survenir si l’on dépasse la fin du tableau ou si l’on ne va pas assez loin et que l’on omet certains éléments. Le code machine généré à partir des boucles `for` peut également être plus efficace, car l’indice n’a pas besoin d’être comparé à la longueur du tableau à chaque itération.

Avec une boucle `for`, vous n’auriez pas besoin de vous rappeler de modifier d’autres éléments du code si vous changiez le nombre de valeurs du tableau, contrairement à la méthode utilisée dans la liste 3-4.

La sécurité et la concision des boucles `for` en font la construction de boucle la plus couramment utilisée en Rust. Même lorsqu’il s’agit d’exécuter du code un nombre déterminé de fois, comme dans l’exemple du compte à rebours utilisant une boucle `while` dans la liste 3-3, la plupart des Rustacéens utiliseraient une boucle `for`. Pour cela, on peut utiliser une `Range`, fournie par la bibliothèque standard, qui génère une suite de nombres commençant par un nombre et s’arrêtant avant un autre nombre.

Voici à quoi ressemblerait le compte à rebours avec une boucle `for` et une autre méthode dont nous n’avons pas encore parlé, `rev`, qui inverse l’ordre de la plage :

<span class="filename">Nom du fichier : src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-34-for-range/src/main.rs}}
```

Ce code est un peu plus agréable, n’est-ce pas ?

## Résumé

Vous y êtes arrivé ! Ce chapitre était conséquent : vous avez découvert les variables, les types de données scalaires et composés, les fonctions, les commentaires, les expressions `if` et les boucles ! Pour mettre en pratique les concepts abordés dans ce chapitre, essayez de créer des programmes qui permettent de :

- Convertir des températures entre les degrés Fahrenheit et Celsius.
- Générer le *n*ᵉ nombre de Fibonacci.
- Afficher les paroles du chant de Noël « Les Douze Jours de Noël », en tirant parti des répétitions dans la chanson.

Lorsque vous serez prêt à continuer, nous parlerons d’un concept de Rust qui n’existe _pas_ couramment dans les autres langages de programmation : la propriété.

[comparing-the-guess-to-the-secret-number]: ch02-00-guessing-game-tutorial.html#comparing-the-guess-to-the-secret-number
[quitting-after-a-correct-guess]: ch02-00-guessing-game-tutorial.html#quitting-after-a-correct-guess