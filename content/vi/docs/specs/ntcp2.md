---
title: "Truyền tải NTCP2"
description: "Giao thức truyền tải TCP dựa trên Noise (khung giao thức mật mã) cho các liên kết giữa các router"
slug: "ntcp2"
lastUpdated: "2025-10"
accurateFor: "0.9.66"
type: docs
---

## Tổng quan

NTCP2 thay thế giao thức truyền tải NTCP cũ bằng cơ chế bắt tay dựa trên Noise (bộ khung giao thức mật mã Noise), có khả năng chống việc lập dấu vân tay lưu lượng, mã hóa các trường độ dài và hỗ trợ các cipher suites (tập hợp thuật toán mật mã) hiện đại. Các router có thể chạy NTCP2 cùng với SSU2 như hai giao thức truyền tải bắt buộc trong mạng I2P. NTCP (phiên bản 1) đã bị ngừng khuyến nghị sử dụng (deprecated) từ 0.9.40 (tháng 5/2019) và bị loại bỏ hoàn toàn trong 0.9.50 (tháng 5/2021).

## Khung giao thức Noise

NTCP2 sử dụng Noise Protocol Framework (khung giao thức Noise) [Revision 33, 2017-10-04](https://noiseprotocol.org/noise.html) với các phần mở rộng dành riêng cho I2P:

- **Mẫu**: `Noise_XK_25519_ChaChaPoly_SHA256`
- **Định danh mở rộng**: `Noise_XKaesobfse+hs2+hs3_25519_ChaChaPoly_SHA256` (dùng để khởi tạo KDF (hàm dẫn xuất khóa))
- **Hàm Diffie-Hellman (DH)**: X25519 (RFC 7748) - khóa 32 byte, biểu diễn little-endian
- **Mật mã**: AEAD_CHACHA20_POLY1305 (RFC 7539/RFC 8439)
  - Nonce 12 byte: 4 byte đầu bằng 0, 8 byte cuối là bộ đếm (little-endian)
  - Giá trị nonce tối đa: 2^64 - 2 (kết nối phải kết thúc trước khi đạt tới 2^64 - 1)
- **Hàm băm**: SHA-256 (đầu ra 32 byte)
- **MAC**: Poly1305 (thẻ xác thực 16 byte)

### Các phần mở rộng dành riêng cho I2P

1. **Làm mờ bằng AES**: Khóa tạm thời được mã hóa bằng AES-256-CBC, sử dụng băm router của Bob và IV (vector khởi tạo) được công bố
2. **Đệm ngẫu nhiên**: Đệm dạng rõ trong các thông điệp 1-2 (được xác thực), đệm AEAD trong thông điệp 3+ (được mã hóa)
3. **Làm mờ độ dài bằng SipHash-2-4**: Độ dài khung 2 byte được XOR với đầu ra của SipHash
4. **Cấu trúc khung**: Khung có tiền tố độ dài cho giai đoạn dữ liệu (tương thích truyền luồng TCP)
5. **Tải trọng dựa trên khối**: Định dạng dữ liệu có cấu trúc với các khối có kiểu

## Quy trình bắt tay

```
Alice (Initiator)             Bob (Responder)
SessionRequest  ──────────────────────►
                ◄────────────────────── SessionCreated
SessionConfirmed ──────────────────────►
```
### Bắt tay ba thông điệp

1. **SessionRequest** - khóa tạm thời được che giấu của Alice, các tùy chọn, gợi ý về đệm
2. **SessionCreated** - khóa tạm thời được che giấu của Bob, các tùy chọn được mã hóa, phần đệm
3. **SessionConfirmed** - khóa tĩnh được mã hóa của Alice và RouterInfo (hai khung AEAD)

### Các mẫu thông điệp của Noise

```
XK(s, rs):           Authentication   Confidentiality
  <- s               (Bob's static key known in advance)
  -> e, es                  0                2
  <- e, ee                  2                1
  -> s, se                  2                5
  <-                        2                5
```
**Mức xác thực:** - 0: Không xác thực (bất kỳ bên nào cũng có thể đã gửi) - 2: Xác thực người gửi kháng key-compromise impersonation (KCI, giả mạo do lộ khóa)

**Các cấp độ tính bí mật:** - 1: Người nhận tạm thời (tính bí mật chuyển tiếp, không xác thực người nhận) - 2: Người nhận đã biết, tính bí mật chuyển tiếp chỉ khi phía người gửi bị xâm phạm - 5: Tính bí mật chuyển tiếp mạnh (tạm thời-tạm thời + tạm thời-tĩnh DH)

## Đặc tả thông điệp

### Ký hiệu khóa

- `RH_A` = Router Hash cho Alice (32 byte, SHA-256)
- `RH_B` = Router Hash cho Bob (32 byte, SHA-256)
- `||` = toán tử nối
- `byte(n)` = một byte có giá trị n
- Tất cả các số nguyên nhiều byte dùng **big-endian** trừ khi có chỉ định khác
- Khóa X25519 ở dạng **little-endian** (32 byte)

### Mã hóa xác thực (ChaCha20-Poly1305)

**Hàm mã hóa:**

```
AEAD_ChaCha20_Poly1305(key, nonce, associatedData, plaintext)
  → (ciphertext || MAC)
```
**Tham số:** - `key`: khóa mã 32 byte từ KDF (hàm dẫn xuất khóa) - `nonce`: 12 byte (4 byte bằng 0 + bộ đếm 8 byte, little-endian) - `associatedData`: băm 32 byte trong pha bắt tay; độ dài bằng 0 trong pha dữ liệu - `plaintext`: Dữ liệu cần mã hóa (0+ byte)

**Đầu ra:** - Bản mã: Cùng độ dài như bản rõ - MAC: 16 byte (thẻ xác thực Poly1305)

**Quản lý nonce (giá trị dùng một lần):** - Bộ đếm bắt đầu từ 0 cho mỗi thể hiện bộ mã - Tăng thêm sau mỗi thao tác AEAD theo chiều đó - Có bộ đếm riêng cho Alice→Bob và Bob→Alice trong giai đoạn dữ liệu - Phải chấm dứt kết nối trước khi bộ đếm đạt tới 2^64 - 1

## Thông điệp 1: SessionRequest (Yêu cầu phiên)

Alice khởi tạo kết nối tới Bob.

**Các thao tác Noise**: `e, es` (tạo và trao đổi khóa tạm thời)

### Định dạng thô

```
+----+----+----+----+----+----+----+----+
|                                       |
+    AES-256-CBC Encrypted X (32B)      +
|    Key: RH_B, IV: Bob's published IV  |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+    ChaChaPoly Frame (48 bytes)        +
|    Plaintext: 32B (X + options)       |
+    k from KDF-1, n=0, ad=h            +
|                                       |
+----+----+----+----+----+----+----+----+
|    Cleartext Padding (optional)       |
+    Length specified in options         +
|    0 to 65535 - 80 bytes              |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+
```
**Giới hạn kích thước:** - Tối thiểu: 80 byte (32 AES + 48 AEAD) - Tối đa: 65535 byte tổng cộng - **Trường hợp đặc biệt**: Tối đa 287 byte khi kết nối tới địa chỉ "NTCP" (giao thức truyền tải dựa trên TCP của I2P) (phát hiện phiên bản)

### Nội dung đã giải mã

```
+----+----+----+----+----+----+----+----+
|                                       |
+    X (Alice ephemeral public key)     +
|    32 bytes, X25519, little-endian    |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|           Options Block               |
+             (16 bytes)                +
|                                       |
+----+----+----+----+----+----+----+----+
|    Cleartext Padding (optional)       |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+
```
### Khối Tùy chọn (16 byte, thứ tự big-endian)

```
+----+----+----+----+----+----+----+----+
| id | ver|  padLen | m3p2len | Rsvd(0) |
+----+----+----+----+----+----+----+----+
|        tsA        |   Reserved (0)    |
+----+----+----+----+----+----+----+----+

id      : 1 byte  - Network ID (2 for mainnet, 16-254 for testnets)
ver     : 1 byte  - Protocol version (currently 2)
padLen  : 2 bytes - Padding length in this message (0-65455)
m3p2len : 2 bytes - Length of SessionConfirmed part 2 frame
Rsvd    : 2 bytes - Reserved, set to 0
tsA     : 4 bytes - Unix timestamp (seconds since epoch)
Reserved: 4 bytes - Reserved, set to 0
```
**Các trường quan trọng:** - **Network ID** (kể từ 0.9.42): Từ chối nhanh các kết nối khác mạng - **m3p2len**: Kích thước chính xác của phần 2 của thông điệp 3 (phải khớp khi gửi)

### Hàm dẫn xuất khóa (KDF-1)

**Khởi tạo giao thức:**

```
protocol_name = "Noise_XKaesobfse+hs2+hs3_25519_ChaChaPoly_SHA256"
h = SHA256(protocol_name)
ck = h  // Chaining key initialized to hash
```
**Các phép toán MixHash:**

```
h = SHA256(h)                    // Null prologue
h = SHA256(h || rs)              // Bob's static key (known)
h = SHA256(h || e.pubkey)        // Alice's ephemeral key X
// h is now the associated data for message 1 AEAD
```
**Hoạt động MixKey (trộn khóa) (es pattern):**

```
dh_result = X25519(Alice.ephemeral_private, Bob.static_public)
temp_key = HMAC-SHA256(ck, dh_result)
ck = HMAC-SHA256(temp_key, byte(0x01))
k = HMAC-SHA256(temp_key, ck || byte(0x02))
// k is the cipher key for message 1
// ck is retained for message 2 KDF
```
### Ghi chú cài đặt

1. **Làm rối AES**: Chỉ dùng để chống DPI (kiểm tra gói tin sâu); bất kỳ ai có router hash của Bob và IV (vector khởi tạo) đều có thể giải mã X
2. **Ngăn chặn phát lại**: Bob phải lưu đệm các giá trị X (hoặc các tương đương đã mã hóa) trong ít nhất 2*D giây (D = độ lệch đồng hồ tối đa)
3. **Xác thực dấu thời gian**: Bob phải từ chối các kết nối với |tsA - current_time| > D (thường D = 60 giây)
4. **Xác thực đường cong**: Bob phải xác minh X là một điểm X25519 hợp lệ
5. **Từ chối nhanh**: Bob có thể kiểm tra X[31] & 0x80 == 0 trước khi giải mã (khóa X25519 hợp lệ có MSB (bit có ý nghĩa cao nhất) bằng 0)
6. **Xử lý lỗi**: Khi gặp lỗi bất kỳ, Bob đóng kết nối bằng TCP RST (gói RST của TCP) sau thời gian chờ ngẫu nhiên và đọc một lượng byte ngẫu nhiên
7. **Bộ đệm**: Alice phải thực hiện flush (xả) toàn bộ thông điệp (bao gồm cả padding (phần đệm)) cùng lúc để đạt hiệu quả

## Thông điệp 2: SessionCreated

Bob trả lời Alice.

**Các thao tác Noise**: `e, ee` (DH tạm thời–tạm thời)

### Định dạng thô

```
+----+----+----+----+----+----+----+----+
|                                       |
+    AES-256-CBC Encrypted Y (32B)      +
|    Key: RH_B, IV: AES state from msg1 |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+    ChaChaPoly Frame (48 bytes)        +
|    Plaintext: 32B (Y + options)       |
+    k from KDF-2, n=0, ad=h            +
|                                       |
+----+----+----+----+----+----+----+----+
|    Cleartext Padding (optional)       |
+    Length specified in options         +
|    0 to 65535 - 80 bytes              |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+
```
### Nội dung đã giải mã

```
+----+----+----+----+----+----+----+----+
|                                       |
+    Y (Bob ephemeral public key)       +
|    32 bytes, X25519, little-endian    |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|           Options Block               |
+             (16 bytes)                +
|                                       |
+----+----+----+----+----+----+----+----+
|    Cleartext Padding (optional)       |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+
```
### Khối Tùy chọn (16 byte, big-endian (thứ tự byte có trọng số lớn nhất trước))

```
+----+----+----+----+----+----+----+----+
| Rsvd(0) | padLen  |   Reserved (0)    |
+----+----+----+----+----+----+----+----+
|        tsB        |   Reserved (0)    |
+----+----+----+----+----+----+----+----+

Rsvd    : 2 bytes - Reserved, set to 0
padLen  : 2 bytes - Padding length in this message
Reserved: 10 bytes - Reserved, set to 0
tsB     : 4 bytes - Unix timestamp (seconds since epoch)
```
### Hàm dẫn xuất khóa (KDF-2)

**Các phép toán MixHash:**

```
h = SHA256(h || encrypted_payload_msg1)  // 32-byte ciphertext
if (msg1_padding_length > 0):
    h = SHA256(h || padding_from_msg1)
h = SHA256(h || e.pubkey)                // Bob's ephemeral key Y
// h is now the associated data for message 2 AEAD
```
**Hoạt động MixKey (trộn khóa) (mẫu ee):**

```
dh_result = X25519(Bob.ephemeral_private, Alice.ephemeral_public)
temp_key = HMAC-SHA256(ck, dh_result)
ck = HMAC-SHA256(temp_key, byte(0x01))
k = HMAC-SHA256(temp_key, ck || byte(0x02))
// k is the cipher key for message 2
// ck is retained for message 3 KDF
```
**Dọn dẹp bộ nhớ:**

```
// Overwrite ephemeral keys after ee DH
Alice.ephemeral_public = zeros(32)
Alice.ephemeral_private = zeros(32)  // Bob side
Bob.received_ephemeral = zeros(32)    // Bob side
```
### Ghi chú hiện thực

1. **Xâu chuỗi AES**: Mã hóa Y sử dụng trạng thái AES-CBC từ thông điệp 1 (không đặt lại)
2. **Ngăn chặn phát lại**: Alice phải lưu vào bộ nhớ đệm các giá trị Y trong ít nhất 2*D giây
3. **Kiểm tra dấu thời gian**: Alice phải từ chối khi |tsB - current_time| > D
4. **Xác minh đường cong**: Alice phải xác minh Y là một điểm X25519 hợp lệ
5. **Xử lý lỗi**: Alice đóng kết nối bằng TCP RST khi xảy ra bất kỳ lỗi nào
6. **Bộ đệm**: Bob phải xả toàn bộ thông điệp trong một lần

## Thông điệp 3: SessionConfirmed (xác nhận phiên)

Alice xác nhận phiên và gửi RouterInfo (thông tin về router).

**Các thao tác Noise**: `s, se` (tiết lộ khóa tĩnh và DH giữa khóa tĩnh và khóa tạm thời)

### Cấu trúc hai phần

Thông điệp 3 bao gồm **hai AEAD frames (khung AEAD) riêng biệt**:

1. **Phần 1**: Khung 48 byte cố định với khóa tĩnh được mã hóa của Alice
2. **Phần 2**: Khung độ dài biến đổi với RouterInfo, các tùy chọn và phần đệm

### Định dạng thô

```
+----+----+----+----+----+----+----+----+
|    ChaChaPoly Frame 1 (48 bytes)      |
+    Plaintext: Alice static key (32B)  +
|    k from KDF-2, n=1, ad=h            |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+    ChaChaPoly Frame 2 (variable)      +
|    Length specified in msg1.m3p2len   |
+    k from KDF-3, n=0, ad=h            +
|    Plaintext: RouterInfo + padding    |
+                                       +
|                                       |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+
```
**Giới hạn kích thước:** - Phần 1: Chính xác 48 byte (32 bản rõ + 16 MAC) - Phần 2: Độ dài được chỉ định trong thông điệp 1 (trường m3p2len) - Tổng tối đa: 65535 byte (phần 1 tối đa 48, nên phần 2 tối đa 65487)

### Nội dung đã giải mã

**Phần 1:**

```
+----+----+----+----+----+----+----+----+
|                                       |
+    S (Alice static public key)        +
|    32 bytes, X25519, little-endian    |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
```
**Phần 2:**

```
+----+----+----+----+----+----+----+----+
|    Block: RouterInfo (required)       |
+    Type=2, contains Alice's RI         +
|                                       |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+
|    Block: Options (optional)          |
+    Type=1, padding parameters          +
|                                       |
+----+----+----+----+----+----+----+----+
|    Block: Padding (optional)          |
+    Type=254, random data               +
|    MUST be last block if present      |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+
```
### Hàm dẫn xuất khóa (KDF-3)

**Phần 1 (mẫu chữ s):**

```
h = SHA256(h || encrypted_payload_msg2)  // 32-byte ciphertext
if (msg2_padding_length > 0):
    h = SHA256(h || padding_from_msg2)

// Encrypt static key with message 2 cipher key
ciphertext = AEAD_ChaCha20_Poly1305(k_msg2, n=1, h, Alice.static_public)
h = SHA256(h || ciphertext)  // 48 bytes (32 + 16)
// h is now the associated data for message 3 part 2
```
**Phần 2 (se pattern):**

```
dh_result = X25519(Alice.static_private, Bob.ephemeral_public)
temp_key = HMAC-SHA256(ck, dh_result)
ck = HMAC-SHA256(temp_key, byte(0x01))
k = HMAC-SHA256(temp_key, ck || byte(0x02))
// k is the cipher key for message 3 part 2
// ck is retained for data phase KDF

ciphertext = AEAD_ChaCha20_Poly1305(k, n=0, h, payload)
h = SHA256(h || ciphertext)
// h is retained for SipHash KDF
```
**Dọn dẹp bộ nhớ:**

```
// Overwrite Bob's ephemeral key after se DH
Alice.received_ephemeral = zeros(32)  // Alice side
Bob.ephemeral_public = zeros(32)       // Bob side
Bob.ephemeral_private = zeros(32)      // Bob side
```
### Ghi chú hiện thực

1. **Xác thực RouterInfo (khối thông tin của router)**: Bob phải xác minh chữ ký, dấu thời gian và tính nhất quán của khóa
2. **Đối chiếu khóa**: Bob phải xác minh khóa tĩnh của Alice ở phần 1 trùng khớp với khóa trong RouterInfo
3. **Vị trí khóa tĩnh**: Tìm tham số "s" trùng khớp trong RouterAddress NTCP hoặc NTCP2
4. **Thứ tự khối**: RouterInfo phải đứng đầu, Options thứ hai (nếu có), Padding cuối cùng (nếu có)
5. **Lập kế hoạch độ dài**: Alice phải bảo đảm m3p2len trong thông điệp 1 khớp chính xác với độ dài của phần 2
6. **Đệm**: Alice phải xả đệm cả hai phần trong cùng một lần gửi TCP duy nhất
7. **Xâu chuỗi tùy chọn**: Alice có thể nối thêm một khung giai đoạn dữ liệu ngay lập tức để tăng hiệu quả

## Giai đoạn dữ liệu

Sau khi hoàn tất quá trình bắt tay, tất cả các thông điệp sử dụng các khung AEAD (mã hóa xác thực kèm dữ liệu liên kết) có độ dài thay đổi, với các trường độ dài được che giấu.

### Hàm dẫn xuất khóa (Giai đoạn dữ liệu)

**Hàm Split (Noise — khung giao thức mật mã):**

```
// Generate transmit and receive keys
zerolen = ""  // Zero-length byte array
temp_key = HMAC-SHA256(ck, zerolen)

// Alice transmits to Bob
k_ab = HMAC-SHA256(temp_key, byte(0x01))

// Bob transmits to Alice  
k_ba = HMAC-SHA256(temp_key, k_ab || byte(0x02))

// Cleanup
ck = zeros(32)
temp_key = zeros(32)
```
**Dẫn xuất khóa bằng SipHash (hàm băm dùng khóa):**

```
// Generate additional symmetric key for SipHash
ask_master = HMAC-SHA256(temp_key, "ask" || byte(0x01))

// "siphash" is 7 bytes US-ASCII
temp_key2 = HMAC-SHA256(ask_master, h || "siphash")
sip_master = HMAC-SHA256(temp_key2, byte(0x01))

// Alice to Bob SipHash keys
temp_key3 = HMAC-SHA256(sip_master, zerolen)
sipkeys_ab = HMAC-SHA256(temp_key3, byte(0x01))
sipk1_ab = sipkeys_ab[0:7]   // 8 bytes, little-endian
sipk2_ab = sipkeys_ab[8:15]  // 8 bytes, little-endian
sipiv_ab = sipkeys_ab[16:23] // 8 bytes, IV

// Bob to Alice SipHash keys
sipkeys_ba = HMAC-SHA256(temp_key3, sipkeys_ab || byte(0x02))
sipk1_ba = sipkeys_ba[0:7]   // 8 bytes, little-endian
sipk2_ba = sipkeys_ba[8:15]  // 8 bytes, little-endian
sipiv_ba = sipkeys_ba[16:23] // 8 bytes, IV
```
### Cấu trúc khung

```
+----+----+----+----+----+----+----+----+
|Obfs Len |                             |
+----+----+    ChaChaPoly Frame         +
|    Encrypted Block Data               |
+    k_ab (Alice→Bob) or k_ba (Bob→Alice)|
|    Nonce starts at 0, increments      |
+    No associated data (empty string)  +
|                                       |
~           .   .   .                   ~
|                                       |
+----+----+----+----+----+----+----+----+
|    Poly1305 MAC (16 bytes)            |
+----+----+----+----+----+----+----+----+
```
**Ràng buộc khung:** - Tối thiểu: 18 byte (2 độ dài đã làm nhiễu + 0 bản rõ + 16 MAC) - Tối đa: 65537 byte (2 độ dài đã làm nhiễu + 65535 khung) - Khuyến nghị: Vài KB mỗi khung (giảm thiểu độ trễ phía nhận)

### Che giấu độ dài bằng SipHash (hàm băm nhẹ, nhanh dùng cho bảng băm)

**Mục đích**: Ngăn DPI (kiểm tra gói tin sâu) nhận diện ranh giới khung

**Thuật toán:**

```
// Initialization (per direction)
IV[0] = sipiv  // From KDF

// For each frame:
IV[n] = SipHash-2-4(sipk1, sipk2, IV[n-1])
Mask[n] = IV[n][0:1]  // First 2 bytes of IV
ObfuscatedLength = ActualLength XOR Mask[n]

// Send 2-byte ObfuscatedLength, then ActualLength bytes
```
**Giải mã:**

```
// Receiver maintains identical IV chain
IV[n] = SipHash-2-4(sipk1, sipk2, IV[n-1])
Mask[n] = IV[n][0:1]
ActualLength = ObfuscatedLength XOR Mask[n]
// Read ActualLength bytes (includes 16-byte MAC)
```
**Ghi chú:** - Tách các chuỗi IV (vector khởi tạo) cho từng hướng (Alice→Bob và Bob→Alice) - Nếu SipHash trả về uint64 (số nguyên không dấu 64-bit), dùng 2 byte có ý nghĩa thấp nhất làm mặt nạ - Chuyển đổi uint64 thành IV tiếp theo dưới dạng các byte little-endian (thứ tự byte từ thấp đến cao)

### Định dạng khối

Mỗi khung có thể chứa 0 hoặc nhiều khối:

```
+----+----+----+----+----+----+----+----+
|Type| Length  |       Data              |
+----+----+----+                        +
|                                       |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+

Type  : 1 byte  - Block type identifier
Length: 2 bytes - Big-endian, data size (0-65516)
Data  : Variable length payload
```
**Giới hạn kích thước:** - Khung tối đa: 65535 byte (bao gồm MAC) - Không gian khối tối đa: 65519 byte (khung - MAC 16 byte) - Khối đơn tối đa: 65519 byte (phần đầu 3 byte + 65516 dữ liệu)

### Các loại khối

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Name</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">DateTime</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Time synchronization (4-byte timestamp)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Options</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Padding parameters, dummy traffic</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">RouterInfo</td><td style="border:1px solid var(--color-border); padding:0.5rem;">RouterInfo delivery/flooding</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">I2NP</td><td style="border:1px solid var(--color-border); padding:0.5rem;">I2NP message with shortened header</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Termination</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Explicit connection close</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">224-253</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Experimental features</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">254</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Padding</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Random padding (must be last)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">255</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Future extensions</td></tr>
  </tbody>
</table>
**Quy tắc sắp xếp khối:** - **Thông điệp 3 phần 2**: RouterInfo, Options (tùy chọn), Padding (tùy chọn) - KHÔNG có loại nào khác - **Giai đoạn dữ liệu**: Bất kỳ thứ tự nào, ngoại trừ:   - Padding (đệm) PHẢI là khối cuối cùng nếu có   - Termination (kết thúc) PHẢI là khối cuối cùng (ngoại trừ Padding) nếu có - Cho phép nhiều khối I2NP trên mỗi khung - KHÔNG cho phép nhiều khối Padding trên mỗi khung

### Loại khối 0: DateTime (ngày giờ)

Đồng bộ hóa thời gian để phát hiện độ lệch đồng hồ.

```
+----+----+----+----+----+----+----+
| 0  |    4    |     timestamp     |
+----+----+----+----+----+----+----+

Type     : 0
Length   : 4 (big-endian)
Timestamp: 4 bytes, Unix seconds (big-endian)
```
**Triển khai**: Làm tròn đến giây gần nhất để ngăn tích lũy sai lệch đồng hồ.

### Loại khối 1: Tùy chọn

Các tham số đệm và định hình lưu lượng.

```
+----+----+----+----+----+----+----+----+
| 1  |  size   |tmin|tmax|rmin|rmax|tdmy|
+----+----+----+----+----+----+----+----+
|tdmy|  rdmy   |  tdelay |  rdelay |    |
+----+----+----+----+----+----+----+    +
|         more_options (TBD)            |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+

Type  : 1
Length: 12+ bytes (big-endian)
```
**Tỷ lệ đệm** (số cố định 4.4 (fixed-point), giá trị/16.0): - `tmin`: Tỷ lệ đệm tối thiểu khi truyền (0.0 - 15.9375) - `tmax`: Tỷ lệ đệm tối đa khi truyền (0.0 - 15.9375) - `rmin`: Tỷ lệ đệm tối thiểu khi nhận (0.0 - 15.9375) - `rmax`: Tỷ lệ đệm tối đa khi nhận (0.0 - 15.9375)

**Ví dụ:** - 0x00 = 0% phần đệm - 0x01 = 6.25% phần đệm - 0x10 = 100% phần đệm (tỉ lệ 1:1) - 0x80 = 800% phần đệm (tỉ lệ 8:1)

**Dummy Traffic (lưu lượng giả):** - `tdmy`: Mức tối đa sẵn sàng gửi (2 byte, trung bình tính theo byte/giây) - `rdmy`: Mức được yêu cầu nhận (2 byte, trung bình tính theo byte/giây)

**Chèn độ trễ:** - `tdelay`: Độ trễ tối đa sẵn sàng chèn (2 byte, trung bình tính theo mili giây) - `rdelay`: Độ trễ được yêu cầu (2 byte, trung bình tính theo mili giây)

**Hướng dẫn:** - Giá trị tối thiểu biểu thị mức độ chống phân tích lưu lượng mong muốn - Giá trị tối đa biểu thị các ràng buộc về băng thông - Bên gửi nên tôn trọng mức tối đa của bên nhận - Bên gửi có thể tôn trọng mức tối thiểu của bên nhận trong phạm vi các ràng buộc - Không có cơ chế cưỡng chế; các triển khai có thể khác nhau

### Kiểu khối 2: RouterInfo (thông tin về router)

Phân phối RouterInfo (thông tin router) để bổ sung netdb và phát tán.

```
+----+----+----+----+----+----+----+----+
| 2  |  size   |flg |    RouterInfo     |
+----+----+----+----+                   +
|                                       |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+

Type : 2
Length: Flag (1 byte) + RouterInfo size
Flag : Bit 0 = flood request (1) or local store (0)
       Bits 1-7 = Reserved, set to 0
```
**Cách sử dụng:**

**Trong Thông điệp 3 Phần 2** (bắt tay): - Alice gửi RouterInfo (bản ghi thông tin của router trong I2P) của cô ấy cho Bob - Flood bit (cờ flood) thường là 0 (lưu trữ cục bộ) - RouterInfo KHÔNG nén gzip

**Trong Giai đoạn Dữ liệu:** - Mỗi bên có thể gửi RouterInfo đã cập nhật của mình - bit Flood = 1: Yêu cầu phân phối qua floodfill (nếu bên nhận là floodfill) - bit Flood = 0: Chỉ lưu trữ cục bộ trong netdb

**Yêu cầu xác minh:** 1. Xác minh loại chữ ký được hỗ trợ 2. Xác minh chữ ký RouterInfo (thông tin router) 3. Xác minh dấu thời gian nằm trong giới hạn chấp nhận được 4. Đối với bắt tay: Xác minh khóa tĩnh khớp với tham số "s" của địa chỉ NTCP2 5. Đối với giai đoạn dữ liệu: Xác minh băm của router khớp với peer (đồng cấp) của phiên 6. Chỉ flood (phát tán) các RouterInfos với các địa chỉ đã công bố

**Ghi chú:** - Không có cơ chế ACK (sử dụng I2NP DatabaseStore (thông điệp DatabaseStore của I2NP) với token phản hồi nếu cần) - Có thể chứa các RouterInfos (bản ghi thông tin router) của bên thứ ba (sử dụng floodfill) - KHÔNG nén gzip (khác với I2NP DatabaseStore)

### Loại khối 3: Thông điệp I2NP

Thông điệp I2NP với phần đầu 9 byte được rút gọn.

```
+----+----+----+----+----+----+----+----+
| 3  |  size   |type|    msg_id         |
+----+----+----+----+----+----+----+----+
|   expiration  |     I2NP payload      |
+----+----+----+                        +
|                                       |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+

Type      : 3
Length    : 9 + payload_size (big-endian)
Type      : 1 byte, I2NP message type
Msg_ID    : 4 bytes, big-endian, I2NP message ID
Expiration: 4 bytes, big-endian, Unix timestamp (seconds)
Payload   : I2NP message body (length = size - 9)
```
**Khác biệt so với NTCP1:** - Thời điểm hết hạn: 4 byte (giây) so với 8 byte (mili giây) - Độ dài: Được lược bỏ (có thể suy ra từ độ dài khối) - Checksum: Được lược bỏ (AEAD - mã hóa xác thực kèm dữ liệu liên kết - cung cấp tính toàn vẹn) - Header: 9 byte so với 16 byte (giảm 44%)

**Phân mảnh:** - Thông điệp I2NP KHÔNG ĐƯỢC bị phân mảnh giữa các khối - Thông điệp I2NP KHÔNG ĐƯỢC bị phân mảnh giữa các khung - Nhiều khối I2NP được phép trên mỗi khung

### Loại khối 4: Kết thúc

Đóng kết nối tường minh kèm mã lý do.

```
+----+----+----+----+----+----+----+----+
| 4  |  size   |  valid_frames_recv    |
+----+----+----+----+----+----+----+----+
| (continued) |rsn |   additional_data   |
+----+----+----+----+                   +
|                                       |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+

Type            : 4
Length          : 9+ bytes (big-endian)
Valid_Frames_Recv: 8 bytes, big-endian (receive nonce value)
                  0 if error in handshake phase
Reason          : 1 byte (see table below)
Additional_Data : Optional (format unspecified, for debugging)
```
**Mã lý do:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Reason</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Phase</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Normal close / unspecified</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Any</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Termination received</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Data</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Idle timeout</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Data</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Router shutdown</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Data</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Data phase AEAD failure</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Data</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Incompatible options</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshake</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Incompatible signature type</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshake</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Clock skew</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshake</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">8</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Padding violation</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Any</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">9</td><td style="border:1px solid var(--color-border); padding:0.5rem;">AEAD framing error</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Data</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Payload format error</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Data</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">11</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Message 1 error</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshake</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Message 2 error</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshake</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">13</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Message 3 error</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshake</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">14</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Intra-frame read timeout</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Data</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">15</td><td style="border:1px solid var(--color-border); padding:0.5rem;">RouterInfo signature verification fail</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshake</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">16</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Static key parameter mismatch</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshake</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">17</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Banned</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Any</td></tr>
  </tbody>
</table>
**Quy tắc:** - Termination (khối kết thúc) PHẢI là khối không phải phần đệm cuối cùng trong khung - Tối đa một khối Termination cho mỗi khung - Bên gửi nên đóng kết nối sau khi gửi - Bên nhận nên đóng kết nối sau khi nhận

**Xử lý lỗi:** - Lỗi bắt tay: Thường đóng bằng TCP RST (không có khối kết thúc) - Lỗi AEAD (mã hóa xác thực kèm dữ liệu liên kết) ở giai đoạn dữ liệu: timeout ngẫu nhiên + đọc ngẫu nhiên, rồi gửi thông điệp kết thúc - Xem phần "AEAD Error Handling" để biết các thủ tục bảo mật

### Loại khối 254: Đệm

Phần đệm ngẫu nhiên để tăng khả năng chống phân tích lưu lượng.

```
+----+----+----+----+----+----+----+----+
|254 |  size   |     random_data       |
+----+----+----+                        +
|                                       |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+

Type: 254
Length: 0-65516 bytes (big-endian)
Data: Cryptographically random bytes
```
**Quy tắc:** - Phần đệm PHẢI là khối cuối cùng trong khung nếu có - Cho phép phần đệm độ dài bằng 0 - Chỉ một khối đệm cho mỗi khung - Cho phép các khung chỉ có phần đệm - Nên tuân theo các tham số đã thương lượng từ khối Options

**Đệm trong Thông điệp 1-2:** - Nằm ngoài khung AEAD (mã hóa xác thực kèm dữ liệu) (bản rõ) - Được đưa vào chuỗi băm của thông điệp tiếp theo (được xác thực) - Phát hiện giả mạo khi AEAD của thông điệp tiếp theo thất bại

**Đệm trong Thông điệp 3+ và Giai đoạn Dữ liệu:** - Bên trong khung AEAD (mã hóa xác thực đồng thời; được mã hóa và xác thực) - Dùng để định hình lưu lượng và che giấu kích thước

## Xử lý lỗi AEAD (mã hóa xác thực kèm dữ liệu)

**Các yêu cầu bảo mật trọng yếu:**

### Giai đoạn bắt tay (Thông điệp 1-3)

**Kích thước thông điệp đã biết:** - Kích thước thông điệp được định sẵn hoặc được chỉ định trước - Lỗi xác thực AEAD (mã hóa xác thực kèm dữ liệu liên kết) là rõ ràng, không mơ hồ

**Phản hồi của Bob khi Thông điệp 1 thất bại:** 1. Đặt thời hạn chờ ngẫu nhiên (khoảng phụ thuộc vào triển khai, đề xuất 100-500ms) 2. Đọc số byte ngẫu nhiên (khoảng phụ thuộc vào triển khai, đề xuất 1KB-64KB) 3. Đóng kết nối bằng TCP RST (không phản hồi) 4. Tạm thời đưa IP nguồn vào danh sách đen 5. Theo dõi các lỗi lặp lại để áp dụng lệnh cấm dài hạn

**Phản hồi của Alice khi Thông điệp 2 thất bại:** 1. Đóng kết nối ngay lập tức bằng TCP RST 2. Không gửi phản hồi cho Bob

**Phản hồi của Bob khi Thông điệp 3 thất bại:** 1. Đóng kết nối ngay lập tức bằng TCP RST 2. Không phản hồi cho Alice

### Giai đoạn dữ liệu

**Kích thước thông điệp được làm rối:** - Trường độ dài được làm rối bằng SipHash - Độ dài không hợp lệ hoặc lỗi AEAD có thể cho thấy:   - Thăm dò từ kẻ tấn công   - Hỏng dữ liệu mạng   - IV SipHash bị mất đồng bộ (IV: vector khởi tạo)   - Nút ngang hàng độc hại

**Phản hồi đối với lỗi AEAD hoặc lỗi độ dài:** 1. Đặt thời gian chờ ngẫu nhiên (đề xuất 100-500ms) 2. Đọc số lượng byte ngẫu nhiên (đề xuất 1KB-64KB) 3. Gửi khối kết thúc với mã lý do 4 (lỗi AEAD) hoặc 9 (lỗi khung) 4. Đóng kết nối

**Ngăn chặn Decryption Oracle (oracle giải mã):** - Không bao giờ tiết lộ loại lỗi cho đồng cấp trước khi hết một thời gian chờ ngẫu nhiên - Không bao giờ bỏ qua kiểm tra tính hợp lệ của độ dài trước khi kiểm tra AEAD (mã hóa xác thực với dữ liệu liên kết) - Xử lý độ dài không hợp lệ giống hệt như lỗi AEAD - Sử dụng cùng một luồng xử lý lỗi cho cả hai lỗi

**Các cân nhắc triển khai:** - Một số triển khai có thể tiếp tục sau lỗi AEAD (mã hóa xác thực kèm dữ liệu liên kết) nếu lỗi hiếm khi xảy ra - Kết thúc sau khi lỗi lặp lại (ngưỡng đề xuất: 3-5 lỗi mỗi giờ) - Cân bằng giữa khả năng phục hồi sau lỗi và bảo mật

## RouterInfo (thông tin router) đã được công bố

### Định dạng địa chỉ Router

Hỗ trợ NTCP2 được quảng bá thông qua các mục RouterAddress được công bố với các tùy chọn cụ thể.

**Kiểu truyền tải:** - `"NTCP2"` - Chỉ NTCP2 trên cổng này - `"NTCP"` - Cả NTCP và NTCP2 trên cổng này (tự động phát hiện)   - **Lưu ý**: Hỗ trợ NTCP (v1) đã bị loại bỏ trong 0.9.50 (Tháng 5/2021)   - Kiểu "NTCP" hiện đã lỗi thời; hãy dùng "NTCP2"

### Tùy chọn bắt buộc

**Tất cả các địa chỉ NTCP2 đã được công bố:**

1. **`host`** - Địa chỉ IP (IPv4 hoặc IPv6) hoặc tên máy chủ
   - Định dạng: Ký hiệu IP chuẩn hoặc tên miền
   - Có thể bỏ qua đối với router chỉ đi ra (outbound-only) hoặc router ẩn (hidden)

2. **`port`** - số cổng TCP
   - Định dạng: Số nguyên, 1-65535
   - Có thể bỏ qua đối với router outbound-only (chỉ gửi ra) hoặc router ẩn

3. **`s`** - Khóa công khai tĩnh (X25519)
   - Định dạng: được mã hóa Base64, 44 ký tự
   - Mã hóa: bảng chữ cái Base64 của I2P
   - Nguồn: khóa công khai X25519 32 byte, little-endian (thứ tự byte thấp trước)

4. **`i`** - Vector khởi tạo cho AES
   - Định dạng: được mã hóa Base64, 24 ký tự
   - Bảng mã: bảng chữ cái Base64 của I2P
   - Nguồn: IV 16 byte, big-endian (thứ tự byte đầu lớn)

5. **`v`** - Phiên bản giao thức
   - Định dạng: Số nguyên hoặc các số nguyên phân tách bằng dấu phẩy
   - Hiện tại: `"2"`
   - Tương lai: `"2,3"` (phải theo thứ tự số tăng dần)

**Các tùy chọn không bắt buộc:**

6. **`caps`** - Khả năng (từ 0.9.50)
   - Định dạng: Chuỗi các ký tự khả năng
   - Giá trị:
     - `"4"` - Khả năng kết nối ra ngoài IPv4
     - `"6"` - Khả năng kết nối ra ngoài IPv6
     - `"46"` - Cả IPv4 và IPv6 (thứ tự khuyến nghị)
   - Không cần thiết nếu `host` được công bố
   - Hữu ích cho routers ẩn/bị tường lửa chặn

7. **`cost`** - Ưu tiên địa chỉ
   - Định dạng: Số nguyên, 0-255
   - Giá trị thấp hơn = ưu tiên cao hơn
   - Gợi ý: 5-10 cho địa chỉ thông thường
   - Gợi ý: 14 cho các địa chỉ chưa công bố

### Ví dụ các mục RouterAddress

**Địa chỉ IPv4 được công bố:**

```
<Address cost="5">
  <transport_style>NTCP2</transport_style>
  <options>
    <host>192.0.2.1</host>
    <port>8887</port>
    <s>9EjeG7BZeznKbL9a2fXx8JBDPgLZbLmKbqY3QrNGJCo=</s>
    <i>MDEyMzQ1Njc4OUFCQ0RFRg==</i>
    <v>2</v>
  </options>
</Address>
```
**Router ẩn (chỉ gửi đi):**

```
<Address cost="14">
  <transport_style>NTCP2</transport_style>
  <options>
    <s>9EjeG7BZeznKbL9a2fXx8JBDPgLZbLmKbqY3QrNGJCo=</s>
    <v>2</v>
    <caps>4</caps>
  </options>
</Address>
```
**Router hai ngăn xếp:**

```
<!-- IPv4 Address -->
<Address cost="5">
  <transport_style>NTCP2</transport_style>
  <options>
    <host>192.0.2.1</host>
    <port>8887</port>
    <s>9EjeG7BZeznKbL9a2fXx8JBDPgLZbLmKbqY3QrNGJCo=</s>
    <i>MDEyMzQ1Njc4OUFCQ0RFRg==</i>
    <v>2</v>
  </options>
</Address>

<!-- IPv6 Address (same keys, same port) -->
<Address cost="5">
  <transport_style>NTCP2</transport_style>
  <options>
    <host>2001:db8::1</host>
    <port>8887</port>
    <s>9EjeG7BZeznKbL9a2fXx8JBDPgLZbLmKbqY3QrNGJCo=</s>
    <i>MDEyMzQ1Njc4OUFCQ0RFRg==</i>
    <v>2</v>
  </options>
</Address>
```
**Quy tắc quan trọng:** - Nhiều địa chỉ NTCP2 với **cùng cổng** PHẢI sử dụng **giống hệt** các giá trị `s`, `i`, và `v` - Các cổng khác nhau có thể sử dụng các khóa khác nhau - Các router dual-stack (hỗ trợ cả IPv4 và IPv6) nên công bố các địa chỉ IPv4 và IPv6 riêng biệt

### Địa chỉ NTCP2 chưa được công bố

**Dành cho các router chỉ kết nối ra ngoài:**

Nếu một router không chấp nhận các kết nối NTCP2 đến nhưng khởi tạo các kết nối đi, thì nó PHẢI vẫn công bố một RouterAddress (địa chỉ Router) bao gồm:

```xml
<Address cost="14">
  <transport_style>NTCP2</transport_style>
  <options>
    <s>9EjeG7BZeznKbL9a2fXx8JBDPgLZbLmKbqY3QrNGJCo=</s>
    <v>2</v>
  </options>
</Address>
```
**Mục đích:** - Cho phép Bob xác thực khóa tĩnh của Alice trong quá trình bắt tay - Bắt buộc cho việc xác minh RouterInfo (thông tin về router) ở thông điệp 3, phần 2 - Không cần `i`, `host` hoặc `port` (chỉ hướng ra)

**Phương án thay thế:** - Thêm `s` và `v` vào địa chỉ "NTCP" hoặc SSU đã được công bố hiện có

### Luân chuyển khóa công khai và IV (vector khởi tạo)

**Chính sách bảo mật trọng yếu:**

**Quy tắc chung:** 1. **Không bao giờ luân chuyển khi router đang chạy** 2. **Lưu trữ bền vững khóa và IV (vector khởi tạo)** qua các lần khởi động lại 3. **Theo dõi thời gian ngừng hoạt động trước đó** để xác định đủ điều kiện luân chuyển

**Thời gian ngừng hoạt động tối thiểu trước khi luân chuyển:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Router Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Min Downtime</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Reason</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Published NTCP2 address</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>1 month</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Many routers cache RouterInfo</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Published SSU only (no NTCP2)</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>1 day</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Moderate caching</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">No published addresses (hidden)</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>2 hours</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Minimal impact</td></tr>
  </tbody>
</table>
**Các điều kiện kích hoạt bổ sung:** - Thay đổi địa chỉ IP cục bộ: Có thể xoay vòng bất kể thời gian ngừng hoạt động - Router "rekey" (new Router Hash): Tạo khóa mới

**Lý do:** - Ngăn lộ thời điểm khởi động lại thông qua việc thay đổi khóa - Cho phép các RouterInfos (thông tin router) được lưu trong bộ nhớ đệm hết hạn tự nhiên - Duy trì sự ổn định của mạng - Giảm số lần thử kết nối thất bại

**Triển khai:** 1. Lưu trữ khóa, IV (vector khởi tạo), và dấu thời gian lần tắt trước lâu dài 2. Khi khởi động, tính downtime = current_time - last_shutdown 3. Nếu downtime > mức tối thiểu cho loại router, có thể xoay vòng khóa/IV 4. Nếu IP thay đổi hoặc đang thay khóa, có thể xoay vòng khóa/IV 5. Nếu không, tái sử dụng khóa và IV trước đó

**Xoay vòng IV (vector khởi tạo):** - Tuân theo các quy tắc giống hệt như xoay vòng khóa - Chỉ xuất hiện trong các địa chỉ đã công bố (không áp dụng cho routers ẩn) - Khuyến nghị thay IV mỗi khi khóa thay đổi

## Phát hiện phiên bản

**Ngữ cảnh:** Khi `transportStyle="NTCP"` (kiểu cũ), Bob hỗ trợ cả NTCP (giao thức truyền tải của I2P) v1 và v2 trên cùng một cổng và phải tự động phát hiện phiên bản giao thức.

**Thuật toán phát hiện:**

```
1. Wait for at least 64 bytes (minimum NTCP2 message 1 size)

2. If received ≥ 288 bytes:
   → Connection is NTCP version 1 (NTCP1 message 1 is 288 bytes)

3. If received < 288 bytes:
   
   Option A (conservative, pre-NTCP2 majority):
   a. Wait additional short time (e.g., 100-500ms)
   b. If total received ≥ 288 bytes → NTCP1
   c. Otherwise → Attempt NTCP2 decode
   
   Option B (aggressive, post-NTCP2 majority):
   a. Attempt NTCP2 decode immediately:
      - Decrypt first 32 bytes (X key) with AES-256-CBC
      - Verify valid X25519 point (X[31] & 0x80 == 0)
      - Verify AEAD frame
   b. If decode succeeds → NTCP2
   c. If decode fails → Wait for more data or NTCP1
```
**Kiểm tra MSB (bit có trọng số lớn nhất) nhanh:** - Trước khi giải mã AES, xác minh: `encrypted_X[31] & 0x80 == 0` - Khóa X25519 hợp lệ có bit cao bằng 0 - Thất bại cho thấy có thể là NTCP1 (hoặc tấn công) - Triển khai cơ chế chống dò quét (thời gian chờ ngẫu nhiên + đọc) khi thất bại

**Yêu cầu triển khai:**

1. **Trách nhiệm của Alice:**
   - Khi kết nối tới địa chỉ "NTCP", giới hạn độ dài thông điệp 1 tối đa 287 byte
   - Buffer (đệm) và flush (xả) toàn bộ thông điệp 1 trong một lần
   - Tăng khả năng truyền trong một gói TCP duy nhất

2. **Trách nhiệm của Bob:**
   - Đệm dữ liệu nhận được trước khi xác định phiên bản
   - Triển khai xử lý timeout (hết thời gian chờ) đúng cách
   - Sử dụng TCP_NODELAY để phát hiện phiên bản nhanh chóng
   - Đệm và flush (xả bộ đệm) toàn bộ thông điệp 2 cùng lúc sau khi xác định phiên bản

**Các cân nhắc bảo mật:** - Tấn công phân đoạn: Bob nên kháng chịu việc phân đoạn TCP - Tấn công thăm dò: Triển khai độ trễ ngẫu nhiên và đọc theo byte khi xảy ra lỗi - Phòng chống DoS (tấn công từ chối dịch vụ): Giới hạn số kết nối đang chờ đồng thời - Thời gian chờ khi đọc: Cả theo từng lần đọc và tổng thể (bảo vệ khỏi "slowloris")

## Hướng dẫn về độ lệch đồng hồ

**Các trường dấu thời gian:** - Thông điệp 1: `tsA` (dấu thời gian của Alice) - Thông điệp 2: `tsB` (dấu thời gian của Bob) - Thông điệp 3+: Các khối DateTime (ngày-giờ) tùy chọn

**Độ lệch thời gian tối đa (D):** - Thông thường: **±60 giây** - Có thể cấu hình theo từng triển khai - Độ lệch > D thường gây lỗi chí mạng

### Cách Bob xử lý (Thông điệp 1)

```
1. Receive tsA from Alice
2. skew = tsA - current_time
3. If |skew| > D:
   a. Still send message 2 (allows Alice to calculate skew)
   b. Include tsB in message 2
   c. Do NOT initiate handshake completion
   d. Optionally: Temporary ban Alice's IP
   e. After message 2 sent, close connection

4. If |skew| ≤ D:
   a. Continue handshake normally
```
**Lý do:** Việc gửi thông điệp 2 ngay cả khi có sai lệch thời gian (skew) cho phép Alice chẩn đoán các vấn đề về đồng hồ.

### Cách xử lý của Alice (Thông điệp 2)

```
1. Receive tsB from Bob
2. RTT = (current_time_now - tsA_sent)
3. adjusted_skew = (tsB - current_time_now) - (RTT / 2)
4. If |adjusted_skew| > D:
   a. Close connection immediately
   b. If local clock suspect: Adjust clock or use external time source
   c. If Bob's clock suspect: Temporary ban Bob
   d. Log for operator review
5. If |adjusted_skew| ≤ D:
   a. Continue handshake normally
   b. Optionally: Track skew for time synchronization
```
**Điều chỉnh RTT (thời gian khứ hồi):** - Trừ một nửa RTT khỏi độ lệch đã tính - Tính đến độ trễ lan truyền của mạng - Ước tính độ lệch chính xác hơn

### Cách Bob xử lý (Thông điệp 3)

```
1. If message 3 received (unlikely if skew exceeded in message 1)
2. Recalculate skew = tsA_received - current_time
3. If |adjusted_skew| > D:
   a. Send termination block (reason code 7: clock skew)
   b. Close connection
   c. Ban Alice for period (e.g., 1-24 hours)
```
### Đồng bộ thời gian

**Các khối DateTime (ngày-giờ) (Giai đoạn dữ liệu):** - Gửi khối DateTime (loại 0) theo định kỳ - Bên nhận có thể dùng để hiệu chỉnh đồng hồ - Làm tròn dấu thời gian về giây gần nhất (tránh sai lệch)

**Nguồn thời gian bên ngoài:** - NTP (Giao thức thời gian mạng) - Đồng bộ hóa đồng hồ hệ thống - Thời gian đồng thuận của mạng I2P

**Chiến lược điều chỉnh đồng hồ:** - Nếu đồng hồ cục bộ bị sai: Điều chỉnh thời gian hệ thống hoặc dùng offset (độ bù) - Nếu đồng hồ của các nút ngang hàng thường xuyên sai: Gắn cờ vấn đề ở nút ngang hàng - Theo dõi thống kê độ lệch (skew) để giám sát sức khỏe mạng

## Thuộc tính bảo mật

### Tính bí mật chuyển tiếp

**Đạt được thông qua:** - Trao đổi khóa Diffie-Hellman tạm thời (X25519) - Ba phép toán DH: es, ee, se (Noise XK pattern (mẫu Noise XK)) - Khóa tạm thời được hủy sau khi hoàn tất bắt tay

**Tiến triển về tính bí mật:** - Thông điệp 1: Mức 2 (bí mật chuyển tiếp khi bên gửi bị thỏa hiệp) - Thông điệp 2: Mức 1 (người nhận tạm thời) - Thông điệp 3+: Mức 5 (bí mật chuyển tiếp mạnh)

**Bí mật chuyển tiếp hoàn hảo:** - Việc bị xâm phạm các khóa tĩnh dài hạn KHÔNG làm lộ các khóa phiên trong quá khứ - Mỗi phiên sử dụng các khóa tạm thời duy nhất - Các khóa riêng tạm thời không bao giờ được tái sử dụng - Dọn sạch bộ nhớ sau khi thỏa thuận khóa

**Hạn chế:** - Thông điệp 1 dễ bị tấn công nếu khóa tĩnh của Bob bị lộ (nhưng vẫn có forward secrecy (bí mật chuyển tiếp) nếu Alice bị xâm phạm) - Có thể xảy ra tấn công phát lại đối với thông điệp 1 (giảm thiểu bằng dấu thời gian và bộ đệm phát lại)

### Xác thực

**Xác thực lẫn nhau:** - Alice được xác thực bằng khóa tĩnh trong thông điệp 3 - Bob được xác thực bằng việc sở hữu khóa riêng tĩnh (ngầm định từ quá trình bắt tay thành công)

**Khả năng kháng Key Compromise Impersonation (mạo danh khi lộ khóa, KCI):** - Cấp độ xác thực 2 (kháng KCI) - Kẻ tấn công không thể mạo danh Alice ngay cả khi có khóa riêng tĩnh của Alice (mà không có khóa tạm thời của Alice) - Kẻ tấn công không thể mạo danh Bob ngay cả khi có khóa riêng tĩnh của Bob (mà không có khóa tạm thời của Bob)

**Xác minh khóa tĩnh:** - Alice biết khóa tĩnh của Bob từ trước (từ RouterInfo) - Bob xác minh khóa tĩnh của Alice khớp với RouterInfo trong thông điệp 3 - Ngăn chặn tấn công kẻ trung gian (man-in-the-middle)

### Khả năng chống phân tích lưu lượng

**Biện pháp đối phó DPI (kiểm tra gói tin sâu):** 1. **Che giấu bằng AES:** Các khóa tạm thời được mã hóa, trông ngẫu nhiên 2. **Che giấu độ dài bằng SipHash:** Độ dài khung không ở dạng rõ 3. **Đệm ngẫu nhiên:** Kích thước thông điệp thay đổi, không có mẫu cố định 4. **Khung được mã hóa:** Toàn bộ tải trọng được mã hóa bằng ChaCha20

**Ngăn chặn tấn công phát lại:** - Xác thực dấu thời gian (±60 giây) - Bộ đệm phát lại cho các khóa tạm thời (thời gian sống 2*D) - Việc tăng nonce (số dùng một lần) ngăn phát lại gói tin trong cùng phiên

**Khả năng chống thăm dò:** - Hết thời gian chờ ngẫu nhiên khi xảy ra lỗi AEAD - Đọc các byte ngẫu nhiên trước khi đóng kết nối - Không phản hồi khi xảy ra lỗi bắt tay - Đưa IP vào danh sách đen khi lỗi lặp lại

**Hướng dẫn về đệm:** - Thông điệp 1-2: Đệm dạng rõ (được xác thực) - Thông điệp 3+: Đệm được mã hóa bên trong các khung AEAD (xác thực kèm dữ liệu) - Tham số đệm được thương lượng (Options block) - Cho phép các khung chỉ chứa đệm

### Giảm thiểu tấn công từ chối dịch vụ

**Giới hạn kết nối:** - Số kết nối đang hoạt động tối đa (phụ thuộc vào cách triển khai) - Số bắt tay đang chờ tối đa (ví dụ: 100-1000) - Giới hạn kết nối theo từng IP (ví dụ: 3-10 đồng thời)

**Bảo vệ tài nguyên:** - Giới hạn tốc độ hoạt động DH (tốn tài nguyên) - Thời gian chờ đọc theo từng socket và tổng thể - Bảo vệ trước "Slowloris" (giới hạn tổng thời gian) - Đưa IP vào danh sách đen khi lạm dụng

**Từ chối nhanh:** - Không khớp Network ID → đóng ngay lập tức - Điểm X25519 không hợp lệ → kiểm tra nhanh MSB (bit có trọng số lớn nhất) trước khi giải mã - Dấu thời gian ngoài phạm vi → đóng mà không cần tính toán - Lỗi AEAD (mã hóa xác thực kèm dữ liệu) → không phản hồi, trễ ngẫu nhiên

**Khả năng chống thăm dò:** - Thời gian chờ ngẫu nhiên: 100-500ms (phụ thuộc vào triển khai) - Đọc ngẫu nhiên: 1KB-64KB (phụ thuộc vào triển khai) - Không cung cấp thông tin lỗi cho kẻ tấn công - Đóng bằng TCP RST (không thực hiện bắt tay FIN)

### An toàn mật mã

**Thuật toán:** - **X25519**: mức an toàn 128-bit, DH trên đường cong elliptic (Curve25519) - **ChaCha20**: mật mã dòng khóa 256-bit - **Poly1305**: MAC an toàn theo lý thuyết thông tin - **SHA-256**: kháng va chạm 128-bit, kháng tiền ảnh 256-bit - **HMAC-SHA256**: PRF (hàm giả ngẫu nhiên) để dẫn xuất khóa

**Kích thước khóa:** - Khóa tĩnh: 32 byte (256 bit) - Khóa tạm thời: 32 byte (256 bit) - Khóa mã hóa: 32 byte (256 bit) - MAC (mã xác thực thông điệp): 16 byte (128 bit)

**Các vấn đề đã biết:** - Tái sử dụng nonce của ChaCha20 gây hậu quả thảm khốc (được ngăn ngừa bằng cách tăng bộ đếm) - X25519 có vấn đề về nhóm con nhỏ (giảm thiểu bằng xác thực đường cong) - SHA-256 về mặt lý thuyết dễ bị tấn công mở rộng độ dài (không thể khai thác trong HMAC)

**Không có lỗ hổng đã biết (tính đến tháng 10 năm 2025):** - Noise Protocol Framework (khung giao thức Noise) đã được phân tích rộng rãi - ChaCha20-Poly1305 được triển khai trong TLS 1.3 - X25519 là tiêu chuẩn trong các giao thức hiện đại - Không có tấn công thực tế vào thiết kế (construction)

## Tài liệu tham khảo

### Các đặc tả chính

- **[Đặc tả NTCP2](/docs/specs/ntcp2/)** - Đặc tả I2P chính thức
- **[Đề xuất 111](/proposals/111-ntcp-2/)** - Tài liệu thiết kế ban đầu kèm phần giải thích lý do
- **[Noise Protocol Framework](https://noiseprotocol.org/noise.html)** - Bản sửa đổi 33 (2017-10-04)

### Các tiêu chuẩn mật mã

- **[RFC 7748](https://www.rfc-editor.org/rfc/rfc7748)** - Đường cong elliptic cho bảo mật (X25519)
- **[RFC 7539](https://www.rfc-editor.org/rfc/rfc7539)** - ChaCha20 và Poly1305 cho các giao thức của IETF
- **[RFC 8439](https://www.rfc-editor.org/rfc/rfc8439)** - ChaCha20-Poly1305 (thay thế RFC 7539)
- **[RFC 2104](https://www.rfc-editor.org/rfc/rfc2104)** - HMAC: Băm có khóa để xác thực thông điệp
- **[SipHash](https://www.131002.net/siphash/)** - SipHash-2-4 cho các ứng dụng của hàm băm

### Các đặc tả kỹ thuật I2P liên quan

- **[I2NP Specification](/docs/specs/i2np/)** - định dạng thông điệp của giao thức mạng I2P
- **[Common Structures](/docs/specs/common-structures/)** - các định dạng RouterInfo, RouterAddress
- **[SSU Transport](/docs/legacy/ssu/)** - transport UDP (ban đầu, nay là SSU2)
- **[Proposal 147](/proposals/147-transport-network-id-check/)** - Kiểm tra Transport Network ID (0.9.42)

### Tài liệu tham khảo triển khai

- **[I2P Java](https://github.com/i2p/i2p.i2p)** - Bản triển khai tham chiếu (Java)
- **[i2pd](https://github.com/PurpleI2P/i2pd)** - Triển khai C++
- **[I2P Release Notes](/blog/)** - Lịch sử phiên bản và cập nhật

### Bối cảnh lịch sử

- **[Station-To-Station Protocol (STS)](https://en.wikipedia.org/wiki/Station-to-Station_protocol)** - Nguồn cảm hứng cho Noise framework (khung giao thức Noise)
- **[obfs4](https://gitlab.com/yawning/obfs4)** - Pluggable transport (cơ chế truyền tải có thể cắm thêm; tiền lệ che giấu độ dài bằng SipHash)

## Hướng dẫn hiện thực

### Các yêu cầu bắt buộc

**Vì mục đích tuân thủ:**

1. **Triển khai bắt tay hoàn chỉnh:**
   - Hỗ trợ cả ba thông điệp với các chuỗi KDF (hàm dẫn xuất khóa) chính xác
   - Kiểm tra tính hợp lệ của mọi thẻ AEAD (mã hóa xác thực kèm dữ liệu)
   - Xác minh rằng các điểm X25519 (thuật toán trao đổi khóa dựa trên đường cong elliptic Curve25519) là hợp lệ

2. **Triển khai Giai đoạn Dữ liệu:**
   - Che giấu độ dài bằng SipHash (theo cả hai hướng)
   - Tất cả các loại khối: 0 (DateTime), 1 (Options), 2 (RouterInfo), 3 (I2NP), 4 (Termination), 254 (Padding)
   - Quản lý nonce (số dùng một lần) đúng cách (các bộ đếm riêng biệt)

3. **Các tính năng bảo mật:**
   - Ngăn chặn phát lại (lưu cache các khóa tạm thời trong 2*D)
   - Xác minh dấu thời gian (mặc định ±60 giây)
   - Đệm ngẫu nhiên trong các thông điệp 1-2
   - Xử lý lỗi AEAD (Authenticated Encryption with Associated Data - mã hóa xác thực kèm dữ liệu) với thời gian chờ ngẫu nhiên

4. **Công bố RouterInfo:**
   - Công bố khóa tĩnh ("s"), IV ("i"), và phiên bản ("v")
   - Luân chuyển khóa theo chính sách
   - Hỗ trợ trường capabilities ("caps") cho router ẩn

5. **Khả năng tương thích mạng:**
   - Hỗ trợ trường Network ID (hiện là 2 đối với mainnet (mạng chính))
   - Tương tác liên thông với các triển khai Java và i2pd hiện có
   - Hỗ trợ cả IPv4 và IPv6

### Thực tiễn khuyến nghị

**Tối ưu hóa hiệu năng:**

1. **Chiến lược đệm:**
   - Xả toàn bộ thông điệp cùng lúc (thông điệp 1, 2, 3)
   - Sử dụng TCP_NODELAY cho các thông điệp bắt tay
   - Gộp nhiều khối dữ liệu vào các khung đơn
   - Giới hạn kích thước khung ở vài KB (giảm thiểu độ trễ phía nhận)

2. **Quản lý kết nối:**
   - Tái sử dụng các kết nối khi có thể
   - Triển khai connection pooling (bể kết nối)
   - Giám sát tình trạng kết nối (DateTime blocks - tình trạng bị chặn liên quan đến DateTime)

3. **Quản lý bộ nhớ:**
   - Xóa sạch dữ liệu nhạy cảm sau khi sử dụng (khóa tạm thời, kết quả DH (Diffie-Hellman))
   - Giới hạn số lượng bắt tay đồng thời (ngăn chặn DoS (tấn công từ chối dịch vụ))
   - Sử dụng pool bộ nhớ cho các lần cấp phát thường xuyên

**Tăng cường bảo mật:**

1. **Khả năng chống thăm dò:**
   - Thời gian chờ ngẫu nhiên: 100-500ms
   - Đọc byte ngẫu nhiên: 1KB-64KB
   - Đưa IP vào danh sách đen khi lỗi lặp lại
   - Không tiết lộ chi tiết lỗi cho các nút ngang hàng

2. **Giới hạn tài nguyên:**
   - Số kết nối tối đa trên mỗi IP: 3-10
   - Số bắt tay đang chờ tối đa: 100-1000
   - Thời gian chờ đọc: 30-60 giây mỗi thao tác
   - Tổng thời gian chờ kết nối: 5 phút cho quá trình bắt tay

3. **Quản lý khóa:**
   - Lưu trữ lâu dài khóa tĩnh và IV (vector khởi tạo)
   - Sinh số ngẫu nhiên an toàn (cryptographic RNG - bộ tạo số ngẫu nhiên mật mã)
   - Tuân thủ nghiêm ngặt các chính sách luân chuyển (rotation)
   - Không bao giờ tái sử dụng khóa tạm thời

**Giám sát và Chẩn đoán:**

1. **Chỉ số:**
   - Tỷ lệ thành công/thất bại của bắt tay
   - Tỷ lệ lỗi AEAD (mã hóa xác thực kèm dữ liệu)
   - Phân bố độ lệch đồng hồ
   - Thống kê thời lượng kết nối

2. **Ghi nhật ký:**
   - Ghi nhật ký các lỗi bắt tay kèm mã lý do
   - Ghi nhật ký các sự kiện lệch thời gian hệ thống
   - Ghi nhật ký các địa chỉ IP bị cấm
   - Tuyệt đối không ghi nhật ký dữ liệu khóa nhạy cảm

3. **Kiểm thử:**
   - Kiểm thử đơn vị cho các chuỗi KDF (hàm dẫn xuất khóa)
   - Kiểm thử tích hợp với các triển khai khác
   - Fuzzing (kiểm thử ngẫu nhiên) cho xử lý gói tin
   - Kiểm thử tải để đánh giá khả năng chống DoS (tấn công từ chối dịch vụ)

### Những cạm bẫy thường gặp

**Các lỗi nghiêm trọng cần tránh:**

1. **Tái sử dụng nonce (giá trị ngẫu nhiên dùng một lần):**
   - Không bao giờ đặt lại bộ đếm nonce giữa phiên
   - Sử dụng các bộ đếm riêng cho từng chiều
   - Kết thúc trước khi đạt tới 2^64 - 1

2. **Luân chuyển khóa:**
   - Không bao giờ luân chuyển khóa khi router đang chạy
   - Không bao giờ tái sử dụng khóa tạm thời giữa các phiên
   - Tuân theo các quy tắc về thời gian ngừng hoạt động tối thiểu

3. **Xử lý dấu thời gian:**
   - Không bao giờ chấp nhận dấu thời gian đã hết hạn
   - Luôn điều chỉnh theo RTT (thời gian khứ hồi) khi tính độ lệch
   - Làm tròn các dấu thời gian DateTime tới giây

4. **Lỗi AEAD:**
   - Không bao giờ tiết lộ loại lỗi cho kẻ tấn công
   - Luôn sử dụng thời gian chờ ngẫu nhiên trước khi đóng
   - Xử lý độ dài không hợp lệ giống như lỗi AEAD

5. **Phần đệm:**
   - Không bao giờ gửi phần đệm vượt ngoài các giới hạn đã thỏa thuận
   - Luôn đặt khối phần đệm ở vị trí cuối cùng
   - Không bao giờ có nhiều hơn một khối phần đệm trong mỗi khung

6. **RouterInfo (thông tin về router):**
   - Luôn xác minh khóa tĩnh khớp với RouterInfo
   - Không bao giờ phát tán RouterInfos mà không có địa chỉ đã được công bố
   - Luôn xác minh chữ ký

### Phương pháp luận kiểm thử

**Kiểm thử đơn vị:**

1. **Các nguyên thủy mật mã:**
   - Vector kiểm thử cho X25519, ChaCha20, Poly1305, SHA-256
   - Vector kiểm thử cho HMAC-SHA256
   - Vector kiểm thử cho SipHash-2-4

2. **Chuỗi KDF:**
   - Kiểm thử đáp án đã biết cho cả ba thông điệp
   - Xác minh sự lan truyền của khóa chuỗi
   - Kiểm tra việc sinh IV (vector khởi tạo) của SipHash

3. **Phân tích cú pháp thông điệp:**
   - Giải mã thông điệp hợp lệ
   - Từ chối thông điệp không hợp lệ
   - Điều kiện biên (rỗng, kích thước tối đa)

**Kiểm thử tích hợp:**

1. **Bắt tay:**
   - Trao đổi ba thông điệp thành công
   - Từ chối do lệch đồng hồ
   - Phát hiện tấn công phát lại
   - Từ chối khóa không hợp lệ

2. **Giai đoạn dữ liệu:**
   - Truyền thông điệp I2NP
   - Trao đổi RouterInfo
   - Xử lý padding (đệm)
   - Thông điệp kết thúc

3. **Khả năng tương tác:**
   - Kiểm thử khả năng tương tác với Java I2P
   - Kiểm thử khả năng tương tác với i2pd
   - Kiểm thử IPv4 và IPv6
   - Kiểm thử router công khai và ẩn

**Kiểm tra bảo mật:**

1. **Kiểm thử tiêu cực:**
   - Thẻ AEAD không hợp lệ
   - Thông điệp bị phát lại
   - Tấn công lệch đồng hồ
   - Khung sai định dạng

2. **Kiểm thử DoS:**
   - Làm ngập kết nối
   - Tấn công Slowloris
   - Làm cạn kiệt CPU (DH (Diffie-Hellman - trao đổi khóa Diffie–Hellman) quá mức)
   - Làm cạn kiệt bộ nhớ

3. **Fuzzing (kiểm thử ngẫu nhiên):**
   - Thông điệp bắt tay ngẫu nhiên
   - Các khung ở pha dữ liệu ngẫu nhiên
   - Các loại và kích thước khối ngẫu nhiên
   - Giá trị mật mã không hợp lệ

### Chuyển đổi từ NTCP (giao thức truyền tải dựa trên TCP của I2P cũ)

**Đối với hỗ trợ NTCP cũ (hiện đã bị loại bỏ):**

NTCP (phiên bản 1) đã được gỡ bỏ kể từ I2P 0.9.50 (tháng 5 năm 2021). Tất cả các bản triển khai hiện tại bắt buộc phải hỗ trợ NTCP2. Ghi chú lịch sử:

1. **Giai đoạn chuyển tiếp (2018-2021):**
   - 0.9.36: NTCP2 được giới thiệu (bị vô hiệu hóa theo mặc định)
   - 0.9.37: NTCP2 được kích hoạt theo mặc định
   - 0.9.40: NTCP bị đánh dấu là lỗi thời
   - 0.9.50: NTCP bị loại bỏ

2. **Phát hiện phiên bản:**
   - "NTCP" (giao thức dựa trên TCP của I2P) transportStyle cho biết cả hai phiên bản đều được hỗ trợ
   - "NTCP2" (phiên bản 2 của NTCP) transportStyle cho biết chỉ hỗ trợ NTCP2
   - Tự động phát hiện thông qua kích thước thông điệp (287 so với 288 byte)

3. **Trạng thái hiện tại:**
   - Tất cả routers phải hỗ trợ NTCP2
   - "NTCP" transportStyle (kiểu truyền tải) đã lỗi thời
   - Chỉ sử dụng "NTCP2" transportStyle

## Phụ lục A: Mẫu Noise XK

**Mẫu Noise XK tiêu chuẩn (một mẫu bắt tay trong bộ khung giao thức Noise):**

```
XK(s, rs):
  <- s
  ...
  -> e, es
  <- e, ee
  -> s, se
```
**Diễn giải:**

- `<-` : Thông điệp từ bên phản hồi (Bob) đến bên khởi tạo (Alice)
- `->` : Thông điệp từ bên khởi tạo (Alice) đến bên phản hồi (Bob)
- `s` : Khóa tĩnh (khóa danh tính dài hạn)
- `rs` : Khóa tĩnh từ xa (khóa tĩnh của đối tác, đã biết trước)
- `e` : Khóa tạm thời (cụ thể cho phiên, được tạo theo yêu cầu)
- `es` : DH tạm thời–tĩnh (Diffie-Hellman - trao đổi khóa; tạm thời của Alice × tĩnh của Bob)
- `ee` : DH tạm thời–tạm thời (tạm thời của Alice × tạm thời của Bob)
- `se` : DH tĩnh–tạm thời (tĩnh của Alice × tạm thời của Bob)

**Trình tự thỏa thuận khóa:**

1. **Tiền thông điệp:** Alice biết khóa công khai tĩnh của Bob (từ RouterInfo)
2. **Thông điệp 1:** Alice gửi khóa tạm thời, thực hiện es DH (ephemeral–static Diffie-Hellman)
3. **Thông điệp 2:** Bob gửi khóa tạm thời, thực hiện ee DH (ephemeral–ephemeral Diffie-Hellman)
4. **Thông điệp 3:** Alice tiết lộ khóa tĩnh, thực hiện se DH (static–ephemeral Diffie-Hellman)

**Thuộc tính bảo mật:**

- Alice đã xác thực: Có (ở thông điệp 3)
- Bob đã xác thực: Có (bằng việc sở hữu khóa riêng tĩnh)
- Bí mật chuyển tiếp: Có (các khóa tạm thời đã bị hủy)
- KCI resistance (khả năng kháng lại tấn công Key Compromise Impersonation): Có (mức xác thực 2)

## Phụ lục B: Mã hóa Base64

**Bảng chữ cái Base64 của I2P:**

```
ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-~
```
**Khác biệt so với Base64 tiêu chuẩn:** - Ký tự 62-63: `-~` thay vì `+/` - Phần đệm: Giống (`=`) hoặc lược bỏ tùy ngữ cảnh

**Cách sử dụng trong NTCP2:** - Khóa tĩnh ("s"): 32 byte → 44 ký tự (không có phần đệm) - IV ("i"): 16 byte → 24 ký tự (không có phần đệm)

**Ví dụ về mã hóa:**

```python
# 32-byte static key (hex): 
# f4489e1bb0597b39ca6cbf5ad9f5f1f09043e02d96cb9aa6a63742b3462429aa

# I2P Base64 encoded:
# 9EjeG7BZeznKbL9a2fXx8JBDPgLZbLmKbqY3QrNGJCo=
```
## Phụ lục C: Phân tích bắt gói tin

**Nhận diện lưu lượng NTCP2:**

1. **Bắt tay TCP:**
   - Chuẩn TCP SYN, SYN-ACK, ACK
   - Cổng đích thường là 8887 hoặc tương tự

2. **Thông điệp 1 (SessionRequest - yêu cầu phiên):**
   - Dữ liệu ứng dụng đầu tiên từ Alice
   - 80-65535 byte (thường là vài trăm)
   - Có vẻ ngẫu nhiên (khóa tạm thời được mã hóa bằng AES)
   - Tối đa 287 byte nếu kết nối tới địa chỉ "NTCP"

3. **Thông điệp 2 (SessionCreated):**
   - Phản hồi từ Bob
   - 80-65535 byte (thường là vài trăm)
   - Cũng có vẻ ngẫu nhiên

4. **Thông điệp 3 (SessionConfirmed):**
   - Từ Alice
   - 48 byte + phần biến thiên (kích thước RouterInfo (thông tin router trong I2P) + phần đệm)
   - Thường khoảng 1–4 KB

5. **Pha dữ liệu:**
   - Khung có độ dài biến thiên
   - Trường độ dài được làm rối (trông như ngẫu nhiên)
   - Phần tải tin được mã hóa
   - Đệm (padding) khiến kích thước khó dự đoán

**Tránh né DPI (kiểm tra gói sâu):** - Không có tiêu đề văn bản thuần - Không có mẫu cố định - Các trường độ dài được che giấu - Phần đệm ngẫu nhiên phá vỡ các heuristic dựa trên kích thước

**So sánh với NTCP:** - Thông điệp 1 của NTCP luôn có kích thước 288 byte (dễ nhận diện) - Kích thước thông điệp 1 của NTCP2 thay đổi (không thể nhận diện) - NTCP có các mẫu dễ nhận ra - NTCP2 được thiết kế để chống DPI (kiểm tra gói dữ liệu sâu)

## Phụ lục D: Lịch sử phiên bản

**Các cột mốc quan trọng:**

- **0.9.36** (23 tháng 8, 2018): NTCP2 được giới thiệu, tắt theo mặc định
- **0.9.37** (4 tháng 10, 2018): NTCP2 được bật theo mặc định
- **0.9.40** (20 tháng 5, 2019): NTCP được đánh dấu lỗi thời
- **0.9.42** (27 tháng 8, 2019): Trường Network ID (mã mạng) được thêm (Đề xuất 147)
- **0.9.50** (17 tháng 5, 2021): NTCP được gỡ bỏ, bổ sung hỗ trợ capabilities (các khả năng)
- **2.10.0** (9 tháng 9, 2025): Bản phát hành ổn định mới nhất

**Tính ổn định giao thức:** - Không có thay đổi không tương thích ngược kể từ 0.9.50 - Các cải tiến liên tục nhằm tăng khả năng chống thăm dò - Tập trung vào hiệu năng và độ tin cậy - Mật mã hậu lượng tử đang được phát triển (không bật theo mặc định)

**Trạng thái truyền tải hiện tại:** - NTCP2: Giao thức truyền tải TCP bắt buộc - SSU2: Giao thức truyền tải UDP bắt buộc - NTCP (v1): Đã loại bỏ - SSU (v1): Đã loại bỏ
