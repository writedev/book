## Valider les références avec des durées de vie

Les durées de vie sont un autre type de générique que nous avons déjà utilisé. Plutôt que de garantir qu’un type possède le comportement souhaité, les durées de vie garantissent que les références sont valides aussi longtemps que nécessaire.

Un point que nous n’avons pas abordé dans la section [« Références et emprunts »][references-and-borrowing]<!-- ignore --> du chapitre 4 est que chaque référence en Rust possède une durée de vie, c’est-à-dire la portée pendant laquelle cette référence est valide. La plupart du temps, les durées de vie sont implicites et inférées, tout comme les types. Nous ne devons annoter les types que lorsque plusieurs types sont possibles. De la même manière, nous devons annoter les durées de vie lorsque celles des références peuvent être liées de différentes façons. Rust nous demande d’annoter ces relations à l’aide de paramètres génériques de durée de vie afin de garantir que les références effectivement utilisées à l’exécution seront toujours valides.

L’annotation des durées de vie est un concept que la plupart des autres langages de programmation ne possèdent même pas ; cela vous semblera donc inhabituel. Bien que nous n’abordions pas les durées de vie dans leur intégralité dans ce chapitre, nous allons examiner des syntaxes courantes que vous pourriez rencontrer afin que vous puissiez vous familiariser avec ce concept.

<!-- Old headings. Do not remove or links may break. -->

<a id="preventing-dangling-references-with-lifetimes"></a>

### Références pendantes

L’objectif principal des durées de vie est d’empêcher les références pendantes, qui, si elles étaient autorisées, amèneraient un programme à référencer des données autres que celles qu’il est censé référencer. Considérons le programme de la liste 10-16, qui comporte une portée externe et une portée interne.

<Listing number="10-16" caption="Tentative d’utilisation d’une référence dont la valeur est sortie de portée">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-16/src/main.rs}}
```

</Listing>

> Remarque : les exemples des listes 10-16, 10-17 et 10-23 déclarent des variables sans leur attribuer de valeur initiale, de sorte que le nom de la variable existe dans la portée externe. À première vue, cela peut sembler incompatible avec le fait que Rust ne possède pas de valeurs nulles. Toutefois, si nous essayons d’utiliser une variable avant de lui attribuer une valeur, nous obtiendrons une erreur à la compilation, ce qui montre que Rust n’autorise effectivement pas les valeurs nulles.

La portée externe déclare une variable nommée `r` sans valeur initiale, et la portée interne déclare une variable nommée `x` avec la valeur initiale `5`. Dans la portée interne, nous essayons de définir la valeur de `r` comme une référence vers `x`. Ensuite, la portée interne se termine, et nous essayons d’afficher la valeur de `r`. Ce code ne compilera pas, car la valeur référencée par `r` est sortie de portée avant que nous essayions de l’utiliser. Voici le message d’erreur :

```console
{{#include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-16/output.txt}}
```

Le message d’erreur indique que la variable `x` « n’a pas une durée de vie suffisante ». En effet, `x` sera hors de portée lorsque la portée interne se terminera à la ligne 7. Mais `r` reste valide dans la portée externe ; comme sa portée est plus grande, nous disons qu’elle « vit plus longtemps ». Si Rust autorisait l’exécution de ce code, `r` référencerait une zone mémoire désallouée lorsque `x` est sortie de portée, et toute opération effectuée avec `r` ne fonctionnerait pas correctement. Alors, comment Rust détermine-t-il que ce code est invalide ? Il utilise un vérificateur d’emprunts.

### Le vérificateur d’emprunts

Le compilateur Rust possède un _vérificateur d’emprunts_ qui compare les portées afin de déterminer si tous les emprunts sont valides. La liste 10-17 présente le même code que la liste 10-16, mais avec des annotations indiquant les durées de vie des variables.

<Listing number="10-17" caption="Annotations des durées de vie de `r` et `x`, nommées respectivement `'a` et `'b`">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-17/src/main.rs}}
```

</Listing>

Ici, nous avons annoté la durée de vie de `r` avec `'a` et celle de `x` avec `'b`. Comme vous pouvez le constater, le bloc interne `'b` est beaucoup plus petit que le bloc de durée de vie externe `'a`. À la compilation, Rust compare la taille des deux durées de vie et constate que `r` a une durée de vie `'a`, mais qu’elle référence une zone mémoire dont la durée de vie est `'b`. Le programme est rejeté parce que `'b` est plus courte que `'a` : la valeur référencée ne vit pas aussi longtemps que la référence.

La liste 10-18 corrige le code afin qu’il ne contienne plus de référence pendante et qu’il compile sans erreur.

<Listing number="10-18" caption="Une référence valide, car les données ont une durée de vie plus longue que la référence">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-18/src/main.rs}}
```

</Listing>

Ici, `x` a la durée de vie `'b`, qui, dans ce cas, est plus longue que `'a`. Cela signifie que `r` peut référencer `x`, car Rust sait que la référence dans `r` sera toujours valide tant que `x` le sera.

Maintenant que vous savez où se situent les durées de vie des références et comment Rust les analyse pour s’assurer que les références seront toujours valides, examinons les durées de vie génériques dans les paramètres et les valeurs de retour des fonctions.

### Durées de vie génériques dans les fonctions

Nous allons écrire une fonction qui renvoie la plus longue de deux tranches de chaîne de caractères. Cette fonction prendra deux tranches de chaîne de caractères et renverra une seule tranche de chaîne de caractères. Une fois la fonction `longest` implémentée, le code de la liste 10-19 devrait afficher `The longest string is abcd`.

<Listing number="10-19" file-name="src/main.rs" caption="Une fonction `main` qui appelle la fonction `longest` pour trouver la plus longue de deux tranches de chaîne de caractères">

```rust,ignore
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-19/src/main.rs}}
```

</Listing>

Notez que nous voulons que la fonction prenne des tranches de chaîne de caractères, qui sont des références, plutôt que des chaînes de caractères, car nous ne voulons pas que la fonction `longest` prenne possession de ses paramètres. Consultez la section [« Les tranches de chaîne de caractères comme paramètres »][string-slices-as-parameters]<!-- ignore --> du chapitre 4 pour en savoir plus sur les raisons pour lesquelles les paramètres utilisés dans la liste 10-19 sont ceux qu’il nous faut.

Si nous essayons d’implémenter la fonction `longest` comme dans la liste 10-20, le code ne compilera pas.

<Listing number="10-20" file-name="src/main.rs" caption="Une implémentation de la fonction `longest` qui renvoie la plus longue de deux tranches de chaîne de caractères, mais qui ne compile pas encore">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-20/src/main.rs:here}}
```

</Listing>

À la place, nous obtenons l’erreur suivante, qui concerne les durées de vie :

```console
{{#include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-20/output.txt}}
```

Le texte d’aide indique que le type de retour doit comporter un paramètre générique de durée de vie, car Rust ne peut pas déterminer si la référence renvoyée désigne `x` ou `y`. En fait, nous ne le savons pas non plus, car le bloc `if` du corps de cette fonction renvoie une référence vers `x` et le bloc `else` renvoie une référence vers `y` !

Lorsque nous définissons cette fonction, nous ne connaissons pas les valeurs concrètes qui lui seront transmises. Nous ne savons donc pas si le cas `if` ou le cas `else` sera exécuté. Nous ne connaissons pas non plus les durées de vie concrètes des références qui seront transmises ; nous ne pouvons donc pas examiner les portées comme nous l’avons fait dans les listes 10-17 et 10-18 pour déterminer si la référence renvoyée sera toujours valide. Le vérificateur d’emprunts ne peut pas non plus le déterminer, car il ne sait pas comment les durées de vie de `x` et de `y` sont liées à celle de la valeur de retour. Pour corriger cette erreur, nous allons ajouter des paramètres génériques de durée de vie qui définissent la relation entre les références, afin que le vérificateur d’emprunts puisse effectuer son analyse.

### Syntaxe des annotations de durée de vie

Les annotations de durée de vie ne modifient pas la durée de vie des références. Elles décrivent plutôt les relations entre les durées de vie de plusieurs références, sans les modifier. De même que les fonctions peuvent accepter n’importe quel type lorsque leur signature spécifie un paramètre de type générique, elles peuvent accepter des références ayant n’importe quelle durée de vie en spécifiant un paramètre générique de durée de vie.

La syntaxe des annotations de durée de vie est légèrement inhabituelle : les noms des paramètres de durée de vie doivent commencer par une apostrophe (`'`) et sont généralement en minuscules et très courts, comme les types génériques. La plupart des gens utilisent le nom `'a` pour la première annotation de durée de vie. Nous plaçons les annotations des paramètres de durée de vie après le `&` d’une référence, en séparant l’annotation du type de la référence par une espace.

Voici quelques exemples : une référence à un `i32` sans paramètre de durée de vie, une référence à un `i32` avec un paramètre de durée de vie nommé `'a`, et une référence mutable à un `i32` qui a également la durée de vie `'a` :

```rust,ignore
&i32        // a reference
&'a i32     // a reference with an explicit lifetime
&'a mut i32 // a mutable reference with an explicit lifetime
```

Une annotation de durée de vie isolée n’a pas beaucoup de sens, car les annotations servent à indiquer à Rust comment les paramètres génériques de durée de vie de plusieurs références sont liés entre eux. Examinons comment les annotations de durée de vie sont liées les unes aux autres dans le contexte de la fonction `longest`.

<!-- Old headings. Do not remove or links may break. -->

<a id="lifetime-annotations-in-function-signatures"></a>

### Dans les signatures de fonctions

Pour utiliser des annotations de durée de vie dans les signatures de fonctions, nous devons déclarer les paramètres génériques de durée de vie entre chevrons, entre le nom de la fonction et la liste des paramètres, comme nous l’avons fait pour les paramètres de type générique.

Nous voulons que la signature exprime la contrainte suivante : la référence renvoyée sera valide tant que les deux paramètres le seront. C’est la relation entre les durées de vie des paramètres et celle de la valeur de retour. Nous nommerons la durée de vie `'a` et l’ajouterons à chaque référence, comme indiqué dans la liste 10-21.

<Listing number="10-21" file-name="src/main.rs" caption="Définition de la fonction `longest` indiquant que toutes les références de la signature doivent avoir la même durée de vie `'a`">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-21/src/main.rs:here}}
```

</Listing>

Ce code devrait compiler et produire le résultat souhaité lorsqu’on l’utilise avec la fonction `main` de la liste 10-19.

La signature de la fonction indique désormais à Rust que, pour une certaine durée de vie `'a`, la fonction prend deux paramètres, qui sont tous deux des tranches de chaîne de caractères vivant au moins aussi longtemps que cette durée de vie `'a`. La signature indique également à Rust que la tranche de chaîne de caractères renvoyée par la fonction vivra au moins aussi longtemps que la durée de vie `'a`. En pratique, cela signifie que la durée de vie de la référence renvoyée par la fonction `longest` est égale à la plus courte des durées de vie des valeurs référencées par les arguments de la fonction. Ce sont ces relations que nous voulons que Rust utilise lors de l’analyse de ce code.

N’oubliez pas que lorsque nous spécifions les paramètres de durée de vie dans cette signature de fonction, nous ne modifions pas les durées de vie des valeurs transmises ou renvoyées. Nous indiquons plutôt que le vérificateur d’emprunts doit rejeter les valeurs qui ne respectent pas ces contraintes. Notez que la fonction `longest` n’a pas besoin de savoir exactement combien de temps `x` et `y` vivront ; elle doit seulement savoir qu’il existe une portée substituable à `'a` qui respecte cette signature.

Lorsque nous annotons les durées de vie dans les fonctions, les annotations figurent dans la signature de la fonction, et non dans son corps. Les annotations de durée de vie font partie du contrat de la fonction, tout comme les types de la signature. Le fait que les signatures de fonctions contiennent le contrat relatif aux durées de vie simplifie l’analyse effectuée par le compilateur Rust. Si une annotation est incorrecte ou si la fonction est appelée d’une manière inadéquate, les erreurs du compilateur peuvent indiquer plus précisément la partie du code et les contraintes concernées. Si, au contraire, le compilateur Rust devait inférer davantage ce que nous voulions exprimer au sujet des relations entre les durées de vie, il ne pourrait peut-être signaler qu’une utilisation de notre code, survenant plusieurs étapes après la cause du problème.

Lorsque nous transmettons des références concrètes à `longest`, la durée de vie concrète substituée à `'a` correspond à la partie de la portée de `x` qui chevauche celle de `y`. Autrement dit, la durée de vie générique `'a` prend la durée de vie concrète égale à la plus courte des durées de vie de `x` et de `y`. Comme nous avons annoté la référence renvoyée avec le même paramètre de durée de vie `'a`, cette référence sera également valide pendant la durée de vie la plus courte de `x` et de `y`.

Voyons comment les annotations de durée de vie limitent la fonction `longest` en lui transmettant des références dont les durées de vie concrètes sont différentes. La liste 10-22 présente un exemple simple.

<Listing number="10-22" file-name="src/main.rs" caption="Utilisation de la fonction `longest` avec des références à des valeurs `String` ayant des durées de vie concrètes différentes">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-22/src/main.rs:here}}
```

</Listing>

Dans cet exemple, `string1` est valide jusqu’à la fin de la portée externe, `string2` est valide jusqu’à la fin de la portée interne, et `result` référence une valeur qui est valide jusqu’à la fin de la portée interne. Exécutez ce code et vous verrez que le vérificateur d’emprunts l’accepte ; il compilera et affichera `The longest string is long string is long`.

Essayons ensuite un exemple qui montre que la durée de vie de la référence dans `result` doit être la plus courte des durées de vie des deux arguments. Nous allons déplacer la déclaration de la variable `result` en dehors de la portée interne, tout en laissant l’affectation de sa valeur à l’intérieur de la portée où se trouve `string2`. Puis, nous déplacerons le `println!` qui utilise `result` en dehors de la portée interne, après la fin de celle-ci. Le code de la liste 10-23 ne compilera pas.

<Listing number="10-23" file-name="src/main.rs" caption="Tentative d’utilisation de `result` après que `string2` est sortie de portée">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-23/src/main.rs:here}}
```

</Listing>

Lorsque nous essayons de compiler ce code, nous obtenons cette erreur :

```console
{{#include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-23/output.txt}}
```

L’erreur indique que, pour que `result` soit valide pour l’instruction `println!`, `string2` devrait être valide jusqu’à la fin de la portée externe. Rust le sait, car nous avons annoté les durées de vie des paramètres et des valeurs de retour de la fonction à l’aide du même paramètre de durée de vie `'a`.

En tant qu’humains, nous pouvons examiner ce code et constater que `string1` a une durée de vie plus longue que `string2`, et que `result` contiendra donc une référence vers `string1`. Comme `string1` n’est pas encore sortie de portée, une référence vers `string1` restera valide pour l’instruction `println!`. Toutefois, le compilateur ne peut pas voir que la référence est valide dans ce cas. Nous avons indiqué à Rust que la durée de vie de la référence renvoyée par la fonction `longest` est égale à la plus courte des durées de vie des références transmises. Le vérificateur d’emprunts interdit donc le code de la liste 10-23, car il pourrait contenir une référence invalide.

Essayez de concevoir d’autres expériences en faisant varier les valeurs et les durées de vie des références transmises à la fonction `longest`, ainsi que l’utilisation de la référence renvoyée. Avant de compiler, formulez des hypothèses sur le fait que vos expériences passeront ou non le vérificateur d’emprunts, puis vérifiez si vous aviez raison !

<!-- Old headings. Do not remove or links may break. -->

<a id="thinking-in-terms-of-lifetimes"></a>

### Relations

La façon dont vous devez spécifier les paramètres de durée de vie dépend de ce que fait votre fonction. Par exemple, si nous modifiions l’implémentation de la fonction `longest` pour qu’elle renvoie toujours le premier paramètre plutôt que la plus longue tranche de chaîne de caractères, nous n’aurions pas besoin de spécifier de durée de vie pour le paramètre `y`. Le code suivant compilera :

<Listing file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-08-only-one-reference-with-lifetime/src/main.rs:here}}
```

</Listing>

Nous avons spécifié un paramètre de durée de vie `'a` pour le paramètre `x` et le type de retour, mais pas pour le paramètre `y`, car la durée de vie de `y` n’a aucun lien avec celle de `x` ni avec celle de la valeur de retour.

Lorsqu’une fonction renvoie une référence, le paramètre de durée de vie du type de retour doit correspondre au paramètre de durée de vie de l’un des paramètres. Si la référence renvoyée ne fait _pas_ référence à l’un des paramètres, elle doit faire référence à une valeur créée dans cette fonction. Il s’agirait toutefois d’une référence pendante, car la valeur sortirait de portée à la fin de la fonction. Considérez cette tentative d’implémentation de la fonction `longest`, qui ne compilera pas :

<Listing file-name="src/main.rs">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-09-unrelated-lifetime/src/main.rs:here}}
```

</Listing>

Ici, même si nous avons spécifié un paramètre de durée de vie `'a` pour le type de retour, cette implémentation ne compilera pas, car la durée de vie de la valeur de retour n’est aucunement liée à celle des paramètres. Voici le message d’erreur obtenu :

```console
{{#include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-09-unrelated-lifetime/output.txt}}
```

Le problème est que `result` sort de portée et est nettoyée à la fin de la fonction `longest`. Nous essayons également de renvoyer une référence vers `result` depuis la fonction. Aucune spécification de paramètres de durée de vie ne peut empêcher cette référence d’être pendante, et Rust ne nous laissera pas créer une référence pendante. Dans ce cas, la meilleure solution consiste à renvoyer un type de données possédé plutôt qu’une référence, afin que la fonction appelante soit responsable de la libération de la valeur.

En fin de compte, la syntaxe des durées de vie sert à relier les durées de vie des différents paramètres et valeurs de retour des fonctions. Une fois ces durées de vie reliées, Rust dispose de suffisamment d’informations pour autoriser les opérations sûres en mémoire et interdire celles qui créeraient des pointeurs pendants ou compromettraient autrement la sécurité mémoire.

<!-- Old headings. Do not remove or links may break. -->

<a id="lifetime-annotations-in-struct-definitions"></a>

### Dans les définitions de structures

Jusqu’à présent, les structures que nous avons définies contiennent toutes des types possédés. Nous pouvons définir des structures qui contiennent des références, mais nous devons alors ajouter une annotation de durée de vie à chaque référence dans la définition de la structure. La liste 10-24 présente une structure nommée `ImportantExcerpt` qui contient une tranche de chaîne de caractères.

<Listing number="10-24" file-name="src/main.rs" caption="Une structure qui contient une référence et nécessite une annotation de durée de vie">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-24/src/main.rs}}
```

</Listing>

Cette structure possède un seul champ, `part`, qui contient une tranche de chaîne de caractères, c’est-à-dire une référence. Comme pour les types de données génériques, nous déclarons le nom du paramètre générique de durée de vie entre chevrons après le nom de la structure, afin de pouvoir utiliser ce paramètre dans le corps de la définition de la structure. Cette annotation signifie qu’une instance de `ImportantExcerpt` ne peut pas vivre plus longtemps que la référence contenue dans son champ `part`.

La fonction `main` crée ici une instance de la structure `ImportantExcerpt` qui contient une référence à la première phrase de la `String` possédée par la variable `novel`. Les données de `novel` existent avant la création de l’instance de `ImportantExcerpt`. De plus, `novel` ne sort pas de portée avant que l’instance de `ImportantExcerpt` ne sorte de portée ; la référence contenue dans l’instance de `ImportantExcerpt` est donc valide.

### Élision des durées de vie

Vous avez appris que chaque référence possède une durée de vie et que vous devez spécifier des paramètres de durée de vie pour les fonctions ou les structures qui utilisent des références. Pourtant, nous avions une fonction dans la liste 4-9, reproduite dans la liste 10-25, qui compilait sans annotations de durée de vie.

<Listing number="10-25" file-name="src/lib.rs" caption="Une fonction définie dans la liste 4-9 qui compilait sans annotations de durée de vie, même si son paramètre et son type de retour sont des références">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-25/src/main.rs:here}}
```

</Listing>

La raison pour laquelle cette fonction compile sans annotations de durée de vie est historique : dans les premières versions de Rust (avant la version 1.0), ce code n’aurait pas compilé, car chaque référence nécessitait une durée de vie explicite. À l’époque, la signature de la fonction aurait été écrite ainsi :

```rust,ignore
fn first_word<'a>(s: &'a str) -> &'a str {
```

Après avoir écrit beaucoup de code Rust, l’équipe Rust a constaté que, dans certaines situations, les programmeurs Rust répétaient sans cesse les mêmes annotations de durée de vie. Ces situations étaient prévisibles et suivaient quelques schémas déterministes. Les développeurs ont intégré ces schémas au code du compilateur afin que le vérificateur d’emprunts puisse inférer les durées de vie dans ces situations, sans annotations explicites.

Cet aspect de l’histoire de Rust est important, car d’autres schémas déterministes pourraient apparaître et être ajoutés au compilateur. À l’avenir, les annotations de durée de vie pourraient donc être encore moins nombreuses.

Les schémas intégrés à l’analyse des références de Rust sont appelés les _règles d’élision des durées de vie_. Ce ne sont pas des règles que les programmeurs doivent suivre ; il s’agit d’un ensemble de cas particuliers que le compilateur prend en compte. Si votre code correspond à ces cas, vous n’avez pas besoin d’écrire explicitement les durées de vie.

Les règles d’élision ne fournissent pas une inférence complète. Si, après leur application par Rust, une ambiguïté subsiste quant aux durées de vie des références, le compilateur ne devinera pas celles des références restantes. Au lieu de deviner, le compilateur vous indiquera une erreur que vous pourrez corriger en ajoutant des annotations de durée de vie.

Les durées de vie des paramètres de fonctions ou de méthodes sont appelées _durées de vie d’entrée_, et celles des valeurs de retour sont appelées _durées de vie de sortie_.

Le compilateur utilise trois règles pour déterminer les durées de vie des références en l’absence d’annotations explicites. La première règle s’applique aux durées de vie d’entrée, et les deuxième et troisième règles s’appliquent aux durées de vie de sortie. Si, après avoir appliqué les trois règles, le compilateur ne parvient toujours pas à déterminer les durées de vie de certaines références, il s’arrête en signalant une erreur. Ces règles s’appliquent aussi bien aux définitions de `fn` qu’aux blocs `impl`.

La première règle veut que le compilateur attribue un paramètre de durée de vie à chaque paramètre qui est une référence. Autrement dit, une fonction avec un paramètre reçoit un paramètre de durée de vie : `fn foo<'a>(x: &'a i32)` ; une fonction avec deux paramètres reçoit deux paramètres de durée de vie distincts : `fn foo<'a, 'b>(x: &'a i32, y: &'b i32)` ; et ainsi de suite.

La deuxième règle veut que, s’il existe exactement un paramètre de durée de vie d’entrée, cette durée de vie soit attribuée à tous les paramètres de durée de vie de sortie : `fn foo<'a>(x: &'a i32) -> &'a i32`.

La troisième règle veut que, s’il existe plusieurs paramètres de durée de vie d’entrée, mais que l’un d’eux est `&self` ou `&mut self` parce qu’il s’agit d’une méthode, la durée de vie de `self` soit attribuée à tous les paramètres de durée de vie de sortie. Cette troisième règle rend les méthodes beaucoup plus agréables à lire et à écrire, car elle réduit le nombre de symboles nécessaires.

Faisons comme si nous étions le compilateur. Nous allons appliquer ces règles pour déterminer les durées de vie des références dans la signature de la fonction `first_word` de la liste 10-25. La signature commence sans aucune durée de vie associée aux références :

```rust,ignore
fn first_word(s: &str) -> &str {
```

Ensuite, le compilateur applique la première règle, qui spécifie que chaque paramètre reçoit sa propre durée de vie. Nous la nommerons `'a`, comme d’habitude ; la signature devient donc :

```rust,ignore
fn first_word<'a>(s: &'a str) -> &str {
```

La deuxième règle s’applique, car il existe exactement une durée de vie d’entrée. Elle spécifie que la durée de vie de l’unique paramètre d’entrée est attribuée à la durée de vie de sortie ; la signature devient donc :

```rust,ignore
fn first_word<'a>(s: &'a str) -> &'a str {
```

Toutes les références de cette signature de fonction ont désormais une durée de vie, et le compilateur peut poursuivre son analyse sans que le programmeur ait besoin d’annoter les durées de vie dans cette signature.

Examinons un autre exemple, cette fois avec la fonction `longest`, qui n’avait pas de paramètres de durée de vie lorsque nous avons commencé à travailler dessus dans la liste 10-20 :

```rust,ignore
fn longest(x: &str, y: &str) -> &str {
```

Appliquons la première règle : chaque paramètre reçoit sa propre durée de vie. Cette fois, nous avons deux paramètres au lieu d’un, donc nous avons deux durées de vie :

```rust,ignore
fn longest<'a, 'b>(x: &'a str, y: &'b str) -> &str {
```

Vous pouvez constater que la deuxième règle ne s’applique pas, car il existe plusieurs durées de vie d’entrée. La troisième règle ne s’applique pas non plus, car `longest` est une fonction et non une méthode ; aucun des paramètres n’est donc `self`. Après avoir appliqué les trois règles, nous n’avons toujours pas déterminé la durée de vie du type de retour. C’est pourquoi nous avons obtenu une erreur en essayant de compiler le code de la liste 10-20 : le compilateur a appliqué les règles d’élision des durées de vie, mais n’a toujours pas pu déterminer toutes les durées de vie des références dans la signature.

Comme la troisième règle ne s’applique réellement qu’aux signatures de méthodes, nous allons maintenant examiner les durées de vie dans ce contexte afin de comprendre pourquoi cette règle nous évite souvent d’avoir à annoter les durées de vie dans les signatures de méthodes.

<!-- Old headings. Do not remove or links may break. -->

<a id="lifetime-annotations-in-method-definitions"></a>

### Dans les définitions de méthodes

Lorsque nous implémentons des méthodes sur une structure avec des durées de vie, nous utilisons la même syntaxe que pour les paramètres de type générique, comme le montre la liste 10-11. L’endroit où nous déclarons et utilisons les paramètres de durée de vie dépend du fait qu’ils soient liés aux champs de la structure ou aux paramètres et valeurs de retour de la méthode.

Les noms des durées de vie des champs d’une structure doivent toujours être déclarés après le mot-clé `impl`, puis utilisés après le nom de la structure, car ces durées de vie font partie du type de la structure.

Dans les signatures de méthodes à l’intérieur du bloc `impl`, les références peuvent être liées à la durée de vie des références dans les champs de la structure, ou être indépendantes. De plus, les règles d’élision des durées de vie rendent souvent les annotations de durée de vie inutiles dans les signatures de méthodes. Examinons quelques exemples utilisant la structure nommée `ImportantExcerpt`, que nous avons définie dans la liste 10-24.

Nous allons d’abord utiliser une méthode nommée `level`, dont le seul paramètre est une référence à `self` et dont la valeur de retour est un `i32`, qui n’est une référence à rien :

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-10-lifetimes-on-methods/src/main.rs:1st}}
```

La déclaration du paramètre de durée de vie après `impl` et son utilisation après le nom du type sont nécessaires, mais, grâce à la première règle d’élision, nous n’avons pas à annoter la durée de vie de la référence à `self`.

Voici un exemple auquel s’applique la troisième règle d’élision des durées de vie :

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-10-lifetimes-on-methods/src/main.rs:3rd}}
```

Il existe deux durées de vie d’entrée ; Rust applique donc la première règle d’élision des durées de vie et attribue une durée de vie propre à `&self` et à `announcement`. Ensuite, comme l’un des paramètres est `&self`, le type de retour reçoit la durée de vie de `&self`, et toutes les durées de vie ont été déterminées.

### La durée de vie statique

Une durée de vie particulière mérite d’être abordée : `'static`, qui indique que la référence concernée _peut_ vivre pendant toute la durée du programme. Tous les littéraux de chaîne de caractères ont la durée de vie `'static`, que nous pouvons annoter comme suit :

```rust
let s: &'static str = "I have a static lifetime.";
```

Le texte de cette chaîne de caractères est directement stocké dans le binaire du programme, où il est toujours disponible. Par conséquent, tous les littéraux de chaîne de caractères ont la durée de vie `'static`.

Il se peut que des messages d’erreur vous suggèrent d’utiliser la durée de vie `'static`. Mais avant de spécifier `'static` comme durée de vie d’une référence, demandez-vous si la référence que vous avez vit réellement pendant toute la durée du programme et si vous le souhaitez. La plupart du temps, un message d’erreur suggérant la durée de vie `'static` résulte d’une tentative de création d’une référence pendante ou d’une incompatibilité entre les durées de vie disponibles. Dans ces cas-là, la solution consiste à corriger ces problèmes, et non à spécifier la durée de vie `'static`.

<!-- Old headings. Do not remove or links may break. -->

<a id="generic-type-parameters-trait-bounds-and-lifetimes-together"></a>

## Paramètres de type générique, bornes de trait et durées de vie

Examinons brièvement la syntaxe permettant de spécifier des paramètres de type générique, des bornes de trait et des durées de vie dans une même fonction !

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-11-generics-traits-and-lifetimes/src/main.rs:here}}
```

Il s’agit de la fonction `longest` de la liste 10-21, qui renvoie la plus longue de deux tranches de chaîne de caractères. Elle possède maintenant un paramètre supplémentaire nommé `ann`, de type générique `T`, qui peut être remplacé par n’importe quel type implémentant le trait `Display`, comme l’indique la clause `where`. Ce paramètre supplémentaire sera affiché à l’aide de `{}`, d’où la nécessité de la borne de trait `Display`. Comme les durées de vie sont un type de générique, les déclarations du paramètre de durée de vie `'a` et du paramètre de type générique `T` figurent dans la même liste, entre chevrons après le nom de la fonction.

## Résumé

Nous avons abordé beaucoup de choses dans ce chapitre ! Maintenant que vous connaissez les paramètres de type générique, les traits et les bornes de trait, ainsi que les paramètres génériques de durée de vie, vous êtes prêt à écrire du code sans répétition qui fonctionne dans de nombreuses situations différentes. Les paramètres de type générique vous permettent d’appliquer le code à différents types. Les traits et les bornes de trait garantissent que, même si les types sont génériques, ils possèdent le comportement dont le code a besoin. Vous avez appris à utiliser les annotations de durée de vie pour vous assurer que ce code flexible ne contiendra pas de références pendantes. Et toute cette analyse se déroule à la compilation, sans affecter les performances à l’exécution !

Croyez-le ou non, les sujets abordés dans ce chapitre ont encore beaucoup à offrir : le chapitre 18 traite des objets de trait, qui constituent une autre façon d’utiliser les traits. Il existe également des situations plus complexes impliquant des annotations de durée de vie, que vous ne rencontrerez que dans des cas très avancés ; pour celles-ci, consultez la [Référence Rust][reference]. Mais dans le prochain chapitre, vous apprendrez à écrire des tests en Rust afin de vérifier que votre code fonctionne comme prévu.

[references-and-borrowing]: ch04-02-references-and-borrowing.html#references-and-borrowing
[string-slices-as-parameters]: ch04-03-slices.html#string-slices-as-parameters
[reference]: ../reference/trait-bounds.html