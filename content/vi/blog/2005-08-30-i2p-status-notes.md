---
title: "Ghi chú trạng thái I2P cho ngày 2005-08-30"
date: 2005-08-30
author: "jr"
description: "Bản cập nhật hàng tuần đề cập đến tình trạng mạng 0.6.0.3 với các vấn đề về NAT, việc triển khai floodfill netDb, và tiến độ quốc tế hóa của Syndie"
categories: ["status"]
---

Chào mọi người, lại đến thời điểm quen thuộc hằng tuần rồi.

* Index

1) Trạng thái mạng 2) floodfill netDb 3) Syndie 4) ???

* 1) Net status

Với 0.6.0.3 đã ra mắt được một tuần, các báo cáo nhìn chung khá tốt, dù việc ghi nhật ký và hiển thị đã gây khá nhiều nhầm lẫn cho một số người. Tính đến vài phút trước, I2P báo cáo rằng có một số lượng đáng kể người dùng đã cấu hình sai các NAT (biên dịch địa chỉ mạng) hoặc tường lửa của họ — trong tổng số 241 nút ngang hàng, 41 thấy trạng thái chuyển sang ERR-Reject, trong khi 200 thì hoàn toàn OK (khi họ có thể lấy được trạng thái tường minh). Điều này không tốt, nhưng nó đã giúp tập trung hơn vào những gì cần phải làm thêm.

Kể từ lần phát hành, đã có một vài bản sửa lỗi cho các lỗi tồn tại từ lâu, nâng CVS HEAD hiện tại lên 0.6.0.3-4, và nhiều khả năng sẽ được phát hành dưới dạng 0.6.0.4 trong tuần này.

* 2) floodfill netDb

Như đã thảo luận [1] trong blog của tôi [2], chúng tôi đang thử một netDb mới tương thích ngược, sẽ giải quyết cả tình trạng đường định tuyến bị hạn chế mà chúng tôi đang thấy (20% số router) và đồng thời đơn giản hóa mọi thứ một chút. floodfill netDb được triển khai như một phần của 0.6.0.3-4 mà không cần cấu hình thêm, và về cơ bản hoạt động bằng cách truy vấn trong floodfill db trước khi quay về kademlia db hiện có. Nếu vài người muốn giúp thử nghiệm, hãy nâng cấp lên 0.6.0.3-4 và thử xem sao!

[1] http://syndiemedia.i2p.net/index.jsp?selector=entry://ovpBy2mpO1CQ7deYhQ1cDGAwI6pQzLbWOm1Sdd0W06c=/1125100800001 [2] http://syndiemedia.i2p.net/index.jsp?blog=ovpBy2mpO1CQ7deYhQ1cDGAwI6pQzLbWOm1Sdd0W06c=

* 3) Syndie

Việc phát triển Syndie đang tiến triển khá tốt, với syndication (phân phối nội dung) từ xa đầy đủ đang vận hành và được tối ưu cho nhu cầu của I2P (giảm thiểu số lượng yêu cầu HTTP, thay vào đó gói chung kết quả trả về và nội dung tải lên trong các HTTP POST dạng multipart). Syndication từ xa mới có nghĩa là bạn có thể chạy phiên bản Syndie cục bộ của riêng mình, đọc và đăng bài khi ngoại tuyến, và sau đó đồng bộ Syndie của bạn với Syndie của người khác - tải xuống mọi bài viết mới và tải lên các bài viết được tạo cục bộ (có thể theo lô, theo blog, hoặc theo từng bài).

Một trang Syndie công cộng là syndiemedia.i2p (cũng có thể truy cập trên web tại http://syndiemedia.i2p.net/) với kho lưu trữ công khai có thể truy cập tại http://syndiemedia.i2p/archive/archive.txt (hãy trỏ nút Syndie của bạn đến đó để đồng bộ). 'trang chủ' trên syndiemedia đó đã được lọc để mặc định chỉ bao gồm blog của tôi, nhưng bạn vẫn có thể truy cập các blog khác thông qua menu thả xuống và điều chỉnh mặc định của bạn cho phù hợp. (Theo thời gian, mặc định của syndiemedia.i2p sẽ thay đổi thành một tập hợp các bài viết và blog giới thiệu, tạo một điểm khởi đầu tốt để bước vào syndie).

Một nỗ lực vẫn đang được tiến hành là quốc tế hóa mã nguồn của Syndie. Tôi đã chỉnh sửa bản sao cục bộ của mình để hoạt động đúng với mọi nội dung (bất kỳ bộ mã ký tự / locale (thiết lập vùng) / v.v.) trên bất kỳ máy nào (có thể có các bộ mã ký tự / locale / v.v. khác nhau), cung cấp dữ liệu sạch để trình duyệt của người dùng có thể diễn giải đúng. Tuy nhiên, tôi đã gặp vấn đề với một thành phần Jetty mà Syndie sử dụng, vì lớp của họ để xử lý các yêu cầu multipart đã quốc tế hóa không nhận biết bộ mã ký tự. Chưa ;)

Dù sao, điều đó có nghĩa là khi phần quốc tế hóa được xử lý xong, nội dung và blog sẽ có thể hiển thị và chỉnh sửa trên mọi ngôn ngữ (nhưng dĩ nhiên là chưa được dịch). Cho đến lúc đó, nội dung đã tạo có thể bị hỏng khi việc quốc tế hóa hoàn tất (vì có các chuỗi UTF-8 bên trong các vùng nội dung đã được ký). Nhưng cứ thoải mái thử nghiệm, và hy vọng tôi sẽ hoàn tất mọi thứ vào tối nay hoặc ngày mai.

Ngoài ra, một số ý tưởng vẫn đang trong lộ trình cho SML [3] bao gồm một thẻ [torrent attachment="1"]tệp của tôi[/torrent] cung cấp cách chỉ với một cú nhấp để cho phép mọi người khởi chạy torrent đính kèm trong client BT ưa thích của họ (susibt, i2p-bt, azneti2p, hoặc thậm chí một client BT không thuộc i2p). Có nhu cầu cho các loại hook (điểm móc) khác không (ví dụ một thẻ [ed2k]?), hay mọi người có những ý tưởng táo bạo hoàn toàn khác để phân phối nội dung trong Syndie?

[3] http://syndiemedia.i2p.net/index.jsp?blog=ovpBy2mpO1CQ7deYhQ1cDGAwI6pQzLbWOm1Sdd0W06c=&entry=1124496000000

* 4) ???

Dù sao đi nữa, có rất nhiều việc đang diễn ra, nên hãy ghé qua cuộc họp trong 10 phút nữa trên irc://irc.{postman,arcturus,freshcoffee}.i2p/#i2p hoặc freenode.net!

=jr
