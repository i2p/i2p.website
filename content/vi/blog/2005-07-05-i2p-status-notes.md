---
title: "Ghi chú trạng thái I2P cho ngày 2005-07-05"
date: 2005-07-05
author: "jr"
description: "Cập nhật hàng tuần bao gồm tiến độ của giao thức truyền tải SSU, biện pháp giảm thiểu tấn công IV trên tunnel, và tối ưu hóa MAC của SSU với HMAC-MD5"
categories: ["status"]
---

Chào cả nhóm, đến hẹn lại lên,

* Index

1) Trạng thái phát triển 2) Tunnel IVs 3) SSU MACs 4) ???

* 1) Dev status

Lại một tuần nữa, lại một thông báo rằng "Đã có rất nhiều tiến triển với SSU transport" ;) Các sửa đổi cục bộ của tôi đã ổn định và đã được đưa lên CVS (HEAD hiện ở 0.5.0.7-9), nhưng vẫn chưa có bản phát hành. Sẽ sớm có thêm tin tức về mảng đó. Chi tiết về các thay đổi không liên quan đến SSU đã có trong phần lịch sử [1], tuy tôi hiện vẫn để các thay đổi liên quan đến SSU ngoài danh sách đó, vì SSU hiện chưa được ai ngoài các nhà phát triển sử dụng (và các nhà phát triển đọc i2p-cvs@ :)

[1] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/history.txt?rev=HEAD

* 2) Tunnel IVs

Trong vài ngày gần đây, dvorak đã đăng rải rác một số ý tưởng về những cách khác nhau để tấn công cơ chế mật mã của tunnel, và dù hầu hết đã được xử lý trước đó, chúng tôi đã nghĩ ra một kịch bản cho phép những người tham gia gắn thẻ một cặp thông điệp để xác định rằng chúng nằm trong cùng một tunnel. Cách nó hoạt động là peer (nút ngang hàng) ở phía trước sẽ để một thông điệp đi qua, rồi sau đó thay IV và khối dữ liệu đầu tiên của một thông điệp mới bằng các phần lấy từ thông điệp tunnel đầu tiên đó. Thông điệp mới này dĩ nhiên sẽ bị hỏng, nhưng sẽ không trông giống một cuộc tấn công phát lại (replay), vì các IV khác nhau. Về sau, peer thứ hai khi đó có thể đơn giản loại bỏ thông điệp đó để điểm cuối tunnel không thể phát hiện cuộc tấn công.

Một trong những vấn đề cốt lõi ở đây là không có cách nào để xác minh một thông điệp khi nó đi qua tunnel mà không mở ra cả một loạt cuộc tấn công (xem một đề xuất mật mã cho tunnel trước đó [2] để biết một phương pháp tiến khá gần, nhưng có xác suất khá đáng ngờ và áp đặt một số giới hạn nhân tạo lên các tunnel).

[2] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/tunnel.html?rev=HEAD

Tuy nhiên, có một cách đơn giản để né cuộc tấn công cụ thể đã nêu - chỉ cần coi xor(IV, first data block) như định danh duy nhất được đưa qua bloom filter (bộ lọc Bloom) thay vì chỉ IV (vector khởi tạo). Bằng cách này, các peer (nút ngang hàng) trung gian sẽ thấy bản trùng (dup) và loại bỏ nó trước khi nó đến được peer thông đồng thứ hai. CVS đã được cập nhật để bao gồm biện pháp phòng vệ này, dù tôi rất, rất hoài nghi đây là một mối đe dọa thực tế với kích thước mạng hiện tại, nên tôi không phát hành nó như một bản phát hành riêng lẻ.

Điều này không ảnh hưởng đến tính khả thi của các tấn công theo thời gian (timing) hoặc shaping; tuy nhiên, tốt nhất là xử lý dứt điểm những cuộc tấn công dễ đối phó ngay khi chúng ta bắt gặp chúng.

* 3) SSU MACs

Như được mô tả trong đặc tả [3], phương thức truyền SSU sử dụng MAC (mã xác thực thông điệp) cho mỗi datagram được truyền. Điều này là bổ sung cho giá trị băm xác minh được gửi kèm với mỗi thông điệp I2NP (cũng như các giá trị băm xác minh đầu-cuối trên thông điệp của máy khách). Hiện tại, đặc tả và mã nguồn sử dụng HMAC-SHA256 dạng rút gọn - chỉ truyền và xác minh 16 byte đầu tiên của MAC. Điều này thì *khụ* hơi lãng phí, vì HMAC dùng hàm băm SHA256 hai lần trong quá trình của nó, mỗi lần chạy với hàm băm 32 byte, và kết quả profiling gần đây đối với phương thức truyền SSU cho thấy đây gần như là nút thắt then chốt gây tải CPU. Vì vậy, tôi đã thử thay HMAC-SHA256-128 bằng HMAC-MD5(-128) thuần - dù MD5 rõ ràng không mạnh bằng SHA256, chúng ta cũng đang rút gọn SHA256 xuống cùng kích thước với MD5 nên lượng tấn công brute force (vét cạn) cần thiết để tạo va chạm là như nhau (2^64 lần thử). Hiện tôi đang thử nghiệm và mức tăng tốc là đáng kể (đạt thông lượng HMAC cao hơn 3x trên các gói 2KB so với SHA256), nên có lẽ chúng ta sẽ triển khai phương án đó thay thế. Hoặc nếu ai có thể đưa ra một lý do thật thuyết phục để không làm vậy (hoặc một giải pháp thay thế tốt hơn), thì việc thay thế cũng khá đơn giản (chỉ một dòng mã).

[3] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/udp.html?rev=HEAD

* 4) ???

Tạm thời thì chỉ có vậy, và như mọi khi, cứ thoải mái đăng ý kiến và băn khoăn của bạn bất cứ lúc nào. CVS HEAD hiện lại có thể build được cho những người chưa cài junit (tạm thời tôi đã tách các bài kiểm thử ra khỏi i2p.jar, nhưng vẫn có thể chạy bằng test ant target), và tôi kỳ vọng sẽ sớm có thêm tin về việc thử nghiệm bản 0.6 (hiện tôi vẫn đang vật lộn với những điều kỳ quặc của cái colo box (máy chủ đặt colocation tại trung tâm dữ liệu) - telnet vào chính các giao diện của mình thì thất bại khi chạy cục bộ (không có errno hữu ích), nhưng lại hoạt động khi truy cập từ xa, và tất cả đều không hề có iptables hay bộ lọc nào khác. vui thật). Tôi vẫn chưa có truy cập mạng ở nhà, nên tối nay sẽ không có mặt trong buổi họp, nhưng có lẽ tuần sau.

=jr
