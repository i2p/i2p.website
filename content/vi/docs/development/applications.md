---
title: "Phát triển Ứng dụng"
description: "Tại sao viết ứng dụng chuyên dành cho I2P, các khái niệm chính, tùy chọn phát triển và hướng dẫn bắt đầu"
slug: "applications"
aliases:
  - "/vi/docs/develop/applications"
  - "/vi/docs/develop/applications/"
  - "/vi/applications"
  - "/vi/applications/"
lastUpdated: "2013-05"
accurateFor: "0.9.6"
---

## Tại sao viết mã cụ thể cho I2P?

Có nhiều cách để sử dụng các ứng dụng trong I2P. Sử dụng [I2PTunnel](/docs/api/i2ptunnel/), bạn có thể sử dụng các ứng dụng thông thường mà không cần lập trình hỗ trợ I2P một cách rõ ràng. Điều này rất hiệu quả cho các tình huống client-server, khi bạn cần kết nối đến một trang web duy nhất. Bạn có thể đơn giản tạo một tunnel bằng I2PTunnel để kết nối đến trang web đó, như được thể hiện trong Hình 1.

Nếu ứng dụng của bạn được phân tán, nó sẽ cần kết nối đến một số lượng lớn các peer. Sử dụng I2PTunnel, bạn sẽ cần tạo một tunnel mới cho mỗi peer mà bạn muốn liên hệ, như được thể hiện trong Hình 2. Quá trình này tất nhiên có thể được tự động hóa, nhưng chạy nhiều phiên bản I2PTunnel sẽ tạo ra một lượng lớn chi phí phụ trội. Ngoài ra, với nhiều giao thức bạn sẽ cần buộc tất cả mọi người sử dụng cùng một bộ cổng cho tất cả các peer — ví dụ: nếu bạn muốn chạy DCC chat một cách đáng tin cậy, tất cả mọi người cần đồng ý rằng cổng 10001 là Alice, cổng 10002 là Bob, cổng 10003 là Charlie, và cứ thế tiếp tục, vì giao thức bao gồm thông tin cụ thể của TCP/IP (host và port).

Các ứng dụng mạng thông thường thường gửi rất nhiều dữ liệu bổ sung có thể được sử dụng để xác định người dùng. Tên máy chủ, số cổng, múi giờ, bộ ký tự, v.v. thường được gửi mà không thông báo cho người dùng. Do đó, việc thiết kế giao thức mạng đặc biệt với mục tiêu ẩn danh có thể tránh làm lộ danh tính người dùng.

Cũng có những cân nhắc về hiệu suất cần xem xét khi quyết định cách tương tác trên I2P. Thư viện streaming và các thứ được xây dựng trên đó hoạt động với các handshake tương tự TCP, trong khi các giao thức I2P cốt lõi (I2NP và I2CP) hoàn toàn dựa trên tin nhắn (giống như UDP hoặc trong một số trường hợp là raw IP). Điểm khác biệt quan trọng là với I2P, việc giao tiếp đang hoạt động trên một mạng dài và béo — mỗi tin nhắn end-to-end sẽ có độ trễ không nhỏ, nhưng có thể chứa payload lên đến vài KB. Một ứng dụng chỉ cần một request và response đơn giản có thể loại bỏ mọi trạng thái và giảm độ trễ phát sinh từ các handshake khởi động và kết thúc bằng cách sử dụng datagram (cố gắng tối đa) mà không cần phải lo lắng về việc phát hiện MTU hoặc phân mảnh tin nhắn.

![Tạo kết nối server-client sử dụng I2PTunnel chỉ cần tạo một tunnel duy nhất.](/images/i2ptunnel_serverclient.png)

*Hình 1: Tạo kết nối server-client bằng I2PTunnel chỉ cần tạo một tunnel duy nhất.*

![Thiết lập kết nối cho các ứng dụng ngang hàng đòi hỏi một lượng rất lớn tunnel.](/images/i2ptunnel_peertopeer.png)

*Hình 2: Thiết lập kết nối cho các ứng dụng ngang hàng yêu cầu một số lượng rất lớn tunnel.*

Tóm lại, có một số lý do để viết code chuyên dụng cho I2P:

- Tạo ra một lượng lớn các I2PTunnel instance tiêu tốn một lượng tài nguyên đáng kể, điều này gây vấn đề cho các ứng dụng phân tán (cần một tunnel mới cho mỗi peer).
- Các giao thức mạng thông thường thường gửi rất nhiều dữ liệu bổ sung có thể được sử dụng để nhận diện người dùng. Lập trình chuyên biệt cho I2P cho phép tạo ra giao thức mạng không làm rò rỉ thông tin như vậy, giữ cho người dùng ẩn danh và an toàn.
- Các giao thức mạng được thiết kế để sử dụng trên internet thông thường có thể không hiệu quả trên I2P, một mạng có độ trễ cao hơn nhiều.

I2P hỗ trợ một [giao diện plugin tiêu chuẩn](/docs/specs/plugin/) cho các nhà phát triển để các ứng dụng có thể được tích hợp và phân phối dễ dàng.

Các ứng dụng được viết bằng Java và có thể truy cập/chạy được bằng giao diện HTML thông qua webapps/app.war chuẩn có thể được xem xét để đưa vào bản phân phối I2P.

---

## Các Khái Niệm Quan Trọng

Có một vài thay đổi cần phải thích nghi khi sử dụng I2P:

### Destination ~= host+port

Một ứng dụng chạy trên I2P gửi tin nhắn từ và nhận tin nhắn đến một điểm cuối duy nhất được bảo mật bằng mật mã — một "destination". Theo thuật ngữ TCP hoặc UDP, một destination có thể (phần lớn) được coi là tương đương với một cặp tên máy chủ cộng với số cổng, mặc dù có một vài điểm khác biệt.

- Một I2P destination bản thân nó là một cấu trúc mật mã — tất cả dữ liệu được gửi đến nó đều được mã hóa như thể có sự triển khai toàn cầu của IPsec với vị trí (được ẩn danh) của điểm cuối được ký như thể có sự triển khai toàn cầu của DNSSEC.
- I2P destination là các định danh di động — chúng có thể được chuyển từ router I2P này sang router khác (hoặc thậm chí có thể "multihome" — hoạt động trên nhiều router cùng lúc). Điều này khá khác biệt so với thế giới TCP hoặc UDP nơi một điểm cuối duy nhất (port) phải ở trên một host duy nhất.
- I2P destination rất xấu và lớn — đằng sau hậu trường, chúng chứa một khóa công khai ElGamal 2048 bit để mã hóa, một khóa công khai DSA 1024 bit để ký, và một certificate có kích thước biến đổi, có thể chứa proof of work hoặc dữ liệu bị che mờ.

Đã có những cách hiện tại để tham chiếu đến các destination lớn và xấu xí này bằng các tên ngắn và đẹp (ví dụ: "irc.duck.i2p"), nhưng những kỹ thuật đó không đảm bảo tính duy nhất toàn cầu (vì chúng được lưu trữ cục bộ trong cơ sở dữ liệu trên máy của mỗi người) và cơ chế hiện tại không đặc biệt có khả năng mở rộng cũng như không an toàn (các cập nhật cho danh sách host được quản lý bằng cách sử dụng "subscription" đến các dịch vụ đặt tên). Có thể một ngày nào đó sẽ có hệ thống đặt tên an toàn, có thể đọc được bởi con người, có khả năng mở rộng và duy nhất toàn cầu, nhưng các ứng dụng không nên phụ thuộc vào việc nó được triển khai, vì có những người không nghĩ rằng một thứ như vậy là khả thi. [Thông tin chi tiết về hệ thống đặt tên](/docs/overview/naming/) có sẵn.

Mặc dù hầu hết các ứng dụng không cần phân biệt giao thức và cổng, I2P *có* hỗ trợ chúng. Các ứng dụng phức tạp có thể chỉ định một giao thức, từ cổng, và đến cổng, trên cơ sở từng thông điệp, để ghép kênh lưu lượng trên một đích đến duy nhất. Xem [trang datagram](/docs/api/datagrams/) để biết chi tiết. Các ứng dụng đơn giản hoạt động bằng cách lắng nghe "tất cả giao thức" trên "tất cả cổng" của một đích đến.

### Ẩn danh và Bảo mật

I2P có mã hóa và xác thực end-to-end minh bạch cho tất cả dữ liệu được truyền qua mạng — nếu Bob gửi đến destination của Alice, chỉ có destination của Alice mới có thể nhận được, và nếu Bob đang sử dụng thư viện datagrams hoặc streaming, Alice biết chắc chắn rằng destination của Bob là người đã gửi dữ liệu.

Tất nhiên, I2P ẩn danh một cách minh bạch dữ liệu được gửi giữa Alice và Bob, nhưng nó không làm gì để ẩn danh nội dung của những gì họ gửi. Ví dụ, nếu Alice gửi cho Bob một biểu mẫu có tên đầy đủ, giấy tờ tùy thân của chính phủ và số thẻ tín dụng của cô ấy, thì I2P không thể làm gì được. Do đó, các giao thức và ứng dụng nên lưu ý thông tin nào họ đang cố gắng bảo vệ và thông tin nào họ sẵn sàng tiết lộ.

### I2P Datagram Có Thể Lên Đến Vài KB

Các ứng dụng sử dụng datagram I2P (dù là dạng thô hay có thể trả lời) về cơ bản có thể được hiểu theo kiểu UDP — các datagram không có thứ tự, cố gắng tối đa, và không kết nối — nhưng khác với UDP, các ứng dụng không cần lo lắng về việc phát hiện MTU và có thể đơn giản gửi các datagram lớn. Mặc dù giới hạn trên danh nghĩa là 32 KB, thông điệp sẽ được phân mảnh để truyền tải, do đó làm giảm độ tin cậy của toàn bộ. Các datagram trên khoảng 10 KB hiện tại không được khuyến nghị. Xem [trang datagram](/docs/api/datagrams/) để biết chi tiết. Đối với nhiều ứng dụng, 10 KB dữ liệu là đủ cho toàn bộ một yêu cầu hoặc phản hồi, cho phép chúng hoạt động minh bạch trong I2P như một ứng dụng giống UDP mà không cần phải viết phân mảnh, gửi lại, v.v.

---

## Tùy chọn Phát triển

Có nhiều cách để gửi dữ liệu qua I2P, mỗi cách đều có những ưu và nhược điểm riêng. Streaming lib là giao diện được khuyến nghị, được sử dụng bởi phần lớn các ứng dụng I2P.

### Thư viện Streaming

[Thư viện streaming đầy đủ](/docs/api/streaming/) hiện là giao diện tiêu chuẩn. Nó cho phép lập trình sử dụng socket giống TCP, như được giải thích trong [Hướng dẫn phát triển Streaming](#developing-with-the-streaming-library).

### BOB

BOB là [Basic Open Bridge](/docs/legacy/bob/), cho phép một ứng dụng bằng bất kỳ ngôn ngữ nào tạo các kết nối streaming đến và từ I2P. Tại thời điểm này nó thiếu hỗ trợ UDP, nhưng hỗ trợ UDP được lên kế hoạch trong tương lai gần. BOB cũng chứa một số công cụ, chẳng hạn như tạo khóa đích, và xác minh rằng một địa chỉ tuân thủ các đặc tả I2P. Thông tin cập nhật và các ứng dụng sử dụng BOB có thể được tìm thấy tại [I2P Site](http://bob.i2p/) này.

### SAM, SAM V2, SAM V3

*SAM không được khuyến nghị. SAM V2 là tạm được, SAMv3 được khuyến nghị.*

SAM là giao thức [Simple Anonymous Messaging](/docs/legacy/sam/) (Nhắn tin Ẩn danh Đơn giản), cho phép một ứng dụng được viết bằng bất kỳ ngôn ngữ nào giao tiếp với một cầu nối SAM thông qua socket TCP thông thường và để cầu nối đó ghép kênh tất cả lưu lượng I2P của nó, phối hợp một cách minh bạch việc mã hóa/giải mã và xử lý dựa trên sự kiện. SAM hỗ trợ ba kiểu hoạt động:

- streams, cho khi Alice và Bob muốn gửi dữ liệu cho nhau một cách đáng tin cậy và theo thứ tự
- repliable datagrams, cho khi Alice muốn gửi cho Bob một tin nhắn mà Bob có thể trả lời
- raw datagrams, cho khi Alice muốn tận dụng tối đa băng thông và hiệu suất có thể, và Bob không quan tâm liệu người gửi dữ liệu có được xác thực hay không (ví dụ: dữ liệu được truyền có thể tự xác thực)

SAM V3 hướng đến cùng mục tiêu với SAM và SAM V2, nhưng không yêu cầu multiplexing/demultiplexing. Mỗi I2P stream được xử lý bởi socket riêng của nó giữa ứng dụng và SAM bridge. Bên cạnh đó, datagram có thể được gửi và nhận bởi ứng dụng thông qua giao tiếp datagram với SAM bridge.

[SAM V2](/docs/legacy/samv2/) là một phiên bản mới được sử dụng bởi imule nhằm khắc phục một số vấn đề trong [SAM](/docs/legacy/sam/).

[SAM V3](/docs/api/samv3/) được sử dụng bởi imule từ phiên bản 1.4.0.

### I2PTunnel

Ứng dụng I2PTunnel cho phép các ứng dụng xây dựng các tunnel TCP-like cụ thể tới các peer bằng cách tạo ra các ứng dụng I2PTunnel 'client' (lắng nghe trên một cổng cụ thể và kết nối tới một destination I2P cụ thể bất cứ khi nào có socket mở tới cổng đó) hoặc các ứng dụng I2PTunnel 'server' (lắng nghe tới một destination I2P cụ thể và bất cứ khi nào nhận được kết nối I2P mới thì outproxy tới một TCP host/port cụ thể). Các luồng này là 8-bit clean và được xác thực cũng như bảo mật thông qua cùng thư viện streaming mà SAM sử dụng, nhưng có chi phí đáng kể khi tạo nhiều instance I2PTunnel duy nhất, vì mỗi instance có destination I2P riêng và bộ tunnel, key riêng, v.v.

### SOCKS

I2P hỗ trợ proxy SOCKS V4 và V5. Các kết nối đi ra hoạt động tốt. Chức năng đến (server) và UDP có thể chưa hoàn thiện và chưa được kiểm tra.

### Ministreaming

*Đã xóa*

Trước đây đã từng có một thư viện "ministreaming" đơn giản, nhưng hiện tại ministreaming.jar chỉ chứa các interface cho thư viện streaming đầy đủ.

### Datagrams

*Được khuyên dùng cho các ứng dụng kiểu UDP*

Thư viện [Datagram](/docs/api/datagrams/) cho phép gửi các gói tin giống UDP. Có thể sử dụng:

- Repliable datagrams (gói dữ liệu có thể phản hồi)
- Raw datagrams (gói dữ liệu thô)

### I2CP

*Không được khuyến nghị*

[I2CP](/docs/specs/i2cp/) bản thân là một giao thức độc lập với ngôn ngữ, nhưng để triển khai một thư viện I2CP bằng ngôn ngữ khác ngoài Java thì cần phải viết một lượng code đáng kể (các thủ tục mã hóa, marshalling đối tượng, xử lý tin nhắn bất đồng bộ, v.v.). Mặc dù có thể viết một thư viện I2CP bằng C hoặc ngôn ngữ khác, nhưng có lẽ sẽ hữu ích hơn nếu sử dụng thư viện SAM bằng C thay thế.

### Ứng dụng Web

I2P đi kèm với webserver Jetty, và việc cấu hình để sử dụng máy chủ Apache thay thế rất đơn giản. Bất kỳ công nghệ ứng dụng web tiêu chuẩn nào cũng sẽ hoạt động.

---

## Bắt Đầu Phát Triển — Hướng Dẫn Đơn Giản

Phát triển ứng dụng sử dụng I2P yêu cầu có một bản cài đặt I2P hoạt động và môi trường phát triển do bạn lựa chọn. Nếu bạn đang sử dụng Java, bạn có thể bắt đầu phát triển với [thư viện streaming](#developing-with-the-streaming-library) hoặc thư viện datagram. Khi sử dụng ngôn ngữ lập trình khác, có thể sử dụng SAM hoặc BOB.

### Phát triển với Thư viện Streaming

Ví dụ sau đây cho thấy cách tạo các ứng dụng client và server giống TCP bằng cách sử dụng thư viện streaming.

Điều này sẽ yêu cầu các thư viện sau trong classpath của bạn:

- `$I2P/lib/streaming.jar`: Thư viện streaming chính
- `$I2P/lib/mstreaming.jar`: Factory và interfaces cho thư viện streaming
- `$I2P/lib/i2p.jar`: Các lớp I2P chuẩn, cấu trúc dữ liệu, API và tiện ích

Bạn có thể lấy chúng từ một bản cài đặt I2P, hoặc thêm các dependency sau từ Maven Central:

- `net.i2p:i2p`
- `net.i2p.client:streaming`

Giao tiếp mạng yêu cầu sử dụng network socket của I2P. Để minh họa điều này, chúng ta sẽ tạo một ứng dụng trong đó một client có thể gửi tin nhắn văn bản đến server, server sẽ in các tin nhắn và gửi lại cho client. Nói cách khác, server sẽ hoạt động như một echo.

Chúng ta sẽ bắt đầu bằng việc khởi tạo ứng dụng server. Điều này yêu cầu lấy một I2PSocketManager và tạo một I2PServerSocket. Chúng ta sẽ không cung cấp cho I2PSocketManagerFactory các khóa đã lưu cho một Destination hiện có, vì vậy nó sẽ tạo một Destination mới cho chúng ta. Do đó chúng ta sẽ yêu cầu I2PSocketManager cung cấp một I2PSession, để có thể tìm ra Destination đã được tạo, vì chúng ta sẽ cần sao chép và dán thông tin đó sau này để client có thể kết nối với chúng ta.

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
*Ví dụ mã 1: khởi tạo ứng dụng máy chủ.*

Khi đã có I2PServerSocket, chúng ta có thể tạo các instance I2PSocket để chấp nhận kết nối từ client. Trong ví dụ này, chúng ta sẽ tạo một instance I2PSocket duy nhất, chỉ có thể xử lý một client tại một thời điểm. Một server thực tế sẽ phải có khả năng xử lý nhiều client. Để làm điều này, nhiều instance I2PSocket sẽ phải được tạo, mỗi instance trong các thread riêng biệt. Khi đã tạo xong instance I2PSocket, chúng ta đọc dữ liệu, in ra và gửi lại cho client.

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
*Ví dụ mã 2: chấp nhận kết nối từ client và xử lý tin nhắn.*

Khi bạn chạy đoạn mã server ở trên, nó sẽ in ra một cái gì đó như thế này (nhưng không có xuống dòng, nó chỉ là một khối ký tự khổng lồ):

```
y17s~L3H9q5xuIyyynyWahAuj6Jeg5VC~Klu9YPquQvD4vlgzmxn4yy~5Z0zVvKJiS2Lk
poPIcB3r9EbFYkz1mzzE3RYY~XFyPTaFQY8omDv49nltI2VCQ5cx7gAt~y4LdWqkyk3au
...
```
Đây là biểu diễn base64 của Destination máy chủ. Client sẽ cần chuỗi này để kết nối đến máy chủ.

Bây giờ, chúng ta sẽ tạo ứng dụng client. Một lần nữa, cần thực hiện một số bước để khởi tạo. Một lần nữa, chúng ta sẽ cần bắt đầu bằng việc lấy một I2PSocketManager. Lần này chúng ta sẽ không sử dụng I2PSession và I2PServerSocket. Thay vào đó, chúng ta sẽ sử dụng chuỗi Destination của server để bắt đầu kết nối. Chúng ta sẽ yêu cầu người dùng nhập chuỗi Destination, và tạo một I2PSocket bằng chuỗi này. Một khi đã có I2PSocket, chúng ta có thể bắt đầu gửi và nhận dữ liệu đến và từ server.

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
*Ví dụ mã 3: khởi động client và kết nối đến ứng dụng server.*

Cuối cùng, bạn có thể chạy cả ứng dụng server và client. Đầu tiên, khởi động ứng dụng server. Nó sẽ in ra một chuỗi Destination (như đã hiển thị ở trên). Tiếp theo, khởi động ứng dụng client. Khi nó yêu cầu một chuỗi Destination, bạn có thể nhập chuỗi mà server đã in ra. Client sau đó sẽ gửi 'Hello I2P!' (cùng với một dòng mới) đến server, server sẽ in thông điệp và gửi nó trở lại cho client.

Chúc mừng, bạn đã giao tiếp thành công qua I2P!

---

## Các Ứng dụng Hiện có

Liên hệ với chúng tôi nếu bạn muốn đóng góp.

- [I2P-Bote](http://i2pbote.i2p/) - liên hệ HungryHobo
- [Syndie](http://syndie.i2p2.de/)
- [IMule](http://www.imule.i2p/)
- [I2Phex](http://forum.i2p/viewforum.php?f=25)

Xem thêm tất cả các plugin trên [plugins.i2p](http://plugins.i2p/), các ứng dụng và mã nguồn được liệt kê trên [echelon.i2p](http://echelon.i2p/), và mã ứng dụng được lưu trữ trên [git.repo.i2p](http://git.repo.i2p/).

Xem thêm các ứng dụng đi kèm trong bản phân phối I2P - SusiMail và I2PSnark.

---

## Ý Tưởng Ứng Dụng

- Máy chủ NNTP - đã có một số trong quá khứ, hiện tại chưa có
- Máy chủ Jabber - đã có một số trong quá khứ, và hiện tại có một máy chủ, với quyền truy cập vào internet công cộng
- Máy chủ khóa PGP và/hoặc proxy
- Ứng dụng phân phối nội dung / DHT - hồi sinh feedspace, chuyển đổi dijjer, tìm kiếm các giải pháp thay thế
- Hỗ trợ phát triển [Syndie](http://syndie.i2p2.de/)
- Ứng dụng dựa trên web - Không giới hạn cho việc lưu trữ các ứng dụng dựa trên máy chủ web như blog, pastebin, lưu trữ, theo dõi, nguồn cấp dữ liệu, v.v. Bất kỳ công nghệ web hoặc CGI nào như Perl, PHP, Python, hoặc Ruby đều có thể hoạt động.
- Hồi sinh một số ứng dụng cũ, một số trước đây có trong gói nguồn i2p - bogobot, pants, proxyscript, q, stasher, socks proxy, i2ping, feedspace
