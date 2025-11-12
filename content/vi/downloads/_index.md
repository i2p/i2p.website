---
title: "Tải xuống I2P"
description: "Tải xuống phiên bản mới nhất của I2P cho Windows, macOS, Linux, Android và nhiều nền tảng khác"
type: "tải xuống"
layout: "downloads"
current_version: "2.10.0"
android_version: "2.10.1"
downloads: # Cài đặt và Cấu hình I2P

I2P là một mạng riêng tư cho phép người dùng duyệt web, gửi tin nhắn, và chia sẻ tệp một cách an toàn và ẩn danh. Để bắt đầu sử dụng I2P, bạn cần cài đặt phần mềm I2P router trên máy tính của mình.

## Yêu cầu hệ thống

- **Hệ điều hành**: Windows, macOS, Linux
- **Java**: Phiên bản 8 hoặc mới hơn
- **Bộ nhớ**: Tối thiểu 512 MB RAM
- **Dung lượng đĩa**: Ít nhất 100 MB

## Hướng dẫn cài đặt

1. Tải xuống gói cài đặt I2P từ [trang web chính thức của I2P](https://geti2p.net).
2. Chạy tệp cài đặt và làm theo hướng dẫn trên màn hình.
3. Sau khi cài đặt, khởi động I2P router từ menu ứng dụng của bạn.

## Cấu hình ban đầu

Khi I2P router khởi động lần đầu tiên, nó sẽ tự động cấu hình các tham số cơ bản. Tuy nhiên, bạn có thể tùy chỉnh cấu hình để tối ưu hóa hiệu suất.

### Cấu hình băng thông

- Truy cập trang cấu hình băng thông tại `http://127.0.0.1:7657/config`
- Điều chỉnh cài đặt băng thông tải lên và tải xuống theo tốc độ kết nối internet của bạn.

### Thiết lập proxy

Để duyệt web thông qua I2P, bạn cần cấu hình trình duyệt của mình để sử dụng proxy HTTP của I2P.

- **Địa chỉ proxy**: `127.0.0.1`
- **Cổng proxy**: `4444`

## Khám phá thêm

Để tìm hiểu thêm về cách sử dụng I2P, hãy truy cập [tài liệu chính thức của I2P](https://geti2p.net/documentation).
windows: Cung cấp CHỈ bản dịch, không có gì khác:
file: "i2pinstall_2.10.0-0_windows.exe"
size: "~24 triệu"
requirements: "Yêu cầu Java"
sha256: "f96110b00c28591691d409bd2f1768b7906b80da5cab2e20ddc060cbb4389fbf"
links: Cung cấp CHỈ bản dịch, không có gì khác:
primary: "https://i2p.net/files/2.10.0/i2pinstall_2.10.0-0_windows.exe"
mirror: "https://mirror.stormycloud.org/2.10.0/i2pinstall_2.10.0-0_windows.exe"
torrent: "magnet:?xt=urn:btih:75d8c74e9cc52f5cb4982b941d7e49f9f890c458&dn=i2pinstall_2.10.0-0_windows.exe&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.torrent.eu.org%3A451%2Fannounce&tr=http%3A%2F%2Ftracker2.postman.i2p%2Fannounce&tr=http%3A%2F%2Fopentracker.simp.i2p%2Fa&tr=http%3A%2F%2Fopentracker.skank.i2p%2Fa&tr=http%3A%2F%2Fopentracker.dg2.i2p%2Fa&tr=udp%3A%2F%2Fdht.transmissionbt.com%3A6881&tr=udp%3A%2F%2Fdht.aelitis.com%3A6881&tr=udp%3A%2F%2Frouter.bittorrent.com%3A6881"
i2p: "http://mirror.stormycloud.i2p/2.10.0/i2pinstall_2.10.0-0_windows.exe"
tor: "http://hhn4r4qyrmplmfiermza6p3d67a5ra7ecwjeoo5a5ddiogwhyjg675id.onion/2.10.0/i2pinstall_2.10.0-0_windows.exe"
windows_easy_installer: # Cài đặt và Cấu hình I2P

## Giới thiệu

I2P (The Invisible Internet Project) là một mạng ẩn danh được thiết kế để bảo vệ quyền riêng tư của người dùng khi truy cập internet. Nó sử dụng các kỹ thuật như garlic encryption để đảm bảo dữ liệu được bảo mật và không thể bị theo dõi.

## Yêu cầu hệ thống

- Java 8 hoặc mới hơn
- Ít nhất 128 MB RAM
- Kết nối internet ổn định

## Cài đặt

1. Tải xuống gói cài đặt từ [trang web chính thức của I2P](https://geti2p.net).
2. Chạy tệp cài đặt và làm theo hướng dẫn trên màn hình.
3. Sau khi cài đặt, khởi động I2P router từ menu ứng dụng của bạn.

## Cấu hình

### Cấu hình cơ bản

- Mở giao diện quản lý I2P router qua trình duyệt tại `http://127.0.0.1:7657`.
- Điều chỉnh băng thông và các cài đặt khác theo nhu cầu của bạn.

### Thiết lập I2PTunnel

I2PTunnel cho phép bạn tạo các tunnel để truy cập các dịch vụ ẩn danh. Để thiết lập một tunnel mới:

1. Truy cập phần "I2PTunnel" trong giao diện quản lý.
2. Chọn loại tunnel bạn muốn tạo (ví dụ: HTTP, SOCKS).
3. Nhập các thông số cần thiết và lưu cấu hình.

## Khắc phục sự cố

Nếu bạn gặp vấn đề khi sử dụng I2P, hãy kiểm tra:

- Kết nối internet của bạn.
- Nhật ký lỗi trong giao diện quản lý.
- Diễn đàn hỗ trợ của I2P để tìm giải pháp từ cộng đồng.
file: "I2P-Easy-Install-Bundle-2.10.0-signed.exe"
size: "~162M"
requirements: "Không cần Java - đi kèm với môi trường chạy Java"
sha256: "afcc937004bcf41d4dd2e40de27f33afac3de0652705aef904834fd18afed4b6"
beta: đúng
links: Cung cấp CHỈ bản dịch, không có gì khác:
primary: "https://i2p.net/files/2.10.0/I2P-Easy-Install-Bundle-2.10.0-signed.exe"
mirror: "https://mirror.stormycloud.org/2.10.0/I2P-Easy-Install-Bundle-2.10.0-signed.exe"
torrent: "magnet:?xt=urn:btih:79e1172aaa21e5bd395a408850de17eff1c5ec24&dn=I2P-Easy-Install-Bundle-2.10.0-signed.exe&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.torrent.eu.org%3A451%2Fannounce&tr=http%3A%2F%2Ftracker2.postman.i2p%2Fannounce&tr=http%3A%2F%2Fopentracker.simp.i2p%2Fa&tr=http%3A%2F%2Fopentracker.skank.i2p%2Fa&tr=http%3A%2F%2Fopentracker.dg2.i2p%2Fa&tr=udp%3A%2F%2Fdht.transmissionbt.com%3A6881&tr=udp%3A%2F%2Fdht.aelitis.com%3A6881&tr=udp%3A%2F%2Frouter.bittorrent.com%3A6881"
i2p: "http://mirror.stormycloud.i2p/2.10.0/I2P-Easy-Install-Bundle-2.10.0-signed.exe"
tor: "http://hhn4r4qyrmplmfiermza6p3d67a5ra7ecwjeoo5a5ddiogwhyjg675id.onion/2.10.0/I2P-Easy-Install-Bundle-2.10.0-signed.exe"
mac_linux: Cung cấp CHỈ bản dịch, không có gì khác:
file: "i2pinstall_2.10.0.jar"
size: "~30 triệu"
requirements: "Java 8 hoặc cao hơn"
sha256: "76372d552dddb8c1d751dde09bae64afba81fef551455e85e9275d3d031872ea"
links: Cung cấp CHỈ bản dịch, không có gì khác:
primary: "https://i2p.net/files/2.10.0/i2pinstall_2.10.0.jar"
mirror: "https://mirror.stormycloud.org/2.10.0/i2pinstall_2.10.0.jar"
torrent: "magnet:?xt=urn:btih:20ce01ea81b437ced30b1574d457cce55c86dce2&dn=i2pinstall_2.10.0.jar&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.torrent.eu.org%3A451%2Fannounce&tr=http%3A%2F%2Ftracker2.postman.i2p%2Fannounce&tr=http%3A%2F%2Fopentracker.simp.i2p%2Fa&tr=http%3A%2F%2Fopentracker.skank.i2p%2Fa&tr=http%3A%2F%2Fopentracker.dg2.i2p%2Fa&tr=udp%3A%2F%2Fdht.transmissionbt.com%3A6881&tr=udp%3A%2F%2Fdht.aelitis.com%3A6881&tr=udp%3A%2F%2Frouter.bittorrent.com%3A6881"
i2p: "http://mirror.stormycloud.i2p/2.10.0/i2pinstall_2.10.0.jar"
tor: "http://hhn4r4qyrmplmfiermza6p3d67a5ra7ecwjeoo5a5ddiogwhyjg675id.onion/2.10.0/i2pinstall_2.10.0.jar"
source: Cung cấp CHỈ bản dịch, không có gì khác:
file: "i2psource_2.10.0.tar.bz2"
size: "~33 triệu"
sha256: "3b651b761da530242f6db6536391fb781bc8e07129540ae7e96882bcb7bf2375"
links: Cung cấp CHỈ bản dịch, không có gì khác:
primary: "https://i2p.net/files/2.10.0/i2psource_2.10.0.tar.bz2"
torrent: "magnet:?xt=urn:btih:f62f519204abefb958d553f737ac0a7e84698f35&dn=i2psource_2.10.0.tar.bz2&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.torrent.eu.org%3A451%2Fannounce&tr=http%3A%2F%2Ftracker2.postman.i2p%2Fannounce&tr=http%3A%2F%2Fopentracker.simp.i2p%2Fa&tr=http%3A%2F%2Fopentracker.skank.i2p%2Fa&tr=http%3A%2F%2Fopentracker.dg2.i2p%2Fa&tr=udp%3A%2F%2Fdht.transmissionbt.com%3A6881&tr=udp%3A%2F%2Fdht.aelitis.com%3A6881&tr=udp%3A%2F%2Frouter.bittorrent.com%3A6881"
github: "https://github.com/i2p/i2p.i2p"
android: Cung cấp CHỈ bản dịch, không có gì khác:
file: "I2P.apk"
version: "2.10.1"
size: "~28 MB"
requirements: "Android 4.0+, tối thiểu 512MB RAM"
sha256: "c3d4e5f6789012345678901234567890123456789012345678901234abcdef"
links: Cung cấp CHỈ bản dịch, không có gì khác:
primary: "https://download.i2p.io/android/I2P.apk"
torrent: "magnet:?xt=urn:btih:android_example"
i2p: "http://stats.i2p/android/I2P.apk"
mirrors: Cung cấp CHỈ bản dịch, không có gì khác:
primary: Cung cấp CHỈ bản dịch, không có gì khác:
name: "StormyCloud"
location: "Hoa Kỳ"
url: "https://stormycloud.org"
resources: Cung cấp CHỈ bản dịch, không có gì khác:
archive: "https://download.i2p.io/archive/"
pgp_keys: "/tải-về/khóa-pgp"
---
