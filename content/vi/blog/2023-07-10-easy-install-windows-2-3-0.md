---
title: "Đã phát hành Easy-Install cho Windows 2.3.0"
date: 2023-07-10
author: "idk"
description: "Easy-Install dành cho Windows 2.3.0 đã được phát hành"
categories: ["release"]
---

I2P Easy-Install bundle cho Windows phiên bản 2.3.0 hiện đã được phát hành. Như thường lệ, bản phát hành này bao gồm một phiên bản cập nhật của I2P router. Điều này cũng mở rộng tới các vấn đề bảo mật ảnh hưởng đến những người vận hành dịch vụ trên mạng.

Đây sẽ là bản phát hành cuối cùng của gói Easy-Install mà không tương thích với I2P Desktop GUI. Gói này đã được cập nhật để bao gồm các phiên bản mới của tất cả các phần mở rộng web đi kèm. Một lỗi tồn tại từ lâu trong I2P in Private Browsing khiến nó không tương thích với các chủ đề tùy chỉnh đã được khắc phục. Người dùng vẫn được khuyến nghị *không* cài đặt chủ đề tùy chỉnh. Các thẻ Snark không được tự động ghim lên đầu thứ tự thẻ trong Firefox. Ngoại trừ việc sử dụng cookieStores thay thế, các thẻ Snark giờ hoạt động như các thẻ trình duyệt thông thường.

**Rất tiếc, bản phát hành này vẫn là trình cài đặt `.exe` chưa được ký.** Vui lòng xác minh checksum của trình cài đặt trước khi sử dụng. **Còn các bản cập nhật** được ký bằng các khóa ký I2P của tôi nên an toàn.

Bản phát hành này được biên dịch bằng OpenJDK 20. Bản này sử dụng i2p.plugins.firefox phiên bản 1.1.0 làm thư viện để khởi chạy trình duyệt. Nó sử dụng i2p.i2p phiên bản 2.3.0 như một I2P router (trình định tuyến I2P), đồng thời cung cấp các ứng dụng. Như thường lệ, khuyến nghị bạn cập nhật lên phiên bản mới nhất của I2P router vào thời điểm thuận tiện sớm nhất.

- [Easy-Install Bundle Source](http://git.idk.i2p/i2p-hackers/i2p.firefox/-/tree/i2p-firefox-2.3.0)
- [Router Source](http://git.idk.i2p/i2p-hackers/i2p.i2p/-/tree/i2p-2.3.0)
- [Profile Manager Source](http://git.idk.i2p/i2p-hackers/i2p.plugins.firefox/-/tree/1.1.0)
