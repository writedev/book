# Caractéristiques des langages fonctionnels : itérateurs et fermetures

La conception de Rust s’inspire de nombreux langages et techniques existants, et l’une de ses influences importantes est la _programmation fonctionnelle_.
Programmer dans un style fonctionnel consiste souvent à utiliser des fonctions comme des valeurs : les passer en arguments, les renvoyer depuis d’autres fonctions, les affecter à des variables pour les exécuter plus tard, et ainsi de suite.

Dans ce chapitre, nous ne débattrons pas de ce qu’est ou n’est pas la programmation fonctionnelle, mais nous examinerons plutôt certaines caractéristiques de Rust qui sont similaires à celles que l’on trouve dans de nombreux langages souvent qualifiés de fonctionnels.

Plus précisément, nous aborderons :

- Les _fermetures_, des constructions semblables à des fonctions que vous pouvez stocker dans une variable
- Les _itérateurs_, une façon de traiter une série d’éléments
- Comment utiliser les fermetures et les itérateurs pour améliorer le projet d’E/S du chapitre 12
- Les performances des fermetures et des itérateurs (attention, divulgâchis : elles sont plus rapides que vous ne le pensez !)

Nous avons déjà abordé d’autres caractéristiques de Rust, comme la correspondance de motifs et les énumérations, qui sont elles aussi influencées par le style fonctionnel. Comme la maîtrise des fermetures et des itérateurs est essentielle pour écrire du code Rust rapide et idiomatique, nous consacrerons tout ce chapitre à ces sujets.