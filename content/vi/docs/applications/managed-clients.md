---
title: "Các Client Được Quản Lý"
description: "Cách các ứng dụng được quản lý bởi router tích hợp với ClientAppManager và port mapper"
slug: "managed-clients"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## 1. Tổng quan

Các mục trong [`clients.config`](/docs/specs/configuration/#clients-config) chỉ định cho router những ứng dụng nào sẽ được khởi chạy khi khởi động. Mỗi mục có thể chạy dưới dạng client **được quản lý** (managed) (được khuyến nghị) hoặc client **không được quản lý** (unmanaged). Các managed client phối hợp với `ClientAppManager`, công cụ này:

- Khởi tạo ứng dụng và theo dõi trạng thái vòng đời của router console
- Cung cấp các điều khiển start/stop cho người dùng và đảm bảo tắt sạch khi thoát router
- Lưu trữ một **client registry** nhẹ và **port mapper** để các ứng dụng có thể khám phá dịch vụ của nhau

Client không được quản lý chỉ đơn giản gọi một phương thức `main()`; chỉ sử dụng chúng cho mã nguồn cũ không thể được hiện đại hóa.

## 2. Triển khai Managed Client

Các managed client phải implement `net.i2p.app.ClientApp` (cho các ứng dụng hướng người dùng) hoặc `net.i2p.router.app.RouterApp` (cho các phần mở rộng của router). Cung cấp một trong các constructor bên dưới để manager có thể truyền các tham số context và configuration:

```java
public MyClientApp(I2PAppContext context, ClientAppManager manager, String[] args)
```
```java
public MyRouterApp(RouterContext context, ClientAppManager manager, String[] args)
```
Mảng `args` chứa các giá trị được cấu hình trong `clients.config` hoặc các tệp riêng lẻ trong `clients.config.d/`. Mở rộng các lớp trợ giúp `ClientApp` / `RouterApp` khi có thể để kế thừa các kết nối vòng đời mặc định.

### 2.1 Lifecycle Methods

Các client được quản lý được kỳ vọng triển khai:

- `startup()` - thực hiện khởi tạo và trả về nhanh chóng. Phải gọi `manager.notify()` ít nhất một lần để chuyển từ trạng thái INITIALIZED.
- `shutdown(String[] args)` - giải phóng tài nguyên và dừng các luồng chạy nền. Phải gọi `manager.notify()` ít nhất một lần để thay đổi trạng thái sang STOPPING hoặc STOPPED.
- `getState()` - thông báo cho console biết ứng dụng đang chạy, đang khởi động, đang dừng, hay đã thất bại

Trình quản lý gọi các phương thức này khi người dùng tương tác với console.

### 2.2 Advantages

- Báo cáo trạng thái chính xác trong bảng điều khiển router
- Khởi động lại sạch sẽ mà không rò rỉ luồng (thread) hoặc tham chiếu tĩnh
- Dung lượng bộ nhớ thấp hơn sau khi ứng dụng dừng
- Tập trung ghi nhật ký và báo cáo lỗi thông qua ngữ cảnh được tiêm vào

## 3. Unmanaged Clients (Fallback Mode)

Nếu class được cấu hình không implement một interface được quản lý, router sẽ khởi chạy nó bằng cách gọi `main(String[] args)` và không thể theo dõi process kết quả. Console hiển thị thông tin hạn chế và shutdown hooks có thể không chạy. Dành chế độ này cho các script hoặc tiện ích sử dụng một lần không thể áp dụng các API được quản lý.

## 4. Client Registry

Các client được quản lý và không được quản lý có thể tự đăng ký với manager để các thành phần khác có thể truy xuất tham chiếu theo tên:

```java
manager.register(this);
```
Việc đăng ký sử dụng giá trị trả về từ `getName()` của client làm khóa registry. Các đăng ký đã biết bao gồm `console`, `i2ptunnel`, `Jetty`, `outproxy`, và `update`. Truy xuất một client bằng `ClientAppManager.getRegisteredApp(String name)` để phối hợp các tính năng (ví dụ, console truy vấn Jetty để lấy chi tiết trạng thái).

Lưu ý rằng client registry và port mapper là hai hệ thống riêng biệt. Client registry cho phép giao tiếp giữa các ứng dụng thông qua tra cứu tên, trong khi port mapper ánh xạ tên dịch vụ tới các tổ hợp host:port để khám phá dịch vụ.

## 3. Clients Không Quản Lý (Chế Độ Dự Phòng)

Port mapper cung cấp một thư mục đơn giản cho các dịch vụ TCP nội bộ. Đăng ký các cổng loopback để người cộng tác tránh các địa chỉ được mã hóa cứng:

```java
context.portMapper().register(PortMapper.SVC_HTTPS_PROXY, 4445);
```
Hoặc với chỉ định host tường minh:

```java
context.portMapper().register(PortMapper.SVC_HTTP_PROXY, "127.0.0.1", 4444);
```
Tra cứu dịch vụ bằng `PortMapper.getPort(String name)` (trả về -1 nếu không tìm thấy) hoặc `getPort(String name, int defaultPort)` (trả về giá trị mặc định nếu không tìm thấy). Kiểm tra trạng thái đăng ký với `isRegistered(String name)` và lấy host đã đăng ký bằng `getActualHost(String name)`.

Các hằng số dịch vụ port mapper phổ biến từ `net.i2p.util.PortMapper`:

- `SVC_CONSOLE` - Bảng điều khiển router (cổng mặc định 7657)
- `SVC_HTTP_PROXY` - HTTP proxy (cổng mặc định 4444)
- `SVC_HTTPS_PROXY` - HTTPS proxy (cổng mặc định 4445)
- `SVC_I2PTUNNEL` - Trình quản lý I2PTunnel
- `SVC_SAM` - Cầu nối SAM (cổng mặc định 7656)
- `SVC_SAM_SSL` - Cầu nối SAM SSL
- `SVC_SAM_UDP` - SAM UDP
- `SVC_BOB` - Cầu nối BOB (cổng mặc định 2827)
- `SVC_EEPSITE` - Eepsite tiêu chuẩn (cổng mặc định 7658)
- `SVC_HTTPS_EEPSITE` - HTTPS eepsite
- `SVC_IRC` - Tunnel IRC (cổng mặc định 6668)
- `SVC_SUSIDNS` - SusiDNS

Lưu ý: `httpclient`, `httpsclient`, và `httpbidirclient` là các loại tunnel của i2ptunnel (được sử dụng trong cấu hình `tunnel.N.type`), không phải hằng số dịch vụ port mapper.

## 4. Registry Client

### 2.1 Các Phương Thức Vòng Đời

Từ phiên bản 0.9.42, router hỗ trợ tách cấu hình thành các file riêng lẻ trong thư mục `clients.config.d/`. Mỗi file chứa các thuộc tính cho một client duy nhất với tất cả thuộc tính có tiền tố `clientApp.0.`:

```
clientApp.0.main=net.i2p.router.web.RouterConsoleRunner
clientApp.0.name=Router Console
clientApp.0.args=7657 ::1,127.0.0.1 ./webapps/
clientApp.0.delay=0
clientApp.0.onBoot=true
```
Đây là phương pháp được khuyến nghị cho các cài đặt và plugin mới.

### 2.2 Ưu điểm

Để tương thích ngược, định dạng truyền thống sử dụng đánh số tuần tự:

```
clientApp.0.main=net.i2p.router.web.RouterConsoleRunner
clientApp.0.name=Router Console
clientApp.0.args=7657 ::1,127.0.0.1 ./webapps/
clientApp.1.main=net.i2p.apps.systray.UrlLauncher
clientApp.1.name=URL Launcher
clientApp.1.delay=5
```
### 6.3 Configuration Properties

**Bắt buộc:** - `main` - Tên đầy đủ của class triển khai ClientApp hoặc RouterApp, hoặc chứa method static `main(String[] args)`

**Tùy chọn:** - `name` - Tên hiển thị cho router console (mặc định là tên class) - `args` - Các tham số phân cách bằng dấu cách hoặc tab (hỗ trợ chuỗi trong dấu ngoặc kép) - `delay` - Số giây trước khi khởi động (mặc định 120) - `onBoot` - Buộc `delay=0` nếu là true - `startOnLoad` - Bật/tắt client (mặc định true)

**Dành riêng cho plugin:** - `stopargs` - Tham số được truyền trong quá trình tắt - `uninstallargs` - Tham số được truyền trong quá trình gỡ cài đặt plugin - `classpath` - Các mục classpath bổ sung được phân tách bằng dấu phẩy

**Thay thế biến cho plugin:** - `$I2P` - Thư mục gốc I2P - `$CONFIG` - Thư mục cấu hình người dùng (ví dụ: ~/.i2p) - `$PLUGIN` - Thư mục plugin - `$OS` - Tên hệ điều hành - `$ARCH` - Tên kiến trúc

## 5. Port Mapper

- Ưu tiên sử dụng managed client; chỉ quay lại unmanaged client khi thực sự cần thiết.
- Giữ cho quá trình khởi tạo và tắt máy nhẹ nhàng để các thao tác console vẫn phản hồi nhanh.
- Sử dụng tên registry và port mô tả rõ ràng để các công cụ chẩn đoán (và người dùng cuối) hiểu được chức năng của service.
- Tránh sử dụng static singleton - dựa vào context và manager được inject để chia sẻ tài nguyên.
- Gọi `manager.notify()` trên tất cả các chuyển đổi trạng thái để duy trì trạng thái console chính xác.
- Nếu bạn phải chạy trong một JVM riêng biệt, hãy ghi chép cách log và chẩn đoán được hiển thị lên console chính.
- Đối với các chương trình bên ngoài, hãy cân nhắc sử dụng ShellService (được thêm vào phiên bản 1.7.0) để có được lợi ích của managed client.

## 6. Định dạng cấu hình

Managed clients được giới thiệu trong **phiên bản 0.9.4** (ngày 17 tháng 12 năm 2012) và vẫn là kiến trúc được khuyến nghị tính đến **phiên bản 2.10.0** (ngày 9 tháng 9 năm 2025). Các API cốt lõi đã duy trì ổn định với không có thay đổi phá vỡ nào trong suốt giai đoạn này:

- Chữ ký constructor không thay đổi
- Các phương thức vòng đời (startup, shutdown, getState) không thay đổi
- Các phương thức đăng ký ClientAppManager không thay đổi
- Các phương thức đăng ký và tra cứu PortMapper không thay đổi

Các cải tiến đáng chú ý: - **0.9.42 (2019)** - cấu trúc thư mục clients.config.d/ cho các tệp cấu hình riêng lẻ - **1.7.0 (2021)** - ShellService được thêm vào để theo dõi trạng thái chương trình bên ngoài - **2.10.0 (2025)** - Phiên bản hiện tại không có thay đổi API managed client

Bản phát hành chính tiếp theo sẽ yêu cầu Java 17+ là phiên bản tối thiểu (yêu cầu hạ tầng, không phải thay đổi API).

## References

- [Đặc tả clients.config](/docs/specs/configuration/#clients-config)
- [Đặc Tả File Cấu Hình](/docs/specs/configuration/)
- [Mục Lục Tài Liệu Kỹ Thuật I2P](/docs/)
- [ClientAppManager Javadoc](https://i2p.github.io/i2p.i2p/net/i2p/app/ClientAppManager.html) (API 0.9.66)
- [PortMapper Javadoc](https://i2p.github.io/i2p.i2p/net/i2p/util/PortMapper.html) (API 0.9.66)
- [ClientApp interface](https://i2p.github.io/i2p.i2p/net/i2p/app/ClientApp.html) (API 0.9.66)
- [RouterApp interface](https://i2p.github.io/i2p.i2p/net/i2p/router/app/RouterApp.html) (API 0.9.66)
- [Javadoc Thay Thế (phiên bản ổn định)](https://docs.i2p-projekt.de/javadoc/)
- [Javadoc Thay Thế (clearnet mirror)](https://eyedeekay.github.io/javadoc-i2p/)

> **Lưu ý:** Mạng I2P lưu trữ tài liệu toàn diện tại http://idk.i2p/javadoc-i2p/ yêu cầu I2P router để truy cập. Để truy cập clearnet, sử dụng GitHub Pages mirror ở trên.
