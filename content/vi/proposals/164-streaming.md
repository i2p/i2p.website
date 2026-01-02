---
title: "Cập Nhật Streaming"
number: "164"
author: "zzz"
created: "2023-01-24"
lastupdated: "2023-10-23"
status: "Closed"
thread: "http://zzz.i2p/topics/3541"
target: "0.9.58"
implementedin: "0.9.58"
toc: true
---

## Tổng Quan

Các router Java I2P và i2pd cũ hơn API 0.9.58 (phát hành tháng 3 năm 2023)
dễ bị tấn công phát lại gói dữ liệu SYN trong streaming.
Đây là vấn đề trong thiết kế giao thức, không phải lỗi thực thi.

Các gói SYN được ký, nhưng chữ ký của gói SYN ban đầu gửi từ Alice tới Bob
không gắn với danh tính của Bob, nên Bob có thể lưu trữ và phát lại gói đó,
gửi nó tới một nạn nhân Charlie. Charlie sẽ nghĩ rằng gói đó đến từ
Alice và phản hồi lại cô. Trong hầu hết các trường hợp, điều này vô hại, nhưng
gói SYN có thể chứa dữ liệu ban đầu (như GET hoặc POST) mà
Charlie sẽ xử lý ngay lập tức.


## Thiết Kế

Giải pháp là Alice đưa vào hash đích của Bob trong dữ liệu SYN đã ký.
Bob xác minh khi nhận rằng hash đó khớp với hash của mình.

Bất kỳ nạn nhân tiềm năng nào Charlie
kiểm tra dữ liệu này và từ chối SYN nếu nó không khớp với hash của anh ta.

Bằng cách sử dụng trường tùy chọn NACKs trong SYN để lưu trữ hash,
sự thay đổi này tương thích ngược, vì NACKs không được kỳ vọng có trong
gói SYN và hiện tại cũng bị bỏ qua.

Tất cả các tùy chọn đều được bảo vệ bởi chữ ký, như thường lệ, nên Bob không thể
viết lại hash.

Nếu Alice và Charlie sử dụng API 0.9.58 hoặc mới hơn, mọi nỗ lực phát lại của Bob sẽ bị từ chối.


## Đặc Tả

Cập nhật [đặc tả Streaming](/docs/specs/streaming/) để thêm phần sau:

### Phòng Ngừa Phát Lại

Để ngăn Bob sử dụng tấn công phát lại bằng cách lưu trữ một gói SYNCHRONIZE đã ký hợp lệ
nhận từ Alice và sau đó gửi nó đến một nạn nhân Charlie,
Alice phải đưa vào hash đích của Bob trong gói SYNCHRONIZE như sau:

.. raw:: html

  {% highlight lang='dataspec' %}
Set NACK count field to 8
  Set the NACKs field to Bob's 32-byte destination hash

{% endhighlight %}

Khi nhận được một SYNCHRONIZE, nếu trường đếm NACK là 8,
Bob phải diễn giải trường NACKs là một hash đích 32-byte,
và phải xác minh rằng nó khớp với hash đích của mình.
Anh ta cũng phải xác minh chữ ký của gói như thường lệ,
vì nó bao phủ toàn bộ gói bao gồm trường đếm NACK và NACKs.
Nếu đếm NACK là 8 và trường NACKs không khớp,
Bob phải loại bỏ gói.

Điều này là cần thiết cho các phiên bản từ 0.9.58 trở lên.
Điều này tương thích ngược với các phiên bản cũ hơn,
vì các NACKs không được kỳ vọng có trong gói SYNCHRONIZE.
Các đích không và không thể biết phiên bản mà phía đối diện đang chạy.

Không cần thiết phải thay đổi gì cho gói SYNCHRONIZE ACK gửi từ Bob tới Alice;
đừng đưa NACKs vào gói đó.


## Phân Tích Bảo Mật

Vấn đề này đã xuất hiện trong giao thức streaming từ khi nó được tạo ra vào năm 2004.
Nó được phát hiện nội bộ bởi các nhà phát triển I2P.
Chúng tôi không có bằng chứng nào cho thấy vấn đề này đã từng bị khai thác.
Khả năng thành công của việc khai thác thực tế có thể thay đổi rất nhiều
tùy thuộc vào giao thức lớp ứng dụng và dịch vụ.
Các ứng dụng peer-to-peer có thể bị ảnh hưởng nhiều hơn
so với các ứng dụng client/server.


## Tương Thích

Không có vấn đề nào. Tất cả các thực thi được biết đến hiện nay đều bỏ qua trường NACKs trong gói SYN.
Và ngay cả nếu chúng không bỏ qua nó, và cố gắng diễn giải nó
như NACKs cho 8 thông điệp khác nhau, các thông điệp đó sẽ không còn nổi bật
trong quá trình bắt tay SYNCHRONIZE và NACKs sẽ không có nghĩa gì.


## Di Cư

Các thực thi có thể thêm hỗ trợ bất cứ lúc nào, không cần phối hợp.
Các router Java I2P và i2pd đã thực thi điều này trong API 0.9.58 (phát hành tháng 3 năm 2023).


