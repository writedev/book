## Annexe A : Mots-clés

Les listes suivantes contiennent les mots-clés réservés à un usage actuel ou
futur par le langage Rust. Ils ne peuvent donc pas être utilisés comme
identifiants (sauf en tant qu’identifiants bruts, comme nous l’expliquons dans
la section [« Identifiants bruts »][raw-identifiers]<!-- ignore -->). Les
_identifiants_ sont les noms des fonctions, variables, paramètres, champs de
structure, modules, crates, constantes, macros, valeurs statiques, attributs,
types, traits ou durées de vie.

[raw-identifiers]: #raw-identifiers

### Mots-clés actuellement utilisés

Voici la liste des mots-clés actuellement utilisés, avec une description de
leur fonction.

- **`as`** : Effectuer une conversion de type primitif, désambiguïser le trait
  spécifique qui contient un élément, ou renommer des éléments dans des
  instructions `use`.
- **`async`** : Renvoyer un `Future` au lieu de bloquer le thread actuel.
- **`await`** : Suspendre l’exécution jusqu’à ce que le résultat d’un `Future`
  soit prêt.
- **`break`** : Quitter immédiatement une boucle.
- **`const`** : Définir des éléments constants ou des pointeurs bruts constants.
- **`continue`** : Passer à l’itération suivante de la boucle.
- **`crate`** : Dans un chemin de module, désigne la racine de la crate.
- **`dyn`** : Effectuer une répartition dynamique vers un objet de trait.
- **`else`** : Définir une alternative pour les constructions de contrôle de
  flux `if` et `if let`.
- **`enum`** : Définir une énumération.
- **`extern`** : Lier une fonction ou une variable externe.
- **`false`** : Littéral booléen faux.
- **`fn`** : Définir une fonction ou le type pointeur de fonction.
- **`for`** : Parcourir les éléments d’un itérateur, implémenter un trait ou
  spécifier une durée de vie à liaison supérieure.
- **`if`** : Effectuer un branchement selon le résultat d’une expression
  conditionnelle.
- **`impl`** : Implémenter des fonctionnalités inhérentes ou celles d’un trait.
- **`in`** : Fait partie de la syntaxe des boucles `for`.
- **`let`** : Lier une variable.
- **`loop`** : Boucler sans condition.
- **`match`** : Faire correspondre une valeur à des motifs.
- **`mod`** : Définir un module.
- **`move`** : Faire en sorte qu’une fermeture prenne possession de toutes ses
  captures.
- **`mut`** : Indiquer la mutabilité dans les références, les pointeurs bruts
  ou les liaisons de motifs.
- **`pub`** : Indiquer une visibilité publique dans les champs de structure,
  les blocs `impl` ou les modules.
- **`ref`** : Lier par référence.
- **`return`** : Renvoyer une valeur depuis une fonction.
- **`Self`** : Alias de type pour le type que nous définissons ou implémentons.
- **`self`** : Sujet d’une méthode ou module actuel.
- **`static`** : Variable globale ou durée de vie couvrant toute l’exécution du
  programme.
- **`struct`** : Définir une structure.
- **`super`** : Module parent du module actuel.
- **`trait`** : Définir un trait.
- **`true`** : Littéral booléen vrai.
- **`type`** : Définir un alias de type ou un type associé.
- **`union`** : Définir une [union][union]<!-- ignore --> ; c’est un mot-clé
  uniquement lorsqu’il est utilisé dans une déclaration d’union.
- **`unsafe`** : Indiquer du code, des fonctions, des traits ou des
  implémentations non sûrs.
- **`use`** : Introduire des symboles dans la portée.
- **`where`** : Indiquer des clauses qui imposent des contraintes à un type.
- **`while`** : Boucler sous condition, selon le résultat d’une expression.

[union]: ../reference/items/unions.html

### Mots-clés réservés à un usage futur

Les mots-clés suivants n’ont pas encore de fonction, mais sont réservés par
Rust en vue d’un éventuel usage futur :

- `abstract`
- `become`
- `box`
- `do`
- `final`
- `gen`
- `macro`
- `override`
- `priv`
- `try`
- `typeof`
- `unsized`
- `virtual`
- `yield`

### Identifiants bruts

Les _identifiants bruts_ sont une syntaxe qui permet d’utiliser des mots-clés
là où ils ne seraient normalement pas autorisés. Pour utiliser un identifiant
brut, préfixez un mot-clé par `r#`.

Par exemple, `match` est un mot-clé. Si vous essayez de compiler la fonction
suivante, qui utilise `match` comme nom :

<span class="filename">Nom du fichier : src/main.rs</span>

```rust,ignore,does_not_compile
fn match(needle: &str, haystack: &str) -> bool {
    haystack.contains(needle)
}
```

vous obtiendrez cette erreur :

```text
error: expected identifier, found keyword `match`
 --> src/main.rs:4:4
  |
4 | fn match(needle: &str, haystack: &str) -> bool {
  |    ^^^^^ expected identifier, found keyword
```

L’erreur montre que vous ne pouvez pas utiliser le mot-clé `match` comme
identifiant de fonction. Pour utiliser `match` comme nom de fonction, vous
devez recourir à la syntaxe des identifiants bruts, comme ceci :

<span class="filename">Nom du fichier : src/main.rs</span>

```rust
fn r#match(needle: &str, haystack: &str) -> bool {
    haystack.contains(needle)
}

fn main() {
    assert!(r#match("foo", "foobar"));
}
```

Ce code se compile sans erreur. Notez le préfixe `r#` dans le nom de la
fonction, à la fois dans sa définition et à l’endroit où elle est appelée dans
`main`.

Les identifiants bruts vous permettent d’utiliser n’importe quel mot comme
identifiant, même s’il s’agit d’un mot-clé réservé. Vous avez ainsi davantage
de liberté dans le choix des noms d’identifiants et pouvez également intégrer
des programmes écrits dans un langage où ces mots ne sont pas des mots-clés.
De plus, les identifiants bruts vous permettent d’utiliser des bibliothèques
écrites dans une édition de Rust différente de celle de votre crate. Par
exemple, `try` n’est pas un mot-clé dans l’édition 2015, mais il l’est dans les
éditions 2018, 2021 et 2024. Si vous dépendez d’une bibliothèque écrite avec
l’édition 2015 et qui possède une fonction `try`, vous devrez utiliser la
syntaxe des identifiants bruts — `r#try` dans ce cas — pour appeler cette
fonction depuis votre code avec une édition ultérieure. Consultez
[l’annexe E][appendix-e]<!-- ignore --> pour en savoir plus sur les éditions.

[appendix-e]: appendix-05-editions.html