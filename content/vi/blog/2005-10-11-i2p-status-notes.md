---
title: "Ghi chú trạng thái I2P ngày 2005-10-11"
date: 2005-10-11
author: "jr"
description: "Bản cập nhật hàng tuần đề cập đến thành công của bản phát hành 0.6.1.2, proxy I2PTunnelIRCClient mới để lọc các tin nhắn IRC không an toàn, Syndie CLI và chuyển đổi RSS sang SML, và kế hoạch tích hợp I2Phex"
categories: ["status"]
---

Chào mọi người, lại là thứ Ba rồi

* Index

1) 0.6.1.2 2) I2PTunnelIRCClient 3) Syndie 4) I2Phex 5) Giấu tin và mạng tối (re: cuộc khẩu chiến) 6) ???

* 1) 0.6.1.2

Bản phát hành 0.6.1.2 tuần trước đến giờ diễn ra khá suôn sẻ - 75% mạng lưới đã nâng cấp, HTTP POST hoạt động tốt, và streaming lib (thư viện truyền dữ liệu theo luồng) đang truyền dữ liệu khá hiệu quả (phản hồi đầy đủ cho một yêu cầu HTTP thường được nhận chỉ trong một vòng khứ hồi từ đầu đến cuối). Mạng lưới cũng đã tăng trưởng thêm một chút - con số ổn định vào khoảng 400 nút, dù đã bùng lên hơn nữa đến 6-700 với biến động trong giai đoạn cao điểm của lần được nhắc đến trên digg/gotroot [1] vào cuối tuần.

[1] http://gotroot.com/tiki-read_article.php?articleId=195     (ừ, bài viết rất cũ, tôi biết, nhưng ai đó lại tìm thấy nó)

Kể từ khi 0.6.1.2 ra mắt, đã có thêm nhiều cải tiến hữu ích được bổ sung — nguyên nhân của các netsplits trên irc2p (sự phân tách mạng trên IRC) gần đây đã được tìm ra (và khắc phục), cùng với một số cải tiến đáng kể đối với việc truyền gói tin của SSU (giúp tiết kiệm trên 5% số gói tin). Tôi chưa chắc 0.6.1.3 sẽ phát hành chính xác khi nào, nhưng có lẽ trong tuần này. Hãy chờ xem.

* 2) I2PTunnelIRCClient

Mới đây, sau một vài cuộc thảo luận, dust đã nhanh chóng tạo ra một phần mở rộng mới cho I2PTunnel - proxy "ircclient". Nó hoạt động bằng cách lọc nội dung được gửi và nhận giữa máy khách và máy chủ qua I2P, loại bỏ các thông điệp IRC không an toàn và viết lại những thông điệp cần được điều chỉnh. Sau một thời gian thử nghiệm, nó hoạt động khá tốt, và dust đã đóng góp nó vào I2PTunnel và hiện nó được cung cấp cho mọi người qua giao diện web. Thật tuyệt khi những người irc2p đã vá các máy chủ IRC của họ để loại bỏ các thông điệp không an toàn, nhưng giờ đây chúng ta không còn phải trông cậy họ làm việc đó nữa - người dùng cục bộ có quyền kiểm soát việc lọc của riêng mình.

Việc sử dụng khá đơn giản - thay vì tạo một "Client proxy" cho IRC như trước, chỉ cần tạo một "IRC proxy". Nếu bạn muốn chuyển đổi "Client proxy" hiện có của mình thành "IRC proxy", bạn có thể (dù hơi vụng về) chỉnh sửa tệp i2ptunnel.config, thay "tunnel.1.type=client" thành "tunnel.1.ircclient" (hoặc bất kỳ số nào phù hợp với proxy của bạn).

Nếu mọi việc suôn sẻ, điều này sẽ trở thành kiểu proxy I2PTunnel mặc định cho các kết nối IRC trong bản phát hành tiếp theo.

Làm tốt lắm dust, cảm ơn!

* 3) Syndie

Tính năng phát hành theo lịch của Ragnarok có vẻ đang hoạt động tốt, và kể từ khi 0.6.1.2 ra mắt, đã có hai tính năng mới được giới thiệu - tôi đã bổ sung một CLI đơn giản hóa (giao diện dòng lệnh) để đăng lên Syndie [2], và dust (hoan hô dust!) đã nhanh chóng viết một ít mã để trích xuất nội dung từ một nguồn cấp RSS/Atom, tải về mọi tệp đính kèm hoặc hình ảnh được tham chiếu trong đó, và chuyển đổi nội dung RSS sang SML (!!!) [3][4].

Hàm ý của hai điều này khi xét cùng nhau đã rõ ràng. Sẽ có thêm tin tức khi có thêm tin tức.

[2] http://syndiemedia.i2p/index.jsp?blog=ovpBy2mpO1CQ7deYhQ1cDGAwI6pQzLbWOm1Sdd0W06c=&entry=1128816000000&expand=true [3] http://syndiemedia.i2p/index.jsp?blog=ovpBy2mpO1CQ7deYhQ1cDGAwI6pQzLbWOm1Sdd0W06c=&entry=1128816000001&expand=true [4] http://dust.i2p/Sucker.java     (chúng tôi sẽ tích hợp nó vào CVS sớm thôi)

* 4) I2Phex

Nghe nói I2Phex hoạt động khá ổn, nhưng về lâu dài vẫn còn một số vấn đề tồn tại. Đã có một số thảo luận trên diễn đàn [5] về cách tiến hành, và GregorK, nhà phát triển chủ chốt của Phex, thậm chí đã lên tiếng bày tỏ ủng hộ việc tích hợp lại chức năng của I2Phex vào Phex (hoặc ít nhất để Phex nhánh chính cung cấp một giao diện plugin đơn giản cho tầng vận chuyển).

Điều này sẽ thực sự rất tuyệt, vì nó sẽ đồng nghĩa với việc có ít mã cần bảo trì hơn nhiều, cộng thêm chúng ta còn được hưởng lợi từ công sức của đội Phex trong việc cải thiện codebase (nền mã nguồn). Tuy vậy, để việc này khả thi, chúng ta cần một vài hacker đứng ra đảm nhận việc chuyển đổi. Mã của I2Phex thể hiện khá rõ những chỗ sirup đã thay đổi, nên chắc là sẽ không quá khó, nhưng có lẽ cũng không hề đơn giản đâu ;)

Hiện tại tôi không thật sự có thời gian để bắt tay vào việc này, nhưng hãy ghé qua diễn đàn nếu bạn muốn giúp.

[5] http://forum.i2p.net/viewforum.php?f=25

* 5) Stego and darknets (re: flamewar)

Danh sách thư [6] gần đây hoạt động khá sôi nổi với các thảo luận liên quan đến steganography (kỹ thuật giấu tin) và darknets (mạng tối). Chủ đề này phần lớn đã chuyển sang danh sách kỹ thuật của Freenet [7] với tiêu đề "I2P conspiracy theories flamewar", nhưng vẫn đang tiếp diễn.

Tôi không chắc mình có nhiều điều để bổ sung ngoài những gì đã có trong chính các bài viết, nhưng một số người cho biết phần thảo luận đã giúp họ hiểu về I2P và Freenet rõ hơn, nên có lẽ cũng đáng xem qua. Hoặc cũng có thể không ;)

[6] http://dev.i2p.net/pipermail/i2p/2005-October/thread.html [7] nttp://news.gmane.org/gmane.network.freenet.technical

* 6) ???

Như bạn thấy đấy, có rất nhiều thứ thú vị đang diễn ra, và tôi chắc là mình đã bỏ sót vài điều. Ghé qua #i2p trong vài phút nữa để tham gia buổi họp hàng tuần của chúng tôi và chào một tiếng nhé!

=jr
