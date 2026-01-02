---
title: "Tunnel một chiều"
description: "Tóm tắt lịch sử về thiết kế tunnel (đường hầm dữ liệu) một chiều của I2P."
slug: "unidirectional"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

> **Lưu ý lịch sử:** Trang này lưu giữ cuộc thảo luận “Unidirectional Tunnels” (tunnel một chiều) cũ để tham khảo. Hãy tham khảo [tài liệu triển khai tunnel](/docs/specs/implementation/) hiện hành để biết hành vi hiện tại.

## Tổng quan

I2P xây dựng các **tunnel một chiều**: một tunnel mang lưu lượng đi ra và một tunnel riêng mang các phản hồi đi vào. Cấu trúc này bắt nguồn từ những thiết kế mạng sớm nhất và vẫn là một yếu tố khác biệt then chốt so với các hệ thống mạch hai chiều như Tor. Để biết thuật ngữ và chi tiết triển khai, xem [tổng quan về tunnel](/docs/overview/tunnel-routing/) và [đặc tả tunnel](/docs/specs/implementation/).

## Đánh giá

- Các tunnel một chiều tách biệt lưu lượng yêu cầu và phản hồi, vì vậy bất kỳ một nhóm nút ngang hàng thông đồng nào cũng chỉ quan sát được một nửa của một vòng khứ hồi.
- Các tấn công thời gian phải giao cắt hai nhóm tunnel (ra và vào) thay vì phân tích một mạch đơn lẻ, qua đó nâng cao rào cản đối với việc tương quan.
- Các nhóm tunnel vào và ra độc lập cho phép routers điều chỉnh độ trễ, dung lượng và các đặc tính xử lý lỗi theo từng hướng.
- Nhược điểm gồm tăng độ phức tạp trong quản lý nút ngang hàng và nhu cầu duy trì nhiều bộ tunnel để cung cấp dịch vụ đáng tin cậy.

## Tính ẩn danh

Bài báo của Hermann và Grothoff, [*I2P is Slow… and What to Do About It*](http://grothoff.org/christian/i2p.pdf), phân tích các predecessor attacks (tấn công tiền nhiệm) đối với các tunnel một chiều, cho rằng các đối thủ đủ quyết tâm rốt cuộc có thể xác định được các peer (nút ngang hàng) hoạt động lâu dài. Phản hồi từ cộng đồng lưu ý rằng nghiên cứu này dựa trên các giả định cụ thể về mức độ kiên nhẫn và quyền lực pháp lý của đối thủ, và không cân nhắc phương pháp này so với các tấn công thời gian ảnh hưởng đến các thiết kế hai chiều. Các nghiên cứu tiếp nối và kinh nghiệm thực tế tiếp tục củng cố rằng các tunnel một chiều là một lựa chọn ẩn danh có chủ ý chứ không phải một sự bỏ sót.
