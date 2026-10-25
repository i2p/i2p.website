---
title: "Thảo luận về Tunnel"
description: "Khám phá lịch sử về chiến lược padding tunnel, phân mảnh và xây dựng"
slug: "tunnel"
aliases:
  - "/vi/docs/discussions/tunnel"
  - "/vi/docs/discussions/tunnel/"
  - "/vi/tunnel_discussion"
  - "/vi/tunnel_discussion/"
lastUpdated: "2019-07"
accurateFor: "0.9.41"
---

Lưu ý: Tài liệu này chứa thông tin cũ về các phương án thay thế cho việc triển khai tunnel hiện tại trong I2P, và các suy đoán về khả năng trong tương lai. Để có thông tin hiện tại, hãy xem [trang tunnel](/docs/specs/tunnel-implementation).

Trang đó ghi lại việc triển khai xây dựng tunnel hiện tại tính đến phiên bản 0.6.1.10. Phương pháp xây dựng tunnel cũ, được sử dụng trước phiên bản 0.6.1.10, được ghi lại trên [trang tunnel cũ](/docs/historical/tunnel-alt).

### Các Phương Án Cấu Hình {#config}

Ngoài độ dài của chúng, có thể có các tham số có thể cấu hình bổ sung cho mỗi tunnel có thể được sử dụng, chẳng hạn như giới hạn tần suất của các thông điệp được gửi, cách sử dụng padding, thời gian một tunnel nên hoạt động, có nên chèn các thông điệp chaff hay không, và các chiến lược batching nào, nếu có, nên được sử dụng. Hiện tại không có tính năng nào trong số này được triển khai.

### Các Phương Án Đệm {#tunnel.padding}

Có thể áp dụng nhiều chiến lược đệm tunnel khác nhau, mỗi chiến lược đều có ưu điểm riêng:

- Không có padding
- Padding đến kích thước ngẫu nhiên
- Padding đến kích thước cố định
- Padding đến KB gần nhất
- Padding đến kích thước lũy thừa gần nhất (2^n bytes)

Các chiến lược padding này có thể được sử dụng ở nhiều cấp độ khác nhau, giải quyết vấn đề tiết lộ thông tin kích thước tin nhắn cho các đối thủ khác nhau. Sau khi thu thập và xem xét một số thống kê từ mạng 0.4, cũng như khám phá các đánh đổi về tính ẩn danh, chúng tôi bắt đầu với kích thước tin nhắn tunnel cố định là 1024 byte. Tuy nhiên, trong phạm vi này, bản thân các tin nhắn được phân mảnh không được padding bởi tunnel (mặc dù đối với các tin nhắn end-to-end, chúng có thể được padding như một phần của garlic wrapping).

### Các Phương Án Thay Thế Phân Mảnh {#tunnel.fragmentation}

Để ngăn chặn kẻ thù đánh dấu các thông điệp dọc theo đường dẫn bằng cách điều chỉnh kích thước thông điệp, tất cả các thông điệp tunnel đều có kích thước cố định là 1024 bytes. Để chứa các thông điệp I2NP lớn hơn cũng như hỗ trợ những thông điệp nhỏ hơn một cách hiệu quả hơn, gateway sẽ chia các thông điệp I2NP lớn hơn thành các mảnh được chứa trong mỗi thông điệp tunnel. Endpoint sẽ cố gắng tái tạo thông điệp I2NP từ các mảnh trong một khoảng thời gian ngắn, nhưng sẽ loại bỏ chúng khi cần thiết.

Các router có nhiều quyền tự do trong việc sắp xếp các fragment, liệu chúng có được nhồi nhét một cách không hiệu quả như các đơn vị rời rạc, được gom lại trong một khoảng thời gian ngắn để chứa nhiều payload hơn vào các tunnel message 1024 byte, hay được đệm một cách cơ hội với các message khác mà gateway muốn gửi đi.

### Thêm Các Lựa Chọn Khác {#tunnel.alternatives}

#### Điều Chỉnh Xử Lý Tunnel Giữa Chừng {#tunnel.reroute}

Trong khi thuật toán định tuyến tunnel đơn giản sẽ đủ cho hầu hết các trường hợp, có ba phương án thay thế có thể được khám phá:

- Có một peer khác endpoint tạm thời đóng vai trò là điểm kết thúc cho một tunnel bằng cách điều chỉnh mã hóa được sử dụng tại gateway để cung cấp cho họ bản rõ của các I2NP message đã được xử lý trước. Mỗi peer có thể kiểm tra xem họ có bản rõ hay không, xử lý message khi nhận được như thể họ có.
- Cho phép các router tham gia trong tunnel trộn lại message trước khi chuyển tiếp - đẩy nó qua một trong những outbound tunnel của chính peer đó, mang theo hướng dẫn để giao đến hop tiếp theo.
- Triển khai code cho tunnel creator để định nghĩa lại "next hop" của peer trong tunnel, cho phép chuyển hướng động thêm.

#### Sử dụng Tunnel Hai Chiều {#tunnel.bidirectional}

Chiến lược hiện tại sử dụng hai tunnel riêng biệt cho giao tiếp đến và đi không phải là kỹ thuật duy nhất có sẵn, và nó có những tác động đến tính ẩn danh. Về mặt tích cực, bằng cách sử dụng các tunnel riêng biệt, nó giảm thiểu dữ liệu lưu lượng bị lộ để phân tích cho những người tham gia trong tunnel - ví dụ, các peer trong tunnel đi từ trình duyệt web chỉ thấy lưu lượng của HTTP GET, trong khi các peer trong tunnel đến sẽ thấy tải trọng được chuyển qua tunnel. Với các tunnel hai chiều, tất cả người tham gia sẽ có quyền truy cập vào thông tin rằng ví dụ 1KB được gửi theo một hướng, sau đó 100KB theo hướng khác. Về mặt tiêu cực, việc sử dụng tunnel một chiều có nghĩa là có hai tập hợp peer cần được phân tích và tính toán, và cần chú ý thêm để giải quyết tốc độ gia tăng của các cuộc tấn công predecessor. Quá trình gộp tunnel và xây dựng được nêu dưới đây sẽ giảm thiểu lo ngại về cuộc tấn công predecessor, mặc dù nếu muốn, việc xây dựng cả tunnel đến và đi dọc theo cùng các peer sẽ không gặp nhiều khó khăn.

#### Giao tiếp Backchannel {#tunnel.backchannel}

Hiện tại, các giá trị IV được sử dụng là những giá trị ngẫu nhiên. Tuy nhiên, có thể sử dụng giá trị 16 byte đó để gửi thông điệp điều khiển từ gateway đến endpoint, hoặc trên các tunnel đi ra, từ gateway đến bất kỳ peer nào. Gateway đến có thể mã hóa một số giá trị nhất định trong IV một lần, mà endpoint có thể khôi phục được (vì nó biết endpoint cũng là người tạo). Đối với các tunnel đi ra, người tạo có thể chuyển giao một số giá trị nhất định cho các thành viên tham gia trong quá trình tạo tunnel (ví dụ: "nếu bạn thấy 0x0 làm IV, có nghĩa là X", "0x1 có nghĩa là Y", v.v.). Vì gateway trên tunnel đi ra cũng là người tạo, họ có thể xây dựng một IV sao cho bất kỳ peer nào cũng sẽ nhận được giá trị chính xác. Người tạo tunnel thậm chí có thể cung cấp cho gateway của tunnel đến một chuỗi các giá trị IV mà gateway đó có thể sử dụng để giao tiếp với từng thành viên tham gia chính xác một lần (mặc dù điều này sẽ có vấn đề liên quan đến việc phát hiện thông đồng).

Kỹ thuật này có thể được sử dụng sau này để gửi thông điệp giữa luồng dữ liệu, hoặc để cho phép gateway đầu vào thông báo với endpoint rằng nó đang bị tấn công DoS hoặc sắp gặp sự cố. Hiện tại, chưa có kế hoạch nào để khai thác backchannel này.

#### Thông điệp Tunnel Kích thước Biến đổi {#tunnel.variablesize}

Mặc dù lớp vận chuyển có thể có kích thước thông điệp cố định hoặc biến đổi riêng của nó, sử dụng phân mảnh riêng, nhưng lớp tunnel thay vào đó có thể sử dụng các thông điệp tunnel có kích thước biến đổi. Sự khác biệt này là một vấn đề về các mô hình đe dọa - kích thước cố định ở lớp vận chuyển giúp giảm thông tin bị lộ cho các đối thủ bên ngoài (mặc dù phân tích luồng tổng thể vẫn hoạt động), nhưng đối với các đối thủ bên trong (hay còn gọi là các thành viên tham gia tunnel) thì kích thước thông điệp vẫn bị lộ. Các thông điệp tunnel có kích thước cố định giúp giảm thông tin bị lộ cho các thành viên tham gia tunnel, nhưng không ẩn được thông tin bị lộ cho các điểm cuối và gateway của tunnel. Các thông điệp đầu cuối đến đầu cuối có kích thước cố định sẽ ẩn thông tin bị lộ cho tất cả các peer trong mạng.

Như thường lệ, đây là câu hỏi về việc I2P đang cố gắng bảo vệ chống lại ai. Các thông điệp tunnel có kích thước biến đổi rất nguy hiểm, vì chúng cho phép các thành viên tham gia sử dụng chính kích thước thông điệp như một kênh phụ đến các thành viên khác - ví dụ, nếu bạn thấy một thông điệp 1337 byte, bạn đang ở trên cùng một tunnel với một peer cấu kết khác. Ngay cả với một tập hợp cố định các kích thước cho phép (1024, 2048, 4096, v.v.), kênh phụ đó vẫn tồn tại vì các peer có thể sử dụng tần suất của mỗi kích thước như một phương tiện truyền tải (ví dụ, hai thông điệp 1024 byte tiếp theo là một thông điệp 8192). Các thông điệp nhỏ hơn có chi phí phụ trội của các header (IV, tunnel ID, phần hash, v.v.), nhưng các thông điệp lớn hơn có kích thước cố định hoặc tăng độ trễ (do việc gộp lô) hoặc tăng chi phí phụ trội đáng kể (do việc padding). Phân mảnh giúp phân bổ chi phí phụ trội, với chi phí là khả năng mất thông điệp do mất các fragment.

Các cuộc tấn công thời gian cũng có liên quan khi xem xét hiệu quả của các thông điệp có kích thước cố định, mặc dù chúng yêu cầu một cái nhìn đáng kể về các mẫu hoạt động mạng để có hiệu quả. Độ trễ nhân tạo quá mức trong tunnel sẽ được phát hiện bởi người tạo tunnel, do việc kiểm tra định kỳ, khiến toàn bộ tunnel đó bị loại bỏ và các hồ sơ cho các peer trong đó được điều chỉnh.

### Xây dựng các lựa chọn thay thế {#tunnel.building.alternatives}

Tham khảo: [Hashing it out in Public](http://www-users.cs.umn.edu/~hopper/hashing_it_out.pdf)

#### Phương Pháp Xây Dựng Tunnel Cũ {#tunnel.building.old}

Phương pháp xây dựng tunnel cũ, được sử dụng trước phiên bản 0.6.1.10, được ghi lại trên [trang tunnel cũ](/docs/historical/tunnel-alt). Đây là phương pháp "tất cả cùng một lúc" hoặc "song song", trong đó các thông điệp được gửi song song đến từng người tham gia.

#### Xây Dựng Telescopic Một Lần {#tunnel.building.oneshot}

LƯU Ý: Đây là phương pháp hiện tại.

Một câu hỏi nảy sinh liên quan đến việc sử dụng các tunnel thăm dò để gửi và nhận thông điệp tạo tunnel là điều này ảnh hưởng như thế nào đến lỗ hổng của tunnel trước các cuộc tấn công tiền nhiệm. Trong khi các điểm cuối và gateway của những tunnel đó sẽ được phân bố ngẫu nhiên trên toàn mạng (thậm chí có thể bao gồm cả người tạo tunnel trong tập hợp đó), một lựa chọn khác là sử dụng chính các đường dẫn tunnel để chuyển tiếp yêu cầu và phản hồi, như được thực hiện trong [Tor](https://www.torproject.org/). Tuy nhiên, điều này có thể dẫn đến rò rỉ thông tin trong quá trình tạo tunnel, cho phép các peer khám phá có bao nhiêu hop ở phía sau trong tunnel bằng cách theo dõi thời gian hoặc số lượng gói tin khi tunnel được xây dựng.

#### Xây dựng Telescopic "Tương tác" {#tunnel.building.telescoping}

Xây dựng từng hop một với một thông điệp qua phần hiện có của tunnel cho mỗi hop. Có vấn đề lớn vì các peer có thể đếm các thông điệp để xác định vị trí của chúng trong tunnel.

#### Tunnel Phi Khám Phá cho Quản Lý {#tunnel.building.nonexploratory}

Một giải pháp thay thế thứ hai cho quá trình xây dựng tunnel là cung cấp cho router một tập hợp bổ sung các pool inbound và outbound không khám phá, sử dụng chúng cho tunnel request và response. Giả sử router có cái nhìn tích hợp tốt về mạng, điều này không cần thiết, nhưng nếu router bị phân vùng theo cách nào đó, việc sử dụng các pool không khám phá cho quản lý tunnel sẽ giảm rò rỉ thông tin về những peer nào có trong phân vùng của router.

#### Gửi Yêu cầu Khám phá {#tunnel.building.exploratory}

Một lựa chọn thứ ba, được sử dụng cho đến I2P 0.6.1.10, garlic encrypt từng thông điệp yêu cầu tunnel riêng lẻ và gửi chúng đến các hop một cách riêng biệt, truyền tải chúng thông qua các exploratory tunnel với phản hồi được gửi trở lại trong một exploratory tunnel riêng biệt. Chiến lược này đã bị loại bỏ để ủng hộ chiến lược được nêu ở trên.

#### Thêm Lịch sử và Thảo luận {#history}

Trước khi giới thiệu Variable Tunnel Build Message, có ít nhất hai vấn đề:

1. Kích thước của các thông điệp (do giới hạn tối đa 8 hop, trong khi độ dài tunnel thông thường là 2 hoặc 3 hop...
   và nghiên cứu hiện tại cho thấy rằng nhiều hơn 3 hop không tăng cường tính ẩn danh);
2. Tỷ lệ thất bại xây dựng cao, đặc biệt đối với các tunnel dài (và khám phá), vì tất cả các hop phải đồng ý hoặc tunnel sẽ bị loại bỏ.

VTBM đã sửa #1 và cải thiện #2.

Welterde đã đề xuất các sửa đổi cho phương pháp song song để cho phép cấu hình lại. Sponge đã đề xuất sử dụng một loại 'token' nào đó.

Bất kỳ sinh viên nào nghiên cứu về xây dựng tunnel đều phải tìm hiểu hồ sơ lịch sử dẫn đến phương pháp hiện tại, đặc biệt là các lỗ hổng tính ẩn danh có thể tồn tại trong các phương pháp khác nhau. Kho lưu trữ thư điện tử từ tháng 10 năm 2005 đặc biệt hữu ích. Như đã nêu trong [đặc tả tạo tunnel](/docs/specs/tunnel-creation), chiến lược hiện tại được hình thành trong một cuộc thảo luận trên danh sách gửi thư I2P giữa Michael Rogers, Matthew Toseland (toad), và jrandom về cuộc tấn công predecessor.

#### Các Phương Án Sắp Xếp Peer {#ordering}

Một thứ tự ít nghiêm ngặt hơn cũng có thể thực hiện được, đảm bảo rằng trong khi hop sau A có thể là B, thì B không bao giờ có thể đứng trước A. Các tùy chọn cấu hình khác bao gồm khả năng chỉ cố định các inbound tunnel gateway và outbound tunnel endpoint, hoặc xoay vòng chúng theo tỷ lệ MTBF.

## Trộn/Gộp lô {#tunnel.mixing}

Những chiến lược nào nên được sử dụng tại gateway và tại mỗi hop để trì hoãn, sắp xếp lại, định tuyến lại, hoặc đệm các thông điệp? Việc này nên được thực hiện tự động đến mức độ nào, bao nhiều nên được cấu hình như một cài đặt cho mỗi tunnel hoặc mỗi hop, và người tạo tunnel (và do đó, người dùng) nên kiểm soát hoạt động này như thế nào? Tất cả những điều này vẫn chưa rõ ràng, sẽ được giải quyết cho một phiên bản tương lai.
