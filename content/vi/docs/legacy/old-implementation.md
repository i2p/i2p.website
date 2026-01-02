---
title: "Hiện thực Tunnel cũ (di sản)"
description: "Mô tả đã lưu trữ về thiết kế tunnel được sử dụng trước I2P 0.6.1.10."
slug: "old-implementation"
lastUpdated: "2005-06"
accurateFor: "0.6.1"
reviewStatus: "needs-review"
---

> **Trạng thái cũ:** Nội dung này được giữ lại chỉ để tham khảo lịch sử. Nó mô tả hệ thống tunnel được phát hành trước I2P&nbsp;0.6.1.10 và không nên dùng cho phát triển hiện đại. Tham khảo [triển khai hiện tại](/docs/specs/implementation/) để có hướng dẫn cho môi trường sản xuất.

Hệ thống con tunnel ban đầu cũng sử dụng các tunnel một chiều, nhưng khác biệt ở bố cục thông điệp, cơ chế phát hiện trùng lặp và chiến lược xây dựng tunnel. Nhiều phần bên dưới phản chiếu cấu trúc của tài liệu đã ngừng dùng (deprecated) để hỗ trợ việc so sánh.

## 1. Tổng quan về Tunnel

- Các Tunnel được xây dựng thành các chuỗi có thứ tự gồm các router do bên tạo lựa chọn.
- Độ dài Tunnel nằm trong khoảng 0–7 hop (chặng nhảy), với nhiều tham số điều chỉnh cho việc đệm dữ liệu, giới hạn tốc độ và tạo lưu lượng nhiễu.
- Các tunnel vào chuyển tiếp thông điệp từ một cổng không tin cậy tới bên tạo (điểm cuối); các tunnel ra đẩy dữ liệu đi khỏi bên tạo.
- Thời gian sống của Tunnel là 10 phút, sau đó các Tunnel mới được tạo (thường sử dụng cùng các router nhưng ID tunnel khác).

## 2. Hoạt động trong thiết kế cũ

### 2.1 Tiền xử lý thông điệp

Các gateway (cổng) đã tích lũy ≤32&nbsp;KB tải trọng I2NP, chọn phần đệm (padding), và tạo ra một tải trọng chứa:

- Một trường độ dài phần đệm gồm hai byte và số byte ngẫu nhiên tương ứng
- Một dãy các cặp `{instructions, I2NP message}` mô tả đích chuyển phát, phân mảnh, và các độ trễ tùy chọn
- Các thông điệp I2NP đầy đủ được đệm để căn chỉnh tới ranh giới 16 byte

Các chỉ thị chuyển phát đóng gói thông tin định tuyến vào các trường bit (loại chuyển phát, các cờ trì hoãn, các cờ phân mảnh và các phần mở rộng tùy chọn). Các thông điệp bị phân mảnh mang theo một ID thông điệp 4 byte cùng với một cờ chỉ mục/mảnh cuối.

### 2.2 Mã hóa Gateway

Thiết kế cũ cố định độ dài tunnel ở mức tám chặng trong giai đoạn mã hóa. Các gateway xếp chồng các khối AES-256/CBC cùng với checksum để mỗi chặng có thể xác minh tính toàn vẹn mà không làm giảm kích thước payload. Bản thân checksum là một khối dẫn xuất từ SHA-256 được nhúng trong thông điệp.

### 2.3 Hành vi của người tham gia

Các bên tham gia theo dõi các ID của inbound tunnel, xác minh tính toàn vẹn từ sớm và loại bỏ các bản trùng lặp trước khi chuyển tiếp. Vì các khối đệm (padding) và khối xác minh được nhúng sẵn, kích thước thông điệp vẫn không đổi bất kể số bước nhảy.

### 2.4 Xử lý điểm cuối

Các điểm cuối đã giải mã các khối phân lớp một cách tuần tự, xác minh các checksum, và tách tải trọng trở lại thành các chỉ thị đã mã hóa cùng với các thông điệp I2NP để tiếp tục chuyển tiếp.

## 3. Xây dựng Tunnel (Quy trình đã lỗi thời)

1. **Lựa chọn nút ngang hàng:** Các nút ngang hàng được chọn từ các hồ sơ được duy trì cục bộ (exploratory (thăm dò) so với client (khách)). Tài liệu gốc đã nhấn mạnh việc giảm thiểu [predecessor attack](https://en.wikipedia.org/wiki/Predecessor_attack) (tấn công tiền nhiệm) bằng cách tái sử dụng các danh sách nút ngang hàng có thứ tự cho mỗi nhóm tunnel (tunnel pool).
2. **Chuyển phát yêu cầu:** Các thông điệp dựng tunnel được chuyển tiếp theo từng hop (bước nhảy), với các phần được mã hóa cho từng nút ngang hàng. Các ý tưởng thay thế như telescopic extension (mở rộng dạng telescopic), midstream rerouting (định tuyến lại giữa dòng), hoặc loại bỏ các khối checksum đã được thảo luận như các thử nghiệm nhưng chưa bao giờ được áp dụng.
3. **Gom nhóm (pooling):** Mỗi đích cục bộ có các pool vào (inbound) và ra (outbound) riêng biệt. Các thiết lập bao gồm số lượng mong muốn, các tunnel dự phòng, độ biến thiên độ dài, throttling (hạn chế tốc độ), và các chính sách padding (đệm).

## 4. Các khái niệm về giới hạn tốc độ và trộn

Bài viết trước đây đã đề xuất một số chiến lược giúp định hình các bản phát hành sau này:

- Cơ chế loại bỏ sớm ngẫu nhiên có trọng số (WRED) để kiểm soát tắc nghẽn
- Các giới hạn theo từng tunnel dựa trên trung bình trượt của mức sử dụng gần đây
- Các điều khiển nhiễu giả và gom lô tùy chọn (chưa được triển khai đầy đủ)

## 5. Các lựa chọn thay thế đã lưu trữ

Các phần của tài liệu gốc đã khám phá các ý tưởng chưa bao giờ được triển khai:

- Loại bỏ các khối checksum (kiểm tra tổng) để giảm khối lượng xử lý trên mỗi bước nhảy
- Thực hiện telescoping (mở rộng tuần tự) tunnels trong khi đang truyền để thay đổi thành phần nút ngang hàng
- Chuyển sang tunnels hai chiều (cuối cùng đã bị bác bỏ)
- Sử dụng các mã băm ngắn hơn hoặc các cách thức đệm khác

Những ý tưởng này vẫn là bối cảnh lịch sử có giá trị nhưng không phản ánh cơ sở mã hiện nay.

## Tài liệu tham khảo

- Kho lưu trữ tài liệu legacy gốc (trước 0.6.1.10)
- [Tổng quan về Tunnel](/docs/overview/tunnel-routing/) cho thuật ngữ hiện hành
- [Lập hồ sơ và lựa chọn nút ngang hàng](/docs/overview/tunnel-routing#peer-selection/) cho các heuristic hiện đại
