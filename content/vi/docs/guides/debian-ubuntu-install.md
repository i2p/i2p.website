---
title: "Cài đặt I2P trên Debian và Ubuntu"
description: "Hướng dẫn đầy đủ cài đặt I2P trên Debian, Ubuntu và các bản phái sinh sử dụng kho lưu trữ chính thức"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

Dự án I2P duy trì các gói chính thức cho Debian, Ubuntu và các bản phân phối dẫn xuất của chúng. Hướng dẫn này cung cấp các chỉ dẫn toàn diện để cài đặt I2P sử dụng các repository chính thức của chúng tôi.

---

Hãy tập trung vào việc cung cấp DỊCH thuật CHÍNH XÁC và HOÀN CHỈNH mà không cần thêm bất kỳ giải thích hay bình luận nào.

## 🚀 Beta: Cài Đặt Tự Động (Thử Nghiệm)

**Dành cho người dùng nâng cao muốn cài đặt tự động nhanh chóng:**

Lệnh một dòng này sẽ tự động phát hiện bản phân phối của bạn và cài đặt I2P. **Sử dụng thận trọng** - xem xét [script cài đặt](https://i2p.net/installlinux.sh) trước khi chạy.

```bash
curl -fsSL https://i2p.net/installlinux.sh | sudo bash
```
**Chức năng:** - Phát hiện bản phân phối Linux của bạn (Ubuntu/Debian) - Thêm kho lưu trữ I2P phù hợp - Cài đặt khóa GPG và các gói cần thiết - Cài đặt I2P tự động

⚠️ **Đây là tính năng beta.** Nếu bạn muốn cài đặt thủ công hoặc muốn hiểu rõ từng bước, hãy sử dụng các phương pháp cài đặt thủ công bên dưới.

---


## Các Nền Tảng Được Hỗ Trợ

Các gói Debian tương thích với:

- **Ubuntu** 18.04 (Bionic) trở lên
- **Linux Mint** 19 (Tara) trở lên
- **Debian** Buster (10) trở lên
- **Knoppix**
- Các bản phân phối dựa trên Debian khác (LMDE, ParrotOS, Kali Linux, v.v.)

**Kiến trúc được hỗ trợ**: amd64, i386, armhf, arm64, powerpc, ppc64el, s390x

Các gói I2P có thể hoạt động trên các hệ thống dựa trên Debian khác không được liệt kê rõ ràng ở trên. Nếu bạn gặp phải vấn đề, vui lòng [báo cáo chúng trên GitLab của chúng tôi](https://i2pgit.org/I2P_Developers/i2p.i2p/).

## Các Phương Pháp Cài Đặt

Chọn phương pháp cài đặt phù hợp với bản phân phối của bạn:

- **Lựa chọn 1**: [Ubuntu và các bản phái sinh](#ubuntu-installation) (Linux Mint, elementary OS, Pop!_OS, v.v.)
- **Lựa chọn 2**: [Debian và các bản phân phối dựa trên Debian](#debian-installation) (bao gồm LMDE, Kali, ParrotOS)

---

(Lưu ý: Văn bản gốc không chứa nội dung cần dịch - chỉ có dấu phân cách "---")

## Cài đặt trên Ubuntu

Ubuntu và các bản phái sinh chính thức (Linux Mint, elementary OS, Trisquel, v.v.) có thể sử dụng I2P PPA (Personal Package Archive) để cài đặt dễ dàng và tự động cập nhật.

### Method 1: Command Line Installation (Recommended)

Đây là phương pháp nhanh nhất và đáng tin cậy nhất để cài đặt I2P trên các hệ thống dựa trên Ubuntu.

**Bước 1: Thêm I2P PPA**

Mở terminal và chạy:

```bash
sudo apt-add-repository ppa:i2p-maintainers/i2p
```
Lệnh này thêm I2P PPA vào `/etc/apt/sources.list.d/` và tự động import khóa GPG ký repository. Chữ ký GPG đảm bảo các gói không bị thay đổi kể từ khi chúng được build.

**Bước 2: Cập nhật danh sách gói**

Cập nhật cơ sở dữ liệu gói của hệ thống để bao gồm PPA mới:

```bash
sudo apt-get update
```
Lệnh này sẽ truy xuất thông tin gói mới nhất từ tất cả các kho lưu trữ đã kích hoạt, bao gồm cả I2P PPA mà bạn vừa thêm vào.

**Bước 3: Cài đặt I2P**

Bây giờ cài đặt I2P:

```bash
sudo apt-get install i2p
```
Xong rồi! Chuyển đến phần [Cấu Hình Sau Cài Đặt](#post-installation-configuration) để tìm hiểu cách khởi động và cấu hình I2P.

### Method 2: Using the Software Center GUI

Nếu bạn muốn sử dụng giao diện đồ họa, bạn có thể thêm PPA bằng cách sử dụng Trung tâm Phần mềm của Ubuntu.

**Bước 1: Mở Software and Updates**

Khởi chạy "Software and Updates" từ menu ứng dụng của bạn.

![Menu Trung tâm Phần mềm](/images/guides/debian/software-center-menu.png)

**Bước 2: Điều hướng đến Phần mềm khác**

Chọn tab "Other Software" và nhấp vào nút "Add" ở phía dưới để cấu hình PPA mới.

![Tab Phần mềm Khác](/images/guides/debian/software-center-addother.png)

**Bước 3: Thêm I2P PPA**

Trong hộp thoại PPA, nhập:

```
ppa:i2p-maintainers/i2p
```
![Hộp thoại Thêm PPA](/images/guides/debian/software-center-ppatool.png)

**Bước 4: Tải lại thông tin kho lưu trữ**

Nhấp vào nút "Reload" để tải xuống thông tin kho lưu trữ đã cập nhật.

![Nút Tải lại](/images/guides/debian/software-center-reload.png)

**Bước 5: Cài đặt I2P**

Mở ứng dụng "Software" từ menu ứng dụng của bạn, tìm kiếm "i2p", và nhấp vào Cài đặt.

![Ứng dụng Phần mềm](/images/guides/debian/software-center-software.png)

Sau khi cài đặt hoàn tất, tiến hành [Cấu hình Sau Cài đặt](#post-installation-configuration).

---

**QUAN TRỌNG**:  KHÔNG đặt câu hỏi, đưa ra giải thích hoặc thêm bất kỳ bình luận nào. Ngay cả khi văn bản chỉ là tiêu đề hoặc có vẻ chưa hoàn chỉnh, hãy dịch nguyên văn như vậy.

## Debian Installation

Debian và các bản phân phối downstream của nó (LMDE, Kali Linux, ParrotOS, Knoppix, v.v.) nên sử dụng kho lưu trữ Debian chính thức của I2P tại `deb.i2p.net`.

### Important Notice

**Các kho lưu trữ cũ của chúng tôi tại `deb.i2p2.de` và `deb.i2p2.no` đã ngừng hỗ trợ.** Nếu bạn đang sử dụng các kho lưu trữ cũ này, vui lòng làm theo hướng dẫn bên dưới để chuyển sang kho lưu trữ mới tại `deb.i2p.net`.

### Prerequisites

Tất cả các bước dưới đây yêu cầu quyền truy cập root. Hãy chuyển sang người dùng root bằng lệnh `su`, hoặc thêm tiền tố `sudo` vào trước mỗi lệnh.

### Phương pháp 1: Cài đặt qua dòng lệnh (Khuyến nghị)

**Bước 1: Cài đặt các gói cần thiết**

Đảm bảo bạn đã cài đặt các công cụ cần thiết:

```bash
sudo apt-get update
sudo apt-get install apt-transport-https lsb-release curl
```
Các gói này cho phép truy cập kho lưu trữ HTTPS an toàn, phát hiện bản phân phối và tải xuống tập tin.

**Bước 2: Thêm kho lưu trữ I2P**

Lệnh bạn sử dụng phụ thuộc vào phiên bản Debian của bạn. Đầu tiên, xác định phiên bản bạn đang chạy:

```bash
cat /etc/debian_version
```
Tham khảo chéo thông tin này với [thông tin phát hành Debian](https://wiki.debian.org/LTS/) để xác định tên mã phân phối của bạn (ví dụ: Bookworm, Bullseye, Buster).

**Dành cho Debian Bullseye (11) trở lên:**

```bash
echo "deb [signed-by=/usr/share/keyrings/i2p-archive-keyring.gpg] https://deb.i2p.net/ $(lsb_release -sc) main" \
  | sudo tee /etc/apt/sources.list.d/i2p.list
```
**Dành cho các bản phân phối dựa trên Debian (LMDE, Kali, ParrotOS, v.v.) trên phiên bản tương đương Bullseye hoặc mới hơn:**

```bash
echo "deb [signed-by=/usr/share/keyrings/i2p-archive-keyring.gpg] https://deb.i2p.net/ $(dpkg --status tzdata | grep Provides | cut -f2 -d'-') main" \
  | sudo tee /etc/apt/sources.list.d/i2p.list
```
**Dành cho Debian Buster (10) hoặc cũ hơn:**

```bash
echo "deb https://deb.i2p.net/ $(lsb_release -sc) main" \
  | sudo tee /etc/apt/sources.list.d/i2p.list
```
**Đối với các bản phái sinh Debian tương đương Buster hoặc cũ hơn:**

```bash
echo "deb https://deb.i2p.net/ $(dpkg --status tzdata | grep Provides | cut -f2 -d'-') main" \
  | sudo tee /etc/apt/sources.list.d/i2p.list
```
**Bước 3: Tải xuống khóa ký kho lưu trữ**

```bash
curl -o i2p-archive-keyring.gpg https://geti2p.net/_static/i2p-archive-keyring.gpg
```
**Bước 4: Xác minh fingerprint của khóa**

Trước khi tin tưởng khóa, hãy xác minh fingerprint của nó khớp với khóa ký chính thức của I2P:

```bash
gpg --keyid-format long --import --import-options show-only --with-fingerprint i2p-archive-keyring.gpg
```
**Xác minh đầu ra hiển thị fingerprint này:**

```
7840 E761 0F28 B904 7535  49D7 67EC E560 5BCF 1346
```
⚠️ **Không tiếp tục nếu fingerprint không khớp.** Điều này có thể cho thấy file tải về đã bị xâm nhập.

**Bước 5: Cài đặt khóa kho lưu trữ**

Sao chép keyring đã xác minh vào thư mục system keyrings:

```bash
sudo cp i2p-archive-keyring.gpg /usr/share/keyrings
```
**Chỉ dành cho Debian Buster hoặc phiên bản cũ hơn**, bạn cũng cần tạo một symlink:

```bash
sudo ln -sf /usr/share/keyrings/i2p-archive-keyring.gpg /etc/apt/trusted.gpg.d/i2p-archive-keyring.gpg
```
**Bước 6: Cập nhật danh sách gói**

Làm mới cơ sở dữ liệu gói của hệ thống để bao gồm kho lưu trữ I2P:

```bash
sudo apt-get update
```
**Bước 7: Cài đặt I2P**

Cài đặt cả gói I2P router và gói keyring (đảm bảo bạn nhận được các bản cập nhật khóa trong tương lai):

```bash
sudo apt-get install i2p i2p-keyring
```
Tuyệt vời! I2P đã được cài đặt. Tiếp tục đến phần [Cấu hình sau cài đặt](#post-installation-configuration).

---


## Post-Installation Configuration

Sau khi cài đặt I2P, bạn cần khởi động router và thực hiện một số cấu hình ban đầu.

### Phương pháp 2: Sử dụng giao diện đồ họa Software Center

Các gói I2P cung cấp ba cách để chạy I2P router:

#### Option 1: On-Demand (Basic)

Khởi động I2P thủ công khi cần thiết bằng cách sử dụng script `i2prouter`:

```bash
i2prouter start
```
**Quan trọng**: **Không** sử dụng `sudo` hoặc chạy dưới quyền root! I2P nên được chạy với tài khoản người dùng thông thường của bạn.

Để dừng I2P:

```bash
i2prouter stop
```
#### Option 2: On-Demand (Without Java Service Wrapper)

Nếu bạn đang sử dụng hệ thống non-x86 hoặc Java Service Wrapper không hoạt động trên nền tảng của bạn, hãy dùng:

```bash
i2prouter-nowrapper
```
Một lần nữa, **không** sử dụng `sudo` hoặc chạy với quyền root.

#### Option 3: System Service (Recommended)

Để có trải nghiệm tốt nhất, hãy cấu hình I2P tự động khởi động khi hệ thống của bạn khởi động, ngay cả trước khi đăng nhập:

```bash
sudo dpkg-reconfigure i2p
```
Thao tác này sẽ mở hộp thoại cấu hình. Chọn "Yes" để bật I2P dưới dạng dịch vụ hệ thống.

**Đây là phương pháp được khuyến nghị** bởi vì: - I2P khởi động tự động khi máy tính khởi động - Router của bạn duy trì khả năng tích hợp mạng tốt hơn - Bạn đóng góp vào sự ổn định của mạng lưới - I2P sẵn sàng ngay lập tức khi bạn cần

### Initial Router Configuration

Sau khi khởi động I2P lần đầu tiên, router sẽ mất vài phút để tích hợp vào mạng lưới. Trong lúc đó, hãy cấu hình các cài đặt thiết yếu sau:

#### 1. Configure NAT/Firewall

Để đạt hiệu suất tối ưu và tham gia mạng lưới, hãy chuyển tiếp các cổng I2P qua NAT/tường lửa của bạn:

1. Mở [I2P Router Console](http://127.0.0.1:7657/)
2. Điều hướng đến [trang Network Configuration](http://127.0.0.1:7657/confignet)
3. Ghi chú các số cổng được liệt kê (thường là các cổng ngẫu nhiên từ 9000-31000)
4. Chuyển tiếp các cổng UDP và TCP này trong router/firewall của bạn

Nếu bạn cần trợ giúp về chuyển tiếp cổng (port forwarding), [portforward.com](https://portforward.com) cung cấp các hướng dẫn cụ thể cho từng router.

#### 2. Adjust Bandwidth Settings

Các cài đặt băng thông mặc định được thiết lập khá thận trọng. Hãy điều chỉnh chúng dựa trên kết nối internet của bạn:

1. Truy cập [trang Cấu hình](http://127.0.0.1:7657/config.jsp)
2. Tìm phần cài đặt băng thông
3. Giá trị mặc định là tải xuống 96 KB/s / tải lên 40 KB/s
4. Tăng các giá trị này nếu bạn có kết nối internet nhanh hơn (ví dụ: 250 KB/s xuống / 100 KB/s lên cho kết nối băng thông rộng thông thường)

**Lưu ý**: Thiết lập giới hạn cao hơn giúp ích cho mạng lưới và cải thiện hiệu suất của chính bạn.

#### 3. Configure Your Browser

Để truy cập các trang web I2P (eepsite) và dịch vụ, hãy cấu hình trình duyệt của bạn để sử dụng HTTP proxy của I2P:

Xem [Hướng dẫn Cấu hình Trình duyệt](/docs/guides/browser-config) của chúng tôi để biết hướng dẫn thiết lập chi tiết cho Firefox, Chrome và các trình duyệt khác.

---

## Cài đặt trên Debian

### Thông Báo Quan Trọng

- Đảm bảo bạn không chạy I2P với quyền root: `ps aux | grep i2p`
- Kiểm tra logs: `tail -f ~/.i2p/wrapper.log`
- Xác minh Java đã được cài đặt: `java -version`

### Điều kiện tiên quyết

Nếu bạn gặp lỗi khóa GPG trong quá trình cài đặt:

1. Tải xuống lại và xác minh dấu vân tay khóa (Bước 3-4 ở trên)
2. Đảm bảo file keyring có quyền truy cập đúng: `sudo chmod 644 /usr/share/keyrings/i2p-archive-keyring.gpg`

### Các Bước Cài Đặt

Nếu I2P không nhận được cập nhật:

1. Xác minh repository đã được cấu hình: `cat /etc/apt/sources.list.d/i2p.list`
2. Cập nhật danh sách gói: `sudo apt-get update`
3. Kiểm tra các bản cập nhật I2P: `sudo apt-get upgrade`

### Migrating from old repositories

Nếu bạn đang sử dụng các repository cũ `deb.i2p2.de` hoặc `deb.i2p2.no`:

1. Xóa repository cũ: `sudo rm /etc/apt/sources.list.d/i2p.list`
2. Làm theo các bước [Cài đặt trên Debian](#debian-installation) ở trên
3. Cập nhật: `sudo apt-get update && sudo apt-get install i2p i2p-keyring`

---


## Next Steps

Bây giờ I2P đã được cài đặt và đang chạy:

- [Cấu hình trình duyệt của bạn](/docs/guides/browser-config) để truy cập các trang web I2P
- Khám phá [bảng điều khiển router I2P](http://127.0.0.1:7657/) để giám sát router của bạn
- Tìm hiểu về [các ứng dụng I2P](/docs/applications/) bạn có thể sử dụng
- Đọc về [cách hoạt động của I2P](/docs/overview/tech-intro) để hiểu về mạng lưới

Chào mừng đến với Invisible Internet!
