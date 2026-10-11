<!-- Old headings. Do not remove or links may break. -->

<a id="yielding"></a>

### Céder le contrôle à l’environnement d’exécution

Rappelez-vous la section [« Notre premier programme asynchrone »][async-program]<!-- ignore --> : à chaque point d’attente, Rust donne à un environnement d’exécution la possibilité de mettre la tâche en pause et de passer à une autre si la future attendue n’est pas prête. L’inverse est également vrai : Rust ne met en pause les blocs asynchrones et ne rend le contrôle à un environnement d’exécution qu’à un point d’attente. Tout ce qui se passe entre deux points d’attente est synchrone.

Cela signifie que si vous effectuez beaucoup de travail dans un bloc asynchrone sans point d’attente, cette future empêchera toute autre future de progresser. Vous entendrez parfois dire qu’une future en _affame_ d’autres. Dans certains cas, cela n’a pas beaucoup d’importance. Toutefois, si vous effectuez une préparation coûteuse, un travail de longue durée ou si vous avez une future qui continuera indéfiniment à effectuer une tâche donnée, vous devrez réfléchir au moment et à l’endroit où rendre le contrôle à l’environnement d’exécution.

Simulons une opération de longue durée pour illustrer le problème d’affamement, puis voyons comment le résoudre. La liste 17-14 présente une fonction `slow`.

<Listing number="17-14" caption="Utiliser `thread::sleep` pour simuler des opérations lentes" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-14/src/main.rs:slow}}
```

</Listing>

Ce code utilise `std::thread::sleep` plutôt que `trpl::sleep`, de sorte qu’un appel à `slow` bloquera le thread courant pendant un certain nombre de millisecondes. Nous pouvons utiliser `slow` pour représenter des opérations du monde réel à la fois longues et bloquantes.

Dans la liste 17-15, nous utilisons `slow` pour simuler ce type de travail limité par le processeur dans une paire de futures.

<Listing number="17-15" caption="Appeler la fonction `slow` pour simuler des opérations lentes" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-15/src/main.rs:slow-futures}}
```

</Listing>

Chaque future ne rend le contrôle à l’environnement d’exécution qu’_après_ avoir effectué une série d’opérations lentes. Si vous exécutez ce code, vous verrez cette sortie :

<!-- manual-regeneration
cd listings/ch17-async-await/listing-17-15/
cargo run
copy just the output
-->

```text
'a' started.
'a' ran for 30ms
'a' ran for 10ms
'a' ran for 20ms
'b' started.
'b' ran for 75ms
'b' ran for 10ms
'b' ran for 15ms
'b' ran for 350ms
'a' finished.
```

Comme dans la liste 17-5, où nous avons utilisé `trpl::select` pour mettre en concurrence des futures récupérant deux URL, `select` se termine toujours dès que `a` est terminée. Toutefois, les appels à `slow` des deux futures ne sont pas entrelacés. La future `a` effectue tout son travail jusqu’à ce que l’appel à `trpl::sleep` soit attendu ; la future `b` effectue ensuite tout son travail jusqu’à ce que son propre appel à `trpl::sleep` soit attendu ; et enfin, la future `a` se termine. Pour permettre aux deux futures de progresser entre leurs tâches lentes, nous avons besoin de points d’attente afin de pouvoir rendre le contrôle à l’environnement d’exécution. Il nous faut donc quelque chose que nous puissions attendre !

Nous pouvons déjà observer ce type de transfert dans la liste 17-15 : si nous supprimions l’appel à `trpl::sleep` à la fin de la future `a`, elle se terminerait sans que la future `b` ne s’exécute _du tout_. Essayons d’utiliser la fonction `trpl::sleep` comme point de départ pour permettre aux opérations de se relayer, comme le montre la liste 17-16.

<Listing number="17-16" caption="Utiliser `trpl::sleep` pour permettre aux opérations de se relayer" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-16/src/main.rs:here}}
```

</Listing>

Nous avons ajouté des appels à `trpl::sleep`, avec des points d’attente entre chaque appel à `slow`. Le travail des deux futures est maintenant entrelacé :

<!-- manual-regeneration
cd listings/ch17-async-await/listing-17-16
cargo run
copy just the output
-->

```text
'a' started.
'a' ran for 30ms
'b' started.
'b' ran for 75ms
'a' ran for 10ms
'b' ran for 10ms
'a' ran for 20ms
'b' ran for 15ms
'a' finished.
```

La future `a` s’exécute encore un moment avant de céder le contrôle à `b`, car elle appelle `slow` avant même d’appeler `trpl::sleep`. Ensuite, les futures alternent à chaque fois que l’une d’elles atteint un point d’attente. Ici, nous avons procédé ainsi après chaque appel à `slow`, mais nous pouvons diviser le travail de la façon qui nous semble la plus judicieuse.

Nous ne voulons toutefois pas vraiment _dormir_ ici : nous voulons progresser aussi vite que possible. Il nous suffit de rendre le contrôle à l’environnement d’exécution. Nous pouvons le faire directement avec la fonction `trpl::yield_now`. Dans la liste 17-17, nous remplaçons tous ces appels à `trpl::sleep` par `trpl::yield_now`.

<Listing number="17-17" caption="Utiliser `yield_now` pour permettre aux opérations de se relayer" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-17/src/main.rs:yields}}
```

</Listing>

Ce code exprime plus clairement l’intention réelle et peut être nettement plus rapide que l’utilisation de `sleep`, car les temporisateurs tels que celui utilisé par `sleep` ont souvent une granularité limitée. La version de `sleep` que nous utilisons, par exemple, attendra toujours au moins une milliseconde, même si nous lui transmettons une `Duration` d’une nanoseconde. Une fois encore, les ordinateurs modernes sont _rapides_ : ils peuvent accomplir beaucoup de choses en une milliseconde !

Cela signifie que l’asynchrone peut être utile même pour des tâches limitées par le processeur, selon ce que fait le reste de votre programme, car il fournit un outil pratique pour structurer les relations entre les différentes parties du programme (au prix, toutefois, du surcoût de la machine à états asynchrone). Il s’agit d’une forme de _multitâche coopératif_, dans laquelle chaque future peut déterminer quand elle cède le contrôle au moyen de points d’attente. Chaque future a donc également la responsabilité d’éviter de bloquer trop longtemps. Dans certains systèmes d’exploitation embarqués basés sur Rust, c’est le _seul_ type de multitâche !

Dans du code réel, vous n’alterneriez généralement pas les appels de fonction et les points d’attente à chaque ligne, bien sûr. Bien que céder le contrôle de cette manière soit relativement peu coûteux, cela ne l’est pas gratuitement. Dans bien des cas, tenter de diviser une tâche limitée par le processeur peut la ralentir considérablement ; il est donc parfois préférable, pour les performances _globales_, de laisser une opération bloquer brièvement. Mesurez toujours votre code pour déterminer quels sont ses véritables goulots d’étranglement. Il est toutefois important de garder à l’esprit cette dynamique si vous constatez qu’une grande quantité de travail s’effectue en série alors que vous vous attendiez à ce qu’elle se déroule simultanément !

### Créer nos propres abstractions asynchrones

Nous pouvons également composer des futures pour créer de nouveaux modèles. Par exemple, nous pouvons créer une fonction `timeout` à partir des éléments asynchrones dont nous disposons déjà. Une fois terminée, elle constituera un autre élément de base que nous pourrons utiliser pour créer des abstractions asynchrones encore plus élaborées.

La liste 17-18 montre comment nous nous attendrions à ce que cette fonction `timeout` se comporte avec une future lente.

<Listing number="17-18" caption="Utiliser notre fonction `timeout` imaginée pour exécuter une opération lente dans un délai imparti" file-name="src/main.rs">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch17-async-await/listing-17-18/src/main.rs:here}}
```

</Listing>

Implémentons cette fonction ! Pour commencer, réfléchissons à l’API de `timeout` :

- Elle doit elle-même être une fonction asynchrone afin que nous puissions l’attendre.
- Son premier paramètre doit être une future à exécuter. Nous pouvons la rendre générique pour qu’elle fonctionne avec n’importe quelle future.
- Son second paramètre sera la durée maximale d’attente. Si nous utilisons une `Duration`, il sera facile de la transmettre à `trpl::sleep`.
- Elle doit renvoyer un `Result`. Si la future se termine avec succès, le `Result` sera `Ok` et contiendra la valeur produite par la future. Si le délai expire d’abord, le `Result` sera `Err` et contiendra la durée pendant laquelle la fonction `timeout` a attendu.

La liste 17-19 montre cette déclaration.

<!-- This is not tested because it intentionally does not compile. -->

<Listing number="17-19" caption="Définir la signature de `timeout`" file-name="src/main.rs">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch17-async-await/listing-17-19/src/main.rs:declaration}}
```

</Listing>

Cela répond à nos objectifs concernant les types. Réfléchissons maintenant au _comportement_ nécessaire : nous voulons mettre en concurrence la future transmise et la durée. Nous pouvons utiliser `trpl::sleep` pour créer une future de temporisation à partir de la durée, puis utiliser `trpl::select` pour exécuter cette temporisation avec la future transmise par l’appelant.

Dans la liste 17-20, nous implémentons `timeout` en faisant une correspondance sur le résultat de l’attente de `trpl::select`.

<Listing number="17-20" caption="Définir `timeout` avec `select` et `sleep`" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-20/src/main.rs:implementation}}
```

</Listing>

L’implémentation de `trpl::select` n’est pas équitable : elle interroge toujours les arguments dans l’ordre où ils sont transmis (d’autres implémentations de `select` choisissent aléatoirement l’argument à interroger en premier). Nous transmettons donc `future_to_try` à `select` en premier pour lui donner une chance de se terminer, même si `max_time` est très court. Si `future_to_try` se termine en premier, `select` renvoie `Left` avec la sortie de `future_to_try`. Si `timer` se termine en premier, `select` renvoie `Right` avec la sortie du temporisateur, `()`.

Si `future_to_try` réussit et que nous obtenons `Left(output)`, nous renvoyons `Ok(output)`. Si le temporisateur de sommeil expire et que nous obtenons `Right(())`, nous ignorons le `()` avec `_` et renvoyons plutôt `Err(max_time)`.

Nous avons ainsi créé une fonction `timeout` fonctionnelle à partir de deux autres outils asynchrones. Si nous exécutons notre code, il affichera le message d’échec une fois le délai expiré :

```text
Échec après 2 secondes
```

Comme les futures se composent avec d’autres futures, vous pouvez créer des outils très puissants à partir de petits éléments asynchrones. Par exemple, vous pouvez utiliser cette même approche pour associer des délais d’expiration à des tentatives répétées, puis utiliser le tout avec des opérations telles que des appels réseau (comme ceux de la liste 17-5).

En pratique, vous utiliserez généralement directement `async` et `await`, et, dans un second temps, des fonctions telles que `select` et des macros telles que la macro `join!` pour contrôler l’exécution des futures les plus externes.

Nous avons maintenant vu plusieurs façons de travailler avec plusieurs futures en même temps. Ensuite, nous verrons comment travailler avec plusieurs futures qui se succèdent au fil du temps, à l’aide des _flux_.

[async-program]: ch17-01-futures-and-syntax.html#our-first-async-program