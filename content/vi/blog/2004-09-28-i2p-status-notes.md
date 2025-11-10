---
title: "Ghi chú trạng thái I2P cho ngày 2004-09-28"
date: 2004-09-28
author: "jr"
description: "Cập nhật tình hình I2P hằng tuần bao gồm việc triển khai giao thức truyền tải mới, tự động phát hiện IP, và tiến độ phát hành 0.4.1"
categories: ["status"]
---

Chào mọi người, đến giờ cập nhật hàng tuần rồi

## Chỉ mục:

1. New transport
2. 0.4.1 status
3. ???

## 1) Giao thức truyền tải mới

Bản phát hành 0.4.1 mất nhiều thời gian hơn dự kiến, nhưng giao thức truyền tải và phần hiện thực mới đã được đưa vào với tất cả những gì đã lên kế hoạch — phát hiện IP, thiết lập kết nối chi phí thấp, và một giao diện dễ dùng hơn để giúp gỡ lỗi khi kết nối thất bại. Điều này được thực hiện bằng cách loại bỏ hoàn toàn giao thức truyền tải cũ và triển khai một giao thức mới, mặc dù chúng tôi vẫn giữ những “từ khóa kêu” giống nhau (2048bit DH + STS, AES256/CBC/PKCS#5). Nếu bạn muốn xem lại giao thức, nó có trong tài liệu. Bản hiện thực mới cũng gọn gàng hơn rất nhiều, vì phiên bản cũ chỉ là một tập hợp các bản cập nhật tích lũy trong năm qua.

Dù sao thì, có một vài điểm trong mã phát hiện IP mới đáng để nhắc đến. Quan trọng nhất, nó hoàn toàn tùy chọn - nếu bạn chỉ định một địa chỉ IP trên trang cấu hình (hoặc trong chính router.config), nó sẽ luôn sử dụng địa chỉ đó, bất kể thế nào. Tuy nhiên, nếu bạn để trống mục đó, router của bạn sẽ để cho peer đầu tiên mà nó liên lạc nói cho nó biết địa chỉ IP của nó là gì, và sau đó nó sẽ bắt đầu lắng nghe trên địa chỉ đó (sau khi thêm thông tin đó vào RouterInfo của chính nó và đưa nó vào cơ sở dữ liệu mạng). À, không hẳn như vậy - nếu bạn chưa đặt rõ ràng một địa chỉ IP, nó sẽ tin bất kỳ ai nói cho nó biết địa chỉ IP mà nó có thể được truy cập tới bất cứ khi nào peer không có kết nối. Vì vậy, nếu kết nối Internet của bạn khởi động lại, có thể cấp cho bạn một địa chỉ DHCP mới, router của bạn sẽ tin tưởng peer đầu tiên mà nó có thể liên hệ được.

Vâng, điều này có nghĩa là không cần dùng dyndns nữa. Dĩ nhiên bạn vẫn có thể tiếp tục sử dụng nó, nhưng không cần thiết.

Tuy nhiên, điều này không làm được hết những gì bạn muốn - nếu bạn có NAT hoặc tường lửa, biết được địa chỉ IP bên ngoài của bạn chỉ mới là một nửa chặng đường - bạn vẫn cần thiết lập chuyển tiếp cổng (port forwarding) cho cổng vào. Nhưng đó cũng là một khởi đầu.

(nhân tiện, đối với những người đang vận hành các mạng I2P riêng của họ hoặc các trình mô phỏng, có một cặp flags (cờ cấu hình) mới cần được thiết lập i2np.tcp.allowLocal và i2np.tcp.tagFile)

## 2) 0.4.1 trạng thái

Vượt ra ngoài các hạng mục trong lộ trình cho 0.4.1, tôi muốn đưa thêm một vài thứ vào — cả các sửa lỗi và các cập nhật giám sát mạng. Hiện tôi đang truy tìm một số vấn đề memory churn quá mức (tần suất cấp phát/giải phóng bộ nhớ quá cao), và tôi muốn kiểm chứng vài giả thuyết về các sự cố độ tin cậy thỉnh thoảng xảy ra trên mạng, nhưng chúng tôi sẽ sẵn sàng tung ra bản phát hành sớm, có lẽ vào thứ Năm. Đáng tiếc là nó sẽ không tương thích ngược, vì vậy quá trình có thể hơi trục trặc một chút, nhưng với quy trình nâng cấp mới và triển khai transport (lớp truyền tải) chịu lỗi tốt hơn, mọi thứ sẽ không tệ như các lần cập nhật trước vốn không tương thích ngược.

## 3) ???

Ừ, hai tuần vừa rồi chúng tôi chỉ có các cập nhật ngắn, vì đang cắm đầu vào phần triển khai thay vì các thiết kế cấp cao hơn. Tôi có thể kể cho mọi người về dữ liệu profiling, hoặc về bộ đệm (cache) thẻ kết nối 10.000 mục cho transport mới, nhưng mấy thứ đó cũng không thú vị lắm. Dù vậy, biết đâu mọi người còn chuyện cần bàn; vậy thì ghé cuộc họp tối nay và cứ thả ga nhé.

=jr
