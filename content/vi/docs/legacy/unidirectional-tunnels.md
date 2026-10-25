---
title: "Tunnels Một Chiều"
description: "Tóm tắt lịch sử thiết kế tunnel một chiều của I2P"
slug: "unidirectional"
aliases:
  - "/vi/unidirectional-tunnels"
  - "/vi/unidirectional-tunnels/"
lastUpdated: "2016-11"
accurateFor: "0.9.27"
---

## Tổng quan

Trang này mô tả nguồn gốc và thiết kế của các tunnel một chiều của I2P. Để biết thêm thông tin, xem:

- [Trang tổng quan tunnel](/docs/overview/tunnel-routing)
- [Thông số kỹ thuật tunnel](/docs/specs/tunnel-implementation)
- [Thông số kỹ thuật tạo tunnel](/docs/specs/tunnel-creation)
- [Thảo luận thiết kế tunnel](/docs/discussions/tunnel)
- [Lựa chọn peer](/docs/overview/peer-selection)

## Đánh giá

Mặc dù chúng tôi không biết về bất kỳ nghiên cứu nào được công bố về những lợi ích của tunnel một chiều, chúng dường như khiến việc phát hiện mô hình yêu cầu/phản hồi trở nên khó khăn hơn, điều mà hoàn toàn có thể phát hiện được qua tunnel hai chiều. Một số ứng dụng và giao thức, đặc biệt là HTTP, thực sự truyền dữ liệu theo cách như vậy. Việc để lưu lượng đi theo cùng một tuyến đường đến đích và quay lại có thể khiến kẻ tấn công chỉ có dữ liệu về thời gian và khối lượng lưu lượng dễ dàng suy luận đường đi mà tunnel đang sử dụng. Việc phản hồi quay về theo một đường khác có thể nói là khiến điều này trở nên khó khăn hơn.

Khi đối phó với kẻ thù nội bộ hoặc hầu hết các kẻ thù bên ngoài, các tunnel một chiều của I2P chỉ để lộ một nửa lượng dữ liệu lưu lượng so với việc sử dụng các mạch hai chiều chỉ bằng cách quan sát các luồng dữ liệu - một yêu cầu và phản hồi HTTP sẽ đi theo cùng một đường dẫn trong Tor, trong khi ở I2P các gói tin tạo nên yêu cầu sẽ đi ra thông qua một hoặc nhiều outbound tunnel và các gói tin tạo nên phản hồi sẽ quay trở lại thông qua một hoặc nhiều inbound tunnel khác nhau.

Chiến lược sử dụng hai tunnel riêng biệt cho giao tiếp inbound và outbound không phải là kỹ thuật duy nhất có sẵn, và nó có những tác động đến tính ẩn danh. Về mặt tích cực, bằng cách sử dụng các tunnel riêng biệt, nó giảm thiểu dữ liệu lưu lượng bị lộ để phân tích cho những người tham gia trong một tunnel - ví dụ, các peer trong một outbound tunnel từ trình duyệt web chỉ thấy lưu lượng của một HTTP GET, trong khi các peer trong inbound tunnel sẽ thấy payload được truyền dọc theo tunnel. Với các tunnel hai chiều, tất cả người tham gia sẽ có quyền truy cập vào thông tin rằng ví dụ như 1KB được gửi theo một hướng, sau đó 100KB theo hướng khác. Về mặt tiêu cực, việc sử dụng các tunnel đơn hướng có nghĩa là có hai tập hợp peer cần được phân tích và tính toán, và cần phải thận trọng thêm để giải quyết tốc độ gia tăng của các cuộc tấn công predecessor. Quá trình pooling và xây dựng tunnel (các chiến lược lựa chọn và sắp xếp peer) nên giảm thiểu những lo ngại về cuộc tấn công predecessor.

## Tính ẩn danh

Một [bài báo của Hermann và Grothoff](http://grothoff.org/christian/i2p.pdf) tuyên bố rằng các tunnel một chiều của I2P "có vẻ là một quyết định thiết kế tồi".

Điểm chính của bài báo là việc khử ẩn danh trên tunnel một chiều mất nhiều thời gian hơn, đây là một lợi thế, nhưng kẻ tấn công có thể chắc chắn hơn trong trường hợp một chiều. Do đó, bài báo khẳng định điều này không phải là lợi thế mà là bất lợi, ít nhất là với các I2P Site tồn tại lâu dài.

Kết luận này không được hỗ trợ đầy đủ bởi bài báo. Các tunnel một chiều rõ ràng giảm thiểu các cuộc tấn công khác và không rõ ràng làm thế nào để cân bằng rủi ro của cuộc tấn công trong bài báo với các cuộc tấn công trên kiến trúc tunnel hai chiều.

Kết luận này dựa trên một sự cân bằng tùy ý giữa độ chắc chắn và thời gian có thể không áp dụng được trong mọi trường hợp. Ví dụ, ai đó có thể tạo danh sách các IP có thể rồi ban hành lệnh triệu tập cho từng IP. Hoặc kẻ tấn công có thể DDoS từng IP một cách lần lượt và thông qua một cuộc tấn công giao thoa đơn giản để xem liệu I2P Site có bị ngừng hoạt động hay bị chậm lại không. Vậy nên gần đúng có thể là đủ tốt, hoặc thời gian có thể quan trọng hơn.

Kết luận này dựa trên việc cân nhắc cụ thể về tầm quan trọng giữa tính chắc chắn và thời gian, và việc cân nhắc đó có thể sai, và chắc chắn có thể tranh luận, đặc biệt là trong thế giới thực với trát đòi hầu tòa, lệnh khám xét và các phương pháp khác có sẵn để xác nhận cuối cùng.

Một phân tích đầy đủ về các đánh đổi giữa tunnel một chiều và hai chiều rõ ràng nằm ngoài phạm vi của bài báo này, và cũng chưa được thực hiện ở nơi nào khác. Ví dụ, cuộc tấn công này so sánh như thế nào với nhiều cuộc tấn công timing có thể xảy ra đã được công bố về các mạng onion-routed? Rõ ràng là các tác giả chưa thực hiện phân tích đó, nếu việc thực hiện một cách hiệu quả có thể.

Tor sử dụng các tunnel hai chiều và đã được nghiên cứu học thuật rất nhiều. I2P sử dụng các tunnel một chiều và đã được nghiên cứu rất ít. Việc thiếu một bài báo nghiên cứu bảo vệ cho tunnel một chiều có nghĩa là đây là một lựa chọn thiết kế kém, hay chỉ là nó cần được nghiên cứu thêm? Các cuộc tấn công timing và tấn công phân tán rất khó phòng thủ trong cả I2P và Tor. Ý định thiết kế (xem tài liệu tham khảo ở trên) là tunnel một chiều có khả năng chống lại các cuộc tấn công timing tốt hơn. Tuy nhiên, bài báo trình bày một loại tấn công timing khác. Liệu cuộc tấn công này, dù sáng tạo, có đủ để gán nhãn kiến trúc tunnel của I2P (và do đó I2P nói chung) là "thiết kế tồi", và ngụ ý rằng nó rõ ràng kém hơn Tor, hay nó chỉ là một lựa chọn thiết kế khác rõ ràng cần thêm điều tra và phân tích? Có một số lý do khác để coi I2P hiện tại kém hơn Tor và các dự án khác (quy mô mạng nhỏ, thiếu tài trợ, thiếu đánh giá) nhưng liệu tunnel một chiều thực sự là một lý do?

Tóm lại, "quyết định thiết kế tồi" rõ ràng là (vì bài báo không gọi tunnel hai chiều là "tồi") cách viết tắt của "tunnel một chiều hoàn toàn kém hơn tunnel hai chiều", nhưng kết luận này không được bài báo hỗ trợ.
