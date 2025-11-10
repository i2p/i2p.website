---
title: "Sử dụng git bundle để lấy mã nguồn I2P"
date: 2020-03-18
author: "idk"
description: "Tải xuống mã nguồn I2P qua Bittorrent"
categories: ["development"]
---

Việc nhân bản (clone) các kho mã nguồn phần mềm lớn qua I2P có thể khó khăn, và việc dùng Git đôi khi còn làm điều này khó hơn. May mắn là đôi khi nó cũng giúp dễ hơn. Git có lệnh `git bundle` có thể dùng để biến một kho Git thành một tệp mà Git sau đó có thể clone, fetch, hoặc import từ một vị trí trên đĩa cục bộ của bạn. Bằng cách kết hợp khả năng này với việc tải xuống BitTorrent, chúng ta có thể giải quyết các vấn đề còn lại với `git clone`.

## Trước khi bắt đầu

Nếu bạn dự định tạo một git bundle, bạn **phải** đã có sẵn một bản sao đầy đủ của kho **git**, không phải kho mtn. Bạn có thể lấy nó từ github hoặc từ git.idk.i2p, nhưng một shallow clone (bản sao nông, clone với --depth=1) *sẽ không hoạt động*. Quá trình đó sẽ thất bại một cách âm thầm, tạo ra một thứ trông như một bundle, nhưng khi bạn thử clone nó thì sẽ thất bại. Nếu bạn chỉ đang tải về một git bundle đã được tạo sẵn, thì phần này không áp dụng cho bạn.

## Tải mã nguồn I2P qua Bittorrent

Ai đó sẽ cần cung cấp cho bạn một tệp torrent hoặc một liên kết magnet tương ứng với `git bundle` hiện có mà họ đã tạo sẵn cho bạn. Khi bạn đã có một bundle từ bittorrent, bạn sẽ cần dùng git để tạo một kho lưu trữ làm việc từ nó.

## Sử dụng `git clone`

Nhân bản từ một git bundle (gói bundle của Git) rất dễ, chỉ cần:

```
git clone $HOME/.i2p/i2psnark/i2p.i2p.bundle
```
Nếu bạn gặp lỗi sau đây, hãy thử chạy git init và git fetch thủ công thay vào đó:

```
fatal: multiple updates for ref 'refs/remotes/origin/master' not allowed
```
## Sử dụng `git init` và `git fetch`

Đầu tiên, tạo một thư mục i2p.i2p để biến nó thành một kho Git:

```
mkdir i2p.i2p && cd i2p.i2p
```
Tiếp theo, khởi tạo một kho Git trống để nhận các thay đổi được lấy về:

```
git init
```
Cuối cùng, lấy về kho lưu trữ từ gói:

```
git fetch $HOME/.i2p/i2psnark/i2p.i2p.bundle
```
## Thay thế remote bundle bằng remote upstream

Bây giờ bạn đã có bundle, bạn có thể theo dõi các thay đổi bằng cách thiết lập remote trỏ đến nguồn kho upstream:

```
git remote set-url origin git@127.0.0.1:i2p-hackers/i2p.i2p
```
## Tạo gói

Trước hết, hãy làm theo hướng dẫn Git cho Người dùng cho đến khi bạn có một clone (bản sao) đã `--unshallow` thành công của kho lưu trữ i2p.i2p. Nếu bạn đã có một clone, hãy đảm bảo chạy `git fetch --unshallow` trước khi bạn tạo một gói torrent.

Khi bạn đã có nó, chỉ cần chạy ant target tương ứng:

```
ant bundle
```
và sao chép gói kết quả vào thư mục tải xuống của I2PSnark. Ví dụ:

```
cp i2p.i2p.bundle* $HOME/.i2p/i2psnark/
```
Trong một hoặc hai phút nữa, I2PSnark sẽ phát hiện torrent. Nhấp vào nút "Start" để bắt đầu seed (chia sẻ) torrent.
