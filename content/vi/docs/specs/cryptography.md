---
title: "Mật mã cấp thấp"
description: "Tóm tắt các nguyên thủy mật mã đối xứng, bất đối xứng và chữ ký được sử dụng trên khắp I2P"
slug: "cryptography"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
reviewStatus: "needs-review"
---

> **Trạng thái:** Trang này cô đọng tài liệu "Low-level Cryptography Specification" (đặc tả mật mã cấp thấp) cũ. Các bản phát hành I2P hiện đại (2.10.0, tháng 10 năm 2025) đã hoàn tất việc chuyển đổi sang các nguyên thủy mật mã mới. Hãy sử dụng các đặc tả chuyên biệt như [ECIES](/docs/specs/ecies/), [Encrypted LeaseSets](/docs/specs/encryptedleaseset/), [NTCP2](/docs/specs/ntcp2/), [Red25519](/docs/specs/red25519-signature-scheme/), [SSU2](/docs/specs/ssu2/), và [Tunnel Creation (ECIES)](/docs/specs/implementation/) để biết chi tiết triển khai.

## Ảnh chụp nhanh quá trình phát triển

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Functional Area</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Legacy Primitive</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Current / Planned Primitive</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Migration Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Transport key exchange</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Diffie–Hellman over 2048-bit prime (NTCP / SSU)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">X25519 (NTCP2 / SSU2)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Completed (NTCP2 and SSU2 fully deployed)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">End-to-end encryption</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ElGamal/AES+SessionTags</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECIES-X25519-AEAD-Ratchet</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Completed (2.4.0+)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Symmetric cipher</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">AES-256/CBC + HMAC-MD5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ChaCha20/Poly1305 (AEAD)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Active (tunnel layer remains AES-256)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Default signatures</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">DSA-SHA1 (1024-bit)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">EdDSA/RedDSA on Ed25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Fully migrated</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Experimental / future</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">—</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Hybrid post-quantum encryption (opt-in)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">In testing (2.10.0)</td>
    </tr>
  </tbody>
  
</table>
## Mã hóa bất đối xứng

### X25519 (thuật toán trao đổi khóa Elliptic Curve Diffie-Hellman dựa trên đường cong elliptic Curve25519)

- Được dùng cho NTCP2, ECIES-X25519-AEAD-Ratchet (cơ chế ECIES dựa trên X25519 sử dụng AEAD và ratchet), SSU2, và khởi tạo tunnel dựa trên X25519.  
- Cung cấp khóa gọn nhẹ, các phép toán thời gian hằng và tính bí mật chuyển tiếp thông qua Noise protocol framework (khung giao thức Noise).  
- Đem lại mức bảo mật 128-bit với khóa 32 byte và trao đổi khóa hiệu quả.

### ElGamal (cũ)

- Được giữ lại để tương thích ngược với các routers cũ hơn.  
- Hoạt động trên số nguyên tố 2048-bit Oakley Group 14 (RFC 3526) với phần tử sinh 2.  
- Mã hóa các khóa phiên AES cùng IV (vector khởi tạo) thành các bản mã 514 byte.  
- Thiếu mã hóa kèm xác thực và bí mật chuyển tiếp; tất cả các điểm cuối hiện đại đã chuyển sang ECIES.

## Mã hóa đối xứng

### ChaCha20/Poly1305 (thuật toán AEAD kết hợp mã dòng ChaCha20 và MAC Poly1305)

- Nguyên thủy mật mã xác thực mặc định được dùng xuyên suốt NTCP2, SSU2 và ECIES.  
- Cung cấp bảo mật AEAD (mã hóa xác thực kèm dữ liệu) và hiệu năng cao ngay cả khi không có hỗ trợ phần cứng AES.  
- Được triển khai theo RFC 7539 (khóa 256‑bit, nonce 96‑bit, thẻ 128‑bit).

### AES‑256/CBC (kiểu cũ)

- Vẫn được dùng cho mã hóa ở tầng tunnel, nơi cấu trúc mã khối của nó phù hợp với mô hình mã hóa phân tầng của I2P.  
- Sử dụng PKCS#5 padding và các biến đổi IV theo từng chặng.  
- Được lên kế hoạch đánh giá dài hạn nhưng vẫn an toàn về mặt mật mã.

## Chữ ký số

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Signature Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Usage Notes</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">DSA‑SHA1 (1024‑bit)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Original default; still accepted for legacy Destinations.</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECDSA‑SHA256/384/512</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Used during 2014–2015 transition.</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Supported</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">EdDSA‑SHA512‑Ed25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Default for Router and Destination identities (since 0.9.15).</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Default</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RedDSA‑SHA512‑Ed25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Used for encrypted LeaseSet signatures (0.9.39+).</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Specialized</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RSA‑SHA512‑4096</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">For out‑of‑band signing (su3 updates, reseeds, plugins).</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Application‑layer</td>
    </tr>
  </tbody>
</table>
## Băm và dẫn xuất khóa

- **SHA‑256:** Được dùng cho các khóa DHT (bảng băm phân tán), HKDF (hàm dẫn xuất khóa dựa trên HMAC), và chữ ký kế thừa (legacy).  
- **SHA‑512:** Được EdDSA/RedDSA (thuật toán chữ ký số đường cong Edwards) sử dụng và được dùng trong các phép dẫn xuất HKDF của Noise (bộ khung giao thức bảo mật).  
- **HKDF‑SHA256:** Dẫn xuất các khóa phiên trong ECIES (lược đồ mã hóa khóa công khai dựa trên đường cong elliptic), NTCP2 và SSU2.  
- Các phép dẫn xuất SHA‑256 xoay vòng theo ngày bảo vệ các vị trí lưu trữ RouterInfo và LeaseSet trong netDb.

## Tóm tắt tầng vận chuyển

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Transport</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Key Exchange</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Encryption</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Authentication</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">NTCP2</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ChaCha20/Poly1305</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">AEAD</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Default TCP transport</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">SSU2</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ChaCha20/Poly1305</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">AEAD</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Default UDP transport</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">SSU (Legacy)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">DH‑2048</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">AES‑256/CBC + HMAC‑MD5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Legacy</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Removed (2.4.0)</td>
    </tr>
  </tbody>
</table>
Cả hai cơ chế truyền tải cung cấp tính bí mật chuyển tiếp ở tầng liên kết và bảo vệ chống phát lại, sử dụng mẫu bắt tay Noise_XK.

## Mã hóa lớp Tunnel

- Tiếp tục sử dụng AES‑256/CBC cho mã hóa phân lớp theo từng hop.  
- Các gateway đầu ra thực hiện giải mã AES lặp dần; mỗi hop mã hóa lại bằng khóa lớp của nó và khóa IV (vector khởi tạo).  
- Mã hóa Double‑IV giúp giảm thiểu các cuộc tấn công tương quan và xác nhận.  
- Việc chuyển sang AEAD (mã hóa xác thực có dữ liệu bổ sung) đang được nghiên cứu nhưng hiện chưa được lên kế hoạch.

## Mật mã hậu lượng tử

- I2P 2.10.0 giới thiệu **mã hóa hậu lượng tử lai mang tính thử nghiệm**.  
- Được bật thủ công qua Trình quản lý Dịch vụ Ẩn để thử nghiệm.  
- Kết hợp X25519 với một KEM (Key Encapsulation Mechanism - cơ chế bao bọc khóa) kháng lượng tử (chế độ lai).  
- Không bật theo mặc định; dành cho mục đích nghiên cứu và đánh giá hiệu năng.

## Khung mở rộng

- Các định danh kiểu mã hóa và chữ ký cho phép hỗ trợ song song nhiều nguyên thủy mật mã.  
- Các ánh xạ hiện tại bao gồm:  
  - **Các kiểu mã hóa:** 0 = ElGamal/AES+SessionTags, 4 = ECIES‑X25519‑AEAD‑Ratchet.  
  - **Các kiểu chữ ký:** 0 = DSA‑SHA1, 7 = EdDSA‑SHA512‑Ed25519, 11 = RedDSA‑SHA512‑Ed25519.  
- Khuôn khổ này cho phép các nâng cấp trong tương lai, bao gồm cả các sơ đồ hậu‑lượng tử, mà không gây phân tách mạng.

## Sự kết hợp mật mã

- **Lớp truyền tải:** X25519 + ChaCha20/Poly1305 (khung Noise).  
- **Lớp tunnel:** Mã hóa phân lớp AES‑256/CBC để đảm bảo ẩn danh.  
- **Đầu‑cuối:** ECIES‑X25519‑AEAD‑Ratchet để đảm bảo tính bí mật và bí mật chuyển tiếp.  
- **Lớp cơ sở dữ liệu:** Chữ ký EdDSA/RedDSA để đảm bảo tính xác thực.

Các lớp này kết hợp lại để cung cấp phòng thủ nhiều lớp: ngay cả khi một lớp bị xâm phạm, các lớp khác vẫn duy trì tính bí mật và tính không thể liên kết.

## Tóm tắt

Ngăn xếp mật mã của I2P 2.10.0 tập trung vào:

- **Curve25519 (X25519)** cho trao đổi khóa  
- **ChaCha20/Poly1305** cho mã hóa đối xứng  
- **EdDSA / RedDSA** cho chữ ký số  
- **SHA‑256 / SHA‑512** cho băm và dẫn xuất  
- **Các chế độ lai hậu lượng tử thử nghiệm** cho khả năng tương thích về sau

Các thuật toán kế thừa ElGamal, AES‑CBC và DSA vẫn được giữ lại để tương thích ngược, nhưng không còn được dùng trong các kênh truyền tải đang hoạt động hoặc các đường dẫn mã hóa.
