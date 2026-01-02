---
title: "Cấu hình Trình duyệt Web"
description: "Cấu hình các trình duyệt phổ biến để sử dụng HTTP/HTTPS proxy của I2P trên máy tính để bàn và Android"
slug: "browser-config"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: tài liệu
---

Hướng dẫn này chỉ ra cách cấu hình các trình duyệt phổ biến để gửi lưu lượng truy cập qua HTTP proxy tích hợp sẵn của I2P. Hướng dẫn bao gồm Safari, Firefox và các trình duyệt Chrome/Chromium với các bước chi tiết từng bước.

**Lưu ý quan trọng**:

- Proxy HTTP mặc định của I2P lắng nghe trên `127.0.0.1:4444`.
- I2P bảo vệ lưu lượng bên trong mạng I2P (các trang .i2p).
- Đảm bảo router I2P của bạn đang chạy trước khi cấu hình trình duyệt.

## Safari (macOS)

Safari sử dụng cài đặt proxy toàn hệ thống trên macOS.

### Step 1: Open Network Settings

1. Mở **Safari** và vào **Safari → Settings** (hoặc **Preferences**)
2. Nhấp vào tab **Advanced**
3. Trong phần **Proxies**, nhấp **Change Settings...**

Thao tác này sẽ mở cài đặt mạng hệ thống trên Mac của bạn.

![Cài đặt nâng cao của Safari](/images/guides/browser-config/accessi2p_1.png)

### Bước 1: Mở Cài đặt Mạng

1. Trong phần cài đặt Network, đánh dấu vào ô **Web Proxy (HTTP)**
2. Nhập các thông tin sau:
   - **Web Proxy Server**: `127.0.0.1`
   - **Port**: `4444`
3. Nhấn **OK** để lưu cài đặt của bạn

![Cấu hình Proxy trên Safari](/images/guides/browser-config/accessi2p_2.png)

Bây giờ bạn có thể duyệt các trang `.i2p` trên Safari!

**Lưu ý**: Các cài đặt proxy này sẽ ảnh hưởng đến tất cả ứng dụng sử dụng proxy hệ thống của macOS. Hãy cân nhắc tạo một tài khoản người dùng riêng hoặc sử dụng một trình duyệt khác chỉ dành riêng cho I2P nếu bạn muốn tách biệt hoạt động duyệt web qua I2P.

## Firefox (Desktop)

Firefox có cài đặt proxy riêng độc lập với hệ thống, khiến nó trở thành lựa chọn lý tưởng cho việc duyệt web I2P chuyên dụng.

### Bước 2: Cấu hình HTTP Proxy

1. Nhấp vào **nút menu** (☰) ở góc trên bên phải
2. Chọn **Settings**

![Cài đặt Firefox](/images/guides/browser-config/accessi2p_3.png)

### Step 2: Find Proxy Settings

1. Trong hộp tìm kiếm Settings, gõ **"proxy"**
2. Cuộn xuống **Network Settings**
3. Nhấp vào nút **Settings...**

![Firefox Proxy Search](/images/guides/browser-config/accessi2p_4.png)

### Bước 1: Mở Cài đặt

1. Chọn **Cấu hình proxy thủ công**
2. Nhập thông tin sau:
   - **HTTP Proxy**: `127.0.0.1` **Port**: `4444`
3. Để trống **SOCKS Host** (trừ khi bạn cần dùng SOCKS proxy)
4. Đánh dấu **Proxy DNS when using SOCKS** chỉ khi sử dụng SOCKS proxy
5. Nhấn **OK** để lưu

![Cấu hình Proxy thủ công trên Firefox](/images/guides/browser-config/accessi2p_5.png)

Bây giờ bạn có thể duyệt các trang web `.i2p` trên Firefox!

**Mẹo**: Hãy cân nhắc tạo một profile Firefox riêng biệt dành cho việc duyệt web I2P. Điều này giúp tách biệt hoạt động duyệt web I2P của bạn khỏi việc duyệt web thông thường. Để tạo profile, gõ `about:profiles` vào thanh địa chỉ của Firefox.

## Chrome / Chromium (Desktop)

Chrome và các trình duyệt dựa trên Chromium (Brave, Edge, v.v.) thường sử dụng cài đặt proxy hệ thống trên Windows và macOS. Hướng dẫn này trình bày cấu hình trên Windows.

### Bước 2: Tìm Cài Đặt Proxy

1. Nhấp vào **menu ba chấm** (⋮) ở góc trên bên phải
2. Chọn **Settings**

![Cài đặt Chrome](/images/guides/browser-config/accessi2p_6.png)

### Bước 3: Cấu hình Proxy Thủ công

1. Trong hộp tìm kiếm Settings, gõ **"proxy"**
2. Nhấp vào **Open your computer's proxy settings**

![Chrome Proxy Search](/images/guides/browser-config/accessi2p_7.png)

### Step 3: Open Manual Proxy Setup

Thao tác này sẽ mở cài đặt Mạng & Internet của Windows.

1. Cuộn xuống **Thiết lập proxy thủ công**
2. Nhấp vào **Thiết lập**

![Cấu hình Proxy trên Windows](/images/guides/browser-config/accessi2p_8.png)

### Bước 1: Mở Chrome Settings

1. Chuyển **Use a proxy server** sang **On**
2. Nhập các thông tin sau:
   - **Proxy IP address**: `127.0.0.1`
   - **Port**: `4444`
3. Tùy chọn, thêm các ngoại lệ vào **"Don't use the proxy server for addresses beginning with"** (ví dụ: `localhost;127.*`)
4. Nhấn **Save**

![Cấu hình Proxy của Chrome](/images/guides/browser-config/accessi2p_9.png)

Bây giờ bạn có thể duyệt các trang `.i2p` trong Chrome!

**Lưu ý**: Các cài đặt này ảnh hưởng đến tất cả trình duyệt dựa trên Chromium và một số ứng dụng khác trên Windows. Để tránh điều này, hãy cân nhắc sử dụng Firefox với profile I2P riêng biệt.

### Bước 2: Mở Cài đặt Proxy

Trên Linux, bạn có thể khởi chạy Chrome/Chromium với các cờ proxy để tránh thay đổi cài đặt hệ thống:

```bash
chromium \
  --proxy-server="http=127.0.0.1:4444 \
  --proxy-bypass-list="<-loopback>"
```
Hoặc tạo một script khởi chạy trên desktop:

```bash
#!/bin/bash
chromium --proxy-server="http=127.0.0.1:4444" --user-data-dir="$HOME/.config/chromium-i2p"
```
Cờ `--user-data-dir` tạo một hồ sơ Chrome riêng biệt cho việc duyệt web I2P.

## Firefox (Desktop)

Các bản build Firefox "Fenix" hiện đại giới hạn about:config và extensions theo mặc định. IceRaven là một nhánh rẽ của Firefox cho phép một tập hợp extensions được tuyển chọn, giúp việc thiết lập proxy trở nên đơn giản.

Cấu hình dựa trên extension (IceRaven):

1) Nếu bạn đã sử dụng IceRaven, hãy cân nhắc xóa lịch sử duyệt web trước (Menu → History → Delete History). 2) Mở Menu → Add‑Ons → Add‑Ons Manager. 3) Cài đặt tiện ích mở rộng "I2P Proxy for Android and Other Systems". 4) Trình duyệt bây giờ sẽ proxy qua I2P.

Tiện ích mở rộng này cũng hoạt động trên các trình duyệt dựa trên Firefox phiên bản pre-Fenix nếu được cài đặt từ [AMO](https://addons.mozilla.org/en-US/android/addon/i2p-proxy/).

Việc bật hỗ trợ extension rộng rãi trong Firefox Nightly yêu cầu một quy trình riêng [được tài liệu hóa bởi Mozilla](https://blog.mozilla.org/addons/2020/09/29/expanded-extension-support-in-firefox-for-android-nightly/).

## Internet Explorer / Windows System Proxy

Trên Windows, hộp thoại proxy hệ thống áp dụng cho IE và có thể được sử dụng bởi các trình duyệt dựa trên Chromium khi chúng kế thừa cài đặt hệ thống.

1) Mở "Network and Internet Settings" → "Proxy". 2) Bật "Use a proxy server for your LAN". 3) Đặt địa chỉ `127.0.0.1`, cổng `4444` cho HTTP.. 4) Tùy chọn đánh dấu "Bypass proxy server for local addresses".
