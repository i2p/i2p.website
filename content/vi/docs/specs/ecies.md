---
title: "Đặc tả mã hóa ECIES-X25519-AEAD-Ratchet (cơ chế bánh cóc)"
description: "Lược đồ mã hóa tích hợp dựa trên đường cong elliptic cho I2P (X25519 + AEAD)"
slug: "ecies"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
toc: true
---

## Tổng quan

### Mục đích

ECIES-X25519-AEAD-Ratchet là giao thức mã hóa đầu-cuối hiện đại của I2P, thay thế hệ thống ElGamal/AES+SessionTags cũ. Nó cung cấp tính bí mật chuyển tiếp, mã hóa xác thực, và những cải tiến đáng kể về hiệu năng và bảo mật.

### Những cải tiến chính so với ElGamal/AES+SessionTags

- **Khóa nhỏ hơn**: Khóa 32-byte so với khóa công khai ElGamal 256-byte (giảm 87.5%)
- **Bảo mật chuyển tiếp**: Đạt được thông qua DH ratcheting (cơ chế bánh cóc) (không có trong giao thức cũ)
- **Mật mã hiện đại**: X25519 DH, ChaCha20-Poly1305 AEAD, SHA-256
- **Mã hóa kèm xác thực**: Xác thực tích hợp thông qua cấu trúc AEAD
- **Giao thức hai chiều**: Các phiên vào/ra được ghép cặp so với giao thức cũ một chiều
- **Thẻ phiên hiệu quả**: Thẻ phiên 8-byte so với thẻ 32-byte (giảm 75%)
- **Che giấu lưu lượng**: Mã hóa Elligator2 khiến các bắt tay không thể phân biệt với dữ liệu ngẫu nhiên

### Trạng thái triển khai

- **Phát hành ban đầu**: Phiên bản 0.9.46 (25 tháng 5, 2020)
- **Triển khai mạng**: Hoàn tất tính đến năm 2020
- **Trạng thái hiện tại**: Trưởng thành, được triển khai rộng rãi (hơn 5 năm trong môi trường sản xuất)
- **Hỗ trợ router**: Yêu cầu phiên bản 0.9.46 hoặc cao hơn
- **Yêu cầu Floodfill**: Mức độ áp dụng gần 100% cho các tra cứu được mã hóa

### Trạng thái triển khai

**Đã triển khai đầy đủ:** - các thông điệp New Session (NS) có ràng buộc - các thông điệp New Session Reply (NSR) - các thông điệp Existing Session (ES) - cơ chế DH ratchet (cơ chế thay đổi khóa tăng dần) - các ratchet cho session tag (thẻ phiên) và khóa đối xứng - các khối DateTime, NextKey, ACK, ACK Request, Garlic Clove (nhánh tỏi - thành phần của thông điệp 'garlic' trong I2P), và Padding

**Chưa được triển khai (tính đến phiên bản 0.9.50):** - khối MessageNumbers (loại 6) - khối Options (loại 5) - khối Termination (loại 4) - phản hồi tự động ở tầng giao thức - Zero static key mode (chế độ không dùng khóa tĩnh) - các phiên multicast

**Lưu ý**: Tình trạng triển khai cho các phiên bản từ 1.5.0 đến 2.10.0 (2021–2025) cần được xác minh vì có thể một số tính năng đã được bổ sung.

---

## Nền tảng giao thức

### Khung giao thức Noise

ECIES-X25519-AEAD-Ratchet dựa trên [Noise Protocol Framework](https://noiseprotocol.org/) (Bản sửa đổi 34, 2018-07-11), cụ thể là mẫu bắt tay **IK** (tương tác, khóa tĩnh từ xa đã biết) với các phần mở rộng dành riêng cho I2P.

### Định danh Giao thức Noise

```
Noise_IKelg2+hs2_25519_ChaChaPoly_SHA256
```
**Các thành phần định danh:** - `Noise` - Khung cơ bản - `IK` - Mẫu bắt tay tương tác với khóa tĩnh từ xa đã biết - `elg2` - Mã hóa Elligator2 cho khóa tạm thời (phần mở rộng I2P) - `+hs2` - MixHash được gọi trước thông điệp thứ hai để trộn tag (phần mở rộng I2P) - `25519` - Hàm Diffie-Hellman X25519 - `ChaChaPoly` - Thuật toán mã hóa AEAD ChaCha20-Poly1305 - `SHA256` - Hàm băm SHA-256

### Mẫu bắt tay Noise

**Ký hiệu mẫu IK:**

```
<- s                    (Bob's static key known to Alice)
...
-> e, es, s, ss         (Alice sends ephemeral, DH es, static key, DH ss)
<- e, ee, se            (Bob sends ephemeral, DH ee, DH se)
```
**Ý nghĩa các token:** - `e` - Truyền khóa tạm thời - `s` - Truyền khóa tĩnh - `es` - DH giữa khóa tạm thời của Alice và khóa tĩnh của Bob - `ss` - DH giữa khóa tĩnh của Alice và khóa tĩnh của Bob - `ee` - DH giữa khóa tạm thời của Alice và khóa tạm thời của Bob - `se` - DH giữa khóa tĩnh của Bob và khóa tạm thời của Alice

### Các thuộc tính bảo mật của Noise (khung giao thức mật mã)

Sử dụng thuật ngữ của Noise (khung giao thức mật mã), mẫu IK cung cấp:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Message</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Authentication Level</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Confidentiality Level</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Message&nbsp;1 (NS)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Level&nbsp;1 (sender auth, KCI vulnerable)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Level&nbsp;2 (weak forward secrecy)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Message&nbsp;2 (NSR)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Level&nbsp;2 (mutual auth)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Level&nbsp;4 (weak forward secrecy)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Transport (ES)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Level&nbsp;2 (mutual auth)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Level&nbsp;5 (strong forward secrecy)</td>
    </tr>
  </tbody>
</table>
**Các cấp độ xác thực:** - **Cấp 1**: Tải dữ liệu được xác thực là thuộc về chủ sở hữu khóa tĩnh của bên gửi, nhưng dễ bị tấn công Key Compromise Impersonation (KCI, mạo danh do lộ khóa) - **Cấp 2**: Kháng các cuộc tấn công KCI sau NSR

**Các cấp độ bảo mật:** - **Cấp 2**: Bí mật chuyển tiếp (forward secrecy) nếu khóa tĩnh của người gửi bị xâm phạm về sau - **Cấp 4**: Bí mật chuyển tiếp nếu khóa tạm thời của người gửi bị xâm phạm về sau - **Cấp 5**: Bí mật chuyển tiếp đầy đủ sau khi cả hai khóa tạm thời được xóa

### Sự khác biệt giữa IK và XK

Mẫu IK khác với mẫu XK được dùng trong NTCP2 và SSU2:

1. **Bốn phép DH (Diffie-Hellman)**: IK sử dụng 4 phép DH (es, ss, ee, se) so với 3 trong XK
2. **Xác thực ngay lập tức**: Alice được xác thực trong thông điệp đầu tiên (Mức xác thực 1)
3. **Bảo mật chuyển tiếp nhanh hơn**: Bảo mật chuyển tiếp đầy đủ (Mức 5) đạt được sau thông điệp thứ hai (1-RTT)
4. **Đánh đổi**: Tải trọng của thông điệp đầu tiên không có bảo mật chuyển tiếp (so với XK, nơi mọi tải trọng đều có bảo mật chuyển tiếp)

**Tóm tắt**: IK (một mẫu bắt tay) cho phép phản hồi của Bob được nhận chỉ trong 1-RTT (một vòng khứ hồi) với đầy đủ bảo mật chuyển tiếp, đổi lại yêu cầu ban đầu không có bảo mật chuyển tiếp.

### Các khái niệm về Double Ratchet (cơ chế bánh cóc kép) của Signal

ECIES (lược đồ mã hóa tích hợp trên đường cong elliptic) kết hợp các khái niệm từ [Signal Double Ratchet Algorithm](https://signal.org/docs/specifications/doubleratchet/):

- **DH Ratchet**: (cơ chế bánh cóc DH) Đảm bảo bí mật chuyển tiếp bằng cách trao đổi định kỳ các khóa DH mới
- **Symmetric Key Ratchet**: (cơ chế bánh cóc khóa đối xứng) Dẫn xuất các khóa phiên mới cho mỗi thông điệp
- **Session Tag Ratchet**: (cơ chế bánh cóc Session Tag) Tạo session tags (thẻ phiên) dùng một lần một cách tất định

**Những khác biệt chính so với Signal:** - **Ratcheting (cơ chế tăng tiến khóa theo từng bước) ít thường xuyên hơn**: I2P chỉ thực hiện ratchet khi cần (gần cạn tag hoặc theo chính sách) - **Session Tags (thẻ phiên) thay cho mã hóa tiêu đề**: Sử dụng các tag có tính xác định thay vì các tiêu đề được mã hóa - **ACK rõ ràng**: Sử dụng các khối ACK trong-băng thay vì chỉ dựa vào lưu lượng ngược chiều - **Tách biệt ratchet cho tag và khóa**: Hiệu quả hơn cho bên nhận (có thể hoãn việc tính toán khóa)

### Các phần mở rộng I2P cho Noise (khung giao thức)

1. **Mã hóa Elligator2**: Khóa tạm thời được mã hóa để không thể phân biệt với dữ liệu ngẫu nhiên
2. **Thẻ được chèn ở đầu NSR**: Thẻ phiên được thêm trước thông điệp NSR để phục vụ mục đích tương quan
3. **Định dạng tải tin được xác định**: Cấu trúc tải tin dạng khối cho mọi loại thông điệp
4. **Bao gói I2NP**: Tất cả thông điệp được bọc trong các tiêu đề Thông điệp Garlic của I2NP
5. **Giai đoạn dữ liệu tách biệt**: Thông điệp truyền tải (ES) khác với giai đoạn dữ liệu tiêu chuẩn của Noise (khung giao thức mật mã)

---

## Các nguyên thủy mật mã

### Trao đổi khóa Diffie-Hellman X25519

**Đặc tả**: [RFC 7748](https://tools.ietf.org/html/rfc7748)

**Thuộc tính chính:** - **Kích thước khóa riêng**: 32 byte - **Kích thước khóa công khai**: 32 byte - **Kích thước bí mật chung**: 32 byte - **Thứ tự byte**: Little-endian - **Đường cong**: Curve25519

**Vận hành:**

### X25519 GENERATE_PRIVATE()

Tạo một khóa riêng 32 byte ngẫu nhiên:

```
privkey = CSRNG(32)
```
### X25519 DERIVE_PUBLIC(privkey)

Suy ra khóa công khai tương ứng:

```
pubkey = curve25519_scalarmult_base(privkey)
```
Trả về khóa công khai 32 byte ở dạng little-endian (thứ tự byte nhỏ trước).

### X25519 DH(privkey, pubkey)

Thực hiện Diffie-Hellman key agreement (thỏa thuận khóa Diffie-Hellman):

```
sharedSecret = curve25519_scalarmult(privkey, pubkey)
```
Trả về một bí mật dùng chung dài 32 byte.

**Ghi chú bảo mật**: Người triển khai phải xác minh rằng bí mật chia sẻ không phải toàn là số 0 (khóa yếu). Hãy từ chối và hủy bỏ quá trình bắt tay nếu điều này xảy ra.

### ChaCha20-Poly1305 AEAD (mã hóa xác thực kèm dữ liệu)

**Đặc tả**: [RFC 7539](https://tools.ietf.org/html/rfc7539) mục 2.8

**Tham số:** - **Kích thước khóa**: 32 byte (256 bit) - **Kích thước Nonce (số dùng một lần)**: 12 byte (96 bit) - **Kích thước MAC**: 16 byte (128 bit) - **Kích thước khối**: 64 byte (nội bộ)

**Định dạng Nonce (số dùng một lần):**

```
Byte 0-3:   0x00 0x00 0x00 0x00  (always zero)
Byte 4-11:  Little-endian counter (message number N)
```
**Cấu trúc AEAD:**

AEAD (mã hóa xác thực kèm dữ liệu liên kết) kết hợp mật mã dòng ChaCha20 với MAC Poly1305:

1. Tạo luồng khóa ChaCha20 từ khóa và nonce (số dùng một lần)
2. Mã hóa bản rõ bằng cách XOR với luồng khóa
3. Tính MAC (mã xác thực thông điệp) Poly1305 trên (dữ liệu liên kết || bản mã)
4. Thêm MAC 16 byte vào bản mã

### ChaCha20-Poly1305 MÃ HÓA(k, n, plaintext, ad)

Mã hóa bản rõ kèm xác thực:

```python
# Inputs
k = 32-byte cipher key
n = 12-byte nonce (first 4 bytes zero, last 8 bytes = message number)
plaintext = data to encrypt (0 to 65519 bytes)
ad = associated data (optional, used in MAC calculation)

# Output
ciphertext = chacha20_encrypt(k, n, plaintext)
mac = poly1305(ad || ciphertext, poly1305_key_gen(k, n))
return ciphertext || mac  # Total length = len(plaintext) + 16
```
**Thuộc tính:** - Bản mã có cùng độ dài với bản rõ (mật mã dòng) - Đầu ra là plaintext_length + 16 byte (bao gồm MAC) - Toàn bộ đầu ra không thể phân biệt với ngẫu nhiên nếu khóa được giữ bí mật - MAC xác thực cả dữ liệu liên kết và bản mã

### ChaCha20-Poly1305 DECRYPT(k, n, ciphertext, ad)

Giải mã và kiểm tra xác thực:

```python
# Split ciphertext and MAC
ct_without_mac = ciphertext[0:-16]
received_mac = ciphertext[-16:]

# Verify MAC
expected_mac = poly1305(ad || ct_without_mac, poly1305_key_gen(k, n))
if not constant_time_compare(received_mac, expected_mac):
    raise AuthenticationError("MAC verification failed")

# Decrypt
plaintext = chacha20_decrypt(k, n, ct_without_mac)
return plaintext
```
**Các yêu cầu bảo mật quan trọng:** - Nonces (giá trị dùng một lần) PHẢI là duy nhất cho mỗi thông điệp dùng cùng một khóa - Nonces KHÔNG ĐƯỢC tái sử dụng (hậu quả thảm khốc nếu tái sử dụng) - Việc kiểm tra MAC (mã xác thực thông điệp) PHẢI sử dụng so sánh thời gian cố định để ngăn chặn các cuộc tấn công dựa trên thời gian - Việc kiểm tra MAC thất bại PHẢI dẫn đến việc từ chối toàn bộ thông điệp (không có giải mã từng phần)

### Hàm băm SHA-256

**Đặc tả**: NIST FIPS 180-4

**Thuộc tính:** - **Kích thước đầu ra**: 32 byte (256 bit) - **Kích thước khối**: 64 byte (512 bit) - **Mức độ bảo mật**: 128 bit (khả năng chống va chạm)

**Vận hành:**

### SHA-256 H(p, d)

Mã băm SHA-256 với chuỗi cá nhân hóa:

```
H(p, d) := SHA256(p || d)
```
Trong đó `||` biểu thị phép nối (concatenation), `p` là chuỗi cá nhân hóa (personalization string), `d` là dữ liệu.

### SHA-256 MixHash(d)

Cập nhật giá trị băm hiện tại với dữ liệu mới:

```
h = SHA256(h || d)
```
Được sử dụng xuyên suốt Noise handshake (quá trình bắt tay của giao thức Noise) để duy trì transcript hash (hàm băm bản ghi bắt tay).

### Dẫn xuất khóa HKDF

**Đặc tả**: [RFC 5869](https://tools.ietf.org/html/rfc5869)

**Mô tả**: Hàm dẫn xuất khóa dựa trên HMAC sử dụng SHA-256

**Tham số:** - **Hàm băm**: HMAC-SHA256 - **Độ dài salt (chuỗi ngẫu nhiên)**: Tối đa 32 byte (kích thước đầu ra SHA-256) - **Độ dài đầu ra**: Biến thiên (tối đa 255 * 32 byte)

**Hàm HKDF (hàm dẫn xuất khóa dựa trên HMAC):**

```python
def HKDF(salt, ikm, info, length):
    """
    Args:
        salt: Salt value (32 bytes max for SHA-256)
        ikm: Input key material (any length)
        info: Context-specific info string
        length: Desired output length in bytes
    
    Returns:
        output: Derived key material (length bytes)
    """
    # Extract phase
    prk = HMAC-SHA256(salt, ikm)
    
    # Expand phase
    n = ceil(length / 32)
    t = b''
    okm = b''
    for i in range(1, n + 1):
        t = HMAC-SHA256(prk, t || info || byte(i))
        okm = okm || t
    
    return okm[0:length]
```
**Các mẫu sử dụng phổ biến:**

```python
# Generate two keys (64 bytes total)
keydata = HKDF(chainKey, sharedSecret, "KDFDHRatchetStep", 64)
nextRootKey = keydata[0:31]
chainKey = keydata[32:63]

# Generate session tag (8 bytes)
tagdata = HKDF(chainKey, CONSTANT, "SessionTagKeyGen", 64)
nextChainKey = tagdata[0:31]
sessionTag = tagdata[32:39]

# Generate symmetric key (32 bytes)
keydata = HKDF(chainKey, ZEROLEN, "SymmetricRatchet", 64)
nextChainKey = keydata[0:31]
sessionKey = keydata[32:63]
```
**Chuỗi thông tin dùng trong ECIES:** - `"KDFDHRatchetStep"` - dẫn xuất khóa cho DH ratchet (cơ chế bánh cóc) - `"TagAndKeyGenKeys"` - khởi tạo các khóa của chuỗi thẻ và chuỗi khóa - `"STInitialization"` - khởi tạo ratchet thẻ phiên - `"SessionTagKeyGen"` - sinh thẻ phiên - `"SymmetricRatchet"` - sinh khóa đối xứng - `"XDHRatchetTagSet"` - khóa tập thẻ cho DH ratchet - `"SessionReplyTags"` - sinh tập thẻ NSR - `"AttachPayloadKDF"` - dẫn xuất khóa payload NSR

### Mã hóa Elligator2

**Mục đích**: Mã hóa các khóa công khai X25519 để chúng không thể phân biệt được với các chuỗi 32 byte ngẫu nhiên phân phối đều.

**Đặc tả**: [Bài báo Elligator2](https://elligator.cr.yp.to/elligator-20130828.pdf)

**Vấn đề**: Các khóa công khai X25519 (thuật toán trao đổi khóa trên đường cong elliptic) tiêu chuẩn có cấu trúc dễ nhận diện. Một người quan sát có thể nhận diện các thông điệp bắt tay bằng cách phát hiện các khóa này, ngay cả khi nội dung được mã hóa.

**Giải pháp**: Elligator2 cung cấp một ánh xạ song ánh giữa ~50% số khóa công khai X25519 hợp lệ và các chuỗi 254-bit trông như ngẫu nhiên.

**Sinh khóa với Elligator2 (kỹ thuật ẩn dạng khóa công khai):**

### Elligator2 GENERATE_PRIVATE_ELG2()

Tạo một khóa riêng tương ứng với một khóa công khai có thể mã hóa theo Elligator2 (kỹ thuật ẩn dạng khóa công khai):

```python
while True:
    privkey = CSRNG(32)
    pubkey = DERIVE_PUBLIC(privkey)
    
    # Test if public key is Elligator2-encodable
    try:
        encoded = ENCODE_ELG2(pubkey)
        # Success - this key pair is suitable
        return privkey
    except NotEncodableError:
        # Try again with new random key
        continue
```
**Quan trọng**: Khoảng 50% khóa riêng được tạo ngẫu nhiên sẽ tạo ra khóa công khai không thể mã hóa. Những khóa đó phải được loại bỏ và thử tạo lại.

**Tối ưu hóa hiệu năng**: Tạo khóa trước trong một luồng nền để duy trì một pool (tập hợp dự trữ) các cặp khóa phù hợp, tránh độ trễ trong quá trình bắt tay.

### Elligator2 ENCODE_ELG2(pubkey)

Mã hóa một khóa công khai thành 32 byte trông ngẫu nhiên:

```python
def ENCODE_ELG2(pubkey):
    """
    Encodes X25519 public key using Elligator2.
    
    Args:
        pubkey: 32-byte X25519 public key (little-endian)
    
    Returns:
        encoded: 32-byte encoded key indistinguishable from random
    
    Raises:
        NotEncodableError: If pubkey cannot be encoded
    """
    # Perform Elligator2 representative calculation
    # Returns 254-bit value (31.75 bytes)
    encodedKey = elligator2_encode(pubkey)
    
    # Add 2 random bits to MSB to make full 32 bytes
    randomByte = CSRNG(1)
    encodedKey[31] |= (randomByte & 0xc0)
    
    return encodedKey
```
**Chi tiết mã hóa:** - Elligator2 (kỹ thuật ánh xạ điểm trên đường cong elliptic thành chuỗi byte trông ngẫu nhiên) tạo ra 254 bit (không đủ 256) - 2 bit cao nhất của byte 31 là phần đệm ngẫu nhiên - Kết quả được phân bố đều trên toàn bộ không gian 32 byte - Mã hóa thành công khoảng 50% khóa công khai X25519 (thuật toán trao đổi khóa ECDH trên Curve25519) hợp lệ

### Elligator2 DECODE_ELG2(encodedKey)

Giải mã trở lại khóa công khai ban đầu:

```python
def DECODE_ELG2(encodedKey):
    """
    Decodes Elligator2-encoded key back to X25519 public key.
    
    Args:
        encodedKey: 32-byte encoded key
    
    Returns:
        pubkey: 32-byte X25519 public key (little-endian)
    """
    # Mask out 2 random padding bits from MSB
    encodedKey[31] &= 0x3f
    
    # Perform Elligator2 representative inversion
    pubkey = elligator2_decode(encodedKey)
    
    return pubkey
```
**Thuộc tính bảo mật:** - Các khóa được mã hóa không thể phân biệt được về mặt tính toán so với các byte ngẫu nhiên - Không có phép kiểm định thống kê nào có thể phát hiện một cách đáng tin cậy các khóa được mã hóa theo Elligator2 (kỹ thuật ánh xạ giúp biểu diễn khóa trông như ngẫu nhiên) - Giải mã là tất định (cùng một khóa đã mã hóa luôn tạo ra cùng một khóa công khai) - Việc mã hóa là song ánh đối với khoảng ~50% số khóa thuộc tập con có thể mã hóa

**Ghi chú triển khai:** - Lưu các khóa đã mã hóa trong giai đoạn tạo sinh để tránh mã hóa lại trong lúc bắt tay - Các khóa không phù hợp từ quá trình tạo bằng Elligator2 (kỹ thuật ẩn dạng khóa công khai) vẫn có thể dùng cho NTCP2 (không yêu cầu Elligator2) - Tạo khóa chạy nền là thiết yếu cho hiệu năng - Thời gian tạo trung bình tăng gấp đôi do tỷ lệ loại bỏ 50%

---

## Định dạng thông điệp

### Tổng quan

ECIES (lược đồ mã hóa tích hợp trên đường cong elliptic) định nghĩa ba loại thông điệp:

1. **New Session (NS)** (Phiên mới): Thông điệp bắt tay ban đầu từ Alice đến Bob
2. **New Session Reply (NSR)** (Phản hồi phiên mới): Phản hồi bắt tay của Bob gửi cho Alice
3. **Existing Session (ES)** (Phiên hiện có): Tất cả các thông điệp tiếp theo ở cả hai chiều

Tất cả thông điệp đều được đóng gói theo định dạng I2NP Garlic Message với các lớp mã hóa bổ sung.

### Bộ chứa thông điệp Garlic của I2NP

Tất cả các thông điệp ECIES (lược đồ mã hóa tích hợp dùng đường cong elliptic) đều được bọc trong các header tiêu chuẩn của I2NP Garlic Message:

```
+----+----+----+----+----+----+----+----+
|type|      msg_id       |  expiration   |
+----+----+----+----+----+----+----+----+
                         |  size   |chks|
+----+----+----+----+----+----+----+----+
|      length       |                   |
+----+----+----+----+                   +
|          encrypted data               |
~                                       ~
```
**Trường:** - `type`: 0x26 (Garlic Message, thông điệp Garlic) - `msg_id`: ID thông điệp I2NP 4 byte - `expiration`: dấu thời gian Unix 8 byte (mili giây) - `size`: kích thước payload 2 byte - `chks`: checksum 1 byte - `length`: độ dài dữ liệu đã mã hóa 4 byte - `encrypted data`: payload được mã hóa bằng ECIES

**Mục đích**: Cung cấp nhận dạng thông điệp và định tuyến ở tầng I2NP. Trường `length` cho phép bên nhận biết được tổng kích thước tải trọng đã mã hóa.

### Thông điệp Phiên mới (NS)

Thông điệp New Session (thông điệp mở phiên) khởi tạo một phiên mới từ Alice đến Bob. Nó có ba biến thể:

1. **Có ràng buộc** (1b): Bao gồm khóa tĩnh của Alice để giao tiếp hai chiều
2. **Không ràng buộc** (1c): Không kèm khóa tĩnh để giao tiếp một chiều
3. **Dùng một lần** (1d): Chế độ một thông điệp, không thiết lập phiên

### Thông điệp NS có ràng buộc (Loại 1b)

**Trường hợp sử dụng**: Truyền phát, datagram (gói dữ liệu không kết nối) có thể phản hồi, bất kỳ giao thức nào yêu cầu phản hồi

**Tổng độ dài**: 96 + payload_length byte

**Định dạng**:

```
+----+----+----+----+----+----+----+----+
|                                       |
+                                       +
|   New Session Ephemeral Public Key    |
+             32 bytes                  +
|     Encoded with Elligator2           |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+         Static Key Section            +
|       ChaCha20 encrypted data         |
+            32 bytes                   +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+    (MAC) for Static Key Section       +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+
|                                       |
+            Payload Section            +
|       ChaCha20 encrypted data         |
~          Variable length              ~
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+         (MAC) for Payload Section     +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+
```
**Chi tiết trường:**

**Khóa công khai tạm thời** (32 byte, dạng rõ): - Khóa công khai X25519 sử dụng một lần của Alice - Được mã hóa bằng Elligator2 (không thể phân biệt với ngẫu nhiên) - Được tạo mới cho mỗi thông điệp NS (không bao giờ tái sử dụng) - Định dạng little-endian

**Phần Khóa Tĩnh** (mã hóa 32 byte, 48 byte kèm MAC): - Chứa khóa công khai tĩnh X25519 của Alice (32 byte) - Được mã hóa bằng ChaCha20 - Được xác thực bằng Poly1305 MAC (16 byte) - Được Bob dùng để ràng buộc phiên với đích (destination) của Alice

**Phần Payload** (mã hóa có độ dài biến đổi, +16 byte MAC): - Chứa các garlic cloves (đơn vị thông điệp trong I2P) và các khối khác - Phải bao gồm khối DateTime là khối đầu tiên - Thường bao gồm các khối Garlic Clove chứa dữ liệu ứng dụng - Có thể bao gồm khối NextKey cho ratchet ngay lập tức (cơ chế cập nhật khóa) - Mã hóa bằng ChaCha20 - Xác thực bằng Poly1305 MAC (16 byte)

**Thuộc tính bảo mật:** - Khóa tạm thời cung cấp thành phần đảm bảo bí mật chuyển tiếp - Khóa tĩnh xác thực Alice (ràng buộc với đích) - Cả hai phần đều có MAC riêng để tách miền (domain separation) - Toàn bộ quy trình bắt tay thực hiện 2 phép toán DH (es, ss)

### Thông điệp NS không có ràng buộc (Loại 1c)

**Trường hợp sử dụng**: Các datagram thô (gói tin không kết nối) trong đó không kỳ vọng hoặc không mong muốn phản hồi

**Tổng độ dài**: 96 + payload_length byte

**Định dạng**:

```
+----+----+----+----+----+----+----+----+
|                                       |
+                                       +
|   New Session Ephemeral Public Key    |
+             32 bytes                  +
|     Encoded with Elligator2           |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+           Flags Section               +
|       ChaCha20 encrypted data         |
+            32 bytes                   +
|           All zeros                   |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+         (MAC) for above section       +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+
|                                       |
+            Payload Section            +
|       ChaCha20 encrypted data         |
~          Variable length              ~
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+         (MAC) for Payload Section     +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+
```
**Khác biệt chính**: Phần Flags chứa 32 byte toàn số 0 thay vì khóa tĩnh.

**Phát hiện**: Bob xác định loại thông điệp bằng cách giải mã phần 32 byte và kiểm tra xem tất cả các byte có bằng 0 hay không: - Tất cả các byte bằng 0 → phiên không ràng buộc (loại 1c) - Khác 0 → phiên ràng buộc với khóa tĩnh (loại 1b)

**Thuộc tính:** - Không có khóa tĩnh đồng nghĩa không ràng buộc với đích của Alice - Bob không thể gửi phản hồi (không biết đích) - Chỉ thực hiện 1 phép toán DH (Diffie–Hellman) (es) - Theo mẫu Noise "N" thay vì "IK" - Hiệu quả hơn khi không bao giờ cần phản hồi

**Phần cờ** (dành cho sử dụng trong tương lai): Hiện tại tất cả là 0. Có thể được dùng để thương lượng tính năng trong các phiên bản tương lai.

### Thông điệp NS dùng một lần (Loại 1d)

**Trường hợp sử dụng**: Thông điệp ẩn danh đơn lẻ không kỳ vọng phiên hoặc phản hồi

**Tổng độ dài**: 96 + payload_length byte

**Định dạng**: Giống hệt NS không có ràng buộc (loại 1c)

**Phân biệt**:  - Type 1c có thể gửi nhiều thông điệp trong cùng một phiên (các thông điệp ES theo sau) - Type 1d gửi đúng một thông điệp mà không thiết lập phiên - Trên thực tế, các triển khai có thể coi chúng giống hệt nhau ban đầu

**Thuộc tính:** - Ẩn danh tối đa (không có khóa tĩnh, không có phiên) - Không bên nào lưu giữ trạng thái phiên - Tuân theo mẫu "N" của Noise (bộ khung giao thức mật mã) - Một phép DH (es)

### Thông điệp Phản hồi Phiên Mới (NSR)

Bob gửi một hoặc nhiều thông điệp NSR (thông điệp 'Session Created') để đáp lại thông điệp NS (thông điệp 'Session Request') của Alice. NSR hoàn tất thủ tục bắt tay Noise IK (mẫu bắt tay IK trong giao thức Noise) và thiết lập một phiên giao tiếp hai chiều.

**Tổng độ dài**: 72 + payload_length byte

**Định dạng**:

```
+----+----+----+----+----+----+----+----+
|       Session Tag   8 bytes           |
+----+----+----+----+----+----+----+----+
|                                       |
+        Ephemeral Public Key           +
|                                       |
+            32 bytes                   +
|     Encoded with Elligator2           |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+  (MAC) for Key Section (empty)        +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+
|                                       |
+            Payload Section            +
|       ChaCha20 encrypted data         |
~          Variable length              ~
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+         (MAC) for Payload Section     +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+
```
**Chi tiết trường:**

**Thẻ phiên** (8 byte, bản rõ):
- Được tạo từ bộ thẻ NSR (xem các phần KDF)
- Liên kết phản hồi này với thông điệp NS của Alice
- Cho phép Alice xác định NS nào mà NSR này phản hồi
- Chỉ dùng một lần (không bao giờ tái sử dụng)

**Khóa công khai tạm thời** (32 byte, dạng rõ): - Khóa công khai X25519 dùng một lần của Bob - Được mã hóa (biểu diễn) bằng Elligator2 (kỹ thuật ánh xạ ngụy trang khóa công khai thành dữ liệu trông như ngẫu nhiên) - Được tạo mới cho mỗi thông điệp NSR - Phải khác nhau cho mỗi NSR được gửi

**Key Section MAC** (16 byte): - Xác thực dữ liệu rỗng (ZEROLEN) - Là một phần của giao thức Noise IK (mẫu se) - Sử dụng hash transcript (bản ghi băm) làm dữ liệu liên kết - Tối quan trọng để ràng buộc NSR với NS

**Phần tải** (độ dài biến đổi): - Chứa garlic cloves (các thành phần con trong thông điệp garlic) và các khối - Thường bao gồm các phản hồi ở tầng ứng dụng - Có thể để trống (ACK-only NSR) - Kích thước tối đa: 65519 byte (65535 - 16 byte MAC)

**Nhiều thông điệp NSR:**

Bob có thể gửi nhiều thông điệp NSR để đáp lại một NS: - Mỗi NSR có khóa tạm thời duy nhất - Mỗi NSR có thẻ phiên duy nhất - Alice sử dụng NSR đầu tiên nhận được để hoàn tất bắt tay - Các NSR còn lại là dự phòng (trong trường hợp mất gói)

**Thời điểm then chốt:** - Alice phải nhận được một NSR trước khi gửi các thông điệp ES - Bob phải nhận được một thông điệp ES trước khi gửi các thông điệp ES - NSR thiết lập các khóa phiên song hướng thông qua thao tác split()

**Thuộc tính bảo mật:** - Hoàn tất Noise IK handshake (thủ tục bắt tay Noise IK) - Thực hiện thêm 2 phép toán DH (Diffie-Hellman) (ee, se) - Tổng cộng 4 phép toán DH trên NS+NSR - Đạt xác thực lẫn nhau (Cấp 2) - Cung cấp bảo mật chuyển tiếp yếu (Cấp 4) cho payload NSR

### Thông điệp Phiên hiện có (ES)

Tất cả các thông điệp sau NS/NSR handshake (bắt tay NS/NSR) sử dụng Existing Session format (định dạng Phiên hiện có). ES messages (các thông điệp ES) được sử dụng hai chiều bởi cả Alice và Bob.

**Tổng độ dài**: 8 + payload_length + 16 byte (tối thiểu 24 byte)

**Định dạng**:

```
+----+----+----+----+----+----+----+----+
|       Session Tag   8 bytes           |
+----+----+----+----+----+----+----+----+
|                                       |
+            Payload Section            +
|       ChaCha20 encrypted data         |
~          Variable length              ~
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+              (MAC)                    +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+
```
**Chi tiết trường:**

**Thẻ phiên (Session Tag)** (8 byte, bản rõ): - Được tạo từ tập thẻ gửi đi hiện tại - Xác định phiên và số thông điệp - Bên nhận tra cứu thẻ để tìm khóa phiên và nonce (giá trị dùng một lần) - Chỉ dùng một lần (mỗi thẻ được dùng đúng một lần) - Định dạng: 8 byte đầu tiên của đầu ra HKDF

**Phần tải** (độ dài thay đổi): - Chứa các garlic cloves (thông điệp con trong mô hình garlic) và các khối - Không có khối bắt buộc (có thể rỗng) - Các khối thường gặp: Garlic Clove, NextKey, ACK, ACK Request, Padding - Kích thước tối đa: 65519 byte (65535 - 16 byte MAC)

**MAC** (16 bytes): - Thẻ xác thực Poly1305 - Được tính trên toàn bộ payload - Dữ liệu liên kết: thẻ phiên 8-byte - Phải được xác minh chính xác; nếu không, thông điệp sẽ bị từ chối

**Quy trình tra cứu thẻ:**

1. Bên nhận trích xuất tag 8 byte
2. Tra cứu tag trong tất cả các inbound tagset (bộ thẻ vào) hiện tại
3. Truy xuất khóa phiên tương ứng và số thông điệp N
4. Dựng nonce (giá trị dùng một lần): `[0x00, 0x00, 0x00, 0x00, N (8 bytes little-endian)]`
5. Giải mã payload (dữ liệu tải) bằng AEAD (mã hóa xác thực kèm dữ liệu liên kết) với tag làm dữ liệu liên kết
6. Xóa tag khỏi tagset (dùng một lần)
7. Xử lý các khối đã giải mã

**Không tìm thấy thẻ phiên:**

Nếu không tìm thấy thẻ trong bất kỳ tagset (bộ thẻ) nào: - Có thể là một thông điệp NS → thử giải mã NS - Có thể là thông điệp NSR → thử giải mã NSR - Có thể là ES đến sai thứ tự → chờ một chút để tagset được cập nhật - Có thể là tấn công phát lại → từ chối - Có thể là dữ liệu bị hỏng → từ chối

**Payload rỗng:**

ES messages (thông điệp ES) có thể có payload (tải dữ liệu) rỗng (0 byte): - Đóng vai trò như một ACK (xác nhận) rõ ràng khi đã nhận được ACK Request - Cung cấp phản hồi ở tầng giao thức mà không có dữ liệu ứng dụng - Vẫn tiêu tốn một session tag (thẻ phiên) - Hữu ích khi tầng cao hơn không có dữ liệu cần gửi ngay

**Thuộc tính bảo mật:** - Tính bí mật chuyển tiếp đầy đủ (Mức 5) sau khi nhận NSR - Mã hóa có xác thực thông qua AEAD - Tag (thẻ) đóng vai trò như dữ liệu liên kết bổ sung - Tối đa 65535 thông điệp cho mỗi tagset (tập thẻ) trước khi cần ratchet (cơ chế nấc)

---

## Các hàm dẫn xuất khóa

Phần này mô tả tất cả các thao tác KDF (hàm dẫn xuất khóa) được sử dụng trong ECIES (sơ đồ mã hóa tích hợp trên đường cong elliptic), và trình bày đầy đủ các suy diễn mật mã.

### Ký hiệu và Hằng số

**Hằng số:** - `ZEROLEN` - Mảng byte độ dài 0 (chuỗi rỗng) - `||` - Toán tử nối

**Biến:** - `h` - Băm tích lũy của bản ghi (32 byte) - `chainKey` - Khóa chuỗi cho HKDF (32 byte) - `k` - Khóa mã hóa đối xứng (32 byte) - `n` - Nonce / số thứ tự thông điệp

**Các khóa:** - `ask` / `apk` - khóa riêng/công khai tĩnh của Alice - `aesk` / `aepk` - khóa riêng/công khai tạm thời của Alice - `bsk` / `bpk` - khóa riêng/công khai tĩnh của Bob - `besk` / `bepk` - khóa riêng/công khai tạm thời của Bob

### Các KDF (hàm dẫn xuất khóa) cho thông điệp NS

### KDF (hàm dẫn xuất khóa) 1: Khóa chuỗi ban đầu

Thực hiện một lần khi khởi tạo giao thức (có thể tính trước):

```python
# Protocol name (40 bytes, ASCII, no null termination)
protocol_name = "Noise_IKelg2+hs2_25519_ChaChaPoly_SHA256"

# Initialize hash
h = SHA256(protocol_name)

# Initialize chaining key
chainKey = h

# MixHash with empty prologue
h = SHA256(h)

# State: chainKey and h initialized
# Can be precalculated for all outbound sessions
```
**Kết quả:** - `chainKey` = Khóa chuỗi ban đầu cho tất cả các KDF tiếp theo - `h` = Bản ghi băm ban đầu

### KDF 2: Trộn khóa tĩnh của Bob

Bob thực hiện điều này một lần (có thể tính trước cho tất cả các phiên inbound (phiên vào)):

```python
# Bob's static keys (published in LeaseSet)
bsk = GENERATE_PRIVATE()
bpk = DERIVE_PUBLIC(bsk)

# Mix Bob's public key into hash
h = SHA256(h || bpk)

# State: h updated with Bob's identity
# Can be precalculated by Bob for all inbound sessions
```
### KDF 3: Sinh khóa tạm thời của Alice

Alice sinh các khóa mới cho mỗi thông điệp NS:

```python
# Generate ephemeral key pair suitable for Elligator2
aesk = GENERATE_PRIVATE_ELG2()
aepk = DERIVE_PUBLIC(aesk)

# Mix ephemeral public key into hash
h = SHA256(h || aepk)

# Elligator2 encode for transmission
elg2_aepk = ENCODE_ELG2(aepk)

# State: h updated with Alice's ephemeral key
# Send elg2_aepk as first 32 bytes of NS message
```
### KDF 4: Phần khóa tĩnh NS (es DH)

Dẫn xuất các khóa để mã hóa khóa tĩnh của Alice:

```python
# Perform first DH (ephemeral-static)
sharedSecret = DH(aesk, bpk)  # Alice computes
# Equivalent: sharedSecret = DH(bsk, aepk)  # Bob computes

# Derive cipher key from shared secret
keydata = HKDF(chainKey, sharedSecret, "", 64)
chainKey = keydata[0:31]
k = keydata[32:63]

# AEAD encryption parameters
nonce = 0
associated_data = h  # Current hash transcript

# Encrypt static key section
if binding_requested:
    plaintext = apk  # Alice's static public key (32 bytes)
else:
    plaintext = bytes(32)  # All zeros for unbound

ciphertext = ENCRYPT(k, nonce, plaintext, associated_data)
# ciphertext = 32 bytes encrypted + 16 bytes MAC = 48 bytes

# Mix ciphertext into hash
h = SHA256(h || ciphertext)

# State: Static key section encrypted, h updated
# Send ciphertext (48 bytes) as next part of NS message
```
### KDF 5 (hàm dẫn xuất khóa): Phần NS Payload (ss DH, chỉ ràng buộc)

Đối với các phiên đã ràng buộc, thực hiện DH lần thứ hai (trao đổi khóa Diffie–Hellman) để mã hóa payload:

```python
if binding_requested:
    # Alice's static keys
    ask = GENERATE_PRIVATE()  # Alice's long-term key
    apk = DERIVE_PUBLIC(ask)
    
    # Perform second DH (static-static)
    sharedSecret = DH(ask, bpk)  # Alice computes
    # Equivalent: sharedSecret = DH(bsk, apk)  # Bob computes
    
    # Derive cipher key
    keydata = HKDF(chainKey, sharedSecret, "", 64)
    chainKey = keydata[0:31]
    k = keydata[32:63]
    
    nonce = 0
    associated_data = h
else:
    # Unbound: reuse keys from static key section
    # chainKey and k unchanged
    nonce = 1  # Increment nonce (reusing same key)
    associated_data = h

# Encrypt payload
payload = build_payload()  # DateTime + Garlic Cloves + etc.
ciphertext = ENCRYPT(k, nonce, payload, associated_data)

# Mix ciphertext into hash
h = SHA256(h || ciphertext)

# State: Payload encrypted, h contains complete NS transcript
# Save chainKey and h for NSR processing
# Send ciphertext as final part of NS message
```
**Lưu ý quan trọng:**

1. **Bound (ràng buộc) vs Unbound (không ràng buộc)**: 
   - Bound thực hiện 2 phép toán DH (es + ss)
   - Unbound thực hiện 1 phép toán DH (chỉ es)
   - Unbound tăng nonce (giá trị dùng một lần) thay vì dẫn xuất khóa mới

2. **An toàn khi tái sử dụng khóa**:
   - Các nonce (giá trị dùng một lần) khác nhau (0 so với 1) ngăn chặn việc tái sử dụng khóa/nonce
   - Dữ liệu liên kết khác nhau (h khác) đảm bảo phân tách miền

3. **Hash Transcript (bản ghi băm)**:
   - `h` hiện chứa: protocol_name, empty prologue, bpk, aepk, static_key_ciphertext, payload_ciphertext
   - Bản ghi này ràng buộc tất cả các phần của NS message (thông điệp NS) lại với nhau

### KDF (hàm dẫn xuất khóa) cho tập thẻ phản hồi NSR (một cơ chế trong I2P; viết tắt, giữ nguyên)

Bob tạo thẻ cho các thông điệp NSR:

```python
# Chain key from NS payload section
# chainKey = final chainKey from NS KDF

# Generate tagset key
tagsetKey = HKDF(chainKey, ZEROLEN, "SessionReplyTags", 32)

# Initialize NSR tagset (see DH_INITIALIZE below)
tagset_nsr = DH_INITIALIZE(chainKey, tagsetKey)

# Get tag for this NSR
tagsetEntry = tagset_nsr.GET_NEXT_ENTRY()
tag = tagsetEntry.SESSION_TAG  # 8 bytes

# State: tag available for NSR message
# Send tag as first 8 bytes of NSR
```
### Các hàm dẫn xuất khóa (KDF) cho thông điệp NSR

### KDF 6: Sinh khóa tạm thời cho NSR

Bob tạo một khóa phiên tạm thời mới cho mỗi NSR:

```python
# Mix tag into hash (I2P extension to Noise)
h = SHA256(h || tag)

# Generate ephemeral key pair
besk = GENERATE_PRIVATE_ELG2()
bepk = DERIVE_PUBLIC(besk)

# Mix ephemeral public key into hash
h = SHA256(h || bepk)

# Elligator2 encode for transmission
elg2_bepk = ENCODE_ELG2(bepk)

# State: h updated with tag and Bob's ephemeral key
# Send elg2_bepk as bytes 9-40 of NSR message
```
### KDF 7: Phần khóa NSR (ee và se DH)

Dẫn xuất các khóa cho phần khóa NSR:

```python
# Perform third DH (ephemeral-ephemeral)
sharedSecret_ee = DH(aesk, bepk)  # Alice computes
# Equivalent: sharedSecret_ee = DH(besk, aepk)  # Bob computes

# Mix ee into chain
keydata = HKDF(chainKey, sharedSecret_ee, "", 32)
chainKey = keydata[0:31]

# Perform fourth DH (static-ephemeral)
sharedSecret_se = DH(ask, bepk)  # Alice computes
# Equivalent: sharedSecret_se = DH(besk, apk)  # Bob computes

# Derive cipher key from se
keydata = HKDF(chainKey, sharedSecret_se, "", 64)
chainKey = keydata[0:31]
k = keydata[32:63]

# AEAD encryption of empty data (key section has no payload)
nonce = 0
associated_data = h
ciphertext = ENCRYPT(k, nonce, ZEROLEN, associated_data)
# ciphertext = 16 bytes (MAC only, no plaintext)

# Mix ciphertext into hash
h = SHA256(h || ciphertext)

# State: Key section encrypted, chainKey contains all 4 DH results
# Send ciphertext (16 bytes MAC) as bytes 41-56 of NSR
```
**Quan trọng**: Điều này hoàn tất Noise IK handshake (thủ tục bắt tay theo giao thức Noise IK). `chainKey` hiện đã bao gồm phần đóng góp từ cả 4 phép toán DH (es, ss, ee, se).

### KDF (hàm dẫn xuất khóa) 8: Phần tải trọng NSR

Dẫn xuất các khóa để mã hóa phần tải NSR:

```python
# Split chainKey into bidirectional keys
keydata = HKDF(chainKey, ZEROLEN, "", 64)
k_ab = keydata[0:31]   # Alice → Bob key
k_ba = keydata[32:63]  # Bob → Alice key

# Initialize ES tagsets for both directions
tagset_ab = DH_INITIALIZE(chainKey, k_ab)  # Alice → Bob
tagset_ba = DH_INITIALIZE(chainKey, k_ba)  # Bob → Alice

# Derive NSR payload key (Bob → Alice)
k_nsr = HKDF(k_ba, ZEROLEN, "AttachPayloadKDF", 32)

# Encrypt NSR payload
nonce = 0
associated_data = h  # Binds payload to entire NSR
payload = build_payload()  # Usually application reply
ciphertext = ENCRYPT(k_nsr, nonce, payload, associated_data)

# State: Bidirectional ES sessions established
# tagset_ab and tagset_ba ready for ES messages
# Send ciphertext as bytes 57+ of NSR message
```
**Lưu ý quan trọng:**

1. **Split Operation** (thao tác tách):
   - Tạo các khóa độc lập cho từng hướng
   - Ngăn việc tái sử dụng khóa giữa Alice→Bob và Bob→Alice

2. **NSR Payload Binding**:
   - Sử dụng `h` làm dữ liệu liên kết để ràng buộc payload với quá trình bắt tay
   - Một KDF (hàm dẫn xuất khóa) tách biệt ("AttachPayloadKDF") cung cấp phân tách miền (domain separation)

3. **Sẵn sàng ES**:
   - Sau NSR, cả hai bên có thể gửi thông điệp ES
   - Alice phải nhận NSR trước khi gửi ES
   - Bob phải nhận ES trước khi gửi ES

### KDFs (hàm dẫn xuất khóa) cho thông điệp ES

Các thông điệp ES sử dụng các khóa phiên được tạo sẵn từ các tagset (tập thẻ phiên):

```python
# Sender gets next tag and key
tagsetEntry = outbound_tagset.GET_NEXT_ENTRY()
tag = tagsetEntry.SESSION_TAG     # 8 bytes
k = tagsetEntry.SESSION_KEY       # 32 bytes
N = tagsetEntry.INDEX             # Message number

# Construct nonce (12 bytes)
nonce = [0x00, 0x00, 0x00, 0x00] + little_endian_8_bytes(N)

# AEAD encryption
associated_data = tag  # Tag is associated data
payload = build_payload()
ciphertext = ENCRYPT(k, nonce, payload, associated_data)

# Send: tag || ciphertext (8 + len(ciphertext) bytes)
```
**Tiến trình nhận:**

```python
# Extract tag
tag = message[0:8]

# Look up tag in inbound tagsets
tagsetEntry = inbound_tagset.GET_SESSION_KEY(tag)
if tagsetEntry is None:
    # Not an ES message, try NS/NSR decryption
    return try_handshake_decryption(message)

k = tagsetEntry.SESSION_KEY
N = tagsetEntry.INDEX

# Construct nonce
nonce = [0x00, 0x00, 0x00, 0x00] + little_endian_8_bytes(N)

# AEAD decryption
associated_data = tag
ciphertext = message[8:]
try:
    payload = DECRYPT(k, nonce, ciphertext, associated_data)
except AuthenticationError:
    # MAC verification failed, reject message
    return reject_message()

# Process payload blocks
process_payload(payload)

# Remove tag from tagset (one-time use)
inbound_tagset.remove(tag)
```
### Hàm DH_INITIALIZE

Tạo một tagset (tập thẻ) cho một chiều:

```python
def DH_INITIALIZE(rootKey, k):
    """
    Initializes a tagset with session tag and symmetric key ratchets.
    
    Args:
        rootKey: Chain key from previous DH ratchet (32 bytes)
        k: Key material from split() or DH ratchet (32 bytes)
    
    Returns:
        tagset: Initialized tagset object
    """
    # Derive next root key and chain key
    keydata = HKDF(rootKey, k, "KDFDHRatchetStep", 64)
    nextRootKey = keydata[0:31]
    chainKey_tagset = keydata[32:63]
    
    # Derive separate chain keys for tags and keys
    keydata = HKDF(chainKey_tagset, ZEROLEN, "TagAndKeyGenKeys", 64)
    sessTag_ck = keydata[0:31]   # Session tag chain key
    symmKey_ck = keydata[32:63]  # Symmetric key chain key
    
    # Create tagset object
    tagset = Tagset()
    tagset.nextRootKey = nextRootKey
    tagset.sessTag_chainKey = sessTag_ck
    tagset.symmKey_chainKey = symmKey_ck
    tagset.lastIndex = -1
    
    return tagset
```
**Ngữ cảnh sử dụng:**

1. **NSR Tagset (tập thẻ)**: `DH_INITIALIZE(chainKey_from_NS, tagsetKey_NSR)`
2. **ES Tagsets**: `DH_INITIALIZE(chainKey_from_NSR, k_ab or k_ba)`
3. **Ratcheted Tagsets (theo cơ chế bánh cóc)**: `DH_INITIALIZE(nextRootKey_from_previous, tagsetKey_from_DH)`

---

## Các cơ chế Ratchet (cơ chế bánh cóc)

ECIES (Sơ đồ mã hóa tích hợp trên đường cong elliptic) sử dụng ba cơ chế ratchet đồng bộ (cơ chế cập nhật khóa từng bước) để cung cấp tính bí mật chuyển tiếp và quản lý phiên hiệu quả.

### Tổng quan về Ratchet (cơ chế ratchet trong mật mã)

**Ba loại Ratchet (cơ chế bánh cóc):**

1. **DH Ratchet (cơ chế ratchet - cơ chế tiến hóa khóa)**: Thực hiện các trao đổi khóa Diffie–Hellman để tạo ra các khóa gốc mới
2. **Session Tag Ratchet**: Dẫn xuất các thẻ phiên dùng một lần một cách xác định
3. **Symmetric Key Ratchet**: Dẫn xuất các khóa phiên để mã hóa thông điệp

**Mối quan hệ:**

```
DH Ratchet (periodic)
    ↓
Creates new tagset
    ↓
Session Tag Ratchet (per message) ← synchronized → Symmetric Key Ratchet (per message)
    ↓                                                      ↓
Session Tags (8 bytes each)                      Session Keys (32 bytes each)
```
**Các thuộc tính chính:**

- **Bên gửi**: Tạo thẻ và khóa theo nhu cầu (không cần lưu trữ)
- **Bên nhận**: Tạo sẵn thẻ cho cửa sổ nhìn trước (cần lưu trữ)
- **Đồng bộ hóa**: Chỉ số thẻ xác định chỉ số khóa (N_tag = N_key)
- **Bí mật chuyển tiếp**: Đạt được thông qua DH ratchet (cơ chế bánh cóc Diffie–Hellman để luân phiên khóa) định kỳ
- **Hiệu quả**: Bên nhận có thể hoãn việc tính toán khóa cho đến khi nhận được thẻ

### DH Ratchet (cơ chế bánh cóc Diffie–Hellman)

DH ratchet (cơ chế “bánh cóc” Diffie–Hellman) cung cấp tính bí mật chuyển tiếp (forward secrecy) bằng cách định kỳ trao đổi các khóa tạm thời mới.

### Tần suất DH Ratchet (cơ chế ratchet Diffie-Hellman)

**Các điều kiện Ratchet (cơ chế xoay khóa) bắt buộc:** - Tập thẻ sắp cạn (thẻ 65535 là tối đa) - Các chính sách cụ thể theo triển khai:   - Ngưỡng số lượng thông điệp (ví dụ, cứ 4096 thông điệp)   - Ngưỡng thời gian (ví dụ, cứ 10 phút)   - Ngưỡng dung lượng dữ liệu (ví dụ, cứ 100 MB)

**Khuyến nghị về First Ratchet (cơ chế bánh cóc trong mật mã)**: Khoảng nhãn số 4096 để tránh đạt tới giới hạn

**Giá trị tối đa:** - **ID tập thẻ tối đa**: 65535 - **ID khóa tối đa**: 32767 - **Số thông điệp tối đa trên mỗi tập thẻ**: 65535 - **Dung lượng dữ liệu tối đa theo lý thuyết mỗi phiên**: ~6.9 TB (64K tập thẻ × 64K thông điệp × 1730 byte trung bình)

### Nhãn và ID khóa trong DH Ratchet (cơ chế bánh cóc Diffie-Hellman)

**Tag set ban đầu (tập thẻ)** (sau bắt tay): - Tag set ID: 0 - Chưa có khối NextKey nào được gửi - Chưa gán ID khóa nào

**Sau Ratchet (cơ chế bánh cóc mật mã) đầu tiên**: - ID tập thẻ: 1 = (1 + ID khóa của Alice + ID khóa của Bob) = (1 + 0 + 0) - Alice gửi NextKey với ID khóa 0 - Bob phản hồi bằng NextKey với ID khóa 0

**Các tập nhãn tiếp theo**: - ID tập nhãn = 1 + ID khóa của bên gửi + ID khóa của bên nhận - Ví dụ: Tập nhãn 5 = (1 + sender_key_2 + receiver_key_2)

**Bảng tiến triển của tập thẻ:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Tag Set ID</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Sender Key ID</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Receiver Key ID</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">n/a</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">n/a</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Initial tag set (post-NSR)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">0 *</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">0 *</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">First ratchet (both generate new keys)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1 *</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Sender generates new key</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1 *</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Receiver generates new key</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2 *</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Sender generates new key</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2 *</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Receiver generates new key</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">...</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">...</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">...</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Pattern repeats</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">65534</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">32767 *</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">32766</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Second-to-last tag set</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">65535</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">32767</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">32767 *</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Final tag set</td>
    </tr>
  </tbody>
</table>
\* = Khóa mới được tạo trong bước ratchet (cơ chế bánh cóc đổi khóa) này

**Quy tắc ID khóa:** - ID theo thứ tự tăng dần, bắt đầu từ 0 - ID chỉ tăng khi tạo khóa mới - ID khóa tối đa là 32767 (15 bit) - Sau ID khóa 32767, cần phiên mới

### Luồng thông điệp của DH Ratchet (cơ chế bánh cóc Diffie-Hellman)

**Vai trò:** - **Tag Sender** (Bên gửi tag): Sở hữu bộ tag hướng ra, gửi thông điệp - **Tag Receiver** (Bên nhận tag): Sở hữu bộ tag hướng vào, nhận thông điệp

**Pattern:** Bên gửi thẻ khởi động ratchet (cơ chế cập nhật khóa) khi tập thẻ gần cạn.

**Sơ đồ luồng thông điệp:**

```
Tag Sender                         Tag Receiver

       ... using tag set #0 ...

(Tag set #0 approaching exhaustion)
(Generate new key #0)

NextKey forward, request reverse, with key #0  -------->
(Repeat until NextKey ACK received)
                                   (Generate new key #0)
                                   (Perform DH: sender_key_0 × receiver_key_0)
                                   (Create inbound tag set #1)

        <---------------           NextKey reverse, with key #0
                                   (Repeat until tag from tag set #1 received)

(Receive NextKey with key #0)
(Perform DH: sender_key_0 × receiver_key_0)
(Create outbound tag set #1)


       ... using tag set #1 ...


(Tag set #1 approaching exhaustion)
(Generate new key #1)

NextKey forward, with key #1        -------->
(Repeat until NextKey ACK received)
                                   (Reuse existing key #0)
                                   (Perform DH: sender_key_1 × receiver_key_0)
                                   (Create inbound tag set #2)

        <--------------            NextKey reverse, id 0 (ACK)
                                   (Repeat until tag from tag set #2 received)

(Receive NextKey with id 0)
(Perform DH: sender_key_1 × receiver_key_0)
(Create outbound tag set #2)


       ... using tag set #2 ...


(Tag set #2 approaching exhaustion)
(Reuse existing key #1)

NextKey forward, request reverse, id 1  -------->
(Repeat until NextKey received)
                                   (Generate new key #1)
                                   (Perform DH: sender_key_1 × receiver_key_1)
                                   (Create inbound tag set #3)

        <--------------            NextKey reverse, with key #1

(Receive NextKey with key #1)
(Perform DH: sender_key_1 × receiver_key_1)
(Create outbound tag set #3)


       ... using tag set #3 ...

       (Pattern repeats: even-numbered tag sets
        use forward key, odd-numbered use reverse key)
```
**Các mẫu Ratchet (cơ chế cập nhật khóa một chiều):**

**Tạo các bộ thẻ đánh số chẵn** (2, 4, 6, ...): 1. Người gửi sinh khóa mới 2. Người gửi gửi khối NextKey kèm khóa mới 3. Người nhận gửi khối NextKey kèm ID khóa cũ (ACK - xác nhận) 4. Cả hai thực hiện DH (trao đổi khóa Diffie-Hellman) với (khóa người gửi mới × khóa người nhận cũ)

**Tạo các tập thẻ số lẻ** (3, 5, 7, ...): 1. Người gửi yêu cầu khóa đảo chiều (gửi NextKey với cờ yêu cầu) 2. Người nhận tạo khóa mới 3. Người nhận gửi khối NextKey với khóa mới 4. Cả hai thực hiện DH (Diffie-Hellman) với (khóa người gửi cũ × khóa người nhận mới)

### Định dạng khối NextKey (khóa tiếp theo)

Xem phần Payload Format để biết đặc tả chi tiết của khối NextKey.

**Các thành phần chính:** - **Byte cờ**:   - Bit 0: Có khóa (1) hoặc chỉ ID (0)   - Bit 1: Khóa ngược (1) hoặc khóa xuôi (0)   - Bit 2: Yêu cầu khóa ngược (1) hoặc không yêu cầu (0) - **ID khóa**: 2 byte, big-endian (0-32767) - **Khóa công khai**: 32 byte X25519 (nếu bit 0 = 1)

**Ví dụ về NextKey Blocks (các khối khóa kế tiếp):**

```python
# Sender initiates ratchet with new key (key ID 0, tag set 1)
NextKey(flags=0x01, key_id=0, pubkey=sender_key_0)

# Receiver replies with new key (key ID 0, tag set 1)
NextKey(flags=0x03, key_id=0, pubkey=receiver_key_0)

# Sender ratchets again with new key (key ID 1, tag set 2)
NextKey(flags=0x01, key_id=1, pubkey=sender_key_1)

# Receiver ACKs with old key ID (tag set 2)
NextKey(flags=0x02, key_id=0)

# Sender requests reverse key (tag set 3)
NextKey(flags=0x04, key_id=1)

# Receiver sends new reverse key (key ID 1, tag set 3)
NextKey(flags=0x03, key_id=1, pubkey=receiver_key_1)
```
### Hàm dẫn xuất khóa (KDF) của DH Ratchet (cơ chế bánh cóc Diffie–Hellman)

Khi các khóa mới được trao đổi:

```python
# Tag sender generates or reuses key
if generating_new:
    sender_sk = GENERATE_PRIVATE()
    sender_pk = DERIVE_PUBLIC(sender_sk)
else:
    # Reuse existing key pair
    sender_pk = existing_sender_pk

# Tag receiver generates or reuses key
if generating_new:
    receiver_sk = GENERATE_PRIVATE()
    receiver_pk = DERIVE_PUBLIC(receiver_sk)
else:
    # Reuse existing key pair
    receiver_pk = existing_receiver_pk

# Both parties perform DH
sharedSecret = DH(sender_sk, receiver_pk)

# Derive tagset key
tagsetKey = HKDF(sharedSecret, ZEROLEN, "XDHRatchetTagSet", 32)

# Get next root key from previous tagset
rootKey = previous_tagset.nextRootKey

# Initialize new tagset
new_tagset = DH_INITIALIZE(rootKey, tagsetKey)

# Tag sender: outbound tagset
# Tag receiver: inbound tagset
```
**Thời điểm then chốt:**

**Tag Sender (bên gửi tag):** - Tạo bộ tag đầu ra mới ngay lập tức - Bắt đầu sử dụng các tag mới ngay lập tức - Xóa bộ tag đầu ra cũ

**Tag Receiver (bộ nhận tag):** - Tạo tập thẻ đến mới - Giữ lại tập thẻ đến cũ trong khoảng ân hạn (3 phút) - Chấp nhận các thẻ từ cả hai tập thẻ cũ và mới trong khoảng ân hạn - Xóa tập thẻ đến cũ sau khi hết khoảng ân hạn

### Quản lý trạng thái DH Ratchet (cơ chế bánh cóc Diffie-Hellman)

**Trạng thái bên gửi:** - Tập thẻ (tag) gửi đi hiện tại - ID tập thẻ và các ID khóa - Khóa gốc kế tiếp (cho ratchet (cơ chế bánh cóc trong mật mã) kế tiếp) - Số lượng thông điệp trong tập thẻ hiện tại

**Trạng thái bên nhận:** - Tập thẻ đến hiện tại (có thể có 2 trong thời gian ân hạn) - Các số thứ tự thông điệp trước đó (PN) để phát hiện khoảng trống - Cửa sổ nhìn trước của các thẻ được tạo trước - Khóa gốc tiếp theo (cho ratchet (cơ chế bánh cóc) tiếp theo)

**Quy tắc chuyển trạng thái:**

1. **Trước lần Ratchet (cơ chế bánh cóc thay đổi khóa) đầu tiên**:
   - Sử dụng tag set 0 (từ NSR)
   - Chưa gán ID khóa nào

2. **Khởi tạo Ratchet (cơ chế bánh cóc mã hóa)**:
   - Tạo khóa mới (nếu bên gửi là bên tạo trong vòng này)
   - Gửi NextKey block (khối thông báo khóa kế tiếp) trong ES message (thông điệp ES)
   - Chờ phản hồi NextKey trước khi tạo tag set (tập thẻ) gửi đi mới

3. **Receiving Ratchet Request (yêu cầu ratchet - cơ chế xoay/luân phiên khóa)**:
   - Tạo khóa mới (nếu bên nhận là bên tạo trong vòng này)
   - Thực hiện DH (Diffie-Hellman) với khóa nhận được
   - Tạo bộ thẻ vào mới
   - Gửi phản hồi NextKey
   - Giữ lại bộ thẻ vào cũ trong một khoảng ân hạn

4. **Hoàn tất Ratchet (cơ chế chuyển khóa trong mật mã)**:
   - Nhận phản hồi NextKey
   - Thực hiện DH (Diffie–Hellman)
   - Tạo tập thẻ gửi đi mới
   - Bắt đầu sử dụng các thẻ mới

### Session Tag Ratchet (Cơ chế ratchet cho Session Tag)

Cơ chế ratchet (cơ chế bánh cóc) của thẻ phiên tạo ra các thẻ phiên 8 byte chỉ dùng một lần theo cách xác định.

### Mục đích của Session Tag Ratchet (cơ chế ratchet cho thẻ phiên)

- Thay thế việc truyền thẻ tường minh (ElGamal gửi các thẻ 32 byte)
- Cho phép bên nhận tạo trước các thẻ cho cửa sổ nhìn trước
- Bên gửi tạo theo nhu cầu (không cần lưu trữ)
- Đồng bộ với symmetric key ratchet (cơ chế ratchet khóa đối xứng) thông qua chỉ mục

### Công thức ratchet (cơ chế bánh cóc trong mật mã) cho nhãn phiên

**Khởi tạo:**

```python
# From DH_INITIALIZE
sessTag_ck = initial_chain_key  # 32 bytes

# Initialize session tag ratchet
keydata = HKDF(sessTag_ck, ZEROLEN, "STInitialization", 64)
sessTag_chainKey = keydata[0:31]    # First chain key
SESSTAG_CONSTANT = keydata[32:63]   # Constant for all tags in this tagset
```
**Sinh Tag (nhãn) (cho tag N):**

```python
# Generate tag N
keydata = HKDF(sessTag_chainKey_(N-1), SESSTAG_CONSTANT, "SessionTagKeyGen", 64)
sessTag_chainKey_N = keydata[0:31]  # Chain key for next tag
tag_N = keydata[32:39]              # Session tag (8 bytes)

# Chain continues for each tag
# tag_0, tag_1, tag_2, ..., tag_65535
```
**Trình tự đầy đủ:**

```python
# Tag 0
keydata_0 = HKDF(sessTag_chainKey, SESSTAG_CONSTANT, "SessionTagKeyGen", 64)
sessTag_chainKey_0 = keydata_0[0:31]
tag_0 = keydata_0[32:39]

# Tag 1
keydata_1 = HKDF(sessTag_chainKey_0, SESSTAG_CONSTANT, "SessionTagKeyGen", 64)
sessTag_chainKey_1 = keydata_1[0:31]
tag_1 = keydata_1[32:39]

# Tag N
keydata_N = HKDF(sessTag_chainKey_(N-1), SESSTAG_CONSTANT, "SessionTagKeyGen", 64)
sessTag_chainKey_N = keydata_N[0:31]
tag_N = keydata_N[32:39]
```
### Triển khai phía gửi của Session Tag Ratchet (cơ chế ratchet cho thẻ phiên)

```python
class OutboundTagset:
    def __init__(self, sessTag_ck):
        # Initialize
        keydata = HKDF(sessTag_ck, ZEROLEN, "STInitialization", 64)
        self.chainKey = keydata[0:31]
        self.constant = keydata[32:63]
        self.index = -1
    
    def get_next_tag(self):
        # Increment index
        self.index += 1
        
        if self.index > 65535:
            raise TagsetExhausted("Ratchet required")
        
        # Generate tag
        keydata = HKDF(self.chainKey, self.constant, "SessionTagKeyGen", 64)
        self.chainKey = keydata[0:31]
        tag = keydata[32:39]
        
        return (tag, self.index)
```
**Quy trình gửi:** 1. Gọi `get_next_tag()` cho mỗi thông điệp 2. Sử dụng thẻ được trả về trong thông điệp ES 3. Lưu chỉ mục N để có thể theo dõi ACK (xác nhận) 4. Không cần lưu trữ thẻ (được tạo theo yêu cầu)

### Triển khai phía nhận của Session Tag Ratchet (cơ chế ratchet cho thẻ phiên)

```python
class InboundTagset:
    def __init__(self, sessTag_ck, look_ahead=32):
        # Initialize
        keydata = HKDF(sessTag_ck, ZEROLEN, "STInitialization", 64)
        self.chainKey = keydata[0:31]
        self.constant = keydata[32:63]
        self.index = -1
        self.look_ahead = look_ahead
        self.tags = {}  # Dictionary: tag -> index
        
        # Pre-generate initial tags
        self.extend(look_ahead)
    
    def extend(self, count):
        """Generate 'count' more tags"""
        for _ in range(count):
            self.index += 1
            
            if self.index > 65535:
                return  # Cannot exceed maximum
            
            # Generate tag
            keydata = HKDF(self.chainKey, self.constant, "SessionTagKeyGen", 64)
            self.chainKey = keydata[0:31]
            tag = keydata[32:39]
            
            # Store tag
            self.tags[tag] = self.index
    
    def lookup_tag(self, tag):
        """Look up tag and return index"""
        if tag in self.tags:
            index = self.tags[tag]
            # Remove tag (one-time use)
            del self.tags[tag]
            return index
        return None
    
    def check_and_extend(self):
        """Extend if tag count is low"""
        current_count = len(self.tags)
        if current_count < self.look_ahead // 2:
            # Extend to restore window
            self.extend(self.look_ahead - current_count)
```
**Quy trình phía nhận:** 1. Tạo sẵn tag (thẻ) cho cửa sổ nhìn trước (ví dụ: 32 tag) 2. Lưu các tag trong bảng băm hoặc từ điển 3. Khi thông điệp đến, tra cứu tag để lấy chỉ số N 4. Xóa tag khỏi bộ lưu trữ (dùng một lần) 5. Mở rộng cửa sổ nếu số lượng tag giảm xuống dưới ngưỡng

### Chiến lược nhìn trước cho thẻ phiên

**Mục đích**: Cân bằng việc sử dụng bộ nhớ với việc xử lý thông điệp không theo thứ tự

**Kích thước Look-Ahead (xem trước) được khuyến nghị:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Tagset Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Initial Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Maximum Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NSR tagset</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">12</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">12</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Short-lived</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ES tagset 0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">24</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">160</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Initial ES tagset</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ES tagset 1+</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">160</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">160</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Ratcheted tagsets</td>
    </tr>
  </tbody>
</table>
**Nhìn trước thích ứng:**

```python
# Dynamic look-ahead based on highest tag received
look_ahead = min(tsmax, tsmin + N // 4)

# Example:
# tsmin = 24, tsmax = 160
# N = 0:   look_ahead = min(160, 24 + 0/4) = 24
# N = 100: look_ahead = min(160, 24 + 100/4) = 49
# N = 500: look_ahead = min(160, 24 + 500/4) = 149
# N = 544: look_ahead = min(160, 24 + 544/4) = 160
```
**Cắt bớt phía sau:**

```python
# Trim tags far behind highest received
trim_behind = look_ahead // 2

# If highest received tag is N=100, trim tags below N=50
```
**Tính toán bộ nhớ:**

```python
# Per tag: 8 bytes (tag) + 2 bytes (index) + overhead ≈ 16 bytes
# Look-ahead of 160 tags ≈ 2.5 KB per inbound tagset

# With multiple sessions:
# 100 inbound sessions × 2.5 KB = 250 KB total
```
### Xử lý Session Tag (thẻ phiên) khi đến không theo thứ tự

**Kịch bản**: Thông điệp đến không theo đúng thứ tự

```
Expected: tag_5, tag_6, tag_7, tag_8
Received: tag_5, tag_7, tag_6, tag_8
```
**Hành vi phía nhận:**

1. Nhận tag_5:
   - Tra cứu: tìm thấy tại chỉ mục 5
   - Xử lý thông điệp
   - Xóa tag_5
   - Giá trị nhận cao nhất: 5

2. Nhận tag_7 (không theo thứ tự):
   - Tra cứu: tìm thấy tại chỉ mục 7
   - Xử lý thông điệp
   - Xóa tag_7
   - Lớn nhất đã nhận: 7
   - Lưu ý: tag_6 vẫn còn trong bộ nhớ lưu trữ (chưa nhận)

3. Nhận tag_6 (bị trễ):
   - Tra cứu: tìm thấy tại chỉ mục 6
   - Xử lý thông điệp
   - Xóa tag_6
   - Giá trị cao nhất đã nhận: 7 (không thay đổi)

4. Nhận tag_8:
   - Tra cứu: tìm thấy tại chỉ mục 8
   - Xử lý thông điệp
   - Xóa tag_8
   - Mức cao nhất đã nhận: 8

**Bảo trì cửa sổ:** - Theo dõi chỉ số nhận được cao nhất - Duy trì danh sách các chỉ số bị thiếu (khoảng trống) - Mở rộng cửa sổ dựa trên chỉ số cao nhất - Tùy chọn: Cho các khoảng trống cũ hết hạn sau khi quá thời gian chờ

### Cơ chế bánh cóc khóa đối xứng

Cơ chế symmetric key ratchet (cơ chế bánh cóc khóa đối xứng) tạo ra các khóa mã hóa 32 byte được đồng bộ với các thẻ phiên.

### Mục đích của cơ chế bánh cóc khóa đối xứng

- Cung cấp khóa mã hóa duy nhất cho từng thông điệp
- Đồng bộ với session tag ratchet (cơ chế "ratchet" của thẻ phiên) (cùng chỉ mục)
- Bên gửi có thể tạo theo yêu cầu
- Bên nhận có thể hoãn việc tạo cho đến khi thẻ được nhận

### Công thức Ratchet (cơ chế bánh cóc) cho khóa đối xứng

**Khởi tạo:**

```python
# From DH_INITIALIZE
symmKey_ck = initial_chain_key  # 32 bytes

# No additional initialization needed
# Unlike session tag ratchet, no constant is derived
```
**Sinh khóa (cho khóa N):**

```python
# Generate key N
SYMMKEY_CONSTANT = ZEROLEN  # Empty string
keydata = HKDF(symmKey_chainKey_(N-1), SYMMKEY_CONSTANT, "SymmetricRatchet", 64)
symmKey_chainKey_N = keydata[0:31]  # Chain key for next key
key_N = keydata[32:63]              # Session key (32 bytes)
```
**Trình tự hoàn chỉnh:**

```python
# Key 0
keydata_0 = HKDF(symmKey_ck, ZEROLEN, "SymmetricRatchet", 64)
symmKey_chainKey_0 = keydata_0[0:31]
key_0 = keydata_0[32:63]

# Key 1
keydata_1 = HKDF(symmKey_chainKey_0, ZEROLEN, "SymmetricRatchet", 64)
symmKey_chainKey_1 = keydata_1[0:31]
key_1 = keydata_1[32:63]

# Key N
keydata_N = HKDF(symmKey_chainKey_(N-1), ZEROLEN, "SymmetricRatchet", 64)
symmKey_chainKey_N = keydata_N[0:31]
key_N = keydata_N[32:63]
```
### Hiện thực phía gửi của Symmetric Key Ratchet (cơ chế bánh cóc dùng khóa đối xứng)

```python
class OutboundKeyRatchet:
    def __init__(self, symmKey_ck):
        self.chainKey = symmKey_ck
        self.index = -1
    
    def get_key(self, index):
        """Generate key for specific index"""
        # Fast-forward to desired index if needed
        while self.index < index:
            self.index += 1
            keydata = HKDF(self.chainKey, ZEROLEN, "SymmetricRatchet", 64)
            self.chainKey = keydata[0:31]
            if self.index == index:
                return keydata[32:63]
        
        # Should not reach here if called correctly
        raise ValueError("Key already generated")
```
**Quy trình phía người gửi:** 1. Lấy tag (thẻ) tiếp theo và chỉ số của nó N 2. Tạo khóa cho chỉ số N 3. Dùng khóa để mã hóa thông điệp 4. Không cần lưu trữ khóa

### Triển khai phía nhận Symmetric Key Ratchet (cơ chế bánh cóc cho khóa đối xứng)

**Chiến lược 1: Deferred Generation (sinh trì hoãn) (Khuyến nghị)**

```python
class InboundKeyRatchet:
    def __init__(self, symmKey_ck):
        self.chainKey = symmKey_ck
        self.index = -1
        self.cache = {}  # Optional: cache recently used keys
    
    def get_key(self, index):
        """Generate key for specific index"""
        # Check cache first (optional optimization)
        if index in self.cache:
            key = self.cache[index]
            del self.cache[index]
            return key
        
        # Fast-forward to desired index
        while self.index < index:
            self.index += 1
            keydata = HKDF(self.chainKey, ZEROLEN, "SymmetricRatchet", 64)
            self.chainKey = keydata[0:31]
            
            if self.index == index:
                return keydata[32:63]
        
        raise ValueError("Index already passed")
```
**Quy trình tạo trì hoãn:** 1. Nhận ES message có tag 2. Tra cứu tag để lấy chỉ số N 3. Sinh các khóa từ 0 đến N (nếu chưa được sinh) 4. Dùng khóa N để giải mã thông điệp 5. Chain key (khóa chuỗi) hiện ở vị trí chỉ số N

**Ưu điểm:** - Mức sử dụng bộ nhớ tối thiểu - Khóa chỉ được tạo khi cần - Triển khai đơn giản

**Nhược điểm:** - Phải tạo tất cả các khóa từ 0 đến N khi sử dụng lần đầu - Không thể xử lý các thông điệp đến không theo thứ tự nếu không có bộ nhớ đệm

**Chiến lược 2: Tạo trước với Tag Window (cửa sổ thẻ) (Phương án thay thế)**

```python
class InboundKeyRatchet:
    def __init__(self, symmKey_ck):
        self.chainKey = symmKey_ck
        self.index = -1
        self.keys = {}  # Dictionary: index -> key
    
    def extend(self, count):
        """Pre-generate 'count' more keys"""
        for _ in range(count):
            self.index += 1
            keydata = HKDF(self.chainKey, ZEROLEN, "SymmetricRatchet", 64)
            self.chainKey = keydata[0:31]
            key = keydata[32:63]
            self.keys[self.index] = key
    
    def get_key(self, index):
        """Retrieve pre-generated key"""
        if index in self.keys:
            key = self.keys[index]
            del self.keys[index]
            return key
        return None
```
**Quy trình tạo trước:** 1. Tạo trước các khóa khớp với tag window (cửa sổ thẻ) (ví dụ, 32 khóa) 2. Lưu các khóa được lập chỉ mục theo số thứ tự thông điệp 3. Khi nhận thẻ, tra cứu khóa tương ứng 4. Mở rộng cửa sổ khi các thẻ được sử dụng

**Ưu điểm:** - Xử lý các thông điệp không theo thứ tự một cách tự nhiên - Truy xuất khóa nhanh (không có độ trễ tạo)

**Nhược điểm:** - Mức sử dụng bộ nhớ cao hơn (32 byte mỗi key (khóa) so với 8 byte mỗi tag (thẻ)) - Phải giữ các key (khóa) đồng bộ với các tag (thẻ)

**So sánh bộ nhớ:**

```python
# Look-ahead of 160:
# Tags only:  160 × 16 bytes = 2.5 KB
# Tags+Keys:  160 × (16 + 32) bytes = 7.5 KB
# 
# For 100 sessions:
# Tags only:  250 KB
# Tags+Keys:  750 KB
```
### Đồng bộ hóa ratchet đối xứng với Session Tags (thẻ phiên)

**Yêu cầu quan trọng**: Chỉ mục Session tag (thẻ phiên) PHẢI bằng chỉ mục khóa đối xứng

```python
# Sender
tag, index = outbound_tagset.get_next_tag()
key = outbound_keyratchet.get_key(index)  # Same index
nonce = construct_nonce(index)
ciphertext = ENCRYPT(key, nonce, payload, tag)

# Receiver
index = inbound_tagset.lookup_tag(tag)
key = inbound_keyratchet.get_key(index)  # Same index
nonce = construct_nonce(index)
plaintext = DECRYPT(key, nonce, ciphertext, tag)
```
**Các chế độ hỏng hóc:**

Nếu việc đồng bộ hóa bị gián đoạn: - Dùng sai khóa để giải mã - Việc xác minh MAC (mã xác thực thông điệp) thất bại - Thông điệp bị từ chối

**Phòng ngừa:** - Luôn dùng cùng một chỉ mục cho thẻ và khóa - Không bao giờ bỏ qua các chỉ mục trong bất kỳ ratchet (cơ chế cập nhật khóa dần) nào - Xử lý cẩn thận các thông điệp không theo thứ tự

### Thiết kế Nonce (số dùng một lần) cho Symmetric Ratchet (ratchet đối xứng)

Nonce (giá trị chỉ dùng một lần) được suy ra từ số thứ tự thông điệp:

```python
def construct_nonce(index):
    """
    Construct 12-byte nonce for ChaCha20-Poly1305
    
    Args:
        index: Message number (0-65535)
    
    Returns:
        nonce: 12-byte nonce
    """
    # First 4 bytes are always zero
    nonce = bytearray(12)
    nonce[0:4] = b'\x00\x00\x00\x00'
    
    # Last 8 bytes are little-endian message number
    nonce[4:12] = index.to_bytes(8, byteorder='little')
    
    return bytes(nonce)
```
**Ví dụ:**

```python
index = 0:     nonce = 0x00000000 0000000000000000
index = 1:     nonce = 0x00000000 0100000000000000
index = 255:   nonce = 0x00000000 FF00000000000000
index = 256:   nonce = 0x00000000 0001000000000000
index = 65535: nonce = 0x00000000 FFFF000000000000
```
**Các thuộc tính quan trọng:** - Nonce (giá trị số dùng một lần) là duy nhất cho mỗi thông điệp trong một bộ thẻ - Nonce không bao giờ lặp lại (các thẻ dùng một lần đảm bảo điều này) - Bộ đếm 8 byte cho phép 2^64 thông điệp (chúng tôi chỉ dùng 2^16) - Định dạng nonce khớp với phương pháp xây dựng dựa trên bộ đếm của RFC 7539

---

## Quản lý phiên

### Ngữ cảnh phiên

Tất cả các phiên vào và ra phải thuộc về một ngữ cảnh cụ thể:

1. **Ngữ cảnh Router**: Các phiên dành cho chính router
2. **Ngữ cảnh Destination** (đích I2P): Các phiên dành cho một destination cục bộ cụ thể (ứng dụng khách)

**Quy tắc quan trọng**: Tuyệt đối không được chia sẻ phiên giữa các ngữ cảnh để ngăn chặn các cuộc tấn công tương quan.

**Triển khai:**

```python
class SessionKeyManager:
    """Context for managing sessions (router or destination)"""
    def __init__(self, context_id):
        self.context_id = context_id
        self.inbound_sessions = {}   # far_end_dest -> [sessions]
        self.outbound_sessions = {}  # far_end_dest -> session
        self.static_keypair = generate_keypair()  # Context's identity
    
    def get_outbound_session(self, destination):
        """Get or create outbound session to destination"""
        if destination not in self.outbound_sessions:
            self.outbound_sessions[destination] = create_outbound_session(destination)
        return self.outbound_sessions[destination]
    
    def add_inbound_session(self, session, destination=None):
        """Add inbound session, optionally bound to destination"""
        if destination:
            if destination not in self.inbound_sessions:
                self.inbound_sessions[destination] = []
            self.inbound_sessions[destination].append(session)
        else:
            # Unbound session
            self.inbound_sessions[None].append(session)
```
**Triển khai I2P bằng Java:**

Trong Java I2P, lớp `SessionKeyManager` cung cấp các chức năng sau: - Một `SessionKeyManager` cho mỗi router - Một `SessionKeyManager` cho mỗi đích cục bộ - Quản lý tách biệt các phiên ECIES và ElGamal trong từng ngữ cảnh

### Ràng buộc phiên

**Binding** (ràng buộc) thiết lập mối liên hệ giữa một phiên và một đích đầu xa cụ thể.

### Các phiên ràng buộc

**Đặc điểm:** - Bao gồm khóa tĩnh của người gửi trong NS message (thông điệp NS) - Người nhận có thể nhận diện destination (đích) của người gửi - Cho phép giao tiếp hai chiều - Một phiên đi cho mỗi destination - Có thể có nhiều phiên đến (trong quá trình chuyển đổi)

**Trường hợp sử dụng:** - Kết nối dạng streaming (tương tự TCP) - Các datagram (gói tin) có thể phản hồi - Bất kỳ giao thức nào đòi hỏi mô hình yêu cầu/đáp ứng

**Quy trình liên kết:**

```python
# Alice creates bound outbound session
outbound_session = OutboundSession(
    destination=bob_destination,
    static_key=alice_static_key,
    bound=True
)

# Alice sends NS with static key
ns_message = build_ns_message(
    ephemeral_key=alice_ephemeral_key,
    static_key=alice_static_key,  # Included for binding
    payload=data
)

# Bob receives NS
bob_receives_ns(ns_message)
# Bob extracts Alice's static key
alice_static_key = decrypt_static_key_section(ns_message)

# Bob looks up Alice's destination (from bundled LeaseSet)
alice_destination = lookup_destination_by_static_key(alice_static_key)

# Bob creates bound inbound session
inbound_session = InboundSession(
    destination=alice_destination,
    bound=True
)

# Bob pairs with outbound session
outbound_session = OutboundSession(
    destination=alice_destination,
    bound=True
)
```
**Lợi ích:** 1. **Ephemeral-Ephemeral DH (cả hai bên dùng khóa Diffie-Hellman tạm thời)**: Phản hồi sử dụng ee DH (bảo mật chuyển tiếp đầy đủ) 2. **Tính liên tục của phiên**: Ratchets (cơ chế cập nhật khóa một chiều) duy trì ràng buộc tới cùng một đích 3. **Bảo mật**: Ngăn chiếm quyền phiên (xác thực bằng khóa tĩnh) 4. **Hiệu quả**: Một phiên cho mỗi đích (không trùng lặp)

### Các phiên chưa ràng buộc

**Đặc điểm:** - Không có khóa tĩnh trong NS message (phần cờ (flags) đều là số 0) - Người nhận không thể xác định người gửi - Chỉ liên lạc một chiều - Cho phép nhiều phiên đến cùng một đích

**Các trường hợp sử dụng:** - Gói datagram thô (gửi rồi quên) - Xuất bản ẩn danh - Nhắn tin kiểu phát quảng bá

**Đặc tính:** - Ẩn danh hơn (không thể xác định người gửi) - Hiệu quả hơn (1 DH (Diffie-Hellman - trao đổi khóa) so với 2 DH trong handshake (quy trình bắt tay)) - Không thể trả lời (người nhận không biết trả lời tới đâu) - Không có session ratcheting (cơ chế tăng dần khóa phiên; dùng một lần hoặc giới hạn)

### Ghép cặp phiên

**Ghép cặp** kết nối một phiên đến với một phiên đi để giao tiếp hai chiều.

### Tạo phiên ghép cặp

**Góc nhìn của Alice (bên khởi tạo):**

```python
# Create outbound session to Bob
outbound_session = create_outbound_session(bob_destination)

# Create paired inbound session
inbound_session = create_inbound_session(
    paired_with=outbound_session,
    bound_to=bob_destination
)

# Link them
outbound_session.paired_inbound = inbound_session
inbound_session.paired_outbound = outbound_session

# Send NS message
send_ns_message(outbound_session, payload)
```
**Góc nhìn của Bob (responder - bên phản hồi):**

```python
# Receive NS message
ns_message = receive_ns_message()

# Create inbound session
inbound_session = create_inbound_session_from_ns(ns_message)

# If NS contains static key (bound):
if ns_message.has_static_key():
    alice_destination = extract_destination(ns_message)
    inbound_session.bind_to(alice_destination)
    
    # Create paired outbound session
    outbound_session = create_outbound_session(alice_destination)
    
    # Link them
    outbound_session.paired_inbound = inbound_session
    inbound_session.paired_outbound = outbound_session

# Send NSR
send_nsr_message(inbound_session, outbound_session, payload)
```
### Lợi ích của việc ghép cặp phiên

1. **ACKs trong băng** (ACK = acknowledgement - xác nhận): Có thể xác nhận thông điệp mà không cần clove riêng biệt (clove: “nhánh” trong garlic message)
2. **Ratcheting hiệu quả** (cơ chế “bánh cóc” mật mã): Cả hai hướng ratchet đồng bộ
3. **Điều khiển luồng**: Có thể triển khai back-pressure (cơ chế áp lực ngược) trên các phiên ghép cặp
4. **Tính nhất quán trạng thái**: Dễ dàng duy trì trạng thái đồng bộ

### Các quy tắc ghép cặp phiên

- Phiên đi ra có thể không được ghép cặp (NS chưa ràng buộc)
- Phiên đi vào đối với NS đã ràng buộc nên được ghép cặp
- Việc ghép cặp diễn ra khi tạo phiên, không phải sau đó
- Các phiên đã ghép cặp có cùng ràng buộc đích
- Các cơ chế ratchet (cơ chế then cài mật mã) diễn ra độc lập nhưng được điều phối

### Vòng đời phiên

### Vòng đời phiên: Giai đoạn khởi tạo

**Khởi tạo phiên gửi đi (Alice):**

```python
def create_outbound_session(destination, bound=True):
    session = OutboundSession()
    session.destination = destination
    session.bound = bound
    session.state = SessionState.NEW
    session.created_time = now()
    
    # Generate keys for NS message
    session.ephemeral_keypair = generate_elg2_keypair()
    if bound:
        session.static_key = context.static_keypair.public_key
    
    # Will be populated after NSR received
    session.outbound_tagset = None
    session.inbound_tagset = None
    
    return session
```
**Khởi tạo phiên đến (Bob):**

```python
def create_inbound_session_from_ns(ns_message):
    session = InboundSession()
    session.state = SessionState.ESTABLISHED
    session.created_time = now()
    
    # Extract from NS
    session.remote_ephemeral_key = ns_message.ephemeral_key
    session.remote_static_key = ns_message.static_key
    
    if session.remote_static_key:
        session.bound = True
        session.destination = lookup_destination(session.remote_static_key)
    else:
        session.bound = False
        session.destination = None
    
    # Generate keys for NSR
    session.ephemeral_keypair = generate_elg2_keypair()
    
    # Create tagsets from KDF
    session.inbound_tagset = create_tagset_from_nsr()
    session.outbound_tagset = create_tagset_from_nsr()
    
    return session
```
### Vòng đời phiên: Giai đoạn hoạt động

**Các chuyển trạng thái:**

```
NEW (outbound only)
  ↓
  NS sent
  ↓
PENDING_REPLY (outbound only)
  ↓
  NSR received
  ↓
ESTABLISHED
  ↓
  ES messages exchanged
  ↓
ESTABLISHED (ongoing)
  ↓
  (optional) RATCHETING
  ↓
ESTABLISHED
```
**Duy trì phiên hoạt động:**

```python
def maintain_active_session(session):
    # Update last activity time
    session.last_activity = now()
    
    # Check for ratchet needed
    if session.outbound_tagset.needs_ratchet():
        initiate_ratchet(session)
    
    # Check for incoming ratchet
    if received_nextkey_block():
        process_ratchet(session)
    
    # Trim old tags from inbound tagset
    session.inbound_tagset.expire_old_tags()
    
    # Check session health
    if session.idle_time() > SESSION_TIMEOUT:
        mark_session_idle(session)
```
### Vòng đời phiên: Giai đoạn hết hạn

**Các giá trị thời gian chờ của phiên:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Session Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Sender Timeout</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Receiver Timeout</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NSR tagset</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">N/A</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3 minutes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Short-lived</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ES tagset 0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">8 minutes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">10 minutes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Initial</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ES tagset 1+</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">8 minutes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">10 minutes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Ratcheted</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Old tagset</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">N/A</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3 minutes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">After ratchet</td>
    </tr>
  </tbody>
</table>
**Cơ chế hết hạn:**

```python
def check_session_expiration():
    for session in active_sessions:
        # Outbound session expiration (sender)
        if session.is_outbound():
            if session.idle_time() > 8 * 60:  # 8 minutes
                expire_outbound_session(session)
        
        # Inbound session expiration (receiver)
        else:
            if session.idle_time() > 10 * 60:  # 10 minutes
                expire_inbound_session(session)
    
    # Old tagsets (after ratchet)
    for tagset in old_tagsets:
        if tagset.age() > 3 * 60:  # 3 minutes
            delete_tagset(tagset)
```
**Quy tắc trọng yếu**: Các phiên ra PHẢI hết hạn trước các phiên vào để tránh mất đồng bộ.

**Kết thúc an toàn:**

```python
def terminate_session(session, reason=0):
    # Send Termination block (if implemented)
    send_termination_block(session, reason)
    
    # Mark session for deletion
    session.state = SessionState.TERMINATED
    
    # Keep session briefly for final messages
    schedule_deletion(session, delay=30)  # 30 seconds
    
    # Notify paired session
    if session.paired_session:
        session.paired_session.mark_remote_terminated()
```
### Nhiều thông điệp NS

**Kịch bản**: Thông điệp NS của Alice bị mất hoặc phản hồi NSR bị mất.

**Hành vi của Alice:**

```python
class OutboundSession:
    def __init__(self):
        self.ns_messages_sent = []
        self.ns_timer = None
        self.max_ns_attempts = 5
    
    def send_ns_message(self, payload):
        # Generate new ephemeral key for each NS
        ephemeral_key = generate_elg2_keypair()
        
        ns_message = build_ns_message(
            ephemeral_key=ephemeral_key,
            static_key=self.static_key,
            payload=payload
        )
        
        # Store state for this NS
        ns_state = {
            'ephemeral_key': ephemeral_key,
            'chainkey': compute_chainkey(ns_message),
            'hash': compute_hash(ns_message),
            'tagset': derive_nsr_tagset(ns_message),
            'sent_time': now()
        }
        self.ns_messages_sent.append(ns_state)
        
        # Send message
        send_message(ns_message)
        
        # Set timer for retry
        if not self.ns_timer:
            self.ns_timer = set_timer(1.0, self.on_ns_timeout)
    
    def on_ns_timeout(self):
        if len(self.ns_messages_sent) >= self.max_ns_attempts:
            # Give up
            fail_session("No NSR received after {self.max_ns_attempts} attempts")
            return
        
        # Retry with new NS message
        send_ns_message(self.payload)
    
    def on_nsr_received(self, nsr_message):
        # Cancel timer
        cancel_timer(self.ns_timer)
        
        # Find which NS this NSR responds to
        tag = nsr_message.tag
        for ns_state in self.ns_messages_sent:
            if tag in ns_state['tagset']:
                # This NSR corresponds to this NS
                self.active_ns_state = ns_state
                break
        
        # Process NSR and complete handshake
        complete_handshake(nsr_message, self.active_ns_state)
        
        # Discard other NS states
        self.ns_messages_sent = []
```
**Các thuộc tính quan trọng:**

1. **Khóa tạm thời riêng biệt**: Mỗi NS sử dụng một khóa tạm thời khác nhau
2. **Bắt tay độc lập**: Mỗi NS tạo trạng thái bắt tay riêng biệt
3. **Tương quan NSR**: Thẻ NSR xác định NS mà nó phản hồi
4. **Dọn dẹp trạng thái**: Các trạng thái NS không dùng sẽ bị loại bỏ sau khi NSR thành công

**Phòng ngừa tấn công:**

Để ngăn ngừa cạn kiệt tài nguyên:

```python
# Limit NS sending rate
max_ns_rate = 5 per 10 seconds per destination

# Limit total NS attempts
max_ns_attempts = 5

# Limit total pending NS states
max_pending_ns = 10 per context
```
### Nhiều thông điệp NSR

**Kịch bản**: Bob gửi nhiều NSR (ví dụ: dữ liệu phản hồi được chia nhỏ thành nhiều thông điệp).

**Hành vi của Bob:**

```python
class InboundSession:
    def send_nsr_replies(self, payload_chunks):
        # One NS received, multiple NSRs to send
        for chunk in payload_chunks:
            # Generate new ephemeral key for each NSR
            ephemeral_key = generate_elg2_keypair()
            
            # Get next tag from NSR tagset
            tag = self.nsr_tagset.get_next_tag()
            
            nsr_message = build_nsr_message(
                tag=tag,
                ephemeral_key=ephemeral_key,
                payload=chunk
            )
            
            send_message(nsr_message)
        
        # Wait for ES message from Alice
        self.state = SessionState.AWAITING_ES
```
**Hành vi của Alice:**

```python
class OutboundSession:
    def on_nsr_received(self, nsr_message):
        if self.state == SessionState.PENDING_REPLY:
            # First NSR received
            complete_handshake(nsr_message)
            self.state = SessionState.ESTABLISHED
            
            # Create ES sessions
            self.es_outbound_tagset = derive_es_outbound_tagset()
            self.es_inbound_tagset = derive_es_inbound_tagset()
            
            # Send ES message (ACK)
            send_es_message(empty_payload)
        
        elif self.state == SessionState.ESTABLISHED:
            # Additional NSR received
            # Decrypt and process payload
            payload = decrypt_nsr_payload(nsr_message)
            process_payload(payload)
            
            # These NSRs are from other NS attempts, ignore handshake
```
**Dọn dẹp của Bob:**

```python
class InboundSession:
    def on_es_received(self, es_message):
        # First ES received from Alice
        # This confirms which NSR Alice used
        
        # Clean up other handshake states
        for other_ns_state in self.pending_ns_states:
            if other_ns_state != self.active_ns_state:
                delete_ns_state(other_ns_state)
        
        # Delete unused NSR tagsets
        for tagset in self.nsr_tagsets:
            if tagset != self.active_nsr_tagset:
                delete_tagset(tagset)
        
        self.state = SessionState.ESTABLISHED
```
**Các thuộc tính quan trọng:**

1. **Cho phép nhiều NSR**: Bob có thể gửi nhiều NSR cho mỗi NS
2. **Khóa tạm thời khác nhau**: Mỗi NSR nên sử dụng một khóa tạm thời duy nhất
3. **Cùng một tagset cho NSR**: Tất cả các NSR cho một NS sử dụng cùng một tagset (tập thẻ)
4. **ES đầu tiên sẽ thắng**: ES đầu tiên của Alice quyết định NSR nào thành công
5. **Dọn dẹp sau ES**: Bob loại bỏ các trạng thái chưa dùng sau khi nhận ES

### Máy trạng thái phiên

**Sơ đồ trạng thái đầy đủ:**

```
                    Outbound Session                    Inbound Session

                         NEW
                          |
                     send NS
                          |
                   PENDING_REPLY -------------------- receive NS ---> ESTABLISHED
                          |                                                |
                   receive NSR                                        send NSR
                          |                                                |
                    ESTABLISHED <---------- receive ES ------------- AWAITING_ES
                          |                     |                          |
                    ┌─────┴─────┐               |                    receive ES
                    |           |               |                          |
              send ES      receive ES           |                    ESTABLISHED
                    |           |               |                          |
                    └─────┬─────┘               |                ┌─────────┴─────────┐
                          |                     |                |                   |
                          |                     |          send ES              receive ES
                          |                     |                |                   |
                          |                     |                └─────────┬─────────┘
                          |                     |                          |
                          └─────────────────────┴──────────────────────────┘
                                              ACTIVE
                                                |
                                         idle timeout
                                                |
                                             EXPIRED
```
**Mô tả trạng thái:**

- **NEW**: Phiên gửi đi đã được tạo, chưa gửi NS
- **PENDING_REPLY**: Đã gửi NS, đang chờ NSR
- **AWAITING_ES**: Đã gửi NSR, đang chờ ES đầu tiên từ Alice
- **ESTABLISHED**: Bắt tay đã hoàn tất, có thể gửi/nhận ES
- **ACTIVE**: Đang tích cực trao đổi các thông điệp ES
- **RATCHETING**: DH ratchet (cơ chế bánh cóc Diffie-Hellman) đang diễn ra (trạng thái con của ACTIVE)
- **EXPIRED**: Phiên đã hết hạn, đang chờ xóa
- **TERMINATED**: Phiên đã bị kết thúc tường minh

---

## Định dạng dữ liệu tải

Phần tải của tất cả các thông điệp ECIES (lược đồ mã hóa tích hợp trên đường cong elliptic) (NS, NSR, ES) sử dụng một định dạng dựa trên khối tương tự NTCP2.

### Cấu trúc khối

**Định dạng chung:**

```
+----+----+----+----+----+----+----+----+
|blk |  size   |       data             |
+----+----+----+                        +
|                                       |
~               ...                     ~
|                                       |
+----+----+----+----+----+----+----+----+
|blk |  size   |       data             |
+----+----+----+                        +
|                                       |
~               ...                     ~
|                                       |
+----+----+----+----+----+----+----+----+
```
**Các trường:**

- `blk`: 1 byte - Số kiểu khối
- `size`: 2 byte - Kích thước big-endian (thứ tự byte lớn trước) của trường dữ liệu (0-65516)
- `data`: Độ dài thay đổi - Dữ liệu dành riêng cho khối

**Các ràng buộc:**

- Khung ChaChaPoly tối đa: 65535 byte
- MAC Poly1305: 16 byte
- Tổng số khối tối đa: 65519 byte (65535 - 16)
- Khối đơn tối đa: 65519 byte (bao gồm phần đầu 3 byte)
- Dữ liệu khối đơn tối đa: 65516 byte

### Các loại khối

**Các loại khối được định nghĩa:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Name</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DateTime</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">7 bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Implemented</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Required in NS</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1-3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">-</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">-</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Future use</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Termination</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">9+ bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Unimplemented</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Session termination</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Options</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">21+ bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Unimplemented</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Session options</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">MessageNumbers</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">5 bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Unimplemented</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">PN value</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NextKey</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">3 or 35 bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Implemented</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DH ratchet</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">8</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ACK</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">4+ bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Implemented</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Message acknowledgment</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">9</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ACK Request</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">3 bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Implemented</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Request ACK</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">10</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">-</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">-</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Future use</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">11</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Garlic Clove</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Variable</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Implemented</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Application data</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">12-223</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">-</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">-</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Future use</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">224-253</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Experimental</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Variable</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">-</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Testing features</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">254</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Padding</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Variable</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Implemented</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Traffic shaping</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">255</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">-</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">-</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Future extension</td>
    </tr>
  </tbody>
</table>
**Xử lý khối không xác định:**

Các triển khai PHẢI bỏ qua các khối có mã kiểu không xác định và coi chúng như phần đệm. Điều này đảm bảo khả năng tương thích tiến.

### Quy tắc sắp xếp các khối

### Thứ tự thông điệp NS

**Bắt buộc:** - Khối DateTime PHẢI đứng đầu tiên

**Được phép:** - Garlic Clove (tiểu thông điệp trong garlic encryption) (type 11) - Tùy chọn (type 5) - nếu được triển khai - Đệm (type 254)

**Bị cấm:** - NextKey, ACK, ACK Request, Termination, MessageNumbers

**Ví dụ về payload NS hợp lệ:**

```
DateTime (0) | Garlic Clove (11) | Garlic Clove (11) | Padding (254)
```
### Thứ tự thông điệp NSR (viết tắt, không dịch)

**Bắt buộc:** - Không có (payload (dữ liệu tải) có thể rỗng)

**Được phép:** - Garlic Clove (đơn vị thông điệp con trong garlic encryption) (loại 11) - Tùy chọn (loại 5) - nếu được triển khai - Đệm (loại 254)

**Không được phép:** - DateTime, NextKey, ACK, ACK Request, Termination, MessageNumbers

**Ví dụ về payload (nội dung dữ liệu) NSR hợp lệ:**

```
Garlic Clove (11) | Garlic Clove (11) | Padding (254)
```
hoặc

```
(empty - ACK only)
```
### Thứ tự thông điệp ES

**Bắt buộc:** - Không có (payload có thể để trống)

**Được phép (theo bất kỳ thứ tự nào):** - Garlic Clove (type 11) - NextKey (type 7) - ACK (type 8) - ACK Request (type 9) - Termination (type 4) - nếu được triển khai - MessageNumbers (type 6) - nếu được triển khai - Options (type 5) - nếu được triển khai - Padding (type 254)

**Quy tắc đặc biệt:** - Termination PHẢI là khối cuối cùng (trừ Padding) - Padding PHẢI là khối cuối cùng - Cho phép nhiều Garlic Cloves - Cho phép tối đa 2 khối NextKey (xuôi và ngược) - KHÔNG cho phép nhiều khối Padding

**Ví dụ các payload ES hợp lệ:**

```
Garlic Clove (11) | ACK (8) | Padding (254)
```
```
NextKey (7) | Garlic Clove (11) | Garlic Clove (11)
```
```
NextKey (7) forward | NextKey (7) reverse | Garlic Clove (11)
```
```
ACK Request (9) | Garlic Clove (11) | Termination (4) | Padding (254)
```
### DateTime Block (khối ngày giờ) (Loại 0)

**Mục đích**: Dấu thời gian để ngăn chặn phát lại và xác thực độ lệch đồng hồ

**Kích thước**: 7 byte (tiêu đề 3 byte + dữ liệu 4 byte)

**Định dạng:**

```
+----+----+----+----+----+----+----+
| 0  |    4    |     timestamp     |
+----+----+----+----+----+----+----+
```
**Các trường:**

- `blk`: 0
- `size`: 4 (big-endian - byte có trọng số lớn nhất trước)
- `timestamp`: 4 byte - dấu thời gian Unix tính bằng giây (không dấu, big-endian)

**Định dạng dấu thời gian:**

```python
timestamp = int(time.time())  # Seconds since 1970-01-01 00:00:00 UTC
# Wraps around in year 2106 (4-byte unsigned maximum)
```
**Quy tắc kiểm tra hợp lệ:**

```python
MAX_CLOCK_SKEW_PAST = 5 * 60      # 5 minutes
MAX_CLOCK_SKEW_FUTURE = 2 * 60    # 2 minutes

def validate_datetime(timestamp):
    now = int(time.time())
    age = now - timestamp
    
    if age < -MAX_CLOCK_SKEW_FUTURE:
        return False  # Too far in future
    
    if age > MAX_CLOCK_SKEW_PAST:
        return False  # Too old
    
    return True
```
**Ngăn chặn phát lại:**

```python
class ReplayFilter:
    def __init__(self, duration=5*60):
        self.duration = duration  # 5 minutes
        self.seen_messages = BloomFilter(size=100000, false_positive_rate=0.001)
        self.cleanup_timer = RepeatTimer(60, self.cleanup)
    
    def check_replay(self, ephemeral_key, timestamp):
        # Check timestamp validity
        if not validate_datetime(timestamp):
            return False
        
        # Check if ephemeral key seen recently
        if ephemeral_key in self.seen_messages:
            return False  # Replay attack
        
        # Add to seen messages
        self.seen_messages.add(ephemeral_key)
        return True
    
    def cleanup(self):
        # Expire old entries (Bloom filter automatically ages out)
        pass
```
**Ghi chú triển khai:**

1. **NS Messages**: DateTime PHẢI là khối đầu tiên
2. **NSR/ES Messages**: Thông thường không bao gồm DateTime
3. **Cửa sổ phát lại**: 5 phút là mức tối thiểu được khuyến nghị
4. **Bộ lọc Bloom**: Được khuyến nghị để phát hiện phát lại hiệu quả
5. **Độ lệch đồng hồ**: Cho phép muộn 5 phút, sớm 2 phút

### Garlic Clove Block (khối nhánh tỏi) (Type 11)

**Mục đích**: Đóng gói các thông điệp I2NP để chuyển giao

**Định dạng:**

```
+----+----+----+----+----+----+----+----+
| 11 |  size   |                        |
+----+----+----+                        +
|      Delivery Instructions            |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|type|  Message_ID       | Expiration  |
+----+----+----+----+----+----+----+----+
     |      I2NP Message body           |
+----+                                  +
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
```
**Các trường:**

- `blk`: 11
- `size`: Tổng kích thước của clove (nhánh trong thông điệp garlic) (biến đổi)
- `Delivery Instructions`: Như được quy định trong đặc tả I2NP
- `type`: Kiểu thông điệp I2NP (1 byte)
- `Message_ID`: ID thông điệp I2NP (4 byte)
- `Expiration`: Dấu thời gian Unix tính bằng giây (4 byte)
- `I2NP Message body`: Dữ liệu thông điệp có độ dài biến đổi

**Định dạng hướng dẫn chuyển phát:**

**Phân phối cục bộ** (1 byte):

```
+----+
|0x00|
+----+
```
**Giao tới Destination (đích)** (33 byte):

```
+----+----+----+----+----+----+----+----+
|0x01|                                  |
+----+        Destination Hash         +
|              32 bytes                 |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
```
**Router Delivery** (33 byte):

```
+----+----+----+----+----+----+----+----+
|0x02|                                  |
+----+         Router Hash              +
|              32 bytes                 |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
```
**Chuyển giao qua Tunnel** (37 bytes):

```
+----+----+----+----+----+----+----+----+
|0x03|         Tunnel ID                |
+----+----+----+----+----+              +
|           Router Hash                 |
+              32 bytes                 +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
```
**Tiêu đề thông điệp I2NP** (tổng cộng 9 byte):

```
+----+----+----+----+----+----+----+----+
|type|      msg_id       |  expiration   |
+----+----+----+----+----+----+----+----+
     |                                   |
```
- `type`: loại thông điệp I2NP (Database Store, Database Lookup, Data, v.v.)
- `msg_id`: định danh thông điệp 4 byte
- `expiration`: dấu thời gian Unix 4 byte (giây)

**Những khác biệt quan trọng so với Định dạng Clove ElGamal (Clove: nhánh trong garlic encryption):**

1. **Không có Chứng chỉ**: Trường Chứng chỉ bị lược bỏ (không dùng trong ElGamal)
2. **Không có Clove ID**: Clove ID bị lược bỏ (Clove: tiểu thông điệp trong garlic encryption; vốn luôn là 0)
3. **Không có thời điểm hết hạn của Clove**: Thay vào đó dùng thời điểm hết hạn của thông điệp I2NP
4. **Header gọn**: Header I2NP 9-byte so với định dạng ElGamal lớn hơn
5. **Mỗi Clove là một khối riêng biệt**: Không có cấu trúc CloveSet (tập hợp các Clove)

**Nhiều Clove (thành phần con của thông điệp trong garlic encryption):**

```python
# Multiple Garlic Cloves in one message
payload = [
    build_datetime_block(),
    build_garlic_clove(i2np_message_1),
    build_garlic_clove(i2np_message_2),
    build_garlic_clove(i2np_message_3),
    build_padding_block()
]
```
**Các kiểu thông điệp I2NP phổ biến trong Cloves (tép tỏi):**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Name</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DatabaseStore</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Publishing LeaseSet</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DatabaseLookup</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Requesting LeaseSet</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DeliveryStatus</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ACK (legacy, avoid in ECIES)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">20</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Data</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Streaming data</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">21</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Garlic</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Nested garlic messages</td>
    </tr>
  </tbody>
</table>
**Xử lý Clove (thông điệp con trong 'garlic' message):**

```python
def process_garlic_clove(clove_data):
    # Parse delivery instructions
    delivery_type = clove_data[0]
    
    if delivery_type == 0x00:
        # Local delivery
        offset = 1
    elif delivery_type == 0x01:
        # Destination delivery
        dest_hash = clove_data[1:33]
        offset = 33
    elif delivery_type == 0x02:
        # Router delivery
        router_hash = clove_data[1:33]
        offset = 33
    elif delivery_type == 0x03:
        # Tunnel delivery
        tunnel_id = struct.unpack('>I', clove_data[1:5])[0]
        router_hash = clove_data[5:37]
        offset = 37
    
    # Parse I2NP header
    i2np_type = clove_data[offset]
    msg_id = struct.unpack('>I', clove_data[offset+1:offset+5])[0]
    expiration = struct.unpack('>I', clove_data[offset+5:offset+9])[0]
    
    # Extract I2NP body
    i2np_body = clove_data[offset+9:]
    
    # Process message
    process_i2np_message(i2np_type, msg_id, expiration, i2np_body)
```
### Khối NextKey (khóa kế tiếp) (Loại 7)

**Mục đích**: trao đổi khóa DH ratchet (cơ chế bánh cóc)

**Định dạng (Có khóa - 38 byte):**

```
+----+----+----+----+----+----+----+----+
| 7  |   35    |flag|  key ID |         |
+----+----+----+----+----+----+         +
|                                       |
+     Next DH Ratchet Public Key        +
|              32 bytes                 |
+                                       +
|                                       |
+                             +----+----+
|                             |
+----+----+----+----+----+----+
```
**Định dạng (Chỉ Key ID - 6 byte):**

```
+----+----+----+----+----+----+
| 7  |    3    |flag|  key ID |
+----+----+----+----+----+----+
```
**Các trường:**

- `blk`: 7
- `size`: 3 (chỉ ID) hoặc 35 (kèm khóa)
- `flag`: 1 byte - các bit cờ
- `key ID`: 2 byte - định danh khóa theo Big-endian (thứ tự byte có trọng số lớn trước) (0-32767)
- `Public Key`: 32 byte - khóa công khai X25519 (little-endian - thứ tự byte có trọng số nhỏ trước), nếu bit cờ 0 = 1

**Các bit cờ:**

```
Bit 7 6 5 4 3 2 1 0
    | | | | | | | |
    | | | | | | | +-- Bit 0: Key present (1) or ID only (0)
    | | | | | | +---- Bit 1: Reverse key (1) or forward key (0)
    | | | | | +------ Bit 2: Request reverse key (1) or no request (0)
    | | | | |
    +-+-+-+-+-------- Bits 3-7: Reserved (set to 0)
```
**Ví dụ về cờ:**

```python
# Forward key present
flags = 0x01  # Binary: 00000001

# Reverse key present
flags = 0x03  # Binary: 00000011

# Forward key ID only (ACK)
flags = 0x00  # Binary: 00000000

# Reverse key ID only (ACK)
flags = 0x02  # Binary: 00000010

# Forward key ID with reverse request
flags = 0x04  # Binary: 00000100
```
**Quy tắc ID khóa:**

- Các ID tăng dần liên tiếp: 0, 1, 2, ..., 32767
- ID chỉ tăng khi tạo khóa mới
- Cùng một ID được dùng cho nhiều thông điệp cho đến lần ratchet (cơ chế xoay vòng khóa) tiếp theo
- ID tối đa là 32767 (sau đó phải bắt đầu phiên mới)

**Ví dụ sử dụng:**

```python
# Initiating ratchet (sender generates new key)
nextkey = NextKeyBlock(
    flags=0x01,           # Key present, forward
    key_id=0,
    public_key=sender_new_pk
)

# Replying to ratchet (receiver generates new key)
nextkey = NextKeyBlock(
    flags=0x03,           # Key present, reverse
    key_id=0,
    public_key=receiver_new_pk
)

# Acknowledging ratchet (no new key from sender)
nextkey = NextKeyBlock(
    flags=0x02,           # ID only, reverse
    key_id=0
)

# Requesting reverse ratchet
nextkey = NextKeyBlock(
    flags=0x04,           # Request reverse, forward ID
    key_id=1
)
```
**Logic xử lý:**

```python
def process_nextkey_block(block):
    flags = block.flags
    key_id = block.key_id
    
    key_present = (flags & 0x01) != 0
    is_reverse = (flags & 0x02) != 0
    request_reverse = (flags & 0x04) != 0
    
    if key_present:
        public_key = block.public_key
        
        if is_reverse:
            # Reverse key received
            perform_dh_ratchet(receiver_key=public_key, key_id=key_id)
            # Sender should ACK with own key ID
        else:
            # Forward key received
            perform_dh_ratchet(sender_key=public_key, key_id=key_id)
            # Receiver should reply with reverse key
            send_reverse_key(generate_new_key())
    
    else:
        # Key ID only (ACK)
        if is_reverse:
            # Reverse key ACK
            confirm_reverse_ratchet(key_id)
        else:
            # Forward key ACK
            confirm_forward_ratchet(key_id)
    
    if request_reverse:
        # Sender requests receiver to generate new key
        send_reverse_key(generate_new_key())
```
**Nhiều khối NextKey:**

Một thông điệp ES có thể chứa tối đa 2 khối NextKey khi cả hai chiều cùng thực hiện ratcheting (cơ chế ratchet tăng bậc khóa) đồng thời:

```python
# Both directions ratcheting
payload = [
    NextKeyBlock(flags=0x01, key_id=2, public_key=forward_key),  # Forward
    NextKeyBlock(flags=0x03, key_id=1, public_key=reverse_key),  # Reverse
    build_garlic_clove(data)
]
```
### Khối ACK (Loại 8)

**Mục đích**: Xác nhận các thông điệp đã nhận in-band (trong cùng kênh)

**Định dạng (ACK đơn - 7 byte):**

```
+----+----+----+----+----+----+----+
| 8  |    4    |tagsetid |   N     |
+----+----+----+----+----+----+----+
```
**Định dạng (nhiều ACK):**

```
+----+----+----+----+----+----+----+----+
| 8  |  size   |tagsetid |   N     |    |
+----+----+----+----+----+----+----+    +
|            more ACKs                  |
~               ...                     ~
|                                       |
+----+----+----+----+----+----+----+----+
```
**Các trường:**

- `blk`: 8
- `size`: 4 * số lượng ACK (gói xác nhận) (tối thiểu 4)
- Đối với mỗi ACK:
  - `tagsetid`: 2 byte - ID tập thẻ Big-endian (thứ tự byte lớn trước) (0-65535)
  - `N`: 2 byte - số thông điệp Big-endian (0-65535)

**Xác định ID của tập thẻ:**

```python
# Tag set 0 (initial, after NSR)
tagset_id = 0

# After first ratchet (tag set 1)
# Both Alice and Bob sent key ID 0
tagset_id = 1 + 0 + 0 = 1

# After second ratchet (tag set 2)
# Alice sent key ID 1, Bob still using key ID 0
tagset_id = 1 + 1 + 0 = 2

# After third ratchet (tag set 3)
# Alice still using key ID 1, Bob sent key ID 1
tagset_id = 1 + 1 + 1 = 3
```
**Ví dụ về ACK đơn lẻ:**

```python
# ACK message from tag set 5, message number 127
ack_block = ACKBlock(
    tagset_id=5,
    message_number=127
)

# Wire format (7 bytes):
# 08 00 04 00 05 00 7F
# |  |  |  |  |  |  |
# |  |  |  |  |  |  +-- N (127)
# |  |  |  |  +--------- N high byte
# |  |  |  +------------ tagset_id (5)
# |  |  +--------------- tagset_id high byte
# |  +------------------ size (4)
# +--------------------- type (8)
```
**Ví dụ về nhiều ACK (thông điệp xác nhận):**

```python
# ACK three messages
ack_block = ACKBlock([
    (tagset_id=3, N=42),
    (tagset_id=3, N=43),
    (tagset_id=4, N=0)
])

# Wire format (15 bytes):
# 08 00 0C 00 03 00 2A 00 03 00 2B 00 04 00 00
#                (ts=3, N=42) (ts=3, N=43) (ts=4, N=0)
```
**Xử lý:**

```python
def process_ack_block(block):
    num_acks = block.size // 4
    
    for i in range(num_acks):
        offset = i * 4
        tagset_id = struct.unpack('>H', block.data[offset:offset+2])[0]
        message_num = struct.unpack('>H', block.data[offset+2:offset+4])[0]
        
        # Mark message as acknowledged
        mark_acked(tagset_id, message_num)
        
        # May trigger retransmission timeout cancellation
        cancel_retransmit_timer(tagset_id, message_num)
```
**Khi nào cần gửi ACKs (thông báo xác nhận):**

1. **Yêu cầu ACK (xác nhận) tường minh**: Luôn phản hồi khối ACK Request
2. **Chuyển giao LeaseSet**: Khi bên gửi bao gồm LeaseSet trong thông điệp
3. **Thiết lập phiên**: Có thể ACK NS/NSR (dù giao thức ưu tiên ACK ngầm qua ES)
4. **Xác nhận Ratchet**: Có thể ACK việc nhận NextKey
5. **Tầng ứng dụng**: Theo yêu cầu của giao thức tầng cao hơn (ví dụ: Streaming)

**Thời gian ACK (gói xác nhận):**

```python
class ACKManager:
    def __init__(self):
        self.pending_acks = []
        self.ack_timer = None
    
    def request_ack(self, tagset_id, message_num):
        self.pending_acks.append((tagset_id, message_num))
        
        if not self.ack_timer:
            # Delay ACK briefly to allow higher layer to respond
            self.ack_timer = set_timer(0.1, self.send_acks)  # 100ms
    
    def send_acks(self):
        if self.pending_acks and not has_outbound_data():
            # No higher layer data, send explicit ACK
            send_es_message(build_ack_block(self.pending_acks))
        
        # Otherwise, ACK will piggyback on next ES message
        self.pending_acks = []
        self.ack_timer = None
```
### Khối yêu cầu ACK (Loại 9)

**Mục đích**: Yêu cầu in-band acknowledgment (xác nhận cùng kênh) cho thông điệp hiện tại

**Định dạng:**

```
+----+----+----+----+
| 9  |    1    |flg |
+----+----+----+----+
```
**Các trường:**

- `blk`: 9
- `size`: 1
- `flg`: 1 byte - Cờ (tất cả các bit hiện không sử dụng, đặt về 0)

**Cách sử dụng:**

```python
# Request ACK for this message
payload = [
    build_ack_request_block(),
    build_garlic_clove(important_data)
]
```
**Phản hồi của phía nhận:**

Khi nhận được yêu cầu ACK (xác nhận):

1. **Có dữ liệu tức thời**: Bao gồm khối ACK trong phản hồi tức thời
2. **Không có dữ liệu tức thời**: Khởi động bộ đếm thời gian (ví dụ, 100ms) và gửi ES rỗng kèm ACK nếu bộ đếm hết hạn
3. **Tag Set ID (mã định danh tập thẻ)**: Sử dụng Tag Set ID của tập thẻ vào hiện tại
4. **Message Number (số hiệu thông điệp)**: Sử dụng Message Number gắn với session tag (thẻ phiên) đã nhận

**Xử lý:**

```python
def process_ack_request(message):
    # Extract message identification
    tagset_id = message.tagset_id
    message_num = message.message_num
    
    # Schedule ACK
    schedule_ack(tagset_id, message_num)
    
    # If no data to send immediately, start timer
    if not has_pending_data():
        set_timer(0.1, lambda: send_ack_only(tagset_id, message_num))
```
**Khi nào nên sử dụng ACK Request (yêu cầu xác nhận):**

1. **Thông điệp trọng yếu**: Các thông điệp bắt buộc phải được xác nhận
2. **Chuyển giao LeaseSet**: Khi đóng gói kèm một LeaseSet
3. **Session Ratchet (cơ chế gài răng phiên – thay khóa liên tục)**: Sau khi gửi khối NextKey (khối chứa khóa tiếp theo)
4. **Kết thúc truyền**: Khi bên gửi không còn dữ liệu để gửi nhưng vẫn muốn nhận xác nhận

**Khi KHÔNG nên sử dụng:**

1. **Giao thức Streaming**: Lớp streaming xử lý ACK (gói xác nhận)
2. **Thông điệp tần suất cao**: Tránh yêu cầu ACK trên mọi thông điệp (chi phí phụ trội)
3. **Các datagram không quan trọng**: Các datagram thô thường không cần ACK

### Khối Kết thúc (Loại 4)

**Trạng thái**: Chưa được triển khai

**Mục đích**: Kết thúc phiên một cách an toàn

**Định dạng:**

```
+----+----+----+----+----+----+----+----+
| 4  |  size   | rsn|     addl data     |
+----+----+----+----+                   +
~               ...                     ~
+----+----+----+----+----+----+----+----+
```
**Các trường:**

- `blk`: 4
- `size`: từ 1 byte trở lên
- `rsn`: 1 byte - Mã lý do
- `addl data`: Dữ liệu bổ sung tùy chọn (định dạng tùy thuộc vào lý do)

**Mã lý do:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Meaning</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Additional Data</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Normal close / unspecified</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">None</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Termination received</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">None</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Idle timeout</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">None (implementation-specific)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Resource exhaustion</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">None (implementation-specific)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4+</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Implementation-specific</td>
    </tr>
  </tbody>
</table>
**Cách sử dụng (khi được triển khai):**

```python
# Normal session close
termination = TerminationBlock(
    reason=0,
    additional_data=b''
)

# Session termination due to received termination
termination = TerminationBlock(
    reason=1,
    additional_data=b''
)
```
**Quy tắc:**

- PHẢI là khối cuối cùng, ngoại trừ Padding (đệm)
- Padding PHẢI theo sau Termination (kết thúc) nếu có
- Không được phép trong các thông điệp NS hoặc NSR
- Chỉ được phép trong các thông điệp ES

### Khối tùy chọn (Loại 5)

**Trạng thái**: CHƯA TRIỂN KHAI

**Mục đích**: Thương lượng các tham số phiên

**Định dạng:**

```
+----+----+----+----+----+----+----+----+
| 5  |  size   |ver |flg |STL |STimeout |
+----+----+----+----+----+----+----+----+
|  SOTW   |  RITW   |tmin|tmax|rmin|rmax|
+----+----+----+----+----+----+----+----+
|  tdmy   |  rdmy   |  tdelay |  rdelay |
+----+----+----+----+----+----+----+----+
|              more_options             |
~               ...                     ~
|                                       |
+----+----+----+----+----+----+----+----+
```
**Các trường:**

- `blk`: 5
- `size`: 21 byte trở lên
- `ver`: 1 byte - Phiên bản giao thức (phải là 0)
- `flg`: 1 byte - Cờ (hiện tại tất cả các bit chưa được sử dụng)
- `STL`: 1 byte - Độ dài thẻ phiên (phải là 8)
- `STimeout`: 2 byte - Thời gian chờ không hoạt động của phiên tính bằng giây (big-endian (thứ tự byte lớn trước))
- `SOTW`: 2 byte - Cửa sổ thẻ gửi đi của phía gửi (big-endian)
- `RITW`: 2 byte - Cửa sổ thẻ nhận vào của phía nhận (big-endian)
- `tmin`, `tmax`, `rmin`, `rmax`: mỗi cái 1 byte - Các tham số đệm (4.4 fixed-point (định dạng số dấu phẩy cố định 4.4))
- `tdmy`: 2 byte - Lưu lượng giả tối đa sẵn sàng gửi (byte/giây, big-endian)
- `rdmy`: 2 byte - Lưu lượng giả được yêu cầu (byte/giây, big-endian)
- `tdelay`: 2 byte - Độ trễ tối đa bên trong thông điệp sẵn sàng chèn (msec, big-endian)
- `rdelay`: 2 byte - Độ trễ bên trong thông điệp được yêu cầu (msec, big-endian)
- `more_options`: Biến (độ dài thay đổi) - Các phần mở rộng trong tương lai

**Tham số đệm (dạng dấu phẩy cố định 4.4):**

```python
def encode_padding_ratio(ratio):
    """
    Encode padding ratio as 4.4 fixed-point
    
    ratio: 0.0 to 15.9375
    returns: 0x00 to 0xFF
    """
    return int(ratio * 16)

def decode_padding_ratio(encoded):
    """
    Decode 4.4 fixed-point to ratio
    
    encoded: 0x00 to 0xFF
    returns: 0.0 to 15.9375
    """
    return encoded / 16.0

# Examples:
# 0x00 = 0.0 (no padding)
# 0x01 = 0.0625 (6.25% padding)
# 0x10 = 1.0 (100% padding - double traffic)
# 0x80 = 8.0 (800% padding - 9x traffic)
# 0xFF = 15.9375 (1593.75% padding)
```
**Thương lượng Tag Window (cửa sổ thẻ):**

```python
# SOTW: Sender's recommendation for receiver's inbound window
# RITW: Sender's declaration of own inbound window

# Receiver calculates actual inbound window:
inbound_window = calculate_window(
    sender_suggestion=SOTW,
    own_constraints=MAX_INBOUND_TAGS,
    own_resources=available_memory()
)

# Sender uses:
# - RITW to know how far ahead receiver will accept
# - Own SOTW to hint optimal window size
```
**Giá trị mặc định (khi các tùy chọn không được đàm phán):**

```python
DEFAULT_OPTIONS = {
    'version': 0,
    'session_tag_length': 8,
    'session_timeout': 600,  # 10 minutes
    'sender_outbound_tag_window': 160,
    'receiver_inbound_tag_window': 160,
    'tmin': 0x00,  # No minimum padding
    'tmax': 0x10,  # Up to 100% padding
    'rmin': 0x00,  # No minimum requested
    'rmax': 0x10,  # Up to 100% requested
    'tdmy': 0,     # No dummy traffic
    'rdmy': 0,     # No dummy traffic requested
    'tdelay': 0,   # No delay
    'rdelay': 0    # No delay requested
}
```
### Khối MessageNumbers (Loại 6)

**Trạng thái**: CHƯA TRIỂN KHAI

**Mục đích**: Chỉ ra tin nhắn cuối cùng được gửi trong tập thẻ trước đó (cho phép phát hiện khoảng trống)

**Định dạng:**

```
+----+----+----+----+----+
| 6  |    2    |  PN    |
+----+----+----+----+----+
```
**Các trường:**

- `blk`: 6
- `size`: 2
- `PN`: 2 byte - Số thứ tự thông điệp cuối cùng của tập thẻ trước (big-endian (thứ tự byte lớn trước), 0-65535)

**Định nghĩa PN (Previous Number):**

PN là chỉ số của thẻ cuối cùng đã được gửi trong tập thẻ trước đó.

**Cách sử dụng (khi được triển khai):**

```python
# After ratcheting to new tag set
# Old tag set: sent messages 0-4095
# New tag set: sending first message

payload = [
    MessageNumbersBlock(PN=4095),
    build_garlic_clove(data)
]
```
**Lợi ích cho bên nhận:**

```python
def process_message_numbers(pn_value):
    # Receiver can now:
    
    # 1. Determine if any messages were skipped
    highest_received_in_old_tagset = 4090
    if pn_value > highest_received_in_old_tagset:
        missing_count = pn_value - highest_received_in_old_tagset
        # 5 messages were never received
    
    # 2. Delete tags higher than PN from old tagset
    for tag_index in range(pn_value + 1, MAX_TAG_INDEX):
        delete_tag(old_tagset, tag_index)
    
    # 3. Expire tags ≤ PN after grace period (e.g., 2 minutes)
    schedule_deletion(old_tagset, delay=120)
```
**Quy tắc:**

- KHÔNG ĐƯỢC gửi trong tag set (nhóm thẻ) 0 (không có tag set trước đó)
- Chỉ được gửi trong ES messages (thông điệp ES)
- Chỉ được gửi trong những thông điệp đầu tiên của tag set mới
- Giá trị PN là từ góc nhìn của người gửi (tag (thẻ) cuối cùng mà người gửi đã gửi)

**Mối quan hệ với Signal:**

Trong Signal Double Ratchet (giao thức Double Ratchet của Signal), PN nằm trong phần đầu của thông điệp. Trong ECIES (lược đồ mã hóa tích hợp trên đường cong elliptic), PN nằm trong payload đã mã hóa và là tùy chọn.

### Khối đệm (Loại 254)

**Mục đích**: Khả năng chống phân tích lưu lượng và che giấu kích thước thông điệp

**Định dạng:**

```
+----+----+----+----+----+----+----+----+
|254 |  size   |      padding           |
+----+----+----+                        +
|                                       |
~               ...                     ~
|                                       |
+----+----+----+----+----+----+----+----+
```
**Các trường:**

- `blk`: 254
- `size`: 0-65516 byte (big-endian: thứ tự byte lớn trước)
- `padding`: Dữ liệu ngẫu nhiên hoặc bằng 0

**Quy tắc:**

- PHẢI là khối cuối cùng trong thông điệp
- KHÔNG được phép có nhiều khối Padding (đệm)
- Có thể có độ dài bằng 0 (chỉ có phần đầu 3 byte)
- Dữ liệu Padding có thể là các số 0 hoặc các byte ngẫu nhiên

**Đệm mặc định:**

```python
DEFAULT_PADDING_MIN = 0
DEFAULT_PADDING_MAX = 15

def generate_default_padding():
    size = random.randint(DEFAULT_PADDING_MIN, DEFAULT_PADDING_MAX)
    data = random.bytes(size)  # or zeros
    return PaddingBlock(size, data)
```
**Chiến lược chống phân tích lưu lượng:**

**Chiến lược 1: Kích thước ngẫu nhiên (Mặc định)**

```python
# Add 0-15 bytes random padding to each message
padding_size = random.randint(0, 15)
padding_block = PaddingBlock(padding_size, random.bytes(padding_size))
```
**Chiến lược 2: Làm tròn đến bội số**

```python
# Round total message size to next multiple of 64
target_size = ((message_size + 63) // 64) * 64
padding_size = target_size - message_size - 3  # -3 for block header
padding_block = PaddingBlock(padding_size, random.bytes(padding_size))
```
**Chiến lược 3: Kích thước thông điệp cố định**

```python
# Always send 1KB messages
TARGET_MESSAGE_SIZE = 1024
padding_size = TARGET_MESSAGE_SIZE - message_size - 3
padding_block = PaddingBlock(padding_size, random.bytes(padding_size))
```
**Chiến lược 4: Đệm được đàm phán (khối Options)**

```python
# Calculate padding based on negotiated parameters
# tmin, tmax from Options block
min_padding = int(payload_size * tmin_ratio)
max_padding = int(payload_size * tmax_ratio)
padding_size = random.randint(min_padding, max_padding)
padding_block = PaddingBlock(padding_size, random.bytes(padding_size))
```
**Padding-Only Messages (các thông điệp chỉ chứa đệm):**

Thông điệp có thể chỉ gồm phần đệm (không có dữ liệu ứng dụng):

```python
# Dummy traffic message
payload = [
    PaddingBlock(random.randint(100, 500), random.bytes(...))
]
```
**Ghi chú triển khai:**

1. **Đệm toàn số 0**: Chấp nhận được (sẽ được ChaCha20 mã hóa)
2. **Đệm ngẫu nhiên**: Không cung cấp thêm bảo mật sau khi đã mã hóa nhưng tiêu tốn nhiều entropy (độ ngẫu nhiên) hơn
3. **Hiệu năng**: Việc tạo đệm ngẫu nhiên có thể tốn kém; cân nhắc dùng đệm toàn số 0
4. **Bộ nhớ**: Khối đệm lớn tiêu tốn băng thông; hãy thận trọng với kích thước tối đa

---

## Hướng dẫn triển khai

### Điều kiện tiên quyết

**Thư viện mật mã:**

- **X25519**: libsodium, NaCl, hoặc Bouncy Castle
- **ChaCha20-Poly1305**: libsodium, OpenSSL 1.1.0+, hoặc Bouncy Castle
- **SHA-256**: OpenSSL, Bouncy Castle, hoặc hỗ trợ tích hợp sẵn trong ngôn ngữ
- **Elligator2**: Hỗ trợ thư viện hạn chế; có thể cần triển khai tùy chỉnh

**Triển khai Elligator2 (kỹ thuật che giấu điểm trên đường cong elliptic):**

Elligator2 (kỹ thuật ánh xạ điểm trên đường cong elliptic thành chuỗi trông ngẫu nhiên) không được triển khai rộng rãi. Các lựa chọn:

1. **OBFS4**: pluggable transport (cơ chế vận chuyển cắm thêm) obfs4 của Tor bao gồm triển khai Elligator2 (kỹ thuật ánh xạ trên đường cong elliptic để ngụy trang khóa công khai)
2. **Triển khai tùy chỉnh**: Dựa trên [bài báo Elligator2](https://elligator.cr.yp.to/elligator-20130828.pdf)
3. **kleshni/Elligator**: Triển khai tham chiếu trên GitHub

**Ghi chú Java I2P:** Java I2P sử dụng thư viện net.i2p.crypto.eddsa với các phần bổ sung Elligator2 (kỹ thuật ánh xạ điểm trên đường cong elliptic trông ngẫu nhiên) tùy chỉnh.

### Thứ tự triển khai được khuyến nghị

**Giai đoạn 1: Mật mã cốt lõi** 1. Tạo và trao đổi khóa X25519 DH (Diffie–Hellman) 2. Mã hóa/giải mã ChaCha20-Poly1305 AEAD (mã hóa xác thực kèm dữ liệu bổ sung) 3. Băm SHA-256 và MixHash (hàm băm trộn) 4. Dẫn xuất khóa với HKDF (hàm dẫn xuất khóa) 5. Mã hóa/giải mã Elligator2 (kỹ thuật ánh xạ ngụy trang) (có thể dùng test vectors (bộ dữ liệu kiểm thử) ban đầu)

**Giai đoạn 2: Định dạng thông điệp** 1. Thông điệp NS (không ràng buộc) - định dạng đơn giản nhất 2. Thông điệp NS (ràng buộc) - bổ sung khóa tĩnh 3. Thông điệp NSR 4. Thông điệp ES 5. Phân tích cú pháp khối và tạo khối

**Giai đoạn 3: Quản lý phiên** 1. Tạo và lưu trữ phiên 2. Quản lý tập thẻ (người gửi và người nhận) 3. Ratchet (cơ chế bánh cóc) thẻ phiên 4. Ratchet khóa đối xứng 5. Tra cứu thẻ và quản lý cửa sổ

**Giai đoạn 4: DH Ratcheting (cơ chế bánh cóc Diffie–Hellman)** 1. Xử lý khối NextKey 2. KDF (hàm dẫn xuất khóa) cho DH ratchet 3. Tạo tag set (tập thẻ) sau khi ratchet 4. Quản lý nhiều tag set

**Giai đoạn 5: Logic giao thức** 1. Máy trạng thái NS/NSR/ES 2. Ngăn phát lại (DateTime, bộ lọc Bloom) 3. Logic truyền lại (nhiều NS/NSR) 4. Xử lý ACK

**Giai đoạn 6: Tích hợp** 1. Xử lý I2NP Garlic Clove (tép trong thông điệp garlic của I2NP) 2. Đính kèm LeaseSet 3. Tích hợp giao thức truyền luồng 4. Tích hợp giao thức datagram

### Triển khai phía gửi

**Vòng đời của phiên gửi đi:**

```python
class OutboundSession:
    def __init__(self, destination, bound=True):
        self.destination = destination
        self.bound = bound
        self.state = SessionState.NEW
        
        # Keys for NS message
        self.ephemeral_keypair = generate_elg2_keypair()
        if bound:
            self.static_key = context.static_keypair
        
        # Will be populated after NSR
        self.outbound_tagset = None
        self.outbound_keyratchet = None
        self.inbound_tagset = None
        self.inbound_keyratchet = None
        
        # Timing
        self.created_time = now()
        self.last_activity = now()
        
        # Retransmission
        self.ns_attempts = []
        self.ns_timer = None
    
    def send_initial_message(self, payload):
        """Send NS message"""
        # Build NS message
        ns_message = self.build_ns_message(payload)
        
        # Send
        send_to_network(self.destination, ns_message)
        
        # Track for retransmission
        self.ns_attempts.append({
            'message': ns_message,
            'time': now(),
            'ephemeral_key': self.ephemeral_keypair,
            'kdf_state': self.save_kdf_state()
        })
        
        # Start timer
        self.ns_timer = set_timer(1.0, self.on_ns_timeout)
        self.state = SessionState.PENDING_REPLY
    
    def build_ns_message(self, payload):
        """Construct NS message"""
        # KDF initialization
        chainKey, h = self.initialize_kdf()
        
        # Ephemeral key section
        elg2_ephemeral = ENCODE_ELG2(self.ephemeral_keypair.public_key)
        h = SHA256(h || self.destination.static_key)
        h = SHA256(h || self.ephemeral_keypair.public_key)
        
        # es DH
        es_shared = DH(self.ephemeral_keypair.private_key, 
                       self.destination.static_key)
        keydata = HKDF(chainKey, es_shared, "", 64)
        chainKey = keydata[0:31]
        k_static = keydata[32:63]
        
        # Encrypt static key section
        if self.bound:
            static_section = self.static_key.public_key
        else:
            static_section = bytes(32)
        
        static_ciphertext = ENCRYPT(k_static, 0, static_section, h)
        h = SHA256(h || static_ciphertext)
        
        # ss DH (if bound)
        if self.bound:
            ss_shared = DH(self.static_key.private_key, 
                          self.destination.static_key)
            keydata = HKDF(chainKey, ss_shared, "", 64)
            chainKey = keydata[0:31]
            k_payload = keydata[32:63]
            nonce = 0
        else:
            k_payload = k_static
            nonce = 1
        
        # Build payload blocks
        payload_data = self.build_ns_payload(payload)
        
        # Encrypt payload
        payload_ciphertext = ENCRYPT(k_payload, nonce, payload_data, h)
        h = SHA256(h || payload_ciphertext)
        
        # Save KDF state for NSR processing
        self.ns_chainkey = chainKey
        self.ns_hash = h
        
        # Assemble message
        return elg2_ephemeral + static_ciphertext + payload_ciphertext
    
    def build_ns_payload(self, application_data):
        """Build NS payload blocks"""
        blocks = []
        
        # DateTime block (required, first)
        blocks.append(build_datetime_block())
        
        # Garlic Clove(s) with application data
        blocks.append(build_garlic_clove(application_data))
        
        # Optionally bundle LeaseSet
        if should_send_leaseset():
            blocks.append(build_garlic_clove(build_leaseset_store()))
        
        # Padding
        blocks.append(build_padding_block(random.randint(0, 15)))
        
        return encode_blocks(blocks)
    
    def on_nsr_received(self, nsr_message):
        """Process NSR and establish ES session"""
        # Cancel retransmission timer
        cancel_timer(self.ns_timer)
        
        # Parse NSR
        tag = nsr_message[0:8]
        elg2_bob_ephemeral = nsr_message[8:40]
        key_section_mac = nsr_message[40:56]
        payload_ciphertext = nsr_message[56:]
        
        # Find corresponding NS attempt
        ns_state = self.find_ns_by_tag(tag)
        if not ns_state:
            raise ValueError("NSR tag doesn't match any NS")
        
        # Restore KDF state
        chainKey = ns_state['chainkey']
        h = ns_state['hash']
        
        # Decode Bob's ephemeral key
        bob_ephemeral = DECODE_ELG2(elg2_bob_ephemeral)
        
        # Mix tag and Bob's ephemeral into hash
        h = SHA256(h || tag)
        h = SHA256(h || bob_ephemeral)
        
        # ee DH
        ee_shared = DH(self.ephemeral_keypair.private_key, bob_ephemeral)
        keydata = HKDF(chainKey, ee_shared, "", 32)
        chainKey = keydata[0:31]
        
        # se DH
        se_shared = DH(self.static_key.private_key, bob_ephemeral)
        keydata = HKDF(chainKey, se_shared, "", 64)
        chainKey = keydata[0:31]
        k_key_section = keydata[32:63]
        
        # Verify key section MAC
        try:
            DECRYPT(k_key_section, 0, key_section_mac, h)
        except AuthenticationError:
            raise ValueError("NSR key section MAC verification failed")
        
        h = SHA256(h || key_section_mac)
        
        # Split for bidirectional ES
        keydata = HKDF(chainKey, ZEROLEN, "", 64)
        k_ab = keydata[0:31]  # Alice → Bob
        k_ba = keydata[32:63]  # Bob → Alice
        
        # Initialize ES tagsets
        self.outbound_tagset = DH_INITIALIZE(chainKey, k_ab)
        self.inbound_tagset = DH_INITIALIZE(chainKey, k_ba)
        
        # Decrypt NSR payload
        k_nsr = HKDF(k_ba, ZEROLEN, "AttachPayloadKDF", 32)
        try:
            payload = DECRYPT(k_nsr, 0, payload_ciphertext, h)
        except AuthenticationError:
            raise ValueError("NSR payload MAC verification failed")
        
        # Process NSR payload blocks
        self.process_payload_blocks(payload)
        
        # Session established
        self.state = SessionState.ESTABLISHED
        self.last_activity = now()
        
        # Send ES message (implicit ACK)
        self.send_es_ack()
    
    def send_es_message(self, payload):
        """Send ES message"""
        if self.state != SessionState.ESTABLISHED:
            raise ValueError("Session not established")
        
        # Get next tag and key
        tag, index = self.outbound_tagset.get_next_tag()
        key = self.outbound_keyratchet.get_key(index)
        
        # Construct nonce
        nonce = construct_nonce(index)
        
        # Build payload blocks
        payload_data = self.build_es_payload(payload)
        
        # AEAD encryption
        ciphertext = ENCRYPT(key, nonce, payload_data, tag)
        
        # Assemble message
        es_message = tag + ciphertext
        
        # Send
        send_to_network(self.destination, es_message)
        
        # Update activity
        self.last_activity = now()
        
        # Check if ratchet needed
        if self.outbound_tagset.should_ratchet():
            self.initiate_ratchet()
```
### Hiện thực phía nhận

**Vòng đời phiên đến:**

```python
class InboundSession:
    def __init__(self):
        self.state = None
        self.bound = False
        self.destination = None
        
        # Keys
        self.remote_ephemeral_key = None
        self.remote_static_key = None
        self.ephemeral_keypair = None
        
        # Tagsets
        self.inbound_tagset = None
        self.outbound_tagset = None
        
        # Timing
        self.created_time = None
        self.last_activity = None
        
        # Paired session
        self.paired_outbound = None
    
    @staticmethod
    def try_decrypt_ns(message):
        """Attempt to decrypt as NS message"""
        # Parse NS structure
        elg2_ephemeral = message[0:32]
        static_ciphertext = message[32:80]  # 32 + 16
        payload_ciphertext = message[80:]
        
        # Decode ephemeral key
        try:
            alice_ephemeral = DECODE_ELG2(elg2_ephemeral)
        except:
            return None  # Not a valid Elligator2 encoding
        
        # Check replay
        if is_replay(alice_ephemeral):
            return None
        
        # KDF initialization
        chainKey, h = initialize_kdf()
        
        # Mix keys
        h = SHA256(h || context.static_keypair.public_key)
        h = SHA256(h || alice_ephemeral)
        
        # es DH
        es_shared = DH(context.static_keypair.private_key, alice_ephemeral)
        keydata = HKDF(chainKey, es_shared, "", 64)
        chainKey = keydata[0:31]
        k_static = keydata[32:63]
        
        # Decrypt static key section
        try:
            static_data = DECRYPT(k_static, 0, static_ciphertext, h)
        except AuthenticationError:
            return None  # Not a valid NS message
        
        h = SHA256(h || static_ciphertext)
        
        # Check if bound or unbound
        if static_data == bytes(32):
            # Unbound
            alice_static_key = None
            k_payload = k_static
            nonce = 1
        else:
            # Bound - perform ss DH
            alice_static_key = static_data
            ss_shared = DH(context.static_keypair.private_key, alice_static_key)
            keydata = HKDF(chainKey, ss_shared, "", 64)
            chainKey = keydata[0:31]
            k_payload = keydata[32:63]
            nonce = 0
        
        # Decrypt payload
        try:
            payload = DECRYPT(k_payload, nonce, payload_ciphertext, h)
        except AuthenticationError:
            return None
        
        h = SHA256(h || payload_ciphertext)
        
        # Create session
        session = InboundSession()
        session.state = SessionState.ESTABLISHED
        session.created_time = now()
        session.last_activity = now()
        session.remote_ephemeral_key = alice_ephemeral
        session.remote_static_key = alice_static_key
        session.bound = (alice_static_key is not None)
        session.ns_chainkey = chainKey
        session.ns_hash = h
        
        # Extract destination if bound
        if session.bound:
            session.destination = extract_destination_from_payload(payload)
        
        # Process payload
        session.process_payload_blocks(payload)
        
        return session
    
    def send_nsr_reply(self, reply_payload):
        """Send NSR message"""
        # Generate NSR tagset
        tagsetKey = HKDF(self.ns_chainkey, ZEROLEN, "SessionReplyTags", 32)
        nsr_tagset = DH_INITIALIZE(self.ns_chainkey, tagsetKey)
        
        # Get tag
        tag, _ = nsr_tagset.get_next_tag()
        
        # Mix tag into hash
        h = SHA256(self.ns_hash || tag)
        
        # Generate ephemeral key
        self.ephemeral_keypair = generate_elg2_keypair()
        bob_ephemeral = self.ephemeral_keypair.public_key
        elg2_bob_ephemeral = ENCODE_ELG2(bob_ephemeral)
        
        # Mix ephemeral key
        h = SHA256(h || bob_ephemeral)
        
        chainKey = self.ns_chainkey
        
        # ee DH
        ee_shared = DH(self.ephemeral_keypair.private_key, 
                      self.remote_ephemeral_key)
        keydata = HKDF(chainKey, ee_shared, "", 32)
        chainKey = keydata[0:31]
        
        # se DH
        se_shared = DH(context.static_keypair.private_key, 
                      self.remote_ephemeral_key)
        keydata = HKDF(chainKey, se_shared, "", 64)
        chainKey = keydata[0:31]
        k_key_section = keydata[32:63]
        
        # Encrypt key section (empty)
        key_section_ciphertext = ENCRYPT(k_key_section, 0, ZEROLEN, h)
        h = SHA256(h || key_section_ciphertext)
        
        # Split for bidirectional ES
        keydata = HKDF(chainKey, ZEROLEN, "", 64)
        k_ab = keydata[0:31]  # Alice → Bob
        k_ba = keydata[32:63]  # Bob → Alice
        
        # Initialize ES tagsets
        self.inbound_tagset = DH_INITIALIZE(chainKey, k_ab)
        self.outbound_tagset = DH_INITIALIZE(chainKey, k_ba)
        
        # Build reply payload
        payload_data = build_payload_blocks(reply_payload)
        
        # Encrypt payload
        k_nsr = HKDF(k_ba, ZEROLEN, "AttachPayloadKDF", 32)
        payload_ciphertext = ENCRYPT(k_nsr, 0, payload_data, h)
        
        # Assemble NSR
        nsr_message = tag + elg2_bob_ephemeral + key_section_ciphertext + payload_ciphertext
        
        # Send
        send_to_network(self.destination, nsr_message)
        
        # Wait for ES
        self.state = SessionState.AWAITING_ES
        self.last_activity = now()
    
    def on_es_received(self, es_message):
        """Process first ES message"""
        if self.state == SessionState.AWAITING_ES:
            # First ES received, confirms session
            self.state = SessionState.ESTABLISHED
        
        # Process ES message
        self.process_es_message(es_message)
    
    def process_es_message(self, es_message):
        """Decrypt and process ES message"""
        # Extract tag
        tag = es_message[0:8]
        ciphertext = es_message[8:]
        
        # Look up tag
        index = self.inbound_tagset.lookup_tag(tag)
        if index is None:
            raise ValueError("Tag not found")
        
        # Get key
        key = self.inbound_keyratchet.get_key(index)
        
        # Construct nonce
        nonce = construct_nonce(index)
        
        # Decrypt
        try:
            payload = DECRYPT(key, nonce, ciphertext, tag)
        except AuthenticationError:
            raise ValueError("ES MAC verification failed")
        
        # Process blocks
        self.process_payload_blocks(payload)
        
        # Update activity
        self.last_activity = now()
```
### Phân loại thông điệp

**Phân biệt các loại thông điệp:**

```python
def classify_message(message):
    """Determine message type"""
    
    # Minimum lengths
    if len(message) < 24:
        return None  # Too short
    
    # Check for session tag (8 bytes)
    tag = message[0:8]
    
    # Try ES decryption first (most common)
    session = lookup_session_by_tag(tag)
    if session:
        return ('ES', session)
    
    # Try NSR decryption (tag + Elligator2 key)
    if len(message) >= 72:
        # Check if bytes 8-40 are valid Elligator2
        try:
            nsr_ephemeral = DECODE_ELG2(message[8:40])
            nsr_session = find_pending_nsr_by_tag(tag)
            if nsr_session:
                return ('NSR', nsr_session)
        except:
            pass
    
    # Try NS decryption (starts with Elligator2 key)
    if len(message) >= 96:
        try:
            ns_ephemeral = DECODE_ELG2(message[0:32])
            ns_session = InboundSession.try_decrypt_ns(message)
            if ns_session:
                return ('NS', ns_session)
        except:
            pass
    
    # Check ElGamal/AES (for dual-key compatibility)
    if len(message) >= 514:
        if (len(message) - 2) % 16 == 0:
            # Might be ElGamal NS
            return ('ELGAMAL_NS', None)
        elif len(message) % 16 == 0:
            # Might be ElGamal ES
            return ('ELGAMAL_ES', None)
    
    return None  # Unknown message type
```
### Thông lệ tốt nhất về quản lý phiên

**Bộ nhớ phiên:**

```python
class SessionKeyManager:
    def __init__(self):
        # Outbound sessions (one per destination)
        self.outbound_sessions = {}  # destination -> OutboundSession
        
        # Inbound sessions (multiple per destination during transition)
        self.inbound_sessions = []  # [InboundSession]
        
        # Session tag lookup (fast path for ES messages)
        self.tag_to_session = {}  # tag -> InboundSession
        
        # Limits
        self.max_inbound_sessions = 1000
        self.max_tags_per_session = 160
    
    def get_outbound_session(self, destination):
        """Get or create outbound session"""
        if destination not in self.outbound_sessions:
            session = OutboundSession(destination)
            self.outbound_sessions[destination] = session
        return self.outbound_sessions[destination]
    
    def add_inbound_session(self, session):
        """Add new inbound session"""
        # Check limits
        if len(self.inbound_sessions) >= self.max_inbound_sessions:
            self.expire_oldest_session()
        
        self.inbound_sessions.append(session)
        
        # Add tags to lookup table
        self.register_session_tags(session)
    
    def register_session_tags(self, session):
        """Register session's tags in lookup table"""
        for tag in session.inbound_tagset.get_all_tags():
            self.tag_to_session[tag] = session
    
    def lookup_tag(self, tag):
        """Fast tag lookup"""
        return self.tag_to_session.get(tag)
    
    def expire_sessions(self):
        """Periodic session expiration"""
        now_time = now()
        
        # Expire outbound sessions
        for dest, session in list(self.outbound_sessions.items()):
            if session.idle_time(now_time) > 8 * 60:
                del self.outbound_sessions[dest]
        
        # Expire inbound sessions
        expired = []
        for session in self.inbound_sessions:
            if session.idle_time(now_time) > 10 * 60:
                expired.append(session)
        
        for session in expired:
            self.remove_inbound_session(session)
    
    def remove_inbound_session(self, session):
        """Remove inbound session and clean up tags"""
        self.inbound_sessions.remove(session)
        
        # Remove tags from lookup
        for tag in session.inbound_tagset.get_all_tags():
            if tag in self.tag_to_session:
                del self.tag_to_session[tag]
```
**Quản lý bộ nhớ:**

```python
class TagMemoryManager:
    def __init__(self, max_memory_kb=10240):  # 10 MB default
        self.max_memory = max_memory_kb * 1024
        self.current_memory = 0
        self.max_tags_per_session = 160
        self.min_tags_per_session = 32
    
    def calculate_tag_memory(self, session):
        """Calculate memory used by session tags"""
        tag_count = len(session.inbound_tagset.tags)
        # Each tag: 8 bytes (tag) + 2 bytes (index) + 32 bytes (key, optional)
        # + overhead
        bytes_per_tag = 16 if session.defer_keys else 48
        return tag_count * bytes_per_tag
    
    def check_pressure(self):
        """Check if under memory pressure"""
        return self.current_memory > (self.max_memory * 0.9)
    
    def handle_pressure(self):
        """Reduce memory usage when under pressure"""
        if not self.check_pressure():
            return
        
        # Strategy 1: Reduce look-ahead windows
        for session in all_sessions:
            if session.look_ahead > self.min_tags_per_session:
                session.reduce_look_ahead(self.min_tags_per_session)
        
        # Strategy 2: Trim old tags aggressively
        for session in all_sessions:
            session.inbound_tagset.trim_behind(aggressive=True)
        
        # Strategy 3: Refuse new ratchets
        for session in all_sessions:
            if session.outbound_tagset.should_ratchet():
                session.defer_ratchet = True
        
        # Strategy 4: Expire idle sessions early
        expire_idle_sessions(threshold=5*60)  # 5 min instead of 10
```
### Chiến lược kiểm thử

**Kiểm thử đơn vị:**

```python
def test_x25519_dh():
    """Test X25519 key exchange"""
    alice_sk = GENERATE_PRIVATE()
    alice_pk = DERIVE_PUBLIC(alice_sk)
    
    bob_sk = GENERATE_PRIVATE()
    bob_pk = DERIVE_PUBLIC(bob_sk)
    
    # Both sides compute same shared secret
    alice_shared = DH(alice_sk, bob_pk)
    bob_shared = DH(bob_sk, alice_pk)
    
    assert alice_shared == bob_shared

def test_elligator2_encode_decode():
    """Test Elligator2 roundtrip"""
    sk = GENERATE_PRIVATE_ELG2()
    pk = DERIVE_PUBLIC(sk)
    
    encoded = ENCODE_ELG2(pk)
    decoded = DECODE_ELG2(encoded)
    
    assert decoded == pk

def test_chacha_poly_encrypt_decrypt():
    """Test ChaCha20-Poly1305 AEAD"""
    key = CSRNG(32)
    nonce = construct_nonce(42)
    plaintext = b"Hello, I2P!"
    ad = b"associated_data"
    
    ciphertext = ENCRYPT(key, nonce, plaintext, ad)
    decrypted = DECRYPT(key, nonce, ciphertext, ad)
    
    assert decrypted == plaintext

def test_session_tag_ratchet():
    """Test session tag generation"""
    sessTag_ck = CSRNG(32)
    tagset = SessionTagRatchet(sessTag_ck)
    
    # Generate 100 tags
    tags = [tagset.get_next_tag() for _ in range(100)]
    
    # All tags should be unique
    assert len(set(tags)) == 100
    
    # Each tag should be 8 bytes
    for tag in tags:
        assert len(tag) == 8
```
**Kiểm thử tích hợp:**

```python
def test_ns_nsr_handshake():
    """Test NS/NSR handshake"""
    # Alice creates outbound session
    alice_session = OutboundSession(bob_destination, bound=True)
    
    # Alice sends NS
    ns_message = alice_session.build_ns_message(b"Hello Bob")
    
    # Bob receives NS
    bob_session = InboundSession.try_decrypt_ns(ns_message)
    assert bob_session is not None
    assert bob_session.bound == True
    
    # Bob sends NSR
    nsr_message = bob_session.build_nsr_message(b"Hello Alice")
    
    # Alice receives NSR
    alice_session.on_nsr_received(nsr_message)
    assert alice_session.state == SessionState.ESTABLISHED
    
    # Both should have matching ES tagsets
    # (Cannot directly compare, but can test by sending ES messages)

def test_es_bidirectional():
    """Test ES messages in both directions"""
    # (After NS/NSR handshake)
    
    # Alice sends ES to Bob
    es_alice_to_bob = alice_session.send_es_message(b"Data from Alice")
    
    # Bob receives ES
    bob_session.process_es_message(es_alice_to_bob)
    
    # Bob sends ES to Alice
    es_bob_to_alice = bob_session.send_es_message(b"Data from Bob")
    
    # Alice receives ES
    alice_session.process_es_message(es_bob_to_alice)

def test_dh_ratchet():
    """Test DH ratchet"""
    # (After established session)
    
    # Alice initiates ratchet
    alice_session.initiate_ratchet()
    nextkey_alice = build_nextkey_block(
        flags=0x01,
        key_id=0,
        public_key=alice_new_key
    )
    
    # Send to Bob
    bob_session.process_nextkey_block(nextkey_alice)
    
    # Bob replies
    nextkey_bob = build_nextkey_block(
        flags=0x03,
        key_id=0,
        public_key=bob_new_key
    )
    
    # Send to Alice
    alice_session.process_nextkey_block(nextkey_bob)
    
    # Both should now be using new tagsets
    assert alice_session.outbound_tagset.id == 1
    assert bob_session.inbound_tagset.id == 1
```
**Các véc-tơ kiểm thử:**

Hiện thực các vector kiểm thử từ đặc tả:

1. **Noise IK Handshake** (bắt tay Noise IK): Sử dụng các vector kiểm thử chuẩn của Noise
2. **HKDF** (hàm dẫn xuất khóa dựa trên HMAC): Sử dụng các vector kiểm thử theo RFC 5869
3. **ChaCha20-Poly1305** (mã hóa xác thực AEAD): Sử dụng các vector kiểm thử theo RFC 7539
4. **Elligator2** (kỹ thuật ánh xạ Elligator2): Sử dụng các vector kiểm thử từ bài báo về Elligator2 hoặc OBFS4 (transport che giấu OBFS4)

**Kiểm thử khả năng tương tác:**

1. **Java I2P**: Kiểm thử đối chiếu với bản triển khai tham chiếu của Java I2P
2. **i2pd**: Kiểm thử đối chiếu với bản triển khai i2pd bằng C++
3. **Ghi bắt gói tin**: Sử dụng Wireshark dissector (trình phân tích giao thức) (nếu có) để xác minh định dạng thông điệp
4. **Tương tác giữa các triển khai**: Tạo khung kiểm thử có thể gửi/nhận giữa các bản triển khai

### Những cân nhắc về hiệu năng

**Sinh khóa:**

Việc sinh khóa Elligator2 (kỹ thuật che giấu khóa công khai) tốn kém (tỷ lệ loại bỏ 50%):

```python
class KeyPool:
    """Pre-generate keys in background thread"""
    def __init__(self, pool_size=10):
        self.pool = Queue(maxsize=pool_size)
        self.generator_thread = Thread(target=self.generate_keys, daemon=True)
        self.generator_thread.start()
    
    def generate_keys(self):
        while True:
            if not self.pool.full():
                keypair = generate_elg2_keypair()
                # Also compute encoded form
                encoded = ENCODE_ELG2(keypair.public_key)
                self.pool.put((keypair, encoded))
            else:
                sleep(0.1)
    
    def get_keypair(self):
        try:
            return self.pool.get(timeout=1.0)
        except Empty:
            # Pool exhausted, generate inline
            return generate_elg2_keypair()
```
**Tra cứu thẻ:**

Sử dụng bảng băm để tra cứu thẻ với độ phức tạp O(1):

```python
class FastTagLookup:
    def __init__(self):
        self.tag_to_session = {}  # Python dict is hash table
    
    def add_tag(self, tag, session, index):
        # 8-byte tag as bytes is hashable
        self.tag_to_session[tag] = (session, index)
    
    def lookup_tag(self, tag):
        return self.tag_to_session.get(tag)
```
**Tối ưu hóa bộ nhớ:**

Trì hoãn việc tạo khóa đối xứng:

```python
class DeferredKeyRatchet:
    """Only generate keys when needed"""
    def __init__(self, symmKey_ck):
        self.chainKey = symmKey_ck
        self.index = -1
        self.cache = LRUCache(maxsize=32)  # Cache recent keys
    
    def get_key(self, index):
        # Check cache first
        if index in self.cache:
            return self.cache[index]
        
        # Generate keys up to index
        while self.index < index:
            self.index += 1
            keydata = HKDF(self.chainKey, ZEROLEN, "SymmetricRatchet", 64)
            self.chainKey = keydata[0:31]
            
            if self.index == index:
                key = keydata[32:63]
                self.cache[index] = key
                return key
```
**Xử lý theo lô:**

Xử lý nhiều thông điệp theo lô:

```python
def process_message_batch(messages):
    """Process multiple messages efficiently"""
    results = []
    
    # Group by type
    ns_messages = []
    nsr_messages = []
    es_messages = []
    
    for msg in messages:
        msg_type = classify_message(msg)
        if msg_type[0] == 'NS':
            ns_messages.append(msg)
        elif msg_type[0] == 'NSR':
            nsr_messages.append(msg)
        elif msg_type[0] == 'ES':
            es_messages.append(msg)
    
    # Process in batches
    # ES messages are most common, process first
    for msg in es_messages:
        results.append(process_es_message(msg))
    
    for msg in nsr_messages:
        results.append(process_nsr_message(msg))
    
    for msg in ns_messages:
        results.append(process_ns_message(msg))
    
    return results
```
---

## Các cân nhắc bảo mật

### Mô hình đe dọa

**Khả năng của đối thủ tấn công:**

1. **Người quan sát thụ động**: Có thể quan sát toàn bộ lưu lượng mạng
2. **Kẻ tấn công chủ động**: Có thể chèn, sửa đổi, loại bỏ, phát lại thông điệp
3. **Nút bị xâm nhập**: Có thể xâm nhập một router hoặc điểm đích
4. **Phân tích lưu lượng**: Có thể thực hiện phân tích thống kê về các mẫu lưu lượng

**Mục tiêu bảo mật:**

1. **Tính bảo mật**: Nội dung thông điệp được ẩn khỏi người quan sát
2. **Xác thực**: Danh tính người gửi được xác minh (trong các phiên ràng buộc)
3. **Tính bí mật chuyển tiếp**: Các thông điệp trước đây vẫn giữ bí mật ngay cả khi khóa bị lộ
4. **Chống phát lại**: Không thể phát lại các thông điệp cũ
5. **Ngụy trang lưu lượng**: Quá trình bắt tay không thể phân biệt với dữ liệu ngẫu nhiên

### Các giả định mật mã

**Các giả định về độ khó:**

1. **X25519 CDH**: Bài toán Diffie–Hellman dạng tính toán là khó trên Curve25519
2. **ChaCha20 PRF**: ChaCha20 là một hàm giả ngẫu nhiên
3. **Poly1305 MAC**: Poly1305 không thể bị giả mạo dưới tấn công chọn thông điệp
4. **SHA-256 CR**: SHA-256 kháng va chạm
5. **HKDF Security**: HKDF trích xuất và mở rộng các khóa được phân bố đồng đều

**Mức độ bảo mật:**

- **X25519**: ~128-bit mức an toàn (bậc đường cong 2^252)
- **ChaCha20**: khóa 256-bit, mức an toàn 256-bit
- **Poly1305**: mức an toàn 128-bit (xác suất va chạm)
- **SHA-256**: khả năng chống va chạm 128-bit, khả năng chống tiền ảnh 256-bit

### Quản lý khóa

**Sinh khóa:**

```python
# CRITICAL: Use cryptographically secure RNG
def CSRNG(length):
    # GOOD: os.urandom, secrets.token_bytes (Python)
    # GOOD: /dev/urandom (Linux)
    # GOOD: BCryptGenRandom (Windows)
    # BAD: random.random(), Math.random() (NOT cryptographically secure)
    return os.urandom(length)

# CRITICAL: Validate keys
def validate_x25519_key(pubkey):
    # Check for weak keys (all zeros, small order points)
    if pubkey == bytes(32):
        raise WeakKeyError("All-zero public key")
    
    # Perform DH to check for weak shared secrets
    test_shared = DH(test_private_key, pubkey)
    if test_shared == bytes(32):
        raise WeakKeyError("Results in zero shared secret")
```
**Lưu trữ khóa:**

```python
# CRITICAL: Protect private keys
class SecureKeyStorage:
    def __init__(self):
        # Store in memory with protection
        self.keys = {}
        
        # Option 1: Memory locking (prevent swapping to disk)
        # mlock(self.keys)
        
        # Option 2: Encrypted storage
        # self.encryption_key = derive_from_password()
    
    def store_key(self, key_id, private_key):
        # Option: Encrypt before storage
        # encrypted = encrypt(private_key, self.encryption_key)
        # self.keys[key_id] = encrypted
        self.keys[key_id] = private_key
    
    def delete_key(self, key_id):
        # Securely wipe memory
        if key_id in self.keys:
            key = self.keys[key_id]
            # Overwrite with zeros before deletion
            for i in range(len(key)):
                key[i] = 0
            del self.keys[key_id]
```
**Luân chuyển khóa:**

```python
# CRITICAL: Rotate keys regularly
class KeyRotationPolicy:
    def __init__(self):
        self.max_messages_per_tagset = 4096  # Ratchet before 65535
        self.max_tagset_age = 10 * 60       # 10 minutes
        self.max_session_age = 60 * 60      # 1 hour
    
    def should_ratchet(self, tagset):
        return (tagset.messages_sent >= self.max_messages_per_tagset or
                tagset.age() >= self.max_tagset_age)
    
    def should_replace_session(self, session):
        return session.age() >= self.max_session_age
```
### Các biện pháp giảm thiểu tấn công

### Các biện pháp giảm thiểu tấn công phát lại

**Xác thực DateTime (ngày giờ):**

```python
MAX_CLOCK_SKEW_PAST = 5 * 60
MAX_CLOCK_SKEW_FUTURE = 2 * 60

def validate_datetime(timestamp):
    now = int(time.time())
    age = now - timestamp
    
    if age < -MAX_CLOCK_SKEW_FUTURE:
        raise ReplayError("Timestamp too far in future")
    
    if age > MAX_CLOCK_SKEW_PAST:
        raise ReplayError("Timestamp too old")
    
    return True
```
**Bộ lọc Bloom cho các thông điệp NS:**

```python
class ReplayFilter:
    def __init__(self, capacity=100000, error_rate=0.001, duration=5*60):
        self.bloom = BloomFilter(capacity=capacity, error_rate=error_rate)
        self.duration = duration
        self.entries = []  # (timestamp, ephemeral_key)
    
    def check_replay(self, ephemeral_key, timestamp):
        # Validate timestamp
        if not validate_datetime(timestamp):
            return False
        
        # Check Bloom filter
        if ephemeral_key in self.bloom:
            # Potential replay (or false positive)
            # Check exact match in entries
            for ts, key in self.entries:
                if key == ephemeral_key:
                    return False  # Definite replay
        
        # Add to filter
        self.bloom.add(ephemeral_key)
        self.entries.append((timestamp, ephemeral_key))
        
        # Expire old entries
        self.expire_old_entries()
        
        return True
    
    def expire_old_entries(self):
        now = int(time.time())
        self.entries = [(ts, key) for ts, key in self.entries
                       if now - ts < self.duration]
```
**Session Tag (thẻ phiên) dùng một lần:**

```python
def process_session_tag(tag):
    # Look up tag
    entry = tagset.lookup_tag(tag)
    if entry is None:
        raise ValueError("Invalid session tag")
    
    # CRITICAL: Remove tag immediately (one-time use)
    tagset.remove_tag(tag)
    
    # Use associated key
    return entry.key, entry.index
```
### Các biện pháp giảm thiểu mạo danh do lộ khóa (Key Compromise Impersonation, KCI)

**Vấn đề**: Việc xác thực thông điệp của NS dễ bị tấn công KCI (Key Compromise Impersonation - giả mạo do lộ khóa) (Mức xác thực 1)

**Biện pháp giảm thiểu**:

1. Chuyển sang NSR (Cấp xác thực 2) càng nhanh càng tốt
2. Đừng tin cậy NS payload cho các thao tác trọng yếu về bảo mật
3. Chờ xác nhận NSR trước khi thực hiện các hành động không thể hoàn tác

```python
def process_ns_message(ns_message):
    # NS authenticated at Level 1 (KCI vulnerable)
    # Do NOT perform security-critical operations yet
    
    # Extract sender's static key
    sender_key = ns_message.static_key
    
    # Mark session as pending Level 2 authentication
    session.auth_level = 1
    session.sender_key = sender_key
    
    # Send NSR
    send_nsr_reply(session)

def process_first_es_message(es_message):
    # Now we have Level 2 authentication (KCI resistant)
    session.auth_level = 2
    
    # Safe to perform security-critical operations
    process_security_critical_operation(es_message)
```
### Các biện pháp giảm thiểu tấn công từ chối dịch vụ

**Bảo vệ chống flood cho NS:**

```python
class NSFloodProtection:
    def __init__(self):
        self.ns_count = defaultdict(int)  # source -> count
        self.ns_timestamps = defaultdict(list)  # source -> [timestamps]
        
        self.max_ns_per_source = 5
        self.rate_window = 10  # seconds
        self.max_concurrent_ns = 100
    
    def check_ns_allowed(self, source):
        # Global limit
        total_pending = sum(self.ns_count.values())
        if total_pending >= self.max_concurrent_ns:
            return False
        
        # Per-source rate limit
        now = time.time()
        timestamps = self.ns_timestamps[source]
        
        # Remove old timestamps
        timestamps = [ts for ts in timestamps if now - ts < self.rate_window]
        self.ns_timestamps[source] = timestamps
        
        # Check rate
        if len(timestamps) >= self.max_ns_per_source:
            return False
        
        # Allow NS
        timestamps.append(now)
        self.ns_count[source] += 1
        return True
    
    def on_session_established(self, source):
        # Decrease pending count
        if self.ns_count[source] > 0:
            self.ns_count[source] -= 1
```
**Giới hạn lưu trữ thẻ:**

```python
class TagStorageLimit:
    def __init__(self, max_tags=1000000):
        self.max_tags = max_tags
        self.current_tags = 0
    
    def can_create_session(self, look_ahead):
        if self.current_tags + look_ahead > self.max_tags:
            return False
        return True
    
    def add_tags(self, count):
        self.current_tags += count
    
    def remove_tags(self, count):
        self.current_tags -= count
```
**Quản lý tài nguyên thích ứng:**

```python
class AdaptiveResourceManager:
    def __init__(self):
        self.load_level = 0  # 0 = low, 1 = medium, 2 = high, 3 = critical
    
    def adjust_parameters(self):
        if self.load_level == 0:
            # Normal operation
            return {
                'max_look_ahead': 160,
                'max_sessions': 1000,
                'session_timeout': 10 * 60
            }
        
        elif self.load_level == 1:
            # Moderate load
            return {
                'max_look_ahead': 80,
                'max_sessions': 800,
                'session_timeout': 8 * 60
            }
        
        elif self.load_level == 2:
            # High load
            return {
                'max_look_ahead': 32,
                'max_sessions': 500,
                'session_timeout': 5 * 60
            }
        
        else:  # load_level == 3
            # Critical load
            return {
                'max_look_ahead': 16,
                'max_sessions': 200,
                'session_timeout': 3 * 60
            }
```
### Khả năng chống phân tích lưu lượng

**Mã hóa Elligator2 (kỹ thuật biểu diễn điểm trên đường cong elliptic thành chuỗi trông ngẫu nhiên):**

Đảm bảo các thông điệp bắt tay không thể phân biệt được so với dữ liệu ngẫu nhiên:

```python
# NS and NSR start with Elligator2-encoded ephemeral keys
# Observer cannot distinguish from random 32-byte string
```
**Chiến lược đệm:**

```python
# Resist message size fingerprinting
def add_padding(payload, strategy='random'):
    if strategy == 'random':
        # Random padding 0-15 bytes
        size = random.randint(0, 15)
    
    elif strategy == 'round':
        # Round to next 64-byte boundary
        target = ((len(payload) + 63) // 64) * 64
        size = target - len(payload) - 3  # -3 for block header
    
    elif strategy == 'fixed':
        # Always 1KB messages
        size = 1024 - len(payload) - 3
    
    return build_padding_block(size)
```
**Tấn công thời gian:**

```python
# CRITICAL: Use constant-time operations
def constant_time_compare(a, b):
    """Constant-time byte string comparison"""
    if len(a) != len(b):
        return False
    
    result = 0
    for x, y in zip(a, b):
        result |= x ^ y
    
    return result == 0

# CRITICAL: Constant-time MAC verification
def verify_mac(computed_mac, received_mac):
    if not constant_time_compare(computed_mac, received_mac):
        # Always take same time regardless of where comparison fails
        raise AuthenticationError("MAC verification failed")
```
### Những cạm bẫy khi hiện thực

**Các lỗi thường gặp:**

1. **Tái sử dụng nonce (số dùng một lần)**: KHÔNG BAO GIỜ tái sử dụng các cặp (key, nonce)
   ```python
   # BAD: Reusing nonce with same key
   ciphertext1 = ENCRYPT(key, nonce, plaintext1, ad1)
   ciphertext2 = ENCRYPT(key, nonce, plaintext2, ad2)  # CATASTROPHIC

# TỐT: Nonce (giá trị dùng một lần) duy nhất cho mỗi thông điệp    ciphertext1 = ENCRYPT(key, nonce1, plaintext1, ad1)    ciphertext2 = ENCRYPT(key, nonce2, plaintext2, ad2)

   ```

2. **Ephemeral Key Reuse**: Generate fresh ephemeral key for each NS/NSR
   ```python
# KHÔNG NÊN: Tái sử dụng khóa tạm thời    ephemeral_key = generate_elg2_keypair()    send_ns_message(ephemeral_key)    send_ns_message(ephemeral_key)  # KHÔNG NÊN

# TỐT: Khóa mới cho mỗi thông điệp    send_ns_message(generate_elg2_keypair())    send_ns_message(generate_elg2_keypair())

   ```

3. **Weak RNG**: Use cryptographically secure random number generator
   ```python
# KHÔNG NÊN: Bộ sinh số ngẫu nhiên không dùng cho mật mã    import random    key = bytes([random.randint(0, 255) for _ in range(32)])  # KHÔNG AN TOÀN

# TỐT: Bộ sinh số ngẫu nhiên an toàn mật mã    import os    key = os.urandom(32)

   ```

4. **Timing Attacks**: Use constant-time comparisons
   ```python
# KHÔNG NÊN: So sánh thoát sớm    if computed_mac == received_mac:  # Rò rỉ thời gian

       pass
   
# TỐT: So sánh thời gian không đổi    if constant_time_compare(computed_mac, received_mac):

       pass
   ```

5. **Incomplete MAC Verification**: Always verify before using data
   ```python
# SAI: Giải mã trước khi xác minh    plaintext = chacha20_decrypt(key, nonce, ciphertext)    mac_ok = verify_mac(mac, plaintext)  # QUÁ MUỘN    if not mac_ok:

       return error
   
# TỐT: AEAD (mã hóa xác thực kèm dữ liệu) kiểm tra tính xác thực trước khi giải mã    try:

       plaintext = DECRYPT(key, nonce, ciphertext, ad)  # Verifies MAC first
except AuthenticationError:

       return error
   ```

6. **Key Deletion**: Securely wipe keys from memory
   ```python
# KHÔNG NÊN: Xóa đơn giản    del private_key  # Vẫn còn trong bộ nhớ

# TỐT: Ghi đè trước khi xóa    for i in range(len(private_key)):

       private_key[i] = 0
del private_key

   ```

### Security Audits

**Recommended Audits:**

1. **Cryptographic Review**: Expert review of KDF chains and DH operations
2. **Implementation Audit**: Code review for timing attacks, key management, RNG usage
3. **Protocol Analysis**: Formal verification of handshake security properties
4. **Side-Channel Analysis**: Timing, power, and cache attacks
5. **Fuzzing**: Random input testing for parser robustness

**Test Cases:**

```python
# Các trường hợp kiểm thử trọng yếu về bảo mật

def test_nonce_uniqueness():

    """Ensure nonces are never reused"""
    nonces = set()
    for i in range(10000):
        nonce = construct_nonce(i)
        assert nonce not in nonces
        nonces.add(nonce)

def test_key_isolation():

    """Ensure sessions don't share keys"""
    session1 = create_session(destination1)
    session2 = create_session(destination2)
    
    assert session1.key != session2.key

def test_replay_prevention():

    """Ensure replay attacks are detected"""
    ns_message = create_ns_message()
    
    # First delivery succeeds
    assert process_ns_message(ns_message) == True
    
    # Replay fails
    assert process_ns_message(ns_message) == False

def test_mac_verification():

    """Ensure MAC verification is enforced"""
    key = CSRNG(32)
    nonce = construct_nonce(0)
    plaintext = b"test"
    ad = b"test_ad"
    
    ciphertext = ENCRYPT(key, nonce, plaintext, ad)
    
    # Correct MAC verifies
    assert DECRYPT(key, nonce, ciphertext, ad) == plaintext
    
    # Corrupted MAC fails
    corrupted = ciphertext[:-1] + bytes([ciphertext[-1] ^ 0xFF])
    with pytest.raises(AuthenticationError):
        DECRYPT(key, nonce, corrupted, ad)
```

---

## Configuration and Deployment

### I2CP Configuration

**Enable ECIES Encryption:**

```properties
# Chỉ ECIES (lược đồ mã hóa tích hợp đường cong elliptic) (được khuyến nghị cho các triển khai mới)

i2cp.leaseSetEncType=4

# Khóa kép (ECIES + ElGamal để tương thích)

i2cp.leaseSetEncType=4,0

# Chỉ ElGamal (lỗi thời, không khuyến nghị)

i2cp.leaseSetEncType=0

```

**LeaseSet Type:**

```properties
# LS2 tiêu chuẩn (phổ biến nhất)

i2cp.leaseSetType=3

# LS2 được mã hóa (blinded destinations - điểm đến bị làm mù)

i2cp.leaseSetType=5

# Meta LS2 (nhiều đích đến)

i2cp.leaseSetType=7

```

**Additional Options:**

```properties
# Khóa tĩnh cho ECIES (tùy chọn, được tạo tự động nếu không được chỉ định)

# Khóa công khai X25519 dài 32 byte, được mã hóa Base64

i2cp.leaseSetPrivateKey=<base64-encoded-key>

# Loại chữ ký (cho LeaseSet)

i2cp.leaseSetSigningPrivateKey=<base64-encoded-key> i2cp.leaseSetSigningType=7  # Ed25519

```

### Java I2P Configuration

**router.config:**

```properties
# ECIES (lược đồ mã hóa tích hợp dựa trên đường cong elliptic) giữa các router

i2p.router.useECIES=true

```

**Build Properties:**

```java
// For I2CP clients (Java) Properties props = new Properties(); props.setProperty("i2cp.leaseSetEncType", "4"); props.setProperty("i2cp.leaseSetType", "3");

I2PSession session = i2pClient.createSession(props);

```

### i2pd Configuration

**i2pd.conf:**

```ini
[giới hạn]

# Giới hạn bộ nhớ cho các phiên ECIES (lược đồ mã hóa tích hợp đường cong elliptic)

ecies.memory = 128M

[ecies (lược đồ mã hóa tích hợp đường cong elliptic)]

# Bật ECIES (lược đồ mã hóa tích hợp trên đường cong elliptic)

enabled = true

# Chỉ ECIES (sơ đồ mã hóa tích hợp dùng đường cong elliptic) hoặc khóa kép

compatibility = true  # true = hai khóa, false = chỉ ECIES

```

**Tunnels Configuration:**

```ini
[my-service] type = http host = 127.0.0.1 port = 8080 keys = my-service-keys.dat

# Chỉ ECIES (sơ đồ mã hóa tích hợp đường cong elliptic)

ecies = true

```

### Compatibility Matrix

**Router Version Support:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">ECIES Support</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">LS2 Support</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Dual-Key</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">&lt; 0.9.38</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">❌ No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">❌ No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">N/A</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Legacy only</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.38-0.9.45</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">❌ No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">✅ Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">N/A</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">LS2 only</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.46-0.9.50</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">✅ Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">✅ Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">✅ Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Initial ECIES</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1.5.0+</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">✅ Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">✅ Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">✅ Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.0.0+</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">✅ Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">✅ Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">✅ Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
  </tbody>
</table>

**Destination Compatibility:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Destination Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Can Connect To</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES-only</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES-only, Dual-key</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Requires 0.9.46+ routers</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Dual-key</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Any</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Maximum compatibility</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ElGamal-only</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ElGamal-only, Dual-key</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Legacy</td>
    </tr>
  </tbody>
</table>

**FloodFill Requirements:**

- **ECIES-only destinations**: Require majority of floodfills on 0.9.46+ for encrypted lookups
- **Dual-key destinations**: Work with any floodfill version
- **Current status**: Near 100% floodfill adoption as of 2025

### Migration Guide

**Migrating from ElGamal to ECIES:**

**Step 1: Enable Dual-Key Mode**

```properties
# Thêm ECIES (lược đồ mã hóa tích hợp trên đường cong elliptic) trong khi vẫn giữ ElGamal (lược đồ mã hóa ElGamal)

i2cp.leaseSetEncType=4,0

```

**Step 2: Monitor Connections**

```bash
# Kiểm tra các loại kết nối

i2prouter.exe status

# hoặc

http://127.0.0.1:7657/peers

```

**Step 3: Switch to ECIES-Only (after testing)**

```properties
# Loại bỏ ElGamal

i2cp.leaseSetEncType=4

```

**Step 4: Restart Application**

```bash
# Khởi động lại router I2P hoặc ứng dụng

systemctl restart i2p

# hoặc

i2prouter.exe restart

```

**Rollback Plan:**

```properties
# Quay lại chỉ dùng ElGamal (thuật toán mật mã ElGamal) nếu có vấn đề

i2cp.leaseSetEncType=0

```

### Performance Tuning

**Session Limits:**

```properties
# Số phiên đến tối đa

i2p.router.maxInboundSessions=1000

# Số phiên gửi đi tối đa

i2p.router.maxOutboundSessions=1000

# Thời gian chờ phiên (giây)

i2p.router.sessionTimeout=600

```

**Memory Limits:**

```properties
# Giới hạn dung lượng lưu trữ thẻ (KB)

i2p.ecies.maxTagMemory=10240  # 10 MB

# Cửa sổ nhìn trước

i2p.ecies.tagLookAhead=160 i2p.ecies.tagLookAheadMin=32

```

**Ratchet Policy:**

```properties
# Thông điệp trước khi ratchet (cơ chế luân chuyển khóa tăng dần)

i2p.ecies.ratchetThreshold=4096

# Thời gian trước khi kích hoạt ratchet (cơ chế cập nhật khóa liên tục trong mật mã) (giây)

i2p.ecies.ratchetTimeout=600  # 10 phút

```

### Monitoring and Debugging

**Logging:**

```properties
# Bật ghi nhật ký gỡ lỗi ECIES (lược đồ mã hóa tích hợp đường cong elliptic)

logger.i2p.router.transport.ecies=DEBUG

```

**Metrics:**

Monitor these metrics:

1. **NS Success Rate**: Percentage of NS messages receiving NSR
2. **Session Establishment Time**: Time from NS to first ES
3. **Tag Storage Usage**: Current memory usage for tags
4. **Ratchet Frequency**: How often sessions ratchet
5. **Session Lifetime**: Average session duration

**Common Issues:**

1. **NS Timeout**: No NSR received
   - Check destination is online
   - Check floodfill availability
   - Verify LeaseSet published correctly

2. **High Memory Usage**: Too many tags stored
   - Reduce look-ahead window
   - Decrease session timeout
   - Implement aggressive expiration

3. **Frequent Ratchets**: Sessions ratcheting too often
   - Increase ratchet threshold
   - Check for retransmissions

4. **Session Failures**: ES messages failing to decrypt
   - Verify tag synchronization
   - Check for replay attacks
   - Validate nonce construction

---

## References

### Specifications

1. **ECIES Proposal**: [Proposal 144](/proposals/144-ecies-x25519-aead-ratchet/)
2. **I2NP**: [I2NP Specification](/docs/specs/i2np/)
3. **Common Structures**: [Common Structures Specification](/docs/specs/common-structures/)
4. **NTCP2**: [NTCP2 Specification](/docs/specs/ntcp2/)
5. **SSU2**: [SSU2 Specification](/docs/specs/ssu2/)
6. **I2CP**: [I2CP Specification](/docs/specs/i2cp/)
7. **ElGamal/AES+SessionTags**: [ElGamal/AES Specification](/docs/legacy/elgamal-aes/)

### Cryptographic Standards

1. **Noise Protocol Framework**: [Noise Specification](https://noiseprotocol.org/noise.html) (Revision 34, 2018-07-11)
2. **Signal Double Ratchet**: [Signal Specification](https://signal.org/docs/specifications/doubleratchet/)
3. **RFC 7748**: [Elliptic Curves for Security (X25519)](https://tools.ietf.org/html/rfc7748)
4. **RFC 7539**: [ChaCha20 and Poly1305 for IETF Protocols](https://tools.ietf.org/html/rfc7539)
5. **RFC 5869**: [HKDF (HMAC-based Key Derivation Function)](https://tools.ietf.org/html/rfc5869)
6. **RFC 2104**: [HMAC: Keyed-Hashing for Message Authentication](https://tools.ietf.org/html/rfc2104)
7. **Elligator2**: [Elligator Paper](https://elligator.cr.yp.to/elligator-20130828.pdf)

### Implementation Resources

1. **Java I2P**: [i2p.i2p Repository](https://github.com/i2p/i2p.i2p)
2. **i2pd (C++)**: [i2pd Repository](https://github.com/PurpleI2P/i2pd)
3. **OBFS4 (Elligator2)**: [obfs4proxy Repository](https://gitlab.com/yawning/obfs4)

### Additional Information

1. **I2P Website**: [/](/)
2. **I2P Forum**: [https://i2pforum.net](https://i2pforum.net)
3. **I2P Wiki**: [https://wiki.i2p-projekt.de](https://wiki.i2p-projekt.de)

---

## Appendix A: KDF Summary

**All KDF Operations in ECIES:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Operation</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Input</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Info String</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Output</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NS Initial ChainKey</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">protocol_name</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">(none - SHA256)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">h, chainKey</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NS Static Key Section</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey, es_shared</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">""</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey, k</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NS Payload Section (bound)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey, ss_shared</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">""</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey, k</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NSR Tagset</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">"SessionReplyTags"</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">tagsetKey</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NSR ee DH</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey, ee_shared</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">""</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NSR se DH</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey, se_shared</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">""</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey, k</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NSR Split</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">""</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">k_ab, k_ba</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NSR Payload</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">k_ba</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">"AttachPayloadKDF"</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">k_nsr</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DH Initialize</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">rootKey, k</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">"KDFDHRatchetStep"</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">nextRootKey, chainKey</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Tag and Key Chain Keys</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">"TagAndKeyGenKeys"</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">sessTag_ck, symmKey_ck</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Session Tag Init</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">sessTag_ck</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">"STInitialization"</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey, CONSTANT</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Session Tag Gen</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey, CONSTANT</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">"SessionTagKeyGen"</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey, tag</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Symmetric Key Gen</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">"SymmetricRatchet"</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey, key</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DH Ratchet</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">sharedSecret</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">"XDHRatchetTagSet"</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">tagsetKey</td>
    </tr>
  </tbody>
</table>

---

## Appendix B: Message Size Calculator

**Calculate message sizes for capacity planning:**

```python
def calculate_ns_size(payload_size, bound=True):

    """Calculate New Session message size"""
    ephemeral_key = 32
    static_section = 32 + 16  # encrypted + MAC
    payload_encrypted = payload_size + 16  # + MAC
    
    return ephemeral_key + static_section + payload_encrypted

def calculate_nsr_size(payload_size):

    """Calculate New Session Reply message size"""
    tag = 8
    ephemeral_key = 32
    key_section_mac = 16
    payload_encrypted = payload_size + 16  # + MAC
    
    return tag + ephemeral_key + key_section_mac + payload_encrypted

def calculate_es_size(payload_size):

    """Calculate Existing Session message size"""
    tag = 8
    payload_encrypted = payload_size + 16  # + MAC
    
    return tag + payload_encrypted

# Ví dụ

print("NS (bound, 1KB payload):", calculate_ns_size(1024, bound=True), "bytes")

# Đầu ra: 1120 byte

print("NSR (1KB payload):", calculate_nsr_size(1024), "bytes")

# Đầu ra: 1096 byte

print("ES (tải trọng 1KB):", calculate_es_size(1024), "byte")

# Đầu ra: 1048 byte

```

---

## Appendix C: Glossary

**AEAD**: Authenticated Encryption with Associated Data - encryption mode that provides both confidentiality and authenticity

**Authentication Level**: Noise protocol security property indicating strength of sender identity verification

**Binding**: Association of a session with a specific far-end destination

**ChaCha20**: Stream cipher designed by Daniel J. Bernstein

**ChainKey**: Cryptographic key used in HKDF chains to derive subsequent keys

**Confidentiality Level**: Noise protocol security property indicating strength of forward secrecy

**DH**: Diffie-Hellman key agreement protocol

**Elligator2**: Encoding technique to make elliptic curve points indistinguishable from random

**Ephemeral Key**: Short-lived key used only for a single handshake

**ES**: Existing Session message (used after handshake completion)

**Forward Secrecy**: Property ensuring past communications remain secure if keys are compromised

**Garlic Clove**: I2NP message container for end-to-end delivery

**HKDF**: HMAC-based Key Derivation Function

**IK Pattern**: Noise handshake pattern where initiator sends static key immediately

**KCI**: Key Compromise Impersonation attack

**KDF**: Key Derivation Function - cryptographic function for generating keys from other keys

**LeaseSet**: I2P structure containing a destination's public keys and tunnel information

**LS2**: LeaseSet version 2 with encryption type support

**MAC**: Message Authentication Code - cryptographic checksum proving authenticity

**MixHash**: Noise protocol function for maintaining running hash transcript

**NS**: New Session message (initiates new session)

**NSR**: New Session Reply message (response to NS)

**Nonce**: Number used once - ensures unique encryption even with same key

**Pairing**: Linking an inbound session with an outbound session for bidirectional communication

**Poly1305**: Message authentication code designed by Daniel J. Bernstein

**Ratchet**: Cryptographic mechanism for deriving sequential keys

**Session Tag**: 8-byte one-time identifier for existing session messages

**Static Key**: Long-term key associated with a destination's identity

**Tag Set**: Collection of session tags derived from a common root

**X25519**: Elliptic curve Diffie-Hellman key agreement using Curve25519

---