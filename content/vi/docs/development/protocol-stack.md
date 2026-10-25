---
title: "Ngăn xếp Giao thức"
description: "Tổng quan về các tầng giao thức I2P protocol stack"
slug: "protocol-stack"
lastUpdated: "2024-01"
accurateFor: "0.9.61"
aliases:
  - "/vi/docs/develop/protocol-stack"
  - "/vi/docs/develop/protocol-stack/"
  - "/vi/protocols"
  - "/vi/protocols/"
---

Stack I2P là một thiết kế phân lớp cho phép giao tiếp ẩn danh. Mỗi lớp bổ sung các khả năng cụ thể trên các lớp bên dưới. Xem [Chỉ mục Tài liệu Kỹ thuật](/docs/develop/overview) để biết thêm chi tiết về từng thành phần.

## Lớp Internet {#internet}

**IP** - Internet Protocol cho phép định địa chỉ các máy chủ trên internet thông thường và định tuyến các gói tin qua internet sử dụng phương thức giao hàng tối ưu.

## Lớp Vận Chuyển {#transport}

- **TCP** - Transmission Control Protocol cho phép truyền tải gói tin đáng tin cậy và theo thứ tự
- **UDP** - User Datagram Protocol cho phép truyền tải gói tin không đáng tin cậy và không theo thứ tự

## Lớp Vận chuyển I2P {#i2p-transport}

Kết nối được mã hóa giữa các router (chưa ẩn danh):

- **[NTCP2](/docs/specs/ntcp2)** - Giao thức truyền tải TCP dựa trên NIO
- **[SSU2](/docs/specs/ssu2)** - Giao thức truyền tải UDP bán tin cậy bảo mật

## Lớp Tunnel I2P {#tunnels}

Cung cấp các kết nối tunnel mã hóa ẩn danh hoàn toàn:

- **[Tunnel messages](/docs/legacy/tunnel-message)** - Các I2NP messages được mã hóa và các
  hướng dẫn được mã hóa để giao hàng chúng
- **[I2NP messages](/docs/specs/i2np)** - Các protocol messages với mã hóa nhiều lớp cho
  việc định tuyến ẩn danh đa hop

## I2P Garlic Layer {#garlic}

Cung cấp việc gửi tin nhắn I2P mã hóa và ẩn danh từ đầu đến cuối:

- **[Garlic messages](/docs/overview/garlic-routing)** - Các thông điệp I2NP được đóng gói để giao hàng ẩn danh

## Lớp Client I2P {#client}

- **[I2CP](/docs/specs/i2cp)** - I2P Control Protocol cho phép các ứng dụng truy cập
  mạng I2P mà không cần sử dụng trực tiếp API của router

## Lớp Vận Chuyển Đầu Cuối đến Đầu Cuối I2P {#e2e-transport}

- **[Streaming Library](/docs/api/streaming)** - Cung cấp khả năng truyền tải đáng tin cậy, theo thứ tự tương tự như TCP
- **[Datagram Library](/docs/api/datagrams)** - Cung cấp khả năng truyền tải không đáng tin cậy tương tự như UDP

## Lớp Giao Diện Ứng Dụng I2P {#app-interface}

Các giao diện tùy chọn cho nhà phát triển ứng dụng:

- **[I2PTunnel](/docs/api/i2ptunnel)** - Tạo tunnel cho các kết nối TCP vào và ra khỏi I2P
- **[SAMv3](/docs/api/samv3)** - Giao thức Simple Anonymous Messaging cho các ứng dụng không phải Java

## Lớp Proxy Ứng dụng I2P {#app-proxy}

Proxy cho các giao thức internet tiêu chuẩn:

- **HTTP** - Proxy duyệt web
- **IRC** - Proxy Internet Relay Chat
- **[SOCKS](/docs/api/socks)** - Proxy SOCKS4/4a/5
- **Streamr** - Proxy streaming UDP

## Ứng dụng {#applications}

Các ứng dụng có thể giao tiếp với I2P ở nhiều tầng khác nhau:

**Ứng dụng Streaming/Datagram:** - Các ứng dụng I2P gốc sử dụng trực tiếp thư viện streaming hoặc datagram

**Ứng dụng SAM:** - Các ứng dụng bằng bất kỳ ngôn ngữ nào sử dụng giao thức SAM

**Ứng dụng chuyên dụng cho I2P:** - Các ứng dụng được thiết kế riêng cho I2P (I2PSnark, SusiMail, v.v.)

**Ứng dụng Internet tiêu chuẩn:** - Các ứng dụng thông thường sử dụng proxy I2P (trình duyệt web, client IRC, v.v.)

## Sơ đồ Stack {#diagram}

![Ngăn xếp giao thức I2P](/images/protocol_stack.png)

Lưu ý: SAM có thể sử dụng cả thư viện streaming và datagram.
