---
title: "Trợ Giúp Địa Chỉ Xác Thực"
number: "135"
author: "zzz"
created: "2017-02-25"
lastupdated: "2017-02-25"
status: "Open"
thread: "http://zzz.i2p/topics/2241"
toc: true
---

## Tổng Quan

Đề xuất này thêm cơ chế xác thực cho URL trợ giúp địa chỉ.


## Động Lực

Các URL trợ giúp địa chỉ vốn dĩ không an toàn. Bất kỳ ai cũng có thể đặt tham số trợ giúp địa chỉ trong một liên kết, thậm chí cho một hình ảnh, và có thể đặt bất kỳ đích đến nào trong tham số URL "i2paddresshelper". Tùy thuộc vào triển khai proxy HTTP của người dùng, ánh xạ tên máy chủ/đích đến này, nếu chưa có trong sổ địa chỉ, có thể được chấp nhận, hoặc có hoặc không có một trang trung gian để người dùng chấp nhận.


## Thiết Kế

Các máy chủ nhảy tin cậy và dịch vụ đăng ký sổ địa chỉ sẽ cung cấp các liên kết trợ giúp địa chỉ mới thêm các tham số xác thực. Hai tham số mới này sẽ là chữ ký dạng base 64 và chuỗi đã được ký bởi.

Các dịch vụ này sẽ tạo ra và cung cấp chứng chỉ khóa công khai. Chứng chỉ này sẽ có sẵn để tải xuống và đưa vào phần mềm proxy http. Người dùng và nhà phát triển phần mềm sẽ quyết định có tin tưởng dịch vụ như vậy bằng cách thêm chứng chỉ.

Khi gặp một liên kết trợ giúp địa chỉ, proxy http sẽ kiểm tra các tham số xác thực bổ sung và thử xác minh chữ ký. Khi xác minh thành công, proxy sẽ tiến hành như trước, bằng cách chấp nhận mục mới hoặc hiển thị trang trung gian cho người dùng. Khi xác minh thất bại, proxy có thể từ chối trợ giúp địa chỉ hoặc hiển thị thông tin bổ sung cho người dùng.

Nếu không có tham số xác thực, proxy http có thể chấp nhận, từ chối, hoặc trình bày thông tin cho người dùng.

Các dịch vụ nhảy sẽ được tin cậy như thường lệ, nhưng với bước xác thực bổ sung. Các liên kết trợ giúp địa chỉ trên các trang web khác sẽ cần được chỉnh sửa.


## Các Vấn Đề Bảo Mật

Đề xuất này thêm bảo mật bằng cách bổ sung xác thực từ các dịch vụ đăng ký / nhảy tin cậy. 


## Đặc Tả

TBD.

Hai tham số mới có thể là i2paddresshelpersig và i2paddresshelpersigner?

Các loại chữ ký được chấp nhận TBD. Có lẽ không phải là RSA vì chữ ký dạng base 64 sẽ rất dài.

Thuật toán chữ ký: TBD. Có thể chỉ là hostname=b64dest (giống như đề xuất 112 cho xác thực đăng ký)

Tham số mới thứ ba có thể có: Chuỗi xác thực đăng ký (phần sau "#!") sẽ được sử dụng để xác minh bổ sung bởi proxy HTTP. Bất kỳ "#" nào trong chuỗi sẽ cần phải được thoát như “&#35;” hoặc “&num;”, hoặc được thay thế bằng một ký tự khác an toàn cho URL (TBD).


## Di Cư

Các proxy HTTP cũ không hỗ trợ các tham số xác thực mới sẽ bỏ qua chúng và chuyển chúng đến máy chủ web, điều này không gây hại.

Các proxy HTTP mới mà hỗ trợ tùy chọn tham số xác thực sẽ hoạt động tốt với các liên kết trợ giúp địa chỉ cũ không chứa chúng.

Các proxy HTTP mới mà yêu cầu tham số xác thực sẽ không cho phép các liên kết trợ giúp địa chỉ cũ không chứa chúng.

Chính sách của một triển khai proxy có thể phát triển trong suốt quá trình di cư.

## Vấn Đề

Một chủ trang web không thể tạo ra một trợ giúp địa chỉ cho trang web của họ, vì cần có chữ ký từ một máy chủ nhảy tin cậy. Họ sẽ phải đăng ký trên máy chủ tin cậy và lấy URL trợ giúp địa chỉ có xác thực từ máy chủ đó. Có cách nào để một trang web tạo ra một URL trợ giúp địa chỉ tự xác thực không?

Ngoài ra, proxy có thể kiểm tra Referer cho một yêu cầu trợ giúp địa chỉ. Nếu Referer hiện diện, chứa một b32, và b32 khớp với đích đến của trợ giúp, thì nó có thể được cho phép như một giới thiệu tự động. Nếu không, có thể cho rằng đó là một yêu cầu của bên thứ ba và từ chối.
