---
title: "B32 cho LS2 mã hóa"
number: "149"
author: "zzz"
created: "2019-03-13"
lastupdated: "2020-08-05"
status: "Đã đóng"
thread: "http://zzz.i2p/topics/2682"
target: "0.9.40"
implementedin: "0.9.40"
---

## Lưu ý
Triển khai và thử nghiệm mạng đang được tiến hành.
Có thể thay đổi nhỏ.
Xem [SPEC](/docs/specs/b32-for-encrypted-leasesets/) để biết đặc tả chính thức.


## Tổng quan

Địa chỉ Base 32 ("b32") tiêu chuẩn chứa băm của đích đến.
Điều này sẽ không hoạt động đối với ls2 mã hóa (đề xuất 123).

Bạn không thể sử dụng địa chỉ base 32 truyền thống cho LS2 mã hóa (đề xuất 123),
vì nó chỉ chứa băm của đích đến. Nó không cung cấp khóa công khai không bị che dấu.
Khách hàng cần biết khóa công khai của đích đến, loại chữ ký,
loại chữ ký bị che dấu, và một khóa bí mật hoặc riêng tư tùy chọn
để tìm nạp và giải mã leaseset.
Do đó, chỉ địa chỉ base 32 là không đủ.
Khách hàng cần hoặc là đích đến đầy đủ (chứa khóa công khai),
hoặc chỉ riêng khóa công khai.
Nếu khách hàng có đích đến đầy đủ trong danh bạ, và danh bạ
hỗ trợ tra cứu ngược theo băm, thì khóa công khai có thể được lấy ra.

Vì vậy, chúng ta cần một định dạng mới đặt khóa công khai thay vì băm vào
một địa chỉ base32. Định dạng này cũng phải chứa loại chữ ký của
khóa công khai, và loại chữ ký của sơ đồ che dấu.

Đề xuất này tài liệu hóa một định dạng b32 mới cho các địa chỉ này.
Mặc dù chúng tôi đã gọi định dạng mới này trong các cuộc thảo luận
như là địa chỉ "b33", định dạng mới thực tế vẫn giữ phần đuôi ".b32.i2p" thông thường.

## Mục tiêu

- Bao gồm cả loại chữ ký không bị che dấu và bị che dấu để hỗ trợ các sơ đồ che dấu trong tương lai
- Hỗ trợ khóa công khai lớn hơn 32 byte
- Đảm bảo các ký tự b32 hoàn toàn hoặc hầu hết ngẫu nhiên, đặc biệt là ở đầu
  (không muốn tất cả các địa chỉ bắt đầu bằng các ký tự giống nhau)
- Có thể phân tích cú pháp
- Chỉ ra rằng cần có một bí mật che dấu và/hoặc khóa riêng cho mỗi khách hàng
- Thêm mã kiểm để phát hiện lỗi đánh máy
- Giảm thiểu độ dài, duy trì độ dài nhãn DNS dưới 63 ký tự cho việc sử dụng thông thường
- Tiếp tục sử dụng base 32 để tránh phân biệt hoa thường
- Giữ phần đuôi ".b32.i2p" thông thường.

## Không mục tiêu

- Không hỗ trợ các liên kết "riêng tư" bao gồm bí mật che dấu và/hoặc khóa riêng cho mỗi khách hàng;
  điều này sẽ không an toàn.


## Thiết kế

- Định dạng mới sẽ chứa khóa công khai không bị che dấu, loại chữ ký không bị che dấu,
  và loại chữ ký bị che dấu.
- Tùy chọn chứa một khóa bí mật và/hoặc khóa riêng, chỉ dành cho các liên kết riêng tư
- Sử dụng phần đuôi ".b32.i2p" hiện có, nhưng với độ dài lớn hơn.
- Thêm mã kiểm.
- Địa chỉ cho các leaseset mã hóa được xác định bằng 56 ký tự mã hóa trở lên
  (35 byte trở lên được giải mã), so với 52 ký tự (32 byte) cho các địa chỉ base 32 truyền thống.


## Đặc tả

### Tạo và mã hóa

Tạo một tên máy chủ có {56+ ký tự}.b32.i2p (35+ ký tự trong nhị phân) như sau:

```text
cờ (1 byte)
    bit 0: 0 đối với loại chữ ký một byte, 1 đối với loại chữ ký hai byte
    bit 1: 0 nếu không có bí mật, 1 nếu yêu cầu bí mật
    bit 2: 0 nếu không có xác thực cho từng khách hàng,
           1 nếu yêu cầu khóa riêng cho mỗi khách hàng
    bits 7-3: Không sử dụng, đặt thành 0

  loại chữ ký khóa công khai (1 hoặc 2 byte như được chỉ định trong cờ)
    Nếu 1 byte, byte cao hơn mặc định là zero

  loại chữ ký bị che dấu (1 hoặc 2 byte như được chỉ định trong cờ)
    Nếu 1 byte, byte cao hơn mặc định là zero

  khóa công khai
    Số byte như được ngụ ý bởi loại chữ ký

```

Xử lý hậu mã hóa và mã kiểm:

```text
Tạo dữ liệu nhị phân như trên.
  Xử lý mã kiểm như little-endian.
  Tính toán mã kiểm = CRC-32(data[3:end])
  data[0] ^= (byte) mã kiểm
  data[1] ^= (byte) (mã kiểm >> 8)
  data[2] ^= (byte) (mã kiểm >> 16)

  tên máy chủ = Base32.encode(data) || ".b32.i2p"
```

Bất kỳ bit nào không sử dụng ở cuối b32 phải là 0.
Không có bit không sử dụng nào cho một địa chỉ chuẩn 56 ký tự (35 byte).


### Giải mã và Xác minh

```text
Xóa ".b32.i2p" khỏi tên máy chủ
  data = Base32.decode(tên máy chủ)
  Tính toán mã kiểm = CRC-32(data[3:end])
  Xử lý mã kiểm như little-endian.
  cờ = data[0] ^ (byte) mã kiểm
  nếu loại chữ ký 1 byte:
    loại chữ ký khóa công khai = data[1] ^ (byte) (mã kiểm >> 8)
    loại chữ ký bị che dấu = data[2] ^ (byte) (mã kiểm >> 16)
  nếu không (loại chữ ký 2 byte) :
    loại chữ ký khóa công khai = data[1] ^ ((byte) (mã kiểm >> 8)) || data[2] ^ ((byte) (mã kiểm >> 16))
    loại chữ ký bị che dấu = data[3] || data[4]
  phân tích cú pháp phần còn lại dựa trên cờ để lấy khóa công khai
```


### Bit Bí mật và Khóa Riêng

Các bit bí mật và khóa riêng được sử dụng để chỉ ra cho khách hàng, đại lý, hoặc mã phía khách hàng khác rằng bí mật và/hoặc khóa riêng sẽ được yêu cầu để giải mã leaseset. Các triển khai cụ thể có thể yêu cầu người dùng cung cấp dữ liệu cần thiết, hoặc từ chối các nỗ lực kết nối nếu dữ liệu cần thiết bị thiếu.


## Biện minh

- XOR hóa 3 byte đầu tiên với băm cung cấp khả năng mã kiểm giới hạn,
  và đảm bảo rằng tất cả các ký tự base32 ở đầu được ngẫu nhiên hóa.
  Chỉ có một vài kết hợp cờ và loại chữ ký hợp lệ, vì vậy bất kỳ lỗi đánh máy nào có khả năng tạo ra một kết hợp không hợp lệ và sẽ bị từ chối.
- Trong trường hợp thông thường (1 byte loại chữ ký, không có bí秘密 mật, không có xác thực cho từng khách hàng),
  tên máy chủ sẽ là {56 ký tự}.b32.i2p, giải mã thành 35 byte, tương tự Tor.
- Kiểm tra checksum 2 byte của Tor có tỷ lệ âm sai là 1/64K. Với 3 byte, trừ đi một vài byte bị bỏ qua,
  chúng tôi dự kiến sẽ tiến gần 1 trên một triệu, do hầu hết các kết hợp cờ/loại chữ ký không hợp lệ.
- Adler-32 là lựa chọn kém cho các đầu vào nhỏ, và để phát hiện thay đổi nhỏ .
  Sử dụng CRC-32 thay thế. CRC-32 nhanh và có sẵn rộng rãi.

## Lưu trữ tạm thời

Mặc dù nằm ngoài phạm vi của đề xuất này, các router và/hoặc khách hàng phải ghi nhớ và lưu trữ tạm thời
(có thể là mãi mãi) ánh xạ của khóa công khai đến điểm đến, và ngược lại.



## Ghi chú

- Phân biệt các kiểu cũ và mới bằng độ dài. Các địa chỉ b32 cũ luôn là {52 ký tự}.b32.i2p. Các địa chỉ mới là {56+ ký tự}.b32.i2p
- Chủ đề thảo luận Tor: https://lists.torproject.org/pipermail/tor-dev/2017-January/011816.html
- Đừng kỳ vọng các loại chữ ký 2-byte sẽ xảy ra, chúng ta chỉ mới lên đến 13. Không cần phải thực hiện bây giờ.
- Định dạng mới có thể được sử dụng trong các liên kết nhảy (và phục vụ bởi các máy chủ nhảy) nếu muốn, giống như b32.


## Vấn đề

- Bất kỳ bí mật, khóa riêng, hoặc khóa công khai nào dài hơn 32 byte sẽ
  vượt quá độ dài nhãn tối đa của DNS là 63 ký tự. Trình duyệt có thể không quan tâm.


## Di chuyển

Không có vấn đề tương thích ngược. Các địa chỉ b32 dài hơn sẽ không thể chuyển đổi
thành băm 32-bytes trong phần mềm cũ.
