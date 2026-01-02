---
title: "Thảo luận về NTCP"
description: "Ghi chú lịch sử so sánh các giao thức truyền tải NTCP và SSU và các ý tưởng tinh chỉnh được đề xuất"
slug: "ntcp"
layout: "single"
reviewStatus: "needs-review"
---

## Thảo luận NTCP vs. SSU (tháng 3 năm 2007)

### Các câu hỏi về NTCP

_Phỏng theo một cuộc trò chuyện trên IRC giữa zzz và cervantes._

- **Tại sao NTCP được ưu tiên hơn SSU khi NTCP có vẻ như thêm phụ phí (overhead) và độ trễ?**  
  NTCP thường cung cấp độ tin cậy tốt hơn so với bản triển khai SSU ban đầu.
- **Việc truyền (streaming) qua NTCP có gặp phải hiện tượng "TCP-over-TCP collapse" (sự sụp đổ hiệu năng khi TCP lồng trên TCP) kinh điển không?**  
  Có thể, nhưng SSU vốn được thiết kế như một lựa chọn UDP gọn nhẹ và đã tỏ ra quá kém tin cậy trong thực tế.

### “NTCP bị coi là có hại” (zzz, 25 tháng 3, 2007)

Tóm tắt: Độ trễ cao hơn và overhead (phụ phí giao thức) của NTCP có thể gây tắc nghẽn, nhưng cơ chế định tuyến vẫn ưu tiên NTCP vì các điểm bid (điểm ưu tiên) của nó được cố định trong mã ở mức thấp hơn so với SSU. Phân tích đã nêu ra một số điểm:

- Hiện NTCP có mức "bid" thấp hơn SSU, nên routers ưu tiên NTCP trừ khi một phiên SSU đã được thiết lập.
- SSU triển khai cơ chế xác nhận (ACK) với timeout được giới hạn chặt và có thống kê; NTCP dựa vào Java NIO TCP với các timeout kiểu RFC có thể dài hơn nhiều.
- Phần lớn lưu lượng (HTTP, IRC, BitTorrent) dùng thư viện streaming của I2P, thực chất là xếp lớp TCP lên trên NTCP. Khi cả hai lớp đều truyền lại, có thể xảy ra hiện tượng collapse (suy sụp do tắc nghẽn). Tài liệu kinh điển gồm [TCP over TCP is a bad idea](http://sites.inka.de/~W1011/devel/tcp-tcp.html).
- Timeout của thư viện streaming đã tăng từ 10 s lên 45 s trong bản phát hành 0.8; timeout tối đa của SSU là 3 s, trong khi timeout của NTCP được cho là tiệm cận 60 s (khuyến nghị của RFC). Các tham số NTCP khó quan sát từ bên ngoài.
- Quan sát thực địa năm 2007 cho thấy thông lượng tải lên của i2psnark dao động, gợi ý tình trạng suy sụp do tắc nghẽn định kỳ.
- Các thử nghiệm hiệu năng (ép ưu tiên SSU) đã giảm tỷ lệ overhead của tunnel từ khoảng 3.5:1 xuống 3:1 và cải thiện các chỉ số streaming (kích thước cửa sổ, độ trễ khứ hồi (RTT), tỷ lệ gửi/ACK).

#### Các đề xuất từ chủ đề năm 2007

1. **Đảo ưu tiên truyền tải** để routers ưu tiên SSU (khôi phục `i2np.udp.alwaysPreferred`).
2. **Gắn thẻ lưu lượng streaming (thư viện truyền theo luồng của I2P)** để SSU ưu tiên thấp hơn chỉ đối với các thông điệp đã được gắn thẻ, mà không làm tổn hại đến tính ẩn danh.
3. **Siết chặt các giới hạn truyền lại của SSU** để giảm rủi ro sụp đổ.
4. **Nghiên cứu các lớp nền bán tin cậy** để xác định liệu việc truyền lại bên dưới thư viện streaming có mang lại lợi ích ròng hay không.
5. **Rà soát hàng đợi ưu tiên và thời gian chờ**—ví dụ, tăng thời gian chờ của streaming vượt quá 45 s để phù hợp với NTCP.

### Phản hồi của jrandom (27 tháng 3 năm 2007)

Các điểm phản biện chính:

- NTCP tồn tại vì các triển khai SSU thời kỳ đầu đã chịu hiện tượng sụp đổ do tắc nghẽn. Ngay cả các tỷ lệ truyền lại theo từng hop ở mức vừa phải cũng có thể bùng nổ trên các tunnel nhiều hop.
- Không có các xác nhận ở cấp độ tunnel, chỉ một phần thông điệp nhận được trạng thái chuyển phát đầu-cuối; các lỗi có thể diễn ra âm thầm.
- Cơ chế điều khiển tắc nghẽn của TCP đã được tối ưu hóa suốt hàng thập kỷ; NTCP tận dụng những điều đó thông qua các stack TCP trưởng thành.
- Mức tăng hiệu quả quan sát được khi ưu tiên SSU có thể phản ánh hành vi xếp hàng của router hơn là lợi thế nội tại của giao thức.
- Các timeout truyền theo luồng (streaming) dài hơn đã và đang cải thiện độ ổn định; khuyến khích có thêm quan sát và dữ liệu trước khi thực hiện thay đổi lớn.

Cuộc tranh luận đã giúp hoàn thiện việc tối ưu hóa lớp truyền tải sau này nhưng không phản ánh kiến trúc NTCP2/SSU2 hiện đại.
