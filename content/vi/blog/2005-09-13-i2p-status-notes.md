---
title: "Ghi chú trạng thái I2P cho ngày 2005-09-13"
date: 2005-09-13
author: "jr"
description: "Bản cập nhật hàng tuần bao gồm cơ chế giới thiệu của SSU phục vụ đục lỗ NAT, tiến độ chương trình tiền thưởng cho kiểm thử đơn vị, thảo luận về lộ trình ứng dụng khách, và việc loại bỏ chế độ giao nhận bảo đảm đã bị đánh dấu lỗi thời."
categories: ["status"]
---

Chào mọi người, đến giờ cho ghi chú tình hình hàng tuần

* Index

1) Trạng thái mạng 2) SSU introductions / đục lỗ NAT 3) Tiền thưởng 4) Hướng dẫn cho ứng dụng khách 5) ???

* 1) Net status

Chúng tôi vẫn tiếp tục vận hành với bản phát hành 0.6.0.5 trên mạng, và gần như mọi người đã nâng cấp, nhiều người đang chạy một trong các bản build kể từ đó (CVS HEAD hiện là 0.6.0.5-9). Nhìn chung mọi thứ vẫn hoạt động tốt, tuy nhiên theo quan sát của tôi, lưu lượng mạng đã tăng đáng kể, có lẽ do việc sử dụng i2p-bt hoặc i2phex nhiều hơn. Một trong các máy chủ IRC gặp chút trục trặc tối qua, nhưng máy chủ còn lại vẫn ổn và có vẻ mọi thứ đã phục hồi tốt. Tuy vậy, các bản build CVS đã có nhiều cải tiến đáng kể về xử lý lỗi và các tính năng khác, nên tôi kỳ vọng chúng ta sẽ có một bản phát hành mới trong tuần này.

* 2) SSU introductions / NAT hole punching

Những bản dựng mới nhất trong CVS bao gồm hỗ trợ cho SSU introductions [1] đã được thảo luận từ lâu, cho phép chúng tôi thực hiện NAT hole punching (kỹ thuật đục lỗ NAT) theo cách phi tập trung cho những người dùng ở phía sau NAT hoặc tường lửa mà họ không kiểm soát. Mặc dù cơ chế này không xử lý NAT đối xứng, nó vẫn bao phủ phần lớn các trường hợp ngoài kia. Phản hồi từ thực tế rất tích cực, tuy nhiên chỉ những người dùng với bản dựng mới nhất mới có thể liên lạc với những người dùng ở phía sau NAT - các bản dựng cũ cần đợi người dùng đó liên lạc trước. Vì vậy, chúng tôi sẽ đưa mã vào một bản phát hành sớm hơn thông thường để giảm khoảng thời gian chúng ta phải duy trì các tuyến bị hạn chế này.

[1] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/udp.html?rev=HEAD#introduction

* 3) Bounties

Tôi đã kiểm tra danh sách thư i2p-cvs trước đó và nhận thấy một loạt commit từ Comwiz, có vẻ liên quan đến giai đoạn 3 của chương trình tiền thưởng kiểm thử đơn vị [2]. Có lẽ Comwiz có thể cung cấp cho chúng ta một bản cập nhật tiến độ về công việc đó trong cuộc họp tối nay.

[2] http://www.i2p.net/bounty_unittests

Nhân tiện, theo gợi ý của một người ẩn danh, tôi đã cập nhật bảng vinh danh [3] đôi chút, bao gồm việc thêm ngày đóng góp, gộp nhiều khoản quyên góp của cùng một người lại, và quy đổi sang một loại tiền tệ duy nhất. Xin cảm ơn một lần nữa tới tất cả những ai đã đóng góp; nếu có thông tin nào không chính xác hoặc còn thiếu, vui lòng liên hệ và chúng tôi sẽ cập nhật.

[3] http://www.i2p.net/halloffame

* 4) Client app directions

Một trong những điều chỉnh gần đây nhất trong các bản dựng CVS hiện tại là việc loại bỏ hình thức chuyển giao cũ mode=guaranteed. Tôi không nhận ra là vẫn còn người dùng nó (và nó hoàn toàn không cần thiết, vì chúng ta đã có the full streaming lib (thư viện streaming đầy đủ) được một năm nay), nhưng khi tôi xem xét kỹ i2phex tôi nhận thấy cờ đó đang được bật. Với bản dựng hiện tại (và tất cả các bản phát hành về sau), i2phex sẽ chỉ sử dụng mode=best_effort, điều này hy vọng sẽ cải thiện hiệu năng của nó.

Điều tôi muốn khi nêu vấn đề này (ngoài việc nhắc đến nó cho người dùng i2phex) là hỏi mọi người cần gì ở phía client (phía máy khách) của I2P, và liệu tôi có nên phân bổ một phần thời gian để giúp đáp ứng một số nhu cầu đó hay không. Ngay lúc này, tôi thấy còn rất nhiều việc ở nhiều khía cạnh:
  = Syndie: đơn giản hóa việc đăng bài, đồng bộ hóa tự động, dữ liệu
     nhập, tích hợp ứng dụng (với i2p-bt, susimail, i2phex, v.v.),
     hỗ trợ threading (theo luồng) để cho phép hành vi giống diễn đàn, và hơn thế nữa.
  = eepproxy: cải thiện thông lượng, hỗ trợ pipelining
  = i2phex: bảo trì chung (tôi chưa dùng đủ nhiều để biết
     những điểm đau của nó)
  = irc: tăng cường khả năng chịu lỗi, phát hiện việc máy chủ irc thường xuyên ngừng hoạt động và
     tránh các máy chủ đang không hoạt động, lọc các hành động CTCP cục bộ thay vì trên
     máy chủ, DCC proxy
  = Cải thiện hỗ trợ x64 với jbigi, jcpuid và service wrapper
  = tích hợp systray, và loại bỏ cái cửa sổ DOS đó
  = Cải thiện điều khiển băng thông cho các đợt tải tăng đột biến
  = Cải thiện kiểm soát nghẽn cho tình trạng quá tải mạng và CPU, cũng
     như khả năng phục hồi.
  = Công khai thêm chức năng và lập tài liệu về các tính năng sẵn có của
     bảng điều khiển router cho các ứng dụng bên thứ ba
  = Tài liệu cho nhà phát triển client
  = Tài liệu giới thiệu I2P

Hơn thế nữa, ngoài tất cả những điều đó, vẫn còn những hạng mục còn lại trong lộ trình [4] và danh sách việc cần làm [5]. Tôi biết về mặt kỹ thuật chúng ta cần gì, nhưng tôi không biết *bạn* cần gì từ góc độ người dùng. Hãy nói với tôi, bạn muốn gì?

[4] http://www.i2p.net/roadmap [5] http://www.i2p.net/todo

* 5) ???

Còn một số việc khác đang diễn ra trong lõi router và phía phát triển ứng dụng, ngoài những gì đã đề cập ở trên, nhưng không phải mọi thứ đều sẵn sàng để sử dụng vào lúc này. Nếu ai có điều gì muốn nêu ra, hãy ghé qua cuộc họp tối nay lúc 8 giờ UTC tại #i2p!

=jr
