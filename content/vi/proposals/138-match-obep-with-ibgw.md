---
title: "Ghép OBEPs với IBGWs"
number: "138"
author: "str4d"
created: "2017-04-10"
lastupdated: "2017-04-10"
status: "Open"
thread: "http://zzz.i2p/topics/2294"
toc: true
---

## Tổng quan

Đề xuất này thêm một tùy chọn I2CP cho các đường hầm đi ra ngoài, nhằm lựa chọn hoặc xây dựng các đường hầm khi một thông điệp được gửi sao cho OBEP khớp với một trong các IBGW từ LeaseSet cho Destination đích.


## Động lực

Hầu hết các router I2P sử dụng một dạng bỏ gói tin để quản lý tắc nghẽn. Triển khai tham chiếu sử dụng chiến lược WRED, tính toán cả kích thước thông điệp và khoảng cách di chuyển (xem [tài liệu tunnel throttling](/docs/specs/implementation/#tunnelthrottling)). Do chiến lược này, nguồn gốc chính của mất gói là OBEP.


## Thiết kế

Khi gửi một thông điệp, người gửi chọn hoặc xây dựng một đường hầm với một OBEP là cùng một router với một trong những IBGW của người nhận. Do đó, thông điệp sẽ đi trực tiếp từ một đường hầm ra và vào đường hầm khác, mà không cần phải gửi qua dây giữa.


## Ảnh hưởng đến bảo mật

Chế độ này có nghĩa là người nhận sẽ lựa chọn OBEP của người gửi. Để duy trì quyền riêng tư hiện tại, chế độ này sẽ khiến các đường hầm đi ra ngoài được xây dựng dài hơn một bước so với tùy chọn outbound.length I2CP (với bước cuối có thể ở ngoài tầng nhanh của người gửi).


## Đặc tả

Một tùy chọn I2CP mới được thêm vào [đặc tả I2CP](/docs/specs/i2cp/):

    outbound.matchEndWithTarget
        Boolean

        Giá trị mặc định: cụ thể từng trường hợp

        Nếu đúng, router sẽ chọn các đường hầm đi ra ngoài cho các thông điệp được gửi trong suốt phiên này sao cho OBEP của đường hầm là một trong các IBGW của Destination đích. Nếu không có đường hầm nào như vậy tồn tại, router sẽ xây dựng một đường.


## Tương thích

Tương thích ngược được đảm bảo, vì các router luôn có thể gửi thông điệp cho chính mình.


## Triển khai

### Java I2P

Xây dựng đường hầm và gửi thông điệp hiện tại là các hệ thống con riêng biệt:

- BuildExecutor chỉ biết về các tùy chọn outbound.* của nhóm đường hầm đi ra ngoài, và không có khả năng nhìn thấy về việc chúng được sử dụng.

- OutboundClientMessageOneShotJob chỉ có thể chọn một đường hầm từ nhóm hiện có; nếu một thông điệp khách hàng đến và không có đường hầm đi ra ngoài nào, router sẽ bỏ thông điệp.

Việc triển khai đề xuất này sẽ yêu cầu thiết kế một cách cho hai hệ thống con này tương tác với nhau.

### i2pd

Một triển khai thử nghiệm đã được hoàn thành.


## Hiệu suất

Đề xuất này có nhiều tác động đến độ trễ, RTT và mất gói tin:

- Có khả năng trong hầu hết các trường hợp, chế độ này sẽ yêu cầu xây dựng một đường hầm mới trên thông điệp đầu tiên thay vì sử dụng một đường hầm hiện có, tăng độ trễ.

- Đối với các đường hầm chuẩn, OBEP có thể cần tìm và kết nối với IBGW, tăng độ trễ có tác động tới RTT đầu (vì việc này xảy ra sau khi gói tin đầu tiên đã được gửi đi). Sử dụng chế độ này, OBEP sẽ cần tìm và kết nối với IBGW trong quá trình xây dựng đường hầm, thêm cùng độ trễ nhưng giảm RTT đầu (vì việc này xảy ra trước khi gói tin đầu tiên được gửi đi).

- Kích thước VariableTunnelBuild hiện tại là 2641 byte. Do đó, dự kiến chế độ này sẽ giảm thiểu mất gói cho các kích thước thông điệp trung bình lớn hơn này.

Cần thêm nhiều nghiên cứu để điều tra các ảnh hưởng này, nhằm quyết định xem những đường hầm chuẩn nào sẽ được hưởng lợi từ việc chế độ này được bật mặc định.
