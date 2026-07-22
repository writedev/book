<!-- Ancien en-têtes. Ne pas supprimer ou les liens peuvent se briser. -->

<a id="yielding"></a>

### Céder le contrôle au Runtime

Rappelons-nous de la section [« Notre premier programme asynchrone »][async-program]<!-- ignore --> que, à chaque point d'attente, Rust donne une chance au runtime de mettre en pause la tâche et de passer à une autre si le futur attendu n'est pas prêt. L'inverse est également vrai : Rust _met uniquement_ en pause les blocs asynchrones et rend le contrôle à un runtime à un point d'attente. Tout ce qui se trouve entre les points d'attente est synchrone.

Cela signifie que si vous effectuez beaucoup de travail dans un bloc asynchrone sans un point d'attente, ce futur bloquera tout autre futur de faire des progrès. Vous entendrez parfois cela désigné comme un futur _affamant_ les autres futurs. Dans certains cas, cela peut ne pas poser de problème. Toutefois, si vous effectuez une sorte de configuration coûteuse ou un travail de longue durée, ou si vous avez un futur qui continuera à réaliser une tâche particulière indéfiniment, vous devrez réfléchir à quand et où céder le contrôle au runtime.

Simulons une opération de longue durée pour illustrer le problème de la famine, puis explorons comment le résoudre. La liste 17-14 introduit une fonction `slow`.

<Listing number="17-14" caption="Utilisation de `thread::sleep` pour simuler des opérations lentes" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-14/src/main.rs:slow}}
```

</Listing>

Ce code utilise `std::thread::sleep` au lieu de `trpl::sleep`, de sorte que l'appel à `slow` bloquera le fil actuel pendant un certain nombre de millisecondes. Nous pouvons utiliser `slow` pour représenter des opérations réelles qui sont à la fois longues et bloquantes.

Dans la liste 17-15, nous utilisons `slow` pour émuler ce type de travail lié au CPU dans une paire de futurs.

<Listing number="17-15" caption="Appel de la fonction `slow` pour simuler des opérations lentes" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-15/src/main.rs:slow-futures}}
```

</Listing>

Chaque futur rend le contrôle au runtime _uniquement_ après avoir effectué une série d'opérations lentes. Si vous exécutez ce code, vous verrez cette sortie :

```text
'a' a commencé.
'a' a tourné pendant 30ms
'a' a tourné pendant 10ms
'a' a tourné pendant 20ms
'b' a commencé.
'b' a tourné pendant 75ms
'b' a tourné pendant 10ms
'b' a tourné pendant 15ms
'b' a tourné pendant 350ms
'a' a terminé.
```

Tout comme dans la liste 17-5 où nous avons utilisé `trpl::select` pour faire concourir des futurs récupérant deux URL, `select` se termine toujours dès que `a` est fait. Il n'y a pas d'interleaving entre les appels à `slow` dans les deux futurs, cependant. Le futur `a` effectue tout son travail jusqu'à ce que l'appel à `trpl::sleep` soit attendu, puis le futur `b` effectue tout son travail jusqu'à ce que son propre appel à `trpl::sleep` soit attendu, et enfin le futur `a` se termine. Pour permettre aux deux futurs de progresser entre leurs tâches lentes, nous avons besoin de points d'attente afin de pouvoir rendre le contrôle au runtime. Cela signifie que nous avons besoin de quelque chose que nous pouvons attendre !

Nous pouvons déjà voir ce type de passation se produisant dans la liste 17-15 : si nous supprimions le `trpl::sleep` à la fin du futur `a`, il se terminerait sans que le futur `b` ne s'exécute _du tout_. Essayons d'utiliser la fonction `trpl::sleep` comme point de départ pour permettre aux opérations de passer le relais dans le progrès, comme indiqué dans la liste 17-16.

<Listing number="17-16" caption="Utilisation de `trpl::sleep` pour laisser les opérations passer le relais dans le progrès" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-16/src/main.rs:here}}
```

</Listing>

Nous avons ajouté des appels `trpl::sleep` avec des points d'attente entre chaque appel à `slow`. Maintenant, le travail des deux futurs est entrelacé :

```text
'a' a commencé.
'a' a tourné pendant 30ms
'b' a commencé.
'b' a tourné pendant 75ms
'a' a tourné pendant 10ms
'b' a tourné pendant 10ms
'a' a tourné pendant 20ms
'b' a tourné pendant 15ms
'a' a terminé.
```

Le futur `a` s'exécute toujours un peu avant de passer le relais à `b`, car il appelle `slow` avant d'appeler `trpl::sleep`, mais après cela, les futurs échangent le relais chaque fois que l'un d'eux atteint un point d'attente. Dans ce cas, nous l'avons fait après chaque appel à `slow`, mais nous pourrions fragmenter le travail de la manière qui a le plus de sens pour nous.

Cependant, nous ne voulons pas vraiment _dormir_ ici ; nous voulons progresser aussi rapidement que possible. Nous devons simplement rendre le contrôle au runtime. Nous pouvons le faire directement, en utilisant la fonction `trpl::yield_now`. Dans la liste 17-17, nous remplaçons tous ces appels à `trpl::sleep` par `trpl::yield_now`.

<Listing number="17-17" caption="Utilisation de `yield_now` pour laisser les opérations passer le relais dans le progrès" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-17/src/main.rs:yields}}
```

</Listing>

Ce code est à la fois plus clair sur l'intention réelle et peut être significativement plus rapide que l'utilisation de `sleep`, car les minuteries comme celle utilisée par `sleep` ont souvent des limites sur leur granularité. La version de `sleep` que nous utilisons, par exemple, dormira toujours pendant au moins une milliseconde, même si nous lui passons une `Duration` d'une nanosecond. Encore une fois, les ordinateurs modernes sont _rapides_ : ils peuvent faire beaucoup en une milliseconde !

Cela signifie que l'asynchrone peut être utile même pour des tâches liées au calcul, selon ce que fait votre programme, car il fournit un outil utile pour structurer les relations entre les différentes parties du programme (mais au prix de la surcharge de la machine d'état asynchrone). C'est une forme de _multitâche coopératif_, où chaque futur a le pouvoir de déterminer quand il passe le contrôle via des points d'attente. Chaque futur a donc également la responsabilité d'éviter de bloquer trop longtemps. Dans certains systèmes d'exploitation embarqués basés sur Rust, c'est le _seul_ type de multitâche !

Dans le code réel, vous ne ferez généralement pas alterner les appels de fonction avec des points d'attente à chaque ligne, bien sûr. Bien que céder le contrôle de cette manière soit relativement peu coûteux, ce n'est pas gratuit. Dans de nombreux cas, essayer de fragmenter une tâche liée au calcul pourrait la rendre significativement plus lente, donc parfois il est préférable pour la performance _globale_ de laisser une opération bloquer brièvement. Mesurez toujours pour voir quels sont les véritables goulets d'étranglement de performance de votre code. La dynamique sous-jacente est importante à garder à l'esprit, cependant, si vous _voyez_ beaucoup de travail se produire en série que vous vous attendiez à voir se produire en parallèle !

### Construire nos propres abstractions asynchrones

Nous pouvons également composer des futurs ensemble pour créer de nouveaux motifs. Par exemple, nous pouvons construire une fonction `timeout` avec des blocs de construction asynchrones que nous avons déjà. Une fois que nous avons terminé, le résultat sera un autre bloc de construction que nous pourrions utiliser pour créer encore plus d'abstractions asynchrones.

La liste 17-18 montre comment nous nous attendrions à ce que ce `timeout` fonctionne avec un futur lent.

<Listing number="17-18" caption="Utilisation de notre imaginé `timeout` pour exécuter une opération lente avec une limite de temps" file-name="src/main.rs">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch17-async-await/listing-17-18/src/main.rs:here}}
```

</Listing>

Mettons cela en œuvre ! Pour commencer, réfléchissons à l'API de `timeout` :

- Il doit s'agir d'une fonction asynchrone elle-même afin que nous puissions l'attendre.
- Son premier paramètre doit être un futur à exécuter. Nous pouvons le rendre générique pour permettre qu'il fonctionne avec n'importe quel futur.
- Son deuxième paramètre sera le temps maximum à attendre. Si nous utilisons une `Duration`, cela facilitera le passage à `trpl::sleep`.
- Il doit renvoyer un `Result`. Si le futur se termine avec succès, le `Result` sera `Ok` avec la valeur produite par le futur. Si le timeout expire d'abord, le `Result` sera `Err` avec la durée que le timeout a attendue.

La liste 17-19 montre cette déclaration.

<!-- Cela n'est pas testé car il ne compile intentionnellement pas. -->

<Listing number="17-19" caption="Définir la signature de `timeout`" file-name="src/main.rs">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch17-async-await/listing-17-19/src/main.rs:declaration}}
```

</Listing>

Cela satisfait nos objectifs pour les types. Maintenant, réfléchissons au _comportement_ dont nous avons besoin : nous voulons faire concourir le futur passé avec la durée. Nous pouvons utiliser `trpl::sleep` pour créer un futur timer à partir de la durée et utiliser `trpl::select` pour exécuter ce timer avec le futur que l'appelant passe.

Dans la liste 17-20, nous implémentons `timeout` en faisant correspondre le résultat de l'attente de `trpl::select`.

<Listing number="17-20" caption="Définir `timeout` avec `select` et `sleep`" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-20/src/main.rs:implementation}}
```

</Listing>

L'implémentation de `trpl::select` n'est pas équitable : elle poll l'argument dans l'ordre dans lequel ils sont passés (d'autres implémentations de `select` choisiront aléatoirement quel argument poll first). Ainsi, nous passons `future_to_try` à `select` en premier afin qu'il ait une chance de se terminer même si `max_time` est une durée très courte. Si `future_to_try` se termine en premier, `select` renverra `Left` avec la sortie de `future_to_try`. Si `timer` se termine en premier, `select` renverra `Right` avec la sortie du timer de `()`.

Si `future_to_try` réussit et que nous obtenons un `Left(output)`, nous renvoyons `Ok(output)`. Si le timer de sommeil expire à la place et que nous obtenons un `Right(())`, nous ignorons le `()` avec `_` et renvoyons `Err(max_time)` à la place.

Avec cela, nous avons un `timeout` fonctionnel construit à partir de deux autres helpers asynchrones. Si nous exécutons notre code, il affichera le mode d'échec après le timeout :

```text
Échec après 2 secondes
```

Parce que les futurs se composent avec d'autres futurs, vous pouvez créer des outils vraiment puissants en utilisant de petits blocs de construction asynchrones. Par exemple, vous pouvez utiliser cette même approche pour combiner des timeouts avec des réessais, et à leur tour les utiliser avec des opérations telles que des appels réseau (comme ceux de la liste 17-5).

En pratique, vous travaillerez généralement directement avec `async` et `await`, et secondairement avec des fonctions telles que `select` et des macros comme la macro `join!` pour contrôler la manière dont les futurs externes sont exécutés.

Nous avons maintenant vu plusieurs façons de travailler avec plusieurs futurs en même temps. Ensuite, nous verrons comment nous pouvons travailler avec plusieurs futurs en séquence dans le temps avec des _flux_.

[async-program]: ch17-01-futures-and-syntax.html#our-first-async-program