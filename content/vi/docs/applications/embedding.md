---
title: "Nhúng I2P vào Ứng dụng của Bạn"
description: "Hướng dẫn thực tiễn cập nhật để tích hợp I2P router vào ứng dụng của bạn một cách có trách nhiệm"
slug: "embedding"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

Tích hợp I2P vào ứng dụng của bạn là một cách mạnh mẽ để thu hút người dùng—nhưng chỉ khi router được cấu hình một cách có trách nhiệm.

## 1. Phối hợp với các nhóm Router

- Liên hệ với các nhà phát triển **Java I2P** và **i2pd** trước khi tích hợp. Họ có thể xem xét các cài đặt mặc định của bạn và chỉ ra các vấn đề tương thích.
- Chọn router phù hợp với stack của bạn:
  - **Java/Scala** → Java I2P
  - **C/C++** → i2pd
  - **Các ngôn ngữ khác** → tích hợp một router và kết nối bằng [SAM v3](/docs/api/samv3/) hoặc [I2CP](/docs/specs/i2cp/)
- Xác minh các điều khoản phân phối lại cho các tệp nhị phân router và các phụ thuộc (Java runtime, ICU, v.v.).

## 2. Cấu hình Mặc định Được Khuyến nghị

Hướng tới "đóng góp nhiều hơn mức tiêu thụ". Các cài đặt mặc định hiện đại ưu tiên sức khhoẻ và sự ổn định của mạng lưới.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Setting</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Recommended Default (2025)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Bandwidth share</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">80% for participating tunnels </td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Tunnel quantities</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2pd: 3 inbound / 3 outbound; Java I2P: 2 inbound / 2 outbound. </td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Signature &amp; encryption</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Use Ed25519 (<code>SIGNATURE_TYPE=7</code>) and advertise ECIES-X25519 + ElGamal (<code>i2cp.leaseSetEncType=4,0</code>).</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Client protocols</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Use SAM v3 or I2CP.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">API listeners</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Bind SAM/I2CP to <code>127.0.0.1</code> only. Disable if not needed.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">UI toggles</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Expose bandwidth controls, logs, and an opt-in checkbox for participating tunnels.</td>
    </tr>
  </tbody>
</table>
### Các Tunnel Tham Gia Vẫn Là Yếu Tố Quan Trọng

**Không** vô hiệu hóa các tunnel tham gia.

1. Các router không chuyển tiếp hoạt động kém hiệu quả hơn.
2. Mạng lưới phụ thuộc vào việc chia sẻ băng thông tự nguyện.
3. Cover traffic (lưu lượng được chuyển tiếp) cải thiện tính ẩn danh.

**Yêu cầu tối thiểu chính thức:** - Băng thông chia sẻ: ≥ 12 KB/s   - Tự động tham gia floodfill: ≥ 128 KB/s   - Khuyến nghị: 2 tunnel vào / 2 tunnel ra (mặc định của Java I2P)

## 3. Tính bền vững và Reseeding (làm mới dữ liệu)

Các thư mục trạng thái lâu dài (`netDb/`, profiles, certificates) phải được giữ nguyên giữa các lần chạy.

Không có tính năng lưu trữ lâu dài, người dùng của bạn sẽ kích hoạt reseed mỗi lần khởi động—làm giảm hiệu suất và tăng tải trên các máy chủ reseed.

Nếu không thể duy trì dữ liệu lâu dài (ví dụ: container hoặc cài đặt tạm thời):

1. Đóng gói **1.000–2.000 router info** trong trình cài đặt.  
2. Vận hành một hoặc nhiều máy chủ reseed tùy chỉnh để giảm tải cho các máy chủ công cộng.

Các biến cấu hình: - Thư mục gốc: `i2p.dir.base` - Thư mục cấu hình: `i2p.dir.config` - Bao gồm `certificates/` cho việc reseeding.

## 4. Bảo mật và Rủi ro Tiết lộ

- Giữ router console (`127.0.0.1:7657`) chỉ truy cập cục bộ.
- Sử dụng HTTPS nếu cần công khai giao diện người dùng ra bên ngoài.
- Vô hiệu hóa SAM/I2CP bên ngoài trừ khi thực sự cần thiết.
- Xem xét các plugin đi kèm—chỉ tích hợp những gì ứng dụng của bạn hỗ trợ.
- Luôn bao gồm xác thực cho quyền truy cập console từ xa.

**Tính năng bảo mật được giới thiệu từ phiên bản 2.5.0:** - Cách ly NetDB giữa các ứng dụng (2.4.0+)   - Giảm thiểu DoS và danh sách chặn Tor (2.5.1)   - Khả năng chống thăm dò NTCP2 (2.9.0)   - Cải tiến lựa chọn floodfill router (2.6.0+)

## 5. Các API được hỗ trợ (2025)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">API</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Status</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>SAM v3 (3.3)</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">✅ Active</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Recommended bridge for non-Java apps.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>I2CP</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">✅ Active</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Stable protocol core, used internally by Java I2P.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>I2PControl</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">✅ Active</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">JSON-RPC API; plugin maintained.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>BOB</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">⚠️ Deprecated</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Removed from Java I2P since 1.7.0; use SAM v3 instead.</td>
    </tr>
  </tbody>
</table>
Tất cả tài liệu chính thức được đặt tại `/docs/api/` — đường dẫn cũ `/spec/samv3/` **không** tồn tại.

## 6. Mạng và Cổng

Các cổng mặc định thông thường: - 4444 – HTTP Proxy   - 4445 – HTTPS Proxy   - 7654 – I2CP   - 7656 – SAM Bridge   - 7657 – Router Console   - 7658 – Trang web I2P cục bộ   - 6668 – IRC Proxy   - 9000–31000 – Cổng router ngẫu nhiên (UDP/TCP inbound)

Router chọn một cổng đầu vào ngẫu nhiên khi chạy lần đầu. Chuyển tiếp cổng giúp cải thiện hiệu suất, nhưng UPnP có thể tự động xử lý việc này.

## 7. Các Thay Đổi Hiện Đại (2024–2025)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Change</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Status</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Details</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>SSU1 Transport</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Removed</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">SSU2 is now the exclusive UDP transport.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>I2P-over-Tor</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Blocked</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Since 2.6.0 (July 2024).</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Datagram2/3</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Added</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Authenticated, repliable datagram formats (2.9.0).</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>LeaseSet service records</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Added</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Enables service discovery (Proposal 167).</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Tunnel build parameters</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Improved</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Adaptive congestion handling (2.9.0+).</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Post-quantum crypto</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Introduced (beta)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ML-KEM hybrid ratchet, opt-in from 2.10.0.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Java 17 requirement</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Announced</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Becomes mandatory in 2.11.0 (early 2026).</td>
    </tr>
  </tbody>
</table>
## 8. Trải nghiệm người dùng và Kiểm thử

- Truyền đạt I2P làm gì và tại sao băng thông được chia sẻ.
- Cung cấp chẩn đoán router (băng thông, tunnel, trạng thái reseed).
- Kiểm tra các gói trên Windows, macOS và Linux (bao gồm cả RAM thấp).
- Xác minh khả năng tương tác với cả peer **Java I2P** và **i2pd**.
- Kiểm tra khả năng phục hồi sau khi mất kết nối mạng và thoát không an toàn.

## 9. Tài Nguyên Cộng Đồng

- Diễn đàn: [i2pforum.net](https://i2pforum.net) hoặc `http://i2pforum.i2p` bên trong I2P.  
- Mã nguồn: [i2pgit.org/I2P_Developers/i2p.i2p](https://i2pgit.org/I2P_Developers/i2p.i2p).  
- IRC (mạng Irc2P): `#i2p-dev`, `#i2pd`.  
  - `#i2papps` chưa xác minh; có thể không tồn tại.  
  - Làm rõ mạng nào (Irc2P hay ilita.i2p) lưu trữ kênh của bạn.

Nhúng một cách có trách nhiệm có nghĩa là cân bằng giữa trải nghiệm người dùng, hiệu suất và đóng góp cho mạng lưới. Sử dụng các giá trị mặc định này, duy trì đồng bộ với các nhà bảo trì router và kiểm tra dưới tải thực tế trước khi phát hành.
