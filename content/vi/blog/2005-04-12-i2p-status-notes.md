---
title: "Ghi chú trạng thái I2P ngày 2005-04-12"
date: 2005-04-12
author: "jr"
description: "Cập nhật hàng tuần bao gồm các sửa lỗi netDb phiên bản 0.5.0.6, tiến độ của lớp truyền tải UDP SSU, kết quả lập hồ sơ peer theo Bayes, và tình hình phát triển Q"
categories: ["status"]
---

Chào mọi người, lại đến lúc cập nhật rồi

* Index

1) Trạng thái mạng 2) Trạng thái SSU 3) Lập hồ sơ peer (nút đồng đẳng) theo Bayes 4) Trạng thái Q 5) ???

* 1) Net status

Bản phát hành 0.5.0.6 tuần trước có vẻ đã khắc phục các vấn đề netDb mà chúng tôi đang gặp (hoan hô). Các trang và dịch vụ đáng tin cậy hơn nhiều so với 0.5.0.5, tuy nhiên đã có một số báo cáo về sự cố khi một trang hoặc dịch vụ trở nên không thể truy cập sau vài ngày hoạt động.

* 2) SSU status

Đã có nhiều tiến triển đối với phần mã UDP của phiên bản 0.6, với loạt commit đầu tiên đã được đưa vào CVS. Chưa phải là thứ bạn có thể sử dụng ngay, nhưng các thành phần cơ bản đã sẵn sàng. Quá trình thương lượng phiên hoạt động tốt và cơ chế truyền tải thông điệp bán tin cậy hoạt động như kỳ vọng. Tuy vẫn còn rất nhiều việc phải làm, như viết các trường hợp kiểm thử và gỡ lỗi những tình huống bất thường, nhưng đó vẫn là tiến triển.

Nếu mọi việc suôn sẻ, chúng tôi có thể có một số thử nghiệm alpha vào tuần sau, chỉ dành cho những người có thể cấu hình rõ ràng tường lửa/NAT của họ. Tôi muốn hoàn thiện hoạt động tổng thể trước, rồi mới bổ sung trình xử lý relay (nút chuyển tiếp), tinh chỉnh netDb để routerInfo hết hạn nhanh hơn, và chọn các relay làm nơi công bố. Tôi cũng sẽ nhân cơ hội này thực hiện một loạt các kiểm thử, vì chúng tôi đang giải quyết một số yếu tố hàng đợi quan trọng.

* 3) Bayesian peer profiling

bla đã miệt mài thực hiện một số sửa đổi về cách chúng ta quyết định tunnel qua các nút ngang hàng nào, và dù bla không thể tham dự cuộc họp, vẫn có một số dữ liệu thú vị để báo cáo:

<+bla> Tôi đã thực hiện đo trực tiếp tốc độ của nút: Tôi đã lập hồ sơ        khoảng 150 nút bằng cách dùng OB tunnels có độ dài 0, IB tunnels        có độ dài 1, batching-interval = 0ms
<+bla> Ngoài ra, tôi vừa làm một ước lượng tốc độ _rất_ cơ bản và        _sơ bộ_ bằng phân loại Bayes ngây thơ
<+bla> Cái sau được thực hiện với độ dài expl. tunnels mặc định
<+bla> Giao của tập các nút mà tôi có "giá trị thực (ground truth)", và tập các nút trong các phép đo hiện tại, là 117 nút
<+bla> Kết quả không _đến nỗi_ tệ, nhưng cũng không quá ấn tượng
<+bla> Xem http://theland.i2p/estspeed.png
<+bla> Phân tách cơ bản giữa rất chậm/nhanh thì tạm ổn, nhưng phân tách        chi tiết giữa các nút nhanh hơn còn có thể tốt hơn nhiều
<+jrandom2p> hmm, các giá trị thực được tính như thế nào - đó là              RTT (thời gian khứ hồi) đầy đủ hay là RTT/chiều dài ?
<+bla> Dùng expl. tunnels thông thường thì gần như không thể        tránh độ trễ do batching.
<+bla> Các giá trị thực là các giá trị ground-truth: những giá trị thu được        khi dùng OB=0 và IB=1
<+bla> (và variance=0, và không có độ trễ do batching)
<+jrandom2p> tuy vậy, từ đây nhìn thì kết quả khá ổn
<+bla> Các thời gian ước tính là các giá trị thu được bằng suy luận        Bayes từ expl. tunnels thực có độ dài 2 +/- 1
<+bla> Điều này được lấy từ 3000 RTT, ghi lại trong khoảng        3 giờ (khá dài)
<+bla> Giả định (tạm thời) rằng tốc độ của nút là tĩnh.        Tôi vẫn chưa triển khai trọng số
<+jrandom2p> nghe tuyệt vời.  làm tốt lắm bla
<+jrandom2p> hmm, vậy ước tính sẽ bằng 1/4 giá trị thực
<+bla> jrandom: Không: Tất cả các RTT đo được (dùng expl.        tunnels thông thường), đều được hiệu chỉnh theo số hop trong        vòng khứ hồi
<+jrandom2p> à ok
<+bla> Chỉ sau đó, bộ phân loại Bayes mới được huấn luyện
<+bla> Hiện tại, tôi phân nhóm thời gian mỗi hop đo được thành 10 lớp:        50, 100, ..., 450 ms, và thêm một lớp >500 ms
<+bla> Ví dụ, các độ trễ mỗi hop nhỏ có thể được gán trọng số lớn hơn,        cũng như các lỗi hoàn toàn (>60000 ms).
<+bla> Mặc dù.... 65% thời gian ước tính nằm trong 0.5        độ lệch chuẩn so với thời gian thực của nút
<+bla> Tuy nhiên, điều này cần được làm lại, vì độ lệch chuẩn        bị ảnh hưởng mạnh bởi các lỗi >60000 ms

Sau khi thảo luận thêm, bla đã đưa ra một so sánh đối chiếu với công cụ tính tốc độ hiện có, được đăng @ http://theland.i2p/oldspeed.png Các bản sao (mirror) của những tệp PNG đó có tại http://dev.i2p.net/~jrandom/estspeed.png và http://dev.i2p.net/~jrandom/oldspeed.png

(về thuật ngữ, IB=số hop (chặng) của inbound tunnel, OB=số hop của outbound tunnel, và sau khi làm rõ, các phép đo "ground truth" được thực hiện với 1 hop outbound và 0 hop inbound, chứ không phải ngược lại)

* 4) Q status

Aum cũng đã đạt được rất nhiều tiến triển với Q, gần đây nhất là làm việc trên một giao diện client trên nền web. Bản build Q tiếp theo sẽ không tương thích ngược, vì nó bao gồm một loạt tính năng mới, nhưng tôi chắc rằng chúng ta sẽ nghe thêm thông tin từ Aum khi có thêm thông tin để chia sẻ :)

* 5) ???

Tạm thời vậy thôi (phải chốt lại trước giờ họp). À, nhân tiện, có vẻ tôi sẽ chuyển nhà sớm hơn dự định, nên có thể một số mốc thời gian trong lộ trình sẽ bị dịch chuyển trong lúc tôi đang di chuyển đến nơi cuối cùng tôi đến. Dù sao, tạt qua kênh trong vài phút nữa để quấy rầy chúng tôi bằng những ý tưởng mới nhé!

=jr
