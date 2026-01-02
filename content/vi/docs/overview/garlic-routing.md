---
title: "Định tuyến Garlic"
description: "Hiểu về thuật ngữ, kiến trúc và triển khai hiện đại của garlic routing trong I2P"
slug: "garlic-routing"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

---

## 1. Tổng quan

**Garlic routing** vẫn là một trong những đổi mới cốt lõi của I2P, kết hợp mã hóa nhiều lớp, đóng gói thông điệp và các tunnel một chiều. Mặc dù về mặt khái niệm tương tự như **onion routing**, nó mở rộng mô hình để đóng gói nhiều thông điệp được mã hóa ("cloves") trong một phong bì duy nhất ("garlic"), cải thiện hiệu suất và tính ẩn danh.

Thuật ngữ *garlic routing* được đặt ra bởi [Michael J. Freedman](https://www.cs.princeton.edu/~mfreed/) trong [Luận văn Thạc sĩ Free Haven của Roger Dingledine](https://www.freehaven.net/papers.html) (tháng 6 năm 2000, §8.1.1). Các nhà phát triển I2P đã áp dụng thuật ngữ này vào đầu những năm 2000 để phản ánh các cải tiến về đóng gói và mô hình truyền tải một chiều, phân biệt nó với thiết kế chuyển mạch kênh của Tor.

> **Tóm tắt:** Garlic routing = mã hóa nhiều lớp + gộp thông điệp + chuyển phát ẩn danh qua tunnel một chiều.

---

## 2. Thuật ngữ "Garlic"

Trong lịch sử, thuật ngữ *garlic* đã được sử dụng trong ba ngữ cảnh khác nhau trong I2P:

1. **Mã hóa phân lớp** – bảo vệ kiểu onion ở cấp độ tunnel  
2. **Đóng gói nhiều thông điệp** – nhiều "cloves" bên trong một "garlic message"  
3. **Mã hóa đầu cuối đến đầu cuối** – trước đây là *ElGamal/AES+SessionTags*, hiện tại là *ECIES‑X25519‑AEAD‑Ratchet*

Mặc dù kiến trúc vẫn giữ nguyên, nhưng lược đồ mã hóa đã được hiện đại hóa hoàn toàn.

---

## 3. Mã hóa phân lớp

Garlic routing có chung nguyên lý nền tảng với onion routing: mỗi router chỉ giải mã một lớp mã hóa, chỉ biết được hop tiếp theo mà không biết toàn bộ đường đi.

Tuy nhiên, I2P triển khai **tunnel một chiều**, không phải mạch hai chiều:

- **Outbound tunnel**: gửi tin nhắn đi từ người tạo
- **Inbound tunnel**: mang tin nhắn trở về cho người tạo

Một vòng đi về hoàn chỉnh (Alice ↔ Bob) sử dụng bốn tunnel: outbound của Alice → inbound của Bob, sau đó outbound của Bob → inbound của Alice. Thiết kế này **giảm một nửa mức độ phơi bày dữ liệu tương quan** so với các mạch hai chiều.

Để biết chi tiết về triển khai tunnel, xem [Đặc tả Tunnel](/docs/specs/implementation) và đặc tả [Tạo Tunnel (ECIES)](/docs/specs/implementation).

---

## 4. Đóng gói nhiều thông điệp (các "Cloves")

Garlic routing ban đầu của Freedman hình dung việc gộp nhiều "bulbs" (củ) được mã hóa trong một thông điệp. I2P triển khai điều này dưới dạng **cloves** (tép) bên trong một **garlic message** — mỗi clove có hướng dẫn phân phối và đích đến được mã hóa riêng (router, destination, hoặc tunnel).

Garlic bundling cho phép I2P:

- Kết hợp xác nhận và metadata với các thông điệp dữ liệu
- Giảm các mẫu lưu lượng có thể quan sát được
- Hỗ trợ cấu trúc thông điệp phức tạp mà không cần kết nối bổ sung

![Garlic Message Cloves](/images/garliccloves.png)   *Hình 1: Một Garlic Message chứa nhiều clove (gói tin con), mỗi gói có hướng dẫn phân phối riêng.*

Các tép tỏi điển hình bao gồm:

1. **Thông báo Trạng thái Gửi** — xác nhận thành công hoặc thất bại khi gửi.  
   Chúng được bọc trong lớp garlic riêng để bảo vệ tính bảo mật.
2. **Thông báo Database Store** — các LeaseSets được tự động gộp chung để các peer có thể trả lời mà không cần truy vấn lại netDb.

Cloves được gộp lại khi:

- Một LeaseSet mới phải được công bố
- Các session tag mới được gửi đến
- Không có gói tin nào được gộp gần đây (~1 phút theo mặc định)

Garlic messages đạt được việc truyền tải hiệu quả đầu-cuối-đầu của nhiều thành phần được mã hóa trong một gói tin duy nhất.

---

## 5. Sự phát triển của mã hóa

### 5.1 Historical Context

Tài liệu ban đầu (≤ v0.9.12) mô tả mã hóa *ElGamal/AES+SessionTags*:   - Khóa phiên AES được bao bọc bằng **ElGamal 2048‑bit**   - **AES‑256/CBC** để mã hóa payload   - Thẻ phiên 32‑byte được sử dụng một lần cho mỗi tin nhắn

Hệ thống mật mã đó đã **không còn được khuyến nghị sử dụng**.

### 5.2 ECIES‑X25519‑AEAD‑Ratchet (Current Standard)

Từ năm 2019 đến 2023, I2P đã chuyển đổi hoàn toàn sang ECIES‑X25519‑AEAD‑Ratchet. Ngăn xếp hiện đại chuẩn hóa các thành phần sau:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Layer</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">ECIES Primitive or Concept</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Transport Layer (NTCP2, SSU2)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Noise_NX → X25519, ChaCha20/Poly1305, BLAKE2s</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">I2NP Delivery</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECIES‑X25519‑AEAD (ChaCha20/Poly1305)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Session Management</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Ratchet with rekey records, per-clove key material</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Offline Authentication</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">EdDSA (Ed25519) with LeaseSet2/MetaLeaseSet chains</td>
    </tr>
  </tbody>
</table>
Lợi ích của việc chuyển đổi sang ECIES:

- **Bảo mật tiến (forward secrecy)** thông qua các khóa ratcheting cho từng tin nhắn
- **Kích thước payload giảm** so với ElGamal
- **Khả năng phục hồi** trước các tiến bộ phân tích mật mã
- **Tương thích** với các hybrid hậu lượng tử trong tương lai (xem Đề xuất 169)

Chi tiết bổ sung: xem [Đặc tả ECIES](/docs/specs/ecies) và [đặc tả EncryptedLeaseSet](/docs/specs/encryptedleaseset).

---

## 6. LeaseSets and Garlic Bundling

Các garlic envelope thường bao gồm LeaseSet để công bố hoặc cập nhật khả năng tiếp cận đích.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Version</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Key Capabilities</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Distribution Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">LeaseSet (legacy)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Single encryption/signature pair</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Accepted for backward compatibility</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">LeaseSet2</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Multiple crypto suites, offline signing keys</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Default for modern routers</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">EncryptedLeaseSet</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Access-controlled, destination hidden from floodfill</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Requires shared decryption key</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MetaLeaseSet</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Aggregates multiple destinations or multi-homed services</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Extends LeaseSet2 fields recursively</td>
    </tr>
  </tbody>
</table>
Tất cả các LeaseSets được phân phối thông qua *floodfill DHT* được duy trì bởi các routers chuyên biệt. Các bản công bố được xác minh, đánh dấu thời gian và giới hạn tốc độ để giảm thiểu việc liên kết siêu dữ liệu.

Xem [tài liệu Network Database](/docs/specs/common-structures) để biết chi tiết.

---

## 7. Modern “Garlic” Applications within I2P

Mã hóa dựa trên garlic và đóng gói tin nhắn được sử dụng trong toàn bộ ngăn xếp giao thức I2P:

1. **Tạo và sử dụng tunnel** — mã hóa phân lớp trên mỗi hop  
2. **Gửi tin nhắn đầu cuối đến đầu cuối** — các tin nhắn garlic được gộp lại với các clove xác nhận nhận sao và LeaseSet  
3. **Xuất bản Network Database** — các LeaseSet được bao bọc trong các gói garlic để bảo vệ quyền riêng tư  
4. **Giao thức vận chuyển SSU2 và NTCP2** — mã hóa tầng nền sử dụng framework Noise và các primitive X25519/ChaCha20

Garlic routing do đó vừa là một *phương pháp phân lớp mã hóa* vừa là một *mô hình truyền tin mạng*.

---

## 6. LeaseSets và Garlic Bundling

Trung tâm tài liệu của I2P [có sẵn tại đây](/docs/), được duy trì liên tục. Các thông số kỹ thuật liên quan bao gồm:

- [Đặc tả ECIES](/docs/specs/ecies) — ECIES‑X25519‑AEAD‑Ratchet
- [Tạo Tunnel (ECIES)](/docs/specs/implementation) — giao thức xây dựng tunnel hiện đại
- [Đặc tả I2NP](/docs/specs/i2np) — định dạng thông điệp I2NP
- [Đặc tả SSU2](/docs/specs/ssu2) — giao thức vận chuyển SSU2 UDP
- [Cấu trúc chung](/docs/specs/common-structures) — hành vi netDb và floodfill

Xác thực học thuật: Hoang và cộng sự (IMC 2018, USENIX FOCI 2019) và Muntaka và cộng sự (2025) xác nhận tính ổn định kiến trúc và khả năng phục hồi hoạt động của thiết kế I2P.

---

## 7. Các ứng dụng "Garlic" hiện đại trong I2P

Các đề xuất đang tiến hành:

- **Đề xuất 169:** Hybrid hậu lượng tử (ML-KEM 512/768/1024 + X25519)  
- **Đề xuất 168:** Tối ưu hóa băng thông transport  
- **Cập nhật datagram và streaming:** Quản lý tắc nghẽn nâng cao

Các cải tiến trong tương lai có thể bao gồm các chiến lược trì hoãn thông điệp bổ sung hoặc dự phòng đa tunnel ở cấp độ garlic-message, xây dựng dựa trên các tùy chọn phân phối chưa sử dụng ban đầu được Freedman mô tả.

---

## 8. Tài liệu và Tham khảo Hiện tại

- Freedman, M. J. & Dingledine, R. (2000). *Free Haven Master's Thesis,* § 8.1.1. [Free Haven Papers](https://www.freehaven.net/papers.html)  
- [Onion Router Publications](https://www.onion-router.net/Publications.html)  
- [Garlic Routing (Wikipedia)](https://en.wikipedia.org/wiki/Garlic_routing)  
- [Tor Project](https://www.torproject.org/)  
- [Free Haven Anonbib](https://freehaven.net/anonbib/topic.html)  
- Goldschlag, D. M., Reed, M. G., Syverson, P. F. (1996). *Hiding Routing Information.* NRL Publication.

---
