---
title: "Ghi chú trạng thái I2P cho ngày 2004-08-03"
date: 2004-08-03
author: "jr"
description: "Bản cập nhật trạng thái I2P hàng tuần bao gồm hiệu năng của bản phát hành 0.3.4, phát triển bảng điều khiển web mới và nhiều dự án ứng dụng."
categories: ["status"]
---

chào mọi người, chúng ta làm nhanh bản cập nhật tình hình này cho xong nhé

## Mục lục:

1. 0.3.4 status
2. On deck for 0.3.4.1
3. New web console / I2PTunnel controller
4. 0.4 stuff
5. Other development activities
6. ???

## 1) 0.3.4 trạng thái

Với bản phát hành 0.3.4 tuần trước, mạng mới hoạt động khá tốt - các kết nối irc duy trì được vài giờ mỗi lần và việc truy xuất eepsite(I2P Site) có vẻ khá tin cậy. Thông lượng nhìn chung vẫn thấp, dù đã cải thiện đôi chút (trước đây tôi thường thấy ổn định ở mức 4-5KBps, giờ tôi thường xuyên thấy 5-8KBps). oOo đã đăng lên một cặp tập lệnh tóm tắt hoạt động irc, bao gồm thời gian khứ hồi của tin nhắn và thời lượng kết nối (dựa trên bogobot của hypercubus, được commit vào CVS gần đây)

## 2) Dự kiến cho 0.3.4.1

Như mọi người dùng 0.3.4 đã nhận thấy, tôi đã *cough* hơi dài dòng trong việc ghi log, và điều đó đã được khắc phục trong cvs. Ngoài ra, sau khi viết một số công cụ để stress-test (kiểm thử tải) ministreaming lib (thư viện ministreaming), tôi đã thêm một 'choke' (cơ chế giới hạn) để nó không ngốn một lượng bộ nhớ khổng lồ (nó sẽ chặn khi cố gắng thêm hơn 128KB dữ liệu vào bộ đệm của luồng (stream), để khi gửi một tệp lớn, router của bạn không phải nạp toàn bộ tệp đó vào bộ nhớ). Tôi nghĩ điều này sẽ giúp khắc phục các vấn đề OutOfMemory mà mọi người đang gặp phải, nhưng tôi sẽ thêm một số mã giám sát / gỡ lỗi bổ sung để xác minh điều này.

## 3) Bảng điều khiển web mới / bộ điều khiển I2PTunnel

Bên cạnh các chỉnh sửa cho 0.3.4.1 ở trên, chúng tôi đã có bản thử nghiệm đầu tiên của bảng điều khiển router mới sẵn sàng cho một số thử nghiệm. Vì một vài lý do, chúng tôi sẽ chưa đưa nó vào gói cài đặt mặc định, nên sẽ có hướng dẫn về cách chạy nó khi bản sửa đổi 0.3.4.1 phát hành trong vài ngày tới. Như các bạn đã thấy, tôi thực sự rất tệ về thiết kế web, và như nhiều người trong các bạn đã nói, tôi nên ngừng loay hoay với tầng ứng dụng và tập trung làm cho phần lõi và router trở nên cực kỳ ổn định. Vì vậy, dù bảng điều khiển mới đã có nhiều chức năng tốt mà chúng ta muốn (cấu hình router hoàn toàn qua vài trang web đơn giản, cung cấp bản tóm tắt nhanh và dễ đọc về tình trạng của router, cho phép tạo / chỉnh sửa / dừng / khởi động các thể hiện I2PTunnel khác nhau), tôi thực sự cần sự giúp đỡ từ những người giỏi mảng web.

Các công nghệ được sử dụng trong bảng điều khiển web mới là JSP, CSS tiêu chuẩn và các java beans đơn giản truy vấn router / I2PTunnels để lấy dữ liệu và xử lý các yêu cầu. Tất cả được đóng gói thành một cặp tệp .war và triển khai trên một máy chủ web Jetty tích hợp (cần được khởi động thông qua các dòng clientApp.* của router). Các JSP và bean của bảng điều khiển chính của router khá vững về mặt kỹ thuật, mặc dù các JSP và bean mới tôi xây dựng để quản lý các thể hiện I2PTunnel thì hơi chắp vá.

## 4) Các hạng mục 0.4

Ngoài giao diện web mới, bản phát hành 0.4 sẽ bao gồm trình cài đặt mới của hypercubus mà chúng tôi vẫn chưa thực sự tích hợp. Chúng tôi cũng cần thực hiện thêm một số mô phỏng quy mô lớn (đặc biệt là xử lý các ứng dụng bất đối xứng như IRC và các outproxy (proxy thoát ra Internet công khai)). Ngoài ra, có một số bản cập nhật tôi cần đưa vào kaffe/classpath để chúng ta có thể vận hành hạ tầng web mới trên các JVM mã nguồn mở. Thêm nữa, tôi phải biên soạn thêm một số tài liệu (một tài liệu về khả năng mở rộng và một tài liệu khác phân tích bảo mật/tính ẩn danh trong một vài kịch bản phổ biến). Chúng tôi cũng muốn tích hợp tất cả các cải tiến mà bạn đề xuất vào bảng điều khiển web mới.

Ồ, và hãy sửa bất kỳ lỗi nào mà bạn giúp phát hiện :)

## 5) Các hoạt động phát triển khác

Trong khi đã có rất nhiều tiến bộ trên hệ thống I2P cơ bản, đó mới chỉ là một nửa câu chuyện - rất nhiều bạn đang làm những công việc tuyệt vời trên các ứng dụng và thư viện để giúp I2P trở nên hữu ích. Tôi đã thấy một số câu hỏi trong phần lịch sử trò chuyện về việc ai đang làm gì, vì vậy để giúp đưa thông tin đó đến mọi người, đây là tất cả những gì tôi biết (nếu bạn đang làm điều gì đó chưa được liệt kê và muốn chia sẻ, nếu tôi có nhầm lẫn, hoặc nếu bạn muốn thảo luận về tiến độ của mình, xin hãy lên tiếng!)

### Active development:

- python SAM/I2P lib (devs: sunshine, aum)
- C SAM lib (devs: nightblade)
- python kademlia/I2P DHT (devs: aum)
- v2v - Voice over I2P (devs: aum)
- outproxy load balancing (devs: mule)

### Development I've heard about but don't know the status of:

- swarming file transfer / BT (devs: nickster)

### Paused development:

- Enclave DHT (devs: nightblade)
- perl SAM lib (devs: BrianR)
- I2PSnark / BT (devs: eco)
- i2pIM (devs: thecrypto)
- httptunnel (devs: mihi)
- MyI2P address book (devs: jrandom)
- MyI2P blogging (devs: jrandom)

## 6) ???

Đó là tất cả những gì tôi nghĩ ra lúc này - ghé qua cuộc họp tối nay để trò chuyện về vài thứ. Như mọi khi, 9 giờ tối GMT trên #i2p trên các máy chủ quen thuộc.

=jr
