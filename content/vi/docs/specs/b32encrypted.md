---
title: "B32 cho các leaseSet mã hóa"
description: "Định dạng địa chỉ Base 32 cho leasesets LS2 được mã hóa"
slug: "b32encrypted"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
status: "Đã triển khai"
---

## Tổng quan

Các địa chỉ Base 32 tiêu chuẩn ("b32") chứa giá trị băm của đích (destination). Điều này sẽ không hoạt động đối với LS2 được mã hóa (proposal 123).

Chúng ta không thể dùng một địa chỉ base 32 truyền thống cho một LS2 được mã hóa (đề xuất 123), vì nó chỉ chứa băm của đích (Destination). Nó không cung cấp khóa công khai không mù hóa. Ứng dụng khách phải biết khóa công khai của đích, kiểu chữ ký, kiểu chữ ký mù hóa, và một bí mật tùy chọn hoặc khóa riêng để lấy và giải mã leaseSet. Do đó, chỉ một địa chỉ base 32 là không đủ. Ứng dụng khách cần hoặc đích đầy đủ (trong đó chứa khóa công khai), hoặc chỉ riêng khóa công khai. Nếu ứng dụng khách có đích đầy đủ trong sổ địa chỉ và sổ địa chỉ hỗ trợ tra cứu ngược theo băm, thì khóa công khai có thể được truy xuất.

Định dạng này đặt khóa công khai vào địa chỉ base32 thay cho giá trị băm. Định dạng này cũng phải chứa kiểu chữ ký của khóa công khai, và kiểu chữ ký của lược đồ làm mù.

Tài liệu này đặc tả một định dạng b32 cho các địa chỉ này. Mặc dù trong quá trình thảo luận, chúng tôi đã gọi định dạng mới này là địa chỉ "b33", nhưng trên thực tế, định dạng mới vẫn giữ hậu tố ".b32.i2p" như thường lệ.

## Tình trạng triển khai

Đề xuất 123 (Các mục netDB mới) đã được triển khai đầy đủ trong phiên bản 0.9.43 (Tháng 10 năm 2019). Bộ tính năng LS2 (LeaseSet 2) được mã hóa đã duy trì ổn định đến phiên bản 2.10.0 (Tháng 9 năm 2025), không có thay đổi phá vỡ tính tương thích đối với định dạng địa chỉ hoặc các đặc tả mật mã.

Các mốc triển khai quan trọng: - 0.9.38: Hỗ trợ Floodfill cho LS2 tiêu chuẩn với các khóa ngoại tuyến - 0.9.39: Kiểu chữ ký RedDSA loại 11 và mã hóa/giải mã cơ bản - 0.9.40: Hỗ trợ định địa chỉ B32 đầy đủ (Đề xuất 149) - 0.9.41: Xác thực theo từng máy khách dựa trên X25519 - 0.9.42: Tất cả các tính năng blinding (kỹ thuật làm mù trong mật mã học) đã hoạt động - 0.9.43: Tuyên bố triển khai hoàn chỉnh (Tháng 10 năm 2019)

## Thiết kế

- Định dạng mới chứa unblinded public key (khóa công khai không làm mù), unblinded signature type (kiểu chữ ký không làm mù), và blinded signature type (kiểu chữ ký làm mù).
- Tùy chọn cho biết các yêu cầu về bí mật và/hoặc khóa riêng cho các liên kết riêng tư.
- Sử dụng hậu tố ".b32.i2p" hiện có, nhưng với độ dài lớn hơn.
- Bao gồm checksum để phát hiện lỗi.
- Địa chỉ cho leasesets được mã hóa được nhận diện bởi 56 ký tự được mã hóa trở lên (35 byte được giải mã trở lên), so với 52 ký tự (32 byte) đối với các địa chỉ base 32 truyền thống.

## Đặc tả

### Tạo và mã hóa

Tạo một tên máy chủ dạng {56+ ký tự}.b32.i2p (35+ ký tự ở dạng nhị phân) như sau:

```
flag (1 byte)
  bit 0: 0 for one-byte sigtypes, 1 for two-byte sigtypes
  bit 1: 0 for no secret, 1 if secret is required
  bit 2: 0 for no per-client auth,
         1 if client private key is required
  bits 7-3: Unused, set to 0

public key sigtype (1 or 2 bytes as indicated in flags)
  If 1 byte, the upper byte is assumed zero

blinded key sigtype (1 or 2 bytes as indicated in flags)
  If 1 byte, the upper byte is assumed zero

public key
  Number of bytes as implied by sigtype
```
Hậu xử lý và checksum (tổng kiểm):

```
Construct the binary data as above.
Treat checksum as little-endian.
Calculate checksum = CRC-32(data[3:end])
data[0] ^= (byte) checksum
data[1] ^= (byte) (checksum >> 8)
data[2] ^= (byte) (checksum >> 16)

hostname = Base32.encode(data) || ".b32.i2p"
```
Bất kỳ bit chưa sử dụng nào ở cuối b32 phải bằng 0. Đối với một địa chỉ tiêu chuẩn 56 ký tự (35 byte), không có bit chưa sử dụng.

### Giải mã và Xác minh

```
strip the ".b32.i2p" from the hostname
data = Base32.decode(hostname)
Calculate checksum = CRC-32(data[3:end])
Treat checksum as little-endian.
flags = data[0] ^ (byte) checksum
if 1 byte sigtypes:
  pubkey sigtype = data[1] ^ (byte) (checksum >> 8)
  blinded sigtype = data[2] ^ (byte) (checksum >> 16)
else (2 byte sigtypes):
  pubkey sigtype = data[1] ^ ((byte) (checksum >> 8)) || data[2] ^ ((byte) (checksum >> 16))
  blinded sigtype = data[3] || data[4]
parse the remainder based on the flags to get the public key
```
### Độ dài (tính bằng bit) của khóa bí mật và khóa riêng

Các bit khóa bí mật và khóa riêng được dùng để cho client, proxy, hoặc mã phía client khác biết rằng cần có khóa bí mật và/hoặc khóa riêng để giải mã leaseset. Một số triển khai cụ thể có thể nhắc người dùng cung cấp dữ liệu cần thiết, hoặc từ chối các lần thử kết nối nếu thiếu dữ liệu cần thiết.

Các bit này chỉ dùng làm chỉ báo. Khóa bí mật hoặc khóa riêng tư tuyệt đối không được đưa vào chính địa chỉ B32, vì như vậy sẽ làm suy giảm tính bảo mật.

## Chi tiết mật mã học

### Lược đồ làm mù

Lược đồ làm mù sử dụng RedDSA dựa trên Ed25519 và thiết kế của ZCash, tạo ra các chữ ký Red25519 trên đường cong Ed25519 sử dụng SHA-512. Cách tiếp cận này đảm bảo các khóa công khai đã làm mù vẫn thuộc nhóm con có cấp nguyên tố của đường cong, tránh được các lo ngại về bảo mật tồn tại trong một số thiết kế thay thế.

Các Blinded keys (khóa đã làm mù) được luân chuyển hằng ngày dựa trên ngày UTC theo công thức:

```
blinded_key = BLIND(unblinded_key, date, optional_secret)
```
Vị trí lưu trữ trong DHT (bảng băm phân tán) được tính như sau:

```
SHA256(type_byte || blinded_public_key)
```
### Mã hóa

leaseSet được mã hóa sử dụng mật mã dòng ChaCha20 cho việc mã hóa, được lựa chọn vì hiệu năng vượt trội trên các thiết bị không có tăng tốc phần cứng AES. Đặc tả sử dụng HKDF (Hàm phái sinh khóa dựa trên HMAC) để phái sinh khóa và X25519 (thuật toán ECDH trên Curve25519) cho các hoạt động Diffie-Hellman (trao đổi khóa Diffie-Hellman).

Các leaseSet được mã hóa có cấu trúc ba lớp: - Lớp ngoài: siêu dữ liệu bản rõ - Lớp giữa: xác thực máy khách (các phương thức DH hoặc PSK) - Lớp trong: phần dữ liệu LS2 chính với thông tin lease

### Các phương thức xác thực

Xác thực theo từng client (máy khách) hỗ trợ hai phương thức:

**Xác thực DH**: Sử dụng thỏa thuận khóa X25519. Mỗi máy khách được ủy quyền sẽ cung cấp khóa công khai của mình cho máy chủ, và máy chủ mã hóa lớp giữa bằng một bí mật chung được dẫn xuất từ ECDH.

**PSK Authentication** (xác thực bằng khóa chia sẻ trước): Sử dụng trực tiếp khóa chia sẻ trước để mã hóa.

Bit cờ thứ 2 trong địa chỉ B32 cho biết liệu xác thực theo từng client có bắt buộc hay không.

## Bộ nhớ đệm

Dù vượt ngoài phạm vi của đặc tả này, các routers và clients phải ghi nhớ và lưu vào bộ nhớ đệm (khuyến nghị lưu bền) ánh xạ từ khóa công khai tới destination (định danh đích trong I2P), và ngược lại.

Blockfile naming service (dịch vụ đặt tên dạng blockfile), hệ thống sổ địa chỉ mặc định của I2P từ phiên bản 0.9.8, duy trì nhiều sổ địa chỉ cùng với một bảng ánh xạ tra ngược chuyên dụng, cung cấp khả năng tra cứu nhanh theo giá trị băm (hash). Tính năng này rất quan trọng để phân giải leaseSet được mã hóa khi ban đầu chỉ biết mỗi giá trị băm.

## Các loại chữ ký

Tính đến phiên bản I2P 2.10.0, các kiểu chữ ký từ 0 đến 11 đã được định nghĩa. Mã hóa một byte vẫn là tiêu chuẩn; mã hóa hai byte có sẵn nhưng trên thực tế không được sử dụng.

**Các loại thường dùng:** - Loại 0 (DSA_SHA1): Không còn được khuyến nghị cho router, vẫn được hỗ trợ cho các destination (đích trong I2P) - Loại 7 (EdDSA_SHA512_Ed25519): Tiêu chuẩn hiện tại cho danh tính router và các đích - Loại 11 (RedDSA_SHA512_Ed25519): Chỉ dùng cho các leaseSet LS2 được mã hóa có hỗ trợ blinding (kỹ thuật làm mù trong mật mã)

**Lưu ý quan trọng**: Chỉ Ed25519 (type 7) và Red25519 (type 11) hỗ trợ blinding (kỹ thuật làm mù trong mật mã) cần thiết cho các leasesets được mã hóa. Các loại chữ ký khác không thể được sử dụng với tính năng này.

Các loại 9-10 (GOST algorithms (thuật toán mật mã GOST)) vẫn được dành trước nhưng chưa được triển khai. Các loại 4-6 và 8 được đánh dấu "offline only" cho các khóa ký ngoại tuyến.

## Ghi chú

- Phân biệt biến thể cũ và mới theo độ dài. Địa chỉ b32 cũ luôn là {52 chars}.b32.i2p. Địa chỉ mới là {56+ chars}.b32.i2p
- Mã hóa base32 tuân theo tiêu chuẩn RFC 4648, giải mã không phân biệt hoa/thường và ưu tiên đầu ra chữ thường
- Địa chỉ có thể vượt quá 200 ký tự khi dùng các kiểu chữ ký có khóa công khai lớn hơn (ví dụ: ECDSA P521 với khóa 132 byte)
- Định dạng mới có thể được dùng trong jump links (liên kết tra cứu) (và được phục vụ bởi jump servers (máy chủ jump)) nếu muốn, tương tự như b32 tiêu chuẩn
- Blinded keys (khóa làm mù) luân phiên hằng ngày theo ngày UTC để tăng cường quyền riêng tư
- Định dạng này khác với cách tiếp cận ở phụ lục A.2 của Tor trong tệp rend-spec-v3.txt, có thể kéo theo các hệ quả bảo mật tiềm ẩn khi dùng off-curve blinded public keys (khóa công khai bị làm mù nằm ngoài đường cong)

## Tương thích phiên bản

Đặc tả này áp dụng cho I2P từ phiên bản 0.9.47 (tháng 8 năm 2020) đến phiên bản 2.10.0 (tháng 9 năm 2025). Không có thay đổi không tương thích ngược đối với định dạng địa chỉ B32, cấu trúc LS2 (LeaseSet phiên bản 2) được mã hóa, hoặc các triển khai mật mã học trong giai đoạn này. Tất cả các địa chỉ được tạo bằng 0.9.47 vẫn hoàn toàn tương thích với các phiên bản hiện tại.

## Tài liệu tham khảo

**CRC-32** - [CRC-32 (Wikipedia)](https://en.wikipedia.org/wiki/CRC-32) - [RFC 3309: Tổng kiểm (checksum) của Giao thức Truyền tải Điều khiển Luồng](https://tools.ietf.org/html/rfc3309)

**Các đặc tả I2P** - [Đặc tả LeaseSet được mã hóa](/docs/specs/encryptedleaseset/) - [Đề xuất 123: Mục nhập netDB mới](/proposals/123-new-netdb-entries/) - [Đề xuất 149: B32 cho LS2 được mã hóa](/proposals/149-b32-encrypted-ls2/) - [Đặc tả cấu trúc chung](/docs/specs/common-structures/) - [Đặt tên và Sổ địa chỉ](/docs/overview/naming/)

**So sánh Tor** - [Chuỗi thảo luận Tor (bối cảnh thiết kế)](https://lists.torproject.org/pipermail/tor-dev/2017-January/011816.html)

**Tài nguyên bổ sung** - [I2P Project](/) - [Diễn đàn I2P](https://i2pforum.net) - [Tài liệu Java API](http://docs.i2p-projekt.de/javadoc/)
