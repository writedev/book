## Lire un fichier

Nous allons maintenant ajouter la fonctionnalité permettant de lire le fichier indiqué par l’argument `file_path`. Tout d’abord, il nous faut un fichier d’exemple pour faire un essai : nous allons utiliser un fichier contenant un court texte réparti sur plusieurs lignes, avec quelques mots répétés. Le listing 12-3 contient un poème d’Emily Dickinson qui conviendra parfaitement ! Créez un fichier appelé _poem.txt_ à la racine de votre projet et saisissez-y le poème « I’m Nobody! Who are you? ».

<Listing number="12-3" file-name="poem.txt" caption="Un poème d’Emily Dickinson constitue un bon cas de test.">

```text
{{#include ../listings/ch12-an-io-project/listing-12-03/poem.txt}}
```

</Listing>

Une fois le texte en place, modifiez _src/main.rs_ et ajoutez le code permettant de lire le fichier, comme indiqué dans le listing 12-4.

<Listing number="12-4" file-name="src/main.rs" caption="Lire le contenu du fichier indiqué par le deuxième argument">

```rust,should_panic,noplayground
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-04/src/main.rs:here}}
```

</Listing>

Nous importons d’abord une partie pertinente de la bibliothèque standard à l’aide d’une instruction `use` : nous avons besoin de `std::fs` pour gérer les fichiers.

Dans `main`, la nouvelle instruction `fs::read_to_string` prend `file_path`, ouvre le fichier correspondant et renvoie une valeur de type `std::io::Result<String>` qui contient le contenu du fichier.

Ensuite, nous ajoutons à nouveau une instruction `println!` temporaire qui affiche la valeur de `contents` après la lecture du fichier, afin de vérifier que le programme fonctionne jusqu’ici.

Exécutons ce code avec n’importe quelle chaîne comme premier argument de ligne de commande (car nous n’avons pas encore implémenté la recherche) et le fichier _poem.txt_ comme deuxième argument :

```console
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-04/output.txt}}
```

Parfait ! Le code a lu le contenu du fichier, puis l’a affiché. Mais il présente quelques défauts. Pour l’instant, la fonction `main` a plusieurs responsabilités : en général, les fonctions sont plus claires et plus faciles à maintenir si chacune n’est responsable que d’une seule tâche. L’autre problème est que nous ne gérons pas les erreurs aussi bien que nous le pourrions. Le programme est encore petit, donc ces défauts ne posent pas de gros problème, mais à mesure qu’il grandira, il sera plus difficile de les corriger proprement. Il est préférable de commencer à refactoriser tôt dans le développement d’un programme, car il est beaucoup plus facile de refactoriser de petites portions de code. C’est ce que nous allons faire maintenant.