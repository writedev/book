## Publier un Crate sur Crates.io

Nous avons utilisé des paquets de [crates.io](https://crates.io/)<!-- ignore --> comme dépendances de notre projet, mais vous pouvez également partager votre code avec d'autres personnes en publiant vos propres paquets. Le registre de crates à [crates.io](https://crates.io/)<!-- ignore --> distribue le code source de vos paquets, donc il héberge principalement du code open source.

Rust et Cargo disposent de fonctionnalités qui facilitent la recherche et l'utilisation de votre paquet publié. Nous allons parler de certaines de ces fonctionnalités ensuite et expliquer comment publier un paquet.

### Rendre les Commentaires de Documentation Utiles

Documenter avec précision vos paquets aidera les autres utilisateurs à savoir comment et quand les utiliser, donc cela vaut la peine d'investir du temps à écrire de la documentation. Dans le Chapitre 3, nous avons discuté de la façon de commenter le code Rust en utilisant deux barres obliques `//`. Rust a également un type particulier de commentaire pour la documentation, connu sous le nom de _commentaire de documentation_, qui générera une documentation HTML. Cette HTML affiche le contenu des commentaires de documentation pour les éléments de l'API publique destinés aux programmeurs intéressés à savoir comment _utiliser_ votre crate plutôt qu'à savoir comment votre crate est _implémentée_.

Les commentaires de documentation utilisent trois barres obliques `///` au lieu de deux et prennent en charge la notation Markdown pour formater le texte. Placez les commentaires de documentation juste avant l'élément qu'ils documentent. La Liste 14-1 montre des commentaires de documentation pour une fonction `add_one` dans une crate nommée `my_crate`.

<Listing number="14-1" file-name="src/lib.rs" caption="Un commentaire de documentation pour une fonction">

```rust,ignore
{{#rustdoc_include ../listings/ch14-more-about-cargo/listing-14-01/src/lib.rs}}
```

</Listing>

Ici, nous donnons une description de ce que fait la fonction `add_one`, commençons une section avec le titre `Examples`, puis fournissons du code qui démontre comment utiliser la fonction `add_one`. Nous pouvons générer la documentation HTML à partir de ce commentaire de documentation en exécutant `cargo doc`. Cette commande exécute l'outil `rustdoc` distribué avec Rust et place la documentation HTML générée dans le répertoire _target/doc_.

Pour plus de commodité, l'exécution de `cargo doc --open` construira le HTML pour la documentation de votre crate actuelle (ainsi que la documentation de toutes les dépendances de votre crate) et ouvrira le résultat dans un navigateur web. Naviguez jusqu'à la fonction `add_one` et vous verrez comment le texte dans les commentaires de documentation est rendu, comme montré dans la Figure 14-1.

<img alt="Documentation HTML rendue pour la fonction `add_one` de `my_crate`" src="img/trpl14-01.png" class="center" />

<span class="caption">Figure 14-1 : La documentation HTML pour la fonction `add_one`</span>

#### Sections Couramment Utilisées

Nous avons utilisé le titre Markdown `# Examples` dans la Liste 14-1 pour créer une section dans le HTML avec le titre « Exemples ». Voici quelques autres sections que les auteurs de crates utilisent souvent dans leur documentation :

- **Paniques** : Ce sont les scénarios dans lesquels la fonction documentée pourrait provoquer une panique. Les appelants de la fonction qui ne veulent pas que leurs programmes paniquent doivent s'assurer qu'ils n'appellent pas la fonction dans ces situations.
- **Erreurs** : Si la fonction retourne un `Result`, il peut être utile de décrire les types d'erreurs qui pourraient survenir et quelles conditions pourraient entraîner le renvoi de ces erreurs, afin que les appelants puissent écrire du code pour gérer les différentes sortes d'erreurs de différentes manières.
- **Sécurité** : Si la fonction est `unsafe` à appeler (nous discutons de l'insécurité dans le Chapitre 20), il doit y avoir une section expliquant pourquoi la fonction est dangereuse et couvrant les invariants que la fonction s'attend à ce que les appelants respectent.

La plupart des commentaires de documentation n'ont pas besoin de toutes ces sections, mais c'est une bonne liste de contrôle pour vous rappeler les aspects de votre code qui intéresseront les utilisateurs.

#### Commentaires de Documentation comme Tests

Ajouter des blocs de code d'exemple dans vos commentaires de documentation peut aider à démontrer comment utiliser votre bibliothèque et a un avantage supplémentaire : exécuter `cargo test` exécutera les exemples de code dans votre documentation en tant que tests ! Rien n'est meilleur que la documentation avec des exemples. Mais rien n'est pire que des exemples qui ne fonctionnent pas parce que le code a changé depuis que la documentation a été écrite. Si nous exécutons `cargo test` avec la documentation de la fonction `add_one` de la Liste 14-1, nous verrons une section dans les résultats de test qui ressemble à ceci :

```text
   Doc-tests my_crate

running 1 test
test src/lib.rs - add_one (line 5) ... ok

test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.27s
```

Maintenant, si nous changeons soit la fonction, soit l'exemple de sorte que le `assert_eq!` dans l'exemple provoque une panique, et exécutons à nouveau `cargo test`, nous verrons que les tests de documentation détectent que l'exemple et le code ne sont pas synchronisés !

#### Commentaires d'Éléments Contenus

Le style de commentaire de documentation `//!` ajoute de la documentation à l'élément qui *contient* les commentaires plutôt qu'aux éléments *suivant* les commentaires. Nous utilisons généralement ces commentaires de documentation dans le fichier racine de la crate (_src/lib.rs_ par convention) ou à l'intérieur d'un module pour documenter l'ensemble de la crate ou du module.

Par exemple, pour ajouter la documentation qui décrit le but de la crate `my_crate` contenant la fonction `add_one`, nous ajoutons des commentaires de documentation qui commencent par `//!` au début du fichier _src/lib.rs_, comme montré dans la Liste 14-2.

<Listing number="14-2" file-name="src/lib.rs" caption="La documentation pour la crate `my_crate` dans son ensemble">

```rust,ignore
{{#rustdoc_include ../listings/ch14-more-about-cargo/listing-14-02/src/lib.rs:here}}
```

</Listing>

Remarquez qu'il n'y a pas de code après la dernière ligne qui commence par `//!`. Parce que nous avons commencé les commentaires par `//!` au lieu de `///`, nous documentons l'élément qui contient ce commentaire plutôt qu'un élément qui suit ce commentaire. Dans ce cas, cet élément est le fichier _src/lib.rs_, qui est la racine de la crate. Ces commentaires décrivent l'ensemble de la crate.

Lorsque nous exécutons `cargo doc --open`, ces commentaires s'afficheront sur la page d'accueil de la documentation pour `my_crate` au-dessus de la liste des éléments publics dans la crate, comme montré dans la Figure 14-2.

Les commentaires de documentation à l'intérieur des éléments sont utiles pour décrire les crates et les modules en particulier. Utilisez-les pour expliquer l'objectif général du conteneur afin d'aider vos utilisateurs à comprendre l'organisation de la crate.

<img alt="Documentation HTML rendue avec un commentaire pour la crate dans son ensemble" src="img/trpl14-02.png" class="center" />

<span class="caption">Figure 14-2 : La documentation rendue pour `my_crate`, y compris le commentaire décrivant la crate dans son ensemble</span>

### Exporter une API Publique Pratique

La structure de votre API publique est une considération majeure lors de la publication d'un crate. Les personnes qui utilisent votre crate connaissent moins bien la structure que vous et pourraient avoir des difficultés à trouver les éléments qu'elles veulent utiliser si votre crate a une grande hiérarchie de modules.

Dans le Chapitre 7, nous avons couvert comment rendre les éléments publics en utilisant le mot-clé `pub`, et comment introduire des éléments dans une portée avec le mot-clé `use`. Toutefois, la structure qui a du sens pour vous pendant le développement d'un crate peut ne pas être très pratique pour vos utilisateurs. Vous pourriez vouloir organiser vos structures dans une hiérarchie contenant plusieurs niveaux, mais ensuite les personnes qui veulent utiliser un type que vous avez défini profondément dans cette hiérarchie pourraient avoir du mal à découvrir que ce type existe. Elles pourraient également être agacées d'avoir à écrire `use my_crate::some_module::another_module::UsefulType;` plutôt que `use my_crate::UsefulType;`.

La bonne nouvelle est que si la structure _n'est pas_ pratique pour les autres à utiliser depuis une autre bibliothèque, vous n'avez pas besoin de réorganiser votre organisation interne : vous pouvez plutôt ré-exporter des éléments pour créer une structure publique qui est différente de votre structure privée en utilisant `pub use`. *Le ré-export* consiste à prendre un élément public dans un endroit et à le rendre public dans un autre endroit, comme s'il était défini à l'autre endroit.

Par exemple, disons que nous avons créé une bibliothèque nommée `art` pour modéliser des concepts artistiques. Dans cette bibliothèque se trouvent deux modules : un module `kinds` contenant deux énumérations nommées `PrimaryColor` et `SecondaryColor`, et un module `utils` contenant une fonction nommée `mix`, comme montré dans la Liste 14-3.

<Listing number="14-3" file-name="src/lib.rs" caption="Une bibliothèque `art` avec des éléments organisés en modules `kinds` et `utils`">

```rust,noplayground,test_harness
{{#rustdoc_include ../listings/ch14-more-about-cargo/listing-14-03/src/lib.rs:here}}
```

</Listing>

La Figure 14-3 montre à quoi ressemblera la page d'accueil de la documentation pour cette crate générée par `cargo doc`.

<img alt="Documentation rendue pour la crate `art` qui liste les modules `kinds` et `utils`" src="img/trpl14-03.png" class="center" />

<span class="caption">Figure 14-3 : La page d'accueil de la documentation pour `art` qui liste les modules `kinds` et `utils`</span>

Notez que les types `PrimaryColor` et `SecondaryColor` ne sont pas listés sur la page d'accueil, pas plus que la fonction `mix`. Nous devons cliquer sur `kinds` et `utils` pour les voir.

Une autre crate qui dépend de cette bibliothèque aurait besoin de déclarations `use` qui apportent les éléments de `art` dans la portée, en spécifiant la structure des modules qui est actuellement définie. La Liste 14-4 montre un exemple d'une crate qui utilise les éléments `PrimaryColor` et `mix` de la crate `art`.

<Listing number="14-4" file-name="src/main.rs" caption="Une crate utilisant les éléments de la crate `art` avec sa structure interne exportée">

```rust,ignore
{{#rustdoc_include ../listings/ch14-more-about-cargo/listing-14-04/src/main.rs}}
```

</Listing>

L'auteur du code dans la Liste 14-4, qui utilise la crate `art`, a dû comprendre que `PrimaryColor` se trouve dans le module `kinds` et que `mix` se trouve dans le module `utils`. La structure des modules de la crate `art` est plus pertinente pour les développeurs travaillant sur la crate `art` que pour ceux qui l'utilisent. La structure interne ne contient aucune information utile pour quelqu'un essayant de comprendre comment utiliser la crate `art`, mais cause plutôt de la confusion car les développeurs qui l'utilisent doivent comprendre où chercher et doivent spécifier les noms de modules dans les déclarations `use`.

Pour supprimer l'organisation interne de l'API publique, nous pouvons modifier le code de la crate `art` dans la Liste 14-3 pour ajouter des déclarations `pub use` afin de ré-exporter les éléments au niveau supérieur, comme montré dans la Liste 14-5.

<Listing number="14-5" file-name="src/lib.rs" caption="Ajouter des déclarations `pub use` pour ré-exporter des éléments">

```rust,ignore
{{#rustdoc_include ../listings/ch14-more-about-cargo/listing-14-05/src/lib.rs:here}}
```

</Listing>

La documentation API que `cargo doc` génère pour cette crate affichera désormais et liera les ré-exportations sur la page d'accueil, comme montré dans la Figure 14-4, rendant les types `PrimaryColor` et `SecondaryColor` ainsi que la fonction `mix` plus faciles à trouver.

<img alt="Documentation rendue pour la crate `art` avec les ré-exportations sur la page d'accueil" src="img/trpl14-04.png" class="center" />

<span class="caption">Figure 14-4 : La page d'accueil de la documentation pour `art` qui liste les ré-exportations</span>

Les utilisateurs de la crate `art` peuvent toujours voir et utiliser la structure interne de la Liste 14-3 comme démontré dans la Liste 14-4, ou ils peuvent utiliser la structure plus pratique de la Liste 14-5, comme montré dans la Liste 14-6.

<Listing number="14-6" file-name="src/main.rs" caption="Un programme utilisant les éléments ré-exportés de la crate `art`">

```rust,ignore
{{#rustdoc_include ../listings/ch14-more-about-cargo/listing-14-06/src/main.rs:here}}
```

</Listing>

Dans les cas où il y a de nombreux modules imbriqués, ré-exporter les types au niveau supérieur avec `pub use` peut faire une différence significative dans l'expérience des personnes qui utilisent la crate. Une autre utilisation courante de `pub use` est de ré-exporter les définitions d'une dépendance dans la crate actuelle pour faire en sorte que les définitions de cette crate fassent partie de l'API publique de votre crate.

Créer une structure d'API publique utile est plus un art qu'une science, et vous pouvez itérer pour trouver l'API qui fonctionne le mieux pour vos utilisateurs. Choisir `pub use` vous donne de la flexibilité quant à la façon dont vous structurez votre crate en interne et découple cette structure interne de ce que vous présentez à vos utilisateurs. Regardez le code de certaines crates que vous avez installées pour voir si leur structure interne diffère de leur API publique.

### Configurer un Compte Crates.io

Avant de pouvoir publier des crates, vous devez créer un compte sur [crates.io](https://crates.io/)<!-- ignore --> et obtenir un jeton API. Pour ce faire, visitez la page d'accueil à [crates.io](https://crates.io/)<!-- ignore --> et connectez-vous via un compte GitHub. (Le compte GitHub est actuellement une exigence, mais le site pourrait supporter d'autres façons de créer un compte à l'avenir.) Une fois connecté, visitez vos paramètres de compte à [https://crates.io/me/](https://crates.io/me/)<!-- ignore --> et récupérez votre clé API. Ensuite, exécutez la commande `cargo login` et collez votre clé API lorsque vous y serez invité, comme ceci :

```console
$ cargo login
abcdefghijklmnopqrstuvwxyz012345
```

Cette commande informera Cargo de votre jeton API et l'enregistrera localement dans _~/.cargo/credentials.toml_. Notez que ce jeton est un secret : ne le partagez pas avec d'autres. Si vous le partagez pour une raison quelconque, vous devez le révoquer et générer un nouveau jeton sur [crates.io](https://crates.io/)<!-- ignore -->.

### Ajouter des Métadonnées à un Nouveau Crate

Disons que vous avez une crate que vous souhaitez publier. Avant de publier, vous devrez ajouter certaines métadonnées dans la section `[package]` du fichier _Cargo.toml_ de la crate.

Votre crate aura besoin d'un nom unique. Pendant que vous travaillez sur un crate localement, vous pouvez nommer un crate comme vous le souhaitez. Cependant, les noms des crates sur [crates.io](https://crates.io/)<!-- ignore --> sont alloués sur une base de premier arrivé, premier servi. Une fois qu'un nom de crate est pris, personne d'autre ne peut publier un crate avec ce nom. Avant d'essayer de publier un crate, recherchez le nom que vous souhaitez utiliser. Si le nom a été utilisé, vous devrez trouver un autre nom et modifier le champ `name` dans le fichier _Cargo.toml_ sous la section `[package]` pour utiliser le nouveau nom pour la publication, comme suit :

<span class="filename">Nom de fichier : Cargo.toml</span>

```toml
[package]
name = "guessing_game"
```

Même si vous avez choisi un nom unique, lorsque vous exécutez `cargo publish` pour publier le crate à ce stade, vous recevrez un avertissement puis une erreur :

```console
$ cargo publish
    Mise à jour de l'index de crates.io
warning: le manifeste n'a pas de description, licence, fichier de licence, documentation, page d'accueil ou dépôt.
Voir https://doc.rust-lang.org/cargo/reference/manifest.html#package-metadata pour plus d'informations.
--snip--
error: échec de la publication sur le registre à https://crates.io

Causé par :
  le serveur distant a répondu par une erreur (statut 400 Bad Request) : champs de métadonnées manquants ou vides : description, licence. Veuillez consulter https://doc.rust-lang.org/cargo/reference/manifest.html pour plus d'informations sur la configuration de ces champs.
```

Cela entraîne une erreur car des informations cruciales font défaut : une description et une licence sont requises afin que les gens sachent ce que fait votre crate et selon quelles conditions ils peuvent l'utiliser. Dans _Cargo.toml_, ajoutez une description qui ne fait qu'une phrase ou deux, car elle apparaîtra avec votre crate dans les résultats de recherche. Pour le champ `license`, vous devez donner une _valeur d'identifiant de licence_. La [Linux Foundation’s Software Package Data Exchange (SPDX)][spdx] répertorie les identifiants que vous pouvez utiliser pour cette valeur. Par exemple, pour spécifier que vous avez licencié votre crate sous la Licence MIT, ajoutez l'identifiant `MIT` :

<span class="filename">Nom de fichier : Cargo.toml</span>

```toml
[package]
name = "guessing_game"
license = "MIT"
```

Si vous souhaitez utiliser une licence qui n'apparaît pas dans l'SPDX, vous devez placer le texte de cette licence dans un fichier, inclure le fichier dans votre projet, puis utiliser `license-file` pour spécifier le nom de ce fichier au lieu d'utiliser la clé `license`.

L'orientation quant à la licence appropriée pour votre projet dépasse le cadre de ce livre. De nombreuses personnes dans la communauté Rust licencient leurs projets de la même manière que Rust en utilisant une double licence de `MIT OU Apache-2.0`. Cette pratique démontre que vous pouvez également spécifier plusieurs identifiants de licence séparés par `OU` pour avoir plusieurs licences pour votre projet.

Avec un nom unique, la version, votre description et une licence ajoutées, le fichier _Cargo.toml_ d'un projet prêt à publier pourrait ressembler à ceci :

<span class="filename">Nom de fichier : Cargo.toml</span>

```toml
[package]
name = "guessing_game"
version = "0.1.0"
edition = "2024"
description = "Un jeu amusant où vous devinez quel numéro l'ordinateur a choisi."
license = "MIT OU Apache-2.0"

[dependencies]
```

La [documentation de Cargo](https://doc.rust-lang.org/cargo/) décrit d'autres métadonnées que vous pouvez spécifier pour garantir que d'autres peuvent découvrir et utiliser votre crate plus facilement.

### Publier sur Crates.io

Maintenant que vous avez créé un compte, enregistré votre jeton API, choisi un nom pour votre crate et spécifié les métadonnées requises, vous êtes prêt à publier ! Publier un crate télécharge une version spécifique sur [crates.io](https://crates.io/)<!-- ignore --> pour que d'autres puissent l'utiliser.

Soyez prudent, car une publication est _permanente_. La version ne peut jamais être écrasée et le code ne peut pas être supprimé sauf dans certaines circonstances. Un objectif majeur de Crates.io est d'agir comme un archive permanent du code afin que les constructions de tous les projets qui dépendent de crates de [crates.io](https://crates.io/) continuent de fonctionner. Permettre les suppressions de versions rendrait cet objectif impossible. Cependant, il n'y a aucune limite au nombre de versions de crate que vous pouvez publier.

Exécutez à nouveau la commande `cargo publish`. Cela devrait réussir maintenant :

```console
$ cargo publish
    Mise à jour de l'index de crates.io
   Packaging guessing_game v0.1.0 (file:///projects/guessing_game)
    Packaged 6 files, 1.2KiB (895.0B compressé)
   Vérification de guessing_game v0.1.0 (file:///projects/guessing_game)
   Compilation de guessing_game v0.1.0
(file:///projects/guessing_game/target/package/guessing_game-0.1.0)
    Profil `dev` terminé [non optimisé + informations de débogage] cible(s) en 0.19s
   Téléversement de guessing_game v0.1.0 (file:///projects/guessing_game)
    Uploaded guessing_game v0.1.0 au registre `crates-io`
note : en attente que `guessing_game v0.1.0` soit disponible au registre `crates-io`.
Vous pouvez appuyer sur ctrl-c pour ignorer l'attente ; le crate devrait être disponible sous peu.
   Publié guessing_game v0.1.0 au registre `crates-io`
```

Félicitations ! Vous avez maintenant partagé votre code avec la communauté Rust, et tout le monde peut facilement ajouter votre crate comme une dépendance de son projet.

### Publier une Nouvelle Version d'une Crate Existante

Lorsque vous avez apporté des modifications à votre crate et êtes prêt à publier une nouvelle version, vous modifiez la valeur `version` spécifiée dans votre fichier _Cargo.toml_ et republiez. Utilisez les règles de [Versionnement Sémantique][semver] pour décider quel numéro de version suivant est approprié, en fonction des types de modifications que vous avez apportées. Ensuite, exécutez `cargo publish` pour télécharger la nouvelle version.

### Déprécier des Versions de Crates.io

Bien que vous ne puissiez pas supprimer les versions précédentes d'un crate, vous pouvez empêcher de nouveaux projets de les ajouter comme nouvelle dépendance. Cela est utile lorsqu'une version d'un crate est cassée pour une raison ou une autre. Dans de telles situations, Cargo prend en charge le fait de _déprécier_ une version de crate.

_Déprécier_ une version empêche de nouveaux projets de dépendre de cette version tout en permettant à tous les projets existants qui en dépendent de continuer. Essentiellement, un dépréciation signifie que tous les projets avec un _Cargo.lock_ ne seront pas brisés, et tous les futurs fichiers _Cargo.lock_ générés ne traiteront pas la version dépréciée.

Pour déprécier une version d'un crate, dans le répertoire de la crate que vous avez précédemment publiée, exécutez `cargo yank` et spécifiez quelle version vous souhaitez déprécier. Par exemple, si nous avons publié un crate nommé `guessing_game` version 1.0.1 et que nous souhaitons le déprécier, alors nous exécuterions ce qui suit dans le répertoire du projet pour `guessing_game` :

```console
$ cargo yank --vers 1.0.1
    Mise à jour de l'index de crates.io
        Dépréciation de guessing_game@1.0.1
```

En ajoutant `--undo` à la commande, vous pouvez également annuler un dépréciation et permettre aux projets de commencer à dépendre d'une version à nouveau :

```console
$ cargo yank --vers 1.0.1 --undo
    Mise à jour de l'index de crates.io
      Annuler la dépréciation de guessing_game@1.0.1
```

Une dépréciation _ne supprime pas_ de code. Elle ne peut pas, par exemple, supprimer des secrets téléchargés accidentellement. Si cela se produit, vous devez réinitialiser ces secrets immédiatement.

[spdx]: https://spdx.org/licenses/  
[semver]: https://semver.org/