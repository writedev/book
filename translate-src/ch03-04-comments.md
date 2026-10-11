## Commentaires

Tous les programmeurs s’efforcent de rendre leur code facile à comprendre, mais il est parfois nécessaire d’ajouter des explications. Dans ces cas-là, les programmeurs laissent des _commentaires_ dans leur code source, que le compilateur ignore, mais qui peuvent être utiles aux personnes qui lisent le code source.

Voici un commentaire simple :

```rust
// hello, world
```

En Rust, la convention consiste à commencer un commentaire par deux barres obliques, et le commentaire se poursuit jusqu’à la fin de la ligne. Pour les commentaires qui s’étendent sur plusieurs lignes, vous devez inclure `//` sur chaque ligne, comme ceci :

```rust
// So we're doing something complicated here, long enough that we need
// multiple lines of comments to do it! Whew! Hopefully, this comment will
// explain what's going on.
```

Les commentaires peuvent aussi être placés à la fin des lignes qui contiennent du code :

<span class="filename">Nom du fichier : src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-24-comments-end-of-line/src/main.rs}}
```

Mais vous les verrez plus souvent sous cette forme, avec le commentaire sur une ligne distincte au-dessus du code qu’il annote :

<span class="filename">Nom du fichier : src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-25-comments-above-line/src/main.rs}}
```

Rust possède également un autre type de commentaire, les commentaires de documentation, dont nous parlerons dans la section [« Publier une crate sur Crates.io »][publishing]<!-- ignore --> du chapitre 14.

[publishing]: ch14-02-publishing-to-crates-io.html