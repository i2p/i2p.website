---
title: "Ghi chú trạng thái I2P ngày 2004-09-14"
date: 2004-09-14
author: "jr"
description: "Bản cập nhật tình hình I2P hằng tuần bao gồm bản phát hành 0.4.0.1, cập nhật mô hình đe dọa, cải tiến trang web, thay đổi lộ trình phát triển, và nhu cầu phát triển ứng dụng khách"
categories: ["status"]
---

Chào mọi người, lại đến lúc đó trong tuần rồi

## Mục lục:

1. 0.4.0.1
2. Threat model updates
3. Website updates
4. Roadmap
5. Client apps
6. ???

## 1) 0.4.0.1

Kể từ bản phát hành 0.4.0.1 vào thứ Tư tuần trước, mọi thứ trên mạng diễn ra khá suôn sẻ — hơn 2/3 mạng lưới đã nâng cấp, và chúng tôi đã duy trì từ 60 đến 80 routers trên mạng. Thời gian kết nối IRC dao động, nhưng gần đây các kết nối kéo dài 4-12 giờ là bình thường. Tuy có một số báo cáo về sự trục trặc khi khởi động trên OS/X, nhưng tôi tin rằng khía cạnh đó cũng đang có tiến triển.

## 2) Cập nhật mô hình đe dọa

Như đã đề cập trong phần trả lời bài đăng của Toni, đã có một lần viết lại khá đáng kể đối với mô hình đe dọa. Khác biệt chính là thay vì cách cũ xử lý các mối đe dọa theo kiểu chắp vá, tôi đã cố gắng tuân theo một số hệ phân loại được nêu trong tài liệu. Vấn đề lớn nhất đối với tôi là tìm cách đưa các kỹ thuật thực tế mà người ta có thể sử dụng vào các khuôn mẫu được đề xuất - thường thì một cuộc tấn công đơn lẻ lại phù hợp với nhiều nhóm khác nhau. Vì vậy, tôi cũng không thực sự hài lòng với cách thông tin trên trang đó được truyền đạt, nhưng vẫn tốt hơn trước đây.

## 3) Cập nhật trang web

Nhờ sự giúp đỡ của Curiosity, chúng tôi đã bắt đầu thực hiện một số cập nhật cho trang web - điều dễ thấy nhất là ngay trên chính trang chủ. Điều này sẽ giúp những người tình cờ gặp I2P và muốn biết ngay lập tức rốt cuộc I2P là cái quái gì, thay vì phải mò mẫm qua đủ loại trang. Dù sao thì, vẫn tiến lên, không ngừng :)

## 4) Lộ trình

Nói về tiến độ, cuối cùng tôi cũng đã phác thảo xong một lộ trình đã được cải tổ, dựa trên những gì tôi cho rằng chúng ta cần triển khai và những gì phải hoàn thành để đáp ứng nhu cầu của người dùng. Những thay đổi lớn so với lộ trình cũ bao gồm:

- Drop AMOC altogether, replaced with UDP (however, we'll support TCP for those who can't use UDP *cough*mihi*cough*)
- Kept all of the restricted route operation to the 2.0 release, rather than bring in partial restricted routes earlier. I believe we'll be able to meet the needs of many users without restricted routes, though of course with them many more users will be able to join us. Walk before run, as they say.
- Pulled the streaming lib in to the 0.4.3 release, as we don't want to go 1.0 with the ~4KBps per stream limit. The bounty on this is still of course valid, but if no one claims it before 0.4.2 is done, I'll start working on it.
- TCP revamp moved to 0.4.1 to address some of our uglier issues (high CPU usage when connecting to people, the whole mess with "target changed identities", adding autodetection of IP address)

Các hạng mục khác được lên lịch cho các bản phát hành 0.4.* khác nhau đã được thực hiện. Tuy nhiên, còn một hạng mục khác đã bị loại khỏi lộ trình...

## 5) Ứng dụng khách

Chúng ta cần các ứng dụng khách. Những ứng dụng hấp dẫn, an toàn, có khả năng mở rộng và ẩn danh. Bản thân I2P không làm được nhiều; nó chỉ cho phép hai điểm cuối trao đổi với nhau một cách ẩn danh. Mặc dù I2PTunnel cung cấp một bộ công cụ kiểu "dao đa năng Thụy Sĩ" cực kỳ lợi hại, những công cụ như vậy chỉ thực sự hấp dẫn đối với những người đam mê kỹ thuật. Chúng ta cần nhiều hơn thế - chúng ta cần những thứ cho phép mọi người làm đúng điều họ thực sự muốn làm, và giúp họ làm điều đó tốt hơn. Chúng ta cần một lý do để mọi người dùng I2P vượt lên trên lý do đơn thuần là vì nó an toàn hơn.

So far I've been touting MyI2P to meet that need - a distributed blogging system offering a LiveJournal-esque interface. I recently discussed some of the functionality within MyI2P on the list. However, I've pulled it out of the roadmap as its just too much work for me to do and still give the base I2P network the attention it needs (we're already packed extremely tight).

Có một vài ứng dụng khác rất hứa hẹn. Stasher sẽ cung cấp một hạ tầng đáng kể cho lưu trữ dữ liệu phân tán, nhưng tôi không chắc nó đang tiến triển đến đâu. Tuy nhiên, ngay cả với Stasher, vẫn cần có một giao diện người dùng hấp dẫn (mặc dù một số ứng dụng FCP (ứng dụng sử dụng giao thức FCP) có thể hoạt động với nó).

IRC cũng là một hệ thống mạnh mẽ, tuy nhiên có những hạn chế do kiến trúc dựa trên máy chủ. oOo đã thực hiện một số công việc để xem xét khả năng triển khai DCC trong suốt, vì vậy có lẽ phía IRC có thể được dùng cho trò chuyện công khai và DCC cho việc truyền tệp riêng tư hoặc trò chuyện không máy chủ.

Chức năng chung của eepsite(I2P Site) cũng quan trọng, và những gì chúng ta có hiện nay hoàn toàn không thỏa đáng. Như DrWoo chỉ ra, có những rủi ro ẩn danh đáng kể với thiết lập hiện tại, và mặc dù oOo đã thực hiện một số bản vá để lọc một số header, vẫn còn rất nhiều việc phải làm trước khi các eepsites(I2P Sites) có thể được coi là an toàn. Có một vài cách tiếp cận khác nhau để giải quyết vấn đề này, tất cả đều khả thi, nhưng tất cả đều đòi hỏi công sức. Tôi có biết duck từng đề cập rằng anh ấy có người đang làm gì đó, dù tôi không biết tiến độ ra sao hoặc liệu nó có thể được đóng gói kèm theo I2P để mọi người sử dụng hay không. Duck?

Một cặp ứng dụng khách khác có thể hữu ích sẽ là một ứng dụng truyền tệp theo kiểu swarm (như BitTorrent) hoặc một ứng dụng chia sẻ tệp truyền thống hơn (như DC/Napster/Gnutella/etc). Tôi cho rằng đây là thứ mà rất nhiều người muốn, nhưng mỗi hệ thống trong số này đều có những vấn đề riêng. Tuy vậy, chúng khá nổi tiếng và việc port có lẽ sẽ không quá rắc rối (có lẽ).

Được rồi, những điều ở trên không có gì mới — tại sao tôi lại nhắc đến tất cả chúng? Chà, chúng ta cần tìm cách triển khai một ứng dụng khách hấp dẫn, an toàn, có khả năng mở rộng và ẩn danh, và điều đó sẽ không tự nhiên xảy ra một cách bất ngờ. Tôi đã chấp nhận rằng tôi sẽ không thể tự mình làm được, vì vậy chúng ta cần chủ động và tìm cách để hoàn thành việc này.

Để làm được như vậy, tôi nghĩ hệ thống bounty (nhiệm vụ có thưởng) của chúng ta có thể giúp, nhưng tôi cho rằng một trong những lý do chúng ta chưa thấy nhiều hoạt động ở khía cạnh đó (mọi người làm việc để thực hiện một bounty) là vì họ đang bị dàn trải quá mỏng. Để đạt được kết quả chúng ta cần, tôi cảm thấy chúng ta cần ưu tiên những gì mình muốn và tập trung nỗ lực vào mục tiêu ưu tiên hàng đầu đó, “tăng mức thưởng” để hy vọng khuyến khích ai đó đứng ra nhận và làm việc trên bounty.

Ý kiến cá nhân của tôi vẫn là một hệ thống blog bảo mật và phân tán như MyI2P sẽ là lựa chọn tốt nhất. Thay vì chỉ đơn thuần đẩy dữ liệu qua lại một cách ẩn danh, nó mang lại một cách thức để xây dựng cộng đồng, vốn là mạch sống của bất kỳ nỗ lực phát triển nào. Ngoài ra, nó còn mang lại tỷ lệ tín hiệu trên nhiễu tương đối cao, khả năng bị lạm dụng tài nguyên chung thấp, và nói chung, tải mạng nhẹ. Tuy nhiên, nó không cung cấp toàn bộ sự đa dạng như các website thông thường, nhưng 1,8 triệu người dùng LiveJournal đang hoạt động có vẻ cũng không bận tâm.

Ngoài ra, ưu tiên tiếp theo của tôi là tăng cường bảo mật cho kiến trúc eepsite(I2P Site), giúp các trình duyệt có được mức độ an toàn cần thiết và cho phép mọi người phục vụ eepsites(I2P Sites) ngay lập tức, không cần cấu hình.

Truyền tệp và lưu trữ dữ liệu phân tán cũng vô cùng mạnh mẽ, nhưng có vẻ chúng không định hướng cộng đồng ở mức mà chúng ta có lẽ mong muốn cho ứng dụng đầu tiên dành cho người dùng cuối phổ thông.

Tôi muốn tất cả các ứng dụng được liệt kê đều đã được triển khai từ hôm qua, cũng như hàng nghìn ứng dụng khác mà tôi còn chưa dám mơ tới. Tôi cũng muốn hòa bình thế giới, chấm dứt nạn đói, xóa bỏ chủ nghĩa tư bản, thoát khỏi chủ nghĩa nhà nước, nạn phân biệt chủng tộc, phân biệt giới tính, kỳ thị đồng tính, chấm dứt việc tàn phá trắng trợn môi trường và mọi điều xấu xa khác. Tuy vậy, chúng ta chỉ có bấy nhiêu người và chỉ có thể làm được bấy nhiêu việc. Vì thế, chúng ta phải ưu tiên và tập trung nỗ lực vào những gì có thể đạt được thay vì ngồi đó choáng ngợp trước tất cả những điều mình muốn làm.

Có lẽ chúng ta có thể thảo luận một vài ý tưởng về việc chúng ta nên làm gì trong cuộc họp tối nay.

## 6) ???

Ừ thì, tạm thời tôi chỉ có thế, và này, tôi đã viết xong ghi chú trạng thái *trước* cuộc họp rồi! Vậy là hết cớ nhé, hãy ghé qua lúc 9 giờ tối GMT và oanh tạc tất cả chúng tôi bằng ý tưởng của bạn.

=jr
