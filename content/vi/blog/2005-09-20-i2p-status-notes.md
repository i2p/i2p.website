---
title: "Ghi chú trạng thái I2P cho ngày 2005-09-20"
date: 2005-09-20
author: "jr"
description: "Bản cập nhật hàng tuần bao gồm thành công của bản phát hành 0.6.0.6 với SSU introductions, bản cập nhật bảo mật I2Phex 0.1.1.27, và hoàn tất quá trình di chuyển colo (colocation)"
categories: ["status"]
---

Chào mọi người, lại là thứ Ba rồi

* Index:

1) 0.6.0.6 2) I2Phex 0.1.1.27 3) chuyển đổi 4) ???

* 1) 0.6.0.6

Với bản phát hành 0.6.0.6 vào thứ bảy vừa rồi, chúng tôi đã đưa một loạt thành phần mới vào mạng đang hoạt động, và mọi người đã làm rất tốt việc nâng cấp - tính đến vài giờ trước, gần 250 routers đã được nâng cấp! Mạng có vẻ cũng hoạt động tốt, và introductions (cơ chế giới thiệu) đến giờ vẫn đang hoạt động - bạn có thể theo dõi hoạt động introduction của riêng mình với http://localhost:7657/oldstats.jsp, bằng cách xem udp.receiveHolePunch và udp.receiveIntroRelayResponse (cũng như udp.receiveRelayIntro, đối với những người ở sau NAT).

Nhân tiện, "Status: ERR-Reject" giờ thực sự không còn là một lỗi nữa, vì vậy có lẽ chúng ta nên đổi thành "Status: OK (NAT)"?

Đã có vài báo cáo lỗi liên quan đến Syndie. Gần đây nhất, có một lỗi khiến nó sẽ không thể đồng bộ với các peer từ xa nếu bạn yêu cầu nó tải quá nhiều bài viết cùng lúc (vì tôi dại dột dùng HTTP GET thay vì POST). Tôi sẽ bổ sung hỗ trợ POST cho EepGet, nhưng trong lúc chờ, hãy thử chỉ tải 20 hoặc 30 bài viết mỗi lần. Nhân tiện, có lẽ ai đó có thể viết JavaScript cho trang remote.jsp để có tùy chọn “lấy tất cả bài viết từ người dùng này”, tự động đánh dấu tất cả các ô chọn (checkbox) trên blog của họ?

Nghe nói rằng hiện giờ OSX hoạt động tốt ngay sau khi cài đặt, và với 0.6.0.6-1, x86_64 cũng hoạt động trên cả Windows và Linux. Tôi chưa nghe báo cáo nào về sự cố với các trình cài đặt .exe mới, nên hoặc là mọi thứ đang diễn ra suôn sẻ, hoặc là nó hỏng hoàn toàn :)

* 2) I2Phex 0.1.1.27

Được thúc đẩy bởi một số báo cáo về sự khác biệt giữa mã nguồn và những gì được gói kèm trong gói phân phối 0.1.1.26 của legion, cũng như lo ngại về mức độ an toàn của trình khởi chạy native đóng mã nguồn, tôi đã tiến hành thêm một i2phex.exe mới được đóng gói bằng launch4j [1] vào cvs (hệ thống quản lý phiên bản) và biên dịch bản mới nhất từ cvs trên kho lưu trữ tệp I2P [2]. Chưa rõ liệu có những thay đổi nào khác do legion thực hiện đối với mã nguồn trước khi phát hành hay không, hoặc liệu mã nguồn mà anh ấy công bố có thực sự giống với bản mà anh ấy đã biên dịch hay không.

Vì lý do bảo mật, tôi không thể khuyến nghị sử dụng trình khởi chạy mã nguồn đóng của legion hoặc bản phát hành 0.1.1.26. Bản phát hành trên trang web I2P [2] chứa mã nguồn mới nhất từ cvs, không bị sửa đổi.

Bạn có thể tái tạo bản dựng bằng cách trước hết lấy mã nguồn và biên dịch I2P, sau đó lấy mã nguồn I2Phex, rồi chạy "ant makeRelease":   mkdir ~/devi2p ; cd ~/devi2p/   cvs -d :pserver:anoncvs-PQcCzt6076/R7s880joybQ@xxxxxxxxxxxxxxxx/cvsroot login

# (mật khẩu: anoncvs)

cvs -d :pserver:anoncvs-PQcCzt6076/R7s880joybQ@xxxxxxxxxxxxxxxx/cvsroot co i2p   cd i2p ; ant build ; cd ..   cvs -d :pserver:anoncvs-PQcCzt6076/R7s880joybQ@xxxxxxxxxxxxxxxx/cvsroot co i2phex   cd i2phex/build ; ant makeRelease ; cd ../..   ls -l i2phex/release/i2phex-0.1.1.27.zip

i2phex.exe bên trong tệp zip đó có thể sử dụng trên Windows chỉ bằng cách chạy nó, hoặc trên *nix/osx thông qua "java -jar i2phex.exe". Nó phụ thuộc vào việc I2Phex được cài đặt trong một thư mục nằm cạnh I2P - (ví dụ: C:\Program Files\i2phex\ và C:\Program Files\i2p\), vì nó tham chiếu đến một số tệp JAR của I2P.

Tôi sẽ không đứng ra duy trì I2Phex, nhưng tôi sẽ đưa các bản phát hành I2Phex trong tương lai lên trang web khi cvs được cập nhật. Nếu ai đó muốn làm một trang web để chúng ta có thể đăng lên nhằm mô tả/giới thiệu nó (sirup, bạn có ở đó không?), với các liên kết tới sirup.i2p, các bài viết hữu ích trên diễn đàn, danh sách các peers (nút ngang hàng) đang hoạt động của legion, thì tốt quá.

[1] http://launch4j.sourceforge.net/ [2] http://dev.i2p.net/i2p/i2phex-0.1.1.27.zip và     http://dev.i2p.net/i2p/i2phex-0.1.1.27.zip.sig (được ký bằng khóa của tôi)

* 3) migration

Chúng tôi đã chuyển đổi các colo boxes (máy chủ colocation) cho các dịch vụ I2P, nhưng hiện giờ mọi thứ trên máy chủ mới đã hoạt động đầy đủ - nếu bạn thấy điều gì bất thường, xin vui lòng cho tôi biết!

* 4) ???

Dạo gần đây đã có rất nhiều thảo luận thú vị trên danh sách thư i2p, proxy/filter SMTP mới khá hay của Adam, cũng như một số bài viết hay trên syndie (đã xem giao diện (skin) của gloin tại http://gloinsblog.i2p chưa?). Tôi hiện đang thực hiện một số thay đổi nhằm xử lý các vấn đề tồn tại đã lâu, nhưng chưa thể triển khai ngay. Nếu ai còn điều gì muốn nêu ra và thảo luận, hãy ghé cuộc họp tại #i2p lúc 8 giờ tối GMT (trong khoảng 10 phút nữa).

=jr
