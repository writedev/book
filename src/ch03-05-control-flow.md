## Flux de Contrôle

La capacité d'exécuter du code selon qu'une condition est `vraie` et la capacité d'exécuter du code de manière répétée tant qu'une condition est `vraie` sont des éléments fondamentaux dans la plupart des langages de programmation. Les constructions les plus courantes qui vous permettent de contrôler le flux d'exécution du code Rust sont les expressions `if` et les boucles.

### Expressions `if`

Une expression `if` vous permet de ramifier votre code en fonction de conditions. Vous fournissez une condition puis indiquez : "Si cette condition est remplie, exécutez ce bloc de code. Si la condition n'est pas remplie, n'exécutez pas ce bloc de code."

Créez un nouveau projet appelé _branches_ dans votre répertoire _projects_ pour explorer l'expression `if`. Dans le fichier _src/main.rs_, saisissez ce qui suit :

<span class="filename">Nom de fichier : src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-26-if-true/src/main.rs}}
```

Toutes les expressions `if` commencent par le mot-clé `if`, suivi d'une condition. Dans ce cas, la condition vérifie si la variable `number` a une valeur inférieure à 5. Nous plaçons le bloc de code à exécuter si la condition est `vraie` immédiatement après la condition, à l'intérieur des accolades. Les blocs de code associés aux conditions dans les expressions `if` sont parfois appelés _bras_, tout comme les bras dans les expressions `match` que nous avons discutées dans la section [« Comparer le Guess au Secret Number »](comparing-the-guess-to-the-secret-number) du Chapitre 2.

Optionnellement, nous pouvons également inclure une expression `else`, ce que nous avons choisi de faire ici, pour donner au programme un bloc de code alternatif à exécuter si la condition évalue à `fausse`. Si vous ne fournissez pas d’expression `else` et que la condition est `fausse`, le programme ignorera simplement le bloc `if` et passera à la partie suivante du code.

Essayez d'exécuter ce code ; vous devriez voir la sortie suivante :

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-26-if-true/output.txt}}
```

Essayons de changer la valeur de `number` pour une valeur qui rend la condition `fausse` pour voir ce qui se passe :

```rust,ignore
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-27-if-false/src/main.rs:here}}
```

Exécutez à nouveau le programme et regardez la sortie :

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-27-if-false/output.txt}}
```

Il convient également de noter que la condition dans ce code _doit_ être un `bool`. Si la condition n'est pas un `bool`, nous obtiendrons une erreur. Par exemple, essayez d'exécuter le code suivant :

<span class="filename">Nom de fichier : src/main.rs</span>

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-28-if-condition-must-be-bool/src/main.rs}}
```

La condition `if` évalue cette fois à une valeur de `3`, et Rust lance une erreur :

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-28-if-condition-must-be-bool/output.txt}}
```

L'erreur indique que Rust s'attendait à un `bool`, mais a obtenu un entier. Contrairement à des langages tels que Ruby et JavaScript, Rust ne tentera pas automatiquement de convertir des types non-Booléens en Booléens. Vous devez être explicite et toujours fournir un Booléen comme condition pour `if`. Si nous voulons que le bloc de code `if` s'exécute uniquement lorsqu'un nombre n'est pas égal à `0`, par exemple, nous pouvons changer l'expression `if` comme suit :

<span class="filename">Nom de fichier : src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-29-if-not-equal-0/src/main.rs}}
```

L'exécution de ce code affichera `number was something other than zero`.

#### Gestion de Conditions Multiples avec `else if`

Vous pouvez utiliser plusieurs conditions en combinant `if` et `else` dans une expression `else if`. Par exemple :

<span class="filename">Nom de fichier : src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-30-else-if/src/main.rs}}
```

Ce programme peut suivre quatre chemins possibles. Après l'avoir exécuté, vous devriez voir la sortie suivante :

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-30-else-if/output.txt}}
```

Lorsque ce programme s'exécute, il vérifie chaque expression `if` à tour de rôle et exécute le premier corps pour lequel la condition évalue à `vraie`. Notez que même si 6 est divisible par 2, nous ne voyons pas le message `number is divisible by 2`, ni le texte `number is not divisible by 4, 3, or 2` provenant du bloc `else`. Cela est dû au fait que Rust n'exécute que le bloc pour la première condition `vraie`, et une fois qu'il en trouve une, il ne vérifie même pas les autres.

Utiliser trop d'expressions `else if` peut encombrer votre code, donc si vous en avez plus d'une, vous pourriez envisager de refactoriser votre code. Le Chapitre 6 décrit une construction de branchement puissante en Rust appelée `match` pour ces cas.

#### Utiliser `if` dans une Instruction `let`

Étant donné que `if` est une expression, nous pouvons l'utiliser sur le côté droit d'une instruction `let` pour assigner le résultat à une variable, comme dans l'Listing 3-2.

<Listing number="3-2" file-name="src/main.rs" caption="Affecter le résultat d'une expression `if` à une variable">

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/listing-03-02/src/main.rs}}
```

</Listing>

La variable `number` sera liée à une valeur basée sur le résultat de l'expression `if`. Exécutez ce code pour voir ce qui se passe :

```console
{{#include ../listings/ch03-common-programming-concepts/listing-03-02/output.txt}}
```

Rappelez-vous que les blocs de code évaluent la dernière expression en eux, et les nombres par eux-mêmes sont également des expressions. Dans ce cas, la valeur de l'ensemble de l'expression `if` dépend de quel bloc de code est exécuté. Cela signifie que les valeurs susceptibles d'être les résultats de chaque bras de l'`if` doivent être du même type ; dans l'Listing 3-2, les résultats des bras `if` et `else` étaient des entiers `i32`. Si les types ne correspondent pas, comme dans l'exemple suivant, nous obtiendrons une erreur :

<span class="filename">Nom de fichier : src/main.rs</span>

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-31-arms-must-return-same-type/src/main.rs}}
```

Lorsque nous essayons de compiler ce code, nous obtiendrons une erreur. Les bras `if` et `else` ont des types de valeur qui sont incompatibles, et Rust indique exactement où trouver le problème dans le programme :

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-31-arms-must-return-same-type/output.txt}}
```

L'expression dans le bloc `if` évalue à un entier, et l'expression dans le bloc `else` évalue à une chaîne. Cela ne fonctionnera pas, car les variables doivent avoir un type unique, et Rust doit connaître de manière définitive à la compilation quel type est la variable `number`. Savoir le type de `number` permet au compilateur de vérifier que le type est valide partout où nous utilisons `number`. Rust ne pourrait pas faire cela si le type de `number` était seulement déterminé à l'exécution ; le compilateur serait plus complexe et ferait moins de garanties sur le code s'il devait suivre plusieurs types hypothétiques pour n'importe quelle variable.

### Répétition avec des Boucles

Il est souvent utile d'exécuter un bloc de code plus d'une fois. Pour cette tâche, Rust fournit plusieurs _boucles_, qui exécuteront le code à l'intérieur du corps de la boucle jusqu'à la fin, puis recommenceront immédiatement depuis le début. Pour expérimenter avec des boucles, faisons un nouveau projet appelé _loops_.

Rust a trois types de boucles : `loop`, `while` et `for`. Essayons chacune d'elles.

#### Répéter du Code avec `loop`

Le mot-clé `loop` indique à Rust d'exécuter un bloc de code encore et encore, soit indéfiniment, soit jusqu'à ce que vous lui disiez explicitement de s'arrêter.

Par exemple, changez le fichier _src/main.rs_ dans votre répertoire _loops_ pour qu'il ressemble à ceci :

<span class="filename">Nom de fichier : src/main.rs</span>

```rust,ignore
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-32-loop/src/main.rs}}
```

Lorsque nous exécutons ce programme, nous verrons `again!` imprimer encore et encore en continu jusqu'à ce que nous arrêtions le programme manuellement. La plupart des terminaux prennent en charge le raccourci clavier <kbd>ctrl</kbd>-<kbd>C</kbd> pour interrompre un programme qui est bloqué dans une boucle continue. Essayez-le :

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

Le symbole `^C` représente l'endroit où vous avez appuyé sur <kbd>ctrl</kbd>-<kbd>C</kbd>.

Vous pouvez ou non voir le mot `again!` imprimé après le `^C`, en fonction de l'endroit où se trouvait le code dans la boucle lorsqu'il a reçu le signal d'interruption.

Heureusement, Rust fournit également un moyen de sortir d'une boucle par code. Vous pouvez placer le mot clé `break` à l'intérieur de la boucle pour indiquer au programme quand il doit arrêter d'exécuter la boucle. Rappelez-vous que nous avons fait cela dans le jeu de devinettes dans la section [« Quitter après une bonne devinette »](quitting-after-a-correct-guess) du Chapitre 2 pour quitter le programme lorsque l'utilisateur a gagné le jeu en devinant le bon nombre.

Nous avons également utilisé `continue` dans le jeu de devinettes, qui dans une boucle indique au programme de sauter tout code restant dans cette itération de la boucle et de passer à l'itération suivante.

#### Retourner des Valeurs depuis des Boucles

Une des utilisations d'une `loop` est de réessayer une opération que vous savez pourrait échouer, comme vérifier si un thread a terminé son travail. Vous pourriez également avoir besoin de passer le résultat de cette opération en dehors de la boucle vers le reste de votre code. Pour ce faire, vous pouvez ajouter la valeur que vous souhaitez retourner après l'expression `break` que vous utilisez pour arrêter la boucle ; cette valeur sera renvoyée en dehors de la boucle pour que vous puissiez l'utiliser, comme montré ici :

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-33-return-value-from-loop/src/main.rs}}
```

Avant la boucle, nous déclarons une variable nommée `counter` et l'initialisons à `0`. Puis, nous déclarons une variable nommée `result` pour contenir la valeur retournée par la boucle. À chaque itération de la boucle, nous ajoutons `1` à la variable `counter`, puis vérifions si `counter` est égal à `10`. Lorsqu'il l'est, nous utilisons le mot clé `break` avec la valeur `counter * 2`. Après la boucle, nous utilisons un point-virgule pour terminer l'instruction qui affecte la valeur à `result`. Enfin, nous imprimons la valeur dans `result`, qui dans ce cas est `20`.

Vous pouvez également `return` depuis l'intérieur d'une boucle. Alors que `break` quitte seulement la boucle courante, `return` quitte toujours la fonction courante.

#### Disambiguïser avec des Étiquettes de Boucle

Si vous avez des boucles imbriquées, `break` et `continue` s'appliquent à la boucle la plus intérieure à ce moment là. Vous pouvez optionnellement spécifier une _étiquette de boucle_ sur une boucle que vous pouvez ensuite utiliser avec `break` ou `continue` pour indiquer que ces mots clés s'appliquent à la boucle étiquetée au lieu de la boucle la plus intérieure. Les étiquettes de boucle doivent commencer par une simple apostrophe. Voici un exemple avec deux boucles imbriquées :

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-32-5-loop-labels/src/main.rs}}
```

La boucle extérieure a l'étiquette `'counting_up`, et elle comptera de 0 à 2. La boucle intérieure sans étiquette compte de 10 à 9. Le premier `break` qui ne spécifie pas d'étiquette sortira seulement de la boucle intérieure. L'instruction `break 'counting_up;` sortira de la boucle extérieure. Ce code imprime :

```console
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-32-5-loop-labels/output.txt}}
```

#### Simplifier les Boucles Conditionnelles avec while

Un programme aura souvent besoin d'évaluer une condition au sein d'une boucle. Tant que la condition est `vraie`, la boucle s'exécute. Lorsque la condition n'est plus `vraie`, le programme appelle `break`, arrêtant la boucle. Il est possible de mettre en œuvre un comportement comme celui-ci en utilisant une combinaison de `loop`, `if`, `else` et `break` ; vous pourriez essayer cela maintenant dans un programme, si vous le souhaitez. Cependant, ce modèle est si courant que Rust a une construction de langage intégrée pour cela, appelée boucle `while`. Dans l'Listing 3-3, nous utilisons `while` pour boucler le programme trois fois, en comptant à rebours à chaque fois, puis, après la boucle, pour imprimer un message et quitter.

<Listing number="3-3" file-name="src/main.rs" caption="Utiliser une boucle `while` pour exécuter du code tant qu'une condition évalue à `vraie`">

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/listing-03-03/src/main.rs}}
```

</Listing>

Cette construction élimine beaucoup d'imbrication qui serait nécessaire si vous utilisiez `loop`, `if`, `else` et `break`, et elle est plus claire. Tant qu'une condition évalue à `vraie`, le code s'exécute ; sinon, il quitte la boucle.

#### Boucler à Travers une Collection avec `for`

Vous pouvez choisir d'utiliser la construction `while` pour boucler à travers les éléments d'une collection, comme un tableau. Par exemple, la boucle dans l'Listing 3-4 imprime chaque élément du tableau `a`.

<Listing number="3-4" file-name="src/main.rs" caption="Boucler à travers chaque élément d'une collection en utilisant une boucle `while`">

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/listing-03-04/src/main.rs}}
```

</Listing>

Ici, le code compte à travers les éléments du tableau. Il commence à l'index `0` et boucle jusqu'à atteindre l'index final du tableau (c'est-à-dire, lorsque `index < 5` n'est plus `vrai`). L'exécution de ce code affichera chaque élément dans le tableau :

```console
{{#include ../listings/ch03-common-programming-concepts/listing-03-04/output.txt}}
```

Tous les cinq valeurs du tableau apparaissent dans le terminal, comme prévu. Même si `index` atteindra une valeur de `5` à un moment donné, la boucle arrête d'exécuter avant d'essayer de récupérer une sixième valeur du tableau.

Cependant, cette approche est sujette aux erreurs ; nous pourrions provoquer une panique du programme si la valeur de l'index ou la condition de test est incorrecte. Par exemple, si vous changiez la définition du tableau `a` pour avoir quatre éléments mais oubliiez de mettre à jour la condition pour `while index < 4`, le code paniquerait. C'est aussi lent, car le compilateur ajoute un code d'exécution pour effectuer la vérification conditionnelle de savoir si l'index est dans les limites du tableau à chaque itération de la boucle.

Comme alternative plus concise, vous pouvez utiliser une boucle `for` et exécuter du code pour chaque élément d'une collection. Une boucle `for` ressemble au code dans l'Listing 3-5.

<Listing number="3-5" file-name="src/main.rs" caption="Boucler à travers chaque élément d'une collection en utilisant une boucle `for`">

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/listing-03-05/src/main.rs}}
```

</Listing>

Lorsque nous exécutons ce code, nous verrons la même sortie que dans l'Listing 3-4. Plus important encore, nous avons maintenant augmenté la sécurité du code et éliminé le risque de bogues pouvant résulter d'un dépassement de la fin du tableau ou de ne pas aller assez loin et sauter certains éléments. Le code machine généré à partir des boucles `for` peut également être plus efficace car l'index n'a pas besoin d'être comparé à la longueur du tableau à chaque itération.

Avec la boucle `for`, vous n'auriez pas besoin de vous souvenir de changer d'autres codes si vous changiez le nombre de valeurs dans le tableau, comme vous le feriez avec la méthode utilisée dans l'Listing 3-4.

La sécurité et la concision des boucles `for` en font la construction de boucle la plus couramment utilisée en Rust. Même dans les situations où vous souhaitez exécuter du code un certain nombre de fois, comme dans l'exemple de compte à rebours qui a utilisé une boucle `while` dans l'Listing 3-3, la plupart des Rustaces choisiraient une boucle `for`. La façon de le faire serait d'utiliser un `Range`, fourni par la bibliothèque standard, qui génère tous les nombres dans la séquence à partir d'un nombre et se termine avant un autre nombre.

Voici à quoi ressemblerait le compte à rebours en utilisant une boucle `for` et une autre méthode que nous n'avons pas encore abordée, `rev`, pour inverser la plage :

<span class="filename">Nom de fichier : src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-34-for-range/src/main.rs}}
```

Ce code est un peu plus agréable, n'est-ce pas ?

## Résumé

Vous y êtes arrivé ! C'était un chapitre conséquent : Vous avez appris sur les variables, les types de données scalaires et composés, les fonctions, les commentaires, les expressions `if`, et les boucles ! Pour pratiquer avec les concepts abordés dans ce chapitre, essayez de construire des programmes pour faire ce qui suit :

- Convertir des températures entre Fahrenheit et Celsius.
- Générer le *n*ième nombre de Fibonacci.
- Imprimer les paroles du chant de Noël « Les Douze Jours de Noël », en profitant de la répétition dans la chanson.

Lorsque vous serez prêt à passer à autre chose, nous parlerons d'un concept en Rust qui _n'existe pas_ couramment dans d'autres langages de programmation : l'appartenance.