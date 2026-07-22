## Annexe C : Traits Dérivables

À divers endroits du livre, nous avons discuté de l'attribut `derive`, que vous pouvez appliquer à une définition de struct ou d'énumération. L'attribut `derive` génère du code qui met en œuvre un trait avec sa propre implémentation par défaut sur le type que vous avez annoté avec la syntaxe `derive`.

Dans cette annexe, nous fournissons une référence de tous les traits de la bibliothèque standard que vous pouvez utiliser avec `derive`. Chaque section couvre :

- Quelles opérations et méthodes la dérivation de ce trait permettra
- Ce que l'implémentation du trait fournie par `derive` fait
- Ce que signifie l'implémentation du trait pour le type
- Les conditions dans lesquelles vous êtes autorisé ou non à implémenter le trait
- Des exemples d'opérations nécessitant le trait

Si vous souhaitez un comportement différent de celui fourni par l'attribut `derive`, consultez la [documentation de la bibliothèque standard](../std/index.html)<!-- ignore --> pour chaque trait pour obtenir des détails sur la manière de les implémenter manuellement.

Les traits énumérés ici sont les seuls définis par la bibliothèque standard qui peuvent être implémentés sur vos types à l'aide de `derive`. D'autres traits définis dans la bibliothèque standard n'ont pas de comportement par défaut sensé, donc il vous appartient de les implémenter de la manière qui a du sens pour ce que vous essayez d'accomplir.

Un exemple de trait qui ne peut pas être dérivé est `Display`, qui gère le formatage pour les utilisateurs finaux. Vous devez toujours considérer la manière appropriée d'afficher un type à un utilisateur final. Quelles parties du type un utilisateur final devrait-il être autorisé à voir ? Quelles parties seraient pertinentes pour lui ? Quel format des données serait le plus pertinent pour lui ? Le compilateur Rust n'a pas cette perspective, donc il ne peut pas fournir un comportement par défaut approprié pour vous.

La liste des traits dérivables fournie dans cette annexe n'est pas exhaustive : Les bibliothèques peuvent implémenter `derive` pour leurs propres traits, rendant la liste des traits avec lesquels vous pouvez utiliser `derive` véritablement ouverte. L'implémentation de `derive` implique l'utilisation d'un macro procédural, qui est couverte dans la section [“Macros personnalisées `derive`”][custom-derive-macros]<!-- ignore --> au chapitre 20.

### `Debug` pour la Sortie du Programmeur

Le trait `Debug` permet un formatage de débogage dans les chaînes de format, que vous indiquez en ajoutant `:?` dans des espaces réservés `{}`.

Le trait `Debug` vous permet d'imprimer des instances d'un type à des fins de débogage, afin que vous et d'autres programmeurs utilisant votre type puissiez inspecter une instance à un moment donné dans l'exécution d'un programme.

Le trait `Debug` est requis, par exemple, lors de l'utilisation du macro `assert_eq!`. Ce macro imprime les valeurs des instances données en tant qu'arguments si l'assertion d'égalité échoue, afin que les programmeurs puissent voir pourquoi les deux instances n'étaient pas égales.

### `PartialEq` et `Eq` pour les Comparaisons d'Égalité

Le trait `PartialEq` vous permet de comparer des instances d'un type pour vérifier leur égalité et permet l'utilisation des opérateurs `==` et `!=`.

Dériver `PartialEq` implémente la méthode `eq`. Lorsque `PartialEq` est dérivé sur des structs, deux instances sont égales uniquement si _tous_ les champs sont égaux, et les instances ne sont pas égales si _au moins_ un champ est différent. Lorsqu'il est dérivé sur des énumérations, chaque variante est égale à elle-même et n'est pas égale aux autres variantes.

Le trait `PartialEq` est requis, par exemple, lors de l'utilisation du macro `assert_eq!`, qui doit être capable de comparer deux instances d'un type pour leur égalité.

Le trait `Eq` n'a pas de méthodes. Son but est de signaler que pour chaque valeur du type annoté, la valeur est égale à elle-même. Le trait `Eq` ne peut être appliqué qu'aux types qui implémentent également `PartialEq`, bien que tous les types qui implémentent `PartialEq` ne puissent pas implémenter `Eq`. Un exemple de cela est les types de nombres à virgule flottante : L'implémentation des nombres à virgule flottante stipule que deux instances de la valeur non-un nombre (`NaN`) ne sont pas égales entre elles.

Un exemple de situation où `Eq` est requis est pour les clés dans un `HashMap<K, V>` afin que le `HashMap<K, V>` puisse déterminer si deux clés sont identiques.

### `PartialOrd` et `Ord` pour les Comparaisons de Classement

Le trait `PartialOrd` vous permet de comparer des instances d'un type à des fins de tri. Un type qui implémente `PartialOrd` peut être utilisé avec les opérateurs `<`, `>`, `<=` et `>=`. Vous ne pouvez appliquer le trait `PartialOrd` qu'aux types qui implémentent également `PartialEq`.

Dériver `PartialOrd` implémente la méthode `partial_cmp`, qui retourne une `Option<Ordering>` qui sera `None` lorsque les valeurs données ne produisent pas un ordre. Un exemple d'une valeur qui ne produit pas d'ordre, même si la plupart des valeurs de ce type peuvent être comparées, est la valeur à virgule flottante `NaN`. Appeler `partial_cmp` avec n'importe quel nombre à virgule flottante et la valeur à virgule flottante `NaN` retournera `None`.

Lorsqu'il est dérivé sur des structs, `PartialOrd` compare deux instances en comparant la valeur dans chaque champ dans l'ordre dans lequel les champs apparaissent dans la définition de la struct. Lorsqu'il est dérivé sur des énumérations, les variantes de l'énumération déclarées plus tôt dans la définition de l'énumération sont considérées comme inférieures aux variantes énumérées plus tard.

Le trait `PartialOrd` est requis, par exemple, pour la méthode `gen_range` du crate `rand` qui génère une valeur aléatoire dans la plage spécifiée par une expression de plage.

Le trait `Ord` vous permet de savoir que pour deux valeurs de n'importe quel type annoté, un ordre valide existera. Le trait `Ord` implémente la méthode `cmp`, qui retourne un `Ordering` plutôt qu'une `Option<Ordering>` car un ordre valide sera toujours possible. Vous ne pouvez appliquer le trait `Ord` qu'aux types qui implémentent également `PartialOrd` et `Eq` (et `Eq` nécessite `PartialEq`). Lorsqu'il est dérivé sur des structs et des énumérations, `cmp` se comporte de la même manière que l'implémentation dérivée pour `partial_cmp` le fait avec `PartialOrd`.

Un exemple de situation où `Ord` est requis est lors du stockage de valeurs dans un `BTreeSet<T>`, une structure de données qui stocke des données en fonction de l'ordre de tri des valeurs.

### `Clone` et `Copy` pour la Duplication de Valeurs

Le trait `Clone` vous permet de créer explicitement une copie profonde d'une valeur, et le processus de duplication peut impliquer l'exécution de code arbitraire et la copie de données sur le tas. Consultez la section [“Variables et Données Interagissant avec
Clone”][variables-and-data-interacting-with-clone]<!-- ignore --> au chapitre 4 pour plus d'informations sur `Clone`.

Dériver `Clone` implémente la méthode `clone`, qui, lorsqu'elle est implémentée pour l'ensemble du type, appelle `clone` sur chacune des parties du type. Cela signifie que tous les champs ou valeurs dans le type doivent également implémenter `Clone` pour dériver `Clone`.

Un exemple de situation où `Clone` est requis est lors de l'appel de la méthode `to_vec` sur un slice. Le slice ne possède pas les instances de type qu'il contient, mais le vecteur retourné par `to_vec` devra posséder ses instances, donc `to_vec` appelle `clone` sur chaque élément. Ainsi, le type stocké dans le slice doit implémenter `Clone`.

Le trait `Copy` vous permet de dupliquer une valeur en copiant uniquement les bits stockés sur la pile ; aucun code arbitraire n'est nécessaire. Consultez la section [“Données Uniquement sur la Pile : Copy”][stack-only-data-copy]<!-- ignore --> au chapitre 4 pour plus d'informations sur `Copy`.

Le trait `Copy` ne définit aucune méthode pour empêcher les programmeurs de surcharger ces méthodes et de violer l'hypothèse selon laquelle aucun code arbitraire n'est exécuté. Ainsi, tous les programmeurs peuvent supposer que copier une valeur sera très rapide.

Vous pouvez dériver `Copy` sur n'importe quel type dont les parties implémentent toutes `Copy`. Un type qui implémente `Copy` doit également implémenter `Clone` car un type qui implémente `Copy` a une implémentation triviale de `Clone` qui effectue la même tâche que `Copy`.

Le trait `Copy` est rarement requis ; les types qui implémentent `Copy` ont des optimisations disponibles, donc vous n'avez pas à appeler `clone`, ce qui rend le code plus concis.

Tout ce qui est possible avec `Copy` peut également être accompli avec `Clone`, mais le code pourrait être plus lent ou devoir utiliser `clone` à certains endroits.

### `Hash` pour Mapper une Valeur à une Valeur de Taille Fixe

Le trait `Hash` vous permet de prendre une instance d'un type de taille arbitraire et de mapper cette instance à une valeur de taille fixe à l'aide d'une fonction de hachage. Dériver `Hash` implémente la méthode `hash`. L'implémentation dérivée de la méthode `hash` combine le résultat de l'appel de `hash` sur chacune des parties du type, ce qui signifie que tous les champs ou valeurs doivent également implémenter `Hash` pour dériver `Hash`.

Un exemple de situation où `Hash` est requis est dans le stockage des clés dans un `HashMap<K, V>` pour stocker des données de manière efficace.

### `Default` pour les Valeurs Par Défaut

Le trait `Default` vous permet de créer une valeur par défaut pour un type. Dériver `Default` implémente la fonction `default`. L'implémentation dérivée de la fonction `default` appelle la fonction `default` sur chaque partie du type, ce qui signifie que tous les champs ou valeurs du type doivent également implémenter `Default` pour dériver `Default`.

La fonction `Default::default` est couramment utilisée en combinaison avec la syntaxe de mise à jour de struct discutée dans la section [“Créer des Instances à Partir d'Autres Instances avec la Syntaxe de Mise à Jour de Struct”][creating-instances-from-other-instances-with-struct-update-syntax]<!-- ignore --> au chapitre 5. Vous pouvez personnaliser quelques champs d'une struct et ensuite définir et utiliser une valeur par défaut pour le reste des champs en utilisant `..Default::default()`.

Le trait `Default` est requis lorsque vous utilisez la méthode `unwrap_or_default` sur des instances `Option<T>`, par exemple. Si l'`Option<T>` est `None`, la méthode `unwrap_or_default` renverra le résultat de `Default::default` pour le type `T` stocké dans l'`Option<T>`.

[creating-instances-from-other-instances-with-struct-update-syntax]: ch05-01-defining-structs.html#creating-instances-from-other-instances-with-struct-update-syntax
[stack-only-data-copy]: ch04-01-what-is-ownership.html#stack-only-data-copy
[variables-and-data-interacting-with-clone]: ch04-01-what-is-ownership.html#variables-and-data-interacting-with-clone
[custom-derive-macros]: ch20-05-macros.html#custom-derive-macros