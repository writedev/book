<!-- Anciennes rubriques. Ne pas supprimer ou les liens risquent de se briser. -->

<a id="writing-error-messages-to-standard-error-instead-of-standard-output"></a>

## Rediriger les erreurs vers la sortie d'erreur standard

Pour le moment, nous écrivons toutes nos sorties dans le terminal en utilisant la macro
`println!`. Dans la plupart des terminaux, il existe deux types de sortie : la _sortie standard_
(`stdout`) pour les informations générales et la _sortie d'erreur standard_ (`stderr`) pour
les messages d'erreur. Cette distinction permet aux utilisateurs de choisir de diriger la
sortie réussie d'un programme vers un fichier tout en imprimant toujours les messages d'erreur à l'écran.

La macro `println!` ne peut imprimer que sur la sortie standard, nous devons donc utiliser autre chose pour imprimer sur la sortie d'erreur standard.

### Vérification de l'emplacement où les erreurs sont écrites

Tout d'abord, observons comment le contenu imprimé par `minigrep` est actuellement écrit sur la sortie standard, y compris les messages d'erreur que nous voulons écrire à la place sur la sortie d'erreur standard. Nous allons le faire en redirigeant le flux de sortie standard vers un fichier tout en provoquant intentionnellement une erreur. Nous ne redirigerons pas le flux d'erreur standard, donc tout contenu envoyé à la sortie d'erreur standard continuera à s'afficher à l'écran.

On s'attend à ce que les programmes en ligne de commande envoient des messages d'erreur vers le flux d'erreur standard afin que nous puissions toujours voir les messages d'erreur à l'écran même si nous redirigeons le flux de sortie standard vers un fichier. Actuellement, notre programme ne se comporte pas bien : nous allons voir qu'il enregistre la sortie des messages d'erreur dans un fichier à la place !

Pour démontrer ce comportement, nous exécuterons le programme avec `>` et le chemin du fichier,
_output.txt_, vers lequel nous voulons rediriger le flux de sortie standard. Nous ne passerons
aucun argument, ce qui devrait provoquer une erreur :

```console
$ cargo run > output.txt
```

La syntaxe `>` indique au shell d'écrire le contenu de la sortie standard dans
_output.txt_ au lieu de l'écran. Nous n'avons pas vu le message d'erreur que nous attendions
imprimé à l'écran, donc cela signifie qu'il a dû se retrouver dans le fichier. Voici ce que
contient _output.txt_ :

```text
Problème de parsing des arguments : pas assez d'arguments
```

Oui, notre message d'erreur est imprimé sur la sortie standard. Il est beaucoup plus utile que les messages d'erreur comme celui-ci soient imprimés sur la sortie d'erreur standard afin que seules les données d'une exécution réussie se retrouvent dans le fichier. Nous allons changer cela.

### Impression des erreurs sur la sortie d'erreur standard

Nous allons utiliser le code dans le Listing 12-24 pour changer la façon dont les messages d'erreur sont imprimés. En raison du refactoring que nous avons effectué précédemment dans ce chapitre, tout le code qui imprime des messages d'erreur se trouve dans une seule fonction, `main`. La bibliothèque standard fournit la macro `eprintln!` qui imprime sur le flux d'erreur standard, donc changeons les deux endroits où nous appelions `println!` pour imprimer des erreurs en utilisant `eprintln!` à la place.

<Listing number="12-24" file-name="src/main.rs" caption="Écriture des messages d'erreur sur la sortie d'erreur standard au lieu de la sortie standard en utilisant `eprintln!`">

```rust,ignore
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-24/src/main.rs:here}}
```

</Listing>

Exécutons à nouveau le programme de la même manière, sans arguments et en redirigeant la sortie standard avec `>` :

```console
$ cargo run > output.txt
Problème de parsing des arguments : pas assez d'arguments
```

Maintenant, nous voyons l'erreur à l'écran et _output.txt_ ne contient rien, ce qui est le comportement que nous attendons des programmes en ligne de commande.

Exécutons à nouveau le programme avec des arguments qui ne provoquent pas d'erreur mais redirigeons toujours la sortie standard vers un fichier, comme ceci :

```console
$ cargo run -- to poem.txt > output.txt
```

Nous ne verrons aucune sortie dans le terminal, et _output.txt_ contiendra nos résultats :

<span class="filename">Nom de fichier : output.txt</span>

```text
Es-tu personne, toi aussi ?
Comme c'est ennuyeux d'être quelqu'un !
```

Cela démontre que nous utilisons désormais la sortie standard pour la sortie réussie et la sortie d'erreur pour la sortie d'erreur de manière appropriée.

## Résumé

Ce chapitre a récapitulé certains des concepts majeurs que vous avez appris jusqu'à présent et a couvert comment effectuer des opérations I/O courantes en Rust. En utilisant des arguments en ligne de commande, des fichiers, des variables d'environnement et la macro `eprintln!` pour imprimer des erreurs, vous êtes maintenant prêt à écrire des applications en ligne de commande. Combiné avec les concepts des chapitres précédents, votre code sera bien organisé, stockera les données efficacement dans les structures de données appropriées, gérera les erreurs correctement et sera bien testé.

Ensuite, nous explorerons certaines fonctionnalités de Rust influencées par les langages fonctionnels : les fermetures et les itérateurs.