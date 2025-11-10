---
title: "Bản phát hành Windows Easy-Install Bundle 1.9.0"
date: 2022-08-28
author: "idk"
description: "Windows Easy-Install Bundle 1.9.0 - Cải tiến lớn về độ ổn định/khả năng tương thích"
categories: ["release"]
---

## Bản cập nhật này bao gồm router 1.9.0 mới và các cải tiến lớn về chất lượng sử dụng dành cho người dùng gói cài đặt

Bản phát hành này bao gồm router I2P 1.9.0 mới và được xây dựng dựa trên Java 18.02.1.

Các tập lệnh batch cũ đã được loại bỏ dần để nhường chỗ cho một giải pháp linh hoạt và ổn định hơn ngay trong chính jpackage. Điều này sẽ khắc phục tất cả các lỗi liên quan đến việc tìm đường dẫn và đặt dấu ngoặc kép cho đường dẫn vốn tồn tại trong các tập lệnh batch. Sau khi bạn nâng cấp, các tập lệnh batch có thể được xóa một cách an toàn. Chúng sẽ được trình cài đặt gỡ bỏ trong bản cập nhật tiếp theo.

Một dự án phụ để quản lý các công cụ duyệt web đã được khởi động: i2p.plugins.firefox, có khả năng mạnh mẽ trong việc cấu hình các trình duyệt I2P một cách tự động và ổn định trên nhiều nền tảng. Giải pháp này đã được dùng để thay thế các tập lệnh batch nhưng đồng thời cũng hoạt động như một công cụ quản lý I2P Browser đa nền tảng. Mọi đóng góp đều được hoan nghênh tại kho mã nguồn: http://git.idk.i2p/idk/i2p.plugins.firefox

Bản phát hành này cải thiện khả năng tương thích với các I2P routers chạy bên ngoài, chẳng hạn như những router do trình cài đặt IzPack cung cấp và các triển khai router của bên thứ ba như i2pd. Nhờ cải thiện cơ chế phát hiện router bên ngoài, nó sử dụng ít tài nguyên hệ thống hơn, rút ngắn thời gian khởi động và ngăn ngừa xung đột tài nguyên.

Ngoài ra, hồ sơ đã được cập nhật lên phiên bản Arkenfox mới nhất. I2P trong chế độ Duyệt web riêng tư và NoScript đều đã được cập nhật. Hồ sơ đã được tái cấu trúc nhằm cho phép đánh giá các cấu hình khác nhau cho các mô hình đe dọa khác nhau.
