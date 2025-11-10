---
title: "Ghi chú trạng thái của I2P cho ngày 2004-10-12"
date: 2004-10-12
author: "jr"
description: "Cập nhật trạng thái I2P hàng tuần bao gồm phát hành 0.4.1.2, các thử nghiệm giới hạn băng thông động, phát triển streaming library (thư viện truyền dòng) 0.4.2, và các thảo luận qua email"
categories: ["status"]
---

Chào mọi người, đã đến lúc cập nhật hàng tuần của chúng ta

## Mục lục:

1. 0.4.1.2
2. 0.4.1.3
3. 0.4.2
4. mail discussions
5. ???

## 1) 0.4.1.2

Bản phát hành 0.4.1.2 mới đã ra mắt được vài ngày và mọi thứ diễn ra khá đúng như kỳ vọng — tuy nhiên đã có vài trục trặc với thành phần watchdog (trình giám sát) mới, khiến nó buộc dừng router của bạn khi mọi thứ ở trạng thái "Bad" thay vì khởi động lại. Như tôi đã đề cập trước đó hôm nay, tôi đang mong mọi người dùng công cụ ghi nhật ký thống kê mới để gửi cho tôi một số dữ liệu, vì vậy sự hỗ trợ của bạn ở việc này sẽ được đánh giá rất cao.

## 2) 0.4.1.3

Sẽ có một bản phát hành nữa trước khi 0.4.2 ra mắt, vì tôi muốn mạng ổn định nhất có thể trước khi tiếp tục. Hiện tại tôi đang thử nghiệm một cơ chế throttle (điều tiết) động đối với việc tham gia tunnel - chỉ định cho các router từ chối yêu cầu theo xác suất nếu chúng bị quá tải hoặc các tunnel của chúng chậm hơn bình thường. Các xác suất và ngưỡng này được tính toán một cách động dựa trên các thống kê đang được ghi nhận - nếu thời gian kiểm tra tunnel 10 phút lớn hơn thời gian kiểm tra tunnel 60 phút, hãy chấp nhận yêu cầu tunnel với xác suất 60minRate/10minRate (và nếu số lượng tunnel hiện tại của bạn lớn hơn số lượng tunnel trung bình trong 60 phút, hãy chấp nhận với p=60mRate/curTunnels).

Một cơ chế giới hạn tiềm năng khác là làm mượt băng thông theo hướng như vậy - từ chối tunnels theo xác suất khi mức sử dụng băng thông tăng đột biến. Dù sao, mục đích của tất cả những điều này là giúp phân tán việc sử dụng mạng và cân bằng các tunnels giữa nhiều người dùng hơn. Vấn đề chính chúng tôi gặp với việc cân bằng tải là sự *dư thừa* công suất quá lớn, vì thế không có bộ kích hoạt nào kiểu "chết tiệt, chúng ta chậm quá, từ chối thôi" được kích hoạt. Những cơ chế mới theo xác suất này hy vọng sẽ giữ các biến động nhanh trong tầm kiểm soát.

Tôi chưa có kế hoạch cụ thể về thời điểm bản phát hành 0.4.1.3 sẽ ra mắt - có thể là cuối tuần. Dữ liệu mọi người gửi về (như ở trên) sẽ giúp xác định liệu việc này có đáng để thực hiện hay không, hoặc liệu có những hướng đi khác đáng để theo đuổi hơn.

## 3) 0.4.2

Như chúng ta đã thảo luận trong cuộc họp tuần trước, chúng tôi đã hoán đổi các bản phát hành 0.4.2 và 0.4.3 - 0.4.2 sẽ là thư viện streaming mới, và 0.4.3 sẽ là bản cập nhật tunnel.

Tôi đã xem xét lại các tài liệu về chức năng truyền dạng luồng của TCP và nhận thấy có một số chủ đề đáng quan tâm đối với I2P. Cụ thể, thời gian khứ hồi (RTT) cao của chúng ta khiến chúng ta thiên về các cơ chế như XCP, và có lẽ chúng ta nên khá tích cực với nhiều dạng khác nhau của Explicit Congestion Notification (ECN), dù chúng ta không thể tận dụng những thứ như tùy chọn timestamp, vì đồng hồ của chúng ta có thể lệch đến một phút.

Ngoài ra, chúng ta cũng muốn đảm bảo rằng có thể tối ưu thư viện truyền luồng để xử lý các kết nối có thời gian tồn tại ngắn (mà TCP thuần (vanilla TCP) làm rất tệ) - chẳng hạn, tôi muốn có thể gửi các yêu cầu HTTP GET nhỏ (<32KB) và các phản hồi nhỏ (<32KB) chỉ trong đúng ba thông điệp:

```
Alice-->Bob: syn+data+close
Bob-->Alice: ack+data+close (the browser gets the response now)
Alice-->Bob: ack (so he doesn't resend the payload)
```
Dù sao, vẫn chưa có nhiều mã được viết cho việc này, phần giao thức thì trông khá giống TCP và các gói tin thì có vẻ giống như sự kết hợp giữa đề xuất của human và đề xuất cũ. Nếu ai có đề xuất hay ý tưởng nào, hoặc muốn hỗ trợ việc triển khai, xin hãy liên hệ.

## 4) thảo luận qua email

Đã có một số cuộc thảo luận thú vị về email bên trong (và bên ngoài) I2P - postman đã đăng một bộ ý tưởng trực tuyến và đang tìm kiếm đề xuất. Cũng đã có các thảo luận liên quan trên #mail.i2p. Có lẽ chúng ta có thể nhờ postman cập nhật tình hình cho chúng ta?

## 5) ???

Tạm thời chỉ có vậy. Trong vài phút nữa ghé qua cuộc họp và mang theo ý kiến của bạn :)

=jr
