---
title: "Thảo luận về Cơ sở dữ liệu mạng"
description: "Ghi chú lịch sử về floodfill, các thử nghiệm Kademlia (một giao thức bảng băm phân tán - DHT), và các tinh chỉnh trong tương lai cho netDb"
slug: "netdb"
reviewStatus: "needs-review"
---

> **Lưu ý:** Bài thảo luận lưu trữ này phác thảo các cách tiếp cận lịch sử đối với cơ sở dữ liệu mạng (netDb). Tham khảo [tài liệu netDb chính](/docs/specs/common-structures/) để biết hành vi và hướng dẫn hiện tại.

## Lịch sử

netDb của I2P được phân phối bằng cách sử dụng một thuật toán floodfill đơn giản. Các bản phát hành sớm cũng duy trì một triển khai Kademlia DHT (bảng băm phân tán Kademlia) như phương án dự phòng, nhưng nó tỏ ra không đáng tin cậy và đã bị vô hiệu hóa hoàn toàn trong phiên bản 0.6.1.20. Thiết kế floodfill chuyển tiếp một mục đã được công bố tới một router tham gia, chờ xác nhận, và thử lại với các peer floodfill khác nếu cần. Các peer floodfill phát quảng bá các bản ghi lưu trữ từ các router không phải floodfill tới mọi thành viên floodfill khác.

Vào cuối năm 2009, việc tra cứu theo Kademlia (một thuật toán bảng băm phân tán - DHT) được tái áp dụng một phần nhằm giảm gánh nặng lưu trữ trên từng floodfill router.

### Giới thiệu về Floodfill

Floodfill lần đầu xuất hiện trong bản phát hành 0.6.0.4, trong khi Kademlia (một thuật toán DHT - bảng băm phân tán) vẫn khả dụng như một phương án dự phòng. Vào thời điểm đó, tình trạng mất gói nghiêm trọng và các tuyến bị hạn chế khiến việc nhận được xác nhận từ bốn nút ngang hàng gần nhất trở nên khó khăn, thường phải thực hiện hàng chục lần thử lưu trữ dư thừa. Việc chuyển sang một tập con floodfill gồm các router có thể truy cập từ bên ngoài đã mang lại một giải pháp thực dụng trong ngắn hạn.

### Xem xét lại Kademlia (thuật toán DHT)

Một số phương án thay thế đã được xem xét bao gồm:

- Vận hành netDb như một Kademlia DHT (bảng băm phân tán Kademlia) được giới hạn ở các routers có thể liên lạc được và chọn tham gia
- Giữ nguyên mô hình floodfill nhưng giới hạn việc tham gia ở các routers đủ khả năng và xác minh việc phân phối bằng các kiểm tra ngẫu nhiên

Phương pháp floodfill được lựa chọn vì dễ triển khai hơn và netDb chỉ mang siêu dữ liệu, không mang tải (payload) của người dùng. Hầu hết các đích (destinations) không bao giờ công bố một LeaseSet vì bên gửi thường gói kèm LeaseSet của mình trong garlic messages (thông điệp Garlic).

## Hiện trạng (Góc nhìn lịch sử)

Các thuật toán netDb được tinh chỉnh cho phù hợp với nhu cầu của mạng và từ trước đến nay có thể xử lý thoải mái vài trăm router. Các ước tính ban đầu cho rằng 3–5 router floodfill có thể hỗ trợ khoảng 10,000 nút.

### Các tính toán cập nhật (Tháng 3 năm 2008)

```
recvKBps = N * (L + 1) * (1 + F) * (1 + R) * S / T
```
Trong đó:

- `N`: Routers trong mạng
- `L`: Số lượng trung bình đích của client trên mỗi router (cộng thêm một cho `RouterInfo`)
- `F`: Tỷ lệ lỗi tunnel
- `R`: Chu kỳ xây dựng lại tunnel dưới dạng tỷ lệ so với thời gian tồn tại của tunnel
- `S`: Kích thước trung bình của bản ghi netDb
- `T`: Thời gian tồn tại của tunnel

Sử dụng các giá trị của giai đoạn năm 2008 (`N = 700`, `L = 0.5`, `F = 0.33`, `R = 0.5`, `S = 4 KB`, `T = 10 minutes`) cho kết quả:

```
recvKBps ≈ 700 * (0.5 + 1) * (1 + 0.33) * (1 + 0.5) * 4 KB / 10m ≈ 28 KBps
```
### Kademlia (thuật toán bảng băm phân tán - DHT) sẽ quay trở lại chứ?

Các nhà phát triển đã thảo luận về việc đưa Kademlia (thuật toán DHT—bảng băm phân tán) trở lại vào khoảng đầu năm 2007. Đồng thuận là năng lực floodfill có thể được mở rộng từng bước khi cần thiết, trong khi Kademlia làm tăng đáng kể độ phức tạp và yêu cầu về tài nguyên đối với tập router cơ sở. Phương án dự phòng vẫn ở trạng thái không hoạt động trừ khi năng lực floodfill trở nên không đủ.

### Hoạch định dung lượng floodfill

Việc tự động đưa các router thuộc lớp băng thông `O` vào floodfill, dù hấp dẫn, vẫn tiềm ẩn nguy cơ các kịch bản tấn công từ chối dịch vụ nếu các nút thù địch chọn tham gia. Phân tích lịch sử cho thấy việc giới hạn pool floodfill (ví dụ, 3–5 nút xử lý khoảng ~10K routers) sẽ an toàn hơn. Các nhà vận hành đáng tin cậy hoặc automatic heuristics (heuristic tự động) đã được sử dụng để duy trì một tập floodfill đủ nhưng có kiểm soát.

## Floodfill TODO (Lịch sử)

> Phần này được giữ lại vì mục đích lưu trữ. Trang netDb chính cập nhật lộ trình hiện tại và các cân nhắc về thiết kế.

Các sự cố vận hành, chẳng hạn như một khoảng thời gian vào ngày 13 tháng 3 năm 2008 khi chỉ có một floodfill router khả dụng, đã thúc đẩy một số cải tiến được đưa vào các bản phát hành từ 0.6.1.33 đến 0.7.x, bao gồm:

- Ngẫu nhiên hóa việc chọn floodfill khi tìm kiếm và ưu tiên các peer (nút ngang hàng) phản hồi tốt
- Hiển thị thêm các chỉ số floodfill trên trang "Profiles" của bảng điều khiển router
- Giảm dần kích thước bản ghi netDb để cắt giảm sử dụng băng thông floodfill
- Tự động opt-in (tự tham gia) cho một tập con các router lớp `O` dựa trên hiệu năng thu thập từ dữ liệu hồ sơ
- Tăng cường blocklisting (danh sách chặn), lựa chọn peer floodfill, và thuật suy nghiệm thăm dò

Các ý tưởng còn lại từ giai đoạn đó bao gồm:

- Sử dụng số liệu thống kê `dbHistory` để đánh giá và lựa chọn các nút floodfill tốt hơn
- Cải thiện hành vi thử lại để tránh liên tục liên hệ với các nút bị lỗi
- Tận dụng các số liệu độ trễ và điểm tích hợp trong khâu lựa chọn
- Phát hiện và phản ứng nhanh hơn trước các floodfill routers bị lỗi
- Tiếp tục giảm nhu cầu tài nguyên trên các nút băng thông cao và các nút floodfill

Ngay tại thời điểm những ghi chú này được viết, mạng lưới được xem là có khả năng chống chịu tốt, với hạ tầng đã được thiết lập để phản ứng nhanh trước các floodfills thù địch hoặc các cuộc tấn công từ chối dịch vụ nhắm vào floodfill.

## Ghi chú bổ sung

- Bảng điều khiển router từ lâu đã cung cấp dữ liệu hồ sơ nâng cao để hỗ trợ phân tích độ tin cậy của floodfill.
- Mặc dù các bình luận trong quá khứ đã suy đoán về Kademlia hoặc các sơ đồ DHT (bảng băm phân tán) thay thế, floodfill vẫn là thuật toán chủ đạo cho các mạng sản xuất.
- Các nghiên cứu hướng tới tương lai tập trung vào việc làm cho việc kết nạp floodfill trở nên thích ứng, đồng thời hạn chế cơ hội bị lạm dụng.
