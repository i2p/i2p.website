---
title: "PT Vận chuyển"
number: "109"
author: "zzz"
created: "2014-01-09"
lastupdated: "2014-09-28"
status: "Open"
thread: "http://zzz.i2p/topics/1551"
---

## Tổng quan

Đề xuất này là tạo ra một phương thức vận chuyển I2P kết nối đến các router khác thông qua Pluggable Transports.

## Động lực

Pluggable Transports (PTs) được phát triển bởi Tor như là một cách để thêm các phương tiện vận chuyển làm mờ kết nối cho các cầu Tor theo cách module hóa.

I2P hiện đã có hệ thống vận chuyển theo module giảm bớt rào cản khi thêm các phương tiện vận chuyển thay thế. Thêm hỗ trợ cho PTs sẽ cung cấp cho I2P một cách dễ dàng để thử nghiệm với các giao thức thay thế và chuẩn bị cho việc chống lại việc bị chặn.

## Thiết kế

Có một vài lớp triển khai tiềm năng:

1. Một PT chung thực hiện SOCKS và ExtORPort và cấu hình và phân nhánh các quy trình vào và ra, và đăng ký với hệ thống liên lạc. Lớp này không biết gì về NTCP và có thể hoặc không sử dụng NTCP. Thích hợp cho việc thử nghiệm.

2. Xây dựng trên 1), một PT NTCP chung dựa trên mã NTCP và hướng dẫn NTCP đến 1).

3. Xây dựng trên 2), một PT NTCP-xxxx cụ thể được cấu hình để chạy một quy trình vào và ra bên ngoài được chỉ định.
