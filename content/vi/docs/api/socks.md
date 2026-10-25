---
title: "SOCKS Proxy"
description: "Sử dụng SOCKS tunnel của I2P một cách an toàn"
slug: "socks"
aliases:
  - "/vi/socks"
  - "/vi/socks/"
lastUpdated: "2024-02"
accurateFor: "0.9.62"
---

## SOCKS và SOCKS Proxies {#overview}

SOCKS proxy đã hoạt động từ phiên bản 0.7.1. SOCKS 4/4a/5 được hỗ trợ. Kích hoạt SOCKS bằng cách tạo một tunnel client SOCKS trong i2ptunnel. Cả shared-clients và non-shared đều được hỗ trợ. Không có SOCKS outproxy nên việc sử dụng còn hạn chế.

Như đã nói trong [FAQ](/docs/overview/faq#socks):

```
Many applications leak sensitive information that could identify you on the
Internet. I2P only filters connection data, but if the program you intend to
run sends this information as content, I2P has no way to protect your anonymity.
For example, some mail applications will send the IP address of the machine
they are running on to a mail server. There is no way for I2P to filter this,
thus using I2P to 'socksify' existing applications is possible, but extremely
dangerous.
```
Và trích dẫn từ một email năm 2005:

```
... there is a reason why human and others have both built and abandoned the
SOCKS proxies. Forwarding arbitrary traffic is just plain unsafe, and it
behooves us as developers of anonymity and security software to have the safety
of our end users foremost in our minds.
```
Hy vọng rằng chúng ta có thể đơn giản gắn một client tùy ý lên trên I2P mà không cần kiểm tra cả hành vi của nó và các giao thức được tiết lộ về mặt bảo mật và ẩn danh là một suy nghĩ ngây thơ. Hầu như *mọi* ứng dụng và giao thức đều vi phạm tính ẩn danh, trừ khi chúng được thiết kế đặc biệt cho mục đích này, và ngay cả khi như vậy, hầu hết trong số đó cũng vẫn có vấn đề. Đó là thực tế. Người dùng cuối sẽ được phục vụ tốt hơn với các hệ thống được thiết kế cho tính ẩn danh và bảo mật. Việc sửa đổi các hệ thống hiện có để hoạt động trong môi trường ẩn danh không phải là một nhiệm vụ nhỏ, đòi hỏi khối lượng công việc lớn hơn hàng bậc so với việc đơn giản sử dụng các I2P API hiện có.

SOCKS proxy hỗ trợ tên sổ địa chỉ tiêu chuẩn, nhưng không hỗ trợ đích Base64. Hash Base32 sẽ hoạt động từ phiên bản 0.7. Nó chỉ hỗ trợ kết nối đi ra, tức là một I2PTunnel Client. Hỗ trợ UDP đã được tạo khung nhưng chưa hoạt động. Việc chọn outproxy theo số cổng đã được tạo khung.

## Xem Thêm {#see-also}

- Các ghi chú cho Cuộc họp 81 (16 tháng 3, 2004) và Cuộc họp 82 (23 tháng 3, 2004).
- [Onioncat](http://www.abenteuerland.at/onioncat/)

## Nếu Bạn Làm Cho Thứ Gì Đó Hoạt Động {#working}

Vui lòng cho chúng tôi biết. Và vui lòng cung cấp các cảnh báo đầy đủ về rủi ro của socks proxies.
