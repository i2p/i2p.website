---
title: "Tùy Chọn Thông Điệp Xây Dựng Đường Hầm"
number: "143"
author: "zzz"
created: "2018-01-14"
lastupdated: "2022-01-28"
status: "Rejected"
thread: "http://zzz.i2p/topics/2500"
toc: true
---

## Lưu ý
Đề xuất này không được thực hiện theo chỉ định,
tuy nhiên, các thông điệp xây dựng dài và ngắn của ECIES (đề xuất 152 và 157)
được thiết kế với các trường tùy chọn mở rộng.
Xem [thông số kỹ thuật Tunnel Creation ECIES](/docs/specs/implementation/#tunnel-creation-ecies) để biết thông số kỹ thuật chính thức.


## Tổng quan

Thêm một cơ chế linh hoạt và mở rộng cho các tùy chọn trong các Bản ghi Xây dựng Đường hầm I2NP
nằm trong các thông điệp Xây dựng Đường hầm và Phản hồi Xây dựng Đường hầm.


## Động cơ


Có một vài đề xuất dự kiến chưa được tài liệu hóa để thiết lập tùy chọn hoặc cấu hình trong Thông điệp Xây dựng Đường hầm,
vì vậy người tạo đường hầm có thể truyền một số tham số đến mỗi trạm đường hầm.

Có 29 byte dự phòng trong TBM. Chúng tôi muốn duy trì sự linh hoạt cho các cải tiến tương lai, nhưng cũng sử dụng không gian một cách khôn ngoan.
Sử dụng cấu trúc 'mapping' sẽ dùng ít nhất 6 byte mỗi tùy chọn ("1a=1b;").
Định nghĩa thêm nhiều trường tùy chọn một cách cứng nhắc có thể gây ra vấn đề sau này.

Tài liệu này đề xuất một lược đồ ánh xạ tùy chọn mới và linh hoạt.


## Thiết kế

Chúng ta cần một biểu diễn tùy chọn vừa gọn gàng vừa linh hoạt, để có thể kết hợp nhiều
tùy chọn, với độ dài khác nhau, vào 29 byte.
Những tùy chọn này chưa được định nghĩa và không cần phải định nghĩa ở thời điểm này.
Không sử dụng cấu trúc "mapping" (mã hóa một đối tượng Java Properties), nó quá lãng phí.
Dùng một số để chỉ ra mỗi tùy chọn và độ dài, dẫn đến một mã hóa vừa gọn gàng vừa linh hoạt.
Tùy chọn phải được đăng ký theo số trong thông số kỹ thuật của chúng tôi, nhưng chúng tôi cũng sẽ dành một phạm vi cho các tùy chọn thử nghiệm.


## Thông số kỹ thuật

Sơ bộ - một số lựa chọn thay thế được mô tả dưới đây.

Điều này sẽ chỉ tồn tại nếu bit 5 trong cờ (byte 184) được đặt thành 1.

Mỗi tùy chọn là một số tùy chọn hai byte và độ dài, theo sau là các byte độ dài của giá trị tùy chọn.

Các tùy chọn bắt đầu từ byte 193 và tiếp tục cho đến tối đa byte 221 cuối cùng.

Số/độ dài tùy chọn:

Hai byte. Các bit 15-4 là số tùy chọn 12-bit, từ 1 đến 4095.
Các bit 3-0 là số byte giá trị tùy chọn theo sau, từ 0 đến 15.
Một tùy chọn boolean có thể có giá trị byte là không.
Chúng tôi sẽ duy trì một đăng ký các số tùy chọn trong các thông số kỹ thuật của chúng tôi, và cũng sẽ định nghĩa một phạm vi cho các tùy chọn thử nghiệm.

Giá trị tùy chọn là từ 0 đến 15 byte, để được diễn giải bởi bất cứ thứ gì cần tùy chọn đó. Các số tùy chọn không xác định nên được bỏ qua.

Các tùy chọn kết thúc với số/độ dài tùy chọn là 0/0, tức là hai byte 0.
 Phần còn lại của 29 byte, nếu có, nên được điền bằng đệm ngẫu nhiên, như thường lệ.

Mã hóa này tạo ra không gian cho 14 tùy chọn 0-byte, hoặc 9 tùy chọn 1-byte, hoặc 7 tùy chọn 2-byte.
Một lựa chọn khác là chỉ sử dụng một byte cho số/độ dài tùy chọn,
có thể với 5 bit cho số tùy chọn (tối đa 32) và 3 bit cho độ dài (tối đa 7).
Điều này sẽ tăng khả năng lên 28 tùy chọn 0-byte, 14 tùy chọn 1-byte, hoặc 9 tùy chọn 2-byte.
Chúng tôi cũng có thể làm cho nó biến đổi, nơi một số tùy chọn 5-bit của 31 có nghĩa là đọc thêm 8 bit cho số tùy chọn.

Nếu trạm đường hầm cần trả lại tùy chọn cho người tạo, chúng tôi có thể sử dụng cùng định dạng trong thông điệp phản hồi xây dựng đường hầm,
được đặt trước bằng một số ma thuật có nhiều byte (vì chúng tôi không có một byte cờ xác định để chỉ ra rằng tùy chọn có mặt).
Có 495 byte dự phòng trong TBRM.


## Ghi chú

Những thay đổi này là đối với các Bản ghi Xây dựng Đường hầm, và do đó có thể được sử dụng trong tất cả
các dạng Thông điệp Xây dựng - Yêu cầu Xây dựng Đường hầm, Yêu cầu Xây dựng Đường hầm Biến, Phản hồi Xây dựng Đường hầm, và Phản hồi Xây dựng Đường hầm Biến.


## Di cư

Không gian chưa sử dụng trong các Bản ghi Xây dựng Đường hầm được điền bằng dữ liệu ngẫu nhiên và hiện đang bị bỏ qua.
Không gian có thể được chuyển đổi để chứa các tùy chọn mà không gặp vấn đề di cư.
Trong thông điệp xây dựng, sự hiện diện của các tùy chọn được chỉ định trong byte cờ.
Trong thông điệp phản hồi xây dựng, sự hiện diện của các tùy chọn được chỉ định bằng một số ma thuật nhiều byte.
