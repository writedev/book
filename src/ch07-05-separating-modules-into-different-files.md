## Séparation des Modules en Fichiers Différents

Jusqu'à présent, tous les exemples de ce chapitre définissaient plusieurs modules dans un seul fichier. Lorsque les modules deviennent volumineux, vous pourriez vouloir déplacer leurs définitions dans un fichier séparé pour faciliter la navigation dans le code.

Par exemple, commençons par le code de l'Annonce 7-17 qui avait plusieurs modules de restaurant. Nous allons extraire les modules dans des fichiers plutôt que d'avoir tous les modules définis dans le fichier racine du crate. Dans ce cas, le fichier racine du crate est _src/lib.rs_, mais cette procédure fonctionne également avec des crates binaires dont le fichier racine est _src/main.rs_.

Tout d'abord, nous allons extraire le module `front_of_house` dans son propre fichier. Supprimez le code à l'intérieur des accolades pour le module `front_of_house`, en laissant uniquement la déclaration `mod front_of_house;`, de sorte que _src/lib.rs_ contienne le code montré dans l'Annonce 7-21. Notez que cela ne compilera pas tant que nous n'avons pas créé le fichier _src/front_of_house.rs_ comme montré dans l'Annonce 7-22.

<Annonce numéro="7-21" nom-du-fichier="src/lib.rs" légende="Déclaration du module `front_of_house` dont le corps sera dans *src/front_of_house.rs*">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-21-and-22/src/lib.rs}}
```

</Annonce>

Ensuite, placez le code qui était dans les accolades dans un nouveau fichier nommé _src/front_of_house.rs_, comme montré dans l'Annonce 7-22. Le compilateur sait chercher dans ce fichier, car il a rencontré la déclaration du module dans le fichier racine du crate avec le nom `front_of_house`.

<Annonce numéro="7-22" nom-du-fichier="src/front_of_house.rs" légende="Définitions à l'intérieur du module `front_of_house` dans *src/front_of_house.rs*">

```rust,ignore
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-21-and-22/src/front_of_house.rs}}
```

</Annonce>

Notez que vous n'avez besoin de charger un fichier utilisant une déclaration `mod` qu'une seule fois dans votre arbre de modules. Une fois que le compilateur sait que le fichier fait partie du projet (et connaît l'emplacement dans l'arbre de modules où se trouve le code en raison de l'emplacement de la déclaration `mod`), d'autres fichiers dans votre projet doivent faire référence au code du fichier chargé en utilisant un chemin vers l'endroit où il a été déclaré, comme couvert dans la section ["Chemins pour se référer à un élément dans l'arbre de modules"] [paths]<!-- ignore -->. En d'autres termes, `mod` n'est pas une opération "include" que vous avez pu voir dans d'autres langages de programmation.

Ensuite, nous allons extraire le module `hosting` dans son propre fichier. Le processus est un peu différent car `hosting` est un sous-module de `front_of_house`, et non du module racine. Nous allons placer le fichier pour `hosting` dans un nouveau répertoire qui sera nommé d'après ses ancêtres dans l'arbre de modules, dans ce cas _src/front_of_house_.

Pour commencer à déplacer `hosting`, nous modifions _src/front_of_house.rs_ pour ne contenir que la déclaration du module `hosting` :

<Annonce nom-du-fichier="src/front_of_house.rs">

```rust,ignore
{{#rustdoc_include ../listings/ch07-managing-growing-projects/no-listing-02-extracting-hosting/src/front_of_house.rs}}
```

</Annonce>

Ensuite, nous créons un répertoire _src/front_of_house_ et un fichier _hosting.rs_ pour contenir les définitions faites dans le module `hosting` :

<Annonce nom-du-fichier="src/front_of_house/hosting.rs">

```rust,ignore
{{#rustdoc_include ../listings/ch07-managing-growing-projects/no-listing-02-extracting-hosting/src/front_of_house/hosting.rs}}
```

</Annonce>

Si nous mettions plutôt _hosting.rs_ dans le répertoire _src_, le compilateur s'attendrait à ce que le code de _hosting.rs_ soit dans un module `hosting` déclaré dans le fichier racine du crate et non déclaré comme un enfant du module `front_of_house`. Les règles du compilateur concernant les fichiers à vérifier pour le code des modules signifient que les répertoires et fichiers correspondent plus étroitement à l'arbre des modules.

> ### Chemins de Fichiers Alternatifs
>
> Jusqu'à présent, nous avons couvert les chemins de fichiers les plus idiomatiques que le compilateur Rust utilise, mais Rust prend également en charge un ancien style de chemins de fichiers. Pour un module nommé `front_of_house` déclaré dans le fichier racine du crate, le compilateur cherchera le code du module dans :
>
> - _src/front_of_house.rs_ (ce que nous avons couvert)
> - _src/front_of_house/mod.rs_ (ancien style, chemin encore pris en charge)
>
> Pour un module nommé `hosting` qui est un sous-module de `front_of_house`, le compilateur cherchera le code du module dans :
>
> - _src/front_of_house/hosting.rs_ (ce que nous avons couvert)
> - _src/front_of_house/hosting/mod.rs_ (ancien style, chemin encore pris en charge)
>
> Si vous utilisez les deux styles pour le même module, vous obtiendrez une erreur de compilation. Utiliser un mélange des deux styles pour différents modules dans le même projet est autorisé mais pourrait être déroutant pour ceux qui naviguent dans votre projet.
>
> L'inconvénient principal du style qui utilise des fichiers nommés _mod.rs_ est que votre projet peut finir par avoir de nombreux fichiers nommés _mod.rs_, ce qui peut devenir déroutant lorsque vous les avez ouverts dans votre éditeur en même temps.

Nous avons déplacé le code de chaque module dans un fichier séparé, et l'arbre des modules reste le même. Les appels de fonction dans `eat_at_restaurant` fonctionneront sans aucune modification, même si les définitions se trouvent dans des fichiers différents. Cette technique vous permet de déplacer des modules dans de nouveaux fichiers à mesure qu'ils grandissent en taille.

Notez que l'instruction `pub use crate::front_of_house::hosting` dans _src/lib.rs_ n'a également pas changé, et l'instruction `use` n'a aucun impact sur les fichiers compilés comme faisant partie du crate. Le mot-clé `mod` déclare des modules, et Rust cherche dans un fichier portant le même nom que le module le code qui va dans ce module.

## Résumé

Rust vous permet de diviser un paquet en plusieurs crates et une crate en modules afin que vous puissiez faire référence à des éléments définis dans un module depuis un autre module. Vous pouvez le faire en spécifiant des chemins absolus ou relatifs. Ces chemins peuvent être mis dans le scope avec une déclaration `use` afin que vous puissiez utiliser un chemin plus court pour plusieurs utilisations de l'élément dans ce scope. Le code des modules est privé par défaut, mais vous pouvez rendre des définitions publiques en ajoutant le mot-clé `pub`.

Dans le prochain chapitre, nous examinerons certaines structures de données de collection dans la bibliothèque standard que vous pouvez utiliser dans votre code soigneusement organisé.

[paths]: ch07-03-paths-for-referring-to-an-item-in-the-module-tree.html