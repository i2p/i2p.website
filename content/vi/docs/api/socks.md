---
title: "SOCKS Proxy"
description: "Sử dụng tunnel SOCKS của I2P một cách an toàn (cập nhật cho phiên bản 2.10.0)"
slug: "socks"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

> **Cảnh báo:** Tunnel SOCKS chuyển tiếp các payload ứng dụng mà không làm sạch chúng. Nhiều giao thức có thể làm rò rỉ IP, hostname hoặc các định danh khác. Chỉ sử dụng SOCKS với phần mềm mà bạn đã kiểm tra về tính ẩn danh.

---

## 1. Tổng quan

I2P cung cấp hỗ trợ proxy **SOCKS 4, 4a và 5** cho các kết nối đi ra thông qua **I2PTunnel client**. Nó cho phép các ứng dụng tiêu chuẩn truy cập các đích đến I2P nhưng **không thể truy cập clearnet** (mạng Internet thông thường). **Không có SOCKS outproxy**, và toàn bộ lưu lượng vẫn ở trong mạng I2P.

### Tóm tắt Triển khai

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Parameter</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Java I2P</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">i2pd</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Default Port</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">User-defined</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>127.0.0.1:4447</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Supported SOCKS Versions</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4, 4a, 5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4, 4a, 5</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">UDP Mode</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Stubbed (non-functional)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Stubbed (non-functional)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Persistent Keys</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">✅ Since 0.9.9</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">✅</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Shared Client Tunnels</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Supported</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Supported</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Outproxy Support</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">❌ None</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">❌ None</td>
    </tr>
  </tbody>
</table>
**Các loại địa chỉ được hỗ trợ:** - Tên miền `.i2p` (các mục trong sổ địa chỉ) - Mã băm Base32 (`.b32.i2p`) - Không hỗ trợ Base64 hoặc clearnet

---

## 2. Rủi ro Bảo mật và Hạn chế

### Rò rỉ ở Tầng Ứng dụng

SOCKS hoạt động ở tầng dưới tầng ứng dụng và không thể làm sạch các giao thức. Nhiều ứng dụng client (ví dụ: trình duyệt, IRC, email) bao gồm metadata có thể tiết lộ địa chỉ IP, tên máy chủ hoặc thông tin chi tiết hệ thống của bạn.

Các rò rỉ thông tin phổ biến bao gồm: - Địa chỉ IP trong header email hoặc phản hồi IRC CTCP   - Tên thật/tên người dùng trong dữ liệu giao thức   - Chuỗi user-agent chứa dấu vết hệ điều hành   - Truy vấn DNS bên ngoài   - WebRTC và dữ liệu thu thập từ trình duyệt

**I2P không thể ngăn chặn những rò rỉ này**—chúng xảy ra ở tầng trên tunnel layer. Chỉ sử dụng SOCKS cho **các client đã được kiểm toán** được thiết kế cho tính ẩn danh.

### Danh Tính Tunnel Dùng Chung

Nếu nhiều ứng dụng chia sẻ cùng một SOCKS tunnel, chúng sẽ dùng chung một định danh I2P destination. Điều này cho phép việc liên kết hoặc định danh dấu vết qua các dịch vụ khác nhau.

**Giảm thiểu:** Sử dụng **tunnel không chia sẻ** cho mỗi ứng dụng và bật **khóa lưu trữ lâu dài** để duy trì danh tính mã hóa nhất quán qua các lần khởi động lại.

### Chế độ UDP đã bị loại bỏ

Hỗ trợ UDP trong SOCKS5 chưa được triển khai. Giao thức quảng bá khả năng UDP, nhưng các lệnh gọi bị bỏ qua. Hãy sử dụng các client chỉ dùng TCP.

### Không có Outproxy theo Thiết kế

Khác với Tor, I2P **không** cung cấp outproxy (proxy ra mạng thường) dựa trên SOCKS. Các nỗ lực truy cập địa chỉ IP bên ngoài sẽ thất bại hoặc làm lộ danh tính. Sử dụng proxy HTTP hoặc HTTPS nếu cần outproxy.

---

## 3. Bối cảnh lịch sử

Các nhà phát triển từ lâu đã không khuyến khích sử dụng SOCKS cho mục đích ẩn danh. Từ các cuộc thảo luận nội bộ của nhà phát triển và năm 2004 [Meeting 81](/vi/blog/2004/03/16/i2p-dev-meeting-march-16-2004/) và [Meeting 82](/vi/blog/2004/03/23/i2p-dev-meeting-march-23-2004/):

> "Chuyển tiếp lưu lượng tùy ý là không an toàn, và với vai trò là những nhà phát triển phần mềm ẩn danh, chúng ta có trách nhiệm phải đặt sự an toàn của người dùng cuối lên hàng đầu trong tâm trí."

Hỗ trợ SOCKS được bao gồm để tương thích nhưng không được khuyến nghị cho môi trường sản xuất. Gần như mọi ứng dụng internet đều rò rỉ metadata nhạy cảm không phù hợp với định tuyến ẩn danh.

---

## 4. Cấu hình

### Java I2P

1. Mở [I2PTunnel Manager](http://127.0.0.1:7657/i2ptunnel)  
2. Tạo một client tunnel mới có kiểu **"SOCKS 4/4a/5"**  
3. Cấu hình các tùy chọn:  
   - Cổng local (bất kỳ cổng khả dụng nào)  
   - Shared client: *tắt* để có danh tính riêng biệt cho mỗi ứng dụng  
   - Persistent key: *bật* để giảm sự tương quan khóa  
4. Khởi động tunnel

### i2pd

i2pd bao gồm hỗ trợ SOCKS5được kích hoạt mặc định tại `127.0.0.1:4447`. Cấu hình trong `i2pd.conf` dưới phần `[SOCKSProxy]` cho phép bạn điều chỉnh cổng, máy chủ và các tham số tunnel.

---

## 5. Lịch trình Phát triển

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Version</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Change</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Date</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.7.1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Initial SOCKS 4/4a/5 support</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2010</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.9</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Added persistent keying</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2013</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1.7.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">BOB API deprecated and removed</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2022</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.6.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">I2P-over-Tor blocked to improve network health</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2024</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.10.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Post-quantum hybrid encryption introduced</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2025</td>
    </tr>
  </tbody>
</table>
Bản thân module SOCKS không có bản cập nhật giao thức lớn nào kể từ năm 2013, nhưng ngăn xếp tunnel xung quanh đã nhận được các cải tiến về hiệu suất và mật mã.

---

## 6. Các Phương Án Thay Thế Được Khuyến Nghị

Đối với bất kỳ ứng dụng **sản xuất**, **hướng công chúng**, hoặc **quan trọng về bảo mật** nào, hãy sử dụng một trong các API I2P chính thức thay vì SOCKS:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">API</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Recommended For</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>SAM v3 (3.3)</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Simple Anonymous Messaging API</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Cross-language apps needing socket-like I/O</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Streaming Library</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">TCP-like sockets for Java</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Native Java integrations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>I2CP</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Low-level router communication</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Custom protocols, router-level integration</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>BOB</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated (removed 2022)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Legacy only; migrate to SAM</td>
    </tr>
  </tbody>
</table>
Các API này cung cấp khả năng cách ly đích đến phù hợp, kiểm soát danh tính mật mã và hiệu suất định tuyến tốt hơn.

---

## 7. OnionCat / GarliCat

OnionCat hỗ trợ I2P thông qua chế độ GarliCat (`fd60:db4d:ddb5::/48` dải IPv6). Vẫn hoạt động nhưng hạn chế phát triển kể từ năm 2019.

**Lưu ý khi sử dụng:** - Yêu cầu cấu hình thủ công `.oc.b32.i2p` trong SusiDNS   - Cần gán địa chỉ IPv6 tĩnh   - Không được hỗ trợ chính thức bởi dự án I2P

Chỉ được khuyến nghị cho các thiết lập VPN-over-I2P nâng cao.

---

## 8. Các Phương Pháp Hay Nhất

Nếu bạn phải sử dụng SOCKS: 1. Tạo các tunnel riêng biệt cho từng ứng dụng.   2. Vô hiệu hóa chế độ client dùng chung.   3. Bật tính năng khóa liên tục.   4. Buộc phân giải DNS qua SOCKS5.   5. Kiểm tra hành vi giao thức để phát hiện rò rỉ.   6. Tránh kết nối clearnet.   7. Giám sát lưu lượng mạng để phát hiện rò rỉ.

---

## 9. Tóm tắt Kỹ thuật

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Parameter</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Supported SOCKS Versions</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4, 4a, 5</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Transport</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">TCP only</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>UDP Support</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Stubbed (non-functional)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Clearnet Access</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Not supported</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Default Ports</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Java I2P: user-set; i2pd: <code>127.0.0.1:4447</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Persistent Keying</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Supported since 0.9.9</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Shared Tunnels</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Supported (discouraged)</td>
    </tr>
  </tbody>
</table>
---

## 10. Kết luận

SOCKS proxy trong I2P cung cấp khả năng tương thích cơ bản với các ứng dụng TCP hiện có nhưng **không được thiết kế để đảm bảo tính ẩn danh mạnh mẽ**. Nó chỉ nên được sử dụng cho các môi trường thử nghiệm có kiểm soát và được kiểm tra kỹ lưỡng.

> Đối với các triển khai nghiêm túc, hãy chuyển sang **SAM v3** hoặc **Streaming API**. Các API này cô lập danh tính ứng dụng, sử dụng mật mã hiện đại và nhận được phát triển liên tục.

---

### Tài Nguyên Bổ Sung

- [Tài liệu SOCKS Chính thức](/docs/api/socks/)  
- [Đặc tả SAMv3](/docs/api/samv3/)  
- [Tài liệu Thư viện Streaming](/docs/specs/streaming/)  
- [Tài liệu Tham khảo I2PTunnel](/docs/specs/implementation/)  
- [Tài liệu Nhà phát triển I2P](https://i2pgit.org/I2P_Developers/i2p.i2p)  
- [Diễn đàn Cộng đồng](https://i2pforum.net)
