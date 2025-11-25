---
title: "ECIES-X25519-AEAD-Ratchet"
number: "144"
author: "zzz, chisana, orignal"
created: "2018-11-22"
lastupdated: "2025-03-05"
status: "Closed"
thread: "http://zzz.i2p/topics/2639"
target: "0.9.46"
implementedin: "0.9.46"
---

## Lưu ý
Việc triển khai và thử nghiệm mạng lưới đang diễn ra.
Có thể có những điều chỉnh nhỏ.
Xem [SPEC](/en/docs/spec/ecies/) để biết đặc tả chính thức.

Các tính năng sau chưa được triển khai tính đến 0.9.46:

- Các khối MessageNumbers, Options và Termination
- Phản hồi ở tầng giao thức
- Khóa tĩnh-zero
- Multicast


## Tổng quan

Đây là một đề xuất cho loại mã hóa đầu-cuối mới đầu tiên
kể từ khi bắt đầu I2P, thay thế cho ElGamal/AES+SessionTags [Elg-AES](/en/docs/spec/elgamal-aes/).

Nó dựa vào công việc trước đây như sau:

- Spec các cấu trúc chung [Common](/en/docs/spec/common-structures/)
- [I2NP](/en/docs/spec/i2np/) spec bao gồm LS2
- ElGamal/AES+Session Tags [Elg-AES](/en/docs/spec/elgamal-aes/)
- http://zzz.i2p/topics/1768 tổng quan về mã hóa bất đối xứng mới
- Tổng quan về mã hóa mức thấp [CRYPTO-ELG](/en/docs/how/cryptography/)
- ECIES http://zzz.i2p/topics/2418
- [NTCP2](/en/docs/transport/ntcp2/) [Prop111](/en/proposals/111-ntcp2/)
- 123 Mục netDB mới
- 142 Mẫu Mã Hóa Mới
- Giao thức [Noise](https://noiseprotocol.org/noise.html)
- Thuật toán dấu kép của [Signal](https://signal.org/docs/specifications/doubleratchet/)

Mục tiêu là hỗ trợ mã hóa mới cho
giao tiếp đầu-cuối, từ điểm đến đến điểm đến.

Thiết kế sẽ sử dụng một thao tác bắt tay Noise và giai đoạn dữ liệu tích hợp dấu kép của Signal.

Tất cả các tham chiếu đến Signal và Noise trong đề xuất này chỉ dành để làm tài liệu nền.
Không cần kiến thức về giao thức Signal và Noise để hiểu
hoặc triển khai đề xuất này.


### Sử dụng ElGamal hiện tại

Để xem xét lại,
các khóa công khai 256-byte của ElGamal có thể được tìm thấy trong các cấu trúc dữ liệu sau đây.
Tham khảo đặc tả cấu trúc chung.

- Trong một Danh tính Router
  Đây là khóa mã hóa của router.

- Trong một Điểm đến
  Khóa công khai của điểm đến đã được sử dụng cho mã hóa i2cp-to-i2cp cũ
  đã bị vô hiệu hóa trong phiên bản 0.6, hiện tại nó không được sử dụng ngoại trừ
  IV cho mã hóa LeaseSet, cái mà đã bị khuyến nghị không nên sử dụng.
  Khóa công khai trong LeaseSet được sử dụng thay vào đó.

- Trong một LeaseSet
  Đây là khóa mã hóa của điểm đến.

- Trong một LS2
  Đây là khóa mã hóa của điểm đến.



### EncTypes trong Key Certs

Để xem xét lại,
chúng tôi đã thêm hỗ trợ cho các loại mã hóa khi chúng tôi thêm hỗ trợ cho các loại chữ ký.
Trường loại mã hóa luôn có giá trị bằng không, cả trong Destinations và RouterIdentities.
Việc có nên thay đổi điều đó là TBD.
Tham khảo đặc tả cấu trúc chung [Common](/en/docs/spec/common-structures/).




### Sử dụng Mã Hóa Bất Đối Xứng

Để xem xét lại, chúng tôi sử dụng ElGamal cho:

1) Các thông điệp Xây dựng Đường hầm (khóa có trong RouterIdentity)
   Thay thế không được bao gồm trong đề xuất này.
   Xem đề xuất 152 [Prop152](/en/proposals/152-ecies-tunnels/).

2) Mã hóa từ router đến router của các thông điệp netdb và I2NP khác (Khóa có trong RouterIdentity)
   Phụ thuộc vào đề xuất này.
   Cần một đề xuất cho 1) cũng như việc đặt khóa trong tùy chọn RI.

3) Mã hóa đầu-cuối ElGamal+AES/SessionTag (khóa có trong LeaseSet, khóa Destination không sử dụng)
   Thay thế ĐƯỢC bao gồm trong đề xuất này.

4) DH tạm thời cho NTCP1 và SSU
   Thay thế không được bao gồm trong đề xuất này.
   Xem đề xuất 111 cho NTCP2.
   Chưa có đề xuất hiện tại cho SSU2.


### Mục tiêu

- Tương thích ngược
- Yêu cầu và xây dựng trên LS2 (đề xuất 123)
- Tận dụng mã hóa mới hoặc các nguyên thủy mới được thêm vào NTCP2 (đề xuất 111)
- Không cần mã hóa mới hoặc nguyên thủy cho hỗ trợ
- Duy trì việc tách biệt giữa mã hóa và ký; hỗ trợ tất cả các phiên bản hiện tại và tương lai
- Cho phép mã hóa mới cho các điểm đến
- Cho phép mã hóa mới cho các router, nhưng chỉ dành cho các thông điệp garlic - việc xây dựng đường hầm sẽ
  là một đề xuất riêng
- Không phá vỡ bất cứ điều gì dựa vào mã băm nhị phân 32 byte của điểm đến, ví dụ như bittorrent
- Duy trì việc truyền tải thông điệp 0-RTT bằng cách sử dụng DH tĩnh-thời gian
- Không yêu cầu đệm / xếp hàng các thông điệp ở lớp giao thức này;
  tiếp tục hỗ trợ việc truyền tải thông điệp không giới hạn theo cả hai hướng mà không cần đợi một phản hồi
- Nâng cấp lên DH tạm thời-tạm thời sau 1 RTT
- Duy trì việc xử lý các thông điệp không theo thứ tự
- Duy trì bảo mật 256-bit
- Thêm bí mật phía trước
- Thêm xác thực (AEAD)
- Hiệu quả CPU hơn nhiều so với ElGamal
- Không dựa vào Java jbigi để làm cho DH hiệu quả
- Giảm thiểu các thao tác DH
- Sử dụng băng thông hơn nhiều so với ElGamal (khối ElGamal 514 byte)
- Hỗ trợ mã hóa mới và cũ trên cùng một đường hầm nếu cần thiết
- Người nhận có thể dễ dàng phân biệt mã hóa mới từ mã hóa cũ đi xuống
  cùng đường hầm
- Những người khác không thể phân biệt giữa mã hóa mới từ mã hóa cũ hoặc trong tương lai
- Loại bỏ phân loại chiều dài Phiên mới vs. Phiên hiện có (hỗ trợ đệm)
- Không yêu cầu thông điệp I2NP mới
- Thay thế kiểm tra SHA-256 trong tải AES bằng AEAD
- Hỗ trợ liên kết của các phiên truyền và nhận để
  các xác nhận có thể xảy ra trong giao thức, thay vì chỉ ngoài băng tầng.
  Điều này cũng sẽ cho phép các phản hồi có bí mật tiền tuyến ngay lập tức.
- Cho phép mã hóa đầu-cuối của một số thông điệp (lưu trữ RouterInfo)
  mà hiện tại chúng ta không thể do chi phí CPULOẠN
- Không thay đổi I2NP Garlic Message
  hoặc Định dạng Hướng dẫn Giao hàng Garlic.
- Loại bỏ các trường không sử dụng hoặc dư thừa trong Bộ Clove Garlic và định dạng Clove. 

Loại bỏ một số vấn đề với thẻ phiên, bao gồm:

- Không thể sử dụng AES cho đến khi có phản hồi đầu tiên
- Không đáng tin cậy và đình trệ nếu giả định việc giao thẻ
- Không hiệu quả về băng thông, đặc biệt là trong việc giao hàng đầu tiên
- Hiệu quả không gian khổng lồ để lưu trữ thẻ
- Chi phí băng thông lớn để giao thẻ
- Rất phức tạp, khó triển khai
- Khó tinh chỉnh cho các trường hợp sử dụng khác nhau
  (truyền phát đối xứng vs. gói dữ liệu, máy chủ vs. khách hàng, băng thông cao vs. thấp)
- Các lỗi cạn kiệt bộ nhớ do việc phân phối thẻ


### Không phải Mục tiêu / Ngoài phạm vi

- Thay đổi định dạng LS2 (đề xuất 123 đã xong)
- Thuật toán xoay vòng DHT mới hoặc tạo ra số ngẫu nhiên chia sẻ
- Mã hóa mới cho việc xây dựng đường hầm.
  Xem đề xuất 152 [Prop152](/en/proposals/152-ecies-tunnels/).
- Mã hóa mới cho mã hóa lớp đường hầm.
  Xem đề xuất 153 [Prop153](/en/proposals/153-ecies-garlic/).
- Phương thức mã hóa, truyền và tiếp nhận các thông điệp I2NP DLM / DSM / DSRM.
  Không thay đổi.
- Không có giao tiếp LS1-to-LS2 hoặc ElGamal/AES-to-đề-xuất này được hỗ trợ.
  Đề xuất này là một giao thức hai chiều.
  Các điểm đến có thể xử lý sự tương thích ngược bằng cách xuất bản hai lease sets
  sử dụng cùng các đường hầm, hoặc đặt cả hai loại mã hóa trong LS2.
- Thay đổi mô hình mối đe doạ
- Chi tiết triển khai không được thảo luận ở đây và sẽ do từng dự án tự giải quyết.
- (Lạc quan) Thêm các phần mở rộng hoặc các móc để hỗ trợ multicast


### Biện minh

ElGamal/AES+SessionTag đã là giao thức đầu-cuối duy nhất của chúng tôi trong khoảng 15 năm,
gần như không có sửa đổi nào cho giao thức.
Hiện có các nguyên thủy mật mã nhanh hơn.
Chúng tôi cần tăng cường bảo mật cho giao thức.
Chúng tôi cũng đã phát triển các chiến lược và giải pháp thay thế để giảm thiểu
chi phí bộ nhớ và băng thông của giao thức, nhưng các chiến lược đó
rất mong manh, khó điều chỉnh, và làm cho giao thức dễ bị
hỏng, dẫn đến việc phiên bị gián đoạn.

Trong khoảng thời gian tương tự, đặc tả ElGamal/AES+SessionTag và tài liệu liên quan
đã mô tả việc tốn băng thông như thế nào để truyền các thẻ phiên,
và đã đề xuất thay thế việc truyền thẻ phiên bằng "PRNG đồng bộ hóa" (Bộ tạo số ngẫu nhiên giả đồng bộ hóa).
PRNG đồng bộ hóa sẽ tạo ra các thẻ giống nhau ở cả hai đầu,
dựa trên một hạt giống chung.
PRNG đồng bộ hóa cũng có thể được gọi là một "ratchet".
Đề xuất này cuối cùng chỉ định cơ chế ratchet đó, và loại bỏ việc gửi thẻ.

Bằng cách sử dụng một ratchet (một PRNG đồng bộ hóa) để tạo ra các
thẻ phiên, chúng tôi loại bỏ chi phí của việc gửi thẻ phiên
trong thông điệp Phiên mới và các thông điệp tiếp theo khi cần.
Đối với một bộ thẻ điển hình gồm 32 thẻ, đây là 1KB.
Điều này cũng loại bỏ việc lưu trữ thẻ phiên ở phía gửi,
do đó cắt giảm yêu cầu lưu trữ một nửa.

Một thao tác bắt tay hai chiều đầy đủ, tương tự như mẫu Noise IK, cần thiết để tránh các cuộc tấn công Key Compromise Impersonation (KCI).
Xem bảng "Payload Security Properties" của Noise trong [NOISE](https://noiseprotocol.org/noise.html).
Để biết thêm thông tin về KCI, xem tài liệu https://www.usenix.org/system/files/conference/woot15/woot15-paper-hlauschek.pdf



### Mô hình đối đe dọa

Mô hình mối đe dọa có phần khác so với NTCP2 (đề xuất 111).
Các node MitM là OBEP và IBGW và được cho là có cái nhìn đầy đủ về
NetDB toàn cầu hiện tại hoặc lịch sử, bằng cách thông đồng với floodfills.

Mục tiêu là ngăn cản các MitM này phân loại lưu lượng như
các thông điệp Phiên mới và Phiên hiện có, hoặc là mã hóa mới so với mã hóa cũ.



## Đề xuất chi tiết

Đề xuất này định nghĩa một giao thức đầu-cuối mới để thay thế ElGamal/AES+SessionTags.
Thiết kế sẽ sử dụng một thao tác bắt tay Noise và giai đoạn dữ liệu tích hợp dấu kép của Signal.


### Tóm tắt Thiết kế Mật mã

Có năm phần của giao thức cần được thiết kế lại:


- 1) Định dạng container Phiên mới và Phiên hiện có
  được thay thế bằng các định dạng mới.
- 2) ElGamal (khóa công khai 256 byte, khóa riêng 128 byte) được thay thế
  bằng ECIES-X25519 (khóa công khai và riêng 32 byte)
- 3) AES được thay thế bằng
  AEAD_ChaCha20_Poly1305 (được viết tắt là ChaChaPoly dưới đây)
- 4) SessionTags sẽ được thay thế bằng ratchets,
  vốn thực chất là một PRNG mật mã hóa, đồng bộ hóa.
- 5) Payload AES, như được định nghĩa trong đặc tả ElGamal/AES+SessionTags,
  được thay thế bằng một định dạng khối tương tự như trong NTCP2.

Mỗi thay đổi trong năm thay đổi có phần riêng của nó dưới đây.


### Các Nguyên Thủy Mật Mã Mới cho I2P

Các triển khai router I2P hiện tại sẽ yêu cầu triển khai cho
các nguyên thủy mật mã chuẩn sau đây,
mà không cần cho các giao thức I2P hiện tại:

- ECIES (nhưng điều này thực chất là X25519)
- Elligator2

Các triển khai router I2P hiện tại chưa triển khai [NTCP2](/en/docs/transport/ntcp2/) ([Prop111](/en/proposals/111-ntcp2/))
cũng sẽ yêu cầu triển khai cho:

- X25519 key generation and DH
- AEAD_ChaCha20_Poly1305 (viết tắt là ChaChaPoly dưới đây)
- HKDF


### Loại mã hóa

Loại mã hóa (sử dụng trong LS2) là 4.
Điều này chỉ ra một khóa công khai X25519 nhỏ-endian 32 byte,
và giao thức đầu-cuối được chỉ định ở đây.

Loại mã hóa 0 là ElGamal.
Các loại mã hóa 1-3 được dành riêng cho ECIES-ECDH-AES-SessionTag, xem đề xuất 145 [Prop145](/en/proposals/145-ecies/).


### Khung Giao thức Noise

Đề xuất này cung cấp yêu cầu dựa trên Noise Protocol Framework
[NOISE](https://noiseprotocol.org/noise.html) (Phiên bản 34, 2018-07-11).
Noise có các tính chất tương tự như giao thức Đứng Quá Gian Đoạn
[STS](https://en.wikipedia.org/wiki/Station-to-Station_protocol), cái mà là cơ sở cho giao thức [SSU](/en/docs/transport/ssu/). Trong thuật ngữ của Noise, Alice
là người khởi xướng, và Bob là người phản hồi.

Đề xuất này dựa trên giao thức Noise_IK_25519_ChaChaPoly_SHA256.
(Thực tế, định danh cho hàm xắc định khóa ban đầu
là "Noise_IKelg2_25519_ChaChaPoly_SHA256"
để chỉ ra các mở rộng I2P - xem phần KDF 1 bên dưới)
Giao thức Noise này sử dụng các nguyên thủy sau:

- Interactive Handshake Pattern: IK
  Alice ngay lập tức truyền khóa tĩnh của cô đến Bob (I)
  Alice đã biết khóa tĩnh của Bob trước đó (K)

- One-Way Handshake Pattern: N
  Alice không truyền khóa tĩnh của cô đến Bob (N)

- DH Function: X25519
  X25519 DH với độ dài khóa là 32 byte như được chỉ định trong [RFC-7748](https://tools.ietf.org/html/rfc7748).

- Cipher Function: ChaChaPoly
  AEAD_CHACHA20_POLY1305 như được chỉ định trong [RFC-7539](https://tools.ietf.org/html/rfc7539) phần 2.8.
  Nonce 12 byte, với 4 byte đầu tiên được đặt thành không.
  Giống hệt như trong [NTCP2](/en/docs/transport/ntcp2/).

- Hash Function: SHA256
  Hash chuẩn 32-byte, đã được sử dụng rộng rãi trong I2P.


Các Bổ sung cho Khung
``````````````````````````

Đề xuất này định nghĩa các cải tiến sau đây cho
Noise_IK_25519_ChaChaPoly_SHA256. Các cải tiến này thường theo hướng dẫn trong
[NOISE](https://noiseprotocol.org/noise.html) phần 13.

1) Các khóa tạm thời rõ ràng được mã hóa với [Elligator2](https://elligator.org/).

2) Phản hồi được tiền tố với một thẻ rõ ràng.

3) Định dạng tải không được mã hóa cho thông điệp 1, 2 và giai đoạn dữ liệu.
   Tất nhiên, điều này không được định nghĩa trong Noise.

Tất cả các thông điệp bao gồm một phần tiêu đề Garlic Message [I2NP](/en/docs/spec/i2np/).
Giai đoạn dữ liệu sử dụng mã hóa tương tự như, nhưng không tương thích với, giai đoạn dữ liệu Noise.


### Thao tác Bắt tay

Các bắt tay sử dụng mẫu thao tác bắt tay [Noise](https://noiseprotocol.org/noise.html).

Sơ đồ chữ cái sau được sử dụng:

- e = khóa tạm thời dùng một lần
- s = khóa tĩnh
- p = tải của thông điệp

Các phiên Một lần và Không bị rằng buộc tương tự như mẫu Noise N.

```dataspec

<- s
  ...
  e es p ->


```

Các phiên rằng buộc tương tự như mẫu Noise IK.

```dataspec

<- s
  ...
  e es s ss p ->
  <- tag e ee se
  <- p
  p ->


```


### Phiên

Giao thức hiện tại của ElGamal/AES+SessionTags là một chiều.
Tại tầng này, người nhận không biết thông điệp từ đâu tới.
Các phiên đi ra và đi vào không được liên kết.
Các xác nhận được thực hiện qua băng tầng qua việc sử dụng một DeliveryStatusMessage
(được chứa trong một GarlicMessage) trong phần đinh.

Có sự không hiệu quả lớn trong một giao thức một chiều.
Bất kỳ sự phản hồi nào cũng phải sử dụng một thông điệp 'Phiên mới' đắt đỏ.
Điều này gây ra sự tiêu tốn lớn hơn về băng thông, CPU và bộ nhớ.

Có cũng các yếu kém bảo mật trong một giao thức một chiều.
Tất cả các phiên dựa trên DH tạm thời-tĩnh.
Không có đường phản hồi, thì Bob không thể "ratchet" khóa tĩnh của mình
thành khóa tạm thời.
Không biết thông điệp từ đâu tới, thì không có cách nào để sử dụng
khóa tạm thời nhận được cho các thông điệp đi ra,
vì vậy phản hồi ban đầu cũng sử dụng DH tạm thời-tĩnh.

Đối với đề xuất này, chúng tôi định nghĩa hai cơ chế để tạo ra một giao thức hai chiều -
"pairing" và "binding".
Các cơ chế này cung cấp hiệu quả và bảo mật tăng cường.


Ngữ cảnh của Phiên
````````````````````

Như với ElGamal/AES+SessionTags, tất cả các phiên đi vào và đi ra
phải ở trong một ngữ cảnh nhất định, hoặc ngữ cảnh của router hoặc
ngữ cảnh cho một điểm đến địa phương cụ thể.
Trong Java I2P, ngữ cảnh này được gọi là Quản lý Khóa Phiên.

Các phiên không được chia sẻ giữa các ngữ cảnh, vì điều đó sẽ
cho phép tương quan giữa các điểm đến địa phương khác nhau,
hoặc giữa một điểm đến địa phương và một router.

Khi một điểm đến nhất định hỗ trợ cả ElGamal/AES+SessionTags
và đề xuất này, cả hai loại phiên có thể chia sẻ một ngữ cảnh.
Xem phần 1c) dưới đây.



kết hợp Các Phiên Đi vào và Đi ra
```````````````````````````````````

Khi một phiên đi ra được tạo tại người bắt đầu (Alice),
một phiên đi vào mới được tạo và ghép cặp với phiên đi ra,
trừ khi không mong đợi có phản hồi (ví dụ: gói dữ liệu thô).

Một phiên đi vào mới luôn luôn được ghép cặp với một phiên đi ra mới,
trừ khi không yêu cầu phản hồi (ví dụ: gói dữ liệu thô).

Nếu một phản hồi được yêu cầu và gắn với một điểm đến hoặc router từ xa,
phiên đi ra mới đó sẽ được gắn với điểm đến hoặc router đó,
và thay thế bất kỳ phiên đi ra trước đó nào đối với điểm đến hoặc router đó.

Ghép cặp các phiên đi vào và đi ra cung cấp một giao thức hai chiều
với khả năng ratcheting khóa DH.



Gắn Kết Các Phiên và Điểm đến
```````````````````````````````

Chỉ có một phiên đi ra đối với một điểm đến hoặc router nhất định.
Có thể có nhiều phiên đi vào hiện tại từ một điểm đến hoặc router nhất định.
Thường thì, khi một phiên đi vào mới được tạo, và luồng dữ liệu được nhận
trên phiên đó (đó cũng là ACK), bất kỳ phiên nào khác sẽ được đánh dấu
để hết hạn khá nhanh chóng, trong vòng một phút hoặc lâu hơn.
Giá trị số các thông điệp đã gửi (PN) được kiểm tra, và nếu không có
các thông điệp chưa được nhận (trong phạm vi) trong phiên đi vào trước,
phiên trước đó có thể bị xóa ngay lập tức.


Khi một phiên đi ra được tạo tại người bắt đầu (Alice),
nó được gắn với một Điểm đến từ xa (Bob),
và bất kỳ phiên đi vào nào được ghép cặp cũng sẽ được gắn với Điểm đến từ xa.
Khi các phiên ratchet, chúng tiếp tục được gắn với Điểm đến từ xa.

Khi một phiên đi vào được tạo tại người nhận (Bob),
nó có thể được gắn với một Điểm đến từ xa (Alice), theo lựa chọn của Alice.
Nếu Alice đưa thông tin gắn kết (khóa tĩnh của cô) trong thông điệp Phiên Mới,
phiên sẽ được gắn với điểm đến đó,
và một phiên đi ra sẽ được tạo và gắn với cùng Điểm đến.
Khi các phiên ratchet, chúng tiếp tục được gắn với Điểm đến từ xa.


Lợi ích của Việc Gắn Kết và Ghép Cặp
`````````````````````````````````````

Đối với trường hợp phổ biến, truyền phát, chúng tôi mong đợi Alice và Bob sử dụng giao thức như sau:

- Alice ghép cặp phiên đi ra mới của cô với một phiên đi vào mới, cả hai đều gắn với điểm đến phía xa (Bob).
- Alice bao gồm thông tin gắn kết và chữ ký, và một yêu cầu phản hồi, trong
  thông điệp Phiên Mới được gửi tới Bob.
- Bob ghép cặp phiên đi vào mới của mình với một phiên đi ra mới, cả hai đều gắn với điểm đến phía xa (Alice).
- Bob gửi một phản hồi (ack) cho Alice trong phiên đã ghép cặp, với một ratchet tới khóa DH mới.
- Alice ratchet tới một phiên đi ra mới với khóa mới của Bob, ghép cặp với phiên đi vào hiện tại.

Bằng cách gắn một phiên đi vào với một điểm đến từ xa, và ghép cặp phiên đi vào
với một phiên đi ra gắn với cùng Điểm đến, chúng ta đạt được hai lợi ích lớn:

1) Phản hồi ban đầu từ Bob đến Alice sử dụng DH tạm thời-tạm thời

2) Sau khi Alice nhận được phản hồi của Bob và ratchet, tất cả các thông điệp tiếp theo từ Alice đến Bob
sử dụng DH tạm thời-tạm thời.


ACK thông điệp
``````````````

Trong ElGamal/AES+SessionTags, khi một LeaseSet được ghép cặp như một nhánh garlic,
hoặc các thẻ được gửi, router gửi yêu cầu một ACK.
Đây là một nhánh garlic riêng biệt chứa một DeliveryStatus Message.
Để có thêm tính bảo mật, DeliveryStatus Message được bọc trong một Garlic Message.
Cơ chế này nằm ngoài băng tầng từ góc độ của giao thức.

Trong giao thức mới, kể từ khi các phiên đi vào và đi ra được ghép cặp,
chúng ta có thể có ACK trong băng tầng. Không cần nhánh riêng biệt nào.

Một ACK rõ ràng chỉ đơn giản là một thông điệp Phiên Hiện Có mà không có khối I2NP.
Tuy nhiên, trong hầu hết các trường hợp, một ACK rõ ràng có thể tránh được, vì có luồng dữ liệu ngược lại.
Có thể là mong muốn cho các triển khai đợi một thời gian ngắn (có lẽ một trăm ms)
trước khi gửi một ACK rõ ràng, để đưa cho tầng ứng dụng hoặc streaming thời gian để phản hồi.

Các triển khai sẽ cũng cần phải hoãn lại bất kỳ việc gửi ACK nào cho đến sau khi
khối I2NP được xử lý, vì Garlic Message có thể chứa một Database Store Message
với một lease set. Một lease set gần đây sẽ là cần thiết để định tuyến ACK,
và điểm đến ở xa (chứa trong lease set) sẽ là cần thiết để
xác minh khóa tĩnh gắn kết.


Thời gian hết hạn Phiên
````````````````````````

Các phiên đi ra phải luôn hết hạn trước các phiên đi vào.
Khi một phiên đi ra hết hạn, và một phiên mới được tạo ra, một phiên đi vào mới cũng sẽ được
tạo ra. Nếu có một phiên đi vào cũ,
nó sẽ được phép hết hạn.



### Multicast

TBD


### Định nghĩa
Chúng tôi định nghĩa các hàm sau đây tương ứng với các khối dựng mật mã được sử dụng.

ZEROLEN
    mảng byte có độ dài bằng không

CSRNG(n)
    đầu ra n-byte từ một bộ tạo số ngẫu nhiên có bảo mật mật mã.

H(p, d)
    Hàm băm SHA-256 nhận một chuỗi cá nhân hóa p và dữ liệu d, và
    tạo ra một đầu ra có độ dài 32 byte.
    Như được định nghĩa trong [NOISE](https://noiseprotocol.org/noise.html). || dưới đây có nghĩa là nối.

    Sử dụng SHA-256 như sau::

        H(p, d) := SHA-256(p || d)

MixHash(d)
    Hàm băm SHA-256 nhận một hash trước đó h và dữ liệu mới d,
    và tạo ra một đầu ra có độ dài 32 byte.
    || dưới đây có nghĩa là nối.

    Sử dụng SHA-256 như sau::

        MixHash(d) := h = SHA-256(h || d)

STREAM
    AEAD ChaCha20/Poly1305 như được chỉ định trong [RFC-7539](https://tools.ietf.org/html/rfc7539).
    S_KEY_LEN = 32 và S_IV_LEN = 12.

    ENCRYPT(k, n, plaintext, ad)
        Mã hóa plaintext sử dụng khóa mã hóa k và nonce n mà PHẢI 
        là duy nhất cho khóa k.
        Dữ liệu liên kết ad là tùy chọn.
        Trả về một ciphertext mà có kích cỡ của plaintext + 16 bytes cho HMAC.

        Toàn bộ ciphertext phải không phân biệt được với ngẫu nhiên
        nếu khóa là bí mật.

    DECRYPT(k, n, ciphertext, ad)
        Giải mã ciphertext sử dụng khóa mã hóa k và nonce n.
        Dữ liệu liên kết ad là tùy chọn.
        Trả về plaintext.

DH
    Hệ thống thỏa thuận khóa công khai X25519. Khóa riêng 32 byte, khóa công khai 32
    byte, tạo đầu ra 32 byte. Có các hàm sau:

    GENERATE_PRIVATE()
        Tạo một khóa riêng mới.

    DERIVE_PUBLIC(privkey)
        Trả về khóa công khai tương ứng với khóa riêng đã cho.

    GENERATE_PRIVATE_ELG2()
        Tạo một khóa riêng mới mà ánh xạ thành khóa công khai phù hợp với mã hóa Elligator2.
        Lưu ý rằng một nửa số khóa riêng tạo ra ngẫu nhiên sẽ không phù hợp và phải bị bỏ qua.

    ENCODE_ELG2(pubkey)
        Trả về khóa công khai được mã hóa Elligator2 tương ứng với khóa công khai đã cho (ảnh ngược).
        Khóa mã hóa là little endian.
        Khóa mã hóa phải 256 bit không phân biệt được với dữ liệu ngẫu nhiên.
        Xem phần Elligator2 bên dưới để biết đặc tả.

    DECODE_ELG2(pubkey)
        Trả về khóa công khai tương ứng với khóa công khai mã hóa Elligator2 đã cho.
        Xem phần Elligator2 bên dưới để biết đặc tả.

    DH(privkey, pubkey)
        Tạo ra một bí mật chia sẻ từ các khóa riêng và công khai đã cho.

HKDF(salt, ikm, info, n)
    Một hàm thỏa thuận khóa mã hóa mà nhận động cơ khóa ikm (cần có entropy tốt nhưng không bị yêu cầu là một chuỗi ngẫu nhiên đồng nhất),
    một muối có độ dài 32 bytes, và một giá trị 'info' cụ thể cho ngữ cảnh, và tạo ra một đầu ra
    n byte phù hợp để sử dụng làm động cơ khóa.

    Sử dụng HKDF như được chỉ định trong [RFC-5869](https://tools.ietf.org/html/rfc5869), sử dụng hàm băm HMAC SHA-256
    như được chỉ định trong [RFC-2104](https://tools.ietf.org/html/rfc2104).

MixKey(d)
    Sử dụng HKDF() với hóa chuỗi trước đó và dữ liệu mới d, và
    đặt hóa chuỗi mới và k.
    Như được định nghĩa trong [NOISE](https://noiseprotocol.org/noise.html).

    Sử dụng HKDF như sau::

        MixKey(d) := output = HKDF(chainKey, d, "", 64)
                     chainKey = output[0:31]
                     k = output[32:63]



### 1) Định dạng thông điệp


Xem xét lại Định dạng thông điệp hiện tại
``````````````````````````````````

Garlic Message như được chỉ định trong [I2NP](/en/docs/spec/i2np/) như sau.
Vì mục tiêu thiết kế là các bước trung gian không thể phân biệt mã hóa mới so với mã hóa cũ,
định dạng này không thể thay đổi, mặc dù trường độ dài là dư thừa.
Định dạng được hiển thị với tiêu đề đầy đủ 16 byte, mặc dù tiêu đề
thực tế có thể ở một định dạng khác nhau, tùy thuộc vào vận chuyển được sử dụng.

Khi được giải mã, dữ liệu chứa một loạt Garlic Clove và dữ liệu bổ sung,
còn được gọi là Bộ Clove.

Xem [I2NP](/en/docs/spec/i2np/) để biết chi tiết và đặc tả đầy đủ.


```dataspec

+----+----+----+----+----+----+----+----+
  |type|      msg_id       |  expiration
  +----+----+----+----+----+----+----+----+
                           |  size   |chks|
  +----+----+----+----+----+----+----+----+
  |      length       |                   |
  +----+----+----+----+                   +
  |          encrypted data               |
  ~                                       ~
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+


```


Xem xét lại Định dạng Dữ liệu Mã hóa
``````````````````````````````````

Định dạng thông điệp hiện tại, được sử dụng hơn 15 năm,
là ElGamal/AES+SessionTags.
Trong ElGamal/AES+SessionTags, có hai định dạng thông điệp:

1) Phiên mới:
- Khối ElGamal 514 byte
- Khối AES (tối thiểu 128 byte, bội số của 16)

2) Phiên hiện tại:
- Thẻ phiên 32 byte
- Khối AES (tối thiểu 128 byte, bội số của 16)

Đệm tối thiểu đến 128 là khi đã thực hiện trong Java I2P nhưng không được thực thi khi tiếp nhận.

Những thông điệp này được đóng gói trong một gói garlic I2NP, thứ chứa
một trường độ dài, vì vậy độ dài đã biết.

Lưu ý rằng không có việc đệm nào được xác định với độ dài không phải bội số 16,
vì vậy Phiên Mới luôn luôn (mod 16 == 2),
và một Phiên Hiện Có luôn luôn (mod 16 == 0).
Chúng ta cần phải sửa điều này.

Người nhận đầu tiên cố gắng tra cứu 32 byte đầu tiên là Thẻ Phiên.
Nếu tìm thấy, anh ta giải mã khối AES.
Nếu không tìm thấy, và dữ liệu dài ít nhất (514+16), anh ta thử giải mã khối ElGamal,
và nếu thành công, giải mã khối AES.


Thẻ Phiên Mới và So Sánh với Signal
````````````````````````````````````

Trong Signal Double Ratchet, tiêu đề chứa:

- DH: Khóa public của ratchet hiện tại
- PN: Độ dài thông điệp của chuỗi trước đó
- N: Message Number

Các "chuỗi gửi" của Signal đại khái tương đương với các bộ thẻ của chúng tôi.
Bằng cách sử dụng một thẻ phiên, chúng ta có thể loại bỏ hầu hết điều đó.

Trong Phiên Mới, chúng tôi chỉ đặt khóa công khai vào tiêu đề chưa mã hóa.

Trong Phiên Hiện Có, chúng tôi sử dụng một thẻ phiên cho tiêu đề.
Thẻ phiên được liên kết với khóa public của ratchet hiện tại,
và số thông điệp.

Trong cả phiên mới và phiên hiện có, PN và N nằm trong nội dung đã mã hóa.

Trong Signal, mọi thứ liên tục ratchet. Một khóa DH mới yêu cầu
người nhận ratchet và gửi một khóa công khai mới trở lại, đó cũng là
xác nhận cho khóa công khai nhận được.
Điều này sẽ nhiều thao tác DH quá nhiều đối với chúng tôi.
Vì vậy chúng tôi tách xác nhận của khóa nhận được và việc tạo ra một khóa mới.
Bất kỳ thông điệp nào sử dụng một thẻ phiên được tạo từ khóa DH mới đều là một ACK.
Chúng tôi chỉ truyền một khóa công khai mới khi chúng tôi muốn tân khóa.

Số lượng tối đa các thông điệp trước khi DH phải ratchet là 65535.

Khi truyền một khóa phiên, chúng tôi dẫn xuất "Bộ Thẻ" từ đó,
thay vì phải gửi thẻ phiên như trước đây.
Một Bộ Thẻ có thể có đến 65536 thẻ.
Tuy nhiên, các nhận nên thực hiện một chiến lược "nhìn về phía trước", thay vì chỉ
tạo tất cả các thẻ có thể cùng một lúc.
Chỉ tạo tối đa N thẻ quá mức so với thẻ cuối cùng đã nhận được.
N có thể tối đa 128, nhưng 32 hoặc thậm chí ít hơn có thể là lựa chọn tốt hơn.



### 1a) Định dạng phiên mới

Khóa công khai một lần của Phiên Mới (32 byte)
Dữ liệu và MAC đã mã hóa (số byte còn lại)

Thông điệp Phiên Mới có thể hoặc không chứa khóa công khai tĩnh của người gửi.
Nếu nó được bao gồm, phiên ngược lại được gắn với khóa đó.
Khóa tĩnh cần được bao gồm nếu dự kiến có phản hồi,
tức là cho luồng dữ liệu và gói dữ liệu có thể phản hồi.
Nó không nên được bao gồm cho các gói dữ liệu thô.

Thông điệp Phiên Mới tương tự như mẫu [NOISE](https://noiseprotocol.org/noise.html) một chiều
"N" (nếu khóa tĩnh không được gửi),
hoặc mẫu hai chiều "IK" (nếu khóa tĩnh được gửi).



### 1b) Định dạng phiên mới (với gắn kết)

Độ dài là 96 + độ dài tải.
Định dạng mã hóa:

```dataspec

+----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   New Session Ephemeral Public Key    |
  +             32 bytes                  +
  |     Encoded with Elligator2           |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +         Static Key                    +
  |       ChaCha20 encrypted data         |
  +            32 bytes                   +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +    (MAC) for Static Key Section       +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +            Payload Section            +
  |       ChaCha20 encrypted data         |
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +         (MAC) for Payload Section     +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+

  Public Key :: 32 bytes, little endian, Elligator2, cleartext

  Static Key encrypted data :: 32 bytes

  Payload Section encrypted data :: remaining data minus 16 bytes

  MAC :: Poly1305 message authentication code, 16 bytes


```


Khóa Tạm thời Phiên Mới
`````````````````````````

Khóa tạm thời dài 32 bytes, được mã hóa với Elligator2.
Khóa này không bao giờ được tái sử dụng; một khóa mới được tạo ra với
mỗi thông điệp, bao gồm cả việc truyền lại.

Khóa Tĩnh
``````````

Khi giải mã, khóa tĩnh X25519 của Alice, 32 bytes.


Tải
```````

Độ dài mã hóa là phần dữ liệu còn lại.
Độ dài đã giải mã là 16 ít hơn độ dài mã hóa.
Tải phải chứa một Khối DateTime và sẽ thường chứa một hoặc nhiều Khối Garlic Clove.
Xem phần tải dưới đây để biết định dạng và yêu cầu bổ sung.



### 1c) Định dạng phiên mới (không có gắn kết)

Nếu không yêu cầu phản hồi, không có khóa tĩnh nào được gửi.


Độ dài là 96 + độ dài tải.
Định dạng mã hóa:

```dataspec

+----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   New Session Ephemeral Public Key    |
  +             32 bytes                  +
  |     Encoded with Elligator2           |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +           Flags Section               +
  |       ChaCha20 encrypted data         |
  +            32 bytes                   +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +         (MAC) for above section       +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +            Payload Section            +
  |       ChaCha20 encrypted data         |
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +         (MAC) for Payload Section     +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+

  Public Key :: 32 bytes, little endian, Elligator2, cleartext

  Flags Section encrypted data :: 32 bytes

  Payload Section encrypted data :: remaining data minus 16 bytes

  MAC :: Poly1305 message authentication code, 16 bytes


```

Khóa Tạm thời Phiên Mới
`````````````````````````

Khóa tạm thời của Alice.
Khóa tạm thời dài 32 bytes, được mã hóa với Elligator2, little endian.
Khóa này không bao giờ được tái sử dụng; một khóa mới được tạo ra với
mỗi thông điệp, bao gồm cả việc truyền lại.


Dữ liệu Giải mã ở Phần Cờ
`````````````````````````

Phần Cờ không chứa gì.
Nó luôn là 32 byte, vì cần phải có chiều dài như
khóa tĩnh cho Phiên Mới với gắn kết.
Bob xác định liệu nó là khóa tĩnh hay phần cờ
bằng cách kiểm tra xem 32 byte có phải là tất cả các số 0 không.

TODO có cần cờ nào ở đây không?

Tải
```````

Độ dài mã hóa là phần dữ liệu còn lại.
Độ dài đã giải mã là 16 ít hơn độ dài mã hóa.
Tải phải chứa một Khối DateTime và sẽ thường chứa một hoặc nhiều Khối Garlic Clove.
Xem phần tải dưới đây để biết định dạng và yêu cầu bổ sung.




### 1d) Định dạng một lần (không có gắn kết hoặc phiên)

Nếu chỉ có một thông điệp duy nhất được mong đợi được gửi,
không cần thiết lập phiên hoặc khóa tĩnh.


Độ dài là 96 + độ dài tải.
Định dạng mã hóa:

```dataspec

+----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |       Ephemeral Public Key            |
  +             32 bytes                  +
  |     Encoded with Elligator2           |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +           Flags Section               +
  |       ChaCha20 encrypted data         +
  +            32 bytes                   +
  |                                       +
  +                                       +
  |                                       +
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code +
  +         (MAC) for above section       +
  |             16 bytes                  +
  +----+----+----+----+----+----+----+----+
  |                                       +
  +            Payload Section            +
  |       ChaCha20 encrypted data         +
  ~                                       ~
  |                                       |
  +                                       +
  |                                       +
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code +
  +         (MAC) for Payload Section     +
  |             16 bytes                  +
  +----+----+----+----+----+----+----+----+

  Public Key :: 32 bytes, little endian, Elligator2, cleartext

  Flags Section encrypted data :: 32 bytes

  Payload Section encrypted data :: remaining data minus 16 bytes

  MAC :: Poly1305 message authentication code, 16 bytes


```


Khóa Một Lần Của Phiên Mới
``````````````````````````

Khóa một lần dài 32 bytes, được mã hóa với Elligator2, little endian.
Khóa này không bao giờ được tái sử dụng; một khóa mới được tạo ra với
mỗi thông điệp, bao gồm cả việc truyền lại.


Dữ liệu Giải mã ở Phần Cờ
``````````````````````````

Phần Cờ không chứa gì.
Nó luôn là 32 byte, vì cần phải có chiều dài như
khóa tĩnh cho Phiên Mới với gắn kết.
Bob xác định liệu nó là khóa tĩnh hay phần cờ
bằng cách kiểm tra xem 32 byte có phải là tất cả các số 0 không.

TODO có cần cờ nào ở đây không?

```dataspec

+----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |                                       |
  +             All zeros                 +
  |              32 bytes                 |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+

  zeros:: All zeros, 32 bytes.


```


Tải
```````

Độ dài mã hóa là phần dữ liệu còn lại.
Độ dài đã giải mã là 16 ít hơn độ dài mã hóa.
Tải phải chứa một Khối DateTime và sẽ thường chứa một hoặc nhiều Khối Garlic Clove.
Xem phần tải dưới đây để biết định dạng và yêu cầu bổ sung.



### 1f) KDFs cho Thông điệp Phiên Mới

KDF cho Chuỗi Khởi Tạo ChainKey
````````````````````````````````

Đây là [NOISE](https://noiseprotocol.org/noise.html) tiêu chuẩn cho IK với tên giao thức đã được sửa đổi.
Lưu ý rằng chúng tôi sử dụng cùng một công cụ khởi tạo cho mẫu IK (các phiên đã gắn kết)
và cho mẫu N (các phiên không gắn kết).

Tên giao thức được sửa đổi vì hai lý do.
Đầu tiên, để chỉ ra rằng các khóa tạm thời được mã hóa với Elligator2,
và thứ hai, để chỉ ra rằng MixHash() được gọi trước thông điệp thứ hai
để kết hợp giá trị thẻ.

```text

Đây là mẫu thông điệp "e":

  // Định nghĩa protocol_name.
  Đặt protocol_name = "Noise_IKelg2+hs2_25519_ChaChaPoly_SHA256"
   (40 bytes, được mã hóa US-ASCII, không NULL kết thúc).

  // Định nghĩa Hash h = 32 bytes
  h = SHA256(protocol_name);

  Định nghĩa ck = chuỗi 32 byte chaining key. Sao chép dữ liệu h vào ck.
  Đặt chainKey = h

  // MixHash(null prologue)
  h = SHA256(h);

  // cho đến đây, có thể được tính toán trước bởi Alice cho tất cả các kết nối đi


```


KDF cho Nội Dung Mã hóa Phần Khóa/Cờ
``````````````````````````````

```text

Đây là mẫu thông điệp "e":

  // Các khóa tĩnh X25519 của Bob
  // bpk là khóa công khai được công bố trong leaseset
  bsk = GENERATE_PRIVATE()
  bpk = DERIVE_PUBLIC(bsk)

  // Khóa công khai tĩnh của Bob
  // MixHash(bpk)
  // || dưới đây nghĩa là nối
  h = SHA256(h || bpk);

  // cho đến đây, có thể được tính toán trước bởi Bob cho tất cả các kết nối vào

  // Các khóa tạm thời X25519 của Alice
  aesk = GENERATE_PRIVATE_ELG2()
  aepk = DERIVE_PUBLIC(aesk)

  // khóa công khai tạm thời của Alice
  // MixHash(aepk)
  // || dưới đây nghĩa là nối
  h = SHA256(h || aepk);

  // h được sử dụng làm dữ liệu liên kết cho AEAD trong Thông điệp Phiên Mới
  // Giữ lại Hash h cho KDF Thư trả lời Phiên Mới
  // eapk được gửi trong thông điệp cleartext trong
  // đầu thông điệp Phiên Mới
  elg2_aepk = ENCODE_ELG2(aepk)
  // As decoded by Bob
  aepk = DECODE_ELG2(elg2_aepk)

  Hết mẫu thông điệp "e".

  Đây là mẫu thông điệp "es":

  // Noise es
  sharedSecret = DH(aesk, bpk) = DH(bsk, aepk)

  // MixKey(DH())
  //[chainKey, k] = MixKey(sharedSecret)
  // các thông số ChaChaPoly để mã hóa/giải mã
  keydata = HKDF(chainKey, sharedSecret, "", 64)
  chainKey = keydata[0:31]

  // các thông số AEAD
  k = keydata[32:63]
  n = 0
  ad = h
  ciphertext = ENCRYPT(k, n, flags/static key section, ad)

  Hết mẫu thông điệp "es".

  Đây là mẫu thông điệp "s":

  // MixHash(ciphertext)
  // Lưu lại cho KDF của Phân Đoạn tải
  h = SHA256(h || ciphertext)

  // Các khóa tĩnh X25519 của Alice
  ask = GENERATE_PRIVATE()
  apk = DERIVE_PUBLIC(ask)

  Hết mẫu thông điệp "s".



```



KDF cho Phân Đoạn Tải (với khóa tĩnh của Alice)
```````````````````````````````````````````````

```text

Đây là mẫu thông điệp "ss":

  // Noise ss
  sharedSecret = DH(ask, bpk) = DH(bsk, apk)

  // MixKey(DH())
  //[chainKey, k] = MixKey(sharedSecret)
  // các thông số ChaChaPoly để mã hóa/giải mã
  // chainKey từ Phần Khóa Static
  Đặt sharedSecret = X25519 DH result
  keydata = HKDF(chainKey, sharedSecret, "", 64)
  chainKey = keydata[0:31]

  // các thông số AEAD
  k = keydata[32:63]
  n = 0
  ad = h
  ciphertext = ENCRYPT(k, n, payload, ad)

  Hết mẫu thông điệp "ss".

  // MixHash(ciphertext)
  // Lưu lại cho KDF của Thư trả lời Phiên Mới
  h = SHA256(h || ciphertext)


```


KDF cho Phân Đoạn Tải (không có khóa tĩnh của Alice)
``````````````````````````````````````````````````

Lưu ý rằng đây là một mẫu Noise "N", nhưng chúng tôi sử dụng cùng một trạng thái khởi tạo "IK"
như cho các phiên đã ràng buộc.

Các thông điệp Phiên Mới không thể được nhận dạng có chứa khóa tĩnh của Alice hay không
cho đến khi khóa tĩnh được giải mã và kiểm tra xem nó có chứa tất cả số 0 không.
Do đó, người nhận phải sử dụng máy trạng thái "IK" cho tất cả
các thông điệp Phiên Mới.
Nếu khóa tĩnh là tất cả số không, mẫu thông điệp "ss" phải được bỏ qua.



```text

chainKey = from Flags/Static key section
  k = from Flags/Static key section
  n = 1
  ad = h from Flags/Static key section
  ciphertext = ENCRYPT(k, n, payload, ad)


```



### 1g) Định dạng Thư trả lời Phiên Mới

Một hoặc nhiều Thư trả lời Phiên Mới có thể được gửi để phản hồi một tin nhắn Phiên Mới duy nhất.
Mỗi phản hồi được đặt trước bởi một thẻ, được tạo từ một Bộ thẻ cho phiên đó.

Thư trả lời Phiên Mới gồm hai phần.
Phần đầu tiên là sự hoàn thành của thao tác ma sát Noise IK với thẻ được thêm trước.
Độ dài của phần đầu tiên là 56 byte.
Phần thứ hai là phân đoạn tải dữ liệu.
Độ dài của phần thứ hai là 16 + độ dài tải.

Tổng độ dài là 72 + độ dài tải.
Định dạng mã hóa:

```dataspec

+----+----+----+----+----+----+----+----+
  |       Session Tag   8 bytes           |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Ephemeral Public Key           +
  |                                       |
  +            32 bytes                   +
  |     Encoded with Elligator2           +
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +  (MAC) for Key Section (no data)      +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +            Payload Section            +
  |       ChaCha20 encrypted data         |
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +         (MAC) for Payload Section     +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+

  Tag :: 8 bytes, cleartext

  Public Key :: 32 bytes, little endian, Elligator2, cleartext

  MAC :: Poly1305 message authentication code, 16 bytes
         Note: The ChaCha20 plaintext data is empty (ZEROLEN)

  Payload Section encrypted data :: remaining data minus 16 bytes

  MAC :: Poly1305 message authentication code, 16 bytes


```

Thẻ Phiên
```````````
Thẻ được tạo trong KDF Thẻ Phiên, như được khởi tạo
trong KDF Khởi tạo DH dưới đây.
Điều này kết nối phản hồi với phiên đó.
Khóa Phiên từ Khởi tạo DH không được sử dụng.


Khóa Tạm thời Phản hồi Phiên Mới
````````````````````````````````

Khóa tạm thời của Bob.
Khóa tạm thời dài 32 bytes, được mã hóa với Elligator2, little endian.
Khóa này không bao giờ được tái sử dụng; một khóa mới được tạo ra với
mỗi thông điệp, bao gồm cả việc truyền lại.


Tải
```````
Độ dài mã hóa là phần dữ liệu còn lại.
Độ dài đã giải mã là 16 ít hơn độ dài mã hóa.
Tải thường sẽ chứa một hoặc nhiều Khối Garlic Clove.
Xem phần tải dưới đây để biết định dạng và yêu cầu bổ sung.


KDF cho Bộ Thẻ Phản hồi
````````````````````````

Một hoặc nhiều thẻ được tạo từ Bộ Thẻ, được khởi tạo bởi
KDF dưới đây, sử dụng chainKey từ thông điệp Phiên Mới.

```text

// Tạo bộ thẻ
  tagsetKey = HKDF(chainKey, ZEROLEN, "SessionReplyTags", 32)
  tagset_nsr = DH_INITIALIZE(chainKey, tagsetKey)


```


KDF cho Nội dung Mã hóa Phần Khóa Phản hồi
``````````````````````````````````````````

```text

// Các khóa từ thông điệp Phiên Mới
  // Các khóa X25519 của Alice
  // apk và tạm thời aepk được gửi trong thông điệp Phiên Mới gốc
  // chìa khoá X25519 tĩnh ask của Alice
  // chìa khoá công khai X25519 apk của Alice
  // chìa khoá riêng tạm thời aesk của Alice
  // chìa khoá công khai X25519 tạm thời aepk của Alice
  // Các khóa tĩnh X25519 của Bob
  // chìa khoá riêng tĩnh bsk của Bob
  // chìa khoá công khai tĩnh bpk của Bob

  // Tạo thẻ
  tagsetEntry = tagset_nsr.GET_NEXT_ENTRY()
  tag = tagsetEntry.SESSION_TAG

  // MixHash(tag)
  h = SHA256(h || tag)

  Đây là mẫu thông điệp "e":

  // Các khóa tạm thời X25519 của Bob
  besk = GENERATE_PRIVATE_ELG2()
  bepk = DERIVE_PUBLIC(besk)

  // khóa tạm thời công khai của Bob
  // MixHash(bepk)
  // || dưới đây nghĩa là nối
  h = SHA256(h || bepk);

  // elg2_bepk được gửi trong phần rõ ràng trong
  // đầu thông điệp Phiên Mới
  elg2_bepk = ENCODE_ELG2(bepk)
  // Được bẻ mã bằng Bob
  bepk = DECODE_ELG2(elg2_bepk)

  Hết mẫu thông điệp "e".

  Đây là mẫu thông điệp "ee":

  // MixKey(DH())
  //[chainKey, k] = MixKey(sharedSecret)
  // các thông số ChaChaPoly để mã hóa/giải mã
  // chainKey từ Phân Đoạn Tải của Thông điệp Phiên Mới
  sharedSecret = DH(aesk, bepk) = DH(besk, aepk)
  keydata = HKDF(chainKey, sharedSecret, "", 32)
  chainKey = keydata[0:31]

  Hết mẫu thông điệp "ee".

  Đây là mẫu thông điệp "se":

  // MixKey(DH())
  //[chainKey, k] = MixKey(sharedSecret)
  sharedSecret = DH(ask, bepk) = DH(besk, apk)
  keydata = HKDF(chainKey, sharedSecret, "", 64)
  chainKey = keydata[0:31]

  // các thông số AEAD
  k = keydata[32:63]
  n = 0
  ad = h
  ciphertext = ENCRYPT(k, n, ZEROLEN, ad)

  Hết mẫu thông điệp "se".

  // MixHash(ciphertext)
  h = SHA256(h || ciphertext)

  chainKey được sử dụng trong ratchet dưới đây.


```


KDF cho Nội Dung Mã hóa Phân Đoạn Tải
``````````````````````````````````````

Điều này giống như thông điệp Phiên Có sẵn đầu tiên,
sau khi tách ra, nhưng không có thẻ riêng.
Ngoài ra, chúng tôi sử dụng băm từ trên để liên kết
tải với thông điệp NSR.


```text

// split()
  keydata = HKDF(chainKey, ZEROLEN, "", 64)
  k_ab = keydata[0:31]
  k_ba = keydata[32:63]
  tagset_ab = DH_INITIALIZE(chainKey, k_ab)
  tagset_ba = DH_INITIALIZE(chainKey, k_ba)

  // các thông số AEAD cho tải của Thư trả lời Phiên Mới
  k = HKDF(k_ba, ZEROLEN, "AttachPayloadKDF", 32)
  n = 0
  ad = h
  ciphertext = ENCRYPT(k, n, payload, ad)

```


### Lưu ý

Nhiều thông điệp NSR có thể được gửi trong phản hồi, mỗi thông điệp với các khóa tạm thời duy nhất, tuỳ thuộc vào kích thước của phản hồi.

Alice và Bob được yêu cầu sử dụng các khóa tạm thời mới cho mỗi thông điệp NS và NSR.

Alice phải nhận được một trong những thông báo NSR của Bob trước khi gửi các thông điệp Phiên Có Sẵn (`Existing Session`),
và Bob phải nhận được một thông điệp ES từ Alice trước khi gửi thông điệp ES.

Các `chainKey` và `k` từ Phần Tải của Bob trong NSR được sử dụng
làm đầu vào cho các Ratchet DH Phiên ES ban đầu (cả hai hướng, xem DH Ratchet KDF).

Bob chỉ được giữ lại các phiên Có Sẵn cho các thông điệp ES nhận được từ Alice.
Bất kỳ phiên đi vào và đi ra nào khác được tạo ra (cho nhiều NSR) nên
được phá hủy ngay sau khi nhận được thông điệp ES đầu tiên của Alice cho một phiên nhất định.



### 1h) Định dạng phiên hiện có

Thẻ phiên (8 byte)
Dữ liệu và MAC đã mã hóa (xem phần 3 dưới đây)


Định dạng
``````
Mã hóa:

```dataspec

+----+----+----+----+----+----+----+----+
  |       Session Tag                     |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +            Payload Section            +
  |       ChaCha20 encrypted data         |
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +              (MAC)                    +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+

  Session Tag :: 8 bytes, cleartext

  Payload Section encrypted data :: remaining data minus 16 bytes

  MAC :: Poly1305 message authentication code, 16 bytes


```


Tải
```````
Độ dài mã hóa là phần dữ liệu còn lại.
Độ dài đã giải mã là 16 ít hơn độ dài mã hóa.
Xem phần tải dưới đây để biết định dạng và yêu cầu.


KDF
```

```text

Xem phần AEAD bên dưới.

  // các thông số AEAD cho tải Phiên Có Sẵn
  k = The 32-byte session key associated with this session tag
  n = The message number N in the current chain, as retrieved from the associated Session Tag.
  ad = The session tag, 8 bytes
  ciphertext = ENCRYPT(k, n, payload, ad)

```



### 2) ECIES-X25519


Định dạng: khóa công khai và khóa riêng 32-byte, little-endian.

Lý do để sử dụng: Được sử dụng trong [NTCP2](/en/docs/transport/ntcp2/).



### 2a) Elligator2

Trong thao tác bắt tay Noise chuẩn, các tin nhắn bắt tay ban đầu trong mỗi hướng bắt đầu với
các khóa tạm thời mà được truyền đi dưới dạng chuỗi rõ ràng.
Vì các khóa X25519 hợp lệ có thể phân biệt từ ngẫu nhiên, một man-in-the-middle có thể phân biệt
những tin nhắn này từ các tin nhắn Phiên Hiện Có thường bắt đầu với các thẻ phiên ngẫu nhiên.
Trong [NTCP2](/en/docs/transport/ntcp2/) ([Prop111](/en/proposals/111-ntcp2/)), chúng tôi đã sử dụng một hàm XOR có chi phí thấp sử dụng khóa tĩnh ngoài băng để làm mờ
khóa này. Tuy nhiên, mô hình đe dọa ở đây là khác nhau; chúng tôi không muốn cho phép bất kỳ MitM nào
sử dụng bất kỳ phương tiện nào để xác nhận điểm đến của lưu lượng, hoặc để phân biệt
các tin nhắn bắt tay ban đầu từ các tin nhắn Phiên Hiện Có.

Do đó, [Elligator2](https://elligator.org/) được sử dụng để chuyển đổi các khóa tạm thời trong các tin nhắn Phiên Mới và Thư trả lời Phiên Mới
để chúng không phân biệt được với các chuỗi ngẫu nhiên đều.



Định dạng
``````

Các khóa công khai và khóa riêng 32-byte.
Các khóa được mã hóa là little endian.

Như được định nghĩa trong [Elligator2](https://elligator.org/), các khóa được mã hóa không phân biệt được với 254 bit ngẫu nhiên.
Chúng tôi yêu cầu 256 bit ngẫu nhiên (32 byte). Do đó, việc mã hóa và giải mã
được định nghĩa như sau:

Mã hóa:

```text

Định nghĩa ENCODE_ELG2()

  // Mã hóa như được định nghĩa trong tài liệu Elligator2
  encodedKey = encode(pubkey)
  // HOẶC với 2 bit ngẫu nhiên với MSB
  randomByte = CSRNG(1)
  encodedKey[31] |= (randomByte & 0xc0)

```


Giải mã:

```text

Định nghĩa DECODE_ELG2()

  // Bịt ngoài 2 bit ngẫu nhiên từ MSB
  encodedKey[31] &= 0x3f
  // Giải mã như được định nghĩa trong tài liệu Elligator2
  pubkey = decode(encodedKey)

```


Lý do để sử dụng
````````````````

Cần thiết để ngăn chặn OBEP và IBGW phân loại lưu lượng.


Ghi chú
```````

Elligator2 làm tăng thời gian tạo khóa trung bình lên gấp đôi, vì một nửa số khóa riêng
sẽ kết quả trong các khóa công khai không phù hợp để mã hóa với Elligator2.
Ngoài ra, thời gian tạo khóa là không giới hạn với phân phối mũ,
vì người tạo khóa phải liên tục thử lại cho tới khi tìm ra một cặp khóa phù hợp.

Chi phí này có thể được quản lý bằng cách thực hiện việc tạo khóa trước,
trong một thread khác, để giữ một hồ chứa các khóa phù hợp.

Người tạo khóa thực hiện hàm ENCODE_ELG2() để xác định sự phù hợp.
Do đó, người tạo khóa nên lưu trữ kết quả của hàm ENCODE_ELG2()
để không cần phải tính toán lại.

Ngoài ra, các khóa không phù hợp có thể được thêm vào hồ chứa khóa
sử dụng cho [NTCP2](/en/docs/transport/ntcp2/), nơi mà Elligator2 không được sử dụng.
Các vấn đề về an ninh của việc làm như vậy đang được xem xét.



### 3) AEAD (ChaChaPoly)

AEAD sử dụng ChaCha20 và Poly1305, giống như trong [NTCP2](/en/docs/transport/ntcp2/).
Điều này tương ứng với [RFC-7539](https://tools.ietf.org/html/rfc7539), cũng được
sử dụng tương tự trong TLS [RFC-7905](https://tools.ietf.org/html/rfc7905).



Đầu vào của Phiên Mới và Thư trả lời Phiên Mới

``````````````````````````````````````

Đầu vào cho các hàm mã hóa/giải mã
cho một khối AEAD trong thông điệp Phiên Mới:

```dataspec

k :: 32 byte cipher key
       Xem KDFs của Phiên Mới và Thư trả lời Phiên Mới bên trên.

  n :: Counter-based nonce, 12 bytes.
       n = 0

  ad :: Associated data, 32 bytes.
        The SHA256 hash of the preceding data, as output from mixHash()

  data :: Plaintext data, 0 or more bytes


```


Đầu vào của Phiên Hiện Có
`````````````````````````

Đầu vào cho các hàm mã hóa/giải mã
cho một khối AEAD trong thông điệp Phiên Hiện Có:

```dataspec

k :: 32 byte session key
       Nhìn từ thẻ phiên đi kèm.

  n :: Counter-based nonce, 12 bytes.
       Bắt đầu từ 0 và tăng dần cho mỗi thông điệp khi truyền tải.
       Đối với người nhận, giá trị
       như đã được tra cứu từ thẻ Phiên đi kèm.
       Bốn byte đầu tiên luôn là không.
       Tám byte cuối cùng là số thông điệp (n), được mã hóa little-endian.
       Giá trị tối đa là 65535.
       Trình phải ratchet khi N đạt giá trị đó.
       Không được sử dụng các giá trị cao hơn.

  ad :: Associated data
        Thẻ phiên

  data :: Plaintext data, 0 or more bytes


```


Định dạng mã hóa
````````````````

Đầu ra của hàm mã hóa, đầu vào của hàm giải mã:

```dataspec

+----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |       ChaCha20 encrypted data         |
  ~               .   .   .               ~
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +              (MAC)                    +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+

  encrypted data :: Same size as plaintext data, 0 - 65519 bytes

  MAC :: Poly1305 message authentication code, 16 bytes


```

Ghi chú
`````
- Vì ChaCha20 là một cipher dòng, các plaintext không cần phải đệm.
  Các byte keystream bổ sung được loại bỏ.

- Khoá cho cipher (256 bits) được đồng ý thông qua phương pháp SHA256 KDF.
  Các chi tiết của KDF cho mỗi thông điệp có trong các phần riêng dưới đây.

- Các khung ChaChaPoly có kích thước đã biết vì chúng được đóng gói trong thông điệp dữ liệu I2NP.

- Đối với tất cả các thông điệp,
  đệm nằm bên trong khung
  dữ liệu được xác thực.


Xử lý lỗi AEAD
```````````````````

Tất cả dữ liệu nhận được mà không vượt qua xác thực AEAD phải bị loại bỏ.
Không có phản hồi nào được gửi trở lại.


Lý do để sử dụng
```````````````

Sử dụng trong [NTCP2](/en/docs/transport/ntcp2/).



### 4) Ratchets

Chúng tôi vẫn sử dụng thẻ phiên, như trước đây, nhưng chúng tôi sử dụng các ratchet để tạo ra chúng.
Thẻ phiên cũng có một tùy chọn thay khóa mà chúng tôi chưa bao giờ triển khai.
Vì vậy, nó giống như một dấu két Signal nhưng chúng tôi chưa bao giờ thực hiện cái thứ hai.

Ở đây chúng tôi định nghĩa một cái gì đó tương tự như Double Ratchet của Signal.
Thẻ phiên được tạo một cách nhất định và đồng nhất trên
cả phía nhận và phía gửi.

Bằng cách sử dụng một ratchet chìa khóa/thẻ đối xứng, chúng tôi loại bỏ việc sử dụng bộ nhớ để lưu trữ thẻ phiên trên phía gửi.
Chúng tôi cũng loại bỏ sự tiêu thụ băng thông của việc gửi các bộ thẻ.
Sử dụng phía nhận vẫn còn đáng kể, nhưng chúng tôi có thể giảm thiểu hơn nữa
bằng cách thu nhỏ thẻ phiên từ 32 byte xuống 8 byte.

Chúng tôi không sử dụng mã hóa tiêu đề như được chỉ định (và tùy chọn) trong Signal,
chúng tôi sử dụng thẻ phiên thay thế.

Bằng cách sử dụng một ratchet DH, chúng tôi đạt được bí mật về phía trước, điều mà chưa bao giờ được triển khai
trong ElGamal/AES+SessionTags.

Lưu ý: Khóa công khai một lần Phiên Mới không phải là một phần của ratchet, chức năng duy nhất của nó
là mã hóa khóa DH ratchet đầu tiên của Alice.


Số Thông Điệp
`````````````

Double Ratchet xử lý các thông điệp bị thất lạc hoặc gửi không theo thứ tự bằng cách bao gồm trong mỗi
