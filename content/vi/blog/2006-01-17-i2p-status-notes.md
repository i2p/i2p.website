---
title: "Ghi chú trạng thái I2P ngày 2006-01-17"
date: 2006-01-17
author: "jr"
description: "Trạng thái mạng với 0.6.1.9, các cải tiến về mật mã cho việc tạo tunnel, và các cập nhật giao diện blog của Syndie"
categories: ["status"]
---

Chào mọi người, lại là thứ Ba rồi

* Index

1) Trạng thái mạng và 0.6.1.9 2) Mật mã cho việc tạo Tunnel (đường hầm trong I2P) 3) Các blog Syndie 4) ???

* 1) Net status and 0.6.1.9

Với phiên bản 0.6.1.9 đã phát hành và 70% mạng lưới đã được nâng cấp, phần lớn các bản vá lỗi đi kèm có vẻ hoạt động như mong đợi, các báo cáo cho biết cơ chế lập hồ sơ tốc độ mới đang chọn ra được một số peer (nút ngang hàng) tốt. Tôi đã nghe về thông lượng duy trì trên các peer nhanh vượt 300KBps với mức sử dụng CPU 50-70%, trong khi các router khác ở mức 100-150KBps, giảm dần xuống những router chỉ đạt 1-5KBps. Tuy vậy vẫn còn biến động đáng kể về danh tính router, nên có vẻ bản vá mà tôi nghĩ sẽ giảm điều đó thì không (hoặc sự biến động là hợp lý).

* 2) Tunnel creation crypto

Vào mùa thu, đã có rất nhiều thảo luận về cách chúng ta xây dựng các tunnel, cùng với các đánh đổi giữa cách tạo tunnel kiểu Tor theo phương pháp telescopic (mở rộng dần theo từng bước) và cách tạo tunnel thăm dò kiểu I2P [1]. Trong quá trình đó, chúng tôi đã đưa ra một phương án kết hợp [2] loại bỏ các vấn đề của cách tạo tunnel theo phương pháp telescopic kiểu Tor [3], giữ được các lợi thế một chiều của I2P, và giảm bớt các lần thất bại không cần thiết. Do thời điểm đó có rất nhiều việc khác đang diễn ra, việc triển khai phương án kết hợp mới đã bị hoãn lại, nhưng hiện nay khi chúng ta đang tiến gần tới bản phát hành 0.6.2, trong đó dù sao chúng ta cũng cần đại tu mã tạo tunnel, thì đã đến lúc hoàn thiện việc này.

Tôi đã phác thảo một bản đặc tả nháp cho cơ chế mật mã mới cho tunnel và đăng nó lên blog Syndie của tôi hôm nọ, và sau một vài thay đổi nhỏ phát sinh khi triển khai thực tế, chúng tôi đã hoàn thiện một bản đặc tả trong CVS [4]. Trong CVS cũng đã có mã nguồn cơ bản hiện thực nó [5], tuy nhiên nó vẫn chưa được tích hợp vào quá trình xây dựng tunnel thực tế. Nếu ai rảnh, tôi rất mong nhận được phản hồi về bản đặc tả. Trong lúc đó, tôi sẽ tiếp tục làm việc trên mã xây dựng tunnel mới.

[1] http://dev.i2p.net/pipermail/i2p/2005-October/thread.html và     xem các chủ đề thảo luận liên quan đến các cuộc tấn công bootstrap (khởi tạo ban đầu) [2] http://dev.i2p.net/pipermail/i2p/2005-October/001064.html [3] http://dev.i2p.net/pipermail/i2p/2005-October/001057.html [4] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/                                tunnel-alt-creation.html?rev=HEAD [5] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/java/src/net/                        i2p/router/tunnel/BuildMessageTest.java

* 3) Syndie blogs

Như đã đề cập trước đó, bản phát hành 0.6.1.9 mới này có một số cải tổ đáng kể đối với giao diện blog của Syndie, bao gồm phong cách mới của cervantes và lựa chọn liên kết blog và logo của từng người dùng (ví dụ: [6]). Bạn có thể kiểm soát các liên kết ở bên trái bằng cách nhấp vào liên kết "configure your blog" trên trang hồ sơ của bạn, đưa bạn đến http://localhost:7657/syndie/configblog.jsp.  Khi bạn thực hiện các thay đổi ở đó, lần tiếp theo bạn đăng một bài viết lên một kho lưu trữ, thông tin đó sẽ được cung cấp cho người khác.

[6] http://syndiemedia.i2p.net/     blog.jsp?blog=ovpBy2mpO1CQ7deYhQ1cDGAwI6pQzLbWOm1Sdd0W06c=

* 4) ???

Vì tôi đã trễ cuộc họp 20 phút rồi, chắc tôi nên nói ngắn gọn thôi. Tôi biết còn vài chuyện khác đang diễn ra, nhưng thay vì đưa chúng ra ở đây, các lập trình viên muốn thảo luận thì ghé qua cuộc họp và nêu lên nhé. Dù sao thì, tạm thời vậy đã, hẹn gặp mọi người trên #i2p!

=jr
