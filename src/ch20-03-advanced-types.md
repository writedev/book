## Types avancés

Le système de types de Rust possède certaines fonctionnalités que nous avons mentionnées jusqu'à présent mais dont nous n'avons pas encore discuté. Nous commencerons par aborder les nouveaux types en général en examinant pourquoi ils sont utiles en tant que types. Ensuite, nous passerons aux alias de types, une fonctionnalité similaire aux nouveaux types mais avec une sémantique légèrement différente. Nous discuterons également du type `!` et des types de taille dynamique.

### Sécurité des types et abstraction avec le patron Newtype

Cette section suppose que vous avez lu la section précédente [« Implémentation de traits externes avec le patron Newtype »][newtype]. Le patron newtype est également utile pour des tâches au-delà de celles que nous avons discutées jusqu'à présent, notamment pour imposer statiquement que les valeurs ne soient jamais confondues et pour indiquer les unités d'une valeur. Vous avez vu un exemple d'utilisation des nouveaux types pour indiquer des unités dans le Listing 20-16 : rappelez-vous que les structures `Millimeters` et `Meters` enveloppaient des valeurs `u32` dans un nouveau type. Si nous écrivions une fonction avec un paramètre de type `Millimeters`, nous ne pourrions pas compiler un programme qui essaierait par accident d'appeler cette fonction avec une valeur de type `Meters` ou un simple `u32`.

Nous pouvons également utiliser le patron newtype pour abstraire certains détails d'implémentation d'un type : le nouveau type peut exposer une API publique différente de l'API du type interne privé.

Les nouveaux types peuvent également masquer l'implémentation interne. Par exemple, nous pourrions fournir un type `People` pour encapsuler un `HashMap<i32, String>` qui stocke l'ID d'une personne associé à son nom. Le code utilisant `People` n'interagirait qu'avec l'API publique que nous fournissons, comme une méthode pour ajouter une chaîne de nom à la collection `People` ; ce code n'aurait pas besoin de savoir que nous assignons un ID `i32` aux noms en interne. Le patron newtype est une manière légère d'atteindre l'encapsulation pour masquer les détails d'implémentation, ce que nous avons discuté dans la section [« Encapsulation qui cache les détails d'implémentation »][encapsulation-that-hides-implementation-details] dans le Chapitre 18.

### Synonymes de types et alias de types

Rust permet de déclarer un _alias de type_ pour donner un autre nom à un type existant. Pour cela, nous utilisons le mot-clé `type`. Par exemple, nous pouvons créer l'alias `Kilometers` pour `i32` de cette manière :

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-04-kilometers-alias/src/main.rs:here}}
```

Maintenant, l'alias `Kilometers` est un _synonyme_ pour `i32` ; contrairement aux types `Millimeters` et `Meters` que nous avons créés dans le Listing 20-16, `Kilometers` n'est pas un type séparé, nouveau. Les valeurs qui ont le type `Kilometers` seront traitées de la même manière que les valeurs de type `i32` :

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-04-kilometers-alias/src/main.rs:there}}
```

Étant donné que `Kilometers` et `i32` sont le même type, nous pouvons ajouter des valeurs des deux types et passer des valeurs `Kilometers` à des fonctions qui prennent des paramètres `i32`. Cependant, en utilisant cette méthode, nous ne récupérons pas les avantages de vérification de type que nous obtenons avec le patron newtype discuté précédemment. En d'autres termes, si nous confondons des valeurs `Kilometers` et `i32` quelque part, le compilateur ne nous donnera pas d'erreur.

Le principal cas d'utilisation des synonymes de types est de réduire la répétition. Par exemple, nous pourrions avoir un type long comme celui-ci :

```rust,ignore
Box<dyn Fn() + Send + 'static>
```

Écrire ce long type dans les signatures de fonction et comme annotations de type dans tout le code peut être épuisant et sujet à erreur. Imaginez avoir un projet rempli de code comme cela dans le Listing 20-25.

<Listing number="20-25" caption="Utilisation d'un long type à plusieurs endroits">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-25/src/main.rs:here}}
```

</Listing>

Un alias de type rend ce code plus gérable en réduisant la répétition. Dans le Listing 20-26, nous avons introduit un alias nommé `Thunk` pour le type verbeux et nous pouvons remplacer toutes les occurrences du type par l'alias plus court `Thunk`.

<Listing number="20-26" caption="Introduction d'un alias de type, `Thunk`, pour réduire la répétition">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-26/src/main.rs:here}}
```

</Listing>

Ce code est beaucoup plus facile à lire et à écrire ! Choisir un nom significatif pour un alias de type peut également aider à communiquer votre intention, car _thunk_ est un mot pour du code devant être évalué plus tard, donc c'est un nom approprié pour une closure qui est stockée.

Les alias de types sont également couramment utilisés avec le type `Result<T, E>` pour réduire la répétition. Considérons le module `std::io` dans la bibliothèque standard. Les opérations d'I/O retournent souvent un `Result<T, E>` pour gérer les situations où les opérations échouent. Cette bibliothèque possède une structure `std::io::Error` qui représente toutes les erreurs potentielles d'I/O. Beaucoup de fonctions dans `std::io` retourneront un `Result<T, E>` où `E` est `std::io::Error`, comme ces fonctions dans le trait `Write` :

```rust,noplayground
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-05-write-trait/src/lib.rs}}
```

Le `Result<..., Error>` est répété de nombreuses fois. En conséquence, `std::io` a cette déclaration d'alias de type :

```rust,noplayground
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-06-result-alias/src/lib.rs:here}}
```

Étant donné que cette déclaration se trouve dans le module `std::io`, nous pouvons utiliser l'alias entièrement qualifié `std::io::Result<T>` ; c'est-à-dire un `Result<T, E>` avec `E` rempli comme `std::io::Error`. Les signatures de fonction du trait `Write` finissent par ressembler à ceci :

```rust,noplayground
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-06-result-alias/src/lib.rs:there}}
```

L'alias de type aide de deux manières : il rend le code plus facile à écrire _et_ il nous donne une interface cohérente dans tout `std::io`. Comme c'est un alias, c'est juste un autre `Result<T, E>`, ce qui signifie que nous pouvons utiliser toutes les méthodes qui fonctionnent sur `Result<T, E>` avec cela, ainsi que la syntaxe spéciale comme l'opérateur `?`.

### Le type Never qui ne renvoie jamais

Rust a un type spécial nommé `!` qui est connu dans le jargon de la théorie des types comme le _type vide_ car il n'a pas de valeurs. Nous préférons l'appeler le _type never_ car il se place à la place du type de retour lorsqu'une fonction ne renvoie jamais. Voici un exemple :

```rust,noplayground
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-07-never-type/src/lib.rs:here}}
```

Ce code se lit comme « la fonction `bar` ne renvoie jamais. » Les fonctions qui ne renvoient jamais sont appelées _fonctions divergent_. Nous ne pouvons pas créer de valeurs du type `!`, donc `bar` ne peut jamais renvoyer.

Mais à quoi bon un type pour lequel vous ne pouvez jamais créer de valeurs ? Rappelez-vous le code du Listing 2-5, qui faisait partie du jeu de devinettes de nombres ; nous en avons reproduit un peu ici dans le Listing 20-27.

<Listing number="20-27" caption="Un `match` avec un bras qui se termine par `continue`">

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-05/src/main.rs:ch19}}
```

</Listing>

À l'époque, nous avons passé certains détails sous silence dans ce code. Dans la section [« Le contrôle de flux `match` »][the-match-control-flow-construct] dans le Chapitre 6, nous avons discuté du fait que les bras `match` doivent tous retourner le même type. Donc, par exemple, le code suivant ne fonctionne pas :

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-08-match-arms-different-types/src/main.rs:here}}
```

Le type de `guess` dans ce code devrait être un entier _et_ une chaîne, et Rust exige que `guess` n'ait qu'un seul type. Alors, que renvoie `continue` ? Comment avons-nous pu retourner un `u32` d'un bras et avoir un autre bras qui se termine par `continue` dans le Listing 20-27 ?

Comme vous l'avez peut-être deviné, `continue` a une valeur de `!`. C'est-à-dire que lorsque Rust calcule le type de `guess`, il regarde les deux bras du match, le premier avec une valeur de `u32` et le second avec une valeur de `!`. Comme `!` ne peut jamais avoir de valeur, Rust décide que le type de `guess` est `u32`.

La manière formelle de décrire ce comportement est que les expressions de type `!` peuvent être coercées en tout autre type. Nous sommes autorisés à terminer ce bras `match` avec `continue` parce que `continue` ne renvoie pas de valeur ; au lieu de cela, cela renvoie le contrôle au début de la boucle, donc dans le cas de `Err`, nous n'assignons jamais une valeur à `guess`.

Le type never est également utile avec le macro `panic!`. Rappelez-vous la fonction `unwrap` que nous appelons sur les valeurs `Option<T>` pour produire une valeur ou paniquer avec cette définition :

```rust,ignore
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-09-unwrap-definition/src/lib.rs:here}}
```

Dans ce code, la même chose se produit que dans le `match` du Listing 20-27 : Rust voit que `val` a le type `T` et que `panic!` a le type `!`, donc le résultat de l'expression `match` globale est `T`. Ce code fonctionne parce que `panic!` ne produit pas de valeur ; il termine le programme. Dans le cas de `None`, nous ne retournerons pas de valeur depuis `unwrap`, donc ce code est valide.

Une dernière expression qui a le type `!` est une boucle :

```rust,ignore
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-10-loop-returns-never/src/main.rs:here}}
```

Ici, la boucle ne se termine jamais, donc `!` est la valeur de l'expression. Cependant, cela ne serait pas vrai si nous incluions un `break`, car la boucle se terminerait lorsque nous atteindrions le `break`.

### Types de taille dynamique et le trait `Sized`

Rust a besoin de connaître certains détails concernant ses types, comme combien d'espace allouer pour une valeur d'un type particulier. Cela laisse un coin du système de types un peu déroutant au début : le concept de _types de taille dynamique_. Parfois appelés _DSTs_ ou _types non dimensionnés_, ces types nous permettent d'écrire du code utilisant des valeurs dont nous ne pouvons connaître la taille qu'au moment de l'exécution.

Examinons les détails d'un type de taille dynamique appelé `str`, que nous avons utilisé tout au long du livre. C'est bien ça, pas `&str`, mais `str` tout seul, est un DST. Dans de nombreux cas, comme lors du stockage de texte saisi par un utilisateur, nous ne pouvons pas savoir combien de temps la chaîne est jusqu'à l'exécution. Cela signifie que nous ne pouvons pas créer une variable de type `str`, ni prendre un argument de type `str`. Considérons le code suivant, qui ne fonctionne pas :

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-11-cant-create-str/src/main.rs:here}}
```

Rust doit savoir combien de mémoire allouer pour toute valeur d'un type particulier, et toutes les valeurs d'un type doivent utiliser la même quantité de mémoire. Si Rust nous permettait d'écrire ce code, ces deux valeurs `str` devraient occuper le même espace. Mais elles ont des longueurs différentes : `s1` nécessite 12 octets de stockage et `s2` nécessite 15. C'est pourquoi il n'est pas possible de créer une variable contenant un type de taille dynamique.

Alors, que faisons-nous ? Dans ce cas, vous connaissez déjà la réponse : nous faisons que le type de `s1` et `s2` soit une tranche de chaîne (`&str`) plutôt que `str`. Rappelez-vous de la section [« Tranches de chaîne »][string-slices] du Chapitre 4, qui explique que la structure de données de tranche ne stocke que la position de départ et la longueur de la tranche. Ainsi, bien que `&T` soit une seule valeur qui stocke l'adresse mémoire de l'endroit où se trouve `T`, une tranche de chaîne est _deux_ valeurs : l'adresse de la `str` et sa longueur. Par conséquent, nous pouvons connaître la taille d'une valeur de tranche de chaîne à la compilation : elle est deux fois la longueur d'un `usize`. C'est-à-dire que nous connaissons toujours la taille d'une tranche de chaîne, peu importe la longueur de la chaîne à laquelle elle fait référence. En général, c'est ainsi que les types de taille dynamique sont utilisés dans Rust : ils ont un bit de métadonnées supplémentaire qui stocke la taille des informations dynamiques. La règle d'or des types de taille dynamique est que nous devons toujours mettre des valeurs de types de taille dynamique derrière un pointeur de quelque sorte.

Nous pouvons combiner `str` avec toutes sortes de pointeurs : par exemple, `Box<str>` ou `Rc<str>`. En fait, vous avez déjà vu cela auparavant mais avec un type de taille dynamique différent : les traits. Chaque trait est un type de taille dynamique auquel nous pouvons nous référer en utilisant le nom du trait. Dans la section [« Utilisation des objets de trait pour abstraire un comportement partagé »][using-trait-objects-to-abstract-over-shared-behavior] dans le Chapitre 18, nous avons mentionné que pour utiliser les traits comme objets de trait, nous devons les mettre derrière un pointeur, tel que `&dyn Trait` ou `Box<dyn Trait>` (`Rc<dyn Trait>` fonctionnerait aussi).

Pour travailler avec les DSTs, Rust fournit le trait `Sized` pour déterminer si la taille d'un type est connue à la compilation. Ce trait est automatiquement implémenté pour tout ce dont la taille est connue à la compilation. De plus, Rust ajoute implicitement une contrainte sur `Sized` à chaque fonction générique. C’est-à-dire qu’une définition de fonction générique comme celle-ci :

```rust,ignore
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-12-generic-fn-definition/src/lib.rs}}
```

est en réalité traitée comme si nous avions écrit ceci :

```rust,ignore
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-13-generic-implicit-sized-bound/src/lib.rs}}
```

Par défaut, les fonctions génériques ne fonctionneront qu'avec des types dont la taille est connue à la compilation. Cependant, vous pouvez utiliser la syntaxe spéciale suivante pour assouplir cette restriction :

```rust,ignore
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-14-generic-maybe-sized/src/lib.rs}}
```

Une contrainte de trait sur `?Sized` signifie « `T` peut être ou non `Sized` », et cette notation annule le défaut selon lequel les types génériques doivent avoir une taille connue à la compilation. La syntaxe `?Trait` avec ce sens n'est disponible que pour `Sized`, pas pour d'autres traits.

Notez également que nous avons changé le type du paramètre `t` de `T` à `&T`. Comme le type pourrait ne pas être `Sized`, nous devons l'utiliser derrière un type de pointeur. Dans ce cas, nous avons choisi une référence.

Ensuite, nous parlerons des fonctions et des closures !

[encapsulation-that-hides-implementation-details]: ch18-01-what-is-oo.html#encapsulation-that-hides-implementation-details
[string-slices]: ch04-03-slices.html#string-slices
[the-match-control-flow-construct]: ch06-02-match.html#the-match-control-flow-construct
[using-trait-objects-to-abstract-over-shared-behavior]: ch18-02-trait-objects.html#using-trait-objects-to-abstract-over-shared-behavior
[newtype]: ch20-02-advanced-traits.html#implementing-external-traits-with-the-newtype-pattern