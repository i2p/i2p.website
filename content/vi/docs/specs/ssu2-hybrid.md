---
title: "PQ Hybrid SSU2"
description: "Biến thể lai hậu lượng tử của giao thức truyền tải SSU2 sử dụng ML-KEM"
slug: "ssu2-hybrid"
lastupdated: "2026-10"
category: "Transports"
accurateFor: "0.9.71"
---

### Trạng thái

Beta Q2 2026, phát hành Q3 2026

## Tổng quan

Đây là biến thể hậu lượng tử lai (hybrid post-quantum) của giao thức truyền tải SSU2, được thiết kế theo Đề xuất 169. Xem đề xuất đó để biết thêm thông tin nền.

PQ Hybrid SSU2 chỉ được định nghĩa trên cùng địa chỉ và cổng với SSU2 tiêu chuẩn. Việc hoạt động trên một cổng khác, hoặc không có hỗ trợ SSU2 tiêu chuẩn, là không được phép, và sẽ không được phép trong vài năm tới, cho đến khi SSU2 tiêu chuẩn bị loại bỏ.

Đặc tả này chỉ ghi lại các thay đổi cần thiết đối với SSU2 tiêu chuẩn để hỗ trợ PQ Hybrid. Xem đặc tả SSU2 để biết chi tiết triển khai cơ bản.

## Thiết kế

Chúng tôi hỗ trợ các tiêu chuẩn NIST FIPS 203 và 204 [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf) [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf), được xây dựng dựa trên, nhưng KHÔNG tương thích với, CRYSTALS-Kyber và CRYSTALS-Dilithium (phiên bản 3.1, 3 và các phiên bản cũ hơn).

### Trao đổi khóa

PQ KEM chỉ cung cấp các khóa tạm thời (ephemeral keys) và không hỗ trợ trực tiếp các quá trình bắt tay với khóa tĩnh (static-key handshakes) như Noise XK và IK. Các loại mã hóa được sử dụng giống như trong PQ Hybrid Ratchet và được định nghĩa trong tài liệu cấu trúc chung [/docs/specs/common-structures/](/docs/specs/common-structures/), tương tự như trong [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf), các loại Hybrid chỉ được định nghĩa kết hợp với X25519.

Các loại mã hóa bao gồm:

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Code</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">SSU2 Version</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM512_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM768_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">6</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
</tr>
</table>
### Các Kết Hợp Hợp Lệ

Các loại mã hóa mới được chỉ định trong RouterAddresses. Loại mã hóa trong chứng chỉ khóa sẽ tiếp tục là loại 4.

## Đặc tả kỹ thuật

### Các Mẫu Bắt Tay

Quá trình bắt tay sử dụng các mẫu bắt tay [Noise Protocol](https://noiseprotocol.org/noise.html).

Ánh xạ ký tự sau được sử dụng:

- e = khóa tạm thời dùng một lần (one-time ephemeral key)
- s = khóa tĩnh (static key)
- p = tải trọng tin nhắn (message payload)
- e1 = khóa PQ tạm thời dùng một lần, gửi từ Alice đến Bob
- ekem1 = bản mã KEM (KEM ciphertext), gửi từ Bob đến Alice

Các sửa đổi sau đây đối với XK và IK cho tính bảo mật chuyển tiếp lai (hfs) được quy định trong [Noise HFS spec](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) phần 5:

```
XK:                       XKhfs:
  <- s                      <- s
  ...                       ...
  -> e, es, p               -> e, es, e1, p
  <- e, ee, p               <- e, ee, ekem1, p
  -> s, se                  -> s, se
  <- p                      <- p
  p ->                      p ->


  e1 and ekem1 are encrypted. See pattern definitions below.
  NOTE: e1 and ekem1 are different sizes (unlike X25519)
```
Mẫu e1 được định nghĩa như sau, theo quy định trong [đặc tả Noise HFS](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) mục 4:

```
For Alice:
  (encap_key, decap_key) = PQ_KEYGEN()

  // EncryptAndHash(encap_key)
  ciphertext = ENCRYPT(k, n, encap_key, ad)
  n++
  MixHash(ciphertext)

  For Bob:

  // DecryptAndHash(ciphertext)
  encap_key = DECRYPT(k, n, ciphertext, ad)
  n++
  MixHash(ciphertext)
```
Mẫu ekem1 được định nghĩa như sau, theo quy định trong [đặc tả Noise HFS](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) phần 4:

```
For Bob:

  (kem_ciphertext, kem_shared_key) = ENCAPS(encap_key)

  // EncryptAndHash(kem_ciphertext)
  ciphertext = ENCRYPT(k, n, kem_ciphertext, ad)
  MixHash(ciphertext)

  // MixKey
  MixKey(kem_shared_key)


  For Alice:

  // DecryptAndHash(ciphertext)
  kem_ciphertext = DECRYPT(k, n, ciphertext, ad)
  MixHash(ciphertext)

  // MixKey
  kem_shared_key = DECAPS(kem_ciphertext, decap_key)
  MixKey(kem_shared_key)
```
### KDF bắt tay Noise

#### Tổng quan

Quy trình bắt tay hybrid được định nghĩa trong [đặc tả Noise HFS](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf). Tin nhắn đầu tiên, từ Alice đến Bob, chứa e1, khóa đóng gói (encapsulation key), đặt trước phần nội dung tin nhắn. Khóa này được xử lý như một khóa tĩnh bổ sung; gọi `EncryptAndHash()` (với tư cách Alice) hoặc `DecryptAndHash()` (với tư cách Bob). Sau đó xử lý phần nội dung tin nhắn như bình thường.

Thông điệp thứ hai, từ Bob gửi đến Alice, chứa ekem1, là bản mã (ciphertext), được đặt trước phần nội dung thông điệp. Phần này được xử lý như một static key bổ sung; gọi EncryptAndHash() (đối với Bob) hoặc DecryptAndHash() (đối với Alice). Sau đó, tính toán kem_shared_key và gọi MixKey(kem_shared_key). Tiếp theo, xử lý phần nội dung thông điệp theo cách thông thường.

#### Các phép toán ML-KEM được định nghĩa

Chúng tôi định nghĩa các hàm sau đây tương ứng với các khối xây dựng mật mã được sử dụng theo định nghĩa trong [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf).

(encap_key, decap_key) = PQ_KEYGEN()

    Alice creates the encapsulation and decapsulation keys
    The encapsulation key is sent in message 1.
    encap_key and decap_key sizes vary based on ML-KEM variant.

(ciphertext, kem_shared_key) = ENCAPS(encap_key)

    Bob calculates the ciphertext and shared key,
    using the ciphertext received in message 1.
    The ciphertext is sent in message 2.
    ciphertext size varies based on ML-KEM variant.
    The kem_shared_key is always 32 bytes.

kem_shared_key = DECAPS(ciphertext, decap_key)

    Alice calculates the shared key,
    using the ciphertext received in message 2.
    The kem_shared_key is always 32 bytes.

Lưu ý rằng cả encap_key và ciphertext đều được mã hóa bên trong các khối ChaCha/Poly trong các thông điệp bắt tay Noise số 1 và 2. Chúng sẽ được giải mã như một phần của quá trình bắt tay.

Khóa kem_shared_key được trộn vào chaining key (khóa dây chuyền) thông qua MixHash(). Xem bên dưới để biết thêm chi tiết.

#### KDF của Alice cho Tin nhắn 1

Sau mẫu tin nhắn 'es' và trước phần payload, thêm vào:

```
This is the "e1" message pattern:
  (encap_key, decap_key) = PQ_KEYGEN()

  // EncryptAndHash(encap_key)
  // AEAD parameters
  k = keydata[32:63]
  n = 0
  ad = h
  ciphertext = ENCRYPT(k, n, encap_key, ad)
  n++

  // MixHash(ciphertext)
  h = SHA256(h || ciphertext)


  End of "e1" message pattern.

  NOTE: For the next section (payload for XK or static key for IK),
  the keydata and chain key remain the same,
  and n now equals 1 (instead of 0 for non-hybrid).
```
#### KDF của Bob cho Tin nhắn 1

Sau mẫu tin nhắn 'es' và trước phần payload, thêm vào:

```
This is the "e1" message pattern:

  // DecryptAndHash(encap_key_section)
  // AEAD parameters
  k = keydata[32:63]
  n = 0
  ad = h
  encap_key = DECRYPT(k, n, encap_key_section, ad)
  n++

  // MixHash(encap_key_section)
  h = SHA256(h || encap_key_section)

  End of "e1" message pattern.

  NOTE: For the next section (payload for XK or static key for IK),
  the keydata and chain key remain the same,
  and n now equals 1 (instead of 0 for non-hybrid).
```
#### KDF của Bob cho Tin nhắn 2

Đối với XK: Sau mẫu thông điệp 'ee' và trước payload, thêm vào:

```
This is the "ekem1" message pattern:

  (kem_ciphertext, kem_shared_key) = ENCAPS(encap_key)

  // EncryptAndHash(kem_ciphertext)
  // AEAD parameters
  k = keydata[32:63]
  n = 0
  ad = h
  ciphertext = ENCRYPT(k, n, kem_ciphertext, ad)

  // MixHash(ciphertext)
  h = SHA256(h || ciphertext)

  // MixKey(kem_shared_key)
  keydata = HKDF(chainKey, kem_shared_key, "", 64)
  chainKey = keydata[0:31]

  End of "ekem1" message pattern.

  // AEAD parameters for payload section
  ... as in standard SSU2 ...
  k = keydata[32:63]
  ...

```
#### Alice KDF cho Thông điệp 2

Sau mẫu tin nhắn 'ee', thêm vào:

```
This is the "ekem1" message pattern:

  // DecryptAndHash(kem_ciphertext_section)
  // AEAD parameters
  k = keydata[32:63]
  n = 0
  ad = h
  kem_ciphertext = DECRYPT(k, n, kem_ciphertext_section, ad)

  // MixHash(kem_ciphertext_section)
  h = SHA256(h || kem_ciphertext_section)

  // MixKey(kem_shared_key)
  kem_shared_key = DECAPS(kem_ciphertext, decap_key)
  keydata = HKDF(chainKey, kem_shared_key, "", 64)
  chainKey = keydata[0:31]

  End of "ekem1" message pattern.

  // AEAD parameters for payload section
  ... as in standard SSU2 ...
  k = keydata[32:63]
  ...

```
#### KDF cho Tin nhắn 3

unchanged

#### KDF cho split()

unchanged

### Chi tiết bắt tay (Handshake)

#### Định danh Noise

- "Noise_XKhfschaobfse+hs1+hs2+hs3_25519+MLKEM512_ChaChaPoly_SHA256"
- "Noise_XKhfschaobfse+hs1+hs2+hs3_25519+MLKEM768_ChaChaPoly_SHA256"

Lưu ý rằng MLKEM-1024 KHÔNG được hỗ trợ cho SSU2, vì các khóa quá lớn để vừa trong một datagram tiêu chuẩn 1500 byte.

#### Tiêu đề dài

Header dài có độ dài 32 byte. Nó được sử dụng trước khi một phiên được tạo, cho các thông điệp Token Request, SessionRequest, SessionCreated và Retry. Nó cũng được sử dụng cho các thông điệp Peer Test và Hole Punch ngoài phiên.

Trong các thông điệp sau, đặt trường ver (version) trong long header thành 3 hoặc 4, để chỉ định MLKEM-512 hoặc MLKEM-768.

- (0) Yêu cầu phiên (Session Request)
- (1) Phiên đã tạo (Session Created)
- (9) Thử lại (Retry)
- (10) Yêu cầu token (Token Request)
- (11) Đục lỗ (Hole Punch)

Trong các thông điệp sau, hãy đặt trường ver (version) trong phần header dài thành 2 như thông thường, ngay cả khi MLKEM-512 hoặc MLKEM-768 được hỗ trợ. Các triển khai cũng có thể đặt giá trị này thành 3 hoặc 4 nếu phía đầu kia hỗ trợ, nhưng điều này không bắt buộc. Các triển khai nên chấp nhận bất kỳ giá trị nào từ 2 đến 4.

- (7) Kiểm tra ngang hàng (Peer Test) (các thông điệp ngoài phiên 5-7)

Thảo luận: Việc đặt trường version thành 3 hoặc 4 có thể không thực sự cần thiết cho tất cả các loại thông điệp, nhưng làm như vậy giúp phát hiện lỗi sớm hơn đối với các kết nối hậu lượng tử (post-quantum) chưa được hỗ trợ. Token Request và Retry (loại 9 và 10) nên có version 3/4 để đảm bảo tính nhất quán. Các thông điệp Hole Punch (loại 11) có thể không yêu cầu cách xử lý này, nhưng chúng ta sẽ tuân theo cùng một mẫu để đảm bảo tính đồng nhất. Thông điệp Peer Test (loại 7) là thông điệp ngoài phiên (out-of-session) và không biểu thị ý định khởi tạo một phiên.

- Yêu cầu chuyển tiếp (Relay Request)
- Phản hồi chuyển tiếp (Relay Response)
- Giới thiệu chuyển tiếp (Relay Intro)
- Kiểm tra ngang hàng (Peer Test)

Trước khi mã hóa header:

Trước khi mã hóa tiêu đề:

```

  +----+----+----+----+----+----+----+----+
  |      Destination Connection ID        |
  +----+----+----+----+----+----+----+----+
  |   Packet Number   |type| ver| id |flag|
  +----+----+----+----+----+----+----+----+
  |        Source Connection ID           |
  +----+----+----+----+----+----+----+----+
  |                 Token                 |
  +----+----+----+----+----+----+----+----+

  Destination Connection ID :: 8 bytes, unsigned big endian integer

  Packet Number :: 4 bytes, unsigned big endian integer

  type :: The message type = 0, 1, 7, 9, 10, or 11

  ver :: The protocol version = 2, 3, or 4 for non-PQ, MLKEM512, MLKEM768

  id :: 1 byte, the network ID (currently 2, except for test networks)

  flag :: 1 byte, unused, set to 0 for future compatibility

  Source Connection ID :: 8 bytes, unsigned big endian integer

  Token :: 8 bytes, unsigned big endian integer

```
#### Header Ngắn

unchanged

#### SessionRequest (Loại 0)

Thay đổi: SSU2 hiện tại chỉ chứa dữ liệu khối trong một phần ChaCha duy nhất. Với ML-KEM, sẽ có một phần ChaCha mới trước dữ liệu khối, chứa khóa công khai PQ đã được mã hóa.

Thay đổi KDF để Chống Giả mạo: Để giải quyết các vấn đề được nêu ra trong Đề xuất 165 [Prop165]_, nhưng với một giải pháp khác, chúng tôi sửa đổi KDF cho Session Request. Điều này chỉ áp dụng cho các phiên PQ. KDF cho các phiên không phải PQ vẫn giữ nguyên không thay đổi.

```

// End of KDF for initial chain key (unchanged)
  // Bob static key
  // MixHash(bpk)
  h = SHA256(h || bpk);

  // Start of KDF for session request
  // NEW for PQ only
  // bhash = Bob router hash (32 bytes)
  // MixHash(bhash)
  h = SHA256(h || bhash);

  // Rest of KDF for session request, unchanged, as in SSU2 spec
  // MixHash(header)
  h = SHA256(h || header)

  ...

```
Nội dung thô:

```
  +----+----+----+----+----+----+----+----+
  |  Long Header bytes 0-15, ChaCha20     |
  +  encrypted with Bob intro key         +
  |    See Header Encryption KDF          |
  +----+----+----+----+----+----+----+----+
  |  Long Header bytes 16-31, ChaCha20    |
  +  encrypted with Bob intro key n=0     +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +       X, ChaCha20 encrypted           +
  |       with Bob intro key n=0          |
  +              (32 bytes)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   ChaCha20 encrypted data (MLKEM)     |
  +          (length varies)              +
  |  k defined in KDF for Session Request |
  +  n = 0                                +
  |  see KDF for associated data          |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   ChaCha20 encrypted data (payload)   |
  +          (length varies)              +
  |  k defined in KDF for Session Request |
  +  n = 1                                +
  |  see KDF for associated data          |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+


```
Dữ liệu chưa được mã hóa (thẻ xác thực Poly1305 không hiển thị):

```
  +----+----+----+----+----+----+----+----+
  |      Destination Connection ID        |
  +----+----+----+----+----+----+----+----+
  |   Packet Number   |type| ver| id |flag|
  +----+----+----+----+----+----+----+----+
  |        Source Connection ID           |
  +----+----+----+----+----+----+----+----+
  |                 Token                 |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |                   X                   |
  +              (32 bytes)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |           ML-KEM encap_key            |
  +      (see table below for length)     +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     Noise payload (block data)        |
  +          (length varies)              +
  |     see below for allowed blocks      |
  +----+----+----+----+----+----+----+----+
```
Kích thước, không tính chi phí IP:

| Loại | Mã loại | Độ dài X | Độ dài Msg 1 | Độ dài Msg 1 đã mã hóa | Độ dài Msg 1 đã giải mã | Độ dài khóa PQ | Độ dài pl |
|------|-----------|-------|-----------|---------------|---------------|------------|--------|
| X25519 | 4 | 32 | 80+pl | 16+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 896+pl | 832+pl | 800+pl | 800 | pl |
| MLKEM768_X25519 | 6 | 32 | 1280+pl | 1216+pl | 1184+pl | 1184 | pl |
| MLKEM1024_X25519 | 7 | n/a | quá lớn | | | | |
Lưu ý: Mã loại (type codes) chỉ dành cho mục đích nội bộ. Các router sẽ vẫn là loại 4, và hỗ trợ sẽ được chỉ định trong các địa chỉ router.

MTU tối thiểu cho MLKEM768_X25519: 1318 đối với IPv4 và 1338 đối với IPv6. Xem bên dưới.

Thay đổi: SSU2 hiện tại chỉ chứa phần tải trong một phần ChaCha duy nhất. Với ML-KEM, sẽ có một phần ChaCha mới trước phần tải, chứa mã hóa văn bản PQ.

#### SessionCreated (Loại 1)

Thay đổi: SSU2 hiện tại chỉ chứa phần tải trong một phần ChaCha duy nhất. Với ML-KEM, sẽ có một phần ChaCha mới trước phần tải, chứa mã hóa văn bản mật PQ.

Nội dung thô:

```
  +----+----+----+----+----+----+----+----+
  |  Long Header bytes 0-15, ChaCha20     |
  +  encrypted with Bob intro key and     +
  | derived key, see Header Encryption KDF|
  +----+----+----+----+----+----+----+----+
  |  Long Header bytes 16-31, ChaCha20    |
  +  encrypted with derived key n=0       +
  |  See Header Encryption KDF            |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +       Y, ChaCha20 encrypted           +
  |       with derived key n=0            |
  +              (32 bytes)               +
  |       See Header Encryption KDF       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaCha20 data (MLKEM)               |
  +   Encrypted and authenticated data    +
  |  length varies                        |
  +  k defined in KDF for Session Created +
  |  (before mixKey)                      |
  +  n = 0; see KDF for associated data   +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaCha20 data (payload)             |
  +   Encrypted and authenticated data    +
  |  length varies                        |
  +  k defined in KDF for Session Created +
  |  (after mixKey)                       |
  +  n = 0; see KDF for associated data   +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+


```
Dữ liệu chưa được mã hóa (thẻ xác thực Poly1305 không hiển thị):

```
  +----+----+----+----+----+----+----+----+
  |      Destination Connection ID        |
  +----+----+----+----+----+----+----+----+
  |   Packet Number   |type| ver| id |flag|
  +----+----+----+----+----+----+----+----+
  |        Source Connection ID           |
  +----+----+----+----+----+----+----+----+
  |                 Token                 |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |                  Y                    |
  +              (32 bytes)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |           ML-KEM Ciphertext           |
  +      (see table below for length)     +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     Noise payload (block data)        |
  +          (length varies)              +
  |      see below for allowed blocks     |
  +----+----+----+----+----+----+----+----+
```
Kích thước, không tính chi phí IP:

| Loại | Mã loại | Độ dài Y | Độ dài Msg 2 | Độ dài Msg 2 Enc | Độ dài Msg 2 Dec | Độ dài PQ CT | Độ dài pl |
|------|-----------|-------|-----------|---------------|---------------|-----------|--------|
| X25519 | 4 | 32 | 80+pl | 16+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 864+pl | 800+pl | 768+pl | 768 | pl |
| MLKEM768_X25519 | 6 | 32 | 1184+pl | 1120+pl | 1088+pl | 1088 | pl |
| MLKEM1024_X25519 | 7 | n/a | quá lớn | | | | |
Lưu ý: Mã loại (type codes) chỉ dành cho mục đích nội bộ. Các router sẽ vẫn là loại 4, và hỗ trợ sẽ được chỉ định trong các địa chỉ router.

MTU tối thiểu cho MLKEM768_X25519: 1318 đối với IPv4 và 1338 đối với IPv6. Xem bên dưới.

Kích thước tối đa: Alice vẫn chưa có RouterInfo của Bob và không biết MTU mà anh ta đã công bố. Đối với tin nhắn này, hãy sử dụng MTU tạm thời như sau. Đối với MLKEM512_X25519, hãy dùng giá trị lớn nhất giữa 1280 hoặc kích thước SessionRequest đã nhận làm MTU. Đối với MLKEM768_X25519, hãy dùng giá trị lớn nhất giữa (1318 đối với IPv4 hoặc 1338 đối với IPv6) hoặc kích thước SessionRequest đã nhận làm MTU. Phần đầu (overhead) của SessionCreated nhỏ hơn phần đầu của SessionRequest, vì văn bản mã hóa MLKEM nhỏ hơn khóa công khai MLKEM. Điều này cho phép một phạm vi kích thước đệm (padding) trong SessionCreated ngay cả khi phần SessionRequest có rất ít hoặc không có đệm.

#### SessionConfirmed (Loại 2)

unchanged

#### KDF cho giai đoạn truyền dữ liệu

unchanged

#### Relay và Kiểm tra Ngang hàng

Các khối sau đây chứa các trường phiên bản. Chúng sẽ giữ nguyên phiên bản 2 (để tương thích với Bob không hỗ trợ PQ), và sẽ không thay đổi sang phiên bản 3/4 cho PQ.

* [CABFORUM](https://cabforum.org/2024/10/10/2024-10-10-minutes-of-the-code-signing-certificate-working-group/)
* [Choosing-Hash](https://kerkour.com/fast-secure-hash-function-sha256-sha512-sha3-blake3)
* [CLOUDFLARE](https://blog.cloudflare.com/pq-2024/)
* [COMMON](/docs/specs/common-structures/)
* [COMPOSITE-SIGS](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/)
* [ECIES](/docs/specs/ecies/)
* [FORUM](http://zzz.i2p/topics/3294)
* [FIPS202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf)
* [FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)
* [FIPS204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf)
* [FIPS205](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.205.pdf)
* [MLDSA-OIDS](https://datatracker.ietf.org/doc/draft-ietf-lamps-dilithium-certificates/)
* [NIST-PQ](https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards)
* [NIST-PQ-UPDATE](https://csrc.nist.gov/csrc/media/Presentations/2022/update-on-post-quantum-encryption-and-cryptographi/Day%202%20-%20230pm%20Chen%20PQC%20ISPAB.pdf)
* [NIST-PQ-END](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf)
* [NIST-VECTORS](https://csrc.nist.gov/projects/cryptographic-standards-and-guidelines/example-values)
* [Noise](https://noiseprotocol.org/noise.html)
* [Noise-Hybrid](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf)
* [NSA-PQ](https://media.defense.gov/2022/Sep/07/2003071836/-1/-1/0/CSI_CNSA_2.0_FAQ_.PDF)
* [NTCP2](/docs/specs/ntcp2/)
* [OPENSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/)
* [Prop165](/docs/proposals/165/)
* [PQ-WIREGUARD](https://eprint.iacr.org/2020/379.pdf)
* [RFC-2104](https://tools.ietf.org/html/rfc2104)
* [Rosenpass](https://rosenpass.eu/)
* [Rosenpass-Whitepaper](https://raw.githubusercontent.com/rosenpass/rosenpass/papers-pdf/whitepaper.pdf)
* [SSH-HYBRID](https://datatracker.ietf.org/doc/draft-ietf-sshm-mlkem-hybrid-kex/)
* [SSU2](/docs/specs/ssu2/)
* [TLS-HYBRID](https://datatracker.ietf.org/doc/draft-ietf-tls-hybrid-design/)

#### Địa chỉ đã công bố

Trong tất cả các trường hợp, hãy sử dụng tên transport SSU2 như thông thường. MLKEM-1024 không được hỗ trợ.

Sử dụng cùng địa chỉ/cổng như cấu hình non-PQ, không bị tường lửa. Một hoặc cả hai biến thể PQ đều được hỗ trợ. Trong địa chỉ router, công bố v=2 (như thông thường) và tham số mới pq=[3|4|3,4|4,3] để chỉ định MLKEM 512/768/cả hai. Các router có MTU nhỏ hơn mức tối thiểu được chỉ định bên dưới không được công bố tham số "pq" có chứa "4". Công bố 4,3 để chỉ ưu tiên MLKEM-768 hoặc 3,4 để chỉ ưu tiên MLKEM-512. Phiên bản thực tế do bên khởi tạo quyết định và tùy chọn ưu tiên có thể không được tuân theo. Các router có MTU nhỏ hơn mức tối thiểu được chỉ định bên dưới không được kết nối sử dụng MLKEM768. Các router cũ hơn sẽ bỏ qua tham số pq và kết nối theo cách non-pq như thông thường.

Địa chỉ/cổng khác so với non-PQ, hoặc chỉ dùng PQ mà không có tường lửa là KHÔNG được hỗ trợ. Tính năng này sẽ không được triển khai cho đến khi SSU2 non-PQ bị vô hiệu hóa, tức là vài năm nữa. Khi non-PQ bị vô hiệu hóa, một hoặc cả hai biến thể PQ sẽ được hỗ trợ. Trong địa chỉ router, hãy công bố v=[3|4|3,4|4,3] để chỉ định MLKEM 512/768/cả hai. Các router cũ hơn sẽ kiểm tra tham số v và bỏ qua địa chỉ này vì không được hỗ trợ.

Địa chỉ bị tường lửa (không công bố IP): Trong địa chỉ router, công bố v=2 (như thường lệ). Tham số pq PHẢI được công bố trong các địa chỉ bị tường lửa, để hỗ trợ relay.

Alice có thể kết nối với một Bob hỗ trợ PQ bằng cách sử dụng biến thể PQ mà Bob công bố, bất kể Alice có quảng bá hỗ trợ PQ trong thông tin router của cô ấy hay không, hoặc liệu cô ấy có quảng bá cùng một biến thể hay không.

#### MTU

Hãy cẩn thận để không vượt quá MTU khi sử dụng MLKEM768. MTU tối thiểu cho MLKEM768_X25519 là 1318 đối với IPv4 và 1338 đối với IPv6 (giả sử payload tối thiểu là 10 byte với một khối DateTime và một khối Padding hoặc RelayTagRequest). MTU tối thiểu cho SSU2 nói chung là 1280, do đó không phải tất cả các peer đều có thể sử dụng MLKEM768. Không công bố hoặc sử dụng MLKEM768 nếu MTU thực tế nhỏ hơn mức tối thiểu, dù là ở phía local hay do peer quảng bá. Cần chú ý không thêm kích thước padding khiến message 1 hoặc 2 vượt quá MTU của local hoặc remote.

## Phân tích chi phí tải mạng

### Trao đổi khóa

Tăng kích thước (byte):

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Pubkey (Msg 1)</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Ciphertext (Msg 2)</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM512_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">+816</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">+784</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM768_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">+1200</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">+1104</td>
</tr>
</table>
## Phân tích Bảo mật

Các danh mục bảo mật NIST được tóm tắt trong [bản trình bày của NIST](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf) trang 10. Tiêu chí sơ bộ: Danh mục bảo mật NIST tối thiểu của chúng ta nên là 2 đối với các giao thức kết hợp (hybrid) và 3 đối với các giao thức chỉ dùng PQ (hậu lượng tử thuần túy).

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Category</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">As Secure As</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">AES128</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">SHA256</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">AES192</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">SHA384</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">AES256</td>
</tr>
</table>
### Bắt tay (Handshakes)

Đây đều là các giao thức lai (hybrid protocols). Các triển khai nên ưu tiên sử dụng MLKEM768; MLKEM512 không đủ an toàn.

Các danh mục bảo mật NIST [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf):

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Algorithm</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Security Category</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM512</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM768</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
</tr>
</table>
## Ghi chú Triển khai

### Hỗ trợ Thư viện

Các thư viện Bouncycastle, BoringSSL và WolfSSL hiện đã hỗ trợ MLKEM và MLDSA. Hỗ trợ OpenSSL sẽ có trong bản phát hành 3.5 vào ngày 8 tháng 4 năm 2025 [OpenSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/).

### Nhận dạng lưu lượng đến

Chúng ta đặt bit MSB của khóa tạm thời (key[31] & 0x80) trong session request để chỉ ra rằng đây là một kết nối hybrid. Điều này cho phép chúng ta chạy đồng thời cả NTCP tiêu chuẩn và NTCP hybrid trên cùng một cổng. Chỉ một biến thể hybrid được hỗ trợ cho kết nối đến (inbound) và được quảng bá trong địa chỉ router. Ví dụ: pq=3 hoặc pq=4.

## Khả năng tương thích của Router

### Tên Transport

Với tư cách là Alice, để thiết lập kết nối PQ, trước khi thực hiện obfuscation (che giấu), hãy đặt X[31] |= 0x80. Điều này làm cho X trở thành một khóa công khai X25519 không hợp lệ. Sau khi obfuscation, AES-CBC sẽ ngẫu nhiên hóa nó. Bit có trọng số cao nhất (MSB) của X sẽ ngẫu nhiên sau khi obfuscation.

## Tài liệu tham khảo

* [CLOUDFLARE](https://blog.cloudflare.com/pq-2024/)
* [COMMON](/docs/specs/common-structures/)
* [ECIES](/docs/specs/ecies/)
* [FORUM](http://zzz.i2p/topics/3294)
* [FIPS202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf)
* [FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)
* [NIST-PQ](https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards)
* [NIST-PQ-UPDATE](https://csrc.nist.gov/csrc/media/Presentations/2022/update-on-post-quantum-encryption-and-cryptographi/Day%202%20-%20230pm%20Chen%20PQC%20ISPAB.pdf)
* [NIST-PQ-END](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf)
* [NIST-VECTORS](https://csrc.nist.gov/projects/cryptographic-standards-and-guidelines/example-values)
* [Noise](https://noiseprotocol.org/noise.html)
* [Noise-Hybrid](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf)
* [NSA-PQ](https://media.defense.gov/2022/Sep/07/2003071836/-1/-1/0/CSI_CNSA_2.0_FAQ_.PDF)
* [OPENSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/)
* [Prop165](/docs/proposals/165/)
* [PQ-WIREGUARD](https://eprint.iacr.org/2020/379.pdf)
* [RFC-2104](https://tools.ietf.org/html/rfc2104)
* [Rosenpass](https://rosenpass.eu/)
* [Rosenpass-Whitepaper](https://raw.githubusercontent.com/rosenpass/rosenpass/papers-pdf/whitepaper.pdf)
* [SSH-HYBRID](https://datatracker.ietf.org/doc/draft-ietf-sshm-mlkem-hybrid-kex/)
* [SSU2](/docs/specs/ssu2/)
* [TLS-HYBRID](https://datatracker.ietf.org/doc/draft-ietf-tls-hybrid-design/)
