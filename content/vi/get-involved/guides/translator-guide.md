---
title: "Hướng Dẫn Dịch"
description: "Giúp I2P đến với người dùng trên toàn thế giới bằng cách dịch giao diện điều khiển router và website"
date: 2025-01-15
layout: "single"
type: "docs"
---

## Tổng Quan

Giúp I2P đến với người dùng trên khắp thế giới bằng cách dịch giao diện điều khiển router I2P và website sang ngôn ngữ của bạn. Dịch thuật là một quá trình liên tục, và mọi đóng góp dù nhỏ đều có giá trị.

## Nền Tảng Dịch Thuật

Chúng tôi sử dụng **Transifex** cho tất cả các bản dịch I2P. Đây là phương pháp dễ dàng và được khuyến nghị cho cả dịch giả mới và có kinh nghiệm.

### Bắt Đầu với Transifex

1. **Tạo tài khoản** tại [Transifex](https://www.transifex.com/)
2. **Tham gia dự án I2P**: [I2P trên Transifex](https://explore.transifex.com/otf/I2P/)
3. **Yêu cầu tham gia** vào nhóm ngôn ngữ của bạn (hoặc yêu cầu một ngôn ngữ mới nếu không có trong danh sách)
4. **Bắt đầu dịch** sau khi được chấp thuận

### Tại sao chọn Transifex?

- **Giao diện thân thiện với người dùng** - Không yêu cầu kiến thức kỹ thuật
- **Bộ nhớ dịch thuật** - Gợi ý bản dịch dựa trên công việc trước đây
- **Cộng tác** - Làm việc với các dịch giả khác bằng ngôn ngữ của bạn
- **Kiểm soát chất lượng** - Quá trình đánh giá đảm bảo độ chính xác
- **Cập nhật tự động** - Các thay đổi đồng bộ với nhóm phát triển

## Những Gì Cần Dịch

### Giao Diện Điều Khiển Router (Ưu Tiên)

Giao diện điều khiển router I2P là giao diện chính mà người dùng tương tác khi chạy I2P. Dịch phần này có ảnh hưởng tức thì nhất đến trải nghiệm người dùng.

**Các khu vực chính cần dịch:**

- **Giao diện chính** - Điều hướng, menu, nút, thông báo trạng thái
- **Trang cấu hình** - Mô tả và tùy chọn cài đặt
- **Tài liệu Hướng dẫn** - Tệp trợ giúp tích hợp và gợi ý 
- **Tin tức và cập nhật** - Nguồn tin tức ban đầu hiển thị cho người dùng
- **Thông báo lỗi** - Thông báo lỗi và cảnh báo cho người dùng
- **Cấu hình proxy** - Các trang cài đặt HTTP, SOCKS, và kênh

Tất cả các bản dịch giao diện điều khiển router được quản lý thông qua Transifex ở định dạng `.po` (gettext).

## Nguyên Tắc Dịch Thuật

### Phong Cách và Giọng Điệu

- **Rõ ràng và ngắn gọn** - I2P liên quan đến các khái niệm kỹ thuật; giữ bản dịch đơn giản
- **Thuật ngữ nhất quán** - Dùng cùng một thuật ngữ suốt bản dịch (kiểm tra bộ nhớ dịch thuật)
- **Phong cách lịch sự hoặc không** - Theo thông lệ cho ngôn ngữ của bạn
- **Bảo toàn định dạng** - Giữ các chỗ trống như `{0}`, `%s`, `<b>tags</b>` nguyên vẹn

### Cân Nhắc Kỹ Thuật

- **Mã hóa** - Luôn sử dụng mã hóa UTF-8
- **Chỗ trống** - Không dịch các chỗ trống biến đổi (`{0}`, `{1}`, `%s`, v.v.)
- **HTML/Markdown** - Bảo toàn các thẻ HTML và định dạng Markdown
- **Liên kết** - Giữ nguyên URL trừ khi có phiên bản địa phương hóa
- **Từ viết tắt** - Cân nhắc dịch hoặc giữ nguyên (vd. "KB/s", "HTTP")

### Thử Nghiệm Bản Dịch Của Bạn

Nếu bạn có quyền truy cập vào router I2P:

1. Tải xuống các tệp bản dịch mới nhất từ Transifex
2. Đặt chúng vào cài đặt I2P của bạn
3. Khởi động lại giao diện điều khiển router
4. Xem xét bản dịch trong ngữ cảnh
5. Báo cáo bất kỳ vấn đề hoặc cải tiến cần thiết

## Nhận Trợ Giúp

### Hỗ Trợ Cộng Đồng

- **Kênh IRC**: `#i2p-dev` trên I2P IRC hoặc OFTC
- **Diễn đàn**: Diễn đàn phát triển I2P
- **Bình luận trên Transifex**: Đặt câu hỏi trực tiếp trên chuỗi dịch

### Câu Hỏi Thường Gặp

**H: Tôi nên dịch bao lâu một lần?**
Dịch theo tốc độ của bạn. Ngay cả việc dịch một vài chuỗi cũng hữu ích. Dự án là liên tục.

**H: Điều gì sẽ xảy ra nếu ngôn ngữ của tôi không có trong danh sách?**
Yêu cầu ngôn ngữ mới trên Transifex. Nếu có nhu cầu, nhóm sẽ thêm vào.

**H: Tôi có thể dịch một mình hay phải cần đội làm việc?**
Bạn có thể bắt đầu một mình. Khi có thêm dịch giả tham gia ngôn ngữ của bạn, bạn có thể cộng tác.

**H: Làm thế nào để tôi biết những gì cần dịch?**
Transifex hiển thị phần trăm hoàn thành và nêu bật các chuỗi chưa được dịch.

**H: Nếu tôi không đồng ý với một bản dịch hiện có thì sao?**
Đề xuất cải tiến trên Transifex. Người đánh giá sẽ đánh giá các thay đổi.

## Nâng Cao: Dịch Thủ Công (Tùy Chọn)

Dành cho dịch giả có kinh nghiệm muốn truy cập trực tiếp vào tệp nguồn:

### Yêu Cầu

- **Git** - Hệ thống kiểm soát phiên bản
- **POEdit** hoặc trình chỉnh sửa văn bản - Để chỉnh sửa tệp `.po`
- **Kiến thức cơ bản về dòng lệnh**

### Quy Trình

1. **Sao chép kho lưu trữ**:
   ```bash
   git clone https://i2pgit.org/i2p-hackers/i2p.i2p.git
   ```

2. **Tìm tệp bản dịch**:
   - Giao diện điều khiển router: `apps/routerconsole/locale/`
   - Tìm `messages_xx.po` (trong đó `xx` là mã ngôn ngữ của bạn)

3. **Chỉnh sửa bản dịch**:
   - Sử dụng POEdit hoặc một trình chỉnh sửa văn bản
   - Lưu với mã hóa UTF-8

4. **Kiểm tra cục bộ** (nếu bạn đã cài đặt I2P)

5. **Gửi thay đổi**:
   - Tạo yêu cầu hợp nhất trên [I2P Git](https://i2pgit.org/)
   - Hoặc chia sẻ tệp `.po` của bạn với nhóm phát triển

**Lưu ý**: Hầu hết các dịch giả nên sử dụng Transifex. Dịch thủ công chỉ phù hợp với những người quen thuộc với Git và luồng công việc phát triển.

## Cảm Ơn Bạn

Mỗi bản dịch giúp I2P trở nên dễ tiếp cận hơn đối với người dùng trên toàn thế giới. Cho dù bạn dịch một vài chuỗi hay các phần toàn bộ, đóng góp của bạn thực sự tạo ra sự khác biệt trong việc giúp mọi người bảo vệ quyền riêng tư của họ trên mạng trực tuyến.

**Sẵn sàng bắt đầu?** [Tham gia I2P trên Transifex →](https://explore.transifex.com/otf/I2P/)
