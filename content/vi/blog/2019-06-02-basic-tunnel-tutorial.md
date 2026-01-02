---
title: "Hướng dẫn cơ bản về I2P Tunnels (đường hầm) kèm hình minh họa"
date: 2019-06-02
author: "idk"
description: "Thiết lập i2ptunnel cơ bản"
categories: ["tutorial"]
---

Mặc dù router I2P Java được cấu hình sẵn với một máy chủ web tĩnh, jetty, để cung cấp eepSite đầu tiên cho người dùng, nhiều người dùng cần các tính năng nâng cao hơn từ máy chủ web của họ và muốn tạo một eepSite với một máy chủ khác. Điều này dĩ nhiên là có thể, và thực ra rất dễ sau khi bạn đã làm một lần.

Mặc dù việc này khá dễ thực hiện, bạn vẫn nên cân nhắc một vài điều trước khi tiến hành. Bạn sẽ muốn loại bỏ các đặc điểm nhận dạng khỏi máy chủ web của mình, chẳng hạn như các header có thể tiết lộ danh tính và các trang lỗi mặc định tiết lộ loại máy chủ/bản phân phối (distro). Để biết thêm thông tin về các mối đe dọa đối với tính ẩn danh do ứng dụng cấu hình không đúng gây ra, xem: [Riseup tại đây](https://riseup.net/en/security/network-security/tor/onionservices-best-practices), [Whonix tại đây](https://www.whonix.org/wiki/Onion_Services), [bài viết blog này về một số sai sót opsec](https://blog.0day.rocks/securing-a-web-hidden-service-89d935ba1c1d), [và trang ứng dụng I2P tại đây](https://geti2p.net/docs/applications/supported). Mặc dù phần lớn thông tin này được trình bày cho Dịch vụ Onion của Tor, các quy trình và nguyên tắc tương tự cũng áp dụng cho việc lưu trữ ứng dụng qua I2P.

### Bước Một: Mở trình hướng dẫn Tunnel

Truy cập giao diện web I2P tại 127.0.0.1:7657 và mở [Trình quản lý Dịch vụ Ẩn](http://127.0.0.1:7657/i2ptunnelmgr) (liên kết tới localhost). Nhấp vào nút có ghi "Tunnel Wizard" để bắt đầu.

### Bước Hai: Chọn một Server Tunnel

Trình hướng dẫn tunnel rất đơn giản. Vì chúng ta đang thiết lập một *máy chủ* http, tất cả những gì chúng ta cần làm là chọn một tunnel *máy chủ*.

### Bước Ba: Chọn một HTTP Tunnel

HTTP tunnel là loại tunnel được tối ưu để lưu trữ các dịch vụ HTTP. Nó có các tính năng lọc và giới hạn tốc độ được bật sẵn, được điều chỉnh cụ thể cho mục đích đó. Một tunnel tiêu chuẩn cũng có thể hoạt động, nhưng nếu bạn chọn tunnel tiêu chuẩn thì bạn sẽ phải tự xử lý các tính năng bảo mật đó. Phần tìm hiểu sâu hơn về cấu hình HTTP Tunnel được trình bày trong hướng dẫn tiếp theo.

### Bước 4: Đặt tên và mô tả

Vì lợi ích của chính bạn và để dễ ghi nhớ cũng như phân biệt mục đích sử dụng tunnel (đường hầm), hãy đặt cho nó một biệt danh và mô tả phù hợp. Nếu sau này bạn cần quay lại để quản lý thêm, thì đây sẽ là cách bạn nhận diện tunnel trong Trình quản lý Dịch vụ Ẩn.

### Bước Năm: Cấu hình máy chủ và cổng

Ở bước này, bạn trỏ máy chủ web tới cổng TCP mà máy chủ web của bạn đang lắng nghe. Vì hầu hết máy chủ web lắng nghe trên cổng 80 hoặc 8080, ví dụ thể hiện điều đó. Nếu bạn dùng các cổng khác hoặc máy ảo hay container để cô lập dịch vụ web của mình, bạn có thể cần điều chỉnh máy chủ, cổng, hoặc cả hai.

### Bước Sáu: Quyết định có tự động khởi động nó hay không

Tôi không thể nghĩ ra cách nào để trình bày chi tiết hơn về bước này.

### Bước Bảy: Xem lại cài đặt của bạn

Cuối cùng, hãy kiểm tra lại các cài đặt bạn đã chọn. Nếu bạn hài lòng, hãy lưu lại. Nếu bạn không chọn khởi động tunnel (đường hầm) tự động, hãy vào trình quản lý dịch vụ ẩn và khởi động nó thủ công khi bạn muốn dịch vụ của mình sẵn sàng.

### Phụ lục: Tùy chọn tùy chỉnh máy chủ HTTP

I2P cung cấp một bảng điều khiển chi tiết để cấu hình tunnel máy chủ HTTP theo nhiều cách tùy biến. Tôi sẽ hoàn tất hướng dẫn này bằng cách lần lượt đi qua tất cả chúng. Sớm muộn gì cũng xong.
