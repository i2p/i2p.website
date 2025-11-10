---
title: "Nghiên Cứu Học Thuật"
description: "Thông tin và hướng dẫn cho nghiên cứu học thuật trên mạng I2P"
layout: "research"
aliases:
  - /en/research
  - /en/research/index
  - /en/research/questions
---

<div id="intro"></div>

## Nghiên Cứu Học Thuật I2P

Có một cộng đồng nghiên cứu lớn đang điều tra nhiều khía cạnh của sự ẩn danh. Để các mạng ẩn danh tiếp tục cải thiện, chúng tôi tin rằng điều cốt yếu là phải hiểu rõ các vấn đề đang phải đối mặt. Nghiên cứu về mạng I2P vẫn đang ở giai đoạn ban đầu, với phần lớn công việc nghiên cứu cho đến nay tập trung vào các mạng ẩn danh khác. Điều này mang lại cơ hội độc đáo để đóng góp nghiên cứu gốc.

<div id="notes"></div>

## Ghi Chú Cho Các Nhà Nghiên Cứu

### Ưu Tiên Nghiên Cứu Phòng Thủ

Chúng tôi chào đón các nghiên cứu giúp củng cố mạng và cải thiện tính bảo mật của nó. Kiểm thử giúp tăng cường cơ sở hạ tầng I2P được khuyến khích và đánh giá cao.

### Hướng Dẫn Truyền Thông Nghiên Cứu

Chúng tôi khuyến khích mạnh mẽ các nhà nghiên cứu liên lạc ý tưởng nghiên cứu của họ sớm với nhóm phát triển. Điều này giúp:

- Tránh trùng lặp tiềm năng với các dự án hiện có
- Giảm thiểu khả năng gây hại cho mạng
- Phối hợp nỗ lực kiểm thử và thu thập dữ liệu
- Đảm bảo nghiên cứu phù hợp với mục tiêu của mạng

<div id="ethics"></div>

## Đạo Đức Nghiên Cứu & Hướng Dẫn Kiểm Thử

### Nguyên Tắc Chung

Khi tiến hành nghiên cứu trên I2P, vui lòng xem xét những điều sau:

1. **Đánh giá lợi ích so với rủi ro của nghiên cứu** - Xem xét liệu lợi ích tiềm năng của nghiên cứu của bạn có vượt trội hơn bất kỳ rủi ro nào đối với mạng hoặc người dùng của nó
2. **Ưu tiên mạng kiểm thử hơn mạng trực tiếp** - Sử dụng cấu hình mạng kiểm thử của I2P bất cứ khi nào có thể
3. **Thu thập dữ liệu cần thiết tối thiểu** - Chỉ thu thập số lượng dữ liệu tối thiểu cần thiết cho nghiên cứu của bạn
4. **Đảm bảo dữ liệu công bố tôn trọng quyền riêng tư của người dùng** - Bất kỳ dữ liệu nào được công bố nên được ẩn danh và tôn trọng quyền riêng tư của người dùng

### Phương Pháp Kiểm Thử Mạng

Đối với các nhà nghiên cứu cần kiểm thử trên I2P:

- **Sử dụng cấu hình mạng kiểm thử** - I2P có thể được cấu hình để chạy trên một mạng kiểm thử độc lập
- **Sử dụng chế độ MultiRouter** - Chạy nhiều phiên bản router trên một máy duy nhất để kiểm thử
- **Cấu hình gia đình router** - Làm cho các router nghiên cứu của bạn có thể nhận dạng được bằng cách cấu hình chúng như một gia đình router

### Thực Hành Được Khuyến Khích

- **Liên lạc với nhóm I2P trước khi kiểm thử trên mạng trực tiếp** - Liên hệ với chúng tôi tại research@i2p.net trước khi tiến hành bất kỳ kiểm thử nào trên mạng trực tiếp
- **Sử dụng cấu hình gia đình router** - Điều này làm cho các router nghiên cứu của bạn trở nên minh bạch với mạng
- **Ngăn chặn sự can thiệp tiềm tàng vào mạng** - Thiết kế các kiểm thử của bạn để giảm thiểu bất kỳ ảnh hưởng tiêu cực nào đến người dùng thường xuyên

<div id="questions"></div>

## Các Câu Hỏi Nghiên Cứu Mở

Cộng đồng I2P đã xác định một số lĩnh vực mà nghiên cứu sẽ có giá trị đặc biệt:

### Cơ Sở Dữ Liệu Mạng

**Floodfills:**
- Có những cách nào khác để giảm thiểu tấn công brute-force trên mạng thông qua việc kiểm soát floodfill đáng kể không?
- Có cách nào để phát hiện, đánh dấu và loại bỏ 'floodfills xấu' mà không cần phải dựa vào một dạng quyền lực trung tâm nào không?

### Kênh Vận Chuyển

- Làm thế nào để cải thiện chiến lược truyền lại gói và thời gian chờ?
- Có cách nào để I2P làm xáo trộn các gói và giảm phân tích lưu lượng hiệu quả hơn không?

### Đường Hầm và Đích

**Chọn Lọc Đồng Ngang (Peer Selection):**
- Có cách nào mà I2P có thể thực hiện chọn lọc đồng ngang hiệu quả hoặc an toàn hơn không?
- Sử dụng geoip để ưu tiên các đồng ngang gần có ảnh hưởng tiêu cực đến tính ẩn danh không?

**Đường Hầm Đơn Hướng:**
- Lợi ích của đường hầm đơn hướng so với đường hầm hai chiều là gì?
- Những đánh đổi giữa đường hầm đơn hướng và hai chiều là gì?

**Kết Nối Đa Quốc Gia (Multihoming):**
- Kết nối đa quốc gia có hiệu quả trong việc cân bằng tải không?
- Nó mở rộng quy mô như thế nào?
- Điều gì xảy ra khi nhiều router lưu trữ cùng một Đích?
- Những đánh đổi về tính ẩn danh là gì?

### Định Tuyến Thông Điệp

- Hiệu quả của các cuộc tấn công theo thời gian giảm đi bao nhiêu khi phân mảnh và trộn các thông điệp?
- Những chiến lược trộn nào có thể mang lại lợi ích cho I2P?
- Làm thế nào các kỹ thuật độ trễ cao có thể được áp dụng hiệu quả trong hoặc cùng với mạng độ trễ thấp của chúng tôi?

### Tính Ẩn Danh

- Việc lấy dấu vân tay trình duyệt ảnh hưởng nhiều đến tính ẩn danh của người dùng I2P không?
- Phát triển một gói trình duyệt có lợi cho người dùng thông thường không?

### Liên Quan Đến Mạng

- Tác động tổng thể đến mạng do 'người dùng tham lam' tạo ra là gì?
- Những bước bổ sung để khuyến khích sự tham gia băng thông có giá trị không?

<div id="contact"></div>

## Liên Hệ

Đối với các thắc mắc nghiên cứu, cơ hội hợp tác, hoặc để thảo luận về kế hoạch nghiên cứu của bạn, vui lòng liên hệ với chúng tôi tại:

**Email:** research@i2p.net

Chúng tôi mong muốn được làm việc cùng cộng đồng nghiên cứu để cải thiện mạng I2P!