---
title: "Tạo một Eepsite trên I2P"
description: "Tìm hiểu cách tạo và tự lưu trữ trang web của riêng bạn trên mạng I2P bằng máy chủ web Jetty tích hợp sẵn"
lastUpdated: "2025-11"
toc: true
---

## Eepsite là gì?

Một **eepsite** (trang web chỉ hoạt động trong mạng I2P) là một trang web tồn tại duy nhất trên mạng I2P. Không giống các trang web truyền thống có thể truy cập qua Internet công khai, các eepsite chỉ có thể truy cập thông qua I2P, mang lại tính ẩn danh và quyền riêng tư cho cả người vận hành trang lẫn khách truy cập. Các eepsite sử dụng miền cấp cao giả `.i2p` và được truy cập thông qua các địa chỉ `.b32.i2p` đặc biệt hoặc các tên dễ đọc được đăng ký trong sổ địa chỉ I2P.

Tất cả các bản triển khai Java I2P đi kèm với [Jetty](https://jetty.org/index.html), một máy chủ web nhẹ dựa trên Java, được cài đặt sẵn và cấu hình sẵn. Điều này giúp bạn dễ dàng bắt đầu lưu trữ eepsite của riêng bạn trong vài phút - không cần cài đặt thêm phần mềm nào.

Hướng dẫn này sẽ dẫn bạn từng bước qua quy trình tạo và cấu hình eepsite đầu tiên của bạn bằng các công cụ tích hợp sẵn của I2P.

---

## Bước 1: Truy cập Trình quản lý dịch vụ ẩn

Hidden Services Manager (trình quản lý Dịch vụ Ẩn; còn được gọi là I2P Tunnel Manager) là nơi bạn cấu hình tất cả các tunnel máy chủ và máy khách của I2P, bao gồm cả các máy chủ HTTP (eepsites).

1. Mở [Bảng điều khiển I2P Router](http://127.0.0.1:7657)
2. Đi tới [Trình quản lý Dịch vụ Ẩn](http://127.0.0.1:7657/i2ptunnelmgr)

Bạn sẽ thấy giao diện Trình quản lý Dịch vụ ẩn hiển thị: - **Thông báo trạng thái** - Trạng thái tunnel và máy khách hiện tại - **Điều khiển tunnel toàn cục** - Các nút để quản lý tất cả tunnel cùng lúc - **Dịch vụ ẩn I2P** - Danh sách các tunnel máy chủ đã cấu hình

![Trình quản lý dịch vụ ẩn](/images/guides/eepsite/hidden-services-manager.png)

Theo mặc định, bạn sẽ thấy một mục **máy chủ web I2P** hiện có đã được cấu hình nhưng chưa được khởi động. Đây là máy chủ web Jetty được cấu hình sẵn, sẵn sàng để bạn sử dụng.

---

## Bước 2: Cấu hình các thiết lập máy chủ Eepsite của bạn

Nhấp vào mục **I2P webserver** trong danh sách Hidden Services để mở trang cấu hình máy chủ. Tại đây bạn sẽ tùy chỉnh các thiết lập cho eepsite (trang web trên I2P) của mình.

![Cài đặt máy chủ Eepsite](/images/guides/eepsite/webserver-settings.png)

### Giải thích các tùy chọn cấu hình

**Tên** - Đây là một định danh nội bộ cho tunnel của bạn - Hữu ích nếu bạn đang chạy nhiều eepsites để dễ phân biệt cái nào với cái nào - Mặc định: "I2P webserver"

**Mô tả** - Một mô tả ngắn gọn về eepsite của bạn để bạn tự tham khảo - Chỉ hiển thị cho bạn trong Hidden Services Manager (Trình quản lý Dịch vụ Ẩn) - Ví dụ: "eepsite của tôi" hoặc "blog cá nhân"

**Tự động khởi động Tunnel** - **Quan trọng**: Đánh dấu vào ô này để tự động khởi động eepsite của bạn khi router I2P khởi động - Đảm bảo trang của bạn vẫn truy cập được mà không cần can thiệp thủ công sau khi router khởi động lại - Khuyến nghị: **Bật**

**Đích (Host và Port)** - **Host**: Địa chỉ cục bộ nơi máy chủ web của bạn đang chạy (mặc định: `127.0.0.1`) - **Port**: Cổng mà máy chủ web của bạn lắng nghe (mặc định: `7658` cho Jetty) - Nếu bạn đang sử dụng máy chủ web Jetty được cài sẵn, **hãy giữ nguyên các giá trị mặc định này** - Chỉ thay đổi nếu bạn đang chạy một máy chủ web tùy chỉnh trên một cổng khác

**Tên máy chủ trang web** - Đây là tên miền `.i2p` dễ đọc của eepsite của bạn - Mặc định: `mysite.i2p` (giá trị giữ chỗ) - Bạn có thể đăng ký một tên miền tùy chỉnh như `stormycloud.i2p` hoặc `myblog.i2p` - Để trống nếu bạn chỉ muốn dùng địa chỉ `.b32.i2p` được tạo tự động (cho outproxy (proxy ra)) - Xem [Đăng ký tên miền I2P của bạn](#registering-your-i2p-domain) bên dưới để biết cách yêu cầu một tên máy chủ tùy chỉnh

**Đích cục bộ** - Đây là mã định danh mật mã (địa chỉ đích) duy nhất của eepsite của bạn - Được tự động tạo khi tunnel được tạo lần đầu - Hãy coi đây như "địa chỉ IP" cố định của trang bạn trên I2P - Chuỗi chữ-số dài chính là địa chỉ `.b32.i2p` của trang bạn ở dạng mã hóa

**Tệp khóa riêng** - Vị trí lưu trữ các khóa riêng của eepsite của bạn - Mặc định: `eepsite/eepPriv.dat` - **Bảo mật tệp này** - bất kỳ ai có quyền truy cập vào tệp này đều có thể mạo danh eepsite của bạn - Không bao giờ chia sẻ hoặc xóa tệp này

### Lưu ý quan trọng

Hộp cảnh báo màu vàng nhắc bạn rằng để kích hoạt các tính năng tạo mã QR hoặc xác thực đăng ký, bạn phải cấu hình Tên máy chủ trang web với hậu tố `.i2p` (ví dụ, `mynewsite.i2p`).

---

## Bước 3: Các tùy chọn mạng nâng cao (Không bắt buộc)

Nếu bạn cuộn xuống trong trang cấu hình, bạn sẽ thấy các tùy chọn mạng nâng cao. **Những cài đặt này là không bắt buộc** - các thiết lập mặc định hoạt động tốt với đa số người dùng. Tuy nhiên, bạn có thể điều chỉnh chúng dựa trên yêu cầu bảo mật và nhu cầu hiệu suất của mình.

### Các tùy chọn độ dài Tunnel

![Tùy chọn độ dài và số lượng tunnel](/images/guides/eepsite/tunnel-options.png)

**Độ dài tunnel** - **Mặc định**: tunnel 3 bước nhảy (mức ẩn danh cao) - Kiểm soát số bước nhảy qua các router mà một yêu cầu phải đi qua trước khi đến eepsite của bạn - **Nhiều bước nhảy hơn = Mức ẩn danh cao hơn, nhưng hiệu năng chậm hơn** - **Ít bước nhảy hơn = Hiệu năng nhanh hơn, nhưng mức ẩn danh giảm** - Các tùy chọn trong khoảng 0-3 bước nhảy với cài đặt độ biến thiên - **Khuyến nghị**: Giữ ở 3 bước nhảy trừ khi bạn có yêu cầu hiệu năng cụ thể

**Độ biến thiên tunnel** - **Mặc định**: độ biến thiên 0 chặng (không ngẫu nhiên hóa, hiệu năng ổn định) - Thêm ngẫu nhiên hóa vào độ dài tunnel để tăng cường bảo mật - Ví dụ: "độ biến thiên 0-1 chặng" nghĩa là các tunnel sẽ ngẫu nhiên dài 3 hoặc 4 chặng - Tăng tính khó dự đoán nhưng có thể khiến thời gian tải không nhất quán

### Tùy chọn số lượng Tunnel

**Số lượng (tunnels vào/ra)** - **Mặc định**: 2 tunnel vào, 2 tunnel ra (băng thông và độ tin cậy tiêu chuẩn) - Kiểm soát số lượng tunnel (đường hầm ẩn danh trong I2P) song song được dành riêng cho eepsite của bạn - **Nhiều tunnel hơn = Khả dụng và xử lý tải tốt hơn, nhưng sử dụng tài nguyên cao hơn** - **Ít tunnel hơn = Sử dụng tài nguyên thấp hơn, nhưng giảm khả năng dự phòng** - Khuyến nghị cho đa số người dùng: 2/2 (mặc định) - Các eepsite lưu lượng cao có thể hưởng lợi từ 3/3 hoặc cao hơn

**Số lượng dự phòng** - **Mặc định**: 0 tunnels dự phòng (không dự phòng, không tăng sử dụng tài nguyên) - Các tunnels chờ sẽ được kích hoạt nếu các tunnels chính bị lỗi - Tăng độ tin cậy nhưng tiêu tốn nhiều băng thông và CPU hơn - Hầu hết eepsites cá nhân không cần tunnels dự phòng

### Giới hạn POST

![Cấu hình giới hạn POST](/images/guides/eepsite/post-limits.png)

Nếu eepsite của bạn bao gồm các biểu mẫu (biểu mẫu liên hệ, mục bình luận, tải lên tệp, v.v.), bạn có thể cấu hình các giới hạn đối với các yêu cầu POST để ngăn chặn lạm dụng:

**Giới hạn theo từng máy khách** - **Mỗi khoảng thời gian**: Số lượng yêu cầu tối đa từ một máy khách (mặc định: 6 trong mỗi 5 phút) - **Thời gian cấm**: Thời gian chặn máy khách lạm dụng (mặc định: 20 phút)

**Giới hạn tổng** - **Tổng**: Số lượng yêu cầu POST tối đa từ tất cả các máy khách cộng lại (mặc định: 20 mỗi 5 phút) - **Thời gian cấm**: Thời gian từ chối tất cả yêu cầu POST nếu vượt quá giới hạn (mặc định: 10 phút)

**Khoảng thời gian giới hạn POST** - Cửa sổ thời gian để đo tần suất yêu cầu (mặc định: 5 phút)

Những giới hạn này giúp bảo vệ chống lại thư rác, các cuộc tấn công từ chối dịch vụ và lạm dụng việc gửi biểu mẫu tự động.

### Khi nào nên điều chỉnh cài đặt nâng cao

- **Trang cộng đồng có lưu lượng truy cập cao**: Tăng số lượng tunnel (3-4 inbound/outbound)
- **Ứng dụng nhạy cảm về hiệu năng**: Giảm độ dài tunnel xuống 2 hops (chặng) (đánh đổi quyền riêng tư)
- **Cần ẩn danh tối đa**: Giữ 3 hops, thêm 0-1 variance (độ biến thiên)
- **Biểu mẫu với mức sử dụng cao chính đáng**: Tăng giới hạn POST tương ứng
- **Blog/hồ sơ năng lực cá nhân**: Dùng tất cả giá trị mặc định

---

## Bước 4: Thêm nội dung vào Eepsite của bạn

Bây giờ eepsite của bạn đã được cấu hình, bạn cần thêm các tệp trang web (HTML, CSS, hình ảnh, v.v.) vào thư mục gốc tài liệu (document root) của máy chủ web. Vị trí này thay đổi tùy theo hệ điều hành, loại cài đặt và bản triển khai I2P của bạn.

### Tìm thư mục gốc tài liệu của bạn

**Thư mục gốc của website** (thường gọi là `docroot`) là thư mục nơi bạn đặt toàn bộ tệp của website. Tệp `index.html` của bạn nên đặt trực tiếp trong thư mục này.

#### Java I2P (Bản phân phối tiêu chuẩn)

**Linux** - **Cài đặt tiêu chuẩn**: `~/.i2p/eepsite/docroot/` - **Cài đặt bằng gói (chạy như dịch vụ)**: `/var/lib/i2p/i2p-config/eepsite/docroot/`

**Windows** - **Cài đặt tiêu chuẩn**: `%LOCALAPPDATA%\I2P\eepsite\docroot\`   - Đường dẫn điển hình: `C:\Users\YourUsername\AppData\Local\I2P\eepsite\docroot\` - **Cài đặt dưới dạng dịch vụ Windows**: `%PROGRAMDATA%\I2P\eepsite\docroot\`   - Đường dẫn điển hình: `C:\ProgramData\I2P\eepsite\docroot\`

**macOS** - **Cài đặt tiêu chuẩn**: `/Users/YourUsername/Library/Application Support/i2p/eepsite/docroot/`

#### I2P+ (Bản phân phối I2P nâng cao)

I2P+ sử dụng cùng một cấu trúc thư mục như Java I2P. Hãy làm theo các đường dẫn ở trên tùy theo hệ điều hành của bạn.

#### i2pd (Hiện thực bằng C++)

**Linux/Unix** - **Mặc định**: `/var/lib/i2pd/eepsite/` hoặc `~/.i2pd/eepsite/` - Kiểm tra tệp cấu hình `i2pd.conf` của bạn để biết thiết lập `root` thực tế trong phần tunnel máy chủ HTTP của bạn

**Windows** - Kiểm tra `i2pd.conf` trong thư mục cài đặt i2pd của bạn

**macOS** - Thông thường: `~/Library/Application Support/i2pd/eepsite/`

### Thêm các tệp trang web của bạn

1. **Đi tới thư mục gốc của website (document root)** bằng trình quản lý tệp hoặc terminal
2. **Tạo hoặc sao chép các tệp trang web của bạn** vào thư mục `docroot`
   - Tối thiểu, hãy tạo một tệp `index.html` (đây là trang chủ của bạn)
   - Thêm CSS, JavaScript, hình ảnh và các tài nguyên khác khi cần
3. **Sắp xếp các thư mục con** như bạn vẫn làm với bất kỳ trang web nào:
   ```
   docroot/
   ├── index.html
   ├── about.html
   ├── css/
   │   └── style.css
   ├── images/
   │   └── logo.png
   └── js/
       └── script.js
   ```

### Bắt đầu nhanh: Ví dụ HTML đơn giản

Nếu bạn chỉ mới bắt đầu, hãy tạo một tệp `index.html` cơ bản trong thư mục `docroot` của bạn:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My I2P Eepsite</title>
</head>
<body>
    <h1>Welcome to My Eepsite!</h1>
    <p>This is my first website on the I2P network.</p>
    <p>Privacy-focused and decentralized!</p>
</body>
</html>
```
### Quyền (Linux/Unix/macOS)

Nếu bạn chạy I2P như một dịch vụ hoặc dưới một tài khoản người dùng khác, hãy đảm bảo tiến trình I2P có quyền đọc các tệp của bạn:

```bash
# Set appropriate ownership (if running as i2p user)
sudo chown -R i2p:i2p /var/lib/i2p/i2p-config/eepsite/docroot/

# Or set readable permissions for all users
chmod -R 755 ~/.i2p/eepsite/docroot/
```
### Mẹo

- **Nội dung mặc định**: Khi bạn cài đặt I2P lần đầu, đã có sẵn nội dung mẫu trong thư mục `docroot` - bạn cứ thoải mái thay thế nó
- **Trang tĩnh hoạt động tốt nhất**: Mặc dù Jetty hỗ trợ các servlet và JSP, các trang HTML/CSS/JavaScript đơn giản là dễ bảo trì nhất
- **Máy chủ web bên ngoài**: Người dùng nâng cao có thể chạy các máy chủ web tùy chỉnh (Apache, Nginx, Node.js, v.v.) trên các cổng khác nhau và trỏ I2P tunnel tới chúng

---

## Bước 5: Khởi chạy Eepsite của bạn

Bây giờ eepsite (trang web ẩn trên mạng I2P) của bạn đã được cấu hình và có nội dung, đã đến lúc khởi chạy nó và làm cho nó có thể truy cập trên mạng I2P.

### Khởi động Tunnel

1. **Quay lại [Trình quản lý Dịch vụ Ẩn](http://127.0.0.1:7657/i2ptunnelmgr)**
2. Tìm mục **I2P webserver** của bạn trong danh sách
3. Nhấp nút **Start** trong cột Control

![Đang chạy eepsite](/images/guides/eepsite/eepsite-running.png)

### Chờ thiết lập Tunnel

Sau khi nhấp Start, eepsite tunnel của bạn sẽ bắt đầu được xây dựng. Quá trình này thường mất **30-60 giây**. Hãy theo dõi chỉ báo trạng thái:

- **Đèn đỏ** = Tunnel đang khởi động/xây dựng
- **Đèn vàng** = Tunnel được thiết lập một phần
- **Đèn xanh** = Tunnel hoạt động hoàn toàn và sẵn sàng

Ngay khi bạn thấy **đèn xanh**, eepsite của bạn đã hoạt động trên mạng I2P!

### Truy cập Eepsite của bạn

Nhấp vào nút **Preview** bên cạnh eepsite đang chạy của bạn. Thao tác này sẽ mở một thẻ trình duyệt mới tới địa chỉ eepsite của bạn.

eepsite của bạn có hai loại địa chỉ:

1. **Địa chỉ Base32 (.b32.i2p)**: Một địa chỉ mật mã dài trông như sau:
   ```
   http://fcyianvr325tdgiiueyg4rsq4r5iuibzovl26msox5ryoselykpq.b32.i2p
   ```
   - Đây là địa chỉ vĩnh viễn của eepsite của bạn, được dẫn xuất bằng mật mã
   - Không thể thay đổi và gắn liền với khóa riêng của bạn
   - Luôn hoạt động, ngay cả khi không đăng ký tên miền

2. **Tên miền dễ đọc (.i2p)**: Nếu bạn đặt một tên máy chủ website (ví dụ: `testwebsite.i2p`)
   - Chỉ hoạt động sau khi đăng ký tên miền (xem phần tiếp theo)
   - Dễ nhớ và chia sẻ hơn
   - Ánh xạ tới địa chỉ .b32.i2p của bạn

Nút **Copy Hostname** cho phép bạn nhanh chóng sao chép địa chỉ `.b32.i2p` đầy đủ của mình để chia sẻ.

---

## ⚠️ Cực kỳ quan trọng: Sao lưu khóa riêng của bạn

Trước khi tiếp tục, bạn **phải sao lưu** tệp khóa riêng của eepsite của bạn. Điều này cực kỳ quan trọng vì một số lý do:

### Tại sao bạn cần sao lưu khóa của mình?

**Khóa riêng (`eepPriv.dat`) của bạn là định danh eepsite của bạn.** Nó xác định địa chỉ `.b32.i2p` của bạn và chứng minh quyền sở hữu eepsite của bạn.

- **Khóa = địa chỉ .b32**: Khóa riêng của bạn tạo (về mặt toán học) địa chỉ .b32.i2p duy nhất của bạn
- **Không thể khôi phục**: Nếu bạn mất khóa, bạn sẽ mất vĩnh viễn địa chỉ eepsite của mình
- **Không thể thay đổi**: Nếu bạn đã đăng ký một tên miền trỏ tới một địa chỉ .b32, **không có cách nào để cập nhật nó** - việc đăng ký là vĩnh viễn
- **Cần thiết cho việc di chuyển**: Chuyển sang máy tính mới hoặc cài đặt lại I2P cần khóa này để giữ nguyên địa chỉ
- **Hỗ trợ multihoming (đa địa điểm)**: Chạy eepsite của bạn từ nhiều địa điểm yêu cầu cùng một khóa trên mỗi máy chủ

### Khóa riêng ở đâu?

Theo mặc định, khóa riêng của bạn được lưu tại: - **Linux**: `~/.i2p/eepsite/eepPriv.dat` (hoặc `/var/lib/i2p/i2p-config/eepsite/eepPriv.dat` dành cho cài đặt dưới dạng dịch vụ) - **Windows**: `%LOCALAPPDATA%\I2P\eepsite\eepPriv.dat` hoặc `%PROGRAMDATA%\I2P\eepsite\eepPriv.dat` - **macOS**: `/Users/YourUsername/Library/Application Support/i2p/eepsite/eepPriv.dat`

Bạn cũng có thể kiểm tra/thay đổi đường dẫn này trong cấu hình tunnel (đường hầm) của bạn, dưới mục "Private Key File".

### Cách sao lưu

1. **Dừng tunnel của bạn** (tùy chọn, nhưng an toàn hơn)
2. **Sao chép `eepPriv.dat`** vào một vị trí an toàn:
   - Ổ USB ngoài
   - Ổ sao lưu được mã hóa
   - Tệp lưu trữ được bảo vệ bằng mật khẩu
   - Lưu trữ đám mây an toàn (được mã hóa)
3. **Giữ nhiều bản sao lưu** ở các vị trí vật lý khác nhau
4. **Không bao giờ chia sẻ tệp này** - bất kỳ ai có nó đều có thể mạo danh eepsite của bạn

### Khôi phục từ bản sao lưu

Để khôi phục eepsite của bạn trên một hệ thống mới hoặc sau khi cài đặt lại:

1. Cài đặt I2P và tạo/cấu hình các thiết lập tunnel của bạn
2. **Dừng tunnel** trước khi sao chép khóa
3. Sao chép `eepPriv.dat` đã sao lưu của bạn đến đúng vị trí
4. Khởi động tunnel - nó sẽ sử dụng địa chỉ .b32 gốc của bạn

---

## Nếu bạn không đăng ký tên miền

**Chúc mừng!** Nếu bạn không dự định đăng ký một tên miền `.i2p` tùy chỉnh, eepsite của bạn hiện đã hoàn tất và đang hoạt động.

Bạn có thể: - Chia sẻ địa chỉ `.b32.i2p` của bạn với người khác - Truy cập trang web của bạn qua mạng I2P bằng bất kỳ trình duyệt hỗ trợ I2P nào - Cập nhật các tệp trang web của bạn trong thư mục `docroot` bất cứ lúc nào - Giám sát trạng thái tunnel của bạn trong Hidden Services Manager (Trình quản lý Dịch vụ Ẩn)

**Nếu bạn muốn một tên miền dễ đọc** (như `mysite.i2p` thay vì một địa chỉ .b32 dài), hãy tiếp tục đến phần tiếp theo.

---

## Đăng ký tên miền I2P của bạn

Một tên miền `.i2p` dễ đọc (như `testwebsite.i2p`) dễ nhớ và chia sẻ hơn nhiều so với một địa chỉ `.b32.i2p` dài. Việc đăng ký tên miền là miễn phí và liên kết tên bạn chọn với địa chỉ mật mã của eepsite (trang web trên I2P) của bạn.

### Điều kiện tiên quyết

- eepsite của bạn phải đang chạy với đèn báo màu xanh lá
- Bạn phải đặt **Website Hostname** trong cấu hình tunnel của bạn (Bước 2)
- Ví dụ: `testwebsite.i2p` hoặc `myblog.i2p`

### Bước 1: Tạo chuỗi xác thực

1. **Quay lại cấu hình tunnel của bạn** trong Trình quản lý Dịch vụ Ẩn
2. Nhấp vào mục **máy chủ web I2P** của bạn để mở phần cài đặt
3. Cuộn xuống để tìm nút **Xác thực đăng ký**

![Xác thực đăng ký](/images/guides/eepsite/registration-authentication.png)

4. Nhấp vào **Registration Authentication**
5. **Sao chép toàn bộ chuỗi xác thực** được hiển thị cho "Authentication for adding host [yourdomainhere]"

Chuỗi xác thực sẽ trông như sau:

```
testwebsite.i2p=I8WiuSx1TcYAutCrhLveZ6gghdqsIJ1v9noSGPb7ItYjxaK5LHVNxgC60KuEu95nqCCF2qwgnW~2ehIY9vsi1iPForksdU3GALrQq4S73meoIIXarCCdb~Z6Ehj2-yLWI8WiuSx1TcYAutCrhLveZ6gghdqsIJ1v9noSGPb7ItYjxaK5LHVNxgC60KuEu95nqCCF2qwgnW~2ehIY9vsi1iPForksdU3GALrQq4S73meoIIXarCCdb~Z6Ehj2-yLWI8WiuSx1TcYAutCrhLveZ6gghdqsIJ1v9noSGPb7ItYjxaK5LHVNxgC60KuEu95nqCCF2qwgnW~2ehIY9vsi1iPForksdU3GALrQq4S73meoIIXarCCdb~Z6Ehj2-yLWI8WiuSx1TcYAutCrhLveZ6gghdqsIJ1v9noSGPb7ItYjxaK5LHVNxgC60KuEu95nqCCF2qwgnW~2ehIY9vsi1uNxFZ0HN7tQbbVj1pmbahepQZNxEW0ufwnMYAoFo8opBQAEAAcAAA==#!date=1762104890#sig=9DjEfrcNRxsoSxiE0Mp0-7rH~ktYWtgwU8c4J0eSo0VHbGxDxdiO9D1Cvwcx8hkherMO07UWOC9BWf-1wRyUAw==
```
Chuỗi này chứa: - Tên miền của bạn (`testwebsite.i2p`) - Địa chỉ đích của bạn (định danh mật mã dài) - Dấu thời gian - Chữ ký số chứng minh bạn sở hữu khóa riêng

**Giữ chuỗi xác thực này** - bạn sẽ cần nó cho cả hai dịch vụ đăng ký.

### Bước 2: Đăng ký với stats.i2p

1. **Truy cập** [stats.i2p Thêm khóa](http://stats.i2p/i2p/addkey.html) (trong I2P)

![Đăng ký tên miền stats.i2p](/images/guides/eepsite/stats-i2p-add.png)

2. **Dán chuỗi xác thực** vào trường "Authentication String"
3. **Thêm tên của bạn** (tùy chọn) - mặc định là "Anonymous"
4. **Thêm mô tả** (khuyến nghị) - mô tả ngắn gọn về nội dung eepsite của bạn
   - Ví dụ: "New I2P Eepsite", "Blog cá nhân", "Dịch vụ chia sẻ tệp"
5. **Chọn "HTTP Service?"** nếu đây là một website (giữ nguyên ở trạng thái đã chọn đối với hầu hết các eepsite)
   - Bỏ chọn đối với IRC, NNTP, các proxy, XMPP, git, v.v.
6. Nhấp **Submit**

Nếu thành công, bạn sẽ thấy một thông báo xác nhận rằng tên miền của bạn đã được thêm vào sổ địa chỉ của stats.i2p.

### Bước 3: Đăng ký với reg.i2p

Để đảm bảo tính sẵn sàng tối đa, bạn cũng nên đăng ký với dịch vụ reg.i2p:

1. **Đi tới** [reg.i2p Thêm miền](http://reg.i2p/add) (trong I2P)

![Đăng ký tên miền reg.i2p](/images/guides/eepsite/reg-i2p-add.png)

2. **Dán cùng một chuỗi xác thực** vào trường "Auth string"
3. **Thêm mô tả** (tùy chọn nhưng được khuyến nghị)
   - Điều này giúp những người dùng I2P khác hiểu trang web của bạn cung cấp gì
4. Nhấp **Submit**

Bạn sẽ nhận được xác nhận rằng tên miền của bạn đã được đăng ký.

### Bước 4: Chờ lan truyền

Sau khi gửi tới cả hai dịch vụ, việc đăng ký tên miền của bạn sẽ được lan truyền thông qua hệ thống sổ địa chỉ của mạng I2P.

**Mốc thời gian lan truyền**: - **Đăng ký ban đầu**: Ngay lập tức trên các dịch vụ đăng ký - **Phổ biến trên toàn mạng**: Vài giờ đến 24 giờ hoặc hơn - **Khả dụng đầy đủ**: Có thể mất tới 48 giờ để tất cả các router được cập nhật

**Đây là điều bình thường!** Hệ thống sổ địa chỉ I2P được cập nhật định kỳ, không phải ngay lập tức. eepsite của bạn đang hoạt động - những người dùng khác chỉ cần nhận được sổ địa chỉ đã cập nhật.

### Xác minh tên miền của bạn

Sau vài giờ, bạn có thể kiểm tra tên miền của mình:

1. **Mở một thẻ trình duyệt mới** trong trình duyệt I2P của bạn
2. Hãy thử truy cập trực tiếp tên miền của bạn: `http://yourdomainname.i2p`
3. Nếu tải được, tên miền của bạn đã được đăng ký và đang được lan truyền!

Nếu vẫn chưa hoạt động: - Chờ lâu hơn (các danh bạ địa chỉ tự cập nhật theo lịch riêng) - Danh bạ địa chỉ trên router của bạn có thể cần thời gian để đồng bộ - Hãy thử khởi động lại I2P router để buộc cập nhật danh bạ địa chỉ

### Lưu ý quan trọng

- **Đăng ký là vĩnh viễn**: Khi đã đăng ký và được lan truyền, miền của bạn sẽ trỏ vĩnh viễn tới địa chỉ `.b32.i2p` của bạn
- **Không thể thay đổi điểm đích**: Bạn không thể cập nhật địa chỉ `.b32.i2p` mà miền của bạn trỏ tới - đó là lý do việc sao lưu `eepPriv.dat` là tối quan trọng
- **Quyền sở hữu miền**: Chỉ người nắm giữ khóa riêng mới có thể đăng ký hoặc cập nhật miền
- **Dịch vụ miễn phí**: Việc đăng ký miền trên I2P là miễn phí, do cộng đồng vận hành và phi tập trung
- **Nhiều nhà đăng ký**: Đăng ký với cả stats.i2p và reg.i2p giúp tăng độ tin cậy và tốc độ lan truyền

---

## Chúc mừng!

Eepsite I2P của bạn hiện đã hoạt động đầy đủ với một tên miền đã được đăng ký!

**Các bước tiếp theo**: - Thêm nhiều nội dung hơn vào thư mục `docroot` của bạn - Chia sẻ tên miền của bạn với cộng đồng I2P - Giữ bản sao lưu `eepPriv.dat` của bạn an toàn - Theo dõi trạng thái tunnel (đường hầm ẩn danh của I2P) của bạn thường xuyên - Cân nhắc tham gia các diễn đàn I2P hoặc IRC để quảng bá trang web của bạn

Chào mừng đến với mạng I2P! 🎉
