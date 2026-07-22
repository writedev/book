<!-- Anciennes en-têtes. Ne pas supprimer ou les liens peuvent se briser. -->

<a id="comparing-performance-loops-vs-iterators"></a>

## Performance des Boucles vs. Itérateurs

Pour déterminer s'il faut utiliser des boucles ou des itérateurs, vous devez savoir quelle implémentation est plus rapide : la version de la fonction `search` avec une boucle `for` explicite ou la version avec des itérateurs.

Nous avons réalisé un benchmark en chargeant l'intégralité du contenu de _The Adventures of Sherlock Holmes_ de Sir Arthur Conan Doyle dans une `String` et en recherchant le mot _the_ dans le contenu. Voici les résultats du benchmark sur la version de `search` utilisant la boucle `for` et la version utilisant des itérateurs :

```text
test bench_search_for  ... bench:  19,620,300 ns/iter (+/- 915,700)
test bench_search_iter ... bench:  19,234,900 ns/iter (+/- 657,200)
```

Les deux implémentations ont une performance similaire ! Nous n'expliquerons pas le code du benchmark ici car le but n'est pas de prouver que les deux versions sont équivalentes, mais d'obtenir une idée générale de la comparaison de performance entre ces deux implémentations.

Pour un benchmark plus complet, vous devriez vérifier en utilisant divers textes de différentes tailles comme `contents`, différents mots et mots de longueurs variées comme `query`, et toutes sortes d'autres variations. Le point est le suivant : Les itérateurs, bien qu'abstraction de haut niveau, sont compilés en gros dans le même code que si vous aviez écrit le code de bas niveau vous-même. Les itérateurs sont l'une des _abstractions sans coût_ de Rust, par quoi nous entendons que l'utilisation de l'abstraction n'impose aucun surcoût d'exécution supplémentaire. Cela est analogue à la façon dont Bjarne Stroustrup, le concepteur et implémenteur original de C++, définit le principe de zéro coût dans sa présentation principale de 2012 à l'ETAPS “Foundations of C++” :

> En général, les implémentations C++ obéissent au principe de zéro coût : Ce que vous n'utilisez pas, vous ne payez pas. Et de plus : Ce que vous utilisez, vous ne pourriez pas le coder mieux à la main.

Dans de nombreux cas, le code Rust utilisant des itérateurs se compile en l'assemblage que vous écririez à la main. Des optimisations telles que le déroulement de boucle et l'élimination des vérifications de limites sur l'accès aux tableaux s'appliquent et rendent le code résultant extrêmement efficace. Maintenant que vous savez cela, vous pouvez utiliser des itérateurs et des fermetures sans crainte ! Ils donnent l'impression que le code est plus abstrait mais n'imposent pas de pénalité de performance d'exécution pour ce faire.

## Résumé

Les fermetures et les itérateurs sont des fonctionnalités de Rust inspirées par des idées de langages de programmation fonctionnels. Ils contribuent à la capacité de Rust à exprimer clairement des idées de haut niveau avec des performances de bas niveau. Les implémentations de fermetures et d'itérateurs sont telles que la performance d'exécution n'est pas affectée. Cela fait partie de l'objectif de Rust de s'efforcer de fournir des abstractions sans coût.

Maintenant que nous avons amélioré l'expressivité de notre projet d'E/S, examinons quelques autres fonctionnalités de `cargo` qui nous aideront à partager le projet avec le monde.