---
title: "Ghi chú trạng thái I2P ngày 2005-10-18"
date: 2005-10-18
author: "jr"
description: "Bản cập nhật hàng tuần bao gồm thành công của bản phát hành 0.6.1.3, thảo luận về hợp tác với Freenet, phân tích các cuộc tấn công bootstrap vào tunnel, tiến độ khắc phục lỗi tải lên của I2Phex, và chương trình tiền thưởng cho NAT đối xứng"
categories: ["status"]
---

Chào mọi người, lại là thứ Ba rồi

* Index

1) 0.6.1.3 2) Freenet, I2P, và darknets (mạng tối) (ôi chao) 3) Tấn công bootstrap vào Tunnel 4) I2Phex 5) Syndie/Sucker 6) ??? [tiền thưởng NAT đối xứng 500+]

* 1) 0.6.1.3

Thứ Sáu tuần trước chúng tôi đã phát hành phiên bản 0.6.1.3 mới, và với 70% mạng lưới đã được nâng cấp, các báo cáo phản hồi đều rất tích cực. Các cải tiến SSU mới dường như đã cắt giảm các lần truyền lại không cần thiết, cho phép thông lượng hiệu quả hơn ở các mức tốc độ cao hơn, và theo tôi được biết thì không có vấn đề lớn nào với proxy IRC hoặc các cải tiến của Syndie.

Một điều đáng lưu ý là Eol đã treo thưởng cho việc hỗ trợ NAT đối xứng trên rentacoder[1], vì vậy hy vọng chúng ta sẽ có một số tiến triển trên phương diện đó!

[1] http://rentacoder.com/RentACoder/misc/BidRequests/ShowBidRequest.asp?lngBidRequestId=349320

* 2) Freenet, I2P, and darknets (oh my)

Chúng tôi cuối cùng cũng đã kết thúc chuỗi thảo luận hơn 100 tin nhắn đó, với cái nhìn rõ ràng hơn về hai mạng, cách chúng phù hợp và dư địa chúng tôi có cho hợp tác thêm. Tôi sẽ không đi sâu vào các tô-pô hoặc mô hình đe dọa mà chúng phù hợp nhất ở đây, nhưng bạn có thể đào sâu vào các danh sách nếu muốn biết thêm. Về phía hợp tác, tôi đã gửi cho toad một số mã mẫu để tái sử dụng SSU transport của chúng tôi, điều này có thể hữu ích cho cộng đồng Freenet trong ngắn hạn, và về sau chúng tôi có thể cùng nhau cung cấp premix routing (định tuyến premix) cho người dùng Freenet trong các môi trường nơi I2P khả thi. Khi Freenet tiến triển, chúng tôi cũng có thể làm cho Freenet chạy trên nền I2P như một ứng dụng khách, cho phép phân phối nội dung tự động giữa những người dùng đang chạy nó (ví dụ: phân phối các kho lưu trữ và bài viết Syndie), nhưng trước hết chúng tôi sẽ xem các hệ thống tải và phân phối nội dung dự kiến của Freenet hoạt động như thế nào.

* 3) Tunnel bootstrap attacks

Michael Rogers đã liên hệ về một số kiểu tấn công mới thú vị vào quy trình tạo tunnel của I2P [2][3][4]. Cuộc tấn công chính (thực hiện thành công một predecessor attack (tấn công kẻ tiền nhiệm) trong suốt quá trình bootstrap (khởi tạo ban đầu)) thì thú vị, nhưng không thật sự thực tiễn - xác suất thành công là (c/n)^t, với c kẻ tấn công, n peer (nút ngang hàng) trong mạng, và t tunnels do mục tiêu xây dựng (trong suốt vòng đời) - nhỏ hơn xác suất đối thủ chiếm quyền kiểm soát toàn bộ h hop (chặng) trong một tunnel (P(success) = (c/n)^h) sau khi router đã xây dựng h tunnels.

Michael đã đăng thêm một phương án tấn công lên danh sách thư mà hiện chúng tôi đang xem xét, vì vậy bạn cũng có thể theo dõi thảo luận đó tại đó.

[2] http://dev.i2p.net/pipermail/i2p/2005-October/001005.html [3] http://dev.i2p.net/pipermail/i2p/2005-October/001008.html [4] http://dev.i2p.net/pipermail/i2p/2005-October/001006.html

* 4) I2Phex

Striker đang đạt thêm tiến bộ về lỗi tải lên, và theo báo cáo thì đã xác định được nguyên nhân. Hy vọng nó sẽ được đưa vào CVS tối nay, và sẽ được phát hành dưới dạng 0.1.1.33 không lâu sau đó. Hãy theo dõi diễn đàn [5] để biết thêm thông tin.

[5] http://forum.i2p.net/viewforum.i2p?f=25

Nghe đồn là redzara cũng đang đạt tiến triển khá tốt trong việc hợp nhất trở lại với nhánh chính của Phex, vì vậy hy vọng với sự giúp đỡ của Gregor, chúng ta sẽ sớm cập nhật mọi thứ lên trạng thái mới nhất!

* 5) Syndie/Sucker

dust cũng đang miệt mài làm việc với Sucker, với mã giúp đưa nhiều dữ liệu RSS/Atom hơn vào Syndie. Có lẽ chúng ta có thể tích hợp Sucker và post CLI (giao diện dòng lệnh) sâu hơn vào Syndie, thậm chí có cả một giao diện điều khiển trên web để lập lịch nhập các nguồn cấp RSS/Atom khác nhau vào nhiều blog. Hãy chờ xem...

* 6) ???

Còn nhiều việc diễn ra ngoài những điều ở trên, nhưng đó là ý chính của những gì tôi nắm được. Nếu ai có câu hỏi/quan ngại, hoặc muốn nêu thêm vấn đề khác, hãy ghé qua cuộc họp tối nay lúc 8PM UTC trên #i2p!

=jr
