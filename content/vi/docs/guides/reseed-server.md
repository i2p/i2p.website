---
title: "Tạo và Chạy Máy Chủ Reseed I2P"
description: "Hướng dẫn đầy đủ về cách thiết lập và vận hành máy chủ reseed I2P để giúp các router mới tham gia mạng lưới"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

Reseed host là cơ sở hạ tầng quan trọng cho mạng lưới I2P, cung cấp cho các router mới một nhóm node ban đầu trong quá trình khởi động. Hướng dẫn này sẽ chỉ cho bạn cách thiết lập và vận hành reseed server của riêng bạn.

## I2P Reseed Server là gì?

Một máy chủ reseed I2P giúp tích hợp các router mới vào mạng I2P bằng cách:

- **Cung cấp khám phá peer ban đầu**: Các router mới nhận được một tập hợp các node mạng khởi đầu để kết nối
- **Khôi phục bootstrap**: Hỗ trợ các router đang gặp khó khăn trong việc duy trì kết nối
- **Phân phối bảo mật**: Quá trình reseeding được mã hóa và ký số để đảm bảo an ninh mạng

Khi một I2P router mới khởi động lần đầu tiên (hoặc đã mất tất cả các kết nối peer), nó sẽ liên hệ với các reseed server để tải xuống một tập hợp thông tin router ban đầu. Điều này cho phép router mới bắt đầu xây dựng netDb riêng của mình và thiết lập các tunnel.

## Điều kiện tiên quyết

Trước khi bắt đầu, bạn sẽ cần:

- Một máy chủ Linux (khuyến nghị Debian/Ubuntu) với quyền truy cập root
- Một tên miền trỏ về máy chủ của bạn
- Ít nhất 1GB RAM và 10GB dung lượng đĩa
- Một I2P router đang chạy trên máy chủ để điền dữ liệu vào network database
- Kiến thức cơ bản về quản trị hệ thống Linux

## Chuẩn bị Máy chủ

### Step 1: Update System and Install Dependencies

Đầu tiên, cập nhật hệ thống của bạn và cài đặt các gói cần thiết:

```bash
sudo apt update && sudo apt upgrade -y && sudo apt-get install golang-go git make docker.io docker-compose -y
```
Lệnh này cài đặt: - **golang-go**: Môi trường thực thi ngôn ngữ lập trình Go - **git**: Hệ thống quản lý phiên bản - **make**: Công cụ tự động hóa biên dịch - **docker.io & docker-compose**: Nền tảng container để chạy Nginx Proxy Manager

![Cài đặt các gói cần thiết](/images/guides/reseed/reseed_01.png)

### Step 2: Clone and Build Reseed Tools

Clone kho reseed-tools và build ứng dụng:

```bash
cd /home/i2p
git clone https://i2pgit.org/idk/reseed-tools
cd reseed-tools
make build
sudo make install
```
Gói `reseed-tools` cung cấp chức năng cốt lõi để chạy một reseed server. Nó xử lý: - Thu thập thông tin router từ network database cục bộ của bạn - Đóng gói thông tin router vào các file SU3 đã ký - Phục vụ các file này qua HTTPS

![Sao chép repository reseed-tools](/images/guides/reseed/reseed_02.png)

### Step 3: Generate SSL Certificate

Tạo chứng chỉ SSL và khóa riêng cho máy chủ reseed của bạn:

```bash
su - i2p -c 'reseed-tools reseed --signer=admin@stormycloud.org --netdb=/home/i2p/.i2p/netDb --port=8443 --ip=127.0.0.1 --trustProxy'
```
**Các tham số quan trọng**: - `--signer`: Địa chỉ email của bạn (thay thế `admin@stormycloud.org` bằng địa chỉ của bạn) - `--netdb`: Đường dẫn đến cơ sở dữ liệu mạng (network database) của I2P router - `--port`: Cổng nội bộ (khuyến nghị 8443) - `--ip`: Gắn với localhost (chúng ta sẽ sử dụng reverse proxy để truy cập công khai) - `--trustProxy`: Tin tưởng các header X-Forwarded-For từ reverse proxy

Lệnh này sẽ tạo ra: - Một khóa riêng để ký các tệp SU3 - Một chứng chỉ SSL cho các kết nối HTTPS an toàn

![Tạo chứng chỉ SSL](/images/guides/reseed/reseed_03.png)

### Bước 1: Cập nhật Hệ thống và Cài đặt Các Gói Phụ thuộc

**Quan trọng**: Sao lưu an toàn các khóa đã tạo nằm trong `/home/i2p/.reseed/`:

```bash
sudo tar -czf reseed-keys-backup.tar.gz /home/i2p/.reseed/
```
Lưu trữ bản sao lưu này ở một vị trí an toàn, được mã hóa và hạn chế quyền truy cập. Những khóa này rất quan trọng cho hoạt động của reseed server và cần được bảo vệ cẩn thận.

## Configuring the Service

### Bước 2: Clone và Build Reseed Tools

Tạo một systemd service để chạy reseed server tự động:

```bash
sudo tee /etc/systemd/system/reseed.service <<EOF
[Unit]
Description=Reseed Service
After=network.target

[Service]
User=i2p
WorkingDirectory=/home/i2p
ExecStart=/bin/bash -c 'reseed-tools reseed --signer=admin@stormycloud.org --netdb=/home/i2p/.i2p/netDb --port=8443 --ip=127.0.0.1 --trustProxy'
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF
```
**Hãy nhớ thay thế** `admin@stormycloud.org` bằng địa chỉ email của riêng bạn.

Bây giờ hãy kích hoạt và khởi động dịch vụ:

```bash
sudo systemctl daemon-reload
sudo systemctl enable reseed
sudo systemctl start reseed
```
Kiểm tra xem dịch vụ đang chạy:

```bash
sudo systemctl status reseed
```
![Xác minh trạng thái dịch vụ reseed](/images/guides/reseed/reseed_04.png)

### Bước 3: Tạo Chứng chỉ SSL

Để đạt hiệu suất tối ưu, bạn có thể muốn khởi động lại dịch vụ reseed định kỳ để làm mới thông tin router:

```bash
sudo crontab -e
```
Thêm dòng này để khởi động lại dịch vụ mỗi 3 giờ:

```
0 */3 * * * systemctl restart reseed
```
## Setting Up Reverse Proxy

Máy chủ reseed chạy trên localhost:8443 và cần một reverse proxy để xử lý lưu lượng HTTPS công khai. Chúng tôi khuyến nghị sử dụng Nginx Proxy Manager vì dễ sử dụng.

### Bước 4: Sao lưu các khóa của bạn

Triển khai Nginx Proxy Manager sử dụng Docker:

```bash
docker run -d \
--name nginx-proxy-manager \
-p 80:80 \
-p 81:81 \
-p 443:443 \
-v $(pwd)/data:/data \
-v $(pwd)/letsencrypt:/etc/letsencrypt \
--restart unless-stopped \
jc21/nginx-proxy-manager:latest
```
Điều này mở các cổng: - **Cổng 80**: Lưu lượng HTTP - **Cổng 81**: Giao diện quản trị - **Cổng 443**: Lưu lượng HTTPS

### Configure Proxy Manager

1. Truy cập giao diện quản trị tại `http://your-server-ip:81`

2. Đăng nhập với thông tin xác thực mặc định:
   - **Email**: admin@example.com
   - **Mật khẩu**: changeme

**Quan trọng**: Thay đổi thông tin đăng nhập này ngay sau lần đăng nhập đầu tiên!

![Đăng nhập Nginx Proxy Manager](/images/guides/reseed/reseed_05.png)

3. Điều hướng đến **Proxy Hosts** và nhấp vào **Add Proxy Host**

![Thêm một proxy host](/images/guides/reseed/reseed_06.png)

4. Cấu hình proxy host:
   - **Domain Name**: Tên miền reseed của bạn (ví dụ: `reseed.example.com`)
   - **Scheme**: `https`
   - **Forward Hostname / IP**: `127.0.0.1`
   - **Forward Port**: `8443`
   - Bật **Cache Assets**
   - Bật **Block Common Exploits**
   - Bật **Websockets Support**

![Cấu hình chi tiết máy chủ proxy](/images/guides/reseed/reseed_07.png)

5. Trong tab **SSL**:
   - Chọn **Request a new SSL Certificate** (Let's Encrypt)
   - Bật **Force SSL**
   - Bật **HTTP/2 Support**
   - Đồng ý với Điều khoản Dịch vụ của Let's Encrypt

![Cấu hình chứng chỉ SSL](/images/guides/reseed/reseed_08.png)

6. Nhấp **Save**

Server reseed của bạn bây giờ sẽ có thể truy cập được tại `https://reseed.example.com`

![Cấu hình máy chủ reseed thành công](/images/guides/reseed/reseed_09.png)

## Registering Your Reseed Server

Khi máy chủ reseed của bạn đã hoạt động, hãy liên hệ với các nhà phát triển I2P để được thêm vào danh sách máy chủ reseed chính thức.

### Bước 5: Tạo Systemd Service

Gửi email cho **zzz** (trưởng nhóm phát triển I2P) với các thông tin sau:

- **Email I2P**: zzz@mail.i2p
- **Email Clearnet**: zzz@i2pmail.org

### Bước 6: Tùy chọn - Cấu hình Khởi động lại Định kỳ

Bao gồm trong email của bạn:

1. **URL máy chủ reseed**: URL HTTPS đầy đủ (ví dụ: `https://reseed.example.com`)
2. **Chứng chỉ reseed công khai**: Nằm tại `/home/i2p/.reseed/` (đính kèm tệp `.crt`)
3. **Email liên hệ**: Phương thức liên hệ ưu tiên của bạn để nhận thông báo bảo trì máy chủ
4. **Vị trí máy chủ**: Tùy chọn nhưng hữu ích (quốc gia/khu vực)
5. **Thời gian hoạt động dự kiến**: Cam kết của bạn trong việc duy trì máy chủ

### Verification

Các nhà phát triển I2P sẽ xác minh rằng reseed server của bạn: - Được cấu hình đúng và đang phục vụ thông tin router - Sử dụng chứng chỉ SSL hợp lệ - Cung cấp các tệp SU3 được ký đúng cách - Có thể truy cập và phản hồi tốt

Sau khi được phê duyệt, reseed server của bạn sẽ được thêm vào danh sách phân phối cùng với các I2P router, giúp người dùng mới tham gia vào mạng lưới!

## Monitoring and Maintenance

### Cài đặt Nginx Proxy Manager

Giám sát dịch vụ reseed của bạn:

```bash
sudo systemctl status reseed
sudo journalctl -u reseed -f
```
### Cấu hình Proxy Manager

Theo dõi tài nguyên hệ thống:

```bash
htop
df -h
```
### Update Reseed Tools

Định kỳ cập nhật reseed-tools để có được các cải tiến mới nhất:

```bash
cd /home/i2p/reseed-tools
git pull
make build
sudo make install
sudo systemctl restart reseed
```
### Thông Tin Liên Hệ

Nếu sử dụng Let's Encrypt thông qua Nginx Proxy Manager, chứng chỉ sẽ tự động gia hạn. Xác minh quá trình gia hạn đang hoạt động:

```bash
docker logs nginx-proxy-manager | grep -i certificate
```
## Cấu hình Dịch vụ

### Thông tin Bắt buộc

Kiểm tra logs để tìm lỗi:

```bash
sudo journalctl -u reseed -n 50
```
Các vấn đề thường gặp: - I2P router chưa chạy hoặc netDb trống - Cổng 8443 đã được sử dụng - Vấn đề về quyền truy cập với thư mục `/home/i2p/.reseed/`

### Xác minh

Đảm bảo router I2P của bạn đang chạy và đã điền dữ liệu vào network database:

```bash
ls -lh /home/i2p/.i2p/netDb/
```
Bạn sẽ thấy nhiều tệp `.dat`. Nếu trống, hãy đợi router I2P của bạn khám phá các peer.

### SSL Certificate Errors

Xác minh chứng chỉ của bạn hợp lệ:

```bash
openssl s_client -connect reseed.example.com:443 -servername reseed.example.com
```
### Kiểm tra Trạng thái Dịch vụ

Kiểm tra: - Bản ghi DNS đang trỏ đúng đến máy chủ của bạn - Tường lửa cho phép cổng 80 và 443 - Nginx Proxy Manager đang chạy: `docker ps`

## Security Considerations

- **Bảo mật khóa riêng tư**: Không bao giờ chia sẻ hoặc để lộ nội dung trong `/home/i2p/.reseed/`
- **Cập nhật thường xuyên**: Giữ các gói hệ thống, Docker và reseed-tools ở phiên bản mới nhất
- **Giám sát logs**: Theo dõi các mẫu truy cập đáng ngờ
- **Giới hạn tốc độ**: Cân nhắc triển khai giới hạn tốc độ để ngăn chặn lạm dụng
- **Quy tắc tường lửa**: Chỉ mở các cổng cần thiết (80, 443, 81 cho admin)
- **Giao diện quản trị**: Hạn chế giao diện quản trị Nginx Proxy Manager (cổng 81) chỉ cho các IP đáng tin cậy

## Contributing to the Network

Bằng cách vận hành một reseed server, bạn đang cung cấp cơ sở hạ tầng quan trọng cho mạng lưới I2P. Cảm ơn bạn đã đóng góp cho một internet riêng tư và phi tập trung hơn!

Nếu có thắc mắc hoặc cần hỗ trợ, hãy liên hệ với cộng đồng I2P: - **Diễn đàn**: [i2pforum.net](https://i2pforum.net) - **IRC/Reddit**: #i2p trên nhiều mạng khác nhau - **Phát triển**: [i2pgit.org](https://i2pgit.org)

---

---

*Hướng dẫn ban đầu được tạo bởi [Stormy Cloud](https://www.stormycloud.org), chuyển thể cho tài liệu I2P.*
