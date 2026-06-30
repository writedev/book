# Un projet I/O : Création d'un programme en ligne de commande

Ce chapitre est un récapitulatif des nombreuses compétences que vous avez acquises jusqu'à présent et une exploration de quelques autres fonctionnalités de la bibliothèque standard. Nous allons créer un outil en ligne de commande qui interagit avec l'entrée/sortie de fichiers et de la ligne de commande pour pratiquer certains concepts de Rust que vous maîtrisez maintenant.

La rapidité, la sécurité, la sortie binaire unique et la prise en charge multiplateforme de Rust en font un langage idéal pour créer des outils en ligne de commande, donc pour notre projet, nous allons créer notre propre version de l'outil de recherche en ligne de commande classique `grep` (**g**lobale recherche une **r**expression **e**xpression et **p**rint). Dans le cas d'utilisation le plus simple, `grep` recherche un fichier spécifié pour une chaîne spécifiée. Pour ce faire, `grep` prend en arguments un chemin de fichier et une chaîne. Ensuite, il lit le fichier, trouve les lignes de ce fichier qui contiennent l'argument chaîne, et imprime ces lignes.

En cours de route, nous montrerons comment faire en sorte que notre outil en ligne de commande utilise les fonctionnalités du terminal que de nombreux autres outils en ligne de commande utilisent. Nous lirons la valeur d'une variable d'environnement pour permettre à l'utilisateur de configurer le comportement de notre outil. Nous imprimerons également des messages d'erreur dans le flux de console d'erreur standard (`stderr`) plutôt que dans la sortie standard (`stdout`), afin que, par exemple, l'utilisateur puisse rediriger la sortie réussie vers un fichier tout en voyant encore les messages d'erreur à l'écran.

Un membre de la communauté Rust, Andrew Gallant, a déjà créé une version entièrement fonctionnelle et très rapide de `grep`, appelée `ripgrep`. En comparaison, notre version sera relativement simple, mais ce chapitre vous fournira certaines des connaissances de base nécessaires pour comprendre un projet réel tel que `ripgrep`.

Notre projet `grep` combinera un certain nombre de concepts que vous avez appris jusqu'à présent :

- Organisation du code ([Chapitre 7][ch7]<!-- ignore -->)
- Utilisation de vecteurs et de chaînes ([Chapitre 8][ch8]<!-- ignore -->)
- Gestion des erreurs ([Chapitre 9][ch9]<!-- ignore -->)
- Utilisation de traits et de durées de vie là où cela est approprié ([Chapitre 10][ch10]<!-- ignore -->)
- Rédaction de tests ([Chapitre 11][ch11]<!-- ignore -->)

Nous introduirons également brièvement les fermetures, les itérateurs et les objets de traits, qui seront couverts en détail dans les [Chapitre 13][ch13]<!-- ignore --> et [Chapitre 18][ch18]<!-- ignore -->.

[ch7]: ch07-00-managing-growing-projects-with-packages-crates-and-modules.html  
[ch8]: ch08-00-common-collections.html  
[ch9]: ch09-00-error-handling.html  
[ch10]: ch10-00-generics.html  
[ch11]: ch11-00-testing.html  
[ch13]: ch13-00-functional-features.html  
[ch18]: ch18-00-oop.html  