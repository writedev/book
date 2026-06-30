## Stockage de clés avec des valeurs associées dans les tables de hachage

La dernière de nos collections courantes est la table de hachage. Le type `HashMap<K, V>` stocke une correspondance de clés de type `K` à des valeurs de type `V` en utilisant une _fonction de hachage_, qui détermine comment il place ces clés et valeurs en mémoire. De nombreux langages de programmation prennent en charge ce type de structure de données, mais ils utilisent souvent un nom différent, comme _hash_, _map_, _object_, _table de hachage_, _dictionnaire_ ou _tableau associatif_, pour en citer quelques-uns.

Les tables de hachage sont utiles lorsque vous souhaitez rechercher des données non pas en utilisant un index, comme vous pouvez le faire avec des vecteurs, mais en utilisant une clé qui peut être de n'importe quel type. Par exemple, dans un jeu, vous pourriez suivre le score de chaque équipe dans une table de hachage où chaque clé est le nom d'une équipe et les valeurs sont le score de chaque équipe. Étant donné un nom d'équipe, vous pouvez récupérer son score.

Nous allons passer en revue l'API de base des tables de hachage dans cette section, mais de nombreuses autres fonctionnalités se cachent dans les fonctions définies sur `HashMap<K, V>` par la bibliothèque standard. Comme toujours, consultez la documentation de la bibliothèque standard pour plus d'informations.

### Création d'une nouvelle table de hachage

Une façon de créer une table de hachage vide est d'utiliser `new` et d'ajouter des éléments avec `insert`. Dans la liste 8-20, nous suivons les scores de deux équipes dont les noms sont _Blue_ et _Yellow_. L'équipe Blue commence avec 10 points, et l'équipe Yellow commence avec 50.

<Listing number="8-20" caption="Création d'une nouvelle table de hachage et insertion de quelques clés et valeurs">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-20/src/main.rs:here}}
```

</Listing>

Notez que nous devons d'abord `use` le `HashMap` de la partie collections de la bibliothèque standard. De nos trois collections communes, celle-ci est la moins fréquemment utilisée, elle n'est donc pas incluse dans les fonctionnalités apportées dans le champ d'application automatiquement dans le préambule. Les tables de hachage ont également moins de support de la bibliothèque standard ; il n'y a pas de macro intégrée pour les construire, par exemple.

Tout comme les vecteurs, les tables de hachage stockent leurs données sur le tas. Ce `HashMap` a des clés de type `String` et des valeurs de type `i32`. Comme les vecteurs, les tables de hachage sont homogènes : toutes les clés doivent avoir le même type, et toutes les valeurs doivent avoir le même type.

### Accès aux valeurs dans une table de hachage

Nous pouvons obtenir une valeur de la table de hachage en fournissant sa clé à la méthode `get`, comme le montre la liste 8-21.

<Listing number="8-21" caption="Accéder au score de l'équipe Blue stocké dans la table de hachage">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-21/src/main.rs:here}}
```

</Listing>

Ici, `score` aura la valeur associée à l'équipe Blue, et le résultat sera `10`. La méthode `get` retourne un `Option<&V>` ; s'il n'y a pas de valeur pour cette clé dans la table de hachage, `get` retournera `None`. Ce programme gère l’`Option` en appelant `copied` pour obtenir un `Option<i32>` plutôt qu'un `Option<&i32>`, puis `unwrap_or` pour définir `score` à zéro si `scores` n'a pas d'entrée pour la clé.

Nous pouvons itérer sur chaque paire clé-valeur dans une table de hachage de manière similaire à ce que nous faisons avec des vecteurs, en utilisant une boucle `for` :

```rust
{{#rustdoc_include ../listings/ch08-common-collections/no-listing-03-iterate-over-hashmap/src/main.rs:here}}
```

Ce code affichera chaque paire dans un ordre arbitraire :

```text
Yellow: 50
Blue: 10
```

<a id="hash-maps-and-ownership"></a>

### Gestion de la propriété dans les tables de hachage

Pour les types qui implémentent le trait `Copy`, comme `i32`, les valeurs sont copiées dans la table de hachage. Pour les valeurs possédées, comme `String`, les valeurs seront déplacées et la table de hachage sera le propriétaire de ces valeurs, comme démontré dans la liste 8-22.

<Listing number="8-22" caption="Montrer que les clés et les valeurs appartiennent à la table de hachage une fois qu'elles sont insérées">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-22/src/main.rs:here}}
```

</Listing>

Nous ne pouvons pas utiliser les variables `field_name` et `field_value` après qu'elles ont été déplacées dans la table de hachage avec l'appel à `insert`.

Si nous insérons des références à des valeurs dans la table de hachage, les valeurs ne seront pas déplacées dans la table de hachage. Les valeurs auxquelles les références pointent doivent être valides aussi longtemps que la table de hachage est valide. Nous parlerons davantage de ces problèmes dans [“Validation des références avec
les durées de vie”][validating-references-with-lifetimes] dans le chapitre 10.

### Mise à jour d'une table de hachage

Bien que le nombre de paires clé-valeur soit extensible, chaque clé unique ne peut avoir qu'une seule valeur associée à la fois (mais pas vice versa : par exemple, les équipes Blue et Yellow pourraient toutes deux avoir la valeur `10` stockée dans la table de hachage `scores`).

Lorsque vous souhaitez modifier les données dans une table de hachage, vous devez décider comment gérer le cas où une clé a déjà une valeur assignée. Vous pourriez remplacer l'ancienne valeur par la nouvelle valeur, en négligeant complètement l'ancienne valeur. Vous pourriez conserver l'ancienne valeur et ignorer la nouvelle valeur, en ajoutant la nouvelle valeur seulement si la clé _n'a pas_ déjà de valeur. Ou vous pourriez combiner l'ancienne valeur et la nouvelle valeur. Voyons comment faire chacune de ces options !

#### Écrasement d'une valeur

Si nous insérons une clé et une valeur dans une table de hachage, puis insérons cette même clé avec une valeur différente, la valeur associée à cette clé sera remplacée. Bien que le code dans la liste 8-23 appelle `insert` deux fois, la table de hachage ne contiendra qu'une seule paire clé-valeur car nous insérons la valeur associée à la clé de l'équipe Blue deux fois.

<Listing number="8-23" caption="Remplacer une valeur stockée avec une clé particulière">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-23/src/main.rs:here}}
```

</Listing>

Ce code affichera `{"Blue": 25}`. La valeur originale de `10` a été écrasée.

<a id="only-inserting-a-value-if-the-key-has-no-value"></a>

#### Ajout d'une clé et d'une valeur uniquement si une clé n'est pas présente

Il est courant de vérifier si une clé particulière existe déjà dans la table de hachage avec une valeur, puis de prendre les actions suivantes : Si la clé existe dans la table de hachage, la valeur existante doit rester telle quelle ; si la clé n'existe pas, insérez-la et une valeur pour celle-ci.

Les tables de hachage ont une API spéciale pour cela appelée `entry` qui prend la clé que vous souhaitez vérifier comme paramètre. La valeur de retour de la méthode `entry` est un enum appelé `Entry` qui représente une valeur qui pourrait ou non exister. Disons que nous voulons vérifier si la clé de l'équipe Yellow a une valeur associée. Si ce n'est pas le cas, nous voulons insérer la valeur `50`, et il en va de même pour l'équipe Blue. En utilisant l'API `entry`, le code ressemble à la liste 8-24.

<Listing number="8-24" caption="Utilisation de la méthode `entry` pour insérer uniquement si la clé n'a pas déjà de valeur">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-24/src/main.rs:here}}
```

</Listing>

La méthode `or_insert` sur `Entry` est définie pour retourner une référence mutable à la valeur pour la clé `Entry` correspondante si cette clé existe, et si ce n'est pas le cas, elle insère le paramètre comme nouvelle valeur pour cette clé et retourne une référence mutable à la nouvelle valeur. Cette technique est beaucoup plus propre que d'écrire la logique nous-mêmes et, de plus, elle fonctionne mieux avec le vérificateur d'emprunts.

L'exécution du code dans la liste 8-24 affichera `{"Yellow": 50, "Blue": 10}`. Le premier appel à `entry` insérera la clé pour l'équipe Yellow avec la valeur `50` car l'équipe Yellow n'a pas encore de valeur. Le deuxième appel à `entry` ne modifiera pas la table de hachage, car l'équipe Blue a déjà la valeur `10`.

#### Mise à jour d'une valeur en fonction de l'ancienne valeur

Un autre cas d'utilisation courant pour les tables de hachage est de rechercher la valeur d'une clé, puis de la mettre à jour en fonction de l'ancienne valeur. Par exemple, la liste 8-25 montre un code qui compte combien de fois chaque mot apparaît dans un texte. Nous utilisons une table de hachage avec les mots comme clés et incrémentons la valeur pour garder une trace du nombre de fois que nous avons vu ce mot. Si c'est la première fois que nous voyons un mot, nous insérerons d'abord la valeur `0`.

<Listing number="8-25" caption="Compter les occurrences de mots à l'aide d'une table de hachage qui stocke des mots et des comptes">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-25/src/main.rs:here}}
```

</Listing>

Ce code affichera `{"world": 2, "hello": 1, "wonderful": 1}`. Vous pourriez voir les mêmes paires clé-valeur imprimées dans un ordre différent : Rappelez-vous de [“Accéder aux valeurs dans une table de hachage”][access] que l'itération sur une table de hachage se fait dans un ordre arbitraire.

La méthode `split_whitespace` renvoie un itérateur sur des sous-tranches, séparées par des espaces, de la valeur dans `text`. La méthode `or_insert` renvoie une référence mutable (`&mut V`) à la valeur pour la clé spécifiée. Ici, nous stockons cette référence mutable dans la variable `count`, donc pour pouvoir assigner à cette valeur, nous devons d'abord dereferencer `count` en utilisant l'astérisque (`*`). La référence mutable sort de la portée à la fin de la boucle `for`, donc tous ces changements sont sûrs et autorisés par les règles de prêt.

### Fonctions de hachage

Par défaut, `HashMap` utilise une fonction de hachage appelée _SipHash_ qui peut fournir une résistance aux attaques par déni de service (DoS) impliquant des tables de hachage[^siphash]. Ce n'est pas l'algorithme de hachage le plus rapide disponible, mais le compromis pour une meilleure sécurité qui accompagne cette perte de performance en vaut la peine. Si vous profilez votre code et constatez que la fonction de hachage par défaut est trop lente pour vos besoins, vous pouvez passer à une autre fonction en spécifiant un hachoir différent. Un _hasher_ est un type qui implémente le trait `BuildHasher`. Nous parlerons des traits et de la manière de les implémenter dans [le chapitre 10][traits]. Vous n'êtes pas obligé de créer votre propre hachoir à partir de zéro ; [crates.io](https://crates.io/) propose des bibliothèques partagées par d'autres utilisateurs de Rust qui fournissent des hachoirs implémentant de nombreux algorithmes de hachage courants.

[^siphash]: [https://en.wikipedia.org/wiki/SipHash](https://en.wikipedia.org/wiki/SipHash)

## Résumé

Les vecteurs, les chaînes de caractères et les tables de hachage fourniront une grande quantité de fonctionnalités nécessaires dans les programmes lorsque vous devez stocker, accéder et modifier des données. Voici quelques exercices pour lesquels vous devriez maintenant être équipé pour résoudre :

1. Étant donné une liste d'entiers, utilisez un vecteur et renvoyez la médiane (lorsqu'elle est triée, la valeur à la position médiane) et le mode (la valeur qui se produit le plus souvent ; une table de hachage sera utile ici) de la liste.
2. Convertissez des chaînes en Pig Latin. La première consonne de chaque mot est déplacée à la fin du mot et _ay_ est ajoutée, donc _first_ devient _irst-fay_. Les mots qui commencent par une voyelle ont _hay_ ajouté à la fin à la place (_apple_ devient _apple-hay_). Gardez à l'esprit les détails concernant l'encodage UTF-8 !
3. En utilisant une table de hachage et des vecteurs, créez une interface texte pour permettre à un utilisateur d'ajouter des noms d'employés à un département d'une entreprise ; par exemple, « Ajouter Sally à l'ingénierie » ou « Ajouter Amir aux ventes ». Ensuite, laissez l'utilisateur récupérer une liste de toutes les personnes dans un département ou toutes les personnes de l'entreprise par département, triée par ordre alphabétique.

La documentation de l'API de la bibliothèque standard décrit les méthodes que les vecteurs, les chaînes et les tables de hachage ont, qui seront utiles pour ces exercices !

Nous entrons dans des programmes plus complexes où les opérations peuvent échouer, il est donc temps de discuter de la gestion des erreurs. Nous allons aborder cela maintenant !

[validating-references-with-lifetimes]: ch10-03-lifetime-syntax.html#validating-references-with-lifetimes
[access]: #accessing-values-in-a-hash-map
[traits]: ch10-02-traits.html