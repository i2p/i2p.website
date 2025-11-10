---
title: "Phát đa hướng"
number: "101"
author: "zzz"
created: "2008-12-08"
lastupdated: "2009-03-25"
status: "Ngừng"
thread: "http://zzz.i2p/topics/172"
---

## Tổng quan

Ý tưởng cơ bản: Gửi một bản sao thông qua đường hầm đi ra, điểm cuối ra phát cho tất cả các cổng vào. Mã hóa đầu cuối không được thực hiện.


## Thiết kế

- Loại thông điệp đường hầm phát đa hướng mới (loại giao nhận = 0x03)
- Điểm cuối ra phát đa hướng
- Loại thông điệp I2NP Phát Đa Hướng mới?
- Loại thông điệp I2CP Gửi Thông Điệp Phát Đa Hướng mới
- Không mã hóa router-router trong OutNetMessageOneShotJob (garlic?)

Ứng dụng:

- Proxy RTSP?

Streamr:

- Điều chỉnh MTU? Hoặc chỉ thực hiện điều này tại ứng dụng?
- Nhận & truyền theo yêu cầu
