---
title: "Máy chủ Reseed (máy chủ cung cấp dữ liệu khởi động ban đầu cho netDb)"
description: "Vận hành các dịch vụ reseed (cấp dữ liệu khởi tạo mạng) và các phương thức bootstrap (khởi động ban đầu) thay thế"
slug: "reseed"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## Giới thiệu về các máy chủ reseed (máy chủ cung cấp dữ liệu khởi tạo netDb)

Các routers mới cần một số ít nút ngang hàng để tham gia mạng I2P. Các máy chủ reseed (máy chủ cấp dữ liệu khởi tạo) cung cấp tập khởi tạo ban đầu đó thông qua các lần tải xuống HTTPS được mã hóa. Mỗi gói reseed được máy chủ ký, ngăn chặn việc can thiệp bởi các bên không được xác thực. Các routers đã hoạt động ổn định đôi khi có thể reseed nếu tập nút ngang hàng của chúng trở nên lỗi thời.

### Quy trình khởi tạo mạng

Khi một I2P router mới khởi động hoặc đã ngoại tuyến trong một khoảng thời gian dài, nó cần dữ liệu RouterInfo (thông tin định danh của router) để kết nối vào mạng. Vì router không có sẵn các nút ngang hàng, nó không thể lấy thông tin này từ ngay bên trong mạng I2P. Cơ chế reseed (khởi tạo kết nối ban đầu) giải quyết vấn đề bootstrap (khởi động ban đầu) này bằng cách cung cấp các tệp RouterInfo từ các máy chủ HTTPS bên ngoài đáng tin cậy.

Quy trình reseed (giai đoạn khởi tạo netDb ban đầu) phân phối 75–100 tệp RouterInfo (bản mô tả router) trong một gói duy nhất có chữ ký mật mã. Điều này bảo đảm các router mới có thể nhanh chóng thiết lập kết nối mà không bị phơi bày trước các cuộc tấn công người trung gian (man-in-the-middle) có thể cô lập chúng thành các phân vùng mạng riêng rẽ, không đáng tin cậy.

### Trạng thái mạng hiện tại

Tính đến tháng 10 năm 2025, mạng I2P vận hành với phiên bản router 2.10.0 (phiên bản API 0.9.67). Giao thức reseed (quy trình khởi tạo ban đầu bằng cách tải netDb) được giới thiệu từ phiên bản 0.9.14 vẫn ổn định và không thay đổi về chức năng cốt lõi. Mạng duy trì nhiều máy chủ reseed độc lập được phân bố trên toàn cầu nhằm bảo đảm tính sẵn sàng và khả năng chống kiểm duyệt.

Dịch vụ [checki2p](https://checki2p.com/reseed) giám sát tất cả các máy chủ reseed (máy chủ cung cấp dữ liệu khởi tạo ban đầu cho mạng I2P) cứ mỗi 4 giờ, cung cấp các kiểm tra trạng thái theo thời gian thực và các chỉ số về tính sẵn sàng cho hạ tầng reseed.

## Đặc tả định dạng tệp SU3

Định dạng tệp SU3 là nền tảng của giao thức reseed (quá trình khởi động ban đầu bằng cách tải dữ liệu seed của netDb) của I2P, cung cấp khả năng phân phối nội dung được ký bằng mật mã. Việc nắm vững định dạng này là điều thiết yếu để triển khai máy chủ và máy khách reseed.

### Cấu trúc tệp

Định dạng SU3 gồm ba thành phần chính: phần đầu (40+ byte), nội dung (độ dài biến đổi), và chữ ký (độ dài được chỉ định trong phần đầu).

#### Định dạng phần đầu (tối thiểu byte 0-39)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Byte Range</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0-5</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Magic Number</td><td style="border:1px solid var(--color-border); padding:0.5rem;">ASCII string "I2Psu3" (0x493250737533)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">6</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused, must be 0x00</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">7</td><td style="border:1px solid var(--color-border); padding:0.5rem;">File Format Version</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current version: 0x00</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">8-9</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Signature Type</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big-endian 16-bit integer. Type 6 = RSA-4096-SHA512 (reseed standard)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">10-11</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Signature Length</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big-endian 16-bit integer. 512 bytes (0x0200) for RSA-4096</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused, must be 0x00</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">13</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Version Length</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Minimum 16 bytes (0x10) for compatibility</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">14</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused, must be 0x00</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">15</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Signer ID Length</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Length of UTF-8 signer identifier string</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">16-23</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Content Length</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big-endian 64-bit integer, length of content in bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">24</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused, must be 0x00</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">25</td><td style="border:1px solid var(--color-border); padding:0.5rem;">File Type</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0x00 = ZIP, 0x01 = XML, 0x02 = HTML, 0x03 = XML.GZ, 0x04 = TXT.GZ, 0x05 = DMG, 0x06 = EXE</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">26</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused, must be 0x00</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">27</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Content Type</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0x00 = unknown, 0x01 = router update, 0x02 = plugin, 0x03 = reseed, 0x04 = news, 0x05 = blocklist</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">28-39</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Padding</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused, must be all zeros</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">40-55</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Version String</td><td style="border:1px solid var(--color-border); padding:0.5rem;">ASCII version string, padded with zeros (minimum 16 bytes)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">56-...</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Signer ID</td><td style="border:1px solid var(--color-border); padding:0.5rem;">UTF-8 encoded signer identifier (e.g., "user@mail.i2p")</td></tr>
  </tbody>
</table>
### Các tham số SU3 (định dạng gói ký trong I2P) dành riêng cho Reseed (quá trình khởi tạo mạng I2P)

Đối với gói reseed (gói dữ liệu khởi tạo mạng I2P), tệp SU3 phải có các đặc điểm sau:

- **Tên tệp**: Phải chính xác là `i2pseeds.su3`
- **Loại nội dung** (byte 27): 0x03 (RESEED)
- **Loại tệp** (byte 25): 0x00 (ZIP)
- **Loại chữ ký** (byte 8-9): 0x0006 (RSA-4096-SHA512)
- **Chuỗi phiên bản**: dấu thời gian Unix bằng ASCII (giây kể từ mốc epoch, định dạng date +%s)
- **ID người ký**: Định danh dạng email khớp với CN của chứng chỉ X.509

#### Tham số truy vấn ID mạng

Từ phiên bản 0.9.42, các router thêm `?netid=2` vào các yêu cầu reseed (khởi tạo ban đầu). Điều này ngăn chặn các kết nối chéo giữa các mạng, vì các mạng thử nghiệm sử dụng các ID mạng khác nhau. Mạng I2P chính thức hiện tại sử dụng ID mạng 2.

Ví dụ yêu cầu: `https://reseed.example.com/i2pseeds.su3?netid=2`

### Cấu trúc nội dung tệp ZIP

Phần nội dung (sau phần tiêu đề, trước phần chữ ký) chứa một tệp ZIP tiêu chuẩn với các yêu cầu sau:

- **Nén**: Nén ZIP tiêu chuẩn (DEFLATE)
- **Số lượng tệp**: Thường là 75-100 tệp RouterInfo (tệp thông tin router)
- **Cấu trúc thư mục**: Tất cả các tệp phải ở mức trên cùng (không có thư mục con)
- **Quy tắc đặt tên tệp**: `routerInfo-{44-character-base64-hash}.dat`
- **Bảng chữ cái Base64**: Phải dùng bảng chữ cái base64 đã được I2P sửa đổi

Bảng chữ cái base64 của I2P khác với base64 chuẩn bằng cách dùng `-` và `~` thay cho `+` và `/` để đảm bảo khả năng tương thích với hệ thống tệp và URL.

### Chữ ký mật mã

Chữ ký bao phủ toàn bộ tệp từ byte 0 đến hết phần nội dung. Bản thân chữ ký được thêm vào sau phần nội dung.

#### Thuật toán chữ ký số (RSA-4096-SHA512)

1. Tính hàm băm SHA-512 của dữ liệu từ byte 0 đến hết nội dung
2. Ký hàm băm bằng RSA "raw" (NONEwithRSA theo thuật ngữ của Java)
3. Đệm chữ ký bằng các số 0 ở đầu nếu cần để đạt 512 byte
4. Nối thêm chữ ký 512 byte vào cuối tệp

#### Quy trình xác minh chữ ký

Các ứng dụng khách phải:

1. Đọc các byte 0-11 để xác định loại và độ dài chữ ký
2. Đọc toàn bộ tiêu đề để xác định ranh giới nội dung
3. Đọc nội dung theo luồng trong khi tính hàm băm SHA-512
4. Trích xuất chữ ký từ cuối tệp
5. Xác minh chữ ký bằng khóa công khai RSA-4096 của người ký
6. Từ chối tệp nếu xác minh chữ ký thất bại

### Mô hình tin cậy chứng chỉ

Các khóa ký reseed được phân phối dưới dạng chứng chỉ X.509 tự ký sử dụng khóa RSA-4096. Các chứng chỉ này được bao gồm trong các gói router I2P trong thư mục `certificates/reseed/`.

Định dạng chứng chỉ: - **Loại khóa**: RSA-4096 - **Chữ ký**: Tự ký - **Subject CN**: Phải khớp với Signer ID trong SU3 header - **Ngày hiệu lực**: Các máy khách nên thực thi thời hạn hiệu lực của chứng chỉ

## Vận hành một Reseed Host (máy chủ cung cấp dữ liệu khởi tạo cho mạng I2P)

Vận hành một dịch vụ reseed (dịch vụ cấp dữ liệu khởi động mạng) đòi hỏi chú ý cẩn trọng đến các yêu cầu về bảo mật, độ tin cậy và đa dạng mạng. Có nhiều máy chủ reseed độc lập hơn sẽ tăng khả năng chống chịu và khiến kẻ tấn công hoặc cơ quan kiểm duyệt khó chặn các routers mới tham gia hơn.

### Yêu cầu kỹ thuật

#### Thông số kỹ thuật máy chủ

- **Hệ điều hành**: Unix/Linux (Ubuntu, Debian, FreeBSD đã được kiểm thử và khuyến nghị)
- **Kết nối**: Địa chỉ IPv4 tĩnh là bắt buộc, IPv6 được khuyến nghị nhưng không bắt buộc
- **CPU**: Tối thiểu 2 lõi
- **RAM**: Tối thiểu 2 GB
- **Băng thông**: Khoảng 15 GB mỗi tháng
- **Thời gian hoạt động**: Yêu cầu hoạt động 24/7
- **I2P Router**: I2P router được tích hợp tốt, chạy liên tục

#### Yêu cầu phần mềm

- **Java**: JDK 8 trở lên (sẽ yêu cầu Java 17+ kể từ I2P 2.11.0)
- **Máy chủ web**: nginx hoặc Apache với hỗ trợ reverse proxy (proxy ngược) (Lighttpd không còn được hỗ trợ do hạn chế của header X-Forwarded-For)
- **TLS/SSL**: Chứng chỉ TLS hợp lệ (Let's Encrypt, tự ký, hoặc CA thương mại (tổ chức cấp chứng chỉ))
- **Bảo vệ DDoS**: fail2ban hoặc tương đương (bắt buộc, không tùy chọn)
- **Công cụ Reseed**: reseed-tools chính thức từ https://i2pgit.org/idk/reseed-tools

### Yêu cầu bảo mật

#### Cấu hình HTTPS/TLS

- **Giao thức**: Chỉ HTTPS, không cho phép chuyển về HTTP
- **Phiên bản TLS**: Tối thiểu TLS 1.2
- **Bộ mã mật mã (cipher suites)**: Phải hỗ trợ các bộ mã mạnh tương thích với Java 8+
- **CN/SAN của chứng chỉ**: Phải khớp với tên máy chủ của URL được phục vụ
- **Loại chứng chỉ**: Có thể tự ký nếu đã thông báo trước cho nhóm phát triển, hoặc do CA (tổ chức chứng thực) được công nhận cấp

#### Quản lý chứng chỉ

Chứng chỉ ký SU3 và chứng chỉ TLS phục vụ những mục đích khác nhau:

- **Chứng chỉ TLS** (`certificates/ssl/`): Bảo mật truyền tải HTTPS
- **Chứng chỉ ký SU3** (`certificates/reseed/`): Ký các gói reseed

Cả hai chứng chỉ phải được cung cấp cho reseed coordinator (điều phối viên khởi tạo mạng ban đầu) (zzz@mail.i2p) để được đưa vào các gói router.

#### Bảo vệ chống DDoS và Scraping (thu thập dữ liệu tự động)

Máy chủ Reseed (máy chủ cung cấp dữ liệu netDb ban đầu cho router mới gia nhập mạng) phải đối mặt định kỳ với các cuộc tấn công từ các triển khai lỗi, botnet và các tác nhân độc hại tìm cách thu thập ồ ạt cơ sở dữ liệu mạng. Các biện pháp bảo vệ bao gồm:

- **fail2ban**: Bắt buộc để giới hạn tần suất và giảm thiểu tấn công
- **Đa dạng gói**: Cung cấp các tập RouterInfo (thông tin về router trong I2P) khác nhau cho các bên yêu cầu khác nhau
- **Nhất quán gói**: Cung cấp cùng một gói cho các yêu cầu lặp lại từ cùng một IP trong một khoảng thời gian có thể cấu hình
- **Hạn chế ghi log IP**: Không công khai nhật ký (log) hoặc địa chỉ IP (yêu cầu của chính sách quyền riêng tư)

### Phương pháp triển khai

#### Phương pháp 1: reseed-tools chính thức (Khuyến nghị)

Bản hiện thực chính tắc do dự án I2P bảo trì. Kho lưu trữ: https://i2pgit.org/idk/reseed-tools

**Cài đặt**:

```bash
# Install dependencies
sudo apt-get install golang git

# Clone repository
git clone https://i2pgit.org/idk/reseed-tools.git
cd reseed-tools

# Build
make

# Generate keys and start server (first run)
./reseed-tools reseed \
  --signer=your-email@mail.i2p \
  --netdb=/path/to/i2p/netDb \
  --tlsHost=your-domain.tld \
  --port=8443
```
Trong lần chạy đầu tiên, công cụ sẽ tạo: - `your-email@mail.i2p.crt` (chứng chỉ ký SU3) - `your-email@mail.i2p.pem` (khóa riêng ký SU3) - `your-email@mail.i2p.crl` (danh sách thu hồi chứng chỉ) - các tệp chứng chỉ và khóa TLS

**Tính năng**: - Tự động tạo gói SU3 (350 biến thể, mỗi biến thể có 77 RouterInfos) - Máy chủ HTTPS tích hợp sẵn - Tái tạo bộ nhớ đệm cứ mỗi 9 giờ thông qua cron - Hỗ trợ header X-Forwarded-For với cờ `--trustProxy` - Tương thích với các cấu hình reverse proxy (proxy ngược)

**Triển khai sản xuất**:

```bash
# Create systemd service
cat > /etc/systemd/system/i2p-reseed.service << EOF
[Unit]
Description=I2P Reseed Server
After=network.target

[Service]
Type=simple
User=i2p-reseed
WorkingDirectory=/opt/i2p-reseed
ExecStart=/opt/i2p-reseed/reseed-tools reseed \
  --signer=your-email@mail.i2p \
  --netdb=/var/lib/i2p/netDb \
  --port=8443 \
  --ip=127.0.0.1 \
  --trustProxy
Restart=always

[Install]
WantedBy=multi-user.target
EOF

systemctl enable i2p-reseed
systemctl start i2p-reseed
```
#### Phương pháp 2: Hiện thực bằng Python (pyseeder)

Một triển khai thay thế do dự án PurpleI2P thực hiện: https://github.com/PurpleI2P/pyseeder

```bash
pip install pyseeder

# Generate SU3 file
echo "your_password" | pyseeder reseed \
  --netdb /path/to/netDb \
  --private-key priv_key.pem \
  --outfile i2pseeds.su3 \
  --signer-id user@mail.i2p

# Serve via built-in server
pyseeder serve \
  --port 8443 \
  --host 0.0.0.0 \
  --private-key priv_key.pem \
  --cert user_at_mail.i2p.crt \
  --file i2pseeds.su3
```
#### Phương pháp 3: Triển khai bằng Docker (nền tảng container)

Đối với các môi trường được container hóa, có một số triển khai sẵn sàng cho Docker:

- **DivaExchange i2p-reseed**: https://github.com/diva-exchange/i2p-reseed
- **RTradeLtd/i2p-tools-1**: Thêm dịch vụ onion của Tor và hỗ trợ IPFS

### Cấu hình proxy ngược

#### Cấu hình nginx

```nginx
upstream i2p_reseed {
    server 127.0.0.1:8443;
}

server {
    listen 443 ssl http2;
    server_name reseed.example.com;

    ssl_certificate /path/to/tls-cert.crt;
    ssl_certificate_key /path/to/tls-key.key;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    location / {
        proxy_pass http://i2p_reseed;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $remote_addr;
        proxy_set_header Host $host;
    }
}
```
#### Cấu hình Apache

```apache
<VirtualHost *:443>
    ServerName reseed.example.com
    
    SSLEngine on
    SSLCertificateFile /path/to/tls-cert.crt
    SSLCertificateKeyFile /path/to/tls-key.key
    SSLProtocol all -SSLv2 -SSLv3 -TLSv1 -TLSv1.1
    
    ProxyRequests Off
    <Proxy *>
        Order deny,allow
        Allow from all
    </Proxy>
    
    ProxyPass / http://127.0.0.1:8443/
    ProxyPassReverse / http://127.0.0.1:8443/
</VirtualHost>
```
### Đăng ký và Điều phối

Để đưa máy chủ reseed (máy chủ cung cấp dữ liệu khởi tạo để người dùng mới tham gia mạng) của bạn vào gói I2P chính thức:

1. Hoàn tất thiết lập và kiểm thử
2. Gửi cả hai chứng chỉ (SU3 signing và TLS) cho reseed coordinator (điều phối viên khởi tạo nút mạng I2P ban đầu)
3. Liên hệ: zzz@mail.i2p hoặc zzz@i2pmail.org
4. Tham gia #i2p-dev trên IRC2P để phối hợp với các vận hành viên khác

### Thực tiễn vận hành tốt nhất

#### Giám sát và ghi nhật ký

- Kích hoạt định dạng log Combined (tổng hợp) của Apache/nginx để phục vụ thống kê
- Thiết lập log rotation (luân phiên nhật ký) (nhật ký tăng dung lượng rất nhanh)
- Giám sát mức độ thành công khi tạo bundle (gói) và thời gian dựng lại
- Theo dõi mức sử dụng băng thông và các mẫu yêu cầu
- Không bao giờ công khai địa chỉ IP hoặc nhật ký truy cập chi tiết

#### Lịch bảo trì

- **Cứ mỗi 9 giờ**: Xây dựng lại bộ đệm gói SU3 (tự động qua cron)
- **Hàng tuần**: Rà soát nhật ký để phát hiện các mẫu tấn công
- **Hàng tháng**: Cập nhật I2P router và reseed-tools
- **Khi cần**: Gia hạn chứng chỉ TLS (tự động hóa bằng Let's Encrypt)

#### Lựa chọn cổng

- Mặc định: 8443 (được khuyến nghị)
- Tùy chọn khác: Bất kỳ cổng nào trong khoảng 1024-49151
- Cổng 443: Cần quyền root hoặc chuyển tiếp cổng (khuyến nghị chuyển hướng iptables)

Ví dụ về chuyển tiếp cổng:

```bash
iptables -A PREROUTING -t nat -p tcp --dport 443 -j REDIRECT --to-port 8443
```
## Các phương thức Reseed (tải dữ liệu khởi tạo mạng) thay thế

Các tùy chọn bootstrap khác giúp người dùng trong các mạng bị hạn chế:

### Reseed (quá trình tải dữ liệu khởi tạo mạng) dựa trên tệp

Được giới thiệu trong phiên bản 0.9.16, reseeding dựa trên tệp (tái gieo dựa trên tệp) cho phép người dùng tải thủ công các gói RouterInfo. Phương pháp này đặc biệt hữu ích cho người dùng ở các khu vực bị kiểm duyệt, nơi các máy chủ reseed qua HTTPS bị chặn.

**Quy trình**: 1. Một người liên hệ đáng tin cậy tạo một gói SU3 sử dụng router của họ 2. Gói được chuyển qua email, ổ USB, hoặc kênh out-of-band (ngoài băng) khác 3. Người dùng đặt `i2pseeds.su3` trong thư mục cấu hình I2P 4. Router tự động phát hiện và xử lý gói khi khởi động lại

**Tài liệu**: /blog/2020/06/07/help-your-friends-join-i2p-by-sharing-reseed-bundles/

**Trường hợp sử dụng**: - Người dùng ở sau các tường lửa cấp quốc gia chặn các máy chủ reseed - Mạng biệt lập yêu cầu khởi tạo ban đầu thủ công - Môi trường thử nghiệm và phát triển

### Reseeding (khởi tạo netDb ban đầu) qua proxy của Cloudflare

Việc định tuyến lưu lượng reseed (lưu lượng khởi tạo mạng I2P) qua CDN của Cloudflare mang lại một số lợi ích cho người vận hành ở các khu vực có mức độ kiểm duyệt cao.

**Lợi ích**: - Địa chỉ IP của máy chủ gốc được ẩn khỏi máy khách - Bảo vệ DDoS thông qua hạ tầng của Cloudflare - Phân phối tải theo khu vực địa lý thông qua bộ nhớ đệm biên - Cải thiện hiệu năng cho các máy khách trên toàn cầu

**Yêu cầu triển khai**: - Cờ `--trustProxy` được bật trong reseed-tools - Proxy Cloudflare được bật cho bản ghi DNS - Xử lý header X-Forwarded-For đúng cách

**Các lưu ý quan trọng**: - Các hạn chế cổng của Cloudflare được áp dụng (phải sử dụng các cổng được hỗ trợ) - Để đảm bảo tính nhất quán bundle (gói) theo từng máy khách, cần hỗ trợ X-Forwarded-For - Cấu hình SSL/TLS do Cloudflare quản lý

**Tài liệu**: https://homepage.np-tokumei.net/post/notes-i2p-reseed-over-cloudflare/

### Các chiến lược kháng kiểm duyệt

Nghiên cứu của Nguyen Phong Hoang (USENIX FOCI 2019) xác định các phương thức bootstrap (khởi tạo ban đầu) bổ sung cho các mạng bị kiểm duyệt:

#### Các nhà cung cấp lưu trữ đám mây

- **Box, Dropbox, Google Drive, OneDrive**: Lưu trữ tệp SU3 trên các liên kết công khai
- **Ưu điểm**: Khó bị chặn mà không làm gián đoạn các dịch vụ hợp pháp
- **Hạn chế**: Cần phân phối URL thủ công cho người dùng

#### Phân phối IPFS

- Lưu trữ các gói reseed (khởi tạo kết nối ban đầu tới mạng I2P) trên InterPlanetary File System
- Lưu trữ định địa chỉ theo nội dung giúp ngăn chặn giả mạo
- Kháng chịu trước các nỗ lực gỡ bỏ

#### Các dịch vụ Onion của Tor

- Reseed servers (máy chủ reseed: máy chủ cung cấp dữ liệu khởi tạo để tham gia mạng I2P) có thể truy cập qua các địa chỉ .onion
- Khó bị chặn dựa trên IP
- Yêu cầu trình khách Tor trên hệ thống của người dùng

**Tài liệu nghiên cứu**: https://homepage.np-tokumei.net/post/notes-censorship-resistant-i2p-reseeding/

#### Các quốc gia được biết là chặn I2P

Tính đến năm 2025, các quốc gia sau được xác nhận là chặn máy chủ reseed của I2P (máy chủ cấp dữ liệu khởi đầu): - Trung Quốc - Iran - Oman - Qatar - Kuwait

Người dùng ở các khu vực này nên sử dụng các phương thức khởi tạo ban đầu thay thế hoặc các chiến lược reseeding (quy trình nạp danh sách nút ban đầu) chống kiểm duyệt.

## Chi tiết giao thức dành cho người hiện thực

### Đặc tả Yêu cầu Reseed (khởi tạo dữ liệu mạng ban đầu)

#### Hành vi của ứng dụng khách

1. **Lựa chọn máy chủ**: Router duy trì danh sách URL reseed (máy chủ khởi tạo mạng I2P) cố định trong mã
2. **Chọn ngẫu nhiên**: Máy khách chọn ngẫu nhiên máy chủ từ danh sách hiện có
3. **Định dạng yêu cầu**: `GET /i2pseeds.su3?netid=2 HTTP/1.1`
4. **User-Agent**: Nên mô phỏng các trình duyệt phổ biến (ví dụ, "Wget/1.11.4")
5. **Logic thử lại**: Nếu yêu cầu SU3 thất bại, chuyển sang phân tích cú pháp trang chỉ mục
6. **Xác thực chứng chỉ**: Xác minh chứng chỉ TLS đối chiếu với kho tin cậy của hệ thống
7. **Xác thực chữ ký SU3**: Xác minh chữ ký đối chiếu với các chứng chỉ reseed đã biết

#### Hành vi của máy chủ

1. **Chọn gói**: Chọn một tập con giả ngẫu nhiên của RouterInfos (thông tin router) từ netDb
2. **Theo dõi máy khách**: Xác định yêu cầu theo IP nguồn (tôn trọng X-Forwarded-For)
3. **Tính nhất quán của gói**: Trả về cùng một gói cho các yêu cầu lặp lại trong cửa sổ thời gian (thường 8–12 giờ)
4. **Tính đa dạng của gói**: Trả về các gói khác nhau cho các máy khách khác nhau để tăng đa dạng mạng
5. **Content-Type**: `application/octet-stream` hoặc `application/x-i2p-reseed`

### Định dạng tệp RouterInfo

Mỗi tệp `.dat` trong gói reseed chứa một cấu trúc RouterInfo:

**Quy ước đặt tên tệp**: `routerInfo-{base64-hash}.dat` - Hash (mã băm) dài 44 ký tự, dùng bảng ký tự base64 của I2P - Ví dụ: `routerInfo-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmn.dat`

**Nội dung tệp**: - RouterIdentity (định danh router) (băm router, khóa mã hóa, khóa ký) - Dấu thời gian công bố - Địa chỉ Router (IP, cổng, loại truyền tải) - Khả năng và tùy chọn của Router - Chữ ký bao trùm toàn bộ dữ liệu ở trên

### Các yêu cầu về đa dạng mạng

Để ngăn chặn tập trung hóa mạng và cho phép phát hiện tấn công Sybil:

- **Không dump NetDb đầy đủ**: Không bao giờ cung cấp toàn bộ RouterInfos (thông tin router) cho một máy khách duy nhất
- **Lấy mẫu ngẫu nhiên**: Mỗi gói chứa một tập con khác nhau của các peers (nút ngang hàng) khả dụng
- **Kích thước gói tối thiểu**: 75 RouterInfos (tăng so với giá trị ban đầu là 50)
- **Kích thước gói tối đa**: 100 RouterInfos
- **Độ mới**: RouterInfos nên còn mới (trong vòng 24 giờ kể từ khi được tạo)

### Các lưu ý về IPv6

**Tình trạng hiện tại** (2025): - Một số máy chủ reseed (máy chủ cung cấp dữ liệu khởi tạo cho I2P) cho thấy tình trạng không phản hồi qua IPv6 - Các máy khách nên ưu tiên hoặc buộc dùng IPv4 để đảm bảo độ tin cậy - Hỗ trợ IPv6 được khuyến nghị cho các triển khai mới nhưng không mang tính thiết yếu

**Lưu ý triển khai**: Khi cấu hình máy chủ dual-stack (hỗ trợ cả IPv4 và IPv6), hãy đảm bảo các địa chỉ lắng nghe của cả IPv4 và IPv6 hoạt động đúng, hoặc vô hiệu hóa IPv6 nếu không thể hỗ trợ đúng cách.

## Các cân nhắc bảo mật

### Mô hình mối đe dọa

reseed protocol (giao thức reseed) bảo vệ chống lại:

1. **Tấn công kẻ đứng giữa (MITM)**: Chữ ký RSA-4096 ngăn việc giả mạo gói
2. **Chia cắt mạng**: Nhiều reseed servers (máy chủ cấp dữ liệu ban đầu cho người dùng tham gia mạng) độc lập ngăn việc tồn tại một điểm kiểm soát duy nhất
3. **Tấn công Sybil**: Sự đa dạng của các gói hạn chế khả năng của kẻ tấn công trong việc cô lập người dùng
4. **Kiểm duyệt**: Nhiều máy chủ và các phương thức thay thế cung cấp tính dự phòng

Giao thức reseed (quy trình khởi tạo netDb ban đầu) KHÔNG bảo vệ chống lại:

1. **Máy chủ reseed (máy chủ cung cấp dữ liệu khởi tạo để tham gia I2P) bị xâm phạm**: Nếu kẻ tấn công kiểm soát khóa riêng của chứng chỉ reseed
2. **Chặn mạng hoàn toàn**: Nếu tất cả các phương thức reseed bị chặn trong một khu vực
3. **Giám sát dài hạn**: Các yêu cầu reseed tiết lộ địa chỉ IP đang cố gắng tham gia I2P

### Quản lý chứng chỉ

**Bảo mật khóa riêng**: - Lưu trữ khóa ký SU3 ngoại tuyến khi không sử dụng - Sử dụng mật khẩu mạnh để mã hóa khóa - Duy trì các bản sao lưu an toàn của khóa và chứng chỉ - Cân nhắc sử dụng mô-đun bảo mật phần cứng (HSMs) cho các triển khai có giá trị cao

**Thu hồi chứng chỉ**: - Danh sách thu hồi chứng chỉ (CRLs) được phân phối qua nguồn cấp tin - Chứng chỉ bị xâm phạm có thể được thu hồi bởi điều phối viên - Các router tự động cập nhật CRLs thông qua các bản cập nhật phần mềm

### Giảm thiểu tấn công

**Bảo vệ DDoS**: - quy tắc fail2ban cho số lượng yêu cầu quá mức - Giới hạn tốc độ ở cấp máy chủ web - Giới hạn số kết nối cho mỗi địa chỉ IP - Cloudflare hoặc CDN tương tự để bổ sung một lớp

**Ngăn chặn scraping (thu thập dữ liệu tự động)**: - Các gói khác nhau cho mỗi IP gửi yêu cầu - Lưu đệm gói theo thời gian cho mỗi IP - Ghi nhật ký các mẫu cho thấy dấu hiệu của các nỗ lực scraping - Phối hợp với những người vận hành khác về các cuộc tấn công đã phát hiện

## Kiểm thử và Xác nhận

### Kiểm tra máy chủ reseed (máy chủ cung cấp dữ liệu netDb ban đầu) của bạn

#### Phương pháp 1: Cài đặt Router mới

1. Cài đặt I2P trên hệ thống mới cài đặt
2. Thêm reseed URL (reseed: nguồn khởi tạo danh sách nút ban đầu) của bạn vào cấu hình
3. Gỡ bỏ hoặc vô hiệu hóa các reseed URL khác
4. Khởi động router và theo dõi nhật ký để kiểm tra reseed thành công
5. Xác minh kết nối tới mạng trong vòng 5-10 phút

Đầu ra nhật ký dự kiến:

```
Reseed got 77 router infos from https://your-reseed.example.com/i2pseeds.su3?netid=2 with 0 errors
Reseed complete, 77 received
```
#### Phương pháp 2: Xác minh SU3 thủ công

```bash
# Download bundle
curl -k -A "Wget/1.11.4" https://your-reseed.example.com/i2pseeds.su3 > test.su3

# Verify it's a valid SU3 file
hexdump -C test.su3 | head -n 3
# Should show: 49 32 50 73 75 33 (I2Psu3)

# Extract content (requires su3 tools)
java -cp /path/to/i2p.jar net.i2p.crypto.SU3File verify test.su3 your-cert.crt

# Unzip content
# (Extract content section, skip header+signature, then unzip)
```
#### Phương pháp 3: checki2p Monitoring (dịch vụ giám sát checki2p)

Dịch vụ tại https://checki2p.com/reseed thực hiện các kiểm tra tự động cứ mỗi 4 giờ đối với tất cả các máy chủ reseed (máy chủ khởi tạo ban đầu) I2P đã đăng ký. Điều này cung cấp:

- Giám sát tính sẵn sàng
- Chỉ số thời gian phản hồi
- Xác minh chứng chỉ TLS
- Xác minh chữ ký SU3
- Dữ liệu uptime lịch sử

Khi reseed (máy chủ khởi tạo mạng ban đầu) của bạn được đăng ký với dự án I2P, nó sẽ tự động xuất hiện trên checki2p trong vòng 24 giờ.

### Khắc phục sự cố thường gặp

**Vấn đề**: "Unable to read signing key" khi chạy lần đầu - **Giải pháp**: Điều này là dự kiến. Trả lời 'y' để tạo các khóa mới.

**Vấn đề**: Router không thể xác minh chữ ký - **Nguyên nhân**: Chứng chỉ không có trong kho tin cậy của Router - **Giải pháp**: Đặt chứng chỉ vào thư mục `~/.i2p/certificates/reseed/`

**Vấn đề**: Cùng một gói được gửi đến các máy khách khác nhau - **Nguyên nhân**: Header X-Forwarded-For không được chuyển tiếp đúng cách - **Giải pháp**: Bật `--trustProxy` và cấu hình các header của proxy ngược

**Sự cố**: lỗi "Connection refused" - **Nguyên nhân**: Cổng không thể truy cập từ Internet - **Giải pháp**: Kiểm tra các quy tắc tường lửa, xác minh chuyển tiếp cổng

**Vấn đề**: Mức sử dụng CPU cao trong quá trình tái xây dựng gói - **Nguyên nhân**: Hành vi bình thường khi tạo hơn 350 biến thể SU3 - **Giải pháp**: Đảm bảo có đủ tài nguyên CPU, cân nhắc giảm tần suất tái xây dựng

## Thông tin tham khảo

### Tài liệu chính thức

- **Hướng dẫn cho người đóng góp Reseed (khởi tạo mạng I2P)**: /guides/creating-and-running-an-i2p-reseed-server/
- **Các yêu cầu về chính sách Reseed**: /guides/reseed-policy/
- **Đặc tả SU3**: /docs/specs/updates/
- **Kho công cụ Reseed**: https://i2pgit.org/idk/reseed-tools
- **Tài liệu công cụ Reseed**: https://eyedeekay.github.io/reseed-tools/

### Các triển khai thay thế

- **PurpleI2P pyseeder**: https://github.com/PurpleI2P/pyseeder
- **DivaExchange i2p-reseed**: https://github.com/diva-exchange/i2p-reseed
- **RTradeLtd i2p-tools-1**: https://github.com/RTradeLtd/i2p-tools-1
- **Python WSGI reseeder**: https://github.com/torbjo/i2p-reseeder

### Tài nguyên cộng đồng

- **Diễn đàn I2P**: https://i2pforum.net/
- **Kho lưu trữ Gitea**: https://i2pgit.org/I2P_Developers/i2p.i2p
- **IRC**: #i2p-dev trên IRC2P
- **Giám sát trạng thái**: https://checki2p.com/reseed

### Lịch sử phiên bản

- **0.9.14** (2014): Giới thiệu định dạng reseed (tải danh sách router ban đầu) SU3
- **0.9.16** (2014): Bổ sung reseeding dựa trên tệp
- **0.9.42** (2019): Bắt buộc tham số truy vấn Network ID
- **2.0.0** (2022): Giới thiệu giao thức truyền tải SSU2
- **2.4.0** (2024): Cô lập NetDB và cải tiến bảo mật
- **2.6.0** (2024): Các kết nối I2P-over-Tor bị chặn
- **2.10.0** (2025): Bản phát hành ổn định hiện tại (tính đến tháng 9 năm 2025)

### Tham chiếu loại chữ ký

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Algorithm</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Key Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Signature Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Hash</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DSA-SHA1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">DSA</td><td style="border:1px solid var(--color-border); padding:0.5rem;">1024-bit</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SHA-1</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA-SHA256-P256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA</td><td style="border:1px solid var(--color-border); padding:0.5rem;">P-256</td><td style="border:1px solid var(--color-border); padding:0.5rem;">64 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SHA-256</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA-SHA384-P384</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA</td><td style="border:1px solid var(--color-border); padding:0.5rem;">P-384</td><td style="border:1px solid var(--color-border); padding:0.5rem;">96 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SHA-384</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA-SHA512-P521</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA</td><td style="border:1px solid var(--color-border); padding:0.5rem;">P-521</td><td style="border:1px solid var(--color-border); padding:0.5rem;">132 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SHA-512</td></tr>
    <tr><td style="border:1px solidvar(--color-border); padding:0.5rem;">RSA-SHA256-2048</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA</td><td style="border:1px solid var(--color-border); padding:0.5rem;">2048-bit</td><td style="border:1px solid var(--color-border); padding:0.5rem;">256 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SHA-256</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA-SHA384-3072</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA</td><td style="border:1px solid var(--color-border); padding:0.5rem;">3072-bit</td><td style="border:1px solid var(--color-border); padding:0.5rem;">384 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SHA-384</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA-SHA512-4096</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA</td><td style="border:1px solid var(--color-border); padding:0.5rem;">4096-bit</td><td style="border:1px solid var(--color-border); padding:0.5rem;">512 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SHA-512</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA-SHA512-Ed25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Ed25519</td><td style="border:1px solid var(--color-border); padding:0.5rem;">64 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SHA-512</td></tr>
  </tbody>
</table>
**Tiêu chuẩn Reseed**: Loại 6 (RSA-SHA512-4096) là bắt buộc đối với các gói reseed (khởi tạo lại netDb).

## Tri ân

Xin cảm ơn mọi người vận hành reseed (máy chủ cung cấp danh sách nút khởi đầu) vì đã giữ cho mạng luôn dễ truy cập và bền bỉ. Ghi nhận đặc biệt gửi tới các cộng tác viên và dự án sau:

- **zzz**: Nhà phát triển I2P lâu năm và điều phối viên reseed (khởi tạo ban đầu mạng I2P)
- **idk**: Người bảo trì hiện tại của reseed-tools và quản lý phát hành
- **Nguyen Phong Hoang**: Nghiên cứu về các chiến lược reseed chống kiểm duyệt
- **PurpleI2P Team**: Các triển khai và công cụ I2P thay thế
- **checki2p**: Dịch vụ giám sát tự động cho cơ sở hạ tầng reseed

Hạ tầng reseed (cơ chế khởi tạo ban đầu để lấy danh sách nút) phi tập trung của mạng I2P là kết quả của nỗ lực hợp tác của hàng chục người vận hành trên toàn thế giới, bảo đảm rằng người dùng mới luôn có thể tìm được cách tham gia mạng lưới, bất kể kiểm duyệt tại địa phương hay rào cản kỹ thuật.
