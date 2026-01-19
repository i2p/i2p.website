---
title: "Quy Trình Phản Ứng Lỗ Hổng Bảo Mật"
description: "Quy trình báo cáo và phản ứng lỗ hổng bảo mật của I2P"
layout: "security-response"
---

<div id="contact"></div>

## Báo Cáo Lỗ Hổng

Phát hiện một vấn đề bảo mật? Báo cáo nó tới **security@i2p.net** (khuyến khích sử dụng PGP)

<a href="/keys/i2p-security-public.asc" download class="pgp-key-btn">Tải xuống Khóa PGP</a> | Dấu vân tay khóa GPG: `EA27 06D6 14F5 28DB 764B F47E CFCD C461 75E6 694A`

<div id="guidelines"></div>

## Hướng Dẫn Nghiên Cứu

**VUI LÒNG KHÔNG:**
- Khai thác mạng I2P trực tiếp
- Thực hiện tấn công kỹ thuật xã hội hoặc hạ tầng I2P
- Gây gián đoạn dịch vụ cho người dùng khác

**VUI LÒNG:**
- Sử dụng các mạng thử nghiệm cô lập khi có thể
- Tuân theo phương thức tiết lộ phối hợp
- Liên hệ với chúng tôi trước khi thử nghiệm mạng thực tế

<div id="process"></div>

## Quy Trình Phản Ứng

### 1. Báo Cáo Nhận Được
- Phản hồi trong vòng **3 ngày làm việc**
- Quản lý Phản ứng được chỉ định
- Phân loại mức độ nghiêm trọng (CAO/TRUNG BÌNH/THẤP)

### 2. Điều Tra & Phát Triển
- Phát triển bản vá riêng qua các kênh mã hóa
- Kiểm tra trên mạng cô lập
- **Nghiêm trọng CAO:** Thông báo công khai trong vòng 3 ngày (không có chi tiết khai thác)

### 3. Phát Hành & Tiết Lộ
- Cập nhật bảo mật được triển khai
- Thời gian tối đa **90 ngày** để tiết lộ đầy đủ
- Tùy chọn ghi công nhà nghiên cứu trong thông báo

### Mức Độ Nghiêm Trọng

**CAO** - Ảnh hưởng toàn mạng, yêu cầu chú ý ngay lập tức
**TRUNG BÌNH** - Các router cá nhân, khai thác mục tiêu
**THẤP** - Ảnh hưởng hạn chế, kịch bản lý thuyết

<div id="communication"></div>

## Giao Tiếp An Toàn

Sử dụng mã hóa PGP/GPG cho tất cả các báo cáo bảo mật:

```
Dấu vân tay: EA27 06D6 14F5 28DB 764B F47E CFCD C461 75E6 694A
```

Bao gồm trong báo cáo của bạn:
- Mô tả kỹ thuật chi tiết
- Các bước để tái tạo
- Mã chứng minh khái niệm (nếu có)

<div id="timeline"></div>

## Mốc Thời Gian

| Giai đoạn | Khung thời gian |
|-----------|-----------------|
| Phản hồi ban đầu | 0-3 ngày |
| Điều tra | 1-2 tuần |
| Phát triển & Kiểm tra | 2-6 tuần |
| Phát hành | 6-12 tuần |
| Tiết lộ đầy đủ | Tối đa 90 ngày |

<div id="faq"></div>

## Câu Hỏi Thường Gặp

**Tôi sẽ gặp rắc rối khi báo cáo chứ?**
Không. Tiết lộ có trách nhiệm được đánh giá cao và bảo vệ.

**Tôi có thể thử nghiệm trên mạng thực tế không?**
Không. Chỉ sử dụng các mạng thử nghiệm cô lập.

**Tôi có thể giữ ẩn danh không?**
Có, mặc dù điều đó có thể làm phức tạp việc giao tiếp.

**Bạn có thưởng lỗi không?**
Hiện nay thì không. I2P được điều hành bởi tình nguyện viên với các nguồn lực hạn chế.

<div id="examples"></div>

## Những Gì Cần Báo Cáo

**Trong Phạm Vi:**
- Lỗ hổng của router I2P
- Khiếm khuyết trong giao thức hoặc mã hóa
- Tấn công cấp mạng
- Kỹ thuật phá vỡ ẩn danh
- Vấn đề từ chối dịch vụ

**Ngoài Phạm Vi:**
- Ứng dụng bên thứ ba (liên hệ với nhà phát triển)
- Tấn công kỹ thuật xã hội hoặc vật lý
- Lỗ hổng đã biết/đã công bố
- Vấn đề chỉ có lý thuyết

---

**Cảm ơn bạn đã giúp giữ an toàn cho I2P!**