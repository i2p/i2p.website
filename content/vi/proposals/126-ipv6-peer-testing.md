---
title: "Kiểm Tra Đồng Đẳng IPv6"
number: "126"
author: "zzz"
created: "2016-05-02"
lastupdated: "2018-03-19"
status: "Đã Đóng"
thread: "http://zzz.i2p/topics/2119"
target: "0.9.27"
implementedin: "0.9.27"
---

## Tổng Quan

Đề xuất này nhằm thực hiện Kiểm Tra Đồng Đẳng SSU cho IPv6.
Đã được triển khai trong 0.9.27.


## Động Lực

Chúng ta không thể xác định và theo dõi đáng tin cậy nếu địa chỉ IPv6 của chúng ta bị tường lửa chặn.

Khi chúng ta thêm hỗ trợ IPv6 nhiều năm trước, chúng ta đã giả định rằng IPv6 không bao giờ bị tường lửa chặn.

Gần đây hơn, trong 0.9.20 (Tháng 5 năm 2015), chúng ta đã phân chia trạng thái khả năng truy cập v4/v6 nội bộ (vé #1458).
Xem vé đó để biết thông tin chi tiết và các liên kết.

Nếu bạn có cả v4 và v6 bị tường lửa chặn, bạn có thể chỉ cần ép buộc bị chặn trong phần cấu hình TCP trên /confignet.

Chúng ta không có kiểm tra đồng đẳng cho v6. Nó bị cấm trong quy chuẩn SSU.
Nếu chúng ta không thể thường xuyên kiểm tra khả năng truy cập v6, chúng ta không thể chuyển tiếp/trở lại trạng thái có thể truy cập v6 một cách hợp lý.
Cái còn lại là đoán rằng chúng ta có thể truy cập nếu chúng ta nhận được một kết nối vào,
và đoán rằng chúng ta không thể nếu chúng ta chưa nhận được kết nối vào trong một thời gian.
Vấn đề là khi bạn tuyên bố không thể truy cập, bạn không xuất bản IP v6 của bạn,
và sau đó bạn sẽ không nhận được thêm kết nối nào nữa (sau khi RI hết hạn trong netdb của mọi người).


## Thiết Kế

Thực hiện Kiểm Tra Đồng Đẳng cho IPv6,
bằng cách loại bỏ hạn chế trước đó rằng kiểm tra đồng đẳng chỉ được phép cho IPv4.
Thông điệp kiểm tra đồng đẳng đã có trường cho độ dài IP.


## Đặc Tả

Trong phần Khả Năng của tổng quan SSU, thực hiện bổ sung sau:

Từ 0.9.26, kiểm tra đồng đẳng không được hỗ trợ cho các địa chỉ IPv6, và
khả năng 'B', nếu có đối với địa chỉ IPv6, phải bị bỏ qua.
Từ 0.9.27, kiểm tra đồng đẳng được hỗ trợ cho các địa chỉ IPv6, và
sự có mặt hoặc không có mặt của khả năng 'B' trong địa chỉ IPv6
chỉ ra sự hỗ trợ thực tế (hoặc không có sự hỗ trợ).


Trong các phần Kiểm Tra Đồng Đẳng của tổng quan SSU và đặc tả SSU, thực hiện các thay đổi sau:

Ghi Chú IPv6:
Thông qua bản phát hành 0.9.26, chỉ hỗ trợ kiểm tra các địa chỉ IPv4.
Do đó, tất cả giao tiếp Alice-Bob và Alice-Charlie phải thông qua IPv4.
Tuy nhiên, giao tiếp Bob-Charlie có thể thông qua IPv4 hoặc IPv6.
Địa chỉ của Alice, khi được chỉ định trong thông điệp PeerTest, phải là 4 byte.
Kể từ bản phát hành 0.9.27, hỗ trợ kiểm tra các địa chỉ IPv6, và giao tiếp Alice-Bob và Alice-Charlie có thể thông qua IPv6,
nếu Bob và Charlie chỉ định hỗ trợ với một khả năng 'B' trong địa chỉ IPv6 công bố của họ.

Alice gửi yêu cầu tới Bob bằng một phiên hiện có qua phương tiện vận chuyển (IPv4 hoặc IPv6) mà cô ấy muốn kiểm tra.
Khi Bob nhận được yêu cầu từ Alice thông qua IPv4, Bob phải chọn một Charlie quảng cáo một địa chỉ IPv4.
Khi Bob nhận được một yêu cầu từ Alice thông qua IPv6, Bob phải chọn một Charlie quảng cáo một địa chỉ IPv6.
Giao tiếp thực tế giữa Bob-Charlie có thể qua IPv4 hoặc IPv6 (tức là độc lập với loại địa chỉ của Alice).


## Di Chuyển

Các bộ định tuyến có thể:

1) Không tăng phiên bản của họ lên 0.9.27 hoặc cao hơn

2) Loại bỏ khả năng 'B' khỏi bất kỳ địa chỉ SSU IPv6 nào đã công bố

3) Thực hiện kiểm tra đồng đẳng IPv6
