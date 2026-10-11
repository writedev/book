## Annexe C : Traits pouvant être dérivés

À différents endroits de ce livre, nous avons parlé de l’attribut `derive`, que vous pouvez appliquer à la définition d’une structure ou d’une énumération. L’attribut `derive` génère du code qui implémente un trait avec son implémentation par défaut sur le type auquel vous avez appliqué la syntaxe `derive`.

Dans cette annexe, nous répertorions tous les traits de la bibliothèque standard que vous pouvez utiliser avec `derive`. Chaque section présente :

- Les opérateurs et méthodes que le dérivé de ce trait rend disponibles
- Ce que fait l’implémentation du trait fournie par `derive`
- Ce que l’implémentation du trait signifie pour le type
- Les conditions dans lesquelles vous pouvez ou ne pouvez pas implémenter le trait
- Des exemples d’opérations qui nécessitent le trait

Si vous souhaitez un comportement différent de celui fourni par l’attribut `derive`, consultez la [documentation de la bibliothèque standard](../std/index.html)<!-- ignore --> de chaque trait pour savoir comment les implémenter manuellement.

Les traits répertoriés ici sont les seuls traits définis par la bibliothèque standard qui peuvent être implémentés sur vos types à l’aide de `derive`. Les autres traits définis par la bibliothèque standard n’ont pas de comportement par défaut pertinent ; c’est donc à vous de les implémenter d’une manière adaptée à ce que vous cherchez à accomplir.

`Display`, qui gère le formatage destiné aux utilisateurs finaux, est un exemple de trait qui ne peut pas être dérivé. Vous devez toujours réfléchir à la manière appropriée d’afficher un type à un utilisateur final. Quelles parties du type un utilisateur final devrait-il pouvoir voir ? Quelles parties lui seraient utiles ? Quel format de données lui serait le plus utile ? Le compilateur Rust ne dispose pas de ces informations et ne peut donc pas fournir de comportement par défaut approprié.

La liste des traits pouvant être dérivés présentée dans cette annexe n’est pas exhaustive : les bibliothèques peuvent implémenter `derive` pour leurs propres traits, ce qui rend la liste des traits utilisables avec `derive` véritablement illimitée. L’implémentation de `derive` implique l’utilisation d’une macro procédurale, présentée dans la section [« Macros `derive` personnalisées »][custom-derive-macros]<!-- ignore --> du chapitre 20.

### `Debug` pour la sortie destinée aux programmeurs

Le trait `Debug` active le formatage de débogage dans les chaînes de format, que vous indiquez en ajoutant `:?` dans les espaces réservés `{}`.

Le trait `Debug` vous permet d’afficher des instances d’un type à des fins de débogage, afin que vous et les autres programmeurs qui utilisent votre type puissiez examiner une instance à un moment donné de l’exécution d’un programme.

Le trait `Debug` est notamment requis pour utiliser la macro `assert_eq!`. Si l’assertion d’égalité échoue, cette macro affiche les valeurs des instances fournies en arguments, afin que les programmeurs puissent voir pourquoi elles ne sont pas égales.

### `PartialEq` et `Eq` pour les comparaisons d’égalité

Le trait `PartialEq` vous permet de comparer des instances d’un type pour vérifier leur égalité et d’utiliser les opérateurs `==` et `!=`.

Dériver `PartialEq` implémente la méthode `eq`. Lorsque `PartialEq` est dérivé pour des structures, deux instances sont égales uniquement si _tous_ leurs champs sont égaux, et elles ne sont pas égales si _au moins un_ de leurs champs ne l’est pas. Lorsqu’il est dérivé pour des énumérations, chaque variante est égale à elle-même et différente des autres variantes.

Le trait `PartialEq` est notamment requis pour utiliser la macro `assert_eq!`, qui doit pouvoir comparer deux instances d’un type pour vérifier leur égalité.

Le trait `Eq` ne possède aucune méthode. Son rôle est de signaler que, pour toute valeur du type annoté, cette valeur est égale à elle-même. Le trait `Eq` ne peut s’appliquer qu’aux types qui implémentent aussi `PartialEq`, même si tous les types qui implémentent `PartialEq` ne peuvent pas implémenter `Eq`. Les types à virgule flottante en sont un exemple : leur implémentation stipule que deux instances de la valeur « pas un nombre » (`NaN`) ne sont pas égales.

Les clés d’une `HashMap<K, V>` sont un exemple de cas où `Eq` est requis, afin que la `HashMap<K, V>` puisse déterminer si deux clés sont identiques.

### `PartialOrd` et `Ord` pour les comparaisons d’ordre

Le trait `PartialOrd` vous permet de comparer des instances d’un type à des fins de tri. Un type qui implémente `PartialOrd` peut être utilisé avec les opérateurs `<`, `>`, `<=` et `>=`. Vous ne pouvez appliquer le trait `PartialOrd` qu’aux types qui implémentent aussi `PartialEq`.

Dériver `PartialOrd` implémente la méthode `partial_cmp`, qui renvoie une `Option<Ordering>` dont la valeur sera `None` lorsque les valeurs fournies ne permettent pas d’établir un ordre. La valeur à virgule flottante `NaN` est un exemple de valeur qui ne permet pas d’établir un ordre, même si la plupart des valeurs de ce type peuvent être comparées. Appeler `partial_cmp` avec n’importe quel nombre à virgule flottante et la valeur `NaN` renverra `None`.

Lorsqu’il est dérivé pour des structures, `PartialOrd` compare deux instances en comparant la valeur de chaque champ dans l’ordre où les champs apparaissent dans la définition de la structure. Lorsqu’il est dérivé pour des énumérations, les variantes déclarées plus tôt dans la définition de l’énumération sont considérées comme inférieures à celles déclarées plus tard.

Le trait `PartialOrd` est notamment requis par la méthode `gen_range` de la crate `rand`, qui génère une valeur aléatoire dans l’intervalle spécifié par une expression d’intervalle.

Le trait `Ord` vous garantit qu’il existera un ordre valide entre deux valeurs quelconques du type annoté. Le trait `Ord` implémente la méthode `cmp`, qui renvoie un `Ordering` plutôt qu’une `Option<Ordering>`, puisqu’un ordre valide est toujours possible. Vous ne pouvez appliquer le trait `Ord` qu’aux types qui implémentent aussi `PartialOrd` et `Eq` (`Eq` exige lui-même `PartialEq`). Lorsqu’il est dérivé pour des structures et des énumérations, `cmp` se comporte comme l’implémentation dérivée de `partial_cmp` pour `PartialOrd`.

Le stockage de valeurs dans un `BTreeSet<T>`, une structure de données qui stocke les données selon l’ordre de tri des valeurs, est un exemple de cas où `Ord` est requis.

### `Clone` et `Copy` pour dupliquer des valeurs

Le trait `Clone` vous permet de créer explicitement une copie profonde d’une valeur ; le processus de duplication peut impliquer l’exécution de code arbitraire et la copie de données situées dans le tas. Pour en savoir plus sur `Clone`, consultez la section [« Variables et données interagissant avec Clone »][variables-and-data-interacting-with-clone]<!-- ignore --> du chapitre 4.

Dériver `Clone` implémente la méthode `clone`, qui, lorsqu’elle est implémentée pour l’ensemble du type, appelle `clone` sur chacune des parties de ce type. Cela signifie que tous les champs ou toutes les valeurs du type doivent aussi implémenter `Clone` pour que `Clone` puisse être dérivé.

L’appel de la méthode `to_vec` sur une tranche est un exemple de cas où `Clone` est requis. La tranche ne possède pas les instances du type qu’elle contient, mais le vecteur renvoyé par `to_vec` doit posséder ses propres instances ; `to_vec` appelle donc `clone` sur chaque élément. Le type stocké dans la tranche doit donc implémenter `Clone`.

Le trait `Copy` vous permet de dupliquer une valeur en copiant uniquement les bits stockés sur la pile ; aucun code arbitraire n’est nécessaire. Pour en savoir plus sur `Copy`, consultez la section [« Données sur la pile uniquement : Copy »][stack-only-data-copy]<!-- ignore --> du chapitre 4.

Le trait `Copy` ne définit aucune méthode, afin d’empêcher les programmeurs de les surcharger et de violer l’hypothèse selon laquelle aucun code arbitraire n’est exécuté. Ainsi, tous les programmeurs peuvent supposer que la copie d’une valeur est très rapide.

Vous pouvez dériver `Copy` pour tout type dont toutes les parties implémentent `Copy`. Un type qui implémente `Copy` doit aussi implémenter `Clone`, car il possède une implémentation triviale de `Clone` qui effectue la même opération que `Copy`.

Le trait `Copy` est rarement requis ; les types qui l’implémentent bénéficient d’optimisations, ce qui vous évite d’appeler `clone` et rend le code plus concis.

Tout ce que vous pouvez faire avec `Copy`, vous pouvez aussi le faire avec `Clone`, mais le code risque d’être plus lent ou de nécessiter l’emploi de `clone` à certains endroits.

### `Hash` pour associer une valeur à une valeur de taille fixe

Le trait `Hash` vous permet de prendre une instance d’un type de taille arbitraire et de lui associer une valeur de taille fixe à l’aide d’une fonction de hachage. Dériver `Hash` implémente la méthode `hash`. L’implémentation dérivée de la méthode `hash` combine les résultats de l’appel de `hash` sur chacune des parties du type ; tous ses champs ou toutes ses valeurs doivent donc aussi implémenter `Hash` pour que `Hash` puisse être dérivé.

Le stockage de clés dans une `HashMap<K, V>` afin d’y stocker des données efficacement est un exemple de cas où `Hash` est requis.

### `Default` pour les valeurs par défaut

Le trait `Default` vous permet de créer une valeur par défaut pour un type. Dériver `Default` implémente la fonction `default`. L’implémentation dérivée de la fonction `default` appelle la fonction `default` sur chacune des parties du type ; tous ses champs ou toutes ses valeurs doivent donc aussi implémenter `Default` pour que `Default` puisse être dérivé.

La fonction `Default::default` est couramment utilisée avec la syntaxe de mise à jour de structure présentée dans la section [« Créer des instances à partir d’autres instances avec la syntaxe de mise à jour de structure »][creating-instances-from-other-instances-with-struct-update-syntax]<!--
ignore --> du chapitre 5. Vous pouvez personnaliser quelques champs d’une structure, puis définir et utiliser une valeur par défaut pour les champs restants en utilisant `..Default::default()`.

Le trait `Default` est notamment requis lorsque vous utilisez la méthode `unwrap_or_default` sur des instances de `Option<T>`. Si le `Option<T>` vaut `None`, la méthode `unwrap_or_default` renverra le résultat de `Default::default` pour le type `T` stocké dans le `Option<T>`.

[creating-instances-from-other-instances-with-struct-update-syntax]: ch05-01-defining-structs.html#creating-instances-from-other-instances-with-struct-update-syntax
[stack-only-data-copy]: ch04-01-what-is-ownership.html#stack-only-data-copy
[variables-and-data-interacting-with-clone]: ch04-01-what-is-ownership.html#variables-and-data-interacting-with-clone
[custom-derive-macros]: ch20-05-macros.html#custom-derive-macros