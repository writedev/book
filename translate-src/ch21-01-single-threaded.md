## Créer un serveur web à thread unique

Nous allons commencer par faire fonctionner un serveur web à thread unique. Avant de commencer, examinons rapidement les protocoles utilisés pour créer des serveurs web. Les détails de ces protocoles dépassent le cadre de ce livre, mais un bref aperçu vous donnera les informations dont vous avez besoin.

Les deux principaux protocoles utilisés par les serveurs web sont le _Hypertext Transfer Protocol_ _(HTTP)_ et le _Transmission Control Protocol_ _(TCP)_. Ce sont tous deux des protocoles de type _requête-réponse_ : un _client_ envoie des requêtes, et un _serveur_ les écoute puis fournit une réponse au client. Le contenu de ces requêtes et réponses est défini par les protocoles.

TCP est le protocole de bas niveau qui décrit comment les informations passent d’un serveur à un autre, mais il ne précise pas de quelles informations il s’agit. HTTP s’appuie sur TCP en définissant le contenu des requêtes et des réponses. Il est techniquement possible d’utiliser HTTP avec d’autres protocoles, mais dans la grande majorité des cas, HTTP envoie ses données via TCP. Nous travaillerons avec les octets bruts des requêtes et réponses TCP et HTTP.

### Écouter la connexion TCP

Notre serveur web doit écouter une connexion TCP ; c’est donc la première partie sur laquelle nous allons travailler. La bibliothèque standard propose un module `std::net` qui nous permet de le faire. Créons un nouveau projet de la manière habituelle :

```console
$ cargo new hello
     Created binary (application) `hello` project
$ cd hello
```

Saisissez maintenant le code de la Liste 21-1 dans _src/main.rs_ pour commencer. Ce code écoutera les flux TCP entrants à l’adresse locale `127.0.0.1:7878`. Lorsqu’il recevra un flux entrant, il affichera `Connection established!`.

<Listing number="21-1" file-name="src/main.rs" caption="Écouter les flux entrants et afficher un message à la réception d’un flux">

```rust,no_run
{{#rustdoc_include ../listings/ch21-web-server/listing-21-01/src/main.rs}}
```

</Listing>

Avec `TcpListener`, nous pouvons écouter les connexions TCP à l’adresse `127.0.0.1:7878`. Dans cette adresse, la partie avant les deux-points est une adresse IP qui représente votre ordinateur (elle est identique sur tous les ordinateurs et ne désigne pas spécifiquement l’ordinateur des auteurs), et `7878` est le port. Nous avons choisi ce port pour deux raisons : HTTP n’est normalement pas utilisé sur ce port, notre serveur a donc peu de chances d’entrer en conflit avec un autre serveur web qui pourrait fonctionner sur votre machine ; et, sur un clavier téléphonique, le mot _rust_ correspond à 7878.

Dans ce contexte, la fonction `bind` fonctionne comme la fonction `new` : elle renvoie une nouvelle instance de `TcpListener`. Elle est appelée `bind` parce qu’en réseau, le fait de se connecter à un port pour l’écouter est appelé « lier un port ».

La fonction `bind` renvoie un `Result<T, E>`, ce qui signifie que la liaison peut échouer, par exemple si nous exécutons deux instances de notre programme et que deux programmes écoutent ainsi le même port. Comme nous écrivons un serveur élémentaire uniquement à des fins d’apprentissage, nous ne nous préoccuperons pas de gérer ce type d’erreur ; nous utilisons plutôt `unwrap` pour arrêter le programme en cas d’erreur.

La méthode `incoming` de `TcpListener` renvoie un itérateur qui nous fournit une séquence de flux (plus précisément, des flux de type `TcpStream`). Un seul _flux_ représente une connexion ouverte entre le client et le serveur. Une _connexion_ désigne le processus complet de requête et de réponse : le client se connecte au serveur, le serveur génère une réponse, puis ferme la connexion. Nous lirons donc depuis `TcpStream` pour examiner ce que le client a envoyé, puis nous écrirons notre réponse dans le flux afin de renvoyer des données au client. Dans l’ensemble, cette boucle `for` traitera chaque connexion à tour de rôle et nous fournira une série de flux à gérer.

Pour l’instant, gérer le flux consiste à appeler `unwrap` pour arrêter le programme si le flux présente une erreur ; en l’absence d’erreur, le programme affiche un message. Nous ajouterons davantage de fonctionnalités pour le cas où tout se passe bien dans la prochaine liste. Si nous pouvons recevoir des erreurs de la méthode `incoming` lorsqu’un client se connecte au serveur, c’est parce que nous ne parcourons pas réellement les connexions, mais les _tentatives de connexion_. Une connexion peut échouer pour diverses raisons, dont beaucoup dépendent du système d’exploitation. Par exemple, de nombreux systèmes d’exploitation limitent le nombre de connexions ouvertes simultanées qu’ils peuvent prendre en charge ; toute nouvelle tentative de connexion au-delà de cette limite produira une erreur jusqu’à ce que certaines des connexions ouvertes soient fermées.

Essayons d’exécuter ce code ! Lancez `cargo run` dans le terminal, puis ouvrez _127.0.0.1:7878_ dans un navigateur web. Le navigateur devrait afficher un message d’erreur du type « Connexion réinitialisée », car le serveur ne renvoie encore aucune donnée. Mais dans votre terminal, vous devriez voir plusieurs messages affichés lorsque le navigateur s’est connecté au serveur !

```text
     Running `target/debug/hello`
Connection established!
Connection established!
Connection established!
```

Il arrive que plusieurs messages s’affichent pour une seule requête du navigateur ; cela peut s’expliquer par le fait que le navigateur demande la page ainsi que d’autres ressources, comme l’icône _favicon.ico_ qui apparaît dans l’onglet du navigateur.

Il se peut aussi que le navigateur essaie de se connecter plusieurs fois au serveur parce que celui-ci ne renvoie aucune donnée. Lorsque `stream` sort de sa portée et est supprimé à la fin de la boucle, la connexion est fermée dans le cadre de l’implémentation de `drop`. Les navigateurs réagissent parfois à la fermeture d’une connexion en réessayant, car le problème peut être temporaire.

Les navigateurs ouvrent aussi parfois plusieurs connexions au serveur sans envoyer de requête, afin que, s’ils en envoient *plus tard*, celles-ci puissent être traitées plus rapidement. Dans ce cas, notre serveur verra chaque connexion, qu’elle transporte ou non des requêtes. Plusieurs versions des navigateurs basés sur Chrome font cela, par exemple ; vous pouvez désactiver cette optimisation en utilisant la navigation privée ou un autre navigateur.

L’essentiel, c’est que nous avons réussi à obtenir un accès à une connexion TCP !

N’oubliez pas d’arrêter le programme en appuyant sur <kbd>ctrl</kbd>-<kbd>C</kbd> lorsque vous avez fini d’exécuter une version donnée du code. Relancez ensuite le programme avec la commande `cargo run` après chaque série de modifications du code pour vous assurer que vous exécutez bien la version la plus récente.

### Lire la requête

Implémentons la lecture de la requête envoyée par le navigateur ! Pour séparer les responsabilités — d’abord établir une connexion, puis agir sur celle-ci — nous allons créer une nouvelle fonction chargée de traiter les connexions. Dans cette nouvelle fonction `handle_connection`, nous lirons les données du flux TCP et les afficherons afin de voir les données envoyées par le navigateur. Modifiez le code pour qu’il ressemble à celui de la Liste 21-2.

<Listing number="21-2" file-name="src/main.rs" caption="Lire depuis `TcpStream` et afficher les données">

```rust,no_run
{{#rustdoc_include ../listings/ch21-web-server/listing-21-02/src/main.rs}}
```

</Listing>

Nous importons `std::io::BufReader` et `std::io::prelude` dans la portée afin d’accéder aux traits et aux types qui nous permettent de lire depuis le flux et d’y écrire. Dans la boucle `for` de la fonction `main`, au lieu d’afficher un message indiquant qu’une connexion a été établie, nous appelons maintenant la nouvelle fonction `handle_connection` et lui transmettons `stream`.

Dans la fonction `handle_connection`, nous créons une nouvelle instance de `BufReader` qui encapsule une référence à `stream`. `BufReader` ajoute un tampon en gérant pour nous les appels aux méthodes du trait `std::io::Read`.

Nous créons une variable nommée `http_request` pour recueillir les lignes de la requête que le navigateur envoie à notre serveur. Nous indiquons que nous voulons recueillir ces lignes dans un vecteur en ajoutant l’annotation de type `Vec<_>`.

`BufReader` implémente le trait `std::io::BufRead`, qui fournit la méthode `lines`. La méthode `lines` renvoie un itérateur de `Result<String, std::io::Error>` en séparant le flux de données chaque fois qu’elle rencontre un octet de nouvelle ligne. Pour obtenir chaque `String`, nous appliquons `map` et `unwrap` à chaque `Result`. Le `Result` peut contenir une erreur si les données ne sont pas de l’UTF-8 valide ou si un problème est survenu lors de la lecture du flux. Là encore, un programme de production devrait gérer ces erreurs avec plus de soin, mais nous choisissons d’arrêter le programme en cas d’erreur par souci de simplicité.

Le navigateur signale la fin d’une requête HTTP en envoyant deux caractères de nouvelle ligne consécutifs. Pour obtenir une requête du flux, nous lisons donc les lignes jusqu’à en trouver une qui soit une chaîne vide. Une fois les lignes recueillies dans le vecteur, nous les affichons avec le formatage de débogage détaillé afin d’examiner les instructions que le navigateur envoie à notre serveur.

Essayons ce code ! Lancez le programme et envoyez de nouveau une requête depuis un navigateur web. Notez que le navigateur affichera toujours une page d’erreur, mais la sortie de notre programme dans le terminal devrait maintenant ressembler à ceci :

<!-- manual-regeneration
cd listings/ch21-web-server/listing-21-02
cargo run
make a request to 127.0.0.1:7878
Can't automate because the output depends on making requests
-->

```console
$ cargo run
   Compiling hello v0.1.0 (file:///projects/hello)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.42s
     Running `target/debug/hello`
Request: [
    "GET / HTTP/1.1",
    "Host: 127.0.0.1:7878",
    "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:99.0) Gecko/20100101 Firefox/99.0",
    "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language: en-US,en;q=0.5",
    "Accept-Encoding: gzip, deflate, br",
    "DNT: 1",
    "Connection: keep-alive",
    "Upgrade-Insecure-Requests: 1",
    "Sec-Fetch-Dest: document",
    "Sec-Fetch-Mode: navigate",
    "Sec-Fetch-Site: none",
    "Sec-Fetch-User: ?1",
    "Cache-Control: max-age=0",
]
```

Selon votre navigateur, la sortie peut légèrement différer. Maintenant que nous affichons les données de la requête, nous pouvons comprendre pourquoi une seule requête du navigateur peut provoquer plusieurs connexions : il suffit d’examiner le chemin qui suit `GET` sur la première ligne de la requête. Si les connexions répétées demandent toutes _/_, nous savons que le navigateur essaie de récupérer _/_ à plusieurs reprises parce qu’il ne reçoit aucune réponse de notre programme.

Examinons ces données de requête pour comprendre ce que le navigateur demande à notre programme.

<!-- Old headings. Do not remove or links may break. -->

<a id="a-closer-look-at-an-http-request"></a>
<a id="looking-closer-at-an-http-request"></a>

### Examen approfondi d’une requête HTTP

HTTP est un protocole textuel, et une requête suit ce format :

```text
Method Request-URI HTTP-Version CRLF
headers CRLF
message-body
```

La première ligne est la _ligne de requête_, qui contient des informations sur ce que le client demande. La première partie de cette ligne indique la méthode utilisée, comme `GET` ou `POST`, qui décrit la manière dont le client formule sa requête. Notre client a utilisé une requête `GET`, ce qui signifie qu’il demande des informations.

La partie suivante de la ligne de requête est _/_, qui indique l’_identifiant uniforme de ressource_ _(URI)_ demandé par le client : un URI est presque, mais pas tout à fait, la même chose qu’un _localisateur uniforme de ressource_ _(URL)_. La différence entre les URI et les URL n’a pas d’importance pour notre propos dans ce chapitre, mais la spécification HTTP emploie le terme _URI_ ; nous pouvons donc simplement le remplacer mentalement par _URL_ ici.

La dernière partie est la version HTTP utilisée par le client, puis la ligne de requête se termine par une séquence CRLF. (_CRLF_ signifie _carriage return_ et _line feed_, deux termes hérités de l’époque des machines à écrire !) La séquence CRLF peut aussi s’écrire `\r\n`, où `\r` correspond au retour chariot et `\n` au saut de ligne. La _séquence CRLF_ sépare la ligne de requête du reste des données de la requête. Notez que lorsque CRLF est affiché, nous voyons le début d’une nouvelle ligne plutôt que `\r\n`.

En examinant les données de la ligne de requête que notre programme a reçues jusqu’ici, nous constatons que `GET` est la méthode, _/_ est l’URI de la requête et `HTTP/1.1` est la version.

Après la ligne de requête, les lignes restantes, à partir de `Host:`, sont des en-têtes. Les requêtes `GET` n’ont pas de corps.

Essayez d’envoyer une requête depuis un autre navigateur ou de demander une autre adresse, comme _127.0.0.1:7878/test_, pour voir comment les données de la requête changent.

Maintenant que nous savons ce que demande le navigateur, renvoyons-lui des données !

### Écrire une réponse

Nous allons implémenter l’envoi de données en réponse à une requête du client. Les réponses suivent le format suivant :

```text
HTTP-Version Status-Code Reason-Phrase CRLF
headers CRLF
message-body
```

La première ligne est une _ligne d’état_ qui contient la version HTTP utilisée dans la réponse, un code d’état numérique qui résume le résultat de la requête et une expression explicative qui décrit le code d’état. Après la séquence CRLF viennent les en-têtes éventuels, une autre séquence CRLF, puis le corps de la réponse.

Voici un exemple de réponse qui utilise la version 1.1 de HTTP, le code d’état 200, l’expression explicative « OK », et qui ne comporte ni en-têtes ni corps :

```text
HTTP/1.1 200 OK\r\n\r\n
```

Le code d’état 200 est la réponse standard en cas de succès. Ce texte constitue une toute petite réponse HTTP réussie. Écrivons-le dans le flux en réponse à une requête réussie ! Dans la fonction `handle_connection`, supprimez le `println!` qui affichait les données de la requête et remplacez-le par le code de la Liste 21-3.

<Listing number="21-3" file-name="src/main.rs" caption="Écrire une réponse HTTP minimale indiquant une réussite dans le flux">

```rust,no_run
{{#rustdoc_include ../listings/ch21-web-server/listing-21-03/src/main.rs:here}}
```

</Listing>

La première nouvelle ligne définit la variable `response`, qui contient les données du message de réussite. Ensuite, nous appelons `as_bytes` sur `response` pour convertir les données de la chaîne en octets. La méthode `write_all` sur `stream` prend un `&[u8]` et envoie directement ces octets sur la connexion. Comme l’opération `write_all` peut échouer, nous utilisons `unwrap` sur tout résultat d’erreur, comme précédemment. Là encore, dans une véritable application, vous ajouteriez ici une gestion des erreurs.

Une fois ces modifications effectuées, exécutons notre code et envoyons une requête. Nous n’affichons plus aucune donnée dans le terminal ; nous ne verrons donc que la sortie de Cargo. Lorsque vous ouvrez _127.0.0.1:7878_ dans un navigateur web, vous devriez obtenir une page blanche plutôt qu’une erreur. Vous venez de coder vous-même la réception d’une requête HTTP et l’envoi d’une réponse !

### Renvoyer du vrai HTML

Implémentons la fonctionnalité permettant de renvoyer autre chose qu’une page blanche. Créez le nouveau fichier _hello.html_ à la racine du répertoire de votre projet, et non dans le répertoire _src_. Vous pouvez y saisir le code HTML de votre choix ; la Liste 21-4 en montre un exemple.

<Listing number="21-4" file-name="hello.html" caption="Exemple de fichier HTML à renvoyer dans une réponse">

```html
{{#include ../listings/ch21-web-server/listing-21-05/hello.html}}
```

</Listing>

Il s’agit d’un document HTML5 minimal qui contient un titre et du texte. Pour le renvoyer par le serveur à la réception d’une requête, nous allons modifier `handle_connection` comme indiqué dans la Liste 21-5 afin de lire le fichier HTML, de l’ajouter au corps de la réponse et de l’envoyer.

<Listing number="21-5" file-name="src/main.rs" caption="Envoyer le contenu de *hello.html* dans le corps de la réponse">

```rust,no_run
{{#rustdoc_include ../listings/ch21-web-server/listing-21-05/src/main.rs:here}}
```

</Listing>

Nous avons ajouté `fs` à l’instruction `use` pour importer le module de gestion du système de fichiers de la bibliothèque standard dans la portée. Le code qui lit le contenu d’un fichier dans une chaîne devrait vous sembler familier ; nous l’avons utilisé lorsque nous avons lu le contenu d’un fichier pour notre projet d’E/S dans la Liste 12-4.

Ensuite, nous utilisons `format!` pour ajouter le contenu du fichier au corps de la réponse de réussite. Pour garantir la validité de la réponse HTTP, nous ajoutons l’en-tête `Content-Length`, dont la valeur correspond à la taille du corps de notre réponse — dans ce cas, à la taille de `hello.html`.

Exécutez ce code avec `cargo run`, puis ouvrez _127.0.0.1:7878_ dans votre navigateur ; votre code HTML devrait s’afficher !

Pour l’instant, nous ignorons les données de la requête dans `http_request` et renvoyons toujours le contenu du fichier HTML, quelles que soient les circonstances. Autrement dit, si vous demandez _127.0.0.1:7878/something-else_ dans votre navigateur, vous recevrez quand même la même réponse HTML. À ce stade, notre serveur est très limité et ne fait pas ce que font la plupart des serveurs web. Nous voulons personnaliser nos réponses en fonction de la requête et ne renvoyer le fichier HTML que pour une requête correctement formée vers _/_.

### Valider la requête et répondre de manière sélective

Pour l’instant, notre serveur web renvoie le contenu du fichier HTML quel que soit ce que le client demande. Ajoutons une fonctionnalité qui vérifie que le navigateur demande _/_ avant de renvoyer le fichier HTML, et qui renvoie une erreur si le navigateur demande autre chose. Pour cela, nous devons modifier `handle_connection`, comme indiqué dans la Liste 21-6. Ce nouveau code compare le contenu de la requête reçue à ce que nous savons d’une requête vers _/_ et ajoute des blocs `if` et `else` pour traiter les requêtes différemment.

<Listing number="21-6" file-name="src/main.rs" caption="Traiter différemment les requêtes vers */* et les autres requêtes">

```rust,no_run
{{#rustdoc_include ../listings/ch21-web-server/listing-21-06/src/main.rs:here}}
```

</Listing>

Nous allons uniquement examiner la première ligne de la requête HTTP. Au lieu de lire la requête entière dans un vecteur, nous appelons donc `next` pour obtenir le premier élément de l’itérateur. Le premier `unwrap` traite le `Option` et arrête le programme si l’itérateur ne contient aucun élément. Le second `unwrap` traite le `Result` et a le même effet que le `unwrap` présent dans le `map` ajouté dans la Liste 21-2.

Ensuite, nous vérifions si `request_line` est égal à la ligne d’une requête `GET` vers le chemin _/_. Si c’est le cas, le bloc `if` renvoie le contenu de notre fichier HTML.

Si `request_line` n’est _pas_ égal à la requête `GET` vers le chemin _/_, cela signifie que nous avons reçu une autre requête. Nous ajouterons dans un instant du code au bloc `else` pour répondre à toutes les autres requêtes.

Exécutez ce code et demandez _127.0.0.1:7878_ ; vous devriez recevoir le contenu de _hello.html_. Si vous envoyez une autre requête, comme _127.0.0.1:7878/something-else_, vous obtiendrez une erreur de connexion comme celles que vous avez vues lors de l’exécution du code des Listes 21-1 et 21-2.

Ajoutons maintenant au bloc `else` le code de la Liste 21-7 afin de renvoyer une réponse avec le code d’état 404, qui indique que le contenu demandé est introuvable. Nous renverrons également du code HTML à afficher dans le navigateur pour informer l’utilisateur final de la réponse.

<Listing number="21-7" file-name="src/main.rs" caption="Renvoyer le code d’état 404 et une page d’erreur si une autre adresse que */* a été demandée">

```rust,no_run
{{#rustdoc_include ../listings/ch21-web-server/listing-21-07/src/main.rs:here}}
```

</Listing>

Ici, notre réponse contient une ligne d’état avec le code 404 et l’expression explicative `NOT FOUND`. Le corps de la réponse contiendra le code HTML du fichier _404.html_. Vous devrez créer un fichier _404.html_ à côté de _hello.html_ pour la page d’erreur ; là encore, utilisez le code HTML de votre choix ou l’exemple de la Liste 21-8.

<Listing number="21-8" file-name="404.html" caption="Exemple de contenu de la page à renvoyer pour toute réponse 404">

```html
{{#include ../listings/ch21-web-server/listing-21-07/404.html}}
```

</Listing>

Une fois ces modifications effectuées, relancez votre serveur. Une requête vers _127.0.0.1:7878_ devrait renvoyer le contenu de _hello.html_, tandis que toute autre requête, comme _127.0.0.1:7878/foo_, devrait renvoyer le code HTML d’erreur de _404.html_.

<!-- Old headings. Do not remove or links may break. -->

<a id="a-touch-of-refactoring"></a>

### Refactorisation

Pour l’instant, les blocs `if` et `else` contiennent beaucoup de répétitions : ils lisent tous deux des fichiers et écrivent leur contenu dans le flux. Seules la ligne d’état et le nom de fichier diffèrent. Rendons le code plus concis en extrayant ces différences dans des lignes `if` et `else` distinctes qui attribueront les valeurs de la ligne d’état et du nom de fichier à des variables ; nous pourrons ensuite utiliser ces variables sans condition dans le code qui lit le fichier et écrit la réponse. La Liste 21-9 montre le code obtenu après le remplacement des grands blocs `if` et `else`.

<Listing number="21-9" file-name="src/main.rs" caption="Refactoriser les blocs `if` et `else` pour ne conserver que le code qui diffère entre les deux cas">

```rust,no_run
{{#rustdoc_include ../listings/ch21-web-server/listing-21-09/src/main.rs:here}}
```

</Listing>

Les blocs `if` et `else` ne renvoient maintenant que les valeurs appropriées pour la ligne d’état et le nom de fichier dans un tuple ; nous utilisons ensuite le destructuring pour attribuer ces deux valeurs à `status_line` et `filename` en utilisant un motif dans l’instruction `let`, comme expliqué au chapitre 19.

Le code auparavant dupliqué se trouve maintenant en dehors des blocs `if` et `else` et utilise les variables `status_line` et `filename`. Il est ainsi plus facile de voir la différence entre les deux cas, et nous n’avons plus qu’un seul endroit à modifier si nous voulons changer la façon dont la lecture du fichier et l’écriture de la réponse fonctionnent. Le code de la Liste 21-9 se comportera comme celui de la Liste 21-7.

Excellent ! Nous avons maintenant un serveur web simple, écrit en environ 40 lignes de code Rust, qui répond à une requête en renvoyant une page et à toutes les autres par une réponse 404.

Pour l’instant, notre serveur s’exécute sur un seul thread, ce qui signifie qu’il ne peut traiter qu’une requête à la fois. Examinons pourquoi cela peut poser problème en simulant des requêtes lentes. Ensuite, nous corrigerons le problème pour que notre serveur puisse traiter plusieurs requêtes en même temps.