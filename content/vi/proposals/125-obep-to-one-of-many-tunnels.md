---
title: "Giao nhận OBEP tới các kênh 1-of-N hoặc N-of-N"
number: "125"
author: "zzz, str4d"
created: "2016-03-10"
lastupdated: "2017-04-07"
status: "Open"
thread: "http://zzz.i2p/topics/2099"
---

## Tổng quan

Đề xuất này bao gồm hai cải tiến nhằm cải thiện hiệu suất mạng:

- Ủy quyền việc chọn IBGW cho OBEP bằng cách cung cấp cho nó một danh sách các
  lựa chọn thay vì một lựa chọn đơn lẻ.

- Cho phép định tuyến gói tin multicast tại OBEP.


## Động lực

Trong trường hợp kết nối trực tiếp, ý tưởng là giảm tắc nghẽn kết nối, bằng
cách cho phép OBEP có sự linh hoạt trong cách nó kết nối với các IBGW. Khả năng chỉ định
nhiều kênh cũng cho phép chúng ta thực hiện multicast tại OBEP (bằng cách
giao nhận thông điệp tới tất cả các kênh được chỉ định).

Một giải pháp thay thế cho phần ủy quyền của đề xuất này là gửi thông qua
một hash [LeaseSet](http://localhost:63465/en/docs/specs/common-structures/#leaseset), tương tự như khả năng hiện tại để chỉ định một hash
[RouterIdentity](http://localhost:63465/en/docs/specs/common-structures/#common-structure-specification). Điều này sẽ dẫn đến một thông điệp nhỏ hơn và một LeaseSet có thể mới hơn. Tuy nhiên:

1. Nó sẽ buộc OBEP phải thực hiện tra cứu

2. LeaseSet có thể không được công bố cho floodfill, vì vậy việc tra cứu sẽ thất bại.

3. LeaseSet có thể bị mã hóa, vì vậy OBEP không thể lấy được các lease.

4. Chỉ định một LeaseSet tiết lộ cho OBEP [Destination](/en/docs/specs/common-structures/#destination) của thông điệp,
   điều mà họ có thể chỉ phát hiện bằng cách quét tất cả các LeaseSets trong
   mạng và tìm kiếm một Lease khớp.


## Thiết kế

Người khởi tạo (OBGW) sẽ đặt một số (toàn bộ?) các [Leases](http://localhost:63465/en/docs/specs/common-structures/#lease) mục tiêu vào
các chỉ dẫn giao nhận [TUNNEL-DELIVERY](/en/docs/specs/i2np/#tunnel-message-delivery-instructions) thay vì chỉ chọn một.

OBEP sẽ chọn một trong số đó để giao nhận tới. OBEP sẽ chọn, nếu có thể, một cái mà nó đã được kết nối
hoặc đã biết. Điều này sẽ làm đường OBEP-IBGW nhanh hơn và đáng tin cậy hơn, và giảm số lượng
kết nối mạng tổng thể.

Chúng ta có một loại phân phối chưa sử dụng (0x03) và hai bit còn lại (0 và 1) trong
các cờ cho [TUNNEL-DELIVERY](/en/docs/specs/i2np/#tunnel-message-delivery-instructions), mà chúng ta có thể tận dụng để thực hiện những tính năng này.


## Tác động bảo mật

Đề xuất này không thay đổi lượng thông tin bị lộ về Mục tiêu của OBGW hay quan điểm của họ về NetDB:

- Một kẻ tấn công kiểm soát OBEP và đang quét LeaseSets từ NetDB đã có thể xác định liệu
  một thông điệp có được gửi tới một Mục tiêu cụ thể hay không, bằng cách tìm kiếm cặp
  [TunnelId](http://localhost:63465/en/docs/specs/common-structures/#tunnelid) / [RouterIdentity](http://localhost:63465/en/docs/specs/common-structures/#common-structure-specification). Tại tệ nhất, sự hiện diện của nhiều Lease trong TMDI
  có thể làm nhanh hơn việc tìm một khớp trong cơ sở dữ liệu của kẻ tấn công.

- Một kẻ tấn công đang điều hành một Mục tiêu độc hại đã có thể thu thập thông tin về quan điểm
  của một nạn nhân đang kết nối về NetDB, bằng cách công bố LeaseSets chứa các kênh vào khác nhau tới
  các floodfill khác nhau, và quan sát xem qua kênh nào OBGW kết nối. Từ quan điểm của họ,
  việc OBEP chọn kênh để sử dụng là tương tự chức năng với việc OBGW thực hiện lựa chọn.

Cờ multicast rò rỉ sự thật rằng OBGW đang multicast tới các OBEPs.
Điều này tạo ra một sự đánh đổi giữa hiệu suất và quyền riêng tư cần được cân nhắc khi
thực hiện các giao thức cấp cao hơn. Là một cờ tùy chọn, người dùng có thể đưa ra quyết định phù hợp cho ứng dụng của họ.
Tuy nhiên, có thể có lợi ích nếu đây là hành vi mặc định cho các ứng dụng tương thích,
vì việc sử dụng rộng rãi bởi một loạt ứng dụng sẽ giảm thiểu sự rò rỉ thông tin về
ứng dụng cụ thể từ thông điệp.


## Đặc tả kỹ thuật

Các Chỉ dẫn Giao nhận Phân đoạn Đầu Tiên [TUNNEL-DELIVERY](/en/docs/specs/i2np/#tunnel-message-delivery-instructions) sẽ được chỉnh sửa như sau:

```
+----+----+----+----+----+----+----+----+
|flag|  Tunnel ID (opt)  |              |
+----+----+----+----+----+              +
|                                       |
+                                       +
|         To Hash (optional)            |
+                                       +
|                                       |
+                        +----+----+----+
|                        |dly | Message  
+----+----+----+----+----+----+----+----+
 ID (opt) |extended opts (opt)|cnt | (o)
+----+----+----+----+----+----+----+----+
 Tunnel ID N   |                        |
+----+----+----+                        +
|                                       |
+                                       +
|         To Hash N (optional)          |
+                                       +
|                                       |
+              +----+----+----+----+----+
|              | Tunnel ID N+1 (o) |    |
+----+----+----+----+----+----+----+    +
|                                       |
+                                       +
|         To Hash N+1 (optional)        |
+                                       +
|                                       |
+                                  +----+
|                                  | sz
+----+----+----+----+----+----+----+----+
     |
+----+

flag ::
       1 byte
       Thứ tự bit: 76543210
       bit 6-5: loại giao nhận
                 0x03 = TUNNELS
       bit 0: multicast? Nếu 0, giao nhận tới một trong những kênh
                          Nếu 1, giao nhận tới tất cả các kênh
                          Đặt giá trị 0 để tương thích với các lần sử dụng trong tương lai nếu
                          loại giao nhận không phải là TUNNELS

Count ::
       1 byte
       Tùy chọn, có mặt nếu loại giao nhận là TUNNELS
       2-255 - Số lượng cặp id/hash theo sau

Tunnel ID :: `TunnelId`
To Hash ::
       36 bytes mỗi cái
       Tùy chọn, có mặt nếu loại giao nhận là TUNNELS
       cặp id/hash

Tổng độ dài: Độ dài thông thường là:
       75 bytes cho giao nhận TUNNELS đếm 2 (tin nhắn không phân mảnh);
       79 bytes cho giao nhận TUNNELS đếm 2 (phân đoạn đầu tiên)

Phần còn lại của chỉ dẫn giao nhận không thay đổi
```


## Tương thích

Các đồng nghiệp duy nhất cần phải hiểu đặc tả mới là OBGWs và OBEPs. Chúng ta có thể
làm thay đổi này tương thích với mạng hiện tại bằng cách khiến việc sử dụng nó có điều kiện
trên phiên bản I2P mục tiêu [VERSIONS](/en/docs/specs/i2np/#protocol-versions):

* OBGWs phải chọn các OBEP tương thích khi xây dựng các kênh outbound, dựa trên
  phiên bản I2P được quảng cáo trong [RouterInfo](http://localhost:63465/en/docs/specs/common-structures/#routerinfo) của họ.

* Các đồng nghiệp quảng cáo phiên bản mục tiêu phải hỗ trợ phân tích các cờ mới,
  và không được từ chối các chỉ dẫn dưới dạng không hợp lệ.
