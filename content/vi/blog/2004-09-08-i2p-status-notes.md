---
title: "Ghi chú trạng thái I2P cho ngày 2004-09-08"
date: 2004-09-08
author: "jr"
description: "Cập nhật tình hình I2P hàng tuần bao gồm bản phát hành 0.4, các vấn đề về dung lượng mạng, các cập nhật cho trang web, và các cải tiến giao diện I2PTunnel"
categories: ["status"]
---

Chào mọi người, xin lỗi vì đến muộn...

## Chỉ mục:

1. 0.4
2. Capacity and overload
3. Website updates
4. I2PTunnel web interface
5. Roadmap and todo
6. ???

## 1) 0.4

Chắc hẳn mọi người đều đã thấy, bản phát hành 0.4 vừa ra mắt mấy hôm trước và nhìn chung, mọi thứ đang diễn ra khá tốt. Thật khó tin là đã 6 tháng kể từ khi 0.3 ra mắt (và một năm kể từ khi 1.0 SDK được phát hành), nhưng chúng ta đã tiến một chặng đường dài, và sự chăm chỉ, nhiệt huyết, cùng sự kiên nhẫn của tất cả mọi người đã làm nên những điều kỳ diệu. Chúc mừng, và cảm ơn!

Giống như bất kỳ bản phát hành tốt nào, ngay khi vừa ra mắt chúng tôi đã phát hiện một số vấn đề, và trong vài ngày qua chúng tôi đã nhận được nhiều báo cáo lỗi và vá lỗi ráo riết (bạn có thể theo dõi các thay đổi khi chúng được khắc phục). Chúng tôi vẫn còn một vài lỗi nữa cần xử lý trước khi phát hành bản sửa đổi tiếp theo, nhưng việc đó sẽ xong trong vòng một ngày tới hoặc khoảng đó.

## 2) Dung lượng và quá tải

Chúng tôi đã thấy một số phân bổ tunnels khá lệch trong vài bản phát hành gần đây, và mặc dù một số trong đó liên quan đến lỗi (hai trong số các lỗi đó đã được sửa kể từ khi 0.4 được phát hành), vẫn còn một câu hỏi tổng quát về thuật toán - khi nào một router nên ngừng chấp nhận thêm tunnels?

Vài phiên bản trước, chúng tôi đã thêm mã điều tiết lưu lượng để từ chối các yêu cầu tham gia vào một tunnel nếu router bị quá tải (thời gian xử lý thông điệp cục bộ vượt quá 1s), và điều đó đã giúp cải thiện đáng kể. Tuy nhiên, có hai khía cạnh của thuật toán đơn giản đó chưa được xử lý: - khi băng thông của chúng tôi bị bão hòa, thời gian xử lý cục bộ có thể vẫn nhanh, vì vậy chúng tôi sẽ tiếp tục chấp nhận thêm các yêu cầu tunnel - khi một nút ngang hàng (peer) đơn lẻ tham gia "quá nhiều" tunnels, khi chúng thất bại, điều đó gây hại cho mạng nhiều hơn.

Vấn đề thứ nhất được xử lý khá dễ dàng bằng cách chỉ cần bật bộ giới hạn băng thông (vì việc giới hạn băng thông làm chậm thời gian xử lý thông điệp tương ứng với độ trễ do băng thông). Vấn đề thứ hai phức tạp hơn, và cần thêm cả nghiên cứu lẫn mô phỏng. Tôi đang nghĩ đến hướng tiếp cận kiểu như từ chối các yêu cầu tunnel theo xác suất dựa trên tỷ lệ giữa số tunnel chúng ta tham gia và số tunnel được yêu cầu từ mạng, bao gồm một "kindness factor" cơ sở, đặt P(reject) = 0 nếu chúng ta tham gia ít hơn mức đó.

Nhưng như tôi đã nói, cần có thêm công việc và mô phỏng.

## 3) Cập nhật trang web

Giờ đây khi chúng ta đã có giao diện web I2P mới, hầu như toàn bộ tài liệu dành cho người dùng cuối trước đây đều đã lỗi thời. Chúng tôi cần sự giúp đỡ rà soát các trang đó và cập nhật chúng để mô tả cách thức hoạt động hiện nay. Như duck và những người khác đã đề xuất, chúng ta cần một hướng dẫn 'khởi động nhanh' mới, ngoài phần readme tại `http://localhost:7657/` — một tài liệu giúp mọi người nhanh chóng bắt đầu và đi vào hệ thống.

Ngoài ra, giao diện web mới của chúng tôi có nhiều chỗ để tích hợp trợ giúp theo ngữ cảnh. Như bạn có thể thấy trên help.jsp đi kèm, "hmm. có lẽ chúng ta nên có một số nội dung trợ giúp ở đây."

Có lẽ sẽ rất hữu ích nếu chúng ta có thể thêm các liên kết 'about' và/hoặc 'troubleshooting' vào các trang khác nhau, giải thích ý nghĩa của các mục và cách sử dụng chúng.

## 4) Giao diện web của I2PTunnel

Việc gọi giao diện mới `http://localhost:7657/i2ptunnel/` là "tối giản" vẫn còn là nói giảm. Chúng tôi cần làm rất nhiều việc để đưa nó tiến gần hơn đến trạng thái có thể sử dụng — hiện tại, về mặt kỹ thuật thì chức năng đã có, nhưng bạn thật sự cần biết những gì đang diễn ra ở hậu trường để hiểu được. Tôi nghĩ duck có thể có thêm một số ý tưởng về vấn đề này để nêu ra trong cuộc họp.

## 5) Lộ trình và việc cần làm

Tôi đã lơ là trong việc giữ cho lộ trình luôn được cập nhật, nhưng thực tế là chúng ta còn phải tiếp tục chỉnh sửa thêm. Để giúp giải thích những gì tôi coi là các "vấn đề lớn", tôi đã tổng hợp một danh sách công việc mới, trong đó đi vào một số chi tiết cho từng mục. Tôi nghĩ ở thời điểm này chúng ta nên khá cởi mở trong việc xem xét lại các phương án và có lẽ sẽ điều chỉnh lại lộ trình.

Một điều tôi đã quên đề cập trong danh sách việc cần làm đó là khi thêm giao thức kết nối nhẹ, chúng ta có thể bao gồm (tùy chọn) tính năng tự động phát hiện địa chỉ IP. Điều này có thể 'nguy hiểm' (đó là lý do tại sao nó sẽ là tùy chọn), nhưng nó sẽ giúp giảm đáng kể số lượng yêu cầu hỗ trợ mà chúng ta nhận được :)

Dù sao, những vấn đề được đăng trong danh sách việc cần làm là những thứ chúng tôi đã lên kế hoạch cho nhiều bản phát hành khác nhau, và chắc chắn sẽ không thể đưa hết vào 1.0 hay thậm chí 2.0. Tôi đã phác thảo một vài phương án ưu tiên / phát hành khác nhau, nhưng tôi vẫn chưa chốt chắc các phương án đó. Tuy nhiên, nếu mọi người có thể xác định những việc lớn khác ở phía trước, chúng tôi sẽ rất cảm kích, vì một vấn đề chưa được lên lịch luôn rất phiền toái.

## 6) ???

Được rồi, hiện giờ tôi chỉ có thế (cũng may, vì cuộc họp sẽ bắt đầu trong vài phút nữa). Hãy ghé qua #i2p trên irc.freenode.net, www.invisiblechat.com, hoặc irc.duck.i2p lúc 9 giờ tối GMT để trò chuyện thêm.
