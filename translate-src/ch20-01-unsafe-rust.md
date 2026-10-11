## Rust non sûr

Tout le code dont nous avons parlé jusqu’ici bénéficiait des garanties de sécurité mémoire de Rust, appliquées à la compilation. Cependant, Rust contient un second langage caché qui n’applique pas ces garanties : il s’appelle _Rust non sûr_ et fonctionne comme Rust ordinaire, mais nous confère des superpouvoirs supplémentaires.

Rust non sûr existe parce que, par nature, l’analyse statique est prudente. Lorsque le compilateur essaie de déterminer si le code respecte les garanties, il vaut mieux qu’il rejette certains programmes valides plutôt qu’il accepte des programmes invalides. Même si le code _pourrait_ être correct, si le compilateur Rust ne dispose pas de suffisamment d’informations pour en être certain, il le rejettera. Dans ces cas, vous pouvez utiliser du code non sûr pour dire au compilateur : « Faites-moi confiance, je sais ce que je fais. » Attention toutefois : vous utilisez Rust non sûr à vos propres risques. Si vous utilisez le code non sûr de manière incorrecte, des problèmes liés à l’insécurité mémoire peuvent survenir, comme le déréférencement d’un pointeur nul.

Une autre raison pour laquelle Rust a un alter ego non sûr est que le matériel informatique sous-jacent est intrinsèquement non sûr. Si Rust ne vous permettait pas d’effectuer des opérations non sûres, vous ne pourriez pas accomplir certaines tâches. Rust doit permettre la programmation système de bas niveau, par exemple l’interaction directe avec le système d’exploitation, voire l’écriture de votre propre système d’exploitation. La programmation système de bas niveau est l’un des objectifs du langage. Voyons ce que nous pouvons faire avec Rust non sûr et comment procéder.

<!-- Old headings. Do not remove or links may break. -->

<a id="unsafe-superpowers"></a>

### Utiliser les superpouvoirs du code non sûr

Pour passer à Rust non sûr, utilisez le mot-clé `unsafe`, puis ouvrez un nouveau bloc qui contiendra le code non sûr. Rust non sûr vous permet d’effectuer cinq actions impossibles en Rust sûr ; nous les appelons les _superpouvoirs du code non sûr_. Ces superpouvoirs incluent la possibilité de :

1. Déréférencer un pointeur brut.
1. Appeler une fonction ou une méthode non sûre.
1. Accéder à une variable statique mutable ou la modifier.
1. Implémenter un trait non sûr.
1. Accéder aux champs des `union`s.

Il est important de comprendre que `unsafe` ne désactive pas le vérificateur d’emprunts ni aucun des autres contrôles de sécurité de Rust : si vous utilisez une référence dans du code non sûr, elle sera tout de même vérifiée. Le mot-clé `unsafe` vous donne uniquement accès à ces cinq fonctionnalités, qui ne sont alors pas contrôlées par le compilateur du point de vue de la sécurité mémoire. Vous bénéficiez tout de même d’un certain degré de sécurité à l’intérieur d’un bloc non sûr.

De plus, `unsafe` ne signifie pas que le code du bloc est nécessairement dangereux ou qu’il entraînera forcément des problèmes de sécurité mémoire : l’intention est que, en tant que programmeur, vous vous assuriez que le code d’un bloc `unsafe` accède à la mémoire de manière valide.

Les humains sont faillibles et des erreurs se produiront, mais en exigeant que ces cinq opérations non sûres se trouvent dans des blocs annotés avec `unsafe`, vous saurez que toute erreur liée à la sécurité mémoire se trouve nécessairement dans un bloc `unsafe`. Gardez les blocs `unsafe` aussi petits que possible ; vous vous en féliciterez plus tard lorsque vous chercherez l’origine de bogues mémoire.

Pour isoler autant que possible le code non sûr, il est préférable de l’encapsuler dans une abstraction sûre et de fournir une API sûre. Nous en parlerons plus loin dans ce chapitre, lorsque nous examinerons les fonctions et les méthodes non sûres. Certaines parties de la bibliothèque standard sont implémentées sous forme d’abstractions sûres reposant sur du code non sûr qui a été audité. L’encapsulation du code non sûr dans une abstraction sûre empêche l’utilisation de `unsafe` de se propager à tous les endroits où vous ou vos utilisateurs pourriez vouloir utiliser les fonctionnalités implémentées avec du code `unsafe`, puisque l’utilisation d’une abstraction sûre est sûre.

Examinons tour à tour chacun des cinq superpouvoirs du code non sûr. Nous verrons également quelques abstractions qui fournissent une interface sûre au code non sûr.

### Déréférencer un pointeur brut

Au chapitre 4, dans la section [« Références pendantes »][dangling-references]<!-- ignore
-->, nous avons mentionné que le compilateur garantit que les références sont toujours valides. Rust non sûr introduit deux nouveaux types appelés _pointeurs bruts_, qui ressemblent aux références. Comme les références, les pointeurs bruts peuvent être immuables ou mutables et s’écrivent respectivement `*const T` et `*mut T`. L’astérisque n’est pas l’opérateur de déréférencement ; il fait partie du nom du type. Dans le contexte des pointeurs bruts, _immuable_ signifie que le pointeur ne peut pas être directement réaffecté après avoir été déréférencé.

Contrairement aux références et aux pointeurs intelligents, les pointeurs bruts :

- Peuvent ignorer les règles d’emprunt en ayant à la fois des pointeurs immuables et mutables, ou plusieurs pointeurs mutables vers le même emplacement
- Ne sont pas garantis de pointer vers une mémoire valide
- Peuvent être nuls
- N’implémentent aucun nettoyage automatique

En choisissant de ne pas demander à Rust d’appliquer ces garanties, vous pouvez renoncer à une sécurité garantie en échange de meilleures performances ou de la possibilité d’interagir avec un autre langage ou avec du matériel auquel les garanties de Rust ne s’appliquent pas.

La liste 20-1 montre comment créer un pointeur brut immuable et un pointeur brut mutable.

<Listing number="20-1" caption="Création de pointeurs bruts avec les opérateurs d’emprunt brut">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-01/src/main.rs:here}}
```

</Listing>

Remarquez que nous n’incluons pas le mot-clé `unsafe` dans ce code. Nous pouvons créer des pointeurs bruts dans du code sûr ; nous ne pouvons simplement pas les déréférencer en dehors d’un bloc non sûr, comme vous le verrez dans un instant.

Nous avons créé des pointeurs bruts à l’aide des opérateurs d’emprunt brut : `&raw const num` crée un pointeur brut immuable `*const i32`, et `&raw mut num` crée un pointeur brut mutable `*mut i32`. Puisque nous les avons créés directement à partir d’une variable locale, nous savons que ces pointeurs bruts particuliers sont valides, mais nous ne pouvons pas faire cette supposition pour n’importe quel pointeur brut.

Pour le montrer, nous allons ensuite créer un pointeur brut dont la validité est moins certaine, en utilisant le mot-clé `as` pour convertir une valeur plutôt que l’opérateur d’emprunt brut. La liste 20-2 montre comment créer un pointeur brut vers un emplacement arbitraire de la mémoire. Tenter d’utiliser une adresse mémoire arbitraire a un comportement indéfini : il peut y avoir des données à cette adresse ou non, le compilateur peut optimiser le code de sorte qu’aucun accès mémoire n’ait lieu, ou le programme peut s’arrêter à la suite d’une erreur de segmentation. En général, il n’y a aucune bonne raison d’écrire du code comme celui-ci, surtout lorsqu’on peut utiliser à la place un opérateur d’emprunt brut, mais cela reste possible.

<Listing number="20-2" caption="Création d’un pointeur brut vers une adresse mémoire arbitraire">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-02/src/main.rs:here}}
```

</Listing>

Rappelez-vous que nous pouvons créer des pointeurs bruts dans du code sûr, mais que nous ne pouvons pas les déréférencer ni lire les données vers lesquelles ils pointent. Dans la liste 20-3, nous utilisons l’opérateur de déréférencement `*` sur un pointeur brut, ce qui nécessite un bloc `unsafe`.

<Listing number="20-3" caption="Déréférencement de pointeurs bruts dans un bloc `unsafe`">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-03/src/main.rs:here}}
```

</Listing>

Créer un pointeur ne fait aucun mal ; c’est seulement lorsque nous essayons d’accéder à la valeur vers laquelle il pointe que nous risquons de manipuler une valeur invalide.

Notez également que, dans les listes 20-1 et 20-3, nous avons créé des pointeurs bruts `*const i32` et `*mut i32` qui pointaient tous deux vers le même emplacement mémoire, là où `num` est stockée. Si nous avions essayé de créer une référence immuable et une référence mutable vers `num`, le code n’aurait pas compilé, car les règles de propriété de Rust n’autorisent pas une référence mutable en même temps que des références immuables. Avec les pointeurs bruts, nous pouvons créer un pointeur mutable et un pointeur immuable vers le même emplacement, puis modifier les données par l’intermédiaire du pointeur mutable, ce qui peut créer une course de données. Soyez prudent !

Compte tenu de tous ces dangers, pourquoi utiliser des pointeurs bruts ? L’un de leurs principaux cas d’utilisation est l’interaction avec du code C, comme vous le verrez dans la section suivante. Ils sont également utiles pour créer des abstractions sûres que le vérificateur d’emprunts ne comprend pas. Nous allons présenter les fonctions non sûres, puis examiner un exemple d’abstraction sûre qui utilise du code non sûr.

### Appeler une fonction ou une méthode non sûre

Le deuxième type d’opération que vous pouvez effectuer dans un bloc non sûr consiste à appeler des fonctions non sûres. Les fonctions et méthodes non sûres ressemblent exactement aux fonctions et méthodes ordinaires, mais elles comportent le mot-clé `unsafe` avant le reste de leur définition. Dans ce contexte, le mot-clé `unsafe` indique que la fonction impose des exigences que nous devons respecter lorsque nous l’appelons, car Rust ne peut pas garantir que nous les avons satisfaites. En appelant une fonction non sûre dans un bloc `unsafe`, nous indiquons que nous avons lu sa documentation et que nous prenons la responsabilité de respecter son contrat.

Voici une fonction non sûre nommée `dangerous` dont le corps ne fait rien :

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-01-unsafe-fn/src/main.rs:here}}
```

Nous devons appeler la fonction `dangerous` dans un bloc `unsafe` distinct. Si nous essayons d’appeler `dangerous` sans le bloc `unsafe`, nous obtenons une erreur :

```console
{{#include ../listings/ch20-advanced-features/output-only-01-missing-unsafe/output.txt}}
```

Avec le bloc `unsafe`, nous affirmons à Rust que nous avons lu la documentation de la fonction, que nous comprenons comment l’utiliser correctement et que nous avons vérifié que nous respectons son contrat.

Pour effectuer des opérations non sûres dans le corps d’une fonction non sûre, vous devez tout de même utiliser un bloc `unsafe`, comme dans une fonction ordinaire ; le compilateur vous avertira si vous l’oubliez. Cela nous aide à garder les blocs `unsafe` aussi petits que possible, car les opérations non sûres ne sont pas forcément nécessaires dans l’ensemble du corps de la fonction.

#### Créer une abstraction sûre à partir de code non sûr

Le fait qu’une fonction contienne du code non sûr ne signifie pas que nous devons marquer la fonction entière comme non sûre. En fait, encapsuler du code non sûr dans une fonction sûre est une abstraction courante. À titre d’exemple, étudions la fonction `split_at_mut` de la bibliothèque standard, qui nécessite du code non sûr. Nous allons voir comment nous pourrions l’implémenter. Cette méthode sûre est définie sur des tranches mutables : elle prend une tranche et la divise en deux à l’indice fourni en argument. La liste 20-4 montre comment utiliser `split_at_mut`.

<Listing number="20-4" caption="Utilisation de la fonction sûre `split_at_mut`">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-04/src/main.rs:here}}
```

</Listing>

Nous ne pouvons pas implémenter cette fonction en utilisant uniquement Rust sûr. Une tentative pourrait ressembler à la liste 20-5, mais elle ne compilera pas. Pour simplifier, nous allons implémenter `split_at_mut` sous forme de fonction plutôt que de méthode, et uniquement pour les tranches de valeurs `i32` plutôt que pour un type générique `T`.

<Listing number="20-5" caption="Tentative d’implémentation de `split_at_mut` en utilisant uniquement Rust sûr">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-05/src/main.rs:here}}
```

</Listing>

Cette fonction récupère d’abord la longueur totale de la tranche. Ensuite, elle vérifie que l’indice fourni en paramètre se trouve dans la tranche, en vérifiant qu’il est inférieur ou égal à la longueur. Cette assertion signifie que si nous fournissons un indice supérieur à la longueur pour diviser la tranche, la fonction paniquera avant d’essayer d’utiliser cet indice.

Ensuite, nous renvoyons deux tranches mutables dans un tuple : l’une va du début de la tranche d’origine jusqu’à l’indice `mid`, et l’autre va de `mid` jusqu’à la fin de la tranche.

Lorsque nous essayons de compiler le code de la liste 20-5, nous obtenons une erreur :

```console
{{#include ../listings/ch20-advanced-features/listing-20-05/output.txt}}
```

Le vérificateur d’emprunts de Rust ne comprend pas que nous empruntons différentes parties de la tranche ; il sait seulement que nous empruntons deux fois la même tranche. Emprunter différentes parties d’une tranche est tout à fait acceptable, car les deux tranches ne se chevauchent pas, mais Rust n’est pas assez intelligent pour le savoir. Lorsque nous savons qu’un code est correct, mais que Rust ne le sait pas, il est temps de recourir au code non sûr.

La liste 20-6 montre comment utiliser un bloc `unsafe`, un pointeur brut et quelques appels à des fonctions non sûres pour faire fonctionner l’implémentation de `split_at_mut`.

<Listing number="20-6" caption="Utilisation de code non sûr dans l’implémentation de la fonction `split_at_mut`">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-06/src/main.rs:here}}
```

</Listing>

Rappelez-vous la section [« Le type tranche »][the-slice-type]<!-- ignore --> du chapitre 4 : une tranche est composée d’un pointeur vers des données et de sa longueur. Nous utilisons la méthode `len` pour obtenir la longueur d’une tranche et la méthode `as_mut_ptr` pour accéder au pointeur brut d’une tranche. Dans ce cas, comme nous avons une tranche mutable de valeurs `i32`, `as_mut_ptr` renvoie un pointeur brut de type `*mut i32`, que nous avons stocké dans la variable `ptr`.

Nous conservons l’assertion selon laquelle l’indice `mid` se trouve dans la tranche. Nous arrivons ensuite au code non sûr : la fonction `slice::from_raw_parts_mut` prend un pointeur brut et une longueur, puis crée une tranche. Nous utilisons cette fonction pour créer une tranche qui commence à `ptr` et comporte `mid` éléments. Ensuite, nous appelons la méthode `add` sur `ptr` en lui passant `mid` comme argument pour obtenir un pointeur brut qui commence à `mid`, puis nous créons une tranche à l’aide de ce pointeur et du nombre d’éléments restants après `mid` comme longueur.

La fonction `slice::from_raw_parts_mut` est non sûre, car elle prend un pointeur brut et doit lui faire confiance pour être valide. La méthode `add` des pointeurs bruts est également non sûre, car elle doit faire confiance à la validité du pointeur situé à l’offset obtenu. Nous avons donc dû placer un bloc `unsafe` autour de nos appels à `slice::from_raw_parts_mut` et `add` pour pouvoir les appeler. En examinant le code et en ajoutant l’assertion selon laquelle `mid` doit être inférieur ou égal à `len`, nous pouvons constater que tous les pointeurs bruts utilisés dans le bloc `unsafe` seront des pointeurs valides vers des données de la tranche. Il s’agit d’une utilisation acceptable et appropriée de `unsafe`.

Notez que nous n’avons pas besoin de marquer la fonction `split_at_mut` résultante comme non sûre, et que nous pouvons l’appeler depuis du Rust sûr. Nous avons créé une abstraction sûre autour du code non sûr en implémentant la fonction de façon à utiliser le code `unsafe` sans danger, puisqu’elle ne crée que des pointeurs valides à partir des données auxquelles cette fonction a accès.

En revanche, l’utilisation de `slice::from_raw_parts_mut` dans la liste 20-7 entraînerait probablement un plantage lors de l’utilisation de la tranche. Ce code prend un emplacement mémoire arbitraire et crée une tranche de 10 000 éléments.

<Listing number="20-7" caption="Création d’une tranche à partir d’un emplacement mémoire arbitraire">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-07/src/main.rs:here}}
```

</Listing>

Nous ne possédons pas la mémoire à cet emplacement arbitraire, et rien ne garantit que la tranche créée par ce code contienne des valeurs `i32` valides. Utiliser `values` comme s’il s’agissait d’une tranche valide entraîne un comportement indéfini.

#### Utiliser des fonctions `extern` pour appeler du code externe

Il arrive que votre code Rust doive interagir avec du code écrit dans un autre langage. Pour cela, Rust possède le mot-clé `extern`, qui facilite la création et l’utilisation d’une _interface de fonctions étrangères (FFI)_. Il s’agit d’un moyen pour un langage de programmation de définir des fonctions et de permettre à un autre langage de programmation, dit étranger, de les appeler.

La liste 20-8 montre comment configurer une intégration avec la fonction `abs` de la bibliothèque standard C. Les fonctions déclarées dans des blocs `extern` ne peuvent généralement pas être appelées sans risque depuis du code Rust ; les blocs `extern` doivent donc également être marqués `unsafe`. En effet, les autres langages n’appliquent pas les règles et garanties de Rust, et Rust ne peut pas les vérifier. Il revient donc au programmeur de garantir la sécurité.

<Listing number="20-8" file-name="src/main.rs" caption="Déclaration et appel d’une fonction `extern` définie dans un autre langage">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-08/src/main.rs}}
```

</Listing>

Dans le bloc `unsafe extern "C"`, nous indiquons les noms et les signatures des fonctions externes d’un autre langage que nous voulons appeler. La partie `"C"` définit l’_interface binaire d’application (ABI)_ utilisée par la fonction externe : l’ABI définit comment appeler la fonction au niveau de l’assembleur. L’ABI `"C"` est la plus courante et suit celle du langage de programmation C. Vous trouverez des informations sur toutes les ABI prises en charge par Rust dans [la référence Rust][ABI].

Chaque élément déclaré dans un bloc `unsafe extern` est implicitement non sûr. Cependant, certaines fonctions FFI *peuvent* être appelées sans risque. Par exemple, la fonction `abs` de la bibliothèque standard C ne présente aucun problème de sécurité mémoire, et nous savons qu’elle peut être appelée avec n’importe quelle valeur `i32`. Dans ce genre de cas, nous pouvons utiliser le mot-clé `safe` pour indiquer que cette fonction en particulier peut être appelée sans risque, même si elle se trouve dans un bloc `unsafe extern`. Une fois cette modification apportée, son appel ne nécessite plus de bloc `unsafe`, comme le montre la liste 20-9.

<Listing number="20-9" file-name="src/main.rs" caption="Marquage explicite d’une fonction comme `safe` dans un bloc `unsafe extern` et appel sûr">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-09/src/main.rs}}
```

</Listing>

Marquer une fonction comme `safe` ne la rend pas intrinsèquement sûre ! C’est plutôt une promesse que vous faites à Rust pour lui garantir qu’elle est sûre. Il vous revient toujours de veiller à tenir cette promesse !

#### Appeler des fonctions Rust depuis d’autres langages

Nous pouvons également utiliser `extern` pour créer une interface qui permet à d’autres langages d’appeler des fonctions Rust. Au lieu de créer un bloc `extern` entier, nous ajoutons le mot-clé `extern` et indiquons l’ABI à utiliser juste avant le mot-clé `fn` de la fonction concernée. Nous devons également ajouter une annotation `#[unsafe(no_mangle)]` pour indiquer au compilateur Rust de ne pas modifier le nom de cette fonction. Le _name mangling_ est une opération par laquelle un compilateur transforme le nom que nous avons donné à une fonction en un autre nom qui contient davantage d’informations destinées aux autres étapes du processus de compilation, mais qui est moins lisible pour les humains. Chaque compilateur de langage de programmation modifie les noms de manière légèrement différente ; pour qu’une fonction Rust puisse être désignée par d’autres langages, nous devons donc désactiver la modification des noms par le compilateur Rust. Cette opération est non sûre, car des collisions de noms peuvent survenir entre bibliothèques en l’absence de cette modification intégrée. Il nous revient donc de veiller à ce que le nom choisi puisse être exporté sans être modifié.

Dans l’exemple suivant, nous rendons la fonction `call_from_c` accessible depuis du code C, après sa compilation dans une bibliothèque partagée et son édition de liens depuis C :

```
#[unsafe(no_mangle)]
pub extern "C" fn call_from_c() {
    println!("Just called a Rust function from C!");
}
```

Cette utilisation de `extern` ne nécessite `unsafe` que dans l’attribut, et non sur le bloc `extern`.

### Accéder à une variable statique mutable ou la modifier

Dans ce livre, nous n’avons pas encore parlé des variables globales, que Rust prend en charge, mais qui peuvent poser problème avec les règles de propriété de Rust. Si deux threads accèdent à la même variable globale mutable, cela peut entraîner une course de données.

En Rust, les variables globales sont appelées des variables _statiques_. La liste 20-10 montre un exemple de déclaration et d’utilisation d’une variable statique dont la valeur est une tranche de chaîne.

<Listing number="20-10" file-name="src/main.rs" caption="Définition et utilisation d’une variable statique immuable">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-10/src/main.rs}}
```

</Listing>

Les variables statiques ressemblent aux constantes, dont nous avons parlé dans la section [« Déclarer des constantes »][constants]<!-- ignore --> du chapitre 3. Par convention, les noms des variables statiques s’écrivent en `SCREAMING_SNAKE_CASE`. Les variables statiques ne peuvent stocker que des références ayant la durée de vie `'static`, ce qui signifie que le compilateur Rust peut déterminer cette durée de vie et que nous n’avons pas besoin de l’annoter explicitement. Accéder à une variable statique immuable est sûr.

Une différence subtile entre les constantes et les variables statiques immuables est que les valeurs d’une variable statique ont une adresse fixe en mémoire. Utiliser cette valeur donne toujours accès aux mêmes données. En revanche, les constantes peuvent dupliquer leurs données à chaque utilisation. Une autre différence est que les variables statiques peuvent être mutables. Accéder à une variable statique mutable et la modifier est _non sûr_. La liste 20-11 montre comment déclarer, lire et modifier une variable statique mutable nommée `COUNTER`.

<Listing number="20-11" file-name="src/main.rs" caption="Lire ou écrire dans une variable statique mutable est non sûr.">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-11/src/main.rs}}
```

</Listing>

Comme pour les variables ordinaires, nous indiquons la mutabilité à l’aide du mot-clé `mut`. Tout code qui lit ou écrit dans `COUNTER` doit se trouver dans un bloc `unsafe`. Le code de la liste 20-11 compile et affiche `COUNTER: 3`, comme prévu, puisqu’il s’exécute dans un seul thread. Si plusieurs threads accédaient à `COUNTER`, cela entraînerait probablement des courses de données et donc un comportement indéfini. Nous devons donc marquer la fonction entière comme `unsafe` et documenter cette restriction de sécurité afin que toute personne qui l’appelle sache ce qu’elle peut ou ne peut pas faire sans risque.

Lorsque nous écrivons une fonction non sûre, il est idiomatique d’écrire un commentaire commençant par `SAFETY` et expliquant ce que l’appelant doit faire pour appeler la fonction sans risque. De même, lorsque nous effectuons une opération non sûre, il est idiomatique d’écrire un commentaire commençant par `SAFETY` pour expliquer comment les règles de sécurité sont respectées.

De plus, le compilateur refusera par défaut toute tentative de création de références vers une variable statique mutable, au moyen d’un lint du compilateur. Vous devez soit désactiver explicitement cette protection du lint en ajoutant une annotation `#[allow(static_mut_refs)]`, soit accéder à la variable statique mutable par l’intermédiaire d’un pointeur brut créé avec l’un des opérateurs d’emprunt brut. Cela inclut les cas où la référence est créée de manière invisible, comme lorsqu’elle est utilisée dans le `println!` de cet exemple. Exiger que les références vers les variables statiques mutables soient créées via des pointeurs bruts aide à rendre plus évidentes les exigences de sécurité liées à leur utilisation.

Avec des données mutables accessibles globalement, il est difficile de garantir l’absence de courses de données, ce qui explique pourquoi Rust considère que les variables statiques mutables sont non sûres. Lorsque c’est possible, il est préférable d’utiliser les techniques de concurrence et les pointeurs intelligents sûrs vis-à-vis des threads que nous avons présentés au chapitre 16, afin que le compilateur vérifie que l’accès aux données depuis différents threads se fait sans risque.

### Implémenter un trait non sûr

Nous pouvons utiliser `unsafe` pour implémenter un trait non sûr. Un trait est non sûr lorsqu’au moins l’une de ses méthodes possède un invariant que le compilateur ne peut pas vérifier. Nous déclarons qu’un trait est `unsafe` en ajoutant le mot-clé `unsafe` avant `trait` et en marquant également son implémentation comme `unsafe`, comme le montre la liste 20-12.

<Listing number="20-12" caption="Définition et implémentation d’un trait non sûr">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-12/src/main.rs:here}}
```

</Listing>

En utilisant `unsafe impl`, nous promettons de respecter les invariants que le compilateur ne peut pas vérifier.

Par exemple, rappelez-vous les traits marqueurs `Send` et `Sync` dont nous avons parlé dans la section [« Concurrence extensible avec `Send` et `Sync` »][send-and-sync]<!-- ignore --> du chapitre 16 : le compilateur implémente automatiquement ces traits si nos types sont composés uniquement d’autres types qui implémentent `Send` et `Sync`. Si nous implémentons un type qui contient un type n’implémentant pas `Send` ou `Sync`, comme les pointeurs bruts, et que nous voulons marquer ce type comme `Send` ou `Sync`, nous devons utiliser `unsafe`. Rust ne peut pas vérifier que notre type respecte les garanties permettant de l’envoyer sans risque entre threads ou d’y accéder depuis plusieurs threads ; nous devons donc effectuer ces vérifications manuellement et l’indiquer avec `unsafe`.

### Accéder aux champs d’une union

La dernière opération qui n’est possible qu’avec `unsafe` consiste à accéder aux champs d’une union. Une *union* ressemble à une `struct`, mais, pour une instance donnée, un seul de ses champs déclarés est utilisé à la fois. Les unions servent principalement à interagir avec les unions du code C. L’accès aux champs d’une union est non sûr, car Rust ne peut pas garantir le type des données actuellement stockées dans l’instance de l’union. Pour en savoir plus sur les unions, consultez [la référence Rust][unions].

### Utiliser Miri pour vérifier du code non sûr

Lorsque vous écrivez du code non sûr, vous voudrez peut-être vérifier qu’il est réellement sûr et correct. L’une des meilleures façons de le faire est d’utiliser Miri, un outil officiel de Rust qui détecte les comportements indéfinis. Alors que le vérificateur d’emprunts est un outil _statique_ qui fonctionne à la compilation, Miri est un outil _dynamique_ qui fonctionne à l’exécution. Il vérifie votre code en exécutant votre programme ou sa suite de tests, et détecte les violations des règles qu’il connaît concernant le fonctionnement de Rust.

Miri nécessite une version nightly de Rust (dont nous parlerons plus en détail dans [l’annexe G : Comment Rust est conçu et « Rust nightly »][nightly]<!-- ignore -->). Vous pouvez installer à la fois une version nightly de Rust et l’outil Miri en exécutant `rustup +nightly component add miri`. Cela ne modifie pas la version de Rust utilisée par votre projet ; cela ajoute uniquement l’outil à votre système pour que vous puissiez l’utiliser lorsque vous le souhaitez. Vous pouvez exécuter Miri sur un projet en lançant `cargo +nightly miri run` ou `cargo +nightly miri test`.

Pour voir à quel point cet outil peut être utile, examinons ce qui se passe lorsque nous l’exécutons sur la liste 20-7.

```console
{{#include ../listings/ch20-advanced-features/listing-20-07/output.txt}}
```

Miri nous avertit à juste titre que nous convertissons un entier en pointeur, ce qui peut poser problème, mais il ne peut pas déterminer si c’est effectivement le cas, car il ne sait pas d’où vient le pointeur. Miri renvoie ensuite une erreur, car la liste 20-7 a un comportement indéfini dû à un pointeur pendant. Grâce à Miri, nous savons maintenant qu’il existe un risque de comportement indéfini, et nous pouvons réfléchir à la manière de rendre le code sûr. Dans certains cas, Miri peut même suggérer des façons de corriger les erreurs.

Miri ne détecte pas toutes les erreurs possibles lorsque vous écrivez du code non sûr. Comme il s’agit d’un outil d’analyse dynamique, il ne détecte que les problèmes liés au code effectivement exécuté. Vous devrez donc l’utiliser en complément de bonnes techniques de test afin d’accroître votre confiance dans le code non sûr que vous avez écrit. Miri ne couvre pas non plus toutes les façons dont votre code peut être incorrect.

En d’autres termes : si Miri détecte un problème, vous savez qu’il y a un bogue, mais le fait que Miri ne détecte _pas_ de bogue ne signifie pas qu’il n’y a pas de problème. Il peut toutefois en détecter beaucoup. Essayez de l’exécuter sur les autres exemples de code non sûr de ce chapitre et voyez ce qu’il indique !

Vous trouverez plus d’informations sur Miri dans [son dépôt GitHub][miri].

<!-- Old headings. Do not remove or links may break. -->

<a id="when-to-use-unsafe-code"></a>

### Utiliser correctement le code non sûr

Utiliser `unsafe` pour exploiter l’un des cinq superpouvoirs présentés plus haut n’est ni incorrect ni même mal vu, mais il est plus difficile d’écrire correctement du code `unsafe`, car le compilateur ne peut pas contribuer au respect de la sécurité mémoire. Lorsque vous avez une raison d’utiliser du code `unsafe`, vous pouvez le faire ; l’annotation explicite `unsafe` facilite la recherche de la source des problèmes lorsqu’ils surviennent. Chaque fois que vous écrivez du code non sûr, vous pouvez utiliser Miri pour vérifier avec plus de confiance qu’il respecte les règles de Rust.

Pour une exploration beaucoup plus approfondie des façons de travailler efficacement avec Rust non sûr, consultez le guide officiel de Rust consacré à `unsafe`, [The Rustonomicon][nomicon].

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