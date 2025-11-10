---
title: "Ghi chú trạng thái I2P cho ngày 2005-10-25"
date: 2005-10-25
author: "jr"
description: "Cập nhật hàng tuần bao gồm tăng trưởng mạng lên 400–500 nút, tích hợp Fortuna PRNG, hỗ trợ biên dịch native bằng GCJ, trình khách torrent gọn nhẹ i2psnark, và phân tích tấn công bootstrap đối với tunnel"
categories: ["status"]
---

Chào mọi người, có thêm tin tức từ tiền tuyến

* Index

1) Trạng thái mạng 2) Tích hợp Fortuna 3) Trạng thái GCJ 4) i2psnark trở lại 5) Thêm về bootstrapping (khởi tạo ban đầu) 6) Điều tra vi-rút 7) ???

* 1) Net status

Tuần vừa rồi trên mạng khá tốt - mọi thứ có vẻ khá ổn định, thông lượng bình thường, và mạng tiếp tục tăng trưởng lên mức khoảng 400–500 peer (nút ngang hàng). Cũng đã có một số cải tiến đáng kể kể từ bản phát hành 0.6.1.3, và vì chúng ảnh hưởng đến hiệu năng và độ tin cậy, tôi kỳ vọng chúng ta sẽ có bản phát hành 0.6.1.4 trong tuần này.

* 2) Fortuna integration

Nhờ bản sửa lỗi nhanh của Casey Marshall [1], chúng tôi đã có thể tích hợp bộ tạo số giả ngẫu nhiên Fortuna [2] của GNU-Crypto. Điều này loại bỏ nguyên nhân gây nhiều bực bội với blackdown JVM (máy ảo Java), và cho phép chúng tôi làm việc trơn tru với GCJ. Việc tích hợp Fortuna vào I2P là một trong những lý do chính khiến smeghead phát triển "pants" (một 'portage' dựa trên 'ant'), vì vậy giờ đây chúng tôi lại có thêm một lần sử dụng pants thành công :)

[1] http://lists.gnu.org/archive/html/gnu-crypto-discuss/2005-10/msg00007.html [2] http://en.wikipedia.org/wiki/Fortuna

* 3) GCJ status

Như đã đề cập trên list [3], giờ đây chúng ta có thể chạy router và hầu hết các client một cách liền mạch với GCJ [4]. Bản thân bảng điều khiển web vẫn chưa hoạt động đầy đủ, vì vậy bạn cần tự cấu hình router bằng router.config (dù về cơ bản nó sẽ tự chạy và khởi động các tunnels của bạn sau khoảng một phút). Tôi chưa hoàn toàn chắc GCJ sẽ phù hợp thế nào với kế hoạch phát hành của chúng tôi, dù hiện tôi thiên về việc phân phối java thuần túy nhưng hỗ trợ cả java & các phiên bản biên dịch native. Việc phải biên dịch và phân phối rất nhiều bản dựng khác nhau cho các hệ điều hành và phiên bản thư viện khác nhau, v.v. cũng khá phiền phức. Có ai có ý kiến mạnh mẽ về vấn đề đó không?

Một ưu điểm khác của hỗ trợ GCJ là khả năng sử dụng thư viện streaming từ C/C++/Python/v.v. Tôi không rõ có ai đang làm loại tích hợp như vậy không, nhưng có lẽ sẽ rất đáng làm, vì vậy nếu bạn quan tâm muốn hack ở mảng đó, hãy cho tôi biết!

[3] http://dev.i2p.net/pipermail/i2p/2005-October/001021.html [4] http://gcc.gnu.org/java/

* 4) i2psnark returns

Mặc dù i2p-bt là client BitTorrent đầu tiên được port sang I2P và được sử dụng rộng rãi, nhưng eco mới là người đi trước một bước với bản port snark [5] của mình từ khá lâu trước đây. Đáng tiếc là nó không được cập nhật kịp thời hoặc duy trì khả năng tương thích với các client BitTorrent ẩn danh khác, nên nó đã biến mất một thời gian. Tuy nhiên, tuần trước tôi gặp một số rắc rối khi xử lý các vấn đề hiệu năng ở đâu đó trong chuỗi i2p-bt<->sam<->streaming lib<->i2cp, nên tôi chuyển sang mã snark gốc của mjw và thực hiện một bản port đơn giản [6], thay thế mọi lời gọi java.net.*Socket bằng các lời gọi I2PSocket*, thay InetAddresses bằng Destinations, và thay URLs bằng các lời gọi EepGet. Kết quả là một client BitTorrent dòng lệnh rất nhỏ (khoảng 60KB sau khi biên dịch) mà chúng tôi sẽ phát hành kèm theo bản phát hành I2P.

Ragnarok đã bắt đầu mổ xẻ và chỉnh sửa để cải tiến thuật toán chọn khối của nó, và chúng tôi hy vọng sẽ bổ sung cả giao diện web lẫn khả năng multitorrent (hỗ trợ nhiều torrent đồng thời) vào đó trước khi phát hành phiên bản 0.6.2. Nếu bạn quan tâm và muốn giúp đỡ, hãy liên hệ nhé! :)

[5] http://klomp.org/snark/ [6] http://dev.i2p.net/~jrandom/snark_diff.txt

* 5) More on bootstrapping

Mailing list (nhóm thư) đã khá sôi động gần đây, với các mô phỏng mới và phân tích của Michael về việc xây dựng tunnel. Cuộc thảo luận vẫn đang diễn ra, với một số ý tưởng hay từ Toad, Tom và polecat, vì vậy hãy xem qua nếu bạn muốn đóng góp ý kiến về các đánh đổi cho một số vấn đề thiết kế liên quan đến ẩn danh mà chúng tôi sẽ cải tiến cho bản phát hành 0.6.2 [7].

Dành cho những ai thích chút mãn nhãn, Michael cũng có thứ dành cho bạn, với một mô phỏng về xác suất cuộc tấn công có thể nhận diện bạn - như là hàm của tỷ lệ phần trăm mạng lưới mà họ kiểm soát [8], và như là hàm của mức độ hoạt động của tunnel của bạn [9]

(làm tốt lắm Michael, cảm ơn!)

[7] http://dev.i2p.net/pipermail/i2p/2005-October/thread.html     (theo dõi chuỗi thảo luận "i2p tunnel bootstrap attack") [8] http://dev.i2p.net/~jrandom/fraction-of-attackers.png [9] http://dev.i2p.net/~jrandom/messages-per-tunnel.png

* 6) Virus investigations

Đã có một số thảo luận về các vấn đề tiềm ẩn liên quan đến phần mềm độc hại được phân phối kèm theo một ứng dụng hỗ trợ I2P cụ thể, và Complication đã làm rất tốt việc đào sâu tìm hiểu về vấn đề này. Dữ liệu đã có sẵn, vì vậy bạn có thể tự đưa ra nhận định. [10]

Cảm ơn Complication vì tất cả những nghiên cứu bạn đã thực hiện về việc này!

[10] http://forum.i2p.net/viewtopic.php?t=1122

* 7) ???

Nhiều chuyện đang diễn ra lắm, như bạn thấy đấy, nhưng vì tôi đã trễ cuộc họp rồi, có lẽ tôi nên lưu lại cái này và gửi đi, nhỉ? Hẹn gặp bạn ở #i2p :)

=jr
