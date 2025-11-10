---
title: "Ghi chú trạng thái I2P cho ngày 2005-02-08"
date: 2005-02-08
author: "jr"
description: "Ghi chú trạng thái phát triển I2P hàng tuần bao gồm các cập nhật 0.4.2.6, tiến độ tunnel 0.5 với bộ lọc Bloom, i2p-bt 0.1.6 và Fortuna PRNG (bộ sinh số ngẫu nhiên giả Fortuna)"
categories: ["status"]
---

Chào mọi người, lại đến giờ cập nhật rồi

* Index

1) 0.4.2.6-* 2) 0.5 3) i2p-bt 0.1.6 4) fortuna 5) ???

* 1) 0.4.2.6-*

Nghe có vẻ không như vậy, nhưng đã hơn một tháng kể từ khi bản phát hành 0.4.2.6 ra mắt và mọi thứ vẫn khá ổn định. Kể từ đó đã có một loạt cập nhật khá hữu ích [1], nhưng chưa có vấn đề “show stopper” nào buộc phải tung ra bản phát hành mới. Tuy vậy, trong một hai ngày vừa rồi chúng tôi nhận được vài bản sửa lỗi rất tốt (cảm ơn anon và Sugadude!), và nếu không đang ở ngưỡng ra mắt bản 0.5, có lẽ tôi đã đóng gói và phát hành luôn rồi. Bản cập nhật của anon sửa một điều kiện biên trong streaming lib (thư viện truyền phát), vốn gây ra nhiều lỗi hết thời gian chờ khi dùng BT và các phiên truyền dữ liệu lớn khác, vậy nên nếu bạn thấy hứng thú mạo hiểm, hãy lấy CVS HEAD và thử luôn. Hoặc tất nhiên là cứ chờ bản phát hành tiếp theo.

[1] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/history.txt?rev=HEAD

* 2) 0.5

Rất nhiều tiến triển đối với phiên bản 0.5 (như bất kỳ ai trên danh sách gửi thư i2p-cvs [2] cũng có thể xác nhận). Tất cả các cập nhật tunnel (đường hầm trong I2P) và các tinh chỉnh hiệu năng khác nhau đã được thử nghiệm, và dù nó không bao gồm nhiều [3] thuật toán đảm bảo thứ tự, nó vẫn bao quát được những điều cơ bản. Chúng tôi cũng đã tích hợp một bộ (theo giấy phép BSD) bộ lọc Bloom [4] từ XLattice [5], cho phép chúng tôi phát hiện các cuộc tấn công replay mà không cần bất kỳ mức sử dụng bộ nhớ trên mỗi thông điệp nào và overhead gần 0ms. Để đáp ứng nhu cầu của chúng tôi, các bộ lọc đã được mở rộng một cách đơn giản để tự suy giảm theo thời gian, để sau khi một tunnel hết hạn, bộ lọc không còn chứa các IV (vector khởi tạo) mà chúng tôi đã thấy trong tunnel đó nữa.

Trong khi tôi đang cố gắng đưa vào càng nhiều thứ càng tốt cho bản phát hành 0.5, tôi cũng nhận ra rằng chúng ta cần phải chuẩn bị cho những điều không lường trước được - nghĩa là cách tốt nhất để cải thiện nó là đưa nó đến tay bạn và học hỏi từ cách nó hoạt động (và không hoạt động) đối với bạn. Để hỗ trợ việc này, như tôi đã đề cập trước đây, chúng ta sẽ có một bản phát hành 0.5 (hy vọng sẽ ra mắt trong tuần tới), phá vỡ khả năng tương thích ngược, rồi từ đó tiếp tục cải thiện, xây dựng bản 0.5.1 khi nó sẵn sàng.

Nhìn lại lộ trình [6], thứ duy nhất bị hoãn sang 0.5.1 là thứ tự nghiêm ngặt. Cũng sẽ có những cải tiến đối với throttling (điều tiết lưu lượng) và cân bằng tải theo thời gian, tôi chắc chắn, nhưng tôi dự đoán chúng ta sẽ còn phải tinh chỉnh những thứ đó gần như mãi mãi. Tuy vậy, cũng có một số thứ khác đã được bàn luận mà tôi hy vọng sẽ đưa vào 0.5, như công cụ tải xuống và mã cập nhật một nhấp chuột, nhưng có vẻ như những thứ đó cũng sẽ bị hoãn lại.

[2] http://dev.i2p.net/pipermail/i2p-cvs/2005-February/thread.html [3] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/                     tunnel-alt.html?rev=HEAD#tunnel.selection.client [4] http://en.wikipedia.org/wiki/Bloom_filter [5] http://xlattice.sourceforge.net/index.html [6] http://www.i2p.net/roadmap

* 3) i2p-bt 0.1.6

duck vừa vá và phát hành một bản i2p-bt mới (yay!), có sẵn ở các địa chỉ quen thuộc, nên hãy tải ngay khi còn nóng hổi [7]. Với bản cập nhật này và bản vá thư viện streaming của anon, tôi gần như đã bão hòa băng thông tải lên của mình khi seed một vài tệp, nên hãy thử đi.

[7] http://forum.i2p.net/viewtopic.php?t=300

* 4) fortuna

Như đã đề cập trong cuộc họp tuần trước, smeghead đã miệt mài xử lý hàng loạt bản cập nhật khác nhau gần đây, và trong khi vật lộn để khiến I2P chạy được với gcj, một số vấn đề PRNG (bộ tạo số ngẫu nhiên giả) cực kỳ khủng khiếp đã xuất hiện trong một số JVM (máy ảo Java), về cơ bản buộc chúng ta phải có một PRNG mà mình có thể tin cậy. Sau khi nhận phản hồi từ nhóm GNU-Crypto, dù bản triển khai fortuna của họ vẫn chưa thật sự được đưa vào sử dụng, nó có vẻ phù hợp nhất với nhu cầu của chúng ta. Chúng ta có thể kịp đưa nó vào bản phát hành 0.5, nhưng nhiều khả năng nó sẽ bị hoãn sang 0.5.1, vì chúng ta muốn tinh chỉnh để nó có thể cung cấp lượng dữ liệu ngẫu nhiên cần thiết.

* 5) ???

Rất nhiều thứ đang diễn ra, và gần đây trên diễn đàn [8] cũng có một đợt bùng nổ hoạt động, nên tôi chắc là mình đã bỏ lỡ vài thứ. Dù sao thì, vài phút nữa ghé qua buổi họp và chia sẻ điều bạn đang nghĩ (hoặc cứ im lặng theo dõi và thỉnh thoảng xen vào vài câu mỉa mai bất chợt).

=jr [8] http://forum.i2p.net/
