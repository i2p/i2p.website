---
title: "Tầng vận chuyển"
description: "Tìm hiểu tầng truyền tải của I2P - các phương thức giao tiếp điểm-điểm giữa các router, bao gồm NTCP2 và SSU2"
slug: "transport"
lastUpdated: "2025-03"
accurateFor: "2.10.0"
---

---

## 1. Tổng quan

Một **transport** (cơ chế truyền tải) trong I2P là một phương thức giao tiếp trực tiếp, điểm-đến-điểm giữa các router. Các cơ chế này bảo đảm tính bí mật và toàn vẹn đồng thời thực hiện việc xác thực router.

Mỗi giao thức truyền tải hoạt động theo các mô hình kết nối với các tính năng như xác thực, điều khiển lưu lượng, cơ chế xác nhận và khả năng tái truyền.

---

## 2. Các giao thức truyền tải hiện tại

I2P hiện hỗ trợ hai giao thức truyền tải chính:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Transport</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Protocol</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>NTCP2</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">TCP</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Noise-based TCP transport with modern encryption (as of 0.9.36)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>SSU2</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">UDP</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Secure Semireliable UDP with modern encryption (as of 0.9.56)</td>
    </tr>
  </tbody>
</table>
### 2.1 Các phương thức truyền tải cũ (đã lỗi thời)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Transport</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Protocol</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>NTCP</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">TCP</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Replaced by NTCP2; removed in 0.9.62</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>SSU</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">UDP</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Replaced by SSU2; removed in 0.9.62</td>
    </tr>
  </tbody>
</table>
---

## 3. Dịch vụ truyền tải

Phân hệ truyền tải cung cấp các dịch vụ sau:

### 3.1 Giao nhận thông điệp

- Giao nhận thông điệp [I2NP](/docs/specs/i2np/) đáng tin cậy (các giao thức truyền tải chỉ xử lý thông điệp I2NP)
- Giao nhận theo đúng thứ tự **KHÔNG được đảm bảo** trong mọi trường hợp
- Hàng đợi thông điệp dựa trên ưu tiên

### 3.2 Quản lý kết nối

- Thiết lập và kết thúc kết nối
- Quản lý giới hạn kết nối kèm áp dụng ngưỡng
- Theo dõi trạng thái theo từng nút ngang hàng (peer)
- Thực thi danh sách cấm nút ngang hàng tự động và thủ công

### 3.3 Cấu hình mạng

- Nhiều địa chỉ router cho mỗi giao thức truyền tải (hỗ trợ IPv4 và IPv6 kể từ v0.9.8)
- Mở cổng tường lửa qua UPnP
- Hỗ trợ xuyên NAT/tường lửa
- Phát hiện IP cục bộ bằng nhiều phương pháp

### 3.4 Bảo mật

- Mã hóa cho các trao đổi điểm-điểm
- Xác minh địa chỉ IP theo các quy tắc cục bộ
- Xác định đồng thuận thời gian (dự phòng NTP)

### 3.5 Quản lý băng thông

- Giới hạn băng thông vào và ra
- Lựa chọn phương thức truyền tối ưu cho các thông điệp gửi đi

---

## 4. Địa chỉ truyền tải

Hệ thống con duy trì danh sách các điểm liên hệ của router:

- Phương thức truyền tải (NTCP2, SSU2)
- Địa chỉ IP
- Số cổng
- Tham số tùy chọn

Có thể có nhiều địa chỉ cho mỗi phương thức truyền tải.

### 4.1 Các cấu hình địa chỉ phổ biến

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Configuration</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Hidden</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Routers with no published addresses</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Firewalled</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Routers publishing SSU2 addresses with "introducer" peer lists for NAT traversal</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Unrestricted</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Routers advertising both NTCP2 and SSU2 addresses on IPv4 and/or IPv6</td>
    </tr>
  </tbody>
</table>
---

## 5. Lựa chọn phương thức truyền tải

Hệ thống chọn các giao thức truyền tải cho [thông điệp I2NP](/docs/specs/i2np/) một cách độc lập với các giao thức tầng trên. Việc lựa chọn sử dụng một **hệ thống đấu giá**, trong đó mỗi giao thức truyền tải gửi các mức chào giá, với giá trị thấp nhất sẽ thắng.

### 5.1 Các yếu tố xác định giá thầu

- Thiết lập ưu tiên transport (lớp truyền tải)
- Các kết nối với nút ngang hàng hiện có
- Số lượng kết nối hiện tại so với ngưỡng
- Lịch sử các lần thử kết nối gần đây
- Giới hạn kích thước thông điệp
- Khả năng transport trong RouterInfo của nút ngang hàng
- Độ trực tiếp của kết nối (trực tiếp so với phụ thuộc vào introducer (nút giới thiệu))
- Các ưu tiên transport do nút ngang hàng quảng bá

Thông thường, hai router duy trì các kết nối đồng thời trên một giao thức truyền tải duy nhất, dù cũng có thể duy trì các kết nối đồng thời trên nhiều giao thức truyền tải.

---

## 6. NTCP2

**NTCP2** (Giao thức truyền tải mới 2) là giao thức truyền tải dựa trên TCP hiện đại cho I2P, được giới thiệu trong phiên bản 0.9.36.

### 6.1 Các tính năng chính

- Dựa trên **Noise Protocol Framework** (khung giao thức Noise) (mẫu Noise_XK)
- Sử dụng **X25519** cho trao đổi khóa
- Sử dụng **ChaCha20/Poly1305** cho mã hóa xác thực
- Sử dụng **BLAKE2s** cho băm
- Ngụy trang giao thức để chống lại DPI (kiểm tra gói tin sâu)
- Đệm tùy chọn để chống phân tích lưu lượng

### 6.2 Thiết lập kết nối

1. **Yêu cầu phiên** (Alice → Bob): Khóa X25519 tạm thời + dữ liệu được mã hóa
2. **Tạo phiên** (Bob → Alice): Khóa tạm thời + xác nhận được mã hóa
3. **Xác nhận phiên** (Alice → Bob): Bắt tay cuối cùng kèm RouterInfo (thông tin định danh của router trong I2P)

Mọi dữ liệu về sau được mã hóa bằng các khóa phiên được dẫn xuất từ quá trình bắt tay.

Xem [Đặc tả NTCP2](/docs/specs/ntcp2/) để biết đầy đủ thông tin chi tiết.

---

## 7. SSU2

**SSU2** (Secure Semireliable UDP 2) là phương thức truyền tải dựa trên UDP hiện đại cho I2P, được giới thiệu trong phiên bản 0.9.56.

### 7.1 Các tính năng chính

- Dựa trên **Noise Protocol Framework** (khung giao thức Noise, mẫu Noise_XK)
- Sử dụng **X25519** cho trao đổi khóa
- Sử dụng **ChaCha20/Poly1305** cho mã hóa có xác thực
- Truyền tải bán tin cậy với các xác nhận chọn lọc
- Xuyên NAT qua hole punching (kỹ thuật đục lỗ kết nối) và chuyển tiếp/giới thiệu
- Hỗ trợ di chuyển kết nối
- Phát hiện MTU trên đường đi

### 7.2 Ưu điểm so với SSU (Legacy)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Feature</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">SSU (Legacy)</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">SSU2</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Encryption</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ElGamal + AES</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">X25519 + ChaCha20/Poly1305</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Header encryption</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Partial</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Full (ChaCha20)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Connection ID</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Fixed</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Encrypted, rotatable</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">NAT traversal</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Basic introduction</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Enhanced hole punching + relay</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Obfuscation</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Minimal</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Improved (variable padding)</td>
    </tr>
  </tbody>
</table>
Xem [Đặc tả SSU2](/docs/specs/ssu2/) để biết mọi chi tiết.

---

## 8. Xuyên NAT

Cả hai giao thức truyền tải đều hỗ trợ xuyên NAT để cho phép các router ở sau tường lửa tham gia vào mạng.

### 8.1 Giới thiệu về SSU2

Khi một router không thể nhận kết nối đến trực tiếp:

1. Router công bố các địa chỉ **introducer** (nút giới thiệu) trong RouterInfo của nó
2. Peer đang kết nối gửi yêu cầu giới thiệu tới introducer
3. Introducer chuyển tiếp thông tin kết nối tới router bị tường lửa chặn
4. Router bị tường lửa chặn khởi tạo kết nối đi ra (hole punch — đục lỗ NAT)
5. Giao tiếp trực tiếp được thiết lập

### 8.2 NTCP2 và tường lửa

NTCP2 yêu cầu khả năng kết nối TCP đến từ bên ngoài. Các router phía sau NAT có thể:

- Sử dụng UPnP để tự động mở cổng
- Cấu hình chuyển tiếp cổng thủ công
- Dựa vào SSU2 cho các kết nối đến, đồng thời sử dụng NTCP2 cho các kết nối đi

---

## 9. Làm rối giao thức

Cả hai cơ chế truyền tải hiện đại đều tích hợp các tính năng che giấu:

- **Đệm ngẫu nhiên** trong các thông điệp bắt tay
- **Tiêu đề được mã hóa** mà không để lộ dấu hiệu nhận dạng của giao thức
- **Thông điệp có độ dài thay đổi** để chống phân tích lưu lượng
- **Không có mẫu cố định** trong quá trình thiết lập kết nối

> **Lưu ý**: Kỹ thuật che giấu ở tầng vận chuyển bổ trợ nhưng không thay thế tính ẩn danh do kiến trúc tunnel của I2P cung cấp.

---

## 10. Phát triển trong tương lai

Các nghiên cứu và cải tiến được lên kế hoạch bao gồm:

- **Pluggable transports (các cơ chế truyền tải có thể cắm thêm)** – Các plugin che giấu lưu lượng tương thích với Tor
- **Truyền tải dựa trên QUIC** – Khảo sát lợi ích của giao thức QUIC
- **Tối ưu hóa giới hạn kết nối** – Nghiên cứu xác định giới hạn kết nối ngang hàng tối ưu
- **Chiến lược đệm nâng cao** – Cải thiện khả năng chống phân tích lưu lượng

---

## 11. Tài liệu tham khảo

- [Đặc tả NTCP2](/docs/specs/ntcp2/) – Giao thức truyền tải TCP dựa trên Noise
- [Đặc tả SSU2](/docs/specs/ssu2/) – UDP bán tin cậy, bảo mật 2
- [Đặc tả I2NP](/docs/specs/i2np/) – Các thông điệp của Giao thức Mạng I2P
- [Cấu trúc chung](/docs/specs/common-structures/) – RouterInfo và các cấu trúc địa chỉ
- [Các thảo luận NTCP lịch sử](/docs/ntcp/) – Lịch sử phát triển giao thức truyền tải kiểu cũ
- [Tài liệu SSU cũ](/docs/legacy/ssu/) – Đặc tả SSU ban đầu (đã ngừng dùng)
