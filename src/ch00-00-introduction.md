# Introduction

> Remarque : Cette édition du livre est identique à [The Rust Programming
> Language][nsprust] disponible en version imprimée et en format ebook chez [No Starch
> Press][nsp].

[nsprust]: https://nostarch.com/rust-programming-language-3rd-edition
[nsp]: https://nostarch.com/

Bienvenue dans _The Rust Programming Language_, un livre d'introduction sur Rust.
Le langage de programmation Rust vous aide à écrire des logiciels plus rapides et plus fiables.
L’ergonomie de haut niveau et le contrôle de bas niveau sont souvent en conflit dans la conception des langages de programmation ; Rust remet en question ce conflit. En équilibrant une capacité technique puissante et une grande expérience développeur, Rust vous offre l’option de contrôler des détails bas niveau (comme l’utilisation de la mémoire) sans tous les tracas traditionnellement associés à un tel contrôle.

## Pour Qui Rust Est-Il Destiné

Rust est idéal pour de nombreuses personnes pour diverses raisons. Examinons quelques-uns des groupes les plus importants.

### Équipes de Développeurs

Rust s'avère être un outil productif pour la collaboration entre de grandes équipes de
développeurs ayant des niveaux de connaissance en programmation système variés. Le code bas niveau est sujet à divers bogues subtils, qui, dans la plupart des autres langages, ne peuvent être repérés qu'à travers des tests approfondis et une révision de code attentive par des développeurs expérimentés. En Rust, le compilateur joue un rôle de gardien en refusant de compiler du code contenant ces bogues insaisissables, y compris les bogues de concurrence. En travaillant aux côtés du compilateur, l'équipe peut se concentrer sur la logique du programme plutôt que de traquer des bogues.

Rust apporte également des outils de développeur contemporains au monde de la programmation système :

- Cargo, le gestionnaire de dépendances et outil de build inclus, rend l’ajout,
  la compilation et la gestion des dépendances indolores et cohérentes à travers l'écosystème Rust.
- L'outil de formatage `rustfmt` garantit un style de code cohérent entre
  les développeurs.
- Le Rust Language Server alimente l'intégration de l'environnement de développement intégré (IDE) pour l'achèvement de code et les messages d'erreur en ligne.

En utilisant ces outils et d'autres dans l'écosystème Rust, les développeurs peuvent être
productifs tout en écrivant du code au niveau des systèmes.

### Étudiants

Rust est destiné aux étudiants et à ceux qui s'intéressent à l'apprentissage des concepts système. Grâce à Rust, de nombreuses personnes ont appris des sujets comme le développement de systèmes d'exploitation. La communauté est très accueillante et heureuse de répondre aux questions des étudiants. Grâce à des efforts comme ce livre, les équipes Rust souhaitent rendre les concepts systèmes plus accessibles à un plus grand nombre de personnes, en particulier à celles qui découvrent la programmation.

### Entreprises

Des centaines d'entreprises, grandes et petites, utilisent Rust en production pour une variété de tâches, y compris des outils en ligne de commande, des services web, des outils DevOps, des dispositifs embarqués, l'analyse et le transcodage audio et vidéo, les cryptomonnaies, la bioinformatique, les moteurs de recherche, les applications Internet des Objets, l'apprentissage automatique, et même de grandes parties du navigateur web Firefox.

### Développeurs Open Source

Rust est pour les personnes qui souhaitent construire le langage de programmation Rust, la communauté, les outils pour développeurs et les bibliothèques. Nous serions ravis que vous contribuiez au langage Rust.

### Personnes Qui Valorisent Vitesse et Stabilité

Rust est pour les personnes qui recherchent la vitesse et la stabilité dans un langage. Par vitesse, nous entendons à la fois la rapidité d'exécution du code Rust et la vitesse à laquelle Rust vous permet d'écrire des programmes. Les vérifications du compilateur de Rust garantissent la stabilité lors de l'ajout de fonctionnalités et du refactoring. Cela contraste avec le code hérité fragile dans des langages sans ces vérifications, que les développeurs évitent souvent de modifier. En visant des abstractions sans coût—des fonctionnalités de haut niveau qui se compilent en code de bas niveau aussi rapidement que du code écrit manuellement—Rust s'efforce de faire en sorte que le code sûr soit également rapide.

Le langage Rust espère soutenir de nombreux autres utilisateurs ; ceux mentionnés ici ne sont que quelques-uns des plus grands acteurs. Dans l'ensemble, la plus grande ambition de Rust est d'éliminer les compromis que les programmeurs ont acceptés depuis des décennies en offrant sécurité _et_ productivité, vitesse _et_ ergonomie. Essayez Rust et voyez si ses choix fonctionnent pour vous.

## Pour Qui Ce Livre Est-Il Destiné

Ce livre suppose que vous avez déjà écrit du code dans un autre langage de programmation, mais il ne fait aucune supposition sur lequel. Nous avons essayé de rendre le matériel facilement accessible à ceux provenant d'une grande variété de parcours en programmation. Nous ne passons pas beaucoup de temps à parler de ce qu'est la programmation _ou_ comment y penser. Si vous êtes complètement nouveau en programmation, il serait préférable de lire un livre qui fournit spécifiquement une introduction à la programmation.

## Comment Utiliser Ce Livre

En général, ce livre suppose que vous le lisez séquentiellement, de l’avant vers l’arrière. Les chapitres suivants s'appuient sur des concepts des chapitres antérieurs, et les chapitres précédents peuvent ne pas approfondir les détails d'un sujet particulier, mais reviendront sur le sujet dans un chapitre ultérieur.

Vous trouverez deux types de chapitres dans ce livre : des chapitres conceptuels et des chapitres de projet. Dans les chapitres conceptuels, vous apprendrez un aspect de Rust. Dans les chapitres de projet, nous construirons de petits programmes ensemble, en appliquant ce que vous avez appris jusqu'à présent. Le Chapitre 2, le Chapitre 12 et le Chapitre 21 sont des chapitres de projet ; les autres sont des chapitres conceptuels.

**Le Chapitre 1** explique comment installer Rust, comment écrire un programme "Hello, world !" et comment utiliser Cargo, le gestionnaire de paquets et outil de build de Rust. **Le Chapitre 2** est une introduction pratique à l'écriture d'un programme en Rust, vous faisant construire un jeu de devinette de nombres. Ici, nous couvrons des concepts à un haut niveau, et des chapitres ultérieurs fourniront des détails supplémentaires. Si vous souhaitez vous plonger directement dans le code, le Chapitre 2 est fait pour cela. Si vous êtes un apprenant particulièrement minutieux qui préfère apprendre chaque détail avant de passer au suivant, vous pourriez vouloir sauter le Chapitre 2 et aller directement au **Chapitre 3**, qui couvre des fonctionnalités de Rust similaires à celles d'autres langages de programmation ; ensuite, vous pourrez revenir au Chapitre 2 lorsque vous souhaiterez travailler sur un projet en appliquant les détails que vous avez appris.

Dans **Le Chapitre 4**, vous apprendrez le système de propriété de Rust. **Le Chapitre 5** discute des structures et des méthodes. **Le Chapitre 6** couvre les énumérations, les expressions `match` et les constructions de flux de contrôle `if let` et `let...else`. Vous utiliserez des structures et des énumérations pour créer des types personnalisés.

Dans **Le Chapitre 7**, vous apprendrez le système de modules de Rust et les règles de confidentialité pour organiser votre code et son interface de programmation d'application (API) publique. **Le Chapitre 8** discute de certaines structures de données de collection courantes que la bibliothèque standard fournit : vecteurs, chaînes de caractères et mappages de hachage. **Le Chapitre 9** explore la philosophie et les techniques de gestion des erreurs de Rust.

**Le Chapitre 10** se penche sur les génériques, les traits et les durées de vie, qui vous donnent le pouvoir de définir du code qui s'applique à plusieurs types. **Le Chapitre 11** est entièrement consacré aux tests, qui, même avec les garanties de sécurité de Rust, sont nécessaires pour s'assurer que la logique de votre programme est correcte. Dans **Le Chapitre 12**, nous construirons notre propre implémentation d'un sous-ensemble de fonctionnalités de l'outil en ligne de commande `grep` qui recherche du texte dans des fichiers. Pour cela, nous utiliserons de nombreux concepts discutés dans les chapitres précédents.

**Le Chapitre 13** explore les fermetures et les itérateurs : des fonctionnalités de Rust issues des langages de programmation fonctionnels. Dans **Le Chapitre 14**, nous examinerons Cargo plus en profondeur et parlerons des meilleures pratiques pour partager vos bibliothèques avec d'autres. **Le Chapitre 15** discute des pointeurs intelligents que la bibliothèque standard fournit et des traits qui permettent leur fonctionnement.

Dans **Le Chapitre 16**, nous passerons en revue différents modèles de programmation concurrente et parlerons de la façon dont Rust vous aide à programmer plusieurs threads sans crainte. Dans **Le Chapitre 17**, nous construirons là-dessus en explorant la syntaxe async et await de Rust, ainsi que les tâches, les promesses (futures) et les flux, et le modèle de concurrence léger qu’elles permettent.

**Le Chapitre 18** examine comment les idiomes Rust se comparent aux principes de programmation orientée objet que vous pourriez connaître. **Le Chapitre 19** est une référence sur les motifs et la correspondance de motifs, qui sont des moyens puissants d'exprimer des idées dans les programmes Rust. **Le Chapitre 20** contient un assortiment de sujets avancés d'intérêt, y compris Rust non sécurisé, les macros, et plus sur les durées de vie, les traits, les types, les fonctions et les fermetures.

Dans **Le Chapitre 21**, nous terminerons un projet dans lequel nous implémenterons un serveur web multithreadé de bas niveau !

Enfin, quelques annexes contiennent des informations utiles sur le langage dans un format plus de référence. **L'Annexe A** couvre les mots-clés de Rust, **l'Annexe B** couvre les opérateurs et symboles de Rust, **l'Annexe C** couvre les traits dérivables fournis par la bibliothèque standard, **l'Annexe D** couvre quelques outils de développement utiles, et **l'Annexe E** explique les éditions de Rust. Dans **l'Annexe F**, vous pouvez trouver des traductions du livre, et dans **l'Annexe G**, nous aborderons la façon dont Rust est fabriqué et ce qu'est Rust nightly.

Il n'y a pas de mauvaise façon de lire ce livre : Si vous souhaitez avancer, allez-y !
Vous devrez peut-être revenir aux chapitres précédents si vous éprouvez des confusions. Mais faites ce qui fonctionne pour vous.

<span id="ferris"></span>

Une partie importante de l'apprentissage de Rust consiste à apprendre à lire les messages d'erreur affichés par le compilateur : ceux-ci vous guideront vers un code fonctionnel. Nous fournirons donc de nombreux exemples qui ne se compilent pas avec le message d'erreur que le compilateur affichera dans chaque situation. Sachez que si vous entrez et exécutez un exemple aléatoire, il peut ne pas se compiler ! Assurez-vous de lire le texte environnant pour voir si l'exemple que vous essayez d'exécuter est censé produire une erreur. Dans la plupart des situations, nous vous guiderons vers la version correcte de tout code qui ne se compile pas. Ferris vous aidera également à distinguer le code qui n'est pas censé fonctionner :

| Ferris                                                                                                           | Signification                                   |
| ---------------------------------------------------------------------------------------------------------------- | ----------------------------------------------- |
| <img src="img/ferris/does_not_compile.svg" class="ferris-explain" alt="Ferris avec un point d'interrogation"/>            | Ce code ne se compile pas !                     |
| <img src="img/ferris/panics.svg" class="ferris-explain" alt="Ferris levant les mains"/>                   | Ce code provoque un panic !                     |
| <img src="img/ferris/not_desired_behavior.svg" class="ferris-explain" alt="Ferris avec une patte levée, haussant les épaules"/> | Ce code ne produit pas le comportement souhaité. |

Dans la plupart des situations, nous vous guiderons vers la version correcte de tout code qui ne se compile pas.

## Code Source

Les fichiers source à partir desquels ce livre est généré peuvent être trouvés sur
[GitHub][book].

[book]: https://github.com/rust-lang/book/tree/main/src