---
title: "Cài Đặt Các Plugin Tùy Chỉnh"
description: "Cài đặt, cập nhật và phát triển các plugin router"
slug: "plugins"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

Framework plugin của I2P cho phép bạn mở rộng router mà không cần chạm vào bản cài đặt lõi. Các plugin khả dụng bao gồm mail, blog, IRC, lưu trữ, wiki, công cụ giám sát và nhiều hơn nữa.

> **Lưu ý bảo mật:** Plugins chạy với quyền tương tự như router. Hãy đối xử với các bản tải xuống từ bên thứ ba giống như cách bạn đối xử với bất kỳ bản cập nhật phần mềm đã ký nào—xác minh nguồn trước khi cài đặt.

## 1. Cài đặt Plugin

1. Sao chép URL tải xuống của plugin từ trang dự án.  
   ![Copy plugin URL](/images/plugins/plugin-step-0.png)
2. Mở [trang Cấu hình Plugin](http://127.0.0.1:7657/configplugins) của router console.  
   ![Open plugin configuration](/images/plugins/plugin-step-1.png)
3. Dán URL vào trường cài đặt và nhấp **Install Plugin**.  
   ![Install plugin](/images/plugins/plugin-step-2.png)

Router tải xuống file nén đã ký, xác minh chữ ký, và kích hoạt plugin ngay lập tức. Hầu hết các plugin đều thêm liên kết console hoặc dịch vụ chạy nền mà không yêu cầu khởi động lại router.

## 2. Tại sao Plugins quan trọng

- Phân phối một cú nhấp chuột cho người dùng cuối—không cần chỉnh sửa thủ công `wrapper.config` hoặc `clients.config`
- Giữ gói `i2update.su3` cốt lõi nhỏ gọn trong khi cung cấp các tính năng lớn hoặc chuyên biệt theo yêu cầu
- JVM riêng cho từng plugin tùy chọn cung cấp cô lập tiến trình khi cần thiết
- Kiểm tra tương thích tự động với phiên bản router, Java runtime và Jetty
- Cơ chế cập nhật giống với router: các gói đã ký và tải xuống tăng dần
- Tích hợp console, gói ngôn ngữ, giao diện UI và các ứng dụng non-Java (thông qua scripts) đều được hỗ trợ
- Cho phép các thư mục "app store" được tuyển chọn như `plugins.i2p`

## 3. Quản lý các Plugin đã cài đặt

Sử dụng các điều khiển trên [I2P Router Plugin](http://127.0.0.1:7657/configclients.jsp#plugin) để:

- Kiểm tra cập nhật cho một plugin đơn lẻ
- Kiểm tra tất cả plugin cùng lúc (tự động kích hoạt sau khi nâng cấp router)
- Cài đặt bất kỳ bản cập nhật nào chỉ với một cú nhấp chuột  
  ![Cập nhật plugin](/images/plugins/plugin-update-0.png)
- Bật/tắt tự động khởi động cho các plugin đăng ký dịch vụ
- Gỡ cài đặt plugin một cách sạch sẽ

## 4. Xây dựng Plugin của riêng bạn

1. Xem lại [đặc tả plugin](/docs/specs/plugin/) để biết các yêu cầu về đóng gói, ký và metadata.
2. Sử dụng [`makeplugin.sh`](https://github.com/i2p/i2p.scripts/tree/master/plugin/makeplugin.sh) để đóng gói một tệp binary hoặc webapp hiện có thành một archive có thể cài đặt.
3. Công bố cả URL cài đặt và URL cập nhật để router có thể phân biệt giữa lần cài đặt đầu tiên và các nâng cấp dần dần.
4. Cung cấp checksum và khóa ký một cách rõ ràng trên trang dự án của bạn để giúp người dùng xác minh tính xác thực.

Đang tìm ví dụ? Duyệt mã nguồn của các plugin cộng đồng trên `plugins.i2p` (ví dụ như mẫu `snowman`).

## 5. Các Hạn Chế Đã Biết

- Cập nhật plugin cung cấp các file JAR thông thường có thể yêu cầu khởi động lại router vì Java class loader lưu cache các class.
- Console có thể hiển thị nút **Stop** ngay cả khi plugin không có tiến trình hoạt động nào.
- Các plugin được chạy trong JVM riêng biệt sẽ tạo thư mục `logs/` trong thư mục làm việc hiện tại.
- Lần đầu tiên một khóa ký xuất hiện, nó sẽ được tin cậy tự động; không có cơ quan ký trung tâm nào.
- Windows đôi khi để lại các thư mục trống sau khi gỡ cài đặt plugin.
- Cài đặt plugin chỉ dành cho Java 6 trên JVM Java 5 sẽ báo lỗi "plugin is corrupt" do nén Pack200.
- Các plugin theme và translation phần lớn chưa được kiểm tra kỹ.
- Cờ autostart không phải lúc nào cũng được giữ lại đối với các unmanaged plugin.

## 6. Yêu Cầu & Thực Hành Tốt Nhất

- Hỗ trợ plugin có sẵn trong I2P **phiên bản 0.7.12 trở lên**.
- Giữ router và plugin của bạn luôn cập nhật để nhận các bản vá bảo mật.
- Đính kèm ghi chú phát hành ngắn gọn để người dùng hiểu những thay đổi giữa các phiên bản.
- Khi có thể, lưu trữ các file plugin qua HTTPS bên trong I2P để giảm thiểu việc để lộ metadata trên mạng công cộng.

## 7. Đọc Thêm

- [Đặc tả plugin](/docs/specs/plugin/)
- [Framework ứng dụng client](/docs/applications/managed-clients/)
- [Kho I2P scripts](https://github.com/i2p/i2p.scripts/) cho các tiện ích đóng gói
