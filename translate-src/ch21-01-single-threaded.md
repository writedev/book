## Création d'un Serveur Web Monothread

Nous allons commencer par faire fonctionner un serveur web monothread. Avant de commencer, examinons un aperçu rapide des protocoles impliqués dans la création de serveurs web. Les détails de ces protocoles dépassent le cadre de ce livre, mais un bref aperçu vous fournira les informations dont vous avez besoin.

Les deux principaux protocoles impliqués dans les serveurs web sont le _Protocole de Transfert Hypertexte_ _(HTTP)_ et le _Protocole de Contrôle de Transmission_ _(TCP)_. Les deux protocoles sont des protocoles _demande-réponse_, ce qui signifie qu'un _client_ initie des demandes et qu'un _serveur_ écoute les demandes et fournit une réponse au client. Le contenu de ces demandes et réponses est défini par les protocoles.

TCP est le protocole de niveau inférieur qui décrit les détails de la façon dont les informations sont transférées d'un serveur à un autre, mais ne précise pas ce que ces informations sont. HTTP s'appuie sur TCP en définissant le contenu des demandes et des réponses. Il est techniquement possible d'utiliser HTTP avec d'autres protocoles, mais dans la grande majorité des cas, HTTP envoie ses données via TCP. Nous allons travailler avec les octets bruts des demandes et des réponses TCP et HTTP.

### Écouter la Connexion TCP

Notre serveur web doit écouter une connexion TCP, c'est donc la première partie sur laquelle nous allons travailler. La bibliothèque standard propose un module `std::net` qui nous permet de le faire. Commençons par créer un nouveau projet comme d'habitude :

```console
$ cargo new hello
     Projet binaire (application) `hello` créé
$ cd hello
```

Entrez maintenant le code de la Liste 21-1 dans _src/main.rs_ pour commencer. Ce code écoutera à l'adresse locale `127.0.0.1:7878` pour les flux TCP entrants. Lorsqu'il recevra un flux entrant, il affichera `Connexion établie !`.

<Listing number="21-1" file-name="src/main.rs" caption="Écoute des flux entrants et impression d'un message lors de la réception d'un flux">

```rust,no_run
{{#rustdoc_include ../listings/ch21-web-server/listing-21-01/src/main.rs}}
```

</Listing>

Avec `TcpListener`, nous pouvons écouter des connexions TCP à l'adresse `127.0.0.1:7878`. Dans l'adresse, la section avant le deux-points est une adresse IP représentant votre ordinateur (cela est identique sur chaque ordinateur et ne représente pas spécifiquement l'ordinateur des auteurs), et `7878` est le port. Nous avons choisi ce port pour deux raisons : HTTP n'est normalement pas accepté sur ce port, donc notre serveur est peu susceptible de rentrer en conflit avec un autre serveur web que vous pourriez avoir en cours d'exécution sur votre machine, et 7878 est _rust_ tapé sur un téléphone.

La fonction `bind` dans ce scénario fonctionne comme la fonction `new` en ce sens qu'elle renvoie une nouvelle instance de `TcpListener`. La fonction est appelée `bind` parce qu'en réseautique, se connecter à un port pour écouter est connu sous le nom de « liaison à un port ».

La fonction `bind` renvoie un `Result<T, E>`, ce qui indique qu'il est possible que la liaison échoue, par exemple, si nous avons exécuté deux instances de notre programme et avons donc deux programmes écoutant le même port. Comme nous écrivons un serveur de base uniquement à des fins d'apprentissage, nous ne nous préoccuperons pas de la gestion de ce type d'erreurs ; à la place, nous utiliserons `unwrap` pour arrêter le programme en cas d'erreurs.

La méthode `incoming` sur `TcpListener` renvoie un itérateur qui nous donne une séquence de flux (plus précisément, des flux de type `TcpStream`). Un seul _flux_ représente une connexion ouverte entre le client et le serveur. _Connexion_ est le terme désignant le processus complet de demande et de réponse dans lequel un client se connecte au serveur, le serveur génère une réponse, et le serveur ferme la connexion. En tant que tel, nous allons lire à partir du `TcpStream` pour voir ce que le client a envoyé, puis écrire notre réponse dans le flux pour renvoyer des données au client. Dans l'ensemble, cette boucle `for` traitera chaque connexion à son tour et produira une série de flux à gérer.

Pour l'instant, notre gestion du flux consiste à appeler `unwrap` pour terminer notre programme si le flux présente des erreurs ; s'il n'y a pas d'erreurs, le programme affiche un message. Nous ajouterons plus de fonctionnalité pour le cas de succès dans la prochaine liste. La raison pour laquelle nous pourrions recevoir des erreurs de la méthode `incoming` lorsque client se connecte au serveur est que nous ne faisons pas réellement itérer sur les connexions. Au lieu de cela, nous itérons sur les _tentatives de connexion_. La connexion peut ne pas être réussie pour de nombreuses raisons, dont beaucoup sont spécifiques au système d'exploitation. Par exemple, de nombreux systèmes d'exploitation ont une limite au nombre de connexions ouvertes simultanément qu'ils peuvent prendre en charge ; les nouvelles tentatives de connexion au-delà de ce nombre produiront une erreur jusqu'à ce que certaines des connexions ouvertes soient fermées.

Essayons maintenant d'exécuter ce code ! Invoquez `cargo run` dans le terminal puis chargez _127.0.0.1:7878_ dans un navigateur web. Le navigateur devrait afficher un message d'erreur tel que « Connexion réinitialisée » car le serveur ne renvoie actuellement aucune donnée. Mais lorsque vous regardez votre terminal, vous devriez voir plusieurs messages qui ont été imprimés lorsque le navigateur s'est connecté au serveur !

```text
     Exécution de `target/debug/hello`
Connexion établie !
Connexion établie !
Connexion établie !
```

Parfois, vous verrez plusieurs messages imprimés pour une demande de navigateur ; la raison pourrait être que le navigateur fait une demande pour la page ainsi qu'une demande pour d'autres ressources, comme l'icône _favicon.ico_ qui apparaît dans l'onglet du navigateur.

Il se peut également que le navigateur essaie de se connecter au serveur plusieurs fois car le serveur ne répond pas avec des données. Lorsque `stream` sort de la portée et est abandonné à la fin de la boucle, la connexion est fermée dans le cadre de l'implémentation `drop`. Les navigateurs gèrent parfois les connexions fermées en réessayant, car le problème peut être temporaire.

Les navigateurs ouvrent parfois plusieurs connexions au serveur sans envoyer de demandes, afin que si ils *font* ensuite des demandes, ces demandes puissent se faire plus rapidement. Lorsque cela se produit, notre serveur verra chaque connexion, qu'il y ait ou non des demandes sur cette connexion. De nombreuses versions des navigateurs basés sur Chrome le font, par exemple ; vous pouvez désactiver cette optimisation en utilisant le mode de navigation privée ou en utilisant un autre navigateur.

Le facteur important est que nous avons réussi à obtenir un accès à une connexion TCP !

N'oubliez pas d'arrêter le programme en appuyant sur <kbd>ctrl</kbd>-<kbd>C</kbd> lorsque vous avez terminé d'exécuter une version particulière du code. Ensuite, redémarrez le programme en invoquant la commande `cargo run` après avoir effectué chaque ensemble de modifications de code pour vous assurer que vous exécutez le code le plus récent.

### Lecture de la Demande

Implémentons la fonctionnalité pour lire la demande du navigateur ! Pour séparer les préoccupations consistant d'abord à obtenir une connexion puis à prendre certaines mesures avec la connexion, nous allons démarrer une nouvelle fonction pour traiter les connexions. Dans cette nouvelle fonction `handle_connection`, nous allons lire les données du flux TCP et les imprimer afin que nous puissions voir les données envoyées par le navigateur. Modifiez le code pour qu'il ressemble à la Liste 21-2.

<Listing number="21-2" file-name="src/main.rs" caption="Lecture depuis le `TcpStream` et impression des données">

```rust,no_run
{{#rustdoc_include ../listings/ch21-web-server/listing-21-02/src/main.rs}}
```

</Listing>

Nous apportons `std::io::BufReader` et `std::io::prelude` dans l'espace de noms pour obtenir accès aux traits et types qui nous permettent de lire et d'écrire dans le flux. Dans la boucle `for` de la fonction `main`, au lieu d'imprimer un message disant que nous avons établi une connexion, nous appelons maintenant la nouvelle fonction `handle_connection` et lui passons le `stream`.

Dans la fonction `handle_connection`, nous créons une nouvelle instance de `BufReader` qui enveloppe une référence au `stream`. Le `BufReader` ajoute une mise en mémoire tampon en gérant les appels aux méthodes du trait `std::io::Read` pour nous.

Nous créons une variable nommée `http_request` pour collecter les lignes de la demande que le navigateur envoie à notre serveur. Nous indiquons que nous voulons collecter ces lignes dans un vecteur en ajoutant l'annotation de type `Vec<_>`.

`BufReader` implémente le trait `std::io::BufRead`, qui fournit la méthode `lines`. La méthode `lines` renvoie un itérateur de `Result<String, std::io::Error>` en séparant le flux de données chaque fois qu'elle voit un octet de nouvelle ligne. Pour obtenir chaque `String`, nous `map` et `unwrap` chaque `Result`. Le `Result` peut être une erreur si les données ne sont pas un UTF-8 valide ou s'il y a un problème en lisant depuis le flux. Encore une fois, un programme de production devrait gérer ces erreurs plus gracieusement, mais nous choisissons d'arrêter le programme dans le cas d'une erreur pour des raisons de simplicité.

Le navigateur signale la fin d'une demande HTTP en envoyant deux caractères de nouvelle ligne consécutifs, donc pour obtenir une demande du flux, nous prenons des lignes jusqu'à ce que nous obtenions une ligne qui est une chaîne vide. Une fois que nous avons collecté les lignes dans le vecteur, nous les imprimons en utilisant un format de débogage agréablement formaté afin que nous puissions examiner les instructions que le navigateur web envoie à notre serveur.

Essayons ce code ! Démarrez le programme et faites une demande dans un navigateur web à nouveau. Notez que nous obtiendrons toujours une page d'erreur dans le navigateur, mais la sortie de notre programme dans le terminal ressemblera désormais à ceci :

```console
$ cargo run
   Compilation du hello v0.1.0 (file:///projects/hello)
    Profil `dev` terminé [non optimisé + information de débogage] cible(s) en 0.42s
     Exécution de `target/debug/hello`
Demande : [
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

Selon votre navigateur, vous pourriez obtenir une sortie légèrement différente. Maintenant que nous imprimons les données de la demande, nous pouvons voir pourquoi nous obtenons plusieurs connexions d'une demande de navigateur en regardant le chemin après `GET` dans la première ligne de la demande. Si les connexions répétées demandent toutes _/_, nous savons que le navigateur essaie de récupérer _/_ de manière répétée car il ne reçoit pas de réponse de notre programme.

Décomposons ces données de demande pour comprendre ce que le navigateur demande à notre programme.

### Examen Plus Approfondi d'une Demande HTTP

HTTP est un protocole basé sur du texte, et une demande prend ce format :

```text
Méthode Request-URI Version-HTTP CRLF
en-têtes CRLF
corps-du-message
```

La première ligne est la _ligne de demande_ qui contient des informations sur ce que le client demande. La première partie de la ligne de demande indique la méthode utilisée, telle que `GET` ou `POST`, qui décrit comment le client fait cette demande. Notre client a utilisé une demande `GET`, ce qui signifie qu'il demande des informations.

La partie suivante de la ligne de demande est _/_, qui indique l'_identifiant de ressource uniforme_ _(URI)_ que le client demande : Un URI est presque, mais pas tout à fait, le même qu'un _localisateur de ressource uniforme_ _(URL)_. La différence entre les URI et les URL n'est pas importante pour nos besoins dans ce chapitre, mais la spécification HTTP utilise le terme _URI_, donc nous pouvons simplement substituer mentalement _URL_ à _URI_ ici.

La dernière partie est la version HTTP utilisée par le client, et ensuite la ligne de demande se termine par une séquence CRLF. (_CRLF_ signifie _retour chariot_ et _saut de ligne_, qui sont des termes issus de l'époque des machines à écrire !) La séquence CRLF peut également être écrite comme `\r\n`, où `\r` est un retour chariot et `\n` est un saut de ligne. La _séquence CRLF_ sépare la ligne de demande des autres données de demande. Notez que lorsque le CRLF est imprimé, nous voyons commencer une nouvelle ligne plutôt que `\r\n`.

En regardant les données de la ligne de demande que nous avons reçues en exécutant notre programme jusqu'à présent, nous voyons que `GET` est la méthode, _/_ est l'URI de demande, et `HTTP/1.1` est la version.

Après la ligne de demande, les lignes restantes à partir de `Host:` représentent des en-têtes. Les demandes `GET` n'ont pas de corps.

Essayez de faire une demande depuis un autre navigateur ou demandez une autre adresse, telle que _127.0.0.1:7878/test_, pour voir comment les données de demande changent.

Maintenant que nous savons ce que demande le navigateur, envoyons des données en retour !

### Écriture d'une Réponse

Nous allons implémenter l'envoi de données en réponse à une demande du client. Les réponses ont le format suivant :

```text
Version-HTTP Code-de-Statut Phrase-de-Raison CRLF
en-têtes CRLF
corps-de-la-réponse
```

La première ligne est une _ligne de statut_ qui contient la version HTTP utilisée dans la réponse, un code de statut numérique qui résume le résultat de la demande, et une phrase de raison qui fournit une description textuelle du code de statut. Après la séquence CRLF se trouvent toutes les en-têtes, une autre séquence CRLF et le corps de la réponse.

Voici un exemple de réponse qui utilise la version HTTP 1.1 et a un code de statut de 200, une phrase de raison OK, sans en-têtes et sans corps :

```text
HTTP/1.1 200 OK\r\n\r\n
```

Le code de statut 200 est la réponse standard de succès. C'est une toute petite réponse HTTP réussie. Écrivons cela dans le flux comme notre réponse à une demande réussie ! À partir de la fonction `handle_connection`, retirez le `println!` qui imprimait les données de la demande et remplacez-le par le code dans la Liste 21-3.

<Listing number="21-3" file-name="src/main.rs" caption="Écriture d'une petite réponse HTTP réussie dans le flux">

```rust,no_run
{{#rustdoc_include ../listings/ch21-web-server/listing-21-03/src/main.rs:here}}
```

</Listing>

La première nouvelle ligne définit la variable `response` qui contient les données du message de succès. Ensuite, nous appelons `as_bytes` sur notre `response` pour convertir les données de la chaîne en octets. La méthode `write_all` sur `stream` prend un `&[u8]` et envoie ces octets directement via la connexion. Étant donné que l'opération `write_all` pourrait échouer, nous utilisons `unwrap` sur tout résultat d'erreur comme précédemment. Encore une fois, dans une application réelle, vous ajouteriez une gestion des erreurs ici.

Avec ces changements, exécutons notre code et faisons une demande. Nous n'imprimons plus de données dans le terminal, donc nous ne verrons aucune sortie autre que celle de Cargo. Lorsque vous chargez _127.0.0.1:7878_ dans un navigateur web, vous devriez obtenir une page blanche au lieu d'une erreur. Vous venez de coder manuellement la réception d'une demande HTTP et l'envoi d'une réponse !

### Retourner un Vrai HTML

Implémentons la fonctionnalité pour retourner plus qu'une page blanche. Créez le nouveau fichier _hello.html_ à la racine de votre répertoire de projet, pas dans le répertoire _src_. Vous pouvez y mettre n'importe quel HTML que vous souhaitez ; la Liste 21-4 montre une possibilité.

<Listing number="21-4" file-name="hello.html" caption="Un fichier HTML d'exemple à retourner dans une réponse">

```html
{{#include ../listings/ch21-web-server/listing-21-05/hello.html}}
```

</Listing>

Il s'agit d'un document HTML5 minimal avec un en-tête et un peu de texte. Pour le retourner depuis le serveur lorsqu'une demande est reçue, nous allons modifier `handle_connection` comme montré dans la Liste 21-5 pour lire le fichier HTML, l'ajouter à la réponse en tant que corps et l'envoyer.

<Listing number="21-5" file-name="src/main.rs" caption="Envoi du contenu de *hello.html* comme le corps de la réponse">

```rust,no_run
{{#rustdoc_include ../listings/ch21-web-server/listing-21-05/src/main.rs:here}}
```

</Listing>

Nous avons ajouté `fs` à l'instruction `use` pour apporter le module système de fichiers de la bibliothèque standard dans l'espace de noms. Le code pour lire les contenus d'un fichier dans une chaîne devrait vous sembler familier ; nous l'avons utilisé lorsque nous avons lu le contenu d'un fichier pour notre projet I/O dans la Liste 12-4.

Ensuite, nous utilisons `format!` pour ajouter le contenu du fichier comme corps de la réponse de succès. Pour assurer une réponse HTTP valide, nous ajoutons l'en-tête `Content-Length`, qui est défini en fonction de la taille de notre corps de réponse — dans ce cas, la taille de `hello.html`.

Exécutez ce code avec `cargo run` et chargez _127.0.0.1:7878_ dans votre navigateur ; vous devriez voir votre HTML rendu !

Actuellement, nous ignorons les données de la demande dans `http_request` et envoyons simplement le contenu du fichier HTML de façon inconditionnelle. Cela signifie que si vous essayez de demander _127.0.0.1:7878/something-else_ dans votre navigateur, vous obtiendrez toujours cette même réponse HTML. Pour le moment, notre serveur est très limité et ne fait pas ce que font la plupart des serveurs web. Nous voulons personnaliser nos réponses en fonction de la demande et ne renvoyer le fichier HTML que pour une demande bien formée à _/_.

### Validation de la Demande et Réponse Sélective

Pour l'instant, notre serveur web retourne le HTML dans le fichier peu importe ce que le client a demandé. Ajoutons une fonctionnalité pour vérifier que le navigateur demande _/_ avant de renvoyer le fichier HTML et pour retourner une erreur si le navigateur demande autre chose. Pour cela, nous devons modifier `handle_connection`, comme montré dans la Liste 21-6. Ce nouveau code vérifie le contenu de la demande reçue par rapport à ce que nous savons être une demande pour _/_ et ajoute des blocs `if` et `else` pour traiter les demandes différemment.

<Listing number="21-6" file-name="src/main.rs" caption="Gestion des demandes à */* différemment des autres demandes">

```rust,no_run
{{#rustdoc_include ../listings/ch21-web-server/listing-21-06/src/main.rs:here}}
```

</Listing>

Nous allons uniquement examiner la première ligne de la demande HTTP, donc plutôt que de lire la demande entière dans un vecteur, nous appelons `next` pour obtenir le premier élément de l'itérateur. Le premier `unwrap` s'occupe de l'`Option` et arrête le programme si l'itérateur n'a pas d'éléments. Le second `unwrap` gère le `Result` et a le même effet que le `unwrap` qui était dans le `map` ajouté dans la Liste 21-2.

Ensuite, nous vérifions si `request_line` est égal à la ligne de demande d'une requête GET à l'URI _/_. Si c'est le cas, le bloc `if` renvoie le contenu de notre fichier HTML.

Si `request_line` n'égale pas la requête GET à l'URI _/_, cela signifie que nous avons reçu une autre demande. Nous allons ajouter du code au bloc `else` dans un instant pour répondre à toutes les autres demandes.

Exécutez ce code maintenant et demandez _127.0.0.1:7878_ ; vous devriez obtenir le HTML dans _hello.html_. Si vous faites une autre demande, comme _127.0.0.1:7878/something-else_, vous obtiendrez une erreur de connexion comme celles que vous avez vues en exécutant le code dans les Listes 21-1 et 21-2.

Maintenant, ajoutons le code dans la Liste 21-7 au bloc `else` pour renvoyer une réponse avec le code de statut 404, qui signale que le contenu de la demande n'a pas été trouvé. Nous allons également retourner un HTML pour une page à rendre dans le navigateur indiquant la réponse à l'utilisateur final.

<Listing number="21-7" file-name="src/main.rs" caption="Répondre avec le code de statut 404 et une page d'erreur si autre chose que */* a été demandé">

```rust,no_run
{{#rustdoc_include ../listings/ch21-web-server/listing-21-07/src/main.rs:here}}
```

</Listing>

Ici, notre réponse a une ligne de statut avec un code de statut 404 et la phrase de raison `NOT FOUND`. Le corps de la réponse sera le HTML dans le fichier _404.html_. Vous devrez créer un fichier _404.html_ à côté de _hello.html_ pour la page d'erreur ; encore une fois, n'hésitez pas à utiliser n'importe quel HTML que vous voulez, ou utilisez l'exemple HTML dans la Liste 21-8.

<Listing number="21-8" file-name="404.html" caption="Contenu d'exemple pour la page à renvoyer avec toute réponse 404">

```html
{{#include ../listings/ch21-web-server/listing-21-07/404.html}}
```

</Listing>

Avec ces changements, exécutez à nouveau votre serveur. Demander _127.0.0.1:7878_ devrait renvoyer le contenu de _hello.html_, et toute autre demande, comme _127.0.0.1:7878/foo_, devrait renvoyer le HTML d'erreur de _404.html_.

### Refactoring

Pour l'instant, les blocs `if` et `else` contiennent beaucoup de répétitions : Ils lisent tous les deux des fichiers et écrivent le contenu des fichiers dans le flux. Les seules différences sont la ligne de statut et le nom de fichier. Rendre le code plus concis consiste à extraire ces différences en lignes `if` et `else` distinctes qui attribueront les valeurs de la ligne de statut et du nom de fichier à des variables ; nous pourrons ensuite utiliser ces variables sans condition dans le code pour lire le fichier et écrire la réponse. La Liste 21-9 montre le code résultant après avoir remplacé les grands blocs `if` et `else`.

<Listing number="21-9" file-name="src/main.rs" caption="Refactorisation des blocs `if` et `else` pour ne contenir que le code qui diffère entre les deux cas">

```rust,no_run
{{#rustdoc_include ../listings/ch21-web-server/listing-21-09/src/main.rs:here}}
```

</Listing>

Maintenant, les blocs `if` et `else` retournent uniquement les valeurs appropriées pour la ligne de statut et le nom de fichier dans un tuple ; nous utilisons ensuite la déstructuration pour attribuer ces deux valeurs à `status_line` et `filename` à l'aide d'un modèle dans l'instruction `let`, comme discuté dans le Chapitre 19.

Le code précédemment dupliqué se trouve maintenant en dehors des blocs `if` et `else` et utilise les variables `status_line` et `filename`. Cela facilite la visualisation de la différence entre les deux cas, et cela signifie que nous n'avons qu'un seul endroit pour mettre à jour le code si nous voulons changer la manière dont la lecture de fichier et l'écriture de réponse fonctionnent. Le comportement du code dans la Liste 21-9 sera le même que celui de la Liste 21-7.

Génial ! Nous avons maintenant un serveur web simple en environ 40 lignes de code Rust qui répond à une demande avec une page de contenu et répond à toutes les autres demandes avec une réponse 404.

Actuellement, notre serveur fonctionne dans un seul thread, ce qui signifie qu'il ne peut servir qu'une demande à la fois. Examinons en quoi cela peut poser problème en simulant quelques demandes lentes. Ensuite, nous corrigerons cela afin que notre serveur puisse gérer plusieurs demandes simultanément.