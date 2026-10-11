## Accepter des arguments de ligne de commande

Créons un nouveau projet avec, comme toujours, `cargo new`. Nous appellerons notre projet
`minigrep` pour le distinguer de l’outil `grep` que vous avez peut-être déjà
sur votre système :

```console
$ cargo new minigrep
     Created binary (application) `minigrep` project
$ cd minigrep
```

La première tâche consiste à faire en sorte que `minigrep` accepte ses deux arguments de ligne de commande : le
chemin du fichier et une chaîne à rechercher. Autrement dit, nous voulons pouvoir exécuter notre
programme avec `cargo run`, deux tirets indiquant que les arguments suivants sont destinés
à notre programme plutôt qu’à `cargo`, une chaîne à rechercher et un chemin vers
un fichier dans lequel effectuer la recherche, comme ceci :

```console
$ cargo run -- searchstring example-filename.txt
```

À l’heure actuelle, le programme généré par `cargo new` ne peut pas traiter les arguments que nous
lui fournissons. Certaines bibliothèques disponibles sur [crates.io](https://crates.io/) peuvent aider
à écrire un programme qui accepte des arguments de ligne de commande, mais puisque vous découvrez
tout juste ce concept, implémentons nous-mêmes cette fonctionnalité.

### Lire les valeurs des arguments

Pour permettre à `minigrep` de lire les valeurs des arguments de ligne de commande que nous lui transmettons,
nous aurons besoin de la fonction `std::env::args` fournie par la bibliothèque standard de Rust.
Cette fonction renvoie un itérateur contenant les arguments de ligne de commande transmis
à `minigrep`. Nous étudierons en détail les itérateurs au [chapitre 13][ch13]<!-- ignore
-->. Pour l’instant, vous devez simplement connaître deux détails à leur sujet : les itérateurs
produisent une série de valeurs, et nous pouvons appeler la méthode `collect` sur un itérateur
pour le convertir en une collection, par exemple un vecteur contenant tous les éléments
produits par l’itérateur.

Le code de la liste 12-1 permet à votre programme `minigrep` de lire tous les arguments de ligne de commande
qui lui sont transmis, puis de collecter leurs valeurs dans un vecteur.

<Listing number="12-1" file-name="src/main.rs" caption="Collecte des arguments de ligne de commande dans un vecteur et affichage de ceux-ci">

```rust
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-01/src/main.rs}}
```

</Listing>

Tout d’abord, nous plaçons le module `std::env` dans la portée à l’aide d’une instruction `use` afin de
pouvoir utiliser sa fonction `args`. Remarquez que la fonction `std::env::args` est
imbriquée dans deux niveaux de modules. Comme nous l’avons expliqué au [chapitre
7][ch7-idiomatic-use]<!-- ignore -->, lorsque la fonction souhaitée est
imbriquée dans plusieurs modules, nous avons choisi de placer le module parent dans la portée plutôt que la fonction. Ainsi,
nous pouvons facilement utiliser d’autres fonctions de `std::env`. C’est également moins ambigu que d’ajouter `use std::env::args`, puis
d’appeler la fonction simplement avec `args`, car `args` pourrait facilement être
confondue avec une fonction définie dans le module courant.

> ### La fonction `args` et les caractères Unicode non valides
>
> Notez que `std::env::args` déclenchera une panique si un argument contient des caractères Unicode non valides.
> Si votre programme doit accepter des arguments contenant des caractères Unicode non valides, utilisez plutôt `std::env::args_os`.
> Cette fonction renvoie un itérateur qui produit des valeurs `OsString` plutôt que des valeurs `String`. Nous avons choisi
> d’utiliser `std::env::args` ici par souci de simplicité, car les valeurs `OsString` varient selon
> la plateforme et sont plus complexes à manipuler que les valeurs `String`.

Sur la première ligne de `main`, nous appelons `env::args`, puis utilisons immédiatement
`collect` pour convertir l’itérateur en un vecteur contenant toutes les valeurs qu’il produit. Nous pouvons utiliser la fonction
`collect` pour créer de nombreux types de collections ; nous annotons donc explicitement le type de `args` pour préciser que
nous voulons un vecteur de chaînes. Bien qu’il soit très rare d’avoir à annoter les types en
Rust, `collect` est l’une des fonctions pour lesquelles cette annotation est souvent nécessaire, car Rust
ne peut pas déduire le type de collection souhaité.

Enfin, nous affichons le vecteur à l’aide de la macro de débogage. Essayons d’abord d’exécuter le code
sans arguments, puis avec deux arguments :

```console
{{#include ../listings/ch12-an-io-project/listing-12-01/output.txt}}
```

```console
{{#include ../listings/ch12-an-io-project/output-only-01-with-args/output.txt}}
```

Remarquez que la première valeur du vecteur est `"target/debug/minigrep"`, qui
est le nom de notre binaire. Cela correspond au comportement de la liste des arguments en
C, qui permet aux programmes d’utiliser le nom sous lequel ils ont été invoqués lors de leur exécution.
Il est souvent pratique de pouvoir accéder au nom du programme, au cas où vous voudriez
l’afficher dans des messages ou modifier le comportement du programme selon l’alias de ligne de commande utilisé pour l’invoquer. Mais pour les besoins de ce
chapitre, nous l’ignorerons et ne conserverons que les deux arguments dont nous avons besoin.

### Enregistrer les valeurs des arguments dans des variables

Le programme peut actuellement accéder aux valeurs fournies comme arguments de ligne de commande. Nous devons maintenant
enregistrer les valeurs des deux arguments dans des variables afin de pouvoir les utiliser dans la suite du programme. Nous faisons cela dans
la liste 12-2.

<Listing number="12-2" file-name="src/main.rs" caption="Création de variables contenant l’argument de requête et l’argument de chemin du fichier">

```rust,should_panic,noplayground
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-02/src/main.rs}}
```

</Listing>

Comme nous l’avons vu en affichant le vecteur, le nom du programme occupe la première valeur du vecteur, à l’index `args[0]` ; nous commençons donc les arguments à l’index 1. Le premier argument reçu par `minigrep` est la chaîne que nous recherchons ; nous plaçons donc une référence vers le premier argument dans la variable `query`. Le deuxième argument correspond au chemin du fichier ; nous plaçons donc une référence vers le deuxième argument dans la variable `file_path`.

Nous affichons temporairement les valeurs de ces variables pour vérifier que le code fonctionne comme prévu. Exécutons à nouveau ce programme avec les arguments `test`
et `sample.txt` :

```console
{{#include ../listings/ch12-an-io-project/listing-12-02/output.txt}}
```

Parfait, le programme fonctionne ! Les valeurs des arguments dont nous avons besoin sont enregistrées dans les bonnes variables. Plus tard, nous ajouterons une gestion des erreurs pour traiter
certaines situations problématiques possibles, par exemple lorsque l’utilisateur ne fournit aucun argument ; pour l’instant, nous ignorerons cette situation et nous nous concentrerons plutôt sur l’ajout de la lecture de fichiers.

[ch13]: ch13-00-functional-features.html
[ch7-idiomatic-use]: ch07-04-bringing-paths-into-scope-with-the-use-keyword.html#creating-idiomatic-use-paths