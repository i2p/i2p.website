---
title: "Truyền tải NTCP2"
description: "Giao thức TCP dựa trên nhiễu cho các kết nối liên kết từ bộ định tuyến đến bộ định tuyến"
slug: "ntcp2"
category: "Truyền tải"
lastUpdated: "2026-07"
accurateFor: "0.9.70"
---

## Tổng quan

NTCP2 là một giao thức thỏa thuận khóa được xác thực, giúp tăng cường khả năng chống lại các hình thức nhận dạng tự động và các cuộc tấn công đối với [NTCP](/docs/transport/ntcp).

NTCP2 được thiết kế để linh hoạt và có thể cùng tồn tại với NTCP. Nó có thể được hỗ trợ trên cùng một cổng với NTCP, hoặc một cổng khác, hoặc hoàn toàn không cần hỗ trợ NTCP đồng thời. Xem phần Thông tin Router đã công bố bên dưới để biết chi tiết.

Giống như các giao thức truyền tải I2P khác, NTCP2 chỉ được định nghĩa để truyền tải điểm-điểm (từ router này sang router khác) các thông điệp I2NP. Nó không phải là một kênh truyền dữ liệu đa năng.

NTCP2 được hỗ trợ kể từ phiên bản 0.9.36. Xem [Prop111](/proposals/111-ntcp-2) để biết đề xuất ban đầu, bao gồm phần thảo luận nền tảng và thông tin bổ sung.

## Khung giao thức Noise

NTCP2 sử dụng Mô hình Giao thức Noise [NOISE](https://noiseprotocol.org/noise.html) (Bản sửa đổi 33, 2017-10-04). Noise có các tính chất tương tự như giao thức Station-To-Station [STS](#references), vốn là cơ sở cho giao thức [SSU](/docs/transport/ssu). Theo thuật ngữ của Noise, Alice là bên khởi tạo và Bob là bên phản hồi.

NTCP2 dựa trên giao thức Noise Noise_XK_25519_ChaChaPoly_SHA256. (Bộ định danh thực tế cho hàm suy xuất khóa ban đầu là "Noise_XKaesobfse+hs2+hs3_25519_ChaChaPoly_SHA256" để chỉ các phần mở rộng của I2P - xem phần KDF 1 bên dưới). Giao thức Noise này sử dụng các nguyên thủy sau đây:

- Mẫu bắt tay: XK Alice truyền khóa của cô ấy cho Bob (X) Alice đã biết khóa tĩnh của Bob trước đó (K)
- Hàm DH: X25519 X25519 DH với độ dài khóa 32 byte như được quy định trong [RFC-7748](https://tools.ietf.org/html/rfc7748).
- Hàm mật mã: ChaChaPoly AEAD_CHACHA20_POLY1305 như được quy định trong mục 2.8 của [RFC-7539](https://tools.ietf.org/html/rfc7539). Nonce 12 byte, với 4 byte đầu tiên được đặt bằng không.
- Hàm băm: SHA256 Hàm băm tiêu chuẩn 32 byte, đã được sử dụng rộng rãi trong I2P.

## Các bổ sung cho Khung công việc

NTCP2 xác định các cải tiến sau đây cho Noise_XK_25519_ChaChaPoly_SHA256. Những cải tiến này nói chung tuân theo các hướng dẫn trong mục 13 của [NOISE](https://noiseprotocol.org/noise.html).

1) Các khóa tạm thời dạng rõ được làm mờ bằng mã hóa AES sử dụng một khóa và IV đã biết. 2) Đệm dạng rõ ngẫu nhiên được thêm vào thông điệp 1 và 2. Phần đệm dạng rõ này được đưa vào quá trình tính toán băm bắt tay (MixHash). Xem các phần KDF bên dưới để biết thông điệp 2 và phần 1 của thông điệp 3. Đệm AEAD ngẫu nhiên được thêm vào thông điệp 3 và các thông điệp trong pha dữ liệu. 3) Một trường độ dài khung gồm hai byte được thêm vào, như yêu cầu khi sử dụng Noise qua TCP, và giống như trong obfs4. Trường này chỉ được dùng trong các thông điệp ở pha dữ liệu. Các khung AEAD của thông điệp 1 và 2 có độ dài cố định. Khung AEAD của phần 1 thông điệp 3 cũng có độ dài cố định. Độ dài khung AEAD của phần 2 thông điệp 3 được xác định trong thông điệp 1. 4) Trường độ dài khung hai byte được làm mờ bằng SipHash-2-4, giống như trong obfs4. 5) Định dạng tải trọng được xác định cho các thông điệp 1, 2, 3 và pha dữ liệu. Tất nhiên, những điều này không được định nghĩa trong khuôn khổ của framework.

## Tin nhắn

Tất cả các tin nhắn NTCP2 đều có độ dài nhỏ hơn hoặc bằng 65537 byte. Định dạng tin nhắn dựa trên các tin nhắn Noise, với những điều chỉnh về khung dữ liệu và tính không thể phân biệt. Các triển khai sử dụng thư viện Noise tiêu chuẩn có thể cần xử lý trước các tin nhắn nhận được/truyền đi để phù hợp với định dạng tin nhắn Noise. Tất cả các trường được mã hóa đều là văn bản mã hóa AEAD.

Trình tự thiết lập như sau:

```
Alice                           Bob

SessionRequest ------------------->
<------------------- SessionCreated
SessionConfirmed ----------------->
```
Sử dụng thuật ngữ Noise, quá trình thiết lập và trình tự dữ liệu như sau: (Các thuộc tính bảo mật tải trọng từ [Noise](https://noiseprotocol.org/noise.html))

```
XK(s, rs):           Authentication   Confidentiality
  <- s
  ...
  -> e, es                  0                2
  <- e, ee                  2                1
  -> s, se                  2                5
  <-                        2                5
```
Sau khi phiên làm việc đã được thiết lập, Alice và Bob có thể trao đổi các tin nhắn Dữ liệu.

Tất cả các loại tin nhắn (SessionRequest, SessionCreated, SessionConfirmed, Data và TimeSync) được quy định trong phần này.

Một số ký hiệu:

    - RH_A = Router Hash for Alice (32 bytes)
    - RH_B = Router Hash for Bob (32 bytes)

### Mã hóa có xác thực

Có ba phiên bản mã hóa được xác thực riêng biệt (CipherStates). Một trong giai đoạn bắt tay, và hai cái (gửi và nhận) cho giai đoạn dữ liệu. Mỗi cái có khóa riêng từ một KDF.

Dữ liệu được mã hóa/xác thực sẽ được biểu thị dưới dạng

```
+----+----+----+----+----+----+----+----+
|                                       |
+                                       +
|   Encrypted and authenticated data    |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+
```
#### ChaCha20/Poly1305

Định dạng dữ liệu được mã hóa và xác thực.

Đầu vào cho các hàm mã hóa/giải mã:

```
k :: 32 byte cipher key, as generated from KDF

nonce :: Counter-based nonce, 12 bytes.
         Starts at 0 and incremented for each message.
         First four bytes are always zero.
         Last eight bytes are the counter, little-endian encoded.
         Maximum value is 2**64 - 2.
         Connection must be dropped and restarted after
         it reaches that value.
         The value 2**64 - 1 must never be sent.

ad :: In handshake phase:
      Associated data, 32 bytes.
      The SHA256 hash of all preceding data.
      In data phase:
      Zero bytes

data :: Plaintext data, 0 or more bytes
```
Đầu ra của hàm mã hóa, đầu vào của hàm giải mã:

```
+----+----+----+----+----+----+----+----+
|Obfs Len |                             |
+----+----+                             +
|       ChaCha20 encrypted data         |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+              (MAC)                    +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+

Obfs Len :: Length of (encrypted data + MAC) to follow, 16 - 65535
            Obfuscation using SipHash (see below)
            Not used in message 1 or 2, or message 3 part 1, where the length is fixed
            Not used in message 3 part 1, as the length is specified in message 1

encrypted data :: Same size as plaintext data, 0 - 65519 bytes

MAC :: Poly1305 message authentication code, 16 bytes
```
Đối với ChaCha20, những gì được mô tả ở đây tương ứng với [RFC-7539](https://tools.ietf.org/html/rfc7539), cũng được sử dụng tương tự trong TLS [RFC-7905](https://tools.ietf.org/html/rfc7905).

#### Ghi chú

- Vì ChaCha20 là một bộ mã hóa dòng, các văn bản gốc không cần được điền thêm dữ liệu. Các byte dòng khóa dư thừa sẽ bị loại bỏ.
- Khóa cho bộ mã hóa (256 bit) được thống nhất thông qua hàm KDF SHA256. Chi tiết về KDF cho từng tin nhắn được trình bày trong các phần riêng biệt bên dưới.
- Các khung ChaChaPoly cho tin nhắn 1, 2 và phần đầu tiên của tin nhắn 3 có kích thước xác định. Bắt đầu từ phần thứ hai của tin nhắn 3, các khung có kích thước thay đổi. Kích thước phần 1 của tin nhắn 3 được chỉ định trong tin nhắn 1. Bắt đầu từ giai đoạn dữ liệu, các khung được thêm vào đầu một độ dài hai byte được ngụy trang bằng SipHash như trong obfs4.
- Phần điền thêm nằm ngoài khung dữ liệu được xác thực đối với tin nhắn 1 và 2. Phần điền này được sử dụng trong KDF cho tin nhắn tiếp theo, do đó việc sửa đổi sẽ bị phát hiện. Bắt đầu từ tin nhắn 3, phần điền nằm bên trong khung dữ liệu được xác thực.

#### Xử lý lỗi AEAD

- Trong các tin nhắn 1, 2 và các phần 1, 2 của tin nhắn 3, kích thước tin nhắn AEAD được biết trước. Khi xác thực AEAD thất bại, người nhận phải ngừng xử lý tin nhắn và đóng kết nối mà không phản hồi. Việc đóng kết nối này nên là bất thường (TCP RST).
- Để chống dò quét, trong tin nhắn 1, sau khi xác thực AEAD thất bại, Bob nên thiết lập một khoảng thời gian chờ ngẫu nhiên (phạm vi chưa xác định) và sau đó đọc một số byte ngẫu nhiên (phạm vi chưa xác định) trước khi đóng socket. Bob nên duy trì danh sách đen các địa chỉ IP có nhiều lần thất bại liên tiếp.
- Trong giai đoạn dữ liệu, kích thước tin nhắn AEAD được "mã hóa" (ẩn danh) bằng SipHash. Cần cẩn trọng để tránh tạo thành oracle giải mã. Khi xác thực AEAD trong giai đoạn dữ liệu thất bại, người nhận nên thiết lập một khoảng thời gian chờ ngẫu nhiên (phạm vi chưa xác định), sau đó đọc một số byte ngẫu nhiên (phạm vi chưa xác định). Sau khi đọc xong hoặc khi hết thời gian chờ đọc, người nhận nên gửi một dữ liệu tải mang khối chấm dứt chứa mã lý do "thất bại AEAD", rồi đóng kết nối.
- Thực hiện cùng hành động xử lý lỗi đối với giá trị trường độ dài không hợp lệ trong giai đoạn dữ liệu.

### Hàm suy xuất khóa (KDF) (cho tin nhắn bắt tay 1)

KDF tạo ra một khóa mật mã k cho giai đoạn bắt tay từ kết quả DH, sử dụng HMAC-SHA256(key, data) như được định nghĩa trong [RFC-2104](https://tools.ietf.org/html/rfc2104). Đây là các hàm InitializeSymmetric(), MixHash() và MixKey(), giống hệt như được định nghĩa trong đặc tả Noise.

```
This is the "e" message pattern:

// Define protocol_name.
Set protocol_name = "Noise_XKaesobfse+hs2+hs3_25519_ChaChaPoly_SHA256"
 (48 bytes, US-ASCII encoded, no NULL termination).

// Define Hash h = 32 bytes
h = SHA256(protocol_name);

Define ck = 32 byte chaining key. Copy the h data to ck.
Set ck = h

Define rs = Bob's 32-byte static key as published in the RouterInfo

// MixHash(null prologue)
h = SHA256(h);

// up until here, can all be precalculated by Alice for all outgoing connections

// Alice must validate that Bob's static key is a valid point on the curve here.

// Bob static key
// MixHash(rs)
// || below means append
h = SHA256(h || rs);

// up until here, can all be precalculated by Bob for all incoming connections

This is the "e" message pattern:

Alice generates her ephemeral DH key pair e.

// Alice ephemeral key X
// MixHash(e.pubkey)
// || below means append
h = SHA256(h || e.pubkey);

// h is used as the associated data for the AEAD in message 1
// Retain the Hash h for the message 2 KDF


End of "e" message pattern.

This is the "es" message pattern:

// DH(e, rs) == DH(s, re)
Define input_key_material = 32 byte DH result of Alice's ephemeral key and Bob's static key
Set input_key_material = X25519 DH result

// MixKey(DH())

Define temp_key = 32 bytes
Define HMAC-SHA256(key, data) as in [RFC-2104]_
// Generate a temp key from the chaining key and DH result
// ck is the chaining key, defined above
temp_key = HMAC-SHA256(ck, input_key_material)
// overwrite the DH result in memory, no longer needed
input_key_material = (all zeros)

// Output 1
// Set a new chaining key from the temp key
// byte() below means a single byte
ck =       HMAC-SHA256(temp_key, byte(0x01)).

// Output 2
// Generate the cipher key k
Define k = 32 bytes
// || below means append
// byte() below means a single byte
k =        HMAC-SHA256(temp_key, ck || byte(0x02)).
// overwrite the temp_key in memory, no longer needed
temp_key = (all zeros)

// retain the chaining key ck for message 2 KDF


End of "es" message pattern.
```
### 1) Yêu cầu phiên

Alice gửi cho Bob.

Nội dung nhiễu: Khóa tạm thời X của Alice, tải trọng Noise: khối tùy chọn 16 byte, tải trọng không phải nhiễu: độn ngẫu nhiên

(Tính năng bảo mật tải trọng từ [Noise](https://noiseprotocol.org/noise.html))

```
XK(s, rs):           Authentication   Confidentiality
  -> e, es                  0                2

  Authentication: None (0).
  This payload may have been sent by any party, including an active attacker.

  Confidentiality: 2.
  Encryption to a known recipient, forward secrecy for sender compromise
  only, vulnerable to replay.  This payload is encrypted based only on DHs
  involving the recipient's static key pair.  If the recipient's static
  private key is compromised, even at a later date, this payload can be
  decrypted.  This message can also be replayed, since there's no ephemeral
  contribution from the recipient.

  "e": Alice generates a new ephemeral key pair and stores it in the e
       variable, writes the ephemeral public key as cleartext into the
       message buffer, and hashes the public key along with the old h to
       derive a new h.

  "es": A DH is performed between the Alice's ephemeral key pair and the
        Bob's static key pair.  The result is hashed along with the old ck to
        derive a new ck and k, and n is set to zero.
```
Giá trị X được mã hóa để đảm bảo tính không thể phân biệt và tính duy nhất của dữ liệu tải, đây là các biện pháp chống lại việc kiểm tra gói tin sâu (DPI). Chúng tôi sử dụng mã hóa AES để đạt được điều này, thay vì các phương pháp phức tạp và chậm hơn như elligator2. Việc sử dụng mã hóa bất đối xứng với khóa công khai của router Bob sẽ quá chậm. Mã hóa AES sử dụng băm router của Bob làm khóa và IV của Bob như đã được công bố trong cơ sở dữ liệu mạng (netDb).

Mã hóa AES chỉ nhằm chống lại việc kiểm tra sâu gói tin (DPI). Bất kỳ bên nào biết được băm router của Bob và giá trị IV, những thông tin này được công khai trong cơ sở dữ liệu mạng, đều có thể giải mã giá trị X trong thông điệp này.

Phần đệm không được mã hóa bởi Alice. Có thể cần Bob giải mã phần đệm để ngăn chặn các cuộc tấn công dựa trên thời gian.

Nội dung gốc:

```
+----+----+----+----+----+----+----+----+
|                                       |
+        obfuscated with RH_B           +
|       AES-CBC-256 encrypted X         |
+             (32 bytes)                +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|   ChaChaPoly encrypted data           |
+             (16 bytes)                +
|   k defined in KDF for message 1      |
+   n = 0                               +
|   see KDF for associated data         |
+----+----+----+----+----+----+----+----+
|                                       |
+        Poly1305 MAC (16 bytes)        +
|                                       |
+----+----+----+----+----+----+----+----+
|     unencrypted authenticated         |
~         padding (optional)            ~
|     length defined in options block   |
+----+----+----+----+----+----+----+----+

X :: 32 bytes, AES-256-CBC encrypted X25519 ephemeral key, little endian
        key: RH_B
        iv: As published in Bobs network database entry

padding :: Random data, 0 or more bytes.
           Total message length must be 65535 bytes or less.
           Total message length must be 287 bytes or less if
           Bob is publishing his address as NTCP
           (see Version Detection section below).
           Alice and Bob will use the padding data in the KDF for message 2.
           It is authenticated so that any tampering will cause the
           next message to fail.
```
Dữ liệu chưa được mã hóa (thẻ xác thực Poly1305 không được hiển thị):

```
+----+----+----+----+----+----+----+----+
|                                       |
+                                       +
|                   X                   |
+              (32 bytes)               +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|               options                 |
+              (16 bytes)               +
|                                       |
+----+----+----+----+----+----+----+----+
|     unencrypted authenticated         |
+         padding (optional)            +
|     length defined in options block   |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+

X :: 32 bytes, X25519 ephemeral key, little endian

options :: options block, 16 bytes, see below

padding :: Random data, 0 or more bytes.
           Total message length must be 65535 bytes or less.
           Total message length must be 287 bytes or less if
           Bob is publishing his address as "NTCP"
           (see Version Detection section below)
           Alice and Bob will use the padding data in the KDF for message 2.
           It is authenticated so that any tampering will cause the
           next message to fail.
```
Khối tùy chọn: Lưu ý: Tất cả các trường đều theo thứ tự big-endian.

```
+----+----+----+----+----+----+----+----+
| id | ver|  padLen | m3p2len | Rsvd(0) |
+----+----+----+----+----+----+----+----+
|        tsA        |   Reserved (0)    |
+----+----+----+----+----+----+----+----+

id :: 1 byte, the network ID (currently 2, except for test networks)
      As of 0.9.42. See proposal 147.

ver :: 1 byte, protocol version (currently 2)

padLen :: 2 bytes, length of the padding, 0 or more
          See below for max guidelines. Random size from 0 to 64 bytes minimum is recommended.
          (Distribution is implementation-dependent)

m3p2Len :: 2 bytes, length of the the second AEAD frame in SessionConfirmed
           (message 3 part 2) See notes below

Rsvd :: 2 bytes, set to 0 for compatibility with future options

tsA :: 4 bytes, Unix timestamp, unsigned seconds.
       Wraps around in 2106

Reserved :: 4 bytes, set to 0 for compatibility with future options
```
#### Ghi chú

- Khi địa chỉ được công bố là "NTCP", Bob hỗ trợ cả NTCP và NTCP2 trên cùng một cổng. Để đảm bảo tương thích, khi khởi tạo kết nối tới một địa chỉ được công bố là "NTCP", Alice phải giới hạn kích thước tối đa của thông điệp này, bao gồm cả phần đệm (padding), ở mức 287 byte hoặc ít hơn. Điều này giúp Bob dễ dàng tự động nhận diện giao thức. Khi được công bố là "NTCP2", sẽ không có giới hạn về kích thước. Xem các phần Địa chỉ được công bố và Nhận diện phiên bản bên dưới.

- Giá trị X duy nhất trong khối AES ban đầu đảm bảo rằng văn bản mã hóa sẽ khác nhau ở mỗi phiên kết nối.

- Bob phải từ chối các kết nối mà giá trị dấu thời gian lệch quá xa so với thời gian hiện tại. Gọi khoảng thời gian chênh lệch tối đa là "D". Bob phải duy trì một bộ nhớ cache cục bộ các giá trị bắt tay đã sử dụng trước đó và từ chối các giá trị trùng lặp, nhằm ngăn chặn các cuộc tấn công phát lại. Các giá trị trong bộ nhớ cache phải có thời lượng sống ít nhất là 2*D. Các giá trị cache tùy thuộc vào cách triển khai, tuy nhiên có thể sử dụng giá trị X 32 byte (hoặc phiên bản đã mã hóa tương ứng).

- Các khóa tạm thời Diffie-Hellman không bao giờ được phép tái sử dụng, để ngăn chặn các cuộc tấn công mật mã học, và việc tái sử dụng sẽ bị từ chối như một cuộc tấn công phát lại.

- Các tùy chọn "KE" và "auth" phải tương thích với nhau, tức là bí mật chung K phải có kích thước phù hợp. Nếu thêm các tùy chọn "auth" khác, điều này có thể làm thay đổi ngầm nghĩa của cờ "KE" để sử dụng một hàm rút trích khóa (KDF) khác hoặc kích thước rút gọn khác.

- Bob phải xác thực rằng khóa tạm thời của Alice là một điểm hợp lệ trên đường cong tại đây.

- Việc chèn dữ liệu thừa (padding) nên được giới hạn ở mức hợp lý. Bob có thể từ chối các kết nối có quá nhiều dữ liệu thừa. Bob sẽ xác định các tùy chọn padding của mình trong thông điệp 2. Hướng dẫn về giới hạn tối thiểu/tối đa sẽ được xác định sau (TBD). Kích thước ngẫu nhiên từ 0 đến 31 byte là tối thiểu? (Phân bố phụ thuộc vào cách triển khai). Các triển khai bằng Java hiện đang giới hạn tối đa 256 byte cho dữ liệu thừa.

- Khi xảy ra bất kỳ lỗi nào, bao gồm lỗi AEAD, DH, dấu thời gian, dấu hiệu lặp lại (replay) hoặc xác thực khóa thất bại, Bob phải ngừng xử lý tin nhắn và đóng kết nối mà không phản hồi. Việc đóng kết nối này cần là một kết thúc bất thường (TCP RST). Để chống dò quét, sau khi xảy ra lỗi AEAD, Bob nên thiết lập một khoảng thời gian chờ ngẫu nhiên (phạm vi sẽ xác định sau) và sau đó đọc một số lượng byte ngẫu nhiên (phạm vi sẽ xác định sau) trước khi đóng socket.

- Bob có thể thực hiện kiểm tra MSB nhanh để xác minh khóa hợp lệ (X[31] & 0x80 == 0) trước khi giải mã. Nếu bit cao được thiết lập, hãy triển khai cơ chế chống dò tìm tương tự như khi xảy ra lỗi AEAD.

- Giảm thiểu tấn công DoS: DH là một thao tác tương đối tốn kém. Như với giao thức NTCP trước đó, các router nên thực hiện mọi biện pháp cần thiết để ngăn chặn việc cạn kiệt CPU hoặc kết nối. Giới hạn số lượng kết nối hoạt động tối đa và số lượng thiết lập kết nối đang tiến hành tối đa. Áp dụng giới hạn thời gian đọc (cả theo từng lần đọc và tổng thời gian cho các cuộc tấn công kiểu "slowloris"). Hạn chế các kết nối lặp lại hoặc đồng thời từ cùng một nguồn. Duy trì danh sách đen các nguồn thường xuyên thất bại. Không phản hồi khi xác thực AEAD thất bại.

- Để hỗ trợ việc dò tìm phiên bản và bắt tay nhanh chóng, các triển khai phải đảm bảo rằng Alice sẽ lưu tạm và sau đó đẩy toàn bộ nội dung của thông điệp đầu tiên cùng với phần đệm (padding) một lần duy nhất. Việc này làm tăng khả năng dữ liệu sẽ nằm gọn trong một gói TCP duy nhất (trừ khi bị phân mảnh bởi hệ điều hành hoặc các thiết bị trung gian), và được Bob nhận toàn bộ cùng lúc. Ngoài ra, các triển khai cũng phải đảm bảo rằng Bob sẽ lưu tạm và sau đó đẩy toàn bộ nội dung của thông điệp thứ hai một lần duy nhất, bao gồm cả phần đệm, và tương tự với toàn bộ nội dung của thông điệp thứ ba. Việc này cũng nhằm mục đích hiệu quả và đảm bảo tính hiệu lực của phần đệm ngẫu nhiên.

- Trường "ver": Giao thức Noise tổng thể, các phần mở rộng và giao thức NTCP bao gồm các đặc tả tải trọng, cho biết NTCP2. Trường này có thể được sử dụng để chỉ hỗ trợ các thay đổi trong tương lai.

- Độ dài phần 2 của tin nhắn 3: Đây là kích thước của khung AEAD thứ hai (bao gồm mã xác thực MAC 16 byte) chứa Thông tin Router của Alice và phần đệm tùy chọn, sẽ được gửi trong tin nhắn SessionConfirmed. Vì các router định kỳ tạo lại và phát hành lại Thông tin Router của chúng, kích thước Thông tin Router hiện tại có thể thay đổi trước khi tin nhắn 3 được gửi. Các triển khai phải chọn một trong hai chiến lược sau:

a) lưu thông tin Bộ định tuyến hiện tại để gửi trong tin nhắn 3, để biết được kích thước, và tùy chọn thêm chỗ trống cho phần đệm;

b) tăng kích thước đã xác định đủ để cho phép kích thước Thông tin Bộ định tuyến (Router Info) có thể tăng lên, và luôn thêm độ đệm khi tin nhắn 3 thực sự được gửi. Trong cả hai trường hợp, độ dài "m3p2len" được đưa vào trong tin nhắn 1 phải chính xác bằng kích thước của khung đó khi được gửi trong tin nhắn 3.

- Bob phải từ chối kết nối nếu còn bất kỳ dữ liệu đầu vào nào tồn tại sau khi xác thực tin nhắn 1 và đọc phần đệm. Không nên có dữ liệu bổ sung nào từ Alice, vì Bob chưa phản hồi bằng tin nhắn 2.

- Trường ID mạng được dùng để nhanh chóng nhận diện các kết nối liên mạng. Nếu trường này khác không và không khớp với ID mạng của Bob, Bob nên ngắt kết nối và chặn các kết nối trong tương lai. Mọi kết nối từ các mạng thử nghiệm nên có ID khác và sẽ không vượt qua kiểm tra. Từ phiên bản 0.9.42 trở đi. Xem đề xuất 147 để biết thêm thông tin.

- Thông qua API 0.9.68 (phát hành 2.11.0), Java I2P đã triển khai giới hạn độ đệm tối đa 256 byte cho các kết nối không dùng mật mã hậu lượng tử (non-PQ), tuy nhiên điều này trước đây chưa được tài liệu hóa.
  Kể từ API 0.9.69 (phát hành 2.12.0), Java I2P áp dụng mức độ đệm tối đa cho các kết nối không dùng mật mã hậu lượng tử giống như với MLKEM-512. Độ đệm tối đa hiện là 880 byte.

### Hàm Phái sinh Khóa (KDF) (cho tin nhắn bắt tay 2 và phần 1 tin nhắn bắt tay 3)

```
// take h saved from message 1 KDF
// MixHash(ciphertext)
h = SHA256(h || 32 byte encrypted payload from message 1)

// MixHash(padding)
// Only if padding length is nonzero
h = SHA256(h || random padding from message 1)

This is the "e" message pattern:

Bob generates his ephemeral DH key pair e.

// h is from KDF for handshake message 1
// Bob ephemeral key Y
// MixHash(e.pubkey)
// || below means append
h = SHA256(h || e.pubkey);

// h is used as the associated data for the AEAD in message 2
// Retain the Hash h for the message 3 KDF

End of "e" message pattern.

This is the "ee" message pattern:

// DH(e, re)
Define input_key_material = 32 byte DH result of Alice's ephemeral key and Bob's ephemeral key
Set input_key_material = X25519 DH result
// overwrite Alice's ephemeral key in memory, no longer needed
// Alice:
e(public and private) = (all zeros)
// Bob:
re = (all zeros)

// MixKey(DH())

Define temp_key = 32 bytes
Define HMAC-SHA256(key, data) as in [RFC-2104]_
// Generate a temp key from the chaining key and DH result
// ck is the chaining key, from the KDF for handshake message 1
temp_key = HMAC-SHA256(ck, input_key_material)
// overwrite the DH result in memory, no longer needed
input_key_material = (all zeros)

// Output 1
// Set a new chaining key from the temp key
// byte() below means a single byte
ck =       HMAC-SHA256(temp_key, byte(0x01)).

// Output 2
// Generate the cipher key k
Define k = 32 bytes
// || below means append
// byte() below means a single byte
k =        HMAC-SHA256(temp_key, ck || byte(0x02)).
// overwrite the temp_key in memory, no longer needed
temp_key = (all zeros)

// retain the chaining key ck for message 3 KDF

End of "ee" message pattern.
```
### 2) SessionCreated

Bob gửi cho Alice.

Nội dung nhiễu: Khóa tạm thời Y của Bob, Dữ liệu tải nhiễu: khối tùy chọn 16 byte, Dữ liệu tải không nhiễu: độn ngẫu nhiên

(Thuộc tính Bảo mật Payload từ [Noise](https://noiseprotocol.org/noise.html) )

```
XK(s, rs):           Authentication   Confidentiality
  <- e, ee                  2                1

  Authentication: 2.
  Sender authentication resistant to key-compromise impersonation (KCI).
  The sender authentication is based on an ephemeral-static DH ("es" or "se")
  between the sender's static key pair and the recipient's ephemeral key pair.
  Assuming the corresponding private keys are secure, this authentication cannot be forged.

  Confidentiality: 1.
  Encryption to an ephemeral recipient.
  This payload has forward secrecy, since encryption involves an ephemeral-ephemeral DH ("ee").
  However, the sender has not authenticated the recipient,
  so this payload might be sent to any party, including an active attacker.


  "e": Bob generates a new ephemeral key pair and stores it in the e variable,
  writes the ephemeral public key as cleartext into the message buffer,
  and hashes the public key along with the old h to derive a new h.

  "ee": A DH is performed between the Bob's ephemeral key pair and the Alice's ephemeral key pair.
  The result is hashed along with the old ck to derive a new ck and k, and n is set to zero.
```
Giá trị Y được mã hóa để đảm bảo tính không thể phân biệt và tính duy nhất của dữ liệu tải, đây là những biện pháp chống lại việc kiểm tra sâu gói tin (DPI). Chúng tôi sử dụng mã hóa AES để đạt được điều này, thay vì các phương pháp phức tạp và chậm hơn như elligator2. Việc mã hóa bất đối xứng bằng khóa công khai của router Alice sẽ quá chậm. Mã hóa AES sử dụng băm router của Bob làm khóa và sử dụng trạng thái AES từ thông điệp 1 (được khởi tạo bằng IV của Bob như đã công bố trong cơ sở dữ liệu mạng).

Mã hóa AES chỉ nhằm chống lại việc kiểm tra sâu gói tin (DPI). Bất kỳ bên nào biết được băm router và IV của Bob, những thông tin này được công bố trong cơ sở dữ liệu mạng, và đã thu thập được 32 byte đầu tiên của thông điệp 1, đều có thể giải mã giá trị Y trong thông điệp này.

Nội dung thô:

```
+----+----+----+----+----+----+----+----+
|                                       |
+        obfuscated with RH_B           +
|       AES-CBC-256 encrypted Y         |
+              (32 bytes)               +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|   ChaChaPoly encrypted data (options) |
+   16 bytes                            +
|   k defined in KDF for message 2      |
+   n = 0; see KDF for associated data  +
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+        Poly1305 MAC (16 bytes)        +
|                                       |
+----+----+----+----+----+----+----+----+
|     unencrypted authenticated         |
+         padding (optional)            +
|     length defined in options block   |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+

Y :: 32 bytes, AES-256-CBC encrypted X25519 ephemeral key, little endian
        key: RH_B
        iv: Using AES state from message 1
```
Dữ liệu chưa được mã hóa (thẻ xác thực Poly1305 không hiển thị):

```
+----+----+----+----+----+----+----+----+
|                                       |
+                                       +
|                  Y                    |
+              (32 bytes)               +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|               options                 |
+              (16 bytes)               +
|                                       |
+----+----+----+----+----+----+----+----+
|     unencrypted authenticated         |
+         padding (optional)            +
|     length defined in options block   |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+

Y :: 32 bytes, X25519 ephemeral key, little endian

options :: options block, 16 bytes, see below

padding :: Random data, 0 or more bytes.
           Total message length must be 65535 bytes or less.
           Alice and Bob will use the padding data in the KDF for message 3 part 1.
           It is authenticated so that any tampering will cause the
           next message to fail.
```
#### Ghi chú

- Alice phải xác thực rằng khóa tạm thời của Bob là một điểm hợp lệ trên đường cong tại đây.
- Việc thêm dữ liệu đệm (padding) nên được giới hạn ở mức độ hợp lý. Alice có thể từ chối các kết nối có quá nhiều dữ liệu đệm. Alice sẽ chỉ định tùy chọn padding của mình trong thông điệp 3. Hướng dẫn về giới hạn tối thiểu/tối đa sẽ được xác định sau (TBD). Kích thước ngẫu nhiên từ 0 đến 31 byte là tối thiểu? (Phân bố phụ thuộc vào triển khai)
- Khi xảy ra bất kỳ lỗi nào, bao gồm lỗi AEAD, DH, dấu thời gian, dấu hiệu lặp lại (replay), hoặc xác thực khóa thất bại, Alice phải dừng việc xử lý thông điệp tiếp theo và đóng kết nối mà không phản hồi. Việc đóng này phải là bất thường (TCP RST).
- Để hỗ trợ việc bắt tay nhanh chóng, các triển khai phải đảm bảo rằng Bob sẽ lưu tạm (buffer) và sau đó gửi ngay toàn bộ nội dung của thông điệp đầu tiên một lần, bao gồm cả dữ liệu đệm. Điều này làm tăng khả năng dữ liệu sẽ nằm gọn trong một gói TCP duy nhất (trừ khi bị phân mảnh bởi hệ điều hành hoặc các thiết bị trung gian), và được Alice nhận toàn bộ cùng lúc. Việc này cũng nhằm tăng hiệu quả và đảm bảo tính hiệu lực của dữ liệu đệm ngẫu nhiên.
- Alice phải hủy bỏ kết nối nếu còn bất kỳ dữ liệu nào gửi đến sau khi xác thực thông điệp 2 và đọc xong phần dữ liệu đệm. Không nên có dữ liệu bổ sung nào từ Bob, vì lúc này Alice vẫn chưa phản hồi bằng thông điệp 3.

Khối tùy chọn: Lưu ý: Tất cả các trường đều là big-endian.

```
+----+----+----+----+----+----+----+----+
| Rsvd(0) | padLen  |   Reserved (0)    |
+----+----+----+----+----+----+----+----+
|        tsB        |   Reserved (0)    |
+----+----+----+----+----+----+----+----+

Reserved :: 10 bytes total, set to 0 for compatibility with future options

padLen :: 2 bytes, big endian, length of the padding, 0 or more
          See below for max guidelines. Random size from 0 to 64 bytes minimum is recommended.
          (Distribution is implementation-dependent)

tsB :: 4 bytes, big endian, Unix timestamp, unsigned seconds.
       Wraps around in 2106
```
#### Ghi chú

- Alice phải từ chối các kết nối mà giá trị dấu thời gian (timestamp) lệch quá xa so với thời gian hiện tại. Gọi khoảng thời gian chênh lệch tối đa là "D". Alice phải duy trì một bộ nhớ đệm cục bộ các giá trị bắt tay đã từng sử dụng và từ chối các giá trị trùng lặp, nhằm ngăn chặn các cuộc tấn công phát lại (replay attacks). Các giá trị trong bộ nhớ đệm phải có thời gian sống ít nhất là 2*D. Các giá trị bộ nhớ đệm phụ thuộc vào cách triển khai, tuy nhiên có thể sử dụng giá trị Y 32 byte (hoặc phiên bản đã mã hóa tương ứng) làm giá trị đó.

- Thông qua API 0.9.68 (phát hành 2.11.0), Java I2P triển khai mức độ đệm tối đa 256 byte cho các kết nối không dùng PQ, tuy nhiên điều này trước đây chưa được tài liệu hóa.
  Kể từ API 0.9.69 (phát hành 2.12.0), Java I2P triển khai mức độ đệm tối đa cho các kết nối không dùng PQ giống như với MLKEM-512. Mức độ đệm tối đa là 848 byte.

#### Vấn đề

- Có nên bao gồm các tùy chọn đệm tối thiểu/tối đa ở đây không?

### Mã hóa cho phần 1 tin nhắn bắt tay 3, sử dụng KDF từ tin nhắn 2

```
// take h saved from message 2 KDF
// MixHash(ciphertext)
h = SHA256(h || 24 byte encrypted payload from message 2)

// MixHash(padding)
// Only if padding length is nonzero
h = SHA256(h || random padding from message 2)
// h is used as the associated data for the AEAD in message 3 part 1, below

This is the "s" message pattern:

Define s = Alice's static public key, 32 bytes

// EncryptAndHash(s.publickey)
// EncryptWithAd(h, s.publickey)
// AEAD_ChaCha20_Poly1305(key, nonce, associatedData, data)
// k is from handshake message 1
// n is 1
ciphertext = AEAD_ChaCha20_Poly1305(k, n++, h, s.publickey)
// MixHash(ciphertext)
// || below means append
h = SHA256(h || ciphertext);

// h is used as the associated data for the AEAD in message 3 part 2

End of "s" message pattern.
```
### Hàm suy xuất khóa (KDF) (cho phần 2 tin nhắn bắt tay 3)

```
This is the "se" message pattern:

// DH(s, re) == DH(e, rs)
Define input_key_material = 32 byte DH result of Alice's static key and Bob's ephemeral key
Set input_key_material = X25519 DH result
// overwrite Bob's ephemeral key in memory, no longer needed
// Alice:
re = (all zeros)
// Bob:
e(public and private) = (all zeros)

// MixKey(DH())

Define temp_key = 32 bytes
Define HMAC-SHA256(key, data) as in [RFC-2104]_
// Generate a temp key from the chaining key and DH result
// ck is the chaining key, from the KDF for handshake message 1
temp_key = HMAC-SHA256(ck, input_key_material)
// overwrite the DH result in memory, no longer needed
input_key_material = (all zeros)

// Output 1
// Set a new chaining key from the temp key
// byte() below means a single byte
ck =       HMAC-SHA256(temp_key, byte(0x01)).

// Output 2
// Generate the cipher key k
Define k = 32 bytes
// || below means append
// byte() below means a single byte
k =        HMAC-SHA256(temp_key, ck || byte(0x02)).

// h from message 3 part 1 is used as the associated data for the AEAD in message 3 part 2

// EncryptAndHash(payload)
// EncryptWithAd(h, payload)
// AEAD_ChaCha20_Poly1305(key, nonce, associatedData, data)
// n is 0
ciphertext = AEAD_ChaCha20_Poly1305(k, n++, h, payload)
// MixHash(ciphertext)
// || below means append
h = SHA256(h || ciphertext);

// retain the chaining key ck for the data phase KDF
// retain the hash h for the data phase Additional Symmetric Key (SipHash) KDF

End of "se" message pattern.

// overwrite the temp_key in memory, no longer needed
temp_key = (all zeros)
```
### 3) SessionConfirmed

Alice gửi cho Bob.

Nội dung nhiễu: Khóa tĩnh của Alice, tải trọng Noise: RouterInfo của Alice và phần đệm ngẫu nhiên, tải trọng không phải Noise: không có

(Các Thuộc Tính Bảo Mật Payload từ [Noise](https://noiseprotocol.org/noise.html) )

```
XK(s, rs):           Authentication   Confidentiality
  -> s, se                  2                5

  Authentication: 2.
  Sender authentication resistant to key-compromise impersonation (KCI).  The
  sender authentication is based on an ephemeral-static DH ("es" or "se")
  between the sender's static key pair and the recipient's ephemeral key
  pair.  Assuming the corresponding private keys are secure, this
  authentication cannot be forged.

  Confidentiality: 5.
  Encryption to a known recipient, strong forward secrecy.  This payload is
  encrypted based on an ephemeral-ephemeral DH as well as an ephemeral-static
  DH with the recipient's static key pair.  Assuming the ephemeral private
  keys are secure, and the recipient is not being actively impersonated by an
  attacker that has stolen its static private key, this payload cannot be
  decrypted.

  "s": Alice writes her static public key from the s variable into the
  message buffer, encrypting it, and hashes the output along with the old h
  to derive a new h.

  "se": A DH is performed between the Alice's static key pair and the Bob's
  ephemeral key pair.  The result is hashed along with the old ck to derive a
  new ck and k, and n is set to zero.
```
Phần này chứa hai khung ChaChaPoly. Khung đầu tiên là khóa công khai tĩnh đã được mã hóa của Alice. Khung thứ hai là dữ liệu tải Noise: RouterInfo đã được mã hóa của Alice, các tùy chọn tùy chọn và phần đệm tùy chọn. Chúng sử dụng các khóa khác nhau, vì hàm MixKey() được gọi ở giữa.

Nội dung thô:

```
+----+----+----+----+----+----+----+----+
|                                       |
+   ChaCha20 encrypted data (32 bytes)  +
|   Alice static key S                  |
+     k defined in KDF for message 2    +
|   n = 1 see KDF for associated data   |
+----+----+----+----+----+----+----+----+
|                                       |
+        Poly1305 MAC (16 bytes)        +
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+   ChaCha20 encrypted data             +
|     Length specified in message 1     |
+     (including 16 byte MAC to follow) +
|                                       |
+       Alice RouterInfo                +
|       using block format 2            |
+       Alice Options (optional)        +
|       using block format 1            |
+       Arbitrary padding               +
|       using block format 254          |
+                                       +
| k defined in KDF for message 3 part 2 |
+     n = 0                             +
|     see KDF for associated data       |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+        Poly1305 MAC (16 bytes)        +
|                                       |
+----+----+----+----+----+----+----+----+

S :: 32 bytes, ChaChaPoly encrypted Alice's X25519 static key, little endian
     inside 48 byte ChaChaPoly frame
```
Dữ liệu chưa được mã hóa (các thẻ xác thực Poly1305 không hiển thị):

```
+----+----+----+----+----+----+----+----+
|                                       |
+                                       +
|              S                        |
+       Alice static key                +
|          (32 bytes)                   |
+                                       +
|                                       |
+                                       +
+----+----+----+----+----+----+----+----+
|                                       |
+                                       +
|                                       |
+                                       +
|       Alice RouterInfo block          |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+       Optional Options block          +
|                                       |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+       Optional Padding block          +
|                                       |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+

S :: 32 bytes, Alice's X25519 static key, little endian
```
#### Ghi chú

- Bob phải thực hiện việc xác thực Thông tin Bộ định tuyến như thường lệ. Đảm bảo loại chữ ký được hỗ trợ, xác minh chữ ký, kiểm tra thời gian gửi nằm trong giới hạn cho phép, và thực hiện mọi kiểm tra cần thiết khác.

- Bob phải xác minh rằng khóa tĩnh của Alice nhận được trong khung đầu tiên khớp với khóa tĩnh trong Thông tin Bộ định tuyến. Bob trước tiên phải tìm kiếm trong Thông tin Bộ định tuyến để tìm địa chỉ Bộ định tuyến NTCP hoặc NTCP2 có tùy chọn phiên bản (v) phù hợp. Xem các phần Thông tin Bộ định tuyến đã công bố và Thông tin Bộ định tuyến chưa công bố bên dưới.

- Nếu Bob có phiên bản cũ hơn của RouterInfo của Alice trong cơ sở dữ liệu mạng (netdb) của mình, hãy xác minh rằng khóa tĩnh trong thông tin bộ định tuyến (router info) giống nhau ở cả hai phiên bản, nếu tồn tại, và nếu phiên bản cũ hơn chưa quá XXX tuổi (xem thời gian quay vòng khóa bên dưới)

- Bob phải xác thực rằng khóa tĩnh của Alice là một điểm hợp lệ trên đường cong tại đây.

- Các tùy chọn nên được bao gồm để xác định các tham số đệm.

- Khi xảy ra bất kỳ lỗi nào, bao gồm lỗi AEAD, RI, DH, dấu thời gian hoặc xác thực khóa, Bob phải dừng toàn bộ quá trình xử lý tin nhắn và đóng kết nối mà không phản hồi. Việc đóng kết nối này phải là đóng bất thường (TCP RST).

- Để tạo điều kiện cho việc bắt tay nhanh chóng, các triển khai phải đảm bảo rằng Alice sẽ lưu tạm và sau đó đẩy toàn bộ nội dung của tin nhắn thứ ba một lần, bao gồm cả hai khung AEAD. Việc này làm tăng khả năng dữ liệu sẽ nằm trong một gói TCP duy nhất (trừ khi bị phân mảnh bởi hệ điều hành hoặc các thiết bị trung gian), và được Bob nhận cùng lúc. Đây cũng là để nâng cao hiệu suất và đảm bảo hiệu quả của phần đệm ngẫu nhiên.

- Độ dài khung phần 2 của tin nhắn 3: Độ dài của khung này (bao gồm cả MAC) được Alice gửi trong tin nhắn 1. Xem tin nhắn đó để biết các lưu ý quan trọng về việc dành đủ không gian cho phần đệm.

- Nội dung khung phần tin nhắn 3 phần 2: Định dạng của khung này giống với định dạng các khung trong giai đoạn dữ liệu, ngoại trừ việc độ dài của khung được Alice gửi trong tin nhắn 1. Xem phần bên dưới để biết định dạng khung trong giai đoạn dữ liệu. Khung này phải chứa từ 1 đến 3 khối theo thứ tự sau:

1) Khối Thông tin Bộ định tuyến của Alice (bắt buộc)   2) Khối Tùy chọn (tùy chọn)

3\) Khối đệm (tùy chọn) Khung này không bao giờ được chứa bất kỳ loại khối nào khác.

- Phần đệm của tin nhắn 3, phần 2 là không bắt buộc nếu Alice thêm một khung pha dữ liệu (có thể chứa phần đệm) vào cuối tin nhắn 3 và gửi cả hai cùng lúc, vì đối với người quan sát, nó sẽ trông giống như một luồng byte lớn duy nhất. Vì thông thường (mặc dù không phải lúc nào cũng vậy) Alice sẽ có một tin nhắn I2NP để gửi cho Bob (đó là lý do cô ấy kết nối với anh ta), nên đây là cách triển khai được khuyến nghị nhằm tăng hiệu quả và đảm bảo hiệu lực của phần đệm ngẫu nhiên.

- Độ dài tối đa lý thuyết của cả hai khung Message 3 AEAD (phần 1 và 2) là 65535 byte; phần 1 dài 48 byte nên độ dài khung tối đa của phần 2 là 65487; độ dài văn bản gốc tối đa của phần 2 (không tính MAC) là 65471.
  CẢNH BÁO: Một số triển khai áp dụng giới hạn nhỏ hơn nhiều. Java I2P hiện đang giới hạn tổng độ dài ở mức 4096 byte. Không nên thêm khoảng đệm quá mức.

### Hàm suy xuất khóa (KDF) (cho giai đoạn dữ liệu)

Giai đoạn dữ liệu sử dụng đầu vào dữ liệu liên kết có độ dài bằng không.

KDF tạo ra hai khóa mật mã k_ab và k_ba từ khóa liên kết ck, sử dụng HMAC-SHA256(key, data) như được định nghĩa trong [RFC-2104](https://tools.ietf.org/html/rfc2104). Đây là hàm Split(), được định nghĩa chính xác như trong đặc tả Noise.

```
ck = from handshake phase

// k_ab, k_ba = HKDF(ck, zerolen)
// ask_master = HKDF(ck, zerolen, info="ask")

// zerolen is a zero-length byte array
temp_key = HMAC-SHA256(ck, zerolen)
// overwrite the chaining key in memory, no longer needed
ck = (all zeros)

// Output 1
// cipher key, for Alice transmits to Bob (Noise doesn't make clear which is which, but Java code does)
k_ab =   HMAC-SHA256(temp_key, byte(0x01)).

// Output 2
// cipher key, for Bob transmits to Alice (Noise doesn't make clear which is which, but Java code does)
k_ba =   HMAC-SHA256(temp_key, k_ab || byte(0x02)).


KDF for SipHash for length field:
Generate an Additional Symmetric Key (ask) for SipHash
SipHash uses two 8-byte keys (big endian) and 8 byte IV for first data.

// "ask" is 3 bytes, US-ASCII, no null termination
ask_master = HMAC-SHA256(temp_key, "ask" || byte(0x01))
// sip_master = HKDF(ask_master, h || "siphash")
// "siphash" is 7 bytes, US-ASCII, no null termination
// overwrite previous temp_key in memory
// h is from KDF for message 3 part 2
temp_key = HMAC-SHA256(ask_master, h || "siphash")
// overwrite ask_master in memory, no longer needed
ask_master = (all zeros)
sip_master = HMAC-SHA256(temp_key, byte(0x01))

Alice to Bob SipHash k1, k2, IV:
// sipkeys_ab, sipkeys_ba = HKDF(sip_master, zerolen)
// overwrite previous temp_key in memory
temp_key = HMAC-SHA256(sip_master, zerolen)
// overwrite sip_master in memory, no longer needed
sip_master = (all zeros)

sipkeys_ab = HMAC-SHA256(temp_key, byte(0x01)).
sipk1_ab = sipkeys_ab[0:7], little endian
sipk2_ab = sipkeys_ab[8:15], little endian
sipiv_ab = sipkeys_ab[16:23]

Bob to Alice SipHash k1, k2, IV:

sipkeys_ba = HMAC-SHA256(temp_key, sipkeys_ab || byte(0x02)).
sipk1_ba = sipkeys_ba[0:7], little endian
sipk2_ba = sipkeys_ba[8:15], little endian
sipiv_ba = sipkeys_ba[16:23]

// overwrite the temp_key in memory, no longer needed
temp_key = (all zeros)
```
### 4) Giai đoạn dữ liệu

Tải trọng nhiễu: Như được định nghĩa bên dưới, bao gồm độn ngẫu nhiên Tải trọng không nhiễu: không có

Bắt đầu từ phần thứ 2 của tin nhắn 3, tất cả các tin nhắn đều nằm bên trong một "khung" ChaChaPoly được xác thực và mã hóa, có độ dài hai byte được ngụy trang đặt ở đầu. Toàn bộ phần đệm đều nằm bên trong khung này. Bên trong khung là một định dạng chuẩn chứa zero hoặc nhiều "khối". Mỗi khối gồm một byte chỉ loại và hai byte chỉ độ dài. Các loại bao gồm ngày/giờ, tin nhắn I2NP, tùy chọn, kết thúc và đệm.

Lưu ý: Bob có thể, nhưng không bắt buộc, gửi RouterInfo của mình cho Alice như tin nhắn đầu tiên trong giai đoạn dữ liệu.

(Thuộc tính Bảo mật Payload từ [Noise](https://noiseprotocol.org/noise.html) )

```
XK(s, rs):           Authentication   Confidentiality
  <-                        2                5
  ->                        2                5

  Authentication: 2.
  Sender authentication resistant to key-compromise impersonation (KCI).
  The sender authentication is based on an ephemeral-static DH ("es" or "se")
  between the sender's static key pair and the recipient's ephemeral key pair.
  Assuming the corresponding private keys are secure, this authentication cannot be forged.

  Confidentiality: 5.
  Encryption to a known recipient, strong forward secrecy.
  This payload is encrypted based on an ephemeral-ephemeral DH as well as
  an ephemeral-static DH with the recipient's static key pair.
  Assuming the ephemeral private keys are secure, and the recipient is not being actively impersonated
  by an attacker that has stolen its static private key, this payload cannot be decrypted.
```
#### Ghi chú

- Để đảm bảo hiệu suất và giảm thiểu khả năng xác định trường độ dài, các triển khai phải đảm bảo bộ đệm bên gửi sau đó ghi toàn bộ nội dung của các tin nhắn dữ liệu một lần, bao gồm cả trường độ dài và khung AEAD. Việc này làm tăng khả năng dữ liệu sẽ được chứa trong một gói TCP duy nhất (trừ khi bị phân mảnh bởi hệ điều hành hoặc các thiết bị trung gian), và được bên kia nhận toàn bộ cùng lúc. Đây cũng là để tăng hiệu suất và đảm bảo hiệu quả của phần đệm ngẫu nhiên.
- Router có thể chọn chấm dứt phiên khi xảy ra lỗi AEAD, hoặc có thể tiếp tục cố gắng giao tiếp. Nếu tiếp tục, router nên chấm dứt sau khi xuất hiện nhiều lỗi lặp lại.

#### Độ dài bị làm mờ bởi SipHash

Tham khảo: [SipHash](https://www.131002.net/siphash/)

Sau khi cả hai bên hoàn tất quá trình bắt tay, chúng sẽ truyền các dữ liệu tải (payloads), sau đó được mã hóa và xác thực trong các "khung" (frames) ChaChaPoly.

Mỗi khung được bắt đầu bằng một độ dài hai byte, theo thứ tự big endian. Độ dài này xác định số byte khung đã mã hóa sẽ theo sau, bao gồm cả MAC. Để tránh việc truyền các trường độ dài có thể nhận dạng được trong luồng, độ dài khung được ngụy trang bằng cách XOR với một mặt nạ được tạo ra từ SipHash, như đã được khởi tạo từ KDF của giai đoạn dữ liệu. Lưu ý rằng hai hướng truyền dữ liệu có các khóa SipHash và IV riêng biệt được lấy từ KDF.

```
    sipk1, sipk2 = The SipHash keys from the KDF.  (two 8-byte long integers)
    IV[0] = sipiv = The SipHash IV from the KDF. (8 bytes)
    length is big endian.
    For each frame:
      IV[n] = SipHash-2-4(sipk1, sipk2, IV[n-1])
      Mask[n] = First 2 bytes of IV[n]
      obfuscatedLength = length ^ Mask[n]

    The first length output will be XORed with with IV[1].
```
Bên nhận có các khóa SipHash và IV hoàn toàn giống nhau. Việc giải mã độ dài được thực hiện bằng cách suy ra mặt nạ được dùng để làm rối độ dài, sau đó thực hiện phép XOR giữa bản băm đã cắt ngắn để thu được độ dài của khung dữ liệu. Độ dài khung là tổng độ dài của khung dữ liệu đã mã hóa, bao gồm cả mã xác thực (MAC).

#### Ghi chú

- Nếu bạn sử dụng một hàm thư viện SipHash trả về một số nguyên không dấu kiểu long, hãy dùng hai byte ít quan trọng nhất làm Mặt nạ (Mask). Chuyển đổi số nguyên long thành IV tiếp theo theo kiểu little endian.

#### Nội dung gốc

```
+----+----+----+----+----+----+----+----+
|obf size |                             |
+----+----+                             +
|                                       |
+   ChaChaPoly frame                    +
|   Encrypted and authenticated         |
+   key is k_ab for Alice to Bob        +
|   key is k_ba for Bob to Alice        |
+   as defined in KDF for data phase    +
|   n starts at 0 and increments        |
+   for each frame in that direction    +
|   no associated data                  |
+   16 bytes minimum                    +
|                                       |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+

obf size :: 2 bytes length obfuscated with SipHash
            when de-obfuscated: 16 - 65535

Minimum size including length field is 18 bytes.
Maximum size including length field is 65537 bytes.
Obfuscated length is 2 bytes.
Maximum ChaChaPoly frame is 65535 bytes.
```
#### Ghi chú

- Vì người nhận phải nhận toàn bộ khung để kiểm tra MAC, nên người gửi được khuyến nghị giới hạn kích thước khung vài KB thay vì tối đa hóa kích thước khung. Điều này sẽ giảm thiểu độ trễ ở phía người nhận.

#### Dữ liệu chưa được mã hóa

Có thể có từ không đến nhiều khối trong khung được mã hóa. Mỗi khối chứa một bộ định danh một byte, một độ dài hai byte và từ không đến nhiều byte dữ liệu.

Để đảm bảo khả năng mở rộng, các bộ nhận phải bỏ qua các khối có định danh không xác định và coi chúng như phần đệm.

Dữ liệu đã mã hóa tối đa là 65535 byte, bao gồm phần tiêu đề xác thực 16 byte, do đó dữ liệu chưa mã hóa tối đa là 65519 byte.

(thẻ xác thực Poly1305 không hiển thị):

```
+----+----+----+----+----+----+----+----+
|blk |  size   |       data             |
+----+----+----+                        +
|                                       |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+
|blk |  size   |       data             |
+----+----+----+                        +
|                                       |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+
~               .   .   .               ~

blk :: 1 byte
       0 for datetime
       1 for options
       2 for RouterInfo
       3 for I2NP message
       4 for termination
       224-253 reserved for experimental features
       254 for padding
       255 reserved for future extension
size :: 2 bytes, big endian, size of data to follow, 0 - 65516
data :: the data

Maximum ChaChaPoly frame is 65535 bytes.
Poly1305 tag is 16 bytes
Maximum total block size is 65519 bytes
Maximum single block size is 65519 bytes
Block type is 1 byte
Block length is 2 bytes
Maximum single block data size is 65516 bytes.
```
#### Quy tắc sắp xếp khối

Trong phần 2 của tin nhắn bắt tay số 3, thứ tự phải là: RouterInfo, tiếp theo là Options nếu có, rồi đến Padding nếu có. Không cho phép các khối khác.

Trong giai đoạn dữ liệu, thứ tự các khối không được quy định, ngoại trừ các yêu cầu sau: Nếu có Padding (dữ liệu đệm), khối này phải là khối cuối cùng. Nếu có Termination (kết thúc), khối này phải là khối cuối cùng, ngoại trừ khối Padding.

Có thể có nhiều khối I2NP trong một khung đơn. Không cho phép nhiều khối Padding trong một khung đơn. Các loại khối khác có lẽ sẽ không có nhiều khối trong một khung đơn, nhưng điều này không bị cấm.

#### Ngày giờ

Trường hợp đặc biệt cho đồng bộ hóa thời gian:

```
+----+----+----+----+----+----+----+
| 0  |    4    |     timestamp     |
+----+----+----+----+----+----+----+

blk :: 0
size :: 2 bytes, big endian, value = 4
timestamp :: Unix timestamp, unsigned seconds.
             Wraps around in 2106
```
LƯU Ý: Các triển khai phải làm tròn đến giây gần nhất để ngăn ngừa sai lệch đồng hồ trong mạng.

#### Tùy chọn

Truyền các tùy chọn đã cập nhật. Các tùy chọn bao gồm: độ đệm tối thiểu và tối đa.

Khối tùy chọn sẽ có độ dài thay đổi.

```
+----+----+----+----+----+----+----+----+
| 1  |  size   |tmin|tmax|rmin|rmax|tdmy|
+----+----+----+----+----+----+----+----+
|tdmy|  rdmy   |  tdelay |  rdelay |    |
~----+----+----+----+----+----+----+    ~
|              more_options             |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+

blk :: 1
size :: 2 bytes, big endian, size of options to follow, 12 bytes minimum

tmin, tmax, rmin, rmax :: requested padding limits
    tmin and rmin are for desired resistance to traffic analysis.
    tmax and rmax are for bandwidth limits.
    tmin and tmax are the transmit limits for the router sending this options block.
    rmin and rmax are the receive limits for the router sending this options block.
    Each is a 4.4 fixed-point float representing 0 to 15.9375
    (or think of it as an unsigned 8-bit integer divided by 16.0).
    This is the ratio of padding to data. Examples:
    Value of 0x00 means no padding
    Value of 0x01 means add 6 percent padding
    Value of 0x10 means add 100 percent padding
    Value of 0x80 means add 800 percent (8x) padding
    Alice and Bob will negotiate the minimum and maximum in each direction.
    These are guidelines, there is no enforcement.
    Sender should honor receiver's maximum.
    Sender may or may not honor receiver's minimum, within bandwidth constraints.

tdmy: Max dummy traffic willing to send, 2 bytes big endian, bytes/sec average
rdmy: Requested dummy traffic, 2 bytes big endian, bytes/sec average
tdelay: Max intra-message delay willing to insert, 2 bytes big endian, msec average
rdelay: Requested intra-message delay, 2 bytes big endian, msec average

Padding distribution specified as additional parameters?
Random delay specified as additional parameters?

more_options :: Format TBD
```
#### Các vấn đề về Tùy chọn

- Định dạng tùy chọn là TBD.
- Thương lượng tùy chọn là TBD.

#### RouterInfo

Chuyển RouterInfo của Alice cho Bob. Được sử dụng trong phần 2 của tin nhắn bắt tay thứ 3. Chuyển RouterInfo của Alice cho Bob, hoặc của Bob cho Alice. Được sử dụng tùy chọn trong giai đoạn truyền dữ liệu.

```
+----+----+----+----+----+----+----+----+
| 2  |  size   |flg |    RouterInfo     |
+----+----+----+----+                   +
| (Alice RI in handshake msg 3 part 2)  |
~ (Alice, Bob, or third-party           ~
|  RI in data phase)                    |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+

blk :: 2
size :: 2 bytes, big endian, size of flag + router info to follow
flg :: 1 byte flags
       bit order: 76543210
       bit 0: 0 for local store, 1 for flood request
       bits 7-1: Unused, set to 0 for future compatibility
routerinfo :: Alice's or Bob's RouterInfo
```
#### Ghi chú

- Khi được sử dụng trong giai đoạn dữ liệu, bên nhận (Alice hoặc Bob) phải xác minh rằng đây là cùng một Router Hash như đã được gửi ban đầu (đối với Alice) hoặc đã được gửi tới (đối với Bob). Sau đó, xử lý như một tin nhắn I2NP DatabaseStore cục bộ. Xác minh chữ ký, xác minh dấu thời gian mới hơn, và lưu vào cơ sở dữ liệu mạng (netdb) cục bộ. Nếu bit cờ 0 là 1 và bên nhận là máy floodfill, hãy xử lý như một tin nhắn DatabaseStore có mã trả lời (reply token) khác 0, và phát tán đến các máy floodfill gần nhất.
- Thông tin Router (Router Info) KHÔNG được nén bằng gzip (khác với tin nhắn DatabaseStore, nơi nó được nén).
- Không được yêu cầu phát tán (flooding) trừ khi có các RouterAddresses đã công khai trong RouterInfo. Bộ định tuyến nhận phải không phát tán RouterInfo trừ khi có các RouterAddresses đã công khai trong đó.
- Những người triển khai phải đảm bảo rằng khi đọc một khối dữ liệu, dữ liệu bị lỗi hoặc độc hại sẽ không khiến việc đọc vượt quá ranh giới sang khối tiếp theo.
- Giao thức này không cung cấp xác nhận rằng RouterInfo đã được nhận, lưu trữ hoặc phát tán (dù ở giai đoạn bắt tay hay giai đoạn dữ liệu). Nếu cần xác nhận, và bên nhận là floodfill, người gửi nên gửi một tin nhắn I2NP DatabaseStoreMessage tiêu chuẩn có mã trả lời (reply token).

#### Vấn đề

- Cũng có thể được sử dụng trong giai đoạn dữ liệu, thay vì sử dụng I2NP DatabaseStoreMessage. Ví dụ, Bob có thể dùng nó để khởi đầu giai đoạn dữ liệu.
- Liệu có được phép để thông điệp này chứa RI của các router khác ngoài người khởi tạo, như một sự thay thế tổng quát cho DatabaseStoreMessage, ví dụ như trong việc lan truyền (flooding) bởi các floodfill?

#### Tin nhắn I2NP

Một tin nhắn I2NP duy nhất với phần tiêu đề đã được sửa đổi. Các tin nhắn I2NP không được phép bị phân mảnh qua các khối hoặc qua các khung ChaChaPoly.

Phần này sử dụng 9 byte đầu tiên từ tiêu đề I2NP NTCP tiêu chuẩn, và loại bỏ 7 byte cuối của tiêu đề, như sau: rút ngắn thời gian hết hạn từ 8 byte xuống còn 4 byte (tính bằng giây thay vì mili giây, giống như SSU), loại bỏ độ dài 2 byte (sử dụng kích thước khối trừ đi 9), và loại bỏ phần kiểm tra SHA256 một byte.

```
+----+----+----+----+----+----+----+----+
| 3  |  size   |type|    msg id         |
+----+----+----+----+----+----+----+----+
|   short exp       |     message       |
+----+----+----+----+                   +
|                                       |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+

blk :: 3
size :: 2 bytes, big endian, size of type + msg id + exp + message to follow
        I2NP message body size is (size - 9).
type :: 1 byte, I2NP msg type, see I2NP spec
msg id :: 4 bytes, big endian, I2NP message ID
short exp :: 4 bytes, big endian, I2NP message expiration, Unix timestamp, unsigned seconds.
             Wraps around in 2106
message :: I2NP message body
```
#### Ghi chú

- Các nhà triển khai phải đảm bảo rằng khi đọc một khối dữ liệu, dữ liệu bị lỗi hoặc độc hại sẽ không gây ra việc đọc tràn sang khối tiếp theo.

#### Chấm dứt

Noise khuyến nghị một thông điệp chấm dứt rõ ràng. NTCP gốc không có thông điệp này. Hãy ngắt kết nối. Đây phải là khối cuối cùng không phải dữ liệu đệm trong khung.

```
+----+----+----+----+----+----+----+----+
| 4  |  size   |    valid data frames   |
+----+----+----+----+----+----+----+----+
    received   | rsn|     addl data     |
+----+----+----+----+                   +
~               .   .   .               ~
+----+----+----+----+----+----+----+----+

blk :: 4
size :: 2 bytes, big endian, value = 9 or more
valid data frames received :: The number of valid AEAD data phase frames received
                              (current receive nonce value)
                              0 if error occurs in handshake phase
                              8 bytes, big endian
rsn :: reason, 1 byte:
       0: normal close or unspecified
       1: termination received
       2: idle timeout
       3: router shutdown
       4: data phase AEAD failure
       5: incompatible options
       6: incompatible signature type
       7: clock skew
       8: padding violation
       9: AEAD framing error
       10: payload format error
       11: message 1 error
       12: message 2 error
       13: message 3 error
       14: intra-frame read timeout
       15: RI signature verification fail
       16: s parameter missing, invalid, or mismatched in RouterInfo
       17: banned
addl data :: optional, 0 or more bytes, for future expansion, debugging,
             or reason text.
             Format unspecified and may vary based on reason code.
```
#### Ghi chú

Không phải tất cả các lý do đều thực sự được sử dụng, tùy thuộc vào cách triển khai. Các lỗi bắt tay thường dẫn đến việc đóng kết nối bằng TCP RST. Xem phần ghi chú trong các mục tin nhắn bắt tay ở trên. Các lý do bổ sung được liệt kê nhằm đảm bảo tính nhất quán, ghi log, gỡ lỗi hoặc trong trường hợp chính sách thay đổi.

#### Đệm

Điều này dùng để chèn khoảng trắng bên trong các khung AEAD. Khoảng trắng cho thông điệp 1 và 2 nằm ngoài các khung AEAD. Toàn bộ khoảng trắng cho thông điệp 3 và giai đoạn dữ liệu đều nằm bên trong các khung AEAD.

Việc chèn độn bên trong AEAD nên tuân thủ một cách tương đối các tham số đã thỏa thuận. Bob đã gửi các tham số tối thiểu/tối đa tx/rx mà anh ta yêu cầu trong tin nhắn 2. Alice đã gửi các tham số tối thiểu/tối đa tx/rx mà cô ấy yêu cầu trong tin nhắn 3. Các tùy chọn cập nhật có thể được gửi trong giai đoạn dữ liệu. Xem phần thông tin khối tùy chọn ở trên.

Nếu có mặt, đây phải là khối cuối cùng trong khung.

```
+----+----+----+----+----+----+----+----+
|254 |  size   |      padding           |
+----+----+----+                        +
|                                       |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+

blk :: 254
size :: 2 bytes, big endian, size of padding to follow
padding :: random data
```
#### Ghi chú

- Cho phép kích thước bằng 0.
- Chiến lược chèn độn (padding) sẽ được xác định sau (TBD).
- Mức độ chèn độn tối thiểu sẽ được xác định sau (TBD).
- Cho phép các khung chỉ chứa dữ liệu chèn độn (padding-only frames).
- Giá trị mặc định của độ chèn độn sẽ được xác định sau (TBD).
- Xem khối tùy chọn để thương lượng tham số chèn độn
- Xem khối tùy chọn để biết các tham số độ chèn độn tối thiểu/tối đa
- Noise giới hạn tin nhắn tối đa 64KB. Nếu cần chèn độn nhiều hơn, hãy gửi nhiều khung tin.
- Phản hồi của router khi vi phạm quy định chèn độn đã thương lượng phụ thuộc vào cách triển khai.

#### Các loại khối khác

Các triển khai nên bỏ qua các loại khối chưa biết để đảm bảo khả năng tương thích ngược, ngoại trừ trong phần 2 của thông điệp 3, nơi không cho phép các khối chưa biết.

#### Công việc trong tương lai

- Độ dài dữ liệu đệm hoặc cần được quyết định cho từng tin nhắn riêng lẻ dựa trên ước tính phân bố độ dài, hoặc nên thêm các khoảng trễ ngẫu nhiên. Những biện pháp đối phó này cần được áp dụng để chống lại việc kiểm tra gói tin sâu (DPI), bởi vì kích thước tin nhắn nếu không sẽ tiết lộ rằng giao thức truyền tải đang mang lưu lượng I2P. Sơ đồ đệm cụ thể là một lĩnh vực cần nghiên cứu trong tương lai.

### 5) Chấm dứt

Các kết nối có thể bị chấm dứt thông qua việc đóng socket TCP bình thường hoặc bất thường, hoặc, như Noise khuyến nghị, một thông điệp chấm dứt rõ ràng. Thông điệp chấm dứt rõ ràng được định nghĩa trong giai đoạn dữ liệu ở trên.

Khi kết thúc bình thường hay bất thường, các bộ định tuyến nên xóa sạch mọi dữ liệu tạm thời trong bộ nhớ, bao gồm các khóa tạm thời dùng trong bắt tay, các khóa mật mã đối xứng và các thông tin liên quan.

## Thông tin Bộ định tuyến đã Xuất bản

### Khả năng

Kể từ phiên bản 0.9.50, tùy chọn "caps" được hỗ trợ trong địa chỉ NTCP2, tương tự như SSU. Một hoặc nhiều khả năng có thể được công bố trong tùy chọn "caps". Các khả năng có thể ở bất kỳ thứ tự nào, nhưng thứ tự "46" được khuyến nghị để đảm bảo tính nhất quán giữa các triển khai. Có hai khả năng được định nghĩa:

4: Chỉ thị khả năng IPv4 đi ra ngoài. Nếu một địa chỉ IP được công bố trong trường host, khả năng này không cần thiết. Nếu router được ẩn, hoặc NTCP2 chỉ hoạt động theo chiều đi ra, '4' và '6' có thể được kết hợp trong một địa chỉ duy nhất.

6: Chỉ thị khả năng IPv6 đi ra. Nếu một địa chỉ IP được công bố trong trường host, khả năng này không cần thiết. Nếu router được ẩn, hoặc NTCP2 chỉ hoạt động theo hướng đi ra, '4' và '6' có thể được kết hợp trong một địa chỉ duy nhất.

### Địa chỉ đã xuất bản

Địa chỉ Router được công bố (một phần của RouterInfo) sẽ có định danh giao thức là "NTCP" hoặc "NTCP2".

RouterAddress phải chứa các tùy chọn "host" và "port", giống như trong giao thức NTCP hiện tại.

RouterAddress phải chứa ba tùy chọn để chỉ hỗ trợ NTCP2:

- s=(khóa Base64) Khóa công khai tĩnh hiện tại (s) cho RouterAddress này. Được mã hóa Base64 sử dụng bảng chữ cái Base64 chuẩn của I2P. 32 byte dạng nhị phân, 44 byte dạng mã hóa Base64, khóa công khai X25519 theo thứ tự little-endian.
- i=(IV Base64) IV hiện tại để mã hóa giá trị X trong thông điệp 1 cho RouterAddress này. Được mã hóa Base64 sử dụng bảng chữ cái Base64 chuẩn của I2P. 16 byte dạng nhị phân, 24 byte dạng mã hóa Base64, theo thứ tự big-endian.
- v=2 Phiên bản hiện tại (2). Khi được công bố là "NTCP", ngụ ý có hỗ trợ thêm cho phiên bản 1. Việc hỗ trợ các phiên bản trong tương lai sẽ sử dụng các giá trị phân tách bằng dấu phẩy, ví dụ: v=2,3. Việc triển khai cần xác minh tính tương thích, bao gồm nhiều phiên bản nếu có dấu phẩy. Các phiên bản phân tách bằng dấu phẩy phải được sắp xếp theo thứ tự số học.

Alice phải xác minh rằng cả ba tùy chọn đều có mặt và hợp lệ trước khi kết nối bằng giao thức NTCP2.

Khi được công bố với tư cách là "NTCP" cùng các tùy chọn "s", "i", và "v", bộ định tuyến phải chấp nhận các kết nối đến trên máy chủ và cổng đó cho cả hai giao thức NTCP và NTCP2, đồng thời tự động phát hiện phiên bản giao thức.

Khi được công bố dưới dạng "NTCP2" với các tùy chọn "s", "i" và "v", bộ định tuyến sẽ chấp nhận các kết nối đến trên máy chủ và cổng đó chỉ cho giao thức NTCP2.

Nếu một router hỗ trợ cả kết nối NTCP1 và NTCP2 nhưng không triển khai việc tự động phát hiện phiên bản cho các kết nối đến, thì nó phải công bố cả hai địa chỉ "NTCP" và "NTCP2", đồng thời chỉ đưa các tùy chọn NTCP2 vào địa chỉ "NTCP2". Router nên đặt giá trị chi phí thấp hơn (ưu tiên cao hơn) trong địa chỉ "NTCP2" so với địa chỉ "NTCP", để ưu tiên sử dụng NTCP2.

Nếu nhiều RouterAddress NTCP2 (dưới dạng "NTCP" hoặc "NTCP2") được công bố trong cùng một RouterInfo (cho các địa chỉ IP hoặc cổng bổ sung), tất cả các địa chỉ chỉ định cùng một cổng phải chứa các tùy chọn và giá trị NTCP2 giống hệt nhau. Đặc biệt, tất cả chúng phải chứa cùng một khóa tĩnh (static key) và iv.

### Địa chỉ NTCP2 chưa được công bố

Nếu Alice không công bố địa chỉ NTCP2 của cô (như "NTCP" hoặc "NTCP2") để nhận kết nối đến, cô phải công bố một địa chỉ bộ định tuyến "NTCP2" chỉ chứa khóa tĩnh và phiên bản NTCP2, để Bob có thể xác thực khóa sau khi nhận RouterInfo của Alice trong phần 2 của tin nhắn 3.

- s=(khóa Base64) Như đã định nghĩa ở trên cho các địa chỉ được công bố.
- v=2 Như đã định nghĩa ở trên cho các địa chỉ được công bố.

Địa chỉ router này sẽ không chứa các tùy chọn "i", "host" hoặc "port", vì chúng không cần thiết cho kết nối NTCP2 đi ra. Chi phí được công bố cho địa chỉ này không quá quan trọng, vì nó chỉ dùng cho kết nối đến; tuy nhiên, có thể hữu ích cho các router khác nếu chi phí được đặt cao hơn (ưu tiên thấp hơn) so với các địa chỉ khác. Giá trị đề xuất là 14.

Alice cũng có thể đơn giản thêm các tùy chọn "s" và "v" vào một địa chỉ "NTCP" đã được công bố trước đó.

### Quay vòng Khóa công khai và IV

Do việc lưu trữ bộ đệm RouterInfos, các bộ định tuyến không được phép thay đổi khóa công khai tĩnh hoặc IV khi bộ định tuyến đang hoạt động, bất kể có được công bố trong một địa chỉ hay không. Các bộ định tuyến phải lưu trữ bền vững khóa và IV này để sử dụng lại sau khi khởi động lại ngay lập tức, nhằm đảm bảo các kết nối đến vẫn hoạt động và thời gian khởi động lại không bị tiết lộ. Các bộ định tuyến phải lưu trữ bền vững, hoặc xác định bằng cách khác, thời điểm tắt máy lần trước, để có thể tính toán khoảng thời gian ngừng hoạt động trước đó khi khởi động.

Tùy theo mức độ lo ngại về việc tiết lộ thời gian khởi động lại, các router có thể xoay khóa hoặc IV này khi khởi động nếu trước đó router đã tắt trong một khoảng thời gian (ít nhất vài giờ).

Nếu router có bất kỳ RouterAddress NTCP2 nào đã được công khai (dưới dạng NTCP hoặc NTCP2), thời gian ngừng hoạt động tối thiểu trước khi luân chuyển nên dài hơn nhiều, ví dụ một tháng, trừ khi địa chỉ IP cục bộ đã thay đổi hoặc router "tái tạo khóa" (rekeys).

Nếu router có bất kỳ SSU RouterAddress nào đã được công bố, nhưng không có NTCP2 (dưới dạng NTCP hoặc NTCP2), thời gian ngừng hoạt động tối thiểu trước khi luân chuyển nên dài hơn, ví dụ một ngày, trừ khi địa chỉ IP cục bộ đã thay đổi hoặc router thực hiện "khóa lại". Điều này áp dụng ngay cả khi địa chỉ SSU đã công bố có các bộ giới thiệu (introducers).

Nếu bộ định tuyến không có bất kỳ RouterAddress nào được công bố (NTCP, NTCP2 hoặc SSU), thời gian ngừng hoạt động tối thiểu trước khi luân chuyển có thể ngắn tới hai giờ, ngay cả khi địa chỉ IP thay đổi, trừ khi bộ định tuyến thực hiện "khóa lại" (rekeys).

Nếu bộ định tuyến "tạo lại khóa" sang một Router Hash khác, nó cũng nên tạo một khóa nhiễu (noise key) và IV mới.

Các triển khai cần lưu ý rằng việc thay đổi khóa công khai tĩnh hoặc IV sẽ ngăn chặn các kết nối NTCP2 đến từ các router đã lưu vào bộ nhớ đệm RouterInfo cũ hơn. Việc xuất bản RouterInfo, lựa chọn peer cho tunnel (bao gồm cả OBGW và IB hop gần nhất), lựa chọn tunnel zero-hop, lựa chọn transport và các chiến lược triển khai khác phải tính đến yếu tố này.

Việc xoay IV tuân theo các quy tắc giống hệt như việc xoay khóa, ngoại trừ việc IV không tồn tại ngoài trừ trong các RouterAddress đã công bố, do đó không có IV dành cho các router ẩn hoặc bị tường lửa. Nếu có bất kỳ thay đổi nào (phiên bản, khóa, tùy chọn?), việc thay đổi IV cũng được khuyến nghị.

Lưu ý: Thời gian ngừng hoạt động tối thiểu trước khi thay đổi khóa có thể được điều chỉnh để đảm bảo sức khỏe của mạng và ngăn việc cập nhật lại nguồn (reseeding) bởi một router đã tắt trong một khoảng thời gian vừa phải.

## Phát hiện phiên bản

Khi được công bố dưới dạng "NTCP", bộ định tuyến phải tự động phát hiện phiên bản giao thức cho các kết nối đến.

Việc phát hiện này phụ thuộc vào cách triển khai, nhưng dưới đây là một số hướng dẫn chung.

Để phát hiện phiên bản của một kết nối NTCP đến, Bob thực hiện như sau:

- Chờ ít nhất 64 byte (kích thước tối thiểu tin nhắn NTCP2 1)

- Nếu dữ liệu nhận ban đầu là 288 byte hoặc nhiều hơn, kết nối đến là phiên bản 1.

- Nếu nhỏ hơn 288 byte, một trong hai

> - Chờ trong thời gian ngắn để nhận thêm dữ liệu (chiến lược tốt trước khi NTCP2 được áp dụng rộng rãi) nếu đã nhận được tổng cộng ít nhất 288 byte, đây là NTCP 1.  
  > - Thử giải mã theo các bước đầu tiên của phiên bản 2, nếu thất bại, hãy chờ trong thời gian ngắn để nhận thêm dữ liệu (chiến lược tốt sau khi NTCP2 được áp dụng rộng rãi)  
  > - Giải mã 32 byte đầu tiên (khóa X) của gói SessionRequest bằng AES-256 với khóa RH_B  
  > - Xác minh điểm hợp lệ trên đường cong. Nếu thất bại, chờ trong thời gian ngắn để nhận thêm dữ liệu cho NTCP 1  
  > - Xác minh khung AEAD. Nếu thất bại, chờ trong thời gian ngắn để nhận thêm dữ liệu cho NTCP 1

Lưu ý rằng các thay đổi hoặc chiến lược bổ sung có thể được đề xuất nếu chúng tôi phát hiện các cuộc tấn công phân đoạn TCP đang diễn ra trên NTCP 1.

Để tạo điều kiện phát hiện phiên bản và bắt tay nhanh chóng, các triển khai phải đảm bảo rằng Alice lưu tạm và sau đó đẩy toàn bộ nội dung của tin nhắn đầu tiên cùng lúc, bao gồm cả phần đệm ngẫu nhiên. Việc này làm tăng khả năng dữ liệu sẽ nằm gọn trong một gói TCP duy nhất (trừ khi bị phân mảnh bởi hệ điều hành hoặc các thiết bị trung gian), và được Bob nhận toàn bộ cùng lúc. Điều này cũng nhằm mục đích hiệu quả và đảm bảo hiệu lực của phần đệm ngẫu nhiên. Quy tắc này áp dụng cho cả quá trình bắt tay NTCP lẫn NTCP2.

## Các biến thể, phương án dự phòng và các vấn đề chung

- Nếu Alice và Bob đều hỗ trợ NTCP2, Alice nên kết nối bằng NTCP2.
- Nếu Alice không thể kết nối với Bob bằng NTCP2 vì bất kỳ lý do gì, phiên kết nối sẽ thất bại. Alice không được phép thử lại bằng NTCP 1.

## Hướng dẫn về Lệch giờ

Thời điểm của các peer được đưa vào hai tin nhắn bắt tay đầu tiên, Yêu cầu phiên (Session Request) và Phiên đã tạo (Session Created). Sự chênh lệch thời gian (clock skew) giữa hai peer vượt quá +/- 60 giây thường gây lỗi nghiêm trọng. Nếu Bob cho rằng đồng hồ cục bộ của anh ấy không chính xác, anh ấy có thể điều chỉnh đồng hồ bằng cách sử dụng độ chênh lệch đã tính toán hoặc một nguồn bên ngoài. Nếu không, Bob nên phản hồi bằng một tin nhắn Session Created ngay cả khi độ chênh lệch vượt quá giới hạn tối đa, thay vì đơn giản là đóng kết nối. Việc này cho phép Alice nhận được thời điểm của Bob, tính toán độ chênh lệch và thực hiện các hành động cần thiết. Ở thời điểm này, Bob chưa có định danh router của Alice, nhưng để tiết kiệm tài nguyên, Bob có thể tạm chặn các kết nối đến từ địa chỉ IP của Alice trong một khoảng thời gian nhất định, hoặc sau nhiều lần thử kết nối liên tiếp với độ chênh lệch quá mức.

Alice nên điều chỉnh độ lệch đồng hồ đã tính bằng cách trừ đi một nửa thời gian vòng đi-về (RTT). Nếu Alice cho rằng đồng hồ cục bộ của cô ấy không chính xác, cô ấy có thể điều chỉnh đồng hồ của mình bằng độ lệch đã tính được, hoặc sử dụng một nguồn bên ngoài khác. Nếu Alice cho rằng đồng hồ của Bob không chính xác, cô ấy có thể cấm Bob trong một khoảng thời gian nhất định. Trong cả hai trường hợp, Alice nên đóng kết nối.

Nếu Alice phản hồi bằng Session Confirmed (có thể vì độ lệch đồng hồ rất gần với giới hạn 60 giây, và phép tính độ lệch ở Alice và Bob không hoàn toàn giống nhau do RTT), Bob nên điều chỉnh độ lệch đồng hồ đã tính bằng cách trừ đi một nửa RTT. Nếu độ lệch đồng hồ đã điều chỉnh vượt quá giới hạn tối đa, Bob nên phản hồi bằng một tin nhắn Disconnect chứa mã lý do về độ lệch đồng hồ, rồi đóng kết nối. Tại thời điểm này, Bob đã có định danh router của Alice và có thể cấm Alice trong một khoảng thời gian nhất định.

## Tài liệu tham khảo

- [Các cấu trúc phổ biến](/docs/specs/common-structures)
- [I2NP](/docs/specs/i2np)
- [Cơ sở dữ liệu mạng](/docs/overview/network-database)
- [NOISE - Khung giao thức Noise](https://noiseprotocol.org/noise.html)
- [NTCP](/docs/transport/ntcp)
- [Prop104](/proposals/104-tls-transport)
- [Prop109](/proposals/109-pt-transport)
- [Prop111](/proposals/111-ntcp-2)
- [RFC-2104 - HMAC](https://tools.ietf.org/html/rfc2104)
- [RFC-3526 - Nhóm DH](https://tools.ietf.org/html/rfc3526)
- [RFC-6151](https://tools.ietf.org/html/rfc6151)
- [RFC-7539 - ChaCha20-Poly1305](https://tools.ietf.org/html/rfc7539)
- [RFC-7748 - X25519](https://tools.ietf.org/html/rfc7748)
- [RFC-7905](https://tools.ietf.org/html/rfc7905)
- [SipHash](https://www.131002.net/siphash/)
- [SSU](/docs/transport/ssu)
- **[STS]** Diffie, W.; van Oorschot P. C.; Wiener M. J., Xác thực và Trao đổi khóa được xác thực
