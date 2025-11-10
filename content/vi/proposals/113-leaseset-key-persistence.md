---
title: "Tính bền vững của khóa LeaseSet"
number: "113"
author: "zzz"
created: "2014-12-13"
lastupdated: "2016-12-02"
status: "Đã đóng"
thread: "http://zzz.i2p/topics/1770"
target: "0.9.18"
implementedin: "0.9.18"
---

## Tổng quan

Đề xuất này nhằm duy trì dữ liệu bổ sung trong LeaseSet hiện đang là thoáng qua.
Đã được triển khai trong phiên bản 0.9.18.

## Động lực

Trong phiên bản 0.9.17 đã thêm chức năng lưu trữ lâu dài cho khóa phân cắt netDb, được lưu trữ trong
i2ptunnel.config. Điều này giúp ngăn chặn một số cuộc tấn công bằng cách giữ nguyên phân cắt
sau khi khởi động lại, và cũng ngăn ngừa sự tương quan có thể với việc khởi động lại router.

Có hai điều khác thậm chí dễ dàng hơn để tương quan với việc khởi động lại router:
đó là khóa mã hóa và ký tên của leaseset. Chúng hiện tại chưa được lưu trữ lâu dài.

## Các thay đổi được đề xuất

Khóa riêng tư được lưu trữ trong i2ptunnel.config, như i2cp.leaseSetPrivateKey và i2cp.leaseSetSigningPrivateKey.
