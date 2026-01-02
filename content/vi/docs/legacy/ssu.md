---
title: "SSU (cũ)"
description: "Giao thức truyền tải Secure Semireliable UDP (UDP bảo mật bán tin cậy) nguyên bản"
slug: "ssu"
lastUpdated: "2025-01"
accurateFor: "0.9.64"
reviewStatus: "needs-review"
---

> **Đã lỗi thời:** SSU đã được thay thế bởi SSU2. Hỗ trợ đã bị gỡ bỏ trong i2pd 2.44.0 (API 0.9.56, tháng 11 năm 2022) và trong Java I2P 2.4.0 (API 0.9.61, tháng 12 năm 2023).

SSU cung cấp truyền tải bán tin cậy dựa trên UDP, kèm kiểm soát tắc nghẽn, xuyên NAT và hỗ trợ introducer (nút giới thiệu). Nó bổ trợ cho NTCP bằng cách xử lý các router ở sau NAT/tường lửa và điều phối việc khám phá IP.

## Các thành phần địa chỉ

- `transport`: `SSU`
- `caps`: cờ khả năng (`B`, `C`, `4`, `6`, v.v.)
- `host` / `port`: trình lắng nghe IPv4 hoặc IPv6 (tùy chọn khi bị chặn bởi tường lửa)
- `key`: khóa giới thiệu Base64
- `mtu`: Tùy chọn; mặc định 1484 (IPv4) / 1488 (IPv6)
- `ihost/ikey/iport/itag/iexp`: introducer entries (các mục giới thiệu) khi router bị tường lửa chặn

## Tính năng

- Xuyên NAT hợp tác bằng cách sử dụng introducers (nút giới thiệu)
- Phát hiện IP cục bộ thông qua kiểm tra ngang hàng và kiểm tra các gói tin đến
- Tự động chuyển tiếp trạng thái tường lửa đến các phương thức truyền tải khác và bảng điều khiển router
- Giao nhận bán tin cậy: các thông điệp được truyền lại đến một giới hạn, rồi bị loại bỏ
- Điều khiển tắc nghẽn với tăng cộng / giảm nhân và các trường bit ACK cho phân mảnh

SSU cũng xử lý các tác vụ siêu dữ liệu như timing beacons (đèn hiệu định thời) và thương lượng MTU (đơn vị truyền tối đa). Hiện toàn bộ chức năng (với mật mã hiện đại) do [SSU2](/docs/specs/ssu2/) cung cấp.
