---
title: "Ghi chú trạng thái I2P cho 2005-08-16"
date: 2005-08-16
author: "jr"
description: "Bản cập nhật ngắn gọn bao gồm trạng thái PeerTest, quá trình chuyển đổi mạng Irc2P, tiến độ GUI của Feedspace, và thay đổi thời gian họp thành 8PM GMT"
categories: ["status"]
---

Chào mọi người, hôm nay chỉ có vài ghi chú ngắn

* Index:

1) Trạng thái PeerTest 2) Irc2P 3) Feedspace 4) meta 5) ???

* 1) PeerTest status

Như đã đề cập trước đó, bản phát hành 0.6.1 sắp tới sẽ bao gồm một chuỗi kiểm thử nhằm cấu hình router cẩn thận hơn và xác minh khả năng tiếp cận (hoặc chỉ ra những gì cần thực hiện), và dù chúng tôi đã có một số mã trong CVS qua hai bản build rồi, vẫn còn vài tinh chỉnh trước khi nó hoạt động trơn tru như cần thiết. Hiện tại, tôi đang thực hiện một vài điều chỉnh nhỏ đối với luồng kiểm thử được mô tả ở [1] bằng cách thêm một gói tin bổ sung để xác minh khả năng tiếp cận của Charlie và trì hoãn phản hồi của Bob cho Alice cho đến khi Charlie đã phản hồi. Điều này sẽ giảm số lượng giá trị trạng thái "ERR-Reject" không cần thiết mà mọi người thấy, vì Bob sẽ không trả lời Alice cho đến khi anh ấy có một Charlie sẵn sàng cho việc kiểm thử (và khi Bob không trả lời, Alice thấy "Unknown" là trạng thái).

[1] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/udp.html#peerTesting

Dù sao thì, ừ, thế là vậy - nhiều khả năng sẽ có bản 0.6.0.2-3 ra vào ngày mai, được phát hành chính thức khi đã được kiểm thử kỹ lưỡng.

* 2) Irc2P

Như đã đề cập trên diễn đàn [2], những người dùng I2P sử dụng IRC cần cập nhật cấu hình để chuyển sang mạng IRC mới. Duck sẽ tạm thời ngừng hoạt động để [redacted], và thay vì trông chờ máy chủ không gặp trục trặc trong thời gian đó, postman và smeghead đã chủ động xây dựng một mạng IRC mới để bạn sử dụng. Postman cũng đã tạo bản mirror (bản sao phản chiếu) cho tracker của duck và trang i2p-bt tại [3], và tôi nghĩ tôi đã thấy trên mạng IRC mới về việc susi khởi chạy một phiên bản IdleRPG mới (xem danh sách kênh để biết thêm thông tin).

Tôi xin gửi lời cảm ơn tới những người phụ trách mạng i2pirc cũ (duck, baffled, nhóm metropipe, postman) và những người phụ trách mạng irc2p mới (postman, arcturus)! Những dịch vụ và nội dung thú vị khiến I2P trở nên đáng giá, và chính các bạn sẽ tạo ra chúng!

[2] http://forum.i2p.net/viewtopic.php?t=898 [3] http://hq.postman.i2p/

* 3) Feedspace

Nhân tiện, hôm trước tôi có đọc blog của frosk và có vẻ như Feedspace đã có thêm tiến triển - cụ thể là về một GUI (giao diện đồ họa) nhỏ xinh. Tôi biết có thể vẫn chưa sẵn sàng để thử nghiệm, nhưng tôi chắc là frosk sẽ chia sẻ ít mã nguồn cho chúng ta khi đến lúc. Nhân tiện nói thêm, tôi cũng nghe đồn về một công cụ viết blog trên web chú trọng ẩn danh khác đang được phát triển, công cụ này sẽ có thể tích hợp với Feedspace khi sẵn sàng, nhưng tôi cũng chắc rằng khi đến lúc chúng ta sẽ nghe thêm thông tin về việc đó.

* 4) meta

Vì tôi đúng là một thằng tham lam, tôi muốn dời các buổi họp lên sớm một chút - thay vì 9 giờ tối GMT, hãy thử 8 giờ tối GMT. Tại sao? Vì như vậy hợp lịch của tôi hơn ;) (mấy quán net gần nhất không mở cửa quá khuya).

* 5) ???

Chừng đó là đủ cho lúc này - tôi sẽ cố gắng ở gần một quán net cho buổi họp tối nay, vì vậy cứ thoải mái ghé qua #i2p lúc *8*P GMT trên các máy chủ irc /new/ {irc.postman.i2p, irc.arcturus.i2p}. Chúng ta có thể sẽ có một changate bot kết nối lên irc.freenode.net - có ai muốn chạy một con không?

Tạm biệt, =jr
