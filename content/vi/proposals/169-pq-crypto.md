---
title: "Giao Thức Mã Hoá Hậu Lượng Tử"
number: "169"
author: "zzz, orignal, drzed, eyedeekay"
created: "2025-01-21"
lastupdated: "2025-06-12"
status: "Open"
thread: "http://zzz.i2p/topics/3294"
target: "0.9.80"
---

## Tổng Quan

Mặc dù nghiên cứu và cạnh tranh mã hóa hậu lượng tử (PQ) đã được tiến hành suốt một thập kỷ, các lựa chọn không trở nên rõ ràng cho đến gần đây.

Chúng tôi bắt đầu xem xét các tiềm năng của mã hóa PQ vào năm 2022 [FORUM](http://zzz.i2p/topics/3294).

Tiêu chuẩn TLS đã thêm hỗ trợ mã hóa lai trong hai năm qua và hiện nay được sử dụng cho một phần đáng kể của lưu lượng mã hóa trên internet nhờ hỗ trợ trong Chrome và Firefox [CLOUDFLARE](https://blog.cloudflare.com/pq-2024/).

NIST gần đây đã hoàn tất và công bố các thuật toán được khuyến nghị cho mã hóa hậu lượng tử [NIST-PQ](https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards). Một số thư viện mã hóa thông dụng hiện nay đã hỗ trợ tiêu chuẩn NIST hoặc sẽ phát hành hỗ trợ trong thời gian tới.

Cả [CLOUDFLARE](https://blog.cloudflare.com/pq-2024/) và [NIST-PQ](https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards) đều khuyến nghị rằng quá trình di chuyển nên bắt đầu ngay lập tức. Cũng xem phần Câu hỏi thường gặp về PQ năm 2022 của NSA [NSA-PQ](https://media.defense.gov/2022/Sep/07/2003071836/-1/-1/0/CSI_CNSA_2.0_FAQ_.PDF). I2P nên là người dẫn đầu trong bảo mật và mã hóa. Bây giờ là thời điểm để triển khai các thuật toán được khuyến nghị. Sử dụng hệ thống loại mật mã và loại chữ ký linh hoạt của chúng ta, chúng ta sẽ thêm các loại cho mật mã lai, và cho chữ ký PQ và lai.

## Mục Tiêu

- Chọn thuật toán chống PQ
- Thêm các thuật toán chỉ PQ và lai vào các giao thức I2P khi thích hợp
- Định nghĩa nhiều biến thể
- Chọn các biến thể tốt nhất sau khi triển khai, thử nghiệm, phân tích và nghiên cứu
- Thêm hỗ trợ từng bước và có khả năng tương thích ngược

## Phi Mục Tiêu

- Không thay đổi giao thức mã hóa một chiều (Noise N)
- Không chuyển khỏi SHA256, không bị đe dọa ngắn hạn bởi PQ
- Không chọn các biến thể ưa thích cuối cùng vào lúc này

## Mô Hình Đe Dọa

- Các bộ định tuyến tại OBEP hoặc IBGW, có thể thông đồng,
  lưu trữ thông điệp garlic để giải mã sau này (bí mật chuyển tiếp)
- Người quan sát mạng 
  lưu trữ tin nhắn truyền tải để giải mã sau này (bí mật chuyển tiếp)
- Các thành viên mạng giả mạo chữ ký cho RI, LS, truyền tải, datagram,
  hoặc các cấu trúc khác

## Giao Thức Bị Ảnh Hưởng

Chúng tôi sẽ điều chỉnh các giao thức sau đây, sắp xếp theo thứ tự phát triển.
Cuộc triển khai tổng thể có thể sẽ từ cuối năm 2025 đến giữa năm 2027.
Xem phần Ưu Tiên và Triển Khai bên dưới để biết chi tiết.
