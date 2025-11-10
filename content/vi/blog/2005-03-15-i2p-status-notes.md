---
title: "Ghi chú trạng thái I2P cho ngày 2005-03-15"
date: 2005-03-15
author: "jr"
description: "Ghi chú trạng thái phát triển I2P hàng tuần bao gồm phân tích hiệu năng mạng, các cải tiến trong tính toán tốc độ và phát triển Feedspace"
categories: ["status"]
---

Chào mọi người, đến giờ cập nhật hàng tuần

* Index

1) Trạng thái mạng 2) Feedspace (không gian nguồn cấp) 3) ???

* 1) Net status

Trong tuần vừa qua, phần lớn thời gian của tôi đã dành cho việc phân tích hành vi của mạng, theo dõi thống kê và cố gắng tái tạo các sự kiện khác nhau trong trình mô phỏng.  Mặc dù một số hành vi khác thường của mạng có thể được quy cho khoảng hai chục router vẫn đang chạy các phiên bản cũ, yếu tố then chốt là các phép tính tốc độ của chúng tôi không cho ra dữ liệu tốt - chúng tôi không thể xác định chính xác những peer (nút ngang hàng) có thể truyền dữ liệu nhanh.  Trước đây, điều này không phải là vấn đề lớn, vì có một lỗi khiến chúng tôi sử dụng 8 peer có dung lượng cao nhất làm nhóm 'fast', thay vì xây dựng các tầng dựa trên dung lượng đúng nghĩa.  Phép tính tốc độ hiện tại của chúng tôi được suy ra từ một bài kiểm tra độ trễ định kỳ (cụ thể là RTT của một bài kiểm tra tunnel), nhưng điều đó không cung cấp đủ dữ liệu để có thể tin tưởng vào giá trị thu được.  Điều chúng ta cần là một cách tốt hơn để thu thập nhiều điểm dữ liệu hơn, đồng thời vẫn cho phép các peer có dung lượng cao được đưa vào tầng 'fast' khi cần.

Để xác minh rằng đây chính là vấn đề cốt lõi mà chúng ta đang gặp phải, tôi đã “ăn gian” một chút và bổ sung chức năng cho phép chọn thủ công những peers (nút ngang hàng) sẽ được dùng trong việc lựa chọn cho một nhóm tunnel cụ thể. Với các peers được chọn tường minh đó, tôi đã ở trên irc hơn hai ngày liền mà không bị ngắt kết nối và có hiệu năng khá ổn với một dịch vụ khác do tôi kiểm soát. Trong khoảng hai ngày vừa qua, tôi đã thử một bộ tính toán tốc độ mới sử dụng một số thống kê mới, và mặc dù nó đã cải thiện việc lựa chọn, nó vẫn còn vài vấn đề. Chiều nay tôi đã xem xét qua một vài phương án thay thế, nhưng vẫn còn việc phải làm để thử chúng trên mạng.

* 2) Feedspace

Frosk đã đưa lên một bản sửa đổi nữa của tài liệu i2pcontent/fusenet, nhưng giờ đã ở một địa chỉ mới với một tên mới: http://feedspace.i2p/ - xem orion [1] hoặc blog của tôi [2] để lấy destination (điểm đến trong I2P). Những thứ này trông rất hứa hẹn, cả từ góc độ "này, chức năng cực kỳ ấn tượng" lẫn "này, điều đó sẽ giúp tăng tính ẩn danh của I2P". Frosk và mọi người đang miệt mài làm việc, nhưng họ chắc chắn đang tìm kiếm ý kiến đóng góp (và hỗ trợ). Có lẽ chúng ta có thể mời Frosk cung cấp một bản cập nhật trong cuộc họp?

[1] http://orion.i2p/#feedspace.i2p [2] http://jrandom.dev.i2p/

* 3) ???

Được rồi, có thể trông không có gì đặc biệt, nhưng thực ra có rất nhiều thứ đang diễn ra :) Tôi chắc là mình cũng đã bỏ sót vài thứ, nên hãy ghé qua cuộc họp để xem tình hình thế nào.

=jr
