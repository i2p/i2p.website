---
title: "I2P Mail (Email Ẩn danh trên I2P)"
description: "Tổng quan về các hệ thống email trong mạng I2P — lịch sử, các lựa chọn và trạng thái hiện tại"
slug: "i2p-mail"
lastUpdated: "2025-10"
---

## Giới thiệu

I2P cung cấp dịch vụ nhắn tin riêng tư theo kiểu email thông qua **dịch vụ Mail.i2p của Postman** kết hợp với **SusiMail**, một ứng dụng webmail tích hợp sẵn. Hệ thống này cho phép người dùng gửi và nhận email cả trong mạng I2P lẫn từ/đến internet thông thường (clearnet) thông qua một cổng cầu nối.

---

## Postman / Mail.i2p + SusiMail

### What it is

- **Mail.i2p** là nhà cung cấp email được lưu trữ bên trong I2P, do "Postman" vận hành
- **SusiMail** là ứng dụng webmail được tích hợp trong bảng điều khiển router I2P. Nó được thiết kế để tránh làm lộ metadata (ví dụ: hostname) đến các máy chủ SMTP bên ngoài.
- Thông qua cấu hình này, người dùng I2P có thể gửi/nhận tin nhắn cả bên trong I2P và đến/từ clearnet (ví dụ: Gmail) thông qua cầu nối Postman.

### How Addressing Works

I2P email sử dụng hệ thống địa chỉ kép:

- **Trong mạng I2P**: `username@mail.i2p` (ví dụ: `idk@mail.i2p`)
- **Từ clearnet**: `username@i2pmail.org` (ví dụ: `idk@i2pmail.org`)

Gateway `i2pmail.org` cho phép người dùng internet thông thường gửi email đến các địa chỉ I2P, và người dùng I2P gửi đến các địa chỉ clearnet. Email từ internet được định tuyến qua gateway trước khi được chuyển tiếp qua I2P đến hộp thư SusiMail của bạn.

**Hạn ngạch gửi Clearnet**: 20 email mỗi ngày khi gửi đến các địa chỉ internet thông thường.

### Nó là gì

**Để đăng ký tài khoản mail.i2p:**

1. Đảm bảo I2P router của bạn đang chạy
2. Truy cập **[http://hq.postman.i2p](http://hq.postman.i2p)** bên trong I2P
3. Làm theo quy trình đăng ký
4. Truy cập email của bạn thông qua **SusiMail** trong router console

> **Lưu ý**: `hq.postman.i2p` là địa chỉ mạng I2P (eepsite) và chỉ có thể truy cập khi đã kết nối với I2P. Để biết thêm thông tin về cài đặt email, bảo mật và cách sử dụng, hãy truy cập Postman HQ.

### Cách thức hoạt động của địa chỉ

- Tự động loại bỏ các header nhận dạng (`User-Agent:`, `X-Mailer:`) để bảo vệ quyền riêng tư
- Làm sạch metadata để ngăn chặn rò rỉ thông tin ra các máy chủ SMTP bên ngoài
- Mã hóa đầu-cuối (end-to-end encryption) cho email nội bộ I2P-to-I2P

### Bắt Đầu

- Khả năng tương tác với email "thông thường" (SMTP/POP) thông qua cầu nối Postman
- Trải nghiệm người dùng đơn giản (webmail tích hợp sẵn trong bảng điều khiển router)
- Tích hợp với bản phân phối I2P cốt lõi (SusiMail đi kèm với Java I2P)
- Loại bỏ header để bảo vệ quyền riêng tư

### Tính năng Bảo mật

- Cầu nối đến email bên ngoài yêu cầu tin tưởng vào cơ sở hạ tầng của Postman
- Cầu nối clearnet làm giảm tính riêng tư so với truyền thông I2P hoàn toàn nội bộ
- Phụ thuộc vào tính khả dụng và bảo mật của máy chủ thư Postman

## Technical Details

**Dịch vụ SMTP**: `localhost:7659` (được cung cấp bởi Postman) **Dịch vụ POP3**: `localhost:7660` **Truy cập Webmail**: Được tích hợp sẵn trong bảng điều khiển router tại `http://127.0.0.1:7657/susimail/`

> **Quan trọng**: SusiMail chỉ dùng để đọc và gửi email. Việc tạo và quản lý tài khoản phải được thực hiện tại **hq.postman.i2p**.

---

## Best Practices

- **Thay đổi mật khẩu** sau khi đăng ký tài khoản mail.i2p của bạn
- **Sử dụng email I2P-to-I2P** bất cứ khi nào có thể để đạt được quyền riêng tư tối đa (không cần cầu nối clearnet)
- **Lưu ý giới hạn 20 email/ngày** khi gửi đến địa chỉ clearnet
- **Hiểu rõ các đánh đổi**: Cầu nối clearnet mang lại sự tiện lợi nhưng giảm tính ẩn danh so với giao tiếp hoàn toàn nội bộ I2P
- **Giữ I2P được cập nhật** để hưởng lợi từ các cải tiến bảo mật trong SusiMail

Tôi sẵn sàng dịch, nhưng tôi không thấy văn bản nào cần dịch trong tin nhắn của bạn. Phần "Text to translate:" không có nội dung theo sau dấu "---".

Vui lòng cung cấp văn bản cần dịch và tôi sẽ thực hiện ngay lập tức mà không có bình luận hay giải thích thêm.
