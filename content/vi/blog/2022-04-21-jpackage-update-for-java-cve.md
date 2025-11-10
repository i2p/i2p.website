---
title: "Bản cập nhật Jpackage (công cụ đóng gói ứng dụng Java) cho CVE-2022-21449 của Java"
date: 2022-04-21
author: "idk"
description: "Các gói Jpackage được phát hành với các bản vá cho lỗ hổng Java CVE-2022-21449"
categories: ["release"]
---

## Chi tiết cập nhật

Các I2P Easy-Install bundles (gói cài đặt dễ dàng) mới đã được tạo bằng phiên bản phát hành mới nhất của Máy ảo Java, trong đó bao gồm bản vá cho CVE-2022-21449 "Psychic Signatures". Khuyến nghị người dùng các easy-install bundles cập nhật càng sớm càng tốt. Người dùng OSX hiện tại sẽ nhận được cập nhật tự động; người dùng Windows nên tải trình cài đặt từ trang tải xuống của chúng tôi và chạy trình cài đặt như bình thường.

I2P router trên Linux sử dụng Máy ảo Java được cấu hình bởi hệ thống chủ. Người dùng trên các nền tảng đó nên hạ cấp xuống một phiên bản Java ổn định thấp hơn Java 14 để giảm thiểu lỗ hổng cho đến khi các bản cập nhật được phát hành bởi những người bảo trì gói. Những người dùng khác đang sử dụng JVM bên ngoài nên cập nhật JVM lên phiên bản đã được vá lỗi càng sớm càng tốt.
