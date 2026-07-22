## Lecture d'un fichier

Nous allons maintenant ajouter une fonctionnalité pour lire le fichier spécifié dans l'argument `file_path`. Tout d'abord, nous avons besoin d'un fichier d'exemple pour le tester : nous utiliserons un fichier contenant un petit texte sur plusieurs lignes avec quelques mots répétés. La liste 12-3 contient un poème d'Emily Dickinson qui fonctionnera bien ! Créez un fichier appelé _poem.txt_ à la racine de votre projet et entrez le poème « Je suis personne ! Qui es-tu ? »

<Listing number="12-3" file-name="poem.txt" caption="Un poème d'Emily Dickinson constitue un bon cas de test.">

```text
{{#include ../listings/ch12-an-io-project/listing-12-03/poem.txt}}
```

</Listing>

Une fois le texte en place, éditez _src/main.rs_ et ajoutez du code pour lire le fichier, comme montré dans la liste 12-4.

<Listing number="12-4" file-name="src/main.rs" caption="Lecture du contenu du fichier spécifié par le deuxième argument">

```rust,should_panic,noplayground
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-04/src/main.rs:here}}
```

</Listing>

Tout d'abord, nous importons une partie pertinente de la bibliothèque standard avec une instruction `use` : nous avons besoin de `std::fs` pour gérer les fichiers.

Dans `main`, la nouvelle instruction `fs::read_to_string` prend le `file_path`, ouvre ce fichier et renvoie une valeur de type `std::io::Result<String>` contenant le contenu du fichier.

Ensuite, nous ajoutons à nouveau une instruction `println!` temporaire qui imprime la valeur de `contents` après la lecture du fichier afin que nous puissions vérifier que le programme fonctionne jusqu'à présent.

Exécutons ce code avec n'importe quelle chaîne comme premier argument de ligne de commande (car nous n'avons pas encore implémenté la partie recherche) et le fichier _poem.txt_ comme deuxième argument :

```console
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-04/output.txt}}
```

Super ! Le code a lu puis imprimé le contenu du fichier. Mais le code présente quelques défauts. Pour le moment, la fonction `main` a plusieurs responsabilités : en général, les fonctions sont plus claires et plus faciles à maintenir si chacune est responsable d'une seule idée. L'autre problème est que nous ne gérons pas les erreurs aussi bien que nous le pourrions. Le programme est encore petit, donc ces défauts ne posent pas de problème majeur, mais à mesure que le programme grandit, il sera plus difficile de les corriger proprement. Il est bon de commencer à refactoriser tôt lors du développement d'un programme, car il est beaucoup plus facile de refactoriser de petites quantités de code. Nous allons faire cela ensuite.