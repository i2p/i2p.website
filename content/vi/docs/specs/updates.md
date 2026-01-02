---
title: "Đặc tả cập nhật phần mềm"
description: "Cơ chế cập nhật được ký an toàn và cấu trúc nguồn cấp cho các router I2P"
slug: "updates"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## Tổng quan

Routers tự động kiểm tra cập nhật bằng cách truy vấn định kỳ một nguồn cấp tin đã được ký số, được phân phối qua mạng I2P. Khi có phiên bản mới được thông báo, router tải về một tệp lưu trữ cập nhật được ký số (`.su3`) và chuẩn bị sẵn cho việc cài đặt.   Hệ thống này đảm bảo việc phân phối các bản phát hành chính thức theo cách **được xác thực, chống giả mạo**, và **đa kênh**.

Kể từ I2P 2.10.0, hệ thống cập nhật sử dụng: - **RSA-4096 / SHA-512** cho chữ ký - **định dạng vùng chứa SU3** (thay thế SUD/SU2 kiểu cũ) - **Các mirror dự phòng:** HTTP trong mạng, HTTPS trên clearnet (mạng Internet công khai), và BitTorrent

---

## 1. Nguồn cấp tin

Các router thăm dò nguồn cấp Atom đã được ký cứ vài giờ một lần để phát hiện phiên bản mới và khuyến cáo bảo mật.   Nguồn cấp được ký và phân phối dưới dạng tệp `.su3`, có thể bao gồm:

- `<i2p:version>` — số phiên bản mới  
- `<i2p:minVersion>` — phiên bản router tối thiểu được hỗ trợ  
- `<i2p:minJavaVersion>` — môi trường chạy Java tối thiểu bắt buộc  
- `<i2p:update>` — liệt kê nhiều mirror tải xuống (I2P, HTTPS, torrent)  
- `<i2p:revocations>` — dữ liệu thu hồi chứng chỉ  
- `<i2p:blocklist>` — danh sách chặn ở cấp mạng dành cho các peer (nút ngang hàng) bị xâm phạm

### Phân phối nguồn cấp dữ liệu

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Channel</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>I2P HTTP (eepsite)</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Primary update source</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Private, resilient</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Clearnet HTTPS</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Fallback mirror</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Public fallback</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>BitTorrent magnet</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Distributed channel</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reduces mirror load</td>
    </tr>
  </tbody>
</table>
Các router ưu tiên nguồn cấp I2P nhưng có thể chuyển sang clearnet hoặc phân phối qua torrent nếu cần.

---

## 2. Định dạng tệp

### SU3 (Tiêu chuẩn hiện hành)

Được giới thiệu trong phiên bản 0.9.9, SU3 đã thay thế các định dạng SUD và SU2 cũ. Mỗi tệp bao gồm phần đầu (header), phần nội dung (payload), và chữ ký ở cuối.

**Cấu trúc tiêu đề** <table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">   <thead>

    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
    </tr>
</thead>   <tbody>

    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Magic</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>"I2Psu3"</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Format Version</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>0</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Signature Type</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">e.g., <code>0x000B</code> (RSA-SHA512-4096)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Signature Length</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>512 bytes</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Version String</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Router version</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Signer ID</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Certificate name</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Content Type</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1 = router update, 3 = reseed, 4 = news feed</td>
    </tr>
</tbody> </table>

**Các bước xác minh chữ ký** 1. Phân tích cú pháp header và xác định thuật toán chữ ký.   2. Xác minh giá trị băm và chữ ký bằng chứng chỉ của người ký được lưu trữ.   3. Xác nhận chứng chỉ của người ký chưa bị thu hồi.   4. So sánh chuỗi phiên bản nhúng với siêu dữ liệu của payload (nội dung tải).

Routers đi kèm với các chứng chỉ của người ký đáng tin cậy (hiện tại là **zzz** và **str4d**) và từ chối mọi nguồn chưa được ký hoặc đã bị thu hồi.

### SU2 (Lỗi thời)

- Đã dùng phần mở rộng `.su2` với các tệp JAR nén bằng Pack200 (định dạng nén của Java).  
- Đã bị gỡ bỏ sau khi Java 14 đánh dấu Pack200 là lỗi thời (JEP 367).  
- Đã bị vô hiệu hóa kể từ I2P 0.9.48+; hiện đã được thay thế hoàn toàn bằng nén ZIP.

### SUD (cũ)

- Định dạng ZIP được ký bằng DSA-SHA1 đời đầu (trước 0.9.9).  
- Không có ID người ký hoặc phần đầu (header), tính toàn vẹn hạn chế.  
- Đã bị thay thế do mật mã yếu và thiếu cơ chế bắt buộc phiên bản.

---

## 3. Quy trình cập nhật

### 3.1 Xác minh header

Các router chỉ tải **SU3 header** để xác minh chuỗi phiên bản trước khi tải xuống các tệp đầy đủ. Điều này giúp tránh lãng phí băng thông vào các mirror cũ (máy chủ bản sao) hoặc các phiên bản lỗi thời.

### 3.2 Tải xuống đầy đủ

Sau khi xác minh header, router tải xuống tệp `.su3` đầy đủ từ: - Các mirror eepsite trong mạng (ưu tiên)   - Các mirror HTTPS clearnet (mạng công khai) (dự phòng)   - BitTorrent (phân phối tùy chọn có hỗ trợ từ các nút ngang hàng)

Quá trình tải xuống sử dụng các client HTTP I2PTunnel tiêu chuẩn, có cơ chế thử lại, xử lý hết thời gian chờ, và chuyển sang mirror dự phòng.

### 3.3 Xác minh chữ ký

Mỗi tệp đã tải xuống sẽ trải qua: - **Kiểm tra chữ ký:** Xác minh RSA-4096/SHA512   - **Khớp phiên bản:** Kiểm tra phiên bản phần đầu (header) so với phần tải (payload)   - **Ngăn chặn hạ cấp phiên bản:** Đảm bảo bản cập nhật mới hơn bản đã cài đặt

Các tệp không hợp lệ hoặc không khớp được loại bỏ ngay lập tức.

### 3.4 Chuẩn bị cài đặt

Sau khi xác minh: 1. Giải nén nội dung ZIP vào thư mục tạm   2. Xóa các tệp được liệt kê trong `deletelist.txt`   3. Thay thế các native libraries (thư viện gốc) nếu có bao gồm `lib/jbigi.jar`   4. Sao chép các chứng chỉ của bên ký vào `~/.i2p/certificates/`   5. Chuyển bản cập nhật thành `i2pupdate.zip` để áp dụng ở lần khởi động lại tiếp theo

Bản cập nhật sẽ được cài đặt tự động vào lần khởi động tiếp theo hoặc khi tùy chọn “Cài đặt bản cập nhật ngay” được kích hoạt thủ công.

---

## 4. Quản lý tệp

### deletelist.txt

Một danh sách văn bản thuần liệt kê các tệp lỗi thời cần được xóa trước khi giải nén nội dung mới.

**Quy tắc:** - Mỗi dòng một đường dẫn (chỉ chấp nhận đường dẫn tương đối) - Các dòng bắt đầu bằng `#` bị bỏ qua - `..` và đường dẫn tuyệt đối bị từ chối

### Thư viện gốc

Để ngăn các tệp nhị phân gốc bị lỗi thời hoặc không khớp: - Nếu `lib/jbigi.jar` tồn tại, các tệp `.so` hoặc `.dll` cũ sẽ bị xóa   - Đảm bảo các thư viện dành riêng cho nền tảng được trích xuất mới

---

## 5. Quản lý chứng chỉ

Các router có thể nhận **các chứng chỉ ký mới** thông qua các bản cập nhật hoặc các thông báo thu hồi trên nguồn tin tức.

- Các tệp `.crt` mới được sao chép vào thư mục chứng chỉ.  
- Các chứng chỉ đã bị thu hồi được xóa trước các lần xác minh tiếp theo.  
- Hỗ trợ xoay vòng khóa mà không cần sự can thiệp thủ công của người dùng.

Tất cả các bản cập nhật được ký ngoại tuyến bằng **air-gapped signing systems** (hệ thống ký số cách ly mạng).   Các khóa riêng không bao giờ được lưu trữ trên các máy chủ build.

---

## 6. Hướng dẫn dành cho nhà phát triển

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Topic</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Details</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Signing</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Use RSA-4096 (SHA-512) via <code>apps/jetty/news</code> SU3 tooling.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Mirror Policy</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">I2P eepsite preferred, clearnet HTTPS fallback, torrent optional.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Testing</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Validate updates from prior releases, across all OS platforms.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Version Enforcement</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>minVersion</code> prevents incompatible upgrades.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Certificate Rotation</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Distribute new certs in updates and revocation lists.</td>
    </tr>
  </tbody>
</table>
Các bản phát hành trong tương lai sẽ khám phá việc tích hợp chữ ký hậu lượng tử (xem Đề xuất 169) và các bản dựng có thể tái lập.

---

## 7. Tổng quan về bảo mật

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Threat</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Mitigation</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Tampering</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Cryptographic signature (RSA-4096/SHA512)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Key Compromise</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Feed-based certificate revocation</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Downgrade Attack</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Version comparison enforcement</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Mirror Hijack</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Signature verification, multiple mirrors</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>DoS</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Fallback to alternate mirrors/torrents</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>MITM</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">HTTPS transport + signature-level integrity</td>
    </tr>
  </tbody>
</table>
---

## 8. Phiên bản hóa

- Router: **2.10.0 (API 0.9.67)**  
- Phiên bản ngữ nghĩa với `Major.Minor.Patch`.  
- Cơ chế bắt buộc phiên bản tối thiểu ngăn chặn các nâng cấp không an toàn.  
- Java được hỗ trợ: **Java 8–17**. Trong tương lai, 2.11.0+ sẽ yêu cầu Java 17+.

---
