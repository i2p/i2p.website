---
title: "Ghi chú trạng thái I2P cho ngày 2004-08-17"
date: 2004-08-17
author: "jr"
description: "Cập nhật trạng thái I2P hàng tuần bao gồm các vấn đề hiệu năng mạng, tấn công DoS, và phát triển Stasher DHT"
categories: ["status"]
---

Chào mọi người, đến giờ cập nhật rồi

## Chỉ mục:

1. Network status and 0.3.4.3
2. Stasher
3. ???

## 1) Trạng thái mạng và 0.3.4.3

Mặc dù mạng vẫn hoạt động trong tuần vừa qua, thỉnh thoảng đã có rất nhiều trục trặc, dẫn đến độ tin cậy giảm mạnh. Bản phát hành 0.3.4.2 đã giúp đáng kể trong việc xử lý một cuộc tấn công DoS do một số vấn đề không tương thích và đồng bộ thời gian gây ra — xem biểu đồ về các yêu cầu tới netDb (cơ sở dữ liệu mạng) cho thấy cuộc DoS (các đỉnh vượt khỏi đồ thị) đã được chặn lại khi 0.3.4.2 được đưa vào. Đáng tiếc là, đổi lại, điều đó lại kéo theo một loạt vấn đề khác, khiến một số lượng đáng kể thông điệp phải được truyền lại, như có thể thấy trên biểu đồ băng thông. Mức tải tăng lên đó cũng là do hoạt động của người dùng thực sự tăng, nên cũng không /đến mức đó/ điên rồ ;) Nhưng dù vậy, đó vẫn là một vấn đề.

Trong vài ngày qua, tôi đã khá ích kỷ. Chúng tôi đã có một loạt bản sửa lỗi được kiểm thử và triển khai trên một vài routers, nhưng tôi vẫn chưa phát hành, vì tôi hiếm khi có dịp kiểm thử sự tương tác giữa các bất tương thích trong phần mềm khi tôi chạy các mô phỏng của mình. Thế là các bạn đã phải chịu đựng hoạt động mạng cực kỳ tệ hại trong khi tôi tinh chỉnh để tìm cách giúp các routers vận hành tốt ngay cả khi nhiều routers dở tệ. Chúng tôi đang có tiến triển ở mặt đó - profiling (phân tích đặc tính) và tránh các peer (nút đồng cấp) lợi dụng cơ sở dữ liệu mạng, quản lý hàng đợi yêu cầu tới cơ sở dữ liệu mạng hiệu quả hơn, và thực thi đa dạng hóa tunnel.

Chúng ta vẫn chưa đạt được điều đó, nhưng tôi vẫn lạc quan. Hiện các kiểm thử đang chạy trên mạng trực tiếp (live net), và khi mọi thứ sẵn sàng, sẽ có bản phát hành 0.3.4.3 nhằm công bố các kết quả đó.

## 2) Stasher

Aum đã làm những việc rất ấn tượng với DHT (bảng băm phân tán) của mình, và mặc dù hiện tại nó vẫn có một số hạn chế đáng kể, nó trông khá hứa hẹn. Nó chắc chắn chưa sẵn sàng cho việc sử dụng rộng rãi, nhưng nếu bạn sẵn sàng giúp anh ấy thử nghiệm (hoặc viết mã :), hãy xem trang web và khởi chạy một node.

## 3) ???

Vậy tạm thời chỉ có vậy. Vì cuộc họp lẽ ra đã bắt đầu cách đây một phút, chắc tôi nên kết thúc ở đây. Hẹn gặp mọi người ở #i2p!

=jr
