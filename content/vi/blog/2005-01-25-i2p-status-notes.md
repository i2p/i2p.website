---
title: "Ghi chú trạng thái I2P ngày 2005-01-25"
date: 2005-01-25
author: "jr"
description: "Ghi chú tình hình phát triển I2P hàng tuần bao gồm tiến độ định tuyến tunnel trong 0.5, bản port SAM cho .NET, biên dịch bằng GCJ, và các thảo luận về cơ chế truyền tải UDP"
categories: ["status"]
---

Chào mọi người, cập nhật nhanh tình hình tuần này

* Index

1) trạng thái phiên bản 0.5 2) sam.net 3) tiến độ gcj 4) udp 5) ???

* 1) 0.5 status

Trong tuần vừa qua, đã có rất nhiều tiến triển ở nhánh 0.5. Các vấn đề mà chúng ta bàn luận trước đây đã được giải quyết, đơn giản hóa đáng kể phần mật mã và loại bỏ vấn đề vòng lặp tunnel (đường hầm). Kỹ thuật mới [1] đã được triển khai và các kiểm thử đơn vị đã được thiết lập. Tiếp theo, tôi đang ghép nối thêm mã để tích hợp các tunnel đó vào router chính (bộ định tuyến), rồi xây dựng hạ tầng quản lý và pooling (tạo pool) cho tunnel. Sau khi phần đó sẵn sàng, chúng tôi sẽ chạy nó qua sim (trình mô phỏng) và cuối cùng lên một mạng song song để kiểm thử độ bền, trước khi hoàn thiện và gọi nó là 0.5.

[1] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/tunnel-alt.html?rev=HEAD

* 2) sam.net

smeghead đã thực hiện một bản port mới của giao thức SAM sang .net - tương thích với c#, mono/gnu.NET (hoan hô smeghead!). Nó nằm trong cvs dưới i2p/apps/sam/csharp/ kèm theo nant và các công cụ hỗ trợ khác - giờ thì tất cả anh em dev .net có thể bắt đầu vọc i2p :)

* 3) gcj progress

smeghead đúng là đang tiến rất nhanh - tính đến lần kiểm tra gần nhất, với một vài chỉnh sửa, router đã biên dịch được trên bản build gcj [2] mới nhất (w00t!). Nó vẫn chưa hoạt động, nhưng các chỉnh sửa nhằm khắc phục sự nhầm lẫn của gcj với một số cấu trúc lớp lồng nhau chắc chắn là một bước tiến. Có lẽ smeghead có thể cho chúng ta một bản cập nhật?

[2] http://gcc.gnu.org/java/

* 4) udp

Không có nhiều điều để nói ở đây, tuy nhiên Nightblade đã nêu ra một loạt mối quan ngại thú vị [3] trên diễn đàn, đặt câu hỏi vì sao chúng tôi chọn sử dụng UDP. Nếu bạn có những mối quan ngại tương tự hoặc có đề xuất khác về cách chúng tôi có thể giải quyết những vấn đề mà tôi đã nêu trong phần trả lời, xin hãy góp ý!

[3] http://forum.i2p.net/viewtopic.php?t=280

* 5) ???

Ừ, được rồi, tôi lại trễ phần ghi chú nữa rồi, trừ lương tôi đi ;) Dù sao thì, có nhiều việc đang diễn ra, nên hoặc ghé qua kênh để dự họp, xem nhật ký đã đăng sau đó, hoặc đăng lên danh sách thư (mailing list) nếu bạn có điều gì muốn nói. À, nhân tiện, tôi đành nhượng bộ và bắt đầu một blog trên i2p [4].

=jr [4] http://jrandom.dev.i2p/ (khóa trong http://dev.i2p.net/i2p/hosts.txt)
