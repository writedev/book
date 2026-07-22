<!-- Old headings. Do not remove or links may break. -->

<a id="tourner-notre-serveur-à-fil-simple-en-un-serveur-multithread"></a>
<a id="de-serveur-à-fil-simple-à-multithread"></a>

## De Serveur à Fil Simple à Serveur Multithread

Actuellement, le serveur traitera chaque requête à son tour, ce qui signifie qu'il ne traitera pas une seconde connexion tant que la première connexion n'est pas terminée. Si le serveur reçoit de plus en plus de requêtes, cette exécution séquentielle deviendra de moins en moins optimale. Si le serveur reçoit une requête qui prend beaucoup de temps à traiter, les requêtes suivantes devront attendre jusqu'à ce que la longue requête soit terminée, même si les nouvelles requêtes peuvent être traitées rapidement. Nous devrons corriger cela, mais d'abord, nous examinerons le problème en action.

<!-- Old headings. Do not remove or links may break. -->

<a id="simuler-une-requête-lente-dans-l-implémentation-actuelle-du-serveur"></a>

### Simuler une Requête Lente

Nous allons voir comment une requête de traitement lent peut affecter d'autres requêtes envoyées à notre implémentation actuelle du serveur. Le Listing 21-10 implémente la gestion d'une requête à _/sleep_ avec une réponse lente simulée qui fera que le serveur dormira pendant cinq secondes avant de répondre.

<Listing number="21-10" file-name="src/main.rs" caption="Simuler une requête lente en dormant pendant cinq secondes">

```rust,no_run
{{#rustdoc_include ../listings/ch21-web-server/listing-21-10/src/main.rs:here}}
```

</Listing>

Nous avons changé de `if` à `match` maintenant que nous avons trois cas. Nous devons explicitement faire correspondre un élément de `request_line` pour effectuer une correspondance de modèle avec les valeurs littérales de chaîne ; `match` ne fait pas de référence automatique et de désérialisation, comme le fait la méthode d'égalité.

Le premier axe est le même que le bloc `if` du Listing 21-9. Le deuxième axe fait correspondre une requête à _/sleep_. Lorsque cette requête est reçue, le serveur s'endormira pendant cinq secondes avant de rendre la page HTML réussie. Le troisième axe est identique au bloc `else` du Listing 21-9.

Vous pouvez voir à quel point notre serveur est primitif : De vraies bibliothèques géreraient la reconnaissance de plusieurs requêtes d'une manière beaucoup moins verbeuse !

Démarrez le serveur en utilisant `cargo run`. Ensuite, ouvrez deux fenêtres de navigateur : une pour _http://127.0.0.1:7878_ et l'autre pour _http://127.0.0.1:7878/sleep_. Si vous entrez plusieurs fois l'URI _/_ comme auparavant, vous verrez qu'il répond rapidement. Mais si vous entrez _/sleep_ puis chargez _/_ , vous verrez que _/_ attend que `sleep` ait dormi pendant ses cinq secondes complètes avant de se charger.

Il existe plusieurs techniques que nous pourrions utiliser pour éviter que les requêtes ne s'accumulent derrière une requête lente, y compris l'utilisation d'async comme nous l'avons fait au Chapitre 17 ; celle que nous allons mettre en œuvre est un pool de threads.

### Améliorer le Débit avec un Pool de Threads

Un _pool de threads_ est un groupe de threads créés qui sont prêts et attendent de gérer une tâche. Lorsque le programme reçoit une nouvelle tâche, il attribue l'une des threads du pool à la tâche, et ce thread traitera la tâche. Les autres threads du pool sont disponibles pour gérer d'autres tâches qui arrivent pendant que le premier thread traite la tâche. Lorsque le premier thread a terminé de traiter sa tâche, il est retourné au pool de threads inactifs, prêt à gérer une nouvelle tâche. Un pool de threads vous permet de traiter les connexions de manière concurrente, augmentant le débit de votre serveur.

Nous limiterons le nombre de threads dans le pool à un petit nombre pour nous protéger contre les attaques DoS ; si nous faisions en sorte que notre programme crée un nouveau thread pour chaque requête à mesure qu'elle arrivait, quelqu'un effectuant 10 millions de requêtes sur notre serveur pourrait causer des ravages en utilisant toutes les ressources de notre serveur et en arrêtant le traitement des requêtes.

Plutôt que de lancer un nombre illimité de threads, nous aurons un nombre fixe de threads en attente dans le pool. Les requêtes qui arrivent sont envoyées au pool pour traitement. Le pool maintiendra une file d'attente de requêtes entrantes. Chacune des threads dans le pool retirera une requête de cette file, gérera la requête, puis demandera à la file une autre requête. Avec ce design, nous pouvons traiter jusqu'à _`N`_ requêtes de manière concurrente, où _`N`_ est le nombre de threads. Si chaque thread répond à une requête de longue durée, les requêtes suivantes peuvent toujours s'accumuler dans la file, mais nous avons augmenté le nombre de requêtes de longue durée que nous pouvons gérer avant d'atteindre ce point.

Cette technique n'est qu'une des nombreuses façons d'améliorer le débit d'un serveur web. D'autres options que vous pouvez explorer sont le modèle fork/join, le modèle I/O asynchrone à thread unique et le modèle I/O asynchrone multithread. Si ce sujet vous intéresse, vous pouvez en lire davantage sur d'autres solutions et essayer de les mettre en œuvre ; avec un langage de bas niveau comme Rust, toutes ces options sont possibles.

Avant de commencer à implémenter un pool de threads, parlons de ce à quoi devrait ressembler l'utilisation du pool. Lorsque vous essayez de concevoir du code, écrire d'abord l'interface client peut aider à guider votre conception. Écrivez l'API du code afin qu'elle soit structurée de la manière dont vous souhaitez l'appeler ; puis, mettez en œuvre la fonctionnalité au sein de cette structure plutôt que d'implémenter la fonctionnalité, puis de concevoir l'API publique.

Similaire à la manière dont nous avons utilisé le développement piloté par les tests dans le projet du Chapitre 12, nous utiliserons le développement piloté par le compilateur ici. Nous allons écrire le code qui appelle les fonctions que nous voulons, puis nous examinerons les erreurs du compilateur pour déterminer ce que nous devrions changer ensuite pour que le code fonctionne. Avant de faire cela, cependant, nous allons explorer la technique que nous n'allons pas utiliser comme point de départ.

<!-- Old headings. Do not remove or links may break. -->

<a id="structure-du-code-si-nous-pouvions-lancer-un-thread-pour-chaque-requête"></a>

#### Lancer un Thread pour Chaque Requête

Tout d'abord, explorons à quoi pourrait ressembler notre code s'il créait un nouveau thread pour chaque connexion. Comme mentionné précédemment, ce n'est pas notre plan final en raison des problèmes de lancement potentiel d'un nombre illimité de threads, mais c'est un point de départ pour obtenir un serveur multithread fonctionnel en premier. Ensuite, nous ajouterons le pool de threads comme amélioration, et il sera plus facile de contraster les deux solutions.

Le Listing 21-11 montre les modifications à apporter à `main` pour lancer un nouveau thread pour gérer chaque flux dans la boucle `for`.

<Listing number="21-11" file-name="src/main.rs" caption="Lancement d'un nouveau thread pour chaque flux">

```rust,no_run
{{#rustdoc_include ../listings/ch21-web-server/listing-21-11/src/main.rs:here}}
```

</Listing>

Comme vous l'avez appris au Chapitre 16, `thread::spawn` créera un nouveau thread puis exécutera le code dans la fermeture dans le nouveau thread. Si vous exécutez ce code et chargez _/sleep_ dans votre navigateur, puis _/_ dans deux autres onglets de navigateur, vous verrez en effet que les requêtes à _/_ n'ont pas à attendre que _/sleep_ soit terminé. Cependant, comme nous l'avons mentionné, cela finira par submerger le système car vous créeriez de nouveaux threads sans aucune limite.

Vous vous souvenez peut-être également du Chapitre 17 que c'est exactement le genre de situation où async et await brillent vraiment ! Gardez cela à l'esprit alors que nous construisons le pool de threads et réfléchissons à la façon dont les choses sembleraient différentes ou similaires avec async.

<!-- Old headings. Do not remove or links may break. -->

<a id="création-d-une-interface-similaire-pour-un-nombre-fini-de-threads"></a>

#### Création d'un Nombre Fini de Threads

Nous voulons que notre pool de threads fonctionne de manière similaire et familière afin que le passage des threads à un pool de threads ne nécessite pas de grands changements au code qui utilise notre API. Le Listing 21-12 montre l'interface hypothétique pour une structure `ThreadPool` que nous voulons utiliser à la place de `thread::spawn`.

<Listing number="21-12" file-name="src/main.rs" caption="Notre interface idéale `ThreadPool`">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch21-web-server/listing-21-12/src/main.rs:here}}
```

</Listing>

Nous utilisons `ThreadPool::new` pour créer un nouveau pool de threads avec un nombre configurable de threads, dans ce cas quatre. Ensuite, dans la boucle `for`, `pool.execute` a une interface similaire à `thread::spawn` en ce sens qu'elle prend une fermeture que le pool doit exécuter pour chaque flux. Nous devons implémenter `pool.execute` afin qu'il prenne la fermeture et la donne à un thread dans le pool pour l'exécuter. Ce code ne compilera pas encore, mais nous allons essayer afin que le compilateur puisse nous guider sur la façon de le corriger.

<!-- Old headings. Do not remove or links may break. -->

<a id="construction-de-la-structure-threadpool-en-utilisant-le-développement-piloté-par-le-compilateur"></a>

#### Construction de `ThreadPool` en Utilisant le Développement Piloté par le Compilateur

Apportez les modifications du Listing 21-12 à _src/main.rs_, puis utilisons les erreurs du compilateur de `cargo check` pour guider notre développement. Voici la première erreur que nous obtenons :

```console
{{#include ../listings/ch21-web-server/listing-21-12/output.txt}}
```

Génial ! Cette erreur nous dit que nous avons besoin d'un type ou d'un module `ThreadPool`, donc nous allons en construire un maintenant. Notre implémentation de `ThreadPool` sera indépendante du type de travail que notre serveur web effectue. Donc, convertissons le crate `hello` d'un crate binaire en un crate de bibliothèque pour contenir notre implémentation de `ThreadPool`. Après avoir changé pour un crate de bibliothèque, nous pourrions également utiliser la bibliothèque de pool de threads séparée pour tout travail que nous souhaitons effectuer en utilisant un pool de threads, pas seulement pour servir des requêtes web.

Créez un fichier _src/lib.rs_ contenant ce qui suit, qui est la définition la plus simple d'une structure `ThreadPool` que nous pouvons avoir pour l'instant :

<Listing file-name="src/lib.rs">

```rust,noplayground
{{#rustdoc_include ../listings/ch21-web-server/no-listing-01-define-threadpool-struct/src/lib.rs}}
```

</Listing>

Ensuite, modifiez le fichier _main.rs_ pour importer `ThreadPool` depuis le crate de bibliothèque en ajoutant le code suivant en haut de _src/main.rs_ :

<Listing file-name="src/main.rs">

```rust,ignore
{{#rustdoc_include ../listings/ch21-web-server/no-listing-01-define-threadpool-struct/src/main.rs:here}}
```

</Listing>

Ce code ne fonctionnera toujours pas, mais vérifions-le à nouveau pour obtenir la prochaine erreur que nous devons résoudre :

```console
{{#include ../listings/ch21-web-server/no-listing-01-define-threadpool-struct/output.txt}}
```

Cette erreur indique que nous devons maintenant créer une fonction associée nommée `new` pour `ThreadPool`. Nous savons également que `new` doit avoir un paramètre qui peut accepter `4` comme argument et doit retourner une instance de `ThreadPool`. Implémentons la fonction `new` la plus simple qui aura ces caractéristiques :

<Listing file-name="src/lib.rs">

```rust,noplayground
{{#rustdoc_include ../listings/ch21-web-server/no-listing-02-impl-threadpool-new/src/lib.rs}}
```

</Listing>

Nous avons choisi `usize` comme type du paramètre `size` car nous savons qu'un nombre négatif de threads n'a pas de sens. Nous savons également que nous utiliserons ce `4` comme nombre d'éléments dans une collection de threads, ce qui est ce pour quoi le type `usize` est destiné, comme discuté dans la section [« Types Entiers »][integer-types]<!-- ignore --> du Chapitre 3.

Vérifions à nouveau le code :

```console
{{#include ../listings/ch21-web-server/no-listing-02-impl-threadpool-new/output.txt}}
```

Maintenant, l'erreur se produit parce que nous n'avons pas de méthode `execute` sur `ThreadPool`. Rappelez-vous de la section [« Création d'un Nombre Fini de Threads »](#creating-a-finite-number-of-threads)<!-- ignore --> où nous avons décidé que notre pool de threads devrait avoir une interface similaire à `thread::spawn`. De plus, nous allons implémenter la fonction `execute` afin qu'elle prenne la fermeture qu'on lui donne et la transmette à un thread inactif du pool pour qu'il l'exécute.

Nous allons définir la méthode `execute` sur `ThreadPool` pour qu'elle prenne une fermeture comme paramètre. Rappelez-vous de la section [« Déplacer les Valeurs Capturées Hors des Fermetures »][moving-out-of-closures]<!-- ignore --> dans le Chapitre 13 que nous pouvons prendre des fermetures comme paramètres avec trois traits différents : `Fn`, `FnMut`, et `FnOnce`. Nous devons décider quel type de fermeture utiliser ici. Nous savons que nous allons finalement faire quelque chose de similaire à l'implémentation standard de `thread::spawn`, donc nous pouvons regarder quels types de contraintes a la signature de `thread::spawn` sur son paramètre. La documentation nous montre ce qui suit :

```rust,ignore
pub fn spawn<F, T>(f: F) -> JoinHandle<T>
    where
        F: FnOnce() -> T,
        F: Send + 'static,
        T: Send + 'static,
```

Le paramètre de type `F` est celui qui nous intéresse ici ; le paramètre de type `T` est lié à la valeur de retour, et cela ne nous préoccupe pas. Nous pouvons voir que `spawn` utilise `FnOnce` comme contrainte de trait sur `F`. C'est probablement ce que nous voulons également, car nous allons finalement passer l'argument que nous obtenons dans `execute` à `spawn`. Nous pouvons être encore plus confiants que `FnOnce` est le trait que nous voulons utiliser car le thread exécutant une requête n'exécutera la fermeture de cette requête qu'une seule fois, ce qui correspond à `Once` dans `FnOnce`.

Le paramètre de type `F` a également la contrainte de trait `Send` et la contrainte de durée de vie `'static`, qui sont utiles dans notre situation : nous avons besoin de `Send` pour transférer la fermeture d'un thread à un autre et de `'static` car nous ne savons pas combien de temps le thread prendra pour s'exécuter. Créons une méthode `execute` sur `ThreadPool` qui prendra un paramètre générique de type `F` avec ces contraintes :

<Listing file-name="src/lib.rs">

```rust,noplayground
{{#rustdoc_include ../listings/ch21-web-server/no-listing-03-define-execute/src/lib.rs:here}}
```

</Listing>

Nous utilisons toujours `()` après `FnOnce` car ce `FnOnce` représente une fermeture qui ne prend pas de paramètres et renvoie le type unité `()`. Comme pour les définitions de fonctions, le type de retour peut être omis dans la signature, mais même si nous n'avons pas de paramètres, nous avons toujours besoin des parenthèses.

Encore une fois, il s'agit de la mise en œuvre la plus simple de la méthode `execute` : elle ne fait rien, mais nous essayons seulement de faire compiler notre code. Vérifions-le à nouveau :

```console
{{#include ../listings/ch21-web-server/no-listing-03-define-execute/output.txt}}
```

Il compile ! Mais notez que si vous essayez `cargo run` et faites une requête dans le navigateur, vous verrez les erreurs dans le navigateur que nous avons vues au début du chapitre. Notre bibliothèque n'appelle pas encore réellement la fermeture passée à `execute` !

> Remarque : Un dicton que vous pourriez entendre sur les langages avec des compilateurs stricts, comme Haskell et Rust, est « Si le code compile, il fonctionne. » Mais ce dicton n'est pas universellement vrai. Notre projet compile, mais il ne fait absolument rien ! Si nous construisions un vrai projet complet, ce serait un bon moment pour commencer à écrire des tests unitaires pour vérifier que le code compile _et_ a le comportement que nous voulons.

Considérez : Qu'est-ce qui serait différent ici si nous devions exécuter un futur plutôt qu'une fermeture ?

#### Validation du Nombre de Threads dans `new`

Nous ne faisons rien avec les paramètres de `new` et `execute`. Implémentons les corps de ces fonctions avec le comportement que nous voulons. Pour commencer, pensons à `new`. Plus tôt, nous avons choisi un type non signé pour le paramètre `size` parce qu'un pool avec un nombre négatif de threads n'a aucun sens. Cependant, un pool avec zéro threads n'a également aucun sens, mais zéro est un `usize` parfaitement valide. Nous allons ajouter du code pour vérifier que `size` est supérieur à zéro avant de retourner une instance de `ThreadPool`, et nous ferons en sorte que le programme panique s'il reçoit un zéro en utilisant la macro `assert!`, comme le montre le Listing 21-13.

<Listing number="21-13" file-name="src/lib.rs" caption="Implémentation de `ThreadPool::new` pour paniquer si `size` est zéro">

```rust,noplayground
{{#rustdoc_include ../listings/ch21-web-server/listing-21-13/src/lib.rs:here}}
```

</Listing>

Nous avons également ajouté de la documentation pour notre `ThreadPool` avec des commentaires doc. Notez que nous avons suivi de bonnes pratiques de documentation en ajoutant une section qui mentionne les situations dans lesquelles notre fonction peut paniquer, comme discuté au Chapitre 14. Essayez d'exécuter `cargo doc --open` et cliquez sur la structure `ThreadPool` pour voir à quoi ressemblent la documentation générée pour `new` !

Plutôt que d'ajouter la macro `assert!` comme nous l'avons fait ici, nous pourrions transformer `new` en `build` et renvoyer un `Result` comme nous l'avons fait avec `Config::build` dans le projet I/O au Listing 12-9. Mais nous avons décidé dans ce cas que tenter de créer un pool de threads sans aucun thread devrait être une erreur irréparable. Si vous vous sentez ambitieux, essayez d'écrire une fonction nommée `build` avec la signature suivante pour la comparer avec la fonction `new` :

```rust,ignore
pub fn build(size: usize) -> Result<ThreadPool, PoolCreationError> {
```

#### Création d'Espace pour Stocker les Threads

Maintenant que nous avons un moyen de savoir que nous avons un nombre valide de threads à stocker dans le pool, nous pouvons créer ces threads et les stocker dans la structure `ThreadPool` avant de retourner la structure. Mais comment « stocker » un thread ? Revoyons à nouveau la signature de `thread::spawn` :

```rust,ignore
pub fn spawn<F, T>(f: F) -> JoinHandle<T>
    where
        F: FnOnce() -> T,
        F: Send + 'static,
        T: Send + 'static,
```

La fonction `spawn` retourne un `JoinHandle<T>`, où `T` est le type que renvoie la fermeture. Essayons également d'utiliser `JoinHandle` et voyons ce qui se passe. Dans notre cas, les fermetures que nous passons au pool de threads géreront la connexion et ne renverront rien, donc `T` sera le type unité `()`.

Le code du Listing 21-14 va compiler, mais il ne crée pas encore de threads. Nous avons changé la définition de `ThreadPool` pour contenir un vecteur d'instances `thread::JoinHandle<()>`, initialisé le vecteur avec une capacité de `size`, mis en place une boucle `for` qui exécutera du code pour créer les threads et retourner une instance de `ThreadPool` qui les contiendra.

<Listing number="21-14" file-name="src/lib.rs" caption="Création d'un vecteur pour que `ThreadPool` contienne les threads">

```rust,ignore,not_desired_behavior
{{#rustdoc_include ../listings/ch21-web-server/listing-21-14/src/lib.rs:here}}
```

</Listing>

Nous avons importé `std::thread` dans le crate de bibliothèque car nous utilisons `thread::JoinHandle` comme type des éléments du vecteur dans `ThreadPool`.

Une fois qu'une taille valide est reçue, notre `ThreadPool` crée un nouveau vecteur qui peut contenir `size` éléments. La fonction `with_capacity` effectue la même tâche que `Vec::new` mais avec une différence importante : elle pré-alloue de l'espace dans le vecteur. Parce que nous savons que nous devons stocker `size` éléments dans le vecteur, faire cette allocation à l'avance est légèrement plus efficace que d'utiliser `Vec::new`, qui redimensionne lui-même au fur et à mesure que des éléments sont insérés.

Lorsque vous exécutez à nouveau `cargo check`, il devrait réussir.

<!-- Old headings. Do not remove or links may break. -->
<a id ="un-structeur-de-travail-responsable-de-l-envoi-de-code-du-threadpool-à-un-thread"></a>

#### Envoi de Code du `ThreadPool` à un Thread

Nous avons laissé un commentaire dans la boucle `for` du Listing 21-14 concernant la création des threads. Ici, nous allons voir comment nous créons effectivement les threads. La bibliothèque standard fournit `thread::spawn` comme moyen de créer des threads, et `thread::spawn` s'attend à recevoir du code que le thread doit exécuter dès que le thread est créé. Cependant, dans notre cas, nous voulons créer les threads et les faire _attendre_ du code que nous enverrons plus tard. L'implémentation standard des threads ne comprend aucun moyen de le faire ; nous devons l'implémenter manuellement.

Nous allons mettre en œuvre ce comportement en introduisant une nouvelle structure de données entre le `ThreadPool` et les threads qui gérera ce nouveau comportement. Nous allons appeler cette structure de données _Worker_, ce qui est un terme courant dans les implémentations de pool. Le `Worker` récupère le code qui doit être exécuté et exécute le code dans son thread.

Pensez aux personnes travaillant dans la cuisine d'un restaurant : Les travailleurs attendent que des commandes arrivent de la part des clients, puis ils sont responsables de prendre ces commandes et de les remplir.

Au lieu de stocker un vecteur d'instances `JoinHandle<()>` dans le pool de threads, nous allons stocker des instances de la structure `Worker`. Chaque `Worker` stockera une seule instance `JoinHandle<()>`. Ensuite, nous allons implémenter une méthode sur `Worker` qui prendra une fermeture de code à exécuter et l'enverra au thread déjà en cours d'exécution pour l'exécution. Nous donnerons également à chaque `Worker` un `id` afin que nous puissions distinguer les différentes instances de `Worker` dans le pool lors de la journalisation ou du débogage.

Voici le nouveau processus qui se produira lorsque nous créerons un `ThreadPool`. Nous allons implémenter le code qui enverra la fermeture au thread après avoir configuré `Worker` de cette manière :

1. Définir une structure `Worker` qui contient un `id` et un `JoinHandle<()>`.
2. Changer `ThreadPool` pour contenir un vecteur d'instances `Worker`.
3. Définir une fonction `Worker::new` qui prend un numéro `id` et retourne une instance `Worker` qui contient l`'id` et un thread créé avec une fermeture vide.
4. Dans `ThreadPool::new`, utiliser le compteur de boucle `for` pour générer un `id`, créer un nouveau `Worker` avec cet `id`, et stocker le `Worker` dans le vecteur.

Si vous vous sentez prêt pour un défi, essayez d'implémenter ces changements par vous-même avant de regarder le code du Listing 21-15.

Prêt ? Voici le Listing 21-15 avec une façon de faire les modifications précédentes.

<Listing number="21-15" file-name="src/lib.rs" caption="Modification de `ThreadPool` pour contenir des instances de `Worker` au lieu de contenir des threads directement">

```rust,noplayground
{{#rustdoc_include ../listings/ch21-web-server/listing-21-15/src/lib.rs:here}}
```

</Listing>

Nous avons changé le nom du champ sur `ThreadPool` de `threads` à `workers` car il contient maintenant des instances de `Worker` au lieu d'instances de `JoinHandle<()>`. Nous utilisons le compteur dans la boucle `for` comme argument pour `Worker::new`, et nous stockons chaque nouveau `Worker` dans le vecteur nommé `workers`.

Le code externe (comme notre serveur dans _src/main.rs_) n'a pas besoin de connaître les détails d'implémentation concernant l'utilisation d'une structure `Worker` au sein de `ThreadPool`, nous rendons donc la structure `Worker` et sa fonction `new` privées. La fonction `Worker::new` utilise l'`id` que nous lui donnons et stocke une instance de `JoinHandle<()>` qui est créée en lançant un nouveau thread avec une fermeture vide.

> Remarque : Si le système d'exploitation ne peut pas créer un thread parce qu'il n'y a pas assez de ressources système, `thread::spawn` panique. Cela fera paniquer notre serveur entier, même si la création de certains threads pourrait réussir. Pour des raisons de simplicité, ce comportement est acceptable, mais dans une implémentation de pool de threads en production, vous voudriez probablement utiliser [`std::thread::Builder`][builder]<!-- ignore --> et sa méthode [`spawn`][builder-spawn]<!-- ignore --> qui retourne un `Result`.

Ce code va compiler et stockera le nombre d'instances `Worker` que nous avons spécifié comme argument pour `ThreadPool::new`. Mais nous ne traitons _toujours pas_ la fermeture que nous obtenons dans `execute`. Voyons comment le faire ensuite.

#### Envoi de Requêtes aux Threads via des Canaux

Le prochain problème que nous allons aborder est que les fermetures données à `thread::spawn` ne font absolument rien. Actuellement, nous obtenons la fermeture que nous voulons exécuter dans la méthode `execute`. Mais nous devons donner à `thread::spawn` une fermeture à exécuter lorsque nous créons chaque `Worker` durant la création du `ThreadPool`.

Nous voulons que les structures `Worker` que nous venons de créer récupèrent le code à exécuter à partir d'une file d'attente détenue dans le `ThreadPool` et envoient ce code à son thread pour l'exécution.

Les canaux que nous avons appris au Chapitre 16 - un moyen simple de communiquer entre deux threads - seraient parfaits pour ce cas d'utilisation. Nous allons utiliser un canal pour fonctionner comme la file d'attente des travaux, et `execute` enverra un travail du `ThreadPool` aux instances de `Worker`, qui enverront le travail à son thread. Voici le plan :

1. Le `ThreadPool` créera un canal et gardera l'émetteur.
2. Chaque `Worker` conservera le récepteur.
3. Nous créerons une nouvelle structure `Job` qui contiendra les fermetures que nous voulons envoyer via le canal.
4. La méthode `execute` enverra le travail qu'elle souhaite exécuter via l'émetteur.
5. Dans son thread, le `Worker` bouclera sur son récepteur et exécutera les fermetures de tout travail qu'il recevra.

Commençons par créer un canal dans `ThreadPool::new` et garder l'émetteur dans l'instance de `ThreadPool`, comme indiqué dans le Listing 21-16. La structure `Job` ne conserve rien pour l'instant mais sera le type d'élément que nous envoyons via le canal.

<Listing number="21-16" file-name="src/lib.rs" caption="Modification de `ThreadPool` pour stocker l'émetteur d'un canal qui transmet des instances `Job`">

```rust,noplayground
{{#rustdoc_include ../listings/ch21-web-server/listing-21-16/src/lib.rs:here}}
```

</Listing>

Dans `ThreadPool::new`, nous créons notre nouveau canal et faisons en sorte que le pool conserve l'émetteur. Cela compilera avec succès.

Essayons de passer un récepteur du canal à chaque `Worker` pendant que le pool de threads crée le canal. Nous savons que nous voulons utiliser le récepteur dans le thread que les instances `Worker` lancent, donc nous allons référencer le paramètre `receiver` dans la fermeture. Le code du Listing 21-17 ne compilera pas encore tout à fait.

<Listing number="21-17" file-name="src/lib.rs" caption="Passage du récepteur à chaque `Worker`">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch21-web-server/listing-21-17/src/lib.rs:here}}
```

</Listing>

Nous avons apporté quelques modifications petites et simples : Nous passons le récepteur à `Worker::new`, puis nous l'utilisons à l'intérieur de la fermeture.

Lorsque nous essayons de vérifier ce code, nous obtenons cette erreur :

```console
{{#include ../listings/ch21-web-server/listing-21-17/output.txt}}
```

Le code essaie de passer le `receiver` à plusieurs instances de `Worker`. Cela ne fonctionnera pas, comme vous vous en souvenez du Chapitre 16 : L'implémentation du canal que Rust fournit est à produit multiple, consommateur unique. Cela signifie que nous ne pouvons pas simplement cloner l'extrémité consommante du canal pour corriger ce code. De plus, nous ne voulons pas envoyer un message plusieurs fois à plusieurs consommateurs ; nous voulons une seule liste de messages avec plusieurs instances de `Worker` de sorte que chaque message soit traité une fois.

De plus, retirer un travail de la file d'attente du canal implique de modifier le `receiver`, donc les threads ont besoin d'un moyen sûr de partager et de modifier le `receiver` ; autrement, nous pourrions avoir des conditions de course (comme couvertes dans le Chapitre 16).

Rappelez-vous des pointeurs intelligents thread-sûrs discutés au Chapitre 16 : Pour partager la propriété entre plusieurs threads et permettre aux threads de modifier la valeur, nous devons utiliser `Arc<Mutex<T>>`. Le type `Arc` permettra à plusieurs instances de `Worker` de posséder le récepteur, et `Mutex` garantira qu'un seul `Worker` obtient un travail du récepteur à la fois. Le Listing 21-18 montre les modifications que nous devons apporter.

<Listing number="21-18" file-name="src/lib.rs" caption="Partage du récepteur entre les instances `Worker` en utilisant `Arc` et `Mutex`">

```rust,noplayground
{{#rustdoc_include ../listings/ch21-web-server/listing-21-18/src/lib.rs:here}}
```

</Listing>

Dans `ThreadPool::new`, nous mettons le récepteur dans un `Arc` et un `Mutex`. Pour chaque nouveau `Worker`, nous clonons l'`Arc` pour augmenter le compte de référence afin que les instances `Worker` puissent partager la propriété du récepteur.

Avec ces changements, le code compile ! Nous progressons !

#### Implémentation de la Méthode `execute`

Implémentons enfin la méthode `execute` sur `ThreadPool`. Nous allons également changer `Job` d'une structure à un alias de type pour un objet de trait qui contient le type de fermeture que `execute` reçoit. Comme discuté dans la section [« Synonymes de Type et Alias de Type »][type-aliases]<!-- ignore --> du Chapitre 20, les alias de type nous permettent de raccourcir des types longs pour faciliter l'utilisation. Regardez le Listing 21-19.

<Listing number="21-19" file-name="src/lib.rs" caption="Création d'un alias de type `Job` pour un `Box` qui contient chaque fermeture et ensuite envoi du travail via le canal">

```rust,noplayground
{{#rustdoc_include ../listings/ch21-web-server/listing-21-19/src/lib.rs:here}}
```

</Listing>

Après avoir créé une nouvelle instance `Job` en utilisant la fermeture que nous recevons dans `execute`, nous envoyons ce travail à l'extrémité d'envoi du canal. Nous appelons `unwrap` sur `send` pour le cas où l'envoi échoue. Cela peut arriver si, par exemple, nous arrêtons tous nos threads d'exécuter, ce qui signifie que l'extrémité recevant a arrêté de recevoir de nouveaux messages. Pour le moment, nous ne pouvons pas arrêter nos threads d'exécuter : Nos threads continuent à s'exécuter tant que le pool existe. La raison pour laquelle nous utilisons `unwrap` est que nous savons que le cas d'échec ne se produira pas, mais le compilateur ne le sait pas.

Mais nous n'avons pas tout à fait fini ! Dans le `Worker`, notre fermeture passée à `thread::spawn` ne fait toujours que _référencer_ l'extrémité recevant du canal. Au lieu de cela, nous avons besoin que la fermeture boucle indéfiniment, demandant l'extrémité recevant du canal pour un travail et exécutant le travail lorsqu'elle en reçoit un. Apportons le changement montré dans le Listing 21-20 à `Worker::new`.

<Listing number="21-20" file-name="src/lib.rs" caption="Réception et exécution des travaux dans le thread de l'instance `Worker`">

```rust,noplayground
{{#rustdoc_include ../listings/ch21-web-server/listing-21-20/src/lib.rs:here}}
```

</Listing>

Ici, nous appelons d'abord `lock` sur le `receiver` pour acquérir le mutex, puis nous appelons `unwrap` pour paniquer sur toute erreur. Acquérir un verrou peut échouer si le mutex est dans un état _empoisonné_, ce qui peut se produire si un autre thread a paniqué tout en tenant le verrou plutôt qu'en le libérant. Dans cette situation, appeler `unwrap` pour faire paniquer ce thread est la bonne chose à faire. N'hésitez pas à changer ce `unwrap` en un `expect` avec un message d'erreur significatif pour vous.

Si nous obtenons le verrou sur le mutex, nous appelons `recv` pour recevoir un `Job` du canal. Un dernier `unwrap` passe également les erreurs, car elles peuvent se produire si le thread tenant l'émetteur a été fermé, de la même manière que la méthode `send` renvoie `Err` si le récepteur se ferme.

L'appel à `recv` bloque, donc s'il n'y a pas de travail pour l'instant, le thread actuel attendra jusqu'à ce qu'un travail devienne disponible. Le `Mutex<T>` garantit qu'un seul thread `Worker` à la fois tente de demander un travail.

Notre pool de threads est maintenant dans un état de fonctionnement ! Faites un `cargo run` et faites quelques requêtes :

<!-- régénération-manuelle
cd listings/ch21-web-server/listing-21-20
cargo run
faire des requêtes à 127.0.0.1:7878
Impossible d'automatiser car la sortie dépend des requêtes faites
-->

```console
$ cargo run
   Compiling hello v0.1.0 (file:///projects/hello)
warning: le champ `workers` n'est jamais lu
 --> src/lib.rs:7:5
  |
6 | pub struct ThreadPool {
  |            ---------- champ dans cette structure
7 |     workers: Vec<Worker>,
  |     ^^^^^^^
  |
  = note : `#[warn(dead_code)]` par défaut

warning: les champs `id` et `thread` ne sont jamais lus
  --> src/lib.rs:48:5
   |
47 | struct Worker {
   |        ------ champs dans cette structure
48 |     id: usize,
   |     ^^
49 |     thread: thread::JoinHandle<()>,
   |     ^^^^^^

warning: `hello` (lib) a généré 2 avertissements
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 4.91s
     Running `target/debug/hello`
Worker 0 a reçu un travail ; exécution en cours.
Worker 2 a reçu un travail ; exécution en cours.
Worker 1 a reçu un travail ; exécution en cours.
Worker 3 a reçu un travail ; exécution en cours.
Worker 0 a reçu un travail ; exécution en cours.
Worker 2 a reçu un travail ; exécution en cours.
Worker 1 a reçu un travail ; exécution en cours.
Worker 3 a reçu un travail ; exécution en cours.
```

Succès ! Nous avons maintenant un pool de threads qui exécute les connexions de manière asynchrone. Il n'y a jamais plus de quatre threads créés, donc notre système ne sera pas submergé si le serveur reçoit beaucoup de requêtes. Si nous faisons une requête à _/sleep_, le serveur pourra servir d'autres requêtes en faisant exécuter celles-ci par un autre thread.

> Remarque : Si vous ouvrez _/sleep_ dans plusieurs fenêtres de navigateur simultanément, elles peuvent se charger une par une par intervalles de cinq secondes. Certains navigateurs web exécutent plusieurs instances de la même requête successivement pour des raisons de mise en cache. Cette limitation n'est pas causée par notre serveur web.

C'est un bon moment pour faire une pause et réfléchir à la façon dont le code dans les Listings 21-18, 21-19, et 21-20 serait différent si nous utilisions des futurs au lieu d'une fermeture pour le travail à réaliser. Quels types changeraient ? Comment les signatures des méthodes seraient-elles différentes, le cas échéant ? Quelles parties du code resteraient les mêmes ?

Après avoir appris sur la boucle `while let` dans le Chapitre 17 et le Chapitre 19, vous vous demandez peut-être pourquoi nous n'avons pas écrit le code du thread `Worker` comme indiqué dans le Listing 21-21.

<Listing number="21-21" file-name="src/lib.rs" caption="Une implémentation alternative de `Worker::new` utilisant `while let`">

```rust,ignore,not_desired_behavior
{{#rustdoc_include ../listings/ch21-web-server/listing-21-21/src/lib.rs:here}}
```

</Listing>

Ce code compile et s'exécute mais ne produit pas le comportement de threading souhaité : Une requête lente entraînera toujours d'autres requêtes en attente d'être traitées. La raison est quelque peu subtile : La structure `Mutex` n'a pas de méthode publique `unlock` car la propriété du verrou est basée sur la durée de vie du `MutexGuard<T>` dans `LockResult<MutexGuard<T>>` que la méthode `lock` retourne. Au moment de la compilation, le vérificateur d'emprunt peut alors faire respecter la règle selon laquelle une ressource protégée par un `Mutex` ne peut être accessible que si nous tenons le verrou. Cependant, cette implémentation peut également entraîner une tenue du verrou plus longtemps que prévu si nous ne sommes pas attentifs à la durée de vie de `MutexGuard<T>`.

Le code dans le Listing 21-20 qui utilise `let job = receiver.lock().unwrap().recv().unwrap();` fonctionne parce qu'avec `let`, toutes les valeurs temporaires utilisées dans l'expression sur le côté droit du signe égal sont immédiatement supprimées lorsque la déclaration `let` se termine. Cependant, `while let` (et `if let` et `match`) ne supprime pas les valeurs temporaires jusqu'à la fin du bloc associé. Dans le Listing 21-21, le verrou reste détenu pendant la durée de l'appel à `job()`, ce qui signifie que d'autres instances de `Worker` ne peuvent pas recevoir de travaux.

[type-aliases]: ch20-03-advanced-types.html#type-synonyms-and-type-aliases
[integer-types]: ch03-02-data-types.html#integer-types
[moving-out-of-closures]: ch13-01-closures.html#moving-captured-values-out-of-closures
[builder]: ../std/thread/struct.Builder.html
[builder-spawn]: ../std/thread/struct.Builder.html#method.spawn