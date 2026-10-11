<!-- Anciens titres. Ne pas supprimer, sinon les liens risquent de ne plus fonctionner. -->

<a id="writing-error-messages-to-standard-error-instead-of-standard-output"></a>

## Rediriger les erreurs vers la sortie d’erreur standard

Pour le moment, nous écrivons toutes nos sorties dans le terminal à l’aide de la
macro `println!`. Dans la plupart des terminaux, il existe deux types de sortie :
la _sortie standard_ (`stdout`), pour les informations générales, et la _sortie
d’erreur standard_ (`stderr`), pour les messages d’erreur. Cette distinction
permet aux utilisateurs de choisir de rediriger la sortie d’un programme qui
s’est exécuté correctement vers un fichier tout en affichant les messages
d’erreur à l’écran.

La macro `println!` ne peut afficher que sur la sortie standard ; nous devons
donc utiliser autre chose pour afficher les erreurs sur la sortie d’erreur
standard.

### Vérifier où les erreurs sont écrites

Commençons par observer comment le contenu affiché par `minigrep` est
actuellement écrit sur la sortie standard, y compris les messages d’erreur que
nous voulons plutôt écrire sur la sortie d’erreur standard. Pour cela, nous
allons rediriger le flux de sortie standard vers un fichier tout en provoquant
intentionnellement une erreur. Nous ne redirigerons pas le flux de sortie
d’erreur standard, de sorte que tout contenu envoyé sur la sortie d’erreur
standard continuera de s’afficher à l’écran.

Les programmes en ligne de commande sont censés envoyer les messages d’erreur
sur le flux de sortie d’erreur standard, afin que nous puissions continuer à les
voir à l’écran même si nous redirigeons le flux de sortie standard vers un
fichier. Pour l’instant, notre programme ne se comporte pas correctement :
nous allons voir qu’il enregistre plutôt le message d’erreur dans un fichier !

Pour illustrer ce comportement, nous allons exécuter le programme avec `>` et
le chemin du fichier _output.txt_, vers lequel nous voulons rediriger le flux de
sortie standard. Nous ne passerons aucun argument, ce qui devrait provoquer une
erreur :

```console
$ cargo run > output.txt
```

La syntaxe `>` indique au shell d’écrire le contenu de la sortie standard dans
_output.txt_ au lieu de l’afficher à l’écran. Nous n’avons pas vu le message
d’erreur attendu s’afficher à l’écran ; il doit donc se trouver dans le fichier.
Voici le contenu de _output.txt_ :

```text
Problem parsing arguments: not enough arguments
```

Eh oui, notre message d’erreur est affiché sur la sortie standard. Il est bien
plus utile que les messages d’erreur de ce type soient affichés sur la sortie
d’erreur standard, afin que seul le contenu d’une exécution réussie se retrouve
dans le fichier. Nous allons corriger cela.

### Afficher les erreurs sur la sortie d’erreur standard

Nous allons utiliser le code de la liste 12-24 pour modifier l’affichage des
messages d’erreur. Grâce à la refactorisation effectuée plus tôt dans ce
chapitre, tout le code qui affiche des messages d’erreur se trouve dans une
seule fonction, `main`. La bibliothèque standard fournit la macro `eprintln!`,
qui affiche sur le flux de sortie d’erreur standard. Remplaçons donc par
`eprintln!` les deux appels à `println!` qui servent à afficher des erreurs.

<Listing number="12-24" file-name="src/main.rs" caption="Écriture des messages d’erreur sur la sortie d’erreur standard plutôt que sur la sortie standard à l’aide de `eprintln!`">

```rust,ignore
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-24/src/main.rs:here}}
```

</Listing>

Exécutons à nouveau le programme de la même manière, sans argument et en
redirigeant la sortie standard avec `>` :

```console
$ cargo run > output.txt
Problem parsing arguments: not enough arguments
```

Nous voyons maintenant l’erreur à l’écran, et _output.txt_ ne contient rien,
ce qui correspond au comportement attendu des programmes en ligne de commande.

Exécutons à nouveau le programme avec des arguments qui ne provoquent pas
d’erreur, tout en redirigeant la sortie standard vers un fichier, comme ceci :

```console
$ cargo run -- to poem.txt > output.txt
```

Aucune sortie ne s’affichera dans le terminal, et _output.txt_ contiendra nos
résultats :

<span class="filename">Nom du fichier : output.txt</span>

```text
Are you nobody, too?
How dreary to be somebody!
```

Cela montre que nous utilisons maintenant la sortie standard pour les sorties
en cas de réussite et la sortie d’erreur standard pour les erreurs, selon le
cas.

## Résumé

Ce chapitre a récapitulé plusieurs concepts importants appris jusqu’ici et
présenté comment effectuer des opérations d’E/S courantes en Rust. En utilisant
les arguments de ligne de commande, les fichiers, les variables d’environnement
et la macro `eprintln!` pour afficher les erreurs, vous êtes maintenant prêt à
écrire des applications en ligne de commande. Combiné aux concepts des chapitres
précédents, votre code sera bien organisé, stockera efficacement les données
dans les structures de données appropriées, gérera correctement les erreurs et
sera bien testé.

Ensuite, nous allons explorer certaines fonctionnalités de Rust influencées par
les langages fonctionnels : les fermetures et les itérateurs.