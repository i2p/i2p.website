---
title: "Chạy GitLab trên I2P"
description: "Triển khai GitLab bên trong I2P sử dụng Docker và I2P router"
slug: "gitlab"
lastUpdated: "2025-02"
accurateFor: "2.5.0"
---

Hosting GitLab bên trong I2P khá đơn giản: chạy container GitLab omnibus, expose nó trên loopback, và forward traffic thông qua I2P tunnel. Các bước dưới đây tương tự với cấu hình được sử dụng cho `git.idk.i2p` nhưng có thể áp dụng cho bất kỳ instance tự host nào.

## 1. Yêu cầu tiên quyết

- Debian hoặc một bản phân phối Linux khác đã cài đặt Docker Engine (`sudo apt install docker.io` hoặc `docker-ce` từ repo của Docker).
- Một I2P router (Java I2P hoặc i2pd) với băng thông đủ để phục vụ người dùng của bạn.
- Tùy chọn: một VM chuyên dụng để GitLab và router được cách ly khỏi môi trường desktop của bạn.

## 2. Tải Image GitLab

```bash
docker pull gitlab/gitlab-ce:latest
```
Image chính thức được xây dựng từ các lớp nền Ubuntu và được cập nhật thường xuyên. Kiểm tra [Dockerfile](https://gitlab.com/gitlab-org/omnibus-gitlab/-/blob/master/docker/Dockerfile) nếu bạn cần thêm sự đảm bảo.

## 3. Quyết định giữa Bridging và I2P-Only

- **Chỉ I2P** (I2P-only) các instance không bao giờ kết nối với các máy chủ clearnet. Người dùng có thể mirror các repository từ các dịch vụ I2P khác nhưng không từ GitHub/GitLab.com. Điều này tối đa hóa tính ẩn danh.
- **Cầu nối** (Bridged) các instance kết nối đến các máy chủ Git clearnet thông qua HTTP proxy. Điều này hữu ích để mirror các dự án công khai vào I2P nhưng nó làm mất tính ẩn danh của các yêu cầu gửi đi từ server.

Nếu bạn chọn chế độ bridged, hãy cấu hình GitLab để sử dụng I2P HTTP proxy được bind trên Docker host (ví dụ `http://172.17.0.1:4446`). Proxy router mặc định chỉ lắng nghe trên `127.0.0.1`; hãy thêm một tunnel proxy mới được bind vào địa chỉ gateway của Docker.

## 4. Khởi động Container

```bash
docker run --detach \
  --env HTTP_PROXY=http://172.17.0.1:4446 \  # omit for I2P-only
  --publish 127.0.0.1:8443:443 \
  --publish 127.0.0.1:8080:80 \
  --publish 127.0.0.1:8022:22 \
  --name gitlab \
  --restart always \
  --volume /srv/gitlab/config:/etc/gitlab:Z \
  --volume /srv/gitlab/logs:/var/log/gitlab:Z \
  --volume /srv/gitlab/data:/var/opt/gitlab:Z \
  gitlab/gitlab-ce:latest
```
- Bind các cổng đã publish vào loopback; các I2P tunnel sẽ expose chúng khi cần thiết.
- Thay thế `/srv/gitlab/...` bằng đường dẫn lưu trữ phù hợp với host của bạn.

Sau khi container đang chạy, truy cập `https://127.0.0.1:8443/`, đặt mật khẩu quản trị viên và cấu hình giới hạn tài khoản.

## 5. Expose GitLab Through I2P

Tạo ba tunnel **máy chủ** I2PTunnel:

| Purpose | Local target | Suggested inbound port |
| --- | --- | --- |
| HTTPS web UI | `127.0.0.1:8443` | auto-generated |
| HTTP web UI (optional) | `127.0.0.1:8080` | auto-generated |
| SSH push/pull | `127.0.0.1:8022` | auto-generated |
Cấu hình mỗi tunnel với độ dài tunnel và băng thông phù hợp. Đối với các instance công khai, 3 hop với 4–6 tunnel mỗi chiều là điểm khởi đầu tốt. Công bố các địa chỉ đích Base32/Base64 thu được trên trang landing page của bạn để người dùng có thể cấu hình client tunnel.

### Destination Enforcement

Nếu bạn sử dụng HTTP(S) tunnel, hãy bật destination enforcement (cưỡng chế đích đến) để chỉ hostname dự định mới có thể truy cập dịch vụ. Điều này ngăn tunnel bị lạm dụng như một proxy chung.

## 6. Maintenance Tips

- Chạy `docker exec gitlab gitlab-ctl reconfigure` mỗi khi bạn thay đổi cài đặt GitLab.
- Theo dõi dung lượng đĩa (`/srv/gitlab/data`)—các repository Git phát triển nhanh chóng.
- Sao lưu thư mục cấu hình và dữ liệu thường xuyên. [Các tác vụ rake backup](https://docs.gitlab.com/ee/raketasks/backup_restore.html) của GitLab hoạt động bên trong container.
- Cân nhắc đặt một tunnel giám sát bên ngoài ở chế độ client để đảm bảo dịch vụ có thể truy cập được từ mạng lưới rộng hơn.

## 6. Mẹo Bảo Trì

- [Nhúng I2P vào ứng dụng của bạn](/docs/applications/embedding/)
- [Git trên I2P (hướng dẫn client)](/docs/applications/git/)
- [Git bundles cho mạng chậm/ngoại tuyến](/docs/applications/git-bundle/)

Một instance GitLab được cấu hình tốt cung cấp một trung tâm phát triển cộng tác hoàn toàn bên trong I2P. Giữ cho router khỏe mạnh, cập nhật thường xuyên các bản vá bảo mật của GitLab, và phối hợp với cộng đồng khi số lượng người dùng của bạn tăng lên.
