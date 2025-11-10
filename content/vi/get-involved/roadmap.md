---
title: "Lộ Trình Phát Triển I2P"
description: "Kế hoạch phát triển hiện tại và cột mốc lịch sử cho mạng I2P"
---

<div style="background: var(--color-bg-secondary); border-left: 4px solid var(--color-primary); padding: 1.5rem; margin-bottom: 2rem; border-radius: var(--radius-md);">

**I2P thực hiện theo mô hình phát triển gia tăng** với các bản phát hành khoảng 13 tuần một lần. Lộ trình này bao gồm phát hành Java cho máy tính để bàn và Android trong một đường phát hành ổn định duy nhất.

**Cập nhật lần cuối:** Tháng 8 năm 2025

</div>

## 🎯 Các Bản Phát Hành Sắp Tới

<div style="border-left: 3px solid var(--color-accent); padding-left: 1.5rem; margin-bottom: 2rem;">

### Phiên Bản 2.11.0
<div style="display: inline-block; background: var(--color-accent); color: white; padding: 0.25rem 0.75rem; border-radius: var(--radius-md); font-size: 0.875rem; margin-bottom: 1rem;">
Mục tiêu: Đầu tháng 12 năm 2025
</div>

- Hybrid PQ MLKEM Ratchet final, kích hoạt theo mặc định (đề xuất 169)
- Jetty 12, yêu cầu Java 17+
- Tiếp tục công việc về PQ (giao thông) (đề xuất 169)
- Hỗ trợ tra cứu I2CP cho các tham số ghi dịch vụ LS (đề xuất 167)
- Điều chặn từng kênh ngầm
- Hệ thống thống kê thân thiện với Prometheus
- Hỗ trợ SAM cho Datagram 2/3

</div>

---

## 📦 Các Bản Phát Hành Gần Đây

### Các Bản Phát Hành 2025

<div style="background: var(--color-bg-secondary); padding: 1.5rem; border-radius: var(--radius-md); margin-bottom: 1.5rem; border-left: 4px solid var(--color-success);">

**Phiên Bản 2.10.0** <span style="color: var(--color-text-muted); font-size: 0.9rem;">— Được Phát Hành Ngày 8 Tháng 9, 2025</span>

- Hỗ trợ theo dõi UDP của i2psnark (đề xuất 160)
- Tham số ghi dịch vụ I2CP LS (một phần) (đề xuất 167)
- API tra cứu không đồng bộ I2CP
- Hybrid PQ MLKEM Ratchet Beta (đề xuất 169)
- Tiếp tục công việc về PQ (giao thông) (đề xuất 169)
- Tham số băng thông xây kênh (đề xuất 168) Phần 2 (xử lý)
- Tiếp tục công việc về điều chặn từng kênh ngầm
- Loại bỏ mã ElGamal giao thông không sử dụng
- Loại bỏ mã bật/tắt "active throttle" cũ của SSU2
- Loại bỏ hỗ trợ ghi nhật ký thống kê cũ
- Dọn dẹp hệ thống thống kê/biểu đồ
- Cải tiến và sửa lỗi chế độ ẩn

</div>

<div style="background: var(--color-bg-secondary); padding: 1.5rem; border-radius: var(--radius-md); margin-bottom: 1.5rem; border-left: 4px solid var(--color-success);">

**Phiên Bản 2.9.0** <span style="color: var(--color-text-muted); font-size: 0.9rem;">— Được Phát Hành Ngày 2 Tháng 6, 2025</span>

- Bản đồ Netdb
- Thực hiện Datagram2, Datagram3 (đề xuất 163)
- Bắt đầu công việc về tham số ghi dịch vụ LS (đề xuất 167)
- Bắt đầu công việc về PQ (đề xuất 169)
- Tiếp tục công việc về điều chặn từng kênh ngầm
- Tham số băng thông xây kênh (đề xuất 168) Phần 1 (gửi)
- Mặc định sử dụng /dev/random cho PRNG trên Linux
- Loại bỏ mã kết xuất LS dư thừa
- Hiển thị nhật ký thay đổi dưới dạng HTML
- Giảm sử dụng luồng của máy chủ HTTP
- Sửa lỗi tự động đăng ký floodfill
- Bản cập nhật Wrapper lên 3.5.60

</div>

<div style="background: var(--color-bg-secondary); padding: 1.5rem; border-radius: var(--radius-md); margin-bottom: 1.5rem; border-left: 4px solid var(--color-success);">

**Phiên Bản 2.8.2** <span style="color: var(--color-text-muted); font-size: 0.9rem;">— Được Phát Hành Ngày 29 Tháng 3, 2025</span>

- Sửa lỗi tham nhũng SHA256

</div>

<div style="background: var(--color-bg-secondary); padding: 1.5rem; border-radius: var(--radius-md); margin-bottom: 1.5rem; border-left: 4px solid var(--color-success);">

**Phiên Bản 2.8.1** <span style="color: var(--color-text-muted); font-size: 0.9rem;">— Được Phát Hành Ngày 17 Tháng 3, 2025</span>

- Sửa lỗi cài đặt thất bại trên Java 21+
- Sửa lỗi "loopback"
- Sửa lỗi kiểm tra kênh ngầm cho kênh ngầm khách hàng ra ngoài
- Sửa lỗi cài đặt vào đường dẫn có dấu cách
- Cập nhật container Docker cũ và các thư viện container
- Bọt thông báo trong điều khiển
- Sắp xếp SusiDNS theo mới nhất
- Sử dụng pool SHA256 trong Noise
- Sửa lỗi và cải tiến giao diện tối của điều khiển
- Hỗ trợ .i2p.alt

</div>

<div style="background: var(--color-bg-secondary); padding: 1.5rem; border-radius: var(--radius-md); margin-bottom: 1.5rem; border-left: 4px solid var(--color-success);">

**Phiên Bản 2.8.0** <span style="color: var(--color-text-muted); font-size: 0.9rem;">— Được Phát Hành Ngày 3 Tháng 2, 2025</span>

- Cải tiến việc công bố RouterInfo
- Cải thiện hiệu quả ACK của SSU2
- Cải thiện xử lý thông điệp lặp lại của SSU2
- Thời gian tra cứu nhanh hơn / thay đổi được
- Cải tiến hết hạn LS
- Thay đổi giới hạn NAT đối xứng
- Thực thi POST trên nhiều mẫu hơn
- Sửa lỗi giao diện tối của SusiDNS
- Dọn dẹp kiểm tra băng thông
- Bản dịch Gan mới
- Thêm tùy chọn giao diện người dùng Kurish
- Bản dựng Jammy mới
- Izpack 5.2.3
- rrd4j 3.10

</div>

<div style="margin: 3rem 0; padding: 1rem 0; border-top: 2px solid var(--color-border); border-bottom: 2px solid var(--color-border);">
  <h3 style="margin: 0; color: var(--color-primary);">📅 Các Bản Phát Hành 2024</h3>
</div>

<div style="background: var(--color-bg-secondary); padding: 1.5rem; border-radius: var(--radius-md); margin-bottom: 1.5rem; border-left: 4px solid var(--color-primary);">

**Phiên Bản 2.7.0** <span style="color: var(--color-text-muted); font-size: 0.9rem;">— 8 Tháng 10, 2024</span>

- Máy chủ HTTP của i2ptunnel giảm sử dụng luồng
- Tunnels UDP Tổng quát trong I2PTunnel
- Trình Duyệt Proxy trong I2PTunnel
- Di Dời Trang Web
- Sửa kênh ngầm chuyển sang màu vàng
- Tái cấu trúc điều khiển /netdb

</div>

<div style="background: var(--color-bg-secondary); padding: 1.5rem; border-radius: var(--radius-md); margin-bottom: 1.5rem; border-left: 4px solid var(--color-primary);">

**Phiên Bản 2.6.1** <span style="color: var(--color-text-muted); font-size: 0.9rem;">— 6 Tháng 8, 2024</span>

- Sửa lỗi kích thước iframe trong điều khiển
- Chuyển đổi biểu đồ sang SVG
- Báo cáo trạng thái dịch bao gồm

</div>

<div style="background: var(--color-bg-secondary); padding: 1.5rem; border-radius: var(--radius-md); margin-bottom: 1.5rem; border-left: 4px solid var(--color-primary);">

**Phiên Bản 2.6.0** <span style="color: var(--color-text-muted); font-size: 0.9rem;">— 19 Tháng 7, 2024</span>

- Giảm sử dụng bộ nhớ netdb
- Loại bỏ mã SSU1
- Sửa lỗi rò rỉ và dừng tệp tạm thời của i2psnark
- PEX hiệu quả hơn trong i2psnark
- Làm mới các biểu đồ JS của điều khiển
- Cải tiến kết xuất biểu đồ
- Tìm kiếm JS Susimail
- Xử lý thông điệp hiệu quả hơn tại OBEP
- Tìm kiếm điểm đích nội địa I2CP hiệu quả hơn
- Sửa lỗi phạm vi biến JS

</div>

<div style="background: var(--color-bg-secondary); padding: 1.5rem; border-radius: var(--radius-md); margin-bottom: 1.5rem; border-left: 4px solid var(--color-primary);">

**Phiên Bản 2.5.2** <span style="color: var(--color-text-muted); font-size: 0.9rem;">— 15 Tháng 5, 2024</span>

- Sửa lỗi cắt HTTP
- Công bố khả năng G nếu phát hiện NAT đối xứng
- Cập nhật lên rrd4j 3.9.1-preview

</div>

<div style="background: var(--color-bg-secondary); padding: 1.5rem; border-radius: var(--radius-md); margin-bottom: 1.5rem; border-left: 4px solid var(--color-primary);">

**Phiên Bản 2.5.1** <span style="color: var(--color-text-muted); font-size: 0.9rem;">— 6 Tháng 5, 2024</span>

- Giảm thiểu tấn công DDoS của NetDB
- Danh sách chặn Tor
- Sửa lỗi và tìm kiếm Susimail
- Tiếp tục loại bỏ mã SSU1
- Cập nhật lên Tomcat 9.0.88

</div>

<div style="background: var(--color-bg-secondary); padding: 1.5rem; border-radius: var(--radius-md); margin-bottom: 1.5rem; border-left: 4px solid var(--color-primary);">

**Phiên Bản 2.5.0** <span style="color: var(--color-text-muted); font-size: 0.9rem;">— 8 Tháng 4, 2024</span>

- Cải tiến giao diện điều khiển iframe
- Thiết kế lại bộ giới hạn băng thông của i2psnark
- Kéo và thả Javascript cho i2psnark và susimail
- Cải tiến xử lý lỗi SSL của i2ptunnel
- Hỗ trợ kết nối HTTP liên tục của i2ptunnel
- Bắt đầu loại bỏ mã SSU1
- Cải tiến yêu cầu thẻ chuyển tiếp SSU2
- Sửa lỗi kiểm tra đồng đối SSU2
- Cải thiện Susimail (tải, đánh dấu, hỗ trợ email HTML)
- Điều chỉnh lựa chọn đồng đối trong kênh ngầm
- Cập nhật RRD4J lên 3.9
- Cập nhật gradlew lên 8.5

</div>

<div style="background: var(--color-bg-secondary); padding: 1.5rem; border-radius: var(--radius-md); margin-bottom: 1.5rem; border-left: 4px solid var(--color-primary);">

**Phiên Bản 2.4.0** <span style="color: var(--color-text-muted); font-size: 0.9rem;">— 18 Tháng 12, 2023</span>

- Quản lý ngữ cảnh NetDB / NetDB Phân khúc
- Xử lý khả năng tắc nghẽn bằng cách hạ ưu tiên router quá tải
- Khôi phục thư viện hỗ trợ Android
- Trình chọn tệp torrent cục bộ của i2psnark
- Sửa lỗi xử lý tra cứu NetDB
- Vô hiệu hóa SSU1
- Cấm router công bố trong tương lai
- Sửa lỗi SAM
- Sửa lỗi Susimail
- Sửa lỗi UPnP

</div>

---

### Các Bản Phát Hành 2023-2022

<details>
<summary>Nhấp để mở rộng các bản phát hành 2023-2022</summary>

**Phiên Bản 2.3.0** — Được Phát Hành Ngày 28 Tháng 6, 2023

- Cải tiến lựa chọn đồng đối cho kênh ngầm
- Hạn định thời gian hết hạn danh sách đen do người dùng cấu hình
- Giảm tốc độ tra cứu nhanh từ cùng nguồn
- Sửa lỗi rò rỉ thông tin phát hiện phát lại
- Sửa lỗi NetDB cho multihomed leaseSets
- Sửa lỗi NetDB cho leaseSets nhận được như một phản hồi trước khi được nhận như một lưu trữ

**Phiên Bản 2.2.1** — Được Phát Hành Ngày 12 Tháng 4, 2023

- Sửa lỗi đóng gói

**Phiên Bản 2.2.0** — Được Phát Hành Ngày 13 Tháng 3, 2023

- Cải tiến lựa chọn đồng đối cho kênh ngầm
- Sửa lỗi phát lại trong streaming

**Phiên Bản 2.1.0** — Được Phát Hành Ngày 10 Tháng 1, 2023

- Sửa lỗi SSU2
- Sửa lỗi tắc nghẽn xây dựng kênh ngầm
- Sửa lỗi kiểm tra đồng đối SSU và phát hiện NAT đối xứng
- Sửa lỗi leaseSets mã hóa LS2 bị lỗi
- Tùy chọn vô hiệu hóa SSU 1 (sơ bộ)
- Đề xuất 161: Đệm nén được
- Tab trạng thái cân nhắc đồng đối mới trên bảng điều khiển
- Thêm hỗ trợ torsocks vào proxy SOCKS và các cải tiến và sửa lỗi khác của SOCKS

**Phiên Bản 2.0.0** — Được Phát Hành Ngày 21 Tháng 11, 2022

- Di chuyển kết nối SSU2
- ACK ngay lập tức của SSU2
- Kích hoạt mặc định SSU2
- Xác thực proxy digest SHA-256 trong i2ptunnel
- Cập nhật quy trình xây dựng Android sử dụng AGP hiện đại
- Hỗ trợ tự động cấu hình trình duyệt I2P cho Máy tính (Desktop)

**Phiên Bản 1.9.0** — Được Phát Hành Ngày 22 Tháng 8, 2022

- Kiểm tra đồng đối SSU2 và triển khai relay
- Sửa lỗi SSU2
- Cải tiến SSU MTU/PMTU
- Kích hoạt SSU2 cho một phần nhỏ các router
- Thêm trình dò ra ngõ cụt
- Sửa lỗi nhập chứng chỉ nhiều hơn
- Sửa lỗi khởi động lại DHT của i2psnark sau khi khởi động lại router

**Phiên Bản 1.8.0** — Được Phát Hành Ngày 23 Tháng 5, 2022

- Sửa lỗi và cải thiện gia đình router
- Sửa lỗi khởi động mềm
- Cải tiến hiệu suất và sửa lỗi SSU
- Sửa lỗi và cải tiến độc lập của I2PSnark
- Tránh hình phạt Sybil cho các gia đình đáng tin cậy
- Giảm thời gian chờ phản hồi xây dựng kênh ngầm
- Sửa lỗi UPnP
- Loại bỏ mã nguồn BOB
- Sửa lỗi nhập chứng chỉ
- Tomcat 9.0.62
- Tái cấu trúc để hỗ trợ SSU2 (đề xuất 159)
- Thực hiện ban đầu của giao thức nền tảng SSU2 (đề xuất 159)
- SAM thông báo ủy quyền popup cho ứng dụng Android
- Cải tiến hỗ trợ cho cài đặt thư mục tùy chỉnh trong i2p.firefox

**Phiên Bản 1.7.0** — Được Phát Hành Ngày 21 Tháng 2, 2022

- Loại bỏ BOB
- Trình chỉnh sửa torrent mới của i2psnark
- Sửa lỗi và cải tiến độc lập của i2psnark
- Cải thiện
