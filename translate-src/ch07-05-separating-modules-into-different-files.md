## Séparer les modules dans différents fichiers

Jusqu’à présent, tous les exemples de ce chapitre définissaient plusieurs modules dans un seul fichier.
Lorsque les modules deviennent volumineux, vous pouvez vouloir déplacer leurs définitions dans un fichier séparé afin de faciliter la navigation dans le code.

Par exemple, repartons du code de la Liste 7-17, qui contenait plusieurs modules de restaurant. Nous allons extraire les modules dans des fichiers plutôt que de les définir tous dans le fichier racine de la caisse. Dans ce cas, le fichier racine de la caisse est _src/lib.rs_, mais cette procédure fonctionne également avec les caisses binaires dont le fichier racine est _src/main.rs_.

Tout d’abord, nous allons extraire le module `front_of_house` dans son propre fichier. Supprimez le code à l’intérieur des accolades du module `front_of_house`, en ne laissant que la déclaration `mod front_of_house;`, afin que _src/lib.rs_ contienne le code présenté dans la Liste 7-21. Notez que le code ne compilera pas tant que nous n’aurons pas créé le fichier _src/front_of_house.rs_ de la Liste 7-22.

<Listing number="7-21" file-name="src/lib.rs" caption="Déclaration du module `front_of_house`, dont le contenu se trouvera dans *src/front_of_house.rs*">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-21-and-22/src/lib.rs}}
```

</Listing>

Ensuite, placez le code qui se trouvait entre les accolades dans un nouveau fichier nommé
_src/front_of_house.rs_, comme indiqué dans la Liste 7-22. Le compilateur sait qu’il doit consulter ce fichier parce qu’il a rencontré, dans la racine de la caisse, une déclaration de module nommée `front_of_house`.

<Listing number="7-22" file-name="src/front_of_house.rs" caption="Définitions à l’intérieur du module `front_of_house` dans *src/front_of_house.rs*">

```rust,ignore
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-21-and-22/src/front_of_house.rs}}
```

</Listing>

Notez qu’il suffit de charger un fichier à l’aide d’une déclaration `mod` _une seule fois_ dans votre arborescence de modules. Une fois que le compilateur sait que le fichier fait partie du projet (et sait où le code se trouve dans l’arborescence de modules, grâce à l’emplacement de l’instruction `mod`), les autres fichiers du projet doivent accéder au code chargé à l’aide d’un chemin vers l’endroit où il a été déclaré, comme expliqué dans la section [« Chemins pour faire référence à un élément de l’arborescence de modules »][paths]<!-- ignore -->. En d’autres termes, `mod` n’est _pas_ une opération « include » que vous avez peut-être rencontrée dans d’autres langages de programmation.

Ensuite, nous allons extraire le module `hosting` dans son propre fichier. La procédure est légèrement différente, car `hosting` est un module enfant de `front_of_house`, et non du module racine. Nous allons placer le fichier de `hosting` dans un nouveau répertoire nommé d’après ses ancêtres dans l’arborescence de modules, en l’occurrence _src/front_of_house_.

Pour commencer à déplacer `hosting`, modifions _src/front_of_house.rs_ afin qu’il ne contienne que la déclaration du module `hosting` :

<Listing file-name="src/front_of_house.rs">

```rust,ignore
{{#rustdoc_include ../listings/ch07-managing-growing-projects/no-listing-02-extracting-hosting/src/front_of_house.rs}}
```

</Listing>

Ensuite, créons un répertoire _src/front_of_house_ et un fichier _hosting.rs_ pour contenir les définitions du module `hosting` :

<Listing file-name="src/front_of_house/hosting.rs">

```rust,ignore
{{#rustdoc_include ../listings/ch07-managing-growing-projects/no-listing-02-extracting-hosting/src/front_of_house/hosting.rs}}
```

</Listing>

Si nous placions plutôt _hosting.rs_ dans le répertoire _src_, le compilateur s’attendrait à trouver le code de _hosting.rs_ dans un module `hosting` déclaré dans la racine de la caisse, et non dans un module enfant de `front_of_house`. Les règles du compilateur déterminant les fichiers à consulter pour trouver le code des modules font en sorte que les répertoires et les fichiers correspondent plus étroitement à l’arborescence de modules.

> ### Autres chemins de fichiers
>
> Jusqu’à présent, nous avons vu les chemins de fichiers les plus idiomatiques utilisés par le compilateur Rust, mais Rust prend également en charge un ancien style de chemin de fichier. Pour un module nommé `front_of_house` déclaré dans la racine de la caisse, le compilateur recherchera le code du module dans :
>
> - _src/front_of_house.rs_ (ce que nous avons vu)
> - _src/front_of_house/mod.rs_ (ancien style, chemin toujours pris en charge)
>
> Pour un module nommé `hosting`, qui est un sous-module de `front_of_house`, le compilateur recherchera le code du module dans :
>
> - _src/front_of_house/hosting.rs_ (ce que nous avons vu)
> - _src/front_of_house/hosting/mod.rs_ (ancien style, chemin toujours pris en charge)
>
> Si vous utilisez les deux styles pour un même module, vous obtiendrez une erreur du compilateur.
> Il est possible de mélanger les deux styles pour différents modules d’un même projet, mais cela peut dérouter les personnes qui parcourent votre projet.
>
> Le principal inconvénient du style qui utilise des fichiers nommés _mod.rs_ est que votre projet peut finir par contenir de nombreux fichiers nommés _mod.rs_, ce qui peut prêter à confusion lorsque vous les avez ouverts en même temps dans votre éditeur.

Nous avons déplacé le code de chaque module dans un fichier distinct, et l’arborescence de modules reste identique. Les appels de fonction dans `eat_at_restaurant` fonctionneront sans aucune modification, même si les définitions se trouvent dans des fichiers différents. Cette technique vous permet de déplacer des modules vers de nouveaux fichiers à mesure qu’ils grandissent.

Notez que l’instruction `pub use crate::front_of_house::hosting` dans
_src/lib.rs_ n’a pas changé non plus, et que `use` n’a aucune incidence sur les fichiers compilés dans le cadre de la caisse. Le mot-clé `mod` déclare des modules, et Rust recherche dans un fichier portant le même nom que le module le code qui doit y figurer.

## Résumé

Rust vous permet de diviser un paquet en plusieurs caisses, et une caisse en modules, afin de pouvoir faire référence, depuis un module, aux éléments définis dans un autre module. Vous pouvez le faire en indiquant des chemins absolus ou relatifs. Ces chemins peuvent être introduits dans la portée avec une instruction `use`, afin que vous puissiez utiliser un chemin plus court lorsque vous faites référence plusieurs fois à l’élément dans cette portée. Le code des modules est privé par défaut, mais vous pouvez rendre les définitions publiques en ajoutant le mot-clé `pub`.

Dans le chapitre suivant, nous examinerons certaines structures de données de collection de la bibliothèque standard que vous pouvez utiliser dans votre code bien organisé.

[paths]: ch07-03-paths-for-referring-to-an-item-in-the-module-tree.html