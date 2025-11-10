---
title: "LeaseSet 2"
number: "110"
author: "zzz"
created: "2014-01-22"
lastupdated: "2016-04-04"
status: "Bị Từ Chối"
thread: "http://zzz.i2p/topics/1560"
supercededby: "123"
---

## Tổng quan

Đề xuất này nói về định dạng LeaseSet mới với hỗ trợ cho các loại mã hóa mới hơn.

## Động lực

Mật mã đầu-cuối được sử dụng thông qua các đường hầm I2P có các khóa mã hóa và ký riêng biệt. Các khóa ký nằm trong điểm đến của đường hầm, mà đã được mở rộng với KeyCertificates để hỗ trợ các loại chữ ký mới hơn. Tuy nhiên, các khóa mã hóa là một phần của LeaseSet, vốn không chứa bất kỳ Chứng chỉ nào. Do đó, cần thiết phải triển khai một định dạng LeaseSet mới và thêm hỗ trợ để lưu trữ nó trong netDb.

Điểm tích cực là một khi LS2 được triển khai, tất cả các Điểm đến hiện có có thể sử dụng các loại mã hóa hiện đại hơn; các bộ định tuyến có thể lấy và đọc một LS2 sẽ được đảm bảo hỗ trợ cho bất kỳ loại mã hóa nào được giới thiệu cùng với nó.

## Đặc tả

Định dạng cơ bản của LS2 sẽ như sau:

- đích
- dấu thời gian công bố (8 byte)
- hết hạn (8 byte)
- kiểu phụ (1 byte) (thường, mã hóa, meta, hoặc dịch vụ)
- cờ (2 byte)

- phần đặc thù của kiểu phụ:
  - loại mã hóa, khóa mã hóa và thuê cho loại thường
  - blob cho mã hóa
  - thuộc tính, băm, cổng, thu hồi, v.v. cho dịch vụ

- chữ ký
