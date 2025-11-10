---
title: "Ghi chú trạng thái I2P cho ngày 2005-06-21"
date: 2005-06-21
author: "jr"
description: "Bản cập nhật hàng tuần bao gồm việc nhà phát triển trở lại sau chuyến công tác, tiến độ của giao thức truyền tải SSU, hoàn tất chương trình treo thưởng cho kiểm thử đơn vị, và sự cố gián đoạn dịch vụ"
categories: ["status"]
---

Chào mọi người, đã đến lúc bắt đầu lại các ghi chú tình hình hàng tuần của chúng ta

* Index

1) Trạng thái nhà phát triển 2) Trạng thái phát triển 3) Tiền thưởng kiểm thử đơn vị 4) Gián đoạn dịch vụ 5) ???

* 1) Dev[eloper] status

Sau 4 thành phố ở 4 quốc gia, cuối cùng tôi cũng ổn định chỗ ở và lại miệt mài viết mã. Tuần trước tôi đã gom đủ những linh kiện cuối cùng để lắp một chiếc laptop, tôi không còn phải ngủ nhờ hết ghế sofa nhà này đến nhà khác nữa, và tuy tôi không có truy cập Internet ở nhà, xung quanh có rất nhiều quán Internet, nên việc truy cập khá đáng tin cậy (chỉ là không thường xuyên và tốn kém).

Điểm cuối cùng đó có nghĩa là tôi sẽ không lên irc nhiều như trước, ít nhất là cho đến mùa thu (tôi đang thuê lại nhà đến khoảng tháng Tám và sẽ tìm một chỗ nơi tôi có thể truy cập mạng 24/7). Tuy nhiên, điều đó không có nghĩa là tôi sẽ làm ít việc hơn - tôi sẽ chủ yếu làm việc trên mạng thử nghiệm riêng của mình, đẩy các bản build ra để thử nghiệm trên mạng thật (và, ờ, à đúng rồi, các bản phát hành). Điều đó cũng có nghĩa là có lẽ chúng ta nên chuyển một số thảo luận vốn trước đây diễn ra tự do trong #i2p sang danh sách thư [1] và/hoặc diễn đàn [2] (dù vậy tôi vẫn đọc lại lịch sử trò chuyện của #i2p). Tôi vẫn chưa tìm được một chỗ phù hợp để có thể tham gia các cuộc họp phát triển của chúng ta, nên tuần này tôi sẽ không có mặt, nhưng có lẽ đến tuần sau tôi sẽ tìm được.

Dù sao đi nữa, nói về tôi thế là đủ rồi.

[1] http://dev.i2p.net/pipermail/i2p/ [2] http://forum.i2p.net/

* 2) Dev[elopment] status

Trong lúc tôi đang chuyển chỗ ở, tôi đã làm việc trên hai mảng chính - tài liệu và SSU transport (cơ chế truyền tải SSU) (mảng sau thì chỉ mới bắt đầu từ khi tôi có laptop). Tài liệu vẫn đang được triển khai, gồm một bản tổng quan lớn, khá đáng sợ, cũng như một loạt tài liệu triển khai nhỏ hơn (bao gồm các nội dung như bố cục mã nguồn, tương tác giữa các thành phần, v.v.).

Tiến độ SSU đang diễn ra tốt đẹp - các trường bit ACK mới đã được triển khai, cơ chế giao tiếp đang xử lý việc mất mát (mô phỏng) một cách hiệu quả, tốc độ truyền phù hợp với các điều kiện khác nhau, và tôi đã khắc phục một số lỗi khó chịu mà trước đây tôi từng gặp phải. Tuy vậy, tôi vẫn đang tiếp tục kiểm thử các thay đổi này, và khi thích hợp chúng tôi sẽ lên kế hoạch một loạt thử nghiệm trực tiếp trên mạng, và sẽ cần một số tình nguyện viên hỗ trợ cho các thử nghiệm đó. Sẽ có thêm thông tin về việc này khi có.

* 3) Unit test bounty

Tôi rất vui được thông báo rằng Comwiz đã chủ động gửi một loạt bản vá để nhận thưởng giai đoạn đầu của tiền thưởng unit test [3]! Chúng tôi vẫn đang hoàn thiện một số chi tiết nhỏ trong các bản vá, nhưng tôi đã nhận được các bản cập nhật và đã tạo cả báo cáo junit và clover theo yêu cầu. Tôi kỳ vọng chúng ta sẽ sớm có các bản vá trong CVS, khi đó chúng tôi sẽ phát hành tài liệu kiểm thử của Comwiz.

Vì clover là một sản phẩm thương mại (miễn phí cho các nhà phát triển mã nguồn mở [4]), chỉ những người đã cài đặt clover và nhận được giấy phép clover mới có thể tạo các báo cáo clover. Dù sao đi nữa, chúng tôi sẽ công bố các báo cáo clover trên web theo định kỳ, vì vậy những người chưa cài đặt clover vẫn có thể xem bộ kiểm thử của chúng tôi hoạt động tốt đến đâu.

[3] http://www.i2p.net/bounties_unittest [4] http://www.cenqua.com/clover/

* 4) Service outage

Như nhiều người có lẽ đã nhận thấy, (ít nhất) một trong các outproxies (proxy thoát) đang ngừng hoạt động (squid.i2p), cũng như www.i2p, dev.i2p, cvs.i2p và blog của tôi. Đây không phải là những sự cố riêng rẽ - máy chủ lưu trữ chúng đã bị hỏng.

=jr
