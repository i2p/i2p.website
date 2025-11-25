---
title: "LeaseSet Mã hóa"
number: "121"
author: "zzz"
created: "2016-01-11"
lastupdated: "2016-01-12"
status: "Bị từ chối"
thread: "http://zzz.i2p/topics/2047"
supercededby: "123"
---

## Tổng quan

Đề xuất này là về việc thiết kế lại cơ chế mã hóa LeaseSets.

## Động lực

LeaseSet mã hóa hiện tại rất tệ và không an toàn. Tôi có thể nói vậy, vì tôi đã thiết kế và triển khai nó.

Lý do:

- Mã hóa AES CBC
- Một khóa AES duy nhất cho tất cả mọi người
- Ngày hết hạn Lease vẫn bị lộ
- Khóa công khai mã hóa vẫn bị lộ

## Thiết kế

### Mục tiêu

- Làm cho toàn bộ trở nên không thể nhìn thấy
- Khóa cho từng người nhận

### Chiến lược

Làm như GPG/OpenPGP đã làm. Mã hóa đối xứng một khóa bất đối xứng cho mỗi người nhận. Dữ liệu được giải mã bằng khóa bất đối xứng đó. Xem ví dụ [RFC-4880-S5.1](https://tools.ietf.org/html/rfc4880#section-5.1)
NẾU chúng ta có thể tìm thấy một thuật toán nhỏ và nhanh.

Thủ thuật là tìm một mã hóa bất đối xứng nhỏ và nhanh. ElGamal với 514 byte có chút khó khăn ở đây. Chúng ta có thể làm tốt hơn.

Xem ví dụ: http://security.stackexchange.com/questions/824...

Điều này hoạt động với số lượng nhỏ người nhận (hoặc thực tế là khóa; bạn vẫn có thể phân phối khóa cho nhiều người nếu muốn).

## Chi tiết kỹ thuật

- Đích đến
- Dấu thời gian công bố
- Thời hạn
- Cờ
- Độ dài dữ liệu
- Dữ liệu mã hóa
- Chữ ký

Dữ liệu mã hóa có thể được đặt trước bởi một trình chỉ định enctype, hoặc không.

## Tham khảo

.. [RFC-4880-S5.1]
    https://tools.ietf.org/html/rfc4880#section-5.1
