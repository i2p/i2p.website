---
title: "Ghi chú trạng thái I2P cho ngày 2005-03-08"
date: 2005-03-08
author: "jr"
description: "Ghi chú tiến độ phát triển I2P hàng tuần bao gồm các cải tiến trong bản phát hành 0.5.0.2, tập trung vào độ tin cậy mạng, và các cập nhật đối với dịch vụ thư điện tử và BitTorrent"
categories: ["status"]
---

Chào mọi người, đến giờ cập nhật hàng tuần rồi.

* Index

1) 0.5.0.2 2) cập nhật mail.i2p 3) cập nhật i2p-bt 4) ???

* 1) 0.5.0.2

Mới đây chúng tôi đã phát hành bản 0.5.0.2 và một phần lớn mạng lưới đã nâng cấp (yay!). Có báo cáo cho biết những lỗi tệ nhất ở 0.5.0.1 đã được loại bỏ, và nhìn chung mọi thứ có vẻ hoạt động ổn. Vẫn còn một số vấn đề về độ tin cậy, dù streaming lib (thư viện streaming) đã xử lý được chúng (các kết nối IRC kéo dài 12–24+ giờ dường như là điều bình thường). Tôi đang cố lần theo một vài vấn đề còn lại, nhưng sẽ thực sự, thực sự tốt nếu mọi người cập nhật lên phiên bản mới nhất càng sớm càng tốt.

Với hiện trạng và hướng đi sắp tới, độ tin cậy là ưu tiên số một. Chỉ sau khi đại đa số các thông điệp lẽ ra phải thành công thực sự thành công, chúng ta mới tập trung cải thiện thông lượng. Ngoài bộ tiền xử lý theo lô cho tunnel, một khía cạnh khác mà chúng ta có thể muốn khám phá là đưa thêm dữ liệu độ trễ vào các hồ sơ. Hiện tại, chúng ta chỉ dùng các thông điệp thử nghiệm và quản lý tunnel để xác định thứ hạng "tốc độ" của từng peer (nút), nhưng có lẽ chúng ta nên thu thập mọi RTT (thời gian khứ hồi) đo được cho các hoạt động khác, như netDb và thậm chí cả các thông điệp client đầu-cuối. Mặt khác, chúng ta sẽ phải gán trọng số phù hợp, vì với một thông điệp đầu-cuối, chúng ta không thể tách bốn thành phần của RTT đo được (outbound của chúng ta, inbound của họ, outbound của họ, inbound của chúng ta). Có lẽ chúng ta có thể dùng một số thủ thuật garlic để gói kèm một thông điệp nhắm tới một trong các tunnel inbound của chúng ta cùng với một số thông điệp outbound, loại bỏ các tunnel phía bên kia khỏi vòng đo lường.

* 2) mail.i2p updates

Ok, tôi không biết postman có những cập nhật gì dành sẵn cho chúng ta, nhưng sẽ có một bản cập nhật trong cuộc họp. Xem nhật ký để biết!

* 3) i2p-bt update

Tôi không biết duck & gang có cập nhật gì cho chúng ta, nhưng tôi có nghe vài lời bàn tán về tiến triển trên kênh. Có lẽ chúng ta có thể lấy được một bản cập nhật từ anh ấy.

* 4) ???

Có rất nhiều việc đang diễn ra, nhưng nếu có điều gì cụ thể mà mọi người muốn nêu ra và thảo luận, hãy ghé qua cuộc họp trong vài phút nữa. À, xin nhắc nhẹ, nếu mọi người vẫn chưa nâng cấp, vui lòng làm càng sớm càng tốt (việc nâng cấp cực kỳ đơn giản - tải một tệp, bấm một nút)

=jr
