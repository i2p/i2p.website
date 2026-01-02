---
title: "v3dgsend"
description: "Tiện ích CLI để gửi datagram I2P qua SAM v3"
slug: "v3dgsend"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

> Trạng thái: Đây là tài liệu tham khảo ngắn gọn cho tiện ích `v3dgsend`. Nó bổ sung cho tài liệu [Datagram API](/docs/api/datagrams/) và [SAM v3](/docs/api/samv3/).

## Tổng quan

`v3dgsend` là công cụ dòng lệnh hỗ trợ gửi datagram I2P sử dụng giao diện SAM v3. Nó hữu ích cho việc kiểm tra việc phân phối datagram, xây dựng nguyên mẫu dịch vụ, và xác minh hành vi đầu cuối đến đầu cuối mà không cần viết một client đầy đủ.

Các trường hợp sử dụng điển hình bao gồm:

- Kiểm tra khả năng tiếp cận datagram đến một Destination
- Xác thực cấu hình tường lửa và sổ địa chỉ
- Thử nghiệm với datagram thô so với datagram đã ký (có thể trả lời)

## Sử dụng

Cách gọi cơ bản thay đổi tùy theo nền tảng và cách đóng gói. Các tùy chọn phổ biến bao gồm:

- Destination: Destination dạng base64 hoặc tên `.i2p`
- Protocol: raw (PROTOCOL 18) hoặc signed (PROTOCOL 17)
- Payload: chuỗi inline hoặc đầu vào từ file

Tham khảo tài liệu đóng gói của bản phân phối hoặc kết quả từ `--help` để biết chính xác các cờ lệnh.

## Xem thêm

- [Datagram API](/docs/api/datagrams/)
- [SAM v3](/docs/api/samv3/)
- [Streaming Library](/docs/api/streaming/) (thay thế cho datagram)
