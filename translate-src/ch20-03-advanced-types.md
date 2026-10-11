## Types avancés

Le système de types de Rust possède certaines fonctionnalités que nous avons mentionnées jusqu’à présent sans encore les examiner. Nous commencerons par parler des newtypes en général et examinerons leur utilité en tant que types. Nous passerons ensuite aux alias de types, une fonctionnalité similaire aux newtypes, mais dont la sémantique est légèrement différente. Nous parlerons également du type `!` et des types de taille dynamique.

<!-- Anciennes rubriques. Ne pas supprimer, sinon les liens risquent de ne plus fonctionner. -->

<a id="using-the-newtype-pattern-for-type-safety-and-abstraction"></a>

### Sécurité des types et abstraction avec le motif newtype

Cette section suppose que vous avez lu la section précédente [« Implémenter des traits externes avec le motif newtype »][newtype]<!-- ignore -->. Le motif newtype est également utile pour des tâches autres que celles que nous avons abordées jusqu’ici, notamment pour garantir statiquement que des valeurs ne puissent jamais être confondues et pour indiquer les unités d’une valeur. Vous avez vu un exemple d’utilisation des newtypes pour indiquer des unités dans l’exemple 20-16 : rappelez-vous que les structures `Millimeters` et `Meters` enveloppaient des valeurs `u32` dans un newtype. Si nous écrivions une fonction dont un paramètre est de type `Millimeters`, nous ne pourrions pas compiler un programme qui essaierait par erreur d’appeler cette fonction avec une valeur de type `Meters` ou un simple `u32`.

Nous pouvons également utiliser le motif newtype pour abstraire certains détails d’implémentation d’un type : le nouveau type peut exposer une API publique différente de celle du type interne privé.

Les newtypes peuvent aussi masquer l’implémentation interne. Par exemple, nous pourrions fournir un type `People` qui enveloppe un `HashMap<i32, String>` stockant l’identifiant d’une personne associé à son nom. Le code qui utilise `People` interagirait uniquement avec l’API publique que nous fournissons, par exemple une méthode permettant d’ajouter une chaîne de nom à la collection `People` ; ce code n’aurait pas besoin de savoir que nous associons en interne un identifiant `i32` aux noms. Le motif newtype est un moyen léger d’obtenir l’encapsulation et de masquer les détails d’implémentation, comme nous l’avons vu dans la section [« L’encapsulation qui masque les détails d’implémentation »][encapsulation-that-hides-implementation-details]<!-- ignore --> du chapitre 18.

<!-- Anciennes rubriques. Ne pas supprimer, sinon les liens risquent de ne plus fonctionner. -->

<a id="creating-type-synonyms-with-type-aliases"></a>

### Synonymes de types et alias de types

Rust permet de déclarer un _alias de type_ pour donner un autre nom à un type existant. Pour cela, nous utilisons le mot-clé `type`. Par exemple, nous pouvons créer l’alias `Kilometers` pour `i32` comme ceci :

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-04-kilometers-alias/src/main.rs:here}}
```

L’alias `Kilometers` est maintenant un _synonyme_ de `i32` ; contrairement aux types `Millimeters` et `Meters` que nous avons créés dans l’exemple 20-16, `Kilometers` n’est pas un type distinct. Les valeurs de type `Kilometers` seront traitées de la même manière que les valeurs de type `i32` :

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-04-kilometers-alias/src/main.rs:there}}
```

Comme `Kilometers` et `i32` sont le même type, nous pouvons additionner des valeurs de ces deux types et transmettre des valeurs `Kilometers` à des fonctions qui prennent des paramètres `i32`. Cependant, avec cette méthode, nous ne bénéficions pas de la vérification des types offerte par le motif newtype abordé précédemment. Autrement dit, si nous confondons des valeurs `Kilometers` et `i32`, le compilateur ne nous signalera pas d’erreur.

Les alias de types servent principalement à réduire les répétitions. Nous pourrions, par exemple, avoir un type long comme celui-ci :

```rust,ignore
Box<dyn Fn() + Send + 'static>
```

Écrire ce type long dans les signatures de fonctions et dans les annotations de types à travers tout le code peut être fastidieux et source d’erreurs. Imaginez un projet rempli de code comme celui de l’exemple 20-25.

<Listing number="20-25" caption="Utilisation d’un type long à plusieurs endroits">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-25/src/main.rs:here}}
```

</Listing>

Un alias de type rend ce code plus facile à gérer en réduisant les répétitions. Dans l’exemple 20-26, nous avons introduit un alias nommé `Thunk` pour le type verbeux et pouvons remplacer toutes ses occurrences par l’alias plus court `Thunk`.

<Listing number="20-26" caption="Introduction d’un alias de type, `Thunk`, pour réduire les répétitions">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-26/src/main.rs:here}}
```

</Listing>

Ce code est beaucoup plus facile à lire et à écrire ! Choisir un nom évocateur pour un alias de type peut aussi aider à communiquer votre intention (_thunk_ désigne du code qui sera évalué ultérieurement ; c’est donc un nom approprié pour une fermeture qui est stockée).

Les alias de types sont également couramment utilisés avec le type `Result<T, E>` afin de réduire les répétitions. Prenons le module `std::io` de la bibliothèque standard. Les opérations d’E/S renvoient souvent un `Result<T, E>` pour gérer les situations où elles échouent. Cette bibliothèque possède une structure `std::io::Error` qui représente toutes les erreurs d’E/S possibles. De nombreuses fonctions de `std::io` renvoient un `Result<T, E>` dont le type `E` est `std::io::Error`, comme les fonctions suivantes du trait `Write` :

```rust,noplayground
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-05-write-trait/src/lib.rs}}
```

Le type `Result<..., Error>` est répété un grand nombre de fois. C’est pourquoi `std::io` déclare l’alias de type suivant :

```rust,noplayground
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-06-result-alias/src/lib.rs:here}}
```

Comme cette déclaration se trouve dans le module `std::io`, nous pouvons utiliser l’alias pleinement qualifié `std::io::Result<T>`, c’est-à-dire un `Result<T, E>` dont le type `E` est `std::io::Error`. Les signatures des fonctions du trait `Write` se présentent alors ainsi :

```rust,noplayground
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-06-result-alias/src/lib.rs:there}}
```

L’alias de type est utile à deux égards : il rend le code plus facile à écrire _et_ fournit une interface cohérente dans tout `std::io`. Comme il s’agit d’un alias, ce n’est qu’un autre `Result<T, E>`, ce qui signifie que nous pouvons utiliser avec lui toutes les méthodes applicables à `Result<T, E>`, ainsi que des syntaxes spéciales comme l’opérateur `?`.

### Le type jamais, qui ne renvoie jamais

Rust possède un type spécial nommé `!`, connu sous le nom de _type vide_ dans le jargon de la théorie des types, car il ne comporte aucune valeur. Nous préférons l’appeler _type jamais_, car il tient lieu de type de retour lorsqu’une fonction ne renvoie jamais. En voici un exemple :

```rust,noplayground
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-07-never-type/src/lib.rs:here}}
```

Ce code se lit ainsi : « la fonction `bar` ne renvoie jamais ». Les fonctions qui ne renvoient jamais sont appelées _fonctions divergentes_. Nous ne pouvons pas créer de valeurs de type `!`, donc `bar` ne peut absolument pas renvoyer de valeur.

Mais à quoi sert un type dont on ne peut jamais créer de valeurs ? Rappelez-vous le code de l’exemple 2-5, tiré du jeu de devinette ; nous en avons reproduit une partie dans l’exemple 20-27.

<Listing number="20-27" caption="Un `match` dont une branche se termine par `continue`">

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-05/src/main.rs:ch19}}
```

</Listing>

À l’époque, nous avons omis certains détails de ce code. Dans la section [« La construction de contrôle de flux `match` »][the-match-control-flow-construct]<!-- ignore --> du chapitre 6, nous avons expliqué que toutes les branches d’un `match` doivent renvoyer le même type. Par exemple, le code suivant ne fonctionne pas :

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-08-match-arms-different-types/src/main.rs:here}}
```

Dans ce code, `guess` devrait être à la fois un entier _et_ une chaîne de caractères, et Rust exige que `guess` n’ait qu’un seul type. Alors, que renvoie `continue` ? Comment avons-nous pu renvoyer un `u32` dans une branche et avoir une autre branche qui se termine par `continue` dans l’exemple 20-27 ?

Comme vous l’avez peut-être deviné, `continue` a une valeur de type `!`. Autrement dit, lorsque Rust détermine le type de `guess`, il examine les deux branches du `match` : la première a une valeur de type `u32` et la seconde, une valeur de type `!`. Comme `!` ne peut jamais avoir de valeur, Rust détermine que le type de `guess` est `u32`.

La manière formelle de décrire ce comportement consiste à dire que les expressions de type `!` peuvent être converties en n’importe quel autre type. Nous pouvons terminer cette branche du `match` par `continue` parce que `continue` ne renvoie pas de valeur ; il ramène plutôt le contrôle au début de la boucle. Ainsi, dans le cas `Err`, nous n’attribuons jamais de valeur à `guess`.

Le type jamais est également utile avec la macro `panic!`. Rappelez-vous la fonction `unwrap`, que nous appelons sur des valeurs `Option<T>` pour obtenir une valeur ou déclencher une panique, et qui est définie ainsi :

```rust,ignore
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-09-unwrap-definition/src/lib.rs:here}}
```

Dans ce code, il se passe la même chose que dans le `match` de l’exemple 20-27 : Rust voit que `val` est de type `T` et que `panic!` est de type `!`, donc le résultat de l’expression `match` complète est de type `T`. Ce code fonctionne parce que `panic!` ne produit pas de valeur ; il met fin au programme. Dans le cas `None`, `unwrap` ne renvoie aucune valeur, ce code est donc valide.

Une dernière expression de type `!` est une boucle :

```rust,ignore
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-10-loop-returns-never/src/main.rs:here}}
```

Ici, la boucle ne se termine jamais, donc l’expression est de type `!`. Cela ne serait toutefois pas vrai si nous ajoutions un `break`, car la boucle se terminerait en atteignant ce `break`.

### Types de taille dynamique et trait `Sized`

Rust doit connaître certains détails de ses types, comme la quantité d’espace à allouer pour une valeur d’un type donné. Cela rend un aspect de son système de types un peu déroutant au premier abord : le concept de _types de taille dynamique_. Parfois appelés _DST_ ou _types non dimensionnés_, ces types nous permettent d’écrire du code utilisant des valeurs dont nous ne pouvons connaître la taille qu’à l’exécution.

Examinons en détail un type de taille dynamique appelé `str`, que nous avons utilisé tout au long de ce livre. Eh oui, `str` seul, et non `&str`, est un DST. Dans de nombreux cas, par exemple lorsqu’on stocke du texte saisi par une personne, nous ne pouvons pas connaître la longueur de la chaîne avant l’exécution. Cela signifie que nous ne pouvons ni créer une variable de type `str`, ni prendre un argument de type `str`. Le code suivant ne fonctionne donc pas :

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-11-cant-create-str/src/main.rs:here}}
```

Rust doit connaître la quantité de mémoire à allouer pour toute valeur d’un type donné, et toutes les valeurs d’un même type doivent occuper la même quantité de mémoire. Si Rust nous autorisait à écrire ce code, ces deux valeurs `str` devraient occuper le même espace. Or, elles ont des longueurs différentes : `s1` nécessite 12 octets de stockage et `s2` en nécessite 15. C’est pourquoi il est impossible de créer une variable contenant un type de taille dynamique.

Que faire alors ? Dans ce cas, vous connaissez déjà la réponse : nous donnons à `s1` et `s2` le type tranche de chaîne (`&str`) plutôt que `str`. Rappelez-vous, d’après la section [« Tranches de chaîne »][string-slices]<!-- ignore --> du chapitre 4, que la structure de données d’une tranche ne stocke que la position de départ et la longueur de la tranche. Ainsi, même si `&T` est une valeur unique qui stocke l’adresse mémoire où se trouve `T`, une tranche de chaîne est constituée de _deux_ valeurs : l’adresse de `str` et sa longueur. Nous pouvons donc connaître la taille d’une valeur de tranche de chaîne à la compilation : elle correspond à deux fois la taille d’un `usize`. Autrement dit, nous connaissons toujours la taille d’une tranche de chaîne, quelle que soit la longueur de la chaîne à laquelle elle fait référence. En général, c’est ainsi que les types de taille dynamique sont utilisés dans Rust : ils comportent une information supplémentaire qui stocke la taille des données dynamiques. La règle d’or des types de taille dynamique est qu’il faut toujours placer leurs valeurs derrière une sorte de pointeur.

Nous pouvons combiner `str` avec toutes sortes de pointeurs : par exemple, `Box<str>` ou `Rc<str>`. En fait, vous avez déjà vu cela avec un autre type de taille dynamique : les traits. Chaque trait est un type de taille dynamique auquel nous pouvons faire référence en utilisant le nom du trait. Dans la section [« Utiliser des objets de trait pour abstraire un comportement partagé »][using-trait-objects-to-abstract-over-shared-behavior]<!-- ignore --> du chapitre 18, nous avons expliqué que, pour utiliser des traits comme objets de trait, il faut les placer derrière un pointeur, par exemple `&dyn Trait` ou `Box<dyn Trait>` (`Rc<dyn Trait>` fonctionnerait également).

Pour travailler avec les DST, Rust fournit le trait `Sized`, qui permet de déterminer si la taille d’un type est connue à la compilation. Ce trait est automatiquement implémenté pour tout type dont la taille est connue à la compilation. De plus, Rust ajoute implicitement une contrainte `Sized` à chaque fonction générique. Autrement dit, une définition de fonction générique comme celle-ci :

```rust,ignore
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-12-generic-fn-definition/src/lib.rs}}
```

est en réalité traitée comme si nous avions écrit ceci :

```rust,ignore
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-13-generic-implicit-sized-bound/src/lib.rs}}
```

Par défaut, les fonctions génériques ne fonctionnent qu’avec des types dont la taille est connue à la compilation. Vous pouvez toutefois assouplir cette restriction à l’aide de la syntaxe spéciale suivante :

```rust,ignore
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-14-generic-maybe-sized/src/lib.rs}}
```

Une contrainte de trait `?Sized` signifie que « `T` peut être `Sized` ou ne pas l’être », et cette notation remplace la règle par défaut selon laquelle les types génériques doivent avoir une taille connue à la compilation. La syntaxe `?Trait` n’est disponible avec cette signification que pour `Sized`, et non pour les autres traits.

Notez également que nous avons remplacé le type du paramètre `t`, qui était `T`, par `&T`. Comme le type n’est pas nécessairement `Sized`, nous devons l’utiliser derrière une sorte de pointeur. Ici, nous avons choisi une référence.

Nous allons maintenant parler des fonctions et des fermetures !

[encapsulation-that-hides-implementation-details]: ch18-01-what-is-oo.html#encapsulation-that-hides-implementation-details
[string-slices]: ch04-03-slices.html#string-slices
[the-match-control-flow-construct]: ch06-02-match.html#the-match-control-flow-construct
[using-trait-objects-to-abstract-over-shared-behavior]: ch18-02-trait-objects.html#using-trait-objects-to-abstract-over-shared-behavior
[newtype]: ch20-02-advanced-traits.html#implementing-external-traits-with-the-newtype-pattern