---
title: "Đặc tả SSU2"
description: "Giao thức truyền tải UDP bán tin cậy bảo mật phiên bản 2"
slug: "ssu2"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## 1. Tổng quan

SSU2 là một giao thức lớp vận chuyển dựa trên UDP được dùng cho giao tiếp an toàn, bán tin cậy giữa các router trong I2P. Nó không phải là một cơ chế vận chuyển đa dụng mà được chuyên biệt cho **trao đổi thông điệp I2NP**.

### Khả năng cốt lõi

- Trao đổi khóa có xác thực thông qua mẫu Noise XK (một biến thể bắt tay của bộ giao thức Noise)
- Tiêu đề được mã hóa để chống kiểm tra gói tin sâu (DPI)
- Vượt NAT bằng các nút chuyển tiếp và kỹ thuật đục lỗ
- Di chuyển kết nối và xác thực địa chỉ
- Xác minh đường dẫn tùy chọn
- Tính bí mật chuyển tiếp và bảo vệ chống phát lại

### Hệ thống cũ và khả năng tương thích

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Implementation</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">SSU2 Default</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">SSU1 Removed</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">i2pd</td><td style="border:1px solid var(--color-border); padding:0.6rem;">2.44.0</td><td style="border:1px solid var(--color-border); padding:0.6rem;">2.44.0</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Java I2P</td><td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.56</td><td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.61</td></tr>
  </tbody>
</table>
SSU1 hiện không còn được sử dụng trên khắp mạng I2P công cộng.

---

## 2. Mật mã học

SSU2 (giao thức vận chuyển trong I2P) sử dụng **Noise_XK_25519_ChaChaPoly_SHA256** với các phần mở rộng dành riêng cho I2P.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Function</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Algorithm</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Diffie-Hellman</td><td style="border:1px solid var(--color-border); padding:0.6rem;">X25519 (RFC 7748)</td><td style="border:1px solid var(--color-border); padding:0.6rem;">32-byte keys</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Cipher</td><td style="border:1px solid var(--color-border); padding:0.6rem;">ChaCha20/Poly1305 (RFC 7539)</td><td style="border:1px solid var(--color-border); padding:0.6rem;">AEAD encryption</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Hash</td><td style="border:1px solid var(--color-border); padding:0.6rem;">SHA-256</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Used for key derivation and message integrity</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">KDF</td><td style="border:1px solid var(--color-border); padding:0.6rem;">HKDF-SHA256 (RFC 5869)</td><td style="border:1px solid var(--color-border); padding:0.6rem;">For session and header keys</td></tr>
  </tbody>
</table>
Phần đầu (header) và phần tải (payload) được ràng buộc bằng mật mã thông qua `mixHash()`.  Mọi nguyên thủy mật mã được dùng chung với NTCP2 và ECIES (lược đồ mã hóa tích hợp đường cong elliptic) để tăng hiệu quả triển khai.

---

## 3. Tổng quan về thông điệp

### 3.1 Các quy tắc Datagram UDP

- Mỗi datagram UDP mang **chính xác một thông điệp SSU2**.  
- Session Confirmed messages (các thông điệp xác nhận phiên) có thể bị phân mảnh thành nhiều datagram.

**Kích thước tối thiểu:** 40 byte   **Kích thước tối đa:** 1472 byte (IPv4) / 1452 byte (IPv6)

### 3.2 Các loại thông điệp

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Message</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Header</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Session Request</td><td style="border:1px solid var(--color-border); padding:0.6rem;">32B</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Handshake initiation</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">1</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Session Created</td><td style="border:1px solid var(--color-border); padding:0.6rem;">32B</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Handshake response</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">2</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Session Confirmed</td><td style="border:1px solid var(--color-border); padding:0.6rem;">16B</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Final handshake, may be fragmented</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">6</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Data</td><td style="border:1px solid var(--color-border); padding:0.6rem;">16B</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Encrypted I2NP message blocks</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">7</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Peer Test</td><td style="border:1px solid var(--color-border); padding:0.6rem;">32B</td><td style="border:1px solid var(--color-border); padding:0.6rem;">NAT reachability testing</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">9</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Retry</td><td style="border:1px solid var(--color-border); padding:0.6rem;">32B</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Token or rejection notice</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">10</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Token Request</td><td style="border:1px solid var(--color-border); padding:0.6rem;">32B</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Request for validation token</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">11</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Hole Punch</td><td style="border:1px solid var(--color-border); padding:0.6rem;">32B</td><td style="border:1px solid var(--color-border); padding:0.6rem;">NAT traversal signaling</td></tr>
  </tbody>
</table>
---

## 4. Thiết lập phiên

### 4.1 Luồng tiêu chuẩn (Mã thông báo hợp lệ)

```
Alice                        Bob
SessionRequest  ─────────────>
<──────────────  SessionCreated
SessionConfirmed ────────────>
```
### 4.2 Thu nhận mã thông báo

```
Alice                        Bob
TokenRequest  ───────────────>
<──────────────  Retry (Token)
SessionRequest  ─────────────>
<──────────────  SessionCreated
SessionConfirmed ────────────>
```
### 4.3 Mã thông báo không hợp lệ

```
Alice                        Bob
SessionRequest ─────────────>
<──────────────  Retry (Termination)
```
---

## 5. Cấu trúc tiêu đề

### 5.1 Tiêu đề dài (32 byte)

Được sử dụng trước khi thiết lập phiên (SessionRequest, Created, Retry, PeerTest, TokenRequest, HolePunch).

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Destination Connection ID</td><td style="border:1px solid var(--color-border); padding:0.6rem;">8</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Random unique ID</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Packet Number</td><td style="border:1px solid var(--color-border); padding:0.6rem;">4</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Random (ignored during handshake)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Type</td><td style="border:1px solid var(--color-border); padding:0.6rem;">1</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Message type</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Version</td><td style="border:1px solid var(--color-border); padding:0.6rem;">1</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Always 2</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">NetID</td><td style="border:1px solid var(--color-border); padding:0.6rem;">1</td><td style="border:1px solid var(--color-border); padding:0.6rem;">2 = main I2P network</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Flags</td><td style="border:1px solid var(--color-border); padding:0.6rem;">1</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved (0)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Source Connection ID</td><td style="border:1px solid var(--color-border); padding:0.6rem;">8</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Random ID distinct from destination</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Token</td><td style="border:1px solid var(--color-border); padding:0.6rem;">8</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Token for address validation</td></tr>
  </tbody>
</table>
### 5.2 Header ngắn (16 byte)

Được sử dụng trong các phiên đã được thiết lập (SessionConfirmed, Data).

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Destination Connection ID</td><td style="border:1px solid var(--color-border); padding:0.6rem;">8</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Stable throughout session</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Packet Number</td><td style="border:1px solid var(--color-border); padding:0.6rem;">4</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Incrementing per message</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Type</td><td style="border:1px solid var(--color-border); padding:0.6rem;">1</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Message type (2 or 6)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Flags</td><td style="border:1px solid var(--color-border); padding:0.6rem;">3</td><td style="border:1px solid var(--color-border); padding:0.6rem;">ACK/fragment flags</td></tr>
  </tbody>
</table>
---

## 6. Mã hóa

### 6.1 AEAD (Mã hóa xác thực kèm dữ liệu liên quan)

Tất cả các payload (dữ liệu tải) đều được mã hóa bằng **ChaCha20/Poly1305 AEAD**:

```
ciphertext = ChaCha20_Poly1305_Encrypt(key, nonce, plaintext, associated_data)
```
- Nonce (giá trị dùng một lần): 12 byte (4 byte 0 + 8 byte bộ đếm)
- Tag (mã xác thực): 16 byte
- Associated Data (dữ liệu liên kết): bao gồm tiêu đề để ràng buộc tính toàn vẹn

### 6.2 Bảo vệ tiêu đề

Các phần đầu được che bằng dòng khóa ChaCha20 được dẫn xuất từ các khóa phần đầu phiên. Điều này đảm bảo rằng mọi ID kết nối và các trường gói tin trông ngẫu nhiên, qua đó cung cấp khả năng chống DPI (kiểm tra gói tin sâu).

### 6.3 Dẫn xuất khóa

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Phase</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Input</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Output</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Initial</td><td style="border:1px solid var(--color-border); padding:0.6rem;">introKey + salt</td><td style="border:1px solid var(--color-border); padding:0.6rem;">handshake header key</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Handshake</td><td style="border:1px solid var(--color-border); padding:0.6rem;">DH(X25519)</td><td style="border:1px solid var(--color-border); padding:0.6rem;">chainKey + AEAD key</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Data phase</td><td style="border:1px solid var(--color-border); padding:0.6rem;">chainKey</td><td style="border:1px solid var(--color-border); padding:0.6rem;">TX/RX keys</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Key rotation</td><td style="border:1px solid var(--color-border); padding:0.6rem;">oldKey</td><td style="border:1px solid var(--color-border); padding:0.6rem;">newKey</td></tr>
  </tbody>
</table>
---

## 7. Bảo mật và Ngăn chặn phát lại

- Token áp dụng theo từng địa chỉ IP, hết hạn sau ~60 giây.  
- Việc phát lại (replay) được ngăn chặn thông qua Bloom filter (bộ lọc Bloom) theo từng phiên.  
- Các khóa tạm thời trùng lặp sẽ bị từ chối.  
- Header và payload được ràng buộc bằng mật mã.

Các router phải loại bỏ mọi gói tin không vượt qua xác thực AEAD (mã hóa xác thực kèm dữ liệu liên kết) hoặc có phiên bản hoặc NetID (mã nhận dạng mạng) không hợp lệ.

---

## 8. Đánh số gói tin và vòng đời phiên

Mỗi chiều duy trì bộ đếm 32-bit riêng.   - Bắt đầu từ 0, tăng theo mỗi gói tin.   - Không được phép quay vòng; thay khóa phiên hoặc kết thúc trước khi đạt tới 2³².

Mã định danh kết nối vẫn không thay đổi trong suốt toàn bộ phiên, kể cả trong quá trình di chuyển.

---

## 9. Giai đoạn Dữ liệu

- Loại = 6 (Dữ liệu)
- Tiêu đề ngắn (16 byte)
- Phần tải (payload) chứa một hoặc nhiều khối được mã hóa:
  - Danh sách ACK/NACK (ACK: xác nhận, NACK: không xác nhận)
  - Các mảnh thông điệp I2NP
  - Đệm (0–31 byte ngẫu nhiên)
  - Các khối kết thúc (tùy chọn)

Hỗ trợ truyền lại có chọn lọc và phân phát ngoài thứ tự. Độ tin cậy vẫn ở mức “bán tin cậy” — các gói tin bị thiếu có thể bị loại bỏ lặng lẽ sau khi vượt quá giới hạn số lần thử lại.

---

## 10. Chuyển tiếp và xuyên NAT

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Message</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Purpose</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Peer Test</td><td style="border:1px solid var(--color-border); padding:0.6rem;">7</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Determines inbound reachability</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Retry</td><td style="border:1px solid var(--color-border); padding:0.6rem;">9</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Issues new token or rejection</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Token Request</td><td style="border:1px solid var(--color-border); padding:0.6rem;">10</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Requests new address token</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Hole Punch</td><td style="border:1px solid var(--color-border); padding:0.6rem;">11</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Coordinates NAT hole punching</td></tr>
  </tbody>
</table>
Các router chuyển tiếp hỗ trợ các peer (nút ngang hàng) nằm sau NAT hạn chế thông qua các thông điệp điều khiển này.

---

## 11. Chấm dứt phiên

Một trong hai peer có thể đóng phiên bằng cách sử dụng một **Termination block** (khối kết thúc) trong một Data message (thông điệp dữ liệu).   Tài nguyên phải được giải phóng ngay sau khi nhận được.   Các gói tin kết thúc lặp lại có thể bị bỏ qua sau khi đã được xác nhận.

---

## 12. Hướng dẫn triển khai

Routers **PHẢI**: - Xác minh version = 2 và NetID = 2.   - Loại bỏ các gói <40 byte hoặc AEAD không hợp lệ.   - Thực thi bộ đệm chống phát lại 120 giây.   - Từ chối token bị dùng lại hoặc khóa tạm thời.

Routers **SHOULD**: - Ngẫu nhiên hóa phần đệm 0–31 byte.   - Sử dụng cơ chế tái truyền thích ứng (RFC 6298).   - Triển khai xác thực đường đi theo từng đồng cấp trước khi di chuyển.

---

## 13. Tóm tắt bảo mật

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Property</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Achieved By</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Forward secrecy</td><td style="border:1px solid var(--color-border); padding:0.6rem;">X25519 ephemeral keys</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Replay protection</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Tokens + Bloom filter</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Authenticated encryption</td><td style="border:1px solid var(--color-border); padding:0.6rem;">ChaCha20/Poly1305</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">KCI resistance</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Noise XK pattern</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">DPI resistance</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Encrypted headers</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">NAT traversal</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Relay + Hole Punch</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Migration</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Static connection IDs</td></tr>
  </tbody>
</table>
---

## 14. Tài liệu tham khảo

- [Đề xuất 159 – SSU2](/proposals/159-ssu2/)
- [Khung giao thức Noise](https://noiseprotocol.org/noise.html)
- [RFC 9000 – Truyền tải QUIC](https://datatracker.ietf.org/doc/html/rfc9000)
- [RFC 9001 – QUIC TLS](https://datatracker.ietf.org/doc/html/rfc9001)
- [RFC 7539 – ChaCha20/Poly1305 AEAD](https://datatracker.ietf.org/doc/html/rfc7539)
- [RFC 7748 – X25519 ECDH](https://datatracker.ietf.org/doc/html/rfc7748)
- [RFC 5869 – HKDF-SHA256](https://datatracker.ietf.org/doc/html/rfc5869)
