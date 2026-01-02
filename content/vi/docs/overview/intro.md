---
title: "Giới thiệu về I2P"
description: "Giới thiệu dễ hiểu hơn về mạng ẩn danh I2P"
slug: "intro"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
reviewStatus: "needs-review"
---

## I2P là gì?

The Invisible Internet Project (I2P) là một lớp mạng ẩn danh cho phép giao tiếp ngang hàng chống kiểm duyệt. Các kết nối ẩn danh được thực hiện bằng cách mã hóa lưu lượng của người dùng và gửi qua một mạng lưới phân tán được vận hành bởi các tình nguyện viên trên toàn thế giới.

## Tính Năng Chính

### Anonymity

I2P ẩn danh cả người gửi và người nhận tin nhắn. Không giống như các kết nối internet truyền thống nơi địa chỉ IP của bạn hiển thị với các trang web và dịch vụ, I2P sử dụng nhiều lớp mã hóa và định tuyến để giữ danh tính của bạn được riêng tư.

### Decentralization

Không có cơ quan trung tâm nào trong I2P. Mạng lưới được duy trì bởi các tình nguyện viên đóng góp băng thông và tài nguyên máy tính. Điều này giúp mạng lưới kháng kiểm duyệt và không có điểm lỗi đơn lẻ.

### Tính ẩn danh

Tất cả lưu lượng trong I2P được mã hóa đầu cuối đến đầu cuối. Thông điệp được mã hóa nhiều lần khi chúng đi qua mạng, tương tự như cách Tor hoạt động nhưng có những khác biệt quan trọng trong cách triển khai.

## How It Works

### Phi tập trung

I2P sử dụng "tunnel" để định tuyến lưu lượng. Khi bạn gửi hoặc nhận dữ liệu:

1. Router của bạn tạo một outbound tunnel (để gửi)
2. Router của bạn tạo một inbound tunnel (để nhận)
3. Các thông điệp được mã hóa và gửi qua nhiều router
4. Mỗi router chỉ biết điểm trước và điểm tiếp theo, không biết toàn bộ đường đi

### Mã hóa đầu cuối (End-to-End Encryption)

I2P cải tiến định tuyến onion truyền thống bằng "garlic routing":

- Nhiều thông điệp có thể được gộp lại với nhau (giống như các tép trong củ tỏi)
- Điều này mang lại hiệu suất tốt hơn và tính ẩn danh bổ sung
- Làm cho việc phân tích lưu lượng trở nên khó khăn hơn

### Network Database

I2P duy trì một cơ sở dữ liệu mạng phân tán chứa:

- Thông tin router
- Địa chỉ đích (tương tự như các trang web .i2p)
- Dữ liệu định tuyến được mã hóa

## Common Use Cases

### Tunnel

Lưu trữ hoặc truy cập các trang web có đuôi `.i2p` - những trang này chỉ có thể truy cập được trong mạng I2P và cung cấp đảm bảo ẩn danh mạnh mẽ cho cả người lưu trữ lẫn người truy cập.

### Garlic Routing

Chia sẻ tệp tin ẩn danh bằng BitTorrent qua I2P. Nhiều ứng dụng torrent đã tích hợp sẵn hỗ trợ I2P.

### Cơ sở dữ liệu mạng

Gửi và nhận email ẩn danh bằng I2P-Bote hoặc các ứng dụng email khác được thiết kế cho I2P.

### Messaging

Sử dụng IRC, nhắn tin tức thời, hoặc các công cụ giao tiếp khác một cách riêng tư qua mạng I2P.

## Getting Started

Sẵn sàng dùng thử I2P? Ghé thăm [trang tải xuống](/downloads) của chúng tôi để cài đặt I2P trên hệ thống của bạn.

Để biết thêm chi tiết kỹ thuật, xem [Technical Introduction](/docs/overview/tech-intro) hoặc khám phá toàn bộ [tài liệu](/docs).

## Cách Thức Hoạt Động

- [Giới thiệu Kỹ thuật](/docs/overview/tech-intro) - Các khái niệm kỹ thuật chuyên sâu hơn
- [Mô hình Mối đe dọa](/docs/overview/threat-model) - Hiểu về mô hình bảo mật của I2P
- [So sánh với Tor](/docs/overview/comparison) - I2P khác biệt với Tor như thế nào
- [Mật mã học](/docs/specs/cryptography) - Chi tiết về các thuật toán mật mã của I2P
