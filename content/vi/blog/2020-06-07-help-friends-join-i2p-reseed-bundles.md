---
title: "Giúp bạn bè tham gia I2P bằng cách chia sẻ các gói reseed"
date: 2020-06-07
author: "idk"
description: "Tạo, trao đổi và sử dụng reseed bundles (gói khởi tạo mạng)"
categories: ["reseed"]
---

Hầu hết I2P router mới tham gia mạng bằng cách bootstrap (khởi tạo ban đầu) với sự trợ giúp của một dịch vụ reseed. Tuy nhiên, các dịch vụ reseed là dạng tập trung và tương đối dễ bị chặn, trong khi phần còn lại của mạng I2P nhấn mạnh vào các kết nối phi tập trung và không thể bị chặn. Nếu một I2P router mới không thể bootstrap, có thể sử dụng một I2P router hiện có để tạo một “Reseed bundle” hoạt động và bootstrap mà không cần đến dịch vụ reseed.

Người dùng có kết nối I2P đang hoạt động có thể giúp một router bị chặn tham gia vào mạng bằng cách tạo một tệp reseed (khởi tạo ban đầu) và chuyển cho họ qua một kênh bí mật hoặc không bị chặn. Thực tế, trong nhiều trường hợp, một I2P router đã kết nối sẽ không bị ảnh hưởng bởi việc chặn reseed, vì vậy **việc có các I2P router đang hoạt động đồng nghĩa với việc các I2P router hiện có có thể giúp các I2P router mới bằng cách cung cấp cho họ một cách khởi động ban đầu ẩn**.

## Tạo gói Reseed

- To create a reseed bundle for others to use, go to the [Reseed configuration page](http://127.0.0.1:7657/configreseed). You will see a section that looks like this. Click the button indicated by the red circle to create a reseed zip.
- Now that you've clicked the button, a zip will be generated containing enough information to bootstrap a new I2P router. Download it and transfer it to the computer with the new, un-bootstrapped I2P router.

## Thực hiện Reseed từ tệp

- Obtain an i2preseed.zip file from a friend with an I2P router that is already running, or from a trusted source somewhere on the internet, and visit the [Reseed Configuration page](http://127.0.0.1:7657/configreseed). Click the button that says "Select zip or su3 file" and navigate to that file.
- When you've selected your reseed file, click the "Reseed from File" button. You're done! Your router will now bootstrap using the zip file, and you will be ready to join the I2P network.
