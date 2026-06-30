## Améliorer notre projet I/O

Avec cette nouvelle connaissance sur les itérateurs, nous pouvons améliorer le projet I/O du Chapitre 12 en utilisant des itérateurs pour rendre certaines parties du code plus claires et plus concises. Voyons comment les itérateurs peuvent améliorer notre implémentation de la fonction `Config::build` et de la fonction `search`.

### Suppression d'un `clone` en utilisant un itérateur

Dans la Liste 12-6, nous avons ajouté du code qui prenait un extrait de valeurs de type `String` et créait une instance de la structure `Config` en indexant dans l'extrait et en clonant les valeurs, permettant ainsi à la structure `Config` de posséder ces valeurs. Dans la Liste 13-17, nous avons reproduit l'implémentation de la fonction `Config::build` telle qu'elle était dans la Liste 12-23.

<Liste numéro="13-17" nom-fichier="src/main.rs" légende="Reproduction de la fonction `Config::build` de la Liste 12-23">

```rust,ignore
{{#rustdoc_include ../listings/ch13-functional-features/listing-12-23-reproduced/src/main.rs:ch13}}
```

</Liste>

À l'époque, nous avons dit de ne pas nous soucier des appels de `clone` inefficaces, car nous les supprimerions à l'avenir. Eh bien, ce moment est maintenant !

Nous avions besoin de `clone` ici parce que nous avons un extrait avec des éléments `String` dans le paramètre `args`, mais la fonction `build` ne possède pas `args`. Pour renvoyer la propriété d'une instance de `Config`, nous devions cloner les valeurs des champs `query` et `file_path` de `Config` afin que l'instance de `Config` puisse posséder ses valeurs.

Avec notre nouvelle connaissance des itérateurs, nous pouvons modifier la fonction `build` pour prendre la propriété d'un itérateur comme argument au lieu d'emprunter un extrait. Nous utiliserons la fonctionnalité de l'itérateur au lieu du code qui vérifie la longueur de l'extrait et indexe à des emplacements spécifiques. Cela clarifiera ce que fait la fonction `Config::build` car l'itérateur accède aux valeurs.

Une fois que `Config::build` prendra possession de l'itérateur et cessera d'utiliser des opérations d'indexation qui empruntent, nous pourrons déplacer les valeurs `String` de l'itérateur vers `Config` plutôt que d'appeler `clone` et de créer une nouvelle allocation.

#### Utilisation de l'itérateur retourné directement

Ouvrez le fichier _src/main.rs_ de votre projet I/O, qui devrait ressembler à ceci :

<span class="filename">Nom de fichier : src/main.rs</span>

```rust,ignore
{{#rustdoc_include ../listings/ch13-functional-features/listing-12-24-reproduced/src/main.rs:ch13}}
```

Nous allons d'abord changer le début de la fonction `main` que nous avions dans la Liste 12-24 pour le code dans la Liste 13-18, qui utilise cette fois un itérateur. Cela ne compilera pas tant que nous n'aurons pas également mis à jour `Config::build`.

<Liste numéro="13-18" nom-fichier="src/main.rs" légende="Passage de la valeur de retour de `env::args` à `Config::build`">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-18/src/main.rs:here}}
```

</Liste>

La fonction `env::args` retourne un itérateur ! Plutôt que de collecter les valeurs de l'itérateur dans un vecteur puis de passer un extrait à `Config::build`, nous passons maintenant la propriété de l'itérateur retourné par `env::args` directement à `Config::build`.

Ensuite, nous devons mettre à jour la définition de `Config::build`. Modifions la signature de `Config::build` pour qu'elle ressemble à la Liste 13-19. Cela ne compilera toujours pas, car nous devons mettre à jour le corps de la fonction.

<Liste numéro="13-19" nom-fichier="src/main.rs" légende="Mise à jour de la signature de `Config::build` pour attendre un itérateur">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-19/src/main.rs:here}}
```

</Liste>

La documentation de la bibliothèque standard concernant la fonction `env::args` montre que le type de l'itérateur qu'elle retourne est `std::env::Args`, et ce type implémente le trait `Iterator` et retourne des valeurs de type `String`.

Nous avons mis à jour la signature de la fonction `Config::build` pour que le paramètre `args` ait un type générique avec les limites du trait `impl Iterator<Item = String>` au lieu de `&[String]`. Cet usage de la syntaxe `impl Trait` que nous avons abordée dans la section [« Utilisation des traits en tant que paramètres »][impl-trait]<!-- ignore --> du Chapitre 10 signifie que `args` peut être de n'importe quel type qui implémente le trait `Iterator` et retourne des éléments de type `String`.

Étant donné que nous prenons possession de `args` et que nous allons muter `args` en l'itérant, nous pouvons ajouter le mot clé `mut` dans la spécification du paramètre `args` pour le rendre mutable.

<!-- Ancien titre. Ne pas supprimer ou les liens peuvent se briser. -->

<a id="using-iterator-trait-methods-instead-of-indexing"></a>

#### Utilisation des méthodes du trait `Iterator`

Ensuite, nous allons corriger le corps de `Config::build`. Étant donné que `args` implémente le trait `Iterator`, nous savons que nous pouvons appeler la méthode `next` dessus ! La Liste 13-20 met à jour le code de la Liste 12-23 pour utiliser la méthode `next`.

<Liste numéro="13-20" nom-fichier="src/main.rs" légende="Changement du corps de `Config::build` pour utiliser des méthodes d'itérateur">

```rust,ignore,noplayground
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-20/src/main.rs:here}}
```

</Liste>

Rappelez-vous que la première valeur dans la valeur de retour de `env::args` est le nom du programme. Nous voulons l'ignorer et accéder à la valeur suivante, donc nous appelons d'abord `next` et ne faisons rien avec la valeur de retour. Ensuite, nous appelons `next` pour obtenir la valeur que nous voulons mettre dans le champ `query` de `Config`. Si `next` retourne `Some`, nous utilisons un `match` pour extraire la valeur. Si cela retourne `None`, cela signifie que pas assez d'arguments ont été fournis, et nous retournons rapidement une valeur `Err`. Nous faisons de même pour la valeur `file_path`.

<!-- Ancien titre. Ne pas supprimer ou les liens peuvent se briser. -->

<a id="making-code-clearer-with-iterator-adapters"></a>

### Clarification du code avec les adaptateurs d'itérateurs

Nous pouvons également tirer parti des itérateurs dans la fonction `search` de notre projet I/O, qui est reproduite ici dans la Liste 13-21 comme elle était dans la Liste 12-19.

<Liste numéro="13-21" nom-fichier="src/lib.rs" légende="L'implémentation de la fonction `search` de la Liste 12-19">

```rust,ignore
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-19/src/lib.rs:ch13}}
```

</Liste>

Nous pouvons écrire ce code de manière plus concise en utilisant des méthodes d'adaptateurs d'itérateurs. Cela nous permet également d'éviter d'avoir un vecteur `results` mutable intermédiaire. Le style de programmation fonctionnelle préfère minimiser la quantité d'état mutable pour rendre le code plus clair. La suppression de l'état mutable pourrait permettre une amélioration future pour effectuer des recherches en parallèle, car nous n'aurions pas à gérer l'accès concurrent au vecteur `results`. La Liste 13-22 montre ce changement.

<Liste numéro="13-22" nom-fichier="src/lib.rs" légende="Utilisation des méthodes d'adaptateurs d'itérateurs dans l'implémentation de la fonction `search`">

```rust,ignore
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-22/src/lib.rs:here}}
```

</Liste>

Rappelez-vous que le but de la fonction `search` est de retourner toutes les lignes dans `contents` qui contiennent la `query`. Semblable à l'exemple de `filter` dans la Liste 13-16, ce code utilise l'adaptateur `filter` pour ne garder que les lignes pour lesquelles `line.contains(query)` retourne `true`. Nous collectons ensuite les lignes correspondantes dans un autre vecteur avec `collect`. Beaucoup plus simple ! N'hésitez pas à apporter le même changement pour utiliser des méthodes d'itérateur dans la fonction `search_case_insensitive`.

Pour une amélioration supplémentaire, retournez un itérateur depuis la fonction `search` en supprimant l'appel à `collect` et en modifiant le type de retour en `impl Iterator<Item = &'a str>` afin que la fonction devienne un adaptateur d'itérateur. Notez que vous devrez également mettre à jour les tests ! Recherchez dans un grand fichier en utilisant votre outil `minigrep` avant et après avoir apporté ce changement pour observer la différence de comportement. Avant ce changement, le programme ne imprimait aucun résultat tant qu'il n'avait pas collecté tous les résultats, mais après le changement, les résultats seront imprimés à mesure que chaque ligne correspondante est trouvée, car la boucle `for` dans la fonction `run` pourra profiter de la paresse de l'itérateur.

<!-- Ancien titre. Ne pas supprimer ou les liens peuvent se briser. -->

<a id="choosing-between-loops-or-iterators"></a>

### Choisir entre boucles ou itérateurs

La question suivante est de savoir quel style vous devriez choisir dans votre propre code et pourquoi : l'implémentation originale dans la Liste 13-21 ou la version utilisant des itérateurs dans la Liste 13-22 (supposant que nous collectons tous les résultats avant de les renvoyer plutôt que de retourner l'itérateur). La plupart des programmeurs Rust préfèrent utiliser le style des itérateurs. C'est un peu plus difficile à maîtriser au début, mais une fois que vous vous familiarisez avec les différents adaptateurs d'itérateurs et ce qu'ils font, les itérateurs peuvent être plus faciles à comprendre. Au lieu de jouer avec les différents aspects de la boucle et de construire de nouveaux vecteurs, le code se concentre sur l'objectif de haut niveau de la boucle. Cela abstrait une partie du code courant pour qu'il soit plus facile de voir les concepts uniques à ce code, tels que la condition de filtrage que chaque élément de l'itérateur doit passer.

Mais les deux implémentations sont-elles réellement équivalentes ? L'hypothèse intuitive pourrait être que la boucle de bas niveau sera plus rapide. Parlons des performances. 

[impl-trait]: ch10-02-traits.html#traits-as-parameters