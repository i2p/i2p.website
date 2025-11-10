---
title: "Ghi chú trạng thái I2P cho ngày 2005-09-06"
date: 2005-09-06
author: "jr"
description: "Bản cập nhật hàng tuần bao gồm thành công của bản phát hành 0.6.0.5, hiệu năng floodfill netDb, tiến độ của Syndie với RSS và pet names (tên thân thuộc), và ứng dụng quản lý sổ địa chỉ susidns mới"
categories: ["status"]
---

Chào mọi người,

* Index

1) Trạng thái mạng 2) Trạng thái Syndie 3) susidns 4) ???

* 1) Net status

Như nhiều người đã thấy, bản phát hành 0.6.0.5 đã ra mắt vào tuần trước sau một bản rev 0.6.0.4 ngắn, và cho đến nay, độ tin cậy đã được cải thiện đáng kể, và mạng lưới đã lớn hơn bao giờ hết. Vẫn còn một số chỗ để cải thiện, nhưng có vẻ như netDb mới đang hoạt động đúng như thiết kế. Chúng tôi thậm chí đã kiểm thử cơ chế dự phòng - khi các peer floodfill không thể truy cập được, các router chuyển sang kademlia netDb, và vài ngày trước, khi kịch bản đó xảy ra, độ tin cậy của irc và eepsite(I2P Site) không bị suy giảm đáng kể.

Tôi đã nhận được một câu hỏi về cách netDb mới hoạt động và đã đăng câu trả lời [1] lên blog của tôi [2]. Như mọi khi, nếu ai có bất kỳ câu hỏi nào về những vấn đề kiểu đó, xin cứ thoải mái gửi cho tôi, dù là trên hoặc ngoài danh sách thư, trên diễn đàn, hoặc thậm chí trên blog của bạn ;)

[1] http://syndiemedia.i2p.net/index.jsp?blog=ovpBy2mpO1CQ7deYhQ1cDGAwI6pQzLbWOm1Sdd0W06c=&entry=1125792000000&expand=true [2] http://syndiemedia.i2p.net/index.jsp?blog=ovpBy2mpO1CQ7deYhQ1cDGAwI6pQzLbWOm1Sdd0W06c=

* 2) Syndie status

Như bạn có thể thấy từ syndiemedia.i2p (và http://syndiemedia.i2p.net/), gần đây đã có rất nhiều tiến triển, bao gồm RSS, pet names (tên thân thuộc do người dùng đặt), các điều khiển quản trị, và những khởi đầu cho việc sử dụng css hợp lý. Phần lớn các đề xuất của Isamoor đã được triển khai, các đề xuất của Adam cũng vậy, vì vậy nếu ai có ý tưởng hay mong muốn gì muốn thấy ở đó, hãy nhắn cho tôi biết nhé!

Syndie hiện đã khá gần tới giai đoạn beta, và khi đó nó sẽ được phát hành kèm như một trong các ứng dụng I2P mặc định cũng như được đóng gói độc lập, vì vậy mọi sự hỗ trợ đều rất được trân trọng. Với những bổ sung mới nhất hôm nay (trong cvs), việc skinning (tùy biến giao diện) cho Syndie cũng trở nên rất dễ dàng — bạn chỉ cần tạo một tệp mới syndie_standard.css trong thư mục i2p/docs/ của bạn, và các style được chỉ định sẽ ghi đè các mặc định của Syndie. Thông tin chi tiết hơn về việc này có thể tìm thấy trên blog của tôi [2].

* 3) susidns

Susi lại vừa tạo ra một ứng dụng web nữa cho chúng ta - susidns [3]. Nó đóng vai trò như một giao diện đơn giản để quản lý ứng dụng addressbook (sổ địa chỉ) - các mục nhập, đăng ký, v.v. của nó. Nó trông khá ổn, nên hy vọng chúng tôi sẽ sớm có thể phát hành nó như một trong các ứng dụng mặc định, nhưng hiện tại thì rất đơn giản: bạn chỉ cần tải nó từ eepsite(I2P Site) của cô ấy, lưu nó vào thư mục webapps của bạn, khởi động lại router, và thế là xong.

[3] http://susi.i2p/?page_id=13

* 4) ???

Trong khi chúng tôi chắc chắn đã tập trung vào phía ứng dụng khách (và sẽ tiếp tục như vậy), phần lớn thời gian của tôi vẫn dành cho hoạt động cốt lõi của mạng, và có một số thứ thú vị sắp ra mắt - vượt tường lửa và NAT bằng introductions (cơ chế giới thiệu), cải thiện khả năng tự cấu hình SSU, sắp xếp và lựa chọn peer (nút ngang hàng) nâng cao, và thậm chí cả một số xử lý tuyến hạn chế đơn giản. Về phía website, HalfEmpty đã có vài cải tiến cho các bảng định kiểu của chúng tôi (tuyệt!).

Dù sao thì, có rất nhiều việc đang diễn ra, nhưng hiện giờ tôi chỉ có thời gian để nói bấy nhiêu thôi; hãy ghé qua buổi họp lúc 8 giờ tối UTC và chào một tiếng nhé :)

=jr
