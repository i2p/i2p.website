---
title: "Ghi chú trạng thái I2P cho ngày 2006-01-24"
date: 2006-01-24
author: "jr"
description: "Cập nhật trạng thái mạng, quy trình xây dựng tunnel mới cho 0.6.2, và các cải tiến về độ tin cậy"
categories: ["status"]
---

Chào mọi người, thứ Ba cứ quay lại mãi...

* Index

1) Trạng thái mạng 2) Quy trình build mới 3) ???

* 1) Net status

Tuần vừa qua không mang đến nhiều thay đổi cho mạng lưới, khi phần lớn người dùng (77%) đã nâng cấp lên bản phát hành mới nhất.  Tuy vậy, có một số thay đổi lớn đang ở phía trước, liên quan đến quy trình xây dựng tunnel (đường hầm) mới, và những thay đổi này sẽ gây ra một vài trục trặc cho những ai đang hỗ trợ thử nghiệm các bản dựng chưa phát hành.  Tuy nhiên, nhìn chung, những người dùng các bản phát hành vẫn sẽ có mức độ dịch vụ khá đáng tin cậy.

* 2) New build process

Là một phần của đợt đại tu tunnel cho 0.6.2, chúng tôi đang thay đổi thủ tục được dùng trong router để thích ứng tốt hơn với các điều kiện thay đổi và xử lý tải một cách gọn gàng hơn. Đây là bước đệm để tích hợp các chiến lược lựa chọn peer (nút ngang hàng) mới và cơ chế mật mã tạo tunnel mới, và hoàn toàn tương thích ngược. Tuy nhiên, trong quá trình đó, chúng tôi cũng tinh chỉnh một số điểm bất thường trong quy trình dựng tunnel; dù vài điểm như vậy từng giúp che mờ một số vấn đề về độ tin cậy, chúng có thể đã dẫn đến một sự đánh đổi giữa ẩn danh và độ tin cậy kém tối ưu. Cụ thể, trước đây hệ thống sẽ sử dụng 1 hop tunnels dự phòng khi gặp sự cố nghiêm trọng; còn quy trình mới sẽ ưu tiên trạng thái không thể tiếp cận thay vì dùng các tunnels dự phòng, đồng nghĩa người dùng sẽ thấy nhiều vấn đề về độ tin cậy hơn. Ít nhất thì chúng sẽ lộ rõ cho đến khi nguồn gốc của vấn đề độ tin cậy của tunnel được xử lý.

Dù sao thì, hiện tại quy trình build chưa đạt mức độ tin cậy chấp nhận được, nhưng khi đạt được, chúng tôi sẽ đưa nó đến mọi người trong một bản phát hành.

* 3) ???

Tôi biết còn một vài người khác đang thực hiện các hoạt động liên quan khác, nhưng tôi sẽ để họ tự thông báo cho chúng ta khi họ thấy phù hợp. Dù sao thì, hẹn gặp mọi người tại buổi họp trong vài phút nữa!

=jr
