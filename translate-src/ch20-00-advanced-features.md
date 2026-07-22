# Fonctions Avancées

À ce stade, vous avez appris les parties les plus couramment utilisées du langage de programmation Rust. Avant de réaliser un dernier projet, dans le chapitre 21, nous allons examiner quelques aspects du langage que vous pourriez rencontrer de temps en temps, mais que vous n'utilisez peut-être pas tous les jours. Vous pouvez utiliser ce chapitre comme référence lorsque vous rencontrez des inconnues. Les fonctionnalités abordées ici sont utiles dans des situations très spécifiques. Bien que vous ne les utilisiez pas souvent, nous voulons nous assurer que vous avez une bonne compréhension de toutes les fonctionnalités offertes par Rust.

Dans ce chapitre, nous aborderons :

- Rust non sécurisé : Comment renoncer à certaines garanties de Rust et prendre la responsabilité de maintenir manuellement ces garanties
- Traits avancés : Types associés, paramètres de type par défaut, syntaxe pleinement qualifiée, supertraits et le motif newtype en relation avec les traits
- Types avancés : Plus d'informations sur le motif newtype, alias de type, type jamais, et types de taille dynamique
- Fonctions et fermetures avancées : Pointeurs de fonction et retour de fermetures
- Macros : Moyens de définir du code qui définit plus de code à la compilation

C’est une panoplie de fonctionnalités Rust avec quelque chose pour tout le monde ! Plongeons-y !