---
title: "Tạo SSH Tunnel để Truy cập I2P từ Xa"
description: "Tìm hiểu cách tạo SSH tunnel bảo mật trên Windows, Linux và Mac để truy cập router I2P từ xa của bạn"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

Một SSH tunnel cung cấp kết nối mã hóa an toàn để truy cập console của I2P router từ xa hoặc các dịch vụ khác. Hướng dẫn này chỉ cho bạn cách tạo SSH tunnel trên các hệ thống Windows, Linux và Mac.

## SSH Tunnel là gì?

SSH tunnel là phương pháp định tuyến dữ liệu và thông tin một cách an toàn qua kết nối SSH được mã hóa. Hãy nghĩ về nó như việc tạo ra một "đường ống" được bảo vệ xuyên qua internet - dữ liệu của bạn di chuyển qua tunnel được mã hóa này, ngăn chặn bất kỳ ai chặn bắt hoặc đọc được nó trong suốt quá trình truyền tải.

SSH tunneling đặc biệt hữu ích cho:

- **Truy cập các router I2P từ xa**: Kết nối tới bảng điều khiển I2P của bạn đang chạy trên máy chủ từ xa
- **Kết nối bảo mật**: Toàn bộ lưu lượng được mã hóa đầu-cuối
- **Vượt qua các hạn chế**: Truy cập các dịch vụ trên hệ thống từ xa như thể chúng đang chạy cục bộ
- **Chuyển tiếp cổng**: Ánh xạ một cổng cục bộ tới một dịch vụ từ xa

Trong bối cảnh I2P, bạn có thể sử dụng SSH tunnel để truy cập bảng điều khiển I2P router của mình (thường ở cổng 7657) trên máy chủ từ xa bằng cách chuyển tiếp nó đến một cổng cục bộ trên máy tính của bạn.

## Yêu cầu tiên quyết

Trước khi tạo một SSH tunnel, bạn sẽ cần:

- **SSH client**:
  - Windows: [PuTTY](https://www.putty.org/) (tải miễn phí)
  - Linux/Mac: SSH client tích hợp sẵn (qua Terminal)
- **Truy cập máy chủ từ xa**:
  - Tên người dùng cho máy chủ từ xa
  - Địa chỉ IP hoặc hostname của máy chủ từ xa
  - Mật khẩu SSH hoặc xác thực bằng key
- **Cổng local khả dụng**: Chọn một cổng chưa sử dụng trong khoảng 1-65535 (7657 thường được dùng cho I2P)

## Hiểu về Lệnh Tunnel

Lệnh tạo SSH tunnel tuân theo mẫu sau:

```
ssh -L [local_port]:[destination_ip]:[destination_port] [username]@[remote_server]
```
**Giải thích các tham số**: - **local_port**: Cổng trên máy cục bộ của bạn (ví dụ: 7657) - **destination_ip**: Thường là `127.0.0.1` (localhost trên máy chủ từ xa) - **destination_port**: Cổng của dịch vụ trên máy chủ từ xa (ví dụ: 7657 cho I2P) - **username**: Tên người dùng của bạn trên máy chủ từ xa - **remote_server**: Địa chỉ IP hoặc hostname của máy chủ từ xa

**Ví dụ**: `ssh -L 7657:127.0.0.1:7657 i2p@20.228.143.58`

Lệnh này tạo một tunnel trong đó: - Cổng local 7657 trên máy của bạn chuyển tiếp đến... - Cổng 7657 trên localhost của server từ xa (nơi I2P đang chạy) - Kết nối với tư cách user `i2p` đến server `20.228.143.58`

## Tạo SSH Tunnel trên Windows

Người dùng Windows có thể tạo SSH tunnel bằng PuTTY, một SSH client miễn phí.

### Step 1: Download and Install PuTTY

Tải PuTTY từ [putty.org](https://www.putty.org/) và cài đặt nó trên hệ thống Windows của bạn.

### Step 2: Configure the SSH Connection

Mở PuTTY và cấu hình kết nối của bạn:

1. Trong danh mục **Session**:
   - Nhập địa chỉ IP hoặc tên máy chủ của máy chủ từ xa vào trường **Host Name**
   - Đảm bảo **Port** được đặt là 22 (cổng SSH mặc định)
   - Loại kết nối phải là **SSH**

![Cấu hình phiên PuTTY](/images/guides/ssh-tunnel/sshtunnel_1.webp)

### Step 3: Configure the Tunnel

Điều hướng đến **Connection → SSH → Tunnels** trong thanh bên trái:

1. **Cổng nguồn**: Nhập cổng cục bộ bạn muốn sử dụng (ví dụ: `7657`)
2. **Đích đến**: Nhập `127.0.0.1:7657` (localhost:port trên máy chủ từ xa)
3. Nhấp **Add** để thêm tunnel
4. Tunnel sẽ xuất hiện trong danh sách "Forwarded ports"

![Cấu hình tunnel PuTTY](/images/guides/ssh-tunnel/sshtunnel_2.webp)

### Step 4: Connect

1. Nhấp vào **Open** để bắt đầu kết nối
2. Nếu đây là lần đầu tiên bạn kết nối, bạn sẽ thấy cảnh báo bảo mật - nhấp vào **Yes** để tin tưởng máy chủ
3. Nhập tên người dùng của bạn khi được yêu cầu
4. Nhập mật khẩu của bạn khi được yêu cầu

![Kết nối PuTTY đã được thiết lập](/images/guides/ssh-tunnel/sshtunnel_3.webp)

Sau khi kết nối, bạn có thể truy cập bảng điều khiển I2P từ xa bằng cách mở trình duyệt và truy cập `http://127.0.0.1:7657`

### Bước 1: Tải xuống và Cài đặt PuTTY

Để tránh phải cấu hình lại mỗi lần:

1. Quay lại danh mục **Session**
2. Nhập tên vào **Saved Sessions** (ví dụ: "I2P Tunnel")
3. Nhấp **Save**
4. Lần sau, chỉ cần tải phiên này và nhấp **Open**

## Creating SSH Tunnels on Linux

Các hệ thống Linux có SSH được tích hợp sẵn trong terminal, giúp việc tạo tunnel nhanh chóng và đơn giản.

### Bước 2: Cấu hình kết nối SSH

Mở terminal và chạy lệnh SSH tunnel:

```bash
ssh -L 7657:127.0.0.1:7657 i2p@20.228.143.58
```
**Thay thế**: - `7657` (lần xuất hiện đầu tiên): Cổng local mong muốn của bạn - `127.0.0.1:7657`: Địa chỉ đích và cổng trên máy chủ từ xa - `i2p`: Tên người dùng của bạn trên máy chủ từ xa - `20.228.143.58`: Địa chỉ IP của máy chủ từ xa

![Tạo SSH tunnel trên Linux](/images/guides/ssh-tunnel/sshtunnel_4.webp)

Khi được nhắc, hãy nhập mật khẩu của bạn. Sau khi kết nối, tunnel sẽ hoạt động.

Truy cập bảng điều khiển I2P từ xa của bạn tại `http://127.0.0.1:7657` trong trình duyệt.

### Bước 3: Cấu hình Tunnel

Tunnel sẽ duy trì hoạt động trong suốt thời gian phiên SSH đang chạy. Để giữ nó chạy trong nền:

```bash
ssh -f -N -L 7657:127.0.0.1:7657 i2p@20.228.143.58
```
**Các cờ bổ sung**: - `-f`: Chạy SSH ở chế độ nền - `-N`: Không thực thi lệnh từ xa (chỉ tunnel)

Để đóng một tunnel chạy nền, tìm và kết thúc tiến trình SSH:

```bash
ps aux | grep ssh
kill [process_id]
```
### Bước 4: Kết nối

Để có bảo mật và tiện lợi tốt hơn, hãy sử dụng xác thực khóa SSH:

1. Tạo cặp khóa SSH (nếu bạn chưa có):
   ```bash
   ssh-keygen -t ed25519 -C "your_email@example.com"
   ```

2. Sao chép khóa công khai của bạn lên máy chủ từ xa:
   ```bash
   ssh-copy-id i2p@20.228.143.58
   ```

3. Bây giờ bạn có thể kết nối mà không cần mật khẩu:
   ```bash
   ssh -L 7657:127.0.0.1:7657 i2p@20.228.143.58
   ```

## Creating SSH Tunnels on Mac

Các hệ thống Mac sử dụng cùng SSH client như Linux, do đó quy trình là giống hệt nhau.

### Tùy chọn: Lưu phiên làm việc của bạn

Mở Terminal (Applications → Utilities → Terminal) và chạy:

```bash
ssh -L 7657:127.0.0.1:7657 i2p@20.228.143.58
```
**Thay thế**: - `7657` (lần xuất hiện đầu tiên): Cổng local mong muốn của bạn - `127.0.0.1:7657`: Địa chỉ và cổng đích trên máy chủ từ xa - `i2p`: Tên người dùng của bạn trên máy chủ từ xa - `20.228.143.58`: Địa chỉ IP của máy chủ từ xa

![Tạo SSH tunnel trên Mac](/images/guides/ssh-tunnel/sshtunnel_5.webp)

Nhập mật khẩu của bạn khi được yêu cầu. Sau khi kết nối, truy cập bảng điều khiển I2P từ xa của bạn tại `http://127.0.0.1:7657`

### Background Tunnels on Mac

Tương tự như Linux, bạn có thể chạy tunnel ở chế độ nền:

```bash
ssh -f -N -L 7657:127.0.0.1:7657 i2p@20.228.143.58
```
### Sử dụng Terminal

Thiết lập SSH key trên Mac giống hệt như trên Linux:

```bash
# Generate key (if needed)
ssh-keygen -t ed25519 -C "your_email@example.com"

# Copy to remote server
ssh-copy-id i2p@20.228.143.58
```
## Common Use Cases

### Giữ Tunnel Hoạt Động

Trường hợp sử dụng phổ biến nhất - truy cập bảng điều khiển I2P router từ xa của bạn:

```bash
ssh -L 7657:127.0.0.1:7657 user@remote-server
```
Sau đó mở `http://127.0.0.1:7657` trong trình duyệt của bạn.

### Sử dụng SSH Keys (Khuyến nghị)

Chuyển tiếp nhiều cổng cùng lúc:

```bash
ssh -L 7657:127.0.0.1:7657 -L 7658:127.0.0.1:7658 user@remote-server
```
Điều này chuyển tiếp cả cổng 7657 (bảng điều khiển I2P) và 7658 (dịch vụ khác).

### Custom Local Port

Sử dụng cổng cục bộ khác nếu 7657 đã được sử dụng:

```bash
ssh -L 8080:127.0.0.1:7657 user@remote-server
```
Thay vào đó, truy cập bảng điều khiển I2P tại `http://127.0.0.1:8080`.

## Troubleshooting

### Sử dụng Terminal

**Lỗi**: "bind: Address already in use"

**Giải pháp**: Chọn một cổng cục bộ khác hoặc kết thúc tiến trình đang sử dụng cổng đó:

```bash
# Linux/Mac - find process on port 7657
lsof -i :7657

# Kill the process
kill [process_id]
```
### Tunnel Nền trên Mac

**Lỗi**: "Connection refused" hoặc "channel 2: open failed"

**Nguyên nhân có thể**: - Dịch vụ từ xa không chạy (kiểm tra router I2P đang chạy trên máy chủ từ xa) - Tường lửa chặn kết nối - Cổng đích không chính xác

**Giải pháp**: Xác minh I2P router đang chạy trên máy chủ từ xa:

```bash
ssh user@remote-server "systemctl status i2p"
```
### Thiết lập SSH Key trên Mac

**Lỗi**: "Permission denied" hoặc "Authentication failed"

**Các nguyên nhân có thể xảy ra**: - Tên người dùng hoặc mật khẩu không chính xác - SSH key chưa được cấu hình đúng cách - Quyền truy cập SSH bị vô hiệu hóa trên máy chủ từ xa

**Giải pháp**: Xác minh thông tin xác thực và đảm bảo truy cập SSH đã được bật trên máy chủ từ xa.

### Tunnel Drops Connection

**Lỗi**: Kết nối bị ngắt sau một khoảng thời gian không hoạt động

**Giải pháp**: Thêm cài đặt keep-alive vào file cấu hình SSH của bạn (`~/.ssh/config`):

```
Host remote-server
    ServerAliveInterval 60
    ServerAliveCountMax 3
```
## Security Best Practices

- **Sử dụng SSH keys**: An toàn hơn mật khẩu, khó bị xâm phạm hơn
- **Vô hiệu hóa xác thực bằng mật khẩu**: Sau khi đã thiết lập SSH keys, hãy tắt đăng nhập bằng mật khẩu trên máy chủ
- **Sử dụng mật khẩu mạnh**: Nếu sử dụng xác thực bằng mật khẩu, hãy dùng mật khẩu mạnh và duy nhất
- **Giới hạn truy cập SSH**: Cấu hình các quy tắc tường lửa để giới hạn truy cập SSH chỉ từ các IP đáng tin cậy
- **Giữ SSH luôn cập nhật**: Thường xuyên cập nhật phần mềm SSH client và server
- **Giám sát logs**: Kiểm tra các logs SSH trên máy chủ để phát hiện hoạt động đáng ngờ
- **Sử dụng cổng SSH không chuẩn**: Thay đổi cổng SSH mặc định (22) để giảm các cuộc tấn công tự động

## Tạo SSH Tunnel trên Linux

### Truy cập I2P Console

Tạo một script để tự động thiết lập các tunnel:

```bash
#!/bin/bash
# i2p-tunnel.sh

ssh -f -N -L 7657:127.0.0.1:7657 i2p@20.228.143.58
echo "I2P tunnel established"
```
Làm cho nó có thể thực thi:

```bash
chmod +x i2p-tunnel.sh
./i2p-tunnel.sh
```
### Nhiều Tunnel

Tạo một systemd service để tự động khởi tạo tunnel:

```bash
sudo nano /etc/systemd/system/i2p-tunnel.service
```
Thêm:

```ini
[Unit]
Description=I2P SSH Tunnel
After=network.target

[Service]
ExecStart=/usr/bin/ssh -NT -o ServerAliveInterval=60 -o ExitOnForwardFailure=yes -L 7657:127.0.0.1:7657 i2p@20.228.143.58
Restart=always
RestartSec=10
User=your-username

[Install]
WantedBy=multi-user.target
```
Kích hoạt và khởi động:

```bash
sudo systemctl enable i2p-tunnel
sudo systemctl start i2p-tunnel
```
## Advanced Tunneling

### Cổng Cục Bộ Tùy Chỉnh

Tạo một SOCKS proxy cho chuyển tiếp động:

```bash
ssh -D 8080 user@remote-server
```
Cấu hình trình duyệt của bạn để sử dụng `127.0.0.1:8080` làm SOCKS5 proxy.

### Reverse Tunneling

Cho phép máy chủ từ xa truy cập các dịch vụ trên máy cục bộ của bạn:

```bash
ssh -R 7657:127.0.0.1:7657 user@remote-server
```
### Cổng Đã Được Sử Dụng

Tunnel thông qua máy chủ trung gian:

```bash
ssh -J jumphost.example.com -L 7657:127.0.0.1:7657 user@final-server
```
## Conclusion

SSH tunneling là một công cụ mạnh mẽ để truy cập an toàn các router I2P từ xa và các dịch vụ khác. Cho dù bạn đang sử dụng Windows, Linux hay Mac, quy trình này đều đơn giản và cung cấp mã hóa mạnh mẽ cho các kết nối của bạn.

Để được hỗ trợ thêm hoặc có thắc mắc, hãy truy cập cộng đồng I2P: - **Diễn đàn**: [i2pforum.net](https://i2pforum.net) - **IRC**: #i2p trên nhiều mạng khác nhau - **Tài liệu**: [I2P Docs](/docs/)

Tôi đã nhận được yêu cầu của bạn, nhưng tôi không thấy văn bản tiếng Anh nào cần dịch trong tin nhắn của bạn. Phần "Text to translate:" không có nội dung phía sau dấu "---".

Vui lòng cung cấp văn bản tiếng Anh cần dịch và tôi sẽ thực hiện ngay lập tức.

*Hướng dẫn ban đầu được tạo bởi [Stormy Cloud](https://www.stormycloud.org), được điều chỉnh cho tài liệu I2P.*
