## Rust non sécurisé

Tout le code dont nous avons discuté jusqu'à présent a eu les garanties de sécurité de la mémoire de Rust appliquées à la compilation. Cependant, Rust a une seconde langue cachée à l'intérieur qui n'applique pas ces garanties de sécurité de la mémoire : elle s'appelle _Rust non sécurisé_ et fonctionne exactement comme Rust normal mais nous donne des superpouvoirs supplémentaires.

Rust non sécurisé existe parce qu'à la nature, l'analyse statique est conservatrice. Lorsque le compilateur essaie de déterminer si le code respecte les garanties, il est préférable de rejeter certains programmes valides plutôt que d'accepter des programmes invalides. Bien que le code _puisse_ être correct, si le compilateur Rust n'a pas suffisamment d'informations pour être confiant, il rejettera le code. Dans ces cas, vous pouvez utiliser du code non sécurisé pour dire au compilateur : « Fais-moi confiance, je sais ce que je fais. » Soyez averti, cependant, que vous utilisez Rust non sécurisé à vos propres risques : si vous utilisez du code non sécurisé de manière incorrecte, des problèmes peuvent survenir en raison de l'instabilité de la mémoire, comme le déréférencement de pointeur nul.

Une autre raison pour laquelle Rust a un alter ego non sécurisé est que le matériel informatique sous-jacent est par nature dangereux. Si Rust ne vous permettait pas d'effectuer des opérations non sécurisées, vous ne pourriez pas accomplir certaines tâches. Rust doit vous permettre de faire de la programmation système de bas niveau, comme interagir directement avec le système d'exploitation ou même écrire votre propre système d'exploitation. Travailler avec la programmation système de bas niveau est l'un des objectifs du langage. Explorons ce que nous pouvons faire avec Rust non sécurisé et comment le faire.

<a id="unsafe-superpowers"></a>

### Exercer des Superpouvoirs Non Sécurisés

Pour passer à Rust non sécurisé, utilisez le mot-clé `unsafe` et commencez ensuite un nouveau bloc qui contient le code non sécurisé. Vous pouvez effectuer cinq actions en Rust non sécurisé que vous ne pouvez pas en Rust sécurisé, que nous appelons _superpouvoirs non sécurisés_. Ces superpouvoirs incluent la capacité à :

1. Déréférencer un pointeur brut.
2. Appeler une fonction ou une méthode non sécurisée.
3. Accéder ou modifier une variable statique mutable.
4. Mettre en œuvre un trait non sécurisé.
5. Accéder aux champs des `union`s.

Il est important de comprendre que `unsafe` ne désactive pas le vérificateur d'emprunt ni ne désactive aucune autre vérification de sécurité de Rust : si vous utilisez une référence dans du code non sécurisé, elle sera toujours vérifiée. Le mot-clé `unsafe` vous donne seulement accès à ces cinq fonctionnalités qui ne sont ensuite pas vérifiées par le compilateur pour la sécurité de la mémoire. Vous obtiendrez toujours un certain degré de sécurité à l'intérieur d'un bloc non sécurisé.

De plus, `unsafe` ne signifie pas que le code à l'intérieur du bloc est nécessairement dangereux ou qu'il aura certainement des problèmes de sécurité de la mémoire : l'objectif est qu'en tant que programmeur, vous vous assuriez que le code à l'intérieur d'un bloc `unsafe` accédera à la mémoire de manière valide.

Les gens sont faillibles et des erreurs se produiront, mais en exigeant que ces cinq opérations non sécurisées se trouvent à l'intérieur de blocs annotés avec `unsafe`, vous saurez que toutes les erreurs liées à la sécurité de la mémoire doivent se trouver dans un bloc `unsafe`. Gardez les blocs `unsafe` petits ; vous en serez reconnaissant plus tard lorsque vous enquêterez sur des bugs de mémoire.

Pour isoler le code non sécurisé autant que possible, il est préférable d'enfermer ce code dans une abstraction sûre et de fournir une API sécurisée, que nous discuterons plus tard dans le chapitre lorsque nous examinerons les fonctions et méthodes non sécurisées. Certaines parties de la bibliothèque standard sont mises en œuvre comme des abstractions sûres au-dessus de code non sécurisé qui a été audité. Enveloppant le code non sécurisé dans une abstraction sûre, vous empêchez les utilisations de `unsafe` de déborder dans tous les endroits où vous ou vos utilisateurs pourriez vouloir utiliser la fonctionnalité mise en œuvre avec du code non sécurisé, car l'utilisation d'une abstraction sûre est sûre.

Examinons chacun des cinq superpouvoirs non sécurisés à tour de rôle. Nous examinerons également certaines abstractions qui fournissent une interface sécurisée au code non sécurisé.

### Déréférencer un Pointeur Brut

Dans le Chapitre 4, dans la section [« Références Dangling »][dangling-references], nous avons mentionné que le compilateur veille à ce que les références soient toujours valides. Rust non sécurisé a deux nouveaux types appelés _pointeurs bruts_ qui sont similaires aux références. Comme pour les références, les pointeurs bruts peuvent être immuables ou mutables et sont notés comme `*const T` et `*mut T`, respectivement. L'astérisque n'est pas l'opérateur de déréférencement ; c'est une partie du nom du type. Dans le contexte des pointeurs bruts, _immuable_ signifie que le pointeur ne peut pas être directement assigné après avoir été déréférencé.

Différent des références et des pointeurs intelligents, les pointeurs bruts :

- Peuvent ignorer les règles d'emprunt en ayant à la fois des pointeurs immuables et mutables, ou plusieurs pointeurs mutables vers le même emplacement
- Ne garantissent pas de pointer vers une mémoire valide
- Peuvent être nuls
- N'implémentent aucun nettoyage automatique

En optant pour ne pas faire respecter ces garanties par Rust, vous pouvez abandonner la sécurité garantie en échange d'une performance plus grande ou de la capacité à interagir avec une autre langue ou un matériel où les garanties de Rust ne s'appliquent pas.

L'énumération 20-1 montre comment créer un pointeur brut immuable et un pointeur brut mutable.

<Énumération numéro="20-1" légende="Création de pointeurs bruts avec les opérateurs d'emprunt brut">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-01/src/main.rs:here}}
```

</Énumération>

Remarquez que nous n'incluons pas le mot-clé `unsafe` dans ce code. Nous pouvons créer des pointeurs bruts dans un code sûr ; nous ne pouvons juste pas déréférencer des pointeurs bruts en dehors d'un bloc non sécurisé, comme vous le verrez bientôt.

Nous avons créé des pointeurs bruts en utilisant les opérateurs d'emprunt brut : `&raw const num` crée un pointeur brut immuable `*const i32` et `&raw mut num` crée un pointeur brut mutable `*mut i32`. Comme nous les avons créés directement à partir d'une variable locale, nous savons que ces pointeurs bruts en particulier sont valides, mais nous ne pouvons pas faire cette hypothèse à propos de n'importe quel pointeur brut.

Pour démontrer cela, nous allons maintenant créer un pointeur brut dont la validité n'est pas aussi certaine, en utilisant le mot-clé `as` pour caster une valeur au lieu d'utiliser l'opérateur d'emprunt brut. L'énumération 20-2 montre comment créer un pointeur brut vers un emplacement arbitraire en mémoire. Essayer d'utiliser une mémoire arbitraire est indéfini : il pourrait y avoir des données à cette adresse ou il pourrait ne pas y en avoir, le compilateur pourrait optimiser le code de sorte qu'il n'y ait pas d'accès à la mémoire, ou le programme pourrait se terminer avec une faute de segmentation. En général, il n'y a pas de bonne raison d'écrire du code comme cela, surtout dans les cas où vous pouvez utiliser un opérateur d'emprunt brut à la place, mais c'est possible.

<Énumération numéro="20-2" légende="Création d'un pointeur brut vers une adresse mémoire arbitraire">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-02/src/main.rs:here}}
```

</Énumération>

Rappelez-vous que nous pouvons créer des pointeurs bruts dans un code sûr, mais nous ne pouvons pas déréférencer des pointeurs bruts et lire les données auxquelles ils pointent. Dans l'énumération 20-3, nous utilisons l'opérateur de déréférencement `*` sur un pointeur brut qui nécessite un bloc `unsafe`.

<Énumération numéro="20-3" légende="Déréférencement de pointeurs bruts au sein d'un bloc `unsafe`">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-03/src/main.rs:here}}
```

</Énumération>

Créer un pointeur ne fait pas de mal ; c'est seulement lorsque nous essayons d'accéder à la valeur à laquelle il pointe que nous pourrions nous retrouver à traiter une valeur invalide.

Notez également que dans les énumérations 20-1 et 20-3, nous avons créé des pointeurs bruts `*const i32` et `*mut i32` qui pointent tous deux vers le même emplacement mémoire, où `num` est stocké. Si nous essayions de créer une référence immuable et une référence mutable vers `num`, le code ne se compilerait pas parce que les règles de propriété de Rust n'autorisent pas une référence mutable en même temps que des références immuables. Avec des pointeurs bruts, nous pouvons créer un pointeur mutable et un pointeur immuable vers le même emplacement et modifier les données via le pointeur mutable, ce qui peut potentiellement créer une course de données. Soyez prudent !

Avec tous ces dangers, pourquoi voudriez-vous utiliser des pointeurs bruts ? Un cas d'utilisation majeur est lors de l'interfaçage avec du code C, comme vous le verrez dans la section suivante. Un autre cas est lorsque vous construisez des abstractions sûres que le vérificateur d'emprunt ne comprend pas. Nous allons introduire des fonctions non sécurisées, puis examiner un exemple d'une abstraction sûre qui utilise du code non sécurisé.

### Appeler une Fonction ou une Méthode Non Sécurisée

Le deuxième type d'opération que vous pouvez effectuer dans un bloc non sécurisé est d'appeler des fonctions non sécurisées. Les fonctions et méthodes non sécurisées ressemblent exactement à des fonctions et méthodes régulières, mais elles ont un `unsafe` supplémentaire avant le reste de la définition. Le mot-clé `unsafe` dans ce contexte indique que la fonction a des exigences que nous devons respecter lorsque nous appelons cette fonction, car Rust ne peut pas garantir que nous avons respecté ces exigences. En appelant une fonction non sécurisée à l'intérieur d'un bloc `unsafe`, nous affirmons que nous avons lu la documentation de cette fonction et que nous prenons la responsabilité de respecter les contrats de la fonction.

Voici une fonction non sécurisée nommée `dangerous` qui ne fait rien dans son corps :

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-01-unsafe-fn/src/main.rs:here}}
```

Nous devons appeler la fonction `dangerous` dans un bloc `unsafe` séparé. Si nous essayons d'appeler `dangerous` sans le bloc `unsafe`, nous obtiendrons une erreur :

```console
{{#include ../listings/ch20-advanced-features/output-only-01-missing-unsafe/output.txt}}
```

Avec le bloc `unsafe`, nous affirmons à Rust que nous avons lu la documentation de la fonction, que nous comprenons comment l'utiliser correctement et que nous avons vérifié que nous remplissons le contrat de la fonction.

Pour effectuer des opérations non sécurisées dans le corps d'une fonction `unsafe`, vous devez encore utiliser un bloc `unsafe`, tout comme dans une fonction régulière, et le compilateur vous avertira si vous oubliez. Cela nous aide à garder les blocs `unsafe` aussi petits que possible, car les opérations non sécurisées peuvent ne pas être nécessaires dans tout le corps de la fonction.

#### Créer une Abstraction Sûre au-dessus du Code Non Sécurisé

Ce n'est pas parce qu'une fonction contient du code non sécurisé que nous devons marquer toute la fonction comme non sécurisée. En fait, envelopper du code non sécurisé dans une fonction sûre est une abstraction courante. Par exemple, étudions la fonction `split_at_mut` de la bibliothèque standard, qui nécessite du code non sécurisé. Nous explorerons comment nous pourrions l'implémenter. Cette méthode sûre est définie sur des tranches mutables : elle prend une tranche et la divise en deux en la scindant à l'index donné comme argument. L'énumération 20-4 montre comment utiliser `split_at_mut`.

<Énumération numéro="20-4" légende="Utilisation de la fonction sûre `split_at_mut`">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-04/src/main.rs:here}}
```

</Énumération>

Nous ne pouvons pas implémenter cette fonction uniquement avec du Rust sûr. Une tentative pourrait ressembler à quelque chose comme l'énumération 20-5, qui ne se compilera pas. Pour simplifier, nous allons implémenter `split_at_mut` en tant que fonction plutôt qu'en tant que méthode et uniquement pour des tranches de valeurs `i32` plutôt que pour un type générique `T`.

<Énumération numéro="20-5" légende="Une tentative d'implémentation de `split_at_mut` en utilisant uniquement du Rust sûr">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-05/src/main.rs:here}}
```

</Énumération>

Cette fonction obtient d'abord la longueur totale de la tranche. Ensuite, elle vérifie que l'index donné en tant que paramètre se trouve dans la tranche en vérifiant s'il est inférieur ou égal à la longueur. L'affirmation signifie que si nous passons un index qui est supérieur à la longueur pour diviser la tranche, la fonction paniquera avant d'essayer d'utiliser cet index.

Ensuite, nous retournons deux tranches mutables dans un tuple : une de commencer de la tranche d'origine jusqu'à l'index `mid` et une autre de `mid` jusqu'à la fin de la tranche.

Lorsque nous essayons de compiler le code de l'énumération 20-5, nous obtiendrons une erreur :

```console
{{#include ../listings/ch20-advanced-features/listing-20-05/output.txt}}
```

Le vérificateur d'emprunt de Rust ne peut pas comprendre que nous empruntons différentes parties de la tranche ; il sait seulement que nous empruntons la même tranche deux fois. Emprunter différentes parties d'une tranche est fondamentalement acceptable car les deux tranches ne se chevauchent pas, mais Rust n'est pas assez intelligent pour le savoir. Lorsque nous savons que le code est correct, mais que Rust ne le sait pas, il est temps d'utiliser du code non sécurisé.

L'énumération 20-6 montre comment utiliser un bloc `unsafe`, un pointeur brut et quelques appels à des fonctions non sécurisées pour rendre l'implémentation de `split_at_mut` fonctionnelle.

<Énumération numéro="20-6" légende="Utilisation de code non sécurisé dans l'implémentation de la fonction `split_at_mut`">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-06/src/main.rs:here}}
```

</Énumération>

Rappelez-vous de la section [« Le Type de Tranche »][the-slice-type] dans le Chapitre 4 que une tranche est un pointeur vers certaines données et la longueur de la tranche. Nous utilisons la méthode `len` pour obtenir la longueur d'une tranche et la méthode `as_mut_ptr` pour accéder au pointeur brut d'une tranche. Dans ce cas, parce que nous avons une tranche mutable vers des valeurs `i32`, `as_mut_ptr` renvoie un pointeur brut de type `*mut i32`, que nous avons stocké dans la variable `ptr`.

Nous maintenons l'affirmation que l'index `mid` est dans la tranche. Ensuite, nous passons au code non sécurisé : la fonction `slice::from_raw_parts_mut` prend un pointeur brut et une longueur, et elle crée une tranche. Nous utilisons cette fonction pour créer une tranche qui commence à partir de `ptr` et a une longueur de `mid` éléments. Ensuite, nous appelons la méthode `add` sur `ptr` avec `mid` comme argument pour obtenir un pointeur brut qui commence à `mid`, et nous créons une tranche utilisant ce pointeur et le nombre restant d'éléments après `mid` comme longueur.

La fonction `slice::from_raw_parts_mut` est non sécurisée car elle prend un pointeur brut et doit se fier à ce que ce pointeur est valide. La méthode `add` sur les pointeurs bruts est également non sécurisée car elle doit se fier à ce que l'emplacement décalé est également un pointeur valide. Par conséquent, nous devions mettre un bloc `unsafe` autour de nos appels à `slice::from_raw_parts_mut` et `add` afin de pouvoir les appeler. En regardant le code et en ajoutant l'affirmation que `mid` doit être inférieur ou égal à `len`, nous pouvons dire que tous les pointeurs bruts utilisés dans le bloc `unsafe` seront des pointeurs valides vers des données dans la tranche. C'est une utilisation acceptable et appropriée de `unsafe`.

Notez que nous n'avons pas besoin de marquer la fonction résultante `split_at_mut` comme `unsafe`, et nous pouvons appeler cette fonction à partir de Rust sûr. Nous avons créé une abstraction sûre pour le code non sécurisé avec une implémentation de la fonction qui utilise le code `unsafe` de manière sûre, car elle ne crée que des pointeurs valides à partir des données dont cette fonction a accès.

En revanche, l'utilisation de `slice::from_raw_parts_mut` dans l'énumération 20-7 provoquerait probablement un plantage lorsque la tranche est utilisée. Ce code prend un emplacement mémoire arbitraire et crée une tranche de 10 000 éléments de long.

<Énumération numéro="20-7" légende="Création d'une tranche à partir d'un emplacement mémoire arbitraire">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-07/src/main.rs:here}}
```

</Énumération>

Nous ne possédons pas la mémoire à cet emplacement arbitraire, et il n'y a aucune garantie que la tranche créée par ce code contient des valeurs `i32` valides. Essayer d'utiliser `values` comme s'il s'agissait d'une tranche valide entraîne un comportement indéfini.

#### Utiliser des Fonctions `extern` pour Appeler du Code Externe

Parfois, votre code Rust pourrait avoir besoin d'interagir avec du code écrit dans une autre langue. Pour cela, Rust a le mot-clé `extern` qui facilite la création et l'utilisation d'une _Interface de Fonction Étrangère (FFI)_, qui est un moyen pour un langage de programmation de définir des fonctions et de permettre à un autre (étranger) langage de programmation d'appeler ces fonctions.

L'énumération 20-8 démontre comment configurer une intégration avec la fonction `abs` de la bibliothèque standard C. Les fonctions déclarées dans des blocs `extern` sont généralement non sécurisées à appeler depuis le code Rust, donc les blocs `extern` doivent également être marqués `unsafe`. La raison en est que les autres langues n'appliquent pas les règles et garanties de Rust, et Rust ne peut pas les vérifier, donc la responsabilité incombe au programmeur de garantir la sécurité.

<Énumération numéro="20-8" file-name="src/main.rs" légende="Déclaration et appel d'une fonction `extern` définie dans une autre langue">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-08/src/main.rs}}
```

</Énumération>

Dans le bloc `unsafe extern "C"`, nous répertorions les noms et signatures des fonctions externes d'une autre langue que nous voulons appeler. La partie `"C"` définit quel _interface binaire d'application (ABI)_ la fonction externe utilise : l'ABI définit comment appeler la fonction au niveau de l'assemblage. L'ABI `"C"` est la plus commune et suit l'ABI du langage de programmation C. Les informations sur tous les ABIs que Rust prend en charge sont disponibles dans [la Référence Rust][ABI].

Chaque élément déclaré dans un bloc `unsafe extern` est implicitement non sécurisé. Cependant, certaines fonctions FFI *sont* sûres à appeler. Par exemple, la fonction `abs` de la bibliothèque standard C n'a pas de considérations de sécurité de la mémoire, et nous savons qu'elle peut être appelée avec n'importe quel `i32`. Dans des cas comme celui-ci, nous pouvons utiliser le mot-clé `safe` pour dire que cette fonction spécifique est sûre à appeler, même si elle se trouve dans un bloc `unsafe extern`. Une fois que nous faisons ce changement, l'appel n'exige plus de bloc `unsafe`, comme le montre l'énumération 20-9.

<Énumération numéro="20-9" file-name="src/main.rs" légende="Marquer explicitement une fonction comme `safe` dans un bloc `unsafe extern` et l'appeler en toute sécurité">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-09/src/main.rs}}
```

</Énumération>

Marquer une fonction comme `safe` ne la rend pas intrinsèquement sûre ! Au lieu de cela, c'est comme une promesse que vous faites à Rust qu'elle est sûre. Il est toujours de votre responsabilité de vous assurer que cette promesse est respectée !

#### Appeler des Fonctions Rust depuis d'Autres Langues

Nous pouvons également utiliser `extern` pour créer une interface qui permet à d'autres langues d'appeler des fonctions Rust. Au lieu de créer tout un bloc `extern`, nous ajoutons le mot-clé `extern` et spécifions l'ABI à utiliser juste avant le mot-clé `fn` pour la fonction concernée. Nous devons également ajouter une annotation `#[unsafe(no_mangle)]` pour dire au compilateur Rust de ne pas altérer le nom de cette fonction. _L'altération_ est lorsque le compilateur change le nom que nous avons donné à une fonction en un nom différent qui contient plus d'informations pour que d'autres parties du processus de compilation puissent le consommer mais qui est moins lisible pour les humains. Chaque compilateur de langage de programmation altère légèrement les noms, donc pour qu'une fonction Rust soit nommable par d'autres langages, nous devons désactiver l'altération des noms du compilateur Rust. Cela est dangereux car il pourrait y avoir des collisions de noms entre bibliothèques sans l'altération incorporée, donc il est de notre responsabilité de nous assurer que le nom que nous choisissons est sans danger à exporter sans altération.

Dans l'exemple suivant, nous rendons la fonction `call_from_c` accessible depuis le code C, après qu'elle a été compilée en une bibliothèque partagée et liée depuis C :

```
#[unsafe(no_mangle)]
pub extern "C" fn call_from_c() {
    println!("Just called a Rust function from C!");
}
```

Cet usage de `extern` nécessite `unsafe` seulement dans l'attribut, pas sur le bloc `extern`.

### Accéder ou Modifier une Variable Statique Mutable

Dans ce livre, nous n'avons pas encore parlé des variables globales, que Rust prend en charge mais qui peuvent poser des problèmes avec les règles de propriété de Rust. Si deux threads accèdent à la même variable globale mutable, cela peut provoquer une course de données.

En Rust, les variables globales sont appelées des variables _statiques_. L'énumération 20-10 montre un exemple de déclaration et d'utilisation d'une variable statique avec une tranche de chaîne comme valeur.

<Énumération numéro="20-10" file-name="src/main.rs" légende="Définir et utiliser une variable statique immuable">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-10/src/main.rs}}
```

</Énumération>

Les variables statiques sont similaires aux constantes, que nous avons discutées dans la section [« Déclaration de Constantes »][constants] dans le Chapitre 3. Par convention, les noms des variables statiques sont en `SCREAMING_SNAKE_CASE`. Les variables statiques ne peuvent stocker que des références avec la durée de vie `'static`, ce qui signifie que le compilateur Rust peut déterminer la durée de vie et que nous ne sommes pas tenus de l'annoter explicitement. Accéder à une variable statique immuable est sûr.

Une différence subtile entre les constantes et les variables statiques immuables est que les valeurs dans une variable statique ont une adresse fixe en mémoire. Utiliser la valeur accédera toujours aux mêmes données. Les constantes, en revanche, sont autorisées à dupliquer leurs données chaque fois qu'elles sont utilisées. Une autre différence est que les variables statiques peuvent être mutables. Accéder et modifier des variables statiques mutables est _non sécurisé_. L'énumération 20-11 montre comment déclarer, accéder et modifier une variable statique mutable nommée `COUNTER`.

<Énumération numéro="20-11" file-name="src/main.rs" légende="Lire ou écrire à partir d'une variable statique mutable est non sécurisé.">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-11/src/main.rs}}
```

</Énumération>

Comme avec les variables régulières, nous spécifions la mutabilité en utilisant le mot-clé `mut`. Tout code qui lit ou écrit à partir de `COUNTER` doit être dans un bloc `unsafe`. Le code dans l'énumération 20-11 se compile et imprime `COUNTER: 3` comme nous nous y attendions car il est un seul thread. Avoir plusieurs threads accédant à `COUNTER` entraînerait probablement des courses de données, donc c'est un comportement indéfini. Par conséquent, nous devons marquer toute la fonction comme `unsafe` et documenter la limitation de sécurité afin que quiconque appelant la fonction sache ce qu'il est et n'est pas autorisé à faire en toute sécurité.

Chaque fois que nous écrivons une fonction non sécurisée, il est idiomatique d'écrire un commentaire commençant par `SAFETY` et expliquant ce que l'appelant doit faire pour appeler la fonction en toute sécurité. De même, chaque fois que nous effectuons une opération non sécurisée, il est idiomatique d'écrire un commentaire commençant par `SAFETY` pour expliquer comment les règles de sécurité sont respectées.

De plus, le compilateur refusera par défaut toute tentative de créer des références à une variable statique mutable via un linter de compilateur. Vous devez soit explicitement vous soustraire aux protections de ce linter en ajoutant une annotation `#[allow(static_mut_refs)]`, soit accéder à la variable statique mutable via un pointeur brut créé avec l'un des opérateurs d'emprunt brut. Cela inclut les cas où la référence est créée de manière invisible, comme lorsqu'elle est utilisée dans le `println!` de ce listing. Exiger que les références aux variables mutables statiques soient créées via des pointeurs bruts aide à rendre les exigences de sécurité pour leur utilisation plus évidentes.

Avec des données mutables qui sont accessibles globalement, il est difficile de garantir qu'il n'y a pas de courses de données, c'est pourquoi Rust considère les variables statiques mutables comme non sécurisées. Où cela est possible, il est préférable d'utiliser les techniques de concurrence et les pointeurs intelligents sûrs pour les threads dont nous avons discuté dans le Chapitre 16 afin que le compilateur vérifie que l'accès aux données par différents threads est effectué en toute sécurité.

### Mettre en œuvre un Trait Non Sécurisé

Nous pouvons utiliser `unsafe` pour implémenter un trait non sécurisé. Un trait est non sécurisé lorsque au moins une de ses méthodes a des invariants que le compilateur ne peut pas vérifier. Nous déclarons qu'un trait est `unsafe` en ajoutant le mot-clé `unsafe` avant `trait` et en marquant l'implémentation du trait comme `unsafe` également, comme le montre l'énumération 20-12.

<Énumération numéro="20-12" légende="Définir et implémenter un trait non sécurisé">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-12/src/main.rs:here}}
```

</Énumération>

En utilisant `unsafe impl`, nous promettons que nous respecterons les invariants que le compilateur ne peut pas vérifier.

Par exemple, rappelez-vous des traits de marque `Send` et `Sync` dont nous avons discuté dans la section [« Concurrence Extensible avec `Send` et `Sync` »][send-and-sync] dans le Chapitre 16 : Le compilateur implémente automatiquement ces traits si nos types sont composés entièrement d'autres types qui implémentent `Send` et `Sync`. Si nous implémentons un type qui contient un type qui n'implémente pas `Send` ou `Sync`, comme des pointeurs bruts, et que nous voulons marquer ce type comme `Send` ou `Sync`, nous devons utiliser `unsafe`. Rust ne peut pas vérifier que notre type respecte les garanties qu'il peut être envoyé en toute sécurité à travers les threads ou accédé par plusieurs threads ; par conséquent, nous devons effectuer ces vérifications manuellement et indiquer cela avec `unsafe`.

### Accéder aux Champs d'une Union

L'action finale qui ne fonctionne qu'avec `unsafe` est l'accès aux champs d'une union. Une *union* est similaire à une `structure`, mais seul un champ déclaré est utilisé dans une instance particulière à un moment donné. Les unions sont principalement utilisées pour interfacer avec des unions dans du code C. Accéder aux champs d'une union est non sécurisé car Rust ne peut garantir le type des données actuellement stockées dans l'instance de l'union. Vous pouvez en apprendre plus sur les unions dans [la Référence Rust][unions].

### Utiliser Miri pour Vérifier le Code Non Sécurisé

Lorsque vous écrivez du code non sécurisé, vous pouvez vouloir vérifier que ce que vous avez écrit est réellement sûr et correct. L'un des meilleurs moyens de le faire est d'utiliser Miri, un outil officiel Rust pour détecter les comportements indéfinis. Alors que le vérificateur d'emprunt est un outil _statique_ qui fonctionne à la compilation, Miri est un outil _dynamique_ qui fonctionne à l'exécution. Il vérifie votre code en exécutant votre programme, ou sa suite de tests, et en détectant lorsque vous enfreignez les règles qu'il comprend sur le fonctionnement de Rust.

Utiliser Miri nécessite une version nightly de Rust (dont nous parlons davantage dans [l'Annexe G : Comment Rust est Fabriqué et « Rust Nightly »][nightly]). Vous pouvez installer à la fois une version nightly de Rust et l'outil Miri en tapant `rustup +nightly component add miri`. Cela ne change pas la version de Rust que votre projet utilise ; cela ajoute seulement l'outil à votre système pour que vous puissiez l'utiliser lorsque vous le souhaitez. Vous pouvez exécuter Miri sur un projet en tapant `cargo +nightly miri run` ou `cargo +nightly miri test`.

Pour un exemple de la manière dont cela peut être utile, considérez ce qui se passe lorsque nous l'exécutons contre l'énumération 20-7.

```console
{{#include ../listings/ch20-advanced-features/listing-20-07/output.txt}}
```

Miri nous avertit correctement que nous castons un entier en un pointeur, ce qui pourrait être un problème, mais Miri ne peut pas déterminer si un problème existe car il ne sait pas comment le pointeur a été créé. Ensuite, Miri renvoie une erreur où l'énumération 20-7 a un comportement indéfini parce que nous avons un pointeur inutilisable. Grâce à Miri, nous savons maintenant qu'il existe un risque de comportement indéfini, et nous pouvons réfléchir à comment rendre le code sûr. Dans certains cas, Miri peut même faire des recommandations sur la manière de corriger les erreurs.

Miri ne détecte pas tout ce que vous pourriez mal faire en écrivant du code non sécurisé. Miri est un outil d'analyse dynamique, donc il ne détecte que les problèmes avec le code qui est effectivement exécuté. Cela signifie que vous devrez l'utiliser en conjonction avec de bonnes techniques de test pour augmenter votre confiance dans le code non sécurisé que vous avez écrit. Miri ne couvre également pas toutes les façons possibles dont votre code peut être peu sûr.

En d'autres termes : si Miri _repère_ un problème, vous savez qu'il y a un bug, mais juste parce que Miri _ne détecte pas_ un bug ne signifie pas qu'il n'y a pas de problème. Cela peut détecter beaucoup de choses, cependant. Essayez de l'exécuter sur les autres exemples de code non sécurisé dans ce chapitre et voyez ce qu'il en dit !

Vous pouvez en apprendre plus sur Miri dans [son dépôt GitHub][miri].

<a id="when-to-use-unsafe-code"></a>

### Utiliser le Code Non Sécurisé Correctement

Utiliser `unsafe` pour exercer l'un des cinq superpouvoirs discutés précédemment n'est ni mal ni même mal vu, mais il est plus délicat d'obtenir un code `unsafe` correct car le compilateur ne peut pas aider à maintenir la sécurité de la mémoire. Lorsque vous avez des raisons d'utiliser du code `unsafe`, vous pouvez le faire, et avoir l'annotation explicite `unsafe` facilite le suivi de la source des problèmes lorsqu'ils surviennent. Chaque fois que vous écrivez du code non sécurisé, vous pouvez utiliser Miri pour vous aider à être plus confiant que le code que vous avez écrit respecte les règles de Rust.

Pour une exploration beaucoup plus approfondie de la manière de travailler efficacement avec Rust non sécurisé, lisez le guide officiel de Rust pour `unsafe`, [The Rustonomicon][nomicon].

[dangling-references]: ch04-02-references-and-borrowing.html#dangling-references
[ABI]: ../reference/items/external-blocks.html#abi
[constants]: ch03-01-variables-and-mutability.html#declaring-constants
[send-and-sync]: ch16-04-extensible-concurrency-sync-and-send.html
[the-slice-type]: ch04-03-slices.html#the-slice-type
[unions]: ../reference/items/unions.html
[miri]: https://github.com/rust-lang/miri
[editions]: appendix-05-editions.html
[nightly]: appendix-07-nightly-rust.html
[nomicon]: https://doc.rust-lang.org/nomicon/