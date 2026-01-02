---
title: "Giao thức truyền tải SSU (Không còn được khuyến nghị)"
description: "Giao thức truyền tải UDP ban đầu được sử dụng trước SSU2"
slug: "ssu"
lastUpdated: "2024-01"
accurateFor: "0.9.61"
type: docs
reviewStatus: "needs-review"
---

> **Đã ngừng sử dụng:** SSU (UDP bán tin cậy bảo mật) đã được thay thế bởi [SSU2](/docs/specs/ssu2/). Java I2P đã loại bỏ SSU trong phiên bản 2.4.0 (API 0.9.61) và i2pd đã loại bỏ nó trong phiên bản 2.44.0 (API 0.9.56). Tài liệu này chỉ được giữ lại để tham khảo lịch sử.

## Điểm nổi bật

- Giao thức truyền tải UDP cung cấp chuyển giao điểm-đến-điểm đã mã hóa, có xác thực cho các thông điệp I2NP.
- Dựa trên một bắt tay Diffie–Hellman (giao thức trao đổi khóa) 2048-bit (dùng cùng số nguyên tố như ElGamal).
- Mỗi gói tin (datagram) mang một HMAC-MD5 16 byte (biến thể rút gọn không tiêu chuẩn) + một IV 16 byte, tiếp theo là phần tải dữ liệu được mã hóa bằng AES-256-CBC.
- Ngăn chặn phát lại và trạng thái phiên được theo dõi bên trong phần tải dữ liệu đã mã hóa.

## Tiêu đề thông điệp

```
[16-byte MAC][16-byte IV][encrypted payload]
```
Phép tính MAC (mã xác thực thông điệp) được sử dụng: `HMAC-MD5(ciphertext || IV || (len ^ version ^ ((netid-2)<<8)))` với khóa MAC dài 32 byte. Độ dài payload là 16-bit big-endian (MSB trước) được thêm vào trong phép tính MAC. Phiên bản giao thức mặc định là `0`; netId mặc định là `2` (mạng chính).

## Khóa Phiên & Khóa MAC (mã xác thực thông điệp)

Được dẫn xuất từ bí mật chung DH (Diffie–Hellman):

1. Chuyển giá trị được chia sẻ thành mảng byte theo big-endian (thêm `0x00` ở đầu nếu bit cao được đặt).
2. Khóa phiên: 32 byte đầu tiên (đệm bằng số 0 nếu ngắn hơn).
3. Khóa MAC: các byte 33–64; nếu không đủ, quay về băm SHA-256 của giá trị được chia sẻ.

## Trạng thái

Các router không còn quảng bá các địa chỉ SSU. Các máy khách nên chuyển sang các giao thức truyền tải SSU2 hoặc NTCP2. Các triển khai trước đây có thể được tìm thấy trong các bản phát hành cũ:

- Mã nguồn Java trước phiên bản 2.4.0 trong thư mục `router/transport/udp`
- Mã nguồn i2pd (triển khai I2P bằng C++) trước phiên bản 2.44.0

Để biết hành vi truyền tải UDP hiện tại, hãy tham khảo [đặc tả SSU2](/docs/specs/ssu2/).
