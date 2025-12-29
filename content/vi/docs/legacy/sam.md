---
title: "SAM v1"
description: "Giao thức Simple Anonymous Messaging (gửi tin nhắn ẩn danh đơn giản) dạng cũ (không còn được khuyến nghị sử dụng)"
slug: "sam"
lastUpdated: "2025-03"
accurateFor: "0.9.20"
reviewStatus: "needs-review"
---

> **Không còn được khuyến nghị:** SAM v1 chỉ được giữ lại để tham khảo lịch sử. Các ứng dụng mới nên sử dụng [SAM v3](/docs/api/samv3/) hoặc [BOB](/docs/legacy/bob/). Cầu nối ban đầu chỉ hỗ trợ các đích DSA-SHA1 và một tập tùy chọn hạn chế.

## Thư viện

Cây mã nguồn Java I2P vẫn bao gồm các bindings (thư viện liên kết ngôn ngữ) cũ cho C, C#, Perl và Python. Chúng không còn được bảo trì và chủ yếu được phát hành kèm để duy trì khả năng tương thích cho mục đích lưu trữ.

## Đàm phán phiên bản

Các máy khách kết nối qua TCP (mặc định `127.0.0.1:7656`) và trao đổi:

```
Client → HELLO VERSION MIN=1 MAX=1
Bridge → HELLO REPLY RESULT=OK VERSION=1.0
```
Kể từ Java I2P 0.9.14, tham số `MIN` là tùy chọn và cả `MIN`/`MAX` chấp nhận dạng một chữ số (`"3"` v.v.) đối với các bridge (nút cầu nối) đã nâng cấp.

## Tạo phiên

```
SESSION CREATE STYLE={STREAM|DATAGRAM|RAW} DESTINATION={name|TRANSIENT} [DIRECTION={BOTH|RECEIVE|CREATE}] [option=value]*
```
- `DESTINATION=name` tải hoặc tạo một mục trong `sam.keys`; `TRANSIENT` luôn tạo một đích tạm thời.
- `STYLE` chọn luồng ảo (giống TCP), datagram có chữ ký, hoặc datagram thô.
- `DIRECTION` chỉ áp dụng cho các phiên luồng; mặc định là `BOTH`.
- Các cặp khóa/giá trị bổ sung được chuyển tiếp như các tùy chọn I2CP (ví dụ, `tunnels.quantityInbound=3`).

Cầu nối phản hồi như sau:

```
SESSION STATUS RESULT=OK DESTINATION=name
```
Khi gặp lỗi, sẽ trả về `DUPLICATED_DEST`, `I2P_ERROR` hoặc `INVALID_KEY` kèm theo một thông báo tùy chọn.

## Định dạng thông điệp

Các thông điệp SAM ở dạng ASCII một dòng, với các cặp khóa/giá trị được phân tách bằng khoảng trắng. Các khóa sử dụng UTF‑8; các giá trị có thể được đặt trong dấu ngoặc kép nếu chúng chứa khoảng trắng. Không có escaping (cơ chế thêm ký tự thoát) được định nghĩa.

Các loại liên lạc:

- **Luồng** – được chuyển tiếp thông qua I2P streaming library (thư viện streaming của I2P)
- **Gói tin có thể hồi đáp** – payload (nội dung dữ liệu) đã được ký (Datagram1)
- **Gói tin thô** – payload chưa được ký (Datagram RAW)

## Các tùy chọn được bổ sung trong 0.9.14

- `DEST GENERATE` chấp nhận `SIGNATURE_TYPE=...` (cho phép Ed25519, v.v.)
- `HELLO VERSION` xem `MIN` là tùy chọn và chấp nhận chuỗi phiên bản một chữ số

## Khi nào nên sử dụng SAM v1 (API Simple Anonymous Messaging của I2P)

Chỉ nhằm bảo đảm khả năng tương tác với phần mềm cũ không thể cập nhật. Đối với mọi phát triển mới, hãy sử dụng:

- [SAM v3](/docs/api/samv3/) để truy cập stream/datagram đầy đủ tính năng
- [BOB](/docs/legacy/bob/) để quản lý Destination (điểm đích) (vẫn còn hạn chế, nhưng hỗ trợ nhiều tính năng hiện đại hơn)

## Tài liệu tham khảo

- [SAM v2](/docs/legacy/samv2/)
- [SAM v3](/docs/api/samv3/)
- [Đặc tả Datagram](/docs/api/datagrams/)
- [Giao thức truyền phát](/docs/specs/streaming/)

SAM v1 đã đặt nền tảng cho việc phát triển ứng dụng không phụ thuộc router, nhưng hệ sinh thái đã tiến xa hơn. Hãy xem tài liệu này như một công cụ hỗ trợ khả năng tương thích, thay vì một điểm khởi đầu.
