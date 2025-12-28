---
title: "UDP Trackers"
number: "160"
author: "zzz"
created: "2022-01-03"
lastupdated: "2025-06-25"
status: "Đã đóng"
thread: "http://zzz.i2p/topics/1634"
target: "0.9.67"
toc: true
---

## Trạng thái

Đã được phê duyệt tại đánh giá 2025-06-24. Đặc tả tại [UDP specification](/docs/specs/udp-bittorrent-announces/). Đã triển khai trong zzzot 0.20.0-beta2. Đã triển khai trong i2psnark từ API 0.9.67. Kiểm tra tài liệu của các triển khai khác để biết trạng thái.

## Tổng quan

Đề xuất này dành cho việc triển khai UDP tracker trong I2P.

### Change History

Một đề xuất sơ bộ về UDP tracker trong I2P đã được đăng tải trên [trang thông số kỹ thuật bittorrent](/docs/applications/bittorrent/) của chúng tôi vào tháng 5 năm 2014; điều này có trước quy trình đề xuất chính thức của chúng tôi, và nó chưa bao giờ được triển khai. Đề xuất này được tạo ra vào đầu năm 2022 và đã đơn giản hóa phiên bản năm 2014.

Vì đề xuất này dựa vào các datagram có thể trả lời, nó đã được tạm hoãn khi chúng tôi bắt đầu làm việc trên [đề xuất Datagram2](/proposals/163-datagram2/) vào đầu năm 2023. Đề xuất đó đã được phê duyệt vào tháng 4 năm 2025.

Phiên bản 2023 của đề xuất này quy định hai chế độ, "tương thích" và "nhanh". Phân tích sâu hơn cho thấy chế độ nhanh sẽ không an toàn và cũng sẽ không hiệu quả đối với các client có số lượng lớn torrent. Hơn nữa, BiglyBT đã bày tỏ sự ưa thích cho chế độ tương thích. Chế độ này sẽ dễ triển khai hơn cho bất kỳ tracker hoặc client nào hỗ trợ tiêu chuẩn [BEP 15](http://www.bittorrent.org/beps/bep_0015.html).

Mặc dù chế độ tương thích phức tạp hơn để triển khai từ đầu ở phía client, chúng tôi đã có mã sơ bộ cho nó được bắt đầu vào năm 2023.

Do đó, phiên bản hiện tại ở đây được đơn giản hóa thêm để loại bỏ chế độ nhanh, và loại bỏ thuật ngữ "tương thích". Phiên bản hiện tại chuyển sang định dạng Datagram2 mới, và thêm các tham chiếu đến giao thức mở rộng UDP announce [BEP 41](http://www.bittorrent.org/beps/bep_0041.html).

Ngoài ra, một trường thời gian tồn tại ID kết nối được thêm vào phản hồi kết nối, để mở rộng hiệu quả đạt được của giao thức này.

## Motivation

Khi số lượng người dùng nói chung và số lượng người dùng bittorrent nói riêng tiếp tục tăng lên, chúng ta cần làm cho các tracker và announce hiệu quả hơn để các tracker không bị quá tải.

Bittorrent đã đề xuất UDP tracker trong BEP 15 [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) vào năm 2008, và phần lớn các tracker trên clearnet hiện tại đều chỉ sử dụng UDP.

Rất khó để tính toán mức tiết kiệm băng thông của datagram so với giao thức streaming. Một yêu cầu có thể trả lời có kích thước tương đương với streaming SYN, nhưng payload nhỏ hơn khoảng 500 byte vì HTTP GET có chuỗi tham số URL khổng lồ 600 byte. Phản hồi thô nhỏ hơn nhiều so với streaming SYN ACK, mang lại mức giảm đáng kể cho lưu lượng outbound của tracker.

Ngoài ra, nên có các giảm thiểu bộ nhớ cụ thể theo từng triển khai, vì các datagram yêu cầu ít trạng thái trong bộ nhớ hơn nhiều so với kết nối streaming.

Mã hóa và chữ ký Post-Quantum như được hình dung trong [/proposals/169-pq-crypto/](/proposals/169-pq-crypto/) sẽ tăng đáng kể chi phí overhead của các cấu trúc được mã hóa và ký, bao gồm destinations, leasesets, streaming SYN và SYN ACK. Việc giảm thiểu overhead này là quan trọng khi có thể trước khi PQ crypto được áp dụng trong I2P.

## Động lực

Đề xuất này sử dụng repliable datagram2, repliable datagram3, và raw datagrams, như được định nghĩa trong [/docs/api/datagrams/](/docs/api/datagrams/). Datagram2 và Datagram3 là các biến thể mới của repliable datagrams, được định nghĩa trong Đề xuất 163 [/proposals/163-datagram2/](/proposals/163-datagram2/). Datagram2 bổ sung khả năng chống replay và hỗ trợ chữ ký offline. Datagram3 nhỏ hơn so với định dạng datagram cũ, nhưng không có xác thực.

### BEP 15

Để tham khảo, luồng thông điệp được định nghĩa trong [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) như sau:

```
Client                        Tracker
    Connect Req. ------------->
      <-------------- Connect Resp.
    Announce Req. ------------->
      <-------------- Announce Resp.
    Announce Req. ------------->
      <-------------- Announce Resp.
```
Giai đoạn kết nối là cần thiết để ngăn chặn việc giả mạo địa chỉ IP. Tracker trả về một ID kết nối mà client sử dụng trong các thông báo tiếp theo. ID kết nối này hết hạn mặc định sau một phút ở client và sau hai phút ở tracker.

I2P sẽ sử dụng cùng luồng thông điệp như BEP 15, để dễ dàng áp dụng trong các cơ sở mã client hiện có hỗ trợ UDP: vì hiệu quả và vì các lý do bảo mật được thảo luận dưới đây:

```
Client                        Tracker
    Connect Req. ------------->       (Repliable Datagram2)
      <-------------- Connect Resp.   (Raw)
    Announce Req. ------------->      (Repliable Datagram3)
      <-------------- Announce Resp.  (Raw)
    Announce Req. ------------->      (Repliable Datagram3)
      <-------------- Announce Resp.  (Raw)
             ...
```
Điều này có khả năng cung cấp tiết kiệm băng thông lớn so với các thông báo streaming (TCP). Mặc dù Datagram2 có kích thước tương đương với streaming SYN, nhưng phản hồi raw nhỏ hơn nhiều so với streaming SYN ACK. Các yêu cầu tiếp theo sử dụng Datagram3, và các phản hồi tiếp theo là raw.

Các yêu cầu announce là Datagram3 để tracker không cần duy trì một bảng ánh xạ lớn từ ID kết nối đến đích announce hoặc hash. Thay vào đó, tracker có thể tạo ra ID kết nối theo cách mật mã từ hash của người gửi, timestamp hiện tại (dựa trên một khoảng thời gian nào đó), và một giá trị bí mật. Khi nhận được yêu cầu announce, tracker sẽ xác thực ID kết nối, và sau đó sử dụng hash của người gửi Datagram3 làm mục tiêu gửi.

### Lịch Sử Thay Đổi

Đối với một ứng dụng tích hợp (router và client trong một tiến trình, ví dụ như i2psnark, và plugin Java ZzzOT), hoặc đối với một ứng dụng dựa trên I2CP (ví dụ như BiglyBT), việc triển khai và định tuyến lưu lượng streaming và datagram một cách riêng biệt sẽ rất đơn giản. ZzzOT và i2psnark được kỳ vọng sẽ là tracker và client đầu tiên triển khai đề xuất này.

Các tracker và client không tích hợp được thảo luận bên dưới.

#### Trackers

Có bốn triển khai I2P tracker được biết đến:

- zzzot, một plugin router Java tích hợp, chạy tại opentracker.dg2.i2p và một số địa chỉ khác
- tracker2.postman.i2p, chạy có thể đằng sau một Java router và HTTP Server tunnel
- OpenTracker C cũ, được port bởi zzz, với hỗ trợ UDP được comment out
- OpenTracker C mới, được port bởi r4sas, chạy tại opentracker.r4sas.i2p và có thể các địa chỉ khác,
  chạy có thể đằng sau một i2pd router và HTTP Server tunnel

Đối với một ứng dụng tracker bên ngoài hiện đang sử dụng HTTP server tunnel để nhận các yêu cầu announce, việc triển khai có thể khá khó khăn. Một tunnel chuyên biệt có thể được phát triển để dịch các datagram thành các yêu cầu/phản hồi HTTP cục bộ. Hoặc, một tunnel chuyên biệt xử lý cả yêu cầu HTTP và datagram có thể được thiết kế để chuyển tiếp các datagram đến quá trình bên ngoài. Những quyết định thiết kế này sẽ phụ thuộc nhiều vào các triển khai router và tracker cụ thể, và nằm ngoài phạm vi của đề xuất này.

#### Clients

Các client torrent bên ngoài dựa trên SAM như qbittorrent và các client dựa trên libtorrent khác sẽ yêu cầu [SAM v3.3](/docs/api/samv3/) không được hỗ trợ bởi i2pd. Điều này cũng cần thiết cho hỗ trợ DHT, và đủ phức tạp đến mức không có client torrent SAM nào đã biết đã triển khai nó. Không có triển khai dựa trên SAM nào của đề xuất này được kỳ vọng sớm.

### Connection Lifetime

[BEP 15](http://www.bittorrent.org/beps/bep_0015.html) chỉ định rằng ID kết nối sẽ hết hạn trong một phút tại client, và trong hai phút tại tracker. Điều này không thể cấu hình được. Điều đó hạn chế các lợi ích hiệu suất tiềm năng, trừ khi các client gom nhóm các thông báo để thực hiện tất cả trong khung thời gian một phút. i2psnark hiện tại không gom nhóm các thông báo; nó phân tán chúng ra để tránh các đợt lưu lượng đột biến. Các power user được báo cáo là đang chạy hàng nghìn torrent cùng lúc, và việc tập trung nhiều thông báo như vậy vào một phút là không thực tế.

Ở đây, chúng tôi đề xuất mở rộng phản hồi connect để thêm trường thời gian tồn tại kết nối tùy chọn. Mặc định, nếu không có, là một phút. Nếu không, thời gian tồn tại được chỉ định tính bằng giây sẽ được client sử dụng, và tracker sẽ duy trì connection ID thêm một phút nữa.

### Compatibility with BEP 15

Thiết kế này duy trì tính tương thích với [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) nhiều nhất có thể để hạn chế các thay đổi cần thiết trong các client và tracker hiện có.

Thay đổi duy nhất cần thiết là định dạng thông tin peer trong phản hồi announce. Việc thêm trường lifetime trong phản hồi connect không bắt buộc nhưng được khuyến khích mạnh mẽ vì hiệu quả, như đã giải thích ở trên.

### BEP 15

Một mục tiêu quan trọng của giao thức UDP announce là ngăn chặn việc giả mạo địa chỉ. Client phải thực sự tồn tại và đóng gói một leaseset thực. Nó phải có các tunnel đến để nhận Connect Response. Những tunnel này có thể là zero-hop và được xây dựng ngay lập tức, nhưng điều đó sẽ làm lộ người tạo. Giao thức này hoàn thành mục tiêu đó.

### Hỗ trợ Tracker/Client

- Đề xuất này không hỗ trợ các điểm đến được che mờ (blinded destinations),
  nhưng có thể được mở rộng để làm như vậy. Xem bên dưới.

## Thiết kế

### Protocols and Ports

Repliable Datagram2 sử dụng giao thức I2CP 19; repliable Datagram3 sử dụng giao thức I2CP 20; raw datagram sử dụng giao thức I2CP 18. Các yêu cầu có thể là Datagram2 hoặc Datagram3. Các phản hồi luôn là raw. Định dạng repliable datagram cũ hơn ("Datagram1") sử dụng giao thức I2CP 17 KHÔNG được sử dụng cho các yêu cầu hoặc phản hồi; chúng phải được loại bỏ nếu nhận được trên các cổng request/reply. Lưu ý rằng giao thức Datagram1 17 vẫn được sử dụng cho giao thức DHT.

Các yêu cầu sử dụng "to port" của I2CP từ URL thông báo; xem bên dưới. "From port" của yêu cầu được client chọn, nhưng nên khác không và khác với các port được DHT sử dụng, để các phản hồi có thể được phân loại dễ dàng. Các tracker nên từ chối các yêu cầu nhận được trên port sai.

Các phản hồi sử dụng "to port" I2CP từ yêu cầu. "From port" của yêu cầu là "to port" từ yêu cầu.

### Announce URL

Định dạng URL announce không được chỉ định trong [BEP 15](http://www.bittorrent.org/beps/bep_0015.html), nhưng như trong clearnet, các URL announce UDP có dạng "udp://host:port/path". Đường dẫn path bị bỏ qua và có thể để trống, nhưng thường là "/announce" trên clearnet. Phần :port nên luôn được có mặt, tuy nhiên, nếu phần ":port" bị bỏ qua, hãy sử dụng cổng I2CP mặc định là 6969, vì đó là cổng phổ biến trên clearnet. Cũng có thể có các tham số cgi &a=b&c=d được thêm vào, những tham số này có thể được xử lý và cung cấp trong yêu cầu announce, xem [BEP 41](http://www.bittorrent.org/beps/bep_0041.html). Nếu không có tham số hoặc đường dẫn path, dấu / ở cuối cũng có thể bị bỏ qua, như được ngụ ý trong [BEP 41](http://www.bittorrent.org/beps/bep_0041.html).

### Thời gian tồn tại của kết nối

Tất cả các giá trị được gửi theo thứ tự byte mạng (big endian). Không nên mong đợi các gói tin có kích thước chính xác như nhau. Các phần mở rộng trong tương lai có thể tăng kích thước của các gói tin.

#### Connect Request

Client đến tracker. 16 bytes. Phải có thể trả lời được Datagram2. Giống như trong [BEP 15](http://www.bittorrent.org/beps/bep_0015.html). Không có thay đổi.

```
Offset  Size            Name            Value
  0       64-bit integer  protocol_id     0x41727101980 // magic constant
  8       32-bit integer  action          0 // connect
  12      32-bit integer  transaction_id
```
#### Connect Response

Tracker đến client. 16 hoặc 18 byte. Phải là dữ liệu thô. Giống như trong [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) ngoại trừ những điều được ghi chú bên dưới.

```
Offset  Size            Name            Value
  0       32-bit integer  action          0 // connect
  4       32-bit integer  transaction_id
  8       64-bit integer  connection_id
  16      16-bit integer  lifetime        optional  // Change from BEP 15
```
Phản hồi PHẢI được gửi đến I2CP "to port" mà đã được nhận như "from port" của yêu cầu.

Trường lifetime là tùy chọn và chỉ ra thời gian tồn tại của connection_id client tính bằng giây. Mặc định là 60, và giá trị tối thiểu nếu được chỉ định là 60. Giá trị tối đa là 65535 hoặc khoảng 18 giờ. Tracker nên duy trì connection_id trong 60 giây lâu hơn so với thời gian tồn tại của client.

#### Announce Request

Client đến tracker. Tối thiểu 98 bytes. Phải là Datagram3 có thể trả lời. Giống như trong [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) trừ những điểm được ghi chú bên dưới.

connection_id là như đã nhận được trong phản hồi kết nối.

```
Offset  Size            Name            Value
  0       64-bit integer  connection_id
  8       32-bit integer  action          1     // announce
  12      32-bit integer  transaction_id
  16      20-byte string  info_hash
  36      20-byte string  peer_id
  56      64-bit integer  downloaded
  64      64-bit integer  left
  72      64-bit integer  uploaded
  80      32-bit integer  event           0     // 0: none; 1: completed; 2: started; 3: stopped
  84      32-bit integer  IP address      0     // default
  88      32-bit integer  key
  92      32-bit integer  num_want        -1    // default
  96      16-bit integer  port
  98      varies          options     optional  // As specified in BEP 41
```
Những thay đổi từ [BEP 15](http://www.bittorrent.org/beps/bep_0015.html):

- key bị bỏ qua
- port có thể bị bỏ qua
- Phần options, nếu có, được định nghĩa như trong [BEP 41](http://www.bittorrent.org/beps/bep_0041.html)

Phản hồi PHẢI được gửi đến "to port" I2CP mà đã nhận được từ "from port" của yêu cầu. Không sử dụng port từ yêu cầu announce.

#### Announce Response

Tracker đến client. Tối thiểu 20 bytes. Phải là raw. Giống như trong [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) ngoại trừ những điểm được ghi chú dưới đây.

```
Offset  Size            Name            Value
  0           32-bit integer  action          1 // announce
  4           32-bit integer  transaction_id
  8           32-bit integer  interval
  12          32-bit integer  leechers
  16          32-bit integer  seeders
  20   32 * n 32-byte hash    binary hashes     // Change from BEP 15
  ...                                           // Change from BEP 15
```
Các thay đổi từ [BEP 15](http://www.bittorrent.org/beps/bep_0015.html):

- Thay vì 6-byte IPv4+port hoặc 18-byte IPv6+port, chúng ta trả về
  bội số của "compact responses" 32-byte với các SHA-256 binary peer hashes.
  Tương tự như với TCP compact responses, chúng ta không bao gồm port.

Phản hồi PHẢI được gửi tới "to port" của I2CP đã nhận được như là "from port" của yêu cầu. Không sử dụng port từ yêu cầu announce.

I2P datagram có kích thước tối đa rất lớn khoảng 64 KB; tuy nhiên, để đảm bảo truyền tải đáng tin cậy, nên tránh các datagram lớn hơn 4 KB. Để hiệu quả băng thông, các tracker có lẽ nên giới hạn số lượng peer tối đa khoảng 50, tương ứng với gói tin khoảng 1600 byte trước khi tính overhead ở các lớp khác nhau, và nên nằm trong giới hạn payload hai tunnel message sau khi phân mảnh.

Như trong BEP 15, không có số lượng được bao gồm về số lượng địa chỉ peer (IP/port cho BEP 15, hash ở đây) để theo sau. Mặc dù không được xem xét trong BEP 15, một dấu hiệu kết thúc peer gồm toàn số không có thể được định nghĩa để chỉ ra rằng thông tin peer đã hoàn chỉnh và một số dữ liệu mở rộng theo sau.

Để có thể mở rộng trong tương lai, các client nên bỏ qua hash 32-byte toàn số không và bất kỳ dữ liệu nào theo sau. Các tracker nên từ chối announce từ hash toàn số không, mặc dù hash đó đã bị cấm bởi các Java router.

#### Scrape

Yêu cầu/phản hồi scrape từ [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) không được yêu cầu bởi đề xuất này, nhưng có thể được triển khai nếu muốn, không cần thay đổi gì. Client phải lấy được connection ID trước. Yêu cầu scrape luôn là Datagram3 có thể phản hồi. Phản hồi scrape luôn ở dạng thô.

#### Trackers

Tracker đến client. Tối thiểu 8 byte (nếu thông điệp trống). Phải là raw. Giống như trong [BEP 15](http://www.bittorrent.org/beps/bep_0015.html). Không có thay đổi.

```
Offset  Size            Name            Value
  0       32-bit integer  action          3 // error
  4       32-bit integer  transaction_id
  8       string          message
```
## Extensions

Các extension bits hoặc trường version không được bao gồm. Clients và trackers không nên giả định các gói tin có kích thước nhất định. Theo cách này, các trường bổ sung có thể được thêm vào mà không làm hỏng tính tương thích. Định dạng extensions được định nghĩa trong [BEP 41](http://www.bittorrent.org/beps/bep_0041.html) được khuyến nghị nếu cần thiết.

Phản hồi kết nối được sửa đổi để thêm thời gian tồn tại ID kết nối tùy chọn.

Nếu cần hỗ trợ blinded destination, chúng ta có thể thêm địa chỉ blinded 35-byte vào cuối yêu cầu announce, hoặc yêu cầu blinded hashes trong các phản hồi, sử dụng định dạng [BEP 41](http://www.bittorrent.org/beps/bep_0041.html) (các tham số TBD). Tập hợp các địa chỉ peer blinded 35-byte có thể được thêm vào cuối phản hồi announce, sau một hash 32-byte toàn số 0.

## Implementation guidelines

Xem phần thiết kế ở trên để thảo luận về những thách thức đối với các client và tracker không tích hợp, không sử dụng I2CP.

### Tương thích với BEP 15

Đối với một hostname tracker nhất định, client nên ưu tiên URL UDP hơn HTTP, và không nên announce đến cả hai.

Các client đã hỗ trợ BEP 15 chỉ cần những thay đổi nhỏ.

Nếu một client hỗ trợ DHT hoặc các giao thức datagram khác, có thể nó nên chọn một cổng khác làm "from port" của yêu cầu để các phản hồi trở về cổng đó và không bị trộn lẫn với các thông điệp DHT. Client chỉ nhận các datagram thô làm phản hồi. Các tracker sẽ không bao giờ gửi datagram2 có thể phản hồi đến client.

Các client với danh sách mặc định của opentracker nên cập nhật danh sách để thêm các URL UDP sau khi các opentracker đã biết được xác nhận hỗ trợ UDP.

Các client có thể hoặc không thể triển khai việc truyền lại các yêu cầu. Việc truyền lại, nếu được triển khai, nên sử dụng thời gian chờ ban đầu ít nhất 15 giây và nhân đôi thời gian chờ cho mỗi lần truyền lại (exponential backoff).

Các client phải back off sau khi nhận được phản hồi lỗi.

### Phân tích Bảo mật

Các tracker đã có hỗ trợ BEP 15 sẽ chỉ cần những thay đổi nhỏ. Đề xuất này khác với đề xuất năm 2014 ở chỗ tracker phải hỗ trợ việc nhận repliable datagram2 và datagram3 trên cùng một cổng.

Để giảm thiểu các yêu cầu tài nguyên của tracker, giao thức này được thiết kế để loại bỏ mọi yêu cầu về việc tracker phải lưu trữ ánh xạ giữa các hash của client với các ID kết nối để xác thực sau này. Điều này có thể thực hiện được vì gói tin yêu cầu announce là một gói tin Datagram3 có thể trả lời, do đó nó chứa hash của người gửi.

Một triển khai được khuyến nghị là:

- Định nghĩa epoch hiện tại là thời gian hiện tại với độ phân giải của thời gian sống kết nối,
  ``epoch = now / lifetime``.
- Định nghĩa hàm hash mã hóa ``H(secret, clienthash, epoch)`` tạo ra
  đầu ra 8 byte.
- Tạo hằng số ngẫu nhiên secret được sử dụng cho tất cả các kết nối.
- Đối với phản hồi kết nối, tạo ``connection_id = H(secret,  clienthash, epoch)``
- Đối với yêu cầu announce, xác thực connection ID nhận được trong epoch hiện tại bằng cách kiểm tra
  ``connection_id == H(secret, clienthash, epoch) || connection_id == H(secret, clienthash, epoch - 1)``

## Migration

Các client hiện có không hỗ trợ UDP announce URL và bỏ qua chúng.

Các tracker hiện tại không hỗ trợ nhận datagram có thể trả lời hoặc datagram thô, chúng sẽ bị loại bỏ.

Đề xuất này hoàn toàn tùy chọn. Cả client và tracker đều không bắt buộc phải triển khai nó vào bất kỳ thời điểm nào.

## Rollout

Các triển khai đầu tiên dự kiến sẽ được thực hiện trong ZzzOT và i2psnark. Chúng sẽ được sử dụng để kiểm thử và xác minh đề xuất này.

Các triển khai khác sẽ được thực hiện theo nhu cầu sau khi hoàn tất việc kiểm thử và xác minh.
