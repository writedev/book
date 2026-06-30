## Références et Emprunt

Le problème avec le code de tuple dans la liste 4-5 est que nous devons renvoyer le `String` à la fonction appelante afin que nous puissions toujours utiliser le `String` après l'appel à `calculate_length`, car le `String` a été déplacé dans `calculate_length`. Au lieu de cela, nous pouvons fournir une référence à la valeur `String`. Une référence est comme un pointeur en ce sens qu'elle représente une adresse que nous pouvons suivre pour accéder aux données stockées à cette adresse ; ces données appartiennent à une autre variable. Contrairement à un pointeur, une référence est garantie de pointer vers une valeur valide d'un type particulier pendant toute la durée de cette référence.

Voici comment vous définiriez et utiliseriez une fonction `calculate_length` qui prend une référence à un objet comme paramètre au lieu de prendre la propriété de la valeur :

<Listing file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-07-reference/src/main.rs:all}}
```

</Listing>

Tout d'abord, remarquez que tout le code du tuple dans la déclaration de variable et la valeur de retour de fonction a disparu. Deuxièmement, notez que nous passons `&s1` dans `calculate_length` et, dans sa définition, nous prenons `&String` au lieu de `String`. Ces esperluettes représentent des références et elles vous permettent de vous référer à une valeur sans en prendre possession. La figure 4-6 illustre ce concept.

<img alt="Trois tables : la table pour s contient uniquement un pointeur vers la table pour s1. La table pour s1 contient les données de la pile pour s1 et pointe vers les données de chaîne sur le tas." src="img/trpl04-06.svg" class="center" />

<span class="caption">Figure 4-6 : Un diagramme de `&String` `s` pointant vers `String` `s1`</span>

> Remarque : L'opposé de la référence utilisant `&` est le _déséquipement_, qui s'effectue avec l'opérateur de déséquipement, `*`. Nous verrons quelques utilisations de l'opérateur de déséquipement dans le chapitre 8 et discuterons des détails du déséquipement dans le chapitre 15.

Prenons un regard plus attentif à l'appel de fonction ici :

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-07-reference/src/main.rs:here}}
```

La syntaxe `&s1` nous permet de créer une référence qui _se réfère_ à la valeur de `s1` mais ne possède pas celle-ci. Étant donné que la référence ne possède pas celle-ci, la valeur à laquelle elle pointe ne sera pas supprimée lorsque la référence cessera d'être utilisée.

De même, la signature de la fonction utilise `&` pour indiquer que le type du paramètre `s` est une référence. Ajoutons quelques annotations explicatives :

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-08-reference-with-annotations/src/main.rs:here}}
```

La portée dans laquelle la variable `s` est valide est la même que celle de tout paramètre de fonction, mais la valeur à laquelle la référence pointe n'est pas supprimée lorsque `s` cesse d'être utilisée, car `s` n'a pas la propriété. Lorsque les fonctions ont des références en tant que paramètres au lieu des valeurs réelles, nous n'avons pas besoin de renvoyer les valeurs afin de rendre la propriété, car nous n'avons jamais eu la propriété.

Nous appelons l'action de créer une référence _emprunt_. Comme dans la vie réelle, si une personne possède quelque chose, vous pouvez l'emprunter. Une fois que vous avez terminé, vous devez le rendre. Vous ne le possédez pas.

Alors, que se passe-t-il si nous essayons de modifier quelque chose que nous empruntons ? Essayez le code dans la liste 4-6. Alerte spoiler : ça ne fonctionne pas !

<Listing number="4-6" file-name="src/main.rs" caption="Tentative de modification d'une valeur empruntée">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch04-understanding-ownership/listing-04-06/src/main.rs}}
```

</Listing>

Voici l'erreur :

```console
{{#include ../listings/ch04-understanding-ownership/listing-04-06/output.txt}}
```

Tout comme les variables sont immuables par défaut, les références le sont aussi. Nous ne sommes pas autorisés à modifier quelque chose auquel nous avons une référence.

### Références Mutables

Nous pouvons corriger le code de la liste 4-6 pour nous permettre de modifier une valeur empruntée avec juste quelques petites modifications qui utilisent, à la place, une _référence mutable_ :

<Listing file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-09-fixes-listing-04-06/src/main.rs}}
```

</Listing>

Tout d'abord, nous changeons `s` pour qu'il soit `mut`. Ensuite, nous créons une référence mutable avec `&mut s` où nous appelons la fonction `change` et mettons à jour la signature de la fonction pour accepter une référence mutable avec `some_string: &mut String`. Cela rend très clair que la fonction `change` va muter la valeur qu'elle emprunte.

Les références mutables ont une grande restriction : si vous avez une référence mutable à une valeur, vous ne pouvez avoir aucune autre référence à cette valeur. Ce code qui tente de créer deux références mutables à `s` échouera :

<Listing file-name="src/main.rs">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-10-multiple-mut-not-allowed/src/main.rs:here}}
```

</Listing>

Voici l'erreur :

```console
{{#include ../listings/ch04-understanding-ownership/no-listing-10-multiple-mut-not-allowed/output.txt}}
```

Cette erreur indique que ce code est invalide car nous ne pouvons pas emprunter `s` comme mutable plus d'une fois à la fois. Le premier emprunt mutable est dans `r1` et doit durer jusqu'à son utilisation dans le `println!`, mais entre la création de cette référence mutable et son utilisation, nous avons essayé de créer une autre référence mutable dans `r2` qui emprunte les mêmes données que `r1`.

La restriction empêchant plusieurs références mutables aux mêmes données en même temps permet la mutation mais de manière très contrôlée. C'est quelque chose avec lequel les nouveaux utilisateurs de Rust ont du mal, car la plupart des langages vous permettent de muter quand vous le souhaitez. Le bénéfice d'avoir cette restriction est que Rust peut prévenir les courses de données à la compilation. Une _course de données_ est similaire à une condition de course et se produit lorsque ces trois comportements se produisent :

- Deux ou plusieurs pointeurs accèdent aux mêmes données en même temps.
- Au moins un des pointeurs est utilisé pour écrire sur les données.
- Aucun mécanisme n'est utilisé pour synchroniser l'accès aux données.

Les courses de données provoquent des comportements indéfinis et peuvent être difficiles à diagnostiquer et à réparer lorsque vous essayez de les traquer à l'exécution ; Rust prévient ce problème en refusant de compiler du code avec des courses de données !

Comme toujours, nous pouvons utiliser des accolades pour créer une nouvelle portée, permettant plusieurs références mutables, juste pas _simultanées_ :

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-11-muts-in-separate-scopes/src/main.rs:here}}
```

Rust applique une règle similaire pour la combinaison des références mutables et immuables. Ce code génère une erreur :

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-12-immutable-and-mutable-not-allowed/src/main.rs:here}}
```

Voici l'erreur :

```console
{{#include ../listings/ch04-understanding-ownership/no-listing-12-immutable-and-mutable-not-allowed/output.txt}}
```

Ouf ! Nous _ne pouvons_ également pas avoir une référence mutable pendant que nous avons une référence immuable à la même valeur.

Les utilisateurs d'une référence immuable ne s'attendent pas à ce que la valeur change soudainement sans avertir ! Cependant, plusieurs références immuables sont autorisées car personne qui lit simplement les données n'a la capacité d'affecter la lecture des données par autrui.

Notez qu'une portée de référence commence à partir du moment où elle est introduite et continue jusqu'à la dernière fois que cette référence est utilisée. Par exemple, ce code va compiler car la dernière utilisation des références immuables est dans le `println!`, avant que la référence mutable soit introduite :

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-13-reference-scope-ends/src/main.rs:here}}
```

Les portées des références immuables `r1` et `r2` se terminent après le `println!` où elles sont last utilisées, ce qui est avant la création de la référence mutable `r3`. Ces portées ne se chevauchent pas, donc ce code est autorisé : le compilateur peut dire que la référence n'est plus utilisée à un moment donné avant la fin de la portée.

Bien que les erreurs d'emprunt puissent parfois être frustrantes, rappelez-vous que c'est le compilateur Rust qui signale un bug potentiel tôt (à la compilation plutôt qu'à l'exécution) et vous montre exactement où se trouve le problème. Ainsi, vous n'avez pas à chercher pourquoi vos données ne sont pas ce que vous pensiez qu'elles étaient.

### Références Danglantes

Dans les langages avec des pointeurs, il est facile de créer par erreur un _pointeur dangleant_ - un pointeur qui fait référence à un emplacement en mémoire qui a peut-être été attribué à quelqu'un d'autre - en libérant de la mémoire tout en conservant un pointeur vers cette mémoire. En Rust, en revanche, le compilateur garantit que les références ne seront jamais des références danglantes : si vous avez une référence à des données, le compilateur s'assurera que les données ne sortiront pas de la portée avant la référence vers les données.

Essayons de créer une référence danglante pour voir comment Rust les empêche avec une erreur de compilation :

<Listing file-name="src/main.rs">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-14-dangling-reference/src/main.rs}}
```

</Listing>

Voici l'erreur :

```console
{{#include ../listings/ch04-understanding-ownership/no-listing-14-dangling-reference/output.txt}}
```

Ce message d'erreur fait référence à une fonctionnalité que nous n'avons pas encore abordée : les durées de vie. Nous discuterons des durées de vie en détail dans le chapitre 10. Mais, si vous ignorez les parties concernant les durées de vie, le message contient la clé de pourquoi ce code pose problème :

```text
le type de retour de cette fonction contient une valeur empruntée, mais il n'y a aucune valeur à partir de laquelle elle puisse être empruntée
```

Examinons de plus près ce qui se passe à chaque étape de notre code `dangle` :

<Listing file-name="src/main.rs">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-15-dangling-reference-annotated/src/main.rs:here}}
```

</Listing>

Parce que `s` est créé à l'intérieur de `dangle`, lorsque le code de `dangle` est terminé, `s` sera désalloué. Mais nous avons essayé de renvoyer une référence à celle-ci. Cela signifie que cette référence pointerait vers un `String` invalide. Ce n'est pas bon ! Rust ne nous laissera pas faire cela.

La solution ici est de renvoyer le `String` directement :

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-16-no-dangle/src/main.rs:here}}
```

Cela fonctionne sans aucun problème. La propriété est transférée, et rien n'est désalloué.

### Les Règles des Références

Récapitulons ce dont nous avons discuté au sujet des références :

- À tout moment, vous pouvez avoir _soit_ une référence mutable _soit_ un nombre quelconque de références immuables.
- Les références doivent toujours être valides.

Ensuite, nous allons examiner un autre type de référence : les tranches.