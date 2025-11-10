---
title: "Danh sách chặn trong Bảng tin"
number: "129"
author: "zzz"
created: "2016-11-23"
lastupdated: "2016-12-02"
status: "Đã đóng"
thread: "http://zzz.i2p/topics/2191"
target: "0.9.28"
implementedin: "0.9.28"
---

## Tổng quan

Đề xuất này là phân phối các bản cập nhật danh sách chặn trong tệp tin tức, được phân phối dưới dạng su3 có chữ ký. Được thực hiện trong phiên bản 0.9.28.

## Động cơ

Nếu không có điều này, danh sách chặn chỉ được cập nhật trong bản phát hành. Sử dụng đăng ký tin tức hiện có. Định dạng này có thể được sử dụng trong các bản triển khai bộ định tuyến khác nhau, nhưng chỉ có bộ định tuyến Java sử dụng đăng ký tin tức hiện nay.

## Thiết kế

Thêm một phần mới vào tệp news.xml. Cho phép chặn theo IP hoặc băm của bộ định tuyến. Phần này sẽ có dấu thời gian riêng. Cho phép mở chặn các mục đã chặn trước đây.

Bao gồm một chữ ký của phần, sẽ được chỉ định. Chữ ký sẽ bao gồm dấu thời gian. Chữ ký phải được xác minh khi nhập. Người ký sẽ được chỉ định và có thể khác với người ký su3. Bộ định tuyến có thể sử dụng danh sách tin cậy khác cho danh sách chặn.

## Đặc tả kỹ thuật

Hiện có trên trang đặc tả cập nhật bộ định tuyến.

Các mục có thể là địa chỉ IPv4 hoặc IPv6 truần, hoặc băm của bộ định tuyến được mã hóa base64 44 ký tự. Địa chỉ IPv6 có thể ở định dạng viết tắt (chứa "::"). Hỗ trợ chặn với mặt nạ mạng, ví dụ: x.y.0.0/16, là tùy chọn. Hỗ trợ tên miền là tùy chọn.

## Di chuyển

Các bộ định tuyến không hỗ trợ tính năng này sẽ bỏ qua phần XML mới.

## Xem thêm

Đề xuất 130
