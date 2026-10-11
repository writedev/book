# Collections courantes

La bibliothèque standard de Rust inclut un certain nombre de structures de données très utiles appelées _collections_. La plupart des autres types de données représentent une valeur spécifique, mais les collections peuvent en contenir plusieurs. Contrairement aux types intégrés tableau et tuple, les données pointées par ces collections sont stockées sur le tas, ce qui signifie que leur taille n’a pas besoin d’être connue à la compilation et qu’elles peuvent grandir ou rétrécir pendant l’exécution du programme. Chaque type de collection possède des capacités et des coûts différents, et choisir celle qui convient à votre situation est une compétence que vous développerez avec le temps. Dans ce chapitre, nous parlerons de trois collections très utilisées dans les programmes Rust :

- Un _vecteur_ vous permet de stocker un nombre variable de valeurs côte à côte.
- Une _chaîne de caractères_ est une collection de caractères. Nous avons déjà mentionné le type `String`, mais dans ce chapitre, nous l’étudierons en détail.
- Une _table de hachage_ vous permet d’associer une valeur à une clé spécifique. Il s’agit d’une implémentation particulière de la structure de données plus générale appelée _map_.

Pour en savoir plus sur les autres types de collections fournis par la bibliothèque standard, consultez [la documentation][collections].

Nous verrons comment créer et mettre à jour des vecteurs, des chaînes de caractères et des tables de hachage, ainsi que ce qui rend chacune d’elles particulière.

[collections]: ../std/collections/index.html