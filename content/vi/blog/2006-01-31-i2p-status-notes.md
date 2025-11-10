---
title: "Ghi chú trạng thái I2P ngày 2006-01-31"
date: 2006-01-31
author: "jr"
description: "Những thách thức về độ tin cậy mạng, bản phát hành 0.6.1.10 sắp ra mắt với cơ chế mật mã mới cho việc tạo tunnel, và các thay đổi không tương thích ngược"
categories: ["status"]
---

Chào mọi người, lại đến thứ Ba rồi,

* Index

1) Trạng thái mạng 2) Trạng thái 0.6.1.10 3) ???

* 1) Net status

Trong tuần vừa qua, tôi đã thử một vài tinh chỉnh khác nhau để tăng độ tin cậy của việc tạo tunnel trên mạng đang hoạt động, nhưng vẫn chưa có đột phá nào. Tuy nhiên, đã có một số thay đổi đáng kể trong CVS, nhưng chúng chưa thể gọi là... ổn định. Vì vậy, nhìn chung, tôi khuyến nghị mọi người hoặc sử dụng bản phát hành mới nhất (0.6.1.9, được gắn thẻ trong CVS là i2p_0_6_1_9), hoặc sử dụng các bản dựng mới nhất với tunnel không quá 1 hop. Mặt khác...

* 2) 0.6.1.10 status

Thay vì cứ mãi vật lộn với những chỉnh sửa nhỏ lẻ, tôi đã làm việc trên mạng thử nghiệm cục bộ của mình để chuyển sang mật mã và quy trình mới cho việc tạo tunnel (đường hầm mạng) [1]. Điều này sẽ giải quyết một phần lớn tỷ lệ thất bại khi tạo tunnel, sau đó chúng ta có thể tinh chỉnh thêm nếu cần.

[1] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/                                tunnel-alt-creation.html?rev=HEAD

Một hệ quả đáng tiếc là 0.6.1.10 sẽ không tương thích ngược. Đã lâu rồi chúng tôi không có một bản phát hành không tương thích ngược, nhưng thời kỳ đầu thì làm vậy khá nhiều, nên có lẽ sẽ không phải là vấn đề lớn. Về cơ bản, sau khi nó chạy tốt trên mạng thử nghiệm cục bộ của tôi, chúng tôi sẽ triển khai song song cho một vài tình nguyện viên dũng cảm để thử nghiệm sớm, rồi khi nó sẵn sàng phát hành, chúng tôi chỉ việc chuyển các seed references (các tham chiếu reseed) sang các seeds (các máy chủ reseed) của mạng mới và tung nó ra.

Tôi chưa có thời gian dự kiến (ETA) cho bản phát hành 0.6.1.10, nhưng hiện tại mọi thứ có vẻ khá ổn (phần lớn độ dài tunnel đang hoạt động tốt, nhưng vẫn còn một vài nhánh tôi chưa kiểm thử áp lực). Sẽ có thêm thông tin khi có thêm thông tin, dĩ nhiên.

* 3) ???

Thats about all I have to mention at the moment, though I know there are things others are hacking on and there are a few tricks up my sleeves for later, but we'll find out more when the time is right. Anyway, see y'all in a few minutes!

=jr
