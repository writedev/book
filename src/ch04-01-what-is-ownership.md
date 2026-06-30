## Qu'est-ce que l'appartenance ?

_L'appartenance_ est un ensemble de règles qui régissent la manière dont un programme Rust gère la mémoire. Tous les programmes doivent gérer la façon dont ils utilisent la mémoire d'un ordinateur pendant leur exécution. Certains langages disposent d'une collecte de mémoire qui recherche régulièrement la mémoire inutilisée pendant l'exécution du programme ; dans d'autres langages, le programmeur doit explicitement allouer et libérer la mémoire. Rust utilise une troisième approche : la mémoire est gérée par un système d'appartenance avec un ensemble de règles que le compilateur vérifie. Si l'une des règles est violée, le programme ne se compile pas. Aucune des fonctionnalités d'appartenance ne ralentira votre programme pendant son exécution.

Comme l'appartenance est un concept nouveau pour de nombreux programmeurs, il faut un certain temps pour s'y habituer. La bonne nouvelle est que plus vous devenez expérimenté avec Rust et les règles du système d'appartenance, plus il vous sera facile de développer naturellement du code qui est sûr et efficace. Continuez comme ça !

Lorsque vous comprenez l'appartenance, vous aurez une base solide pour comprendre les caractéristiques qui rendent Rust unique. Dans ce chapitre, vous apprendrez l'appartenance en travaillant à travers des exemples qui se concentrent sur une structure de données très commune : les chaînes de caractères.

> ### La pile et le tas
>
> De nombreux langages de programmation ne vous obligent pas à penser à la pile et au tas très souvent. Mais dans un langage de programmation système comme Rust, que la valeur soit dans la pile ou dans le tas affecte le comportement du langage et pourquoi vous devez prendre certaines décisions. Des parties de l'appartenance seront décrites en relation avec la pile et le tas plus loin dans ce chapitre, donc voici une brève explication en préparation.
>
> La pile et le tas sont des parties de la mémoire disponibles pour votre code à utiliser à l'exécution, mais elles sont structurées de manières différentes. La pile stocke les valeurs dans l'ordre où elle les reçoit et les retire dans l'ordre inverse. Cela est appelé _dernier entré, premier sorti (LIFO)_. Pensez à une pile d'assiettes : lorsque vous ajoutez plus d'assiettes, vous les mettez sur le dessus de la pile, et lorsque vous avez besoin d'une assiette, vous en prenez une du dessus. Ajouter ou retirer des assiettes du milieu ou du bas ne fonctionnerait pas aussi bien ! Ajouter des données est appelé _ajouter à la pile_, et retirer des données est appelé _retirer de la pile_. Toutes les données stockées dans la pile doivent avoir une taille fixe et connue. Les données dont la taille est inconnue au moment de la compilation ou qui peuvent changer doivent être stockées dans le tas.
>
> Le tas est moins organisé : lorsque vous mettez des données dans le tas, vous demandez une certaine quantité d'espace. L'allocateur de mémoire trouve un endroit vide dans le tas qui est assez grand, le marque comme étant utilisé et renvoie un _pointeur_, qui est l'adresse de cet emplacement. Ce processus est appelé _allocation dans le tas_ et est parfois abrégé simplement en _allocation_ (pousser des valeurs sur la pile n'est pas considéré comme une allocation). Comme le pointeur vers le tas a une taille fixe et connue, vous pouvez stocker le pointeur dans la pile, mais lorsque vous voulez les données réelles, vous devez suivre le pointeur. Pensez à être assis dans un restaurant. Lorsque vous entrez, vous indiquez le nombre de personnes dans votre groupe, et l'hôte trouve une table vide qui peut accueillir tout le monde et vous y conduit. Si quelqu'un de votre groupe arrive en retard, il peut demander où vous êtes assis pour vous retrouver.
>
> Pousser sur la pile est plus rapide que d'allouer dans le tas, car l'allocateur n'a jamais à chercher un endroit pour stocker de nouvelles données ; cet emplacement est toujours en haut de la pile. En comparaison, allouer de l'espace dans le tas nécessite plus de travail car l'allocateur doit d'abord trouver un espace suffisamment grand pour contenir les données, puis effectuer des tâches administratives pour préparer la prochaine allocation.
>
> Accéder aux données dans le tas est généralement plus lent que d'accéder aux données dans la pile car vous devez suivre un pointeur pour y arriver. Les processeurs contemporains sont plus rapides s'ils sautent moins dans la mémoire. En continuant l'analogie, pensez à un serveur dans un restaurant prenant des commandes de plusieurs tables. Il est plus efficace de prendre toutes les commandes d'une table avant de passer à la table suivante. Prendre une commande de la table A, puis une commande de la table B, puis de nouveau une de A, puis de B à nouveau serait un processus beaucoup plus lent. De la même manière, un processeur peut généralement mieux faire son travail s'il traite des données proches d'autres données (comme cela l'est dans la pile) plutôt que plus éloignées (comme cela peut être dans le tas).
>
> Lorsque votre code appelle une fonction, les valeurs passées à la fonction (y compris, potentiellement, des pointeurs vers des données dans le tas) et les variables locales de la fonction sont ajoutées à la pile. Lorsque la fonction est terminée, ces valeurs sont retirées de la pile.
>
> Garder une trace des parties du code qui utilisent quelles données dans le tas, minimiser la quantité de données dupliquées dans le tas, et nettoyer les données inutilisées dans le tas afin de ne pas manquer d'espace sont tous des problèmes que l'appartenance résout. Une fois que vous comprendrez l'appartenance, vous n'aurez plus besoin de penser très souvent à la pile et au tas. Mais savoir que le principal objectif de l'appartenance est de gérer les données du tas peut aider à expliquer pourquoi cela fonctionne de la manière dont cela fonctionne.

### Règles d'appartenance

Tout d'abord, examinons les règles d'appartenance. Gardez ces règles à l'esprit alors que nous travaillerons à travers les exemples qui les illustrent :

- Chaque valeur en Rust a un _propriétaire_.
- Il ne peut y avoir qu'un seul propriétaire à la fois.
- Lorsque le propriétaire sort de la portée, la valeur sera supprimée.

### Portée des variables

Maintenant que nous avons passé la syntaxe de base de Rust, nous n'inclurons pas tout le code `fn main() {` dans les exemples, donc si vous suivez, assurez-vous de placer les exemples suivants dans une fonction `main` manuellement. Par conséquent, nos exemples seront un peu plus concis, nous permettant de nous concentrer sur les détails réels plutôt que sur le code standard.

Comme premier exemple d'appartenance, nous allons examiner la portée de certaines variables. Une _portée_ est l'étendue au sein d'un programme pour laquelle un élément est valide. Prenez la variable suivante :

```rust
let s = "hello";
```

La variable `s` fait référence à une chaîne littérale, où la valeur de la chaîne est codée en dur dans le texte de notre programme. La variable est valide depuis le moment où elle est déclarée jusqu'à la fin de la portée actuelle. La liste 4-1 montre un programme avec des commentaires annotant où la variable `s` serait valide.

<liste numéro="4-1" légende="Une variable et la portée dans laquelle elle est valide">

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/listing-04-01/src/main.rs:here}}
```

</liste>

Autrement dit, il y a deux points importants dans le temps ici :

- Lorsque `s` entre dans la portée, il est valide.
- Il reste valide jusqu'à ce qu'il sorte de la portée.

À ce stade, la relation entre les portées et la validité des variables est similaire à celle des autres langages de programmation. Maintenant, nous allons nous appuyer sur cette compréhension en introduisant le type `String`.

### Le type `String`

Pour illustrer les règles d'appartenance, nous avons besoin d'un type de données qui soit plus complexe que ceux que nous avons couverts dans la section [« Types de données »][data-types]<!-- ignore --> du chapitre 3. Les types précédemment couverts sont de taille connue, peuvent être stockés dans la pile et retirés de la pile lorsque leur portée est terminée, et peuvent être rapidement et trivialement copiés pour créer une nouvelle instance indépendante si une autre partie du code doit utiliser la même valeur dans une portée différente. Mais nous voulons examiner des données stockées dans le tas et explorer comment Rust sait quand nettoyer ces données, et le type `String` est un excellent exemple.

Nous nous concentrerons sur les parties de `String` qui se rapportent à l'appartenance. Ces aspects s'appliquent également à d'autres types de données complexes, qu'ils soient fournis par la bibliothèque standard ou créés par vous. Nous discuterons des aspects non liés à l'appartenance de `String` dans [Chapitre 8][ch8]<!-- ignore -->.

Nous avons déjà vu des chaînes littérales, où une valeur de chaîne est codée en dur dans notre programme. Les chaînes littérales sont pratiques, mais elles ne sont pas adaptées à toutes les situations où nous pouvons vouloir utiliser du texte. Une raison est qu'elles sont immuables. Une autre est que toutes les valeurs de chaîne ne peuvent pas être connues lorsque nous écrivons notre code : Par exemple, que se passe-t-il si nous voulons prendre une entrée utilisateur et la stocker ? C'est pour ces situations que Rust dispose du type `String`. Ce type gère les données allouées dans le tas et, en tant que tel, est capable de stocker une quantité de texte qui nous est inconnue au moment de la compilation. Vous pouvez créer un `String` à partir d'une chaîne littérale en utilisant la fonction `from`, comme ceci :

```rust
let s = String::from("hello");
```

L'opérateur double deux-points `::` nous permet de nommer cette fonction `from` particulière sous le type `String` plutôt que d'utiliser un nom comme `string_from`. Nous discuterons plus de cette syntaxe dans la section [« Méthodes »][methods]<!-- ignore --> du chapitre 5, et lorsque nous parlerons de nomination avec des modules dans [« Chemins pour se référer à un élément dans l'arbre de module »][paths-module-tree]<!-- ignore --> dans le chapitre 7.

Ce type de chaîne _peut_ être muté :

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-01-can-mutate-string/src/main.rs:here}}
```

Alors, quelle est la différence ici ? Pourquoi `String` peut-il être muté mais pas les littéraux ? La différence réside dans la façon dont ces deux types gèrent la mémoire.

### Mémoire et allocation

Dans le cas d'une chaîne littérale, nous connaissons le contenu au moment de la compilation, donc le texte est codé en dur directement dans l'exécutable final. C'est pourquoi les chaînes littérales sont rapides et efficaces. Mais ces propriétés découlent uniquement de l'immuabilité de la chaîne littérale. Malheureusement, nous ne pouvons pas mettre un bloc de mémoire dans le binaire pour chaque morceau de texte dont la taille est inconnue au moment de la compilation et dont la taille pourrait changer pendant l'exécution du programme.

Avec le type `String`, pour prendre en charge un morceau de texte mutable et extensible, nous devons allouer une quantité de mémoire dans le tas, inconnue au moment de la compilation, pour contenir le contenu. Cela signifie :

- La mémoire doit être demandée à l'allocateur de mémoire à l'exécution.
- Nous avons besoin d'un moyen de retourner cette mémoire à l'allocateur lorsque nous avons terminé avec notre `String`.

Cette première partie est effectuée par nous : Lorsque nous appelons `String::from`, son implémentation demande la mémoire dont elle a besoin. C'est à peu près universel dans les langages de programmation.

Cependant, la deuxième partie est différente. Dans les langages avec un _collecteur de déchets (GC)_, le GC suit et nettoie la mémoire qui n'est plus utilisée, et nous n'avons pas à y penser. Dans la plupart des langages sans GC, c'est à nous de déterminer quand la mémoire n'est plus utilisée et d'appeler du code pour la libérer explicitement, tout comme nous l'avons fait pour la demander. Faire cela correctement a historiquement été un problème de programmation difficile. Si nous oublions, nous gaspillerons de la mémoire. Si nous le faisons trop tôt, nous aurons une variable invalide. Si nous le faisons deux fois, c'est aussi un bug. Nous devons associer exactement une `allocation` à exactement une `libération`.

Rust prend une voie différente : la mémoire est automatiquement retournée une fois la variable qui en est propriétaire sort de la portée. Voici une version de notre exemple de portée de la liste 4-1 utilisant un `String` au lieu d'une chaîne littérale :

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-02-string-scope/src/main.rs:here}}
```

Il existe un point naturel auquel nous pouvons retourner la mémoire dont notre `String` a besoin à l'allocateur : lorsque `s` sort de la portée. Lorsqu'une variable sort de la portée, Rust appelle une fonction spéciale pour nous. Cette fonction s'appelle `drop`, et c'est là où l'auteur de `String` peut mettre le code pour retourner la mémoire. Rust appelle `drop` automatiquement à la dernière accolade fermante.

> Remarque : Dans C++, ce modèle de désallocation des ressources à la fin de la durée de vie d'un élément est parfois appelé _Resource Acquisition Is Initialization (RAII)_. La fonction `drop` en Rust vous sera familière si vous avez utilisé des modèles RAII.

Ce modèle a un impact profond sur la manière dont le code Rust est écrit. Cela peut sembler simple pour le moment, mais le comportement du code peut être inattendu dans des situations plus compliquées lorsque nous voulons que plusieurs variables utilisent les données que nous avons allouées dans le tas. Explorons certaines de ces situations maintenant.

#### Interaction des variables et des données avec le mouvement

Plusieurs variables peuvent interagir avec les mêmes données de différentes manières en Rust. La liste 4-2 montre un exemple utilisant un entier.

<liste numéro="4-2" légende="Assignation de la valeur entière de la variable `x` à `y`">

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/listing-04-02/src/main.rs:here}}
```

</liste>

Nous pouvons probablement deviner ce que cela fait : « Lier la valeur `5` à `x` ; ensuite, faire une copie de la valeur dans `x` et la lier à `y` ». Nous avons maintenant deux variables, `x` et `y`, qui sont toutes deux égales à `5`. C'est en effet ce qui se passe, car les entiers sont des valeurs simples de taille fixe et connue, et ces deux valeurs `5` sont ajoutées à la pile.

Examinons maintenant la version `String` :

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-03-string-move/src/main.rs:here}}
```

Cela semble très similaire, donc nous pourrions supposer que le fonctionnement serait le même : c'est-à-dire que la deuxième ligne ferait une copie de la valeur dans `s1` et la lierait à `s2`. Mais ce n'est pas tout à fait ce qui se passe.

Regardez la Figure 4-1 pour voir ce qui se passe avec `String` sous le capot. Un `String` est composé de trois parties, montrées à gauche : un pointeur vers la mémoire qui contient le contenu de la chaîne, une longueur et une capacité. Ce groupe de données est stocké dans la pile. À droite se trouve la mémoire dans le tas qui contient le contenu.

<img alt="Deux tableaux : le premier tableau contient la représentation de s1 sur la pile, consistant en sa longueur (5), sa capacité (5) et un pointeur vers la première valeur dans le deuxième tableau. Le second tableau contient la représentation des données de la chaîne dans le tas, octet par octet." src="img/trpl04-01.svg" class="center" style="width: 50%;" />

<span class="caption">Figure 4-1 : La représentation en mémoire d'un `String` contenant la valeur `"hello"` liée à `s1`</span>

La longueur est la quantité de mémoire, en octets, que le contenu du `String` utilise actuellement. La capacité est le montant total de mémoire, en octets, que le `String` a reçu de l'allocateur. La différence entre longueur et capacité est importante, mais pas dans ce contexte, donc pour l'instant, il est acceptable d'ignorer la capacité.

Lorsque nous assignons `s1` à `s2`, les données `String` sont copiées, ce qui signifie que nous copions le pointeur, la longueur et la capacité qui se trouvent sur la pile. Nous ne copions pas les données dans le tas auxquelles le pointeur fait référence. En d'autres termes, la représentation des données en mémoire ressemble à la Figure 4-2.

<img alt="Trois tableaux : les tableaux s1 et s2 représentant ces chaînes sur la pile, respectivement, et tous deux pointant vers les mêmes données de chaîne dans le tas." src="img/trpl04-02.svg" class="center" style="width: 50%;" />

<span class="caption">Figure 4-2 : La représentation en mémoire de la variable `s2` qui a une copie du pointeur, de la longueur et de la capacité de `s1`</span>

La représentation _ne_ ressemble pas à la Figure 4-3, qui est ce que la mémoire ressemblerait si Rust copiait également les données du tas. Si Rust faisait cela, l'opération `s2 = s1` pourrait être très coûteuse en termes de performances d'exécution si les données dans le tas étaient volumineuses.

Plus tôt, nous avons dit que lorsqu'une variable sort de la portée, Rust appelle automatiquement la fonction `drop` et nettoie la mémoire du tas pour cette variable. Mais la Figure 4-2 montre que les deux pointeurs de données pointent vers le même emplacement. C'est un problème : lorsque `s2` et `s1` sortent de la portée, elles essaieront toutes deux de libérer la même mémoire. Cela est connu comme une erreur de _libération double_ et est l'un des bugs de sécurité de la mémoire que nous avons mentionnés précédemment. Libérer de la mémoire deux fois peut provoquer une corruption de la mémoire, ce qui peut potentiellement entraîner des vulnérabilités de sécurité.

Pour garantir la sécurité de la mémoire, après la ligne `let s2 = s1;`, Rust considère que `s1` n'est plus valide. Par conséquent, Rust n'a pas besoin de libérer quoi que ce soit lorsque `s1` sort de la portée. Découvrez ce qui se passe lorsque vous essayez d'utiliser `s1` après la création de `s2` ; cela ne fonctionnera pas :

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-04-cant-use-after-move/src/main.rs:here}}
```

Vous obtiendrez une erreur comme celle-ci parce que Rust vous empêche d'utiliser la référence invalidée :

```console
{{#include ../listings/ch04-understanding-ownership/no-listing-04-cant-use-after-move/output.txt}}
```

Si vous avez entendu les termes _copie superficielle_ et _copie profonde_ en travaillant avec d'autres langages, le concept de copier le pointeur, la longueur et la capacité sans copier les données ressemble probablement à une copie superficielle. Mais parce que Rust invalide également la première variable, au lieu de cela, on appelle cela un _mouvement_. Dans cet exemple, nous dirions que `s1` a été _déplacé_ dans `s2`. Ainsi, ce qui se passe réellement est montré dans la Figure 4-4.

<img alt="Trois tableaux : les tableaux s1 et s2 représentant ces chaînes sur la pile, respectivement, et tous deux pointant vers les mêmes données de chaîne dans le tas. Le tableau s1 est grisé car s1 n'est plus valide ; seul s2 peut être utilisé pour accéder aux données du tas." src="img/trpl04-04.svg" class="center" style="width: 50%;" />

<span class="caption">Figure 4-4 : La représentation en mémoire après que `s1` a été invalidé</span>

Cela résout notre problème ! Avec seulement `s2` valide, lorsqu'il sort de la portée, il libérera la mémoire à lui seul, et nous avons fini.

De plus, il y a un choix de conception qui est implicite dans cela : Rust ne créera jamais automatiquement des copies « profondes » de vos données. Par conséquent, toute opération de _copie_ peut être considérée comme peu coûteuse en termes de performances d'exécution.

#### Portée et affectation

L'inverse est vrai pour la relation entre la portée, l'appartenance, et la mémoire libérée via la fonction `drop`. Lorsque vous assignez une valeur totalement nouvelle à une variable existante, Rust appellera `drop` et libérera immédiatement la mémoire de la valeur d'origine. Considérez ce code, par exemple :

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-04b-replacement-drop/src/main.rs:here}}
```

Nous déclarons initialement une variable `s` et la relions à un `String` avec la valeur `"hello"`. Ensuite, nous créons immédiatement un nouveau `String` avec la valeur `"ahoy"` et l'assignons à `s`. À ce stade, rien ne fait référence à la valeur d'origine dans le tas. La Figure 4-5 illustre maintenant les données de la pile et du tas :

<img alt="Un tableau représentant la valeur de chaîne sur la pile, pointant vers le second morceau de données de chaîne (ahoy) dans le tas, avec les données de chaîne d'origine (hello) grisée car elle ne peut plus être accédée." src="img/trpl04-05.svg" class="center" style="width: 50%;" />

<span class="caption">Figure 4-5 : La représentation en mémoire après que la valeur initiale a été complètement remplacée</span>

La chaîne originale sort donc immédiatement de la portée. Rust exécutera la fonction `drop` sur elle et sa mémoire sera libérée immédiatement. Lorsque nous imprimons la valeur à la fin, elle sera `"ahoy, world!"`.

#### Interaction des variables et des données avec clone

Si nous _voulons_ copier profondément les données du tas de `String`, pas seulement les données de la pile, nous pouvons utiliser une méthode commune appelée `clone`. Nous discuterons de la syntaxe des méthodes dans le chapitre 5, mais comme les méthodes sont une caractéristique commune de nombreux langages de programmation, vous les avez probablement déjà vues auparavant.

Voici un exemple de la méthode `clone` en action :

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-05-clone/src/main.rs:here}}
```

Cela fonctionne très bien et produit explicitement le comportement montré dans la Figure 4-3, où les données du tas _sont_ effectivement copiées.

Lorsque vous voyez un appel à `clone`, vous savez qu'un code arbitraire est en cours d'exécution et que ce code peut être coûteux. C'est un indicateur visuel que quelque chose de différent se passe.

#### Données uniquement sur la pile : Copy

Il y a un autre aspect que nous n'avons pas encore abordé. Ce code utilisant des entiers – dont une partie a été montrée dans la liste 4-2 – fonctionne et est valide :

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-06-copy/src/main.rs:here}}
```

Mais ce code semble contredire ce que nous venons d'apprendre : nous n'avons pas d'appel à `clone`, mais `x` est toujours valide et n'a pas été déplacé dans `y`.

La raison en est que les types tels que les entiers qui ont une taille connue au moment de la compilation sont entièrement stockés dans la pile, donc les copies des valeurs réelles sont rapides à réaliser. Cela signifie qu'il n'y a aucune raison d'empêcher `x` d'être valide après la création de la variable `y`. En d'autres termes, il n'y a aucune différence entre les copies profondes et superficielles ici, donc appeler `clone` ne ferait rien de différent d'une copie superficielle habituelle, et nous pouvons l'omettre.

Rust a une annotation spéciale appelée le trait `Copy` que nous pouvons placer sur des types qui sont stockés dans la pile, comme les entiers (nous aborderons plus en détail les traits dans [Chapitre 10][traits]<!-- ignore -->). Si un type implémente le trait `Copy`, les variables qui l'utilisent ne se déplacent pas, mais sont plutôt copiées de manière trivial, les rendant toujours valides après avoir été assignées à une autre variable.

Rust ne nous permettra pas d'annoter un type avec `Copy` si le type, ou une de ses parties, a implémenté le trait `Drop`. Si le type nécessite que quelque chose de spécial se produise lorsque la valeur sort de la portée et que nous ajoutons l'annotation `Copy` à ce type, nous obtiendrons une erreur au moment de la compilation. Pour apprendre à ajouter l'annotation `Copy` à votre type pour implémenter le trait, consultez [« Traits dérivables »][derivable-traits]<!-- ignore --> dans l'appendice C.

Alors, quels types implémentent le trait `Copy` ? Vous pouvez vérifier la documentation pour le type donné pour en être sûr, mais en règle générale, tout groupe de valeurs scalaires simples peut implémenter `Copy`, et rien qui nécessite une allocation ou est une forme de ressource ne peut implémenter `Copy`. Voici quelques-uns des types qui implémentent `Copy` :

- Tous les types d'entiers, comme `u32`.
- Le type booléen, `bool`, avec les valeurs `true` et `false`.
- Tous les types à virgule flottante, comme `f64`.
- Le type caractère, `char`.
- Les tuples, s'ils ne contiennent que des types qui implémentent également `Copy`. Par exemple, `(i32, i32)` implémente `Copy`, mais `(i32, String)` ne le fait pas.

### Appartenance et fonctions

Les mécanismes de passage d'une valeur à une fonction sont similaires à ceux lors de l'assignation d'une valeur à une variable. Passer une variable à une fonction se déplacera ou se copiera, tout comme l'assignation. La liste 4-3 contient un exemple avec des annotations montrant où les variables entrent et sortent de la portée.

<liste numéro="4-3" nom de fichier="src/main.rs" légende="Fonctions avec appartenance et portée annotées">

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/listing-04-03/src/main.rs}}
```

</liste>

Si nous essayions d'utiliser `s` après l'appel à `takes_ownership`, Rust génèrerait une erreur de compilation. Ces vérifications statiques nous protègent des erreurs. Essayez d'ajouter du code à `main` qui utilise `s` et `x` pour voir où vous pouvez les utiliser et où les règles d'appartenance vous en empêchent.

### Valeurs de retour et portée

Le retour de valeurs peut également transférer l'appartenance. La liste 4-4 montre un exemple d'une fonction qui retourne une valeur, avec des annotations similaires à celles de la liste 4-3.

<liste numéro="4-4" nom de fichier="src/main.rs" légende="Transférer l'appartenance des valeurs de retour">

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/listing-04-04/src/main.rs}}
```

</liste>

L'appartenance d'une variable suit le même modèle chaque fois : assigner une valeur à une autre variable la déplace. Lorsqu'une variable qui inclut des données dans le tas sort de la portée, la valeur sera nettoyée par `drop` à moins que l'appartenance des données n'ait été déplacée vers une autre variable.

Bien que cela fonctionne, prendre l'appartenance puis retourner l'appartenance avec chaque fonction est un peu fastidieux. Que se passe-t-il si nous voulons permettre à une fonction d'utiliser une valeur sans prendre l'appartenance ? Il est assez ennuyeux que tout ce que nous passons doive également être renvoyé si nous voulons l'utiliser à nouveau, en plus de toutes les données résultant du corps de la fonction que nous pourrions également vouloir renvoyer.

Rust nous permet de retourner plusieurs valeurs en utilisant un tuple, comme le montre la liste 4-5.

<liste numéro="4-5" légende="Retourner l'appartenance des paramètres">

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/listing-04-05/src/main.rs}}
```

</liste>

Mais cela est trop de cérémonie et beaucoup de travail pour un concept qui devrait être courant. Heureusement pour nous, Rust a une fonctionnalité pour utiliser une valeur sans transférer l'appartenance : les références.

[data-types]: ch03-02-data-types.html#data-types
[ch8]: ch08-02-strings.html
[traits]: ch10-02-traits.html
[derivable-traits]: appendix-03-derivable-traits.html
[methods]: ch05-03-method-syntax.html#methods
[paths-module-tree]: ch07-03-paths-for-referring-to-an-item-in-the-module-tree.html