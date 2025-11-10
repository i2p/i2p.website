---
title: "Ghi chú trạng thái I2P cho ngày 2005-03-22"
date: 2005-03-22
author: "jr"
description: "Ghi chú trạng thái phát triển I2P hàng tuần, đề cập đến bản phát hành 0.5.0.3, việc triển khai cơ chế gộp (batching) thông điệp cho tunnel, và các công cụ cập nhật tự động"
categories: ["status"]
---

Chào mọi người, cập nhật nhanh tình hình

* Index

1) 0.5.0.3 2) xử lý theo lô 3) cập nhật 4) ???

* 0.5.0.3

Bản phát hành mới đã ra mắt và hầu hết mọi người đã nâng cấp khá nhanh — cảm ơn! Có một số bản sửa lỗi cho nhiều vấn đề khác nhau, nhưng không có gì đột phá — thay đổi lớn nhất là ngừng cho phép người dùng 0.5 và 0.5.0.1 tham gia mạng. Từ đó đến nay tôi đã theo dõi hành vi của mạng, đào sâu tìm hiểu những gì đang diễn ra, và dù đã có một số cải thiện, vẫn còn một vài việc cần được giải quyết.

Sẽ có một bản phát hành mới trong một đến hai ngày tới, kèm theo bản vá cho một lỗi mà chưa ai gặp phải nhưng lại làm hỏng phần mã xử lý theo lô mới. Cũng sẽ có một số công cụ để tự động hóa quy trình cập nhật theo tùy chọn của người dùng, cùng với một số hạng mục nhỏ khác.

* batching

Như tôi đã đề cập trong blog của mình, có thể giảm đáng kể băng thông và số lượng thông điệp cần thiết trên mạng bằng cách gộp theo lô rất đơn giản các thông điệp tunnel - thay vì đặt mỗi thông điệp I2NP, bất kể kích thước, vào một thông điệp tunnel riêng, bằng cách thêm một độ trễ ngắn, chúng tôi có thể gom tới 15 thông điệp hoặc hơn vào một thông điệp tunnel duy nhất. Lợi ích lớn nhất sẽ đạt được với các dịch vụ sử dụng thông điệp nhỏ (chẳng hạn như IRC), trong khi các truyền tải tệp lớn sẽ không bị ảnh hưởng nhiều. Mã để thực hiện việc gộp theo lô đã được triển khai và kiểm thử, nhưng đáng tiếc hiện có một lỗi trên mạng đang hoạt động khiến tất cả các thông điệp I2NP trong một thông điệp tunnel, ngoại trừ thông điệp đầu tiên, bị mất. Đó là lý do chúng tôi sẽ tung ra một bản phát hành tạm thời có kèm bản sửa lỗi đó, sau đó khoảng một tuần sẽ phát hành bản có tính năng gộp theo lô.

* updating

Trong bản phát hành tạm thời này, chúng tôi sẽ đưa vào một phần của mã 'autoupdate' vốn thường được bàn luận. Chúng tôi đã có các công cụ để định kỳ kiểm tra các thông báo cập nhật đã được xác thực, tải bản cập nhật một cách ẩn danh hoặc không, và sau đó hoặc cài đặt nó, hoặc chỉ hiển thị một thông báo trên router console (bảng điều khiển của router) cho bạn biết rằng nó đã sẵn sàng và đang chờ được cài đặt. Bản cập nhật hiện sẽ sử dụng định dạng cập nhật được ký mới của smeghead, về cơ bản là gói cập nhật kèm chữ ký DSA. Các khóa dùng để xác minh chữ ký đó sẽ được đóng gói kèm với I2P, đồng thời có thể cấu hình trên router console.

Hành vi mặc định sẽ đơn giản là kiểm tra định kỳ các thông báo cập nhật nhưng không tự động cập nhật - chỉ hiển thị tính năng "Cập nhật ngay" chỉ với một lần nhấp trên bảng điều khiển router.  Sẽ còn nhiều kịch bản khác cho các nhu cầu người dùng khác nhau, nhưng hy vọng tất cả sẽ được đáp ứng thông qua một trang cấu hình mới.

* ???

Tôi thấy hơi mệt, nên phần trên không thực sự đi vào đầy đủ chi tiết về chuyện gì đang diễn ra. Ghé qua cuộc họp và bổ sung những chỗ còn thiếu nhé :)

À, nhân tiện, tôi cũng sẽ phát hành một khóa PGP mới cho riêng tôi trong một hoặc hai ngày tới (vì khóa hiện tại sắp hết hạn...), vậy nên hãy chú ý theo dõi.

=jr
