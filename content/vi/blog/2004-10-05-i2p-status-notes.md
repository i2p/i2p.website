---
title: "Ghi chú trạng thái I2P cho ngày 2004-10-05"
date: 2004-10-05
author: "jr"
description: "Bản cập nhật trạng thái I2P hàng tuần bao gồm bản phát hành 0.4.1.1, phân tích thống kê mạng, kế hoạch cho thư viện streaming 0.4.2 và eepserver đi kèm"
categories: ["status"]
---

Chào mọi người, đến giờ cập nhật hàng tuần.

## Mục lục:

1. 0.4.1.1 status
2. Pretty pictures
3. 0.4.1.2 and 0.4.2
4. Bundled eepserver
5. ???

## 1) 0.4.1.1 trạng thái

Sau một bản phát hành 0.4.1 khá trắc trở (và bản cập nhật 0.4.1.1 nhanh chóng ngay sau đó), mạng có vẻ đã trở lại bình thường - hiện có khoảng 50-mấy nút (peer) đang hoạt động, và cả IRC lẫn eepsites(I2P Sites) đều có thể truy cập. Phần lớn rắc rối là do việc thử nghiệm lớp truyền tải (transport) mới bên ngoài điều kiện phòng thí nghiệm chưa đầy đủ (ví dụ: các socket bị hỏng vào những thời điểm kỳ lạ, độ trễ quá lớn, v.v.). Lần tới khi cần thay đổi ở lớp đó, chúng tôi chắc chắn sẽ kiểm thử rộng rãi hơn trước khi phát hành.

## 2) Hình ảnh đẹp

Trong vài ngày qua đã có rất nhiều bản cập nhật diễn ra trong CVS, và một trong những thứ mới được thêm vào là một thành phần ghi log thống kê mới, cho phép chúng tôi đơn giản trích xuất dữ liệu thống kê thô ngay khi nó được tạo ra, thay vì phải xử lý các giá trị trung bình thô sơ được thu thập trên /stats.jsp. Với nó, tôi đã theo dõi một vài thống kê chủ chốt trên một vài router, và chúng tôi đang tiến gần hơn tới việc lần ra các vấn đề ổn định còn lại. Dữ liệu thống kê thô khá cồng kềnh (một lần chạy 20 giờ trên máy của duck tạo ra gần 60MB dữ liệu), nhưng đó là lý do chúng tôi có những hình ảnh đẹp - `http://dev.i2p.net/~jrandom/stats/`

Trên đa số các đồ thị đó, trục Y là mili giây, còn trục X là giây. Có một vài điểm đáng chú ý. Trước hết, client.sendAckTime.png là một xấp xỉ khá tốt của độ trễ cho một vòng khứ hồi, vì thông điệp xác nhận (ACK) được gửi kèm với payload và sau đó quay trở lại qua toàn bộ tuyến đường của tunnel — vì vậy, phần lớn trong gần 33.000 thông điệp được gửi thành công có thời gian khứ hồi dưới 10 giây. Nếu sau đó chúng ta xem client.sendsPerFailure.png cùng với client.sendAttemptAverage.png, ta thấy rằng 563 lần gửi thất bại gần như đều đã dùng hết số lần thử lại tối đa mà chúng tôi cho phép (5 lần, với thời gian chờ mềm 10s cho mỗi lần thử và thời gian chờ cứng 60s), trong khi hầu hết các lần thử khác thành công ngay ở lần thứ nhất hoặc thứ hai.

Một hình ảnh thú vị khác là client.timeout.png, hình này gây nhiều hoài nghi về một giả thuyết tôi từng có - rằng các lỗi gửi thông điệp có tương quan với một dạng tắc nghẽn cục bộ nào đó. Dữ liệu trên đồ thị cho thấy mức sử dụng băng thông vào dao động rất lớn khi xảy ra lỗi, không có các đột biến nhất quán trong thời gian xử lý việc gửi ở phía cục bộ, và dường như hoàn toàn không có bất kỳ mẫu hình nào liên quan đến độ trễ kiểm thử tunnel.

Các tệp dbResponseTime.png và dbResponseTime2.png tương tự như client.sendAckTime.png, ngoại trừ chúng tương ứng với các thông điệp netDb thay vì các thông điệp end-to-end của máy khách.

Tệp transport.sendMessageFailedLifetime.png cho thấy chúng ta giữ một thông điệp ở phía cục bộ bao lâu trước khi coi nó là thất bại vì một lý do nào đó (ví dụ, do đến hạn hết hiệu lực hoặc peer (nút ngang hàng) mà nó nhắm tới không thể liên lạc được). Một số thất bại là không thể tránh khỏi, nhưng hình này cho thấy một số lượng đáng kể thất bại ngay sau khi hết thời hạn chờ gửi cục bộ (10s). Có một vài việc chúng ta có thể làm để khắc phục điều này: - trước hết, chúng ta có thể làm cho danh sách đen linh hoạt hơn- tăng theo hàm mũ thời gian một peer bị đưa vào danh sách đen, thay vì cố định 4 phút cho mỗi lần. (điều này đã được đưa vào CVS) - thứ hai, chúng ta có thể chủ động đánh dấu thất bại các thông điệp khi có vẻ như chúng sẽ thất bại dù sao đi nữa. Để làm điều đó, mỗi kết nối sẽ theo dõi tốc độ gửi của mình và mỗi khi có thông điệp mới được thêm vào hàng đợi của nó, nếu số byte đã xếp hàng chia cho tốc độ gửi vượt quá thời gian còn lại cho tới khi hết hạn, thì đánh dấu thông điệp là thất bại ngay lập tức. Chúng ta cũng có thể dùng số đo này khi xác định có chấp nhận thêm yêu cầu tunnel đi qua một peer hay không.

Dù sao, chuyển sang bức hình đẹp tiếp theo - transport.sendProcessingTime.png. Trong đó bạn thấy rằng máy cụ thể này hiếm khi chịu trách nhiệm cho độ trễ lớn - thường là 10-100ms, dù đôi khi có những đỉnh tăng lên tới 1s hoặc hơn.

Mỗi điểm được vẽ trên tunnel.participatingMessagesProcessed.png biểu thị số lượng thông điệp đã được chuyển tiếp qua một tunnel mà router đó tham gia. Kết hợp điều này với kích thước thông điệp trung bình sẽ cho chúng ta ước tính về mức tải mạng mà peer (nút ngang hàng) đảm nhận cho những người khác.

Hình cuối cùng là tunnel.testSuccessTime.png, cho thấy mất bao lâu để gửi một thông điệp ra ngoài một tunnel và quay trở về lại thông qua một inbound tunnel khác, giúp chúng ta ước lượng chất lượng các tunnel của chúng ta.

Được rồi, từng đó hình minh họa đẹp là đủ cho lúc này. Bạn có thể tự tạo dữ liệu với bất kỳ bản phát hành nào sau 0.4.1.1-6 bằng cách đặt thuộc tính cấu hình của router "stat.logFilters" thành một danh sách tên thống kê được phân tách bằng dấu phẩy (lấy các tên từ trang /stats.jsp). Dữ liệu đó sẽ được ghi ra stats.log mà bạn có thể xử lý bằng

```
java -cp lib/i2p.jar net.i2p.stat.StatLogFilter stat.log
```
mà chia nhỏ nó thành các tệp riêng cho từng thống kê, phù hợp để nhập vào công cụ ưa thích của bạn (ví dụ: gnuplot).

## 3) 0.4.1.2 và 0.4.2

Đã có rất nhiều bản cập nhật kể từ bản phát hành 0.4.1.1 (xem mục lịch sử để biết danh sách đầy đủ), nhưng vẫn chưa có bản sửa lỗi quan trọng nào. Chúng tôi sẽ triển khai chúng trong bản phát hành vá lỗi 0.4.1.2 vào cuối tuần này, sau khi một số lỗi còn tồn đọng liên quan đến tự động phát hiện IP được khắc phục.

Nhiệm vụ lớn tiếp theo vào thời điểm đó sẽ là đạt mốc 0.4.2, hiện được lên kế hoạch như một cuộc đại tu lớn đối với quy trình xử lý tunnel. Đó sẽ là rất nhiều việc, bao gồm sửa đổi cơ chế mã hóa và xử lý thông điệp cũng như cơ chế gộp tunnel, nhưng nó khá quan trọng, vì kẻ tấn công hiện có thể tương đối dễ dàng thực hiện một số cuộc tấn công thống kê vào các tunnel (ví dụ: predecessor (tiền nhiệm) với sắp xếp tunnel ngẫu nhiên hoặc thu thập netDb).

Tuy nhiên, dm nêu câu hỏi liệu có hợp lý không nếu làm streaming lib (thư viện streaming) trước (hiện được lên kế hoạch cho bản phát hành 0.4.3). Lợi ích của cách đó là mạng sẽ vừa đáng tin cậy hơn vừa có thông lượng tốt hơn, qua đó khuyến khích các nhà phát triển khác bắt tay vào phát triển các ứng dụng client. Sau khi phần đó được triển khai, tôi có thể quay lại việc đại tu tunnel và giải quyết các vấn đề bảo mật (không hiển thị với người dùng).

Về mặt kỹ thuật, hai tác vụ dự kiến cho 0.4.2 và 0.4.3 là độc lập với nhau, và dù sao thì cả hai cũng sẽ được thực hiện, nên có vẻ không có nhiều bất lợi khi hoán đổi chúng. Tôi nghiêng về việc đồng ý với dm, và trừ khi ai đó có thể đưa ra một số lý do để giữ 0.4.2 là bản cập nhật tunnel và 0.4.3 là thư viện streaming, chúng ta sẽ đổi chỗ chúng.

## 4) eepserver đi kèm

Như đã đề cập trong ghi chú phát hành 0.4.1, chúng tôi đã đóng gói phần mềm và cấu hình cần thiết để chạy một eepsite(I2P Site) ngay sau khi cài đặt - bạn chỉ cần đặt một tệp vào thư mục ./eepsite/docroot/ và chia sẻ I2P destination được tìm thấy trên bảng điều khiển router.

Một vài người đã góp ý rằng tôi quá hào hứng với các tệp .war - đáng tiếc là hầu hết ứng dụng cần làm thêm một chút nữa, chứ không chỉ đơn giản là thả một tệp vào thư mục ./eepsite/webapps/. Tôi đã soạn một hướng dẫn ngắn về cách chạy công cụ blog blojsom, và bạn có thể xem nó trông như thế nào trên trang web của detonate.

## 5) ???

Hiện tại tôi chỉ có vậy thôi - ghé qua buổi họp trong 90 phút nữa nếu bạn muốn thảo luận.

=jr
