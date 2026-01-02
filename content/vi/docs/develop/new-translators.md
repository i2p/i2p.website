---
title: "Hướng Dẫn Cho Người Dịch Mới"
description: "Cách đóng góp bản dịch cho trang web I2P và bảng điều khiển router bằng Transifex hoặc phương pháp thủ công"
slug: "new-translators"
lastUpdated: "2025-10"
type: docs
---

Bạn muốn giúp I2P tiếp cận được nhiều người hơn trên toàn thế giới? Dịch thuật là một trong những đóng góp có giá trị nhất bạn có thể làm cho dự án. Hướng dẫn này sẽ giúp bạn dịch router console.

## Phương pháp Dịch thuật

Có hai cách để đóng góp bản dịch:

### Phương pháp 1: Transifex (Khuyến nghị)

**Đây là cách dễ nhất để dịch I2P.** Transifex cung cấp giao diện web giúp việc dịch thuật trở nên đơn giản và dễ tiếp cận.

1. Đăng ký tại [Transifex](https://www.transifex.com/otf/I2P/)
2. Yêu cầu tham gia nhóm dịch thuật I2P
3. Bắt đầu dịch trực tiếp trên trình duyệt của bạn

Không cần kiến thức chuyên môn - chỉ cần đăng ký và bắt đầu dịch!

### Phương pháp 2: Dịch thủ công

Dành cho các biên dịch viên muốn làm việc với git và các tệp cục bộ, hoặc cho các ngôn ngữ chưa được thiết lập trên Transifex.

**Yêu cầu:** - Quen thuộc với hệ thống quản lý phiên bản git - Trình soạn thảo văn bản hoặc công cụ dịch thuật (khuyến nghị POEdit) - Công cụ dòng lệnh: git, gettext

**Thiết lập:** 1. Tham gia [#i2p-dev trên IRC](/contact/#irc) và giới thiệu bản thân 2. Cập nhật trạng thái dịch thuật trên wiki (hỏi trên IRC để được cấp quyền truy cập) 3. Clone repository phù hợp (xem các phần bên dưới)

---

## Bản dịch Bảng điều khiển Router

Router console là giao diện web mà bạn thấy khi chạy I2P. Việc dịch thuật nó giúp ích cho những người dùng không thoải mái với tiếng Anh.

### Sử dụng Transifex (Khuyên dùng)

1. Truy cập [I2P trên Transifex](https://www.transifex.com/otf/I2P/)
2. Chọn dự án router console
3. Chọn ngôn ngữ của bạn
4. Bắt đầu dịch

### Dịch Bảng Điều Khiển Router Thủ Công

**Yêu cầu:** - Giống như dịch website (git, gettext) - Khóa GPG (để có quyền commit) - Thỏa thuận nhà phát triển đã ký

**Sao chép kho lưu trữ I2P chính:**

```bash
git clone https://i2pgit.org/I2P_Developers/i2p.i2p.git
cd i2p.i2p
```
**Các tệp cần dịch:**

Bảng điều khiển router có khoảng 15 tệp cần dịch:

1. **Tệp giao diện cốt lõi:**
   - `apps/routerconsole/locale/messages_*.po` - Thông điệp console chính
   - `apps/routerconsole/locale-news/messages_*.po` - Thông điệp tin tức

2. **Các tệp Proxy:**
   - `apps/i2ptunnel/locale/messages_*.po` - Giao diện cấu hình tunnel

3. **Ngôn ngữ ứng dụng:**
   - `apps/susidns/locale/messages_*.po` - Giao diện sổ địa chỉ
   - `apps/susimail/locale/messages_*.po` - Giao diện email
   - Các thư mục ngôn ngữ riêng cho từng ứng dụng khác

4. **Tệp tài liệu:**
   - `installer/resources/readme/readme_*.html` - Tài liệu hướng dẫn cài đặt
   - Các tệp trợ giúp trong nhiều ứng dụng khác nhau

**Quy trình dịch thuật:**

```bash
# Update .po files from source
ant extractMessages

# Edit .po files with POEdit or text editor
poedit apps/routerconsole/locale/messages_es.po

# Build and test
ant updaters
# Install the update and check translations in the console
```
**Gửi công việc của bạn:** - Tạo merge request trên [GitLab](https://i2pgit.org/I2P_Developers/i2p.i2p) - Hoặc chia sẻ tệp với nhóm phát triển trên IRC

---

## Công cụ Dịch thuật

### POEdit (Rất Khuyến Nghị)

[POEdit](https://poedit.net/) là một trình soạn thảo chuyên dụng cho các tệp dịch thuật .po.

**Tính năng:** - Giao diện trực quan cho công việc dịch thuật - Hiển thị ngữ cảnh bản dịch - Xác thực tự động - Có sẵn cho Windows, macOS và Linux

### Trình soạn thảo văn bản

Bạn cũng có thể sử dụng bất kỳ trình soạn thảo văn bản nào: - VS Code (với tiện ích mở rộng i18n) - Sublime Text - vim/emacs (dành cho người dùng terminal)

### Kiểm tra Chất lượng

Trước khi gửi: 1. **Kiểm tra định dạng:** Đảm bảo các placeholder như `%s` và `{0}` không bị thay đổi 2. **Kiểm tra bản dịch:** Cài đặt và chạy I2P để xem chúng hiển thị như thế nào 3. **Tính nhất quán:** Giữ thuật ngữ nhất quán trong các tệp 4. **Độ dài:** Một số chuỗi có giới hạn không gian trong giao diện

---

## Mẹo dành cho Người dịch

### Hướng dẫn chung

- **Giữ nhất quán:** Sử dụng cùng một bản dịch cho các thuật ngữ phổ biến xuyên suốt
- **Giữ nguyên định dạng:** Bảo toàn thẻ HTML, placeholder (`%s`, `{0}`), và ngắt dòng
- **Ngữ cảnh quan trọng:** Đọc kỹ văn bản tiếng Anh gốc để hiểu ngữ cảnh
- **Đặt câu hỏi:** Sử dụng IRC hoặc diễn đàn nếu có điều gì không rõ ràng

### Các Thuật Ngữ I2P Phổ Biến

Một số thuật ngữ nên giữ nguyên tiếng Anh hoặc phiên âm cẩn thận:

- **I2P** - Keep as is
- **eepsite** - Trang web I2P (website trên mạng I2P)
- **tunnel** - Đường dẫn kết nối
- **netDb** - Cơ sở dữ liệu mạng
- **floodfill** - Loại router
- **destination** - Điểm đích địa chỉ I2P

### Kiểm tra bản dịch của bạn

1. Biên dịch I2P với bản dịch của bạn
2. Thay đổi ngôn ngữ trong cài đặt router console
3. Điều hướng qua tất cả các trang để kiểm tra:
   - Văn bản vừa khít với các phần tử giao diện
   - Không có ký tự lỗi (vấn đề mã hóa)
   - Bản dịch có ý nghĩa phù hợp với ngữ cảnh

---

## Câu Hỏi Thường Gặp

### Tại sao quy trình dịch thuật lại phức tạp như vậy?

Quy trình sử dụng kiểm soát phiên bản (git) và các công cụ dịch thuật chuẩn (tệp .po) bởi vì:

1. **Trách nhiệm:** Theo dõi ai đã thay đổi gì và khi nào
2. **Chất lượng:** Xem xét các thay đổi trước khi chúng được công bố
3. **Nhất quán:** Duy trì định dạng và cấu trúc tệp tin phù hợp
4. **Khả năng mở rộng:** Quản lý bản dịch trên nhiều ngôn ngữ một cách hiệu quả
5. **Cộng tác:** Nhiều người dịch có thể làm việc cùng một ngôn ngữ

### Tôi có cần kỹ năng lập trình không?

**Không!** Nếu bạn sử dụng Transifex, bạn chỉ cần: - Thông thạo cả tiếng Anh và ngôn ngữ đích của bạn - Một trình duyệt web - Kỹ năng máy tính cơ bản

Đối với dịch thuật thủ công, bạn sẽ cần kiến thức cơ bản về dòng lệnh, nhưng không yêu cầu lập trình.

### Mất bao lâu?

- **Router console:** Khoảng 15-20 giờ cho tất cả các tệp
- **Bảo trì:** Vài giờ mỗi tháng để cập nhật các chuỗi mới

### Nhiều người có thể cùng làm việc trên một ngôn ngữ không?

Có! Phối hợp là chìa khóa: - Sử dụng Transifex để phối hợp tự động - Đối với công việc thủ công, giao tiếp trong kênh IRC #i2p-dev - Phân chia công việc theo từng phần hoặc tệp tin

### Điều gì xảy ra nếu ngôn ngữ của tôi không được liệt kê?

Yêu cầu trên Transifex hoặc liên hệ với nhóm trên IRC. Nhóm phát triển có thể thiết lập ngôn ngữ mới một cách nhanh chóng.

### Làm thế nào để kiểm tra bản dịch của tôi trước khi gửi?

- Biên dịch I2P từ mã nguồn với bản dịch của bạn
- Cài đặt và chạy cục bộ
- Thay đổi ngôn ngữ trong cài đặt console

---

## Nhận Trợ Giúp

### Hỗ trợ IRC

Tham gia [#i2p-dev trên IRC](/contact/#irc) để: - Nhận trợ giúp kỹ thuật về công cụ dịch thuật - Đặt câu hỏi về thuật ngữ I2P - Phối hợp với các dịch giả khác - Nhận hỗ trợ trực tiếp từ các nhà phát triển

### Diễn đàn

- Thảo luận về dịch thuật trên [I2P Forums](http://i2pforum.net/)
- Inside I2P: Diễn đàn dịch thuật trên zzz.i2p (yêu cầu I2P router)

### Tài liệu

- [Tài liệu Transifex](https://docs.transifex.com/)
- [Tài liệu POEdit](https://poedit.net/support)
- [Hướng dẫn gettext](https://www.gnu.org/software/gettext/manual/)

---

## Ghi nhận

Tất cả các biên dịch viên được ghi nhận trong: - Bảng điều khiển I2P router (trang Giới thiệu) - Trang ghi nhận đóng góp của website - Lịch sử commit trên Git - Thông báo phát hành

Công việc của bạn trực tiếp giúp mọi người trên khắp thế giới sử dụng I2P một cách an toàn và riêng tư. Cảm ơn bạn đã đóng góp!

---

## Các Bước Tiếp Theo

Sẵn sàng bắt đầu dịch?

1. **Chọn phương pháp của bạn:**
   - Bắt đầu nhanh: [Đăng ký trên Transifex](https://www.transifex.com/otf/I2P/)
   - Phương pháp thủ công: Tham gia [#i2p-dev trên IRC](/contact/#irc)

2. **Bắt đầu từ nhỏ:** Dịch một vài chuỗi để làm quen với quy trình

3. **Yêu cầu trợ giúp:** Đừng ngần ngại liên hệ qua IRC hoặc diễn đàn

**Cảm ơn bạn đã giúp đỡ làm cho I2P dễ tiếp cận với tất cả mọi người!**
