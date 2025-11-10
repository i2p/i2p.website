---
title: "Vậy bạn muốn viết một thư viện SAM"
date: 2019-06-23
author: "idk"
description: "Hướng dẫn dành cho người mới bắt đầu viết thư viện SAM!"
---

*Hoặc, giao tiếp với [i2p](https://geti2p.net) dành cho những người chưa quen lắm với việc đọc đặc tả*

Theo quan điểm của tôi, một trong những tính năng tốt nhất của I2P là SAM API (giao diện lập trình ứng dụng SAM), có thể được dùng để xây dựng một cầu nối giữa I2P và ứng dụng hoặc ngôn ngữ mà bạn chọn. Hiện nay, có hàng chục thư viện SAM dành cho nhiều ngôn ngữ khác nhau, bao gồm:

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

Nếu bạn đang sử dụng bất kỳ ngôn ngữ nào trong số này, bạn có thể chuyển ứng dụng của mình sang I2P ngay bằng cách dùng một thư viện hiện có. Tuy nhiên, đó không phải là điều mà hướng dẫn này đề cập. Hướng dẫn này nói về việc cần làm nếu bạn muốn tạo một thư viện SAM bằng một ngôn ngữ mới. Trong hướng dẫn này, tôi sẽ triển khai một thư viện SAM mới bằng Java. Tôi chọn Java vì hiện chưa có thư viện Java nào kết nối bạn với SAM, vì Java được sử dụng trên Android, và vì đó là một ngôn ngữ mà hầu như ai cũng có ít nhất *một chút* kinh nghiệm, nên hy vọng bạn có thể chuyển nó sang ngôn ngữ mình lựa chọn.

## Tạo thư viện của bạn

Cách bạn thiết lập thư viện riêng của mình sẽ khác nhau tùy theo ngôn ngữ bạn muốn sử dụng. Trong ví dụ thư viện này, chúng ta sẽ dùng Java để có thể tạo một thư viện như sau:

```sh
mkdir jsam
cd jsam
gradle init --type java-library
```
Hoặc, nếu bạn đang sử dụng gradle 5 trở lên:

```sh
gradle init --type java-library --project-name jsam
```
## Thiết lập thư viện

Có một vài dữ liệu mà gần như bất kỳ thư viện SAM nào cũng nên quản lý. Ít nhất, thư viện đó sẽ cần lưu trữ địa chỉ của SAM Bridge (cầu nối SAM) mà bạn dự định sử dụng và kiểu chữ ký bạn muốn dùng.

### Storing the SAM address

Tôi thích lưu trữ địa chỉ SAM dưới dạng một String và một Integer, rồi kết hợp lại chúng trong một hàm khi chương trình chạy.

```java
public String SAMHost = "127.0.0.1";
public int SAMPort = 7656;
public String SAMAddress(){
    return SAMHost + ":" + SAMPort;
}
```
### Storing the Signature Type

Các kiểu chữ ký hợp lệ cho một I2P Tunnel là DSA_SHA1, ECDSA_SHA256_P256, ECDSA_SHA384_P384, ECDSA_SHA512_P521, EdDSA_SHA512_Ed25519, nhưng khuyến nghị mạnh mẽ bạn sử dụng EdDSA_SHA512_Ed25519 làm mặc định nếu bạn triển khai ít nhất SAM 3.1. Trong Java, cấu trúc dữ liệu 'enum' rất phù hợp cho nhiệm vụ này, vì nó được thiết kế để chứa một nhóm hằng số. Thêm enum và một instance (thể hiện) của enum vào định nghĩa lớp Java của bạn.

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
### Lưu trữ địa chỉ SAM

Điều đó đảm bảo việc lưu trữ đáng tin cậy kiểu chữ ký đang được sử dụng bởi kết nối SAM, nhưng bạn vẫn cần truy xuất nó dưới dạng chuỗi để gửi nó tới cầu nối.

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
Việc kiểm thử là quan trọng, vậy hãy viết vài bài kiểm thử:

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
Sau khi hoàn tất, hãy bắt đầu tạo hàm khởi tạo của bạn. Lưu ý rằng chúng tôi đã thiết lập các giá trị mặc định cho thư viện của mình, những giá trị này sẽ hữu ích trong các trường hợp mặc định trên tất cả các router I2P hiện có cho đến nay.

```java
public Jsam(String host, int port, SIGNATURE_TYPE sig) {
    SAMHost = host;
    SAMPort = port;
    SigType = sig;
}
```
## Establishing a SAM Connection

Cuối cùng cũng đến phần hay. Việc tương tác với SAM bridge (cầu nối SAM) được thực hiện bằng cách gửi một "command" tới địa chỉ của SAM bridge, và bạn có thể phân tích cú pháp kết quả của lệnh đó dưới dạng một tập các cặp khóa-giá trị dựa trên chuỗi. Vì vậy, ghi nhớ điều đó, hãy thiết lập một kết nối đọc-ghi tới SAM Address (Địa chỉ SAM) mà chúng ta đã xác định trước đó, sau đó viết một hàm "CommandSAM" và một bộ phân tích phản hồi.

### Lưu trữ kiểu chữ ký

Chúng ta đang giao tiếp với SAM qua một socket, vì vậy để kết nối tới, đọc từ và ghi vào socket, bạn sẽ cần tạo các biến private sau đây trong lớp Jsam:

```java
private Socket socket;
private PrintWriter writer;
private BufferedReader reader;
```
Bạn cũng sẽ muốn khởi tạo các biến đó trong các hàm khởi tạo của mình bằng cách tạo một hàm để làm điều đó.

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
### Truy xuất loại chữ ký:

Bây giờ bạn đã thiết lập xong và cuối cùng có thể bắt đầu giao tiếp với SAM. Để mọi thứ được sắp xếp gọn gàng, hãy tạo một hàm gửi một lệnh duy nhất tới SAM, được kết thúc bằng ký tự xuống dòng, và trả về một đối tượng Reply, mà chúng ta sẽ tạo ở bước tiếp theo:

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
Lưu ý rằng chúng ta đang sử dụng writer và reader mà chúng ta đã tạo từ socket ở bước trước làm đầu vào và đầu ra cho socket. Khi nhận được phản hồi từ reader, chúng ta truyền chuỗi đó vào hàm khởi tạo Reply, hàm này sẽ phân tích cú pháp chuỗi và trả về đối tượng Reply.

### Parsing a reply and creating a Reply object.

Để xử lý phản hồi dễ dàng hơn, chúng ta sẽ sử dụng một đối tượng Reply để tự động phân tích cú pháp các kết quả mà chúng ta nhận được từ SAM bridge (cầu nối SAM). Một phản hồi có ít nhất một topic (chủ đề), một type (kiểu), và một result (kết quả), cũng như một số lượng bất kỳ các cặp khóa-giá trị.

```java
public class Reply {
    String topic;
    String type;
    REPLY_TYPES result;
    Map<String, String> replyMap = new HashMap<String, String>();
```
Như bạn thấy, chúng ta sẽ lưu trữ "result" dưới dạng một kiểu liệt kê (enum), REPLY_TYPES. Kiểu liệt kê này chứa tất cả các kết quả phản hồi mà SAM bridge có thể trả về.

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
Bây giờ hãy tạo hàm khởi tạo của chúng ta, hàm này nhận chuỗi phản hồi nhận từ socket làm tham số, phân tích nó và sử dụng thông tin để thiết lập đối tượng phản hồi. Phản hồi được phân tách bằng dấu cách, với các cặp khóa-giá trị được nối bằng dấu bằng và kết thúc bằng ký tự xuống dòng.

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
Cuối cùng, để tiện sử dụng, hãy thêm cho đối tượng Reply một hàm toString() trả về biểu diễn dạng chuỗi của đối tượng Reply.

```java
public String toString() {
    return topic + " " + type + " " + REPLY_TYPES.get(result) + " " + replyMap.toString();
}
}
```
### Kết nối tới cổng SAM

Bây giờ chúng ta đã sẵn sàng thiết lập giao tiếp với SAM bằng cách gửi một thông điệp "Hello". Nếu bạn đang viết một thư viện SAM mới, bạn có lẽ nên nhắm tới ít nhất SAM 3.1, vì nó có sẵn trong cả I2P và i2pd và bổ sung hỗ trợ cho tham số SIGNATURE_TYPE.

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
Như bạn có thể thấy, chúng tôi sử dụng hàm CommandSAM mà chúng tôi đã tạo trước đó để gửi lệnh kết thúc bằng ký tự xuống dòng `HELLO VERSION MIN=3.0 MAX=3.1 \n`. Điều này cho SAM biết rằng bạn muốn bắt đầu giao tiếp với API, và rằng bạn biết cách sử dụng SAM phiên bản 3.0 và 3.1. Đến lượt mình, router sẽ phản hồi bằng chuỗi như `HELLO REPLY RESULT=OK VERSION=3.1`, đây là một chuỗi mà bạn có thể truyền vào hàm khởi tạo Reply để nhận một đối tượng Reply hợp lệ. Từ bây giờ, chúng ta có thể dùng hàm CommandSAM và đối tượng Reply để xử lý mọi giao tiếp của chúng ta qua SAM bridge (cầu nối SAM).

Cuối cùng, hãy thêm một bài kiểm thử cho hàm "HelloSAM" của chúng ta.

```java
@Test public void testHelloSAM() {
    Jsam classUnderTest = new Jsam();
    assertTrue("HelloSAM should return 'true' in the presence of an alive SAM bridge", classUnderTest.HelloSAM());
}
```
### Gửi lệnh đến SAM

Bây giờ, sau khi bạn đã đàm phán kết nối với SAM và thống nhất về phiên bản SAM mà cả hai cùng hỗ trợ, bạn có thể thiết lập các kết nối ngang hàng (peer-to-peer) cho ứng dụng của mình để kết nối với các ứng dụng I2P khác. Bạn thực hiện điều này bằng cách gửi lệnh "SESSION CREATE" tới SAM Bridge. Để làm vậy, chúng ta sẽ dùng hàm CreateSession nhận vào một ID phiên và một tham số kiểu đích.

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
Dễ thôi, phải không? Tất cả những gì chúng ta cần làm là điều chỉnh mẫu mà chúng ta đã dùng trong hàm HelloSAM cho lệnh `SESSION CREATE`. Một phản hồi hợp lệ từ cầu nối vẫn sẽ trả về OK, và trong trường hợp đó, chúng ta trả về ID của kết nối SAM vừa được tạo. Còn nếu không, chúng ta trả về một chuỗi rỗng vì dù sao đó cũng là một ID không hợp lệ và thao tác đã thất bại, nên rất dễ kiểm tra. Hãy xem hàm này có hoạt động không bằng cách viết một bài kiểm thử cho nó:

```java
@Test public void testCreateSession() {
    Jsam classUnderTest = new Jsam();
    assertTrue("HelloSAM should return 'true' in the presence of an alive SAM bridge", classUnderTest.HelloSAM());
    assertEquals("test", classUnderTest.CreateSession("test", ""));
}
```
Lưu ý rằng trong bài kiểm thử này, chúng ta *phải* gọi HelloSAM trước để thiết lập liên lạc với SAM trước khi bắt đầu phiên. Nếu không, bridge (cầu nối) sẽ phản hồi bằng một lỗi và bài kiểm thử sẽ thất bại.

### Phân tích cú pháp một phản hồi và tạo một đối tượng Reply.

Bây giờ bạn đã thiết lập phiên và destination (đích trong I2P) cục bộ của mình, và cần quyết định sẽ làm gì với chúng. Bạn có thể điều khiển phiên để kết nối đến một dịch vụ từ xa qua I2P, hoặc chờ các kết nối đến để phản hồi. Tuy nhiên, trước khi có thể kết nối đến một destination từ xa, bạn có thể cần lấy base64 của destination, đây là thứ mà API yêu cầu. Để làm điều này, chúng ta sẽ tạo một hàm LookupName, hàm này sẽ trả về base64 ở dạng có thể sử dụng.

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
Một lần nữa, điều này gần như giống hệt các hàm HelloSAM và CreateSession của chúng ta, chỉ khác một điểm. Vì chúng ta đang tìm cụ thể VALUE và trường NAME sẽ trùng với đối số `name`, nên nó chỉ đơn giản trả về chuỗi base64 của đích được yêu cầu.

Bây giờ chúng ta đã có hàm LookupName, hãy kiểm thử nó:

```java
@Test public void testLookupName() {
    Jsam classUnderTest = new Jsam();
    assertTrue("HelloSAM should return 'true' in the presence of an alive SAM bridge", classUnderTest.HelloSAM());
    assertEquals("8ZAW~KzGFMUEj0pdchy6GQOOZbuzbqpWtiApEj8LHy2~O~58XKxRrA43cA23a9oDpNZDqWhRWEtehSnX5NoCwJcXWWdO1ksKEUim6cQLP-VpQyuZTIIqwSADwgoe6ikxZG0NGvy5FijgxF4EW9zg39nhUNKRejYNHhOBZKIX38qYyXoB8XCVJybKg89aMMPsCT884F0CLBKbHeYhpYGmhE4YW~aV21c5pebivvxeJPWuTBAOmYxAIgJE3fFU-fucQn9YyGUFa8F3t-0Vco-9qVNSEWfgrdXOdKT6orr3sfssiKo3ybRWdTpxycZ6wB4qHWgTSU5A-gOA3ACTCMZBsASN3W5cz6GRZCspQ0HNu~R~nJ8V06Mmw~iVYOu5lDvipmG6-dJky6XRxCedczxMM1GWFoieQ8Ysfuxq-j8keEtaYmyUQme6TcviCEvQsxyVirr~dTC-F8aZ~y2AlG5IJz5KD02nO6TRkI2fgjHhv9OZ9nskh-I2jxAzFP6Is1kyAAAA", classUnderTest.LookupName("i2p-projekt.i2p"));
}
```
### Nói "HELLO" với SAM

Cuối cùng, chúng ta sẽ thiết lập kết nối tới một dịch vụ khác bằng thư viện mới của mình. Phần này ban đầu khiến tôi hơi bối rối, nhưng các lập trình viên Java tinh ý có lẽ đã tự hỏi vì sao chúng ta không kế thừa lớp Socket thay vì tạo một biến Socket bên trong lớp Jsam. Đó là bởi cho đến lúc này, chúng ta mới chỉ giao tiếp với "Control Socket" và cần tạo một Socket mới để thực hiện giao tiếp thực sự. Vì vậy, chúng ta đã chờ đến bây giờ mới cho lớp Jsam kế thừa lớp Socket:

```java
public class Jsam extends Socket {
```
Ngoài ra, hãy sửa đổi hàm startConnection của chúng ta để có thể dùng nó để chuyển từ socket điều khiển sang socket mà chúng ta sẽ sử dụng trong ứng dụng. Giờ đây nó sẽ nhận một đối số kiểu Socket.

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
Điều này cho phép chúng ta nhanh chóng và dễ dàng mở một socket mới để giao tiếp qua đó, thực hiện lại thủ tục bắt tay "Hello SAM", và kết nối luồng.

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
Và bây giờ bạn đã có một Socket mới để giao tiếp qua SAM! Hãy làm điều tương tự cho việc chấp nhận kết nối từ xa:

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
Vậy là xong. Đó là cách bạn xây dựng một thư viện SAM, từng bước một. Trong tương lai, tôi sẽ đối chiếu nội dung này với phiên bản thư viện đang hoạt động, Jsam, và đặc tả SAM v3, nhưng hiện tại tôi còn phải làm một số việc khác.
