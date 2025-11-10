---
title: "I2P trên Maven Central"
date: 2016-06-13
author: "str4d"
description: "Các thư viện phía máy khách của I2P hiện đã có trên Maven Central!"
categories: ["summer-dev"]
---

Chúng ta đã gần đi được nửa chặng đường của tháng dành cho API trong Summer Dev, và đang đạt được những tiến bộ đáng kể trên nhiều phương diện. Tôi vui mừng thông báo rằng điều đầu tiên trong số này đã hoàn tất: các thư viện client của I2P hiện đã có trên Maven Central!

Điều này sẽ giúp các nhà phát triển Java sử dụng I2P trong các ứng dụng của họ trở nên đơn giản hơn nhiều. Thay vì phải lấy các thư viện từ một bản cài đặt hiện có, họ chỉ cần thêm I2P vào danh sách phụ thuộc của mình. Tương tự, việc nâng cấp lên các phiên bản mới sẽ dễ dàng hơn nhiều.

## Cách sử dụng chúng

Có hai thư viện mà bạn cần biết:

- `net.i2p:i2p` - The core I2P APIs; you can use these to send individual datagrams.
- `net.i2p.client:streaming` - A TCP-like set of sockets for communicating over I2P.

Thêm một hoặc cả hai mục này vào các phụ thuộc của dự án của bạn, và bạn đã sẵn sàng!

### Gradle

```
compile 'net.i2p:i2p:0.9.26'
compile 'net.i2p.client:streaming:0.9.26'
```
### Gradle

```xml
<dependency>
    <groupId>net.i2p</groupId>
    <artifactId>i2p</artifactId>
    <version>0.9.26</version>
</dependency>
<dependency>
    <groupId>net.i2p.client</groupId>
    <artifactId>streaming</artifactId>
    <version>0.9.26</version>
</dependency>
```
Đối với các hệ thống build khác, hãy xem các trang trên Maven Central cho các thư viện core và streaming.

Các nhà phát triển Android nên sử dụng I2P Android client library, thư viện này chứa các thư viện giống hệt cùng với các tiện ích hỗ trợ dành riêng cho Android. Tôi sẽ sớm cập nhật nó để phụ thuộc vào các thư viện I2P mới, để các ứng dụng đa nền tảng có thể hoạt động trực tiếp với I2P Android hoặc I2P trên máy tính để bàn.

## Get hacking!

Xem hướng dẫn phát triển ứng dụng của chúng tôi để được hỗ trợ bắt đầu với các thư viện này. Bạn cũng có thể trò chuyện với chúng tôi về chúng tại kênh #i2p-dev trên IRC. Và nếu bạn bắt đầu sử dụng chúng, hãy cho chúng tôi biết bạn đang thực hiện điều gì với hashtag #I2PSummer trên Twitter!
