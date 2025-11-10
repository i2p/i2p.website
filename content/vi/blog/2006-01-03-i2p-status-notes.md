---
title: "Ghi chú trạng thái I2P cho ngày 2006-01-03"
date: 2006-01-03
author: "jr"
description: "Cập nhật năm mới bao gồm tính ổn định của bản phát hành 0.6.1.8, kết quả kiểm thử tải và peer profiling (lập hồ sơ peer) nhằm tối ưu hóa thông lượng, và tổng kết toàn diện năm 2005 kèm xem trước lộ trình 2006"
categories: ["status"]
---

Chào mọi người, chúc mừng năm mới! Hãy cùng quay lại với các ghi chú trạng thái hằng tuần sau một tuần không có chúng -

* Index

1) Trạng thái mạng và 0.6.1.8 2) Kết quả kiểm thử tải và lập hồ sơ nút ngang hàng (peer) 3) Tổng kết 2005 / Dự báo 2006 / ???

* 1) Net status and 0.6.1.8

Tuần trước chúng tôi đã phát hành 0.6.1.8 và theo các báo cáo từ thực tế sử dụng thì những sửa đổi của zzz đã giúp ích khá nhiều, và mọi thứ có vẻ khá ổn định trên mạng, ngay cả khi lưu lượng mạng gần đây tăng đáng kể (giá trị trung bình dường như đã tăng gấp đôi trong tháng qua, theo stats.i2p). I2PSnark cũng có vẻ hoạt động khá tốt — dù có gặp một vài trục trặc, chúng tôi đã lần ra và sửa hầu hết trong các bản dựng sau đó. Chưa có nhiều phản hồi về giao diện blog mới của Syndie, nhưng lưu lượng Syndie có tăng nhẹ (một phần là do protocol phát hiện ra trình nhập rss/atom của dust :)

* 2) Load testing results and peer profiling

Trong vài tuần qua, tôi đã cố gắng khoanh vùng nút thắt cổ chai về thông lượng của chúng tôi. Các thành phần phần mềm khác nhau đều có khả năng đẩy dữ liệu ở tốc độ cao hơn nhiều so với mức chúng ta thường thấy đối với truyền thông đầu-cuối qua I2P, vì vậy tôi đã đo hiệu năng chúng trên mạng thực bằng mã tùy chỉnh để kiểm thử chịu tải. Bộ thử nghiệm đầu tiên, xây dựng các tunnel (đường hầm) inbound một hop đi qua tất cả các router (thiết bị định tuyến) trong mạng và truyền dữ liệu qua tunnel đó ngay khi có thể, cho kết quả khá hứa hẹn, với các router xử lý tốc độ xấp xỉ mức mà ta kỳ vọng chúng có thể đạt được (ví dụ đa số chỉ xử lý trung bình trong suốt thời gian hoạt động 4–16KBps, nhưng một số khác đẩy được 20–120KBps qua một tunnel duy nhất). Bài kiểm tra này là một điểm chuẩn cơ sở tốt cho việc khảo sát thêm và cho thấy bản thân quá trình xử lý tunnel có khả năng đẩy nhiều hơn đáng kể so với những gì chúng ta thường thấy.

Những nỗ lực tái lập các kết quả đó qua các tunnels (đường hầm I2P) đang hoạt động thì không thành công bằng. Hoặc, có lẽ bạn có thể nói là chúng còn thành công hơn, vì chúng cho thấy thông lượng tương tự những gì chúng ta hiện đang thấy, nghĩa là chúng ta đã đi đúng hướng. Quay lại các kết quả kiểm thử 1hop, tôi đã sửa đổi mã để chọn các peers (nút đồng đẳng) mà tôi tự tay xác định là nhanh và chạy lại các bài kiểm thử tải qua các tunnels đang hoạt động với cách chọn "cheating" peer này, và dù không đạt đến mốc 120KBps, nó vẫn cho thấy một mức cải thiện hợp lý.

Thật không may, việc yêu cầu mọi người tự chọn thủ công các peers (nút ngang hàng) của họ gây ra những vấn đề nghiêm trọng cho cả tính ẩn danh và, nói thẳng ra, tính dễ sử dụng, nhưng với dữ liệu kiểm thử tải trong tay, dường như có một lối thoát. Vài ngày gần đây tôi đã thử nghiệm một phương pháp mới để lập hồ sơ hiệu năng các peers theo tốc độ của họ - về cơ bản là theo dõi thông lượng tối đa duy trì, thay vì độ trễ gần đây. Các triển khai đơn giản đã khá thành công, và mặc dù nó không chọn đúng y các peers mà tôi sẽ chọn thủ công, nó vẫn làm khá tốt. Tuy vậy, vẫn còn vài trục trặc cần xử lý, chẳng hạn như bảo đảm chúng ta có thể thăng hạng các tunnels thăm dò lên tầng nhanh, nhưng hiện tôi đang thử một vài thí nghiệm ở khía cạnh đó.

Nhìn chung, tôi nghĩ chúng ta đang tiến gần đến cuối của đợt tối ưu hóa thông lượng này, vì chúng ta đang dồn ép vào nút thắt cổ chai nhỏ nhất và làm nó rộng ra. Tôi chắc chắn chúng ta sẽ sớm gặp nút thắt tiếp theo, và điều này chắc chắn sẽ không giúp chúng ta đạt được tốc độ Internet thông thường, nhưng nó sẽ giúp ích phần nào.

* 3) 2005 review / 2006 preview / ???

Nói rằng năm 2005 đã có nhiều đột phá thì vẫn còn là nói giảm — trong 25 bản phát hành năm ngoái, chúng tôi đã cải tiến I2P theo nhiều cách, tăng quy mô mạng lên gấp 5 lần, triển khai một số ứng dụng khách mới (Syndie, I2Phex, I2PSnark, I2PRufus), chuyển sang mạng IRC irc2p mới của postman và cervantes, và chứng kiến một số eepsites(I2P Sites) hữu ích nở rộ (chẳng hạn stats.i2p của zzz, orion.i2p của orion, và các dịch vụ proxy và giám sát của tino, để kể vài ví dụ). Cộng đồng cũng đã trưởng thành hơn đôi chút, phần không nhỏ nhờ các nỗ lực hỗ trợ của Complication và những người khác trên diễn đàn và trong các kênh, và chất lượng cũng như sự đa dạng của các báo cáo lỗi từ mọi phía đã được cải thiện đáng kể. Sự hỗ trợ tài chính liên tục từ những người trong cộng đồng thật ấn tượng, và dù vẫn chưa đạt đến mức cần thiết cho phát triển hoàn toàn bền vững, chúng tôi vẫn có một khoản đệm tài chính đủ để nuôi tôi qua mùa đông.

Xin cảm ơn tất cả những ai đã tham gia trong năm vừa qua, dù về mặt kỹ thuật, xã hội hay tài chính, vì sự giúp đỡ của mọi người!

Năm 2006 sẽ là một năm quan trọng đối với chúng tôi, với 0.6.2 ra mắt vào mùa đông này, dự kiến phát hành 1.0 vào khoảng mùa xuân hoặc mùa hè, và 2.0 vào mùa thu, nếu không sớm hơn. Đây là năm chúng ta sẽ thấy mình có thể làm được những gì, và công việc ở lớp ứng dụng sẽ còn quan trọng hơn trước. Vì vậy, nếu bạn có vài ý tưởng, bây giờ là lúc bắt tay vào việc ngay :)

Dù sao thì, cuộc họp cập nhật tình hình hàng tuần của chúng tôi sẽ diễn ra trong vài phút nữa, nên nếu bạn còn điều gì muốn thảo luận thêm, hãy ghé qua #i2p ở những địa điểm quen thuộc [1] và chào một tiếng!

=jr [1] http://forum.i2p.net/viewtopic.php?t=952
