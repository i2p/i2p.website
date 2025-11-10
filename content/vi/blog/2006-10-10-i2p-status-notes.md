---
title: "Ghi chú trạng thái I2P cho ngày 2006-10-10"
date: 2006-10-10
author: "jr"
description: "Bản phát hành 0.6.1.26 với phản hồi tích cực, Syndie 0.910a đang tiến gần 1.0, và đánh giá hệ thống kiểm soát phiên bản phân tán cho Syndie"
categories: ["status"]
---

Chào mọi người, vài ghi chú tình hình ngắn gọn tuần này

* Index

1) 0.6.1.26 và tình trạng mạng 2) Tình trạng phát triển của Syndie 3) Xem lại hệ thống quản lý phiên bản phân tán 4) ???

* 1) 0.6.1.26 and network status

Mới đây chúng tôi đã phát hành bản 0.6.1.26 mới, bao gồm nhiều cải tiến i2psnark từ zzz và một số kiểm tra an toàn NTP mới từ Complication, và các phản hồi đều tích cực. Mạng có vẻ đang tăng trưởng nhẹ mà không có hiệu ứng lạ mới nào, dù một số người vẫn gặp khó khăn khi xây dựng tunnels của họ (vẫn như trước giờ).

* 2) Syndie development status

Ngày càng có nhiều cải tiến được đưa vào, với phiên bản alpha hiện tại đang ở 0.910a. Danh sách tính năng cho 1.0 hầu như đã hoàn tất, vì vậy hiện giờ chủ yếu là sửa lỗi và viết tài liệu. Ghé qua #i2p nếu bạn muốn giúp kiểm thử :)

Ngoài ra, trên kênh cũng đã có vài cuộc thảo luận về các thiết kế cho Syndie GUI - meerboop đã đưa ra một số ý tưởng rất hay và đang viết tài liệu cho chúng. Syndie GUI là thành phần chính của bản phát hành Syndie 2.0, vì vậy chúng ta khởi động việc đó càng sớm thì càng sớm có thể thống trị thế giớ^W^W^W^W tung Syndie ra cho quần chúng còn chưa hay biết.

Ngoài ra, tôi còn có một đề xuất mới trên blog Syndie của mình về việc theo dõi lỗi và yêu cầu tính năng bằng chính Syndie. Để tiện truy cập, tôi đã tạo một bản xuất dạng văn bản thuần (plain text) của bài viết đó và đưa lên web - trang 1 ở <http://dev.i2p.net/~jrandom/bugsp1.txt> và trang 2 ở <http://dev.i2p.net/~jrandom/bugsp2.txt>

* 3) Distributed version control revisited

Một trong những việc vẫn còn cần quyết định cho Syndie là hệ thống kiểm soát phiên bản công khai sẽ sử dụng, và như đã đề cập trước đây, cần có khả năng phân tán và hoạt động ngoại tuyến. Tôi đã xem qua chừng nửa tá hệ thống mã nguồn mở hiện có (darcs, mercurial, git/cogito, monotone, arch, bzr, codeville), đào sâu tài liệu của họ, dùng thử, và trao đổi với các nhà phát triển của họ. Hiện tại, monotone và bzr có vẻ tốt nhất về mặt chức năng và bảo mật (với các repository (kho lưu trữ) không đáng tin cậy, chúng ta cần mật mã mạnh để bảo đảm chỉ kéo về những thay đổi xác thực), và việc tích hợp mật mã chặt chẽ của monotone có vẻ rất hấp dẫn. Tuy nhiên, tôi vẫn đang đọc nốt vài trăm trang tài liệu, nhưng qua những gì tôi đã trao đổi với các nhà phát triển monotone, có vẻ họ đang làm mọi thứ Đúng cách.

Dĩ nhiên, bất kể cuối cùng chúng ta chọn DVCS (hệ thống quản lý phiên bản phân tán) nào, mọi bản phát hành sẽ được cung cấp dưới dạng tarball thuần, và các bản vá sẽ được chấp nhận để xem xét ở định dạng diff -uw thuần. Tuy vậy, đối với những ai có thể đang cân nhắc tham gia vào quá trình phát triển, tôi rất muốn nghe ý kiến và ưu tiên của bạn.

* 4) ???

Như bạn có thể thấy, như mọi khi, có rất nhiều thứ đang diễn ra. Cũng đã có thêm thảo luận trong chủ đề "solve world hunger" trên diễn đàn, vì vậy hãy xem tại <http://forum.i2p.net/viewtopic.php?t=1910>

Nếu bạn còn điều gì muốn thảo luận, hãy ghé qua #i2p để tham dự cuộc họp của các nhà phát triển tối nay, hoặc đăng lên diễn đàn hay danh sách thư (mailing list)!

=jr
