# Pointeurs intelligents

Un pointeur est un concept général désignant une variable qui contient une adresse en mémoire. Cette adresse fait référence à d’autres données, ou « pointe vers » celles-ci. Le type de pointeur le plus courant en Rust est une référence, que vous avez découverte au chapitre 4. Les références sont représentées par le symbole `&` et empruntent la valeur vers laquelle elles pointent. Elles n’ont aucune capacité particulière autre que celle de faire référence à des données, et elles n’ont aucun coût supplémentaire.

Les _pointeurs intelligents_, quant à eux, sont des structures de données qui se comportent comme des pointeurs, mais possèdent également des métadonnées et des capacités supplémentaires. Le concept de pointeur intelligent n’est pas propre à Rust : les pointeurs intelligents sont apparus en C++ et existent aussi dans d’autres langages. Rust dispose de plusieurs pointeurs intelligents définis dans sa bibliothèque standard, qui offrent des fonctionnalités allant au-delà de celles fournies par les références. Pour explorer ce concept général, nous allons examiner quelques exemples de pointeurs intelligents, dont un type de pointeur intelligent à _comptage de références_. Ce pointeur permet à plusieurs propriétaires de posséder des données en gardant le compte du nombre de propriétaires et, lorsqu’il n’en reste plus aucun, en nettoyant les données.

En Rust, avec ses concepts de propriété et d’emprunt, il existe une différence supplémentaire entre les références et les pointeurs intelligents : alors que les références ne font qu’emprunter des données, dans de nombreux cas, les pointeurs intelligents _possèdent_ les données vers lesquelles ils pointent.

Les pointeurs intelligents sont généralement implémentés à l’aide de structures. Contrairement à une structure ordinaire, les pointeurs intelligents implémentent les traits `Deref` et `Drop`. Le trait `Deref` permet à une instance de la structure du pointeur intelligent de se comporter comme une référence, afin que vous puissiez écrire du code qui fonctionne aussi bien avec des références qu’avec des pointeurs intelligents. Le trait `Drop` permet de personnaliser le code exécuté lorsqu’une instance du pointeur intelligent sort de portée. Dans ce chapitre, nous aborderons ces deux traits et montrerons pourquoi ils sont importants pour les pointeurs intelligents.

Puisque le modèle des pointeurs intelligents est un modèle de conception général fréquemment utilisé en Rust, ce chapitre ne couvrira pas tous les pointeurs intelligents existants. De nombreuses bibliothèques ont leurs propres pointeurs intelligents, et vous pouvez même créer les vôtres. Nous aborderons les pointeurs intelligents les plus courants de la bibliothèque standard :

- `Box<T>`, pour allouer des valeurs sur le tas
- `Rc<T>`, un type à comptage de références qui permet une propriété multiple
- `Ref<T>` et `RefMut<T>`, accessibles par l’intermédiaire de `RefCell<T>`, un type qui applique les règles d’emprunt à l’exécution plutôt qu’à la compilation

Nous aborderons également le modèle de _mutabilité intérieure_, dans lequel un type immuable expose une API permettant de modifier une valeur intérieure. Nous parlerons aussi des cycles de références : comment ils peuvent entraîner des fuites de mémoire et comment les éviter.

Plongeons dans le sujet !