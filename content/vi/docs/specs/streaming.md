---
title: "Giao thức Streaming (giao thức truyền theo luồng)"
description: "Cơ chế truyền tải đáng tin cậy, tương tự TCP, được hầu hết các ứng dụng I2P sử dụng"
slug: "streaming"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
---

## Tổng quan

I2P Streaming Library (thư viện truyền tải theo luồng của I2P) cung cấp khả năng chuyển giao dữ liệu đáng tin cậy, theo đúng thứ tự và được xác thực trên lớp thông điệp không đáng tin cậy của I2P — tương tự như TCP trên IP. Nó được sử dụng bởi hầu như tất cả các ứng dụng I2P mang tính tương tác như duyệt web, IRC, email và chia sẻ tệp.

Nó đảm bảo truyền dữ liệu đáng tin cậy, điều khiển tắc nghẽn, truyền lại và điều khiển luồng xuyên suốt các tunnel ẩn danh có độ trễ cao của I2P. Mỗi luồng được mã hóa hoàn toàn từ đầu đến cuối giữa các điểm đích.

---

## Các nguyên tắc thiết kế cốt lõi

Thư viện streaming (thư viện truyền luồng) triển khai một **thiết lập kết nối một pha**, trong đó các cờ SYN, ACK và FIN có thể mang tải dữ liệu trong cùng một thông điệp. Điều này giúp giảm thiểu số lượt khứ hồi (round-trip) trong môi trường độ trễ cao — một giao dịch HTTP nhỏ có thể hoàn tất chỉ trong một lượt khứ hồi.

Kiểm soát tắc nghẽn và truyền lại được mô phỏng theo TCP nhưng đã được điều chỉnh cho môi trường của I2P. Kích thước cửa sổ dựa trên thông điệp chứ không dựa trên byte, và được tinh chỉnh theo độ trễ tunnel và overhead (chi phí phụ trội). Giao thức hỗ trợ slow start (khởi động chậm), congestion avoidance (tránh tắc nghẽn), và exponential backoff (giảm lùi theo hàm mũ) tương tự thuật toán AIMD của TCP (Additive Increase, Multiplicative Decrease).

---

## Kiến trúc

Thư viện truyền luồng hoạt động giữa các ứng dụng và giao diện I2CP.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Layer</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Responsibility</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Application</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Standard I2PSocket and I2PServerSocket usage</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Streaming Library</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Connection setup, sequencing, retransmission, and flow control</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>I2CP</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Tunnel creation, routing, and message handling</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>I2NP / Router Layer</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Transport through tunnels</td>
    </tr>
  </tbody>
</table>
Hầu hết người dùng truy cập nó thông qua I2PSocketManager, I2PTunnel hoặc SAMv3. Thư viện xử lý một cách trong suốt việc quản lý destination (điểm đích trong I2P), sử dụng tunnel và truyền lại.

---

## Định dạng gói tin

```
+-----------------------------------------------+
| Send Stream ID (4B) | Receive Stream ID (4B) |
+-----------------------------------------------+
| Sequence Number (4B) | Ack Through (4B)      |
+-----------------------------------------------+
| NACK Count (1B) | optional NACK list (4B each)
+-----------------------------------------------+
| Flags (1B) | Option Size (1B) | Options ...   |
+-----------------------------------------------+
| Payload ...                                  |
```
### Chi tiết phần đầu

- **ID luồng**: Các giá trị 32-bit nhận diện duy nhất các luồng cục bộ và từ xa.
- **Số thứ tự**: Bắt đầu từ 0 đối với SYN, tăng dần theo mỗi thông điệp.
- **Ack Through (xác nhận đến)**: Xác nhận tất cả các thông điệp đến N, ngoại trừ những thông điệp nằm trong danh sách NACK (không xác nhận).
- **Cờ**: Mặt nạ bit điều khiển trạng thái và hành vi.
- **Tùy chọn**: Danh sách có độ dài biến đổi dùng cho RTT, MTU và thương lượng giao thức.

### Cờ khóa

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Flag</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Purpose</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">SYN</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Connection initiation</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ACK</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Acknowledge received packets</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">FIN</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Graceful close</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RST</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reset connection</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">FROM_INCLUDED</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Sender’s destination included</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">SIGNATURE_INCLUDED</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Message signed by sender</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECHO / ECHO_REPLY</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Ping/Pong keepalive</td>
    </tr>
  </tbody>
</table>
---

## Điều khiển luồng và độ tin cậy

Streaming sử dụng **cửa sổ dựa trên thông điệp**, khác với cách tiếp cận dựa trên byte của TCP. Số lượng gói tin chưa được xác nhận được phép trên đường truyền bằng với kích thước cửa sổ hiện tại (mặc định 128).

### Cơ chế

- **Kiểm soát tắc nghẽn:** Khởi đầu chậm và tránh tắc nghẽn dựa trên AIMD (Additive Increase Multiplicative Decrease - tăng tuyến tính, giảm nhân).  
- **Choke/Unchoke:** Tín hiệu điều khiển lưu lượng dựa trên mức chiếm dụng bộ đệm (chặn/giải chặn).  
- **Truyền lại:** Tính toán RTO (thời hạn chờ truyền lại) theo RFC 6298 với cơ chế lùi theo hàm mũ.  
- **Lọc trùng lặp:** Bảo đảm độ tin cậy khi thông điệp có thể bị đảo thứ tự.

Các giá trị cấu hình điển hình:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Parameter</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Default</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>maxWindowSize</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Max unacknowledged messages</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>maxMessageSize</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1730</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Maximum payload bytes per message</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>initialRTO</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">9000 ms</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Initial retransmission timeout</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>inactivityTimeout</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">90000 ms</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Idle connection timeout</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>connectTimeout</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">300000 ms</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Connection establishment timeout</td>
    </tr>
  </tbody>
</table>
---

## Thiết lập kết nối

1. **Bên khởi tạo** gửi một SYN (tùy chọn kèm payload (nội dung dữ liệu) và FROM_INCLUDED).  
2. **Bên đáp ứng** phản hồi bằng SYN+ACK (có thể bao gồm payload).  
3. **Bên khởi tạo** gửi ACK cuối cùng để xác nhận việc thiết lập (kết nối).

Các payload ban đầu tùy chọn cho phép truyền dữ liệu trước khi toàn bộ quá trình bắt tay được hoàn tất.

---

## Chi tiết hiện thực

### Truyền lại và Hết thời gian chờ

Thuật toán truyền lại tuân theo **RFC 6298**.   - **RTO ban đầu:** 9s   - **RTO tối thiểu:** 100ms   - **RTO tối đa:** 45s   - **Alpha:** 0.125   - **Beta:** 0.25

### Chia sẻ khối điều khiển

Các kết nối gần đây tới cùng một nút ngang hàng tái sử dụng RTT (thời gian khứ hồi) và dữ liệu cửa sổ trước đó để đạt tăng tốc ban đầu nhanh hơn, tránh độ trễ “khởi động lạnh”. Các khối điều khiển sẽ hết hạn sau vài phút.

### MTU và phân mảnh

- MTU mặc định: **1730 byte** (đủ cho hai thông điệp I2NP).  
- Đích ECIES: **1812 byte** (giảm chi phí giao thức).  
- MTU tối thiểu được hỗ trợ: 512 byte.

Kích thước payload không bao gồm phần tiêu đề streaming tối thiểu 22 byte.

---

## Lịch sử phiên bản

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Router Version</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Feature</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.7.1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Protocol numbers defined in I2CP</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.11</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Variable-length signatures</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECDSA signature support</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.15</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Ed25519 signature support</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.18</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Ping/Pong payloads</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.20</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">FROM_INCLUDED not required in RESET</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.36</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Protocol enforcement enabled by default</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.39</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">OFFLINE_SIGNATURE support</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.58</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Bob’s hash added to NACK field in SYN</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.10.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Post-Quantum hybrid encryption (experimental)</td>
    </tr>
  </tbody>
</table>
---

## Sử dụng ở cấp độ ứng dụng

### Ví dụ Java

```java
Properties props = new Properties();
props.setProperty("i2p.streaming.maxWindowSize", "512");
I2PSocketManager mgr = I2PSocketManagerFactory.createManager(props);

I2PSocket socket = mgr.connect(destination);
InputStream in = socket.getInputStream();
OutputStream out = socket.getOutputStream();
```
### Hỗ trợ SAMv3 và i2pd

- **SAMv3**: Cung cấp các chế độ STREAM (luồng) và DATAGRAM (datagram) cho các ứng dụng khách không dùng Java.  
- **i2pd**: Cung cấp các tham số streaming (truyền dòng) giống hệt thông qua các tùy chọn trong tệp cấu hình (ví dụ: `i2p.streaming.maxWindowSize`, `profile`, v.v.).

---

## Lựa chọn giữa Streaming (truyền luồng) và Datagrams (gói tin không kết nối)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Use Case</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Recommended Transport</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Reason</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">HTTP, IRC, Email</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Streaming</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Requires reliability</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">DNS</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Repliable Datagram</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Single request/response</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Telemetry, Logging</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Raw Datagram</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Best-effort acceptable</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">P2P DHT</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Datagram</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">High connection churn</td>
    </tr>
  </tbody>
</table>
---

## Bảo mật và tương lai hậu lượng tử

Các phiên streaming được mã hóa đầu-cuối ở lớp I2CP.   Mã hóa lai hậu lượng tử (ML-KEM + X25519) được hỗ trợ ở dạng thử nghiệm trong phiên bản 2.10.0 nhưng mặc định bị tắt.

---

## Tài liệu tham khảo

- [Tổng quan về API Streaming](/docs/specs/streaming/)  
- [Đặc tả Giao thức Streaming](/docs/specs/streaming/)  
- [Đặc tả I2CP](/docs/specs/i2cp/)  
- [Đề xuất 144: Tính toán MTU cho Streaming](/proposals/144-ecies-x25519-aead-ratchet/)  
- [Ghi chú phát hành I2P 2.10.0](/vi/blog/2025/09/08/i2p-2.10.0-release/)
