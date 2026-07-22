# Collections Courantes

La bibliothèque standard de Rust inclut un certain nombre de structures de données très utiles appelées _collections_. La plupart des autres types de données représentent une valeur spécifique, mais les collections peuvent contenir plusieurs valeurs. Contrairement aux types de tableau et de tuple intégrés, les données auxquelles ces collections font référence sont stockées dans le tas, ce qui signifie que la quantité de données n'a pas besoin d'être connue à la compilation et peut croître ou diminuer au fur et à mesure que le programme s'exécute. Chaque type de collection a des capacités et des coûts différents, et choisir une appropriée pour votre situation actuelle est une compétence que vous développerez avec le temps. Dans ce chapitre, nous discuterons de trois collections qui sont très souvent utilisées dans les programmes Rust :

- Un _vecteur_ vous permet de stocker un nombre variable de valeurs les unes à côté des autres.
- Une _chaîne_ est une collection de caractères. Nous avons mentionné le type `String` précédemment, mais dans ce chapitre, nous en parlerons en profondeur.
- Une _table de hachage_ vous permet d'associer une valeur à une clé spécifique. C'est une implémentation particulière de la structure de données plus générale appelée _carte_.

Pour en savoir plus sur les autres types de collections fournies par la bibliothèque standard, consultez [la documentation][collections].

Nous discuterons de la création et de la mise à jour des vecteurs, des chaînes et des tables de hachage, ainsi que de ce qui les rend chacune spéciale.

[collections]: ../std/collections/index.html