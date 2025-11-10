---
title: "Ghi chú trạng thái I2P cho ngày 2005-01-18"
date: 2005-01-18
author: "jr"
description: "Ghi chú trạng thái phát triển I2P hàng tuần bao gồm trạng thái mạng, thiết kế định tuyến tunnel 0.5, i2pmail.v2 và bản vá bảo mật azneti2p_0.2"
categories: ["status"]
---

Chào mọi người, đến giờ cập nhật hằng tuần

* Index

1) Trạng thái mạng 2) 0.5 3) i2pmail.v2 4) azneti2p_0.2 5) ???

* 1) Net status

Ừm, không có nhiều điều để báo cáo ở đây - mọi thứ vẫn hoạt động như tuần trước, kích thước của mạng vẫn khá tương tự, có lẽ lớn hơn một chút. Một vài trang mới thú vị đang xuất hiện - xem diễn đàn [1] và orion [2] để biết chi tiết.

[1] http://forum.i2p.net/viewforum.php?f=16 [2] http://orion.i2p/

* 2) 0.5

Nhờ sự giúp đỡ của postman, dox, frosk, và cervantes (và mọi người đã tunnel dữ liệu qua router của họ ;), chúng tôi đã thu thập dữ liệu thống kê kích thước thông điệp trong suốt một ngày [3]. Có hai bộ thống kê ở đó - chiều cao và chiều rộng của vùng phóng to (zoom). Động lực là mong muốn khám phá tác động của các chiến lược đệm (padding) thông điệp khác nhau đối với tải mạng, như đã giải thích [4] trong một trong các bản nháp cho định tuyến tunnel 0.5. (ooOOoo hình ảnh đẹp mắt).

Điều đáng lo nhất trong những gì tôi tìm thấy khi đào sâu vào chúng là chỉ bằng cách dùng một vài ngưỡng padding (đệm dữ liệu) được điều chỉnh thủ công khá đơn giản, việc padding tới những kích thước cố định đó vẫn dẫn tới lãng phí hơn 25% băng thông.  Ừ, tôi biết, chúng ta sẽ không làm vậy. Có lẽ mọi người có thể nghĩ ra thứ gì đó tốt hơn bằng cách đào sâu vào dữ liệu thô đó.

[3] http://dev.i2p.net/~jrandom/messageSizes/ [4] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/                                  tunnel.html?rev=HEAD#tunnel.padding

Thực ra, liên kết [4] đó dẫn chúng ta đến hiện trạng của các kế hoạch 0.5 về định tuyến tunnel. Như Connelly đã đăng [5], gần đây đã có rất nhiều thảo luận trên IRC về một số bản thảo, với polecat, bla, duck, nickster, detonate và những người khác đóng góp đề xuất và các câu hỏi đào sâu (ok, và snarks ;). Sau hơn một tuần một chút, chúng tôi phát hiện một lỗ hổng tiềm tàng liên quan đến [4], trong đó một kẻ tấn công bằng cách nào đó có thể chiếm quyền inbound tunnel gateway (cổng vào của tunnel) và đồng thời kiểm soát một trong các peer (nút ngang hàng) khác ở phần sau của tunnel đó. Mặc dù trong hầu hết các trường hợp, riêng điều này sẽ không làm lộ điểm cuối, và về mặt xác suất thì càng khó thực hiện khi mạng phát triển, nhưng nó vẫn thật tệ (tm).

Và rồi [6] xuất hiện. Điều này loại bỏ vấn đề đó, cho phép chúng ta có các tunnel với độ dài bất kỳ, và giải quyết nạn đói trên thế giới [7]. Tuy nhiên, nó lại mở ra một vấn đề khác theo đó kẻ tấn công có thể tạo các vòng lặp trong tunnel, nhưng dựa trên một đề xuất [8] mà Taral đưa ra năm ngoái liên quan đến session tags (thẻ phiên) dùng trên ElGamal/AES, chúng ta có thể giảm thiểu thiệt hại gây ra bằng cách sử dụng một chuỗi các bộ tạo số giả ngẫu nhiên đồng bộ [9].

[5] http://dev.i2p.net/pipermail/i2p/2005-January/000557.html [6] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/                                             tunnel-alt.html?rev=HEAD [7] đoán xem phát biểu nào là sai? [8] http://www.i2p.net/todo#sessionTag [9] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/                                 tunnel-alt.html?rev=HEAD#tunnel.prng

Đừng lo nếu những điều ở trên nghe có vẻ rối rắm - bạn đang chứng kiến phần bên trong của vài vấn đề thiết kế khó nhằn được đem ra mổ xẻ công khai. Nếu những điều trên nghe có vẻ *không* rối rắm, hãy liên hệ với chúng tôi, vì chúng tôi luôn tìm thêm người để cùng mổ xẻ những thứ này :)

Dù sao, như tôi đã đề cập trên danh sách [10], tiếp theo tôi muốn triển khai chiến lược thứ hai [6] để rà soát và xử lý các chi tiết còn lại. Kế hoạch cho 0.5 hiện tại là gom tất cả các thay đổi không tương thích ngược lại với nhau — mật mã tunnel mới, v.v. — và phát hành dưới dạng 0.5.0, sau đó, khi điều đó đã ổn định trên mạng, chuyển sang các phần khác của 0.5 [11], chẳng hạn như điều chỉnh chiến lược pooling (gộp tài nguyên) như mô tả trong các đề xuất, và phát hành dưới dạng 0.5.1. Tôi hy vọng chúng ta vẫn kịp ra mắt 0.5.0 vào cuối tháng, nhưng để xem sao.

[10] http://dev.i2p.net/pipermail/i2p/2005-January/000558.html [11] http://www.i2p.net/roadmap#0.5

* 3) i2pmail.v2

Mới đây postman đã đưa ra một bản kế hoạch hành động dạng nháp cho hạ tầng thư thế hệ tiếp theo [12], và nó trông cực kỳ ấn tượng. Dĩ nhiên, lúc nào chúng ta cũng có thể nghĩ ra thêm nhiều tính năng hào nhoáng, nhưng về nhiều mặt thì kiến trúc của nó khá ổn. Hãy xem những gì đã được tài liệu hóa đến giờ [13], và liên hệ với postman để chia sẻ ý kiến của bạn!

[12] http://forum.i2p.net/viewtopic.php?t=259 [13] http://www.postman.i2p/mailv2.html

* 4) azneti2p_0.2

Như tôi đã đăng lên danh sách thư [14], plugin azneti2p ban đầu dành cho azureus có một lỗi nghiêm trọng ảnh hưởng đến tính ẩn danh. Vấn đề là ở các torrent hỗn hợp, nơi một số người dùng ẩn danh và những người khác thì không, người dùng ẩn danh sẽ kết nối tới người dùng không ẩn danh /trực tiếp/ thay vì thông qua I2P. Paul Gardner và các nhà phát triển azureus khác đã phản hồi rất nhanh và phát hành một bản vá ngay lập tức. Sự cố tôi thấy không còn xuất hiện trong azureus v. 2203-b12 + azneti2p_0.2.

Chúng tôi vẫn chưa tiến hành rà soát và kiểm toán mã nguồn để đánh giá các vấn đề ẩn danh tiềm ẩn, vì vậy “tự chịu rủi ro khi sử dụng” (Mặt khác, chúng tôi cũng nói điều tương tự về I2P trước khi phát hành phiên bản 1.0). Nếu bạn sẵn sàng, tôi biết các nhà phát triển Azureus sẽ đánh giá cao việc nhận thêm phản hồi và báo cáo lỗi liên quan đến plugin. Dĩ nhiên, chúng tôi sẽ thông báo cho mọi người nếu phát hiện ra bất kỳ vấn đề nào khác.

[14] http://dev.i2p.net/pipermail/i2p/2005-January/000553.html

* 5) ???

Có rất nhiều việc đang diễn ra, như bạn thấy. Tôi nghĩ vậy là hết những gì tôi muốn nêu, nhưng hãy ghé qua cuộc họp trong 40 phút nữa nếu còn điều gì bạn muốn thảo luận (hoặc nếu bạn chỉ muốn than phiền về những thứ ở trên)

=jr
