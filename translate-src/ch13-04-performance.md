<!-- Anciens titres. Ne pas supprimer, sinon les liens risquent de ne plus fonctionner. -->

<a id="comparing-performance-loops-vs-iterators"></a>

## Performances des boucles et des itérateurs

Pour déterminer s’il vaut mieux utiliser des boucles ou des itérateurs, vous devez savoir quelle implémentation est la plus rapide : la version de la fonction `search` avec une boucle `for` explicite ou la version utilisant des itérateurs.

Nous avons effectué un test de performances en chargeant l’intégralité du contenu des _Aventures de Sherlock Holmes_ de Sir Arthur Conan Doyle dans une `String`, puis en recherchant le mot _the_ dans ce contenu. Voici les résultats du test pour la version de `search` utilisant la boucle `for` et celle utilisant des itérateurs :

```text
test bench_search_for  ... bench:  19,620,300 ns/iter (+/- 915,700)
test bench_search_iter ... bench:  19,234,900 ns/iter (+/- 657,200)
```

Les deux implémentations ont des performances similaires ! Nous n’expliquerons pas ici le code du test de performances, car le but n’est pas de prouver que les deux versions sont équivalentes, mais de se faire une idée générale de leurs performances respectives.

Pour réaliser un test de performances plus complet, vous devriez essayer différents textes de différentes tailles comme `contents`, différents mots et des mots de différentes longueurs comme `query`, ainsi que toutes sortes d’autres variations. Voici l’essentiel : les itérateurs, bien qu’ils constituent une abstraction de haut niveau, sont compilés en un code pratiquement identique à celui que vous auriez écrit vous-même à un niveau inférieur. Les itérateurs font partie des _abstractions à coût nul_ de Rust : cela signifie que leur utilisation n’entraîne aucune surcharge supplémentaire à l’exécution. Cela rejoint la définition du coût nul donnée par Bjarne Stroustrup, concepteur et développeur d’origine du C++, dans sa présentation liminaire à ETAPS en 2012, « Foundations of C++ » :

> En général, les implémentations du C++ respectent le principe du coût nul : ce que vous n’utilisez pas ne vous coûte rien. Et, de plus : ce que vous utilisez, vous ne pourriez pas l’écrire à la main de façon plus efficace.

Dans de nombreux cas, le code Rust utilisant des itérateurs est compilé en un code assembleur identique à celui que vous écririez à la main. Des optimisations telles que le déroulement des boucles et la suppression des vérifications de limites lors de l’accès aux tableaux sont appliquées, ce qui rend le code produit extrêmement efficace. Maintenant que vous le savez, vous pouvez utiliser des itérateurs et des fermetures sans crainte ! Ils donnent au code une apparence de haut niveau, sans pour autant entraîner de pénalité en matière de performances à l’exécution.

## Résumé

Les fermetures et les itérateurs sont des fonctionnalités de Rust inspirées des idées des langages de programmation fonctionnelle. Elles contribuent à la capacité de Rust à exprimer clairement des idées de haut niveau tout en offrant des performances de bas niveau. Les implémentations des fermetures et des itérateurs sont conçues de telle sorte que les performances à l’exécution ne sont pas affectées. Cela s’inscrit dans l’objectif de Rust de proposer des abstractions à coût nul.

Maintenant que nous avons amélioré l’expressivité de notre projet d’E/S, intéressons-nous à d’autres fonctionnalités de `cargo` qui nous aideront à partager le projet avec le monde entier.