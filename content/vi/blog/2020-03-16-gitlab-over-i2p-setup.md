---
title: "Thiết lập Gitlab qua I2P"
date: 2020-03-16
author: "idk"
description: "Phản chiếu các kho lưu trữ Git của I2P và bắc cầu các kho lưu trữ Clearnet (mạng công khai) cho người khác"
categories: ["development"]
---

This is the setup process I use for configuring Gitlab and I2P, with Docker in place to manage the service itself. Gitlab is very easy to host on I2P in this fashion, it can be administered by one person without much difficulty. These instructions should work on any Debian-based system and should easily translate to any system where Docker and an I2P router are available.

## Các phụ thuộc và Docker

Vì Gitlab chạy trong một container, chúng ta chỉ cần cài đặt các phụ thuộc cần thiết cho container trên hệ thống chính của mình. Thật tiện lợi, bạn có thể cài đặt mọi thứ cần thiết bằng:

```
sudo apt install docker.io
```
## Tải về các container Docker

Sau khi bạn đã cài đặt docker, bạn có thể tải về các container docker cần thiết cho gitlab. *Đừng chạy chúng ngay.*

```
docker pull gitlab/gitlab-ce
```
## Set up an I2P HTTP Proxy for Gitlab (Important information, optional steps)

Các máy chủ Gitlab bên trong I2P có thể được vận hành có hoặc không có khả năng tương tác với các máy chủ trên internet bên ngoài I2P. Trong trường hợp máy chủ Gitlab *không được phép* tương tác với các máy chủ bên ngoài I2P, nó không thể bị giải ẩn danh bằng cách sao chép (clone) một kho git từ một máy chủ git trên internet bên ngoài I2P.

Trong trường hợp máy chủ Gitlab *được phép* tương tác với các máy chủ bên ngoài I2P, nó có thể đóng vai trò như một "cầu nối" cho người dùng, để họ có thể sử dụng nó nhằm phản chiếu nội dung từ bên ngoài I2P sang một nguồn có thể truy cập qua I2P, tuy nhiên trong trường hợp này nó *không ẩn danh*.

**If you want to have a bridged, non-anonymous Gitlab instance with access to web repositories**, no further modification is necessary.

**Nếu bạn muốn có một phiên bản Gitlab chỉ I2P mà không có quyền truy cập vào các kho chỉ dành cho Web**, bạn sẽ cần cấu hình Gitlab để sử dụng một I2P HTTP Proxy. Vì I2P HTTP proxy mặc định chỉ lắng nghe trên `127.0.0.1`, bạn sẽ cần thiết lập một proxy mới cho Docker để lắng nghe trên địa chỉ Host/Gateway của mạng Docker, thường là `172.17.0.1`. Tôi cấu hình nó trên cổng `4446`.

## Khởi chạy Container trên máy cục bộ

Sau khi bạn đã thiết lập xong, bạn có thể khởi động container và công bố thể hiện Gitlab của mình cục bộ:

```
docker run --detach \
  --env HTTP_PROXY=http://172.17.0.1:4446 \
  --publish 127.0.0.1:8443:443 --publish 127.0.0.1:8080:80 --publish 127.0.0.1:8022:22 \
  --name gitlab \
  --restart always \
  --volume /srv/gitlab/config:/etc/gitlab:Z \
  --volume /srv/gitlab/logs:/var/log/gitlab:Z \
  --volume /srv/gitlab/data:/var/opt/gitlab:Z \
  gitlab/gitlab-ce:latest
```
Truy cập instance Gitlab cục bộ của bạn và thiết lập tài khoản quản trị viên. Chọn một mật khẩu mạnh và cấu hình các giới hạn tài khoản người dùng để phù hợp với tài nguyên của bạn.

## Thiết lập các tunnel dịch vụ của bạn và đăng ký một tên máy chủ

Sau khi bạn đã thiết lập Gitlab cục bộ, hãy truy cập I2P Router console. Bạn sẽ cần thiết lập hai server tunnels, một cái trỏ tới giao diện web(HTTP) của Gitlab trên cổng TCP 8080, và một cái tới giao diện SSH của Gitlab trên cổng TCP 8022.

### Gitlab Web(HTTP) Interface

Đối với giao diện Web, hãy sử dụng một tunnel máy chủ "HTTP". Từ http://127.0.0.1:7657/i2ptunnelmgr khởi chạy "New Tunnel Wizard" và nhập các giá trị sau:

1. Select "Server Tunnel"
2. Select "HTTP Server"
3. Fill in "Gitlab Web Service" or otherwise describe the tunnel
4. Fill in `127.0.0.1` for the host and `8080` for the port
5. Select "Automatically start tunnel when Router Starts"
6. Confirm your selections

### Gitlab SSH Interface

Đối với giao diện SSH, hãy sử dụng server tunnel "Standard". Từ http://127.0.0.1:7657/i2ptunnelmgr khởi chạy "New Tunnel Wizard" và nhập các giá trị sau:

1. Select "Server Tunnel"
2. Select "Standard Server"
3. Fill in "Gitlab SSH Service" or otherwise describe the tunnel
4. Fill in `127.0.0.1` for the host and `8022` for the port
5. Select "Automatically start tunnel when Router Starts"
6. Confirm your selections

## Re-start the Gitlab Service with the new Hostname

Cuối cùng, nếu bạn đã sửa đổi `gitlab.rb` hoặc đã đăng ký một tên máy chủ, bạn sẽ cần khởi động lại dịch vụ gitlab để các thiết lập có hiệu lực.
