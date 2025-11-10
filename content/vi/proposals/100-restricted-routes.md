---
title: "Các Tuyến Đường Hạn Chế"
number: "100"
author: "zzz"
created: "2008-09-14"
lastupdated: "2008-10-13"
status: "Reserve"
thread: "http://zzz.i2p/topics/114"
---

## Giới thiệu


## Suy nghĩ

- Thêm một phương thức truyền tải mới "IND" (gián tiếp) công bố một hàm băm leaseSet trong
  cấu trúc RouterAddress: "IND: [key=aababababababababb]". Phương thức truyền tải này đặt
  giá thầu ưu tiên thấp nhất khi router mục tiêu công bố nó. Để gửi cho một đối tác qua
  phương thức này, lấy leaseSet từ một đối tác ff như thường lệ, và gửi trực tiếp tới lease.

- Một đối tác quảng cáo IND phải xây dựng và duy trì một bộ đường hầm khác với một
  đối tác khác. Đây không phải là các đường hầm thăm dò và không phải đường hầm khách hàng,
  mà là một bộ đường hầm router thứ hai.

  - 1-hop có đủ không?
  - Làm thế nào để chọn đối tác cho các đường hầm này?
  - Chúng cần phải là "không bị hạn chế" nhưng làm thế nào để biết điều đó? Bản đồ tiếp cận?
    Lý thuyết đồ thị, thuật toán, cấu trúc dữ liệu có thể giúp ở đây. Cần đọc thêm về điều này.
    Xem các công việc cần làm của đường hầm.

- Nếu bạn có đường hầm IND thì phương thức truyền tải IND của bạn phải đấu giá (ưu tiên thấp)
  để gửi thông điệp qua các đường hầm này.

- Làm thế nào để quyết định kích hoạt việc xây dựng các đường hầm gián tiếp

- Làm thế nào để thực hiện và kiểm tra mà không làm mất sự che đậy
