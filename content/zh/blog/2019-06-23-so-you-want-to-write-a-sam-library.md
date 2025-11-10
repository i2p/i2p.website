---
title: "所以你想编写一个 SAM 库"
date: 2019-06-23
author: "idk"
description: "编写 SAM 库的初学者指南！"
---

*或者，面向不太习惯阅读规范文档的人：如何与 [i2p](https://geti2p.net) 通信*

在我看来，I2P 最出色的功能之一是它的 SAM API，它可以用来在 I2P 与所选的应用程序或编程语言之间建立桥接。目前，已经有数十个适用于多种语言的 SAM 库，包括：

- [i2psam, for c++](https://github.com/i2p/i2psam)
- [libsam3, for C](https://github.com/i2p/libsam3)
- [txi2p for Python](https://github.com/str4d/txi2p)
- [i2plib for Python](https://github.com/l-n-s/i2plib)
- [i2p.socket for Python](https://github.com/majestrate/i2p.socket)
- [leaflet for Python](https://github.com/MuxZeroNet/leaflet)
- [gosam, for Go](https://github.com/eyedeekay/gosam)
- [sam3 for Go](https://github.com/eyedeekay/sam3)
- [node-i2p for nodejs](https://github.com/redhog/node-i2p)
- [haskell-network-anonymous-i2p](https://github.com/solatis/haskell-network-anonymous-i2p)
- [i2pdotnet for .Net languages](https://github.com/SamuelFisher/i2pdotnet)
- [rust-i2p](https://github.com/stallmanifold/rust-i2p)
- [and i2p.rb for ruby](https://github.com/dryruby/i2p.rb)

如果你正在使用这些语言中的任何一种，你也许已经可以使用现有库把你的应用移植到 I2P 上了。不过，这并不是本教程要讲的内容。本教程关注的是：当你想在一种新的语言中创建一个 SAM 库时，该怎么做。在本教程中，我将用 Java 实现一个新的 SAM 库。我之所以选择 Java，是因为目前还没有能把你与 SAM 连接起来的 Java 库；也因为 Java 在 Android 中的使用；还因为这是一门几乎每个人至少有*一点*经验的语言，因此希望你可以把它改写成你所选择的语言。

## 创建你的库

你如何设置自己的库会因你希望使用的编程语言而异。对于这个示例库，我们将使用 Java，因此可以像这样创建一个库：

```sh
mkdir jsam
cd jsam
gradle init --type java-library
```
或者，如果你使用的是 gradle 5 或更高版本：

```sh
gradle init --type java-library --project-name jsam
```
## 配置库

几乎任何 SAM 库都需要管理一些数据。它至少需要存储你打算使用的 SAM Bridge（SAM 桥接）的地址，以及你希望使用的签名类型。

### Storing the SAM address

我更倾向于将 SAM 地址分别存为一个 String 和一个 Integer，并在运行时通过函数将它们重新组合。

```java
public String SAMHost = "127.0.0.1";
public int SAMPort = 7656;
public String SAMAddress(){
    return SAMHost + ":" + SAMPort;
}
```
### Storing the Signature Type

对于 I2P Tunnel，有效的签名类型包括 DSA_SHA1、ECDSA_SHA256_P256、ECDSA_SHA384_P384、ECDSA_SHA512_P521、EdDSA_SHA512_Ed25519，但如果你至少实现了 SAM 3.1，则强烈建议默认使用 EdDSA_SHA512_Ed25519。在 Java 中，'enum' 数据结构非常适合完成这项任务，因为它旨在包含一组常量。将 enum 以及该 enum 的一个实例添加到你的 Java 类定义中。

```java
enum SIGNATURE_TYPE {
    DSA_SHA1,
    ECDSA_SHA256_P256,
    ECDSA_SHA384_P384,
    ECDSA_SHA512_P521,
    EdDSA_SHA512_Ed25519;
}
public SIGNATURE_TYPE SigType = SIGNATURE_TYPE.EdDSA_SHA512_Ed25519;
```
### 存储 SAM 地址

这就能可靠地存储由 SAM 连接使用的签名类型，但你仍然需要将其以字符串形式取回，以便将其传递给桥接器。

```java
public String SignatureType() {
    switch (SigType) {
        case DSA_SHA1:
            return "SIGNATURE_TYPE=DSA_SHA1";
        case ECDSA_SHA256_P256:
            return "SIGNATURE_TYPE=ECDSA_SHA256_P256";
        case ECDSA_SHA384_P384:
            return "SIGNATURE_TYPE=ECDSA_SHA384_P384";
        case ECDSA_SHA512_P521:
            return "SIGNATURE_TYPE=ECDSA_SHA512_P521";
        case EdDSA_SHA512_Ed25519:
            return "SIGNATURE_TYPE=EdDSA_SHA512_Ed25519";
    }
    return "";
}
```
测试很重要，所以让我们编写一些测试：

```java
@Test public void testValidDefaultSAMAddress() {
    Jsam classUnderTest = new Jsam();
    assertEquals("127.0.0.1:7656", classUnderTest.SAMAddress());
}
@Test public void testValidDefaultSignatureType() {
    Jsam classUnderTest = new Jsam();
    assertEquals("EdDSA_SHA512_Ed25519", classUnderTest.SignatureType());
}
```
一旦完成，开始创建你的构造函数。请注意，我们已经为库设置了默认值，这些默认值在迄今所有现有的 I2P router 上的默认情况下都很有用。

```java
public Jsam(String host, int port, SIGNATURE_TYPE sig) {
    SAMHost = host;
    SAMPort = port;
    SigType = sig;
}
```
## Establishing a SAM Connection

终于到精彩部分了。与 SAM bridge 的交互是通过向 SAM bridge 的地址发送一个"command"，然后将该命令的结果解析为一组基于字符串的键值对来完成的。记住这一点，我们先与之前定义的 SAM Address 建立一个可读写连接，然后编写一个"CommandSAM"函数和一个响应解析器。

### 存储签名类型

我们通过套接字（Socket）与 SAM 通信，因此为了连接到该套接字、从中读取并向其写入，你需要在 Jsam 类中创建以下私有变量：

```java
private Socket socket;
private PrintWriter writer;
private BufferedReader reader;
```
你还会希望通过创建一个函数，在构造函数中实例化这些变量。

```java
public Jsam(String host, int port, SIGNATURE_TYPE sig) {
    SAMHost = host;
    SAMPort = port;
    SigType = sig;
    startConnection();
}
public void startConnection() {
    try {
        socket = new Socket(SAMHost, SAMPort);
        writer = new PrintWriter(socket.getOutputStream(), true);
        reader = new BufferedReader(new InputStreamReader(socket.getInputStream()));
    } catch (Exception e) {
        //omitted for brevity
    }
}
```
### 获取签名类型：

现在一切都准备就绪，终于可以开始与 SAM 通信了。为了保持结构清晰，我们来创建一个函数，用于向 SAM 发送一条以换行符结尾的命令，并返回一个 Reply 对象，这个对象我们将在下一步创建：

```java
public Reply CommandSAM(String args) {
    writer.println(args + "\n");
    try {
        String repl = reader.readLine();
        return new Reply(repl);
    } catch (Exception e) {
        //omitted for brevity
    }
}
```
请注意，我们将上一步从 socket（套接字）创建的 writer（写入器）和 reader（读取器）作为该 socket 的输入与输出。当我们从 reader 收到回复时，我们把该字符串传给 Reply 构造函数，由其解析并返回 Reply 对象。

### Parsing a reply and creating a Reply object.

为了更容易地处理回复，我们将使用一个 Reply 对象来自动解析从 SAM bridge 获取的结果。一个回复至少包含一个 topic、一个 type 和一个 result，以及任意数量的键值对。

```java
public class Reply {
    String topic;
    String type;
    REPLY_TYPES result;
    Map<String, String> replyMap = new HashMap<String, String>();
```
如你所见，我们将把“result”存储为一个枚举类型 REPLY_TYPES。该枚举包含 SAM bridge（SAM 网桥）可能返回的所有响应结果。

```java
enum REPLY_TYPES {
    OK,
    CANT_REACH_PEER,
    DUPLICATED_ID,
    DUPLICATED_DEST,
    I2P_ERROR,
    INVALID_KEY,
    KEY_NOT_FOUND,
    PEER_NOT_FOUND,
    TIMEOUT;
    public static REPLY_TYPES set(String type) {
        String temp = type.trim();
        switch (temp) {
        case "RESULT=OK":
            return OK;
        case "RESULT=CANT_REACH_PEER":
            return CANT_REACH_PEER;
        case "RESULT=DUPLICATED_ID":
            return DUPLICATED_ID;
        case "RESULT=DUPLICATED_DEST":
            return DUPLICATED_DEST;
        case "RESULT=I2P_ERROR":
            return I2P_ERROR;
        case "RESULT=INVALID_KEY":
            return INVALID_KEY;
        case "RESULT=KEY_NOT_FOUND":
            return KEY_NOT_FOUND;
        case "RESULT=PEER_NOT_FOUND":
            return PEER_NOT_FOUND;
        case "RESULT=TIMEOUT":
            return TIMEOUT;
        }
        return I2P_ERROR;
    }
    public static String get(REPLY_TYPES type) {
        switch (type) {
        case OK:
            return "RESULT=OK";
        case CANT_REACH_PEER:
            return "RESULT=CANT_REACH_PEER";
        case DUPLICATED_ID:
            return "RESULT=DUPLICATED_ID";
        case DUPLICATED_DEST:
            return "RESULT=DUPLICATED_DEST";
        case I2P_ERROR:
            return "RESULT=I2P_ERROR";
        case INVALID_KEY:
            return "RESULT=INVALID_KEY";
        case KEY_NOT_FOUND:
            return "RESULT=KEY_NOT_FOUND";
        case PEER_NOT_FOUND:
            return "RESULT=PEER_NOT_FOUND";
        case TIMEOUT:
            return "RESULT=TIMEOUT";
        }
        return "RESULT=I2P_ERROR";
    }
};
```
现在让我们创建构造函数：它接收从套接字收到的回复字符串作为参数，对其进行解析，并使用这些信息来初始化回复对象。该回复以空格分隔，键值对由等号连接，并以换行符结束。

```java
public Reply(String reply) {
    String trimmed = reply.trim();
    String[] replyvalues = reply.split(" ");
    if (replyvalues.length < 2) {
        //omitted for brevity
    }
    topic = replyvalues[0];
    type = replyvalues[1];
    result = REPLY_TYPES.set(replyvalues[2]);

    String[] replyLast = Arrays.copyOfRange(replyvalues, 2, replyvalues.length);
    for (int x = 0; x < replyLast.length; x++) {
        String[] kv = replyLast[x].split("=", 2);
        if (kv.length != 2) {

        }
        replyMap.put(kv[0], kv[1]);
    }
}
```
最后，为了方便起见，我们给 Reply 对象添加一个 toString() 函数，它返回该 Reply 对象的字符串表示。

```java
public String toString() {
    return topic + " " + type + " " + REPLY_TYPES.get(result) + " " + replyMap.toString();
}
}
```
### 连接到 SAM 端口

现在我们已经准备好通过发送一条 "Hello" 消息与 SAM 建立通信。如果你正在编写一个新的 SAM 库，通常应至少面向 SAM 3.1，因为它在 I2P 和 i2pd 中都可用，并且引入了对 SIGNATURE_TYPE 参数的支持。

```java
public boolean HelloSAM() {
    Reply repl = CommandSAM("HELLO VERSION MIN=3.0 MAX=3.1 \n");
    if (repl.result == Reply.REPLY_TYPES.OK) {
        return true;
    }
    System.out.println(repl.String());
    return false;
}
```
如你所见，我们使用之前创建的 CommandSAM 函数发送以换行结尾的命令 `HELLO VERSION MIN=3.0 MAX=3.1 \n`。这告诉 SAM 你想开始与该 API 通信，并且你会使用 SAM 3.0 和 3.1 版本进行交流。router 随后会返回类似 `HELLO REPLY RESULT=OK VERSION=3.1` 的内容，这是一段字符串，你可以将其传递给 Reply 构造函数以获取一个有效的 Reply 对象。从现在开始，我们可以使用 CommandSAM 函数和 Reply 对象来处理通过 SAM 网桥进行的所有通信。

最后，让我们为我们的 "HelloSAM" 函数添加一个测试。

```java
@Test public void testHelloSAM() {
    Jsam classUnderTest = new Jsam();
    assertTrue("HelloSAM should return 'true' in the presence of an alive SAM bridge", classUnderTest.HelloSAM());
}
```
### 向 SAM 发送命令

既然你已经与 SAM 协商好了连接，并就双方都能使用的 SAM 版本达成一致，你就可以为你的应用程序建立点对点连接，使其连接到其他 I2P 应用程序。你可以通过向 SAM Bridge 发送 "SESSION CREATE" 命令来完成此操作。为此，我们将使用一个 CreateSession 函数，它接受一个会话 ID 和一个目标类型参数。

```java
public String CreateSession(String id, String destination ) {
    if (destination == "") {
        destination = "TRANSIENT";
    }
    Reply repl = CommandSAM("SESSION CREATE STYLE=STREAM ID=" + ID + " DESTINATION=" + destination);
    if (repl.result == Reply.REPLY_TYPES.OK) {
        return id;
    }
    return "";
}
```
很简单，对吧？我们要做的只是把在 HelloSAM 函数中使用的模式套用到 `SESSION CREATE` 命令上。来自 SAM bridge（SAM 网桥）的成功回复仍然会返回 OK，在这种情况下我们返回新创建的 SAM 连接的 ID。否则，我们返回空字符串，因为那本来就是无效的 ID，而且它失败了，这样也便于检查。让我们通过为它编写一个测试来看看这个函数是否有效：

```java
@Test public void testCreateSession() {
    Jsam classUnderTest = new Jsam();
    assertTrue("HelloSAM should return 'true' in the presence of an alive SAM bridge", classUnderTest.HelloSAM());
    assertEquals("test", classUnderTest.CreateSession("test", ""));
}
```
请注意，在此测试中，我们*必须*先调用 HelloSAM，才能在启动我们的会话之前与 SAM 建立通信。否则，SAM 桥接器将返回错误，测试将失败。

### 解析应答并创建一个 Reply 对象。

现在你的会话已建立，并且已有本地 destination（目标标识），接下来需要决定如何使用它们。现在你可以指示会话通过 I2P 连接到远程服务，或者让它等待传入连接以便响应。不过，在你连接到远程 destination 之前，可能需要获取该 destination 的 base64，这是 API 所期望的格式。为此，我们将创建一个 LookupName 函数，它会以可用的形式返回该 destination 的 base64。

```java
public String LookupName(String name) {
    String cmd = "NAMING LOOKUP NAME=" + name + "\n";
    Reply repl = CommandSAM(cmd);
    if (repl.result == Reply.REPLY_TYPES.OK) {
        System.out.println(repl.replyMap.get("VALUE"));
        return repl.replyMap.get("VALUE");
    }
    return "";
}
```
同样，这与我们的 HelloSAM 和 CreateSession 函数几乎相同，只是有一个不同点。由于我们要专门查找 VALUE，且 NAME 字段将与 `name` 参数相同，因此它仅返回所请求的 Destination（目标标识）的 base64 字符串。

现在我们已经有了 LookupName 函数，让我们来测试一下：

```java
@Test public void testLookupName() {
    Jsam classUnderTest = new Jsam();
    assertTrue("HelloSAM should return 'true' in the presence of an alive SAM bridge", classUnderTest.HelloSAM());
    assertEquals("8ZAW~KzGFMUEj0pdchy6GQOOZbuzbqpWtiApEj8LHy2~O~58XKxRrA43cA23a9oDpNZDqWhRWEtehSnX5NoCwJcXWWdO1ksKEUim6cQLP-VpQyuZTIIqwSADwgoe6ikxZG0NGvy5FijgxF4EW9zg39nhUNKRejYNHhOBZKIX38qYyXoB8XCVJybKg89aMMPsCT884F0CLBKbHeYhpYGmhE4YW~aV21c5pebivvxeJPWuTBAOmYxAIgJE3fFU-fucQn9YyGUFa8F3t-0Vco-9qVNSEWfgrdXOdKT6orr3sfssiKo3ybRWdTpxycZ6wB4qHWgTSU5A-gOA3ACTCMZBsASN3W5cz6GRZCspQ0HNu~R~nJ8V06Mmw~iVYOu5lDvipmG6-dJky6XRxCedczxMM1GWFoieQ8Ysfuxq-j8keEtaYmyUQme6TcviCEvQsxyVirr~dTC-F8aZ~y2AlG5IJz5KD02nO6TRkI2fgjHhv9OZ9nskh-I2jxAzFP6Is1kyAAAA", classUnderTest.LookupName("i2p-projekt.i2p"));
}
```
### 向 SAM 发送 "HELLO"

终于，我们要用新的库与另一个服务建立连接。这一部分起初让我有些困惑，不过最敏锐的 Java 开发者可能已经在疑惑：为什么我们没有让 Jsam 类去继承 socket 类，而是在 Jsam 类内部创建了一个 Socket 变量？这是因为到目前为止，我们一直在通过 "Control Socket" 进行通信，而要进行真正的通信，我们需要创建一个新的 socket。因此我们一直等到现在，才让 Jsam 类去继承 Socket 类：

```java
public class Jsam extends Socket {
```
另外，让我们修改 startConnection 函数，这样我们就可以用它把连接从控制套接字切换到应用程序将使用的套接字。它现在将接收一个 Socket（套接字）参数。

```java
public void startConnection(Socket socket) {
    try {
        socket.connect(new InetSocketAddress(SAMHost, SAMPort), 600 );
    } catch (Exception e) {
        System.out.println(e);
    }
    try {
        writer = new PrintWriter(socket.getOutputStream(), true);
    } catch (Exception e) {
        System.out.println(e);
    }
    try {
        reader = new BufferedReader(new InputStreamReader(socket.getInputStream()));
    } catch (Exception e) {
        System.out.println(e);
    }
}
```
这使我们能够快速而轻松地打开一个新的套接字用于通信、再次执行"Hello SAM"握手，并建立流连接。

```java
public String ConnectSession(String id, String destination) {
    startConnection(this);
    HelloSAM();
    if (destination.endsWith(".i2p")) {
        destination = LookupName(destination);
    }
    String cmd = "STREAM CONNECT ID=" + id + " DESTINATION=" + destination + " SILENT=false";
    Reply repl = CommandSAM(cmd);
    if (repl.result == Reply.REPLY_TYPES.OK) {
        System.out.println(repl.String());
        return id;
    }
    System.out.println(repl.String());
    return "";
}
```
现在你已经有了一个用于通过 SAM 通信的新套接字了！我们也来为接受远程连接做同样的事情：

```java
public String AcceptSession(String id) {
    startConnection(this);
    HelloSAM();
    String cmd = "STREAM ACCEPT ID=" + id  + " SILENT=false";
    Reply repl = CommandSAM(cmd);
    if (repl.result == Reply.REPLY_TYPES.OK) {
        System.out.println(repl.String());
        return id;
    }
    System.out.println(repl.String());
    return "";
}
```
就这样。这就是如何一步一步构建一个 SAM 库。以后我会把这篇内容与该库的可用版本 Jsam 以及 SAM v3 规范进行交叉对照，不过现在我得先去处理其他一些事情。
