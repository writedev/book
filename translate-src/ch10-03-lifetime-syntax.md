## Validation des Références avec des Durées de Vie

Les durées de vie sont un autre type de générique que nous utilisons déjà. Plutôt que d'assurer qu'un type a le comportement souhaité, les durées de vie garantissent que les références sont valides aussi longtemps que nous en avons besoin.

Un détail que nous n'avons pas abordé dans la section [« Références et Emprunt »][references-and-borrowing]<!-- ignore --> du chapitre 4 est que chaque référence en Rust a une durée de vie, qui est l'étendue pendant laquelle cette référence est valide. La plupart du temps, les durées de vie sont implicites et déduites, tout comme la plupart du temps, les types sont déduits. Nous devons seulement annoter les types lorsque plusieurs types sont possibles. De manière similaire, nous devons annoter les durées de vie lorsque les durées de vie des références pourraient être liées de différentes manières. Rust exige que nous annotions les relations en utilisant des paramètres de durée de vie génériques pour garantir que les références réelles utilisées à l'exécution seront définitivement valides.

L'annotation des durées de vie n'est même pas un concept que la plupart des autres langages de programmation possèdent, donc cela va sembler inhabituel. Bien que nous ne couvrions pas les durées de vie dans leur intégralité dans ce chapitre, nous discuterons des façons courantes dont vous pourriez rencontrer la syntaxe des durées de vie afin que vous puissiez vous familiariser avec le concept.

### Références Pendantes

L'objectif principal des durées de vie est d'éviter les références pendantes, qui, si elles étaient autorisées à exister, feraient en sorte qu'un programme référence des données autres que celles qu'il est censé référencer. Considérons le programme dans la liste 10-16, qui a une portée externe et une portée interne.

<Listing number="10-16" caption="Une tentative d'utiliser une référence dont la valeur est sortie de la portée">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-16/src/main.rs}}
```

</Listing>

> Note : Les exemples dans les listes 10-16, 10-17 et 10-23 déclarent des variables sans leur donner une valeur initiale, donc le nom de la variable existe dans la portée externe. À première vue, cela pourrait sembler être en conflit avec le fait que Rust n’a pas de valeurs nulles. Cependant, si nous essayons d'utiliser une variable avant de lui donner une valeur, nous obtiendrons une erreur de compilation, ce qui montre qu'en effet Rust n'autorise pas les valeurs nulles.

La portée externe déclare une variable nommée `r` sans valeur initiale, et la portée interne déclare une variable nommée `x` avec la valeur initiale de `5`. À l'intérieur de la portée interne, nous tentons d'assigner la valeur de `r` comme référence de `x`. Ensuite, la portée interne se termine, et nous tentons d'imprimer la valeur dans `r`. Ce code ne se compilera pas, car la valeur à laquelle `r` fait référence est sortie de la portée avant que nous n'essayions de l'utiliser. Voici le message d'erreur :

```console
{{#include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-16/output.txt}}
```

Le message d'erreur indique que la variable `x` « ne vit pas assez longtemps ». La raison est que `x` sera hors de portée lorsque la portée interne se termine à la ligne 7. Mais `r` est toujours valide pour la portée externe ; puisque son étendue est plus grande, nous disons qu'il « vit plus longtemps ». Si Rust permettait à ce code de fonctionner, `r` ferait référence à une mémoire qui a été désallouée lorsque `x` est sorti de la portée, et toute opération tentée avec `r` ne fonctionnerait pas correctement. Alors, comment Rust détermine-t-il que ce code est invalide ? Il utilise un vérificateur d'emprunt.

### Le Vérificateur d'Emprunt

Le compilateur Rust a un _vérificateur d'emprunt_ qui compare les portées pour déterminer si tous les emprunts sont valides. La liste 10-17 montre le même code que la liste 10-16 mais avec des annotations montrant les durées de vie des variables.

<Listing number="10-17" caption="Annotations des durées de vie de `r` et `x`, nommées respectivement `'a` et `'b`">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-17/src/main.rs}}
```

</Listing>

Ici, nous avons annoté la durée de vie de `r` avec `'a` et la durée de vie de `x` avec `'b`. Comme vous pouvez le voir, le bloc interne `'b` est beaucoup plus petit que le bloc de durée de vie externe `'a`. À la compilation, Rust compare la taille des deux durées de vie et constate que `r` a une durée de vie de `'a` mais qu'il fait référence à une mémoire avec une durée de vie de `'b`. Le programme est rejeté car `'b` est plus court que `'a` : le sujet de la référence ne vit pas aussi longtemps que la référence.

La liste 10-18 corrige le code afin qu'il n'ait pas de référence pendante et qu'il compile sans erreurs.

<Listing number="10-18" caption="Une référence valide car les données ont une durée de vie plus longue que la référence">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-18/src/main.rs}}
```

</Listing>

Ici, `x` a la durée de vie `'b`, qui dans ce cas est plus longue que `'a`. Cela signifie que `r` peut référencer `x` car Rust sait que la référence dans `r` sera toujours valide tant que `x` est valide.

Maintenant que vous savez où se trouvent les durées de vie des références et comment Rust analyse les durées de vie pour s'assurer que les références seront toujours valides, explorons les durées de vie génériques dans les paramètres de fonction et les valeurs de retour.

### Durées de Vie Génériques dans les Fonctions

Nous allons écrire une fonction qui retourne le plus long des deux morceaux de chaîne. Cette fonction prendra deux morceaux de chaîne et retournera un seul morceau de chaîne. Après avoir implémenté la fonction `longest`, le code de la liste 10-19 devrait imprimer `La plus longue chaîne est abcd`.

<Listing number="10-19" file-name="src/main.rs" caption="Une fonction `main` qui appelle la fonction `longest` pour trouver le plus long des deux morceaux de chaîne">

```rust,ignore
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-19/src/main.rs}}
```

</Listing>

Notez que nous voulons que la fonction prenne des morceaux de chaîne, qui sont des références, plutôt que des chaînes, car nous ne voulons pas que la fonction `longest` prenne possession de ses paramètres. Consultez [« Morceaux de Chaîne comme Paramètres »][string-slices-as-parameters]<!-- ignore --> dans le chapitre 4 pour plus de discussion sur les raisons pour lesquelles les paramètres que nous utilisons dans la liste 10-19 sont ceux que nous voulons.

Si nous essayons d'implémenter la fonction `longest` comme montré dans la liste 10-20, elle ne se compilera pas.

<Listing number="10-20" file-name="src/main.rs" caption="Une implémentation de la fonction `longest` qui retourne le plus long des deux morceaux de chaîne mais qui ne compile pas encore">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-20/src/main.rs:here}}
```

</Listing>

Au lieu de cela, nous obtenons l'erreur suivante qui parle de durées de vie :

```console
{{#include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-20/output.txt}}
```

Le texte d'aide révèle que le type de retour a besoin d'un paramètre de durée de vie générique parce que Rust ne peut pas dire si la référence renvoyée fait référence à `x` ou à `y`. En fait, nous ne savons pas non plus, car le bloc `if` dans le corps de cette fonction retourne une référence à `x` et le bloc `else` retourne une référence à `y` !

Lorsque nous définissons cette fonction, nous ne connaissons pas les valeurs concrètes qui seront passées à cette fonction, donc nous ne savons pas si le cas `if` ou le cas `else` sera exécuté. Nous ne connaissons également pas les durées de vie concrètes des références qui seront passées, donc nous ne pouvons pas examiner les portées comme nous l'avons fait dans les listes 10-17 et 10-18 pour déterminer si la référence que nous retournons sera toujours valide. Le vérificateur d'emprunt ne peut pas non plus déterminer cela, car il ne sait pas comment les durées de vie de `x` et `y` se rapportent à celle de la valeur de retour. Pour corriger cette erreur, nous ajouterons des paramètres de durée de vie générique qui définissent la relation entre les références afin que le vérificateur d'emprunt puisse effectuer son analyse.

### Syntaxe des Annotations de Durée de Vie

Les annotations de durée de vie ne changent pas combien de temps vivent les références. Au lieu de cela, elles décrivent les relations entre les durées de vie de plusieurs références sans affecter les durées de vie. De la même manière que les fonctions peuvent accepter n'importe quel type lorsque la signature spécifie un paramètre de type générique, les fonctions peuvent accepter des références avec n'importe quelle durée de vie en spécifiant un paramètre de durée de vie générique.

Les annotations de durée de vie ont une syntaxe légèrement inhabituelle : les noms des paramètres de durée de vie doivent commencer par une apostrophe (`'`) et sont généralement en minuscules et très courts, comme les types génériques. La plupart des gens utilisent le nom `'a` pour la première annotation de durée de vie. Nous plaçons les annotations de paramètres de durée de vie après le `&` d'une référence, en utilisant un espace pour séparer l'annotation du type de la référence.

Voici quelques exemples : une référence à un `i32` sans paramètre de durée de vie, une référence à un `i32` qui a un paramètre de durée de vie nommé `'a`, et une référence mutable à un `i32` qui a aussi la durée de vie `'a` :

```rust,ignore
&i32        // une référence
&'a i32     // une référence avec une durée de vie explicite
&'a mut i32 // une référence mutable avec une durée de vie explicite
```

Une annotation de durée de vie à elle seule n'a pas beaucoup de signification, car les annotations sont destinées à dire à Rust comment des paramètres de durée de vie génériques de plusieurs références se rapportent les uns aux autres. Examinons comment les annotations de durée de vie se rapportent les unes aux autres dans le contexte de la fonction `longest`.

### Dans les Signatures de Fonction

Pour utiliser des annotations de durée de vie dans les signatures de fonction, nous devons déclarer les paramètres de durée de vie génériques à l'intérieur de chevrons entre le nom de la fonction et la liste des paramètres, tout comme nous l'avons fait avec les paramètres de type générique.

Nous voulons que la signature exprime la contrainte suivante : La référence retournée sera valide tant que les deux paramètres sont valides. C'est la relation entre les durées de vie des paramètres et de la valeur de retour. Nous appellerons la durée de vie `'a` et l'ajouterons à chaque référence, comme montré dans la liste 10-21.

<Listing number="10-21" file-name="src/main.rs" caption="La définition de la fonction `longest` spécifiant que toutes les références dans la signature doivent avoir la même durée de vie `'a`">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-21/src/main.rs:here}}
```

</Listing>

Ce code devrait se compiler et produire le résultat désiré lorsque nous l'utilisons avec la fonction `main` dans la liste 10-19.

La signature de la fonction indique maintenant à Rust que pour une certaine durée de vie `'a`, la fonction prend deux paramètres, dont les deux sont des morceaux de chaînes qui vivent au moins aussi longtemps que la durée de vie `'a`. La signature de la fonction indique également à Rust que le morceau de chaîne renvoyé par la fonction vivra au moins aussi longtemps que la durée de vie `'a`. En pratique, cela signifie que la durée de vie de la référence retournée par la fonction `longest` est la même que la plus petite des durées de vie des valeurs référencées par les arguments de la fonction. Ces relations sont ce que nous voulons que Rust utilise lors de l'analyse de ce code.

Rappelez-vous, lorsque nous spécifions les paramètres de durée de vie dans cette signature de fonction, nous ne changeons pas les durées de vie de valeurs passées ou retournées. Au lieu de cela, nous spécifions que le vérificateur d'emprunt doit rejeter toute valeur qui ne respecte pas ces contraintes. Notez que la fonction `longest` n'a pas besoin de savoir exactement combien de temps `x` et `y` vivront, seulement qu'une certaine portée peut être substituée pour `'a` qui satisfera cette signature.

Lors de l'annotation des durées de vie dans les fonctions, les annotations vont dans la signature de la fonction, pas dans le corps de la fonction. Les annotations de durée de vie deviennent partie du contrat de la fonction, tout comme les types dans la signature. Avoir des signatures de fonction contenant le contrat de durée de vie signifie que l'analyse effectuée par le compilateur Rust peut être plus simple. S'il y a un problème avec la façon dont une fonction est annotée ou la manière dont elle est appelée, les erreurs du compilateur peuvent pointer vers la partie de notre code et les contraintes plus précisément. Si, au lieu de cela, le compilateur Rust faisait plus d'inférences sur ce que nous avions l'intention que soient les relations des durées de vie, le compilateur pourrait seulement être capable d'indiquer une utilisation de notre code à de nombreuses étapes du problème.

Lorsque nous passons des références concrètes à `longest`, la durée de vie concrète qui est substituée pour `'a` est la partie de la portée de `x` qui se chevauche avec la portée de `y`. En d'autres termes, la durée de vie générique `'a` obtiendra la durée de vie concrète qui est égale à la plus petite des durées de vie de `x` et `y`. Parce que nous avons annoté la référence retournée avec le même paramètre de durée de vie `'a`, la référence retournée sera également valide tant que la plus petite des durées de vie de `x` et `y` est valide.

Voyons comment les annotations de durée de vie restreignent la fonction `longest` en passant des références qui ont différentes durées de vie concrètes. La liste 10-22 est un exemple simple.

<Listing number="10-22" file-name="src/main.rs" caption="Utilisation de la fonction `longest` avec des références à des valeurs `String` qui ont différentes durées de vie concrètes">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-22/src/main.rs:here}}
```

</Listing>

Dans cet exemple, `string1` est valide jusqu'à la fin de la portée externe, `string2` est valide jusqu'à la fin de la portée interne, et `result` référence quelque chose qui est valide jusqu'à la fin de la portée interne. Exécutez ce code et vous verrez que le vérificateur d'emprunt approuve ; il se compilera et imprimera `La plus longue chaîne est une longue chaîne`.

Ensuite, essayons un exemple qui montre que la durée de vie de la référence dans `result` doit être la plus petite durée de vie des deux arguments. Nous allons déplacer la déclaration de la variable `result` en dehors de la portée interne mais laisser l'assignation de la valeur à la variable `result` à l'intérieur de la portée avec `string2`. Ensuite, nous déplacerons le `println!` qui utilise `result` à l'extérieur de la portée interne, après la fin de la portée interne. Le code dans la liste 10-23 ne se compilera pas.

<Listing number="10-23" file-name="src/main.rs" caption="Tentative d'utiliser `result` après que `string2` est sorti de la portée">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-23/src/main.rs:here}}
```

</Listing>

Lorsque nous essayons de compiler ce code, nous obtenons cette erreur :

```console
{{#include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-23/output.txt}}
```

L'erreur montre que pour que `result` soit valide pour l'instruction `println!`, `string2` devrait être valide jusqu'à la fin de la portée externe. Rust sait cela parce que nous avons annoté les durées de vie des paramètres de fonction et des valeurs de retour avec le même paramètre de durée de vie `'a`.

En tant qu'êtres humains, nous pouvons regarder ce code et voir que `string1` est plus longue que `string2`, et donc `result` contiendra une référence à `string1`. Comme `string1` n'est pas sorti de la portée, une référence à `string1` sera toujours valide pour l'instruction `println!`. Cependant, le compilateur ne peut pas voir que la référence est valide dans ce cas. Nous avons dit à Rust que la durée de vie de la référence retournée par la fonction `longest` est la même que la plus petite des durées de vie des références passées en paramètre. Par conséquent, le vérificateur d'emprunt interdit le code dans la liste 10-23 en tant que suspect de référence invalide.

Essayez de concevoir d'autres expériences qui varient les valeurs et les durées de vie des références passées à la fonction `longest` et comment la référence retournée est utilisée. Formulez des hypothèses sur la réussite ou non de vos expériences face au vérificateur d'emprunt avant de compiler ; ensuite, vérifiez si vous avez raison !

### Relations

La manière dont vous devez spécifier les paramètres de durée de vie dépend de ce que fait votre fonction. Par exemple, si nous changions l'implémentation de la fonction `longest` pour toujours retourner le premier paramètre plutôt que le plus long morceau de chaîne, nous n'aurions pas besoin de spécifier une durée de vie pour le paramètre `y`. Le code suivant se compilera :

<Listing file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-08-only-one-reference-with-lifetime/src/main.rs:here}}
```

</Listing>

Nous avons spécifié un paramètre de durée de vie `'a` pour le paramètre `x` et le type de retour, mais pas pour le paramètre `y`, car la durée de vie de `y` n'a aucune relation avec la durée de vie de `x` ou la valeur de retour.

Lors de la restitution d'une référence d'une fonction, le paramètre de durée de vie pour le type de retour doit correspondre au paramètre de durée de vie de l'un des paramètres. Si la référence retournée _ne_ fait _pas_ référence à l'un des paramètres, elle doit faire référence à une valeur créée dans cette fonction. Cependant, ce serait une référence pendante car la valeur sortira de la portée à la fin de la fonction. Considérons cette tentative d'implémentation de la fonction `longest` qui ne se compilera pas :

<Listing file-name="src/main.rs">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-09-unrelated-lifetime/src/main.rs:here}}
```

</Listing>

Ici, même si nous avons spécifié un paramètre de durée de vie `'a` pour le type de retour, cette implémentation échouera à se compiler car la durée de vie de la valeur de retour n'est pas liée à la durée de vie des paramètres. Voici le message d'erreur que nous obtenons :

```console
{{#include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-09-unrelated-lifetime/output.txt}}
```

Le problème est que `result` sort de la portée et est nettoyé à la fin de la fonction `longest`. Nous essayons également de retourner une référence à `result` de la fonction. Il n'y a aucun moyen de spécifier des paramètres de durée de vie qui changeraient la référence pendante, et Rust ne nous laissera pas créer une référence pendante. Dans ce cas, la meilleure solution serait de retourner un type de données possédé plutôt qu'une référence afin que la fonction appelante soit alors responsable de nettoyer la valeur.

En fin de compte, la syntaxe des durées de vie est une question de connexion des durées de vie des différents paramètres et valeurs de retour des fonctions. Une fois qu'elles sont connectées, Rust dispose de suffisamment d'informations pour permettre des opérations sûres en mémoire et interdire les opérations qui pourraient créer des pointeurs pendants ou autrement violer la sécurité mémoire.

### Dans les Définitions de Struct

Jusqu'à présent, les structures que nous avons définies contiennent toutes des types possédés. Nous pouvons définir des structures pour contenir des références, mais dans ce cas, nous devrions ajouter une annotation de durée de vie sur chaque référence dans la définition de la structure. La liste 10-24 présente une structure nommée `ImportantExcerpt` qui contient un morceau de chaîne.

<Listing number="10-24" file-name="src/main.rs" caption="Une struct qui contient une référence, requérant une annotation de durée de vie">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-24/src/main.rs}}
```

</Listing>

Cette structure a le champ unique `part` qui contient un morceau de chaîne, qui est une référence. Comme avec les types de données génériques, nous déclarons le nom du paramètre de durée de vie générique à l'intérieur de chevrons après le nom de la structure afin que nous puissions utiliser le paramètre de durée de vie dans le corps de la définition de la structure. Cette annotation signifie qu'une instance de `ImportantExcerpt` ne peut pas vivre au-delà de la référence qu'elle contient dans son champ `part`.

La fonction `main` ici crée une instance de la structure `ImportantExcerpt` qui détient une référence à la première phrase de la `String` possédée par la variable `novel`. Les données dans `novel` existent avant que l'instance de `ImportantExcerpt` ne soit créée. De plus, `novel` ne sortira pas de la portée avant que l'instance `ImportantExcerpt` ne soit hors de portée, donc la référence dans l'instance de `ImportantExcerpt` est valide.

### Élision de Durée de Vie

Vous avez appris que chaque référence a une durée de vie et que vous devez spécifier des paramètres de durée de vie pour les fonctions ou structures qui utilisent des références. Cependant, nous avions une fonction dans la liste 4-9, montrée à nouveau dans la liste 10-25, qui s'est compilée sans annotations de durée de vie.

<Listing number="10-25" file-name="src/lib.rs" caption="Une fonction que nous avons définie dans la liste 4-9 qui se compile sans annotations de durée de vie, même si le paramètre et le type de retour sont des références">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-25/src/main.rs:here}}
```

</Listing>

La raison pour laquelle cette fonction se compile sans annotations de durée de vie est historique : dans les versions anciennes (avant 1.0) de Rust, ce code n’aurait pas compilé, car chaque référence avait besoin d'une durée de vie explicite. À ce moment-là, la signature de la fonction aurait été écrite de cette manière :

```rust,ignore
fn first_word<'a>(s: &'a str) -> &'a str {
```

Après avoir écrit beaucoup de code Rust, l'équipe Rust a constaté que les programmeurs Rust saisissaient les mêmes annotations de durée de vie encore et encore dans des situations particulières. Ces situations étaient prévisibles et suivaient quelques modèles déterministes. Les développeurs ont programmé ces modèles dans le code du compilateur afin que le vérificateur d'emprunt puisse inférer les durées de vie dans ces situations et ne nécessiterait pas d'annotations explicites.

Ce morceau d'histoire de Rust est pertinent car il est possible que des modèles plus déterministes émergent et soient ajoutés au compilateur. À l'avenir, encore moins d'annotations de durée de vie pourraient être nécessaires.

Les modèles programmés dans l'analyse de Rust des références sont appelés les _règles d'élision de durée de vie_. Ce ne sont pas des règles que les programmeurs doivent suivre ; ce sont un ensemble de cas particuliers que le compilateur considérera, et si votre code correspond à ces cas, vous n'avez pas besoin d'écrire explicitement les durées de vie.

Les durées de vie sur les paramètres de fonction ou de méthode sont appelées _durées de vie d'entrée_, et les durées de vie sur les valeurs de retour sont appelées _durées de vie de sortie_.

Le compilateur utilise trois règles pour déterminer les durées de vie des références lorsqu'il n'y a pas d'annotations explicites. La première règle s'applique aux durées de vie d'entrée, et les deuxième et troisième règles s'appliquent aux durées de vie de sortie. Si le compilateur arrive à la fin des trois règles et qu'il y a encore des références pour lesquelles il ne peut pas déterminer les durées de vie, le compilateur arrêtera avec une erreur. Ces règles s'appliquent aux définitions de `fn` ainsi qu'aux blocs `impl`.

La première règle stipule que le compilateur assigne un paramètre de durée de vie à chaque paramètre qui est une référence. En d'autres termes, une fonction avec un paramètre obtient un paramètre de durée de vie : `fn foo<'a>(x: &'a i32)` ; une fonction avec deux paramètres obtient deux paramètres de durée de vie séparés : `fn foo<'a, 'b>(x: &'a i32, y: &'b i32)` ; et ainsi de suite.

La deuxième règle est que, s'il y a exactement un paramètre de durée de vie d'entrée, cette durée de vie est assignée à tous les paramètres de durée de vie de sortie : `fn foo<'a>(x: &'a i32) -> &'a i32`.

La troisième règle est que, s'il y a plusieurs paramètres de durée de vie d'entrée, mais qu'un d'eux est `&self` ou `&mut self` parce que c'est une méthode, la durée de vie de `self` est assignée à tous les paramètres de durée de vie de sortie. Cette troisième règle rend les méthodes beaucoup plus agréables à lire et à écrire, car moins de symboles sont nécessaires.

Faisons comme si nous étions le compilateur. Nous allons appliquer ces règles pour déterminer les durées de vie des références dans la signature de la fonction `first_word` dans la liste 10-25. La signature commence sans aucune durée de vie associée aux références :

```rust,ignore
fn first_word(s: &str) -> &str {
```

Ensuite, le compilateur applique la première règle, qui spécifie que chaque paramètre obtient sa propre durée de vie. Nous l'appellerons `'a`, comme d'habitude, donc maintenant la signature est la suivante :

```rust,ignore
fn first_word<'a>(s: &'a str) -> &str {
```

La deuxième règle s'applique car il y a exactement un paramètre de durée de vie d'entrée. La deuxième règle spécifie que la durée de vie du seul paramètre d'entrée est assignée à la durée de vie de sortie, donc la signature est maintenant cette :

```rust,ignore
fn first_word<'a>(s: &'a str) -> &'a str {
```

Maintenant, toutes les références dans cette signature de fonction ont des durées de vie, et le compilateur peut continuer son analyse sans avoir besoin que le programmeur annoté les durées de vie dans cette signature.

Examinons un autre exemple, cette fois en utilisant la fonction `longest` qui n'avait pas de paramètres de durée de vie lorsque nous avons commencé à travailler avec elle dans la liste 10-20 :

```rust,ignore
fn longest(x: &str, y: &str) -> &str {
```

Appliquons la première règle : Chaque paramètre obtient sa propre durée de vie. Cette fois, nous avons deux paramètres au lieu d'un, donc nous avons deux durées de vie :

```rust,ignore
fn longest<'a, 'b>(x: &'a str, y: &'b str) -> &str {
```

Vous pouvez voir que la deuxième règle ne s'applique pas, car il y a plus d'une durée de vie d'entrée. La troisième règle ne s'applique pas non plus, car `longest` est une fonction plutôt qu'une méthode, donc aucun des paramètres n'est `self`. Après avoir travaillé à travers les trois règles, nous n'avons toujours pas déterminé la durée de vie du type de retour. C'est pourquoi nous avons eu une erreur en essayant de compiler le code dans la liste 10-20 : Le compilateur a appliqué les règles d'élision de durée de vie mais n'a pas pu déterminer toutes les durées de vie des références dans la signature.

Puisque la troisième règle ne s'applique vraiment qu'aux signatures de méthode, examinons les durées de vie dans ce contexte ensuite pour voir pourquoi la troisième règle signifie que nous n'avons pas besoin d'annoter souvent les durées de vie dans les signatures de méthode.

### Dans les Définitions de Méthode

Lorsque nous implémentons des méthodes sur une structure avec des durées de vie, nous utilisons la même syntaxe que celle des paramètres de type génériques, comme montré dans la liste 10-11. Où nous déclarons et utilisons les paramètres de durée de vie dépend de ce qu'ils ont rapport avec les champs de la structure ou les paramètres et les valeurs de retour de la méthode.

Les noms des durées de vie pour les champs de structure doivent toujours être déclarés après le mot clé `impl` et ensuite utilisés après le nom de la structure, car ces durées de vie font partie du type de la structure.

Dans les signatures de méthodes à l'intérieur du bloc `impl`, les références pourraient être liées à la durée de vie des références dans les champs de la structure, ou elles pourraient être indépendantes. De plus, les règles d'élision de durée de vie rendent souvent les annotations de durée de vie inutiles dans les signatures de méthode. Examinons quelques exemples utilisant la structure nommée `ImportantExcerpt` que nous avons définie dans la liste 10-24.

D'abord, nous utiliserons une méthode nommée `level` dont le seul paramètre est une référence à `self` et dont la valeur de retour est un `i32`, qui n'est pas une référence à quoi que ce soit :

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-10-lifetimes-on-methods/src/main.rs:1st}}
```

La déclaration de paramètre de durée de vie après `impl` et son utilisation après le nom de type sont requises, mais grâce à la première règle d'élision, nous ne sommes pas obligés d'annoter la durée de vie de la référence à `self`.

Voici un exemple où la troisième règle d'élision de durée de vie s'applique :

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-10-lifetimes-on-methods/src/main.rs:3rd}}
```

Il y a deux durées de vie d'entrée, donc Rust applique la première règle d'élision de durée de vie et donne à `&self` et `announcement` leurs propres durées de vie. Ensuite, parce qu’un des paramètres est `&self`, la valeur de retour obtient la durée de vie de `&self`, et toutes les durées de vie ont été prises en compte.

### La Durée de Vie Static

Une durée de vie spéciale dont nous devons discuter est `'static`, qui indique que la référence concernée _peut_ vivre pendant toute la durée du programme. Toutes les chaînes littérales ont la durée de vie `'static`, que nous pouvons annoter comme suit :

```rust
let s: &'static str = "J'ai une durée de vie statique.";
```

Le texte de cette chaîne est stocké directement dans le binaire du programme, qui est toujours disponible. Par conséquent, la durée de vie de toutes les chaînes littérales est `'static`.

Vous pourriez voir des suggestions dans les messages d'erreur pour utiliser la durée de vie `'static`. Mais avant de spécifier `'static` comme durée de vie pour une référence, pensez à savoir si la référence que vous avez vit réellement pendant toute la durée de votre programme, et si vous le souhaitez. La plupart du temps, un message d'erreur suggérant la durée de vie `'static` résulte de la tentative de créer une référence pendante ou d'un décalage entre les durées de vie disponibles. Dans de tels cas, la solution consiste à résoudre ces problèmes, et non à spécifier la durée de vie `'static`.

## Paramètres de Type Génériques, Limites de Trait, et Durées de Vie Ensemble

Jetons un coup d'œil rapide à la syntaxe pour spécifier ensemble des paramètres de type génériques, des limites de trait et des durées de vie dans une fonction !

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-11-generics-traits-and-lifetimes/src/main.rs:here}}
```

C'est la fonction `longest` de la liste 10-21 qui retourne le plus long des deux morceaux de chaîne. Mais maintenant elle a un paramètre supplémentaire nommé `ann` du type générique `T`, qui peut être rempli par n'importe quel type qui implémente le trait `Display`, tel que spécifié par la clause `where`. Ce paramètre supplémentaire sera imprimé en utilisant `{}`, c'est pourquoi la limite de trait `Display` est nécessaire. Comme les durées de vie sont un type de générique, les déclarations du paramètre de durée de vie `'a` et du paramètre de type générique `T` vont dans la même liste à l'intérieur des chevrons après le nom de la fonction.

## Conclusion

Nous avons couvert beaucoup de choses dans ce chapitre ! Maintenant que vous en savez plus sur les paramètres de type génériques, les traits et les limites de traits, ainsi que les paramètres de durée de vie génériques, vous êtes prêt à écrire du code sans répétition qui fonctionne dans de nombreuses situations différentes. Les paramètres de type génériques vous permettent d'appliquer le code à différents types. Les traits et les limites de traits garantissent que même si les types sont génériques, ils auront le comportement dont le code a besoin. Vous avez appris à utiliser des annotations de durée de vie pour vous assurer que ce code flexible n'aura pas de références pendantes. Et toute cette analyse se fait à la compilation, ce qui n'affecte pas la performance à l'exécution !

Croyez-le ou non, il y a beaucoup plus à apprendre sur les sujets que nous avons discutés dans ce chapitre : Le chapitre 18 aborde les objets de trait, qui sont une autre façon d'utiliser les traits. Il y a aussi des scénarios plus complexes impliquant des annotations de durée de vie que vous ne rencontrerez que dans des scénarios très avancés ; pour cela, vous devriez lire la [Référence Rust][reference]. Mais ensuite, vous apprendrez à écrire des tests en Rust afin de vous assurer que votre code fonctionne comme il se doit.

[references-and-borrowing]: ch04-02-references-and-borrowing.html#references-and-borrowing
[string-slices-as-parameters]: ch04-03-slices.html#string-slices-as-parameters
[reference]: ../reference/trait-bounds.html