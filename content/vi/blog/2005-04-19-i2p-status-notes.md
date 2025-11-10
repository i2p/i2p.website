---
title: "Ghi chú trạng thái I2P ngày 2005-04-19"
date: 2005-04-19
author: "jr"
description: "Bản cập nhật hàng tuần đề cập đến các sửa lỗi sắp tới cho 0.5.0.7, tiến độ của SSU (giao thức truyền tải UDP), các thay đổi lộ trình dời 0.6 sang tháng Sáu, và tiến độ phát triển Q"
categories: ["status"]
---

Chào mọi người, lại đến hẹn hàng tuần rồi,

* Index

1) Trạng thái mạng 2) Trạng thái SSU 3) Cập nhật lộ trình 4) Trạng thái Q 5) ???

* 1) Net status

Trong gần hai tuần kể từ khi 0.5.0.6 được phát hành, mọi thứ nhìn chung là tích cực, dù các nhà cung cấp dịch vụ (eepsites(I2P Sites), ircd, v.v.) gần đây đã gặp phải một số lỗi. Mặc dù các máy khách đang hoạt động tốt, theo thời gian máy chủ có thể rơi vào tình huống mà các tunnels bị lỗi kích hoạt một số mã giới hạn tốc độ quá mức, ngăn cản việc tái xây dựng và công bố leaseSet một cách đúng đắn.

Đã có một số sửa lỗi trong CVS, cùng với các thay đổi khác, và tôi kỳ vọng chúng ta sẽ phát hành bản 0.5.0.7 mới trong khoảng một hai ngày tới.

* 2) SSU status

Đối với những ai không theo dõi blog (rất chi là thú vị) của tôi, đã có rất nhiều tiến triển với UDP transport (cơ chế truyền tải UDP), và hiện giờ có thể khá yên tâm mà nói rằng UDP transport sẽ không là nút thắt cổ chai về thông lượng của chúng ta :) Trong khi gỡ lỗi phần mã đó, tôi đã tranh thủ rà soát cả việc xử lý hàng đợi ở các tầng cao hơn, tìm ra những điểm có thể loại bỏ các điểm nghẽn không cần thiết. Tuy nhiên, như tôi đã nói tuần trước, vẫn còn rất nhiều việc phải làm. Sẽ có thêm thông tin khi có thêm thông tin.

* 3) Roadmap update

Bây giờ là tháng Tư, nên lộ trình [1] đã được cập nhật tương ứng - bỏ 0.5.1 và điều chỉnh một số mốc thời gian. Thay đổi lớn nhất là dời 0.6 từ tháng Tư sang tháng Sáu, dù thực ra không lớn như nhìn có vẻ. Như tôi đã đề cập tuần trước, lịch cá nhân của tôi đã thay đổi đôi chút, và thay vì chuyển đến $somewhere vào tháng Sáu, tôi sẽ chuyển đến $somewhere vào tháng Năm. Mặc dù chúng tôi có thể chuẩn bị xong những gì cần thiết cho 0.6 trong tháng này, tôi sẽ không đời nào phát hành gấp một bản cập nhật lớn như vậy rồi biến mất một tháng, vì thực tế của phần mềm là sẽ luôn có lỗi không bị phát hiện trong quá trình kiểm thử.

[1] http://www.i2p.net/roadmap

* 4) Q status

Aum đã làm việc rất tích cực trên Q, bổ sung thêm nhiều tính năng hay ho cho chúng ta, với các ảnh chụp màn hình mới nhất đã được đăng trên trang web của anh ấy [2]. Anh ấy cũng đã commit mã nguồn lên CVS (tuyệt!), vì vậy hy vọng chúng ta sẽ sớm có thể bắt đầu thử nghiệm alpha. Tôi chắc rằng chúng ta sẽ còn nghe thêm từ aum với chi tiết về cách hỗ trợ, hoặc bạn có thể tự đào sâu vào những thứ hay ho trong CVS tại i2p/apps/q/

[2] http://aum.i2p/q/

* 5) ???

Cũng còn nhiều điều khác đang diễn ra, với một số cuộc thảo luận sôi nổi trên danh sách gửi thư, diễn đàn và irc. Tôi sẽ không cố gắng tóm tắt những điều đó ở đây, vì chỉ còn vài phút nữa là đến cuộc họp, nhưng hãy ghé qua nếu có điều gì chưa được thảo luận mà bạn muốn nêu ra!

=jr
