---
title: "I2PControl JSON-RPC"
description: "API quản lý router từ xa thông qua webapp I2PControl"
slug: "i2pcontrol"
lastUpdated: "2026-07-10"
accurateFor: "2.12.0"
reviewStatus: "needs-review"
---

# Tài liệu API I2PControl

-------------kiểm tra thêm nội dung--------------

I2PControl là một API **JSON-RPC 2.0** được tích hợp sẵn với I2P router (từ phiên bản 0.9.39). Nó cho phép giám sát và điều khiển router đã được xác thực thông qua các yêu cầu JSON có cấu trúc.

> **Mật khẩu mặc định:** `itoopie` — đây là mật khẩu gốc từ nhà máy và **nên được thay đổi** ngay lập tức để đảm bảo bảo mật.

## 1. Tổng quan & Truy cập

| Implementation             | Default Endpoint                 | Protocol | Enabled by Default                             | Notes                  |
|----------------------------|----------------------------------|----------|------------------------------------------------|------------------------|
| Java I2P (2.10.0+)         | `http://127.0.0.1:7657/jsonrpc/` | HTTP     | ❌ Phải bật thông qua WebApps (Router Console) | Ứng dụng web tích hợp  |
| i2pd (C++ implementation)  | `https://127.0.0.1:7650/`        | HTTPS    | ✅ Được bật theo mặc định                       | Hành vi plugin cũ      |
---

Trong trường hợp Java I2P, bạn phải vào **Router Console → WebApps → I2PControl** và bật nó (đặt khởi động tự động). Khi đã hoạt động, tất cả các phương thức đều yêu cầu bạn phải xác thực trước và nhận token phiên.

## 2. Định dạng JSON-RPC

---

```json
{
  "jsonrpc": "2.0",
  "id": "1",
  "method": "MethodName",
  "params": {
    /* named parameters */
  }
}
```
Tất cả các yêu cầu đều tuân theo cấu trúc JSON-RPC 2.0:

```json
{
  "jsonrpc": "2.0",
  "id": "1",
  "result": { /* data */ }
}
```
Một phản hồi thành công bao gồm trường `result`; khi thất bại, một đối tượng `error` sẽ được trả về:

```json
{
  "jsonrpc": "2.0",
  "id": "1",
  "error": {
    "code": -32001,
    "message": "Invalid password"
  }
}
```
hoặc

## 3. Luồng Xác thực

### Yêu cầu (Xác thực)

```bash
curl -s -H "Content-Type: application/json" \
  -d '{
        "jsonrpc": "2.0",
        "id": "1",
        "method": "Authenticate",
        "params": {
          "API": 1,
          "Password": "itoopie"
        }
      }' \
  http://127.0.0.1:7657/jsonrpc/
```
### Phản hồi thành công

```json
{
  "jsonrpc": "2.0",
  "id": "1",
  "result": {
    "Token": "a1b2c3d4e5",
    "API": 1
  }
}
```
| Trường      | Hướng     | Kiểu   | Mô tả                                                    |
|------------|-----------|--------|----------------------------------------------------------|
| `API`      | Yêu cầu   | long   | Phiên bản API I2PControl mà client yêu cầu. Sử dụng `1`. |
| `Password` | Yêu cầu   | String | Mật khẩu dùng để xác thực với I2PControl.                |
| `API`      | Phản hồi  | long   | Phiên bản API chính được triển khai bởi server.          |
| `Token`    | Phản hồi  | String | Mã xác thực dùng cho các yêu cầu tiếp theo.              |
---

Bạn phải bao gồm `Token` đó trong tất cả các yêu cầu tiếp theo trong `params`.

## 4. Phương thức & Điểm cuối

### 4.1 RouterInfo

---

Lấy dữ liệu telemetry chính về router.

```bash
curl -s -H "Content-Type: application/json" \
  -d '{
        "jsonrpc": "2.0",
        "id": "2",
        "method": "RouterInfo",
        "params": {
          "Token": "a1b2c3d4e5",
          "i2p.router.version": "",
          "i2p.router.status": "",
          "i2p.router.net.status": "",
          "i2p.router.net.tunnels.participating": "",
          "i2p.router.net.bw.inbound.1s": "",
          "i2p.router.net.bw.outbound.1s": ""
        }
      }' \
  http://127.0.0.1:7657/jsonrpc/
```
**Ví dụ Yêu cầu**

#### Enum Mã Trạng Thái (`i2p.router.net.status`)

| Key                                    | Type   | Mô tả                                                                 |
|----------------------------------------|--------|----------------------------------------------------------------------|
| `i2p.router.status`                    | String | Trạng thái router dưới dạng văn bản tự do, đã được dịch để hiển thị. |
| `i2p.router.uptime`                    | long   | Thời gian hoạt động của router tính bằng mili giây. Một số phiên bản i2pd cũ hơn có thể trả về chuỗi ký tự. |
| `i2p.router.version`                   | String | Phiên bản đầy đủ của router.                                         |
| `i2p.router.net.status`                | long   | Mã trạng thái mạng; xem bảng dưới đây.                               |
| `i2p.router.net.bw.inbound.1s`         | double | Băng thông đầu vào hiện tại tính bằng byte mỗi giây.                 |
| `i2p.router.net.bw.inbound.15s`        | double | Băng thông trung bình đầu vào trong 15 giây tính bằng byte mỗi giây. |
| `i2p.router.net.bw.outbound.1s`        | double | Băng thông đầu ra hiện tại tính bằng byte mỗi giây.                  |
| `i2p.router.net.bw.outbound.15s`       | double | Băng thông trung bình đầu ra trong 15 giây tính bằng byte mỗi giây.  |
| `i2p.router.net.tunnels.participating` | long   | Số lượng tunnel mà router này đang tham gia.                         |
#### Liệt kê mã trạng thái (`i2p.router.net.status`)

| Code | Ý nghĩa                                             |
|------|-----------------------------------------------------|
| 0    | Thành công                                          |
| 1    | ĐANG KIỂM TRA                                       |
| 2    | BỊ CHẶN BỞI TƯỜNG LỬA                               |
| 3    | ẨN                                                 |
| 4    | CẢNH BÁO: BỊ CHẶN BỞI TƯỜNG LỬA VÀ KẾT NỐI NHANH     |
| 5    | CẢNH BÁO: BỊ CHẶN BỞI TƯỜNG LỬA VÀ LÀ MÁY FLOODFILL   |
| 6    | CẢNH BÁO: BỊ CHẶN BỞI TƯỜNG LỬA NHƯNG CÓ TCP ĐẦU VÀO |
| 7    | CẢNH BÁO: BỊ CHẶN BỞI TƯỜNG LỬA VÀ UDP BỊ TẮT        |
| 8    | LỖI I2CP                                            |
| 9    | LỖI ĐỒNG HỒ LỆCH THỜI GIAN                          |
| 10   | LỖI ĐỊA CHỈ TCP RIÊNG TƯ                             |
| 11   | LỖI NAT ĐỐI XỨNG                                    |
| 12   | LỖI CỔNG UDP ĐÃ ĐƯỢC SỬ DỤNG                        |
| 13   | LỖI: KHÔNG CÓ PEER NÀO HOẠT ĐỘNG, KIỂM TRA KẾT NỐI VÀ TƯỜNG LỬA |
| 14   | LỖI: UDP BỊ TẮT VÀ TCP CHƯA ĐƯỢC THIẾT LẬP           |
#### Cơ sở dữ liệu mạng và các trường ngang hàng

| Key                                  | Type    | Mô tả                                              |
|--------------------------------------|---------|----------------------------------------------------|
| `i2p.router.netdb.knownpeers`        | long    | Số lượng peer đã biết, không bao gồm router cục bộ. |
| `i2p.router.netdb.activepeers`       | long    | Số lượng peer đang hoạt động.                     |
| `i2p.router.netdb.fastpeers`         | long    | Số lượng peer được phân loại là nhanh.            |
| `i2p.router.netdb.highcapacitypeers` | long    | Số lượng peer được phân loại là có sức chứa cao.  |
| `i2p.router.netdb.isreseeding`       | boolean | Cho biết liệu việc reseed có đang được thực hiện hay không. |
**Các Trường Phản Hồi (result)** Theo tài liệu chính thức (GetI2P): - `i2p.router.status` (String) — trạng thái có thể đọc được - `i2p.router.uptime` (long) — mili giây (hoặc chuỗi cho i2pd cũ hơn) :contentReference[oaicite:0]{index=0} - `i2p.router.version` (String) — chuỗi phiên bản :contentReference[oaicite:1]{index=1} - `i2p.router.net.bw.inbound.1s`, `i2p.router.net.bw.inbound.15s` (double) — băng thông đến theo B/s :contentReference[oaicite:2]{index=2} - `i2p.router.net.bw.outbound.1s`, `i2p.router.net.bw.outbound.15s` (double) — băng thông đi theo B/s :contentReference[oaicite:3]{index=3} - `i2p.router.net.status` (long) — mã trạng thái số (xem enum bên dưới) :contentReference[oaicite:4]{index=4} - `i2p.router.net.tunnels.participating` (long) — số lượng tunnel tham gia :contentReference[oaicite:5]{index=5} - `i2p.router.netdb.activepeers`, `fastpeers`, `highcapacitypeers` (long) — thống kê peer của netDB :contentReference[oaicite:6]{index=6} - `i2p.router.netdb.isreseeding` (boolean) — có đang thực hiện reseed hay không :contentReference[oaicite:7]{index=7} - `i2p.router.netdb.knownpeers` (long) — tổng số peer đã biết :contentReference[oaicite:8]{index=8}

### 4.2 GetRate

---

| Tham số | Kiểu   | Mô tả                        |
|---------|--------|------------------------------|
| `Stat`  | Chuỗi  | Tên RateStat của bộ định tuyến. |
| `Period`| dài    | Chu kỳ tính theo mili giây.  |
Được sử dụng để lấy các chỉ số tốc độ (ví dụ: băng thông, tỷ lệ thành công tunnel) trong một khoảng thời gian nhất định.

```bash
curl -s -H "Content-Type: application/json" \
  -d '{
        "jsonrpc": "2.0",
        "id": "3",
        "method": "GetRate",
        "params": {
          "Token": "a1b2c3d4e5",
          "Stat": "bw.combined",
          "Period": 60000
        }
      }' \
  http://127.0.0.1:7657/jsonrpc/
```
**Ví dụ Yêu cầu**

```json
{
  "jsonrpc": "2.0",
  "id": "3",
  "result": {
    "Result": 12345.67
  }
}
```
**Phản hồi mẫu**

### 4.3 RouterManager

---

| Tham số             | Kết quả           | Mô tả                                                                |
|---------------------|-------------------|----------------------------------------------------------------------|
| `Restart`           | null              | Khởi động lại bộ định tuyến ngay lập tức.                            |
| `RestartGraceful`   | null              | Khởi động lại sau khi các tunnel tham gia hết hạn.                  |
| `Shutdown`          | null              | Tắt bộ định tuyến ngay lập tức.                                     |
| `ShutdownGraceful`  | null              | Tắt sau khi các tunnel tham gia hết hạn.                            |
| `Reseed`            | null              | Bắt đầu quá trình reseed cho bộ định tuyến.                         |
| `FindUpdates`       | boolean hoặc String | Chặn. Tìm kiếm bản cập nhật bộ định tuyến đã ký.                   |
| `Update`            | String            | Chặn. Bắt đầu cập nhật bộ định tuyến đã ký và trả về trạng thái cuối. |
Thực hiện các hành động quản trị.

```bash
curl -s -H "Content-Type: application/json" \
  -d '{
        "jsonrpc": "2.0",
        "id": "4",
        "method": "RouterManager",
        "params": {
          "Token": "a1b2c3d4e5",
          "Restart": true
        }
      }' \
  http://127.0.0.1:7657/jsonrpc/
```
**Các tham số / phương thức được phép**   - `Restart`, `RestartGraceful`   - `Shutdown`, `ShutdownGraceful`   - `Reseed`, `FindUpdates`, `Update` :contentReference[oaicite:10]{index=10}

```json
{
  "jsonrpc": "2.0",
  "id": "4",
  "result": {
    "Restart": null
  }
}
```
**Ví dụ Request**

### 4.4 NetworkSetting

**Phản hồi thành công**

---

| Chìa khóa                            | Giá trị được chấp nhận                                   | Mô tả                                                         |
|--------------------------------------|----------------------------------------------------------|--------------------------------------------------------------|
| `i2p.router.net.ntcp.port`           | Chuỗi, 1–65535                                          | Cổng NTCP; thay đổi yêu cầu khởi động lại.                  |
| `i2p.router.net.ntcp.hostname`       | Chuỗi                                                   | Tên máy chủ NTCP; thay đổi yêu cầu khởi động lại.           |
| `i2p.router.net.ntcp.autoip`         | `always`, `true`, hoặc `false`                          | Tự động chọn địa chỉ cho NTCP.                               |
| `i2p.router.net.ssu.port`            | Chuỗi, 1–65535                                          | Cổng SSU; thay đổi yêu cầu khởi động lại.                   |
| `i2p.router.net.ssu.hostname`        | Chuỗi                                                   | Tên máy chủ ngoài SSU; thay đổi yêu cầu khởi động lại.       |
| `i2p.router.net.ssu.autoip`          | `ssu`, `local,ssu`, `upnp,ssu`, hoặc `local,upnp,ssu`   | Các nguồn phát hiện địa chỉ cho SSU.                         |
| `i2p.router.net.ssu.detectedip`      | null                                                    | Địa chỉ SSU được phát hiện (chỉ đọc).                        |
| `i2p.router.net.upnp`                | Chuỗi                                                   | Thiết lập UPnP.                                              |
| `i2p.router.net.bw.share`            | Chuỗi, 0–100                                            | Phần trăm băng thông dùng cho các tunnel tham gia.          |
| `i2p.router.net.bw.in`               | Chuỗi số nguyên không âm                                | Giới hạn băng thông vào tính theo KiB/s.                    |
| `i2p.router.net.bw.out`              | Chuỗi số nguyên không âm                                | Giới hạn băng thông ra tính theo KiB/s.                     |
| `i2p.router.net.laptopmode`          | Chuỗi                                                   | Thiết lập chế độ máy tính xách tay.                          |
Lấy hoặc thiết lập các tham số cấu hình mạng (cổng, upnp, chia sẻ băng thông, v.v.)

```bash
curl -s -H "Content-Type: application/json" \
  -d '{
        "jsonrpc": "2.0",
        "id": "5",
        "method": "NetworkSetting",
        "params": {
          "Token": "a1b2c3d4e5",
          "i2p.router.net.ntcp.port": null,
          "i2p.router.net.ssu.port": null,
          "i2p.router.net.bw.share": null,
          "i2p.router.net.upnp": null
        }
      }' \
  http://127.0.0.1:7657/jsonrpc/
```
**Ví dụ Request (lấy giá trị hiện tại)**

```json
{
  "jsonrpc": "2.0",
  "id": "5",
  "result": {
    "i2p.router.net.ntcp.port": "1234",
    "i2p.router.net.ssu.port": "5678",
    "i2p.router.net.bw.share": "50",
    "i2p.router.net.upnp": "true",
    "SettingsSaved": false,
    "RestartNeeded": false
  }
}
```
**Phản Hồi Mẫu**

> Lưu ý: các phiên bản i2pd trước 2.41 có thể trả về các kiểu số thay vì chuỗi — client nên xử lý cả hai. :contentReference[oaicite:11]{index=11}

### 4.5 Cài đặt Nâng cao

---

| Tham số | Kiểu | Mô tả |
|-----------|---------------------|-----------------------------------------------------------------------|
| `get`     | Chuỗi              | Trả về một thiết lập bên trong đối tượng kết quả `get`.                     |
| `getAll`  | không áp dụng       | Trả về toàn bộ bản đồ cấu hình bên trong `getAll`.               |
| `set`     | Bản đồ<String, String> | Cập nhật các thiết lập được cung cấp mà không xóa các khóa khác.            |
| `setAll`  | Bản đồ<String, String> | **Có tính phá hủy:** thay thế tất cả các thiết lập và xóa các khóa không được cung cấp. |
Cho phép thao tác các tham số bên trong router.

**Ví dụ Yêu cầu**

```bash
curl -s -H "Content-Type: application/json" \
  -d '{
        "jsonrpc": "2.0",
        "id": "6",
        "method": "AdvancedSettings",
        "params": {
          "Token": "a1b2c3d4e5",
          "set": {
            "router.sharePercentage": "75",
            "i2np.flushInterval": "6000"
          }
        }
      }' \
  http://127.0.0.1:7657/jsonrpc/
```
**Ví dụ Phản hồi**

```json
{
  "jsonrpc": "2.0",
  "id": "6",
  "result": {}
}
```
---

### Mã Lỗi Chuẩn JSON-RPC2

---

| Tham số | Kiểu | Mô tả |
|-----------|--------|-----------------------------|
| `Echo`    | Chuỗi | Giá trị được trả về như `Result`. |
```json
{
  "jsonrpc": "2.0",
  "id": "7",
  "method": "Echo",
  "params": {
    "Token": "a1b2c3d4e5",
    "Echo": "hello"
  }
}
```
```json
{
  "jsonrpc": "2.0",
  "id": "7",
  "result": {
    "Result": "hello"
  }
}
```
---

### Mã Lỗi Cụ Thể của I2PControl

Quản lý chính I2PControl. Trình xử lý Java hiện tại hỗ trợ thay đổi mật khẩu.

| Tham số               | Kiểu   | Mô tả                                                                      |
|-----------------------|--------|----------------------------------------------------------------------------|
| `i2pcontrol.password` | Chuỗi  | Đặt mật khẩu I2PControl mới và hủy các mã xác thực hiện tại.               |
Kết quả chứa `SettingsSaved`. Nếu mật khẩu đã được thay đổi, kết quả cũng chứa `"i2pcontrol.password": null`. Các cài đặt địa chỉ và cổng lắng nghe từ plugin độc lập cũ không còn hiệu lực trong bộ xử lý Java hiện tại.

> **Mật khẩu mặc định:** `itoopie` — đây là mật khẩu gốc từ nhà máy và **nên được thay đổi** ngay lập tức để đảm bảo bảo mật.

## 5. Mã Lỗi

### Mã lỗi JSON-RPC2 tiêu chuẩn

| Code   | Ý nghĩa               |
|--------|-----------------------|
| -32700 | Lỗi phân tích JSON   |
| -32600 | Yêu cầu không hợp lệ  |
| -32601 | Không tìm thấy phương thức |
| -32602 | Tham số không hợp lệ  |
| -32603 | Lỗi nội bộ            |
### Mã lỗi riêng của I2PControl

| Mã lỗi  | Ý nghĩa                                                                                  |
|--------|------------------------------------------------------------------------------------------|
| -32001 | Mật khẩu cung cấp không hợp lệ                                                           |
| -32002 | Không có token xác thực được cung cấp                                                    |
| -32003 | Token xác thực không tồn tại                                                             |
| -32004 | Token xác thực cung cấp đã hết hạn và sẽ bị xóa                                          |
| -32005 | Phiên bản API I2PControl được dùng chưa được chỉ định, nhưng bắt buộc phải chỉ định      |
| -32006 | Phiên bản API I2PControl được chỉ định không được I2PControl hỗ trợ                     |
> **Mật khẩu mặc định:** `itoopie` — đây là mật khẩu gốc từ nhà máy và **nên được thay đổi** ngay lập tức để đảm bảo bảo mật.

## 6. Sử dụng & Các phương pháp tốt nhất

- Luôn bao gồm tham số `Token` (trừ khi đang xác thực).  
- Thay đổi mật khẩu mặc định (`itoopie`) khi sử dụng lần đầu.  
- Đối với Java I2P, đảm bảo webapp I2PControl được kích hoạt qua WebApps.  
- Chuẩn bị cho những biến đổi nhỏ: một số trường có thể là số hoặc chuỗi, tùy thuộc vào phiên bản I2P.  
- Ngắt dòng các chuỗi trạng thái dài để hiển thị thân thiện hơn.

> **Mật khẩu mặc định:** `itoopie` — đây là mật khẩu gốc từ nhà máy và **nên được thay đổi** ngay lập tức để đảm bảo bảo mật.
