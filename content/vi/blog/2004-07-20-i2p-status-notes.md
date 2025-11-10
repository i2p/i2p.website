---
title: "Ghi chú trạng thái I2P cho ngày 2004-07-20"
date: 2004-07-20
author: "jr"
description: "Cập nhật tình hình hằng tuần bao gồm bản phát hành 0.3.2.3, thay đổi về năng lực, cập nhật trang web và các cân nhắc về bảo mật"
categories: ["status"]
---

**1) 0.3.2.3, 0.3.3, và lộ trình**

Sau khi phát hành 0.3.2.3 tuần trước, mọi người đã nâng cấp rất tốt - hiện chúng ta chỉ còn hai trường hợp chưa nâng cấp (một ở 0.3.2.2 và một còn tận 0.3.1.4 :).

Trong vài ngày qua, mạng đáng tin cậy hơn bình thường - mọi người ở trên irc.duck.i2p hàng giờ liền, các lượt tải xuống tệp lớn từ eepsites(I2P Sites) đều thành công, và khả năng truy cập eepsite(I2P Site) nói chung khá tốt. Vì mọi thứ đang diễn ra tốt đẹp và tôi muốn giữ mọi người luôn cảnh giác, tôi đã quyết định thay đổi một vài khái niệm cơ bản và chúng tôi sẽ triển khai chúng trong bản phát hành 0.3.3 trong một hai ngày tới.

Vì có vài người đã bình luận về lịch trình của chúng tôi, tự hỏi liệu chúng tôi có kịp các mốc thời gian đã đưa ra hay không, tôi quyết định có lẽ mình nên cập nhật trang web để phản ánh lộ trình tôi có trong palmpilot của mình, và tôi đã làm vậy [1]. Các mốc thời gian đã bị lùi và một số hạng mục đã được sắp xếp lại, nhưng kế hoạch vẫn giống như đã thảo luận hồi tháng trước [2].

0.4 sẽ đáp ứng bốn tiêu chí phát hành đã nêu (chức năng, an toàn, ẩn danh và khả năng mở rộng), tuy nhiên trước 0.4.2, rất ít người dùng ở sau NAT và tường lửa sẽ có thể tham gia, và trước 0.4.3 sẽ tồn tại một giới hạn trên thực tế đối với kích thước của mạng do chi phí duy trì số lượng lớn kết nối TCP tới các router khác.

[1] http://www.i2p.net/redesign/roadmap [2] http://dev.i2p.net/pipermail/i2p/2004-June/000286.html

**2) s/reliability/capacity/g**

Trong khoảng tuần vừa rồi, mọi người trên #i2p đã thỉnh thoảng nghe tôi phàn nàn về việc bảng xếp hạng độ tin cậy của chúng ta hoàn toàn võ đoán (và những phiền toái mà nó đã gây ra trong vài bản phát hành gần đây). Vì vậy, chúng tôi đã loại bỏ hoàn toàn khái niệm độ tin cậy, thay thế nó bằng thước đo về năng lực - "một peer (nút đồng đẳng) có thể làm được bao nhiêu cho chúng ta?" Điều này đã tạo ra các tác động dây chuyền xuyên suốt phần mã peer selection và peer profiling (và hiển nhiên cả trên router console), nhưng ngoài điều đó ra thì không có nhiều thay đổi.

Thông tin chi tiết hơn về thay đổi này có thể xem tại trang lựa chọn peer đã được cập nhật [3], và khi 0.3.3 được phát hành, mọi người sẽ có thể thấy tác động trực tiếp (tôi đã thử nghiệm với nó vài ngày qua, tinh chỉnh một số thiết lập, v.v.).

[3] http://www.i2p.net/redesign/how_peerselection

**3) cập nhật trang web**

Trong tuần vừa qua, chúng tôi đã đạt được nhiều tiến triển trong việc thiết kế lại trang web [4] - đơn giản hóa phần điều hướng, tinh chỉnh một số trang quan trọng, nhập nội dung cũ, và soạn thảo một số bài viết mới [5]. Chúng tôi gần như đã sẵn sàng đưa trang web vào hoạt động, nhưng vẫn còn vài việc cần phải làm.

Đầu ngày hôm nay, duck đã rà soát trang web và lập danh sách các trang mà chúng ta còn thiếu, và sau các cập nhật chiều nay, vẫn còn một vài vấn đề tồn đọng mà tôi hy vọng chúng ta có thể tự xử lý hoặc kêu gọi một số tình nguyện viên tham gia giải quyết.

* **documentation**: hmm, do we need any content for this? or can we have it just sit as a header with no page behind it?
* **development**: I think this is in the same boat as "documentation" above
* **news**: perhaps we can remove the 'announcements' page and put that content here? or should we do as above and let news be a simple heading, with an announcements page below?
* **i2ptunnel_services, i2ptunnel_tuning, i2ptunnel_lan**: We need someone to rewrite the 'how to set up an eepsite(I2P Site)' page, as well as include answers to the two most frequently asked I2PTunnel questions (how to access it through a LAN and how to configure its tunnels - answers being: -e "listen_on 0.0.0.0" and -e 'clientoptions tunnels.numInbound=1 tunnels.depthInbound=1', respectively) Perhaps we can come up with some more comprehensive user level I2PTunnel documentation?
* **jvm**: er, I'm not sure about this page - is it 'how to tweak the JVM for optimal performance'? do we *know*?
* **config_tweaks**: other config parameters for the router (bandwidth limiting, etc). could someone go through the router.config and take a stab at what everything means? if anyone has any questions, please let me know.
* **more meeting logs**: mihi posted up an archive of some logs, perhaps a volunteer can sift through those and post them up?
* perhaps we can update the meetings.html to be date based and include a link to that week's status update along with any release announcements preceding it?

Ngoài những điều đó, tôi nghĩ trang web đã gần như sẵn sàng để đưa vào hoạt động chính thức. Có ai có đề xuất hoặc lo ngại nào liên quan không?

[4] http://www.i2p.net/redesign/ [5] http://dev.i2p.net/pipermail/i2pwww/2004-July/thread.html

**4) tấn công và phòng thủ**

Dạo này Connelly đã nghĩ ra vài hướng tiếp cận mới để thử tìm kẽ hở trong bảo mật và tính ẩn danh của mạng, và trong quá trình đó anh ấy cũng phát hiện ra một số cách chúng ta có thể cải thiện mọi thứ. Dù một số khía cạnh của các kỹ thuật anh ấy mô tả không thật sự phù hợp với I2P, có lẽ mọi người có thể nhìn ra cách mở rộng chúng để tấn công mạng sâu hơn nữa? Nào, thử xem nào :)

**5) ???**

Đại khái tôi chỉ nhớ được bấy nhiêu trước cuộc họp tối nay - mọi người cứ thoải mái nêu thêm bất kỳ điều gì tôi đã bỏ sót. Dù sao thì, hẹn gặp mọi người trên #i2p trong vài phút nữa.

=jr
