## Commentaires

Tous les programmeurs s'efforcent de rendre leur code facile à comprendre, mais parfois une explication supplémentaire est justifiée. Dans ces cas, les programmeurs laissent des _commentaires_ dans leur code source que le compilateur ignorera, mais que les personnes lisant le code source pourraient trouver utiles.

Voici un simple commentaire :

```rust
// bonjour, le monde
```

En Rust, le style de commentaire idiomatique commence un commentaire par deux barres obliques, et le commentaire continue jusqu'à la fin de la ligne. Pour les commentaires qui s'étendent au-delà d'une seule ligne, vous devez inclure `//` sur chaque ligne, comme ceci :

```rust
// Donc, nous faisons quelque chose de compliqué ici, assez long pour que nous 
// ayons besoin de plusieurs lignes de commentaires pour le faire ! Ouf ! 
// J'espère que ce commentaire expliquera ce qui se passe.
```

Les commentaires peuvent également être placés à la fin des lignes contenant du code :

<span class="filename">Nom du fichier : src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-24-comments-end-of-line/src/main.rs}}
```

Mais vous les verrez plus souvent utilisés dans ce format, avec le commentaire sur une ligne séparée au-dessus du code qu'il annotent :

<span class="filename">Nom du fichier : src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-25-comments-above-line/src/main.rs}}
```

Rust a également un autre type de commentaire, les commentaires de documentation, que nous aborderons dans la section [« Publier un Crate sur Crates.io »][publishing]<!-- ignore -->
du Chapitre 14.

[publishing]: ch14-02-publishing-to-crates-io.html