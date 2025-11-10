---
title: "Loại chữ ký GOST"
number: "134"
author: "orignal"
created: "2017-02-18"
lastupdated: "2017-03-31"
status: "Open"
thread: "http://zzz.i2p/topics/2239"
---

## Tổng quan

Chữ ký đường cong elliptic GOST R 34.10 được sử dụng bởi các quan chức và doanh nghiệp tại Nga. Hỗ trợ nó có thể đơn giản hóa việc tích hợp các ứng dụng hiện có (thường dựa trên CryptoPro). Hàm băm là GOST R 34.11 dài 32 hoặc 64 byte. Cơ bản hoạt động tương tự như EcDSA, kích thước chữ ký và khóa công khai là 64 hoặc 128 byte.

## Động lực

Mã hóa đường cong elliptic chưa bao giờ được tin tưởng hoàn toàn và gây ra nhiều suy đoán về các cửa hậu có thể có. Do đó, không có loại chữ ký tối ưu nào được mọi người tin tưởng. Thêm một loại chữ ký nữa sẽ cho phép người dùng lựa chọn dựa trên độ tin cậy của họ.

## Thiết kế

GOST R 34.10 sử dụng đường cong elliptic tiêu chuẩn với các tập thông số riêng. Có thể tái sử dụng toán học của các nhóm hiện có. Tuy nhiên, việc ký và xác minh là khác nhau và cần phải được triển khai. Xem RFC: https://www.rfc-editor.org/rfc/rfc7091.txt GOST R 34.10 được cho là hoạt động cùng với hàm băm GOST R 34.11. Chúng tôi sẽ sử dụng GOST R 34.10-2012 (còn gọi là steebog) với 256 hoặc 512 bit. Xem RFC: https://tools.ietf.org/html/rfc6986

GOST R 34.10 không xác định các thông số nhưng có một số tập thông số tốt được sử dụng rộng rãi. GOST R 34.10-2012 với khóa công khai dài 64 byte thừa hưởng tập thông số của CryptoPro từ GOST R 34.10-2001. Xem RFC: https://tools.ietf.org/html/rfc4357

Tuy nhiên, các tập thông số mới hơn cho khóa dài 128 byte được tạo bởi ủy ban kỹ thuật chuyên biệt tc26 (tc26.ru). Xem RFC: https://www.rfc-editor.org/rfc/rfc7836.txt

Việc triển khai dựa trên OpenSSL trong i2pd cho thấy nó nhanh hơn P256 và chậm hơn 25519.

## Chi tiết kỹ thuật

Chỉ hỗ trợ GOST R 34.10-2012 và GOST R 34.11-2012. Hai loại chữ ký mới: 9 - GOSTR3410_GOSTR3411_256_CRYPTO_PRO_A dành cho loại khóa công khai và chữ ký dài 64 byte, kích thước băm là 32 byte và tập thông số CryptoProA (còn gọi là CryptoProXchA) 10 - GOSTR3410_GOSTR3411_512_TC26_A dành cho loại khóa công khai và chữ ký dài 128 byte, kích thước băm là 64 byte và tập thông số A từ TC26.

## Chuyển đổi

Các loại chữ ký này được cho là chỉ được sử dụng như loại chữ ký tùy chọn. Không yêu cầu chuyển đổi. i2pd đã hỗ trợ nó.
