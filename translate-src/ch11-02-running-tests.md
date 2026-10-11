## Contrôler l’exécution des tests

Tout comme `cargo run` compile votre code puis exécute le binaire obtenu, `cargo test` compile votre code en mode test et exécute le binaire de test obtenu. Par défaut, le binaire produit par `cargo test` exécute tous les tests en parallèle et capture la sortie générée pendant leur exécution, empêchant son affichage et facilitant la lecture des résultats des tests. Vous pouvez toutefois spécifier des options de ligne de commande pour modifier ce comportement par défaut.

Certaines options de ligne de commande sont destinées à `cargo test`, et d’autres au binaire de test obtenu. Pour séparer ces deux types d’arguments, indiquez d’abord ceux destinés à `cargo test`, puis le séparateur `--`, suivi de ceux destinés au binaire de test. La commande `cargo test --help` affiche les options que vous pouvez utiliser avec `cargo test`, et la commande `cargo test -- --help` affiche celles que vous pouvez utiliser après le séparateur. Ces options sont également documentées dans la [section « Tests » du _livre de `rustc`_][tests].

[tests]: https://doc.rust-lang.org/rustc/tests/index.html

### Exécuter les tests en parallèle ou les uns après les autres

Lorsque vous exécutez plusieurs tests, ils s’exécutent par défaut en parallèle à l’aide de threads, ce qui leur permet de terminer plus rapidement et vous donne un retour plus tôt. Comme les tests s’exécutent en même temps, vous devez vous assurer qu’ils ne dépendent pas les uns des autres ni d’un état partagé, notamment d’un environnement partagé, comme le répertoire de travail actuel ou les variables d’environnement.

Par exemple, supposons que chacun de vos tests exécute du code qui crée un fichier sur le disque nommé _test-output.txt_ et y écrit des données. Chaque test lit ensuite les données de ce fichier et vérifie qu’il contient une valeur particulière, différente pour chaque test. Comme les tests s’exécutent en même temps, l’un d’eux pourrait écraser le fichier entre le moment où un autre test l’écrit et celui où il le lit. Le second test échouerait alors, non pas parce que le code est incorrect, mais parce que les tests se sont gênés mutuellement lors de leur exécution en parallèle. Une solution consiste à s’assurer que chaque test écrit dans un fichier différent ; une autre consiste à exécuter les tests un par un.

Si vous ne souhaitez pas exécuter les tests en parallèle, ou si vous voulez contrôler plus finement le nombre de threads utilisés, vous pouvez transmettre au binaire de test l’indicateur `--test-threads` ainsi que le nombre de threads que vous souhaitez utiliser. Examinez l’exemple suivant :

```console
$ cargo test -- --test-threads=1
```

Nous avons défini le nombre de threads de test à `1`, indiquant ainsi au programme de ne pas utiliser le parallélisme. L’exécution des tests avec un seul thread prendra plus de temps que leur exécution en parallèle, mais les tests ne se gêneront pas s’ils partagent un état.

### Afficher la sortie des fonctions

Par défaut, si un test réussit, la bibliothèque de test de Rust capture tout ce qui est affiché sur la sortie standard. Par exemple, si nous appelons `println!` dans un test et que celui-ci réussit, nous ne verrons pas la sortie de `println!` dans le terminal ; nous ne verrons que la ligne indiquant que le test a réussi. Si un test échoue, nous verrons tout ce qui a été affiché sur la sortie standard avec le reste du message d’échec.

À titre d’exemple, le Listing 11-10 présente une fonction amusante qui affiche la valeur de son paramètre et renvoie 10, ainsi qu’un test qui réussit et un test qui échoue.

<Listing number="11-10" file-name="src/lib.rs" caption="Tests d’une fonction qui appelle `println!`">

```rust,panics,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-10/src/lib.rs}}
```

</Listing>

Lorsque nous exécutons ces tests avec `cargo test`, nous voyons la sortie suivante :

```console
{{#include ../listings/ch11-writing-automated-tests/listing-11-10/output.txt}}
```

Notez que nous ne voyons nulle part dans cette sortie `I got the value 4`, qui est affiché lors de l’exécution du test qui réussit. Cette sortie a été capturée. La sortie du test qui a échoué, `I got the value 8`, apparaît dans la section du résumé des tests, qui indique également la cause de l’échec.

Si nous voulons aussi voir les valeurs affichées pour les tests qui réussissent, nous pouvons demander à Rust d’afficher également la sortie des tests réussis avec `--show-output` :

```console
$ cargo test -- --show-output
```

Lorsque nous exécutons à nouveau les tests du Listing 11-10 avec l’indicateur `--show-output`, nous voyons la sortie suivante :

```console
{{#include ../listings/ch11-writing-automated-tests/output-only-01-show-output/output.txt}}
```

### Exécuter un sous-ensemble de tests par nom

L’exécution d’une suite de tests complète peut parfois prendre beaucoup de temps. Si vous travaillez sur le code d’une partie particulière, vous voudrez peut-être exécuter uniquement les tests qui s’y rapportent. Vous pouvez choisir les tests à exécuter en passant à `cargo test` le nom ou les noms des tests souhaités en argument.

Pour montrer comment exécuter un sous-ensemble de tests, nous allons d’abord créer trois tests pour notre fonction `add_two`, comme indiqué dans le Listing 11-11, puis choisir ceux à exécuter.

<Listing number="11-11" file-name="src/lib.rs" caption="Trois tests portant des noms différents">

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-11/src/lib.rs}}
```

</Listing>

Si nous exécutons les tests sans passer d’arguments, comme nous l’avons vu précédemment, tous les tests s’exécuteront en parallèle :

```console
{{#include ../listings/ch11-writing-automated-tests/listing-11-11/output.txt}}
```

#### Exécuter un seul test

Nous pouvons passer à `cargo test` le nom de n’importe quelle fonction de test pour n’exécuter que ce test :

```console
{{#include ../listings/ch11-writing-automated-tests/output-only-02-single-test/output.txt}}
```

Seul le test nommé `one_hundred` s’est exécuté ; les deux autres tests ne correspondaient pas à ce nom. La sortie des tests nous indique qu’il y avait d’autres tests qui n’ont pas été exécutés en affichant `2 filtered out` à la fin.

Nous ne pouvons pas indiquer de cette manière les noms de plusieurs tests ; seule la première valeur passée à `cargo test` sera utilisée. Il existe toutefois un moyen d’exécuter plusieurs tests.

#### Filtrer pour exécuter plusieurs tests

Nous pouvons indiquer une partie du nom d’un test ; tout test dont le nom correspond à cette valeur sera exécuté. Par exemple, comme deux des noms de nos tests contiennent `add`, nous pouvons exécuter ces deux tests en lançant `cargo test add` :

```console
{{#include ../listings/ch11-writing-automated-tests/output-only-03-multiple-tests/output.txt}}
```

Cette commande a exécuté tous les tests dont le nom contient `add` et a filtré le test nommé `one_hundred`. Notez également que le module dans lequel figure un test fait partie de son nom ; nous pouvons donc exécuter tous les tests d’un module en filtrant sur le nom de ce module.

<!-- Anciennes rubriques. Ne pas supprimer, sinon les liens risquent de ne plus fonctionner. -->

<a id="ignoring-some-tests-unless-specifically-requested"></a>

### Ignorer les tests sauf demande explicite

Certains tests peuvent parfois être très longs à exécuter ; vous voudrez peut-être les exclure de la plupart des exécutions de `cargo test`. Plutôt que de lister en arguments tous les tests que vous souhaitez exécuter, vous pouvez annoter les tests longs à l’aide de l’attribut `ignore` pour les exclure, comme ici :

<span class="filename">Nom du fichier : src/lib.rs</span>

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-11-ignore-a-test/src/lib.rs:here}}
```

Après `#[test]`, nous ajoutons la ligne `#[ignore]` au test que nous voulons exclure. Désormais, lorsque nous exécutons nos tests, `it_works` s’exécute, mais pas `expensive_test` :

```console
{{#include ../listings/ch11-writing-automated-tests/no-listing-11-ignore-a-test/output.txt}}
```

La fonction `expensive_test` est indiquée comme `ignored`. Si nous voulons exécuter uniquement les tests ignorés, nous pouvons utiliser `cargo test -- --ignored` :

```console
{{#include ../listings/ch11-writing-automated-tests/output-only-04-running-ignored/output.txt}}
```

En contrôlant les tests exécutés, vous pouvez vous assurer que les résultats de `cargo test` vous seront renvoyés rapidement. Lorsque vous serez prêt à vérifier les résultats des tests `ignored` et que vous aurez le temps d’attendre, vous pourrez lancer `cargo test -- --ignored`. Si vous souhaitez exécuter tous les tests, qu’ils soient ignorés ou non, vous pouvez lancer `cargo test -- --include-ignored`.