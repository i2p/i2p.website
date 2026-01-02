---
title: "Định tuyến Tunnel"
description: "Tổng quan về thuật ngữ tunnel I2P, cách xây dựng và vòng đời"
slug: "tunnel-routing"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## Tổng quan

I2P xây dựng các tunnel tạm thời, một chiều — chuỗi các router được sắp xếp theo thứ tự để chuyển tiếp lưu lượng được mã hóa. Các tunnel được phân loại thành **inbound** (tin nhắn chảy về phía người tạo) hoặc **outbound** (tin nhắn chảy ra khỏi người tạo).

Một quá trình trao đổi điển hình định tuyến tin nhắn của Alice ra ngoài thông qua một trong các outbound tunnel của cô ấy, hướng dẫn điểm cuối outbound chuyển tiếp tin nhắn đó đến gateway của một trong các inbound tunnel của Bob, và sau đó Bob nhận được tin nhắn tại điểm cuối inbound của anh ấy.

![Alice kết nối thông qua tunnel gửi đi của mình đến Bob qua tunnel nhận vào của anh ta](/images/tunnelSending.png)

- **A**: Outbound Gateway (Alice)
- **B**: Outbound Participant
- **C**: Outbound Endpoint
- **D**: Inbound Gateway
- **E**: Inbound Participant
- **F**: Inbound Endpoint (Bob)

Các tunnel có thời gian tồn tại cố định là 10 phút và truyền tải các thông điệp có kích thước cố định là 1024 byte (1028 byte bao gồm cả header của tunnel) để ngăn chặn phân tích lưu lượng dựa trên kích thước thông điệp hoặc các mẫu thời gian.

## Từ vựng về Tunnel

- **Tunnel gateway:** Router đầu tiên trong một tunnel. Đối với inbound tunnel, danh tính của router này xuất hiện trong [LeaseSet](/docs/specs/common-structures/) được công bố. Đối với outbound tunnel, gateway là router khởi tạo (A và D ở trên).
- **Tunnel endpoint:** Router cuối cùng trong một tunnel (C và F ở trên).
- **Tunnel participant:** Router trung gian trong một tunnel (B và E ở trên). Các participant không thể xác định vị trí hoặc hướng của tunnel.
- **n-hop tunnel:** Số lượng hop (bước nhảy) giữa các router.
  - **0-hop:** Gateway và endpoint là cùng một router – ẩn danh tối thiểu.
  - **1-hop:** Gateway kết nối trực tiếp với endpoint – độ trễ thấp, ẩn danh thấp.
  - **2-hop:** Mặc định cho exploratory tunnel; cân bằng giữa bảo mật và hiệu suất.
  - **3-hop:** Được khuyến nghị cho các ứng dụng yêu cầu ẩn danh cao.
- **Tunnel ID:** Số nguyên 4 byte duy nhất cho mỗi router và mỗi hop, được chọn ngẫu nhiên bởi người tạo. Mỗi hop nhận và chuyển tiếp trên các ID khác nhau.

## Thông tin Xây dựng Tunnel

Các router đảm nhận vai trò gateway, participant và endpoint nhận các bản ghi khác nhau trong Tunnel Build Message. I2P hiện đại hỗ trợ hai phương pháp:

- **ElGamal** (cũ, bản ghi 528-byte)
- **ECIES-X25519** (hiện tại, bản ghi 218-byte thông qua Short Tunnel Build Message – STBM)

### Information Distributed to Participants

**Gateway nhận được:** - Khóa lớp tunnel (khóa AES-256 hoặc ChaCha20 tùy thuộc vào loại tunnel) - Khóa IV tunnel (để mã hóa các vector khởi tạo) - Khóa reply và reply IV (để mã hóa build reply) - Tunnel ID (chỉ dành cho inbound gateways) - Hash định danh hop tiếp theo và tunnel ID (nếu không phải terminal)

**Các thành viên trung gian nhận được:** - Khóa tầng tunnel và khóa IV cho hop của họ - ID tunnel và thông tin hop tiếp theo - Khóa phản hồi và IV để mã hóa phản hồi xây dựng

**Endpoint nhận:** - Các khóa tunnel layer và IV - Router trả lời và tunnel ID (chỉ outbound endpoint) - Khóa trả lời và IV (chỉ outbound endpoint)

Để biết chi tiết đầy đủ, xem [Tunnel Creation Specification](/docs/specs/implementation/) và [ECIES Tunnel Creation Specification](/docs/specs/implementation/).

## Tunnel Pooling

Router nhóm các tunnel thành **tunnel pool** để đảm bảo dự phòng và phân phối tải. Mỗi pool duy trì nhiều tunnel song song, cho phép chuyển đổi dự phòng khi một tunnel bị lỗi. Các pool được sử dụng nội bộ là **exploratory tunnel**, trong khi các pool dành riêng cho ứng dụng là **client tunnel**.

Mỗi destination duy trì các pool đường hầm inbound và outbound riêng biệt được cấu hình bởi các tùy chọn I2CP (số lượng tunnel, số lượng backup, độ dài và các tham số QoS). Các router giám sát tình trạng tunnel, chạy kiểm tra định kỳ và tự động xây dựng lại các tunnel bị lỗi để duy trì kích thước pool.

## Gộp Tunnel

**Tunnel 0-hop**: Chỉ cung cấp khả năng chối bỏ hợp lý. Lưu lượng luôn xuất phát và kết thúc tại cùng một router — không khuyến khích cho bất kỳ mục đích sử dụng ẩn danh nào.

**Tunnel 1 hop**: Cung cấp tính ẩn danh cơ bản chống lại những người quan sát thụ động nhưng dễ bị tấn công nếu kẻ thù kiểm soát hop duy nhất đó.

**Tunnel 2-hop** : Bao gồm hai router từ xa và tăng đáng kể chi phí tấn công. Mặc định cho các exploratory pool.

**Tunnel 3 hop**: Được khuyến nghị cho các ứng dụng yêu cầu bảo vệ tính ẩn danh mạnh mẽ. Các hop bổ sung sẽ tăng độ trễ mà không mang lại lợi ích bảo mật đáng kể.

**Mặc định**: Router sử dụng **2-hop** exploratory tunnel và **2 hoặc 3 hop** client tunnel theo ứng dụng cụ thể, cân bằng giữa hiệu suất và tính ẩn danh.

## Độ dài Tunnel

Router định kỳ kiểm tra các tunnel bằng cách gửi một `DeliveryStatusMessage` qua một outbound tunnel đến một inbound tunnel. Nếu kiểm tra thất bại, cả hai tunnel sẽ nhận trọng số profile tiêu cực. Các lần thất bại liên tiếp sẽ đánh dấu tunnel không khả dụng; sau đó router sẽ xây dựng lại một tunnel thay thế và công bố một LeaseSet mới. Kết quả được đưa vào các chỉ số năng lực ngang hàng được sử dụng bởi [hệ thống lựa chọn ngang hàng](/docs/overview/tunnel-routing/).

## Kiểm Tra Tunnel

Các router xây dựng tunnel bằng phương pháp **telescoping** không tương tác: một Tunnel Build Message duy nhất lan truyền theo từng hop. Mỗi hop giải mã bản ghi của nó, thêm phản hồi và chuyển tiếp thông điệp đi tiếp. Hop cuối cùng trả về phản hồi xây dựng tổng hợp qua một đường dẫn khác, ngăn chặn việc tương quan. Các triển khai hiện đại sử dụng **Short Tunnel Build Messages (STBM)** cho ECIES và **Variable Tunnel Build Messages (VTBM)** cho các đường dẫn cũ. Mỗi bản ghi được mã hóa theo từng hop sử dụng ElGamal hoặc ECIES-X25519.

## Tạo Tunnel

Lưu lượng tunnel sử dụng mã hóa đa lớp. Mỗi hop thêm hoặc gỡ bỏ một lớp mã hóa khi các thông điệp đi qua tunnel.

- **Tunnel ElGamal:** AES-256/CBC cho payload với PKCS#5 padding.
- **Tunnel ECIES:** ChaCha20 hoặc ChaCha20-Poly1305 cho mã hóa có xác thực.

Mỗi hop có hai khóa: một **layer key** và một **IV key**. Các router giải mã IV, sử dụng nó để xử lý payload, sau đó mã hóa lại IV trước khi chuyển tiếp. Cơ chế IV kép này ngăn chặn việc gắn thẻ thông điệp.

Các cổng ra mã hóa trước tất cả các lớp để các điểm cuối nhận được văn bản rõ sau khi tất cả các bên tham gia đã thêm mã hóa. Các tunnel vào mã hóa theo hướng ngược lại. Các bên tham gia không thể xác định hướng hoặc độ dài của tunnel.

## Mã hóa Tunnel

- Thời gian tồn tại tunnel động và điều chỉnh kích thước pool thích ứng để cân bằng tải mạng
- Các chiến lược kiểm tra tunnel thay thế và chẩn đoán từng hop riêng lẻ
- Xác thực chứng chỉ băng thông hoặc proof-of-work tùy chọn (được triển khai trong API 0.9.65+)
- Nghiên cứu về định hình lưu lượng và chèn chaff cho việc trộn lẫn endpoint
- Tiếp tục loại bỏ ElGamal và di chuyển sang ECIES-X25519

## Phát triển liên tục

- [Đặc tả Triển khai Tunnel](/docs/specs/implementation/)
- [Đặc tả Tạo Tunnel (ElGamal)](/docs/specs/implementation/)
- [Đặc tả Tạo Tunnel (ECIES-X25519)](/docs/specs/implementation/)
- [Đặc tả Thông điệp Tunnel](/docs/specs/implementation/)
- [Garlic Routing](/docs/overview/garlic-routing/)
- [I2P Network Database](/docs/specs/common-structures/)
- [Phân tích và Lựa chọn Peer](/docs/overview/tunnel-routing/)
- [Mô hình Đe dọa I2P](/docs/overview/threat-model/)
- [Mã hóa ElGamal/AES + SessionTag](/docs/legacy/elgamal-aes/)
- [Tùy chọn I2CP](/docs/specs/i2cp/)
