---
title: "Giao thức truyền tải SSU2"
date: 2022-10-11
author: "zzz"
description: "Giao thức truyền tải SSU2"
categories: ["development"]
---

## Tổng quan

I2P đã sử dụng giao thức truyền tải UDP chống kiểm duyệt "SSU" từ năm 2005. Trong 17 năm, chúng tôi hầu như không nhận được (nếu có) báo cáo nào về việc SSU bị chặn. Tuy nhiên, theo các tiêu chuẩn ngày nay về bảo mật, khả năng chống bị chặn và hiệu năng, chúng ta có thể làm tốt hơn. Tốt hơn rất nhiều.

Vì vậy, cùng với [dự án i2pd](https://i2pd.xyz/), chúng tôi đã tạo ra và triển khai "SSU2", một giao thức UDP hiện đại được thiết kế theo các tiêu chuẩn cao nhất về bảo mật và khả năng chống bị chặn. Giao thức này sẽ thay thế SSU.

Chúng tôi đã kết hợp mã hóa theo tiêu chuẩn công nghiệp với các tính năng tốt nhất của các giao thức UDP WireGuard và QUIC, cùng với các tính năng chống kiểm duyệt của giao thức TCP "NTCP2" của chúng tôi. SSU2 có thể là một trong những giao thức truyền tải an toàn nhất từng được thiết kế.

Các nhóm Java I2P và i2pd đang hoàn thiện lớp truyền tải SSU2 và chúng tôi sẽ kích hoạt nó cho tất cả các router trong bản phát hành tiếp theo. Điều này hoàn tất kế hoạch kéo dài suốt một thập kỷ của chúng tôi nhằm nâng cấp toàn bộ phần mật mã từ bản hiện thực Java I2P ban đầu có từ năm 2003. SSU2 sẽ thay thế SSU, vốn là cách duy nhất còn lại mà chúng tôi sử dụng mật mã ElGamal.

- Signature types and ECDSA signatures (0.9.8, 2013)
- Ed25519 signatures and leasesets (0.9.15, 2014)
- Ed25519 routers (0.9.22, 2015)
- Destination encryption types and X25519 leasesets (0.9.46, 2020)
- Router encryption types and X25519 routers (0.9.49, 2021)

Sau khi chuyển sang SSU2, chúng tôi sẽ hoàn tất việc chuyển tất cả các giao thức được xác thực và mã hóa của mình sang các thủ tục bắt tay chuẩn của [Noise Protocol](https://noiseprotocol.org/):

- NTCP2 (0.9.36, 2018)
- ECIES-X25519-Ratchet end-to-end protocol (0.9.46, 2020)
- ECIES-X25519 tunnel build messages (1.5.0, 2021)
- SSU2 (2.0.0, 2022)

Tất cả các giao thức Noise của I2P sử dụng các thuật toán mật mã tiêu chuẩn sau:

- [X25519](https://en.wikipedia.org/wiki/Curve25519)
- [ChaCha20/Poly1305 AEAD](https://www.rfc-editor.org/rfc/rfc8439.html)
- [SHA-256](https://en.wikipedia.org/wiki/SHA-2)

## Mục tiêu

- Upgrade the asymmetric cryptography to the much faster X25519
- Use standard symmetric authenticated encryption ChaCha20/Poly1305
- Improve the obfuscation and blocking resistance features of SSU
- Improve the resistance to spoofed addresses by adapting strategies from QUIC
- Improved handshake CPU efficiency
- Improved bandwidth efficiency via smaller handshakes and acknowledgements
- Improve the security of the peer test and relay features of SSU
- Improve the handling of peer IP and port changes by adapting the "connection migration" feature of QUIC
- Move away from heuristic code for packet handling to documented, algorithmic processing
- Support a gradual network transition from SSU to SSU2
- Easy extensibility using the block concept from NTCP2

## Thiết kế

I2P sử dụng nhiều lớp mã hóa để bảo vệ lưu lượng khỏi kẻ tấn công. Lớp thấp nhất là lớp giao thức truyền tải, được dùng cho các liên kết điểm-đến-điểm giữa hai router. Hiện tại chúng tôi có hai giao thức truyền tải: NTCP2, một giao thức TCP hiện đại được giới thiệu vào năm 2018, và SSU, một giao thức UDP được phát triển vào năm 2005.

SSU2, giống như các giao thức truyền tải của I2P trước đó, không phải là một kênh truyền dữ liệu đa dụng. Nhiệm vụ chính của nó là truyền tải một cách an toàn các thông điệp I2NP cấp thấp của I2P từ router này sang router tiếp theo. Mỗi kết nối điểm-điểm như vậy tạo thành một hop trong một tunnel I2P. Các giao thức I2P tầng cao hơn chạy trên các kết nối điểm-điểm này để chuyển giao garlic messages (thông điệp sử dụng garlic encryption) đầu-cuối giữa các đích đến của I2P.

Việc thiết kế một cơ chế truyền tải UDP đặt ra những thách thức độc đáo và phức tạp không xuất hiện trong các giao thức TCP. Một giao thức UDP phải xử lý các vấn đề bảo mật do giả mạo địa chỉ gây ra, và phải tự triển khai cơ chế kiểm soát tắc nghẽn của riêng nó. Ngoài ra, mọi thông điệp phải được phân mảnh để phù hợp với kích thước gói tối đa (MTU) trên đường dẫn mạng, và được bên nhận ghép lại.

Đầu tiên, chúng tôi dựa rất nhiều vào kinh nghiệm trước đây của mình với các giao thức NTCP2, SSU và streaming của chúng tôi. Sau đó, chúng tôi xem xét kỹ lưỡng và tham khảo sâu rộng từ hai giao thức UDP mới được phát triển:

- QUIC ([RFC 9000](https://www.rfc-editor.org/rfc/rfc9000.html), [RFC 9001](https://www.rfc-editor.org/rfc/rfc9001.html), [RFC 9002](https://www.rfc-editor.org/rfc/rfc9002.html))
- [WireGuard](https://www.wireguard.com/protocol/)

Việc phân loại giao thức và chặn bởi các kẻ tấn công trên đường truyền mang tính đối địch, chẳng hạn như tường lửa cấp quốc gia, không phải là một phần được nêu rõ trong mô hình đe dọa của các giao thức đó. Tuy nhiên, đây là một phần quan trọng trong mô hình đe dọa của I2P, vì sứ mệnh của chúng tôi là cung cấp một hệ thống liên lạc ẩn danh và chống kiểm duyệt cho những người dùng có nguy cơ trên khắp thế giới. Do đó, phần lớn công việc thiết kế của chúng tôi tập trung vào việc kết hợp các bài học rút ra từ NTCP2 và SSU với các tính năng và khả năng bảo mật được hỗ trợ bởi QUIC và WireGuard.

## Hiệu năng

Mạng I2P là một tổ hợp phức tạp của nhiều loại router đa dạng. Có hai triển khai chính đang chạy trên khắp thế giới trên phần cứng từ máy tính trung tâm dữ liệu hiệu năng cao đến Raspberry Pi và điện thoại Android. Các router sử dụng cả hai giao thức truyền tải TCP và UDP. Mặc dù những cải tiến SSU2 là đáng kể, chúng tôi không kỳ vọng chúng sẽ dễ nhận thấy đối với người dùng, dù là cục bộ hay ở tốc độ truyền đầu-cuối.

Dưới đây là một số điểm nổi bật về các cải tiến ước tính của SSU2 so với SSU:

- 40% reduction in total handshake packet size
- 50% or more reduction in handshake CPU
- 90% or more reduction in ACK overhead
- 50% reduction in packet fragmentation
- 10% reduction in data phase overhead

## Kế hoạch chuyển đổi

I2P nỗ lực duy trì khả năng tương thích ngược, vừa để đảm bảo tính ổn định của mạng, vừa để các routers cũ tiếp tục hữu ích và an toàn. Tuy nhiên, vẫn có những giới hạn, vì tính tương thích làm tăng độ phức tạp của mã nguồn và yêu cầu bảo trì.

Các dự án Java I2P và i2pd sẽ đều kích hoạt SSU2 theo mặc định trong các bản phát hành tiếp theo của họ (2.0.0 và 2.44.0) vào cuối tháng 11 năm 2022. Tuy nhiên, họ có các kế hoạch khác nhau về việc vô hiệu hóa SSU. I2pd sẽ vô hiệu hóa SSU ngay lập tức, vì SSU2 là một cải tiến vượt trội so với triển khai SSU của họ. Java I2P dự định vô hiệu hóa SSU vào giữa năm 2023, để hỗ trợ quá trình chuyển đổi dần dần và cho các router cũ thời gian để nâng cấp.

## Tóm tắt


Những người sáng lập I2P đã phải đưa ra một số lựa chọn về các thuật toán và giao thức mật mã. Một số lựa chọn đó tốt hơn những lựa chọn khác, nhưng sau hai mươi năm, phần lớn đang bộc lộ dấu hiệu lạc hậu. Dĩ nhiên, chúng tôi biết điều này sẽ xảy ra, và trong mười năm qua chúng tôi đã lên kế hoạch và triển khai các nâng cấp về mật mã.

SSU2 là giao thức cuối cùng và phức tạp nhất cần phát triển trong lộ trình nâng cấp kéo dài của chúng tôi. UDP có một tập hợp các giả định và mô hình đe dọa đầy thách thức. Trước tiên, chúng tôi đã thiết kế và triển khai ba biến thể khác của các giao thức Noise, và qua đó tích lũy kinh nghiệm cùng hiểu biết sâu hơn về các vấn đề bảo mật và thiết kế giao thức.

Dự kiến SSU2 sẽ được kích hoạt trong các bản phát hành i2pd và Java I2P được lên lịch vào cuối tháng 11 năm 2022. Nếu bản cập nhật diễn ra suôn sẻ, sẽ chẳng ai nhận thấy điều gì khác biệt. Các lợi ích về hiệu năng, tuy đáng kể, có lẽ sẽ không thể đo lường được đối với hầu hết mọi người.

As usual, we recommend that you update to the new release when it's available. The best way to maintain security and help the network is to run the latest release.
