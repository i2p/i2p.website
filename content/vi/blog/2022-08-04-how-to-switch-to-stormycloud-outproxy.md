---
title: "Cách chuyển sang dịch vụ Outproxy của StormyCloud"
date: 2022-08-04
author: "idk"
description: "Cách chuyển sang dịch vụ Outproxy của StormyCloud"
categories: ["general"]
---

## Cách chuyển sang dịch vụ Outproxy StormyCloud

**Một Outproxy (proxy lối ra) mới, chuyên nghiệp**

Trong nhiều năm, I2P được phục vụ bởi một outproxy (proxy ra Internet) mặc định duy nhất, `false.i2p`, mà độ tin cậy đã suy giảm.
Mặc dù đã có một vài đối thủ xuất hiện để chia sẻ bớt gánh nặng, nhưng hầu hết họ không thể tình nguyện phục vụ theo mặc định cho các máy khách của toàn bộ một triển khai I2P.
Tuy nhiên, StormyCloud, một tổ chức phi lợi nhuận hoạt động chuyên nghiệp vận hành các nút thoát của Tor, đã khởi chạy một dịch vụ outproxy chuyên nghiệp mới, dịch vụ này đã được các thành viên cộng đồng I2P kiểm thử và sẽ trở thành outproxy mặc định mới trong bản phát hành sắp tới.

**StormyCloud là ai**

Theo chính lời họ, StormyCloud là:

> Sứ mệnh của StormyCloud Inc: Bảo vệ quyền truy cập Internet như một quyền con người phổ quát. Bằng cách đó, tổ chức bảo vệ quyền riêng tư điện tử của người dùng và xây dựng cộng đồng bằng cách thúc đẩy quyền tiếp cận thông tin không bị hạn chế, qua đó tạo điều kiện cho sự trao đổi tự do các ý tưởng xuyên biên giới. Điều này là thiết yếu vì Internet là công cụ mạnh mẽ nhất hiện có để tạo ra những thay đổi tích cực trên thế giới.

> Phần cứng: Chúng tôi sở hữu toàn bộ phần cứng của mình và hiện đang đặt máy chủ tại một trung tâm dữ liệu Tier 4. Hiện tại chúng tôi có đường uplink 10GBps với tùy chọn nâng cấp lên 40GBps mà không cần thay đổi nhiều. Chúng tôi có ASN và không gian địa chỉ IP riêng (IPv4 & IPv6).

Để tìm hiểu thêm về StormyCloud, hãy truy cập [trang web](https://www.stormycloud.org/) của họ.

Hoặc, hãy ghé thăm họ trên [I2P](http://stormycloud.i2p/).

**Chuyển sang StormyCloud Outproxy (máy chủ ủy nhiệm lối ra) trên I2P**

Để chuyển sang outproxy (proxy thoát) StormyCloud *ngay hôm nay* bạn có thể truy cập [Trình quản lý Dịch vụ Ẩn](http://127.0.0.1:7657/i2ptunnel/edit?tunnel=0). Khi ở đó, bạn nên đổi giá trị của **Outproxies** và **SSL Outproxies** thành `exit.stormycloud.i2p`. Sau khi hoàn tất, cuộn xuống cuối trang và nhấp vào nút "Save".

**Cảm ơn StormyCloud**

Chúng tôi xin cảm ơn StormyCloud đã tình nguyện cung cấp các dịch vụ outproxy (proxy ra ngoài) chất lượng cao cho mạng I2P.
