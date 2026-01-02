---
title: "Hướng dẫn viết tài liệu I2P"
description: "Duy trì tính nhất quán, độ chính xác và tính dễ tiếp cận trong toàn bộ tài liệu kỹ thuật của I2P"
slug: "writing-guidelines"
lastUpdated: "2025-10"
---

**Mục đích:** Đảm bảo tính nhất quán, độ chính xác và khả năng truy cập trong toàn bộ tài liệu kỹ thuật I2P

---

## Các nguyên tắc cốt lõi

### 1. Xác minh mọi thứ

**Không bao giờ giả định hay đoán mò.** Mọi phát biểu kỹ thuật phải được xác minh đối chiếu với: - Mã nguồn I2P hiện tại (https://i2pgit.org/I2P_Developers/i2p.i2p/src/branch/master) - Tài liệu API chính thức (https://i2p.github.io/i2p.i2p/  - Đặc tả cấu hình [/docs/specs/](/docs/) - Ghi chú phát hành gần đây [/releases/](/categories/release/)

**Ví dụ về việc xác minh đúng cách:**

```markdown
❌ BAD: "The ClientApp interface probably requires three constructor parameters."
✅ GOOD: "The ClientApp interface requires this constructor signature: 
         public MyClientApp(I2PAppContext context, ClientAppManager manager, String[] args)"
```
### 2. Ưu tiên rõ ràng hơn ngắn gọn

Hãy viết cho đối tượng là các nhà phát triển có thể lần đầu tiên tiếp xúc với I2P. Giải thích đầy đủ các khái niệm thay vì giả định người đọc đã có sẵn kiến thức.

**Ví dụ:**

```markdown
❌ BAD: "Use the port mapper for service discovery."
✅ GOOD: "The port mapper offers a simple directory for internal TCP services. 
         Register loopback ports so other applications can discover your service 
         without hardcoded addresses."
```
### 3. Ưu tiên khả năng tiếp cận

Tài liệu phải có thể được truy cập bởi các nhà phát triển trên clearnet (internet thông thường), mặc dù I2P là một network overlay (lớp phủ mạng). Luôn cung cấp các lựa chọn thay thế có thể truy cập từ clearnet cho các tài nguyên nội bộ của I2P.

---

## Độ chính xác kỹ thuật

### Tài liệu về API và giao diện

**Luôn bao gồm:** 1. Tên gói đầy đủ ở lần đề cập đầu tiên: `net.i2p.app.ClientApp` 2. Chữ ký phương thức đầy đủ, kèm kiểu trả về 3. Tên và kiểu của tham số 4. Các tham số bắt buộc và tùy chọn

**Ví dụ:**

```markdown
The `startup()` method has signature `void startup() throws IOException` and must 
execute without blocking. The method must call `ClientAppManager.notify()` at least 
once to transition from INITIALIZED state.
```
### Các thuộc tính cấu hình

Khi viết tài liệu cho các tệp cấu hình: 1. Hiển thị chính xác tên thuộc tính 2. Chỉ định mã hóa tệp (UTF-8 cho cấu hình I2P) 3. Cung cấp các ví dụ đầy đủ 4. Ghi rõ giá trị mặc định 5. Ghi chú phiên bản khi các thuộc tính được giới thiệu/thay đổi

**Ví dụ:**

```markdown
### clients.config Properties

**Required:**
- `clientApp.N.main` - Full class name (no default)

**Optional:**
- `clientApp.N.delay` - Seconds before starting (default: 120)
- `clientApp.N.onBoot` - Forces delay=0 if true (default: false, added in 0.9.4)
```
### Hằng số và Kiểu liệt kê

Khi viết tài liệu cho các hằng số, hãy dùng chính tên định danh trong mã:

```markdown
❌ BAD: "Common registrations include console, i2ptunnel, Jetty, sam, and bob"

✅ GOOD: "Common port mapper service constants from `net.i2p.util.PortMapper`:
- `SVC_CONSOLE` - Router console (default port 7657)
- `SVC_HTTP_PROXY` - HTTP proxy (default port 4444)
- `SVC_SAM` - SAM bridge (default port 7656)"
```
### Phân biệt giữa các khái niệm tương tự

I2P có nhiều hệ thống chồng chéo. Luôn nêu rõ bạn đang viết tài liệu cho hệ thống nào:

**Ví dụ:**

```markdown
Note that client registry and port mapper are separate systems:
- **ClientAppManager registry** enables inter-application communication by name lookup
- **PortMapper** maps service names to host:port combinations for service discovery
- **i2ptunnel tunnel types** are configuration values (tunnel.N.type), not service registrations
```
---

## Các URL tài liệu và tài liệu tham khảo

### Các quy tắc về khả năng truy cập URL

1. **Tham chiếu chính** nên sử dụng URL có thể truy cập trên clearnet (mạng Internet công khai)
2. **URL nội bộ I2P** (.i2p domains) phải kèm ghi chú về khả năng truy cập
3. **Luôn cung cấp phương án thay thế** khi liên kết đến tài nguyên nội bộ I2P

**Mẫu cho các URL nội bộ của I2P:**

```markdown
> **Note:** The I2P network hosts comprehensive documentation at http://idk.i2p/javadoc-i2p/ 
> which requires an I2P router for access. For clearnet access, use the GitHub Pages 
> mirror at https://eyedeekay.github.io/javadoc-i2p/
```
### Các URL tham khảo I2P được khuyến nghị

**Đặc tả chính thức:** - [Cấu hình](/docs/specs/configuration/) - [Plugin](/docs/specs/plugin/) - [Mục lục tài liệu](/docs/)

**Tài liệu API (chọn phiên bản mới nhất):** - Mới nhất: https://i2p.github.io/i2p.i2p/ (API 0.9.66 tính đến I2P 2.10.0) - Bản sao trên Clearnet (mạng Internet công khai): https://eyedeekay.github.io/javadoc-i2p/

**Mã nguồn:** - GitLab (chính thức): https://i2pgit.org/I2P_Developers/i2p.i2p/src/branch/master - GitHub mirror (bản sao): https://github.com/i2p/i2p.i2p

### Tiêu chuẩn định dạng liên kết

```markdown
✅ GOOD: [ClientApp Javadoc](https://i2p.github.io/i2p.i2p/net/i2p/app/ClientApp.html)
✅ GOOD: [Configuration Specification](https://geti2p.net/spec/configuration)

❌ BAD: See the ClientApp docs at http://idk.i2p/...
❌ BAD: [link](url) with no descriptive text
```
---

## Theo dõi phiên bản

### Siêu dữ liệu tài liệu

Mỗi tài liệu kỹ thuật nên bao gồm siêu dữ liệu phiên bản trong frontmatter (phần mở đầu):

```markdown
---
title: "Document Title"
description: "Brief description"
slug: "url-slug"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
reviewStatus: "verified"
---
```
**Định nghĩa các trường:** - `lastUpdated`: Năm-tháng khi tài liệu được rà soát/cập nhật lần cuối - `accurateFor`: Phiên bản I2P mà tài liệu đã được xác minh đối chiếu - `reviewStatus`: Một trong "draft", "needs-review", "verified", "outdated"

### Tham chiếu phiên bản trong nội dung

Khi đề cập đến phiên bản: 1. Dùng **in đậm** cho phiên bản hiện tại: "**version 2.10.0** (September 2025)" 2. Ghi cả số phiên bản và ngày phát hành khi nhắc tới các phiên bản trước đây 3. Ghi phiên bản API riêng, tách biệt với phiên bản I2P khi phù hợp

**Ví dụ:**

```markdown
Managed clients were introduced in **version 0.9.4** (December 17, 2012) and 
remain the recommended architecture as of **version 2.10.0** (September 9, 2025). 
The current API version is **0.9.66**.
```
### Tài liệu hóa các thay đổi theo thời gian

Đối với các tính năng đã phát triển:

```markdown
**Version history:**
- **0.9.4 (December 2012)** - Managed clients introduced
- **0.9.42 (2019)** - clients.config.d/ directory structure added
- **1.7.0 (2021)** - ShellService added for external program tracking
- **2.10.0 (September 2025)** - Current release, no API changes to managed clients
```
### Thông báo ngừng sử dụng

Nếu viết tài liệu về các tính năng không còn được khuyến nghị sử dụng (deprecated):

```markdown
> **Deprecated:** This feature was deprecated in version X.Y.Z and will be removed 
> in version A.B.C. Use [alternative feature](link) instead.
```
---

## Tiêu chuẩn thuật ngữ

### Các thuật ngữ I2P chính thức

Sử dụng các thuật ngữ chính xác này một cách nhất quán:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Correct Term</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Avoid</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">I2P router</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">I2P node, I2P client (ambiguous)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">eepsite</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">I2P website, hidden service (Tor term)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">tunnel</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">connection, circuit (Tor term)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">netDb</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">network database, DHT</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">lease set</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">destination info</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">destination</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">address, endpoint</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">base64 destination</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">I2P address, .i2p address</td>
    </tr>
  </tbody>
</table>
### Thuật ngữ máy khách được quản lý

Khi viết tài liệu về các máy khách được quản lý:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Use This</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Not This</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">managed client</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">managed application</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">unmanaged client</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">legacy client, static client</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ClientAppManager</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">application manager, client manager</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">lifecycle methods</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">state methods, control methods</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">client registry</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">application registry, name service</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">port mapper</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">port registry, service directory</td>
    </tr>
  </tbody>
</table>
### Thuật ngữ cấu hình

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Correct</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Incorrect</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>clients.config</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">clients.cfg, client.config</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>clients.config.d/</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">clients.d/, config.d/</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">router.config</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">router.cfg</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2ptunnel.config</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">tunnel.config</td>
    </tr>
  </tbody>
</table>
### Tên gói và lớp

Luôn sử dụng tên đầy đủ khi nhắc đến lần đầu, sau đó dùng tên ngắn:

```markdown
The `net.i2p.app.ClientApp` interface requires implementation of three lifecycle 
methods. When a ClientApp starts, the manager calls `startup()`...
```
---

## Ví dụ về mã và định dạng

### Ví dụ mã Java

Sử dụng tô sáng cú pháp đúng chuẩn và các ví dụ đầy đủ:

```markdown
### Example: Registering with Port Mapper

\`\`\`java
// Register HTTP proxy service
context.portMapper().register(
    PortMapper.SVC_HTTP_PROXY, 
    "127.0.0.1", 
    4444
);

// Later, retrieve the port
int port = context.portMapper().getPort(PortMapper.SVC_HTTP_PROXY);
if (port == -1) {
    // Service not registered
}
\`\`\`
```
**Yêu cầu cho ví dụ mã:** 1. Bao gồm chú thích giải thích các dòng quan trọng 2. Hiển thị xử lý lỗi khi phù hợp 3. Sử dụng tên biến thực tế 4. Tuân theo quy ước viết mã của I2P (thụt lề 4 dấu cách) 5. Hiển thị các câu lệnh import nếu không rõ ràng từ ngữ cảnh

### Ví dụ cấu hình

Hiển thị các ví dụ cấu hình đầy đủ, hợp lệ:

```markdown
### Example: clients.config.d/ Entry

File: `clients.config.d/00-console.config`

\`\`\`properties
# Router console configuration
clientApp.0.main=net.i2p.router.web.RouterConsoleRunner
clientApp.0.name=Router Console
clientApp.0.args=7657 ::1,127.0.0.1 ./webapps/
clientApp.0.delay=0
clientApp.0.onBoot=true
\`\`\`
```
### Các ví dụ dòng lệnh

Dùng `$` cho lệnh của người dùng, `#` cho lệnh của root:

```markdown
\`\`\`bash
# Install I2P on Debian/Ubuntu
$ sudo apt-get install i2p

# Start the router
$ i2prouter start
\`\`\`
```
### Mã trong dòng

Sử dụng dấu backtick cho: - Tên phương thức: `startup()` - Tên lớp: `ClientApp` - Tên thuộc tính: `clientApp.0.main` - Tên tệp: `clients.config` - Hằng số: `SVC_HTTP_PROXY` - Tên gói: `net.i2p.app`

---

## Giọng điệu và giọng văn

### Chuyên nghiệp nhưng dễ tiếp cận

Hãy viết cho độc giả có nền tảng kỹ thuật mà không tỏ ra trịch thượng:

```markdown
❌ BAD: "Obviously, you should implement the startup() method."
✅ GOOD: "Managed clients must implement the startup() method to initialize resources."

❌ BAD: "Even a junior dev knows you need to call notify()."
✅ GOOD: "The manager requires at least one notify() call during startup to track state transitions."
```
### Thể chủ động

Hãy dùng giọng chủ động để tăng tính rõ ràng:

```markdown
❌ PASSIVE: "The ClientAppManager is notified by the client when state changes."
✅ ACTIVE: "The client notifies ClientAppManager when state changes."
```
### Thể mệnh lệnh trong hướng dẫn

Hãy dùng câu mệnh lệnh trực tiếp trong nội dung hướng dẫn thao tác:

```markdown
✅ "Implement these three lifecycle methods:"
✅ "Call manager.notify() after changing state."
✅ "Register services using context.portMapper().register()"
```
### Tránh sử dụng biệt ngữ không cần thiết

Giải thích thuật ngữ khi lần đầu tiên xuất hiện:

```markdown
✅ GOOD: "The netDb (network database) stores information about I2P routers and destinations."
❌ BAD: "Query the netDb for peer info." (no explanation)
```
### Hướng dẫn về dấu câu

1. **Không dùng gạch ngang dài (em-dash)** - dùng dấu gạch ngang thông thường, dấu phẩy, hoặc dấu chấm phẩy
2. Dùng **dấu phẩy Oxford (Oxford comma)** trong danh sách: "console, i2ptunnel, và Jetty"
3. **Dấu chấm bên trong khối mã** chỉ dùng khi cần thiết về ngữ pháp
4. **Danh sách liệt kê nối tiếp** dùng dấu chấm phẩy khi các mục có dấu phẩy

---

## Cấu trúc tài liệu

### Thứ tự các phần tiêu chuẩn

Về tài liệu API:

1. **Tổng quan** - tính năng làm gì, vì sao nó tồn tại
2. **Triển khai** - cách triển khai/sử dụng
3. **Cấu hình** - cách cấu hình
4. **Tham chiếu API** - mô tả chi tiết phương thức/thuộc tính
5. **Ví dụ** - ví dụ hoàn chỉnh chạy được
6. **Thực tiễn tốt nhất** - mẹo và khuyến nghị
7. **Lịch sử phiên bản** - thời điểm giới thiệu, các thay đổi theo thời gian
8. **Tài liệu tham khảo** - liên kết tới tài liệu liên quan

### Thứ bậc tiêu đề

Sử dụng các cấp độ tiêu đề theo ngữ nghĩa:

```markdown
# Document Title (h1 - only one per document)

## Major Section (h2)

### Subsection (h3)

#### Detail Section (h4)

**Bold text for emphasis within sections**
```
### Các hộp thông tin

Sử dụng blockquotes (khối trích dẫn) cho các lưu ý đặc biệt:

```markdown
> **Note:** Additional information that clarifies the main content.

> **Warning:** Important information about potential issues or breaking changes.

> **Deprecated:** This feature is deprecated and will be removed in version X.Y.Z.

> **Status:** Current implementation status or version information.
```
### Danh sách và tổ chức

**Danh sách không thứ tự** cho các mục không theo trình tự:

```markdown
- First item
- Second item
- Third item
```
**Danh sách có thứ tự** cho các bước tuần tự:

```markdown
1. First step
2. Second step
3. Third step
```
**Danh sách định nghĩa** dùng để giải thích thuật ngữ:

```markdown
**Term One**
: Explanation of term one

**Term Two**  
: Explanation of term two
```
---

## Những lỗi thường gặp cần tránh

### 1. Nhầm lẫn giữa các hệ thống tương tự

**Đừng nhầm lẫn:** - bảng đăng ký của ClientAppManager so với PortMapper - các loại tunnel của i2ptunnel so với các hằng số của dịch vụ PortMapper - ClientApp so với RouterApp (ngữ cảnh khác nhau) - client được quản lý so với client không được quản lý

**Luôn làm rõ hệ thống nào** bạn đang thảo luận:

```markdown
✅ "Register with ClientAppManager using manager.register(this) for name-based lookup."
✅ "Register with PortMapper using context.portMapper().register() for port discovery."
```
### 2. Các tham chiếu phiên bản lỗi thời

**Không nên:** - Gọi các phiên bản cũ là "hiện tại" - Liên kết đến tài liệu API đã lỗi thời - Sử dụng chữ ký phương thức deprecated (không còn được khuyến nghị sử dụng) trong các ví dụ

**Nên làm:** - Kiểm tra ghi chú phát hành trước khi phát hành - Xác minh tài liệu API phù hợp với phiên bản hiện tại - Cập nhật các ví dụ để sử dụng các thực tiễn tốt nhất hiện nay

### 3. URL không thể truy cập

**Đừng:** - Chỉ liên kết đến các tên miền .i2p mà không có lựa chọn thay thế trên clearnet (mạng Internet công khai) - Sử dụng URL tài liệu bị hỏng hoặc đã lỗi thời - Liên kết đến file:// paths cục bộ

**Nên làm:** - Cung cấp các lựa chọn thay thế trên clearnet (mạng công khai) cho tất cả các liên kết nội bộ I2P - Kiểm tra URL có thể truy cập được trước khi xuất bản - Sử dụng các URL ổn định (geti2p.net, không phải dịch vụ lưu trữ tạm thời)

### 4. Ví dụ mã chưa đầy đủ

**Đừng:** - Hiển thị các đoạn trích không có ngữ cảnh - Bỏ qua xử lý lỗi - Sử dụng biến chưa được định nghĩa - Bỏ qua các câu lệnh import khi không rõ ràng

**Nên làm:** - Đưa ra các ví dụ hoàn chỉnh, có thể biên dịch - Bao gồm xử lý lỗi cần thiết - Giải thích chức năng của từng dòng quan trọng - Kiểm thử các ví dụ trước khi xuất bản

### 5. Các tuyên bố mơ hồ

```markdown
❌ "Some applications register services."
✅ "Applications implementing ClientApp may register with ClientAppManager 
   using manager.register(this) to enable name-based lookup."

❌ "Configuration files go in the config directory."
✅ "Modern I2P installations store client configurations in 
   $I2P/clients.config.d/ as individual files."
```
---

## Quy ước Markdown

### Đặt tên tệp

Sử dụng kebab-case (kiểu đặt tên dùng dấu gạch nối) cho tên tệp: - `managed-clients.md` - `port-mapper-guide.md` - `configuration-reference.md`

### Định dạng Frontmatter (phần siêu dữ liệu ở đầu tài liệu)

Luôn bao gồm YAML frontmatter (phần siêu dữ liệu ở đầu tài liệu bằng YAML):

```yaml
---
title: "Document Title"
description: "Brief description under 160 characters"
slug: "url-slug"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
reviewStatus: "verified"
---
```
### Định dạng liên kết

**Liên kết nội bộ** (trong tài liệu):

```markdown
See [clients.config specification](https://geti2p.net/spec/configuration#clients-config)
```
**Liên kết ngoài** (đến các tài nguyên khác):

```markdown
For more details, see [ClientApp Javadoc](https://i2p.github.io/i2p.i2p/net/i2p/app/ClientApp.html)
```
**Liên kết kho mã nguồn**:

```markdown
View source: [ClientApp.java](https://i2pgit.org/I2P_Developers/i2p.i2p/src/branch/master/core/java/src/net/i2p/app/ClientApp.java)
```
### Định dạng bảng

Sử dụng các bảng Markdown kiểu GitHub:

```markdown
| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `main` | String | (required) | Full class name |
| `delay` | Integer | 120 | Seconds before start |
| `onBoot` | Boolean | false | Force immediate start |
```
### Thẻ ngôn ngữ của khối mã

Luôn chỉ định ngôn ngữ để tô sáng cú pháp:

```markdown
\`\`\`java
// Java code
\`\`\`

\`\`\`bash
# Shell commands
\`\`\`

\`\`\`properties
# Configuration files
\`\`\`

\`\`\`xml
<!-- XML files -->
\`\`\`
```
---

## Danh sách kiểm tra rà soát

Trước khi xuất bản tài liệu, hãy xác minh:

- [ ] Tất cả các tuyên bố kỹ thuật được kiểm chứng đối chiếu với mã nguồn hoặc tài liệu chính thức
- [ ] Số phiên bản và ngày tháng được cập nhật
- [ ] Tất cả URL có thể truy cập từ clearnet (Internet công khai) (hoặc đã cung cấp phương án thay thế)
- [ ] Ví dụ mã hoàn chỉnh và đã được kiểm thử
- [ ] Thuật ngữ tuân theo quy ước của I2P
- [ ] Không dùng dấu gạch ngang dài; dùng gạch ngang thông thường hoặc dấu câu khác
- [ ] Frontmatter (phần đầu tài liệu) đầy đủ và chính xác
- [ ] Thứ bậc tiêu đề mang tính ngữ nghĩa (h1 → h2 → h3)
- [ ] Danh sách và bảng được định dạng đúng
- [ ] Mục tài liệu tham khảo bao gồm tất cả các nguồn đã trích dẫn
- [ ] Tài liệu tuân theo các hướng dẫn về cấu trúc
- [ ] Giọng điệu chuyên nghiệp nhưng dễ tiếp cận
- [ ] Các khái niệm tương tự được phân biệt rõ ràng
- [ ] Không có liên kết hoặc tham chiếu bị hỏng
- [ ] Ví dụ cấu hình hợp lệ và cập nhật

---

**Phản hồi:** Nếu bạn phát hiện vấn đề hoặc có đề xuất cho các hướng dẫn này, vui lòng gửi chúng qua các kênh phát triển chính thức của I2P.
