---
title: "Làm mờ khóa ECDSA"
number: "151"
author: "orignal"
created: "2019-05-21"
lastupdated: "2019-05-29"
status: "Open"
thread: "http://zzz.i2p/topics/2717"
toc: true
---

## Động lực

Một số người không thích EdDSA hoặc RedDSA. Chúng ta nên cung cấp một số lựa chọn thay thế và để họ làm mờ chữ ký ECDSA.

## Tổng quan

Đề xuất này mô tả việc làm mờ khóa cho các loại chữ ký ECDSA 1, 2, 3.

## Đề xuất

Hoạt động giống như RedDSA, nhưng mọi thứ ở dạng Big Endian.
Chỉ cho phép cùng loại chữ ký, ví dụ: 1->1, 2->2, 3->3.

### Định nghĩa

B
    Điểm cơ sở của đường cong

L
    Thứ tự nhóm của đường cong Elliptic. Tính chất của đường cong.

DERIVE_PUBLIC(a)
    Chuyển đổi một khóa riêng tư thành khóa công cộng, bằng cách nhân B trên một đường cong elliptic

alpha
    Một số ngẫu nhiên 32 byte được biết đến bởi những người biết đích đến.

GENERATE_ALPHA(destination, date, secret)
    Tạo alpha cho ngày hiện tại, cho những người biết đến đích đến và bí mật.

a
    Khóa riêng tư ký 32 byte không bị làm mờ, được dùng để ký đích đến

A
    Khóa công công 32 byte không bị làm mờ trong đích đến,
    = DERIVE_PUBLIC(a), như trong đường cong tương ứng

a'
    Khóa riêng tư ký 32 byte bị làm mờ, dùng để ký leaseset mã hóa
    Đây là một khóa riêng tư ECDSA hợp lệ.

A'
    Khóa công ký ECDSA 32 byte bị làm mờ trong Đích đến,
    có thể được tạo ra với DERIVE_PUBLIC(a'), hoặc từ A và alpha.
    Đây là một khóa công ECDSA hợp lệ trên đường cong

H(p, d)
    Hàm băm SHA-256 nhận một chuỗi cá nhân hoá p và dữ liệu d, và
    sinh ra đầu ra có độ dài 32 byte.

    Sử dụng SHA-256 như sau::

        H(p, d) := SHA-256(p || d)

HKDF(salt, ikm, info, n)
    Một hàm phái sinh khóa mã hóa nhận một số liệu đầu vào ikm (nên có entropy tốt nhưng không yêu cầu là một chuỗi ngẫu nhiên đồng đều), một muối có độ dài 32 byte, và một giá trị 'info' cụ thể theo ngữ cảnh, và sinh ra đầu ra
    có độ dài n byte phù hợp để sử dụng làm liệu khóa.

    Sử dụng HKDF như được chỉ định trong [RFC-5869](https://tools.ietf.org/html/rfc5869), sử dụng hàm băm HMAC SHA-256
    như được chỉ định trong [RFC-2104](https://tools.ietf.org/html/rfc2104). Điều này có nghĩa là SALT_LEN là tối đa 32 byte.


### Tính toán làm mờ

Một alpha bí mật mới và các khóa bị làm mờ phải được tạo ra mỗi ngày (UTC).
Alpha bí mật và các khóa bị làm mờ được tính toán như sau.

GENERATE_ALPHA(destination, date, secret), cho tất cả các bên:

```text
// GENERATE_ALPHA(destination, date, secret)

  // bí mật là tùy chọn, nếu không thì chuỗi rỗng
  A = khóa công ký của đích đến
  stA = loại chữ ký của A, 2 byte big endian (0x0001, 0x0002 hoặc 0x0003)
  stA' = loại chữ ký của khóa công bị làm mờ A', 2 byte big endian, luôn giống như stA
  keydata = A || stA || stA'
  datestring = 8 byte ASCII YYYYMMDD từ ngày hiện tại UTC
  bí mật = chuỗi mã hóa UTF-8
  seed = HKDF(H("I2PGenerateAlpha", keydata), datestring || secret, "i2pblinding1", 64)
  // xử lý seed như một giá trị big-endian 64 byte
  alpha = seed mod L
```


BLIND_PRIVKEY(), cho chủ sở hữu phát hành leaseset:

```text
// BLIND_PRIVKEY()

  alpha = GENERATE_ALPHA(destination, date, secret)
  a = khóa riêng tư ký của đích đến
  // Cộng sử dụng số học vô hướng
  khóa riêng tư ký bị làm mờ = a' = BLIND_PRIVKEY(a, alpha) = (a + alpha) mod L
  khóa công ký bị làm mờ = A' = DERIVE_PUBLIC(a')
```


BLIND_PUBKEY(), cho các khách hàng lấy leaseset:

```text
// BLIND_PUBKEY()

  alpha = GENERATE_ALPHA(destination, date, secret)
  A = khóa công ký của đích đến
  // Cộng sử dụng các phần tử nhóm (điểm trên đường cong)
  khóa công bị làm mờ = A' = BLIND_PUBKEY(A, alpha) = A + DERIVE_PUBLIC(alpha)
```


Cả hai phương pháp tính toán A' đều cho kết quả giống nhau, như yêu cầu.

## Địa chỉ b33

Khóa công của ECDSA là cặp (X, Y), vì vậy đối với P256, ví dụ, nó là 64 byte, thay vì 32 như RedDSA.
Địa chỉ b33 sẽ dài hơn, hoặc khóa công có thể được lưu trữ dưới dạng nén như trong ví bitcoin.


## Tài liệu tham khảo

* [RFC-2104](https://tools.ietf.org/html/rfc2104)
* [RFC-5869](https://tools.ietf.org/html/rfc5869)
