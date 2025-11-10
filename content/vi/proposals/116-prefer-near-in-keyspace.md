---
title: "Ưu Tiên Router Gần Nhau Trong Không Gian Khóa"
number: "116"
author: "chisquare"
created: "2015-04-25"
lastupdated: "2015-04-25"
status: "Cần Nghiên Cứu"
thread: "http://zzz.i2p/topics/1874"
---

## Tổng Quan

Đây là đề xuất để tổ chức các peer sao cho chúng ưu tiên kết nối với các 
peer khác gần chúng trong không gian khóa.


## Động Lực

Ý tưởng là cải thiện thành công trong việc xây dựng đường hầm, bằng cách tăng
xác suất rằng một router đã được kết nối với một router khác.


## Thiết Kế

### Thay Đổi Cần Thiết

Sự thay đổi này sẽ yêu cầu:

1. Mỗi router ưu tiên các kết nối gần chúng trong không gian khóa.
2. Mỗi router phải nhận thức rằng mỗi router ưu tiên các kết nối gần chúng trong
   không gian khóa.


### Ưu Điểm cho Việc Xây Dựng Đường Hầm

Nếu bạn xây dựng một đường hầm::

    A -dài-> B -ngắn-> C -ngắn-> D

(dài/ngẫu nhiên so với nhanh trong không gian khóa), bạn có thể đoán nơi mà việc 
xây dựng đường hầm có thể thất bại và thử một peer khác tại điểm đó. Thêm vào đó, 
nó có thể cho phép bạn phát hiện các phần dày đặc hơn trong không gian khóa và 
cho các router không sử dụng chúng vì có thể đó là ai đó đang thông đồng.

Nếu bạn xây dựng một đường hầm::

    A -dài-> B -dài-> C -ngắn-> D

và nó thất bại, bạn có thể suy ra rằng có nhiều khả năng nó đã thất bại tại C -> D
và bạn có thể chọn một bước D khác.

Bạn cũng có thể xây dựng các đường hầm sao cho OBEP gần hơn với IBGW và sử dụng các
đường hầm đó với OBEP mà gần hơn với IBGW trong một LeaseSet đã cho.


## Ý Nghĩa Bảo Mật

Nếu bạn ngẫu nhiên hoá vị trí của các bước ngắn so với các bước dài trong không gian khóa, kẻ tấn công có thể sẽ không có nhiều lợi thế.

Điểm trừ lớn nhất là nó có thể khiến việc liệt kê người dùng dễ dàng hơn chút.
