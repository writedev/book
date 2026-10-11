<!-- Old headings. Do not remove or links may break. -->

<a id="turning-our-single-threaded-server-into-a-multithreaded-server"></a>
<a id="from-single-threaded-to-multithreaded-server"></a>

## D’un serveur monothread à un serveur multithread

Actuellement, le serveur traite chaque requête à tour de rôle : il ne traite pas
de deuxième connexion tant que le traitement de la première n’est pas terminé.
Si le serveur reçoit de plus en plus de requêtes, cette exécution séquentielle
devient de moins en moins optimale. Si le serveur reçoit une requête dont le
traitement prend beaucoup de temps, les requêtes suivantes devront attendre
qu’elle soit terminée, même si elles peuvent être traitées rapidement. Nous
devrons corriger cela, mais commençons par observer le problème en action.

<!-- Old headings. Do not remove or links may break. -->

<a id="simulating-a-slow-request-in-the-current-server-implementation"></a>

### Simuler une requête lente

Nous allons voir comment une requête traitée lentement peut affecter les autres
requêtes adressées à notre implémentation actuelle du serveur. Le Listing 21-10
implémente le traitement d’une requête vers _/sleep_ avec une réponse lente
simulée, qui fera attendre le serveur pendant cinq secondes avant de répondre.

<Listing number="21-10" file-name="src/main.rs" caption="Simuler une requête lente en attendant cinq secondes">

```rust,no_run
{{#rustdoc_include ../listings/ch21-web-server/listing-21-10/src/main.rs:here}}
```

</Listing>

Nous avons remplacé `if` par `match`, puisque nous avons maintenant trois cas.
Nous devons explicitement effectuer une correspondance sur une tranche de
`request_line` pour comparer avec les valeurs littérales de chaîne ; `match`
n’effectue pas automatiquement les emprunts et les déréférencements, comme le
fait la méthode d’égalité.

Le premier bras est identique au bloc `if` du Listing 21-9. Le deuxième bras
correspond à une requête vers _/sleep_. Lorsque cette requête est reçue, le
serveur attend cinq secondes avant de générer la page HTML de réussite. Le
troisième bras est identique au bloc `else` du Listing 21-9.

Vous pouvez constater à quel point notre serveur est rudimentaire : les
bibliothèques réelles géreraient la reconnaissance de plusieurs requêtes de
façon beaucoup moins verbeuse !

Démarrez le serveur avec `cargo run`. Ouvrez ensuite deux fenêtres de
navigateur : l’une pour _http://127.0.0.1:7878_ et l’autre pour
_http://127.0.0.1:7878/sleep_. Si vous saisissez plusieurs fois l’URI _/_, comme
précédemment, vous verrez que le serveur répond rapidement. Mais si vous
saisissez _/sleep_, puis chargez _/_, vous verrez que _/_ attend que `sleep` ait
terminé ses cinq secondes avant de se charger.

Il existe plusieurs techniques pour éviter que les requêtes ne s’accumulent
derrière une requête lente, notamment l’utilisation de l’asynchrone, comme au
Chapitre 17 ; celle que nous allons implémenter est un pool de threads.

### Améliorer le débit avec un pool de threads

Un _pool de threads_ est un groupe de threads lancés qui sont prêts et attendent
de prendre en charge une tâche. Lorsque le programme reçoit une nouvelle tâche,
il l’attribue à l’un des threads du pool, qui la traite. Les autres threads du
pool restent disponibles pour prendre en charge toute autre tâche reçue pendant
que le premier thread traite la sienne. Lorsque le premier thread a terminé sa
tâche, il est réintégré au pool de threads inactifs, prêt à prendre en charge
une nouvelle tâche. Un pool de threads permet de traiter les connexions
simultanément, ce qui augmente le débit de votre serveur.

Nous limiterons le nombre de threads du pool à un petit nombre afin de nous
protéger contre les attaques par déni de service (DoS) ; si notre programme
créait un nouveau thread pour chaque requête à mesure de leur arrivée, une
personne envoyant 10 millions de requêtes à notre serveur pourrait faire des
ravages en épuisant toutes ses ressources et en ralentissant le traitement des
requêtes jusqu’à l’arrêt.

Au lieu de lancer un nombre illimité de threads, nous aurons donc un nombre
fixe de threads en attente dans le pool. Les requêtes entrantes sont envoyées
au pool pour y être traitées. Le pool maintient une file d’attente des requêtes
entrantes. Chacun des threads du pool retire une requête de cette file, la
traite, puis demande une autre requête à la file. Avec cette conception, nous
pouvons traiter jusqu’à _`N`_ requêtes simultanément, où _`N`_ est le nombre de
threads. Si chaque thread traite une requête de longue durée, les requêtes
suivantes peuvent toujours s’accumuler dans la file, mais nous avons augmenté
le nombre de requêtes de longue durée que nous pouvons traiter avant d’en
arriver là.

Cette technique n’est qu’une des nombreuses façons d’améliorer le débit d’un
serveur web. Vous pourriez aussi explorer le modèle fork/join, le modèle
d’E/S asynchrones monothread et le modèle d’E/S asynchrones multithread. Si ce
sujet vous intéresse, vous pouvez lire davantage sur d’autres solutions et
essayer de les implémenter ; avec un langage de bas niveau comme Rust, toutes
ces options sont possibles.

Avant de commencer à implémenter un pool de threads, parlons de la façon dont
son utilisation devrait se présenter. Lorsque vous concevez du code, écrire
d’abord l’interface cliente peut vous aider à guider votre conception. Écrivez
l’API du code de façon à structurer les appels comme vous souhaitez les
effectuer ; implémentez ensuite les fonctionnalités dans cette structure,
plutôt que d’implémenter les fonctionnalités avant de concevoir l’API publique.

Comme nous avons utilisé le développement piloté par les tests dans le projet
du Chapitre 12, nous utiliserons ici le développement piloté par le compilateur.
Nous allons écrire le code qui appelle les fonctions souhaitées, puis examiner
les erreurs du compilateur afin de déterminer les modifications à apporter
pour faire fonctionner le code. Avant cela, cependant, nous allons explorer la
technique que nous n’utiliserons pas comme point de départ.

<!-- Old headings. Do not remove or links may break. -->

<a id="code-structure-if-we-could-spawn-a-thread-for-each-request"></a>

#### Lancer un thread pour chaque requête

Commençons par examiner à quoi pourrait ressembler notre code s’il créait un
nouveau thread pour chaque connexion. Comme indiqué précédemment, ce n’est pas
notre plan final, car il pourrait lancer un nombre illimité de threads, mais
c’est un bon point de départ pour créer d’abord un serveur multithread
fonctionnel. Nous ajouterons ensuite le pool de threads comme amélioration, et
la comparaison des deux solutions sera plus facile.

Le Listing 21-11 présente les modifications à apporter à `main` pour lancer un
nouveau thread chargé de traiter chaque flux dans la boucle `for`.

<Listing number="21-11" file-name="src/main.rs" caption="Lancer un nouveau thread pour chaque flux">

```rust,no_run
{{#rustdoc_include ../listings/ch21-web-server/listing-21-11/src/main.rs:here}}
```

</Listing>

Comme vous l’avez appris au Chapitre 16, `thread::spawn` crée un nouveau thread,
puis exécute le code de la fermeture dans ce nouveau thread. Si vous exécutez
ce code et chargez _/sleep_ dans votre navigateur, puis _/_ dans deux autres
onglets, vous constaterez effectivement que les requêtes vers _/_ n’ont pas à
attendre la fin de _/sleep_. Cependant, comme nous l’avons mentionné, cela
finira par submerger le système, car vous créeriez de nouveaux threads sans
aucune limite.

Vous vous souvenez peut-être aussi du Chapitre 17 que c’est exactement le genre
de situation où async et await brillent ! Gardez cela à l’esprit pendant que
nous construisons le pool de threads et réfléchissez à ce qui serait différent
ou identique avec async.

<!-- Old headings. Do not remove or links may break. -->

<a id="creating-a-similar-interface-for-a-finite-number-of-threads"></a>

#### Créer un nombre fini de threads

Nous voulons que notre pool de threads fonctionne de façon similaire et
familière, afin que le passage des threads à un pool de threads ne nécessite
pas de modifications importantes du code qui utilise notre API. Le Listing
21-12 montre l’interface hypothétique d’une structure `ThreadPool` que nous
voulons utiliser à la place de `thread::spawn`.

<Listing number="21-12" file-name="src/main.rs" caption="L’interface `ThreadPool` idéale">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch21-web-server/listing-21-12/src/main.rs:here}}
```

</Listing>

Nous utilisons `ThreadPool::new` pour créer un nouveau pool de threads avec un
nombre configurable de threads, quatre dans cet exemple. Ensuite, dans la
boucle `for`, `pool.execute` présente une interface similaire à
`thread::spawn` : elle prend une fermeture que le pool doit exécuter pour
chaque flux. Nous devons implémenter `pool.execute` afin qu’elle prenne la
fermeture et la confie à un thread du pool pour qu’il l’exécute. Ce code ne
sera pas encore compilé, mais nous allons essayer afin que le compilateur nous
guide pour le corriger.

<!-- Old headings. Do not remove or links may break. -->

<a id="building-the-threadpool-struct-using-compiler-driven-development"></a>

#### Construire `ThreadPool` avec le développement piloté par le compilateur

Effectuez les modifications du Listing 21-12 dans _src/main.rs_, puis
utilisons les erreurs du compilateur produites par `cargo check` pour guider
notre développement. Voici la première erreur que nous obtenons :

```console
{{#include ../listings/ch21-web-server/listing-21-12/output.txt}}
```

Parfait ! Cette erreur nous indique que nous avons besoin d’un type ou d’un
module `ThreadPool` ; nous allons donc le créer. Notre implémentation de
`ThreadPool` sera indépendante du type de travail effectué par notre serveur
web. Nous allons donc transformer la crate `hello` de crate binaire en crate
bibliothèque afin d’y placer notre implémentation de `ThreadPool`. Une fois
cette conversion effectuée, nous pourrons également utiliser cette bibliothèque
de pool de threads pour tous les travaux nécessitant un pool de threads, et pas
seulement pour servir des requêtes web.

Créez un fichier _src/lib.rs_ contenant ce qui suit, la définition la plus
simple possible d’une structure `ThreadPool` pour le moment :

<Listing file-name="src/lib.rs">

```rust,noplayground
{{#rustdoc_include ../listings/ch21-web-server/no-listing-01-define-threadpool-struct/src/lib.rs}}
```

</Listing>


Modifiez ensuite le fichier _main.rs_ pour importer `ThreadPool` depuis la
crate bibliothèque en ajoutant le code suivant en haut de _src/main.rs_ :

<Listing file-name="src/main.rs">

```rust,ignore
{{#rustdoc_include ../listings/ch21-web-server/no-listing-01-define-threadpool-struct/src/main.rs:here}}
```

</Listing>

Ce code ne fonctionnera toujours pas, mais vérifions-le à nouveau pour obtenir
la prochaine erreur à corriger :

```console
{{#include ../listings/ch21-web-server/no-listing-01-define-threadpool-struct/output.txt}}
```

Cette erreur indique que nous devons maintenant créer une fonction associée
nommée `new` pour `ThreadPool`. Nous savons aussi que `new` doit prendre un
paramètre pouvant recevoir `4` comme argument et renvoyer une instance de
`ThreadPool`. Implémentons la fonction `new` la plus simple possible qui
présente ces caractéristiques :

<Listing file-name="src/lib.rs">

```rust,noplayground
{{#rustdoc_include ../listings/ch21-web-server/no-listing-02-impl-threadpool-new/src/lib.rs}}
```

</Listing>

Nous avons choisi `usize` comme type du paramètre `size`, car nous savons qu’un
nombre négatif de threads n’a aucun sens. Nous savons également que nous
utiliserons ce `4` comme nombre d’éléments d’une collection de threads, ce qui
correspond à l’usage du type `usize`, comme expliqué dans la section [« Types
entiers »][integer-types]<!-- ignore --> du Chapitre 3.

Vérifions à nouveau le code :

```console
{{#include ../listings/ch21-web-server/no-listing-02-impl-threadpool-new/output.txt}}
```

L’erreur apparaît maintenant parce que `ThreadPool` ne possède pas de méthode
`execute`. Rappelez-vous, dans la section [« Créer un nombre fini de
threads »](#creating-a-finite-number-of-threads)<!-- ignore -->, nous avons
décidé que notre pool de threads devrait avoir une interface similaire à
`thread::spawn`. De plus, nous allons implémenter la fonction `execute` afin
qu’elle prenne la fermeture reçue et la confie à un thread inactif du pool pour
qu’il l’exécute.

Nous allons définir la méthode `execute` sur `ThreadPool` de façon à ce qu’elle
prenne une fermeture comme paramètre. Rappelez-vous, dans la section
[« Déplacer des valeurs capturées hors des fermetures
»][moving-out-of-closures]<!-- ignore --> du Chapitre 13, que nous pouvons
prendre des fermetures comme paramètres avec trois traits différents : `Fn`,
`FnMut` et `FnOnce`. Nous devons choisir le type de fermeture à utiliser ici.
Nous savons que nous finirons par faire quelque chose de similaire à
l’implémentation de `thread::spawn` dans la bibliothèque standard ; nous
pouvons donc examiner les contraintes de traits de la signature de
`thread::spawn`. La documentation nous présente ce qui suit :

```rust,ignore
pub fn spawn<F, T>(f: F) -> JoinHandle<T>
    where
        F: FnOnce() -> T,
        F: Send + 'static,
        T: Send + 'static,
```

Le paramètre de type `F` est celui qui nous intéresse ici ; le paramètre de
type `T` est lié à la valeur de retour et ne nous intéresse pas. Nous voyons que
`spawn` utilise `FnOnce` comme contrainte de trait sur `F`. C’est probablement
ce que nous voulons aussi, car nous finirons par transmettre à `spawn`
l’argument reçu par `execute`. Nous pouvons en être d’autant plus sûrs que
`FnOnce` est le trait que nous voulons utiliser, car le thread chargé de traiter
une requête n’exécutera la fermeture de cette requête qu’une seule fois, ce qui
correspond à `Once` dans `FnOnce`.

Le paramètre de type `F` possède également la contrainte de trait `Send` et la
contrainte de durée de vie `'static`, qui sont utiles dans notre cas : nous
avons besoin de `Send` pour transférer la fermeture d’un thread à un autre, et
de `'static` parce que nous ne savons pas combien de temps le thread mettra à
s’exécuter. Créons une méthode `execute` sur `ThreadPool` qui prend un
paramètre générique de type `F` doté de ces contraintes :

<Listing file-name="src/lib.rs">

```rust,noplayground
{{#rustdoc_include ../listings/ch21-web-server/no-listing-03-define-execute/src/lib.rs:here}}
```

</Listing>

Nous conservons `()` après `FnOnce`, car ce `FnOnce` représente une fermeture
qui ne prend aucun paramètre et renvoie le type unité `()`. Comme dans les
définitions de fonctions, le type de retour peut être omis de la signature,
mais même si nous n’avons aucun paramètre, nous devons quand même conserver les
parenthèses.

Là encore, il s’agit de l’implémentation la plus simple possible de la méthode
`execute` : elle ne fait rien, mais nous cherchons uniquement à faire compiler
notre code. Vérifions-le à nouveau :

```console
{{#include ../listings/ch21-web-server/no-listing-03-define-execute/output.txt}}
```

La compilation réussit ! Mais notez que si vous essayez `cargo run` et envoyez
une requête depuis le navigateur, vous verrez les mêmes erreurs dans le
navigateur qu’au début du chapitre. Notre bibliothèque n’appelle pas encore la
fermeture transmise à `execute` !

> Remarque : À propos des langages dotés de compilateurs stricts, comme Haskell
> et Rust, vous entendrez peut-être l’adage « Si le code compile, il fonctionne
> ». Mais cet adage n’est pas toujours vrai. Notre projet compile, mais ne fait
> absolument rien ! Si nous développions un vrai projet complet, ce serait le
> bon moment pour commencer à écrire des tests unitaires afin de vérifier que le
> code compile _et_ présente le comportement voulu.

À votre avis, qu’est-ce qui serait différent ici si nous devions exécuter une
future plutôt qu’une fermeture ?

#### Valider le nombre de threads dans `new`

Nous ne faisons rien avec les paramètres de `new` et de `execute`. Implémentons
le corps de ces fonctions avec le comportement souhaité. Commençons par
réfléchir à `new`. Nous avons choisi précédemment un type non signé pour le
paramètre `size`, car un pool avec un nombre négatif de threads n’a aucun sens.
Cependant, un pool avec zéro thread n’a pas plus de sens, bien que zéro soit
une valeur parfaitement valide de type `usize`. Nous allons ajouter du code
pour vérifier que `size` est supérieur à zéro avant de renvoyer une instance
de `ThreadPool`, et nous ferons paniquer le programme s’il reçoit zéro en
utilisant la macro `assert!`, comme indiqué dans le Listing 21-13.

<Listing number="21-13" file-name="src/lib.rs" caption="Implémenter `ThreadPool::new` pour provoquer une panique si `size` vaut zéro">

```rust,noplayground
{{#rustdoc_include ../listings/ch21-web-server/listing-21-13/src/lib.rs:here}}
```

</Listing>

Nous avons également ajouté de la documentation pour notre `ThreadPool` avec
des commentaires de documentation. Notez que nous avons suivi les bonnes
pratiques de documentation en ajoutant une section qui précise les situations
dans lesquelles notre fonction peut provoquer une panique, comme expliqué au
Chapitre 14. Essayez d’exécuter `cargo doc --open` et de cliquer sur la
structure `ThreadPool` pour voir à quoi ressemble la documentation générée pour
`new` !

Au lieu d’ajouter la macro `assert!` comme nous l’avons fait ici, nous pourrions
transformer `new` en `build` et renvoyer un `Result`, comme nous l’avons fait
pour `Config::build` dans le projet d’E/S du Listing 12-9. Mais nous avons
décidé dans ce cas qu’essayer de créer un pool de threads sans threads devrait
être une erreur irrécupérable. Si vous êtes ambitieux, essayez d’écrire une
fonction nommée `build` avec la signature suivante, afin de la comparer à la
fonction `new` :

```rust,ignore
pub fn build(size: usize) -> Result<ThreadPool, PoolCreationError> {
```

#### Créer un espace pour stocker les threads

Maintenant que nous savons comment vérifier que le nombre de threads à stocker
dans le pool est valide, nous pouvons les créer et les stocker dans la
structure `ThreadPool` avant de renvoyer celle-ci. Mais comment « stocker » un
thread ? Réexaminons la signature de `thread::spawn` :

```rust,ignore
pub fn spawn<F, T>(f: F) -> JoinHandle<T>
    where
        F: FnOnce() -> T,
        F: Send + 'static,
        T: Send + 'static,
```

La fonction `spawn` renvoie un `JoinHandle<T>`, où `T` est le type renvoyé par
la fermeture. Essayons également d’utiliser `JoinHandle` pour voir ce qui se
passe. Dans notre cas, les fermetures transmises au pool de threads traiteront
la connexion et ne renverront rien ; `T` sera donc le type unité `()`.

Le code du Listing 21-14 compile, mais ne crée pas encore de threads. Nous avons
modifié la définition de `ThreadPool` pour qu’elle contienne un vecteur
d’instances de `thread::JoinHandle<()>`, initialisé le vecteur avec une capacité
de `size`, ajouté une boucle `for` qui exécutera du code pour créer les threads
et renvoyé une instance de `ThreadPool` qui les contient.

<Listing number="21-14" file-name="src/lib.rs" caption="Créer un vecteur dans lequel `ThreadPool` stockera les threads">

```rust,ignore,not_desired_behavior
{{#rustdoc_include ../listings/ch21-web-server/listing-21-14/src/lib.rs:here}}
```

</Listing>

Nous avons importé `std::thread` dans la crate bibliothèque, car nous utilisons
`thread::JoinHandle` comme type des éléments du vecteur dans `ThreadPool`.

Une fois qu’une taille valide est reçue, notre `ThreadPool` crée un nouveau
vecteur capable de contenir `size` éléments. La fonction `with_capacity`
effectue la même tâche que `Vec::new`, mais présente une différence importante :
elle préalloue de l’espace dans le vecteur. Puisque nous savons que nous devons
y stocker `size` éléments, effectuer cette allocation à l’avance est légèrement
plus efficace que d’utiliser `Vec::new`, qui redimensionne le vecteur au fur
et à mesure de l’ajout des éléments.

Lorsque vous exécutez à nouveau `cargo check`, la compilation devrait réussir.

<!-- Old headings. Do not remove or links may break. -->
<a id ="a-worker-struct-responsible-for-sending-code-from-the-threadpool-to-a-thread"></a>

#### Envoyer du code du `ThreadPool` à un thread

Nous avons laissé un commentaire dans la boucle `for` du Listing 21-14 à propos
de la création des threads. Nous allons voir ici comment les créer réellement.
La bibliothèque standard fournit `thread::spawn` pour créer des threads, et
`thread::spawn` attend du code que le thread exécutera dès sa création.
Cependant, dans notre cas, nous voulons créer les threads et les faire
_attendre_ le code que nous leur enverrons plus tard. L’implémentation des
threads de la bibliothèque standard ne permet pas de le faire ; nous devons
l’implémenter nous-mêmes.

Nous allons implémenter ce comportement en introduisant une nouvelle structure
de données entre `ThreadPool` et les threads, chargée de gérer ce nouveau
comportement. Nous appellerons cette structure de données _Worker_, un terme
courant dans les implémentations de pools. Le `Worker` récupère le code à
exécuter et l’exécute dans son thread.

Imaginez le personnel qui travaille dans la cuisine d’un restaurant : les
employés attendent les commandes des clients, puis ils sont chargés de les
prendre en charge et de les préparer.

Au lieu de stocker un vecteur d’instances de `JoinHandle<()>` dans le pool de
threads, nous stockerons des instances de la structure `Worker`. Chaque
`Worker` stockera une seule instance de `JoinHandle<()>`. Nous implémenterons
ensuite une méthode sur `Worker` qui prendra une fermeture contenant le code à
exécuter et l’enverra au thread déjà en cours d’exécution pour qu’il l’exécute.
Nous attribuerons également un `id` à chaque `Worker` afin de pouvoir distinguer
les différentes instances de `Worker` du pool lors de la journalisation ou du
débogage.

Voici le processus qui aura lieu lors de la création d’un `ThreadPool`. Nous
implémenterons le code qui envoie la fermeture au thread une fois que nous
aurons configuré `Worker` de la manière suivante :

1. Définir une structure `Worker` qui contient un `id` et un `JoinHandle<()>`.
2. Modifier `ThreadPool` pour qu’il contienne un vecteur d’instances de
   `Worker`.
3. Définir une fonction `Worker::new` qui prend un numéro `id` et renvoie une
   instance de `Worker` contenant cet `id` et un thread lancé avec une
   fermeture vide.
4. Dans `ThreadPool::new`, utiliser le compteur de la boucle `for` pour générer
   un `id`, créer un nouveau `Worker` avec cet `id` et stocker le `Worker` dans
   le vecteur.

Si vous êtes prêt à relever le défi, essayez d’implémenter ces modifications
par vous-même avant de consulter le code du Listing 21-15.

Prêt ? Voici le Listing 21-15, qui présente une façon d’effectuer les
modifications précédentes.

<Listing number="21-15" file-name="src/lib.rs" caption="Modifier `ThreadPool` pour qu’il contienne des instances de `Worker` plutôt que des threads directement">

```rust,noplayground
{{#rustdoc_include ../listings/ch21-web-server/listing-21-15/src/lib.rs:here}}
```

</Listing>

Nous avons renommé le champ de `ThreadPool` de `threads` en `workers`, car il
contient maintenant des instances de `Worker` plutôt que des instances de
`JoinHandle<()>`. Nous utilisons le compteur de la boucle `for` comme argument
pour `Worker::new` et stockons chaque nouveau `Worker` dans le vecteur nommé
`workers`.

Le code externe, comme notre serveur dans _src/main.rs_, n’a pas besoin de
connaître les détails d’implémentation liés à l’utilisation d’une structure
`Worker` au sein de `ThreadPool` ; nous rendons donc la structure `Worker` et sa
fonction `new` privées. La fonction `Worker::new` utilise l’`id` que nous lui
transmettons et stocke une instance de `JoinHandle<()>`, créée en lançant un
nouveau thread avec une fermeture vide.

> Remarque : Si le système d’exploitation ne peut pas créer de thread faute de
> ressources système suffisantes, `thread::spawn` provoquera une panique. Notre
> serveur tout entier paniquera alors, même si la création de certains threads
> a pu réussir. Pour simplifier, ce comportement convient, mais dans une
> implémentation de pool de threads destinée à la production, vous préféreriez
> probablement utiliser [`std::thread::Builder`][builder]<!-- ignore --> et sa
> méthode [`spawn`][builder-spawn]<!-- ignore -->, qui renvoie plutôt un
> `Result`.

Ce code compile et stocke le nombre d’instances de `Worker` que nous avons
indiqué comme argument de `ThreadPool::new`. Mais nous ne traitons _toujours_
pas la fermeture reçue par `execute`. Voyons maintenant comment y remédier.

#### Envoyer des requêtes aux threads par des canaux

Le prochain problème auquel nous allons nous attaquer est que les fermetures
transmises à `thread::spawn` ne font absolument rien. Actuellement, nous
récupérons la fermeture que nous voulons exécuter dans la méthode `execute`.
Mais nous devons fournir à `thread::spawn` une fermeture à exécuter au moment où
nous créons chaque `Worker` lors de la création du `ThreadPool`.

Nous voulons que les structures `Worker` que nous venons de créer récupèrent le
code à exécuter dans une file d’attente détenue par `ThreadPool`, puis envoient
ce code à leur thread pour qu’il l’exécute.

Les canaux que nous avons découverts au Chapitre 16 — un moyen simple de
communiquer entre deux threads — conviendraient parfaitement à ce cas
d’utilisation. Nous utiliserons un canal comme file d’attente des tâches, et
`execute` enverra une tâche de `ThreadPool` aux instances de `Worker`, qui
l’enverront à leur thread. Voici le plan :

1. Le `ThreadPool` créera un canal et conservera son émetteur.
2. Chaque `Worker` conservera le récepteur.
3. Nous créerons une nouvelle structure `Job` qui contiendra les fermetures que
   nous voulons envoyer par le canal.
4. La méthode `execute` enverra la tâche à exécuter par l’émetteur.
5. Dans son thread, le `Worker` parcourra les messages reçus et exécutera les
   fermetures des tâches reçues.

Commençons par créer un canal dans `ThreadPool::new` et conserver l’émetteur
dans l’instance de `ThreadPool`, comme indiqué dans le Listing 21-16. La
structure `Job` ne contient encore rien, mais elle représentera le type
d’élément que nous envoyons par le canal.

<Listing number="21-16" file-name="src/lib.rs" caption="Modifier `ThreadPool` pour qu’il stocke l’émetteur d’un canal qui transmet des instances de `Job`">

```rust,noplayground
{{#rustdoc_include ../listings/ch21-web-server/listing-21-16/src/lib.rs:here}}
```

</Listing>

Dans `ThreadPool::new`, nous créons notre nouveau canal et faisons en sorte
que le pool en conserve l’émetteur. La compilation réussit.

Essayons de transmettre un récepteur du canal à chaque `Worker` lorsque le pool
de threads crée le canal. Nous savons que nous voulons utiliser le récepteur
dans le thread lancé par les instances de `Worker` ; nous allons donc faire
référence au paramètre `receiver` dans la fermeture. Le code du Listing 21-17
ne compilera pas tout à fait.

<Listing number="21-17" file-name="src/lib.rs" caption="Transmettre le récepteur à chaque `Worker`">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch21-web-server/listing-21-17/src/lib.rs:here}}
```

</Listing>

Nous avons apporté quelques modifications simples : nous transmettons le
récepteur à `Worker::new`, puis nous l’utilisons dans la fermeture.

Lorsque nous essayons de vérifier ce code, nous obtenons cette erreur :

```console
{{#include ../listings/ch21-web-server/listing-21-17/output.txt}}
```

Le code essaie de transmettre `receiver` à plusieurs instances de `Worker`.
Cela ne fonctionnera pas, comme vous vous en souvenez peut-être du Chapitre 16 :
l’implémentation des canaux fournie par Rust permet plusieurs _producteurs_,
mais un seul _consommateur_. Nous ne pouvons donc pas simplement cloner
l’extrémité réceptrice du canal pour corriger ce code. Nous ne voulons pas non
plus envoyer plusieurs fois le même message à plusieurs consommateurs ; nous
voulons une seule liste de messages et plusieurs instances de `Worker`, de façon
à ce que chaque message soit traité une seule fois.

De plus, retirer une tâche de la file du canal implique de modifier le
`receiver`. Les threads doivent donc pouvoir partager et modifier `receiver` de
façon sûre ; autrement, nous risquerions des conditions de concurrence (comme
expliqué au Chapitre 16).

Rappelez-vous les pointeurs intelligents thread-safe présentés au Chapitre 16 :
pour partager la propriété entre plusieurs threads et leur permettre de
modifier la valeur, nous devons utiliser `Arc<Mutex<T>>`. Le type `Arc`
permettra à plusieurs instances de `Worker` de posséder le récepteur, et
`Mutex` garantira qu’une seule instance de `Worker` récupère une tâche du
récepteur à la fois. Le Listing 21-18 présente les modifications nécessaires.

<Listing number="21-18" file-name="src/lib.rs" caption="Partager le récepteur entre les instances de `Worker` à l’aide de `Arc` et de `Mutex`">

```rust,noplayground
{{#rustdoc_include ../listings/ch21-web-server/listing-21-18/src/lib.rs:here}}
```

</Listing>

Dans `ThreadPool::new`, nous plaçons le récepteur dans un `Arc` et un `Mutex`.
Pour chaque nouveau `Worker`, nous clonons l’`Arc` afin d’incrémenter le compteur
de références et de permettre aux instances de `Worker` de partager la
propriété du récepteur.

Avec ces modifications, le code compile ! Nous avançons !

#### Implémenter la méthode `execute`

Implémentons enfin la méthode `execute` sur `ThreadPool`. Nous remplacerons
également `Job`, qui était une structure, par un alias de type pour un objet de
trait contenant le type de fermeture reçu par `execute`. Comme expliqué dans
la section [« Synonymes de type et alias de type
»][type-aliases]<!-- ignore --> du Chapitre 20, les alias de type nous
permettent de raccourcir les types longs afin de les utiliser plus facilement.
Consultez le Listing 21-19.

<Listing number="21-19" file-name="src/lib.rs" caption="Créer un alias de type `Job` pour une `Box` contenant chaque fermeture, puis envoyer la tâche par le canal">

```rust,noplayground
{{#rustdoc_include ../listings/ch21-web-server/listing-21-19/src/lib.rs:here}}
```

</Listing>

Après avoir créé une nouvelle instance de `Job` à partir de la fermeture
reçue dans `execute`, nous envoyons cette tâche par l’extrémité émettrice du
canal. Nous appelons `unwrap` sur `send` au cas où l’envoi échouerait. Cela
pourrait se produire si, par exemple, nous arrêtions tous nos threads, ce qui
signifierait que l’extrémité réceptrice ne reçoit plus de nouveaux messages.
Pour l’instant, nous ne pouvons pas arrêter nos threads : ils continuent leur
exécution tant que le pool existe. Nous utilisons `unwrap` parce que nous
savons que le cas d’échec ne se produira pas, mais le compilateur ne le sait
pas.

Mais nous n’avons pas tout à fait terminé ! Dans `Worker`, notre fermeture
transmise à `thread::spawn` ne fait encore que _référencer_ l’extrémité
réceptrice du canal. Nous devons plutôt faire en sorte que la fermeture tourne
indéfiniment, en demandant une tâche à l’extrémité réceptrice du canal et en
l’exécutant lorsqu’elle en reçoit une. Apportons à `Worker::new` la
modification présentée dans le Listing 21-20.

<Listing number="21-20" file-name="src/lib.rs" caption="Recevoir et exécuter les tâches dans le thread de l’instance `Worker`">

```rust,noplayground
{{#rustdoc_include ../listings/ch21-web-server/listing-21-20/src/lib.rs:here}}
```

</Listing>

Ici, nous appelons d’abord `lock` sur `receiver` pour acquérir le verrou du
mutex, puis nous appelons `unwrap` pour provoquer une panique en cas d’erreur.
L’acquisition d’un verrou peut échouer si le mutex est dans un état
_empoisonné_, ce qui peut arriver si un autre thread a paniqué alors qu’il
détenait le verrou, au lieu de le libérer. Dans cette situation, appeler
`unwrap` pour faire paniquer ce thread est la bonne chose à faire. N’hésitez
pas à remplacer cet appel à `unwrap` par un appel à `expect` accompagné d’un
message d’erreur pertinent pour vous.

Si nous obtenons le verrou du mutex, nous appelons `recv` pour recevoir un
`Job` du canal. Un dernier appel à `unwrap` permet également de traiter les
erreurs possibles à ce stade, qui peuvent se produire si le thread détenant
l’émetteur s’est arrêté, de la même façon que la méthode `send` renvoie `Err`
si le récepteur s’arrête.

L’appel à `recv` bloque le thread ; s’il n’y a pas encore de tâche, le thread
actuel attend qu’une tâche soit disponible. `Mutex<T>` garantit qu’un seul
thread `Worker` à la fois essaie de demander une tâche.

Notre pool de threads fonctionne maintenant ! Lancez-le avec `cargo run` et
envoyez quelques requêtes :

<!-- manual-regeneration
cd listings/ch21-web-server/listing-21-20
cargo run
make some requests to 127.0.0.1:7878
Can't automate because the output depends on making requests
-->

```console
$ cargo run
   Compiling hello v0.1.0 (file:///projects/hello)
warning: field `workers` is never read
 --> src/lib.rs:7:5
  |
6 | pub struct ThreadPool {
  |            ---------- field in this struct
7 |     workers: Vec<Worker>,
  |     ^^^^^^^
  |
  = note: `#[warn(dead_code)]` on by default

warning: fields `id` and `thread` are never read
  --> src/lib.rs:48:5
   |
47 | struct Worker {
   |        ------ fields in this struct
48 |     id: usize,
   |     ^^
49 |     thread: thread::JoinHandle<()>,
   |     ^^^^^^

warning: `hello` (lib) generated 2 warnings
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 4.91s
     Running `target/debug/hello`
Worker 0 got a job; executing.
Worker 2 got a job; executing.
Worker 1 got a job; executing.
Worker 3 got a job; executing.
Worker 0 got a job; executing.
Worker 2 got a job; executing.
Worker 1 got a job; executing.
Worker 3 got a job; executing.
Worker 0 got a job; executing.
Worker 2 got a job; executing.
```

Bravo ! Nous avons maintenant un pool de threads qui traite les connexions de
façon asynchrone. Il n’y a jamais plus de quatre threads créés, notre système
ne sera donc pas surchargé si le serveur reçoit beaucoup de requêtes. Si nous
envoyons une requête vers _/sleep_, le serveur pourra traiter d’autres requêtes
en les faisant exécuter par un autre thread.

> Remarque : Si vous ouvrez _/sleep_ dans plusieurs fenêtres de navigateur en
> même temps, elles pourraient se charger l’une après l’autre, à intervalles de
> cinq secondes. Certains navigateurs exécutent séquentiellement plusieurs
> instances d’une même requête pour des raisons de mise en cache. Cette
> limitation n’est pas due à notre serveur web.

C’est le bon moment pour faire une pause et réfléchir à ce qui serait différent
dans le code des Listings 21-18, 21-19 et 21-20 si nous utilisions des futures
plutôt qu’une fermeture pour le travail à effectuer. Quels types changeraient ?
En quoi les signatures des méthodes seraient-elles différentes, le cas
échéant ? Quelles parties du code resteraient identiques ?

Après avoir découvert la boucle `while let` aux Chapitres 17 et 19, vous vous
demandez peut-être pourquoi nous n’avons pas écrit le code du thread `Worker`
comme dans le Listing 21-21.

<Listing number="21-21" file-name="src/lib.rs" caption="Une implémentation alternative de `Worker::new` utilisant `while let`">

```rust,ignore,not_desired_behavior
{{#rustdoc_include ../listings/ch21-web-server/listing-21-21/src/lib.rs:here}}
```

</Listing>

Ce code compile et s’exécute, mais ne produit pas le comportement attendu en
matière de threads : une requête lente fera toujours attendre les autres
requêtes avant leur traitement. La raison est assez subtile : la structure
`Mutex` n’a pas de méthode publique `unlock`, car la propriété du verrou dépend
de la durée de vie de `MutexGuard<T>` dans le `LockResult<MutexGuard<T>>`
renvoyé par la méthode `lock`. À la compilation, l’emprunteur peut alors faire
respecter la règle selon laquelle une ressource protégée par un `Mutex` ne peut
pas être utilisée sans détenir le verrou. Cependant, cette implémentation peut
aussi faire en sorte que le verrou soit conservé plus longtemps que prévu si
nous ne prêtons pas attention à la durée de vie de `MutexGuard<T>`.

Le code du Listing 21-20, qui utilise `let job =
receiver.lock().unwrap().recv().unwrap();`, fonctionne parce qu’avec `let`,
toutes les valeurs temporaires utilisées dans l’expression située à droite du
signe égal sont immédiatement supprimées à la fin de l’instruction `let`.
Cependant, `while let` (ainsi que `if let` et `match`) ne supprime pas les
valeurs temporaires avant la fin du bloc associé. Dans le Listing 21-21, le
verrou reste détenu pendant toute la durée de l’appel à `job()`, ce qui empêche
les autres instances de `Worker` de recevoir des tâches.

[type-aliases]: ch20-03-advanced-types.html#type-synonyms-and-type-aliases
[integer-types]: ch03-02-data-types.html#integer-types
[moving-out-of-closures]: ch13-01-closures.html#moving-captured-values-out-of-closures
[builder]: ../std/thread/struct.Builder.html
[builder-spawn]: ../std/thread/struct.Builder.html#method.spawn