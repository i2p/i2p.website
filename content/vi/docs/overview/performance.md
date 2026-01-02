---
title: "Hiệu năng"
description: "Hiệu suất mạng I2P: cách hoạt động hiện nay, các cải tiến trong quá khứ, và ý tưởng điều chỉnh trong tương lai"
slug: "performance"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
reviewStatus: "needs-review"
---

## Hiệu Năng Mạng I2P: Tốc Độ, Kết Nối và Quản Lý Tài Nguyên

Mạng I2P hoàn toàn động. Mỗi client được các node khác biết đến và kiểm tra các node đã biết cục bộ về khả năng kết nối và năng lực. Chỉ những node có thể kết nối được và có đủ năng lực mới được lưu vào NetDB cục bộ. Trong quá trình xây dựng tunnel, các tài nguyên tốt nhất được chọn từ nhóm này để xây dựng tunnel. Do việc kiểm tra diễn ra liên tục, nhóm các node sẽ thay đổi. Mỗi node I2P biết một phần khác nhau của NetDB, có nghĩa là mỗi router có một tập hợp các node I2P khác nhau để sử dụng cho tunnel. Ngay cả khi hai router có cùng tập hợp con các node đã biết, các bài kiểm tra về khả năng kết nối và năng lực có thể sẽ cho kết quả khác nhau, vì các router khác có thể đang chịu tải ngay khi một router kiểm tra, nhưng lại rảnh khi router thứ hai kiểm tra.

Điều này giải thích tại sao mỗi node I2P có các node khác nhau để xây dựng tunnel. Bởi vì mỗi node I2P có độ trễ và băng thông khác nhau, các tunnel (được xây dựng thông qua những node đó) có các giá trị độ trễ và băng thông khác nhau. Và bởi vì mỗi node I2P có các tunnel được xây dựng khác nhau, không có hai node I2P nào có cùng bộ tunnel giống nhau.

Một server/client được gọi là một "destination" và mỗi destination có ít nhất một tunnel vào và một tunnel ra. Mặc định là 3 hop mỗi tunnel. Điều này tổng cộng là 12 hop (12 node I2P khác nhau) cho một hành trình khứ hồi đầy đủ client → server → client.

Mỗi gói dữ liệu được gửi qua 6 node I2P khác cho đến khi đến được máy chủ:

client - hop1 - hop2 - hop3 - hopa1 - hopa2 - hopa3 - server

và trên đường quay lại qua 6 node I2P khác nhau:

server - hopb1 - hopb2 - hopb3 - hopc1 - hopc2 - hopc3 - client

Lưu lượng trên mạng cần một ACK trước khi dữ liệu mới được gửi; nó cần đợi cho đến khi một ACK quay trở về từ máy chủ: gửi dữ liệu, đợi ACK, gửi thêm dữ liệu, đợi ACK. Khi RTT (Round Trip Time - Thời gian khứ hồi) cộng dồn từ độ trễ của từng node I2P riêng lẻ và mỗi kết nối trong hành trình khứ hồi này, thường mất 1–3 giây cho đến khi một ACK quay trở về client. Do thiết kế giao thức TCP và I2P transport, một gói dữ liệu có kích thước giới hạn. Kết hợp các điều kiện này đặt ra một giới hạn băng thông tối đa cho mỗi tunnel khoảng 20–50 kB/s. Tuy nhiên, nếu chỉ một hop trong tunnel chỉ có 5 kB/s băng thông để sử dụng, toàn bộ tunnel sẽ bị giới hạn ở 5 kB/s, độc lập với độ trễ và các giới hạn khác.

Mã hóa, độ trễ và cách một tunnel được xây dựng khiến việc tạo tunnel tốn khá nhiều thời gian CPU. Đây là lý do tại sao một destination chỉ được phép có tối đa 6 inbound tunnels và 6 outbound tunnels để truyền tải dữ liệu. Với tốc độ tối đa 50 kB/s mỗi tunnel, một destination có thể sử dụng khoảng 300 kB/s lưu lượng tổng hợp (trong thực tế có thể cao hơn nếu sử dụng các tunnel ngắn hơn với mức ẩn danh thấp hoặc không có). Các tunnel đang sử dụng sẽ bị loại bỏ sau mỗi 10 phút và những tunnel mới được xây dựng. Sự thay đổi tunnel này, cùng với việc đôi khi các client bị tắt hoặc mất kết nối với mạng, đôi khi sẽ làm hỏng các tunnel và kết nối. Một ví dụ về điều này có thể được thấy trên IRC2P Network khi mất kết nối (ping timeout) hoặc khi sử dụng eepget.

Với một tập hợp đích hạn chế và một số lượng tunnel hạn chế cho mỗi đích, một node I2P chỉ sử dụng một tập hợp tunnel hạn chế qua các node I2P khác. Ví dụ, nếu một node I2P là "hop1" trong ví dụ nhỏ ở trên, nó chỉ thấy một participating tunnel bắt nguồn từ client. Nếu chúng ta tổng hợp toàn bộ mạng I2P, chỉ có một số lượng khá hạn chế các participating tunnel có thể được xây dựng với một lượng băng thông hạn chế tổng cộng. Nếu phân bổ những con số hạn chế này trên số lượng các node I2P, chỉ có một phần nhỏ băng thông/dung lượng khả dụng có thể được sử dụng.

Để duy trì tính ẩn danh, một router không nên được sử dụng bởi toàn bộ mạng lưới để xây dựng tunnel. Nếu một router đóng vai trò là tunnel router cho tất cả các node I2P, nó sẽ trở thành một điểm thất bại trung tâm rất thực tế cũng như là một điểm tập trung để thu thập IP và dữ liệu từ các client. Đây là lý do tại sao mạng lưới phân phối lưu lượng truy cập qua các node trong quá trình xây dựng tunnel.

Một yếu tố khác cần xem xét về hiệu năng là cách I2P xử lý mesh networking. Mỗi kết nối hop-to-hop sử dụng một kết nối TCP hoặc UDP trên các I2P node. Với 1000 kết nối, ta sẽ thấy 1000 kết nối TCP. Đó là một con số khá lớn, và một số router gia đình cũng như văn phòng nhỏ chỉ cho phép một số lượng kết nối hạn chế. I2P cố gắng giới hạn các kết nối này xuống dưới 1500 cho mỗi loại UDP và TCP. Điều này cũng giới hạn lượng traffic được định tuyến qua một I2P node.

Nếu một node có thể truy cập được, có cài đặt băng thông chia sẻ >128 kB/s và hoạt động 24/7, nó sẽ được sử dụng sau một thời gian để tham gia lưu lượng. Nếu nó ngừng hoạt động trong khoảng thời gian đó, việc kiểm tra node I2P được thực hiện bởi các node khác sẽ cho họ biết rằng nó không thể truy cập được. Điều này sẽ chặn node đó trong ít nhất 24 giờ trên các node khác. Vì vậy, các node khác đã kiểm tra và thấy node đó ngừng hoạt động sẽ không sử dụng node đó trong 24 giờ để xây dựng tunnel. Đây là lý do tại sao lưu lượng của bạn thấp hơn sau khi khởi động lại/tắt router I2P của bạn trong tối thiểu 24 giờ.

Ngoài ra, các node I2P khác cần biết một I2P router để kiểm tra khả năng truy cập và năng lực của nó. Quá trình này có thể được thực hiện nhanh hơn khi bạn tương tác với mạng, ví dụ như sử dụng các ứng dụng hoặc truy cập các trang web I2P, điều này sẽ dẫn đến việc xây dựng tunnel nhiều hơn và do đó có nhiều hoạt động và khả năng truy cập hơn để các node trên mạng kiểm tra.

## Lịch sử Hiệu suất (đã chọn)

Qua nhiều năm, I2P đã chứng kiến một số cải tiến hiệu năng đáng chú ý:

### Native math

Được triển khai thông qua JNI bindings tới thư viện GNU MP (GMP) để tăng tốc `modPow` của BigInteger, trước đây chiếm phần lớn thời gian CPU. Kết quả ban đầu cho thấy tốc độ tăng đáng kể trong mã hóa khóa công khai. Xem: /misc/jbigi/

### Garlic wrapping a "reply" LeaseSet (tuned)

Trước đây, các phản hồi thường yêu cầu tra cứu LeaseSet của người gửi trong cơ sở dữ liệu mạng. Việc đính kèm LeaseSet của người gửi vào garlic ban đầu giúp cải thiện độ trễ phản hồi. Hiện tại điều này được thực hiện có chọn lọc (khi bắt đầu kết nối hoặc khi LeaseSet thay đổi) để giảm chi phí hoạt động.

### Toán học gốc

Đã di chuyển một số bước xác thực sớm hơn trong quá trình bắt tay transport để từ chối các peer xấu sớm hơn (đồng hồ sai, NAT/firewall xấu, phiên bản không tương thích), tiết kiệm CPU và băng thông.

### Garlic wrapping một "reply" LeaseSet (được điều chỉnh)

Sử dụng kiểm tra tunnel nhận biết ngữ cảnh: tránh kiểm tra các tunnel đã biết đang truyền dữ liệu; ưu tiên kiểm tra khi rảnh rỗi. Điều này giảm thiểu chi phí hoạt động và tăng tốc độ phát hiện các tunnel bị lỗi.

### Từ chối TCP hiệu quả hơn

Duy trì các lựa chọn cho một kết nối nhất định giúp giảm hiện tượng giao hàng không theo thứ tự và cho phép thư viện streaming tăng kích thước cửa sổ, cải thiện thông lượng.

### Điều chỉnh kiểm tra tunnel

GZip hoặc tương tự cho các cấu trúc dài dòng (ví dụ: tùy chọn RouterInfo) giảm băng thông khi phù hợp.

### Lựa chọn tunnel/lease cố định

Thay thế cho giao thức "ministreaming" đơn giản. Streaming hiện đại bao gồm selective ACK và kiểm soát tắc nghẽn được tùy chỉnh cho nền tảng hướng thông điệp ẩn danh của I2P. Xem: /docs/api/streaming/

## Future Performance Improvements (historical ideas)

Dưới đây là các ý tưởng được ghi chép lịch sử như những cải tiến tiềm năng. Nhiều trong số đó đã lỗi thời, đã được triển khai, hoặc đã được thay thế bởi các thay đổi kiến trúc.

### Nén các cấu trúc dữ liệu đã chọn

Cải thiện cách các router chọn peer để xây dựng tunnel nhằm tránh những peer chậm hoặc quá tải, đồng thời duy trì khả năng chống lại các cuộc tấn công Sybil từ những kẻ đối đầu có quyền lực.

### Giao thức streaming đầy đủ

Giảm việc khám phá không cần thiết khi keyspace ổn định; điều chỉnh số lượng peer được trả về trong các tra cứu và số lượng tìm kiếm đồng thời được thực hiện.

### Session Tag tuning and improvements (legacy)

Đối với cơ chế ElGamal/AES+SessionTag cũ, các chiến lược hết hạn và bổ sung thông minh hơn giúp giảm thiểu việc quay về ElGamal và lãng phí tag.

### Cải thiện việc phân tích và lựa chọn peer

Tạo các tag từ PRNG đồng bộ được khởi tạo trong quá trình thiết lập phiên mới, giảm overhead trên mỗi thông điệp so với các tag được phân phối trước.

### Điều chỉnh cơ sở dữ liệu mạng

Thời gian sống của tunnel dài hơn kết hợp với healing có thể giảm chi phí rebuild; cân bằng với tính ẩn danh và độ tin cậy.

### Điều chỉnh và cải tiến Session Tag (phiên bản cũ)

Từ chối các peer không hợp lệ sớm hơn và làm cho các bài kiểm tra tunnel nhận biết ngữ cảnh tốt hơn để giảm tranh chấp và độ trễ.

### Chuyển đổi SessionTag sang PRNG đồng bộ hóa (legacy)

Selective LeaseSet bundling, tùy chọn nén RouterInfo, và việc áp dụng giao thức streaming đầy đủ đều góp phần cải thiện hiệu năng cảm nhận được tốt hơn.

---


Xem thêm:

- [Định tuyến Tunnel](/docs/overview/tunnel-routing/)
- [Lựa chọn Peer](/docs/overview/tunnel-routing/)
- [Transports](/docs/overview/transport/)
- [Đặc tả SSU2](/docs/specs/ssu2/) và [Đặc tả NTCP2](/docs/specs/ntcp2/)
