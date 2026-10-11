## Refactoriser pour améliorer la modularité et la gestion des erreurs

Pour améliorer notre programme, nous allons corriger quatre problèmes liés à sa structure et à la façon dont il gère les erreurs potentielles. Tout d’abord, notre fonction `main` effectue maintenant deux tâches : elle analyse les arguments et lit les fichiers. À mesure que notre programme grandit, le nombre de tâches distinctes prises en charge par la fonction `main` augmentera. Plus une fonction a de responsabilités, plus il devient difficile de raisonner à son sujet, de la tester et de la modifier sans en altérer une partie. Il est préférable de séparer les fonctionnalités afin que chaque fonction soit responsable d’une seule tâche.

Ce problème est également lié au deuxième : bien que `query` et `file_path` soient des variables de configuration pour notre programme, des variables comme `contents` servent à exécuter la logique du programme. Plus la fonction `main` s’allonge, plus nous devons introduire de variables dans sa portée ; et plus nous avons de variables dans cette portée, plus il est difficile de se souvenir du rôle de chacune. Il est préférable de regrouper les variables de configuration dans une seule structure pour clarifier leur rôle.

Le troisième problème est que nous avons utilisé `expect` pour afficher un message d’erreur lorsque la lecture du fichier échoue, mais le message d’erreur se contente d’afficher `Should have been able to read the file`. La lecture d’un fichier peut échouer de plusieurs façons : par exemple, le fichier peut être absent ou nous ne disposons peut-être pas des autorisations nécessaires pour l’ouvrir. Pour l’instant, quelle que soit la situation, nous affichons le même message d’erreur, qui ne fournit aucune information à l’utilisateur !

Quatrièmement, nous utilisons `expect` pour gérer une erreur et, si l’utilisateur exécute notre programme sans spécifier suffisamment d’arguments, il obtient une erreur `index out of bounds` de Rust qui n’explique pas clairement le problème. Il serait préférable que tout le code de gestion des erreurs se trouve au même endroit, afin que les futurs responsables de la maintenance n’aient qu’un seul endroit à consulter si la logique de gestion des erreurs doit être modifiée. Regrouper tout le code de gestion des erreurs au même endroit garantira également que les messages affichés seront utiles aux utilisateurs finaux.

Corrigeons ces quatre problèmes en refactorisant notre projet.

<!-- Old headings. Do not remove or links may break. -->

<a id="separation-of-concerns-for-binary-projects"></a>

### Séparer les préoccupations dans les projets binaires

Le problème d’organisation qui consiste à attribuer à la fonction `main` la responsabilité de plusieurs tâches est courant dans de nombreux projets binaires. C’est pourquoi beaucoup de programmeurs Rust trouvent utile de séparer les différentes préoccupations d’un programme binaire lorsque la fonction `main` commence à devenir volumineuse. Ce processus comporte les étapes suivantes :

- Séparez votre programme en un fichier _main.rs_ et un fichier _lib.rs_, puis déplacez la logique de votre programme dans _lib.rs_.
- Tant que la logique d’analyse de la ligne de commande reste simple, elle peut demeurer dans la fonction `main`.
- Lorsque la logique d’analyse de la ligne de commande commence à se compliquer, extrayez-la de la fonction `main` et placez-la dans d’autres fonctions ou types.

Après ce processus, les responsabilités qui restent dans la fonction `main` devraient se limiter aux suivantes :

- Appeler la logique d’analyse de la ligne de commande en lui transmettant les valeurs des arguments
- Configurer tout autre élément nécessaire
- Appeler une fonction `run` dans _lib.rs_
- Gérer l’erreur si `run` renvoie une erreur

Ce modèle consiste à séparer les préoccupations : _main.rs_ se charge de l’exécution du programme et _lib.rs_ de toute la logique de la tâche à accomplir. Comme il est impossible de tester directement la fonction `main`, cette structure vous permet de tester toute la logique de votre programme en la déplaçant hors de la fonction `main`. Le code qui reste dans la fonction `main` sera suffisamment court pour que vous puissiez vérifier sa correction en le lisant. Réorganisons notre programme en suivant ce processus.

#### Extraire l’analyseur d’arguments

Nous allons extraire la fonctionnalité d’analyse des arguments dans une fonction que `main` appellera. La liste 12-5 montre le début de la nouvelle fonction `main`, qui appelle une nouvelle fonction `parse_config` que nous allons définir dans _src/main.rs_.

<Listing number="12-5" file-name="src/main.rs" caption="Extraire une fonction `parse_config` de `main`">

```rust,ignore
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-05/src/main.rs:here}}
```

</Listing>

Nous continuons à rassembler les arguments de la ligne de commande dans un vecteur, mais au lieu d’affecter la valeur de l’argument à l’index 1 à la variable `query` et celle de l’argument à l’index 2 à la variable `file_path` dans la fonction `main`, nous transmettons le vecteur entier à la fonction `parse_config`. La fonction `parse_config` contient alors la logique qui détermine quel argument correspond à quelle variable, puis renvoie les valeurs à `main`. Nous créons toujours les variables `query` et `file_path` dans `main`, mais `main` n’a plus la responsabilité de déterminer la correspondance entre les arguments de la ligne de commande et les variables.

Cette réorganisation peut sembler excessive pour notre petit programme, mais nous refactorisons par petites étapes progressives. Après cette modification, exécutez à nouveau le programme pour vérifier que l’analyse des arguments fonctionne toujours. Il est judicieux de vérifier souvent votre progression afin de pouvoir identifier la cause des problèmes lorsqu’ils surviennent.

#### Regrouper les valeurs de configuration

Nous pouvons faire un autre petit pas pour améliorer davantage la fonction `parse_config`. Pour le moment, nous renvoyons un tuple, puis nous le décomposons immédiatement en éléments individuels. C’est peut-être le signe que nous n’avons pas encore trouvé la bonne abstraction.

Un autre indice qu’il est possible d’améliorer les choses est la partie `config` de `parse_config`, qui suggère que les deux valeurs renvoyées sont liées et font toutes deux partie d’une même valeur de configuration. Pour l’instant, la structure des données n’exprime pas cette signification autrement qu’en regroupant les deux valeurs dans un tuple ; nous allons plutôt les placer dans une seule structure et donner à chacun de ses champs un nom évocateur. Les futurs responsables de la maintenance de ce code comprendront ainsi plus facilement les liens entre les différentes valeurs et le rôle de chacune.

La liste 12-6 présente les améliorations apportées à la fonction `parse_config`.

<Listing number="12-6" file-name="src/main.rs" caption="Refactoriser `parse_config` pour renvoyer une instance d’une structure `Config`">

```rust,should_panic,noplayground
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-06/src/main.rs:here}}
```

</Listing>

Nous avons ajouté une structure nommée `Config`, définie avec des champs nommés `query` et `file_path`. La signature de `parse_config` indique maintenant qu’elle renvoie une valeur `Config`. Dans le corps de `parse_config`, là où nous renvoyions auparavant des tranches de chaînes faisant référence aux valeurs `String` de `args`, nous définissons maintenant `Config` pour qu’elle contienne des valeurs `String` possédées. La variable `args` dans `main` possède les valeurs des arguments et ne fait que les prêter à la fonction `parse_config`, ce qui signifie que nous enfreindrions les règles d’emprunt de Rust si `Config` essayait de prendre possession des valeurs de `args`.

Il existe plusieurs façons de gérer les données `String` ; la plus simple, quoique quelque peu inefficace, consiste à appeler la méthode `clone` sur les valeurs. Cela créera une copie complète des données, que l’instance `Config` possédera, ce qui demande plus de temps et de mémoire que de stocker une référence aux données de la chaîne. Toutefois, cloner les données simplifie aussi beaucoup notre code, car nous n’avons pas à gérer les durées de vie des références ; dans ce cas, renoncer à un peu de performances pour gagner en simplicité est un compromis qui en vaut la peine.

> ### Les compromis liés à l’utilisation de `clone`
>
> De nombreux adeptes de Rust ont tendance à éviter d’utiliser `clone` pour résoudre des problèmes de propriété, en raison de son coût à l’exécution. Dans le [chapitre 13][ch13]<!-- ignore -->, vous apprendrez à utiliser des méthodes plus efficaces dans ce genre de situation. Pour le moment, cependant, vous pouvez copier quelques chaînes afin de continuer à avancer, car vous ne les copierez qu’une seule fois et que votre chemin de fichier et votre chaîne de recherche sont très courts. Mieux vaut avoir un programme fonctionnel, même un peu inefficace, que d’essayer de l’optimiser à l’excès dès le premier passage. À mesure que vous gagnerez en expérience avec Rust, il vous sera plus facile de commencer par la solution la plus efficace, mais pour l’instant, vous pouvez tout à fait appeler `clone`.

Nous avons modifié `main` afin qu’elle place l’instance de `Config` renvoyée par `parse_config` dans une variable nommée `config`, et nous avons mis à jour le code qui utilisait auparavant les variables distinctes `query` et `file_path` pour qu’il utilise maintenant les champs de la structure `Config`.

Notre code indique maintenant plus clairement que `query` et `file_path` sont liés et qu’ils servent à configurer le fonctionnement du programme. Tout code qui utilise ces valeurs sait qu’il doit les trouver dans l’instance `config`, dans les champs nommés d’après leur rôle.

#### Créer un constructeur pour `Config`

Jusqu’à présent, nous avons extrait de `main` la logique responsable de l’analyse des arguments de la ligne de commande et l’avons placée dans la fonction `parse_config`. Cela nous a aidés à constater que les valeurs `query` et `file_path` étaient liées et que cette relation devait être exprimée dans notre code. Nous avons ensuite ajouté une structure `Config` pour désigner le rôle commun de `query` et `file_path` et pour pouvoir renvoyer ces valeurs sous forme de champs de la structure depuis la fonction `parse_config`.

Maintenant que la fonction `parse_config` a pour rôle de créer une instance `Config`, nous pouvons remplacer cette fonction ordinaire par une fonction nommée `new` associée à la structure `Config`. Cette modification rendra le code plus idiomatique. Nous pouvons créer des instances de types de la bibliothèque standard, comme `String`, en appelant `String::new`. De même, en transformant `parse_config` en une fonction `new` associée à `Config`, nous pourrons créer des instances de `Config` en appelant `Config::new`. La liste 12-7 montre les modifications à apporter.

<Listing number="12-7" file-name="src/main.rs" caption="Remplacer `parse_config` par `Config::new`">

```rust,should_panic,noplayground
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-07/src/main.rs:here}}
```

</Listing>

Nous avons modifié l’appel à `parse_config` dans `main` pour appeler `Config::new` à la place. Nous avons renommé `parse_config` en `new` et déplacé la fonction dans un bloc `impl`, qui associe la fonction `new` à `Config`. Essayez de compiler à nouveau ce code pour vérifier qu’il fonctionne.

### Corriger la gestion des erreurs

Nous allons maintenant nous occuper de corriger la gestion des erreurs. Rappelez-vous que tenter d’accéder aux valeurs du vecteur `args` à l’index 1 ou 2 provoquera une panique si le vecteur contient moins de trois éléments. Essayez d’exécuter le programme sans arguments ; voici ce qui s’affichera :

```console
{{#include ../listings/ch12-an-io-project/listing-12-07/output.txt}}
```

La ligne `index out of bounds: the len is 1 but the index is 1` est un message d’erreur destiné aux programmeurs. Elle n’aidera pas nos utilisateurs finaux à comprendre ce qu’ils doivent faire. Corrigeons cela maintenant.

#### Améliorer le message d’erreur

Dans la liste 12-8, nous ajoutons à la fonction `new` une vérification qui s’assure que la tranche est suffisamment longue avant d’accéder aux index 1 et 2. Si la tranche n’est pas assez longue, le programme déclenche une panique et affiche un meilleur message d’erreur.

<Listing number="12-8" file-name="src/main.rs" caption="Ajouter une vérification du nombre d’arguments">

```rust,ignore
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-08/src/main.rs:here}}
```

</Listing>

Ce code ressemble à la [fonction `Guess::new` que nous avons écrite dans la liste 9-13][ch9-custom-types]<!-- ignore -->, où nous avons appelé `panic!` lorsque l’argument `value` était en dehors de la plage des valeurs valides. Ici, au lieu de vérifier une plage de valeurs, nous vérifions que la longueur de `args` est au moins égale à `3`, et le reste de la fonction peut partir du principe que cette condition est remplie. Si `args` contient moins de trois éléments, cette condition sera `true` et nous appellerons la macro `panic!` pour mettre immédiatement fin au programme.

Après avoir ajouté ces quelques lignes de code à `new`, exécutons à nouveau le programme sans arguments pour voir à quoi ressemble maintenant l’erreur :

```console
{{#include ../listings/ch12-an-io-project/listing-12-08/output.txt}}
```

Cette sortie est meilleure : nous avons maintenant un message d’erreur raisonnable. Cependant, elle contient aussi des informations superflues que nous ne voulons pas communiquer à nos utilisateurs. La technique utilisée dans la liste 9-13 n’est peut-être pas la meilleure dans ce cas : un appel à `panic!` convient davantage à un problème de programmation qu’à un problème d’utilisation, [comme nous l’avons vu au chapitre 9][ch9-error-guidelines]<!-- ignore -->. Nous allons plutôt utiliser l’autre technique présentée au chapitre 9 : [renvoyer un `Result`][ch9-result]<!-- ignore --> indiquant soit une réussite, soit une erreur.

<!-- Old headings. Do not remove or links may break. -->

<a id="returning-a-result-from-new-instead-of-calling-panic"></a>

#### Renvoyer un `Result` au lieu d’appeler `panic!`

Nous pouvons renvoyer une valeur `Result` qui contiendra une instance `Config` en cas de réussite et décrira le problème en cas d’erreur. Nous allons également renommer la fonction `new` en `build`, car de nombreux programmeurs s’attendent à ce que les fonctions `new` ne puissent jamais échouer. Lorsque `Config::build` communiquera avec `main`, nous pourrons utiliser le type `Result` pour signaler un problème. Nous pourrons alors modifier `main` pour transformer une variante `Err` en une erreur plus compréhensible pour nos utilisateurs, sans le texte environnant sur `thread 'main'` et `RUST_BACKTRACE` qu’entraîne un appel à `panic!`.

La liste 12-9 présente les modifications à apporter à la valeur de retour de la fonction que nous appelons maintenant `Config::build`, ainsi qu’au corps de la fonction pour qu’elle renvoie un `Result`. Notez que ce code ne compilera pas tant que nous n’aurons pas également modifié `main`, ce que nous ferons dans la liste suivante.

<Listing number="12-9" file-name="src/main.rs" caption="Renvoyer un `Result` depuis `Config::build`">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-09/src/main.rs:here}}
```

</Listing>

Notre fonction `build` renvoie un `Result` contenant une instance `Config` en cas de réussite et un littéral de chaîne en cas d’erreur. Nos valeurs d’erreur seront toujours des littéraux de chaîne ayant la durée de vie `'static`.

Nous avons apporté deux modifications au corps de la fonction : au lieu d’appeler `panic!` lorsque l’utilisateur ne transmet pas assez d’arguments, nous renvoyons maintenant une valeur `Err`, et nous avons enveloppé la valeur `Config` renvoyée dans un `Ok`. Ces modifications rendent la fonction conforme à sa nouvelle signature de type.

Renvoyer une valeur `Err` depuis `Config::build` permet à la fonction `main` de gérer la valeur `Result` renvoyée par la fonction `build` et de se terminer plus proprement en cas d’erreur.

<!-- Old headings. Do not remove or links may break. -->

<a id="calling-confignew-and-handling-errors"></a>

#### Appeler `Config::build` et gérer les erreurs

Pour gérer le cas d’erreur et afficher un message compréhensible pour l’utilisateur, nous devons modifier `main` afin qu’elle gère le `Result` renvoyé par `Config::build`, comme le montre la liste 12-10. Nous allons également retirer à `panic!` la responsabilité de terminer l’outil en ligne de commande avec un code d’erreur non nul et l’implémenter nous-mêmes. Un statut de sortie non nul est une convention qui signale au processus ayant appelé notre programme que celui-ci s’est terminé dans un état d’erreur.

<Listing number="12-10" file-name="src/main.rs" caption="Terminer avec un code d’erreur si la construction de `Config` échoue">

```rust,ignore
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-10/src/main.rs:here}}
```

</Listing>

Dans cette liste, nous utilisons une méthode que nous n’avons pas encore étudiée en détail : `unwrap_or_else`, qui est définie sur `Result<T, E>` par la bibliothèque standard. L’utilisation de `unwrap_or_else` nous permet de définir une gestion personnalisée des erreurs qui ne déclenche pas de `panic!`. Si le `Result` est une valeur `Ok`, le comportement de cette méthode est similaire à celui de `unwrap` : elle renvoie la valeur interne enveloppée par `Ok`. En revanche, si la valeur est `Err`, cette méthode appelle le code de la fermeture, une fonction anonyme que nous définissons et transmettons comme argument à `unwrap_or_else`. Nous étudierons les fermetures plus en détail au [chapitre 13][ch13]<!-- ignore -->. Pour le moment, retenez que `unwrap_or_else` transmettra à notre fermeture la valeur interne de `Err` — ici, la chaîne statique `"not enough arguments"` que nous avons ajoutée dans la liste 12-9 — sous la forme de l’argument `err`, qui apparaît entre les barres verticales. Le code de la fermeture peut alors utiliser la valeur `err` lorsqu’il s’exécute.

Nous avons ajouté une nouvelle ligne `use` pour introduire `process` de la bibliothèque standard dans la portée. Le code de la fermeture exécuté en cas d’erreur ne compte que deux lignes : nous affichons la valeur `err`, puis nous appelons `process::exit`. La fonction `process::exit` arrête immédiatement le programme et renvoie le nombre transmis comme code de statut de sortie. C’est similaire à la gestion des erreurs fondée sur `panic!` que nous avons utilisée dans la liste 12-8, mais sans toutes les informations supplémentaires. Essayons :

```console
{{#include ../listings/ch12-an-io-project/listing-12-10/output.txt}}
```

Parfait ! Cette sortie est beaucoup plus claire pour nos utilisateurs.

<!-- Old headings. Do not remove or links may break. -->

<a id="extracting-logic-from-the-main-function"></a>

### Extraire la logique de `main`

Maintenant que nous avons terminé la refactorisation de l’analyse de la configuration, intéressons-nous à la logique du programme. Comme nous l’avons indiqué dans [« Séparer les préoccupations dans les projets binaires »](#separation-of-concerns-for-binary-projects)<!-- ignore -->, nous allons extraire une fonction nommée `run` qui contiendra toute la logique actuellement présente dans la fonction `main`, à l’exception de celle qui sert à configurer le programme ou à gérer les erreurs. Une fois cette opération terminée, la fonction `main` sera concise et facile à vérifier par inspection, et nous pourrons écrire des tests pour toute la logique restante.

La liste 12-11 montre cette petite amélioration progressive, qui consiste à extraire une fonction `run`.

<Listing number="12-11" file-name="src/main.rs" caption="Extraire une fonction `run` contenant le reste de la logique du programme">

```rust,ignore
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-11/src/main.rs:here}}
```

</Listing>

La fonction `run` contient maintenant toute la logique restante de `main`, à commencer par la lecture du fichier. La fonction `run` prend l’instance `Config` comme argument.

<!-- Old headings. Do not remove or links may break. -->

<a id="returning-errors-from-the-run-function"></a>

#### Renvoyer les erreurs depuis `run`

La logique restante du programme étant maintenant séparée dans la fonction `run`, nous pouvons améliorer la gestion des erreurs, comme nous l’avons fait pour `Config::build` dans la liste 12-9. Au lieu de laisser le programme déclencher une panique en appelant `expect`, la fonction `run` renverra un `Result<T, E>` en cas de problème. Cela nous permettra de regrouper davantage la logique de gestion des erreurs dans `main`, de manière compréhensible pour l’utilisateur. La liste 12-12 montre les modifications à apporter à la signature et au corps de `run`.

<Listing number="12-12" file-name="src/main.rs" caption="Modifier la fonction `run` pour qu’elle renvoie un `Result`">

```rust,ignore
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-12/src/main.rs:here}}
```

</Listing>

Nous avons apporté trois modifications importantes. Premièrement, nous avons changé le type de retour de la fonction `run` en `Result<(), Box<dyn Error>>`. Auparavant, cette fonction renvoyait le type unité, `()`, et nous le conservons comme valeur renvoyée en cas de réussite.

Pour le type d’erreur, nous avons utilisé l’objet trait `Box<dyn Error>` (et introduit `std::error::Error` dans la portée à l’aide d’une instruction `use` en haut du fichier). Nous étudierons les objets trait au [chapitre 18][ch18]<!-- ignore -->. Pour l’instant, retenez que `Box<dyn Error>` signifie que la fonction renverra un type qui implémente le trait `Error`, sans que nous ayons à préciser de quel type il s’agit. Cela nous permet de renvoyer des valeurs d’erreur de types différents selon les cas. Le mot-clé `dyn` est l’abréviation de _dynamic_ (« dynamique »).

Deuxièmement, nous avons remplacé l’appel à `expect` par l’opérateur `?`, comme nous l’avons vu au [chapitre 9][ch9-question-mark]<!-- ignore -->. Au lieu de déclencher une panique en cas d’erreur, `?` renvoie la valeur d’erreur depuis la fonction courante afin que l’appelant puisse la gérer.

Troisièmement, la fonction `run` renvoie maintenant une valeur `Ok` en cas de réussite. Nous avons déclaré le type de réussite de la fonction `run` comme étant `()` dans la signature, ce qui signifie que nous devons envelopper la valeur de type unité dans une valeur `Ok`. La syntaxe `Ok(())` peut sembler un peu étrange au premier abord. Cependant, utiliser `()` de cette manière est la façon idiomatique d’indiquer que nous appelons `run` uniquement pour ses effets de bord ; elle ne renvoie aucune valeur dont nous avons besoin.

Lorsque vous exécuterez ce code, il compilera, mais affichera un avertissement :

```console
{{#include ../listings/ch12-an-io-project/listing-12-12/output.txt}}
```

Rust nous indique que notre code a ignoré la valeur `Result` et que celle-ci peut signaler qu’une erreur s’est produite. Or, nous ne vérifions pas s’il y a eu une erreur, et le compilateur nous rappelle que nous avions probablement l’intention d’ajouter du code de gestion des erreurs ici ! Corrigeons ce problème maintenant.

#### Gérer dans `main` les erreurs renvoyées par `run`

Nous allons vérifier la présence d’erreurs et les gérer à l’aide d’une technique similaire à celle que nous avons utilisée avec `Config::build` dans la liste 12-10, avec une légère différence :

<span class="filename">Nom du fichier : src/main.rs</span>

```rust,ignore
{{#rustdoc_include ../listings/ch12-an-io-project/no-listing-01-handling-errors-in-main/src/main.rs:here}}
```

Nous utilisons `if let` plutôt que `unwrap_or_else` pour vérifier si `run` renvoie une valeur `Err` et appeler `process::exit(1)` le cas échéant. La fonction `run` ne renvoie pas de valeur que nous souhaitons extraire avec `unwrap`, contrairement à `Config::build`, qui renvoie l’instance `Config`. Comme `run` renvoie `()` en cas de réussite, nous voulons seulement détecter une erreur ; nous n’avons donc pas besoin que `unwrap_or_else` renvoie la valeur extraite, qui serait simplement `()`.

Dans les deux cas, le corps de `if let` et celui de la fonction `unwrap_or_else` sont identiques : nous affichons l’erreur et nous quittons le programme.

### Répartir le code dans une crate de bibliothèque

Notre projet `minigrep` se présente bien jusqu’ici ! Nous allons maintenant séparer le fichier _src/main.rs_ et placer une partie du code dans le fichier _src/lib.rs_. Nous pourrons ainsi tester le code et réduire le nombre de responsabilités du fichier _src/main.rs_.

Définissons le code chargé de rechercher du texte dans _src/lib.rs_ plutôt que dans _src/main.rs_. Cela permettra à nous-mêmes — ou à toute autre personne utilisant notre bibliothèque `minigrep` — d’appeler la fonction de recherche depuis davantage de contextes que notre binaire `minigrep`.

Tout d’abord, définissons la signature de la fonction `search` dans _src/lib.rs_, comme le montre la liste 12-13, avec un corps qui appelle la macro `unimplemented!`. Nous expliquerons plus en détail la signature lorsque nous compléterons son implémentation.

<Listing number="12-13" file-name="src/lib.rs" caption="Définir la fonction `search` dans *src/lib.rs*">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-13/src/lib.rs}}
```

</Listing>

Nous avons utilisé le mot-clé `pub` dans la définition de la fonction pour indiquer que `search` fait partie de l’API publique de notre crate de bibliothèque. Nous disposons maintenant d’une crate de bibliothèque que nous pouvons utiliser depuis notre crate binaire et que nous pouvons tester !

Nous devons maintenant introduire dans la portée de la crate binaire le code défini dans _src/lib.rs_, depuis _src/main.rs_, et l’appeler, comme le montre la liste 12-14.

<Listing number="12-14" file-name="src/main.rs" caption="Utiliser la fonction `search` de la crate de bibliothèque `minigrep` dans *src/main.rs*">

```rust,ignore
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-14/src/main.rs:here}}
```

</Listing>

Nous ajoutons une ligne `use minigrep::search` pour introduire la fonction `search` de la crate de bibliothèque dans la portée de la crate binaire. Ensuite, dans la fonction `run`, au lieu d’afficher le contenu du fichier, nous appelons la fonction `search` en lui transmettant la valeur `config.query` et `contents` comme arguments. La fonction `run` utilise alors une boucle `for` pour afficher chaque ligne renvoyée par `search` qui correspond à la requête. C’est également le bon moment pour supprimer les appels à `println!` dans la fonction `main` qui affichaient la requête et le chemin du fichier, afin que notre programme n’affiche que les résultats de la recherche (en l’absence d’erreur).

Notez que la fonction de recherche rassemble tous les résultats dans un vecteur qu’elle renvoie avant que quoi que ce soit ne soit affiché. Cette implémentation peut ralentir l’affichage des résultats lors de la recherche dans de gros fichiers, car les résultats ne sont pas affichés au fur et à mesure qu’ils sont trouvés ; nous verrons au chapitre 13 une façon de résoudre ce problème à l’aide d’itérateurs.

Ouf ! Cela a demandé beaucoup de travail, mais nous avons préparé le terrain pour la suite. Il est maintenant beaucoup plus facile de gérer les erreurs, et notre code est plus modulaire. À partir de maintenant, presque tout notre travail se fera dans _src/lib.rs_.

Profitons de cette nouvelle modularité pour faire quelque chose qui aurait été difficile avec l’ancien code, mais qui est facile avec le nouveau : écrire des tests !

[ch13]: ch13-00-functional-features.html
[ch9-custom-types]: ch09-03-to-panic-or-not-to-panic.html#creating-custom-types-for-validation
[ch9-error-guidelines]: ch09-03-to-panic-or-not-to-panic.html#guidelines-for-error-handling
[ch9-result]: ch09-02-recoverable-errors-with-result.html
[ch18]: ch18-00-oop.html
[ch9-question-mark]: ch09-02-recoverable-errors-with-result.html#a-shortcut-for-propagating-errors-the--operator