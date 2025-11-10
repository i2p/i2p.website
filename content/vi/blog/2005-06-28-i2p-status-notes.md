---
title: "Ghi chú trạng thái I2P cho ngày 2005-06-28"
date: 2005-06-28
author: "jr"
description: "Cập nhật hàng tuần bao gồm các kế hoạch triển khai giao thức truyền tải SSU, việc hoàn tất chương trình tiền thưởng cho kiểm thử đơn vị và các cân nhắc về giấy phép, và trạng thái của Kaffe Java"
categories: ["status"]
---

Chào mọi người, lại đến giờ cập nhật hàng tuần rồi

* Index

1) Trạng thái SSU 2) Trạng thái kiểm thử đơn vị 3) Trạng thái Kaffe 4) ???

* 1) SSU status

Đã có thêm một số tiến triển đối với giao thức truyền tải SSU, và hiện tại tôi cho rằng sau khi tiến hành thêm một số thử nghiệm trên mạng thực, chúng tôi sẽ có thể triển khai phiên bản 0.6 mà không bị chậm trễ nhiều. Bản phát hành SSU đầu tiên sẽ không bao gồm hỗ trợ cho những người dùng không thể mở cổng trên tường lửa hoặc cấu hình NAT của họ, nhưng tính năng đó sẽ được triển khai trong 0.6.1. Sau khi 0.6.1 được phát hành, kiểm thử và chạy rất tốt (còn gọi là 0.6.1.42), chúng tôi sẽ chuyển sang 1.0.

Xu hướng cá nhân của tôi là loại bỏ hoàn toàn phương thức truyền tải TCP khi phương thức truyền tải SSU được triển khai, để mọi người không cần phải bật cả hai (chuyển tiếp cả cổng TCP và UDP) và để các lập trình viên không phải duy trì phần mã không còn cần thiết. Có ai có ý kiến mạnh mẽ về việc này không?

* 2) Unit test status

Như đã đề cập tuần trước, Comwiz đã đứng ra nhận giai đoạn đầu của khoản tiền thưởng cho kiểm thử đơn vị (unit test) (hoan hô Comwiz! cảm ơn duck & zab đã tài trợ khoản tiền thưởng nữa!). Mã nguồn đã được đưa vào CVS và, tùy thuộc vào thiết lập cục bộ của bạn, bạn có thể tạo báo cáo junit và clover bằng cách vào thư mục i2p/core/java và chạy "ant test junit.report" (đợi khoảng một giờ...) rồi xem i2p/reports/core/html/junit/index.html. Ngoài ra, bạn có thể chạy "ant useclover test junit.report clover.report" và xem i2p/reports/core/html/clover/index.html.

Điểm bất lợi của cả hai bộ kiểm thử có liên quan đến khái niệm ngớ ngẩn mà giai cấp cầm quyền gọi là "luật bản quyền". Clover là một sản phẩm thương mại, dù phía cenqua cho phép các nhà phát triển mã nguồn mở sử dụng miễn phí (và họ đã vui lòng đồng ý cấp cho chúng tôi một giấy phép). Để tạo các báo cáo Clover, bạn cần cài đặt Clover cục bộ - tôi có clover.jar trong ~/.ant/lib/, bên cạnh tệp giấy phép của tôi. Hầu hết mọi người sẽ không cần Clover, và vì chúng tôi sẽ công bố các báo cáo trên web, nên việc không cài đặt nó cũng không làm mất đi bất kỳ chức năng nào.

Mặt khác, khi xét đến chính bộ khung kiểm thử đơn vị, chúng ta lại bị vướng bởi một mặt khác của luật bản quyền - junit được phát hành theo IBM Common Public License 1.0, mà theo FSF [1], không tương thích với GPL. Hiện tại, dù bản thân chúng ta không có bất kỳ mã GPL nào (ít nhất là không trong lõi hoặc router), khi nhìn lại chính sách cấp phép của mình [2], mục tiêu của chúng ta trong cách cấp phép chi tiết là cho phép càng nhiều người càng tốt sử dụng những gì đang được tạo ra, vì ẩn danh cần số đông.

[1] http://www.fsf.org/licensing/licenses/index_html#GPLIncompatibleLicenses [2] http://www.i2p.net/licenses

Vì một số người, thật khó hiểu, lại phát hành phần mềm theo GPL, nên hợp lý là chúng tôi cố gắng cho phép họ sử dụng I2P mà không bị hạn chế. Ít nhất thì điều đó có nghĩa là chúng tôi không thể để chức năng thực tế mà chúng tôi cung cấp phụ thuộc vào mã theo giấy phép CPL (ví dụ: junit.framework.*). Tôi muốn mở rộng điều đó để bao gồm cả các bài kiểm thử đơn vị, nhưng junit có vẻ như là chuẩn chung của các framework kiểm thử (và tôi không nghĩ đó sẽ là một ý tưởng sáng suốt chút nào khi nói "này, hãy tự xây một framework kiểm thử đơn vị public domain (miền công cộng)!", xét nguồn lực của chúng tôi).

Với tất cả những điều đó, đề xuất của tôi như sau. Chúng tôi sẽ đóng gói kèm junit.jar trong CVS và sử dụng nó khi chạy các kiểm thử đơn vị, nhưng bản thân các kiểm thử đơn vị sẽ không được đưa vào i2p.jar hoặc router.jar, và sẽ không được phân phối trong các bản phát hành. Chúng tôi có thể cung cấp thêm một bộ JAR (i2p-test.jar và router-test.jar), nếu cần, nhưng các bộ đó sẽ không thể được các ứng dụng theo GPL sử dụng (vì chúng phụ thuộc vào junit).

=jr
