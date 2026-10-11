## Améliorer notre projet d’E/S

Grâce à ces nouvelles connaissances sur les itérateurs, nous pouvons améliorer le projet d’E/S du chapitre 12 en les utilisant pour rendre certaines parties du code plus claires et plus concises. Voyons comment les itérateurs peuvent améliorer notre implémentation des fonctions `Config::build` et `search`.

### Supprimer un `clone` à l’aide d’un itérateur

Dans l’exemple 12-6, nous avons ajouté du code qui prenait une tranche de valeurs `String` et créait une instance de la structure `Config` en indexant la tranche et en clonant les valeurs, ce qui permettait à la structure `Config` de posséder ces valeurs. Dans l’exemple 13-17, nous avons reproduit l’implémentation de la fonction `Config::build` telle qu’elle figurait dans l’exemple 12-23.

<Listing number="13-17" file-name="src/main.rs" caption="Reproduction de la fonction `Config::build` de l’exemple 12-23">

```rust,ignore
{{#rustdoc_include ../listings/ch13-functional-features/listing-12-23-reproduced/src/main.rs:ch13}}
```

</Listing>

À l’époque, nous vous avions dit de ne pas vous inquiéter des appels inefficaces à `clone`, car nous les supprimerions plus tard. Eh bien, ce moment est arrivé !

Nous avions besoin de `clone` ici parce que le paramètre `args` contient une tranche dont les éléments sont des valeurs `String`, mais la fonction `build` ne possède pas `args`. Pour renvoyer la propriété d’une instance de `Config`, nous devions cloner les valeurs des champs `query` et `file_path` de `Config` afin que l’instance de `Config` puisse posséder ses valeurs.

Grâce à nos nouvelles connaissances sur les itérateurs, nous pouvons modifier la fonction `build` pour qu’elle prenne possession d’un itérateur en argument, au lieu d’emprunter une tranche. Nous utiliserons les fonctionnalités de l’itérateur plutôt que le code qui vérifie la longueur de la tranche et accède à des positions précises par index. Cela clarifiera le rôle de la fonction `Config::build`, puisque l’itérateur accédera aux valeurs.

Une fois que `Config::build` prendra possession de l’itérateur et n’utilisera plus d’opérations d’indexation qui empruntent les valeurs, nous pourrons déplacer les valeurs `String` de l’itérateur vers `Config` au lieu d’appeler `clone` et d’effectuer une nouvelle allocation.

#### Utiliser directement l’itérateur renvoyé

Ouvrez le fichier _src/main.rs_ de votre projet d’E/S, qui devrait ressembler à ceci :

<span class="filename">Nom du fichier : src/main.rs</span>

```rust,ignore
{{#rustdoc_include ../listings/ch13-functional-features/listing-12-24-reproduced/src/main.rs:ch13}}
```

Nous allons d’abord remplacer le début de la fonction `main` de l’exemple 12-24 par le code de l’exemple 13-18, qui utilise cette fois un itérateur. Ce code ne compilera pas tant que nous n’aurons pas également mis à jour `Config::build`.

<Listing number="13-18" file-name="src/main.rs" caption="Passage de la valeur renvoyée par `env::args` à `Config::build`">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-18/src/main.rs:here}}
```

</Listing>

La fonction `env::args` renvoie un itérateur ! Au lieu de collecter les valeurs de l’itérateur dans un vecteur, puis de passer une tranche à `Config::build`, nous transmettons maintenant directement à `Config::build` la propriété de l’itérateur renvoyé par `env::args`.

Ensuite, nous devons mettre à jour la définition de `Config::build`. Modifions sa signature pour qu’elle ressemble à celle de l’exemple 13-19. Le code ne compilera toujours pas, car nous devons également mettre à jour le corps de la fonction.

<Listing number="13-19" file-name="src/main.rs" caption="Mise à jour de la signature de `Config::build` pour qu’elle attende un itérateur">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-19/src/main.rs:here}}
```

</Listing>

La documentation de la bibliothèque standard pour la fonction `env::args` indique que le type de l’itérateur qu’elle renvoie est `std::env::Args`, et que ce type implémente le trait `Iterator` et renvoie des valeurs `String`.

Nous avons mis à jour la signature de la fonction `Config::build` afin que le paramètre `args` ait un type générique assorti de la borne de trait `impl Iterator<Item = String>` au lieu de `&[String]`. Cette utilisation de la syntaxe `impl Trait`, présentée dans la section [« Utiliser les traits comme paramètres »][impl-trait]<!-- ignore --> du chapitre 10, signifie que `args` peut être de n’importe quel type qui implémente le trait `Iterator` et renvoie des éléments `String`.

Comme nous prenons possession de `args` et que nous allons le modifier en itérant dessus, nous pouvons ajouter le mot-clé `mut` à la déclaration du paramètre `args` pour le rendre mutable.

<!-- Old headings. Do not remove or links may break. -->

<a id="using-iterator-trait-methods-instead-of-indexing"></a>

#### Utiliser les méthodes du trait `Iterator`

Ensuite, nous allons corriger le corps de `Config::build`. Puisque `args` implémente le trait `Iterator`, nous savons que nous pouvons appeler sa méthode `next` ! L’exemple 13-20 met à jour le code de l’exemple 12-23 pour utiliser la méthode `next`.

<Listing number="13-20" file-name="src/main.rs" caption="Modification du corps de `Config::build` pour utiliser les méthodes des itérateurs">

```rust,ignore,noplayground
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-20/src/main.rs:here}}
```

</Listing>

Rappelez-vous que la première valeur renvoyée par `env::args` est le nom du programme. Nous voulons l’ignorer et passer à la valeur suivante : nous appelons donc d’abord `next` sans rien faire de la valeur renvoyée. Puis nous appelons `next` pour obtenir la valeur à placer dans le champ `query` de `Config`. Si `next` renvoie `Some`, nous utilisons un `match` pour extraire la valeur. S’il renvoie `None`, cela signifie que le nombre d’arguments fournis est insuffisant, et nous renvoyons immédiatement une valeur `Err`. Nous procédons de la même façon pour la valeur de `file_path`.

<!-- Old headings. Do not remove or links may break. -->

<a id="making-code-clearer-with-iterator-adapters"></a>

### Clarifier le code avec les adaptateurs d’itérateur

Nous pouvons également tirer parti des itérateurs dans la fonction `search` de notre projet d’E/S, reproduite ici dans l’exemple 13-21 telle qu’elle figurait dans l’exemple 12-19.

<Listing number="13-21" file-name="src/lib.rs" caption="L’implémentation de la fonction `search` de l’exemple 12-19">

```rust,ignore
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-19/src/lib.rs:ch13}}
```

</Listing>

Nous pouvons écrire ce code de manière plus concise en utilisant les méthodes adaptatrices d’itérateur. Cela nous permet également d’éviter d’avoir un vecteur intermédiaire mutable `results`. Le style de programmation fonctionnelle privilégie la réduction de l’état mutable afin de rendre le code plus clair. La suppression de cet état mutable pourrait permettre une amélioration ultérieure consistant à effectuer la recherche en parallèle, car nous n’aurions pas à gérer les accès concurrents au vecteur `results`. L’exemple 13-22 présente cette modification.

<Listing number="13-22" file-name="src/lib.rs" caption="Utilisation de méthodes adaptatrices d’itérateur dans l’implémentation de la fonction `search`">

```rust,ignore
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-22/src/lib.rs:here}}
```

</Listing>

Rappelez-vous que la fonction `search` a pour but de renvoyer toutes les lignes de `contents` qui contiennent `query`. Comme dans l’exemple de `filter` de l’exemple 13-16, ce code utilise l’adaptateur `filter` pour ne conserver que les lignes pour lesquelles `line.contains(query)` renvoie `true`. Nous collectons ensuite les lignes correspondantes dans un autre vecteur à l’aide de `collect`. C’est beaucoup plus simple ! N’hésitez pas à effectuer la même modification dans la fonction `search_case_insensitive` pour y utiliser aussi les méthodes des itérateurs.

Pour aller plus loin, renvoyez un itérateur depuis la fonction `search` en supprimant l’appel à `collect` et en modifiant le type de retour en `impl Iterator<Item = &'a str>`, afin que la fonction devienne un adaptateur d’itérateur. Notez que vous devrez également mettre à jour les tests ! Faites une recherche dans un gros fichier avec votre outil `minigrep` avant et après cette modification afin d’observer la différence de comportement. Avant la modification, le programme n’affiche aucun résultat tant qu’il ne les a pas tous collectés. Après, les résultats sont affichés au fur et à mesure que chaque ligne correspondante est trouvée, car la boucle `for` de la fonction `run` peut tirer parti de l’évaluation paresseuse de l’itérateur.

<!-- Old headings. Do not remove or links may break. -->

<a id="choosing-between-loops-or-iterators"></a>

### Choisir entre les boucles et les itérateurs

La question qui se pose ensuite est de savoir quel style choisir dans votre propre code et pourquoi : l’implémentation d’origine de l’exemple 13-21 ou la version utilisant des itérateurs de l’exemple 13-22 (en supposant que nous collectons tous les résultats avant de les renvoyer plutôt que de renvoyer l’itérateur). La plupart des programmeurs Rust préfèrent le style des itérateurs. Il est un peu plus difficile à maîtriser au début, mais une fois que vous connaissez les différents adaptateurs d’itérateur et leur fonctionnement, les itérateurs peuvent être plus faciles à comprendre. Au lieu de manipuler les différentes parties d’une boucle et de créer de nouveaux vecteurs, le code se concentre sur l’objectif général de la boucle. Cela masque une partie du code courant, ce qui permet de mieux repérer les concepts propres à ce code, comme la condition de filtrage que chaque élément de l’itérateur doit satisfaire.

Mais les deux implémentations sont-elles vraiment équivalentes ? On pourrait intuitivement supposer que la boucle de plus bas niveau serait plus rapide. Parlons des performances.

[impl-trait]: ch10-02-traits.html#traits-as-parameters