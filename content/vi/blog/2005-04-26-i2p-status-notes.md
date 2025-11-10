---
title: "Ghi chú trạng thái I2P cho ngày 2005-04-26"
date: 2005-04-26
author: "jr"
description: "Bản cập nhật hàng tuần ngắn gọn bao gồm độ ổn định mạng của phiên bản 0.5.0.7, tiến triển của SSU UDP transport với hỗ trợ đa mạng, và kinh phí treo thưởng cho kiểm thử đơn vị"
categories: ["status"]
---

Chào mọi người, hôm nay chỉ là vài ghi chú cập nhật hàng tuần ngắn gọn

* Index

1) Trạng thái mạng 2) Trạng thái SSU 3) Khoản thưởng cho kiểm thử đơn vị 4) ???

* 1) Net status

Hầu hết mọi người đã nâng cấp lên bản phát hành 0.5.0.7 của tuần trước khá nhanh (cảm ơn!), và kết quả tổng thể có vẻ tích cực. Mạng có vẻ khá đáng tin cậy và vấn đề giới hạn tốc độ tunnel trước đây đã được khắc phục. Tuy nhiên, vẫn còn một số sự cố gián đoạn được một số người dùng báo cáo, và chúng tôi đang lần ra nguyên nhân.

* 2) SSU status

Phần lớn thời gian của tôi dành để tập trung vào mã UDP 0.6, và không, nó chưa sẵn sàng để phát hành, và vâng, vẫn có tiến triển ;) Hiện tại nó có thể xử lý nhiều mạng, duy trì một số nút trên UDP và số khác trên TCP với hiệu năng khá ổn. Phần khó là xử lý tất cả các trường hợp tắc nghẽn/tranh chấp, vì mạng đang hoạt động sẽ chịu tải liên tục, nhưng trong khoảng một ngày trở lại đây đã có rất nhiều tiến triển ở mảng đó. Sẽ có thêm tin khi có thêm tin.

* 3) Unit test bounty

Như duck đã đề cập trên danh sách thư [1], zab đã khởi xướng một khoản tiền thưởng (bounty) để hỗ trợ I2P với một loạt bản cập nhật phục vụ kiểm thử — một ít kinh phí cho bất kỳ ai có thể hoàn thành các nhiệm vụ được liệt kê trên trang bounty [2]. Chúng tôi cũng đã nhận được thêm một số khoản quyên góp cho bounty đó [3] — hiện đang ở mức $1000USD. Mặc dù các bounty chắc chắn không trả theo "giá thị trường", chúng là một sự khích lệ nho nhỏ dành cho các nhà phát triển muốn giúp sức.

[1] http://dev.i2p.net/pipermail/i2p/2005-April/000721.html [2] http://www.i2p.net/bounty_unittests [3] http://www.i2p.net/halloffame

* 4) ???

Ok, tôi lại đến muộn cuộc họp nữa rồi... Chắc tôi nên ký và gửi cái này đi, ha? Ghé qua cuộc họp đi, rồi chúng ta có thể bàn thêm những vấn đề khác nữa.

=jr
