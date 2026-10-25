---
title: "应用程序开发"
description: "为什么要编写I2P专用应用程序、关键概念、开发选项和入门指南"
slug: "applications"
aliases:
  - "/zh/docs/develop/applications"
  - "/zh/docs/develop/applications/"
  - "/zh/applications"
  - "/zh/applications/"
lastUpdated: "2013-05"
accurateFor: "0.9.6"
---

## 为什么要编写I2P专用代码？

在I2P中有多种使用应用程序的方式。使用[I2PTunnel](/docs/api/i2ptunnel/)，您可以使用常规应用程序而无需编程显式的I2P支持。这对于客户端-服务器场景非常有效，当您需要连接到单个网站时。您可以简单地使用I2PTunnel创建一个tunnel来连接到该网站，如图1所示。

如果您的应用程序是分布式的，它将需要连接到大量对等节点。使用I2PTunnel时，您需要为每个要联系的对等节点创建一个新的tunnel，如图2所示。当然，这个过程可以自动化，但运行大量I2PTunnel实例会产生很大的开销。此外，对于许多协议，您需要强制每个人为所有对等节点使用同一组端口——例如，如果您想可靠地运行DCC聊天，每个人都需要同意端口10001是Alice，端口10002是Bob，端口10003是Charlie，以此类推，因为协议包含TCP/IP特定信息（主机和端口）。

一般的网络应用程序通常会发送大量额外数据，这些数据可能被用来识别用户身份。主机名、端口号、时区、字符集等信息经常在用户不知情的情况下被发送。因此，在设计网络协议时专门考虑匿名性可以避免泄露用户身份。

在确定如何在I2P之上进行交互时，还需要考虑效率问题。streaming库及其上构建的应用程序使用类似TCP的握手操作，而核心I2P协议（I2NP和I2CP）则严格基于消息传递（类似UDP或在某些情况下是原始IP）。重要的区别在于，使用I2P时，通信是在长肥网络（long fat network）上运行的——每个端到端消息都会有不可忽略的延迟，但可能包含高达几KB的有效载荷。对于需要简单请求和响应的应用程序，可以通过使用（尽力而为的）数据报来消除任何状态并减少启动和关闭握手产生的延迟，而无需担心MTU检测或消息分片问题。

![使用 I2PTunnel 创建服务器-客户端连接只需要创建一个 tunnel。](/images/i2ptunnel_serverclient.png)

*图1：使用I2PTunnel创建服务器-客户端连接只需要创建一个隧道。*

![为点对点应用程序设置连接需要大量的 tunnel。](/images/i2ptunnel_peertopeer.png)

*图2：为点对点应用程序建立连接需要大量的tunnel。*

总结来说，编写I2P专用代码的几个原因：

- 创建大量的 I2PTunnel 实例会消耗大量资源，这对分布式应用程序来说是个问题（每个对等节点都需要一个新的 tunnel）。
- 通用网络协议通常会发送大量可用于识别用户的额外数据。专门为 I2P 编程可以创建不会泄露此类信息的网络协议，从而保持用户匿名和安全。
- 为常规互联网设计的网络协议在 I2P 上可能效率低下，因为 I2P 是一个延迟更高的网络。

I2P 支持标准的 [plugins 接口](/docs/specs/plugin/) 供开发者使用，以便应用程序可以轻松集成和分发。

使用Java编写且可通过标准webapps/app.war的HTML界面访问/运行的应用程序可以考虑纳入I2P发行版中。

---

## 重要概念

使用I2P时需要适应一些变化：

### Destination ~= host+port

在I2P上运行的应用程序从唯一的密码学安全端点（"destination"）发送和接收消息。用TCP或UDP术语来说，destination基本上可以被视为等同于主机名加端口号对，尽管存在一些差异。

- I2P destination 本身是一个加密构造——发送到其中的所有数据都被加密，就像普遍部署了 IPsec 一样，并且端点的（匿名化）位置被签名，就像普遍部署了 DNSSEC 一样。
- I2P destination 是移动标识符——它们可以从一个 I2P router 移动到另一个（或者甚至可以"多宿主"——同时在多个 router 上运行）。这与 TCP 或 UDP 世界非常不同，在那里单个端点（端口）必须保持在单个主机上。
- I2P destination 是丑陋且庞大的——在幕后，它们包含一个用于加密的 2048 位 ElGamal 公钥，一个用于签名的 1024 位 DSA 公钥，以及一个可变大小的证书，其中可能包含工作量证明或盲化数据。

虽然已经存在一些方法可以用简短美观的名称来指代这些冗长难看的目标地址（例如"irc.duck.i2p"），但这些技术并不能保证全局唯一性（因为它们是本地存储在每个人机器上的数据库中的），而且当前的机制在可扩展性和安全性方面都不够理想（主机列表的更新是通过对命名服务的"订阅"来管理的）。也许有一天会出现某种安全、人类可读、可扩展且全局唯一的命名系统，但应用程序不应该依赖于它的存在，因为有些人认为这样的系统是不可能实现的。关于命名系统的[更多信息](/docs/overview/naming/)可供参考。

虽然大多数应用程序不需要区分协议和端口，但 I2P *确实* 支持它们。复杂的应用程序可以在每条消息的基础上指定协议、源端口和目标端口，以在单个目标上复用流量。详细信息请参见 [datagram 页面](/docs/api/datagrams/)。简单的应用程序通过监听目标的"所有协议"和"所有端口"来运行。

### 匿名性和机密性

I2P 为网络中传输的所有数据提供透明的端到端加密和身份验证——如果 Bob 发送数据到 Alice 的 destination，只有 Alice 的 destination 能够接收到；如果 Bob 使用数据报或流式库，Alice 可以确定发送数据的就是 Bob 的 destination。

当然，I2P 透明地匿名化了 Alice 和 Bob 之间发送的数据，但它不能匿名化他们发送内容的内容。例如，如果 Alice 向 Bob 发送一个包含她全名、政府身份证件和信用卡号码的表单，I2P 对此无能为力。因此，协议和应用程序应该考虑它们试图保护哪些信息以及愿意暴露哪些信息。

### I2P 数据报可达几KB大小

使用 I2P 数据报（无论是原始数据报还是可回复数据报）的应用程序本质上可以按照 UDP 的方式来理解——数据报是无序的、尽力而为的、无连接的——但与 UDP 不同的是，应用程序不需要担心 MTU 检测，可以直接发送大数据报。虽然上限名义上是 32 KB，但消息会被分片传输，从而降低了整体的可靠性。目前不建议使用超过 10 KB 的数据报。详情请参阅[数据报页面](/docs/api/datagrams/)。对于许多应用程序来说，10 KB 的数据足以承载整个请求或响应，使它们能够作为类似 UDP 的应用程序在 I2P 中透明运行，而无需编写分片、重传等功能。

---

## 开发选项

有几种通过I2P发送数据的方式，每种都有各自的优缺点。streaming lib是推荐的接口，被大多数I2P应用程序使用。

### 流媒体库

[完整的流式库](/docs/api/streaming/)现在是标准接口。它允许使用类似TCP的套接字进行编程，如[流式开发指南](#developing-with-the-streaming-library)中所述。

### BOB

BOB 是 [Basic Open Bridge](/docs/legacy/bob/)（基本开放桥接），允许任何语言的应用程序建立到 I2P 和从 I2P 的流连接。目前它缺乏 UDP 支持，但计划在不久的将来支持 UDP。BOB 还包含几个工具，如目标密钥生成，以及验证地址是否符合 I2P 规范。最新信息和使用 BOB 的应用程序可以在这个 [I2P 站点](http://bob.i2p/) 找到。

### SAM, SAM V2, SAM V3

*不推荐使用 SAM。SAM V2 可以接受，推荐使用 SAMv3。*

SAM 是 [Simple Anonymous Messaging](/docs/legacy/sam/) 协议，允许用任何语言编写的应用程序通过普通 TCP 套接字与 SAM 桥接器通信，让该桥接器复用其所有 I2P 流量，透明地协调加密/解密和基于事件的处理。SAM 支持三种操作模式：

- 流（streams），当 Alice 和 Bob 希望可靠且有序地互相发送数据时使用
- 可回复数据报（repliable datagrams），当 Alice 想要向 Bob 发送一条 Bob 可以回复的消息时使用
- 原始数据报（raw datagrams），当 Alice 想要尽可能地压榨带宽和性能，而 Bob 不关心数据发送者是否经过身份验证时使用（例如传输的数据本身具有自验证性）

SAMv3与SAM和SAM V2的目标相同，但不需要多路复用/解复用。每个I2P流都通过应用程序和SAM网桥之间自己的套接字处理。此外，应用程序可以通过与SAM网桥的数据报通信来发送和接收数据报。

[SAM V2](/docs/legacy/samv2/) 是 imule 使用的新版本，修复了 [SAM](/docs/legacy/sam/) 中的一些问题。

[SAM V3](/docs/api/samv3/) 自版本 1.4.0 起被 imule 使用。

### I2PTunnel

I2PTunnel 应用程序允许应用程序通过创建 I2PTunnel "客户端"应用程序（监听特定端口并在该端口的套接字打开时连接到特定的 I2P destination）或 I2PTunnel "服务器"应用程序（监听特定的 I2P destination，每当收到新的 I2P 连接时就代理到特定的 TCP 主机/端口）来构建与对等节点之间特定的类似 TCP 的 tunnel。这些数据流是 8 位清洁的，通过与 SAM 使用的相同流式库进行身份验证和保护，但创建多个唯一的 I2PTunnel 实例会涉及不小的开销，因为每个实例都有自己唯一的 I2P destination 和自己的 tunnel 集合、密钥等。

### SOCKS

I2P 支持 SOCKS V4 和 V5 代理。出站连接运行良好。入站（服务器）和 UDP 功能可能不完整且未经测试。

### Ministreaming

*已移除*

过去曾有一个简单的"ministreaming"库，但现在 ministreaming.jar 只包含完整流媒体库的接口。

### 数据报

*推荐用于类 UDP 应用*

[Datagram 库](/docs/api/datagrams/) 允许发送类似 UDP 的数据包。可以使用：

- 可回复数据报
- 原始数据报

### I2CP

*不推荐*

[I2CP](/docs/specs/i2cp/) 本身是一个与语言无关的协议，但要在Java以外的语言中实现I2CP库，需要编写大量代码（加密例程、对象编组、异步消息处理等）。虽然有人可以用C或其他语言编写I2CP库，但使用C SAM库可能会更有用。

### Web 应用程序

I2P 自带 Jetty Web 服务器，配置为使用 Apache 服务器也很简单。任何标准的 Web 应用技术都应该可以正常工作。

---

## 开始开发——简单指南

使用 I2P 进行开发需要一个正常工作的 I2P 安装和您选择的开发环境。如果您使用 Java，可以使用 [streaming library](#developing-with-the-streaming-library) 或 datagram library 开始开发。使用其他编程语言时，可以使用 SAM 或 BOB。

### 使用Streaming Library进行开发

以下示例展示了如何使用流式库创建类似TCP的客户端和服务器应用程序。

这需要在你的 classpath 中包含以下库：

- `$I2P/lib/streaming.jar`: 流传输库本身
- `$I2P/lib/mstreaming.jar`: 流传输库的工厂类和接口
- `$I2P/lib/i2p.jar`: 标准 I2P 类、数据结构、API 和实用工具

您可以从 I2P 安装中获取这些文件，或从 Maven Central 添加以下依赖：

- `net.i2p:i2p`
- `net.i2p.client:streaming`

网络通信需要使用I2P网络套接字。为了演示这一点，我们将创建一个应用程序，客户端可以向服务器发送文本消息，服务器会打印这些消息并将它们发送回客户端。换句话说，服务器将充当回显功能。

我们将首先初始化服务器应用程序。这需要获取一个I2PSocketManager并创建一个I2PServerSocket。我们不会向I2PSocketManagerFactory提供现有目标地址的保存密钥，因此它将为我们创建一个新的目标地址。所以我们将向I2PSocketManager请求一个I2PSession，这样我们就可以找到创建的目标地址，因为我们稍后需要复制粘贴该信息以便客户端可以连接到我们。

```java
package i2p.echoserver;

import net.i2p.client.I2PSession;
import net.i2p.client.streaming.I2PServerSocket;
import net.i2p.client.streaming.I2PSocketManager;
import net.i2p.client.streaming.I2PSocketManagerFactory;

public class Main {

    public static void main(String[] args) {
        //Initialize application
        I2PSocketManager manager = I2PSocketManagerFactory.createManager();
        I2PServerSocket serverSocket = manager.getServerSocket();
        I2PSession session = manager.getSession();
        //Print the base64 string, the regular string would look like garbage.
        System.out.println(session.getMyDestination().toBase64());
        //The additional main method code comes here...
    }

}
```
*代码示例1：初始化服务器应用程序。*

一旦我们有了I2PServerSocket，我们就可以创建I2PSocket实例来接受来自客户端的连接。在这个例子中，我们将创建一个单独的I2PSocket实例，它一次只能处理一个客户端。真正的服务器必须能够处理多个客户端。要做到这一点，必须创建多个I2PSocket实例，每个实例都在单独的线程中。一旦我们创建了I2PSocket实例，我们就读取数据，打印它并将其发送回客户端。

```java
package i2p.echoserver;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.ConnectException;
import java.net.SocketTimeoutException;
import net.i2p.I2PException;
import net.i2p.client.streaming.I2PSocket;
import net.i2p.util.I2PThread;

import net.i2p.client.I2PSession;
import net.i2p.client.streaming.I2PServerSocket;
import net.i2p.client.streaming.I2PSocketManager;
import net.i2p.client.streaming.I2PSocketManagerFactory;

public class Main {

    public static void main(String[] args) {
        I2PSocketManager manager = I2PSocketManagerFactory.createManager();
        I2PServerSocket serverSocket = manager.getServerSocket();
        I2PSession session = manager.getSession();
        //Print the base64 string, the regular string would look like garbage.
        System.out.println(session.getMyDestination().toBase64());

        //Create socket to handle clients
        I2PThread t = new I2PThread(new ClientHandler(serverSocket));
        t.setName("clienthandler1");
        t.setDaemon(false);
        t.start();
    }

    private static class ClientHandler implements Runnable {

        public ClientHandler(I2PServerSocket socket) {
            this.socket = socket;
        }

        public void run() {
            while(true) {
                try {
                    I2PSocket sock = this.socket.accept();
                    if(sock != null) {
                        //Receive from clients
                        BufferedReader br = new BufferedReader(new InputStreamReader(sock.getInputStream()));
                        //Send to clients
                        BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(sock.getOutputStream()));
                        String line = br.readLine();
                        if(line != null) {
                            System.out.println("Received from client: " + line);
                            bw.write(line);
                            bw.flush(); //Flush to make sure everything got sent
                        }
                        sock.close();
                    }
                } catch (I2PException ex) {
                    System.out.println("General I2P exception!");
                } catch (ConnectException ex) {
                    System.out.println("Error connecting!");
                } catch (SocketTimeoutException ex) {
                    System.out.println("Timeout!");
                } catch (IOException ex) {
                    System.out.println("General read/write-exception!");
                }
            }
        }

        private I2PServerSocket socket;

    }

}
```
*代码示例2：接受来自客户端的连接并处理消息。*

当你运行上述服务器代码时，它应该会打印出类似这样的内容（但没有换行符，应该只是一大块字符）：

```
y17s~L3H9q5xuIyyynyWahAuj6Jeg5VC~Klu9YPquQvD4vlgzmxn4yy~5Z0zVvKJiS2Lk
poPIcB3r9EbFYkz1mzzE3RYY~XFyPTaFQY8omDv49nltI2VCQ5cx7gAt~y4LdWqkyk3au
...
```
这是服务器 Destination 的 base64 表示。客户端需要这个字符串来连接到服务器。

现在，我们将创建客户端应用程序。同样，初始化需要多个步骤。再次，我们需要首先获取一个I2PSocketManager。这次我们不会使用I2PSession和I2PServerSocket。相反，我们将使用服务器的Destination字符串来启动我们的连接。我们将要求用户提供Destination字符串，并使用此字符串创建一个I2PSocket。一旦我们有了I2PSocket，就可以开始向服务器发送和接收数据。

```java
package i2p.echoclient;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.InterruptedIOException;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.net.ConnectException;
import java.net.NoRouteToHostException;
import net.i2p.I2PException;
import net.i2p.client.streaming.I2PSocket;
import net.i2p.client.streaming.I2PSocketManager;
import net.i2p.client.streaming.I2PSocketManagerFactory;
import net.i2p.data.DataFormatException;
import net.i2p.data.Destination;

public class Main {

    public static void main(String[] args) {
        I2PSocketManager manager = I2PSocketManagerFactory.createManager();
        System.out.println("Please enter a Destination:");
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String destinationString;
        try {
            destinationString = br.readLine();
        } catch (IOException ex) {
            System.out.println("Failed to get a Destination string.");
            return;
        }
        Destination destination;
        try {
            destination = new Destination(destinationString);
        } catch (DataFormatException ex) {
            System.out.println("Destination string incorrectly formatted.");
            return;
        }
        I2PSocket socket;
        try {
            socket = manager.connect(destination);
        } catch (I2PException ex) {
            System.out.println("General I2P exception occurred!");
            return;
        } catch (ConnectException ex) {
            System.out.println("Failed to connect!");
            return;
        } catch (NoRouteToHostException ex) {
            System.out.println("Couldn't find host!");
            return;
        } catch (InterruptedIOException ex) {
            System.out.println("Sending/receiving was interrupted!");
            return;
        }
        try {
            //Write to server
            BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(socket.getOutputStream()));
            bw.write("Hello I2P!\n");
            //Flush to make sure everything got sent
            bw.flush();
            //Read from server
            BufferedReader br2 = new BufferedReader(new InputStreamReader(socket.getInputStream()));
            String s = null;
            while ((s = br2.readLine()) != null) {
                System.out.println("Received from server: " + s);
            }
            socket.close();
        } catch (IOException ex) {
            System.out.println("Error occurred while sending/receiving!");
        }
    }

}
```
*代码示例3：启动客户端并将其连接到服务器应用程序。*

最后，您可以同时运行服务器和客户端应用程序。首先，启动服务器应用程序。它会打印一个 Destination 字符串（如上所示）。接下来，启动客户端应用程序。当它请求 Destination 字符串时，您可以输入服务器打印的字符串。然后客户端会发送 'Hello I2P!'（连同换行符）给服务器，服务器会打印该消息并将其发送回客户端。

恭喜，您已成功通过 I2P 进行通信！

---

## 现有应用程序

如果您想要贡献，请联系我们。

- [I2P-Bote](http://i2pbote.i2p/) - 联系 HungryHobo
- [Syndie](http://syndie.i2p2.de/)
- [IMule](http://www.imule.i2p/)
- [I2Phex](http://forum.i2p/viewforum.php?f=25)

另请参阅 [plugins.i2p](http://plugins.i2p/) 上的所有插件、[echelon.i2p](http://echelon.i2p/) 上列出的应用程序和源代码，以及托管在 [git.repo.i2p](http://git.repo.i2p/) 上的应用程序代码。

另请参阅I2P分发包中的捆绑应用程序 - SusiMail和I2PSnark。

---

## 应用程序想法

- NNTP 服务器 - 过去有过一些，目前没有
- Jabber 服务器 - 过去有过一些，目前有一个，可以访问公共互联网
- PGP 密钥服务器和/或代理
- 内容分发 / DHT 应用程序 - 重新启动 feedspace，移植 dijjer，寻找替代方案
- 协助 [Syndie](http://syndie.i2p2.de/) 开发
- 基于 Web 的应用程序 - 对于托管基于 Web 服务器的应用程序（如博客、粘贴板、存储、追踪、订阅等）来说，天空是极限。任何 Web 或 CGI 技术（如 Perl、PHP、Python 或 Ruby）都可以使用。
- 重新启动一些旧应用程序，其中几个之前在 i2p 源码包中 - bogobot、pants、proxyscript、q、stasher、socks proxy、i2ping、feedspace
