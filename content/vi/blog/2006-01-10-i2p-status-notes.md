---
title: "Ghi chú trạng thái I2P cho ngày 2006-01-10"
date: 2006-01-10
author: "jr"
description: "Bản cập nhật hàng tuần đề cập đến các thuật toán lập hồ sơ thông lượng, các cải tiến cho chế độ xem blog của Syndie, tiến triển về kết nối HTTP giữ sống (persistent connections), và phát triển gwebcache cho I2Phex"
categories: ["status"]
---

Chào mọi người, hình như thứ Ba lại tới rồi

* Index

1) Tình trạng mạng 2) Lập hồ sơ thông lượng 3) Các blog Syndie 4) Kết nối HTTP persistent (duy trì) 5) I2Phex gwebcache 6) ???

* 1) Net status

Tuần vừa qua đã có rất nhiều bản sửa lỗi và cải tiến được đưa vào CVS, với bản build hiện tại là 0.6.1.8-11. Mạng đã tương đối ổn định, dù một vài lần ngừng dịch vụ tại các nhà cung cấp dịch vụ i2p khác nhau đã dẫn tới đôi chút trục trặc lẻ tẻ. Cuối cùng chúng tôi đã loại bỏ được tình trạng churn (thay đổi liên tục) danh tính router quá mức cần thiết trong CVS, và có một bản sửa lỗi mới cho phần lõi do zzz đưa ra hôm qua nghe khá hứa hẹn, nhưng chúng ta sẽ phải chờ xem nó ảnh hưởng như thế nào. Hai điểm lớn khác trong tuần qua là cơ chế lập hồ sơ tốc độ dựa trên thông lượng mới và một số công việc lớn trên chế độ xem blog của Syndie. Về thời điểm 0.6.1.9, nó dự kiến sẽ phát hành trong tuần này, muộn nhất là vào cuối tuần. Hãy theo dõi các kênh quen thuộc.

* 2) Throughput profiling

Chúng tôi đã thử nghiệm một vài thuật toán lập hồ sơ peer (nút ngang hàng) mới để giám sát thông lượng, nhưng trong khoảng một tuần trở lại đây, chúng tôi có vẻ đã thống nhất chọn được một thuật toán khá tốt. Về bản chất, nó theo dõi thông lượng đã được xác nhận của từng tunnel trong các khoảng thời gian 1 phút, và điều chỉnh các ước lượng thông lượng cho các peer tương ứng. Nó không cố gắng tính ra tốc độ trung bình cho một peer, vì làm như vậy rất phức tạp, do các tunnel bao gồm nhiều peer, cũng như việc đo thông lượng đã được xác nhận thường đòi hỏi nhiều tunnel. Thay vào đó, nó tính ra tốc độ đỉnh trung bình - cụ thể, nó đo ba tốc độ nhanh nhất mà các tunnel của peer có thể truyền tải và lấy trung bình các giá trị đó.

Tóm lại, vì các tốc độ này được đo trong trọn một phút, chúng phản ánh tốc độ duy trì mà peer (nút đồng cấp) có thể đẩy, và vì mỗi peer ít nhất cũng nhanh bằng tốc độ đo được từ đầu đến cuối, nên có thể yên tâm đánh dấu từng peer là đạt tốc độ đó. Chúng tôi đã thử một biến thể khác — đo thông lượng tổng thể của một peer qua các tunnels trong những khoảng thời gian khác nhau; cách đó cung cấp thông tin về tốc độ đỉnh còn rõ ràng hơn, nhưng lại thiên lệch mạnh bất lợi cho các peer chưa được đánh dấu là "fast", vì các peer "fast" được sử dụng thường xuyên hơn rất nhiều (các client tunnels chỉ sử dụng các peer "fast"). Kết quả của phép đo thông lượng tổng thể đó là nó thu thập được dữ liệu rất tốt cho những peer bị đặt dưới tải đủ mức, nhưng chỉ các peer "fast" mới thực sự bị đặt dưới tải đủ mức và vì thế có rất ít sự thăm dò hiệu quả.

Tuy nhiên, việc sử dụng các khoảng thời gian 1 phút và thông lượng của một tunnel riêng lẻ dường như cho ra các giá trị hợp lý hơn. Chúng ta sẽ thấy thuật toán này được triển khai trong bản phát hành tiếp theo.

* 3) Syndie blogs

Dựa trên một số phản hồi, đã có thêm các cải tiến trong chế độ xem blog của Syndie, khiến nó mang một phong cách khác biệt rõ rệt so với giao diện dạng luồng (threaded) giống nhóm tin/diễn đàn. Ngoài ra, nó còn có một khả năng hoàn toàn mới để định nghĩa thông tin chung của blog thông qua kiến trúc Syndie hiện có. Ví dụ, hãy xem bài đăng blog mặc định "about Syndie":  http://syndiemedia.i2p.net/blog.jsp?blog=ovpBy2mpO1CQ7deYhQ1cDGAwI6pQzLbWOm1Sdd0W06c=&entry=ovpBy2mpO1CQ7deYhQ1cDGAwI6pQzLbWOm1Sdd0W06c=/1132012800001

Điều này mới chỉ là bước khởi đầu cho những gì chúng ta có thể làm. Bản phát hành tiếp theo sẽ cho phép bạn tự đặt logo cho blog của mình, các liên kết riêng (đến blog, bài đăng, tệp đính kèm, các URL bên ngoài tùy ý), và hy vọng còn có nhiều tùy biến hơn nữa. Một tùy biến như vậy là biểu tượng cho từng tag (thẻ) - tôi muốn cung cấp kèm một bộ biểu tượng mặc định để dùng với các tag chuẩn, nhưng mọi người sẽ có thể tự định nghĩa biểu tượng cho các tag riêng của họ để dùng trong blog của mình, và thậm chí ghi đè các biểu tượng mặc định cho các tag chuẩn (nhắc lại, dĩ nhiên là chỉ khi người khác đang xem blog của họ). Có lẽ còn có cả cấu hình style (kiểu hiển thị) để hiển thị các bài đăng với các tag khác nhau theo những cách khác nhau (dĩ nhiên, chỉ cho phép tùy biến style ở mức rất cụ thể - không có chuyện lợi dụng CSS tùy ý với Syndie đâu, xin cảm ơn rất nhiều :)

Vẫn còn rất nhiều điều tôi muốn làm với chế độ xem blog mà sẽ chưa có trong bản phát hành tiếp theo, nhưng chừng đó cũng đủ làm cú hích để mọi người bắt đầu dùng thử một số khả năng của nó, qua đó hy vọng mọi người có thể cho tôi thấy điều mà *các bạn* cần, thay vì điều tôi nghĩ là các bạn muốn. Tôi có thể là một lập trình viên giỏi, nhưng tôi không phải là nhà ngoại cảm.

* 4) HTTP persistent connections

zzz làm việc như điên, tôi nói thật đấy. Đã có một số tiến triển về một tính năng được yêu cầu từ lâu - hỗ trợ kết nối HTTP duy trì (persistent), cho phép bạn gửi nhiều yêu cầu HTTP qua một luồng duy nhất và nhận lại nhiều phản hồi. Tôi nghĩ ai đó đã yêu cầu điều này lần đầu cách đây khoảng hai năm, và nó có thể giúp ích cho một số loại eepsite (trang I2P) hoặc việc outproxy (truy cập Internet công khai qua proxy của I2P) khá nhiều. Tôi biết công việc vẫn chưa xong, nhưng đang tiến triển. Hy vọng zzz có thể cho chúng ta một bản cập nhật trạng thái trong cuộc họp.

* 5) I2Phex gwebcache

Tôi đã nghe có báo cáo về tiến triển trong việc đưa lại hỗ trợ gwebcache vào I2Phex, nhưng tôi không rõ tình hình hiện tại ra sao. Có lẽ tối nay Complication có thể cập nhật cho chúng ta về việc đó?

* 6) ???

Như mọi người thấy đấy, có khá nhiều thứ đang diễn ra, nhưng nếu còn điều gì mọi người muốn nêu ra và thảo luận, thì ghé buổi họp trong vài phút nữa và lên tiếng nhé. Nhân tiện, một trang hay mà dạo gần đây tôi theo dõi là http://freedomarchive.i2p/ (dành cho bạn nào lười chưa cài I2P, bạn có thể dùng inproxy (proxy truy cập eepsite từ Internet mở) của Tino qua http://freedomarchive.i2p.tin0.de/). Dù sao thì, hẹn gặp mọi người trong vài phút nữa.

=jr
