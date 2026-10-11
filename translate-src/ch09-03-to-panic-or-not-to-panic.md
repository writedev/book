## Appeler `panic!` ou non

Alors, comment décider quand appeler `panic!` et quand renvoyer `Result` ? Lorsqu’un code panique, il n’y a aucun moyen de récupérer. Vous pourriez appeler `panic!` pour toute situation d’erreur, qu’il soit possible de récupérer ou non, mais vous décideriez alors à la place du code appelant qu’une situation est irrécupérable. En choisissant de renvoyer une valeur `Result`, vous laissez des possibilités au code appelant. Celui-ci peut tenter de récupérer d’une manière adaptée à sa situation, ou bien décider qu’une valeur `Err` est ici irrécupérable et appeler `panic!` pour transformer votre erreur récupérable en une erreur irrécupérable. Par conséquent, renvoyer `Result` est un bon choix par défaut lorsque vous définissez une fonction susceptible d’échouer.

Dans des situations telles que les exemples, le code de prototype et les tests, il est plus approprié d’écrire du code qui panique plutôt que de renvoyer `Result`. Voyons pourquoi, puis discutons des situations dans lesquelles le compilateur ne peut pas savoir que l’échec est impossible, mais où vous, en tant qu’humain, le pouvez. Ce chapitre se conclura par quelques recommandations générales pour décider s’il faut paniquer dans le code d’une bibliothèque.

### Exemples, code de prototype et tests

Lorsque vous écrivez un exemple pour illustrer un concept, y inclure également un code robuste de gestion des erreurs peut le rendre moins clair. Dans les exemples, on comprend qu’un appel à une méthode comme `unwrap`, qui peut paniquer, sert de substitut à la manière dont vous souhaiteriez que votre application gère les erreurs, ce qui peut varier selon le reste de votre code.

De même, les méthodes `unwrap` et `expect` sont très pratiques lors du prototypage, quand vous n’êtes pas encore prêt à décider comment gérer les erreurs. Elles laissent dans votre code des marqueurs clairs que vous pourrez repérer lorsque vous serez prêt à rendre votre programme plus robuste.

Si un appel de méthode échoue dans un test, vous voudrez que le test entier échoue, même si cette méthode ne correspond pas à la fonctionnalité testée. Comme `panic!` est le moyen de marquer un test comme ayant échoué, appeler `unwrap` ou `expect` est exactement ce qu’il faut faire.

<!-- Old headings. Do not remove or links may break. -->

<a id="cases-in-which-you-have-more-information-than-the-compiler"></a>

### Lorsque vous avez plus d’informations que le compilateur

Il peut également être approprié d’appeler `expect` lorsque vous disposez d’une autre logique qui garantit que le `Result` contiendra une valeur `Ok`, mais que le compilateur ne comprend pas cette logique. Vous aurez toujours une valeur `Result` à traiter : l’opération que vous appelez peut toujours échouer en général, même si cela est logiquement impossible dans votre situation particulière. Si vous pouvez vous assurer, en inspectant manuellement le code, que vous n’obtiendrez jamais de variante `Err`, il est tout à fait acceptable d’appeler `expect` et de documenter, dans le texte de son argument, la raison pour laquelle vous pensez ne jamais obtenir de variante `Err`. Voici un exemple :

```rust
{{#rustdoc_include ../listings/ch09-error-handling/no-listing-08-unwrap-that-cant-fail/src/main.rs:here}}
```

Nous créons une instance de `IpAddr` en analysant une chaîne codée en dur. Nous savons que `127.0.0.1` est une adresse IP valide ; il est donc acceptable d’utiliser `expect` ici. Cependant, le fait d’avoir une chaîne valide codée en dur ne change pas le type de retour de la méthode `parse` : nous obtenons toujours une valeur `Result`, et le compilateur nous obligera toujours à traiter ce `Result` comme si la variante `Err` était possible, car il n’est pas assez intelligent pour voir que cette chaîne est toujours une adresse IP valide. Si la chaîne représentant l’adresse IP provenait d’un utilisateur plutôt que d’être codée en dur dans le programme, et qu’un échec était donc possible, nous voudrions absolument traiter le `Result` de manière plus robuste. Mentionner que cette adresse IP est codée en dur nous incitera à remplacer `expect` par un code de gestion des erreurs plus adapté si, à l’avenir, nous devons obtenir l’adresse IP depuis une autre source.

### Recommandations pour la gestion des erreurs

Il est conseillé de faire paniquer votre code lorsqu’il est possible qu’il se retrouve dans un mauvais état. Dans ce contexte, un _mauvais état_ signifie qu’une hypothèse, une garantie, un contrat ou un invariant a été enfreint, par exemple lorsque des valeurs invalides, contradictoires ou manquantes sont transmises à votre code, et qu’une ou plusieurs des conditions suivantes sont réunies :

- Le mauvais état est inattendu, par opposition à quelque chose qui risque de se produire occasionnellement, comme lorsqu’un utilisateur saisit des données dans un format incorrect.
- Votre code, à partir de ce point, doit pouvoir compter sur le fait de ne pas se trouver dans ce mauvais état, au lieu de vérifier à chaque étape si le problème s’est produit.
- Il n’existe pas de bonne façon de représenter cette information dans les types que vous utilisez. Nous verrons un exemple de ce que nous entendons par là dans [« Encoder des états et des comportements avec des types »][encoding]<!-- ignore --> au chapitre 18.

Si quelqu’un appelle votre code et lui transmet des valeurs qui n’ont pas de sens, il vaut mieux renvoyer une erreur si vous le pouvez, afin que l’utilisateur de la bibliothèque puisse décider de la marche à suivre. Toutefois, dans les cas où continuer pourrait être dangereux ou préjudiciable, le meilleur choix peut être d’appeler `panic!` et de signaler à la personne qui utilise votre bibliothèque le bogue dans son code, afin qu’elle puisse le corriger pendant le développement. De même, `panic!` est souvent approprié si vous appelez du code externe que vous ne contrôlez pas et qui renvoie un état invalide que vous n’avez aucun moyen de corriger.

Cependant, lorsqu’un échec est attendu, il est plus approprié de renvoyer un `Result` que d’appeler `panic!`. Par exemple, un analyseur syntaxique peut recevoir des données mal formées, ou une requête HTTP peut renvoyer un statut indiquant que vous avez atteint une limite de débit. Dans ces cas, renvoyer un `Result` indique que l’échec est une possibilité attendue et que le code appelant doit décider comment le gérer.

Lorsque votre code effectue une opération susceptible de mettre un utilisateur en danger si elle est appelée avec des valeurs invalides, il doit d’abord vérifier que les valeurs sont valides et paniquer si elles ne le sont pas. C’est principalement une question de sécurité : tenter d’opérer sur des données invalides peut exposer votre code à des vulnérabilités. C’est la principale raison pour laquelle la bibliothèque standard appelle `panic!` si vous tentez d’accéder à un emplacement hors limites en mémoire : essayer d’accéder à une mémoire qui n’appartient pas à la structure de données actuelle est un problème de sécurité courant. Les fonctions ont souvent des _contrats_ : leur comportement n’est garanti que si les entrées satisfont à certaines exigences. Il est logique de paniquer lorsque le contrat est enfreint, car une telle violation indique toujours un bogue du côté de l’appelant, et ce n’est pas un type d’erreur que vous voulez obliger le code appelant à gérer explicitement. En fait, il n’existe aucun moyen raisonnable pour le code appelant de récupérer ; ce sont les _programmeurs_ qui appellent la fonction qui doivent corriger le code. Les contrats d’une fonction, en particulier lorsque leur violation provoquera une panique, doivent être expliqués dans sa documentation d’API.

Toutefois, ajouter de nombreuses vérifications d’erreurs dans toutes vos fonctions serait verbeux et fastidieux. Heureusement, vous pouvez utiliser le système de types de Rust (et donc la vérification des types effectuée par le compilateur) pour effectuer bon nombre de ces vérifications à votre place. Si votre fonction prend un type particulier en paramètre, vous pouvez poursuivre la logique de votre code en sachant que le compilateur a déjà vérifié que vous disposez d’une valeur valide. Par exemple, si vous avez un type plutôt qu’un `Option`, votre programme s’attend à avoir _quelque chose_ plutôt que _rien_. Votre code n’a alors pas à traiter deux cas correspondant aux variantes `Some` et `None` : il n’aura qu’un seul cas, celui où une valeur est assurément présente. Le code qui tenterait de ne rien transmettre à votre fonction ne compilerait même pas ; votre fonction n’a donc pas à vérifier ce cas à l’exécution. Un autre exemple consiste à utiliser un type d’entier non signé tel que `u32`, qui garantit que le paramètre n’est jamais négatif.

<!-- Old headings. Do not remove or links may break. -->

<a id="creating-custom-types-for-validation"></a>

### Types personnalisés pour la validation

Poussons un peu plus loin l’idée d’utiliser le système de types de Rust pour garantir que nous disposons d’une valeur valide, et voyons comment créer un type personnalisé à des fins de validation. Souvenez-vous du jeu de devinettes du chapitre 2, dans lequel notre code demandait à l’utilisateur de deviner un nombre entre 1 et 100. Nous ne vérifiions jamais que la proposition de l’utilisateur se trouvait dans cette plage avant de la comparer à notre nombre secret ; nous vérifiions seulement que la proposition était positive. Dans ce cas, les conséquences n’étaient pas très graves : notre réponse « Trop grand » ou « Trop petit » restait correcte. Mais il serait utile d’aider l’utilisateur à proposer des valeurs valides et d’adopter un comportement différent lorsqu’il devine un nombre hors plage, par rapport au cas où il saisit, par exemple, des lettres.

Une façon de procéder serait d’analyser la proposition comme un `i32` plutôt que comme un `u32`, afin d’autoriser les nombres potentiellement négatifs, puis d’ajouter une vérification pour s’assurer que le nombre se trouve dans la plage, comme ceci :

<Listing file-name="src/main.rs">

```rust,ignore
{{#rustdoc_include ../listings/ch09-error-handling/no-listing-09-guess-out-of-range/src/main.rs:here}}
```

</Listing>

L’expression `if` vérifie si notre valeur est hors plage, informe l’utilisateur du problème et appelle `continue` pour passer à l’itération suivante de la boucle et demander une autre proposition. Après l’expression `if`, nous pouvons procéder aux comparaisons entre `guess` et le nombre secret en sachant que `guess` se trouve entre 1 et 100.

Cependant, cette solution n’est pas idéale : si le programme devait absolument fonctionner uniquement avec des valeurs entre 1 et 100 et que de nombreuses fonctions avaient cette exigence, il serait fastidieux (et pourrait nuire aux performances) d’ajouter une vérification comme celle-ci dans chaque fonction.

Nous pouvons plutôt créer un nouveau type dans un module dédié et placer les validations dans une fonction qui crée une instance de ce type, plutôt que de répéter les validations partout. Ainsi, les fonctions peuvent utiliser sans risque le nouveau type dans leurs signatures et se fier aux valeurs qu’elles reçoivent. La liste 9-13 montre une façon de définir un type `Guess` qui ne crée une instance de `Guess` que si la fonction `new` reçoit une valeur comprise entre 1 et 100.

<Listing number="9-13" caption="Un type `Guess` qui n’accepte que des valeurs comprises entre 1 et 100" file-name="src/guessing_game.rs">

```rust
{{#rustdoc_include ../listings/ch09-error-handling/listing-09-13/src/guessing_game.rs}}
```

</Listing>

Notez que ce code dans *src/guessing_game.rs* dépend de l’ajout d’une déclaration de module `mod guessing_game;` dans *src/lib.rs*, que nous n’avons pas montrée ici. Dans le fichier de ce nouveau module, nous définissons une structure nommée `Guess` qui possède un champ nommé `value` contenant un `i32`. C’est là que le nombre sera stocké.

Ensuite, nous implémentons sur `Guess` une fonction associée nommée `new`, qui crée des instances de valeurs `Guess`. La fonction `new` est définie avec un paramètre nommé `value` de type `i32` et renvoie un `Guess`. Le code du corps de la fonction `new` vérifie que `value` se trouve entre 1 et 100. Si `value` ne satisfait pas cette vérification, nous appelons `panic!`, ce qui avertit le programmeur qui écrit le code appelant qu’il y a un bogue à corriger, car créer un `Guess` avec une valeur `value` hors de cette plage enfreindrait le contrat sur lequel repose `Guess::new`. Les conditions dans lesquelles `Guess::new` peut paniquer doivent être décrites dans sa documentation d’API publique ; nous aborderons au chapitre 14 les conventions de documentation permettant d’indiquer la possibilité d’un `panic!` dans la documentation d’API que vous créez. Si `value` satisfait la vérification, nous créons un nouveau `Guess`, définissons son champ `value` à partir du paramètre `value` et renvoyons le `Guess`.

Ensuite, nous implémentons une méthode nommée `value` qui emprunte `self`, ne prend aucun autre paramètre et renvoie un `i32`. Ce type de méthode est parfois appelé un _accesseur_ (_getter_), car son but est d’obtenir une donnée de ses champs et de la renvoyer. Cette méthode publique est nécessaire, car le champ `value` de la structure `Guess` est privé. Il est important que le champ `value` soit privé afin que le code qui utilise la structure `Guess` ne puisse pas définir directement `value` : le code situé en dehors du module `guessing_game` _doit_ utiliser la fonction `Guess::new` pour créer une instance de `Guess`, ce qui garantit qu’il est impossible qu’un `Guess` ait une valeur `value` qui n’a pas été vérifiée par les conditions de la fonction `Guess::new`.

Une fonction qui prend en paramètre ou renvoie uniquement des nombres entre 1 et 100 pourrait alors déclarer dans sa signature qu’elle prend ou renvoie un `Guess` plutôt qu’un `i32`, et n’aurait pas besoin d’effectuer de vérification supplémentaire dans son corps.

## Résumé

Les fonctionnalités de gestion des erreurs de Rust sont conçues pour vous aider à écrire du code plus robuste. La macro `panic!` signale que votre programme se trouve dans un état qu’il ne peut pas gérer et vous permet d’indiquer au processus de s’arrêter plutôt que de tenter de continuer avec des valeurs invalides ou incorrectes. L’énumération `Result` utilise le système de types de Rust pour indiquer que des opérations peuvent échouer d’une manière dont votre code pourrait se remettre. Vous pouvez utiliser `Result` pour indiquer au code qui appelle le vôtre qu’il doit également gérer les éventuels succès ou échecs. Utiliser `panic!` et `Result` dans les situations appropriées rendra votre code plus fiable face aux problèmes inévitables.

Maintenant que vous avez vu comment la bibliothèque standard utilise les génériques avec les énumérations `Option` et `Result`, nous allons parler du fonctionnement des génériques et de la manière de les utiliser dans votre code.

[encoding]: ch18-03-oo-design-patterns.html#encoding-states-and-behavior-as-types