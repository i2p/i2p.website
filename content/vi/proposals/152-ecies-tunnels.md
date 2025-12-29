---
title: "Các tunnel ECIES"
number: "152"
author: "chisana, zzz, orignal"
created: "2019-07-04"
lastupdated: "2025-03-05"
status: "Đã đóng"
thread: "http://zzz.i2p/topics/2737"
target: "0.9.48"
implementedin: "0.9.48"
toc: true
---

## Lưu ý

Việc triển khai và kiểm thử mạng đang được tiến hành. Có thể sẽ có các điều chỉnh nhỏ. Xem [SPEC](/docs/specs/implementation/) để biết đặc tả chính thức.

## Tổng quan

Tài liệu này đề xuất các thay đổi đối với việc mã hóa thông điệp Tunnel Build bằng cách sử dụng các nguyên thủy mật mã được giới thiệu bởi [ECIES-X25519](/docs/specs/ecies/). Đây là một phần của đề xuất tổng thể [Proposal 156](/proposals/156-ecies-routers) nhằm chuyển đổi routers từ ElGamal sang các khóa ECIES-X25519.

Để phục vụ việc chuyển đổi mạng từ ElGamal + AES256 sang ECIES + ChaCha20, các tunnels với các routers ElGamal và ECIES trộn lẫn là cần thiết. Các đặc tả kỹ thuật để xử lý các hop (chặng) trong tunnel hỗn hợp được cung cấp. Sẽ không có thay đổi nào đối với định dạng, xử lý hoặc mã hóa của các hop ElGamal.

Những người tạo tunnel ElGamal sẽ cần tạo các cặp khóa X25519 tạm thời cho mỗi hop (bước nhảy), và tuân theo đặc tả này để tạo các tunnel chứa các hop ECIES.

Đề xuất này nêu rõ các thay đổi cần thiết cho việc xây dựng Tunnel bằng ECIES-X25519. Để có cái nhìn tổng quan về tất cả các thay đổi cần thiết cho ECIES routers, xem đề xuất 156 [Đề xuất 156](/proposals/156-ecies-routers).

Đề xuất này giữ nguyên kích thước của các bản ghi xây dựng tunnel, theo yêu cầu để đảm bảo khả năng tương thích. Các bản ghi xây dựng và thông điệp nhỏ hơn sẽ được triển khai sau - xem [Proposal 157](/proposals/157-new-tbm).

### Các nguyên thủy mật mã

Không có phép nguyên thủy mật mã mới nào được giới thiệu. Các phép nguyên thủy cần thiết để triển khai đề xuất này là:

- AES-256-CBC như trong [Mật mã học](/docs/specs/cryptography/)
- Các hàm STREAM ChaCha20/Poly1305:
  ENCRYPT(k, n, plaintext, ad) và DECRYPT(k, n, ciphertext, ad) - như trong [NTCP2](/docs/specs/ntcp2/) [ECIES-X25519](/docs/specs/ecies/) và [RFC-7539](https://tools.ietf.org/html/rfc7539)
- Các hàm DH X25519 - như trong [NTCP2](/docs/specs/ntcp2/) và [ECIES-X25519](/docs/specs/ecies/)
- HKDF(salt, ikm, info, n) (hàm dẫn xuất khóa dựa trên HMAC) - như trong [NTCP2](/docs/specs/ntcp2/) và [ECIES-X25519](/docs/specs/ecies/)

Các hàm Noise (khuôn khổ giao thức mật mã) khác được định nghĩa ở nơi khác:

- MixHash(d) (hàm trộn băm) - như trong [NTCP2](/docs/specs/ntcp2/) và [ECIES-X25519](/docs/specs/ecies/)
- MixKey(d) (hàm trộn khóa) - như trong [NTCP2](/docs/specs/ntcp2/) và [ECIES-X25519](/docs/specs/ecies/)

### Mục tiêu


### Các mục tiêu không đặt ra

- Thiết kế lại hoàn toàn các thông điệp dựng tunnel, yêu cầu một "flag day" (thời điểm chuyển đổi đồng loạt không tương thích ngược).
- Thu nhỏ các thông điệp dựng tunnel (yêu cầu các hop (chặng trung gian) đều dùng ECIES và một đề xuất mới)
- Sử dụng các tùy chọn dựng tunnel như được định nghĩa trong [Proposal 143](/proposals/143-build-message-options), chỉ bắt buộc đối với các thông điệp nhỏ
- Các tunnel hai chiều - xem [Proposal 119](/proposals/119-bidirectional-tunnels)
- Các thông điệp dựng tunnel nhỏ hơn - xem [Proposal 157](/proposals/157-new-tbm)

## Mô hình đe dọa

### Mục tiêu thiết kế

- Không có nút trung gian nào có thể xác định được bên khởi tạo của tunnel.

- Các hop (chặng) trung gian không thể xác định hướng của tunnel
  hoặc vị trí của mình trong tunnel.

- Không chặng nào có thể đọc bất kỳ nội dung nào của các bản ghi yêu cầu hoặc phản hồi khác, ngoại trừ
  hash router đã bị cắt ngắn và khóa tạm thời cho chặng tiếp theo

- Không thành viên nào của tunnel phản hồi dùng cho outbound build (quá trình dựng tunnel đi ra) có thể đọc bất kỳ bản ghi phản hồi nào.

- Không thành viên nào của tunnel đi ra dùng cho việc xây dựng tunnel đi vào có thể đọc bất kỳ bản ghi yêu cầu nào,
  ngoại trừ việc OBEP (Outbound Endpoint - nút cuối của outbound tunnel) có thể thấy hash router bị cắt ngắn và khóa tạm thời dành cho IBGW (Inbound Gateway - cổng vào của inbound tunnel)

### Các cuộc tấn công gắn thẻ (tagging attacks)

Một mục tiêu quan trọng của thiết kế xây dựng tunnel là khiến việc các router X và Y thông đồng biết rằng chúng đang ở trong cùng một tunnel trở nên khó khăn hơn. Nếu router X ở bước nhảy m và router Y ở bước nhảy m+1, hiển nhiên chúng sẽ biết. Nhưng nếu router X ở bước nhảy m và router Y ở bước nhảy m+n với n>1, thì điều đó sẽ khó hơn nhiều.

Tấn công gắn thẻ là khi router ở chặng trung gian X sửa đổi thông điệp xây dựng tunnel theo cách để router Y có thể phát hiện sự sửa đổi đó khi thông điệp đến nơi. Mục tiêu là mọi thông điệp đã bị sửa đổi sẽ bị một router nằm giữa X và Y loại bỏ trước khi nó tới router Y. Đối với các sửa đổi không bị loại bỏ trước router Y, router tạo tunnel phải phát hiện dữ liệu bị hỏng trong phản hồi và hủy bỏ tunnel.

Các cuộc tấn công có thể xảy ra:

- Sửa đổi một build record (bản ghi xây dựng)
- Thay thế một build record
- Thêm hoặc xóa một build record
- Sắp xếp lại các build record

TODO: Thiết kế hiện tại có ngăn chặn tất cả các cuộc tấn công này không?

## Thiết kế

### Noise Protocol Framework (khung giao thức Noise)

Đề xuất này nêu các yêu cầu dựa trên Noise Protocol Framework [NOISE](https://noiseprotocol.org/noise.html) (Bản sửa đổi 34, 2018-07-11). Theo thuật ngữ của Noise, Alice là bên khởi tạo (initiator), và Bob là bên phản hồi (responder).

Đề xuất này dựa trên giao thức Noise Noise_N_25519_ChaChaPoly_SHA256. Giao thức Noise này sử dụng các nguyên thủy mật mã sau:

- Mẫu bắt tay một chiều: N
  Alice không gửi khóa tĩnh của mình cho Bob (N)

- Hàm DH: X25519
  X25519 DH với độ dài khóa 32 byte như được quy định trong [RFC-7748](https://tools.ietf.org/html/rfc7748).

- Hàm mật mã: ChaChaPoly
  AEAD_CHACHA20_POLY1305 như được quy định trong [RFC-7539](https://tools.ietf.org/html/rfc7539) Mục 2.8.
  Nonce (giá trị dùng một lần) 12 byte, với 4 byte đầu được đặt về 0.
  Giống hệt như trong [NTCP2](/docs/specs/ntcp2/).

- Hàm băm: SHA256
  Mã băm tiêu chuẩn 32 byte, đã được sử dụng rộng rãi trong I2P.

#### Bổ sung cho khung làm việc

Không có.

### Các mẫu bắt tay

Các quy trình bắt tay sử dụng các mẫu bắt tay [Noise](https://noiseprotocol.org/noise.html).

Bảng ánh xạ chữ cái sau đây được sử dụng:

- e = khóa tạm thời dùng một lần
- s = khóa tĩnh
- p = phần tải của thông điệp

Yêu cầu xây dựng giống hệt với Noise N pattern (mẫu Noise N). Điều này cũng giống hệt với thông điệp đầu tiên (Session Request) trong XK pattern (mẫu XK) được sử dụng trong [NTCP2](/docs/specs/ntcp2/).

```text
<- s
  ...
  e es p ->
```
### Mã hóa yêu cầu

Các bản ghi yêu cầu xây dựng được tạo bởi người tạo tunnel và được mã hóa bất đối xứng cho từng hop (bước nhảy qua một nút trung gian). Việc mã hóa bất đối xứng các bản ghi yêu cầu hiện sử dụng ElGamal như được định nghĩa trong [Cryptography](/docs/specs/cryptography/) và bao gồm một checksum SHA-256. Thiết kế này không có forward secrecy (tính bảo mật chuyển tiếp).

Thiết kế mới sẽ sử dụng mẫu Noise một chiều "N" với ECIES-X25519 Diffie–Hellman tạm–tĩnh (ephemeral-static), cùng HKDF và ChaCha20/Poly1305 AEAD để đạt bí mật chuyển tiếp, tính toàn vẹn và xác thực. Alice là bên yêu cầu xây dựng tunnel. Mỗi chặng (hop) trong tunnel là một Bob.

(Các thuộc tính bảo mật của Payload (phần dữ liệu))

```text
N:                      Authentication   Confidentiality
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
### Mã hóa phản hồi

Các bản ghi phản hồi xây dựng được tạo bởi người tạo hop (nút trung gian) và được mã hóa đối xứng cho người tạo. Việc mã hóa đối xứng các bản ghi phản hồi này hiện sử dụng AES, với một checksum SHA-256 được chèn ở đầu. Thiết kế này không có tính bảo mật chuyển tiếp (forward secrecy).

Thiết kế mới sẽ sử dụng ChaCha20/Poly1305 AEAD (mã hóa xác thực kèm dữ liệu) để bảo đảm tính toàn vẹn và xác thực.

### Lý do

Khóa công khai tạm thời trong yêu cầu không cần phải được che giấu bằng AES hoặc Elligator2 (kỹ thuật ánh xạ điểm trên đường cong elliptic thành dữ liệu trông ngẫu nhiên). Chỉ chặng trước đó mới có thể thấy nó, và chặng đó biết rằng chặng kế tiếp sử dụng ECIES (lược đồ mã hóa tích hợp dựa trên đường cong elliptic).

Các bản ghi phản hồi không cần mã hóa bất đối xứng đầy đủ với một lần DH (Diffie–Hellman, trao đổi khóa) khác.

## Đặc tả

### Bản ghi yêu cầu xây dựng

BuildRequestRecords (các bản ghi yêu cầu xây dựng) được mã hóa có kích thước 528 byte cho cả ElGamal và ECIES, để đảm bảo tính tương thích.

#### Bản ghi yêu cầu không mã hóa (ElGamal)

Để tham khảo, đây là đặc tả hiện tại của tunnel BuildRequestRecord (bản ghi yêu cầu xây dựng) dành cho các router ElGamal, trích từ [I2NP](/docs/specs/i2np/). Dữ liệu chưa mã hóa được thêm ở đầu một byte khác 0 và giá trị băm SHA-256 của dữ liệu trước khi mã hóa, như được định nghĩa trong [Cryptography](/docs/specs/cryptography/).

Tất cả các trường đều ở dạng big-endian (thứ tự byte lớn trước).

Kích thước chưa mã hóa: 222 byte

```text
bytes     0-3: tunnel ID to receive messages as, nonzero
  bytes    4-35: local router identity hash
  bytes   36-39: next tunnel ID, nonzero
  bytes   40-71: next router identity hash
  bytes  72-103: AES-256 tunnel layer key
  bytes 104-135: AES-256 tunnel IV key
  bytes 136-167: AES-256 reply key
  bytes 168-183: AES-256 reply IV
  byte      184: flags
  bytes 185-188: request time (in hours since the epoch, rounded down)
  bytes 189-192: next message ID
  bytes 193-221: uninterpreted / random padding
```
#### Bản ghi yêu cầu được mã hóa (ElGamal)

Để tham khảo, đây là đặc tả hiện tại của BuildRequestRecord (bản ghi yêu cầu xây dựng) trong tunnel dành cho các router ElGamal, được lấy từ [I2NP](/docs/specs/i2np/).

Kích thước đã mã hóa: 528 byte

```text
bytes    0-15: Hop's truncated identity hash
  bytes  16-528: ElGamal encrypted BuildRequestRecord
```
#### Bản ghi yêu cầu không mã hóa (ECIES - sơ đồ mã hóa tích hợp dùng đường cong elliptic)

Đây là bản đặc tả được đề xuất cho BuildRequestRecord (bản ghi yêu cầu xây dựng) của tunnel dành cho các router ECIES-X25519. Tóm tắt các thay đổi:

- Loại bỏ băm router 32 byte không dùng
- Thay đổi thời gian yêu cầu từ giờ sang phút
- Thêm trường hết hạn cho thời gian tunnel biến đổi trong tương lai
- Tăng dung lượng dành cho các cờ
- Thêm Mapping cho các tùy chọn dựng bổ sung
- Khóa phản hồi AES-256 và IV không được dùng cho bản ghi phản hồi của chính hop (chặng)
- Bản ghi không được mã hóa dài hơn vì phần phụ trội mã hóa ít hơn

Bản ghi yêu cầu không chứa bất kỳ khóa trả lời ChaCha nào. Những khóa đó được dẫn xuất từ một KDF (hàm dẫn xuất khóa). Xem bên dưới.

Tất cả các trường đều theo big-endian (byte có trọng số cao đứng trước).

Kích thước chưa mã hóa: 464 byte

```text
bytes     0-3: tunnel ID to receive messages as, nonzero
  bytes     4-7: next tunnel ID, nonzero
  bytes    8-39: next router identity hash
  bytes   40-71: AES-256 tunnel layer key
  bytes  72-103: AES-256 tunnel IV key
  bytes 104-135: AES-256 reply key
  bytes 136-151: AES-256 reply IV
  byte      152: flags
  bytes 153-155: more flags, unused, set to 0 for compatibility
  bytes 156-159: request time (in minutes since the epoch, rounded down)
  bytes 160-163: request expiration (in seconds since creation)
  bytes 164-167: next message ID
  bytes   168-x: tunnel build options (Mapping)
  bytes     x-x: other data as implied by flags or options
  bytes   x-463: random padding
```
Trường flags giống như được định nghĩa trong [Tạo Tunnel](/docs/specs/implementation/) và chứa các nội dung sau đây::

Thứ tự bit: 76543210 (bit 7 là MSB (bit có ý nghĩa lớn nhất))  bit 7: nếu được đặt, cho phép nhận thông điệp từ bất kỳ ai  bit 6: nếu được đặt, cho phép gửi thông điệp tới bất kỳ ai, và gửi phản hồi tới

        specified next hop in a Tunnel Build Reply Message
các bit 5-0: Không xác định, phải đặt thành 0 để đảm bảo khả năng tương thích với các tùy chọn trong tương lai

Bit 7 cho biết chặng sẽ là một inbound gateway (IBGW).  Bit 6 cho biết chặng sẽ là một outbound endpoint (OBEP).  Nếu không bit nào được đặt, chặng sẽ là một chặng trung gian.  Không thể đặt cả hai cùng lúc.

Request expiration (thời điểm hết hạn của yêu cầu) được dùng cho tính năng thời lượng tunnel thay đổi trong tương lai. Hiện tại, giá trị duy nhất được hỗ trợ là 600 (10 phút).

Tùy chọn xây dựng tunnel là một cấu trúc Mapping (ánh xạ) như được định nghĩa trong [Common Structures](/docs/specs/common-structures/). Phần này dành cho việc sử dụng trong tương lai. Hiện chưa có tùy chọn nào được định nghĩa. Nếu cấu trúc Mapping trống, thì phần này là hai byte 0x00 0x00. Kích thước tối đa của Mapping (bao gồm cả trường độ dài) là 296 byte, và giá trị tối đa của trường độ dài Mapping là 294.

#### Bản ghi yêu cầu được mã hóa (ECIES, lược đồ mã hóa tích hợp trên đường cong elliptic)

Tất cả các trường đều ở dạng big-endian (thứ tự byte lớn trước), ngoại trừ khóa công khai tạm thời, vốn ở dạng little-endian (thứ tự byte nhỏ trước).

Kích thước đã mã hóa: 528 byte

```text
bytes    0-15: Hop's truncated identity hash
  bytes   16-47: Sender's ephemeral X25519 public key
  bytes  48-511: ChaCha20 encrypted BuildRequestRecord
  bytes 512-527: Poly1305 MAC
```
### Các bản ghi phản hồi xây dựng

BuildReplyRecords được mã hóa (các bản ghi phản hồi xây dựng) có kích thước 528 byte cho cả ElGamal và ECIES, để đảm bảo khả năng tương thích.

#### Bản ghi phản hồi không mã hóa (ElGamal)

Các phản hồi ElGamal (một thuật toán mã hóa khóa công khai) được mã hóa bằng AES (chuẩn mã hóa đối xứng).

Tất cả các trường sử dụng big-endian (thứ tự byte từ cao đến thấp).

Kích thước chưa mã hóa: 528 byte

```text
bytes   0-31: SHA-256 Hash of bytes 32-527
  bytes 32-526: random data
  byte     527: reply

  total length: 528
```
#### Bản ghi phản hồi không được mã hóa (ECIES - lược đồ mã hóa tích hợp dựa trên đường cong elliptic)

Đây là bản đặc tả được đề xuất cho BuildReplyRecord của tunnel áp dụng cho các routers ECIES-X25519. Tóm tắt các thay đổi:

- Thêm ánh xạ cho các tùy chọn Build Reply (phản hồi xây dựng)
- Bản ghi không được mã hóa dài hơn vì có ít phụ phí mã hóa hơn

Các phản hồi ECIES (lược đồ mã hóa tích hợp đường cong elliptic) được mã hóa bằng ChaCha20/Poly1305.

Tất cả các trường theo big-endian (thứ tự byte có ý nghĩa cao trước).

Kích thước chưa mã hóa: 512 byte

```text
bytes    0-x: Tunnel Build Reply Options (Mapping)
  bytes    x-x: other data as implied by options
  bytes  x-510: Random padding
  byte     511: Reply byte
```
Các tùy chọn phản hồi xây dựng tunnel là một cấu trúc Mapping (ánh xạ) như được định nghĩa trong [Common Structures](/docs/specs/common-structures/). Đây là để sử dụng trong tương lai. Hiện chưa có tùy chọn nào được định nghĩa. Nếu cấu trúc Mapping trống, thì nó là hai byte 0x00 0x00. Kích thước tối đa của Mapping (bao gồm cả trường độ dài) là 511 byte, và giá trị tối đa của trường độ dài của Mapping là 509.

Byte phản hồi là một trong các giá trị sau đây, như được định nghĩa trong [Tunnel Creation](/docs/specs/implementation/) để tránh bị nhận dạng qua dấu vân tay:

- 0x00 (chấp nhận)
- 30 (TUNNEL_REJECT_BANDWIDTH)

#### Bản ghi phản hồi được mã hóa (ECIES, lược đồ mã hóa tích hợp dựa trên đường cong elliptic)

Kích thước đã mã hóa: 528 byte

```text
bytes   0-511: ChaCha20 encrypted BuildReplyRecord
  bytes 512-527: Poly1305 MAC
```
Sau khi chuyển đổi hoàn toàn sang các bản ghi ECIES (Elliptic Curve Integrated Encryption Scheme - sơ đồ mã hóa tích hợp đường cong elliptic), các quy tắc đệm theo phạm vi giống như đối với các bản ghi yêu cầu.

### Mã hóa đối xứng cho các bản ghi

Các tunnels hỗn hợp được phép và là cần thiết để chuyển đổi từ ElGamal sang ECIES. Trong giai đoạn chuyển tiếp, ngày càng nhiều routers sẽ sử dụng khóa ECIES.

Tiền xử lý mật mã đối xứng sẽ chạy theo cùng một cách:

- "encryption":

- thuật toán mật mã chạy ở chế độ giải mã
  - các bản ghi yêu cầu được giải mã sớm trong bước tiền xử lý (nhằm che giấu các bản ghi yêu cầu đã mã hóa)

- "giải mã":

- thuật toán mật mã chạy ở chế độ mã hóa
  - các bản ghi yêu cầu được mã hóa (làm lộ bản ghi yêu cầu ở dạng bản rõ tiếp theo) bởi các hop (bước nhảy) tham gia

- ChaCha20 không có "chế độ", vì vậy nó chỉ đơn giản được chạy ba lần:

- một lần trong bước tiền xử lý
  - một lần do hop (nút trung gian) thực hiện
  - một lần trong bước xử lý phản hồi cuối cùng

Khi sử dụng các tunnel hỗn hợp, bên tạo tunnel sẽ cần cấu hình việc mã hóa đối xứng của BuildRequestRecord (bản ghi yêu cầu xây dựng) dựa vào loại mã hóa của chặng hiện tại và chặng liền trước.

Mỗi hop (chặng) sẽ sử dụng kiểu mã hóa riêng của nó để mã hóa BuildReplyRecords và các bản ghi khác trong VariableTunnelBuildMessage (VTBM).

Trên đường đi phản hồi, điểm cuối (người gửi) sẽ cần gỡ bỏ [Mã hóa nhiều lần](https://en.wikipedia.org/wiki/Multiple_encryption), bằng cách sử dụng khóa phản hồi của từng hop (bước nhảy).

Để minh họa rõ hơn, hãy xem một tunnel đi ra với ECIES được bao bọc bởi ElGamal:

- Người gửi (OBGW) -> ElGamal (H1) -> ECIES (H2) -> ElGamal (H3)

Tất cả BuildRequestRecords đều ở trạng thái được mã hóa (sử dụng ElGamal hoặc ECIES).

Mật mã AES256/CBC, khi được sử dụng, vẫn được áp dụng cho từng bản ghi, không xâu chuỗi qua nhiều bản ghi.

Tương tự, ChaCha20 sẽ được dùng để mã hóa từng bản ghi, không mã hóa theo luồng trên toàn bộ VTBM (thông điệp VTBM).

Các bản ghi yêu cầu được tiền xử lý bởi bên gửi (OBGW):

- Bản ghi của H3 được "mã hóa" bằng:

- Khóa phản hồi của H2 (ChaCha20)
  - Khóa phản hồi của H1 (AES256/CBC)

- Bản ghi của H2 được "mã hóa" bằng:

- khóa phản hồi của H1 (AES256/CBC)

- Bản ghi của H1 được gửi đi mà không có mã hóa đối xứng

Chỉ H2 kiểm tra cờ mã hóa phản hồi, và nhận thấy nó được theo sau bởi AES256/CBC.

Sau khi được xử lý qua từng hop (nút chuyển tiếp), các bản ghi ở trạng thái "decrypted":

- Bản ghi của H3 được "giải mã" bằng:

- Khóa hồi đáp của H3 (AES256/CBC)

- Bản ghi của H2 được "giải mã" bằng:

- Khóa phản hồi của H3 (AES256/CBC)
  - Khóa phản hồi của H2 (ChaCha20-Poly1305)

- Bản ghi của H1 được "giải mã" bằng:

- Khóa phản hồi của H3 (AES256/CBC)
  - Khóa phản hồi của H2 (ChaCha20)
  - Khóa phản hồi của H1 (AES256/CBC)

Trình tạo tunnel, còn gọi là Inbound Endpoint (IBEP) (điểm cuối vào), thực hiện hậu xử lý đối với phản hồi:

- Bản ghi của H3 được "mã hóa" bằng:

- Khóa phản hồi của H3 (AES256/CBC)

- Bản ghi của H2 được "mã hóa" bằng:

- Khóa phản hồi của H3 (AES256/CBC)
  - Khóa phản hồi của H2 (ChaCha20-Poly1305)

- Bản ghi của H1 được "mã hóa" bằng:

- Khóa phản hồi của H3 (AES256/CBC)
  - Khóa phản hồi của H2 (ChaCha20)
  - Khóa phản hồi của H1 (AES256/CBC)

### Các khóa của Request Record (ECIES)

Những khóa này được bao gồm tường minh trong ElGamal BuildRequestRecords (bản ghi yêu cầu xây dựng). Đối với ECIES BuildRequestRecords, các khóa tunnel và khóa phản hồi AES được bao gồm, nhưng các khóa phản hồi ChaCha được dẫn xuất từ DH exchange (trao đổi khóa Diffie–Hellman). Xem [Đề xuất 156](/proposals/156-ecies-routers) để biết chi tiết về các khóa ECIES tĩnh của router.

Dưới đây là mô tả về cách dẫn xuất các khóa đã được truyền trước đó trong các bản ghi yêu cầu.

#### KDF (hàm dẫn xuất khóa) cho ck và h khởi tạo

Đây là [NOISE](https://noiseprotocol.org/noise.html) tiêu chuẩn cho mẫu "N" với tên giao thức tiêu chuẩn.

```text
This is the "e" message pattern:

  // Define protocol_name.
  Set protocol_name = "Noise_N_25519_ChaChaPoly_SHA256"
  (31 bytes, US-ASCII encoded, no NULL termination).

  // Define Hash h = 32 bytes
  // Pad to 32 bytes. Do NOT hash it, because it is not more than 32 bytes.
  h = protocol_name || 0

  Define ck = 32 byte chaining key. Copy the h data to ck.
  Set chainKey = h

  // MixHash(null prologue)
  h = SHA256(h);

  // up until here, can all be precalculated by all routers.
```
#### Hàm dẫn xuất khóa (KDF) cho bản ghi yêu cầu

Các bên tạo tunnel dùng ElGamal (thuật toán mật mã ElGamal) tạo ra một cặp khóa X25519 (thuật toán trao đổi khóa dựa trên đường cong elliptic) tạm thời cho mỗi chặng ECIES (hệ mã dựa trên đường cong elliptic) trong tunnel, và dùng lược đồ ở trên để mã hóa BuildRequestRecord của họ. Các bên tạo tunnel dùng ElGamal sẽ dùng lược đồ trước đặc tả này để mã hóa tới các chặng ElGamal.

Các bên tạo tunnel ECIES sẽ cần mã hóa bằng khóa công khai của từng hop (nút trung gian) ElGamal theo sơ đồ được định nghĩa trong [Tunnel Creation](/docs/specs/implementation/). Các bên tạo tunnel ECIES sẽ sử dụng sơ đồ trên để mã hóa cho các hop ECIES.

Điều này có nghĩa là các hop (chặng trung gian) của tunnel sẽ chỉ nhìn thấy các bản ghi được mã hóa bằng cùng kiểu mã hóa như của chúng.

Đối với các trình tạo tunnel dùng ElGamal và ECIES, họ sẽ tạo các cặp khóa X25519 tạm thời, duy nhất cho mỗi hop (chặng) để mã hóa khi gửi tới các hop ECIES.

**QUAN TRỌNG**: Khóa tạm thời phải là duy nhất cho mỗi hop ECIES (nút trung gian) và cho mỗi bản ghi xây dựng. Không dùng khóa duy nhất sẽ mở ra một hướng tấn công để các hop thông đồng xác nhận rằng chúng đang ở trong cùng một tunnel.

```text
// Each hop's X25519 static keypair (hesk, hepk) from the Router Identity
  hesk = GENERATE_PRIVATE()
  hepk = DERIVE_PUBLIC(hesk)

  // MixHash(hepk)
  // || below means append
  h = SHA256(h || hepk);

  // up until here, can all be precalculated by each router
  // for all incoming build requests

  // Sender generates an X25519 ephemeral keypair per ECIES hop in the VTBM (sesk, sepk)
  sesk = GENERATE_PRIVATE()
  sepk = DERIVE_PUBLIC(sesk)

  // MixHash(sepk)
  h = SHA256(h || sepk);

  End of "e" message pattern.

  This is the "es" message pattern:

  // Noise es
  // Sender performs an X25519 DH with Hop's static public key.
  // Each Hop, finds the record w/ their truncated identity hash,
  // and extracts the Sender's ephemeral key preceding the encrypted record.
  sharedSecret = DH(sesk, hepk) = DH(hesk, sepk)

  // MixKey(DH())
  //[chainKey, k] = MixKey(sharedSecret)
  // ChaChaPoly parameters to encrypt/decrypt
  keydata = HKDF(chainKey, sharedSecret, "", 64)
  // Save for Reply Record KDF
  chainKey = keydata[0:31]

  // AEAD parameters
  k = keydata[32:63]
  n = 0
  plaintext = 464 byte build request record
  ad = h
  ciphertext = ENCRYPT(k, n, plaintext, ad)

  End of "es" message pattern.

  // MixHash(ciphertext)
  // Save for Reply Record KDF
  h = SHA256(h || ciphertext)
```
``replyKey``, ``layerKey`` và ``layerIV`` vẫn phải được bao gồm trong các bản ghi ElGamal (mật mã bất đối xứng ElGamal) và có thể được tạo ngẫu nhiên.

### Mã hóa bản ghi yêu cầu (ElGamal, thuật toán mật mã khóa công khai)

Như được định nghĩa trong [Tunnel Creation](/docs/specs/implementation/). Không có thay đổi nào đối với mã hóa cho các hop ElGamal.

### Mã hóa bản ghi phản hồi (ECIES - lược đồ mã hóa tích hợp dùng đường cong elliptic)

Bản ghi phản hồi được mã hóa bằng ChaCha20/Poly1305.

```text
// AEAD parameters
  k = chainkey from build request
  n = 0
  plaintext = 512 byte build reply record
  ad = h from build request

  ciphertext = ENCRYPT(k, n, plaintext, ad)
```
### Mã hóa bản ghi phản hồi (ElGamal)

Như được định nghĩa trong [Tạo Tunnel](/docs/specs/implementation/). Không có thay đổi nào đối với việc mã hóa cho các chặng ElGamal.

### Phân tích bảo mật

ElGamal không cung cấp bảo mật chuyển tiếp (forward secrecy) cho các thông điệp xây dựng Tunnel.

AES256/CBC ở vị thế tốt hơn một chút, chỉ dễ bị suy yếu mang tính lý thuyết bởi một cuộc tấn công `biclique` (một kỹ thuật dùng cấu trúc hai phía hoàn chỉnh trong phân tích mật mã) dựa trên bản rõ đã biết.

Kiểu tấn công thực tế duy nhất đã biết nhằm vào AES256/CBC là padding oracle attack (khai thác phản hồi kiểm tra phần đệm), khi kẻ tấn công biết được IV (vector khởi tạo).

Kẻ tấn công sẽ cần phá vỡ mã hóa ElGamal của nút kế tiếp để thu được thông tin khóa AES256/CBC (khóa phản hồi và IV (vector khởi tạo)).

ElGamal (thuật toán mật mã khóa công khai ElGamal) tiêu tốn CPU hơn đáng kể so với ECIES (hệ mã hóa dựa trên đường cong elliptic ECIES), dẫn đến nguy cơ cạn kiệt tài nguyên.

ECIES (sơ đồ mã hóa tích hợp trên đường cong elliptic), khi được sử dụng với các khóa tạm thời mới cho mỗi BuildRequestRecord (bản ghi yêu cầu xây dựng) hoặc VariableTunnelBuildMessage (thông điệp xây dựng tunnel biến đổi), cung cấp tính bảo mật chuyển tiếp.

ChaCha20Poly1305 cung cấp AEAD encryption (mã hóa xác thực kèm dữ liệu liên kết), cho phép bên nhận xác minh tính toàn vẹn của thông điệp trước khi tiến hành giải mã.

## Lý do

Thiết kế này tối đa hóa việc tái sử dụng các nguyên thủy mật mã, các giao thức và mã nguồn hiện có. Thiết kế này giảm thiểu rủi ro.

## Ghi chú triển khai

* Các router cũ không kiểm tra loại mã hóa của hop (bước nhảy) và sẽ gửi các bản ghi được mã hóa bằng ElGamal
  bản ghi. Một số router gần đây có lỗi và sẽ gửi nhiều loại bản ghi sai định dạng.
  Những người triển khai nên phát hiện và loại bỏ các bản ghi này trước khi thực hiện thao tác DH (trao đổi khóa Diffie-Hellman)
  nếu có thể, để giảm mức sử dụng CPU.

## Vấn đề

## Di chuyển

Xem [Đề xuất 156](/proposals/156-ecies-routers).

## Tài liệu tham khảo

* [Chung](/docs/specs/common-structures/)
* [Mật mã học](/docs/specs/cryptography/)
* [ECIES-X25519](/docs/specs/ecies/)
* [I2NP](/docs/specs/i2np/)
* [NOISE](https://noiseprotocol.org/noise.html)
* [NTCP2](/docs/specs/ntcp2/)
* [Đề xuất 119](/proposals/119-bidirectional-tunnels/)
* [Đề xuất 143](/proposals/143-build-message-options/)
* [Đề xuất 153](/proposals/153-chacha20-layer-encryption/)
* [Đề xuất 156](/proposals/156-ecies-routers/)
* [Đề xuất 157](/proposals/157-new-tbm/)
* [Đặc tả](/docs/specs/implementation/#tunnel-creation-ecies)
* [Tạo tunnel](/docs/specs/implementation/)
* [Mã hóa nhiều lần](https://en.wikipedia.org/wiki/Multiple_encryption)
* [RFC-7539](https://tools.ietf.org/html/rfc7539)
* [RFC-7748](https://tools.ietf.org/html/rfc7748)
