---
title: "Bản phát hành Windows Easy-Install 2.1.0"
date: 2023-01-13
author: "idk"
description: "Windows Easy-Install Bundle 2.1.0 được phát hành nhằm cải thiện độ ổn định và hiệu năng"
categories: ["release"]
---

## Chi tiết cập nhật

Gói Easy-Install của I2P cho Windows phiên bản 2.1.0 đã được phát hành. Như thường lệ, bản phát hành này bao gồm một phiên bản I2P Router đã được cập nhật. Bản phát hành I2P này đưa ra các chiến lược cải tiến để xử lý tình trạng tắc nghẽn mạng. Những chiến lược này sẽ giúp cải thiện hiệu năng, khả năng kết nối và bảo đảm sức khỏe lâu dài của mạng I2P.

Bản phát hành này chủ yếu mang đến các cải tiến nội bộ cho trình khởi chạy hồ sơ trình duyệt. Khả năng tương thích với Tor Browser Bundle đã được cải thiện bằng cách cho phép cấu hình TBB thông qua các biến môi trường. Hồ sơ Firefox đã được cập nhật, và các phiên bản cơ sở của các tiện ích mở rộng đã được cập nhật. Các cải tiến đã được thực hiện xuyên suốt mã nguồn và quy trình triển khai.

Unfortunately, this release is still an unsigned .exe installer. Please verify the checksum of the installer before using it. The updates, on the other hand are signed by my I2P signing keys and therefore safe.

Bản phát hành này được biên dịch với OpenJDK 19. Nó sử dụng i2p.plugins.firefox phiên bản 1.0.7 làm thư viện để khởi chạy trình duyệt. Nó sử dụng i2p.i2p phiên bản 2.1.0 như một I2P router, và để cung cấp các ứng dụng. Như thường lệ, bạn nên cập nhật lên phiên bản mới nhất của I2P router vào thời điểm thuận tiện sớm nhất.
