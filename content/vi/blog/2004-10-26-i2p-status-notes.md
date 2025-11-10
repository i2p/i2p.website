---
title: "Ghi chú trạng thái I2P cho ngày 2004-10-26"
date: 2004-10-26
author: "jr"
description: "Weekly I2P status update covering network stability, streaming library development, mail.i2p progress, and BitTorrent advancements"
categories: ["status"]
---

Chào mọi người, đến giờ cập nhật hàng tuần rồi

## Chỉ mục

1. Net status
2. Streaming lib
3. mail.i2p progress
4. ???

## 1) Trạng thái mạng

Không muốn nói gở, nhưng trong tuần vừa qua mạng hoạt động hầu như giống như trước - khá ổn định cho irc, eepsites(I2P Sites) tải đáng tin cậy, dù các tệp lớn vẫn thường phải tiếp tục tải lại. Về cơ bản thì không có gì mới để báo cáo, ngoài việc là chẳng có gì mới để báo cáo.

Ồ, một điều chúng tôi phát hiện là dù Jetty hỗ trợ tiếp tục tải (resume) qua HTTP, nó chỉ làm vậy với HTTP 1.1. Điều đó ổn với hầu hết trình duyệt và công cụ tải xuống, *ngoại trừ* wget - wget gửi yêu cầu tiếp tục tải dưới dạng HTTP 1.0. Vì vậy, khi tải các tệp lớn, hãy dùng curl hoặc một công cụ khác hỗ trợ tiếp tục tải qua HTTP 1.1 (cảm ơn duck và ardvark vì đã đào sâu và tìm ra giải pháp!)

## 2) Streaming lib (thư viện truyền dữ liệu dạng luồng)

Vì mạng đã khá ổn định, hầu như toàn bộ thời gian của tôi đã dành để phát triển streaming lib mới (thư viện xử lý truyền luồng dữ liệu). Mặc dù nó chưa hoàn thiện, đã có rất nhiều tiến triển - các kịch bản cơ bản đều hoạt động tốt, các cửa sổ trượt hoạt động hiệu quả cho việc tự điều nhịp, và lib mới hoạt động như một drop-in replacement (có thể thay thế trực tiếp) cho lib cũ, từ góc nhìn của phía client (tuy nhiên hai streaming lib không thể giao tiếp với nhau).

Vài ngày gần đây tôi đã xử lý thêm một số kịch bản thú vị. Quan trọng nhất là kịch bản mạng có độ trễ cao, mà chúng tôi mô phỏng bằng cách chèn độ trễ vào các thông điệp nhận được - hoặc một độ trễ ngẫu nhiên đơn giản 0-30s, hoặc một độ trễ phân tầng (80% thời gian có độ trễ 0-10s, 10% ở 10-20s, 5% ở 20-30s, 3% ở 30-40s, 4% ở 40-50s). Một phép thử quan trọng khác là việc loại bỏ ngẫu nhiên các thông điệp - điều này không thường gặp trên I2P, nhưng chúng ta nên có khả năng xử lý được.

Hiệu năng tổng thể đến giờ khá tốt, nhưng vẫn còn rất nhiều việc phải làm trước khi chúng ta có thể triển khai bản cập nhật này trên mạng đang hoạt động. Bản cập nhật này sẽ 'nguy hiểm' ở chỗ nó cực kỳ mạnh mẽ - nếu thực hiện sai trầm trọng, chúng ta có thể tự DDoS chính mình chỉ trong nháy mắt, nhưng nếu làm đúng, hãy để tôi nói rằng có rất nhiều tiềm năng (hứa ít, làm nhiều).

Nói vậy chứ, vì mạng hiện đang khá 'ổn định', tôi không vội phát hành thứ gì đó chưa được kiểm thử đủ kỹ. Sẽ có thêm tin khi có thêm tin.

## 3) tiến độ của mail.i2p

postman và nhóm đã và đang làm việc hết mình cho mail qua i2p (xem www.postman.i2p), và có một số thứ thú vị sắp tới - có lẽ postman có cập nhật cho chúng ta?

Nhân tiện, tôi hiểu và đồng cảm với các yêu cầu về một giao diện webmail, nhưng postman đang cực kỳ bận rộn làm một số thứ hay ho ở phần backend (phần chạy phía máy chủ) của hệ thống thư. Một giải pháp thay thế là cài đặt một giao diện webmail *cục bộ* trên máy chủ web của chính bạn - hiện có các ứng dụng webmail kiểu JSP/servlet ngoài kia. Như vậy bạn có thể chạy giao diện webmail cục bộ của riêng mình tại ví dụ: `http://localhost:7657/mail/`

Tôi biết có vài script mã nguồn mở ngoài kia để truy cập các tài khoản pop3, điều đó đưa chúng ta đi được nửa chặng đường - có lẽ ai đó có thể tìm xem có cái nào hỗ trợ pop3 và SMTP có xác thực không? Thôi nào, bạn biết là bạn muốn mà!

## 4) ???

Ok, hiện tại tôi chỉ có bấy nhiêu - ghé qua cuộc họp trong vài phút nữa và cho chúng tôi biết chuyện gì đang diễn ra.

=jr
