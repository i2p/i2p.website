---
title: "Định dạng gói plugin"
description: "Quy tắc đóng gói .xpi2p / .su3 cho các plugin I2P"
slug: "plugin"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
---

## Tổng quan

Các plugin I2P là các gói lưu trữ đã được ký nhằm mở rộng chức năng của router. Chúng được phát hành dưới dạng tệp `.xpi2p` hoặc `.su3`, cài đặt vào `~/.i2p/plugins/<name>/` (hoặc `%APPDIR%\I2P\plugins\<name>\` trên Windows), và chạy với toàn bộ quyền của router, không có sandboxing (cơ chế cô lập).

### Các loại plugin được hỗ trợ

- Ứng dụng web của Bảng điều khiển
- Các eepsites mới có cgi-bin, ứng dụng web
- Chủ đề của Bảng điều khiển
- Bản dịch cho Bảng điều khiển
- Chương trình Java (chạy trong tiến trình hoặc JVM riêng)
- Kịch bản shell và tệp nhị phân gốc

### Mô hình bảo mật

**NGHIÊM TRỌNG:** Các plugin chạy trong cùng một JVM với các quyền giống hệt như I2P router. Chúng có quyền truy cập không hạn chế vào:
- Hệ thống tệp (đọc và ghi)
- API của router và trạng thái nội bộ
- Kết nối mạng
- Thực thi chương trình bên ngoài

Các plugin nên được coi là mã được tin cậy hoàn toàn. Người dùng phải xác minh nguồn phát hành và chữ ký số của plugin trước khi cài đặt.

---

## Định dạng tệp

### Định dạng SU3 (Rất khuyến nghị)

**Trạng thái:** Hoạt động, định dạng ưu tiên kể từ I2P 0.9.15 (Tháng 9 năm 2014)

Định dạng `.su3` cung cấp: - **Khóa ký RSA-4096** (so với DSA-1024 trong xpi2p) - Chữ ký được lưu trong phần đầu tệp - Số ma thuật (magic number): `I2Psu3` - Khả năng tương thích về sau tốt hơn

**Cấu trúc:**

```
[SU3 Header with RSA-4096 signature]
[ZIP Archive]
  ├── plugin.config (required)
  ├── console/
  ├── lib/
  ├── webapps/
  └── [other plugin files]
```
### Định dạng XPI2P (cũ, không còn được khuyến nghị)

**Trạng thái:** Được hỗ trợ vì lý do tương thích ngược, không khuyến nghị cho plugin mới

Định dạng `.xpi2p` sử dụng các chữ ký mật mã đời cũ: - **Chữ ký DSA-1024** (đã lỗi thời theo NIST-800-57) - Chữ ký DSA 40 byte được thêm vào đầu tệp ZIP - Yêu cầu trường `key` trong plugin.config

**Cấu trúc:**

```
[40-byte DSA signature]
[16-byte version string (UTF-8, zero-padded)]
[ZIP Archive]
```
**Lộ trình chuyển đổi:** Khi chuyển từ xpi2p sang su3, hãy cung cấp cả `updateURL` và `updateURL.su3` trong giai đoạn chuyển tiếp. Các router hiện đại (0.9.15+) sẽ tự động ưu tiên SU3.

---

## Bố cục gói nén và plugin.config

### Các tệp cần thiết

**plugin.config** - Tệp cấu hình I2P tiêu chuẩn với các cặp khóa-giá trị

### Thuộc tính bắt buộc

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Property</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Format</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>name</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Installation directory name, must match for updates</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Alphanumeric, no spaces</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>signer</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Developer contact information</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>user@mail.i2p</code> format recommended</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>version</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Plugin version for update comparison</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Max 16 bytes, parsed by VersionComparator</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>key</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">DSA public key (172 B64 chars ending with '=')</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Omit for SU3 format</strong></td></tr>
  </tbody>
</table>
**Ví dụ về định dạng phiên bản:** - `1.2.3` - `1.2.3-4` - `2.0.0-beta.1`

Các dấu phân cách hợp lệ: `.` (dấu chấm), `-` (dấu gạch ngang), `_` (dấu gạch dưới)

### Thuộc tính siêu dữ liệu tùy chọn

#### Hiển thị thông tin

- `date` - Ngày phát hành (dấu thời gian kiểu long của Java)
- `author` - Tên nhà phát triển (khuyến nghị `user@mail.i2p`)
- `description` - Mô tả bằng tiếng Anh
- `description_xx` - Mô tả bản địa hóa (xx = mã ngôn ngữ)
- `websiteURL` - Trang chủ plugin (`http://foo.i2p/`)
- `license` - Mã định danh giấy phép (ví dụ: "Apache-2.0", "GPL-3.0")

#### Cập nhật cấu hình

- `updateURL` - Địa chỉ cập nhật XPI2P (cũ)
- `updateURL.su3` - Địa chỉ cập nhật SU3 (được khuyến nghị)
- `min-i2p-version` - Phiên bản I2P tối thiểu bắt buộc
- `max-i2p-version` - Phiên bản I2P tương thích tối đa
- `min-java-version` - Phiên bản Java tối thiểu (ví dụ: `1.7`, `17`)
- `min-jetty-version` - Phiên bản Jetty tối thiểu (dùng `6` cho Jetty 6+)
- `max-jetty-version` - Phiên bản Jetty tối đa (dùng `5.99999` cho Jetty 5)

#### Hành vi cài đặt

- `dont-start-at-install` - Mặc định là `false`. Nếu `true`, yêu cầu khởi động thủ công
- `router-restart-required` - Mặc định là `false`. Thông báo cho người dùng rằng cần khởi động lại sau khi cập nhật
- `update-only` - Mặc định là `false`. Sẽ thất bại nếu plugin chưa được cài đặt
- `install-only` - Mặc định là `false`. Sẽ thất bại nếu plugin đã tồn tại
- `min-installed-version` - Phiên bản tối thiểu cần thiết để cập nhật
- `max-installed-version` - Phiên bản tối đa có thể được cập nhật
- `disableStop` - Mặc định là `false`. Ẩn nút dừng nếu `true`

#### Tích hợp bảng điều khiển

- `consoleLinkName` - Văn bản cho liên kết trên thanh tóm tắt của bảng điều khiển
- `consoleLinkName_xx` - Văn bản liên kết đã bản địa hóa (xx = mã ngôn ngữ)
- `consoleLinkURL` - Đích liên kết (ví dụ: `/appname/index.jsp`)
- `consoleLinkTooltip` - Văn bản gợi ý khi di chuột (được hỗ trợ từ 0.7.12-6)
- `consoleLinkTooltip_xx` - Chú giải đã bản địa hóa
- `console-icon` - Đường dẫn tới biểu tượng 32x32 (được hỗ trợ từ 0.9.20)
- `icon-code` - PNG 32x32 được mã hóa Base64 dành cho plugin không có tài nguyên web (từ 0.9.25)

#### Yêu cầu nền tảng (chỉ hiển thị)

- `required-platform-OS` - Yêu cầu hệ điều hành (không được áp dụng bắt buộc)
- `other-requirements` - Yêu cầu bổ sung (ví dụ: "Python 3.8+")

#### Quản lý phụ thuộc (Chưa được triển khai)

- `depends` - Các phụ thuộc của plugin, phân tách bằng dấu phẩy
- `depends-version` - Yêu cầu phiên bản đối với các phụ thuộc
- `langs` - Nội dung gói ngôn ngữ
- `type` - Loại plugin (app/theme/locale/webapp)

### Thay thế biến trong URL cập nhật

**Trạng thái tính năng:** Có sẵn từ I2P 1.7.0 (0.9.53)

Cả `updateURL` và `updateURL.su3` đều hỗ trợ các biến đặc thù theo nền tảng:

**Biến:** - `$OS` - Hệ điều hành: `windows`, `linux`, `mac` - `$ARCH` - Kiến trúc: `386`, `amd64`, `arm64`

**Ví dụ:**

```properties
updateURL.su3=http://foo.i2p/downloads/foo-$OS-$ARCH.su3
```
**Kết quả trên Windows AMD64:**

```
http://foo.i2p/downloads/foo-windows-amd64.su3
```
Điều này cho phép sử dụng một tệp plugin.config duy nhất cho các bản dựng dành riêng cho từng nền tảng.

---

## Cấu trúc thư mục

### Bố cục tiêu chuẩn

```
plugins/
└── pluginname/
    ├── plugin.config (required)
    ├── console/
    │   ├── locale/          # Translation JARs
    │   ├── themes/          # Console themes
    │   ├── webapps/         # Web applications
    │   └── webapps.config   # Webapp configuration
    ├── eepsite/
    │   ├── cgi-bin/
    │   ├── docroot/
    │   ├── logs/
    │   ├── webapps/
    │   └── jetty.xml
    ├── lib/
    │   └── *.jar            # Plugin libraries
    └── clients.config       # Client startup configuration
```
### Mục đích của thư mục

**console/locale/** - các tệp JAR chứa các gói tài nguyên cho các bản dịch cơ sở của I2P - các bản dịch dành riêng cho plugin nên đặt trong `console/webapps/*.war` hoặc `lib/*.jar`

**console/themes/** - Mỗi thư mục con chứa một chủ đề bảng điều khiển hoàn chỉnh - Tự động được thêm vào đường dẫn tìm kiếm chủ đề

**console/webapps/** - các tệp `.war` dùng để tích hợp với bảng điều khiển - Được khởi động tự động trừ khi bị vô hiệu hóa trong `webapps.config` - Tên WAR không nhất thiết phải trùng với tên plugin

**eepsite/** - eepsite hoàn chỉnh với một thể hiện Jetty riêng - Yêu cầu cấu hình `jetty.xml` với cơ chế thay thế biến - Xem các ví dụ plugin zzzot và pebble

**lib/** - Thư viện JAR của plugin - Chỉ định trong classpath (đường dẫn lớp) qua `clients.config` hoặc `webapps.config`

---

## Cấu hình ứng dụng web

### Định dạng webapps.config

Tệp cấu hình I2P tiêu chuẩn kiểm soát cách ứng dụng web hoạt động.

**Cú pháp:**

```properties
# Disable autostart
webapps.warname.startOnLoad=false

# Add classpath JARs (as of API 0.9.53, works for any warname)
webapps.warname.classpath=$PLUGIN/lib/foo.jar,$I2P/lib/bar.jar
```
**Lưu ý quan trọng:** - Trước router 0.7.12-9, hãy dùng `plugin.warname.startOnLoad` để tương thích - Trước API 0.9.53, classpath (đường dẫn lớp) chỉ hoạt động nếu warname trùng với tên plugin - Kể từ 0.9.53+, classpath hoạt động với bất kỳ tên webapp nào

### Thực tiễn tốt nhất cho ứng dụng web

1. **Triển khai ServletContextListener**
   - Triển khai `javax.servlet.ServletContextListener` để dọn dẹp tài nguyên
   - Hoặc ghi đè `destroy()` trong servlet
   - Đảm bảo tắt đúng cách trong quá trình cập nhật và khi router dừng

2. **Quản lý thư viện**
   - Đặt các JAR dùng chung vào `lib/`, không nằm trong WAR
   - Tham chiếu thông qua classpath của `webapps.config`
   - Cho phép cài đặt/cập nhật plugin tách biệt

3. **Tránh xung đột thư viện**
   - Không bao giờ đóng gói kèm các JAR của Jetty, Tomcat hoặc servlet
   - Không bao giờ đóng gói kèm các JAR từ bản cài đặt I2P tiêu chuẩn
   - Kiểm tra phần classpath cho các thư viện tiêu chuẩn

4. **Yêu cầu biên dịch**
   - Không bao gồm các tệp mã nguồn `.java` hoặc `.jsp`
   - Biên dịch trước tất cả các JSP để tránh chậm trễ khi khởi động
   - Không thể giả định sự sẵn có của trình biên dịch Java/JSP

5. **Khả năng tương thích Servlet API**
   - I2P hỗ trợ Servlet 3.0 (từ 0.9.30)
   - **Không hỗ trợ quét Annotation (chú thích)** (@WebContent)
   - Phải cung cấp tệp mô tả triển khai `web.xml` theo kiểu truyền thống

6. **Phiên bản Jetty**
   - Hiện tại: Jetty 9 (I2P 0.9.30+)
   - Sử dụng `net.i2p.jetty.JettyStart` để trừu tượng hóa
   - Bảo vệ trước các thay đổi Jetty API

---

## Cấu hình máy khách

### Định dạng clients.config

Xác định các máy khách (dịch vụ) được khởi chạy cùng plugin.

**Máy khách cơ bản:**

```properties
clientApp.0.main=com.example.PluginMain
clientApp.0.name=Example Plugin Service
clientApp.0.delay=30
clientApp.0.args=arg1 arg2 $PLUGIN/config.properties
```
**Ứng dụng khách có Dừng/Gỡ cài đặt:**

```properties
clientApp.0.stopargs=stop
clientApp.0.uninstallargs=uninstall
clientApp.0.classpath=$PLUGIN/lib/plugin.jar,$I2P/lib/i2p.jar
```
### Tham khảo thuộc tính

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Property</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>main</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Fully qualified class name implementing ClientApp interface</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>name</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Display name for user interface</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>delay</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Startup delay in seconds (default: 0)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>args</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Space-separated arguments passed to constructor</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>stopargs</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Arguments for shutdown (must handle gracefully)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>uninstallargs</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Arguments called before plugin deletion</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>classpath</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Comma-separated JAR paths</td></tr>
  </tbody>
</table>
### Thay thế biến

Các biến sau được thay thế trong `args`, `stopargs`, `uninstallargs` và `classpath`:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Variable</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Replacement</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>$I2P</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">I2P base installation directory</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>$CONFIG</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">I2P configuration directory (typically <code>~/.i2p</code>)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>$PLUGIN</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">This plugin's directory (<code>$CONFIG/plugins/name</code>)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>$OS</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Operating system: <code>windows</code>, <code>linux</code>, <code>mac</code></td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>$ARCH</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Architecture: <code>386</code>, <code>amd64</code>, <code>arm64</code></td></tr>
  </tbody>
</table>
### Máy khách được quản lý so với máy khách không được quản lý

**Các client được quản lý (Khuyến nghị, từ 0.9.4):** - Được khởi tạo bởi ClientAppManager (trình quản lý ứng dụng khách) - Duy trì tham chiếu và theo dõi trạng thái - Quản lý vòng đời dễ dàng hơn - Quản lý bộ nhớ tốt hơn

**Các ứng dụng khách không được quản lý:** - Được khởi động bởi router, không theo dõi trạng thái - Phải xử lý nhiều lần gọi start/stop một cách ổn thỏa - Sử dụng trạng thái tĩnh hoặc tệp PID (định danh tiến trình) để điều phối - Được gọi khi router tắt (as of 0.7.12-3)

### ShellService (kể từ phiên bản 0.9.53 / 1.7.0)

Giải pháp tổng quát để chạy các chương trình bên ngoài với khả năng theo dõi trạng thái tự động.

**Tính năng:** - Quản lý vòng đời tiến trình - Giao tiếp với ClientAppManager - Quản lý PID tự động - Hỗ trợ đa nền tảng

**Cách sử dụng:**

```properties
clientApp.0.main=net.i2p.apps.ShellService
clientApp.0.args=$PLUGIN/bin/myservice.sh
```
Đối với các tập lệnh dành riêng cho từng nền tảng:

```properties
clientApp.0.args=$PLUGIN/bin/myservice-$OS.$ARCH
```
**Phương án thay thế (kiểu cũ):** Viết Java wrapper (trình bao) kiểm tra loại hệ điều hành, gọi `ShellCommand` với tệp `.bat` hoặc `.sh` phù hợp.

---

## Quy trình cài đặt

### Luồng cài đặt dành cho người dùng

1. Người dùng dán URL plugin vào Trang cấu hình Plugin của Router Console (`/configplugins`)
2. Router tải xuống tệp plugin
3. Xác minh chữ ký (thất bại nếu khóa chưa biết và chế độ nghiêm ngặt được bật)
4. Kiểm tra tính toàn vẹn ZIP
5. Giải nén và phân tích `plugin.config`
6. Xác minh tương thích phiên bản (`min-i2p-version`, `min-java-version`, v.v.)
7. Phát hiện xung đột tên ứng dụng web
8. Dừng plugin hiện có khi cập nhật
9. Xác thực thư mục (phải nằm dưới `plugins/`)
10. Giải nén toàn bộ tệp vào thư mục plugin
11. Cập nhật `plugins.config`
12. Khởi động plugin (trừ khi `dont-start-at-install=true`)

### Bảo mật và Tin cậy

**Quản lý khóa:** - Mô hình tin cậy 'first-key-seen' (tin cậy theo khóa được thấy đầu tiên) cho người ký mới - Chỉ có các khóa jrandom và zzz được đóng gói sẵn - Kể từ 0.9.14.1, các khóa không xác định bị từ chối theo mặc định - Một thuộc tính nâng cao có thể ghi đè cho mục đích phát triển

**Hạn chế cài đặt:** - Các gói nén chỉ được giải nén vào thư mục plugin - Trình cài đặt từ chối các đường dẫn bên ngoài `plugins/` - Các plugin có thể truy cập tệp ở nơi khác sau khi cài đặt - Không có sandboxing (cô lập môi trường chạy) hoặc cô lập đặc quyền

---

## Cơ chế cập nhật

### Quy trình kiểm tra cập nhật

1. Router đọc `updateURL.su3` (ưu tiên) hoặc `updateURL` từ plugin.config
2. Yêu cầu HTTP HEAD hoặc GET một phần để lấy các byte 41-56
3. Trích xuất chuỗi phiên bản từ tệp từ xa
4. So sánh với phiên bản đã cài đặt bằng VersionComparator (bộ so sánh phiên bản)
5. Nếu mới hơn, nhắc người dùng hoặc tự động tải xuống (dựa trên cài đặt)
6. Dừng plugin
7. Cài đặt bản cập nhật
8. Khởi động plugin (trừ khi tùy chọn của người dùng đã thay đổi)

### So sánh phiên bản

Các phiên bản được phân tích dưới dạng các thành phần tách nhau bằng dấu chấm/gạch ngang/gạch dưới: - `1.2.3` < `1.2.4` - `1.2.3` < `1.2.3-1` - `2.0.0` > `1.9.9`

**Độ dài tối đa:** 16 byte (phải khớp với phần đầu SUD/SU3)

### Phương pháp hay nhất khi cập nhật

1. Luôn tăng phiên bản khi phát hành
2. Kiểm thử lộ trình cập nhật từ phiên bản trước đó
3. Cân nhắc `router-restart-required` cho các thay đổi lớn
4. Cung cấp cả `updateURL` và `updateURL.su3` trong quá trình chuyển đổi
5. Sử dụng hậu tố số bản dựng để kiểm thử (`1.2.3-456`)

---

## Classpath (đường dẫn lớp) và Thư viện Chuẩn

### Luôn có sẵn trong Classpath (danh sách đường dẫn lớp)

Các tệp JAR sau từ `$I2P/lib` luôn có trong classpath (đường dẫn lớp) cho I2P 0.9.30+:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">JAR</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Plugin Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>i2p.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Core API</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Required for all plugins</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>mstreaming.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Streaming API</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Most plugins need</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>streaming.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Streaming implementation</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Most plugins need</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>i2ptunnel.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">I2PTunnel</td><td style="border:1px solid var(--color-border); padding:0.6rem;">HTTP/server plugins</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>router.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Router internals</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Rarely needed, avoid if possible</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>javax.servlet.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Servlet 3.1, JSP 2.3 API</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Plugins with servlets/JSPs</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>jasper-runtime.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Jasper compiler/runtime</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Plugins with JSPs</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>commons-el.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">EL 3.0 API</td><td style="border:1px solid var(--color-border); padding:0.6rem;">JSPs using expression language</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>jetty-i2p.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Jetty utilities</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Plugins starting Jetty</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>org.mortbay.jetty.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Jetty 9 base</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Custom Jetty instances</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>sam.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">SAM API</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Rarely needed</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>addressbook.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Subscription/blockfile</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Use NamingService instead</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>routerconsole.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Console libraries</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Not public API, avoid</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>jbigi.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Native crypto</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Plugins should not need</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>systray.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">URL launcher</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Rarely needed</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>wrapper.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Service wrapper</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Plugins should not need</td></tr>
  </tbody>
</table>
### Ghi chú đặc biệt

**commons-logging.jar:** - Trống kể từ 0.9.30 - Trước 0.9.30: Apache Tomcat JULI - Trước 0.9.24: Commons Logging + JULI - Trước 0.9: Chỉ Commons Logging

**jasper-compiler.jar:** - Trống kể từ Jetty 6 (0.9)

**systray4j.jar:** - Đã được loại bỏ từ 0.9.26

### Không có trong Classpath (đường dẫn lớp của Java) (Phải chỉ định)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">JAR</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>jstl.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Standard Taglib</td><td style="border:1px solid var(--color-border); padding:0.6rem;">JSP tag libraries</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>standard.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Standard Taglib</td><td style="border:1px solid var(--color-border); padding:0.6rem;">JSP tag libraries</td></tr>
  </tbody>
</table>
### Đặc tả Classpath (đường dẫn lớp)

**Trong clients.config:**

```properties
clientApp.0.classpath=$PLUGIN/lib/mylib.jar,$I2P/lib/i2p.jar
```
**Trong webapps.config:**

```properties
webapps.mywebapp.classpath=$PLUGIN/lib/mylib.jar,$I2P/lib/jstl.jar
```
**Quan trọng:** Kể từ 0.7.13-3, các classpath (đường dẫn lớp) là riêng cho từng luồng, không mang tính toàn cục trên JVM (Máy ảo Java). Hãy chỉ định classpath đầy đủ cho từng client.

---

## Yêu cầu về phiên bản Java

### Các yêu cầu hiện tại (Tháng 10 năm 2025)

**I2P 2.10.0 và các phiên bản trước:** - Tối thiểu: Java 7 (bắt buộc kể từ 0.9.24, tháng 1 năm 2016) - Khuyến nghị: Java 8 hoặc cao hơn

**I2P 2.11.0 và các phiên bản sau (SẮP RA MẮT):** - **Tối thiểu: Java 17+** (được công bố trong ghi chú phát hành 2.9.0) - Đã đưa ra cảnh báo trước hai bản phát hành (2.9.0 → 2.10.0 → 2.11.0)

### Chiến lược Tương thích Plugin

**Để có khả năng tương thích tối đa (tới I2P 2.10.x):**

```xml
<javac source="1.7" target="1.7" />
```
```properties
min-java-version=1.7
```
**Đối với các tính năng Java 8+:**

```xml
<javac source="1.8" target="1.8" />
```
```properties
min-java-version=1.8
```
**Đối với các tính năng của Java 11+:**

```xml
<javac source="11" target="11" />
```
```properties
min-java-version=11
```
**Chuẩn bị cho 2.11.0+:**

```xml
<javac source="17" target="17" />
```
```properties
min-java-version=17
min-i2p-version=2.11.0
```
### Thực tiễn tốt nhất về biên dịch

**Khi biên dịch với JDK mới cho mục tiêu cũ hơn:**

```xml
<javac source="1.7" target="1.7" 
       bootclasspath="${java7.home}/jre/lib/rt.jar"
       includeantruntime="false" />
```
Điều này ngăn việc sử dụng các API không có sẵn trong phiên bản Java mục tiêu.

---

## Nén Pack200 - ĐÃ LỖI THỜI

### Cập nhật quan trọng: Không sử dụng Pack200

**Trạng thái:** ĐÃ NGỪNG HỖ TRỢ VÀ ĐÃ GỠ BỎ

Đặc tả ban đầu đã khuyến nghị mạnh mẽ việc nén Pack200 để giảm kích thước 60-65%. **Điều này không còn áp dụng nữa.**

**Dòng thời gian:** - **JEP 336:** Pack200 được đánh dấu ngừng sử dụng trong Java 11 (Tháng 9 năm 2018) - **JEP 367:** Pack200 bị gỡ bỏ trong Java 14 (Tháng 3 năm 2020)

**Đặc tả Cập nhật I2P chính thức nêu rõ:** > "Các tệp JAR và WAR trong gói zip không còn được nén bằng pack200 như đã mô tả ở trên cho các tệp 'su2', vì các runtime Java (môi trường chạy Java) gần đây không còn hỗ trợ pack200."

**Cần làm gì:**

1. **Loại bỏ pack200 khỏi quy trình build ngay lập tức**
2. **Sử dụng nén ZIP tiêu chuẩn**
3. **Cân nhắc các lựa chọn thay thế:**
   - ProGuard/R8 để thu gọn mã
   - UPX cho các tệp nhị phân native
   - Các thuật toán nén hiện đại (zstd, brotli) nếu có cung cấp bộ giải nén tùy chỉnh

**Đối với plugin hiện có:** - Các router cũ (0.7.11-5 đến Java 10) vẫn có thể giải nén pack200 (định dạng nén JAR của Java) - Các router mới (Java 11+) không thể giải nén pack200 - Phát hành lại plugin không dùng nén pack200

---

## Khóa ký và bảo mật

### Sinh khóa (định dạng SU3)

Sử dụng tập lệnh `makeplugin.sh` từ kho lưu trữ i2p.scripts:

```bash
# Generate new signing key
./makeplugin.sh keygen

# Keys stored in ~/.i2p-plugin-keys/
```
**Thông tin chính:** - Thuật toán: RSA_SHA512_4096 - Định dạng: chứng chỉ X.509 - Lưu trữ: định dạng Java keystore

### Ký phần bổ trợ

```bash
# Create signed su3 file
./makeplugin.sh sign myplugin.zip myplugin.su3 keyname

# Verify signature
./makeplugin.sh verify myplugin.su3
```
### Các thực tiễn tốt nhất về quản lý khóa

1. **Tạo một lần, bảo vệ mãi mãi**
   - Routers từ chối các tên khóa trùng lặp với các khóa khác nhau
   - Routers từ chối các khóa trùng lặp với các tên khóa khác nhau
   - Các bản cập nhật bị từ chối nếu khóa/tên không khớp

2. **Lưu trữ an toàn**
   - Sao lưu keystore (kho khóa) một cách an toàn
   - Sử dụng cụm từ mật khẩu mạnh
   - Không bao giờ commit vào hệ thống quản lý phiên bản

3. **Xoay vòng khóa**
   - Không được hỗ trợ bởi kiến trúc hiện tại
   - Lập kế hoạch cho việc sử dụng khóa dài hạn
   - Cân nhắc các lược đồ đa chữ ký cho phát triển theo nhóm

### Ký số DSA kiểu cũ (XPI2P)

**Trạng thái:** Hoạt động nhưng đã lỗi thời

Chữ ký DSA-1024 được dùng trong định dạng xpi2p: - chữ ký dài 40 byte - khóa công khai dài 172 ký tự base64 - NIST-800-57 khuyến nghị tối thiểu (L=2048, N=224) - I2P sử dụng mức yếu hơn (L=1024, N=160)

**Khuyến nghị:** Thay vào đó, hãy sử dụng SU3 (định dạng gói cập nhật có chữ ký của I2P) với RSA-4096 (khóa RSA 4096-bit).

---

## Hướng dẫn phát triển Plugin (phần bổ trợ)

### Các thực hành tốt nhất thiết yếu

1. **Tài liệu**
   - Cung cấp README rõ ràng kèm hướng dẫn cài đặt
   - Tài liệu hóa các tùy chọn cấu hình và giá trị mặc định
   - Bao gồm nhật ký thay đổi cho mỗi bản phát hành
   - Chỉ định các phiên bản I2P/Java yêu cầu

2. **Tối ưu hóa dung lượng**
   - Chỉ bao gồm các tệp cần thiết
   - Không bao giờ đóng gói kèm các JAR của router
   - Tách biệt gói cài đặt và gói cập nhật (thư viện trong lib/)
   - ~~Sử dụng nén Pack200~~ **LỖI THỜI - Sử dụng ZIP tiêu chuẩn**

3. **Cấu hình**
   - Không bao giờ chỉnh sửa `plugin.config` trong lúc chạy
   - Sử dụng tệp cấu hình riêng cho các thiết lập khi chạy
   - Tài liệu hóa các cấu hình bắt buộc của router (cổng SAM, tunnels, v.v.)
   - Tôn trọng cấu hình hiện có của người dùng

4. **Sử dụng tài nguyên**
   - Tránh mức tiêu thụ băng thông mặc định quá mức
   - Áp dụng giới hạn sử dụng CPU hợp lý
   - Giải phóng tài nguyên khi tắt ứng dụng
   - Sử dụng luồng daemon khi thích hợp

5. **Kiểm thử**
   - Kiểm thử cài đặt/nâng cấp/gỡ cài đặt trên tất cả các nền tảng
   - Kiểm thử cập nhật từ phiên bản trước
   - Xác minh ứng dụng web dừng/khởi động lại trong quá trình cập nhật
   - Kiểm thử với phiên bản I2P được hỗ trợ tối thiểu

6. **Hệ thống tệp**
   - Không bao giờ ghi vào `$I2P` (có thể chỉ đọc)
   - Ghi dữ liệu thời gian chạy vào `$PLUGIN` hoặc `$CONFIG`
   - Sử dụng `I2PAppContext` để phát hiện vị trí thư mục
   - Không giả định vị trí của `$CWD`

7. **Tương thích**
   - Không trùng lặp các lớp I2P chuẩn
   - Mở rộng các lớp khi cần, đừng thay thế
   - Kiểm tra `min-i2p-version`, `min-jetty-version` trong plugin.config
   - Kiểm thử với các phiên bản I2P cũ hơn nếu có hỗ trợ chúng

8. **Xử lý tắt**
   - Thiết lập `stopargs` phù hợp trong clients.config
   - Đăng ký shutdown hooks (móc gọi khi tắt): `I2PAppContext.addShutdownTask()`
   - Xử lý nhiều lần gọi khởi động/dừng một cách an toàn
   - Đặt tất cả các luồng sang chế độ daemon (tiến trình nền)

9. **Bảo mật**
   - Xác thực mọi đầu vào từ bên ngoài
   - Không bao giờ gọi `System.exit()`
   - Tôn trọng quyền riêng tư của người dùng
   - Tuân theo các thực hành lập trình an toàn

10. **Giấy phép**
    - Nêu rõ ràng giấy phép của plugin
    - Tuân thủ các giấy phép của những thư viện được đóng gói kèm
    - Bao gồm phần ghi công bắt buộc
    - Cung cấp quyền truy cập mã nguồn nếu được yêu cầu

### Các cân nhắc nâng cao

**Xử lý múi giờ:** - Router đặt múi giờ JVM thành UTC - Múi giờ thực tế của người dùng: thuộc tính `i2p.systemTimeZone` trong `I2PAppContext`

**Khám phá thư mục:**

```java
// Plugin directory
String pluginDir = I2PAppContext.getGlobalContext()
    .getAppDir().getAbsolutePath() + "/plugins/" + pluginName;

// Or use $PLUGIN variable in clients.config args
```
**Đánh số phiên bản:** - Sử dụng phiên bản theo ngữ nghĩa (major.minor.patch) - Thêm số build phục vụ thử nghiệm (1.2.3-456) - Đảm bảo số phiên bản tăng đơn điệu qua các lần cập nhật

**Truy cập lớp router:** - Nói chung nên tránh phụ thuộc vào `router.jar` - Thay vào đó, hãy dùng các API công khai trong `i2p.jar` - Trong tương lai, I2P có thể hạn chế quyền truy cập lớp router

**Ngăn ngừa sự cố JVM (trước đây):** - Đã sửa trong 0.7.13-3 - Sử dụng class loader (bộ nạp lớp) đúng cách - Tránh cập nhật các tệp JAR trong phần bổ trợ đang chạy - Thiết kế để khởi động lại khi cập nhật nếu cần thiết

---

## Các phần bổ trợ cho Eepsite

### Tổng quan

Các plugin có thể cung cấp các eepsites hoàn chỉnh với các thể hiện Jetty (máy chủ web) và I2PTunnel riêng của mình.

### Kiến trúc

**Không được cố gắng:** - Cài đặt vào eepsite hiện có - Hợp nhất với eepsite mặc định của router - Giả định chỉ có một eepsite khả dụng

**Thay vào đó:** - Khởi chạy một thể hiện I2PTunnel mới (thông qua CLI (giao diện dòng lệnh)) - Khởi chạy một thể hiện Jetty mới - Cấu hình cả hai trong `clients.config`

### Cấu trúc ví dụ

```
plugins/myeepsite/
├── plugin.config
├── clients.config          # Starts Jetty + I2PTunnel
├── eepsite/
│   ├── jetty.xml          # Requires variable substitution
│   ├── docroot/
│   ├── webapps/
│   └── logs/
└── lib/
    └── [dependencies]
```
### Thay thế biến trong jetty.xml

Sử dụng biến `$PLUGIN` cho các đường dẫn:

```xml
<Set name="resourceBase">$PLUGIN/eepsite/docroot</Set>
```
Router thực hiện việc thay thế trong quá trình khởi động plugin.

### Ví dụ

Các triển khai tham chiếu: - **zzzot plugin** - Trình theo dõi torrent - **pebble plugin** - Nền tảng blog

Cả hai đều có tại trang plugin của zzz (I2P-internal).

---

## Tích hợp Bảng điều khiển

### Các liên kết trên Thanh tóm tắt

Thêm liên kết có thể nhấp vào thanh tóm tắt của bảng điều khiển router:

```properties
consoleLinkName=My Plugin
consoleLinkURL=/myplugin/
consoleLinkTooltip=Open My Plugin Interface
```
Các phiên bản đã được bản địa hóa:

```properties
consoleLinkName_de=Mein Plugin
consoleLinkTooltip_de=Öffne Mein Plugin Schnittstelle
```
### Biểu tượng bảng điều khiển

**Tệp ảnh (kể từ 0.9.20):**

```properties
console-icon=/myicon.png
```
Đường dẫn tương đối so với `consoleLinkURL` nếu được chỉ định (kể từ 0.9.53), nếu không thì tương đối so với tên ứng dụng web.

**Biểu tượng nhúng (từ 0.9.25):**

```properties
icon-code=iVBORw0KGgoAAAANSUhEUgAAA...Base64EncodedPNG...
```
Tạo bằng:

```bash
base64 -w 0 icon-32x32.png
```
Hoặc Java:

```bash
java -cp i2p.jar net.i2p.data.Base64 encode icon.png
```
Yêu cầu: - 32x32 điểm ảnh - Định dạng PNG - Mã hóa Base64 (không ngắt dòng)

---

## Quốc tế hóa

### Gói dịch thuật

**Đối với bản dịch cơ sở của I2P:** - Đặt các tệp JAR vào `console/locale/` - Bao gồm các gói tài nguyên cho các ứng dụng I2P hiện có - Quy ước đặt tên: `messages_xx.properties` (xx = mã ngôn ngữ)

**Đối với bản dịch dành riêng cho plugin:** - Bao gồm trong `console/webapps/*.war` - Hoặc bao gồm trong `lib/*.jar` - Sử dụng cách tiếp cận ResourceBundle chuẩn của Java

### Chuỗi bản địa hóa trong plugin.config

```properties
description=My awesome plugin
description_de=Mein tolles Plugin
description_fr=Mon plugin génial
description_es=Mi plugin increíble
```
Các trường được hỗ trợ: - `description_xx` - `consoleLinkName_xx` - `consoleLinkTooltip_xx`

### Dịch chủ đề bảng điều khiển

Các chủ đề trong `console/themes/` được tự động thêm vào đường dẫn tìm kiếm chủ đề.

---

## Các plugin dành riêng cho nền tảng

### Cách tiếp cận các gói tách biệt

Sử dụng các tên plugin khác nhau cho từng nền tảng:

```properties
# Windows package
name=myplugin-windows

# Linux package  
name=myplugin-linux

# macOS package
name=myplugin-mac
```
### Cách tiếp cận thay thế biến

Một plugin.config duy nhất với các biến theo nền tảng:

```properties
name=myplugin
updateURL.su3=http://myplugin.i2p/downloads/myplugin-$OS-$ARCH.su3
```
Trong clients.config:

```properties
clientApp.0.main=net.i2p.apps.ShellService
clientApp.0.args=$PLUGIN/bin/myapp-$OS-$ARCH
```
### Phát hiện hệ điều hành trong thời gian chạy

Cách tiếp cận trong Java cho việc thực thi có điều kiện:

```java
String os = System.getProperty("os.name").toLowerCase();
if (os.contains("win")) {
    // Windows-specific code
} else if (os.contains("nix") || os.contains("nux")) {
    // Linux-specific code
} else if (os.contains("mac")) {
    // macOS-specific code
}
```
---

## Khắc phục sự cố

### Các vấn đề thường gặp

**Plugin không khởi động:** 1. Kiểm tra khả năng tương thích phiên bản I2P (`min-i2p-version`) 2. Xác minh phiên bản Java (`min-java-version`) 3. Kiểm tra nhật ký router để tìm lỗi 4. Xác minh tất cả các JAR bắt buộc trong classpath (đường dẫn lớp)

**Webapp không thể truy cập:** 1. Xác nhận `webapps.config` không vô hiệu hóa webapp 2. Kiểm tra khả năng tương thích phiên bản Jetty (`min-jetty-version`) 3. Đảm bảo có `web.xml` (không hỗ trợ quét annotation (chú thích)) 4. Kiểm tra xung đột tên webapp

**Cập nhật thất bại:** 1. Xác minh chuỗi phiên bản đã tăng 2. Kiểm tra chữ ký khớp với khóa ký 3. Đảm bảo tên plugin khớp với phiên bản đã cài đặt 4. Xem lại cài đặt `update-only`/`install-only`

**Chương trình bên ngoài không dừng:** 1. Dùng ShellService để quản lý vòng đời tự động 2. Triển khai xử lý `stopargs` đúng cách 3. Kiểm tra việc dọn dẹp tệp PID 4. Xác minh việc kết thúc tiến trình

### Ghi nhật ký gỡ lỗi

Kích hoạt ghi nhật ký gỡ lỗi trong router:

```
logger.record.net.i2p.router.web.ConfigPluginsHandler=DEBUG
```
Kiểm tra nhật ký:

```
~/.i2p/logs/log-router-0.txt
```
---

## Thông tin tham khảo

### Đặc tả chính thức

- [Đặc tả Plugin](/docs/specs/plugin/)
- [Định dạng cấu hình](/docs/specs/configuration/)
- [Đặc tả cập nhật](/docs/specs/updates/)
- [Mật mã học](/docs/specs/cryptography/)

### Lịch sử phiên bản I2P

**Bản phát hành hiện tại:** - **I2P 2.10.0** (8 tháng 9 năm 2025)

**Các bản phát hành lớn kể từ 0.9.53:** - 2.10.0 (Thg 9 2025) - thông báo Java 17+ - 2.9.0 (Thg 6 2025) - cảnh báo Java 17+ - 2.8.0 (Thg 10 2024) - thử nghiệm mật mã hậu lượng tử - 2.6.0 (Thg 5 2024) - chặn I2P-over-Tor - 2.4.0 (Thg 12 2023) - cải thiện bảo mật NetDB - 2.2.0 (Thg 3 2023) - điều khiển tắc nghẽn - 2.1.0 (Thg 1 2023) - cải thiện mạng - 2.0.0 (Thg 11 2022) - giao thức truyền tải SSU2 - 1.7.0/0.9.53 (Thg 2 2022) - ShellService, thay thế biến - 0.9.15 (Thg 9 2014) - giới thiệu định dạng SU3

**Đánh số phiên bản:** - Dòng 0.9.x: Đến hết phiên bản 0.9.53 - Dòng 2.x: Bắt đầu từ 2.0.0 (giới thiệu SSU2)

### Tài nguyên cho nhà phát triển

**Mã nguồn:** - Kho lưu trữ chính: https://i2pgit.org/I2P_Developers/i2p.i2p - GitHub mirror (bản sao): https://github.com/i2p/i2p.i2p

**Ví dụ plugin:** - zzzot (trình theo dõi BitTorrent) - pebble (nền tảng blog) - i2p-bote (email không máy chủ) - orchid (trình khách Tor) - seedless (trao đổi ngang hàng)

**Công cụ build:** - makeplugin.sh - Sinh khóa và ký - Có trong kho i2p.scripts - Tự động hóa việc tạo và xác minh su3

### Hỗ trợ cộng đồng

**Diễn đàn:** - [I2P Forum](https://i2pforum.net/) - [zzz.i2p](http://zzz.i2p/) (nội bộ I2P)

**IRC/Trò chuyện:** - #i2p-dev trên OFTC - I2P IRC trong mạng

---

## Phụ lục A: Ví dụ plugin.config hoàn chỉnh

```properties
# Required fields
name=example-plugin
signer=developer@mail.i2p
version=1.2.3

# Update configuration
updateURL.su3=http://example.i2p/plugins/example-$OS-$ARCH.su3
min-i2p-version=2.0.0
min-java-version=17

# Display information
date=1698796800000
author=Example Developer <developer@mail.i2p>
websiteURL=http://example.i2p/
license=Apache-2.0

description=An example I2P plugin demonstrating best practices
description_de=Ein Beispiel-I2P-Plugin zur Demonstration bewährter Praktiken
description_es=Un plugin I2P de ejemplo que demuestra las mejores prácticas

# Console integration
consoleLinkName=Example Plugin
consoleLinkName_de=Beispiel-Plugin
consoleLinkURL=/example/
consoleLinkTooltip=Open the Example Plugin control panel
consoleLinkTooltip_de=Öffne das Beispiel-Plugin-Kontrollfeld
console-icon=/icon.png

# Installation behavior
dont-start-at-install=false
router-restart-required=false

# Platform requirements (informational)
required-platform-OS=All platforms supported
other-requirements=Requires 512MB free disk space
```
---

## Phụ lục B: Ví dụ clients.config hoàn chỉnh

```properties
# Main service client (managed)
clientApp.0.main=com.example.plugin.MainService
clientApp.0.name=Example Plugin Main Service
clientApp.0.delay=30
clientApp.0.args=$PLUGIN/config.properties --port=7656
clientApp.0.stopargs=shutdown
clientApp.0.uninstallargs=cleanup
clientApp.0.classpath=$PLUGIN/lib/example.jar,$I2P/lib/i2p.jar,$I2P/lib/mstreaming.jar

# External program via ShellService
clientApp.1.main=net.i2p.apps.ShellService
clientApp.1.name=Example Native Helper
clientApp.1.delay=35
clientApp.1.args=$PLUGIN/bin/helper-$OS-$ARCH --config $PLUGIN/helper.conf
clientApp.1.classpath=$I2P/lib/i2p.jar

# Jetty eepsite
clientApp.2.main=net.i2p.jetty.JettyStart
clientApp.2.name=Example Eepsite
clientApp.2.delay=40
clientApp.2.args=$PLUGIN/eepsite/jetty.xml
clientApp.2.stopargs=$PLUGIN/eepsite/jetty.xml stop
clientApp.2.classpath=$PLUGIN/lib/example-web.jar,$I2P/lib/i2p.jar

# I2PTunnel for eepsite
clientApp.3.main=net.i2p.i2ptunnel.TunnelControllerGroup
clientApp.3.name=Example Eepsite Tunnel
clientApp.3.delay=45
clientApp.3.args=$PLUGIN/eepsite/i2ptunnel.config
```
---

## Phụ lục C: Ví dụ webapps.config đầy đủ

```properties
# Disable autostart for admin webapp
webapps.example-admin.startOnLoad=false

# Main webapp with classpath
webapps.example.startOnLoad=true
webapps.example.classpath=$PLUGIN/lib/example-core.jar,$PLUGIN/lib/commons-utils.jar,$I2P/lib/jstl.jar,$I2P/lib/standard.jar

# Legacy support (pre-0.7.12-9)
plugin.example.startOnLoad=true
```
---

## Phụ lục D: Danh sách kiểm tra chuyển đổi (0.9.53 đến 2.10.0)

### Các thay đổi bắt buộc

- [ ] **Loại bỏ nén Pack200 khỏi quy trình xây dựng**
  - Loại bỏ các tác vụ pack200 khỏi các tập lệnh Ant/Maven/Gradle
  - Phát hành lại các plugin hiện có mà không dùng pack200

- [ ] **Rà soát các yêu cầu về phiên bản Java**
  - Cân nhắc yêu cầu Java 11+ cho các tính năng mới
  - Lên kế hoạch cho yêu cầu Java 17+ trong I2P 2.11.0
  - Cập nhật `min-java-version` trong plugin.config

- [ ] **Cập nhật tài liệu**
  - Loại bỏ các tham chiếu tới Pack200
  - Cập nhật yêu cầu phiên bản Java
  - Cập nhật các tham chiếu phiên bản I2P (0.9.x → 2.x)

### Các thay đổi được khuyến nghị

- [ ] **Tăng cường chữ ký số**
  - Chuyển đổi từ XPI2P sang SU3 nếu chưa thực hiện
  - Sử dụng khóa RSA-4096 cho các plugin mới

- [ ] **Tận dụng các tính năng mới (nếu dùng 0.9.53+)**
  - Sử dụng biến `$OS` / `$ARCH` cho các cập nhật dành riêng cho nền tảng
  - Sử dụng ShellService (dịch vụ Shell) cho các chương trình bên ngoài
  - Sử dụng classpath của webapp đã được cải tiến (hoạt động với bất kỳ warname (tên WAR) nào)

- [ ] **Kiểm tra khả năng tương thích**
  - Kiểm tra trên I2P 2.10.0
  - Xác minh với Java 8, 11, 17
  - Kiểm tra trên Windows, Linux, macOS

### Các cải tiến tùy chọn

- [ ] Triển khai đúng cách ServletContextListener (trình lắng nghe ngữ cảnh Servlet)
- [ ] Thêm mô tả được bản địa hóa
- [ ] Cung cấp biểu tượng cho bảng điều khiển
- [ ] Cải thiện xử lý khi tắt
- [ ] Thêm ghi nhật ký toàn diện
- [ ] Viết các bài kiểm thử tự động
