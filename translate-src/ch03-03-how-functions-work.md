## Fonctions

Les fonctions sont très présentes dans le code Rust. Vous avez déjà vu l’une
des fonctions les plus importantes du langage : la fonction `main`, qui est le
point d’entrée de nombreux programmes. Vous avez également vu le mot-clé `fn`,
qui permet de déclarer de nouvelles fonctions.

Le code Rust utilise la _casse snake case_ comme convention pour les noms de
fonctions et de variables : toutes les lettres sont en minuscules et les mots
sont séparés par des traits de soulignement. Voici un programme qui contient un
exemple de définition de fonction :

<span class="filename">Nom de fichier : src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-16-functions/src/main.rs}}
```

En Rust, nous définissons une fonction en saisissant `fn`, suivi du nom de la
fonction et d’une paire de parenthèses. Les accolades indiquent au compilateur
où le corps de la fonction commence et se termine.

Nous pouvons appeler n’importe quelle fonction que nous avons définie en
saisissant son nom, suivi d’une paire de parenthèses. Comme `another_function`
est définie dans le programme, elle peut être appelée depuis la fonction
`main`. Notez que nous avons défini `another_function` _après_ la fonction
`main` dans le code source ; nous aurions tout aussi bien pu la définir avant.
Rust ne se soucie pas de l’endroit où vous définissez vos fonctions, mais
seulement du fait qu’elles soient définies quelque part dans une portée visible
par l’appelant.

Créons un nouveau projet binaire nommé _functions_ pour explorer plus en
détail les fonctions. Placez l’exemple `another_function` dans _src/main.rs_ et
exécutez-le. Vous devriez voir le résultat suivant :

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-16-functions/output.txt}}
```

Les lignes s’exécutent dans l’ordre où elles apparaissent dans la fonction
`main`. Le message « Hello, world! » s’affiche d’abord, puis
`another_function` est appelée et son message s’affiche.

### Paramètres

Nous pouvons définir des fonctions avec des _paramètres_, qui sont des
variables particulières faisant partie de la signature d’une fonction.
Lorsqu’une fonction possède des paramètres, vous pouvez lui fournir des valeurs
concrètes pour ces paramètres. Techniquement, ces valeurs concrètes sont
appelées des _arguments_, mais dans les conversations courantes, on utilise
souvent les mots _paramètre_ et _argument_ de manière interchangeable, qu’il
s’agisse des variables dans la définition d’une fonction ou des valeurs
concrètes passées lors de l’appel de cette fonction.

Dans cette version de `another_function`, nous ajoutons un paramètre :

<span class="filename">Nom de fichier : src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-17-functions-with-parameters/src/main.rs}}
```

Essayez d’exécuter ce programme ; vous devriez obtenir le résultat suivant :

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-17-functions-with-parameters/output.txt}}
```

La déclaration de `another_function` comporte un paramètre nommé `x`. Le type
de `x` est spécifié comme étant `i32`. Lorsque nous passons `5` à
`another_function`, la macro `println!` place `5` à l’endroit des accolades
contenant `x` dans la chaîne de formatage.

Dans les signatures de fonction, vous _devez_ déclarer le type de chaque
paramètre. C’est un choix délibéré dans la conception de Rust : exiger des
annotations de type dans les définitions de fonction signifie que le
compilateur n’a presque jamais besoin que vous les utilisiez ailleurs dans le
code pour déterminer le type voulu. Le compilateur peut également fournir des
messages d’erreur plus utiles s’il connaît les types attendus par la fonction.

Lorsque vous définissez plusieurs paramètres, séparez leurs déclarations par
des virgules, comme ceci :

<span class="filename">Nom de fichier : src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-18-functions-with-multiple-parameters/src/main.rs}}
```

Cet exemple crée une fonction nommée `print_labeled_measurement` avec deux
paramètres. Le premier paramètre se nomme `value` et est de type `i32`. Le
second se nomme `unit_label` et est de type `char`. La fonction affiche ensuite
un texte contenant à la fois `value` et `unit_label`.

Essayons d’exécuter ce code. Remplacez le programme actuellement présent dans
le fichier _src/main.rs_ de votre projet _functions_ par l’exemple précédent,
puis exécutez-le avec `cargo run` :

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-18-functions-with-multiple-parameters/output.txt}}
```

Comme nous avons appelé la fonction avec `5` comme valeur de `value` et `'h'`
comme valeur de `unit_label`, ces valeurs apparaissent dans le résultat du
programme.

### Instructions et expressions

Les corps de fonction sont constitués d’une série d’instructions, éventuellement
suivies d’une expression finale. Jusqu’ici, les fonctions que nous avons
étudiées ne comportaient pas d’expression finale, mais vous avez déjà vu une
expression faire partie d’une instruction. Comme Rust est un langage fondé sur
les expressions, il est important de comprendre cette distinction. D’autres
langages ne font pas la même distinction ; examinons donc ce que sont les
instructions et les expressions, ainsi que la manière dont leurs différences
influent sur les corps de fonction.

- Les _instructions_ sont des opérations qui effectuent une action et ne
  renvoient aucune valeur.
- Les _expressions_ s’évaluent en une valeur résultante.

Examinons quelques exemples.

Nous avons en fait déjà utilisé des instructions et des expressions. Créer une
variable et lui assigner une valeur à l’aide du mot-clé `let` constitue une
instruction. Dans le listing 3-1, `let y = 6;` est une instruction.

<Listing number="3-1" file-name="src/main.rs" caption="Une déclaration de fonction `main` contenant une instruction">

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/listing-03-01/src/main.rs}}
```

</Listing>

Les définitions de fonction sont également des instructions ; l’exemple
précédent dans son ensemble est lui-même une instruction. (Comme nous le
verrons bientôt, appeler une fonction n’est toutefois pas une instruction.)

Les instructions ne renvoient aucune valeur. Par conséquent, vous ne pouvez pas
assigner une instruction `let` à une autre variable, comme le tente le code
suivant ; vous obtiendrez une erreur :

<span class="filename">Nom de fichier : src/main.rs</span>

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-19-statements-vs-expressions/src/main.rs}}
```

Lorsque vous exécutez ce programme, l’erreur obtenue ressemble à ceci :

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-19-statements-vs-expressions/output.txt}}
```

L’instruction `let y = 6` ne renvoie aucune valeur ; il n’y a donc rien que
`x` puisse recevoir. C’est différent de ce qui se passe dans d’autres langages,
comme C et Ruby, où une assignation renvoie la valeur assignée. Dans ces
langages, vous pouvez écrire `x = y = 6` et obtenir la valeur `6` pour `x` et
`y` ; ce n’est pas le cas en Rust.

Les expressions s’évaluent en une valeur et constituent la majeure partie du
reste du code que vous écrirez en Rust. Prenons une opération mathématique,
telle que `5 + 6`, qui est une expression s’évaluant en la valeur `11`. Les
expressions peuvent faire partie d’instructions : dans le listing 3-1, le `6`
de l’instruction `let y = 6;` est une expression qui s’évalue en la valeur
`6`. L’appel d’une fonction est une expression. L’appel d’une macro est une
expression. Un nouveau bloc de portée créé avec des accolades est une
expression, par exemple :

<span class="filename">Nom de fichier : src/main.rs</span>

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

est un bloc qui, dans ce cas, s’évalue en `4`. Cette valeur est assignée à `y`
dans le cadre de l’instruction `let`. Notez la ligne `x + 1`, qui ne se
termine pas par un point-virgule, contrairement à la plupart des lignes vues
jusqu’ici. Les expressions ne se terminent pas par un point-virgule. Si vous
ajoutez un point-virgule à la fin d’une expression, vous la transformez en
instruction, qui ne renvoie alors aucune valeur. Gardez cela à l’esprit pour
la suite, lorsque nous étudierons les valeurs de retour des fonctions et les
expressions.

### Fonctions avec des valeurs de retour

Les fonctions peuvent renvoyer des valeurs au code qui les appelle. Nous ne
nommons pas les valeurs de retour, mais nous devons en déclarer le type après
une flèche (`->`). En Rust, la valeur de retour d’une fonction correspond à la
valeur de la dernière expression du bloc constituant son corps. Vous pouvez
quitter une fonction plus tôt à l’aide du mot-clé `return` et en indiquant une
valeur, mais la plupart des fonctions renvoient implicitement leur dernière
expression. Voici un exemple de fonction qui renvoie une valeur :

<span class="filename">Nom de fichier : src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-21-function-return-values/src/main.rs}}
```

La fonction `five` ne contient aucun appel de fonction, aucune macro ni même
d’instruction `let` : seulement le nombre `5`. C’est une fonction tout à fait
valide en Rust. Notez que le type de retour de la fonction est également
spécifié, sous la forme `-> i32`. Essayez d’exécuter ce code ; le résultat
devrait ressembler à ceci :

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-21-function-return-values/output.txt}}
```

Le `5` de `five` est la valeur de retour de la fonction, ce qui explique
pourquoi son type de retour est `i32`. Examinons cela plus en détail. Il y a
deux éléments importants : premièrement, la ligne `let x = five();` montre que
nous utilisons la valeur de retour d’une fonction pour initialiser une
variable. Comme la fonction `five` renvoie `5`, cette ligne équivaut à :

```rust
let x = 5;
```

Deuxièmement, la fonction `five` ne prend aucun paramètre et définit le type de
la valeur de retour, mais son corps contient simplement un `5` sans
point-virgule, car il s’agit d’une expression dont nous voulons renvoyer la
valeur.

Examinons un autre exemple :

<span class="filename">Nom de fichier : src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-22-function-parameter-and-return/src/main.rs}}
```

L’exécution de ce code affichera `The value of x is: 6`. Mais que se passe-t-il
si nous plaçons un point-virgule à la fin de la ligne contenant `x + 1`, la
transformant ainsi d’une expression en une instruction ?

<span class="filename">Nom de fichier : src/main.rs</span>

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-23-statements-dont-return-values/src/main.rs}}
```

La compilation de ce code produira une erreur, comme suit :

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-23-statements-dont-return-values/output.txt}}
```

Le principal message d’erreur, `mismatched types`, révèle le problème
fondamental de ce code. La définition de la fonction `plus_one` indique qu’elle
renverra un `i32`, mais les instructions ne s’évaluent pas en une valeur, ce
qui est représenté par `()`, le type unité. Par conséquent, rien n’est renvoyé,
ce qui contredit la définition de la fonction et provoque une erreur. Dans ce
résultat, Rust propose une piste pour éventuellement résoudre le problème : il
suggère de supprimer le point-virgule, ce qui corrigerait l’erreur.