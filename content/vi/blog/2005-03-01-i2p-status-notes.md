---
title: "Ghi chú trạng thái I2P cho ngày 2005-03-01"
date: 2005-03-01
author: "jr"
description: "Ghi chú trạng thái phát triển I2P hàng tuần bao gồm các lỗi của 0.5.0.1 và phiên bản 0.5.0.2 sắp ra mắt, cập nhật lộ trình, trình chỉnh sửa sổ địa chỉ, và cập nhật cho i2p-bt"
categories: ["status"]
---

Chào mọi người, đến lúc cập nhật tình hình rồi

* Index

1) 0.5.0.1 2) lộ trình 3) trình chỉnh sửa sổ địa chỉ và cấu hình 4) i2p-bt 5) ???

* 1) 0.5.0.1

Như đã thảo luận tuần trước, vài giờ sau cuộc họp chúng tôi đã phát hành bản 0.5.0.1 mới để sửa các lỗi trong 0.5 vốn đã khiến số lượng tunnels được xây dựng khổng lồ (cùng với một số vấn đề khác). Nhìn chung, bản này đã cải thiện tình hình, nhưng khi kiểm thử rộng hơn, chúng tôi phát hiện thêm một số lỗi nữa đang ảnh hưởng đến một vài người dùng. Cụ thể, bản 0.5.0.1 có thể ngốn rất nhiều CPU nếu bạn dùng máy chậm hoặc các tunnels của router bạn bị lỗi hàng loạt, và một số máy chủ I2PTunnel chạy lâu có thể ngốn RAM cho đến khi OOM (hết bộ nhớ). Cũng có một lỗi tồn tại lâu trong thư viện streaming, nơi chúng tôi có thể không thiết lập được kết nối nếu xảy ra đúng những lỗi theo tổ hợp nhất định.

Hầu hết những thứ này (cùng với một số thứ khác) đã được sửa trong cvs, nhưng một số vẫn chưa được giải quyết. Khi tất cả đều được sửa xong, chúng tôi sẽ đóng gói và phát hành dưới dạng bản 0.5.0.2. Tôi không chắc chính xác khi nào, hy vọng là trong tuần này, nhưng hãy chờ xem.

* 2) roadmap

Sau các bản phát hành lớn, lộ trình [1] dường như được... điều chỉnh.  Bản phát hành 0.5 cũng không khác.  Trang đó phản ánh những gì tôi cho là hợp lý và phù hợp cho định hướng sắp tới, nhưng dĩ nhiên, nếu có thêm người tham gia hỗ trợ, nó hoàn toàn có thể được điều chỉnh.  Bạn sẽ nhận thấy khoảng gián đoạn đáng kể giữa 0.6 và 0.6.1, và tuy điều đó phản ánh rất nhiều công việc, nó cũng phản ánh thực tế là tôi sẽ chuyển nhà (lại đến thời điểm đó trong năm).

[1] http://www.i2p.net/roadmap

* 3) addressbook editor and config

Detonate đã bắt đầu một số công việc về một giao diện web để quản lý các mục trong sổ địa chỉ (hosts.txt), và có vẻ khá hứa hẹn. Có lẽ chúng ta có thể nhận được một bản cập nhật từ detonate trong cuộc họp?

Ngoài ra, smeghead đang làm việc trên một giao diện web để quản lý cấu hình addressbook (sổ địa chỉ) (subscriptions.txt, config.txt). Có lẽ chúng ta có thể nhận được một bản cập nhật từ smeghead trong cuộc họp?

* 4) i2p-bt

Đã có một số tiến triển về phía i2p-bt, với bản phát hành 0.1.8 mới giải quyết các vấn đề tương thích của azneti2p như đã thảo luận trong cuộc họp tuần trước. Có lẽ chúng ta có thể nhận được bản cập nhật từ duck hoặc smeghead trong cuộc họp?

Legion cũng đã tạo một nhánh (fork) từ rev i2p-bt, gộp thêm một số mã khác, vá lại một số thứ, và có một bản binary cho Windows sẵn trên eepsite(I2P Site) của anh ấy.  Thông báo [2] có vẻ gợi ý rằng mã nguồn có thể sẽ được công bố, mặc dù hiện tại nó chưa được đưa lên eepsite(I2P Site).  Các nhà phát triển i2p chưa kiểm toán (thậm chí còn chưa xem) mã của ứng dụng khách đó, vì vậy những ai cần tính ẩn danh có thể muốn tải về và rà soát một bản sao mã trước.

[2] http://forum.i2p.net/viewtopic.php?t=382

Ngoài ra, phiên bản 2 của trình khách BT (BitTorrent) của Legion cũng đang được phát triển, dù tôi không rõ tình trạng của nó. Có lẽ chúng ta có thể xin Legion cập nhật trong cuộc họp?

* 5) ???

Đó là tất cả những gì tôi muốn nói lúc này, có rất nhiều việc đang diễn ra. Có ai khác đang làm việc gì mà có lẽ chúng ta có thể cập nhật trong cuộc họp không?

=jr
