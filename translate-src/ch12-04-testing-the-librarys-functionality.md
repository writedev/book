<!-- Anciennes en-têtes. Ne pas supprimer ou les liens pourront se briser. -->
<a id="developing-the-librarys-functionality-with-test-driven-development"></a>

## Ajouter de la fonctionnalité avec le développement dirigé par les tests

Maintenant que nous avons la logique de recherche dans _src/lib.rs_ séparée de la fonction `main`, il est beaucoup plus facile d'écrire des tests pour la fonctionnalité principale de notre code. Nous pouvons appeler des fonctions directement avec divers arguments et vérifier les valeurs de retour sans avoir à appeler notre binaire depuis la ligne de commande.

Dans cette section, nous allons ajouter la logique de recherche au programme `minigrep` en utilisant le processus de développement dirigé par les tests (TDD) avec les étapes suivantes :

1. Écrire un test qui échoue et l'exécuter pour s'assurer qu'il échoue pour la raison que vous attendez.
2. Écrire ou modifier juste assez de code pour faire passer le nouveau test.
3. Refactoriser le code que vous venez d'ajouter ou de modifier et vous assurer que les tests continuent de passer.
4. Répéter à partir de l'étape 1 !

Bien que ce ne soit qu'une des nombreuses façons d'écrire un logiciel, le TDD peut aider à orienter la conception du code. Écrire le test avant d'écrire le code qui fait passer le test aide à maintenir une bonne couverture de test tout au long du processus.

Nous allons tester le développement de la fonctionnalité qui effectuera réellement la recherche de la chaîne de requête dans le contenu du fichier et produira une liste de lignes qui correspondent à la requête. Nous ajouterons cette fonctionnalité dans une fonction appelée `search`.

### Écrire un test échouant

Dans _src/lib.rs_, nous allons ajouter un module `tests` avec une fonction de test, comme nous l'avons fait dans [Chapitre 11][ch11-anatomy]<!-- ignore -->. La fonction de test précise le comportement que nous voulons que la fonction `search` ait : elle prendra une requête et le texte à rechercher, et elle ne renverra que les lignes du texte qui contiennent la requête. La Listing 12-15 montre ce test.

<Listing number="12-15" file-name="src/lib.rs" caption="Création d'un test échouant pour la fonction `search` pour la fonctionnalité que nous aimerions avoir">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-15/src/lib.rs:here}}
```

</Listing>

Ce test recherche la chaîne `"duct"`. Le texte que nous recherchons est constitué de trois lignes, dont une seule contient `"duct"` (notez que le caractère de retour après le guillemet d'ouverture indique à Rust de ne pas mettre un caractère de nouvelle ligne au début du contenu de cette chaîne littérale). Nous affirmons que la valeur renvoyée par la fonction `search` ne contient que la ligne que nous attendons.

Si nous exécutons ce test, il échouera actuellement car la macro `unimplemented!` panique avec le message « non implémenté ». Conformément aux principes du TDD, nous allons prendre une petite étape en ajoutant juste assez de code pour éviter que le test ne panique lors de l'appel de la fonction en définissant la fonction `search` pour renvoyer toujours un vecteur vide, comme montré dans la Listing 12-16. Ensuite, le test devrait compiler et échouer car un vecteur vide ne correspond pas à un vecteur contenant la ligne `"safe, fast, productive."`.

<Listing number="12-16" file-name="src/lib.rs" caption="Définition juste suffisante de la fonction `search` pour que l'appel ne panique pas">

```rust,noplayground
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-16/src/lib.rs:here}}
```

</Listing>

Discutons maintenant pourquoi nous devons définir un temps de vie explicite `'a` dans la signature de `search` et utiliser ce temps de vie avec l'argument `contents` et la valeur de retour. Rappelons-nous dans [Chapitre 10][ch10-lifetimes]<!-- ignore --> que les paramètres de durée de vie spécifient quel temps de vie d'argument est relié au temps de vie de la valeur de retour. Dans ce cas, nous indiquons que le vecteur renvoyé doit contenir des tranches de chaînes qui font référence à des tranches de l'argument `contents` (plutôt que de l'argument `query`).

En d'autres termes, nous disons à Rust que les données renvoyées par la fonction `search` vivront aussi longtemps que les données passées à la fonction `search` dans l'argument `contents`. C'est important ! Les données référencées _par_ une tranche doivent être valides pour que la référence soit valide ; si le compilateur suppose que nous faisons des tranches de chaînes de `query` plutôt que de `contents`, il effectuera ses vérifications de sécurité incorrectement.

Si nous oublions les annotations de temps de vie et essayons de compiler cette fonction, nous obtiendrons cette erreur :

```console
{{#include ../listings/ch12-an-io-project/output-only-02-missing-lifetimes/output.txt}}
```

Rust ne peut pas savoir lequel des deux paramètres nous avons besoin pour la sortie, donc nous devons le lui indiquer explicitement. Notez que le texte d'aide suggère de spécifier le même paramètre de durée de vie pour tous les paramètres et le type de sortie, ce qui est incorrect ! Parce que `contents` est le paramètre qui contient tout notre texte et que nous voulons retourner les parties de ce texte qui correspondent, nous savons que `contents` est le seul paramètre qui devrait être relié à la valeur de retour en utilisant la syntaxe des durées de vie.

D'autres langages de programmation ne nécessitent pas de relier les arguments aux valeurs de retour dans la signature, mais cette pratique deviendra plus facile avec le temps. Vous pourriez vouloir comparer cet exemple avec les exemples de la section [« Validation des Références avec les Durées de Vie »][validating-references-with-lifetimes]<!-- ignore --> dans le Chapitre 10.

### Écrire du code pour faire passer le test

Actuellement, notre test échoue car nous renvoyons toujours un vecteur vide. Pour corriger cela et implémenter `search`, notre programme doit suivre ces étapes :

1. Itérer à travers chaque ligne du contenu.
2. Vérifier si la ligne contient notre chaîne de requête.
3. Si c'est le cas, l'ajouter à la liste des valeurs que nous renvoyons.
4. Si ce n'est pas le cas, ne rien faire.
5. Retourner la liste des résultats qui correspondent.

Développons chaque étape, en commençant par l'itération à travers les lignes.

#### Itérer à travers les lignes avec la méthode `lines`

Rust dispose d'une méthode utile pour gérer l'itération ligne par ligne des chaînes, nommée `lines`, qui fonctionne comme indiqué dans la Listing 12-17. Notez que cela ne compilera pas encore.

<Listing number="12-17" file-name="src/lib.rs" caption="Itération à travers chaque ligne dans `contents`">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-17/src/lib.rs:here}}
```

</Listing>

La méthode `lines` renvoie un itérateur. Nous parlerons des itérateurs en profondeur dans [Chapitre 13][ch13-iterators]<!-- ignore -->. Mais rappelez-vous que vous avez vu cette façon d'utiliser un itérateur dans [Listing 3-5][ch3-iter]<!-- ignore -->, où nous avons utilisé une boucle `for` avec un itérateur pour exécuter du code sur chaque élément d'une collection.

#### Rechercher chaque ligne pour la requête

Ensuite, nous allons vérifier si la ligne actuelle contient notre chaîne de requête. Heureusement, les chaînes ont une méthode utile nommée `contains` qui s'en charge pour nous ! Ajoutez un appel à la méthode `contains` dans la fonction `search`, comme le montre la Listing 12-18. Notez que cela ne compilera toujours pas.

<Listing number="12-18" file-name="src/lib.rs" caption="Ajout de la fonctionnalité pour voir si la ligne contient la chaîne dans `query`">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-18/src/lib.rs:here}}
```

</Listing>

Pour le moment, nous construisons la fonctionnalité. Pour que le code se compile, nous devons retourner une valeur du corps comme nous l'avons indiqué dans la signature de la fonction.

#### Stocker les lignes correspondantes

Pour terminer cette fonction, nous avons besoin d'un moyen de stocker les lignes correspondantes que nous voulons retourner. Pour cela, nous pouvons créer un vecteur mutable avant la boucle `for` et appeler la méthode `push` pour stocker une `line` dans le vecteur. Après la boucle `for`, nous retournons le vecteur, comme le montre la Listing 12-19.

<Listing number="12-19" file-name="src/lib.rs" caption="Stocker les lignes qui correspondent pour que nous puissions les retourner">

```rust,ignore
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-19/src/lib.rs:here}}
```

</Listing>

Maintenant, la fonction `search` devrait retourner uniquement les lignes contenant `query`, et notre test devrait passer. Exécutons le test :

```console
{{#include ../listings/ch12-an-io-project/listing-12-19/output.txt}}
```

Notre test est passé, donc nous savons que cela fonctionne !

À ce stade, nous pourrions envisager des opportunités pour refactoriser l'implémentation de la fonction de recherche tout en maintenant les tests réussis pour conserver la même fonctionnalité. Le code de la fonction `search` n'est pas trop mauvais, mais il ne profite pas de certaines caractéristiques utiles des itérateurs. Nous reviendrons sur cet exemple dans [Chapitre 13][ch13-iterators]<!-- ignore -->, où nous explorerons les itérateurs en détail et verrons comment l'améliorer.

Maintenant, tout le programme devrait fonctionner ! Essayons, d'abord avec un mot qui devrait renvoyer exactement une ligne du poème d'Emily Dickinson : _frog_.

```console
{{#include ../listings/ch12-an-io-project/no-listing-02-using-search-in-run/output.txt}}
```

Super ! Essayons maintenant un mot qui correspondra à plusieurs lignes, comme _body_ :

```console
{{#include ../listings/ch12-an-io-project/output-only-03-multiple-matches/output.txt}}
```

Et enfin, assurons-nous que nous ne recevons aucune ligne lorsque nous recherchons un mot qui n'est nulle part dans le poème, tel que _monomorphization_ :

```console
{{#include ../listings/ch12-an-io-project/output-only-04-no-matches/output.txt}}
```

Excellent ! Nous avons construit notre propre mini version d'un outil classique et avons beaucoup appris sur la façon de structurer des applications. Nous avons également appris un peu sur la saisie et la sortie de fichiers, les durées de vie, les tests et l'analyse des lignes de commande.

Pour compléter ce projet, nous allons brièvement démontrer comment travailler avec des variables d'environnement et comment imprimer dans l'erreur standard, qui sont toutes deux utiles lorsque vous écrivez des programmes en ligne de commande.

[validating-references-with-lifetimes]: ch10-03-lifetime-syntax.html#validating-references-with-lifetimes
[ch11-anatomy]: ch11-01-writing-tests.html#the-anatomy-of-a-test-function
[ch10-lifetimes]: ch10-03-lifetime-syntax.html
[ch3-iter]: ch03-05-control-flow.html#looping-through-a-collection-with-for
[ch13-iterators]: ch13-02-iterators.html