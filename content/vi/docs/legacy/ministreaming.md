---
title: "Thư viện Ministreaming"
description: "Ghi chú lịch sử về lớp vận chuyển tương tự TCP đầu tiên của I2P"
slug: "ministreaming"
lastUpdated: "2025-02"
accurateFor: "historical"
---

> **Không dùng nữa:** Thư viện ministreaming ra đời trước [thư viện streaming](/docs/specs/streaming/) hiện nay. Các ứng dụng hiện đại phải sử dụng API streaming đầy đủ hoặc SAM v3. Thông tin bên dưới được giữ lại cho các nhà phát triển đang xem xét mã nguồn cũ được phân phối trong `ministreaming.jar`.

## Tổng quan

Ministreaming (lớp truyền tải dạng luồng tối giản) hoạt động ở phía trên [I2CP](/docs/specs/i2cp/) để cung cấp việc truyền tải tin cậy, theo đúng thứ tự trên lớp thông điệp của I2P—tương tự như TCP qua IP. Ban đầu nó được tách ra từ ứng dụng **I2PTunnel** thời kỳ đầu (theo giấy phép BSD) để các giao thức truyền tải thay thế có thể phát triển độc lập.

Các ràng buộc thiết kế chính:

- Thiết lập kết nối hai pha kiểu cổ điển (SYN/ACK/FIN) mượn từ TCP
- Kích thước cửa sổ cố định là **1** gói
- Không có ID cho từng gói hoặc xác nhận chọn lọc

Những lựa chọn này giữ cho phần triển khai nhỏ gọn nhưng hạn chế thông lượng—mỗi gói thường phải chờ gần như hai RTT (thời gian khứ hồi) trước khi gói tiếp theo được gửi đi. Với các luồng kéo dài, mức độ trễ này có thể chấp nhận được, nhưng các trao đổi ngắn theo kiểu HTTP bị ảnh hưởng rõ rệt.

## Mối quan hệ với Streaming Library (thư viện truyền luồng)

Thư viện streaming hiện tại mở rộng cùng một gói Java (`net.i2p.client.streaming`). Các lớp và phương thức đã bị đánh dấu là lỗi thời vẫn được giữ trong Javadocs, được chú thích rõ ràng để các nhà phát triển có thể nhận diện các API thời kỳ ministreaming (tên của thư viện streaming thu gọn trước đây). Khi thư viện streaming thay thế ministreaming, nó đã bổ sung:

- Quy trình thiết lập kết nối thông minh hơn với ít vòng khứ hồi hơn
- Cửa sổ tắc nghẽn thích ứng và logic tái truyền
- Hiệu năng tốt hơn trên các tunnels dễ mất gói

## Ministreaming đã hữu ích khi nào?

Bất chấp những giới hạn của nó, ministreaming (cơ chế streaming tối giản) đã mang lại truyền tải đáng tin cậy trong những triển khai sớm nhất. API được cố ý giữ nhỏ gọn và sẵn sàng cho tương lai để các bộ máy streaming thay thế có thể được hoán đổi vào mà không phá vỡ mã gọi. Các ứng dụng Java liên kết trực tiếp với nó; các trình khách không dùng Java truy cập cùng chức năng thông qua hỗ trợ [SAM](/docs/legacy/sam/) cho các phiên streaming.

Hiện nay, hãy coi `ministreaming.jar` chỉ như một lớp tương thích. Phát triển mới nên:

1. Nhắm tới thư viện streaming đầy đủ (Java) hoặc SAM v3 (kiểu `STREAM`)  
2. Loại bỏ mọi giả định còn sót lại về fixed-window (cửa sổ cố định) khi hiện đại hóa mã  
3. Ưu tiên kích thước cửa sổ lớn hơn và bắt tay kết nối được tối ưu để cải thiện các khối lượng công việc nhạy cảm với độ trễ

## Tài liệu tham khảo

- [Tài liệu Thư viện Streaming](/docs/specs/streaming/)
- [Javadoc của Streaming](http://idk.i2p/javadoc-i2p/net/i2p/client/streaming/package-summary.html) – bao gồm các lớp ministreaming không còn được khuyến nghị sử dụng
- [Đặc tả SAM v3](/docs/api/samv3/) – hỗ trợ streaming cho các ứng dụng không phải Java

Nếu bạn gặp mã vẫn còn phụ thuộc vào ministreaming (cơ chế streaming tối giản cũ), hãy lên kế hoạch chuyển nó sang API streaming hiện đại—mạng lưới và các công cụ của nó mong đợi hành vi mới hơn.
