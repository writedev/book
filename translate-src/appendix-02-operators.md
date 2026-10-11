## Annexe B : opérateurs et symboles

Cette annexe contient un glossaire de la syntaxe de Rust, notamment les opérateurs et
les autres symboles qui apparaissent seuls ou dans le contexte des chemins, des génériques,
des contraintes de trait, des macros, des attributs, des commentaires, des tuples et des
crochets.

### Opérateurs

Le tableau B-1 contient les opérateurs de Rust, un exemple illustrant leur utilisation
dans leur contexte, une brève explication et indique si l’opérateur est surchargeable.
Si un opérateur est surchargeable, le trait correspondant à utiliser pour le
surcharger est indiqué.

<span class="caption">Tableau B-1 : opérateurs</span>

| Opérateur                 | Exemple                                                 | Explication                                                           | Surchargeable ? |
| ------------------------- | ------------------------------------------------------- | --------------------------------------------------------------------- | -------------- |
| `!`                       | `ident!(...)`, `ident!{...}`, `ident![...]`             | Expansion de macro                                                    |                |
| `!`                       | `!expr`                                                 | Complément bit à bit ou logique                                       | `Not`          |
| `!=`                      | `expr != expr`                                          | Comparaison d’inégalité                                               | `PartialEq`    |
| `%`                       | `expr % expr`                                           | Reste arithmétique                                                    | `Rem`          |
| `%=`                      | `var %= expr`                                           | Reste arithmétique et affectation                                     | `RemAssign`    |
| `&`                       | `&expr`, `&mut expr`                                    | Emprunt                                                                |                |
| `&`                       | `&type`, `&mut type`, `&'a type`, `&'a mut type`        | Type pointeur emprunté                                                |                |
| `&`                       | `expr & expr`                                           | ET bit à bit                                                          | `BitAnd`       |
| `&=`                      | `var &= expr`                                           | ET bit à bit et affectation                                           | `BitAndAssign` |
| `&&`                      | `expr && expr`                                          | ET logique avec court-circuit                                         |                |
| `*`                       | `expr * expr`                                           | Multiplication arithmétique                                           | `Mul`          |
| `*=`                      | `var *= expr`                                           | Multiplication arithmétique et affectation                            | `MulAssign`    |
| `*`                       | `*expr`                                                 | Déréférencement                                                       | `Deref`        |
| `*`                       | `*const type`, `*mut type`                              | Pointeur brut                                                         |                |
| `+`                       | `trait + trait`, `'a + trait`                           | Contrainte de type composée                                           |                |
| `+`                       | `expr + expr`                                           | Addition arithmétique                                                 | `Add`          |
| `+=`                      | `var += expr`                                           | Addition arithmétique et affectation                                  | `AddAssign`    |
| `,`                       | `expr, expr`                                            | Séparateur d’arguments et d’éléments                                  |                |
| `-`                       | `- expr`                                                | Négation arithmétique                                                 | `Neg`          |
| `-`                       | `expr - expr`                                           | Soustraction arithmétique                                             | `Sub`          |
| `-=`                      | `var -= expr`                                           | Soustraction arithmétique et affectation                              | `SubAssign`    |
| `->`                      | `fn(...) -> type`, <code>&vert;...&vert; -> type</code> | Type de retour d’une fonction ou d’une fermeture                     |                |
| `.`                       | `expr.ident`                                            | Accès à un champ                                                      |                |
| `.`                       | `expr.ident(expr, ...)`                                 | Appel de méthode                                                      |                |
| `.`                       | `expr.0`, `expr.1`, et ainsi de suite                   | Indexation d’un tuple                                                 |                |
| `..`                      | `..`, `expr..`, `..expr`, `expr..expr`                  | Littéral d’intervalle ouvert à droite                                 | `PartialOrd`   |
| `..=`                     | `..=expr`, `expr..=expr`                                | Littéral d’intervalle fermé à droite                                  | `PartialOrd`   |
| `..`                      | `..expr`                                                | Syntaxe de mise à jour d’un littéral de structure                     |                |
| `..`                      | `variant(x, ..)`, `struct_type { x, .. }`               | Liaison de motif « et le reste »                                      |                |
| `...`                     | `expr...expr`                                           | (Obsolète, utiliser `..=` à la place) Dans un motif : intervalle inclusif | `PartialOrd` |
| `/`                       | `expr / expr`                                           | Division arithmétique                                                 | `Div`          |
| `/=`                      | `var /= expr`                                           | Division arithmétique et affectation                                  | `DivAssign`    |
| `:`                       | `pat: type`, `ident: type`                              | Contraintes                                                            |                |
| `:`                       | `ident: expr`                                           | Initialisation d’un champ de structure                                |                |
| `:`                       | `'a: loop {...}`                                        | Étiquette de boucle                                                   |                |
| `;`                       | `expr;`                                                 | Terminateur d’instruction et d’élément                                |                |
| `;`                       | `[...; len]`                                            | Partie de la syntaxe des tableaux de taille fixe                       |                |
| `<<`                      | `expr << expr`                                          | Décalage vers la gauche                                               | `Shl`          |
| `<<=`                     | `var <<= expr`                                          | Décalage vers la gauche et affectation                                | `ShlAssign`    |
| `<`                       | `expr < expr`                                           | Comparaison « inférieur à »                                           | `PartialOrd`   |
| `<=`                      | `expr <= expr`                                          | Comparaison « inférieur ou égal à »                                  | `PartialOrd`   |
| `=`                       | `var = expr`, `ident = type`                            | Affectation/équivalence                                               |                |
| `==`                      | `expr == expr`                                          | Comparaison d’égalité                                                 | `PartialEq`    |
| `=>`                      | `pat => expr`                                           | Partie de la syntaxe d’un bras de match                               |                |
| `>`                       | `expr > expr`                                           | Comparaison « supérieur à »                                           | `PartialOrd`   |
| `>=`                      | `expr >= expr`                                          | Comparaison « supérieur ou égal à »                                  | `PartialOrd`   |
| `>>`                      | `expr >> expr`                                          | Décalage vers la droite                                               | `Shr`          |
| `>>=`                     | `var >>= expr`                                          | Décalage vers la droite et affectation                                | `ShrAssign`    |
| `@`                       | `ident @ pat`                                           | Liaison de motif                                                      |                |
| `^`                       | `expr ^ expr`                                           | OU exclusif bit à bit                                                 | `BitXor`       |
| `^=`                      | `var ^= expr`                                           | OU exclusif bit à bit et affectation                                  | `BitXorAssign` |
| <code>&vert;</code>       | <code>pat &vert; pat</code>                             | Alternatives de motifs                                                |                |
| <code>&vert;</code>       | <code>expr &vert; expr</code>                           | OU bit à bit                                                          | `BitOr`        |
| <code>&vert;=</code>      | <code>var &vert;= expr</code>                           | OU bit à bit et affectation                                           | `BitOrAssign`  |
| <code>&vert;&vert;</code> | <code>expr &vert;&vert; expr</code>                     | OU logique avec court-circuit                                         |                |
| `?`                       | `expr?`                                                 | Propagation des erreurs                                               |                |

### Symboles non opérateurs

Les tableaux suivants présentent tous les symboles qui ne fonctionnent pas comme des
opérateurs, c’est-à-dire qui ne se comportent pas comme un appel de fonction ou de méthode.

Le tableau B-2 présente les symboles qui apparaissent seuls et sont valides dans différents
emplacements.

<span class="caption">Tableau B-2 : syntaxe autonome</span>

| Symbole                                                                | Explication                                                           |
| ---------------------------------------------------------------------- | --------------------------------------------------------------------- |
| `'ident`                                                               | Durée de vie nommée ou étiquette de boucle                            |
| Chiffres immédiatement suivis de `u8`, `i32`, `f64`, `usize`, etc.     | Littéral numérique d’un type précis                                   |
| `"..."`                                                                | Littéral de chaîne                                                    |
| `r"..."`, `r#"..."#`, `r##"..."##`, et ainsi de suite                  | Littéral de chaîne brute ; les caractères d’échappement ne sont pas traités |
| `b"..."`                                                               | Littéral de chaîne d’octets ; construit un tableau d’octets plutôt qu’une chaîne |
| `br"..."`, `br#"..."#`, `br##"..."##`, et ainsi de suite               | Littéral de chaîne brute d’octets ; combinaison d’un littéral brut et d’un littéral de chaîne d’octets |
| `'...'`                                                                | Littéral de caractère                                                 |
| `b'...'`                                                               | Littéral d’octet ASCII                                                |
| <code>&vert;...&vert; expr</code>                                      | Fermeture                                                             |
| `!`                                                                    | Type bottom toujours vide pour les fonctions divergentes              |
| `_`                                                                    | Liaison de motif « ignorée » ; également utilisé pour faciliter la lecture des littéraux entiers |

Le tableau B-3 présente les symboles qui apparaissent dans le contexte d’un chemin
parcourant la hiérarchie des modules jusqu’à un élément.

<span class="caption">Tableau B-3 : syntaxe liée aux chemins</span>

| Symbole                                  | Explication                                                                                                  |
| --------------------------------------- | -------------------------------------------------------------------------------------------------------------|
| `ident::ident`                          | Chemin d’espace de noms                                                                                      |
| `::path`                                | Chemin relatif à la racine de la caisse (c’est-à-dire un chemin explicitement absolu)                        |
| `self::path`                            | Chemin relatif au module actuel (c’est-à-dire un chemin explicitement relatif)                              |
| `super::path`                           | Chemin relatif au parent du module actuel                                                                    |
| `type::ident`, `<type as trait>::ident` | Constantes, fonctions et types associés                                                                      |
| `<type>::...`                           | Élément associé à un type qui ne peut pas être nommé directement (par exemple, `<&T>::...`, `<[T]>::...`, etc.) |
| `trait::method(...)`                    | Désambiguïsation d’un appel de méthode en nommant le trait qui la définit                                    |
| `type::method(...)`                     | Désambiguïsation d’un appel de méthode en nommant le type pour lequel elle est définie                      |
| `<type as trait>::method(...)`          | Désambiguïsation d’un appel de méthode en nommant le trait et le type                                        |

Le tableau B-4 présente les symboles qui apparaissent dans le contexte de l’utilisation
de paramètres de type génériques.

<span class="caption">Tableau B-4 : génériques</span>

| Symbole                         | Explication                                                                                                                                         |
| ------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| `path<...>`                    | Spécifie les paramètres d’un type générique dans un type (par exemple, `Vec<u8>`)                                                                   |
| `path::<...>`, `method::<...>` | Spécifie les paramètres d’un type générique, d’une fonction ou d’une méthode dans une expression ; souvent appelé _turbofish_ (par exemple, `"42".parse::<i32>()`) |
| `fn ident<...> ...`            | Définition d’une fonction générique                                                                                                                 |
| `struct ident<...> ...`        | Définition d’une structure générique                                                                                                                |
| `enum ident<...> ...`          | Définition d’une énumération générique                                                                                                              |
| `impl<...> ...`                | Définition d’une implémentation générique                                                                                                           |
| `for<...> type`                | Contraintes de durée de vie à rang supérieur                                                                                                       |
| `type<ident=type>`             | Type générique où un ou plusieurs types associés ont des affectations précises (par exemple, `Iterator<Item=T>`)                                    |

Le tableau B-5 présente les symboles qui apparaissent dans le contexte des contraintes
imposées aux paramètres de type génériques au moyen de contraintes de trait.

<span class="caption">Tableau B-5 : contraintes de borne de trait</span>

| Symbole                        | Explication                                                                                                                                |
| ----------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| `T: U`                        | Paramètre générique `T` contraint aux types qui implémentent `U`                                                                            |
| `T: 'a`                       | Le type générique `T` doit vivre plus longtemps que la durée de vie `'a` (c’est-à-dire que le type ne peut contenir, même indirectement, de références dont la durée de vie est plus courte que `'a`) |
| `T: 'static`                  | Le type générique `T` ne contient aucune référence empruntée autre que celles de durée de vie `'static`                                     |
| `'b: 'a`                      | La durée de vie générique `'b` doit vivre plus longtemps que la durée de vie `'a`                                                           |
| `T: ?Sized`                   | Autorise le paramètre de type générique à être un type dont la taille est déterminée dynamiquement                                        |
| `'a + trait`, `trait + trait` | Contrainte de type composée                                                                                                                 |

Le tableau B-6 présente les symboles qui apparaissent dans le contexte de l’appel ou de la
définition de macros et de la spécification d’attributs sur un élément.

<span class="caption">Tableau B-6 : macros et attributs</span>

| Symbole                                      | Explication          |
| ------------------------------------------- | -------------------- |
| `#[meta]`                                   | Attribut externe     |
| `#![meta]`                                  | Attribut interne     |
| `$ident`                                    | Substitution de macro |
| `$ident:kind`                               | Métavariable de macro |
| `$(...)...`                                 | Répétition de macro  |
| `ident!(...)`, `ident!{...}`, `ident![...]` | Appel de macro       |

Le tableau B-7 présente les symboles qui créent des commentaires.

<span class="caption">Tableau B-7 : commentaires</span>

| Symbole    | Explication                 |
| ---------- | --------------------------- |
| `//`       | Commentaire de ligne        |
| `//!`      | Commentaire de documentation de ligne interne |
| `///`      | Commentaire de documentation de ligne externe |
| `/*...*/`  | Commentaire de bloc         |
| `/*!...*/` | Commentaire de documentation de bloc interne |
| `/**...*/` | Commentaire de documentation de bloc externe |

Le tableau B-8 présente les contextes dans lesquels les parenthèses sont utilisées.

<span class="caption">Tableau B-8 : parenthèses</span>

| Symbole            | Explication                                                                                 |
| ------------------ | ------------------------------------------------------------------------------------------- |
| `()`               | Tuple vide (aussi appelé unité), à la fois littéral et type                                 |
| `(expr)`           | Expression entre parenthèses                                                                |
| `(expr,)`          | Expression de tuple à un seul élément                                                       |
| `(type,)`          | Type tuple à un seul élément                                                                |
| `(expr, ...)`      | Expression de tuple                                                                          |
| `(type, ...)`      | Type tuple                                                                                  |
| `expr(expr, ...)`  | Expression d’appel de fonction ; également utilisée pour initialiser des `struct` tuple et des variantes d’`enum` tuple |

Le tableau B-9 présente les contextes dans lesquels les accolades sont utilisées.

<span class="caption">Tableau B-9 : accolades</span>

| Contexte    | Explication           |
| ----------- | --------------------- |
| `{...}`     | Expression de bloc    |
| `Type {...}` | Littéral de structure |

Le tableau B-10 présente les contextes dans lesquels les crochets sont utilisés.

<span class="caption">Tableau B-10 : crochets</span>

| Contexte                                            | Explication                                                                                                                   |
| -------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| `[...]`                                            | Littéral de tableau                                                                                                           |
| `[expr; len]`                                      | Littéral de tableau contenant `len` copies de `expr`                                                                          |
| `[type; len]`                                      | Type tableau contenant `len` instances de `type`                                                                              |
| `expr[expr]`                                       | Indexation de collection ; surchargeable (`Index`, `IndexMut`)                                                                |
| `expr[..]`, `expr[a..]`, `expr[..b]`, `expr[a..b]` | Indexation de collection simulant une opération de découpage, en utilisant `Range`, `RangeFrom`, `RangeTo` ou `RangeFull` comme « index » |