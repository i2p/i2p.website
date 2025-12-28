---
title: "Hướng dẫn vận hành Tunnel"
description: "Đặc tả hợp nhất cho việc xây dựng, mã hóa và truyền tải lưu lượng qua I2P tunnels."
slug: "implementation"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
reviewStatus: "needs-review"
---

> **Phạm vi:** Hướng dẫn này tổng hợp cách triển khai tunnel, định dạng thông điệp, và cả hai đặc tả tạo tunnel (ECIES và ElGamal cũ). Các liên kết sâu hiện có vẫn hoạt động thông qua các bí danh ở trên.

## Mô hình Tunnel {#tunnel-model}

I2P chuyển tiếp tải trọng dữ liệu qua *tunnels một chiều*: các tập hợp router có thứ tự, truyền lưu lượng theo một hướng duy nhất. Một vòng khứ hồi đầy đủ giữa hai điểm đích cần bốn tunnels (hai ra, hai vào).

Bắt đầu với [Tổng quan về Tunnel](/docs/overview/tunnel-routing/) để nắm thuật ngữ, sau đó dùng hướng dẫn này cho các chi tiết vận hành.

### Vòng đời thông điệp {#message-lifecycle}

1. **Cổng** tunnel gom nhóm một hoặc nhiều thông điệp I2NP, phân mảnh chúng, và ghi các chỉ dẫn chuyển phát.
2. Cổng đóng gói tải trọng vào một thông điệp tunnel có kích thước cố định (1024&nbsp;B), thêm đệm nếu cần.
3. Mỗi **nút tham gia** xác minh hop (chặng) trước, áp dụng lớp mã hóa của mình, và chuyển tiếp {nextTunnelId, nextIV, encryptedPayload} đến hop tiếp theo.
4. **Điểm cuối** tunnel gỡ bỏ lớp cuối cùng, xử lý các chỉ dẫn chuyển phát, lắp ráp lại các mảnh, và gửi đi các thông điệp I2NP đã được lắp ráp lại.

Cơ chế phát hiện trùng lặp sử dụng một bộ lọc Bloom suy giảm theo thời gian, với giá trị lập chỉ mục là phép XOR giữa IV (vector khởi tạo) và khối mã hóa đầu tiên, nhằm ngăn chặn các cuộc tấn công gắn thẻ dựa trên việc hoán đổi IV.

### Tổng quan nhanh về các vai trò {#roles}

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Role</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Pre-processing</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Crypto Operation</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Post-processing</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Outbound gateway (creator)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Fragment, batch, pad</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Iteratively <em>decrypt</em> using every hop’s keys (so downstream peers encrypt)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Forward to first hop</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Participant</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">—</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Encrypt IV and payload with hop keys</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Forward to next hop</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Outbound endpoint</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">—</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Encrypt once more to reveal plaintext payload</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deliver to target tunnel/destination</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Inbound gateway</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Fragment, batch, pad</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Encrypt with local keys</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Forward to next hop</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Inbound endpoint (creator)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">—</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Iteratively decrypt using stored hop keys</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reassemble and deliver locally</td>
    </tr>
  </tbody>
</table>
### Quy trình mã hóa {#encryption-workflow}

- **Inbound tunnels:** gateway (cổng) mã hóa một lần bằng khóa lớp của nó; các thành viên phía sau tiếp tục mã hóa cho đến khi người tạo giải mã tải dữ liệu cuối cùng.
- **Outbound tunnels:** gateway (cổng) áp dụng trước nghịch đảo của mã hóa tại mỗi chặng để mỗi thành viên đều mã hóa. Khi endpoint (điểm cuối) mã hóa, bản rõ gốc của gateway (cổng) được khôi phục.

Cả hai chiều chuyển tiếp `{tunnelId, IV, encryptedPayload}` đến chặng kế tiếp.

---

## Định dạng thông điệp Tunnel {#tunnel-message-format}

Các gateway của tunnel phân mảnh các thông điệp I2NP thành các phong bì có kích thước cố định để che giấu độ dài phần tải và đơn giản hóa việc xử lý ở mỗi chặng (hop).

### Bố cục được mã hóa {#encrypted-layout}

```
+----------------+----------------+-------------------+
| Tunnel ID (4B) | IV (16B)       | Encrypted payload |
+----------------+----------------+-------------------+
```
- **Tunnel ID** – định danh 32-bit cho nút kế tiếp (khác 0, thay đổi luân phiên mỗi chu kỳ dựng).
- **IV** – IV (vector khởi tạo) AES 16 byte được chọn cho mỗi thông điệp.
- **Payload được mã hóa** – 1008 byte bản mã AES-256-CBC.

Tổng kích thước: 1028 byte.

### Bố cục đã giải mã {#decrypted-layout}

Sau khi một hop (nút chuyển tiếp trong tuyến) loại bỏ lớp mã hóa của nó:

```
[Checksum (4B)][Padding ... 0x00 terminator]
[Delivery Instructions 1][I2NP fragment 1]
[Delivery Instructions 2][I2NP fragment 2]
...
```
- **Checksum** xác minh khối đã giải mã.
- **Padding** là các byte ngẫu nhiên khác 0 và kết thúc bằng một byte 0.
- **Delivery instructions** cho điểm cuối biết cách xử lý từng mảnh (giao nội bộ, chuyển tiếp tới một tunnel khác, v.v.).
- **Fragments** mang các thông điệp I2NP bên dưới; điểm cuối lắp ráp lại chúng trước khi chuyển chúng lên các lớp cao hơn.

### Các bước xử lý {#processing-steps}

1. Các cổng phân mảnh và xếp hàng đợi các thông điệp I2NP, giữ tạm các mảnh chưa hoàn chỉnh trong thời gian ngắn để lắp ráp lại.
2. Cổng mã hóa phần tải (payload) bằng các khóa tầng phù hợp và chèn Tunnel ID cùng IV.
3. Mỗi thành viên tham gia mã hóa IV (AES-256/ECB) rồi đến phần tải (AES-256/CBC), sau đó mã hóa lại IV và chuyển tiếp thông điệp.
4. Điểm cuối giải mã theo thứ tự ngược lại, xác minh checksum, xử lý các chỉ dẫn chuyển phát, và lắp ráp lại các mảnh.

---

## Tạo Tunnel (ECIES-X25519) {#tunnel-creation-ecies}

Các router hiện đại xây dựng tunnels bằng các khóa ECIES-X25519, rút gọn các thông điệp dựng tunnel và cho phép tính bí mật chuyển tiếp.

- **Thông điệp dựng (Build message):** một thông điệp I2NP `TunnelBuild` (hoặc `VariableTunnelBuild`) duy nhất mang 1–8 bản ghi dựng đã được mã hóa, mỗi bản ghi tương ứng một hop.
- **Khóa lớp (Layer keys):** bên khởi tạo suy ra các khóa lớp theo từng hop, IV, và khóa phản hồi thông qua HKDF, sử dụng danh tính X25519 tĩnh của hop và khóa tạm thời của bên khởi tạo.
- **Xử lý (Processing):** mỗi hop giải mã bản ghi của mình, xác thực các cờ yêu cầu, ghi khối phản hồi (thành công hoặc mã lỗi chi tiết), mã hóa lại các bản ghi còn lại, rồi chuyển tiếp thông điệp.
- **Phản hồi (Replies):** bên khởi tạo nhận một thông điệp phản hồi được bọc theo garlic encryption (mã hóa garlic). Các bản ghi được đánh dấu thất bại bao gồm một mã mức độ nghiêm trọng để router có thể lập hồ sơ đối tác.
- **Tương thích (Compatibility):** các router vẫn có thể chấp nhận kiểu dựng ElGamal cũ vì lý do tương thích ngược, nhưng các tunnel mới mặc định dùng ECIES.

> Đối với các hằng số theo từng trường và các ghi chú về dẫn xuất khóa, hãy xem lịch sử đề xuất ECIES (lược đồ mã hóa tích hợp trên đường cong elliptic) và mã nguồn router; hướng dẫn này trình bày luồng vận hành.

---

## Tạo Tunnel kiểu cũ (ElGamal-2048) {#tunnel-creation-elgamal}

Định dạng xây dựng tunnel ban đầu đã sử dụng khóa công khai ElGamal. Các router hiện đại duy trì hỗ trợ hạn chế để đảm bảo khả năng tương thích ngược.

> **Trạng thái:** Đã lỗi thời. Được giữ lại ở đây để tham khảo như tư liệu lịch sử và cho bất kỳ ai đang duy trì các công cụ tương thích với hệ thống cũ (legacy).

- **Non-interactive telescoping (mở rộng theo chuỗi không tương tác):** một thông điệp xây dựng duy nhất đi qua toàn bộ đường đi. Mỗi hop (nút trung gian) giải mã bản ghi 528 byte của nó, cập nhật thông điệp, rồi chuyển tiếp nó.
- **Độ dài biến thiên:** Variable Tunnel Build Message (VTBM, thông điệp xây dựng tunnel có độ dài biến thiên) cho phép 1–8 bản ghi. Thông điệp cố định trước đó luôn chứa tám bản ghi để che giấu độ dài tunnel.
- **Bố cục bản ghi yêu cầu:**

```
Bytes 0–3    : Tunnel ID (receiving ID)
Bytes 4–35   : Current hop router hash
Bytes 36–39  : Next tunnel ID
Bytes 40–71  : Next hop router hash
Bytes 72–103 : AES-256 layer key
Bytes 104–135: AES-256 IV key
Bytes 136–167: AES-256 reply key
Bytes 168–183: AES-256 reply IV
Byte 184     : Flags (bit7=IBGW, bit6=OBEP)
Bytes 185–188: Request time (hours since epoch)
Bytes 189–192: Next message ID
Bytes 193–221: Padding
```
- **Cờ:** bit 7 chỉ thị một inbound gateway (IBGW, cổng vào); bit 6 đánh dấu một outbound endpoint (OBEP, điểm ra). Chúng loại trừ lẫn nhau.
- **Mã hóa:** mỗi bản ghi được mã hóa ElGamal-2048 bằng khóa công khai của hop (nút trung gian). Phân lớp đối xứng AES-256-CBC đảm bảo chỉ hop đích có thể đọc bản ghi của mình.
- **Các điểm chính:** ID tunnel là các giá trị 32-bit khác 0; người tạo có thể chèn bản ghi giả để che giấu độ dài tunnel thực; độ tin cậy phụ thuộc vào việc thử lại các lần dựng thất bại.

---

## Các nhóm tunnel và vòng đời {#tunnel-pools}

Các router duy trì các nhóm tunnel vào và ra độc lập cho lưu lượng thăm dò và cho từng phiên I2CP.

- **Chọn peer (nút ngang hàng):** các tunnel thăm dò lấy từ nhóm peer “đang hoạt động, không lỗi” để khuyến khích đa dạng; các tunnel client ưu tiên các peer nhanh, dung lượng cao.
- **Sắp xếp xác định:** các peer được sắp xếp theo khoảng cách XOR giữa `SHA256(peerHash || poolKey)` và khóa ngẫu nhiên của nhóm. Khóa sẽ luân chuyển khi khởi động lại, mang lại sự ổn định trong một lần chạy, đồng thời gây khó cho các cuộc tấn công tiền nhiệm giữa các lần chạy.
- **Vòng đời:** routers theo dõi thời gian dựng lịch sử theo từng bộ {mode, direction, length, variance}. Khi các tunnel sắp hết hạn, việc thay thế bắt đầu sớm; router tăng số lượt dựng song song khi xảy ra lỗi, đồng thời giới hạn số lần thử đang mở.
- **Các tham số cấu hình:** số lượng tunnel active/backup, độ dài hop (bước nhảy mạng) và độ lệch, cho phép zero-hop, và giới hạn tốc độ dựng đều có thể tinh chỉnh theo từng nhóm.

---

## Tắc nghẽn và độ tin cậy {#congestion}

Mặc dù tunnels giống các mạch, routers coi chúng như các hàng đợi thông điệp. Weighted Random Early Discard (WRED) (cơ chế loại bỏ sớm ngẫu nhiên có trọng số) được dùng để giữ độ trễ trong giới hạn:

- Xác suất loại bỏ tăng khi mức sử dụng tiến gần các giới hạn đã cấu hình.
- Các thành phần tham gia xem xét các mảnh có kích thước cố định; gateway/endpoint (cổng/điểm cuối) loại bỏ dựa trên tổng kích thước các mảnh, ưu tiên loại bỏ các payload (dữ liệu tải) lớn trước.
- Các endpoint gửi đi sẽ loại bỏ trước các vai trò khác để lãng phí ít tài nguyên mạng nhất.

Chức năng đảm bảo chuyển phát được dành cho các tầng cao hơn, chẳng hạn như [Streaming library](/docs/specs/streaming/) (thư viện Streaming). Các ứng dụng yêu cầu độ tin cậy phải tự xử lý việc truyền lại và xác nhận.

---

## Tài liệu đọc thêm {#further-reading}

- [Tunnel một chiều (Lịch sử)](/docs/legacy/unidirectional-tunnels/)
- [Lựa chọn peer (nút ngang hàng)](/docs/overview/tunnel-routing#peer-selection/)
- [Tổng quan về tunnel](/docs/overview/tunnel-routing/)
- [Triển khai tunnel cũ](/docs/legacy/old-implementation/)
