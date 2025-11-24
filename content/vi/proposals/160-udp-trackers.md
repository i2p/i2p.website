---
title: "UDP Trackers"
number: "160"
author: "zzz"
created: "2022-01-03"
lastupdated: "2025-06-25"
status: "Closed"
thread: "http://zzz.i2p/topics/1634"
target: "0.9.67"
---

## Trạng thái

Đã được phê duyệt trong cuộc họp ngày 24-06-2025. 
Quy cách tại [UDP specification](/en/docs/spec/udp-bittorrent-announces/). 
Đã được triển khai trong zzzot 0.20.0-beta2. 
Đã được triển khai trong i2psnark tính đến API 0.9.67. 
Kiểm tra tài liệu của các triển khai khác để biết trạng thái.


## Tổng quan

Đề xuất này để thực hiện các tracker UDP trong I2P.


### Lịch sử thay đổi

Một đề xuất sơ bộ về các tracker UDP trong I2P đã được đăng trên trang quy cách bittorrent của chúng tôi [/en/docs/applications/bittorrent/](/en/docs/applications/bittorrent/)
vào tháng 5 năm 2014; điều này tiền đề quy trình đề xuất chính thức của chúng tôi, và nó chưa bao giờ được triển khai.
Đề xuất này được tạo ra vào đầu năm 2022 và đơn giản hóa phiên bản 2014.

Do đề xuất này phụ thuộc vào datagram có thể trả lời, nên nó được tạm hoãn khi chúng tôi 
bắt đầu làm việc trên đề xuất Datagram2 [/en/proposals/163-datagram2/](/en/proposals/163-datagram2/) vào đầu năm 2023. 
Đề xuất đó đã được phê duyệt vào tháng 4 năm 2025.

Phiên bản 2023 của đề xuất này đã chỉ định hai chế độ, "tương thích" và "nhanh".
Phân tích thêm đã chỉ ra rằng chế độ nhanh sẽ không an toàn và cũng sẽ 
không hiệu quả với các khách hàng có số lượng torrents lớn.
Hơn nữa, BiglyBT đã chỉ ra sự ưu tiên cho chế độ tương thích.
Chế độ này sẽ dễ triển khai hơn cho bất kỳ tracker hoặc khách hàng nào hỗ trợ 
chuẩn [BEP 15](http://www.bittorrent.org/beps/bep_0015.html).

Mặc dù chế độ tương thích phức tạp hơn khi triển khai từ đầu 
về phía khách hàng, chúng tôi đã có mã sơ bộ cho nó bắt đầu từ năm 2023.

Vì vậy, phiên bản hiện tại này được đơn giản hóa hơn nữa để loại bỏ chế độ nhanh,
và loại bỏ thuật ngữ "tương thích". Phiên bản hiện tại chuyển sang
định dạng Datagram2 mới, và thêm các tham chiếu đến giao thức mở rộng thông báo UDP [BEP 41](http://www.bittorrent.org/beps/bep_0041.html).

Cũng vậy, một phần đời sống ID kết nối được thêm vào phản hồi kết nối,
để mở rộng các lợi ích hiệu quả của giao thức này.


## Động lực

Khi số lượng người dùng nói chung và số lượng người dùng bittorrent cụ thể tiếp tục tăng,
chúng tôi cần làm cho các tracker và thông báo thông minh hơn để tránh quá tải cho các tracker.

Bittorrent đã đề xuất các tracker UDP trong BEP 15 [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) vào năm 2008, và phần lớn
các tracker trên clearnet hiện giờ chỉ có UDP.

Thật khó để tính toán phạm vi băng thông tiết kiệm giữa giao thức datagram và giao thức streaming.
Một yêu cầu có thể trả lời có kích thước tương đương một streaming SYN, nhưng tải trọng
giảm khoảng 500 byte vì HTTP GET có một chuỗi tham số URL lớn 600 byte.
Phản hồi thực sự nhỏ hơn rất nhiều so với một streaming SYN ACK, giảm rõ rệt
khối lượng dữ liệu đi ra ngoài của tracker.

Ngoài ra, có thể có những giảm bộ nhớ cụ thể trong triển khai,
vì datagram yêu cầu ít trạng thái trong bộ nhớ hơn so với kết nối streaming.

Mã hóa và chữ ký hậu lượng tử như dự tính trong [/en/proposals/169-pq-crypto/](/en/proposals/169-pq-crypto/) sẽ tăng đáng kể
overhead của các cấu trúc được mã hóa và ký, bao gồm các điểm đến,
leaseset, streaming SYN và SYN ACK. Quan trọng là giảm thiểu điều này
trước khi mã hóa PQ được áp dụng trong I2P.


## Thiết kế

Đề xuất này sử dụng datagram có thể trả lời Datagram2, datagram có thể trả lời Datagram3, và datagram thô,
như định nghĩa trong [/en/docs/spec/datagrams/](/en/docs/spec/datagrams/).
Datagram2 và Datagram3 là các biến thể mới của datagram có thể trả lời,
được định nghĩa trong Đề xuất 163 [/en/proposals/163-datagram2/](/en/proposals/163-datagram2/).
Datagram2 thêm khả năng chống lại phát lại và hỗ trợ chữ ký ngoại tuyến.
Datagram3 nhỏ hơn định dạng datagram cũ, nhưng không có xác thực.


### BEP 15

Để tham khảo, luồng tin nhắn được định nghĩa trong [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) như sau:

```
Client                        Tracker
    Connect Req. ------------->
      <-------------- Connect Resp.
    Announce Req. ------------->
      <-------------- Announce Resp.
    Announce Req. ------------->
      <-------------- Announce Resp.
```

Giai đoạn kết nối là cần thiết để ngăn chặn giả mạo địa chỉ IP.
Tracker trả về một ID kết nối mà khách hàng sử dụng trong các thông báo tiếp theo.
ID kết nối này hết hạn mặc định trong một phút tại khách hàng, và trong hai phút tại tracker.

I2P sẽ sử dụng cùng luồng tin nhắn như BEP 15,
để dễ dàng áp dụng trong các mã cơ sở khách hàng có khả năng UDP hiện tại:
để tăng hiệu quả, và vì các lý do bảo mật được thảo luận dưới đây:

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

Điều này có thể cung cấp tiết kiệm băng thông lớn hơn
so với thông báo streaming (TCP).
Mặc dù Datagram2 có kích thước tương đương một streaming SYN,
phản hồi thô nhỏ hơn rất nhiều so với streaming SYN ACK.
Các yêu cầu sau sử dụng Datagram3, và các phản hồi sau là thô.

Các yêu cầu thông báo là Datagram3 để tracker không cần
duy trì một bảng ánh xạ lớn của ID kết nối đến điểm đến thông báo hoặc hash.
Thay vào đó, tracker có thể tạo ra các ID kết nối bằng mật mã
từ hash người gửi, dấu thời gian hiện tại (dựa trên một khoảng thời gian),
và một giá trị bí mật.
Khi một yêu cầu thông báo được nhận, tracker xác nhận
ID kết nối, và sau đó sử dụng
Datagram3 hash người gửi làm mục tiêu gửi.

### Hỗ trợ Tracker/Khách hàng

Đối với một ứng dụng tích hợp (bộ định tuyến và khách hàng trong một quy trình, ví dụ như i2psnark, và plugin Java ZzzOT),
hoặc đối với một ứng dụng dựa trên I2CP (ví dụ như BiglyBT),
nó sẽ đơn giản để triển khai và định hướng lưu lượng streaming và datagram riêng biệt.
ZzzOT và i2psnark dự kiến sẽ là tracker và khách hàng đầu tiên thực hiện đề xuất này.

Các tracker và khách hàng không tích hợp được thảo luận dưới đây.


Trackers
````````

Có bốn triển khai tracker I2P được biết đến:

- zzzot, một plugin Java router tích hợp, chạy tại opentracker.dg2.i2p và một số khác
- tracker2.postman.i2p, có lẽ chạy sau một Java router và HTTP Server tunnel
- Opentracker C cũ, được port bởi zzz, với hỗ trợ UDP bị bình luận
- Opentracker C mới, được port bởi r4sas, chạy tại opentracker.r4sas.i2p và có thể các khác,
  có lẽ chạy sau một router i2pd và HTTP Server tunnel

Đối với một ứng dụng tracker bên ngoài hiện sử dụng một HTTP server tunnel để nhận các yêu cầu thông báo,
việc triển khai có thể khá khó khăn.
Một tunnel chuyên biệt có thể được phát triển để dịch các datagram thành các yêu cầu/đáp ứng HTTP địa phương.
Hoặc, một tunnel chuyên biệt xử lý cả yêu cầu HTTP và datagram có thể được thiết kế
để chuyển tiếp datagrams tới quá trình bên ngoài.
Những quyết định thiết kế này sẽ phụ thuộc nặng nề vào các triển khai router và tracker riêng lẻ,
và nằm ngoài phạm vi của đề xuất này.


Clients
```````

Các khách hàng torrent bên ngoài dựa trên SAM như qbittorrent và các khách hàng dựa trên libtorrent khác
sẽ yêu cầu SAM v3.3 [/en/docs/api/samv3/](/en/docs/api/samv3/) mà không được hỗ trợ bởi i2pd.
Đây cũng là yêu cầu cho hỗ trợ DHT, và đủ phức tạp để không khách hàng torrent SAM nào đã thực hiện nó.
Không mong đợi bất kỳ triển khai nào dựa trên SAM của đề xuất này sớm.


### Thời hạn kết nối

[BEP 15](http://www.bittorrent.org/beps/bep_0015.html) chỉ định rằng ID kết nối hết hạn trong một phút tại khách hàng, và trong hai phút tại tracker.
Nó không điều chỉnh được.
Điều này hạn chế các lợi thế hiệu quả có thể, trừ khi
các khách hàng ghép thông báo để thực hiện tất cả chúng trong cửa sổ một phút.
i2psnark không hiện tại ghép thông báo; nó phân bổ chúng ra, để tránh sự bùng nổ của trafffic.
Người dùng power được báo cáo đang chạy hàng ngàn torrents đồng thời,
và bùng nổ nhiều thông báo như vậy trong một phút là không thực tế.

Ở đây, chúng tôi đề xuất mở rộng phản hồi kết nối để thêm một trường thời hạn kết nối tùy chọn.
Mặc định, nếu không có, là một phút. Nếu có, thời hạn được chỉ định
tính bằng giây, sẽ được khách hàng sử dụng, và tracker sẽ duy trì
ID kết nối thêm một phút nữa.


### Tương thích với BEP 15

Thiết kế này duy trì sự tương thích với [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) càng nhiều càng tốt
để giảm thiểu thay đổi yêu cầu trong các khách hàng và trackers hiện tại.

Thay đổi duy nhất được yêu cầu là định dạng thông tin peer trong phản hồi thông báo.
Việc thêm trường thời gian sống trong phản hồi kết nối không bắt buộc
nhưng được khuyến cáo mạnh mẽ cho hiệu quả, như được giải thích ở trên.



### Phân tích bảo mật

Mục tiêu quan trọng của một giao thức thông báo UDP là ngăn chặn giả mạo địa chỉ.
Khách hàng phải thật sự tồn tại và đi kèm với một leaseset thực sự.
Nó phải có các kênh vào để nhận Phản hồi Kết nối.
Các kênh này có thể là không-hóp và được tạo tức thì, nhưng điều đó sẽ
làm lộ người tạo.
Protocol này đạt được mục tiêu đó.



### Vấn đề

- Đề xuất này không hỗ trợ các điểm đến huyền bí,
  nhưng có thể được mở rộng để làm như vậy. Xem bên dưới.




## Quy cách

### Giao thức và cổng

Datagram có thể trả lời Datagram2 sử dụng giao thức I2CP 19;
datagram có thể trả lời Datagram3 sử dụng giao thức I2CP 20;
datagram thô sử dụng giao thức I2CP 18.
Yêu cầu có thể là Datagram2 hoặc Datagram3. Phản hồi luôn là thô.
Định dạng datagram có thể trả lời cũ ("Datagram1") sử dụng giao thức I2CP 17
không được sử dụng cho yêu cầu hoặc phản hồi; chúng phải bị hủy nếu nhận được
trên các cổng yêu cầu/phản hồi. Lưu ý rằng giao thức Datagram1 17
vẫn được sử dụng cho giao thức DHT.

Các yêu cầu sử dụng cổng "to port" từ URL thông báo; xem bên dưới.
"Cổng từ" trong yêu cầu được khách hàng chọn, nhưng nên không bằng không,
và là một cổng khác so với những cổng được sử dụng bởi DHT, để đáp ứng
có thể dễ dàng phân loại.
Tracker nên từ chối các yêu cầu nhận sai cổng.

Phản hồi sử dụng "cổng đến" I2CP từ yêu cầu.
"Cổng từ" trong yêu cầu là "cổng đến" từ yêu cầu.


### URL thông báo

Định dạng URL thông báo không được chỉ định trong [BEP 15](http://www.bittorrent.org/beps/bep_0015.html),
nhưng như trên clearnet, URL thông báo UDP là dưới dạng "udp://host:port/path".
Đường dẫn bị bỏ qua và có thể để trống, nhưng thường là "/announce" trên clearnet.
Phần ":port" nên luôn có mặt, tuy nhiên,
nếu phần ":port" bị bỏ qua, sử dụng cổng mặc định I2CP là 6969,
vì đó là cổng phổ biến trên clearnet.
Cũng có thể có các tham số cgi &a=b&c=d đính kèm,
được có thể xử lý và cung cấp trong yêu cầu thông báo, xem [BEP 41](http://www.bittorrent.org/beps/bep_0041.html).
Nếu không có tham số hay đường dẫn, có thể bỏ qua dấu gạch chéo phía sau,
như được ngụ ý trong [BEP 41](http://www.bittorrent.org/beps/bep_0041.html).


### Định dạng Datagram

Tất cả các giá trị được gửi trong thứ tự byte mạng (big endian).
Không kỳ vọng các gói tin có kích thước cố định.
Các phần mở rộng tương lai có thể tăng kích thước gói tin.



Yêu cầu Kết nối
```````````````

Khách hàng đến tracker.
16 byte. Phải là Datagram2 có thể trả lời. Tương tự như trong [BEP 15](http://www.bittorrent.org/beps/bep_0015.html). Không có thay đổi.


```
Offset  Size            Name            Value
  0       64-bit integer  protocol_id     0x41727101980 // hằng số phép màu
  8       32-bit integer  action          0 // kết nối
  12      32-bit integer  transaction_id
```



Phản hồi Kết nối
````````````````

Tracker đến khách hàng.
16 hoặc 18 byte. Phải là thô. Tương tự như trong [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) ngoại trừ được ghi chú dưới đây.


```
Offset  Size            Name            Giá trị
  0       32-bit integer  action          0 // kết nối
  4       32-bit integer  transaction_id
  8       64-bit integer  connection_id
  16      16-bit integer  lifetime        tùy chọn // Thay đổi từ BEP 15
```

Phản hồi PHẢI được gửi đến "to port" của I2CP đã nhận được như là "from port" của yêu cầu.

Trường thời gian sống là tùy chọn và chỉ ra thời gian sống của connection_id tại máy khách tính bằng giây.
Mặc định là 60, và tối thiểu nếu được chỉ ra là 60.
Tối đa là 65535 hoặc khoảng 18 giờ.
Tracker nên duy trì connection_id thêm 60 giây so với thời gian sống của máy khách.



Yêu cầu Thông báo
````````````````

Khách hàng đến tracker.
98 byte tối thiểu. Phải là Datagram3 có thể trả lời. Tương tự như trong [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) ngoại trừ được ghi chú dưới đây.

Connection_id là như nhận được trong phản hồi kết nối.



```
Offset  Size            Name            Giá trị
  0       64-bit integer  connection_id
  8       32-bit integer  action          1     // thông báo
  12      32-bit integer  transaction_id
  16      20-byte string  info_hash
  36      20-byte string  peer_id
  56      64-bit integer  downloaded
  64      64-bit integer  left
  72      64-bit integer  uploaded
  80      32-bit integer  event           0     // 0: không có; 1: hoàn thành; 2: bắt đầu; 3: dừng lại
  84      32-bit integer  IP address      0     // mặc định
  88      32-bit integer  key
  92      32-bit integer  num_want        -1    // mặc định
  96      16-bit integer  port
  98      varies          options     tùy chọn  // Như được chỉ định trong BEP 41
```

Thay đổi từ [BEP 15](http://www.bittorrent.org/beps/bep_0015.html):

- key bị bỏ qua
- port có lẽ bị bỏ qua
- Phần cài đặt tùy chọn, nếu có, được định nghĩa trong [BEP 41](http://www.bittorrent.org/beps/bep_0041.html)

Phản hồi PHẢI được gửi đến "to port" của I2CP đã nhận được như là "from port" của yêu cầu.
Không sử dụng cổng của yêu cầu thông báo.



Phản hồi Thông báo
`````````````````

Tracker đến khách hàng.
20 byte tối thiểu. Phải là thô. Tương tự như trong [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) ngoại trừ được ghi chú dưới đây.



```
Offset  Size            Name            Giá trị
  0           32-bit integer  action          1 // thông báo
  4           32-bit integer  transaction_id
  8           32-bit integer  interval
  12          32-bit integer  leechers
  16          32-bit integer  seeders
  20   32 * n 32-byte hash    binary hashes     // Thay đổi từ BEP 15
  ...                                           // Thay đổi từ BEP 15
```

Thay đổi từ [BEP 15](http://www.bittorrent.org/beps/bep_0015.html):

- Thay vì 6-byte IPv4+port hoặc 18-byte IPv6+port, chúng tôi trả về
  một bội số của các "phản hồi ngắn" 32-byte với các hash peer nhị phân SHA-256.
  Như với các phản hồi TCP ngắn, chúng tôi không bao gồm một cổng.

Phản hồi PHẢI được gửi đến "to port" của I2CP đã nhận được như là "from port" của yêu cầu.
Không sử dụng cổng của yêu cầu thông báo.

I2P datagrams có kích thước tối đa rất lớn khoảng 64 KB;
tuy nhiên, để đảm bảo gửi đi đáng tin cậy, các datagrams lớn hơn 4 KB nên được tránh.
Để tối ưu hóa băng thông, trackers có thể giới hạn số peers tối đa
khoảng 50, tương ứng với gói tin khoảng 1600 byte trước khi có overhead
ở các lớp khác nhau, và nên trong giới hạn tải hai-tunnel-message
sau khi phân mảnh.

Như trong BEP 15, không có số lượng bao gồm của số địa chỉ peer
(IP/cổng cho BEP 15, hashes ở đây) sẽ theo.
Trong khi không được dự tính trong BEP 15, một chỉ thị kết thúc-peers
của tất cả các số không có thể được định nghĩa để chỉ ra rằng thông tin peer đã hoàn thành
và một số dữ liệu mở rộng theo sau.

Để mở rộng là có thể trong tương lai, khách hàng nên bỏ qua
một hash 32-byte toàn-số không, và mọi dữ liệu theo sau.
Trackers nên từ chối thông báo từ một hash toàn số không,
dù hash đó đã bị cấm bởi các router Java.


Scrape
``````

Yêu cầu/phản hồi scrape từ [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) không được yêu cầu bởi đề xuất này,
nhưng có thể được thực hiện nếu cần, không cần thay đổi.
Khách hàng phải chiếm lấy một ID kết nối trước tiên.
Yêu cầu scrape luôn là Datagram3 có thể trả lời.
Phản hồi scrape luôn là thô.



Phản hồi Lỗi
``````````````

Tracker đến khách hàng.
8 byte tối thiểu (nếu thông điệp trống).
Phải là thô. Tương tự như trong [BEP 15](http://www.bittorrent.org/beps/bep_0015.html). Không có thay đổi.

```

Offset  Size            Name            Value
  0       32-bit integer  action          3 // error
  4       32-bit integer  transaction_id
  8       string          message

```



## Phần mở rộng

Các bit mở rộng hoặc trường phiên bản không được bao gồm.
Khách hàng và trackers không nên giả định các packets sẽ có kích thước cố định.
Bằng cách này, các trường bổ sung có thể được thêm vào mà không phá vỡ tính tương thích.
Định dạng các phần mở rộng được định nghĩa trong [BEP 41](http://www.bittorrent.org/beps/bep_0041.html) được khuyến khích nếu cần thiết.

Phản hồi kết nối được sửa đổi để thêm một trường thời gian sống ID kết nối tùy chọn.

Nếu hỗ trợ các điểm đến huyền bí là cần thiết, chúng ta có thể thêm
địa chỉ mù 35-byte vào cuối yêu cầu thông báo,
hoặc yêu cầu các hashes mù trong phản hồi,
sử dụng định dạng [BEP 41](http://www.bittorrent.org/beps/bep_0041.html) (tham số TBD).
Tập hợp các địa chỉ peer mù 35-byte có thể được thêm vào cuối phản hồi thông báo,
sau một hash 32-byte toàn số không.



## Hướng dẫn triển khai

Xem phần thiết kế ở trên để thảo luận về những thách thức cho
các khách hàng và trackers không tích hợp, không phải I2CP.


### Khách hàng

Đối với một tên miền tracker nhất định, một khách hàng nên ưu tiên URL UDP hơn HTTP,
và không nên thông báo tới cả hai.

Khách hàng có hỗ trợ BEP 15 hiện tại nên chỉ yêu cầu các sửa đổi nhỏ.

Nếu một khách hàng hỗ trợ DHT hoặc các giao thức datagram khác, họ nên có thể
chọn một cổng khác làm "cổng từ" yêu cầu để các phản hồi
trở lại cổng đó và không bị trộn lẫn với các tin nhắn DHT.
Khách hàng chỉ nhận datagram thô làm phản hồi.
Trackers sẽ không bao giờ gửi một datagram có thể trả lời đến khách hàng.

Khách hàng có danh sách mặc định các opentracker nên cập nhật danh sách để
thêm các URL UDP sau khi các opentracker đã biết hỗ trợ UDP.

Khách hàng có thể hoặc không thực hiện việc truyền lại các yêu cầu.
Việc truyền lại, nếu thực hiện, nên sử dụng thời gian chờ ban đầu
ít nhất 15 giây, và nhân đôi thời gian chờ với mỗi lần truyền lại
(thay đổi theo cấp số nhân).

Khách hàng phải điều chỉnh sau khi nhận được một phản hồi lỗi.


### Trackers

Các trackers có hỗ trợ BEP 15 hiện tại nên chỉ yêu cầu các sửa đổi nhỏ.
Đề xuất này khác với đề xuất 2014, trong đó tracker
phải hỗ trợ tiếp nhận datagram có thể trả lời và datagram thô cùng một cổng.

Để giảm thiểu yêu cầu tài nguyên tracker,
giao thức này được thiết kế để loại bỏ yêu cầu phải lưu trữ ánh xạ
của các hash khách hàng tới các ID kết nối để xác thực sau này.
Điều này có thể bởi vì gói tin yêu cầu thông báo là gói canh datagram3 có thể trả lời,
nên nó chứa hash của người gửi.

Một triển khai được khuyến nghị là:

- Định nghĩa thời gian hiện tại là thời gian hiện tại với độ phân giải của thời gian sống kết nối,
  ``epoch = now / lifetime``.
- Định nghĩa một hàm băm mật mã ``H(secret, clienthash, epoch)`` mà tạo ra
  đầu ra 8 byte.
- Tạo một hằng số bí mật ngẫu nhiên được sử dụng cho tất cả các kết nối.
- Đối với phản hồi kết nối, tạo ``connection_id = H(secret,  clienthash, epoch)``
- Đối với các yêu cầu thông báo, xác thực ID kết nối nhận được trong thời gian hiện tại bằng cách xác thực
  ``connection_id == H(secret, clienthash, epoch) || connection_id == H(secret, clienthash, epoch - 1)``


## Di cư

Các khách hàng hiện tại không hỗ trợ URL thông báo UDP và bỏ qua chúng.

Các trackers hiện tại không hỗ trợ tiếp nhận các datagram có thể trả lời hoặc thô, chúng sẽ bị bỏ qua.

Đề xuất này hoàn toàn tùy chọn. Khách hàng hoặc trackers không bắt buộc phải thực hiện nó ở bất kỳ thời điểm nào.



## Triển khai

Các triển khai đầu tiên dự kiến sẽ là trong ZzzOT và i2psnark.
Chúng sẽ được sử dụng để kiểm tra và xác minh đề xuất này.

Các triển khai khác sẽ theo sau khi các kiểm tra và xác minh hoàn tất.




