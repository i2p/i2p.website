---
title: "Ghi chú trạng thái I2P cho ngày 2005-01-04"
date: 2005-01-04
author: "jr"
description: "Ghi chú trạng thái hàng tuần đầu tiên của năm 2005, bao gồm tăng trưởng mạng lên tới 160 router, các tính năng của 0.4.2.6 và quá trình phát triển 0.5"
categories: ["status"]
---

Chào mọi người, đã đến lúc cho những ghi chú tình hình hàng tuần đầu tiên của chúng ta trong năm 2005

* Index

1) Trạng thái mạng 2) 0.4.2.6 3) 0.5 4) jabber @ chat.i2p 5) ???

* 1) Net status

Trong tuần vừa qua, tình hình trên mạng khá thú vị — vào đêm Giao thừa, có một số bình luận được đăng trên một trang web phổ biến nói về i2p-bt và chúng tôi ghi nhận một đợt tăng nhẹ người dùng mới. Hiện có khoảng 120–150 routers trên mạng, dù vài ngày trước con số đạt đỉnh 160. Tuy vậy, mạng vẫn trụ vững, với các peer (nút ngang hàng) có dung lượng cao gánh phần tải dư thừa mà không gây gián đoạn đáng kể cho các peer khác. Một số người dùng chạy không đặt giới hạn băng thông trên các kết nối rất nhanh báo cáo thông lượng 2–300KBps, trong khi những người có dung lượng thấp hơn chỉ đạt mức thấp thông thường 1–5KBps.

Tôi nhớ Connelly có nói rằng anh ấy đã thấy hơn 300 router khác nhau trong vòng vài ngày sau dịp năm mới, vì vậy đã có sự biến động đáng kể. Mặt khác, hiện chúng ta có 120-150 người dùng trực tuyến ổn định, khác với mức 80-90 trước đây, đây là một mức tăng hợp lý. Tuy vậy, chúng tôi *không* muốn nó tăng quá nhiều vào lúc này, vì vẫn còn những vấn đề triển khai đã biết cần phải xử lý. Cụ thể, cho đến khi ra bản 0.6 [1], chúng tôi sẽ muốn duy trì dưới 2-300 peer (nút ngang hàng) để giữ số lượng luồng ở mức hợp lý. Tuy nhiên, nếu ai đó muốn giúp triển khai cơ chế truyền tải UDP, chúng ta có thể đạt được điều đó nhanh hơn nhiều.

Trong tuần vừa qua, tôi đã theo dõi các thống kê do các tracker i2p-bt đưa ra và đã có hàng gigabyte dữ liệu từ các tệp lớn được truyền, với một số báo cáo cho thấy tốc độ 80–120 KB/giây. IRC gặp nhiều trục trặc hơn thường lệ kể từ khi những bình luận đó được đăng trên trang web đó, nhưng thời gian giữa các lần mất kết nối vẫn ở mức hàng giờ. (theo như tôi thấy, router mà irc.duck.i2p đang chạy trên đó đang hoạt động khá sát với giới hạn băng thông của nó, điều này có thể giải thích mọi chuyện)

[1] http://www.i2p.net/roadmap#0.6

* 2) 0.4.2.6

Đã có một số bản sửa lỗi và tính năng mới được thêm vào CVS kể từ bản phát hành 0.4.2.5 mà chúng tôi muốn sớm triển khai, bao gồm các bản sửa lỗi về độ tin cậy cho streaming lib (thư viện streaming), cải thiện khả năng chống chịu khi thay đổi địa chỉ IP, và việc đóng gói triển khai sổ địa chỉ của ragnarok.

Nếu bạn chưa từng nghe nói về addressbook (sổ địa chỉ) hoặc chưa từng dùng nó, thì nói ngắn gọn là nó sẽ tự động cập nhật tệp hosts.txt của bạn bằng cách định kỳ tải về và hợp nhất các thay đổi từ một số địa điểm được lưu trữ ẩn danh (mặc định là http://dev.i2p/i2p/hosts.txt và http://duck.i2p/hosts.txt). Bạn sẽ không cần phải thay đổi bất kỳ tệp nào, đụng đến bất kỳ cấu hình nào, hay chạy thêm ứng dụng nào khác - nó sẽ được triển khai bên trong I2P router dưới dạng một tệp .war chuẩn.

Đương nhiên, nếu bạn *thực sự* muốn đào sâu, vọc vạch với addressbook thì hoàn toàn hoan nghênh - xem trang của Ragnarok [2] để biết chi tiết. Những người đã triển khai addressbook trong router của mình sẽ cần làm một vài thao tác nhỏ trong quá trình nâng cấp lên 0.4.2.6, nhưng nó sẽ hoạt động với tất cả các thiết lập cấu hình cũ của bạn.

[2] http://ragnarok.i2p/

* 3) 0.5

Số liệu, số liệu, số liệu! Vâng, như tôi đã nói trước đây, bản phát hành 0.5 sẽ đại tu cách thức tunnel routing (định tuyến tunnel) hoạt động, và chúng tôi đang đạt được tiến triển ở mảng đó. Vài ngày qua tôi đã triển khai mã cho cơ chế mã hóa mới (kèm kiểm thử đơn vị), và khi chúng chạy ổn, tôi sẽ đăng một tài liệu mô tả những suy nghĩ hiện tại của tôi về cách thức, nội dung và lý do tunnel routing mới sẽ vận hành. Tôi triển khai phần mã hóa cho nó ngay bây giờ thay vì để sau để mọi người có thể xem xét ý nghĩa của nó một cách cụ thể, cũng như tìm ra những điểm còn vấn đề và đề xuất cải tiến. Tôi hy vọng mã sẽ chạy được vào cuối tuần, nên có thể sẽ có thêm tài liệu được đăng vào cuối tuần này. Tuy nhiên, không hứa trước.

* 4) jabber @ chat.i2p

jdot đã khởi chạy một máy chủ jabber mới, và có vẻ hoạt động khá tốt cho cả các cuộc trò chuyện một-một và trò chuyện nhóm. xem thông tin trên diễn đàn [3]. kênh thảo luận dev i2p vẫn sẽ là irc #i2p, nhưng có thêm lựa chọn thay thế thì luôn tốt.

[3] http://forum.i2p.net/viewtopic.php?t=229

* 5) ???

Ok, chừng đó là hầu như tất cả những gì tôi cần đề cập lúc này - tôi chắc là còn nhiều chuyện khác đang diễn ra mà những người khác muốn nêu ra, vậy nên ghé qua cuộc họp trong 15 phút nữa tại chỗ quen thuộc [4] và cho chúng tôi biết tình hình nhé!

=jr
