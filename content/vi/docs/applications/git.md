---
title: "Git qua I2P"
description: "Kết nối các Git client với các dịch vụ lưu trữ trên I2P như i2pgit.org"
slug: "git"
lastUpdated: "2025-02"
accurateFor: "2.5.0"
reviewStatus: "needs-review"
---

Việc sao chép và đẩy các kho lưu trữ bên trong I2P sử dụng các lệnh Git giống như bạn đã biết—client của bạn chỉ đơn giản là kết nối thông qua các tunnel I2P thay vì TCP/IP. Hướng dẫn này sẽ hướng dẫn bạn cách thiết lập tài khoản, cấu hình tunnel, và xử lý các liên kết chậm.

> **Bắt đầu nhanh:** Truy cập chỉ đọc hoạt động thông qua HTTP proxy: `http_proxy=http://127.0.0.1:4444 git clone http://example.i2p/project.git`. Thực hiện các bước bên dưới để có quyền truy cập đọc/ghi qua SSH.

## 1. Tạo Tài Khoản

Chọn một dịch vụ Git I2P và đăng ký:

- Bên trong I2P: `http://git.idk.i2p`
- Mirror clearnet: `https://i2pgit.org`

Việc đăng ký có thể yêu cầu phê duyệt thủ công; kiểm tra trang đích để biết hướng dẫn. Sau khi được phê duyệt, hãy fork hoặc tạo một repository để bạn có thứ gì đó để thử nghiệm.

## 2. Cấu hình I2PTunnel Client (SSH)

1. Mở bảng điều khiển router → **I2PTunnel** và thêm một tunnel **Client** mới.
2. Nhập destination của dịch vụ (Base32 hoặc Base64). Đối với `git.idk.i2p`, bạn sẽ tìm thấy cả destination HTTP và SSH trên trang chủ của dự án.
3. Chọn một cổng cục bộ (ví dụ `localhost:7442`).
4. Bật tự động khởi động nếu bạn có kế hoạch sử dụng tunnel thường xuyên.

Giao diện người dùng sẽ xác nhận tunnel mới và hiển thị trạng thái của nó. Khi đang chạy, các SSH client có thể kết nối tới `127.0.0.1` trên cổng đã chọn.

## 3. Sao chép qua SSH

Sử dụng cổng tunnel với `GIT_SSH_COMMAND` hoặc một đoạn cấu hình SSH:

```bash
GIT_SSH_COMMAND="ssh -p 7442" \
    git clone git@127.0.0.1:your-project/example.git
```
Nếu lần thử đầu tiên thất bại (các tunnel có thể chậm), hãy thử shallow clone:

```bash
GIT_SSH_COMMAND="ssh -p 7442" \
    git clone --depth 1 git@127.0.0.1:your-project/example.git
cd example
git fetch --unshallow
```
Cấu hình Git để tải về tất cả các nhánh:

```bash
git config remote.origin.fetch "+refs/heads/*:refs/remotes/origin/*"
git fetch origin
```
### Mẹo Tối Ưu Hiệu Suất

- Thêm một hoặc hai tunnel dự phòng trong trình chỉnh sửa tunnel để cải thiện khả năng phục hồi.
- Đối với việc thử nghiệm hoặc các repo có rủi ro thấp, bạn có thể giảm độ dài tunnel xuống 1 hop, nhưng hãy lưu ý về sự đánh đổi tính ẩn danh.
- Giữ `GIT_SSH_COMMAND` trong môi trường của bạn hoặc thêm một mục vào `~/.ssh/config`:

```sshconfig
Host git.i2p
    HostName 127.0.0.1
    Port 7442
    User git
```
Sau đó clone bằng lệnh `git clone git@git.i2p:namespace/project.git`.

## 4. Gợi ý Quy trình Làm việc

Áp dụng quy trình làm việc fork-and-branch phổ biến trên GitLab/GitHub:

1. Thiết lập remote upstream: `git remote add upstream git@git.i2p:I2P_Developers/i2p.i2p`
2. Giữ `master` của bạn đồng bộ: `git pull upstream master`
3. Tạo các nhánh tính năng cho thay đổi: `git checkout -b feature/new-thing`
4. Đẩy các nhánh lên fork của bạn: `git push origin feature/new-thing`
5. Gửi merge request, sau đó fast-forward master của fork từ upstream.

## 5. Nhắc nhở về Quyền riêng tư

- Git lưu trữ dấu thời gian commit theo múi giờ địa phương của bạn. Để buộc sử dụng dấu thời gian UTC:

```bash
git config --global alias.utccommit '!git commit --date="$(date --utc +%Y-%m-%dT%H:%M:%S%z)"'
```
Sử dụng `git utccommit` thay vì `git commit` khi vấn đề riêng tư quan trọng.

- Tránh nhúng các URL clearnet hoặc địa chỉ IP vào thông điệp commit hoặc metadata của repository nếu tính ẩn danh là một mối quan tâm.

## 6. Khắc phục sự cố

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Symptom</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Fix</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>connection closed</code> during clone</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Retry with <code>--depth 1</code>, add backup tunnels, or increase tunnel quantities.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>ssh: connect to host 127.0.0.1 port …: Connection refused</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Ensure the I2PTunnel client is running and SAM is enabled.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Slow performance</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Lower tunnel length, increase bandwidth limits, or schedule large fetches during off-peak hours.</td>
    </tr>
  </tbody>
</table>
Đối với các kịch bản nâng cao (sao chép repo bên ngoài, phân phối bundle), xem các hướng dẫn bổ sung: [Quy trình làm việc với Git bundle](/docs/applications/git-bundle/) và [Lưu trữ GitLab trên I2P](/docs/guides/gitlab/).
