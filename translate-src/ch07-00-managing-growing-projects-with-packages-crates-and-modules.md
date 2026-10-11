<!-- Old headings. Do not remove or links may break. -->

<a id="managing-growing-projects-with-packages-crates-and-modules"></a>

# Paquets, crates et modules

À mesure que vous écrivez des programmes volumineux, l’organisation de votre code devient de plus en plus importante. En regroupant les fonctionnalités apparentées et en séparant le code aux caractéristiques distinctes, vous clarifierez où trouver le code qui implémente une fonctionnalité particulière et où aller pour modifier son fonctionnement.

Jusqu’à présent, les programmes que nous avons écrits se trouvaient dans un seul module et un seul fichier. À mesure qu’un projet grandit, vous devriez organiser le code en le répartissant dans plusieurs modules, puis dans plusieurs fichiers. Un paquet peut contenir plusieurs crates binaires et, éventuellement, une crate de bibliothèque. À mesure qu’un paquet grandit, vous pouvez en extraire des parties dans des crates distinctes qui deviennent des dépendances externes. Ce chapitre aborde toutes ces techniques. Pour les très grands projets composés d’un ensemble de paquets interdépendants qui évoluent ensemble, Cargo fournit les espaces de travail, que nous aborderons dans [« Espaces de travail Cargo »][workspaces]<!-- ignore --> au chapitre 14.

Nous parlerons également de l’encapsulation des détails d’implémentation, qui vous permet de réutiliser le code à un niveau supérieur : une fois une opération implémentée, d’autres éléments de code peuvent appeler votre code via son interface publique sans avoir à savoir comment l’implémentation fonctionne. La façon dont vous écrivez votre code détermine quelles parties sont publiques et peuvent être utilisées par d’autres éléments de code, et quelles parties sont des détails d’implémentation privés que vous vous réservez le droit de modifier. C’est une autre façon de limiter la quantité de détails que vous devez garder à l’esprit.

La portée est un concept apparenté : le contexte imbriqué dans lequel le code est écrit possède un ensemble de noms définis comme étant « dans la portée ». Lorsqu’ils lisent, écrivent et compilent du code, les programmeurs et les compilateurs doivent savoir si un nom donné à un endroit donné désigne une variable, une fonction, une structure, une énumération, un module, une constante ou un autre élément, et ce que cet élément signifie. Vous pouvez créer des portées et modifier les noms qui sont ou ne sont pas dans la portée. Deux éléments ne peuvent pas porter le même nom dans une même portée ; des outils permettent de résoudre les conflits de noms.

Rust possède plusieurs fonctionnalités qui vous permettent de gérer l’organisation de votre code, notamment les détails exposés, les détails privés et les noms présents dans chaque portée de vos programmes. Ces fonctionnalités, parfois désignées collectivement sous le nom de _système de modules_, comprennent :

* **Paquets** : une fonctionnalité de Cargo qui vous permet de créer, tester et partager des crates
* **Crates** : un arbre de modules qui produit une bibliothèque ou un exécutable
* **Modules et `use`** : vous permettent de contrôler l’organisation, la portée et la confidentialité des chemins
* **Chemins** : une façon de nommer un élément, tel qu’une structure, une fonction ou un module

Dans ce chapitre, nous aborderons toutes ces fonctionnalités, expliquerons leurs interactions et verrons comment les utiliser pour gérer la portée. À la fin, vous devriez avoir une bonne compréhension du système de modules et être capable de gérer les portées comme un pro !

[workspaces]: ch14-03-cargo-workspaces.html