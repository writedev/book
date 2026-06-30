## Fonctions

Les fonctions sont courantes dans le code Rust. Vous avez déjà vu l'une des fonctions les plus importantes du langage : la fonction `main`, qui est le point d'entrée de nombreux programmes. Vous avez également vu le mot-clé `fn`, qui vous permet de déclarer de nouvelles fonctions.

Le code Rust utilise le _snake case_ comme style conventionnel pour les noms de fonctions et de variables, où toutes les lettres sont minuscules et des underscores séparent les mots. Voici un programme contenant un exemple de définition de fonction :

<span class="filename">Nom du fichier : src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-16-functions/src/main.rs}}
```

Nous définissons une fonction en Rust en entrant `fn` suivi d'un nom de fonction et d'une parenthèse. Les accolades indiquent au compilateur où commence et se termine le corps de la fonction.

Nous pouvons appeler n'importe quelle fonction que nous avons définie en entrant son nom suivi d'une parenthèse. Parce que `another_function` est défini dans le programme, il peut être appelé depuis l'intérieur de la fonction `main`. Notez que nous avons défini `another_function` _après_ la fonction `main` dans le code source ; nous aurions également pu le définir avant. Rust ne se préoccupe pas de l'endroit où vous définissez vos fonctions, seulement qu'elles soient définies quelque part dans un contexte visible par l'appelant.

Commençons un nouveau projet binaire nommé _functions_ pour explorer les fonctions plus en détail. Placez l'exemple `another_function` dans _src/main.rs_ et exécutez-le. Vous devriez voir la sortie suivante :

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-16-functions/output.txt}}
```

Les lignes s'exécutent dans l'ordre dans lequel elles apparaissent dans la fonction `main`. D'abord, le message "Hello, world!" est imprimé, puis `another_function` est appelé et son message est imprimé.

### Paramètres

Nous pouvons définir des fonctions pour avoir des _paramètres_, qui sont des variables spéciales faisant partie de la signature d'une fonction. Lorsqu'une fonction a des paramètres, vous pouvez lui fournir des valeurs concrètes pour ces paramètres. Techniquement, les valeurs concrètes sont appelées _arguments_, mais dans une conversation informelle, les gens ont tendance à utiliser les mots _paramètre_ et _argument_ de manière interchangeable pour désigner soit les variables dans la définition d'une fonction, soit les valeurs concrètes passées lors de l'appel d'une fonction.

Dans cette version de `another_function`, nous ajoutons un paramètre :

<span class="filename">Nom du fichier : src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-17-functions-with-parameters/src/main.rs}}
```

Essayez d'exécuter ce programme ; vous devriez obtenir la sortie suivante :

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-17-functions-with-parameters/output.txt}}
```

La déclaration de `another_function` a un paramètre nommé `x`. Le type de `x` est spécifié comme `i32`. Lorsque nous passons `5` à `another_function`, le macro `println!` place `5` à l'endroit des accolades contenant `x` dans la chaîne de format.

Dans les signatures de fonction, vous _devez_ déclarer le type de chaque paramètre. C'est une décision délibérée dans la conception de Rust : exiger des annotations de type dans les définitions de fonction signifie que le compilateur a presque jamais besoin de vous les demander ailleurs dans le code pour comprendre quel type vous entendez. Le compilateur peut également fournir des messages d'erreur plus utiles s'il sait quels types la fonction attend.

Lorsque vous définissez plusieurs paramètres, séparez les déclarations de paramètres par des virgules, comme ceci :

<span class="filename">Nom du fichier : src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-18-functions-with-multiple-parameters/src/main.rs}}
```

Cet exemple crée une fonction nommée `print_labeled_measurement` avec deux paramètres. Le premier paramètre est nommé `value` et est de type `i32`. Le second est nommé `unit_label` et est de type `char`. La fonction imprime ensuite un texte contenant à la fois le `value` et le `unit_label`.

Essayons d'exécuter ce code. Remplacez le programme actuellement dans le fichier _src/main.rs_ de votre projet _functions_ par l'exemple précédent et exécutez-le en utilisant `cargo run` :

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-18-functions-with-multiple-parameters/output.txt}}
```

Puisque nous avons appelé la fonction avec `5` comme valeur pour `value` et `'h'` comme valeur pour `unit_label`, la sortie du programme contient ces valeurs.

### Instructions et expressions

Les corps des fonctions sont composés d'une série d'instructions se terminant éventuellement par une expression. Jusqu'à présent, les fonctions que nous avons couvertes n'ont pas inclus de dernière expression, mais vous avez vu une expression dans le cadre d'une instruction. Parce que Rust est un langage basé sur les expressions, il est important de comprendre cette distinction. D'autres langages n'ont pas les mêmes distinctions, alors examinons ce que sont les instructions et les expressions et comment leurs différences affectent les corps des fonctions.

- Les _instructions_ sont des instructions qui effectuent une action et ne retournent pas une valeur.
- Les _expressions_ évaluent à une valeur résultante.

Examinons quelques exemples.

Nous avons déjà utilisé des instructions et des expressions. Créer une variable et lui assigner une valeur avec le mot-clé `let` est une instruction. Dans la Liste 3-1, `let y = 6;` est une instruction.

<Listing number="3-1" file-name="src/main.rs" caption="Une déclaration de fonction `main` contenant une instruction">

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/listing-03-01/src/main.rs}}
```

</Listing>

Les définitions de fonction sont également des instructions ; tout l'exemple précédent est une instruction en soi. (Comme nous le verrons bientôt, appeler une fonction n'est pas une instruction, cependant.)

Les instructions ne retournent pas de valeurs. Par conséquent, vous ne pouvez pas assigner une instruction `let` à une autre variable, comme le code suivant tente de le faire ; vous obtiendrez une erreur :

<span class="filename">Nom du fichier : src/main.rs</span>

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-19-statements-vs-expressions/src/main.rs}}
```

Lorsque vous exécutez ce programme, l'erreur que vous obtiendrez ressemble à ceci :

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-19-statements-vs-expressions/output.txt}}
```

L'instruction `let y = 6` ne retourne pas de valeur, donc il n'y a rien à lier à `x`. Cela diffère de ce qui se passe dans d'autres langages, comme C et Ruby, où l'affectation retourne la valeur de l'affectation. Dans ces langages, vous pouvez écrire `x = y = 6` et avoir à la fois `x` et `y` ayant la valeur `6` ; ce n'est pas le cas en Rust.

Les expressions évaluent une valeur et constituent la majorité du reste du code que vous écrirez en Rust. Considérez une opération mathématique, telle que `5 + 6`, qui est une expression qui évalue à la valeur `11`. Les expressions peuvent faire partie d'instructions : Dans la Liste 3-1, le `6` dans l'instruction `let y = 6;` est une expression qui évalue à la valeur `6`. Appeler une fonction est une expression. Appeler un macro est une expression. Un nouveau bloc de portée créé avec des accolades est une expression, par exemple :

<span class="filename">Nom du fichier : src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-20-blocks-are-expressions/src/main.rs}}
```

Cette expression :

```rust,ignore
{
    let x = 3;
    x + 1
}
```

est un bloc qui, dans ce cas, évalue à `4`. Cette valeur est liée à `y` dans le cadre de l'instruction `let`. Notez la ligne `x + 1` sans point-virgule à la fin, ce qui est différent de la plupart des lignes que vous avez vues jusqu'à présent. Les expressions n'incluent pas de points-virgules finaux. Si vous ajoutez un point-virgule à la fin d'une expression, vous la transformez en instruction, et elle ne retournera alors pas de valeur. Gardez cela à l'esprit alors que vous explorez les valeurs de retour des fonctions et les expressions par la suite.

### Fonctions avec valeurs de retour

Les fonctions peuvent renvoyer des valeurs au code qui les appelle. Nous ne nommons pas les valeurs de retour, mais nous devons déclarer leur type après une flèche (`->`). En Rust, la valeur de retour de la fonction est synonyme de la valeur de la dernière expression dans le bloc du corps d'une fonction. Vous pouvez retourner quelque chose précocement d'une fonction en utilisant le mot-clé `return` et en spécifiant une valeur, mais la plupart des fonctions retournent la dernière expression implicitement. Voici un exemple d'une fonction qui renvoie une valeur :

<span class="filename">Nom du fichier : src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-21-function-return-values/src/main.rs}}
```

Il n'y a pas d'appels de fonctions, de macros, ni même d'instructions `let` dans la fonction `five`—juste le nombre `5` tout seul. C'est une fonction parfaitement valide en Rust. Notez que le type de retour de la fonction est également spécifié, comme `-> i32`. Essayez d'exécuter ce code ; la sortie devrait ressembler à ceci :

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-21-function-return-values/output.txt}}
```

Le `5` dans `five` est la valeur de retour de la fonction, c'est pourquoi le type de retour est `i32`. Examinons cela plus en détail. Il y a deux points importants : Premièrement, la ligne `let x = five();` montre que nous utilisons la valeur de retour d'une fonction pour initialiser une variable. Puisque la fonction `five` retourne un `5`, cette ligne est la même que :

```rust
let x = 5;
```

Deuxièmement, la fonction `five` n'a pas de paramètres et définit le type de la valeur de retour, mais le corps de la fonction est un `5` isolé sans point-virgule car c'est une expression dont nous voulons retourner la valeur.

Regardons un autre exemple :

<span class="filename">Nom du fichier : src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-22-function-parameter-and-return/src/main.rs}}
```

Exécuter ce code imprimera `La valeur de x est : 6`. Mais que se passe-t-il si nous ajoutons un point-virgule à la fin de la ligne contenant `x + 1`, la transformant d'une expression à une instruction ?

<span class="filename">Nom du fichier : src/main.rs</span>

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-23-statements-dont-return-values/src/main.rs}}
```

La compilation de ce code produira une erreur, comme suit :

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-23-statements-dont-return-values/output.txt}}
```

Le message d'erreur principal, `types mismatched`, révèle le problème central de ce code. La définition de la fonction `plus_one` indique qu'elle retournera un `i32`, mais les instructions ne s'évaluent pas à une valeur, ce qui est exprimé par `()`, le type unité. Par conséquent, rien n'est retourné, ce qui contredit la définition de la fonction et entraîne une erreur. Dans cette sortie, Rust fournit un message pour éventuellement aider à rectifier ce problème : il suggère de retirer le point-virgule, ce qui corrigerait l'erreur.