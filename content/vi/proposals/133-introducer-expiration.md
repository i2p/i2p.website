---
title: "Giới thiệu Hết hạn"
number: "133"
author: "zzz"
created: "2017-02-05"
lastupdated: "2017-08-09"
status: "Closed"
thread: "http://zzz.i2p/topics/2230"
target: "0.9.30"
implementedin: "0.9.30"
---

## Tổng quan

Đề xuất này nhằm cải thiện tỷ lệ thành công cho việc giới thiệu.


## Động lực

Người giới thiệu hết hạn sau một thời gian nhất định, nhưng thông tin đó không được công bố trong
RouterInfo. Các router hiện tại phải sử dụng các phương pháp suy đoán để ước tính khi nào một người giới thiệu không còn hợp lệ.


## Thiết kế

Trong một RouterAddress SSU chứa người giới thiệu, nhà phát hành có thể tùy chọn
bao gồm thời gian hết hạn cho mỗi người giới thiệu.


## Đặc tả

```
iexp{X}={nnnnnnnnnn}

X :: Số của người giới thiệu (0-2)

nnnnnnnnnn :: Thời gian tính bằng giây (không phải ms) kể từ kỷ nguyên.
```

### Ghi chú
* Mỗi thời gian hết hạn phải lớn hơn ngày công bố của RouterInfo,
  và nhỏ hơn 6 giờ sau ngày công bố của RouterInfo.

* Các router phát hành và người giới thiệu nên cố gắng giữ cho người giới thiệu còn hợp lệ
  cho đến khi hết hạn, tuy nhiên không có cách nào để đảm bảo điều này.

* Các router không nên sử dụng một người giới thiệu sau khi hết hạn.

* Thời gian hết hạn của người giới thiệu nằm trong ánh xạ RouterAddress.
  Chúng không phải là trường hết hạn (hiện không được sử dụng) 8-byte trong RouterAddress.

**Ví dụ:** `iexp0=1486309470`


## Di cư

Không có vấn đề. Việc triển khai là tùy chọn.
Tương thích ngược được đảm bảo, vì các router cũ sẽ bỏ qua các tham số không xác định.
