#Java & Socket 通讯实验报告
####学号：13331158 林义涵  
##异常处理
按照程序错误类型、错误发现时刻及错误处理原则，可以将错误大致分为三类：违反语法规 范的错误称为语法错，这可以在程序编译时发现；在程序语义上存在错误，则称为语义错，通常在 程序运行时才能被发现；其它就是系统无法发现的逻辑错误，这需要特别的工具与方法才能处理。  

1. throw: 直接抛出异常  
throw new MyException();
2. throws:关键字通常被应用在声明方法时，用来指定可能抛出的异常
        public void func() throws MyException{            if(y<0) thorw new MyException();        }##多线程1. 通过实现Runnable接口定义新线程

		class Counter implements Runnable{
			public void run() {
				for (inti = 0; i < 100; i++) 	System.out.println("计数器＝" + i);
			}
		}
		public class RunnableThread{
			public static void main(String[] args) {
				Counter counter= new Counter();
				Thread thread= new Thread(counter); thread.start();
				System.out.println("主程序结束");
			}
		}
2. 通过继承Thread类定义新线程

		public class SubclassThreadextends Thread {
			public void run() {
				while (true) { // 执行线程自身的任务
					try {
						sleep(5 * 1000);
						break;
					} catch (InterruptedExceptionexc) { // 睡眠被中断
					}
				}
			}

			public static void main(String[] args) {
				Thread thread= new SubclassThread(); thread.start();
				System.out.println("主程序结束");
			}
		}
##套接字Socket API
套接字 Socket API提供给用户一种处理通信的方法，使得相关进程可以存在于横跨网络的 不同的工作站上。套接字类型有二种方式：  

- 流式套接字，它提供进程之间的逻辑连接，并且支持可靠的数据交换。 
- 数据报套接字，它是无连接的并且不可靠。 

基于 socket 通信的客户程序首先通过指定主机（主机名或 InetAddress 的实例）和端口号 构造一个 socket，然后调用 Socket 类的 getInputStream()和 getOutputStream()分别打开与该 socket 关联的输入流和输出流，依照服务程序约定的协议读取输入流或写入输出流，最后依次 关闭输入∕输出流和 socket。 
##反射机制
Java 语言的 反射（Reflection）机制则可以在程序运行时判断任意一个对象所属的类，构造任 意一个类的对象，判断任意一个类所具有的成员变量和方法，调用任意一个对象的 方法，或者生成动态代理。  

如果使用静态代理方式，那么对于每一个需要代理的类，都要手工编写静 态代理类的源代码；如果使用动态代理方式，那么只要编写一个动态代理工厂类， 它就能自动创建各种类型的动态代理类，从而大大简化了编程，并且提高了软件系 统的可扩展。 