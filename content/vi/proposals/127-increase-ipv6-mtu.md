---
title: "Tăng MTU IPv6"
number: "127"
author: "zzz"
created: "2016-08-23"
lastupdated: "2016-12-02"
status: "Closed"
thread: "http://zzz.i2p/topics/2181"
target: "0.9.28"
implementedin: "0.9.28"
---

## Tổng quan

Đề xuất này là tăng tối đa SSU IPv6 MTU từ 1472 lên 1488.
Đã được triển khai trong 0.9.28.


## Động lực

IPv4 MTU phải là bội số của 16, + 12. IPv6 MTU phải là bội số của 16.

Khi hỗ trợ IPv6 lần đầu tiên được thêm vào vài năm trước, chúng tôi đặt tối đa IPv6 MTU ở mức 1472, nhỏ hơn IPv4 MTU là 1484. Điều này nhằm giữ mọi thứ đơn giản và đảm bảo rằng IPv6 MTU nhỏ hơn IPv4 MTU hiện tại. Bây giờ hỗ trợ IPv6 đã ổn định, chúng ta nên có thể đặt IPv6 MTU cao hơn IPv4 MTU.

MTU giao diện điển hình là 1500, vì vậy chúng ta có thể tăng hợp lý IPv6 MTU thêm 16 lên 1488.


## Thiết kế

Thay đổi tối đa từ 1472 lên 1488.


## Đặc tả

Trong các phần "Router Address" và "MTU" của tổng quan SSU, thay đổi tối đa IPv6 MTU từ 1472 lên 1488.


## Di cư

Chúng tôi dự đoán rằng các bộ định tuyến sẽ đặt kết nối MTU là mức nhỏ nhất của MTU cục bộ và từ xa, như thường lệ. Không cần kiểm tra phiên bản.

Nếu chúng tôi xác định rằng cần kiểm tra phiên bản, chúng tôi sẽ đặt mức phiên bản tối thiểu là 0.9.28 cho thay đổi này.
