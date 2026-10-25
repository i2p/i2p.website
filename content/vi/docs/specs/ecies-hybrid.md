---
title: "PQ Hybrid ECIES-X25519-AEAD-Ratchet"
description: "Biến thể lai lượng tử hậu của giao thức mã hóa ECIES sử dụng ML-KEM"
slug: "ecies-hybrid"
category: "Các giao thức"
lastUpdated: "2026-04"
accurateFor: "0.9.69"
---

## Lưu ý

Việc triển khai, kiểm thử và phát hành đang trong quá trình thực hiện trên các router implementation khác nhau. Hãy kiểm tra tài liệu của những implementation đó để biết trạng thái.

## Tổng quan

Đây là phiên bản PQ Hybrid của giao thức ECIES-X25519-AEAD-Ratchet [ECIES](/docs/specs/ecies/). Đây là giai đoạn đầu tiên của đề xuất PQ tổng thể [Prop169](/proposals/169-pq-crypto/) được phê duyệt. Xem đề xuất đó để biết các mục tiêu tổng thể, mô hình mối đe dọa, phân tích, các lựa chọn thay thế và thông tin bổ sung.

Đặc tả này chỉ chứa những điểm khác biệt so với [ECIES](/docs/specs/ecies/) tiêu chuẩn và phải được đọc cùng với đặc tả đó.

## Thiết kế

Chúng tôi hỗ trợ tiêu chuẩn NIST FIPS 203 [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf), tiêu chuẩn này dựa trên CRYSTALS-Kyber nhưng KHÔNG tương thích với CRYSTALS-Kyber.

Hybrid handshakes được chỉ định như trong [Noise-Hybrid](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf).

### Trao Đổi Khóa

Chúng tôi định nghĩa một trao đổi khóa lai cho Ratchet. PQ KEM chỉ cung cấp các khóa tạm thời và không trực tiếp hỗ trợ các handshake khóa tĩnh như Noise IK.

Chúng tôi định nghĩa ba biến thể ML-KEM như trong [FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf), tổng cộng 3 loại mã hóa mới. Các loại hybrid chỉ được định nghĩa khi kết hợp với X25519.

Các loại mã hóa mới là:

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Code</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM512_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM768_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">6</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM1024_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">7</td>
</tr>
</table>
Overhead sẽ rất đáng kể. Kích thước điển hình của message 1 và 2 (cho IK) hiện tại khoảng 100 bytes (trước khi có bất kỳ payload bổ sung nào). Điều này sẽ tăng từ 8x đến 15x tùy thuộc vào thuật toán.

### Yêu cầu mã hóa mới

- ML-KEM (trước đây là CRYSTALS-Kyber) [FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)
- SHA3-128 (trước đây là Keccak-256) [FIPS202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf) Chỉ được sử dụng cho SHAKE128
- SHA3-256 (trước đây là Keccak-512) [FIPS202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf)
- SHAKE128 và SHAKE256 (phần mở rộng XOF cho SHA3-128 và SHA3-256)
  [FIPS202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf)

Các vector kiểm tra cho SHA3-256, SHAKE128, và SHAKE256 có tại [NIST-VECTORS](https://csrc.nist.gov/projects/cryptographic-standards-and-guidelines/example-values).

Lưu ý rằng thư viện Java bouncycastle hỗ trợ tất cả các mục trên. Hỗ trợ thư viện C++ có trong OpenSSL 3.5 [OPENSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/).

## Thông số kỹ thuật

### Cấu trúc Chung

Xem đặc tả cấu trúc chung [COMMON](/docs/specs/common-structures/) để biết độ dài khóa và các định danh.

### Các Mẫu Bắt Tay

Handshake sử dụng các mẫu handshake [Noise](https://noiseprotocol.org/noise.html).

Ánh xạ chữ cái sau đây được sử dụng:

- e = khóa tạm thời một lần
- s = khóa tĩnh
- p = tải trọng thông điệp
- e1 = khóa PQ tạm thời một lần, gửi từ Alice đến Bob
- ekem1 = bản mã KEM, gửi từ Bob đến Alice

Các sửa đổi sau đây đối với XK và IK cho hybrid forward secrecy (hfs) được quy định như trong [Noise-Hybrid](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) mục 5:

```
IK:                         IKhfs:
<- s                        <- s
...                         ...
-> e, es, s, ss, p          -> e, es, e1, s, ss, p
<- tag, e, ee, se, p        <- tag, e, ee, ekem1, se, p
<- p                        <- p
p ->                        p ->

e1 and ekem1 are encrypted. See pattern definitions below.
NOTE: e1 and ekem1 are different sizes (unlike X25519)
```
Mẫu e1 được định nghĩa như sau, theo đặc tả trong [Noise-Hybrid](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) phần 4:

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
Mẫu ekem1 được định nghĩa như sau, theo quy định trong [Noise-Hybrid](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) phần 4:

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
### Các Phép Toán ML-KEM Được Định Nghĩa

Chúng tôi định nghĩa các hàm sau tương ứng với các khối xây dựng mật mã được sử dụng như đã định nghĩa trong [FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf).

**(encap_key, decap_key) = PQ_KEYGEN()**

Alice tạo ra các khóa đóng gói và giải mã. Khóa đóng gói được gửi trong thông điệp NS. Kích thước encap_key và decap_key thay đổi dựa trên biến thể ML-KEM.

**(ciphertext, kem_shared_key) = ENCAPS(encap_key)**

Bob tính toán ciphertext và shared key, sử dụng ciphertext nhận được trong thông điệp NS. Ciphertext được gửi trong thông điệp NSR. Kích thước ciphertext thay đổi dựa trên biến thể ML-KEM. kem_shared_key luôn có kích thước 32 byte.

**kem_shared_key = DECAPS(ciphertext, decap_key)**

Alice tính toán khóa chia sẻ, sử dụng ciphertext nhận được trong thông điệp NSR. Khóa kem_shared_key luôn có độ dài 32 byte.

Lưu ý rằng cả encap_key và ciphertext đều được mã hóa bên trong các khối ChaCha/Poly trong các thông điệp bắt tay Noise 1 và 2. Chúng sẽ được giải mã như một phần của quá trình bắt tay.

kem_shared_key được trộn vào chaining key bằng MixHash(). Xem chi tiết bên dưới.

### Noise Handshake KDF

#### Tổng quan

Handshake hybrid được định nghĩa trong [Noise-Hybrid](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf). Thông điệp đầu tiên, từ Alice gửi tới Bob, chứa e1, encapsulation key, trước message payload. Điều này được xử lý như một static key bổ sung; gọi EncryptAndHash() trên nó (với vai trò Alice) hoặc DecryptAndHash() (với vai trò Bob). Sau đó xử lý message payload như thường lệ.

Thông điệp thứ hai, từ Bob đến Alice, chứa ekem1, bản mã hóa, trước phần tải tin nhắn. Điều này được xử lý như một khóa tĩnh bổ sung; gọi EncryptAndHash() trên đó (với vai trò Bob) hoặc DecryptAndHash() (với vai trò Alice). Sau đó, tính toán kem_shared_key và gọi MixKey(kem_shared_key). Tiếp theo xử lý phần tải tin nhắn như bình thường.

#### Định danh Noise

Đây là các chuỗi khởi tạo Noise:

- "Noise_IKhfselg2_25519+MLKEM512_ChaChaPoly_SHA256"
- "Noise_IKhfselg2_25519+MLKEM768_ChaChaPoly_SHA256"
- "Noise_IKhfselg2_25519+MLKEM1024_ChaChaPoly_SHA256"

#### Alice KDF cho NS Message

Sau mẫu thông điệp 'es' và trước mẫu thông điệp 's', thêm:

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

NOTE: For the next section (static key for IK),
the keydata and chain key remain the same, and n now equals 1
(instead of 0 for non-hybrid).
```
#### Bob KDF cho NS Message

Sau mẫu thông điệp 'es' và trước mẫu thông điệp 's', thêm:

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

NOTE: For the next section (static key for IK),
the keydata and chain key remain the same, and n now equals 1
(instead of 0 for non-hybrid).
```
#### Bob KDF cho Thông điệp NSR

Sau mẫu thông điệp 'ee' và trước mẫu thông điệp 'se', thêm:

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
```
#### Alice KDF cho Thông điệp NSR

Sau mẫu thông điệp 'ee' và trước mẫu thông điệp 'ss', thêm:

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
```
#### KDF cho split()

không thay đổi

### Định dạng Thông điệp

#### Định dạng NS

Thay đổi: Ratchet hiện tại chứa static key trong phần ChaCha đầu tiên, và payload trong phần thứ hai. Với ML-KEM, giờ có ba phần. Phần đầu tiên chứa PQ public key được mã hóa. Phần thứ hai chứa static key. Phần thứ ba chứa payload.

Định dạng mã hóa:

```
+----+----+----+----+----+----+----+----+
|                                       |
+         New Session Ephemeral         +
|            Public Key                 |
+            32 bytes                   +
|      Encoded with Elligator2          |
+----+----+----+----+----+----+----+----+
|                                       |
+         ML-KEM encap_key              +
|       ChaCha20 encrypted data         |
+   (see table below for length)        +
|                                       |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+      (MAC) for encap_key Section      +
|              16 bytes                 |
+----+----+----+----+----+----+----+----+
|                                       |
+         X25519 Static Key             +
|       ChaCha20 encrypted data         |
+            32 bytes                   +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+     (MAC) for Static Key Section      +
|              16 bytes                 |
+----+----+----+----+----+----+----+----+
|                                       |
+          Payload Section              +
|       ChaCha20 encrypted data         |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+      (MAC) for Payload Section        +
|              16 bytes                 |
+----+----+----+----+----+----+----+----+
```
Định dạng đã giải mã:

```
Payload Part 1:

+----+----+----+----+----+----+----+----+
|                                       |
+         ML-KEM encap_key              +
|                                       |
+   (see table below for length)        +
|                                       |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

Payload Part 2:

+----+----+----+----+----+----+----+----+
|                                       |
+         X25519 Static Key             +
|            (32 bytes)                 |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+

Payload Part 3:

+----+----+----+----+----+----+----+----+
|                                       |
+          Payload Section              +
|                                       |
~                                       ~
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
```
Kích thước:

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Type Code</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">X len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">NS len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">NS Enc len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">NS Dec len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">PQ key len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">pl len</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">96+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">64+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">--</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">pl</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM512_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">912+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">880+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">800+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">800</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">pl</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM768_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">6</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1296+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1360+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1184+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1184</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">pl</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM1024_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1680+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1648+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1568+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1568</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">pl</td>
</tr>
</table>
Lưu ý rằng payload phải chứa một khối DateTime, vì vậy kích thước payload tối thiểu là 7. Kích thước NS tối thiểu có thể được tính toán tương ứng.

#### Định dạng NSR

Thay đổi: Ratchet hiện tại có payload trống cho phần ChaCha đầu tiên, và payload ở phần thứ hai. Với ML-KEM, giờ đây có ba phần. Phần đầu tiên chứa ciphertext PQ được mã hóa. Phần thứ hai có payload trống. Phần thứ ba chứa payload.

Định dạng mã hóa:

```
+----+----+----+----+----+----+----+----+
|       Session Tag 8 bytes             |
+----+----+----+----+----+----+----+----+
|                                       |
+       Ephemeral Public Key            +
|            32 bytes                   |
+      Encoded with Elligator2          +
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+         ML-KEM ciphertext             +
|       ChaCha20 encrypted data         |
+   (see table below for length)        +
|                                       |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+     (MAC) for ciphertext Section      +
|              16 bytes                 |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+   (MAC) for key Section (no data)     +
|              16 bytes                 |
+----+----+----+----+----+----+----+----+
|                                       |
+          Payload Section              +
|       ChaCha20 encrypted data         |
~                                       ~
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+      (MAC) for Payload Section        +
|              16 bytes                 |
+----+----+----+----+----+----+----+----+
```
Định dạng đã giải mã:

```
Payload Part 1:

+----+----+----+----+----+----+----+----+
|                                       |
+         ML-KEM ciphertext             +
|                                       |
+   (see table below for length)        +
|                                       |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

Payload Part 2:

empty

Payload Part 3:

+----+----+----+----+----+----+----+----+
|                                       |
+          Payload Section              +
|                                       |
~                                       ~
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
```
Kích thước:

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Type Code</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Y len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">NSR len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">NSR Enc len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">NSR Dec len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">PQ CT len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">opt len</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">72+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">--</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">pl</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM512_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">856+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">816+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">768+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">768</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">pl</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM768_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">6</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1176+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1136+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1088+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1088</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">pl</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM1024_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1656+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1616+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1568+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1568</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">pl</td>
</tr>
</table>
Lưu ý rằng trong khi NSR thường sẽ có payload khác không, đặc tả ratchet [ECIES](/docs/specs/ecies/) không yêu cầu điều này, vì vậy kích thước payload tối thiểu là 0. Kích thước NSR tối thiểu có thể được tính toán tương ứng.

## Phân Tích Chi Phí Bổ Sung

### Trao đổi khóa

Tăng kích thước (byte):

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Pubkey (NS)</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Ciphertext (NSR)</th>
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
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM1024_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">+1584</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">+1584</td>
</tr>
</table>
Tốc độ:

Tốc độ theo báo cáo của [CLOUDFLARE](https://blog.cloudflare.com/pq-2024/):

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Relative speed</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">X25519 DH/keygen</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">baseline</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM512</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">2.25x faster</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM768</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1.5x faster</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM1024</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1x (same)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">XK</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4x DH (keygen + 3 DH)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM512_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4x DH + 2x PQ (keygen + enc/dec) = 4.9x DH = 22% slower</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM768_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4x DH + 2x PQ (keygen + enc/dec) = 5.3x DH = 32% slower</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM1024_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4x DH + 2x PQ (keygen + enc/dec) = 6x DH = 50% slower</td>
</tr>
</table>
## Phân tích bảo mật

Các danh mục bảo mật NIST được tóm tắt trong [NIST-PQ-END](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf) slide 10. Tiêu chí sơ bộ: Danh mục bảo mật NIST tối thiểu của chúng ta nên là 2 cho các giao thức hybrid và 3 cho PQ-only.

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
### Bắt tay

Đây đều là các giao thức hybrid. Có lẽ cần ưu tiên MLKEM768; MLKEM512 không đủ bảo mật.

Các danh mục bảo mật NIST [FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf):

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
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM1024</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
</tr>
</table>
## Tùy chọn Loại

Loại được khuyến nghị để hỗ trợ ban đầu, dựa trên danh mục bảo mật và độ dài khóa, là:

MLKEM768_X25519 (loại 6)

## Ghi chú Triển khai

### Hỗ trợ Thư viện

Các thư viện Bouncycastle, BoringSSL, và WolfSSL hiện đã hỗ trợ MLKEM. Hỗ trợ OpenSSL có trong phiên bản 3.5 phát hành ngày 8 tháng 4 năm 2025 [OPENSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/).

### Tunnel Chia Sẻ

Tự động phân loại/phát hiện nhiều giao thức trên cùng một tunnel có thể thực hiện dựa trên kiểm tra độ dài của thông điệp 1 (New Session Message). Lấy MLKEM512_X25519 làm ví dụ, thông điệp 1 có độ dài lớn hơn 816 byte so với giao thức ratchet hiện tại, và kích thước tối thiểu của thông điệp 1 (chỉ bao gồm payload DateTime) là 919 byte. Hầu hết kích thước thông điệp 1 với ratchet hiện tại có payload nhỏ hơn 816 byte, do đó chúng có thể được phân loại là non-hybrid ratchet. Các thông điệp lớn có lẽ là POST và khá hiếm.

Vì vậy chiến lược được khuyến nghị là:

- Nếu thông điệp 1 nhỏ hơn 919 byte, đó là giao thức ratchet hiện tại.
- Nếu thông điệp 1 lớn hơn hoặc bằng 919 byte, có thể đó là MLKEM512_X25519. Hãy thử MLKEM512_X25519 trước, và nếu thất bại, hãy thử giao thức ratchet hiện tại.

Điều này sẽ cho phép chúng ta hỗ trợ hiệu quả cả ratchet tiêu chuẩn và hybrid ratchet trên cùng một đích đến, giống như trước đây chúng ta đã hỗ trợ ElGamal và ratchet trên cùng một đích đến. Do đó, chúng ta có thể di chuyển sang giao thức hybrid MLKEM nhanh hơn nhiều so với việc không thể hỗ trợ song song hai giao thức cho cùng một đích đến, bởi vì chúng ta có thể thêm hỗ trợ MLKEM vào các đích đến hiện có.

Các kết hợp được hỗ trợ bắt buộc là:

- X25519 + MLKEM512
- X25519 + MLKEM768
- X25519 + MLKEM1024

Các kết hợp sau đây có thể phức tạp và KHÔNG bắt buộc phải được hỗ trợ, nhưng có thể được hỗ trợ tùy thuộc vào cách triển khai:

- Nhiều hơn một MLKEM
- ElG + một hoặc nhiều MLKEM
- X25519 + một hoặc nhiều MLKEM
- ElG + X25519 + một hoặc nhiều MLKEM

Không bắt buộc phải hỗ trợ nhiều thuật toán MLKEM (ví dụ, MLKEM512_X25519 và MLKEM_768_X25519) trên cùng một destination. Chỉ cần chọn một thuật toán. Phụ thuộc vào implementation.

Không bắt buộc phải hỗ trợ ba thuật toán (ví dụ X25519, MLKEM512_X25519, và MLKEM769_X25519) trên cùng một destination. Việc phân loại và chiến lược thử lại có thể quá phức tạp. Cấu hình và giao diện cấu hình có thể quá phức tạp. Phụ thuộc vào cách triển khai.

Không bắt buộc phải hỗ trợ các thuật toán ElGamal và hybrid trên cùng một đích đến. ElGamal đã lỗi thời, và chỉ ElGamal + hybrid (không có X25519) không có nhiều ý nghĩa. Ngoài ra, cả ElGamal và Hybrid New Session Messages đều có kích thước lớn, vì vậy các chiến lược phân loại thường phải thử cả hai phương thức giải mã, điều này sẽ không hiệu quả. Phụ thuộc vào việc triển khai.

Các client có thể sử dụng cùng một hoặc các X25519 static key khác nhau cho giao thức X25519 và giao thức hybrid trên cùng các tunnel, tùy thuộc vào cách triển khai.

### Bảo mật tiến về phía trước

Đặc tả ECIES cho phép Garlic Messages trong payload New Session Message, điều này cho phép giao hàng 0-RTT của gói streaming ban đầu, thường là HTTP GET, cùng với leaseset của client. Tuy nhiên, payload New Session Message không có tính bảo mật chuyển tiếp. Vì đề xuất này nhấn mạnh việc tăng cường tính bảo mật chuyển tiếp cho ratchet, các triển khai có thể hoặc nên hoãn việc bao gồm payload streaming, hoặc toàn bộ thông điệp streaming, cho đến Existing Session Message đầu tiên. Điều này sẽ phải đánh đổi khả năng giao hàng 0-RTT. Các chiến lược cũng có thể phụ thuộc vào loại lưu lượng hoặc loại tunnel, hoặc phụ thuộc vào GET so với POST, chẳng hạn. Tùy thuộc vào triển khai.

### Kích thước phiên mới

MLKEM sẽ tăng đáng kể kích thước của New Session Message, như đã mô tả ở trên. Điều này có thể giảm đáng kể độ tin cậy của việc gửi New Session Message qua tunnel, nơi chúng phải được phân mảnh thành nhiều tunnel message 1024 byte. Khả năng gửi thành công tỷ lệ thuận với số mũ của số lượng mảnh. Các implementation có thể sử dụng nhiều chiến lược khác nhau để giới hạn kích thước thông điệp, với chi phí là việc gửi 0-RTT. Phụ thuộc vào implementation.

## Tài liệu tham khảo

- [CLOUDFLARE](https://blog.cloudflare.com/pq-2024/)
- [COMMON](/docs/specs/common-structures/)
- [ECIES](/docs/specs/ecies/)
- [FIPS202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf)
- [FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)
- [FORUM](http://zzz.i2p/topics/3294)
- [NIST-PQ-END](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf)
- [NIST-VECTORS](https://csrc.nist.gov/projects/cryptographic-standards-and-guidelines/example-values)
- [Noise](https://noiseprotocol.org/noise.html)
- [Noise-Hybrid](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf)
- [OPENSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/)
- [PQ-WIREGUARD](https://eprint.iacr.org/2020/379.pdf)
- [Prop169](/proposals/169-pq-crypto/)
