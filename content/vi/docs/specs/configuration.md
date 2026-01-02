---
title: "Cấu hình Router"
description: "Các tùy chọn cấu hình và định dạng dành cho I2P routers và máy khách"
slug: "configuration"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
---

## Tổng quan

Tài liệu này cung cấp đặc tả kỹ thuật toàn diện về các tệp cấu hình I2P được sử dụng bởi router và nhiều ứng dụng khác nhau. Nó bao gồm các đặc tả định dạng tệp, định nghĩa thuộc tính và các chi tiết triển khai được xác minh đối chiếu với mã nguồn I2P và tài liệu chính thức.

### Phạm vi

- Các tệp cấu hình và định dạng của Router
- Cấu hình ứng dụng khách
- Cấu hình tunnel cho I2PTunnel
- Đặc tả định dạng tệp và việc triển khai
- Các tính năng đặc thù theo phiên bản và các tính năng bị ngưng dùng

### Ghi chú triển khai

Các tệp cấu hình được đọc và ghi bằng các phương thức `DataHelper.loadProps()` và `storeProps()` trong thư viện lõi I2P. Định dạng tệp này khác biệt đáng kể so với định dạng tuần tự hóa được dùng trong các giao thức I2P (xem [Đặc tả Cấu trúc Chung - Ánh xạ Kiểu](/docs/specs/common-structures/#type-mapping)).

---

## Định dạng tệp cấu hình chung

Các tệp cấu hình I2P tuân theo một định dạng Java Properties đã được sửa đổi với các ngoại lệ và ràng buộc cụ thể.

### Đặc tả định dạng

Dựa trên [Java Properties](http://docs.oracle.com/javase/1.5.0/docs/api/java/util/Properties.html#load%28java.io.InputStream%29) nhưng có các khác biệt quan trọng sau:

#### Mã hóa

- **PHẢI** sử dụng mã hóa UTF-8 (KHÔNG phải ISO-8859-1 như trong Java Properties tiêu chuẩn)
- Triển khai: Sử dụng tiện ích `DataHelper.getUTF8()` cho tất cả các thao tác tệp

#### Các chuỗi thoát

- **KHÔNG** có chuỗi thoát (escape sequences) nào được nhận diện (bao gồm cả dấu gạch chéo ngược `\`)
- Nối dòng **KHÔNG** được hỗ trợ
- Các ký tự dấu gạch chéo ngược được xem như nguyên văn

#### Ký tự chú thích

- `#` bắt đầu một chú thích ở bất kỳ vị trí nào trên một dòng
- `;` **chỉ** bắt đầu một chú thích khi ở cột 1
- `!` **KHÔNG** bắt đầu một chú thích (khác với Java Properties)

#### Dấu phân cách khóa-giá trị

- `=` là dấu phân tách khóa-giá trị hợp lệ **DUY NHẤT**
- `:` **KHÔNG** được nhận diện như một dấu phân tách
- Khoảng trắng **KHÔNG** được nhận diện như một dấu phân tách

#### Xử lý khoảng trắng

- Khoảng trắng ở đầu và cuối **KHÔNG** được cắt bỏ đối với khóa
- Khoảng trắng ở đầu và cuối **ĐƯỢC** cắt bỏ đối với giá trị

#### Xử lý dòng

- Các dòng không có `=` sẽ bị bỏ qua (được xem như chú thích hoặc dòng trống)
- Giá trị rỗng (`key=`) được hỗ trợ kể từ phiên bản 0.9.10
- Các khóa có giá trị rỗng được lưu trữ và truy xuất bình thường

#### Giới hạn ký tự

**Các khóa KHÔNG được chứa**: - `#` (dấu thăng) - `=` (dấu bằng) - `\n` (ký tự xuống dòng) - Không được bắt đầu bằng `;` (dấu chấm phẩy)

**Giá trị KHÔNG được chứa**: - `#` (dấu thăng/dấu số) - `\n` (ký tự xuống dòng) - Không được bắt đầu hoặc kết thúc bằng `\r` (carriage return - ký tự CR, trả về đầu dòng) - Không được bắt đầu hoặc kết thúc bằng khoảng trắng (tự động cắt bỏ)

### Sắp xếp tệp

Tệp cấu hình không nhất thiết phải được sắp xếp theo khóa. Tuy nhiên, hầu hết các ứng dụng I2P sắp xếp các khóa theo thứ tự bảng chữ cái khi ghi tệp cấu hình để thuận tiện cho: - Chỉnh sửa thủ công - Các thao tác diff (so sánh khác biệt) trong hệ thống kiểm soát phiên bản - Tính dễ đọc đối với con người

### Chi tiết triển khai

#### Đọc các tệp cấu hình

```java
// Method signature from net.i2p.data.DataHelper
public static Properties loadProps(File file)
```
**Hành vi**: - Đọc các tệp được mã hóa UTF-8 - Thực thi tất cả các quy tắc định dạng được mô tả ở trên - Kiểm tra các ràng buộc ký tự - Trả về đối tượng Properties rỗng nếu tệp không tồn tại - Ném `IOException` khi gặp lỗi đọc

#### Viết tệp cấu hình

```java
// Method signature from net.i2p.data.DataHelper
public static void storeProps(Properties props, File file)
```
**Hành vi**: - Ghi các tệp được mã hóa UTF-8 - Sắp xếp các khóa theo thứ tự bảng chữ cái (trừ khi dùng OrderedProperties) - Đặt quyền tệp thành chế độ 600 (chỉ người dùng đọc/ghi) kể từ phiên bản 0.8.1 - Ném `IllegalArgumentException` đối với các ký tự không hợp lệ trong khóa hoặc giá trị - Ném `IOException` đối với lỗi ghi

#### Xác thực định dạng

Bản triển khai thực hiện kiểm tra tính hợp lệ nghiêm ngặt: - Khóa và giá trị được kiểm tra để phát hiện các ký tự bị cấm - Các mục nhập không hợp lệ gây ra ngoại lệ trong quá trình ghi - Khi đọc, các dòng sai định dạng (các dòng không có `=`) sẽ bị bỏ qua âm thầm

### Ví dụ về định dạng

#### Tệp cấu hình hợp lệ

```properties
# This is a comment
; This is also a comment (column 1 only)
key.with.dots=value with spaces
another_key=value=with=equals
empty.value=
numeric.value=12345
unicode.value=こんにちは
```
#### Các ví dụ cấu hình không hợp lệ

```properties
# INVALID: Key contains equals sign
invalid=key=value

# INVALID: Key contains hash
invalid#key=value

# INVALID: Value contains newline (implicit)
key=value
continues here

# INVALID: Semicolon comment not in column 1 (treated as key)
 ; not.a.comment=value
```
---

## Thư viện lõi và cấu hình Router

### Cấu hình ứng dụng khách (clients.config)

**Vị trí**: `$I2P_CONFIG_DIR/clients.config` (cũ) hoặc `$I2P_CONFIG_DIR/clients.config.d/` (hiện đại)   **Giao diện cấu hình**: Bảng điều khiển Router tại `/configclients`   **Thay đổi định dạng**: Phiên bản 0.9.42 (Tháng 8 năm 2019)

#### Cấu trúc thư mục (Phiên bản 0.9.42+)

Kể từ bản phát hành 0.9.42, tệp clients.config mặc định được tự động tách thành các tệp cấu hình riêng lẻ:

```
$I2P_CONFIG_DIR/
├── clients.config.d/
│   ├── 00-webConsole.config
│   ├── 01-i2ptunnel.config
│   ├── 02-i2psnark.config
│   ├── 03-susidns.config
│   └── ...
└── clients.config (legacy, auto-migrated)
```
**Hành vi chuyển đổi (migration)**:
- Ở lần chạy đầu tiên sau khi nâng cấp lên 0.9.42+, tệp nguyên khối (monolithic file) sẽ được tách tự động
- Các thuộc tính trong các tệp đã tách có tiền tố `clientApp.0.`
- Vẫn hỗ trợ định dạng cũ để tương thích ngược
- Định dạng tách rời cho phép đóng gói theo mô-đun và quản lý plugin

#### Định dạng thuộc tính

Các dòng có dạng `clientApp.x.prop=val`, trong đó `x` là số ứng dụng.

**Yêu cầu đánh số ứng dụng**: - PHẢI bắt đầu từ 0 - PHẢI liên tiếp (không bỏ số) - Thứ tự xác định trình tự khởi động

#### Các thuộc tính bắt buộc

##### chính

- **Kiểu**: Chuỗi (tên lớp được định danh đầy đủ)
- **Bắt buộc**: Có
- **Mô tả**: Hàm khởi tạo hoặc phương thức `main()` trong lớp này sẽ được gọi tùy theo kiểu ứng dụng khách (được quản lý vs. không được quản lý)
- **Ví dụ**: `clientApp.0.main=net.i2p.router.web.RouterConsoleRunner`

#### Thuộc tính tùy chọn

##### tên

- **Loại**: Chuỗi
- **Bắt buộc**: Không
- **Mô tả**: Tên hiển thị trong router console
- **Ví dụ**: `clientApp.0.name=Router Console`

##### đối số

- **Type**: String (phân tách bằng khoảng trắng hoặc tab)
- **Required**: Không
- **Description**: Các đối số được truyền vào hàm tạo của lớp chính hoặc phương thức main()
- **Quoting**: Các đối số chứa khoảng trắng hoặc tab có thể được đặt trong dấu nháy `'` hoặc `"`
- **Example**: `clientApp.0.args=-d $CONFIG/eepsite`

##### độ trễ

- **Loại**: Số nguyên (giây)
- **Bắt buộc**: Không
- **Mặc định**: 120
- **Mô tả**: Số giây chờ trước khi khởi chạy máy khách
- **Ghi đè**: Bị ghi đè bởi `onBoot=true` (đặt độ trễ về 0)
- **Giá trị đặc biệt**:
  - `< 0`: Chờ router đạt trạng thái RUNNING, rồi khởi động ngay trong luồng mới
  - `= 0`: Chạy ngay trong cùng luồng (ngoại lệ được truyền tới console)
  - `> 0`: Bắt đầu sau khoảng trễ trong luồng mới (ngoại lệ được ghi log, không được truyền tiếp)

##### onBoot

- **Loại**: Boolean
- **Bắt buộc**: Không
- **Mặc định**: false
- **Mô tả**: Buộc độ trễ là 0, ghi đè thiết lập độ trễ tường minh
- **Trường hợp sử dụng**: Khởi chạy các dịch vụ trọng yếu ngay khi router khởi động

##### startOnLoad

- **Loại**: Boolean (kiểu luận lý)
- **Bắt buộc**: Không
- **Mặc định**: true
- **Mô tả**: Có khởi động ứng dụng khách hay không
- **Trường hợp sử dụng**: Vô hiệu hóa các ứng dụng khách mà không xóa cấu hình

#### Thuộc tính dành riêng cho plugin

Các thuộc tính này chỉ được sử dụng bởi các plugin (không phải các client lõi):

##### stopargs

- **Kiểu**: Chuỗi (phân tách bằng dấu cách hoặc tab)
- **Mô tả**: Các đối số được truyền khi dừng ứng dụng khách
- **Thay thế biến**: Có (xem bên dưới)

##### uninstallargs

- **Kiểu**: Chuỗi (phân tách bằng khoảng trắng hoặc tab)
- **Mô tả**: Các đối số được truyền khi gỡ cài đặt ứng dụng khách
- **Thay thế biến**: Có (xem bên dưới)

##### đường dẫn lớp

- **Kiểu**: Chuỗi (các đường dẫn được phân tách bằng dấu phẩy)
- **Mô tả**: Các thành phần classpath (đường dẫn lớp) bổ sung cho ứng dụng khách
- **Thay thế biến**: Có (xem bên dưới)

#### Thay thế biến (Chỉ dành cho plugin)

Các biến sau sẽ được thay thế trong `args`, `stopargs`, `uninstallargs` và `classpath` cho các plugin:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Variable</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Expands To</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Example</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>$I2P</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Base I2P installation directory</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>/usr/share/i2p</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>$CONFIG</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">User configuration directory</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>~/.i2p</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>$PLUGIN</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Plugin directory</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>~/.i2p/plugins/foo</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>$OS</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Operating system name</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>linux</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>$ARCH</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Architecture name</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>amd64</code></td>
    </tr>
  </tbody>
</table>
**Lưu ý**: Việc thay thế biến chỉ được thực hiện cho các plugin, không áp dụng cho các client lõi.

#### Các loại client

##### Các ứng dụng khách được quản lý

- Hàm khởi tạo được gọi với các tham số `RouterContext` và `ClientAppManager`
- Ứng dụng khách phải triển khai giao diện `ClientApp`
- Vòng đời do router kiểm soát
- Có thể được khởi động, dừng và khởi động lại một cách động

##### Các ứng dụng khách không được quản lý

- Phương thức `main(String[] args)` được gọi
- Chạy trong một luồng riêng biệt
- Vòng đời không được router quản lý
- Kiểu client cũ (legacy)

#### Ví dụ cấu hình

```properties
# Router Console (core client)
clientApp.0.main=net.i2p.router.web.RouterConsoleRunner
clientApp.0.name=Router Console
clientApp.0.args=-d $CONFIG/eepsite
clientApp.0.delay=0
clientApp.0.onBoot=true
clientApp.0.startOnLoad=true

# I2PTunnel (core client)
clientApp.1.main=net.i2p.i2ptunnel.TunnelControllerGroup
clientApp.1.name=I2PTunnel
clientApp.1.args=
clientApp.1.delay=120
clientApp.1.startOnLoad=true

# Plugin Example
clientApp.2.main=org.example.plugin.PluginMain
clientApp.2.name=Example Plugin
clientApp.2.args=-config $PLUGIN/config.properties
clientApp.2.stopargs=-shutdown
clientApp.2.uninstallargs=-remove $PLUGIN
clientApp.2.classpath=$PLUGIN/lib/plugin.jar,$PLUGIN/lib/dep.jar
clientApp.2.delay=240
clientApp.2.startOnLoad=true
```
---

### Cấu hình Logger (logger.config)

**Vị trí**: `$I2P_CONFIG_DIR/logger.config`   **Giao diện cấu hình**: Bảng điều khiển Router tại `/configlogging`

#### Tham chiếu thuộc tính

##### Cấu hình bộ đệm bảng điều khiển

###### logger.consoleBufferSize

- **Kiểu**: Số nguyên
- **Mặc định**: 20
- **Mô tả**: Số lượng tối đa thông điệp nhật ký được lưu đệm trong bảng điều khiển
- **Phạm vi**: 1-1000 (khuyến nghị)

##### Định dạng ngày và giờ

###### logger.dateFormat

- **Loại**: String (mẫu SimpleDateFormat)
- **Mặc định**: Theo locale (thiết lập vùng) của hệ thống
- **Ví dụ**: `HH:mm:ss.SSS`
- **Tài liệu**: [Java SimpleDateFormat](https://docs.oracle.com/javase/8/docs/api/java/text/SimpleDateFormat.html)

##### Mức độ ghi nhật ký

###### logger.defaultLevel

- **Loại**: Enum (kiểu liệt kê)
- **Mặc định**: ERROR
- **Giá trị**: `CRIT`, `ERROR`, `WARN`, `INFO`, `DEBUG`
- **Mô tả**: Mức ghi log mặc định cho tất cả các lớp

###### logger.minimumOnScreenLevel

- **Kiểu**: Enum (kiểu liệt kê)
- **Mặc định**: CRIT
- **Giá trị**: `CRIT`, `ERROR`, `WARN`, `INFO`, `DEBUG`
- **Mô tả**: Mức tối thiểu cho các thông báo hiển thị trên màn hình

###### logger.record.{class}

- **Kiểu**: Kiểu liệt kê (Enum)
- **Giá trị**: `CRIT`, `ERROR`, `WARN`, `INFO`, `DEBUG`
- **Mô tả**: Ghi đè mức ghi nhật ký theo từng lớp
- **Ví dụ**: `logger.record.net.i2p.router.transport.udp=DEBUG`

##### Tùy chọn hiển thị

###### logger.displayOnScreen

- **Loại**: Boolean
- **Mặc định**: true
- **Mô tả**: Có hiển thị thông điệp nhật ký trong đầu ra của console hay không

###### logger.dropDuplicates

- **Kiểu**: Boolean
- **Mặc định**: true
- **Mô tả**: Bỏ qua các thông điệp nhật ký trùng lặp liên tiếp

###### logger.dropOnOverflow

- **Kiểu**: Boolean
- **Mặc định**: false
- **Mô tả**: Loại bỏ thông điệp khi bộ đệm đầy (thay vì chặn)

##### Hành vi xả (flush)

###### logger.flushInterval

- **Loại**: Số nguyên (giây)
- **Mặc định**: 29
- **Từ**: Phiên bản 0.9.18
- **Mô tả**: Tần suất ghi (flush) bộ đệm log xuống đĩa

##### Cấu hình định dạng

###### logger.format

- **Type**: Chuỗi (dãy ký tự)
- **Description**: Mẫu định dạng thông điệp nhật ký
- **Format Characters**:
  - `d` = ngày/giờ
  - `c` = tên lớp
  - `t` = tên luồng
  - `p` = độ ưu tiên (cấp độ nhật ký)
  - `m` = thông điệp
- **Example**: `dctpm` tạo ra `[dấu thời gian] [lớp] [luồng] [mức] thông điệp`

##### Nén (Phiên bản 0.9.56+)

###### logger.gzip

- **Kiểu**: Boolean
- **Mặc định**: false
- **Từ**: Phiên bản 0.9.56
- **Mô tả**: Kích hoạt nén gzip cho các tệp nhật ký xoay vòng

###### logger.minGzipSize

- **Kiểu**: Số nguyên (byte)
- **Mặc định**: 65536
- **Kể từ**: Phiên bản 0.9.56
- **Mô tả**: Kích thước tệp tối thiểu để kích hoạt nén (mặc định 64 KB)

##### Quản lý tệp

###### logger.logBufferSize

- **Type**: Số nguyên (byte)
- **Default**: 1024
- **Description**: Số lượng thông điệp tối đa sẽ được đệm trước khi xả bộ đệm

###### logger.logFileName

- **Loại**: Chuỗi (đường dẫn tệp)
- **Mặc định**: `logs/log-@.txt`
- **Mô tả**: Mẫu đặt tên tệp nhật ký (`@` được thay thế bằng số thứ tự xoay vòng)

###### logger.logFilenameOverride

- **Kiểu**: Chuỗi (đường dẫn tệp)
- **Mô tả**: Ghi đè tên tệp nhật ký (vô hiệu hóa mẫu xoay vòng)

###### logger.logFileSize

- **Loại**: Chuỗi (kích thước kèm đơn vị)
- **Mặc định**: 10M
- **Đơn vị**: K (kilobyte), M (megabyte), G (gigabyte)
- **Ví dụ**: `50M`, `1G`

###### logger.logRotationLimit

- **Kiểu**: Số nguyên
- **Mặc định**: 2
- **Mô tả**: Số thứ tự tệp nhật ký xoay vòng cao nhất (log-0.txt đến log-N.txt)

#### Cấu hình mẫu

```properties
# Basic logging configuration
logger.consoleBufferSize=50
logger.dateFormat=yyyy-MM-dd HH:mm:ss.SSS
logger.defaultLevel=WARN
logger.displayOnScreen=true
logger.dropDuplicates=true
logger.dropOnOverflow=false

# Flushing and format
logger.flushInterval=30
logger.format=dctpm

# File management
logger.logBufferSize=2048
logger.logFileName=logs/log-@.txt
logger.logFileSize=25M
logger.logRotationLimit=5

# Compression (0.9.56+)
logger.gzip=true
logger.minGzipSize=131072

# On-screen filtering
logger.minimumOnScreenLevel=ERROR

# Per-class overrides
logger.record.net.i2p.router.transport=INFO
logger.record.net.i2p.router.tunnel=DEBUG
logger.record.net.i2p.crypto=WARN
```
---

### Cấu hình plugin

#### Cấu hình plugin riêng lẻ (plugins/*/plugin.config)

**Vị trí**: `$I2P_CONFIG_DIR/plugins/{plugin-name}/plugin.config`   **Định dạng**: Định dạng tệp cấu hình chuẩn của I2P   **Tài liệu**: [Đặc tả Plugin](/docs/specs/plugin/)

##### Các thuộc tính bắt buộc

###### tên

- **Kiểu**: Chuỗi
- **Bắt buộc**: Có
- **Mô tả**: Tên hiển thị của plugin
- **Ví dụ**: `name=I2P Plugin Example`

###### khóa

- **Loại**: Chuỗi (khóa công khai)
- **Bắt buộc**: Có (bỏ qua đối với plugin được ký bằng SU3)
- **Mô tả**: Khóa công khai ký plugin để xác minh
- **Định dạng**: Khóa ký được mã hóa Base64

###### người ký

- **Loại**: Chuỗi
- **Bắt buộc**: Có
- **Mô tả**: Định danh người ký plugin
- **Ví dụ**: `signer=user@example.i2p`

###### phiên bản

- **Kiểu**: Chuỗi (định dạng VersionComparator)
- **Bắt buộc**: Có
- **Mô tả**: Phiên bản plugin để kiểm tra cập nhật
- **Định dạng**: Semantic versioning (phiên bản hóa ngữ nghĩa) hoặc định dạng tùy chỉnh có thể so sánh
- **Ví dụ**: `version=1.2.3`

##### Thuộc tính hiển thị

###### ngày

- **Loại**: Long (mốc thời gian Unix tính bằng mili giây)
- **Mô tả**: Ngày phát hành plugin

###### tác giả

- **Loại**: Chuỗi
- **Mô tả**: Tên tác giả plugin

###### websiteURL

- **Loại**: Chuỗi (URL)
- **Mô tả**: URL trang web của plugin

###### updateURL

- **Loại**: Chuỗi (URL)
- **Mô tả**: URL kiểm tra cập nhật cho plugin (phần bổ trợ)

###### updateURL.su3

- **Type**: Chuỗi (URL)
- **Since**: Phiên bản 0.9.15
- **Description**: URL cập nhật ở định dạng SU3 (được ưu tiên)

###### mô tả

- **Kiểu**: Chuỗi
- **Mô tả**: Mô tả plugin bằng tiếng Anh

###### description_{language}

- **Loại**: Chuỗi
- **Mô tả**: Mô tả plugin được bản địa hóa
- **Ví dụ**: `description_de=Deutsche Beschreibung`

###### giấy phép

- **Loại**: Chuỗi
- **Mô tả**: Định danh giấy phép của plugin
- **Ví dụ**: `license=Apache 2.0`

##### Thuộc tính cài đặt

###### Không khởi động ngay sau khi cài đặt

- **Loại**: Boolean
- **Mặc định**: false
- **Mô tả**: Ngăn khởi động tự động sau khi cài đặt

###### Cần khởi động lại router

- **Kiểu**: Boolean
- **Mặc định**: false
- **Mô tả**: Yêu cầu khởi động lại router sau khi cài đặt

###### chỉ cài đặt

- **Kiểu**: Boolean
- **Mặc định**: false
- **Mô tả**: Chỉ cài đặt một lần (không cập nhật)

###### chỉ cập nhật

- **Kiểu**: Boolean
- **Mặc định**: false
- **Mô tả**: Chỉ cập nhật bản cài đặt hiện có (không cài đặt mới)

##### Cấu hình plugin mẫu

```properties
# Required properties
name=Example I2P Plugin
signer=developer@mail.i2p
version=1.5.0

# Display properties
author=Plugin Developer
websiteURL=http://plugin.example.i2p
updateURL=http://plugin.example.i2p/update.xpi2p
updateURL.su3=http://plugin.example.i2p/update.su3
description=Example plugin demonstrating configuration
description_de=Beispiel-Plugin zur Demonstration der Konfiguration
license=MIT

# Installation behavior
dont-start-at-install=false
router-restart-required=false
```
#### Cấu hình Plugin Toàn cục (plugins.config)

**Vị trí**: `$I2P_CONFIG_DIR/plugins.config`   **Mục đích**: Bật/tắt các plugin đã cài đặt ở phạm vi toàn cục

##### Định dạng thuộc tính

```properties
plugin.{name}.startOnLoad=true|false
```
- `{name}`: Tên plugin từ plugin.config
- `startOnLoad`: Có khởi động plugin khi router khởi động hay không

##### Ví dụ

```properties
plugin.i2psnark.startOnLoad=true
plugin.susimail.startOnLoad=true
plugin.susidns.startOnLoad=true
plugin.i2pbote.startOnLoad=false
```
---

### Cấu hình ứng dụng web (webapps.config)

**Vị trí**: `$I2P_CONFIG_DIR/webapps.config`   **Mục đích**: Bật/tắt và cấu hình các ứng dụng web

#### Định dạng thuộc tính

##### webapps.{name}.startOnLoad

- **Kiểu**: Boolean
- **Mô tả**: Có khởi chạy ứng dụng web khi router khởi động hay không
- **Định dạng**: `webapps.{name}.startOnLoad=true|false`

##### webapps.{name}.classpath

- **Kiểu**: Chuỗi (các đường dẫn được phân tách bằng dấu cách hoặc dấu phẩy)
- **Mô tả**: Các phần tử classpath (đường dẫn lớp) bổ sung cho ứng dụng web
- **Định dạng**: `webapps.{name}.classpath=[paths]`

#### Thay thế biến

Các đường dẫn hỗ trợ các phép thay thế biến sau:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Variable</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Expands To</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Context</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>$I2P</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Base I2P directory</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Core webapps</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>$CONFIG</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">User config directory</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">All webapps</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>$PLUGIN</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Plugin directory</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Plugin webapps</td>
    </tr>
  </tbody>
</table>
#### Phân giải classpath (đường dẫn lớp)

- **Ứng dụng web cốt lõi**: Các đường dẫn tương đối so với `$I2P/lib`
- **Ứng dụng web plugin**: Các đường dẫn tương đối so với `$CONFIG/plugins/{appname}/lib`

#### Cấu hình ví dụ

```properties
# Router console
webapps.routerconsole.startOnLoad=true
webapps.routerconsole.classpath=routerconsole.jar

# I2PSnark
webapps.i2psnark.startOnLoad=true
webapps.i2psnark.classpath=i2psnark.jar

# SusiDNS
webapps.susidns.startOnLoad=true
webapps.susidns.classpath=susidns.jar

# Plugin webapp example
webapps.exampleplugin.startOnLoad=false
webapps.exampleplugin.classpath=$PLUGIN/lib/webapp.jar,$PLUGIN/lib/deps.jar
```
---

### Cấu hình Router (router.config)

**Vị trí**: `$I2P_CONFIG_DIR/router.config`   **Giao diện cấu hình**: Bảng điều khiển router tại `/configadvanced`   **Mục đích**: Các thiết lập router cốt lõi và các tham số mạng

#### Danh mục cấu hình

##### Cấu hình mạng

Cài đặt băng thông:

```properties
i2np.bandwidth.inboundKBytesPerSecond=100
i2np.bandwidth.outboundKBytesPerSecond=50
i2np.bandwidth.share.percentage=80
```
Cấu hình truyền tải:

```properties
# NTCP (TCP-based transport)
i2np.ntcp.port=8887
i2np.ntcp.enable=true
i2np.ntcp.autoip=true

# SSU (UDP-based transport)
i2np.udp.port=8887
i2np.udp.enable=true

# UPnP/NAT-PMP
i2np.upnp.enable=true
```
##### Hành vi của Router

```properties
# Tunnel participation
router.maxParticipatingTunnels=200
router.sharePercentage=80

# Updates
router.updatePolicy=notify
router.updateURL=http://update.i2p2.i2p/

# Network integration
router.hiddenMode=false
router.clockSkewOffset=0
```
##### Cấu hình bảng điều khiển

```properties
# Language and display
routerconsole.lang=en
routerconsole.country=US
routerconsole.summaryRefresh=60

# Browser
routerconsole.browser=default

# Security
routerconsole.enableCompression=true
```
##### Cấu hình thời gian

```properties
# NTP
time.disabled=false
time.sntpServerList=0.pool.ntp.org,1.pool.ntp.org
```
**Lưu ý**: Cấu hình Router rất phong phú. Xem bảng điều khiển Router tại `/configadvanced` để có tài liệu tham chiếu đầy đủ về các thuộc tính.

---

## Tệp cấu hình ứng dụng

### Cấu hình Sổ địa chỉ (addressbook/config.txt)

**Vị trí**: `$I2P_CONFIG_DIR/addressbook/config.txt`   **Ứng dụng**: SusiDNS   **Mục đích**: Phân giải tên máy chủ và quản lý sổ địa chỉ

#### Vị trí tệp

##### router_addressbook

- **Mặc định**: `../hosts.txt`
- **Mô tả**: Sổ địa chỉ chính (tên máy chủ trên toàn hệ thống)
- **Định dạng**: Định dạng tệp hosts tiêu chuẩn

##### privatehosts.txt

- **Vị trí**: `$I2P_CONFIG_DIR/addressbook/privatehosts.txt`
- **Mô tả**: Ánh xạ tên máy chủ riêng tư
- **Ưu tiên**: Cao nhất (ghi đè tất cả các nguồn khác)

##### userhosts.txt

- **Vị trí**: `$I2P_CONFIG_DIR/addressbook/userhosts.txt`
- **Mô tả**: Ánh xạ tên máy chủ do người dùng thêm
- **Quản lý**: Qua giao diện SusiDNS

##### hosts.txt

- **Vị trí**: `$I2P_CONFIG_DIR/addressbook/hosts.txt`
- **Mô tả**: Sổ địa chỉ công khai được tải xuống
- **Nguồn**: Nguồn cấp dữ liệu đăng ký

#### Dịch vụ đặt tên

##### BlockfileNamingService (dịch vụ phân giải tên sử dụng blockfile) (Mặc định từ 0.8.8)

Định dạng lưu trữ: - **Tệp**: `hostsdb.blockfile` - **Vị trí**: `$I2P_CONFIG_DIR/addressbook/` - **Hiệu năng**: tra cứu nhanh hơn khoảng 10 lần so với hosts.txt - **Định dạng**: Cơ sở dữ liệu nhị phân

Dịch vụ đặt tên kế thừa: - **Định dạng**: Tệp văn bản thuần túy hosts.txt - **Trạng thái**: Đã lỗi thời nhưng vẫn được hỗ trợ - **Trường hợp sử dụng**: Chỉnh sửa thủ công, kiểm soát phiên bản

#### Quy tắc tên máy chủ

Tên máy chủ I2P phải tuân theo:

1. **Yêu cầu TLD (miền cấp cao nhất)**: Phải kết thúc bằng `.i2p`
2. **Độ dài tối đa**: Tổng cộng 67 ký tự
3. **Bộ ký tự**: `[a-z]`, `[0-9]`, `.` (dấu chấm), `-` (dấu gạch ngang)
4. **Kiểu chữ**: Chỉ chữ thường
5. **Hạn chế khi bắt đầu**: Không được bắt đầu bằng `.` hoặc `-`
6. **Mẫu bị cấm**: Không được chứa `..`, `.-`, hoặc `-.` (từ 0.6.1.33)
7. **Dành riêng**: Tên máy chủ Base32 `*.b32.i2p` (52 ký tự của base32.b32.i2p)

##### Ví dụ hợp lệ

```
example.i2p
my-site.i2p
test.example.i2p
site123.i2p
```
##### Ví dụ không hợp lệ

```
example.com          # Wrong TLD
-invalid.i2p         # Starts with hyphen
invalid..i2p         # Contains double dot
invalid.-.i2p        # Contains dot-hyphen
UPPERCASE.I2P        # Must be lowercase
verylonghostnameover67charactersthatexceedsthemaximumlength.i2p  # Too long
```
#### Quản lý đăng ký

##### subscriptions.txt

- **Vị trí**: `$I2P_CONFIG_DIR/addressbook/subscriptions.txt`
- **Định dạng**: Mỗi dòng một URL
- **Mặc định**: `http://i2p-projekt.i2p/hosts.txt`

##### Định dạng nguồn cấp đăng ký (kể từ 0.9.26)

Định dạng nguồn cấp nâng cao với siêu dữ liệu:

```
#
# I2P Address Book Subscription Feed
# Format: hostname=destination [#property=value ...]
#

example.i2p=base64destination #added=20250101 #src=manual
another.i2p=base64destination #added=20250102 #src=feed1
```
Thuộc tính siêu dữ liệu: - `added`: Ngày hostname được thêm (định dạng YYYYMMDD) - `src`: Định danh nguồn - `sig`: Chữ ký tùy chọn

**Tương thích ngược**: Định dạng hostname=destination đơn giản vẫn được hỗ trợ.

#### Cấu hình mẫu

```properties
# Address book locations
router_addressbook=../hosts.txt
privatehosts.txt=$CONFIG/addressbook/privatehosts.txt
userhosts.txt=$CONFIG/addressbook/userhosts.txt
hosts.txt=$CONFIG/addressbook/hosts.txt

# Naming service
naming.service=BlockfileNamingService
naming.service.blockfile.location=$CONFIG/addressbook/hostsdb.blockfile

# Subscriptions
subscriptions.txt=$CONFIG/addressbook/subscriptions.txt
subscriptions.schedule=daily
subscriptions.proxy=false
```
---

### Cấu hình I2PSnark (i2psnark.config.d/i2psnark.config)

**Vị trí**: `$I2P_CONFIG_DIR/i2psnark.config.d/i2psnark.config`   **Ứng dụng**: trình khách BitTorrent I2PSnark   **Giao diện cấu hình**: Giao diện web tại http://127.0.0.1:7657/i2psnark

#### Cấu trúc thư mục

```
$I2P_CONFIG_DIR/i2psnark.config.d/
├── i2psnark.config
├── [torrent-hash-1]/
│   └── *.config
├── [torrent-hash-2]/
│   └── *.config
└── ...
```
#### Cấu hình chính (i2psnark.config)

Cấu hình mặc định tối thiểu:

```properties
i2psnark.dir=i2psnark
```
Các thuộc tính bổ sung được quản lý qua giao diện web:

```properties
# Basic settings
i2psnark.dir=i2psnark
i2psnark.autoStart=false
i2psnark.openTrackers=true

# Network settings
i2psnark.uploaders=8
i2psnark.upBW=40
i2psnark.seedPct=100

# I2CP settings
i2psnark.i2cpHost=127.0.0.1
i2psnark.i2cpPort=7654
```
#### Cấu hình torrent riêng lẻ

**Vị trí**: `$I2P_CONFIG_DIR/i2psnark.config.d/[torrent-hash]/*.config`   **Định dạng**: Thiết lập riêng cho mỗi torrent   **Quản lý**: Tự động (qua giao diện web)

Các thuộc tính bao gồm: - các thiết lập tải lên/tải xuống dành riêng cho torrent - độ ưu tiên của tệp - thông tin về tracker - giới hạn số lượng peer

**Lưu ý**: Các cấu hình torrent chủ yếu được quản lý thông qua giao diện web. Không khuyến nghị chỉnh sửa thủ công.

#### Tổ chức dữ liệu Torrent

Lưu trữ dữ liệu tách biệt với cấu hình:

```
$I2P_CONFIG_DIR/i2psnark/          # Data directory
├── *.torrent                       # Torrent metadata files
├── *.torrent.downloaded/           # Downloaded file directories
├── file1.dat                       # Direct file downloads
└── ...

$I2P_CONFIG_DIR/i2psnark.config.d/ # Configuration directory
├── i2psnark.config                 # Main config
└── [hashes]/                       # Per-torrent configs
```
---

### Cấu hình I2PTunnel (i2ptunnel.config)

**Vị trí**: `$I2P_CONFIG_DIR/i2ptunnel.config` (cũ) hoặc `$I2P_CONFIG_DIR/i2ptunnel.config.d/` (hiện đại)   **Giao diện cấu hình**: bảng điều khiển Router tại `/i2ptunnel`   **Thay đổi định dạng**: Phiên bản 0.9.42 (Tháng 8 năm 2019)

#### Cấu trúc thư mục (Phiên bản 0.9.42+)

Kể từ phiên bản 0.9.42, tệp i2ptunnel.config mặc định được tự động tách:

```
$I2P_CONFIG_DIR/
├── i2ptunnel.config.d/
│   ├── http-proxy/
│   │   └── tunnel.config
│   ├── irc-proxy/
│   │   └── tunnel.config
│   ├── ssh-service/
│   │   └── tunnel.config
│   └── ...
└── i2ptunnel.config (legacy, auto-migrated)
```
**Khác biệt định dạng quan trọng**: - **Định dạng nguyên khối**: Các thuộc tính có tiền tố `tunnel.N.` - **Định dạng phân tách**: Các thuộc tính **KHÔNG** có tiền tố (ví dụ: `description=`, không phải `tunnel.0.description=`)

#### Hành vi di chuyển

Khi chạy lần đầu sau khi nâng cấp lên 0.9.42: 1. Tệp i2ptunnel.config hiện có được đọc 2. Các cấu hình tunnel riêng lẻ được tạo trong i2ptunnel.config.d/ 3. Các thuộc tính được gỡ bỏ tiền tố trong các tệp đã tách 4. Tệp gốc được sao lưu 5. Định dạng cũ vẫn được hỗ trợ để đảm bảo khả năng tương thích ngược

#### Các Phần Cấu Hình

Cấu hình I2PTunnel được trình bày chi tiết trong phần [I2PTunnel Configuration Reference](#i2ptunnel-configuration-reference) bên dưới. Các mô tả thuộc tính áp dụng cho cả định dạng nguyên khối (`tunnel.N.property`) và định dạng tách rời (`property`).

---

## Tham chiếu cấu hình I2PTunnel

Phần này cung cấp tài liệu tham chiếu kỹ thuật toàn diện cho tất cả các thuộc tính cấu hình của I2PTunnel. Các thuộc tính được trình bày theo split format (định dạng tách, không có tiền tố `tunnel.N.`). Đối với monolithic format (định dạng đơn khối), thêm tiền tố `tunnel.N.` vào tất cả các thuộc tính, trong đó N là số của tunnel.

**Quan trọng**: Các thuộc tính được mô tả dưới dạng `tunnel.N.option.i2cp.*` được triển khai trong I2PTunnel và **KHÔNG** được hỗ trợ thông qua các giao diện khác như giao thức I2CP hoặc SAM API.

### Thuộc tính cơ bản

#### tunnel.N.description (mô tả)

- **Kiểu**: Chuỗi
- **Ngữ cảnh**: Tất cả tunnels
- **Mô tả**: Mô tả tunnel dễ đọc cho con người để hiển thị trong giao diện người dùng (UI)
- **Ví dụ**: `description=HTTP Proxy for outproxy access`

#### tunnel.N.name (tên)

- **Kiểu**: Chuỗi
- **Ngữ cảnh**: Tất cả tunnels
- **Bắt buộc**: Có
- **Mô tả**: Định danh tunnel duy nhất và tên hiển thị
- **Ví dụ**: `name=I2P HTTP Proxy`

#### tunnel.N.type (kiểu)

- **Kiểu**: Enum
- **Ngữ cảnh**: Tất cả các tunnel
- **Bắt buộc**: Có
- **Giá trị**:
  - `client` - tunnel client chung
  - `httpclient` - client proxy HTTP
  - `ircclient` - tunnel client IRC
  - `socksirctunnel` - proxy SOCKS IRC
  - `sockstunnel` - proxy SOCKS (phiên bản 4, 4a, 5)
  - `connectclient` - client proxy CONNECT
  - `streamrclient` - client Streamr
  - `server` - tunnel server chung
  - `httpserver` - tunnel máy chủ HTTP
  - `ircserver` - tunnel máy chủ IRC
  - `httpbidirserver` - máy chủ HTTP hai chiều
  - `streamrserver` - máy chủ Streamr

#### tunnel.N.interface (giao diện)

- **Loại**: Chuỗi (địa chỉ IP hoặc tên máy chủ)
- **Ngữ cảnh**: Chỉ áp dụng cho Client tunnels
- **Mặc định**: 127.0.0.1
- **Mô tả**: Giao diện cục bộ để lắng nghe cho các kết nối đến
- **Lưu ý bảo mật**: Việc bind tới 0.0.0.0 cho phép kết nối từ xa
- **Ví dụ**: `interface=127.0.0.1`

#### tunnel.N.listenPort (listenPort)

- **Kiểu**: Số nguyên
- **Ngữ cảnh**: Chỉ dành cho các tunnel (đường hầm) phía client
- **Phạm vi**: 1-65535
- **Mô tả**: Cổng cục bộ để lắng nghe cho các kết nối từ client
- **Ví dụ**: `listenPort=4444`

#### tunnel.N.targetHost (targetHost)

- **Loại**: Chuỗi (địa chỉ IP hoặc tên máy chủ)
- **Ngữ cảnh**: Chỉ áp dụng cho Server tunnels
- **Mô tả**: Máy chủ cục bộ để chuyển tiếp các kết nối đến
- **Ví dụ**: `targetHost=127.0.0.1`

#### tunnel.N.targetPort (targetPort)

- **Kiểu**: Số nguyên
- **Ngữ cảnh**: Chỉ áp dụng cho tunnel máy chủ
- **Phạm vi**: 1-65535
- **Mô tả**: Cổng trên targetHost để kết nối tới
- **Ví dụ**: `targetPort=80`

#### tunnel.N.targetDestination (targetDestination)

- **Loại**: Chuỗi (các đích được phân tách bằng dấu phẩy hoặc khoảng trắng)
- **Ngữ cảnh**: Chỉ dành cho client tunnels
- **Định dạng**: `destination[:port][,destination[:port]]`
- **Mô tả**: Các đích I2P để kết nối tới
- **Ví dụ**:
  - `targetDestination=example.i2p`
  - `targetDestination=example.i2p:8080`
  - `targetDestination=site1.i2p,site2.i2p:8080`

#### tunnel.N.i2cpHost (i2cpHost)

- **Kiểu**: Chuỗi (địa chỉ IP hoặc tên máy chủ)
- **Mặc định**: 127.0.0.1
- **Mô tả**: địa chỉ giao diện I2CP của router I2P
- **Lưu ý**: Bị bỏ qua khi chạy trong ngữ cảnh router
- **Ví dụ**: `i2cpHost=127.0.0.1`

#### tunnel.N.i2cpPort (i2cpPort)

- **Loại**: Số nguyên
- **Mặc định**: 7654
- **Phạm vi**: 1-65535
- **Mô tả**: Cổng I2CP của router I2P
- **Ghi chú**: Bị bỏ qua khi chạy trong ngữ cảnh router
- **Ví dụ**: `i2cpPort=7654`

#### tunnel.N.startOnLoad (startOnLoad)

- **Loại**: Boolean
- **Mặc định**: true
- **Mô tả**: Có khởi động tunnel khi I2PTunnel được tải hay không
- **Ví dụ**: `startOnLoad=true`

### Cấu hình proxy

#### tunnel.N.proxyList (proxyList)

- **Loại**: Chuỗi (các tên máy chủ được phân tách bằng dấu phẩy hoặc khoảng trắng)
- **Ngữ cảnh**: Chỉ áp dụng cho các proxy HTTP và SOCKS
- **Mô tả**: Danh sách các máy chủ outproxy (proxy chuyển tiếp từ I2P ra Internet clearnet)
- **Ví dụ**: `proxyList=outproxy.example.i2p,backup.example.i2p`

### Cấu hình máy chủ

#### tunnel.N.privKeyFile (privKeyFile)

- **Type**: Chuỗi (đường dẫn tệp)
- **Context**: Máy chủ và các tunnel máy khách lưu bền
- **Description**: Tệp chứa các khóa riêng của đích được lưu bền
- **Path**: Tuyệt đối hoặc tương đối so với thư mục cấu hình I2P
- **Example**: `privKeyFile=eepsite/eepPriv.dat`

#### tunnel.N.spoofedHost (spoofedHost)

- **Kiểu**: Chuỗi (tên máy chủ)
- **Ngữ cảnh**: Chỉ dành cho máy chủ HTTP
- **Mặc định**: Tên máy chủ Base32 của điểm đích
- **Mô tả**: Giá trị header Host được chuyển tới máy chủ cục bộ
- **Ví dụ**: `spoofedHost=example.i2p`

#### tunnel.N.spoofedHost.NNNN (spoofedHost.NNNN)

- **Kiểu**: String (hostname)
- **Ngữ cảnh**: Chỉ dành cho máy chủ HTTP
- **Mô tả**: Ghi đè virtual host cho cổng đến cụ thể
- **Trường hợp sử dụng**: Lưu trữ nhiều trang web trên các cổng khác nhau
- **Ví dụ**: `spoofedHost.8080=site1.example.i2p`

### Tùy chọn dành riêng cho ứng dụng khách

#### tunnel.N.sharedClient (sharedClient)

- **Type**: Boolean
- **Context**: Chỉ dành cho client tunnel
- **Default**: false
- **Description**: Nhiều client có thể dùng chung tunnel này hay không
- **Example**: `sharedClient=false`

#### tunnel.N.option.persistentClientKey (persistentClientKey)

- **Kiểu**: Boolean
- **Ngữ cảnh**: Chỉ áp dụng cho Client tunnels
- **Mặc định**: false
- **Mô tả**: Lưu trữ và tái sử dụng khóa đích qua các lần khởi động lại
- **Xung đột**: Loại trừ lẫn nhau với `i2cp.newDestOnResume=true`
- **Ví dụ**: `option.persistentClientKey=true`

### Tùy chọn I2CP (Triển khai I2PTunnel)

**Quan trọng**: Các thuộc tính này có tiền tố `option.i2cp.` nhưng được **triển khai trong I2PTunnel**, chứ không phải ở lớp giao thức I2CP. Chúng không khả dụng thông qua I2CP hoặc các API của SAM.

#### tunnel.N.option.i2cp.delayOpen (option.i2cp.delayOpen)

- **Kiểu**: Boolean
- **Ngữ cảnh**: Chỉ áp dụng cho tunnel phía máy khách
- **Mặc định**: false
- **Mô tả**: Trì hoãn việc tạo tunnel cho đến khi có kết nối đầu tiên
- **Trường hợp sử dụng**: Tiết kiệm tài nguyên cho các tunnel ít khi được sử dụng
- **Ví dụ**: `option.i2cp.delayOpen=false`

#### tunnel.N.option.i2cp.newDestOnResume (option.i2cp.newDestOnResume)

- **Loại**: Boolean
- **Ngữ cảnh**: Chỉ dành cho Client tunnels
- **Mặc định**: false
- **Yêu cầu**: `i2cp.closeOnIdle=true`
- **Xung đột**: Không thể dùng đồng thời với `persistentClientKey=true`
- **Mô tả**: Tạo destination (điểm đích) mới sau khi hết thời gian không hoạt động
- **Ví dụ**: `option.i2cp.newDestOnResume=false`

#### tunnel.N.option.i2cp.leaseSetPrivateKey (option.i2cp.leaseSetPrivateKey)

- **Loại**: Chuỗi (khóa được mã hóa Base64)
- **Ngữ cảnh**: Chỉ dành cho server tunnels
- **Mô tả**: Khóa mã hóa leaseset riêng tư thường trực
- **Trường hợp sử dụng**: Duy trì leaseset được mã hóa nhất quán qua các lần khởi động lại
- **Ví dụ**: `option.i2cp.leaseSetPrivateKey=AAAA...base64...`

#### tunnel.N.option.i2cp.leaseSetSigningPrivateKey (option.i2cp.leaseSetSigningPrivateKey)

- **Kiểu**: Chuỗi (sigtype:base64)
- **Ngữ cảnh**: Chỉ áp dụng cho tunnel máy chủ
- **Định dạng**: `sigtype:base64key`
- **Mô tả**: Khóa riêng để ký leaseset cố định
- **Ví dụ**: `option.i2cp.leaseSetSigningPrivateKey=7:AAAA...base64...`

### Tùy chọn dành riêng cho máy chủ

#### tunnel.N.option.enableUniqueLocal (option.enableUniqueLocal)

- **Kiểu**: Boolean (kiểu logic đúng/sai)
- **Ngữ cảnh**: Chỉ áp dụng cho server tunnels
- **Mặc định**: false
- **Mô tả**: Sử dụng địa chỉ IP cục bộ duy nhất cho mỗi đích I2P từ xa
- **Trường hợp sử dụng**: Theo dõi địa chỉ IP của máy khách trong nhật ký máy chủ
- **Lưu ý bảo mật**: Có thể làm giảm tính ẩn danh
- **Ví dụ**: `option.enableUniqueLocal=false`

#### tunnel.N.option.targetForPort.NNNN (option.targetForPort.NNNN)

- **Kiểu**: Chuỗi (tên máy chủ:cổng)
- **Ngữ cảnh**: Chỉ dành cho tunnel máy chủ
- **Mô tả**: Ghi đè targetHost/targetPort đối với cổng đến NNNN
- **Trường hợp sử dụng**: Định tuyến theo cổng tới các dịch vụ cục bộ khác nhau
- **Ví dụ**: `option.targetForPort.8080=localhost:8080`

### Cấu hình Thread Pool (nhóm luồng)

#### tunnel.N.option.i2ptunnel.usePool (option.i2ptunnel.usePool)

- **Loại**: Boolean
- **Ngữ cảnh**: Chỉ dành cho server tunnels
- **Mặc định**: true
- **Mô tả**: Sử dụng pool luồng để xử lý kết nối
- **Lưu ý**: Luôn là false đối với standard servers (bị bỏ qua)
- **Ví dụ**: `option.i2ptunnel.usePool=true`

#### tunnel.N.option.i2ptunnel.blockingHandlerCount (option.i2ptunnel.blockingHandlerCount)

- **Loại**: Số nguyên
- **Ngữ cảnh**: Chỉ áp dụng cho các tunnel máy chủ
- **Mặc định**: 65
- **Mô tả**: Kích thước tối đa của pool luồng (thread pool)
- **Lưu ý**: Bị bỏ qua đối với các máy chủ tiêu chuẩn
- **Ví dụ**: `option.i2ptunnel.blockingHandlerCount=100`

### Tùy chọn máy khách HTTP

#### tunnel.N.option.i2ptunnel.httpclient.allowInternalSSL (option.i2ptunnel.httpclient.allowInternalSSL)

- **Kiểu**: Boolean
- **Ngữ cảnh**: Chỉ áp dụng cho client HTTP
- **Mặc định**: false
- **Mô tả**: Cho phép kết nối SSL tới các địa chỉ .i2p
- **Ví dụ**: `option.i2ptunnel.httpclient.allowInternalSSL=false`

#### tunnel.N.option.i2ptunnel.httpclient.disableAddressHelper (option.i2ptunnel.httpclient.disableAddressHelper)

- **Kiểu**: Boolean (đúng/sai)
- **Ngữ cảnh**: Chỉ dành cho máy khách HTTP
- **Mặc định**: false
- **Mô tả**: Vô hiệu hóa các liên kết trợ giúp địa chỉ trong phản hồi của proxy
- **Ví dụ**: `option.i2ptunnel.httpclient.disableAddressHelper=false`

#### tunnel.N.option.i2ptunnel.httpclient.jumpServers (option.i2ptunnel.httpclient.jumpServers)

- **Type**: Chuỗi (các URL được phân tách bằng dấu phẩy hoặc khoảng trắng)
- **Context**: Chỉ áp dụng cho HTTP client
- **Description**: Các URL Jump server (máy chủ Jump hỗ trợ phân giải tên) dùng để phân giải tên máy chủ (hostname)
- **Example**: `option.i2ptunnel.httpclient.jumpServers=http://jump.i2p/jump,http://stats.i2p/jump`

#### tunnel.N.option.i2ptunnel.httpclient.sendAccept (option.i2ptunnel.httpclient.sendAccept)

- **Kiểu**: Boolean
- **Ngữ cảnh**: Chỉ dành cho client HTTP
- **Mặc định**: false
- **Mô tả**: Chuyển tiếp các header Accept-* (ngoại trừ Accept và Accept-Encoding)
- **Ví dụ**: `option.i2ptunnel.httpclient.sendAccept=false`

#### tunnel.N.option.i2ptunnel.httpclient.sendReferer (option.i2ptunnel.httpclient.sendReferer)

- **Loại**: Boolean
- **Ngữ cảnh**: Chỉ áp dụng cho client HTTP
- **Mặc định**: false
- **Mô tả**: Chuyển tiếp các header Referer qua proxy
- **Lưu ý về quyền riêng tư**: Có thể làm rò rỉ thông tin
- **Ví dụ**: `option.i2ptunnel.httpclient.sendReferer=false`

#### tunnel.N.option.i2ptunnel.httpclient.sendUserAgent (option.i2ptunnel.httpclient.sendUserAgent)

- **Kiểu**: Boolean
- **Ngữ cảnh**: Chỉ dành cho máy khách HTTP
- **Mặc định**: false
- **Mô tả**: Chuyển tiếp các tiêu đề User-Agent qua proxy
- **Lưu ý về quyền riêng tư**: Có thể làm lộ thông tin trình duyệt
- **Ví dụ**: `option.i2ptunnel.httpclient.sendUserAgent=false`

#### tunnel.N.option.i2ptunnel.httpclient.sendVia (option.i2ptunnel.httpclient.sendVia)

- **Loại**: Boolean
- **Ngữ cảnh**: Chỉ áp dụng cho máy khách HTTP
- **Mặc định**: false
- **Mô tả**: Cho phép chuyển tiếp các tiêu đề Via qua proxy
- **Ví dụ**: `option.i2ptunnel.httpclient.sendVia=false`

#### tunnel.N.option.i2ptunnel.httpclient.SSLOutproxies (option.i2ptunnel.httpclient.SSLOutproxies)

- **Kiểu**: String (các đích được phân tách bằng dấu phẩy hoặc khoảng trắng)
- **Ngữ cảnh**: Chỉ áp dụng cho client HTTP
- **Mô tả**: Các outproxies (proxy thoát) SSL nội mạng cho HTTPS
- **Ví dụ**: `option.i2ptunnel.httpclient.SSLOutproxies=ssl-outproxy.i2p`

#### tunnel.N.option.i2ptunnel.useLocalOutproxy (option.i2ptunnel.useLocalOutproxy)

- **Loại**: Boolean
- **Ngữ cảnh**: Chỉ áp dụng cho các HTTP client
- **Mặc định**: true
- **Mô tả**: Sử dụng các plugin outproxy (proxy ra ngoài tới clearnet) cục bộ đã được đăng ký
- **Ví dụ**: `option.i2ptunnel.useLocalOutproxy=true`

### Xác thực máy khách HTTP

#### tunnel.N.option.proxyAuth (option.proxyAuth)

- **Kiểu**: Enum
- **Ngữ cảnh**: Chỉ dành cho client HTTP
- **Mặc định**: false
- **Giá trị**: `true`, `false`, `basic`, `digest`
- **Mô tả**: Yêu cầu xác thực cục bộ để truy cập proxy
- **Lưu ý**: `true` tương đương với `basic`
- **Ví dụ**: `option.proxyAuth=basic`

#### tunnel.N.option.proxy.auth.USER.md5 (option.proxy.auth.USER.md5)

- **Kiểu**: Chuỗi (hex chữ thường 32 ký tự)
- **Ngữ cảnh**: Chỉ dành cho client HTTP
- **Yêu cầu**: `proxyAuth=basic` hoặc `proxyAuth=digest`
- **Mô tả**: Giá trị băm MD5 của mật khẩu cho người dùng USER
- **Không dùng nữa**: Sử dụng SHA-256 thay thế (0.9.56+)
- **Ví dụ**: `option.proxy.auth.alice.md5=5f4dcc3b5aa765d61d8327deb882cf99`

#### tunnel.N.option.proxy.auth.USER.sha256 (option.proxy.auth.USER.sha256)

- **Kiểu**: Chuỗi (64 ký tự hex chữ thường)
- **Ngữ cảnh**: Chỉ dành cho client HTTP
- **Yêu cầu**: `proxyAuth=digest`
- **Kể từ**: Phiên bản 0.9.56
- **Tiêu chuẩn**: RFC 7616
- **Mô tả**: Giá trị băm SHA-256 của mật khẩu cho người dùng USER
- **Ví dụ**: `option.proxy.auth.alice.sha256=5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8`

### Xác thực Outproxy

#### tunnel.N.option.outproxyAuth (option.outproxyAuth)

- **Kiểu**: Boolean
- **Ngữ cảnh**: Chỉ dành cho máy khách HTTP
- **Mặc định**: false
- **Mô tả**: Gửi thông tin xác thực tới outproxy (proxy chuyển tiếp ra Internet bên ngoài I2P)
- **Ví dụ**: `option.outproxyAuth=false`

#### tunnel.N.option.outproxyUsername (option.outproxyUsername)

- **Kiểu**: String
- **Ngữ cảnh**: Chỉ dành cho client HTTP
- **Yêu cầu**: `outproxyAuth=true`
- **Mô tả**: Tên người dùng cho xác thực outproxy (proxy ra Internet công khai)
- **Ví dụ**: `option.outproxyUsername=user`

#### tunnel.N.option.outproxyPassword (option.outproxyPassword)

- **Kiểu**: Chuỗi
- **Ngữ cảnh**: Chỉ dành cho client HTTP
- **Yêu cầu**: `outproxyAuth=true`
- **Mô tả**: Mật khẩu cho xác thực outproxy (proxy đi ra Internet công khai)
- **Bảo mật**: Được lưu ở dạng văn bản thuần
- **Ví dụ**: `option.outproxyPassword=secret`

### Tùy chọn máy khách SOCKS

#### tunnel.N.option.i2ptunnel.socks.proxy.default (option.i2ptunnel.socks.proxy.default)

- **Kiểu**: Chuỗi (các đích đến được phân tách bằng dấu phẩy hoặc dấu cách)
- **Ngữ cảnh**: chỉ dành cho client SOCKS
- **Mô tả**: Các outproxy (proxy thoát từ I2P ra Internet công khai) trong mạng cho các cổng không được chỉ định
- **Ví dụ**: `option.i2ptunnel.socks.proxy.default=outproxy.i2p`

#### tunnel.N.option.i2ptunnel.socks.proxy.NNNN (option.i2ptunnel.socks.proxy.NNNN)

- **Loại**: Chuỗi (các đích được phân tách bằng dấu phẩy hoặc khoảng trắng)
- **Ngữ cảnh**: Chỉ dành cho client SOCKS
- **Mô tả**: Các outproxy (proxy đi ra) trong mạng dành riêng cho cổng NNNN
- **Ví dụ**: `option.i2ptunnel.socks.proxy.443=ssl-outproxy.i2p`

#### tunnel.N.option.outproxyType (option.outproxyType)

- **Kiểu**: Enum (kiểu liệt kê)
- **Ngữ cảnh**: Chỉ dành cho client SOCKS
- **Mặc định**: socks
- **Từ**: Phiên bản 0.9.57
- **Giá trị**: `socks`, `connect` (HTTPS)
- **Mô tả**: Loại outproxy (proxy ra ngoài) đã được cấu hình
- **Ví dụ**: `option.outproxyType=connect`

### Các tùy chọn máy chủ HTTP

#### tunnel.N.option.maxPosts (option.maxPosts)

- **Type**: Số nguyên
- **Context**: Chỉ áp dụng cho máy chủ HTTP
- **Default**: 0 (không giới hạn)
- **Description**: Số yêu cầu POST tối đa từ một destination (địa chỉ đích I2P) trong mỗi postCheckTime
- **Example**: `option.maxPosts=10`

#### tunnel.N.option.maxTotalPosts (option.maxTotalPosts)

- **Kiểu**: Số nguyên
- **Ngữ cảnh**: Chỉ máy chủ HTTP
- **Mặc định**: 0 (không giới hạn)
- **Mô tả**: Số yêu cầu POST tối đa từ tất cả các đích mỗi postCheckTime
- **Ví dụ**: `option.maxTotalPosts=50`

#### tunnel.N.option.postCheckTime (option.postCheckTime)

- **Loại**: Số nguyên (giây)
- **Ngữ cảnh**: Chỉ máy chủ HTTP
- **Mặc định**: 300
- **Mô tả**: Khoảng thời gian để kiểm tra giới hạn POST
- **Ví dụ**: `option.postCheckTime=600`

#### tunnel.N.option.postBanTime (option.postBanTime)

- **Kiểu**: Số nguyên (giây)
- **Ngữ cảnh**: Chỉ áp dụng cho máy chủ HTTP
- **Mặc định**: 1800
- **Mô tả**: Thời lượng cấm áp dụng cho một destination (đích I2P) sau khi vượt quá maxPosts
- **Ví dụ**: `option.postBanTime=3600`

#### tunnel.N.option.postTotalBanTime (option.postTotalBanTime)

- **Loại**: Số nguyên (giây)
- **Ngữ cảnh**: Chỉ dành cho máy chủ HTTP
- **Mặc định**: 600
- **Mô tả**: Thời gian cấm sau khi vượt quá maxTotalPosts
- **Ví dụ**: `option.postTotalBanTime=1200`

### Tùy chọn bảo mật máy chủ HTTP

#### tunnel.N.option.rejectInproxy (option.rejectInproxy)

- **Kiểu**: Boolean
- **Ngữ cảnh**: Chỉ dành cho máy chủ HTTP
- **Mặc định**: false
- **Mô tả**: Từ chối các kết nối có vẻ đi qua một inproxy (proxy vào)
- **Ví dụ**: `option.rejectInproxy=false`

#### tunnel.N.option.rejectReferer (option.rejectReferer)

- **Kiểu**: Boolean
- **Ngữ cảnh**: Chỉ dành cho máy chủ HTTP
- **Mặc định**: false
- **Từ**: Phiên bản 0.9.25
- **Mô tả**: Từ chối các kết nối có header Referer
- **Ví dụ**: `option.rejectReferer=false`

#### tunnel.N.option.rejectUserAgents (option.rejectUserAgents)

- **Loại**: Boolean
- **Ngữ cảnh**: Chỉ dành cho máy chủ HTTP
- **Mặc định**: false
- **Từ phiên bản**: 0.9.25
- **Yêu cầu**: thuộc tính `userAgentRejectList`
- **Mô tả**: Từ chối các kết nối có User-Agent trùng khớp
- **Ví dụ**: `option.rejectUserAgents=false`

#### tunnel.N.option.userAgentRejectList (option.userAgentRejectList)

- **Kiểu**: Chuỗi (các chuỗi so khớp, phân tách bằng dấu phẩy)
- **Ngữ cảnh**: Chỉ áp dụng cho máy chủ HTTP
- **Kể từ**: Phiên bản 0.9.25
- **Phân biệt hoa/thường**: So khớp phân biệt hoa/thường
- **Đặc biệt**: "none" (từ 0.9.33) khớp với User-Agent trống
- **Mô tả**: Danh sách các mẫu User-Agent cần từ chối
- **Ví dụ**: `option.userAgentRejectList=Mozilla,Opera,none`

### Tùy chọn máy chủ IRC

#### tunnel.N.option.ircserver.fakeHostname (option.ircserver.fakeHostname)

- **Loại**: Chuỗi (mẫu tên máy chủ)
- **Ngữ cảnh**: Chỉ dành cho máy chủ IRC
- **Mặc định**: `%f.b32.i2p`
- **Token**:
  - `%f` = Băm đích base32 đầy đủ
  - `%c` = Băm đích được che (xem cloakKey)
- **Mô tả**: Định dạng tên máy chủ được gửi tới máy chủ IRC
- **Ví dụ**: `option.ircserver.fakeHostname=%c.irc.i2p`

#### tunnel.N.option.ircserver.cloakKey (option.ircserver.cloakKey)

- **Loại**: Chuỗi (cụm mật khẩu)
- **Ngữ cảnh**: Chỉ dành cho máy chủ IRC
- **Mặc định**: Ngẫu nhiên cho mỗi phiên
- **Hạn chế**: Không dùng dấu ngoặc kép hoặc khoảng trắng
- **Mô tả**: Cụm mật khẩu để che giấu tên máy chủ một cách nhất quán
- **Trường hợp sử dụng**: Nhận diện người dùng bền vững qua các lần khởi động lại/giữa các máy chủ
- **Ví dụ**: `option.ircserver.cloakKey=mysecretkey`

#### tunnel.N.option.ircserver.method (option.ircserver.method)

- **Kiểu**: Enum (kiểu liệt kê)
- **Ngữ cảnh**: Chỉ dành cho máy chủ IRC
- **Mặc định**: user
- **Giá trị**: `user`, `webirc`
- **Mô tả**: Phương thức xác thực cho máy chủ IRC
- **Ví dụ**: `option.ircserver.method=webirc`

#### tunnel.N.option.ircserver.webircPassword (option.ircserver.webircPassword)

- **Kiểu**: Chuỗi (mật khẩu)
- **Ngữ cảnh**: Chỉ áp dụng cho máy chủ IRC
- **Yêu cầu**: `method=webirc`
- **Hạn chế**: Không được có dấu ngoặc kép hoặc khoảng trắng
- **Mô tả**: Mật khẩu để xác thực theo giao thức WEBIRC
- **Ví dụ**: `option.ircserver.webircPassword=webircpass`

#### tunnel.N.option.ircserver.webircSpoofIP (option.ircserver.webircSpoofIP)

- **Loại**: Chuỗi (địa chỉ IP)
- **Ngữ cảnh**: Chỉ dành cho máy chủ IRC
- **Yêu cầu**: `method=webirc`
- **Mô tả**: Địa chỉ IP giả mạo cho giao thức WEBIRC
- **Ví dụ**: `option.ircserver.webircSpoofIP=10.0.0.1`

### Cấu hình SSL/TLS

#### tunnel.N.option.useSSL (option.useSSL)

- **Kiểu**: Boolean
- **Mặc định**: false
- **Ngữ cảnh**: Tất cả tunnel
- **Hành vi**:
  - **Máy chủ**: Sử dụng SSL cho các kết nối đến máy chủ cục bộ
  - **Máy khách**: Yêu cầu SSL từ các máy khách cục bộ
- **Ví dụ**: `option.useSSL=false`

#### tunnel.N.option.keystoreFile (option.keystoreFile)

- **Kiểu**: Chuỗi (đường dẫn tệp)
- **Ngữ cảnh**: Chỉ áp dụng cho Client tunnels
- **Mặc định**: `i2ptunnel-(random).ks`
- **Đường dẫn**: Tương đối so với `$(I2P_CONFIG_DIR)/keystore/` nếu không phải đường dẫn tuyệt đối
- **Tự động tạo**: Sẽ được tạo nếu chưa tồn tại
- **Mô tả**: Tệp keystore (kho khóa) chứa khóa riêng SSL
- **Ví dụ**: `option.keystoreFile=my-tunnel.ks`

#### tunnel.N.option.keystorePassword (option.keystorePassword)

- **Type**: Chuỗi (mật khẩu)
- **Context**: Chỉ áp dụng cho client tunnels
- **Default**: changeit
- **Auto-generated**: Mật khẩu ngẫu nhiên nếu keystore (kho khóa) mới được tạo
- **Description**: Mật khẩu cho keystore SSL
- **Example**: `option.keystorePassword=secretpassword`

#### tunnel.N.option.keyAlias (option.keyAlias)

- **Kiểu**: String (bí danh)
- **Ngữ cảnh**: Chỉ dành cho Client tunnels
- **Tự động tạo**: Được tạo khi có khóa mới
- **Mô tả**: Bí danh cho khóa riêng trong keystore (kho lưu trữ khóa)
- **Ví dụ**: `option.keyAlias=mytunnel-key`

#### tunnel.N.option.keyPassword (option.keyPassword)

- **Loại**: Chuỗi (mật khẩu)
- **Ngữ cảnh**: Chỉ áp dụng cho client tunnels
- **Tự động tạo**: Mật khẩu ngẫu nhiên nếu tạo khóa mới
- **Mô tả**: Mật khẩu cho khóa riêng trong keystore (kho lưu trữ khóa)
- **Ví dụ**: `option.keyPassword=keypass123`

### Tùy chọn chung cho I2CP và Streaming

Tất cả các thuộc tính `tunnel.N.option.*` (không được tài liệu hóa cụ thể ở trên) được chuyển tiếp tới giao diện I2CP và streaming library (thư viện truyền dữ liệu dạng luồng) sau khi bỏ tiền tố `tunnel.N.option.`.

**Quan trọng**: Chúng tách biệt với các tùy chọn dành riêng cho I2PTunnel. Tham khảo: - [Đặc tả I2CP](/docs/specs/i2cp/) - [Đặc tả Thư viện Streaming](/docs/specs/streaming/)

Ví dụ về các tùy chọn streaming (truyền dữ liệu dạng luồng):

```properties
option.i2cp.messageReliability=BestEffort
option.i2p.streaming.connectDelay=1000
option.i2p.streaming.maxWindowSize=128
```
### Ví dụ Tunnel (đường hầm) hoàn chỉnh

```properties
# HTTP Proxy (split format without tunnel.N. prefix)
name=I2P HTTP Proxy
description=HTTP proxy for accessing I2P sites and outproxy
type=httpclient
interface=127.0.0.1
listenPort=4444
targetDestination=
sharedClient=true
startOnLoad=true

# I2CP configuration
i2cpHost=127.0.0.1
i2cpPort=7654

# HTTP client options
option.i2ptunnel.httpclient.allowInternalSSL=false
option.i2ptunnel.httpclient.disableAddressHelper=false
option.i2ptunnel.httpclient.jumpServers=http://stats.i2p/cgi-bin/jump.cgi
option.i2ptunnel.httpclient.sendAccept=false
option.i2ptunnel.httpclient.sendReferer=false
option.i2ptunnel.httpclient.sendUserAgent=false

# Proxy authentication
option.proxyAuth=false

# Outproxy configuration
option.i2ptunnel.httpclient.SSLOutproxies=false.i2p
proxyList=false.i2p

# Client behavior
option.persistentClientKey=false
option.i2cp.delayOpen=false

# I2CP tunnel options
option.inbound.length=3
option.outbound.length=3
option.inbound.quantity=2
option.outbound.quantity=2
```
---

## Lịch sử phiên bản và mốc thời gian tính năng

### Phiên bản 0.9.10 (2013)

**Tính năng**: Hỗ trợ giá trị rỗng trong các tệp cấu hình - Các khóa có giá trị rỗng (`key=`) hiện được hỗ trợ - Trước đây bị bỏ qua hoặc gây lỗi phân tích cú pháp

### Phiên bản 0.9.18 (2015)

**Tính năng**: Cấu hình khoảng thời gian flush (xả bộ đệm) của logger - Thuộc tính: `logger.flushInterval` (mặc định 29 giây) - Giảm I/O đĩa đồng thời duy trì độ trễ ghi log ở mức chấp nhận được

### Phiên bản 0.9.23 (Tháng 11 năm 2015)

**Thay đổi lớn**: Yêu cầu tối thiểu là Java 7 - Hỗ trợ cho Java 6 đã kết thúc - Bắt buộc để tiếp tục nhận các bản cập nhật bảo mật

### Phiên bản 0.9.25 (2015)

**Tính năng**: các tùy chọn bảo mật của máy chủ HTTP - `tunnel.N.option.rejectReferer` - Từ chối các kết nối có tiêu đề Referer - `tunnel.N.option.rejectUserAgents` - Từ chối các tiêu đề User-Agent cụ thể - `tunnel.N.option.userAgentRejectList` - Các mẫu User-Agent cần từ chối - **Trường hợp sử dụng**: Giảm thiểu trình thu thập dữ liệu và máy khách không mong muốn

### Phiên bản 0.9.33 (Tháng 1 năm 2018)

**Tính năng**: Lọc User-Agent nâng cao - chuỗi `userAgentRejectList` "none" khớp với User-Agent rỗng - Các bản sửa lỗi bổ sung cho i2psnark, i2ptunnel, streaming, SusiMail

### Phiên bản 0.9.41 (2019)

**Ngừng hỗ trợ**: BOB Protocol (giao thức BOB) đã bị loại bỏ khỏi Android - người dùng Android phải chuyển sang SAM hoặc I2CP

### Phiên bản 0.9.42 (Tháng 8 năm 2019)

**Thay đổi lớn**: Phân tách tệp cấu hình - `clients.config` được tách thành cấu trúc thư mục `clients.config.d/` - `i2ptunnel.config` được tách thành cấu trúc thư mục `i2ptunnel.config.d/` - Chuyển đổi tự động khi chạy lần đầu sau khi nâng cấp - Cho phép đóng gói mô-đun và quản lý plugin - Vẫn hỗ trợ định dạng nguyên khối cũ

**Các tính năng bổ sung**: - Cải thiện hiệu năng cho SSU - Ngăn chặn chéo mạng (Đề xuất 147) - Hỗ trợ kiểu mã hóa ban đầu

### Phiên bản 0.9.56 (2021)

**Tính năng**: Cải thiện bảo mật và ghi nhật ký - `logger.gzip` - Nén Gzip cho nhật ký xoay vòng (mặc định: false) - `logger.minGzipSize` - Kích thước tối thiểu để nén (mặc định: 65536 byte) - `tunnel.N.option.proxy.auth.USER.sha256` - digest authentication (xác thực dạng băm) bằng SHA-256 (RFC 7616) - **Bảo mật**: SHA-256 thay thế MD5 cho digest authentication

### Phiên bản 0.9.57 (tháng 1 năm 2023)

**Tính năng**: Cấu hình loại outproxy (proxy ra ngoài) SOCKS - `tunnel.N.option.outproxyType` - Chọn loại outproxy (socks|connect) - Mặc định: socks - Hỗ trợ HTTPS CONNECT cho các outproxy HTTPS

### Phiên bản 2.6.0 (Tháng 7 năm 2024)

**Thay đổi không tương thích**: I2P-over-Tor bị chặn - Kết nối từ các địa chỉ IP của Tor exit node (nút thoát) hiện bị từ chối - **Lý do**: Làm suy giảm hiệu năng I2P, lãng phí tài nguyên của các Tor exit node - **Tác động**: Người dùng truy cập I2P thông qua các Tor exit node sẽ bị chặn - Các nút chuyển tiếp không phải exit và ứng dụng khách Tor không bị ảnh hưởng

### Phiên bản 2.10.0 (Tháng 9 năm 2025 - Hiện tại)

**Tính năng chính**: - **Mật mã hậu lượng tử** khả dụng (tùy chọn bật qua Hidden Service Manager) - **Hỗ trợ tracker UDP** cho I2PSnark để giảm tải cho tracker - Cải thiện độ ổn định của Hidden Mode để giảm tình trạng cạn kiệt RouterInfo - Cải thiện mạng cho router bị tắc nghẽn - Tăng cường khả năng xuyên qua UPnP/NAT - Cải tiến NetDB với việc loại bỏ leaseset quyết liệt - Giảm khả năng quan sát đối với các sự kiện của router

**Cấu hình**: Không có thuộc tính cấu hình mới nào được thêm

**Thay đổi quan trọng sắp tới**: Bản phát hành tiếp theo (nhiều khả năng là 2.11.0 hoặc 3.0.0) sẽ yêu cầu Java 17 trở lên

---

## Ngừng hỗ trợ và thay đổi phá vỡ tương thích

### Những tính năng ngừng hỗ trợ quan trọng

#### Truy cập I2P-over-Tor (Phiên bản 2.6.0+)

- **Trạng thái**: Bị chặn từ tháng 7 năm 2024
- **Tác động**: Các kết nối từ IP của các nút thoát Tor bị từ chối
- **Lý do**: Làm giảm hiệu năng của mạng I2P mà không mang lại lợi ích về tính ẩn danh
- **Phạm vi ảnh hưởng**: Chỉ ảnh hưởng đến các nút thoát Tor, không ảnh hưởng đến các relay hoặc client Tor thông thường
- **Phương án thay thế**: Sử dụng I2P hoặc Tor riêng biệt, không kết hợp

#### Xác thực Digest MD5

- **Trạng thái**: Không dùng nữa (hãy dùng SHA-256)
- **Thuộc tính**: `tunnel.N.option.proxy.auth.USER.md5`
- **Lý do**: MD5 đã bị phá vỡ về mặt mật mã
- **Thay thế**: `tunnel.N.option.proxy.auth.USER.sha256` (từ 0.9.56)
- **Mốc thời gian**: MD5 vẫn được hỗ trợ nhưng không được khuyến nghị

### Các thay đổi trong kiến trúc cấu hình

#### Tệp cấu hình nguyên khối (Phiên bản 0.9.42+)

- **Bị ảnh hưởng**: `clients.config`, `i2ptunnel.config`
- **Trạng thái**: Không còn được khuyến nghị; ưu tiên dùng cấu trúc thư mục phân tách
- **Chuyển đổi**: Tự động khi chạy lần đầu sau khi nâng cấp lên 0.9.42
- **Tương thích**: Định dạng cũ vẫn hoạt động (tương thích ngược)
- **Khuyến nghị**: Dùng định dạng phân tách cho các cấu hình mới

### Yêu cầu về phiên bản Java

#### Hỗ trợ Java 6

- **Đã kết thúc**: Phiên bản 0.9.23 (Tháng 11 năm 2015)
- **Tối thiểu**: Yêu cầu Java 7 kể từ 0.9.23

#### Yêu cầu Java 17 (Sắp tới)

- **Trạng thái**: THAY ĐỔI QUAN TRỌNG SẮP TỚI
- **Mục tiêu**: Bản phát hành lớn tiếp theo sau 2.10.0 (nhiều khả năng là 2.11.0 hoặc 3.0.0)
- **Yêu cầu tối thiểu hiện tại**: Java 8
- **Hành động cần thiết**: Chuẩn bị cho việc chuyển sang Java 17
- **Mốc thời gian**: Sẽ được công bố cùng với ghi chú phát hành

### Các tính năng đã bị loại bỏ

#### Giao thức BOB (Android)

- **Đã loại bỏ**: Kể từ phiên bản 0.9.41
- **Nền tảng**: Chỉ dành cho Android
- **Thay thế**: các giao thức SAM (Simple Anonymous Messaging — giao thức nhắn tin ẩn danh đơn giản của I2P) hoặc I2CP
- **Máy tính để bàn**: BOB (giao thức BOB của I2P) vẫn khả dụng trên các nền tảng máy tính để bàn

### Các di chuyển được khuyến nghị

1. **Xác thực**: Chuyển từ xác thực Digest dùng MD5 sang dùng SHA-256
2. **Định dạng cấu hình**: Chuyển sang cấu trúc thư mục tách biệt cho máy khách và tunnels
3. **Java Runtime**: Lên kế hoạch nâng cấp lên Java 17 trước bản phát hành lớn tiếp theo
4. **Tích hợp Tor**: Không định tuyến I2P qua các exit node (nút thoát) của Tor

---

## Tài liệu tham khảo

### Tài liệu chính thức

- [Đặc tả cấu hình I2P](/docs/specs/configuration/) - Đặc tả chính thức về định dạng tệp cấu hình
- [Đặc tả plugin I2P](/docs/specs/plugin/) - Cấu hình và đóng gói plugin
- [Cấu trúc chung của I2P - Ánh xạ kiểu dữ liệu](/docs/specs/common-structures/#type-mapping) - Định dạng tuần tự hóa dữ liệu giao thức
- [Định dạng Java Properties](http://docs.oracle.com/javase/1.5.0/docs/api/java/util/Properties.html#load%28java.io.InputStream%29) - Đặc tả định dạng cơ sở

### Mã nguồn

- [Kho lưu trữ Router I2P (Java)](https://github.com/i2p/i2p.i2p) - Bản sao phản chiếu trên GitHub
- [I2P Developers Gitea](https://i2pgit.org/I2P_Developers/i2p.i2p) - Kho mã nguồn chính thức của I2P
- [DataHelper.java](https://github.com/i2p/i2p.i2p/blob/master/core/java/src/net/i2p/data/DataHelper.java) - Triển khai I/O (nhập/xuất) cho tệp cấu hình

### Tài nguyên cộng đồng

- [I2P Forum](https://i2pforum.net/) - Thảo luận cộng đồng sôi nổi và hỗ trợ
- [I2P Website](/) - Trang web chính thức của dự án

### Tài liệu API

- [DataHelper JavaDoc](https://i2pplus.github.io/javadoc/net/i2p/data/DataHelper.html) - tài liệu API cho các phương thức của tệp cấu hình

### Trạng thái của đặc tả

- **Cập nhật đặc tả lần cuối**: Tháng 1 năm 2023 (Phiên bản 0.9.57)
- **Phiên bản I2P hiện tại**: 2.10.0 (Tháng 9 năm 2025)
- **Độ chính xác kỹ thuật**: Đặc tả vẫn chính xác đến 2.10.0 (không có thay đổi phá vỡ tương thích)
- **Bảo trì**: Tài liệu sống được cập nhật khi định dạng cấu hình được sửa đổi
