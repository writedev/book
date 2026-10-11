<!-- Old headings. Do not remove or links may break. -->
<a id="developing-the-librarys-functionality-with-test-driven-development"></a>

## Ajouter des fonctionnalités avec le développement piloté par les tests

Maintenant que la logique de recherche se trouve dans _src/lib.rs_, séparée de la fonction `main`, il est beaucoup plus facile d’écrire des tests pour les fonctionnalités essentielles de notre code. Nous pouvons appeler directement les fonctions avec différents arguments et vérifier les valeurs de retour sans avoir à lancer notre binaire depuis la ligne de commande.

Dans cette section, nous allons ajouter la logique de recherche au programme `minigrep` en suivant le processus de développement piloté par les tests (TDD), selon les étapes suivantes :

1. Écrire un test qui échoue et l’exécuter pour vérifier qu’il échoue pour la raison attendue.
2. Écrire ou modifier juste assez de code pour que le nouveau test réussisse.
3. Refactoriser le code que vous venez d’ajouter ou de modifier et vérifier que les tests continuent de réussir.
4. Recommencer à l’étape 1 !

Bien qu’il ne s’agisse que d’une des nombreuses façons d’écrire des logiciels, le TDD peut aider à orienter la conception du code. Écrire le test avant le code qui le fera réussir permet de maintenir une couverture de tests élevée tout au long du processus.

Nous allons utiliser le développement piloté par les tests pour implémenter la fonctionnalité qui recherchera la chaîne de requête dans le contenu du fichier et produira une liste des lignes qui correspondent. Nous ajouterons cette fonctionnalité dans une fonction appelée `search`.

### Écrire un test qui échoue

Dans _src/lib.rs_, nous allons ajouter un module `tests` avec une fonction de test, comme nous l’avons fait au [chapitre 11][ch11-anatomy]<!-- ignore -->. La fonction de test décrit le comportement attendu de la fonction `search` : elle prend une requête et le texte dans lequel effectuer la recherche, puis renvoie uniquement les lignes du texte qui contiennent la requête. Ce test est présenté dans la liste 12-15.

<Listing number="12-15" file-name="src/lib.rs" caption="Créer un test qui échoue pour la fonction `search` et la fonctionnalité souhaitée">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-15/src/lib.rs:here}}
```

</Listing>

Ce test recherche la chaîne `"duct"`. Le texte dans lequel nous effectuons la recherche comporte trois lignes, dont une seule contient `"duct"` (notez que la barre oblique inverse après le guillemet double ouvrant indique à Rust de ne pas placer de caractère de nouvelle ligne au début du contenu de ce littéral de chaîne). Nous vérifions que la valeur renvoyée par la fonction `search` contient uniquement la ligne attendue.

Si nous lançons ce test, il échouera pour le moment, car la macro `unimplemented!` provoque une panique avec le message « not implemented ». Conformément aux principes du TDD, nous allons faire un petit pas en ajoutant juste assez de code pour que l’appel de la fonction ne provoque pas de panique : nous allons définir la fonction `search` de façon à ce qu’elle renvoie toujours un vecteur vide, comme dans la liste 12-16. Le test devrait alors compiler et échouer, car un vecteur vide ne correspond pas à un vecteur contenant la ligne `"safe, fast, productive."`.

<Listing number="12-16" file-name="src/lib.rs" caption="Définir juste assez la fonction `search` pour que son appel ne provoque pas de panique">

```rust,noplayground
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-16/src/lib.rs:here}}
```

</Listing>

Voyons maintenant pourquoi nous devons définir une durée de vie explicite `'a` dans la signature de `search` et utiliser cette durée de vie pour l’argument `contents` et la valeur de retour. Rappelez-vous qu’au [chapitre 10][ch10-lifetimes]<!-- ignore -->, nous avons vu que les paramètres de durée de vie précisent quelle durée de vie des arguments est liée à celle de la valeur de retour. Dans ce cas, nous indiquons que le vecteur renvoyé doit contenir des tranches de chaînes qui font référence à des tranches de l’argument `contents` (plutôt qu’à l’argument `query`).

Autrement dit, nous indiquons à Rust que les données renvoyées par la fonction `search` vivront aussi longtemps que les données transmises à la fonction `search` dans l’argument `contents`. C’est important ! Les données référencées par une tranche doivent être valides pour que la référence le soit aussi ; si le compilateur suppose que nous créons des tranches de chaînes à partir de `query` plutôt que de `contents`, il effectuera incorrectement ses vérifications de sûreté.

Si nous oublions les annotations de durée de vie et essayons de compiler cette fonction, nous obtiendrons cette erreur :

```console
{{#include ../listings/ch12-an-io-project/output-only-02-missing-lifetimes/output.txt}}
```

Rust ne peut pas savoir lequel des deux paramètres utiliser pour la sortie ; nous devons donc le lui indiquer explicitement. Notez que le texte d’aide suggère de préciser le même paramètre de durée de vie pour tous les paramètres et le type de sortie, ce qui est incorrect ! Comme `contents` est le paramètre qui contient tout notre texte et que nous voulons renvoyer les parties de ce texte qui correspondent, nous savons que `contents` est le seul paramètre qui doit être lié à la valeur de retour au moyen de la syntaxe des durées de vie.

Les autres langages de programmation n’exigent pas de lier les arguments aux valeurs de retour dans la signature, mais cette pratique deviendra plus facile avec le temps. Vous pouvez comparer cet exemple à ceux de la section [« Valider les références avec les durées de vie »][validating-references-with-lifetimes]<!-- ignore --> du chapitre 10.

### Écrire du code pour réussir le test

Pour le moment, notre test échoue parce que nous renvoyons toujours un vecteur vide. Pour corriger cela et implémenter `search`, notre programme doit suivre les étapes suivantes :

1. Parcourir chaque ligne du contenu.
2. Vérifier si la ligne contient notre chaîne de requête.
3. Si c’est le cas, l’ajouter à la liste des valeurs que nous renvoyons.
4. Sinon, ne rien faire.
5. Renvoyer la liste des résultats correspondants.

Examinons chaque étape, en commençant par le parcours des lignes.

#### Parcourir les lignes avec la méthode `lines`

Rust dispose d’une méthode pratique pour parcourir une chaîne ligne par ligne, qui s’appelle `lines`. Elle fonctionne comme indiqué dans la liste 12-17. Notez que ce code ne compilera pas encore.

<Listing number="12-17" file-name="src/lib.rs" caption="Parcourir chaque ligne de `contents`">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-17/src/lib.rs:here}}
```

</Listing>

La méthode `lines` renvoie un itérateur. Nous parlerons des itérateurs en détail au [chapitre 13][ch13-iterators]<!-- ignore -->. Mais rappelez-vous que vous avez vu cette façon d’utiliser un itérateur dans la [liste 3-5][ch3-iter]<!-- ignore -->, où nous avons utilisé une boucle `for` avec un itérateur pour exécuter du code sur chaque élément d’une collection.

#### Rechercher la requête dans chaque ligne

Ensuite, nous allons vérifier si la ligne courante contient notre chaîne de requête. Heureusement, les chaînes disposent d’une méthode pratique appelée `contains` qui s’en charge pour nous ! Ajoutez un appel à la méthode `contains` dans la fonction `search`, comme indiqué dans la liste 12-18. Notez que ce code ne compilera toujours pas.

<Listing number="12-18" file-name="src/lib.rs" caption="Ajouter une fonctionnalité pour vérifier si la ligne contient la chaîne de `query`">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-18/src/lib.rs:here}}
```

</Listing>

Pour le moment, nous construisons progressivement cette fonctionnalité. Pour que le code compile, nous devons renvoyer une valeur à la fin du corps de la fonction, comme indiqué dans sa signature.

#### Stocker les lignes correspondantes

Pour terminer cette fonction, nous avons besoin d’un moyen de stocker les lignes correspondantes que nous voulons renvoyer. Pour cela, nous pouvons créer un vecteur mutable avant la boucle `for` et appeler la méthode `push` pour y stocker une `line`. Après la boucle `for`, nous renvoyons le vecteur, comme indiqué dans la liste 12-19.

<Listing number="12-19" file-name="src/lib.rs" caption="Stocker les lignes correspondantes afin de pouvoir les renvoyer">

```rust,ignore
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-19/src/lib.rs:here}}
```

</Listing>

La fonction `search` devrait maintenant renvoyer uniquement les lignes qui contiennent `query`, et notre test devrait réussir. Lançons-le :

```console
{{#include ../listings/ch12-an-io-project/listing-12-19/output.txt}}
```

Notre test a réussi, nous savons donc que cela fonctionne !

À ce stade, nous pourrions envisager de refactoriser l’implémentation de la fonction de recherche tout en gardant les tests réussis, afin de conserver la même fonctionnalité. Le code de la fonction `search` n’est pas trop mauvais, mais il ne tire pas parti de certaines fonctionnalités pratiques des itérateurs. Nous reviendrons sur cet exemple au [chapitre 13][ch13-iterators]<!-- ignore -->, où nous examinerons les itérateurs en détail et verrons comment l’améliorer.

Le programme entier devrait maintenant fonctionner ! Essayons-le d’abord avec un mot qui devrait renvoyer exactement une ligne du poème d’Emily Dickinson : _frog_.

```console
{{#include ../listings/ch12-an-io-project/no-listing-02-using-search-in-run/output.txt}}
```

Super ! Essayons maintenant un mot qui correspond à plusieurs lignes, comme _body_ :

```console
{{#include ../listings/ch12-an-io-project/output-only-03-multiple-matches/output.txt}}
```

Enfin, vérifions que nous n’obtenons aucune ligne lorsque nous recherchons un mot qui n’apparaît nulle part dans le poème, comme _monomorphization_ :

```console
{{#include ../listings/ch12-an-io-project/output-only-04-no-matches/output.txt}}
```

Excellent ! Nous avons créé notre propre version miniature d’un outil classique et appris beaucoup de choses sur la structuration des applications. Nous avons également appris quelques notions sur les entrées et sorties de fichiers, les durées de vie, les tests et l’analyse des arguments de la ligne de commande.

Pour terminer ce projet, nous allons montrer brièvement comment utiliser des variables d’environnement et comment écrire sur la sortie d’erreur standard, deux techniques utiles pour écrire des programmes en ligne de commande.

[validating-references-with-lifetimes]: ch10-03-lifetime-syntax.html#validating-references-with-lifetimes
[ch11-anatomy]: ch11-01-writing-tests.html#the-anatomy-of-a-test-function
[ch10-lifetimes]: ch10-03-lifetime-syntax.html
[ch3-iter]: ch03-05-control-flow.html#looping-through-a-collection-with-for
[ch13-iterators]: ch13-02-iterators.html