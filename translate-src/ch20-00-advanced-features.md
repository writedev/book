# Fonctionnalités avancées

À ce stade, vous avez appris les parties du langage de programmation Rust les plus couramment utilisées. Avant de réaliser un dernier projet, au chapitre 21, nous allons examiner quelques aspects du langage que vous pourriez rencontrer de temps à autre, mais que vous n’utiliserez peut-être pas tous les jours. Vous pouvez consulter ce chapitre lorsque vous rencontrez des éléments inconnus. Les fonctionnalités présentées ici sont utiles dans des situations très spécifiques. Même si vous n’y aurez peut-être pas souvent recours, nous voulons nous assurer que vous maîtrisez toutes les fonctionnalités offertes par Rust.

Dans ce chapitre, nous aborderons :

- Rust non sécurisé : comment renoncer à certaines garanties de Rust et prendre la responsabilité de les faire respecter manuellement
- Les traits avancés : les types associés, les paramètres de type par défaut, la syntaxe entièrement qualifiée, les supertraits et le modèle newtype appliqué aux traits
- Les types avancés : plus d’informations sur le modèle newtype, les alias de types, le type jamais et les types à taille dynamique
- Les fonctions et les fermetures avancées : les pointeurs de fonction et le renvoi de fermetures
- Les macros : des façons de définir du code qui définit davantage de code à la compilation

C’est tout un éventail de fonctionnalités Rust, avec quelque chose pour tout le monde ! Plongeons-nous dans le sujet !