---
title: "Ghi chú trạng thái I2P cho ngày 2005-02-22"
date: 2005-02-22
author: "jr"
description: "Ghi chú tình trạng phát triển I2P hàng tuần bao gồm thành công của bản phát hành 0.5, bản sửa lỗi 0.5.0.1 sắp tới, các chiến lược sắp xếp thứ tự các peer của tunnel và các cập nhật azneti2p"
categories: ["status"]
---

Chào mọi người, đến giờ cập nhật hàng tuần

* Index

1) 0.5 2) Các bước tiếp theo 3) azneti2p 4) ???

* 1) 0.5

Như các bạn đã biết, cuối cùng chúng tôi cũng phát hành 0.5, và nhìn chung thì nó hoạt động khá tốt. Tôi rất đánh giá cao việc mọi người cập nhật nhanh — chỉ trong ngày đầu tiên, 50-75% mạng đã lên 0.5! Nhờ tốc độ áp dụng nhanh, chúng tôi có thể thấy tác động của các thay đổi nhanh hơn, và qua đó đã tìm ra một loạt lỗi. Mặc dù vẫn còn một số vấn đề tồn đọng, tối nay chúng tôi sẽ phát hành bản 0.5.0.1 mới để giải quyết những vấn đề quan trọng nhất.

Như một lợi ích phụ từ các lỗi, thật thú vị khi thấy rằng các router có thể xử lý hàng nghìn tunnel ;)

* 2) Next steps

Sau bản phát hành 0.5.0.1, có thể sẽ có một bản dựng nữa để thử nghiệm một số thay đổi trong việc xây dựng tunnel thăm dò (chẳng hạn chỉ sử dụng một hoặc hai nút không lỗi, phần còn lại là các nút dung lượng cao, thay vì tất cả các nút đều không lỗi). Sau đó, chúng tôi sẽ chuyển sang 0.5.1, phiên bản sẽ cải thiện thông lượng tunnel (bằng cách gom nhiều thông điệp nhỏ thành một thông điệp tunnel duy nhất) và cho phép người dùng kiểm soát tốt hơn mức độ dễ bị tấn công predecessor (tiền nhiệm).

Các cơ chế kiểm soát đó sẽ có dạng các chiến lược sắp xếp và chọn peer (đồng cấp) theo từng máy khách, một dành cho cổng vào và điểm cuối ra, và một dành cho phần còn lại của tunnel.  Bản phác thảo nhanh hiện tại về các chiến lược tôi dự kiến:
  = random (những gì chúng ta đang có hiện nay)
  = balanced (cố gắng chủ động giảm tần suất chúng ta dùng mỗi peer)
  = strict (nếu chúng ta từng dùng A-->B-->C, thì chúng giữ nguyên thứ tự đó
            trong các tunnels tiếp theo [giới hạn theo thời gian])
  = loose (tạo một khóa ngẫu nhiên cho máy khách, tính XOR
           từ khóa đó và từng peer, và luôn sắp xếp các peer
           được chọn theo khoảng cách tính từ khóa đó [giới hạn theo thời gian])
  = fixed (luôn dùng cùng các peer theo MBTF)

Dù sao thì đó là kế hoạch, nhưng tôi không chắc chiến lược nào sẽ được triển khai trước.  Mọi góp ý đều vô cùng hoan nghênh :)

* 3) azneti2p

Những người bên azureus đã làm việc rất chăm chỉ với hàng loạt bản cập nhật, và bản snapshot b34 mới nhất [1] của họ có vẻ bao gồm một số bản sửa lỗi liên quan đến I2P. Mặc dù tôi chưa có thời gian để rà soát mã nguồn kể từ sau vấn đề về tính ẩn danh lần trước mà tôi đã nêu, họ đã sửa lỗi cụ thể đó, nên nếu bạn cảm thấy muốn mạo hiểm một chút, hãy tải bản cập nhật của họ về và thử xem sao!

[1] http://azureus.sourceforge.net/index_CVS.php

* 4) ???

Có rất nhiều việc đang diễn ra, và tôi chắc là mình vẫn chưa thể bao quát hết. Ghé qua cuộc họp trong vài phút nữa để xem tình hình thế nào nhé!

=jr
