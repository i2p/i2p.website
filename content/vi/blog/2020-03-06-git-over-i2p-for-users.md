---
title: "Git qua I2P dành cho người dùng"
date: 2020-03-06
author: "idk"
description: "Git qua I2P"
categories: ["development"]
---

Hướng dẫn thiết lập truy cập git thông qua một I2P Tunnel. Tunnel này sẽ đóng vai trò là điểm truy cập của bạn tới một dịch vụ git duy nhất trên I2P. Đây là một phần của nỗ lực tổng thể nhằm chuyển I2P từ monotone sang Git.

## Trước hết: Hãy nắm rõ các khả năng mà dịch vụ cung cấp cho công chúng

Tùy thuộc vào cách dịch vụ Git được cấu hình, nó có thể cung cấp hoặc không cung cấp tất cả các dịch vụ trên cùng một địa chỉ.
Trong trường hợp git.idk.i2p, có một URL HTTP công khai và một URL SSH để cấu hình cho máy khách Git SSH của bạn.
Cả hai đều có thể được dùng để push hoặc pull, nhưng SSH được khuyến nghị.

## Đầu tiên: Tạo tài khoản trên một dịch vụ Git

Để tạo các kho của bạn trên một dịch vụ git từ xa, hãy đăng ký một tài khoản người dùng tại dịch vụ đó. Dĩ nhiên, bạn cũng có thể tạo các kho cục bộ và đẩy (push) chúng lên một dịch vụ git từ xa, nhưng đa số các dịch vụ sẽ yêu cầu có tài khoản và bạn phải tạo sẵn một kho (repository) trên máy chủ.

## Thứ hai: Tạo một dự án để thử nghiệm

Để đảm bảo quá trình thiết lập hoạt động, sẽ hữu ích nếu tạo một kho lưu trữ để kiểm thử từ phía máy chủ. Truy cập kho i2p-hackers/i2p.i2p và fork nó vào tài khoản của bạn.

## Thứ ba: Thiết lập tunnel máy khách Git của bạn

Để có quyền truy cập đọc-ghi vào một máy chủ, bạn sẽ cần thiết lập một tunnel (đường hầm) cho client SSH của mình. Nếu bạn chỉ cần nhân bản HTTP/S ở chế độ chỉ đọc, thì bạn có thể bỏ qua tất cả điều này và chỉ cần dùng biến môi trường http_proxy để cấu hình git sử dụng I2P HTTP Proxy đã được cấu hình sẵn. Ví dụ:

```
http_proxy=http://localhost:4444 git clone --depth=1 http://git.idk.i2p/youruser/i2p.i2p
git fetch --unshallow
```
Để truy cập SSH, khởi chạy "New Tunnel Wizard" từ http://127.0.0.1:7657/i2ptunnelmgr và thiết lập một client tunnel trỏ tới địa chỉ base32 SSH của dịch vụ Git.

## Thứ tư: Thử nhân bản

Bây giờ tunnel của bạn đã được thiết lập xong, bạn có thể thử thực hiện clone (nhân bản) qua SSH:

```
GIT_SSH_COMMAND="ssh -p 7670" \
    git clone git@127.0.0.1:youruser/i2p.i2p
```
Bạn có thể gặp lỗi khi phía đầu xa (remote) ngắt kết nối đột ngột. Thật không may, git vẫn chưa hỗ trợ clone có thể tiếp tục (resumable cloning). Cho đến lúc đó, có một vài cách khá đơn giản để xử lý. Cách đầu tiên và dễ nhất là thử clone với độ sâu nông (shallow depth):

```
GIT_SSH_COMMAND="ssh -p 7670" \
    git clone --depth 1 git@127.0.0.1:youruser/i2p.i2p
```
Sau khi bạn đã thực hiện một shallow clone (sao chép nông), bạn có thể tải nốt phần còn lại với khả năng nối lại bằng cách chuyển vào thư mục repo và chạy:

```
git fetch --unshallow
```
Tại thời điểm này, bạn vẫn chưa có tất cả các nhánh của mình. Bạn có thể lấy chúng bằng cách chạy:

```
git config remote.origin.fetch "+refs/heads/*:refs/remotes/origin/*"
git fetch origin
```
## Quy trình làm việc được đề xuất cho các nhà phát triển

Kiểm soát phiên bản hoạt động tốt nhất khi được sử dụng đúng cách! Chúng tôi đặc biệt khuyến nghị quy trình làm việc fork-first, feature-branch:

1. **Never make changes to the Master Branch**. Use the master branch to periodically obtain updates to the official source code. All changes should be made in feature branches.

2. Set up a second remote in your local repository using the upstream source code:

```
git remote add upstream git@127.0.0.1:i2p-hackers/i2p.i2p
```
3. Pull in any upstream changes on your current master:

```
git pull upstream master
```
4. Before making any changes to the source code, check out a new feature branch to develop on:

```
git checkout -b feature-branch-name
```
5. When you're done with your changes, commit them and push them to your branch:

```
git commit -am "I added an awesome feature!"
git push origin feature-branch-name
```
6. Submit a merge request. When the merge request is approved, check out the master locally and pull in the changes:

```
git checkout master
git pull upstream master
```