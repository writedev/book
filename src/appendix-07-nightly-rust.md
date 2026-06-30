## Annexe G - Comment Rust est Fabriqué et « Rust Nightly »

Cette annexe traite de la façon dont Rust est fabriqué et de l'impact que cela a sur vous en tant que développeur Rust.

### Stabilité sans Stagnation

En tant que langage, Rust se soucie énormément de la stabilité de votre code. Nous voulons que Rust soit une fondation solide sur laquelle vous pouvez construire ; si les choses changeaient constamment, cela serait impossible. En même temps, si nous ne pouvons pas expérimenter de nouvelles fonctionnalités, nous risquons de ne découvrir des flaws importants qu'après leur publication, lorsque nous ne pouvons plus modifier quoi que ce soit.

Notre solution à ce problème est ce que nous appelons « stabilité sans stagnation », et notre principe directeur est le suivant : vous ne devriez jamais avoir peur de passer à une nouvelle version de Rust stable. Chaque mise à niveau doit être indolore, mais doit également vous apporter de nouvelles fonctionnalités, moins de bogues et des temps de compilation plus rapides.

### Choo, Choo ! Canaux de Publication et Montée à Bord des Trains

Le développement de Rust fonctionne sur un _calendrier de train_. C'est-à-dire que tout le développement se fait dans la branche principale du dépôt Rust. Les publications suivent un modèle de train de publication de logiciel, qui a été utilisé par Cisco IOS et d'autres projets logiciels. Il existe trois _canaux de publication_ pour Rust :

- Nightly
- Beta
- Stable

La plupart des développeurs Rust utilisent principalement le canal stable, mais ceux qui souhaitent essayer de nouvelles fonctionnalités expérimentales peuvent utiliser nightly ou beta.

Voici un exemple de la façon dont le processus de développement et de publication fonctionne : supposons que l'équipe Rust travaille sur la publication de Rust 1.5. Cette version est sortie en décembre 2015, mais elle nous fournira des numéros de version réalistes. Une nouvelle fonctionnalité est ajoutée à Rust : un nouveau commit est effectué dans la branche principale. Chaque nuit, une nouvelle version nightly de Rust est produite. Chaque jour est un jour de publication, et ces publications sont créées automatiquement par notre infrastructure de publication. Au fil du temps, nos publications ressemblent à ceci, chaque nuit :

```text
nightly: * - - * - - *
```

Tous les six semaines, c'est le moment de préparer une nouvelle publication ! La branche `beta` du dépôt Rust se sépare de la branche principale utilisée par nightly. Maintenant, il y a deux versions :

```text
nightly: * - - * - - *
                     |
beta:                *
```

La plupart des utilisateurs de Rust n'utilisent pas activement les publications beta, mais testent par rapport à beta dans leur système CI pour aider Rust à découvrir d'éventuelles régressions. En attendant, il y a toujours une publication nightly chaque nuit :

```text
nightly: * - - * - - * - - * - - *
                     |
beta:                *
```

Disons qu'une régression est trouvée. Heureusement, nous avons eu le temps de tester la publication beta avant que la régression ne se glisse dans une publication stable ! Le correctif est appliqué à la branche principale, afin que nightly soit corrigé, puis le correctif est reporté à la branche `beta`, et une nouvelle publication de beta est produite :

```text
nightly: * - - * - - * - - * - - * - - *
                     |
beta:                * - - - - - - - - *
```

Six semaines après la première beta, c'est le moment pour une publication stable ! La branche `stable` est produite à partir de la branche `beta` :

```text
nightly: * - - * - - * - - * - - * - - * - * - *
                     |
beta:                * - - - - - - - - *
                                       |
stable:                                *
```

Hourra ! Rust 1.5 est terminé ! Cependant, nous avons oublié une chose : parce que les six semaines se sont écoulées, nous avons également besoin d'une nouvelle beta de la _prochaine_ version de Rust, 1.6. Donc, après que `stable` se soit séparé de `beta`, la prochaine version de `beta` se sépare de `nightly` à nouveau :

```text
nightly: * - - * - - * - - * - - * - - * - * - *
                     |                         |
beta:                * - - - - - - - - *       *
                                       |
stable:                                *
```

Cela s'appelle le « modèle de train » car toutes les six semaines, une publication « quitte la station », mais doit toujours effectuer un voyage à travers le canal beta avant d'arriver en tant que publication stable.

Rust publie toutes les six semaines, comme une horloge. Si vous connaissez la date d'une publication Rust, vous pouvez connaître la date de la suivante : elle est six semaines plus tard. Un aspect agréable d'avoir des publications programmées toutes les six semaines est que le prochain train arrive bientôt. Si une fonctionnalité manque une publication particulière, il n'est pas nécessaire de s'inquiéter : une autre arrive dans peu de temps ! Cela aide à réduire la pression de faire entrer des fonctionnalités peut-être non polies juste avant la date limite de publication.

Grâce à ce processus, vous pouvez toujours consulter la prochaine version de Rust et vérifier par vous-même qu'il est facile de passer à la version suivante : si une publication beta ne fonctionne pas comme prévu, vous pouvez le signaler à l'équipe et la faire corriger avant la prochaine publication stable ! Les interruptions dans une publication beta sont relativement rares, mais `rustc` est toujours un logiciel et des bogues existent.

### Temps de Maintenance

Le projet Rust prend en charge la version stable la plus récente. Lorsqu'une nouvelle version stable est publiée, l'ancienne version atteint sa fin de vie (EOL). Cela signifie que chaque version est prise en charge pendant six semaines.

### Fonctionnalités Instables

Il y a encore un piège avec ce modèle de publication : les fonctionnalités instables. Rust utilise une technique appelée « drapeaux de fonctionnalités » pour déterminer quelles fonctionnalités sont activées dans une publication donnée. Si une nouvelle fonctionnalité est en cours de développement actif, elle est ajoutée à la branche principale et donc, dans nightly, mais derrière un _drapeau de fonctionnalité_. Si vous, en tant qu'utilisateur, souhaitez essayer la fonctionnalité en cours de développement, vous le pouvez, mais vous devez utiliser une publication nightly de Rust et annoter votre code source avec le drapeau approprié pour vous y inscrire.

Si vous utilisez une publication beta ou stable de Rust, vous ne pouvez pas utiliser de drapeaux de fonctionnalité. C'est la clé qui nous permet d'obtenir des utilisations pratiques de nouvelles fonctionnalités avant de les déclarer stables pour toujours. Ceux qui souhaitent opter pour le dernier cri peuvent le faire, et ceux qui veulent une expérience solide peuvent rester avec stable et savoir que leur code ne se cassera pas. Stabilité sans stagnation.

Ce livre ne contient que des informations sur des fonctionnalités stables, car les fonctionnalités en cours de développement changent encore, et elles seront certainement différentes entre le moment où ce livre a été écrit et le moment où elles seront activées dans des builds stables. Vous pouvez trouver de la documentation pour les fonctionnalités uniquement disponibles en nightly en ligne.

### Rustup et le Rôle de Rust Nightly

Rustup facilite le changement entre différents canaux de publication de Rust, au niveau global ou par projet. Par défaut, vous aurez Rust stable installé. Pour installer nightly, par exemple :

```console
$ rustup toolchain install nightly
```

Vous pouvez également voir tous les _toolchains_ (publications de Rust et composants associés) que vous avez installés avec `rustup`. Voici un exemple sur l'un des ordinateurs de vos auteurs sous Windows :

```powershell
> rustup toolchain list
stable-x86_64-pc-windows-msvc (par défaut)
beta-x86_64-pc-windows-msvc
nightly-x86_64-pc-windows-msvc
```

Comme vous pouvez le constater, le toolchain stable est par défaut. La plupart des utilisateurs de Rust utilisent stable la plupart du temps. Vous pourriez vouloir utiliser stable la plupart du temps, mais utiliser nightly sur un projet spécifique, car vous vous souciez d'une fonctionnalité à la pointe. Pour ce faire, vous pouvez utiliser `rustup override` dans le répertoire de ce projet pour définir le toolchain nightly comme celui que `rustup` doit utiliser lorsque vous êtes dans ce répertoire :

```console
$ cd ~/projects/needs-nightly
$ rustup override set nightly
```

Maintenant, chaque fois que vous appelez `rustc` ou `cargo` à l'intérieur de _~/projects/needs-nightly_, `rustup` s'assurera que vous utilisez Rust nightly, plutôt que votre défaut, Rust stable. Cela s'avère pratique lorsque vous avez de nombreux projets Rust !

### Le Processus RFC et les Équipes

Alors, comment apprenez-vous ces nouvelles fonctionnalités ? Le modèle de développement de Rust suit un _processus de Demande de Commentaires (RFC)_. Si vous souhaitez une amélioration dans Rust, vous pouvez rédiger une proposition, appelée RFC.

Tout le monde peut rédiger des RFC pour améliorer Rust, et les propositions sont examinées et discutées par l'équipe Rust, qui est composée de nombreuses sous-equipes thématiques. Il existe une liste complète des équipes [sur le site web de Rust](https://www.rust-lang.org/governance), qui comprend des équipes pour chaque domaine du projet : conception du langage, mise en œuvre du compilateur, infrastructure, documentation, et plus encore. L'équipe appropriée lit la proposition et les commentaires, écrit ses propres commentaires, et finalement, il y a consensus pour accepter ou rejeter la fonctionnalité.

Si la fonctionnalité est acceptée, un problème est ouvert sur le dépôt Rust, et quelqu'un peut l'implémenter. La personne qui l'implémente peut très bien ne pas être celle qui a proposé la fonctionnalité au départ ! Lorsque l'implémentation est prête, elle est intégrée à la branche principale derrière une porte de fonctionnalité, comme nous l'avons discuté dans la section [« Fonctionnalités Instables »](#unstable-features)<!-- ignore -->.

Après un certain temps, une fois que les développeurs Rust qui utilisent des versions nightly ont pu essayer la nouvelle fonctionnalité, les membres de l'équipe discuteront de la fonctionnalité, de la façon dont elle a fonctionné en nightly, et décideront si elle doit être intégrée dans Rust stable ou non. Si la décision est de passer à l'étape suivante, la porte de fonctionnalité est supprimée, et la fonctionnalité est désormais considérée comme stable ! Elle quitte le train pour une nouvelle publication stable de Rust.