---
title: "Thảo luận về Tunnel"
description: "Khảo sát lịch sử về đệm cho tunnel, phân mảnh, và các chiến lược xây dựng"
slug: "tunnel"
layout: "single"
lastUpdated: "2019-07"
accurateFor: "0.9.41"
reviewStatus: "needs-review"
---

> **Lưu ý:** Bản lưu trữ này ghi lại công việc thiết kế mang tính suy đoán có từ trước I2P 0.9.41. Đối với bản triển khai cho môi trường sản xuất, hãy tham khảo [tài liệu về tunnel](/docs/specs/implementation/).

## Các lựa chọn cấu hình

Các ý tưởng được cân nhắc cho các tham số cấu hình tunnel trong tương lai bao gồm:

- Cơ chế điều tiết tần suất cho việc chuyển phát thông điệp
- Chính sách padding (đệm dữ liệu) (bao gồm chèn chaff (dữ liệu nhiễu giả))
- Cơ chế kiểm soát vòng đời của Tunnel
- Chiến lược theo lô và hàng đợi cho việc phân phối tải dữ liệu

Không có tùy chọn nào trong số này đi kèm với bản triển khai cũ.

## Các chiến lược đệm

Các cách tiếp cận đệm tiềm năng đã được thảo luận:

- Không có đệm nào cả
- Đệm độ dài ngẫu nhiên
- Đệm độ dài cố định
- Đệm đến kilobyte gần nhất
- Đệm theo lũy thừa của hai (`2^n` byte)

Các phép đo ban đầu (phiên bản 0.4) đã dẫn tới kích thước thông điệp tunnel cố định hiện tại là 1024 byte. Các garlic messages (thông điệp "garlic" trong I2P) ở cấp cao hơn có thể thêm phần đệm riêng của chúng.

## Phân mảnh

Để ngăn chặn các cuộc tấn công gắn thẻ dựa trên độ dài thông điệp, các thông điệp tunnel được cố định ở 1024 byte. Các payload I2NP (tải trọng dữ liệu I2NP) lớn hơn được cổng vào (gateway) phân mảnh; điểm cuối (endpoint) lắp ráp lại các mảnh trong một khoảng thời gian chờ ngắn. Các router có thể sắp xếp lại các mảnh để tối đa hóa hiệu quả đóng gói trước khi gửi.

## Các lựa chọn thay thế bổ sung

### Điều chỉnh xử lý Tunnel khi đang hoạt động

Ba khả năng đã được xem xét:

1. Cho phép một chặng trung gian kết thúc một tunnel tạm thời bằng cách cấp quyền truy cập vào tải dữ liệu đã giải mã.
2. Cho phép các router tham gia “remix” các thông điệp bằng cách gửi chúng qua một trong các tunnel đi ra của chính họ trước khi tiếp tục tới chặng tiếp theo.
3. Cho phép người tạo tunnel tái xác định chặng kế tiếp của một điểm ngang hàng (peer) một cách động.

### Tunnels hai chiều

Việc sử dụng các tunnel vào và ra riêng biệt giới hạn lượng thông tin mà bất kỳ một tập các nút ngang hàng nào có thể quan sát được (ví dụ, một yêu cầu GET so với một phản hồi lớn). Các tunnel hai chiều giúp đơn giản hóa việc quản lý các nút ngang hàng nhưng đồng thời làm lộ toàn bộ mẫu lưu lượng theo cả hai hướng. Do đó, các tunnel một chiều vẫn là thiết kế được ưu tiên.

### Kênh ngược và kích thước biến đổi

Việc cho phép các kích thước thông điệp tunnel (đường hầm) thay đổi sẽ tạo điều kiện cho các kênh ngầm giữa những nút ngang hàng thông đồng (ví dụ: mã hóa dữ liệu thông qua việc lựa chọn kích thước hoặc tần suất). Các thông điệp có kích thước cố định giúp giảm thiểu rủi ro này, nhưng phải đánh đổi bằng chi phí phần đệm bổ sung.

## Các phương án thay thế cho việc xây dựng Tunnel

Tài liệu tham khảo: [Hashing it out in Public](http://www-users.cs.umn.edu/~hopper/hashing_it_out.pdf)

### Phương pháp xây dựng “Parallel” kiểu cũ

Trước bản phát hành 0.6.1.10, các yêu cầu xây dựng tunnel được gửi song song tới từng nút tham gia. Phương pháp này được mô tả trên [trang tunnel cũ](/docs/legacy/old-implementation/).

### Xây dựng kiểu Telescopic (mở rộng theo từng chặng) một lần (Phương pháp hiện tại)

Cách tiếp cận hiện đại gửi các thông điệp dựng tunnel theo kiểu hop-by-hop (từng bước qua từng nút) dọc theo tunnel đang được xây dựng một phần. Mặc dù tương tự telescoping của Tor (mở rộng từng bước), việc định tuyến các thông điệp dựng tunnel qua các tunnel thăm dò giúp giảm rò rỉ thông tin.

### “Tương tác” Telescoping (mở rộng dần kiểu ống lồng)

Xây dựng từng hop (chặng) một với các vòng khứ hồi tường minh cho phép các nút ngang hàng đếm các thông điệp và suy ra vị trí của họ trong tunnel, vì vậy cách tiếp cận này đã bị bác bỏ.

### Các Tunnels quản lý không thăm dò

Một đề xuất là duy trì một nhóm tunnel quản lý riêng cho lưu lượng xây dựng tunnel. Mặc dù điều này có thể giúp các router bị phân tách, nhưng khi tích hợp mạng là đủ thì điều đó được coi là không cần thiết.

### Chuyển phát thăm dò (Legacy)

Trước 0.6.1.10, các yêu cầu tunnel riêng lẻ được mã hóa bằng garlic encryption và chuyển qua các tunnel thăm dò, với các phản hồi quay lại riêng biệt. Chiến lược này đã được thay thế bằng phương pháp one-shot telescoping (thiết lập đường đi qua nhiều chặng theo kiểu telescoping chỉ trong một lần gửi) hiện tại.

## Các điểm rút ra chính

- Các thông điệp tunnel kích thước cố định giúp chống lại đánh dấu dựa trên kích thước và các kênh bí mật, mặc dù phải chịu chi phí đệm (padding) bổ sung.
- Các phương án đệm, phân mảnh (fragmentation), và chiến lược xây dựng đã được xem xét nhưng không được áp dụng khi cân nhắc các đánh đổi về tính ẩn danh.
- Thiết kế tunnel tiếp tục cân bằng giữa hiệu quả, tính quan sát được, và khả năng chống lại các cuộc tấn công predecessor (tiền nhiệm) và congestion (nghẽn).
