---
title: "'Cờ' Truyền Tải Được Mã Hóa"
number: "114"
author: "orignal"
created: "2015-01-21"
lastupdated: "2015-01-21"
status: "Cần-Nghiên-Cứu"
thread: "http://zzz.i2p/topics/1795"
---

## Tổng Quan

Đề xuất này liên quan đến việc thêm một cờ vào truyền tải để chỉ định loại mã hóa
end-to-end đang được sử dụng.

## Động Lực

Các ứng dụng có tải cao có thể gặp phải tình trạng thiếu thẻ ElGamal/AES+SessionTags.

## Thiết Kế

Thêm một cờ mới ở đâu đó trong giao thức truyền tải. Nếu một gói dữ liệu đến với
cờ này, điều đó có nghĩa là payload được mã hóa AES bằng khóa từ khóa riêng tư và
khóa công khai của đồng nghiệp. Điều này sẽ cho phép loại bỏ mã hóa tỏi (ElGamal/AES)
và khắc phục vấn đề thiếu thẻ.

Có thể được thiết lập theo gói hoặc theo luồng thông qua SYN.
