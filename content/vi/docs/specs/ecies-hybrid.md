---
title: "ECIES-X25519-AEAD-Ratchet Hybrid Encryption (lược đồ mã hóa lai sử dụng ECIES với X25519, AEAD và ratchet)"
description: "Biến thể lai hậu lượng tử của giao thức mã hóa ECIES (lược đồ mã hóa tích hợp đường cong elliptic) sử dụng ML-KEM (cơ chế đóng gói khóa dựa trên lưới mô-đun)"
slug: "ecies-hybrid"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## Trạng thái triển khai

**Triển khai hiện tại:** - **i2pd (triển khai C++)**: Được triển khai đầy đủ trong phiên bản 2.58.0 (tháng 9 năm 2025) với hỗ trợ ML-KEM-512, ML-KEM-768 và ML-KEM-1024. Mã hóa đầu-cuối hậu lượng tử được bật theo mặc định khi có OpenSSL 3.5.0 hoặc mới hơn. - **Java I2P**: Chưa được triển khai tính đến phiên bản 0.9.67 / 2.10.0 (tháng 9 năm 2025). Đặc tả đã được phê duyệt và việc triển khai được lên kế hoạch cho các bản phát hành trong tương lai.

Bản đặc tả này mô tả các chức năng đã được phê duyệt, hiện đang được triển khai trong i2pd và được lên kế hoạch cho các triển khai Java I2P.

## Tổng quan

Đây là biến thể lai hậu lượng tử của giao thức ECIES-X25519-AEAD-Ratchet [ECIES](/docs/specs/ecies/). Nó đại diện cho giai đoạn đầu tiên của Đề xuất 169 [Prop169](/proposals/169-pq-crypto/) được phê duyệt. Xem đề xuất đó để biết các mục tiêu tổng thể, mô hình mối đe dọa, phân tích, các phương án thay thế và thông tin bổ sung.

Trạng thái Đề xuất 169: **Đang mở** (giai đoạn đầu đã được phê duyệt cho việc triển khai ECIES (lược đồ mã hóa tích hợp dựa trên đường cong elliptic) dạng lai).

Đặc tả này chỉ bao gồm những khác biệt so với [ECIES](/docs/specs/ecies/) tiêu chuẩn và phải được đọc cùng với đặc tả đó.

## Thiết kế

Chúng tôi sử dụng tiêu chuẩn NIST FIPS 203 [FIPS203](https://csrc.nist.gov/pubs/fips/203/final), được xây dựng dựa trên, nhưng không tương thích với, CRYSTALS-Kyber (các phiên bản 3.1, 3 và cũ hơn).

Bắt tay lai kết hợp Diffie-Hellman X25519 cổ điển với các cơ chế đóng gói khóa ML-KEM hậu lượng tử (KEM). Cách tiếp cận này dựa trên các khái niệm về bí mật chuyển tiếp lai được ghi nhận trong nghiên cứu PQNoise và các triển khai tương tự trong TLS 1.3, IKEv2 và WireGuard.

### Trao đổi khóa

Chúng tôi định nghĩa một cơ chế trao đổi khóa lai cho Ratchet (cơ chế ratchet trong mật mã). Post-quantum KEM (cơ chế đóng gói khóa hậu lượng tử) chỉ cung cấp các khóa tạm thời và không hỗ trợ trực tiếp các bắt tay dùng khóa tĩnh như Noise IK.

Chúng tôi định nghĩa ba biến thể ML-KEM (cơ chế bao bọc khóa dựa trên mạng tinh thể mô-đun, hậu lượng tử) như được quy định trong [FIPS203](https://csrc.nist.gov/pubs/fips/203/final), tổng cộng có 3 kiểu mã hóa mới. Các kiểu lai chỉ được định nghĩa khi kết hợp với X25519.

Các loại mã hóa mới là:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Security Level</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">ML-KEM Variant</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM512_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">NIST Category 1 (AES-128 equivalent)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ML-KEM-512</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM768_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">6</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">NIST Category 3 (AES-192 equivalent)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ML-KEM-768 (Recommended)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM1024_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">NIST Category 5 (AES-256 equivalent)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ML-KEM-1024</td>
    </tr>
  </tbody>
</table>
**Lưu ý:** MLKEM768_X25519 (Type 6) là biến thể mặc định được khuyến nghị, cung cấp bảo mật hậu lượng tử mạnh mẽ với độ quá tải hợp lý.

Chi phí phụ trội là đáng kể so với mã hóa chỉ dùng X25519 (thuật toán trao đổi khóa dùng đường cong elliptic). Kích thước điển hình của thông điệp 1 và 2 (đối với IK pattern, tức mẫu IK trong Noise Protocol) hiện vào khoảng 96-103 byte (trước phần payload bổ sung). Con số này sẽ tăng khoảng gấp 9-12 lần với MLKEM512 (thuật toán mã hóa khóa công khai kháng lượng tử ML‑KEM, cấu hình 512), gấp 13-16 lần với MLKEM768, và gấp 17-23 lần với MLKEM1024, tùy theo loại thông điệp.

### Cần mật mã mới

- **ML-KEM** (trước đây là CRYSTALS-Kyber) [FIPS203](https://csrc.nist.gov/pubs/fips/203/final) - Tiêu chuẩn cơ chế đóng gói khóa dựa trên lưới mô-đun
- **SHA3-256** (trước đây là Keccak-512) [FIPS202](https://csrc.nist.gov/pubs/fips/202/final) - Một phần của tiêu chuẩn SHA-3
- **SHAKE128 và SHAKE256** (các phần mở rộng XOF cho SHA3) [FIPS202](https://csrc.nist.gov/pubs/fips/202/final) - Các hàm đầu ra có thể mở rộng

Các vector kiểm thử cho SHA3-256, SHAKE128 và SHAKE256 (các hàm băm và hàm mở rộng đầu ra trong mật mã) có sẵn trong [NIST Cryptographic Algorithm Validation Program](https://csrc.nist.gov/Projects/cryptographic-algorithm-validation-program) (Chương trình Xác thực Thuật toán Mật mã của NIST).

**Hỗ trợ thư viện:** - Java: Thư viện Bouncycastle phiên bản 1.79 trở lên hỗ trợ tất cả các biến thể ML-KEM và các hàm SHA3/SHAKE - C++: OpenSSL 3.5 trở lên bao gồm hỗ trợ ML-KEM đầy đủ (phát hành tháng 4 năm 2025) - Go: Có nhiều thư viện có sẵn cho việc triển khai ML-KEM và SHA3

## Đặc tả

### Cấu trúc chung

Xem [Đặc tả Cấu trúc Chung](/docs/specs/common-structures/) để biết độ dài khóa và các định danh.

### Các mẫu bắt tay

Các quy trình bắt tay sử dụng các mẫu bắt tay của [Noise Protocol Framework](https://noiseprotocol.org/noise.html) (khuôn khổ giao thức Noise), với các thích ứng dành riêng cho I2P để cung cấp bảo mật hậu lượng tử lai.

Bảng ánh xạ ký tự sau đây được sử dụng:

- **e** = khóa tạm thời dùng một lần (X25519)
- **s** = khóa tĩnh
- **p** = tải trọng thông điệp (payload)
- **e1** = khóa PQ (hậu lượng tử) tạm thời dùng một lần, gửi từ Alice đến Bob (token đặc thù của I2P)
- **ekem1** = bản mã KEM (Key Encapsulation Mechanism – cơ chế đóng gói khóa), gửi từ Bob đến Alice (token đặc thù của I2P)

**Lưu ý quan trọng:** Các tên mẫu "IKhfs" và "IKhfselg2" cùng các token "e1" và "ekem1" là những điều chỉnh đặc thù của I2P, không được mô tả trong đặc tả chính thức của Noise Protocol Framework (khung giao thức Noise). Chúng là các định nghĩa tùy biến nhằm tích hợp ML-KEM (cơ chế đóng gói khóa dựa trên mạng tinh thể) vào mẫu IK của Noise. Mặc dù cách tiếp cận lai X25519 + ML-KEM được thừa nhận rộng rãi trong nghiên cứu về mật mã hậu lượng tử và trong các giao thức khác, phép đặt tên cụ thể được dùng ở đây là đặc thù của I2P.

Các sửa đổi sau đây đối với IK để đạt được bí mật chuyển tiếp lai được áp dụng:

```
Standard IK:              I2P IKhfs (Hybrid):
<- s                      <- s
...                       ...
-> e, es, s, ss, p        -> e, es, e1, s, ss, p
<- e, ee, se, p           <- e, ee, ekem1, se, p
<- p                      <- p
p ->                      p ->

Note: e1 and ekem1 are encrypted within ChaCha20-Poly1305 AEAD blocks.
Note: e1 (ML-KEM public key) and ekem1 (ML-KEM ciphertext) have different sizes.
```
Mẫu **e1** được định nghĩa như sau:

```
For Alice (sender):
(encap_key, decap_key) = PQ_KEYGEN()

// EncryptAndHash(encap_key)
ciphertext = ENCRYPT(k, n, encap_key, ad)
n++
MixHash(ciphertext)

For Bob (receiver):
// DecryptAndHash(ciphertext)
encap_key = DECRYPT(k, n, ciphertext, ad)
n++
MixHash(ciphertext)
```
Mẫu **ekem1** được định nghĩa như sau:

```
For Bob (receiver of encap_key):
(kem_ciphertext, kem_shared_key) = ENCAPS(encap_key)

// EncryptAndHash(kem_ciphertext)
ciphertext = ENCRYPT(k, n, kem_ciphertext, ad)
MixHash(ciphertext)

// MixKey
MixKey(kem_shared_key)

For Alice (sender of encap_key):
// DecryptAndHash(ciphertext)
kem_ciphertext = DECRYPT(k, n, ciphertext, ad)
MixHash(ciphertext)

// MixKey
kem_shared_key = DECAPS(kem_ciphertext, decap_key)
MixKey(kem_shared_key)
```
### Các thao tác ML-KEM (cơ chế đóng gói khóa dựa trên mô-đun lưới) được định nghĩa

Chúng tôi định nghĩa các hàm sau tương ứng với các khối xây dựng mật mã như được chỉ định trong [FIPS203](https://csrc.nist.gov/pubs/fips/203/final).

**(encap_key, decap_key) = PQ_KEYGEN()** : Alice tạo các encapsulation key (khóa bao gói) và decapsulation key (khóa giải bao gói). encapsulation key được gửi trong thông điệp NS. Kích thước khóa:   - ML-KEM-512: encap_key = 800 byte, decap_key = 1632 byte   - ML-KEM-768: encap_key = 1184 byte, decap_key = 2400 byte   - ML-KEM-1024: encap_key = 1568 byte, decap_key = 3168 byte

**(ciphertext, kem_shared_key) = ENCAPS(encap_key)** : Bob tính toán bản mã và khóa chia sẻ bằng khóa đóng gói (encapsulation key) nhận được trong thông điệp NS. Bản mã được gửi trong thông điệp NSR. Kích thước bản mã:   - ML-KEM-512: 768 byte   - ML-KEM-768: 1088 byte   - ML-KEM-1024: 1568 byte

kem_shared_key luôn là **32 byte** đối với cả ba biến thể.

**kem_shared_key = DECAPS(ciphertext, decap_key)** : Alice tính toán khóa dùng chung bằng cách sử dụng bản mã nhận được trong thông điệp NSR. kem_shared_key luôn có độ dài **32 byte**.

**Quan trọng:** Cả encap_key và bản mã đều được mã hóa bên trong các khối ChaCha20-Poly1305 trong các thông điệp bắt tay Noise số 1 và 2. Chúng sẽ được giải mã như một phần của quy trình bắt tay.

kem_shared_key được trộn vào chaining key (khóa xâu chuỗi) bằng MixKey(). Xem chi tiết bên dưới.

### KDF (hàm dẫn xuất khóa) cho bắt tay Noise

#### Tổng quan

Bắt tay lai kết hợp ECDH X25519 cổ điển với ML-KEM hậu lượng tử. Thông điệp đầu tiên, từ Alice tới Bob, chứa e1 (khóa bao gói ML-KEM) trước phần tải của thông điệp (payload). Thành phần này được coi như vật liệu khóa bổ sung; hãy gọi EncryptAndHash() trên nó (với vai trò Alice) hoặc DecryptAndHash() (với vai trò Bob). Sau đó xử lý phần tải của thông điệp như bình thường.

Thông điệp thứ hai, từ Bob gửi Alice, chứa ekem1 (bản mã ML-KEM) ở trước phần tải thông điệp. Phần này được coi là vật liệu khóa bổ sung; gọi EncryptAndHash() trên nó (với vai trò Bob) hoặc DecryptAndHash() (với vai trò Alice). Sau đó tính kem_shared_key và gọi MixKey(kem_shared_key). Tiếp theo, xử lý phần tải thông điệp như bình thường.

#### Các định danh của Noise (giao thức Noise)

Đây là các chuỗi khởi tạo của Noise (bộ khung giao thức bắt tay) (dành riêng cho I2P):

- `Noise_IKhfselg2_25519+MLKEM512_ChaChaPoly_SHA256`
- `Noise_IKhfselg2_25519+MLKEM768_ChaChaPoly_SHA256`
- `Noise_IKhfselg2_25519+MLKEM1024_ChaChaPoly_SHA256`

#### KDF (hàm dẫn xuất khóa) của Alice cho thông điệp NS

Sau mẫu thông điệp 'es' và trước mẫu thông điệp 's', hãy thêm:

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
#### Bob KDF (hàm dẫn xuất khóa) cho thông điệp NS

Sau mẫu thông điệp 'es' và trước mẫu thông điệp 's', hãy thêm:

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
#### KDF (hàm dẫn xuất khóa) của Bob cho thông điệp NSR

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
#### KDF (hàm dẫn xuất khóa) của Alice cho thông điệp NSR

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
#### Hàm dẫn xuất khóa (KDF) cho split()

Hàm split() vẫn không thay đổi so với đặc tả ECIES tiêu chuẩn. Sau khi hoàn tất bắt tay:

```
keydata = HKDF(chainKey, ZEROLEN, "", 64)
k_ab = keydata[0:31]
k_ba = keydata[32:63]
```
Đây là các khóa phiên hai chiều cho việc liên lạc đang diễn ra.

### Định dạng thông điệp

#### Định dạng NS (New Session - phiên mới)

**Thay đổi:** Ratchet (cơ chế cập nhật khóa tuần tự) hiện tại chứa khóa tĩnh trong phần ChaCha20-Poly1305 thứ nhất và payload (nội dung dữ liệu) trong phần thứ hai. Với ML-KEM, hiện có ba phần. Phần thứ nhất chứa khóa công khai ML-KEM được mã hóa (encap_key). Phần thứ hai chứa khóa tĩnh. Phần thứ ba chứa payload.

**Kích thước thông điệp:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type Code</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">X25519 len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">NS len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">NS Enc len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">NS Dec len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">PQ key len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">pl len</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">96+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">64+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">--</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM512_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">912+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">880+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">800+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">800</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM768_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">6</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1296+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1264+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1184+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1184</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM1024_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1680+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1648+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1568+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1568</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
    </tr>
  </tbody>
</table>
**Lưu ý:** Payload (dữ liệu tải) phải chứa một khối DateTime (tối thiểu 7 byte: 1 byte loại, 2 byte kích thước, 4 byte dấu thời gian). Kích thước NS tối thiểu có thể được tính toán tương ứng. Do đó, kích thước NS tối thiểu trên thực tế là 103 byte cho X25519 và đối với các biến thể lai thì nằm trong khoảng 919 đến 1687 byte.

Các mức tăng kích thước 816, 1200 và 1584 byte cho ba biến thể ML-KEM tương ứng với khóa công khai ML-KEM cộng thêm một Poly1305 MAC (mã xác thực thông điệp Poly1305) 16 byte dành cho mã hóa có xác thực.

#### Định dạng NSR (New Session Reply - Phản hồi phiên mới)

**Thay đổi:** Ratchet (cơ chế cập nhật khóa liên tục) hiện tại có payload (dữ liệu tải) trống ở phần ChaCha20-Poly1305 thứ nhất và payload ở phần thứ hai. Với ML-KEM, hiện có ba phần. Phần thứ nhất chứa bản mã ML-KEM đã được mã hóa. Phần thứ hai có payload trống. Phần thứ ba chứa payload.

**Kích thước thông điệp:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type Code</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">X25519 len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">NSR len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">NSR Enc len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">NSR Dec len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">PQ ct len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">pl len</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">72+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">40+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">--</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM512_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">856+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">824+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">784+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">768</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM768_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">6</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1176+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1144+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1104+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1088</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM1024_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1656+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1624+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1584+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1568</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
    </tr>
  </tbody>
</table>
Các mức tăng kích thước 784, 1104 và 1584 byte cho ba biến thể ML-KEM (cơ chế đóng gói khóa hậu lượng tử) phản ánh việc bao gồm bản mã ML-KEM cộng thêm một Poly1305 MAC 16 byte (mã xác thực thông điệp) cho mã hóa xác thực.

## Phân tích overhead (chi phí phụ trội)

### Trao đổi khóa

Chi phí bổ sung của mã hóa lai là đáng kể so với X25519-only:

- **MLKEM512_X25519**: Tăng khoảng 9-12x kích thước thông điệp bắt tay (NS: 9.5x, NSR: 11.9x)
- **MLKEM768_X25519**: Tăng khoảng 13-16x kích thước thông điệp bắt tay (NS: 13.5x, NSR: 16.3x)
- **MLKEM1024_X25519**: Tăng khoảng 17-23x kích thước thông điệp bắt tay (NS: 17.5x, NSR: 23x)

Phần phụ trội này là chấp nhận được vì những lợi ích bảo mật hậu lượng tử bổ sung. Các hệ số nhân thay đổi theo từng loại thông điệp vì kích thước cơ sở của thông điệp khác nhau (NS tối thiểu 96 byte, NSR tối thiểu 72 byte).

### Các cân nhắc về băng thông

Đối với việc thiết lập phiên điển hình với payload tối thiểu:
- Chỉ X25519: ~200 byte tổng cộng (NS + NSR)
- MLKEM512_X25519: ~1,800 byte tổng cộng (tăng 9 lần)
- MLKEM768_X25519: ~2,500 byte tổng cộng (tăng 12.5 lần)
- MLKEM1024_X25519: ~3,400 byte tổng cộng (tăng 17 lần)

Sau khi phiên được thiết lập, việc mã hóa thông điệp đang diễn ra sử dụng cùng định dạng truyền tải dữ liệu như các phiên chỉ dùng X25519, vì vậy không có chi phí bổ sung cho các thông điệp tiếp theo.

## Phân tích bảo mật

### Bắt tay

Hybrid handshake (bắt tay lai) cung cấp cả bảo mật cổ điển (X25519) và hậu lượng tử (ML-KEM). Kẻ tấn công phải phá vỡ **cả hai** ECDH cổ điển (Diffie–Hellman trên đường cong elliptic) và KEM hậu lượng tử (cơ chế đóng gói khóa) thì mới có thể xâm phạm các khóa phiên.

Điều này cung cấp: - **Bảo mật hiện tại**: X25519 ECDH cung cấp bảo vệ trước các kẻ tấn công cổ điển (mức bảo mật 128-bit) - **Bảo mật tương lai**: ML-KEM cung cấp bảo vệ trước các kẻ tấn công lượng tử (thay đổi theo bộ tham số) - **Bảo mật lai**: Cả hai đều phải bị phá vỡ để xâm phạm phiên (mức bảo mật = tối đa của cả hai thành phần)

### Các mức bảo mật

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Variant</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">NIST Category</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Classical Security</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">PQ Security</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Hybrid Security</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM512_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Category 1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128-bit (X25519)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">AES-128 equivalent</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128-bit</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM768_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Category 3</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128-bit (X25519)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">AES-192 equivalent</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128-bit</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM1024_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Category 5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128-bit (X25519)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">AES-256 equivalent</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128-bit</td>
    </tr>
  </tbody>
</table>
**Lưu ý:** Mức bảo mật lai bị giới hạn bởi thành phần yếu hơn trong hai thành phần. Trong mọi trường hợp, X25519 cung cấp mức bảo mật cổ điển 128-bit. Nếu một máy tính lượng tử có ý nghĩa đối với mật mã trở nên khả dụng, mức bảo mật sẽ phụ thuộc vào bộ tham số ML-KEM được chọn.

### Bảo mật chuyển tiếp

Cách tiếp cận lai duy trì các thuộc tính bí mật chuyển tiếp. Các khóa phiên được dẫn xuất từ cả hai trao đổi khóa tạm thời X25519 và ML-KEM. Nếu một trong hai khóa riêng tạm thời X25519 hoặc ML-KEM bị hủy sau khi bắt tay, các phiên trước đó không thể giải mã ngay cả khi các khóa tĩnh dài hạn bị xâm phạm.

IK pattern (mẫu bắt tay IK của Noise) cung cấp bảo mật chuyển tiếp đầy đủ (Noise Confidentiality level 5) sau khi thông điệp thứ hai (NSR) được gửi đi.

## Tùy chọn loại

Các triển khai nên hỗ trợ nhiều kiểu lai và đàm phán biến thể mạnh nhất mà cả hai bên đều hỗ trợ. Thứ tự ưu tiên nên là:

1. **MLKEM768_X25519** (Loại 6) - Mặc định được khuyến nghị, cân bằng tốt nhất giữa bảo mật và hiệu năng
2. **MLKEM1024_X25519** (Loại 7) - Mức bảo mật cao nhất cho các ứng dụng nhạy cảm
3. **MLKEM512_X25519** (Loại 5) - Mức bảo mật hậu lượng tử cơ bản cho các kịch bản bị hạn chế tài nguyên
4. **X25519** (Loại 4) - Chỉ cổ điển, dùng làm phương án dự phòng để tương thích

**Lý do:** MLKEM768_X25519 được khuyến nghị làm mặc định vì nó cung cấp mức bảo mật NIST Cấp 3 (tương đương AES-192), được coi là đủ để chống lại máy tính lượng tử đồng thời vẫn duy trì kích thước thông điệp hợp lý. MLKEM1024_X25519 cung cấp mức bảo mật cao hơn nhưng với overhead (chi phí phụ trội) tăng đáng kể.

## Ghi chú triển khai

### Hỗ trợ thư viện

- **Java**: Thư viện Bouncycastle phiên bản 1.79 (tháng 8 năm 2024) và các phiên bản mới hơn hỗ trợ tất cả các biến thể ML-KEM cần thiết và các hàm SHA3/SHAKE. Sử dụng `org.bouncycastle.pqc.crypto.mlkem.MLKEMEngine` để tuân thủ FIPS 203 (chuẩn liên bang về ML-KEM).
- **C++**: OpenSSL 3.5 (tháng 4 năm 2025) và các phiên bản mới hơn bao gồm hỗ trợ ML-KEM thông qua giao diện EVP_KEM. Đây là bản phát hành Hỗ trợ Dài hạn (Long Term Support) được duy trì đến tháng 4 năm 2030.
- **Go**: Có một số thư viện bên thứ ba dành cho ML-KEM và SHA3, bao gồm thư viện CIRCL của Cloudflare.

### Chiến lược di chuyển

Các triển khai nên: 1. Hỗ trợ cả biến thể chỉ X25519 và các biến thể ML-KEM lai trong giai đoạn chuyển tiếp 2. Ưu tiên biến thể lai khi cả hai nút đồng cấp đều hỗ trợ 3. Duy trì cơ chế quay lui về chỉ X25519 để bảo đảm tương thích ngược 4. Cân nhắc các ràng buộc băng thông mạng khi chọn biến thể mặc định

### Các tunnel dùng chung

Kích thước thông điệp tăng lên có thể ảnh hưởng đến việc sử dụng tunnel dùng chung. Các triển khai nên cân nhắc: - Gom lô các thủ tục bắt tay khi có thể để giảm chi phí phụ trội - Sử dụng thời gian hết hạn ngắn hơn cho các phiên lai để giảm trạng thái cần lưu trữ - Theo dõi mức sử dụng băng thông và điều chỉnh các tham số tương ứng - Triển khai kiểm soát tắc nghẽn cho lưu lượng thiết lập phiên

### Các cân nhắc về kích thước phiên mới

Do các thông điệp bắt tay có kích thước lớn hơn, các triển khai có thể cần: - Tăng kích thước bộ đệm cho thương lượng phiên (khuyến nghị tối thiểu 4KB) - Điều chỉnh giá trị thời gian chờ cho các kết nối chậm hơn (tính đến việc thông điệp lớn hơn khoảng ~3-17x) - Cân nhắc nén dữ liệu payload (dữ liệu tải) trong các thông điệp NS/NSR - Triển khai xử lý phân mảnh nếu được lớp truyền tải yêu cầu

### Kiểm thử và thẩm định

Các triển khai nên xác minh: - Tạo khóa ML-KEM, encapsulation (đóng gói), và decapsulation (giải đóng gói) chính xác - Tích hợp đúng kem_shared_key vào Noise KDF (hàm dẫn xuất khóa của giao thức Noise) - Việc tính toán kích thước thông điệp khớp với đặc tả - Khả năng tương tác với các triển khai I2P router khác - Hành vi dự phòng khi ML-KEM không khả dụng

Các vector kiểm thử cho các hoạt động ML-KEM có sẵn trong [Chương trình Xác thực Thuật toán Mật mã](https://csrc.nist.gov/Projects/cryptographic-algorithm-validation-program) của NIST.

## Khả năng tương thích phiên bản

**Đánh số phiên bản I2P:** I2P duy trì hai hệ đánh số phiên bản song song:
- **Router release version**: định dạng 2.x.x (ví dụ: 2.10.0 phát hành tháng 9 năm 2025)
- **API/protocol version**: định dạng 0.9.x (ví dụ: 0.9.67 tương ứng với router 2.10.0)

Đặc tả này tham chiếu tới phiên bản giao thức 0.9.67, tương ứng với bản phát hành router 2.10.0 trở lên.

**Ma trận tương thích:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Implementation</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Version</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">ML-KEM Support</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2pd</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.58.0+</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Full (512/768/1024)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deployed September 2025</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Java I2P</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.67 / 2.10.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Not yet</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Planned for future release</td>
    </tr>
  </tbody>
</table>
## Tài liệu tham khảo

- **[ECIES]**: [Đặc tả ECIES-X25519-AEAD-Ratchet](/docs/specs/ecies/)
- **[Prop169]**: [Đề xuất 169: Mật mã hậu lượng tử](/proposals/169-pq-crypto/)
- **[FIPS203]**: [NIST FIPS 203 - Tiêu chuẩn ML-KEM](https://csrc.nist.gov/pubs/fips/203/final)
- **[FIPS202]**: [NIST FIPS 202 - Tiêu chuẩn SHA-3](https://csrc.nist.gov/pubs/fips/202/final)
- **[Noise]**: [Khung giao thức Noise](https://noiseprotocol.org/noise.html)
- **[COMMON]**: [Đặc tả Cấu trúc chung](/docs/specs/common-structures/)
- **[RFC7539]**: [RFC 7539 - ChaCha20 và Poly1305](https://www.rfc-editor.org/rfc/rfc7539)
- **[RFC5869]**: [RFC 5869 - HKDF](https://www.rfc-editor.org/rfc/rfc5869)
- **[OpenSSL]**: [Tài liệu OpenSSL 3.5 ML-KEM](https://docs.openssl.org/3.5/man7/EVP_KEM-ML-KEM/)
- **[Bouncycastle]**: [Thư viện mật mã Java Bouncycastle](https://www.bouncycastle.org/)

---
