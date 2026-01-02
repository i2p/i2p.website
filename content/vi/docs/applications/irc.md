---
title: "IRC qua I2P"
description: "Hướng dẫn toàn diện về mạng IRC trên I2P, client, tunnel và cài đặt server (cập nhật 2025)"
slug: "irc"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## Tổng quan

**Những điểm chính**

- I2P cung cấp **mã hóa đầu cuối đến đầu cuối (end-to-end encryption)** cho lưu lượng IRC thông qua các tunnel của nó. **Tắt SSL/TLS** trong các IRC client trừ khi bạn đang outproxy ra clearnet.
- Tunnel client **Irc2P** được cấu hình sẵn lắng nghe trên **127.0.0.1:6668** theo mặc định. Kết nối IRC client của bạn đến địa chỉ và cổng đó.
- Không sử dụng thuật ngữ "router‑provided TLS." Sử dụng "mã hóa gốc của I2P (I2P's native encryption)" hoặc "mã hóa đầu cuối đến đầu cuối (end‑to‑end encryption)."

## Bắt đầu nhanh (Java I2P)

1. Mở **Hidden Services Manager** tại `http://127.0.0.1:7657/i2ptunnel/` và đảm bảo tunnel **Irc2P** đang **chạy**.
2. Trong IRC client của bạn, đặt **server** = `127.0.0.1`, **port** = `6668`, **SSL/TLS** = **off**.
3. Kết nối và tham gia các kênh như `#i2p`, `#i2p-dev`, `#i2p-help`.

Đối với người dùng **i2pd** (router C++), tạo một client tunnel trong `tunnels.conf` (xem các ví dụ bên dưới).

## Mạng và máy chủ

### IRC2P (main community network)

- Các máy chủ liên hợp: `irc.postman.i2p:6667`, `irc.echelon.i2p:6667`, `irc.dg.i2p:6667`.
- **Tunnel Irc2P** tại `127.0.0.1:6668` kết nối tự động đến một trong các máy chủ này.
- Các kênh thông dụng: `#i2p`, `#i2p-chat`, `#i2p-dev`, `#i2p-help`.

### Ilita network

- Máy chủ: `irc.ilita.i2p:6667`, `irc.r4sas.i2p:6667`, `irc.acetone.i2p:6667`, `rusirc.ilita.i2p:6667`.
- Ngôn ngữ chính: Tiếng Nga và Tiếng Anh. Giao diện web có sẵn trên một số máy chủ.

## Client setup

### Recommended, actively maintained

- **WeeChat (terminal)** — hỗ trợ SOCKS mạnh mẽ; dễ dàng viết script.
- **Pidgin (desktop)** — vẫn được bảo trì; hoạt động tốt trên Windows/Linux.
- **Thunderbird Chat (desktop)** — được hỗ trợ trong ESR 128+.
- **The Lounge (self‑hosted web)** — client web hiện đại.

### IRC2P (mạng cộng đồng chính)

- **LimeChat** (miễn phí, mã nguồn mở).
- **Textual** (trả phí trên App Store; mã nguồn có sẵn để build).

### Mạng Ilita

#### WeeChat via SOCKS5

```
/proxy add i2p socks5 127.0.0.1 4447
/set irc.server.i2p.addresses "127.0.0.1/6668"
/set irc.server.i2p.proxy "i2p"
/connect i2p
```
#### Pidgin

- Giao thức: **IRC**
- Máy chủ: **127.0.0.1**
- Cổng: **6668**
- Mã hóa: **tắt**
- Tên người dùng/nick: bất kỳ

#### Thunderbird Chat

- Loại tài khoản: **IRC**
- Server: **127.0.0.1**
- Cổng: **6668**
- SSL/TLS: **tắt**
- Tùy chọn: tự động tham gia kênh khi kết nối

#### Dispatch (SAM v3)

Ví dụ mặc định cho `config.toml`:

```
[defaults]
name = "Irc2P"
host = "irc.postman.i2p"
port = 6667
channels = ["#i2p","#i2p-dev"]
ssl = false
```
## Tunnel configuration

### Java I2P defaults

- Tunnel client Irc2P: **127.0.0.1:6668** → máy chủ upstream trên **cổng 6667**.
- Trình quản lý Hidden Services: `http://127.0.0.1:7657/i2ptunnel/`.

### Được khuyến nghị, đang được bảo trì tích cực

`~/.i2pd/tunnels.conf`:

```
[IRC-IRC2P]
type = client
address = 127.0.0.1
port = 6668
destination = irc.postman.i2p
destinationport = 6667
keys = irc-keys.dat
```
Tunnel riêng cho Ilita (ví dụ):

```
[IRC-ILITA]
type = client
address = 127.0.0.1
port = 6669
destination = irc.ilita.i2p
destinationport = 6667
keys = irc-ilita-keys.dat
```
### Tùy chọn macOS

- **Bật SAM** trong Java I2P (mặc định tắt) tại `/configclients` hoặc `clients.config`.
- Mặc định: **127.0.0.1:7656/TCP** và **127.0.0.1:7655/UDP**.
- Khuyến nghị mã hóa: `SIGNATURE_TYPE=7` (Ed25519) và `i2cp.leaseSetEncType=4,0` (ECIES‑X25519 với dự phòng ElGamal) hoặc chỉ `4` cho phiên bản hiện đại.

### Các cấu hình mẫu

- Java I2P mặc định: **2 đường hầm vào / 2 đường hầm ra**.
- i2pd mặc định: **5 đường hầm vào / 5 đường hầm ra**.
- Đối với IRC: **2–3 mỗi loại** là đủ; thiết lập rõ ràng để đảm bảo hành vi nhất quán giữa các router.

## Thiết lập client

- **Không bật SSL/TLS** cho các kết nối IRC nội bộ I2P. I2P đã cung cấp mã hóa đầu cuối đến đầu cuối. TLS bổ sung chỉ tạo thêm chi phí mà không tăng tính ẩn danh.
- Sử dụng **khóa cố định** (persistent keys) để duy trì danh tính ổn định; tránh tạo lại khóa sau mỗi lần khởi động lại trừ khi đang thử nghiệm.
- Nếu nhiều ứng dụng sử dụng IRC, nên dùng **tunnel riêng biệt** (non‑shared) để giảm tương quan giữa các dịch vụ.
- Nếu bắt buộc phải cho phép điều khiển từ xa (SAM/I2CP), chỉ bind vào localhost và bảo mật truy cập bằng SSH tunnel hoặc reverse proxy có xác thực.

## Alternative connection method: SOCKS5

Một số client có thể kết nối qua SOCKS5 proxy của I2P: **127.0.0.1:4447**. Để đạt kết quả tốt nhất, nên ưu tiên sử dụng tunnel IRC chuyên dụng trên cổng 6668; SOCKS không thể làm sạch các định danh ở tầng ứng dụng và có thể làm lộ thông tin nếu client không được thiết kế cho tính ẩn danh.

## Troubleshooting

- **Không thể kết nối** — đảm bảo tunnel Irc2P đang chạy và router đã hoàn tất quá trình bootstrap.
- **Treo ở bước resolve/join** — kiểm tra kỹ SSL đã được **tắt** và client trỏ đến **127.0.0.1:6668**.
- **Độ trễ cao** — I2P có độ trễ cao hơn theo thiết kế. Giữ số lượng tunnel ở mức vừa phải (2–3) và tránh vòng lặp kết nối lại liên tục.
- **Sử dụng ứng dụng SAM** — xác nhận SAM đã được bật (Java) hoặc không bị chặn bởi firewall (i2pd). Nên sử dụng session dài hạn.

## Appendix: Ports and naming

- Các cổng tunnel IRC thông dụng: **6668** (mặc định của Irc2P), **6667** và **6669** làm cổng thay thế.
- Hostname `.b32.i2p`: dạng chuẩn 52 ký tự; dạng mở rộng 56+ ký tự tồn tại cho LS2/chứng chỉ nâng cao. Sử dụng hostname `.i2p` trừ khi bạn cần rõ ràng địa chỉ b32.
