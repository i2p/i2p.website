---
title: "Ghi chú trạng thái I2P cho ngày 2005-02-15"
date: 2005-02-15
author: "jr"
description: "Ghi chú tình hình phát triển I2P hằng tuần bao gồm sự tăng trưởng của mạng lên 211 routers, công tác chuẩn bị cho bản phát hành 0.5, và i2p-bt 0.1.7"
categories: ["status"]
---

Xin chào, lại đến thời điểm đó trong tuần rồi,

* Index

1) Trạng thái mạng 2) Trạng thái 0.5 3) i2p-bt 0.1.7 4) ???

* 1) Net status

Mặc dù không có lỗi mới nào xuất hiện trên mạng, tuần trước chúng tôi được nhắc đến trên một trang web P2P của Pháp khá nổi tiếng, điều này đã dẫn đến sự gia tăng cả về số lượng người dùng lẫn hoạt động bittorrent. Ở đỉnh điểm, chúng tôi đạt 211 routers trên mạng, mặc dù gần đây con số này dao động trong khoảng 150 đến 180. Mức sử dụng băng thông được báo cáo cũng tăng, tuy nhiên đáng tiếc là độ tin cậy của IRC đã giảm, khi một trong các máy chủ đã hạ giới hạn băng thông của họ do tải. Đã có một loạt cải tiến cho streaming lib (thư viện truyền phát) để giúp khắc phục điều này, nhưng chúng nằm trên nhánh 0.5-pre, nên chưa có sẵn trên mạng đang hoạt động.

Một sự cố tạm thời khác là việc một trong các HTTP outproxies (proxy chuyển tiếp ra Internet) bị ngừng hoạt động (www1.squid.i2p), khiến 50% yêu cầu tới outproxy thất bại. Bạn có thể tạm thời loại bỏ outproxy đó bằng cách mở cấu hình I2PTunnel [1], chỉnh sửa eepProxy và thay đổi dòng "Outproxies:" để chỉ chứa "squid.i2p". Hy vọng chúng tôi sẽ sớm đưa outproxy còn lại hoạt động trở lại để tăng tính dự phòng.

[1] http://localhost:7657/i2ptunnel/index.jsp

* 2) 0.5 status

Tuần vừa rồi đã có rất nhiều tiến triển đối với 0.5 (tôi cá là bạn nghe câu đó cũng phát chán rồi, nhỉ?). Nhờ sự giúp đỡ của postman, cervantes, duck, spaetz và một người không nêu tên, chúng tôi đã vận hành một mạng thử nghiệm với mã mới gần một tuần và đã xử lý khá nhiều lỗi mà trước đây tôi chưa thấy trong mạng thử nghiệm cục bộ của mình.

Trong khoảng một ngày trở lại đây, các thay đổi đều nhỏ, và tôi không thấy còn phần mã đáng kể nào trước khi bản phát hành 0.5 được tung ra. Vẫn còn một chút dọn dẹp, viết tài liệu và đóng gói, và cũng không hại gì khi để mạng thử nghiệm 0.5 tiếp tục chạy phòng khi các lỗi bổ sung lộ ra theo thời gian.  Vì đây sẽ là một BẢN PHÁT HÀNH KHÔNG TƯƠNG THÍCH NGƯỢC, để bạn có thời gian lên kế hoạch cập nhật, tôi sẽ ấn định một hạn chót đơn giản là THỨ SÁU NÀY cho thời điểm phát hành 0.5.

Như bla đã đề cập trên irc, những người vận hành eepsite(I2P Site) có thể muốn tạm ngừng trang của họ vào thứ Năm hoặc thứ Sáu và giữ chúng ngừng hoạt động cho đến thứ Bảy khi nhiều người dùng đã nâng cấp. Điều này sẽ giúp giảm tác động của một cuộc tấn công giao cắt (ví dụ: nếu 90% mạng đã chuyển sang 0.5 còn bạn vẫn ở 0.4, nếu ai đó truy cập đến eepsite(I2P Site) của bạn, họ sẽ biết bạn là một trong 10% các router còn lại trên mạng).

Tôi có thể bắt đầu đi sâu vào những gì đã được cập nhật trong bản 0.5, nhưng rồi tôi sẽ nói dài hàng trang liền, nên có lẽ tôi sẽ tạm hoãn và đưa điều đó vào tài liệu mà tôi nên soạn :)

* 3) i2p-bt 0.1.7

duck đã đưa ra một bản phát hành sửa lỗi cho bản cập nhật 0.1.6 của tuần trước, và nghe đồn là nó rất xịn (có lẽ còn /quá/ xịn, do mức sử dụng mạng tăng lên ;)  Thêm thông tin @ diễn đàn i2p-bt [2]

[2] http://forum.i2p.net/viewtopic.php?t=300

* 4) ???

Còn rất nhiều điều khác đang diễn ra trong các cuộc thảo luận trên IRC và trên diễn đàn [3], quá nhiều để tóm tắt ngắn gọn. Có lẽ những người quan tâm có thể ghé qua cuộc họp và cung cấp cho chúng tôi các cập nhật và ý kiến? Dù sao thì, hẹn gặp mọi người sớm nhé

=jr
