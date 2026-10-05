## Annexe B : Opérateurs et Symboles

Cette annexe contient un glossaire de la syntaxe de Rust, y compris les opérateurs et d'autres symboles qui apparaissent seuls ou dans le contexte des chemins, des génériques, des limites de traits, des macros, des attributs, des commentaires, des tuples et des crochets.

### Opérateurs

Le tableau B-1 contient les opérateurs en Rust, un exemple de la façon dont l'opérateur apparaîtrait dans le contexte, une explication courte et si cet opérateur est surchargé. Si un opérateur est surchargé, le trait pertinent à utiliser pour surcharger cet opérateur est listé.

<span class="caption">Tableau B-1 : Opérateurs</span>

| Opérateur                  | Exemple                                                 | Explication                                                           | Surchargé ?      |
| ------------------------- | ------------------------------------------------------- | --------------------------------------------------------------------- | -------------- |
| `!`                       | `ident!(...)`, `ident!{...}`, `ident![...]`             | Expansion de macro                                                    |                |
| `!`                       | `!expr`                                                 | Complément bitwise ou logique                                         | `Not`          |
| `!=`                      | `expr != expr`                                          | Comparaison d'inégalité                                               | `PartialEq`    |
| `%`                       | `expr % expr`                                           | Reste arithmétique                                                   | `Rem`          |
| `%=`                      | `var %= expr`                                           | Reste arithmétique et affectation                                    | `RemAssign`    |
| `&`                       | `&expr`, `&mut expr`                                    | Emprunt                                                             |                |
| `&`                       | `&type`, `&mut type`, `&'a type`, `&'a mut type`        | Type de pointeur emprunté                                            |                |
| `&`                       | `expr & expr`                                           | ET bitwise                                                           | `BitAnd`       |
| `&=`                      | `var &= expr`                                           | ET bitwise et affectation                                            | `BitAndAssign` |
| `&&`                      | `expr && expr`                                          | ET logique à court-circuit                                           |                |
| `*`                       | `expr * expr`                                           | Multiplication arithmétique                                          | `Mul`          |
| `*=`                      | `var *= expr`                                           | Multiplication arithmétique et affectation                           | `MulAssign`    |
| `*`                       | `*expr`                                                 | Déréférencement                                                       | `Deref`        |
| `*`                       | `*const type`, `*mut type`                              | Pointeur brut                                                        |                |
| `+`                       | `trait + trait`, `'a + trait`                           | Contrainte de type composite                                         |                |
| `+`                       | `expr + expr`                                           | Addition arithmétique                                                | `Add`          |
| `+=`                      | `var += expr`                                           | Addition arithmétique et affectation                                 | `AddAssign`    |
| `,`                       | `expr, expr`                                            | Séparateur d'argument et d'élément                                   |                |
| `-`                       | `- expr`                                                | Négation arithmétique                                                | `Neg`          |
| `-`                       | `expr - expr`                                           | Soustraction arithmétique                                           | `Sub`          |
| `-=`                      | `var -= expr`                                           | Soustraction arithmétique et affectation                             | `SubAssign`    |
| `->`                      | `fn(...) -> type`, <code>&vert;...&vert; -> type</code> | Type de retour de fonction et de fermeture                            |                |
| `.`                       | `expr.ident`                                            | Accès au champ                                                       |                |
| `.`                       | `expr.ident(expr, ...)`                                 | Appel de méthode                                                    |                |
| `.`                       | `expr.0`, `expr.1`, etc.                               | Indexation de tuple                                                  |                |
| `..`                      | `..`, `expr..`, `..expr`, `expr..expr`                  | Littéral de plage droite-exclusif                                     | `PartialOrd`   |
| `..=`                     | `..=expr`, `expr..=expr`                                | Littéral de plage droite-inclusif                                     | `PartialOrd`   |
| `..`                      | `..expr`                                                | Syntaxe de mise à jour de la structure                                |                |
| `..`                      | `variant(x, ..)`, `struct_type { x, .. }`               | Liaison de motif « Et le reste »                                      |                |
| `...`                     | `expr...expr`                                           | (Déprécié, utilisez `..=` à la place) Dans un motif : motif de plage inclusif |                |
| `/`                       | `expr / expr`                                           | Division arithmétique                                               | `Div`          |
| `/=`                      | `var /= expr`                                           | Division arithmétique et affectation                                 | `DivAssign`    |
| `:`                       | `pat: type`, `ident: type`                              | Contraintes                                                          |                |
| `:`                       | `ident: expr`                                           | Initialisation de champ de structure                                  |                |
| `:`                       | `'a: loop {...}`                                        | Étiquette de boucle                                                  |                |
| `;`                       | `expr;`                                                 | Terminal de déclaration et d'élément                                  |                |
| `;`                       | `[...; len]`                                            | Partie de la syntaxe de tableau à taille fixe                        |                |
| `<<`                      | `expr << expr`                                          | Décalage à gauche                                                    | `Shl`          |
| `<<=`                     | `var <<= expr`                                          | Décalage à gauche et affectation                                     | `ShlAssign`    |
| `<`                       | `expr < expr`                                           | Comparaison inférieure                                              | `PartialOrd`   |
| `<=`                      | `expr <= expr`                                          | Comparaison inférieure ou égale                                      | `PartialOrd`   |
| `=`                       | `var = expr`, `ident = type`                            | Affectation/équivalence                                              |                |
| `==`                      | `expr == expr`                                          | Comparaison d'égalité                                               | `PartialEq`    |
| `=>`                      | `pat => expr`                                           | Partie de la syntaxe de bras de correspondance                      |                |
| `>`                       | `expr > expr`                                           | Comparaison supérieure                                              | `PartialOrd`   |
| `>=`                      | `expr >= expr`                                          | Comparaison supérieure ou égale                                      | `PartialOrd`   |
| `>>`                      | `expr >> expr`                                          | Décalage à droite                                                   | `Shr`          |
| `>>=`                     | `var >>= expr`                                          | Décalage à droite et affectation                                     | `ShrAssign`    |
| `@`                       | `ident @ pat`                                           | Liaison de motif                                                     |                |
| `^`                       | `expr ^ expr`                                           | OU exclusif bitwise                                                 | `BitXor`       |
| `^=`                      | `var ^= expr`                                           | OU exclusif bitwise et affectation                                   | `BitXorAssign` |
| <code>&vert;</code>       | <code>pat &vert; pat</code>                             | Alternatives de motifs                                               |                |
| <code>&vert;</code>       | <code>expr &vert; expr</code>                           | OU bitwise                                                         | `BitOr`        |
| <code>&vert;=</code>      | <code>var &vert;= expr</code>                           | OU bitwise et affectation                                           | `BitOrAssign`  |
| <code>&vert;&vert;</code> | <code>expr &vert;&vert; expr</code>                     | OU logique à court-circuit                                          |                |
| `?`                       | `expr?`                                                 | Propagation des erreurs                                             |                |

### Symboles non-opérateurs

Les tableaux suivants contiennent tous les symboles qui ne fonctionnent pas comme des opérateurs ; c'est-à-dire qu'ils ne se comportent pas comme un appel de fonction ou de méthode.

Le tableau B-2 montre les symboles qui apparaissent seuls et sont valides dans une variété de contextes.

<span class="caption">Tableau B-2 : Syntaxe autonome</span>

| Symbole                                                               | Explication                                                            |
| ---------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| `'ident`                                                               | Durée de vie nommée ou étiquette de boucle                             |
| Chiffres suivis immédiatement de `u8`, `i32`, `f64`, `usize`, etc.    | Littéral numérique d'un type spécifique                                |
| `"..."`                                                                | Littéral de chaîne                                                    |
| `r"..."`, `r#"..."#`, `r##"..."##`, etc.                              | Littéral de chaîne brut ; les caractères d'échappement ne sont pas traités |
| `b"..."`                                                               | Littéral de chaîne de bytes ; construit un tableau de bytes au lieu d'une chaîne |
| `br"..."`, `br#"..."#`, `br##"..."##`, etc.                           | Littéral de chaîne de bytes brut ; combinaison de littéral brut et de chaîne de bytes |
| `'...'`                                                                | Littéral de caractère                                                  |
| `b'...'`                                                               | Littéral de byte ASCII                                                |
| <code>&vert;...&vert; expr</code>                                      | Fermeture                                                             |
| `!`                                                                    | Type vide toujours pour les fonctions divergentes                     |
| `_`                                                                    | Liaison de motif « ignoré » ; utilisé aussi pour rendre les littéraux entiers lisibles |

Le tableau B-3 montre les symboles qui apparaissent dans le contexte d'un chemin à travers la hiérarchie des modules vers un élément.

<span class="caption">Tableau B-3 : Syntaxe liée aux chemins</span>

| Symbole                                  | Explication                                                                                                  |
| --------------------------------------- | -------------------------------------------------------------------------------------------------------------|
| `ident::ident`                          | Chemin de l'espace de noms                                                                                   |
| `::path`                                | Chemin relatif à la racine du crate (c'est-à-dire un chemin explicitement absolu)                            |
| `self::path`                            | Chemin relatif au module actuel (c'est-à-dire un chemin explicitement relatif)                               |
| `super::path`                           | Chemin relatif au parent du module actuel                                                                     |
| `type::ident`, `<type as trait>::ident` | Constantes, fonctions et types associés                                                                        |
| `<type>::...`                           | Élément associé pour un type qui ne peut pas être nommé directement (par exemple, `<&T>::...`, `<[T]>::...`, etc.) |
| `trait::method(...)`                    | Désambiguïser un appel de méthode en nommant le trait qui le définit                                         |
| `type::method(...)`                     | Désambiguïser un appel de méthode en nommant le type pour lequel il est défini                                |
| `<type as trait>::method(...)`          | Désambiguïser un appel de méthode en nommant le trait et le type                                            |

Le tableau B-4 montre les symboles qui apparaissent dans le contexte de l'utilisation de paramètres de type génériques.

<span class="caption">Tableau B-4 : Génériques</span>

| Symbole                         | Explication                                                                                                                                         |
| ------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| `path<...>`                    | Spécifie les paramètres d'un type générique dans un type (par exemple, `Vec<u8>`)                                                                  |
| `path::<...>`, `method::<...>` | Spécifie les paramètres d'un type, d'une fonction ou d'une méthode dans une expression ; souvent appelé _turbofish_ (par exemple, `"42".parse::<i32>()`) |
| `fn ident<...> ...`            | Définir une fonction générique                                                                                                                     |
| `struct ident<...> ...`        | Définir une structure générique                                                                                                                    |
| `enum ident<...> ...`          | Définir une énumération générique                                                                                                                  |
| `impl<...> ...`                | Définir une implémentation générique                                                                                                               |
| `for<...> type`                | Limites de durée de vie de rang supérieur                                                                                                         |
| `type<ident=type>`             | Un type générique où un ou plusieurs types associés ont des affectations spécifiques (par exemple, `Iterator<Item=T>`)                              |

Le tableau B-5 montre les symboles qui apparaissent dans le contexte de la contrainte des paramètres de type génériques avec des limites de traits.

<span class="caption">Tableau B-5 : Contraintes de limites de traits</span>

| Symbole                        | Explication                                                                                                                                |
| ----------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| `T: U`                        | Paramètre générique `T` contraint aux types qui implémentent `U`                                                                          |
| `T: 'a`                       | Le type générique `T` doit survivre à la durée de vie `'a` (ce qui signifie que le type ne peut pas contenir de références dont les durées de vie sont plus courtes que `'a`) |
| `T: 'static`                  | Le type générique `T` ne contient aucune référence empruntée autre que celles de type `'static`                                           |
| `'b: 'a`                      | La durée de vie générique `'b` doit survivre à la durée de vie `'a`                                                                       |
| `T: ?Sized`                   | Autoriser le paramètre de type générique à être un type de taille dynamique                                                               |
| `'a + trait`, `trait + trait` | Contrainte de type composite                                                                                                               |

Le tableau B-6 montre les symboles qui apparaissent dans le contexte de l'appel ou de la définition de macros et de la spécification d'attributs sur un élément.

<span class="caption">Tableau B-6 : Macros et Attributs</span>

| Symbole                                      | Explication        |
| ------------------------------------------- | ------------------ |
| `#[meta]`                                   | Attribut externe    |
| `#![meta]`                                  | Attribut interne    |
| `$ident`                                    | Substitution de macro |
| `$ident:kind`                               | Métavariable de macro |
| `$(...)...`                                 | Répétition de macro   |
| `ident!(...)`, `ident!{...}`, `ident![...]` | Invocation de macro    |

Le tableau B-7 montre les symboles qui créent des commentaires.

<span class="caption">Tableau B-7 : Commentaires</span>

| Symbole     | Explication             |
| ---------- | ----------------------- |
| `//`       | Commentaire sur une ligne |
| `//!`      | Commentaire de doc interne |
| `///`      | Commentaire de doc externe |
| `/*...*/`  | Commentaire en bloc       |
| `/*!...*/` | Commentaire de doc en bloc interne |
| `/**...*/` | Commentaire de doc en bloc externe |

Le tableau B-8 montre les contextes dans lesquels des parenthèses sont utilisées.

<span class="caption">Tableau B-8 : Parenthèses</span>

| Symbole                   | Explication                                                                                 |
| ------------------------ | ------------------------------------------------------------------------------------------- |
| `()`                     | Tuple vide (c'est-à-dire unité), à la fois littéral et type                                  |
| `(expr)`                 | Expression parenthésée                                                                       |
| `(expr,)`                | Expression de tuple à un élément                                                              |
| `(type,)`                | Type de tuple à un élément                                                                    |
| `(expr, ...)`            | Expression de tuple                                                                           |
| `(type, ...)`            | Type de tuple                                                                                 |
| `expr(expr, ...)`        | Expression d'appel de fonction ; utilisée aussi pour initialiser des tuples `struct` et des variantes d'énumérations tuple |

Le tableau B-9 montre les contextes dans lesquels des accolades sont utilisées.

<span class="caption">Tableau B-9 : Accolades</span>

| Contexte      | Explication      |
| ------------ | ---------------- |
| `{...}`      | Expression de bloc |
| `Type {...}` | Littéral de structure |

Le tableau B-10 montre les contextes dans lesquels des crochets sont utilisés.

<span class="caption">Tableau B-10 : Crochets</span>

| Contexte                                            | Explication                                                                                                                   |
| -------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| `[...]`                                            | Littéral de tableau                                                                                                          |
| `[expr; len]`                                      | Littéral de tableau contenant `len` copies de `expr`                                                                        |
| `[type; len]`                                      | Type de tableau contenant `len` instances de `type`                                                                         |
| `expr[expr]`                                       | Indexation de collection ; surchargé (`Index`, `IndexMut`)                                                                  |
| `expr[..]`, `expr[a..]`, `expr[..b]`, `expr[a..b]` | Indexation de collection se faisant passer pour un tranchage de collection, utilisant `Range`, `RangeFrom`, `RangeTo` ou `RangeFull` comme « index » |