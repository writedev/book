<!-- Anciennes en-têtes. Ne pas supprimer ou les liens peuvent se briser. -->

<a id="managing-growing-projects-with-packages-crates-and-modules"></a>

# Packages, Caisses et Modules

À mesure que vous écrivez de grands programmes, l'organisation de votre code deviendra de plus en plus importante. En regroupant des fonctionnalités connexes et en séparant le code avec des fonctionnalités distinctes, vous clarifierez où trouver le code qui implémente une fonctionnalité particulière et où aller pour modifier le fonctionnement d'une fonctionnalité.

Les programmes que nous avons écrits jusqu'à présent étaient dans un seul module dans un seul fichier. À mesure qu'un projet grandit, vous devez organiser le code en le répartissant sur plusieurs modules puis plusieurs fichiers. Un package peut contenir plusieurs caisses binaires et éventuellement une librairie. À mesure qu'un package se développe, vous pouvez extraire des parties dans des caisses séparées qui deviennent des dépendances externes. Ce chapitre couvre toutes ces techniques. Pour les très grands projets composés d'un ensemble de packages interconnectés qui évoluent ensemble, Cargo fournit des espaces de travail, que nous aborderons dans [“Espaces de travail Cargo”][workspaces]<!-- ignore --> au Chapitre 14.

Nous discuterons également de l'encapsulation des détails d'implémentation, ce qui vous permet de réutiliser le code à un niveau supérieur : Une fois que vous avez implémenté une opération, d'autres codes peuvent appeler votre code via son interface publique sans avoir à savoir comment l'implémentation fonctionne. La manière dont vous écrivez le code définit quelles parties sont publiques pour que d'autres codes les utilisent et quelles parties sont des détails d'implémentation privés que vous vous réservez le droit de modifier. C'est une autre façon de limiter la quantité de détails que vous devez garder en tête.

Un concept connexe est la portée : Le contexte imbriqué dans lequel le code est écrit a un ensemble de noms qui sont définis comme "dans la portée". Lors de la lecture, de l'écriture et de la compilation du code, les programmeurs et les compilateurs doivent savoir si un nom particulier à un endroit particulier fait référence à une variable, une fonction, une structure, un énuméré, un module, une constante ou un autre élément et ce que cet élément signifie. Vous pouvez créer des portées et modifier quels noms sont dans ou hors de portée. Vous ne pouvez pas avoir deux éléments avec le même nom dans la même portée ; des outils sont disponibles pour résoudre les conflits de nom.

Rust dispose de plusieurs fonctionnalités qui vous permettent de gérer l'organisation de votre code, y compris quels détails sont exposés, quels détails sont privés et quels noms sont dans chaque portée dans vos programmes. Ces fonctionnalités, parfois collectivement appelées le _système de modules_, incluent :

* **Packages** : Une fonctionnalité Cargo qui vous permet de construire, tester et partager des caisses
* **Caisses** : Un arbre de modules qui produit une librairie ou un exécutable
* **Modules et utilisation** : Vous permettent de contrôler l'organisation, la portée et la confidentialité des chemins
* **Chemins** : Un moyen de nommer un élément, comme une structure, une fonction ou un module

Dans ce chapitre, nous aborderons toutes ces fonctionnalités, discuterons de leurs interactions et expliquerons comment les utiliser pour gérer la portée. À la fin, vous devriez avoir une solide compréhension du système de modules et être capable de travailler avec des portées comme un pro !

[workspaces]: ch14-03-cargo-workspaces.html