# Fondamentaux de la programmation asynchrone : Async, Await, Futures et Streams

De nombreuses opérations que nous demandons à l'ordinateur d'effectuer peuvent prendre du temps à se terminer. Ce serait bien si nous pouvions faire quelque chose d'autre pendant que nous attendons que ces processus longs se complètent. Les ordinateurs modernes offrent deux techniques pour travailler sur plusieurs opérations à la fois : le parallélisme et la concurrence. Cependant, la logique de nos programmes est écrite de manière principalement linéaire. Nous aimerions pouvoir spécifier les opérations qu'un programme doit effectuer et les points auxquels une fonction pourrait se mettre en pause et qu'une autre partie du programme pourrait s'exécuter à la place, sans avoir besoin de spécifier à l'avance l'ordre et la manière exacts dont chaque morceau de code doit s'exécuter. La _programmation asynchrone_ est une abstraction qui nous permet d'exprimer notre code en termes de points de pause potentiels et de résultats éventuels, tout en s'occupant des détails de coordination pour nous.

Ce chapitre s'appuie sur l'utilisation des threads pour le parallélisme et la concurrence présentée dans le chapitre 16 en introduisant une approche alternative pour écrire du code : les futures, les streams et la syntaxe `async` et `await` de Rust, qui nous permettent d'exprimer comment les opérations peuvent être asynchrones, ainsi que les bibliothèques tierces qui mettent en œuvre des environnements d'exécution asynchrone : du code qui gère et coordonne l'exécution des opérations asynchrones.

Considérons un exemple. Supposons que vous exportiez une vidéo que vous avez créée lors d'une célébration familiale, une opération qui peut prendre de quelques minutes à quelques heures. L'exportation de la vidéo utilisera autant de puissance CPU et GPU que possible. Si vous n'aviez qu'un seul cœur de CPU et que votre système d'exploitation ne mettait pas en pause cette exportation jusqu'à ce qu'elle soit terminée — c'est-à-dire s'il exécutait l'exportation _synchroniquement_ — vous ne pourriez rien faire d'autre sur votre ordinateur pendant que cette tâche s'exécute. Ce serait une expérience assez frustrante. Heureusement, le système d'exploitation de votre ordinateur peut, et le fait, interrompre invisiblement l'exportation souvent assez pour vous permettre d'accomplir d'autres tâches simultanément.

Maintenant, disons que vous téléchargez une vidéo partagée par quelqu'un d'autre, ce qui peut également prendre du temps mais n'utilise pas autant de temps CPU. Dans ce cas, le CPU doit attendre que les données arrivent du réseau. Bien que vous puissiez commencer à lire les données une fois qu'elles commencent à arriver, il peut falloir un certain temps avant que toutes soient présentes. Même une fois toutes les données présentes, si la vidéo est assez grande, il pourrait falloir au moins une ou deux secondes pour la charger complètement. Cela peut ne pas sembler beaucoup, mais c'est une période très longue pour un processeur moderne, qui peut effectuer des milliards d'opérations par seconde. Encore une fois, votre système d'exploitation interrompra invisiblement votre programme pour permettre au CPU d'effectuer d'autres travaux en attendant que l'appel réseau se termine.

L'exportation vidéo est un exemple d'une opération _limitée par le CPU_ ou _limitée par le calcul_. Elle est limitée par la vitesse de traitement des données de l'ordinateur au sein du CPU ou du GPU, et par la quantité de cette vitesse qui peut être dédiée à l'opération. Le téléchargement de la vidéo est un exemple d'une opération _limitée par I/O_, car elle est limitée par la vitesse des _entrées et sorties_ de l'ordinateur ; elle ne peut aller aussi vite que les données peuvent être envoyées à travers le réseau.

Dans ces deux exemples, les interruptions invisibles du système d'exploitation fournissent une forme de concurrence. Cette concurrence se produit uniquement au niveau de l'ensemble du programme, cependant : le système d'exploitation interrompt un programme pour permettre à d'autres programmes d'accomplir du travail. Dans de nombreux cas, parce que nous comprenons nos programmes à un niveau beaucoup plus granulaire que le fait le système d'exploitation, nous pouvons repérer des opportunités de concurrence que le système d'exploitation ne peut pas voir.

Par exemple, si nous construisons un outil pour gérer les téléchargements de fichiers, nous devrions être capables d'écrire notre programme de sorte qu'un téléchargement ne bloque pas l'interface utilisateur, et que les utilisateurs puissent démarrer plusieurs téléchargements en même temps. Cependant, de nombreuses API de systèmes d'exploitation pour interagir avec le réseau sont _bloquantes_ ; c'est-à-dire qu'elles bloquent le progrès du programme jusqu'à ce que les données qu'elles traitent soient complètement prêtes.

> Remarque : C'est ainsi que fonctionnent _la plupart_ des appels de fonction, si vous y réfléchissez. Cependant, le terme _bloquant_ est généralement réservé aux appels de fonction qui interagissent avec des fichiers, le réseau ou d'autres ressources sur l'ordinateur, car ce sont les cas où un programme individuel bénéficierait de l'opération étant _non_-bloquante.

Nous pourrions éviter de bloquer notre thread principal en lançant un thread dédié pour télécharger chaque fichier. Cependant, le surcoût des ressources système utilisées par ces threads deviendrait éventuellement un problème. Il serait préférable que l'appel ne bloque pas en premier lieu, et que nous puissions plutôt définir un nombre de tâches que nous aimerions que notre programme achève et permettre au runtime de choisir le meilleur ordre et la manière de les exécuter.

C'est exactement ce que l'abstraction _async_ (abréviation de _asynchrone_) de Rust nous offre. Dans ce chapitre, vous apprendrez tout sur async alors que nous aborderons les sujets suivants :

- Comment utiliser la syntaxe `async` et `await` de Rust et exécuter des fonctions asynchrones avec un runtime
- Comment utiliser le modèle asynchrone pour résoudre certains des mêmes défis que nous avons examinés dans le chapitre 16
- Comment le multithreading et l'asynchrone offrent des solutions complémentaires que vous pouvez combiner dans de nombreux cas

Avant de voir comment async fonctionne en pratique, nous devons faire un détour pour discuter des différences entre le parallélisme et la concurrence.

## Parallélisme et Concurrence

Nous avons jusqu'à présent traité le parallélisme et la concurrence comme essentiellement interchangeables. Maintenant, nous devons les distinguer plus précisément, car les différences apparaîtront lorsque nous commencerons à travailler.

Considérons les différentes manières dont une équipe pourrait répartir le travail sur un projet logiciel. Vous pourriez attribuer à un seul membre plusieurs tâches, assigner à chaque membre une tâche, ou utiliser un mélange des deux approches.

Lorsqu'un individu travaille sur plusieurs tâches différentes avant que l'une d'elles ne soit complétée, c'est de la _concurrence_. Une façon d'implémenter la concurrence est similaire à avoir deux projets différents vérifiés sur votre ordinateur, et lorsque vous vous ennuyez ou restez bloqué sur un projet, vous passez à l'autre. Vous êtes juste une personne, donc vous ne pouvez pas progresser sur les deux tâches en même temps exactement, mais vous pouvez faire du multitâche, en progressant sur une à la fois en alternant entre elles (voir Figure 17-1).

<figure>

<img src="img/trpl17-01.svg" class="center" alt="Un diagramme avec des boîtes empilées étiquetées Tâche A et Tâche B, avec des losanges en elles représentant des sous-tâches. Des flèches pointent de A1 à B1, de B1 à A2, de A2 à B2, de B2 à A3, de A3 à A4, et de A4 à B3." />

<figcaption>Figure 17-1 : Un flux de travail concurrent, alternant entre la Tâche A et la Tâche B</figcaption>

</figure>

Lorsque l'équipe divise un groupe de tâches en faisant travailler chaque membre sur une tâche seule, c'est du _parallélisme_. Chaque personne de l'équipe peut progresser en même temps (voir Figure 17-2).

<figure>

<img src="img/trpl17-02.svg" class="center" alt="Un diagramme avec des boîtes empilées étiquetées Tâche A et Tâche B, avec des losanges en elles représentant des sous-tâches. Des flèches pointent de A1 à A2, A2 à A3, A3 à A4, B1 à B2, et B2 à B3. Aucune flèche ne traverse les cases pour la Tâche A et la Tâche B." />

<figcaption>Figure 17-2 : Un flux de travail parallèle, où le travail se fait sur la Tâche A et la Tâche B de manière indépendante</figcaption>

</figure>

Dans ces deux flux de travail, vous pourriez devoir coordonner entre différentes tâches. Peut-être pensiez-vous que la tâche assignée à une personne était totalement indépendante du travail des autres, mais elle nécessite en réalité qu'une autre personne de l'équipe termine sa tâche en premier. Une partie du travail pourrait être effectuée en parallèle, mais une autre partie était en réalité _série_: elle ne pouvait se faire qu'en série, une tâche après l'autre, comme dans la Figure 17-3.

<figure>

<img src="img/trpl17-03.svg" class="center" alt="Un diagramme avec des boîtes empilées étiquetées Tâche A et Tâche B, avec des losanges en elles représentant des sous-tâches. Dans la Tâche A, des flèches pointent de A1 à A2, de A2 à une paire de lignes verticales épaisses comme un symbole de « pause », et de ce symbole à A3. Dans la Tâche B, des flèches pointent de B1 à B2, de B2 à B3, de B3 à A3, et de B3 à B4." />

<figcaption>Figure 17-3 : Un flux de travail partiellement parallèle, où le travail se fait sur la Tâche A et la Tâche B indépendamment jusqu'à ce que Tâche A3 soit bloquée sur les résultats de Tâche B3.</figcaption>

</figure>

De même, vous pourriez réaliser que l'une de vos propres tâches dépend d'une autre de vos tâches. Maintenant, votre travail concurrent est également devenu sériel.

Le parallélisme et la concurrence peuvent également s'intersectionner. Si vous apprenez qu'un collègue est bloqué jusqu'à ce que vous terminiez l'une de vos tâches, vous vous concentrerez probablement tous vos efforts sur cette tâche pour « débloquer » votre collègue. Vous et votre collègue n'êtes plus capables de travailler en parallèle, et vous n'êtes également plus capables de travailler simultanément sur vos propres tâches.

Les mêmes dynamiques de base s'appliquent aux logiciels et au matériel. Sur une machine avec un seul cœur de CPU, le CPU ne peut effectuer qu'une seule opération à la fois, mais il peut néanmoins travailler de manière concurrente. En utilisant des outils tels que des threads, des processus et l'asynchrone, l'ordinateur peut mettre une activité en pause et passer à d'autres avant de revenir finalement à cette première activité. Sur une machine avec plusieurs cœurs de CPU, elle peut également effectuer un travail en parallèle. Un cœur peut effectuer une tâche pendant qu'un autre cœur en effectue une complètement distincte, et ces opérations se déroulent effectivement en même temps.

L'exécution de code asynchrone en Rust se fait généralement de manière concurrente. Selon le matériel, le système d'exploitation et l'environnement d'exécution asynchrone que nous utilisons (plus sur les environnements d'exécution asynchrones sous peu), cette concurrence peut également utiliser le parallélisme en arrière-plan.

Maintenant, explorons comment fonctionner la programmation asynchrone en Rust.