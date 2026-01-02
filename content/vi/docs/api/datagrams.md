---
title: "Datagrams"
description: "Các định dạng tin nhắn đã xác thực, có thể trả lời và thô (raw) trên I2CP"
slug: "datagrams"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
toc: true
---

## Tổng quan

Datagram cung cấp giao tiếp định hướng thông điệp trên [I2CP](/docs/specs/i2cp/) và song song với thư viện streaming. Chúng cho phép các gói tin **có thể trả lời**, **được xác thực**, hoặc **thô** mà không cần các luồng định hướng kết nối. Router đóng gói datagram vào các thông điệp I2NP và thông điệp tunnel, bất kể NTCP2 hay SSU2 mang lưu lượng đó.

Động lực cốt lõi là cho phép các ứng dụng (như tracker, DNS resolver, hoặc game) gửi các gói tin độc lập có thể xác định người gửi của chúng.

> **Mới trong năm 2025:** Dự án I2P đã phê duyệt **Datagram2 (protocol 19)** và **Datagram3 (protocol 20)**, bổ sung khả năng bảo vệ chống replay và hệ thống nhắn tin có thể trả lời với chi phí thấp hơn lần đầu tiên trong một thập kỷ.

---

## 1. Hằng số Giao thức

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Protocol</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Value</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Introduced</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>PROTO_DATAGRAM</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">17</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Signed (repliable) datagram – “Datagram1”</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Original</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>PROTO_DATAGRAM_RAW</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">18</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Unsigned (raw) datagram – no sender info</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Original</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>PROTO_DATAGRAM2</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">19</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Signed + replay-protected datagram</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">API 0.9.66 (2025)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>PROTO_DATAGRAM3</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">20</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Repliable (no signature, hash only)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">API 0.9.66 (2025)</td>
    </tr>
  </tbody>
</table>
Các giao thức 19 và 20 đã được chính thức hóa trong **Đề xuất 163 (Tháng 4 năm 2025)**. Chúng cùng tồn tại với Datagram1 / RAW để đảm bảo khả năng tương thích ngược.

---

## 2. Các loại Datagram

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Protocol</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Repliable</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Authenticated</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Replay Protection</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Min Overhead</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Raw</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">18</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Minimal size; spoofable.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Datagram1</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">17</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">≈ 427</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Full Destination + signature.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Datagram2</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">19</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">≈ 457</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Replay prevention + offline signatures; PQ-ready.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Datagram3</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">20</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">≈ 34</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Sender hash only; low overhead.</td>
    </tr>
  </tbody>
</table>
### Các Mẫu Thiết Kế Điển Hình

- **Request → Response:** Gửi một Datagram2 đã ký (yêu cầu + nonce), nhận phản hồi dạng raw hoặc Datagram3 (echo nonce).  
- **Tần suất cao/chi phí thấp:** Ưu tiên Datagram3 hoặc RAW.  
- **Thông điệp điều khiển đã xác thực:** Datagram2.  
- **Tương thích ngược:** Datagram1 vẫn được hỗ trợ đầy đủ.

---

## 3. Chi tiết về Datagram2 và Datagram3 (2025)

### Datagram2 (Giao thức 19)

Phiên bản nâng cấp thay thế cho Datagram1. Tính năng: - **Ngăn chặn tấn công replay:** token chống replay 4 byte. - **Hỗ trợ chữ ký ngoại tuyến:** cho phép sử dụng bởi các Destination được ký ngoại tuyến. - **Mở rộng phạm vi chữ ký:** bao gồm destination hash, cờ, tùy chọn, khối chữ ký ngoại tuyến, payload. - **Sẵn sàng cho hậu lượng tử:** tương thích với các hybrid ML-KEM trong tương lai. - **Chi phí:** ≈ 457 bytes (khóa X25519).

### Datagram3 (Giao thức 20)

Kết nối khoảng cách giữa các loại raw và signed. Tính năng: - **Có thể trả lời mà không cần chữ ký:** chứa hash 32-byte của người gửi + cờ 2-byte. - **Overhead nhỏ gọn:** ≈ 34 bytes. - **Không có cơ chế chống replay** — ứng dụng phải tự triển khai.

Cả hai giao thức đều là tính năng của API 0.9.66 và được triển khai trong router Java kể từ Bản phát hành 2.9.0; chưa có triển khai i2pd hoặc Go (tháng 10 năm 2025).

---

## 4. Giới hạn Kích thước và Phân mảnh

- **Kích thước thông điệp tunnel:** 1 028 byte (4 B Tunnel ID + 16 B IV + 1 008 B payload).  
- **Fragment ban đầu:** 956 B (TUNNEL delivery điển hình).  
- **Fragment tiếp theo:** 996 B.  
- **Số fragment tối đa:** 63–64.  
- **Giới hạn thực tế:** ≈ 62 708 B (~61 KB).  
- **Giới hạn khuyến nghị:** ≤ 10 KB để truyền tải đáng tin cậy (tỷ lệ mất gói tăng theo cấp số nhân khi vượt quá mức này).

**Tóm tắt overhead:** - Datagram1 ≈ 427 B (tối thiểu).   - Datagram2 ≈ 457 B.   - Datagram3 ≈ 34 B.   - Các lớp bổ sung (I2CP gzip header, I2NP, Garlic, Tunnel): + ~5.5 KB trường hợp xấu nhất.

---

## 5. Tích hợp I2CP / I2NP

Đường đi của thông điệp: 1. Ứng dụng tạo datagram (thông qua I2P API hoặc SAM).   2. I2CP bọc với gzip header (`0x1F 0x8B 0x08`, RFC 1952) và checksum CRC-32.   3. Số Protocol + Port được lưu trong các trường gzip header.   4. Router đóng gói thành I2NP message → Garlic clove → các fragment tunnel 1 KB.   5. Các fragment đi qua outbound tunnel → mạng → inbound tunnel.   6. Datagram được ghép lại và chuyển đến application handler dựa trên số protocol.

**Tính toàn vẹn:** CRC-32 (từ I2CP) + chữ ký mật mã tùy chọn (Datagram1/2). Không có trường checksum riêng biệt trong chính datagram.

---

## 6. Giao diện lập trình

### Java API

Package `net.i2p.client.datagram` bao gồm: - `I2PDatagramMaker` – xây dựng các datagram đã ký.   - `I2PDatagramDissector` – xác minh và trích xuất thông tin người gửi.   - `I2PInvalidDatagramException` – được ném ra khi xác minh thất bại.

`I2PSessionMuxedImpl` (`net.i2p.client.impl.I2PSessionMuxedImpl`) quản lý việc ghép kênh giao thức và cổng cho các ứng dụng chia sẻ cùng một Destination.

**Truy cập Javadoc:** - [idk.i2p Javadoc](http://idk.i2p/javadoc-i2p/) (chỉ trong mạng I2P) - [Javadoc Mirror](https://eyedeekay.github.io/javadoc-i2p/) (bản sao trên clearnet) - [Official Javadocs](http://docs.i2p-projekt.de/javadoc/) (tài liệu chính thức)

### Hỗ trợ SAM v3

- SAM 3.2 (2016): đã thêm các tham số PORT và PROTOCOL.  
- SAM 3.3 (2016): giới thiệu mô hình PRIMARY/subsession; cho phép streams + datagrams trên một Destination.  
- Hỗ trợ cho các kiểu phiên Datagram2 / 3 đã được thêm vào đặc tả năm 2025 (đang chờ triển khai).  
- Đặc tả chính thức: [Đặc tả SAM v3](/docs/api/samv3/)

### Các mô-đun i2ptunnel

- **udpTunnel:** Nền tảng hoàn chỉnh và hoạt động đầy đủ cho các ứng dụng I2P UDP (`net.i2p.i2ptunnel.udpTunnel`).  
- **streamr:** Hoạt động cho streaming A/V (`net.i2p.i2ptunnel.streamr`).  
- **SOCKS UDP:** **Không hoạt động** tính đến phiên bản 2.10.0 (chỉ có UDP stub).

> Đối với UDP mục đích chung, hãy sử dụng Datagram API hoặc udpTunnel trực tiếp—không nên dựa vào SOCKS UDP.

---

## 7. Hệ sinh thái và Hỗ trợ Ngôn ngữ (2025)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Language</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Library / Package</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">SAM Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Java</td><td style="border:1px solid var(--color-border); padding:0.5rem;">core API (net.i2p.client.datagram)</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">✓ full support</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">C++</td><td style="border:1px solid var(--color-border); padding:0.5rem;">i2pd / libsam3</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.2 partial</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Limited</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Go</td><td style="border:1px solid var(--color-border); padding:0.5rem;">go-i2p / sam3</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1–3.2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Python</td><td style="border:1px solid var(--color-border); padding:0.5rem;">i2plib, i2p.socket, txi2p</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Rust</td><td style="border:1px solid var(--color-border); padding:0.5rem;">i2p-rs, i2p_client</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">C#</td><td style="border:1px solid var(--color-border); padding:0.5rem;">I2PSharp</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">JS/TS</td><td style="border:1px solid var(--color-border); padding:0.5rem;">node-i2p, i2p-sam</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Haskell</td><td style="border:1px solid var(--color-border); padding:0.5rem;">network-anonymous-i2p</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Experimental</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Lua</td><td style="border:1px solid var(--color-border); padding:0.5rem;">mooni2p</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Experimental</td></tr>
  </tbody>
</table>
Java I2P là router duy nhất hỗ trợ đầy đủ SAM 3.3 subsessions và Datagram2 API tại thời điểm này.

---

## 8. Ví dụ Sử dụng – UDP Tracker (I2PSnark 2.10.0)

Ứng dụng thực tế đầu tiên của Datagram2/3:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Operation</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Datagram Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Purpose</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Announce Request</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Datagram3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Repliable but low-overhead update</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Response</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Raw Datagram</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Minimal payload return</td></tr>
  </tbody>
</table>
Pattern này minh họa việc sử dụng kết hợp các datagram có xác thực và datagram nhẹ để cân bằng giữa bảo mật và hiệu suất.

---

## 9. Bảo mật và Thực hành Tốt nhất

- Sử dụng Datagram2 cho bất kỳ trao đổi được xác thực nào hoặc khi các cuộc tấn công replay quan trọng.
- Ưu tiên Datagram3 cho các phản hồi có thể trả lời nhanh với mức độ tin cậy vừa phải.
- Sử dụng RAW cho phát sóng công khai hoặc dữ liệu ẩn danh.
- Giữ payload ≤ 10 KB để đảm bảo gửi nhận đáng tin cậy.
- Lưu ý rằng SOCKS UDP vẫn không hoạt động.
- Luôn xác minh CRC gzip và chữ ký số khi nhận.

---

## 10. Đặc tả kỹ thuật

Phần này trình bày các định dạng datagram ở mức thấp, đóng gói và chi tiết giao thức.

### 10.1 Xác định giao thức

Các định dạng datagram **không** chia sẻ một header chung. Các router không thể suy ra loại từ các byte payload một mình.

Khi kết hợp nhiều loại datagram—hoặc khi kết hợp datagram với streaming—hãy thiết lập rõ ràng: - **Số hiệu giao thức** (thông qua I2CP hoặc SAM) - Tùy chọn **số cổng**, nếu ứng dụng của bạn ghép kênh các dịch vụ

Để giao thức không được thiết lập (`0` hoặc `PROTO_ANY`) không được khuyến khích và có thể dẫn đến lỗi định tuyến hoặc phân phối.

### 10.2 Raw Datagrams (Datagram Thô)

Các datagram không thể trả lời không mang dữ liệu người gửi hoặc dữ liệu xác thực. Chúng là các payload mờ đục, được xử lý bên ngoài API datagram cấp cao hơn nhưng được hỗ trợ thông qua SAM và I2PTunnel.

**Giao thức:** `18` (`PROTO_DATAGRAM_RAW`)

**Định dạng:**

```
+----+----+----+----+----//
|     payload...
+----+----+----+----+----//
```
Độ dài payload bị giới hạn bởi các giới hạn vận chuyển (tối đa thực tế ≈32 KB, thường ít hơn nhiều).

### 10.3 Datagram1 (Datagram có thể trả lời)

Nhúng **Destination** của người gửi và một **Signature** để xác thực và định địa chỉ phản hồi.

**Giao thức:** `17` (`PROTO_DATAGRAM`)

**Overhead:** ≥427 byte **Payload:** tối đa ~31,5 KB (giới hạn bởi giao thức truyền tải)

**Định dạng:**

```
+----+----+----+----+----+----+----+----+
|               from                    |
+                                       +
|                                       |
~             Destination bytes         ~
|                                       |
+----+----+----+----+----+----+----+----+
|             signature                 |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|     payload...
+----+----+----+----//
```
- `from`: một Destination (387+ byte)
- `signature`: một Signature khớp với loại khóa
  - Với DSA_SHA1: Signature của hash SHA-256 của payload
  - Với các loại khóa khác: Signature trực tiếp trên payload

**Ghi chú:** - Chữ ký cho các loại không phải DSA đã được chuẩn hóa trong I2P 0.9.14. - Chữ ký ngoại tuyến LS2 (Đề xuất 123) hiện không được hỗ trợ trong Datagram1.

### 10.4 Định dạng Datagram2

Một datagram có thể trả lời được cải tiến, bổ sung khả năng **chống replay** như được định nghĩa trong [Đề xuất 163](/proposals/163-datagram2/).

**Giao thức:** `19` (`PROTO_DATAGRAM2`)

Việc triển khai đang được tiến hành. Các ứng dụng nên bao gồm kiểm tra nonce hoặc timestamp để đảm bảo tính dự phòng.

### 10.5 Định dạng Datagram3

Cung cấp các datagram **có thể trả lời nhưng không xác thực**. Dựa vào xác thực phiên do router duy trì thay vì destination và chữ ký được nhúng.

**Giao thức:** `20` (`PROTO_DATAGRAM3`) **Trạng thái:** Đang phát triển từ phiên bản 0.9.66

Hữu ích khi: - Các điểm đến có kích thước lớn (ví dụ: khóa post-quantum) - Xác thực diễn ra ở một lớp khác - Hiệu suất băng thông là yếu tố quan trọng

### 10.6 Tính Toàn Vẹn Dữ Liệu

Tính toàn vẹn của datagram được bảo vệ bởi **gzip CRC-32 checksum** trong lớp I2CP. Không có trường checksum rõ ràng nào tồn tại trong chính định dạng payload của datagram.

### 10.7 Đóng gói Gói tin

Mỗi datagram được đóng gói thành một I2NP message đơn lẻ hoặc thành một clove riêng biệt trong **Garlic Message**. Các lớp I2CP, I2NP và tunnel xử lý độ dài và đóng khung — không có dấu phân cách nội bộ hay trường độ dài trong giao thức datagram.

### 10.8 Các Cân nhắc về Hậu Lượng tử (PQ)

Nếu **Đề xuất 169** (chữ ký ML-DSA) được triển khai, kích thước chữ ký và destination sẽ tăng mạnh — từ ~455 byte lên **≥3739 byte**. Thay đổi này sẽ làm tăng đáng kể chi phí overhead của datagram và giảm dung lượng payload hiệu dụng.

**Datagram3**, dựa trên xác thực cấp phiên (không phải chữ ký nhúng), có khả năng sẽ trở thành thiết kế ưu tiên trong các môi trường I2P hậu lượng tử.

---

## 11. Tài liệu tham khảo

- [Đề xuất 163 – Datagram2 và Datagram3](/proposals/163-datagram2/)
- [Đề xuất 160 – Tích hợp UDP Tracker](/proposals/160-udp-trackers/)
- [Đề xuất 144 – Tính toán MTU Streaming](/proposals/144-ecies-x25519-aead-ratchet/)
- [Đề xuất 169 – Chữ ký Post-Quantum](/proposals/169-pq-crypto/)
- [Đặc tả I2CP](/docs/specs/i2cp/)
- [Đặc tả I2NP](/docs/specs/i2np/)
- [Đặc tả Tunnel Message](/docs/specs/implementation/)
- [Đặc tả SAM v3](/docs/api/samv3/)
- [Tài liệu i2ptunnel](/docs/api/i2ptunnel/)

## 12. Điểm nổi bật của nhật ký thay đổi (2019 – 2025)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Year</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Release</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Change</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">2019</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.43</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Datagram API stabilization</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">2021</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.50</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Protocol port handling reworked</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">2022</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2.0.0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SSU2 adoption completed</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">2024</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2.6.0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Legacy transport removal simplified UDP code</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">2025</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2.9.0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Datagram2/3 support added (Java API)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">2025</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2.10.0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">UDP Tracker implementation released</td></tr>
  </tbody>
</table>
---

## 13. Tóm tắt

Hệ thống con datagram hiện hỗ trợ bốn biến thể giao thức cung cấp một phổ từ xác thực đầy đủ đến truyền tải thô nhẹ. Các nhà phát triển nên chuyển sang **Datagram2** cho các trường hợp sử dụng nhạy cảm về bảo mật và **Datagram3** cho lưu lượng có khả năng trả lời hiệu quả. Tất cả các loại cũ vẫn tương thích để đảm bảo khả năng tương tác dài hạn.
