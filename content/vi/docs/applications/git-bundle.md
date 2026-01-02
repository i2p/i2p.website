---
title: "Git Bundles cho I2P"
description: "Tải và phân phối kho lưu trữ lớn với git bundle và BitTorrent"
slug: "git-bundle"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

Khi điều kiện mạng khiến `git clone` không ổn định, bạn có thể phân phối repository dưới dạng **git bundle** qua BitTorrent hoặc bất kỳ phương thức truyền tải file nào khác. Bundle là một file đơn chứa toàn bộ lịch sử của repository. Sau khi tải xuống, bạn fetch từ nó ở local rồi chuyển lại về remote upstream.

## 1. Trước Khi Bắt Đầu

Tạo bundle yêu cầu bản sao Git **đầy đủ**. Các bản sao nông (shallow clone) được tạo bằng `--depth 1` sẽ âm thầm tạo ra các bundle bị lỗi mà có vẻ hoạt động nhưng thất bại khi người khác cố gắng sử dụng chúng. Luôn fetch từ nguồn đáng tin cậy (GitHub tại [github.com/i2p/i2p.i2p](https://github.com/i2p/i2p.i2p), I2P Gitea instance tại [i2pgit.org](https://i2pgit.org), hoặc `git.idk.i2p` qua I2P) và chạy `git fetch --unshallow` nếu cần thiết để chuyển đổi bất kỳ bản sao nông nào thành bản sao đầy đủ trước khi tạo bundle.

Nếu bạn chỉ sử dụng một bundle hiện có, chỉ cần tải xuống. Không cần chuẩn bị đặc biệt gì.

## 2. Tải xuống Gói cài đặt

### Obtaining the Bundle File

Tải file bundle thông qua BitTorrent bằng I2PSnark (trình torrent tích hợp sẵn trong I2P) hoặc các client tương thích I2P khác như BiglyBT với plugin I2P.

**Quan trọng**: I2PSnark chỉ hoạt động với các torrent được tạo riêng cho mạng I2P. Các torrent clearnet thông thường không tương thích vì I2P sử dụng Destination (địa chỉ dài 387+ byte) thay vì địa chỉ IP và cổng.

Vị trí file bundle phụ thuộc vào loại cài đặt I2P của bạn:

- **Cài đặt người dùng/thủ công** (cài đặt bằng trình cài đặt Java): `~/.i2p/i2psnark/`
- **Cài đặt hệ thống/daemon** (cài đặt qua apt-get hoặc trình quản lý gói): `/var/lib/i2p/i2p-config/i2psnark/`

Người dùng BiglyBT sẽ tìm thấy các tệp đã tải xuống trong thư mục downloads đã cấu hình của họ.

### Cloning from the Bundle

**Phương pháp tiêu chuẩn** (hoạt động trong hầu hết các trường hợp):

```bash
git clone ~/.i2p/i2psnark/i2p.i2p.bundle
```
Nếu bạn gặp lỗi `fatal: multiple updates for ref` (một vấn đề đã biết trong Git 2.21.0 trở lên khi cấu hình Git toàn cục chứa các refspec fetch xung đột), hãy sử dụng phương pháp khởi tạo thủ công:

```bash
mkdir i2p.i2p && cd i2p.i2p
git init
git fetch ~/.i2p/i2psnark/i2p.i2p.bundle
```
Ngoài ra, bạn có thể sử dụng cờ `--update-head-ok`:

```bash
git fetch --update-head-ok ~/.i2p/i2psnark/i2p.i2p.bundle '*:*'
```
### Lấy Tệp Bundle

Sau khi clone từ bundle, hãy trỏ bản clone của bạn vào remote chính thức để các lần fetch sau sẽ đi qua I2P hoặc clearnet:

```bash
git remote set-url origin git@127.0.0.1:I2P_Developers/i2p.i2p
```
Hoặc để truy cập clearnet:

```bash
git remote set-url origin https://github.com/i2p/i2p.i2p
```
Để truy cập SSH qua I2P, bạn cần cấu hình một tunnel SSH client trong bảng điều khiển I2P router của mình (thường là cổng 7670) trỏ đến `g6u4vqiuy6bdc3dbu6a7gmi3ip45sqwgtbgrr6uupqaaqfyztrka.b32.i2p`. Nếu sử dụng cổng không chuẩn:

```bash
GIT_SSH_COMMAND="ssh -p 7670" git clone git@127.0.0.1:I2P_Developers/i2p.i2p
```
## 3. Creating a Bundle

### Sao chép từ Bundle

Đảm bảo repository của bạn được cập nhật đầy đủ với một **bản clone hoàn chỉnh** (không phải shallow):

```bash
git fetch --all
```
Nếu bạn có shallow clone, hãy chuyển đổi nó trước:

```bash
git fetch --unshallow
```
### Chuyển sang Remote Trực Tiếp

**Sử dụng target build của Ant** (được khuyến nghị cho cây mã nguồn I2P):

```bash
ant git-bundle
```
Lệnh này tạo ra cả `i2p.i2p.bundle` (file bundle) và `i2p.i2p.bundle.torrent` (metadata BitTorrent).

**Sử dụng git bundle trực tiếp**:

```bash
git bundle create i2p.i2p.bundle --all
```
Đối với các bundle chọn lọc hơn:

```bash
git bundle create i2p.i2p.bundle --branches --tags
```
### Verifying Your Bundle

Luôn xác minh bundle trước khi phân phối:

```bash
git bundle verify i2p.i2p.bundle
```
Điều này xác nhận bundle hợp lệ và hiển thị các commit điều kiện tiên quyết cần thiết.

### Điều kiện tiên quyết

Sao chép bundle và metadata torrent của nó vào thư mục I2PSnark của bạn:

**Đối với cài đặt người dùng**:

```bash
cp i2p.i2p.bundle* ~/.i2p/i2psnark/
```
**Đối với cài đặt hệ thống**:

```bash
cp i2p.i2p.bundle* /var/lib/i2p/i2p-config/i2psnark/
```
I2PSnark tự động phát hiện và tải các tệp .torrent trong vòng vài giây. Truy cập giao diện web tại [http://127.0.0.1:7657/i2psnark](http://127.0.0.1:7657/i2psnark) để bắt đầu seed.

## 4. Creating Incremental Bundles

Để cập nhật định kỳ, hãy tạo các bundle tăng dần chỉ chứa các commit mới kể từ bundle trước đó:

```bash
git tag lastBundleTag
git bundle create update.bundle lastBundleTag..master
```
Người dùng có thể tải về từ gói cập nhật gia tăng nếu họ đã có kho lưu trữ cơ sở:

```bash
git fetch /path/to/update.bundle
```
Luôn xác minh các gói tăng dần (incremental bundles) hiển thị các commit điều kiện tiên quyết như mong đợi:

```bash
git bundle verify update.bundle
```
## 5. Updating After the Initial Clone

Sau khi bạn có một repository hoạt động từ bundle, hãy xử lý nó như bất kỳ bản sao Git clone nào khác:

```bash
git remote add upstream git@127.0.0.1:I2P_Developers/i2p.i2p
git fetch upstream
git merge upstream/master
```
Hoặc cho các quy trình đơn giản hơn:

```bash
git fetch origin
git pull origin master
```
## 3. Tạo Bundle

- **Phân phối kiên cường**: Các repository lớn có thể được chia sẻ qua BitTorrent, tự động xử lý việc thử lại, xác minh từng phần và tiếp tục tải.
- **Bootstrap ngang hàng**: Những người đóng góp mới có thể bootstrap bản clone của họ từ các peer gần đó trên mạng I2P, sau đó tải các thay đổi tăng dần trực tiếp từ Git host.
- **Giảm tải cho server**: Các mirror có thể công bố các bundle định kỳ để giảm áp lực lên các Git host hoạt động, đặc biệt hữu ích cho các repository lớn hoặc điều kiện mạng chậm.
- **Vận chuyển ngoại tuyến**: Các bundle hoạt động trên bất kỳ phương thức truyền tệp nào (USB drive, truyền trực tiếp, sneakernet), không chỉ BitTorrent.

Bundles không thay thế remotes trực tiếp. Chúng chỉ đơn giản cung cấp phương pháp bootstrapping ổn định hơn cho việc clone ban đầu hoặc các cập nhật lớn.

## 7. Troubleshooting

### Tạo Bundle

**Vấn đề**: Tạo bundle thành công nhưng người khác không thể clone từ bundle.

**Nguyên nhân**: Bản sao nguồn của bạn là shallow (được tạo với tùy chọn `--depth`).

**Giải pháp**: Chuyển đổi sang bản sao đầy đủ (full clone) trước khi tạo bundle:

```bash
git fetch --unshallow
```
### Xác minh Bundle của bạn

**Vấn đề**: `fatal: multiple updates for ref` khi clone từ bundle.

**Nguyên nhân**: Git 2.21.0+ xung đột với các refspec fetch toàn cục trong `~/.gitconfig`.

**Giải pháp**: 1. Sử dụng khởi tạo thủ công: `mkdir repo && cd repo && git init && git fetch /path/to/bundle` 2. Sử dụng cờ `--update-head-ok`: `git fetch --update-head-ok /path/to/bundle '*:*'` 3. Xóa cấu hình xung đột: `git config --global --unset remote.origin.fetch`

### Phân phối qua I2PSnark

**Vấn đề**: `git bundle verify` báo thiếu các điều kiện tiên quyết.

**Nguyên nhân**: Bundle tăng dần hoặc bản sao source không đầy đủ.

**Giải pháp**: Tải các commit tiên quyết hoặc sử dụng bundle cơ sở trước, sau đó áp dụng các bản cập nhật tăng dần.
