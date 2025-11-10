---
title: "Ghi chú trạng thái I2P cho ngày 2005-07-12"
date: 2005-07-12
author: "jr"
description: "Bản cập nhật hàng tuần về khôi phục dịch vụ, tiến độ thử nghiệm SSU và phân tích lớp mã hóa của I2CP để cân nhắc việc đơn giản hóa"
categories: ["status"]
---

Chào mọi người, lại đến lúc đó trong tuần rồi

* Index

1) squid/www/cvs/dev.i2p đã được khôi phục 2) kiểm thử SSU 3) mật mã I2CP 4) ???

* 1) squid/www/cvs/dev.i2p restored

Sau khi vật lộn với vài máy chủ colo, một số dịch vụ cũ đã được khôi phục - squid.i2p (một trong hai outproxies (proxy ra ngoài) mặc định), www.i2p (một liên kết an toàn tới www.i2p.net), dev.i2p (một liên kết an toàn tới dev.i2p.net, nơi có kho lưu trữ danh sách thư, cvsweb, và các seeds netDb mặc định), và cvs.i2p (một liên kết an toàn tới máy chủ CVS của chúng tôi - cvs.i2p.net:2401). Blog của tôi thì vẫn bặt vô âm tín, nhưng nội dung của nó vốn đã bị mất nên sớm muộn gì cũng sẽ phải bắt đầu lại từ đầu. Giờ đây khi các dịch vụ này đã trực tuyến ổn định trở lại, đã đến lúc chuyển sang...

* 2) SSU testing

Như đã đề cập trong ô nhỏ màu vàng trên bảng điều khiển router của mọi người, chúng tôi đã bắt đầu vòng thử nghiệm trực tiếp trên mạng tiếp theo cho SSU. Các thử nghiệm này không dành cho tất cả mọi người, nhưng nếu bạn ưa mạo hiểm và cảm thấy thoải mái khi thực hiện một số cấu hình thủ công, hãy xem các chi tiết được nêu trên bảng điều khiển router của bạn (http://localhost:7657/index.jsp). Có thể sẽ có vài vòng thử nghiệm, nhưng tôi không dự đoán sẽ có bất kỳ thay đổi lớn nào đối với SSU trước bản phát hành 0.6 (0.6.1 sẽ bổ sung hỗ trợ cho những người không thể chuyển tiếp cổng (port forwarding) của họ hoặc theo cách khác không thể nhận kết nối UDP đến).

* 3) I2CP crypto

Trong khi rà soát lại các tài liệu giới thiệu mới, tôi gặp chút khó khăn khi biện minh cho lớp mã hóa bổ sung được thực hiện trong I2CP SDK. Mục đích ban đầu của lớp mật mã của I2CP là cung cấp một mức bảo vệ đầu-cuối cơ bản cho các thông điệp được truyền, đồng thời cho phép các client I2CP (ví dụ như I2PTunnel, the SAM bridge, I2Phex, azneti2p, v.v.) giao tiếp thông qua các router không đáng tin cậy. Tuy nhiên, khi việc triển khai tiến triển, cơ chế bảo vệ đầu-cuối của lớp I2CP đã trở nên dư thừa, vì tất cả thông điệp của client đều được mã hóa đầu-cuối bên trong garlic messages (thông điệp garlic) bởi router, kèm theo leaseSet của bên gửi và đôi khi cả một thông điệp trạng thái giao nhận. Lớp garlic này vốn đã cung cấp mã hóa đầu-cuối từ router của bên gửi đến router của bên nhận; điểm khác biệt duy nhất là nó không bảo vệ trước trường hợp chính router đó là thù địch.

Tuy nhiên, khi xem xét các trường hợp sử dụng có thể dự liệu, tôi dường như không thể nghĩ ra một kịch bản hợp lý trong đó router (bộ định tuyến) cục bộ lại không được tin cậy. Ít nhất thì, cơ chế mật mã I2CP chỉ ẩn nội dung của thông điệp được truyền từ router - router vẫn cần biết nó phải được gửi tới đích nào. Nếu cần, chúng ta có thể thêm một SSH/SSL I2CP listener để cho phép I2CP client và router vận hành trên các máy riêng biệt, hoặc những người cần kiểu thiết lập như vậy có thể dùng các công cụ tunnel (đường hầm) hiện có.

Để nhắc lại các lớp mã hóa đang được sử dụng hiện nay, chúng ta có:  * Lớp ElGamal/AES+SessionTag đầu-cuối của I2CP, mã hóa từ    điểm đích của người gửi đến điểm đích của người nhận.  * Lớp garlic encryption đầu-cuối của router    (ElGamal/AES+SessionTag), mã hóa từ router của người gửi đến    router của người nhận.  * Lớp mã hóa tunnel cho cả các tunnel hướng vào và hướng ra    tại các chặng dọc theo từng tunnel (nhưng không giữa    điểm cuối hướng ra và cổng vào).  * Lớp mã hóa truyền tải giữa mỗi router.

Tôi muốn khá thận trọng khi loại bỏ một trong những lớp đó, nhưng tôi không muốn lãng phí tài nguyên của chúng ta vào công việc không cần thiết. Điều tôi đề xuất là bỏ lớp mã hóa I2CP đầu tiên (nhưng dĩ nhiên vẫn giữ cơ chế xác thực được dùng trong quá trình thiết lập phiên I2CP, ủy quyền leaseSet, và xác thực người gửi). Có ai nêu ra được lý do vì sao chúng ta nên giữ nó không?

* 4) ???

Tạm thời chỉ có vậy, nhưng như thường lệ vẫn còn rất nhiều việc đang diễn ra. Tuần này vẫn chưa có cuộc họp, nhưng nếu ai có điều gì muốn nêu ra, xin đừng ngần ngại đăng lên list (mailing list) hoặc lên diễn đàn. Ngoài ra, tuy tôi có đọc scrollback (lịch sử trò chuyện) trong #i2p, các câu hỏi hoặc mối quan ngại chung nên được gửi tới list thay vào đó để nhiều người có thể tham gia thảo luận.

=jr
