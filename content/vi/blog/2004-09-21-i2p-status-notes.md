---
title: "Ghi chú trạng thái I2P ngày 2004-09-21"
date: 2004-09-21
author: "jr"
description: "Cập nhật tình hình I2P hàng tuần bao gồm tiến độ phát triển, các cải tiến tầng vận chuyển TCP, và tính năng mới cho userhosts.txt"
categories: ["status"]
---

Chào mọi người, cập nhật nhanh tuần này

## Mục lục

1. Dev status
2. New userhosts.txt vs. hosts.txt
3. ???

## 1) Trạng thái phát triển

Mạng lưới đã khá ổn định trong tuần vừa qua, vì vậy tôi đã có thể tập trung vào bản phát hành 0.4.1 — đại tu transport TCP và bổ sung hỗ trợ phát hiện địa chỉ IP, đồng thời loại bỏ thông báo cũ "target changed identities". Điều này cũng sẽ loại bỏ nhu cầu dùng các bản ghi dyndns.

Nó sẽ không phải là một thiết lập không cần nhấp chuột lý tưởng cho những người ở phía sau NAT hoặc tường lửa - họ vẫn cần thực hiện chuyển tiếp cổng (port forwarding) để có thể nhận các kết nối TCP đến. Tuy vậy, nó sẽ ít dễ gặp lỗi hơn. Tôi đang cố hết sức để giữ khả năng tương thích ngược, nhưng tôi không hứa hẹn gì về mặt đó. Sẽ có thêm thông tin khi mọi thứ sẵn sàng.

## 2) userhosts.txt mới so với hosts.txt

Trong bản phát hành tiếp theo, chúng tôi sẽ có tính năng hỗ trợ được yêu cầu thường xuyên cho một cặp tệp hosts.txt - một tệp sẽ bị ghi đè trong quá trình nâng cấp (hoặc từ `http://dev.i2p.net/i2p/hosts.txt`) và một tệp khác mà người dùng có thể duy trì cục bộ. Trong bản phát hành tiếp theo (hoặc CVS HEAD) bạn có thể chỉnh sửa tệp "userhosts.txt", tệp này được kiểm tra trước hosts.txt để tìm bất kỳ mục nào - vui lòng thực hiện các thay đổi cục bộ của bạn ở đó, vì quy trình cập nhật sẽ ghi đè hosts.txt (nhưng không ghi đè userhosts.txt).

## 3) ???

Như tôi đã đề cập, tuần này chỉ có một vài ghi chú ngắn. Có ai còn điều gì muốn nêu ra không? Hãy ghé qua cuộc họp trong vài phút nữa.

=jr
