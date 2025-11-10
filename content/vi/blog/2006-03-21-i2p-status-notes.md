---
title: "I2P Status Notes for 2006-03-21"
date: 2006-03-21
author: "jr"
description: "Tích hợp JRobin cho thống kê mạng, các bot IRC biff và toopie, và thông báo khóa GPG mới"
categories: ["status"]
---

Chào mọi người, lại là thứ Ba rồi

* Index

1) Trạng thái mạng 2) jrobin 3) biff and toopie 4) khóa mới 5) ???

* 1) Net status

Tuần vừa qua khá ổn định, chưa có bản phát hành mới.  Tôi vẫn đang miệt mài với việc giới hạn tốc độ tunnel và vận hành ở băng thông thấp, nhưng để hỗ trợ việc kiểm thử đó, tôi đã tích hợp JRobin với bảng điều khiển web và hệ thống quản lý thống kê của chúng tôi.

* 2) JRobin

JRobin [1] là một bản port thuần Java của RRDtool [2], cho phép chúng tôi tạo ra các biểu đồ đẹp mắt giống như những biểu đồ mà zzz đã đều đặn tạo ra với chi phí bộ nhớ bổ sung rất nhỏ. Chúng tôi đã cấu hình nó để chạy hoàn toàn trong bộ nhớ, nên không có tranh chấp khóa tệp, và thời gian cập nhật cơ sở dữ liệu hầu như không đáng kể. Có rất nhiều tính năng hay ho mà JRobin có thể làm nhưng chúng tôi chưa khai thác; tuy nhiên, bản phát hành tiếp theo sẽ có các chức năng cơ bản, cùng với một phương thức để xuất dữ liệu theo định dạng mà RRDtool có thể hiểu.

[1] http://www.jrobin.org/ [2] http://people.ee.ethz.ch/~oetiker/webtools/rrdtool/

* 3) biff and toopie

Postman đã miệt mài phát triển một số bot hữu ích, và tôi vui mừng báo rằng biff đáng yêu đã trở lại [3], thông báo cho bạn mỗi khi bạn có thư (ẩn danh) khi đang ở trên irc2p. Ngoài ra, postman đã xây dựng một bot hoàn toàn mới cho chúng ta - toopie - để làm bot cung cấp thông tin cho I2P/irc2p. Chúng tôi vẫn đang nạp cho toopie các mục Hỏi-đáp thường gặp, nhưng toopie sẽ sớm xuất hiện trong các kênh quen thuộc. Cảm ơn postman!

[3] http://hq.postman.i2p/?page_id=15

* 4) new key

Ai để ý sẽ thấy rằng khóa GPG của tôi sẽ hết hạn trong vài ngày nữa. Khóa mới của tôi tại http://dev.i2p.net/~jrandom có vân tay 0209 9706 442E C4A9 91FA  B765 CE08 BC25 33DC 8D49 và ID khóa 33DC8D49. Bài viết này được ký bằng khóa cũ của tôi, nhưng các bài viết (và bản phát hành) của tôi trong năm tới sẽ được ký bằng khóa mới.

* 5) ???

Tạm thời chỉ có vậy - ghé qua #i2p trong vài phút nữa để tham gia cuộc họp hàng tuần của chúng tôi và chào một tiếng!

=jr
