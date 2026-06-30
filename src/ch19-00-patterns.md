# Modèles et Correspondance

Les modèles sont une syntaxe spéciale en Rust pour faire correspondre la structure des types, qu'ils soient complexes ou simples. L'utilisation de modèles avec les expressions `match` et d'autres constructions vous donne plus de contrôle sur le flux d'exécution d'un programme. Un modèle consiste en une combinaison de certains éléments suivants :

- Littéraux
- Tableaux, énumérations, structures ou tuples déstructurés
- Variables
- Jokers
- Espaces réservés

Quelques exemples de modèles incluent `x`, `(a, 3)`, et `Some(Color::Red)`. Dans les contextes où les modèles sont valides, ces composants décrivent la forme des données. Notre programme compare ensuite des valeurs aux modèles pour déterminer si elles ont la forme de données correcte pour continuer l'exécution d'un code particulier.

Pour utiliser un modèle, nous le comparons à une valeur. Si le modèle correspond à la valeur, nous utilisons les parties de la valeur dans notre code. Rappelez-vous des expressions `match` dans le Chapitre 6 qui utilisaient des modèles, comme l'exemple de la machine à trier les pièces. Si la valeur correspond à la forme du modèle, nous pouvons utiliser les éléments nommés. Si ce n'est pas le cas, le code associé au modèle ne s'exécutera pas.

Ce chapitre est une référence sur tout ce qui concerne les modèles. Nous aborderons les endroits valides pour utiliser des modèles, la différence entre les modèles réfutables et irréfutables, et les différents types de syntaxe de modèles que vous pourriez rencontrer. À la fin du chapitre, vous saurez comment utiliser les modèles pour exprimer de nombreux concepts de manière claire.