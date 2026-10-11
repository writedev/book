## Stocker des clés et leurs valeurs associées dans des tables de hachage

La dernière de nos collections courantes est la table de hachage. Le type `HashMap<K, V>` stocke une association entre des clés de type `K` et des valeurs de type `V` à l’aide d’une _fonction de hachage_, qui détermine comment ces clés et ces valeurs sont placées en mémoire. De nombreux langages de programmation prennent en charge ce type de structure de données, mais lui donnent souvent un autre nom, comme _hash_, _map_, _objet_, _table de hachage_, _dictionnaire_ ou _tableau associatif_, pour n’en citer que quelques-uns.

Les tables de hachage sont utiles lorsque vous souhaitez rechercher des données non pas à l’aide d’un indice, comme vous pouvez le faire avec les vecteurs, mais à l’aide d’une clé qui peut être de n’importe quel type. Par exemple, dans un jeu, vous pourriez suivre le score de chaque équipe dans une table de hachage où chaque clé est le nom d’une équipe et chaque valeur est son score. À partir du nom d’une équipe, vous pouvez retrouver son score.

Nous allons passer en revue l’API de base des tables de hachage dans cette section, mais la bibliothèque standard définit de nombreuses autres fonctions utiles pour `HashMap<K, V>`. Comme toujours, consultez la documentation de la bibliothèque standard pour en savoir plus.

### Créer une nouvelle table de hachage

Une façon de créer une table de hachage vide consiste à utiliser `new` et à ajouter des éléments avec `insert`. Dans l’exemple 8-20, nous suivons les scores de deux équipes nommées _Blue_ et _Yellow_. L’équipe Blue commence avec 10 points et l’équipe Yellow avec 50.

<Listing number="8-20" caption="Créer une nouvelle table de hachage et y insérer des clés et des valeurs">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-20/src/main.rs:here}}
```

</Listing>

Notez que nous devons d’abord importer `HashMap` depuis la partie collections de la bibliothèque standard. Parmi nos trois collections courantes, c’est la moins utilisée ; elle ne fait donc pas partie des éléments automatiquement importés dans la portée par le préambule. La bibliothèque standard offre également moins de fonctionnalités pour les tables de hachage ; il n’existe par exemple aucune macro intégrée pour les construire.

Comme les vecteurs, les tables de hachage stockent leurs données sur le tas. Cette `HashMap` a des clés de type `String` et des valeurs de type `i32`. Comme les vecteurs, les tables de hachage sont homogènes : toutes les clés doivent être du même type, et toutes les valeurs doivent être du même type.

### Accéder aux valeurs d’une table de hachage

Nous pouvons récupérer une valeur de la table de hachage en transmettant sa clé à la méthode `get`, comme le montre l’exemple 8-21.

<Listing number="8-21" caption="Accéder au score de l’équipe Blue stocké dans la table de hachage">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-21/src/main.rs:here}}
```

</Listing>

Ici, `score` aura la valeur associée à l’équipe Blue, et le résultat sera `10`. La méthode `get` renvoie un `Option<&V>` ; si aucune valeur n’est associée à cette clé dans la table de hachage, `get` renvoie `None`. Ce programme gère l’`Option` en appelant `copied` pour obtenir un `Option<i32>` plutôt qu’un `Option<&i32>`, puis `unwrap_or` pour définir `score` à zéro si `scores` ne contient pas d’entrée pour la clé.

Nous pouvons parcourir chaque paire clé-valeur d’une table de hachage de la même manière que pour les vecteurs, à l’aide d’une boucle `for` :

```rust
{{#rustdoc_include ../listings/ch08-common-collections/no-listing-03-iterate-over-hashmap/src/main.rs:here}}
```

Ce code affichera chaque paire dans un ordre arbitraire :

```text
Yellow: 50
Blue: 10
```

<!-- Old headings. Do not remove or links may break. -->

<a id="hash-maps-and-ownership"></a>

### Gérer la propriété dans les tables de hachage

Pour les types qui implémentent le trait `Copy`, comme `i32`, les valeurs sont copiées dans la table de hachage. Pour les valeurs possédées comme `String`, elles sont déplacées et la table de hachage en devient propriétaire, comme le montre l’exemple 8-22.

<Listing number="8-22" caption="Montrer que les clés et les valeurs appartiennent à la table de hachage une fois insérées">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-22/src/main.rs:here}}
```

</Listing>

Nous ne pouvons pas utiliser les variables `field_name` et `field_value` après leur déplacement dans la table de hachage lors de l’appel à `insert`.

Si nous insérons dans la table de hachage des références à des valeurs, celles-ci ne sont pas déplacées dans la table. Les valeurs vers lesquelles pointent les références doivent rester valides au moins aussi longtemps que la table de hachage. Nous approfondirons ces questions au [chapitre 10](ch10-03-lifetime-syntax.html#validating-references-with-lifetimes), dans la section [« Valider les références avec les durées de vie »][validating-references-with-lifetimes]<!-- ignore -->.

### Mettre à jour une table de hachage

Le nombre de paires clé-valeur peut augmenter, mais chaque clé unique ne peut être associée qu’à une seule valeur à la fois (mais pas l’inverse : par exemple, les équipes Blue et Yellow pourraient toutes deux avoir la valeur `10` dans la table de hachage `scores`).

Lorsque vous souhaitez modifier les données d’une table de hachage, vous devez décider comment gérer le cas où une clé possède déjà une valeur. Vous pouvez remplacer l’ancienne valeur par la nouvelle et ignorer complètement l’ancienne. Vous pouvez conserver l’ancienne valeur et ignorer la nouvelle, en ajoutant cette dernière uniquement si la clé n’a _pas_ déjà de valeur. Ou vous pouvez combiner l’ancienne valeur et la nouvelle. Voyons comment procéder dans chacun de ces cas !

#### Remplacer une valeur

Si nous insérons une clé et une valeur dans une table de hachage, puis insérons cette même clé avec une valeur différente, la valeur associée à cette clé sera remplacée. Même si le code de l’exemple 8-23 appelle `insert` deux fois, la table de hachage ne contiendra qu’une seule paire clé-valeur, car nous insérons les deux fois une valeur pour la clé de l’équipe Blue.

<Listing number="8-23" caption="Remplacer la valeur associée à une clé donnée">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-23/src/main.rs:here}}
```

</Listing>

Ce code affichera `{"Blue": 25}`. La valeur d’origine, `10`, a été remplacée.

<!-- Old headings. Do not remove or links may break. -->

<a id="only-inserting-a-value-if-the-key-has-no-value"></a>

#### Ajouter une clé et une valeur uniquement si la clé n’est pas déjà présente

Il est courant de vérifier si une clé donnée existe déjà dans la table de hachage avec une valeur, puis d’agir en conséquence : si la clé existe, la valeur actuelle doit rester inchangée ; si elle n’existe pas, on l’insère avec une valeur.

Les tables de hachage disposent d’une API spéciale pour cela, appelée `entry`, qui prend en paramètre la clé à vérifier. La valeur renvoyée par la méthode `entry` est une énumération appelée `Entry`, qui représente une valeur susceptible d’exister ou non. Supposons que nous voulions vérifier si la clé de l’équipe Yellow est associée à une valeur. Si ce n’est pas le cas, nous voulons insérer la valeur `50`, et faire de même pour l’équipe Blue. Avec l’API `entry`, le code ressemble à celui de l’exemple 8-24.

<Listing number="8-24" caption="Utiliser la méthode `entry` pour n’insérer une valeur que si la clé n’en possède pas déjà une">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-24/src/main.rs:here}}
```

</Listing>

La méthode `or_insert` de `Entry` est définie de façon à renvoyer une référence mutable à la valeur associée à la clé de l’`Entry` si cette clé existe. Sinon, elle insère le paramètre comme nouvelle valeur pour cette clé et renvoie une référence mutable vers cette nouvelle valeur. Cette technique est beaucoup plus claire que d’écrire nous-mêmes la logique et, de plus, elle s’accorde mieux avec le vérificateur d’emprunts.

L’exécution du code de l’exemple 8-24 affichera `{"Yellow": 50, "Blue": 10}`. Le premier appel à `entry` insère la clé de l’équipe Yellow avec la valeur `50`, car cette équipe n’a pas encore de valeur. Le deuxième appel à `entry` ne modifie pas la table de hachage, car l’équipe Blue a déjà la valeur `10`.

#### Mettre à jour une valeur en fonction de l’ancienne valeur

Un autre cas d’utilisation courant des tables de hachage consiste à rechercher la valeur associée à une clé, puis à la mettre à jour en fonction de l’ancienne valeur. Par exemple, l’exemple 8-25 présente du code qui compte le nombre d’occurrences de chaque mot dans un texte. Nous utilisons une table de hachage dont les clés sont les mots et incrémentons les valeurs pour compter le nombre de fois où nous avons vu chaque mot. Si c’est la première fois que nous voyons un mot, nous insérons d’abord la valeur `0`.

<Listing number="8-25" caption="Compter les occurrences de mots à l’aide d’une table de hachage qui stocke les mots et leur nombre d’occurrences">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-25/src/main.rs:here}}
```

</Listing>

Ce code affichera `{"world": 2, "hello": 1, "wonderful": 1}`. Il se peut que les mêmes paires clé-valeur soient affichées dans un ordre différent : rappelez-vous que, comme nous l’avons vu dans [« Accéder aux valeurs d’une table de hachage »][access]<!-- ignore -->, le parcours d’une table de hachage s’effectue dans un ordre arbitraire.

La méthode `split_whitespace` renvoie un itérateur sur les sous-tranches de la valeur de `text`, séparées par des espaces blancs. La méthode `or_insert` renvoie une référence mutable (`&mut V`) à la valeur associée à la clé indiquée. Ici, nous stockons cette référence mutable dans la variable `count` ; pour affecter cette valeur, nous devons donc d’abord déréférencer `count` à l’aide de l’astérisque (`*`). La référence mutable sort de portée à la fin de la boucle `for`, ce qui rend toutes ces modifications sûres et autorisées par les règles d’emprunt.

### Fonctions de hachage

Par défaut, `HashMap` utilise une fonction de hachage appelée _SipHash_, qui peut protéger contre les attaques par déni de service (DoS) visant les tables de hachage[^siphash]<!-- ignore -->. Ce n’est pas l’algorithme de hachage le plus rapide qui soit, mais le gain de sécurité obtenu au prix d’une baisse des performances en vaut la peine. Si le profilage de votre code révèle que la fonction de hachage par défaut est trop lente pour vos besoins, vous pouvez en utiliser une autre en indiquant un hasher différent. Un _hasher_ est un type qui implémente le trait `BuildHasher`. Nous parlerons des traits et de leur implémentation au [chapitre 10][traits]<!-- ignore -->. Vous n’avez pas nécessairement à implémenter votre propre hasher à partir de zéro ; [crates.io](https://crates.io/)<!-- ignore --> propose des bibliothèques partagées par d’autres utilisateurs de Rust qui fournissent des hashers implémentant de nombreux algorithmes de hachage courants.

[^siphash]: [https://en.wikipedia.org/wiki/SipHash](https://en.wikipedia.org/wiki/SipHash)

## Résumé

Les vecteurs, les chaînes de caractères et les tables de hachage offrent une grande partie des fonctionnalités nécessaires aux programmes qui doivent stocker, consulter et modifier des données. Voici quelques exercices que vous devriez maintenant être en mesure de résoudre :

1. À partir d’une liste d’entiers, utilisez un vecteur et renvoyez la médiane (une fois la liste triée, la valeur en position centrale) et le mode (la valeur la plus fréquente ; une table de hachage sera utile ici) de la liste.
1. Convertissez des chaînes de caractères en Pig Latin. La première consonne de chaque mot est déplacée à la fin du mot et _ay_ est ajouté, de sorte que _first_ devient _irst-fay_. Les mots commençant par une voyelle reçoivent plutôt _hay_ à la fin (_apple_ devient _apple-hay_). Gardez à l’esprit les détails de l’encodage UTF-8 !
1. À l’aide d’une table de hachage et de vecteurs, créez une interface textuelle permettant à une personne d’ajouter des noms d’employés à un service d’une entreprise ; par exemple, « Ajouter Sally au service Ingénierie » ou « Ajouter Amir au service Ventes ». Permettez ensuite de récupérer la liste de toutes les personnes d’un service ou de toutes les personnes de l’entreprise, classées par service et par ordre alphabétique.

La documentation de l’API de la bibliothèque standard décrit des méthodes des vecteurs, des chaînes de caractères et des tables de hachage qui vous seront utiles pour ces exercices !

Nous abordons des programmes plus complexes, dans lesquels des opérations peuvent échouer : c’est le moment idéal pour parler de la gestion des erreurs. C’est ce que nous ferons ensuite !

[validating-references-with-lifetimes]: ch10-03-lifetime-syntax.html#validating-references-with-lifetimes
[access]: #accessing-values-in-a-hash-map
[traits]: ch10-02-traits.html