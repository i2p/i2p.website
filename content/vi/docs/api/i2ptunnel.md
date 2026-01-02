---
title: "I2PTunnel"
description: "Công cụ để giao tiếp với và cung cấp dịch vụ trên I2P"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## Tổng quan

I2PTunnel là một thành phần cốt lõi của I2P dùng để giao tiếp và cung cấp dịch vụ trên mạng I2P. Nó cho phép các ứng dụng dựa trên TCP và phát trực tuyến phương tiện hoạt động ẩn danh thông qua trừu tượng hóa tunnel. Điểm đến của tunnel có thể được xác định bằng [hostname](/docs/overview/naming), [Base32](/docs/overview/naming#base32), hoặc một destination key đầy đủ.

Mỗi tunnel đã thiết lập sẽ lắng nghe cục bộ (ví dụ: `localhost:port`) và kết nối nội bộ đến các điểm đến I2P. Để lưu trữ một dịch vụ, hãy tạo một tunnel trỏ đến IP và cổng mong muốn. Một khóa đích I2P tương ứng sẽ được tạo ra, cho phép dịch vụ có thể truy cập toàn cầu trong mạng I2P. Giao diện web I2PTunnel có sẵn tại [I2P Router Tunnel Manager](http://localhost:7657/i2ptunnel/).

---

## Dịch vụ Mặc định

### Tunnel máy chủ

- **I2P Webserver** – Một tunnel tới máy chủ web Jetty tại [localhost:7658](http://localhost:7658) để dễ dàng lưu trữ trên I2P.  
  - **Unix:** `$HOME/.i2p/eepsite/docroot`  
  - **Windows:** `%LOCALAPPDATA%\I2P\I2P Site\docroot` → `C:\Users\<username>\AppData\Local\I2P\I2P Site\docroot`

### Tunnel client

- **I2P HTTP Proxy** – `localhost:4444` – Dùng để duyệt web I2P và Internet thông qua outproxies (proxy đầu ra).  
- **I2P HTTPS Proxy** – `localhost:4445` – Phiên bản bảo mật của HTTP proxy.  
- **Irc2P** – `localhost:6668` – Tunnel mạng IRC ẩn danh mặc định.  
- **Git SSH (gitssh.idk.i2p)** – `localhost:7670` – Client tunnel cho truy cập SSH kho lưu trữ.  
- **Postman SMTP** – `localhost:7659` – Client tunnel cho thư đi.  
- **Postman POP3** – `localhost:7660` – Client tunnel cho thư đến.

> Lưu ý: Chỉ có I2P Webserver là **server tunnel** mặc định; tất cả các tunnel khác đều là client tunnel kết nối đến các dịch vụ I2P bên ngoài.

---

## Cấu hình

Đặc tả cấu hình I2PTunnel được ghi chép tại [/spec/configuration](/docs/specs/configuration/).

---

## Chế độ Client

### Tiêu chuẩn

Mở một cổng TCP cục bộ kết nối đến một dịch vụ trên một destination I2P. Hỗ trợ nhiều destination được phân tách bằng dấu phẩy để đảm bảo dự phòng.

### HTTP

Một tunnel proxy cho các yêu cầu HTTP/HTTPS. Hỗ trợ outproxy cục bộ và từ xa, loại bỏ header, bộ nhớ đệm, xác thực và nén trong suốt.

**Bảo vệ riêng tư:**   - Loại bỏ các header: `Accept-*`, `Referer`, `Via`, `From`   - Thay thế host header bằng các địa chỉ đích Base32   - Thực thi việc loại bỏ hop-by-hop tuân thủ RFC   - Thêm hỗ trợ giải nén trong suốt   - Cung cấp các trang lỗi nội bộ và phản hồi đã được bản địa hóa

**Hành vi nén:**   - Các yêu cầu có thể sử dụng header tùy chỉnh `X-Accept-Encoding: x-i2p-gzip`   - Các phản hồi với `Content-Encoding: x-i2p-gzip` được giải nén một cách minh bạch   - Việc nén được đánh giá dựa trên loại MIME và độ dài phản hồi để tối ưu hiệu suất

**Tính bền vững (mới từ phiên bản 2.5.0):**   HTTP Keepalive và kết nối bền vững hiện đã được hỗ trợ cho các dịch vụ lưu trữ trên I2P thông qua Hidden Services Manager. Điều này giảm độ trễ và chi phí kết nối nhưng chưa cho phép socket bền vững tuân thủ đầy đủ RFC 2616 trên tất cả các hop.

**Pipelining:**   Vẫn không được hỗ trợ và không cần thiết; các trình duyệt hiện đại đã loại bỏ tính năng này.

**Hành vi User-Agent:**   - **Outproxy:** Sử dụng User-Agent Firefox ESR hiện tại.   - **Internal:** `MYOB/6.66 (AN/ON)` để duy trì tính nhất quán về ẩn danh.

### Ứng dụng IRC

Kết nối tới các máy chủ IRC dựa trên I2P. Cho phép một tập hợp con các lệnh an toàn trong khi lọc các định danh để bảo vệ quyền riêng tư.

### SOCKS 4/4a/5

Cung cấp khả năng proxy SOCKS cho các kết nối TCP. UDP vẫn chưa được triển khai trong Java I2P (chỉ có trong i2pd).

### CONNECT

Triển khai tạo tunnel HTTP `CONNECT` cho các kết nối SSL/TLS.

### Streamr

Cho phép truyền tải dạng UDP thông qua đóng gói dựa trên TCP. Hỗ trợ truyền tải media khi kết hợp với tunnel máy chủ Streamr tương ứng.

![Sơ đồ I2PTunnel Streamr](/images/I2PTunnel-streamr.png)

---

## Chế độ Máy chủ

### Máy chủ Tiêu chuẩn

Tạo một destination TCP được ánh xạ tới một địa chỉ IP:cổng cục bộ.

### Máy chủ HTTP

Tạo một destination kết nối với máy chủ web cục bộ. Hỗ trợ nén (`x-i2p-gzip`), loại bỏ header và bảo vệ chống DDoS. Hiện được hưởng lợi từ **hỗ trợ kết nối liên tục** (v2.5.0+) và **tối ưu hóa thread pooling** (v2.7.0–2.9.0).

### HTTP Hai chiều

**Không còn được khuyến nghị** – Vẫn hoạt động nhưng không được khuyến khích sử dụng. Hoạt động như cả HTTP server và client mà không có outproxying. Chủ yếu được sử dụng cho các bài kiểm tra loopback chẩn đoán.

### Máy chủ IRC

Tạo một đích đã lọc cho các dịch vụ IRC, truyền khóa đích của client dưới dạng tên máy chủ.

### Máy chủ Streamr

Kết hợp với tunnel client Streamr để xử lý các luồng dữ liệu kiểu UDP qua I2P.

---

## Tính năng mới (2.4.0–2.10.0)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Feature</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Introduced</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Summary</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Keepalive/Persistent Connections</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.5.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">HTTP tunnels now support persistent sockets for I2P-hosted services, improving performance.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Thread Pooling Optimization</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.7.0-2.9.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reduced CPU overhead and latency by improving thread management.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Post-Quantum Encryption (ML-KEM)</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.10.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Optional hybrid X25519+ML-KEM encryption to resist future quantum attacks.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>NetDB Segmentation</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.4.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Isolates I2PTunnel contexts for improved security and privacy.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>SSU1 Removal / SSU2 Adoption</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.4.0-2.6.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Upgraded transport layer; transparent to users.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>I2P-over-Tor Blocking</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.6.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Prevents inefficient and unstable I2P-over-Tor routing.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Browser Proxy (Proposal 166)</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.7.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Introduced identity-aware proxy mode; details pending confirmation.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Java 17 Requirement (upcoming)</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.11.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Future release will require Java 17+.</td>
    </tr>
  </tbody>
</table>
---

## Tính năng Bảo mật

- **Loại bỏ header** để đảm bảo ẩn danh (Accept, Referer, From, Via)
- **Ngẫu nhiên hóa User-Agent** tùy thuộc vào in/outproxy
- **Giới hạn tốc độ POST** và **bảo vệ Slowloris**
- **Điều tiết kết nối** trong hệ thống con streaming
- **Xử lý tắc nghẽn mạng** ở lớp tunnel
- **Cô lập NetDB** ngăn chặn rò rỉ thông tin giữa các ứng dụng

---

## Chi tiết Kỹ thuật

- Kích thước khóa đích mặc định: 516 bytes (có thể vượt quá đối với chứng chỉ LS2 mở rộng)  
- Địa chỉ Base32: `{52–56+ ký tự}.b32.i2p`  
- Server tunnel vẫn tương thích với cả Java I2P và i2pd  
- Tính năng không được khuyến nghị: chỉ `httpbidirserver`; không có gì bị loại bỏ kể từ 0.9.59  
- Đã xác minh cổng mặc định và thư mục gốc tài liệu chính xác cho tất cả các nền tảng

---

## Tóm tắt

I2PTunnel vẫn là xương sống cho việc tích hợp ứng dụng với I2P. Từ phiên bản 0.9.59 đến 2.10.0, nó đã có thêm hỗ trợ kết nối liên tục, mã hóa post-quantum và cải tiến lớn về luồng xử lý. Hầu hết các cấu hình vẫn tương thích, nhưng các nhà phát triển nên kiểm tra thiết lập của mình để đảm bảo tuân thủ các mặc định về truyền tải và bảo mật hiện đại.
