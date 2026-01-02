---
title: "Phát triển Ứng dụng"
description: "Tại sao nên viết ứng dụng dành riêng cho I2P, các khái niệm chính, tùy chọn phát triển và hướng dẫn bắt đầu đơn giản"
slug: "applications"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
---

## Tại sao cần viết mã lệnh chuyên biệt cho I2P?

Có nhiều cách để sử dụng các ứng dụng trong I2P. Sử dụng [I2PTunnel](/docs/api/i2ptunnel/), bạn có thể dùng các ứng dụng thông thường mà không cần lập trình hỗ trợ I2P một cách tường minh. Cách này rất hiệu quả cho các tình huống client-server, khi bạn cần kết nối đến một trang web duy nhất. Bạn chỉ cần tạo một tunnel bằng I2PTunnel để kết nối đến trang web đó, như được minh họa trong Hình 1.

Nếu ứng dụng của bạn được phân tán, nó sẽ yêu cầu kết nối đến một lượng lớn các peer. Khi sử dụng I2PTunnel, bạn sẽ cần tạo một tunnel mới cho mỗi peer mà bạn muốn liên hệ, như được hiển thị trong Hình 2. Quá trình này tất nhiên có thể được tự động hóa, nhưng việc chạy nhiều phiên bản I2PTunnel tạo ra một lượng lớn chi phí hoạt động. Ngoài ra, với nhiều giao thức, bạn sẽ cần buộc mọi người sử dụng cùng một tập hợp các cổng cho tất cả các peer — ví dụ: nếu bạn muốn chạy DCC chat một cách đáng tin cậy, mọi người cần thống nhất rằng cổng 10001 là Alice, cổng 10002 là Bob, cổng 10003 là Charlie, v.v., vì giao thức bao gồm thông tin cụ thể của TCP/IP (host và port).

Các ứng dụng mạng thông thường thường gửi rất nhiều dữ liệu bổ sung có thể được sử dụng để xác định người dùng. Tên máy chủ, số cổng, múi giờ, bộ ký tự, v.v. thường được gửi đi mà không thông báo cho người dùng. Do đó, việc thiết kế giao thức mạng với tính ẩn danh được đặt làm trọng tâm có thể tránh làm lộ danh tính người dùng.

Ngoài ra còn có các cân nhắc về hiệu suất cần xem xét khi quyết định cách tương tác trên I2P. Thư viện streaming và các thành phần được xây dựng trên đó hoạt động với các bước bắt tay tương tự như TCP, trong khi các giao thức I2P cốt lõi (I2NP và I2CP) hoàn toàn dựa trên thông điệp (giống như UDP hoặc trong một số trường hợp là raw IP). Điểm khác biệt quan trọng là với I2P, việc giao tiếp diễn ra qua một mạng lưới dài và rộng — mỗi thông điệp đầu cuối sẽ có độ trễ đáng kể, nhưng có thể chứa payload lên đến vài KB. Một ứng dụng chỉ cần một yêu cầu và phản hồi đơn giản có thể loại bỏ mọi trạng thái và giảm độ trễ phát sinh từ các bước bắt tay khởi động và ngắt kết nối bằng cách sử dụng datagram (nỗ lực tối đa) mà không cần lo lắng về việc phát hiện MTU hoặc phân mảnh thông điệp.

<figure style="text-align:center; margin: 2rem 0;">
  <img src="/images/i2ptunnel_serverclient.png" alt="Creating a server-client connection using I2PTunnel only requires creating a single tunnel." />
  <figcaption>Figure 1: Creating a server-client connection using I2PTunnel only requires creating a single tunnel.</figcaption>
</figure>
<figure style="text-align:center; margin: 2rem 0;">
  <img src="/images/i2ptunnel_peertopeer.png" alt="Setting up connections for a peer-to-peer applications requires a very large amount of tunnels." />
  <figcaption>Figure 2: Setting up connections for a peer-to-peer applications requires a very large amount of tunnels.</figcaption>
</figure>
Tóm lại, có một số lý do để viết mã riêng cho I2P:

- Tạo một lượng lớn các instance I2PTunnel tiêu tốn một lượng tài nguyên đáng kể, điều này gây vấn đề cho các ứng dụng phân tán (một tunnel mới được yêu cầu cho mỗi peer).
- Các giao thức mạng thông thường thường gửi rất nhiều dữ liệu bổ sung có thể được sử dụng để xác định người dùng. Lập trình đặc biệt cho I2P cho phép tạo ra một giao thức mạng không làm rò rỉ thông tin như vậy, giữ cho người dùng ẩn danh và an toàn.
- Các giao thức mạng được thiết kế để sử dụng trên internet thông thường có thể không hiệu quả trên I2P, một mạng có độ trễ cao hơn nhiều.

I2P hỗ trợ một [giao diện plugins](/docs/specs/plugin/) tiêu chuẩn cho các nhà phát triển để các ứng dụng có thể dễ dàng tích hợp và phân phối.

Các ứng dụng được viết bằng Java và có thể truy cập/chạy được thông qua giao diện HTML qua webapps/app.war tiêu chuẩn có thể được xem xét để đưa vào bản phân phối I2P.

## Các Khái Niệm Quan Trọng

Có một số thay đổi cần phải điều chỉnh khi sử dụng I2P:

### Đích đến

Một ứng dụng chạy trên I2P gửi và nhận tin nhắn từ một điểm cuối duy nhất được bảo mật bằng mã hóa — một "destination" (đích đến). Về mặt TCP hoặc UDP, một destination có thể (phần lớn) được coi là tương đương với một cặp tên máy chủ cộng với số cổng, mặc dù có một số khác biệt.

- Bản thân I2P destination là một cấu trúc mật mã — tất cả dữ liệu gửi đến nó đều được mã hóa như thể có triển khai IPsec toàn cầu với vị trí (ẩn danh) của điểm cuối được ký như thể có triển khai DNSSEC toàn cầu.
- I2P destinations là các định danh di động — chúng có thể được chuyển từ I2P router này sang router khác (hoặc thậm chí có thể "multihome" — hoạt động trên nhiều router cùng lúc). Điều này khá khác biệt so với thế giới TCP hoặc UDP, nơi một điểm cuối duy nhất (cổng) phải ở trên một máy chủ duy nhất.
- I2P destinations khá lớn và phức tạp — bên trong, chúng chứa một khóa công khai ElGamal 2048 bit để mã hóa, một khóa công khai DSA 1024 bit để ký, và một chứng chỉ có kích thước biến đổi, có thể chứa proof of work (bằng chứng công việc) hoặc dữ liệu làm mờ.

Hiện có các cách để tham chiếu đến những destination lớn và khó đọc này bằng các tên ngắn và dễ nhớ (ví dụ: "irc.duck.i2p"), nhưng các kỹ thuật đó không đảm bảo tính duy nhất toàn cục (vì chúng được lưu trữ cục bộ trong cơ sở dữ liệu trên máy của mỗi người) và cơ chế hiện tại không đặc biệt khả mở rộng hay an toàn (các cập nhật cho danh sách host được quản lý bằng cách "đăng ký" các dịch vụ đặt tên). Có thể một ngày nào đó sẽ có hệ thống đặt tên an toàn, dễ đọc với con người, khả mở rộng và duy nhất toàn cục, nhưng các ứng dụng không nên phụ thuộc vào việc nó đã sẵn có. [Thông tin chi tiết về hệ thống đặt tên](/docs/overview/naming/) đã có sẵn.

Mặc dù hầu hết các ứng dụng không cần phân biệt giao thức và cổng, I2P *vẫn* hỗ trợ chúng. Các ứng dụng phức tạp có thể chỉ định giao thức, cổng nguồn và cổng đích trên cơ sở mỗi thông điệp, để ghép kênh lưu lượng trên một destination duy nhất. Xem [trang datagram](/docs/api/datagrams/) để biết chi tiết. Các ứng dụng đơn giản hoạt động bằng cách lắng nghe "tất cả các giao thức" trên "tất cả các cổng" của một destination.

### Tính ẩn danh và bảo mật

I2P có mã hóa đầu cuối đầu cuối minh bạch và xác thực cho tất cả dữ liệu được truyền qua mạng — nếu Bob gửi đến destination của Alice, chỉ có destination của Alice mới có thể nhận được, và nếu Bob đang sử dụng thư viện datagrams hoặc streaming, Alice biết chắc chắn rằng destination của Bob là người đã gửi dữ liệu.

Tất nhiên, I2P ẩn danh một cách minh bạch dữ liệu được gửi giữa Alice và Bob, nhưng nó không làm gì để ẩn danh nội dung của những gì họ gửi. Ví dụ, nếu Alice gửi cho Bob một biểu mẫu có tên đầy đủ, giấy tờ tùy thân của chính phủ và số thẻ tín dụng của cô ấy, thì I2P không thể làm gì được. Do đó, các giao thức và ứng dụng nên lưu ý thông tin nào họ đang cố gắng bảo vệ và thông tin nào họ sẵn sàng để lộ.

### I2P Datagram Có Thể Lên Đến Vài KB

Các ứng dụng sử dụng datagram I2P (dù là raw hay repliable) về cơ bản có thể được hiểu theo khái niệm của UDP — các datagram không có thứ tự, tối ưu nhất có thể và phi kết nối — nhưng không giống như UDP, các ứng dụng không cần lo lắng về việc phát hiện MTU và có thể đơn giản gửi đi các datagram lớn. Mặc dù giới hạn trên danh nghĩa là 32 KB, thông điệp được phân mảnh để truyền tải, do đó làm giảm độ tin cậy của toàn bộ. Hiện tại không khuyến nghị sử dụng datagram trên khoảng 10 KB. Xem [trang datagram](/docs/api/datagrams/) để biết chi tiết. Đối với nhiều ứng dụng, 10 KB dữ liệu là đủ cho toàn bộ một yêu cầu hoặc phản hồi, cho phép chúng hoạt động minh bạch trong I2P như một ứng dụng giống UDP mà không cần phải viết mã phân mảnh, gửi lại, v.v.

## Tùy Chọn Phát Triển

Có nhiều cách để gửi dữ liệu qua I2P, mỗi cách có ưu và nhược điểm riêng. Thư viện streaming là giao diện được khuyến nghị, được sử dụng bởi phần lớn các ứng dụng I2P.

### Thư viện Streaming

[Thư viện streaming đầy đủ](/docs/specs/streaming/) hiện là giao diện tiêu chuẩn. Nó cho phép lập trình sử dụng các socket giống TCP, như được giải thích trong [Hướng dẫn phát triển Streaming](#developing-with-the-streaming-library).

### BOB

BOB là [Basic Open Bridge](/docs/legacy/bob/), cho phép ứng dụng bằng bất kỳ ngôn ngữ nào thực hiện kết nối streaming đến và từ I2P. Tại thời điểm hiện tại, nó chưa hỗ trợ UDP, nhưng hỗ trợ UDP đang được lên kế hoạch trong tương lai gần. BOB cũng chứa một số công cụ, chẳng hạn như tạo khóa destination và xác minh rằng một địa chỉ tuân thủ các đặc tả của I2P. Thông tin cập nhật và các ứng dụng sử dụng BOB có thể được tìm thấy tại [I2P Site](http://bob.i2p/) này.

### SAM, SAM V2, SAM V3

*SAM không được khuyến nghị. SAM V2 chấp nhận được, SAM V3 được khuyến nghị.*

SAM là giao thức [Simple Anonymous Messaging](/docs/legacy/sam/) (Nhắn tin Ẩn danh Đơn giản), cho phép một ứng dụng được viết bằng bất kỳ ngôn ngữ nào giao tiếp với cầu nối SAM thông qua một socket TCP thông thường và để cầu nối đó ghép kênh tất cả lưu lượng I2P của nó, phối hợp minh bạch việc mã hóa/giải mã và xử lý dựa trên sự kiện. SAM hỗ trợ ba kiểu hoạt động:

- streams, khi Alice và Bob muốn gửi dữ liệu cho nhau một cách đáng tin cậy và theo thứ tự
- repliable datagrams, khi Alice muốn gửi cho Bob một tin nhắn mà Bob có thể trả lời
- raw datagrams, khi Alice muốn tận dụng tối đa băng thông và hiệu suất có thể, và Bob không quan tâm liệu người gửi dữ liệu có được xác thực hay không (ví dụ: dữ liệu được truyền tải tự xác thực)

SAM V3 hướng đến cùng mục tiêu với SAM và SAM V2, nhưng không yêu cầu ghép kênh/tách kênh. Mỗi luồng I2P được xử lý bởi socket riêng giữa ứng dụng và cầu nối SAM. Ngoài ra, các gói dữ liệu có thể được gửi và nhận bởi ứng dụng thông qua truyền thông datagram với cầu nối SAM.

[SAM V2](/docs/legacy/samv2/) là phiên bản mới được sử dụng bởi imule, khắc phục một số vấn đề trong [SAM](/docs/legacy/sam/).

[SAM V3](/docs/api/samv3/) được sử dụng bởi imule kể từ phiên bản 1.4.0.

### I2PTunnel

Ứng dụng I2PTunnel cho phép các ứng dụng xây dựng các tunnel giống TCP cụ thể tới các peer bằng cách tạo các ứng dụng I2PTunnel 'client' (lắng nghe trên một cổng cụ thể và kết nối đến một destination I2P cụ thể bất cứ khi nào có socket mở đến cổng đó) hoặc các ứng dụng I2PTunnel 'server' (lắng nghe một destination I2P cụ thể và bất cứ khi nào nhận được kết nối I2P mới, nó sẽ outproxy đến một máy chủ TCP/cổng cụ thể). Các luồng này là 8-bit clean và được xác thực và bảo mật thông qua cùng thư viện streaming mà SAM sử dụng, nhưng có một chi phí không nhỏ liên quan đến việc tạo nhiều instance I2PTunnel riêng biệt, vì mỗi instance có destination I2P riêng và bộ tunnel, khóa, v.v. riêng của chúng.

### SOCKS

I2P hỗ trợ proxy SOCKS V4 và V5. Các kết nối outbound hoạt động tốt. Chức năng inbound (máy chủ) và UDP có thể chưa hoàn thiện và chưa được kiểm tra đầy đủ.

### Ministreaming

*Đã xóa*

Trước đây có một thư viện "ministreaming" đơn giản, nhưng bây giờ ministreaming.jar chỉ chứa các giao diện cho thư viện streaming đầy đủ.

### Datagram

*Được khuyến nghị cho các ứng dụng kiểu UDP*

[Thư viện Datagram](/docs/api/datagrams/) cho phép gửi các gói tin kiểu UDP. Có thể sử dụng:

- Datagram có thể trả lời
- Datagram thô

### I2CP

*Không khuyến nghị*

[I2CP](/docs/specs/i2cp/) là một giao thức độc lập với ngôn ngữ lập trình, nhưng để triển khai thư viện I2CP bằng ngôn ngữ khác ngoài Java thì cần phải viết một lượng mã nguồn đáng kể (các thủ tục mã hóa, xử lý tuần tự hóa đối tượng, xử lý thông điệp không đồng bộ, v.v.). Mặc dù có thể viết thư viện I2CP bằng C hoặc ngôn ngữ khác, nhưng nhiều khả năng sẽ hữu ích hơn khi sử dụng thư viện SAM bằng C.

### Ứng dụng Web

I2P đi kèm với máy chủ web Jetty, và việc cấu hình để sử dụng máy chủ Apache thay thế rất đơn giản. Bất kỳ công nghệ ứng dụng web tiêu chuẩn nào cũng có thể hoạt động.

## Bắt Đầu Phát Triển — Hướng Dẫn Đơn Giản

Phát triển ứng dụng sử dụng I2P yêu cầu một bản cài đặt I2P đang hoạt động và một môi trường phát triển theo lựa chọn của bạn. Nếu bạn đang sử dụng Java, bạn có thể bắt đầu phát triển với [streaming library](#developing-with-the-streaming-library) hoặc datagram library. Khi sử dụng ngôn ngữ lập trình khác, có thể sử dụng SAM hoặc BOB.

### Phát triển với Thư viện Streaming

Dưới đây là phiên bản được cắt gọn và hiện đại hóa của ví dụ trong trang gốc. Để xem ví dụ đầy đủ, hãy xem trang legacy hoặc các ví dụ Java của chúng tôi trong codebase.

```java
// Server example (excerpt)
I2PSocketManager manager = I2PSocketManagerFactory.createManager();
I2PServerSocket server = manager.getServerSocket();
I2PSocket socket = server.accept();
BufferedReader br = new BufferedReader(new InputStreamReader(socket.getInputStream()));
String s;
while ((s = br.readLine()) != null) {
    System.out.println("Received: " + s);
}
```
*Ví dụ code: máy chủ cơ bản nhận dữ liệu.*

```java
// Client example (excerpt)
I2PSocketManager manager = I2PSocketManagerFactory.createManager();
Destination dest = new Destination(serverDestBase64);
I2PSocket socket = manager.connect(dest);
BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(socket.getOutputStream()));
bw.write("Hello I2P!\n");
bw.flush();
```
*Ví dụ mã: client kết nối và gửi một dòng.*
