---
title: "Tổng quan về Transport"
description: "Tổng quan về tầng vận chuyển của I2P cho giao tiếp router điểm-điểm"
slug: "transport"
aliases:
  - "/vi/transport"
  - "/vi/transport/"
lastUpdated: "2026-03"
accurateFor: "0.9.69"
---

## Transport trong I2P

Một "transport" trong I2P là một phương thức để giao tiếp trực tiếp, điểm-tới-điểm giữa hai router. Các transport phải cung cấp tính bảo mật và toàn vẹn chống lại các đối thủ bên ngoài trong khi xác thực rằng router được liên hệ là router đúng để nhận một thông điệp cụ thể.

I2P hỗ trợ đồng thời nhiều phương thức truyền tải. Hiện tại có ba phương thức truyền tải được triển khai:

1. [NTCP](/docs/legacy/ntcp/), một giao thức truyền tải TCP Java New I/O (NIO)
2. [SSU](/docs/legacy/ssu/), hoặc Secure Semireliable UDP
3. [NTCP2](/docs/specs/ntcp2/), phiên bản mới của NTCP

Mỗi cái cung cấp một mô hình "kết nối", với xác thực, kiểm soát luồng, xác nhận và truyền lại.

- Giao hàng đáng tin cậy các thông điệp [I2NP](/docs/specs/i2np/). Các transport chỉ hỗ trợ giao hàng thông điệp I2NP. Chúng không phải là các đường ống dữ liệu đa mục đích.
- Giao hàng thông điệp theo thứ tự KHÔNG được đảm bảo bởi tất cả các transport.
- Duy trì một tập hợp các địa chỉ router, một hoặc nhiều cho mỗi transport, mà router công bố như thông tin liên lạc toàn cầu của nó (RouterInfo). Mỗi transport có thể kết nối sử dụng một trong các địa chỉ này, có thể là IPv4 hoặc (từ phiên bản 0.9.8) IPv6.
- Lựa chọn transport tốt nhất cho mỗi thông điệp gửi đi
- Xếp hàng các thông điệp gửi đi theo mức độ ưu tiên
- Giới hạn băng thông, cả gửi đi và nhận về, theo cấu hình của router
- Thiết lập và ngắt kết nối transport
- Mã hóa truyền thông điểm-tới-điểm
- Duy trì giới hạn kết nối cho mỗi transport, triển khai các ngưỡng khác nhau cho các giới hạn này, và truyền đạt trạng thái ngưỡng tới router để nó có thể thực hiện các thay đổi hoạt động dựa trên trạng thái
- Mở cổng tường lửa sử dụng UPnP (Universal Plug and Play)
- Vượt qua NAT/Firewall hợp tác
- Phát hiện IP cục bộ bằng các phương pháp khác nhau, bao gồm UPnP, kiểm tra các kết nối đến, và liệt kê các thiết bị mạng
- Điều phối trạng thái tường lửa và IP cục bộ, và các thay đổi đối với cả hai, giữa các transport
- Truyền đạt trạng thái tường lửa và IP cục bộ, và các thay đổi đối với cả hai, tới router và giao diện người dùng
- Xác định đồng hồ đồng thuận, được sử dụng để định kỳ cập nhật đồng hồ của router, như một phương án dự phòng cho NTP
- Duy trì trạng thái cho mỗi peer, bao gồm việc nó có đang kết nối không, có kết nối gần đây không, và có thể tiếp cận được trong lần thử cuối cùng không
- Đánh giá các địa chỉ IP hợp lệ theo một tập quy tắc cục bộ
- Tuân thủ các danh sách tự động và thủ công của các peer bị cấm do router duy trì, và từ chối các kết nối gửi đi và nhận về tới các peer đó

---

Hệ thống con transport trong I2P cung cấp các dịch vụ sau:

## Dịch vụ Vận chuyển

---

- Một router không có địa chỉ được công bố, vì vậy nó được coi là "ẩn" và không thể nhận kết nối đến
- Một router bị tường lửa chặn, và do đó công bố một địa chỉ SSU chứa danh sách các peer hợp tác hoặc "introducers" sẽ hỗ trợ trong việc vượt qua NAT (xem [đặc tả SSU](/docs/legacy/ssu/) để biết chi tiết)
- Một router không bị tường lửa chặn hoặc các cổng NAT của nó đã mở; nó công bố cả địa chỉ NTCP2 và SSU chứa IP và cổng có thể truy cập trực tiếp.

Hệ thống con transport duy trì một tập hợp các địa chỉ router, mỗi địa chỉ liệt kê một phương thức transport, IP và cổng. Những địa chỉ này tạo thành các điểm liên lạc được quảng cáo, và được router công bố lên cơ sở dữ liệu mạng. Các địa chỉ cũng có thể chứa một tập hợp tùy ý các tùy chọn bổ sung.

## Địa Chỉ Vận Chuyển

Mỗi phương thức vận chuyển có thể công bố nhiều địa chỉ router.

Các tình huống điển hình là:

---

- Cấu hình tùy chọn vận chuyển
- Liệu vận chuyển đã được kết nối với peer hay chưa
- Số lượng kết nối hiện tại so với các ngưỡng giới hạn kết nối khác nhau
- Liệu các nỗ lực kết nối gần đây với peer có thất bại hay không
- Kích thước của thông điệp, vì các vận chuyển khác nhau có giới hạn kích thước khác nhau
- Liệu peer có thể chấp nhận kết nối đến cho vận chuyển đó hay không, như được quảng cáo trong RouterInfo của nó
- Liệu kết nối có phải là gián tiếp (yêu cầu introducers) hay trực tiếp
- Tùy chọn vận chuyển của peer, như được quảng cáo trong RouterInfo của nó

Hệ thống transport chỉ truyền tải [các thông điệp I2NP](/docs/specs/i2np/). Transport được chọn cho bất kỳ thông điệp nào đều độc lập với các giao thức và nội dung tầng trên (thông điệp router hoặc client, cho dù ứng dụng bên ngoài có sử dụng TCP hay UDP để kết nối với I2P, cho dù tầng trên có sử dụng [thư viện streaming](/docs/api/streaming/) hay [datagrams](/docs/api/datagrams/), v.v.).

## Lựa chọn Transport

Đối với mỗi thông điệp gửi đi, hệ thống transport sẽ yêu cầu "đấu giá" từ mỗi transport. Transport đưa ra giá trị thấp nhất (tốt nhất) sẽ thắng cuộc đấu giá và nhận thông điệp để gửi đi. Một transport có thể từ chối tham gia đấu giá.

Việc một transport có đấu thầu hay không, và với giá trị bao nhiêu, phụ thuộc vào nhiều yếu tố:

Nói chung, các giá trị bid được chọn sao cho hai router chỉ được kết nối bằng một transport duy nhất tại bất kỳ thời điểm nào. Tuy nhiên, đây không phải là một yêu cầu bắt buộc.

- Một giao thức truyền tải giống TLS/SSH
- Một giao thức truyền tải "gián tiếp" cho các router không thể truy cập được bởi tất cả các router khác (một dạng của "restricted routes")
- Các giao thức truyền tải pluggable tương thích với Tor

---

Các phương thức truyền tải bổ sung có thể được phát triển, bao gồm:

## Giao thức Truyền tải Mới và Công việc Tương lai

Công việc tiếp tục được thực hiện để điều chỉnh giới hạn kết nối mặc định cho mỗi phương thức truyền tải. I2P được thiết kế như một "mạng lưới ô", trong đó giả định rằng bất kỳ router nào cũng có thể kết nối với bất kỳ router nào khác. Giả định này có thể bị phá vỡ bởi các router đã vượt quá giới hạn kết nối của chúng, và bởi các router nằm sau tường lửa trạng thái hạn chế (các tuyến đường bị hạn chế).

- Giao thức truyền tải giống TLS/SSH
- Giao thức truyền tải "gián tiếp" dành cho các bộ định tuyến không thể kết nối được với tất cả các bộ định tuyến khác (một dạng của "tuyến đường bị hạn chế")
- Các giao thức truyền tải cắm thêm tương thích với Tor

Các giới hạn kết nối hiện tại cao hơn đối với SSU so với NTCP, dựa trên giả định rằng yêu cầu bộ nhớ cho một kết nối NTCP cao hơn so với SSU. Tuy nhiên, vì buffer NTCP một phần nằm trong kernel và buffer SSU nằm trên Java heap, giả định đó khó có thể xác minh.

Phân tích [Breaking and Improving Protocol Obfuscation](http://www.iis.se/docs/hjelmvik_breaking.pdf) và xem cách padding ở tầng transport có thể cải thiện mọi thứ.

Phân tích [Phá vỡ và Cải thiện Việc Ngụy trang Giao thức](http://www.iis.se/docs/hjelmvik_breaking.pdf) và xem xét cách thức thêm độn ở tầng truyền tải có thể cải thiện tình hình.
