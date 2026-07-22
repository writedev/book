## Annexe A : Mots-clés

Les listes suivantes contiennent des mots-clés réservés pour l'utilisation actuelle ou future par le langage Rust. En tant que tels, ils ne peuvent pas être utilisés comme identifiants (sauf en tant qu'identifiants bruts, comme nous l'aborderons dans la section [« Identifiants Bruts »][raw-identifiers]<!-- ignore -->). Les _identifiants_ sont des noms de fonctions, variables, paramètres, champs de structure, modules, crates, constantes, macros, valeurs statiques, attributs, types, traits ou durées de vie.

[raw-identifiers]: #raw-identifiers

### Mots-clés Actuellement en Utilisation

Voici une liste de mots-clés actuellement en usage, avec leur fonctionnalité décrite.

- **`as`** : Effectuer un casting primitif, désambiguïser le trait spécifique contenant un élément ou renommer des éléments dans les instructions `use`.
- **`async`** : Retourner un `Future` au lieu de bloquer le fil d'exécution actuel.
- **`await`** : Suspendre l'exécution jusqu'à ce que le résultat d'un `Future` soit prêt.
- **`break`** : Sortir d'une boucle immédiatement.
- **`const`** : Définir des éléments constants ou des pointeurs bruts constants.
- **`continue`** : Passer à l'itération suivante de la boucle.
- **`crate`** : Dans un chemin de module, désigne la racine de la crate.
- **`dyn`** : Dispatch dynamique vers un objet trait.
- **`else`** : Solution de repli pour les constructions de contrôle `if` et `if let`.
- **`enum`** : Définir une énumération.
- **`extern`** : Lier une fonction ou une variable externe.
- **`false`** : Littéral booléen faux.
- **`fn`** : Définir une fonction ou le type d'un pointeur de fonction.
- **`for`** : Boucler sur des éléments d'un itérateur, implémenter un trait ou spécifier une durée de vie à classement supérieur.
- **`if`** : Brancher en fonction du résultat d'une expression conditionnelle.
- **`impl`** : Implémenter une fonctionnalité inhérente ou de trait.
- **`in`** : Partie de la syntaxe de boucle `for`.
- **`let`** : Lier une variable.
- **`loop`** : Boucler de manière inconditionnelle.
- **`match`** : Appariement d'une valeur à des motifs.
- **`mod`** : Définir un module.
- **`move`** : Faire en sorte qu'une fermeture prenne possession de toutes ses captures.
- **`mut`** : Indiquer la mutabilité dans les références, pointeurs bruts ou liaisons de motifs.
- **`pub`** : Indiquer une visibilité publique dans les champs de structure, blocs `impl` ou modules.
- **`ref`** : Lier par référence.
- **`return`** : Retourner d'une fonction.
- **`Self`** : Un alias de type pour le type que nous définissons ou implémentons.
- **`self`** : Sujet de la méthode ou module courant.
- **`static`** : Variable globale ou durée de vie durant toute l'exécution du programme.
- **`struct`** : Définir une structure.
- **`super`** : Module parent du module actuel.
- **`trait`** : Définir un trait.
- **`true`** : Littéral booléen vrai.
- **`type`** : Définir un alias de type ou un type associé.
- **`union`** : Définir une [union][union]<!-- ignore --> ; est un mot-clé seulement lorsqu'il est utilisé dans une déclaration d'union.
- **`unsafe`** : Indiquer du code, des fonctions, des traits ou des implémentations non sûrs.
- **`use`** : Amener des symboles dans le scope.
- **`where`** : Indiquer des clauses qui contraignent un type.
- **`while`** : Boucler de manière conditionnelle en fonction du résultat d'une expression.

[union]: ../reference/items/unions.html

### Mots-clés Réservés pour une Utilisation Future

Les mots-clés suivants n'ont pas encore de fonctionnalité mais sont réservés par Rust pour une utilisation future potentielle :

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

### Identifiants Bruts

Les _identifiants bruts_ sont la syntaxe qui vous permet d'utiliser des mots-clés là où ils ne seraient normalement pas autorisés. Vous utilisez un identifiant brut en préfixant un mot-clé avec `r#`.

Par exemple, `match` est un mot-clé. Si vous essayez de compiler la fonction suivante qui utilise `match` comme son nom :

<span class="filename">Nom de fichier : src/main.rs</span>

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

L'erreur montre que vous ne pouvez pas utiliser le mot-clé `match` comme identifiant de fonction. Pour utiliser `match` comme nom de fonction, vous devez utiliser la syntaxe d'identifiant brut, comme ceci :

<span class="filename">Nom de fichier : src/main.rs</span>

```rust
fn r#match(needle: &str, haystack: &str) -> bool {
    haystack.contains(needle)
}

fn main() {
    assert!(r#match("foo", "foobar"));
}
```

Ce code se compilera sans erreurs. Notez le préfixe `r#` sur le nom de la fonction dans sa définition ainsi que là où la fonction est appelée dans `main`.

Les identifiants bruts vous permettent d'utiliser n'importe quel mot de votre choix comme identifiant, même si ce mot est un mot-clé réservé. Cela nous donne plus de liberté pour choisir des noms d'identifiants, ainsi que nous permet de nous intégrer avec des programmes écrits dans un langage où ces mots ne sont pas des mots-clés. De plus, les identifiants bruts vous permettent d'utiliser des bibliothèques écrites dans une édition Rust différente de celle utilisée par votre crate. Par exemple, `try` n'est pas un mot-clé dans l'édition 2015 mais l'est dans les éditions 2018, 2021 et 2024. Si vous dépendez d'une bibliothèque écrite en utilisant l'édition 2015 et qu'elle a une fonction `try`, vous devrez utiliser la syntaxe d'identifiant brut, `r#try` dans ce cas, pour appeler cette fonction depuis votre code dans les éditions ultérieures. Voir [Annexe E][appendix-e]<!-- ignore --> pour plus d'informations sur les éditions.

[appendix-e]: appendix-05-editions.html