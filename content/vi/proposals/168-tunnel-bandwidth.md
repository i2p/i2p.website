---
title: "Tham Số Băng Thông Tunel"
number: "168"
author: "zzz"
created: "2024-07-31"
lastupdated: "2024-12-10"
status: "Đã đóng"
thread: "http://zzz.i2p/topics/3652"
target: "0.9.65"
toc: true
---

## LƯU Ý

Đề xuất này đã được phê duyệt và hiện nằm trong
[Tunnel Creation ECIES specification](/docs/specs/implementation/#tunnel-creation-ecies) từ API 0.9.65.
Chưa có triển khai nào được biết đến; ngày triển khai / phiên bản API là TBD.


## Tổng quan

Vì chúng ta đã tăng hiệu suất của mạng trong vài năm qua
với các giao thức mới, loại mã hóa, và cải tiến kiểm soát tắc nghẽn,
các ứng dụng nhanh hơn như phát video trực tuyến trở nên khả thi.
Những ứng dụng này yêu cầu băng thông cao tại mỗi bước trong các đường hầm của khách hàng.

Các bộ định tuyến tham gia tuy nhiên không có thông tin nào về lượng
băng thông mà một đường hầm sẽ sử dụng khi họ nhận được một thông điệp xây dựng đường hầm.
Họ chỉ có thể chấp nhận hoặc từ chối một đường hầm dựa trên tổng băng thông
hiện tại được sử dụng bởi tất cả các đường hầm tham gia và giới hạn băng thông tổng thể cho các đường hầm tham gia.

Các bộ định tuyến yêu cầu cũng không có thông tin về lượng băng thông
có sẵn tại mỗi bước.

Ngoài ra, hiện tại các bộ định tuyến không có cách nào để giới hạn lưu lượng vào trên một đường hầm.
Điều này sẽ khá hữu ích trong những lúc quá tải hoặc DDoS dịch vụ.

Đề xuất này giải quyết các vấn đề này bằng cách thêm các tham số băng thông vào
các thông điệp yêu cầu và trả lời xây dựng đường hầm.


## Thiết kế

Thêm các tham số băng thông vào các bản ghi trong thông điệp xây dựng đường hầm ECIES (xem [Tunnel Creation ECIES specification](/docs/specs/implementation/#tunnel-creation-ecies))
trong trường ánh xạ tùy chọn xây dựng đường hầm. Sử dụng tên tham số ngắn vì không gian có sẵn
cho trường tùy chọn bị hạn chế.
Các thông điệp xây dựng đường hầm có kích thước cố định nên điều này không làm tăng
kích thước của các thông điệp.


## Đặc tả

Cập nhật [các đặc tả thông điệp xây dựng đường hầm ECIES](/docs/specs/implementation/#tunnel-creation-ecies)
như sau:

Đối với cả bản ghi xây dựng dài và ngắn của ECIES:

### Tùy chọn Yêu cầu Xây dựng

Ba tùy chọn sau đây có thể được đặt trong trường ánh xạ tùy chọn xây dựng đường hầm của bản ghi:
Một bộ định tuyến yêu cầu có thể bao gồm bất kỳ, tất cả, hoặc không có.

- m := băng thông tối thiểu yêu cầu cho đường hầm này (số nguyên KBps dưới dạng chuỗi)
- r := băng thông yêu cầu cho đường hầm này (số nguyên KBps dưới dạng chuỗi)
- l := giới hạn băng thông cho đường hầm này; chỉ được gửi đến IBGW (số nguyên KBps dưới dạng chuỗi)

Ràng buộc: m <= r <= l

Bộ định tuyến tham gia nên từ chối đường hầm nếu "m" được chỉ định và không thể
cung cấp ít nhất mức băng thông đó.

Tùy chọn yêu cầu được gửi cho từng người tham gia trong bản ghi yêu cầu xây dựng mã hóa tương ứng,
và không hiển thị cho những người tham gia khác.


### Tùy chọn Trả lời Xây dựng

Tùy chọn sau đây có thể được đặt trong trường ánh xạ tùy chọn trả lời xây dựng của bản ghi,
khi câu trả lời là CHẤP NHẬN:

- b := băng thông có sẵn cho đường hầm này (số nguyên KBps dưới dạng chuỗi)

Bộ định tuyến tham gia nên bao gồm điều này nếu "m" hoặc "r" đã được chỉ định
trong yêu cầu xây dựng. Giá trị nên ít nhất ngang bằng với giá trị "m" nếu được chỉ định,
nhưng có thể ít hơn hoặc nhiều hơn giá trị "r" nếu được chỉ định.

Bộ định tuyến tham gia nên cố gắng dự trữ và cung cấp ít nhất mức
băng thông này cho đường hầm, tuy nhiên điều này không phải là đảm bảo.
Bộ định tuyến không thể dự đoán các điều kiện 10 phút sau, và
lưu lượng tham gia có ưu tiên thấp hơn lưu lượng và đường hầm riêng của bộ định tuyến.

Các bộ định tuyến cũng có thể phân bổ quá mức băng thông có sẵn nếu cần thiết, và điều này
có thể là mong muốn, vì các bước khác trong đường hầm có thể từ chối nó.

Vì những lý do này, câu trả lời của bộ định tuyến tham gia nên được coi
như một cam kết nỗ lực tốt nhất, nhưng không phải là đảm bảo.

Tùy chọn trả lời được gửi đến bộ định tuyến yêu cầu trong bản ghi trả lời xây dựng mã hóa tương ứng,
và không hiển thị cho những người tham gia khác.


## Ghi chú Thực hiện

Các tham số băng thông được thấy tại các bộ định tuyến tham gia tại lớp đường hầm,
tức là số thông điệp đường hầm có kích thước cố định 1 KB mỗi giây.
Chi phí vận chuyển (NTCP2 hoặc SSU2) không được bao gồm.

Băng thông này có thể nhiều hơn hoặc ít hơn rất nhiều so với băng thông thấy tại khách hàng.
Các thông điệp đường hầm chứa một khoản chi phí đáng kể, bao gồm chi phí từ các lớp cao hơn
bao gồm ratchet và streaming. Các thông điệp nhỏ ngắt quãng như ack streaming
sẽ được mở rộng thành 1 KB mỗi cái.
Tuy nhiên, nén gzip tại lớp I2CP có thể giảm đáng kể băng thông.

Thực hiện đơn giản nhất tại bộ định tuyến yêu cầu là sử dụng
băng thông trung bình, tối thiểu, và/hoặc tối đa của các đường hầm hiện tại trong bể
để tính toán các giá trị đưa vào yêu cầu.
Các thuật toán phức tạp hơn có thể và phụ thuộc vào người thực hiện.

Hiện tại không có tùy chọn I2CP hoặc SAM nào được định nghĩa để khách hàng nói với
bộ định tuyến mức băng thông cần thiết, và không có tùy chọn mới nào được đề xuất tại đây.
Tùy chọn có thể được định nghĩa vào một ngày sau nếu cần thiết.

Thực hiện có thể sử dụng băng thông có sẵn hoặc bất kỳ dữ liệu nào khác, thuật toán, chính sách địa phương,
hoặc cấu hình địa phương để tính toán giá trị băng thông trả về trong
phản hồi xây dựng. Không được quy định bởi đề xuất này.

Đề xuất này yêu cầu các cổng đầu vào thực hiện giới hạn băng thông theo từng đường hầm nếu yêu cầu bởi tùy chọn "l".
Nó không yêu cầu các bước tham gia khác thực hiện giới hạn băng thông theo từng đường hầm hoặc toàn cầu theo bất kỳ kiểu nào, hoặc quy định một thuật toán hay triển khai cụ thể, nếu có.

Đề xuất này cũng không yêu cầu các bộ định tuyến của khách hàng giới hạn lưu lượng
theo giá trị "b" được trả về bởi bước tham gia, và tùy thuộc vào ứng dụng,
điều đó có thể không khả thi, đặc biệt là cho các đường hầm vào.

Đề xuất này chỉ ảnh hưởng đến các đường hầm được tạo bởi người khởi tạo. Không có
phương pháp nào được định nghĩa để yêu cầu hoặc phân bổ băng thông cho "far-end" tunnels được tạo
bởi chủ sở hữu của đầu kia của một kết nối từ đầu này đến đầu kia.


## Phân tích An ninh

Dấu vân tay hoặc tương quan khách hàng có thể có thể dựa trên các yêu cầu.
Bộ định tuyến (khởi tạo) của khách hàng có thể muốn ngẫu nhiên hóa các giá trị "m" và "r" thay vì gửi
giá trị giống nhau cho mỗi bước; hoặc gửi một tập hợp giá trị giới hạn đại diện cho "xô" băng thông,
hoặc một số kết hợp của cả hai.

Over-allocation DDoS: Mặc dù nó có thể là có thể DDoS một bộ định tuyến hiện nay bằng cách xây dựng và
sử dụng một số lượng lớn các đường hầm qua nó, đề xuất này chắc chắn làm cho nó dễ dàng hơn nhiều,
bằng cách chỉ cần yêu cầu một hoặc nhiều đường hầm với yêu cầu băng thông lớn.

Các bài thực hiện có thể và nên sử dụng một hoặc nhiều chiến lược sau
để giảm thiểu nguy cơ này:

- Phân bổ vượt quá băng thông có sẵn
- Giới hạn phân bổ băng thông theo từng đường hầm đến một tỷ lệ phần trăm nào đó của băng thông có sẵn
- Giới hạn tốc độ tăng băng thông được phân bổ
- Giới hạn tốc độ tăng băng thông được sử dụng
- Giới hạn băng thông phân bổ cho một đường hầm nếu không được sử dụng sớm trong vòng đời của đường hầm (sử dụng nó hoặc mất nó)
- Theo dõi băng thông trung bình theo từng đường hầm
- Theo dõi băng thông yêu cầu so với băng thông thực tế sử dụng theo từng đường hầm


## Tương thích

Không có vấn đề. Tất cả các bài thực hiện được biết hiện tại bỏ qua trường ánh xạ trong các thông điệp xây dựng,
và bỏ qua đúng một trường tùy chọn không trống.


## Di trú

Các bài thực hiện có thể thêm hỗ trợ bất kỳ lúc nào, không cần phối hợp.

Vì hiện tại chưa có phiên bản API nào được định nghĩa mà yêu cầu hỗ trợ cho đề xuất này,
các bộ định tuyến nên kiểm tra phản hồi "b" để xác nhận hỗ trợ.


