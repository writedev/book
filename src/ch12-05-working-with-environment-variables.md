## Travailler avec des Variables d'Environnement

Nous allons améliorer le binaire `minigrep` en ajoutant une fonctionnalité supplémentaire : une option pour la recherche insensible à la casse que l'utilisateur peut activer via une variable d'environnement. Nous pourrions faire de cette fonctionnalité une option de ligne de commande et exiger que les utilisateurs la saisissent chaque fois qu'ils veulent qu'elle s'applique, mais en la transformant plutôt en une variable d'environnement, nous permettons à nos utilisateurs de configurer la variable d'environnement une fois et d'avoir toutes leurs recherches insensibles à la casse lors de cette session de terminal.

<!-- Ancien en-tête. Ne pas supprimer ou les liens pourraient être rompues. -->
<a id="écriture-dun-test-échoué-pour-la-fonction-de-recherche-insensible-à-la-casse"></a>

### Écriture d'un Test Échoué pour la Recherche Insensible à la Casse

Nous ajoutons d'abord une nouvelle fonction `search_case_insensitive` à la bibliothèque `minigrep` qui sera appelée lorsque la variable d'environnement a une valeur. Nous continuerons à suivre le processus TDD, donc la première étape consiste à écrire à nouveau un test échoué. Nous ajouterons un nouveau test pour la nouvelle fonction `search_case_insensitive` et renommerons notre ancien test de `one_result` à `case_sensitive` pour clarifier les différences entre les deux tests, comme montré dans la Liste 12-20.

<Listing number="12-20" file-name="src/lib.rs" caption="Ajout d'un nouveau test échoué pour la fonction insensible à la casse que nous allons ajouter">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-20/src/lib.rs:here}}
```

</Listing>

Notez que nous avons également modifié le `contents` de l'ancien test. Nous avons ajouté une nouvelle ligne avec le texte `"Duct tape."` utilisant un _D_ majuscule qui ne devrait pas correspondre à la requête `"duct"` lorsque nous recherchons de manière sensible à la casse. Modifier l'ancien test de cette manière aide à garantir que nous ne rompions pas accidentellement la fonctionnalité de recherche sensible à la casse que nous avons déjà mise en œuvre. Ce test devrait passer maintenant et continuer à passer pendant que nous travaillons sur la recherche insensible à la casse.

Le nouveau test pour la recherche insensible à la casse utilise `"rUsT"` comme requête. Dans la fonction `search_case_insensitive` que nous sommes sur le point d'ajouter, la requête `"rUsT"` devrait correspondre à la ligne contenant `"Rust:"` avec un _R_ majuscule et correspondre à la ligne `"Trust me."` bien que les deux aient des cas différents de la requête. C'est notre test échoué, et il échouera à la compilation car nous n'avons pas encore défini la fonction `search_case_insensitive`. N'hésitez pas à ajouter une implémentation squelette qui renvoie toujours un vecteur vide, de manière similaire à ce que nous avons fait pour la fonction `search` dans la Liste 12-16 afin de voir le test compiler et échouer.

### Implémentation de la Fonction `search_case_insensitive`

La fonction `search_case_insensitive`, montrée dans la Liste 12-21, sera presque la même que la fonction `search`. La seule différence est que nous mettrons la chaîne `query` et chaque `line` en minuscules afin que peu importe le cas des arguments d'entrée, ils soient du même cas lorsque nous vérifions si la ligne contient la requête.

<Listing number="12-21" file-name="src/lib.rs" caption="Définition de la fonction `search_case_insensitive` pour mettre en minuscules la requête et la ligne avant de les comparer">

```rust,noplayground
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-21/src/lib.rs:here}}
```

</Listing>

Tout d'abord, nous mettons la chaîne `query` en minuscules et la stockons dans une nouvelle variable avec le même nom, masquant ainsi la requête originale. Appeler `to_lowercase` sur la requête est nécessaire afin que peu importe si la requête de l'utilisateur est `"rust"`, `"RUST"`, `"Rust"` ou `"rUsT"`, nous traiterons la requête comme si elle était `"rust"` et nous serons insensibles à la casse. Bien que `to_lowercase` gère les cas Unicode de base, il ne sera pas 100 % précis. Si nous écrivions une véritable application, nous voudrions faire un peu plus de travail ici, mais cette section concerne les variables d'environnement, pas Unicode, donc nous nous en tiendrons à cela ici.

Notez que `query` est maintenant une `String` plutôt qu'une tranche de chaîne car l'appel à `to_lowercase` crée de nouvelles données plutôt que de référencer des données existantes. Supposons que la requête soit `"rUsT"` : cette tranche de chaîne ne contient pas un `u` ou un `t` en minuscules que nous pouvons utiliser, donc nous devons allouer une nouvelle `String` contenant `"rust"`. Lorsque nous passons `query` comme argument à la méthode `contains` maintenant, nous devons ajouter un ampersand car la signature de `contains` est définie pour prendre une tranche de chaîne.

Ensuite, nous ajoutons un appel à `to_lowercase` sur chaque `line` pour mettre toutes les lettres en minuscules. Maintenant que nous avons converti `line` et `query` en minuscules, nous trouverons des correspondances peu importe le cas de la requête.

Voyons si cette implémentation passe les tests :

```console
{{#include ../listings/ch12-an-io-project/listing-12-21/output.txt}}
```

Super ! Ils ont passé. Maintenant, appelons la nouvelle fonction `search_case_insensitive` depuis la fonction `run`. Tout d'abord, nous ajouterons une option de configuration à la structure `Config` pour basculer entre une recherche sensible à la casse et une recherche insensible à la casse. L'ajout de ce champ entraînera des erreurs de compilation car nous n'initialisons pas ce champ nulle part encore :

<span class="filename">Nom de fichier : src/main.rs</span>

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-22/src/main.rs:here}}
```

Nous avons ajouté le champ `ignore_case` qui contient un Booléen. Ensuite, nous avons besoin que la fonction `run` vérifie la valeur du champ `ignore_case` et l'utilise pour décider d'appeler la fonction `search` ou la fonction `search_case_insensitive`, comme montré dans la Liste 12-22. Cela ne compilera toujours pas encore.

<Listing number="12-22" file-name="src/main.rs" caption="Appel de `search` ou de `search_case_insensitive` en fonction de la valeur dans `config.ignore_case`">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-22/src/main.rs:there}}
```

</Listing>

Enfin, nous devons vérifier la variable d'environnement. Les fonctions pour travailler avec les variables d'environnement se trouvent dans le module `env` de la bibliothèque standard, qui est déjà dans le scope en haut de _src/main.rs_. Nous allons utiliser la fonction `var` du module `env` pour vérifier si une valeur a été définie pour une variable d'environnement nommée `IGNORE_CASE`, comme montré dans la Liste 12-23.

<Listing number="12-23" file-name="src/main.rs" caption="Vérification de toute valeur dans une variable d'environnement nommée `IGNORE_CASE`">

```rust,ignore,noplayground
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-23/src/main.rs:here}}
```

</Listing>

Ici, nous créons une nouvelle variable, `ignore_case`. Pour définir sa valeur, nous appelons la fonction `env::var` et lui passons le nom de la variable d'environnement `IGNORE_CASE`. La fonction `env::var` renvoie un `Result` qui sera le variant `Ok` réussi contenant la valeur de la variable d'environnement si elle est définie à une valeur quelconque. Elle retournera le variant `Err` si la variable d'environnement n'est pas définie.

Nous utilisons la méthode `is_ok` sur le `Result` pour vérifier si la variable d'environnement est définie, ce qui signifie que le programme devrait effectuer une recherche insensible à la casse. Si la variable d'environnement `IGNORE_CASE` n'est pas définie, `is_ok` renverra `false` et le programme effectuera une recherche sensible à la casse. Nous ne nous soucions pas de la _valeur_ de la variable d'environnement, juste de savoir si elle est configurée ou non, nous vérifions donc `is_ok` plutôt que d'utiliser `unwrap`, `expect`, ou d'autres méthodes que nous avons vues sur `Result`.

Nous passons la valeur de la variable `ignore_case` à l'instance `Config` afin que la fonction `run` puisse lire cette valeur et décider d'appeler `search_case_insensitive` ou `search`, comme nous l'avons implémenté dans la Liste 12-22.

Essayons cela ! Tout d'abord, nous allons exécuter notre programme sans la variable d'environnement définie et avec la requête `to`, qui devrait correspondre à toute ligne contenant le mot _to_ en minuscules :

```console
{{#include ../listings/ch12-an-io-project/listing-12-23/output.txt}}
```

Il semble que cela fonctionne toujours ! Maintenant, exécutons le programme avec `IGNORE_CASE` défini sur `1` mais avec la même requête `to` :

```console
$ IGNORE_CASE=1 cargo run -- to poem.txt
```

Si vous utilisez PowerShell, vous devez définir la variable d'environnement et exécuter le programme en tant que commandes distinctes :

```console
PS> $Env:IGNORE_CASE=1; cargo run -- to poem.txt
```

Cela fera en sorte que `IGNORE_CASE` persiste pour le reste de votre session shell. Il peut être supprimé avec la cmdlet `Remove-Item` :

```console
PS> Remove-Item Env:IGNORE_CASE
```

Nous devrions obtenir des lignes contenant _to_ qui pourraient avoir des lettres majuscules :

<!-- régénération manuelle
cd listings/ch12-an-io-project/listing-12-23
IGNORE_CASE=1 cargo run -- to poem.txt
can't extract because of the environment variable
-->

```console
Es-tu personne, aussi ?
Quelle tristesse d'être quelqu'un !
Pour dire ton nom toute la journée
À un marais admiratif !
```

Excellent, nous avons aussi obtenu des lignes contenant _To_ ! Notre programme `minigrep` peut maintenant effectuer des recherches insensibles à la casse contrôlées par une variable d'environnement. Maintenant, vous savez comment gérer les options définies à l'aide soit d'arguments de ligne de commande, soit de variables d'environnement.

Certains programmes permettent des arguments _et_ des variables d'environnement pour la même configuration. Dans ces cas, les programmes décident que l'un ou l'autre a la priorité. Pour un autre exercice à faire seul, essayez de contrôler la sensibilité à la casse via soit un argument de ligne de commande, soit une variable d'environnement. Décidez si l'argument de ligne de commande ou la variable d'environnement devrait avoir la priorité si le programme est exécuté avec l'un défini sur sensible à la casse et l'autre sur insensible à la casse. 

Le module `std::env` contient beaucoup plus de fonctionnalités utiles pour gérer les variables d'environnement : consultez sa documentation pour voir ce qui est disponible.