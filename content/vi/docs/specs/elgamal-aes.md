---
title: "Mã hóa ElGamal/AES + SessionTag"
description: "Mã hóa đầu cuối đến cuối cũ kết hợp ElGamal, AES, SHA-256, và thẻ phiên một lần"
slug: "elgamal-aes"
aliases:
  - "/vi/how_elgamalaes"
  - "/vi/how_elgamalaes/"
lastUpdated: "2020-04"
accurateFor: "0.9.46"
---

## Tổng quan

ElGamal/AES+SessionTags được sử dụng cho mã hóa đầu cuối.

Là một hệ thống không đáng tin cậy, không có thứ tự, dựa trên tin nhắn, I2P sử dụng một sự kết hợp đơn giản của các thuật toán mã hóa bất đối xứng và đối xứng để cung cấp tính bảo mật và toàn vẹn dữ liệu cho các garlic messages. Nhìn chung, sự kết hợp này được gọi là ElGamal/AES+SessionTags, nhưng đó là một cách quá dài dòng để mô tả việc sử dụng ElGamal 2048bit, AES256, SHA256, và nonces 32 byte.

Lần đầu tiên một router muốn mã hóa một thông điệp garlic tới một router khác, họ mã hóa tài liệu khóa cho một session key AES256 bằng ElGamal và nối thêm payload được mã hóa AES256/CBC sau khối ElGamal đã mã hóa đó. Ngoài payload được mã hóa, phần được mã hóa AES chứa độ dài payload, hash SHA256 của payload chưa mã hóa, cũng như một số "session tags" - các nonce ngẫu nhiên 32 byte. Lần tiếp theo người gửi muốn mã hóa một thông điệp garlic tới một router khác, thay vì mã hóa ElGamal một session key mới, họ đơn giản chọn một trong các session tags đã gửi trước đó và mã hóa AES payload như trước, sử dụng session key đã dùng với session tag đó, được thêm vào đầu với chính session tag đó. Khi một router nhận được một thông điệp mã hóa garlic, họ kiểm tra 32 byte đầu tiên để xem có khớp với một session tag khả dụng hay không - nếu có, họ đơn giản giải mã AES thông điệp, nhưng nếu không, họ giải mã ElGamal khối đầu tiên.

Mỗi session tag chỉ có thể được sử dụng một lần để ngăn chặn các đối thủ nội bộ không cần thiết liên kết các thông điệp khác nhau như là giữa cùng các router. Người gửi thông điệp mã hóa ElGamal/AES+SessionTag quyết định khi nào và bao nhiêu tag để gửi, dự trữ cho người nhận đủ tag để bao phủ một loạt thông điệp. Các thông điệp garlic có thể phát hiện việc gửi tag thành công bằng cách gói một thông điệp bổ sung nhỏ như một clove (một "thông điệp trạng thái gửi") - khi thông điệp garlic đến được người nhận dự định và được giải mã thành công, thông điệp trạng thái gửi nhỏ này là một trong những clove được tiết lộ và có hướng dẫn cho người nhận gửi clove này trở lại cho người gửi ban đầu (thông qua một tunnel đầu vào, tất nhiên). Khi người gửi ban đầu nhận được thông điệp trạng thái gửi này, họ biết rằng các session tag được gói trong thông điệp garlic đã được gửi thành công.

Session tag bản thân có thời gian tồn tại ngắn, sau đó chúng sẽ bị loại bỏ nếu không được sử dụng. Ngoài ra, số lượng được lưu trữ cho mỗi khóa bị giới hạn, cũng như số lượng khóa - nếu có quá nhiều khóa đến, các tin nhắn mới hoặc cũ có thể bị loại bỏ. Người gửi theo dõi liệu các tin nhắn sử dụng session tag có được gửi đến hay không, và nếu không có đủ giao tiếp thì có thể loại bỏ những tin nhắn trước đó được giả định là đã gửi thành công, quay trở lại mã hóa ElGamal đầy đủ tốn kém. Một session sẽ tiếp tục tồn tại cho đến khi tất cả tag của nó bị cạn kiệt hoặc hết hạn.

Các phiên làm việc là một chiều. Các tag được gửi từ Alice đến Bob, và sau đó Alice sử dụng các tag này, từng cái một, trong các tin nhắn tiếp theo gửi đến Bob.

Các session có thể được thiết lập giữa các Destination, giữa các router, hoặc giữa một router và một Destination. Mỗi router và Destination duy trì Session Key Manager riêng của mình để theo dõi các Session Key và Session Tag. Các Session Key Manager riêng biệt ngăn chặn việc kẻ thù liên kết nhiều Destination với nhau hoặc với một router.

## Tiếp Nhận Tin Nhắn

Mỗi tin nhắn nhận được có một trong hai điều kiện có thể xảy ra:

1. Nó là một phần của session đã tồn tại và chứa Session Tag và một khối mã hóa AES
2. Nó dành cho session mới và chứa cả khối mã hóa ElGamal và AES

Khi một router nhận được một thông điệp, nó sẽ trước tiên giả định rằng thông điệp đó đến từ một phiên hiện có và cố gắng tra cứu Session Tag và giải mã dữ liệu sau đó bằng AES. Nếu thất bại, nó sẽ giả định rằng đó là cho một phiên mới và cố gắng giải mã bằng ElGamal.

## Đặc tả Thông báo Phiên mới {#new}

Một Thông điệp ElGamal Phiên mới chứa hai phần, một khối ElGamal được mã hóa và một khối AES được mã hóa.

Thông điệp được mã hóa chứa:

```
   +----+----+----+----+----+----+----+----+
   |                                       |
   +                                       +
   |       ElGamal Encrypted Block         |
   ~                                       ~
   |                                       |
   +         +----+----+----+----+----+----+
   |         |                             |
   +----+----+                             +
   |                                       |
   +                                       +
   |         AES Encrypted Block           |
   ~                                       ~
   |                                       |
   +         +----+----+----+----+----+----+
   |         +
   +----+----+
```
### ElGamal Block

Khối ElGamal được mã hóa luôn có độ dài 514 byte.

Dữ liệu ElGamal không mã hóa dài 222 byte, chứa:

```
   +----+----+----+----+----+----+----+----+
   |                                       |
   +                                       +
   |           Session Key                 |
   +                                       +
   |                                       |
   +                                       +
   |                                       |
   +----+----+----+----+----+----+----+----+
   |                                       |
   +                                       +
   |              Pre-IV                   |
   +                                       +
   |                                       |
   +                                       +
   |                                       |
   +----+----+----+----+----+----+----+----+
   +                                       +
   |                                       |
   +                                       +
   |       158 bytes random padding        |
   ~                                       ~
   |                                       |
   +                             +----+----+
   |                             |
   +----+----+----+----+----+----+
```
[Session Key](/docs/specs/common-structures#type_SessionKey) 32 byte là định danh cho phiên làm việc. Pre-IV 32 byte sẽ được sử dụng để tạo IV cho khối AES theo sau; IV là 16 byte đầu tiên của SHA-256 Hash của Pre-IV.

Payload 222 byte được mã hóa [sử dụng ElGamal](/docs/specs/cryptography#elgamal) và khối được mã hóa có độ dài 514 byte.

### AES Block {#aes}

Dữ liệu không mã hóa trong khối AES chứa những thông tin sau:

```
   +----+----+----+----+----+----+----+----+
   |tag count|                             |
   +----+----+                             +
   |                                       |
   +                                       +
   |          Session Tags                 |
   ~                                       ~
   |                                       |
   +                                       +
   |                                       |
   +         +----+----+----+----+----+----+
   |         |    payload size   |         |
   +----+----+----+----+----+----+         +
   |                                       |
   +                                       +
   |          Payload Hash                 |
   +                                       +
   |                                       |
   +                             +----+----+
   |                             |flag|    |
   +----+----+----+----+----+----+----+    +
   |                                       |
   +                                       +
   |          New Session Key (opt.)       |
   +                                       +
   |                                       |
   +                                  +----+
   |                                  |    |
   +----+----+----+----+----+----+----+    +
   |                                       |
   +                                       +
   |           Payload                     |
   ~                                       ~
   |                                       |
   +                        +----//---+----+
   |                        |              |
   +----+----+----//---+----+              +
   |          Padding to 16 bytes          |
   +----+----+----+----+----+----+----+----+
```
#### Định nghĩa

```
tag count:
    2-byte Integer, 0-200

Session Tags:
    That many 32-byte SessionTags

payload size:
    4-byte Integer

Payload Hash:
    The 32-byte SHA256 Hash of the payload

flag:
    A one-byte value. Normally == 0. If == 0x01, a Session Key follows

New Session Key:
    A 32-byte SessionKey,
    to replace the old key, and is only present if preceding flag is 0x01

Payload:
    the data

Padding:
    Random data to a multiple of 16 bytes for the total length.
    May contain more than the minimum required padding.
```
Độ dài tối thiểu: 48 byte

Dữ liệu sau đó được [Mã hóa AES](/docs/specs/cryptography), sử dụng khóa phiên và IV (được tính toán từ pre-IV) từ phần ElGamal. Độ dài khối AES được mã hóa có thể thay đổi nhưng luôn là bội số của 16 byte.

#### Ghi chú

- Độ dài payload tối đa thực tế và độ dài block tối đa là nhỏ hơn 64 KB; xem [Tổng quan I2NP](/docs/protocol/i2np).
- New Session Key hiện tại không được sử dụng và không bao giờ có mặt.

## Thông Số Kỹ Thuật Thông Điệp Phiên Hiện Tại {#existing}

Các session tags được gửi thành công sẽ được ghi nhớ trong một khoảng thời gian ngắn (hiện tại là 15 phút) cho đến khi chúng được sử dụng hoặc bị loại bỏ. Một tag được sử dụng bằng cách đóng gói nó trong một Existing Session Message chỉ chứa một khối mã hóa AES và không được đi trước bởi một khối ElGamal.

Thông điệp phiên hiện tại như sau:

```
   +----+----+----+----+----+----+----+----+
   |                                       |
   +                                       +
   |            Session Tag                |
   +                                       +
   |                                       |
   +                                       +
   |                                       |
   +----+----+----+----+----+----+----+----+
   |                                       |
   +                                       +
   |         AES Encrypted Block           |
   ~                                       ~
   |                                       |
   +                                       +
   |                                       |
   +----+----+----+----+----+----+----+----+
```
#### Định nghĩa

```
Session Tag:
    A 32-byte SessionTag
    previously delivered in an AES block

AES Encrypted Block:
    As specified above.
```
Session tag cũng đóng vai trò như pre-IV. IV là 16 byte đầu tiên của SHA-256 Hash của sessionTag.

Để giải mã một thông điệp từ phiên hiện có, router tìm kiếm Session Tag để tìm Session Key tương ứng. Nếu tìm thấy Session Tag, khối AES sẽ được giải mã bằng Session Key tương ứng. Nếu không tìm thấy tag, thông điệp được coi là một [New Session Message](#new).

## Tùy Chọn Cấu Hình Session Tag {#config}

Từ phiên bản 0.9.2, client có thể cấu hình số lượng Session Tags mặc định để gửi và ngưỡng tag thấp cho phiên hiện tại. Đối với các kết nối streaming ngắn hoặc datagram, các tùy chọn này có thể được sử dụng để giảm đáng kể băng thông. Xem [đặc tả tùy chọn I2CP](/docs/protocol/i2cp#options) để biết chi tiết. Các cài đặt phiên cũng có thể được ghi đè trên cơ sở từng tin nhắn. Xem [đặc tả I2CP Send Message Expires](/docs/specs/i2cp#msg_SendMessageExpires) để biết chi tiết.

## Công việc tương lai {#future}

**Lưu ý:** ElGamal/AES+SessionTags đang được thay thế bằng ECIES-X25519-AEAD-Ratchet (Đề xuất 144). Các vấn đề và ý tưởng được tham chiếu bên dưới đã được tích hợp vào thiết kế của giao thức mới. Các mục sau đây sẽ không được giải quyết trong ElGamal/AES+SessionTags.

Có nhiều lĩnh vực có thể điều chỉnh các thuật toán của Session Key Manager; một số có thể tương tác với hành vi của thư viện streaming, hoặc có tác động đáng kể đến hiệu suất tổng thể.

- Số lượng tag được gửi có thể phụ thuộc vào kích thước thông điệp, cần lưu ý việc padding cuối cùng lên 1KB ở lớp thông điệp tunnel.

- Các client có thể gửi ước tính thời gian tồn tại của phiên đến router, như một lời khuyên về số lượng tag cần thiết.

- Việc gửi quá ít tag sẽ khiến router phải quay lại sử dụng mã hóa ElGamal tốn kém.

- Router có thể giả định việc giao Session Tags, hoặc chờ xác nhận trước khi sử dụng chúng;
  có những đánh đổi cho mỗi chiến lược.

- Đối với các thông điệp rất ngắn, gần như toàn bộ 222 byte của các trường pre-IV và padding trong khối ElGamal có thể được sử dụng cho toàn bộ thông điệp, thay vì thiết lập một phiên.

- Đánh giá chiến lược padding; hiện tại chúng ta pad tối thiểu 128 bytes.
  Sẽ tốt hơn nếu thêm vài tag vào các tin nhắn nhỏ thay vì pad.

- Có lẽ mọi thứ có thể hiệu quả hơn nếu hệ thống Session Tag hoạt động hai chiều,
  để các tag được gửi trong đường 'thuận' có thể được sử dụng trong đường 'ngược',
  do đó tránh được ElGamal trong phản hồi ban đầu.
  Router hiện tại đã sử dụng một số thủ thuật như thế này khi gửi
  các thông điệp kiểm tra tunnel đến chính nó.

- Thay đổi từ Session Tags sang
  [một PRNG đồng bộ](/docs/overview/performance#future#prng).

- Một số ý tưởng này có thể yêu cầu loại thông điệp I2NP mới, hoặc
  đặt cờ trong
  [Delivery Instructions](/docs/specs/tunnel-message#struct_TunnelMessageDeliveryInstructions),
  hoặc đặt số magic trong vài byte đầu của trường Session Key
  và chấp nhận rủi ro nhỏ của việc Session Key ngẫu nhiên trùng với số magic.
