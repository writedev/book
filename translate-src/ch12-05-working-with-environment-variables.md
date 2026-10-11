## Travailler avec les variables d’environnement

Nous allons améliorer le binaire `minigrep` en ajoutant une fonctionnalité : une option de recherche insensible à la casse que l’utilisateur peut activer au moyen d’une variable d’environnement. Nous pourrions en faire une option de ligne de commande et demander aux utilisateurs de la saisir chaque fois qu’ils veulent l’activer. Mais en choisissant plutôt une variable d’environnement, nous leur permettons de la définir une seule fois et de rendre ainsi toutes leurs recherches insensibles à la casse pendant toute la session du terminal.

<!-- Old headings. Do not remove or links may break. -->
<a id="writing-a-failing-test-for-the-case-insensitive-search-function"></a>

### Écrire un test qui échoue pour la recherche insensible à la casse

Nous allons d’abord ajouter à la bibliothèque `minigrep` une nouvelle fonction `search_case_insensitive`, qui sera appelée lorsque la variable d’environnement aura une valeur. Nous allons continuer à suivre le processus TDD : la première étape consiste donc à écrire à nouveau un test qui échoue. Nous allons ajouter un test pour la nouvelle fonction `search_case_insensitive` et renommer notre ancien test `one_result` en `case_sensitive` afin de clarifier les différences entre les deux tests, comme le montre la liste 12-20.

<Listing number="12-20" file-name="src/lib.rs" caption="Ajout d’un nouveau test qui échoue pour la fonction insensible à la casse que nous allons ajouter">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-20/src/lib.rs:here}}
```

</Listing>

Notez que nous avons également modifié le `contents` de l’ancien test. Nous avons ajouté une nouvelle ligne contenant le texte `"Duct tape."`, avec un _D_ majuscule, qui ne devrait pas correspondre à la requête `"duct"` lors d’une recherche sensible à la casse. Modifier ainsi l’ancien test permet de s’assurer que nous ne cassons pas accidentellement la fonctionnalité de recherche sensible à la casse que nous avons déjà implémentée. Ce test devrait réussir maintenant et continuer de réussir pendant que nous travaillons sur la recherche insensible à la casse.

Le nouveau test pour la recherche insensible à la casse utilise `"rUsT"` comme requête. Dans la fonction `search_case_insensitive` que nous allons ajouter, la requête `"rUsT"` devrait correspondre à la ligne contenant `"Rust:"`, avec un _R_ majuscule, et à la ligne `"Trust me."`, bien que la casse de ces deux chaînes diffère de celle de la requête. Voilà notre test qui échoue : il ne pourra pas être compilé, car nous n’avons pas encore défini la fonction `search_case_insensitive`. N’hésitez pas à ajouter une implémentation provisoire qui renvoie toujours un vecteur vide, comme nous l’avons fait pour la fonction `search` dans la liste 12-16, afin de pouvoir compiler le test et le voir échouer.

### Implémenter la fonction `search_case_insensitive`

La fonction `search_case_insensitive`, présentée dans la liste 12-21, sera presque identique à la fonction `search`. La seule différence est que nous convertirons en minuscules la `query` et chaque `line` afin que, quelle que soit la casse des arguments d’entrée, ils soient écrits de la même manière lorsque nous vérifierons si la ligne contient la requête.

<Listing number="12-21" file-name="src/lib.rs" caption="Définition de la fonction `search_case_insensitive` pour convertir en minuscules la requête et la ligne avant de les comparer">

```rust,noplayground
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-21/src/lib.rs:here}}
```

</Listing>

Tout d’abord, nous convertissons la chaîne `query` en minuscules et la stockons dans une nouvelle variable portant le même nom, ce qui masque la variable `query` d’origine. Il est nécessaire d’appeler `to_lowercase` sur la requête pour que, quelle que soit sa forme — `"rust"`, `"RUST"`, `"Rust"` ou `"rUsT"` —, nous la traitions comme si elle était `"rust"` et ne tenions pas compte de la casse. Bien que `to_lowercase` gère les caractères Unicode de base, cette gestion ne sera pas exacte à 100 %. Si nous écrivions une véritable application, nous voudrions approfondir ce point. Mais cette section porte sur les variables d’environnement, et non sur Unicode, nous allons donc nous en tenir là.

Notez que `query` est maintenant une `String` plutôt qu’une tranche de chaîne, car l’appel à `to_lowercase` crée de nouvelles données au lieu de faire référence à des données existantes. Prenons par exemple la requête `"rUsT"` : cette tranche de chaîne ne contient ni `u` ni `t` en minuscules que nous pourrions utiliser. Nous devons donc allouer une nouvelle `String` contenant `"rust"`. Lorsque nous passons maintenant `query` comme argument à la méthode `contains`, nous devons ajouter une esperluette, car la signature de `contains` indique qu’elle accepte une tranche de chaîne.

Ensuite, nous appelons `to_lowercase` sur chaque `line` pour convertir tous ses caractères en minuscules. Maintenant que nous avons converti `line` et `query` en minuscules, nous trouverons des correspondances quelle que soit la casse de la requête.

Voyons si cette implémentation réussit les tests :

```console
{{#include ../listings/ch12-an-io-project/listing-12-21/output.txt}}
```

Parfait ! Ils ont réussi. Appelons maintenant la nouvelle fonction `search_case_insensitive` depuis la fonction `run`. Tout d’abord, nous allons ajouter à la structure `Config` une option de configuration permettant de choisir entre une recherche sensible à la casse et une recherche insensible à la casse. L’ajout de ce champ provoquera des erreurs de compilation, car nous ne l’initialisons encore nulle part :

<span class="filename">Nom du fichier : src/main.rs</span>

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-22/src/main.rs:here}}
```

Nous avons ajouté le champ `ignore_case`, qui contient une valeur booléenne. Ensuite, la fonction `run` doit vérifier la valeur du champ `ignore_case` et s’en servir pour décider d’appeler la fonction `search` ou la fonction `search_case_insensitive`, comme le montre la liste 12-22. Cela ne compilera toujours pas.

<Listing number="12-22" file-name="src/main.rs" caption="Appel de `search` ou de `search_case_insensitive` selon la valeur de `config.ignore_case`">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-22/src/main.rs:there}}
```

</Listing>

Enfin, nous devons vérifier la variable d’environnement. Les fonctions permettant de travailler avec les variables d’environnement se trouvent dans le module `env` de la bibliothèque standard, qui est déjà inclus au début de _src/main.rs_. Nous utiliserons la fonction `var` du module `env` pour vérifier si une valeur a été définie pour une variable d’environnement nommée `IGNORE_CASE`, comme le montre la liste 12-23.

<Listing number="12-23" file-name="src/main.rs" caption="Vérification de la présence d’une valeur pour une variable d’environnement nommée `IGNORE_CASE`">

```rust,ignore,noplayground
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-23/src/main.rs:here}}
```

</Listing>

Ici, nous créons une nouvelle variable, `ignore_case`. Pour lui attribuer une valeur, nous appelons la fonction `env::var` et lui transmettons le nom de la variable d’environnement `IGNORE_CASE`. La fonction `env::var` renvoie un `Result` : si une valeur a été définie pour la variable d’environnement, le résultat sera la variante `Ok`, qui contient cette valeur. Si la variable d’environnement n’est pas définie, le résultat sera la variante `Err`.

Nous utilisons la méthode `is_ok` sur le `Result` pour vérifier si la variable d’environnement est définie, ce qui signifie que le programme doit effectuer une recherche insensible à la casse. Si la variable d’environnement `IGNORE_CASE` n’a aucune valeur, `is_ok` renvoie `false` et le programme effectue une recherche sensible à la casse. La _valeur_ de la variable d’environnement ne nous importe pas ; seule compte sa présence ou son absence. C’est pourquoi nous vérifions `is_ok` plutôt que d’utiliser `unwrap`, `expect` ou une autre des méthodes que nous avons vues sur `Result`.

Nous transmettons la valeur de la variable `ignore_case` à l’instance de `Config`, afin que la fonction `run` puisse la lire et décider d’appeler `search_case_insensitive` ou `search`, comme nous l’avons implémenté dans la liste 12-22.

Essayons ! D’abord, nous allons exécuter notre programme sans définir la variable d’environnement et avec la requête `to`, qui devrait correspondre à toute ligne contenant le mot _to_ entièrement en minuscules :

```console
{{#include ../listings/ch12-an-io-project/listing-12-23/output.txt}}
```

On dirait que cela fonctionne toujours ! Exécutons maintenant le programme avec `IGNORE_CASE` définie sur `1`, en conservant la même requête `to` :

```console
$ IGNORE_CASE=1 cargo run -- to poem.txt
```

Si vous utilisez PowerShell, vous devrez définir la variable d’environnement et exécuter le programme en deux commandes distinctes :

```console
PS> $Env:IGNORE_CASE=1; cargo run -- to poem.txt
```

La variable `IGNORE_CASE` restera ainsi définie jusqu’à la fin de votre session de terminal. Vous pouvez la supprimer à l’aide de l’applet de commande `Remove-Item` :

```console
PS> Remove-Item Env:IGNORE_CASE
```

Nous devrions obtenir des lignes contenant _to_, y compris celles où certaines lettres sont en majuscules :

<!-- manual-regeneration
cd listings/ch12-an-io-project/listing-12-23
IGNORE_CASE=1 cargo run -- to poem.txt
can't extract because of the environment variable
-->

```console
Are you nobody, too?
How dreary to be somebody!
To tell your name the livelong day
To an admiring bog!
```

Excellent, nous avons également obtenu les lignes contenant _To_ ! Notre programme `minigrep` peut maintenant effectuer des recherches insensibles à la casse, selon la valeur d’une variable d’environnement. Vous savez maintenant comment gérer des options définies au moyen d’arguments de ligne de commande ou de variables d’environnement.

Certains programmes permettent d’utiliser des arguments _et_ des variables d’environnement pour configurer la même option. Dans ce cas, ils déterminent lequel des deux a priorité. Pour un exercice que vous pouvez faire seul, essayez de contrôler la sensibilité à la casse au moyen d’un argument de ligne de commande ou d’une variable d’environnement. Décidez si l’argument de ligne de commande ou la variable d’environnement doit avoir priorité lorsque le programme est exécuté avec l’un réglé sur une recherche sensible à la casse et l’autre sur une recherche insensible à la casse.

Le module `std::env` contient de nombreuses autres fonctionnalités utiles pour gérer les variables d’environnement. Consultez sa documentation pour découvrir ce qui est disponible.