# Pointeurs intelligents

Un pointeur est un concept général pour une variable qui contient une adresse en mémoire. Cette adresse fait référence à, ou "pointe vers", d'autres données. Le type de pointeur le plus courant en Rust est une référence, que vous avez apprise au Chapitre 4. Les références sont indiquées par le symbole `&` et empruntent la valeur à laquelle elles pointent. Elles n'ont pas de capacités spéciales en dehors de faire référence à des données, et n'ont aucun coût additionnel.

Les _pointeurs intelligents_, en revanche, sont des structures de données qui agissent comme un pointeur mais possèdent également des métadonnées et des capacités supplémentaires. Le concept de pointeurs intelligents n'est pas unique à Rust : les pointeurs intelligents ont vu le jour en C++ et existent également dans d'autres langages. Rust dispose d'une variété de pointeurs intelligents définis dans la bibliothèque standard qui offrent des fonctionnalités allant au-delà de celles fournies par les références. Pour explorer le concept général, nous examinerons quelques exemples différents de pointeurs intelligents, y compris un type de pointeur intelligent à _compte de références_. Ce pointeur vous permet d'autoriser des données à avoir plusieurs propriétaires en suivant le nombre de propriétaires et, lorsqu'aucun propriétaire ne reste, de libérer les données.

En Rust, avec son concept de propriété et d'emprunt, il existe une différence supplémentaire entre les références et les pointeurs intelligents : tandis que les références ne font qu'emprunter des données, dans de nombreux cas, les pointeurs intelligents _possèdent_ les données auxquelles ils pointent.

Les pointeurs intelligents sont généralement implémentés à l'aide de structures. Contrairement à une structure ordinaire, les pointeurs intelligents implémentent les traits `Deref` et `Drop`. Le trait `Deref` permet à une instance de la structure de pointeur intelligent de se comporter comme une référence afin que vous puissiez écrire votre code pour fonctionner avec des références ou des pointeurs intelligents. Le trait `Drop` vous permet de personnaliser le code qui est exécuté lorsqu'une instance de pointeur intelligent sort du scope. Dans ce chapitre, nous allons discuter de ces deux traits et démontrer pourquoi ils sont importants pour les pointeurs intelligents.

Étant donné que le modèle de pointeur intelligent est un modèle de conception général fréquemment utilisé en Rust, ce chapitre ne couvrira pas tous les pointeurs intelligents existants. De nombreuses bibliothèques ont leurs propres pointeurs intelligents, et vous pouvez même écrire les vôtres. Nous couvrirons les pointeurs intelligents les plus courants dans la bibliothèque standard :

- `Box<T>`, pour allouer des valeurs sur le tas
- `Rc<T>`, un type de compte de références qui permet la propriété multiple
- `Ref<T>` et `RefMut<T>`, accessibles via `RefCell<T>`, un type qui impose les règles d'emprunt à l'exécution plutôt qu'à la compilation

De plus, nous aborderons le modèle de _mutabilité intérieure_ où un type immuable expose une API pour muter une valeur intérieure. Nous discuterons également des cycles de références : comment ils peuvent entraîner des fuites de mémoire et comment les prévenir.

Plongeons-nous !