#  **操作系统**

### 汇编语言（机器语言）

汇编语言的本质：机器语言的助记符

00001000 mov

计算机通电-cpu读取内存中的程序（电信号的输入）-时钟发生器不断的震荡通断电-推动cpu内部一步步执行（执行多少步取决于指令需要的时钟周期）-计算完成-写会（电信号）-写给显卡输出（sout或者图像）

### 计算机组成

cpu：pc- program counter 程序计数器记录内存指令的地址

​          registers寄存器，暂时存储计算需要用到的数据 64位cpu指寄存器可以一次读64位数据

​          cache缓存

​          alu-arithmetic & logic unit 运算单元

​          cu-control unit 控制单元，对中断信号等进行控制

​          mmu- memory management unit 内存管理单元

系统总线：连接cpu和io brigde

io bridge: 连接系统总线，内存总线，io总线

内存总线：连接内存和io brige

内存 main memory

io总线：上面可以自由连接显卡，网卡，磁盘等。

### 超线程

一个alu对应多个pc和register，所谓的四核八线程。如果只有一个pc和register，线程上下文切换的时候，需要把上一个pc和register的内容拿出去，再把另一个线程的pc和register内容装进来，这个过程要消耗资源。如果alu有多个pc/regiser，线程上下文切换的过程就更简单了。

### 存储器层次结构                                       

寄存器 ->  L1 -> L2 -> L3-> main memory -> 磁盘 -> 远程文件存储

更小，更贵，更快                                                               更大，更慢，更便宜

### 缓存

多存几份，先从近的拿，没有就去更远的地方拿。

1.物理结构： 

​              核1: alu，register，pc，l1，l2

Cpu1 ｜                                                              l3  ｜ ----------------

​              核2: alu，register，pc，l1，l2

​                                                                                                              ｜---------------内存

​              核1: alu，register，pc，l1，l2

Cpu2 ｜                                                              l3  ｜ ----------------

​              核2: alu，register，pc，l1，l2



2.读取数据的过程：（按块读取）

根据程序的局部性原理（用这个一个数字，通常会马上需要它相邻的数字），读取数据是按照

块的。

3.cache line的概念，缓存行对齐，伪共享

内存               [（x,y)]  [       ] [       ] [          ]

L3                                      [(x, y)]     

cpu     核1:[x (modified), y]                    核2:  [(x, y(modified))]

x和y位于同一个块cacheline，读x进来会将整块一起读进来，如果x和y需要数据一致性，内部使用缓存一致性协议。其中，intel用的是mesi。其中缓存锁不够用，就锁总线。

缓存行大：局部性效率高，但读取时间慢

缓存行小：局部性效率低。读取快

intel用了64个字节 

伪共享：看起来共享了，要互相通知保持一致性，很麻烦

```java
public class CacheLinePadding{
  public static volatile long[] arr = new long[2];
  public static void main(string[] args) throws Exception {
  	Thread t1 = new Thread(()-> {
      for (long i = 0; i <10_0000_10000L; i++) {
        arr[0] = i;
      }
    });
  
    Thread t2 = new Thread(()-> {
      for (long i = 0; i <10_0000_10000L; i++) {
        arr[1] = i;
      }
    });
    final long start = System.getNanoTime();
  	t1.start();
    t2.start();
    t1.join();
    t2.join();
    final long end = System.getNanoTime();
    System.out.println(end - start);
	}
}

vs 
  
public class CacheLinePadding2{
  public static volatile long[] arr = new long[16];
  public static void main(string[] args) throws Exception {
  	Thread t1 = new Thread(()-> {
      for (long i = 0; i <10_0000_10000L; i++) {
        arr[0] = i;
      }
    });
  
    Thread t2 = new Thread(()-> {
      for (long i = 0; i <10_0000_10000L; i++) {
        arr[8] = i;
      }
    });
    final long start = System.getNanoTime();
  	t1.start();
    t2.start();
    t1.join();
    t2.join();
    final long end = System.getNanoTime();
    System.out.println(end - start);
	}
}

```

缓存行对齐：对于有些特别敏感的数字，会存在线程高竞争访问，为了保证不发生伪共享，可以使用缓存行对齐方式编程。

```java
public long p1,p2,p3,p4,p5,p6,p7,p8;
public static volitale long INFINTE_CURSOR;
public long p9,p10,p11,p12,p13,p14,p15,p16;
```

Jdk7中，很多采用long padding提高效率

jdk8加入了 @contended注解, （jvm会保证x和y在底层cpu中不会放在一个缓存行里）需要加上jvm参数 vm option：-xx:-RestrictContended

```
@Contended
long x;
@Contended
long y;
```

### cpu乱序执行

cpu在进行读等待的同时执行指令，是cpu指令的根源而不是乱，而是提高效率

```java
class Disorder{
  public static void main(String[] args) {
    x = 0;y = 0;a = 0;b = 0;
    Thread one = new Thread(new Runnable() {
      public void run() {
        a = 1;
        x = b;
      }
    });
    Thread two = new Thread(new Runnable() {
      public void run() {
        b = 1;
        y = a;
      }
    }); 
    one.start();two.start();
    one.join();two.join();
    String result = i +" " + x + " " + y;
    if (x == 0 && y == 0) {
      System.err.println(result);
      break;
    } 
  }
}
```

实验结果：第27288842次才发生了重排序

注：因为任何的排列组合都不应该出现x和y都是0，除非出现乱序

可能产生的问题：

如何禁止指令重排序？

### 禁止乱序

内存屏障

对某部分内存做操作时前后添加屏障，屏障前后的操作不可以乱序。

指令1一-去内存读数据

————————————屏障，指令1，2不可换

指令2-优先指令



cpu底层如何解决？ 原子指令 或者 intel lock指令

jvm层级如何解决？（一种规范，跟硬件没有关系）

jsr内存屏障：

loadload屏障 load1，loadload，load2 在load2以及后续读取操作要读取数据之前，保障load1要						读取的数据被读取完毕。

storestore屏障 store1，loadload，store2

loadstore屏障 load1，loadload，store2

storeload屏障 store1，storeload，load2



volatile实现细节---------------jvm层面

storestorebarrier               loadloadbarrier

volatile写操作                      volatile读操作

storeloadbarrier                 loadstorebarrier



cpu原则就是只要前后没有逻辑关系就可以乱序执行



<u>cpu原则：intel-》原语或者锁总线</u>

<u>jvm层面：8个happends before原则， 4个内存屏障</u>

as if serial 不管硬件什么顺序，单线程执行结果不变，看上去像serial

扩展：如果好几个线程想要它们顺序执行，可以放在singlethreadpool里面

### 合并写

（不重要）

write combining buffer

一般是四个字节

由于alu速度太快，所以在写入l1的同时，写入wc buffer，满了之后再写入l2



### os基础

从第一次通电开机，bios，加载好操作系统，电脑的一切都是听操作系统的了“老大”

什么是操作系统？ 一边管理硬件，一边提供服务

结构：

kernel最重要，直接管理硬件

《linux内核设计与实现？》以后拓展用

 内核：管理各种硬件+cpu调度

平时用的都是宏内核，鸿蒙微内核只有一个工作就是cpu调度，5g，物联网

### linux用户态和内核态

dos可以啥都干，病毒天堂，所以linux将操作分开了，分级别。

cpu分成不同的指令级别，0 1 2 3 ring级

<u>内核态</u> 0 + <u>用户态</u> 3

内核跑在ring 0 级，用户程序跑在ring 3 级

比如，去网卡读个数据就切换到0 ring态，回到内存计算3 态，再去读切来切去

dos时代，一个程序就是计算机之王。很容易写病毒

现在，操作系统才是老大，用户干一些操作，只能向老大申请同意。

内核执行的操作，大概200多个系统调用， read write

小问题：jvm对于操作系统就是一个普通的程序，当然是用户态

### 进程 线程 纤程

问题：进程和线程有什么区别？

答案：进程就是一个程序运行起来的状态，线程是一个进程中不同的执行单元。

<u>进程是os调度的基本单位，线程是执行调度的基本单位。</u>分配资源最重要的是，

独立的内存空间，线程调度执行（线程共享一个进程的储存空间，线程没有独立的空间）



线程在linux里面的实现：就是一个普通的进程，只是和主进程共享一个内存空间

在其他的操作系统中会有轻量级的进程。

fiber 纤程 ：在用户空间的线程，线程里面的线程。切换和调度不需要跟os的内核打交道，只需要

跟用户态的线程打交道，可以启动几万个。



多个fiber------一个线程

多个线程-------一个jvm

一个jvm----------os  （当然os也有其他的进程）

特点：跑在用户态！！！！！

优点：1.占有的资源很少，os启动一个线程要用1m，fiber也有4k

​          2.轻量级，切换比较简单

​          3.轻量级，可以启动10万+，os启动这么多线程，所有的资源估计都用在切换上

目前语言内置fiber的 ，scala，go，koltin，python+一个类库，java open jdk有一个loom

###  纤程应用场景

纤程vs线程池：很短的计算任务，不需要和内核打交道，并发量高！

### 进程

linux中也称为task，是系统分配资源的基本单位

资源：独立的地址空间，内核数据结构（进程描述符。。。）全局变量 数据段

进程描述符：pcb（process control block）

内核线程：内核启动之后经常需要一些后台操作，这些都是由kernel thread来完成只在内核空间运行

进程的创建和启动：

系统函数fork（）exec（）-----linux用c语言写的

从 a 中fork b的话，a也称为b的父进程

a--------fork-----b

父进程             子进程



### 僵尸进程 孤儿进程

什么是僵尸进程

​            ps -ef｜grep defuct

​           父进程产生子进程后，会维护子进程的一个pcb结构，子进程退出后。由父进程释放

​            如果父进程没有释放，那么子进程成为一个僵尸进程

什么是孤儿进程

​            子进程结束之前，父进程以及退出了。系统一般会把孤儿们交给一个特殊的进程init处理

### 进程调度

内核进程调度器决定：该哪一个进程运行？何时开始？运行多长时间？

（内核的调度方案决定，可以自己写，原则：最大限度的压榨cpu资源）

多任务：multitasking

----非抢占式 cooperative multitasking （也许军方会用）

​     除非进程主动让出cpu（yiedling），否则将一直运行

----抢占式的preepmptive multitasking （current）

​     由进程调度器强制开始或者暂停某一进程的执行

<u>Linux2.6采用的completely fair scheduler</u>

<u>按优先级分配时间片的比例，记录每个进程执行的时间，如果有一个进程执行时间不打牌它</u>

<u>应该分配的比例，优先执行。</u>

<u>实时（急诊）优先级分高低-按照优先级fifo，优先级一样rr（round robin）</u>

进程类型：io密集型，大部分时间都在等待io

​                   cpu密集型 大部分时间都在闷头计算

进程优先级： 实时进程   》普通进程（0-99）

​                        普通进程nice值（-20---19）

时间分配        linux采用按优先级的cpu时间比

-------------linux默认的调度策略-----------------------------------

实时进程：使用sched——fifo 和sched——rr两种

普通进程：使用cfs

其中等级最高的是fifo，这种进程除非自己让出cpu否则linux会一直执行它

除非更高级的fifo和rr抢占它

rr只是这种线程中是同级别fifo的平均分配

只有实时进程主动让出，或者执行完毕后，普通进程才有机会运行

------------------------------------------------------------------------------------------------------

### 中断

“一个信号：内核！哥们我有个急事，你要不要处理一下？”

硬中断：键盘，网卡这些硬件直接请求cpu中断，cpu再通知os，os去内存里面中断表找

软中断：”interupt80“  软件请求中断，Java读网络-jvm read（）---c库read（）---内核空间---system call（）

（系统调用处理程序）---sys read（）

### 从汇编角度理解80软中断

搭建汇编环境 `$yum install nasm`

往fd=1（也就是terminal）的文件写一个hello。

```shell
;hello.asm
;write(int fd, const void *buffer, size_t nbytes)
;fd 文件描述符 file descriptor -linux下一切皆文件

section data
msg db "hello", 0xA
len equ $ -msg

section .text
global _start
_start:
      mov edx, len
      mov ecx, msg
      mov ebc, 1  ;文件描述符1 std_out
      mov eax, 4  ;write函数系统调用号 4
      int 0x80
      
      mov ebx, 0
      mov eax, 1; exit系统调用号
      int 0x80

```

编译 `nasm -f elf hellp.asm -o hello.o`

链接 `ld -m elf_i386 -0 hello hello.o`

一个程序的执行过程，要么处于用户态，要么处于内核态。

网络编程io时，用户空间要去内核态执行一个read，用户态那部分还可以继续干活？如果可以就是非阻塞

### 中断与fiber

为什么fiber更快？因为不需要cpu内核操作，因为不需要中断处理，中断需要系统调用

### 内存管理

   dos时代，同一个时间只能有一个进程在运行（也有一些特殊算法可以支持多进程）

早期问题：多个进程装不进，内存撑爆；进程之间互相打扰

为了解决这个问题，诞生了 现在的内存管理系统，虚拟地址 分页装入 交换分区 

解决内存撑爆问题：分块装入页框中page frame （内存页，4k标准页）

（局部性原理：时间局部性-指令旁边的指令很快被用到

​     空间局部性-数据局部性-数据旁边的数据很快被用的）

内存满了，进行交换分区（lru算法），在linux里面就是swap，硬盘实现的，所以很慢了。

问题：运行qq。exe的时候，没把有整个程序放在内存，实际上只是把那个程序的页表拿出来

放在内存里面了。

1.分页，内存中分成固定大小的页框（4k），把程序（硬盘上）分成4k大小的块，用到那一块

就加载哪一块。加载过程中，如果内存满了，新加载的块把最不常用的一块置出，放在swap分区

把最新的一块加载进来。这就是著名的lru算法

2.虚拟内存（解决互相打扰的问题）

1. dos win31.。。。互相干掉

2. 为了保证互相不影响，让进程工作在虚拟空间，程序中用的空间地址不在时直接的地址，

   而是虚拟的地址，这样a进程永远不可能访问到b进程的空间

3. 虚拟空间多大呢？寻找空间-64位操作系统 2^64，比物理空间大很多byte

4. 站在虚拟的进程角度，进程时独享整个系统 + cpu

   进程会将程序分成小一段一小段，内部是一页页4k的页，平时写程序用的是虚拟地址

   如何将虚拟地址和物理地址映射起来了？地址映射

5. why？ 安全，隔离应用程序突破物理内存限制

6. how内存映射？ 偏移量+段的基地址=线性地址（虚拟空间）

7. 线性地址通过os core+mmu 映射成为物理地址 （站在用户空间process不知道，除了os core谁也不知道到底存在哪里）

   

   P1    p2  p3 p4

   ​        Os core

   ----mmu-----------

   【P2 p1p3】            p4

   内存          swap硬盘上

   3。 缺页中断：如果需要的页面在内存没有，发生缺页中断，也叫缺页异常，由内核处理，从硬件load到内存

### 内核同步机制

   临界区 critical area：访问或操作共享数据的代码段

   竞争条件 race condition 两个线程同时拥有临界区的执行权

   数据不一致 data unconsistency 有竞争条件引起的数据破坏

   同步 synchronization 避免race condition

   锁：完成同步的手段（门锁，门后是临界区，只允许一个线程的存在）

   上锁解锁也需要原子性！

   原子性（像原子一样不可分割的操作）

   有序性（禁止指令重排）

   可见性（一个线程内的修改，另一个线程可见）

   

   原子性 有序性 可见性（atomicity ordering visibility）

   1。原子操作- 原语支持， linux/types。h

   2. 自旋锁-内核中通过汇编支持的cas，位于 spinlock。h

   3. 读写自旋-类似于readwritelock，可同时读，只能一个写

      读的时候是共享锁，写的时候是排他锁

   4. 信号量-类似于semaphore（pv操作downup操作 占有和释放，pv操作都是原子操作）

      重量级的锁，线程会进入wait，适合长时间持有的锁情况

      5. 读写信号量-downread upread downwrite upwrite

         （多个写，可以分段写，比较少用）（分段锁）

         6.互斥体 mutex-特殊的信号量（其实是特殊的信号量）

         7.完成变量-特殊的信号量（a发生信号给b，b等待在完成变量上）

         vfork（）在子进程结束后通过完成变量叫醒父进程，类似latch

         8.顺序锁-线程可以挂起的读写自旋锁，序列计数器从0开始，写的时候+1 写完释放+1，读前发现单数，

         说明有写线程，等待，读前读后序列一样，说明没有写线程打断。

         

#  ZooKeeper

### BASE理论

BASE理论是基本可用，软状态，最终一致性三个短语的缩写。BASE理论是对CAP中一致性和可用性（CA）权衡的结果，其来源于对大规模互联网系统分布式实践的总结，是基于CAP定理逐步演化而来的，它大大降低了我们对系统的要求。
1. 基本可用：基本可用是指分布式系统在出现不可预知故障的时候，**允许损失部分可用性**。但是，这绝不等价于系统不可用。比如正常情况下，一个在线搜索引擎需要在0.5秒之内返回给用户相应的查询结果，但由于出现故障，查询结果的响应时间增加了1~2秒。
2. 软状态：软状态指允许系统中的数据存在中间状态，并认为该中间状态的存在不会影响系统的整体可用性，即允许系统在不同节点的数据副本之间进行数据同步的过程存在延时。
3. 最终一致性：最终一致性强调的是系统中所有的数据副本，在经过一段时间的同步后，最终能够达到一个一致的状态。因此，最终一致性的本质是需要系统保证最终数据能够达到一致，而不需要实时保证系统数据的强一致性。

### ZooKeeper特点

1. 顺序一致性：**同一客户端**发起的事务请求，最终将会严格地按照顺序被应用到 ZooKeeper 中去。
2. 原子性：所有事务请求的处理结果在整个集群中所有机器上的应用情况是一致的，也就是说，要么整个集群中所有的机器都成功应用了某一个事务，要么都没有应用。
3. 单一系统映像：无论客户端连到哪一个 ZooKeeper 服务器上，其看到的服务端数据模型都是一致的。
4. 可靠性：一旦一次更改请求被应用，更改的结果就会被持久化，直到被下一次更改覆盖。

### ZAB协议：

解决崩溃恢复和主从数据同步问题。

ZAB (Zookeeper Atomic Broadcast **Protocol**)协议包括两种基本的模式：崩溃恢复和消息广播。当整个 Zookeeper 集群刚刚启动或者Leader服务器宕机、重启或者网络故障导致不存在过半的服务器与 Leader 服务器保持正常通信时，所有服务器进入崩溃恢复模式，首先选举产生新的 Leader 服务器，然后集群中 Follower 服务器开始与新的 Leader 服务器进行数据同步。当集群中超过半数机器与该 Leader 服务器完成数据同步之后，退出恢复模式进入消息广播模式，Leader 服务器开始接收客户端的事务请求生成事物提案（超过半数同意）来进行事务请求处理。

### 集群服务器节点

leader写/读

follower 只负责读，还会参与leader选举

observer 只负责读，不参与leader选举

### 选举算法和流程：FastLeaderElection(默认提供的选举算法)

目前有5台服务器，每台服务器均没有数据，它们的编号分别是1,2,3,4,5,按编号依次启动，它们的选择举过程如下：
1. 服务器1启动，给自己投票，然后发投票信息，由于其它机器还没有启动所以它收不到反馈信息，服务器1的状态一直属于Looking。
2. 服务器2启动，给自己投票，同时与之前启动的服务器1交换结果，由于服务器2的编号大所以服务器2胜出，但此时投票数没有大于半数，所以两个服务器的状态依然是LOOKING。
3. 服务器3启动，给自己投票，同时与之前启动的服务器1,2交换信息，由于服务器3的编号最大所以服务器3胜出，此时投票数正好大于半数，所以服务器3成为leader，服务器1,2成为follower。
4. 服务器4启动，给自己投票，同时与之前启动的服务器1,2,3交换信息，尽管服务器4的编号大，但之前服务器3已经胜出，所以服务器4只能成为follower。
5. 服务器5启动，后面的逻辑同服务器4成为follower。

### 集群一致性

1.客户端向主节点写数据

2.主节点先把数据写在自己的数据文件中，并返回一个ack

3.leader把数据发送给follwer

4.follwer将数据写到本地数据文件中，并返回ack给主节点

5.leader收到半数以上的ack就向follwer发送commit

6.follwer收到commit之后将数据文件中的数据写入内存

### zk的节点类型

Zookeeper的四种节点类型

- PERSISTENT // 持久化**节点**
- PERSISTENT_SEQUENTIAL // 持久化排序**节点**
- EPHEMERAL // 临时**节点**
- EPHEMERAL_SEQUENTIAL // 临时排序**节点** ，带序号，会话断开节点会被删除。

### zk中的监控原理

zk类似于linux中的目录节点树方式的数据存储，即分层命名空间，zk并不是专门存储数据的，它的作用是主要是维护和监控存储数据的状态变化，通过监控这些数据状态的变化，从而可以达到基于数据的集群管理，zk中的节点的数据上限是1M。

client端会对某个znode建立一个watcher事件，当该znode发生变化时，这些client会收到zk的通知，然后client可以根据znode变化来做出业务上的改变等。

### Zookeeper 的原理及实现

#### zookeeper如何避免 split brain

ZooKeeper默认采用了Quorums(法定人数)的方式: **只有获得超过半数节点的投票, 才能选举出leader.**

这种方式可以确保要么选出唯一的leader, 要么选举失败.

假设: leader发生了假死, followers选举出了一个新的leader.

当旧的leader复活并认为自己仍然是leader, 它向其他followers发出写请求时, 会被拒绝.

—— 因为ZooKeeper维护了一个叫epoch的变量, 每当新leader产生时, epoch都会递增, followers如果确认了新的leader存在, 同时也会知道其epoch的值 —— 它们会拒绝epoch小于现任leader的epoch的所有旧leader的任何请求.



zookeeper如何从奔溃中恢复



Zab 通过巧妙的设计 zxid 来实现这一目的。一个 zxid 是64位&#xff0c;高 32 是纪元&#xff08;epoch&#xff09;编号&#xff0c;每经过一次 leader 选举产生一个新的 leader&#xff0c;新 leader 会将 epoch 号 &#43;1。低 32 位是消息计数器&#xff0c;每接收到一条消息这个值 &#43;1&#xff0c;新 leader 选举后这个值重置为 0。这样设计的好处是旧的 leader 挂了后重启&#xff0c;它不会被选举为 leader&#xff0c;因为此时它的 zxid 肯定小于当前的新 leader。当旧的 leader 作为 follower 接入新的 leader 后，新的 leader 会让它将所有的拥有旧的 epoch 号的未被 COMMIT 的 proposal 清除。

### 了解 Paxos/Raft等协议



### 分布式协调

参考：https://github.com/doocs/advanced-java/blob/master/docs/distributed-system/zookeeper-application-scenarios.md

简单来说，就好比，你 A 系统发送个请求到 mq，然后 B 系统消息消费之后处理了。那 A 系统如何知道 B 系统的处理结果？用 zookeeper 就可以实现分布式系统之间的协调工作。A 系统发送请求之后可以在 zookeeper 上**对某个节点的值注册个监听器**，一旦 B 系统处理完了就修改 zookeeper 那个节点的值，A 系统立马就可以收到通知，完美解决。

### zk的锁

1. 读锁（共享锁）：大家都可以读，想要上读锁，前提是没有写锁

2. 写锁，只有拿到写锁才能写，想要上写锁，前提是没有锁

   如何上读锁？

   -创建一个临时序号节点，节点的数据是read，表示读锁；

   -获取当前zk中序号比自己小的所有节点，判断最小节点是否为读锁，如果不是读锁则上锁失败，为最小节点设置监听。该请求线程阻塞等待，zk的watch机制会通知最小节点锁是否释放，上锁成功

   如何上写锁？

   创建一个临时序号节点，节点的数据是write，表示写锁

   获取zk中序号比自己小的所有的节点，判断自己是否为最小节点，如果是上锁成功，如果不是上锁失败并监听最小节点变化。

3. 养群效应

   100个都在监听第一个节点，第一个节点发生变化，全部节点都收到了惊喜。如何解决？调整成链式监听。

### 分布式锁zookeeper vs. Redis



参考同上

举个栗子。对某一个数据连续发出两个修改操作，两台机器同时收到了请求，但是只能一台机器先执行完另外一个机器再执行。那么此时就可以使用 zookeeper 分布式锁，一个机器接收到了请求之后先获取 zookeeper 上的一把分布式锁，就是可以去创建一个 znode，接着执行操作；然后另外一个机器也**尝试去创建**那个 znode，结果发现自己创建不了，因为被别人创建了，那只能等着，等第一个机器执行完了自己再执行。

参考：https://zhuanlan.zhihu.com/p/73807097

Redis的话，就是 setnx + expire。

对于 Redis 的分布式锁而言，redis有以下缺点：

- 它获取锁的方式简单粗暴，获取不到锁直接不断尝试获取锁，比较消耗性能。
- 另外来说的话，Redis 的设计定位决定了它的数据并不是强一致性的，在某些极端情况下，可能会出现问题。锁的模型不够健壮。
- 即便使用 Redlock 算法来实现，在某些复杂场景下，也无法保证其实现 100% 没有问题，关于 Redlock 的讨论可以看 How to do distributed locking。

但是另一方面使用 Redis 实现分布式锁在很多企业中非常常见，而且大部分情况下都不会遇到所谓的“极端复杂场景”。

所以使用 Redis 作为分布式锁也不失为一种好的方案，最重要的一点是 Redis 的性能很高，可以支撑高并发的获取、释放锁操作。



对于 ZK 分布式锁而言:

- ZK 天生设计定位就是分布式协调，强一致性。锁的模型健壮、简单易用、适合做分布式锁。
- 如果获取不到锁，只需要添加一个监听器就可以了，不用一直轮询，性能消耗较小。

但是 ZK 也有其缺点：如果有较多的客户端频繁的申请加锁、释放锁，对于 ZK 集群的压力会比较大。



另外一点就是，如果是 Redis 获取锁的那个客户端 出现 bug 挂了，那么只能等待超时时间之后才能释放锁；而 zk 的话，因为创建的是临时 znode，只要客户端挂了，znode 就没了，此时就自动释放锁。



### 分布式Session

1. session 复制：可以在Web容器中开启session复制功能，在集群中的几个服务器之间同步session对象。
2. Sticky Session：利用负载均衡将来源于同一个IP的请求分发到同一台服务器上。
3. session服务器（集群）：使用专门的session服务器集群管理会话，比如redis。



### 分布式ID 生成

首先为什么要分布式ID：数据增长特别快之后，主从同步扛不住数据增长，需要对数据库进行一个分库分表。分完需要用一个唯一ID来标识每条数据，需要一个全局唯一ID来做查询支撑。

分布式ID需要：全局唯一，高可用，高性能，好接入，拿来即用

UUID：简单，但是，订单号一串字符串没有意义，看不出与订单有用的信息。另外字符串太长，存储查询耗时。

数据库自增：单独建立一个自增的mysql表用来生成ID。优点：实现简单。缺点：DB单节点存在宕机风险，无法抗住高并发场景。

基于Redis：利用redis 的自增命令 incr。优点：不依赖于数据库，灵活方便。缺点：如果系统中没有Redis，需要引入新的组建，增加系统复杂度。

雪花算法：1bit不用+41bit时间戳+10bit工作机器ID + 12 bit 序列号。缺点：单机上是递增，但是涉及到分布式环境，每台机器始终不完全同步。有可能会出现不是全局递增的情况。



### 分布式事务

2阶段提交，3阶段提交

prepare + accept

两阶段提交：一个分布式的事务过程拆分成两个阶段： 投票 和 事务提交。

三阶段提交：can-commit （预询盘），pre-commit （预提交），do_commit （事务提交）

**投票阶段：**

主要是为了检查数据库各个集群之间的参与者是否能够正常的执行事务。步骤：

1. 协调者向所有的参与者发送事务执行请求，并等待参与者反馈事务执行结果；
2. 事务参与者收到请求之后，执行事务但不提交，并记录事务日志；
3. 参与者将自己事务执行情况反馈给协调者，同时阻塞等待协调者的后续指令。

**事务提交阶段：**

在经过第一阶段协调者的询盘之后，各个参与者会回复自己事务的执行情况，这时候存在 3 种可能性：

1. 所有的参与者都回复能够正常执行事务。
2. 一个或多个参与者回复事务执行失败。
3. 协调者等待超时。

参考：https://blog.csdn.net/o9109003234/article/details/105259962

存在的问题：

- 单点问题

协调者在整个两阶段提交过程中扮演着举足轻重的作用，一旦协调者所在服务器宕机，就会影响整个数据库集群的正常运行。比如在第二阶段中，如果协调者因为故障不能正常发送事务提交或回滚通知，那么参与者们将一直处于阻塞状态，整个数据库集群将无法提供服务。

- 同步阻塞

两阶段提交执行过程中，所有的参与者都需要听从协调者的统一调度，期间处于阻塞状态而不能从事其他操作，这样效率极其低下。

- 数据不一致性

两阶段提交协议虽然是分布式数据强一致性所设计，但仍然存在数据不一致性的可能性。比如在第二阶段中，假设协调者发出了事务 commit 通知，但是因为网络问题该通知仅被一部分参与者所收到并执行了commit 操作，其余的参与者则因为没有收到通知一直处于阻塞状态，这时候就产生了数据的不一致性。

解决：

超时机制 和 互询机制

对于协调者来说如果在指定时间内没有收到所有参与者的应答，则可以自动退出 WAIT 状态，并向所有参与者发送 rollback 通知。对于参与者来说如果位于 READY 状态，但是在指定时间内没有收到协调者的第二阶段通知，则**不能**武断地执行 rollback 操作，因为协调者可能发送的是 commit 通知，这个时候执行 rollback 就会导致数据不一致。

此时，我们可以介入互询机制，让参与者 A 去询问其他参与者 B 的执行情况。如果 B 执行了 rollback 或 commit 操作，则 A 可以大胆的与 B 执行相同的操作；如果 B 此时还没有到达 READY 状态，则可以推断出协调者发出的肯定是 rollback 通知；如果 B 同样位于 READY 状态，则 A 可以继续询问另外的参与者。只有当所有的参与者都位于 READY 状态时，此时两阶段提交协议无法处理，将陷入长时间的阻塞状态。

# 微服务

【为什么使用微服务呢？】 在你对某一个微服务进行更新的时候，你不需要动其他的微服务，也就不需要动整个服务系统。 如果你的系统非常之庞大，做一次更新可能要需要很长的时间，从编译到安装是一个非常痛苦的过程，如果用微服务的话，你只需要更新那一小块儿服务就可以了。 接口方面，因为要求API是无状态的请求接口，这样子可以允许不同的微服务使用不同的技术来开发。 比如你可以用任何你想用的技术Java Spring Boot, PHP, Ruby On Rails, Asp.Net Core, nodejs, python, Go等各种后台开发技术



# Redis

### 应用场景

1. 缓存
2. 共享Session
3. 消息队列系统
4. 分布式锁

### 单线程的Redis为什么快

1. 纯内存操作
2. 单线程操作，避免了频繁的上下文切换
3. 合理高效的数据结构
4. 采用了非阻塞I/O多路复用机制（有一个文件描述符同时监听多个文件描述符是否有数据到来）同步非阻塞的`epoll`

epoll：内核通过一个事件表，直接管理用户感兴趣的所有事件，因此每次调用epoll_wait 时， 无须反复传入用户感兴趣的事件。epoll_wait 系统调用的参数event仅用来反馈就绪的事件。

epoll 使用事件驱动，但是用户进程依然处于阻塞状态，因此仍然属于同步阻塞。

多 路 复 用 I O ，“ 多 路 ” 指 的 是 多 个 网 络 连 接 ，“ 复 用 ” 指 的 是 复 用 同 一 个 线 程 。采用多路I/O复用的技术可以让单个线程高效的处理多个连接（尽量减少网络IO的时间消耗）

### I/O 模型

只是针对io读取这个过程，分为

同步模型：app 自己r/w

异步模型：kernel完成r/w，好像程序没有访问io，只访问了buffer

阻塞模型：blocking

非阻塞：noblocking

linux，netty： 同步+阻塞 或者 同步+非阻塞 

windows支持异步+非阻塞

http://www.masterraghu.com/subjects/np/introduction/unix_network_programming_v1.3/ch06lev1sec2.html

- blocking I/O （就是说，application发起一个recvfrom的时候，经过system call，kernel在没有收到数据的时候，就一直等待。直到收到数据后，才返回相应的数据）

- **nonblocking I/O** 

    o(n) recv系统调用需要用到软中断，浪费的

    > ```
    > （我们前三次调用recvfrom，没有数据要返回，因此内核立即返回错误EWOULDBLOCK。第四次我们调用recvfrom时，一个数据报已准备就绪，将其复制到application buffer中，然后recvfrom成功返回，然后我们处理数据。
    > ```

    > ```
    > 当应用程序像这样在nonblocking descriptor上循环调用recvfrom时，它称为polling。该应用程序不断轮询内核，以查看是否已准备好某些操作。这通常会浪费CPU时间，但是通常在专用于一个功能的系统上偶尔会遇到此模型。）
    > ```

    多路复用模型，多条路通过一个系统调用，获取io的状态，程序自己对有状态的io进行读写。注意：只要是程序自己读写，那么io模型就是同步的。

    select/poll/epoll都是多路复用器模型，同步非阻塞。

- I/O multiplexing (`select` and `poll`) 

    > 对于用select/poll做系统调用，我们会被block在select/poll上，等待datagram ready。当select返回数据可读之后，我们再用系统调用recvfrom来copy数据到application buffer里面。
    >
    > 缺点：要经过2个系统调用（select + recvfrom）
    >
    > 优点：我们可以等待多个文件描述符准备就绪

- signal driven I/O (`SIGIO`) 

> We first enable the socket for signal-driven I/O (as we will describe in [Section 25.2](http://www.masterraghu.com/subjects/np/introduction/unix_network_programming_v1.3/ch25lev1sec2.html#ch25lev1sec2)) and install a signal handler using the `sigaction` system call. The return from this system call is immediate and our process continues; it is not blocked. When the datagram is ready to be read, the `SIGIO` signal is generated for our process. We can either read the datagram from the signal handler by calling `recvfrom` and then notify the main loop that the data is ready to be processed (this is what we will do in [Section 25.3](http://www.masterraghu.com/subjects/np/introduction/unix_network_programming_v1.3/ch25lev1sec3.html#ch25lev1sec3)), or we can notify the main loop and let it read the datagram.

- asynchronous I/O (the POSIX `aio_`functions)

> ```
> 这个模型与上一节中的信号驱动的I / O模型之间的主要区别在于，使用信号驱动的I / O，内核会告诉我们何时可以启动I / O操作，而异步I / O内核会告诉我们I / O操作何时完成。
> ```

### select，poll，epoll

都是多路复用器；

Select出现的比较早，poll跟epoll后来出现的优化版本；

**其实无论nio还是select，poll全是要遍历所有的io询问状态！只不过在nio中这个遍历的过程成本高，需要用户态和内核态切换。**

**在select，poll下这个遍历的过程触发了一次系统调用，用户态和内核态的切换，过程中将fds传递给内核，内核重新根据用户这次调用传递过来的fds，遍历，修改状态**

select，poll的弊端：1.每次都要重新，重复传递fds

                                     2. 每次内核被调用之后针对这次调用出发一个遍历fds的复杂度

——————细节——————————————

内核层面： 网卡产生io中断方式，可以pakage，buffer，轮循

中断就有回调函数call back

event--》回调处理事件

在epoll之前的call back，只是将网卡发来的数据走内核的网络协议栈

最终关联到fd的buffer。所以你某一时间从app询问内核某一个或者某些fd是否可r/w，会有返回状态。

————————————————————————————

epoll有三个系统调用 epoll_create() epoll_ctl() epoll_wait()

epoll create 会在内核开辟一个空间（红黑树）解决重复传递

epoll ctl会传递（fd6，add，fd4）fd6空间会有fd-》accept

epoll wait等待链表就可以了

![截屏2021-12-20 下午6.11.45](/Users/jialinzhang/Library/Application Support/typora-user-images/截屏2021-12-20 下午6.11.45.png)

epoll程序只要调用wait就可以及时的取走有状态fd的结果集fds。

### BIO

面试回答：BIO就是一个同步阻塞模型，线程发起IO请求后，一直阻塞IO，直到缓冲区数据就绪后，再进入下一步操作。

BIO全称是Blocking IO，是JDK1.4之前的传统IO模型，本身是同步阻塞模式。 线程发起IO请求后，一直阻塞IO，直到缓冲区数据就绪后，再进入下一步操作。针对网络通信都是一请求一应答的方式，虽然简化了上层的应用开发，但在性能和可靠性方面存在着巨大瓶颈，试想一下如果每个请求都需要新建一个线程来专门处理，那么在高并发的场景下，机器资源很快就会被耗尽。

###NIO

面试回答：NIO non-blocking IO，同步非阻塞的IO模型。同步指的是必须等待IO缓冲区内的数据就绪，线程发起io请求后，立即返回（非阻塞io）

而Java中的new IO指的是线程轮询地去查看一堆IO缓冲区中哪些数据就绪，这是一种IO多路复用的思想。

IO多路复用模型中，将检查IO数据是否就绪的任务，交给系统级别的select或epoll模型，由系统进行监控，减轻用户线程负担。

=======分割线=========

NIO也叫Non-Blocking IO 是同步非阻塞的IO模型。线程发起io请求后，立即返回（非阻塞io）。同步指的是必须等待IO缓冲区内的数据就绪，而非阻塞指的是，用户线程不原地等待IO缓冲区，可以先做一些其他操作，但是要定时轮询检查IO缓冲区数据是否就绪。Java中的NIO 是new IO的意思。其实是NIO加上IO多路复用技术。普通的NIO是线程轮询查看一个IO缓冲区是否就绪，而Java中的new IO指的是线程轮询地去查看一堆IO缓冲区中哪些就绪，这是一种IO多路复用的思想。IO多路复用模型中，将检查IO数据是否就绪的任务，交给系统级别的select或epoll模型，由系统进行监控，减轻用户线程负担。

NIO主要有buffer、channel、selector三种技术的整合，通过零拷贝的buffer取得数据，每一个客户端通过channel在selector（多路复用器）上进行注册。服务端不断轮询channel来获取客户端的信息。channel上有connect, accept（阻塞）、read（可读）、write(可写)四种状态标识。根据标识来进行后续操作。所以一个服务端可接收无限多的channel。不需要新开一个线程。大大提升了性能。


参考：https://juejin.cn/post/6844903985158045703



### 零拷贝 zero copy

简单来说，内核（kernel）可以将硬盘（disk）里面的数据直接传输到socket里面，而不是通过程序传输，大大提高了应用程序的性能，并且减少了用户态和内核态的上下文切换。

考虑一个场景：开发者需要将硬盘里面的数据通过socket传输给用户：

需要经过4次拷贝的过程。

- 数据文件A通过DMA copy（Direct Memory Access）拷贝到kernel space 的kernel buffer （DMA copy）
- CPU将kernel 模式下的数据拷贝到用户的buffer （CPU copy）
- 调用write时，先将user模式下的内容复制到到kernel模式下的socket的buffer中 （CPU copy）
- 最后将kernel模式下的socket buffer的数据复制到网卡设备中传送 （DMA copy）

Linux 中的零拷贝：

在 Linux 中，减少拷贝次数的一种方法是调用 mmap() 来代替调用 read。

首先，应用程序调用了 mmap() 之后，数据会先通过 DMA 被复制到操作系统内核的缓冲区中去。接着，应用程序跟操作系统共享这个缓冲区，这样，操作系统内核和应用程序存储空间就不需要再进行任何的数据复制操作。应用程序调用了 write() 之后，操作系统内核将数据从原来的内核缓冲区中复制到与 socket 相关的内核缓冲区中。接下来，数据从内核 socket 缓冲区复制到协议引擎中去，这是第三次数据拷贝操作

通过使用 mmap() 来代替 read(), 已经可以减半操作系统需要进行数据拷贝的次数。当大量数据需要传输的时候，这样做就会有一个比较好的效率

**可能存在的问题：**

使用 mmap() 其实是存在潜在的问题的。当对文件进行了内存映射，然后调用 write() 系统调用，如果此时其他的进程截断了这个文件，那么 write() 系统调用将会被总线错误信号 SIGBUS 中断，因为此时正在执行的是一个错误的存储访问。这个信号将会导致进程被杀死

解决办法之一：

Linux 在版本 2.1 中引入了 sendfile() 这个系统调用。sendfile() 不仅减少了数据复制操作，它也减少了上下文切换。

参考：https://zhuanlan.zhihu.com/p/88789697

参考2: https://blog.csdn.net/weixin_37782390/article/details/103833306

**mmap 和 sendFile 的区别**

1. mmap 适合小数据量读写，sendFile 适合大文件传输。
2. mmap 需要 4 次上下文切换，3 次数据拷贝；sendFile 需要 3 次上下文切换，最少 2 次数据拷贝。
3. sendFile 可以利用 DMA 方式，减少 CPU 拷贝，mmap 则不能（必须从内核拷贝到 Socket 缓冲区）。

在这个选择上：rocketMQ 在消费消息时，使用了 mmap。kafka 使用了 sendFile。

### Redis 的数据结构及使用场景

1. String字符串:字符串类型是 Redis 最基础的数据结构，首先键都是字符串类型，而且 其他几种数据结构都是在字符串类型基础上构建的，我们常使用的 set key value 命令就是字符串。常用在缓存、计数、共享Session、限速等。
2. Hash哈希:在Redis中，哈希类型是指键值本身又是一个键值对结构，哈希可以用来存放用户信息，比如实现购物车。redis的哈希对象的底层存储可以使用ziplist（压缩列表）和hashtable。（什么时候用ziplist：哈希对象保存的所有键值对的键和值的字符串长度都小于64字节， 或者，哈希对象保存的键值对数量小于512个）
3. List列表（双向链表）:列表（list）类型是用来存储多个有序的字符串。可以做简单的消息队列的功能。
4. Set集合：集合（set）类型也是用来保存多个的字符串元素，但和列表类型不一 样的是，集合中不允许有重复元素，并且集合中的元素是无序的，不能通过索引下标获取元素。利用 Set 的交集、并集、差集等操作，可以计算共同喜好，全部的喜好，自己独有的喜好等功能。(sdiff key1 key2 返回第一个集合和第二个集合的差异。 sinter key1 key2 交集)
5. Sorted Set有序集合（跳表实现）：Sorted Set 多了一个权重参数 Score，集合中的元素能够按 Score 进行排列。可以做排行榜应用，取 TOP N 操作。

### Redis String 的编码方式

编码方式可以用 

```
OBJECT ENCODING keyname
```

来查看。

String类型的编码方式有：

- **int 编码**：保存long 型的64位有符号整数
- **embstr 编码**：保存长度小于44字节的字符串(embeded string)
- **raw 编码**：保存长度大于44字节的字符串

### String在Redis底层存储

Redis自己构建了`动态字符串（SDS）`的抽象类型

```c
struct sdshr {
	int len;
    int free;
    char buf[];
}
```





### Redis 的字典 与 Java 的 HashMap区别

看到散列算法、散列冲突解决方式，没有太大的区别，那么差别到底在哪儿呢？那就是**再哈希**。

- `Rehash`的目的在于为了让哈希表的负载因子维持在合理的范围内，哈希表在键值对太多或者太少时，需要进行**扩展或收缩**。

### Redis 的数据过期策略

Redis 中数据过期策略采用定期删除+惰性删除策略
* 定期删除策略：优点：所有过期key可以被删除，缺点：扫描所有key，消耗CPU资源，定时器还没启动时，过期key还是可用

* 惰性删除策略：在获取 key 时，先判断 key 是否过期，如果过期则删除。这种方式存在一个缺点：如果这个 key 一直未被使用，那么它一直在内存中，其实它已经过期了，会浪费大量的空间。

* 这两种策略天然的互补，结合起来之后，定时删除策略就发生了一些改变，不在是每次扫描全部的 key 了，而是随机抽取一部分 key 进行检查，这样就降低了对 CPU 资源的损耗，惰性删除策略互补了为检查到的key，基本上满足了所有要求。但是有时候就是那么的巧，既没有被定时器抽取到，又没有被使用，这些数据又如何从内存中消失？没关系，还有内存淘汰机制，当内存不够用时，内存淘汰机制就会上场。淘汰策略分为：
  
### 内存淘汰机制

    1. 当内存不足以容纳新写入数据时，新写入操作会报错。（Redis 默认策略）
    2. 当内存不足以容纳新写入数据时，在键空间中，移除最近最少使用的 Key。（LRU推荐使用）
    3. 当内存不足以容纳新写入数据时，在键空间中，随机移除某个 Key。
    4. 当内存不足以容纳新写入数据时，在设置了过期时间的键空间中，移除最近最少使用的 Key。这种情况一般是把 Redis 既当缓存，又做持久化存储的时候才用。
    5. 当内存不足以容纳新写入数据时，在设置了过期时间的键空间中，随机移除某个 Key。
    6. 当内存不足以容纳新写入数据时，在设置了过期时间的键空间中，有更早过期时间的 Key 优先移除。

### Redis的set和setnx

为什么用setnx？原子性（不存在的情况下完成创建）

为什么用set？

Redis中setnx不支持设置过期时间，做分布式锁时要想避免某一客户端中断导致死锁，需设置lock过期时间，在高并发时 setnx与 expire 不能实现原子操作，如果要用，得在程序代码上显示的加锁。使用SET代替SETNX ，相当于SETNX+EXPIRE实现了原子性，不必担心SETNX成功，EXPIRE失败的问题。

### Redis的LRU具体实现：

传统的LRU是使用栈的形式，每次都将最新使用的移入栈顶，但是用栈的形式会导致执行select * 的时候大量非热点数据占领头部数据，所以需要改进。Redis每次按key获取一个值的时候，都会更新value中的lru字段为当前秒级别的时间戳（意思是，LRU是用sorted set 来实现的）。Redis初始的实现算法很简单，随机从dict中取出五个key,淘汰一个lru字段值最小的。在3.0的时候，又改进了一版算法，首先第一次随机选取的key都会放入一个pool中(pool的大小为16),pool中的key是按lru大小顺序排列的。接下来每次随机选取的key lru值必须小于pool中最小的lru才会继续放入，直到将pool放满。放满之后，每次如果有新的key需要放入，需要将pool中lru最大的一个key取出（最大的意思是，score最大，意味着时间戳最大，很可能是刚刚用过的，所以可以幸免于难）。淘汰的时候，直接从pool中选取一个lru最小的值然后将其淘汰（那这个时候，说明这个pool里面这个还是最早之前使用，最近可能一直没用过）。

### 如何进行缓存预热

1.提前把热点数据塞入redis，但不可能真的评估100%

2.避免20%还是开发逻辑也要规避差集，会造成击穿，穿透雪崩，这样一劳永逸。

### Redis如何发现热点key

1. 凭借经验，进行预估：例如提前知道了某个活动的开启，那么就将此Key作为热点Key。
2. 服务端收集：在操作redis之前，加入一行代码进行数据统计。
3. 抓包进行评估：Redis使用TCP协议与客户端进行通信，通信协议采用的是RESP，所以自己写程序监听端口也能进行拦截包进行解析。
4. 在proxy层，对每一个 redis 请求进行收集上报。
5. Redis自带命令查询：Redis4.0.4版本提供了redis-cli –hotkeys就能找出热点Key。（如果要用Redis自带命令查询时，要注意需要先把内存逐出策略设置为allkeys-lfu或者volatile-lfu，否则会返回错误。进入Redis中使用config set maxmemory-policy allkeys-lfu即可。）

### Redis的热点key解决方案

1. 服务端缓存：即将热点数据缓存至服务端的内存中.（利用Redis自带的消息通知机制来保证Redis和服务端热点Key的数据一致性，对于热点Key客户端建立一个监听，当热点Key有更新操作的时候，服务端也随之更新。)
2. 备份热点Key：即将热点Key+随机数，随机分配至Redis其他节点中。这样访问热点key的时候就不会全部命中到一台机器上了。

### 缓存雪崩

缓存机器意外发生了全盘宕机。缓存挂了，此时 1 秒 5000 个请求全部落数据库，数据库必然扛不住，它会报一下警，然后就挂了

### 缓存穿透

对于系统 A，假设一秒 5000 个请求，结果其中 4000 个请求是黑客发出的恶意攻击。黑客发出的那 4000 个攻击，缓存中查不到，每次你去数据库里查，流量一下子打过来数据库挂了。

### 缓存击穿

缓存击穿，就是说某个 key 非常热点，访问非常频繁，处于集中式高并发访问的情况，当这个 key 在失效的瞬间，大量的请求就击穿了缓存，直接请求数据库，就像是在一道屏障上凿开了一个洞。

### 如何解决 Redis 缓存雪崩问题

1. 使用 Redis 高可用架构：使用 Redis 集群来保证 Redis 服务不会挂掉

### 如何解决 Redis 缓存穿透问题

1. 在接口做校验
2. 存null值（缓存击穿加锁, 或设置不过期）
3. 布隆过滤器拦截： 将所有可能的查询key 先映射到布隆过滤器中，查询时先判断key是否存在布隆过滤器中，存在才继续向下执行，如果不存在，则直接返回。

### 如何解决 Redis 缓存击穿问题

1. 缓存时间不一致，给缓存的失效时间，加上一个随机值，避免集体失效
2. 限流降级策略：有一定的备案，比如个性推荐服务不可用了，换成热点数据推荐服务

1.请求redis，肯定没有

2.大家抢锁 o（只有发生redis取不到的时候）

3.抢到的碰db o（1）

4.没抢到的sleep

5.db更新o（1）

6.sleep的回到第一步

为啥加redis锁：1.你不知道请求是不是并发的 2.保障db的压力

### 布隆过滤

基于hash算法和位数组bit array的，有误判率。如果它说不在，那一定不在，如果它说在，有可能不在。

优点：空间效率高，hashfunction没关系，并行操作，时间效率高。

​             不需要储存数据本身，保密高。

缺点：不能删除，数据越多误判率越低。

【0001000001000100】将zero 的三个hash函数，hash1，hash2， hash3的位置都放入1，

判断的时候，如果这三个位置都是1，那么就是存在（有可能误判，1可能是别的one存进去的）

### COW （copy on write）

面试回答：fork出来的子进程和主进程共享内存。如果主进程同时在修改数据，那么copy on write 机制，相当于会把数据段分成N个数据页，主进程修改的是copy出来的数据页。但是fork的子进程读的数据始终是没有变化的。

COW：子进程刚产生的时候它和主进程共享内存里面的数据段跟代码段，Linux为了节省内存资源，让他们共享起来，在进程分离的一瞬，内存基本没变化。进程分离的步骤大致是：fork函数会在子进程同时返回，在父进程里面返回子进程的pid，在子进程里返回0，如果系统内存资源不足则返回-1，fork失败。

子进程做数据持久化不会修改现有内存数据，只对数据进行遍历然后序列化到磁盘。

这时候有人就会问了：子进程读父进程的数据，主进程此时还对外提供服务，那么主进程肯定会不停的修改内存数据，子进程怎么保证自己读到的数据跟主进程的最新数据一致呢？

这时候我们就得引入系统的COW机制了，COW将数据段分成N个数据页，当主进程修改任意一个页面数据的时候，将会把此页面从共享内存中复制一份分离出来，然后对复制出来的新页面进行修改，此时子进程的内存页是没有变化的。这就是快照的概念了，当fork成功的一瞬间一直到它持久化到磁盘的数据始终是一致的。当下次子线程进入的时候就会共享到那些被修改过的页面数据了（主进程未修改过的+页分离数据）。一般情况下页分离的数量取决于Redis的热数据的多少。

参考：https://zhuanlan.zhihu.com/p/97527245

### Redis和memcached的区别

1. 存储方式上：memcache会把数据全部存在内存之中，断电后会挂掉，数据不能超过内存大小。redis有部分数据存在硬盘上，这样能保证数据的持久性。
2. 数据支持类型上：memcache对数据类型的支持简单，只支持简单的key-value，，而redis支持五种数据类型。
3. 用底层模型不同：它们之间底层实现方式以及与客户端之间通信的应用协议不一样。redis直接自己构建了VM机制，因为一般的系统调用系统函数的话，会浪费一定的时间去移动和请求。
4. value的大小：redis可以达到1GB，而memcache只有1MB。

### Redis并发竞争key的解决方案

1. 分布式锁+时间戳
2. 利用消息队列

### Redis与Mysql双写一致性方案

描述问题：redis是缓存，更倾向于稍微的有时差

​                   为的还是减少db的操作

​                    如果真的要落地，canal

用分布式事务意义不大，为了解决一个问题引入更复杂的问题。

1.客户端都去redis写，然后事后更新到mysql：redis挂掉会丢失数据，数据不一致

2.先写数据库，然后更新redis：

​       数据有时差；

​      如果这个操作由客户端操作，如果更新redis过程失败，数据不一致；由阿里canal binlog来实现，订阅 Mysql 数据库的 binlog 日志对缓存进行操作

3.完全异步化

   客户端放在消息队列中，由消费服务来统一放入redis和mysql

### Redis的管道pipeline

对于单线程阻塞式的Redis，Pipeline可以满足批量的操作，把多个命令连续的发送给Redis Server，然后一一解析响应结果。Pipelining可以提高批量处理性能，提升的原因主要是TCP连接中减少了“交互往返”的时间。pipeline 底层是通过把所有的操作封装成流，redis有定义自己的出入输出流。在 sync() 方法执行操作，每次请求放在队列里面，解析响应包。

### Redis 压缩表 ziplist

ziplist是一个经过特殊编码的 `双向链表` ，它的设计目标就是为了提高存储效率。ziplist可以用于存储字符串或整数，其中整数是按真正的二进制表示进行编码的，而不是编码成字符串序列。 它能以 `O(1)` 的时间复杂度在表的两端提供 `push` 和`pop` 操作。

需要注意的是：

而ziplist 却是将表中每一项存放在前后 `连续的地址空间` 内，一个ziplist整体占用一大块内存。 `它是一个表（list），但其实不是一个链表（linked list）`

ziplist 内部是有header，entry，end标识（255）组成，

entry中存的是连续的 （数据，score）一对数据。最大entry个数为128个，以及最大的entry中的value长度为64，一旦超过了这两个限制中的一个，那么Redis将使用 skiplist 来实现zset结构。并且不会再回退会为ziplist结构。

### Redis 跳表 Skiplist

Redis 里面实现的skiplist是为了sorted set而实现的。skiplist本质上也是一种查找结构，用于解决算法中的查找问题（Searching），即根据给定的key，快速查到它所在的位置（或者对应的value）。它是在有序链表的基础上发展起来的。上面每一层链表的节点个数，是下面一层的节点个数的一半，这样查找过程就非常类似于一个二分查找，使得查找的时间复杂度可以降低到O(log n)。![截屏2021-12-20 下午6.18.00](/Users/jialinzhang/Library/Application Support/typora-user-images/截屏2021-12-20 下午6.18.00.png)

但是，这种方法在插入数据的时候有很大的问题。新插入一个节点之后，就会打乱上下相邻两层链表上节点个数严格的2:1的对应关系。如果要维持这种对应关系，就必须把新插入的节点后面的所有节点（也包括新插入的节点）重新进行调整，这会让时间复杂度重新蜕化成O(n)。删除数据也有同样的问题。

skiplist为了避免这一问题，它不要求上下相邻两层链表之间的节点个数有严格的对应关系，而是为每个节点随机出一个层数(level)。比如，一个节点随机出的层数是3，那么就把它链入到第1层到第3层这三层链表中。

每一个节点的层数（level）是随机出来的，而且新插入一个节点不会影响其它节点的层数。

执行插入操作时计算随机数的过程，是一个很关键的过程，它对skiplist的统计特性有着很重要的影响。这并不是一个普通的服从均匀分布的随机数，它的计算过程如下：

- 首先，每个节点肯定都有第1层指针（每个节点都在第1层链表里）。
- 如果一个节点有第i层(i>=1)指针（即节点已经在第1层到第i层链表中），那么它有第(i+1)层指针的概率为p。
- 节点最大的层数不允许超过一个最大值，记为MaxLevel。

在Redis的skiplist实现中，这两个参数的取值为：

```
p = 1/4
MaxLevel = 32
```


链接：https://juejin.im/post/6844903446475177998

### Redis为什么用skiplist而不用平衡树？

摘自楼上的文章

There are a few reasons:

1) They are not very memory intensive. It's up to you basically. Changing parameters about the probability of a node to have a given number of levels will make then less memory intensive than btrees.

skiplist相对来说不会对内存要求太高，一方面取决于那个level的概率的设置大小。得当的话，占用内存会比 btree少

2) A sorted set is often target of many ZRANGE or ZREVRANGE operations, that is, traversing the skip list as a linked list. With this operation the cache locality of skip lists is at least as good as with other kind of balanced trees.

另外 sorted set 经常会用于范围查找，那像跳表这样的linkedlist的实现遍历的过程就会更快。因为根据局部性原理，linkedlist更能把存储相近的数据一次性加载入内存，减少io。

3) They are simpler to implement, debug, and so forth. For instance thanks to the skip list simplicity I received a patch (already in Redis master) with augmented skip lists implementing ZRANK in O(log(N)). It required little changes to the code.

另外 跳表更容易实现，debug。

### 主从不一致问题

1.redis的确是弱一致的，异步的同步

2.锁不可能用主从（单实例/分片集群/redlock）---》redission

3.在配置中提供了必须有多少个clinet连接能同步，可以配置同步因子，趋向于强一致

4. wait 2 0 小心
5. 从 3 4 点开始违背redis初衷了

### redis 持久化原理

Redis为了保证效率，数据缓存在了内存中，但是会周期性的把更新的数据写入磁盘或者把修改操作写入追加的记录文件中，以保证数据的持久化。Redis的持久化策略有两种：

1. RDB(**Redis** Database Backup)：快照形式是直接把内存中的数据保存到一个dump的文件中，定时保存，保存策略。
   当Redis需要做持久化时，Redis会fork一个子进程，子进程将数据写到磁盘上一个临时RDB文件中。当子进程完成写临时文件后，将原来的RDB替换掉。（BGSAVE，在后台开始执行）（恢复用rdbLoad，）

2. AOF （append only file）：把所有的对Redis的服务器进行修改的命令都存到一个文件里，命令的集合。
   使用AOF做持久化，每一个写命令都通过write函数追加到appendonly.aof中。aof的默认策略是每秒钟fsync一次，在这种配置下，就算发生故障停机，也最多丢失一秒钟的数据。
   缺点是对于相同的数据集来说，AOF的文件体积通常要大于RDB文件的体积。根据所使用的fsync策略，AOF的速度可能会慢于RDB。
   Redis默认是快照RDB的持久化方式。对于主从同步来说，主从刚刚连接的时候，进行全量同步（RDB）；全同步结束后，进行增量同步(AOF)。

   > Redis提供了bgrewriteaof指令对AOF进行重写，其原理就是开辟一个子线程对当前内存进行遍历转化成一个新的文本指令，生成一个新的AOF文件保存在操作系统cache中，操作系统再异步将这个cache中的数据写到磁盘，生成真正的AOF文件

### Redis 哨兵模式高可用

参考：https://github.com/doocs/advanced-java/blob/master/docs/high-concurrency/redis-sentinel.md

哨兵介绍：哨兵是 Redis 集群架构中非常重要的一个组件，主要有以下功能：

- 集群监控：负责监控 Redis master 和 slave 进程是否正常工作。
- 消息通知：如果某个 Redis 实例有故障，那么哨兵负责发送消息作为报警通知给管理员。
- 故障转移：如果 master node 挂掉了，会自动转移到 slave node 上。
- 配置中心：如果故障转移发生了，通知 client 客户端新的 master 地址。

哨兵用于实现 Redis 集群的高可用，本身也是分布式的，作为一个哨兵集群去运行，互相协同工作。

- 故障转移时，判断一个 master node 是否宕机了，需要大部分的哨兵都同意才行，涉及到了分布式选举的问题。
- 即使部分哨兵节点挂掉了，哨兵集群还是能正常工作的，因为如果一个作为高可用机制重要组成部分的故障转移系统本身是单点的，那就很坑爹了。

基础：

哨兵至少需要 3 个实例，来保证自己的健壮性。

哨兵 + Redis 主从的部署架构，是**不保证数据零丢失**的，**只能保证 Redis 集群的高可用性。**



redis**主备切换数据丢失**的2种情况

- 主备切换的过程，可能会导致数据丢失：异步复制导致的数据丢失。因为master->slave 的复制是异步的，所以可能有部分数据还没复制到 slave，master 就宕机了，此时这部分数据就丢失了

- 脑裂导致的数据丢失：此时虽然某个 slave 被切换成了 master，但是可能 client 还没来得及切换到新的 master，还继续向旧 master 写数据。因此旧 master 再次恢复的时候，会被作为一个 slave 挂到新的 master 上去，自己的数据会清空，重新从新的 master 复制数据。而新的 master 并没有后来 client 写入的数据，因此，这部分数据也就丢失了。

数据丢失解决方案：

```
min-slaves-to-write 1
min-slaves-max-lag 10
```

表示，要求至少有 1 个 slave，数据复制和同步的延迟不能超过 10 秒。

- 减少异步复制数据的丢失

有了 `min-slaves-max-lag` 这个配置，就可以确保说，一旦 slave 复制数据和 ack 延时太长，就认为可能 master 宕机后损失的数据太多了，那么就拒绝写请求，这样可以把 master 宕机时由于部分数据未同步到 slave 导致的数据丢失降低的可控范围内。

- 减少脑裂的数据丢失

如果一个 master 出现了脑裂，跟其他 slave 丢了连接，那么上面两个配置可以确保说，如果不能继续给指定数量的 slave 发送数据，而且 slave 超过 10 秒没有给自己 ack 消息，那么就直接拒绝客户端的写请求。因此在脑裂场景下，最多就丢失 10 秒的数据。

## Mysql

### 事务的基本要素

1. 原子性：事务是一个原子操作单元，其对数据的修改，要么全都执行，要么全都不执行
2. 一致性：事务开始前和结束后，数据库的完整性约束没有被破坏。
3. 隔离性：同一时间，只允许一个事务请求同一数据，不同的事务之间彼此没有任何干扰。
4. 持久性：事务完成后，事务对数据库的所有更新将被保存到数据库，不能回滚。

### Mysql的存储引擎

InnoDB 和 MyISAM区别：

InnoDB支持事务，MyISAM 不支持事务

InnoDB有行锁设计，MyISAM表锁

InnoDB 聚簇索引，MyISAM 非聚簇索引

1. InnoDB存储引擎：InnoDB存储引擎支持事务，其设计目标主要面向在线事务处理（OLTP）的应用。其特点是行锁设计，支持外键，并支持非锁定锁，即默认读取操作不会产生锁。从Mysql5.5.8版本开始，InnoDB存储引擎是默认的存储引擎。
2. MyISAM存储引擎：MyISAM存储引擎不支持事务、表锁设计，支持全文索引，主要面向一些OLAP数据库应用。InnoDB的数据文件本身就是主索引文件，而MyISAM的主索引和数据是分开的。（非聚簇索引）
3. NDB存储引擎：NDB存储引擎是一个集群存储引擎，其结构是share nothing的集群架构，能提供更高的可用性。NDB的特点是数据全部放在内存中（从MySQL 5.1版本开始，可以将非索引数据放在磁盘上），因此主键查找的速度极快，并且通过添加NDB数据存储节点可以线性地提高数据库性能，是高可用、高性能的集群系统。NDB存储引擎的连接操作是在MySQL数据库层完成的，而不是在存储引擎层完成的。这意味着，复杂的连接操作需要巨大的网络开销，因此查询速度很慢。如果解决了这个问题，NDB存储引擎的市场应该是非常巨大的。
4. Memory存储引擎：Memory存储引擎（之前称HEAP存储引擎）将表中的数据存放在内存中，如果数据库重启或发生崩溃，表中的数据都将消失。它非常适合用于存储临时数据的临时表，以及数据仓库中的纬度表。Memory存储引擎默认使用哈希索引，而不是我们熟悉的B+树索引。虽然Memory存储引擎速度非常快，但在使用上还是有一定的限制。比如，只支持表锁，并发性能较差，并且不支持TEXT和BLOB列类型。最重要的是，存储变长字段时是按照定长字段的方式进行的，因此会浪费内存。
5. Archive存储引擎：Archive存储引擎只支持INSERT和SELECT操作，从MySQL 5.1开始支持索引。Archive存储引擎使用zlib算法将数据行（row）进行压缩后存储，压缩比一般可达1∶10。正如其名字所示，Archive存储引擎非常适合存储归档数据，如日志信息。Archive存储引擎使用行锁来实现高并发的插入操作，但是其本身并不是事务安全的存储引擎，其设计目标主要是提供高速的插入和压缩功能。
6. Maria存储引擎：Maria存储引擎是新开发的引擎，设计目标主要是用来取代原有的MyISAM存储引擎，从而成为MySQL的默认存储引擎。它可以看做是MyISAM的后续版本。Maria存储引擎的特点是：支持缓存数据和索引文件，应用了行锁设计，提供了MVCC功能，支持事务和非事务安全的选项，以及更好的BLOB字符类型的处理性能。

### 事务的并发问题

1. 脏读：事务A读取了事务B更新的数据，然后B回滚操作，那么A读取到的数据是脏数据
2. 不可重复读：事务A多次读取同一数据，事务B在事务A多次读取的过程中，对数据作了更新并提交，导致事务A多次读取同一数据时，结果不一致。（针对 update ）
3. 幻读：A事务读取了B事务已经提交的新增数据。注意和不可重复读的区别，这里是 insert 新增（或删除），不可重复读是更改。select某记录是否存在，不存在，准备插入此记录，但执行 insert 时发现此记录已存在，无法插入，此时就发生了幻读。

### MySQL事务隔离级别

| 事务隔离级别                   | 脏读 | 不可重复读 | 幻读 |
| ------------------------------ | ---- | ---------- | ---- |
| 读未提交 （read uncommitted ） | 是   | 是         | 是   |
| 不可重复读 Read committed      | 否   | 是         | 是   |
| 可重复读 Repeatable read       | 否   | 否         | 是   |
| 串行化 Serializable            | 否   | 否         | 否   |

### 锁机制 - InnoDB的实现，锁释放时机

锁机制：阻止其他事务对数据进行操作， 各个隔离级别主要体现在读取数据时加的锁的释放时机。

- RU：事务读取时不加锁
- RC：事务读取时加行级共享锁（读到才加锁），一旦读完，立刻释放（并不是事务结束）。
- RR：事务读取时加**行级共享锁**，直到事务结束时，才会释放。
- SE：事务读取时加**表级共享锁**，直到事务结束时，才会释放。

### Mysql默认隔离级别是RR

为什么默认的是RR但是一般都用RC？RC会出现什么问题？

> Bin Log 的格式：binlog有两种格式，一种是statement,一种是row

为什么statement的格式会导致主从不一致？

> statement记录的是sql语句原文，而row格式记录的是执行的逻辑过程。

参考：https://dominicpoi.com/2019/06/16/MySQL-1/

在MySQL5.0之前，binlog只支持statement。这样根据事务的提交顺序，我们可以得知binlog中的statement如下：

```
insert into test values(3); -- session2先提交
delete from test where b <= 6; -- session1后提交
```

显然，在master上执行这两个事务，得到的查询结果应当是有一条记录b=3的，然而因为statement记录的原因，从库在根据binlog同步的时候，就会变先删后插为先插后删。查询的结果就变成了**Empty set**。

> 为什么RR为了实现真正的“可重复读”？ 因为引入了间隙锁（Gap lock），不仅锁住了行，而且锁住了行与行之间的间隙，避免出现幻读



### Mysql的逻辑结构

* 最上层的服务类似其他CS结构，比如连接处理，授权处理。
* 第二层是Mysql的服务层，包括SQL的解析分析优化，存储过程触发器视图等也在这一层实现。
* 最后一层是存储引擎的实现，类似于Java接口的实现，Mysql的执行器在执行SQL的时候只会关注API的调用，完全屏蔽了不同引擎实现间的差异。比如Select语句，先会判断当前用户是否拥有权限，其次到缓存（内存）查询是否有相应的结果集，如果没有再执行解析sql，检查SQL 语句语法是否正确，再优化生成执行计划，调用API执行。

### SQL执行顺序

SQL的执行顺序：from---where--group by---having---select---order by

### MVCC,redolog,undolog,binlog

* Undo log：保存了事务发生之前的数据的一个版本（被修改前的值），可以用于回滚，同时可以提供多版本并发控制下的读（MVCC），也即非锁定读。当事务提交之后，undo log并不能立马被删除, 而是会被放到待清理链表中,待判断没有事务用到该版本的信息时才可以清理相应undolog。

* redo log 是重做日志，innodb level，确保数据的持久性。记录的是数据修改后的值。不管事务是否提交都会记录下来。执行更新操作时，会把更新操作写进redo log，然后更新内存。然后在空闲的时候或者是按照设定的更新策略将redo log中的内容更新到磁盘中，这里涉及到`WAL`即`Write Ahead logging`技术，他的关键点是先写日志，再写磁盘。redo log日志的大小是固定的，即记录满了以后就从头循环写。（一些注意事项：修改的数据一般会先存在buffer pool，这时候和磁盘的不一致，会把buffer pool里面的数据叫做脏数据页 dirty page。因为写到磁盘是随机IO，所以有可能MySQL崩溃但是数据还没写到磁盘。但是redo log 存的是修改的值，并且是一个 write ahead logging。所以可以用redo log里面的数据恢复）

* bin log：MySQL level，属于逻辑日志，是以二进制的形式记录的是这个语句的原始逻辑。

* MVCC多版本并发控制是MySQL中基于乐观锁理论实现隔离级别的方式，用于读已提交（RC）和可重复读取（RR）隔离级别的实现。在MySQL中，会在表中每一条数据后面添加两个字段：最近修改该行数据的事务ID，指向该行（undolog表中）回滚段的指针。Read View判断行的可见性，创建一个新事务时，copy一份当前系统中的活跃事务列表。意思是，当前不应该被本事务看到的其他事务id列表。 ->> 

* > 已提交读隔离级别下的事务在每次查询的开始都会生成一个独立的ReadView, 而可重复读隔离级别则在第一次读的时候生成一个ReadView，之后的读都复用之前的ReadView。

* Undolog  是否是redolog的逆过程？ 不是。undolog 是逻辑日志(记录的是select这样的操作)，对事务的回滚时，只是将数据库逻辑的恢复到原来的样子。而 redolog 是物理日志，记录的是数据页的物理变化（就是数据的变化）。

### binlog和redolog的区别

- redo log是属于innoDB层面，binlog属于MySQL Server层面的，这样在数据库用别的存储引擎时可以达到一致性的要求。
- redo log是物理日志，记录该数据页更新的内容；binlog是逻辑日志，记录的是这个更新语句的原始逻辑
- redo log是循环写，日志空间大小固定；binlog是追加写，是指一份写到一定大小的时候会更换下一个文件，不会覆盖。
- binlog可以作为恢复数据使用，主从复制搭建，redo log作为异常宕机或者介质故障后的数据恢复使用。MySQL level 的。逻辑日志。

### Mysql 删除数据

DELETE只是将数据标识为删除，并没有整理数据文件，当插入新数据后，会再次使用这些被置为删除标识的记录空间，可以使用OPTIMIZE TABLE来回收未使用的空间，并整理数据文件的碎片。

### Mysql读写分离以及主从同步

1. 原理：主库将更新写binlog日志，然后从库连接到主库后，从库有一个IO线程，将主库的binlog日志拷贝到自己本地，写入一个中继日志中，接着从库中有一个sql线程会从中继日志读取binlog，然后执行binlog日志中的内容，也就是在自己本地再执行一遍sql，这样就可以保证自己跟主库的数据一致。
2. 问题：这里有很重要一点，就是从库同步主库数据的过程是串行化的，也就是说主库上并行操作，在从库上会串行化执行，由于从库从主库拷贝日志以及串行化执行sql特点，在高并发情况下，从库数据一定比主库慢一点，是有延时的，所以经常出现，刚写入主库的数据可能读不到了，要过几十毫秒，甚至几百毫秒才能读取到。还有一个问题，如果突然主库宕机了，然后恰巧数据还没有同步到从库，那么有些数据可能在从库上是没有的，有些数据可能就丢失了。所以mysql实际上有两个机制，一个是半同步复制，用来解决主库数据丢失问题，一个是并行复制，用来解决主从同步延时问题。
3. 半同步复制：semi-sync复制，指的就是主库写入binlog日志后，就会将强制此时立即将数据同步到从库，从库将日志写入自己本地的relay log之后，接着会返回一个ack给主库，主库接收到至少一个从库ack之后才会认为写完成。
4. 并发复制：指的是从库开启多个线程，并行读取relay log中不同库的日志，然后并行重放不同库的日志，这样库级别的并行。（将主库分库也可缓解延迟问题）
### Next-Key Lock

InnoDB 采用 Next-Key Lock 解决幻读问题。

在`insert into test(xid) values (1), (3), (5), (8), (11);`后，由于xid上是有索引的，该算法总是会去锁住索引记录。现在，该索引可能被锁住的范围如下：(-∞, 1], (1, 3], (3, 5], (5, 8], (8, 11], (11, +∞)。Session A（`select * from test where id = 8 for update`）执行后会锁住的范围：(5, 8], (8, 11]。除了锁住8所在的范围，还会锁住下一个范围，所谓Next-Key。

### InnoDB的关键特性

1. 插入缓冲：对于非聚集索引的插入或更新操作，不是每一次直接插入到索引页中，而是先判断插入的非聚集索引页是否在缓冲池中，若在，则直接插入；若不在，则先放入到一个Insert Buffer对象中。然后再以一定的频率和情况进行Insert Buffer和辅助索引页子节点的merge（合并）操作，这时通常能将多个插入合并到一个操作中（因为在一个索引页中），这就大大提高了对于非聚集索引插入的性能。
2. 两次写：两次写带给InnoDB存储引擎的是数据页的可靠性，有经验的DBA也许会想，如果发生写失效，可以通过重做日志进行恢复。这是一个办法。但是必须清楚地认识到，如果这个页本身已经发生了损坏（物理到page页的物理日志成功，页内逻辑日志失败），再对其进行重做是没有意义的。这就是说，在应用（apply）重做日志前，用户需要一个页的副本，当写入失效发生时，先通过页的副本来还原该页，再进行重做。在对缓冲池的脏页进行刷新时，并不直接写磁盘，而是会通过memcpy函数将脏页先复制到内存中的doublewrite buffer，之后通过doublewrite buffer再分两次，每次1MB顺序地写入共享表空间的物理磁盘上，这就是doublewrite。
3. 自适应哈希索引：InnoDB存储引擎会监控对表上各索引页的查询。如果观察到建立哈希索引可以带来速度提升，则建立哈希索引，称之为自适应哈希索引。
4. 异步IO：为了提高磁盘操作性能，当前的数据库系统都采用异步IO（AIO）的方式来处理磁盘操作。AIO的另一个优势是可以进行IO Merge操作，也就是将多个IO合并为1个IO，这样可以提高IOPS的性能。
5. 刷新邻接页：当刷新一个脏页时，InnoDB存储引擎会检测该页所在区（extent）的所有页，如果是脏页，那么一起进行刷新。这样做的好处显而易见，通过AIO可以将多个IO写入操作合并为一个IO操作，故该工作机制在传统机械磁盘下有着显著的优势。

### Mysql如何保证一致性和持久性

MySQL为了保证ACID中的一致性和持久性，使用了WAL(Write-Ahead Logging,先写日志再写磁盘)。Redo log就是一种WAL的应用。当数据库忽然掉电，再重新启动时，MySQL可以通过Redo log还原数据。也就是说，每次事务提交时，不用同步刷新磁盘数据文件，只需要同步刷新Redo log就足够了。

### MySQL行锁的实现

**InnoDB行锁是通过给索引上的索引项加锁来实现的**

InnoDB这种行锁实现特点意味着：只有通过索引条件检索数据，InnoDB才使用行级锁，否则，InnoDB将使用表锁！

参考：https://lanjingling.github.io/2015/10/10/mysql-hangsuo/

1. **在不通过索引条件查询的时候，InnoDB确实使用的是表锁，而不是行锁**：例子：

    ```
    students 表格没有建立索引。
    session 1:
    select from students where id = 1 for update;
    
    session 2:
    select from students where id = 2 for update; （这个时候，会被阻塞。因为session1 中在查询的时候给表加了锁）
    ```

    ⚠️：有了索引以后，在对索引字段查询时，使用的就是行级锁：

    

2. **由于MySQL的行锁是针对索引加的锁，不是针对记录加的锁，所以虽然是访问不同行的记录，但是如果是使用相同的索引键，是会出现锁冲突的**

3. 当表有多个索引的时候，不同的事务可以使用不同的索引锁定不同的行，另外，不论是使用主键索引、唯一索引或普通索引，InnoDB都会使用行锁来对数据加锁

### InnoDB的行锁模式

* 共享锁(S)：用法lock in share mode，又称读锁，允许一个事务去读一行，阻止其他事务获得相同数据集的排他锁。若事务T对数据对象A加上S锁，则事务T可以读A但不能修改A，其他事务只能再对A加S锁，而不能加X锁，直到T释放A上的S锁。这保证了其他事务可以读A，但在T释放A上的S锁之前不能对A做任何修改。
* 排他锁(X)：用法for update，又称写锁，允许获取排他锁的事务更新数据，阻止其他事务取得相同的数据集共享读锁和排他写锁。若事务T对数据对象A加上X锁，事务T可以读A也可以修改A，其他事务不能再对A加任何锁，直到T释放A上的锁。在没有索引的情况下，InnoDB只能使用表锁。

### MySQL 死锁

1. 设置 innodb wait time out=50s 太大不能忍，太小会有误伤
2. 开启inoodb deadlock detect 消耗资源

如何预防？

   1.减少长事务

   2.大事务拆分成小事务，结合业务需求

   3.保持加锁顺序一致，尽量一次性锁住随需要的行

   4.在允许的情况下，降低隔离级别（比如读提交）rr的间隙锁会提高发生死锁的概率

如何排查和解决？1。日志通知死锁事件 2.show engine innodb status死锁日志结合分析

死锁的关键在于：两个(或以上)的Session加锁的顺序不一致。

几个加锁算法：

- next KeyLocks锁，同时锁住记录(数据)，并且锁住记录前面的Gap  
- Gap锁，不锁记录，仅仅记录前面的Gap
- Recordlock锁（锁数据，不锁Gap）
- 所以其实 Next-KeyLocks=Gap锁+ Recordlock锁



要注意，innodb 中，只有通过索引查询加的才是行锁，否则是表锁

当对`存在的行`进行锁的时候(主键)，mysql就只有行锁。
当对`未存在的行`进行锁的时候(即使条件为主键)，mysql是会锁住一段范围（有gap锁）

锁住的范围为：

(无穷小或小于表中锁住id的最大值，无穷大或大于表中锁住id的最小值)

如：如果表中目前有已有的id为（11 ， 12）

那么就锁住（12，无穷大）

如果表中目前已有的id为（11 ， 30）

那么就锁住（11，30）

对于这种死锁的解决办法是：

insert into t3(xx,xx) on duplicate key update `xx`='XX';

用mysql特有的语法来解决此问题。**因为insert语句对于主键来说，插入的行不管有没有存在，都会只有行锁**



**死锁产生的几个前提：**

- Delete操作，针对的是唯一索引上的等值查询的删除；(范围下的删除，也会产生死锁，但是死锁的场景，跟本文分析的场景，有所不同)
- 至少有3个(或以上)的并发删除操作；
- 并发删除操作，有可能删除到同一条记录，并且保证删除的记录一定存在；
- 事务的隔离级别设置为Repeatable Read，同时未设置innodb_locks_unsafe_for_binlog参数(此参数默认为FALSE)；(Read Committed隔离级别，由于不会加Gap锁，不会有next key，因此也不会产生死锁)
- 使用的是InnoDB存储引擎；(废话！MyISAM引擎根本就没有行锁)

### MySQL explain 执行计划

执行计划里面有的列：

id, select_type, table, type, possible_keys, key, key_len, ref, rows, extra

id：包含一组数字，表示查询中执行select子句或操作表的顺序。id相同，执行顺序由上至下。id值越大优先级越高，越先被执行

select_type: 表示查询中每个select子句的类型（简单 OR复杂）

```
a.SIMPLE：查询中不包含子查询或者UNION
b.查询中若包含任何复杂的子部分，最外层查询则被标记为：PRIMARY
c.在SELECT或WHERE列表中包含了子查询，该子查询被标记为：SUBQUERY
d.在FROM列表中包含的子查询被标记为：DERIVED（衍生）
e.若第二个SELECT出现在UNION之后，则被标记为UNION；若UNION包含在  FROM子句的子查询中，外层SELECT将被标记为：DERIVED
f.从UNION表获取结果的SELECT被标记为：UNION RESULT
```

Type: 表示MySQL在表中找到所需行的方式，又称“访问类型”，常见类型如下：

```
a.ALL：Full Table Scan， MySQL将遍历全表以找到匹配的行
b.index：Full Index Scan，index与ALL区别为index类型只遍历索引树
c.range：索引范围扫描，对索引的扫描开始于某一点，返回匹配值域的行，常见于between、<、>等的查询
d.ref：非唯一性索引扫描，返回匹配某个单独值的所有行。常见于使用非唯一索引即唯一索引的非唯一前缀进行的查找
e.eq_ref：唯一性索引扫描，对于每个索引键，表中只有一条记录与之匹配。常见于主键或唯一索引扫描
f.const、system：当MySQL对查询某部分进行优化，并转换为一个常量时，使用这些类型访问。如将主键置于where列表中，MySQL就能将该查询转换为一个常量
g.NULL：MySQL在优化过程中分解语句，执行时甚至不用访问表或索引
```

Possible_keys: 指出MySQL能使用哪个索引在表中找到行，查询涉及到的字段上若存在索引，则该索引将被列出，但不一定被查询使用

Key: 显示MySQL在查询中实际使用的索引，若没有使用索引，显示为NULL

Key_len: 表示索引中使用的字节数，可通过该列计算查询中使用的索引的长度

Ref: 表示上述表的连接匹配条件，即哪些列或常量被用于查找索引列上的值

Rows: 表示MySQL根据表统计信息及索引选用情况，估算的找到所需的记录所需要读取的行数

Extra: 包含不适合在其他列中显示但十分重要的额外信息

```
a.Using index
b.Using where
c.Using temporary
```

参考：https://www.cnblogs.com/ggjucheng/archive/2012/11/11/2765237.html

### 索引为什么快

1. 索引本身就是一个排序好的结构，并且比原表小很多，可以一次加载很多进入内存，减少IO开销。
2. 索引确定了数据位置，直接读取磁盘上相应数据块，速度快

参考：https://www.zhihu.com/question/20759653/answer/16161189

### 为什么选择B+树作为索引结构

选择B+树的原因是树高低，IO量可以减少。并且数据都集中在叶子结点，并且有双向链表连接，便于范围查询。

* Hash索引：Hash索引底层是哈希表，哈希表是一种以key-value存储数据的结构，所以多个数据在存储关系上是完全没有任何顺序关系的，所以，对于区间查询是无法直接通过索引查询的，就需要全表扫描。所以，哈希索引只适用于等值查询的场景。而B+ 树是一种多路平衡查询树，所以他的节点是天然有序的（左子节点小于父节点、父节点小于右子节点），所以对于范围查询的时候不需要做全表扫描
* 二叉查找树：解决了排序的基本问题，但是由于无法保证平衡，可能退化为链表。
* 平衡二叉树：通过旋转解决了平衡的问题，但是旋转操作效率太低。
* 红黑树：通过舍弃严格的平衡和引入红黑节点，解决了AVL旋转效率过低的问题，但是在磁盘等场景下，树仍然太高，IO次数太多。
* B+树：在B树的基础上，将非叶节点改造为不存储数据纯索引节点，进一步降低了树的高度；此外将叶节点使用指针连接成链表，范围查询更加高效。

### 常见的index数据结构

我们常用的数据结构有数组、链表、散列表、树等

1. **数组**支持快速查找，但是需要占用大量的连续存储空间、为了保证顺序存储，增删元素可能需要移动大量数据；
2. **链表**不用占用连续存储空间，但不支持快速查找，在非首尾结点增删元素也比较麻烦；
3. **散列表**可以进行快速查找，但是只支持等值匹配，不支持区间查找和顺序查找；
4. 在双向链表之上加多层索引可以改造出跳表，跳表也可以实现快速查找，区间查询，顺序查询。如果忽略看过的 B+ 树与跳表的示意图，二者已十分接近。
5. 关于 B 树 与 B+ 树
    1. B 树遍历元素时效率低下，B+ 树只需要去遍历叶子节点就可以实现整棵树的遍历，而在 B树 中遍历数据则需要进行中序遍历。数据库中基于范围的查询是十分频繁，B 树不支持这样的操作或者说效率太低。
    2. B+ 树中间节点只存索引，不存数据，所以体积更小，在磁盘大小一定（如4KB）时，相比 B 树，磁盘可以存储更多 B+ 树节点，一次读入内存的数据项也更多，减少了 IO 次数。
    3. B+ 树的查找更稳定，数据都存储在叶子节点上，查找数据总是要走到叶子节点，而 B 树查找到数据后就返回。

### B+树的叶子节点都可以存哪些东西

对于聚簇索引，存储的是整行数据，对于非聚簇索引存的是主键的值。

### 为什么普通索引不能存储数据地址

存储主键键值和存储记录地址在作用上是一样的，因为聚集索引就存储了完整的数据记录，通过主键找到数据和通过记录地址查找数据是一样的，但是如果存储的是记录地址的话，如果数据记录发生了**页裂变**导致数据地址变了，那辅助索引也要更新，对于这种情况来说存储主键更好

### 覆盖索引

指一个查询语句的执行只用从索引中就能够取得，不必从数据表中读取。

```
前提，table表对于id 和 name 都建立了索引
select * from table where name = ?;//需要回表，因为要根据id再回到id的B+ tree进行查找
select id from table where name = ?;//不需要回表，因为这个时候我只要id，直接拿到，这就是索引覆盖
```

参考： https://juejin.im/post/6844904062329028621

普通索引：

如果查询条件为普通索引（非聚簇索引），需要扫描两次B+树，第一次扫描通过普通索引定位到聚簇索引的值，然后第二次扫描通过聚簇索引的值定位到要查找的行记录数据。

### 查询在什么时候不走（预期中的）索引

1. 模糊查询 %like
2. 索引列参与计算,使用了函数
3. 非最左前缀顺序
4. where对null判断 
5. where不等于
6. or操作有至少一个字段没有索引
7. 需要回表的查询结果集过大（超过配置的范围）

### 唯一索引和普通索引

参考：https://zhuanlan.zhihu.com/p/69369688

总结：如果业务能保证唯一性的情况下，还是选择普通索引性能更好

```
select id from T where k=5
```

对于普通索引来说，查询到满足条件的第一个记录后，需要查找下一个记录，直到碰到第一个不满足k=5条件的记录

对于唯一索引来说，由于索引上有唯一性，查询到第一个满足条件的记录后就停止检索了

#### 更新过程

首先我们说下change_buffer的概念，如果要更新的数据在内存中，那么就直接更新内存，如果要更新的数据没有在内存中，那么就会把更新记录存在change_buffer中，等到有**查询来读取数据页**的时候，就会执行change_buffer中有关这个数据页的操作。通过这种方式就能保证这个数据逻辑的正确性。

#### 唯一索引不用change buffer

对于唯一索引来说，每次更新都必须先判断这个操作是否违反唯一性约束，所以必须要将数据页读入内存才能判断，既然都读入内存了，那么直接更新内存会更快，就没必要使用change buffer了。

因此，唯一索引的更新就不能使用change buffer

更新的过程：

**如果这个记录要更新的目标页不在内存中**，流程如下:

- 对于唯一索引来说，由于需要判断唯一性，所以要从磁盘中读取所在的数据页到内存中，判断到没有冲突，插入值，结束
- 对于普通索引来说，则是将更新记录在change buffer，结束

### 分析 change buffer 应用场景

但是：change buffer 应用场景：写多读少

但是change buffer的应用场景只是对于**写多读少**的的业务，页面在写完以后马上被访问的概率比较小，此时change buffer的使用效果最好，这种业务模型常见的就是账单类，日志类的系统。

反过来，在读多写少的场景，如果一个业务的更新模式是写完之后马上会做查询，那么即使满足了条件，将更新记录在change buffer，但之后由于马上要访问这个数据页，会立即触发Merge过程，这样**随机访问io的次数不会减少，反而增加了change buffer的维护代价**。所以，对于这种业务模式来说，change buffer反而起到了反作用。



### 数据库优化指南

1. 创建并使用正确的索引
2. 只返回需要的字段
3. 减少交互次数（批量提交）
4. 设置合理的Fetch Size（数据每次返回给客户端的条数）

### 分库分表

水平拆分：就是把数据拆分开，比如原来500w，现在分完每个表200w的数据量

垂直拆分：就是把表中的列拆开。

水平分表按照什么拆分：按照 用户ID，取哈希分表

分布式ID如何生成：一个公共组建生成，大概是雪花算法。（雪花算法就是第一位不用，接下来的前41位位是时间戳，精确到毫秒，后面10位是工作机器ID，后12位是序列号。缺点是依赖时钟，可能会导致重复ID生成）

# **JVM**

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

### 对象头具体包括什么

1.锁标记位：有两位用来标志次对象是否被锁定

2.gc标记：对象被回收多少次，分代年龄4bit

3.hashcode：没有被重写时才会被写在这里 system.identityhashcode()

4.线程id：使用偏向锁时，也就是锁标记为01会出现

等等                 

### Java对象分配的过程

![截屏2021-12-19 下午9.50.36](/Users/jialinzhang/Desktop/截屏2021-12-19 下午9.50.36.png)

### 对象内存分配的两种方法

1. 指针碰撞(Serial、ParNew等带Compact过程的收集器) ：假设Java堆中内存是绝对规整的，所有用过的内存都放在一边，空闲的内存放在另一边，中间放着一个指针作为分界点的指示器，那所分配内存就仅仅是把那个指针向空闲空间那边挪动一段与对象大小相等的距离，这种分配方式称为“指针碰撞”（Bump the Pointer）。 
2. 空闲列表(CMS这种基于Mark-Sweep算法的收集器) ：如果Java堆中的内存并不是规整的，已使用的内存和空闲的内存相互交错，那就没有办法简单地进行指针碰撞了，虚拟机就必须维护一个列表，记录上哪些内存块是可用的，在分配的时候从列表中找到一块足够大的空间划分给对象实例，并更新列表上的记录，这种分配方式称为“空闲列表”（Free List）。   

### TLAB Threadlocal Allocation Buffer

多线程创建对象并发问题，解决：

内存分配的动作按照线程划分在不同的空间之中进行，即每个线程在Java堆中预先分配一小块内存，称为本地线程分配缓冲（Thread Local Allocation Buffer, TLAB）。

哪个线程要分配内存，就在哪个线程的TLAB上分配，只有TLAB用完并分配新的TLAB时，才需要同步锁定。虚拟机是否使用TLAB，可以通过-XX:+/-UseTLAB参数来设定。通常默认的TLAB区域大小是Eden区域的1%

### 内存溢出如何线上排查

StackOverFlow：

Thrown when a stack overflow occurs because an application recurses too deeply.

调用栈深度超过限制，递归运算时会遇到 / xss设置太小

OOM：Out of memory
当JVM分配内存时 不够才会抛出异常

OOM 又分为很多种：

- Java Heap Space：代码问题极大,拿出堆内存快照，定位代码
- GC overhead limit exceeded：GC回收时间过长时会抛出该异常。过长的定义是，超过98%的时间用来做GC并且回收了不到2%的堆内存，连续多次GC都只回收了不到2%的极端情况下才会抛出。避免恶性循环 浪费CPU性能
- Direct buffer memory: ByteBuffer.allocateDirect 在堆外内存创建过多对象（DirectByteBuffer），导致本地内存用光。开启netty诊断参数，在本地复现
- Unbale to create new native thread: (应用创建了太多线程，服务器一般允许单个进程创建1024个线程)
- Metaspace: 

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

### 常见的垃圾收集器

![截屏2021-12-19 下午10.09.10](/Users/jialinzhang/Library/Application Support/typora-user-images/截屏2021-12-19 下午10.09.10.png)

serial：a stop the world，copying collector which use a single gc thread

1.serial + serial old：停顿时间太长，基本不用了。

parallel scavenge: a STW,copying collector use multiple gc threads

2.Ps + po: jdk版本默认的，cms缺点太大

3.parnew+cms ：parnew和ps区别就是可以配合cms使用

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

### volitale 实现

jvm层面就是一种规范，使用屏障，cpu底层使用原子指令/intel lock指令

StoreStoreBarrier

volitale 写操作

StoreLoadBarrier

——————————

LoadLoadBarrier

Volatile读操作

loadstorebarrier

### synchronize 实现

hotspot效率高的原因！--锁升级

sync（object）第一个线程进入时，markword记录这个线程的id（偏向锁），如果还是这个线程直接使用，如果有别的线程征用，这时候才升级为自旋锁（用一个while循环自己转圈等待，默认旋转10次之后），如果还没有得到这把锁，升级为重量级锁（os，进入等待队列，不在占有cpu了）就在那边等待。

什么时候用自旋锁？虽然占cpu，但在在用户态不进入内核态。

加锁的代码执行时间短，线程数少--》自旋锁

执行时间长，线程数多-〉系统锁

### JVM锁优化和膨胀过程

1. 自旋锁：自旋锁其实就是在拿锁时发现已经有线程拿了锁，这个时候会选择进行一次忙循环尝试。也就是不停循环看是否能等到上个线程自己释放锁。自适应自旋锁指的是例如第一次设置最多自旋10次，结果在自旋的过程中成功获得了锁，那么下一次就可以设置成最多自旋20次。
2. 锁粗化：虚拟机通过适当扩大加锁的范围以避免频繁的拿锁释放锁的过程。
3. 锁消除：通过逃逸分析发现其实根本就没有别的线程产生竞争的可能（别的线程没有临界量的引用），或者同步块内进行的是原子操作，而“自作多情”地给自己加上了锁。有可能虚拟机会直接去掉这个锁。
4. 偏向锁：在大多数的情况下，锁不仅不存在多线程的竞争，而且总是由同一个线程获得。因此为了让线程获得锁的代价更低引入了偏向锁的概念。偏向锁的意思是如果一个线程获得了一个偏向锁，如果在接下来的一段时间中没有其他线程来竞争锁，那么持有偏向锁的线程再次进入或者退出同一个同步代码块，不需要再次进行抢占锁和释放锁的操作。
5. 轻量级锁：当存在超过一个线程在竞争同一个同步代码块时，会发生偏向锁的撤销。当前线程会尝试使用CAS来获取锁，当自旋超过指定次数(可以自定义)时仍然无法获得锁，此时锁会膨胀升级为重量级锁。
6. 重量级锁：重量级锁依赖对象内部的monitor锁来实现，而monitor又依赖操作系统的MutexLock（互斥锁）。当系统检查到是重量级锁之后，会把等待想要获取锁的线程阻塞，被阻塞的线程不会消耗CPU，但是阻塞或者唤醒一个线程，都需要通过操作系统来实现。

### 什么情况下需要开始类加载过程的第一个阶段加载

1. 遇到new、getstatic、putstatic或invokestatic这4条字节码指令时，如果类没有进行过初始化，则需要先触发其初始化。生成这4条指令的最常见的Java代码场景是：使用new关键字实例化对象的时候、读取或设置一个类的静态字段（被final修饰、已在编译期把结果放入常量池的静态字段除外）的时候，以及调用一个类的静态方法的时候。
2. 使用java.lang.reflect包的方法对类进行反射调用的时候，如果类没有进行过初始化，则需要先触发其初始化。
3. 当初始化一个类的时候，如果发现其父类还没有进行过初始化，则需要先触发其父类的初始化。
4. 当虚拟机启动时，用户需要指定一个要执行的主类（包含main（）方法的那个类），虚拟机会先初始化这个主类。

### i++操作的字节码指令

1. 将int类型常量加载到操作数栈顶
2. 将int类型数值从操作数栈顶取出，并存储到到局部变量表的第1个Slot中
3. 将int类型变量从局部变量表的第1个Slot中取出，并放到操作数栈顶
4. 将局部变量表的第1个Slot中的int类型变量加1
5. 表示将int类型数值从操作数栈顶取出，并存储到到局部变量表的第1个Slot中，即i中

### JVM性能监控

1. JDK的命令行工具

    * jps(虚拟机进程状况工具)：jps可以列出正在运行的虚拟机进程，并显示虚拟机执行主类(Main Class,main()函数所在的类)名称 以及这些进程的本地虚拟机唯一ID(Local Virtual Machine Identifier,LVMID)。
    * jstat(虚拟机统计信息监视工具)：jstat是用于监视虚拟机各种运行状态信息的命令行工 具。它可以显示本地或者远程虚拟机进程中的类装载、内存、垃圾收集、JIT编译等运行数据。
    * jinfo(Java配置信息工具)：jinfo的作用是实时地查看和调整虚拟机各项参数。
    * jmap(Java内存映像工具)：命令用于生成堆转储快照(一般称为heapdump或dump文 件)。如果不使用jmap命令，要想获取Java堆转储快照，还有一些比较“暴力”的手段:譬如 在第2章中用过的-XX:+HeapDumpOnOutOfMemoryError参数，可以让虚拟机在OOM异常出 现之后自动生成dump文件。jmap的作用并不仅仅是为了获取dump文件，它还可以查询finalize执行队列、Java堆和永久代的详细信息，如空间使用率、当前用的是哪种收集器等。
    * jhat(虚拟机堆转储快照分析工具)：jhat命令与jmap搭配使用，来分析jmap生成的堆 转储快照。jhat内置了一个微型的HTTP/HTML服务器，生成dump文件的分析结果后，可以在 浏览器中查看。
    * jstack(Java堆栈跟踪工具)：jstack命令用于生成虚拟机当前时刻的线程快照。线程快照就是当前虚拟机内每一条线程正在执行的方法堆栈 的集合，生成线程快照的主要目的是定位线程出现长时间停顿的原因，如线程间死锁、死循环、请求外部资源导致的长时间等待等都是导致线程长时间停顿的常见原因。线程出现停顿的时候通过jstack来查看各个线程的调用堆栈，就可以知道没有响应的线程到底在后台做些什么事情，或者等待着什么资源。

2. JDK的可视化工具

    * JConsole
    * VisualVM
    
### JVM常见参数

1. -Xms20M：表示设置JVM启动内存的最小值为20M，必须以M为单位
2. -Xmx20M：表示设置JVM启动内存的最大值为20M，必须以M为单位。将-Xmx和-Xms设置为一样可以避免JVM内存自动扩展。大的项目-Xmx和-Xms一般都要设置到10G、20G甚至还要高
3. -verbose:gc：表示输出虚拟机中GC的详细情况
4. -Xss128k：表示可以设置虚拟机栈的大小为128k
5. -Xoss128k：表示设置本地方法栈的大小为128k。不过HotSpot并不区分虚拟机栈和本地方法栈，因此对于HotSpot来说这个参数是无效的
6. -XX:PermSize=10M：表示JVM初始分配的永久代（方法区）的容量，必须以M为单位
7. -XX:MaxPermSize=10M：表示JVM允许分配的永久代（方法区）的最大容量，必须以M为单位，大部分情况下这个参数默认为64M
8. -Xnoclassgc：表示关闭JVM对类的垃圾回收
9. -XX:+TraceClassLoading表示查看类的加载信息
10. -XX:+TraceClassUnLoading：表示查看类的卸载信息
11. -XX:NewRatio=4：表示设置年轻代（包括Eden和两个Survivor区）/老年代 的大小比值为1：4，这意味着年轻代占整个堆的1/5
12. -XX:SurvivorRatio=8：表示设置2个Survivor区：1个Eden区的大小比值为2:8，这意味着Survivor区占整个年轻代的1/5，这个参数默认为8
13. -Xmn20M：表示设置年轻代的大小为20M
14. -XX:+HeapDumpOnOutOfMemoryError：表示可以让虚拟机在出现内存溢出异常时Dump出当前的堆内存转储快照
15. -XX:+UseG1GC：表示让JVM使用G1垃圾收集器
16. -XX:+PrintGCDetails：表示在控制台上打印出GC具体细节
17. -XX:+PrintGC：表示在控制台上打印出GC信息
18. -XX:PretenureSizeThreshold=3145728：表示对象大于3145728（3M）时直接进入老年代分配，这里只能以字节作为单位
19. -XX:MaxTenuringThreshold=1：表示对象年龄大于1，自动进入老年代,如果设置为0的话，则年轻代对象不经过Survivor区，直接进入年老代。对于年老代比较多的应用，可以提高效率。如果将此值设置为一个较大值，则年轻代对象会在Survivor区进行多次复制，这样可以增加对象在年轻代的存活时间，增加在年轻代被回收的概率。
20. -XX:CompileThreshold=1000：表示一个方法被调用1000次之后，会被认为是热点代码，并触发即时编译
21. -XX:+PrintHeapAtGC：表示可以看到每次GC前后堆内存布局
22. -XX:+PrintTLAB：表示可以看到TLAB的使用情况
23. -XX:+UseSpining：开启自旋锁
24. -XX:PreBlockSpin：更改自旋锁的自旋次数，使用这个参数必须先开启自旋锁
25. -XX:+UseSerialGC：表示使用jvm的串行垃圾回收机制，该机制适用于单核cpu的环境下
26. -XX:+UseParallelGC：表示使用jvm的并行垃圾回收机制，该机制适合用于多cpu机制，同时对响应时间无强硬要求的环境下，使用-XX:ParallelGCThreads=<N>设置并行垃圾回收的线程数，此值可以设置与机器处理器数量相等。
27. -XX:+UseParallelOldGC：表示年老代使用并行的垃圾回收机制
28. -XX:+UseConcMarkSweepGC：表示使用并发模式的垃圾回收机制，该模式适用于对响应时间要求高，具有多cpu的环境下
29. -XX:MaxGCPauseMillis=100：设置每次年轻代垃圾回收的最长时间，如果无法满足此时间，JVM会自动调整年轻代大小，以满足此值。
30. -XX:+UseAdaptiveSizePolicy：设置此选项后，并行收集器会自动选择年轻代区大小和相应的Survivor区比例，以达到目标系统规定的最低响应时间或者收集频率等，此值建议使用并行收集器时，一直打开

### JVM调优目标-何时需要做jvm调优

1. heap 内存（老年代）持续上涨达到设置的最大内存值；
2. Full GC 次数频繁；
3. GC 停顿时间过长（超过1秒）；
4. 应用出现OutOfMemory 等内存异常；
5. 应用中有使用本地缓存且占用大量内存空间；
6. 系统吞吐量与响应性能不高或下降。

### JVM调优实战

一般的调优过程：如果生产上出现OOM异常，首先判断一下他是在堆里面发生的还是在元空间。还有一种是GC效率过低。这个意思是用了80%的时间，但是清除的垃圾不到2%，效率低下。

如果是堆空间不够，首先考虑一下是不是内存泄露，可以拿到当时的内存快照snapshot，用jmap？virtualVM什么之类的工具分析。如果对象应该是回收的但是还在，就看看代码该修改一下/。如果不是的话，就考虑增大堆内存。

如果遇到线上CPU 100%的情况，如何排查？

先登到机器上去，top查看哪个线程占用内存最高。print %x 把线程ID转换为16进制（或者jps -l来查看线程），jstack查看这个线程ID的内容。

1. Major GC和Minor GC频繁

    首先优化Minor GC频繁问题。通常情况下，由于新生代空间较小，Eden区很快被填满，就会导致频繁Minor GC，因此可以通过增大新生代空间来降低Minor GC的频率。例如在相同的内存分配率的前提下，新生代中的Eden区增加一倍，Minor GC的次数就会减少一半。
    
    扩容Eden区虽然可以减少Minor GC的次数，但会增加单次Minor GC时间么？扩容后，Minor GC时增加了T1（扫描时间），但省去T2（复制对象）的时间，更重要的是对于虚拟机来说，复制对象的成本要远高于扫描成本，所以，单次Minor GC时间更多取决于GC后存活对象的数量，而非Eden区的大小。因此如果堆中短期对象很多，那么扩容新生代，单次Minor GC时间不会显著增加。
    
2. 请求高峰期发生GC，导致服务可用性下降

    由于跨代引用的存在，CMS在Remark阶段必须扫描整个堆，同时为了避免扫描时新生代有很多对象，增加了可中断的预清理阶段用来等待Minor GC的发生。只是该阶段有时间限制，如果超时等不到Minor GC，Remark时新生代仍然有很多对象，我们的调优策略是，通过参数强制Remark前进行一次Minor GC，从而降低Remark阶段的时间。
    另外，类似的JVM是如何避免Minor GC时扫描全堆的？ 经过统计信息显示，老年代持有新生代对象引用的情况不足1%，根据这一特性JVM引入了卡表（card table）来实现这一目的。卡表的具体策略是将老年代的空间分成大小为512B的若干张卡（card）。卡表本身是单字节数组，数组中的每个元素对应着一张卡，当发生老年代引用新生代时，虚拟机将该卡对应的卡表元素设置为适当的值。如上图所示，卡表3被标记为脏（卡表还有另外的作用，标识并发标记阶段哪些块被修改过），之后Minor GC时通过扫描卡表就可以很快的识别哪些卡中存在老年代指向新生代的引用。这样虚拟机通过空间换时间的方式，避免了全堆扫描。

3. STW过长的GC

    对于性能要求很高的服务，建议将MaxPermSize和MinPermSize设置成一致（JDK8开始，Perm区完全消失，转而使用元空间。而元空间是直接存在内存中，不在JVM中），Xms和Xmx也设置为相同，这样可以减少内存自动扩容和收缩带来的性能损失。虚拟机启动的时候就会把参数中所设定的内存全部化为私有，即使扩容前有一部分内存不会被用户代码用到，这部分内存在虚拟机中被标识为虚拟内存，也不会交给其他进程使用。

4. 外部命令导致系统缓慢

    一个数字校园应用系统，发现请求响应时间比较慢，通过操作系统的mpstat工具发现CPU使用率很高，并且系统占用绝大多数的CPU资源的程序并不是应用系统本身。每个用户请求的处理都需要执行一个外部shell脚本来获得系统的一些信息，执行这个shell脚本是通过Java的 Runtime.getRuntime().exec()方法来调用的。这种调用方式可以达到目的，但是它在Java 虚拟机中是非常消耗资源的操作，即使外部命令本身能很快执行完毕，频繁调用时创建进程 的开销也非常可观。Java虚拟机执行这个命令的过程是:首先克隆一个和当前虚拟机拥有一样环境变量的进程，再用这个新的进程去执行外部命令，最后再退出这个进程。如果频繁执行这个操作，系统的消耗会很大，不仅是CPU，内存负担也很重。用户根据建议去掉这个Shell脚本执行的语句，改为使用Java的API去获取这些信息后，系统很快恢复了正常。
    
5. 由Windows虚拟内存导致的长时间停顿

    一个带心跳检测功能的GUI桌面程序，每15秒会发送一次心跳检测信号，如果对方30秒以内都没有信号返回，那就认为和对方程序的连接已经断开。程序上线后发现心跳 检测有误报的概率，查询日志发现误报的原因是程序会偶尔出现间隔约一分钟左右的时间完 全无日志输出，处于停顿状态。
    
    因为是桌面程序，所需的内存并不大(-Xmx256m)，所以开始并没有想到是GC导致的 程序停顿，但是加入参数-XX:+PrintGCApplicationStoppedTime-XX:+PrintGCDateStamps- Xloggc:gclog.log后，从GC日志文件中确认了停顿确实是由GC导致的，大部分GC时间都控 制在100毫秒以内，但偶尔就会出现一次接近1分钟的GC。

    从GC日志中找到长时间停顿的具体日志信息(添加了-XX:+PrintReferenceGC参数)， 找到的日志片段如下所示。从日志中可以看出，真正执行GC动作的时间不是很长，但从准 备开始GC，到真正开始GC之间所消耗的时间却占了绝大部分。
    
    除GC日志之外，还观察到这个GUI程序内存变化的一个特点，当它最小化的时候，资源 管理中显示的占用内存大幅度减小，但是虚拟内存则没有变化，因此怀疑程序在最小化时它的工作内存被自动交换到磁盘的页面文件之中了，这样发生GC时就有可能因为恢复页面文件的操作而导致不正常的GC停顿。在Java的GUI程序中要避免这种现象，可以 加入参数“-Dsun.awt.keepWorkingSetOnMinimize=true”来解决。

## Java基础

### string vs new string（）

string a = “hello”创建时首先会在字符串常量池string table中找，看是否有相等的对象，没有的话就在heap中创建一个对象，并把引用地址存放在string table中，然后将这个对象的引用赋给a这个变量

string a = new string("hello") 也是一样只是即使string table中有hello，还是会在heap中创建一个对象，把这个对象的引用赋给a

stringtable jdk1.6在堆上，jdk1.7之后放在方法区（1.7是永生代，1.8是元空间）

### 单例模式

饿汉模式：饿汉模式是最简单的一种实现方式，**饿汉模式在类加载的时候就对实例进行创建，实例在整个程序周期都存在**。

- 它的**好处**是只**在类加载的时候创建一次实例**，不会存在多个线程创建多个实例的情况，**避免了多线程同步的问题**。
- 它的**缺点**也很明显，即使这个单例没有用到也会被创建，而且在类加载之后就被创建，**内存就被浪费**了。

```java
public class Singleton {
    private static Singleton singleton = new Singleton();
    private Singleton() {}
    public static Singleton getInstance() {
        return singleton;
    }
}
```



懒汉模式：

```java
public class Singleton{
    private static Singleton instance = null;
    private Singleton(){}
    public static Singleton newInstance(){
        if (null == instance){
            instance = new Singleton();
        }
        return instance;
    }
}
```

改进版（加synchronized同步）：双检锁

```java
public class Singleton {
    private static Singleton instance = null;
    private Singleton(){}
    public static Singleton getInstance() {
        if (instance == null) {   // Single Checked
            synchronized (Singleton.class) {
                if (instance == null) { // Double checked
                    instance = new Singleton();
                }
            }
        }
        return instance;
    }
}
```

上面的依然会有问题，

- 这个问题的关键就在于**由于指令重排优化的存在，导致初始化Singleton和将对象地址赋给instance字段**的顺序是不确定的。

volatile禁止指令重排：

```java
public class Singleton {
    private static volatile Singleton instance = null;
    private Singleton(){}
    public static Singleton getInstance() {
        if (instance == null) { // Single Checked
            synchronized (Singleton.class) {
                if (instance == null) { // Double checked
                    instance = new Singleton();
                }
            }
        }
        return instance;
    }
}
```

枚举模式：

```java
public class SingletonExample {
    private SingletonExample() {}
    public static SingletonExample getInstance() {
        return Singleton.INSTANCE.getInstance();
    }
    private enum Singleton {
        INSTANCE;

        private SingletonExample singleton;

        //JVM保证这个方法绝对只调用一次
        Singleton() {
            singleton = new SingletonExample();
        }

        public SingletonExample getInstance() {
            return singleton;
        }
    }
    
}
```

用CAS来解决

```java
package com.example.demo.concurrency.singleton;

import java.util.concurrent.atomic.AtomicReference;

public class SingletonExample5 {
    // 用CAS方法来实现
    private static final AtomicReference<SingletonExample5> INSTANCE = new AtomicReference<>();
    private SingletonExample5() {}
    public static SingletonExample5 getInstance() {
        while (true) {
            SingletonExample5 singleton = INSTANCE.get();
            if (null != singleton) {
                return singleton;
            }
            singleton = new SingletonExample5();
            if (INSTANCE.compareAndSet(null, singleton)) {
                return singleton;
            }
        }
    }
}
```



### 线程的6种状态

- NEW    未启动的,不会出现在dump文件中(可以通过jstack命令查看线程堆栈)

- RUNNABLE    正在JVM中执行的

- BLOCKED    被阻塞,等待获取监视器锁进入synchronized代码块或者在调用Object.wait之后重新进入synchronized代码块

- WAITING    无限期等待另一个线程执行特定动作后唤醒它,也就是调用Object.wait后会等待拥有同一个监视器锁的线程调用notify/notifyAll来进行唤醒

- TIMED_WAITING    有时限的等待另一个线程执行特定动作

- TERMINATED    已经完成了执行


参考：https://juejin.cn/post/6844903961409880078

### Wait 和 Sleep 的区别

Wait：wait要释放对象锁，进入等待池，放弃CPU。

Sleep 它是一个静态方法，并不会让出监视器，不会放弃CPU

wait被唤醒之后线程是什么状态？--->>> 就绪状态 Ready

### Notify释放锁的时机

**notify()或者notifyAll()调用时并不会真正释放对象锁, 必须等到synchronized方法或者语法块执行完才真正释放锁.**

### 什么是反射

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


链接：https://www.jianshu.com/p/d6035d5d4d12

### IO流

|        | 输入流      | 输出流       |
| ------ | ----------- | ------------ |
| 字节流 | InputStream | OutputStream |
| 字符流 | Reader      | Writer       |

- 从流的传输单位划分： 分为 `字节流`（8位字节），`字符流`（16位的字符）

IO 流用了 装饰者模式和适配器模式

### Happens-Before

是判断是否存在竞争，线程是否安全的主要依据。

**1. 如果一个操作happens-before另一个操作，那么第一个操作的执行结果将对第二个操作可见，而且第一个操作的执行顺序排在第二个操作之前。**

**2. 两个操作之间存在happens-before关系，并不意味着一定要按照happens-before原则制定的顺序来执行。如果重排序之后的执行结果与按照happens-before关系来执行的结果一致，那么这种重排序并不非法。**

比如：

锁定规则：一个unlock操作一定先于同一个锁的lock操作

线程启动规则：Thread对象的start()方法先行发生于此线程的每个一个动作

### Java 的接口 Interface

为什么要接口呢？接口定义了一个规范，让我们可以知道接口里面有哪些方法。然后针对里面的方法，可以有不同的实现。

接口可以多继承，多实现。但所有的方法需要自己实现。

统一标准的目的，是大家都知道这个是***做什么***的，但是具体不用知道具体***怎么做***。
比如说：
我知道 Comparable 这个接口是用来比较两个对象的，那么如何去比较呢？
数字有数字的比较方法，字符串有字符串的比较方法，学生（自己定义的类）也有自己的比较方法。

### Java 抽象类

抽象类中除了抽象方法，还可能有许多一般方法，你可以继承后直接拿去用，提高效率。

java没有多继承的原因：因为父类可能会有方法名和参数的冲突。那我该实现哪个呢？对吧。这就是问题所在

### Java 8 的新特性

**lambda表达式**

什么时候用？怎么用？ Lambda 表达式可以简化代码，简化内部匿名类的写法。他只能用来取代**函数接口（Functional Interface）**的简写

#### 函数接口：

这类接口只定义了唯一的抽象方法的接口。

**Lambda表达式通过\*invokedynamic\*指令实现，书写Lambda表达式不会产生新的类**

### Collection中的新方法

#### **Collection接口**

**forEach()**

foreach有个新的签名，`void forEach(Consumer<? super E> action)` 那传入的是 Consumer。其中`Consumer`是个函数接口，里面只有一个待实现方法`void accept(T t)`

####**List接口**

**sort()**

该方法定义在`List`接口中，方法签名为`void sort(Comparator<? super E> c)`，该方法**根据`c`指定的比较规则对容器元素进行排序**。`Comparator`接口我们并不陌生，其中有一个方法`int compare(T o1, T o2)`需要实现，显然该接口是个函数接口。

#### Map接口

**forEach()**

该方法签名为`void forEach(BiConsumer<? super K,? super V> action)`，作用是**对`Map`中的每个映射执行`action`指定的操作**，其中`BiConsumer`是一个函数接口，里面有一个待实现方法`void accept(T t, U u)`。`BinConsumer`接口名字和`accept()`方法名字都不重要，请不要记忆他们



### Inegter， String 常量池

参考： https://www.cnblogs.com/qlqwjy/p/8759152.html

**总结:Integer i = value;如果i是在-128到127之间，不会去堆中创建对象，而是直接返回IntegerCache中的值;如果值不在上面范围内则会从堆中创建对象。= 走的是valueOf()方法,valueOf(int)会走缓存。**

　　**Integer i2 = new Integer(xxxx);不管参数的value是多少都会从堆中创建对象，与IntegerCache没关系。**



String s = new String("xxx")在检查常量池的时候会涉及到堆中创建对象；String s = "x"直接检查常量池，不会涉及堆。

![Integer:String常量池](/Users/zhangsheng/Desktop/testEquals/learning/面试/国内面试/jpg/Integer:String常量池.png)

**一道经典的面试题: new String("abc")创建几个对象?**

　　**简单的回答是一个或者两个，如果是常量区有值为"abc"的值，则只在堆中创建一个对象；如果常量区没有则会在常量区创建"abc"，此处的常量区是方法区的运行时常量池(也称为动态常量区)。**

### equals() 和 hashcode()

> 为什么重写 equals() 就要重写 hashCode()？

因为如果不这样做的话，就会违反 hashCode() 的通用约定，从而导致该类无法结合所有基于散列的集合一起正常工作，这类集合包括 HashMap 和 HashSet。如果用对象作为 Key 的话，可能会返回 null。

很多时候我们使用 equals() 需要比较的是**对象的值，而不是地址**，如果两个对象内存地址相同，那两个对象也一定相同。所以 equals() 重写的 equals() 方法中首先判断的还是**地址**(如 String 类)，如果地址不同才会去判断**值是否相等**。

### equals() 和 ==

**java当中的数据类型和“==”的含义：**

- 基本数据类型（也称原始数据类型） ：byte,short,char,int,long,float,double,boolean。他们之间的比较，应用双等号（==）,比较的是他们的值。
- 引用数据类型：当他们用（==）进行比较的时候，比较的是他们在内存中的存放地址（确切的说，是**堆内存**地址）。

### ArrayList 实现

首先 ArrayList 底层是数组，然后初始化的时候数据量是0，当你add的时候，它会默认变成10。扩容是每次变成原来的1.5倍。它的特性是查询比较快。删除效率比较低

### CopyOnWriteArrayList

线程安全的list

即复制再写入，就是在添加元素的时候，先把原 List 列表复制一份，再添加新的元素。

### LinkedList实现

LinkedList的底层是带有头节点和尾节点的双向链表，它提供了2种插入的方式，一种是头插和尾插。它的特性是适用于经常性的增加和删除。查询比较慢。因为是链表结构，就得拿值按顺序一个个的比较，最坏是O（n）

### HashMap和ConcurrentHashMap

HashMap的底层说起，那1.7 和1.8 的版本是有些不一样的地方。

1.7的底层是数组+单链表。1.8的时候是数组加上单链表或者红黑树。单链表到红黑树的转换，在链表长度大于8并且哈希桶的大小大于等于64的时候，会转换。如果红黑树节点的数量小于等于6的时候，会重新转换成单链表。

哈希桶的默认数量是16，负载因子是0.75

扩容：当哈希桶的数量大于：16 * 0.75=12 时候，触发扩容，首先会把哈希桶的数量变成原来的2倍。然后原来老的那些元素再rehash，填充到新的哈希桶里面。

1. 在jdk1.7中，在多线程环境下，扩容时会造成环形链或数据丢失。
2. 在jdk1.8中，在多线程环境下，会发生数据覆盖的情况。（因为在put的时候只要当前没有哈希碰撞，就直接赋值，多线程竞争的情况下会有数据覆盖）

线程不安全。在多线程的情况下会出现数据覆盖的情况。

死循环：Put的时候会有个resize的过程，在1.7版本的时候采用的是头插法，会有可能产生一个死循环。下一次get的时候可能会出现死循环。解决：1.8的时候改成尾插法。



由于HashMap是线程不同步的，虽然处理数据的效率高，但是在多线程的情况下存在着安全问题，因此设计了CurrentHashMap来解决多线程安全问题。

HashMap在put的时候，插入的元素超过了容量（由负载因子决定）的范围就会触发扩容操作，就是rehash，这个会重新将原数组的内容重新hash到新的扩容数组中，在多线程的环境下，存在同时其他的元素也在进行put操作，如果hash值相同，可能出现同时在同一数组下用链表表示，造成闭环，导致在get时会出现死循环，所以HashMap是线程不安全的。

### ConcurrentHashMap

ConcurrentHashmap在JDK1.7和1.8的版本改动比较大，1.7使用Segment+HashEntry分段锁的方式实现，1.8则抛弃了Segment，改为使用CAS+synchronized+Node实现，同样也加入了红黑树，避免链表过长导致性能的问题。

```
1.7版本的ConcurrentHashMap采用分段锁机制，里面包含一个Segment数组，Segment继承于ReentrantLock，Segment则包含HashEntry的数组，HashEntry本身就是一个链表的结构，具有保存key、value的能力能指向下一个节点的指针。

其实就是相当于每个Segment都是一个HashMap，默认的Segment长度是16，也就是支持16个线程的并发写，Segment之间相互不会受到影响。
```

1.7版本的ConcurrentHashMap取值的时候需要经过`2次hash`，第一次需要经过一次hash定位到Segment的位置，然后再hash定位到指定的HashEntry，遍历该HashEntry下的链表进行对比，成功就返回，不成功就返回null.。（高位哈希桶，低位哈希槽）



### CopyOnWriteArraySet

线程安全的set

CopyOnWriteArraySet逻辑就更简单了，就是使用 CopyOnWriteArrayList 的 addIfAbsent 方法来去重的，添加元素的时候判断对象是否已经存在，不存在才添加进集合。

这两种并发集合，虽然牛逼，但只适合于读多写少的情况，如果写多读少，使用这个就没意义了，因为每次写操作都要进行集合内存复制，性能开销很大，如果集合较大，很容易造成内存溢出。



### 为什么是红黑树而不是AVL树

因为红黑树的插入删除速度比AVL快。

参考：https://github.com/codeegginterviewgroup/CodeEggDailyInterview/issues/71

1. 为什么有了平衡树还需要红黑树？

    因为为了保证严格的平衡树的性质，需要频繁的左旋右旋来进行调整，所以在插入删除很频繁的场景中，平衡树性能会降低很多。

红黑树在插入、删除等操作，不会像平衡树那样，频繁着破坏红黑树的规则，所以不需要频繁着调整。红黑树是一种不大严格的平衡树。也可以说是一个折中方案。

### HashMap如果我想要让自己的Object作为Key应该怎么办

1. 重写hashCode()是因为在map这样的结构中，需要计算存储数据的存储位置，需要注意不要试图从散列码计算中排除掉一个对象的关键部分来提高性能，这样虽然能更快但可能会导致更多的Hash碰撞；
2. 重写equals()方法，需要遵守自反性、对称性、传递性、一致性以及对于任何非null的引用值x，x.equals(null)必须返回false的这几个特性，目的是为了保证key在哈希表中的唯一性（Java建议重写equal方法的时候需重写hashcode的方法）



### 原子性 && 可见性 && 有序性

- 原子性

一个操作或者多个操作，要么全部执行成功，要么全部执行失败。满足原子性的操作，中途不可被中断。

- 可见性

多个线程共同访问共享变量时，某个线程修改了此变量，其他线程能立即看到修改后的值。

- 有序性

程序执行的顺序按照代码的先后顺序执行。（由于JMM模型中允许编译器和处理器为了效率，进行指令重排序的优化。指令重排序在单线程内表现为串行语义，在多线程中会表现为无序。那么多线程并发编程中，就要考虑如何在多线程环境下可以允许部分指令重排，又要保证有序性）

### volatile

volatile在多处理器开发中保证了共享变量的“ 可见性”。可见性的意思是当一个线程修改一个共享变量时，另外一个线程能读到这个修改的值。

相比synchronized，volatile就是更轻量的选择，他没有上下文切换的额外开销。使用volatile声明的变量，可以确保值被更新的时候对其他线程立刻可见。

volatile使用内存屏障来保证不会发生指令重排，解决了内存可见性的问题。

字节码层面：volatile在字节码层面，就是使用访问标志：**ACC_VOLATILE**来表示，供后续操作此变量时判断访问标志是否为ACC_VOLATILE，来决定是否遵循volatile的语义处理。

**OrderAccess::storeload();** 即：只要volatile变量赋值完成后，都会走这段代码逻辑

注意一下和synchronized的一个区别：synchronized无法限制指令重排，仅是满足as-if-serial语义，保证单线程情况下程序的结果。（这是为什么单例模式中，要volatile+synchronized的原因）

### JMM

Java虚拟机规范中定义了一种Java内存 模型（Java Memory Model，即JMM）来屏蔽掉各种硬件和操作系统的内存访问差异，以实现让Java程序在各种平台下都能达到一致的并发效果。Java内存模型的主要目标就是**定义程序中各个变量的访问规则，即在虚拟机中将变量存储到内存和从内存中取出变量这样的细节**。

JMM中规定所有的变量都存储在主内存（Main Memory）中，每条线程都有自己的工作内存（Work Memory），线程的工作内存中保存了该线程所使用的变量的从主内存中拷贝的副本。线程对于变量的读、写都必须在工作内存中进行，而不能直接读、写主内存中的变量。同时，本线程的工作内存的变量也无法被其他线程直接访问，必须通过主内存完成。



### Atomic类的CAS操作

CAS是英文单词CompareAndSwap的缩写，CAS需要有3个操作数：内存地址V，旧的预期值A，即将要更新的目标值B。CAS指令执行时，当且仅当内存地址V的值与预期值A相等时，将内存地址V的值修改为B，否则就什么都不做。整个比较并替换的操作是一个原子操作。如 Intel 处理器，比较并交换通过指令的 cmpxchg 系列实现。

### AtomicReference

AtomicReference的作用则是对对象进行原子操作。

有了之前的AtomicLong和AtomicLongArray的基础，AtomicReference的源码比较简单。它是通过volatile和Unsafe提供的CAS函数实现原子操作。value 是volatile类型。这保证了当某线程修改value的值时，其他线程看到的value值都是最新的value值，即修改之后的volatile的值。通过CAS设置value，这保证了当某线程池通过CAS函数（如compareAndSet函数）设置value时，它的操作是原子的，即线程在操作value时不会被中断。

### LongAdder 对 CAS的优化

参考：http://www.mobabel.net/%E8%BD%ACjava-8%E5%A6%82%E4%BD%95%E4%BC%98%E5%8C%96cas%E6%80%A7%E8%83%BD/

尝试使用分段CAS以及自动分段迁移的方式来大幅度提升多线程高并发执行CAS操作的性能。

**分段CAS的机制**，也就是内部会搞一个Cell数组，每个数组是一个数值分段。如果某个Cell的value执行CAS失败了，那么就会自动去找另外一个Cell分段内的value值进行CAS操作。

### CAS操作ABA问题：

如果在这段期间它的值曾经被改成了B，后来又被改回为A，那CAS操作就会误认为它从来没有被改变过。Java并发包为了解决这个问题，提供了一个带有标记的原子引用类“AtomicStampedReference”，它可以通过控制变量值的版本来保证CAS的正确性。

### CAS 的缺点

ABA问题 👆

**循环时间长开销大**：自旋CAS的方式如果长时间不成功，会给CPU带来很大的开销。

**只能保证一个共享变量的原子操作**：只对一个共享变量操作可以保证原子性，但是多个则不行，多个可以通过AtomicReference来处理或者使用锁synchronized实现。

### Synchronized

- synchronized 用在方法上面的时候，底层是 ACC_SYNCHRONIZED
- 特性保证：有序性（as-if-serial），可见性（内存强制刷新），原子性（单一线程持有）， 可重入性（计数器）
- synchronized和lock的区别见👇，劣势是锁不可逆
- 对象：
    - 对象头（Header）包括：1. Mark Word（存储对象的Hashcode，分代年龄和锁的标志位信息）2. Klass Pointer（对象指向它的类元数据的指针，虚拟机通过这个指针确定这个对象是哪个类的实例）3. Monitor（EntryList， waitSet，owner：会指向持有monitor对象的线程）
    - 实例数据
    - 对齐填充
- 代码块：MonitorEnter，MonitorExit，多少次enter的计数器 加减
- 锁膨胀：无锁，偏向锁（mark word里面有线程信息，cas比较），轻量级锁（复制了一份mark word，叫做 Lock Record，也是CAS尝试修改对象头指针）
- 重量级锁：用户态内核态切换

### Synchronized 锁住了什么

synchronized修饰静态方法以及同步代码块的synchronized (类.class)用法锁的是类，线程想要执行对应同步代码，需要获得类锁。

synchronized修饰成员方法，线程获取的是当前调用该方法的对象实例的对象锁。

### Synchronized和Lock的区别

1. 首先synchronized是java内置关键字在jvm层面，Lock是个java类。
2. synchronized无法判断锁的状态，Lock可以判断是否获取到锁，并且可以主动尝试去获取锁。
3. synchronized会自动释放锁(a 线程执行完同步代码会释放锁 ；b 线程执行过程中发生异常会释放锁)，Lock需在finally中手工释放锁（unlock()方法释放锁），否则容易造成线程死锁。
4. 用synchronized关键字的两个线程1和线程2，如果当前线程1获得锁，线程2线程等待。如果线程1阻塞，线程2则会一直等待下去，而Lock锁就不一定会等待下去，如果尝试获取不到锁，线程可以不用一直等待就结束了。
5. synchronized的锁可重入、不可中断、非公平，而Lock锁可重入、可判断、可公平（两者皆可）
6. Lock锁适合大量同步的代码的同步问题，synchronized锁适合代码少量的同步问题。
7. Lock可以使用读线程提高多线程的读效率

### 锁升级过程

参考 深入理解java虚拟机

#### 轻量级锁的获取过程：

轻量级锁的获取过程：虚拟机首先会在当前线程的帧栈中创建一个lock record的空间，用来存当前对象的 mark word。（这个lock record的里面的内容取名字叫做 displaced mark word）然后虚拟机用 CAS 尝试将**对象**的 mark word 更新为指向 Lock Record的指针。

如果这个指针的更新动作成功，那么线程就拥有了这个对象的锁。并且 对象的 mark word的锁标志位（mark word最后2个bit）会变为‘00’ （表示此时对象处于轻量级锁定状态）

如果更新失败，虚拟机会先检查对象的Mark Word是否指向当前线程的栈帧，如果是，则当前线程已经拥有对象的锁，可以直接进入代码块执行。如果不是，那么这个锁对象已经被其他线程给抢占。

如果同时有 > 2 个线程竞争同一个锁，那么轻量级锁不再有效，要膨胀为重量级锁。锁标志位要变成 ‘10’。Mark Word 中存储的就是指向重量级锁（互斥量）的指针。后面等待的线程也要进入阻塞状态。

### 轻量级锁的同步性能

轻量级锁 能提升同步性能的依据 是：

> 对于绝大部分的锁，在整个同步周期内都是不存在竞争的。

但是这是个经验数据，

- 如果没有竞争，轻量级锁使用CAS操作避免了使用互斥量的开销。但是

- 但是如果存在锁竞争， 除了互斥量的开销外，还额外发生了CAS操作，**因此在有竞争的情况下，轻量级锁会比重量级锁更慢！！**

### 偏向锁

目的是消除数据在无竞争的情况下的同步原语，进一步提高性能。

如果说轻量级锁是在无竞争的情况下，使用CAS操作去消除同步使用的互斥量，那么偏向锁就是在无竞争的情况下把整个同步都消除掉，连CAS都不做了。
偏向锁会偏向于第一个获得它的线程。如果这个锁没有被其他线程获取，那么会一直持有这个偏向锁，永远不需要同步。

第一次偏向的时候，虚拟机会把对象头的mark word 标志位设为 01 偏向模式，同时CAS操作把获取到这个锁的线程ID记录到对象的mark word中。如果CAS成功，那以后这个线程进入这个同步块时，不再需要任何同步操作。

如果有另外一个线程去尝试获取这个锁时，偏向模式就宣告结束。虚拟机会根据目前是否处于锁定状态，撤销偏向后恢复到未锁定或轻量级锁定到状态。

偏向锁的Trade Off：

如果程序中大多数的锁总是被多个不同的线程访问，那么偏向模式就是多余的。 -XX:-UseBiasesLocking  -> true/false 来决定



### 读写锁

ReadWriteLock是一个接口，实现类是ReentrantReadWriteLock，看着名字的翻译就是可重入读写锁

读写锁就是分了两种情况，一种是读时的锁，一种是写时的锁，它允许多个线程同时读共享变量，但是只允许一个线程写共享变量，当写共享变量的时候也会阻塞读的操作。这样在读的时候就不会互斥，提高读的效率。

> **读写锁不允许锁的升级，不能直接从读锁升级到写锁**

> Downgrade by acquiring read lock before releasing write lock(通过在释放写锁之前获取读锁来降级)

### ReentrantLock

非公平锁：tryAcquire，acquiredQueue，CAS

公平锁：hasQueuedPredecessor：如果是当前持有锁的线程，可重入



### CLH 如何实现公平非公平





### AQS理论的数据结构

什么是AQS

```
A reentrant mutual exclusion with the same basic behavior and semantics as the implicit monitor lock accessed using methods and statements, but with extended capabilities.
可以做到 可重入互斥的隐式监视器（implicit monitor）。可以通过方法和语句访问，并且有扩展的功能。
```



AbstractQueuedSynchronizer

（知识点：入队，出队。头节点设计。共享和独享的实现。CAS）

AQS 是一个双向链表的一个结构。

AQS内部有3个对象，一个是state（用于计数器，类似gc的回收计数器），一个是线程标记（当前线程是谁加锁的），一个是阻塞队列。

AQS是自旋锁，在等待唤醒的时候，经常会使用自旋的方式，不停地尝试获取锁，直到被其他线程获取成功。

AQS有两个队列，同步队列和条件队列。同步队列依赖一个双向链表来完成同步状态的管理，当前线程获取同步状态失败后，同步器会将线程构建成一个节点，并将其加入同步队列中。通过signal或signalAll将条件队列中的节点转移到同步队列。



AQS 中的 公平锁和非公平锁的区别在于：

在 tryAcquire() 方法中，公平锁会有一个 hasQueuedPredecessors() 的判断，判断当前的线程是不是在queue的头部Node。如果不是的话直接false 返回。但是非公平锁没有这个判断。（意味着可以直接去抢锁，不用排队）

**非公平锁**和**公平锁**的区别：**非公平锁**性能高于**公平锁**性能。**非公平锁**可以减少`CPU`唤醒线程的开销，整体的吞吐效率会高点，`CPU`也不必取唤醒所有线程，会减少唤起线程的数量





### CountdownLatch

如何实现计数功能？

用一个volatile修饰的state标志位。



### Future

Callable can throw checked and unchecked exceptions,

Callable 可以抛出 checked 和 unchecked的异常，无论代码抛出何种异常，都会被封装到一个 ExecutionExecption, 并且在 Future.get 中重新抛出。





### 总线嗅探

CAS经常性的总线嗅探会导致CPU消耗高，总线风暴

什么是总线风暴：

如果在短时间内产生大量的cas操作在加上 volatile的嗅探机制则会不断地占用总线带宽，导致总线流量激增，就会产生总线风暴。 总之，就是因为volatile 和CAS 的操作导致BUS总线缓存一致性流量激增所造成的影响。

#### 总线锁

在早期处理器提供一个 LOCK# 信号，CPU1在操作共享变量的时候会预先对总线加锁，此时CPU2就不能通过总线来读取内存中的数据了，但这无疑会大大降低CPU的执行效率。

#### MESI

modified（修改）、exclusive（互斥）、share（共享）、invalid（无效）

CPU1使用共享数据时会先数据拷贝到CPU1缓存中,然后置为独占状态(E)，这时CPU2也使用了共享数据，也会拷贝也到CPU2缓存中。通过总线嗅探机制，当该CPU1监听总线中其他CPU对内存进行操作，此时共享变量在CPU1和CPU2两个缓存中的状态会被标记为共享状态(S)；

若CPU1将变量通过缓存回写到主存中，需要先锁住缓存行，此时状态切换为（M），向总线发消息告诉其他在嗅探的CPU该变量已经被CPU1改变并回写到主存中。接收到消息的其他CPU会将共享变量状态从（S）改成无效状态（I），缓存行失效。若其他CPU需要再次操作共享变量则需要重新从内存读取。

#### 嗅探机制

每个处理器会通过嗅探器来监控总线上的数据来检查自己缓存内的数据是否失效，如果发现自己缓存行对应的地址被修改了，就会将此缓存行置为无效。当处理器对此数据进行操作时，就会重新从主内存中读取数据到缓存行。

#### 缓存一致性流量

通过前面都知道了缓存一致性协议，比如MESI会触发嗅探器进行数据传播。当有大量的volatile 和cas 进行数据修改的时候就会产大量嗅探消息。



### 如何指定多个线程的执行顺序

1. 设定一个 orderNum，每个线程执行结束之后，更新 orderNum，指明下一个要执行的线程。并且唤醒所有的等待线程。
2. 在每一个线程的开始，要 while 判断 orderNum 是否等于自己的要求值，不是，则 wait，是则执行本线程。

### 为什么要使用线程池

1. 减少创建和销毁线程的次数，每个工作线程都可以被重复利用，可执行多个任务。
2. 可以根据系统的承受能力，调整线程池中工作线程的数目，防止因为消耗过多的内存，而把服务器累趴下。

### 核心线程池ThreadPoolExecutor内部参数

1. corePoolSize：指定了线程池中的线程数量
2. maximumPoolSize：指定了线程池中的最大线程数量
3. keepAliveTime：线程池维护线程所允许的空闲时间
4. unit: keepAliveTime 的单位。
5. workQueue：任务队列，被提交但尚未被执行的任务。
6. threadFactory：线程工厂，用于创建线程，一般用默认的即可。
7. handler：拒绝策略。当任务太多来不及处理，如何拒绝任务。

### 线程池的线程使用过程

工作提交到线程池里面，先进入核心池里面，如果线程数大于corePoolSize，就会进入到阻塞队列。阻塞队列满了之后就会新建一些新的线程。进入最大池中。然后当线程数超过最大线程池数目之后，就会执行一个拒绝策略。（saturation policy）包含 Abort policy, discard policy 等等

### 线程池的种类

newFixedThreadPool: 创建一个定长线程池，可控制线程最大并发数，超出的线程会在队列中等待。
FixedThreadPool: 适用于为了满足资源管理的需求，而需要限制当前线程数量的应用场景，它适用于负载比较重的服务器。

SingleThreadExecutor: 它只会用唯一的工作线程来执行任务，保证所有任务按照指定顺序(FIFO, LIFO, 优先级)执行。
SingleThreadExecutor: 适用于需要保证顺序地执行各个任务；并且在任意时间点，不会有多个线程是活动的应用场景。

CachedThreadPool: 创建一个可缓存线程池，如果线程池长度超过处理需要，可灵活回收空闲线程，若无可回收，则新建线程。
CachedThreadPool是大小无界的线程池，适用于执行很多的短期异步任务的小程序，或者是负载较轻的服务器。

### 线程池都有哪几种工作队列

1. ArrayBlockingQueue：底层是数组，有界队列，如果我们要使用生产者-消费者模式，这是非常好的选择。
2. LinkedBlockingQueue：底层是链表，可以当做无界和有界队列来使用，所以大家不要以为它就是无界队列。
3. SynchronousQueue：本身不带有空间来存储任何元素，使用上可以选择公平模式和非公平模式。
4. PriorityBlockingQueue：无界队列，基于数组，数据结构为二叉堆，数组第一个也是树的根节点总是最小值。

举例 ArrayBlockingQueue 实现并发同步的原理：原理就是读操作和写操作都需要获取到 AQS 独占锁才能进行操作。如果队列为空，这个时候读操作的线程进入到读线程队列排队，等待写线程写入新的元素，然后唤醒读线程队列的第一个等待线程。如果队列已满，这个时候写操作的线程进入到写线程队列排队，等待读线程将队列元素移除腾出空间，然后唤醒写线程队列的第一个等待线程。

### 线程池的拒绝策略

1. ThreadPoolExecutor.AbortPolicy:丢弃任务并抛出RejectedExecutionException异常。
2. ThreadPoolExecutor.DiscardPolicy：丢弃任务，但是不抛出异常。
3. ThreadPoolExecutor.DiscardOldestPolicy：丢弃队列最前面的任务，然后重新提交被拒绝的任务
4. ThreadPoolExecutor.CallerRunsPolicy：由提交任务的线程，处理该任务

### 线程池的线程数量怎么确定

1. 一般来说，如果是CPU密集型应用，则线程池大小设置为N+1。
2. 一般来说，如果是IO密集型应用，则线程池大小设置为2N+1。
3. 在IO优化中，线程等待时间所占比例越高，需要越多线程，线程CPU时间所占比例越高，需要越少线程。这样的估算公式可能更适合：最佳线程数目 = （（线程等待时间+线程CPU时间）/线程CPU时间 ）* CPU数目

### 如何实现一个带优先级的线程池

利用priority参数，继承 ThreadPoolExecutor 使用 PriorityBlockingQueue 优先级队列。

### ThreadLocal的原理和实现

ThreadLocal的作用主要是做数据隔离，填充的数据只属于当前线程，变量的数据对别的线程而言是相对隔离的。

线程进来之后初始化一个可以泛型的ThreadLocal对象，之后这个线程只要在remove之前去get，都能拿到之前set的值。ThreadLocalMap是自定义实现的Entry[]数组结构，没有实现map接口，而且他的Entry是继承一个WeakReference（弱引用）的。底层用的是一个数组。用数组是因为，一个线程可以有多个TreadLocal来存放不同类型的对象，但是他们都将放到当前线程的ThreadLocalMap里，所以肯定要数组来存。key：threadLocal， value：设置的值。

因此ThreadLocal其实只是个符号意义，本身不存储变量，仅仅是用来索引各个线程中的变量副本。

### ThreadLocal 父子之间不能继承

要继承的话有个 inheritableThreadLocal

### ThreadLocal为什么要使用弱引用和内存泄露问题

1.为什么ThreadLocalMap使用弱引用存储ThreadLocal？

假如使用强引用，当ThreadLocal不再使用需要回收时，发现某个线程中ThreadLocalMap存在该ThreadLocal的强引用，无法回收，造成内存泄漏。

因此，使用弱引用可以防止长期存在的线程（通常使用了线程池）导致ThreadLocal无法回收造成内存泄漏。

2.那通常说的ThreadLocal内存泄漏是如何引起的呢？

我们注意到Entry对象中，虽然Key(ThreadLocal)是通过弱引用引入的，但是value即变量值本身是通过强引用引入。

这就导致，假如不作任何处理，由于ThreadLocalMap和线程的生命周期是一致的，当线程资源长期不释放，即使ThreadLocal本身由于弱引用机制已经回收掉了，但value还是驻留在线程的ThreadLocalMap的Entry中。即存在key为null，但value却有值的无效Entry。导致内存泄漏。

所以最好在使用完了之后调用remove（）方法， expungeStaleEntry会帮助把key为 null 的value置为null。



参考：https://zhuanlan.zhihu.com/p/91579723

### 软引用和弱引用的区别

参考：https://juejin.cn/post/6844903665241686029

**弱引用**与**软引用**的区别在于：只具有**弱引用**的对象拥有**更短暂**的**生命周期**。垃圾回收器一旦发现了只具有**弱引用**的对象，不管当前**内存空间足够与否**，都会**回收**它的内存。不过，由于垃圾回收器是一个**优先级很低的线程**，因此**不一定**会**很快**发现那些只具有**弱引用**的对象。

软引用：如果一个对象只具有**软引用**，则**内存空间充足**时，**垃圾回收器**就**不会**回收它；如果**内存空间不足**了，就会**回收**这些对象的内存。只要垃圾回收器没有回收它，该对象就可以被程序使用。

> 软引用可用来实现内存敏感的高速缓存。

**软引用**可以和一个**引用队列**(`ReferenceQueue`)联合使用。如果**软引用**所引用对象被**垃圾回收**，JAVA虚拟机就会把这个**软引用**加入到与之关联的**引用队列**中。（应用：浏览器的后退按钮。按后退时，这个后退时显示的网页内容是重新进行请求还是从缓存中取出呢？这就要看具体的实现策略了。）

### HashSet和HashMap

HashSet的value存的是一个static finial PRESENT = newObject()。而HashSet的remove是使用HashMap实现,则是map.remove而map的移除会返回value,如果底层value都是存null,显然将无法分辨是否移除成功。

### Boolean占几个字节

未精确定义字节。Java语言表达式所操作的boolean值，在编译之后都使用Java虚拟机中的int数据类型来代替，而 boolean[] 将会被编码成Java虚拟机的byte数组，每个boolean元素占8位。

### 阻塞非阻塞与同步异步的区别

总结：在处理 IO 的时候，阻塞和非阻塞都是同步 IO。
			只有使用了特殊的 API 才是异步 IO。

下面的定义不是很准确：

1. 同步和异步关注的是消息通信机制，所谓同步，就是在发出一个调用时，在没有得到结果之前，该调用就不返回。但是一旦调用返回，就得到返回值了。而异步则是相反，调用在发出之后，这个调用就直接返回了，所以没有返回结果。换句话说，当一个异步过程调用发出后，调用者不会立刻得到结果。而是在调用发出后，被调用者通过状态、通知来通知调用者，或通过回调函数处理这个调用。
2. 阻塞和非阻塞关注的是程序在等待调用结果（消息，返回值）时的状态。阻塞调用是指调用结果返回之前，当前线程会被挂起。调用线程只有在得到结果之后才会返回。非阻塞调用指在不能立刻得到结果之前，该调用不会阻塞当前线程。

### Java 类加载

类加载是：负责动态的加载java类到虚拟机的内存中。

引导类加载器（bootstrap class loader）：它用来加载 Java 的核心库

扩展类加载器（extensions class loader）：它用来加载 Java 的扩展库。

应用程序类加载器（app class loader）：它根据 Java 应用的类路径（CLASSPATH）来加载 Java 类

保证安全：代理模式是为了保证 Java 核心库的类型安全。

双亲委派机制是代理模式的一种，并不是所有的类加载都采用这种机制。比如Tomcat的类加载器是用代理模式，但是是首先自己尝试加载某个类，找不到然后交给父类加载器。

### 线程上下文类加载器

这个类加载器是为了抛弃双亲委派模型的加载链。

Thread.currentThread().getContextClassLoader();

Thread.currentThread().setContextClassLoader();

可以通过这个setContextClassLoader 来改变类加载器。默认情况下，我们的应用程序是使用app class loader。但是因为比如sql.Driver 这些，JDK提供了规范接口，是在bootstrap classloader / extensions classloader 定义，但是实现会在 extension或者app classloader里面实现。（注意，一般情况下，同一个类中所关联的其他类都是由当前类加载器 加载的。不会是第一个等级的加载器。）

参考：https://www.bilibili.com/video/BV19W411R772?p=16

### Java SPI

由于双亲委派模型损失了一丢丢灵活性。就比如java.sql.Driver这个东西。JDK只能提供一个规范接口，而不能提供实现。提供实现的是实际的数据库提供商。提供商的库总不能放JDK目录里吧。Java从1.6搞出了SPI就是为了优雅的解决这类问题——JDK提供接口，供应商提供服务。编程人员编码时面向接口编程，然后JDK能够自动找到合适的实现。

### CSRF 

Cross Site Request Forgery. 跨站请求伪造。是一种挟制用户在当前已登录的Web应用程序上执行非本意的操作的攻击方法。

攻击者并不能通过CSRF攻击来直接获取用户的账户控制权，也不能直接窃取用户的任何信息。他们能做到的，是**欺骗用户的浏览器，让其以用户的名义运行操作**。

防御：令牌token同步模式：令牌同步模式（英语：Synchronizer token pattern，简称STP）。原理是：当用户发送请求时，服务器端应用将令牌（英语：token，一个保密且唯一的值）嵌入HTML表格，并发送给客户端。客户端提交HTML表格时候，会将令牌发送到服务端，令牌的验证是由服务端实行的。令牌可以通过任何方式生成，只要确保随机性和唯一性（如：使用随机种子【英语：random seed】的[哈希链](https://zh.wikipedia.org/wiki/哈希链) ）。这样确保攻击者发送请求时候，由于没有该令牌而无法通过验证。

### 动态代理

可以在运行期动态创建某个`interface`的实例。

参考：https://zhuanlan.zhihu.com/p/58092627

#### JDK动态代理实现的原理

首先Jdk的动态代理实现方法是依赖于**接口**的，首先使用接口来定义好操作的规范。然后通过`Proxy`类产生的代理对象调用被代理对象的操作，而这个操作又被分发给`InvocationHandler`接口的 `invoke`方法具体执行

#### cgLib的动态代理实现

由于JDK只能针对实现了接口的类做动态代理，而不能对没有实现接口的类做动态代理，所以[cgLib](https://link.zhihu.com/?target=https%3A//github.com/cglib/cglib)横空出世！CGLib（Code Generation Library）是一个强大、高性能的Code生成类库，它可以在程序运行期间动态扩展类或接口，它的底层是使用java字节码操作框架ASM实现。

CGLIB原理：动态生成一个要代理类的子类，子类重写要代理的类的所有不是final的方法。在子类中采用方法拦截的技术拦截所有父类方法的调用，顺势织入横切逻辑。它比使用java反射的JDK动态代理要快。

CGLIB底层：使用字节码处理框架ASM，来转换字节码并生成新的类。不鼓励直接使用ASM，因为它要求你必须对JVM内部结构包括class文件的格式和指令集都很熟悉。

CGLIB缺点：对于final方法，无法进行代理。

### 设计模式

Java里面用到了哪些设计模式？

参考：https://zhuanlan.zhihu.com/p/64062500

**适配器模式：（Adaptor）**

> 常用于将一个新接口适配旧接口。举例：一个假装是鸭子的火鸡。火鸡可以 implement Duck，传入一个火鸡实体，在Adaptor里override 方法，用火鸡的实例调用方法。看起来是调用鸭子的方法，实则call的是火鸡的方法

**代理模式**

> 代理模式用于向较简单的对象代替创建复杂或耗时的对象。

代理模式用得很广泛，基本所有大家知道的开源框架，都用到了动态代理。

**组合模式**

> 让客户端看起来在处理单个对象和对象的组合是平等的，换句话说，某个类型的方法同时也接受自身类型作为参数。（So in other words methods on a type accepting the same type）

从上面那句英文我们就可以得知，组合模式常用于递归操作的优化上，比如每个公司都有个boss系统，都会有什么菜单的功能。比如一级菜单下有二级菜单，二级菜单又有三级菜单。删除一级菜单的时候需要不断删除子菜单，那么这个设计模式你可以试试。总之，凡是有级联操作的，你都可以尝试这个设计模式。

**装饰者模式**

> 动态的给一个对象附加额外的功能，因此它也是子类化的一种替代方法。该设计模式在JDK中广泛运用，以下只是列举一小部分

这个模式使用就太广了，我们常用的AOP，既有动态代理，也有装饰者的味道。



## 分布式 Distributed System

本节参考：https://segmentfault.com/a/1190000022863259

分布式基本的概念：（我的个人理解）

对于服务service，存储store 等 来说，对于单一的机器节点，很可能出现一些单点故障，比如某一时刻存储系统就挂了，那么就导致了服务完全不可用。这样就很致命。那对于分布式的话，就是用多个节点或者机器共同对外形成某个服务。比如一个分布式存储的场景，我们可能需要用多个数据库，形成一个主从结构，把一些均匀的数据备份到不同的节点上，这样即使某个节点除了问题，也可以根据其他节点剩余的信息，恢复出丢失的数据，同时还能通过快速的奔溃恢复机制，顺利重新选出主服务器，来降低系统不可用的时间，降低对用户的影响。

上面说的是机器宕机的可能性，其实还有很多东西需要考虑，比如网络异常，那消息丢失了怎么办这样，消息乱序，即使使用TCP可以保证两个系统之间的通信顺序，但是多个系统之间的网络通信，那他们的顺序又需要怎么保证？

以一个分布式的存储系统为例，可以需要主节点和几个从节点（副本之间）来共同组成一个分布式存储系统的概念。那这中间要考虑的一些问题，比如主从的同步，选主（避免 split brain）的问题等等。这些可能需要引入一下 协议来做。比如zookeeper的一些选主协议或者说是奔溃恢复策略。



副本之间的一致性也是很重要的问题。比如一些定义的 最终一致性，强一致性，会话一致性（session consistency）

```
Session Consistency: 任何用户在某一次会话内一旦读到某个数据在某次更新后的值，这个用户在这次会话过程中不会再读到比这个值更旧的值。会话一致性通过引入会话的概念，在单调一致性的基础上进一步放松约束，会话一致性只保证单个用户单次会话内数据的单调修改，对于不同用户间的一致性和同一用户不同会话间的一致性没有保障。实践中有许多机制正好对应会话的概念，例如php 中的session 概念
```

衡量一个分布式系统的一些指标，

- 性能：系统的吞吐能力（比如每秒可以处理的总数据量，或者 可以同时完成某一功能的能力 QPS）
- 可用性：availability，面对各种异常情况下的正确提供服务的能力
- 可扩展性：scalability，
- 一致性：

### 副本与数据分布

更合适的做法不是以机器作为副本单位，而是将数据拆为较合理的数据段，以数据段为单位作为副本。数据段（chunk/segment/partition）称谓不同。

对于哈希分数据的方式，每个哈希分桶后的余数可以作为一个数据段，为了控制数据段的大小，常常使得分桶个数大于集群规模。一旦将数据分为数据段，则可以以数据段为单位管理副本，从而副本与机器不再硬相关，每台机器都可以负责一定数据段的副本

好处：恢复快，容错性好

坏处就是元数据的存储压力比较大

#### 计算本地化



#### 数据同步

Primary 与 Secondary 同步

- 由于网络原因导致的secondary落后于primary的数据。通常可以通过回放（redo）primary上的操作日志。
- 脏数据。某些primary上没有的数据，secondary上面却有。可以简单的直接丢弃有脏数据的副本，这样相当于副本没有数据。另外，也可以设计一些基于undo 日志的方式从而可以删除脏数据
- secondary 是一个新增加的副本，完全没有数据，需要从其他副本上拷贝数据。这就要求primary 副本支持快照(snapshot)功能。即对某一刻的副本数据形成快照，然后拷贝快照，拷贝完成后使用回放日志的方式追快照形成后的更新操作



## Raft 的原理和实现

一个可视化的理解raft的网站：http://thesecretlivesofdata.com/raft/

参考：https://www.freecodecamp.org/news/in-search-of-an-understandable-consensus-algorithm-a-summary-4bc294c97e0d/



简单的概括：每个server可以有3种状态， leader/follower/candidate

正常情况下，只有一个leader，其余的都是follower。follower只响应来自leader和candidate的request。所有的对外通信的都由leader来完成。（如果client把request发给了follower，follower会把这个消息redirect给leader）。 candidate 的状态只有在选举的时候才会出现。



Raft 把时间用不同长度的 terms 来区分。每个term都由election标志着开始。有的可能选不出leader，这个term就结束了。关于这个term，很重要，像是logical clock一样，如果有人发现自己的term 是stale的，那么自己会update成最新的，如果是leader发现自己的term不是最新的，leader会自动变成follower，开始新的一轮选举。如果server收到stale的term，那么这个server会拒绝这个request。



Raft有几个重要的RPC：

- RequestVotes RPC：是candidate用来选leader的
- AppendEntries RPC：用来replicate log entries的，也可用于心跳检查
- 还有一个是用来 transferring snapshots between servers.



### Leader Election

：Leader通过发送一个空的 AppendEntries RPC来保证自己的权威。什么时候会发生 leader election呢？一旦某个 follower 过了 *election timeout* 的时间还没有收到任何 communication的话，就会自动发起一个选举。自己变成candidate 状态，并且提高自己的term number，然后投自己一票，并且给所有的在同一个cluster的 server发送 RequestVote RPC。

这种状态要一致保持下去，除非：

1. 自己赢了，变成leader
2. 别人赢了，自己自动退回成follower
3. 没人赢，某一个candidate timeout。

并且为了减少出现split votes的可能性，Raft采取了 randomized election timeouts （一般在150ms - 300ms之间的随机值），并且在开始election的时候，重新开始倒计时。



### Log Replication

Log 的写入的过程是这样的，leader接受到来自client的request后，会把记录写到log里面，然后AppendEntries RPC 并行的发到所有的follower上面去，每个follower会先写log，然后返回给leader说自己可以了，超过半数同意，则leader commit这个change，并且告知client这个写入操作成功，并且会再发送一个AppendEntries的RPC到followers，（这个RPC包含了一个最大的需要被committed的index）



如何保持同步的呢？ Leader 里面维护了针对每个follower的 nextIndex，这个nextIndex就是leader要发给每个follower的下个log entry。 每个刚选出来的leader都会同步更新一下这个 nextIndex。目的是为了保持每个follower都有相同的log。如果follower返回failure，那 leader就会减少这个follower的 nextIndex，再次尝试，直到成功为止。



## 分布式 Lease 机制

### 活锁

基于lease 的 分布式 cache系统，中心节点会向各个服务器节点颁发一个lease。每个lease 具有一个有效期。中心服务器发出的lease 的含义为：在lease 的有效期内，中心服务器保证不会修改对应数据的值。因此，节点收到数据和lease 后，将数据加入本地Cache，一旦对应的lease 超时，节点将对应的本地cache 数据删除。

中心服务器在修改数据时，首先阻塞所有新的读请求，并等待之前为该数据发出的所有lease 超时过期，然后修改数据的值。

这样做法的原因是为了防止活锁。如果有读请求进来一直读，一直延续 lease的到期时间，那么写请求永远都不会执行。



### 阻塞读请求的性能问题

为了解决这个问题，可以有2个优化

- 一旦收到写请求，读请求不阻塞，但是为了防止活锁，可以不颁发lease。但是这样的问题在于，有写请求的时候，客户端可以读到数据，只是不能缓存元数据。
- 或者继续颁发lease，但是lease的有效期是已经发出的最大的截止日期。



### 时钟不同步

实践中的通常做法是将颁发者的有效期设置得比接收者的略大，只需大过时钟误差就可以避免对lease 的有效性的影响。



### 如何确定节点状态

中心节点会和其他节点发送lease 以及heartbeat交换信息

实际中可以把中心节点做成小的集群。具有高可用。对于防止split brain的问题，可以等到 lease 到期后，中心节点再选出primary的工作节点。lease 有效期一般是10秒



## Spring

### Spring全家桶

参考：https://blog.csdn.net/xlgen157387/article/details/77773908

**Spring Cloud Eureka**

服务的注册和发现，包括：服务注册中心、服务提供者、服务消费者。

服务注册原理：

1、两台Eureka服务注册中心构成的主从复制集群；
2、然后**服务提供者**向注册中心进行注册、续约、下线服务等；
3、**服务消费者**向**Eureka注册中心**拉取服务列表并维护在本地（这也是**客户端发现模式**的机制体现！）；
4、然后**消费者**根据从**Eureka注册中心**获取的服务列表选取一个服务提供者进行消费服务。

**Spring Cloud Ribbon**

负载均衡。

消费者是将服务从注册中心拉取服务生产者的服务列表并维护在本地，这种客户端发现模式是消费者选择合适的节点进行访问生产者提供的数据。Spring Cloud Ribbon客户端负载均衡器由此而来。

**Spring Cloud Feign** （注解）

Feign 创建一个接口并对它进行注解，它具有可插拔的注解支持包括Feign注解与JAX-RS注解，Feign还支持可插拔的编码器与解码器，Spring Cloud 增加了对 Spring MVC的注解

**Spring Cloud Hystrix**

服务的熔断降级

**Spring Cloud Zuul**

通过服务网关统一向外系统提供REST API的过程中，除了具备服务路由、均衡负载功能之外，它还具备了权限控制等功能

Zuul，为微服务架构提供了前门保护的作用，同时将权限控制这些较重的非业务逻辑内容迁移到服务路由层面，使得服务集群主体能够具备更高的可复用性和可测试性。

### Spring 的 IOC 是什么

Inverse of control: 是一种思想，意味着我们把设计好的对象交给容器控制，而不是在对象内部直接new 出来。

IOC：把对象的创建，初始化，销毁都交给Spring来管理，而不是由开发者控制。

传统的方式不好原因是 类之间的耦合太高。并且测试起来比较麻烦。



### Spring 的 Dependency Injection

说到了 IOC就会有DI，那么DI的话，就是说组件之间的依赖关系由容器在运行期间决定。



### 常用注解

@RestController 注解相当于@ResponseBody + @Controller 合在一起的作用

@Autowire 默认按照 ByType 注入

@Resource 默认按照 ByName 自动注入





### Spring 用到的设计模式

参考：https://zhuanlan.zhihu.com/p/114244039

- 1.简单工厂(非23种设计模式中的一种)
- 2.工厂方法
- 3.单例模式
- 4.适配器模式（一些HandlerAdapter）
- 5.装饰器模式 （一些wrapper，包裹了其他的功能， IO流）
- 6.代理模式
- 7.观察者模式
- 8.策略模式
- 9.模版方法模式

### Spring Bean的创建方式

1. 普通构造方法创建，直接配置bean节点即可
2. 静态工厂创建
3. 实例工厂创建

### Spring Bean 的初始化过程

Spring在创建Bean的过程中分为三步

- 实例化，对应方法：createBeanInstance
- 属性注入，：populateBean
- 初始化，：initializeBean

### Spring 如何管理 Bean

Spring容器做的事情：它在初始化的时候将配置文件中bean以及相对应关系的配置都加入到ApplicationContext,通过一系列的转换将这些bean实例化，bean被它进行了管理，所以ApplicationContext就扮演了一个容器的角色。

### spring 的beanDefinition

BeanDefinition是用来承载Bean的生命周期，销毁，初始化等操作的对象。

XML中的各种属性会先加载到BeanDefinition上，然后通过DeanDefinition来生成一个Bean。有点类和对象的感觉。

BeanDefinition 是一个接口，继承自 BeanMetadataElement 和AttributeAccessor 接口

BeanMetadataElement：该接口只有一个方法 getSource，该方法返回 Bean 的来源。

AttributeAccessor：该接口主要规范了问任意对象元数据的方法

### 什么是三级缓存

1. 第一级缓存：单例缓存池singletonObjects。
2. 第二级缓存：早期提前暴露的对象缓存earlySingletonObjects。（属性还没有值对象也没有被初始化）
3. 第三级缓存：singletonFactories单例对象工厂缓存。

三级缓存详解：[根据 Spring 源码写一个带有三级缓存的 IOC](https://zhuanlan.zhihu.com/p/144627581)

### 什么是循环依赖

循环依赖其实就是循环引用，也就是两个或则两个以上的bean互相持有对方，最终形成闭环。比如A依赖于B，B依赖于C，C又依赖于A。

注意，这里不是函数的循环调用，是对象的相互依赖关系。

Spring中循环依赖场景有：
（1）构造器的循环依赖 （应该是无法解决的）
（2）field属性的循环依赖。（三级缓存解决）

### Spring如何解决循环依赖问题

（原型(Prototype)的场景是不支持循环依赖的，通常会走到`AbstractBeanFactory`类中下面的判断，抛出异常。）

首先，Spring内部维护了三个Map，也就是我们通常说的三级缓存。

- *singletonObjects* 它是我们最熟悉的朋友，俗称“单例池”“容器”，缓存创建完成单例Bean的地方。
- *singletonFactories* 映射创建Bean的原始工厂
- *earlySingletonObjects* 映射Bean的早期引用，也就是说在这个Map里的Bean不是完整的，甚至还不能称之为“Bean”，只是一个Instance.

Spring使用了三级缓存解决了循环依赖的问题。在populateBean()给属性赋值阶段里面Spring会解析你的属性，并且赋值，当发现，A对象里面依赖了B，此时又会走getBean方法，但这个时候，你去缓存中是可以拿的到的。因为我们在对createBeanInstance对象创建完成以后已经放入了缓存当中，所以创建B的时候发现依赖A，直接就从缓存中去拿，此时B创建完，A也创建完，一共执行了4次。至此Bean的创建完成，最后将创建好的Bean放入单例缓存池（singletonObjects）中。

### BeanFactory和ApplicationContext的区别

1. BeanFactory是Spring里面最低层的接口，提供了最简单的容器的功能，只提供了实例化对象和拿对象的功能。
2. ApplicationContext应用上下文，继承BeanFactory接口，它是Spring的一个更高级的容器，提供了更多的有用的功能。如国际化，访问资源，载入多个（有继承关系）上下文 ，使得每一个上下文都专注于一个特定的层次，消息发送、响应机制，AOP等。
3. BeanFactory在启动的时候不会去实例化Bean，只有从容器中拿Bean的时候才会去实例化。ApplicationContext在启动的时候就把所有的Singleton 的 Bean 全部实例化了。它还可以为Bean配置lazy-init=true来让Bean延迟实例化

### 动态代理的实现方式，AOP的实现方式

1. JDK动态代理：利用反射机制生成一个实现代理接口的匿名类，在调用具体方法前调用InvokeHandler的invoke方法来处理。
2. CGlib动态代理：利用ASM（开源的Java字节码编辑库，操作字节码）开源包，将代理对象类的class文件加载进来，通过修改其字节码生成子类来处理。
3. 区别：JDK代理只能对实现接口的类生成代理；CGlib是针对类实现代理，对指定的类生成一个子类，并覆盖其中的方法，这种通过继承类的实现方式，不能代理final修饰的类。

### @Transactional错误使用失效场景

1. @Transactional 在private上：当标记在protected、private、package-visible方法上时，不会产生错误，但也不会表现出为它指定的事务配置。可以认为它作为一个普通的方法参与到一个public方法的事务中。
2. @Transactional 的事务传播方式配置错误。
3. @Transactional 注解属性 rollbackFor 设置错误：Spring默认抛出了未检查unchecked异常（继承自 RuntimeException 的异常）或者 Error才回滚事务；其他异常不会触发回滚事务。
4. 同一个类中方法调用，导致@Transactional失效：由于使用Spring AOP代理造成的，因为只有当事务方法被当前类以外的代码调用时，才会由Spring生成的代理对象来管理。
5. 异常被 catch 捕获导致@Transactional失效。
6. 数据库引擎不支持事务。

### Spring的隔离级别

五种，default，read_uncommitted, read_committed, repeatable_read, serializable 

- **TransactionDefinition.ISOLATION_DEFAULT:** 使用后端数据库默认的隔离级别，Mysql 默认采 用的 REPEATABLE_READ隔离级别 Oracle 默认采用的 READ_COMMITTED隔离级别.
- **TransactionDefinition.ISOLATION_READ_UNCOMMITTED:** 最低的隔离级别，允许读取尚未提交的 数据变更，可能会导致脏读、幻读或不可重复读
- **TransactionDefinition.ISOLATION_READ_COMMITTED:** 允许读取并发事务已经提交的数据，可以 阻止脏读，但是幻读或不可重复读仍有可能发生
- **TransactionDefinition.ISOLATION_REPEATABLE_READ:** 对同一字段的多次读取结果都是一致 的，除非数据是被本身事务自己所修改，可以阻止脏读和不可重复读，但幻读仍有可能发生。
- **TransactionDefinition.ISOLATION_SERIALIZABLE:** 最高的隔离级别，完全服从ACID的隔离级别。所有的事务依次逐个执行，这样事务之间就完全不可能产生干扰，也就是说，该级别可以防止脏读、不可重复读以及幻读。但是这将严重影响程序的性能。通常情况下也不会用到该级别。

### Spring的的事务传播机制

事务传播行为用来描述由某一个事务传播行为修饰的方法被嵌套进另一个方法的时事务如何传播。

1. REQUIRED（默认，常用）：支持使用当前事务，如果当前事务不存在，创建一个新事务。eg:方法B用REQUIRED修饰，方法A调用方法B，如果方法A当前没有事务，方法B就新建一个事务（若还有C则B和C在各自的事务中独立执行），如果方法A有事务，方法B就加入到这个事务中，当成一个事务。
2. SUPPORTS：支持使用当前事务，如果当前事务不存在，则不使用事务。
3. MANDATORY：强制，支持使用当前事务，如果当前事务不存在，则抛出Exception。
4. REQUIRES_NEW（常用）：创建一个新事务，如果当前事务存在，把当前事务挂起。eg:方法B用REQUIRES_NEW修饰，方法A调用方法B，不管方法A上有没有事务方法B都新建一个事务，在该事务执行。
5. NOT_SUPPORTED：无事务执行，如果当前事务存在，把当前事务挂起。
6. NEVER：无事务执行，如果当前有事务则抛出Exception。
7. NESTED：嵌套事务，如果当前事务存在，那么在嵌套的事务中执行。如果当前事务不存在，则表现跟REQUIRED一样。

### Spring中Bean的生命周期

1. 实例化 Instantiation
2. 属性赋值 Populate
3. 初始化 Initialization
4. 销毁 Destruction

参考：https://www.zhihu.com/question/38597960

简而言之：Spring 先对bean进行实例化，然后加入它的一些属性进行初始化，然后如果Bean实现一些Aware接口，就会调用 setBeanName（实现 BeanNameAware 接口），setBeanFactory（实现BeanFactoryAware接口），setApplicationContext（实现ApplicationContextAware接口），如果实现了BeanPostProcess接口，会用 postProcessBeforeInitialization 方法**（作用是在Bean实例创建成功后对进行增强处理，如对Bean进行修改，增加某个功能）** 经过以上的工作后，Bean将一直驻留在应用上下文中给应用使用，直到应用上下文被销毁。如果Bean实现了DisposableBean接口，Spring将调用它的destory方法，作用与在配置文件中对Bean使用destory-method属性的作用一样，都是在Bean实例销毁前执行的方法。

### Spring的后置处理器

1. BeanPostProcessor：Bean的后置处理器，主要在bean初始化前后工作。（before和after两个回调中间只处理了init-method）
2. InstantiationAwareBeanPostProcessor：继承于BeanPostProcessor，主要在实例化bean前后工作（TargetSource的AOP创建代理对象就是通过该接口实现）
3. BeanFactoryPostProcessor：Bean工厂的后置处理器，在bean定义(bean definitions)加载完成后，bean尚未初始化前执行。
4. BeanDefinitionRegistryPostProcessor：继承于BeanFactoryPostProcessor。其自定义的方法postProcessBeanDefinitionRegistry会在bean定义(bean definitions)将要加载，bean尚未初始化前真执行，即在BeanFactoryPostProcessor的postProcessBeanFactory方法前被调用。

### Bean 的 5种作用域

Bean 定义了 5 中作用域，分别为 singleton(单例)、prototype(原型)、

request、session 和 global session

- singleton:单例模式，Spring IoC 容器中只会存在一个共享的 Bean 实例，无论有多少个 Bean 引用它，始终指向同一对象。该模式在多线程下是不安全的 （为什么？**将有状态的bean配置成singleton会造成资源混乱问题（线程安全问题）**）
- prototype:原型模式，每次通过 Spring 容器获取 prototype 定义的 bean 时，容器都将创建 一个新的 Bean 实例，每个 Bean 实例都有自己的属性和状态，而 singleton 全局只有一个对 象。根据经验，对有状态的 bean 使用 prototype 作用域 （有状态是指 有实例化对象的bean，如每个user action），而对无状态的 bean 使用 singleton 作用域（比如 service对象）

- request: 在一次 Http 请求中，容器会返回该 Bean 的同一实例。而对不同的 Http 请求则会 产生新的 Bean，而且该 bean 仅在当前 Http Request 内有效,当前 Http 请求结束，该 bean 实例也将会被销毁。
- session:在一次 Http Session 中，容器会返回该 Bean 的同一实例。而对不同的 Session 请 求则会创建新的实例，该 bean 实例仅在当前 Session 内有效。同 Http 请求相同，每一次 session 请求创建新的实例，而不同的实例之间不共享属性，且实例仅在自己的 session 请求 内有效，请求结束，则实例将被销毁。
- global Session:在一个全局的 Http Session 中，容器会返回该 Bean 的同一个实例，仅在 使用 portlet context 时有效。

> 很多人可能对Spring中为什么DAO和Service对象采用单实例方式很迷惑
>
> 但是！因为Spring用 ThreadLocal这个类管理这些bean，所以每个线程用的bean可以是不一样的，保证了线程内部使用的 bean 是同一个，所以还是准确的！



### Spring MVC的工作流程（源码层面）

参考文章：[自己写个Spring MVC](https://zhuanlan.zhihu.com/p/139751932)

## 消息队列

### 为什么需要消息队列

解耦，异步处理，削峰/限流

### RocketMQ 如何保证高可用

开启 Confirm 机制，并且开启消息持久化。只有持久化了的消息才返回成功给 生产者

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

## RPC

### 什么是RPC

Remote Procedure Call：远程过程调用，简单的理解是一个节点请求另一个节点提供的服务

### RPC的步骤

简要回答！

1）服务消费方（client）用本地调用方式调用服务；

2）client stub接收到调用后负责将方法、参数等组装成能够进行网络传输的消息体；

3）client stub找到服务地址，并将消息发送到服务端；

4）server stub收到消息后进行解码；

5）server stub根据解码结果调用本地的服务；

6）本地服务执行并将结果返回给server stub；

7）server stub将返回结果打包成消息并发送至client方；

8）client stub接收到消息，并进行解码；

9）服务消费方得到最终结果。

　　RPC的目标就是要2~8这些步骤都封装起来，让用户对这些细节透明。

![RPC步骤](/Users/zhangsheng/Desktop/testEquals/learning/面试/国内面试/jpg/RPC步骤.png)

### RPC例子

参考：https://www.jianshu.com/p/7d6853140e13

```csharp
// Client端 
//    Student student = Call(ServerAddr, addAge, student)
1. 将这个调用映射为Call ID。
2. 将Call ID，student（params）序列化，以二进制形式打包
3. 把2中得到的数据包发送给ServerAddr，这需要使用网络传输层
4. 等待服务器返回结果
5. 如果服务器调用成功，那么就将结果反序列化，并赋给student，年龄更新

// Server端
1. 在本地维护一个Call ID到函数指针的映射call_id_map，可以用Map<String, Method> callIdMap
2. 等待服务端请求
3. 得到一个请求后，将其数据包反序列化，得到Call ID
4. 通过在callIdMap中查找，得到相应的函数指针
5. 将student（params）反序列化后，在本地调用addAge()函数，得到结果
6. 将student结果序列化后通过网络返回给Client
```

## Dubbo

### Dubbo的容错机制

1. 失败自动切换，当出现失败，重试其它服务器。通常用于读操作，但重试会带来更长延迟。可通过 retries="2" 来设置重试次数
2. 快速失败（fail - fast），只发起一次调用，失败立即报错。通常用于非幂等性的写操作，比如新增记录。
3. 失败安全 （fail - safe），出现异常时，直接忽略。通常用于写入审计日志等操作。
4. 失败自动恢复，后台记录失败请求，定时重发。通常用于消息通知操作。
5. 并行调用多个服务器，只要一个成功即返回。通常用于实时性要求较高的读操作，但需要浪费更多服务资源。可通过 forks="2" 来设置最大并行数。
6. 广播调用所有提供者，逐个调用，任意一台报错则报错。通常用于通知所有提供者更新缓存或日志等本地资源信息

### Dubbo注册中心挂了还可以继续通信么

可以，因为刚开始初始化的时候，消费者会将提供者的地址等信息拉取到本地缓存，所以注册中心挂了可以继续通信。

### Dubbo **monitor**  挂了还能通信吗

可以，因为监控中心主要是起到一个收集数据的作用，监控中心宕机，只会影响采集数据，不影响生产者和消费者之间的通信。

### Zookeeper 注册 producer/consumer

zookeeper采用树状结构来存储相关的信息，会创建相关的znode节点来存储信息

流程说明：

- 服务提供者启动时: 向 `/dubbo/com.foo.BarService/providers` 目录下写入自己的 URL 地址
- 服务消费者启动时: 订阅 `/dubbo/com.foo.BarService/providers` 目录下的提供者 URL 地址。并向 `/dubbo/com.foo.BarService/consumers` 目录下写入自己的 URL 地址
- 监控中心启动时: 订阅 `/dubbo/com.foo.BarService` 目录下的所有提供者和消费者 URL 地址。

### Dubbo提供的线程池

1. fixed：固定大小线程池，启动时建立线程，不关闭，一直持有。 
2. cached：缓存线程池，空闲一分钟自动删除，需要时重建。 
3. limited：可伸缩线程池，但池中的线程数只会增长不会收缩。(为避免收缩时突然来了大流量引起的性能问题)。

### Dubbo框架设计结构

1. 服务接口层：该层是与实际业务逻辑相关的，根据服务提供方和服务消费方的业务设计对应的接口和实现。
2. 配置层：对外配置接口，以ServiceConfig和ReferenceConfig为中心，可以直接new配置类，也可以通过spring解析配置生成配置类。
3. 服务代理层：服务接口透明代理，生成服务的客户端Stub和服务器端Skeleton，以ServiceProxy为中心，扩展接口为ProxyFactory。
4. 服务注册层：封装服务地址的注册与发现，以服务URL为中心，扩展接口为RegistryFactory、Registry和RegistryService。可能没有服务注册中心，此时服务提供方直接暴露服务。
5. 集群层：封装多个提供者的路由及负载均衡，并桥接注册中心，以Invoker为中心，扩展接口为Cluster、Directory、Router和LoadBalance。将多个服务提供方组合为一个服务提供方，实现对服务消费方来透明，只需要与一个服务提供方进行交互。
6. 监控层：RPC调用次数和调用时间监控，以Statistics为中心，扩展接口为MonitorFactory、Monitor和MonitorService。
7. 远程调用层：封将RPC调用，以Invocation和Result为中心，扩展接口为Protocol、Invoker和Exporter。Protocol是服务域，它是Invoker暴露和引用的主功能入口，它负责Invoker的生命周期管理。Invoker是实体域，它是Dubbo的核心模型，其它模型都向它靠扰，或转换成它，它代表一个可执行体，可向它发起invoke调用，它有可能是一个本地的实现，也可能是一个远程的实现，也可能一个集群实现。
8. 信息交换层：封装请求响应模式，同步转异步，以Request和Response为中心，扩展接口为Exchanger、ExchangeChannel、ExchangeClient和ExchangeServer。
9. 网络传输层：抽象mina和netty为统一接口，以Message为中心，扩展接口为Channel、Transporter、Client、Server和Codec。
10. 数据序列化层：可复用的一些工具，扩展接口为Serialization、 ObjectInput、ObjectOutput和ThreadPool。



### 设计一个dubbo？

- 上来你的服务就得去注册中心注册吧，你是不是得有个注册中心，保留各个服务的信心，可以用zookeeper来做，对吧
- 然后你的消费者需要去注册中心拿对应的服务信息吧，对吧，而且每个服务可能会存在于多台机器上
- 接着你就该发起一次请求了，咋发起？蒙圈了是吧。当然是基于动态代理了，你面向接口获取到一个动态代理，这个动态代理就是接口在本地的一个代理，然后这个代理会找到服务对应的机器地址
- 然后找哪个机器发送请求？那肯定得有个负载均衡算法了，比如最简单的可以随机轮询是不是
- 接着找到一台机器，就可以跟他发送请求了，第一个问题咋发送？你可以说用netty了，nio方式；第二个问题发送啥格式数据？你可以说用hessian序列化协议了，或者是别的，对吧。然后请求过去了。。
- 服务器那边一样的，需要针对你自己的服务生成一个动态代理，监听某个网络端口了，然后代理你本地的服务代码。接收到请求的时候，就调用对应的服务代码，对吧。



参考 https://blog.csdn.net/qq_22172133/article/details/104459452



## 操作系统

### 进程和线程

1. 进程是操作系统资源分配的最小单位，线程是CPU任务调度的最小单位。一个进程可以包含多个线程，所以进程和线程都是一个时间段的描述，是CPU工作时间段的描述，不过是颗粒大小不同。
2. 不同进程间数据很难共享，同一进程下不同线程间数据很易共享。
3. 每个进程都有独立的代码和数据空间，进程要比线程消耗更多的计算机资源。线程可以看做轻量级的进程，同一类线程共享代码和数据空间，每个线程都有自己独立的运行栈和程序计数器，线程之间切换的开销小。
4. 进程间不会相互影响，一个线程挂掉将导致整个进程挂掉。
5. 系统在运行的时候会为每个进程分配不同的内存空间；而对线程而言，除了CPU外，系统不会为线程分配内存（线程所使用的资源来自其所属进程的资源），线程组之间只能共享资源。

### 多线程和单线程

线程不是越多越好，假如你的业务逻辑全部是计算型的（CPU密集型）,不涉及到IO，并且只有一个核心。那肯定一个线程最好，多一个线程就多一点线程切换的计算，CPU不能完完全全的把计算能力放在业务计算上面，线程越多就会造成CPU利用率（用在业务计算的时间/总的时间）下降。但是在WEB场景下，业务并不是CPU密集型任务，而是IO密集型的任务，一个线程是不合适，如果一个线程在等待数据时，把CPU的计算能力交给其他线程，这样也能充分的利用CPU资源。但是线程数量也要有个限度，一般线程数有一个公式：最佳启动线程数=[任务执行时间/(任务执行时间-IO等待时间)]*CPU内核数超过这个数量，CPU要进行多余的线程切换从而浪费计算能力，低于这个数量，CPU要进行IO等待从而造成计算能力不饱和。总之就是要尽可能的榨取CPU的计算能力。如果你的CPU处于饱和状态，并且没有多余的线程切换浪费，那么此时就是你服务的完美状态，如果再加大并发量，势必会造成性能上的下降。

### 进程的组成部分

进程由进程控制块（PCB process control block）、程序段、数据段 三部分组成。

### 进程的通信方式

1. 无名管道 Pipes：半双工的，即数据只能在一个方向上流动，只能用于具有亲缘关系的进程之间的通信，可以看成是一种特殊的文件，对于它的读写也可以使用普通的read、write 等函数。但是它不是普通的文件，并不属于其他任何文件系统，并且**只存在于内存中**。｜grep 中的 ｜
2. FIFO命名管道：FIFO是一种文件类型，可以在无关的进程之间交换数据，与无名管道不同，FIFO有路径名与之相关联，**它以一种特殊设备文件形式存在于文件系统中**。
3. 消息队列：消息队列，是消息的链接表，存放在内核中。一个消息队列由一个标识符（即队列ID）来标识。
4. 信号量 Singal：信号量是一个计数器，信号量用于实现进程间的互斥与同步，而不是用于存储进程间通信数据。
5. 共享内存：共享内存指两个或多个进程共享一个给定的存储区，一般配合信号量使用。

### 进程间五种通信方式的比较

1. 管道：速度慢，容量有限，只有父子进程能通讯。
2. FIFO命名管道：任何进程间都能通讯，但速度慢。
3. 消息队列：容量受到系统限制，且要注意第一次读的时候，要考虑上一次没有读完数据的问题。
4. 信号量：不能传递复杂消息，只能用来同步。
5. 共享内存区：能够很容易控制容量，速度快，但要保持同步，比如一个进程在写的时候，另一个进程要注意读写的问题，相当于线程中的线程安全，当然，共享内存区同样可以用作线程间通讯，不过没这个必要，线程间本来就已经共享了同一进程内的一块内存。

### 内存管理有哪几种方式

1. 块式管理 Chunk：把主存分为一大块、一大块的，当所需的程序片断不在主存时就分配一块主存空间，把程序片断load入主存，就算所需的程序片度只有几个字节也只能把这一块分配给它。这样会造成很大的浪费，平均浪费了50％的内存空间，但是易于管理。
2. 页式管理 Page：把主存分为一页一页的，每一页的空间要比一块一块的空间小很多，显然这种方法的空间利用率要比块式管理高很多。
3. 段式管理 Segment：把主存分为一段一段的，每一段的空间又要比一页一页的空间小很多，这种方法在空间利用率上又比页式管理高很多，但是也有另外一个缺点。一个程序片断可能会被分为几十段，这样很多时间就会被浪费在计算每一段的物理地址上。Look aside buffer
4. 段页式管理：结合了段式管理和页式管理的优点。将程序分成若干段，每个段分成若干页。段页式管理每取一数据，要访问3次内存。

### 页面置换算法

1. 最佳置换算法OPT：只具有理论意义的算法，用来评价其他页面置换算法。置换策略是将当前页面中在未来最长时间内不会被访问的页置换出去。
2. 先进先出置换算法FIFO：简单粗暴的一种置换算法，没有考虑页面访问频率信息。每次淘汰最早调入的页面。
3. 最近最久未使用算法LRU：算法赋予每个页面一个访问字段，用来记录上次页面被访问到现在所经历的时间t，每次置换的时候把t值最大的页面置换出去(实现方面可以采用寄存器或者栈的方式实现)。
4. 时钟算法clock(也被称为是最近未使用算法NRU)：页面设置一个访问位，并将页面链接为一个环形队列，页面被访问的时候访问位设置为1。页面置换的时候，如果当前指针所指页面访问为为0，那么置换，否则将其置为0，循环直到遇到一个访问为位0的页面。
5. 改进型Clock算法：在Clock算法的基础上添加一个修改位，替换时根究访问位和修改位综合判断。优先替换访问位和修改位都是0的页面，其次是访问位为0修改位为1的页面。
6. LFU最少使用算法：设置寄存器记录页面被访问次数，每次置换的时候置换当前访问次数最少的。

### 操作系统中进程调度策略有哪几种

1. 先来先服务调度算法FCFS：队列实现，非抢占，先请求CPU的进程先分配到CPU，可以作为作业调度算法也可以作为进程调度算法；按作业或者进程到达的先后顺序依次调度，对于长作业比较有利.
2. 最短作业优先调度算法SJF：作业调度算法，算法从就绪队列中选择估计时间最短的作业进行处理，直到得出结果或者无法继续执行，平均等待时间最短，但难以知道下一个CPU区间长度；缺点：不利于长作业；未考虑作业的重要性；运行时间是预估的，并不靠谱.
3. 优先级调度算法(可以是抢占的，也可以是非抢占的)：优先级越高越先分配到CPU，相同优先级先到先服务，存在的主要问题是：低优先级进程无穷等待CPU，会导致无穷阻塞或饥饿.
4. 时间片轮转调度算法(可抢占的)：按到达的先后对进程放入队列中，然后给队首进程分配CPU时间片，时间片用完之后计时器发出中断，暂停当前进程并将其放到队列尾部，循环 ;队列中没有进程被分配超过一个时间片的CPU时间，除非它是唯一可运行的进程。如果进程的CPU区间超过了一个时间片，那么该进程就被抢占并放回就绪队列。

### 死锁的4个必要条件

1. 互斥条件：一个资源每次只能被一个线程使用；
2. 请求与保持条件：一个线程因请求资源而阻塞时，对已获得的资源保持不放；
3. 不剥夺条件：进程已经获得的资源，在未使用完之前，不能强行剥夺；
4. 循环等待条件：若干线程之间形成一种头尾相接的循环等待资源关系。   

### 如何避免（预防）死锁

1. 破坏“请求和保持”条件：让进程在申请资源时，一次性申请所有需要用到的资源，不要一次一次来申请，当申请的资源有一些没空，那就让线程等待。不过这个方法比较浪费资源，进程可能经常处于饥饿状态。还有一种方法是，要求进程在申请资源前，要释放自己拥有的资源。
2. 破坏“不可抢占”条件：允许进程进行抢占，方法一：如果去抢资源，被拒绝，就释放自己的资源。方法二：操作系统允许抢，只要你优先级大，可以抢到。
3. 破坏“循环等待”条件：将系统中的所有资源统一编号，进程可在任何时刻提出资源申请，但所有申请必须按照资源的编号顺序提出（指定获取锁的顺序，顺序加锁）。

## 计算机网路

### 加密解密证书

对称加密：加密解密用一个密钥，且加密解密方都知道密钥

非对称加密：加密用一个密钥，解密用另一个密钥且加密方一般有两个密钥，解密方只有一个解密密钥。rsa算法

摘要算法：将原文和摘要同时传输给接收方（保证数据不可篡改，公开，一致，难碰撞）md5，sha1

使用例子密码保存： 123456---md5（12345+aaaaa）= a1456gfsgkbckad----存这个在数据库

权威机构证书：alice和bob都去第三方机构注册账号，然后上传自己的公钥给第三方机构，第三方机构可以给alice和bob颁发一个证书，证书含有它们的公钥。

### https

https       应用层

stl/ssl      链路层

 tcp          链路层

1.tcp协议三次握手建立连接

2 .服务器利用tcp将证书发送给浏览器

3.浏览器通过本地的root ca验证网站证书

4.浏览器用证书的公钥加密：协商对称加密的算法和密码

5.服务器响应，确认对称加密的算法和密码

6.会话建立（来往数据使用对称加密）

https为了解决安全问题，https2.0解决性能问题

https1.1 keep  alive over tcp 其实还是一个串行的过程

Http2.0 1）使用了多路复用，一个请求阻塞了，其他的请求依旧可以响应。

2）头部压缩   http/1.1/get content-type：application/json --》23475239

### DDOS攻击

什么是DDOS， DOS是deney of service，第一个D是distributed的意思。DDOS一般是个总称。一般有CC攻击（Challenge Collapsar）挑战黑洞。黑洞是以前防御DDOS的安全设备。

如何解决：一个是备份网站，如果主网站下线，可以切换到备份。如果请求有特征，可以直接拦截。比如封掉IP，可以用IPtable来drop掉来自某个ip的请求。nginx也可以拦截，apache也可以。但是比较耗费性能。可以用CDN将网站静态内容放到多个服务器。但是如果源服务器的IP地址暴露，否则可以绕过CDN直接攻击源服务器。如果直接攻击源服务器，我买了弹性 IP ，可以动态挂载主机实例

### 跨域问题

跨域，指的是浏览器不能执行其他网站的脚本。它是由浏览器的同源策略造成的，是**浏览器施加的**安全限制。

1.预检请求（Preflight Request）

**OPTIONS请求**即预检**请求**，可用于检测服务器允许的http方法。 当发起跨域**请求**时，由于安全原因，触发一定条件时浏览器会在正式**请求**之前自动先发起**OPTIONS请求**，即CORS预检**请求**，服务器若接受该跨域**请求**，浏览器才继续发起正式**请求**

2.代理 proxy 优势：快一些，做缓存

### Get和Post区别

1. Get是不安全的，因为在传输过程，数据被放在请求的URL中；Post的所有操作对用户来说都是不可见的。
2. Get传送的数据量较小，这主要是因为受URL长度限制；Post传送的数据量较大，一般被默认为不受限制。
3. Get限制Form表单的数据集的值必须为ASCII字符；而Post支持整个ISO10646字符集。
4. Get执行效率却比Post方法好。Get是form提交的默认方法。
5. GET产生一个TCP数据包；POST产生两个TCP数据包。（非必然，客户端可灵活决定）有点争议，看这里https://blog.csdn.net/zerooffdate/article/details/78962818

### Head

HEAD方法和GET方法一致，除了服务器不能在响应里返回消息主体。HEAD请求响应里HTTP头域里的元信息应该和GET请求响应里的元信息一致。此方法被用来获取请求实体的元信息而不需要传输实体主体（entity-body）。此方法经常被用来测试超文本链接的有效性，可访问性，和最近的改变。.

### Options

OPTIONS方法允许客户端去判定请求资源的选项和/或需求，或者服务器的能力，而不需要利用一个资源动作（译注：使用POST，PUT，DELETE方法）或一个资源获取（译注：用GET方法）方法。OPTIONS的响应是不可以被缓存的。

### Cookie

Cookie是存放在 response header 中从服务器传回到客户端。发出的时候，放在request header里面传给服务器

### forward和redirect 的区别

forward 是容器中控制权的转向，是服务器请求资源，服务器直接访问目标地址的 URL，把那个 URL 的响应内容读取过来，然后把这些内容再发给浏览器，浏览器根本不知道服务器发送 的内容是从哪儿来的，所以它的地址栏中还是原来的地址。

redirect是服务器根据逻辑，发送一个状态码告诉浏览器，去重新请求资源。对于受保护的资源，redirect就无法访问了

forward更快

### Http和https的区别

- http是超文本传输协议，信息是明文传输，https则是具有安全性的ssl加密传输协议。
- http和https使用的是完全不同的连接方式，用的端口也不一样，http是80，https是443。
- https协议需要到ca申请证书

### Http请求的完全过程

（版本1）

链接：https://www.nowcoder.com/questionTerminal/f09d6db0077d4731ac5b34607d4431ee

**事件顺序**    

  (1) 浏览器获取输入的域名www.baidu.com 

（2.1）向本地的 etc/hosts 文件查看是否定义了域名对应的IP地址

  (2.2) 浏览器向DNS请求解析www.baidu.com的IP地址 

  (3) 域名系统DNS解析出百度服务器的IP地址 

  (4) 浏览器与该服务器建立TCP连接(默认端口号80) 

  (5) 浏览器发出HTTP请求，请求百度首页 

  (6) 服务器通过HTTP响应把首页文件发送给浏览器 

  (7) TCP连接释放 （http 1.1是长链接，不一定放开）

  (8) 浏览器将首页文件进行解析，并将Web页显示给用户。

========================================================

（版本2）

1. 浏览器根据域名解析IP地址（DNS）,并查DNS缓存
2. 浏览器与WEB服务器建立一个TCP连接
3. 浏览器给WEB服务器发送一个HTTP请求（GET/POST）：一个HTTP请求报文由请求行（request line）、请求头部（headers）、空行（blank line）和请求数据（request body）4个部分组成。
4. 服务端响应HTTP响应报文，报文由状态行（status line）、相应头部（headers）、空行（blank line）和响应数据（response body）4个部分组成。
5. 浏览器解析渲染

### Http请求的数据包在网络中的历程

参考：https://segmentfault.com/a/1190000022037918

1. 浏览器根据域名解析，生成HTTP请求。

2. 真实地址查询 DNS：通过浏览器生成http请求之后，需要委托操作系统将消息发送给web服务器。在发送之前，需要知道 域名对应的IP地址。需要用到DNS服务器。

    > 域名的层级关系：
    >
    > 在域名中，越靠右的层级越高。比如 www.server.com 根域名在顶层，下一层就是com顶级域，
    >
    > - 根DNS服务器
    > - 顶级域DNS服务器（com/cn）
    > - 权威DNS服务器（server.com）

3. 拿到IP之后，就可以把HTTP的传输工作交给操作系统的协议栈

4. 协议栈 内部分为几个部分。传输层的TCP/UDP，和网络层的IP。协议栈的上半部分有两块，分别是负责收发数据的 TCP 和 UDP 协议，它们两会接受应用层的委托执行收发数据的操作。协议栈的下面一半是用 IP 协议控制网络包收发操作，在互联网上传数据时，数据刽被切分成一块块的网络包，而将网络包发送给对方的操作就是由 IP 负责的

5. 其中，IP包含了 ICMP 和 ARP协议。

    - ICMP：用于告知网络包传送过程中产生的错误以及各种控制信息
    - ARP：用于根据 IP 地址查询相应的以太网 MAC 地址

6. TCP的3次握手建立连接。

7. IP 将数据封装成<strong>网络包</strong>发送给通信对象

    > 假设客户端有多个网卡，就会有多个 IP 地址，那 IP 头部的源地址应该选择哪个 IP 呢？

    > 当存在多个网卡时，在填写源地址 IP 时，就需要判断到底应该填写哪个地址。这个判断相当于在多块网卡中判断应该使用哪个一块网卡来发送包
    >
    > 根据  **路由表** 规则来判断哪一个网卡作为源IP地址。
    >
    > 在 Linux 操作系统，我们可以使用 <code>route -n</code> 命令查看当前系统的路由表
    >
    > 用 目标地址 和本地的 子网掩码（Genmask）来做 **与运算**，和路由表的 目的地址匹配。
    >
    > 第三条目比较特殊，它目标地址和子网掩码都是 <code>0.0.0.0</code>，这表示<strong>默认网关</strong>，如果其他所有条目都无法匹配，就会自动匹配这一行。并且后续就把包发给路由器，<code>Gateway</code> 即是路由器的 IP 地址

8. 两点传输MAC：生成了 IP 头部之后，接下来网络包还需要在 IP 头部的前面加上 <strong>MAC 头部</strong>

9. 一般在TCP/IP的通信协议里面，MAC包头部协议类型只有

    - 0800: IP协议
    - 0806: ARP 协议

10. 要得到接收方的 MAC 地址：现在**路由表**中找到 目标地址IP。但是怎么知道目的IP的MAC地址呢？ARP协议可以通过广播📢帮助找到路由器的MAC地址。（MAC地址会在ARP缓存中存在几分钟， 用`arp -a` 可以查看缓存内容）

11. 网卡：数字信号转成电信号（会检查MAC地址，如果不是发给自己的会丢弃）

12. 交换机：交换机的作用和网卡类似，但是交换机的端口没有MAC地址，直接接受所有的包，并检查FCS校验通过后存入缓存。

13. 路由器

### 计算机网络的五层模型

1. 应用层：为操作系统或网络应用程序提供访问网络服务的接口 ，通过应用进程间的交互完成特定网络应用。应用层定义的是应用进程间通信和交互的规则。（HTTP，FTP，SMTP，RPC）
2. 传输层：负责向两个主机中进程之间的通信提供通用数据服务。（TCP,UDP）
3. 网络层：负责对数据包进行路由选择和存储转发。（IP，ICMP(ping命令)）
4. 数据链路层：两个相邻节点之间传送数据时，数据链路层将网络层交下来的IP数据报组装成帧，在两个相邻的链路上传送帧（frame)。每一帧包括数据和必要的控制信息。
5. 物理层：物理层所传数据单位是比特（bit)。物理层要考虑用多大的电压代表1 或 0 ，以及接受方如何识别发送方所发送的比特。

### tcp和udp区别

1. TCP面向连接，UDP是无连接的，即发送数据之前不需要建立连接。
2. TCP提供可靠的服务。也就是说，通过TCP连接传送的数据，无差错，不丢失，不重复，且按序到达; UDP尽最大努力交付，即不保证可靠交付。
3. TCP面向字节流，实际上是TCP把数据看成一连串无结构的字节流，UDP是面向报文的，UDP没有拥塞控制，因此网络出现拥塞不会使源主机的发送速率降低（对实时应用很有用，如IP电话，实时视频会议等）
4. 每一条TCP连接只能是点到点的，UDP支持一对一，一对多，多对一和多对多的交互通信。
5. TCP首部开销20字节，UDP的首部开销小，只有8个字节。
6. TCP的逻辑通信信道是全双工的可靠信道，UDP则是不可靠信道。

### tcp和udp的优点

* TCP的优点： 可靠，稳定 TCP的可靠体现在TCP在传递数据之前，会有三次握手来建立连接，而且在数据传递时，有确认、窗口、重传、拥塞控制机制，在数据传完后，还会断开连接用来节约系统资源。 TCP的缺点： 慢，效率低，占用系统资源高，易被攻击 TCP在传递数据之前，要先建连接，这会消耗时间，而且在数据传递时，确认机制、重传机制、拥塞控制机制等都会消耗大量的时间，而且要在每台设备上维护所有的传输连接，事实上，每个连接都会占用系统的CPU、内存等硬件资源。 而且，因为TCP有确认机制、三次握手机制，这些也导致TCP容易被人利用，实现DOS、DDOS、CC等攻击。
* UDP的优点： 快，比TCP稍安全 UDP没有TCP的握手、确认、窗口、重传、拥塞控制等机制，UDP是一个无状态的传输协议，所以它在传递数据时非常快。没有TCP的这些机制，UDP较TCP被攻击者利用的漏洞就要少一些。但UDP也是无法避免攻击的，比如：UDP Flood攻击…… UDP的缺点： 不可靠，不稳定 因为UDP没有TCP那些可靠的机制，在数据传递时，如果网络质量不好，就会很容易丢包。 基于上面的优缺点，那么： 什么时候应该使用TCP： 当对网络通讯质量有要求的时候，比如：整个数据要准确无误的传递给对方，这往往用于一些要求可靠的应用，比如HTTP、HTTPS、FTP等传输文件的协议，POP、SMTP等邮件传输的协议。 在日常生活中，常见使用TCP协议的应用如下： 浏览器，用的HTTP FlashFXP，用的FTP Outlook，用的POP、SMTP Putty，用的Telnet、SSH QQ文件传输。什么时候应该使用UDP： 当对网络通讯质量要求不高的时候，要求网络通讯速度能尽量的快，这时就可以使用UDP。 比如，日常生活中，常见使用UDP协议的应用如下： QQ语音 QQ视频 TFTP。

### 三次握手

* 第一次握手：建立连接时，客户端发送syn包（syn=x）到服务器，并进入SYN_SENT状态，等待服务器确认；SYN：同步序列编号（Synchronize Sequence Numbers）。
* 第二次握手：服务器收到syn包，必须确认客户的SYN（ack=x+1），同时自己也发送一个SYN包（syn=y），即SYN+ACK包，此时服务器进入SYN_RECV状态；
* 第三次握手：客户端收到服务器的SYN+ACK包，向服务器发送确认包ACK(ack=y+1），此包发送完毕，客户端和服务器进入ESTABLISHED（TCP连接成功）状态，完成三次握手。

### 为什么不能两次握手

TCP是一个双向通信协议，通信双方都有能力发送信息，并接收响应。如果只是两次握手， 至多只有连接发起方的起始序列号能被确认， 另一方选择的序列号则得不到确认

### 四次挥手

1. 客户端进程发出连接释放报文，并且停止发送数据。释放数据报文首部，FIN=1，其序列号为seq=u（等于前面已经传送过来的数据的最后一个字节的序号加1），此时，客户端进入FIN-WAIT-1（终止等待1）状态。 TCP规定，FIN报文段即使不携带数据，也要消耗一个序号。
2. 服务器收到连接释放报文，发出确认报文，ACK=1，ack=u+1，并且带上自己的序列号seq=v，此时，服务端就进入了CLOSE-WAIT（关闭等待）状态。TCP服务器通知高层的应用进程，客户端向服务器的方向就释放了，这时候处于半关闭状态，即客户端已经没有数据要发送了，但是服务器若发送数据，客户端依然要接受。这个状态还要持续一段时间，也就是整个CLOSE-WAIT状态持续的时间。
3. 客户端收到服务器的确认请求后，此时，客户端就进入FIN-WAIT-2（终止等待2）状态，等待服务器发送连接释放报文（在这之前还需要接受服务器发送的最后的数据）。
4. 服务器将最后的数据发送完毕后，就向客户端发送连接释放报文，FIN=1，ack=u+1，由于在半关闭状态，服务器很可能又发送了一些数据，假定此时的序列号为seq=w，此时，服务器就进入了LAST-ACK（最后确认）状态，等待客户端的确认。
5. 客户端收到服务器的连接释放报文后，必须发出确认，ACK=1，ack=w+1，而自己的序列号是seq=u+1，此时，客户端就进入了TIME-WAIT（时间等待）状态。注意此时TCP连接还没有释放，必须经过2∗∗MSL（最长报文段寿命）的时间后，当客户端撤销相应的TCP后，才进入CLOSED状态。
6. 服务器只要收到了客户端发出的确认，立即进入CLOSED状态。同样，撤销TCP后，就结束了这次的TCP连接。可以看到，服务器结束TCP连接的时间要比客户端早一些

![TCP四次挥手](/Users/zhangsheng/Desktop/testEquals/learning/面试/国内面试/jpg/TCP四次挥手.png)

### 为什么连接的时候是三次握手，关闭的时候却是四次握手

因为当Server端收到Client端的SYN连接请求报文后，可以直接发送SYN+ACK报文。其中ACK报文是用来应答的，SYN报文是用来同步的。但是关闭连接时，**当Server端收到FIN报文时，很可能并不会立即关闭SOCKET，所以只能先回复一个ACK报文**，告诉Client端，"你发的FIN报文我收到了"。只有等到我Server端所有的报文都发送完了，我才能发送FIN报文，因此不能一起发送。故需要四步握手。

### 为什么要有TIME_WAIT?

1、 网络情况不好时，如果主动方无TIME_WAIT等待，关闭前一个连接后，主动方与被动方又建立起新的TCP连接，这时被动方重传或延时过来的FIN包过来后会直接影响新的TCP连接；（因为有可能最后一个ACK没收到，被动方重新发送了FIN）

2、 同样网络情况不好并且无TIME_WAIT等待，关闭连接后无新连接，当主动方接收到被动方重传或延迟的FIN包后，主动方会给被动方回一个RST包，可能会影响被动方其它的服务连接。

### TIME_WAIT为什么保留的时间是两个MSL

为了可靠安全的关闭TCP连接。比如网络拥塞，主动方最后一个ACK被动方没收到，这时被动方会对FIN开启TCP重传，发送多个FIN包，在这时，尚未关闭的TIME_WAIT就会把这些尾巴问题处理掉，不至于对新连接及其它服务产生影响。

### 怎么查有多少个TIME_WAIT？

参考：https://blog.csdn.net/fanren224/article/details/89849276

```bash
$ netstat -a |grep TIME_WAIT|wc -l
-a 是 -all 的意思

TIME_WAIT 多了对系统有很多影响，比如：
内存， 一般来说，内核里都需要有相关的数据结构来保存这个数据。 不过占用内存很少很少。 一个tcp socket占用不到4k。1万条TIME_WAIT的连接，也就多消耗1M左右的内存

CPU：每次找到一个随机端口，还是需要遍历一遍bound ports的吧，这必然需要一些CPU时间。

源端口数量：处于TIME_WAIT状态说明连接还未关闭，没关闭的连接自然会占用一个端口，一台机器的端口是有限的，最多只有65536个

文件描述符数量 (max open file)：一个socket占用一个文件描述符

TIME_WAIT bucket 数量 (net.ipv4.tcp_max_tw_buckets)：TCP: time wait bucket table overflow产生原因及影响：原因是超过了linux系统tw数量的阀值。危害是超过阀值后﹐系统会把多余的time-wait socket 删除掉，并且显示警告信息，如果是NAT网络环境又存在大量访问，会产生各种连接不稳定断开的情况。
```

### 四次挥手时会出现大量的**TIME_WAIT**是什么原因

我的理解是，首先出现 TIME_WAIT 肯定是主动断开链接方才会有的情况。那一般情况下，客户端主动断开的话，讲道理客户端不应该太繁忙。那我们就考虑是服务端主动断开链接。

（事实上也是可能的，对于一些 Mysql 的服务器，与许多客户端有短链接的时候，就会主动断开与客户端的链接，以确保自己有足够的端口可以用，减少资源浪费）

那我觉得如果服务端很繁忙的话，可能客户端与服务端的建立的短链接需要断开，结果服务器在TIME_WAIT  的情况下，假如客户端又在尝试和服务器链接，如果量比较大的话，肯定会出现端口重复使用的情况。那这个时候在端口还没完全CLOSED的情况下，服务器在收到新连接的SYN包后，并不认为这是一个新建连接请求的SYN包过来，而是把它当做一个普通数据包来处理，所以就出现了问题

> 首先，我们知道，linux下连接进入TIME_WAIT状态的时间是2个MSL，也就是120秒。在每秒3000个短连接的情况下，120秒内可以产生大约36万个进入TIME_WAIT状态的连接。而客户端可以使用的总端口数是65536，除去一些系统固定分配的，差不多也就60000个左右。假如这3000个每秒的短连接都是由一台客户端连接过来的，那20秒的时间就会复用到之前已经使用过的端口，这个时候该端口对应在服务器端的连接还在TIME_WAIT状态。所以服务器在收到新连接的SYN包后，并不认为这是一个新建连接请求的SYN包过来，而是把它当做一个普通数据包来处理，所以回复了一个普通的ACK和一个较大的seq。其实这个seq就是上一次连接的最后一个seq。

解决：

> 客户端改用长连接

需要客户端的改动比较大，但能彻底解决问题，高并发的场景下，长连接的性能也明显好于短连接。

> 增加客户端的个数，避免在2MSL时间内使用到重复的端口

能够降低出问题概率，但需要增加成本，性价比不高。

> 修改linux内核减小MSL时间

能够降低出问题的概率，需要修改linux内核，难度和风险都较大。

### TCP拥塞控制

一开始采用慢开始方法，只要发现出现网络拥塞，就采用拥塞控制方法；如果遇到网络拥塞，接收方就使用快重传方法，接收方连续发送3个重复确认，然后使用快恢复方法，利用拥塞避免算法增大拥塞窗口。

- 慢开始（slow start）：指数增长至ssthresh的大小，然后进入拥塞避免阶段
- 拥塞避免（congestion avoidance）：并非完全避免拥塞，而是指在拥塞避免阶段，将拥塞窗口控制为线性增长，使网络比较不容易出现拥塞。若出现报文段丢失，则： ssthresh的值会降为当前cwnd的一半，同时cwnd会重新从1开始。（tahoe是老的策略。新的Reno会降到CWND的一半，继续采用慢开始策略）
- 快重传 （fast retransmit）：所谓快重传就是，使发送方尽快进行重传，而不是等到超时重传计时器超时了才重新发送。如何判断需要快重传呢？---> 若发送方收到3个连续的重复确认，就将相应的报文段立即重传，而不是等到该报文段超时才重传。如图，M3丢失，接收方连续回复重复确认M2，发送方知道M3丢失立即重传。最后M3收到，接收方会回复当前最大的接收到的报文段M6的确认，节约了很多时间

![TCP快重传](/Users/zhangsheng/Desktop/testEquals/learning/面试/国内面试/jpg/TCP快重传.jpeg)

- 快恢复 （fast recovery）

![超时重传](/Users/zhangsheng/Desktop/testEquals/learning/面试/国内面试/jpg/超时重传.jpeg)

快恢复的做法是：将当前的cwnd， 和 ssthresh的大小调整为当前的窗口cwnd的一半，并且开始拥塞避免算法。

CWND: 拥塞窗口

ssthresh：slow start threshold



### TCP 的保活机制

定义一个时间段，在这个时间段内，如果没有任何连接相关的活动，TCP 保活机制会开始作用，每隔一个时间间隔，发送一个探测报文，该探测报文包含的数据非常少，如果连续几个探测报文都没有得到响应，则认为当前的 TCP 连接已经死亡，系统内核将错误信息通知给上层应用程序。

- tcp_keepalive_time=7200：表示保活时间是 7200 秒（2小时），也就 2 小时内如果没有任何连接相关的活动，则会启动保活机制
- tcp_keepalive_intvl=75：表示每次检测间隔 75 秒；
- tcp_keepalive_probes=9：表示检测 9 次无响应，认为对方是不可达的，从而中断本次的连接。



> 为什么 UDP 头部没有「首部长度」字段，而 TCP 头部有「首部长度」字段呢？

原因是 TCP 有**可变长**的「选项」字段，而 UDP 头部长度则是**不会变化**的，无需多一个字段去记录 UDP 的首部长度。（每个选项的开始是1字节的kind字段，说明选项的类型。一个TCP包可以包含多个可选项。比如kind=2时maximum segment size）

> 为什么 UDP 头部有「包长度」字段，而 TCP 头部则没有「包长度」字段呢？

**因为为了网络设备硬件设计和处理方便，首部长度需要是 `4`字节的整数倍。**

### UDP没有拥塞控制

udp没有流量控制和拥塞控制，也不需要确认。因为UDP没有确认机制，即使网络拥堵了或者对端机器吃不消了，发送端还是不停的发送，这样就会加重病态的恶化程度。

### **IP数据分片之MTU**

Maximum transmit unit. = 1500

MTU = MSS （1460）+ TCP header （20）+ IP header （20）

还有 TCP的 MSS maximum segment size = 1460



## ActiveMQ

消息中间件的话，我们用了ActiveMQ。这个比较老，但是因为支持的功能比较多，并且对于我们的技术栈（php + perl）比较友好，对于我们的应用场景 live score，吞吐量要求也不是特别巨大。（不是很需要Kafka这种10万级别的中间件做支持）

所以选择了ActiveMQ。

我们的应用场景比如NFL，是每周四晚上周天白天的时候，好几场比赛同时进行，我们需要 live stats update。这个时候我们的不同的 stats provider （realwire，stats.inc）就会进行实时的数据发送。这个时候我们需要把实时的数据消费到我们的sports site上面。

几个设置：

```
	<journal-type>NIO</journal-type>
	<paging-directory>data/paging</paging-directory>
    <bindings-directory>data/bindings</bindings-directory>
      <journal-directory>data/journal</journal-directory>
      <large-messages-directory>data/large-messages</large-messages-directory>
      <journal-datasync>true</journal-datasync>
      <journal-min-files>2</journal-min-files>
      <journal-pool-files>10</journal-pool-files>
      <journal-device-block-size>4096</journal-device-block-size>
      <journal-file-size>10M</journal-file-size>
      
      
acceptor
<acceptor name=“artemis”>tcp://0.0.0.0:61616?tcpSendBufferSize=1048576;tcpReceiveBufferSize=1048576;protocols=CORE,AMQP,STOMP,HORNETQ,MQTT,OPENWIRE;useEpoll=true;amqpCredits=1000;amqpLowCredits=300</acceptor>
```

协议用的是stomp，（Simple or streaming Text Orientated Messaging Protocol）

>  **auto ack**

stomp + NIO: For better scalability and performancethe Stomp protool can be configured to run over the NIO transport. NIO transport 用的线程成比TCP connector更少。这个可以支持更大数量的queue。





我们disable了 <persistence-enabled>, 因为需要增大吞吐量。而且实时数据其实我们并不担心丢了某个messge，系统不会因此出问题，所以就关掉了persistence。

数据从producer出来之后，会经过activemq，被分发到几个auditorium servers上，然后又通过这2个server，被其他的aud server 消费掉数据/message。上面跑了很多daemon scirpt，专门把这些数据写到一个叫做Boson 的内部工具 （apache storm实现），最后写到redis上



遇到的问题：

producer有几个消息同时发出，但是我们只处理了前面4个消息，第五个消息及后面的就不能正常的处理。

原因：要处理的文件大小超过100kb，而且官方文档有提到压缩的话，对于byte会 压缩 size 会 乘以 2

### ActiveMQ  VS Kafka







## 数据结构与算法

### 排序算法

1. 冒泡排序：俩俩相邻的比较并交换。O（n平方）
2. 选择排序：选择排序与冒泡排序有点像，只不过选择排序每次都是在确定了最小数的下标之后再进行交换，大大减少了交换的次数
3. 插入排序：将一个记录插入到已排序的有序表中，从而得到一个新的，记录数增1的有序表
4. 快速排序：通过一趟排序将序列分成左右两部分，其中左半部分的的值均比右半部分的值小，然后再分别对左右部分的记录进行排序，直到整个序列有序。
```java
int partition(int a[], int low, int high){
    int key = a[low];
    while( low < high ){
        while(low < high && a[high] >= key) high--;
        a[low] = a[high];
        while(low < high && a[low] <= key) low++;
        a[high] = a[low];
    }
    a[low] = key;
    return low;
}
void quick_sort(int a[], int low, int high){
    if(low >= high) return;
    int keypos = partition(a, low, high);
    quick_sort(a, low, keypos-1);
    quick_sort(a, keypos+1, high);
}
```

5. 堆排序：将待排序序列构造成一个大顶堆，此时，整个序列的最大值就是堆顶的根节点。将其与末尾元素进行交换，此时末尾就为最大值。然后将剩余n-1个元素重新构造成一个堆，这样会得到n个元素的次小值。如此反复执行，便能得到一个有序序列了。
```java
public class Test {

    public void sort(int[] arr) {
        for (int i = arr.length / 2 - 1; i >= 0; i--) {
            adjustHeap(arr, i, arr.length);
        }
        for (int j = arr.length - 1; j > 0; j--) {
            swap(arr, 0, j);
            adjustHeap(arr, 0, j);
        }

    }

    public void adjustHeap(int[] arr, int i, int length) {
        int temp = arr[i];
        for (int k = i * 2 + 1; k < length; k = k * 2 + 1) {
            if (k + 1 < length && arr[k] < arr[k + 1]) {
                k++;
            }
            if (arr[k] > temp) {
                arr[i] = arr[k];
                i = k;
            } else {
                break;
            }
        }
        arr[i] = temp;
    }

    public void swap(int[] arr, int a, int b) {
        int temp = arr[a];
        arr[a] = arr[b];
        arr[b] = temp;
    }

    public static void main(String[] args) {
        int[] arr = {9, 8, 7, 6, 5, 4, 3, 2, 1};
        new Test().sort(arr);
        System.out.println(Arrays.toString(arr));
    }
}
```
6. 希尔排序：先将整个待排记录序列分割成为若干子序列分别进行直接插入排序，待整个序列中的记录基本有序时再对全体记录进行一次直接插入排序。
7. 归并排序：把有序表划分成元素个数尽量相等的两半，把两半元素分别排序，两个有序表合并成一个

## 其他

### 高并发系统的设计与实现

在开发高并发系统时有三把利器用来保护系统：缓存、降级和限流。

* 缓存：缓存比较好理解，在大型高并发系统中，如果没有缓存数据库将分分钟被爆，系统也会瞬间瘫痪。使用缓存不单单能够提升系统访问速度、提高并发访问量，也是保护数据库、保护系统的有效方式。大型网站一般主要是“读”，缓存的使用很容易被想到。在大型“写”系统中，缓存也常常扮演者非常重要的角色。比如累积一些数据批量写入，内存里面的缓存队列（生产消费），以及HBase写数据的机制等等也都是通过缓存提升系统的吞吐量或者实现系统的保护措施。甚至消息中间件，你也可以认为是一种分布式的数据缓存。
* 降级：服务降级是当服务器压力剧增的情况下，根据当前业务情况及流量对一些服务和页面有策略的降级，以此释放服务器资源以保证核心任务的正常运行。降级往往会指定不同的级别，面临不同的异常等级执行不同的处理。根据服务方式：可以拒接服务，可以延迟服务，也有时候可以随机服务。根据服务范围：可以砍掉某个功能，也可以砍掉某些模块。总之服务降级需要根据不同的业务需求采用不同的降级策略。主要的目的就是服务虽然有损但是总比没有好。
* 限流：限流可以认为服务降级的一种，限流就是限制系统的输入和输出流量已达到保护系统的目的。一般来说系统的吞吐量是可以被测算的，为了保证系统的稳定运行，一旦达到的需要限制的阈值，就需要限制流量并采取一些措施以完成限制流量的目的。比如：延迟处理，拒绝处理，或者部分拒绝处理等等。

### 负载均衡算法：

1. 轮询
2. 加权轮询
3. 随机算法
4. 一致性Hash

### 常见的限流算法：

常见的限流算法有计数器、漏桶和令牌桶算法。漏桶算法在分布式环境中消息中间件或者Redis都是可选的方案。发放令牌的频率增加可以提升整体数据处理的速度，而通过每次获取令牌的个数增加或者放慢令牌的发放速度和降低整体数据处理速度。而漏桶不行，因为它的流出速率是固定的，程序处理速度也是固定的。

### 秒杀并发情况下库存为负数问题

1. for update显示加锁
2. 把update语句写在前边，先把数量-1，之后select出库存如果>-1就commit,否则rollback。
```
update products set quantity = quantity-1 WHERE id=3;
select quantity from products WHERE id=3 for update;
```
3. update语句在更新的同时加上一个条件
```
quantity = select quantity from products WHERE id=3;
update products set quantity = ($quantity-1) WHERE id=3 and queantity = $quantity;
```



## 综合素质

### 设计一个死锁

设计两个static final 的object。一个boolean，然后在if里面，先锁住o1，再锁住o2. 在else里面，先锁住o2，再锁住o1. 两个里面都加个sleep，假装在干事情。这样会发现，会有死锁。

### Java创建对象过程

A a =new A()的过程

假设是第一次使用这个类。那么会先有类加载的过程，并且初始化这个类，然后创建对象。类加载的过程需要多级classloader共同完成。因为java是子的类加载器会把加载任务委托给父类加载器完成。经过加载，验证，准备，解析（这3个步骤称为linking过程），然后再初始化。（先父类，再子类初始化，先静态变量，再静态代码块，注意：static代码块只有jvm能够调用）

然后再创建对象。在堆中分配需要的内存，静态变量在方法区分配。然后初始化（先执行实例代码块，再constructor）

在栈空间中定义A的类型引用指向堆中的地址。

### 双亲委派机制好处

使用双亲委托机制的好处是：能够有效确保 类的全局唯一性，当程序中出现多个限定名相同的类时，类加载器在执行加载时，始终只会加载其中的某一个类。

### 锁升级的过程

Hotspot 的研究人员发现，大部分情况下虽然加了锁，但是没有竞争情况，甚至是同一个线程反复获得这个锁。（偏向锁）这个时候会在对象头和栈帧的（Lock Record）里面记录获得偏向锁的线程ID。下一次有线程来的时候首先检查对象头的Mark Word是不是存的这个线程ID，如果是，直接进去。如果不是，分2种情况：1. 对象的偏向锁标志位为0（当前不是偏向锁），说明发生了竞争，已经膨胀为轻量级锁，使用CAS尝试获取锁。2. 对象的偏向锁标志位为1，说明还是偏向锁，只是不同的线程来竞争，也会使用CAS尝试把对象头的线程ID指向当前的请求线程ID。

如果CAS竞争失败，现在的线程会要求对象撤销偏向锁，首先暂停拥有偏向锁的线程，检查这个线程是否是个活动线程。如果不是，拿了锁没干事，直接把对象头设置为无锁状态，重新来过，如果还是活动线程，那么先遍历栈帧里面的Lock Record，让这个偏向锁变为无锁状态，然后恢复线程。

轻量级锁的加锁过程：

JVM在当前线程的栈帧中创建一个Lock Record，然后拷贝对象的MarkWord进去。同时生成一个Owner的指针指向那个加锁对象。同时用CAS尝试把对象头的MarkWord指向LockRecord的指针。成功就拿到了锁，不成功，有2种可能：1，对象的MarkWord值存的就是当前线程ID，那可以锁重入，直接得到锁。2. 其他的线程ID，膨胀成重量级锁（Mutex Lock）。

### Java join

等待这个线程结束。t1.join()就是等待t1这个线程结束，然后主线程继续下去。

```
public final void join()throws InterruptedException: Waits for this thread to die
```

### Java 如何使一个不安全的对象变成安全对象

除了Lock synchronized 外，可以用 CAS的方法来实现。atomic包里面有 AtomicReference 可以用，里面有compareAndSet方法。先比较然后再set。

用CAS的好处在于不需要使用传统的锁机制来保证线程安全,CAS是一种基于忙等待的算法,依赖底层硬件的实现,相对于锁它没有线程切换和阻塞的额外消耗,可以支持较大的并行度。

CAS的一个重要缺点在于如果忙等待一直执行不成功(一直在死循环中),会对CPU造成较大的执行开销。

另外，如果N个线程同时执行到singleton = new Singleton();的时候，会有大量对象创建，很可能导致内存溢出。（这个是说用CAS实现 singleton的时候，可能会发生的内存溢出）

参考：https://blog.csdn.net/u011277123/article/details/89916224

### 虚拟内存，内存分区

TODO：https://zhenbianshu.github.io/2018/11/understand_virtual_memory.html

算法：TODO：

一个数组 找出所有和为n的种类数目

给定两个稀疏矩阵 求乘法 要优化后的



## 阿里Java开发面试

第一轮**疯狂问Java基础知识**。讲讲Hash Collision，new String()和“string”的区别，Comparator vs Comparable，equals()，Generics，type erase，**线程安全的单例模式**会不会写，**类加载器**懂不懂。（后两个我不会，她说这个要会…）

问了reflection，git熟练度，vim熟练度。

1. Hash Collision：

比如在hashmap中，碰撞的意思是计算得到的Hash值相同，需要放到同一个bucket中

Hashmap里面的bucket出现了单链表的形式，散列表要解决的一个问题就是散列值的冲突问题，通常是两种方法：**链表法和开放地址法**。

> 链表法就是将相同hash值的对象组织成一个链表放在hash值对应的槽位；
> 开放地址法是通过一个探测算法，当某个槽位已经被占据的情况下继续查找下一个可以使用的槽位。

2. new String()和“string”的区别

String str = “Hello”；=> **字符串常量，它们在编译期就被确定了**

**用new String() 创建的字符串不是常量，不能在编译期就确定**，所以new String() 创建的字符串不放入常量池中，它们有自己的地址空间。

直接定义的String a =“a”是储存在常量存储区中的字符串**常量池**中；new String(“a”)是存储在**堆**中；

引入常量池的概念：**常量池(constant pool)指的是在编译期被确定，并被保存在已编译的.class文件中的一些数据**。它包括了关于类、方法、接口等中的常量，也包括字符串常量。

3. Comparator vs Comparable

Comparable 是一个 java.lang 下面的 interface，为了让自己新建的Object 可以Collections.sort()，可以implement Comparable<Laptop>, 里面可以Override 一个 

```java
@Override
public int compareTo(Laptop lap2) {
    if (this.getRam() > lap2.getRam()) return 1;
    else return -1;
} 
```

的方法。升序

Comparator： java.util 下面的 interface，functional interface。

实现 int compare(T o1, T o2);

什么时候用Comparator呢？一个是当你的class没有implements Comparable的时候，另一个是，你想用自己的方式实现sort。



4. equals()

Equals 比较的是值是否相等，== 判断的是地址是不是相等

5. Generics

参考：https://blog.csdn.net/justloveyou_/article/details/52420071

泛型：实现**类型参数化**的概念，使代码可以应用于多种类型。泛型是通过类型擦除来实现的

泛型的核心：告诉编译器想用什么类型（指定具体的类型参数或对其进行限制）

简单地说：**泛型 = 编译时的类型检查 + 编译时的类型擦除(编译器插入 checkcast 等) + 运行时的自动类型转换**。所以，我们在理解和应用泛型时，一定要从 编译期 和 运行时 两个视角去分析

**类型擦除：**

编译器在编译时擦除了所有类型相关的信息，所以在运行时不存在任何类型相关的信息。**桥方法(bridge method)** 用来真正覆写超类方法

限定通配符对类型进行了限制。

<?>表示了非限定通配符，因为<?>可以用任意类型来替代



List<? extends T>和List <? super T>之间有什么区别？

List<? extends T>可以接受任何继承自T的类型的List （类型上界），而List<? super T>可以接受任何T的父类构成的List （类型下界）。

6. 线程安全的单例模式

```java
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

7. 类加载器

负责动态的加载java类到虚拟机的内存中。

引导类加载器（bootstrap class loader）：它用来加载 Java 的核心库

扩展类加载器（extensions class loader）：它用来加载 Java 的扩展库。

系统类加载器（system class loader）：它根据 Java 应用的类路径（CLASSPATH）来加载 Java 类

保证安全：代理模式是为了保证 Java 核心库的类型安全。



========================================================



**数据库访问量很高怎么办**。我说了用hash分流就说不出别的了。又问一道**1亿integer，10M内存，找top 5k**的问题，我说了heap。又问了道国内培训班宣传最喜欢提的一道**多线程顺序打印ABC怎么实现**以后我就跪了。。感觉这次面得不好。面试官说要多去看看面经题（这么直白吗？……）说后面主管会问多线程高并发。问我“给你一周时间，你能自学这些吗？不能的话现在就可以结束了”。我：“……”

1. 数据库访问量很高怎么办

- 一个是sql语句必须得优化，不然会加重数据库服务器的负担
- 主从复制，读写分离，负载均衡。
- 数据库分表，分区，分库

垂直拆分

  在主键和一些列放在一个表中，然后把主键和另外的列放在另一个表中。如果一个表中某些列常用，而另外一些不常用，则可以采用垂直拆分。

水平拆分

  根据一列或者多列数据的值把数据行放到两个独立的表中。

分区就是把一张表的数据分成多个区块，这些区块可以在一个磁盘上，也可以在不同的磁盘上，分区后，表面上还是一张表，但是数据散列在多个位置，这样一来，多块硬盘同时处理不同的请求，从而提高磁盘**I/O读写性能。**实现比较简单，包括水平分区和垂直分区。

***\*注意：\****分库分表最难解决的问题是统计，还有跨表的连接（比如这个表的订单在另外一张表），解决这个的方法就是使用中间件，比如大名鼎鼎的***\*MyCat\****，用它来做路由，管理整个分库分表，乃至跨库跨表的连接

2. **1亿integer，10M内存，找top 5k**

TOP k 的问题：https://cloud.tencent.com/developer/article/1154735

针对top K类问题，通常比较好的方案是分治+Trie树/hash+最小堆，即先将数据集按照Hash方法分解成多个小数据集，然后使用Trie树或者Hash统计每个小数据集中的query词频，之后用小顶堆求出每个数据集中出现频率最高的前K个数，最后在所有top K中求出最终的top K。



========================================================



问了**"string".getBytes("UTF-8")和new String(byte[] byteArray, "UTF-8")的区别**；问了**抽象类和接口的异同**，interface的方法有哪些修饰词；问了**类加载**过程，类同名会发生什么，还有类加载器原理，线程上下文加载器的作用，双亲委派机制，以及ClassNotFoundException和NoClassDefFoundError的区别（感谢马士兵，答出来了一半）；**String和StringBuilder、StringBuffer的区别**；**不通过构造函数创建对象的方法**（4种）；**transient关键字**知不知道（不知道）；看到我写会Spring，他问**Interceptor**懂不懂（不懂）……



代码考了一道，100个人按3报数出列，求最后留下的是几号。我写了以后他问为什么不用链表，于是又写了一遍。

https://leetcode-cn.com/problems/yuan-quan-zhong-zui-hou-sheng-xia-de-shu-zi-lcof/comments/

```java
class Solution {
    // 模拟移除法
    public int lastRemaining(int n, int m) {
        List<Integer> list = new ArrayList<>();
        for (int i = 0; i < n; i++) {
            list.add(i);
        }
        int index = 0;
        while (n > 1) {
            index = (index + m - 1) % n;
            list.remove(index);
            n--;
        }
        return list.get(0);
    }
}
```



1. **getBytes()方法** 和 **new String(byte[],decode)**方法

在Java中,String的getBytes()方法是得到一个操作系统默认的编码格式的字节数组。这表示在不同的操作系统下, 返回的东西不一样!

而与getBytes相对的,可以通过new String(byte[], decode)的方式来还原这个"中"字,

2. **抽象类和接口的异同**

相同点：

1) 都是上层的抽象层。
2) 都不能被实例化
3) 都能包含抽象的方法，这些抽象的方法用于描述类具备的功能，但是不比提供具体的实现

不同点：

1) 在抽象类中可以写非抽象的方法，从而避免在子类中重复书写他们，这样可以提高代码的复用性，这是抽象类的优势；接口中只能有抽象的方法。

2) 一个类只能继承一个直接父类，这个父类可以是具体的类也可是抽象类；但是一个类可以实现多个接口。

3. interface的方法有哪些修饰词

public, 

private和protected是也是可以的 (内部接口是可以用public, private, protected修饰的。。。跟内部类一样，此时private和protect都有了意义)

就访问来说，可以用public,默认修饰符，而不能用private，因为接口本身就是为了让别的类或接口使用的，用private就没有了意义。

static

如果接口被定义为static类型，那它里面的方法势必也要被定义为静态类型。但是静态方法是不能被重写的，所以一个类如果继承了一个静态接口，但是却不能重写里面的静态方法，也就不能实现运行时多态，这样接口存在也就没有意义了。

4. 类加载中，类同名会发生什么

jvm 加载包名和类名相同的类时，先加载classpath中jar路径放在前面的，包名类名都相同，那jvm没法区分了，如果使用ide一般情况下是会提示发生冲突而报错，若不报错，只有第一个包被引入（在classpath路径下排在前面的包），第二个包会在classloader加载类时判断重复而忽略。

5. ClassNotFoundException和NoClassDefFoundError的区别

NoClassDefFoundError是**一个错误(Error)**，而 ClassNOtFoundException 是**一个异常**。



Java支持使用 Class.forName 方法来动态地加载类，任意一个类的类名如果被作为参数传，递给这个方法都将导致该类被加载到 JVM 中。如果这个类在类路径中没有被找到，那么此时就会在运行时抛出 ClassNotFoundException 异常。

另外还有一个导致 ClassNotFoundException 的原因就是：当一个类已经某个类加载器加载到内存中了，此时另一个类加载器又尝试着动态地从同一个包中加载这个类。

NoClassDefFoundError 产生的原因：

当 Java 虚拟机 或 ClassLoader 实例试图在类的定义中加载（作为通常方法调用的一部分，或者是使用 new 来创建新的对象）时，却**找不到类的定义（**要查找的类在编译的时候是存在的，运行的时候却找不到了），抛出此错误。

ClassNotFoundException 发生在装入阶段。 

NoClassDefFoundError 当目前执行的类已经编译，但是找不到它的定义时。也就是说你如果编译了一个类B，在类A中调用，编译完成以后，你又删除掉B，运行A的时候那么就会出现这个错误。



6. 类加载器原理，线程上下文加载器的作用



7. 不通过构造函数创建对象

(1) 用 new 语句创建对象，这是最常见的创建对象的方法。 (2) 运用反射手段,调用 java.lang.Class 或者 java.l ang.reflect.Constructor 类的 newInstance() 实例方法。 (3) 调用对象的 clone() 方法。 (4) 运用反序列化手 段，调用 java.io.ObjectInputStream 对象的

3，4 都不会调用构造函数。

8. **String和StringBuilder、StringBuffer的区别**

都是final类，都不允许被继承；

String类长度是不可变的，StringBuffer和StringBuilder类长度是可以改变的；

StringBuffer类是线程安全的，StringBuilder不是线程安全的；

StringBuilder 和 StringBuffer 底层是 char[] 数组，StringBuffer用synchronized的修饰。保证线程安全。



9. **transient关键字**

java 的transient关键字为我们提供了便利，你只需要实现Serilizable接口，将不需要序列化的属性前添加关键字transient，序列化对象的时候，这个属性就不会序列化到指定的目的地中。比如密码什么的，不想serialized出来

（1）一旦变量被transient修饰，变量将不再是对象持久化的一部分，该变量内容在序列化后无法获得访问。

（2）transient关键字只能修饰变量，而不能修饰方法和类。注意，本地变量是不能被transient关键字修饰的。变量如果是用户自定义类变量，则该类需要实现Serializable接口。

（3）被transient关键字修饰的变量不再能被序列化，一个静态变量不管是否被transient修饰，均不能被序列化。

10. spring 中的 Interceptor

- Interceptor是基于**Java的反射机制**（AOP思想）进行实现，不依赖Servlet容器。
- **拦截器可以在方法执行之前(preHandle)和方法执行之后(afterCompletion)进行操作，回调操作(postHandle)**，***\*可以获取执行的方法的名称\****，请求(HttpServletRequest)

========================================================



数据库的底层实现，Spring的底层实现，GC知不知道CMS和G1，这些基本上除了能说一句浅显的了解和应用，全都没有答出来；问了**Java内存结构**。算法简单问了一道判断长string是否是2个小string顺序交叉组成的，提示“知道DP吗”以后答出DP思路（这算答出吗），口述思路没有写代码……

https://blog.csdn.net/Hairy_Monsters/article/details/80492802

问了一道题：**两个有序数组，怎么用2个CPU优化merge过程？**事后回忆采分点：median+binary search （简单到凌乱）。可能是我描述得比较好，居然被夸思路不错。。

1. 数据库底层实现





##拼多多技术面

**二：技术面**



1 讲一下项目

2 做的主要是Java对吧，讲一下多线程把，用到哪些写一下 （线程池，ThreadLocal。）线程池包括了：线程池管理器，工作线程，任务接口，任务队列。参数包括：核心线程数，最大线程数，线程允许的空闲时间，空闲时间的单位，任务队列，线程工厂，拒绝策略。

3 写了thread和runnable，然后写了线程池，她问我线程池由哪些组件组成，有哪些线程池，分别怎么使用，以及拒绝策略有哪些。

答：线程池管理器（ThreadPoolManager）：用于创建和管理线程

工作线程（WorkThread）：线程池中的线程

任务接口（Task）：每个任务必须实现的接口，用来提供工作线程的调度任务的执行

任务队列：提供一种缓冲队列，存放还没有处理的任务。

工作提交到线程池里面，先进入核心池里面，如果线程数大于corePoolSize，就会进入到阻塞队列。阻塞队列满了之后就会新建一些新的线程。进入最大池中。然后当线程数超过最大线程池数目之后，就会执行一个拒绝策略。（saturation policy）包含 Abort policy, discard policy 等等

有哪些线程池：FixedThreadPool, CachedThreadPool, SingleThreadPool

上文有写： 线程池的拒绝策略

4 什么时候多线程会发生死锁，写一个例子吧，然后我写了一个两个线程，两个锁，分别持有一个，请求另一个的死锁实例。

写在了自己的intellji里面，查看，记得要有sleep，否则可能出现重排，解决了死锁。

5 集合类熟悉吧，写一个题目，一个字符串集合，找出pdd并且删除，我直接写了一个list然后for循环判断相等时删除，她说明显问题，我才发现list直接删位置会出错，于是我说改用数组，她说不太符合要求，所以应该使用iterator删除会好一点，修改会反映到集合类，并且不会出错。

用iterator 来remove。

```java
Iterator<Integer> it = al.iterator();
        while (it.hasNext()) {
            Integer i = it.next();
            if (i == 30) {
                it.remove();
            }
        }
```

或者用jdk 1.8 新方法：

```java
//Removes all of the elements of this collection that satisfy the given predicate.
list.removeIf(str -> str.equals("pdd"));
```



6 然后说一下Redis吧，是单线程还是多线程，Redis的分布式怎么做，说了集群。

Redis 确实是单线程模型，指的是执行 Redis 命令的核心模块是单线程的，而不是整个 Redis 实例就一个线程，Redis 其他模块还有各自模块的线程。

> 因为文件事件分派器队列的消费是单线程的，所以Redis才叫单线程模型。
>
> 参考：https://www.cnblogs.com/javastack/p/12848446.html

多线程的概念：比如 Redis 通过多线程方式在后台删除对象、以及通过 Redis 模块实现的阻塞命令等。

集群：

可以用redis cluster来做。相当于可以有多个redis master node，然后每个master node都可以挂载多个slave node。这样redis可以横向扩容。

redis cluster的话，自动将数据分片，每个master上放一部分数据，提供内置高可用。

哨兵模式，自动故障恢复， 引入zookeeper分布式协调组件。

分布式寻址算法：hash算法，一致性哈希（自动缓存迁移）+虚拟节点

7 RPC了解么，我说了主要是协议栈+数据格式+序列化方式，然后需要有服务注册中心管理生产者和消费者，他问我注册中心宕机怎么办，我说可以做高可用，他说要问的不是这个，是想问我注册中心宕机时消费者是否能访问生产者。

我说消费者本地有缓存，可以访问缓存中的生产者。但是不能保证缓存中的生产者都可用。（因为没有更新）

RPC：通过RPC框架，使得我们可以像调用本地方法一样地调用远程机器上的方法

1、本地调用某个函数方法

2、本地机器的RPC框架把这个调用信息封装起来（调用的函数、入参等），序列化(json、xml等)后，通过网络传输发送给远程服务器

3、远程服务器收到调用请求后，远程机器的RPC框架反序列化获得调用信息，并根据调用信息定位到实际要执行的方法，执行完这个方法后，序列化执行结果，通过网络传输把执行结果发送回本地机器

4、本地机器的RPC框架反序列化出执行结果，函数return这个结果



作者：EnjoyMoving
链接：https://www.zhihu.com/question/25536695/answer/285844835
来源：知乎
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。



9 TCP三次握手的过程，如果没有第三次握手有什么问题。



**三面：技术面**

1 自我介绍

2 讲一下项目的主要架构，你在里面做了什么

3 有什么比较复杂的业务逻辑讲一下。

4 最大的难点是什么，收获是什么。

5 MySQL的主从复制怎么做的，答日志，具体原理是什么，有什么优缺点。

主从复制

6 Redis了解哪些内容，是单线程么，为什么是单线程呢，数据一定是存在物理内存中么，我不懂这话啥意思，就问了一下是不是指可能也在虚拟内存中。他说那讲一下虚拟内存的机制把，我就讲了分页，页表，换页这些东西。

7 项目用到了多线程，如果线程数很多会怎么样，我说会占内存，还有就是切换线程比较频繁，他问切换线程会发生什么，应该就是CPU切换上下文，具体就是寄存器和内存地址的刷新。（发生任务切换时, 保存当前任务的寄存器到内存中, 将下一个即将要切换过来的任务的寄存器状态恢复到当前CPU寄存器中, 使其继续执行, 同一时刻只允许一个任务独享寄存器）

8 计算机如何访问一个文件的字节流呢，讲一下过程，说了Linux从inode节点找到磁盘地址，进行读取，他问我是直接读取么，我就说还会有读缓存，其实还应该说一下DMA的。

问了我知道swap分区么，我说不太清楚。

Linux 提出 SWAP 的概念，Linux 中可以使用 SWAP 分区，在分配物理内存，但可用内存不足时，将暂时不用的内存数据先放到磁盘上，让有需要的进程先使用，等进程再需要使用这些数据时，再将这些数据加载到内存中，通过这种”交换”技术，Linux 可以让进程使用更多的内存。缺点：虚拟内存的 SWAP 特性并不总是有益，放任进程不停地将数据在内存与磁盘之间大量交换会极大地占用 CPU，降低系统运行效率，所以有时候我们并不希望使用 swap。

9 分布式了解哪些东西，消息队列了解么，用在什么场景，说了削峰，限流和异步。说了kafka，问我怎么保证数据不丢失，以及确保消息不会被重复消费。还问了消息送达确认是怎么做的。

个人认为消息队列的主要特点是异步处理，主要目的是减少请求响应时间和解耦。所以主要的使用场景就是将比较耗时而且不需要即时（同步）返回结果的操作作为消息放入消息队列。同时由于使用了消息队列，只要保证消息格式不变，消息的发送方和接收方并不需要彼此联系，也不需要受对方的影响，即解耦和。



10 cap了解么，分别指什么，base呢，强一致性和弱一致性有什么方法来做，2pc了解么，说一下大概过程。

Consistency, Availability, Partition tolerance. 

BASE: Basica Available, Soft state, Eventual consistency. 

强一致性可以用关系型数据库。

弱一致性可以用Redis 的 RDB/AOF来存。因为可能以为主节点宕机，丢失部分数据。

对于关系型数据库，要求更新过的数据能被后续的访问都能看到，这是强一致性，如果能容忍后续的部分或者全部访问不到，则是弱一致性。如果经过一段时间后要求能访问到更新后的数据，则是最终一致性。

11 负载均衡怎么做的呢，为什么这么做，了解过集群雪崩么。

12 这样一个题目，一个节点要和客户连接建立心跳检测，大概有百万数量的连接，并且会定期发送心跳包，要写一个update方法和check方法，update方法更新心跳状态，check删除超时节点，怎么做，刚开始做了个hash发现check要轮询太慢了，然后用计时器和开线程检测也不行，最后说了个LRU，他说OK的。

13 写一道题，二叉树的后序遍历，非递归算法。

用一个栈可以实现，先压自己，再压右节点，再压左节点。不过我卡在一半没写完，面试官说有思路就行了，今天就面到这，然后就溜了，发现已经没人了。



TCP和UDP传输协议监听同一个端口后，接收数据互不影响，不冲突。因为数据接收时时根据五元组`{传输协议，源IP，目的IP，源端口，目的端口}`判断接受者的。



##快手面经



**一面：**

1 写一个选择排序或者插入排序

2 写一个生产者消费者

3 Java多线程了解么，什么时候一个int类型的操作是不安全的，自加呢，赋值呢。（什么是多线程：一个进程中可以并发**多**个**线程**，每条**线程**并行执行不同的任务。 **多线程是多**任务的一种特别的形式，但**多线程**使用了更小的资源开销。）

如果使用volatile修饰的话有什么作用。

（禁止指令重排，内存可见性，但不保证原子性。可见性的意思是当一个线程修改一个共享变量时，另外一个线程能读到这个修改的值）

4 MySQL和redis的区别是什么

5 为什么MySQL和Redis都要使用独立进程来部署，开放端口来提供服务，为什么不写在内核中。（大概就是回答了方便网络通信和搭建集群吧）

6 有一个场景，多线程并发，为每个线程安排一个随机的睡眠时间，设想一种数据结构去唤醒睡眠时间结束的线程，应该用哪种结构，答应该用优先级队列，也就是小顶堆，顶部是剩余睡眠时间最短的那个线程。

7 好像就是这些了。



**二面:**

1 项目

2 多线程

3 一道算法题，一个二维矩阵进行逆置操作，也就是行变列列变行。刚开始我理解错了，直接用一维数组转储再重新填入新数组。

面试官说可以不用一维数组么

然后解答的过程中才发现我理解错了。改了一会才搞定。

4 扩展一下，二维数组存在500g的文件中，怎么做才能完成上面算法的操作，我就说先按行拆分，最后再拼接。

5 扩展两下，一行数据就会超出内存，应该怎么做，那就按列拆分，最后合并。

6 知道服务的横向扩展和纵向扩展么，刚开始理解错了，后来就说是提高单机性能，以及扩展成集群。

7 cap介绍一下吧，为什么只能3选2

8 线程与进程

9 tcp和udp的区别

10 get和post的区别

11 并发量大概多少，做过优化吗

## 字节好的面经，一定要准备

https://www.cnblogs.com/itxu/p/12011509.html



https://www.nowcoder.com/discuss/336659?type=2&order=4&pos=19&page=2

- 任务系统怎么保证任务完成后发奖一定成功？

- zset 延时队列怎么实现的

- Redis 的 ZSET 怎么实现的？ 尽量介绍的全一点，跳跃表加哈希表以及压缩链表

- Redis 的 ZSET 做排行榜时，如果要实现分数相同时按时间顺序排序怎么实现？ 说了一个将 score 拆成高 32 位和低 32 位，高 32 位存分数，低 32 位存时间的方法。问还有没有其他方法，想不出了 （分数 = 等级 + 时间 （当前系统时间戳）  分数是 64位的长整型 double）

    ```
     2) 设计方式二    
    64位双精度浮点数只有52位有效数字，最高只能表示 16 位十进制整数。，如果前面时间戳占了 10 位的话，分数就只剩下 6 位了，这对于某些排行榜分数来说是不够用的。我们可以考虑缩减时间戳位数
    
             等级偏移： Math.power(10, 14) = 10000000000000000（14位）
    
             这里有一个最大时间 MAX_TIME = 9999999999999 （13位）
    
             A 玩家，（10 * 等级偏移） + MAX_TIME - 11111111111111（ 时间戳），最终分数 10888888888888888
             B 玩家，（10 * 等级偏移） + MAX_TIME - 22222222222222（ 时间戳），最终分数 10777777777777777
    
    
    ```

- linux 系统里，一个被打开的文件可以被另一个进程删除吗？（可以的，删除的只是减掉一个link, 退出之后才是删除）

- 一个完整的 HTTP 请求会涉及到哪些协议？（ 
  TCP/IP，-ICMP：用于告知网络包传送过程中产生的错误以及各种控制信息- ARP（链路层）：用于根据 IP 地址查询相应的以太网 MAC 地址）

- 设计一个限流的系统怎么做？令牌桶，

- 让你设计一个延时任务系统怎么做 说了两个方案，一个是使用 [redis] 的 ZSET 来实现，考虑分片来抗高并发，使用 [redis] 的持久化来实现落地，使用 [redis] 的哨兵实现故障转移。 一个是使用时间轮的方法。（时间轮就是将一个时间轮分成比如8份，0-7，新的定时任务可以用时间余上8，并且要存cycle，表示时间轮需要经过多少圈。不过如果时间轮的槽比较少，导致某一个槽上的任务非常多那效率也比较低，这就和 `HashMap` 的 `hash` 冲突是一样的）

- Redis 的 sorted set，底层实现是 ziplist 和 skiplist。

- Synchronized 修饰字符串会有什么问题：如果是new出来的字符串会在堆中新建一个对象，所以锁的时候可能会锁到不同的对象，导致没锁上，这个时候可以用String 提供的intern 方法。intern 方法会先查询字符串常量池中是否存在，如果不存在，就会将当前字符串放进去再返回对象地址。s=“mystring”字符串是会分配在常量池里面。注意⚠️：String#intern 方法调用时，如果存在堆中的对象，会直接保存对象的引用，而不会重新创建对象。https://tech.meituan.com/2014/03/06/in-depth-understanding-string-intern.html
- HTTP的属于应用层，用的TCP/IP协议。UDP常见的应用层有NFS。网关：因为协议转换是网关最重要的功能，所以答案是工作在传输层及以上层次。路由器：工作在网络层，在不同的网络间存储并转发分组。交换机：工作在数据链路层，原理等同于多端口网桥。网桥：工作在数据链路层，在不同或相同类型的LAN之间存储并转发数据帧，必要时进行链路层上的协议转换。**数据链路层**主要有两个功能：帧编码和误差纠正控制
- 

- 1、一个 TCP 连接可以对应几个 HTTP 请求？(提示，这在问你HTTP1.0和1.1的区别) --多个。
- 2、一个 TCP 连接中 HTTP 请求发送可以一起发送么（比如一起发三个请求，再三个响应一起接收）？(提示，这就是在问你HTTP2.0和HTTP1.1协议的区别) http1.1 中是不可以的，因为单个 TCP 连接在同一时刻只能处理一个请求，意思是说：两个请求的生命周期不能重叠，任意两个 HTTP 请求从开始到结束的时间在同一个 TCP 连接里不能重叠。HTTP2 提供了 Multiplexing 多路传输特性，可以在一个 TCP 连接中同时完成多个 HTTP 请求
- 3、浏览器对同一Host建立TCP连接到数量有没有限制？(拜托，一个网站那么多图片，开一个TCP连接，按顺序下载？那不是等到死？) --- 有限制的，Chrome是最多6个.




## 字节面经

https://studygolang.com/articles/24768

某一个业务中现在需要生成全局唯一的递增 ID, 并发量非常大, 怎么做？

 一般的话，数据库自增ID在并发量大的情况下就不是很理想。UUID也不是很理想，因为生成的主键无法保证自增。我会想到用雪花算法。但是雪花算法有点依赖于本地机器的时钟，不能保证全局唯一递增。所以可能会考虑用redis 的auto increment。但是需要编码配置的工作比较多。

自己想法：时间戳+机器ID+自增ID

自增ID用Mysql，每个应用每次取100个ID缓存在内存。Mysql对应的行数值加100。类似TDDL 方案。

总体上保持递增。

严格递增，可以用redis做。





## 字节跳动 常考算法题

作者：sam3125C
链接：https://www.nowcoder.com/discuss/377141
来源：牛客网



✅ LeetCode 001. Two Sum 

✅ LeetCode 015. 3Sum (可能会问 LeetCode 18. 4Sum 思路) 

✅ LeetCode 020. Valid Parentheses 

✅ LeetCode 021. Merge Two Sorted Lists 

 LeetCode 025. Reverse Nodes in k-Group 以及 变形题：从尾部开始翻转 k group. 

https://github.com/iamshuaidi/algo-basic/blob/master/%E5%AD%A6%E7%AE%97%E6%B3%95/%E5%86%8D%E7%8E%B0%E6%A0%A1%E6%8B%9B%E7%AE%97%E6%B3%95%E9%9D%A2%E8%AF%95%E7%8E%B0%E5%9C%BA/%E8%AE%B0%E4%B8%80%E9%81%93%E5%AD%97%E8%8A%82%E8%B7%B3%E5%8A%A8%E7%9A%84%E7%AE%97%E6%B3%95%E9%9D%A2%E8%AF%95%E9%A2%98%EF%BC%9A%E5%8F%98%E5%BD%A2%E7%9A%84%E9%93%BE%E8%A1%A8%E5%8F%8D%E8%BD%AC.md



 ✅ LeetCode 053. Maximum Subarray 

 ✅ LeetCode 066. Plus One（等价于：高精度加法） 

 ✅ LeetCode 098. Validate Binary Search Tree 

 ✅ LeetCode 110. Balanced Binary Tree 

 ✅ LeetCode 134. Gas Station 

 ✅ LeetCode 1214. Two Sum BSTs

 ✅ LeetCode 136. Single Number 

 LeetCode 137. Single Number II 

 LeetCode 146. LRU Cache（变形题：带有过期时间的 LRU 缓存） 

  ✅ LeetCode 206. Reverse Linked List 

  ✅ LeetCode 215. Kth Largest Element in an Array（等价于：快速[排序]()） 

 LeetCode 232. Implement Queue using Stacks 

 LeetCode 328. Odd Even Linked List 

 LeetCode 415. Add Strings（等价于：[大数加法]()） 

 LeetCode 470：rand7() rand10() 

 LeetCode 496. Next Greater Element I（时间复杂度O(n)） 

 LeetCode 716. Max Stack（两个栈实现最大栈，要求 pop，push，get_max 都为O(1)） 

 LeetCode 860. Lemonade Change 

 LeetCode 862. Shortest Subarray with Sum at Least K 

 LeetCode 876. Middle of the Linked List 

 LeetCode 946. Validate Stack Sequences

 ✅ 322 零钱兑换 

树的非递归先序遍历。

回行矩阵遍历。

二叉树多个节点的最近公共祖先



https://github.com/YaxeZhang/Just-Code



字节：

作者：Liz_wang
链接：https://www.nowcoder.com/discuss/434895?type=2
来源：牛客网



**一面：** 

 1、请详细描述三次握手和四次挥手的过程，要求熟悉三次握手和四次挥手的机制，要求画出状态图。 

 2、四次挥手中TIME_WAIT状态存在的目的是什么？ 

 3、TCP是通过什么机制保障可靠性的？（从四个方面进行回答，ACK确认机制、超时重传、滑动窗口以及流量控制，深入的话要求详细讲出流量控制的机制。） 

 4、描述线程、进程以及协程的区别？ 

 5、GO语言中的协程与Python中的协程的区别？ 

 6、网络IO模型有哪些？（5种网络I/O模型，阻塞、非阻塞、I/O多路复用、信号驱动IO、异步I/O） 

 7、I/O多路复用中select/poll/epoll的区别？ 

 8、客户端访问url到服务器，整个过程会经历哪些？ 

 9、描述HTTPS和HTTP的区别。 

 10、HTTP协议的请求报文和响应报文格式。 

 11、HTTP的状态码有哪些？ 

 12、描述一下[redis]()有哪些数据结构。（基础的数据结构有5种，String/List/Hash/Set/Zset；高级数据结构有：HyperLogLog/BitMap/BloomFilter/GeoHash） 

  

 13、面试官还问了BloomFilter的原理以及Zset的实现原理。 

  

 14、MySQL场景题目（面试官提供场景，要求写出查询SQL，考察联合语句，如何分页以及复杂语句的优化） 

 15、裸写[算法]()：树的非递归先序遍历。 

 


 **二面：** 

 1、先详细介绍最近的[项目]()，之前[项目]()经验里写了一个分布式的[项目]()，面试官着重讨论了这个[项目]()的实现方案，引申出分布式事务以及分布式一致性等问题，同时会要求在当前[项目]()的基础上附加条件，要求提供解决方案。 

 2、还问了一些API业务的架构问题，负载均衡、CDN、DNS等问题。 

 3、也问到了HTTP相关问题，要求描述HTTP的版本之间的区别，主要是1.0/1.1/2.0三个版本的区别。 

 4、裸写[算法]()：回行矩阵遍历。 

 


 **三面****:** 

 1、首先也是考察[项目]()经验，但是着重系统设计，会抽一段之前的[项目]()经验(跟二面的经验肯定不同)，要求你描述目前的方案，以及缺点。 

 2、要求模块化，如果要求对目前系统做微服务架构，如何进行服务的拆分，拆分的规则是什么，考察微服务架构相关知识，服务治理（限流、降级、熔断）。 

 3、裸写[算法]()：[二叉树]()多个节点的最近公共祖先。



### 二分法

https://leetcode-cn.com/problems/find-first-and-last-position-of-element-in-sorted-array/solution/da-jia-bu-yao-kan-labuladong-de-jie-fa-fei-chang-2/





阿里：

1. 如何动态分表（0 downtime）怎么路由database的traffic

     分库分表，垂直拆分（把列拆开），水平拆分（把数据分拆到不同的表中）

     数据库的双写迁移方案，旧表新表一起写。如果旧数据来，就不往新表里面加，确保新表写的新数据不会被旧数据给覆盖，（可以检查modified字段）。route的话可以选择mycat（proxy层中间件）或者 sharding-jdbc （client层的方案）作为数据库中间件。

2. Redis，为什么选这个技术选型

3. 什么是index，为什么快

    1. 索引本身就是一个排序好的结构，并且比原表小很多，可以一次加载很多进入内存，减少IO开销。
    2. 索引确定了数据位置，直接读取磁盘上相应数据块，速度快

4. 1000亿个数字，找出出现的最多的10个（分情况做，时间复杂度，空间复杂度来考虑问题）要考虑的东西，比如，单机单核内存足够，我不用担心内存，都足够大的话，我可以直接sort，nlogn的复杂度，简单。如果是单机多核，内存足够的话，可以直接partition到n份，然后每份发给每个线程来做。然后归并。这个有个问题是，有的线程做的很慢，会拖累整个进度。解决办法是，把partition多分点，快的结束了再去认领新的任务。如果是单机单核内存受限，那用hash(x)%M，将原文件中的数据切割成M小文件，如果小文件仍大于内存大小，继续采用Hash的方法对数据文件进行分割，知道每个小文件小于内存大小，这样每个文件可放到内存中处理。多机内存受限的话，为了合理利用多台机器的资源，可将数据分发到多台机器上，每台机器采用（3）中的策略解决本地的数据。

     top K问题很适合采用MapReduce框架解决，用户只需编写一个Map函数和两个Reduce 函数，然后提交到Hadoop（采用Mapchain和Reducechain）上即可解决该问题。具体而言，就是首先根据数据值或者把数据hash(MD5)后的值按照范围划分到不同的机器上，最好可以让数据划分后一次读入内存，这样不同的机器负责处理不同的数值范围，实际上就是Map。得到结果后，各个机器只需拿出各自出现次数最多的前N个数据，然后汇总，选出所有的数据中出现次数最多的前N个数据，这实际上就是Reduce过程。对于Map函数，采用Hash算法，将Hash值相同的数据交给同一个Reduce task；对于第一个Reduce函数，采用HashMap统计出每个词出现的频率，对于第二个Reduce 函数，统计所有Reduce task，输出数据中的top K即可。

     位图法去重可以节约空间。但是问题是，如果数据量不大，但是最大值特别大，其实会浪费空间。另外只能用来查重和去重，不能用来统计数字个数

5. CSRF 是什么，定义精简

     跨站请求伪造 CSRF（Cross-site request forgery）通过伪装来自受信任用户的请求来利用受信任的网站。**根本原因**是服务器对用户身份的过分信任或验证机制的不完善。

     

6. RPC是什么，精简

7. dubbo是什么，精简



> TIME-WAIT 为什么要等待 2MSL？Maximum segment lifetime

- 第一，为了保证 A 发送的最后一个 ACK 报文段能够到达 B。这个 ACK 报文段有可能丢失，因而使处在 LAST-ACK 状态的 B 收不到对已发送的 FIN+ACK 报文段 的确认。B 会超时重传这个 FIN+ACK 报文段，而 A 就能在 2MSL 时间内收到这个重传的 FIN+ACK 报文段。接着 A 重传一次确认，重新启动 2MSL 计时器。最后，A 和 B 都正常进入到 CLOSED 状态。**如果 A 在 TIME-WAIT 状态不等待一段时间，而是在发送完 ACK 报文段后立即释放连接，那么就无法收到 B 重传的 FIN+ACK 报文段，因而也不会再发送一次确认报文段。**这样，B就无法按照正常步骤进入 CLOSED 状态。
- 第二，防止“已失效的连接请求报文段”出现在本连接中。A 在发送完最后一个 ACK 报文段后，再经过时间 2MSL，就可以使本连接持续的时间内所产生的所有报文段都从网络中消失。这样就可以使下一个新的连接中不会出现这种旧的连接请求报文段。



操作系统：Semaphore 和 Mutex的区别

**锁是服务于共享资源的；而semaphore是服务于多个线程间的执行的逻辑顺序的**



如何定位找到crash的问题所在

如果是mobile的话，我们可以控制api访问某一台机器。（stage/int）

Flight recorder java  可以记录线程的所有的状态数据之类



字节：

项目

概率题，rand6 -> rand9, 如何等概率9个人中取出2个。 C（9，2）= 36， 和投出2次骰子的出现的次数一样也是36次，用一个表一一对应即可

列车站点如何售票，表示分段售卖

sql：插入和查询比较慢怎么办

sql：

```
查找2门课不及格的学生姓名
学生表：student(stu_id,name,birthday,gender)
成绩表：score(stu_id,course_id,score)


select s.stuid, count(distinct course_id)
From student s left join score c on a.stuid = c.stuid
Where c. score <60
Group by s.stuid
Having count(distinct course_id) = 2
```

算法：找到重复的最长子串 substring



一个好的网址：

https://raymond-zhao.top/campus-interview/#/Network/HTTP



如何设计一个秒杀系统

https://github.com/yunfeiyanggzq/miaosha#%E5%A6%82%E4%BD%95%E8%AE%BE%E8%AE%A1%E4%B8%80%E4%B8%AA%E7%A7%92%E6%9D%80%E7%B3%BB%E7%BB%9F





哪几种线程的创建方法

Java使用Thread类代表线程，所有的线程对象都必须是Thread类或其子类的实例。Java可以用四种方式来创建线程，如下所示：

1）继承Thread类创建线程

2）实现Runnable接口创建线程

3）使用Callable和Future创建线程

4）使用线程池例如用Executor框架





ConcurrentHashMap

线程池，以及参数

```
/*
 问题：实现一个多线程类，并用该线程类实例化3个线程A,B,C；A线程打印字符A,B线程打印字符B，C线程打印字符C；启动这3个线程，
 要求启动线程的顺序为C线程->B线程->A线程，并且最后输出内容为：
A
B
C
不能用sleep函数，注意考虑线程安全问题。编程语言不限
---------------------------------------------------------------------
*/
```



## 解释一下 Object o = new Object();

1. 请解释一下对象的创建过程（半初始化）

    当new一个对象时，首先内存开辟一块空间，成员变量赋默认值（0或者null），字节码指令调用invokespecial才会赋初始值，调用astore_1时，栈空间的变量会和堆空间的对象建立关联

2. 加问 DCL（双检锁） 和 volatile 问题（指令重排序）

    Double_Checked_Lock，比如单例模式中，两次判断instance不为null。这个可见性其实是用synchronized来保障的，并不需要volatile来多此一举了。但是volatile有个禁止指令重排。这里的指令重排序主要体现在instance = new Singleton()这条语句上了。

    这条语句显然是个复合操作，可以简单分下，（已完成类加载 ，假设在堆上分配内存）

    1.在堆中分配对象内存

    2.填充对象必要信息+具体数据初始化+末位填充

    3.将引用指向这个对象的堆内地址

    那么，在完成1后，对象的大小和地址已经确定，因此，2和3其实存在指令重排序的可能。

    并且可以看到，3的操作明显比2要少，那么如果让2与3一起执行，并且反应到具体的顺序上变成了1-3-2.

    先完成3，引用变量instance先指向了在堆中给对象分配的空间，然后2仍在慢慢吞吞继续。

    这时候，被synchronized挡在外面的阻塞线程其实是不会有什么影响的，因为一定会等到对象创建完，首个拿锁者才会释放锁。

    那么关键是在，此刻如果在3完成而2未完成这个临界点，有一个新线程调用getInstance()，那么第一个if，会怎么样？

    答案是因为第一个if没在同步块里，而此时instance已经非空，指向具体内存地址了，所以直接返回此时未完成初始化的instance实例

    那么如果在Singleton里有个变量int number ,有个方法int getNumber()返回number，这时候调用

    Singleton.getInstance().getNumber();

    会怎样？

    不知道，可能会报错，或者会得到错误结果，但这就是我能想到的volatile避免的情况了。

    参考：https://blog.csdn.net/Lin_coffee/article/details/79890361

3. 对象在内存中的布局

    一个Java对象在内存中包括对象头、实例数据和补齐填充3个部分

4. 对象头包括什么（markword, klasspointer, synchronized 锁信息）

    **Mark Word**：包含一系列的标记位，比如轻量级锁的标记位，偏向锁标记位等等。在32位系统占4字节，在64位系统中占8字节；

    **Class Pointer**：用来指向对象对应的Class对象（其对应的元数据对象）的内存地址。在32位系统占4字节，在64位系统中占8字节；

    **Length**：如果是数组对象，还有一个保存数组长度的空间，占4个字节；
    参考：https://www.jianshu.com/p/91e398d5d17c

5. 对象怎么定位（直接，间接）

6. 对象怎么分配（栈，本地栈空间，eden，old）

7. Object o = new Object() 在内存中占用多少字节

    32位机和64位机不一样。

    在32位系统下，存放Class Pointer的空间大小是4字节，MarkWord是4字节，对象头为8字节;

    在64位系统下，存放Class Pointer的空间大小是8字节，MarkWord是8字节，对象头为16字节;

    64位开启指针压缩的情况下，存放Class Pointer的空间大小是4字节，`MarkWord`是8字节，对象头为12字节;

    如果是数组对象，对象头的大小为：数组对象头8字节+数组长度4字节+对齐4字节=16字节。其中对象引用占4字节（未开启指针压缩的64位为8字节），数组`MarkWord`为4字节（64位未开启指针压缩的为8字节）;

    静态属性不算在对象大小内。


    链接：https://www.jianshu.com/p/91e398d5d17c





