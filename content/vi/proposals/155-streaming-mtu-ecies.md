---
title: "Truyền trực tuyến MTU cho Điểm đến ECIES"
number: "155"
author: "zzz"
created: "2020-05-06"
lastupdated: "2020-05-30"
status: "Đã đóng"
thread: "http://zzz.i2p/topics/2886"
target: "0.9.47"
implementedin: "0.9.47"
toc: true
---

## Lưu ý
Triển khai và thử nghiệm mạng đang tiến hành.
Có thể chỉnh sửa nhỏ.


## Tổng quan


### Tóm tắt

ECIES giảm mức tiêu thụ thông điệp phiên hiện tại (ES) khoảng 90 byte.
Do đó, chúng ta có thể tăng MTU lên khoảng 90 byte cho các kết nối ECIES.
Xem the [ECIES specification](/docs/specs/ecies/#overhead), [Streaming specification](/docs/specs/streaming/#flags-and-option-data-fields), and [Streaming API documentation](/docs/api/streaming/).

Nếu không tăng MTU, trong nhiều trường hợp tiết kiệm không thực sự 'tiết kiệm',
vì các thông điệp sẽ được đệm để sử dụng hết hai thông điệp đường hầm đầy đủ.

Đề xuất này không yêu cầu thay đổi nào với các tiêu chuẩn.
Nó được đăng như một đề xuất chỉ để thúc đẩy thảo luận và xây dựng sự đồng thuận
về giá trị đề xuất và chi tiết thực hiện.


### Mục tiêu

- Tăng MTU thương lượng
- Tối đa hóa việc sử dụng thông điệp đường hầm 1 KB
- Không thay đổi giao thức truyền trực tuyến


## Thiết kế

Sử dụng tùy chọn hiện có MAX_PACKET_SIZE_INCLUDED và thương lượng MTU.
Truyền trực tuyến tiếp tục sử dụng tối thiểu của MTU đã gửi và nhận.
Mặc định vẫn là 1730 cho tất cả các kết nối, dù sử dụng khóa nào.

Các triển khai được khuyến khích bao gồm tùy chọn MAX_PACKET_SIZE_INCLUDED trong tất cả các gói SYN, trong cả hai hướng,
mặc dù điều này không phải là yêu cầu.

Nếu điểm đến chỉ là ECIES, sử dụng giá trị cao hơn (hoặc là Alice hoặc Bob).
Nếu điểm đến có hai khóa, hành vi có thể thay đổi:

Nếu khách hàng hai khóa nằm ngoài router (trong một ứng dụng ngoài),
nó có thể không "biết" khóa đang được sử dụng ở đầu kia, và Alice có thể yêu cầu
giá trị cao hơn trong SYN, trong khi dữ liệu tối đa trong SYN vẫn là 1730.

Nếu khách hàng hai khóa nằm trong router, thông tin về khóa
đang được sử dụng có thể hoặc không được biết đến với khách hàng.
Bộ hợp đồng có thể chưa được truy xuất, hoặc các giao diện API nội bộ
có thể không dễ dàng cung cấp thông tin đó cho khách hàng.
Nếu thông tin có sẵn, Alice có thể sử dụng giá trị cao hơn;
nếu không có, Alice phải sử dụng giá trị chuẩn là 1730 cho đến khi thương lượng được.

Khách hàng hai khóa là Bob có thể gửi giá trị cao hơn làm phản hồi,
ngay cả khi không có giá trị hoặc một giá trị là 1730 được nhận từ Alice;
tuy nhiên, không có quy định cho việc thương lượng lên trong luồng,
nên MTU nên duy trì ở mức 1730.


Như đã nêu trong the [Streaming API documentation](/docs/api/streaming/),
dữ liệu trong các gói SYN được gửi từ Alice đến Bob có thể vượt quá MTU của Bob.
Đây là một điểm yếu trong giao thức truyền trực tuyến.
Do đó, khách hàng hai khóa phải giới hạn dữ liệu trong các gói SYN gửi
tới 1730 byte, trong khi gửi một tùy chọn MTU cao hơn.
Khi nhận được MTU cao hơn từ Bob, Alice có thể tăng tối đa
tải trọng thực tế được gửi.


### Phân tích

Như mô tả trong the [ECIES specification](/docs/specs/ecies/#overhead), mức tiêu thụ của ElGamal cho các thông điệp phiên hiện tại là
151 byte, và mức tiêu thụ Ratchet là 69 byte.
Do đó, chúng ta có thể tăng MTU cho các kết nối ratchet lên (151 - 69) = 82 byte,
từ 1730 lên 1812.


## Thông số kỹ thuật

Thêm các thay đổi và làm rõ sau vào phần Lựa chọn và Thương lượng MTU của the [Streaming API documentation](/docs/api/streaming/).
Không có thay đổi nào với the [Streaming specification](/docs/specs/streaming/).


Giá trị mặc định của tùy chọn i2p.streaming.maxMessageSize vẫn là 1730 cho tất cả các kết nối, dù sử dụng khóa nào.
Khách hàng phải sử dụng tối thiểu của MTU đã gửi và nhận, như thường lệ.

Có bốn hằng số và biến MTU liên quan:

- DEFAULT_MTU: 1730, không thay đổi, cho tất cả các kết nối
- i2cp.streaming.maxMessageSize: mặc định 1730 hoặc 1812, có thể được thay đổi bởi cấu hình
- ALICE_SYN_MAX_DATA: Dữ liệu tối đa mà Alice có thể bao gồm trong một gói SYN
- negotiated_mtu: Tối thiểu của MTU của Alice và Bob, được sử dụng như kích thước dữ liệu tối đa
  trong SYN ACK từ Bob đến Alice, và trong tất cả các gói gửi sau đó theo cả hai hướng


Có năm trường hợp cần xem xét:


### 1) Alice chỉ có ElGamal
Không thay đổi, MTU 1730 trong tất cả các gói.

- ALICE_SYN_MAX_DATA = 1730
- i2cp.streaming.maxMessageSize mặc định: 1730
- Alice có thể gửi MAX_PACKET_SIZE_INCLUDED trong SYN, không bắt buộc trừ khi khác 1730


### 2) Alice chỉ có ECIES
MTU 1812 trong tất cả các gói.

- ALICE_SYN_MAX_DATA = 1812
- i2cp.streaming.maxMessageSize mặc định: 1812
- Alice phải gửi MAX_PACKET_SIZE_INCLUDED trong SYN


### 3) Alice có hai khóa và biết Bob là ElGamal
MTU 1730 trong tất cả các gói.

- ALICE_SYN_MAX_DATA = 1730
- i2cp.streaming.maxMessageSize mặc định: 1812
- Alice có thể gửi MAX_PACKET_SIZE_INCLUDED trong SYN, không bắt buộc trừ khi khác 1730


### 4) Alice có hai khóa và biết Bob là ECIES
MTU 1812 trong tất cả các gói.

- ALICE_SYN_MAX_DATA = 1812
- i2cp.streaming.maxMessageSize mặc định: 1812
- Alice phải gửi MAX_PACKET_SIZE_INCLUDED trong SYN


### 5) Alice có hai khóa và khóa của Bob không rõ
Gửi 1812 dưới dạng MAX_PACKET_SIZE_INCLUDED trong gói SYN nhưng giới hạn dữ liệu gói SYN trong 1730.

- ALICE_SYN_MAX_DATA = 1730
- i2cp.streaming.maxMessageSize mặc định: 1812
- Alice phải gửi MAX_PACKET_SIZE_INCLUDED trong SYN


### Cho tất cả các trường hợp

Alice và Bob tính toán
negotiated_mtu, tối thiểu của MTU của Alice và Bob, được sử dụng như kích thước dữ liệu tối đa
trong SYN ACK từ Bob đến Alice, và trong tất cả các gói gửi sau đó theo cả hai hướng.


## Biện minh

Xem the [Java I2P source code](https://github.com/i2p/i2p.i2p/blob/master/apps/streaming/java/src/net/i2p/client/streaming/impl/ConnectionOptions.java#L220) để biết lý do tại sao giá trị hiện tại là 1730.
Xem the [ECIES specification](/docs/specs/ecies/#overhead) để biết tại sao tiêu thụ ECIES thấp hơn ElGamal là 82 byte.


## Ghi chú thực hiện

Nếu truyền trực tuyến đang tạo các thông điệp có kích thước tối ưu, thì rất quan trọng
rằng lớp ECIES-Ratchet không thêm đệm vượt quá kích thước đó.

Kích thước Garlic Message tối ưu để phù hợp với hai thông điệp đường hầm,
bao gồm tiêu đề I2NP Garlic Message dài 16 byte, Độ dài Garlic Message dài 4 byte,
thẻ ES dài 8 byte, và MAC dài 16 byte, là 1956 byte.

Một thuật toán đệm được khuyến nghị trong ECIES như sau:

- Nếu tổng chiều dài của Garlic Message từ 1954-1956 byte,
  không thêm khối đệm (không đủ không gian)
- Nếu tổng chiều dài của Garlic Message từ 1938-1953 byte,
  thêm một khối đệm để đệm chính xác 1956 byte.
- Nếu không, đệm như thường lệ, ví dụ với lượng ngẫu nhiên 0-15 byte.

Chính sách tương tự có thể được sử dụng tại kích thước tối ưu của một thông điệp đường hầm (964)
và kích thước ba thông điệp đường hầm (2952), mặc dù các kích thước này nên hiếm gặp trong thực tế.


## Vấn đề

Giá trị 1812 chỉ là sơ bộ. Cần được xác nhận và có thể điều chỉnh.


## Di cư

Không có vấn đề tương thích ngược.
Đây là một tùy chọn hiện có và thương lượng MTU đã là một phần của tiêu chuẩn.

Điểm đến ECIES cũ sẽ hỗ trợ 1730.
Bất kỳ khách hàng nào nhận được một giá trị cao hơn sẽ phản hồi với 1730, và đầu xa
sẽ thương lượng xuống, như thường lệ.


