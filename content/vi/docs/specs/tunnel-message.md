---
title: "Đặc tả Thông điệp Tunnel"
description: "Đặc tả cho định dạng các thông điệp tunnel trong I2P"
slug: "tunnel-message"
aliases:
  - "/vi/docs/legacy/tunnel-message"
  - "/vi/docs/legacy/tunnel-message/"
  - "/vi/tunnel_message_spec"
  - "/vi/tunnel_message_spec/"
category: "Thiết kế"
lastUpdated: "2021-01"
accurateFor: "0.9.49"
---

## Tổng quan

Tài liệu này xác định định dạng của các thông điệp tunnel. Để biết thông tin chung về tunnel, hãy xem [tài liệu tunnel](/docs/specs/tunnel-implementation).

## Xử Lý Trước Tin Nhắn

*Tunnel gateway* là lối vào, hoặc bước nhảy đầu tiên, của một tunnel. Đối với outbound tunnel, gateway là người tạo ra tunnel. Đối với inbound tunnel, gateway nằm ở đầu đối diện với người tạo ra tunnel.

Một gateway *tiền xử lý* các thông điệp [I2NP](/docs/specs/i2np) bằng cách phân mảnh và kết hợp chúng thành các thông điệp tunnel.

Trong khi các thông điệp I2NP có kích thước biến đổi từ 0 đến gần 64 KB, thì các thông điệp tunnel có kích thước cố định, khoảng 1 KB. Kích thước thông điệp cố định giúp hạn chế một số loại tấn công có thể thực hiện thông qua việc quan sát kích thước thông điệp.

Sau khi các thông điệp tunnel được tạo, chúng sẽ được mã hóa như mô tả trong [tài liệu tunnel](/docs/specs/tunnel-implementation).

### Thông Điệp Tunnel (Đã Mã Hóa)

Đây là nội dung của một thông điệp dữ liệu tunnel sau khi được mã hóa.

```
+----+----+----+----+----+----+----+----+
|    Tunnel ID      |       IV          |
+----+----+----+----+                   +
|                                       |
+                   +----+----+----+----+
|                   |                   |
+----+----+----+----+                   +
|                                       |
+           Encrypted Data              +
~                                       ~
|                                       |
+                   +-------------------+
|                   |
+----+----+----+----+
```
**Tunnel ID** :: [TunnelId](/docs/specs/common-structures#tunnelid) : 4 byte. ID của hop tiếp theo, khác không.

**IV** :: : 16 bytes. Vector khởi tạo.

**Dữ liệu Mã hóa** :: : 1008 byte. Thông điệp tunnel được mã hóa.

**Tổng kích thước: 1028 byte**

### Thông Điệp Tunnel (Đã Giải Mã)

Đây là nội dung của một thông điệp dữ liệu tunnel khi đã được giải mã.

```
+----+----+----+----+----+----+----+----+
|    Tunnel ID      |       IV          |
+----+----+----+----+                   +
|                                       |
+                   +----+----+----+----+
|                   |     Checksum      |
+----+----+----+----+----+----+----+----+
|          nonzero padding...           |
~                                       ~
|                                       |
+                                  +----+
|                                  |zero|
+----+----+----+----+----+----+----+----+
|                                       |
|       Delivery Instructions  1        |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+       I2NP Message Fragment 1         +
|                                       |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
|       Delivery Instructions 2...      |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+       I2NP Message Fragment 2...      +
|                                       |
~                                       ~
|                                       |
+                   +-------------------+
|                   |
+----+----+----+----+
```
**Tunnel ID** :: [TunnelId](/docs/specs/common-structures#tunnelid) : 4 bytes. ID của hop tiếp theo, khác không.

**IV** :: : 16 byte. Vector khởi tạo.

**Checksum** :: : 4 bytes. 4 byte đầu tiên của hash SHA256 của (nội dung thông điệp (sau byte không) + IV).

**Nonzero padding** :: : 0 hoặc nhiều byte hơn. Dữ liệu ngẫu nhiên khác không để đệm.

**Zero** :: : 1 byte. Giá trị 0x00.

**Hướng dẫn Giao hàng** :: TunnelMessageDeliveryInstructions : Độ dài thay đổi nhưng thường là 7, 39, 43, hoặc 47 byte. Chỉ ra phân đoạn và định tuyến cho phân đoạn.

**Message Fragment** :: : 1 đến 996 byte, giá trị tối đa thực tế phụ thuộc vào kích thước chỉ dẫn giao hàng. Một I2NP Message một phần hoặc đầy đủ.

**Tổng kích thước: 1028 bytes**

#### Ghi chú

- Padding, nếu có, phải được đặt trước các cặp instruction/message. Không có quy định cho padding ở cuối.
- Checksum KHÔNG bao gồm padding hoặc zero byte. Lấy message bắt đầu từ delivery instructions đầu tiên, nối với IV, và tính Hash của nó.

## Hướng dẫn Gửi Tin nhắn Tunnel

Các lệnh được mã hóa bằng một byte điều khiển duy nhất, theo sau là bất kỳ thông tin bổ sung cần thiết nào. Bit đầu tiên (MSB) trong byte điều khiển đó xác định cách phần còn lại của header được diễn giải - nếu nó không được thiết lập, thông điệp hoặc không bị phân mảnh hoặc đây là fragment đầu tiên trong thông điệp. Nếu nó được thiết lập, đây là fragment tiếp theo.

Đặc tả này chỉ dành cho Delivery Instructions bên trong Tunnel Messages. Lưu ý rằng "Delivery Instructions" cũng được sử dụng bên trong Garlic Cloves, nơi định dạng khác biệt đáng kể. Xem [tài liệu I2NP](/docs/specs/i2np#garlicclovedeliveryinstructions) để biết chi tiết. KHÔNG sử dụng đặc tả sau đây cho Garlic Clove Delivery Instructions!

### Hướng Dẫn Giao Nhận Fragment Đầu Tiên

Nếu MSB của byte đầu tiên là 0, đây là một fragment tin nhắn I2NP ban đầu, hoặc một tin nhắn I2NP hoàn chỉnh (không bị phân mảnh), và các hướng dẫn là:

```
+----+----+----+----+----+----+----+----+
|flag|  Tunnel ID (opt)  |              |
+----+----+----+----+----+              +
|                                       |
+                                       +
|         To Hash (optional)            |
+                                       +
|                                       |
+                        +--------------+
|                        |dly | Message
+----+----+----+----+----+----+----+----+
 ID (opt) |extended opts (opt)|  size   |
+----+----+----+----+----+----+----+----+
```
**flag** :: : 1 byte. Thứ tự bit: 76543210   - bit 7: 0 để chỉ định một fragment đầu tiên hoặc một thông điệp không phân mảnh   - bit 6-5: loại phân phối

    - 0x0 = LOCAL
    - 0x01 = TUNNEL
    - 0x02 = ROUTER
    - 0x03 = unused, invalid
    - Note: LOCAL is used for inbound tunnels only, unimplemented for outbound tunnels
- bit 4: có bao gồm delay không? Chưa được triển khai, luôn là 0. Nếu là 1, một byte delay được bao gồm.
  - bit 3: có phân mảnh không? Nếu là 0, thông điệp không bị phân mảnh, những gì theo sau là toàn bộ thông điệp. Nếu là 1, thông điệp bị phân mảnh, và các hướng dẫn chứa một Message ID.
  - bit 2: có extended options không? Chưa được triển khai, luôn là 0. Nếu là 1, extended options được bao gồm.
  - bits 1-0: dành riêng, đặt về 0 để tương thích với các sử dụng trong tương lai

**Tunnel ID** :: [TunnelId](/docs/specs/common-structures#tunnelid) : 4 bytes. Tùy chọn, có mặt nếu loại giao hàng là TUNNEL. ID tunnel đích, khác không.

**To Hash** :: : 32 byte. Tùy chọn, có mặt nếu kiểu gửi là ROUTER hoặc TUNNEL. Nếu là ROUTER, SHA256 Hash của router. Nếu là TUNNEL, SHA256 Hash của gateway router.

**Delay** :: : 1 byte. Tùy chọn, có mặt nếu cờ bao gồm độ trễ được thiết lập. Trong các thông điệp tunnel: Chưa được triển khai, không bao giờ có mặt; đặc tả gốc: bit 7: loại (0 = nghiêm ngặt, 1 = ngẫu nhiên), bit 6-0: số mũ độ trễ (2^giá trị phút).

**Message ID** :: : 4 bytes. Tùy chọn, có mặt nếu thông điệp này là phần đầu tiên trong 2 hoặc nhiều fragment (tức là nếu bit fragmented là 1). Một ID xác định duy nhất tất cả các fragment như thuộc về một thông điệp đơn (implementation hiện tại sử dụng I2NPMessageHeader.msg_id).

**Tùy chọn mở rộng** :: : 2 byte trở lên. Tùy chọn, có mặt nếu cờ tùy chọn mở rộng được đặt. Chưa được triển khai, không bao giờ có mặt; đặc tả gốc: Một byte độ dài và sau đó là nhiều byte tương ứng.

**size** :: : 2 byte. Độ dài của fragment theo sau. Giá trị hợp lệ: 1 đến khoảng 960 trong một tunnel message.

**Tổng chiều dài:** Chiều dài điển hình là: - 3 byte cho việc giao hàng LOCAL (tunnel message) - 35 byte cho việc giao hàng ROUTER hoặc 39 byte cho việc giao hàng TUNNEL (tunnel message không phân mảnh) - 39 byte cho việc giao hàng ROUTER hoặc 43 byte cho việc giao hàng TUNNEL (mảnh đầu tiên)

### Hướng Dẫn Giao Hàng Fragment Tiếp Theo

Nếu MSB của byte đầu tiên là 1, đây là một fragment tiếp theo, và các hướng dẫn là:

```
+----+----+----+----+----+----+----+
|frag|     Message ID    |  size   |
+----+----+----+----+----+----+----+
```
**frag** :: : 1 byte. Thứ tự bit: 76543210. Nhị phân 1nnnnnnd:   - bit 7: 1 để chỉ ra đây là một fragment tiếp theo   - bit 6-1: nnnnnn là số fragment 6 bit từ 1 đến 63   - bit 0: d là 1 để chỉ ra fragment cuối cùng, 0 nếu không phải

**Message ID** :: : 4 bytes. Xác định chuỗi fragment mà fragment này thuộc về. Giá trị này sẽ khớp với message ID của fragment ban đầu (một fragment có flag bit 7 được đặt thành 0 và flag bit 3 được đặt thành 1).

**size** :: : 2 byte. Độ dài của đoạn dữ liệu theo sau. Giá trị hợp lệ: 1 đến 996.

**Tổng độ dài: 7 byte**

## Ghi chú

### Kích thước tối đa của I2NP Message

Mặc dù kích thước tối đa của thông điệp I2NP danh nghĩa là 64 KB, kích thước này còn bị hạn chế thêm bởi phương pháp phân mảnh các thông điệp I2NP thành nhiều tunnel message 1 KB. Số lượng mảnh tối đa là 64, và mảnh đầu tiên có thể không được căn chỉnh hoàn hảo ở đầu tunnel message. Vì vậy thông điệp danh nghĩa phải vừa trong 63 mảnh.

Kích thước tối đa của một fragment ban đầu là 956 bytes (giả sử chế độ phân phối TUNNEL); kích thước tối đa của một fragment tiếp theo là 996 bytes. Do đó kích thước tối đa xấp xỉ 956 + (62 * 996) = 62708 bytes, hoặc 61.2 KB.

### Sắp xếp, Gộp lô, Đóng gói

Các tunnel message có thể bị drop hoặc sắp xếp lại thứ tự. Tunnel gateway, đơn vị tạo ra tunnel message, có quyền tự do triển khai bất kỳ chiến lược batching, mixing, hoặc sắp xếp lại thứ tự nào để phân mảnh các I2NP message và đóng gói hiệu quả các mảnh vào tunnel message. Nói chung, việc đóng gói tối ưu là không thể (vấn đề "packing problem"). Các gateway có thể triển khai nhiều chiến lược delay và sắp xếp lại thứ tự khác nhau.

### Cover Traffic

Các thông điệp tunnel có thể chỉ chứa padding (tức là không có hướng dẫn giao hàng hoặc các đoạn thông điệp nào cả) để tạo lưu lượng che giấu. Tính năng này chưa được triển khai.

## Tài liệu tham khảo

- **[I2NP]** [Giao thức I2NP](/docs/specs/i2np)
- **[I2NP-GC]** [GarlicClove](/docs/specs/i2np#garlicclove)
- **[I2NP-GCDI]** [GarlicCloveDeliveryInstructions](/docs/specs/i2np#garlicclovedeliveryinstructions)
- **[TUNNEL-IMPL]** [Triển khai Tunnel](/docs/specs/tunnel-implementation)
