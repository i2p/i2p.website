---
title: "Ghi chú trạng thái I2P cho ngày 2005-05-03"
date: 2005-05-03
author: "jr"
description: "Bản cập nhật hàng tuần bao gồm tính ổn định của mạng, thành công của thử nghiệm trực tiếp cơ chế truyền tải SSU qua UDP, tiến triển chia sẻ tệp của i2phex, và sự vắng mặt sắp tới trong 3-4 tuần"
categories: ["status"]
---

Chào mọi người, tuần này có rất nhiều thứ cần bàn

* Index

1) Trạng thái mạng 2) Trạng thái SSU 3) i2phex 4) vắng mặt 5) ???

* 1) Net status

Không có thay đổi lớn nào về tình trạng hoạt động tổng thể của mạng — mọi thứ có vẻ khá ổn định, và dù thỉnh thoảng có vài trục trặc, các dịch vụ nhìn chung vẫn hoạt động tốt. Đã có rất nhiều cập nhật lên CVS kể từ bản phát hành trước, nhưng không có bản sửa lỗi nghiêm trọng chặn phát hành (showstopper). Có thể sẽ có thêm một bản phát hành nữa trước khi tôi chuyển đi, chỉ để đưa những cập nhật mới nhất từ CVS ra rộng rãi hơn, nhưng tôi vẫn chưa chắc.

* 2) SSU status

Bạn đã chán nghe tôi nói rằng đã có rất nhiều tiến triển trên UDP transport (cơ chế truyền tải UDP) chưa? Ừ thì tiếc quá - đã có rất nhiều tiến triển trên UDP transport. Cuối tuần qua, chúng tôi đã rời khỏi giai đoạn thử nghiệm trên mạng riêng và chuyển sang mạng đang hoạt động và khoảng một tá router đã được nâng cấp và công khai địa chỉ SSU của họ - cho phép chúng có thể được liên lạc qua TCP transport (cơ chế truyền tải TCP) bởi phần lớn người dùng nhưng cho phép các router bật SSU trao đổi qua UDP.

Việc thử nghiệm vẫn đang ở giai đoạn rất sớm, nhưng diễn ra tốt hơn nhiều so với tôi kỳ vọng. Cơ chế kiểm soát tắc nghẽn hoạt động rất ổn định và cả thông lượng lẫn độ trễ đều đủ tốt - nó có thể xác định đúng các giới hạn băng thông thực tế và chia sẻ hiệu quả đường truyền đó với các luồng TCP cạnh tranh.

Với các số liệu thống kê thu thập được từ các tình nguyện viên đã hỗ trợ, đã trở nên rõ ràng tầm quan trọng của phần mã selective acknowledgement (xác nhận chọn lọc - SACK) đối với việc hoạt động đúng cách trong các mạng có mức tắc nghẽn cao. Tôi đã dành vài ngày qua để triển khai và kiểm thử phần mã đó, và đã cập nhật đặc tả SSU [1] để bao gồm một kỹ thuật SACK mới, hiệu quả. Nó sẽ không tương thích ngược với phần mã SSU trước đây, vì vậy những người đã và đang giúp thử nghiệm nên vô hiệu hóa SSU transport cho đến khi có bản dựng mới sẵn sàng để thử nghiệm (hy vọng trong một hoặc hai ngày tới).

[1] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/udp.html?rev=HEAD

* 3) i2phex

sirup đã miệt mài làm một bản port (chuyển ứng dụng sang nền tảng khác) của phex sang i2p, và tuy còn rất nhiều việc phải làm trước khi nó sẵn sàng cho người dùng phổ thông, đầu tối nay tôi đã có thể khởi chạy nó, duyệt các tệp chia sẻ của sirup, lấy một ít dữ liệu, và dùng giao diện trò chuyện *khụ* "tức thời" của nó.

Có rất nhiều thông tin khác trên eepsite(I2P Site) của sirup [2], và sự hỗ trợ thử nghiệm từ những người đã ở trong cộng đồng i2p sẽ rất tuyệt (nhưng xin vui lòng, cho đến khi sirup phê chuẩn nó như một bản phát hành công khai, và i2p ít nhất là 0.6 nếu không muốn nói là 1.0, hãy giữ nó trong phạm vi cộng đồng i2p). Tôi tin là sirup sẽ có mặt trong buổi họp tuần này, nên có lẽ khi đó chúng ta có thể nhận thêm một số thông tin!

[2] http://sirup.i2p/

* 4) awol

Nhân tiện nói về chuyện có mặt, có lẽ tôi sẽ không có ở đây cho cuộc họp tuần tới và sẽ ngoại tuyến trong 3-4 tuần tiếp theo. Mặc dù điều đó có lẽ đồng nghĩa sẽ không có bản phát hành mới nào, vẫn còn một loạt thứ rất thú vị để mọi người hack/phát triển thêm:  = các ứng dụng như feedspace, i2p-bt/ducktorrent, i2phex, fire2pe,     addressbook, susimail, q, hoặc thứ gì đó hoàn toàn mới.  = eepproxy - sẽ thật tuyệt nếu có tính năng lọc, hỗ trợ     kết nối HTTP persistent, 'listen on' ACLs (danh sách kiểm soát truy cập), và có lẽ một     cơ chế backoff theo hàm mũ để xử lý các timeout của outproxy (proxy ra ngoài) (thay vì     round robin đơn giản)  = PRNG (bộ tạo số ngẫu nhiên giả) (như đã thảo luận trên danh sách thư)  = một thư viện PMTU (kích thước đơn vị truyền tối đa theo đường đi) (bằng Java hoặc bằng C với JNI)  = tiền thưởng cho unit test và tiền thưởng cho GCJ  = profiling bộ nhớ của router và tinh chỉnh  = và còn rất nhiều nữa.

Vì vậy, nếu bạn thấy chán và muốn góp sức nhưng đang thiếu cảm hứng, có lẽ một trong những điều ở trên sẽ giúp bạn bắt đầu. Tôi có lẽ sẽ thỉnh thoảng ghé qua một quán net, nên vẫn có thể liên lạc qua email, nhưng thời gian phản hồi sẽ là O(days).

* 5) ???

Được rồi, đại khái vậy là hết những gì tôi muốn nêu ra lúc này. Ai muốn hỗ trợ kiểm thử SSU trong tuần tới thì hãy theo dõi thông tin trên blog của tôi [3]. Còn những người khác, hẹn gặp mọi người tại buổi họp!

=jr [3] http://jrandom.dev.i2p/
