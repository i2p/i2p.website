---
title: "Hỗ trợ Floodfill cho các loại chữ ký tùy chọn"
number: "137"
author: "zzz"
created: "2017-03-31"
lastupdated: "2017-11-12"
status: "Mở"
thread: "http://zzz.i2p/topics/2280"
toc: true
---

## Tổng quan

Thêm cách để floodfills quảng cáo hỗ trợ các loại chữ ký tùy chọn. Điều này sẽ cung cấp cách để hỗ trợ các loại chữ ký mới trong dài hạn, ngay cả khi không phải tất cả các triển khai đều hỗ trợ chúng.


## Động lực

Đề xuất GOST 134 đã tiết lộ một số vấn đề với phạm vi loại chữ ký thử nghiệm chưa được sử dụng trước đây.

Đầu tiên, vì các loại chữ ký trong phạm vi thử nghiệm không thể được dành riêng, chúng có thể được sử dụng cho nhiều loại chữ ký cùng một lúc.

Thứ hai, trừ khi một thông tin router hoặc lease set với loại chữ ký thử nghiệm có thể được lưu trữ tại một floodfill, loại chữ ký mới sẽ khó để thử nghiệm hoặc sử dụng thử.

Thứ ba, nếu đề xuất 136 được thực hiện, đây không phải là an toàn, vì bất kỳ ai cũng có thể ghi đè một mục nhập.

Thứ tư, triển khai một loại chữ ký mới có thể là một nỗ lực phát triển lớn. Có thể khó thuyết phục các nhà phát triển cho tất cả các triển khai router thêm hỗ trợ cho một loại chữ ký mới kịp thời cho bất kỳ phiên bản cụ thể nào. Thời gian và động lực của nhà phát triển có thể khác nhau.

Thứ năm, nếu GOST sử dụng một loại chữ ký trong phạm vi tiêu chuẩn, vẫn không có cách nào để biết liệu một floodfill cụ thể có hỗ trợ GOST hay không.


## Thiết kế

Tất cả floodfills phải hỗ trợ các loại chữ ký DSA (0), ECDSA (1-3) và EdDSA (7).

Đối với bất kỳ loại chữ ký nào khác trong phạm vi tiêu chuẩn (không phải thử nghiệm), một floodfill có thể quảng cáo hỗ trợ trong các thuộc tính thông tin router của nó.


## Đặc tả


Một router hỗ trợ một loại chữ ký tùy chọn sẽ thêm thuộc tính "sigTypes" vào thông tin router đã công bố của nó, với các số loại chữ ký được tách bằng dấu phẩy. Các loại chữ ký sẽ được sắp xếp theo thứ tự số. Các loại chữ ký bắt buộc (0-4,7) sẽ không được bao gồm.

Ví dụ: sigTypes=9,10

Các router hỗ trợ các loại chữ ký tùy chọn phải chỉ lưu trữ, tìm kiếm hoặc phát tán, đến các floodfills quảng cáo hỗ trợ cho loại chữ ký đó.


## Di cư

Không áp dụng. Chỉ các router hỗ trợ một loại chữ ký tùy chọn mới phải triển khai.


## Vấn đề

Nếu không có nhiều floodfills hỗ trợ loại chữ ký, chúng có thể khó tìm.

Có thể không cần thiết yêu cầu ECDSA 384 và 521 (các loại chữ ký 2 và 3) cho tất cả floodfills. Các loại này không được sử dụng rộng rãi.

Các vấn đề tương tự sẽ cần được giải quyết với các loại mã hóa không bằng không, điều này chưa được đề xuất chính thức.


## Chú thích

NetDB lưu trữ các loại chữ ký không xác định không nằm trong phạm vi thử nghiệm sẽ tiếp tục bị từ chối bởi floodfills, vì chữ ký không thể được xác minh.


