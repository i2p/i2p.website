---
title: "Thư viện Ministreaming"
description: "Ghi chú lịch sử về lớp vận chuyển giống TCP đầu tiên của I2P"
slug: "ministreaming"
aliases:
  - "/vi/ministreaming"
  - "/vi/ministreaming/"
lastUpdated: "2025-02"
accurateFor: "historical"
---

## Lưu ý

Thư viện ministreaming đã được nâng cao và mở rộng bởi [streaming library](/docs/api/streaming) "đầy đủ". Ministreaming đã bị phản đối và không tương thích với các ứng dụng ngày nay. Tài liệu sau đây đã cũ. Cũng lưu ý rằng streaming mở rộng ministreaming trong cùng một Java package (net.i2p.client.streaming), vì vậy tài liệu API hiện tại chứa cả hai. Các lớp và phương thức ministreaming lỗi thời được đánh dấu rõ ràng là deprecated trong Javadocs.

## Thư viện Ministreaming

Thư viện ministreaming là một lớp nằm trên cốt lõi [I2CP](/docs/protocol/i2cp) cho phép các luồng tin nhắn đáng tin cậy, theo thứ tự và được xác thực hoạt động trên một lớp tin nhắn không đáng tin cậy, không có thứ tự và không được xác thực. Giống như mối quan hệ TCP với IP, chức năng streaming này có một loạt các đánh đổi và tối ưu hóa khả dụng, nhưng thay vì nhúng chức năng đó vào mã I2P cơ sở, nó đã được tách thành thư viện riêng để vừa giữ cho các phức tạp giống TCP tách biệt vừa cho phép các triển khai tối ưu hóa thay thế.

Thư viện ministreaming được viết bởi mihi như một phần của ứng dụng [I2PTunnel](/docs/api/i2ptunnel) của ông ấy và sau đó được tách ra và phát hành dưới giấy phép BSD. Nó được gọi là thư viện "mini"streaming vì nó đơn giản hóa một số điều trong việc triển khai, trong khi một thư viện streaming mạnh mẽ hơn có thể được tối ưu hóa thêm để hoạt động trên I2P. Hai vấn đề chính với thư viện ministreaming là việc sử dụng giao thức thiết lập hai pha TCP truyền thống và kích thước cửa sổ cố định hiện tại là 1. Vấn đề thiết lập là nhỏ đối với các luồng tồn tại lâu dài, nhưng đối với những luồng ngắn, chẳng hạn như các yêu cầu HTTP nhanh, tác động có thể đáng kể. Về kích thước cửa sổ, thư viện ministreaming không duy trì bất kỳ ID hoặc thứ tự nào trong các tin nhắn được gửi (hoặc bao gồm bất kỳ ACK hoặc SACK cấp ứng dụng nào), vì vậy nó phải chờ trung bình gấp đôi thời gian cần thiết để gửi một tin nhắn trước khi gửi tin nhắn khác.

Ngay cả với những vấn đề đó, thư viện ministreaming vẫn hoạt động khá tốt trong nhiều tình huống, và API của nó vừa đơn giản vừa có khả năng giữ nguyên khi các triển khai streaming khác nhau được giới thiệu. Thư viện được triển khai trong file ministreaming.jar riêng của nó. Các nhà phát triển Java muốn sử dụng nó có thể truy cập trực tiếp vào API, trong khi các nhà phát triển sử dụng ngôn ngữ khác có thể sử dụng thông qua hỗ trợ streaming của [SAM](/docs/api/samv3).
