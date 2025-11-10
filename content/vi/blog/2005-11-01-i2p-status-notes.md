---
title: "Ghi chú trạng thái I2P cho ngày 2005-11-01"
date: 2005-11-01
author: "jr"
description: "Cập nhật hàng tuần bao gồm thành công của bản phát hành 0.6.1.4, phân tích tấn công bootstrap (khởi tạo), các bản sửa lỗi bảo mật cho I2Phex 0.1.1.34, phát triển ứng dụng thoại voi2p, và tích hợp nguồn cấp RSS của Syndie"
categories: ["status"]
---

Chào mọi người, đến hẹn lại lên.

* Index

1) 0.6.1.4 và trạng thái mạng 2) boostraps, tiền nhiệm, đối thủ thụ động toàn cục, và CBR 3) i2phex 0.1.1.34 4) ứng dụng voi2p 5) syndie và sucker 6) ???

* 1) 0.6.1.4 and net status

Bản phát hành 0.6.1.4 vào thứ Bảy vừa rồi có vẻ đã diễn ra khá suôn sẻ - 75% của mạng lưới đã nâng cấp rồi (cảm ơn!), và phần lớn số còn lại thì cũng đang ở 0.6.1.3. Mọi thứ có vẻ hoạt động tương đối ổn, và dù tôi chưa nghe được nhiều phản hồi về nó - dù tích cực hay tiêu cực, tôi đoán mọi người sẽ phàn nàn ầm ĩ nếu nó tệ :)

Đặc biệt, tôi rất muốn nhận được bất kỳ phản hồi nào từ những người dùng kết nối modem quay số, vì các thử nghiệm tôi đã thực hiện chỉ là một mô phỏng cơ bản của loại kết nối đó.

* 2) boostraps, predecessors, global passive adversaries, and CBR

Đã có nhiều thảo luận hơn trên mailing list về một vài ý tưởng, với bản tóm tắt về các cuộc tấn công bootstrap (khởi động) được đăng trực tuyến [1]. Tôi đã đạt được một số tiến triển trong việc xây dựng đặc tả cho phần mật mã của tùy chọn 3, và dù chưa có gì được đăng, nó khá đơn giản.

[1] http://dev.i2p.net/pipermail/i2p/2005-October/001146.html

Đã có thêm nhiều thảo luận về cách cải thiện khả năng chống chịu trước các đối thủ mạnh bằng các tunnels có tốc độ bit cố định (CBR), và mặc dù chúng tôi có thể theo đuổi hướng đi đó, hiện điều này được lên kế hoạch cho I2P 3.0, vì việc sử dụng đúng cách đòi hỏi nguồn lực đáng kể và có thể sẽ có tác động có thể đo lường được đến việc ai sẽ sẵn sàng sử dụng I2P với mức chi phí phụ trội (overhead) như vậy, cũng như những nhóm nào có hoặc thậm chí không thể sử dụng I2P.

* 3) I2Phex 0.1.1.34

Thứ Bảy vừa rồi, chúng tôi cũng phát hành một bản I2Phex mới [2], sửa lỗi rò rỉ bộ mô tả tệp mà về sau có thể khiến I2Phex ngừng hoạt động (cảm ơn Complication!) và loại bỏ một số đoạn mã vốn cho phép người khác điều khiển từ xa phiên bản I2Phex của bạn để tải xuống một số tệp cụ thể (cảm ơn GregorK!). Rất khuyến nghị nâng cấp.

Cũng đã có một bản cập nhật cho phiên bản CVS (chưa phát hành) nhằm khắc phục một số vấn đề đồng bộ — Phex giả định rằng một số hoạt động mạng được xử lý ngay lập tức, trong khi I2P đôi khi mất một lúc để thực hiện :) Điều này biểu hiện ở việc giao diện đồ họa (GUI) bị treo trong một thời gian, tải xuống hoặc tải lên bị đình trệ, hoặc kết nối bị từ chối (và có lẽ còn một vài cách khác). Nó vẫn chưa được kiểm thử nhiều, nhưng có lẽ sẽ được đưa vào bản 0.1.1.35 trong tuần này. Tôi chắc rằng sẽ có thêm thông tin được đăng trên diễn đàn khi có thêm cập nhật.

[2] http://forum.i2p.net/viewtopic.php?t=1143

* 4) voi2p app

Aum đang miệt mài phát triển ứng dụng thoại (và nhắn tin) qua I2P, và dù tôi chưa thấy nó, nghe có vẻ thú vị. Có lẽ Aum có thể cập nhật cho chúng ta trong cuộc họp, hoặc chúng ta có thể kiên nhẫn chờ bản phát hành alpha đầu tiên :)

* 5) syndie and sucker

dust đã miệt mài làm việc trên syndie và sucker, và bản dựng CVS mới nhất của I2P giờ cho phép bạn tự động lấy nội dung từ các nguồn cấp RSS và Atom và đăng chúng lên blog syndie của bạn. Hiện tại, bạn phải thêm thủ công lib/rome-0.7.jar and lib/jdom.jar vào wrapper.config (wrapper.java.classpath.20 and 21), nhưng chúng tôi sẽ đóng gói lại để về sau không còn cần thiết nữa. Nó vẫn đang trong quá trình hoàn thiện, và rome 0.8 (chưa phát hành) có vẻ sẽ mang đến một số tính năng rất hay, chẳng hạn khả năng lấy các enclosures (tệp đính kèm trong nguồn cấp) từ một nguồn cấp, mà sau đó sucker sẽ có thể nhập như một tệp đính kèm cho một bài đăng trên syndie (hiện giờ nó đã xử lý cả hình ảnh và liên kết rồi!).

Giống như mọi nguồn cấp RSS, dường như có một vài điểm không nhất quán trong cách nội dung được đưa vào, nên một số nguồn cấp được đưa vào trơn tru hơn những cái khác. Tôi nghĩ nếu mọi người giúp kiểm thử với các nguồn cấp khác nhau và báo cho dust biết về bất kỳ vấn đề nào khiến nó bị lỗi, thì có lẽ sẽ hữu ích. Dù sao thì, thứ này trông khá thú vị, làm tốt lắm, dust!

* 6) ???

Tạm thời vậy thôi, nhưng nếu ai có câu hỏi hoặc muốn thảo luận thêm, hãy ghé qua buổi họp lúc 8P GMT (nhớ là giờ mùa hè!).

=jr
