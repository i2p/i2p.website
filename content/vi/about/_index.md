---
title: "Về I2P"
description: "Tìm hiểu về The Invisible Internet Project - một mạng phủ ngang hàng, mã hóa hoàn toàn được thiết kế cho liên lạc ẩn danh."
tagline: "The Invisible Internet Project"
type: "about"
layout: "about"
established: "2002"
---

The Invisible Internet Project bắt đầu vào năm 2002. Tầm nhìn của dự án là mạng I2P "cung cấp sự ẩn danh, quyền riêng tư và an ninh ở mức độ cao nhất có thể. Internet phi tập trung và ngang hàng đồng nghĩa với việc không cần lo lắng về nhà cung cấp dịch vụ internet kiểm soát lưu lượng truy cập của bạn. Điều này sẽ cho phép mọi người thực hiện các hoạt động liền mạch và thay đổi cách chúng ta nhìn nhận về an ninh và thậm chí là Internet, sử dụng mật mã khóa công khai, che giấu địa chỉ IP và xác thực thông điệp. Internet mà đáng lẽ phải có, sẽ sớm xuất hiện."

Kể từ đó, I2P đã phát triển để xác định và thực hiện một bộ giao thức mạng hoàn chỉnh có khả năng cung cấp mức độ quyền riêng tư, an ninh và xác thực cao cho một loạt ứng dụng.

## Mạng I2P

Mạng I2P là một mạng phủ ngang hàng mã hóa hoàn toàn. Một người quan sát không thể nhìn thấy nội dung, nguồn gốc hay đích đến của một thông điệp. Không ai có thể thấy lưu lượng truy cập đến từ đâu, đi đến đâu, hay nội dung là gì. Ngoài ra, các phương tiện vận chuyển của I2P còn có khả năng chống nhận diện và chặn bởi những người kiểm duyệt. Bởi vì mạng phụ thuộc vào các thành viên để điều hướng lưu lượng, việc chặn theo địa điểm trở thành một thách thức tăng theo sự phát triển của mạng. Mỗi bộ định tuyến trong mạng tham gia vào việc làm cho mạng trở nên ẩn danh. Trừ khi không an toàn, mọi người đều tham gia vào việc gửi và nhận lưu lượng mạng.

## Cách Kết Nối với Mạng I2P

Phần mềm cốt lõi (Java) bao gồm một bộ định tuyến giới thiệu và duy trì một kết nối với mạng. Nó cũng cung cấp các ứng dụng và tùy chọn cấu hình để cá nhân hóa trải nghiệm và quy trình làm việc của bạn. Tìm hiểu thêm trong [tài liệu của chúng tôi](/docs/).

## Tôi Có Thể Làm Gì Trên Mạng I2P?

Mạng cung cấp một lớp ứng dụng cho các dịch vụ, ứng dụng, và quản lý mạng. Mạng cũng có riêng hệ thống DNS cho phép tự lưu trữ và phản chiếu nội dung từ Internet (Clearnet). Mạng I2P hoạt động giống như Internet. Phần mềm Java bao gồm một máy khách BitTorrent, và email cũng như một mẫu trang web tĩnh. Các ứng dụng khác có thể dễ dàng thêm vào bảng điều khiển bộ định tuyến của bạn.

## Tổng Quan Về Mạng

I2P sử dụng mật mã để đạt được một loạt các thuộc tính cho các hầm mà nó tạo ra và các giao tiếp mà nó vận chuyển. Các hầm I2P sử dụng các phương tiện vận chuyển, [NTCP2](/docs/specs/ntcp2/) và [SSU2](/docs/specs/ssu2/), để che giấu lưu lượng được vận chuyển qua nó. Các kết nối được mã hóa từ bộ định tuyến đến bộ định tuyến, và từ máy khách đến máy khách (từ đầu cuối đến đầu cuối). Bảo mật tiếp nối được cung cấp cho tất cả các kết nối. Bởi vì I2P sử dụng địa chỉ mật mã, địa chỉ mạng I2P tự xác thực và chỉ thuộc về người dùng đã tạo ra chúng.

Mạng được tạo thành từ các thành viên ("bộ định tuyến") và các hầm ảo chỉ hướng vào và ra. Các bộ định tuyến giao tiếp với nhau sử dụng các giao thức được xây dựng trên các cơ chế vận chuyển hiện có (TCP, UDP), truyền thông điệp. Các ứng dụng khách có mã định danh mật mã riêng ("Đích Đích") cho phép nó gửi và nhận thông điệp. Những máy khách này có thể kết nối với bất kỳ bộ định tuyến nào và ủy quyền cho việc phân bổ tạm thời ("một phần") một số hầm sẽ được sử dụng để gửi và nhận thông điệp qua mạng. I2P có cơ sở dữ liệu mạng nội bộ riêng (sử dụng một sự điều chỉnh của Kademlia DHT) để phân phối thông tin điều hướng và liên lạc một cách an toàn.

## Về Phi Tập Trung và Mạng I2P

Mạng I2P gần như hoàn toàn phi tập trung, ngoại trừ những gì được gọi là Máy chủ Reseed. Điều này là để giải quyết vấn đề khởi động DHT (Bảng băm phân phối). Về cơ bản, không có cách tốt nào đáng tin cậy để tránh chạy ít nhất một nút khởi động vĩnh viễn mà những người không tham gia mạng có thể tìm thấy để bắt đầu. Khi đã kết nối với mạng, một bộ định tuyến chỉ phát hiện các thành viên bằng cách xây dựng các hầm "khám phá", nhưng để tạo kết nối ban đầu, một máy chủ reseed cần được yêu cầu để tạo kết nối và đưa bộ định tuyến mới tham gia mạng. Máy chủ Reseed có thể quan sát khi một bộ định tuyến mới đã tải xuống reseed từ chúng, nhưng không có gì khác về lưu lượng trên mạng I2P.

## So Sánh

Có rất nhiều ứng dụng và dự án khác đang làm về liên lạc ẩn danh và I2P đã được truyền cảm hứng rất nhiều từ những nỗ lực của họ. Đây không phải là danh sách toàn diện về các tài nguyên ẩn danh - cả [Thư mục ẩn danh của freehaven](http://freehaven.net/anonbib/topic.html) và [các dự án liên quan của GNUnet](https://www.gnunet.org/links/) đều phục vụ mục đích đó rất tốt. Nói như vậy, một số hệ thống nổi bật hơn để so sánh thêm. Tìm hiểu thêm về cách I2P so sánh với các mạng ẩn danh khác trong [tài liệu so sánh chi tiết của chúng tôi](/docs/overview/comparison/).
