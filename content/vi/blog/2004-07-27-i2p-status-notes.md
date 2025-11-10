---
title: "Ghi chú trạng thái I2P ngày 2004-07-27"
date: 2004-07-27
author: "jr"
description: "Bản cập nhật tình hình I2P hàng tuần đề cập đến các vấn đề hiệu năng của bản phát hành 0.3.3 và các tối ưu hóa sắp tới"
categories: ["status"]
---

Chào mọi người, đến giờ phiên than phiền hàng tuần rồi

## Mục lục:

1. 0.3.3 & current updates
2. NativeBigInteger
3. ???

## 1) 0.3.3

Chúng tôi đã phát hành phiên bản 0.3.3 vào thứ Sáu vừa rồi và sau một hai ngày đầu khá trục trặc, có vẻ mọi thứ đã ổn. Chưa tốt bằng 0.3.2.3, nhưng thường tôi vẫn có thể ở lại trên irc.duck.i2p trong các phiên 2–7 giờ. Tuy nhiên, vì thấy nhiều người gặp sự cố, tôi bật logger (trình ghi log) và theo dõi chi tiết xem chuyện gì đang diễn ra. Câu trả lời ngắn gọn là chúng tôi đã dùng băng thông nhiều hơn mức cần thiết, gây tắc nghẽn và lỗi tunnel (do các thông điệp kiểm thử bị hết thời gian chờ, v.v.).

Tôi đã dành vài ngày vừa qua trở lại với trình mô phỏng, chạy một loạt tín hiệu heartbeat (tín hiệu kiểm tra trạng thái) qua một mạng để xem chúng ta có thể cải thiện gì, và dựa trên đó, chúng ta có một loạt bản cập nhật sắp được triển khai:

### netDb update to operate more efficiently

Các thông điệp tra cứu netDb hiện tại có thể lên tới 10+KB, và mặc dù các phản hồi thành công xuất hiện thường xuyên, các phản hồi không thành công có thể lên tới 30+KB (vì cả hai đều chứa đầy đủ các cấu trúc RouterInfo). netDb mới thay thế các cấu trúc RouterInfo đầy đủ đó bằng giá trị băm của router - biến các thông điệp 10KB và 30KB thành các thông điệp ~100 byte.

### throw out the SourceRouteBlock and SourceRouteReplyMessage

Những cấu trúc này là phần sót lại của một ý tưởng cũ nhưng không mang lại giá trị nào cho tính ẩn danh hoặc bảo mật của hệ thống. Bằng cách loại bỏ chúng và thay bằng một tập các điểm dữ liệu phản hồi đơn giản hơn, chúng tôi giảm mạnh kích thước các thông điệp quản lý tunnel, và giảm thời gian garlic encryption (kỹ thuật mã hóa "garlic" trong I2P) xuống còn một nửa.

### Cập nhật netDb để hoạt động hiệu quả hơn

Phần mã hơi 'lắm lời' trong quá trình tạo tunnel, nên các thông báo không cần thiết đã được cắt bớt.

### loại bỏ SourceRouteBlock và SourceRouteReplyMessage

Một số mã mật mã cho garlic routing (định tuyến garlic) đã dùng đệm cố định dựa trên một số kỹ thuật garlic routing mà chúng tôi không sử dụng (khi tôi viết nó hồi tháng 9 và tháng 10, tôi đã nghĩ rằng chúng tôi sẽ thực hiện garlic routing nhiều hop thay vì dùng tunnels).

Tôi cũng đang xem xét liệu tôi có thể thực hiện bản cập nhật toàn diện cho định tuyến tunnel để thêm các tunnel ids theo từng hop (bước nhảy).

Như bạn có thể thấy trong lộ trình, điều này bao quát phần lớn bản phát hành 0.4.1, nhưng vì thay đổi netDb đồng nghĩa với việc mất khả năng tương thích ngược, chúng ta cũng nên thực hiện luôn hàng loạt thay đổi không tương thích ngược cùng lúc.

Tôi vẫn đang chạy thử nghiệm trong trình mô phỏng (sim) và còn phải xem liệu tôi có thể hoàn tất phần per-hop tunnel ID hay không, nhưng tôi hy vọng sẽ phát hành một bản vá mới trong một hoặc hai ngày tới. Nó sẽ không tương thích ngược, nên việc nâng cấp có thể sẽ trục trặc, nhưng sẽ đáng giá.

## 2) NativeBigInteger

Iakin đã thực hiện một số cập nhật cho mã NativeBigInteger cho nhóm Freenet, tối ưu hóa một số phần mà chúng tôi không sử dụng, đồng thời viết thêm mã phát hiện CPU mà chúng tôi có thể dùng để tự động chọn đúng native library. Điều đó có nghĩa là chúng tôi sẽ có thể triển khai jbigi trong một lib duy nhất kèm theo cài đặt mặc định và nó sẽ tự chọn cái phù hợp mà không phải hỏi người dùng điều gì. Anh ấy cũng đã đồng ý phát hành các chỉnh sửa của mình và mã phát hiện CPU mới để chúng tôi có thể tích hợp nó vào mã nguồn của mình (yay Iakin!). Tôi chưa chắc khi nào việc này sẽ được triển khai, nhưng tôi sẽ thông báo khi có, vì những ai đang dùng các thư viện jbigi hiện tại nhiều khả năng sẽ cần một bản mới.

## 3) ???

À, tuần vừa rồi hầu như chỉ cắm đầu vào hack mã nguồn, nên không có nhiều cập nhật. Có ai còn điều gì muốn nêu ra không? Nếu có, ghé qua cuộc họp tối nay, lúc 9 giờ tối GMT tại #i2p.

=jr
