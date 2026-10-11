# Motifs et correspondance

Les motifs sont une syntaxe spéciale de Rust qui permet de faire correspondre la structure des types, qu’ils soient complexes ou simples. Utiliser des motifs avec les expressions `match` et d’autres constructions vous donne davantage de contrôle sur le flux d’exécution d’un programme. Un motif se compose d’une combinaison des éléments suivants :

- Littéraux
- Tableaux, énumérations, structures ou tuples déstructurés
- Variables
- Jokers
- Espaces réservés

Parmi les exemples de motifs, on trouve `x`, `(a, 3)` et `Some(Color::Red)`. Dans les contextes où les motifs sont valides, ces éléments décrivent la forme des données. Notre programme compare ensuite les valeurs aux motifs pour déterminer si elles ont la forme attendue pour poursuivre l’exécution d’une partie du code.

Pour utiliser un motif, nous le comparons à une valeur. Si le motif correspond à la valeur, nous utilisons les parties de cette valeur dans notre code. Rappelez-vous les expressions `match` du chapitre 6 qui utilisaient des motifs, comme l’exemple du distributeur de pièces. Si la valeur correspond à la forme du motif, nous pouvons utiliser les éléments nommés. Dans le cas contraire, le code associé au motif ne s’exécutera pas.

Ce chapitre est une référence sur tout ce qui concerne les motifs. Nous aborderons les endroits où les motifs peuvent être utilisés, la différence entre les motifs réfutables et irréfutables, ainsi que les différents types de syntaxe de motif que vous pourrez rencontrer. À la fin du chapitre, vous saurez comment utiliser les motifs pour exprimer clairement de nombreux concepts.