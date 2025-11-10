---
title: "I2P Jpackages nhận bản cập nhật đầu tiên"
date: 2021-11-02
author: "idk"
description: "Các gói phần mềm mới, dễ cài đặt hơn đạt một cột mốc mới"
categories: ["general"]
---

Vài tháng trước, chúng tôi đã phát hành các gói mới với kỳ vọng sẽ giúp nhiều người mới tham gia mạng I2P bằng cách làm cho việc cài đặt và cấu hình I2P trở nên dễ dàng hơn cho nhiều người. Chúng tôi đã lược bỏ hàng chục bước khỏi quy trình cài đặt bằng cách chuyển từ một JVM bên ngoài sang một Jpackage, xây dựng các gói chuẩn cho các hệ điều hành mục tiêu, và ký chúng theo cách mà hệ điều hành có thể nhận diện để giữ an toàn cho người dùng. Kể từ đó, các router jpackage đã đạt một cột mốc mới, chúng sắp nhận được các bản cập nhật gia tăng đầu tiên của mình. Những bản cập nhật này sẽ thay thế jpackage JDK 16 bằng jpackage JDK 17 đã được cập nhật và cung cấp các bản sửa cho một số lỗi nhỏ mà chúng tôi phát hiện sau khi phát hành.

## Các cập nhật chung cho Mac OS và Windows

Tất cả các trình cài đặt I2P dạng jpackaged nhận được các bản cập nhật sau:

* Update the jpackaged I2P router to 1.5.1 which is built with JDK 17

Vui lòng cập nhật càng sớm càng tốt.

## Cập nhật Jpackage cho I2P trên Windows

Các gói dành riêng cho Windows nhận được các bản cập nhật sau:

* Updates I2P in Private Browsing, NoScript browser extensions
* Begins to phase out HTTPS everywhere on new Firefox releases
* Updates launcher script to fix post NSIS launch issue on some architectures

Để xem danh sách đầy đủ các thay đổi, hãy xem changelog.txt trong i2p.firefox

## Các bản cập nhật Jpackage cho I2P trên Mac OS

Các gói chỉ dành cho Mac OS nhận được các cập nhật sau:

* No Mac-Specific changes. Mac OS is updated to build with JDK 17.

Để có tóm tắt về quá trình phát triển, hãy xem các check-ins (các lần cập nhật mã) trong i2p-jpackage-mac
