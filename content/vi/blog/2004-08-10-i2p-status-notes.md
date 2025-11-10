---
title: "Ghi chú trạng thái I2P cho 2004-08-10"
date: 2004-08-10
author: "jr"
description: "Bản cập nhật trạng thái I2P hàng tuần bao gồm hiệu năng của bản phát hành 0.3.4.1, cân bằng tải outproxy (proxy thoát ra Internet công khai), và các cập nhật tài liệu"
categories: ["status"]
---

Chào mọi người, đến giờ cập nhật hằng tuần

## Mục lục:

1. 0.3.4.1 status
2. Updated docs
3. 0.4 progress
4. ???

## 1) 0.3.4.1 trạng thái

À, chúng tôi đã tung ra bản phát hành 0.3.4.1 cách đây vài ngày, và nó đang hoạt động khá tốt. Các phiên kết nối trên IRC ổn định, kéo dài hàng giờ liền, và tốc độ truyền cũng khá tốt (tôi đã đạt khoảng 25KBps từ một eepsite (trang web I2P) hôm trước khi dùng 3 luồng song song).

Một tính năng cực kỳ hay được bổ sung trong bản phát hành 0.3.4.1 (mà tôi đã quên đưa vào thông báo phát hành) là bản vá của mule cho phép eepproxy (proxy HTTP của I2P) phân phối theo cơ chế round-robin các yêu cầu không thuộc I2P qua một loạt outproxy (proxy thoát ra Internet thông thường). Mặc định vẫn chỉ sử dụng outproxy squid.i2p, nhưng nếu bạn vào router.config của mình và thay đổi dòng clientApp để chứa:

```
-e 'httpclient 4444 squid.i2p,www1.squid.i2p'
```
nó sẽ định tuyến ngẫu nhiên mỗi yêu cầu HTTP qua một trong hai outproxies (proxy thoát) đã liệt kê (squid.i2p và www1.squid.i2p). Như vậy, nếu có thêm một vài người vận hành outproxies, mọi người sẽ không còn phụ thuộc quá nhiều vào squid.i2p. Tất nhiên, mọi người đều đã nghe những quan ngại của tôi về outproxies, nhưng có được khả năng này sẽ mang lại cho mọi người nhiều lựa chọn hơn.

Chúng tôi đã thấy một số tình trạng không ổn định trong vài giờ qua, nhưng với sự giúp đỡ của duck và cervantes, tôi đã xác định được hai lỗi nghiêm trọng và hiện tại đang thử nghiệm các bản sửa lỗi. Các bản sửa lỗi này khá quan trọng, vì vậy tôi kỳ vọng sẽ phát hành bản 0.3.4.2 trong một hoặc hai ngày tới, sau khi tôi xác minh kết quả.

## 2) Tài liệu đã được cập nhật

Chúng tôi đã có phần chậm trễ trong việc cập nhật tài liệu trên trang web, và dù vẫn còn một vài khoảng trống lớn (ví dụ: tài liệu netDb và i2ptunnel), gần đây chúng tôi đã cập nhật một vài mục (so sánh các mạng và FAQ). Khi chúng ta tiến gần hơn tới các bản phát hành 0.4 và 1.0, tôi rất mong mọi người có thể xem qua trang web và xem còn gì có thể cải thiện.

Đáng chú ý là Bảng Vinh Danh đã được cập nhật - cuối cùng chúng tôi cũng đã đồng bộ hóa để phản ánh những khoản đóng góp hào phóng mà mọi người đã thực hiện (cảm ơn!). Trong thời gian tới, chúng tôi sẽ sử dụng các nguồn lực này để thù lao cho các lập trình viên và những người đóng góp khác, cũng như bù đắp các chi phí phát sinh (ví dụ: nhà cung cấp dịch vụ hosting, v.v.).

## 3) tiến độ 0.4

Nhìn lại ghi chú tuần trước, chúng tôi vẫn còn một vài hạng mục cho 0.4, nhưng các mô phỏng đã diễn ra khá tốt, và phần lớn các vấn đề về kaffe đã được phát hiện. Sẽ thật tuyệt nếu mọi người có thể tích cực thử nghiệm các khía cạnh khác nhau của router hoặc các ứng dụng khách và báo cáo bất kỳ lỗi nào mà bạn gặp phải.

## 4) ???

Hiện tại tôi chỉ có bấy nhiêu điều muốn nêu ra - tôi rất cảm kích thời gian mọi người bỏ ra để giúp chúng ta tiến về phía trước, và tôi nghĩ chúng ta đang đạt được tiến bộ rất tốt. Tất nhiên, nếu ai còn điều gì muốn bàn thêm, hãy ghé qua cuộc họp ở #i2p vào... ờ... ngay bây giờ :)

=jr
