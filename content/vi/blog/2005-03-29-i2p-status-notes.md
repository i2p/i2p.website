---
title: "Ghi chú trạng thái I2P cho ngày 2005-03-29"
date: 2005-03-29
author: "jr"
description: "Ghi chú trạng thái phát triển I2P hàng tuần đề cập đến bản phát hành 0.5.0.5 với cơ chế gộp lô, giao thức truyền tải UDP (SSU), và kho phân tán Q"
categories: ["status"]
---

Chào mọi người, đã đến lúc cho các ghi chú cập nhật hàng tuần.

* Index

1) 0.5.0.5 2) UDP (SSU) 3) Q 4) ???

* 1) 0.5.0.5

Vì mọi người đã nâng cấp lên 0.5.0.4 rất nhanh và làm rất tốt, chúng tôi sẽ phát hành bản 0.5.0.5 mới sau cuộc họp. Như đã thảo luận tuần trước, thay đổi lớn là đưa batching code (mã gom lô) vào, gộp nhiều thông điệp nhỏ lại với nhau thay vì cấp cho mỗi cái một thông điệp tunnel 1KB đầy đủ riêng. Dù chỉ riêng điều này không phải là đột phá, nó sẽ giúp giảm đáng kể số lượng thông điệp được truyền cũng như băng thông sử dụng, đặc biệt đối với các dịch vụ như IRC.

Sẽ có thêm thông tin trong thông báo phát hành, nhưng còn hai điều quan trọng khác đi kèm với rev 0.5.0.5. Trước hết, chúng tôi sẽ ngừng hỗ trợ người dùng các phiên bản trước 0.5.0.4 – hiện có hơn 100 người dùng ở 0.5.0.4, và các bản phát hành trước gặp phải những vấn đề nghiêm trọng. Thứ hai, có một bản sửa lỗi quan trọng về ẩn danh trong bản dựng mới; tuy việc khai thác sẽ đòi hỏi một số nỗ lực phát triển, nhưng đó không phải là điều khó xảy ra. Phần lớn thay đổi nằm ở cách chúng tôi quản lý netDb (cơ sở dữ liệu mạng của I2P) – thay vì xử lý tùy tiện và lưu đệm các mục tràn lan, chúng tôi sẽ chỉ phản hồi các yêu cầu netDb đối với những phần tử đã được cung cấp cho chúng tôi một cách tường minh, bất kể chúng tôi có hay không có dữ liệu đó.

Như thường lệ, có các bản sửa lỗi và một số tính năng mới, nhưng thêm thông tin sẽ được công bố trong thông báo phát hành.

* 2) UDP (SSU)

Như đã thảo luận rải rác trong 6–12 tháng qua, chúng tôi sẽ chuyển sang sử dụng UDP cho giao tiếp giữa các router khi phiên bản 0.6 được phát hành. Để tiến xa hơn theo hướng đó, chúng tôi đã có bản dự thảo đầu tiên của giao thức truyền tải trên CVS tại http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/udp.html?rev=HEAD

Đây là một giao thức khá đơn giản với các mục tiêu được nêu trong tài liệu, và tận dụng các khả năng của I2P để vừa xác thực vừa bảo mật dữ liệu, đồng thời tiết lộ ít thông tin ra bên ngoài nhất có thể. Ngay cả phần đầu tiên của quá trình bắt tay kết nối cũng không thể nhận diện được đối với người không chạy I2P. Hành vi của giao thức vẫn chưa được đặc tả đầy đủ, chẳng hạn như cách các timer kích hoạt hoặc cách sử dụng ba chỉ báo trạng thái bán đáng tin cậy khác nhau, nhưng đặc tả đã bao quát những điều cơ bản về mã hóa, đóng gói và NAT hole punching (kỹ thuật "đục lỗ" NAT). Hiện chưa có phần nào được triển khai, nhưng sẽ sớm có, vì vậy rất mong nhận được phản hồi!

* 3) Q

Aum đã miệt mài làm việc với Q(uartermaster), một kho lưu trữ phân tán, và bản nháp đầu tiên của tài liệu đã được đưa lên [1].  Một trong những ý tưởng thú vị ở đó dường như là chuyển từ một DHT thuần (bảng băm phân tán) sang một hệ thống theo kiểu memcached [2] (hệ thống cache phân tán), trong đó mỗi người dùng tự thực hiện mọi tìm kiếm hoàn toàn *cục bộ*, và yêu cầu dữ liệu thực từ máy chủ Q "trực tiếp" (tất nhiên là thông qua I2P).  Dù sao thì, cũng có vài thứ hay ho, có lẽ nếu Aum đang thức [3] chúng ta có thể moi được một bản cập nhật từ anh ấy?

[1] http://aum.i2p/q/ [2] http://www.danga.com/memcached/ [3] Chết tiệt mấy múi giờ đó!

* 4) ???

Còn nhiều chuyện nữa đang diễn ra, và nếu trước cuộc họp còn hơn vài phút nữa thì tôi đã có thể tiếp tục nói, nhưng đời là thế. Ghé qua nhé

# i2p in a few to chat.

=jr
