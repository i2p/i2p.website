---
title: "Cài đặt I2P trên macOS (Cách Thủ Công)"
description: "Hướng dẫn từng bước để cài đặt thủ công I2P và các gói phụ thuộc trên macOS"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## Những Gì Bạn Cần

- Máy Mac chạy macOS 10.14 (Mojave) trở lên
- Quyền quản trị viên để cài đặt ứng dụng
- Khoảng 15-20 phút
- Kết nối Internet để tải các trình cài đặt

## Tổng quan

Quá trình cài đặt này có bốn bước chính:

1. **Cài đặt Java** - Tải xuống và cài đặt Oracle Java Runtime Environment
2. **Cài đặt I2P** - Tải xuống và chạy trình cài đặt I2P
3. **Cấu hình ứng dụng I2P** - Thiết lập trình khởi chạy và thêm vào dock
4. **Cấu hình băng thông I2P** - Chạy trình hướng dẫn thiết lập để tối ưu hóa kết nối của bạn

## Phần Một: Cài đặt Java

I2P yêu cầu Java để chạy. Nếu bạn đã cài đặt Java 8 hoặc phiên bản mới hơn, bạn có thể [chuyển đến Phần Hai](#part-two-download-and-install-i2p).

### Step 1: Download Java

Truy cập [trang tải xuống Oracle Java](https://www.oracle.com/java/technologies/downloads/) và tải về trình cài đặt macOS cho Java 8 hoặc phiên bản mới hơn.

![Tải xuống Oracle Java cho macOS](/images/guides/macos-install/0-jre.png)

### Step 2: Run the Installer

Tìm tệp `.dmg` đã tải xuống trong thư mục Downloads của bạn và nhấp đúp để mở nó.

![Mở trình cài đặt Java](/images/guides/macos-install/1-jre.png)

### Step 3: Allow Installation

macOS có thể hiển thị cảnh báo bảo mật vì trình cài đặt đến từ một nhà phát triển đã được xác định. Nhấp **Mở** để tiếp tục.

![Cấp quyền cho trình cài đặt để tiếp tục](/images/guides/macos-install/2-jre.png)

### Bước 1: Tải Java xuống

Nhấp vào **Install** để bắt đầu quá trình cài đặt Java.

![Bắt đầu cài đặt Java](/images/guides/macos-install/3-jre.png)

### Bước 2: Chạy Trình Cài Đặt

Trình cài đặt sẽ sao chép các tệp và cấu hình Java trên hệ thống của bạn. Quá trình này thường mất 1-2 phút.

![Đợi trình cài đặt hoàn tất](/images/guides/macos-install/4-jre.png)

### Bước 3: Cho phép Cài đặt

Khi bạn thấy thông báo thành công, Java đã được cài đặt! Nhấp vào **Đóng** để hoàn tất.

![Cài đặt Java hoàn tất](/images/guides/macos-install/5-jre.png)

## Part Two: Download and Install I2P

Bây giờ Java đã được cài đặt, bạn có thể cài đặt I2P router.

### Bước 4: Cài đặt Java

Truy cập [trang Tải xuống](/downloads/) và tải về trình cài đặt **I2P cho Unix/Linux/BSD/Solaris** (tệp `.jar`).

![Tải về trình cài đặt I2P](/images/guides/macos-install/0-i2p.png)

### Bước 5: Chờ quá trình cài đặt hoàn tất

Nhấp đúp vào tệp `i2pinstall_X.X.X.jar` đã tải xuống. Trình cài đặt sẽ khởi chạy và yêu cầu bạn chọn ngôn ngữ ưa thích.

![Chọn ngôn ngữ của bạn](/images/guides/macos-install/1-i2p.png)

### Bước 6: Hoàn Tất Cài Đặt

Đọc thông điệp chào mừng và nhấp vào **Next** để tiếp tục.

![Giới thiệu trình cài đặt](/images/guides/macos-install/2-i2p.png)

### Step 4: Important Notice

Trình cài đặt sẽ hiển thị một thông báo quan trọng về các bản cập nhật. Các bản cập nhật I2P được **ký và xác minh end-to-end**, mặc dù bản thân trình cài đặt này không được ký. Nhấp **Next**.

![Thông báo quan trọng về cập nhật](/images/guides/macos-install/3-i2p.png)

### Bước 1: Tải I2P

Đọc thỏa thuận cấp phép I2P (giấy phép kiểu BSD). Nhấp **Next** để chấp nhận.

![Thỏa thuận cấp phép](/images/guides/macos-install/4-i2p.png)

### Bước 2: Chạy Trình Cài Đặt

Chọn nơi cài đặt I2P. Vị trí mặc định (`/Applications/i2p`) được khuyến nghị. Nhấp **Next**.

![Chọn thư mục cài đặt](/images/guides/macos-install/5-i2p.png)

### Bước 3: Màn hình Chào mừng

Để tất cả các thành phần được chọn cho một cài đặt hoàn chỉnh. Nhấp vào **Tiếp theo**.

![Chọn các thành phần để cài đặt](/images/guides/macos-install/6-i2p.png)

### Bước 4: Thông Báo Quan Trọng

Xem lại các lựa chọn của bạn và nhấp vào **Next** để bắt đầu cài đặt I2P.

![Bắt đầu cài đặt](/images/guides/macos-install/7-i2p.png)

### Bước 5: Thỏa thuận cấp phép

Trình cài đặt sẽ sao chép các tệp I2P vào hệ thống của bạn. Quá trình này mất khoảng 1-2 phút.

![Đang cài đặt](/images/guides/macos-install/8-i2p.png)

### Bước 6: Chọn Thư Mục Cài Đặt

Trình cài đặt tạo các script khởi chạy để khởi động I2P.

![Tạo các script khởi động](/images/guides/macos-install/9-i2p.png)

### Bước 7: Chọn các thành phần

Trình cài đặt sẽ đề nghị tạo các lối tắt trên desktop và mục trong menu. Hãy chọn những tùy chọn của bạn và nhấn **Next**.

![Tạo lối tắt](/images/guides/macos-install/10-i2p.png)

### Bước 8: Bắt đầu Cài đặt

Thành công! I2P hiện đã được cài đặt. Nhấp vào **Done** để hoàn tất.

![Hoàn tất cài đặt](/images/guides/macos-install/11-i2p.png)

## Part Three: Configure I2P App

Bây giờ hãy giúp I2P dễ khởi chạy hơn bằng cách thêm nó vào thư mục Applications và Dock của bạn.

### Bước 9: Cài đặt các tệp

Mở Finder và điều hướng đến thư mục **Applications** của bạn.

![Mở thư mục Applications](/images/guides/macos-install/0-conf.png)

### Bước 10: Tạo Script Khởi Chạy

Tìm thư mục **I2P** hoặc ứng dụng **Start I2P Router** bên trong `/Applications/i2p/`.

![Tìm trình khởi chạy I2P](/images/guides/macos-install/1-conf.png)

### Bước 11: Các Phím Tắt Cài Đặt

Kéo ứng dụng **Start I2P Router** vào Dock của bạn để truy cập dễ dàng. Bạn cũng có thể tạo một alias trên màn hình desktop.

![Thêm I2P vào Dock của bạn](/images/guides/macos-install/2-conf.png)

**Mẹo**: Nhấp chuột phải vào biểu tượng I2P trong Dock và chọn **Options → Keep in Dock** để giữ nó vĩnh viễn.

## Part Four: Configure I2P Bandwidth

Khi bạn khởi chạy I2P lần đầu tiên, bạn sẽ thực hiện qua trình hướng dẫn thiết lập để cấu hình các cài đặt băng thông. Điều này giúp tối ưu hóa hiệu suất của I2P cho kết nối của bạn.

### Bước 12: Hoàn Tất Cài Đặt

Nhấp vào biểu tượng I2P trong Dock của bạn (hoặc nhấp đúp vào trình khởi chạy). Trình duyệt web mặc định của bạn sẽ mở trang I2P Router Console.

![Màn hình chào mừng I2P Router Console](/images/guides/macos-install/0-wiz.png)

### Step 2: Welcome Wizard

Trình hướng dẫn thiết lập sẽ chào đón bạn. Nhấp vào **Next** để bắt đầu cấu hình I2P.

![Giới thiệu trình hướng dẫn cài đặt](/images/guides/macos-install/1-wiz.png)

### Bước 1: Mở Thư mục Applications

Chọn **ngôn ngữ giao diện** ưa thích của bạn và chọn giữa chủ đề **sáng** hoặc **tối**. Nhấp **Tiếp theo**.

![Chọn ngôn ngữ và giao diện](/images/guides/macos-install/2-wiz.png)

### Bước 2: Tìm I2P Launcher

Trình hướng dẫn sẽ giải thích về kiểm tra băng thông. Kiểm tra này kết nối đến dịch vụ **M-Lab** để đo tốc độ internet của bạn. Nhấp **Next** để tiếp tục.

![Giải thích kiểm tra băng thông](/images/guides/macos-install/3-wiz.png)

### Bước 3: Thêm vào Dock

Nhấp **Run Test** để đo tốc độ tải lên và tải xuống của bạn. Bài kiểm tra mất khoảng 30-60 giây.

![Chạy kiểm tra băng thông](/images/guides/macos-install/4-wiz.png)

### Step 6: Test Results

Xem lại kết quả kiểm tra của bạn. I2P sẽ đề xuất cài đặt băng thông dựa trên tốc độ kết nối của bạn.

![Kết quả kiểm tra băng thông](/images/guides/macos-install/5-wiz.png)

### Bước 1: Khởi chạy I2P

Chọn lượng băng thông bạn muốn chia sẻ với mạng I2P:

- **Tự động** (Khuyến nghị): I2P quản lý băng thông dựa trên mức sử dụng của bạn
- **Giới hạn**: Đặt giới hạn tải lên/tải xuống cụ thể
- **Không giới hạn**: Chia sẻ nhiều nhất có thể (dành cho kết nối tốc độ cao)

Nhấp **Next** để lưu cài đặt của bạn.

![Cấu hình chia sẻ băng thông](/images/guides/macos-install/6-wiz.png)

### Bước 2: Trình hướng dẫn chào mừng

Router I2P của bạn hiện đã được cấu hình và đang chạy! Bảng điều khiển router sẽ hiển thị trạng thái kết nối và cho phép bạn duyệt các trang web I2P.

## Getting Started with I2P

Bây giờ I2P đã được cài đặt và cấu hình, bạn có thể:

1. **Duyệt các trang I2P**: Truy cập [trang chủ I2P](http://127.0.0.1:7657/home) để xem liên kết đến các dịch vụ I2P phổ biến
2. **Cấu hình trình duyệt**: Thiết lập [profile trình duyệt](/docs/guides/browser-config) để truy cập các trang `.i2p`
3. **Khám phá dịch vụ**: Tìm hiểu email I2P, diễn đàn, chia sẻ file và nhiều hơn nữa
4. **Giám sát router**: [Console](http://127.0.0.1:7657/console) hiển thị trạng thái mạng và thống kê của bạn

### Bước 3: Ngôn ngữ và Giao diện

- **Router Console**: [http://127.0.0.1:7657/](http://127.0.0.1:7657/)
- **Cấu hình**: [http://127.0.0.1:7657/config](http://127.0.0.1:7657/config)
- **Sổ địa chỉ**: [http://127.0.0.1:7657/susidns/addressbook](http://127.0.0.1:7657/susidns/addressbook)
- **Cài đặt băng thông**: [http://127.0.0.1:7657/config](http://127.0.0.1:7657/config)

## Re-running the Setup Wizard

Nếu bạn muốn thay đổi cài đặt băng thông hoặc cấu hình lại I2P sau này, bạn có thể chạy lại trình hướng dẫn chào mừng từ Router Console:

1. Truy cập [I2P Setup Wizard](http://127.0.0.1:7657/welcome)
2. Thực hiện lại các bước của wizard

## Troubleshooting

### Bước 4: Thông tin Kiểm tra Băng thông

- **Kiểm tra Java**: Đảm bảo Java đã được cài đặt bằng cách chạy lệnh `java -version` trong Terminal
- **Kiểm tra quyền truy cập**: Đảm bảo thư mục I2P có đúng quyền truy cập
- **Kiểm tra logs**: Xem tại `~/.i2p/wrapper.log` để tìm thông báo lỗi

### Bước 5: Chạy Kiểm Tra Băng Thông

- Đảm bảo I2P đang chạy (kiểm tra Router Console)
- Cấu hình proxy trong trình duyệt để sử dụng HTTP proxy `127.0.0.1:4444`
- Đợi 5-10 phút sau khi khởi động để I2P tích hợp vào mạng lưới

### Bước 6: Kết quả kiểm tra

- Chạy lại kiểm tra băng thông và điều chỉnh cài đặt của bạn
- Đảm bảo bạn đang chia sẻ một phần băng thông với mạng lưới
- Kiểm tra trạng thái kết nối trong Router Console

## Phần Hai: Tải xuống và Cài đặt I2P

Để gỡ bỏ I2P khỏi Mac của bạn:

1. Thoát khỏi I2P router nếu nó đang chạy
2. Xóa thư mục `/Applications/i2p`
3. Xóa thư mục `~/.i2p` (cấu hình và dữ liệu I2P của bạn)
4. Xóa biểu tượng I2P khỏi Dock của bạn

## Next Steps

- **Tham gia cộng đồng**: Truy cập [i2pforum.net](http://i2pforum.net) hoặc xem I2P trên Reddit
- **Tìm hiểu thêm**: Đọc [tài liệu I2P](/en/docs) để hiểu cách mạng lưới hoạt động
- **Tham gia đóng góp**: Cân nhắc [đóng góp cho I2P](/en/get-involved) trong phát triển hoặc vận hành hạ tầng

Chúc mừng! Bạn hiện đã là một phần của mạng lưới I2P. Chào mừng đến với internet vô hình!

