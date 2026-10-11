# Énumérations et filtrage par motif

Dans ce chapitre, nous allons étudier les énumérations, également appelées _enums_.
Les enums vous permettent de définir un type en énumérant ses variantes possibles. Nous
commencerons par définir et utiliser une enum afin de montrer comment une enum peut
associer une signification à des données. Ensuite, nous étudierons une enum
particulièrement utile, appelée `Option`, qui exprime qu’une valeur peut être soit
quelque chose, soit rien. Puis, nous verrons comment le filtrage par motif dans
l’expression `match` permet facilement d’exécuter un code différent selon les
valeurs d’une enum. Enfin, nous aborderons la construction `if let`, une autre
syntaxe pratique et concise pour gérer les enums dans votre code.