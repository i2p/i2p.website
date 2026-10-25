---
title: "SSU (Secure Semireliable UDP)"
description: "Đặc tả giao thức truyền tải UDP gốc (đã lỗi thời, được thay thế bởi SSU2)"
slug: "ssu"
aliases:
  - "/vi/docs/transport/ssu"
  - "/vi/docs/transport/ssu/"
  - "/vi/docs/transports/ssu"
  - "/vi/docs/transports/ssu/"
  - "/vi/docs/specs/ssu-spec"
  - "/vi/docs/specs/ssu-spec/"
category: "Giao thức vận chuyển"
lastUpdated: "2024-01"
accurateFor: "0.9.61"
---

## Tổng quan

ĐÃ NGỪNG SỬ DỤNG - SSU đã được thay thế bằng SSU2. Hỗ trợ SSU đã được loại bỏ khỏi i2pd trong phiên bản 2.44.0 (API 0.9.56) tháng 11/2022. Hỗ trợ SSU đã được loại bỏ khỏi Java I2P trong phiên bản 2.4.0 (API 0.9.61) tháng 12/2023.

Xem [tổng quan về SSU](/docs/transport/ssu/) để biết thêm thông tin.

## Trao đổi khóa DH {#dh}

Việc trao đổi khóa DH 2048-bit ban đầu được mô tả trên [trang SSU Keys](/docs/transport/ssu/#keys). Việc trao đổi này sử dụng cùng một số nguyên tố chung như được sử dụng cho [mã hóa ElGamal](/docs/specs/cryptography/#elgamal) của I2P.

## Tiêu đề Thông điệp {#header}

Tất cả các datagram UDP đều bắt đầu bằng một MAC (Message Authentication Code) 16 byte và một IV (Initialization Vector) 16 byte, tiếp theo là payload có kích thước biến đổi được mã hóa bằng khóa phù hợp. MAC được sử dụng là HMAC-MD5, được cắt ngắn thành 16 byte, trong khi khóa là một khóa AES256 đầy đủ 32 byte. Cấu trúc cụ thể của MAC là 16 byte đầu tiên từ:

```
HMAC-MD5(encryptedPayload + IV + (payloadLength ^ protocolVersion ^ ((netid - 2) << 8)), macKey)
```
trong đó '+' có nghĩa là nối thêm và '^' có nghĩa là phép XOR (loại trừ tuyệt đối).

IV được tạo ngẫu nhiên cho mỗi gói tin. encryptedPayload là phiên bản được mã hóa của thông điệp bắt đầu bằng flag byte (encrypt-then-MAC). payloadLength được sử dụng trong MAC là một số nguyên không dấu 2 byte, big endian. Lưu ý rằng protocolVersion là 0, vì vậy phép exclusive-or không có tác dụng gì. macKey có thể là introduction key hoặc được xây dựng từ DH key đã trao đổi (xem chi tiết bên dưới), như được chỉ định cho từng thông điệp dưới đây.

**CẢNH BÁO** - HMAC-MD5-128 được sử dụng ở đây không chuẩn, xem [chi tiết HMAC](/docs/specs/cryptography/#udp) để biết thêm thông tin.

Payload chính nó (tức là thông điệp bắt đầu với byte cờ) được mã hóa AES256/CBC với IV và sessionKey, với việc ngăn chặn tấn công replay được xử lý trong phần thân của nó, được giải thích bên dưới.

protocolVersion là một số nguyên không dấu 2 byte, big endian, và hiện tại được đặt thành 0. Các peer sử dụng phiên bản giao thức khác sẽ không thể giao tiếp với peer này, mặc dù các phiên bản trước đó không sử dụng cờ này vẫn có thể.

Phép toán XOR độc quyền của ((netid - 2) << 8) được sử dụng để nhanh chóng xác định các kết nối chéo mạng. netid là một số nguyên không dấu 2 byte, big endian, và hiện tại được đặt là 2. Kể từ phiên bản 0.9.42. Xem đề xuất 147 để biết thêm thông tin. Vì ID mạng hiện tại là 2, điều này không có tác dụng gì đối với mạng hiện tại và tương thích ngược. Bất kỳ kết nối nào từ các mạng thử nghiệm sẽ có ID khác và sẽ thất bại trong quá trình HMAC.

### Đặc tả HMAC

- Inner padding: 0x36...
- Outer padding: 0x5C...
- Key: 32 bytes
- Hash digest function: MD5, 16 bytes
- Block size: 64 bytes
- MAC size: 16 bytes
- Ví dụ triển khai C:
  - hmac.h trong [i2pd](https://github.com/PurpleI2P/i2pd)
  - I2PHMAC.cpp trong [i2pcpp](http://git.repo.i2p/w/i2pcpp.git)
- Ví dụ triển khai Java:
  - I2PHMac.java trong [I2P](https://github.com/i2p/i2p.i2p)

### Chi tiết Session Key

Khóa phiên 32 byte được tạo như sau:

1. Lấy khóa DH đã trao đổi, được biểu diễn dưới dạng mảng byte BigInteger có độ dài tối thiểu dương (two's complement big-endian)
2. Nếu bit quan trọng nhất là 1 (tức là array[0] & 0x80 != 0), thêm một byte 0x00 vào đầu, như trong biểu diễn BigInteger.toByteArray() của Java
3. Nếu mảng byte lớn hơn hoặc bằng 32 byte, sử dụng 32 byte đầu tiên (quan trọng nhất)
4. Nếu mảng byte nhỏ hơn 32 byte, thêm các byte 0x00 vào cuối để mở rộng thành 32 byte. *Rất khó xảy ra - Xem ghi chú bên dưới.*

### Chi tiết Khóa MAC

Khóa MAC 32-byte được tạo như sau:

1. Lấy mảng byte khóa DH đã trao đổi, có thể được thêm byte 0x00 ở đầu nếu
   cần thiết, từ bước 2 trong phần Chi tiết Khóa Phiên ở trên.
2. Nếu mảng byte đó lớn hơn hoặc bằng 64 byte, thì khóa MAC
   là các byte từ 33-64 trong mảng byte đó.
3. Nếu mảng byte đó nhỏ hơn 64 byte, thì khóa MAC là hash SHA-256
   của mảng byte đó. *Kể từ phiên bản 0.9.8. Xem ghi chú bên dưới.*

#### Lưu ý quan trọng

Code trước phiên bản 0.9.8 bị lỗi và không xử lý đúng mảng byte khóa DH từ 32 đến 63 byte (bước 3 và 4 ở trên) và kết nối sẽ thất bại. Vì những trường hợp này chưa bao giờ hoạt động, chúng đã được định nghĩa lại như mô tả ở trên cho phiên bản 0.9.8, và trường hợp 0-32 byte cũng được định nghĩa lại. Vì khóa DH trao đổi danh nghĩa là 256 byte, khả năng biểu diễn tối thiểu ít hơn 64 byte là cực kỳ nhỏ.

### Định dạng Header

Trong payload được mã hóa AES, có một cấu trúc chung tối thiểu cho các thông điệp khác nhau - một cờ một byte và một timestamp gửi bốn byte (số giây kể từ unix epoch).

Định dạng header là:

```
Header: 37+ bytes
  Encryption starts with the flag byte.
  +----+----+----+----+----+----+----+----+
  |                  MAC                  |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                   IV                  |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |flag|        time       |              |
  +----+----+----+----+----+              +
  | keying material (optional)            |
  +                                       +
  |                                       |
  ~                                       ~
  |                                       |
  +                        +----+----+----+
  |                        |#opt|         |
  +----+----+----+----+----+----+         +
  | #opt extended option bytes (optional) |
  ~                                       ~
  ~                                       ~
  +----+----+----+----+----+----+----+----+
```
Byte cờ chứa các trường bit sau:

```
Bit order: 76543210 (bit 7 is MSB)

  bits 7-4: payload type
     bit 3: If 1, rekey data is included. Always 0, unimplemented
     bit 2: If 1, extended options are included. Always 0 before release
            0.9.24.
  bits 1-0: reserved, set to 0 for compatibility with future uses
```
Không có rekeying và các tùy chọn mở rộng, kích thước header là 37 byte.

### Đổi khóa {#rekey}

Nếu cờ rekey được đặt, 64 byte dữ liệu khóa sẽ theo sau timestamp.

Khi thực hiện rekeying, 32 byte đầu tiên của keying material được đưa vào SHA256 để tạo ra MAC key mới, và 32 byte tiếp theo được đưa vào SHA256 để tạo ra session key mới, mặc dù các key này không được sử dụng ngay lập tức. Phía bên kia cũng nên phản hồi với rekey flag được thiết lập và cùng keying material đó. Một khi cả hai phía đã gửi và nhận được những giá trị đó, các key mới nên được sử dụng và các key trước đó bị loại bỏ. Có thể hữu ích khi giữ lại các key cũ trong thời gian ngắn để xử lý việc mất gói tin và sắp xếp lại thứ tự.

LƯU Ý: Rekeying hiện tại chưa được triển khai.

### Tùy chọn mở rộng {#extend}

Nếu cờ tùy chọn mở rộng được đặt, một giá trị kích thước tùy chọn một byte sẽ được thêm vào, theo sau là nhiều byte tùy chọn mở rộng tương ứng. Các tùy chọn mở rộng luôn là một phần của đặc tả, nhưng chưa được triển khai cho đến bản phát hành 0.9.24. Khi có mặt, định dạng tùy chọn sẽ cụ thể cho loại thông điệp. Xem tài liệu thông điệp bên dưới để biết liệu các tùy chọn mở rộng có được mong đợi cho thông điệp đã cho hay không, và định dạng được chỉ định. Mặc dù các router Java luôn nhận ra cờ và độ dài tùy chọn, các triển khai khác thì không. Do đó, không gửi các tùy chọn mở rộng đến các router cũ hơn bản phát hành 0.9.24.

## Đệm

Tất cả các thông điệp đều chứa 0 hoặc nhiều byte padding. Mỗi thông điệp phải được padding đến ranh giới 16 byte, như yêu cầu bởi [lớp mã hóa AES256](/docs/specs/cryptography/#AES).

Cho đến phiên bản 0.9.7, các thông điệp chỉ được đệm đến ranh giới 16 byte tiếp theo, và các thông điệp không phải bội số của 16 byte có thể không hợp lệ.

Từ phiên bản 0.9.7 trở đi, các thông điệp có thể được đệm đến bất kỳ độ dài nào miễn là MTU hiện tại được tuân thủ. Bất kỳ byte đệm bổ sung nào từ 1-15 byte vượt quá khối 16 byte cuối cùng sẽ không thể được mã hóa hoặc giải mã và sẽ bị bỏ qua. Tuy nhiên, toàn bộ độ dài và tất cả phần đệm đều được bao gồm trong tính toán MAC.

Kể từ phiên bản 0.9.8, các thông điệp được truyền không nhất thiết phải là bội số của 16 byte. Thông điệp SessionConfirmed là một ngoại lệ, xem bên dưới.

## Khóa

Chữ ký trong các thông điệp SessionCreated và SessionConfirmed được tạo ra bằng cách sử dụng [SigningPublicKey](/docs/specs/common-structures/#signingpublickey) từ [RouterIdentity](/docs/specs/common-structures/#routeridentity) được phân phối ngoài băng thông bằng cách xuất bản trong cơ sở dữ liệu mạng, và [SigningPrivateKey](/docs/specs/common-structures/#signingprivatekey) liên quan.

Qua phiên bản 0.9.15, thuật toán chữ ký luôn là DSA, với chữ ký 40 byte.

Kể từ phiên bản 0.9.16, thuật toán chữ ký có thể được chỉ định bởi một [KeyCertificate](/docs/specs/common-structures/#key-certificates) trong [RouterIdentity](/docs/specs/common-structures/#routeridentity) của Bob.

Cả introduction keys và session keys đều có độ dài 32 byte, và được định nghĩa theo đặc tả Common structures [SessionKey](/docs/specs/common-structures/#sessionkey). Khóa được sử dụng cho MAC và mã hóa sẽ được chỉ định cụ thể cho từng thông điệp bên dưới.

Introduction keys được chuyển giao thông qua một kênh bên ngoài (cơ sở dữ liệu mạng), nơi chúng theo truyền thống đã giống hệt với router Hash cho đến phiên bản 0.9.47, nhưng có thể là ngẫu nhiên kể từ phiên bản 0.9.48.

## Ghi chú

### IPv6

Đặc tả giao thức cho phép cả địa chỉ IPv4 4-byte và địa chỉ IPv6 16-byte. SSU-over-IPv6 được hỗ trợ từ phiên bản 0.9.8. Xem tài liệu của từng thông điệp bên dưới để biết chi tiết về hỗ trợ IPv6.

### Dấu thời gian {#time}

Trong khi hầu hết I2P sử dụng dấu thời gian [Date](/docs/specs/common-structures/#date) 8 byte với độ phân giải mili giây, SSU sử dụng dấu thời gian số nguyên không dấu 4 byte với độ phân giải một giây. Vì các giá trị này không có dấu, chúng sẽ không quay vòng lại cho đến tháng 2 năm 2106.

## Tin nhắn

Có 10 thông điệp (loại payload) được định nghĩa:

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Message</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Notes</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#sessionrequest">SessionRequest</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#sessioncreated">SessionCreated</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#sessionconfirmed">SessionConfirmed</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#relayrequest">RelayRequest</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#relayresponse">RelayResponse</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#relayintro">RelayIntro</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">6</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#data">Data</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#peertest">PeerTest</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">8</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#sessiondestroyed">SessionDestroyed</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Implemented as of 0.8.9</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">n/a</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#holepunch">HolePunch</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
</table>
### SessionRequest (loại 0) {#sessionrequest}

Đây là thông điệp đầu tiên được gửi để thiết lập một phiên kết nối.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Peer:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice to Bob</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Data:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">256 byte X, to begin the DH agreement; 1 byte IP address size; that many bytes representation of Bob's IP address; N bytes, currently uninterpreted</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Crypto Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob's introKey, as retrieved from the network database</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>MAC Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob's introKey, as retrieved from the network database</td>
</tr>
</table>
Định dạng thông điệp:

```
+----+----+----+----+----+----+----+----+
|         X, as calculated from DH      |
~                .  .  .                ~
|                                       |
+----+----+----+----+----+----+----+----+
|size| that many byte IP address (4-16) |
+----+----+----+----+----+----+----+----+
| arbitrary amount of uninterpreted data|
~                .  .  .                ~
```
Kích thước điển hình bao gồm header, trong triển khai hiện tại: 304 (IPv4) hoặc 320 (IPv6) byte (trước khi padding non-mod-16)

#### Tùy chọn mở rộng

Lưu ý: Đã được triển khai trong phiên bản 0.9.24.

- Độ dài tối thiểu: 3 (byte độ dài tùy chọn + 2 byte)
- Độ dài tùy chọn: tối thiểu 2
- 2 byte cờ:

```
Bit order: 15...76543210 (bit 15 is MSB)

      bit 0: 1 for Alice to request a relay tag from Bob in the
             SessionCreated response, 0 if Alice does not need a relay tag.
             Note that "1" is the default if no extended options are present
  bits 15-1: unused, set to 0 for compatibility with future uses
```
#### Ghi chú

- Địa chỉ IPv4 và IPv6 được hỗ trợ.
- Dữ liệu không được diễn giải có thể được sử dụng trong tương lai cho các thử thách.

### SessionCreated (loại 1) {#sessioncreated}

Đây là phản hồi cho một [SessionRequest](#sessionrequest).

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Peer:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob to Alice</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Data:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">256 byte Y, to complete the DH agreement; 1 byte IP address size; that many bytes representation of Alice's IP address; 2 byte Alice's port number; 4 byte relay (introduction) tag which Alice can publish (else 0x00000000); 4 byte timestamp (seconds from the epoch) for use in the DSA signature; Bob's <a href="/docs/specs/common-structures/#signature">Signature</a> of the critical exchanged data (X + Y + Alice's IP + Alice's port + Bob's IP + Bob's port + Alice's new relay tag + Bob's signed on time), encrypted with another layer of encryption using the negotiated sessionKey. The IV is reused here. See notes for length information.; 0-15 bytes of padding of the signature, using random data, to a multiple of 16 bytes, so that the signature + padding may be encrypted with an additional layer of encryption using the negotiated session key as part of the DSA block.; N bytes, currently uninterpreted</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Crypto Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob's introKey, with an additional layer of encryption over the 40 byte signature and the following 8 bytes padding.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>MAC Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob's introKey</td>
</tr>
</table>
Định dạng tin nhắn:

```
+----+----+----+----+----+----+----+----+
|         Y, as calculated from DH      |
~                .  .  .                ~
|                                       |
+----+----+----+----+----+----+----+----+
|size| that many byte IP address (4-16) |
+----+----+----+----+----+----+----+----+
| Port (A)| public relay tag  |  signed
+----+----+----+----+----+----+----+----+
  on time |                             |
+----+----+                             +
|                                       |
+                                       +
|             signature                 |
+                                       +
|                                       |
+                                       +
|                                       |
+         +----+----+----+----+----+----+
|         |   (0-15 bytes of padding) 
+----+----+----+----+----+----+----+----+
          |                             |
+----+----+                             +
|           arbitrary amount            |
~        of uninterpreted data          ~
~                .  .  .                ~
```
Kích thước thông thường bao gồm header, trong triển khai hiện tại: 368 bytes (IPv4 hoặc IPv6) (trước khi padding non-mod-16)

#### Ghi chú

- Địa chỉ IPv4 và IPv6 đều được hỗ trợ.
- Nếu thẻ relay khác không, Bob đang đề xuất hoạt động như một introducer cho
  Alice. Alice có thể sau đó công bố địa chỉ của Bob và thẻ relay trong cơ sở
  dữ liệu mạng.
- Đối với chữ ký, Bob phải sử dụng cổng bên ngoài của mình, vì đó là những gì Alice sẽ
  sử dụng để xác minh. Nếu NAT/firewall của Bob đã ánh xạ cổng nội bộ của anh ta sang một
  cổng bên ngoài khác, và Bob không biết về điều đó, việc xác minh bởi Alice
  sẽ thất bại.
- Xem phần [Keys](#keys) ở trên để biết chi tiết về chữ ký. Alice đã có
  khóa ký công khai của Bob, từ cơ sở dữ liệu mạng.
- Thông qua phiên bản 0.9.15, chữ ký luôn là chữ ký DSA 40 byte và
  phần đệm luôn là 8 byte. Kể từ phiên bản 0.9.16, loại chữ ký và
  độ dài được ngụ ý bởi loại [SigningPublicKey](/docs/specs/common-structures/#signingpublickey) trong
  [RouterIdentity](/docs/specs/common-structures/#routeridentity) của Bob. Phần đệm là cần thiết để đạt bội số của 16 byte.
- Đây là thông báo duy nhất sử dụng khóa intro của người gửi. Tất cả những thông báo khác sử dụng
  khóa intro của người nhận hoặc khóa phiên đã thiết lập.
- Thời gian signed-on dường như không được sử dụng hoặc không được xác minh trong
  triển khai hiện tại.
- Dữ liệu chưa được diễn giải có thể được sử dụng trong tương lai cho các thách thức.
- Tùy chọn mở rộng trong header: Không được mong đợi, không được xác định.

### SessionConfirmed (loại 2) {#sessionconfirmed}

Đây là phản hồi cho thông điệp [SessionCreated](#sessioncreated) và là bước cuối cùng trong việc thiết lập một phiên. Có thể cần nhiều thông điệp SessionConfirmed nếu Router Identity phải được phân mảnh.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Peer:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice to Bob</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Data:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1 byte identity fragment info (bits 7-4: current identity fragment # 0-14; bits 3-0: total identity fragments (F) 1-15); 2 byte size of the current identity fragment; that many byte fragment of Alice's <a href="/docs/specs/common-structures/#routeridentity">RouterIdentity</a>; After the last identity fragment only: 4 byte signed-on time; N bytes padding, currently uninterpreted; After the last identity fragment only: The remaining bytes contain Alice's <a href="/docs/specs/common-structures/#signature">Signature</a> of the critical exchanged data (X + Y + Alice's IP + Alice's port + Bob's IP + Bob's port + Alice's new relay tag + Alice's signed on time). See notes for length information.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Crypto Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice/Bob sessionKey, as generated from the DH exchange</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>MAC Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice/Bob MAC Key, as generated from the DH exchange</td>
</tr>
</table>
**Fragment 0 đến F-2** (chỉ khi F > 1; hiện không sử dụng, xem ghi chú bên dưới):

```
+----+----+----+----+----+----+----+----+
|info| cursize |                        |
+----+----+----+                        +
|      fragment of Alice's full         |
~            Router Identity            ~
~                .  .  .                ~
|                                       |
+----+----+----+----+----+----+----+----+
| arbitrary amount of uninterpreted data|
~                .  .  .                ~
```
**Fragment F-1 (fragment cuối cùng hoặc duy nhất):**

```
+----+----+----+----+----+----+----+----+
|info| cursize |                        |
+----+----+----+                        +
|     last fragment of Alice's full     |
~            Router Identity            ~
~                .  .  .                ~
|                                       |
+----+----+----+----+----+----+----+----+
|  signed on time   |                   |
+----+----+----+----+                   +
|  arbitrary amount of uninterpreted    |
~      data, until the signature at     ~
~       end of the current packet       ~
|  Packet length must be mult. of 16    |
+----+----+----+----+----+----+----+----+
+                                       +
|                                       |
+                                       +
|             signature                 |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
```
Kích thước điển hình bao gồm header, trong triển khai hiện tại: 512 byte (với chữ ký Ed25519) hoặc 480 byte (với chữ ký DSA-SHA1) (trước khi padding non-mod-16)

#### Ghi chú

- Trong triển khai hiện tại, kích thước fragment tối đa là 512 byte. Điều này
  cần được mở rộng để các chữ ký dài hơn có thể hoạt động mà không cần phân mảnh.
  Triển khai hiện tại không xử lý đúng các chữ ký được chia thành
  hai fragment.
- [RouterIdentity](/docs/specs/common-structures/#routeridentity) điển hình có kích thước 387 byte, nên không bao giờ
  cần phân mảnh. Nếu mật mã mới mở rộng kích thước của RouterIdentity, thì
  sơ đồ phân mảnh phải được kiểm tra cẩn thận.
- Không có cơ chế để yêu cầu hoặc gửi lại các fragment bị thiếu.
- Trường tổng số fragment F phải được thiết lập giống hệt nhau trong tất cả các fragment.
- Xem phần [Keys](#keys) ở trên để biết chi tiết về chữ ký DSA.
- Thời gian ký có vẻ không được sử dụng hoặc không được xác minh trong triển khai
  hiện tại.
- Do chữ ký ở cuối, phần padding trong packet cuối cùng hoặc duy nhất
  phải đệm tổng packet thành bội số của 16 byte, nếu không chữ ký sẽ
  không được giải mã đúng. Điều này khác với tất cả các loại message
  khác, nơi padding ở cuối.
- Đến phiên bản 0.9.15, chữ ký luôn là chữ ký DSA 40 byte. Từ
  phiên bản 0.9.16, loại và độ dài chữ ký được ngụ ý bởi loại của
  [SigningPublicKey](/docs/specs/common-structures/#signingpublickey) trong [RouterIdentity](/docs/specs/common-structures/#routeridentity) của Alice. Padding được thực hiện
  cần thiết để thành bội số của 16 byte.
- Tùy chọn mở rộng trong header: Không mong đợi, không xác định.

### SessionDestroyed (loại 8) {#sessiondestroyed}

Thông điệp SessionDestroyed đã được triển khai (chỉ nhận) trong phiên bản 0.8.1, và được gửi từ phiên bản 0.8.9.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Peer:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice to Bob or Bob to Alice</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Data:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">none</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Crypto Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice/Bob sessionKey</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>MAC Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice/Bob MAC Key</td>
</tr>
</table>
Thông điệp này không chứa bất kỳ dữ liệu nào. Kích thước điển hình bao gồm header, trong triển khai hiện tại: 48 bytes (trước khi padding non-mod-16)

#### Ghi chú

- Tin nhắn hủy nhận được với intro key của người gửi hoặc người nhận sẽ bị
  bỏ qua.
- Tùy chọn mở rộng trong header: Không mong đợi, không xác định.

### RelayRequest (loại 3) {#relayrequest}

Đây là thông điệp đầu tiên được gửi từ Alice tới Bob để yêu cầu giới thiệu với Charlie.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Peer:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice to Bob</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Data:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4 byte relay (introduction) tag, nonzero, as received by Alice in the SessionCreated message from Bob; 1 byte IP address size; that many byte representation of Alice's IP address; 2 byte port number (of Alice); 1 byte challenge size; that many bytes to be relayed to Charlie in the intro; Alice's 32-byte introduction key (so Bob can reply with Charlie's info); 4 byte nonce of Alice's relay request; N bytes, currently uninterpreted</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Crypto Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob's introKey, as retrieved from the network database (or Alice/Bob sessionKey, if established)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>MAC Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob's introKey, as retrieved from the network database (or Alice/Bob MAC Key, if established)</td>
</tr>
</table>
Định dạng thông điệp:

```
+----+----+----+----+----+----+----+----+
|      relay tag    |size| Alice IP addr
+----+----+----+----+----+----+----+----+
     | Port (A)|size| challenge bytes   |
+----+----+----+----+                   +
|      to be delivered to Charlie       |
+----+----+----+----+----+----+----+----+
| Alice's intro key                     |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|       nonce       |                   |
+----+----+----+----+                   +
| arbitrary amount of uninterpreted data|
~                .  .  .                ~
```
Kích thước điển hình bao gồm header, trong triển khai hiện tại: 96 byte (không bao gồm Alice IP) hoặc 112 byte (bao gồm Alice IP 4-byte) (trước khi padding non-mod-16)

#### Ghi chú

- Địa chỉ IP chỉ được bao gồm nếu nó khác với địa chỉ nguồn và cổng của gói tin.
- Thông điệp này có thể được gửi qua IPv4 hoặc IPv6.
  Nếu thông điệp được gửi qua IPv6 cho một introduction IPv4,
  hoặc (kể từ phiên bản 0.9.50) qua IPv4 cho một introduction IPv6,
  Alice phải bao gồm địa chỉ và cổng introduction của mình.
  Điều này được hỗ trợ kể từ phiên bản 0.9.50.
- Nếu Alice bao gồm địa chỉ/cổng của mình, Bob có thể thực hiện xác thực bổ sung
  trước khi tiếp tục.
  - Trước phiên bản 0.9.24, Java I2P từ chối bất kỳ địa chỉ hoặc cổng nào khác
    với kết nối.
- Challenge chưa được triển khai, kích thước challenge luôn bằng không
- Relaying cho IPv6 được hỗ trợ kể từ phiên bản 0.9.50.
- Trước phiên bản 0.9.12, intro key của Bob luôn được sử dụng. Kể từ phiên bản
  0.9.12, session key được sử dụng nếu có một phiên làm việc đã được thiết lập giữa
  Alice và Bob. Trên thực tế, phải có một phiên làm việc đã được thiết lập, vì Alice
  chỉ sẽ nhận được nonce (introduction tag) từ thông điệp tạo phiên làm việc,
  và Bob sẽ đánh dấu introduction tag không hợp lệ khi phiên làm việc bị hủy.
- Tùy chọn mở rộng trong header: Không được mong đợi, chưa được định nghĩa.

### RelayResponse (loại 4) {#relayresponse}

Đây là phản hồi cho một [RelayRequest](#relayrequest) và được gửi từ Bob đến Alice.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Peer:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob to Alice</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Data:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1 byte IP address size; that many byte representation of Charlie's IP address; 2 byte Charlie's port number; 1 byte IP address size; that many byte representation of Alice's IP address; 2 byte Alice's port number; 4 byte nonce sent by Alice; N bytes, currently uninterpreted</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Crypto Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice's introKey, as received in the Relay Request (or Alice/Bob sessionKey, if established)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>MAC Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice's introKey, as received in the Relay Request (or Alice/Bob MAC Key, if established)</td>
</tr>
</table>
Định dạng thông điệp:

```
+----+----+----+----+----+----+----+----+
|size|    Charlie IP     | Port (C)|size|
+----+----+----+----+----+----+----+----+
|    Alice IP       | Port (A)|  nonce
+----+----+----+----+----+----+----+----+
          |   arbitrary amount of       |
+----+----+                             +
|          uninterpreted data           |
~                .  .  .                ~
```
Kích thước điển hình bao gồm header, trong triển khai hiện tại: 64 (Alice IPv4) hoặc 80 (Alice IPv6) bytes (trước khi padding không chia hết cho 16)

#### Ghi chú

- Thông điệp này có thể được gửi qua IPv4 hoặc IPv6.
- Địa chỉ IP/cổng của Alice là địa chỉ IP/cổng rõ ràng mà Bob đã nhận được
  RelayRequest (không nhất thiết là IP mà Alice đã bao gồm trong RelayRequest),
  và có thể là IPv4 hoặc IPv6. Alice hiện tại bỏ qua những thông tin này khi nhận.
- Địa chỉ IP của Charlie có thể là IPv4, hoặc từ phiên bản 0.9.50 trở đi, là IPv6,
  vì đó là địa chỉ mà Alice sẽ
  gửi SessionRequest đến sau Hole Punch.
- Relaying cho IPv6 được hỗ trợ từ phiên bản 0.9.50.
- Trước phiên bản 0.9.12, intro key của Alice luôn được sử dụng. Từ phiên bản
  0.9.12 trở đi, session key được sử dụng nếu có một phiên kết nối đã được thiết lập giữa
  Alice và Bob.
- Các tùy chọn mở rộng trong header: Không được mong đợi, chưa được định nghĩa.

### RelayIntro (loại 5) {#relayintro}

Đây là phần giới thiệu cho Alice, được gửi từ Bob đến Charlie.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Peer:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob to Charlie</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Data:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1 byte IP address size; that many byte representation of Alice's IP address; 2 byte port number (of Alice); 1 byte challenge size; that many bytes relayed from Alice; N bytes, currently uninterpreted</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Crypto Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob/Charlie sessionKey</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>MAC Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob/Charlie MAC Key</td>
</tr>
</table>
Định dạng thông điệp:

```
+----+----+----+----+----+----+----+----+
|size|     Alice IP      | Port (A)|size|
+----+----+----+----+----+----+----+----+
|      that many bytes of challenge     |
+                                       +
|        data relayed from Alice        |
+----+----+----+----+----+----+----+----+
| arbitrary amount of uninterpreted data|
~                .  .  .                ~
```
Kích thước điển hình bao gồm header, trong triển khai hiện tại: 48 byte (trước khi padding không chia hết cho 16)

#### Ghi chú

- Đối với IPv4, địa chỉ IP của Alice luôn là 4 byte, vì Alice đang cố gắng kết nối với Charlie qua IPv4.
  Từ phiên bản 0.9.50, IPv6 được hỗ trợ, và địa chỉ IP của Alice có thể là 16 byte.
- Đối với IPv4, thông điệp này phải được gửi qua một kết nối IPv4 đã thiết lập,
  vì đây là cách duy nhất để Bob biết địa chỉ IPv4 của Charlie để trả về cho Alice trong RelayResponse.
  Từ phiên bản 0.9.50, IPv6 được hỗ trợ, và thông điệp này có thể được gửi qua một kết nối IPv6 đã thiết lập.
- Từ phiên bản 0.9.50, bất kỳ địa chỉ SSU nào được công bố với introducer phải chứa "4" hoặc "6" trong tùy chọn "caps".
- Challenge chưa được triển khai, kích thước challenge luôn bằng không
- Tùy chọn mở rộng trong header: Không được mong đợi, không được định nghĩa.

### Dữ liệu (loại 6) {#data}

Thông điệp này được sử dụng để vận chuyển dữ liệu và xác nhận.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Peer:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Any</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Crypto Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice/Bob sessionKey</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>MAC Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice/Bob MAC Key</td>
</tr>
</table>
**Dữ liệu:** 1 byte flags (xem bên dưới); nếu explicit ACKs được bao gồm: 1 byte số lượng ACKs, bấy nhiêu MessageIds 4 byte được ACK đầy đủ; nếu ACK bitfields được bao gồm: 1 byte số lượng ACK bitfields, bấy nhiêu MessageIds 4 byte + 1 hoặc nhiều byte ACK bitfield (xem ghi chú); Nếu extended data được bao gồm: 1 byte kích thước dữ liệu, bấy nhiêu byte extended data (hiện tại chưa được diễn giải); 1 byte số lượng fragments (có thể bằng không); Nếu khác không, bấy nhiêu message fragments.

```
Flags byte:
  Bit order: 76543210 (bit 7 is MSB)
  bit 7: explicit ACKs included
  bit 6: ACK bitfields included
  bit 5: reserved
  bit 4: explicit congestion notification (ECN)
  bit 3: request previous ACKs
  bit 2: want reply
  bit 1: extended data included (unused, never set)
  bit 0: reserved
```
Mỗi fragment chứa: - 4 byte messageId - 3 byte thông tin fragment:   - bits 23-17: fragment # 0 - 127   - bit 16: isLast (1 = true)   - bits 15-14: không sử dụng, đặt về 0 để tương thích với các mục đích sử dụng trong tương lai   - bits 13-0: kích thước fragment 0 - 16383 - nhiều byte dữ liệu fragment như vậy

Định dạng tin nhắn:

```
+----+----+----+----+----+----+----+----+
|flag| (additional headers, determined  |
+----+                                  +
~ by the flags, such as ACKs or         ~
| bitfields                             |
+----+----+----+----+----+----+----+----+
|#frg|     messageId     |   frag info  |
+----+----+----+----+----+----+----+----+
| that many bytes of fragment data      |
~                .  .  .                ~
|                                       |
+----+----+----+----+----+----+----+----+
|     messageId     |   frag info  |    |
+----+----+----+----+----+----+----+    +
| that many bytes of fragment data      |
~                .  .  .                ~
|                                       |
+----+----+----+----+----+----+----+----+
|     messageId     |   frag info  |    |
+----+----+----+----+----+----+----+    +
| that many bytes of fragment data      |
~                .  .  .                ~
|                                       |
+----+----+----+----+----+----+----+----+
| arbitrary amount of uninterpreted data|
~                .  .  .                ~
```
#### Ghi chú về Bitfield ACK

Bitfield sử dụng 7 bit thấp của mỗi byte, với bit cao chỉ định liệu có byte bitfield bổ sung nào theo sau nó hay không (1 = có, 0 = byte bitfield hiện tại là byte cuối cùng). Chuỗi các mảng 7 bit này biểu thị liệu một fragment đã được nhận hay chưa - nếu một bit là 1, fragment đã được nhận. Để làm rõ, giả sử các fragment 0, 2, 5, và 9 đã được nhận, các byte bitfield sẽ như sau:

```
byte 0:
   Bit order: 76543210 (bit 7 is MSB)
   bit 7: 1 (further bitfield bytes follow)
   bit 6: 0 (fragment 6 not received)
   bit 5: 1 (fragment 5 received)
   bit 4: 0 (fragment 4 not received)
   bit 3: 0 (fragment 3 not received)
   bit 2: 1 (fragment 2 received)
   bit 1: 0 (fragment 1 not received)
   bit 0: 1 (fragment 0 received)
byte 1:
   Bit order: 76543210 (bit 7 is MSB)
   bit 7: 0 (no further bitfield bytes)
   bit 6: 0 (fragment 13 not received)
   bit 5: 0 (fragment 12 not received)
   bit 4: 0 (fragment 11 not received)
   bit 3: 0 (fragment 10 not received)
   bit 2: 1 (fragment 9 received)
   bit 1: 0 (fragment 8 not received)
   bit 0: 0 (fragment 7 not received)
```
#### Ghi chú

- Triển khai hiện tại thêm một số lượng hạn chế các ack trùng lặp cho các thông điệp đã được ack trước đó, nếu có không gian khả dụng.
- Nếu số lượng fragment là zero, đây là thông điệp chỉ ack hoặc keepalive.
- Tính năng ECN chưa được triển khai, và bit này không bao giờ được đặt.
- Trong triển khai hiện tại, bit want reply được đặt khi số lượng fragment lớn hơn zero, và không được đặt khi không có fragment.
- Extended data chưa được triển khai và không bao giờ có mặt.
- Việc nhận nhiều fragment được hỗ trợ trong tất cả các bản phát hành. Việc truyền nhiều fragment được triển khai trong bản phát hành 0.9.16.
- Như được triển khai hiện tại, tối đa fragment là 64 (số fragment tối đa = 63).
- Như được triển khai hiện tại, kích thước fragment tối đa tất nhiên nhỏ hơn MTU.
- Hãy cẩn thận không vượt quá MTU tối đa ngay cả khi có một số lượng lớn ACK cần gửi.
- Giao thức cho phép fragment có độ dài zero nhưng không có lý do gì để gửi chúng.
- Trong SSU, dữ liệu sử dụng header I2NP ngắn 5-byte theo sau bởi payload của thông điệp I2NP thay vì header I2NP tiêu chuẩn 16-byte. Header I2NP ngắn chỉ bao gồm loại I2NP một byte và thời gian hết hạn 4-byte tính bằng giây. Message ID của I2NP được sử dụng làm message ID cho fragment. Kích thước I2NP được lắp ráp từ các kích thước fragment. Checksum I2NP không cần thiết vì tính toàn vẹn của thông điệp UDP được đảm bảo bằng giải mã.
- Message ID không phải là số thứ tự và không liên tiếp. SSU không đảm bảo việc giao hàng theo thứ tự. Mặc dù chúng ta sử dụng message ID của I2NP làm message ID của SSU, từ góc độ giao thức SSU, chúng là các số ngẫu nhiên. Thực tế, vì router sử dụng một Bloom filter duy nhất cho tất cả các peer, message ID phải là một số ngẫu nhiên thực sự.
- Vì không có số thứ tự, không có cách nào để chắc chắn một ACK đã được nhận. Triển khai hiện tại thường xuyên gửi một lượng lớn ACK trùng lặp. ACK trùng lặp không nên được coi là dấu hiệu của tắc nghẽn.
- Ghi chú về ACK Bitfield: Người nhận gói data không biết có bao nhiêu fragment trong thông điệp trừ khi nó đã nhận được fragment cuối cùng. Do đó, số byte bitfield được gửi để phản hồi có thể ít hơn hoặc nhiều hơn số fragment chia cho 7. Ví dụ, nếu fragment cao nhất mà người nhận đã thấy là số 4, chỉ cần gửi một byte, ngay cả khi có thể có tổng cộng 13 fragment. Có thể bao gồm tối đa 10 byte (tức là (64 / 7) + 1) cho mỗi message ID được ack.
- Tùy chọn mở rộng trong header: Không mong đợi, không xác định.

### PeerTest (type 7) {#peertest}

Xem [SSU Peer Testing](/docs/transport/ssu/#peerTesting) để biết chi tiết. Lưu ý: Kiểm thử peer IPv6 được hỗ trợ từ phiên bản 0.9.27.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Peer:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Any</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Data:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4 byte nonce; 1 byte IP address size (may be zero); that many byte representation of Alice's IP address, if size > 0; 2 byte Alice's port number; Alice's or Charlie's 32-byte introduction key; N bytes, currently uninterpreted</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Crypto Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">See notes below</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>MAC Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">See notes below</td>
</tr>
</table>
Khóa mật mã được sử dụng (liệt kê theo thứ tự xuất hiện): 1. Khi gửi từ Alice đến Bob: Alice/Bob sessionKey 2. Khi gửi từ Bob đến Charlie: Bob/Charlie sessionKey 3. Khi gửi từ Charlie đến Bob: Bob/Charlie sessionKey 4. Khi gửi từ Bob đến Alice: Alice/Bob sessionKey (hoặc đối với Bob trước phiên bản 0.9.52, Alice's introKey) 5. Khi gửi từ Charlie đến Alice: Alice's introKey, như đã nhận trong thông điệp PeerTest từ Bob 6. Khi gửi từ Alice đến Charlie: Charlie's introKey, như đã nhận trong thông điệp PeerTest từ Charlie

MAC Key được sử dụng (liệt kê theo thứ tự xuất hiện): 1. Khi gửi từ Alice đến Bob: Alice/Bob MAC Key 2. Khi gửi từ Bob đến Charlie: Bob/Charlie MAC Key 3. Khi gửi từ Charlie đến Bob: Bob/Charlie MAC Key 4. Khi gửi từ Bob đến Alice: introKey của Alice, như đã nhận trong thông điệp PeerTest từ Alice 5. Khi gửi từ Charlie đến Alice: introKey của Alice, như đã nhận trong thông điệp PeerTest từ Bob 6. Khi gửi từ Alice đến Charlie: introKey của Charlie, như đã nhận trong thông điệp PeerTest từ Charlie

Định dạng thông điệp:

```
+----+----+----+----+----+----+----+----+
|    test nonce     |size| Alice IP addr
+----+----+----+----+----+----+----+----+
     | Port (A)|                        |
+----+----+----+                        +
| Alice or Charlie's                    |
+ introduction key (Alice's is sent to  +
| Bob and Charlie, while Charlie's is   |
+ sent to Alice)                        +
|                                       |
+              +----+----+----+----+----+
|              | arbitrary amount of    |
+----+----+----+                        |
| uninterpreted data                    |
~                .  .  .                ~
```
Kích thước thông thường bao gồm header, trong triển khai hiện tại: 80 bytes (trước khi padding non-mod-16)

#### Ghi chú

- Khi được gửi bởi Alice, kích thước địa chỉ IP là 0, địa chỉ IP không có mặt, và port
  là 0, vì Bob và Charlie không sử dụng dữ liệu này; mục đích là để xác định
  địa chỉ IP/port thực sự của Alice và thông báo cho Alice; Bob và Charlie không quan tâm
  Alice nghĩ địa chỉ của cô ấy là gì.
- Khi được gửi bởi Bob hoặc Charlie, IP và port có mặt, và địa chỉ IP có
  4 hoặc 16 byte. Kiểm tra IPv6 được hỗ trợ từ phiên bản 0.9.27.
- Khi được gửi bởi Charlie tới Alice, IP và port như sau:
  Lần đầu tiên (thông điệp 5): IP và port được yêu cầu của Alice như đã nhận trong thông điệp 2.
  Lần thứ hai (thông điệp 7): IP và port thực tế của Alice mà thông điệp 6 được nhận từ đó.
- Ghi chú IPv6: Qua phiên bản 0.9.26, chỉ hỗ trợ kiểm tra địa chỉ IPv4. Do đó, tất cả
  giao tiếp Alice-Bob và Alice-Charlie phải qua IPv4. Tuy nhiên, giao tiếp Bob-Charlie
  có thể qua IPv4 hoặc IPv6. Địa chỉ của Alice, khi
  được chỉ định trong thông điệp PeerTest, phải có 4 byte.
  Từ phiên bản 0.9.27, việc kiểm tra địa chỉ IPv6 được hỗ trợ,
  và giao tiếp Alice-Bob và Alice-Charlie có thể qua IPv6,
  nếu Bob và Charlie chỉ ra hỗ trợ với khả năng 'B' trong địa chỉ IPv6 được công bố của họ.
  Xem Đề xuất 126 để biết chi tiết.
- Alice gửi yêu cầu tới Bob sử dụng phiên hiện có qua transport (IPv4 hoặc IPv6) mà cô ấy muốn kiểm tra.
  Khi Bob nhận yêu cầu từ Alice qua IPv4, Bob phải chọn một Charlie quảng cáo địa chỉ IPv4.
  Khi Bob nhận yêu cầu từ Alice qua IPv6, Bob phải chọn một Charlie quảng cáo địa chỉ IPv6.
  Giao tiếp Bob-Charlie thực tế có thể qua IPv4 hoặc IPv6 (tức là, độc lập với loại địa chỉ của Alice).
- Một peer phải duy trì bảng các trạng thái kiểm tra đang hoạt động (nonces). Khi nhận
  thông điệp PeerTest, tra cứu nonce trong bảng. Nếu tìm thấy, đây là
  kiểm tra hiện có và bạn biết vai trò của mình (Alice, Bob, hoặc Charlie). Ngược lại, nếu
  IP không có mặt và port là 0, đây là kiểm tra mới và bạn là Bob.
  Ngược lại, đây là kiểm tra mới và bạn là Charlie.
- Từ phiên bản 0.9.15, Alice phải có phiên đã thiết lập với Bob và sử dụng
  session key.
- Trước API version 0.9.52, trong một số triển khai, Bob trả lời Alice sử dụng
  intro key của Alice thay vì session key Alice/Bob, mặc dù
  Alice và Bob có phiên đã thiết lập (từ 0.9.15).
  Từ API version 0.9.52, Bob sẽ sử dụng session key một cách chính xác trong tất cả
  triển khai, và Alice nên từ chối thông điệp nhận từ Bob
  với intro key của Alice nếu Bob có API version 0.9.52 hoặc cao hơn.
- Tùy chọn mở rộng trong header: Không mong đợi, không xác định.

### HolePunch {#holepunch}

HolePunch đơn giản là một gói UDP không có dữ liệu. Nó không được xác thực và không được mã hóa. Nó không chứa header SSU, vì vậy nó không có số loại thông điệp. Nó được gửi từ Charlie đến Alice như một phần của chuỗi Introduction.

## Các Datagram Mẫu {#sampledatagrams}

### Tin nhắn dữ liệu tối giản

- không có fragments, không có ACKs, không có NACKs, v.v.
- Kích thước: 39 bytes

```
+----+----+----+----+----+----+----+----+
|                  MAC                  |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|                   IV                  |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|flag|        time       |flag|#frg|    |
+----+----+----+----+----+----+----+    +
|  padding to fit a full AES256 block   |
+----+----+----+----+----+----+----+----+
```
### Thông điệp dữ liệu tối thiểu với payload

- Kích thước: 46+fragmentSize byte

```
+----+----+----+----+----+----+----+----+
|                  MAC                  |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|                   IV                  |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|flag|        time       |flag|#frg|
+----+----+----+----+----+----+----+----+
  messageId    |   frag info  |         |
----+----+----+----+----+----+         +
| that many bytes of fragment data      |
~                .  .  .                ~
|                                       |
+----+----+----+----+----+----+----+----+
```
## Tài liệu tham khảo

- [Mã hóa AES](/docs/specs/cryptography/#AES)
- [Đặc tả Cấu trúc Chung](/docs/specs/common-structures/)
- [Ngày tháng](/docs/specs/common-structures/#date)
- [Mã hóa ElGamal](/docs/specs/cryptography/#elgamal)
- [Chi tiết HMAC](/docs/specs/cryptography/#udp)
- [Mã nguồn I2P](https://github.com/i2p/i2p.i2p)
- [Mã nguồn i2pd](https://github.com/PurpleI2P/i2pd)
- [KeyCertificate](/docs/specs/common-structures/#key-certificates)
- [RouterIdentity](/docs/specs/common-structures/#routeridentity)
- [SessionKey](/docs/specs/common-structures/#sessionkey)
- [Chữ ký](/docs/specs/common-structures/#signature)
- [SigningPrivateKey](/docs/specs/common-structures/#signingprivatekey)
- [SigningPublicKey](/docs/specs/common-structures/#signingpublickey)
- [Tổng quan SSU](/docs/transport/ssu/)
- [Khóa SSU](/docs/transport/ssu/#keys)
- [Kiểm tra Peer SSU](/docs/transport/ssu/#peerTesting)
