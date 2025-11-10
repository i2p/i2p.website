---
title: "Ghi chú trạng thái I2P cho ngày 2005-01-11"
date: 2005-01-11
author: "jr"
description: "Ghi chú hàng tuần về trạng thái phát triển I2P, bao gồm tình trạng mạng, tiến độ 0.5, trạng thái 0.6, azneti2p, bản port cho FreeBSD, và hosts.txt như Web of Trust (mạng lưới tin cậy)"
categories: ["status"]
---

Chào mọi người, đến giờ cập nhật hàng tuần rồi.

* Index

1) Trạng thái mạng 2) Tiến độ 0.5 3) Trạng thái 0.6 4) azneti2p 5) fbsd 6) hosts.txt dưới dạng WoT 7) ???

* 1) Net status

Nhìn chung, mạng đang hoạt động tốt, dù chúng tôi đã gặp một số vấn đề khi một trong các máy chủ IRC bị ngoại tuyến và outproxy (proxy đi ra) của tôi gặp trục trặc. Tuy vậy, máy chủ IRC còn lại vẫn (và hiện vẫn) khả dụng (dù hiện tại chưa vô hiệu hóa CTCP - xem [1]), nên chúng tôi vẫn đáp ứng được nhu cầu IRC :)

[1] http://ugha.i2p/HowTo/IrcAnonymityGuide

* 2) 0.5 progress

Có tiến triển, cứ thế tiến lên! Được rồi, có lẽ tôi nên đi vào chi tiết hơn một chút. Cuối cùng tôi đã triển khai và kiểm thử xong cơ chế mật mã định tuyến mới cho tunnel (hoan hô!), nhưng trong một số cuộc thảo luận chúng tôi phát hiện một chỗ có thể gây rò rỉ một mức ẩn danh, nên nó đang được chỉnh sửa (first hop (bước nhảy đầu tiên) sẽ biết họ là first hop, điều này là Tệ, nhưng thực sự thực sự rất dễ khắc phục). Dù sao thì, tôi hy vọng sẽ sớm cập nhật và đăng tài liệu cùng mã nguồn về phần đó, và đăng tài liệu về phần còn lại của hoạt động tunnel 0.5 / pooling / v.v. sau đó. Sẽ có thêm tin khi có thêm tin.

* 3) 0.6 status

(cái gì!?)

Mule đã bắt đầu nghiên cứu về UDP transport (cơ chế truyền tải UDP), và chúng tôi đã tìm hiểu từ zab những kinh nghiệm với mã UDP của limewire. Tất cả đều rất hứa hẹn, nhưng còn rất nhiều việc phải làm (và trên lộ trình [2] thì vẫn còn vài tháng nữa). Có ý tưởng hoặc đề xuất nào không? Hãy tham gia và giúp tập trung nỗ lực vào những việc cần phải làm!

[2] http://www.i2p.net/roadmap#0.6

* 4) azneti2p

Tôi suýt ngã ngửa khi nhận được tin, nhưng có vẻ như những người bên Azureus đã viết một plugin I2P, cho phép vừa dùng tracker ẩn danh vừa giao tiếp dữ liệu ẩn danh! Nhiều torrent cũng có thể hoạt động trong một I2P destination (điểm đích I2P) duy nhất, và nó dùng trực tiếp I2PSocket, cho phép tích hợp chặt chẽ với thư viện streaming. Plugin azneti2p vẫn còn ở giai đoạn đầu với bản phát hành 0.1 này, và sẽ còn nhiều tối ưu hóa cùng các cải tiến về tính dễ sử dụng sắp tới, nhưng nếu bạn sẵn sàng xắn tay áo, hãy ghé qua i2p-bt trên các mạng IRC của I2P và tham gia cho vui :)

Dành cho những ai ưa khám phá, hãy tải Azureus phiên bản mới nhất [3], xem hướng dẫn I2P của họ [4], và tải plugin [5].

[3] http://azureus.sourceforge.net/index_CVS.php [4] http://azureus.sourceforge.net/doc/AnonBT/i2p/I2P_howto.htm [5] http://azureus.sourceforge.net/plugin_details.php?plugin=azneti2p

duck đã và đang thực hiện những nỗ lực phi thường để duy trì khả năng tương thích với i2p-bt, và ở #i2p-bt hiện đang có những màn hacking điên cuồng ngay lúc tôi đang gõ những dòng này, vì vậy hãy chú ý theo dõi bản phát hành i2p-bt mới sẽ ra mắt rất sớm thôi.

* 5) fbsd

Nhờ công sức của lioux, hiện đã có một mục trong FreeBSD Ports cho i2p [6].  Mặc dù chúng tôi không thực sự muốn có quá nhiều bản cài đặt đặc thù cho từng bản phân phối (distro) ngoài kia, anh ấy hứa sẽ giữ nó luôn được cập nhật khi chúng tôi thông báo trước đủ thời gian về các bản phát hành mới.  Điều này sẽ hữu ích cho những người dùng fbsd-current - Cảm ơn lioux!

[6] http://www.freshports.org/net/i2p/

* 6) hosts.txt as WoT

Giờ đây khi bản phát hành 0.4.2.6 đã đi kèm addressbook (sổ địa chỉ) của Ragnarok, việc giữ cho hosts.txt của bạn luôn có thêm các mục mới nằm trong tầm kiểm soát của từng người dùng.  Không chỉ vậy, bạn còn có thể xem các đăng ký addressbook như một dạng mạng lưới tin cậy giản lược - bạn nhập các mục mới từ một trang mà bạn tin cậy để giới thiệu cho bạn các destinations (đích đến) mới (mặc định là dev.i2p và duck.i2p).

Với khả năng này xuất hiện một chiều kích hoàn toàn mới - khả năng để mọi người lựa chọn những trang web nào họ sẽ về cơ bản liên kết trong hosts.txt của mình và những trang nào thì không. Trong khi mô hình công khai “ai cũng có thể tham gia” từng tồn tại trước đây vẫn có chỗ đứng, nay khi hệ thống đặt tên không chỉ còn trên lý thuyết mà trên thực tế đã phân tán hoàn toàn, mọi người sẽ cần tự xây dựng các chính sách của riêng mình về việc công bố Destination (điểm đích) của người khác.

Điều quan trọng đằng sau hậu trường ở đây là đây là một cơ hội học hỏi cho cộng đồng I2P. Trước đây, cả gott và tôi đều cố gắng thúc đẩy vấn đề đặt tên bằng cách công bố trang của gott dưới tên jrandom.i2p (anh ấy là người yêu cầu tên trang đó trước - tôi thì không, và tôi hoàn toàn không có quyền kiểm soát đối với nội dung tại URL đó). Giờ đây chúng ta có thể bắt đầu tìm hiểu cách chúng ta sẽ xử lý các trang không được liệt kê trong http://dev.i2p.net/i2p/hosts.txt hoặc trên forum.i2p. Việc không được đăng ở những nơi đó không hề ngăn cản một trang hoạt động - hosts.txt của bạn chỉ là sổ địa chỉ cục bộ của bạn.

Dù sao thì, nói lan man thế là đủ; tôi chỉ muốn lưu ý mọi người để tất cả chúng ta cùng thấy những gì cần phải làm.

* 7) ???

Ôi chà, nhiều thứ quá. Tuần này bận rộn, và tôi không nghĩ mọi thứ sẽ chậm lại trong thời gian tới. Vậy nên, ghé qua cuộc họp trong vài phút nữa để chúng ta trao đổi thêm.

=jr
