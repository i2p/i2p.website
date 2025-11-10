---
title: "Ghi chú trạng thái I2P ngày 2005-08-23"
date: 2005-08-23
author: "jr"
description: "Cập nhật hàng tuần bao gồm các cải tiến trong bản phát hành 0.6.0.3, tình trạng mạng Irc2P, giao diện web susibt cho i2p-bt, và viết blog an toàn với Syndie"
categories: ["status"]
---

Chào mọi người, lại đến lúc cho ghi chú trạng thái hàng tuần rồi.

* Index

1) Trạng thái 0.6.0.3 2) Trạng thái IRC 3) susibt 4) Syndie 5) ???

* 1) 0.6.0.3 status

As mentioned the other day [1], we've got a new 0.6.0.3 release out there, ready for your enjoyment. Its a big improvement from the 0.6.0.2 release (its not uncommon to get several days without disconnect on irc - I've had 5 day uptimes broken by an upgrade), but there are a few things worth noting. Still, its not always like that - people with slow net connections run into troubles, but its progress.

Có một câu hỏi (rất) thường gặp liên quan đến mã kiểm tra peer (nút ngang hàng)-"Tại sao nó hiển thị Status: Unknown?" Unknown là *hoàn toàn ổn* - điều đó KHÔNG phải là dấu hiệu của một vấn đề. Ngoài ra, nếu bạn thấy đôi khi nó chuyển qua lại giữa "OK" và "ERR-Reject", điều đó KHÔNG có nghĩa là mọi thứ ổn - nếu bạn từng thấy ERR-Reject, điều đó có nghĩa là rất có thể bạn đang gặp sự cố NAT hoặc tường lửa. Tôi biết điều đó gây bối rối, và sẽ có một bản phát hành sau này với hiển thị trạng thái rõ ràng hơn (và tự động khắc phục khi có thể), nhưng hiện tại, đừng ngạc nhiên nếu tôi phớt lờ bạn khi bạn nói "trời ơi, nó hỏng rồi!!!11 trạng thái là Unknown!" ;)

(Nguyên nhân của việc có quá nhiều giá trị trạng thái Unknown là vì chúng tôi đang bỏ qua các kiểm tra peer trong đó "Charlie" [2] là một nút mà chúng tôi đã có sẵn phiên SSU, vì điều đó ngụ ý rằng họ vẫn có thể vượt qua NAT của chúng tôi ngay cả khi NAT của chúng tôi bị lỗi)

[1] http://dev.i2p.net/pipermail/i2p/2005-August/000844.html [2] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/udp.html?rev=HEAD#peerTesting

* 2) IRC status

Như đã đề cập ở trên, những người vận hành Irc2P đã làm rất tốt với mạng của họ, vì độ trễ giảm mạnh và độ tin cậy tăng cao - tôi đã không thấy netsplit (sự phân tách mạng) trong nhiều ngày. Cũng có một máy chủ IRC mới ở đó, nâng tổng số lên 3 - irc.postman.i2p, irc.arcturus.i2p, và irc.freshcoffee.i2p. Có lẽ một trong những người của Irc2P có thể cung cấp cho chúng ta một bản cập nhật về tiến độ của họ trong cuộc họp?

* 3) susibt

susi23 (nổi tiếng với susimail) đã trở lại với một cặp công cụ liên quan đến bt - susibt [3] và một tracker bot (bot theo dõi) mới [4]. susibt là một ứng dụng web (có thể triển khai một cách cực kỳ đơn giản trong i2p jetty instance của bạn) để quản lý hoạt động của i2p-bt. Như trang web của cô ấy cho biết:

SusiBT là một web frontend (giao diện web) cho i2p-bt. Nó tích hợp vào i2p router của bạn và cho phép tải lên và tải xuống tự động, tiếp tục sau khi khởi động lại, cùng một số chức năng quản lý như tải lên và tải xuống tệp. Các phiên bản sau của ứng dụng sẽ hỗ trợ tự động tạo và tải lên các tệp torrent.

[3] http://susi.i2p/?page_id=31 [4] http://susi.i2p/?p=33

Cho tôi nghe một tiếng "w00t" nào?

* 4) Syndie

Như đã đề cập trên danh sách thư và trong kênh, chúng tôi có một ứng dụng khách mới dành cho viết blog/phân phối nội dung an toàn và có xác thực. Với Syndie, câu hỏi "is your eepsite(I2P Site) up" không còn nữa, vì bạn vẫn có thể đọc nội dung ngay cả khi site đó ngừng hoạt động, và Syndie tránh được mọi vấn đề rắc rối vốn có của các mạng phân phối nội dung bằng cách tập trung vào phần giao diện (frontend). Dù sao thì, nó vẫn đang trong quá trình hoàn thiện, nhưng nếu mọi người muốn tham gia và dùng thử, hiện có một nút Syndie công cộng tại http://syndiemedia.i2p/ (cũng có thể truy cập trên web tại http://66.111.51.110:8000/). Cứ thoải mái vào đó và tạo một blog, hoặc nếu bạn cảm thấy mạo hiểm, hãy viết vài bình luận/đề xuất/quan ngại lên blog! Dĩ nhiên, rất hoan nghênh các bản vá, và cả các đề xuất tính năng nữa, nên cứ mạnh dạn.

* 5) ???

Nói rằng có nhiều thứ đang diễn ra thì có lẽ vẫn còn là nói giảm... ngoài những điều ở trên, tôi đang mày mò cải tiến điều khiển tắc nghẽn của SSU (-1 đã có trong cvs rồi), bộ giới hạn băng thông của chúng ta, và netDb (để xử lý việc thỉnh thoảng một số site không truy cập được), cũng như gỡ lỗi vấn đề CPU được báo cáo trên diễn đàn. Tôi chắc những người khác cũng đang mày mò vài thứ hay ho để báo cáo, nên hy vọng họ sẽ tạt qua buổi họp tối nay để thoải mái chia sẻ :)

Dù sao thì, hẹn gặp mọi người tối nay lúc 20:00 GMT trên kênh #i2p ở các máy chủ quen thuộc!

=jr
