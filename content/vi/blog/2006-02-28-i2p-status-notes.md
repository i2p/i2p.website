---
title: "Ghi chú trạng thái I2P ngày 2006-02-28"
date: 2006-02-28
author: "jr"
description: "Các cải tiến về mạng trong 0.6.1.12, lộ trình tới 0.6.2 với các chiến lược lựa chọn peer (nút ngang hàng) mới, và cơ hội cho các dự án nhỏ"
categories: ["status"]
---

Này mọi người, lại đến giờ buổi than thở thứ Ba của chúng ta rồi.

* Index

1) Trạng thái mạng và 0.6.1.12 2) Lộ trình tới 0.6.2 3) Các dự án nhỏ 4) ???

* 1) Net status and 0.6.1.12

Tuần qua đã chứng kiến những cải thiện đáng kể trên toàn mạng, trước hết là việc triển khai rộng rãi 0.6.1.11 vào thứ Ba tuần trước, tiếp theo là bản phát hành 0.6.1.12 vào thứ Hai vừa qua (hiện đã được đẩy tới 70% toàn mạng - cảm ơn!). Nhìn chung, mọi thứ đã cải thiện nhiều so với cả 0.6.1.10 và các bản trước đó — tỷ lệ thiết lập tunnel thành công cao hơn hẳn một bậc độ lớn mà không cần các tunnel dự phòng đó, độ trễ giảm, mức sử dụng CPU giảm, và thông lượng tăng. Ngoài ra, với TCP được vô hiệu hóa hoàn toàn, tỷ lệ truyền lại gói tin vẫn nằm trong tầm kiểm soát.

* 2) Road to 0.6.2

Vẫn còn một số điểm cần cải thiện trong mã lựa chọn peer (nút ngang hàng), vì chúng tôi vẫn thấy tỷ lệ từ chối tunnel phía client ở mức 10-20%, và các tunnels có thông lượng cao (10+KBps) chưa phổ biến như kỳ vọng. Ngược lại, nay khi tải CPU đã giảm đáng kể, tôi có thể chạy thêm một router trên dev.i2p.net mà không gây vấn đề cho router chính của tôi (router này phục vụ squid.i2p, www.i2p, cvs.i2p, syndiemedia.i2p và các dịch vụ khác, đạt 2-300+KBps).

Ngoài ra, tôi đang thử một số cải tiến cho những người dùng trên các mạng bị tắc nghẽn nặng (gì cơ, ý bạn là vẫn có người không bị như vậy ư?). Có vẻ đã có một số tiến triển về mặt này, nhưng sẽ cần thử nghiệm thêm. Hy vọng điều này sẽ giúp được 4 hay 5 người trên irc2p dường như gặp khó khăn trong việc duy trì kết nối ổn định (và dĩ nhiên cũng giúp những người âm thầm chịu đựng tình trạng tương tự).

Sau khi điều đó hoạt động tốt, chúng ta vẫn còn một số việc phải làm trước khi có thể gọi nó là 0.6.2 - chúng ta cần các chiến lược sắp xếp peer (nút) mới, bên cạnh những chiến lược chọn peer đã được cải thiện này.  Ở mức cơ bản, tôi muốn có ba chiến lược mới - 
= sắp xếp nghiêm ngặt (giới hạn peer liền trước và liền sau của mỗi peer,   với cơ chế xoay vòng theo MTBF)
= cố định hai đầu (sử dụng một peer cố định làm cổng vào và   điểm cuối ra)
= láng giềng giới hạn (sử dụng một tập peer giới hạn làm bước nhảy từ xa   đầu tiên)

Còn có những chiến lược thú vị khác cần được xử lý, nhưng ba chiến lược đó là quan trọng nhất. Khi chúng đã được triển khai, chúng ta sẽ hoàn tất về mặt chức năng cho 0.6.2. ETA (thời gian ước tính) mơ hồ vào tháng 3/tháng 4.

* 3) Miniprojects

Có nhiều việc hữu ích để làm đến mức tôi đếm không xuể, nhưng tôi chỉ muốn giới thiệu với bạn một bài viết trên blog của tôi mô tả năm dự án nhỏ mà một lập trình viên có thể làm nhanh mà không cần đầu tư quá nhiều thời gian [1]. Nếu ai đó hứng thú bắt tay vào những việc đó, tôi chắc rằng chúng tôi sẽ phân bổ một ít nguồn lực [2] từ quỹ chung như lời cảm ơn, dù tôi hiểu rằng đa số các bạn được thúc đẩy bởi niềm đam mê hack chứ không phải vì tiền ;)

[1] http://syndiemedia.i2p.net:8000/blog.jsp?     blog=ovpBy2mpO1CQ7deYhQ1cDGAwI6pQzLbWOm1Sdd0W06c=&     entry=ovpBy2mpO1CQ7deYhQ1cDGAwI6pQzLbWOm1Sdd0W06c=/1140652800002 [2] http://www.i2p.net/halloffame

* 4) ???

Dù sao thì, đó là bản tóm tắt nhanh về những gì đang diễn ra theo như tôi biết. Chúc mừng cervantes nữa nhé nhân dịp diễn đàn đạt người dùng thứ 500, tiện thể :) Như mọi khi, ghé qua #i2p để tham gia cuộc họp trong vài phút nữa!

=jr
