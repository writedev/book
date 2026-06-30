## Contrôler l'exécution des tests

Tout comme `cargo run` compile votre code puis exécute le binaire résultant, `cargo test` compile votre code en mode test et exécute le binaire de test résultant. Le comportement par défaut du binaire produit par `cargo test` est de faire fonctionner tous les tests en parallèle et de capturer la sortie générée durant les exécutions de test, empêchant l'affichage de cette sortie et facilitant la lecture des résultats des tests. Vous pouvez cependant spécifier des options de ligne de commande pour changer ce comportement par défaut.

Certaines options de ligne de commande s'appliquent à `cargo test`, et d'autres au binaire de test résultant. Pour séparer ces deux types d'arguments, vous listez les arguments destinés à `cargo test` suivis du séparateur `--`, puis ceux qui vont au binaire de test. Exécuter `cargo test --help` affiche les options que vous pouvez utiliser avec `cargo test`, et exécuter `cargo test -- --help` affiche les options que vous pouvez utiliser après le séparateur. Ces options sont également documentées dans [la section "Tests" de _The `rustc` Book_][tests].

[tests]: https://doc.rust-lang.org/rustc/tests/index.html

### Exécution des tests en parallèle ou consécutivement

Lorsque vous exécutez plusieurs tests, par défaut, ils s'exécutent en parallèle à l'aide de threads, ce qui signifie qu'ils se terminent plus rapidement et que vous recevez des retours plus tôt. Étant donné que les tests s'exécutent en même temps, vous devez vous assurer que vos tests ne dépendent pas les uns des autres ou d'un état partagé, y compris un environnement partagé, tel que le répertoire de travail actuel ou les variables d'environnement.

Par exemple, supposons que chacun de vos tests exécute un code qui crée un fichier sur le disque nommé _test-output.txt_ et écrit des données dans ce fichier. Ensuite, chaque test lit les données de ce fichier et vérifie que le fichier contient une valeur particulière, qui est différente dans chaque test. Comme les tests s'exécutent en même temps, un test pourrait écraser le fichier entre le moment où un autre test écrit dans le fichier et le moment où il le lit. Le second test échouera alors, non pas parce que le code est incorrect, mais parce que les tests se sont interférés les uns avec les autres pendant leur exécution en parallèle. Une solution consiste à s'assurer que chaque test écrit dans un fichier différent ; une autre solution consiste à exécuter les tests un par un.

Si vous ne souhaitez pas exécuter les tests en parallèle ou si vous souhaitez un contrôle plus précis sur le nombre de threads utilisés, vous pouvez envoyer le drapeau `--test-threads` et le nombre de threads que vous souhaitez utiliser au binaire de test. Examinez l'exemple suivant :

```console
$ cargo test -- --test-threads=1
```

Nous avons défini le nombre de threads de test sur `1`, indiquant au programme de ne pas utiliser de parallélisme. Exécuter les tests avec un seul thread prendra plus de temps qu'en parallèle, mais les tests n'interféreront pas les uns avec les autres s'ils partagent un état.

### Affichage de la sortie des fonctions

Par défaut, si un test réussit, la bibliothèque de test de Rust capture tout ce qui est imprimé sur la sortie standard. Par exemple, si nous appelons `println!` dans un test et que le test réussit, nous ne verrons pas la sortie de `println!` dans le terminal ; nous verrons seulement la ligne indiquant que le test a réussi. Si un test échoue, nous verrons tout ce qui a été imprimé sur la sortie standard avec le reste du message d'échec.

À titre d'exemple, l'énoncé 11-10 contient une fonction triviale qui imprime la valeur de son paramètre et retourne 10, ainsi qu'un test qui réussit et un test qui échoue.

<Énoncé numéro="11-10" nom-de-fichier="src/lib.rs" légende="Tests pour une fonction qui appelle `println!`">

```rust,panics,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-10/src/lib.rs}}
```

</Énoncé>

Lorsque nous exécutons ces tests avec `cargo test`, nous verrons la sortie suivante :

```console
{{#include ../listings/ch11-writing-automated-tests/listing-11-10/output.txt}}
```

Notez qu'aucune mention de `I got the value 4`, qui est imprimé lors de l'exécution du test réussi, n'apparaît dans cette sortie. Cette sortie a été capturée. La sortie du test qui a échoué, `I got the value 8`, apparaît dans la section du résumé de test, qui montre également la cause de l'échec du test.

Si nous voulons voir les valeurs imprimées des tests réussis également, nous pouvons demander à Rust d'afficher aussi la sortie des tests réussis avec `--show-output` :

```console
$ cargo test -- --show-output
```

Lorsque nous exécutons à nouveau les tests de l'énoncé 11-10 avec le drapeau `--show-output`, nous voyons la sortie suivante :

```console
{{#include ../listings/ch11-writing-automated-tests/output-only-01-show-output/output.txt}}
```

### Exécution d'un sous-ensemble de tests par nom

Exécuter une suite de tests complète peut parfois prendre beaucoup de temps. Si vous travaillez sur du code dans un domaine particulier, vous voudrez peut-être exécuter uniquement les tests concernant ce code. Vous pouvez choisir quels tests exécuter en passant à `cargo test` le nom ou les noms des tests que vous souhaitez exécuter en argument.

Pour démontrer comment exécuter un sous-ensemble de tests, nous allons d'abord créer trois tests pour notre fonction `add_two`, comme montré dans l'énoncé 11-11, et choisir lesquels exécuter.

<Énoncé numéro="11-11" nom-de-fichier="src/lib.rs" légende="Trois tests avec trois noms différents">

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-11/src/lib.rs}}
```

</Énoncé>

Si nous exécutons les tests sans passer d'arguments, comme nous l'avons vu précédemment, tous les tests s'exécuteront en parallèle :

```console
{{#include ../listings/ch11-writing-automated-tests/listing-11-11/output.txt}}
```

#### Exécution de tests uniques

Nous pouvons passer le nom de n'importe quelle fonction de test à `cargo test` pour exécuter uniquement ce test :

```console
{{#include ../listings/ch11-writing-automated-tests/output-only-02-single-test/output.txt}}
```

Seul le test nommé `one_hundred` s'est exécuté ; les deux autres tests n'ont pas correspondé à ce nom. La sortie des tests nous fait savoir qu'il y avait d'autres tests qui ne se sont pas exécutés en affichant `2 filtrés`.

Nous ne pouvons pas spécifier les noms de plusieurs tests de cette manière ; seul le premier nom donné à `cargo test` sera utilisé. Mais il existe un moyen d'exécuter plusieurs tests.

#### Filtrage pour exécuter plusieurs tests

Nous pouvons spécifier une partie d'un nom de test, et tout test dont le nom correspond à cette valeur sera exécuté. Par exemple, comme deux des noms de nos tests contiennent `add`, nous pouvons exécuter ces deux tests en lançant `cargo test add` :

```console
{{#include ../listings/ch11-writing-automated-tests/output-only-03-multiple-tests/output.txt}}
```

Cette commande a exécuté tous les tests contenant `add` dans le nom et a filtré le test nommé `one_hundred`. Notez également que le module dans lequel un test apparaît fait partie du nom du test, ce qui nous permet d'exécuter tous les tests dans un module en filtrant sur le nom du module.

### Ignorer certains tests sauf demande spécifique

Parfois, quelques tests spécifiques peuvent être très longs à exécuter, donc vous pourriez vouloir les exclure lors de la plupart des exécutions de `cargo test`. Au lieu de lister comme arguments tous les tests que vous souhaitez exécuter, vous pouvez annoter les tests coûteux en utilisant l'attribut `ignore` pour les exclure, comme montré ici :

<span class="nom-fichier">Nom de fichier : src/lib.rs</span>

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-11-ignore-a-test/src/lib.rs:here}}
```

Après `#[test]`, nous ajoutons la ligne `#[ignore]` au test que nous voulons exclure. Maintenant, lorsque nous exécutons nos tests, `it_works` s'exécute, mais `expensive_test` ne s'exécute pas :

```console
{{#include ../listings/ch11-writing-automated-tests/no-listing-11-ignore-a-test/output.txt}}
```

La fonction `expensive_test` est indiquée comme `ignorée`. Si nous voulons exécuter uniquement les tests ignorés, nous pouvons utiliser `cargo test -- --ignored` :

```console
{{#include ../listings/ch11-writing-automated-tests/output-only-04-running-ignored/output.txt}}
```

En contrôlant quels tests s'exécutent, vous pouvez vous assurer que les résultats de `cargo test` seront renvoyés rapidement. Lorsque vous êtes à un moment où il est logique de vérifier les résultats des tests `ignorés` et que vous avez le temps d'attendre les résultats, vous pouvez exécuter `cargo test -- --ignored` à la place. Si vous souhaitez exécuter tous les tests qu'ils soient ignorés ou non, vous pouvez exécuter `cargo test -- --include-ignored`.