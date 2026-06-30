# Projet final : Construction d'un serveur web multithread

C'est un long chemin, mais nous sommes arrivés à la fin du livre. Dans ce chapitre, nous allons construire un projet de plus pour démontrer certains des concepts que nous avons abordés dans les derniers chapitres, ainsi que récapituler certaines leçons précédentes.

Pour notre projet final, nous allons créer un serveur web qui dit "Bonjour !" et qui ressemble à la Figure 21-1 dans un navigateur web.

Voici notre plan pour construire le serveur web :

1. Apprendre un peu sur TCP et HTTP.
2. Écouter les connexions TCP sur un socket.
3. Analyser un petit nombre de requêtes HTTP.
4. Créer une réponse HTTP appropriée.
5. Améliorer le débit de notre serveur avec un pool de threads.

<img alt="Capture d'écran d'un navigateur web visitant l'adresse 127.0.0.1:8080 affichant une page web avec le texte “Bonjour ! Bonjour de Rust”" src="img/trpl21-01.png" class="center" style="width: 50%;" />

<span class="caption">Figure 21-1 : Notre projet final partagé</span>

Avant de commencer, nous devons mentionner deux détails. Tout d'abord, la méthode que nous allons utiliser ne sera pas la meilleure façon de construire un serveur web avec Rust. Des membres de la communauté ont publié un certain nombre de crates prêtes pour la production disponibles sur [crates.io](https://crates.io/) qui offrent des implementations de serveurs web et de pools de threads plus complètes que celles que nous allons construire. Cependant, notre intention dans ce chapitre est de vous aider à apprendre, et non de prendre le chemin facile. Étant donné que Rust est un langage de programmation système, nous pouvons choisir le niveau d'abstraction avec lequel nous voulons travailler et pouvons aller à un niveau plus bas que ce qui est possible ou pratique dans d'autres langages.

Deuxièmement, nous n'utiliserons pas async et await ici. Construire un pool de threads est suffisamment difficile en soi, sans ajouter la construction d'un runtime async ! Cependant, nous noterons comment async et await pourraient s'appliquer à certains des mêmes problèmes que nous allons voir dans ce chapitre. En fin de compte, comme nous l'avons noté au chapitre 17, de nombreux runtimes async utilisent des pools de threads pour gérer leur travail.

Nous allons donc écrire manuellement le serveur HTTP de base et le pool de threads afin que vous puissiez apprendre les idées et techniques générales derrière les crates que vous pourriez utiliser à l'avenir.