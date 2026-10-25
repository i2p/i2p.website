---
title: "Đặc tả Tạo Tunnel (ECIES-X25519)"
description: "Mã hóa thông điệp Tunnel Build sử dụng các thành phần mật mã ECIES-X25519 để đảm bảo tính bảo mật chuyển tiếp."
slug: "tunnel-creation-ecies"
aliases:
  - "/vi/docs/specs/tunnel-creation-ecies-spec"
  - "/vi/docs/specs/tunnel-creation-ecies-spec/"
category: "Giao thức"
lastUpdated: "2025-06"
accurateFor: "0.9.66"
---

## Tổng quan

Tài liệu này chỉ định việc mã hóa thông điệp Tunnel Build sử dụng các nguyên thủy mật mã được giới thiệu bởi [ECIES-X25519](/docs/specs/ecies/). Đây là một phần của đề xuất tổng thể [Prop156](/proposals/156/) để chuyển đổi router từ khóa ElGamal sang khóa ECIES-X25519.

Có hai phiên bản được chỉ định. Phiên bản đầu tiên sử dụng các build message hiện có và kích thước build record hiện tại, để tương thích với các router ElGamal. Đặc tả này đã được triển khai từ bản phát hành 0.9.48 và hiện đã bị phản đối. Phiên bản thứ hai sử dụng hai build message mới và kích thước build record nhỏ hơn, và chỉ có thể được sử dụng với các router ECIES. Đặc tả này được triển khai từ bản phát hành 0.9.51.

Để chuyển đổi mạng từ ElGamal + AES256 sang ECIES + ChaCha20, tunnel với các router hỗn hợp ElGamal và ECIES là cần thiết. Các đặc tả để xử lý các tunnel hop hỗn hợp được cung cấp. Không có thay đổi nào sẽ được thực hiện đối với định dạng, xử lý, hoặc mã hóa của các ElGamal hop. Định dạng này duy trì cùng kích thước cho các tunnel build record, như yêu cầu để tương thích.

Các tunnel creator ElGamal sẽ tạo ra các cặp khóa X25519 tạm thời cho mỗi hop, và tuân theo đặc tả này để tạo tunnel chứa các hop ECIES.

Tài liệu này mô tả chi tiết ECIES-X25519 Tunnel Building. Để có cái nhìn tổng quan về tất cả các thay đổi cần thiết cho ECIES router, xem đề xuất 156 [Prop156](/proposals/156/). Để hiểu thêm về bối cảnh phát triển đặc tả long record, xem đề xuất 152 [Prop152](/proposals/152/). Để hiểu thêm về bối cảnh phát triển đặc tả short record, xem đề xuất 157 [Prop157](/proposals/157/).

### Các Nguyên Thủy Mật Mã

Các thành phần cơ bản cần thiết để triển khai đặc tả này là:

- AES-256-CBC như trong [Cryptography](/docs/specs/cryptography/)
- Hàm STREAM ChaCha20: ENCRYPT(k, iv, plaintext) và DECRYPT(k, iv, ciphertext) - như trong [EncryptedLeaseSet](/docs/specs/encryptedleaseset/) và [RFC-7539](https://tools.ietf.org/html/rfc7539)
- Hàm STREAM ChaCha20/Poly1305: ENCRYPT(k, n, plaintext, ad) và DECRYPT(k, n, ciphertext, ad) - như trong [NTCP2](/docs/specs/ntcp2/), [ECIES-X25519](/docs/specs/ecies/), và [RFC-7539](https://tools.ietf.org/html/rfc7539)
- Hàm X25519 DH - như trong [NTCP2](/docs/specs/ntcp2/) và [ECIES-X25519](/docs/specs/ecies/)
- HKDF(salt, ikm, info, n) - như trong [NTCP2](/docs/specs/ntcp2/) và [ECIES-X25519](/docs/specs/ecies/)

Các hàm Noise khác được định nghĩa ở nơi khác:

- MixHash(d) - như trong [NTCP2](/docs/specs/ntcp2/) và [ECIES-X25519](/docs/specs/ecies/)
- MixKey(d) - như trong [NTCP2](/docs/specs/ntcp2/) và [ECIES-X25519](/docs/specs/ecies/)

## Thiết kế

### Noise Protocol Framework

Thông số kỹ thuật này cung cấp các yêu cầu dựa trên Noise Protocol Framework [NOISE](https://noiseprotocol.org/noise.html) (Revision 34, 2018-07-11). Trong thuật ngữ của Noise, Alice là bên khởi tạo, và Bob là bên phản hồi.

Nó dựa trên giao thức Noise Noise_N_25519_ChaChaPoly_SHA256. Giao thức Noise này sử dụng các thành phần cơ bản sau:

- One-Way Handshake Pattern: N - Alice không truyền static key của mình cho Bob (N)
- DH Function: X25519 - X25519 DH với độ dài key là 32 byte như được chỉ định trong [RFC-7748](https://tools.ietf.org/html/rfc7748)
- Cipher Function: ChaChaPoly - AEAD_CHACHA20_POLY1305 như được chỉ định trong [RFC-7539](https://tools.ietf.org/html/rfc7539) mục 2.8. Nonce 12 byte, với 4 byte đầu được đặt về zero. Giống hệt như trong [NTCP2](/docs/specs/ntcp2/)
- Hash Function: SHA256 - Hash tiêu chuẩn 32-byte, đã được sử dụng rộng rãi trong I2P

### Mẫu Bắt Tay

Handshake sử dụng các mẫu handshake [Noise](https://noiseprotocol.org/noise.html).

Ánh xạ chữ cái sau đây được sử dụng:

- e = khóa tạm thời một lần
- s = khóa tĩnh
- p = tải trọng thông điệp

Yêu cầu build này giống hệt với mẫu Noise N. Điều này cũng giống hệt với thông điệp đầu tiên (Session Request) trong mẫu XK được sử dụng trong [NTCP2](/docs/specs/ntcp2/).

```
<- s
  ...
  e es p ->
```
### Mã hóa Yêu cầu

Các bản ghi yêu cầu xây dựng được tạo bởi người tạo tunnel và được mã hóa bất đối xứng cho từng hop riêng lẻ. Việc mã hóa bất đối xứng này của các bản ghi yêu cầu hiện tại là ElGamal như được định nghĩa trong [Cryptography](/docs/specs/cryptography/) và chứa một checksum SHA-256. Thiết kế này không có tính bảo mật tiến về phía trước.

Thiết kế ECIES sử dụng mẫu Noise một chiều "N" với ECIES-X25519 ephemeral-static DH, với HKDF, và ChaCha20/Poly1305 AEAD để đảm bảo tính bảo mật chuyển tiếp, tính toàn vẹn và xác thực. Alice là người yêu cầu xây dựng tunnel. Mỗi hop trong tunnel là một Bob.

### Mã hóa Phản hồi

Các bản ghi phản hồi build được tạo bởi người tạo hop và được mã hóa đối xứng cho người tạo. Việc mã hóa đối xứng này của các bản ghi phản hồi ElGamal sử dụng AES với checksum SHA-256 được thêm vào đầu. Thiết kế này không có tính bảo mật tiến (forward-secret).

Các phản hồi ECIES sử dụng ChaCha20/Poly1305 AEAD để đảm bảo tính toàn vẹn và xác thực.

## Đặc tả Bản ghi Dài

LƯU Ý: Đã lỗi thời, không còn sử dụng. Hãy sử dụng định dạng Short Record được chỉ định bên dưới.

### Bản Ghi Yêu Cầu Xây Dựng

Các BuildRequestRecord được mã hóa có kích thước 528 byte cho cả ElGamal và ECIES, để đảm bảo tính tương thích.

#### Bản ghi yêu cầu không mã hóa

Đây là đặc tả của tunnel BuildRequestRecord cho các router ECIES-X25519. Tóm tắt các thay đổi:

- Xóa router hash 32-byte không sử dụng
- Thay đổi thời gian yêu cầu từ giờ sang phút
- Thêm trường hết hạn cho thời gian tunnel biến đổi trong tương lai
- Thêm không gian cho các cờ hiệu
- Thêm Mapping cho các tùy chọn xây dựng bổ sung
- Khóa phản hồi AES-256 và IV không được sử dụng cho bản ghi phản hồi của chính hop đó
- Bản ghi không mã hóa dài hơn vì có ít chi phí mã hóa hơn

Bản ghi yêu cầu không chứa bất kỳ khóa phản hồi ChaCha nào. Các khóa này được tạo ra từ một KDF. Xem bên dưới.

Tất cả các trường đều theo định dạng big-endian.

Kích thước không mã hóa: 464 bytes

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bytes</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-3</td><td style="border:1px solid var(--color-border); padding:0.6rem;">tunnel ID to receive messages as, nonzero</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">4-7</td><td style="border:1px solid var(--color-border); padding:0.6rem;">next tunnel ID, nonzero</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">8-39</td><td style="border:1px solid var(--color-border); padding:0.6rem;">next router identity hash</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">40-71</td><td style="border:1px solid var(--color-border); padding:0.6rem;">AES-256 tunnel layer key</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">72-103</td><td style="border:1px solid var(--color-border); padding:0.6rem;">AES-256 tunnel IV key</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">104-135</td><td style="border:1px solid var(--color-border); padding:0.6rem;">AES-256 reply key</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">136-151</td><td style="border:1px solid var(--color-border); padding:0.6rem;">AES-256 reply IV</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">152</td><td style="border:1px solid var(--color-border); padding:0.6rem;">flags</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">153-155</td><td style="border:1px solid var(--color-border); padding:0.6rem;">more flags, unused, set to 0 for compatibility</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">156-159</td><td style="border:1px solid var(--color-border); padding:0.6rem;">request time (in minutes since the epoch, rounded down)</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">160-163</td><td style="border:1px solid var(--color-border); padding:0.6rem;">request expiration (in seconds since creation)</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">164-167</td><td style="border:1px solid var(--color-border); padding:0.6rem;">next message ID</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">168-x</td><td style="border:1px solid var(--color-border); padding:0.6rem;">tunnel build options (Mapping)</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">x-x</td><td style="border:1px solid var(--color-border); padding:0.6rem;">other data as implied by flags or options</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">x-463</td><td style="border:1px solid var(--color-border); padding:0.6rem;">random padding</td></tr>
</tbody>
</table>
Trường flags giống như được định nghĩa trong [Tunnel-Creation](/docs/specs/tunnel-creation/) và chứa những thông tin sau:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bit</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;" colspan="2"><em>Bit order: 76543210 (bit 7 is MSB)</em></td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">7</td><td style="border:1px solid var(--color-border); padding:0.6rem;">if set, allow messages from anyone</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">6</td><td style="border:1px solid var(--color-border); padding:0.6rem;">if set, allow messages to anyone, and send the reply to the specified next hop in a Tunnel Build Reply Message</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">5-0</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Undefined, must set to 0 for compatibility with future options</td></tr>
</tbody>
</table>
Bit 7 cho biết hop sẽ là một inbound gateway (IBGW). Bit 6 cho biết hop sẽ là một outbound endpoint (OBEP). Nếu không có bit nào được thiết lập, hop sẽ là một participant trung gian. Không thể thiết lập cả hai bit cùng một lúc.

Thời gian hết hạn yêu cầu dành cho thời lượng tunnel có thể thay đổi trong tương lai. Hiện tại, giá trị duy nhất được hỗ trợ là 600 (10 phút).

Các tùy chọn xây dựng tunnel là một cấu trúc Mapping như được định nghĩa trong [Common](/docs/specs/common-structures/). Các tùy chọn duy nhất hiện được định nghĩa là cho các tham số băng thông, kể từ API 0.9.65, xem chi tiết bên dưới. Nếu cấu trúc Mapping rỗng, đây là hai byte 0x00 0x00. Kích thước tối đa của Mapping (bao gồm trường độ dài) là 296 byte, và giá trị tối đa của trường độ dài Mapping là 294.

#### Bản Ghi Yêu Cầu Được Mã Hóa

Tất cả các trường đều là big-endian trừ ephemeral public key là little-endian.

Kích thước mã hóa: 528 bytes

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bytes</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-15</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Hop's truncated identity hash</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">16-47</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Sender's ephemeral X25519 public key</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">48-511</td><td style="border:1px solid var(--color-border); padding:0.6rem;">ChaCha20 encrypted BuildRequestRecord</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">512-527</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Poly1305 MAC</td></tr>
</tbody>
</table>
### Xây dựng Bản ghi Phản hồi

Các BuildReplyRecord được mã hóa có kích thước 528 byte cho cả ElGamal và ECIES, để đảm bảo tính tương thích.

#### Bản ghi phản hồi không được mã hóa

Đây là đặc tả của tunnel BuildReplyRecord cho các router ECIES-X25519. Tóm tắt các thay đổi:

- Thêm ánh xạ cho các tùy chọn phản hồi xây dựng
- Bản ghi không mã hóa dài hơn vì có ít chi phí mã hóa hơn

Các phản hồi ECIES được mã hóa bằng ChaCha20/Poly1305.

Tất cả các trường đều là big-endian.

Kích thước không mã hóa: 512 bytes

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bytes</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-x</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Tunnel Build Reply Options (Mapping)</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">x-x</td><td style="border:1px solid var(--color-border); padding:0.6rem;">other data as implied by options</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">x-510</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Random padding</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">511</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Reply byte</td></tr>
</tbody>
</table>
Các tùy chọn tunnel build reply là một cấu trúc Mapping như được định nghĩa trong [Common](/docs/specs/common-structures/). Các tùy chọn duy nhất hiện được định nghĩa là cho các tham số băng thông, kể từ API 0.9.65, xem chi tiết bên dưới. Nếu cấu trúc Mapping trống, điều này là hai byte 0x00 0x00. Kích thước tối đa của Mapping (bao gồm trường length) là 511 byte, và giá trị tối đa của trường Mapping length là 509.

Byte phản hồi là một trong các giá trị sau như được định nghĩa trong [Tunnel-Creation](/docs/specs/tunnel-creation/) để tránh việc tạo dấu vân tay:

- 0x00 (chấp nhận)
- 30 (TUNNEL_REJECT_BANDWIDTH)

#### Bản Ghi Phản Hồi Đã Mã Hóa

Kích thước đã mã hóa: 528 bytes

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bytes</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-511</td><td style="border:1px solid var(--color-border); padding:0.6rem;">ChaCha20 encrypted BuildReplyRecord</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">512-527</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Poly1305 MAC</td></tr>
</tbody>
</table>
Sau khi chuyển đổi hoàn toàn sang các bản ghi ECIES, các quy tắc padding theo phạm vi sẽ giống như đối với các bản ghi yêu cầu.

### Mã hóa đối xứng các bản ghi

Mixed tunnel được cho phép và cần thiết cho việc chuyển đổi từ ElGamal sang ECIES. Trong giai đoạn chuyển tiếp, số lượng router ngày càng tăng sẽ được khóa dưới các khóa ECIES.

Tiền xử lý mật mã đối xứng sẽ chạy theo cùng một cách:

- "encryption":
  - cipher chạy ở chế độ giải mã
  - các bản ghi yêu cầu được giải mã trước trong quá trình tiền xử lý (che giấu các bản ghi yêu cầu đã mã hóa)
- "decryption":
  - cipher chạy ở chế độ mã hóa
  - các bản ghi yêu cầu được mã hóa (tiết lộ bản ghi yêu cầu văn bản thuần tiếp theo) bởi các hop tham gia
- ChaCha20 không có "chế độ", vì vậy nó chỉ đơn giản được chạy ba lần:
  - một lần trong quá trình tiền xử lý
  - một lần bởi hop
  - một lần trong quá trình xử lý phản hồi cuối cùng

Khi các tunnel hỗn hợp được sử dụng, những người tạo tunnel sẽ cần dựa vào loại mã hóa đối xứng của BuildRequestRecord trên loại mã hóa của hop hiện tại và hop trước đó.

Mỗi hop sẽ sử dụng loại mã hóa riêng của nó để mã hóa BuildReplyRecords và các bản ghi khác trong VariableTunnelBuildMessage (VTBM).

Trên đường dẫn phản hồi, endpoint (người gửi) sẽ cần hoàn tác [Multiple-Encryption](https://en.wikipedia.org/wiki/Multiple_encryption), sử dụng khóa phản hồi của từng hop.

Để làm rõ ví dụ, hãy xem xét một tunnel gửi đi có ECIES được bao quanh bởi ElGamal:

- Người gửi (OBGW) -> ElGamal (H1) -> ECIES (H2) -> ElGamal (H3)

Tất cả BuildRequestRecords đều ở trạng thái được mã hóa (sử dụng ElGamal hoặc ECIES).

Mã hóa AES256/CBC, khi được sử dụng, vẫn được áp dụng cho từng bản ghi riêng biệt, không có chuỗi liên kết qua nhiều bản ghi.

Tương tự, ChaCha20 sẽ được sử dụng để mã hóa từng bản ghi, không phải truyền liên tục qua toàn bộ VTBM.

Các bản ghi yêu cầu được xử lý trước bởi Sender (OBGW):

- Bản ghi của H3 được "mã hóa" bằng:
  - Reply key của H2 (ChaCha20)
  - Reply key của H1 (AES256/CBC)
- Bản ghi của H2 được "mã hóa" bằng:
  - Reply key của H1 (AES256/CBC)
- Bản ghi của H1 được gửi đi mà không có mã hóa đối xứng

Chỉ có H2 kiểm tra cờ mã hóa phản hồi, và thấy rằng nó được theo sau bởi AES256/CBC.

Sau khi được xử lý bởi mỗi hop, các bản ghi ở trạng thái "đã giải mã":

- Bản ghi của H3 được "giải mã" bằng cách sử dụng:
  - Reply key của H3 (AES256/CBC)
- Bản ghi của H2 được "giải mã" bằng cách sử dụng:
  - Reply key của H3 (AES256/CBC)
  - Reply key của H2 (ChaCha20-Poly1305)
- Bản ghi của H1 được "giải mã" bằng cách sử dụng:
  - Reply key của H3 (AES256/CBC)
  - Reply key của H2 (ChaCha20)
  - Reply key của H1 (AES256/CBC)

Người tạo tunnel, còn được gọi là Inbound Endpoint (IBEP), xử lý sau phản hồi:

- Bản ghi của H3 được "mã hóa" bằng:
  - Khóa phản hồi của H3 (AES256/CBC)
- Bản ghi của H2 được "mã hóa" bằng:
  - Khóa phản hồi của H3 (AES256/CBC)
  - Khóa phản hồi của H2 (ChaCha20-Poly1305)
- Bản ghi của H1 được "mã hóa" bằng:
  - Khóa phản hồi của H3 (AES256/CBC)
  - Khóa phản hồi của H2 (ChaCha20)
  - Khóa phản hồi của H1 (AES256/CBC)

### Khóa Bản Ghi Yêu Cầu

Các khóa này được bao gồm một cách rõ ràng trong ElGamal BuildRequestRecords. Đối với ECIES BuildRequestRecords, các khóa tunnel và khóa trả lời AES được bao gồm, nhưng các khóa trả lời ChaCha được tạo ra từ việc trao đổi DH. Xem [Prop156](/proposals/156/) để biết chi tiết về các khóa ECIES tĩnh của router.

Dưới đây là mô tả về cách tạo ra các khóa đã được truyền trước đó trong các bản ghi yêu cầu.

#### KDF cho ck và h ban đầu

Đây là [NOISE](https://noiseprotocol.org/noise.html) tiêu chuẩn cho pattern "N" với tên giao thức tiêu chuẩn.

```
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
#### KDF cho Bản ghi Yêu cầu

Các tunnel creator ElGamal tạo ra một cặp khóa X25519 tạm thời cho mỗi hop ECIES trong tunnel, và sử dụng sơ đồ trên để mã hóa BuildRequestRecord của họ. Các tunnel creator ElGamal sẽ sử dụng sơ đồ trước đặc tả này để mã hóa đến các hop ElGamal.

Các tunnel creator ECIES sẽ cần mã hóa cho từng public key của ElGamal hop bằng cách sử dụng phương án được định nghĩa trong [Tunnel-Creation](/docs/specs/tunnel-creation/). Các tunnel creator ECIES sẽ sử dụng phương án trên để mã hóa cho các ECIES hop.

Điều này có nghĩa là các tunnel hop sẽ chỉ thấy các bản ghi được mã hóa từ cùng loại mã hóa của chúng.

Đối với các tunnel creator ElGamal và ECIES, chúng sẽ tạo ra các cặp khóa X25519 ephemeral duy nhất cho mỗi hop để mã hóa tới các ECIES hop.

**QUAN TRỌNG**: Ephemeral keys phải là duy nhất cho mỗi ECIES hop và mỗi build record. Việc không sử dụng các khóa duy nhất sẽ tạo ra lỗ hổng tấn công cho các hop thông đồng để xác nhận chúng nằm trong cùng một tunnel.

```
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
`replyKey`, `layerKey` và `layerIV` vẫn phải được bao gồm bên trong các bản ghi ElGamal, và có thể được tạo ngẫu nhiên.

### Mã hóa Bản ghi Phản hồi

Bản ghi phản hồi được mã hóa bằng ChaCha20/Poly1305.

```
// AEAD parameters
k = chainkey from build request
n = 0
plaintext = 512 byte build reply record
ad = h from build request

ciphertext = ENCRYPT(k, n, plaintext, ad)
```
## Đặc tả Bản ghi Ngắn

Đặc tả này sử dụng hai loại I2NP tunnel build message mới, Short Tunnel Build Message (loại 25) và Outbound Tunnel Build Reply Message (loại 26).

Người tạo tunnel và tất cả các hop trong tunnel được tạo phải hỗ trợ ECIES-X25519, và ít nhất phiên bản 0.9.51. Các hop trong reply tunnel (đối với outbound build) hoặc outbound tunnel (đối với inbound build) không có yêu cầu gì.

Các bản ghi yêu cầu và phản hồi được mã hóa sẽ có kích thước 218 byte, so với 528 byte cho tất cả các thông điệp build khác.

Các bản ghi yêu cầu plaintext sẽ có kích thước 154 byte, so với 222 byte cho các bản ghi ElGamal, và 464 byte cho các bản ghi ECIES như đã định nghĩa ở trên.

Các bản ghi phản hồi plaintext sẽ có kích thước 202 byte, so với 496 byte cho các bản ghi ElGamal, và 512 byte cho các bản ghi ECIES như đã định nghĩa ở trên.

Mã hóa phản hồi sẽ là ChaCha20/Poly1305 cho bản ghi của chính hop đó, và ChaCha20 (KHÔNG phải ChaCha20/Poly1305) cho các bản ghi khác trong thông điệp xây dựng.

Các bản ghi yêu cầu sẽ được làm nhỏ hơn bằng cách sử dụng HKDF để tạo ra các khóa lớp và khóa phản hồi, do đó chúng không được bao gồm một cách rõ ràng trong yêu cầu.

### Luồng Thông điệp

```
STBM: Short tunnel build message (type 25)
OTBRM: Outbound tunnel build reply message (type 26)

Outbound Build A-B-C
Reply through existing inbound D-E-F


                New Tunnel
         STBM      STBM      STBM
Creator ------> A ------> B ------> C ---\
                                   OBEP   \
                                          | Garlic wrapped (optional)
                                          | OTBRM
                                          | (TUNNEL delivery)
                                          | from OBEP to
                                          | creator
              Existing Tunnel             /
Creator <-------F---------E-------- D <--/
                                   IBGW



Inbound Build D-E-F
Sent through existing outbound A-B-C


              Existing Tunnel
Creator ------> A ------> B ------> C ---\
                                  OBEP    \
                                          | Garlic wrapped (optional)
                                          | STBM
                                          | (ROUTER delivery)
                                          | from creator
                New Tunnel                | to IBGW
          STBM      STBM      STBM        /
Creator <------ F <------ E <------ D <--/
                                   IBGW
```
#### Ghi chú

Việc bọc garlic các thông điệp sẽ ẩn chúng khỏi OBEP (đối với build đầu vào) hoặc IBGW (đối với build đầu ra). Điều này được khuyến nghị nhưng không bắt buộc. Nếu OBEP và IBGW là cùng một router, thì không cần thiết.

### Bản Ghi Yêu Cầu Xây Dựng Ngắn

BuildRequestRecords được mã hóa ngắn có kích thước 218 byte.

#### Bản Ghi Yêu Cầu Ngắn Không Mã Hóa

Tóm tắt các thay đổi từ bản ghi dài:

- Thay đổi độ dài không mã hóa từ 464 xuống 154 bytes
- Thay đổi độ dài mã hóa từ 528 xuống 218 bytes
- Loại bỏ các khóa layer và reply cùng IV, chúng sẽ được tạo ra từ một KDF

Bản ghi yêu cầu không chứa bất kỳ khóa phản hồi ChaCha nào. Những khóa này được tạo ra từ một KDF. Xem bên dưới.

Tất cả các trường đều sử dụng big-endian.

Kích thước không mã hóa: 154 byte.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bytes</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-3</td><td style="border:1px solid var(--color-border); padding:0.6rem;">tunnel ID to receive messages as, nonzero</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">4-7</td><td style="border:1px solid var(--color-border); padding:0.6rem;">next tunnel ID, nonzero</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">8-39</td><td style="border:1px solid var(--color-border); padding:0.6rem;">next router identity hash</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">40</td><td style="border:1px solid var(--color-border); padding:0.6rem;">flags</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">41-42</td><td style="border:1px solid var(--color-border); padding:0.6rem;">more flags, unused, set to 0 for compatibility</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">43</td><td style="border:1px solid var(--color-border); padding:0.6rem;">layer encryption type</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">44-47</td><td style="border:1px solid var(--color-border); padding:0.6rem;">request time (in minutes since the epoch, rounded down)</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">48-51</td><td style="border:1px solid var(--color-border); padding:0.6rem;">request expiration (in seconds since creation)</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">52-55</td><td style="border:1px solid var(--color-border); padding:0.6rem;">next message ID</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">56-x</td><td style="border:1px solid var(--color-border); padding:0.6rem;">tunnel build options (Mapping)</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">x-x</td><td style="border:1px solid var(--color-border); padding:0.6rem;">other data as implied by flags or options</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">x-153</td><td style="border:1px solid var(--color-border); padding:0.6rem;">random padding (see below)</td></tr>
</tbody>
</table>
Trường flags giống như được định nghĩa trong [Tunnel-Creation](/docs/specs/tunnel-creation/) và chứa các thông tin sau:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bit</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;" colspan="2"><em>Bit order: 76543210 (bit 7 is MSB)</em></td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">7</td><td style="border:1px solid var(--color-border); padding:0.6rem;">if set, allow messages from anyone</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">6</td><td style="border:1px solid var(--color-border); padding:0.6rem;">if set, allow messages to anyone, and send the reply to the specified next hop in a Tunnel Build Reply Message</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">5-0</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Undefined, must set to 0 for compatibility with future options</td></tr>
</tbody>
</table>
Bit 7 cho biết rằng hop sẽ là một inbound gateway (IBGW). Bit 6 cho biết rằng hop sẽ là một outbound endpoint (OBEP). Nếu không có bit nào được thiết lập, hop sẽ là một participant trung gian. Cả hai bit không thể được thiết lập cùng lúc.

Loại mã hóa lớp: 0 cho AES (như trong các tunnel hiện tại); 1 cho tương lai (ChaCha?)

Thời gian hết hạn yêu cầu dành cho thời lượng tunnel biến đổi trong tương lai. Hiện tại, giá trị duy nhất được hỗ trợ là 600 (10 phút).

Khóa công khai tạm thời của người tạo là một khóa ECIES, big-endian. Nó được sử dụng cho KDF cho lớp IBGW và các khóa phản hồi cùng IV. Điều này chỉ được bao gồm trong bản ghi plaintext trong thông điệp Inbound Tunnel Build. Nó là bắt buộc vì không có DH ở lớp này cho bản ghi xây dựng.

Các tùy chọn xây dựng tunnel là một cấu trúc Mapping như được định nghĩa trong [Common](/docs/specs/common-structures/). Các tùy chọn duy nhất hiện được định nghĩa là cho các tham số băng thông, kể từ API 0.9.65, xem chi tiết bên dưới. Nếu cấu trúc Mapping rỗng, đây sẽ là hai byte 0x00 0x00. Kích thước tối đa của Mapping (bao gồm trường độ dài) là 98 byte, và giá trị tối đa của trường độ dài Mapping là 96.

#### Bản Ghi Yêu Cầu Ngắn Được Mã Hóa

Tất cả các trường đều theo thứ tự big-endian ngoại trừ khóa công khai tạm thời (ephemeral public key) theo thứ tự little-endian.

Kích thước mã hóa: 218 byte

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bytes</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-15</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Hop's truncated identity hash</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">16-47</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Sender's ephemeral X25519 public key</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">48-201</td><td style="border:1px solid var(--color-border); padding:0.6rem;">ChaCha20 encrypted ShortBuildRequestRecord</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">202-217</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Poly1305 MAC</td></tr>
</tbody>
</table>
### Bản ghi phản hồi xây dựng ngắn

BuildReplyRecords được mã hóa ngắn có kích thước 218 byte.

#### Bản Ghi Phản Hồi Ngắn Không Mã Hóa

Tóm tắt các thay đổi từ bản ghi dài:

- Thay đổi độ dài không mã hóa từ 512 xuống 202 byte
- Thay đổi độ dài đã mã hóa từ 528 xuống 218 byte

Các phản hồi ECIES được mã hóa bằng ChaCha20/Poly1305.

Tất cả các trường đều theo định dạng big-endian.

Kích thước chưa mã hóa: 202 bytes.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bytes</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-x</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Tunnel Build Reply Options (Mapping)</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">x-x</td><td style="border:1px solid var(--color-border); padding:0.6rem;">other data as implied by options</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">x-200</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Random padding (see below)</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">201</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Reply byte</td></tr>
</tbody>
</table>
Tùy chọn phản hồi xây dựng tunnel là một cấu trúc Mapping như được định nghĩa trong [Common](/docs/specs/common-structures/). Các tùy chọn hiện tại chỉ được định nghĩa cho các tham số băng thông, kể từ API 0.9.65, xem chi tiết bên dưới. Nếu cấu trúc Mapping rỗng, đây là hai byte 0x00 0x00. Kích thước tối đa của Mapping (bao gồm trường độ dài) là 201 byte, và giá trị tối đa của trường độ dài Mapping là 199.

Byte phản hồi là một trong các giá trị sau như được định nghĩa trong [Tunnel-Creation](/docs/specs/tunnel-creation/) để tránh fingerprinting:

- 0x00 (chấp nhận)
- 30 (TUNNEL_REJECT_BANDWIDTH)

Một giá trị phản hồi bổ sung có thể được định nghĩa trong tương lai để biểu thị việc từ chối các tùy chọn không được hỗ trợ.

#### Bản Ghi Phản Hồi Ngắn Được Mã Hóa

Kích thước mã hóa: 218 bytes

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bytes</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-201</td><td style="border:1px solid var(--color-border); padding:0.6rem;">ChaCha20 encrypted ShortBuildReplyRecord</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">202-217</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Poly1305 MAC</td></tr>
</tbody>
</table>
### KDF

Chúng tôi sử dụng chaining key (ck) từ trạng thái Noise sau khi mã hóa/giải mã bản ghi xây dựng tunnel để tạo ra các khóa sau: khóa phản hồi, khóa lớp AES, khóa AES IV và garlic reply key/tag cho OBEP.

Reply keys: Lưu ý rằng KDF hơi khác một chút cho các hop OBEP và non-OBEP. Không giống như các bản ghi dài, chúng ta không thể sử dụng phần trái của ck cho reply key, vì nó không phải là cuối cùng và sẽ được sử dụng sau này. Reply key được sử dụng để mã hóa reply cho bản ghi đó bằng AEAD/ChaCha20/Poly1305 và ChaCha20 để reply các bản ghi khác. Cả hai đều sử dụng cùng một key. Nonce là vị trí của bản ghi trong thông điệp bắt đầu từ 0. Xem chi tiết bên dưới.

```
keydata = HKDF(ck, ZEROLEN, "SMTunnelReplyKey", 64)
replyKey = keydata[32:63]
ck = keydata[0:31]

AES Layer key:
keydata = HKDF(ck, ZEROLEN, "SMTunnelLayerKey", 64)
layerKey = keydata[32:63]

IV key for non-OBEP record:
ivKey = keydata[0:31]
because it's last

IV key for OBEP record:
ck = keydata[0:31]
keydata = HKDF(ck, ZEROLEN, "TunnelLayerIVKey", 64)
ivKey = keydata[32:63]
ck = keydata[0:31]

OBEP garlic reply key/tag:
keydata = HKDF(ck, ZEROLEN, "RGarlicKeyAndTag", 64)
garlicReplyKey = keydata[32:63]
garlicReplyTag = keydata[0:7]
```
Lưu ý: KDF cho khóa IV tại OBEP khác với KDF cho các hop khác, ngay cả khi phản hồi không được mã hóa garlic.

#### Mã hóa Bản ghi

Bản ghi phản hồi của hop được mã hóa bằng ChaCha20/Poly1305. Điều này giống với đặc tả bản ghi dài ở trên, NGOẠI TRỪ 'n' là số bản ghi 0-7, thay vì luôn là 0. Xem [RFC-7539](https://tools.ietf.org/html/rfc7539).

```
// AEAD parameters
k = replyKey from KDF above
n = record number 0-7
plaintext = 202 byte build reply record
ad = h from build request

ciphertext = ENCRYPT(k, n, plaintext, ad)
```
Các bản ghi khác được mã hóa lặp và đối xứng tại mỗi hop với ChaCha20 (KHÔNG phải ChaCha20/Poly1305). Điều này khác với đặc tả bản ghi dài ở trên, sử dụng AES và không sử dụng số bản ghi.

Số bản ghi được đặt trong IV tại byte 4, vì ChaCha20 sử dụng IV 12-byte với nonce little-endian tại các byte 4-11. Xem [RFC-7539](https://tools.ietf.org/html/rfc7539).

```
// Parameters
k = replyKey from KDF above
n = record number 0-7
iv = 12 bytes, all zeros except iv[4] = n
plaintext = 218 byte encrypted record

ciphertext = ENCRYPT(k, iv, plaintext)
```
#### Garlic Encryption

Việc bọc garlic encryption các thông điệp sẽ ẩn chúng khỏi OBEP (đối với quá trình xây dựng inbound) hoặc IBGW (đối với quá trình xây dựng outbound). Điều này được khuyến nghị nhưng không bắt buộc. Nếu OBEP và IBGW là cùng một router, thì không cần thiết.

Garlic encryption của một Inbound Short Tunnel Build Message, bởi người tạo, được mã hóa tới ECIES IBGW, sử dụng mã hóa Noise 'N', như được định nghĩa trong [ECIES-ROUTERS](/docs/specs/ecies-routers/).

Garlic encryption của một Outbound Tunnel Build Reply Message, bởi OBEP, được mã hóa cho người tạo, sử dụng các thông điệp Existing Session với 32-byte garlic reply key và 8-byte garlic reply tag từ KDF ở trên. Định dạng được chỉ định như cho các phản hồi cho Database Lookups trong [I2NP](/docs/specs/i2np/), [ECIES-ROUTERS](/docs/specs/ecies-routers/), và [ECIES-X25519](/docs/specs/ecies/).

#### Mã hóa lớp

Thông số kỹ thuật này bao gồm một trường loại mã hóa lớp trong bản ghi yêu cầu xây dựng. Loại mã hóa lớp duy nhất hiện được hỗ trợ là loại 0, đó là AES. Điều này không thay đổi so với các thông số kỹ thuật trước đây, ngoại trừ việc khóa lớp và khóa IV được tạo ra từ KDF ở trên thay vì được bao gồm trong bản ghi yêu cầu xây dựng.

Việc thêm các loại mã hóa lớp mới, ví dụ như ChaCha20, là chủ đề cần nghiên cứu thêm và hiện tại không phải là một phần của đặc tả này.

## Ghi Chú Triển Khai

- Các router cũ không kiểm tra loại mã hóa của hop và sẽ gửi các bản ghi được mã hóa ElGamal. Một số router gần đây có lỗi và sẽ gửi nhiều loại bản ghi bị hỏng. Các nhà phát triển nên phát hiện và từ chối những bản ghi này trước thao tác DH nếu có thể, để giảm mức sử dụng CPU.

### Bản Ghi Xây Dựng

Thứ tự bản ghi xây dựng phải được ngẫu nhiên hóa, do đó các hop trung gian không biết vị trí của chúng trong tunnel.

Số lượng build record tối thiểu được khuyến nghị là 4. Nếu có nhiều build record hơn số hop, các record "giả" phải được thêm vào, chứa dữ liệu ngẫu nhiên hoặc dữ liệu cụ thể của implementation. Đối với việc xây dựng inbound tunnel, phải luôn có một record "giả" cho router khởi tạo, với tiền tố hash 16-byte chính xác và một X25519 ephemeral key thực, nếu không hop gần nhất sẽ biết rằng hop tiếp theo chính là router khởi tạo.

Phần còn lại của bản ghi "giả" có thể là dữ liệu ngẫu nhiên, hoặc có thể được mã hóa theo bất kỳ định dạng nào để người khởi tạo gửi dữ liệu cho chính mình về quá trình xây dựng, có lẽ để giảm yêu cầu lưu trữ cho các bản dựng đang chờ xử lý.

Những người khởi tạo các tunnel đến phải sử dụng một phương pháp nào đó để xác thực rằng bản ghi "giả" của họ không bị thay đổi bởi hop trước đó, vì điều này cũng có thể được sử dụng để phá vỡ tính ẩn danh. Người khởi tạo có thể lưu trữ và xác minh checksum của bản ghi, hoặc bao gồm checksum trong bản ghi, hoặc sử dụng hàm mã hóa/giải mã AEAD, tùy thuộc vào cách triển khai. Nếu tiền tố hash 16 byte hoặc nội dung build record khác bị thay đổi, router phải loại bỏ tunnel.

Các bản ghi giả cho outbound tunnel và các bản ghi giả bổ sung cho inbound tunnel không có những yêu cầu này, và có thể là dữ liệu hoàn toàn ngẫu nhiên, vì chúng sẽ không bao giờ hiển thị với bất kỳ hop nào. Người tạo ra vẫn có thể muốn xác thực rằng chúng không bị thay đổi.

## Thông số băng thông Tunnel

### Tổng quan

Khi chúng tôi đã nâng cao hiệu suất của mạng trong vài năm qua với các giao thức mới, loại mã hóa mới và cải tiến kiểm soát tắc nghẽn, các ứng dụng nhanh hơn như phát trực tuyến video đang trở nên khả thi. Các ứng dụng này yêu cầu băng thông cao tại mỗi hop trong tunnel máy khách của chúng.

Tuy nhiên, các router tham gia không có bất kỳ thông tin nào về lượng băng thông mà một tunnel sẽ sử dụng khi họ nhận được thông điệp xây dựng tunnel. Họ chỉ có thể chấp nhận hoặc từ chối một tunnel dựa trên tổng băng thông hiện tại được sử dụng bởi tất cả các tunnel đang tham gia và giới hạn tổng băng thông cho các tunnel tham gia.

Các router yêu cầu cũng không có bất kỳ thông tin nào về lượng băng thông khả dụng tại mỗi hop.

Ngoài ra, các router hiện tại không có cách nào để giới hạn lưu lượng đến trên một tunnel. Điều này sẽ khá hữu ích trong thời gian quá tải hoặc DDoS một dịch vụ.

Các tham số băng thông tunnel trong các thông điệp yêu cầu và phản hồi xây dựng tunnel bổ sung hỗ trợ cho những tính năng này. Xem [Prop168](/proposals/168/) để biết thêm thông tin nền. Các tham số này được định nghĩa từ API 0.9.65, nhưng việc hỗ trợ có thể khác nhau tùy theo triển khai. Chúng được hỗ trợ cho cả các bản ghi xây dựng ECIES dài và ngắn.

### Tùy chọn Yêu cầu Xây dựng

Ba tùy chọn sau đây có thể được thiết lập trong trường ánh xạ tùy chọn xây dựng tunnel của bản ghi: Một router yêu cầu có thể bao gồm bất kỳ, tất cả, hoặc không có tùy chọn nào.

- m := băng thông tối thiểu yêu cầu cho tunnel này (KBps số nguyên dương dưới dạng chuỗi)
- r := băng thông được yêu cầu cho tunnel này (KBps số nguyên dương dưới dạng chuỗi)
- l := băng thông giới hạn cho tunnel này; chỉ gửi đến IBGW (KBps số nguyên dương dưới dạng chuỗi)

Ràng buộc: m <= r <= l

Router tham gia nên từ chối tunnel nếu "m" được chỉ định và nó không thể cung cấp ít nhất băng thông đó.

Các tùy chọn yêu cầu được gửi đến từng người tham gia trong bản ghi yêu cầu xây dựng được mã hóa tương ứng, và không hiển thị với các người tham gia khác.

### Tùy chọn Xây dựng Phản hồi

Tùy chọn sau đây có thể được đặt trong trường ánh xạ tùy chọn phản hồi xây dựng tunnel của bản ghi, khi phản hồi là ACCEPTED:

- b := băng thông khả dụng cho tunnel này (số nguyên dương KBps dưới dạng chuỗi)

Ràng buộc: b >= m

Router tham gia nên bao gồm điều này nếu "m" hoặc "r" được chỉ định trong yêu cầu xây dựng. Giá trị nên ít nhất bằng giá trị "m" nếu được chỉ định, nhưng có thể nhỏ hơn hoặc lớn hơn giá trị "r" nếu được chỉ định.

Router tham gia nên cố gắng dành riêng và cung cấp ít nhất lượng băng thông này cho tunnel, tuy nhiên điều này không được đảm bảo. Các router không thể dự đoán điều kiện 10 phút trong tương lai, và lưu lượng tham gia có mức độ ưu tiên thấp hơn lưu lượng và tunnel riêng của router.

Các router cũng có thể phân bổ quá mức băng thông khả dụng nếu cần thiết, và điều này có lẽ là mong muốn, vì các hop khác trong tunnel có thể từ chối nó.

Vì những lý do này, phản hồi của router tham gia nên được coi là cam kết cố gắng hết sức, nhưng không phải là bảo đảm.

Các tùy chọn phản hồi được gửi đến router yêu cầu trong bản ghi phản hồi xây dựng được mã hóa tương ứng, và không hiển thị với các thành viên tham gia khác.

### Ghi chú Triển khai

Các tham số băng thông được xem tại các router tham gia ở lớp tunnel, tức là số lượng tin nhắn tunnel có kích thước cố định 1 KB mỗi giây. Chi phí phụ trội của transport (NTCP2 hoặc SSU2) không được tính vào.

Băng thông này có thể nhiều hơn hoặc ít hơn đáng kể so với băng thông quan sát được ở phía client. Các thông điệp tunnel chứa overhead đáng kể, bao gồm overhead từ các lớp cao hơn như ratchet và streaming. Các thông điệp nhỏ không liên tục như streaming acks sẽ được mở rộng thành 1 KB mỗi thông điệp. Tuy nhiên, nén gzip tại lớp I2CP có thể giảm đáng kể băng thông.

Cách triển khai đơn giản nhất tại router yêu cầu là sử dụng băng thông trung bình, tối thiểu và/hoặc tối đa của các tunnel hiện tại trong pool để tính toán các giá trị đưa vào yêu cầu. Các thuật toán phức tạp hơn là có thể và tùy thuộc vào người triển khai.

Hiện tại không có tùy chọn I2CP hoặc SAM nào được định nghĩa để client có thể báo cho router biết băng thông cần thiết, và cũng không có tùy chọn mới nào được đề xuất ở đây. Các tùy chọn có thể được định nghĩa sau này nếu cần thiết.

Các triển khai có thể sử dụng băng thông khả dụng hoặc bất kỳ dữ liệu, thuật toán, chính sách cục bộ, hoặc cấu hình cục bộ nào khác để tính toán giá trị băng thông được trả về trong phản hồi xây dựng.

## Tài liệu tham khảo

- [Cấu trúc chung](/docs/specs/common-structures/)
- [Mật mã học](/docs/specs/cryptography/)
- [ECIES-ROUTERS](/docs/specs/ecies-routers/)
- [ECIES-X25519](/docs/specs/ecies/)
- [EncryptedLeaseSet](/docs/specs/encryptedleaseset/)
- [I2NP](/docs/specs/i2np/)
- [Multiple-Encryption](https://en.wikipedia.org/wiki/Multiple_encryption)
- [NOISE](https://noiseprotocol.org/noise.html)
- [NTCP2](/docs/specs/ntcp2/)
- [Prop119](/proposals/119/)
- [Prop143](/proposals/143/)
- [Prop152](/proposals/152/)
- [Prop153](/proposals/153/)
- [Prop156](/proposals/156/)
- [Prop157](/proposals/157/)
- [Prop168](/proposals/168/)
- [RFC-7539](https://tools.ietf.org/html/rfc7539)
- [RFC-7748](https://tools.ietf.org/html/rfc7748)
- [Tạo tunnel](/docs/specs/tunnel-creation/)
