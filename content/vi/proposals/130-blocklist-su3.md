---
title: "Danh sách chặn trong Định dạng SU3"
number: "130"
author: "psi, zzz"
created: "2016-11-23"
lastupdated: "2016-11-23"
status: "Open"
thread: "http://zzz.i2p/topics/2192"
---

## Tổng quan

Đề xuất này là để phân phối các cập nhật danh sách chặn trong một tệp su3 riêng biệt.

## Động lực

Nếu không có điều này, danh sách chặn chỉ được cập nhật trong bản phát hành. Định dạng này có thể được sử dụng trong các triển khai bộ định tuyến khác nhau.

## Thiết kế

Định nghĩa định dạng để bọc trong một tệp su3. Cho phép chặn bằng IP hoặc hash của bộ định tuyến. Các bộ định tuyến có thể đăng ký một URL hoặc nhập một tệp được thu thập bằng các phương tiện khác. Tệp su3 chứa chữ ký cần phải được xác minh khi nhập.

## Đặc tả

Sẽ được thêm vào trang đặc tả cập nhật bộ định tuyến.

Định nghĩa loại nội dung mới BLOCKLIST (5). Định nghĩa loại tệp mới TXT_GZ (4) (định dạng .txt.gz). Các mục được ghi một dòng mỗi, hoặc là một địa chỉ IPv4 hoặc IPv6 rõ ràng, hoặc một hash bộ định tuyến mã hóa base64 có 44 ký tự. Hỗ trợ chặn với mặt nạ mạng, ví dụ x.y.0.0/16, là tuỳ chọn. Để bỏ chặn một mục, đặt trước nó với '!'. Các bình luận bắt đầu với '#'.

## Chuyển đổi

không áp dụng

## Xem thêm

Đề xuất 129
