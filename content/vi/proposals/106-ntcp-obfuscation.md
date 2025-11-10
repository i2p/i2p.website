---
title: "Giấu thông tin NTCP"
number: "106"
author: "zzz"
created: "2010-11-23"
lastupdated: "2014-01-03"
status: "Bị Từ Chối"
thread: "http://zzz.i2p/topics/774"
supercededby: "111"
---

## Tổng quan

Đề xuất này là về việc cải tiến giao thức truyền tải NTCP để cải thiện khả năng chống lại 
việc nhận dạng tự động.

## Động lực

Dữ liệu NTCP được mã hóa sau thông điệp đầu tiên (và thông điệp đầu tiên xuất hiện 
dưới dạng dữ liệu ngẫu nhiên), do đó ngăn chặn việc nhận dạng giao thức thông qua "phân tích gói 
tin". Nó vẫn dễ bị tổn thương bởi việc nhận dạng giao thức thông qua "phân tích luồng". Đó là bởi vì 
bốn thông điệp đầu tiên (tức là quá trình bắt tay) có độ dài cố định (288, 304, 448 và 48 byte).

Bằng cách thêm lượng dữ liệu ngẫu nhiên vào từng thông điệp, chúng ta có thể làm cho việc nhận dạng 
trở nên khó khăn hơn nhiều.

## Sửa đổi NTCP

Điều này khá nặng nề nhưng nó ngăn chặn bất kỳ phát hiện nào bởi thiết bị DPI.

Dữ liệu sau sẽ được thêm vào cuối thông điệp 288 byte 1:

- Một khối mã hóa ElGamal dài 514 byte
- Đệm ngẫu nhiên

Khối ElG được mã hóa bằng khóa công khai của Bob. Khi giải mã thành 222 byte, 
nó chứa:
- 214 byte đệm ngẫu nhiên
- 4 byte dự trữ 0
- 2 byte độ dài đệm theo sau
- 2 byte phiên bản và cờ giao thức

Trong các thông điệp 2-4, hai byte cuối cùng của đệm giờ sẽ chỉ định độ dài 
 của nhiều đệm tiếp theo.

Lưu ý rằng khối ElG không có bảo mật chuyển tiếp hoàn hảo nhưng không có gì quan trọng trong đó.

Chúng ta có thể sửa đổi thư viện ElG của mình để nó sẽ mã hóa các kích cỡ dữ liệu nhỏ hơn nếu chúng ta 
nghĩ rằng 514 byte là quá nhiều? Mã hóa ElG cho mỗi cài đặt NTCP có quá nhiều không?

Hỗ trợ cho việc này sẽ được quảng cáo trong netdb RouterAddress với tùy chọn 
"version=2". Nếu chỉ có 288 byte được nhận trong Thông điệp 1, Alice được giả định là phiên bản 1 và 
không có đệm nào được gửi trong các thông điệp tiếp theo. Lưu ý rằng việc giao tiếp có thể 
bị chặn nếu một MITM phân mảnh IP thành 288 byte (rất ít khả năng theo như Brandon nói).
