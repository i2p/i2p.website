---
title: "Meta-LeaseSet cho Multihoming"
number: "120"
author: "zzz"
created: "2016-01-09"
lastupdated: "2016-01-11"
status: "Rejected"
thread: "http://zzz.i2p/topics/2045"
supercededby: "123"
---

## Tổng quan

Đề xuất này là về việc triển khai hỗ trợ multihoming đúng cách trong I2P có thể
mở rộng đến các trang web lớn.


## Động lực

Multihoming là một giải pháp tạm thời và có thể sẽ không hoạt động đối với vd. facebook.i2p ở quy mô lớn.
Giả sử chúng ta có 100 multihome, mỗi cái có 16 đường hầm, đó là 1600 LS đăng tải mỗi
10 phút, hay gần 3 lần mỗi giây. Các floodfill sẽ bị quá tải và các giới hạn sẽ có hiệu lực.
Và đó là trước khi chúng ta đề cập đến lưu lượng tìm kiếm.

Chúng ta cần một loại meta-LS nào đó, nơi LS liệt kê các hàm băm của 100 LS thực tế.
Điều này sẽ tồn tại lâu dài, lâu hơn 10 phút rất nhiều. Vì vậy, đây là tìm kiếm hai giai đoạn cho LS, nhưng giai đoạn đầu tiên có thể được lưu trong bộ nhớ đệm trong hàng giờ.


## Đặc tả

Meta-LeaseSet sẽ có định dạng sau::

  - Đích
  - Dấu thời gian đã xuất bản
  - Hết hạn
  - Cờ
  - Thuộc tính
  - Số lượng mục
  - Số lượng thu hồi

  - Các mục. Mỗi mục chứa:
    - Hàm băm
    - Cờ
    - Hết hạn
    - Chi phí (ưu tiên)
    - Thuộc tính

  - Thu hồi. Mỗi thu hồi chứa:
    - Hàm băm
    - Cờ
    - Hết hạn

  - Chữ ký

Cờ và thuộc tính được bao gồm để tối đa hóa tính linh hoạt.


## Bình luận

Sau đó, điều này có thể được tổng quát hóa thành một tra cứu dịch vụ của bất kỳ loại nào. 
Bộ định danh dịch vụ là một hàm băm SHA256.

Để có khả năng mở rộng lớn hơn nữa, chúng ta có thể có nhiều cấp độ, tức là một meta-LS
có thể chỉ đến các meta-LS khác.
