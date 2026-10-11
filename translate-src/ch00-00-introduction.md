# Introduction

> Remarque : cette édition du livre est identique à [The Rust Programming
> Language][nsprust], disponible en version imprimée et en ebook chez [No Starch
> Press][nsp].

[nsprust]: https://nostarch.com/rust-programming-language-3rd-edition
[nsp]: https://nostarch.com/

Bienvenue dans _Le langage de programmation Rust_, un livre d’introduction à Rust.
Le langage de programmation Rust vous aide à écrire des logiciels plus rapides et plus fiables.
Dans la conception des langages de programmation, l’ergonomie de haut niveau et le contrôle de bas niveau sont souvent incompatibles ; Rust remet en question cette opposition. En conciliant de puissantes capacités techniques et une excellente expérience de développement, Rust vous permet de contrôler les détails de bas niveau (comme l’utilisation de la mémoire) sans tous les tracas traditionnellement associés à ce contrôle.

## À qui s’adresse Rust

Rust convient idéalement à de nombreuses personnes, pour différentes raisons. Examinons quelques-uns des groupes les plus importants.

### Équipes de développeurs

Rust se révèle être un outil productif pour la collaboration au sein de grandes équipes de développeurs ayant des niveaux variés de connaissances en programmation système. Le code de bas niveau est sujet à diverses erreurs subtiles qui, dans la plupart des autres langages, ne peuvent être détectées qu’au moyen de tests approfondis et d’une révision minutieuse du code par des développeurs expérimentés. Dans Rust, le compilateur joue un rôle de gardien en refusant de compiler du code contenant ces erreurs difficiles à déceler, y compris les erreurs de concurrence. En travaillant aux côtés du compilateur, l’équipe peut consacrer son temps à la logique du programme plutôt qu’à traquer les erreurs.

Rust apporte également des outils de développement modernes au monde de la programmation système :

- Cargo, le gestionnaire de dépendances et l’outil de compilation inclus, facilite l’ajout, la compilation et la gestion des dépendances, de manière cohérente dans tout l’écosystème Rust.
- L’outil de formatage `rustfmt` assure un style de code cohérent entre les développeurs.
- Le serveur de langage Rust permet l’intégration aux environnements de développement intégrés (IDE), notamment pour la complétion de code et l’affichage de messages d’erreur en ligne.

Grâce à ces outils et à d’autres outils de l’écosystème Rust, les développeurs peuvent être productifs tout en écrivant du code système.

### Étudiants

Rust s’adresse aux étudiants et aux personnes qui souhaitent découvrir les concepts des systèmes. Grâce à Rust, de nombreuses personnes ont appris des sujets comme le développement de systèmes d’exploitation. La communauté est très accueillante et se fait un plaisir de répondre aux questions des étudiants. Avec des initiatives comme ce livre, les équipes Rust souhaitent rendre les concepts des systèmes plus accessibles à un plus grand nombre de personnes, en particulier aux personnes qui débutent en programmation.

### Entreprises

Des centaines d’entreprises, grandes et petites, utilisent Rust en production pour diverses tâches, notamment des outils en ligne de commande, des services web, des outils DevOps, des appareils embarqués, l’analyse et le transcodage audio et vidéo, les cryptomonnaies, la bio-informatique, les moteurs de recherche, les applications de l’Internet des objets, l’apprentissage automatique, ainsi que des parties importantes du navigateur web Firefox.

### Développeurs de logiciels libres

Rust s’adresse aux personnes qui souhaitent contribuer au langage de programmation Rust, à sa communauté, à ses outils de développement et à ses bibliothèques. Nous serions ravis de vous voir contribuer au langage Rust.

### Personnes qui accordent de l’importance à la vitesse et à la stabilité

Rust s’adresse aux personnes qui recherchent la vitesse et la stabilité dans un langage. Par vitesse, nous entendons à la fois la rapidité d’exécution du code Rust et la vitesse à laquelle Rust vous permet d’écrire des programmes. Les vérifications du compilateur Rust assurent la stabilité lors de l’ajout de fonctionnalités et de la refactorisation. Cela contraste avec le code hérité fragile des langages dépourvus de ces vérifications, que les développeurs hésitent souvent à modifier. En visant des abstractions à coût nul — des fonctionnalités de plus haut niveau compilées en code de plus bas niveau aussi rapide que du code écrit manuellement —, Rust s’efforce de rendre le code sûr également rapide.

Le langage Rust espère aussi répondre aux besoins de nombreux autres utilisateurs ; les groupes mentionnés ici ne sont que quelques-uns des principaux concernés. Dans l’ensemble, la plus grande ambition de Rust est d’éliminer les compromis que les programmeurs acceptent depuis des décennies en offrant à la fois sécurité _et_ productivité, vitesse _et_ ergonomie. Essayez Rust et voyez si ses choix vous conviennent.

## À qui s’adresse ce livre

Ce livre part du principe que vous avez déjà écrit du code dans un autre langage de programmation, mais ne présuppose pas lequel. Nous avons essayé de rendre le contenu largement accessible aux personnes ayant des expériences variées en programmation. Nous ne consacrons pas beaucoup de temps à expliquer ce qu’est la programmation _ou_ comment l’aborder. Si vous débutez complètement en programmation, vous aurez davantage intérêt à lire un livre qui en propose spécifiquement une introduction.

## Comment utiliser ce livre

En règle générale, ce livre part du principe que vous le lisez dans l’ordre, du début à la fin. Les chapitres suivants s’appuient sur les concepts des chapitres précédents, et les premiers chapitres peuvent ne pas approfondir certains sujets, qui seront repris dans un chapitre ultérieur.

Ce livre comporte deux types de chapitres : les chapitres conceptuels et les chapitres consacrés à des projets. Dans les chapitres conceptuels, vous découvrirez un aspect de Rust. Dans les chapitres consacrés à des projets, nous créerons ensemble de petits programmes en mettant en pratique ce que vous aurez appris jusque-là. Les chapitres 2, 12 et 21 sont consacrés à des projets ; les autres sont conceptuels.

**Le chapitre 1** explique comment installer Rust, écrire un programme « Hello, world! » et utiliser Cargo, le gestionnaire de paquets et l’outil de compilation de Rust. **Le chapitre 2** est une introduction pratique à l’écriture d’un programme en Rust : vous y créerez un jeu de devinettes. Nous y présentons les concepts à un niveau général, et les chapitres suivants apporteront davantage de détails. Si vous souhaitez vous lancer tout de suite, c’est le chapitre 2 qu’il vous faut. Si vous êtes particulièrement méticuleux et préférez apprendre chaque détail avant de passer au suivant, vous pouvez sauter le chapitre 2 et passer directement au **chapitre 3**, qui présente les fonctionnalités de Rust similaires à celles d’autres langages de programmation ; vous pourrez ensuite revenir au chapitre 2 lorsque vous souhaiterez réaliser un projet mettant en pratique les détails appris.

Au **chapitre 4**, vous découvrirez le système de propriété de Rust. Le **chapitre 5** traite des structures et des méthodes. Le **chapitre 6** aborde les énumérations, les expressions `match` et les constructions de contrôle de flux `if let` et `let...else`. Vous utiliserez les structures et les énumérations pour créer des types personnalisés.

Au **chapitre 7**, vous découvrirez le système de modules de Rust et les règles de confidentialité qui permettent d’organiser votre code et son interface de programmation applicative (API) publique. Le **chapitre 8** présente quelques structures de données de collections courantes fournies par la bibliothèque standard : les vecteurs, les chaînes de caractères et les tables de hachage. Le **chapitre 9** explore la philosophie et les techniques de gestion des erreurs de Rust.

Le **chapitre 10** approfondit les génériques, les traits et les durées de vie, qui vous permettent de définir du code s’appliquant à plusieurs types. Le **chapitre 11** est consacré aux tests, nécessaires pour garantir la justesse de la logique de votre programme, même avec les garanties de sécurité de Rust. Au **chapitre 12**, nous créerons notre propre implémentation d’un sous-ensemble des fonctionnalités de l’outil en ligne de commande `grep`, qui recherche du texte dans des fichiers. Pour cela, nous utiliserons plusieurs des concepts abordés dans les chapitres précédents.

Le **chapitre 13** explore les fermetures et les itérateurs, des fonctionnalités de Rust issues des langages de programmation fonctionnelle. Au **chapitre 14**, nous examinerons Cargo plus en détail et parlerons des bonnes pratiques pour partager vos bibliothèques avec d’autres personnes. Le **chapitre 15** aborde les pointeurs intelligents fournis par la bibliothèque standard et les traits qui leur permettent de fonctionner.

Au **chapitre 16**, nous passerons en revue différents modèles de programmation concurrente et verrons comment Rust vous aide à programmer sereinement avec plusieurs fils d’exécution. Au **chapitre 17**, nous poursuivrons en explorant la syntaxe async et await de Rust, ainsi que les tâches, les futures et les flux, et le modèle de concurrence léger qu’ils rendent possible.

Le **chapitre 18** examine les différences entre les idiomes de Rust et les principes de la programmation orientée objet que vous connaissez peut-être. Le **chapitre 19** est une référence sur les motifs et la mise en correspondance de motifs, qui sont des moyens puissants d’exprimer des idées dans les programmes Rust. Le **chapitre 20** rassemble de nombreux sujets avancés susceptibles de vous intéresser, notamment Rust non sécurisé, les macros et d’autres informations sur les durées de vie, les traits, les types, les fonctions et les fermetures.

Au **chapitre 21**, nous mènerons à bien un projet dans lequel nous implémenterons un serveur web multithread de bas niveau !

Enfin, certaines annexes présentent des informations utiles sur le langage dans un format proche d’un ouvrage de référence. **L’annexe A** traite des mots-clés de Rust, **l’annexe B** de ses opérateurs et symboles, **l’annexe C** des traits dérivables fournis par la bibliothèque standard, **l’annexe D** de quelques outils de développement utiles et **l’annexe E** des éditions de Rust. Dans **l’annexe F**, vous trouverez des traductions du livre, et dans **l’annexe G**, nous expliquerons comment Rust est conçu et ce qu’est Rust nightly.

Il n’y a pas de mauvaise façon de lire ce livre : si vous souhaitez passer à la suite, n’hésitez pas ! En cas de confusion, vous devrez peut-être revenir aux chapitres précédents. Mais faites ce qui vous convient.

<span id="ferris"></span>

Apprendre à lire les messages d’erreur affichés par le compilateur est une étape importante de l’apprentissage de Rust : ils vous guideront vers du code fonctionnel. Nous fournirons donc de nombreux exemples qui ne compilent pas, accompagnés du message d’erreur que le compilateur affichera dans chaque situation. Gardez à l’esprit que si vous saisissez et exécutez un exemple au hasard, il se peut qu’il ne compile pas ! Lisez attentivement le texte qui l’entoure pour savoir si l’exemple que vous essayez d’exécuter est censé provoquer une erreur. Dans la plupart des cas, nous vous présenterons la version correcte de tout code qui ne compile pas. Ferris vous aidera également à distinguer le code qui n’est pas censé fonctionner :

| Ferris                                                                                                           | Signification                                      |
| ---------------------------------------------------------------------------------------------------------------- | -------------------------------------------------- |
| <img src="img/ferris/does_not_compile.svg" class="ferris-explain" alt="Ferris avec un point d’interrogation"/>   | Ce code ne compile pas !                           |
| <img src="img/ferris/panics.svg" class="ferris-explain" alt="Ferris qui lève les mains au ciel"/>                | Ce code provoque une panique !                     |
| <img src="img/ferris/not_desired_behavior.svg" class="ferris-explain" alt="Ferris qui hausse les épaules, une pince levée"/> | Ce code ne produit pas le comportement souhaité. |

Dans la plupart des cas, nous vous présenterons la version correcte de tout code qui ne compile pas.

## Code source

Les fichiers sources à partir desquels ce livre est généré sont disponibles sur
[GitHub][book].

[book]: https://github.com/rust-lang/book/tree/main/src