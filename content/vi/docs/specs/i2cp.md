---
title: "Giao thức máy khách I2P (I2CP)"
description: "Cách các ứng dụng thương lượng các phiên, tunnels và LeaseSets với I2P router."
slug: "i2cp"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## Tổng quan

I2CP là giao thức điều khiển cấp thấp giữa một I2P router và bất kỳ tiến trình khách nào. Nó xác định một sự phân tách trách nhiệm nghiêm ngặt:

- **Router**: Quản lý định tuyến, mật mã học, vòng đời tunnel, và các thao tác cơ sở dữ liệu mạng
- **Ứng dụng khách**: Chọn các thuộc tính ẩn danh, cấu hình tunnels, và gửi/nhận thông điệp

Tất cả giao tiếp diễn ra qua một socket TCP duy nhất (tùy chọn được bọc TLS), cho phép các hoạt động bất đồng bộ, song công hoàn toàn.

**Phiên bản giao thức**: I2CP sử dụng một byte phiên bản giao thức `0x2A` (42 ở dạng thập phân) được gửi trong quá trình thiết lập kết nối ban đầu. Byte phiên bản này đã giữ ổn định kể từ khi giao thức ra đời.

**Trạng thái hiện tại**: Đặc tả này áp dụng chính xác cho router phiên bản 0.9.67 (phiên bản API 0.9.67), phát hành vào 2025-09.

## Ngữ cảnh triển khai

### Hiện thực bằng Java

Bản triển khai tham chiếu nằm trong Java I2P: - SDK phía client: gói `i2p.jar` - Phần triển khai Router: gói `router.jar` - [Javadocs](http://docs.i2p-projekt.de/javadoc/)

Khi ứng dụng khách và router chạy trong cùng một JVM, các thông điệp I2CP được truyền dưới dạng đối tượng Java mà không cần tuần tự hóa. Các ứng dụng khách bên ngoài sử dụng giao thức đã tuần tự hóa qua TCP.

### Triển khai bằng C++

i2pd (router I2P viết bằng C++) cũng triển khai I2CP bên ngoài để phục vụ các kết nối của máy khách.

### Các ứng dụng khách không dùng Java

Hiện **không có triển khai không dùng Java nào đã biết** cho một thư viện client I2CP hoàn chỉnh. Các ứng dụng không dùng Java nên thay vào đó sử dụng các giao thức cấp cao hơn:

- **SAM (Nhắn tin ẩn danh đơn giản) v3**: Giao diện dựa trên socket với các thư viện cho nhiều ngôn ngữ
- **BOB (Cầu mở cơ bản)**: Giải pháp thay thế đơn giản hơn cho SAM

Các giao thức cấp cao hơn này tự xử lý sự phức tạp của I2CP bên trong và đồng thời cung cấp thư viện streaming (cho các kết nối kiểu TCP) và thư viện datagram (cho các kết nối kiểu UDP).

## Thiết lập kết nối

### 1. Kết nối TCP

Kết nối tới cổng I2CP của router: - Mặc định: `127.0.0.1:7654` - Có thể cấu hình qua cài đặt của router - Lớp bọc TLS tùy chọn (rất khuyến nghị cho các kết nối từ xa)

### 2. Bắt tay giao thức

**Bước 1**: Gửi byte phiên bản giao thức `0x2A`

**Bước 2**: Đồng bộ thời gian

```
Client → Router: GetDateMessage
Router → Client: SetDateMessage
```
router trả về dấu thời gian hiện tại của nó và chuỗi phiên bản I2CP API (kể từ 0.8.7).

**Bước 3**: Xác thực (nếu được bật)

Kể từ 0.9.11, xác thực có thể được đưa vào GetDateMessage (thông điệp lấy ngày/giờ) thông qua một Mapping (ánh xạ) chứa: - `i2cp.username` - `i2cp.password`

Từ phiên bản 0.9.16, khi tính năng xác thực được bật, việc xác thực **phải** được hoàn tất thông qua GetDateMessage trước khi bất kỳ bản tin nào khác được gửi đi.

**Bước 4**: Tạo phiên

```
Client → Router: CreateSessionMessage (contains SessionConfig)
Router → Client: SessionStatusMessage (status=Created)
```
**Bước 5**: Tín hiệu sẵn sàng của tunnel

```
Router → Client: RequestVariableLeaseSetMessage
```
Thông báo này cho biết rằng các tunnel vào đã được thiết lập. Router sẽ KHÔNG gửi thông báo này cho đến khi có ít nhất một tunnel vào VÀ một tunnel ra tồn tại.

**Bước 6**: Công bố LeaseSet

```
Client → Router: CreateLeaseSet2Message
```
Lúc này, phiên đã hoạt động hoàn toàn để gửi và nhận thông điệp.

## Các mẫu luồng thông điệp

### Thông điệp gửi đi (Máy khách gửi tới điểm đến từ xa)

**Với i2cp.messageReliability=none**:

```
Client → Router: SendMessageMessage (nonce=0)
[No acknowledgments]
```
**Với i2cp.messageReliability=BestEffort**:

```
Client → Router: SendMessageMessage (nonce>0)
Router → Client: MessageStatusMessage (status=Accepted)
Router → Client: MessageStatusMessage (status=Success or Failure)
```
### Thông điệp đến (Router giao cho ứng dụng khách)

**Với i2cp.fastReceive=true** (mặc định từ 0.9.4):

```
Router → Client: MessagePayloadMessage
[No acknowledgment required]
```
**Với i2cp.fastReceive=false** (ĐÃ LỖI THỜI):

```
Router → Client: MessageStatusMessage (status=Available)
Client → Router: ReceiveMessageBeginMessage
Router → Client: MessagePayloadMessage
Client → Router: ReceiveMessageEndMessage
```
Các máy khách hiện đại nên luôn sử dụng chế độ nhận nhanh.

## Các cấu trúc dữ liệu phổ biến

### Phần đầu bản tin I2CP

Tất cả các thông điệp I2CP sử dụng phần đầu chung này:

```
+----+----+----+----+----+----+----+----+
| Body Length (4 bytes)                 |
+----+----+----+----+----+----+----+----+
|Type|  Message Body (variable)        |
+----+----+----+----+----+----+----+----+
```
- **Độ dài phần thân**: Số nguyên 4 byte, chỉ độ dài của phần thân thông điệp (không bao gồm phần tiêu đề)
- **Loại**: Số nguyên 1 byte, định danh kiểu thông điệp
- **Phần thân thông điệp**: 0+ byte, định dạng thay đổi theo loại thông điệp

**Giới hạn kích thước thông điệp**: Tối đa khoảng 64 KB.

### ID phiên

Số nguyên 2 byte dùng để định danh duy nhất một phiên trên một router.

**Giá trị đặc biệt**: `0xFFFF` cho biết "không có phiên" (được dùng khi tra cứu tên máy chủ mà chưa có phiên được thiết lập).

### ID thông điệp

Số nguyên 4 byte được router tạo ra để định danh duy nhất một thông điệp trong một phiên.

**Quan trọng**: ID thông điệp **không** duy nhất ở phạm vi toàn cục, mà chỉ duy nhất trong phạm vi một phiên. Chúng cũng khác với nonce (giá trị ngẫu nhiên dùng một lần) do máy khách tạo ra.

### Định dạng payload (dữ liệu tải)

Nội dung thông điệp (payload) được nén bằng gzip với header gzip chuẩn 10 byte: - Bắt đầu bằng: `0x1F 0x8B 0x08` (RFC 1952) - Kể từ 0.7.1: Các phần chưa dùng của header gzip chứa thông tin về giao thức, from-port (cổng nguồn) và to-port (cổng đích) - Điều này cho phép truyền phát và các datagram (gói tin không kết nối) trên cùng một đích

**Điều khiển nén**: Đặt `i2cp.gzip=false` để tắt nén (đặt mức nỗ lực gzip về 0). Phần đầu gzip vẫn được bao gồm, nhưng với chi phí phụ trội do nén ở mức tối thiểu.

### Cấu trúc SessionConfig (cấu hình phiên)

Định nghĩa cấu hình cho một phiên máy khách:

```
+----------------------------------+
| Destination                      |
+----------------------------------+
| Mapping (configuration options)  |
+----------------------------------+
| Creation Date                    |
+----------------------------------+
| Signature                        |
+----------------------------------+
```
**Yêu cầu quan trọng**: 1. **Ánh xạ phải được sắp xếp theo khóa** để xác minh chữ ký 2. **Ngày tạo** phải nằm trong ±30 giây so với thời gian hiện tại của router 3. **Chữ ký** được tạo bởi SigningPrivateKey của Destination (địa chỉ đích trong I2P)

**Chữ ký ngoại tuyến** (tính đến 0.9.38):

Nếu sử dụng ký ngoại tuyến, Mapping (bản ánh xạ) phải chứa: - `i2cp.leaseSetOfflineExpiration` - `i2cp.leaseSetTransientPublicKey` - `i2cp.leaseSetOfflineSignature`

Sau đó, Signature được tạo bởi SigningPrivateKey tạm thời.

## Các tùy chọn cấu hình cốt lõi

### Cấu hình Tunnel

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Option</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Default</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>inbound.length</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Number of hops for inbound tunnels</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>outbound.length</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Number of hops for outbound tunnels</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>inbound.lengthVariance</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Random variance in hop count (since 0.7.6)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>outbound.lengthVariance</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Random variance in hop count (since 0.7.6)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>inbound.quantity</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Number of concurrent inbound tunnels</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>outbound.quantity</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Number of concurrent outbound tunnels</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>inbound.backupQuantity</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Standby inbound tunnels (hot spares)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>outbound.backupQuantity</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Standby outbound tunnels (hot spares)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>inbound.allowZeroHop</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">true</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Allow 0-hop tunnels (disable for full anonymity)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>outbound.allowZeroHop</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">true</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Allow 0-hop tunnels (disable for full anonymity)</td>
    </tr>
  </tbody>
</table>
**Ghi chú**: - Các giá trị của `quantity` > 6 yêu cầu các peer chạy 0.9.0+ và làm tăng đáng kể mức sử dụng tài nguyên - Đặt `backupQuantity` thành 1-2 cho các dịch vụ có tính sẵn sàng cao - Các tunnels 0-hop đánh đổi ẩn danh để giảm độ trễ nhưng hữu ích cho việc thử nghiệm

### Xử lý thông điệp

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Option</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Default</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>clientMessageTimeout</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">60000&nbsp;ms</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Legacy timeout for message delivery</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.messageReliability</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">BestEffort</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>None</code>, <code>BestEffort</code>, or <code>Guaranteed</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.fastReceive</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">true</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Skip ReceiveMessageBegin/End handshake (default since 0.9.4)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.gzip</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">true</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Enable gzip compression of message payloads</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>outbound.priority</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Priority for outbound scheduling (-25 to +25)</td>
    </tr>
  </tbody>
</table>
**Độ tin cậy của thông điệp**: - `None`: Không có xác nhận từ router (mặc định của thư viện streaming kể từ 0.8.1) - `BestEffort`: Router gửi thông báo chấp nhận + thành công/thất bại - `Guaranteed`: Chưa được triển khai (hiện hoạt động giống BestEffort)

**Ghi đè theo từng thông điệp** (kể từ 0.9.14): - Trong một phiên với `messageReliability=none`, đặt một nonce (giá trị ngẫu nhiên dùng một lần) khác 0 sẽ yêu cầu thông báo đã giao cho thông điệp cụ thể đó - Đặt nonce=0 trong một phiên `BestEffort` sẽ tắt thông báo cho thông điệp đó

### Cấu hình LeaseSet

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Option</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Default</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.dontPublishLeaseSet</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">false</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Disable automatic LeaseSet publication (for client-only destinations)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetType</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet variant: 1 = standard, 3 = LS2, 5 = encrypted, 7 = meta</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetEncType</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Comma-separated encryption type codes (see below)</td>
    </tr>
  </tbody>
</table>
### Thẻ phiên ElGamal/AES kiểu cũ

Các tùy chọn này chỉ áp dụng cho mã hóa ElGamal kiểu cũ:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Option</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Default</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>crypto.lowTagThreshold</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">30</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Minimum session tags before replenishing</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>crypto.tagsToSend</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">40</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Number of tags to send in a batch</td>
    </tr>
  </tbody>
</table>
**Lưu ý**: Các máy khách ECIES-X25519 sử dụng một cơ chế ratchet (cơ chế cập nhật khóa dần theo từng bước) khác và bỏ qua các tùy chọn này.

## Các loại mã hóa

I2CP hỗ trợ nhiều cơ chế mã hóa đầu-cuối thông qua tùy chọn `i2cp.leaseSetEncType`. Có thể chỉ định nhiều loại (phân tách bằng dấu phẩy) để hỗ trợ cả các peer (nút ngang hàng) hiện đại và tương thích cũ.

### Các loại mã hóa được hỗ trợ

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Algorithm</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Key Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ElGamal/AES+SessionTags</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2048-bit ElGamal</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Legacy</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1-3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">-</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Unused</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES-X25519-AEAD-Ratchet</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">32-byte X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.46</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current Standard</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES-X25519-AEAD-Ratchet + ML-KEM-768 hybrid</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">32&nbsp;+&nbsp;PQ</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES-X25519-AEAD-Ratchet + ML-KEM-1024 hybrid</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">32&nbsp;+&nbsp;PQ</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved (likely ML-KEM-512 hybrid)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">32&nbsp;+&nbsp;PQ</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Future</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Planned</td>
    </tr>
  </tbody>
</table>
**Cấu hình khuyến nghị**:

```
i2cp.leaseSetEncType=4,0
```
Điều này cung cấp X25519 (thuật toán trao đổi khóa dựa trên đường cong elliptic Curve25519; được ưu tiên) cùng với phương án dự phòng ElGamal (lược đồ mật mã khóa công khai) để bảo đảm khả năng tương thích.

### Chi tiết về kiểu mã hóa

**Loại 0 - ElGamal/AES+SessionTags (thẻ phiên)**: - khóa công khai ElGamal 2048-bit (256 byte) - mã hóa đối xứng AES-256 - session tags 32 byte được gửi theo từng lô - mức tiêu tốn CPU, băng thông và bộ nhớ cao - đang được loại bỏ dần trên toàn mạng

**Loại 4 - ECIES-X25519-AEAD-Ratchet**: - Trao đổi khóa X25519 (khóa 32 byte) - ChaCha20/Poly1305 AEAD - Double ratchet kiểu Signal (cơ chế tăng tiến khóa kép kiểu Signal) - Thẻ phiên 8 byte (so với 32 byte của ElGamal) - Thẻ được tạo qua PRNG đồng bộ (không gửi trước) - Giảm overhead ~92% so với ElGamal - Tiêu chuẩn cho I2P hiện đại (hầu hết routers dùng cơ chế này)

**Loại 5-6 - Post-Quantum Hybrid (lai hậu lượng tử)**: - Kết hợp X25519 với ML-KEM (NIST FIPS 203) - Cung cấp bảo mật kháng lượng tử - ML-KEM-768 cho cân bằng giữa bảo mật/hiệu năng - ML-KEM-1024 cho mức bảo mật tối đa - Kích thước thông điệp lớn hơn do thành phần khóa hậu lượng tử (PQ) - Hỗ trợ ở cấp độ mạng vẫn đang được triển khai

### Chiến lược di chuyển

Mạng I2P đang tích cực chuyển đổi từ ElGamal (loại 0) sang X25519 (loại 4):
- NTCP → NTCP2 (đã hoàn tất)
- SSU → SSU2 (đã hoàn tất)
- ElGamal tunnels → X25519 tunnels (đã hoàn tất)
- ElGamal đầu-cuối → ECIES-X25519 (phần lớn đã hoàn tất)

## LeaseSet2 và các tính năng nâng cao

### Tùy chọn LeaseSet2 (định dạng LeaseSet thế hệ thứ hai) (kể từ 0.9.38)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Option</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Purpose</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetType</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.38</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Specifies LeaseSet variant (1, 3, 5, 7)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetEncType</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.38</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Encryption types supported (comma-separated)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetAuthType</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.41</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Per-client authentication: 0 = none, 1 = DH, 2 = PSK</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetPrivKey</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.41</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">X25519 private key for decrypting LS2 with auth</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetSecret</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.39</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Base64 secret for blinded addresses</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetTransientPublicKey</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.38</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Transient signing key for offline signatures</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetPrivateKey</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.18</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Persistent LeaseSet encryption keys (type:key pairs)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetOption.nnn</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.66</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Service records (proposal 167)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetClient.dh.nnn</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.41</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DH client auth material (indexed from 0)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetClient.psk.nnn</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.41</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">PSK client auth material (indexed from 0)</td>
    </tr>
  </tbody>
</table>
### Địa chỉ bị làm mù

Kể từ 0.9.39, các đích (Destination) có thể sử dụng các địa chỉ "blinded" (địa chỉ được làm mù) (định dạng b33) thay đổi định kỳ: - Yêu cầu `i2cp.leaseSetSecret` để bảo vệ bằng mật khẩu - Tùy chọn xác thực theo từng máy khách - Xem các đề xuất 123 và 149 để biết chi tiết

### Bản ghi dịch vụ (từ 0.9.66)

LeaseSet2 hỗ trợ các tùy chọn bản ghi dịch vụ (đề xuất 167):

```
i2cp.leaseSetOption.0=_smtp._tcp=1 86400 0 0 25 mail.example.b32.i2p
```
Định dạng tuân theo kiểu bản ghi DNS SRV nhưng đã được điều chỉnh cho I2P.

## Nhiều phiên (từ 0.9.21)

Một kết nối I2CP duy nhất có thể duy trì nhiều phiên:

**Phiên chính**: Phiên đầu tiên được tạo trên một kết nối **Các phiên phụ**: Các phiên bổ sung chia sẻ nhóm tunnel của phiên chính

### Các đặc tính của Subsession (phiên con)

1. **Tunnels dùng chung**: Sử dụng cùng các pool tunnel vào/ra như phiên chính
2. **Khóa mã hóa dùng chung**: Phải dùng các khóa mã hóa LeaseSet giống hệt nhau
3. **Khóa ký khác nhau**: Phải dùng các khóa ký của Destination (đích trong I2P) khác nhau
4. **Không có bảo đảm ẩn danh**: Được liên kết rõ ràng với phiên chính (cùng router, cùng tunnels)

### Trường hợp sử dụng Subsession (phiên con)

Cho phép giao tiếp với các đích sử dụng các loại chữ ký khác nhau: - Chính: chữ ký EdDSA (hiện đại) - Subsession (phiên phụ): chữ ký DSA (tương thích với hệ thống cũ)

### Vòng đời Subsession (phiên con)

**Tạo lập**:

```
Client → Router: CreateSessionMessage
Router → Client: SessionStatusMessage (unique Session ID)
Router → Client: RequestVariableLeaseSetMessage (separate for each destination)
Client → Router: CreateLeaseSet2Message (separate for each destination)
```
**Hủy**: - Hủy một phiên con: Giữ nguyên phiên chính - Hủy phiên chính: Hủy tất cả các phiên con và đóng kết nối - DisconnectMessage (Thông điệp ngắt kết nối): Hủy tất cả các phiên

### Xử lý ID phiên

Hầu hết các thông điệp I2CP chứa một trường Session ID. Ngoại lệ: - DestLookup / DestReply (đã lỗi thời, hãy dùng HostLookup / HostReply) - GetBandwidthLimits / BandwidthLimits (phản hồi không gắn với phiên)

**Quan trọng**: Các ứng dụng khách không nên đồng thời có nhiều thông điệp CreateSession đang chờ xử lý, vì không thể đối chiếu một cách chắc chắn các phản hồi với các yêu cầu.

## Danh mục thông điệp

### Tóm tắt các loại thông điệp

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Name</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Direction</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">CreateSession</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ReconfigureSession</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.7.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DestroySession</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">CreateLeaseSet</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">SendMessage</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ReceiveMessageBegin</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ReceiveMessageEnd</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">8</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">GetBandwidthLimits</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.7.2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">20</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">SessionStatus</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">R → C</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">21</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">RequestLeaseSet</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">R → C</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">22</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">MessageStatus</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">R → C</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">23</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">BandwidthLimits</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">R → C</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.7.2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">29</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ReportAbuse</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Bidirectional</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Unused</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">30</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Disconnect</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Bidirectional</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">31</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">MessagePayload</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">R → C</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">GetDate</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">33</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">SetDate</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">R → C</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">34</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DestLookup</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.7</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">35</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DestReply</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">R → C</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.7</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">36</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">SendMessageExpires</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.7.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">37</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">RequestVariableLeaseSet</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">R → C</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.7</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">38</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">HostLookup</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.11</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">39</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">HostReply</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">R → C</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.11</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">41</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">CreateLeaseSet2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.39</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">42</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">BlindingInfo</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.43</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
  </tbody>
</table>
**Chú giải**: C = Máy khách, R = Router

### Chi tiết chính của thông điệp

#### CreateSessionMessage (thông điệp khởi tạo phiên) (Loại 1)

**Mục đích**: Khởi tạo một phiên I2CP mới

**Nội dung**: Cấu trúc SessionConfig

**Phản hồi**: SessionStatusMessage (status=Created hoặc Invalid)

**Yêu cầu**: - Date trong SessionConfig phải trong vòng ±30 giây so với thời gian của router - Bảng ánh xạ phải được sắp xếp theo khóa để xác minh chữ ký - Destination (đích trong I2P) không được có một phiên đang hoạt động từ trước

#### RequestVariableLeaseSetMessage (Loại 37)

**Mục đích**: Router yêu cầu máy khách ủy quyền cho các tunnel đầu vào

**Nội dung**: - ID phiên - Số lượng Lease (bản ghi thuê đường hầm trong I2P) - Mảng các cấu trúc Lease (mỗi cấu trúc có thời điểm hết hạn riêng)

**Phản hồi**: CreateLeaseSet2Message (thông điệp tạo LeaseSet2)

**Ý nghĩa**: Đây là tín hiệu cho biết phiên đang hoạt động. Router chỉ gửi điều này sau khi: 1. Ít nhất một tunnel vào đã được thiết lập 2. Ít nhất một tunnel ra đã được thiết lập

**Khuyến nghị về thời gian chờ**: Các ứng dụng khách nên hủy phiên nếu không nhận được thông điệp này trong vòng từ 5 phút trở lên kể từ khi tạo phiên.

#### CreateLeaseSet2Message (Loại 41)

**Mục đích**: Ứng dụng khách công bố LeaseSet lên cơ sở dữ liệu mạng (netDb)

**Nội dung**: - ID phiên - byte loại LeaseSet (1, 3, 5, hoặc 7) - LeaseSet hoặc LeaseSet2 hoặc EncryptedLeaseSet hoặc MetaLeaseSet - Số lượng khóa riêng - Danh sách khóa riêng (một khóa cho mỗi khóa công khai trong LeaseSet, cùng thứ tự)

**Khóa riêng**: Cần thiết để giải mã các garlic messages (thông điệp theo mô hình 'garlic' của I2P) đến. Định dạng:

```
Encryption type (2 bytes)
Key length (2 bytes)
Private key data (variable)
```
**Lưu ý**: Thay thế CreateLeaseSetMessage (type 4) đã lỗi thời, vốn không hỗ trợ: - Các biến thể LeaseSet2 - Mã hóa không phải ElGamal - Nhiều loại mã hóa - LeaseSets được mã hóa - Khóa ký ngoại tuyến

#### SendMessageExpiresMessage (thông điệp thông báo việc gửi tin nhắn đã hết hạn) (Loại 36)

**Mục đích**: Gửi thông điệp tới đích đến kèm thời hạn hết hiệu lực và các tùy chọn nâng cao

**Nội dung**: - ID phiên - Đích - Tải (được nén gzip) - Nonce (số dùng một lần) (4 byte) - Cờ (2 byte) - xem bên dưới - Ngày hết hạn (6 byte, rút gọn từ 8)

**Trường cờ** (2 byte, thứ tự bit 15...0):

**Các bit 15-11**: Không sử dụng, phải là 0

**Bits 10-9**: Ghi đè độ tin cậy của thông điệp (không sử dụng, dùng nonce (giá trị dùng một lần) thay thế)

**Bit 8**: Không đóng gói kèm LeaseSet - 0: Router có thể đóng gói kèm LeaseSet trong garlic (một cơ chế thông điệp/mã hóa trong I2P) - 1: Không đóng gói kèm LeaseSet

**Các bit 7-4**: Ngưỡng thẻ thấp (chỉ áp dụng cho ElGamal, bị bỏ qua đối với ECIES)

```
0000 = Use session settings
0001 = 2 tags
0010 = 3 tags
...
1111 = 192 tags
```
**Các bit 3-0**: Các thẻ cần gửi nếu cần (chỉ dùng với ElGamal (thuật toán mã hóa khóa công khai ElGamal), bị bỏ qua trong ECIES (Elliptic Curve Integrated Encryption Scheme - hệ mã tích hợp đường cong elliptic))

```
0000 = Use session settings
0001 = 2 tags
0010 = 4 tags
...
1111 = 160 tags
```
#### MessageStatusMessage (Loại 22)

**Mục đích**: Thông báo cho ứng dụng khách về trạng thái chuyển phát thông điệp

**Nội dung**: - ID phiên - ID thông điệp (được router tạo ra) - Mã trạng thái (1 byte) - Kích thước (4 byte, chỉ áp dụng khi status=0) - Nonce (giá trị dùng một lần; 4 byte, khớp nonce SendMessage của máy khách)

**Mã trạng thái** (Thông điệp gửi đi):

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Name</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Meaning</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Result</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Accepted</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Router accepted message</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Success</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Best Effort Success</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Probable delivery</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Success</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Guaranteed Success</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Probable delivery</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Success</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Local Success</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Delivered to local client</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Success</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Best Effort Failure</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Probable failure</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Guaranteed Failure</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Generic failure</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Local Failure</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Local delivery failed</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">8</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Router Failure</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Router shutdown/error</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">9</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Network Failure</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">No network connectivity</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">10</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Bad Session</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Invalid/closed session</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">11</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Bad Message</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Invalid payload</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">12</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Bad Options</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Invalid options/expiration</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">13</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Overflow Failure</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Queue/buffer full</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">14</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Message Expired</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Expired before send</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">15</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Bad Local LeaseSet</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Local LeaseSet problem</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">16</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">No Local Tunnels</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">No tunnels available</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">17</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Unsupported Encryption</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Incompatible encryption</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">18</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Bad Destination</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Invalid remote destination</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">19</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Bad Leaseset</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Invalid remote LeaseSet</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">20</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Expired Leaseset</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Remote LeaseSet expired</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">21</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">No Leaseset</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Remote LeaseSet not found</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">22</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Meta Leaseset</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Cannot send to meta LS</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">23</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Loopback Denied</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Same source and destination</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
  </tbody>
</table>
**Mã thành công**: 1, 2, 4, 6 **Mã thất bại**: Tất cả các mã khác

**Mã trạng thái 0** (ĐÃ NGỪNG SỬ DỤNG): Thông điệp sẵn có (đến, fast receive (nhận nhanh) bị vô hiệu hóa)

#### HostLookupMessage (Loại 38)

**Mục đích**: Tra cứu đích theo tên máy chủ hoặc mã băm (thay thế DestLookup)

**Nội dung**: - ID phiên (hoặc 0xFFFF nếu không có phiên) - ID yêu cầu (4 byte) - Thời gian chờ tính bằng mili giây (4 byte, giá trị tối thiểu khuyến nghị: 10000) - Loại yêu cầu (1 byte) - Khóa tra cứu (Hash, chuỗi hostname, hoặc Destination (đích I2P))

**Các loại yêu cầu**:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Lookup Key</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Returns</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Since</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Hash</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Destination</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Hostname String</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Destination</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Hash</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Destination + Options</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.66</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Hostname String</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Destination + Options</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.66</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Destination</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Destination + Options</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.66</td>
    </tr>
  </tbody>
</table>
Các loại 2-4 trả về các tùy chọn LeaseSet (đề xuất 167) nếu có.

**Phản hồi**: HostReplyMessage

#### HostReplyMessage (Loại 39)

**Mục đích**: Phản hồi cho HostLookupMessage (thông điệp tra cứu máy chủ)

**Nội dung**: - ID phiên - ID yêu cầu - Mã kết quả (1 byte) - Destination (điểm đích) (xuất hiện khi thành công, đôi khi trong một số lỗi cụ thể) - Ánh xạ (chỉ cho các kiểu tra cứu 2-4, có thể để trống)

**Mã kết quả**:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Name</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Meaning</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Success</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Lookup succeeded</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Generic failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Lookup Password Required</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Blinded address requires password</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Private Key Required</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Blinded address requires private key</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Password and Key Required</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Blinded address requires both</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet Decryption Failure</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Cannot decrypt LeaseSet</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet Lookup Failure</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet not found in netdb</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Lookup Type Unsupported</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Router doesn't support this type</td>
    </tr>
  </tbody>
</table>
#### BlindingInfoMessage (thông điệp thông tin blinding) (Loại 42)

**Mục đích**: Thông báo cho router về các yêu cầu xác thực cho blinded destination (đích được che giấu định danh bằng kỹ thuật blinding) (kể từ 0.9.43)

**Nội dung**: - ID phiên - Cờ (1 byte) - Kiểu điểm cuối (1 byte): 0=Băm, 1=tên máy chủ, 2=Destination (đích trong I2P), 3=SigType+Key - Loại chữ ký mù (2 byte) - Thời gian hết hạn (4 byte, số giây kể từ Unix epoch) - Dữ liệu điểm cuối (thay đổi tùy theo loại) - Khóa riêng (32 byte, chỉ khi bit cờ 0 được đặt) - Mật khẩu tra cứu (String, chỉ khi bit cờ 4 được đặt)

**Cờ** (thứ tự bit 76543210):

- **Bit 0**: 0=tất cả, 1=theo từng máy khách
- **Các bit 3-1**: Lược đồ xác thực (nếu bit 0=1): 000=DH, 001=PSK
- **Bit 4**: 1=yêu cầu bí mật
- **Các bit 7-5**: Không sử dụng, đặt thành 0

**Không có phản hồi**: Router xử lý âm thầm

**Trường hợp sử dụng**: Trước khi gửi đến đích mù (địa chỉ b33), máy khách phải thực hiện một trong hai: 1. Tra cứu b33 qua HostLookup, HOẶC 2. Gửi thông điệp BlindingInfo

Nếu đích (Destination) yêu cầu xác thực, BlindingInfo là bắt buộc.

#### ReconfigureSessionMessage (thông điệp cấu hình lại phiên) (Loại 2)

**Mục đích**: Cập nhật cấu hình phiên sau khi tạo

**Nội dung**: - Session ID - SessionConfig (chỉ cần các tùy chọn đã thay đổi)

**Phản hồi**: SessionStatusMessage (thông điệp trạng thái phiên) (status=Updated or Invalid)

**Ghi chú**: - Router hợp nhất cấu hình mới với cấu hình hiện có - Tùy chọn Tunnel (`inbound.*`, `outbound.*`) luôn được áp dụng - Một số tùy chọn có thể là bất biến sau khi tạo phiên - Thời gian phải nằm trong ±30 giây so với thời gian của router - Bảng ánh xạ phải được sắp xếp theo khóa

#### DestroySessionMessage (Loại 3)

**Mục đích**: Kết thúc phiên

**Nội dung**: ID phiên

**Phản hồi dự kiến**: SessionStatusMessage (status=Destroyed)

**Hành vi thực tế** (Java I2P đến 0.9.66): - Router không bao giờ gửi SessionStatus(Destroyed) - Nếu không còn phiên nào: Gửi DisconnectMessage - Nếu còn subsessions (các phiên con): Không phản hồi

**Quan trọng**: Hành vi của Java I2P lệch khỏi đặc tả. Các triển khai nên thận trọng khi hủy các subsessions (tiểu phiên) riêng lẻ.

#### DisconnectMessage (thông điệp ngắt kết nối) (Loại 30)

**Mục đích**: Thông báo rằng kết nối sắp bị chấm dứt

**Nội dung**: Chuỗi lý do

**Tác động**: Tất cả các phiên trên kết nối bị hủy, socket (điểm cuối giao tiếp mạng) được đóng

**Hiện thực**: Chủ yếu từ router → máy khách trong Java I2P

## Lịch sử phiên bản giao thức

### Phát hiện phiên bản

Phiên bản giao thức I2CP được trao đổi trong các thông điệp Get/SetDate (kể từ 0.8.7). Đối với các router cũ hơn, thông tin về phiên bản không khả dụng.

**Chuỗi phiên bản**: Cho biết phiên bản API “core”, không nhất thiết là phiên bản router.

### Dòng thời gian các tính năng

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Key Features</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.67</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">PQ Hybrid ML-KEM (enc types 5-7) in LeaseSet</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.66</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Host lookup/reply extensions (proposal 167), service records</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.62</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">MessageStatus loopback error code</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.46</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">X25519 (enc type 4) in LeaseSet, ECIES end-to-end</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.43</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">BlindingInfo message, extended HostReply failure codes</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.41</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">EncryptedLeaseSet options, Meta LS error code</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.39</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">CreateLeaseSet2 message, RedDSA Ed25519 support</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.38</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Preliminary LS2 support (format changed in 0.9.39)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.21</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Multiple sessions on single connection</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.20</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Additional SetDate messages for clock shifts</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.16</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Authentication required before other messages (when enabled)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.15</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA Ed25519 signature type</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.14</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Per-message reliability override with nonzero nonce</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.12</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA P-256/384/521 signature types, RSA support</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.11</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">HostLookup/HostReply messages, auth in GetDate</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.7</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">RequestVariableLeaseSet message</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.5</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Additional MessageStatus codes</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.4</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Fast receive mode default, nonce=0 allowed</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.2</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">SendMessageExpires flag tag bits</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">16 leases per LeaseSet (up from 6)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.8.7</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Version strings in Get/SetDate</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.8.4</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">SendMessageExpires flag bits</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.8.3</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DestLookup in standard session, concurrent lookups</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.8.1</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>messageReliability=none</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.7.2</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">GetBandwidthLimits, BandwidthLimits</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.7.1</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">SendMessageExpires, ReconfigureSession, ports in gzip header</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.7</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DestLookup, DestReply</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.6.5-</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Original protocol features</td>
    </tr>
  </tbody>
</table>
## Các cân nhắc bảo mật

### Xác thực

**Mặc định**: Không yêu cầu xác thực **Tùy chọn**: Xác thực bằng tên người dùng/mật khẩu (kể từ 0.9.11) **Bắt buộc**: Khi được bật, quá trình xác thực phải hoàn tất trước các thông điệp khác (kể từ 0.9.16)

**Kết nối từ xa**: Luôn sử dụng TLS (`i2cp.SSL=true`) để bảo vệ thông tin xác thực và khóa riêng.

### Độ lệch đồng hồ

SessionConfig Date (ngày trong cấu hình phiên) phải nằm trong khoảng ±30 giây so với thời gian của router, nếu không phiên sẽ bị từ chối. Hãy dùng Get/SetDate (lấy/đặt ngày) để đồng bộ.

### Xử lý khóa riêng

CreateLeaseSet2Message chứa các khóa riêng để giải mã các thông điệp đến. Các khóa này phải:
- Được truyền một cách an toàn (TLS cho các kết nối từ xa)
- Được router lưu trữ an toàn
- Được xoay vòng khi bị xâm phạm

### Hết hạn thông điệp

Luôn dùng SendMessageExpires (không phải SendMessage) để thiết lập thời điểm hết hạn tường minh. Điều này: - Ngăn thông điệp bị xếp hàng vô thời hạn - Giảm tiêu thụ tài nguyên - Cải thiện độ tin cậy

### Quản lý Session Tag (thẻ phiên)

**ElGamal** (đã lỗi thời): - Các thẻ phải được truyền theo lô - Mất thẻ gây lỗi giải mã - Chi phí bộ nhớ cao

**ECIES-X25519** (hiện tại): - Thẻ được tạo thông qua PRNG (bộ tạo số giả ngẫu nhiên) được đồng bộ - Không cần truyền trước - Kháng chịu mất thông điệp - Chi phí phụ trội thấp hơn đáng kể

## Thực hành tốt nhất

### Dành cho các nhà phát triển ứng dụng khách

1. **Sử dụng Chế độ Nhận Nhanh**: Luôn đặt `i2cp.fastReceive=true` (hoặc dựa vào giá trị mặc định)

2. **Ưu tiên ECIES-X25519 (lược đồ mã hóa khóa công khai tích hợp dựa trên đường cong elliptic X25519)**: Cấu hình `i2cp.leaseSetEncType=4,0` để đạt hiệu năng tốt nhất mà vẫn đảm bảo khả năng tương thích

3. **Thiết lập thời gian hết hạn tường minh**: Sử dụng SendMessageExpires, không phải SendMessage

4. **Xử lý Subsessions (các phiên con) một cách cẩn trọng**: Lưu ý rằng subsessions không cung cấp tính ẩn danh giữa các destinations (đích đến)

5. **Hết thời gian khi tạo phiên**: Hủy phiên nếu không nhận được RequestVariableLeaseSet (thông điệp yêu cầu leaseSet biến đổi) trong vòng 5 phút

6. **Sắp xếp Configuration Mappings (các ánh xạ cấu hình)**: Luôn sắp xếp các khóa của Mapping trước khi ký SessionConfig (cấu hình phiên)

7. **Sử dụng số lượng Tunnel phù hợp**: Không đặt `quantity` > 6 trừ khi cần thiết

8. **Cân nhắc SAM/BOB cho các ngôn ngữ không phải Java**: Triển khai SAM thay vì sử dụng trực tiếp I2CP

### Dành cho các nhà phát triển Router

1. **Xác thực mốc thời gian**: Bắt buộc cửa sổ ±30 giây đối với các mốc thời gian trong SessionConfig

2. **Giới hạn kích thước thông điệp**: Bắt buộc kích thước thông điệp tối đa ~64 KB

3. **Hỗ trợ nhiều phiên**: Triển khai hỗ trợ subsession (phiên phụ) theo đặc tả 0.9.21

4. **Gửi RequestVariableLeaseSet kịp thời**: Chỉ sau khi cả inbound và outbound tunnels đều tồn tại

5. **Xử lý các thông điệp đã bị loại bỏ dần (deprecated)**: Chấp nhận nhưng không khuyến khích sử dụng ReceiveMessageBegin/End

6. **Hỗ trợ ECIES-X25519 (lược đồ mã hóa ECIES dùng X25519)**: Ưu tiên mã hóa loại 4 cho các triển khai mới

## Gỡ lỗi và khắc phục sự cố

### Các vấn đề thường gặp

**Phiên bị từ chối (không hợp lệ)**: - Kiểm tra độ lệch đồng hồ (phải nằm trong ±30 giây) - Xác minh ánh xạ được sắp xếp theo khóa - Đảm bảo đích chưa được sử dụng

**Không có RequestVariableLeaseSet**: - Router có thể đang xây dựng tunnels (chờ tối đa 5 phút) - Kiểm tra sự cố kết nối mạng - Xác minh có đủ kết nối peer (nút ngang hàng)

**Lỗi chuyển phát thông điệp**: - Kiểm tra các mã MessageStatus để biết lý do lỗi cụ thể - Xác minh LeaseSet từ xa (tập hợp thông tin đường hầm đến) đã được công bố và còn hiệu lực - Đảm bảo các loại mã hóa tương thích

**Vấn đề Subsession (phiên phụ)**: - Xác minh phiên chính được tạo trước - Xác nhận dùng cùng khóa mã hóa - Kiểm tra các khóa ký riêng biệt

### Thông báo chẩn đoán

**GetBandwidthLimits**: Truy vấn giới hạn băng thông của router **HostLookup**: Kiểm tra phân giải tên và tính sẵn sàng của LeaseSet **MessageStatus**: Theo dõi việc chuyển phát thông điệp từ đầu đến cuối

## Các đặc tả liên quan

- **Cấu trúc chung**: /docs/specs/common-structures/
- **I2NP (Giao thức mạng)**: /docs/specs/i2np/
- **ECIES-X25519**: /docs/specs/ecies/
- **Tạo Tunnel**: /docs/specs/implementation/
- **Thư viện Streaming (truyền dòng)**: /docs/specs/streaming/
- **Thư viện Datagram (gói tin)**: /docs/api/datagrams/
- **SAM v3**: /docs/api/samv3/

## Các đề xuất được tham chiếu

- [Đề xuất 123](/proposals/123-new-netdb-entries/): LeaseSets được mã hóa và xác thực
- [Đề xuất 144](/proposals/144-ecies-x25519-aead-ratchet/): ECIES-X25519-AEAD-Ratchet (cơ chế mã hóa lai dùng ECIES và X25519 với AEAD và ratchet)
- [Đề xuất 149](/proposals/149-b32-encrypted-ls2/): Định dạng địa chỉ bị làm mù (b33)
- [Đề xuất 152](/proposals/152-ecies-tunnels/): Tạo tunnel X25519
- [Đề xuất 154](/proposals/154-ecies-lookups/): Tra cứu cơ sở dữ liệu từ các đích ECIES (Destination)
- [Đề xuất 156](/proposals/156-ecies-routers/): Di chuyển router sang ECIES-X25519
- [Đề xuất 161](/vi/proposals/161-ri-dest-padding/): Nén phần đệm của đích
- [Đề xuất 167](/proposals/167-service-records/): Bản ghi dịch vụ LeaseSet
- [Đề xuất 169](/proposals/169-pq-crypto/): Mật mã lai hậu lượng tử (ML-KEM)

## Tài liệu tham chiếu Javadocs

- [Gói I2CP](http://docs.i2p-projekt.de/javadoc/net/i2p/data/i2cp/package-summary.html)
- [MessageStatusMessage](http://docs.i2p-projekt.de/javadoc/net/i2p/data/i2cp/MessageStatusMessage.html)
- [API máy khách](http://docs.i2p-projekt.de/javadoc/net/i2p/client/package-summary.html)

## Tóm tắt ngừng hỗ trợ

### Các thông điệp lỗi thời (Không được sử dụng)

- **CreateLeaseSetMessage** (loại 4): Sử dụng CreateLeaseSet2Message
- **RequestLeaseSetMessage** (loại 21): Sử dụng RequestVariableLeaseSetMessage
- **ReceiveMessageBeginMessage** (loại 6): Sử dụng chế độ nhận nhanh
- **ReceiveMessageEndMessage** (loại 7): Sử dụng chế độ nhận nhanh
- **DestLookupMessage** (loại 34): Sử dụng HostLookupMessage
- **DestReplyMessage** (loại 35): Sử dụng HostReplyMessage
- **ReportAbuseMessage** (loại 29): Chưa bao giờ được triển khai

### Các tùy chọn đã lỗi thời

- Mã hóa ElGamal (loại 0): Chuyển sang ECIES-X25519 (loại 4)
- Chữ ký DSA: Chuyển sang EdDSA hoặc ECDSA
- `i2cp.fastReceive=false`: Luôn sử dụng chế độ nhận nhanh
