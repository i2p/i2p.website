---
title: "Mã hóa bằng ElGamal/AES + SessionTag (thẻ phiên)"
description: "Mã hóa đầu-cuối kiểu cũ kết hợp ElGamal, AES, SHA-256 và các thẻ phiên dùng một lần"
slug: "elgamal-aes"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
reviewStatus: "needs-review"
---

> **Trạng thái:** Tài liệu này mô tả giao thức mã hóa ElGamal/AES+SessionTag (thẻ phiên) kiểu cũ. Nó vẫn được hỗ trợ chỉ để bảo đảm tương thích ngược, vì các phiên bản I2P hiện đại (2.10.0+) sử dụng [ECIES-X25519-AEAD-Ratchet](/docs/specs/ecies/). Giao thức ElGamal đã bị loại bỏ dần và được giữ lại thuần túy vì mục đích lịch sử và khả năng tương tác.

## Tổng quan

ElGamal/AES+SessionTag đã cung cấp cơ chế mã hóa đầu-cuối ban đầu của I2P dành cho garlic messages (thông điệp "garlic", một dạng thông điệp kết bó đặc trưng của I2P). Nó kết hợp:

- **ElGamal (2048-bit)** — để trao đổi khóa
- **AES-256/CBC** — để mã hóa tải trọng
- **SHA-256** — để băm và dẫn xuất IV
- **Thẻ phiên (32 byte)** — dùng làm định danh thông điệp dùng một lần

Giao thức cho phép routers và các đích giao tiếp một cách an toàn mà không cần duy trì các kết nối lâu dài. Mỗi phiên sử dụng một phép trao đổi ElGamal bất đối xứng để thiết lập một khóa AES đối xứng, tiếp theo là các thông điệp "tagged" nhẹ tham chiếu tới phiên đó.

## Hoạt động của giao thức

### Thiết lập phiên (Phiên mới)

Một phiên mới bắt đầu với một thông điệp gồm hai phần:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Section</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Purpose</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>ElGamal-encrypted block</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">514 bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">222 bytes of plaintext encrypted using the recipient's ElGamal public key</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Establishes the AES session key and IV seed</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>AES-encrypted block</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Variable (≥128 bytes typical)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Payload data, integrity hash, and session tags</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Carries the actual message and new tags</td>
    </tr>
  </tbody>
</table>
Phần bản rõ bên trong khối ElGamal bao gồm:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Session Key</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32 bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">AES-256 key for the session</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Pre-IV</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32 bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Material for deriving the AES initialization vector (<code>IV = first 16 bytes of SHA-256(Pre-IV)</code>)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Random Padding</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">158 bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Filler to reach required ElGamal plaintext length</td>
    </tr>
  </tbody>
</table>
### Các thông điệp của phiên hiện có

Khi một phiên đã được thiết lập, bên gửi có thể gửi các thông điệp **existing-session** bằng cách sử dụng các thẻ phiên đã được lưu vào bộ đệm:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Session Tag</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32 bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Single-use identifier tied to the existing session key</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">AES-Encrypted Block</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Variable</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Encrypted payload and metadata using the established AES key</td>
    </tr>
  </tbody>
</table>
Các router lưu vào bộ nhớ đệm các thẻ đã được chuyển đến trong khoảng **15 phút**, sau đó các thẻ chưa dùng sẽ hết hạn. Mỗi thẻ chỉ hợp lệ cho đúng **một thông điệp** nhằm ngăn chặn các cuộc tấn công tương quan.

### Định dạng khối mã hóa AES

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Tag Count</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2 bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Number (0–200) of new session tags included</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Session Tags</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32 × N bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Newly generated single-use tags</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Payload Size</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4 bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Length of the payload in bytes</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Payload Hash</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32 bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">SHA-256 digest of the payload</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Flag</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1 byte</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>0x00</code> normal, <code>0x01</code> = new session key follows (unused)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">New Session Key</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32 bytes (optional)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Replacement AES key (rarely used)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Payload</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Variable</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Encrypted message data</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Padding</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Variable (16-byte aligned)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Random padding to block boundary</td>
    </tr>
  </tbody>
</table>
Các router giải mã bằng khóa phiên và IV (vector khởi tạo) được suy ra từ Pre-IV (IV tiền khởi tạo, dành cho phiên mới) hoặc session tag (thẻ phiên, dành cho phiên hiện có). Sau khi giải mã, chúng xác minh tính toàn vẹn bằng cách tính lại hàm băm SHA-256 của tải trọng bản rõ.

## Quản lý Session Tag (thẻ phiên)

- Các tag (thẻ) là **một chiều**: các tag từ Alice → Bob không thể được sử dụng lại cho Bob → Alice.
- Tag hết hạn sau khoảng **15 phút**.
- Routers duy trì các bộ quản lý khóa phiên theo từng đích để theo dõi tag, khóa và thời điểm hết hạn.
- Các ứng dụng có thể kiểm soát hành vi của tag thông qua [tùy chọn I2CP](/docs/specs/i2cp/):
  - **`i2cp.tagThreshold`** — số lượng tag được lưu đệm tối thiểu trước khi bổ sung
  - **`i2cp.tagCount`** — số lượng tag mới trên mỗi thông điệp

Cơ chế này giảm thiểu các lần bắt tay ElGamal (một hệ mật mã) tốn kém, đồng thời vẫn duy trì tính không thể liên kết giữa các thông điệp.

## Cấu hình và Hiệu quả

Session tags (thẻ phiên) được giới thiệu nhằm cải thiện hiệu suất trên lớp truyền tải có độ trễ cao và không đảm bảo thứ tự của I2P. Một cấu hình điển hình gửi kèm **40 thẻ cho mỗi thông điệp**, làm tăng thêm khoảng 1.2 KB phụ trội. Các ứng dụng có thể điều chỉnh hành vi chuyển phát dựa trên lưu lượng dự kiến:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Use Case</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Recommended Tags</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Short-lived requests (HTTP, datagrams)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0 – 5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Low overhead, may trigger ElGamal fallback</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Persistent streams or bulk transfer</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">20 – 50</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Higher bandwidth use, avoids session re-establishment</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Long-term services</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">50+</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Ensures steady tag supply despite loss or delay</td>
    </tr>
  </tbody>
</table>
Các router định kỳ dọn sạch các thẻ đã hết hạn và loại bỏ trạng thái phiên không được sử dụng nhằm giảm mức sử dụng bộ nhớ và giảm thiểu các tấn công làm ngập thẻ (tag-flooding attacks).

## Hạn chế

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Category</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Limitation</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Performance</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">514-byte ElGamal block adds heavy overhead for new sessions; session tags consume 32 bytes each.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Security</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">No forward secrecy – compromise of ElGamal private key exposes past sessions.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Integrity</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">AES-CBC requires manual hash verification; no AEAD.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Quantum Resistance</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Vulnerable to Shor's algorithm – will not survive quantum attacks.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Complexity</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Requires stateful tag management and careful timeout tuning.</td>
    </tr>
  </tbody>
</table>
Những thiếu sót này đã trực tiếp thúc đẩy việc thiết kế giao thức [ECIES-X25519-AEAD-Ratchet](/docs/specs/ecies/), giao thức này cung cấp bảo mật chuyển tiếp hoàn hảo, mã hóa có xác thực và trao đổi khóa hiệu quả.

## Trạng thái ngừng hỗ trợ và chuyển đổi

- **Giới thiệu:** Các bản phát hành I2P thời kỳ đầu (trước 0.6)
- **Ngừng dùng:** Khi giới thiệu ECIES-X25519 (sơ đồ ECIES dùng X25519) (0.9.46 → 0.9.48)
- **Gỡ bỏ:** Không còn là mặc định kể từ 2.4.0 (Tháng 12 năm 2023)
- **Hỗ trợ:** Chỉ nhằm tương thích ngược

Các router và các điểm đích hiện nay quảng bá **kiểu mã hóa 4 (ECIES-X25519)** thay vì **kiểu 0 (ElGamal/AES)**. Giao thức cũ vẫn được công nhận để đảm bảo khả năng tương tác với các đồng cấp lỗi thời nhưng không nên sử dụng cho các triển khai mới.

## Bối cảnh lịch sử

ElGamal/AES+SessionTag là nền tảng cho kiến trúc mật mã ban đầu của I2P. Thiết kế lai của nó đã giới thiệu các đổi mới như thẻ phiên dùng một lần và các phiên một chiều, qua đó ảnh hưởng đến các giao thức về sau. Nhiều ý tưởng này đã phát triển thành các cấu trúc hiện đại như deterministic ratchets (cơ chế bánh cóc xác định) và hybrid post-quantum key exchanges (trao đổi khóa hậu lượng tử kiểu lai).
