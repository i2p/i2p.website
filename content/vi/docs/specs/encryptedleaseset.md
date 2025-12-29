---
title: "LeaseSet được mã hóa"
description: "Định dạng LeaseSet có kiểm soát truy cập cho các Destinations (điểm đích trong I2P) riêng tư"
slug: "encryptedleaseset"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## Tổng quan

Tài liệu này đặc tả quy trình làm mù, mã hóa và giải mã đối với LeaseSet2 (LS2) được mã hóa. LeaseSets được mã hóa cung cấp cơ chế công bố có kiểm soát truy cập đối với thông tin dịch vụ ẩn trong cơ sở dữ liệu mạng I2P.

**Các tính năng chính:** - Luân chuyển khóa hằng ngày để đảm bảo bí mật chuyển tiếp - Ủy quyền phía khách hai tầng (dựa trên DH và dựa trên PSK) - Mã hóa ChaCha20 để có hiệu năng tốt trên thiết bị không có phần cứng AES - Chữ ký Red25519 cùng với kỹ thuật làm mù khóa - Tư cách thành viên phía khách bảo toàn quyền riêng tư

**Tài liệu liên quan:** - [Đặc tả Cấu trúc Chung](/docs/specs/common-structures/) - Cấu trúc LeaseSet (tập hợp tham số truy cập các tunnel vào) được mã hóa - [Đề xuất 123: Các mục netDB mới (cơ sở dữ liệu mạng của I2P)](/proposals/123-new-netdb-entries/) - Thông tin nền về các LeaseSet được mã hóa - [Tài liệu về Cơ sở dữ liệu Mạng](/docs/specs/common-structures/) - Cách sử dụng NetDB

---

## Lịch sử phiên bản và trạng thái triển khai

### Dòng thời gian phát triển giao thức

**Lưu ý quan trọng về đánh số phiên bản:**   I2P sử dụng hai hệ thống đánh số phiên bản riêng biệt: - **Phiên bản API/Router:** dòng 0.9.x (được dùng trong các đặc tả kỹ thuật) - **Phiên bản phát hành sản phẩm:** dòng 2.x.x (được dùng cho các bản phát hành công khai)

Các đặc tả kỹ thuật tham chiếu phiên bản API (ví dụ: 0.9.41), trong khi người dùng cuối thấy các phiên bản sản phẩm (ví dụ: 2.10.0).

### Các mốc triển khai

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Release Date</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Features</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.38</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">January 2019</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Floodfill support for standard LS2, offline keys</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.39</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">March 2019</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Full encrypted LS2 support, Red25519 (sig type&nbsp;11)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.40</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">May 2019</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Per-client authorization, encrypted LS2 with offline keys, B32 support</strong></td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.41</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">June 2019</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Protocol finalized as stable</strong></td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>2.10.0</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">September 2025</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Latest Java implementation (API version 0.9.61)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>i2pd 2.58.0</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">September 2025</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Full C++ implementation compatibility</td></tr>
  </tbody>
</table>
### Trạng thái hiện tại

- ✅ **Trạng thái giao thức:** Ổn định và không thay đổi kể từ tháng 6 năm 2019
- ✅ **Java I2P:** Được triển khai đầy đủ trong phiên bản 0.9.40+
- ✅ **i2pd (C++):** Được triển khai đầy đủ trong phiên bản 2.58.0+
- ✅ **Khả năng tương tác:** Hoàn chỉnh giữa các hiện thực
- ✅ **Triển khai mạng:** Sẵn sàng cho môi trường sản xuất với hơn 6 năm kinh nghiệm vận hành

---

## Các định nghĩa mật mã học

### Ký hiệu và quy ước

- `||` biểu thị phép nối
- `mod L` biểu thị phép giảm theo mô-đun bởi cấp (order) của Ed25519
- Tất cả các mảng byte ở thứ tự byte mạng (big-endian - byte cao trước) trừ khi có chỉ định khác
- Các giá trị little-endian (byte thấp trước) được ghi chú rõ ràng

### CSRNG(n) (bộ tạo số ngẫu nhiên an toàn mật mã)

**Bộ sinh số ngẫu nhiên an toàn mật mã**

Tạo ra `n` byte dữ liệu ngẫu nhiên an toàn mật mã, phù hợp cho việc tạo key material (dữ liệu dùng để sinh khóa).

**Yêu cầu bảo mật:** - Phải đảm bảo an toàn mật mã (phù hợp cho việc tạo khóa) - Phải an toàn khi các chuỗi byte liền kề bị lộ trên mạng - Các triển khai nên băm đầu ra từ các nguồn có thể không đáng tin cậy

**Tài liệu tham khảo:** - [Các cân nhắc bảo mật PRNG (bộ sinh số ngẫu nhiên giả)](http://projectbullrun.org/dual-ec/ext-rand.html) - [Thảo luận của các nhà phát triển Tor](https://lists.torproject.org/pipermail/tor-dev/2015-November/009954.html)

### H(p, d)

**Hàm băm SHA-256 với cá nhân hóa**

Hàm băm phân tách miền nhận:
- `p`: Chuỗi cá nhân hóa (cung cấp phân tách miền)
- `d`: Dữ liệu cần băm

**Triển khai:**

```
H(p, d) := SHA-256(p || d)
```
**Cách sử dụng:** Cung cấp domain separation (phân tách miền) trong mật mã để ngăn chặn các tấn công va chạm giữa các cách sử dụng SHA-256 trong các giao thức khác nhau.

### LUỒNG: ChaCha20

**Mật mã dòng: ChaCha20 như được đặc tả trong RFC 7539 Mục 2.4**

**Tham số:** - `S_KEY_LEN = 32` (khóa 256-bit) - `S_IV_LEN = 12` (nonce 96-bit) - Bộ đếm ban đầu: `1` (RFC 7539 cho phép 0 hoặc 1; khuyến nghị dùng 1 trong các ngữ cảnh AEAD (mã hóa xác thực kèm dữ liệu liên kết))

**MÃ HÓA(k, iv, plaintext)**

Mã hóa bản rõ bằng: - `k`: khóa mã hóa 32 byte - `iv`: nonce (giá trị chỉ dùng một lần) 12 byte (PHẢI là duy nhất cho mỗi khóa) - Trả về bản mã có cùng kích thước với bản rõ

**Thuộc tính bảo mật:** Toàn bộ bản mã phải không thể phân biệt được với dữ liệu ngẫu nhiên nếu khóa được giữ bí mật.

**DECRYPT(k, iv, ciphertext)**

Giải mã bản mã bằng: - `k`: khóa mã 32 byte - `iv`: nonce (giá trị chỉ dùng một lần) 12 byte - Trả về bản rõ

**Cơ sở thiết kế:** ChaCha20 được chọn thay vì AES vì: - Nhanh hơn AES 2.5-3x trên thiết bị không có tăng tốc phần cứng - Triển khai constant-time (thời gian hằng) dễ đạt được hơn - Bảo mật và tốc độ tương đương khi có AES-NI

**Tài liệu tham khảo:** - [RFC 7539](https://datatracker.ietf.org/doc/html/rfc7539) - ChaCha20 và Poly1305 cho các giao thức IETF

### SIG (chữ ký): Red25519

**Lược đồ chữ ký: Red25519 (SigType 11) với Key Blinding (làm mù khóa)**

Red25519 được xây dựng dựa trên các chữ ký Ed25519 trên đường cong Ed25519, sử dụng SHA-512 để băm, và hỗ trợ key blinding (kỹ thuật làm mù khóa) theo đặc tả trong ZCash RedDSA.

**Hàm:**

#### DERIVE_PUBLIC(privkey)

Trả về khóa công khai tương ứng với khóa riêng đã cho. - Sử dụng phép nhân vô hướng Ed25519 tiêu chuẩn với điểm cơ sở

#### SIGN(privkey, m)

Trả về chữ ký số được tạo bằng khóa riêng `privkey` cho thông điệp `m`.

**Khác biệt khi ký của Red25519 so với Ed25519:** 1. **Nonce (giá trị dùng một lần) ngẫu nhiên:** Sử dụng 80 byte dữ liệu ngẫu nhiên bổ sung

   ```
   T = CSRNG(80)  // 80 random bytes
   r = H*(T || publickey || message)
   ```
Điều này khiến mỗi chữ ký Red25519 (một loại chữ ký số dùng trong I2P) là duy nhất, ngay cả khi áp dụng cho cùng một thông điệp và khóa.

2. **Sinh khóa riêng:** Các khóa riêng Red25519 (một biến thể của Ed25519) được sinh từ các số ngẫu nhiên và được giảm theo `mod L`, thay vì sử dụng phương pháp bit-clamping của Ed25519 (thuật toán chữ ký số dựa trên đường cong elliptic).

#### VERIFY(pubkey, m, sig)

Xác minh chữ ký `sig` đối chiếu với khóa công khai `pubkey` và thông điệp `m`. - Trả về `true` nếu chữ ký hợp lệ, `false` nếu không - Việc xác minh giống hệt Ed25519

**Các thao tác làm mù khóa:**

#### GENERATE_ALPHA(data, secret)

Sinh alpha cho key blinding (kỹ thuật làm mù khóa). - `data`: Thường chứa khóa công khai dùng để ký và các loại chữ ký - `secret`: Bí mật bổ sung tùy chọn (độ dài bằng 0 nếu không dùng) - Kết quả có phân bố giống hệt như các khóa riêng Ed25519 (sau khi rút gọn modulo L)

#### BLIND_PRIVKEY(privkey, alpha)

Làm mù một khóa riêng bằng bí mật `alpha`. - Hiện thực: `blinded_privkey = (privkey + alpha) mod L` - Sử dụng số học vô hướng trên trường

#### BLIND_PUBKEY(pubkey, alpha)

Làm mù (blinding) một khóa công khai bằng bí mật `alpha`. - Cách triển khai: `blinded_pubkey = pubkey + DERIVE_PUBLIC(alpha)` - Sử dụng phép cộng phần tử nhóm (điểm) trên đường cong

**Tính chất then chốt:**

```
BLIND_PUBKEY(pubkey, alpha) == DERIVE_PUBLIC(BLIND_PRIVKEY(privkey, alpha))
```
**Các cân nhắc về bảo mật:**

Trích từ Đặc tả Giao thức Zcash, Mục 5.4.6.1: Vì mục đích bảo mật, alpha phải có phân phối giống hệt như các khóa riêng đã bỏ mù. Điều này đảm bảo rằng "sự kết hợp giữa một khóa công khai được tái ngẫu nhiên hóa và các chữ ký bằng khóa đó không tiết lộ khóa mà từ đó nó được tái ngẫu nhiên hóa."

**Các loại chữ ký được hỗ trợ:** - **Loại 7 (Ed25519):** Được hỗ trợ cho các destinations (đích trong I2P) hiện có (tương thích ngược) - **Loại 11 (Red25519):** Khuyến nghị cho các destinations mới sử dụng mã hóa - **Blinded keys (khóa che mờ):** Luôn sử dụng loại 11 (Red25519)

**Tài liệu tham khảo:** - [Đặc tả Giao thức ZCash](https://zips.z.cash/protocol/protocol.pdf) - Mục 5.4.6 RedDSA (thuật toán chữ ký số) - [Đặc tả I2P Red25519](/docs/specs/red25519-signature-scheme/)

### DH (trao đổi khóa Diffie–Hellman): X25519

**Diffie-Hellman trên đường cong elliptic: X25519**

Hệ thống thỏa thuận khóa công khai dựa trên Curve25519.

**Tham số:** - Khóa riêng: 32 byte - Khóa công khai: 32 byte - Đầu ra bí mật chung: 32 byte

**Chức năng:**

#### GENERATE_PRIVATE()

Tạo một khóa riêng 32 byte mới bằng cách sử dụng CSRNG (bộ sinh số ngẫu nhiên an toàn về mật mã).

#### DERIVE_PUBLIC(privkey)

Suy ra khóa công khai 32 byte từ khóa riêng đã cho. - Sử dụng phép nhân vô hướng trên Curve25519

#### DH(privkey, pubkey)

Thực hiện thỏa thuận khóa Diffie-Hellman. - `privkey`: Khóa riêng 32 byte cục bộ - `pubkey`: Khóa công khai 32 byte từ xa - Trả về: bí mật chung 32 byte

**Thuộc tính bảo mật:** - Giả định Diffie–Hellman tính toán trên Curve25519 - Bảo mật chuyển tiếp khi sử dụng khóa tạm thời - Yêu cầu triển khai thời gian hằng để ngăn chặn tấn công định thời

**Tài liệu tham khảo:** - [RFC 7748](https://datatracker.ietf.org/doc/html/rfc7748) - Các đường cong elliptic cho bảo mật

### HKDF (hàm dẫn xuất khóa dựa trên HMAC)

**Hàm dẫn xuất khóa dựa trên HMAC**

Trích xuất và mở rộng vật liệu khóa từ vật liệu khóa đầu vào.

**Tham số:** - `salt`: tối đa 32 byte (thường là 32 byte cho SHA-256) - `ikm`: vật liệu khóa đầu vào (độ dài bất kỳ, nên có entropy (độ ngẫu nhiên) tốt) - `info`: thông tin theo ngữ cảnh (phân tách miền) - `n`: độ dài đầu ra tính theo byte

**Hiện thực:**

Sử dụng HKDF như được đặc tả trong RFC 5869 với: - **Hàm băm:** SHA-256 - **HMAC:** Như được đặc tả trong RFC 2104 - **Độ dài muối:** Tối đa 32 byte (HashLen đối với SHA-256)

**Mẫu sử dụng:**

```
keys = HKDF(salt, ikm, info, n)
```
**Domain Separation (phân tách miền):** Tham số `info` cung cấp sự phân tách miền ở cấp mật mã giữa các lần sử dụng HKDF khác nhau trong giao thức.

**Các giá trị thông tin đã xác minh:** - `"ELS2_L1K"` - mã hóa lớp 1 (bên ngoài) - `"ELS2_L2K"` - mã hóa lớp 2 (bên trong) - `"ELS2_XCA"` - ủy quyền máy khách DH (Diffie–Hellman) - `"ELS2PSKA"` - ủy quyền máy khách PSK (khóa chia sẻ trước) - `"i2pblinding1"` - tạo Alpha

**Tài liệu tham khảo:** - [RFC 5869](https://datatracker.ietf.org/doc/html/rfc5869) - Đặc tả HKDF - [RFC 2104](https://datatracker.ietf.org/doc/html/rfc2104) - Đặc tả HMAC

---

## Đặc tả định dạng

LS2 được mã hóa bao gồm ba lớp lồng nhau:

1. **Lớp 0 (Bên ngoài):** Thông tin bản rõ để lưu trữ và truy xuất
2. **Lớp 1 (Ở giữa):** Dữ liệu xác thực máy khách (được mã hóa)
3. **Lớp 2 (Bên trong):** Dữ liệu LeaseSet2 thực (được mã hóa)

**Cấu trúc tổng thể:**

```
Layer 0 data + Enc(layer 1 data + Enc(layer 2 data)) + Signature
```
**Quan trọng:** LS2 được mã hóa sử dụng blinded keys (khóa làm mù). Destination (đích I2P) không nằm trong header. Vị trí lưu trữ trên DHT (bảng băm phân tán) là `SHA-256(sig type || blinded public key)`, được xoay vòng hàng ngày.

### Lớp 0 (Ngoài) - Bản rõ

Lớp 0 KHÔNG sử dụng tiêu đề LS2 tiêu chuẩn. Nó có một định dạng tùy chỉnh được tối ưu hóa cho blinded keys (khóa được làm mù).

**Cấu trúc:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Type</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1 byte</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Not in header, from DatabaseStore message field</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Blinded Public Key Sig Type</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big endian, always <code>0x000b</code> (Red25519 type 11)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Blinded Public Key</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Red25519 blinded public key</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Published Timestamp</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big endian, seconds since epoch (rolls over in 2106)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Expires</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big endian, offset from published in seconds (max 65,535 &asymp; 18.2 hours)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Flags</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Bit flags (see below)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">[Optional] Transient Key Data</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Variable</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Present if flag bit&nbsp;0 is set</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">lenOuterCiphertext</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big endian, length of outer ciphertext</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">outerCiphertext</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">lenOuterCiphertext</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Encrypted Layer&nbsp;1 data</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Signature</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Red25519 signature over all preceding data</td></tr>
  </tbody>
</table>
**Trường cờ (2 byte, bit 15-0):** - **Bit 0:** Chỉ báo khóa ngoại tuyến   - `0` = Không có khóa ngoại tuyến   - `1` = Có khóa ngoại tuyến (tiếp theo là dữ liệu khóa tạm thời) - **Các bit 1-15:** Dành riêng, phải bằng 0 để tương thích trong tương lai

**Dữ liệu khóa tạm thời (có mặt nếu bit cờ 0 = 1):**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Expires Timestamp</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big endian, seconds since epoch</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Transient Sig Type</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big endian, signature type</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Transient Signing Public Key</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Variable</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Length implied by signature type</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Signature</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Signed by blinded public key; covers expires timestamp, transient sig type, and transient public key</td></tr>
  </tbody>
</table>
**Xác minh chữ ký:** - **Không có khóa ngoại tuyến:** Xác minh bằng khóa công khai bị làm mù (blinded) - **Có khóa ngoại tuyến:** Xác minh bằng khóa công khai tạm thời

Chữ ký bao phủ tất cả dữ liệu từ Type đến outerCiphertext (bao gồm cả hai đầu).

### Lớp 1 (Trung gian) - Ủy quyền máy khách

**Giải mã:** Xem phần [Mã hóa Tầng 1](#layer-1-encryption).

**Cấu trúc:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Flags</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1 byte</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Authorization flags (see below)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">[Optional] Auth Data</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Variable</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Present based on flags</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">innerCiphertext</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Variable</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Encrypted Layer&nbsp;2 data (remainder)</td></tr>
  </tbody>
</table>
**Trường cờ (Flags) (1 byte, các bit 7-0):** - **Bit 0:** Chế độ ủy quyền   - `0` = Không ủy quyền theo từng máy khách (mọi người)   - `1` = Ủy quyền theo từng máy khách (phần auth theo sau) - **Bits 3-1:** Cơ chế xác thực (chỉ khi bit 0 = 1)   - `000` = Xác thực máy khách DH (Diffie-Hellman)   - `001` = Xác thực máy khách PSK (khóa chia sẻ trước)   - Các giá trị khác: dành riêng - **Bits 7-4:** Không sử dụng, phải bằng 0

**Dữ liệu ủy quyền máy khách DH (Diffie–Hellman) (cờ = 0x01, bit 3-1 = 000):**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ephemeralPublicKey</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Server's ephemeral X25519 public key</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">clients</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big endian, number of client entries</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">authClient[]</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">40 bytes each</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Array of client authorization entries</td></tr>
  </tbody>
</table>
**Bản ghi authClient (40 byte):** - `clientID_i`: 8 byte - `clientCookie_i`: 32 byte (authCookie được mã hóa)

**Dữ liệu ủy quyền máy khách PSK (cờ = 0x03, các bit 3-1 = 001):**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">authSalt</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Salt for PSK key derivation</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">clients</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big endian, number of client entries</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">authClient[]</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">40 bytes each</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Array of client authorization entries</td></tr>
  </tbody>
</table>
**Mục nhập authClient (40 byte):** - `clientID_i`: 8 byte - `clientCookie_i`: 32 byte (authCookie được mã hóa)

### Lớp 2 (Bên trong) - Dữ liệu LeaseSet

**Giải mã:** Xem phần [Mã hóa Tầng 2](#layer-2-encryption).

**Cấu trúc:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Type</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1 byte</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>3</code> (LS2) or <code>7</code> (Meta LS2)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Data</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Variable</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Complete LeaseSet2 or MetaLeaseSet2</td></tr>
  </tbody>
</table>
Lớp bên trong chứa đầy đủ cấu trúc LeaseSet2, bao gồm: - tiêu đề LS2 - thông tin Lease (bản ghi tunnel) - chữ ký LS2

**Yêu cầu xác minh:** Sau khi giải mã, các triển khai phải xác minh: 1. Dấu thời gian bên trong khớp với dấu thời gian được công bố bên ngoài 2. Thời điểm hết hạn bên trong khớp với thời điểm hết hạn bên ngoài 3. LS2 signature (chữ ký LS2) hợp lệ 4. Dữ liệu Lease được định dạng đúng

**Tham khảo:** - [Đặc tả Cấu trúc Chung](/docs/specs/common-structures/) - Chi tiết về định dạng LeaseSet2

---

## Dẫn xuất khóa Blinding (làm mù)

### Tổng quan

I2P sử dụng một lược đồ làm mù khóa dạng cộng dựa trên Ed25519 và ZCash RedDSA. Các khóa đã làm mù được xoay vòng hàng ngày (lúc nửa đêm UTC) nhằm đảm bảo bí mật chuyển tiếp.

**Lý do thiết kế:**

I2P đã chọn một cách rõ ràng KHÔNG sử dụng cách tiếp cận trong Phụ lục A.2 của tài liệu rend-spec-v3.txt của Tor. Theo đặc tả:

> "Chúng tôi không sử dụng phụ lục A.2 của rend-spec-v3.txt của Tor, vốn có các mục tiêu thiết kế tương tự, vì các khóa công khai bị làm mù của nó có thể không thuộc nhóm con bậc nguyên tố, với những hệ quả về bảo mật chưa rõ."

Cơ chế additive blinding (kỹ thuật làm mù cộng tính) của I2P đảm bảo rằng các khóa đã được làm mù vẫn nằm trong nhóm con bậc nguyên tố của đường cong Ed25519.

### Các định nghĩa toán học

**Tham số Ed25519:** - `B`: điểm cơ sở (điểm sinh) Ed25519 = `2^255 - 19` - `L`: bậc Ed25519 = `2^252 + 27742317777372353535851937790883648493`

**Các biến chính:** - `A`: khóa công khai dùng để ký 32 byte không mù hóa (trong Destination) - `a`: khóa riêng dùng để ký 32 byte không mù hóa - `A'`: khóa công khai dùng để ký 32 byte đã mù hóa (dùng trong LeaseSet được mã hóa) - `a'`: khóa riêng dùng để ký 32 byte đã mù hóa - `alpha`: hệ số mù hóa 32 byte (bí mật)

**Các hàm trợ giúp:**

#### LEOS2IP(x)

"Chuyển chuỗi Octet (chuỗi byte) little-endian (thứ tự byte thấp trước) thành số nguyên"

Chuyển đổi một mảng byte từ little-endian (thứ tự byte thấp trước) sang biểu diễn số nguyên.

#### H*(x)

"Băm và Rút gọn"

```
H*(x) = (LEOS2IP(SHA512(x))) mod L
```
Cùng phép toán như trong quá trình tạo khóa Ed25519 (chuẩn chữ ký số dựa trên đường cong Edwards 25519).

### Thế hệ Alpha

**Xoay vòng hàng ngày:** Một alpha mới và các blinded keys (khóa làm mù) mới PHẢI được tạo mỗi ngày vào lúc nửa đêm UTC (00:00:00 UTC).

**Thuật toán GENERATE_ALPHA(destination, date, secret):**

```python
# Input parameters
A = destination's signing public key (32 bytes)
stA = signature type of A (2 bytes, big endian)
     # 0x0007 for Ed25519 or 0x000b for Red25519
stA' = signature type of blinded key A' (2 bytes, big endian) 
     # Always 0x000b (Red25519)
datestring = "YYYYMMDD" (8 bytes ASCII from current UTC date)
secret = optional UTF-8 encoded string (zero-length if not used)

# Computation
keydata = A || stA || stA'  # 36 bytes total
seed = HKDF(
    salt=H("I2PGenerateAlpha", keydata),
    ikm=datestring || secret,
    info="i2pblinding1",
    n=64
)

# Treat seed as 64-byte little-endian integer and reduce
alpha = seed mod L
```
**Các tham số đã được xác minh:** - Cá nhân hóa (personalization) của salt: `"I2PGenerateAlpha"` - Tham số info của HKDF: `"i2pblinding1"` - Đầu ra: 64 byte trước khi rút gọn - Phân bố Alpha: Phân bố giống hệt như các khóa riêng Ed25519 sau `mod L`

### Làm mù khóa riêng

**Thuật toán BLIND_PRIVKEY(a, alpha):**

Đối với chủ sở hữu destination (đích) khi xuất bản LeaseSet đã được mã hóa:

```python
# For Ed25519 private key (type 7)
if sigtype == 7:
    seed = destination's signing private key (32 bytes)
    a = left_half(SHA512(seed))  # 32 bytes
    a = clamp(a)  # Ed25519 clamping
    
# For Red25519 private key (type 11)
elif sigtype == 11:
    a = destination's signing private key (32 bytes)
    # No clamping for Red25519

# Additive blinding using scalar arithmetic
blinded_privkey = a' = (a + alpha) mod L

# Derive blinded public key
blinded_pubkey = A' = DERIVE_PUBLIC(a')
```
**Tối quan trọng:** Phép rút gọn `mod L` là bắt buộc để duy trì mối quan hệ đại số đúng đắn giữa khóa bí mật và khóa công khai.

### Làm mù khóa công khai

**Thuật toán BLIND_PUBKEY(A, alpha):**

Đối với các ứng dụng khách truy xuất và xác minh LeaseSet được mã hóa:

```python
alpha = GENERATE_ALPHA(destination, date, secret)
A = destination's signing public key (32 bytes)

# Additive blinding using group elements (curve points)
blinded_pubkey = A' = A + DERIVE_PUBLIC(alpha)
```
**Tương đương toán học:**

Cả hai phương pháp cho ra kết quả giống hệt nhau:

```
BLIND_PUBKEY(A, alpha) == DERIVE_PUBLIC(BLIND_PRIVKEY(a, alpha))
```
Điều này là do:

```
A' = A + [alpha]B
   = [a]B + [alpha]B
   = [a + alpha]B  (group operation)
   = DERIVE_PUBLIC(a + alpha mod L)
```
### Ký số với Blinded Keys (khóa mù)

**Ký LeaseSet Unblinded (không mù):**

LeaseSet unblinded (không làm mù) (được gửi trực tiếp cho các client đã xác thực) được ký bằng: - Chữ ký Ed25519 chuẩn (type 7) hoặc Red25519 (type 11) - Khóa riêng dùng để ký unblinded - Được xác minh bằng khóa công khai unblinded

**Với các khóa ngoại tuyến:** - Được ký bằng khóa riêng tạm thời unblinded (không bị làm mù) - Được xác minh bằng khóa công khai tạm thời unblinded - Cả hai phải là loại 7 hoặc 11

**Ký số cho LeaseSet được mã hóa:**

Phần bên ngoài của LeaseSet được mã hóa sử dụng chữ ký Red25519 với các khóa được làm mù.

**Thuật toán ký số Red25519:**

```python
# Generate per-signature random nonce
T = CSRNG(80)  # 80 random bytes

# Calculate r (differs from Ed25519)
r = H*(T || blinded_pubkey || message)

# Rest is same as Ed25519
R = [r]B
S = (r + H(R || A' || message) * a') mod L
signature = R || S  # 64 bytes total
```
**Những khác biệt chính so với Ed25519:** 1. Sử dụng 80 byte dữ liệu ngẫu nhiên `T` (không phải băm của khóa riêng) 2. Sử dụng trực tiếp giá trị khóa công khai (không phải băm của khóa riêng) 3. Mỗi chữ ký đều là duy nhất ngay cả với cùng một thông điệp và cùng một khóa

**Xác minh:**

Giống như Ed25519:

```python
# Parse signature
R = signature[0:32]
S = signature[32:64]

# Verify equation: [S]B = R + [H(R || A' || message)]A'
return [S]B == R + [H(R || A' || message)]A'
```
### Các cân nhắc bảo mật

**Phân phối Alpha:**

Vì lý do bảo mật, alpha phải có cùng phân phối như các khóa riêng không bị làm mù. Khi blinding (kỹ thuật làm mù) Ed25519 (loại 7) sang Red25519 (loại 11), các phân phối khác nhau đôi chút.

**Khuyến nghị:** Sử dụng Red25519 (loại 11) cho cả khóa không bị làm mù và khóa bị làm mù để đáp ứng yêu cầu của ZCash: "sự kết hợp giữa một khóa công khai được tái ngẫu nhiên hóa và các chữ ký được tạo bằng khóa đó không tiết lộ khóa mà từ đó khóa công khai đã được tái ngẫu nhiên hóa."

**Hỗ trợ Type 7:** Ed25519 được hỗ trợ để tương thích ngược với các điểm đích hiện có, nhưng Type 11 được khuyến nghị cho các điểm đích được mã hóa mới.

**Lợi ích của xoay vòng hàng ngày:** - Bí mật chuyển tiếp: Việc lộ khóa đã làm mù của hôm nay không làm lộ khóa của ngày hôm qua - Không thể liên kết: Xoay vòng hàng ngày ngăn chặn việc theo dõi dài hạn qua DHT - Phân tách khóa: Dùng các khóa khác nhau cho các khoảng thời gian khác nhau

**Tài liệu tham khảo:** - [Đặc tả giao thức ZCash](https://zips.z.cash/protocol/protocol.pdf) - Mục 5.4.6.1 - [Thảo luận về Key Blinding (kỹ thuật làm mù khóa) của Tor](https://lists.torproject.org/pipermail/tor-dev/2013-December/005943.html) - [Ticket Tor #8106](https://trac.torproject.org/projects/tor/ticket/8106)

---

## Mã hóa và xử lý

### Dẫn xuất Subcredential (chứng thực phụ)

Trước khi mã hóa, chúng tôi dẫn xuất một credential (thông tin xác thực) và một subcredential (thông tin xác thực phụ) để ràng buộc các tầng được mã hóa với việc biết khóa công khai dùng để ký của Destination (đích trong I2P).

**Mục tiêu:** Đảm bảo chỉ những người biết khóa công khai dùng để ký của Destination (định danh đích trong I2P) mới có thể giải mã LeaseSet được mã hóa. Không cần Destination đầy đủ.

#### Tính toán thông tin xác thực

```python
A = destination's signing public key (32 bytes)
stA = signature type of A (2 bytes big endian)
     # 0x0007 for Ed25519 or 0x000b for Red25519
stA' = signature type of blinded key A' (2 bytes big endian)
     # Always 0x000b (Red25519)

keydata = A || stA || stA'  # 36 bytes

credential = H("credential", keydata)  # 32 bytes
```
**Phân tách miền:** Chuỗi cá nhân hóa "credential" đảm bảo giá trị băm này không va chạm với bất kỳ khóa tra cứu DHT (bảng băm phân tán) nào hoặc các mục đích sử dụng khác trong giao thức.

#### Tính toán Subcredential (thông tin xác thực phụ)

```python
blindedPublicKey = A' (32 bytes, from blinding process)

subcredential = H("subcredential", credential || blindedPublicKey)  # 32 bytes
```
**Mục đích:** Thông tin xác thực con ràng buộc LeaseSet được mã hóa với: 1. Destination (đích) cụ thể (thông qua thông tin xác thực) 2. Khóa đã được làm mù cụ thể (thông qua blindedPublicKey) 3. Ngày cụ thể (thông qua việc xoay vòng hàng ngày của blindedPublicKey)

Điều này ngăn chặn các cuộc tấn công phát lại và khả năng liên kết qua nhiều ngày.

### Mã hóa tầng 1

**Ngữ cảnh:** Lớp 1 chứa dữ liệu ủy quyền của máy khách và được mã hóa bằng khóa được dẫn xuất từ subcredential (thông tin xác thực con).

#### Thuật toán mã hóa

```python
# Prepare input
outerInput = subcredential || publishedTimestamp
# publishedTimestamp: 4 bytes from Layer 0

# Generate random salt
outerSalt = CSRNG(32)  # 32 bytes

# Derive encryption key and IV
keys = HKDF(
    salt=outerSalt,
    ikm=outerInput,
    info="ELS2_L1K",  # Domain separation
    n=44  # 32 bytes key + 12 bytes IV
)

outerKey = keys[0:31]    # 32 bytes (indices 0-31 inclusive)
outerIV = keys[32:43]    # 12 bytes (indices 32-43 inclusive)

# Encrypt and prepend salt
outerPlaintext = [Layer 1 data]
outerCiphertext = outerSalt || ENCRYPT(outerKey, outerIV, outerPlaintext)
```
**Đầu ra:** `outerCiphertext` có độ dài `32 + len(outerPlaintext)` byte.

**Thuộc tính bảo mật:** - Salt đảm bảo các cặp khóa/IV (vector khởi tạo) là duy nhất ngay cả khi dùng cùng một subcredential (thông tin xác thực phụ) - Chuỗi ngữ cảnh `"ELS2_L1K"` cung cấp phân tách miền - ChaCha20 cung cấp bảo mật ngữ nghĩa (bản mã không thể phân biệt với ngẫu nhiên)

#### Thuật toán giải mã

```python
# Parse salt from ciphertext
outerSalt = outerCiphertext[0:31]  # First 32 bytes

# Derive decryption key and IV (same process as encryption)
outerInput = subcredential || publishedTimestamp
keys = HKDF(
    salt=outerSalt,
    ikm=outerInput,
    info="ELS2_L1K",
    n=44
)

outerKey = keys[0:31]    # 32 bytes
outerIV = keys[32:43]    # 12 bytes

# Decrypt (skip salt bytes)
outerPlaintext = DECRYPT(outerKey, outerIV, outerCiphertext[32:end])
```
**Xác minh:** Sau khi giải mã, hãy xác minh rằng cấu trúc của Lớp 1 (Layer 1) đúng định dạng trước khi tiếp tục sang Lớp 2 (Layer 2).

### Mã hóa Lớp 2

**Ngữ cảnh:** Lớp 2 chứa dữ liệu LeaseSet2 thực tế và được mã hóa bằng khóa được dẫn xuất từ authCookie (nếu bật xác thực theo từng máy khách) hoặc chuỗi rỗng (nếu không).

#### Thuật toán mã hóa

```python
# Determine authCookie based on authorization mode
if per_client_auth_enabled:
    authCookie = [32-byte cookie from client authorization process]
else:
    authCookie = b''  # Zero-length byte array

# Prepare input
innerInput = authCookie || subcredential || publishedTimestamp

# Generate random salt
innerSalt = CSRNG(32)  # 32 bytes

# Derive encryption key and IV
keys = HKDF(
    salt=innerSalt,
    ikm=innerInput,
    info="ELS2_L2K",  # Domain separation
    n=44  # 32 bytes key + 12 bytes IV
)

innerKey = keys[0:31]    # 32 bytes
innerIV = keys[32:43]    # 12 bytes

# Encrypt and prepend salt
innerPlaintext = [Layer 2 data: LS2 type byte + LeaseSet2 data]
innerCiphertext = innerSalt || ENCRYPT(innerKey, innerIV, innerPlaintext)
```
**Đầu ra:** `innerCiphertext` có độ dài `32 + len(innerPlaintext)` byte.

**Ràng buộc khóa:** - Nếu không có xác thực client: Chỉ ràng buộc với subcredential và timestamp - Nếu bật xác thực client: Ngoài ra còn ràng buộc với authCookie (khác nhau cho mỗi client được ủy quyền)

#### Thuật toán giải mã

```python
# Determine authCookie (same as encryption)
if per_client_auth_enabled:
    authCookie = [32-byte cookie from client authorization process]
else:
    authCookie = b''  # Zero-length byte array

# Parse salt from ciphertext
innerSalt = innerCiphertext[0:31]  # First 32 bytes

# Derive decryption key and IV
innerInput = authCookie || subcredential || publishedTimestamp
keys = HKDF(
    salt=innerSalt,
    ikm=innerInput,
    info="ELS2_L2K",
    n=44
)

innerKey = keys[0:31]    # 32 bytes
innerIV = keys[32:43]    # 12 bytes

# Decrypt (skip salt bytes)
innerPlaintext = DECRYPT(innerKey, innerIV, innerCiphertext[32:end])
```
**Xác minh:** Sau khi giải mã: 1. Xác minh byte loại LS2 hợp lệ (3 hoặc 7) 2. Phân tích cú pháp cấu trúc LeaseSet2 3. Xác minh dấu thời gian bên trong khớp với dấu thời gian được công bố bên ngoài 4. Xác minh thời gian hết hạn bên trong khớp với thời gian hết hạn bên ngoài 5. Xác minh chữ ký LeaseSet2

### Tóm tắt lớp mã hóa

```
┌─────────────────────────────────────────────────┐
│ Layer 0 (Plaintext)                             │
│ - Blinded public key                            │
│ - Timestamps                                    │
│ - Signature                                     │
│                                                 │
│  ┌─────────────────────────────────────────┐   │
│  │ Layer 1 (Encrypted with subcredential)  │   │
│  │ - Authorization flags                   │   │
│  │ - Client auth data (if enabled)         │   │
│  │                                          │   │
│  │  ┌────────────────────────────────┐     │   │
│  │  │ Layer 2 (Encrypted with        │     │   │
│  │  │          authCookie + subcred) │     │   │
│  │  │ - LeaseSet2 type               │     │   │
│  │  │ - LeaseSet2 data               │     │   │
│  │  │ - Leases                       │     │   │
│  │  │ - LS2 signature                │     │   │
│  │  └────────────────────────────────┘     │   │
│  └─────────────────────────────────────────┘   │
└─────────────────────────────────────────────────┘
```
**Quy trình giải mã:** 1. Xác minh chữ ký của Lớp 0 bằng khóa công khai được làm mù 2. Giải mã Lớp 1 bằng subcredential (thông tin xác thực phụ) 3. Xử lý dữ liệu ủy quyền (nếu có) để lấy authCookie 4. Giải mã Lớp 2 bằng authCookie và subcredential 5. Xác minh và phân tích cú pháp LeaseSet2

---

## Phân quyền theo từng máy khách

### Tổng quan

Khi bật ủy quyền theo từng máy khách, máy chủ duy trì danh sách các máy khách được ủy quyền. Mỗi máy khách có key material (dữ liệu khóa) cần được truyền an toàn qua kênh out-of-band (kênh riêng tách biệt khỏi kênh thông thường).

**Hai cơ chế ủy quyền:** 1. **Ủy quyền client DH (Diffie-Hellman):** Bảo mật hơn, sử dụng thỏa thuận khóa X25519 2. **Ủy quyền PSK (Pre-Shared Key — khóa chia sẻ trước):** Đơn giản hơn, sử dụng khóa đối xứng

**Thuộc tính bảo mật phổ biến:** - Tính riêng tư về tư cách thành viên của máy khách: Người quan sát chỉ thấy số lượng máy khách nhưng không thể nhận diện các máy khách cụ thể - Ẩn danh khi thêm/thu hồi máy khách: Không thể theo dõi thời điểm các máy khách cụ thể được thêm hoặc bị gỡ bỏ - Xác suất va chạm của định danh máy khách 8 byte: ~1 trên 18 tỷ tỷ (không đáng kể)

### Ủy quyền máy khách DH (Diffie-Hellman - thuật toán trao đổi khóa)

**Tổng quan:** Mỗi máy khách tạo một cặp khóa X25519 và gửi khóa công khai của mình tới máy chủ qua một kênh out-of-band (ngoài băng) bảo mật. Máy chủ sử dụng ephemeral DH (Diffie-Hellman tạm thời) để mã hóa một authCookie duy nhất cho từng máy khách.

#### Sinh khóa cho máy khách

```python
# Client generates keypair
csk_i = GENERATE_PRIVATE()  # 32-byte X25519 private key
cpk_i = DERIVE_PUBLIC(csk_i)  # 32-byte X25519 public key

# Client sends cpk_i to server via secure out-of-band channel
# Client KEEPS csk_i secret (never transmitted)
```
**Ưu điểm bảo mật:** Khóa riêng của máy khách không bao giờ rời khỏi thiết bị của họ. Kẻ tấn công chặn được việc truyền ngoài băng cũng không thể giải mã các LeaseSets được mã hóa trong tương lai nếu không bẻ gãy X25519 DH.

#### Xử lý phía máy chủ

```python
# Server generates new auth cookie and ephemeral keypair
authCookie = CSRNG(32)  # 32-byte cookie

esk = GENERATE_PRIVATE()  # 32-byte ephemeral private key
epk = DERIVE_PUBLIC(esk)  # 32-byte ephemeral public key

# For each authorized client i
for cpk_i in authorized_clients:
    # Perform DH key agreement
    sharedSecret = DH(esk, cpk_i)  # 32 bytes
    
    # Derive client-specific encryption key
    authInput = sharedSecret || cpk_i || subcredential || publishedTimestamp
    okm = HKDF(
        salt=epk,  # Ephemeral public key as salt
        ikm=authInput,
        info="ELS2_XCA",  # Domain separation
        n=52  # 32 key + 12 IV + 8 ID
    )
    
    # Extract components
    clientKey_i = okm[0:31]    # 32 bytes
    clientIV_i = okm[32:43]    # 12 bytes
    clientID_i = okm[44:51]    # 8 bytes
    
    # Encrypt authCookie for this client
    clientCookie_i = ENCRYPT(clientKey_i, clientIV_i, authCookie)
    
    # Store [clientID_i, clientCookie_i] entry in Layer 1
```
**Cấu trúc dữ liệu tầng 1:**

```
ephemeralPublicKey (32 bytes)
clients (2 bytes) = N
[clientID_1 (8 bytes) || clientCookie_1 (32 bytes)]
[clientID_2 (8 bytes) || clientCookie_2 (32 bytes)]
...
[clientID_N (8 bytes) || clientCookie_N (32 bytes)]
```
**Khuyến nghị cho máy chủ:** - Tạo cặp khóa tạm thời mới cho mỗi LeaseSet mã hóa được công bố - Ngẫu nhiên hóa thứ tự client để ngăn theo dõi dựa trên vị trí - Cân nhắc thêm các mục giả để che giấu số lượng client thực

#### Xử lý phía ứng dụng khách

```python
# Client has: csk_i (their private key), destination, date, secret
# Client receives: encrypted LeaseSet with epk in Layer 1

# Perform DH key agreement with server's ephemeral public key
sharedSecret = DH(csk_i, epk)  # 32 bytes

# Derive expected client identifier and decryption key
cpk_i = DERIVE_PUBLIC(csk_i)  # Client's own public key
authInput = sharedSecret || cpk_i || subcredential || publishedTimestamp

okm = HKDF(
    salt=epk,
    ikm=authInput,
    info="ELS2_XCA",
    n=52
)

clientKey_i = okm[0:31]    # 32 bytes
clientIV_i = okm[32:43]    # 12 bytes
clientID_i = okm[44:51]    # 8 bytes

# Search Layer 1 authorization data for clientID_i
for (clientID, clientCookie) in layer1_auth_entries:
    if clientID == clientID_i:
        # Found matching entry, decrypt authCookie
        authCookie = DECRYPT(clientKey_i, clientIV_i, clientCookie)
        # Use authCookie to decrypt Layer 2
        break
else:
    # No matching entry - client not authorized or revoked
    raise AuthorizationError("Client not authorized")
```
**Xử lý lỗi phía máy khách:** - Nếu không tìm thấy `clientID_i`: Máy khách đã bị thu hồi quyền hoặc chưa từng được cấp quyền - Nếu giải mã thất bại: Dữ liệu bị hỏng hoặc khóa sai (rất hiếm) - Máy khách nên định kỳ lấy lại để phát hiện việc thu hồi quyền

### Ủy quyền máy khách bằng PSK (khóa chia sẻ trước)

**Tổng quan:** Mỗi máy khách có một khóa đối xứng 32 byte được chia sẻ trước. Máy chủ mã hóa cùng một authCookie sử dụng PSK (khóa chia sẻ trước) của từng máy khách.

#### Sinh khóa

```python
# Option 1: Client generates key
psk_i = CSRNG(32)  # 32-byte pre-shared key
# Client sends psk_i to server via secure out-of-band channel

# Option 2: Server generates key
psk_i = CSRNG(32)  # 32-byte pre-shared key
# Server sends psk_i to one or more clients via secure out-of-band channel
```
**Lưu ý bảo mật:** Cùng một PSK (khóa chia sẻ trước) có thể được chia sẻ giữa nhiều máy khách nếu muốn (tạo cơ chế ủy quyền "nhóm").

#### Xử lý phía máy chủ

```python
# Server generates new auth cookie and salt
authCookie = CSRNG(32)  # 32-byte cookie
authSalt = CSRNG(32)     # 32-byte salt

# For each authorized client i
for psk_i in authorized_clients:
    # Derive client-specific encryption key
    authInput = psk_i || subcredential || publishedTimestamp
    
    okm = HKDF(
        salt=authSalt,
        ikm=authInput,
        info="ELS2PSKA",  # Domain separation
        n=52  # 32 key + 12 IV + 8 ID
    )
    
    # Extract components
    clientKey_i = okm[0:31]    # 32 bytes
    clientIV_i = okm[32:43]    # 12 bytes
    clientID_i = okm[44:51]    # 8 bytes
    
    # Encrypt authCookie for this client
    clientCookie_i = ENCRYPT(clientKey_i, clientIV_i, authCookie)
    
    # Store [clientID_i, clientCookie_i] entry in Layer 1
```
**Cấu trúc dữ liệu Lớp 1:**

```
authSalt (32 bytes)
clients (2 bytes) = N
[clientID_1 (8 bytes) || clientCookie_1 (32 bytes)]
[clientID_2 (8 bytes) || clientCookie_2 (32 bytes)]
...
[clientID_N (8 bytes) || clientCookie_N (32 bytes)]
```
#### Xử lý phía máy khách

```python
# Client has: psk_i (their pre-shared key), destination, date, secret
# Client receives: encrypted LeaseSet with authSalt in Layer 1

# Derive expected client identifier and decryption key
authInput = psk_i || subcredential || publishedTimestamp

okm = HKDF(
    salt=authSalt,
    ikm=authInput,
    info="ELS2PSKA",
    n=52
)

clientKey_i = okm[0:31]    # 32 bytes
clientIV_i = okm[32:43]    # 12 bytes
clientID_i = okm[44:51]    # 8 bytes

# Search Layer 1 authorization data for clientID_i
for (clientID, clientCookie) in layer1_auth_entries:
    if clientID == clientID_i:
        # Found matching entry, decrypt authCookie
        authCookie = DECRYPT(clientKey_i, clientIV_i, clientCookie)
        # Use authCookie to decrypt Layer 2
        break
else:
    # No matching entry - client not authorized or revoked
    raise AuthorizationError("Client not authorized")
```
### So sánh và khuyến nghị

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Feature</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">DH Authorization</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">PSK Authorization</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Key Exchange</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Asymmetric (X25519)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Symmetric (shared secret)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Security</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Higher (forward secrecy)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Lower (depends on PSK secrecy)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Client Privacy</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Private key never transmitted</td><td style="border:1px solid var(--color-border); padding:0.5rem;">PSK must be transmitted securely</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Performance</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">N+1 DH operations</td><td style="border:1px solid var(--color-border); padding:0.5rem;">No DH operations</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Key Sharing</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">One key per client</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Can share key among multiple clients</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Revocation Detection</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Adversary cannot tell when revoked</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Adversary can track revocation if PSK intercepted</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Use Case</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">High security requirements</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Performance-critical or group access</td></tr>
  </tbody>
</table>
**Khuyến nghị:** - **Sử dụng DH authorization** (ủy quyền dựa trên Diffie–Hellman) cho các ứng dụng bảo mật cao, nơi bí mật chuyển tiếp là quan trọng - **Sử dụng PSK authorization** (ủy quyền bằng khóa chia sẻ trước) khi hiệu năng là yếu tố then chốt hoặc khi quản lý các nhóm máy khách - **Không bao giờ tái sử dụng PSKs** giữa các dịch vụ khác nhau hoặc qua các khoảng thời gian - **Luôn sử dụng các kênh bảo mật** để phân phối khóa (ví dụ: Signal, OTR, PGP)

### Các cân nhắc bảo mật

**Quyền riêng tư về tư cách thành viên của ứng dụng khách:**

Cả hai cơ chế bảo vệ quyền riêng tư về tư cách thành viên của máy khách thông qua: 1. **Định danh máy khách được mã hóa:** clientID 8-byte được suy ra từ đầu ra HKDF 2. **Cookie không thể phân biệt:** Tất cả các giá trị clientCookie 32-byte trông như ngẫu nhiên 3. **Không có siêu dữ liệu riêng theo máy khách:** Không có cách nào để xác định mục nào thuộc về máy khách nào

Một người quan sát có thể thấy: - Số lượng máy khách được ủy quyền (từ trường `clients`) - Sự thay đổi trong số lượng máy khách theo thời gian

Một người quan sát KHÔNG thể thấy: - Những máy khách cụ thể nào được ủy quyền - Khi các máy khách cụ thể được thêm hoặc bị gỡ bỏ (nếu số lượng giữ nguyên) - Bất kỳ thông tin nhận dạng máy khách nào

**Khuyến nghị về ngẫu nhiên hóa:**

Máy chủ NÊN xáo trộn ngẫu nhiên thứ tự các máy khách mỗi lần máy chủ tạo một LeaseSet được mã hóa:

```python
import random

# Before serializing
auth_entries = [(clientID_i, clientCookie_i) for each client]
random.shuffle(auth_entries)
# Now serialize in randomized order
```
**Lợi ích:** - Ngăn máy khách biết vị trí của mình trong danh sách - Ngăn chặn các cuộc tấn công suy luận dựa trên thay đổi vị trí - Khiến việc thêm/thu hồi máy khách không thể phân biệt được

**Ẩn số lượng máy khách:**

Máy chủ CÓ THỂ chèn các mục giả ngẫu nhiên:

```python
# Add dummy entries
num_dummies = random.randint(0, max_dummies)
for _ in range(num_dummies):
    dummy_id = CSRNG(8)
    dummy_cookie = CSRNG(32)
    auth_entries.append((dummy_id, dummy_cookie))

# Randomize all entries (real + dummy)
random.shuffle(auth_entries)
```
**Chi phí:** Các mục giả làm tăng kích thước LeaseSet được mã hóa (40 byte mỗi mục).

**Xoay vòng AuthCookie (cookie xác thực):**

Máy chủ NÊN tạo một authCookie mới: - Mỗi lần một LeaseSet được mã hóa được công bố (thường là mỗi vài giờ) - Ngay sau khi hủy quyền truy cập của một máy khách - Theo lịch định kỳ (ví dụ: hàng ngày) ngay cả khi không có thay đổi nào ở phía máy khách

**Lợi ích:** - Giới hạn mức độ lộ lọt nếu authCookie bị xâm phạm - Đảm bảo các máy khách đã bị thu hồi quyền truy cập sẽ nhanh chóng mất quyền truy cập - Cung cấp bảo mật chuyển tiếp cho Lớp 2

---

## Định địa chỉ Base32 cho LeaseSets được mã hóa

### Tổng quan

Các địa chỉ base32 I2P truyền thống chỉ chứa băm của Destination (đích kết nối trong I2P) (32 byte → 52 ký tự). Điều này là chưa đủ đối với LeaseSets được mã hóa vì:

1. Các client cần **khóa công khai không làm mù (unblinded public key)** để dẫn xuất khóa công khai đã làm mù (blinded public key)
2. Các client cần **các loại chữ ký** (không làm mù và làm mù) để dẫn xuất khóa đúng cách
3. Chỉ riêng giá trị băm (hash) không cung cấp thông tin này

**Giải pháp:** Một định dạng base32 mới bao gồm khóa công khai và các loại chữ ký.

### Đặc tả định dạng địa chỉ

**Cấu trúc đã giải mã (35 byte):**

```
┌─────────────────────────────────────────────────────┐
│ Byte 0   │ Byte 1  │ Byte 2  │ Bytes 3-34          │
│ Flags    │ Unblind │ Blinded │ Public Key          │
│ (XOR)    │ SigType │ SigType │ (32 bytes)          │
│          │ (XOR)   │ (XOR)   │                     │
└─────────────────────────────────────────────────────┘
```
**3 byte đầu tiên (XOR với checksum):**

3 byte đầu tiên chứa siêu dữ liệu được XOR với các phần của checksum (tổng kiểm) CRC-32:

```python
# Data structure before XOR
flags = 0x00           # 1 byte (reserved for future use)
unblinded_sigtype = 0x07 or 0x0b  # 1 byte (7 or 11)
blinded_sigtype = 0x0b  # 1 byte (always 11)

# Compute CRC-32 checksum of public key
checksum = crc32(pubkey)  # 4-byte CRC-32 of bytes 3-34

# XOR first 3 bytes with parts of checksum
data[0] = flags XOR (checksum >> 24) & 0xFF
data[1] = unblinded_sigtype XOR (checksum >> 16) & 0xFF  
data[2] = blinded_sigtype XOR (checksum >> 8) & 0xFF

# Bytes 3-34 contain the unmodified 32-byte public key
data[3:34] = pubkey
```
**Thuộc tính checksum (mã kiểm tra):** - Sử dụng đa thức CRC-32 tiêu chuẩn - Tỉ lệ bỏ sót lỗi: ~1 trên 16 triệu - Hỗ trợ phát hiện lỗi do gõ sai địa chỉ - Không thể dùng làm xác thực (không an toàn về mặt mật mã)

**Định dạng được mã hóa:**

```
Base32Encode(35 bytes) || ".b32.i2p"
```
**Đặc điểm:** - Tổng số ký tự: 56 (35 byte × 8 bit ÷ 5 bit mỗi ký tự) - Hậu tố: ".b32.i2p" (giống như base32 truyền thống) - Tổng độ dài: 56 + 8 = 64 ký tự (không bao gồm ký tự kết thúc null)

**Mã hóa Base32:** - Bảng chữ cái: `abcdefghijklmnopqrstuvwxyz234567` (chuẩn RFC 4648) - 5 bit không sử dụng ở cuối PHẢI bằng 0 - Không phân biệt chữ hoa/thường (theo quy ước dùng chữ thường)

### Tạo địa chỉ

```python
import struct
from zlib import crc32
import base64

def generate_encrypted_b32_address(pubkey, unblinded_sigtype, blinded_sigtype):
    """
    Generate base32 address for encrypted LeaseSet.
    
    Args:
        pubkey: 32-byte public key (bytes)
        unblinded_sigtype: Unblinded signature type (7 or 11)
        blinded_sigtype: Blinded signature type (always 11)
    
    Returns:
        String address ending in .b32.i2p
    """
    # Verify inputs
    assert len(pubkey) == 32, "Public key must be 32 bytes"
    assert unblinded_sigtype in [7, 11], "Unblinded sigtype must be 7 or 11"
    assert blinded_sigtype == 11, "Blinded sigtype must be 11"
    
    # Compute CRC-32 of public key
    checksum = crc32(pubkey) & 0xFFFFFFFF  # Ensure 32-bit unsigned
    
    # Prepare metadata bytes
    flags = 0x00
    
    # XOR metadata with checksum parts
    byte0 = flags ^ ((checksum >> 24) & 0xFF)
    byte1 = unblinded_sigtype ^ ((checksum >> 16) & 0xFF)
    byte2 = blinded_sigtype ^ ((checksum >> 8) & 0xFF)
    
    # Construct 35-byte data
    data = bytes([byte0, byte1, byte2]) + pubkey
    
    # Base32 encode (standard alphabet)
    # Python's base64 module uses uppercase by default
    b32 = base64.b32encode(data).decode('ascii').lower().rstrip('=')
    
    # Construct full address
    address = b32 + ".b32.i2p"
    
    return address
```
### Phân tích cú pháp địa chỉ

```python
import struct
from zlib import crc32
import base64

def parse_encrypted_b32_address(address):
    """
    Parse base32 address for encrypted LeaseSet.
    
    Args:
        address: String address ending in .b32.i2p
    
    Returns:
        Tuple of (pubkey, unblinded_sigtype, blinded_sigtype)
    
    Raises:
        ValueError: If address is invalid or checksum fails
    """
    # Remove suffix
    if not address.endswith('.b32.i2p'):
        raise ValueError("Invalid address suffix")
    
    b32 = address[:-8]  # Remove ".b32.i2p"
    
    # Verify length (56 characters for 35 bytes)
    if len(b32) != 56:
        raise ValueError(f"Invalid length: {len(b32)} (expected 56)")
    
    # Base32 decode
    # Add padding if needed
    padding_needed = (8 - (len(b32) % 8)) % 8
    b32_padded = b32.upper() + '=' * padding_needed
    
    try:
        data = base64.b32decode(b32_padded)
    except Exception as e:
        raise ValueError(f"Invalid base32 encoding: {e}")
    
    # Verify decoded length
    if len(data) != 35:
        raise ValueError(f"Invalid decoded length: {len(data)} (expected 35)")
    
    # Extract public key
    pubkey = data[3:35]
    
    # Compute CRC-32 for verification
    checksum = crc32(pubkey) & 0xFFFFFFFF
    
    # Un-XOR metadata bytes
    flags = data[0] ^ ((checksum >> 24) & 0xFF)
    unblinded_sigtype = data[1] ^ ((checksum >> 16) & 0xFF)
    blinded_sigtype = data[2] ^ ((checksum >> 8) & 0xFF)
    
    # Verify expected values
    if flags != 0x00:
        raise ValueError(f"Invalid flags: {flags:#x} (expected 0x00)")
    
    if unblinded_sigtype not in [7, 11]:
        raise ValueError(f"Invalid unblinded sigtype: {unblinded_sigtype} (expected 7 or 11)")
    
    if blinded_sigtype != 11:
        raise ValueError(f"Invalid blinded sigtype: {blinded_sigtype} (expected 11)")
    
    return pubkey, unblinded_sigtype, blinded_sigtype
```
### So sánh với Base32 truyền thống

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Feature</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Traditional B32</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Encrypted LS2 B32</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Content</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">SHA-256 hash of Destination</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Public key + signature types</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Decoded Size</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">35 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Encoded Length</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">52 characters</td><td style="border:1px solid var(--color-border); padding:0.5rem;">56 characters</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Suffix</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">.b32.i2p</td><td style="border:1px solid var(--color-border); padding:0.5rem;">.b32.i2p</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Total Length</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">60 chars</td><td style="border:1px solid var(--color-border); padding:0.5rem;">64 chars</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Checksum</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">None</td><td style="border:1px solid var(--color-border); padding:0.5rem;">CRC-32 (XOR'd into first 3 bytes)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Use Case</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Regular destinations</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Encrypted LeaseSet destinations</td></tr>
  </tbody>
</table>
### Hạn chế sử dụng

**Sự không tương thích của BitTorrent:**

Các địa chỉ LS2 được mã hóa KHÔNG THỂ được sử dụng với các phản hồi announce dạng rút gọn của BitTorrent:

```
Compact announce reply format:
┌────────────────────────────┐
│ 32-byte destination hash   │  ← Only hash, no signature types
│ 2-byte port                │
└────────────────────────────┘
```
**Vấn đề:** Định dạng rút gọn chỉ chứa giá trị băm (32 bytes), không có chỗ cho các kiểu chữ ký hoặc thông tin khóa công khai.

**Giải pháp:** Hãy sử dụng các phản hồi announce đầy đủ hoặc các tracker dựa trên HTTP có hỗ trợ địa chỉ đầy đủ.

### Tích hợp sổ địa chỉ

Nếu một máy khách có Destination (địa chỉ đích trong I2P) đầy đủ trong sổ địa chỉ:

1. Lưu trữ Destination (địa chỉ đích) đầy đủ (bao gồm khóa công khai)
2. Hỗ trợ tra cứu ngược theo giá trị băm
3. Khi gặp LS2 được mã hóa, truy xuất khóa công khai từ sổ địa chỉ
4. Không cần định dạng base32 mới nếu Destination đầy đủ đã được biết

**Các định dạng sổ địa chỉ hỗ trợ LS2 được mã hóa:** - hosts.txt với các chuỗi destination (địa chỉ đích trong I2P) đầy đủ - các cơ sở dữ liệu SQLite với cột destination - các định dạng JSON/XML với dữ liệu destination đầy đủ

### Ví dụ hiện thực

**Ví dụ 1: Tạo địa chỉ**

```python
# Ed25519 destination example
pubkey = bytes.fromhex('a' * 64)  # 32-byte public key
unblinded_type = 7   # Ed25519
blinded_type = 11    # Red25519 (always)

address = generate_encrypted_b32_address(pubkey, unblinded_type, blinded_type)
print(f"Address: {address}")
# Output: 56 base32 characters + .b32.i2p
```
**Ví dụ 2: Phân tích cú pháp và kiểm tra tính hợp lệ**

```python
address = "abc...xyz.b32.i2p"  # 56 chars + suffix

try:
    pubkey, unblinded, blinded = parse_encrypted_b32_address(address)
    print(f"Public Key: {pubkey.hex()}")
    print(f"Unblinded SigType: {unblinded}")
    print(f"Blinded SigType: {blinded}")
except ValueError as e:
    print(f"Invalid address: {e}")
```
**Ví dụ 3: Chuyển đổi từ Destination (điểm đích trong I2P)**

```python
def destination_to_encrypted_b32(destination):
    """
    Convert full Destination to encrypted LS2 base32 address.
    
    Args:
        destination: I2P Destination object
    
    Returns:
        Base32 address string
    """
    # Extract public key and signature type from destination
    pubkey = destination.signing_public_key  # 32 bytes
    sigtype = destination.sig_type  # 7 or 11
    
    # Blinded type is always 11 (Red25519)
    blinded_type = 11
    
    # Generate address
    return generate_encrypted_b32_address(pubkey, sigtype, blinded_type)
```
### Các cân nhắc bảo mật

**Quyền riêng tư:** - Địa chỉ Base32 tiết lộ khóa công khai - Điều này là có chủ đích và là yêu cầu của giao thức - KHÔNG tiết lộ khóa riêng tư hay làm suy yếu bảo mật - Khóa công khai là thông tin công khai theo thiết kế

**Kháng va chạm:** - CRC-32 chỉ cung cấp 32 bit kháng va chạm - Không an toàn về mặt mật mã (chỉ dùng để phát hiện lỗi) - KHÔNG dựa vào checksum (tổng kiểm) để xác thực - Vẫn cần xác minh đích đến đầy đủ

**Xác thực địa chỉ:** - Luôn xác thực checksum trước khi sử dụng - Từ chối các địa chỉ có loại chữ ký không hợp lệ - Xác minh khóa công khai nằm trên đường cong (phụ thuộc vào triển khai)

**Tài liệu tham khảo:** - [Đề xuất 149: B32 cho Encrypted LS2](/proposals/149-b32-encrypted-ls2/) - [Đặc tả định địa chỉ B32](/docs/specs/b32-for-encrypted-leasesets/) - [Đặc tả đặt tên I2P](/docs/overview/naming/)

---

## Hỗ trợ khóa ngoại tuyến

### Tổng quan

Các khóa ngoại tuyến cho phép khóa ký chính luôn ở trạng thái ngoại tuyến (lưu trữ lạnh), trong khi một khóa ký tạm thời được dùng cho các hoạt động hằng ngày. Điều này tối quan trọng đối với các dịch vụ có mức độ bảo mật cao.

**Các yêu cầu cụ thể đối với LS2 (LeaseSet phiên bản 2) được mã hóa:** - Các khóa tạm thời phải được tạo ngoại tuyến - Khóa riêng được làm mù phải được tạo sẵn (mỗi ngày một khóa) - Cả khóa tạm thời và khóa được làm mù đều được phân phối theo lô - Chưa có định dạng tệp chuẩn được xác định (TODO trong đặc tả)

### Cấu trúc khóa ngoại tuyến

**Dữ liệu khóa tạm thời lớp 0 (khi bit cờ 0 = 1):**

```
┌───────────────────────────────────────────────────┐
│ Expires Timestamp       │ 4 bytes (seconds)       │
│ Transient Sig Type      │ 2 bytes (big endian)    │
│ Transient Signing Pubkey│ Variable (sigtype len)  │
│ Signature (by blinded)  │ 64 bytes (Red25519)     │
└───────────────────────────────────────────────────┘
```
**Phạm vi chữ ký:** Chữ ký trong khối khóa ngoại tuyến bao gồm: - Dấu thời gian hết hạn (4 byte) - Loại chữ ký tạm thời (2 byte)   - Khóa công khai ký tạm thời (biến độ dài)

Chữ ký này được xác minh bằng **blinded public key** (khóa công khai đã làm mù), chứng minh rằng thực thể nắm giữ blinded private key (khóa riêng đã làm mù) đã ủy quyền cho khóa tạm thời này.

### Quy trình sinh khóa

**Đối với LeaseSet được mã hóa với khóa ngoại tuyến:**

1. **Tạo cặp khóa tạm thời** (ngoại tuyến, trong lưu trữ lạnh):
   ```python
   # For each day in future
   for date in future_dates:
       # Generate daily transient keypair
       transient_privkey = generate_red25519_privkey()  # Type 11
       transient_pubkey = derive_public(transient_privkey)

       # Store for later delivery
       keys[date] = (transient_privkey, transient_pubkey)
   ```

2. **Generate daily blinded keypairs** (offline, in cold storage):
   ```python
# Với mỗi ngày    for date in future_dates:

       # Derive alpha for this date
       datestring = date.strftime("%Y%m%d")  # "YYYYMMDD"
       alpha = GENERATE_ALPHA(destination, datestring, secret)
       
       # Blind the signing private key
       a = destination_signing_privkey  # Type 7 or 11
       blinded_privkey = BLIND_PRIVKEY(a, alpha)  # Result is type 11
       blinded_pubkey = DERIVE_PUBLIC(blinded_privkey)
       
       # Store for later delivery
       blinded_keys[date] = (blinded_privkey, blinded_pubkey)
   ```

3. **Sign transient keys with blinded keys** (offline):
   ```python
for date in future_dates:

       transient_pubkey = keys[date][1]
       blinded_privkey = blinded_keys[date][0]
       
       # Create signature data
       expires = int((date + timedelta(days=1)).timestamp())
       sig_data = struct.pack('>I', expires)  # 4 bytes
       sig_data += struct.pack('>H', 11)     # Transient type (Red25519)
       sig_data += transient_pubkey          # 32 bytes
       
       # Sign with blinded private key
       signature = RED25519_SIGN(blinded_privkey, sig_data)
       
       # Package for delivery
       offline_sig_blocks[date] = {
           'expires': expires,
           'transient_type': 11,
           'transient_pubkey': transient_pubkey,
           'signature': signature
       }
   ```

4. **Package for delivery to router:**
   ```python
# Cho mỗi ngày    delivery_package[date] = {

       'transient_privkey': keys[date][0],
       'transient_pubkey': keys[date][1],
       'blinded_privkey': blinded_keys[date][0],
       'blinded_pubkey': blinded_keys[date][1],
       'offline_sig_block': offline_sig_blocks[date]
}

   ```

### Router Usage

**Daily Key Loading:**

```python
# Vào lúc nửa đêm UTC (hoặc trước khi xuất bản)

date = datetime.utcnow().date()

# Nạp các khóa của hôm nay

today_keys = load_delivery_package(date)

transient_privkey = today_keys['transient_privkey'] transient_pubkey = today_keys['transient_pubkey'] blinded_privkey = today_keys['blinded_privkey'] blinded_pubkey = today_keys['blinded_pubkey'] offline_sig_block = today_keys['offline_sig_block']

# Hãy dùng các khóa này cho LeaseSet được mã hóa hôm nay

```

**Publishing Process:**

```python
# 1. Tạo LeaseSet2 bên trong

inner_ls2 = create_leaseset2(

    destinations, leases, expires, 
    signing_key=transient_privkey  # Use transient key
)

# 2. Mã hóa Lớp 2

layer2_ciphertext = encrypt_layer2(inner_ls2, authCookie, subcredential, timestamp)

# 3. Tạo Lớp 1 với dữ liệu ủy quyền

layer1_plaintext = create_layer1(authorization_data, layer2_ciphertext)

# 4. Mã hóa lớp 1

layer1_ciphertext = encrypt_layer1(layer1_plaintext, subcredential, timestamp)

# 5. Tạo Lớp 0 với khối chữ ký ngoại tuyến

layer0 = create_layer0(

    blinded_pubkey,
    timestamp,
    expires,
    flags=0x0001,  # Bit 0 set (offline keys present)
    offline_sig_block=offline_sig_block,
    layer1_ciphertext=layer1_ciphertext
)

# 6. Ký Lớp 0 bằng khóa riêng tạm thời

signature = RED25519_SIGN(transient_privkey, layer0)

# 7. Thêm chữ ký và công bố

encrypted_leaseset = layer0 + signature publish_to_netdb(encrypted_leaseset)

```

### Security Considerations

**Tracking via Offline Signature Block:**

The offline signature block is in plaintext (Layer 0). An adversary scraping floodfills could:
- Track the same encrypted LeaseSet across multiple days
- Correlate encrypted LeaseSets even though blinded keys change daily

**Mitigation:** Generate new transient keys daily (in addition to blinded keys):

```python
# Tạo CẢ HAI khóa tạm thời mới và blinded keys (khóa mù hóa) mới mỗi ngày

for date in future_dates:

    # New transient keypair for this day
    transient_privkey = generate_red25519_privkey()
    transient_pubkey = derive_public(transient_privkey)
    
    # New blinded keypair for this day
    alpha = GENERATE_ALPHA(destination, datestring, secret)
    blinded_privkey = BLIND_PRIVKEY(signing_privkey, alpha)
    blinded_pubkey = DERIVE_PUBLIC(blinded_privkey)
    
    # Sign new transient key with new blinded key
    sig = RED25519_SIGN(blinded_privkey, transient_pubkey || metadata)
    
    # Now offline sig block changes daily
```

**Benefits:**
- Prevents tracking across days via offline signature block
- Provides same security as encrypted LS2 without offline keys
- Each day appears completely independent

**Cost:**
- More keys to generate and store
- More complex key management

### File Format (TODO)

**Current Status:** No standardized file format defined for batch key delivery.

**Requirements for Future Format:**

1. **Must support multiple dates:**
   - Batch delivery of 30+ days worth of keys
   - Clear date association for each key set

2. **Must include all necessary data:**
   - Transient private key
   - Transient public key
   - Blinded private key
   - Blinded public key
   - Pre-computed offline signature block
   - Expiration timestamps

3. **Should be tamper-evident:**
   - Checksums or signatures over entire file
   - Integrity verification before loading

4. **Should be encrypted:**
   - Keys are sensitive material
   - Encrypt file with router's key or passphrase

**Proposed Format Example (JSON, encrypted):**

```json
{   "version": 1,   "destination_hash": "base64...",   "keys": [

    {
      "date": "2025-10-15",
      "transient": {
        "type": 11,
        "privkey": "base64...",
        "pubkey": "base64..."
      },
      "blinded": {
        "privkey": "base64...",
        "pubkey": "base64..."
      },
      "offline_sig_block": {
        "expires": 1729123200,
        "signature": "base64..."
      }
    }
],   "signature": "base64..."  // Signature over entire structure }

```

### I2CP Protocol Enhancement (TODO)

**Current Status:** No I2CP protocol enhancement defined for offline keys with encrypted LeaseSet.

**Requirements:**

1. **Key delivery mechanism:**
   - Upload batch of keys from client to router
   - Acknowledgment of successful key loading

2. **Key expiration notification:**
   - Router notifies client when keys running low
   - Client can generate and upload new batch

3. **Key revocation:**
   - Emergency revocation of future keys if compromise suspected

**Proposed I2CP Messages:**

```
UPLOAD_OFFLINE_KEYS   - Lô dữ liệu khóa đã mã hóa   - Khoảng thời gian bao phủ

OFFLINE_KEY_STATUS   - Số ngày còn lại   - Ngày hết hạn khóa tiếp theo

REVOKE_OFFLINE_KEYS     - Khoảng thời gian cần thu hồi   - Các khóa mới để thay thế (tùy chọn)

```

### Implementation Status

**Java I2P:**
- ✅ Offline keys for standard LS2: Fully supported (since 0.9.38)
- ⚠️ Offline keys for encrypted LS2: Implemented (since 0.9.40)
- ❌ File format: Not standardized
- ❌ I2CP protocol: Not enhanced

**i2pd (C++):**
- ✅ Offline keys for standard LS2: Fully supported
- ✅ Offline keys for encrypted LS2: Fully supported (since 2.58.0)
- ❌ File format: Not standardized
- ❌ I2CP protocol: Not enhanced

**References:**
- [Offline Signatures Proposal](/proposals/123-new-netdb-entries/)
- [I2CP Specification](/docs/specs/i2cp/)

---

## Security Considerations

### Cryptographic Security

**Algorithm Selection:**

All cryptographic primitives are based on well-studied algorithms:
- **ChaCha20:** Modern stream cipher, constant-time, no timing attacks
- **SHA-256:** NIST-approved hash, 128-bit security level
- **HKDF:** RFC 5869 standard, proven security bounds
- **Ed25519/Red25519:** Curve25519-based, ~128-bit security level
- **X25519:** Diffie-Hellman over Curve25519, ~128-bit security level

**Key Sizes:**
- All symmetric keys: 256 bits (32 bytes)
- All public/private keys: 256 bits (32 bytes)
- All nonces/IVs: 96 bits (12 bytes)
- All signatures: 512 bits (64 bytes)

These sizes provide adequate security margins against current and near-future attacks.

### Forward Secrecy

**Daily Key Rotation:**

Encrypted LeaseSets rotate keys daily (UTC midnight):
- New blinded public/private key pair
- New storage location in DHT
- New encryption keys for both layers

**Benefits:**
- Compromising today's blinded key doesn't reveal yesterday's
- Limits exposure window to 24 hours
- Prevents long-term tracking via DHT

**Enhanced with Ephemeral Keys:**

DH client authorization uses ephemeral keys:
- Server generates new ephemeral DH keypair for each publication
- Compromising ephemeral key only affects that publication
- True forward secrecy even if long-term keys compromised

### Privacy Properties

**Destination Blinding:**

The blinded public key:
- Is unlinkable to the original destination (without knowing the secret)
- Changes daily, preventing long-term correlation
- Cannot be reversed to find the original public key

**Client Membership Privacy:**

Per-client authorization provides:
- **Anonymity:** No way to identify which clients are authorized
- **Untraceability:** Cannot track when specific clients added/revoked
- **Size obfuscation:** Can add dummy entries to hide true count

**DHT Privacy:**

Storage location rotates daily:
```
location = SHA-256(sig_type || blinded_public_key)

```

This prevents:
- Correlation across days via DHT lookups
- Long-term monitoring of service availability
- Traffic analysis of DHT queries

### Threat Model

**Adversary Capabilities:**

1. **Network Adversary:**
   - Can monitor all DHT traffic
   - Can observe encrypted LeaseSet publications
   - Cannot decrypt without proper keys

2. **Floodfill Adversary:**
   - Can store and analyze all encrypted LeaseSets
   - Can track publication patterns over time
   - Cannot decrypt Layer 1 or Layer 2
   - Can see client count (but not identities)

3. **Authorized Client Adversary:**
   - Can decrypt specific encrypted LeaseSets
   - Can access inner LeaseSet2 data
   - Cannot determine other clients' identities
   - Cannot decrypt past LeaseSets (with ephemeral keys)

**Out of Scope:**

- Malicious router implementations
- Compromised router host systems
- Side-channel attacks (timing, power analysis)
- Physical access to keys
- Social engineering attacks

### Attack Scenarios

**1. Offline Keys Tracking Attack:**

**Attack:** Adversary tracks encrypted LeaseSets via unchanging offline signature block.

**Mitigation:** Generate new transient keys daily (in addition to blinded keys).

**Status:** Documented recommendation, implementation-specific.

**2. Client Position Inference Attack:**

**Attack:** If client order is static, clients can infer their position and detect when other clients added/removed.

**Mitigation:** Randomize client order in authorization list for each publication.

**Status:** Documented recommendation in specification.

**3. Client Count Analysis Attack:**

**Attack:** Adversary monitors client count changes over time to infer service popularity or client churn.

**Mitigation:** Add random dummy entries to authorization list.

**Status:** Optional feature, deployment-specific trade-off (size vs. privacy).

**4. PSK Interception Attack:**

**Attack:** Adversary intercepts PSK during out-of-band exchange and can decrypt all future encrypted LeaseSets.

**Mitigation:** Use DH client authorization instead, or ensure secure key exchange (Signal, OTR, PGP).

**Status:** Known limitation of PSK approach, documented in specification.

**5. Timing Correlation Attack:**

**Attack:** Adversary correlates publication times across days to link encrypted LeaseSets.

**Mitigation:** Randomize publication times, use delayed publishing.

**Status:** Implementation-specific, not addressed in core specification.

**6. Long-term Secret Compromise:**

**Attack:** Adversary compromises the blinding secret and can compute all past and future blinded keys.

**Mitigation:** 
- Use optional secret parameter (not empty)
- Rotate secret periodically
- Use different secrets for different services

**Status:** Secret parameter is optional; using it is highly recommended.

### Operational Security

**Key Management:**

1. **Signing Private Key:**
   - Store offline in cold storage
   - Use only for generating blinded keys (batch process)
   - Never expose to online router

2. **Blinded Private Keys:**
   - Generate offline, deliver in batches
   - Rotate daily automatically
   - Delete after use (forward secrecy)

3. **Transient Private Keys (with offline keys):**
   - Generate offline, deliver in batches
   - Can be longer-lived (days/weeks)
   - Rotate regularly for enhanced privacy

4. **Client Authorization Keys:**
   - DH: Client private keys never leave client device
   - PSK: Use unique keys per client, secure exchange
   - Revoke immediately upon client removal

**Secret Management:**

The optional secret parameter in `GENERATE_ALPHA`:
- SHOULD be used for high-security services
- MUST be transmitted securely to authorized clients
- SHOULD be rotated periodically (e.g., monthly)
- CAN be different for different client groups

**Monitoring and Auditing:**

1. **Publication Monitoring:**
   - Verify encrypted LeaseSets published successfully
   - Monitor floodfill acceptance rates
   - Alert on publication failures

2. **Client Access Monitoring:**
   - Log client authorization attempts (without identifying clients)
   - Monitor for unusual patterns
   - Detect potential attacks early

3. **Key Rotation Auditing:**
   - Verify daily key rotation occurs
   - Check blinded key changes daily
   - Ensure old keys are deleted

### Implementation Security

**Constant-Time Operations:**

Implementations MUST use constant-time operations for:
- All scalar arithmetic (mod L operations)
- Private key comparisons
- Signature verification
- DH key agreement

**Memory Security:**

- Zero sensitive key material after use
- Use secure memory allocation for keys
- Prevent keys from being paged to disk
- Clear stack variables containing key material

**Random Number Generation:**

- Use cryptographically secure RNG (CSRNG)
- Properly seed RNG from OS entropy source
- Do not use predictable RNGs for key material
- Verify RNG output quality periodically

**Input Validation:**

- Validate all public keys are on the curve
- Check all signature types are supported
- Verify all lengths before parsing
- Reject malformed encrypted LeaseSets early

**Error Handling:**

- Do not leak information via error messages
- Use constant-time comparison for authentication
- Do not expose timing differences in decryption
- Log security-relevant events properly

### Recommendations

**For Service Operators:**

1. ✅ **Use Red25519 (type 11)** for new destinations
2. ✅ **Use DH client authorization** for high-security services
3. ✅ **Generate new transient keys daily** when using offline keys
4. ✅ **Use the optional secret parameter** in GENERATE_ALPHA
5. ✅ **Randomize client order** in authorization lists
6. ✅ **Monitor publication success** and investigate failures
7. ⚠️ **Consider dummy entries** to hide client count (size trade-off)

**For Client Implementers:**

1. ✅ **Validate blinded public keys** are on prime-order subgroup
2. ✅ **Verify all signatures** before trusting data
3. ✅ **Use constant-time operations** for cryptographic primitives
4. ✅ **Zero key material** immediately after use
5. ✅ **Implement proper error handling** without information leaks
6. ✅ **Support both Ed25519 and Red25519** destination types

**For Network Operators:**

1. ✅ **Accept encrypted LeaseSets** in floodfill routers
2. ✅ **Enforce reasonable size limits** to prevent abuse
3. ✅ **Monitor for anomalous patterns** (extremely large, frequent updates)
4. ⚠️ **Consider rate limiting** encrypted LeaseSet publications

---

## Implementation Notes

### Java I2P Implementation

**Repository:** https://github.com/i2p/i2p.i2p

**Key Classes:**
- `net.i2p.data.LeaseSet2` - LeaseSet2 structure
- `net.i2p.data.EncryptedLeaseSet` - Encrypted LS2 implementation
- `net.i2p.crypto.eddsa.EdDSAEngine` - Ed25519/Red25519 signatures
- `net.i2p.crypto.HKDF` - HKDF implementation
- `net.i2p.crypto.ChaCha20` - ChaCha20 cipher

**Configuration:**

Enable encrypted LeaseSet in `clients.config`:
```properties
# Bật LeaseSet được mã hóa

i2cp.encryptLeaseSet=true

# Tùy chọn: Bật ủy quyền cho máy khách

i2cp.enableAccessList=true

# Tùy chọn: Sử dụng DH authorization (ủy quyền bằng Diffie‑Hellman) (mặc định là PSK (khóa chia sẻ trước))

i2cp.accessListType=0

# Tùy chọn: Blinding secret (chuỗi bí mật dùng để làm mù địa chỉ) (rất được khuyến nghị)

i2cp.blindingSecret=your-secret-here

```

**API Usage Example:**

```java
// Tạo LeaseSet được mã hóa EncryptedLeaseSet els = new EncryptedLeaseSet();

// Thiết lập đích els.setDestination(destination);

// Bật ủy quyền theo từng máy khách els.setAuthorizationEnabled(true); els.setAuthType(EncryptedLeaseSet.AUTH_DH);

// Thêm các máy khách được ủy quyền (khóa công khai DH (Diffie-Hellman)) for (byte[] clientPubKey : authorizedClients) {

    els.addClient(clientPubKey);
}

// Thiết lập các tham số blinding (làm mù) els.setBlindingSecret("your-secret");

// Ký và công bố els.sign(signingPrivateKey); netDb.publish(els);

```

### i2pd (C++) Implementation

**Repository:** https://github.com/PurpleI2P/i2pd

**Key Files:**
- `libi2pd/LeaseSet.h/cpp` - LeaseSet implementations
- `libi2pd/Crypto.h/cpp` - Cryptographic primitives
- `libi2pd/Ed25519.h/cpp` - Ed25519/Red25519 signatures
- `libi2pd/ChaCha20.h/cpp` - ChaCha20 cipher

**Configuration:**

Enable in tunnel configuration (`tunnels.conf`):
```ini
[my-hidden-service] type = http host = 127.0.0.1 port = 8080 keys = my-service-keys.dat

# Bật LeaseSet được mã hóa

encryptleaseset = true

# Tùy chọn: Loại ủy quyền của máy khách (0=DH, 1=PSK)

authtype = 0

# Tùy chọn: Bí mật làm mù

secret = your-secret-here

# Tùy chọn: Các máy khách được ủy quyền (mỗi dòng một khóa công khai được mã hóa base64)

client.1 = base64-encoded-client-pubkey-1 client.2 = base64-encoded-client-pubkey-2

```

**API Usage Example:**

```cpp
// Tạo LeaseSet được mã hóa auto encryptedLS = std::make_shared<i2p::data::EncryptedLeaseSet>(

    destination,
    blindingSecret
);

// Kích hoạt ủy quyền theo từng máy khách encryptedLS->SetAuthType(i2p::data::AUTH_TYPE_DH);

// Thêm các máy khách được ủy quyền for (const auto& clientPubKey : authorizedClients) {

    encryptedLS->AddClient(clientPubKey);
}

// Ký và công bố encryptedLS->Sign(signingPrivKey); netdb.Publish(encryptedLS);

```

### Testing and Debugging

**Test Vectors:**

Generate test vectors for implementation verification:

```python
# Vector kiểm thử 1: Làm mù khóa

destination_pubkey = bytes.fromhex('a' * 64) sigtype = 7 blinded_sigtype = 11 date = "20251015" secret = ""

alpha = generate_alpha(destination_pubkey, sigtype, blinded_sigtype, date, secret) print(f"Alpha: {alpha.hex()}")

# Kết quả mong đợi: (xác minh đối chiếu với bản triển khai tham chiếu)

```

**Unit Tests:**

Key areas to test:
1. HKDF derivation with various inputs
2. ChaCha20 encryption/decryption
3. Red25519 signature generation and verification
4. Key blinding (private and public)
5. Layer 1/2 encryption/decryption
6. Client authorization (DH and PSK)
7. Base32 address generation and parsing

**Integration Tests:**

1. Publish encrypted LeaseSet to test network
2. Retrieve and decrypt from client
3. Verify daily key rotation
4. Test client authorization (add/remove clients)
5. Test offline keys (if supported)

**Common Implementation Errors:**

1. **Incorrect mod L reduction:** Must use proper modular arithmetic
2. **Endianness errors:** Most fields are big-endian, but some crypto uses little-endian
3. **Off-by-one in array slicing:** Verify indices are inclusive/exclusive as needed
4. **Missing constant-time comparisons:** Use constant-time for all sensitive comparisons
5. **Not zeroing key material:** Always zero keys after use

### Performance Considerations

**Computational Costs:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Operation</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Cost</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Key blinding (server)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">1 scalar mult</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per publication</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Key blinding (client)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">1 point add + 1 scalar mult</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per retrieval</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Layer 1 encryption</td><td style="border:1px solid var(--color-border); padding:0.5rem;">1 HKDF + 1 ChaCha20</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Fast</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Layer 2 encryption</td><td style="border:1px solid var(--color-border); padding:0.5rem;">1 HKDF + 1 ChaCha20</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Fast</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DH client auth (server)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">N+1 X25519 ops</td><td style="border:1px solid var(--color-border); padding:0.5rem;">N = number of clients</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DH client auth (client)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">1 X25519 op</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per retrieval</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">PSK client auth</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0 DH ops</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Only HKDF + ChaCha20</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Signature (Red25519)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">1 signature op</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Similar cost to Ed25519</td></tr>
  </tbody>
</table>

**Size Overhead:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Component</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Frequency</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Blinded public key</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per LeaseSet</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Layer 1 encryption overhead</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes (salt)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per LeaseSet</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Layer 2 encryption overhead</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes (salt)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per LeaseSet</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DH auth per client</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per client per LeaseSet</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DH ephemeral pubkey</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per LeaseSet (if DH auth)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">PSK auth per client</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per client per LeaseSet</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">PSK salt</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per LeaseSet (if PSK auth)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Signature</td><td style="border:1px solid var(--color-border); padding:0.5rem;">64 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per LeaseSet</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline sig block</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈100 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per LeaseSet (if offline keys)</td></tr>
  </tbody>
</table>

**Typical Sizes:**

- **No client auth:** ~200 bytes overhead
- **With 10 DH clients:** ~600 bytes overhead
- **With 100 DH clients:** ~4200 bytes overhead

**Optimization Tips:**

1. **Batch key generation:** Generate blinded keys for multiple days in advance
2. **Cache subcredentials:** Compute once per day, reuse for all publications
3. **Reuse ephemeral keys:** Can reuse ephemeral DH key for short period (minutes)
4. **Parallel client encryption:** Encrypt client cookies in parallel
5. **Fast path for no auth:** Skip authorization layer entirely when disabled

### Compatibility

**Backward Compatibility:**

- Ed25519 (type 7) destinations supported for unblinded keys
- Red25519 (type 11) required for blinded keys
- Traditional LeaseSets still fully supported
- Encrypted LeaseSets do not break existing network

**Forward Compatibility:**

- Reserved flag bits for future features
- Extensible authorization scheme (3 bits allow 8 types)
- Version field in various structures

**Interoperability:**

- Java I2P and i2pd fully interoperable since:
  - Java I2P 0.9.40 (May 2019)
  - i2pd 2.58.0 (September 2025)
- Encrypted LeaseSets work across implementations
- Client authorization works across implementations

---

## References

### IETF RFCs

- **[RFC 2104](https://datatracker.ietf.org/doc/html/rfc2104)** - HMAC: Keyed-Hashing for Message Authentication (February 1997)
- **[RFC 5869](https://datatracker.ietf.org/doc/html/rfc5869)** - HMAC-based Extract-and-Expand Key Derivation Function (HKDF) (May 2010)
- **[RFC 7539](https://datatracker.ietf.org/doc/html/rfc7539)** - ChaCha20 and Poly1305 for IETF Protocols (May 2015)
- **[RFC 7748](https://datatracker.ietf.org/doc/html/rfc7748)** - Elliptic Curves for Security (January 2016)

### I2P Specifications

- **[Common Structures Specification](/docs/specs/common-structures/)** - LeaseSet2 and EncryptedLeaseSet structures
- **[Proposal 123: New netDB Entries](/proposals/123-new-netdb-entries/)** - Background and design of LeaseSet2
- **[Proposal 146: Red25519](/proposals/146-red25519/)** - Red25519 signature scheme specification
- **[Proposal 149: B32 for Encrypted LS2](/proposals/149-b32-encrypted-ls2/)** - Base32 addressing for encrypted LeaseSets
- **[Red25519 Specification](/docs/specs/red25519-signature-scheme/)** - Detailed Red25519 implementation
- **[B32 Addressing Specification](/docs/specs/b32-for-encrypted-leasesets/)** - Base32 address format
- **[Network Database Documentation](/docs/specs/common-structures/)** - NetDB usage and operations
- **[I2CP Specification](/docs/specs/i2cp/)** - I2P Client Protocol

### Cryptographic References

- **[Ed25519 Paper](http://cr.yp.to/papers.html#ed25519)** - "High-speed high-security signatures" by Bernstein et al.
- **[ZCash Protocol Specification](https://zips.z.cash/protocol/protocol.pdf)** - Section 5.4.6: RedDSA signature scheme
- **[Tor Rendezvous Specification v3](https://spec.torproject.org/rend-spec)** - Tor's onion service specification (for comparison)

### Security References

- **[Key Blinding Security Discussion](https://lists.torproject.org/pipermail/tor-dev/2013-December/005943.html)** - Tor Project mailing list discussion
- **[Tor Ticket #8106](https://trac.torproject.org/projects/tor/ticket/8106)** - Key blinding implementation discussion
- **[PRNG Security](http://projectbullrun.org/dual-ec/ext-rand.html)** - Random number generator security considerations
- **[Tor PRNG Discussion](https://lists.torproject.org/pipermail/tor-dev/2015-November/009954.html)** - Discussion of PRNG usage in Tor

### Implementation References

- **[Java I2P Repository](https://github.com/i2p/i2p.i2p)** - Official Java implementation
- **[i2pd Repository](https://github.com/PurpleI2P/i2pd)** - C++ implementation
- **[I2P Website](/)** - Official I2P project website
- **[I2P Specifications](/docs/specs/)** - Complete specification index

### Version History

- **[I2P Release Notes](/en/blog)** - Official release announcements
- **[Java I2P Releases](https://github.com/i2p/i2p.i2p/releases)** - GitHub release history
- **[i2pd Releases](https://github.com/PurpleI2P/i2pd/releases)** - GitHub release history

---

## Appendix A: Cryptographic Constants

### Ed25519 / Red25519 Constants

```python
# Điểm cơ sở Ed25519 (điểm sinh)

B = 2**255 - 19

# Bậc của Ed25519 (kích thước của trường vô hướng)

L = 2**252 + 27742317777372353535851937790883648493

# Các giá trị kiểu chữ ký

SIGTYPE_ED25519 = 7    # 0x0007 SIGTYPE_RED25519 = 11  # 0x000b

# Độ dài khóa

PRIVKEY_SIZE = 32  # bytes PUBKEY_SIZE = 32   # bytes SIGNATURE_SIZE = 64  # bytes

```

### ChaCha20 Constants

```python
# Tham số ChaCha20

CHACHA20_KEY_SIZE = 32   # byte (256 bit) CHACHA20_NONCE_SIZE = 12  # byte (96 bit) CHACHA20_INITIAL_COUNTER = 1  # RFC 7539 cho phép 0 hoặc 1

```

### HKDF Constants

```python
# Các tham số HKDF (hàm dẫn xuất khóa dựa trên HMAC)

HKDF_HASH = "SHA-256" HKDF_SALT_MAX = 32  # bytes (HashLen)

# Các chuỗi "info" của HKDF (phân tách miền)

HKDF_INFO_ALPHA = b"i2pblinding1" HKDF_INFO_LAYER1 = b"ELS2_L1K" HKDF_INFO_LAYER2 = b"ELS2_L2K" HKDF_INFO_DH_AUTH = b"ELS2_XCA" HKDF_INFO_PSK_AUTH = b"ELS2PSKA"

```

### Hash Personalization Strings

```python
# SHA-256 personalization strings (chuỗi cá nhân hóa)

HASH_PERS_ALPHA = b"I2PGenerateAlpha" HASH_PERS_RED25519 = b"I2P_Red25519H(x)" HASH_PERS_CREDENTIAL = b"credential" HASH_PERS_SUBCREDENTIAL = b"subcredential"

```

### Structure Sizes

```python
# Kích thước lớp 0 (bên ngoài)

BLINDED_SIGTYPE_SIZE = 2   # bytes BLINDED_PUBKEY_SIZE = 32   # bytes (for Red25519) PUBLISHED_TS_SIZE = 4      # bytes EXPIRES_SIZE = 2           # bytes FLAGS_SIZE = 2             # bytes LEN_OUTER_CIPHER_SIZE = 2  # bytes SIGNATURE_SIZE = 64        # bytes (Red25519)

# Kích thước khối của khóa ngoại tuyến

OFFLINE_EXPIRES_SIZE = 4   # byte OFFLINE_SIGTYPE_SIZE = 2   # byte OFFLINE_SIGNATURE_SIZE = 64  # byte

# Kích thước lớp 1 (giữa)

AUTH_FLAGS_SIZE = 1        # byte EPHEMERAL_PUBKEY_SIZE = 32  # byte (xác thực DH) AUTH_SALT_SIZE = 32        # byte (xác thực PSK) NUM_CLIENTS_SIZE = 2       # byte CLIENT_ID_SIZE = 8         # byte CLIENT_COOKIE_SIZE = 32    # byte AUTH_CLIENT_ENTRY_SIZE = 40  # byte (CLIENT_ID + CLIENT_COOKIE)

# Chi phí phụ trội do mã hóa

SALT_SIZE = 32  # byte (được thêm vào đầu mỗi lớp được mã hóa)

# Địa chỉ Base32

B32_ENCRYPTED_DECODED_SIZE = 35  # byte B32_ENCRYPTED_ENCODED_LEN = 56   # ký tự B32_SUFFIX = ".b32.i2p"

```

---

## Appendix B: Test Vectors

### Test Vector 1: Alpha Generation

**Input:**
```python
# Khóa công khai của Destination (Ed25519)

A = bytes.fromhex('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa') stA = 0x0007  # Ed25519 stA_prime = 0x000b  # Red25519 date = "20251015" secret = ""  # Empty secret

```

**Computation:**
```python
keydata = A || bytes([0x00, 0x07]) || bytes([0x00, 0x0b])

# keydata = 36 byte

salt = SHA256(b"I2PGenerateAlpha" + keydata) ikm = b"20251015" info = b"i2pblinding1"

seed = HKDF(salt, ikm, info, 64) alpha = LEOS2IP(seed) mod L

```

**Expected Output:**
```
(Xác minh so với bản triển khai tham chiếu) alpha = [giá trị thập lục phân 64 byte]

```

### Test Vector 2: ChaCha20 Encryption

**Input:**
```python
key = bytes([i for i in range(32)])  # 0x00..0x1f nonce = bytes([i for i in range(12)])  # 0x00..0x0b plaintext = b"Hello, I2P!"

```

**Computation:**
```python
ciphertext = ChaCha20_Encrypt(key, nonce, plaintext, counter=1)

```

**Expected Output:**
```
ciphertext = [xác minh đối chiếu với các vector kiểm thử của RFC 7539]

```

### Test Vector 3: HKDF

**Input:**
```python
salt = bytes(32)  # All zeros ikm = b"test input keying material" info = b"ELS2_L1K" n = 44

```

**Computation:**
```python
keys = HKDF(salt, ikm, info, n)

```

**Expected Output:**
```
keys = [giá trị thập lục phân 44 byte]

```

### Test Vector 4: Base32 Address

**Input:**
```python
pubkey = bytes.fromhex('bbbb' + 'bb' * 30)  # 32 bytes unblinded_sigtype = 11  # Red25519 blinded_sigtype = 11    # Red25519

```

**Computation:**
```python
address = generate_encrypted_b32_address(pubkey, unblinded_sigtype, blinded_sigtype)

```

**Expected Output:**
```
địa chỉ = [56 ký tự base32].b32.i2p

# Xác minh rằng việc kiểm tra checksum cho kết quả chính xác

```

---

## Appendix C: Glossary

**Alpha (α):** The secret blinding factor used to blind public and private keys. Generated from the destination, date, and optional secret.

**AuthCookie:** A 32-byte random value encrypted for each authorized client, used as input to Layer 2 encryption.

**B (Base Point):** The generator point for the Ed25519 elliptic curve.

**Blinded Key:** A public or private key that has been transformed using the alpha blinding factor. Blinded keys cannot be linked to the original keys without knowing alpha.

**ChaCha20:** A stream cipher providing fast, secure encryption without requiring AES hardware support.

**ClientID:** An 8-byte identifier derived from HKDF output, used to identify authorization entries for clients.

**ClientCookie:** A 32-byte encrypted value containing the authCookie for a specific client.

**Credential:** A 32-byte value derived from the destination's public key and signature types, binding encryption to knowledge of the destination.

**CSRNG:** Cryptographically Secure Random Number Generator. Must provide unpredictable output suitable for key generation.

**DH (Diffie-Hellman):** A cryptographic protocol for securely establishing shared secrets. I2P uses X25519.

**Ed25519:** An elliptic curve signature scheme providing fast signatures with 128-bit security level.

**Ephemeral Key:** A short-lived cryptographic key, typically used once and then discarded.

**Floodfill:** I2P routers that store and serve network database entries, including encrypted LeaseSets.

**HKDF:** HMAC-based Key Derivation Function, used to derive multiple cryptographic keys from a single source.

**L (Order):** The order of the Ed25519 scalar field (approximately 2^252).

**Layer 0 (Outer):** The plaintext portion of an encrypted LeaseSet, containing blinded key and metadata.

**Layer 1 (Middle):** The first encrypted layer, containing client authorization data.

**Layer 2 (Inner):** The innermost encrypted layer, containing the actual LeaseSet2 data.

**LeaseSet2 (LS2):** Second version of I2P's network database entry format, introducing encrypted variants.

**NetDB:** The I2P network database, a distributed hash table storing router and destination information.

**Offline Keys:** A feature allowing the main signing key to remain in cold storage while a transient key handles daily operations.

**PSK (Pre-Shared Key):** A symmetric key shared in advance between two parties, used for PSK client authorization.

**Red25519:** An Ed25519-based signature scheme with key blinding support, based on ZCash RedDSA.

**Salt:** Random data used as input to key derivation functions to ensure unique outputs.

**SigType:** A numeric identifier for signature algorithms (e.g., 7 = Ed25519, 11 = Red25519).

**Subcredential:** A 32-byte value derived from the credential and blinded public key, binding encryption to a specific encrypted LeaseSet.

**Transient Key:** A temporary signing key used with offline keys, with a limited validity period.

**X25519:** An elliptic curve Diffie-Hellman protocol over Curve25519, providing key agreement.

---

## Document Information

**Status:** This document represents the current stable encrypted LeaseSet specification as implemented in I2P since June 2019. The protocol is mature and widely deployed.

**Contributing:** For corrections or improvements to this documentation, please submit issues or pull requests to the I2P specifications repository.

**Support:** For questions about implementing encrypted LeaseSets:
- I2P Forum: https://i2pforum.net/
- IRC: #i2p-dev on OFTC
- Matrix: #i2p-dev:matrix.org

**Acknowledgments:** This specification builds on work by the I2P development team, ZCash cryptography research, and Tor Project's key blinding research.