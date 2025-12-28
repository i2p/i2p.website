---
title: "Các thông báo BitTorrent qua UDP"
description: "Đặc tả giao thức cho các announce dựa trên UDP của tracker BitTorrent trong I2P"
slug: "udp-announces"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## Tổng quan

Đặc tả này mô tả giao thức cho các announce (yêu cầu thông báo tới tracker) UDP của BitTorrent trong I2P. Đối với đặc tả tổng quan về BitTorrent trong I2P, hãy xem [tài liệu BitTorrent trên I2P](/docs/applications/bittorrent/). Để biết bối cảnh và thông tin bổ sung về quá trình phát triển của đặc tả này, xem [Đề xuất 160](/proposals/160-udp-trackers/).

Giao thức này đã được phê duyệt chính thức vào ngày 24 tháng 6 năm 2025 và được triển khai trong I2P phiên bản 2.10.0 (API 0.9.67), phát hành ngày 8 tháng 9 năm 2025. Hỗ trợ UDP tracker (máy chủ tracker dùng UDP) hiện đang hoạt động trên mạng I2P với nhiều tracker vận hành ở môi trường sản xuất và hỗ trợ đầy đủ cho trình khách i2psnark.

## Thiết kế

Thông số kỹ thuật này sử dụng datagram2 có thể trả lời, datagram3 có thể trả lời và datagram thô, như được định nghĩa trong [Đặc tả Datagram I2P](/docs/api/datagrams/). Datagram2 và Datagram3 là các biến thể của datagram có thể trả lời, được định nghĩa trong [Đề xuất 163](/proposals/163-datagram2/). Datagram2 bổ sung khả năng chống tấn công phát lại và hỗ trợ chữ ký ngoại tuyến. Datagram3 nhỏ hơn so với định dạng datagram cũ, nhưng không có xác thực.

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
Giai đoạn kết nối là bắt buộc để ngăn chặn việc giả mạo địa chỉ IP. Tracker (máy chủ theo dõi) trả về một ID kết nối mà client (máy khách) sử dụng trong các lần announce (thông báo) tiếp theo. ID kết nối này theo mặc định sẽ hết hạn sau một phút ở phía client, và sau hai phút ở phía tracker.

I2P sử dụng cùng luồng thông điệp như BEP 15 (đề xuất mở rộng BitTorrent số 15), để dễ áp dụng vào các codebase client hỗ trợ UDP hiện có, vì hiệu quả, và vì các lý do bảo mật được thảo luận bên dưới:

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
Điều này có thể giúp tiết kiệm đáng kể băng thông so với các thông báo dạng streaming (TCP). Mặc dù Datagram2 có kích thước gần bằng một gói SYN của streaming, phản hồi thô nhỏ hơn nhiều so với gói SYN ACK của streaming. Các yêu cầu tiếp theo sử dụng Datagram3, và các phản hồi tiếp theo ở dạng thô.

Các yêu cầu announce (thông báo tới tracker) sử dụng Datagram3 (giao thức Datagram phiên bản 3), để tracker (trình theo dõi) không phải duy trì một bảng ánh xạ lớn từ các ID kết nối tới đích announce hoặc mã băm. Thay vào đó, tracker có thể tạo ID kết nối bằng mật mã từ mã băm của bên gửi, dấu thời gian hiện tại (dựa trên một khoảng thời gian nhất định) và một giá trị bí mật. Khi nhận được một yêu cầu announce, tracker xác thực ID kết nối, rồi sử dụng mã băm của bên gửi trong Datagram3 làm đích gửi.

### Thời gian sống của kết nối

[BEP 15](http://www.bittorrent.org/beps/bep_0015.html) quy định rằng ID kết nối hết hạn sau một phút ở phía máy khách và sau hai phút ở phía tracker. Không thể cấu hình. Điều đó hạn chế các cải thiện hiệu quả tiềm năng, trừ khi các máy khách gộp các announce (yêu cầu thông báo tới tracker) để thực hiện tất cả trong một cửa sổ thời gian một phút. i2psnark hiện không gộp announce; nó giãn chúng ra để tránh các đợt bùng nổ lưu lượng. Có báo cáo rằng người dùng nâng cao đang chạy hàng nghìn torrent cùng lúc, và dồn từng ấy announce vào trong một phút là không thực tế.

Ở đây, chúng tôi đề xuất mở rộng phản hồi kết nối để bổ sung một trường thời hạn kết nối tùy chọn. Giá trị mặc định, nếu trường này không có, là một phút. Ngược lại, thời hạn được chỉ định tính bằng giây phải được máy khách sử dụng, và tracker (máy chủ theo dõi) sẽ duy trì ID kết nối thêm một phút nữa.

### Tương thích với BEP 15 (Đề xuất Cải tiến BitTorrent số 15)

Thiết kế này duy trì khả năng tương thích với [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) hết mức có thể nhằm hạn chế các thay đổi cần thiết trong các ứng dụng khách và trình theo dõi hiện có.

Thay đổi duy nhất bắt buộc là định dạng của thông tin peer trong phản hồi announce. Việc bổ sung trường lifetime trong phản hồi connect không bắt buộc nhưng rất được khuyến nghị để nâng cao hiệu quả, như đã giải thích ở trên.

### Phân tích bảo mật

Một mục tiêu quan trọng của một giao thức thông báo UDP là ngăn chặn giả mạo địa chỉ. Máy khách phải thực sự tồn tại và đính kèm một leaseSet (tập hợp thông tin cho phép nhận lưu lượng trong I2P) thực. Nó phải có các tunnel vào để nhận Connect Response. Những tunnel này có thể là 0-hop và được dựng ngay lập tức, nhưng như vậy sẽ làm lộ người tạo. Giao thức này đạt được mục tiêu đó.

### Các vấn đề

Giao thức này không hỗ trợ blinded destinations (đích được làm mù để tăng ẩn danh), nhưng có thể được mở rộng để hỗ trợ. Xem bên dưới.

## Đặc tả

### Giao thức và cổng

Datagram2 có thể hồi đáp sử dụng giao thức I2CP 19; Datagram3 có thể hồi đáp sử dụng giao thức I2CP 20; các datagram thô sử dụng giao thức I2CP 18. Các yêu cầu có thể là Datagram2 hoặc Datagram3. Các phản hồi luôn ở dạng thô. Định dạng datagram có thể hồi đáp cũ ("Datagram1") dùng giao thức I2CP 17 KHÔNG được dùng cho yêu cầu hoặc phản hồi; những gói tin này phải bị loại bỏ nếu nhận trên các cổng yêu cầu/phản hồi. Lưu ý rằng Datagram1 theo giao thức 17 vẫn được dùng cho giao thức DHT (bảng băm phân tán).

Các yêu cầu sử dụng trường "to port" của I2CP lấy từ announce URL; xem bên dưới. Trường "from port" của yêu cầu do máy khách chọn, nhưng nên khác 0 và khác với các cổng được DHT sử dụng, để các phản hồi có thể được phân loại dễ dàng. Các tracker nên từ chối các yêu cầu nhận trên sai cổng.

Các phản hồi sử dụng "to port" của I2CP trong yêu cầu. Trường "from port" của phản hồi chính là "to port" của yêu cầu.

### URL thông báo

Định dạng URL announce không được quy định trong [BEP 15](http://www.bittorrent.org/beps/bep_0015.html), nhưng giống như trên clearnet (Internet công khai), các URL announce qua UDP có dạng "udp://host:port/path". Đường dẫn (path) bị bỏ qua và có thể trống, nhưng trên clearnet thường là "/announce". Phần :port luôn phải có; tuy nhiên, nếu bỏ qua phần ":port", hãy dùng cổng I2CP mặc định 6969, vì đó là cổng phổ biến trên clearnet. Cũng có thể có các tham số CGI &a=b&c=d được nối thêm; các tham số đó có thể được xử lý và đưa vào yêu cầu announce, xem [BEP 41](http://www.bittorrent.org/beps/bep_0041.html). Nếu không có tham số hoặc đường dẫn, dấu / ở cuối cũng có thể được lược bỏ, như được ngụ ý trong [BEP 41](http://www.bittorrent.org/beps/bep_0041.html).

### Định dạng Datagram (gói tin không kết nối)

Mọi giá trị đều được gửi theo thứ tự byte trên mạng (big endian). Đừng kỳ vọng các gói tin có đúng một kích thước nhất định. Các phần mở rộng trong tương lai có thể làm tăng kích thước của gói tin.

#### Yêu cầu kết nối

Từ client đến tracker. 16 byte. Phải là Datagram2 có thể hồi đáp (repliable). Giống như trong [BEP 15](http://www.bittorrent.org/beps/bep_0015.html). Không có thay đổi.

```
Offset  Size            Name            Value
0       64-bit integer  protocol_id     0x41727101980 // magic constant
8       32-bit integer  action          0 // connect
12      32-bit integer  transaction_id
```
#### Phản hồi kết nối

Từ tracker đến client. 16 hoặc 18 byte. Phải ở dạng thô (raw). Giống như trong [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) ngoại trừ như ghi chú bên dưới.

```
Offset  Size            Name            Value
0       32-bit integer  action          0 // connect
4       32-bit integer  transaction_id
8       64-bit integer  connection_id
16      16-bit integer  lifetime        optional  // Change from BEP 15
```
Phản hồi PHẢI được gửi tới I2CP "to port" trùng với "from port" của yêu cầu.

Trường lifetime (thời hạn) là tùy chọn và cho biết thời hạn có hiệu lực của connection_id ở phía máy khách, tính bằng giây. Mặc định là 60, và nếu có chỉ định thì giá trị tối thiểu là 60. Giá trị tối đa là 65535, tương đương khoảng 18 giờ. Tracker (trình theo dõi) nên duy trì connection_id lâu hơn thời hạn của máy khách thêm 60 giây.

#### Yêu cầu thông báo

Máy khách tới tracker. Tối thiểu 98 byte. Phải là repliable Datagram3 (datagram có thể trả lời, loại 3). Giống như trong [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) trừ các điểm được ghi chú bên dưới.

connection_id trùng với giá trị nhận được trong phản hồi kết nối.

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
84      32-bit integer  IP address      0     // default, unused in I2P
88      32-bit integer  key
92      32-bit integer  num_want        -1    // default
96      16-bit integer  port                  // must be same as I2CP from port
98      varies          options     optional  // As specified in BEP 41
```
Những thay đổi so với [BEP 15](http://www.bittorrent.org/beps/bep_0015.html):

- key bị bỏ qua
- địa chỉ IP không được sử dụng
- cổng có thể sẽ bị bỏ qua nhưng phải trùng với I2CP from port (cổng nguồn)
- phần tùy chọn, nếu có, được định nghĩa như trong [BEP 41](http://www.bittorrent.org/beps/bep_0041.html)

Phản hồi PHẢI được gửi tới I2CP "to port" là giá trị đã được nhận trong trường "from port" của yêu cầu. Không được sử dụng cổng từ announce request (yêu cầu thông báo).

#### Phản hồi thông báo

Từ tracker đến máy khách. Tối thiểu 20 byte. Phải ở dạng thô. Giống như trong [BEP 15](http://www.bittorrent.org/beps/bep_0015.html), trừ những điểm được nêu bên dưới.

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
Các thay đổi so với [BEP 15](http://www.bittorrent.org/beps/bep_0015.html):

- Thay vì 6-byte IPv4+cổng hoặc 18-byte IPv6+cổng, chúng tôi trả về một số lượng (là bội số) các "compact responses" (phản hồi dạng compact) 32-byte chứa các băm SHA-256 dạng nhị phân của peer. Tương tự như TCP compact responses, chúng tôi không bao gồm cổng.

Phản hồi PHẢI được gửi tới I2CP "to port" đã được nhận như "from port" của yêu cầu. Không sử dụng cổng từ yêu cầu announce.

I2P datagrams (gói dữ liệu không kết nối) có kích thước tối đa rất lớn, khoảng 64 KB; tuy nhiên, để truyền tải đáng tin cậy, nên tránh các datagram lớn hơn 4 KB. Vì hiệu quả băng thông, trackers (máy chủ theo dõi trong BitTorrent) có lẽ nên giới hạn số nút ngang hàng tối đa khoảng 50, tương ứng với một gói khoảng 1600 byte trước phần phụ trội (overhead) ở các lớp khác nhau, và sau khi phân mảnh, nên nằm trong giới hạn tải trọng của hai thông điệp tunnel.

Như trong BEP 15, không có số đếm kèm theo về số lượng địa chỉ peer (IP/port đối với BEP 15, còn ở đây là các băm) sẽ theo sau. Mặc dù BEP 15 không đề cập đến điều này, có thể định nghĩa một end-of-peers marker (dấu mốc kết thúc danh sách peer) gồm toàn số 0 để cho biết rằng thông tin peer đã đầy đủ và sẽ có một số dữ liệu mở rộng theo sau.

Để có thể mở rộng trong tương lai, các ứng dụng khách nên bỏ qua một giá trị băm dài 32 byte toàn số 0, cùng với mọi dữ liệu theo sau. Các tracker nên từ chối các yêu cầu announce (thông báo) từ một giá trị băm toàn số 0, mặc dù giá trị băm đó đã bị Java routers chặn sẵn.

#### Trích xuất

Yêu cầu/phản hồi scrape (truy vấn thống kê từ tracker) từ [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) không bắt buộc theo đặc tả này, nhưng có thể được triển khai nếu muốn; không cần thay đổi. Máy khách phải lấy ID kết nối trước. Yêu cầu scrape luôn là repliable Datagram3 (datagram v3 có thể phản hồi). Phản hồi scrape luôn là raw (datagram thô, không có khả năng phản hồi).

#### Phản hồi lỗi

Từ tracker đến client. Tối thiểu 8 byte (nếu thông điệp rỗng). Phải ở dạng thô. Giống như trong [BEP 15](http://www.bittorrent.org/beps/bep_0015.html). Không có thay đổi.

```
Offset  Size            Name            Value
0       32-bit integer  action          3 // error
4       32-bit integer  transaction_id
8       string          message
```
## Phần mở rộng

Các bit mở rộng hoặc trường phiên bản không được đưa vào. Các client và tracker không nên giả định các gói tin có kích thước nhất định. Bằng cách này, có thể thêm các trường bổ sung mà không phá vỡ tính tương thích. Nếu cần, khuyến nghị sử dụng định dạng phần mở rộng được định nghĩa trong [BEP 41](http://www.bittorrent.org/beps/bep_0041.html).

Phản hồi kết nối được sửa đổi để thêm một thời gian tồn tại tùy chọn cho ID kết nối.

Nếu cần hỗ trợ blinded destination (đích được làm mù/che khuất), chúng ta có thể hoặc thêm địa chỉ 35 byte dạng blinded vào cuối yêu cầu announce, hoặc yêu cầu các băm blinded trong các phản hồi, sử dụng định dạng [BEP 41](http://www.bittorrent.org/beps/bep_0041.html) (các tham số TBD). Tập hợp các địa chỉ peer 35 byte dạng blinded có thể được thêm vào cuối phản hồi announce, sau một băm 32 byte toàn số 0.

## Hướng dẫn triển khai

Xem phần thiết kế ở trên để xem thảo luận về những thách thức đối với các máy khách và tracker (máy chủ theo dõi) không tích hợp, không sử dụng I2CP.

### Ứng dụng khách

Với một hostname tracker nhất định, máy khách nên ưu tiên các URL UDP hơn các URL HTTP, và không nên gửi announce (yêu cầu thông báo) tới cả hai.

Các ứng dụng khách đã hỗ trợ BEP 15 chỉ cần một vài chỉnh sửa nhỏ.

Nếu một ứng dụng khách hỗ trợ DHT hoặc các giao thức datagram (gói dữ liệu không kết nối) khác, thì có lẽ nên chọn một cổng khác làm "from port" của yêu cầu để các phản hồi quay về cổng đó và không bị lẫn với các thông điệp DHT. Ứng dụng khách chỉ nhận các datagram thô dưới dạng phản hồi. Các tracker sẽ không bao giờ gửi một repliable datagram2 (datagram có thể hồi đáp) tới ứng dụng khách.

Các máy khách có danh sách mặc định các opentracker nên cập nhật danh sách để thêm các URL UDP sau khi các opentracker đã được xác nhận là hỗ trợ UDP.

Các client có thể triển khai hoặc không triển khai cơ chế gửi lại yêu cầu. Nếu có triển khai gửi lại, nên sử dụng thời gian chờ ban đầu tối thiểu 15 giây và nhân đôi thời gian chờ cho mỗi lần gửi lại (exponential backoff — tăng thời gian trì hoãn theo cấp số nhân).

Các client phải back off (giảm tần suất/đợi trước khi thử lại) sau khi nhận được phản hồi lỗi.

### Các máy chủ theo dõi

Các tracker (máy chủ theo dõi BitTorrent) đã hỗ trợ BEP 15 chỉ cần những chỉnh sửa nhỏ. Đặc tả này khác với đề xuất năm 2014 ở chỗ tracker phải hỗ trợ việc tiếp nhận repliable datagram2 và datagram3 (datagram có thể hồi đáp) trên cùng một cổng.

Để giảm thiểu yêu cầu tài nguyên của tracker, giao thức này được thiết kế nhằm loại bỏ mọi yêu cầu buộc tracker phải lưu trữ các ánh xạ từ băm của máy khách tới ID kết nối để xác thực về sau. Điều này khả thi vì gói yêu cầu announce là một gói Datagram3 (định dạng datagram phiên bản 3 của I2P) có thể hồi đáp, nên nó chứa băm của người gửi.

Một phương án triển khai được khuyến nghị là:

- Định nghĩa epoch (thời đoạn) hiện tại là thời gian hiện tại với độ phân giải bằng thời gian tồn tại của kết nối, `epoch = now / lifetime`.
- Định nghĩa một hàm băm mật mã `H(secret, clienthash, epoch)` tạo ra đầu ra 8 byte.
- Tạo ra giá trị bí mật hằng ngẫu nhiên dùng cho mọi kết nối.
- Đối với các phản hồi kết nối, tạo `connection_id = H(secret, clienthash, epoch)`
- Đối với các yêu cầu announce (thông báo), xác thực ID kết nối nhận được trong epoch hiện tại bằng cách kiểm tra `connection_id == H(secret, clienthash, epoch) || connection_id == H(secret, clienthash, epoch - 1)`

## Trạng thái triển khai

Giao thức này được phê duyệt vào ngày 24 tháng 6 năm 2025 và hoạt động đầy đủ trên mạng I2P kể từ tháng 9 năm 2025.

### Các triển khai hiện tại

**i2psnark**: Hỗ trợ đầy đủ cho UDP tracker (máy chủ theo dõi sử dụng giao thức UDP) được tích hợp trong I2P phiên bản 2.10.0 (API 0.9.67), phát hành ngày 8 tháng 9 năm 2025. Tất cả các bản cài đặt I2P từ phiên bản này trở đi mặc định có hỗ trợ UDP tracker.

**zzzot tracker**: Phiên bản 0.20.0-beta2 và các phiên bản mới hơn hỗ trợ announce qua UDP (thông báo tới tracker). Tính đến tháng 10 năm 2025, các tracker triển khai chính thức sau đang hoạt động: - opentracker.dg2.i2p - opentracker.simp.i2p - opentracker.skank.i2p

### Ghi chú về khả năng tương thích của ứng dụng khách

**Các hạn chế của SAM v3.3**: Các ứng dụng khách BitTorrent bên ngoài sử dụng SAM (Simple Anonymous Messaging - Nhắn tin ẩn danh đơn giản) yêu cầu hỗ trợ SAM v3.3 cho Datagram2/3. Tính năng này có sẵn trong Java I2P nhưng hiện chưa được i2pd (bản triển khai I2P bằng C++) hỗ trợ, điều này có thể hạn chế việc áp dụng trong các ứng dụng khách dựa trên libtorrent như qBittorrent.

**Các client I2CP**: Các client sử dụng I2CP trực tiếp (chẳng hạn như BiglyBT) có thể triển khai hỗ trợ cho tracker UDP mà không bị các hạn chế của SAM (giao thức SAM của I2P).

## Tài liệu tham khảo

- **[BEP15]**: [Giao thức Tracker UDP của BitTorrent](http://www.bittorrent.org/beps/bep_0015.html)
- **[BEP41]**: [Các phần mở rộng cho Giao thức Tracker UDP](http://www.bittorrent.org/beps/bep_0041.html)
- **[DATAGRAMS]**: [Đặc tả I2P Datagrams](/docs/api/datagrams/)
- **[Prop160]**: [Đề xuất Tracker UDP](/proposals/160-udp-trackers/)
- **[Prop163]**: [Đề xuất Datagram2](/proposals/163-datagram2/)
- **[SPEC]**: [BitTorrent qua I2P](/docs/applications/bittorrent/)
