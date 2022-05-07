# JAVA

### string vs new string（）

string a = “hello”创建时首先会在字符串常量池string table中找，看是否有相等的对象，没有的话就在heap中创建一个对象，并把引用地址存放在string table中，然后将这个对象的引用赋给a这个变量

string a = new string("hello") 也是一样只是即使string table中有hello，还是会在heap中创建一个对象，把这个对象的引用赋给a

stringtable jdk1.6在堆上，jdk1.7之后放在方法区（1.7是永生代，1.8是元空间）

```
public String toString() {
    return getClass().getName() + "@" + Integer.toHexString(hashCode());
}
```

### Integer

java有个内部静态类IntegerCache.java，它缓存了-128-127之间的整数，如果在这个范围内，=和valueOf()方法会直接返回cache中的数，不在范围就会在堆中创建对象

why在此范围内的“小”整数使用率比大整数要高，可以减少潜在的内存占用。

### Comparator vs Comparable

Comparable和 Comparator都是接口

1.class继承了comparable接口，重写compareto，实例对象之间就可以直接比较

```
class person implements comparable {
	@Override
	public int compareTo(Person p) {...}
}
ArrayList<person> list = new ArrayList<>();
collection.sort(list)
```

2.如果不想让一个类implements comparable，或者不想修改原来类的compare方法，也可以在外部比较

1）写一个类implements Comparator

2）创建一个实例

3）sort的时候把list和这个实例一起传入 

````
ArrayList<person> list = new ArrayList<>();
class RatingCompare implements Comparator<person> {public int compare(p a, p b){...}}
Collections.sort(list, ratingCompare);
````

### String和StringBuilder、StringBuffer的区别

都是final类，都不允许被继承；

String类长度是不可变的，StringBuffer和StringBuilder类长度是可以改变的；

StringBuffer类是线程安全的，StringBuilder不是线程安全的；

StringBuilder 和 StringBuffer 底层是 char[] 数组，StringBuffer用synchronized的修饰。保证线程安全。

###  transient关键字

java 的transient关键字为我们提供了便利，你只需要实现Serilizable接口，将不需要序列化的属性前添加关键字transient，序列化对象的时候，这个属性就不会序列化到指定的目的地中。比如密码什么的，不想serialized出来

（1）一旦变量被transient修饰，变量将不再是对象持久化的一部分，该变量内容在序列化后无法获得访问。

（2）transient关键字只能修饰变量，而不能修饰方法和类。注意，本地变量是不能被transient关键字修饰的。变量如果是用户自定义类变量，则该类需要实现Serializable接口。

（3）被transient关键字修饰的变量不再能被序列化，一个静态变量不管是否被transient修饰，均不能被序列化。

### 泛型

generic：允许在定义类，接口，方法的时候使用类型型参（泛型）、在声明变量、创建对象、调用方法的时候动态的指定实际类型。带来了简洁性和健壮性

泛型通配符 ？

1.上限`Foo<? extends Person>`为了支持协变：Foo是Bar的子类，  A<Foo> 就是A<? extends Bar> 的子类，将前者赋给后者就是协变。

协变只出不进：只能调用泛型类型作为返回值类型的方法，（编译器当作通配符上限类型）不可以作为方法传入参数

2.下限为了支持类型型变，`Foo<? super Person>`, 逆变只出不进

### 异常

1.可查异常（编译器要求必须处置的异常）：正确的程序在运行中，很容易出现的、情理可容的异常状况。除了Exception中的RuntimeException及其子类以外，其他的Exception类及其子类(例如：IOException和ClassNotFoundException)都属于可查异常。这种异常的特点是Java编译器会检查它，也就是说，当程序中可能出现这类异常，要么用try-catch语句捕获它，要么用throws子句声明抛出它，否则编译不会通过。

2.不可查异常(编译器不要求强制处置的异常):包括运行时异常（RuntimeException与其子类）和错误（Error）。RuntimeException表示编译器不会检查程序是否对RuntimeException作了处理，在程序中不必捕获RuntimException类型的异常，也不必在方法体声明抛出RuntimeException类。RuntimeException发生的时候，表示程序中出现了编程错误，所以应该找出错误修改程序，而不是去捕获RuntimeException



Error（错误）:是程序无法处理的错误，表示运行应用程序中较严重问题。大多数错误与代码编写者执行的操作无关，而表示代码运行时 JVM（Java 虚拟机）出现的问题。例如，Java虚拟机运行错误（Virtual MachineError），当 JVM 不再有继续执行操作所需的内存资源时，将出现 OutOfMemoryError。这些异常发生时，Java虚拟机（JVM）一般会选择线程终止。这些错误表示故障发生于虚拟机自身、或者发生在虚拟机试图执行应用时，如Java虚拟机运行错误（Virtual MachineError）、类定义错误（NoClassDefFoundError）等。

### equals（）



### hash

Hash code哈希值：把任意长度的输入，通过hash算法，变换成固定长度的输出，该输出就是hashcode、是一个二进制值、唯一性、对称性、传递性、反射性

hash算法：安全的hash算法要求1.碰撞概率低 2.不能猜测出输出。常见的有md5（输出16bytes），sha1（20字节）、sha255（32字节），sha256（64字节）

Hash碰撞：哈希碰撞是指，两个不同的输入得到了相同的输出，不可避免，根据碰撞概率，哈希算法的输出长度越长，就越难产生碰撞，也就越安全。

```java
public native int hashCode(); //default, donot know
public static int hashCode(byte[] value) {  //for StringUTF16
        int h = 0;
        int length = value.length >> 1;
        for (int i = 0; i < length; i++) {
            h = 31 * h + getChar(value, i);
        }
        return h;
}
public static int hashCode(int value) {   // for integer,int 
        return value;
}
```

### hashmap

jdk1.8

HashMap的默认初始容量为16

```
static int indexFor(int h, int length) {
    return h & (length-1);
}
static final int hash(Object key) {
     int h;
     return (key == null) ? 0 : (h = key.hashCode()) ^ (h >>> 16);
}
why? 要是高16位也参与运算，会让得到的下标更加散列。
```

HashMap的底层说起，那1.7 和1.8 的版本是有些不一样的地方。

1.7的底层是数组+单链表。1.8的时候是数组加上单链表或者红黑树。单链表到红黑树的转换，在链表长度大于8并且哈希桶的大小大于等于64的时候，会转换。如果红黑树节点的数量小于等于6的时候，会重新转换成单链表。

哈希桶的默认数量是16，负载因子是0.75

扩容：当哈希桶的数量大于：16 * 0.75=12 时候，触发扩容，首先会把哈希桶的数量变成原来的2倍。然后原来老的那些元素再rehash，填充到新的哈希桶里面。动态加载

Why 线程不安全？

1.扩容时新旧index上的链表顺序时相反的，会造成闭环，get时就会死循环，1.7头插法导致循环，1.8使用尾插法：

2.多线程会造成覆盖

### 红黑树 vs AVL

平衡树是为了解决二叉查找树退化为链表的情况，而红黑树是为了解决平衡树在插入、删除等操作需要频繁调整的情况。

AVL：但是要进行预先或随后做一次或多次所谓的"AVL旋转"。

任一节点对应的两棵子树的最大高度差为1

红黑树：

```
1. 具有二叉查找树的特点。
2. 根节点是黑色的；
3. 每个叶子节点都是黑色的空节点（NIL），也就是说，叶子节点不存数据。
4. 任何相邻的节点都不能同时为红色，也就是说，红色节点是被黑色节点隔开的。
5. 每个节点，从该节点到达其可达的叶子节点是所有路径，都包含相同数目的黑色节点
```

Q: 为什么有了平衡树还需要红黑树？

A: 因为红黑树的插入删除速度比AVL快。

因为为了保证严格的平衡树的性质，需要频繁的左旋右旋来进行调整，所以在插入删除很频繁的场景中，平衡树性能会降低很多。

红黑树在插入、删除等操作，不会像平衡树那样，频繁着破坏红黑树的规则，所以不需要频繁着调整。红黑树是一种不大严格的平衡树。也可以说是一个折中方案。

### HashMap如果我想要让自己的Object作为Key应该怎么办

1. 重写hashCode()是因为在map这样的结构中，需要计算存储数据的存储位置，需要注意不要试图从散列码计算中排除掉一个对象的关键部分来提高性能，这样虽然能更快但可能会导致更多的Hash碰撞；
2. 重写equals()方法，需要遵守自反性、对称性、传递性、一致性以及对于任何非null的引用值x，x.equals(null)必须返回false的这几个特性，目的是为了保证key在哈希表中的唯一性（Java建议重写equal方法的时候需重写hashcode的方法）

### 反射

Java 反射机制可以动态的创建对象并调用其属性，这样对象的类型在编译期是未知的。 程序中一般的对象类型都是在编译期就确定下来的。

通过反射，我们可以在运行时获得程序中 每一个类型成员和成员变量的信息。

通过反射来生成对象主要有两种方式。
 （1）使用 Class 对象的 getInstance() 方法来创建对象对应类的实例。

```dart
Class<?> c  = String.class;
Object str = c.getInstance();
```

（2）先通过 Class 对象获取指定的 Constructor 对象，在调用 Constructor 对象的 newInstance() 方法来创建实例。这种方法可以用指定的构造器构造类的实例。

```tsx
  //获取String所对应的Class对象
   Class<?> c = String.class;
  //获取String类带一个String参数的构造器
  Constructor constructor = c.getConstructor(String.class);
  //根据构造器创建实例
  Object obj = constructor.newInstance("23333");
  System.out.println(obj);
```

### IO

|        | 输入流      | 输出流       |
| ------ | ----------- | ------------ |
| 字节流 | InputStream | OutputStream |
| 字符流 | Reader      | Writer       |

- 从流的传输单位划分： 分为 `字节流`（8位字节），`字符流`（16位的字符）

IO 流用了 装饰者模式和适配器模式

### HashSet和HashMap

HashSet的value存的是一个static finial PRESENT = newObject()。而HashSet的remove是使用HashMap实现,则是map.remove而map的移除会返回value,如果底层value都是存null,显然将无法分辨是否移除成功。

### Boolean占几个字节

未精确定义字节。Java语言表达式所操作的boolean值，在编译之后都使用Java虚拟机中的int数据类型来代替，而 boolean[] 将会被编码成Java虚拟机的byte数组，每个boolean元素占8位。

### JVM类加载过程

当程序主动使用某个类的时候，如果该类还未被加载到内存，系统将会通过加载，连接。初始化三个步骤来对该类进行初始化。

1.类加载：将类的class文件读入内存，并为之创建一个java.lang.class实例对象。由加载器完成。jvm规范无需首次使用，允许预先加载某些类。

2.类的连接：把类的二进制数据合并到jre中，验证（检验被加载类是否与有正确的内部结构，并和其他类协调）

准备（为类的类变量分配内存，并设置默认值）解析（将类的二进制数据的二进制符号引用替换成直接引用）

3.类的初始化：类指定的值和静态初始化块按照代码排列顺序

步骤：假如这个类还没被加载和连接，则程序先加载并连接该类

​            假如该类的直接父类还没有被初始化，则先初始化直接父类-----jvm最先初始化java.lang.object类

​			假如类中有初始化语句，则系统依次执行这些初始化语句           

时机：创建类实例、调用类方法、访问类变量、class.forname("person") (new classloader().loadclass("person") 只是加载类不会初始化)

### 类加载器

同一个类不会被重复加载，类（person、pg、kl）和 类（person、pg、kl2）是不同的，包名+类名+类加载器区分。

jvm启动的时候，会形成三个类加载器组成的层次结构（不是继承关系哦，是组合关系）

1.bootstrap classloader：根类加载器、c++编写的虚拟机自己的一部分, 不是继承于`java.lang.ClassLoader`的类加载器，负责加载`<JAVA_HOME>\lib`目录中的，或者被`-Xbootclasspath`参数所指定的路径

2.extension classloader：扩展加载器、负责加载`<JAVA_HOME>\lib\ext`目录中的，或者被`java.ext.dirs`系统变量所指定路径中的所有类库

3. application classloader：系统加载器、负责加载用户类路径（`ClassPath`）上所指定的类库

4.开发者也可以实现自己的类加载器

jvm类加载器有三种机制

1.全盘负责：当一个类加载器负责加载某个类的时候，该class所依赖和引用的其他class也由该类负责载入

2.父类委托：先让parent父类加载器试图加载该class，只有在父类加载器无法加载该类的时候才尝试从自己的类路径中加载该类

3.缓存机制：保证加载过的class都会被缓存，当程序使用某个class时，类加载器先从缓存中搜索该class，不存在时候才读取该类对应的二进制转化为class对象，存入内存。

### 类加载器加载class过程

loadclass（）方法

1.检测次class是否被载入过（缓存区中是否有该class）findloadedclass（）如果有，直接返回该class对象

2.如果父类加载器存在，依次交给父类加载器载入目标类，如果成功就返回class对象

3.如果父类加载失败，当前类加载器findclass（）尝试寻找class文件（从与此classloader相关的类路径中寻找）如果找到就载入，载入失败会抛出classnotFoundException异常

### 双亲委派模型破坏

why？ 一个非常明显的目的就是保证java官方的类库<JAVA_HOME>\lib和扩展类库<JAVA_HOME>\lib\ext的加载安全性，不会被开发者覆盖。

例如类java.lang.Object，它存放在rt.jar之中，无论哪个类加载器要加载这个类，最终都是委派给根类加载器加载，因此Object类在程序的各种类加载器环境中都是同一个类。

如果开发者自己开发开源框架，也可以自定义类加载器，利用双亲委派模型，保护自己框架需要加载的类不被应用程序覆盖。

如何破坏？

第一种，自定义类加载器，必须重写`findClass`和`loadClass`；

第二种是通过线程上下文类加载器的传递性，让父类加载器中调用子类加载器的加载动作。

重写`loadClass`：

1、*找到ext classLoader，并首先委派给它加载，（为什么？*双亲委派的破坏只能发生在`AppClassLoader`及其以下的加载委派顺序，`ExtClassLoader`上面的双亲委派是不能破坏的！）

*2、自己加载*

3、*自己加载不了，再调用父类loadClass，保持双亲委派模式* 

通过自定义类加载器破坏双亲委派的案例在日常开发中非常常见，比如Tomcat为了实现web应用间加载隔离，自定义了类加载器，每个Context代表一个web应用，都有一个webappClassLoader。再如热部署、热加载的实现都是需要自定义类加载器的。破坏的位置都是跳过AppClassLoader。

线程上下文类加载器：

解决问题：服务提供者接口spi第三方软件实现，比如jdbc和jdni，这些spi接口属于核心类库，一般在jtjar包里，由根类加载器加载，而第三方实现的代码一般作为依赖jar包放在classpath路径下。当spi接口中的代码需要加载第三方实现类并调用相关方法的时候，bootstrap不能直接加载位于classpath下的具体实现类。

实现：通过java.lang.Thread的getcontextclassloader（）获取

比如，bootstrapclassloader 直接加载java.sql.driver 委托contextclassloader加载com.mysql.driver

具体代码在java.sql.drivermanager里面

### 热部署类加载器

想要让一个类重复加载，可以让不同的类加载器来加载，使用findclass（）。因为如果loadclass（）

会默认双亲委派模式，同一个类被重复加载就会报错。

### 什么情况下需要开始类加载过程的第一个阶段加载

1. 遇到new、getstatic、putstatic或invokestatic这4条字节码指令时，如果类没有进行过初始化，则需要先触发其初始化。生成这4条指令的最常见的Java代码场景是：使用new关键字实例化对象的时候、读取或设置一个类的静态字段（被final修饰、已在编译期把结果放入常量池的静态字段除外）的时候，以及调用一个类的静态方法的时候。
2. 使用java.lang.reflect包的方法对类进行反射调用的时候，如果类没有进行过初始化，则需要先触发其初始化。
3. 当初始化一个类的时候，如果发现其父类还没有进行过初始化，则需要先触发其父类的初始化。
4. 当虚拟机启动时，用户需要指定一个要执行的主类（包含main（）方法的那个类），虚拟机会先初始化这个主类。

### 运行时数据区域

JVM 规范下分为：

![截屏2021-12-21 上午2.31.58](/Users/jialinzhang/Library/Application Support/typora-user-images/截屏2021-12-21 上午2.31.58.png)

1. pc：程序计数器是一块较小的内存空间，它可以看作是当前线程所执行的字节码的行号指示器。在虚拟机的概念模型里，字节码解释器工作时就是通过改变这个计数器的值来选取下一条需要执行的字节码指令，分支、循环、跳转、异常处理、线程恢复等基础功能都需要依赖这个计数器来完成。是线程私有”的内存。

2. Java虚拟机栈：与程序计数器一样，Java虚拟机栈（Java Virtual Machine Stacks）也是线程私有的，它的生命周期与线程相同。虚拟机栈描述的是Java方法执行的内存模型：每个方法在执行的同时都会创建一个栈帧frames ，用于存储局部变量表、操作数栈、动态链接、方法出口等信息。每一个方法从调用直至执行完成的过程，就对应着一个栈帧在虚拟机栈中入栈到出栈的过程。

3. 本地方法栈：本地方法栈（Native Method Stack）与虚拟机栈所发挥的作用是非常相似的，它们之间的区别不过是虚拟机栈为虚拟机执行Java方法（也就是字节码）服务，而本地方法栈则为虚拟机使用到的Native方法c/c++服务。

4. Java堆：堆内存是 JVM 所有线程共享的部分，在虚拟机启动的时候就已经创建。所有的对象和数组都在堆上进行分配。这部分空间可通过 GC 进行回收。当申请不到空间时会抛出 OutOfMemoryError。

5. 方法区：

   ​      存放的是类信息、常量、静态变量

   ​       Jdk1.8之前 只有HotSpot 才有 “PermGen space”，是对jvm方法区规范的实现；JDK 1.8 中， HotSpot 已经没有 “PermGen space”这个区间了，取而代之是一个叫做 Metaspace（元空间）

   ​     区别在于：元空间并不在虚拟机中，而是使用本地内存。因此，默认情况下，元空间的大小仅受本地内存限制，但可以通过以下参数来指定元空间的大小

   ​      why？　1. 字符串存在永久代中，容易出现性能问题和内存溢出。

   ​                     2 .类及方法的信息等比较难确定其大小，因此对于永久代的大小指定比较困难，太小容易出现永          久代溢出，太大则容易导致老年代溢出。

   ​                     3.永久代会为 GC 带来不必要的复杂度，并且回收效率偏低。

6. 直接内存 Direct Memory

   ​            并不再jvm规范中，但也会引发outofmemory；jdk1.4后，NIO类，引入了基于channel和buffer的Io方式，它可以使用native函数库直接分配堆外内存，然后通过一个存储在heap中的directbytebuffer对象作为这块内存的引用操作，避免java heap和native堆来回复制数据。

### 对象的创建过程

1.class loading

2.class linking(verification, preparation, resolution)

3.class initializing：静态变量赋初始值，执行static块

4.申请对象内存

5.成员变量赋默认值

6.调用构造方法：成员变量赋初始值，执行构造方法语句

### 对象在内存中的存储布局

普通对象包括：1.对象头/markword，8个字节

​						   2.class pointer指针指向class

​                           3.成员变量

​						   4.padding对齐，8的倍数

数组对象包括： 1.对象头 2. Class pointer 3. 数组长度 4字节 4.数组数据 	5.padding

### 对象头

1.锁标记位：有两位用来标志次对象是否被锁定

2.gc标记：对象被回收多少次，分代年龄4bit

3.hashcode：没有被重写时才会被写在这里 system.identityhashcode()

4.线程id：使用偏向锁时，也就是锁标记为01会出现

等等     

### 常见的垃圾回收机制

1. 引用计数法：引用计数法是一种简单但速度很慢的垃圾回收技术。每个对象都含有一个引用计数器,当有引用连接至对象时,引用计数加1。当引用离开作用域或被置为null时,引用计数减1。虽然管理引用计数的开销不大,但这项开销在整个程序生命周期中将持续发生。垃圾回收器会在含有全部对象的列表上遍历,当发现某个对象引用计数为0时,就释放其占用的空间。
2. 可达性分析算法：从“GC Roots”的对象作为起始点，从这些节点开始向下搜索，搜索所走过的路径称为引用链，当一个对象到GC Roots没有任何引用链相连时，则证明此对象是不可用的。

### GC Roots

1. 虚拟机栈（栈帧中的本地变量表）中引用的对象。
2. 方法区中类静态属性引用的对象。
3. 方法区中常量引用的对象。
4. 本地方法栈中 JNI（即一般说的Native方法）引用的对象。

### 垃圾回收算法

1. 复制：先暂停程序的运行,然后将所有存活的对象从当前堆复制到另一个堆,没有被复制的对象全部都是垃圾。当对象被复制到新堆时,它们是一个挨着一个的,所以新堆保持紧凑排列,然后就可以按前述方法简单,直接的分配了。缺点是一浪费空间,两个堆之间要来回倒腾,二是当程序进入稳定态时,可能只会产生极少的垃圾,甚至不产生垃圾,尽管如此,复制式回收器仍会将所有内存自一处复制到另一处。
2. 标记-清除：同样是从堆栈和静态存储区出发,遍历所有的引用,进而找出所有存活的对象。每当它找到一个存活的对象,就会给对象一个标记,这个过程中不会回收任何对象。只有全部标记工作完成的时候,清理动作才会开始。在清理过程中,没有标记的对象会被释放,不会发生任何复制动作。所以剩下的堆空间是不连续的,垃圾回收器如果要希望得到连续空间的话,就得重新整理剩下的对象。
3. 标记-整理：它的第一个阶段与标记/清除算法是一模一样的，均是遍历GC Roots，然后将存活的对象标记。移动所有存活的对象，且按照内存地址次序依次排列，然后将末端内存地址以后的内存全部回收。因此，第二阶段才称为整理阶段。
4. 分代收集算法：把Java堆分为新生代和老年代，然后根据各个年代的特点采用最合适的收集算法。新生代中，对象的存活率比较低，所以选用复制算法，老年代中对象存活率高且没有额外空间对它进行分配担保，所以使用“标记-清除”或“标记-整理”算法进行回收。

### 分代回收

 1.部分垃圾回收器使用，除了epsilon,zgc,shenandoah之外都适用逻辑分代模型； G1逻辑分代，物理不分代，除此之外逻辑不分代，物理分代；

2. 年轻代 + 老年代 + 永久代1.7/元空间

HotSpot JVM把年轻代分为了三部分：1个Eden区和2个Survivor区（分别叫from和to）。一般情况下，新创建的对象都会被分配到Eden区(一些大对象特殊处理),这些对象经过第一次Minor GC后，如果仍然存活，将会被移到Survivor区。对象在Survivor区中每熬过一次Minor GC，年龄就会增加1岁，当它的年龄增加到一定程度时，就会被移动到年老代中。老年代满了会进行full gc

因为年轻代中的对象基本都是朝生夕死的，所以在年轻代的垃圾回收算法使用的是复制算法，复制算法的基本思想就是将内存分为两块，每次只用其中一块，当这一块内存用完，就将还活着的对象复制到另外一块上面。复制算法不会产生内存碎片。

在GC开始的时候，对象只会存在于Eden区和名为“From”的Survivor区，Survivor区“To”是空的。紧接着进行GC，Eden区中所有存活的对象都会被复制到“To”，而在“From”区中，仍存活的对象会根据他们的年龄值来决定去向。年龄达到一定值(年龄阈值，可以通过-XX:MaxTenuringThreshold来设置)的对象会被移动到年老代中，没有达到阈值的对象会被复制到“To”区域。经过这次GC后，Eden区和From区已经被清空。这个时候，“From”和“To”会交换他们的角色，也就是新的“To”就是上次GC前的“From”，新的“From”就是上次GC前的“To”。不管怎样，都会保证名为To的Survivor区域是空的。Minor GC会一直重复这样的过程，直到“To”区被填满，“To”区被填满之后，会将所有对象移动到年老代中。

### 动态年龄计算

Hotspot在遍历所有对象时，按照年龄从小到大对其所占用的大小进行累积，当累积的某个年龄大小超过了survivor区的一半时，取这个年龄和MaxTenuringThreshold中更小的一个值，作为新的晋升年龄阈值。

JVM引入动态年龄计算，主要基于如下两点考虑：

1. 如果固定按照MaxTenuringThreshold设定的阈值作为晋升条件： a）MaxTenuringThreshold设置的过大，原本应该晋升的对象一直停留在Survivor区，直到Survivor区溢出，一旦溢出发生，Eden+Svuvivor中对象将不再依据年龄全部提升到老年代，这样对象老化的机制就失效了。 b）MaxTenuringThreshold设置的过小，“过早晋升”即对象不能在新生代充分被回收，大量短期对象被晋升到老年代，老年代空间迅速增长，引起频繁的Major GC。分代回收失去了意义，严重影响GC性能。
2. 相同应用在不同时间的表现不同：特殊任务的执行或者流量成分的变化，都会导致对象的生命周期分布发生波动，那么固定的阈值设定，因为无法动态适应变化，会造成和上面相同的问题。

### 常见的垃圾收集器

Young: serial parnew parallel sacenge

Old: serial old ,cms ,parallel old

serial：a stop the world，copying collector which use a single gc thread

1.serial + serial old：停顿时间太长，基本不用了。

parallel scavenge: a STW,copying collector use multiple gc threads

2.Ps + po: jdk版本默认的，cms缺点太大

3.parnew+cms ：parnew和ps区别就是可以配合cms使用

---g1，zgc

### CMS的执行过程

Concurrent Mark and Sweep

简单步骤：

初始标记：会有stop the world，暂停所有其他线程。记下所有GC root 直接可达的对象， 速度很快

并发标记：基本不会stw。同时开启 用户线程 和GC线程，因为用户线程可能会不断的更新引用域，所以 GC线程无法保证可达性分析的实时性。所以这个算法里会跟踪记录这些发生引用更新的地方。

重新标记：会有stw，重新标记阶段就是为了修正并发标记期间因为用户程序继续运行产生的变动，这个阶段的停顿时间一般会比初始标记阶段的时间稍⻓，远远比 并发标记阶段时间短

并发清除：开启用户线程，同时GC线程开始对为标记的区域做清扫。

CMS 缺点：对CPU资源敏感，无法清理浮动垃圾，会有内存碎片（mark and sweep）

老年代碎片话太严重，promotionfailed，新的对象进入不了老年代了，cms会将

serial old拿出来，效率低下。

详细步骤：

1. 初始标记(STW initial mark)：这个过程从垃圾回收的"根对象"开始，只扫描到能够和"根对象"直接关联的对象，并作标记。所以这个过程虽然暂停了整个JVM，但是很快就完成了。
2. 并发标记(Concurrent marking)：这个阶段紧随初始标记阶段，在初始标记的基础上继续向下追溯标记。并发标记阶段，应用程序的线程和并发标记的线程并发执行，所以用户不会感受到停顿。
3. 并发预清理(Concurrent precleaning)：并发预清理阶段仍然是并发的。在这个阶段，虚拟机查找在执行并发标记阶段新进入老年代的对象(可能会有一些对象从新生代晋升到老年代， 或者有一些对象被分配到老年代)。通过重新扫描，减少下一个阶段"重新标记"的工作，因为下一个阶段会Stop The World。
4. 重新标记(STW remark)：这个阶段会暂停虚拟机，收集器线程扫描在CMS堆中剩余的对象。扫描从"根对象"开始向下追溯，并处理对象关联。
5. 并发清理(Concurrent sweeping)：清理垃圾对象，这个阶段收集器线程和应用程序线程并发执行。
6. 并发重置(Concurrent reset)：这个阶段，重置CMS收集器的数据结构状态，等待下一次垃圾回收。

### G1的执行过程

把堆分成了一个个的region，有eden space，survivor space，old space，G1从整体来看是基于“标记整理”算法实现的收集器;从局部上来看是基于“复制”算法实现的。

1. 标记阶段：首先是初始标记(Initial-Mark),这个阶段也是停顿的(stop-the-word)，并且会稍带触发一次yong GC。
2. 并发标记：这个过程在整个堆中进行，并且和应用程序并发运行。并发标记过程可能被yong GC中断。在并发标记阶段，如果发现区域对象中的所有对象都是垃圾，那个这个区域会被立即回收(图中打X)。同时，并发标记过程中，每个区域的对象活性(区域中存活对象的比例)被计算。
3. 再标记：这个阶段是用来补充收集并发标记阶段产新的新垃圾。与之不同的是，G1中采用了更快的算法:SATB。
4. 清理阶段：选择活性低的区域(同时考虑停顿时间)，等待下次yong GC一起收集，对应GC log: [GC pause (mixed)]，这个过程也会有停顿(STW)。
5. 回收/完成：新的yong GC清理被计算好的区域。但是有一些区域还是可能存在垃圾对象，可能是这些区域中对象活性较高，回收不划算，也肯能是为了迎合用户设置的时间，不得不舍弃一些区域的收集。

### G1和CMS的比较

1. CMS收集器是获取最短回收停顿时间为目标的收集器，因为CMS工作时，GC工作线程与用户线程可以并发执行，以此来达到降低停顿时间的目的（只有初始标记和重新标记会STW）。但是CMS收集器对CPU资源非常敏感。在并发阶段，虽然不会导致用户线程停顿，但是会占用CPU资源而导致引用程序变慢，总吞吐量下降。
2. CMS仅作用于老年代，是基于标记清除算法，所以清理的过程中会有大量的空间碎片。
3. CMS收集器无法处理浮动垃圾，由于CMS并发清理阶段用户线程还在运行，伴随程序的运行自热会有新的垃圾不断产生，这一部分垃圾出现在标记过程之后，CMS无法在本次收集中处理它们，只好留待下一次GC时将其清理掉。
4. G1是一款面向服务端应用的垃圾收集器，适用于多核处理器、大内存容量的服务端系统。G1能充分利用CPU、多核环境下的硬件优势，使用多个CPU（CPU或者CPU核心）来缩短STW的停顿时间，它满足短时间停顿的同时达到一个高的吞吐量。
5. 从JDK 9开始，G1成为默认的垃圾回收器。当应用有以下任何一种特性时非常适合用G1：Full GC持续时间太长或者太频繁；对象的创建速率和存活率变动很大；应用不希望停顿时间长(长于0.5s甚至1s)。
6. G1将空间划分成很多块（Region），然后他们各自进行回收。堆比较大的时候可以采用，采用复制算法，碎片化问题不严重。整体上看属于标记整理算法,局部(region之间)属于复制算法。
7. G1 需要记忆集来记录新生代和老年代之间的引用关系，这种数据结构在 G1 中需要占用大量的内存，可能达到整个堆内存容量的 20% 甚至更多。而且 G1 中维护记忆集的成本较高，带来了更高的执行负载，影响效率。所以 CMS 在小内存应用上的表现要优于 G1，而大内存应用上 G1 更有优势，大小内存的界限是6GB到8GB。（Card Table（CMS中）的结构是一个连续的byte[]数组，扫描Card Table的时间比扫描整个老年代的代价要小很多！G1也参照了这个思路，不过采用了一种新的数据结构 Remembered Set 简称Rset。RSet记录了其他Region中的对象引用本Region中对象的关系，属于points-into结构（谁引用了我的对象）。而Card Table则是一种points-out（我引用了谁的对象）的结构，每个Card 覆盖一定范围的Heap（一般为512Bytes）。G1的RSet是在Card Table的基础上实现的：每个Region会记录下别的Region有指向自己的指针，并标记这些指针分别在哪些Card的范围内。 这个RSet其实是一个Hash Table，Key是别的Region的起始地址，Value是一个集合，里面的元素是Card Table的Index。每个Region都有一个对应的Rset。）

### GC中Stop the world（STW）

在执行垃圾收集算法时，Java应用程序的其他所有除了垃圾收集收集器线程之外的线程都被挂起。此时，系统只能允许GC线程进行运行，其他线程则会全部暂停，等待GC线程执行完毕后才能再次运行。这些工作都是由虚拟机在后台自动发起和自动完成的，是在用户不可见的情况下把用户正常工作的线程全部停下来，这对于很多的应用程序，尤其是那些对于实时性要求很高的程序来说是难以接受的。

但不是说GC必须STW,你也可以选择降低运行速度但是可以并发执行的收集算法，这取决于你的业务。

### Minor GC和Full GC触发条件

* Minor GC触发条件：当Eden区满时，触发Minor GC。
* Full GC触发条件：
  1. 调用System.gc时，系统建议执行Full GC，但是不必然执行
  2. 老年代空间不足
  3. 方法区空间不足
  4. 通过Minor GC后进入老年代的平均大小大于老年代的可用内存
  5. 由Eden区、From Space区向To Space区复制时，对象大小大于To Space可用内存，则把该对象转存到老年代，且老年代的可用内存小于该对象大小

### 强引用 弱引用

**强引用**是使用最普遍的引用。如果一个对象具有强引用，那**垃圾回收器**绝不会回收它。当**内存空间不足**时，`Java`虚拟机宁愿抛出`OutOfMemoryError`错误，使程序**异常终止**，也不会靠随意**回收**具有**强引用**的**对象**来解决内存不足的问题。 
如果强引用对象**不使用时**，需要弱化从而使`GC`能够回收 strongReference = null;

arraylist.clear（）在调用`clear`方法清空数组时，每个数组元素被赋值为`null`

如果一个对象只具有**软引用**，则**内存空间充足**时，**垃圾回收器**就**不会**回收它；如果**内存空间不足**了，就会**回收**这些对象的内存。只要垃圾回收器没有回收它，该对象就可以被程序使用。

    // 强引用
    String strongReference = new String("abc");
    // 软引用
    String str = new String("abc");
    SoftReference<String> softReference = new SoftReference<String>(str);
当内存不足时，`JVM`首先将**软引用**中的**对象**引用置为`null`，然后通知**垃圾回收器**进行回收

**弱引用**与**软引用**的区别在于：只具有**弱引用**的对象拥有**更短暂**的**生命周期**。在垃圾回收器线程扫描它所管辖的内存区域的过程中，一旦发现了只具有**弱引用**的对象，不管当前**内存空间足够与否**，都会**回收**它的内存。不过，由于垃圾回收器是一个**优先级很低的线程**，因此**不一定**会**很快**发现那些只具有**弱引用**的对象。

如果一个对象**仅持有虚引用**，那么它就和**没有任何引用**一样，在任何时候都可能被垃圾回收器回收。**虚引用**主要用来**跟踪对象**被垃圾回收器**回收**的活动。 

# I/O+网络

### socket

操作系统提供socket套接字部件，网络数据传输使用的软件设备

server端接受连接请求的socket创建过程：

1.调用socket函数创建套接字

```
int socket(int domain, int type, int protocol); 成功返回套接字文件描述符，失败返回-1
//Domain 套接字的协议族，比如pf_inet ip v4, pf_inet6 ipv6互联网协议族
//type：套接字类型
1. 面向连接的套接字 sock_stream：传输过程中数据不会丢失；按序传输数据；
   传输的数据不存在数据边界boundary（100个糖果分批传递，但接收者凑齐了100后才装袋）
   收发数据的socket内部有缓冲buffer，通过socket传输的数据将保存在数组里面，read函数从缓存中读取部分数据，buffer不总是满的，但如果read读取的速度比接受数据的速度慢，buffer会满。如果满了，socket无法接受数据，停止传输。
2. 面向消息的套接字 sock_dgram：强调快速传输而非传输速度；传输的数据可能丢失也可能损毁；有数据边界；限制数据大小
//protocol：比如tcp
```

2.调用bind函数分配ip和端口号

3.调用listen函数转为可接受请求状态(-此时client才可以调用connect)

```
# include <sys/socket.h>
int listen(int sock, int backlog) //成功返回0，失败返回-1
sock 希望进入等待请求状态的套接字文件描述符，监听套接字
backlog 连接请求等待队列queue的长度，比如5表是最多有5个连接请求进入队列
```

4.调用accept函数受理连接请求

```
int accept(int sock, struc sockaddr * addr, socklen_t * addrlen);
成功返回创建的套接字文件描述符
```

![截屏2022-01-04 下午8.52.39](/Users/jialinzhang/Library/Application Support/typora-user-images/截屏2022-01-04 下午8.52.39.png)、

5.read()/write()交换数据

6.close

client端发送请求的socket创建过程：

1.调用socket函数创建套接字

2.调用connect函数

```
int connect(int sock, struct serveraddr) // sock客户端clinet的套接字文件描述符
//server adder 服务端的地址
```

客户端调用connect函数后，服务端接收连接请求（服务端只是把连接请求信息放在等待队列里）

客户端在调用connect函数时候自动分配ip和端后号（随机），内核中发生。无需要bind

3.read()/write()交换数据

4.close（）断开连接

tcp内部工作原理是

1.与对方的套接字进行连接

2.与对方的主机数据交换

### 基于linux文件操作

一切都是文件，将socket也看作文件。所以socket操作和文件操作没有区别，因此在网络数据传输过程中，会使用文件io相关函数。

文件描述符 file descriptor：文件/套接字创建过程自动分配，一个整数。0，1，2分配给了标准的io

-打开文件 int open(const path, int flag) 成功返回一个文件描述符

-关闭文件 int close（int fd) 失败返回-1，成功返回0

-将数据写入文件 ssize_t write(int fdm, const buf,  size_t nbytes)

-读取文件中的数据 ssize_t read(int fd, void * buf, size_t nbytes)

### ip地址/port

端口号port：由16位组成，0-1023是知名端口号，分配给特定的应用程序，两个tcp socket不可以共用，tcp socket 和 udp socket可以共用端口号

**ipv4 vs ipv6**

1.扩展了路由和寻址的能力，IPv6把IP地址由32位增加到128位，从而能够支持更大的地址空间

2.报头格式的简化，IPv 4报头格式中一些冗余的域或被丢弃或被列为扩展报头，从而降低了包处理和报头带宽的开销。虽然IPv6的地址是IPv4地址的4倍。但报头只有它的2倍大

3.在IPv6中加入了关于身份验证、数据一致性和保密性的内容。

4.IPv6的可选项不放入报头，而是放在一个个独立的扩展头部。如果不指定路由器不会打开处理扩展头部.这大大改变了路由性能

### ip网络层

**ip协议无法应对数据错误**：Ip面向消息的，不可靠的协议。每次传输数据时会帮我们选择路径，但不一致，如果传输中发生路径错误、则选择其他路径；但如果发生数据丢失或错误，则无法解决。

**网络层：**将数据传输到目标地址；目标地址可以使多个网络通过路由器连接而成的某一个地址，主要负责寻找地址和路由选择，网络层还可以实现拥塞控制、网际互连等功能

在这一层，数据的单位称为数据包（packet）

MAC地址由制造商制造的网卡，通过识别制造商号，制造商内部产品编号以及产品通用编号来确保MAC地址的唯一性

IP地址由网络号和主机号2部分组成，即通信主体IP地址不同，若主机号不同，网络号相同，说明其处于同一个网段

**传输速率：**数据传输过程中，两个设备之间数据流动的物理速度称为传输速率，单位为bps（Bits Per Second，每秒比特数），即单位时间内传输的数据量多少

​       传输速率又称为带宽，带宽越大网络传输能力就越强

**吞吐量：**主机之间实际的传输速率称为吞吐量，单位为bps

​      吞吐量不仅衡量带宽，同时还有主机的CPU处理能力、网络拥堵程度、报文中数据字段的占有份额（不含报文首部，只计算数据字段本身）等信息

这一层的网络设备：路由器/3层 4到7层的交换机

### TCP

tcp vs ip

ip只关注一个包，每个数据包也是由ip实际传输的，但传输顺序和传输本身不可靠。

tcp利用ip传输，可以确保对方收到数据，重传丢失的数据，可靠的

-----------------------------------------**TCP**----------------------------------------------------------------------------------------------------

- TCP 提供一种**面向连接的、可靠的**字节流服务
- 在一个 TCP 连接中，仅有两方进行彼此通信。广播和多播不能用于 TCP
- TCP 使用校验和，确认和重传机制来保证可靠传输
- TCP 给数据分节进行排序，并使用累积确认保证数据的顺序不变和非重复
- TCP 使用滑动窗口机制来实现流量控制，通过动态改变窗口的大小进行拥塞控制

**注意**：TCP 并不能保证数据一定会被对方接收到，因为这是不可能的。TCP 能够做到的是，如果有可能，就把数据递送到接收方，否则就（通过放弃重传并且中断连接这一手段）通知用户。因此准确说 TCP 也不是 100% 可靠的协议，它所能提供的是数据的可靠递送或故障的可靠通知

#### 三次握手

所谓三次握手(Three-way Handshake)，是指建立一个 TCP 连接时，需要客户端和服务器总共发送3个包。

三次握手的目的是连接服务器指定端口，建立 TCP 连接，并同步连接双方的序列号和确认号，交换 TCP 窗口大小信息。在 socket 编程中，客户端执行 `connect()` 时。将触发三次握手。

- 第一次握手(SYN=1, seq=x):

  客户端发送一个 TCP 的 SYN 标志位置1的包，指明客户端打算连接的服务器的端口，以及初始序号 X,保存在包头的序列号(Sequence Number)字段里。

  发送完毕后，客户端进入 `SYN_SEND` 状态。

- 第二次握手(SYN=1, ACK=1, seq=y, ACKnum=x+1):

  服务器发回确认包(ACK)应答。即 SYN 标志位和 ACK 标志位均为1。服务器端选择自己 ISN 序列号，放到 Seq 域里，同时将确认序号(Acknowledgement Number)设置为客户的 ISN 加1，即X+1。 发送完毕后，服务器端进入 `SYN_RCVD` 状态。

- 第三次握手(ACK=1，ACKnum=y+1)

  客户端再次发送确认包(ACK)，SYN 标志位为0，ACK 标志位为1，并且把服务器发来 ACK 的序号字段+1，放在确定字段中发送给对方，并且在数据段放写ISN的+1

  发送完毕后，客户端进入 `ESTABLISHED` 状态，当服务器端接收到这个包时，也进入 `ESTABLISHED` 状态，TCP 握手结束。

#### 四次挥手

TCP 的连接的拆除需要发送四个包，因此称为四次挥手(Four-way handshake)，也叫做改进的三次握手。客户端或服务器均可主动发起挥手动作，在 socket 编程中，任何一方执行 `close()` 操作即可产生挥手操作。

- 第一次挥手(FIN=1，seq=x)

  假设客户端想要关闭连接，客户端发送一个 FIN 标志位置为1的包，表示自己已经没有数据可以发送了，但是仍然可以接受数据。

  发送完毕后，客户端进入 `FIN_WAIT_1` 状态。

- 第二次挥手(ACK=1，ACKnum=x+1)

  服务器端确认客户端的 FIN 包，发送一个确认包，表明自己接受到了客户端关闭连接的请求，但还没有准备好关闭连接。

  发送完毕后，服务器端进入 `CLOSE_WAIT` 状态，客户端接收到这个确认包之后，进入 `FIN_WAIT_2` 状态，等待服务器端关闭连接。

- 第三次挥手(FIN=1，seq=y)

  服务器端准备好关闭连接时，向客户端发送结束连接请求，FIN 置为1。

  发送完毕后，服务器端进入 `LAST_ACK` 状态，等待来自客户端的最后一个ACK。

- 第四次挥手(ACK=1，ACKnum=y+1)

  客户端接收到来自服务器端的关闭请求，发送一个确认包，并进入 `TIME_WAIT`状态，等待可能出现的要求重传的 ACK 包。

  服务器端接收到这个确认包之后，关闭连接，进入 `CLOSED` 状态。

  客户端等待了某个固定时间（两个最大段生命周期，2MSL，2 Maximum Segment Lifetime）之后，没有收到服务器端的 ACK ，认为服务器端已经正常关闭连接，于是自己也关闭连接，进入 `CLOSED` 状态。

  ![截屏2022-01-04 下午8.15.26](/Users/jialinzhang/Library/Application Support/typora-user-images/截屏2022-01-04 下午8.15.26.png)

#### why 四次？

因为当Server端收到Client端的SYN连接请求报文后，可以直接发送SYN+ACK报文。其中ACK报文是用来应答的，SYN报文是用来同步的。但是关闭连接时，**当Server端收到FIN报文时，很可能并不会立即关闭SOCKET，所以只能先回复一个ACK报文**，告诉Client端，"你发的FIN报文我收到了"。只有等到我Server端所有的报文都发送完了，我才能发送FIN报文，因此不能一起发送。故需要四步握手

#### 为什么要有TIME_WAIT?

1、 网络情况不好时，如果主动方无TIME_WAIT等待，关闭前一个连接后，主动方与被动方又建立起新的TCP连接，这时被动方重传或延时过来的FIN包过来后会直接影响新的TCP连接；（因为有可能最后一个ACK没收到，被动方重新发送了FIN）

2、 同样网络情况不好并且无TIME_WAIT等待，关闭连接后无新连接，当主动方接收到被动方重传或延迟的FIN包后，主动方会给被动方回一个RST包，可能会影响被动方其它的服务连接。

why 2 * msl ？

为了可靠安全的关闭TCP连接。比如网络拥塞，主动方最后一个ACK被动方没收到，这时被动方会对FIN开启TCP重传，发送多个FIN包，在这时，尚未关闭的TIME_WAIT就会把这些尾巴问题处理掉，不至于对新连接及其它服务产生影响。

#### TCP KeepAlive

TCP KeepAlive 的基本原理是，隔一段时间给连接对端发送一个探测包，如果收到对方回应的 ACK，则认为连接还是存活的，在超过一定重试次数之后还是没有收到对方的回应，则丢弃该 TCP 连接。

例如当一个服务器 CPU 进程服务器占用达到 100%，已经卡死不能响应请求了，此时 TCP KeepAlive 依然会认为连接是存活的。因此 TCP KeepAlive 对于应用层程序的价值是相对较小的。需要做连接保活的应用层程序，例如 QQ，往往会在应用层实现自己的心跳功能。

#### 超时与重传

**超时重传**是**TCP**协议保证数据可靠性的另一个重要机制，其原理是在发送某一个数据以后就开启一个计时器，在一定时间内如果没有得到发送的数据报的ACK报文，那么就重新发送数据，直到发送成功为止。

#### TCP流量控制

利用滑动窗口实现流量控制：让发送方的发送速率不要太快，要让接收方来得及接收
设A向B发送数据。在连接建立时，B告诉了A：“我的接收窗口是 rwnd = 400 ”(这里的 rwnd 表示 receiver window) 。因此，发送方的发送窗口不能超过接收方给出的接收窗口的数值。请注意，TCP的窗口单位是字节，不是报文段。

### UDP

UDP 是一个简单的传输层协议。和 TCP 相比，UDP 有下面几个显著特性：

- UDP 缺乏可靠性。UDP 本身不提供确认，序列号，超时重传等机制。UDP 数据报可能在网络中被复制，被重新排序。即 UDP 不保证数据报会到达其最终目的地，也不保证各个数据报的先后顺序，也不保证每个数据报只到达一次
- UDP 数据报是有长度的。每个 UDP 数据报都有长度，如果一个数据报正确地到达目的地，那么该数据报的长度将随数据一起传递给接收方。而 TCP 是一个字节流协议，没有任何（协议上的）记录边界。
- UDP 是无连接的。UDP 客户和服务器之前不必存在长期的关系。UDP 发送数据报之前也不需要经过握手创建连接的过程。
- UDP 支持多播和广播。

### 应用层

选择数据传输路径、数据确认过程都被隐藏在套接字内部。程序员在进行网络编程可以从这些细节解放出来，要根据程序的特性来决定服务端和客户端之间数据传输的规则（规定）、也就是应用层协议。设计和实现应用层协议。

### 并发服务端

使其同时向所有发起请求的客户端提供服务，提高平均满意度；

网络通信时间大于cpu的运算时间，向多个客户端提供服务也有效利用cpu；

**方式一：多进程服务器，创建多个进程**

缺点：创建进程需要付出代价的，进程之间要有独立的内存空间，互相之间的数据交换也要采用很复杂的方法

**方式二：多路复用服务器**：捆绑并统一管理io对象提供服务

多路复用机制： 无论多少个客户端，提供服务的进程只有一个，所以该进程需要确认收到数据的套接字，并通过该套接字解说数据。linux提供了三种方式 Select，poll，epoll

I/O多路复用就通过一种机制，可以监视多个描述符，一旦某个描述符就绪（一般是读就绪或者写就绪），能够通知程序进行相应的读写操作

将多个文件描述符集中到一起统一监视：（事件 event）

-是否存在socket接受数据？

-无需阻塞传输数据的套接字有哪些？

-哪些套接字发生了异常？

**方式三：多线程服务器**（通过生成与客户端等量的线程提供服务）

#### select系统调用

**使用步骤**

步骤一：设置文件描述符，指定监控范围，设置超时

步骤二：调用select函数

步骤三：查看select调用结果

select函数只有在超时/监视的文件描述符发生变化时才返回。如果没有发生变化，就进入阻塞状态。

```c
int select(int nfds, fd_set *readfds, fd_set *writefds, fd_set *exceptfds, struct timeval *timeout);
//readfds set are watched to see if data is available for reading
//writefds set are watched to see if a write operation will complete without blocking.
//exceptfds set are watched to see if an exception has occurred, or if out-of-band data is available (these states apply only to sockets).
```

**select的几大缺点：**

（1）每次调用select，都需要把fd集合从用户态拷贝到内核态，这个开销在fd很多时会很大

（2）同时每次调用select都需要在内核遍历传递进来的所有fd，这个开销在fd很多时也很大

#### poll 

poll的实现和select非常相似，只是描述fd集合的方式不同，poll使用pollfd结构而不是select的fd_set结构，其他的都差不多

```c
int poll (struct pollfd *fds, unsigned int nfds, int timeout);

```

#### epoll

epoll_create() 创建epoll文件描述符空间

epoll_ctl() 向空间注册并注销文件描述符

```
epoll_ctl（a, epoll_add, b, cevent) //向epolll历程a中注册文件描述符b主要监听cevent描述的事件
```

epoll_wait() 与select类似，等待文件描述符发生变化

```
int epoll_wait(int epfd, struct events, int maxevents, int timeout) //成功返回发生事件的文件描述符，失败返回-1
epfd表示发生监视范围的epoll例程的文件描述符
events保存发生事件的文件描述符集合的结构题地址
```

调用函数后，返回发生事件的文件描述符，同时在第二个参数指向的缓冲中保存发生事件的文件描述符，因此，无需像select那样针对所有文件描述符的循环。

优点：

1.对于第一个缺点，epoll的解决方案在epoll_ctl函数中。每次注册新的事件到epoll句柄中时（在epoll_ctl中指定EPOLL_CTL_ADD），会把所有的fd拷贝进内核，而不是在epoll_wait的时候重复拷贝。epoll保证了每个fd在整个过程中只会拷贝一次

2.对于第二个缺点，epoll的解决方案不像select或poll一样每次都把current轮流加入fd对应的设备等待队列中，而只在epoll_ctl时把current挂一遍（这一遍必不可少）并为每个fd指定一个回调函数，当设备就绪，唤醒等待队列上的等待者时，就会调用这个回调函数，而这个回调函数会把就绪的fd加入一个就绪链表）。epoll_wait的工作实际上就是在这个就绪链表中查看有没有就绪的fd（利用schedule_timeout()实现睡一会，判断一会的效果，和select实现中的第7步是类似的）

#### 区别

（1）select，poll实现需要自己不断轮询所有fd集合，直到设备就绪，期间可能要睡眠和唤醒多次交替。而epoll其实也需要调用epoll_wait不断轮询就绪链表，期间也可能多次睡眠和唤醒交替，但是它是设备就绪时，调用回调函数，把就绪fd放入就绪链表中，并唤醒在epoll_wait中进入睡眠的进程。虽然都要睡眠和交替，但是select和poll在“醒着”的时候要遍历整个fd集合，而epoll在“醒着”的时候只要判断一下就绪链表是否为空就行了，这节省了大量的CPU时间。这就是回调机制带来的性能提升。

（2）select，poll每次调用都要把fd集合从用户态往内核态拷贝一次，并且要把current往设备等待队列中挂一次，而epoll只要一次拷贝，而且把current往等待队列上挂也只挂一次（在epoll_wait的开始，注意这里的等待队列并不是设备等待队列，只是一个epoll内部定义的等待队列）。这也能节省不少的开销

#### 5种io模型

Io device---------kernel buffer---- copy----process

所以，对于一个网络输入操作通常包括两个不同阶段：

- 等待网络数据到达网卡→读取到内核缓冲区，数据准备好；
- 从内核缓冲区复制数据到进程空间。

**第一种：阻塞io**

进程发起IO系统调用后，进程被阻塞，转到内核空间处理，整个IO处理完毕后返回进程。操作成功则进程获取到数据。

1、典型应用：阻塞socket、Java BIO；

2、特点：

- 进程阻塞挂起不消耗CPU资源，及时响应每个操作；
- 实现难度低、开发应用较容易；
- 适用并发量小的网络应用开发；

不适用并发量大的应用：因为一个请求IO会阻塞进程，所以，得为每请求分配一个处理进程（线程）以及时响应，系统开销大。

**第二种：非阻塞io**

进程发起IO系统调用后，如果内核缓冲区没有数据，需要到IO设备中读取，进程返回一个错误而不会被阻塞；进程发起IO系统调用后，如果内核缓冲区有数据，内核就会把数据返回进程。

1、典型应用：socket是非阻塞的方式（设置为NONBLOCK）

2、特点：

- 进程轮询（重复）调用，消耗CPU的资源；
- 实现难度低、开发应用相对阻塞IO模式较难；
- 适用并发量较小、且不需要及时响应的网络应用开发；

第三种：**IO复用模型**

多个的进程的IO可以注册到一个复用器上，然后用一个进程调用该select， select会监听所有注册进来的IO；

如果select没有监听的IO在内核缓冲区都没有可读数据，select调用进程会被阻塞；而当任一IO在内核缓冲区中有可数据时，select调用就会返回；

而后select调用进程可以自己或通知另外的进程（注册进程）来再次发起读取IO，读取内核中准备好的数据。

1、典型应用：select、poll、epoll三种方案，nginx都可以选择使用这三个方案;Java NIO;

2、特点：

- 专一进程解决多个进程IO的阻塞问题，性能好；Reactor模式;
- 实现、开发应用难度较大；
- 适用高并发服务应用开发：一个进程（线程）响应多个请求；

**第四种：信号驱动IO模型**

当进程发起一个IO操作，会向内核注册一个信号处理函数，然后进程返回不阻塞；当内核数据就绪时会发送一个信号给进程，进程便在信号处理函数中调用IO读取数据。

特点：回调机制，实现、开发应用难度大

**第五种：异步IO模型**

当进程发起一个IO操作，进程返回（不阻塞），但也不能返回果结；内核把整个IO处理完后，会通知进程结果。如果IO操作成功则进程直接获取到数据。

**同步I/O，因为他们都需要在读写事件就绪后自己负责进行读写，也就是说这个读写过程是阻塞的，而异步I/O则无需自己负责进行读写，异步I/O的实现会负责把数据从内核拷贝到用户空间。**

1、典型应用：JAVA7 AIO、高性能服务器应用

2、特点：

- 不阻塞，数据一步到位；Proactor模式；
- 需要操作系统的底层支持，LINUX 2.5 版本内核首现，2.6 版本产品的内核标准特性；
- 实现、开发应用难度大；
- 非常适合高性能高并发应用；

阻塞IO模型、非阻塞IO模型、IO复用模型、信号驱动的IO模型者为同步IO模型，只有异步IO模型是异步IO

### http

- HTTP 协议构建于 TCP/IP 协议之上，是一个应用层协议，默认端口号是 80
- HTTP 是**无连接无状态**的

**事件顺序**    

  (1) 浏览器获取输入的域名"www.baidu.com"

（2.1）向本地的 etc/hosts 文件查看是否定义了域名对应的IP地址

  (2.2) 浏览器向DNS请求解析www.baidu.com的IP地址 

  (3) 域名系统DNS解析出百度服务器的IP地址 

  (4) 浏览器与该服务器建立TCP连接(默认端口号80) 

  (5) 浏览器发出HTTP请求，请求百度首页 

  (6) 服务器通过HTTP响应把首页文件发送给浏览器 

  (7) TCP连接释放 （http 1.1是长链接，不一定放开）

  (8) 浏览器将首页文件进行解析，并将Web页显示给用户。

**请求报文**

```
<method> <request-URL> <version> 
//GET，POST，PUT，DELETE就对应着对这个资源的查，增，改，删4个操作
//URL全称是资源描述符，我们可以这样认为：一个URL地址，它用于描述一个网络上的资源
<headers>
//服务端通常是根据请求头（headers）中的 Content-Type 字段来获知请求中的消息主体是用何种方式编码，再对主体进行解析
<entity-body>
```

相应报文

状态行、响应头(Response Header)、响应正文

`200 OK` 客户端请求成功

`301 Moved Permanently` 请求永久重定向

`302 Moved Temporarily` 请求临时重定向

`304 Not Modified` 文件未修改，可以直接使用缓存的文件。

`400 Bad Request` 由于客户端请求有语法错误，不能被服务器所理解。`401 Unauthorized` 请求未经授权。这个状态代码必须和WWW-Authenticate报头域一起使用

`403 Forbidden` 服务器收到请求，但是拒绝提供服务。服务器通常会在响应正文中给出不提供服务的原因

`404 Not Found` 请求的资源不存在，例如，输入了错误的URL

`500 Internal Server Error` 服务器发生不可预期的错误，导致无法完成客户端的请求。

`503 Service Unavailable` 服务器当前不能够处理客户端的请求，在一段时间之后，服务器可能会恢复正常。

#### 持久连接

我们知道 HTTP 协议采用“请求-应答”模式，当使用普通模式，即非 Keep-Alive 模式时，每个请求/应答客户和服务器都要新建一个连接，完成之后立即断开连接（HTTP 协议为无连接的协议）；当使用 Keep-Alive 模式（又称持久连接、连接重用）时，Keep-Alive 功能使客户端到服务器端的连接持续有效，当出现对服务器的后继请求时，Keep-Alive 功能避免了建立或者重新建立连接。

 HTTP 1.0协议上，如果客户端浏览器支持 Keep-Alive ，那么就在HTTP请求头中添加一个字段 Connection: Keep-Alive，当服务器收到附带有 Connection: Keep-Alive 的请求时，它也会在响应头中添加一个同样的字段来使用 Keep-Alive

在 HTTP 1.1 版本中，默认情况下所有连接都被保持，如果加入 "Connection: close" 才关闭

HTTP 长连接不可能一直保持，例如 `Keep-Alive: timeout=5, max=100`，表示这个TCP通道可以保持5秒，max=100，表示这个长连接最多接收100次请求就断开

#### 会话跟踪

客户端打开与服务器的连接发出请求到服务器响应客户端请求的全过程称之为会话。会话跟踪指的是对同一个用户对服务器的连续的请求和接受响应的监视。

Cookie： 是Web 服务器发送给客户端的一小段信息，客户端请求时可以读取该信息发送到服务器端，进而进行用户的识别。对于客户端的每次请求，服务器都会将 Cookie 发送到客户端,在客户端可以进行保存,以便下次使用。

客户端可以采用两种方式来保存这个 Cookie 对象，一种方式是保存在客户端内存中，称为临时 Cookie，浏览器关闭后这个 Cookie 对象将消失。另外一种方式是保存在客户机的磁盘上，称为永久 Cookie。以后客户端只要访问该网站，就会将这个 Cookie 再次发送到服务器上，前提是这个 Cookie 在有效期内，这样就实现了对客户的跟踪。

Cookie 是可以被客户端禁用的。

每一个用户都有一个不同的 session，各个用户之间是不能共享的，是每个用户所独享的，在 session 中可以存放信息。

在服务器端会创建一个 session 对象，产生一个 sessionID 来标识这个 session 对象，然后将这个 sessionID 放入到 Cookie 中发送到客户端，下一次访问时，sessionID 会发送到服务器，在服务器端进行识别不同的用户。

Session 的实现依赖于 Cookie，如果 Cookie 被禁用，那么 session 也将失效。

#### 跨域问题

cSRF（Cross-site request forgery，跨站请求伪造） `http://example.com/bbs/create_post.php?title=我是脑残&content=哈哈`

- 关键操作只接受 POST 请求
- 验证码
- Token 抵御 CSRF 攻击。主流

CSRF 攻击要成功的条件在于攻击者能够预测所有的参数从而构造出合法的请求。所以根据不可预测性原则，我们可以对参数进行加密从而防止 CSRF 攻击。

另一个更通用的做法是保持原有参数不变，另外添加一个参数 Token，其值是随机的。这样攻击者因为不知道 Token 而无法构造出合法的请求进行攻击。

Token 使用原则

- Token 要足够随机————只有这样才算不可预测
- Token 是一次性的，即每次请求成功后要更新Token————这样可以增加攻击难度，增加预测难度
- Token 要注意保密性————敏感操作使用 post，防止 Token 出现在 URL 中

### https

HTTPS 即 HTTP over TLS，是一种在加密信道进行 HTTP 内容传输的协议

TLS 握手：（transport layer security）

- 客户端发送一个 `ClientHello` 消息到服务器端，消息中同时包含了它的 Transport Layer Security (TLS) 版本，可用的加密算法和压缩算法。
- 服务器端向客户端返回一个 `ServerHello` 消息，消息中包含了服务器端的TLS版本，服务器所选择的加密和压缩算法，以及数字证书认证机构（Certificate Authority，缩写 CA）签发的服务器公开证书，证书中包含了公钥。客户端会使用这个公钥加密接下来的握手过程，直到协商生成一个新的对称密钥
- 客户端根据自己的信任CA列表，验证服务器端的证书是否可信。如果认为可信，客户端会生成一串伪随机数，使用服务器的公钥加密它。这串随机数会被用于生成新的对称密钥
- 服务器端使用自己的私钥解密上面提到的随机数，然后使用这串随机数生成自己的对称主密钥
- 客户端发送一个 `Finished` 消息给服务器端，使用对称密钥加密这次通讯的一个散列值
- 服务器端生成自己的 hash 值，然后解密客户端发送来的信息，检查这两个值是否对应。如果对应，就向客户端发送一个 `Finished` 消息，也使用协商好的对称密钥加密
- 从现在开始，接下来整个 TLS 会话都使用对称秘钥进行加密，传输应用层（HTTP)内容

![截屏2022-01-05 下午5.18.21](/Users/jialinzhang/Library/Application Support/typora-user-images/截屏2022-01-05 下午5.18.21.png)

如果这个过程中拿到了server的private key，就可以解开拿到对称的钥匙。危险

diffien hellman算法：client不是直接提供这个key而是

这个机制的巧妙在于需要安全通信的双方可以用这个方法确定对称密钥。然后可以用这个密钥进行加密和解密。但是注意，这个密钥交换协议/算法只能用于密钥的交换，而不能进行消息的加密和解密。双方确定要用的密钥后，要使用其他对称密钥操作加密算法实现加密和解密消息。

![截屏2022-01-05 下午5.34.44](/Users/jialinzhang/Library/Application Support/typora-user-images/截屏2022-01-05 下午5.34.44.png)

### ouauth2.0



### restful

一种设计风格，特点：结构清晰、符合标准、易于理解、扩展方便。

每列分别对应，（请求类型：请求地址：功能描述）

1. HTTP 动词

```
GET：   读取（Read）
POST：  新建（Create）
PUT：   更新（Update）
PATCH： 更新（Update），通常是部分更新
DELETE：删除（Delete）
```

2. URL（宾语）必须是名词

```
/getAllCars
/createNewCar
/deleteAllRedCars 是错误的
```

### 零拷贝

传统读：

1.JVM向OS发出read()系统调用，触发上下文切换，从用户态切换到内核态。

2.从外部存储（如硬盘）读取文件内容，通过直接内存访问（DMA）存入内核地址空间的缓冲区。

3.将数据从内核缓冲区拷贝到用户空间缓冲区，read()系统调用返回，并从内核态切换回用户态。

写：

1.JVM向OS发出write()系统调用，触发上下文切换，从用户态切换到内核态。

2.将数据从用户缓冲区拷贝到内核中与目的地Socket关联的缓冲区。

3.数据最终经由Socket通过DMA传送到硬件（如网卡）缓冲区，write()系统调用返回，并从内核态切换回用户态

我们都知道，上下文切换是CPU密集型的工作，数据拷贝是I/O密集型的工作。如果一次简单的传输就要像上面这样复杂的话，效率是相当低下的。零拷贝机制的终极目标，就是消除冗余的上下文切换和数据拷贝，提高效率。

大多数Unix-like系统都是提供了一个名为sendfile()的系统调用

sendfile() copies data between one file descriptor and another.
Because this copying is done within the kernel, sendfile() is more efficient than the combination of read(2) and write(2), which would require transferring data to and from user space.

FileChannel类是抽象类，transferTo()也是一个抽象方法，因此还要依赖于具体实现。FileChannel的实现类并不在JDK本身，而位于sun.nio.ch.FileChannelImpl类中，零拷贝的具体实现自然也都是native方法

零拷贝在很多框架中得到了广泛应用，一般都以Netty、Kafka、Spark

# 多线程

### 线程安全的单例模式

```
public class Singleton {
    private static volatile Singelton instance = null;
    private Singleton() {}
    private static Singleton getInstance() {
        if (instance == null) {
            synchronized(Singleton.class) {
                if (instance = null) {
                    instance = new Singelton();
                }
            }
        }
        return instance;
    }
}
```

### 线程池

为什么使用：

1.可以提高性能，因为创建一个线程会需要和os交互，如果程序中有大量的生存期很短的线程

2.有效控制系统并发线程的数量，当系统大量的并发线程时，会导致系统的性能下降，甚至jvm崩溃。线程池的最大线程数可以控制并发线程数不会超过次数。

自定义的线程池ThreadPoolExecutor：

1 corePoolSize //int 核心线程池大小

 2 maximumPoolSize //int 最大线程池大小 

3 keepAliveTime// long 线程最大空闲时间 

4 unit //TimeUnit 时间单位 

5 workQueue //BlockingQueue<Runnable> 线程等待队列 

6 threadFactory //ThreadFactory 线程创建工厂 

7 handler //RejectedExecutionHandler 拒绝策略

1. 首先检测线程池运行状态，如果不是RUNNING，则直接拒绝，线程池要保证在RUNNING的状态下执行任务。
2. 如果workerCount < corePoolSize，则创建并启动一个线程来执行新提交的任务。
3. 如果workerCount >= corePoolSize，且线程池内的阻塞队列未满，则将任务添加到该阻塞队列中。
4. 如果workerCount >= corePoolSize && workerCount < maximumPoolSize，且线程池内的阻塞队列已满，则创建并启动一个线程来执行新提交的任务。
5. 如果workerCount >= maximumPoolSize，并且线程池内的阻塞队列已满, 则根据拒绝策略来处理该任务, 默认的处理方式是直接抛异常

Java预定义线程池：

1. **FixedThreadPool**：

   corePoolSize与maximumPoolSize相等，即其线程全为核心线程，是一个固定大小的线程池，是其优势；

   keepAliveTime = 0 该参数默认对核心线程无效，而FixedThreadPool全部为核心线程；

   workQueue 为LinkedBlockingQueue（无界阻塞队列），队列最大值为Integer.MAX_VALUE。如果任务提交速度持续大余任务处理速度，会造成队列大量阻塞。因为队列很大，很有可能在拒绝策略前，内存溢出。是其劣势；

   FixedThreadPool的任务执行是无序的；

   适用场景：可用于Web服务瞬时削峰，但需注意长时间持续高峰情况造成的队列阻塞。

2. **CachedThreadPool**：

   corePoolSize = 0，maximumPoolSize = Integer.MAX_VALUE，即线程数量几乎无限制；

   keepAliveTime = 60s，线程空闲60s后自动结束。

   workQueue 为 SynchronousQueue 同步队列，这个队列类似于一个接力棒，入队出队必须同时传递，因为CachedThreadPool线程创建无限制，不会有队列等待，所以使用SynchronousQueue；

   适用场景：快速处理大量耗时较短的任务，如Netty的NIO接受请求时，可使用CachedThreadPool。

3. **SingleThreadExecutor**：newFixedThreadPool(1)多了一层FinalizableDelegatedExecutorService包装

   无法成功向下转型。因此，SingleThreadExecutor被定以后，无法修改，做到了真正的Single。

4. CachedThreadPool: 创建一个可缓存线程池，如果线程池长度超过处理需要，可灵活回收空闲线程，若无可回收，则新建线程。CachedThreadPool是大小无界的线程池，适用于执行很多的短期异步任务的小程序，或者是负载较轻的服务器。

#### 线程池的拒绝策略

1. ThreadPoolExecutor.AbortPolicy:丢弃任务并抛出RejectedExecutionException异常。
2. ThreadPoolExecutor.DiscardPolicy：丢弃任务，但是不抛出异常。
3. ThreadPoolExecutor.DiscardOldestPolicy：丢弃队列最前面的任务，然后重新提交被拒绝的任务
4. ThreadPoolExecutor.CallerRunsPolicy：由提交任务的线程，处理该任务

#### 线程池的线程数量怎么确定

1. 一般来说，如果是CPU密集型应用，则线程池大小设置为N+1。
2. 一般来说，如果是IO密集型应用，则线程池大小设置为2N+1。
3. 在IO优化中，线程等待时间所占比例越高，需要越多线程，线程CPU时间所占比例越高，需要越少线程。这样的估算公式可能更适合：最佳线程数目 = （（线程等待时间+线程CPU时间）/线程CPU时间 ）* CPU数目

而且从安全考虑，也不希望cpu利用到百分比，百分之80就行了。实际中，压测，找到一个合适的数。

提前推算肯定不准确，要通过工具来测试。***<u>Profiler</u>***

#### 线程池都有哪几种工作队列

1. ArrayBlockingQueue：底层是数组，有界队列，如果我们要使用生产者-消费者模式，这是非常好的选择。
2. LinkedBlockingQueue：底层是链表，可以当做无界和有界队列来使用，所以大家不要以为它就是无界队列。
3. SynchronousQueue：本身不带有空间来存储任何元素，使用上可以选择公平模式和非公平模式。
4. PriorityBlockingQueue：无界队列，基于数组，数据结构为二叉堆，数组第一个也是树的根节点总是最小值。

举例 ArrayBlockingQueue 实现并发同步的原理：原理就是读操作和写操作都需要获取到 AQS 独占锁才能进行操作。如果队列为空，这个时候读操作的线程进入到读线程队列排队，等待写线程写入新的元素，然后唤醒读线程队列的第一个等待线程。如果队列已满，这个时候写操作的线程进入到写线程队列排队，等待读线程将队列元素移除腾出空间，然后唤醒写线程队列的第一个等待线程

### 进程线程纤程

进程：操作系统进行资源分配的基本单位

线程：执行调度的基本单位

纤程：用户空间的线程

### 线程切换

操作系统把一个线程的指令地址和寄存器的内容放在缓存里面，再把另一个线程相关的指令地址和寄存器放进来，cup就会执行（cpu傻傻的只会执行）。

### 单核cpu多线程优势

有意义。有一些线程，等待数据或者sleep的时候不需要cpu，别的线程可以利用cpu。

cpu密集型：大量时间cpu处理

io密集型：大量时间等待数据

大部分线程都是既有cpu既有io



### 如何指定多个线程的执行顺序

1. 设定一个 orderNum，每个线程执行结束之后，更新 orderNum，指明下一个要执行的线程。并且唤醒所有的等待线程。
2. 在每一个线程的开始，要 while 判断 orderNum 是否等于自己的要求值，不是，则 wait，是则执行本线程。

### 单机器并发编程

三大特性：

**原子性**

一个操作或者多个操作，要么全部执行成功，要么全部执行失败。满足原子性的操作，中途不可被中断。

-------上锁保证

**可见性**

多个线程共同访问共享变量时，某个线程修改了此变量，其他线程能立即看到修改后的值。

-------volatile保障线程可见性，volatile 关键字通过内存屏障禁止了指令的重排序，并在单个核心中，强制数据的更新及时更新到缓存。在此基础上，依靠多核心处理器的缓存一致性协议等机制，保证了变量的可见性。

**有序性**

为了提高执行效率，cpu指令可能会乱序执行；

乱序执行不得影响单线程的最终一致性as-if-serial：单线程看上去像序列化执行

乱序在多线程情况下会产生难以察觉的错误；

“happends before”jvm规定的不可以排序的八个情况

### volitale 

1.保证了共享变量的“ 可见性”。可见性的意思是当一个线程修改一个共享变量时，另外一个线程能读到这个修改的值。

2.禁止指令的重排序

3.不能保证原子性

通过内存屏障，保证了对volatile 的写操作一定会及时刷新到 CPU 缓存系统，通过 CPU 的缓存一致性协议，进而保证了多核环境下 volatile 的 happen-before 原则，一个对 volatile 的写操作只要发生在读操作之前，写的结果一定对读操作可见。

注意一下和synchronized的一个区别：synchronize无法限制指令重排，仅是满足as-if-serial语义，保证单线程情况下程序的结果。（这是为什么单例模式中，要volatile+synchronize的原因）synchronize可以解决原子性和可见性

底层实现：

字节码层面：volatile在字节码层面，就是使用访问标志：**ACC_VOLATILE**来表示，供后续操作此变量时判断访问标志是否为ACC_VOLATILE，来决定是否遵循volatile的语义处理。

jvm层面：就是一种规范，使用屏障，cpu底层使用原子指令/intel lock指令

StoreStoreBarrier

volitale 写操作

StoreLoadBarrier

——————————

LoadLoadBarrier

Volatile读操作

loadstorebarrier

### 线程同步

竞争条件/race condition：多个线程访问共享数据的时候产生竞争

数据的不一致：并发访问下产生的不期望出现的结果

如果保证数据一致呢：使用线程同步也就是让线程按照顺序规则安排好

monitor也叫锁、临界区critical section拿到锁才能执行的部分程序

粒度：如果临界区执行时间长就是锁的粒度粗反之粒度细

#### 乐观锁悲观锁

**悲观锁：**

总是假设最坏的情况，每次读取数据的时候都默认其他线程会更改数据，因此需要进行加锁操作，当其他线程想要访问数据时，都需要阻塞挂起。悲观锁的实现：

1. 传统的关系型数据库使用这种锁机制，比如行锁、表锁、读锁、写锁等，都是在操作之前先上锁。

2. Java 里面的同步 synchronized 关键字的实现。

   主要分为：

共享锁【shared locks】又称为读锁，简称 S 锁。顾名思义，共享锁就是多个事务对于同一数据可以共享一把锁，都能访问到数据，但是只能读不能修改。

排他锁【exclusive locks】又称为写锁，简称 X 锁。顾名思义，排他锁就是不能与其他锁并存，如果一个事务获取了一个数据行的排他锁，其他事务就不能再获取该行的其他锁，包括共享锁和排他锁。获取排他锁的事务可以对数据行读取和修改

**乐观锁**

假设数据一般情况不会造成冲突，所以在数据进行提交更新的时候，才会正式对数据的冲突与否进行检测，如果冲突，则返回给用户异常信息，让用户决定如何去做。乐观锁适用于读多写少的场景，这样可以提高程序的吞吐量。

所以不会产生任何锁和死锁。

1.CAS 实现：Java 中java.util.concurrent.atomic包下面的原子变量使用了乐观锁的一种 CAS 实现方式。

2.版本号控制：一般是在数据表中加上一个数据版本号 version 字段，表示数据被修改的次数。当数据被修改时，version 值会 +1。当线程 A 要更新数据时，在读取数据的同时也会读取 version 值，在提交更新时，若刚才读取到的 version 值与当前数据库中的 version 值相等时才更新，否则重试更新操作，直到更新成功。

**比较**

悲观锁往往有一个等待队列，没有抢到锁的线程在等待队列里面，是不消耗cpu的。但乐观锁的线程一直活着是消耗cpu的。如果等待的线程特别多，临界区执行时间长会导致等待的时间又很长，使用悲观锁。乐观锁比较适用于读多写少的情况(多读场景)，悲观锁比较适用于写多读少的情况(多写场景)。

如果是量化可以使用压测结果，用synchronize就很好，因为内部自动锁升级

#### synchronize锁升级

jdk早期syncronize是重量级锁，why重？因为jvm(在用户态）申请资源必须通过os kernel态的系统调用（软中断）；

过程：

new 一个普通对象/无锁，加synchronize关键字就变成了偏向锁，偏向锁轻度竞争升级为轻量级锁（也叫自旋锁/无锁化），偏向锁如果重度竞争就升级成重量级锁。

hotspot如何查看状态：

在markword里面看最低两位，00代表轻量级锁，10代表重量级锁，11表示cms正在回收次对象，01包含两种可能的状态，无锁/偏向锁；看偏向锁位再判断

**偏向锁**：多数实际运行的时候很有可能就是一个线程比如随便就用stringbuffer，第一个访问的线程不需要申请锁，mark word 更新为指向 Lock Record的指针

**自旋锁：**当有别的线程也要抢锁的时候，hotspot会将第一个线程的偏向锁取消，两个线程在自己的线程栈里面生成一个lock record，他们自旋的竞争将markword的标志指向自己的lock record，其他没抢到的线程就在用户态采用cas自旋等待。

**重量级锁**：重量级锁依赖对象内部的monitor锁来实现，而monitor又依赖操作系统的MutexLock（互斥锁）。当系统检查到是重量级锁之后，会把等待想要获取锁的线程阻塞，被阻塞的线程不会消耗CPU，但是阻塞或者唤醒一个线程，都需要通过操作系统来实现。

**锁重入：**synchronize是可重入锁、重入的次数需要记录自旋锁方式就是每重入一次在线程栈再生成一个lock record，偏向锁就是identifyhashcode也会放在lock record，markword记录次数

**自旋锁什么时候升级为重量级锁**？ 有的线程超过了10次自旋；自旋的数量超过cpu内核的一半

1.6之后自适应自旋，不需要用户设置，由jvm优化决定

**为什么需要重量级锁？**因为自旋锁占用cpu，而monitor里面有队列/waitset不消耗cpu资源、cpu线程调度再唤醒

**偏向锁一定比自旋锁效率高吗**？不一定，如果明确知道会有多个线程竞争，偏向锁撤销浪费，可以直接关闭偏向锁

#### Synchronized和Lock的区别

1. 首先synchronized是java内置关键字在jvm层面，Lock是个java类。
2. synchronized无法判断锁的状态，Lock可以判断是否获取到锁，并且可以主动尝试去获取锁。
3. synchronized会自动释放锁(a 线程执行完同步代码会释放锁 ；b 线程执行过程中发生异常会释放锁)，Lock需在finally中手工释放锁（unlock()方法释放锁），否则容易造成线程死锁。
4. 用synchronized关键字的两个线程1和线程2，如果当前线程1获得锁，线程2线程等待。如果线程1阻塞，线程2则会一直等待下去，而Lock锁就不一定会等待下去，如果尝试获取不到锁，线程可以不用一直等待就结束了。
5. synchronized的锁可重入、不可中断、非公平，而Lock锁可重入、可判断、可公平（两者皆可）
6. Lock锁适合大量同步的代码的同步问题，synchronized锁适合代码少量的同步问题。
7. Lock可以使用读线程提高多线程的读效率

#### CAS

CAS是英文单词CompareAndSwap的缩写，CAS需要有3个操作数：内存地址V，旧的预期值A，即将要更新的目标值B。CAS指令执行时，当且仅当内存地址V的值与预期值A相等时，将内存地址V的值修改为B，否则就什么都不做。整个比较并替换的操作是一个原子操作。

“将a=0读出来，尝试设置1，如果发现a还是0就设置成功，如果发现a=8，就再用9试一试，如果变成100，继续试......”

**CAS操作ABA问题：**

如果在这段期间它的值曾经被改成了B，后来又被改回为A，那CAS操作就会误认为它从来没有被改变过。

有些情况下，会在意，比如是一个引用指向的内容发生了改变。

Java并发包为了解决这个问题，提供了一个带有标记的原子引用类“AtomicStampedReference”，它可以通过控制变量值的版本来保证CAS的正确性。

**CAS 的缺点**

1.ABA问题 

2.**循环时间长开销大**：自旋CAS的方式如果长时间不成功，会给CPU带来很大的开销。

3.**只能保证一个共享变量的原子操作**：只对一个共享变量操作可以保证原子性，但是多个则不行，多个可以通过AtomicReference来处理或者使用锁synchronized实现。

#### AtomicInteger

**底层实现**

IncreateAndGet()用到了native compareAndSwapInt()保证原子性，hotspot里面利用到cpu汇编语言有cas原语

很遗憾在多核cpu，这条cpu原语不是原子的，会用到lock原语（将总线锁住）

#### 死锁

防止死锁可以采用以下的方法：

尽量使用 tryLock(long timeout, TimeUnit unit)的方法(ReentrantLock、ReentrantReadWriteLock)，设置超时时间，超时可以退出防止死锁。
尽量使用 Java. util. concurrent 并发类代替自己手写锁。
尽量降低锁的使用粒度，尽量不要几个功能用同一把锁。
尽量减少同步的代码块。

死锁：是指两个或两个以上的进程（或线程）在执行过程中，因争夺资源而造成的一种互相等待的现象，若无外力作用，它们都将无法推进下去。

活锁：任务或者执行者没有被阻塞，由于某些条件没有满足，导致一直重复尝试，失败，尝试，失败。

饥饿：一个或者多个线程因为种种原因无法获得所需要的资源，导致一直无法执行的状态。

#### AQS

AQS是一个用来构建锁和同步器的框架，使用AQS能简单且高效地构造出应用广泛的大量的同步器，比如我们提到的ReentrantLock，Semaphore，其他的诸如ReentrantReadWriteLock，SynchronousQueue，FutureTask等等皆是基于AQS的。当然，我们自己也能利用AQS非常轻松容易地构造出符合我们自己需求的同步器。

AQS核心思想是，如果被请求的共享资源空闲，则将当前请求资源的线程设置为有效的工作线程，并且将共享资源设置为锁定状态。如果被请求的共享资源被占用，那么就需要一套线程阻塞等待以及被唤醒时锁分配的机制，这个机制AQS是用CLH队列锁实现的，即将暂时获取不到锁的线程加入到队列中。

CLH(Craig,Landin,and Hagersten)队列是一个虚拟的双向队列（虚拟的双向队列即不存在队列实例，仅存在结点之间的关联关系）。AQS是将每条请求共享资源的线程封装成一个CLH锁队列的一个结点（Node）来实现锁的分配。

AQS定义两种资源共享方式

Exclusive（独占）：只有一个线程能执行，如ReentrantLock。又可分为公平锁和非公平锁：

公平锁：按照线程在队列中的排队顺序，先到者先拿到锁
非公平锁：当线程要获取锁时，无视队列顺序直接去抢锁，谁抢到就是谁的
Share（共享）：多个线程可同时执行，如Semaphore/CountDownLatch。Semaphore、CountDownLatch、 CyclicBarrier、ReadWriteLock 我们都会在后面讲到。

### 并发容器

#### ThreadLocal

ThreadLocal 是一个本地线程副本变量工具类，在每个线程中都创建了一个 ThreadLocalMap 对象，简单说 ThreadLocal 就是一种以空间换时间的做法，每个线程可以访问自己内部 ThreadLocalMap 对象内的 value。通过这种方式，避免资源在多线程间共享。

原理：线程局部变量是局限于线程内部的变量，属于线程自身所有，不在多个线程间共享。Java提供ThreadLocal类来支持线程局部变量，是一种实现线程安全的方式。但是在管理环境下（如 web 服务器）使用线程局部变量的时候要特别小心，在这种情况下，工作线程的生命周期比任何应用变量的生命周期都要长。任何线程局部变量一旦在工作完成后没有释放，Java 应用就存在内存泄露的风险。

经典的使用场景是为每个线程分配一个 JDBC 连接 Connection。这样就可以保证每个线程的都在各自的 Connection 上进行数据库的操作，不会出现 A 线程关了 B线程正在使用的 Connection； 还有 Session 管理 等问题

线程局部变量是局限于线程内部的变量，属于线程自身所有，不在多个线程间共享.

ThreadLocal造成**内存泄漏**的原因？

ThreadLocalMap 中使用的 key 为 ThreadLocal 的弱引用,而 value 是强引用。所以，如果 ThreadLocal 没有被外部强引用的情况下，在垃圾回收的时候，key 会被清理掉，而 value 不会被清理掉。这样一来，ThreadLocalMap 中就会出现key为null的Entry。假如我们不做任何措施的话，value 永远无法被GC 回收，这个时候就可能会产生内存泄露。ThreadLocalMap实现中已经考虑了这种情况，在调用 set()、get()、remove() 方法的时候，会清理掉 key 为 null 的记录。使用完 ThreadLocal方法后 最好手动调用remove()方法

#### ConcurrentHashMap

jdk1.8

**Q: 数据结构什么样？**

跟hashmap一样，数组+链表+红黑树，存储结构是node，node有key、value还有指向下一个node的next，还有hash值，next作用是解决hash冲突之后生成一个链表使用的。

Q:负载因子可以修改吗？

普通的hashmap是可以修改的，并发map不可以修改，0.75

**Q:node.hash 一般情况下>= 0为什么？**

因为小于0是有别的意义的，就是散列表扩容的时候会触发一个数据迁移的过程，把原表的数据迁移到扩容之后的散列表，迁移完之后在老表的桶放一个标记节点forwarding node节点，这个node的hash值就是-1

红黑树的情况，红黑树由一个特殊的节点代理，treebin结构，hash值-2

**Q:sizectl 含义是什么？**

1.sizeCtl为0，代表数组未初始化，且数组的初始容量为16
2.sizeCtl为正数：

如果数组未初始化，纪录数组的初始容量，如果已初始化，纪录的是数组的扩容阈值。

比如64，size >=64就要开始扩容了

3.sizeCtl为-1：

表示正在进行初始化, 跟hashmap一样延迟初始化，只是并发过程中，多个线程都执行inittable这个逻辑的时候，就会使用cas的方式去修改这个sizectl的值。sizectl的期望初始值就是0，更新成功就是-1，更新成功的线程去真正执行初始化散列表的逻辑，失败的线程就自旋检查，（dogeelee优化每次检查之后会让线程短暂的释放所占的cpu让当前线程重新抢占cpu）
4.sizeCtl小于0但不是-1：

表示数组正在扩容，高十六位是扩容标志戳，第十六位表示有n + 1个线程正在共同完成扩容操作。

**Q:扩容标志戳的计算方式**

保证每个线程在扩容的，散列表从小到大，每次计算出来的值是一致的。比方说，从16扩容到32，每个线程计算出来的扩容唯一标识戳，他们都是同一个值。扩容标志戳和table是强相关的，不同的长度计算出来的戳是不一样的。不同的线程看到的同一个长度，计算出来的戳是一样的

**Q:如何保证线程写数据安全呢？**

先说一个如何保证线程安全吧，并发map采用的方式就是synchronized锁住桶头节点保证桶内的写操作是线程安全的，如果桶内是空的，采用cas来创建头节点保证线程安全，线程采用cas方式向slot里面写头节点数据，成功就返回，失败表示有别的线程在竞争这个slot位置，当前线程重新路由到这个位置的时候，slot有值了，就synchronize锁住头节点，这样桶内就是串行了

**Q:描述一下hash寻址算法？**

跟普通的hashmap区别不大，先拿到key的hashcode，然后进行扰动运算，让高16位和低16位异或。将符合位强制设置为0，让hash成为一个正数。为了让高位的数字也参与进去，增强散列性

**Q:size字段-统计当前散列表数据量在并发map中使用什么呢？**

使用了一个longadder、dougelee没有直接引用包，而是源码；

longaddr内部结构：base + cell数据+cell里面有value

采用cas方式去更新base字段，当某个线程失败，就将cell数组构建出来，往后的累积请求不再首选base字段而是根据分配给线程的一个hash值进行位于运算，找到cell，通过cas写入cell的值里面

**Q:为什么不用atomiclong？**

cas并发量大的情况下，比较期望值，如果很多线程会消耗cpu，一个是内核会检查是不是多核，如果是多核，会执行lock总线方式让同一时刻只有一个cpu去执行 compareandchange这个操作；而且一个从线程成功，之后线程全部失败，再次尝试修改；那并发map如何处理size这个问题呢？

相当于热点数据，原来的请求打在一点上，现在想办法打在不同的点上，冲突概率小，性能提升用空间换时间；

**Q:触发扩容条件的线程，执行的预处理工作有哪些？**

修改sizectl，根据扩容前的散列表长度，计算出扩容的唯一标志戳，一个16位的值，最高位是1，存在高16位，

低16位是参与扩容的工作线程+1，设置2；

创建一个新的table，大小是扩容前的2倍，需要告诉新表的引用地址到map.nexttable字段，因为后续的协助扩容线程需要知道老表的数据迁移到哪里去了，

保存老表的长度到map。transferindex字段，迁移工作从高位开始，一致迁移到下表是0的桶

**Q:迁移完的桶怎么标记？**

forwarding node，hash<0 不是-1表示被迁移走了，里面还有一个指向新表的字段，查询的时候可以重定向到新表查询

**Q:散列表正在扩容时候，再来的写请求如何处理呢**？

如果写操作要访问的桶还没有被迁移，就拿到桶锁，正常操作；

如果访问的forwardingnode，为了让扩容的速度越快越好，多几线程进行操作，正好咱们这个写操作这个线程

也没什么事情干，不如去帮忙扩容，sizectl低16位+1（写操作协助扩容）根据全局transferindex去规划当前线程的任务区间，比如说【256，270】就搬运到新的地方，然后再回来根据transderindex分配下一批任务，知道线程再也分配不到任务的时候，扩容工作就算完成了，当前线程返回写数据的逻辑，数据会写在新的table

最后一个线程收尾工作：sizectl 低16位- 1 = 1 表示自己是最后一个线程，检查一遍老表看看有没有拉下的，根据新表的大小，算出阈值更新sizectl

**Q:桶已经升级为红黑树了，且当前红黑树上有读线程访问，再来写请求怎么办？**

写数据会导致红黑树失衡，会自平衡操作，所以不能写；treebin怎么处理呢？有一个int字段，叫state，读的时候cas将state+4，读完state-4，写线程在写的时候要检查这个state是否为0如果是0表示这颗树上没有访问线程可以写，cas将state设置为1，表示加了写锁。如果不是0就等待把自己挂起来state=2，读线程检查state是2表示有些线程等待将等待写线程唤起。

**Q:红黑树如果进行写操作，此时再来读请求怎么办？**

treebin现在是state=1，读请求不再红黑树上查询，treebin保留了链表结构去访问

**Q: vs SynchronizedMap** 

一次锁住整张表来保证线程安全，所以每次只能有一个线程来访为 map。ConcurrentHashMap 使用分段锁来保证在多线程下的性能。

#### BlockingQueue

在Java中，BlockingQueue是一个接口，它的实现类有ArrayBlockingQueue、DelayQueue、 LinkedBlockingDeque、LinkedBlockingQueue、PriorityBlockingQueue、SynchronousQueue等，它们的区别主要体现在存储结构上或对元素操作上的不同，但是对于take与put操作的原理，却是类似的：

入队

offer(E e)：如果队列没满，立即返回true； 如果队列满了，立即返回false-->不阻塞

put(E e)：如果队列满了，一直阻塞，直到队列不满了或者线程被中断-->阻塞

offer(E e, long timeout, TimeUnit unit)：在队尾插入一个元素,，如果队列已满，则进入等待，直到出现以下三种情况：被唤醒、等待时间超时、当前线程被中断 ->阻塞

出队：

poll()：如果没有元素，直接返回null；如果有元素，出队

take()：如果队列空了，一直阻塞，直到队列不为空或者线程被中断-->阻塞

poll(long timeout, TimeUnit unit)：如果队列不空，出队；如果队列已空且已经超时，返回null；如果队列已空且时间未超时，则进入等待，直到出现以下三种情况：被唤醒、等待时间超时、当前线程被中断

**有界队列**：就是有固定大小的队列。比如设定了固定大小的 LinkedBlockingQueue，又或者大小为 0，只是在生产者和消费者中做中转用的 SynchronousQueue。

**无界队列**：指的是没有设置固定大小的队列。这些队列的特点是可以直接入列，直到溢出。当然现实几乎不会有到这么大的容量（超过 Integer.MAX_VALUE），所以从使用者的体验上，就相当于 “无界”。比如没有设定固定大小的 LinkedBlockingQueue
我们这里的队列都指线程池使用的阻塞队列 BlockingQueue 的实现，使用的最多的应该是LinkedBlockingQueue，注意一般情况下要配置一下队列大小，设置成有界队列，否则JVM内存会被撑爆！

**LinkedBlockingQueue**：LinkedBlockingQueue是允许两个线程同时在两端进行入队或出队的操作的，但一端同时只能有一个线程进行操作，这是通过两把锁来区分的；

为了维持底部数据的统一，引入了AtomicInteger的一个count变量，表示队列中元素的个数。count只能在两个地方变化，一个是入队的方法（可以+1），另一个是出队的方法（可以-1），而AtomicInteger是原子安全的，所以也就确保了底层队列的数据同步。

**ArrayBlockingQueue**的并发阻塞是通过ReentrantLock和Condition来实现的，ArrayBlockingQueue内部只有一把锁，意味着同一时刻只有一个线程能进行入队或者出队的操作。

#### CopyOnWriteArrayList

CopyOnWriteArrayList 是一个并发容器。有很多人称它是线程安全的，我认为这句话不严谨，缺少一个前提条件，那就是非复合场景下操作它是线程安全的。

CopyOnWriteArrayList(免锁容器)的好处之一是当多个迭代器同时遍历和修改这个列表时，不会抛出 ConcurrentModificationException。在CopyOnWriteArrayList 中，写入将导致创建整个底层数组的副本，而源数组将保留在原地，使得复制的数组在被修改时，读取操作可以安全地执行。

CopyOnWriteArrayList 的使用场景

通过源码分析，我们看出它的优缺点比较明显，所以使用场景也就比较明显。就是合适读多写少的场景。

CopyOnWriteArrayList 的设计思想

1. 读写分离，读和写分开
2. 最终一致性
3. 使用另外开辟空间的思路，来解决并发冲突

CopyOnWriteArrayList 的缺点

由于写操作的时候，需要拷贝数组，会消耗内存，如果原数组的内容比较多的情况下，可能导致 young gc 或者 full gc。
不能用于实时读的场景，像拷贝数组、新增元素都需要时间，所以调用一个 set 操作后，读取到数据可能还是旧的，虽然CopyOnWriteArrayList 能做到最终一致性,但是还是没法满足实时性要求。
由于实际使用中可能没法保证 CopyOnWriteArrayList 到底要放置多少数据，万一数据稍微有点多，每次 add/set 都要重新复制数组，这个代价实在太高昂了。在高性能的互联网应用中，这种操作分分钟引起故障。

### 并发工具

**Semaphore(信号量)**-允许多个线程同时访问： synchronized 和 ReentrantLock 都是一次只允许一个线程访问某个资源，Semaphore(信号量)可以指定多个线程同时访问某个资源。
**CountDownLatch(倒计时器)：** CountDownLatch是一个同步工具类，用来协调多个线程之间的同步。这个工具通常用来控制线程等待，它可以让某一个线程等待直到倒计时结束，再开始执行。
**CyclicBarrier(循环栅栏)**： CyclicBarrier 和 CountDownLatch 非常类似，它也可以实现线程间的技术等待，但是它的功能比 CountDownLatch 更加复杂和强大。主要应用场景和 CountDownLatch 类似。CyclicBarrier 的字面意思是可循环使用（Cyclic）的屏障（Barrier）。它要做的事情是，让一组线程到达一个屏障（也可以叫同步点）时被阻塞，直到最后一个线程到达屏障时，屏障才会开门，所有被屏障拦截的线程才会继续干活。CyclicBarrier默认的构造方法是 CyclicBarrier(int parties)，其参数表示屏障拦截的线程数量，每个线程调用await()方法告诉 CyclicBarrier 我已经到达了屏障，然后当前线程被阻塞。

# mysql

### 存储引擎

innodb默认事务型引擎，最广泛的，用来处理大量的短期事务，短期事务都是正常提交的，很少回滚。innodb性能和自动崩溃恢复特性，在非事务存储需求下也很流行，一般没必要用别的。

innodb采用mvcc来支持高并发，实现了四个隔离级别，默认rr，通过间隙锁防止幻读；

表基于聚簇索引建立的；从磁盘读取数据采用可预测读，自动在内存中创建hash索引来加速读操作的自适应哈希算法，插入缓存区；热备份

5.1之前的myisam，csv引擎可以将普通的csv文件作为mysql的表来处理，但不支持索引，在数据库运行时拷入烤出文件；memory引擎，如果需要快速访问数据，并且数据不会修改，重启之后丢失也没关系，快，因为所有的数据包存在内存中，没有磁盘i/o

###  mysql持久性

最简单的做法是在每次事务提交的时候，将该事务涉及修改的数据页全部刷新到磁盘中。但是这么做会有严重的性能问题，主要体现在两个方面：

1. 因为`Innodb`是以`页`为单位进行磁盘交互的，而一个事务很可能只修改一个数据页里面的几个字节，这个时候将完整的数据页刷到磁盘的话，太浪费资源了！
2. 一个事务可能涉及修改多个数据页，并且这些数据页在物理上并不连续，使用随机IO写入性能太差！

因此`mysql`设计了`redo log`，**具体来说就是只记录事务对数据页做了哪些修改**，这样就能完美地解决性能问题了(相对而言文件更小并且是顺序IO)。

#### redolog

redo log包括两部分：一个是内存中的日志缓冲(redo log buffer)，另一个是磁盘上的日志文件(redo log file)。mysql每执行一条DML语句，先将记录写入redo log buffer，后续某个时间点再一次性将多个操作记录写到redo log file。这种先写日志，再写磁盘的技术就是MySQL里经常说到的WAL(Write-Ahead Logging) 技术

redo log buffer写入redo log file实际上是先写入OS Buffer，然后再通过系统调用fsync()将其刷到redo log file中

mysql支持三种：

1. 延迟写：事务提交时不会将`redo log buffer`中日志写入到`os buffer`，而是每秒写入`os buffer`并调用`fsync()`写入到`redo log file`中。也就是说设置为0时是(大约)每秒刷新写入到磁盘中的，当系统崩溃，会丢失1秒钟的数据。
2. 实时写，实时刷：事务每次提交都会将`redo log buffer`中的日志写入`os buffer`并调用`fsync()`刷到`redo log file`中。这种方式即使系统崩溃也不会丢失任何数据，但是因为每次提交都写入磁盘，IO的性能较差。
3. 实时写，延迟刷：每次提交都仅写入到`os buffer`，然后是每秒调用`fsync()`将`os buffer`中的日志写入到`redo log file`

#### binlog vs redolog

1)文件大小:`redo log`的大小是固定的。`binlog`可通过配置参数`max_binlog_size`设置每个`binlog`文件的大小。

2)实现方式:`redo log`是`InnoDB`引擎层实现的，并不是所有引擎都有。`binlog`是`Server`层实现的，所有引擎都可以使用 `binlog`日志

3)记录方式:redo log 采用循环写的方式记录，当写到结尾时，会回到开头循环写日志。binlog 通过追加的方式记录，当文件大小大于给定值后，后续的日志会记录到新的文件上

4)适用场景`redo log`适用于崩溃恢复(crash-safe) `binlog`适用于主从复制和数据恢复

#### 数据恢复

由`binlog`和`redo log`的区别可知：`binlog`日志只用于归档，只依靠`binlog`是没有`crash-safe`能力的。但只有`redo log`也不行，因为`redo log`是`InnoDB`特有的，且日志上的记录落盘后会被覆盖掉。因此需要`binlog`和`redo log`二者同时记录，才能保证当数据库发生宕机重启时，数据不会丢失。

### mysql主从复制

1）首先，MySQL主服务器在更新数据库或其他进行数据库相关操作时，会在二进制日志文件中记录这些改变，当写入日志完成后，主服务器会告知存储引擎提交事务；

2）MySQL从服务器会将主服务器的二进制日志文件（Binary log）复制到其中继日志（Relay log）中。中继日志通常存放在系统缓存中，因此中继日志的开销很小；

3）从服务器通过自身线程从中继日志中读取事件，更新自身的日志文件使其与主服务器中的数据一致。

#### binlog

`binlog`用于记录数据库执行的写入性操作(不包括查询)信息，以二进制的形式保存在磁盘中。`binlog`是`mysql`的逻辑日志，并且由`Server`层进行记录，使用任何存储引擎的`mysql`数据库都会记录`binlog`日志。

逻辑日志：可以简单理解为记录的就是sql语句

物理日志：因为`mysql`数据最终是保存在数据页中的，物理日志记录的就是数据页变更

**binlog使用场景：**

在实际应用中，`binlog`的主要使用场景有两个，分别是**主从复制**和**数据恢复**。

1. **主从复制**：在`Master`端开启`binlog`，然后将`binlog`发送到各个`Slave`端，`Slave`端重放`binlog`从而达到主从数据一致。
2. **数据恢复**：通过使用`mysqlbinlog`工具来恢复数据。

**binlog刷盘时机：**

对于InnoDB存储引擎而言，只有在事务提交时才会记录biglog，此时记录还在内存中，那么biglog是什么时候刷到磁盘中的呢？mysql通过sync_binlog参数控制biglog的刷盘时机，取值范围是0-N：

0：不去强制要求，由系统自行判断何时写入磁盘；
1：每次commit的时候都要将binlog写入磁盘；
N：每N个事务，才会将binlog写入磁盘。

从上面可以看出，sync_binlog最安全的是设置是1，这也是MySQL 5.7.7之后版本的默认值

**binlog日志格式**

binlog`日志有三种格式，分别为`STATMENT`、`ROW`和`MIXED

STATMENT
基于SQL语句的复制(statement-based replication, SBR)，每一条会修改数据的sql语句会记录到binlog中。
优点：不需要记录每一行的变化，减少了binlog日志量，节约了IO, 从而提高了性能；
缺点：在某些情况下会导致主从数据不一致，比如执行sysdate()、slepp()等。
ROW
基于行的复制(row-based replication, RBR)，不记录每条sql语句的上下文信息，仅需记录哪条数据被修改了。
优点：不会出现某些特定情况下的存储过程、或function、或trigger的调用和触发无法被正确复制的问题；
缺点：会产生大量的日志，尤其是alter table的时候会让日志暴涨
MIXED
基于STATMENT和ROW两种模式的混合复制(mixed-based replication, MBR)，一般的复制使用STATEMENT模式保存binlog，对于STATEMENT模式无法复制的操作使用ROW模式保存binlog

### mysql读写分离

MySQL的读写分离的实现需要基于主从复制的基础之上。在主服务器上写数据，使用从服务器轮循读取数据的功能。

### mysql数据恢复

MySQL的binlog日志是MySQL日志中非常重要的一种日志，记录了数据库所有的DML操作。通过binlog日志我们可以进行数据库的读写分离、数据增量备份以及服务器宕机时的数据恢复。



### mysql并发控制

#### 读写锁

在处理并发读or写时候，可以通过实现一个由两种类型的锁组成的锁系统来解决问题。这两种类型的锁通常称为共享锁和排他锁，也叫读锁和写锁。读锁是共享的，多个客户在同一时刻读取同一资源，并且互不干扰。写锁是排他的，一个写锁会阻塞其他的写锁和读锁。

#### 锁粒度

1任何时候，在给定的资源上，锁定的数据量越少，则系统的并发度越高，只要相互之间不发生冲突即可。

2但加锁需要消耗资源，锁的各种操作，获得锁，检查锁是否释放，解除锁，都会增加系统的开销。如果系统话费大量的时间来管理锁，而不是存取数据，那么系统的性能就会受到影响。

so，权衡，mysql提供了多种引擎，可以实现自己的锁策略和锁力度。

**表锁 table lock**：

最基本，开销最小，锁住整张表。一个用户对表进行写操作（插入，删除，更新）之前需要获得写锁，这会阻塞其他用户对该表的所有读写操作。尽管存储引擎可以管理自己的锁，mysql本身还是会使用各种有效的表锁来实现不同的目的。例如，服务器会为alter table之类的语句加表锁，忽略innodb的锁机制。

**行级锁：row lock** 

可以最大程度的支持并发处理（带来了最大的锁开销）innodb支持。

#### 死锁

mysql有死锁检测和死锁超时机制。事务型数据库无法避免

解决方式一：innodb可以检测到死锁的循环依赖，并立即返回一个错误。否则死锁会出现非常慢的查询

解决方式二：当查询的时间达到锁等待超时的设定后放弃锁请求，innodb是将持有最少行级排他锁的事务进行回滚，重新执行因死锁回滚的事务即可。

### 什么是索引？

explain * from temp 可以从type里面看到等级

- 索引的种类有很多：主键索引（这是最常见的一种索引，主键不能为空且必须唯一）、唯一索引（相对于主键索引，它的值可以为空）、全文索引（在char、varchar、text类型可以使用）、普通索引、前缀索引。按照列数来区分：单一索引、组合索引（多字段组成）

1.用途：用来提高查询效率，**索引和数据其实都是存放在磁盘上的，只是进行数据读取的时候会优先把索引存放在内存上。**

client--server---存储引擎：不同数据文件在磁盘的组织形式

2.格式 kv格式

3.选择合理的数据结构进行存储，为什么不是b树，不是hash表，而是b+树？

### 为什么要b+树？

当表的数据变大，索引也会变大，没办法直接加载到内存怎么办？只好分块读取。

磁盘预读：内存和磁盘交互的时候有一个最小的逻辑单位，这个单位是datapage，4k/8k，我们在进行数据读取的时候，一般会读取页的整数倍。innodb在进行数据加载的时候读取16kb。

1.hash表有什么问题？需要范围查找的时候需要挨个遍历，效率低下。

memory支持哈希索引，innodb也支持自适应哈希

当InnoDB注意到某些**索引值被使用得非常频繁时**，它会在内存中基于B-Tree索引之上再创建一个哈希索引，这样就让B-Tree索引也具有哈希索引的一些优点，比如快速的哈希查找。这是一个完全自动的、内部的行为，用户无法控制或者配置，不过如果有必要，完全可以关闭该功能

2.二叉树，bst，avl，红黑树为什么不行？ 需要向这些树中插入数据的时候，会让这些树非常高。会加大读取的次数，影响查询效率。

3.想要高度变低：b树。3层的b树，假设一个磁盘块16kb，也就16^3=4096条记录，也就是最多这么多了。如果想存更多的记录，树变高，io又变高。

4.b+树，只在叶子节点放数据。3层的b+树，假设一个磁盘块16kb，一个磁盘块就可以放16乘1024/1000=1600个范围。1600乘1600乘以16kb=4k万个记录。

一般情况下，3到4层的b加树足以支持千万级别的数据量存储。

索引的选择性：

进行索引设计时候，让key尽可能的少去占用存储空间。-----前缀索引，可以自己试一试调整选几个字符。

### 聚簇索引，非聚簇索引

聚簇：数据和索引存储在一起的

非聚簇：数据和索引没有存在一起

innodb在进行数据插入的时候，数据必须要跟某一个索引列存储在一起，可以是主键，如果没有主键，选择唯一建，如果没有，选择6字节row id，数据必然是跟某一个索引绑定在一起的，此时的索引就是聚簇索引。

如果一个数据已经跟主键绑定在一起了，其他索引的叶子节点中，存储的数据不再是整行的记录，而是聚簇索引的id值。

innodb既有聚簇索引也有非聚簇索引 myisam中只有非聚簇索引（索引在内存，数据在disk）

——————————————————————————————————————————————

id name age gender

id是主键，name普通索引，id是聚簇索引，name对应的索引的b+树上的叶子节点存储的就是id值。

主索引树 vs 辅助索引树

（所以不要用select *， 如果select name 就不用回表了，更快）

**回表**： select * from user where name = ‘zhangsan’ 检索过程是先根据nameb+树比配到对应的叶子节点，查询到对应行记录的id值，再根据id去b+树中检索整行记录，这个过程是回表，效率低，尽量避免回表。

select id，name from user where name = ‘zhangsan’ 根据name的值去nameb+树检索对应的记录，能获取到的id属性值，索引的叶子节点包含了查询的所有的列，此时不需要回表，这个过程叫索引覆盖，

**联合索引**（索引覆盖）：在某些场景中，可以考虑将要查询的所有列都变成组合索引，此时会使用索引覆盖，加快查询效率。（索引会变的大）select id，age from table where name = ‘zhangsan’

alter table user add index 'id_name_age'('name', 'age')

联合索引的b+树存储结构：先比较第一个，再比较第二个

​                                                      （b，18） 

左子树：（a，12）（a，19）（b，12） 右子树：（b，18）（c，12）（c，13）

先按照第一列的顺序，也就是name是有序的，age是无序的

使用联合索引的时候，容易写成**索引失效**的语句：

 select id，age  from table where age =12 

**最左匹配**：创建索引的时候，可以选择多个列共同组成索引，就是组合索引，要遵循最左匹配原则。

**索引下推**：icp（index condition pushdown），mysql5.6的新特性

----只针对二级（辅助）索引 select * from user where name = zhangsn and age = 10；

之前是第一步通过联合索引，先查询符合要求的主键，第二步回表多次查询到完整的数据，第三步再将符合的结果返回。

icp如果能在二级索引中拿到数据，直接过滤数据，最后满足条件的再回表，减少回表

**索引失效**

典型的场景：

a.最左前缀-联合索引

b.like语句 “bob%”可以使用索引（字符先比较第一个字符再比较第二个字符）“%bob”会失效

c.在列上不能函数运算 abs(salary) < 10000 

d. in 不会进行索引失效，但not in 就会失效 比如in(400,500)是一个range type

e. mysql走不走索引不是绝对的，mysql会去分析sql语句，分析走什么索引，或者不走索引全表扫描看一下时间

f. or也会 eg. salary in(400,500) or from date=1990-09-01  索引失效

g. 使用null is null 不会走索引吗？不一定，如果只是select主键也会去扫描二级索引，因为二级索引小，i/o少

my很聪明的，会自己语句优化。

### 快照读 vs 当前读

**快照读**

快照读是指读取数据时不是读取最新版本的数据，而是基于历史版本读取的一个快照信息（mysql读取undo log历史版本) ，快照读可以使普通的SELECT 读取数据时不用对表数据进行加锁，从而解决了因为对数据库表的加锁而导致的两个如下问题

1、解决了因加锁导致的修改数据时无法对数据读取问题;

2、解决了因加锁导致读取数据时无法对数据进行修改的问题;

**MVCC不存在幻读问题（RR级别的情况下）**

首先确认一点MVCC属于快照读的，在进行快照读的情况下是不会对数据进行加锁，而是基于事务版本号和undo历史版本读取数据。快照读的时候就根本没加锁，否则的话数据是不可能插入成功的，而且在插入数据提交成功后，我们执行第二条查询 语句是读取不到中间插入的这条数据的，这也就说明在没有加锁的情况下，**基于历史版本的MVCC快照读是可以避免幻读问题的**。

**当前读**

当前读是读取的数据库最新的数据，当前读和快照读不同，因为要读取最新的数据而且要保证事务的隔离性，所以当前读是需要对数据进行加锁的（Update delete insert select ....lock in share mode select for update 为当前读）

###  next-key locking

索引失效，行锁升级为表锁

间隙锁：where a>1 and a < 10 会将1到10全部都锁住，update a = 8不可以

### read view

在innodb 中每个事务开启后都会得到一个read_view。副本主要保存了当前数据库系统中正处于活跃（没有commit）的事务的ID号，其实简单的说这个副本中保存的是系统中当前不应该被本事务看到的其他事务id列表。

**Read view 的几个重要属性**

**trx_ids:** 当前系统活跃(未提交)事务版本号集合。

**low_limit_id:** 创建当前read view 时“当前系统最大**事务版本号**+1”。

**up_limit_id:** 创建当前read view 时“系统正处于**活跃事务**最小版本号”

**creator_trx_id:** 创建当前read view的事务版本号；

**Read view 匹配条件**

**（1）数据事务ID <up_limit_id 则显示**

如果数据事务ID小于read view中的最小活跃事务ID，则可以肯定该数据是在当前事务启之前就已经存在了的,所以可以显示。

**（2）数据事务ID>=low_limit_id 则不显示**

如果数据事务ID大于read view 中的当前系统的最大事务ID，则说明该数据是在当前read view 创建之后才产生的，所以数据不予显示。

**（3） up_limit_id <=**数据事务ID<**low_limit_id 则与活跃事务集合**trx_ids**里匹配**

如果数据的事务ID大于最小的活跃事务ID,同时又小于等于系统最大的事务ID，这种情况就说明这个数据有可能是在当前事务开始的时候还没有提交的。

所以这时候我们需要把数据的事务ID与当前read view 中的活跃事务集合trx_ids 匹配:

**情况1:** 如果事务ID不存在于trx_ids 集合（则说明read view产生的时候事务已经commit了），这种情况数据则可以显示。

**情况2：** 如果事务ID存在trx_ids则说明read view产生的时候数据还没有提交，但是如果数据的事务ID等于creator_trx_id ，那么说明这个数据就是当前事务自己生成的，自己生成的数据自己当然能看见，所以这种情况下此数据也是可以显示的。

**情况3：** 如果事务ID既存在trx_ids而且又不等于creator_trx_id那就说明read view产生的时候数据还没有提交，又不是自己生成的，所以这种情况下此数据不能显示。

（4）如果满足read view条件，此时，如果这条记录的delete_flag为true，说明这条记录已被删除，不返回。

　　　如果delete_flag为false，说明此记录可以安全返回给客户端

**（5）不满足read view条件时候，从undo log里面获取数据**

当数据的事务ID不满足read view条件时候，从undo log里面获取数据的历史版本，然后数据历史版本事务号回头再来和read view 条件匹配 ，直到找到一条满足条件的历史数据，或者找不到则返回空结果；

### mvcc

mysql大多数的事务型存储引擎都不是简单的行级锁，基于提高并发性能的考虑，它们一般同时实现了多版本并发控制mvcc。oracle等数据库系统也实现了mvcc，但各自的实现机制不尽相同，mvcc没有统一的实现标准。

mvcc是行级锁的变种，很多情况避免了加锁操作，开销更低。虽然机制不同，但也是非阻塞读，写只锁定必要行。mvcc的实现是通过保存数据在某个时间点的快照来实现的，不管需要执行多长时间，每个事务看到的数据都是一致的。根据事务开始的时间不同，每个事务对同一个表，同一时刻看到的数据可能不一样。

不同存储引擎实现不同，比如乐观/悲观并发控制。

--------------------------------------innodb 实现-------------------------------------------------------------------------------------------------

1. **每条记录含有的隐藏列三个**

**DB_TRX_ID**, 6byte, 创建这条记录/最后一次更新这条记录的事务ID

**DB_ROLL_PTR**, 7byte，回滚指针，指向这条记录的上一个版本（存储于rollback segment里）

**DB_ROW_ID**, 6byte，隐含的自增ID，如果数据表没有主键，InnoDB会自动以DB_ROW_ID产生一个聚簇索引

另外，每条记录的头信息（record header）里都有一个专门的bit（**deleted_flag**）表示当前记录是否已经被删除

2. **记录的历史版本是放在专门的rollback segment里（undo log）**

   　　UPDATE非主键语句的效果是

      　　　　老记录被复制到rollback segment中形成undo log，DB_TRX_ID和DB_ROLL_PTR不动

      　　　　新记录的DB_TRX_ID = 当前事务ID，DB_ROLL_PTR指向老记录形成的undo log

      　　　　这样就能通过DB_ROLL_PTR找到这条记录的历史版本。如果对同一行记录执行连续的update操作，新记录与undo log会组成一个链表，遍历这个链表可以看到这条记录的变迁

3.  **MySQL的一致性读，是通过一个叫做read view的结构来实现的**

4. **用MVCC这一种手段可以同时实现RR与RC隔离级别**

它们的不同之处在于：

**RR**：read view是在**first touch read**时创建的，也就是执行事务中的第一条SELECT语句的瞬间，后续所有的SELECT都是复用这个read view，所以能保证每次读取的一致性（可重复读的语义）

**RC**：每次读取，都会创建一个新的read view。这样就能读取到其他事务已经COMMIT的内容。

所以对于InnoDB来说，RR虽然比RC隔离级别高，但是开销反而相对少。

补充：RU的实现就简单多了，不使用read view，也不需要管什么DB_TRX_ID和DB_ROLL_PTR，直接读取最新的record即可。

5. **二级索引与MVCC**

MySQL的索引分为聚簇索引(clustered index)与二级索引(secondary index)两种。

刚才讲的内容是基于聚簇索引的，只有聚簇索引中含有DB_TRX_ID与DB_ROLL_PTR隐藏列，可以比较容易的实现MVCC

但是二级索引中并不含有这几个隐藏列，只含有1个bit的deleted flag，咋办？

 　好办，如果UPDATE语句涉及到二级索引的键值，将老的二级索引的deleted flag标记为true，然后创建一条新的二级索引记录即可。

但是如果想根据二级索引来做查询，这可就麻烦了。因为二级索引不维护版本信息，无法判断二级索引中记录的可见性。

所以还是需要回到聚簇索引中来：

根据二级索引维护的主键值去聚簇索引中查找记录（使用MVCC规则）

如果查出来的结果跟二级索引里维护的结果相同 -> 返回，如果不同 -> 丢弃

如果对于一条查询语句，二级索引中有很多条满足条件的结果（连续多次更新，导致二级索引中有很多条记录），那上面这个流程就比较低效了。所以InnoDB的作者搞了个机智的小优化：

> 在二级索引中，用一个额外的名为**MAX_TRX_ID**的变量来记录最后一次更新二级索引的事务的ID

那么，如果当前语句关联的read_view的 up_limit_id > MAX_TRX_ID，说明在创建read_view时最后一次更新二级索引的事务已经结束，也就是说二级索引里的所有记录对于当前查询都是可见的，此时可以直接根据二级索引的deleted flag来确定记录是否应该被返回。

小结一下：二级索引的MVCC可见性判断在MAX_TRX_ID失效的情况下需要依赖聚簇索引才能完成

6. purge清除老的记录

从前面的分析可以看出，为了实现InnoDB的MVCC机制，更新或者删除操作都只是设置一下老记录的deleted_bit，并不真正将过时的记录删除。

为了节省磁盘空间，InnoDB有专门的purge线程来清理deleted_bit为true的记录。

为了不影响MVCC的正常工作，purge线程自己也维护了一个read view（**这个read view相当于系统中最老活跃事务的read view**）

如果某个记录的deleted_bit为true，并且DB_TRX_ID相对于purge线程的read view可见，那么这条记录一定是可以被安全清除的。

#### undolog



### 事务

a collection of queries 比如account deposit（select，update，update）

begin tx1

​        select balance from account where id = 1

​        update account set balance = balance - 100 where ID= 1

​         update account set balance = balance  + 100 where ID= 2

commit tx1

事务四个特性：acid atomicity，consistency，isolation，durability

1. **原子性**：全部的query都要执行，有一个fail就需求全部roll back（回滚）

2. **一致性**：事务开始前和结束后，数据库的完整性约束没有被破坏。

   consisitency in data

   原子性，隔离性保证一致性，用户定义的，foreign keys，比如图片点赞可以不一致

   consistency in reads

   如果一个transaction提交了一个变化，另一个新事物是不是可以立刻看到变化？

   sql/nosql也不行，因为有多个server replica，只好最终一致性

   

3. **隔离性**：一个事务正在执行可不可以看到其他事务的改变？？

   读情况：

1. 脏读：事务A读取了事务B更新的数据，然后B回滚操作，那么A读取到的数据是脏数据

2. 不可重复读：事务A多次读取同一数据，事务B在事务A多次读取的过程中，对数据作了更新并提交，导致事务A多次读取同一数据时，结果不一致。（针对 update ）

3. 幻读：A事务读取了B事务已经提交的新增数据。注意和不可重复读的区别，这里是 insert 新增（或删除），不可重复读是更改。select某记录是否存在，不存在，准备插入此记录，但执行 insert 时发现此记录已存在，无法插入，此时就发生了幻读。

   更新情况： 

   更新丢失：lost update 当两个或多个事务选择同一行，然后基于最初选定的值更新该行时，由于每个事务都不知道其他事务的存在，就会发生丢失更新问题



| 事务隔离级别                                                 | 脏读 | 不可重复读 | 幻读 |
| ------------------------------------------------------------ | ---- | ---------- | ---- |
| 读未提交 （read uncommitted ）no isolation, any change from the outside is visible to transaction | 可能 | 可能发生   | 可能 |
| 不可重复读 (Read committed) each query in transaction only sees committed stuff | 不会 | 可能       | 可能 |
| 可重复读(Repeatable read):each query in a transaction only sees committed updates before this transaction start | 不会 | 不会       | 可能 |
| 串行化 (Serializable) transactions are serialized 慢         | 不会 | 不会发生   | 不会 |

锁机制：阻止其他事务对数据进行操作， 各个隔离级别主要体现在读取数据时加的锁的释放时机。

- RU：事务读取时不加锁
- RC：事务读取时加行级共享锁（读到才加锁），一旦读完，立刻释放（并不是事务结束）。
- RR：事务读取时加**行级共享锁**，直到事务结束时，才会释放。
- SE：事务读取时加**表级共享锁**，直到事务结束时，才会释放。

4.持久性：事务完成后，事务对数据库的所有更新将被保存到数据库，数据库断电也不能丢



### herbinates



### SQL执行顺序

SQL的执行顺序：from---where--group by---having---select---order by

### sql 优化

1.使用连接池？

1. TCP建立连接的三次握手；
2. MySQL认证的三次握手；
3. 真正的SQL执行；
4. MySQL的关闭；
5. TCP的四次握手关闭；

调用流程为：

- 应用数据层向DataSource请求数据库连接
- DataSource使用数据库Driver打开数据库连接
- 创建数据库连接，打开TCP socket
- 应用读/写数据库
- 如果该连接不再需要就关闭连接
- 关闭socket

从客户端的角度来说，使用长连接有一个好处，可以不用每次创建新连接，若客户端对MySQL服务器的连接请求很频繁，永久连接将更加高效。对于高并发业务，如果可能会碰到连接的冲击，推荐使用长连接或连接池

原理：无论何时请求一个连接，池数据源会从可用的连接池获取新连接。仅当没有可用的连接而且未达到最大的连接数时连接池将创建新的连接。close()方法把连接返回到连接池而不是真正地关闭它。

2.连接池的大小怎么选择？

如果我们无视磁盘和网络，那么结论就非常简单。在一个8核的服务器上，设定连接/线程数为8能够提供最优的性能，再增加连接数就会因上下文切换的损耗导致性能下降。

在这一时间段（即"I/O等待"）内，线程是在“阻塞”着等待磁盘，此时操作系统可以将那个空闲的CPU核心用于服务其他线程。所以，由于线程总是在I/O上阻塞，我们可以让线程/连接数比CPU核心多一些，这样能够在同样的时间内完成更多的工作。应该多多少呢？ 取决于磁盘，如果磁盘比较快，意味着阻塞比较少，意味着不需要多太多了。**连接数 = ((核心数 \* 2) + 有效磁盘数)**

公理：你需要一个小连接池，和一个充满了等待连接的线程的队列 
如果你有10000个并发用户，设置一个10000的连接池是非常不明智的。1000仍然很恐怖。即是100也太多了。你需要一个10来个连接的小连接池，然后让剩下的业务线程都在队列里等待。连接池中的连接数量应该等于你的数据库能够有效同时进行的查询任务数（通常不会高于2*CPU核心数）

2. sql语句设计不合理

**1.保证不查询多余的列与行。**

- 尽量避免select * 的存在，使用具体的列代替*，避免多余的列
- 使用where限定具体要查询的数据，避免多余的行
- 使用top，distinct关键字减少多余重复的行

**2.慎用distinct关键字**

distinct在查询一个字段或者很少字段的情况下使用，会避免重复数据的出现，给查询带来优化效果。

但是查询字段很多的情况下使用，则会大大降低查询效率

3. where id=1 or id = 2 -> where id in（1，2，3，4）

**5.连接查询的优化**

首先你要弄明白你想要的数据是什么样子的，然后再做出决定使用哪一种连接，这很重要。

各种连接的取值大小为：

- 内连接结果集大小取决于左右表满足条件的数量

- 左连接取决与左表大小，右相反。

- 完全连接和交叉连接取决与左右两个表的数据总数量

  

**1.查看执行时间和cpu占用时间**

```
set statistics time on
select * from dbo.Product
set statistics time off
```

2. **查看查询对I/0的操作情况**

```
set statistics io on
select * from dbo.Product
set statistics io off
```

3. 索引

4. **批处理(batch)指的是一次操作中执行多条SQL语句，批处理相比于一次一次执行效率会提高很多。**

   **批处理操作数据库的过程主要是分两步：**

   - 将要执行的SQL语句保存
   - 执行保存的SQL语句

### 性能为什么会下降

为了调和 CPU 和磁盘的速度不匹配，MySQL 用 buffer pool 来加载磁盘数据到一段连续的内存中，供读写使用。一般情况下，如果缓冲池足够大，能够放下所有数据页，那 mysql 操作基本不会产生读 IO，而写 IO 是异步的，不会影响读写操作。

**Buffer pool 不够大，数据页不在里面该怎么办？**

去磁盘中读取，将磁盘文件中的数据页加载到 buffer pool 中，那么就需要等待物理 IO 的同步读操作完成，如果此时 IO 没有及时响应，则会被堵塞。因为读写操作需要数据页在 buffer 中才能进行，所以必须等待操作系统完成 IO，否则该线程无法继续后续的步骤。

**热点数据，当新的会话线程也需要去访问相同的数据页怎么办？**

会等待上面的线程将这个数据页读入到缓存中 buffer pool。如果第一个请求该数据页的线程因为磁盘 IO 瓶颈，迟迟没有将物理数据页读入 buffer pool, 这个时间区间拖得越长，则造成等待该数据块的用户线程就越多。对高并发的系统来说，将造成大量的等待。

**高并发，大量请求的访问行为被阻塞，会造成什么后果？**

对于服务来说，大量超时会使服务器处于不可用的状态。该台机器会触发熔断。熔断触发后，该机器的流量会打到其他机器，其他机器发生类似的情况的可能性会提高，极端情况会引起所有服务宕机，曲线掉底。

---so 缓存

### 数据库访问量很大怎么办？

- 一个是sql语句必须得优化，不然会加重数据库服务器的负担
- 数据库连接池
- 主从复制，读写分离，负载均衡。
- 数据库分表，分区，分库
- +缓存

垂直拆分

 在主键和一些列放在一个表中，然后把主键和另外的列放在另一个表中。如果一个表中某些列常用，而另外一些不常用，则可以采用垂直拆分。

水平拆分

  根据一列或者多列数据的值把数据行放到两个独立的表中。

分区就是把一张表的数据分成多个区块，这些区块可以在一个磁盘上，也可以在不同的磁盘上，分区后，表面上还是一张表，但是数据散列在多个位置，这样一来，多块硬盘同时处理不同的请求，从而提高磁盘**I/O读写性能。**实现比较简单，包括水平分区和垂直分区。

***\*注意：\****分库分表最难解决的问题是统计，还有跨表的连接（比如这个表的订单在另外一张表），解决这个的方法就是使用中间件，比如大名鼎鼎的***\*MyCat\****，用它来做路由，管理整个分库分表，乃至跨库跨表的连接

# redis

### redis可以用来干嘛？

1. 缓存
2. 共享Session
3. 消息队列系统
4. 分布式锁

### Redis 的数据结构及使用场景

1. String字符串:字符串类型是 Redis 最基础的数据结构，首先键都是字符串类型，而且 其他几种数据结构都是在字符串类型基础上构建的，我们常使用的 set key value 命令就是字符串。常用在缓存、计数、共享Session、限速等。

   ```
   redis 127.0.0.1:6379> SET runoobkey redis
   OK
   redis 127.0.0.1:6379> GET runoobkey
   "redis"
   ```

2. Hash哈希:在Redis中，哈希类型是指键值本身又是一个键值对结构，哈希可以用来存放用户信息，比如实现购物车。redis的哈希对象的底层存储可以使用ziplist（压缩列表）和hashtable。（什么时候用ziplist：哈希对象保存的所有键值对的键和值的字符串长度都小于64字节， 或者，哈希对象保存的键值对数量小于512个）

   ```
   127.0.0.1:6379> hset person name jack
   (integer) 1
   127.0.0.1:6379> hset person age 20
   (integer) 1
   127.0.0.1:6379> hset person sex famale
   (integer) 1
   127.0.0.1:6379> hgetall person
   1) "name"
   2) "jack"
   3) "age"
   4) "20"
   5) "sex"
   6) "famale"
   127.0.0.1:6379> hkeys person
   1) "name"
   2) "age"
   3) "sex"
   127.0.0.1:6379> hvals person
   1) "jack"
   2) "20"
   3) "famale"
   ```

   

3. List列表（双向链表）:列表（list）类型是用来存储多个有序的字符串。twitter的关注列表、粉丝列表, 可以做简单的消息队列的功能。

 ```
 redis 127.0.0.1:6379> lpush list1 redis
 (integer) 1
 redis 127.0.0.1:6379> lpush list1 hello
 (integer) 2
 redis 127.0.0.1:6379> rpush list1 world
 (integer) 3
 redis 127.0.0.1:6379> llen list1
 (integer) 3
 redis 127.0.0.1:6379> lrange list1 0 3
 1) "hello"
 2) "redis"
 3) "world"
 redis 127.0.0.1:6379> lpop list1
 "hello"
 redis 127.0.0.1:6379> rpop list1
 "world"
 redis 127.0.0.1:6379> lrange list1 0 3
 1) "redis"
 ```



4. Set集合：Redis set对外提供的功能与list类似是一个列表的功能，特殊之处在于set是可以自动排重的，当你需要存储一个列表数据，又不希望出现重复数据时，set是一个很好的选择，并且set提供了判断某个成员是否在一个set集合内的重要接口，这个也是list所不能提供的。

   又或者在微博应用中，每个用户关注的人存在一个集合中，就很容易实现求两个人的共同好友功能。

```
redis> SADD myset "Hello"
(integer) 1
redis> SADD myset "World"
(integer) 1
redis> SMEMBERS myset
1) "World"
2) "Hello"
redis> SADD myset "one"
(integer) 1
redis> SISMEMBER myset "one"
(integer) 1
redis> SISMEMBER myset "two"
(integer) 0
```



5. Sorted Set有序集合（跳表实现）：Sorted Set 多了一个权重参数 Score，集合中的元素能够按 Score 进行排列。比如twitter 的public timeline可以以发表时间作为score来存储，这样获取时就是自动按时间排好序的。

   又比如用户的积分排行榜需求就可以通过有序集合实现。

   还有上面介绍的使用List实现轻量级的消息队列，其实也可以通过Sorted Set实现有优先级或按权重的队列。

   ```
   redis 127.0.0.1:6379> zadd dbs 100 redis
   (integer) 1
   redis 127.0.0.1:6379> zadd dbs 98 memcached
   (integer) 1
   redis 127.0.0.1:6379> zadd dbs 99 mongodb
   (integer) 1
   redis 127.0.0.1:6379> zadd dbs 99 leveldb
   (integer) 1
   redis 127.0.0.1:6379> zcard dbs
   (integer) 4
   redis 127.0.0.1:6379> zcount dbs 10 99
   (integer) 3
   redis 127.0.0.1:6379> zrank dbs leveldb
   (integer) 1
   redis 127.0.0.1:6379> zrank dbs other
   (nil)
   redis 127.0.0.1:6379> zrangebyscore dbs 98 100
   1) "memcached"
   2) "leveldb"
   3) "mongodb"
   4) "redis"
   ```

   

### 如何保证高可用？

1.哨兵模式

2.可以自动分片的redis cluster

### 哨兵模式

sentinel是redis高可用的解决方案，sentinel系统可以监视一个或者多个redis master服务，以及这些master服务的所有从服务；当某个master服务下线时，自动将该master下的某个从服务升级为master服务替代已下线的master服务继续处理请求，集群中的其他redis服务器自动指向新的master同步数据

1.多个哨兵node组成哨兵系统防止单点，至少三个

2. 每个Sentinel以每秒钟一次的频率向它所知的Master，Slave以及其他 Sentinel 实例发送一个PING命令
3. 如果一个实例（instance）距离最后一次有效回复PING命令的时间超过 own-after-milliseconds 选项所指定的值，则这个实例会被Sentinel标记为主观下线。
4. 如果一个Master被标记为主观下线，则正在监视这个Master的所有 Sentinel 要以每秒一次的频率确认Master的确进入了主观下线状态
5. 当有足够数量的Sentinel（大于等于配置文件指定的值）在指定的时间范围内确认Master的确进入了主观下线状态，则Master会被标记为客观下线

### cluster集群模式

多个由主从节点群组成的服务器群，分布式存储，可以水平扩展，每台redis节点存储不同的内容，任意两个节点之间都是相互联通的，客户端可以与任何一个节点连接，然后就可以访问集群中的任何一个节点，对其进行存取和其他操作。

特点：

- 所有的 redis 节点彼此互联，内部使用二进制协议优化传输速度和带宽。
- 节点的 fail 是通过集群中超过半数的节点检测失效时才生效。
- 客户端与 Redis 节点直连，不需要中间代理层.客户端不需要连接集群所有节点，连接集群中任何一个可用节点即可

集群的数据分片：

Redis 集群没有使用一致性 hash，而是引入了哈希槽【hash slot】的概念。

Redis 集群有16384 个哈希槽，每个 key 通过 CRC16 校验后对 16384 取模来决定放置哪个槽。集群的每个节点负责一部分hash槽，举个例子，比如当前集群有3个节点，那么：

- 节点 A 包含 0 到 5460 号哈希槽

- 节点 B 包含 5461 到 10922 号哈希槽

- 节点 C 包含 10923 到 16383 号哈希槽

因为从一个节点向另一个节点移动hash slot并不需要停止工作。所以添加/删除节点，或者改变节点持有hash slot的百分比，都不需要任何停机时间。

redis集群subset主从复制模型：abc是主节点，a1 a2，b1 b2，c1 c2 

为了保证高可用，redis-cluster集群引入了主从复制模型，一个主节点对应一个或者多个从节点，当主节点宕机的时候，就会启用从节点。当其它主节点 ping 一个主节点 A 时，如果半数以上的主节点与 A 通信超时，那么认为主节点 A 宕机了。如果主节点 A 和它的从节点 A1 都宕机了，那么该集群就无法再提供服务了。

redis节点之间互联？

每个节点有两个tcp端口，一个正常port for 服务客户端，一个port也叫bus port for cluster bus，for node to node communication，二进制协议

strong consistency一致性不保证：异步写的过程

- Your client writes to the master B.
- The master B replies OK to your client.
- The master B propagates the write to its replicas B1, B2 and B3. （延迟丢失数据）

trade-off to be made between performance and consistency （同步写）

### redis数据分片

why 1. 不被限制在单服务器的内存容量 2. 允许多服务器进行可扩展、可伸缩

根据范围来分片：根据不同的业务

根据hash分片：连续性要求不高，也就不能连续查询了。

1. 客户端分片，客户端使用一致性hash算法决定key分布到哪一个redis节点上

   缺点：静态的分片方案，增加/减少redis实例需要人工调整；可维护性差；

2. 代理分片：客户端请求发到代理，由代理请求找到正确的节点

3. 服务端分片：客户端发送查询到一个随机实例，这个实例会保证转发你的查询到正确节点，Redis集群在客户端的帮助下，实现了查询路由的一种混合形式(请求不是直接从redis实例转发到另一个，而是客户端收到重定向以后的节点，再次发送请求到正确的redis实例)

- 涉及多个key的操作通常是不被支持的。举例来说，当两个set映射到不同的redis实例上时，你就不能对这两个set执行交集操作。
- 涉及多个key的redis事务不能使用。
- 当使用分区时，数据处理较为复杂，比如你需要处理多个rdb/aof文件，并且从多个实例和主机备份持久化文件。

###  redis zset如何实现？



### Redis hashmap如何实现

比java的hashmap简单很多啊，组织结构跟jdk1.7的hashmap挺类似的，都是由数组跟链表组成，实际存放数据的对象为一个dictEntry对象对应到HashMap就是Entry对象，对比jdk1.7的hashmap多了一些冗余字段比如sizemask、used等，最大区别就是存放dictEntry的数组对象有两个,且哈希表的负载因子大于等于1

VS java hashmap

回顾一下hashmap的扩容过程，简单点来说就是需要复制一个新的数组，然后把旧数组内的元素进行rehash，然后把元素重新插入到新的数组中。因为resize操作是一次性，集中式完成的，当hashmap的数组大小为初始容量16时，整个resize过程还是可控的，而经过多次扩容后，数组的元素变多，进行resize的时候操作元素也增多，resize所需要的时间就不可控了。

所以:

而redis作为高性能缓存，从结构设计上就需要避免这种操作时间不可控的场景存在，而采取的策略就是喜闻乐见的用空间换时间了，所以能看到dict中包含了两个dictht的数组。

步骤：

1. 为ht[1]分配空间，让字典同时持有ht[0]和ht[1]两个hash表
2. 在字典中维持一个索引计数器变量rehashidx，并将它的值设置为0，表示rehash工作正式开始
3. 在rehash进行期间，每次对字典执行添加，删除，查找或者更新操作时，程序除了执行特定的操作以外，还会顺带将ht[0]哈希表在rehashidx索引上的所有键值对rehash到ht[1],当rehash工作完成之后，程序将rehashidx属性的值增1
4. 随着字典操作的不断执行，最终在某个时间点上，ht[0]的所有键值对都会被rehash至ht[1]，这时程序将rehashidx属性的值设为-1，表示rehash操作已完成

由于多了一个dictht维护，当哈希表的负载因子小于0.1时，还会对哈希表进行缩容的操作，操作的过程跟渐进式rehash是一致的

**总结一下跟jdk的hashmap的区别**

1. 数据结构上，采用了两个数组保存数据，发生hash冲突时，只采用了链地址法解决hash冲突，并没有跟jdk1.8一样当链表超过8时优化成红黑树，因此插入元素时跟jdk1.7的hashmap一样采用的是头插法。
2. 在发生扩容时，跟jdk的hashmap一次性、集中式进行扩容不一样，采取的是渐进式的rehash，每次操作只会操作当前的元素，在当前数组中移除或者存放到新的数组中，直到老数组的元素彻底变成空表。
3. 当负载因子小于0.1时，会自动进行缩容。jdk的hashmap出于性能考虑，不提供缩容的操作。
4. redis使用MurmurHash来计算哈希表的键的hash值，而jdk的hashmap使用key.hashcode()的高十六位跟低十六位做与运算获得键的hash值。

MurmurHash 是一种非 加密型 哈希函数，适用于一般的哈希检索操作，对于规律性较强的key，MurmurHash的随机分布特征表现更良好

### Redis的LRU具体实现：

传统的LRU是使用栈的形式，每次都将最新使用的移入栈顶，但是用栈的形式会导致执行select * 的时候大量非热点数据占领头部数据，所以需要改进。Redis每次按key获取一个值的时候，都会更新value中的lru字段为当前秒级别的时间戳（意思是，LRU是用sorted set 来实现的）。Redis初始的实现算法很简单，随机从dict中取出五个key,淘汰一个lru字段值最小的。在3.0的时候，又改进了一版算法，首先第一次随机选取的key都会放入一个pool中(pool的大小为16),pool中的key是按lru大小顺序排列的。接下来每次随机选取的key lru值必须小于pool中最小的lru才会继续放入，直到将pool放满。放满之后，每次如果有新的key需要放入，需要将pool中lru最大的一个key取出（最大的意思是，score最大，意味着时间戳最大，很可能是刚刚用过的，所以可以幸免于难）。淘汰的时候，直接从pool中选取一个lru最小的值然后将其淘汰（那这个时候，说明这个pool里面这个还是最早之前使用，最近可能一直没用过）。

### 单线程的Redis为什么快

1. 纯内存操作
2. 单线程操作，避免了频繁的上下文切换
3. 合理高效的数据结构
4. 采用了非阻塞I/O多路复用机制（有一个文件描述符同时监听多个文件描述符是否有数据到来）同步非阻塞的`epoll`

### redis 事务

Redis 事务可以一次执行多个命令，就是批量的执行脚本

- 批量操作在发送 EXEC 命令前被放入队列缓存。
- 收到 EXEC 命令后进入事务执行，事务中任意命令执行失败，其余的命令依然被执行。
- 在事务执行过程，其他客户端提交的命令请求不会插入到事务执行命令序列中。

一个事务从开始到执行会经历以下三个阶段：

- 开始事务。
- 命令入队。
- 执行事务。

单个 Redis 命令的执行是原子性的，但 Redis 没有在事务上增加任何维持原子性的机制，所以 Redis 事务的执行并不是原子性的。

### redis管道技术

对于单线程阻塞式的Redis，Pipeline可以满足批量的操作，把多个命令连续的发送给Redis Server，然后一一解析响应结果。Pipelining可以提高批量处理性能，提升的原因主要是TCP连接中减少了“交互往返”的时间。pipeline 底层是通过把所有的操作封装成流，redis有定义自己的出入输出流。在 sync() 方法执行操作，每次请求放在队列里面，解析响应包。

### redis 持久化

第一种方式：RDB方式的持久化是通过快照的方式完成的。当符合某种规则时，会将内存中的数据全量生成一份副本存储到硬盘上，这个过程称作”快照”， 快照文件存储在Redis当前进程的工作目录的dump.rdb（硬盘上）

1. Redis使用fork函数复制一份当前进程（父进程）的副本（子进程）；
2. 父进程继续处理来自客户端的请求，子进程开始将内存中的数据写入硬盘中的临时文件；
3. 当子进程写完所有的数据后，用该临时文件替换旧的RDB文件，至此，一次快照操作完成

Redis启动时会自动读取RDB快照文件，将数据从硬盘载入到内存，根据数量的不同，这个过程持续的时间也不尽相同，通常来讲，一个记录1000万个字符串类型键，大小为1GB的快照文件载入到内存需要20-30秒的时间。

第二种方式append only file：在使用Redis存储非临时数据时，一般都需要打开AOF持久化来降低进程终止导致的数据丢失，AOF可以将Redis执行的每一条写命令追加到硬盘文件中，这已过程显然会降低Redis的性能，但是大部分情况下这个影响是可以接受的，另外，使用较快的硬盘能提高AOF的性能。

第三种：rdb+aof

第四种：不持久化

### Redis和memcached的区别

1. 存储方式上：memcache会把数据全部存在内存之中，断电后会挂掉，数据不能超过内存大小。redis有部分数据存在硬盘上，这样能保证数据的持久性。
2. 数据支持类型上：memcache对数据类型的支持简单，只支持简单的key-value，，而redis支持五种数据类型。
3. 用底层模型不同：它们之间底层实现方式以及与客户端之间通信的应用协议不一样。redis直接自己构建了VM机制，因为一般的系统调用系统函数的话，会浪费一定的时间去移动和请求。
4. value的大小：redis可以达到1GB，而memcache只有1MB。

### redis 做消息队列



### Redis并发竞争key的解决方案

**问题描述：**多客户端同时并发写一个key，可能本来应该先到的数据后到了，导致数据版本错了。或者是多客户端同时获取一个key，修改值之后再写回去，只要顺序错了，数据就错了

1. 分布式锁+时间戳

这种情况，主要是准备一个分布式锁，大家去抢锁，加锁的目的实际上就是把并行读写改成串行读写的方式，从而来避免资源竞争。利用SETNX非常简单地实现分布式锁。

时间戳：由于key的操作需要顺序执行，所以需要保存一个时间戳判断顺序。假设系统B先抢到锁，将key1设置为{ValueB 7:05}。接下来系统A抢到锁，发现自己的key1的时间戳早于缓存中的时间戳（7:00<=7:05），那就不做set操作了。

2.利用消息队列



# 系统设计

### 负载均衡

#### LVS+Keepalive

LVS 特点是：

1. 首先它是基于 4 层的网络协议的，抗负载能力强，对于服务器的硬件要求除了网卡外，其他没有太多要求；
2. 配置性比较低，这是一个缺点也是一个优点，因为没有可太多配置的东西，大大减少了人为出错的几率；
3. 应用范围比较广，不仅仅对 web 服务做负载均衡，还可以对其他应用（mysql）做负载均衡；
4. LVS 架构中存在一个虚拟 IP 的概念，需要向 IDC 多申请一个 IP 来做虚拟 IP。

在 lvs+keepalived 环境里面，lvs 主要的工作是提供调度算法，把客户端请求按照需求调度在 real 服务器，keepalived 主要的工作是提供 lvs 控制器的一个冗余，并且对 real 服务器做健康检查，发现不健康的 real 服务器，就把它从 lvs 集群中剔除，real 服务器只负责提供服务。

keepalived 通过选举（看服务器设置的权重）挑选出一台热备服务器做 MASTER 机器，MASTER 机器会被分配到一个指定的虚拟 ip，外部程序可通过该 ip 访问这台服务器，如果这台服务器出现故障（断网，重启，或者本机器上的 keepalived crash 等），keepalived 会从其他的备份机器上重选（还是看服务器设置的权重）一台机器做 MASTER 并分配同样的虚拟 IP，充当前一台 MASTER 的角色。

#### Nginx

特点是：

1. 工作在网络的 7 层之上，可以针对 http 应用做一些分流的策略，比如针对域名、目录结构；
2. Nginx 安装和配置比较简单，测试起来比较方便；
3. 也可以承担高的负载压力且稳定，一般能支撑超过上万次的并发；
4. Nginx 可以通过端口检测到服务器内部的故障，比如根据服务器处理网页返回的状态码、超时等等，并且会把返回错误的请求重新提交到另一个节点，不过其中缺点就是不支持 url 来检测；
5. Nginx 对请求的异步处理可以帮助节点服务器减轻负载；
6. Nginx 能支持 http 和 Email，这样就在适用范围上面小很多；
7. 默认有三种调度算法: 轮询、weight 以及 ip_hash（可以解决会话保持的问题），还可以支持第三方的 fair 和 url_hash 等调度算法；

负载均衡的几种常用方式

1、轮询（默认）

每个请求按时间顺序逐一分配到不同的后端服务器，如果后端服务器down掉，能自动剔除

upstream backserver {
    server 192.168.0.14;
    server 192.168.0.15;
}

2.weight

指定轮询几率，weight和访问比率成正比，用于后端服务器性能不均的情况。

upstream backserver {
    server 192.168.0.14 weight=3;
    server 192.168.0.15 weight=7;
}

3.ip_hash

上述方式存在一个问题就是说，在负载均衡系统中，假如用户在某台服务器上登录了，那么该用户第二次请求的时候，因为我们是负载均衡系统，每次请求都会重新定位到服务器集群中的某一个，那么***已经登录某一个服务器的用户再重新定位到另一个服务器，其登录信息将会丢失，这样显然是不妥的\***
我们可以采用***ip_hash\***指令解决这个问题，如果客户已经访问了某个服务器，当用户再次访问时，会将该请求通过***哈希算法，自动定位到该服务器\***。
每个请求按访问ip的hash结果分配，这样每个访客固定访问一个后端服务器，可以解决***session的问题\***

upstream backserver {
    ip_hash;
    server 192.168.0.14:88;
    server 192.168.0.15:80;
}

4.fair（第三方）

按后端服务器的响应时间来分配请求，响应时间短的优先分配。

5.url_hash（第三方）

按访问url的hash结果来分配请求，使每个url定向到同一个（对应的）后端服务器，后端服务器为缓存时比较有效。

### 微服务容错模式

在使用了微服务架构后，整体的业务被拆成小的微服务，并组合在一起对外提供服务、微服务之间使用轻量级的网络协议通信，通常是restful风格的远程调用。由于服务之间调用不再是进程内的调用，而是通过网络进行远程调用，网络不可靠，不稳定，一个服务依赖的服务可能出错、超时或者宕机，如果没有及时的发现和隔离问题，或者在设计中没有考虑如何应对这样的问题，那么可能短时间内服务的线程池中的线程被用满，资源耗尽，导致雪崩效应。解决方案如下：

#### 1.舱壁隔离模式

1）微服务容器分组

负载均衡（分流）----------分组服务1、分组服务2、分组服务3（容器1、容器2、容器3）

一些社交平台将名人的自媒体流量全部路由到服务的名人池里面、而普通用户流量路由到另一个服务池中，有效的隔离了普通用户和重要用户的负载。

2）线程池隔离

拆分适可而止，有时候将同一个类功能分在一个微服务里面，导致多个功能混合部署在一个微服务实例里面，如果这个高微服务的不同的功能使用一个线程池，导致一个功能流量增加耗尽线程池的线程，阻塞其他功能的服务。

#### 2.熔断模式

熔断器模式其实就是对服务的调用做了一层代理，对最近服务固定时间段调用错误次数进行统计，如果达到指定次数，则直接返回失败，并允许再接下的时间段内允许个别调用者真实调用服务，如果成功则认为服务已正常，允许后面服务的正常调用，否则继续返回失败。

**Hystrix是Netflix公司开源的防雪崩的利器，是一个帮助解决分布式系统交互时超时处理和容错的类库, 拥有保护系统的能力。**

闭合（closed）状态： 对应用程序的请求能够直接引起方法的调用。代理类维护了最近调用失败的次数，如果某次调用失败，则使失败次数加1。如果最近失败次数超过了在给定时间内允许失败的阈值，则代理类切换到断开(Open)状态。此时代理开启了一个超时时钟，当该时钟超过了该时间，则切换到半断开（Half-Open）状态。该超时时间的设定是给了系统一次机会来修正导致调用失败的错误。

断开(Open)状态：在该状态下，对应用程序的请求会立即返回错误响应。

半断开（Half-Open）状态：允许对应用程序的一定数量的请求可以去调用服务。如果这些请求对服务的调用成功，那么可以认为之前导致调用失败的错误已经修正，此时熔断器切换到闭合状态(并且将错误计数器重置)；如果这一定数量的请求有调用失败的情况，则认为导致之前调用失败的问题仍然存在，熔断器切回到断开方式，然后开始重置计时器来给系统一定的时间来修正错误。半断开状态能够有效防止正在恢复中的服务被突然而来的大量请求再次拖垮

#### 3. 限流模式

服务突然上量对于飞速发展的平台也是常有的事情，必须有限流机制。限流机制一般都是控制访问并发量，例如每秒钟允许处理的并发用户数以及查询量、请求量。

限流方法 

1）计数器

计数器固定窗口算法是最基础也是最简单的一种限流算法。原理就是对一段固定时间窗口内的请求进行计数，如果请求数超过了阈值，则舍弃该请求；如果没有达到设定的阈值，则接受该请求，且计数加1。当时间窗口结束时，重置计数器为0。

优点：实现简单，容易理解。

缺点：

1.一段时间内（不超过时间窗口）系统服务不可用。比如窗口大小为1s，限流大小为100，然后恰好在某个窗口的第1ms来了100个请求，然后第2ms-999ms的请求就都会被拒绝，这段时间用户会感觉系统服务不可用。

2.窗口切换时可能会产生两倍于阈值流量的请求。比如窗口大小为1s，限流大小为100，然后恰好在某个窗口的第999ms来了100个请求，窗口前期没有请求，所以这100个请求都会通过。再恰好，下一个窗口的第1ms有来了100个请求，也全部通过了，那也就是在2ms之内通过了200个请求，而我们设定的阈值是100，通过的请求达到了阈值的两倍

2）漏斗算法

请求来了之后会首先进到漏斗里，然后漏斗以恒定的速率将请求流出进行处理，从而起到平滑流量的作用。当请求的流量过大时，漏斗达到最大容量时会溢出，此时请求被丢弃。从系统的角度来看，我们不知道什么时候会有请求来，也不知道请求会以多大的速率来，这就给系统的安全性埋下了隐患。但是如果加了一层漏斗算法限流之后，就能够保证请求以恒定的速率流出。在系统看来，请求永远是以平滑的传输速率过来，从而起到了保护系统的作用。

缺点：**不能解决流量突发的问题**。还是拿刚刚测试的例子，我们设定的漏斗速率是2个/秒，然后突然来了10个请求，受限于漏斗的容量，只有5个请求被接受，另外5个被拒绝。

3）令牌桶算法

在令牌桶算法中，存在一个令牌桶，算法中存在一种机制以恒定的速率向令牌桶中放入令牌。令牌桶也有一定的容量，如果满了令牌就无法放进去了。当请求来时，会首先到令牌桶中去拿令牌，如果拿到了令牌，则该请求会被处理，并消耗掉拿到的令牌；如果令牌桶为空，则该请求会被丢弃。

**令牌桶算法**作为漏斗算法的一种改进，除了能够起到平滑流量的作用，还允许一定程度的流量突发。

比较：

令牌桶算法一般用于保护自身的系统，对调用者进行限流，保护自身的系统不被突发的流量打垮。如果自身的系统实际的处理能力强于配置的流量限制时，可以允许一定程度的流量突发，使得实际的处理速率高于配置的速率，充分利用系统资源。

漏斗算法一般用于保护第三方的系统，比如自身的系统需要调用第三方的接口，为了保护第三方的系统不被自身的调用打垮，便可以通过漏斗算法进行限流，保证自身的流量平稳的打到第三方的接口上。

#### 4.失效转移模式

若微服务中发生了熔断和限流，该如何处理被拒绝的请求呢？

1.采用快速失败的策略，直接返回使用方法错误，让使用方知道发生了什么自行判断

2.是否有备份服务，如果有备份服务，迅速切换到备份

3.失败的服务可能是某台机器失败，而不是全部的机器，failover策略，然后重试。

### 微服务框架技术

#### RPC

RPC 全称 Remote Procedure Call——远程过程调用

为什么需要RPC?

1、首先要明确一点：RPC可以用HTTP协议实现，并且用HTTP是建立在 TCP 之上最广泛使用的 RPC，但是互联网公司往往用自己的私有协议，比如鹅厂的JCE协议，私有协议不具备通用性为什么还要用呢？因为相比于HTTP协议，RPC采用二进制字节码传输，更加高效也更加安全。
2、现在业界提倡“微服务“的概念，而服务之间通信目前有两种方式，RPC就是其中一种。RPC可以保证不同服务之间的互相调用。即使是跨语言跨平台也不是问题，让构建分布式系统更加容易。
3、RPC框架都会有服务降级、流量控制的功能，保证服务的高可用

1)用Protobuf优化数据序列化

数据序列化方法有很多种方法，常见的有Avro，Thrift,，XML，JSON，Protocol Buffer等工具。本文主要介绍的是Protobuf。Protobuf 全称““Protocol Buffer”” 是google 推出的高性能序列化工具。现已经在Github上[开源](https://link.jianshu.com/?t=https%3A%2F%2Fgithub.com%2Fgoogle%2Fprotobuf)。Protobuf采用tag来标识字段序号，用varint 和zigzag两种编码方式对整形做特殊的处理，Protobuf序列化后的数据紧凑，而且序列化时间短

2)用Netty优化I/O模型,Netty 正是采用了第三种 I/O多路复用的方法

JDK RMI:JDk 内置的

Hessian序列化为二进制协议,Burlap使用xml数据，适合大规模高并发的短小请求

String HTTP Invoker：基于rmi http通道

#### Dubbo

阿里巴巴开源的分布式服务框架、高性能和透明化的RPC远程服务调用方案

**Provider**: 暴露服务的服务提供方。 
**Consumer**: 调用远程服务的服务消费方。 
**Registry**: 服务注册与发现的注册中心。 
**Monitor**: 统计服务的调用次数和调用时间的监控中心。

调用流程 
0.服务容器负责启动，加载，运行服务提供者。 
1.服务提供者在启动时，向注册中心注册自己提供的服务。 
2.服务消费者在启动时，向注册中心订阅自己所需的服务。 
3.注册中心返回服务提供者地址列表给消费者，如果有变更，注册中心将基于长连接推送变更数据给消费者。 
4.服务消费者，从提供者地址列表中，基于软负载均衡算法，选一台提供者进行调用，如果调用失败，再选另一台调用。 
5.服务消费者和提供者，在内存中累计调用次数和调用时间，定时每分钟发送一次统计数据到监控中心

dubbo注册中心：通过将服务统一管理起来，可以有效地优化内部应用对服务发布/使用的流程和管理。服务注册中心可以通过特定协议来完成服务对外的统一。

可选：Multicast注册中心、Zookeeper注册中心、Redis注册中心、Simple注册中心

HFS也是淘宝的不开源，比dubbo好

Thrift 最初是由 Facebook 开发,允许定义一个简单的定义文件中的数据类型和服务接口无缝跨编程语言。

#### Spring Boot

#### spring cloud netflix



### 系统高可用

硬件出现故障应视为必然的，而**高可用的系统架构设计目标就是要保证当出现硬件故障时，服务依然可用，数据依然能够保存并被访问**。**实现高可用的系统架构的主要手段是数据和服务的冗余备份及失效转移**，一旦某些服务器宕机，就将服务切换到其他可用的服务器上；如果磁盘损坏，则从备份的磁盘读取数据

- 高可用的应用 - 主要手段是：负载均衡
- 高可用的服务 - 主要手段是：分级管理、超时重试、异步调用、限流、降解、断路、幂等性设计
- 高可用的数据 - 主要手段是：数据备份和失效转移

#### 可用性指标

1. **网络问题**。网络链接出现问题，网络带宽出现拥塞……
2. **性能问题**。数据库慢 SQL、Java Full GC、硬盘 IO 过大、CPU 飙高、内存不足……
3. **安全问题**。被网络攻击，如 DDoS 等。
4. **运维问题**。系统总是在被更新和修改，架构也在不断地被调整，监控问题……
5. **管理问题**。没有梳理出关键服务以及服务的依赖关系，运行信息没有和控制系统同步……
6. **硬件问题**。硬盘损坏、网卡出问题、交换机出问题、机房掉电、挖掘机问题……

网站不可用时间 = 故障修复时间点 - 故障发现时间点
网站年度可用性指标 = (1 - 网站不可用时间/年度总时间) * 100%

系统不可用也被称作系统故障，业界通常用多个 9 来衡量系统的可用性，90%不可用，99%基本可用99.9%较高可用，99.99%高可用

#### 存储高可用

**1）主备复制**

主备复制是最常见也是最简单的一种存储高可用方案，几乎所有的存储系统都提供了主备复制的功能，例如 MySQL、Redis、MongoDB 等。

主备复制要点：存在一主多备、主机负责读&写，并定期复制数据给备机、一旦主机宕机，可以通过人工手段，将其中一个备节点作为主节点。

优点：

主备复制架构中，客户端可以不感知备机的存在。即使灾难恢复后，原来的备机被人工修改为主机后，对于客户端来说，只是认为主机的地址换了而已，无须知道是原来的备机升级为主机

主备复制架构中，主机和备机之间，只需要进行数据复制即可，无须进行状态判断和主备切换这类复杂的操作。

缺点：主备复制架构中，故障后需要人工干预，无法自动恢复。

**2）主从复制**

主从复制和主备复制只有一字之差，区别在于：主从复制模式中，从机要承担读操作。

优点：

主从复制架构中，主机故障时，读操作相关的业务可以继续运行。
主从复制架构中，从机提供读操作，发挥了硬件的性能。

缺点：从机提供读业务，如果主从复制延迟比较大，业务会因为数据不一致出现问题，故障后需要人工干预，无法自动恢复。

**3）集群+分区**

在主备复制和主从复制模式中，都由一个共性问题：

每个机器上存储的都是全量数据。但是，单机的数据存储量总是有上限的，当数据量上升为 TB 级甚至 PB 级数据，单机终究有无法支撑的时候。这时，就需要对数据进行分片（sharding）。

分片后的节点可以视为一个独立的子集，针对子集，任然需要保证高可用。

#### 服务高可用

**1）无状态应用的失效转移可以利用负载均衡来实现**

当单台服务器不足以承担所有的负载压力时，通过负载均衡手段，将流量和数据分摊到一个集群组成的多台服务器上，以提高整体的负载处理能力。

无状态的应用实现高可用架构十分简单，由于服务器不保存请求状态，那么所有服务器完全对等，在任意节点执行同样的请求，结果总是一致的。这种情况下，最简单的高可用方案就是使用负载均衡。

**2）有状态应用利用分布式session**

应用服务器的高可用架构设计主要基于服务无状态这一特性。事实上，业务总是有状态的，如购物车记录用户的购买信息；用户的登录状态；最新发布的消息等等。

在分布式场景下，一个用户的 Session 如果只存储在一个服务器上，那么当负载均衡器把用户的下一个请求转发到另一个服务器上，该服务器没有用户的 Session，就可能导致用户需要重新进行登录等操作。

为了解决分布式 Session 问题，常见的解决方案有：

**方法一：客户端存储，其实就是cookie**

直接将信息存储在cookie中，cookie是存储在客户端上的一小段数据，客户端通过http协议和服务器进行cookie交互，通常用来存储一些不敏感信息

缺点：数据存储在客户端，存在安全隐患；如果一次请求cookie过大，会给网络增加更大的开销

**方法一：使用nginx进行session绑定**

我们利用nginx的反向代理和负载均衡，之前是客户端会被分配到其中一台服务器进行处理，具体分配到哪台服务器进行处理还得看服务器的负载均衡算法(轮询、随机、ip-hash、权重等)，但是我们可以基于nginx的`ip-hash策略`，可以对客户端和服务器进行绑定，同一个客户端就只能访问该服务器，无论客户端发送多少次请求都被同一个服务器处理

缺点：容易造成单点故障，如果有一台服务器宕机，那么该台服务器上的session信息将会丢

**方法三：基于redis存储session方案**

这是企业中使用的最多的一种方式、spring为我们封装好了spring-session，直接引入依赖即可、数据保存在redis中，无缝接入，不存在任何安全隐患

缺点：多了一次网络调用，web容器需要向redis访问

#### 系统监控

- 监控数据采集

  - 用户行为日志收集
    - 服务端日志收集 - Apache、Nginx 等几乎所有 Web 服务器都具备日志记录功能，只要开启日志记录即可。如果是服务器比较多，需要集中采集日志，通常会使用 Elastic 来进行收集。
    - 客户端日志收集 - 利用页面嵌入专门的 JavaScript 脚本可以收集用户真实的操作行为。
    - 日志分析 - 可以利用 ElasticSearch 做语义分析及搜索；利用实时计算框架 Storm、Flink 等开发日志统计与分析工具。
  - **服务器性能监控** - 收集服务器性能指标，如系统负载、内存占用、CPU 占用、磁盘 IO、网络 IO 等。常用的监控工具有：Apache SkyWalking、Pinpoint等。
  - **运行数据报告** - 应该监控一些与具体业务场景相关的技术和业务指标，如：缓存命中率、平均响应时延、TPS、QPS 等。

- 监控管理

  - **系统报警** - 设置阈值。当达到阈值，及时触发告警（短信、邮件、通信工具均可），通过及时判断状况，防患于未然。

  - **失效转移** - 监控系统可以在发现故障的情况下主动通知应用进行失效转移。

  - 自动优雅降级

    - 优雅降级是为了应付突然爆发的访问高峰，主动关闭部分功能，释放部分资源，以保证核心功能的优先访问。
    - 系统在监控管理基础之上实现自动优雅降级，是柔性架构的理想状态

    

    

    log4j？？？？？？？

### 分布式系统一致性

#### 前提：拆分、分而治之

水平拆分：指单一节点无法满足性能要求，需要扩展多个节点，多个节点具有一致的功能，组成一个服务池，一个节点服务一部分的请求，所有的节点共同处理大规模的高并发请求量。

垂直拆分：按照功能划分，秉承“专业的人干专业的事”将一个复杂的功能拆分成多个单一、简单的功能，不同的单一功能组合在一起，和未拆分前完成的功能一样，各个模块维护和变更容易简单安全

#### 出现的场景

**案例一：下订单和扣库存**

电商系统中有一个经典的案例，既下订单和扣库存如何保持一致。如果先下订单，扣库存失败，会导致超卖；

如果订单不成功，扣库存成功导致少卖；

**案例二：同步调用超时**

因为网络问题，服务可能调用超时，系统a调用系统b超时时，系统a可能明确得到超时反馈，但是无法确定系统b是否已经完成了预设的功能，于是系统a不知道应该做什么，如何反馈给使用方。

**案例三：异步回调超时**

受理模式下，系统a同步调用系统b，然后系统b是受理模式，受理之后就会返回成功信息，然后系统b处理后异步通知系统a处理结果。如果系统a由于某种原因迟迟没有处理回调结果，那么两个系统之间状态不同，互相认知的状态也不一致。

**案例四：掉单**

两个系统互为上下游，一个系统存在一个请求（通常指订单）另一个系统不存在，则会掉单

**案例五：系统间的状态不一致**

不同的两个系统之间都存在请求，但是请求的状态不一致。

**案例六：缓存和数据不一致**

交易系统离不开关系型数据库，因为依赖关系型数据库事务acid特性，但是大规模、高并发的互联网系统中，一些特殊的场景对读操作性能要求极高，数据库难以抗住大规模的读流量，会加一层缓存，缓存和数据库之间的数据一致性如何？

**案例七：本地缓存节点不一致**

一个服务池上有多个节点，为了满足较高的性能要求，会使用本地缓存，这样每个节点都会有一份缓存数据的复制，如果这些数据是静态的那就没什么问题，但如果是动态的需要更新的，则每个节点的更新有先后顺序，在更新的瞬间，某个事件窗口各个节点的数据是不一致的。

**案例八：缓存数据结构不一致**

这个案例有时候发生，某系统需要在缓存中暂存某种类型的数据，该数据由多个数据元素组成，其中，某个数据元素需要从数据库或者服务中获取，如果一部分数据元素获取失败，还是将部分数据存入缓存，然后缓存使用者拿到这个不完整的数据抛出一些没有写处理模块的异常，程序出错。

#### ACID

数据量比较小的情况下，可以用关系型数据库的强一致性来解决，订单表和库存表放在一个关系型数据库。

但对于大规模高并发，单机无法满足需求，单机关系型数据库也不能满足存储和性能需求，尽量保证订单和库存放在同一个数据库分片，通过关系型数据库解决了不一致的问题

但是事与愿违，由于业务规则限制，我们无法将相关数据分到同一个数据库分片，这时就需要最终一致性。

#### CAP

CAP 原则又称 CAP 定理，指的是在一个分布式系统中， Consistency（一致性）、 Availability（可用性）、Partition tolerance（分区容错性），三者不可得兼。

一致性（C）：在分布式系统中的所有数据备份，在同一时刻是否同样的值。（等同于所有节点访问同一份最新的数据副本）

可用性（A）：在集群中一部分节点故障后，集群整体是否还能响应客户端的读写请求。（对数据更新具备高可用性）

分区容错性（P）：以实际效果而言，分区相当于对通信的时限要求。

关系型数据库单点无复制，不具备分区容忍性----CA

分布式的服务化系统都符合P, 必须就当前操作在 C 和 A 之间做出选择。

如果在网络上有消息丢失，也就是出现了网络分区，则复制操作可能会被延后，如果这时候我们的使用方等待复制完成在返回，可能导致有限时间内无法返回，失去了可用性；‘

如果不等复制完成，而在主分片写完直接返回，则具有可用性，但是去了一致性。

#### BASE

BASE思想于ACID思想截然不同，它满足CAP原理，通过牺牲强一致性获得可用性，一般用应用在服务化系统的应用层or大数据处理系统中，通过达到最终一致性来尽量满足业务的绝大数需求。

BA：Basically Available 基本可用，分布式系统在出现故障的时候，允许损失部分可用性，即保证核心可用。
S：Soft State 软状态，允许系统存在中间状态，而该中间状态不会影响系统整体可用性。
E：Consistency 最终一致性，系统中的所有数据副本经过一定时间后，最终能够达到一致的状态。

软状态是实现BASE思想的方法，基本可用和最终一致性是目标。处理请求的过程中可能出现短暂的不一致，在短暂的不一致的事件窗口内，请求处理处于临时状态中，系统在进行每步操作时，通过记录每个临时状态在系统出现故障可以从中间状态继续处理未完成的请求或者退回原始状态。

####  最终一致性解决方案

**1.查询模式**

任何服务操作都需要提供一个查询接口，用来向外部输出操作执行的状态，服务操作的使用方可以通过查询接口得知服务操作的状态，然后根据不同的状态来做不同的处理。（补偿未完成的操作还是回滚已完成的操作）

为了实现查询，每个服务都要有一个唯一的流水号标识id，比如请求流水号，订单号。

查询模式下，服务模块包括：正常操作api（id）、查询（id）、批量查询（ids）

针对案例二-案例五，了解被调用服务的处理情况，决定下一步做什么，例如补偿或者回滚

**2.补偿模式**

有了查询的模式，在任何情况下，我们可以知道具体操作所处的状态，如果操作处于不正常的状态，我们需要修正操作中有问题的子操作，可能重新执行未完成的子操作或者取消已经完成的子操作。

补偿模式下，服务模块包括：操作：id、重新操作（id）、取消操作（id）

**针对同步调用情况**：

如果业务操作发起方还没有收到业务操作执行方的明确返回或者调用超时，这时业务发起方需要及时调用业务执行方查询业务操作执行的状态；得到状态之后，如果执行方已经完成，则业务发起方向业务使用方返回成功；如果查询状态失败，则立即告诉业务使用方失败，快速失败，然后调用业务操作的逆向操作，保证操作不被执行或者回滚已经执行的操作，以保证最终一致性。

分类：

自动恢复：程序根据不一致的情况，通过继续进行未完成的操作，回滚已经完成的操作，来自动达到一致。

通知运营：如果程序无法恢复，并且设计时考虑到不一致的场景，则可以提供运营功能，让运营手工补偿。

技术运行：最糟的情况就是进行数据库的更新，代码的变更，尽量避免这种场景。

**3.异步确保模式**

对响事件要求不高的场景，可以对高并发的流量进行消峰，例如，电商系统中对物流，配送，以及支付系统中的技术，入账等。

将这类操作从主流程中摘除，然后通过异步的方式进行处理，将处理后的结果通知给使用方。

方案三适合

**4.定时校对模式**

-如何发现需要补偿操作呢？
首先，需要一个分布式的全局唯一id

主流程操作1---------->主流程操作2------------->主流程操作3

​         ｜——————       ｜    ————————  ｜

​                             第三方核对系统

从第三方的角度来监控服务执行的健康程度、针对方案4、5

**5.可靠消息模式**

1）消息的可靠发送（保证消息一定发送出去，也就是重试）

第1种，发送消息之前持久化在数据库，标记为待发送，然后发送消息，如果发送成功，则将消息改为发送成功。

定时任务从数据库捞取一定时间内未发送的消息并将消息发送

第2种，不同的是持久消息的数据库是独立的，并不耦合在业务系统中。发送消息前，先发一个预消息给某个第三方消息管理器，消息管理器将其持久到数据库，并标记为待发送，发送成功后，标记消息为发送成功。定时任务从数据库中捞出一定时间内未发送的消息，查询业务系统是否继续发送，根据查询结果来确定消息的状态。

2）消息的幂等

有了重试机制之后，消息一定重复，那我们需要对重复的问题进行处理，比如：

保证数据库表的唯一健进行过滤重复，拒绝重复的请求；

使用分布式的表来滤重；

**6.缓存一致性模式**

针对经典的缓存模式：

1）如果性能要求不高，尽可能使用分布式的缓存，而不是本地的缓存；

2）写缓存的时候数据一定要完整，如果缓存数据一部分有效，另一部分无效，宁可在需要的时候回源数据库而不是吧部分数据放在缓存里；

3）使用缓存牺牲了一致性，为了提高性能，数据库和缓存只需要保持一个弱一致性，而不是强的一致性，否则也违背了缓存的初衷

4）读的顺序是先读缓存，后读数据库，写的顺序是先写数据库，再写缓存。



### 分布式事务

事务acid属性；分布式事务是指事务的参与者、支持事务的服务器、资源服务器以及事务管理器分别位于不同的分布式系统的不同节点之上；例如在大型电商系统中，下单接口通常会扣减库存、减去优惠、生成订单 id, 而订单服务与库存、优惠、订单 id 都是不同的服务，下单接口的成功与否，不仅取决于本地的 db 操作，而且依赖第三方系统的结果，这时候分布式事务就保证这些操作要么全部成功，要么全部失败。本质上来说，分布式事务就是为了保证不同数据库的数据一致性。

#### 柔性事务

不同于 ACID 的刚性事务，在分布式场景下基于 BASE 理论，就出现了柔性事务的概念。要想通过柔性事务来达到最终的一致性，就需要依赖于一些特性，这些特性在具体的方案中不一定都要满足，因为不同的方案要求不一样；但是都不满足的话，是不可能做柔性事务的。

#### 幂等操作

在编程中一个幂等操作的特点是其任意多次执行所产生的影响均与一次执行的影响相同。幂等函数，或幂等方法，是指可以使用相同参数重复执行，并能获得相同结果的函数。这些函数不会影响系统状态，也不用担心重复执行会对系统造成改变。例如，支付流程中第三方支付系统告知系统中某个订单支付成功，接收该支付回调接口在网络正常的情况下无论操作多少次都应该返回成功。

#### 分布式事务使用场景

“两个操作A和B,需要先执行在执行B，如果A成功高了，但B失败了怎么办?“

最简单就是在A里面那条数据多存一个marker先设置成False，当B操作成功之后再标记换成true

这种情况怎么处理a里面的这条数据呢？lazy的方法就是get all marker=true

坏处就是：如果操作b过程比较慢，会有一些latency

1.转账

转账是最经典那的分布式事务场景，假设用户 A 使用银行 app 发起一笔跨行转账给用户 B，银行系统首先扣掉用户 A 的钱，然后增加用户 B 账户中的余额。此时就会出现 2 种异常情况：1. 用户 A 的账户扣款成功，用户 B 账户余额增加失败 2. 用户 A 账户扣款失败，用户 B 账户余额增加成功。对于银行系统来说，以上 2 种情况都是不允许发生，此时就需要分布式事务来保证转账操作的成功。

2.下单扣库存

在电商系统中，下单是用户最常见操作。在下单接口中必定会涉及生成订单 id, 扣减库存等操作，对于微服务架构系统，订单 id 与库存服务一般都是独立的服务，此时就需要分布式事务来保证整个下单接口的成功。

3.同步超时

继续以电商系统为例，在微服务体系架构下，我们的支付与订单都是作为单独的系统存在。订单的支付状态依赖支付系统的通知，假设一个场景：我们的支付系统收到来自第三方支付的通知，告知某个订单支付成功，接收通知接口需要同步调用订单服务变更订单状态接口，更新订单状态为成功。流程图如下，从图中可以看出有两次调用，第三方支付调用支付服务，以及支付服务调用订单服务，这两步调用都可能出现调用超时的情况，此处如果没有分布式事务的保证，就会出现用户订单实际支付情况与最终用户看到的订单支付情况不一致的情况。

第三方支付--------支付服务-------订单服务

#### 分布式事务的解决方案

一：两阶段提交/XA

准备阶段：协调者向参与者发出指令，参与者评估自己的状态，如果参与者评估指令可以完成，则会写redo或者undolog，然后锁定资源，执行完成但是不提交

提交阶段：如果每个参与者明确返回准备成功，也就是预留了资源和执行操作成功，则协调者向参与者发出提交指令，参与者提交资源变更的事务，释放锁定的资源，如果任何一个参与者明确返回失败，也就是预留资源或者执行操作失败，则协调者向参与者发出中止指令，参与者取消已经变更的事务，执行undo日志释放锁定的资源。

带来的问题：

1.阻塞，对于任何的指令都必须说到明确的回应才能进入下一步，负责处于阻塞状态，占用的资源一直锁定，不会释放。

2.单点故障：如果协调者宕机，参与者没有协调者指挥就会一直阻塞，尽量可以通过选举新的协调者代替原来的协调者，但是如果协调者在发送一个指令后宕机，而提交指令仅仅被一个参与者接受，参与者接受后也宕机，则新上任的协调者无法处理这种情况

3.脑裂：协调者发送提交指令，有的参与者接受，有的没有接收到，多个参与者之间不一致。

“两阶段可以保证系统的强一致性，但是出现异常需要人工干预解决，可用性不够好”

二：三阶段提交

“超时机制解决了阻塞的问题，发生超时参与者和协调者都会默认成功（根据概率统计决定的）“

询问阶段：协调者询问参与者是否可以完成指令，参与值只需要回答是或者否，不需要真正的操作，这个阶段超时会被中止。

准备阶段：两阶段一样，增加了超时

提交阶段：一样，增加了超时

三：TCC 需要事务接口提供 try, confirm, cancel 三个接口，提高了编程的复杂性。依赖于业务方来配合提供这样的接口，推行难度大，所以一般不推荐使用这种方式。

但是tcc是简化版的三阶段提交协议，解决了两阶段协议的阻塞问题，但没有解决极端情况下的脑裂和不一致问题，然后tcc通过自动化补偿的方式，将人工处理的不一致情况降到最低，也算有用。

在秒杀场景下：

用户发起订单请求，应用层先检查库存，确认商品还有余量，则锁定库存，此时订单状态为待支付，然后指引用户去支付，如果支付失败，或者支付超时，系统会自动将锁定的库存解锁，以供其他用户去秒杀。

### 分布式锁

- 分布式与单机情况下最大的不同在于其不是多线程而是**多进程**。
- 多线程由于可以共享堆内存，因此可以简单的采取内存作为标记存储位置。而进程之间甚至可能都不在同一台物理机上，因此需要将标记存储在一个所有进程都能看到的地方。
- 主要就是需要考虑到**网络的延时和不可靠**。

​    这个锁可以放在公共内存比如redis、memcache里面。只要能保证互斥就可以了。

我们需要怎样的分布式锁？

- 可以保证在分布式部署的应用集群中，同一个方法在同一时间只能被一台机器上的一个线程执行。
- 这把锁要是一把可重入锁（避免死锁）
- 这把锁最好是一把阻塞锁（根据业务需求考虑要不要这条）
- 这把锁最好是一把公平锁（根据业务需求考虑要不要这条）
- 有高可用的获取锁和释放锁功能
- 获取锁和释放锁的性能要好

#### 基于redis的分布式锁

-------setnx()

setnx 的含义就是 SET if Not Exists，其主要有两个参数 setnx(key, value)。该方法是原子的，如果 key 不存在，则设置当前 key 成功，返回 1；如果当前 key 已经存在，则设置当前 key 失败，返回 0。

-------expire()

expire 设置过期时间，要注意的是 setnx 命令不能设置 key 的超时时间，只能通过 expire() 来对 key 设置。

方法一：

1、setnx(lockkey, 1) 如果返回 0，则说明占位失败；如果返回 1，则说明占位成功

2、expire() 命令对 lockkey 设置超时时间，为的是避免死锁问题。

3、执行完业务代码后，可以通过 delete 命令删除 key。

方法一的问题：如果在第一步 setnx 执行成功后，在 expire() 命令执行成功前，发生了宕机的现象，那么就依然会出现死锁的问题

方法二：

--------getset()

这个命令主要有两个参数 getset(key，newValue)。该方法是原子的，对 key 设置 newValue 这个值，并且返回 key 原来的旧值。假设 key 原来是不存在的，那么多次执行这个命令，会出现下边的效果

1. getset(key, "value1") 返回 null 此时 key 的值会被设置为 value1
2. getset(key, "value2") 返回 value1 此时 key 的值会被设置为 value2
3. 依次类推！

步骤：

1. setnx(lockkey, 当前时间+过期超时时间)，如果返回 1，则获取锁成功；如果返回 0 则没有获取到锁，转向 2。
2. get(lockkey) 获取值 oldExpireTime ，并将这个 value 值与当前的系统时间进行比较，如果小于当前系统时间，则认为这个锁已经超时，可以允许别的请求重新获取，转向 3。
3. 计算 newExpireTime = 当前时间+过期超时时间，然后 getset(lockkey, newExpireTime) 会返回当前 lockkey 的值currentExpireTime。
4. 判断 currentExpireTime 与 oldExpireTime 是否相等，如果相等，说明当前 getset 设置成功，获取到了锁。如果不相等，说明这个锁又被别的请求获取走了，那么当前请求可以直接返回失败，或者继续重试。
5. 在获取到锁之后，当前线程可以开始自己的业务处理，当处理完毕后，比较自己的处理时间和对于锁设置的超时时间，如果小于锁设置的超时时间，则直接执行 delete 释放锁；如果大于锁设置的超时时间，则不需要再锁进行处理。

#### zookeeper 做分布式锁

zk 基本锁

- 原理：利用临时节点与 watch 机制。每个锁占用一个普通节点 /lock，当需要获取锁时在 /lock 目录下创建一个临时节点，创建成功则表示获取锁成功，失败则 watch/lock 节点，有删除操作后再去争锁。临时节点好处在于当进程挂掉后能自动上锁的节点自动删除即取消锁。
- 缺点：所有取锁失败的进程都监听父节点，很容易发生羊群效应，即当释放锁后所有等待进程一起来创建节点，并发量很大。

zk 锁优化

- 原理：上锁改为创建临时有序节点，每个上锁的节点均能创建节点成功，只是其序号不同。只有序号最小的可以拥有锁，如果这个节点序号不是最小的则 watch 序号比本身小的前一个节点 (公平锁)。
- 步骤：
- 在 /lock 节点下创建一个有序临时节点 (EPHEMERAL_SEQUENTIAL)。
- 判断创建的节点序号是否最小，如果是最小则获取锁成功。不是则取锁失败，然后 watch 序号比本身小的前一个节点。
- 当取锁失败，设置 watch 后则等待 watch 事件到来后，再次判断是否序号最小。
- 取锁成功则执行代码，最后释放锁（删除该节点）



### 关系型数据库 vs 非关系型数据库

**总结：数据库与NoSql及各种NoSql间的对比**



![img](https://img2018.cnblogs.com/blog/801753/201908/801753-20190810232930008-331448438.png)

第一点，不多解释应该都理解，非关系型数据库都是通过牺牲了ACID特性来获取更高的性能的，假设两张表之间有比较强的一致性需求，那么这类数据是不适合放在非关系型数据库中的。

第二点，核心数据不走非关系型数据库，例如用户表、订单表，但是这有一个前提，就是这一类核心数据会有多种查询模式，例如用户表有ABCD四个字段，可能根据AB查，可能根据AC查，可能根据D查，假设核心数据，但是就是个KV形式，比如用户的聊天记录，那么HBase一存就完事了。

非核心数据尤其是日志、流水一类中间数据千万不要写在关系型数据库中，这一类数据通常有两个特点：

- 写远高于读
- 写入量巨大

一旦使用关系型数据库作为存储引擎，将大大降低关系型数据库的能力，正常读写QPS不高的核心服务会受这一类数据读写的拖累。

接着是第二个问题，如果我们使用非关系型数据库作为存储引擎，那么如何选型？其实上面的文章基本都写了，这里只是做一个总结（所有的缺点都不会体现事务这个点，因为这是所有NoSql相比关系型数据库共有的一个问题）：

![img](https://img2018.cnblogs.com/blog/801753/201908/801753-20190812094840816-785471233.png)

——————————————————————————————————————————————————

关系型数据库优点：

- **易理解**

　　因为行 + 列的二维表逻辑是非常贴近逻辑世界的一个概念，关系模型相对网状、层次等其他模型更加容易被理解

- **操作方便**

　　通用的SQL语言使得操作关系型数据库非常方便，支持join等复杂查询，Sql + 二维关系是关系型数据库最无可比拟的优点，这种易用性非常贴近开发者

- **数据一致性**

　　支持ACID特性，可以维护数据之间的一致性，这是使用数据库非常重要的一个理由之一，例如同银行转账，张三转给李四100元钱，张三扣100元，李四加100元，而且必须同时成功或者同时失败，否则就会造成用户的资损

- **数据稳定**

　　数据持久化到磁盘，没有丢失数据风险，支持海量数据存储

- **服务稳定**

　　最常用的关系型数据库产品MySql、Oracle服务器性能卓越，服务稳定，通常很少出现宕机异常

关系型数据库的缺点：

- **高并发下IO压力大**

　　数据按行存储，即使只针对其中某一列进行运算，也会将整行数据从存储设备中读入内存，导致IO较高

- **为维护索引付出的代价大**

　　为了提供丰富的查询能力，通常热点表都会有多个二级索引，一旦有了二级索引，数据的新增必然伴随着所有二级索引的新增，数据的更新也必然伴随着所有二级索引的更新，这不可避免地降低了关系型数据库的读写能力，且索引越多读写能力越差。有机会的话可以看一下自己公司的数据库，除了数据文件不可避免地占空间外，索引占的空间其实也并不少

- **为维护数据一致性付出的代价大**

　　数据一致性是关系型数据库的核心，但是同样为了维护数据一致性的代价也是非常大的。我们都知道SQL标准为事务定义了不同的隔离级别，从低到高依次是读未提交、读已提交、可重复度、串行化，事务隔离级别越低，可能出现的并发异常越多，但是通常而言能提供的并发能力越强。那么为了保证事务一致性，数据库就需要提供并发控制与故障恢复两种技术，前者用于减少并发异常，后者可以在系统异常的时候保证事务与数据库状态不会被破坏。对于并发控制，其核心思想就是加锁，无论是乐观锁还是悲观锁，只要提供的隔离级别越高，那么读写性能必然越差

- **水平扩展后带来的种种问题难处理**

　　前文提过，随着企业规模扩大，一种方式是对数据库做分库，做了分库之后，数据迁移（1个库的数据按照一定规则打到2个库中）、跨库join（订单数据里有用户数据，两条数据不在同一个库中）、分布式事务处理都是需要考虑的问题，尤其是分布式事务处理，业界当前都没有特别好的解决方案

- **表结构扩展不方便**

　　由于数据库存储的是结构化数据，因此表结构schema是固定的，扩展不方便，如果需要修改表结构，需要执行DDL（data definition language）语句修改，修改期间会导致锁表，部分服务不可用

- **全文搜索功能弱**

　　例如like "%中国真伟大%"，只能搜索到"2019年中国真伟大，爱祖国"，无法搜索到"中国真是太伟大了"这样的文本，即不具备分词能力，且like查询在"%中国真伟大"这样的搜索条件下，无法命中索引，将会导致查询效率大大降低

写了这么多，我的理解核心还是前三点，它反映出的一个问题是**关系型数据库在高并发下的能力是有瓶颈的**，尤其是写入/更新频繁的情况下，出现瓶颈的结果就是数据库CPU高、Sql执行慢、客户端报数据库连接池不够等错误，因此例如万人秒杀这种场景，我们绝对不可能通过数据库直接去扣减库存。

————————————————————————————————————————————

**KV型NoSql（代表----Redis，MemCache）**

KV型NoSql最大的优点就是**高性能**，利用Redis自带的BenchMark做基准测试，TPS可达到10万的级别，性能非常强劲。

比较明显的缺点：

- 只能根据K查V，无法根据V查K
- 查询方式单一，只有KV的方式，不支持条件查询，多条件查询唯一的做法就是数据冗余，但这会极大的浪费存储空间
- 内存是有限的，无法支持海量数据存储
- 由于KV型NoSql的存储是基于内存的，会有丢失数据的风险

综上所述，KV型NoSql最合适的场景就是**缓存**的场景：

- 读远多于写
- 读取能力强
- 没有持久化的需求，可以容忍数据丢失，反正丢了再查询一把写入就是了

—————————————————————————————————————————————————

**搜索型NoSql（代表----ElasticSearch）**

传统关系型数据库主要通过索引来达到快速查询的目的，但是在全文搜索的场景下，索引是无能为力的，like查询一来无法满足所有模糊匹配需求，二来使用限制太大且使用不当容易造成慢查询，**搜索型NoSql的诞生正是为了解决关系型数据库全文搜索能力较弱的问题**，ElasticSearch是搜索型NoSql的代表产品

​	全文搜索的原理是**倒排索引**，我们看一下什么是倒排索引。要说倒排索引我们先看下什么是正排索引，传统的正排索引是**文档-->关键字**的映射，例如"Tom is my friend"这句话，会将其切分为"Tom"、"is"、"my"、"friend"四个单词，在搜索的时候对文档进行扫描，符合条件的查出来。这种方式原理非常简单，但是由于其检索效率太低，基本没什么实用价值。

倒排索引则完全相反，它是**关键字-->文档**的映射，我用张表格展示一下就比较清楚了：

![img](https://img2018.cnblogs.com/blog/801753/201908/801753-20190810164641874-1306125222.png)

意思是我现在这里有四个短句：

- "Tom is Tom"
- "Tom is my friend"
- "Thank you, Betty"
- "Tom is Betty's husband"

搜索引擎会根据一定的切分规则将这句话切成N个关键字，并以关键字的维度维护关键字在每个文本中的出现次数。这样下次搜索"Tom"的时候，由于Tom这个词语在"Tom is Tom"、"Tom is my friend"、"Tom is Betty's husband"三句话中都有出现，因此这三条记录都会被检索出来，且由于"Tom is Tom"这句话中"Tom"出现了2次，因此这条记录对"Tom"这个单词的匹配度最高，最先展示。这就是**搜索引擎倒排索引的基本原理**，假设某个关键字在某个文档中出现，那么倒排索引中有两部分内容：

- 文档ID
- 在该文档中出现的位置情况

因此，搜索型NoSql最适用的场景就是**有条件搜索尤其是全文搜索的场景**，作为关系型数据库的一种替代方案。

另外，搜索型数据库还有一种特别重要的应用场景。我们可以想，一旦对数据库做了分库分表后，原来可以在单表中做的聚合操作、统计操作是否统统失效？例如我把订单表分16个库，1024张表，那么订单数据就散落在1024张表中，我想要统计昨天浙江省单笔成交金额最高的订单是哪笔如何做？我想要把昨天的所有订单按照时间排序分页展示如何做？**这就是搜索型NoSql的另一大作用了，我们可以把分表之后的数据统一打在搜索型NoSql中，利用搜索型NoSql的搜索与聚合能力完成对全量数据的查询**。

——————————————————————————————————————————————————

**文档型NoSql（代表----MongoDB）**

因此，对于MongDB，我们只要理解成一个Free-Schema的关系型数据库就完事了，它的优缺点比较一目了然，优点：

- 没有预定义的字段，扩展字段容易
- 相较于关系型数据库，读写性能优越，命中二级索引的查询不会比关系型数据库慢，对于非索引字段的查询则是全面胜出

缺点在于：

- 不支持事务操作
- 多表之间的关联查询不支持（虽然有嵌入文档的方式），join查询还是需要多次操作
- 空间占用较大，这个是MongDB的设计问题，空间预分配机制 + 删除数据后空间不释放，只有用db.repairDatabase()去修复才能释放
- 目前没发现MongoDB有关系型数据库例如MySql的Navicat这种成熟的运维工具

### redis消息队列处理高并发



### 高并发带来的问题

在同时或极短时间内，有大量的请求到达服务端，每个请求都需要服务端耗费资源进行处理，并做出相应的反馈。

服务端处理请求需要耗费服务端的资源，比如能同时开启的进程数、能同时运行的线程数、网络连接数、cpu、I/O、内存等等，由于服务端资源是有限的，那么服务端能同时处理的请求也是有限的
高并发问题的本质就是：资源的有限性

高并发带来的问题：服务端的处理和响应会越来越慢，甚至会丢弃部分请求不予处理，更严重的会导致服务端崩溃。

前端请求、Web服务器、Web应用、数据库等

```
服务端的处理基本原则是：分而治之，并提高单个请求的处理速度
```

### 高并发系统的设计与实现

在开发高并发系统时有三把利器用来保护系统：缓存、降级和限流。

* 缓存：缓存比较好理解，在大型高并发系统中，如果没有缓存数据库将分分钟被爆，系统也会瞬间瘫痪。使用缓存不单单能够提升系统访问速度、提高并发访问量，也是保护数据库、保护系统的有效方式。大型网站一般主要是“读”，缓存的使用很容易被想到。在大型“写”系统中，缓存也常常扮演者非常重要的角色。比如累积一些数据批量写入，内存里面的缓存队列（生产消费），以及HBase写数据的机制等等也都是通过缓存提升系统的吞吐量或者实现系统的保护措施。甚至消息中间件，你也可以认为是一种分布式的数据缓存。
* 降级：服务降级是当服务器压力剧增的情况下，根据当前业务情况及流量对一些服务和页面有策略的降级，以此释放服务器资源以保证核心任务的正常运行。降级往往会指定不同的级别，面临不同的异常等级执行不同的处理。根据服务方式：可以拒接服务，可以延迟服务，也有时候可以随机服务。根据服务范围：可以砍掉某个功能，也可以砍掉某些模块。总之服务降级需要根据不同的业务需求采用不同的降级策略。主要的目的就是服务虽然有损但是总比没有好。
* 限流：限流可以认为服务降级的一种，限流就是限制系统的输入和输出流量已达到保护系统的目的。一般来说系统的吞吐量是可以被测算的，为了保证系统的稳定运行，一旦达到的需要限制的阈值，就需要限制流量并采取一些措施以完成限制流量的目的。比如：延迟处理，拒绝处理，或者部分拒绝处理等等。

### 高并发-缓存

#### Redis的热点key解决方案

1. 服务端缓存：即将热点数据缓存至服务端的内存中.（利用Redis自带的消息通知机制来保证Redis和服务端热点Key的数据一致性，对于热点Key客户端建立一个监听，当热点Key有更新操作的时候，服务端也随之更新。)
2. 备份热点Key：即将热点Key+随机数，随机分配至Redis其他节点中。这样访问热点key的时候就不会全部命中到一台机器上了

#### Redis与Mysql双写一致性方案

- 第一种： **先更新数据库，再更新缓存 no**

问题1: 脏读：

1）线程A更新了数据库

2）线程B更新了数据库

3）线程B更新了缓存

4）线程A更新了缓存

问题2: 读多写少的情况，浪费

- 第二种：先删除缓存，再更新数据库 no

（1）请求A进行写操作，删除缓存

（2）请求B查询发现缓存不存在

   3）请求B去数据库查询得到旧值

   4）请求B将旧值写入缓存

  5）请求A将新值写入数据库 

 上述情况就会导致不一致的情形出现。而且，如果不采用给缓存设置过期时间策略，该数据永远都是脏数据。

- 第三种： 先更新数据库，再删除缓存，也是cache aside pattern

1. **失效**：应用程序先从cache取数据，没有得到，则从数据库中取数据，成功后，放到缓存中。
2. **命中**：应用程序从cache中取数据，取到后返回。
3. **更新**：先把数据存到数据库中，成功后，再让缓存失效。

（1）缓存刚好失效

（2）请求A查询数据库，得一个旧值

（3）请求B将新值写入数据库

（4）请求B删除缓存

（5）请求A将查到的旧值写入缓存

数据库的读操作的速度远快于写操作的，很少发生！

#### 如何解决 Redis 缓存穿透问题

问题：查询的是数据库中不存在的数据，没有命中缓存而数据库查询为空，也不会更新缓存。导致每次都查库，如果不加处理，遇到恶意攻击，会导致数据库承受巨大压力，直至崩溃。

一种是遇到查询为空的，就缓存一个空值到缓存，不至于每次都进数据库。

二是布隆过滤器，提前判断是否是数据库中存在的数据，若不在则拦截。

#### 布隆过滤

基于hash算法和位数组bit array的，有误判率。如果它说不在，那一定不在，如果它说在，有可能不在。

优点：空间效率高，hashfunction没关系，并行操作，时间效率高。

​             不需要储存数据本身，保密高。

缺点：不能删除，数据越多误判率越低。

【0001000001000100】将zero 的三个hash函数，hash1，hash2， hash3的位置都放入1，

判断的时候，如果这三个位置都是1，那么就是存在（有可能误判，1可能是别的one存进去的）

#### 如何解决 Redis 缓存击穿问题

缓存起初时起作用的。发生的场景是某些热点 key 的缓存失效导致大量热点请求打到数据库，导致数据库压力陡增，甚至宕机。

1. 一种是热点 key 不过期
2. 第二种是从执行逻辑上进行限制。

1.请求redis，肯定没有

2.大家抢锁 o（只有发生redis取不到的时候）

3.抢到的碰db o（1）

4.没抢到的sleep

5.db更新o（1）

6.sleep的回到第一步

为啥加redis锁：1.你不知道请求是不是并发的 2.保障db的压力

#### 如何解决 Redis 缓存雪崩问题

鉴于缓存的作用，一般在数据存入时，会设置一个失效时间，如果插入操作是和用户操作同步进行，则该问题出现的可能性不大，因为用户的操作天然就是散列均匀的。

而另一些例如缓存预热的情况，依赖离线任务，*定时批量的进行数据更新或存储*，过期时间问题则要特别关注。

因为离线任务会在短时间内将大批数据操作完成，如果过期时间设置的一样，会在同一时间过期失效，后果则是上游请求会在同一时间将大量失效请求打到下游数据库，从而造成底层存储压力。同样的情况还发生在缓存宕机的时候。

**解决方案**：

一是考虑热点数据不过期/上一节提到的逻辑过期。

二是让过期时间离散化，如，在固定的过期时间上额外增加一个随机数，这样会让缓存失效的时间分散在不同时间点，底层存储不至于瞬间飙升。

三是用集群主从的方式，保障缓存服务的高可用。防止全面崩溃。使用 Redis 集群来保证 Redis 服务不会挂掉

### 爬虫系统设计

爬虫---> crawling web pages --> analyze page content --> store in the index

 用户-------(User queries) --->ranking algorithms---(fetch data)--> store in the index

frontier：消息队列 + 用来去重的数据库

单机过程：一开始先从种子url放在queue里，每次从queue拿出一个url发出http请求，将内容读出来，然后分析处理内容，将里面的超链接的url拿出来，放回queue；将文本图片等内容做一下处理放在 index db里面

爬虫需要考虑： 1. 不能变成攻击网站，不能过度访问，防止被封，需要某种机制（robot协议，yahoo就有表示两个请求应该隔多久）

2.选择哪些网页进行下载，不可能全部爬下来，bfs就比较好，比如某个网页有其他的100url关联性比较好

3.针对网站如果发生变化的情况，需要一些机制可以重新访问（比如10天再次访问，频繁更新新闻10min）

4.怎么样多台机器沟通好，不要同时访问同一个url

内容解析的过程：

1.要看网页的内容是不是看到过？可以将内容md5 的hashcode放在一个数据库里面，然后进行对比，

如果有，表示不需要处理了，如果没有访问到，可以更新数据库，然后将内容放在索引数据库

2. 拿出网页的url，有些url我们不想访问，可以加一个url filter，然后去重，再加入mq，比如rabbit mq

<img src="/Users/jialinzhang/Library/Application Support/typora-user-images/截屏2022-01-09 下午9.36.01.png" alt="截屏2022-01-09 下午9.36.01" style="zoom:50%;" />

urlset 里面有时间戳，offline job可以将一些老的url重新放在queue里

url去重设计：

1. 直接存url在数据库，性能不理想，但是还可以前面fetch page过程http也挺慢的
2. 直接存in memory 的set里面，小型的爬虫可以放下，或者多几台机器也可以
3. hash url（md5）然后放在 in memory的set里面，128 bit string，16 bytes
4. bitmap，hash url to bitmap，但会有冲突
5. 步容过滤器，数据不那么多的时候性能还可以

反被拉黑：

可以用ip poxy，可以存一些浏览器的信息，user agent 随机放在header里面

### 秒杀系统设计



### 分布式唯一ID系统设计



### 设计直播间弹幕互动系统



### Sort URL 设计



### 主播礼物排行表





# kafka

### 用途：

异步，做解耦，做流处理，做可靠传输：

日志收集：一个公司可以用Kafka可以收集各种服务的log，通过kafka以统一接口服务的方式开放给各种consumer，例如hadoop、Hbase、Solr等。

消息系统：解耦和生产者和消费者、缓存消息等。

用户活动跟踪：Kafka经常被用来记录web用户或者app用户的各种活动，如浏览网页、搜索、点击等活动，这些活动信息被各个服务器发布到kafka的topic中，然后订阅者通过订阅这些topic来做实时的监控分析，或者装载到hadoop、数据仓库中做离线分析和挖掘。

运营指标：Kafka也经常用来记录运营监控数据。包括收集各种分布式应用的数据，生产各种操作的集中反馈，比如报警和报告。

流式处理：比如spark streaming和storm

事件源

### kafka vs rabbitmq 

Kafka主要为高吞吐量的订阅发布系统而设计，主要追求速度与持久化。kafka中的消息由键、值、时间戳组成，kafka不记录每个消息被谁使用，只通过偏移量记录哪些消息是未读的，kafka中可以指定消费组来实现订阅发布的功能。

首先来看rabbit，他通过broker来进行统一调配消息去向，生产者通过指定的规则将消息发送到broker，broker再按照规则发送给消费者进行消费，消费者方可以选择消费方式为pull或者是broker主动push，支持的消费模式也有多种，点对点，广播，正则匹配等。

如何选择？

**Kafka：**

1.从A系统到B系统的消息没有复杂的传递规则，并且具有较高的吞吐量要求。

2.需要访问消息的历史记录的场景，因为kafak是持久化消息的，所以可以通过偏移量访问到那些已经被消费的消息（前提是磁盘空间足够，kafka没有将日志文件删除）

3.流处理的场景。处理源源不断的流式消息，比较典型的是日志的例子，将系统中源源不断生成的日志发送到kafka中。

**rabbit：**

1.需要对消息进行更加细粒度的控制，包括一些可靠性方面的特性，比如死信队列。

2.需要多种消费模式（点对点，广播，订阅发布等）

3.消息需要通过复杂的路由到消费者

众所周知，kafka的吞吐量优于rabbit，大约是100k/sec，而rabbit大约是20k/sec，但是这个不应该成为我们选择的主要原因，因为性能方面的瓶颈都是可以通过集群方案来解决的。



### 如何保证高可用？

kafka在0.8以前是没有HA机制的，也就是说任何一个broker宕机了，那个broker上的partition就丢了，没法读也没法写，没有什么高可用可言。

kafka在0.8之后，提过了HA机制，也就是replica副本机制。每个partition的数据都会同步到其他机器上，形成自己的replica副本。然后所有的replica副本会选举一个leader出来，那么生产者消费者都和这个leader打交道，其他的replica就是follower。写的时候，leader会把数据同步到所有follower上面去，读的时候直接从leader上面读取即可。
**为什么只能读写leader：**因为要是你可以随意去读写每个follower，那么就要关心数据一致性问题，系统复杂度太高，容易出问题。kafka会均匀度讲一个partition的所有数据replica分布在不同的机器上，这样就可以提高容错性。
这样就是高可用了，因为如果某个broker宕机 了，没事儿，那个broker的partition在其他机器上有副本，如果这上面有某个partition的leader，那么此时会重新选举出一个现代leader出来，继续读写这个新的leader即可。



**写消息：** 写数据的时候，生产者就写leader，然后leader将数据落到磁盘上之后，接着其他follower自己主动从leader来pull数据。一旦所有follower同步好了数据，就会发送ack个leader，leader收到了所有的follower的ack之后，就会返回写成功的消息给消息生产者。（这只是一种模式，可以调整）。
**读数据:**消费数据的时候，只会从leader进行消费。但是只有一个消息已经被所有follower都同步成功返回ack的时候，这个消息才会被消费者读到。

### 如何恢复？

Kakfa Broker Leader的选举：Kakfa Broker集群受Zookeeper管理。所有的Kafka Broker节点一起去Zookeeper上注册一个临时节点，因为只有一个Kafka Broker会注册成功，其他的都会失败，所以这个成功在Zookeeper上注册临时节点的这个Kafka Broker会成为Kafka Broker Controller，其他的Kafka broker叫Kafka Broker follower。（这个过程叫Controller在ZooKeeper注册Watch）。这个Controller会监听其他的Kafka Broker的所有信息，如果这个kafka broker controller宕机了，在zookeeper上面的那个临时节点就会消失，此时所有的kafka broker又会一起去Zookeeper上注册一个临时节点，因为只有一个Kafka Broker会注册成功，其他的都会失败，所以这个成功在Zookeeper上注册临时节点的这个Kafka Broker会成为Kafka Broker Controller，其他的Kafka broker叫Kafka Broker follower。例如：一旦有一个broker宕机了，这个kafka broker controller会读取该宕机broker上所有的partition在zookeeper上的状态，并选取ISR列表中的一个replica作为partition leader（如果ISR列表中的replica全挂，选一个幸存的replica作为leader; 如果该partition的所有的replica都宕机了，则将新的leader设置为-1，等待恢复，等待ISR中的任一个Replica“活”过来，并且选它作为Leader；或选择第一个“活”过来的Replica（不一定是ISR中的）作为Leader），这个broker宕机的事情，kafka controller也会通知zookeeper，zookeeper就会通知其他的kafka broker。

### Kafka的文件存储机制

Kafka中消息是以topic进行分类的，生产者通过topic向Kafka broker发送消息，消费者通过topic读取数据。然而topic在物理层面又能以partition为分组，一个topic可以分成若干个partition。partition还可以细分为segment，一个partition物理上由多个segment组成，segment文件由两部分组成，分别为“.index”文件和“.log”文件，分别表示为segment索引文件和数据文件。这两个文件的命令规则为：partition全局的第一个segment从0开始，后续每个segment文件名为上一个segment文件最后一条消息的offset值。

### Kafka 如何保证可靠性

**消息确认机制**。Kafka 主题对应了多个分区，每个分区下面又对应了多个副本；为了让用户设置数据可靠性， Kafka 在 Producer 里面提供了消息确认机制。也就是说我们可以通过配置来决定消息发送到对应分区的几个副本才算消息发送成功。可以在定义 Producer 时通过 acks 参数指定。这个参数支持以下三种值：

* acks = 0：意味着如果生产者能够通过网络把消息发送出去，那么就认为消息已成功写入 Kafka 。在这种情况下还是有可能发生错误，比如发送的对象无能被序列化或者网卡发生故障，但如果是分区离线或整个集群长时间不可用，那就不会收到任何错误。在 acks=0 模式下的运行速度是非常快的（这就是为什么很多基准测试都是基于这个模式），你可以得到惊人的吞吐量和带宽利用率，不过如果选择了这种模式， 一定会丢失一些消息。
* acks = 1：意味若 Leader 在收到消息并把它写入到分区数据文件（不一定同步到磁盘上）时会返回确认或错误响应。在这个模式下，如果发生正常的 Leader 选举，生产者会在选举时收到一个 LeaderNotAvailableException 异常，如果生产者能恰当地处理这个错误，它会重试发送悄息，最终消息会安全到达新的 Leader 那里。不过在这个模式下仍然有可能丢失数据，比如消息已经成功写入 Leader，但在消息被复制到 follower 副本之前 Leader发生崩溃。
* acks = all（这个和 request.required.acks = -1 含义一样）：意味着 Leader 在返回确认或错误响应之前，会等待所有同步副本都收到悄息。如果和min.insync.replicas 参数结合起来，就可以决定在返回确认前至少有多少个副本能够收到悄息，生产者会一直重试直到消息被成功提交。不过这也是最慢的做法，因为生产者在继续发送其他消息之前需要等待所有副本都收到当前的消息。

### Kafka消息是采用Pull模式，还是Push模式 （Pull 模式）

Kafka最初考虑的问题是，consumer应该从brokes拉取消息还是brokers将消息推送到consumer，也就是pull还push。在这方面，Kafka遵循了一种大部分消息系统共同的传统的设计：producer将消息推送到broker，consumer从broker拉取消息。push模式下，当broker推送的速率远大于consumer消费的速率时，consumer恐怕就要崩溃了。最终Kafka还是选取了传统的pull模式。Pull模式的另外一个好处是consumer可以自主决定是否批量的从broker拉取数据。Pull有个缺点是，如果broker没有可供消费的消息，将导致consumer不断在循环中轮询，直到新消息到t达。为了避免这点，Kafka有个参数可以让consumer阻塞知道新消息到达。（注意pull方法的参数的含义，设置为0，那么如果没有数据返回，轮询线程立马返回，如果设置了超时时间，那么将会等待相应的时间如果没有数据返回）

### Kafka是如何实现高吞吐率的

1. 顺序读写：kafka的消息是不断追加到文件中的，这个特性使kafka可以充分利用磁盘的顺序读写性能
2. 零拷贝：跳过“用户缓冲区”的拷贝，建立一个磁盘空间和内存的直接映射，数据不再复制到“用户态缓冲区”
3. 文件分段：kafka的队列topic被分为了多个区partition，每个partition又分为多个段segment，所以一个队列中的消息实际上是保存在N多个片段文件中
4. 批量发送：Kafka允许进行批量发送消息，先将消息缓存在内存中，然后一次请求批量发送出去
5. 数据压缩：Kafka还支持对消息集合进行压缩，Producer可以通过GZIP或Snappy格式对消息集合进行压缩

### Kafka判断一个节点还活着的两个条件

1. 节点必须可以维护和 ZooKeeper 的连接，Zookeeper 通过心跳机制检查每个节点的连接
2. 如果节点是个 follower,他必须能及时的同步 leader 的写操作，延时不能太久

# apache strom 

#### 为什么选择strom

Storm是一个免费开源、分布式、高容错的实时计算系统。Storm令持续不断的流计算变得容易，弥补了Hadoop批处理所不能满足的实时要求。

Stream是storm里面的关键抽象。一个stream是一个没有边界的tuple序列。storm提供一些原语来分布式地、可靠地把一个stream传输进一个新的stream。比如： 你可以把一个tweets流传输到热门话题的流。

storm提供的最基本的处理stream的原语是spout和bolt。你可以实现Spout和Bolt对应的接口以处理你的应用的逻辑。

spout的英文名字是水龙头，流的源头，他可以从外部拿到流数据，比如消息队列，http response，也可以是一些定时的triger，数据库等等，然后发送给bolt

bolt闪电可以接收任意多个输入stream， 作一些处理， 有些bolt可能还会发射一些新的stream。一些复杂的流转换， 比如从一些tweet里面计算出热门话题， 需要多个步骤， 从而也就需要多个bolt。 Bolt可以做任何事情: 运行函数， 过滤tuple, 做一些聚合， 做一些合并以及访问数据库等等。

spout和bolt所组成一个网络会被打包成topology， topology是storm里面最高一级的抽象， 你可以把topology提交给storm的集群来运行。

| Storm                                                        | Hadoop                                                       |
| :----------------------------------------------------------- | :----------------------------------------------------------- |
| 实时流处理                                                   | 批量处理                                                     |
| 无状态                                                       | 有状态                                                       |
| 主/从架构与基于**ZooKeeper**的协调。主节点称为nimbus，从属节点是**主管**。 | 具有/不具有基于ZooKeeper的协调的主 - 从结构。主节点是**作业跟踪器**，从节点是**任务跟踪器**。 |
| Storm流过程在集群上每秒可以访问数万条消息。                  | Hadoop分布式文件系统（HDFS）使用MapReduce框架来处理大量的数据，需要几分钟或几小时。 |
| Storm拓扑运行直到用户关闭或意外的不可恢复故障。              | MapReduce作业按顺序执行并最终完成。                          |
| **两者都是分布式和容错的**                                   |                                                              |
| 如果nimbus / supervisor死机，重新启动使它从它停止的地方继续，因此没有什么受到影响。 | 如果JobTracker死机，所有正在运行的作业都会丢失。             |

#### 介绍

Storm集群和Hadoop集群表面上看很类似。但是Hadoop上运行的是MapReduce jobs，而在Storm上运行的是拓扑（topology），这两者之间是非常不一样的。一个关键的区别是： 一个MapReduce job最终会结束， 而一个topology永远会运行（除非你手动kill掉）。

在Storm的集群里面有两种节点： 控制节点（master node）和工作节点（worker node）。控制节点上面运行一个叫Nimbus后台程序，它的作用类似Hadoop里面的JobTracker。Nimbus负责在集群里面分发代码，分配计算任务给机器， 并且监控状态。

每一个工作节点上面运行一个叫做Supervisor的节点。Supervisor会监听分配给它那台机器的工作，根据需要启动/关闭工作进程。每一个工作进程processor执行一个topology的一个子集；一个运行的topology由运行在很多机器上的很多工作进程组成

Nimbus和Supervisor之间的所有协调工作都是通过Zookeeper集群完成。另外，Nimbus进程和Supervisor进程都是快速失败（fail-fast)和无状态的。所有的状态要么在zookeeper里面， 要么在本地磁盘上。这也就意味着你可以用kill -9来杀死Nimbus和Supervisor进程， 然后再重启它们，就好像什么都没有发生过。这个设计使得Storm异常的稳定。

**topologies**

一个topology是spouts和bolts组成的图，一个topology会一直运行直到你手动kill掉，Storm自动重新分配执行失败的任务， 并且Storm可以保证你不会有数据丢失（如果开启了高可靠性的话）。如果一些机器意外停机它上面的所有任务会被转移到其他机器上。

**Streams**

消息流stream是storm里的关键抽象。一个消息流是一个没有边界的tuple序列， 而这些tuple序列会以一种分布式的方式并行地创建和处理。通过对stream中tuple序列中每个字段命名来定义stream。在默认的情况下，tuple的字段类型可以是：integer，long，short， byte，string，double，float，boolean和byte array。你也可以自定义类型（只要实现相应的序列化器）。

**spouts** 闪电

消息源spout是Storm里面一个topology里面的消息生产者。一般来说消息源会从一个外部源读取数据并且向topology里面发出消息：tuple。Spout可以是可靠的也可以是不可靠的。如果这个tuple没有被storm成功处理，可靠的消息源spouts可以重新发射一个tuple， 但是不可靠的消息源spouts一旦发出一个tuple就不能重发了。

另外两个比较重要的spout方法是ack和fail。storm在检测到一个tuple被整个topology成功处理的时候调用ack，否则调用fail。storm只对可靠的spout调用ack和fail。

**bolts** 水龙头

所有的消息处理逻辑被封装在bolts里面。Bolts可以做很多事情：过滤，聚合，查询数据库等等。

Bolts可以简单的做消息流的传递。复杂的消息流处理往往需要很多步骤，从而也就需要经过很多bolts。

Bolts的主要方法是execute, 它以一个tuple作为输入，bolts使用OutputCollector来发射tuple

**可靠性**

Storm保证每个tuple会被topology完整的执行。Storm会追踪由每个spout tuple所产生的tuple树（一个bolt处理一个tuple之后可能会发射别的tuple从而形成树状结构），并且跟踪这棵tuple树什么时候成功处理完。每个topology都有一个消息超时的设置，如果storm在这个超时的时间内检测不到某个tuple树到底有没有执行成功， 那么topology会把这个tuple标记为执行失败，并且过一会儿重新发射这个tuple。

**tasks**

每一个spout和bolt会被当作很多task在整个集群里执行。每一个executor对应到一个线程，在这个线程上运行多个task，而stream grouping则是定义怎么从一堆task发射tuple到另外一堆task。你可以调用TopologyBuilder类的setSpout和setBolt来设置并行度（也就是有多少个task）。

**workers**

一个topology可能会在一个或者多个worker（工作进程）里面执行，每个worker是一个物理JVM并且执行整个topology的一部分。比如，对于并行度是300的topology来说，如果我们使用50个工作进程来执行，那么每个工作进程会处理其中的6个tasks。Storm会尽量均匀的工作分配给所有的worker。

#### 每个水龙头spout

#### 高性能？



#### 如何保证消息的可靠性？



