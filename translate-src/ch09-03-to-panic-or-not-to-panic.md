## À `panic!` ou Pas à `panic!`

Alors, comment décidez-vous quand appeler `panic!` et quand vous devriez retourner un `Result` ? Lorsque le code panique, il n’y a aucun moyen de récupérer. Vous pourriez appeler `panic!` pour n’importe quelle situation d’erreur, qu’il soit possible de se remettre d’une erreur ou non, mais vous prenez alors la décision qu’une situation est irrécupérable au nom du code appelant. Lorsque vous choisissez de retourner une valeur `Result`, vous donnez au code appelant des options. Le code appelant pourrait choisir de tenter de récupérer d'une manière qui lui convient, ou il pourrait décider qu'une valeur `Err` dans ce cas est irrécupérable, et donc appeler `panic!` et transformer votre erreur récupérable en une erreur irrécupérable. Par conséquent, retourner un `Result` est un bon choix par défaut lorsque vous définissez une fonction qui pourrait échouer.

Dans des situations telles que des exemples, du code prototype et des tests, il est plus approprié d’écrire du code qui panique plutôt que de retourner un `Result`. Explorons pourquoi, puis discutons des situations dans lesquelles le compilateur ne peut pas dire qu’un échec est impossible, mais vous en tant qu’humain pouvez le faire. Le chapitre se conclura par quelques lignes directrices sur la manière de décider si vous devez paniquer dans le code de bibliothèque.

### Exemples, Code Prototype et Tests

Lorsque vous écrivez un exemple pour illustrer un concept, inclure également un code de gestion des erreurs robuste peut rendre l'exemple moins clair. Dans les exemples, il est entendu qu'un appel à une méthode comme `unwrap` qui pourrait paniquer est censé être un espace réservé pour la manière dont vous souhaitez que votre application gère les erreurs, ce qui peut différer en fonction de ce que fait le reste de votre code.

De même, les méthodes `unwrap` et `expect` sont très pratiques lorsque vous prototypiez et que vous n’êtes pas encore prêt à décider comment gérer les erreurs. Elles laissent des marqueurs clairs dans votre code pour lorsque vous êtes prêt à rendre votre programme plus robuste.

Si un appel de méthode échoue dans un test, vous voudrez que l’ensemble du test échoue, même si cette méthode n'est pas la fonctionnalité testée. Parce que `panic!` est comment un test est marqué comme un échec, appeler `unwrap` ou `expect` est exactement ce qui doit arriver.

### Quand Vous Avez Plus d'Information Que le Compilateur

Il serait également approprié d'appeler `expect` lorsque vous avez une autre logique qui garantit que le `Result` aura une valeur `Ok`, mais que la logique n’est pas quelque chose que le compilateur comprend. Vous aurez toujours une valeur `Result` que vous devez traiter : Quel que soit l’opération que vous appelez, elle a toujours la possibilité d’échouer en général, même s’il est logiquement impossible dans votre situation particulière. Si vous pouvez vous assurer en inspectant manuellement le code que vous n’aurez jamais une variante `Err`, il est tout à fait acceptable d'appeler `expect` et de documenter la raison pour laquelle vous pensez que vous n’aurez jamais une variante `Err` dans le texte de l’argument. Voici un exemple :

```rust
{{#rustdoc_include ../listings/ch09-error-handling/no-listing-08-unwrap-that-cant-fail/src/main.rs:here}}
```

Nous créons une instance `IpAddr` en analysant une chaîne codée en dur. Nous pouvons voir que `127.0.0.1` est une adresse IP valide, il est donc acceptable d'utiliser `expect` ici. Cependant, avoir une chaîne valide codée en dur ne change pas le type de retour de la méthode `parse` : Nous obtenons toujours une valeur `Result`, et le compilateur exigera toujours que nous traitions le `Result` comme si la variante `Err` était une possibilité, car le compilateur n'est pas assez intelligent pour voir que cette chaîne est toujours une adresse IP valide. Si la chaîne d’adresse IP provenait d’un utilisateur plutôt que d’être codée en dur dans le programme et avait donc une réelle possibilité d’échec, nous devrions définitivement gérer le `Result` de manière plus robuste. Mentionner l'hypothèse selon laquelle cette adresse IP est codée en dur nous incitera à changer `expect` par un code de gestion des erreurs meilleur si, à l'avenir, nous devons obtenir l'adresse IP d'une autre source.

### Lignes Directrices pour la Gestion des Erreurs

Il est conseillé de faire paniquer votre code lorsqu'il est possible que votre code puisse se retrouver dans un mauvais état. Dans ce contexte, un _mauvais état_ est lorsque certaines hypothèses, garanties, contrats ou invariants ont été brisés, comme lorsque des valeurs invalides, contradictoires ou manquantes sont passées à votre code, plus un ou plusieurs des éléments suivants :

- Le mauvais état est quelque chose d'inattendu, contrairement à quelque chose qui est susceptible de se produire occasionnellement, comme un utilisateur saisissant des données dans le mauvais format.
- Votre code après ce point doit compter sur le fait de ne pas être dans cet état mauvais, plutôt que de vérifier le problème à chaque étape.
- Il n’y a pas de bonne manière d’encoder cette information dans les types que vous utilisez. Nous allons travailler sur un exemple de ce que nous voulons dire dans [“Encoder des États et Comportements en Types”][encoding]<!-- ignore --> dans le Chapitre 18.

Si quelqu'un appelle votre code et passe des valeurs qui n'ont pas de sens, il est préférable de retourner une erreur si vous le pouvez afin que l’utilisateur de la bibliothèque puisse décider ce qu'il souhaite faire dans ce cas. Cependant, dans les cas où continuer pourrait être dangereux ou nuisible, le meilleur choix pourrait être d'appeler `panic!` et d’alerter la personne utilisant votre bibliothèque sur le bug dans son code afin qu’elle puisse le corriger pendant le développement. De même, `panic!` est souvent approprié si vous appelez un code externe qui échappe à votre contrôle et renvoie un état invalide que vous n'avez aucun moyen de corriger.

Cependant, lorsque l'échec est attendu, il est plus approprié de retourner un `Result` que de faire un appel à `panic!`. Des exemples incluent un analyseur recevant des données malformées ou une requête HTTP retournant un statut indiquant que vous avez atteint une limite de fréquence. Dans ces cas, retourner un `Result` indique que l'échec est une possibilité attendue que le code appelant doit décider comment gérer.

Lorsque votre code effectue une opération qui pourrait mettre un utilisateur en danger s'il est appelé avec des valeurs invalides, votre code devrait vérifier que les valeurs sont valides d'abord et paniquer si les valeurs ne sont pas valides. C'est principalement pour des raisons de sécurité : Tenter d'opérer sur des données invalides peut exposer votre code à des vulnérabilités. C'est la principale raison pour laquelle la bibliothèque standard appelera `panic!` si vous tentez un accès mémoire en dehors des limites : Essayer d'accéder à une mémoire qui n'appartient pas à la structure de données actuelle est un problème de sécurité courant. Les fonctions ont souvent des _contrats_ : Leur comportement n'est garanti que si les entrées répondent à des exigences particulières. Faire paniquer lorsque le contrat est violé a du sens parce qu'une violation de contrat indique toujours un bug côté appelant, et ce n'est pas un type d'erreur que vous voulez que le code appelant ait à gérer explicitement. En fait, il n'y a aucune manière raisonnable pour le code appelant de se rétablir ; les _programmeurs_ appelants doivent corriger le code. Les contrats pour une fonction, surtout lorsque la violation entraînera une panique, doivent être expliqués dans la documentation API publique de la fonction.

Cependant, avoir beaucoup de vérifications d'erreurs dans toutes vos fonctions serait verbeux et ennuyeux. Heureusement, vous pouvez utiliser le système de types de Rust (et donc la vérification de types effectuée par le compilateur) pour effectuer de nombreuses vérifications pour vous. Si votre fonction a un type particulier comme paramètre, vous pouvez poursuivre la logique de votre code en sachant que le compilateur a déjà garanti que vous avez une valeur valide. Par exemple, si vous avez un type plutôt qu'un `Option`, votre programme s'attend à avoir _quelque chose_ plutôt que _rien_. Votre code n’a donc pas à gérer deux cas pour les variantes `Some` et `None` : Il n'aura qu'un seul cas pour avoir définitivement une valeur. Le code tentant de passer rien à votre fonction ne compilera même pas, donc votre fonction n’a pas à vérifier ce cas à l'exécution. Un autre exemple est l'utilisation d'un type entier non signé tel que `u32`, qui garantit que le paramètre n'est jamais négatif.

### Types Personnalisés pour la Validation

Prenons l’idée d’utiliser le système de types de Rust pour nous assurer que nous avons une valeur valide un peu plus loin et examinons la création d’un type personnalisé pour la validation. Rappelez-vous du jeu de devinettes dans le Chapitre 2 dans lequel notre code demandait à l’utilisateur de deviner un nombre entre 1 et 100. Nous n’avons jamais validé que la devinette de l’utilisateur était comprise entre ces nombres avant de la comparer à notre nombre secret ; nous avons seulement validé que la devinette était positive. Dans ce cas, les conséquences n’étaient pas très graves : Notre sortie “Trop haut” ou “Trop bas” serait toujours correcte. Mais il serait utile d'orienter l'utilisateur vers des devinettes valides et d'avoir un comportement différent lorsque l'utilisateur devine un nombre qui est hors de portée par rapport à quand l'utilisateur tape, par exemple, des lettres.

Une façon de faire cela serait d’analyser la devinette comme un `i32` au lieu de seulement un `u32` pour permettre des nombres potentiellement négatifs, puis d’ajouter une vérification pour que le nombre soit dans la plage, comme suit :

<Listing file-name="src/main.rs">

```rust,ignore
{{#rustdoc_include ../listings/ch09-error-handling/no-listing-09-guess-out-of-range/src/main.rs:here}}
```

</Listing>

L’expression `if` vérifie si notre valeur est hors de portée, informe l'utilisateur du problème et appelle `continue` pour commencer la prochaine itération de la boucle et demander une autre devinette. Après l’expression `if`, nous pouvons poursuivre les comparaisons entre `guess` et le nombre secret en sachant que `guess` est compris entre 1 et 100.

Cependant, ce n'est pas une solution idéale : S'il était absolument critique que le programme n'opère qu'avec des valeurs comprises entre 1 et 100, et qu'il avait de nombreuses fonctions ayant cette exigence, avoir une vérification comme celle-ci dans chaque fonction serait fastidieux (et pourrait affecter la performance).

Au lieu de cela, nous pouvons créer un nouveau type dans un module dédié et mettre les validations dans une fonction pour créer une instance du type plutôt que de répéter les validations partout. Ainsi, il est sûr pour les fonctions d'utiliser le nouveau type dans leurs signatures et d'utiliser les valeurs qu'elles reçoivent en toute confiance. Le listing 9-13 montre une façon de définir un type `Guess` qui ne créera une instance de `Guess` que si la fonction `new` reçoit une valeur comprise entre 1 et 100.

<Listing number="9-13" caption="Un type `Guess` qui ne continuera qu'avec des valeurs comprises entre 1 et 100" file-name="src/guessing_game.rs">

```rust
{{#rustdoc_include ../listings/ch09-error-handling/listing-09-13/src/guessing_game.rs}}
```

</Listing>

Notez que ce code dans *src/guessing_game.rs* dépend de l'ajout d'une déclaration de module `mod guessing_game;` dans *src/lib.rs* que nous n'avons pas montré ici. Dans le fichier du nouveau module, nous définissons une struct nommée `Guess` qui a un champ nommé `value` qui contient un `i32`. C’est là où le nombre sera stocké.

Ensuite, nous implémentons une fonction associée nommée `new` sur `Guess` qui crée des instances de valeurs `Guess`. La fonction `new` est définie pour avoir un paramètre nommé `value` de type `i32` et pour retourner un `Guess`. Le code à l'intérieur de la fonction `new` teste `value` pour s'assurer qu'il est compris entre 1 et 100. Si `value` ne réussit pas ce test, nous appelons `panic!`, ce qui alertera le programmeur qui écrit le code appelant qu'il a un bug à corriger, car créer un `Guess` avec une `value` en dehors de cette plage violerait le contrat sur lequel `Guess::new` repose. Les conditions dans lesquelles `Guess::new` pourrait paniquer devraient être discutées dans sa documentation API publique ; nous aborderons les conventions de documentation indiquant la possibilité d’un `panic!` dans la documentation API que vous créez au Chapitre 14. Si `value` passe le test, nous créons un nouveau `Guess` avec son champ `value` défini sur le paramètre `value` et retournons le `Guess`.

Enfin, nous implémentons une méthode nommée `value` qui emprunte `self`, n’a pas d'autres paramètres et retourne un `i32`. Ce type de méthode est parfois appelé un _getter_ car son but est d'obtenir certaines données de ses champs et de les retourner. Cette méthode publique est nécessaire car le champ `value` de la struct `Guess` est privée. Il est important que le champ `value` soit privé pour que le code utilisant la struct `Guess` ne puisse pas définir `value` directement : Le code en dehors du module `guessing_game` _doit_ utiliser la fonction `Guess::new` pour créer une instance de `Guess`, garantissant ainsi qu'il n'y a aucune possibilité qu'un `Guess` ait une `value` qui n'ait pas été vérifiée par les conditions dans la fonction `Guess::new`.

Une fonction qui a un paramètre ou retourne uniquement des nombres entre 1 et 100 pourrait alors déclarer dans sa signature qu'elle accepte ou retourne un `Guess` plutôt qu'un `i32` et n’aurait pas besoin de faire de vérifications supplémentaires dans son corps.

## Résumé

Les fonctionnalités de gestion des erreurs de Rust sont conçues pour vous aider à écrire un code plus robuste. La macro `panic!` signale que votre programme est dans un état qu'il ne peut pas gérer et vous permet de dire au processus de s'arrêter au lieu d'essayer de continuer avec des valeurs invalides ou incorrectes. L'énumération `Result` utilise le système de types de Rust pour indiquer que les opérations peuvent échouer d'une manière dont votre code pourrait se remettre. Vous pouvez utiliser `Result` pour informer le code qui appelle le vôtre qu'il doit gérer le succès potentiel ou l'échec également. Utiliser `panic!` et `Result` dans les situations appropriées rendra votre code plus fiable face à des problèmes inévitables.

Maintenant que vous avez vu des moyens utiles dont la bibliothèque standard utilise des génériques avec les énumérations `Option` et `Result`, nous allons parler de la manière dont les génériques fonctionnent et comment vous pouvez les utiliser dans votre code.

[encoding]: ch18-03-oo-design-patterns.html#encoding-states-and-behavior-as-types