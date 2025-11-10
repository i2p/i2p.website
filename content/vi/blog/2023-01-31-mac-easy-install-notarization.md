---
title: "Cập nhật về Notarization (dịch vụ chứng thực của Apple) cho Mac Easy Install"
date: 2023-01-31
author: "idk, sadie"
description: "Gói cài đặt dễ dàng cho Mac bị treo"
categories: ["release"]
---

Gói I2P Easy-Install cho Mac đã gặp tình trạng cập nhật bị đình trệ trong 2 bản phát hành vừa qua do người duy trì của nó đã rời đi. Khuyến nghị người dùng của gói Easy-Install cho Mac chuyển sang trình cài đặt kiểu Java cổ điển, vốn đã được khôi phục gần đây trên trang tải xuống. 1.9.0 có các vấn đề bảo mật đã biết và không phù hợp cho hosting services (dịch vụ lưu trữ) hoặc bất kỳ mục đích sử dụng dài hạn nào. Người dùng được khuyến cáo di chuyển khỏi bản này càng sớm càng tốt. Người dùng nâng cao của gói Easy-Install có thể khắc phục bằng cách biên dịch gói từ mã nguồn và tự ký phần mềm.

## Quy trình Notarization (chứng thực) cho MacOS

Có nhiều bước trong quy trình phân phối một ứng dụng đến người dùng Apple. Để phân phối ứng dụng dưới dạng .dmg một cách an toàn, ứng dụng phải vượt qua quy trình notarization (xác thực của Apple). Để gửi ứng dụng đi notarization, nhà phát triển phải ký ứng dụng bằng một bộ chứng chỉ, bao gồm một chứng chỉ dành cho code signing (ký mã) và một chứng chỉ để ký chính ứng dụng. Việc ký này phải được thực hiện tại các điểm cụ thể trong quá trình build, trước khi có thể tạo gói .dmg cuối cùng sẽ được phân phối tới người dùng cuối.

I2P Java là một ứng dụng phức tạp, và vì vậy việc ghép nối các loại mã được sử dụng trong ứng dụng với các chứng chỉ của Apple, cũng như xác định bước nào thực hiện ký để tạo ra dấu thời gian hợp lệ, là một quá trình thử và sai. Chính vì sự phức tạp này mà tài liệu hiện có dành cho nhà phát triển chưa đủ để giúp nhóm hiểu được sự kết hợp đúng đắn của các yếu tố sẽ dẫn đến notarization (quy trình chứng thực của Apple) thành công.

Những khó khăn này khiến khung thời gian để hoàn tất quy trình này trở nên khó dự đoán. Chúng tôi sẽ không biết là đã xong cho đến khi có thể dọn dẹp môi trường build và thực hiện quy trình từ đầu đến cuối. Tin vui là chúng tôi chỉ còn 4 lỗi trong quá trình chứng thực (notarization), giảm từ hơn 50 lỗi ở lần thử đầu tiên, và có thể dự đoán hợp lý rằng việc này sẽ được hoàn tất trước hoặc kịp thời cho bản phát hành tiếp theo vào tháng Tư.

## Tùy chọn cho cài đặt mới và cập nhật I2P trên macOS

Những người tham gia I2P mới vẫn có thể tải xuống Easy Installer cho phần mềm I2P 1.9.0 trên macOS. Tôi hy vọng sẽ có bản phát hành sẵn sàng vào khoảng cuối tháng Tư. Bản cập nhật lên phiên bản mới nhất sẽ được cung cấp ngay khi notarization (quy trình Apple chứng thực phần mềm) hoàn tất thành công.

Tùy chọn cài đặt cổ điển cũng có sẵn. Điều này sẽ yêu cầu tải xuống Java và phần mềm I2P thông qua trình cài đặt dựa trên .jar.

[Hướng dẫn cài đặt JAR có sẵn tại đây](https://geti2p.net/en/download/macos)

Người dùng Easy-Install có thể cập nhật lên phiên bản mới nhất đó bằng cách sử dụng một bản dựng phát triển được tạo cục bộ.

[Hướng dẫn xây dựng Easy-Install có sẵn tại đây](https://i2pgit.org/i2p-hackers/i2p-jpackage-mac/-/blob/master/BUILD.md)

Bạn cũng có thể gỡ cài đặt phần mềm, xóa thư mục cấu hình I2P và cài đặt lại I2P bằng trình cài đặt .jar.
