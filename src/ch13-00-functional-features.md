# Caractéristiques du langage fonctionnel : Itérateurs et fermetures

Le design de Rust s'est inspiré de nombreux langages et techniques existants, et une influence significative est la _programmation fonctionnelle_. Programmer dans un style fonctionnel inclut souvent l'utilisation de fonctions comme valeurs en les passant en arguments, en les retournant d'autres fonctions, en les assignant à des variables pour une exécution ultérieure, et ainsi de suite.

Dans ce chapitre, nous ne débattrons pas de ce qu'est ou n'est pas la programmation fonctionnelle, mais nous discuterons plutôt de certaines caractéristiques de Rust qui ressemblent à des caractéristiques de nombreux langages souvent qualifiés de fonctionnels.

Plus spécifiquement, nous aborderons :

- _Fermetures_, une construction semblable à une fonction que vous pouvez stocker dans une variable
- _Itérateurs_, une façon de traiter une série d'éléments
- Comment utiliser les fermetures et les itérateurs pour améliorer le projet I/O au chapitre 12
- La performance des fermetures et des itérateurs (alerte spoiler : elles sont plus rapides que vous ne le pensez !)

Nous avons déjà abordé d'autres caractéristiques de Rust, telles que le pattern matching et les enums, qui sont également influencées par le style fonctionnel. Comme maîtriser les fermetures et les itérateurs est une partie importante de l'écriture d'un code Rust rapide et idiomatique, nous consacrerons tout ce chapitre à ces sujets.