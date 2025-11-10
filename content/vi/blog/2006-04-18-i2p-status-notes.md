---
title: "Ghi chú trạng thái I2P cho ngày 2006-04-18"
date: 2006-04-18
author: "jr"
description: "Các cải tiến mạng trong 0.6.1.16, phân tích hiện tượng sụp đổ do tắc nghẽn khi tạo tunnel, và các cập nhật về phát triển Feedspace"
categories: ["status"]
---

Chào mọi người, lại đến thứ Ba rồi, đến lúc cho bản ghi chú trạng thái hàng tuần của chúng ta.

* Index

1) Trạng thái mạng và 0.6.1.16 2) Tạo Tunnel (đường hầm) và tắc nghẽn 3) Feedspace 4) ???

* 1) Net status and 0.6.1.16

Với 70% mạng lưới đã nâng cấp lên 0.6.1.16, chúng tôi dường như đang thấy sự cải thiện so với các bản phát hành trước; và với việc các vấn đề trong bản phát hành đó đã được khắc phục, chúng tôi có cái nhìn rõ ràng hơn về điểm nghẽn tiếp theo. Đối với những người chưa nâng cấp lên 0.6.1.16, vui lòng nâng cấp càng sớm càng tốt, vì các bản phát hành trước sẽ từ chối một cách tùy tiện các yêu cầu tạo tunnel (đường hầm trong I2P), ngay cả khi router (bộ định tuyến I2P) có đủ tài nguyên để tham gia thêm nhiều tunnels.

* 2) Tunnel creation and congestion

Hiện tại, có vẻ như chúng ta đang gặp tình trạng có lẽ được mô tả đúng nhất là congestion collapse (sụp đổ do tắc nghẽn) - các yêu cầu tạo tunnel đang bị từ chối vì routers thiếu băng thông, nên lại gửi thêm nhiều yêu cầu tạo tunnel với hy vọng tìm được các routers còn dư tài nguyên, nhưng rốt cuộc chỉ làm tăng băng thông sử dụng. Vấn đề này đã tồn tại từ khi chúng ta chuyển sang cơ chế mật mã tạo tunnel mới trong 0.6.1.10 và phần lớn bắt nguồn từ việc chúng ta không nhận được phản hồi tham gia/từ chối theo từng hop (chặng) cho đến khi (hoặc chính xác hơn, *trừ khi*) yêu cầu và phản hồi đã đi xuyên qua chiều dài của hai tunnel. Nếu bất kỳ peer (nút ngang hàng) nào trong số đó không chuyển tiếp được thông điệp, chúng ta không biết peer nào bị lỗi, peer nào đã đồng ý, và peer nào đã từ chối rõ ràng.

Chúng tôi đã giới hạn số lượng yêu cầu tạo tunnel đồng thời đang được xử lý (và các thử nghiệm cho thấy việc tăng thời gian chờ không giúp ích), vì vậy giải pháp truyền thống của Nagle là không đủ. Hiện tôi đang thử một vài tinh chỉnh đối với mã xử lý yêu cầu của chúng tôi, nhằm giảm tần suất các yêu cầu bị rơi mất một cách âm thầm (trái ngược với các từ chối rõ ràng), và đối với mã tạo yêu cầu của chúng tôi để giảm mức độ đồng thời khi tải cao. Tôi cũng đang thử một số cải tiến khác đang giúp tăng đáng kể tỷ lệ xây dựng tunnel thành công, dù chúng vẫn chưa sẵn sàng để sử dụng một cách an toàn.

Có ánh sáng ở cuối tunnel, và tôi trân trọng sự kiên nhẫn tiếp tục đồng hành cùng chúng tôi khi chúng ta tiến về phía trước. Tôi kỳ vọng chúng tôi sẽ có một bản phát hành khác muộn hơn trong tuần này để triển khai một số cải tiến, sau đó chúng tôi sẽ đánh giá lại tình trạng của mạng để xem hiện tượng sụp đổ do tắc nghẽn đã được khắc phục hay chưa.

* 3) Feedspace

Frosk đã miệt mài làm việc với Feedspace và đã cập nhật một vài trang trên trang Trac, bao gồm một tài liệu tổng quan mới, một danh sách các tác vụ còn dang dở, một số chi tiết về db (cơ sở dữ liệu), và nhiều hơn nữa. Hãy ghé qua http://feedspace.i2p/ để bắt kịp những thay đổi mới nhất, và có lẽ hỏi dồn Frosk bằng các câu hỏi khi bạn thuận tiện nhất :)

* 4) ???

Tạm thời tôi chỉ có thể bàn đến đây, nhưng xin mời ghé qua #i2p tham dự buổi họp của chúng tôi tối nay (8pm UTC) để trò chuyện thêm!

=jr
