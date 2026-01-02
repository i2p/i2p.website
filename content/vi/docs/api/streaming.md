---
title: "Giao thức Streaming"
description: "Giao thức vận chuyển giống TCP được sử dụng bởi hầu hết các ứng dụng I2P"
slug: "streaming"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## Tổng quan

**Thư viện I2P Streaming** cung cấp truyền tải đáng tin cậy, theo thứ tự, được xác thực qua lớp thông điệp của I2P, tương tự như **TCP trên IP**. Nó nằm phía trên [giao thức I2CP](/docs/specs/i2cp/) và được sử dụng bởi hầu hết các ứng dụng I2P tương tác, bao gồm HTTP proxy, IRC, BitTorrent và email.

### Đặc điểm Cốt lõi

- Thiết lập kết nối một pha sử dụng các cờ **SYN**, **ACK**, và **FIN** có thể được đóng gói cùng dữ liệu payload để giảm số lượt truyền tin qua lại.
- **Kiểm soát tắc nghẽn cửa sổ trượt**, với khởi động chậm và tránh tắc nghẽn được điều chỉnh cho môi trường độ trễ cao của I2P.
- Nén gói tin (các phân đoạn nén mặc định 4KB) cân bằng giữa chi phí truyền lại và độ trễ phân mảnh.
- Trừu tượng hóa kênh **xác thực, mã hóa** đầy đủ và **đáng tin cậy** giữa các destination I2P.

Thiết kế này cho phép các yêu cầu và phản hồi HTTP nhỏ hoàn thành trong một lượt truyền dữ liệu duy nhất. Một gói tin SYN có thể chứa dữ liệu yêu cầu, trong khi gói SYN/ACK/FIN của bên phản hồi có thể chứa toàn bộ nội dung phản hồi.

---

## Kiến Thức Cơ Bản về API

API streaming của Java tương tự như lập trình socket Java tiêu chuẩn:

```java
I2PSocketManager mgr = I2PSocketManagerFactory.createManager(host, port, options);
I2PSocket socket       = mgr.connect(destination);
I2PServerSocket server = mgr.getServerSocket();
```
- `I2PSocketManagerFactory` thương lượng hoặc tái sử dụng phiên router thông qua I2CP.  
- Nếu không cung cấp khóa, một destination mới sẽ được tự động tạo ra.  
- Các nhà phát triển có thể truyền các tùy chọn I2CP (ví dụ: độ dài tunnel, các loại mã hóa, hoặc cài đặt kết nối) thông qua map `options`.  
- `I2PSocket` và `I2PServerSocket` phản ánh các giao diện `Socket` Java chuẩn, giúp việc di chuyển trở nên đơn giản.

Tài liệu Javadocs đầy đủ có sẵn từ bảng điều khiển router I2P hoặc [tại đây](/docs/specs/streaming/).

---

## Cấu hình và Điều chỉnh

Bạn có thể truyền các thuộc tính cấu hình khi tạo socket manager thông qua:

```java
I2PSocketManagerFactory.createManager(host, port, properties);
```
### Các Tùy Chọn Khóa

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Option</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Default</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>i2p.streaming.maxWindowSize</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Maximum send window (bytes)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128 KB</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>i2p.streaming.initialRTO</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Initial retransmission timeout</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">9s</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>i2p.streaming.inactivityTimeout</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Timeout before connection close</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">90s</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>i2p.streaming.enforceProtocol</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Enforce protocol ID (prevents confusion)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">true</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>i2p.streaming.congestionAlgorithm</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Congestion control method</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Default (AIMD TCP-like)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>i2p.streaming.disableRejectLogging</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Disable logging rejected packets</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">false</td>
    </tr>
  </tbody>
</table>
### Hành vi theo Khối lượng Công việc

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Workload</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Recommended Settings</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>HTTP-like</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Default parameters are ideal.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Bulk Transfer</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Increase window size to 256 KB or 512 KB; lengthen timeouts.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Real-time Streaming</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Lower tunnel length to 1-2 hops; adjust RTO downwards.</td>
    </tr>
  </tbody>
</table>
Các tính năng mới hơn kể từ phiên bản 0.9.4 bao gồm chặn ghi log từ chối, hỗ trợ danh sách DSA (0.9.21) và thực thi giao thức bắt buộc (0.9.36). Các router kể từ phiên bản 2.10.0 bao gồm mã hóa lai hậu lượng tử (ML-KEM + X25519) tại tầng vận chuyển.

---

## Chi tiết Giao thức

Mỗi luồng được xác định bằng một **Stream ID**. Các gói tin mang các cờ điều khiển tương tự như TCP: `SYNCHRONIZE`, `ACK`, `FIN`, và `RESET`. Các gói tin có thể chứa đồng thời cả dữ liệu và cờ điều khiển, cải thiện hiệu suất cho các kết nối tồn tại trong thời gian ngắn.

### Vòng đời Kết nối

1. **Gửi SYN** — bên khởi tạo bao gồm dữ liệu tùy chọn.  
2. **Phản hồi SYN/ACK** — bên phản hồi bao gồm dữ liệu tùy chọn.  
3. **Hoàn tất ACK** — thiết lập độ tin cậy và trạng thái phiên.  
4. **FIN/RESET** — được sử dụng để đóng có trật tự hoặc kết thúc đột ngột.

### Phân mảnh và sắp xếp lại

Vì các tunnel I2P gây ra độ trễ và sắp xếp lại thứ tự thông điệp, thư viện sẽ đệm các gói tin từ các luồng chưa xác định hoặc đến sớm. Các thông điệp được đệm sẽ được lưu trữ cho đến khi quá trình đồng bộ hóa hoàn tất, đảm bảo việc phân phối đầy đủ và theo đúng thứ tự.

### Thực thi Giao thức

Tùy chọn `i2p.streaming.enforceProtocol=true` (mặc định từ phiên bản 0.9.36) đảm bảo các kết nối sử dụng đúng số giao thức I2CP, ngăn chặn xung đột giữa nhiều hệ thống con chia sẻ cùng một destination.

---

## Khả năng tương tác và Thực hành tốt nhất

Giao thức streaming cùng tồn tại với **Datagram API**, cho phép nhà phát triển lựa chọn giữa giao thức truyền tải hướng kết nối và không kết nối.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Use Case</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Recommended Transport</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reliable, ordered data (HTTP, IRC, FTP)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Streaming</strong></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Connectionless or lossy data (DNS, telemetry)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Datagram</strong></td>
    </tr>
  </tbody>
</table>
### Ứng dụng khách chia sẻ

Các ứng dụng có thể tái sử dụng các tunnel hiện có bằng cách chạy dưới dạng **shared clients** (máy khách chia sẻ), cho phép nhiều dịch vụ chia sẻ cùng một destination. Mặc dù điều này giảm thiểu chi phí hệ thống, nhưng nó làm tăng nguy cơ tương quan giữa các dịch vụ—sử dụng cẩn thận.

### Kiểm Soát Tắc Nghẽn

- Lớp streaming liên tục thích ứng với độ trễ mạng và thропускная способность thông qua phản hồi dựa trên RTT.
- Các ứng dụng hoạt động tốt nhất khi các router đang đóng góp như các peer (bật chế độ tham gia tunnel).
- Các cơ chế kiểm soát tắc nghẽn giống TCP ngăn chặn việc quá tải các peer chậm và giúp cân bằng việc sử dụng băng thông qua các tunnel.

### Các Yếu Tố Về Độ Trễ

Vì I2P thêm vào vài trăm millisecond độ trễ cơ bản, các ứng dụng nên giảm thiểu số lượt truyền tải qua lại. Gộp dữ liệu vào quá trình thiết lập kết nối khi có thể (ví dụ: yêu cầu HTTP trong SYN). Tránh các thiết kế dựa vào nhiều trao đổi tuần tự nhỏ.

---

## Kiểm thử và Tương thích

- Luôn kiểm tra với cả **Java I2P** và **i2pd** để đảm bảo tương thích hoàn toàn.
- Mặc dù giao thức đã được chuẩn hóa, vẫn có thể tồn tại những khác biệt nhỏ trong cách triển khai.
- Xử lý các router cũ một cách mượt mà—nhiều peer vẫn chạy các phiên bản trước 2.0.
- Giám sát thống kê kết nối bằng cách sử dụng `I2PSocket.getOptions()` và `getSession()` để đọc các chỉ số RTT và truyền lại.

Hiệu suất phụ thuộc rất nhiều vào cấu hình tunnel:   - **Tunnel ngắn (1–2 hop)** → độ trễ thấp hơn, tính ẩn danh giảm.   - **Tunnel dài (3+ hop)** → tính ẩn danh cao hơn, RTT tăng.

---

## Cải tiến chính (2.0.0–2.10.0)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Feature</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Introduced</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Persistent ACK Bundling</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.0.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Optimized round-trip reduction for HTTP workloads.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Adaptive Window Scaling</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.3.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Improved large file transfer stability.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Thread Pooling and Socket Reuse</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.5.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reduced per-connection overhead.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Protocol Enforcement Default</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.36</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Ensures correct stream usage.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Hybrid ML-KEM Ratchet</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.10.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Adds post-quantum hybrid encryption layer.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>i2pd Streaming API Compatibility Fixes</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.9.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Full parity with Java I2P library behavior.</td>
    </tr>
  </tbody>
</table>
---

## Tóm tắt

**Thư viện I2P Streaming** là nền tảng cho mọi giao tiếp đáng tin cậy trong I2P. Nó đảm bảo việc truyền tải thông điệp theo thứ tự, được xác thực và mã hóa, đồng thời cung cấp giải pháp thay thế gần như hoàn toàn cho TCP trong môi trường ẩn danh.

Để đạt hiệu suất tối ưu: - Giảm thiểu số lượng round-trip bằng cách gộp SYN+payload.   - Điều chỉnh các tham số window và timeout phù hợp với khối lượng công việc của bạn.   - Ưu tiên các tunnel ngắn hơn cho các ứng dụng nhạy cảm với độ trễ.   - Sử dụng thiết kế thân thiện với tắc nghẽn để tránh quá tải các peer.
