---
title: "SAM v2"
description: "Giao thức Simple Anonymous Messaging (nhắn tin ẩn danh đơn giản) cũ"
slug: "samv2"
lastUpdated: "2025-03"
accurateFor: "0.9.20"
reviewStatus: "needs-review"
---

> **Đã lỗi thời:** SAM v2 được phát hành kèm I2P 0.6.1.31 và không còn được duy trì. Hãy dùng [SAM v3](/docs/api/samv3/) cho các phát triển mới. Cải tiến duy nhất của v2 so với v1 là hỗ trợ nhiều socket được ghép kênh qua một kết nối SAM duy nhất.

## Ghi chú phiên bản

- Chuỗi phiên bản được báo cáo vẫn là "2.0".
- Kể từ 0.9.14, thông điệp `HELLO VERSION` chấp nhận các giá trị `MIN`/`MAX` một chữ số và tham số `MIN` là tùy chọn.
- `DEST GENERATE` hỗ trợ `SIGNATURE_TYPE`, vì vậy có thể tạo các đích Ed25519.

## Những điều cơ bản về phiên

```
SESSION CREATE STYLE={STREAM|DATAGRAM|RAW} DESTINATION={name|TRANSIENT} [DIRECTION={BOTH|RECEIVE|CREATE}] [option=value]
```
- Mỗi Destination (đích I2P) chỉ được có một phiên SAM đang hoạt động (luồng, datagram hoặc thô).
- `STYLE` chọn giữa luồng ảo, datagram có chữ ký, hoặc datagram thô.
- Các tùy chọn bổ sung được chuyển tới I2CP (ví dụ, `tunnels.quantityInbound=3`).
- Phản hồi giống v1: `SESSION STATUS RESULT=OK|DUPLICATED_DEST|I2P_ERROR|INVALID_KEY`.

## Mã hóa thông điệp

ASCII theo từng dòng với các cặp `key=value` được phân tách bằng khoảng trắng (giá trị có thể được đặt trong dấu ngoặc kép). Các loại giao tiếp giống như v1:

- Luồng qua thư viện streaming của I2P
- Datagram (gói tin) có thể phản hồi (`PROTO_DATAGRAM`)
- Datagram thô (`PROTO_DATAGRAM_RAW`)

## Khi nào nên sử dụng

Chỉ dành cho các ứng dụng khách cũ (legacy) không thể chuyển đổi. SAM v3 cung cấp:

- Chuyển giao đích dạng nhị phân (`DEST GENERATE BASE64`)
- Hỗ trợ Subsessions (phiên con) và DHT (v3.3)
- Báo cáo lỗi tốt hơn và đàm phán tùy chọn

Tham khảo:

- [SAM v1](/docs/legacy/sam/)
- [SAM v3](/docs/api/samv3/)
- [API Datagram (gói tin không kết nối)](/docs/api/datagrams/)
- [Giao thức truyền phát](/docs/specs/streaming/)
