## Annexe G - Comment Rust est développé et « Rust nightly »

Cette annexe explique comment Rust est développé et quelles conséquences cela a pour vous en tant que développeur Rust.

### La stabilité sans stagnation

En tant que langage, Rust accorde _beaucoup_ d’importance à la stabilité de votre code. Nous voulons que Rust soit une base solide sur laquelle vous puissiez bâtir, et si tout changeait constamment, ce serait impossible. En même temps, si nous ne pouvons pas expérimenter de nouvelles fonctionnalités, nous risquons de ne découvrir des défauts importants qu’après leur publication, lorsqu’il est trop tard pour modifier quoi que ce soit.

Notre solution à ce problème est ce que nous appelons la « stabilité sans stagnation », et notre principe directeur est le suivant : vous ne devriez jamais avoir à craindre de passer à une nouvelle version de Rust stable. Chaque mise à jour devrait se faire sans difficulté, tout en vous apportant de nouvelles fonctionnalités, moins de bogues et des temps de compilation plus courts.

### Tchou, tchou ! Canaux de publication et train de versions

Le développement de Rust suit un _calendrier de trains_. Autrement dit, tout le développement se fait dans la branche principale du dépôt Rust. Les versions suivent un modèle de train de publication logicielle, utilisé par Cisco IOS et d’autres projets logiciels. Rust possède trois _canaux de publication_ :

- Nightly
- Beta
- Stable

La plupart des développeurs Rust utilisent principalement le canal stable, mais ceux qui veulent essayer de nouvelles fonctionnalités expérimentales peuvent utiliser nightly ou beta.

Voici un exemple du fonctionnement du processus de développement et de publication : supposons que l’équipe Rust travaille à la sortie de Rust 1.5. Cette version est sortie en décembre 2015, mais elle nous fournira des numéros de version réalistes. Une nouvelle fonctionnalité est ajoutée à Rust : un nouveau commit est intégré à la branche principale. Chaque nuit, une nouvelle version nightly de Rust est produite. Chaque jour est un jour de publication, et ces versions sont créées automatiquement par notre infrastructure de publication. Au fil du temps, nos versions ressemblent donc à ceci, chaque nuit :

```text
nightly: * - - * - - *
```

Toutes les six semaines, vient le moment de préparer une nouvelle version ! La branche `beta` du dépôt Rust est créée à partir de la branche principale utilisée par nightly. Il y a désormais deux versions :

```text
nightly: * - - * - - *
                     |
beta:                *
```

La plupart des utilisateurs de Rust n’utilisent pas activement les versions beta, mais les testent dans leur système d’intégration continue pour aider Rust à détecter d’éventuelles régressions. Pendant ce temps, une version nightly continue de paraître chaque nuit :

```text
nightly: * - - * - - * - - * - - *
                     |
beta:                *
```

Supposons qu’une régression soit détectée. Heureusement que nous avons eu le temps de tester la version beta avant que la régression ne se glisse dans une version stable ! Le correctif est appliqué à la branche principale, ce qui corrige nightly, puis il est rétroporté vers la branche `beta`, et une nouvelle version beta est produite :

```text
nightly: * - - * - - * - - * - - * - - *
                     |
beta:                * - - - - - - - - *
```

Six semaines après la création de la première beta, vient le moment de publier une version stable ! La branche `stable` est créée à partir de la branche `beta` :

```text
nightly: * - - * - - * - - * - - * - - * - * - *
                     |
beta:                * - - - - - - - - *
                                       |
stable:                                *
```

Hourra ! Rust 1.5 est prêt ! Cependant, nous avons oublié une chose : puisque six semaines se sont écoulées, nous devons également créer une nouvelle beta de la _prochaine_ version de Rust, la 1.6. Ainsi, après la création de la branche `stable` à partir de `beta`, la branche `beta` de la version suivante est à nouveau créée à partir de `nightly` :

```text
nightly: * - - * - - * - - * - - * - - * - * - *
                     |                         |
beta:                * - - - - - - - - *       *
                                       |
stable:                                *
```

On appelle cela le « modèle du train », car toutes les six semaines, une version « quitte la gare », mais doit encore parcourir le canal beta avant d’arriver sous la forme d’une version stable.

Rust publie une nouvelle version toutes les six semaines, comme une horloge. Si vous connaissez la date d’une version de Rust, vous pouvez connaître celle de la suivante : six semaines plus tard. L’avantage des publications programmées toutes les six semaines, c’est que le prochain train arrive bientôt. Si une fonctionnalité ne parvient pas à être prête à temps pour une version donnée, inutile de s’inquiéter : une autre suivra sous peu ! Cela réduit la pression qui pourrait pousser à intégrer des fonctionnalités insuffisamment abouties à l’approche de la date limite de publication.

Grâce à ce processus, vous pouvez toujours essayer la prochaine version de Rust et vérifier par vous-même qu’il est facile de mettre à niveau votre installation : si une version beta ne fonctionne pas comme prévu, vous pouvez le signaler à l’équipe, qui pourra corriger le problème avant la prochaine version stable ! Les régressions dans une version beta sont relativement rares, mais `rustc` reste un logiciel, et les bogues existent.

### Durée de maintenance

Le projet Rust prend en charge la version stable la plus récente. Lorsqu’une nouvelle version stable est publiée, l’ancienne arrive en fin de vie (EOL). Cela signifie que chaque version est prise en charge pendant six semaines.

### Fonctionnalités instables

Ce modèle de publication comporte un autre élément à prendre en compte : les fonctionnalités instables. Rust utilise une technique appelée « indicateurs de fonctionnalité » pour déterminer quelles fonctionnalités sont activées dans une version donnée. Si une nouvelle fonctionnalité est en cours de développement, elle est intégrée à la branche principale, et donc à nightly, mais reste protégée par un _indicateur de fonctionnalité_. Si, en tant qu’utilisateur, vous souhaitez essayer cette fonctionnalité en cours de développement, vous le pouvez, mais vous devez utiliser une version nightly de Rust et annoter votre code source avec l’indicateur approprié pour l’activer.

Si vous utilisez une version beta ou stable de Rust, vous ne pouvez pas utiliser d’indicateurs de fonctionnalité. C’est ce qui nous permet d’utiliser concrètement de nouvelles fonctionnalités avant de les déclarer stables pour toujours. Ceux qui souhaitent accéder aux toutes dernières nouveautés peuvent le faire, tandis que ceux qui veulent une expérience parfaitement stable peuvent s’en tenir à stable, en sachant que leur code ne cessera pas de fonctionner. La stabilité sans stagnation.

Ce livre ne traite que des fonctionnalités stables, car les fonctionnalités en cours de développement changent encore, et elles seront certainement différentes entre le moment où ce livre a été écrit et celui où elles seront activées dans les versions stables. Vous trouverez en ligne la documentation des fonctionnalités réservées à nightly.

### Rustup et le rôle de Rust nightly

Rustup permet facilement de passer d’un canal de publication de Rust à un autre, à l’échelle du système ou projet par projet. Par défaut, Rust stable est installé. Pour installer nightly, par exemple :

```console
$ rustup toolchain install nightly
```

Vous pouvez également afficher toutes les _chaînes d’outils_ (versions de Rust et composants associés) que vous avez installées avec `rustup`. Voici un exemple sur l’ordinateur Windows de l’un des auteurs :

```powershell
> rustup toolchain list
stable-x86_64-pc-windows-msvc (default)
beta-x86_64-pc-windows-msvc
nightly-x86_64-pc-windows-msvc
```

Comme vous pouvez le constater, la chaîne d’outils stable est celle utilisée par défaut. La plupart des utilisateurs de Rust utilisent stable la plupart du temps. Vous souhaiterez peut-être utiliser stable la plupart du temps, mais nightly pour un projet précis, parce qu’une fonctionnalité de pointe vous intéresse. Pour cela, vous pouvez utiliser `rustup override` dans le répertoire du projet afin de définir la chaîne d’outils nightly comme celle que `rustup` doit utiliser lorsque vous vous trouvez dans ce répertoire :

```console
$ cd ~/projects/needs-nightly
$ rustup override set nightly
```

Désormais, chaque fois que vous appellerez `rustc` ou `cargo` dans _~/projects/needs-nightly_, `rustup` veillera à ce que vous utilisiez Rust nightly plutôt que Rust stable, qui est la version par défaut. C’est très pratique lorsque vous avez beaucoup de projets Rust !

### Le processus RFC et les équipes

Comment se tenir au courant de ces nouvelles fonctionnalités ? Le modèle de développement de Rust suit un _processus de demande de commentaires (Request For Comments, RFC)_. Si vous souhaitez proposer une amélioration de Rust, vous pouvez rédiger une proposition appelée RFC.

Tout le monde peut rédiger des RFC pour améliorer Rust. Les propositions sont examinées et discutées par l’équipe Rust, qui se compose de nombreuses sous-équipes spécialisées. Vous trouverez la liste complète des équipes [sur le site Web de Rust](https://www.rust-lang.org/governance). Elle comprend des équipes pour chaque domaine du projet : conception du langage, implémentation du compilateur, infrastructure, documentation, et bien d’autres. L’équipe concernée lit la proposition et les commentaires, formule ses propres commentaires et finit par parvenir à un consensus sur l’acceptation ou le rejet de la fonctionnalité.

Si la fonctionnalité est acceptée, une issue est créée dans le dépôt Rust, et quelqu’un peut l’implémenter. Il se peut très bien que la personne qui l’implémente ne soit pas celle qui l’a proposée au départ ! Lorsque l’implémentation est prête, elle est intégrée à la branche principale derrière un garde de fonctionnalité, comme nous l’avons expliqué dans la section [« Fonctionnalités instables »](#unstable-features)<!-- ignore -->.

Après un certain temps, une fois que les développeurs Rust qui utilisent les versions nightly ont pu essayer la nouvelle fonctionnalité, les membres de l’équipe en discutent, examinent son fonctionnement dans nightly et décident si elle doit être intégrée à Rust stable. Si la décision est positive, le garde de fonctionnalité est supprimé, et la fonctionnalité est alors considérée comme stable ! Elle emprunte les trains jusqu’à une nouvelle version stable de Rust.