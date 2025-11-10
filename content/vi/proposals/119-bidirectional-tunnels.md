---
title: "Đường Hầm Hai Chiều"
number: "119"
author: "orignal"
created: "2016-01-07"
lastupdated: "2016-01-07"
status: "Cần-Nghiên-Cứu"
thread: "http://zzz.i2p/topics/2041"
---

## Tổng quan

Đề xuất này là về việc triển khai các đường hầm hai chiều trong I2P.

## Động lực

i2pd sẽ giới thiệu đường hầm hai chiều chỉ xây dựng thông qua các bộ định tuyến i2pd khác hiện tại. Đối với mạng lưới, chúng sẽ xuất hiện như các đường hầm đi vào và đi ra thông thường.

## Thiết kế

### Mục tiêu

1. Giảm bớt sự sử dụng mạng và CPU bằng cách giảm số lượng thông điệp TunnelBuild
2. Khả năng biết ngay lập tức nếu một thành viên đã rời đi.
3. Hồ sơ và thống kê chính xác hơn
4. Sử dụng các darknet khác làm đối tượng trung gian

### Sửa đổi đường hầm

TunnelBuild
```````````
Các đường hầm được xây dựng theo cách giống như đường hầm đi vào. Không cần thông điệp phản hồi. Có một loại thành viên đặc biệt gọi là "entrance" được đánh dấu bằng cờ, phục vụ như IBGW và OBEP cùng một lúc. Thông điệp có định dạng giống như VaribaleTunnelBuild nhưng ClearText chứa các trường khác::

    in_tunnel_id
    out_tunnel_id
    in_next_tunnel_id
    out_next_tunnel_id
    in_next_ident
    out_next_ident
    layer_key, iv_key

Nó cũng sẽ chứa trường nhắc đến darknet mà đồng sự tiếp theo thuộc về và một số thông tin bổ sung nếu không phải là I2P.

TunnelTermination
`````````````````
Nếu đối tác muốn rời đi, nó tạo ra các thông điệp TunnelTermination mã hóa với khóa lớp và gửi theo hướng "in". Nếu một thành viên nhận được thông điệp như vậy, nó sẽ mã hóa lại với khóa lớp của nó và gửi đến đối tượng tiếp theo. Khi thông điệp đến chủ sở hữu đường hầm, nó sẽ bắt đầu giải mã từng đối tượng một cho đến khi nhận được thông điệp không mã hóa. Nó sẽ tìm ra đối tượng nào đã rời đi và chấm dứt đường hầm.
