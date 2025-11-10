---
title: "Ghi chú trạng thái I2P cho ngày 2005-08-02"
date: 2005-08-02
author: "jr"
description: "Bản cập nhật muộn đề cập đến trạng thái phát hành 0.6, hệ thống PeerTest, giới thiệu về SSU, các bản sửa lỗi cho giao diện web I2PTunnel, và mnet qua I2P"
categories: ["status"]
---

Chào mọi người, hôm nay ghi chú đến muộn,

* Index:

1) trạng thái phiên bản 0.6 2) PeerTest (kiểm thử ngang hàng) 3) cơ chế giới thiệu của SSU 4) giao diện web của I2PTunnel 5) mnet qua i2p 6) ???

* 1) 0.6 status

Như các bạn đều thấy, chúng tôi đã phát hành phiên bản 0.6 cách đây vài ngày, và nhìn chung mọi thứ diễn ra khá suôn sẻ. Một số cải tiến ở lớp truyền tải kể từ 0.5.* đã làm lộ ra các vấn đề trong phần triển khai netDb, nhưng các bản sửa cho phần lớn các vấn đề đó hiện đang được thử nghiệm (dưới dạng bản dựng 0.6-1) và sẽ sớm được triển khai dưới dạng 0.6.0.1. Chúng tôi cũng đã gặp một số vấn đề với các cấu hình NAT và tường lửa khác nhau, cũng như các vấn đề về MTU đối với một số người dùng - những vấn đề không xuất hiện trong mạng thử nghiệm nhỏ hơn do có ít người thử nghiệm. Các biện pháp tạm thời đã được bổ sung cho các tình huống gây ảnh hưởng nặng nhất, nhưng chúng tôi sắp có một giải pháp dài hạn - kiểm thử peer (nút ngang hàng).

* 2) PeerTest

Với 0.6.1, chúng tôi sẽ triển khai một hệ thống mới để kiểm tra và cấu hình một cách hợp tác các địa chỉ IP công khai và các cổng. Hệ thống này được tích hợp trong giao thức SSU lõi và sẽ tương thích ngược. Về cơ bản, nó cho phép Alice hỏi Bob địa chỉ IP công khai và số cổng của cô ấy là gì, và sau đó Bob lần lượt nhờ Charlie xác nhận cấu hình đúng của cô ấy, hoặc tìm ra giới hạn đang ngăn cản properation. Kỹ thuật này không có gì mới trên mạng, nhưng là một bổ sung mới cho cơ sở mã i2p và sẽ loại bỏ phần lớn các lỗi cấu hình phổ biến.

* 3) SSU introductions

Như đã mô tả trong đặc tả giao thức SSU, sẽ có chức năng cho phép những người dùng ở phía sau tường lửa và NAT (biên dịch địa chỉ mạng) tham gia đầy đủ vào mạng, ngay cả khi nếu không thì họ không thể nhận được các thông điệp UDP không được yêu cầu. Nó sẽ không hoạt động cho mọi tình huống có thể xảy ra, nhưng sẽ giải quyết được phần lớn. Có những điểm tương đồng giữa các thông điệp được mô tả trong đặc tả SSU và các thông điệp cần thiết cho PeerTest (kiểm tra ngang hàng), vì vậy có lẽ khi đặc tả được cập nhật với những thông điệp đó, chúng tôi sẽ có thể ghép kèm introductions (cơ chế giới thiệu) cùng với các thông điệp PeerTest. Dù sao đi nữa, chúng tôi sẽ triển khai các introductions này trong 0.6.2, và điều đó cũng sẽ tương thích ngược.

* 4) I2PTunnel web interface

Một số người đã nhận thấy và gửi báo cáo về nhiều trục trặc nhỏ trên giao diện web của I2PTunnel, và smeghead đã bắt đầu triển khai các bản sửa lỗi cần thiết - có lẽ anh ấy có thể giải thích chi tiết hơn về những cập nhật đó, cũng như ETA (thời gian dự kiến) cho chúng?

* 5) mnet over i2p

Mặc dù tôi không có mặt trên kênh khi các cuộc thảo luận diễn ra, nhưng qua việc đọc log (nhật ký) có vẻ như icepick đã hack để mnet chạy trên nền i2p - cho phép kho dữ liệu phân tán của mnet cung cấp khả năng xuất bản nội dung có tính chịu lỗi với hoạt động ẩn danh. Tôi không nắm rõ lắm về tiến độ ở mảng này, nhưng nghe có vẻ icepick đang đạt tiến triển tốt trong việc tích hợp với I2P thông qua SAM và twisted; có lẽ icepick có thể cung cấp thêm chi tiết?

* 6) ???

Được rồi, còn nhiều việc đang diễn ra hơn những gì ở trên, nhưng tôi đã trễ mất rồi nên có lẽ tôi nên dừng gõ và gửi tin nhắn này đi. Tối nay tôi có thể lên mạng một lúc, nên nếu ai có mặt, chúng ta có thể họp vào khoảng 9:30 tối hoặc tầm đó (khi nào bạn nhận được cái này ;) tại #i2p trên các máy chủ irc thông thường {irc.duck.i2p, irc.postman.i2p, irc.freenode.net, irc.metropipe.net}.

Cảm ơn bạn đã kiên nhẫn và hỗ trợ, giúp mọi việc tiến triển!

=jr
