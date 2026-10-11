# Un projet d’E/S : créer un programme en ligne de commande

Ce chapitre récapitule les nombreuses compétences que vous avez acquises jusqu’à présent et vous fait découvrir quelques fonctionnalités supplémentaires de la bibliothèque standard. Nous allons créer un outil en ligne de commande qui interagit avec les entrées et sorties des fichiers et de la ligne de commande afin de mettre en pratique certains des concepts de Rust que vous maîtrisez désormais.

La vitesse, la sûreté, la production d’un binaire unique et la prise en charge multiplateforme de Rust en font un langage idéal pour créer des outils en ligne de commande. Pour notre projet, nous allons donc créer notre propre version de l’outil de recherche classique en ligne de commande `grep` (recherche globale d’une expression régulière et affichage). Dans le cas d’utilisation le plus simple, `grep` recherche une chaîne spécifiée dans un fichier spécifié. Pour ce faire, `grep` prend comme arguments un chemin de fichier et une chaîne. Il lit ensuite le fichier, trouve les lignes qui contiennent la chaîne fournie en argument et affiche ces lignes.

Au fil du chapitre, nous montrerons comment faire en sorte que notre outil en ligne de commande utilise les fonctionnalités du terminal employées par de nombreux autres outils du même type. Nous lirons la valeur d’une variable d’environnement pour permettre à l’utilisateur de configurer le comportement de notre outil. Nous afficherons également les messages d’erreur dans le flux d’erreur standard de la console (`stderr`) plutôt que dans la sortie standard (`stdout`), afin que, par exemple, l’utilisateur puisse rediriger les résultats positifs vers un fichier tout en continuant à voir les messages d’erreur à l’écran.

Andrew Gallant, membre de la communauté Rust, a déjà créé une version complète et très rapide de `grep`, appelée `ripgrep`. Notre version sera relativement simple en comparaison, mais ce chapitre vous apportera les connaissances de base nécessaires pour comprendre un projet réel tel que `ripgrep`.

Notre projet `grep` combinera plusieurs concepts que vous avez déjà appris :

- Organiser le code ([chapitre 7][ch7]<!-- ignore -->)
- Utiliser des vecteurs et des chaînes de caractères ([chapitre 8][ch8]<!-- ignore -->)
- Gérer les erreurs ([chapitre 9][ch9]<!-- ignore -->)
- Utiliser les traits et les durées de vie lorsque cela est approprié ([chapitre 10][ch10]<!-- ignore -->)
- Écrire des tests ([chapitre 11][ch11]<!-- ignore -->)

Nous présenterons aussi brièvement les fermetures, les itérateurs et les objets de trait, que les [chapitres 13][ch13]<!-- ignore --> et [18][ch18]<!-- ignore --> examineront en détail.

[ch7]: ch07-00-managing-growing-projects-with-packages-crates-and-modules.html
[ch8]: ch08-00-common-collections.html
[ch9]: ch09-00-error-handling.html
[ch10]: ch10-00-generics.html
[ch11]: ch11-00-testing.html
[ch13]: ch13-00-functional-features.html
[ch18]: ch18-00-oop.html