---
title: "Giao thức mạng I2P (I2NP)"
description: "Các định dạng thông điệp từ router đến router, mức độ ưu tiên và giới hạn kích thước bên trong I2P."
slug: "i2np"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## Tổng quan

Giao thức Mạng I2P (I2NP) xác định cách các routers trao đổi thông điệp, lựa chọn các phương thức truyền tải và trộn lưu lượng đồng thời bảo toàn tính ẩn danh. Nó hoạt động ở giữa **I2CP** (API máy khách) và các giao thức truyền tải (**NTCP2** và **SSU2**).

I2NP là lớp nằm trên các giao thức truyền tải của I2P. Đây là một giao thức router-to-router được dùng cho: - Tra cứu và phản hồi cơ sở dữ liệu mạng - Tạo tunnels - Các thông điệp dữ liệu được mã hóa của router và máy khách

Các thông điệp I2NP có thể được gửi theo kiểu điểm-tới-điểm tới một router khác, hoặc được gửi ẩn danh thông qua các tunnels đến router đó.

Routers xếp hàng các công việc gửi ra dựa trên các mức ưu tiên cục bộ. Các số ưu tiên cao hơn được xử lý trước. Bất kỳ mức ưu tiên nào vượt quá mức ưu tiên dữ liệu tunnel tiêu chuẩn (400) đều được coi là khẩn cấp.

### Các giao thức truyền tải hiện tại

I2P hiện sử dụng **NTCP2** (TCP) và **SSU2** (UDP) cho cả IPv4 và IPv6. Cả hai phương thức truyền tải đều sử dụng: - trao đổi khóa **X25519** (khung giao thức Noise) - mã hóa xác thực **ChaCha20/Poly1305** (AEAD) - hàm băm **SHA-256**

**Đã loại bỏ các giao thức truyền tải cũ:** - NTCP (TCP ban đầu) đã được loại bỏ khỏi router Java trong bản phát hành 0.9.50 (Tháng 5 năm 2021) - SSU v1 (UDP ban đầu) đã được loại bỏ khỏi router Java trong bản phát hành 2.4.0 (Tháng 12 năm 2023) - SSU v1 đã được loại bỏ khỏi i2pd trong bản phát hành 2.44.0 (Tháng 11 năm 2022)

Kể từ năm 2025, mạng đã chuyển đổi hoàn toàn sang các giao thức truyền tải dựa trên Noise (khung giao thức mật mã), và hoàn toàn không hỗ trợ các giao thức truyền tải kiểu cũ.

---

## Hệ thống đánh số phiên bản

**QUAN TRỌNG:** I2P sử dụng một cơ chế đánh số phiên bản kép cần được hiểu rõ:

### Phiên bản phát hành (dành cho người dùng)

Đây là các phiên bản mà người dùng thấy và tải xuống: - 0.9.50 (Tháng 5 năm 2021) - Bản phát hành 0.9.x cuối cùng - **1.5.0** (Tháng 8 năm 2021) - Bản phát hành 1.x đầu tiên - 1.6.0, 1.7.0, 1.8.0, 1.9.0 (trong giai đoạn 2021-2022) - **2.0.0** (Tháng 11 năm 2022) - Bản phát hành 2.x đầu tiên - 2.1.0 đến 2.9.0 (trong giai đoạn 2023-2025) - **2.10.0** (ngày 8 tháng 9 năm 2025) - Bản phát hành hiện tại

### Phiên bản API (Tương thích giao thức)

Đây là các số phiên bản nội bộ được công bố trong trường "router.version" trong các thuộc tính RouterInfo: - 0.9.50 (Tháng 5 năm 2021) - **0.9.51** (Tháng 8 năm 2021) - Phiên bản API cho bản phát hành 1.5.0 - 0.9.52 đến 0.9.66 (tiếp tục qua các bản phát hành 2.x) - **0.9.67** (Tháng 9 năm 2025) - Phiên bản API cho bản phát hành 2.10.0

**Điểm chính:** KHÔNG có bản phát hành nào được đánh số từ 0.9.51 đến 0.9.67. Các số này chỉ tồn tại như các định danh phiên bản API. I2P đã nhảy từ bản phát hành 0.9.50 trực tiếp lên 1.5.0.

### Bảng ánh xạ phiên bản

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Release Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">API Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Date</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Key Features</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.50</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.50</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">May 2021</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Last 0.9.x release, removed NTCP1</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1.5.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.51</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">August 2021</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Short tunnel build messages (218 bytes)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1.6.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.52</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">November 2021</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Various improvements</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1.7.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.53</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">January 2022</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Performance enhancements</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1.8.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.54</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">May 2022</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">SSU2 introduced</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1.9.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.55</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">August 2022</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">SSU2 improvements</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.0.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.56</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">November 2022</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">SSU2 enabled by default</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.1.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.57</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">January 2023</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Stability improvements</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.2.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.58</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">March 2023</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>ElGamal routers deprecated</strong></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.3.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.59</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">May 2023</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Various improvements</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.4.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.61</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">December 2023</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Removed SSU1 support</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.5.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.62</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">February 2024</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Performance improvements</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.6.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.63</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">May 2024</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Network optimizations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.7.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.64</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">October 2024</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Post-quantum preparation work</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.8.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.65</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">February 2025</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Tunnel bandwidth parameters</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.9.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.66</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">June 2025</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet service records</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.10.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">September 2025</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Post-quantum hybrid cryptography (beta)</td>
    </tr>
  </tbody>
</table>
**Sắp tới:** Bản phát hành 2.11.0 (dự kiến tháng 12 năm 2025) sẽ yêu cầu Java 17 trở lên và bật mật mã hậu lượng tử theo mặc định.

---

## Phiên bản giao thức

Tất cả các router phải công bố phiên bản giao thức I2NP của mình trong trường "router.version" trong các thuộc tính của RouterInfo (cấu trúc thông tin về router). Trường phiên bản này là phiên bản API, cho biết mức độ hỗ trợ đối với các tính năng khác nhau của giao thức I2NP, và không nhất thiết trùng với phiên bản router thực tế.

Nếu các router thay thế (không dùng Java) muốn công bố bất kỳ thông tin phiên bản nào về bản triển khai router thực tế, họ phải thực hiện điều đó trong một thuộc tính khác. Các phiên bản khác với những phiên bản liệt kê bên dưới đều được phép. Khả năng hỗ trợ sẽ được xác định thông qua so sánh số; ví dụ, 0.9.13 ngụ ý hỗ trợ các tính năng của 0.9.12.

**Lưu ý:** Thuộc tính "coreVersion" không còn được công bố trong thông tin router và trước đây cũng chưa từng được sử dụng để xác định phiên bản giao thức I2NP.

### Tóm tắt tính năng theo phiên bản API

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">API Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Required I2NP Features</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Post-quantum hybrid cryptography (MLKEM ratchet) support (beta), UDP tracker support</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.66</td><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet2 service record options (see proposal 167)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.65</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Tunnel build bandwidth parameters (see proposal 168)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.59</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Minimum peers will build tunnels through (as of 0.9.63), minimum floodfill peers will send DSM to (as of 0.9.63)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.58</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Minimum peers will build tunnels through (as of 0.9.62), <strong>ElGamal routers deprecated</strong></td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.55</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SSU2 transport support (if published in router info)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.51</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Short tunnel build messages for ECIES-X25519 routers, minimum peers will build tunnels through (as of 0.9.58), minimum floodfill peers will send DSM to (as of 0.9.58)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.49</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Garlic messages to ECIES-X25519 routers</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.48</td><td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES-X25519 routers, ECIES-X25519 build request/response records</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.46</td><td style="border:1px solid var(--color-border); padding:0.5rem;">DatabaseLookup flag bit 4 for AEAD reply</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.44</td><td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES-X25519 keys in LeaseSet2</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.40</td><td style="border:1px solid var(--color-border); padding:0.5rem;">MetaLeaseSet may be sent in a DSM</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.39</td><td style="border:1px solid var(--color-border); padding:0.5rem;">EncryptedLeaseSet may be sent in a DSM, RedDSA_SHA512_Ed25519 signature type supported</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.38</td><td style="border:1px solid var(--color-border); padding:0.5rem;">DSM type bits 3-0 now contain the type; LeaseSet2 may be sent in a DSM</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.36</td><td style="border:1px solid var(--color-border); padding:0.5rem;">NTCP2 transport support (if published in router info), minimum peers will build tunnels through (as of 0.9.46)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.28</td><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA signature types disallowed, minimum floodfill peers will send DSM to (as of 0.9.34)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.18</td><td style="border:1px solid var(--color-border); padding:0.5rem;">DSM type bits 7-1 ignored</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.16</td><td style="border:1px solid var(--color-border); padding:0.5rem;">RI key certs / ECDSA and EdDSA signature types, DLM lookup types (flag bits 3-2), minimum version compatible with the current network</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.15</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Destination/LeaseSet key certificates with EdDSA Ed25519 signature type (if floodfill)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Destination/LeaseSet key certificates with ECDSA P-256, P-384, and P-521 signature types (if floodfill); non-zero expiration allowed in RouterAddress</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.7</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Encrypted DSM/DSRM replies supported (DLM flag bit 1) for floodfill routers</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.6</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Non-zero DLM flag bits 7-1 allowed</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Requires zero expiration in RouterAddress</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Supports up to 16 leases in a DSM LeaseSet store (previously 6)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.7.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">VTBM and VTBRM message support</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.7.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Floodfill supports encrypted DSM stores</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.6.1.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBM and TBRM messages introduced; minimum version compatible with the current network</td></tr>
  </tbody>
</table>
**Lưu ý:** Cũng có các tính năng liên quan đến lớp truyền tải và các vấn đề tương thích. Xem tài liệu về cơ chế truyền tải NTCP2 và SSU2 để biết chi tiết.

---

## Phần đầu thông điệp

I2NP sử dụng một cấu trúc tiêu đề 16 byte ở mức logic, trong khi các giao thức truyền tải hiện đại (NTCP2 và SSU2) sử dụng tiêu đề 9 byte rút gọn, loại bỏ các trường kích thước và kiểm tra tổng (checksum) dư thừa. Các trường vẫn tương đương về mặt khái niệm.

### So sánh định dạng tiêu đề

**Định dạng tiêu chuẩn (16 byte):**

Được sử dụng trong cơ chế truyền tải NTCP cũ và khi các thông điệp I2NP được nhúng bên trong các thông điệp khác (TunnelData, TunnelGateway, GarlicClove).

```
Bytes 0-15:
+----+----+----+----+----+----+----+----+
|type|      msg_id       |  expiration
+----+----+----+----+----+----+----+----+
                         |  size   |chks|
+----+----+----+----+----+----+----+----+

type :: Integer (1 byte)
        Identifies the message type (see message type table)

msg_id :: Integer (4 bytes)
          Uniquely identifies this message (for some time at least)
          Usually a locally-generated random number, but for outgoing
          tunnel build messages may be derived from the incoming message

expiration :: Date (8 bytes)
              Unix timestamp in milliseconds when this message expires

size :: Integer (2 bytes)
        Length of the payload (0 to ~61.2 KB for tunnel messages)

chks :: Integer (1 byte)
        SHA256 hash of payload truncated to first byte
        Deprecated - NTCP2/SSU2 use ChaCha20/Poly1305 AEAD for integrity
```
**Định dạng ngắn cho SSU (đã lỗi thời, 5 byte):**

```
+----+----+----+----+----+
|type| short_expiration  |
+----+----+----+----+----+

type :: Integer (1 byte)
short_expiration :: Integer (4 bytes, seconds since epoch)
```
**Định dạng ngắn cho NTCP2, SSU2 và ECIES-Ratchet Garlic Cloves (các nhánh thông điệp trong mô hình garlic) (9 byte):**

Được sử dụng trong các transport hiện đại và trong các thông điệp garlic được mã hóa bằng ECIES.

```
+----+----+----+----+----+----+----+----+
|type|      msg_id       | short_expira-
+----+----+----+----+----+----+----+----+
 tion|
+----+

type :: Integer (1 byte)
msg_id :: Integer (4 bytes)
short_expiration :: Integer (4 bytes, seconds since epoch, unsigned)
```
### Chi tiết các trường tiêu đề

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Bytes</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Type</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Identifies the message class (0&ndash;255, see message types below)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Unique ID</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Locally unique identifier for matching replies</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Expiration</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">8 (standard) / 4 (short)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Timestamp when the message expires. Routers discard expired messages. Short format uses seconds since epoch (unsigned, wraps February 7, 2106)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Payload Length</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Size in bytes (0 to ~61.2 KB for tunnel messages). NTCP2 and SSU2 encode this in their frame headers</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Checksum</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated. First byte of SHA-256 hash of the payload. NTCP2/SSU2 use ChaCha20/Poly1305 AEAD for integrity</td>
    </tr>
  </tbody>
</table>
### Ghi chú triển khai

- Khi được truyền qua SSU (đã lỗi thời), chỉ bao gồm trường loại và thời điểm hết hạn 4 byte
- Khi được truyền qua NTCP2 hoặc SSU2, sử dụng định dạng rút gọn 9 byte
- Phần đầu 16 byte tiêu chuẩn là bắt buộc cho các thông điệp I2NP được chứa trong các thông điệp khác (Data, TunnelData, TunnelGateway, GarlicClove)
- Kể từ bản phát hành 0.8.12, việc xác minh checksum (mã kiểm tra) bị tắt tại một số điểm trong ngăn xếp giao thức để tăng hiệu suất, nhưng việc tạo checksum vẫn là bắt buộc để đảm bảo khả năng tương thích
- Thời điểm hết hạn rút gọn là số không dấu và sẽ tràn quay vòng vào ngày 7 tháng 2 năm 2106. Sau thời điểm đó, phải cộng thêm một độ lệch để có thời gian chính xác
- Để tương thích với các phiên bản cũ, luôn tạo checksum ngay cả khi chúng có thể không được xác minh

---

## Giới hạn kích thước

Các thông điệp Tunnel phân mảnh các tải trọng I2NP thành các mảnh có kích thước cố định: - **Mảnh đầu tiên:** xấp xỉ 956 byte - **Các mảnh tiếp theo:** xấp xỉ 996 byte mỗi mảnh - **Số mảnh tối đa:** 64 (đánh số 0-63) - **Tải trọng tối đa:** xấp xỉ 61,200 byte (61.2 KB)

**Tính toán:** 956 + (63 × 996) = 63,704 byte tối đa theo lý thuyết, với giới hạn thực tế khoảng 61,200 byte do phần overhead (chi phí quản trị).

### Bối cảnh lịch sử

Các giao thức truyền tải cũ có giới hạn kích thước khung nghiêm ngặt hơn: - NTCP: khung 16 KB - SSU: khung khoảng 32 KB

NTCP2 hỗ trợ các khung dữ liệu khoảng 65 KB, nhưng giới hạn phân mảnh tunnel vẫn áp dụng.

### Các cân nhắc về dữ liệu ứng dụng

Garlic messages (thông điệp garlic) có thể đóng gói LeaseSets, Session Tags (thẻ phiên), hoặc các biến thể LeaseSet2 được mã hóa, làm giảm dung lượng dành cho dữ liệu payload.

**Khuyến nghị:** Các datagram (gói tin không kết nối) nên giữ ≤ 10 KB để đảm bảo chuyển phát đáng tin cậy. Các thông điệp tiến gần tới giới hạn 61 KB có thể gặp:
- Độ trễ tăng do phân mảnh và tái lắp ráp
- Xác suất thất bại khi chuyển phát cao hơn
- Dễ bị phân tích lưu lượng hơn

### Chi tiết kỹ thuật về phân mảnh

Mỗi thông điệp tunnel có kích thước chính xác 1,024 byte (1 KB) và bao gồm: - tunnel ID 4 byte - vector khởi tạo (IV) 16 byte - 1,004 byte dữ liệu được mã hóa

Bên trong dữ liệu đã mã hóa, các thông điệp tunnel mang các thông điệp I2NP bị phân mảnh với fragment header (tiêu đề mảnh) cho biết: - Số thứ tự mảnh (0-63) - Đây là mảnh đầu tiên hay mảnh theo sau - ID của thông điệp hoàn chỉnh để tái lắp ráp

Mảnh đầu tiên bao gồm toàn bộ phần đầu (header) của thông điệp I2NP (16 byte), để lại khoảng 956 byte cho phần tải (payload). Các mảnh tiếp theo không bao gồm phần đầu thông điệp, nhờ đó mỗi mảnh có khoảng 996 byte phần tải.

---

## Các loại thông điệp phổ biến

Routers sử dụng loại thông điệp và mức độ ưu tiên để lập lịch các tác vụ gửi đi. Các giá trị ưu tiên cao hơn được xử lý trước. Các giá trị dưới đây khớp với mặc định hiện tại của Java I2P (tính đến phiên bản API 0.9.67).

**Lưu ý:** Các mức ưu tiên phụ thuộc vào cách triển khai. Để biết các giá trị ưu tiên chính thức, hãy tham khảo tài liệu của lớp `OutNetMessage` trong mã nguồn Java I2P.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Message</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Priority</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Typical Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Purpose</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>DatabaseStore</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">460</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Varies (LeaseSet ≈ 898&nbsp;B, RouterInfo ≈ 2&ndash;4&nbsp;KB compressed)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Publishes RouterInfo or LeaseSet objects. Supports LeaseSet2, EncryptedLeaseSet, and MetaLeaseSet</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>DatabaseLookup</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">500</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Varies</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Queries the network database for RouterInfo or LeaseSet entries</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>DatabaseSearchReply</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">300</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">≈161&nbsp;B (5 hashes)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Returns candidate floodfill router hashes (typically 3&ndash;16 hashes, recommended maximum 16)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>DeliveryStatus</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">10</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Varies</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">12&nbsp;B</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Receipts for tunnel tests or acknowledgements inside GarlicMessages</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>GarlicMessage</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">11</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">100 (local)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Varies</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Bundles multiple message cloves (e.g., DataMessage, LeaseSets). Supports ElGamal/AES (deprecated) and ECIES-X25519-AEAD-Ratchet encryption</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>TunnelData</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">18</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">400</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1,028&nbsp;B (fixed)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Encrypted tunnel message exchanged between hops. Contains a 4-byte tunnel ID, 16-byte IV, and 1,004 bytes of encrypted data</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>TunnelGateway</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">19</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">300&ndash;400</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Varies</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Encapsulates messages at the tunnel gateway before fragmentation</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>DataMessage</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">20</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">425</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">4&ndash;62&nbsp;KB</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Carries end-to-end garlic payloads (application traffic)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>TunnelBuild</strong> <em>(deprecated)</em></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">21</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">500</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">4,224&nbsp;B</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Requests tunnel participation from routers (8 × 528-byte records). Replaced by VariableTunnelBuild for ECIES</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>TunnelBuildReply</strong> <em>(deprecated)</em></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">22</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">300</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">4,224&nbsp;B</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Replies to TunnelBuild with accept/reject status per hop</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>VariableTunnelBuild</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">23</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">500</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1,057&ndash;4,225&nbsp;B</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Variable-length tunnel build for ElGamal or ECIES-X25519 routers (1&ndash;8 records, API 0.9.12+)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>VariableTunnelBuildReply</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">24</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">300</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1,057&ndash;4,225&nbsp;B</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Replies to VariableTunnelBuild</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>ShortTunnelBuild</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">25</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">500</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">873&ndash;1,745&nbsp;B</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Short tunnel build messages for ECIES-X25519 routers only (1&ndash;8 × 218-byte records, API 0.9.51+)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>OutboundTunnelBuildReply</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">26</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">300</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">873&ndash;1,745&nbsp;B</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Sent from outbound endpoint to originator for ECIES-X25519 routers (API 0.9.51+)</td>
    </tr>
  </tbody>
</table>
**Các kiểu thông điệp dành riêng:** - Kiểu 0: Dành riêng - Các kiểu 4-9: Dành cho sử dụng trong tương lai - Các kiểu 12-17: Dành cho sử dụng trong tương lai - Các kiểu 224-254: Dành cho thông điệp thử nghiệm - Kiểu 255: Dành cho mở rộng trong tương lai

### Ghi chú về kiểu thông điệp

- Các thông điệp mặt phẳng điều khiển (DatabaseLookup, TunnelBuild, v.v.) thường đi qua **exploratory tunnels** (tunnel thăm dò), không phải client tunnels (tunnel khách), cho phép ưu tiên độc lập
- Các giá trị ưu tiên chỉ mang tính xấp xỉ và có thể khác nhau tùy theo cách triển khai
- TunnelBuild (21) và TunnelBuildReply (22) đã lỗi thời nhưng vẫn được triển khai để tương thích với các tunnel rất dài (>8 bước nhảy)
- Mức ưu tiên dữ liệu tunnel chuẩn là 400; mọi giá trị cao hơn mức này được coi là khẩn
- Độ dài tunnel điển hình trong mạng hiện nay là 3-4 bước nhảy, vì vậy phần lớn các lần dựng tunnel sử dụng ShortTunnelBuild (bản ghi 218 byte) hoặc VariableTunnelBuild (bản ghi 528 byte)

---

## Mã hóa và bao gói thông điệp

Các router thường đóng gói các thông điệp I2NP trước khi truyền, tạo ra nhiều lớp mã hóa. Một DeliveryStatus message (thông điệp trạng thái giao nhận) có thể: 1. Được bọc trong GarlicMessage (thông điệp Garlic) (được mã hóa) 2. Ở bên trong một DataMessage (thông điệp dữ liệu) 3. Nằm trong một TunnelData message (thông điệp dữ liệu tunnel) (được mã hóa lần nữa)

Mỗi nút trung gian chỉ giải mã lớp của riêng nó; đích đến cuối cùng sẽ tiết lộ nội dung ở lớp trong cùng.

### Các thuật toán mã hóa

**Cũ (Đang dần bị loại bỏ):** - ElGamal/AES + SessionTags (thẻ phiên) - ElGamal-2048 cho mã hóa bất đối xứng - AES-256 cho mã hóa đối xứng - thẻ phiên 32 byte

**Hiện tại (Tiêu chuẩn kể từ API 0.9.48):** - ECIES-X25519 + ChaCha20/Poly1305 AEAD với forward secrecy (bí mật chuyển tiếp) dạng ratcheting - Khung giao thức Noise (Noise_IK_25519_ChaChaPoly_SHA256 cho các đích) - Thẻ phiên 8 byte (giảm từ 32 byte) - Thuật toán Signal Double Ratchet cho forward secrecy - Được giới thiệu trong phiên bản API 0.9.46 (2020) - Bắt buộc đối với tất cả router kể từ phiên bản API 0.9.58 (2023)

**Tương lai (Beta kể từ 2.10.0):** - Mật mã lai hậu lượng tử sử dụng MLKEM (ML-KEM-768) kết hợp với X25519 - ratchet lai (cơ chế cập nhật khóa dần) kết hợp thỏa thuận khóa cổ điển và hậu lượng tử - Tương thích ngược với ECIES-X25519 - Sẽ trở thành mặc định trong bản phát hành 2.11.0 (Tháng 12 năm 2025)

### Loại bỏ dần Router ElGamal

**LƯU Ý QUAN TRỌNG:** Các router ElGamal đã bị ngừng khuyến nghị sử dụng (deprecated) kể từ phiên bản API 0.9.58 (bản phát hành 2.2.0, tháng 3 năm 2023). Vì phiên bản floodfill tối thiểu được khuyến nghị để truy vấn hiện là 0.9.58, các triển khai không cần thực hiện mã hóa cho các router floodfill ElGamal.

**Tuy nhiên:** Các đích ElGamal vẫn được hỗ trợ để đảm bảo khả năng tương thích ngược. Các ứng dụng khách sử dụng mã hóa ElGamal vẫn có thể giao tiếp thông qua các router ECIES.

### Chi tiết về ECIES-X25519-AEAD-Ratchet (cơ chế mật mã kết hợp ECIES, X25519, AEAD và ratchet)

Đây là kiểu mật mã 4 trong đặc tả mật mã của I2P. Nó cung cấp:

**Tính năng chính:** - Bí mật chuyển tiếp thông qua ratcheting (cơ chế bánh cóc; khóa mới cho mỗi tin nhắn) - Giảm dung lượng lưu trữ session tag (thẻ phiên) (8 byte so với 32 byte) - Nhiều loại phiên (Phiên Mới, Phiên Hiện Có, Một Lần) - Dựa trên giao thức Noise Noise_IK_25519_ChaChaPoly_SHA256 - Tích hợp với thuật toán Double Ratchet (bánh cóc kép) của Signal

**Nguyên thủy mật mã:** - X25519 cho thỏa thuận khóa Diffie-Hellman - ChaCha20 cho mã hóa luồng - Poly1305 cho xác thực thông điệp (AEAD) - SHA-256 cho băm - HKDF cho dẫn xuất khóa

**Quản lý phiên:** - Phiên mới: Kết nối ban đầu sử dụng static destination key (khóa đích tĩnh) - Phiên hiện có: Các thông điệp tiếp theo sử dụng session tags (thẻ phiên) - Phiên dùng một lần: Phiên chỉ một thông điệp để giảm overhead (chi phí quản trị)

Xem [Đặc tả ECIES](/docs/specs/ecies/) và [Đề xuất 144](/proposals/144-ecies-x25519-aead-ratchet/) để biết toàn bộ chi tiết kỹ thuật.

---

## Các cấu trúc chung

Các cấu trúc sau đây là các thành phần của nhiều thông điệp I2NP. Chúng không phải là các thông điệp hoàn chỉnh.

### BuildRequestRecord (bản ghi yêu cầu xây dựng) (ElGamal)

**ĐÃ LỖI THỜI.** Chỉ được sử dụng trong mạng hiện tại khi một tunnel chứa router ElGamal. Xem [Tạo Tunnel ECIES](/docs/specs/implementation/) để biết định dạng hiện đại.

**Mục đích:** Một bản ghi thuộc tập nhiều bản ghi dùng để yêu cầu tạo một chặng trong tunnel.

**Định dạng:**

Được mã hóa bằng ElGamal và AES (tổng cộng 528 byte):

```
+----+----+----+----+----+----+----+----+
| encrypted data (528 bytes)            |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
```
Cấu trúc được mã hóa bằng ElGamal (528 byte):

```
+----+----+----+----+----+----+----+----+
| toPeer (16 bytes)                     |
+----+----+----+----+----+----+----+----+
| ElGamal encrypted data (512 bytes)    |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

toPeer :: First 16 bytes of SHA-256 hash of peer's RouterIdentity

encrypted_data :: ElGamal-2048 encrypted (bytes 1-256 and 258-513
                  of the 514-byte ElGamal block, with padding bytes
                  at positions 0 and 257 removed)
```
Cấu trúc bản rõ (222 byte trước khi mã hóa):

```
+----+----+----+----+----+----+----+----+
| receive_tunnel (4) | our_ident (32)   |
+----+----+----+----+                   +
|                                       |
+                   +----+----+----+----+
|                   | next_tunnel (4)   |
+----+----+----+----+----+----+----+----+
| next_ident (32 bytes)                 |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| layer_key (32 bytes)                  |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| iv_key (32 bytes)                     |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| reply_key (32 bytes)                  |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| reply_iv (16 bytes)                   |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|flag| request_time (4) | send_msg_id  |
+----+----+----+----+----+----+----+----+
     (4)                | padding (29)  |
+----+----+----+----+----+              +
|                                       |
+                             +----+----+
|                             |
+----+----+----+----+----+----+

receive_tunnel :: TunnelId (4 bytes, nonzero)
our_ident :: Hash (32 bytes)
next_tunnel :: TunnelId (4 bytes, nonzero)
next_ident :: Hash (32 bytes)
layer_key :: SessionKey (32 bytes)
iv_key :: SessionKey (32 bytes)
reply_key :: SessionKey (32 bytes)
reply_iv :: 16 bytes
flag :: Integer (1 byte)
request_time :: Integer (4 bytes, hours since epoch = time / 3600)
send_message_id :: Integer (4 bytes)
padding :: 29 bytes random data
```
**Ghi chú:** - Mã hóa ElGamal-2048 tạo ra một khối 514 byte, nhưng hai byte đệm (tại các vị trí 0 và 257) được loại bỏ, kết quả còn 512 byte - Xem [Đặc tả Tạo Tunnel](/docs/specs/implementation/) để biết chi tiết về các trường - Mã nguồn: `net.i2p.data.i2np.BuildRequestRecord` - Hằng số: `EncryptedBuildRecord.RECORD_SIZE = 528`

### BuildRequestRecord (bản ghi yêu cầu xây dựng) (ECIES-X25519 Long)

Đối với các router ECIES-X25519, được giới thiệu từ phiên bản API 0.9.48. Sử dụng 528 byte để đảm bảo tương thích ngược với các tunnels hỗn hợp.

**Định dạng:**

```
+----+----+----+----+----+----+----+----+
| toPeer (16 bytes)                     |
+----+----+----+----+----+----+----+----+
| ephemeral_key (32 bytes)              |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| ChaCha20 encrypted data (464 bytes)   |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Poly1305 MAC (16 bytes)               |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+

toPeer :: First 16 bytes of SHA-256 hash of peer's RouterIdentity
ephemeral_key :: X25519 ephemeral public key (32 bytes)
encrypted_data :: ChaCha20 encrypted (464 bytes)
mac :: Poly1305 message authentication code (16 bytes)
```
**Tổng kích thước:** 528 byte (giống như ElGamal để tương thích)

Xem [ECIES Tunnel Creation](/docs/specs/implementation/) để biết về cấu trúc cleartext (dữ liệu không mã hóa) và các chi tiết mã hóa.

### BuildRequestRecord (ECIES-X25519 phiên bản rút gọn)

Chỉ dành cho các router ECIES-X25519, kể từ phiên bản API 0.9.51 (bản phát hành 1.5.0). Đây là định dạng tiêu chuẩn hiện tại.

**Định dạng:**

```
+----+----+----+----+----+----+----+----+
| toPeer (16 bytes)                     |
+----+----+----+----+----+----+----+----+
| ephemeral_key (32 bytes)              |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| ChaCha20 encrypted data (154 bytes)   |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Poly1305 MAC (16 bytes)               |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+

toPeer :: First 16 bytes of SHA-256 hash of peer's RouterIdentity
ephemeral_key :: X25519 ephemeral public key (32 bytes)
encrypted_data :: ChaCha20 encrypted (154 bytes)
mac :: Poly1305 message authentication code (16 bytes)
```
**Tổng kích thước:** 218 byte (giảm 59% so với 528 byte)

**Khác biệt chính:** Bản ghi ngắn dẫn xuất tất cả các khóa thông qua HKDF (key derivation function - hàm dẫn xuất khóa) thay vì đưa chúng vào bản ghi một cách tường minh. Bao gồm: - Khóa lớp (cho mã hóa tunnel) - Khóa IV (cho mã hóa tunnel) - Khóa phản hồi (cho build reply - phản hồi dựng tunnel) - IV phản hồi (cho build reply)

Tất cả các khóa được dẫn xuất bằng HKDF mechanism (cơ chế HKDF) của Noise protocol (giao thức Noise), dựa trên bí mật chung thu được từ X25519 key exchange (trao đổi khóa X25519).

**Lợi ích:** - 4 bản ghi ngắn vừa trong một thông điệp tunnel (873 byte) - Dựng tunnel bằng 3 thông điệp thay vì các thông điệp riêng cho từng bản ghi - Giảm băng thông và độ trễ - Các thuộc tính bảo mật giống như định dạng dài

Xem [Đề xuất 157](/proposals/157-new-tbm/) để biết lý do thiết kế và [ECIES Tunnel Creation](/docs/specs/implementation/) để xem đặc tả đầy đủ.

**Mã nguồn:** - `net.i2p.data.i2np.ShortEncryptedBuildRecord` - Hằng số: `ShortEncryptedBuildRecord.RECORD_SIZE = 218`

### BuildResponseRecord (ElGamal)

**KHÔNG CÒN ĐƯỢC KHUYẾN NGHỊ SỬ DỤNG.** Chỉ được sử dụng khi tunnel chứa một router ElGamal.

**Mục đích:** Một bản ghi trong một tập hợp gồm nhiều bản ghi chứa các phản hồi cho một yêu cầu xây dựng.

**Định dạng:**

Được mã hóa (528 byte, cùng kích thước với BuildRequestRecord (bản ghi yêu cầu xây dựng)):

```
bytes 0-527 :: AES-encrypted record
```
Cấu trúc không mã hóa:

```
+----+----+----+----+----+----+----+----+
| SHA-256 hash (32 bytes)               |
+                                       +
|        (hash of bytes 32-527)         |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| random data (495 bytes)               |
~                                       ~
|                                  |ret |
+----+----+----+----+----+----+----+----+

bytes 0-31 :: SHA-256 hash of bytes 32-527
bytes 32-526 :: Random data (could be used for congestion info)
byte 527 :: Reply code (0 = accept, 30 = reject)
```
**Mã phản hồi:** - `0` - Chấp nhận - `30` - Từ chối (vượt quá băng thông)

Xem [Tunnel Creation Specification](/docs/specs/implementation/) để biết chi tiết về trường phản hồi.

### BuildResponseRecord (ECIES-X25519)

Đối với routers ECIES-X25519, phiên bản API 0.9.48+. Có cùng kích thước với yêu cầu tương ứng (528 cho bản dài, 218 cho bản ngắn).

**Định dạng:**

Định dạng dài (528 byte):

```
+----+----+----+----+----+----+----+----+
| ChaCha20 encrypted data (512 bytes)   |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Poly1305 MAC (16 bytes)               |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
```
Định dạng ngắn (218 byte):

```
+----+----+----+----+----+----+----+----+
| ChaCha20 encrypted data (202 bytes)   |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Poly1305 MAC (16 bytes)               |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
```
**Cấu trúc bản rõ (cả hai định dạng):**

Chứa một cấu trúc ánh xạ (định dạng khóa-giá trị của I2P) với: - Mã trạng thái phản hồi (bắt buộc) - Tham số băng thông khả dụng ("b") (tùy chọn, được thêm trong API 0.9.65) - Các tham số tùy chọn khác cho các mở rộng trong tương lai

**Mã trạng thái phản hồi:** - `0` - Thành công - `30` - Từ chối: vượt quá giới hạn băng thông

Xem [ECIES Tunnel Creation](/docs/specs/implementation/) để biết đặc tả đầy đủ.

### GarlicClove (đơn vị thông điệp trong garlic encryption) (ElGamal/AES)

**CẢNH BÁO:** Đây là định dạng được dùng cho garlic cloves (các phần tử con trong thông điệp garlic) trong các garlic messages được mã hóa bằng ElGamal. Định dạng cho ECIES-AEAD-X25519-Ratchet garlic messages và garlic cloves khác biệt đáng kể. Xem [ECIES Specification](/docs/specs/ecies/) để biết định dạng hiện đại.

**Không còn được khuyến nghị cho routers (API 0.9.58+), nhưng vẫn được hỗ trợ cho các điểm đích.**

**Định dạng:**

Không mã hóa:

```
+----+----+----+----+----+----+----+----+
| Delivery Instructions (variable)      |
~                                       ~
+----+----+----+----+----+----+----+----+
| I2NP Message (variable)               |
~                                       ~
+----+----+----+----+----+----+----+----+
| Clove ID (4)  | Expiration (8)   |Cert|
+----+----+----+----+----+----+----+----+
                                    (3) |
+----+----+----+----+----+----+----+----+

Delivery Instructions :: Variable length (typically 1, 33, or 37 bytes)
I2NP Message :: Any I2NP message
Clove ID :: 4-byte Integer (random, checked for duplicates)
Expiration :: Date (8 bytes)
Certificate :: Always NULL (3 bytes total, all zeroes)
```
**Ghi chú:** - Clove (đơn vị tải trong GarlicMessage) không bao giờ bị phân mảnh - Khi bit đầu tiên của byte cờ Delivery Instructions là 0, clove không được mã hóa - Khi bit đầu tiên là 1, clove được mã hóa (tính năng chưa được triển khai) - Độ dài tối đa phụ thuộc vào tổng độ dài các clove và độ dài tối đa của GarlicMessage - Chứng chỉ có thể được dùng cho HashCash để "trả phí" cho định tuyến (khả năng trong tương lai) - Các thông điệp được dùng trong thực tế: DataMessage, DeliveryStatusMessage, DatabaseStoreMessage - GarlicMessage có thể chứa GarlicMessage (garlic lồng nhau), nhưng điều này không được dùng trong thực tế

Xem [Garlic Routing](/docs/overview/garlic-routing/) (định tuyến tỏi) để có cái nhìn tổng quan ở mức khái niệm.

### GarlicClove (ECIES-X25519-AEAD-Ratchet)

Dành cho routers và destinations (đích) ECIES-X25519, phiên bản API 0.9.46+. Đây là định dạng tiêu chuẩn hiện tại.

**KHÁC BIỆT QUAN TRỌNG:** ECIES garlic (dạng garlic dựa trên ECIES trong I2P) sử dụng một cấu trúc hoàn toàn khác, dựa trên các khối của giao thức Noise thay vì các cấu trúc clove (tiểu thông điệp con) tường minh.

**Định dạng:**

ECIES garlic messages (thông điệp kiểu garlic trong I2P) bao gồm một loạt các khối:

```
Block structure:
+----+----+----+----+----+----+----+----+
|type| length    | data ...
+----+----+----+----+----+-//-

type :: 1 byte block type
length :: 2 bytes block length
data :: variable length data
```
**Các loại khối:** - `0` - Khối Garlic Clove (tép tỏi; chứa một thông điệp I2NP) - `1` - Khối ngày-giờ (dấu thời gian) - `2` - Khối tùy chọn (tùy chọn chuyển phát) - `3` - Khối đệm - `254` - Khối kết thúc (chưa triển khai)

**Garlic Clove Block (khối tép tỏi trong I2P) (loại 0):**

```
+----+----+----+----+----+----+----+----+
|  0 | length    | Delivery Instructions |
+----+----+----+----+                    +
~                                       ~
+----+----+----+----+----+----+----+----+
| I2NP Message                          |
~                                       ~
+----+----+----+----+----+----+----+----+
| Clove ID (4)  | Expiration (4)        |
+----+----+----+----+----+----+----+----+
```
**Những khác biệt chính so với định dạng ElGamal:** - Sử dụng thời gian hết hạn 4 byte (giây kể từ epoch) thay vì Date 8 byte - Không có trường chứng chỉ - Được bao gói trong cấu trúc khối với kiểu và độ dài - Toàn bộ thông điệp được mã hóa bằng ChaCha20/Poly1305 AEAD - Quản lý phiên thông qua ratcheting (cơ chế tăng dần khóa một chiều)

Xem [Đặc tả ECIES](/docs/specs/ecies/) để biết toàn bộ chi tiết về khung giao thức Noise và các cấu trúc khối.

### Chỉ dẫn chuyển phát Garlic Clove (tép tỏi trong garlic encryption)

Định dạng này được dùng cho cả ElGamal và ECIES garlic cloves (các 'nhánh' trong mô hình garlic encryption). Nó chỉ rõ cách chuyển phát thông điệp được bao chứa bên trong.

**CẢNH BÁO NGHIÊM TRỌNG:** Đặc tả này chỉ áp dụng cho Delivery Instructions (chỉ dẫn phân phối) bên trong Garlic Cloves. "Delivery Instructions" cũng được dùng bên trong Tunnel Messages (các thông điệp trong tunnel), nơi định dạng khác biệt đáng kể. Xem [Đặc tả Tunnel Message](/docs/specs/implementation/) để biết Delivery Instructions cho tunnel. KHÔNG được nhầm lẫn hai định dạng này.

**Định dạng:**

Khóa phiên và độ trễ không được sử dụng và không bao giờ xuất hiện, vì vậy có ba độ dài khả dĩ: - 1 byte (LOCAL) - 33 byte (ROUTER và DESTINATION) - 37 byte (TUNNEL)

```
+----+----+----+----+----+----+----+----+
|flag|                                  |
+----+                                  +
|       Session Key (optional, 32)     |
+                                       +
|                                       |
+    +----+----+----+----+--------------+
|    |                                  |
+----+                                  +
|       To Hash (optional, 32)         |
+                                       +
|                                       |
+    +----+----+----+----+--------------+
|    | Tunnel ID (4, opt)| Delay (4, opt)|
+----+----+----+----+----+----+----+----+

flag :: 1 byte
        Bit order: 76543210
        bit 7: encrypted? (Unimplemented, always 0)
               If 1, a 32-byte encryption session key follows
        bits 6-5: delivery type
               0x0 = LOCAL (0)
               0x1 = DESTINATION (1)
               0x2 = ROUTER (2)
               0x3 = TUNNEL (3)
        bit 4: delay included? (Not fully implemented, always 0)
               If 1, four delay bytes are included
        bits 3-0: reserved, set to 0 for compatibility

Session Key :: 32 bytes (Optional, unimplemented)
               Present if encrypt flag bit is set

To Hash :: 32 bytes (Optional)
           Present if delivery type is DESTINATION, ROUTER, or TUNNEL
           - DESTINATION: SHA256 hash of the destination
           - ROUTER: SHA256 hash of the router identity
           - TUNNEL: SHA256 hash of the gateway router identity

Tunnel ID :: 4 bytes (Optional)
             Present if delivery type is TUNNEL
             The destination tunnel ID (nonzero)

Delay :: 4 bytes (Optional, unimplemented)
         Present if delay included flag is set
         Specifies delay in seconds
```
**Độ dài điển hình:** - Giao tới LOCAL: 1 byte (chỉ cờ) - Giao tới ROUTER / DESTINATION: 33 byte (cờ + giá trị băm) - Giao tới TUNNEL: 37 byte (cờ + giá trị băm + tunnel ID)

**Mô tả các kiểu chuyển giao:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Value</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">LOCAL</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Deliver to the local router (this router)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DESTINATION</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Deliver to a destination (client) identified by hash</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ROUTER</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Deliver to another router identified by hash</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">TUNNEL</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Deliver to a tunnel gateway router</td>
    </tr>
  </tbody>
</table>
**Ghi chú triển khai:** - Mã hóa khóa phiên chưa được triển khai và bit cờ luôn là 0 - Độ trễ chưa được triển khai đầy đủ và bit cờ luôn là 0 - Đối với chuyển phát TUNNEL, hàm băm xác định gateway router (router cổng) và tunnel ID chỉ ra tunnel vào nào - Đối với chuyển phát DESTINATION, hàm băm là SHA-256 của khóa công khai của đích - Đối với chuyển phát ROUTER, hàm băm là SHA-256 của định danh của router

---

## Các thông điệp I2NP

Đặc tả thông điệp hoàn chỉnh cho mọi loại thông điệp I2NP.

### Tóm tắt các loại thông điệp

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Message</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DatabaseStore</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.6.1.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DatabaseLookup</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.6.1.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DatabaseSearchReply</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.6.1.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DeliveryStatus</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">10</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.6.1.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Garlic</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">11</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.6.1.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">TunnelData</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">18</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.6.1.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">TunnelGateway</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">19</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.6.1.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Data</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">20</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.6.1.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">TunnelBuild</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">21</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.6.1.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">TunnelBuildReply</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">22</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.6.1.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">VariableTunnelBuild</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">23</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.7.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">VariableTunnelBuildReply</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">24</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.7.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ShortTunnelBuild</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">25</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.51</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">OutboundTunnelBuildReply</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">26</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.51</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
  </tbody>
</table>
**Dành riêng:** - Loại 0: Dành riêng - Các loại 4-9: Dành riêng cho sử dụng trong tương lai - Các loại 12-17: Dành riêng cho sử dụng trong tương lai - Các loại 224-254: Dành riêng cho các thông điệp thử nghiệm - Loại 255: Dành riêng cho mở rộng trong tương lai

---

### DatabaseStore (thông điệp lưu trữ cơ sở dữ liệu) (Loại 1)

**Mục đích:** Một lần lưu trữ cơ sở dữ liệu không được yêu cầu, hoặc phản hồi cho một thông điệp DatabaseLookup thành công.

**Nội dung:** Một LeaseSet, LeaseSet2, MetaLeaseSet hoặc EncryptedLeaseSet không nén, hoặc một RouterInfo được nén.

**Định dạng với token phản hồi:**

```
+----+----+----+----+----+----+----+----+
| SHA256 Hash as key (32 bytes)        |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|type| reply token (4)   | reply_tunnelId
+----+----+----+----+----+----+----+----+
     (4)               | reply gateway  |
+----+----+----+----+----+              +
|       SHA256 hash (32 bytes)          |
+                                       +
|                                       |
+                                  +----+
|                                  |
+----+----+----+----+----+----+----+
| data ...
+----+-//

key :: 32 bytes
       SHA256 hash (the "real" hash, not routing key)

type :: 1 byte
        Type identifier
        bit 0:
            0 = RouterInfo
            1 = LeaseSet or variants
        bits 3-1: (as of 0.9.38)
            0: RouterInfo or LeaseSet (types 0 or 1)
            1: LeaseSet2 (type 3)
            2: EncryptedLeaseSet (type 5)
            3: MetaLeaseSet (type 7)
            4-7: Unsupported, invalid
        bits 7-4:
            Reserved, set to 0

reply token :: 4 bytes
               If greater than zero, a DeliveryStatusMessage is
               requested with the Message ID set to the reply token
               A floodfill router is also expected to flood the data
               to the closest floodfill peers

reply_tunnelId :: 4 bytes (only if reply token > 0)
                  TunnelId of the inbound gateway of the tunnel
                  for the response
                  If 0, reply is sent directly to reply gateway

reply gateway :: 32 bytes (only if reply token > 0)
                 SHA256 hash of the RouterInfo
                 If reply_tunnelId is nonzero: inbound gateway router
                 If reply_tunnelId is zero: router to send reply to

data :: Variable length
        If type == 0: 2-byte Integer length + gzip-compressed RouterInfo
        If type == 1: Uncompressed LeaseSet
        If type == 3: Uncompressed LeaseSet2
        If type == 5: Uncompressed EncryptedLeaseSet
        If type == 7: Uncompressed MetaLeaseSet
```
**Định dạng với reply token == 0:**

```
+----+----+----+----+----+----+----+----+
| SHA256 Hash as key (32 bytes)        |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|type|         0         | data ...
+----+----+----+----+----+-//
```

**Mã nguồn:** - `net.i2p.data.i2np.DatabaseStoreMessage` - `net.i2p.data.RouterInfo` (cho cấu trúc RouterInfo — thông tin router) - `net.i2p.data.LeaseSet` (cho cấu trúc LeaseSet — tập hợp lease)

---

### DatabaseLookup (Tra cứu cơ sở dữ liệu, Loại 2)

**Mục đích:** Một yêu cầu để tra cứu một mục trong cơ sở dữ liệu mạng (netDb). Phản hồi có thể là DatabaseStore hoặc DatabaseSearchReply.

**Định dạng:**

```
+----+----+----+----+----+----+----+----+
| SHA256 hash as the key (32 bytes)    |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| SHA256 hash of the from router (32)  |
+    or reply tunnel gateway            +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|flag| reply_tunnelId (4)| size (2)|   |
+----+----+----+----+----+----+----+    +
| SHA256 of key1 to exclude (32 bytes) |
+                                       +
|                                       |
+                                  +----+
|                                  |    |
+----+----+----+----+----+----+----+    +
| SHA256 of key2 to exclude (32)       |
+                                       +
~                                       ~
|                                       |
+                                  +----+
|                                  |    |
+----+----+----+----+----+----+----+    +
|   Session key if reply encryption     |
+       requested (32 bytes)             +
|                                       |
+                                  +----+
|                                  |tags|
+----+----+----+----+----+----+----+----+
|   Session tags if reply encryption    |
+       requested (variable)             +
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

key :: 32 bytes
       SHA256 hash of the object to lookup

from :: 32 bytes
        If deliveryFlag == 0: SHA256 hash of RouterInfo (sender)
        If deliveryFlag == 1: SHA256 hash of reply tunnel gateway

flags :: 1 byte
         Bit order: 76543210
         bit 0: deliveryFlag
             0 = send reply directly
             1 = send reply to some tunnel
         bit 1: encryptionFlag
             Through 0.9.5: must be 0
             As of 0.9.6: ignored
             As of 0.9.7:
                 0 = send unencrypted reply
                 1 = send AES encrypted reply using key and tag
         bits 3-2: lookup type flags
             Through 0.9.5: must be 00
             As of 0.9.6: ignored
             As of 0.9.16:
                 00 = ANY (deprecated, use LS or RI as of 0.9.16)
                 01 = LS lookup (LeaseSet or variants)
                 10 = RI lookup (RouterInfo)
                 11 = exploration lookup (RouterInfo, non-floodfill)
         bit 4: ECIESFlag
             Before 0.9.46: ignored
             As of 0.9.46:
                 0 = send unencrypted or ElGamal reply
                 1 = send ChaCha/Poly encrypted reply using key
         bits 7-5:
             Reserved, set to 0

reply_tunnelId :: 4 bytes (only if deliveryFlag == 1)
                  TunnelId of the tunnel to send reply to (nonzero)

size :: 2 bytes
        Integer (valid range: 0-512)
        Number of peers to exclude from DatabaseSearchReply

excludedPeers :: $size SHA256 hashes of 32 bytes each
                 If lookup fails, exclude these peers from the reply
                 If includes a hash of all zeroes, the request is
                 exploratory (return non-floodfill routers only)

reply_key :: 32 bytes (conditional, see encryption modes below)
reply_tags :: 1 byte count + variable length tags (conditional)
```
**Chế độ mã hóa phản hồi:**

**LƯU Ý:** ElGamal routers không còn được khuyến nghị kể từ API 0.9.58. Vì phiên bản floodfill tối thiểu được khuyến nghị để truy vấn hiện là 0.9.58, các triển khai không cần thực hiện mã hóa cho ElGamal floodfill routers. Các điểm đến ElGamal vẫn được hỗ trợ.

Bit cờ 4 (ECIESFlag) được dùng cùng với bit 1 (encryptionFlag) để xác định chế độ mã hóa phản hồi:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Flag bits 4,1</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">From</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">To Router</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Reply</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">DH?</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0 0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Any</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Any</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">No encryption</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">n/a</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">No encryption</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0 1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ElG</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ElG</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">AES</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">As of 0.9.7, deprecated 0.9.58</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1 0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ElG</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">AEAD</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">As of 0.9.46, deprecated 0.9.58</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1 0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">AEAD</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">As of 0.9.49, current standard</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1 1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ElG</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">AES</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">TBD, future</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1 1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">AEAD</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">TBD, future</td>
    </tr>
  </tbody>
</table>
**Không mã hóa (cờ 0,0):**

reply_key, tags và reply_tags không có.

**ElG (ElGamal) sang ElG (cờ 0,1) - ĐÃ LỖI THỜI:**

Được hỗ trợ từ 0.9.7, bị đánh dấu là không khuyến nghị sử dụng (deprecated) từ 0.9.58.

```
reply_key :: 32 byte SessionKey (big-endian)
             CSRNG(32) random data

tags :: 1 byte Integer (1-32, typically 1)
        Number of reply tags that follow

reply_tags :: One or more 32-byte SessionTags
              Each is CSRNG(32) random data
```
**ECIES sang ElG (flags 1,0) - ĐÃ LỖI THỜI:**

Được hỗ trợ từ 0.9.46, không còn được khuyến nghị sử dụng từ 0.9.58.

```
reply_key :: 32 byte ECIES SessionKey (big-endian)
             CSRNG(32) random data

tags :: 1 byte Integer (required value: 1)
        Number of reply tags that follow

reply_tags :: One 8-byte ECIES SessionTag
              CSRNG(8) random data
```
Phản hồi là một thông điệp ECIES Existing Session (thông điệp Phiên hiện có của ECIES) như được định nghĩa trong [ECIES Specification](/docs/specs/ecies/):

```
+----+----+----+----+----+----+----+----+
| Session Tag (8 bytes)                 |
+----+----+----+----+----+----+----+----+
| ChaCha20 encrypted payload            |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Poly1305 MAC (16 bytes)               |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+

tag :: 8 byte reply_tag
k :: 32 byte session key (the reply_key)
n :: 0 (nonce)
ad :: The 8 byte reply_tag
payload :: Plaintext data (DSM or DSRM)
ciphertext = ENCRYPT(k, n, payload, ad)
```
**ECIES sang ECIES (flags 1,0) - TIÊU CHUẨN HIỆN HÀNH:**

Đích ECIES (mã hóa khóa công khai dựa trên đường cong elliptic) hoặc router gửi một yêu cầu tra cứu đến một router ECIES. Được hỗ trợ kể từ 0.9.49.

Cùng định dạng như "ECIES to ElG" ở trên. Việc mã hóa thông điệp tra cứu được đặc tả trong [ECIES Routers](/docs/specs/ecies/#routers). Người yêu cầu là ẩn danh.

**ECIES (Elliptic Curve Integrated Encryption Scheme - lược đồ mã hóa tích hợp đường cong elliptic) tới ECIES với DH (Diffie-Hellman - trao đổi khóa Diffie-Hellman) (cờ 1,1) - TƯƠNG LAI:**

Chưa được xác định đầy đủ. Xem [Đề xuất 156](/proposals/156-ecies-routers/).

**Ghi chú:** - Trước 0.9.16, khóa có thể thuộc về một RouterInfo hoặc LeaseSet (cùng không gian khóa, không có cờ để phân biệt) - Các phản hồi được mã hóa chỉ hữu ích khi phản hồi đi qua một tunnel - Số lượng thẻ đi kèm có thể lớn hơn một nếu các chiến lược tra cứu DHT (bảng băm phân tán) thay thế được triển khai - Khóa tra cứu và các khóa loại trừ là các giá trị băm "thật", KHÔNG phải khóa định tuyến - Các kiểu 3, 5 và 7 (biến thể LeaseSet2) có thể được trả về kể từ 0.9.38. Xem [Proposal 123](/proposals/123-new-netdb-entries/) - **Ghi chú về tra cứu thăm dò:** Một tra cứu thăm dò được định nghĩa là trả về danh sách các giá trị băm không phải floodfill gần với khóa. Tuy nhiên, các bản triển khai khác nhau: Java có tra cứu khóa tìm kiếm cho một RI (RouterInfo) và trả về một DatabaseStore nếu có; i2pd thì không. Do đó, không khuyến nghị dùng tra cứu thăm dò cho các giá trị băm đã nhận trước đó

**Mã nguồn:** - `net.i2p.data.i2np.DatabaseLookupMessage` - Mã hóa: `net.i2p.crypto.SessionKeyManager`

---

### DatabaseSearchReply (Phản hồi tìm kiếm cơ sở dữ liệu) (Loại 3)

**Mục đích:** Phản hồi đối với một thông điệp DatabaseLookup thất bại.

**Nội dung:** Danh sách các băm của router gần nhất với khóa được yêu cầu.

**Định dạng:**

```
+----+----+----+----+----+----+----+----+
| SHA256 hash as query key (32 bytes)  |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| num| peer_hashes (variable)           |
+----+                                  +
|                                       |
~                                       ~
|                                       |
+    +----+----+----+----+----+----+----+
|    | from (32 bytes)                  |
+----+                                  +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+    +----+----+----+----+----+----+----+
|    |
+----+

key :: 32 bytes
       SHA256 of the object being searched

num :: 1 byte Integer
       Number of peer hashes that follow (0-255)

peer_hashes :: $num SHA256 hashes of 32 bytes each (total $num*32 bytes)
               SHA256 of the RouterIdentity that the sender thinks is
               close to the key

from :: 32 bytes
        SHA256 of the RouterInfo of the router this reply was sent from
```
**Ghi chú:** - 'from' hash không được xác thực và không thể tin cậy - Các băm của peer (nút ngang hàng) được trả về không nhất thiết gần với khóa hơn so với router đang được truy vấn. Đối với các phản hồi cho tra cứu thông thường, điều này giúp khám phá các floodfill mới và tìm kiếm "ngược" (xa khóa hơn) để tăng độ bền vững - Đối với các tra cứu thăm dò, khóa thường được tạo ngẫu nhiên. non-floodfill peer_hashes trong phản hồi có thể được chọn bằng một thuật toán được tối ưu (ví dụ: các peer ở gần nhưng không nhất thiết là gần nhất) để tránh phải sắp xếp kém hiệu quả toàn bộ cơ sở dữ liệu cục bộ. Cũng có thể sử dụng các chiến lược lưu đệm. Điều này phụ thuộc vào triển khai - **Số lượng băm trả về điển hình:** 3 - **Số lượng băm tối đa khuyến nghị để trả về:** 16 - Khóa tra cứu, các băm của peer, và 'from' hash là các băm "thực", KHÔNG PHẢI các khóa định tuyến - Nếu num là 0, điều này cho biết không tìm thấy các peer gần hơn (ngõ cụt)

**Mã nguồn:** - `net.i2p.data.i2np.DatabaseSearchReplyMessage`

---

### DeliveryStatus (trạng thái giao nhận) (Loại 10)

**Mục đích:** Một xác nhận thông điệp đơn giản. Thường do bên khởi tạo thông điệp tạo ra và được bọc trong một Garlic Message (dạng thông điệp Garlic trong I2P) cùng với chính thông điệp, để được phía đích trả lại.

**Nội dung:** ID của thông điệp đã được giao và thời điểm tạo hoặc thời điểm đến.

**Định dạng:**

```
+----+----+----+----+----+----+----+----+----+----+----+----+
| msg_id (4)            | time_stamp (8)                    |
+----+----+----+----+----+----+----+----+----+----+----+----+

msg_id :: Integer (4 bytes)
          Unique ID of the message we deliver the DeliveryStatus for
          (see I2NP Message Header for details)

time_stamp :: Date (8 bytes)
              Time the message was successfully created or delivered
```
**Ghi chú:** - Dấu thời gian luôn được bên tạo đặt thành thời gian hiện tại. Tuy nhiên, có một số nơi trong mã nguồn đang sử dụng mục này, và có thể sẽ bổ sung thêm trong tương lai - Thông điệp này cũng được dùng như một xác nhận đã thiết lập phiên trong SSU. Trong trường hợp này, message ID được đặt thành một số ngẫu nhiên, và "arrival time" được đặt thành ID toàn mạng hiện tại, là 2 (tức `0x0000000000000002`) - DeliveryStatus (thông điệp trạng thái giao nhận) thường được gói trong một GarlicMessage (kiểu thông điệp Garlic trong I2P) và gửi qua tunnel để cung cấp xác nhận mà không tiết lộ người gửi - Dùng để kiểm thử tunnel nhằm đo độ trễ và độ tin cậy

**Mã nguồn:** - `net.i2p.data.i2np.DeliveryStatusMessage` - Được dùng trong: `net.i2p.router.tunnel.InboundEndpointProcessor` để kiểm thử tunnel

---

### GarlicMessage (thông điệp Garlic trong I2P) (Loại 11)

**CẢNH BÁO:** Đây là định dạng được dùng cho garlic messages (thông điệp "garlic" trong I2P) mã hóa bằng ElGamal. Định dạng cho garlic messages ECIES-AEAD-X25519-Ratchet khác biệt đáng kể. Xem [Đặc tả ECIES](/docs/specs/ecies/) để biết định dạng hiện đại.

**Mục đích:** Được dùng để bao gói nhiều thông điệp I2NP đã được mã hóa.

**Nội dung:** Khi được giải mã, một chuỗi Garlic Cloves (các clove - tiểu thông điệp) và dữ liệu bổ sung, còn được gọi là một Clove Set (tập hợp các clove).

**Định dạng được mã hóa:**

```
+----+----+----+----+----+----+----+----+
| length (4)            | data          |
+----+----+----+----+----+              +
|                                       |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

length :: 4 byte Integer
          Number of bytes that follow (0 to 64 KB)

data :: $length bytes
        ElGamal encrypted data
```
**Dữ liệu đã giải mã (Clove Set - tập hợp các "clove" trong garlic encryption):**

```
+----+----+----+----+----+----+----+----+
| num| clove 1 (variable)               |
+----+                                  +
|                                       |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| clove 2 (variable)                    |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Certificate (3) | Message_ID (4)  |
+----+----+----+----+----+----+----+----+
    Expiration (8)                  |
+----+----+----+----+----+----+----+----+

num :: 1 byte Integer
       Number of GarlicCloves to follow

clove :: GarlicClove (see GarlicClove structure above)

Certificate :: Always NULL (3 bytes total, all zeroes)

Message_ID :: 4 byte Integer

Expiration :: Date (8 bytes)
```

**Đối với định dạng ECIES-X25519-AEAD-Ratchet (tiêu chuẩn hiện tại cho routers):**

Xem [Đặc tả ECIES](/docs/specs/ecies/) và [Đề xuất 144](/proposals/144-ecies-x25519-aead-ratchet/).

**Mã nguồn:** - `net.i2p.data.i2np.GarlicMessage` - Mã hóa: `net.i2p.crypto.elgamal.ElGamalAESEngine` (đã lỗi thời) - Mã hóa hiện đại: `net.i2p.crypto.ECIES` các gói

---

### TunnelData (Loại 18)

**Mục đích:** Một thông điệp được gửi từ cổng của một tunnel hoặc một thành viên tới thành viên tiếp theo hoặc điểm cuối. Dữ liệu có độ dài cố định, chứa các thông điệp I2NP được phân mảnh, gom theo lô, đệm và mã hóa.

**Định dạng:**

```
+----+----+----+----+----+----+----+----+
| tunnelID (4)          | data (1024)   |
+----+----+----+----+----+              +
|                                       |
~                                       ~
|                                       |
+                   +----+----+----+----+
|                   |
+----+----+----+----+

tunnelId :: 4 bytes
            TunnelId identifying the tunnel this message is directed at
            Nonzero

data :: 1024 bytes
        Payload data, fixed to 1024 bytes
```
**Cấu trúc Payload (phần dữ liệu hữu ích) (1024 byte):**

```
Bytes 0-15: Initialization Vector (IV) for AES encryption
Bytes 16-1023: Encrypted tunnel message data (1008 bytes)
```
**Ghi chú:** - ID thông điệp I2NP cho TunnelData được đặt thành một số ngẫu nhiên mới tại mỗi hop (nút chuyển tiếp) - Định dạng thông điệp tunnel (bên trong dữ liệu đã mã hóa) được quy định trong [Đặc tả Thông điệp tunnel](/docs/specs/implementation/) - Mỗi hop giải mã một lớp bằng AES-256 ở chế độ CBC - IV (vector khởi tạo) được cập nhật tại mỗi hop bằng cách sử dụng dữ liệu đã giải mã - Tổng kích thước chính xác là 1,028 byte (4 tunnelId + 1024 data) - Đây là đơn vị cơ bản của lưu lượng tunnel - Các thông điệp TunnelData mang các thông điệp I2NP bị phân mảnh (GarlicMessage, DatabaseStore, v.v.)

**Mã nguồn:** - `net.i2p.data.i2np.TunnelDataMessage` - Hằng số: `TunnelDataMessage.DATA_LENGTH = 1024` - Xử lý: `net.i2p.router.tunnel.InboundGatewayProcessor`

---

### TunnelGateway (Loại 19)

**Mục đích:** Bao bọc một thông điệp I2NP khác để gửi vào một tunnel tại cổng vào của tunnel.

**Định dạng:**

```
+----+----+----+----+----+----+----+-//
| tunnelId (4)          | length (2)| data...
+----+----+----+----+----+----+----+-//

tunnelId :: 4 bytes
            TunnelId identifying the tunnel this message is directed at
            Nonzero

length :: 2 byte Integer
          Length of the payload

data :: $length bytes
        Actual payload of this message
```
**Ghi chú:** - Nội dung (payload) là một thông điệp I2NP với phần đầu chuẩn 16 byte - Dùng để chèn các thông điệp vào tunnel từ router cục bộ - Cổng sẽ phân mảnh thông điệp đính kèm nếu cần - Sau khi phân mảnh, các mảnh được bao gói trong các thông điệp TunnelData - TunnelGateway không bao giờ được gửi qua mạng; đây là một kiểu thông điệp nội bộ được dùng trước khi xử lý tunnel

**Mã nguồn:** - `net.i2p.data.i2np.TunnelGatewayMessage` - Xử lý: `net.i2p.router.tunnel.OutboundGatewayProcessor`

---

### DataMessage (Loại 20)

**Mục đích:** Được sử dụng bởi Garlic Messages (thông điệp Garlic trong I2P) và Garlic Cloves (các clove—thành phần con trong thông điệp Garlic) để đóng gói dữ liệu tùy ý (thông thường là dữ liệu ứng dụng được mã hóa đầu-cuối).

**Định dạng:**

```
+----+----+----+----+----+----+-//-+
| length (4)            | data...    |
+----+----+----+----+----+----+-//-+

length :: 4 bytes
          Length of the payload

data :: $length bytes
        Actual payload of this message
```
**Ghi chú:** - Thông điệp này không chứa thông tin định tuyến và sẽ không bao giờ được gửi ở dạng "unwrapped" - Chỉ được dùng bên trong Garlic messages (thông điệp Garlic) - Thường chứa dữ liệu ứng dụng được mã hóa đầu-cuối (HTTP, IRC, email, v.v.) - Dữ liệu thường là một tải trọng được mã hóa bằng ElGamal/AES hoặc ECIES - Độ dài thực tế tối đa khoảng 61.2 KB do giới hạn phân mảnh thông điệp tunnel

**Mã nguồn:** - `net.i2p.data.i2np.DataMessage`

---

### TunnelBuild (Loại 21)

**ĐÃ LỖI THỜI.** Hãy dùng VariableTunnelBuild (type 23) hoặc ShortTunnelBuild (type 25).

**Mục đích:** Yêu cầu xây dựng tunnel có độ dài cố định gồm 8 hop (chặng).

**Định dạng:**

```
+----+----+----+----+----+----+----+----+
| Record 0 (528 bytes)                  |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Record 1 (528 bytes)                  |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Record 7 (528 bytes)                  |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

Just 8 BuildRequestRecords attached together
Record size: 528 bytes
Total size: 8 × 528 = 4,224 bytes
```
**Ghi chú:** - Kể từ 0.9.48, có thể chứa ECIES-X25519 BuildRequestRecords. Xem [Tạo tunnel ECIES](/docs/specs/implementation/) - Xem [Đặc tả tạo tunnel](/docs/specs/implementation/) để biết chi tiết - ID thông điệp I2NP cho thông điệp này phải được đặt theo đặc tả tạo tunnel - Mặc dù hiếm khi thấy trong mạng hiện nay (được thay thế bởi VariableTunnelBuild), nó vẫn có thể được dùng cho các tunnel rất dài và chưa bị loại bỏ một cách chính thức - Các router vẫn phải triển khai điều này để tương thích - Định dạng cố định 8-bản ghi thiếu linh hoạt và lãng phí băng thông đối với các tunnel ngắn hơn

**Mã nguồn:** - `net.i2p.data.i2np.TunnelBuildMessage` - Hằng số: `TunnelBuildMessageBase.MAX_RECORD_COUNT = 8`

---

### TunnelBuildReply (Loại 22)

**ĐÃ LỖI THỜI.** Hãy dùng VariableTunnelBuildReply (loại 24) hoặc OutboundTunnelBuildReply (loại 26).

**Mục đích:** Phản hồi xây dựng tunnel có độ dài cố định cho 8 chặng.

**Định dạng:**

Cùng định dạng như TunnelBuildMessage, với BuildResponseRecords thay cho BuildRequestRecords.

```
Total size: 8 × 528 = 4,224 bytes
```
**Ghi chú:** - Kể từ 0.9.48, có thể chứa ECIES-X25519 BuildResponseRecords (các bản ghi phản hồi trong quá trình xây dựng). Xem [Tạo tunnel bằng ECIES](/docs/specs/implementation/) - Xem [Đặc tả tạo tunnel](/docs/specs/implementation/) để biết chi tiết - ID thông điệp I2NP cho thông điệp này phải được đặt theo đặc tả tạo tunnel - Mặc dù hiếm gặp trên mạng hiện nay (được thay thế bởi VariableTunnelBuildReply (thông điệp phản hồi xây dựng tunnel biến độ dài)), nó vẫn có thể được dùng cho các tunnel rất dài và chưa bị loại bỏ chính thức - Các router vẫn phải triển khai điều này để đảm bảo khả năng tương thích

**Mã nguồn:** - `net.i2p.data.i2np.TunnelBuildReplyMessage`

---

### VariableTunnelBuild (Xây dựng tunnel biến thiên) (Loại 23)

**Mục đích:** Xây dựng tunnel có độ dài thay đổi từ 1 đến 8 hops (bước nhảy). Hỗ trợ cả routers ElGamal và ECIES-X25519.

**Định dạng:**

```
+----+----+----+----+----+----+----+----+
| num| BuildRequestRecords (variable)   |
+----+----+----+----+----+----+----+----+

num :: 1 byte Integer
       Valid values: 1-8

BuildRequestRecords :: $num records of 528 bytes each

Record size: 528 bytes
Total size: 1 + ($num × 528) bytes
```
**Ghi chú:** - Kể từ 0.9.48, có thể chứa ECIES-X25519 BuildRequestRecords (bản ghi yêu cầu xây dựng). Xem [Tạo Tunnel ECIES](/docs/specs/implementation/) - Được giới thiệu trong phiên bản router 0.7.12 (2009) - Không được gửi tới các thành viên tunnel chạy phiên bản trước 0.7.12 - Xem [Đặc tả Tạo Tunnel](/docs/specs/implementation/) để biết chi tiết - ID thông điệp I2NP phải được đặt theo đặc tả tạo tunnel - **Số lượng bản ghi điển hình:** 4 (đối với một tunnel 4-hop) - **Kích thước tổng điển hình:** 1 + (4 × 528) = 2,113 byte - Đây là thông điệp xây dựng tunnel tiêu chuẩn cho các router ElGamal - Các router ECIES thường sử dụng ShortTunnelBuild (loại 25) thay vào đó

**Mã nguồn:** - `net.i2p.data.i2np.VariableTunnelBuildMessage`

---

### VariableTunnelBuildReply (Loại 24)

**Mục đích:** Phản hồi xây dựng tunnel có độ dài biến thiên cho 1–8 chặng. Hỗ trợ cả routers ElGamal và ECIES-X25519.

**Định dạng:**

Cùng định dạng như VariableTunnelBuildMessage, nhưng dùng BuildResponseRecords thay cho BuildRequestRecords.

```
+----+----+----+----+----+----+----+----+
| num| BuildResponseRecords (variable)  |
+----+----+----+----+----+----+----+----+

num :: 1 byte Integer
       Valid values: 1-8

BuildResponseRecords :: $num records of 528 bytes each

Record size: 528 bytes
Total size: 1 + ($num × 528) bytes
```
**Ghi chú:** - Kể từ 0.9.48, có thể chứa ECIES-X25519 BuildResponseRecords (bản ghi phản hồi xây dựng). Xem [Tạo Tunnel bằng ECIES](/docs/specs/implementation/) - Được giới thiệu trong phiên bản router 0.7.12 (2009) - Có thể không được gửi tới các thành viên tunnel dùng phiên bản trước 0.7.12 - Xem [Đặc tả Tạo Tunnel](/docs/specs/implementation/) để biết chi tiết - ID của thông điệp I2NP phải được đặt theo đặc tả tạo tunnel - **Số lượng bản ghi điển hình:** 4 - **Tổng kích thước điển hình:** 2,113 byte

**Mã nguồn:** - `net.i2p.data.i2np.VariableTunnelBuildReplyMessage`

---

### ShortTunnelBuild (xây dựng tunnel rút gọn, Loại 25)

**Purpose:** Thông điệp dựng tunnel dạng ngắn chỉ dành cho routers ECIES-X25519. Được giới thiệu trong phiên bản API 0.9.51 (phát hành 1.5.0, tháng 8 năm 2021). Đây là tiêu chuẩn hiện tại cho việc dựng tunnel ECIES.

**Định dạng:**

```
+----+----+----+----+----+----+----+----+
| num| ShortBuildRequestRecords (var)   |
+----+----+----+----+----+----+----+----+

num :: 1 byte Integer
       Valid values: 1-8

ShortBuildRequestRecords :: $num records of 218 bytes each

Record size: 218 bytes
Total size: 1 + ($num × 218) bytes
```
**Ghi chú:** - Được giới thiệu trong phiên bản router 0.9.51 (phát hành 1.5.0, tháng 8/2021) - Có thể không được gửi tới các thành viên tunnel trước phiên bản API 0.9.51 - Xem [Tạo Tunnel ECIES](/docs/specs/implementation/) để biết đặc tả đầy đủ - Xem [Đề xuất 157](/proposals/157-new-tbm/) để biết lý do - **Số lượng bản ghi điển hình:** 4 - **Tổng kích thước điển hình:** 1 + (4 × 218) = 873 bytes - **Tiết kiệm băng thông:** nhỏ hơn 59% so với VariableTunnelBuild (873 vs 2,113 bytes) - **Lợi ích hiệu năng:** 4 bản ghi ngắn vừa trong một tunnel message; VariableTunnelBuild cần 3 tunnel messages - Đây hiện là định dạng xây dựng tunnel tiêu chuẩn cho các tunnel ECIES-X25519 thuần túy (ECIES: sơ đồ mã hóa dựa trên đường cong elliptic; X25519: cơ chế trao đổi khóa Curve25519) - Các bản ghi suy dẫn khóa thông qua HKDF (hàm dẫn xuất khóa dựa trên HMAC), thay vì đưa chúng vào một cách tường minh

**Mã nguồn:** - `net.i2p.data.i2np.ShortTunnelBuildMessage` - Hằng số: `ShortEncryptedBuildRecord.RECORD_SIZE = 218`

---

### OutboundTunnelBuildReply (Loại 26)

**Mục đích:** Được gửi từ điểm cuối gửi đi của một tunnel mới đến bên khởi tạo. Chỉ áp dụng cho các router ECIES-X25519. Được giới thiệu trong phiên bản API 0.9.51 (bản phát hành 1.5.0, tháng 8 năm 2021).

**Định dạng:**

Cùng định dạng như ShortTunnelBuildMessage, với ShortBuildResponseRecords thay vì ShortBuildRequestRecords.

```
+----+----+----+----+----+----+----+----+
| num| ShortBuildResponseRecords (var)  |
+----+----+----+----+----+----+----+----+

num :: 1 byte Integer
       Valid values: 1-8

ShortBuildResponseRecords :: $num records of 218 bytes each

Record size: 218 bytes
Total size: 1 + ($num × 218) bytes
```
**Ghi chú:** - Được giới thiệu trong router phiên bản 0.9.51 (phát hành 1.5.0, tháng 8 năm 2021) - Xem [ECIES Tunnel Creation](/docs/specs/implementation/) để biết đặc tả đầy đủ - **Số lượng bản ghi điển hình:** 4 - **Tổng kích thước điển hình:** 873 byte - Phản hồi này được gửi từ outbound endpoint (điểm cuối hướng ra, OBEP) trở lại bên tạo tunnel thông qua tunnel hướng ra vừa được tạo - Cung cấp xác nhận rằng mọi nút trung gian đều đã chấp nhận việc dựng tunnel

**Mã nguồn:** - `net.i2p.data.i2np.OutboundTunnelBuildReplyMessage`

---

## Tài liệu tham khảo

### Các đặc tả chính thức

- **[Đặc tả I2NP](/docs/specs/i2np/)** - Đặc tả đầy đủ về định dạng thông điệp I2NP
- **[Cấu trúc chung](/docs/specs/common-structures/)** - Các kiểu dữ liệu và cấu trúc được sử dụng xuyên suốt I2P
- **[Tạo tunnel](/docs/specs/implementation/)** - Tạo tunnel ElGamal (đã lỗi thời)
- **[Tạo tunnel ECIES](/docs/specs/implementation/)** - Tạo tunnel ECIES-X25519 (hiện tại)
- **[Thông điệp tunnel](/docs/specs/implementation/)** - Định dạng thông điệp tunnel và hướng dẫn chuyển giao
- **[Đặc tả NTCP2](/docs/specs/ntcp2/)** - Giao thức truyền tải TCP
- **[Đặc tả SSU2](/docs/specs/ssu2/)** - Giao thức truyền tải UDP
- **[Đặc tả ECIES](/docs/specs/ecies/)** - Mã hóa ECIES-X25519-AEAD-Ratchet
- **[Đặc tả mật mã](/docs/specs/cryptography/)** - Các nguyên thủy mật mã cấp thấp
- **[Đặc tả I2CP](/docs/specs/i2cp/)** - Đặc tả giao thức máy khách
- **[Đặc tả Datagram](/docs/api/datagrams/)** - Định dạng Datagram2 và Datagram3

### Các đề xuất

- **[Đề xuất 123](/proposals/123-new-netdb-entries/)** - Các mục netDB mới (LeaseSet2, EncryptedLeaseSet, MetaLeaseSet)
- **[Đề xuất 144](/proposals/144-ecies-x25519-aead-ratchet/)** - Mã hóa ECIES-X25519-AEAD-Ratchet
- **[Đề xuất 154](/proposals/154-ecies-lookups/)** - Tra cứu cơ sở dữ liệu được mã hóa
- **[Đề xuất 156](/proposals/156-ecies-routers/)** - Các router ECIES
- **[Đề xuất 157](/proposals/157-new-tbm/)** - Thông điệp xây dựng tunnel nhỏ hơn (định dạng ngắn)
- **[Đề xuất 159](/proposals/159-ssu2/)** - Giao thức truyền tải SSU2
- **[Đề xuất 161](/vi/proposals/161-ri-dest-padding/)** - Đệm có thể nén
- **[Đề xuất 163](/proposals/163-datagram2/)** - Datagram2 và Datagram3
- **[Đề xuất 167](/proposals/167-service-records/)** - Các tham số bản ghi dịch vụ LeaseSet
- **[Đề xuất 168](/proposals/168-tunnel-bandwidth/)** - Các tham số băng thông xây dựng tunnel
- **[Đề xuất 169](/proposals/169-pq-crypto/)** - Mật mã lai hậu lượng tử

### Tài liệu

- **[Định tuyến Garlic](/docs/overview/garlic-routing/)** - Đóng gói thông điệp theo lớp
- **[ElGamal/AES](/docs/legacy/elgamal-aes/)** - Lược đồ mã hóa không còn được khuyến nghị
- **[Triển khai Tunnel](/docs/specs/implementation/)** - Phân mảnh và xử lý
- **[Cơ sở dữ liệu mạng](/docs/specs/common-structures/)** - Bảng băm phân tán
- **[Truyền tải NTCP2](/docs/specs/ntcp2/)** - Đặc tả truyền tải TCP
- **[Truyền tải SSU2](/docs/specs/ssu2/)** - Đặc tả truyền tải UDP
- **[Giới thiệu kỹ thuật](/docs/overview/tech-intro/)** - Tổng quan kiến trúc I2P

### Mã nguồn

- **[Kho mã nguồn Java I2P](https://i2pgit.org/I2P_Developers/i2p.i2p)** - Triển khai Java chính thức
- **[Bản phản chiếu GitHub](https://github.com/i2p/i2p.i2p)** - Bản phản chiếu trên GitHub của Java I2P
- **[Kho mã nguồn i2pd](https://github.com/PurpleI2P/i2pd)** - Triển khai C++

### Các vị trí mã nguồn chính

**Java I2P (i2pgit.org/I2P_Developers/i2p.i2p):** - `core/java/src/net/i2p/data/i2np/` - Các triển khai thông điệp I2NP - `core/java/src/net/i2p/crypto/` - Các triển khai mật mã - `router/java/src/net/i2p/router/tunnel/` - Xử lý tunnel - `router/java/src/net/i2p/router/transport/` - Các triển khai transport

**Hằng số và giá trị:** - `I2NPMessage.MAX_SIZE = 65536` - Kích thước thông điệp I2NP tối đa - `I2NPMessageImpl.HEADER_LENGTH = 16` - Kích thước phần đầu (header) tiêu chuẩn - `TunnelDataMessage.DATA_LENGTH = 1024` - Phần tải của thông điệp Tunnel - `EncryptedBuildRecord.RECORD_SIZE = 528` - Bản ghi xây dựng dài - `ShortEncryptedBuildRecord.RECORD_SIZE = 218` - Bản ghi xây dựng ngắn - `TunnelBuildMessageBase.MAX_RECORD_COUNT = 8` - Số bản ghi tối đa cho mỗi lần xây dựng

---

## Phụ lục A: Thống kê mạng và trạng thái hiện tại

### Thành phần của mạng (tính đến tháng 10 năm 2025)

- **Tổng số router (nút I2P):** Khoảng 60,000-70,000 (thay đổi)
- **Router floodfill (nút lưu trữ netDb phân tán):** Khoảng 500-700 đang hoạt động
- **Các loại mã hóa:**
  - ECIES-X25519: >95% số router
  - ElGamal: <5% số router (không còn được khuyến nghị, chỉ dành cho mục đích kế thừa)
- **Mức độ sử dụng giao thức truyền tải:**
  - SSU2 (giao thức truyền tải dựa trên UDP thế hệ 2): >60% giao thức truyền tải chính
  - NTCP2 (giao thức truyền tải dựa trên TCP thế hệ 2): ~40% giao thức truyền tải chính
  - Giao thức truyền tải kế thừa (SSU1, NTCP): 0% (đã loại bỏ)
- **Các loại chữ ký:**
  - EdDSA (Ed25519): Chiếm đại đa số
  - ECDSA: Tỷ lệ nhỏ
  - RSA: Không cho phép (đã loại bỏ)

### Yêu cầu tối thiểu cho Router

- **Phiên bản API:** 0.9.16+ (đảm bảo tương thích EdDSA với mạng)
- **Mức khuyến nghị tối thiểu:** API 0.9.51+ (các bản dựng tunnel (đường hầm) ngắn ECIES)
- **Mức tối thiểu hiện tại cho floodfills (các router lưu trữ netDb):** API 0.9.58+ (loại bỏ dần router ElGamal)
- **Yêu cầu sắp tới:** Java 17+ (kể từ bản phát hành 2.11.0, tháng 12/2025)

### Yêu cầu về băng thông

- **Tối thiểu:** 128 KBytes/sec (cờ N hoặc cao hơn) cho floodfill (chế độ nút lưu trữ netDb phân tán)
- **Khuyến nghị:** 256 KBytes/sec (cờ O) hoặc cao hơn
- **Yêu cầu floodfill:**
  - Băng thông tối thiểu 128 KB/sec
  - Thời gian hoạt động ổn định (>95% được khuyến nghị)
  - Độ trễ thấp (<500ms tới các peer)
  - Vượt qua các bài kiểm tra sức khỏe (thời gian hàng đợi, độ trễ tác vụ)

### Thống kê Tunnel

- **Độ dài tunnel điển hình:** 3-4 hop (chặng truyền)
- **Độ dài tunnel tối đa:** 8 hop (mang tính lý thuyết, hiếm khi dùng)
- **Thời gian tồn tại điển hình của tunnel:** 10 phút
- **Tỷ lệ xây dựng tunnel thành công:** >85% đối với các routers kết nối tốt
- **Định dạng thông điệp xây dựng tunnel:**
  - Các routers ECIES: ShortTunnelBuild (bản ghi 218 byte)
  - Các tunnel hỗn hợp: VariableTunnelBuild (bản ghi 528 byte)

### Các chỉ số hiệu năng

- **Thời gian xây dựng Tunnel:** 1-3 giây (điển hình)
- **Độ trễ đầu-cuối:** 0.5-2 giây (điển hình, 6-8 hop tổng cộng)
- **Thông lượng:** Bị giới hạn bởi băng thông tunnel (thường 10-50 KB/sec mỗi tunnel)
- **Kích thước datagram tối đa:** Khuyến nghị 10 KB (61.2 KB tối đa theo lý thuyết)

---

## Phụ lục B: Các tính năng đã ngừng hỗ trợ và đã bị loại bỏ

### Đã loại bỏ hoàn toàn (không còn được hỗ trợ)

- **Giao thức truyền tải NTCP** - Đã bị loại bỏ trong bản phát hành 0.9.50 (Tháng 5 năm 2021)
- **Giao thức truyền tải SSU v1** - Đã bị loại bỏ khỏi Java I2P trong bản phát hành 2.4.0 (Tháng 12 năm 2023)
- **Giao thức truyền tải SSU v1** - Đã bị loại bỏ khỏi i2pd trong bản phát hành 2.44.0 (Tháng 11 năm 2022)
- **Các loại chữ ký RSA** - Không được phép kể từ API 0.9.28

### Đã lỗi thời (vẫn được hỗ trợ nhưng không khuyến nghị)

- **router ElGamal** - Ngừng sử dụng kể từ API 0.9.58 (tháng 3 năm 2023)
  - Các đích ElGamal vẫn được hỗ trợ để bảo đảm tương thích ngược
  - Các router mới nên chỉ sử dụng ECIES-X25519
- **TunnelBuild (type 21)** - Ngừng sử dụng, thay bằng VariableTunnelBuild và ShortTunnelBuild
  - Vẫn được triển khai cho các tunnel rất dài (>8 hop)
- **TunnelBuildReply (type 22)** - Ngừng sử dụng, thay bằng VariableTunnelBuildReply và OutboundTunnelBuildReply
- **Mã hóa ElGamal/AES** - Ngừng sử dụng, thay bằng ECIES-X25519-AEAD-Ratchet
  - Vẫn được dùng cho các đích cũ
- **BuildRequestRecords ECIES dạng dài (528 byte)** - Ngừng sử dụng, thay bằng định dạng ngắn (218 byte)
  - Vẫn được dùng cho các tunnel hỗn hợp có hop ElGamal

### Lộ trình hỗ trợ các phiên bản cũ

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Feature</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Introduced</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Deprecated</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Removed</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NTCP</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2003</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2018 (0.9.36)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2021 (0.9.50)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Replaced by NTCP2</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">SSU v1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2004</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2022 (0.9.54)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2023 (Java) / 2022 (i2pd)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Replaced by SSU2</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ElGamal routers</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2003</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2023 (0.9.58)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">TBD</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Destinations still supported</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">RSA signatures</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2015</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2017</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2017 (0.9.28)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Never widely used</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">TunnelBuild</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2004</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2009 (0.7.12)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Not removed</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Still supported for long tunnels</td>
    </tr>
  </tbody>
</table>
---

## Phụ lục C: Các phát triển trong tương lai

### Mật mã hậu lượng tử

**Trạng thái:** Beta kể từ bản phát hành 2.10.0 (tháng 9 năm 2025), sẽ trở thành mặc định trong bản 2.11.0 (tháng 12 năm 2025)

**Triển khai:** - Cách tiếp cận lai kết hợp X25519 cổ điển và MLKEM hậu lượng tử (ML-KEM-768) - Tương thích ngược với cơ sở hạ tầng ECIES-X25519 hiện có - Sử dụng Signal Double Ratchet (thuật toán Ratchet kép của Signal) với cả vật liệu khóa cổ điển và PQ (hậu lượng tử) - Xem [Đề xuất 169](/proposals/169-pq-crypto/) để biết chi tiết

**Lộ trình chuyển đổi:** 1. Bản phát hành 2.10.0 (Tháng 9 năm 2025): Có sẵn dưới dạng tùy chọn beta 2. Bản phát hành 2.11.0 (Tháng 12 năm 2025): Được bật theo mặc định 3. Các bản phát hành tương lai: Cuối cùng sẽ trở thành bắt buộc

### Các tính năng dự kiến

- **Cải tiến IPv6** - Hỗ trợ IPv6 tốt hơn và các cơ chế chuyển đổi
- **Giới hạn băng thông theo từng tunnel** - Kiểm soát băng thông chi tiết theo từng tunnel
- **Cải tiến số liệu đo lường** - Giám sát hiệu năng và chẩn đoán tốt hơn
- **Tối ưu hóa giao thức** - Giảm chi phí phụ trội và cải thiện hiệu quả
- **Cải thiện lựa chọn floodfill** - Phân phối netDb tốt hơn

### Các lĩnh vực nghiên cứu

- **Tối ưu hóa độ dài Tunnel** - Độ dài Tunnel động dựa trên mô hình đe dọa
- **Đệm nâng cao** - Cải thiện khả năng chống phân tích lưu lượng
- **Các sơ đồ mã hóa mới** - Chuẩn bị cho các mối đe dọa từ điện toán lượng tử
- **Kiểm soát tắc nghẽn** - Xử lý tải mạng tốt hơn
- **Hỗ trợ di động** - Tối ưu hóa cho thiết bị và mạng di động

---

## Phụ lục D: Hướng dẫn triển khai

### Dành cho các triển khai mới

**Yêu cầu tối thiểu:** 1. Hỗ trợ các tính năng của API phiên bản 0.9.51+ 2. Triển khai mã hóa ECIES-X25519-AEAD-Ratchet (thuật toán mã hóa lai ECIES dùng X25519, AEAD và cơ chế ratchet) 3. Hỗ trợ các giao thức truyền tải NTCP2 và SSU2 4. Triển khai các thông điệp ShortTunnelBuild (thông điệp xây dựng tunnel dạng rút gọn; bản ghi 218 byte) 5. Hỗ trợ các biến thể LeaseSet2 (kiểu 3, 5, 7) 6. Sử dụng chữ ký EdDSA (Ed25519)

**Khuyến nghị:** 1. Hỗ trợ post-quantum hybrid cryptography (mật mã lai hậu lượng tử) (kể từ 2.11.0) 2. Triển khai các tham số băng thông theo tunnel 3. Hỗ trợ các định dạng Datagram2 và Datagram3 4. Triển khai các tùy chọn bản ghi dịch vụ trong LeaseSets 5. Tuân theo các đặc tả chính thức tại /docs/specs/

**Không bắt buộc:** 1. Hỗ trợ router ElGamal (không còn được khuyến nghị) 2. Hỗ trợ transport cũ (SSU1, NTCP) 3. BuildRequestRecords ECIES loại dài (528 byte cho các tunnel ECIES thuần túy) 4. Các thông điệp TunnelBuild/TunnelBuildReply (sử dụng các biến thể Variable hoặc Short)

### Kiểm thử và thẩm định

**Tuân thủ giao thức:** 1. Kiểm thử khả năng tương tác với router I2P Java chính thức 2. Kiểm thử khả năng tương tác với router i2pd C++ 3. Xác minh định dạng thông điệp đối chiếu với đặc tả 4. Kiểm thử các chu kỳ thiết lập/hủy tunnel 5. Xác minh mã hóa/giải mã bằng các test vectors (bộ vector kiểm thử tiêu chuẩn)

**Kiểm thử hiệu năng:** 1. Đo tỷ lệ thành công khi xây dựng tunnel (nên >85%) 2. Kiểm thử với các độ dài tunnel khác nhau (2-8 chặng (hop)) 3. Xác minh phân mảnh và tái lắp ráp 4. Kiểm thử dưới tải (nhiều tunnels đồng thời) 5. Đo độ trễ đầu-cuối

**Kiểm thử bảo mật:** 1. Xác minh triển khai mã hóa (sử dụng test vectors (bộ giá trị kiểm thử chuẩn)) 2. Kiểm thử cơ chế ngăn chặn tấn công phát lại 3. Xác thực cơ chế xử lý hết hạn thông điệp 4. Kiểm thử đối với thông điệp sai định dạng 5. Xác minh việc tạo số ngẫu nhiên đúng cách

### Những cạm bẫy thường gặp khi hiện thực

1. **Định dạng chỉ dẫn chuyển giao gây nhầm lẫn** - Garlic clove (một “nhánh” trong cơ chế garlic) vs thông điệp tunnel
2. **Dẫn xuất khóa không đúng** - Cách dùng HKDF cho bản ghi build dạng ngắn
3. **Xử lý Message ID** - Không thiết lập đúng cho việc build tunnel
4. **Vấn đề phân mảnh** - Không tuân thủ giới hạn thực tế 61.2 KB
5. **Lỗi thứ tự byte** - Java dùng big-endian cho mọi số nguyên
6. **Xử lý hết hạn** - Định dạng ngắn sẽ quay vòng vào ngày 7 tháng 2 năm 2106
7. **Tạo checksum** - Vẫn bắt buộc ngay cả khi không được xác minh
