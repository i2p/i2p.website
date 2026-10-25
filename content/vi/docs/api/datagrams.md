---
title: "Datagram"
description: "Các định dạng thông điệp được xác thực, có thể trả lời và thô phía trên I2CP"
slug: "datagrams"
aliases:
  - "/vi/datagrams"
  - "/vi/datagrams/"
lastUpdated: "2025-04"
accurateFor: "0.9.66"
---

## Tổng quan về Datagram {#overview}

Datagram được xây dựng dựa trên [I2CP](/docs/specs/i2cp) cơ bản để cung cấp các thông điệp có thể xác thực và trả lời theo định dạng tiêu chuẩn. Điều này cho phép các ứng dụng đọc một cách đáng tin cậy địa chỉ "from" từ datagram và biết rằng địa chỉ đó thực sự đã gửi thông điệp. Điều này cần thiết cho một số ứng dụng vì thông điệp I2P cơ bản là hoàn toàn thô - nó không có địa chỉ "from" (không giống như gói IP). Ngoài ra, thông điệp và người gửi được xác thực bằng cách ký payload.

Datagram, giống như [các gói thư viện streaming](/docs/api/streaming), là một cấu trúc ở tầng ứng dụng. Các giao thức này độc lập với các [transport](/docs/overview/transport) tầng thấp; các giao thức được chuyển đổi thành các thông điệp I2NP bởi router, và bất kỳ giao thức nào cũng có thể được truyền tải bởi bất kỳ transport nào.

## Hướng dẫn Ứng dụng {#application}

Các ứng dụng được viết bằng Java có thể sử dụng datagram API, trong khi các ứng dụng bằng ngôn ngữ khác có thể sử dụng hỗ trợ datagram của [SAM](/docs/api/samv3). Cũng có hỗ trợ hạn chế trong i2ptunnel ở [SOCKS proxy](/docs/api/socks), các loại tunnel 'streamr', và các lớp udpTunnel.

### Độ dài Datagram {#length}

Nhà thiết kế ứng dụng nên cân nhắc kỹ lưỡng sự đánh đổi giữa datagram có thể trả lời và không thể trả lời. Ngoài ra, kích thước datagram sẽ ảnh hưởng đến độ tin cậy, do việc phân mảnh tunnel thành các thông điệp tunnel 1KB. Càng nhiều mảnh thông điệp thì càng có khả năng một trong số chúng sẽ bị loại bỏ bởi một hop trung gian. Không khuyến nghị các thông điệp lớn hơn vài KB. Trên khoảng 10 KB, xác suất giao hàng giảm mạnh.

[Xem trang Đặc tả Datagrams.](/docs/specs/datagrams)

Cũng cần lưu ý rằng các chi phí phụ khác nhau được thêm bởi các lớp thấp hơn, đặc biệt là garlic messages, tạo ra gánh nặng lớn cho các thông điệp không liên tục như được sử dụng bởi ứng dụng Kademlia-over-UDP. Các triển khai hiện tại được tối ưu hóa cho lưu lượng thường xuyên sử dụng thư viện streaming.

### Số Giao thức và Cổng I2CP {#protocol}

Số giao thức I2CP tiêu chuẩn cho các datagram đã ký (có thể trả lời) là PROTO_DATAGRAM (17). Các ứng dụng có thể chọn thiết lập hoặc không thiết lập giao thức trong header I2CP. Giá trị mặc định phụ thuộc vào implementation. Nó phải được thiết lập để phân tách lưu lượng datagram và streaming nhận được trên cùng một Destination.

Vì datagram không định hướng kết nối, ứng dụng có thể yêu cầu số cổng để liên kết datagram với các peer cụ thể hoặc phiên giao tiếp, như truyền thống với UDP qua IP. Các ứng dụng có thể thêm cổng 'from' và 'to' vào header I2CP (gzip) như được mô tả trong [trang I2CP](/docs/specs/i2cp#format).

Không có phương thức nào trong datagram API để chỉ định liệu nó có thể trả lời (raw) hay không thể trả lời. Ứng dụng nên được thiết kế để mong đợi loại phù hợp. Số giao thức I2CP hoặc cổng nên được ứng dụng sử dụng để chỉ ra loại datagram. Các số giao thức I2CP PROTO_DATAGRAM (có chữ ký, còn được gọi là Datagram1), PROTO_DATAGRAM_RAW, PROTO_DATAGRAM2, và PROTO_DATAGRAM3 được định nghĩa trong I2PSession API cho mục đích này. Một mẫu thiết kế phổ biến trong các ứng dụng datagram client/server là sử dụng datagram có chữ ký cho yêu cầu bao gồm một nonce, và sử dụng raw datagram cho phản hồi, trả về nonce từ yêu cầu.

**Mặc định:**

- PROTO_DATAGRAM = 17
- PROTO_DATAGRAM_RAW = 18
- PROTO_DATAGRAM2 = 19
- PROTO_DATAGRAM3 = 20

### Tính Toàn Vẹn Dữ Liệu {#integrity}

Tính toàn vẹn dữ liệu được đảm bảo bởi checksum gzip CRC-32 được triển khai trong [lớp I2CP](/docs/specs/i2cp#format). Các datagram được xác thực (Datagram1 và Datagram2) cũng đảm bảo tính toàn vẹn. Không có trường checksum trong giao thức datagram.

### Đóng gói Gói tin {#encapsulation}

Mỗi datagram được gửi qua I2P dưới dạng một thông điệp đơn lẻ (hoặc như một clove riêng lẻ trong [Garlic Message](/docs/overview/garlic-routing)). Việc đóng gói thông điệp được triển khai trong các lớp [I2CP](/docs/specs/i2cp), [I2NP](/docs/specs/i2np), và [tunnel message](/docs/specs/tunnel-message) bên dưới. Không có cơ chế phân tách gói tin hoặc trường chiều dài trong giao thức datagram.

## Đặc tả {#spec}

[Xem trang Đặc tả Datagrams.](/docs/specs/datagrams)
