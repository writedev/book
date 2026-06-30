## Refactorisation pour Améliorer la Modularité et la Gestion des Erreurs

Pour améliorer notre programme, nous allons résoudre quatre problèmes liés à la structure du programme et à la gestion des erreurs potentielles. Tout d'abord, notre fonction `main` effectue désormais deux tâches : elle analyse les arguments et lit les fichiers. À mesure que notre programme se développe, le nombre de tâches distinctes gérées par la fonction `main` augmentera. Lorsqu'une fonction accumule des responsabilités, elle devient plus difficile à comprendre, plus difficile à tester et plus difficile à modifier sans casser une de ses parties. Il est préférable de séparer les fonctionnalités afin que chaque fonction soit responsable d'une seule tâche.

Ce problème est également lié au deuxième : bien que `query` et `file_path` soient des variables de configuration pour notre programme, des variables comme `contents` sont utilisées pour exécuter la logique du programme. Plus la fonction `main` devient longue, plus nous aurons besoin d'inclure de variables dans le contexte ; plus nous avons de variables dans le contexte, plus il sera difficile de garder une trace de leur but. Il est préférable de regrouper les variables de configuration dans une seule structure pour clarifier leur objectif.

Le troisième problème est que nous utilisons `expect` pour afficher un message d'erreur lorsque la lecture du fichier échoue, mais le message d'erreur indique seulement `Should have been able to read the file`. La lecture d'un fichier peut échouer de plusieurs manières : par exemple, le fichier peut être manquant ou nous n'avons peut-être pas la permission de l'ouvrir. En ce moment, peu importe la situation, nous afficherions le même message d'erreur pour tout, ce qui ne donnerait aucune information à l'utilisateur !

Quatrièmement, nous utilisons `expect` pour gérer une erreur, et si l'utilisateur exécute notre programme sans spécifier suffisamment d'arguments, il obtiendra une erreur `index out of bounds` de Rust qui n'explique pas clairement le problème. Il serait préférable que tout le code de gestion des erreurs soit regroupé au même endroit afin que les futurs mainteneurs n'aient qu'un seul endroit à consulter si la logique de gestion des erreurs devait changer. Avoir tout le code de gestion des erreurs au même endroit garantira également que nous affichons des messages significatifs pour nos utilisateurs finaux.

Abordons ces quatre problèmes en refactorisant notre projet.

### Séparation des Préoccupations dans les Projets Binaires

Le problème organisationnel d'allocation de responsabilités pour plusieurs tâches à la fonction `main` est commun à de nombreux projets binaires. En conséquence, de nombreux programmeurs Rust trouvent utile de séparer les préoccupations d'un programme binaire lorsque la fonction `main` commence à devenir grande. Ce processus comporte les étapes suivantes :

- Divisez votre programme en un fichier _main.rs_ et un fichier _lib.rs_ et déplacez la logique de votre programme vers _lib.rs_.
- Tant que votre logique d'analyse des commandes est petite, elle peut rester dans la fonction `main`.
- Lorsque la logique d'analyse des commandes devient compliquée, extrayez-la de la fonction `main` dans d'autres fonctions ou types.

Les responsabilités qui restent dans la fonction `main` après ce processus devraient être limitées aux éléments suivants :

- Appeler la logique d'analyse des commandes avec les valeurs des arguments
- Mettre en place toute autre configuration
- Appeler une fonction `run` dans _lib.rs_
- Gérer l'erreur si `run` renvoie une erreur

Ce modèle vise à séparer les préoccupations : _main.rs_ gère l'exécution du programme et _lib.rs_ gère toute la logique de la tâche en cours. Comme vous ne pouvez pas tester la fonction `main` directement, cette structure vous permet de tester toute la logique de votre programme en la déplaçant hors de la fonction `main`. Le code restant dans la fonction `main` sera assez petit pour que sa correction puisse être vérifiée en le lisant. Retravaillons notre programme en suivant ce processus.

#### Extraction du Parser d'Arguments

Nous allons extraire la fonctionnalité d'analyse des arguments dans une fonction que `main` appellera. La Liste 12-5 montre le nouveau début de la fonction `main` qui appelle une nouvelle fonction `parse_config`, que nous définirons dans _src/main.rs_.

Nous collectons toujours les arguments de ligne de commande dans un vecteur, mais au lieu d'assigner la valeur de l'argument à l'index 1 à la variable `query` et la valeur de l'argument à l'index 2 à la variable `file_path` au sein de la fonction `main`, nous passons tout le vecteur à la fonction `parse_config`. La fonction `parse_config` contient alors la logique qui détermine quel argument va dans quelle variable et renvoie les valeurs à `main`. Nous créons toujours les variables `query` et `file_path` dans `main`, mais `main` n'a plus la responsabilité de déterminer comment les arguments de ligne de commande et les variables correspondent.

Cette refonte peut sembler excessive pour notre petit programme, mais nous refactorisons par petites étapes incrémentales. Après avoir effectué ce changement, exécutez à nouveau le programme pour vérifier que l'analyse des arguments fonctionne toujours. Il est bon de vérifier vos progrès souvent, afin d'aider à identifier la cause des problèmes lorsqu'ils surviennent.

#### Regroupement des Valeurs de Configuration

Nous pouvons faire un autre petit pas pour améliorer la fonction `parse_config` davantage. Pour l'instant, nous renvoyons un tuple, mais ensuite nous décomposons immédiatement ce tuple en parties individuelles. C'est un signe qu'il y a peut-être une mauvaise abstraction.

Un autre indicateur qui montre qu'il y a une marge d'amélioration est la partie `config` de `parse_config`, qui implique que les deux valeurs que nous renvoyons sont liées et font toutes deux partie d'une seule valeur de configuration. Nous ne transmettons pas actuellement ce sens dans la structure des données, sinon en regroupant les deux valeurs dans un tuple ; nous allons donc plutôt mettre les deux valeurs dans une seule structure et donner à chaque champ de la structure un nom significatif. Cela facilitera la compréhension par les futurs mainteneurs de ce code de la relation entre les différentes valeurs et de leur objectif.

La Liste 12-6 montre les améliorations apportées à la fonction `parse_config`.

Nous avons ajouté une structure nommée `Config` définie pour avoir des champs nommés `query` et `file_path`. La signature de `parse_config` indique désormais qu'elle renvoie une valeur `Config`. Dans le corps de `parse_config`, où nous utilisions auparavant des tranches de chaînes qui font référence aux valeurs `String` dans `args`, nous définissons maintenant `Config` pour contenir des valeurs `String` possédées. La variable `args` dans `main` est le propriétaire des valeurs des arguments et ne laisse que la fonction `parse_config` y accéder, ce qui signifie que nous violerions les règles d'emprunt de Rust si `Config` essayait de prendre possession des valeurs dans `args`.

Il existe plusieurs façons de gérer les données `String` ; la plus simple, bien que quelque peu inefficace, consiste à appeler la méthode `clone` sur les valeurs. Cela fera une copie complète des données pour que l'instance de `Config` en prenne possession, ce qui nécessite plus de temps et de mémoire que le stockage d'une référence aux données de chaîne. Cependant, cloner les données rend également notre code très simple car nous n'avons pas à gérer la durée de vie des références ; dans ce cas, renoncer à un peu de performance pour gagner en simplicité est un compromis précieux.

> ### Les Compromis de l'Utilisation de `clone`
>
> Il existe une tendance parmi de nombreux Rustaceans à éviter d'utiliser `clone` pour résoudre des problèmes de propriété en raison de son coût d'exécution. Dans [le Chapitre 13][ch13], vous apprendrez à utiliser des méthodes plus efficaces dans ce type de situation. Mais pour l'instant, il est acceptable de copier quelques chaînes pour continuer à progresser car vous ne ferez ces copies qu'une seule fois et votre chemin de fichier et votre chaîne de requête sont très petits. Il est préférable d'avoir un programme fonctionnel qui est un peu inefficace que d'essayer d'hyper-optimiser le code dès le premier essai. À mesure que vous gagnerez en expérience avec Rust, il sera plus facile de commencer avec la solution la plus efficace, mais pour l'instant, il est parfaitement acceptable d'appeler `clone`.

Nous avons mis à jour `main` afin qu'il place l'instance de `Config` renvoyée par `parse_config` dans une variable nommée `config`, et nous avons mis à jour le code qui utilisait auparavant les variables séparées `query` et `file_path` pour qu'il utilise désormais les champs de la structure `Config à la place.

Maintenant, notre code indique plus clairement que `query` et `file_path` sont liés et que leur objectif est de configurer le fonctionnement du programme. Tout code utilisant ces valeurs sait où les trouver dans l'instance `config` dans les champs nommés en fonction de leur objectif.

#### Création d'un Constructeur pour `Config`

Jusqu'à présent, nous avons extrait la logique responsable de l'analyse des arguments de la fonction `main` et l'avons placée dans la fonction `parse_config`. Ce faisant, nous avons constaté que les valeurs `query` et `file_path` étaient liées, et que cette relation devait être transmise dans notre code. Nous avons ensuite ajouté une structure `Config` pour nommer le but lié de `query` et `file_path` et pouvoir renvoyer les noms des valeurs sous forme de noms de champs de la structure depuis la fonction `parse_config`.

Désormais que l'objectif de la fonction `parse_config` est de créer une instance `Config`, nous pouvons changer `parse_config` d'une fonction ordinaire en une fonction nommée `new` qui est associée à la structure `Config`. Ce changement rendra le code plus idiomatique. Nous pouvons créer des instances de types dans la bibliothèque standard, comme `String`, en appelant `String::new`. De même, en changeant `parse_config` en une fonction `new` associée à `Config`, nous pourrons créer des instances de `Config` en appelant `Config::new`. La Liste 12-7 montre les changements que nous devons apporter.

Nous avons mis à jour `main` où nous appelions `parse_config` pour appeler à la place `Config::new`. Nous avons changé le nom de `parse_config` en `new` et l'avons déplacé dans un bloc `impl`, ce qui associe la fonction `new` à `Config`. Essayez de compiler ce code à nouveau pour vous assurer qu'il fonctionne.

### Correction de la Gestion des Erreurs

Maintenant, nous allons travailler à corriger notre gestion des erreurs. Rappelons que tenter d'accéder aux valeurs dans le vecteur `args` à l'index 1 ou à l'index 2 entraînera un plantage du programme si le vecteur contient moins de trois éléments. Essayez d'exécuter le programme sans arguments ; il aura un aspect comme celui-ci :

La ligne `index out of bounds: the len is 1 but the index is 1` est un message d'erreur destiné aux programmeurs. Cela n'aidera pas nos utilisateurs à comprendre ce qu'ils devraient faire à la place. Corrigeons cela maintenant.

#### Amélioration du Message d'Erreur

Dans la Liste 12-8, nous ajoutons une vérification dans la fonction `new` qui vérifiera que la tranche est suffisamment longue avant d'accéder à l'index 1 et à l'index 2. Si la tranche n'est pas suffisamment longue, le programme se bloque et affiche un meilleur message d'erreur.

Ce code est similaire à la fonction `Guess::new` que nous avons écrite dans la Liste 9-13, où nous avons appelé `panic!` lorsque l'argument `value` était en dehors de la plage de valeurs valides. Au lieu de vérifier une plage de valeurs ici, nous vérifions que la longueur de `args` est au moins `3`, et le reste de la fonction peut fonctionner dans l'hypothèse que cette condition a été respectée. Si `args` a moins de trois éléments, cette condition sera `true`, et nous appelons la macro `panic!` pour mettre fin au programme immédiatement.

Avec ces quelques lignes supplémentaires de code dans `new`, exécutons à nouveau le programme sans arguments pour voir quel aspect a maintenant le message d'erreur :

Cette sortie est mieux : nous avons maintenant un message d'erreur raisonnable. Cependant, nous avons également des informations superflues que nous ne souhaitons pas communiquer à nos utilisateurs. Peut-être que la technique que nous avons utilisée dans la Liste 9-13 n'est-elle pas la meilleure pour nous ici : un appel à `panic!` est plus approprié pour un problème de programmation qu'un problème d'utilisation. Au lieu de cela, nous allons utiliser l'autre technique que vous avez apprise au Chapitre 9 : [renvoyer un `Result`] qui indique soit un succès soit une erreur.

#### Retourner un `Result` au Lieu d'Appeler `panic!`

Nous pouvons plutôt renvoyer une valeur `Result` qui contiendra une instance de `Config` en cas de succès et décrira le problème en cas d'erreur. Nous changeons également le nom de la fonction de `new` à `build` car de nombreux programmeurs s'attendent à ce que les fonctions `new` ne rencontrent jamais d'échec. Lorsque `Config::build` communique avec `main`, nous pouvons utiliser le type `Result` pour signaler qu'il y a eu un problème. Nous pouvons ensuite modifier `main` pour convertir un variant `Err` en une erreur plus pratique pour nos utilisateurs sans le texte environnant sur `thread 'main'` et `RUST_BACKTRACE` qu'un appel à `panic!` entraîne.

La Liste 12-9 montre les modifications que nous devons apporter à la valeur de retour de la fonction que nous appelons maintenant `Config::build` et au corps de la fonction nécessaire pour renvoyer un `Result`. Notez que cela ne compilera pas jusqu'à ce que nous mettions également à jour `main`, ce que nous ferons dans la prochaine liste.

Notre fonction `build` renvoie un `Result` avec une instance de `Config` dans le cas de succès et une chaîne littérale dans le cas d'erreur. Nos valeurs d'erreur seront toujours des chaînes littérales qui ont la durée de vie `'static`.

Nous avons apporté deux changements dans le corps de la fonction : au lieu d'appeler `panic!` lorsque l'utilisateur ne passe pas assez d'arguments, nous renvoyons maintenant une valeur `Err`, et nous avons enveloppé la valeur de retour `Config` dans un `Ok`. Ces modifications rendent la fonction conforme à sa nouvelle signature de type.

Retourner une valeur `Err` de `Config::build` permet à la fonction `main` de gérer la valeur `Result` renvoyée par la fonction `build` et de quitter le processus plus proprement en cas d'erreur.

#### Appel de `Config::build` et Gestion des Erreurs

Pour gérer le cas d'erreur et afficher un message convivial, nous devons mettre à jour `main` pour gérer le `Result` étant renvoyé par `Config::build`, comme montré dans la Liste 12-10. Nous allons également retirer la responsabilité de quitter l'outil de ligne de commande avec un code d'erreur non nul d'`panic!` et la mettre en œuvre manuellement. Un code de sortie non nul est une convention pour signaler au processus qui a appelé notre programme que le programme s'est terminé dans un état d'erreur.

Dans cette liste, nous avons utilisé une méthode que nous n'avons pas encore couverte en détail : `unwrap_or_else`, qui est définie sur `Result<T, E>` par la bibliothèque standard. Utiliser `unwrap_or_else` nous permet de définir une gestion des erreurs personnalisée, non `panic!`. Si le `Result` est une valeur `Ok`, le comportement de cette méthode est similaire à `unwrap` : elle renvoie la valeur interne que `Ok` enveloppe. Cependant, si la valeur est une `Err`, cette méthode appelle le code de la fermeture, qui est une fonction anonyme que nous définissons et passons comme argument à `unwrap_or_else`. Nous couvrirons les fermetures en détail dans [le Chapitre 13]. Pour l'instant, vous devez simplement savoir que `unwrap_or_else` passera la valeur interne de `Err`, qui dans ce cas est la chaîne statique `"not enough arguments"` que nous avons ajoutée dans la Liste 12-9, à notre fermeture dans l'argument `err` qui apparaît entre les barres verticales. Le code dans la fermeture peut ensuite utiliser la valeur `err` lorsqu'il s'exécute.

Nous avons ajouté une nouvelle ligne `use` pour amener `process` de la bibliothèque standard dans le scope. Le code dans la fermeture qui sera exécuté en cas d'erreur ne comporte que deux lignes : nous imprimons la valeur `err` puis appelons `process::exit`. La fonction `process::exit` arrêtera le programme immédiatement et renverra le nombre passé comme code de statut de sortie. C'est similaire à la gestion basée sur `panic!` que nous avons utilisée dans la Liste 12-8, mais nous n'obtenons plus toute la sortie supplémentaire. Essayons :

Super ! Cette sortie est beaucoup plus amicale pour nos utilisateurs.

### Extraction de la Logique de la Fonction `main`

Maintenant que nous avons terminé de refactoriser l'analyse de la configuration, tournons-nous vers la logique du programme. Comme nous l'avons déclaré dans [« Séparation des Préoccupations dans les Projets Binaires »], nous allons extraire une fonction nommée `run` qui contiendra toute la logique actuelle de la fonction `main` qui n'est pas impliquée dans la mise en place de la configuration ou la gestion des erreurs. Une fois que nous aurons terminé, la fonction `main` sera concise et facile à vérifier par inspection, et nous pourrons écrire des tests pour toute la logique restante.

La Liste 12-11 montre l'amélioration incrémentale et petite de l'extraction d'une fonction `run`.

La fonction `run` contient désormais toute la logique restante de `main`, à partir de la lecture du fichier. La fonction `run` prend l'instance de `Config` comme argument.

#### Retourner des Erreurs de la Fonction `run`

Avec la logique restante du programme séparée dans la fonction `run`, nous pouvons améliorer la gestion des erreurs, comme nous l'avons fait avec `Config::build` dans la Liste 12-9. Au lieu de permettre au programme de planter en appelant `expect`, la fonction `run` renverra un `Result<T, E>` lorsqu'un problème survient. Cela nous permettra de consolider davantage la logique autour de la gestion des erreurs dans `main` de manière conviviale. La Liste 12-12 montre les changements que nous devons apporter à la signature et au corps de `run`.

Nous avons effectué trois changements significatifs ici. Tout d'abord, nous avons changé le type de retour de la fonction `run` en `Result<(), Box<dyn Error>>`. Cette fonction renvoyait auparavant le type unitaire `()`, et nous le conservons comme la valeur renvoyée dans le cas de succès.

Pour le type d'erreur, nous avons utilisé l'objet de trait `Box<dyn Error>` (et nous avons amené `std::error::Error` dans le scope avec une ligne `use` au sommet). Nous couvrirons les objets de trait dans [le Chapitre 18]. Pour l'instant, sachez simplement que `Box<dyn Error>` signifie que la fonction renverra un type qui implémente le trait `Error`, mais nous n'avons pas à spécifier quel type particulier la valeur de retour sera. Cela nous donne la flexibilité de renvoyer des valeurs d'erreur qui peuvent être de différents types dans différents cas d'erreur. Le mot-clé `dyn` est une abrégé pour _dynamique_.

Deuxièmement, nous avons supprimé l'appel à `expect` en faveur de l'opérateur `?`, comme nous l'avons mentionné dans [le Chapitre 9]. Plutôt que de faire un `panic!` sur une erreur, `?` renverra la valeur d'erreur de la fonction actuelle pour que l'appelant puisse la gérer.

Troisièmement, la fonction `run` renvoie désormais une valeur `Ok` en cas de succès. Nous avons déclaré le type de succès de la fonction `run` comme `()` dans la signature, ce qui signifie que nous devons envelopper la valeur de type unitaire dans la valeur `Ok`. Cette syntaxe `Ok(())` peut sembler un peu étrange au début. Mais utiliser `()` de cette manière est la façon idiomatique d'indiquer que nous appelons `run` uniquement pour ses effets secondaires ; elle ne renvoie pas une valeur dont nous avons besoin.

Lorsque vous exécutez ce code, il compilera mais affichera un avertissement :

Rust nous dit que notre code a ignoré la valeur `Result` et que cette valeur pourrait indiquer qu'une erreur s'est produite. Mais nous ne vérifions pas si une erreur s'est produite ou non, et le compilateur nous rappelle que nous voulions probablement avoir du code de gestion des erreurs ici ! Corrigeons ce problème maintenant.

#### Gestion des Erreurs Renvoyées par `run` dans `main`

Nous allons vérifier les erreurs et les gérer à l'aide d'une technique similaire à celle que nous avons utilisée avec `Config::build` dans la Liste 12-10, mais avec une légère différence :

Nous utilisons `if let` plutôt qu`'unwrap_or_else` pour vérifier si `run` renvoie une valeur `Err` et appeler `process::exit(1)` si c'est le cas. La fonction `run` ne renvoie pas une valeur que nous voulons `unwrap` de la même manière que `Config::build` renvoie l'instance de `Config`. Étant donné que `run` renvoie `()` dans le cas de succès, nous ne nous soucions que de détecter une erreur, donc nous n'avons pas besoin d'utiliser `unwrap_or_else` pour renvoyer la valeur décompressée, qui serait uniquement `()`.

Les corps des fonctions `if let` et `unwrap_or_else` sont identiques dans les deux cas : nous imprimons l'erreur et sortons.

### Division du Code en un Crate de Bibliothèque

Notre projet `minigrep` est encore meilleur jusqu'à présent ! Maintenant, nous allons diviser le fichier _src/main.rs_ et déplacer du code dans le fichier _src/lib.rs_. De cette façon, nous pourrons tester le code et avoir un fichier _src/main.rs_ avec moins de responsabilités.

Définissons la fonction `search` responsable de la recherche de texte dans _src/lib.rs_ plutôt que dans _src/main.rs_, ce qui nous permettra (ou à quiconque utilisant notre bibliothèque `minigrep`) d'appeler la fonction de recherche depuis plus de contextes que notre binaire `minigrep`.

D'abord, définissons la signature de la fonction `search` dans _src/lib.rs_ comme montré dans la Liste 12-13, avec un corps qui appelle la macro `unimplemented!`. Nous expliquerons la signature plus en détail lorsque nous remplirons l'implémentation.

Nous avons utilisé le mot-clé `pub` dans la définition de la fonction pour désigner `search` comme faisant partie de l'API publique de notre crate de bibliothèque. Nous avons maintenant une crate de bibliothèque que nous pouvons utiliser depuis notre crate binaire et que nous pouvons tester !

Maintenant, nous devons amener le code défini dans _src/lib.rs_ dans le scope de la crate binaire dans _src/main.rs_ et l'appeler, comme montré dans la Liste 12-14.

Nous ajoutons une ligne `use minigrep::search` pour amener la fonction `search` de la crate de bibliothèque dans le scope de la crate binaire. Ensuite, dans la fonction `run`, au lieu d'afficher le contenu du fichier, nous appelons la fonction `search` et transmettons les valeurs `config.query` et `contents` comme arguments. La fonction `run` utilisera ensuite une boucle `for` pour imprimer chaque ligne renvoyée par `search` qui correspond à la requête. C'est aussi un bon moment pour supprimer les appels `println!` dans la fonction `main` qui affichent la requête et le chemin de fichier afin que notre programme n'affiche que les résultats de recherche (si aucune erreur ne se produit).

Notez que la fonction de recherche collectera tous les résultats dans un vecteur qu'elle renvoie avant que n'importe quelle impression ne se produise. Cette implémentation pourrait être lente pour afficher des résultats lors de recherches dans de grands fichiers, car les résultats ne sont pas imprimés à mesure qu'ils sont trouvés ; nous discuterons d'un moyen possible de corriger cela en utilisant des itérateurs dans le Chapitre 13.

Ouf ! Cela a été beaucoup de travail, mais nous nous sommes mis en bonne position pour réussir à l'avenir. Désormais, il est beaucoup plus facile de gérer les erreurs, et nous avons rendu le code plus modulaire. Presque tout notre travail se fera dans _src/lib.rs_ à partir de maintenant.

Profitons de cette nouvelle modularité en faisant quelque chose qui aurait été difficile avec l'ancien code mais qui est facile avec le nouveau code : nous allons écrire quelques tests !