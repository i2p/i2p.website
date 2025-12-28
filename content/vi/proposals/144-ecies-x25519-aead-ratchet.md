---
title: "ECIES-X25519-AEAD-Ratchet"
number: "144"
author: "zzz, chisana, orignal"
created: "2018-11-22"
lastupdated: "2025-03-05"
status: "Đã đóng"
thread: "http://zzz.i2p/topics/2639"
target: "0.9.46"
implementedin: "0.9.46"
toc: true
---

## Ghi chú

Việc triển khai và kiểm thử mạng đang được tiến hành. Có thể có những sửa đổi nhỏ. Xem [SPEC](/docs/specs/ecies/) để biết thông số kỹ thuật chính thức.

Các tính năng sau đây chưa được triển khai tính đến phiên bản 0.9.46:

- Các khối MessageNumbers, Options và Termination
- Phản hồi tầng giao thức
- Khóa tĩnh bằng không
- Multicast

## Tổng quan

Đây là đề xuất cho loại mã hóa đầu-cuối-đầu mới đầu tiên kể từ khi I2P ra đời, để thay thế ElGamal/AES+SessionTags [Elg-AES](/docs/legacy/elgamal-aes/).

Nó dựa trên các công trình trước đó như sau:

- Đặc tả cấu trúc chung [Common Structures](/docs/specs/common-structures/)
- Đặc tả [I2NP](/docs/specs/i2np/) bao gồm LS2
- ElGamal/AES+Session Tags [Elg-AES](/docs/legacy/elgamal-aes/)
- [http://zzz.i2p/topics/1768](http://zzz.i2p/topics/1768) tổng quan mã hóa bất đối xứng mới
- Tổng quan mã hóa cấp thấp [CRYPTO-ELG](/docs/specs/cryptography/)
- ECIES [http://zzz.i2p/topics/2418](http://zzz.i2p/topics/2418)
- [NTCP2](/docs/specs/ntcp2/) [Đề xuất 111](/proposals/111-ntcp-2/)
- 123 Các mục netDB mới
- 142 Template mã hóa mới
- Giao thức [Noise](https://noiseprotocol.org/noise.html)
- Thuật toán double ratchet của [Signal](https://signal.org/docs/)

Mục tiêu là hỗ trợ mã hóa mới cho việc liên lạc đầu cuối, từ destination đến destination.

Thiết kế sẽ sử dụng quá trình bắt tay Noise và giai đoạn dữ liệu kết hợp double ratchet của Signal.

Tất cả các tham chiếu đến Signal và Noise trong đề xuất này chỉ mang tính chất thông tin nền. Không cần kiến thức về các giao thức Signal và Noise để hiểu hoặc triển khai đề xuất này.

### Current ElGamal Uses

Để xem lại, các khóa công khai ElGamal 256-byte có thể được tìm thấy trong các cấu trúc dữ liệu sau. Tham khảo đặc tả các cấu trúc chung.

- Trong Router Identity
  Đây là khóa mã hóa của router.

- Trong một Destination
  Khóa công khai của destination đã được sử dụng cho mã hóa i2cp-to-i2cp cũ
  đã bị vô hiệu hóa trong phiên bản 0.6, hiện tại không được sử dụng ngoại trừ
  IV cho mã hóa LeaseSet, đã lỗi thời.
  Thay vào đó, khóa công khai trong LeaseSet được sử dụng.

- Trong một LeaseSet
  Đây là khóa mã hóa của destination.

- Trong một LS2
  Đây là khóa mã hóa của đích đến.

### EncTypes in Key Certs

Để ôn tập lại, chúng tôi đã thêm hỗ trợ cho các loại mã hóa khi thêm hỗ trợ cho các loại chữ ký. Trường loại mã hóa luôn bằng không, cả trong Destinations và RouterIdentities. Việc có bao giờ thay đổi điều đó hay không vẫn chưa được xác định. Tham khảo đặc tả cấu trúc chung [Common Structures](/docs/specs/common-structures/).

### Các Ứng dụng ElGamal Hiện tại

Để ôn tập, chúng ta sử dụng ElGamal cho:

1) Thông điệp Tunnel Build (khóa nằm trong RouterIdentity)    Việc thay thế không được đề cập trong đề xuất này.    Xem đề xuất 152 [Proposal 152](/proposals/152-ecies-tunnels).

2) Mã hóa router-to-router của netDb và các I2NP msgs khác (Key nằm trong RouterIdentity)    Phụ thuộc vào đề xuất này.    Yêu cầu một đề xuất cho 1) cũng như vậy, hoặc đặt key trong các tùy chọn RI.

3) Client End-to-end ElGamal+AES/SessionTag (khóa nằm trong LeaseSet, khóa Destination không được sử dụng)    Việc thay thế ĐƯỢC đề cập trong đề xuất này.

4) Ephemeral DH cho NTCP1 và SSU    Việc thay thế không được đề cập trong đề xuất này.    Xem đề xuất 111 cho NTCP2.    Hiện tại không có đề xuất nào cho SSU2.

### EncTypes trong Key Certs

- Tương thích ngược
- Yêu cầu và được xây dựng dựa trên LS2 (đề xuất 123)
- Tận dụng crypto mới hoặc các primitives được thêm vào cho NTCP2 (đề xuất 111)
- Không yêu cầu crypto mới hoặc primitives mới để hỗ trợ
- Duy trì sự tách biệt giữa crypto và ký tên; hỗ trợ tất cả các phiên bản hiện tại và tương lai
- Kích hoạt crypto mới cho các destination
- Kích hoạt crypto mới cho các router, nhưng chỉ dành cho garlic message - việc xây dựng tunnel sẽ
  là một đề xuất riêng biệt
- Không làm hỏng bất cứ thứ gì phụ thuộc vào hash destination nhị phân 32-byte, ví dụ như bittorrent
- Duy trì việc gửi tin nhắn 0-RTT bằng cách sử dụng ephemeral-static DH
- Không yêu cầu đệm / xếp hàng tin nhắn tại tầng giao thức này;
  tiếp tục hỗ trợ gửi tin nhắn không giới hạn theo cả hai hướng mà không cần chờ phản hồi
- Nâng cấp lên ephemeral-ephemeral DH sau 1 RTT
- Duy trì xử lý các tin nhắn không theo thứ tự
- Duy trì bảo mật 256-bit
- Thêm forward secrecy
- Thêm xác thực (AEAD)
- Hiệu quả CPU hơn nhiều so với ElGamal
- Không dựa vào Java jbigi để làm cho DH hiệu quả
- Giảm thiểu các hoạt động DH
- Hiệu quả băng thông hơn nhiều so với ElGamal (khối ElGamal 514 byte)
- Hỗ trợ crypto mới và cũ trên cùng một tunnel nếu muốn
- Người nhận có thể phân biệt hiệu quả crypto mới với cũ đi xuống
  cùng một tunnel
- Những người khác không thể phân biệt crypto mới với cũ hoặc tương lai
- Loại bỏ phân loại độ dài phiên Mới so với Hiện có (hỗ trợ padding)
- Không yêu cầu tin nhắn I2NP mới
- Thay thế checksum SHA-256 trong AES payload bằng AEAD
- Hỗ trợ liên kết các phiên truyền và nhận để
  xác nhận có thể xảy ra trong giao thức, thay vì chỉ out-of-band.
  Điều này cũng sẽ cho phép các phản hồi có forward secrecy ngay lập tức.
- Kích hoạt mã hóa end-to-end cho một số tin nhắn nhất định (RouterInfo stores)
  mà hiện tại chúng ta không làm do overhead CPU.
- Không thay đổi I2NP Garlic Message
  hoặc định dạng Garlic Message Delivery Instructions.
- Loại bỏ các trường không sử dụng hoặc thừa trong định dạng Garlic Clove Set và Clove.

Loại bỏ một số vấn đề với session tags, bao gồm:

- Không thể sử dụng AES cho đến khi có phản hồi đầu tiên
- Không đáng tin cậy và bị treo nếu giả định việc gửi tag
- Không hiệu quả về băng thông, đặc biệt là khi gửi lần đầu
- Không hiệu quả về không gian lưu trữ để lưu tag
- Chi phí băng thông rất lớn để gửi tag
- Rất phức tạp, khó thực hiện
- Khó điều chỉnh cho các trường hợp sử dụng khác nhau
  (streaming vs. datagrams, server vs. client, băng thông cao vs. thấp)
- Lỗ hổng cạn kiệt bộ nhớ do việc gửi tag

### Các Ứng Dụng Mã Hóa Bất Đối Xứng

- Thay đổi định dạng LS2 (proposal 123 đã hoàn thành)
- Thuật toán xoay DHT mới hoặc tạo random chia sẻ
- Mã hóa mới cho xây dựng tunnel.
  Xem proposal 152 [Proposal 152](/proposals/152-ecies-tunnels).
- Mã hóa mới cho mã hóa lớp tunnel.
  Xem proposal 153 [Proposal 153](/proposals/153-chacha20-layer-encryption).
- Phương pháp mã hóa, truyền tải và nhận tin nhắn I2NP DLM / DSM / DSRM.
  Không thay đổi.
- Không hỗ trợ giao tiếp LS1-to-LS2 hoặc ElGamal/AES-to-this-proposal.
  Proposal này là một giao thức hai chiều.
  Các destination có thể xử lý khả năng tương thích ngược bằng cách xuất bản hai leaseSet
  sử dụng cùng các tunnel, hoặc đặt cả hai loại mã hóa trong LS2.
- Thay đổi mô hình đe dọa
- Chi tiết triển khai không được thảo luận ở đây và được để lại cho từng dự án.
- (Lạc quan) Thêm extension hoặc hook để hỗ trợ multicast

### Mục tiêu

ElGamal/AES+SessionTag đã là giao thức end-to-end duy nhất của chúng tôi trong khoảng 15 năm, về cơ bản không có sửa đổi nào đối với giao thức. Hiện tại đã có các nguyên thủy mật mã học nhanh hơn. Chúng tôi cần tăng cường bảo mật của giao thức. Chúng tôi cũng đã phát triển các chiến lược heuristic và giải pháp thay thế để giảm thiểu chi phí bộ nhớ và băng thông của giao thức, nhưng những chiến lược đó dễ vỡ, khó điều chỉnh và khiến giao thức càng dễ bị lỗi hơn, dẫn đến việc session bị ngắt.

Trong khoảng thời gian tương tự, đặc tả ElGamal/AES+SessionTag và tài liệu liên quan đã mô tả việc phân phối session tag tốn băng thông như thế nào, và đã đề xuất thay thế việc phân phối session tag bằng một "synchronized PRNG". Một synchronized PRNG tạo ra các tag giống nhau một cách xác định ở cả hai đầu, được sinh ra từ một seed chung. Một synchronized PRNG cũng có thể được gọi là "ratchet". Đề xuất này (cuối cùng) xác định cơ chế ratchet đó, và loại bỏ việc phân phối tag.

Bằng cách sử dụng một ratchet (một PRNG đồng bộ) để tạo ra các session tag, chúng ta loại bỏ chi phí truyền tải session tag trong thông điệp New Session và các thông điệp tiếp theo khi cần thiết. Đối với một tập tag điển hình gồm 32 tag, điều này tiết kiệm được 1KB. Việc này cũng loại bỏ việc lưu trữ session tag ở phía gửi, do đó cắt giảm một nửa yêu cầu lưu trữ.

Cần có một handshake hai chiều đầy đủ, tương tự như Noise IK pattern, để tránh các cuộc tấn công Key Compromise Impersonation (KCI). Xem bảng "Payload Security Properties" của Noise trong [NOISE](https://noiseprotocol.org/noise.html). Để biết thêm thông tin về KCI, xem bài báo https://www.usenix.org/system/files/conference/woot15/woot15-paper-hlauschek.pdf

### Không phải mục tiêu / Ngoài phạm vi

Mô hình đe dọa có phần khác biệt so với NTCP2 (đề xuất 111). Các node MitM là OBEP và IBGW và được giả định có tầm nhìn đầy đủ về NetDB toàn cầu hiện tại hoặc lịch sử, thông qua việc thông đồng với các floodfill.

Mục tiêu là ngăn chặn các MitM này phân loại traffic thành tin nhắn phiên mới và phiên hiện có, hoặc phân biệt giữa crypto mới và crypto cũ.

## Detailed Proposal

Đề xuất này định nghĩa một giao thức đầu cuối mới để thay thế ElGamal/AES+SessionTags. Thiết kế sẽ sử dụng quá trình bắt tay Noise và giai đoạn dữ liệu kết hợp cơ chế double ratchet của Signal.

### Lý do chính đáng

Có năm phần của giao thức cần được thiết kế lại:

- 1) Các định dạng container Session mới và hiện tại
  được thay thế bằng các định dạng mới.
- 2) ElGamal (khóa công khai 256 byte, khóa riêng tư 128 byte) được thay thế
  bằng ECIES-X25519 (khóa công khai và riêng tư 32 byte)
- 3) AES được thay thế bằng
  AEAD_ChaCha20_Poly1305 (viết tắt là ChaChaPoly bên dưới)
- 4) SessionTags sẽ được thay thế bằng ratchets,
  về cơ bản là một PRNG mật mã được đồng bộ hóa.
- 5) Tải trọng AES, như được định nghĩa trong đặc tả ElGamal/AES+SessionTags,
  được thay thế bằng định dạng khối tương tự như trong NTCP2.

Mỗi một trong năm thay đổi có phần riêng của nó bên dưới.

### Mô hình Đe dọa

Các triển khai router I2P hiện tại sẽ yêu cầu triển khai cho các nguyên thủy mật mã tiêu chuẩn sau đây, những thứ không được yêu cầu cho các giao thức I2P hiện tại:

- ECIES (nhưng về cơ bản đây là X25519)
- Elligator2

Các triển khai router I2P hiện có chưa thực hiện [NTCP2](/docs/specs/ntcp2/) ([Đề xuất 111](/proposals/111-ntcp-2/)) cũng sẽ yêu cầu các triển khai cho:

- Tạo khóa X25519 và DH
- AEAD_ChaCha20_Poly1305 (viết tắt là ChaChaPoly bên dưới)
- HKDF

### Crypto Type

Loại mã hóa (được sử dụng trong LS2) là 4. Điều này cho biết một khóa công khai X25519 32-byte little-endian, và giao thức end-to-end được chỉ định tại đây.

Crypto type 0 là ElGamal. Crypto types 1-3 được dành riêng cho ECIES-ECDH-AES-SessionTag, xem đề xuất 145 [Proposal 145](/proposals/145-ecies).

### Tóm tắt Thiết kế Mật mã học

Đề xuất này cung cấp các yêu cầu dựa trên Noise Protocol Framework [NOISE](https://noiseprotocol.org/noise.html) (Phiên bản 34, 2018-07-11). Noise có các thuộc tính tương tự như giao thức Station-To-Station [STS](https://en.wikipedia.org/wiki/Station-to-Station_protocol), là cơ sở cho giao thức [SSU](/docs/legacy/ssu/). Theo thuật ngữ của Noise, Alice là bên khởi tạo, và Bob là bên phản hồi.

Đề xuất này dựa trên giao thức Noise Noise_IK_25519_ChaChaPoly_SHA256. (Định danh thực tế cho hàm dẫn xuất khóa ban đầu là "Noise_IKelg2_25519_ChaChaPoly_SHA256" để chỉ ra các mở rộng I2P - xem phần KDF 1 bên dưới) Giao thức Noise này sử dụng các nguyên hàm sau:

- Interactive Handshake Pattern: IK
  Alice ngay lập tức truyền static key của mình cho Bob (I)
  Alice đã biết static key của Bob trước đó (K)

- One-Way Handshake Pattern: N
  Alice không truyền static key của mình tới Bob (N)

- DH Function: X25519
  X25519 DH với độ dài khóa 32 byte như được quy định trong [RFC-7748](https://tools.ietf.org/html/rfc7748).

- Cipher Function: ChaChaPoly
  AEAD_CHACHA20_POLY1305 như được quy định trong [RFC-7539](https://tools.ietf.org/html/rfc7539) mục 2.8.
  Nonce 12 byte, với 4 byte đầu được đặt bằng không.
  Giống hệt như trong [NTCP2](/docs/specs/ntcp2/).

- Hash Function: SHA256
  Hàm băm chuẩn 32-byte, đã được sử dụng rộng rãi trong I2P.

### Các Nguyên Thủy Mật Mã Mới cho I2P

Đề xuất này định nghĩa các cải tiến sau đây cho Noise_IK_25519_ChaChaPoly_SHA256. Những cải tiến này thường tuân theo các hướng dẫn trong [NOISE](https://noiseprotocol.org/noise.html) mục 13.

1) Khóa tạm thời dạng rõ được mã hóa bằng [Elligator2](https://elligator.cr.yp.to/).

2) Phản hồi được thêm tiền tố với một thẻ cleartext.

3) Định dạng payload được định nghĩa cho các thông điệp 1, 2, và giai đoạn dữ liệu. Tất nhiên, điều này không được định nghĩa trong Noise.

Tất cả các thông điệp đều bao gồm header [I2NP](/docs/specs/i2np/) Garlic Message. Giai đoạn dữ liệu sử dụng mã hóa tương tự nhưng không tương thích với giai đoạn dữ liệu Noise.

### Loại Mã Hóa

Handshake sử dụng các mẫu handshake [Noise](https://noiseprotocol.org/noise.html).

Ánh xạ chữ cái sau đây được sử dụng:

- e = khóa tạm thời một lần
- s = khóa tĩnh
- p = tải trọng thông điệp

Các phiên One-time và Unbound tương tự như mẫu Noise N.

```

<- s
  ...
  e es p ->

```
Các phiên bound tương tự như mẫu Noise IK.

```

<- s
  ...
  e es s ss p ->
  <- tag e ee se
  <- p
  p ->

```
### Noise Protocol Framework

Giao thức ElGamal/AES+SessionTag hiện tại là đơn hướng. Ở lớp này, bên nhận không biết tin nhắn đến từ đâu. Các phiên kết nối đi ra và đi vào không được liên kết với nhau. Xác nhận được thực hiện ngoài băng tần bằng cách sử dụng DeliveryStatusMessage (được bao bọc trong GarlicMessage) trong clove.

Có sự kém hiệu quả đáng kể trong giao thức một chiều. Bất kỳ phản hồi nào cũng phải sử dụng thông điệp 'New Session' tốn kém. Điều này gây ra việc sử dụng băng thông, CPU và bộ nhớ cao hơn.

Ngoài ra còn có những điểm yếu về bảo mật trong giao thức một chiều. Tất cả các phiên đều dựa trên ephemeral-static DH. Không có đường trả về, Bob không có cách nào để "ratchet" khóa tĩnh của mình thành khóa ephemeral. Không biết tin nhắn đến từ đâu, không có cách nào sử dụng khóa ephemeral đã nhận cho các tin nhắn gửi đi, vì vậy phản hồi ban đầu cũng sử dụng ephemeral-static DH.

Đối với đề xuất này, chúng tôi định nghĩa hai cơ chế để tạo ra một giao thức hai chiều - "pairing" và "binding". Các cơ chế này cung cấp hiệu quả và bảo mật tăng cường.

### Bổ sung vào Framework

Giống như với ElGamal/AES+SessionTags, tất cả các phiên inbound và outbound phải nằm trong một ngữ cảnh nhất định, hoặc là ngữ cảnh của router hoặc ngữ cảnh cho một điểm đích cục bộ cụ thể. Trong Java I2P, ngữ cảnh này được gọi là Session Key Manager.

Các session không được chia sẻ giữa các context, vì điều đó sẽ cho phép tương quan giữa các local destination khác nhau, hoặc giữa một local destination và router.

Khi một destination nhất định hỗ trợ cả ElGamal/AES+SessionTags và đề xuất này, cả hai loại session có thể chia sẻ một context. Xem phần 1c) bên dưới.

### Các Mẫu Handshake

Khi một phiên outbound được tạo tại nguồn gốc (Alice), một phiên inbound mới sẽ được tạo và ghép đôi với phiên outbound, trừ khi không mong đợi phản hồi (ví dụ: raw datagrams).

Một phiên inbound mới luôn được ghép cặp với một phiên outbound mới, trừ khi không yêu cầu phản hồi (ví dụ: raw datagrams).

Nếu một phản hồi được yêu cầu và liên kết với một đích xa hoặc router, phiên gửi đi mới đó sẽ được liên kết với đích hoặc router đó, và thay thế bất kỳ phiên gửi đi trước đó nào đến đích hoặc router đó.

Việc ghép nối các phiên inbound và outbound cung cấp một giao thức hai chiều với khả năng ratcheting các khóa DH.

### Phiên

Chỉ có một phiên gửi đi (outbound session) đến một đích hoặc router nhất định. Có thể có nhiều phiên nhận vào (inbound session) hiện tại từ một đích hoặc router nhất định. Nói chung, khi một phiên nhận vào mới được tạo và lưu lượng được nhận trên phiên đó (đóng vai trò như một ACK), bất kỳ phiên nào khác sẽ được đánh dấu để hết hạn tương đối nhanh, trong khoảng một phút hoặc hơn. Giá trị tin nhắn đã gửi trước đó (PN) được kiểm tra, và nếu không có tin nhắn chưa được nhận (trong phạm vi kích thước cửa sổ) trong phiên nhận vào trước đó, phiên trước đó có thể bị xóa ngay lập tức.

Khi một phiên outbound được tạo tại điểm khởi tạo (Alice), nó được ràng buộc với Destination đầu xa (Bob), và bất kỳ phiên inbound được ghép đôi nào cũng sẽ được ràng buộc với Destination đầu xa. Khi các phiên ratchet, chúng tiếp tục được ràng buộc với Destination đầu xa.

Khi một phiên inbound được tạo tại bên nhận (Bob), nó có thể được ràng buộc với Destination ở đầu xa (Alice), tùy thuộc vào tùy chọn của Alice. Nếu Alice bao gồm thông tin ràng buộc (static key của cô ấy) trong thông điệp New Session, phiên sẽ được ràng buộc với destination đó, và một phiên outbound sẽ được tạo và ràng buộc với cùng Destination. Khi các phiên ratchet, chúng tiếp tục được ràng buộc với Destination ở đầu xa.

### Ngữ cảnh Session

Đối với trường hợp phổ biến, streaming, chúng tôi mong đợi Alice và Bob sử dụng giao thức như sau:

- Alice ghép phiên gửi đi mới của cô với một phiên nhận về mới, cả hai đều được ràng buộc với đích đến ở đầu xa (Bob).
- Alice bao gồm thông tin ràng buộc và chữ ký, cùng với yêu cầu phản hồi, trong thông điệp New Session được gửi tới Bob.
- Bob ghép phiên nhận về mới của anh với một phiên gửi đi mới, cả hai đều được ràng buộc với đích đến ở đầu xa (Alice).
- Bob gửi phản hồi (ack) tới Alice trong phiên đã được ghép, với một ratchet tới khóa DH mới.
- Alice thực hiện ratchet tới phiên gửi đi mới với khóa mới của Bob, được ghép với phiên nhận về hiện có.

Bằng cách liên kết một phiên inbound với một Destination ở đầu xa, và ghép cặp phiên inbound đó với một phiên outbound được liên kết với cùng một Destination, chúng ta đạt được hai lợi ích chính:

1) Phản hồi ban đầu từ Bob đến Alice sử dụng ephemeral-ephemeral DH

2) Sau khi Alice nhận được phản hồi của Bob và thực hiện ratchet, tất cả các thông điệp tiếp theo từ Alice gửi đến Bob đều sử dụng DH ephemeral-ephemeral.

### Ghép Nối Các Phiên Inbound và Outbound

Trong ElGamal/AES+SessionTags, khi một LeaseSet được đóng gói như một garlic clove, hoặc các tag được gửi đi, router gửi sẽ yêu cầu một ACK. Đây là một garlic clove riêng biệt chứa một DeliveryStatus Message. Để tăng cường bảo mật, DeliveryStatus Message được bao bọc trong một Garlic Message. Cơ chế này nằm ngoài băng tần từ góc độ của giao thức.

Trong protocol mới, vì các phiên inbound và outbound được ghép cặp, chúng ta có thể có ACKs trong cùng băng tần. Không cần clove riêng biệt.

ACK rõ ràng đơn giản là một thông điệp Existing Session không có khối I2NP. Tuy nhiên, trong hầu hết các trường hợp, ACK rõ ràng có thể được tránh, vì có lưu lượng ngược. Có thể mong muốn cho các triển khai đợi một thời gian ngắn (có lẽ khoảng một trăm ms) trước khi gửi ACK rõ ràng, để cung cấp thời gian cho lớp streaming hoặc ứng dụng phản hồi.

Các triển khai cũng sẽ cần trì hoãn việc gửi bất kỳ ACK nào cho đến sau khi khối I2NP được xử lý, vì Garlic Message có thể chứa Database Store Message với một lease set. Một lease set gần đây sẽ cần thiết để định tuyến ACK, và điểm đích xa (chứa trong lease set) sẽ cần thiết để xác minh khóa tĩnh ràng buộc.

### Ràng Buộc Sessions và Destinations

Các phiên outbound phải luôn hết hạn trước các phiên inbound. Khi một phiên outbound hết hạn và một phiên mới được tạo, một phiên inbound được ghép đôi mới cũng sẽ được tạo. Nếu có phiên inbound cũ, nó sẽ được cho phép hết hạn.

### Lợi ích của Binding và Pairing

Sẽ được bổ sung

### Message ACKs

Chúng ta định nghĩa các hàm sau tương ứng với các khối xây dựng mật mã được sử dụng.

ZEROLEN

    zero-length byte array

CSRNG(n)

    n-byte output from a cryptographically-secure random number generator.

H(p, d)

    SHA-256 hash function that takes a personalization string p and data d, and
    produces an output of length 32 bytes.
    As defined in [NOISE](https://noiseprotocol.org/noise.html).
    || below means append.

    Use SHA-256 as follows::

        H(p, d) := SHA-256(p || d)

MixHash(d)

    SHA-256 hash function that takes a previous hash h and new data d,
    and produces an output of length 32 bytes.
    || below means append.

    Use SHA-256 as follows::

        MixHash(d) := h = SHA-256(h || d)

STREAM

    The ChaCha20/Poly1305 AEAD as specified in [RFC-7539](https://tools.ietf.org/html/rfc7539).
    S_KEY_LEN = 32 and S_IV_LEN = 12.

    ENCRYPT(k, n, plaintext, ad)
        Encrypts plaintext using the cipher key k, and nonce n which MUST be unique for
        the key k.
        Associated data ad is optional.
        Returns a ciphertext that is the size of the plaintext + 16 bytes for the HMAC.

        The entire ciphertext must be indistinguishable from random if the key is secret.

    DECRYPT(k, n, ciphertext, ad)
        Decrypts ciphertext using the cipher key k, and nonce n.
        Associated data ad is optional.
        Returns the plaintext.

DH

    X25519 public key agreement system. Private keys of 32 bytes, public keys of 32
    bytes, produces outputs of 32 bytes. It has the following
    functions:

    GENERATE_PRIVATE()
        Generates a new private key.

    DERIVE_PUBLIC(privkey)
        Returns the public key corresponding to the given private key.

    GENERATE_PRIVATE_ELG2()
        Generates a new private key that maps to a public key suitable for Elligator2 encoding.
        Note that half of the randomly-generated private keys will not be suitable and must be discarded.

    ENCODE_ELG2(pubkey)
        Returns the Elligator2-encoded public key corresponding to the given public key (inverse mapping).
        Encoded keys are little endian.
        Encoded key must be 256 bits indistinguishable from random data.
        See Elligator2 section below for specification.

    DECODE_ELG2(pubkey)
        Returns the public key corresponding to the given Elligator2-encoded public key.
        See Elligator2 section below for specification.

    DH(privkey, pubkey)
        Generates a shared secret from the given private and public keys.

HKDF(salt, ikm, info, n)

    A cryptographic key derivation function which takes some input key material ikm (which
    should have good entropy but is not required to be a uniformly random string), a salt
    of length 32 bytes, and a context-specific 'info' value, and produces an output
    of n bytes suitable for use as key material.

    Use HKDF as specified in [RFC-5869](https://tools.ietf.org/html/rfc5869), using the HMAC hash function SHA-256
    as specified in [RFC-2104](https://tools.ietf.org/html/rfc2104). This means that SALT_LEN is 32 bytes max.

MixKey(d)

    Use HKDF() with a previous chainKey and new data d, and
    sets the new chainKey and k.
    As defined in [NOISE](https://noiseprotocol.org/noise.html).

    Use HKDF as follows::

        MixKey(d) := output = HKDF(chainKey, d, "", 64)
                     chainKey = output[0:31]
                     k = output[32:63]


### Thời Gian Chờ Session

### Multicast

Garlic Message như được quy định trong [I2NP](/docs/specs/i2np/) như sau. Vì mục tiêu thiết kế là các hop trung gian không thể phân biệt crypto mới với cũ, định dạng này không thể thay đổi, mặc dù trường length là dư thừa. Định dạng được hiển thị với header 16-byte đầy đủ, mặc dù header thực tế có thể ở định dạng khác, tùy thuộc vào transport được sử dụng.

Khi được giải mã, dữ liệu chứa một chuỗi các Garlic Cloves và dữ liệu bổ sung, còn được gọi là Clove Set.

Xem [I2NP](/docs/specs/i2np/) để biết chi tiết và đặc tả đầy đủ.

```

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
### Định nghĩa

Định dạng thông điệp hiện tại, được sử dụng trong hơn 15 năm, là ElGamal/AES+SessionTags. Trong ElGamal/AES+SessionTags, có hai định dạng thông điệp:

1) Phiên mới: - Khối ElGamal 514 byte - Khối AES (tối thiểu 128 byte, bội số của 16)

2) Phiên hiện có: - 32 byte Session Tag - Khối AES (tối thiểu 128 byte, bội số của 16)

Padding tối thiểu đến 128 được triển khai như trong Java I2P nhưng không được thực thi khi nhận.

Những thông điệp này được đóng gói trong một thông điệp I2NP garlic, chứa trường độ dài, vì vậy độ dài đã được biết.

Lưu ý rằng không có padding được định nghĩa cho độ dài không chia hết cho 16, do đó New Session luôn có (mod 16 == 2), và Existing Session luôn có (mod 16 == 0). Chúng ta cần khắc phục điều này.

Bên nhận đầu tiên cố gắng tra cứu 32 byte đầu tiên như một Session Tag. Nếu tìm thấy, nó giải mã khối AES. Nếu không tìm thấy và dữ liệu có độ dài ít nhất (514+16), nó cố gắng giải mã khối ElGamal, và nếu thành công, sẽ giải mã khối AES.

### 1) Định dạng thông điệp

Trong Signal Double Ratchet, header chứa:

- DH: Khóa công khai ratchet hiện tại
- PN: Độ dài tin nhắn chuỗi trước đó
- N: Số thứ tự tin nhắn

"Sending chains" của Signal tương đương với các tag set của chúng ta. Bằng cách sử dụng session tag, chúng ta có thể loại bỏ phần lớn điều đó.

Trong New Session, chúng tôi chỉ đặt public key vào header không được mã hóa.

Trong Existing Session, chúng ta sử dụng session tag cho header. Session tag được liên kết với ratchet public key hiện tại và message number.

Trong cả phiên mới và phiên hiện có, PN và N đều nằm trong phần thân được mã hóa.

Trong Signal, mọi thứ liên tục được ratchet. Một public key DH mới yêu cầu bên nhận phải ratchet và gửi lại một public key mới, điều này cũng đóng vai trò như ack cho public key đã nhận. Điều này sẽ có quá nhiều phép toán DH đối với chúng ta. Vì vậy chúng ta tách biệt việc ack public key đã nhận và việc truyền một public key mới. Bất kỳ thông điệp nào sử dụng session tag được tạo từ public key DH mới đều cấu thành một ACK. Chúng ta chỉ truyền một public key mới khi muốn rekey.

Số lượng thông điệp tối đa trước khi DH phải ratchet là 65535.

Khi phân phối một session key, chúng tôi rút ra "Tag Set" từ nó, thay vì phải phân phối cả session tags. Một Tag Set có thể chứa tối đa 65536 tags. Tuy nhiên, các receiver nên triển khai chiến lược "look-ahead", thay vì tạo ra tất cả các tags có thể cùng một lúc. Chỉ tạo ra tối đa N tags sau tag tốt cuối cùng đã nhận. N có thể tối đa là 128, nhưng 32 hoặc thậm chí ít hơn có thể là lựa chọn tốt hơn.

### Xem xét Định dạng Thông điệp Hiện tại

New Session One Time Public key (32 bytes) Dữ liệu mã hóa và MAC (các byte còn lại)

Thông điệp New Session có thể chứa hoặc không chứa khóa công khai tĩnh của người gửi. Nếu được bao gồm, phiên ngược sẽ được liên kết với khóa đó. Khóa tĩnh nên được bao gồm nếu dự kiến có phản hồi, tức là cho streaming và datagram có thể trả lời. Không nên bao gồm cho raw datagram.

Thông điệp New Session tương tự như pattern Noise [NOISE](https://noiseprotocol.org/noise.html) một chiều "N" (nếu static key không được gửi), hoặc pattern hai chiều "IK" (nếu static key được gửi).

### Đánh giá Định dạng Dữ liệu Mã hóa

Độ dài là 96 + độ dài payload. Định dạng mã hóa:

```

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
### Session Tags Mới và So sánh với Signal

Khóa tạm thời có độ dài 32 byte, được mã hóa bằng Elligator2. Khóa này không bao giờ được sử dụng lại; một khóa mới được tạo ra với mỗi thông điệp, bao gồm cả việc truyền lại.

### 1a) Định dạng phiên mới

Khi được giải mã, khóa tĩnh X25519 của Alice, 32 bytes.

### 1b) Định dạng phiên mới (với ràng buộc)

Độ dài được mã hóa là phần dữ liệu còn lại. Độ dài được giải mã ít hơn độ dài được mã hóa 16 byte. Payload phải chứa một khối DateTime và thường sẽ chứa một hoặc nhiều khối Garlic Clove. Xem phần payload bên dưới để biết định dạng và các yêu cầu bổ sung.

### Khóa Tạm Thời Phiên Mới

Nếu không yêu cầu phản hồi, không có static key nào được gửi.

Độ dài là 96 + độ dài payload. Định dạng mã hóa:

```

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
### Khóa Tĩnh

Khóa tạm thời của Alice. Khóa tạm thời có độ dài 32 byte, được mã hóa bằng Elligator2, little endian. Khóa này không bao giờ được tái sử dụng; một khóa mới được tạo ra cho mỗi thông điệp, bao gồm cả việc truyền lại.

### Tải trọng

Phần Flags không chứa gì cả. Nó luôn có độ dài 32 byte, vì nó phải có cùng độ dài với static key cho các thông điệp New Session với binding. Bob xác định xem đó là static key hay phần flags bằng cách kiểm tra xem 32 byte đó có phải toàn là số không hay không.

TODO có cần thêm cờ (flag) nào ở đây không?

### 1c) Định dạng phiên mới (không có ràng buộc)

Độ dài được mã hóa là phần dữ liệu còn lại. Độ dài sau khi giải mã nhỏ hơn 16 so với độ dài được mã hóa. Payload phải chứa một khối DateTime và thường sẽ chứa một hoặc nhiều khối Garlic Clove. Xem phần payload bên dưới để biết định dạng và các yêu cầu bổ sung.

### Khóa Tạm Thời Phiên Mới

Nếu chỉ có một tin nhắn duy nhất được dự kiến sẽ được gửi, không cần thiết lập phiên hoặc khóa tĩnh.

Độ dài là 96 + độ dài payload. Định dạng mã hóa:

```

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
### Phần Flags Dữ liệu đã giải mã

Khóa một lần có độ dài 32 byte, được mã hóa bằng Elligator2, little endian. Khóa này không bao giờ được sử dụng lại; một khóa mới được tạo ra với mỗi thông điệp, bao gồm cả việc truyền lại.

### Payload

Phần Flags không chứa gì cả. Nó luôn có độ dài 32 byte, bởi vì nó phải có cùng độ dài với static key cho các thông điệp New Session có binding. Bob xác định xem đó là static key hay phần flags bằng cách kiểm tra xem 32 byte đó có phải toàn số không hay không.

TODO có cần flag nào ở đây không?

```

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
### 1d) Định dạng một lần (không có ràng buộc hoặc phiên)

Độ dài mã hóa là phần còn lại của dữ liệu. Độ dài sau giải mã ít hơn 16 so với độ dài mã hóa. Payload phải chứa một khối DateTime và thường sẽ chứa một hoặc nhiều khối Garlic Clove. Xem phần payload bên dưới để biết định dạng và các yêu cầu bổ sung.

### Khóa Một Lần Cho Phiên Mới

### Phần Flags Dữ liệu đã giải mã

Đây là [NOISE](https://noiseprotocol.org/noise.html) chuẩn cho IK với tên giao thức đã được sửa đổi. Lưu ý rằng chúng tôi sử dụng cùng một bộ khởi tạo cho cả mẫu IK (phiên ràng buộc) và cho mẫu N (phiên không ràng buộc).

Tên giao thức được sửa đổi vì hai lý do. Thứ nhất, để chỉ ra rằng các ephemeral key được mã hóa bằng Elligator2, và thứ hai, để chỉ ra rằng MixHash() được gọi trước thông điệp thứ hai để trộn vào giá trị tag.

```

This is the "e" message pattern:

  // Define protocol_name.
  Set protocol_name = "Noise_IKelg2+hs2_25519_ChaChaPoly_SHA256"
   (40 bytes, US-ASCII encoded, no NULL termination).

  // Define Hash h = 32 bytes
  h = SHA256(protocol_name);

  Define ck = 32 byte chaining key. Copy the h data to ck.
  Set chainKey = h

  // MixHash(null prologue)
  h = SHA256(h);

  // up until here, can all be precalculated by Alice for all outgoing connections

```
### Tải trọng

```

This is the "e" message pattern:

  // Bob's X25519 static keys
  // bpk is published in leaseset
  bsk = GENERATE_PRIVATE()
  bpk = DERIVE_PUBLIC(bsk)

  // Bob static public key
  // MixHash(bpk)
  // || below means append
  h = SHA256(h || bpk);

  // up until here, can all be precalculated by Bob for all incoming connections

  // Alice's X25519 ephemeral keys
  aesk = GENERATE_PRIVATE_ELG2()
  aepk = DERIVE_PUBLIC(aesk)

  // Alice ephemeral public key
  // MixHash(aepk)
  // || below means append
  h = SHA256(h || aepk);

  // h is used as the associated data for the AEAD in the New Session Message
  // Retain the Hash h for the New Session Reply KDF
  // eapk is sent in cleartext in the
  // beginning of the New Session message
  elg2_aepk = ENCODE_ELG2(aepk)
  // As decoded by Bob
  aepk = DECODE_ELG2(elg2_aepk)

  End of "e" message pattern.

  This is the "es" message pattern:

  // Noise es
  sharedSecret = DH(aesk, bpk) = DH(bsk, aepk)

  // MixKey(DH())
  //[chainKey, k] = MixKey(sharedSecret)
  // ChaChaPoly parameters to encrypt/decrypt
  keydata = HKDF(chainKey, sharedSecret, "", 64)
  chainKey = keydata[0:31]

  // AEAD parameters
  k = keydata[32:63]
  n = 0
  ad = h
  ciphertext = ENCRYPT(k, n, flags/static key section, ad)

  End of "es" message pattern.

  This is the "s" message pattern:

  // MixHash(ciphertext)
  // Save for Payload section KDF
  h = SHA256(h || ciphertext)

  // Alice's X25519 static keys
  ask = GENERATE_PRIVATE()
  apk = DERIVE_PUBLIC(ask)

  End of "s" message pattern.


```
### 1f) KDF cho New Session Message

```

This is the "ss" message pattern:

  // Noise ss
  sharedSecret = DH(ask, bpk) = DH(bsk, apk)

  // MixKey(DH())
  //[chainKey, k] = MixKey(sharedSecret)
  // ChaChaPoly parameters to encrypt/decrypt
  // chainKey from Static Key Section
  Set sharedSecret = X25519 DH result
  keydata = HKDF(chainKey, sharedSecret, "", 64)
  chainKey = keydata[0:31]

  // AEAD parameters
  k = keydata[32:63]
  n = 0
  ad = h
  ciphertext = ENCRYPT(k, n, payload, ad)

  End of "ss" message pattern.

  // MixHash(ciphertext)
  // Save for New Session Reply KDF
  h = SHA256(h || ciphertext)

```
### KDF cho ChainKey Ban đầu

Lưu ý rằng đây là một pattern Noise "N", nhưng chúng ta sử dụng cùng một initializer "IK" như đối với các phiên bound.

Các thông điệp New Session không thể được xác định là có chứa static key của Alice hay không cho đến khi static key được giải mã và kiểm tra để xác định xem nó có chứa toàn bộ số không hay không. Do đó, bên nhận phải sử dụng state machine "IK" cho tất cả các thông điệp New Session. Nếu static key là toàn bộ số không, thì message pattern "ss" phải được bỏ qua.

```

chainKey = from Flags/Static key section
  k = from Flags/Static key section
  n = 1
  ad = h from Flags/Static key section
  ciphertext = ENCRYPT(k, n, payload, ad)

```
### KDF cho Nội dung Mã hóa của Phần Flags/Static Key

Một hoặc nhiều New Session Replies có thể được gửi để phản hồi một New Session message duy nhất. Mỗi reply được đặt trước bởi một tag, được tạo ra từ một TagSet cho phiên làm việc.

New Session Reply có hai phần. Phần đầu tiên là việc hoàn thành quá trình bắt tay Noise IK với một thẻ được thêm vào phía trước. Độ dài của phần đầu tiên là 56 byte. Phần thứ hai là payload của giai đoạn dữ liệu. Độ dài của phần thứ hai là 16 + độ dài payload.

Tổng độ dài là 72 + độ dài payload. Định dạng mã hóa:

```

+----+----+----+----+----+----+----+----+
  |       Session Tag   8 bytes           |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Ephemeral Public Key           +
  |                                       |
  +            32 bytes                   +
  |     Encoded with Elligator2           |
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
### KDF cho Phần Payload (với khóa tĩnh của Alice)

Tag được tạo ra trong Session Tags KDF, được khởi tạo trong DH Initialization KDF bên dưới. Điều này liên kết phản hồi với phiên. Session Key từ DH Initialization không được sử dụng.

### KDF cho Phần Payload (không có khóa tĩnh của Alice)

Khóa tạm thời của Bob. Khóa tạm thời có độ dài 32 byte, được mã hóa bằng Elligator2, little endian. Khóa này không bao giờ được tái sử dụng; một khóa mới được tạo với mỗi tin nhắn, bao gồm cả việc truyền lại.

### 1g) Định dạng New Session Reply

Chiều dài được mã hóa là phần còn lại của dữ liệu. Chiều dài được giải mã ngắn hơn chiều dài được mã hóa 16 byte. Payload thường sẽ chứa một hoặc nhiều khối Garlic Clove. Xem phần payload bên dưới để biết định dạng và các yêu cầu bổ sung.

### Thẻ Phiên (Session Tag)

Một hoặc nhiều tag được tạo ra từ TagSet, được khởi tạo bằng cách sử dụng KDF bên dưới, sử dụng chainKey từ thông điệp New Session.

```

// Generate tagset
  tagsetKey = HKDF(chainKey, ZEROLEN, "SessionReplyTags", 32)
  tagset_nsr = DH_INITIALIZE(chainKey, tagsetKey)

```
### Khóa Tạm Thời Phản Hồi Phiên Mới

```

// Keys from the New Session message
  // Alice's X25519 keys
  // apk and aepk are sent in original New Session message
  // ask = Alice private static key
  // apk = Alice public static key
  // aesk = Alice ephemeral private key
  // aepk = Alice ephemeral public key
  // Bob's X25519 static keys
  // bsk = Bob private static key
  // bpk = Bob public static key

  // Generate the tag
  tagsetEntry = tagset_nsr.GET_NEXT_ENTRY()
  tag = tagsetEntry.SESSION_TAG

  // MixHash(tag)
  h = SHA256(h || tag)

  This is the "e" message pattern:

  // Bob's X25519 ephemeral keys
  besk = GENERATE_PRIVATE_ELG2()
  bepk = DERIVE_PUBLIC(besk)

  // Bob's ephemeral public key
  // MixHash(bepk)
  // || below means append
  h = SHA256(h || bepk);

  // elg2_bepk is sent in cleartext in the
  // beginning of the New Session message
  elg2_bepk = ENCODE_ELG2(bepk)
  // As decoded by Bob
  bepk = DECODE_ELG2(elg2_bepk)

  End of "e" message pattern.

  This is the "ee" message pattern:

  // MixKey(DH())
  //[chainKey, k] = MixKey(sharedSecret)
  // ChaChaPoly parameters to encrypt/decrypt
  // chainKey from original New Session Payload Section
  sharedSecret = DH(aesk, bepk) = DH(besk, aepk)
  keydata = HKDF(chainKey, sharedSecret, "", 32)
  chainKey = keydata[0:31]

  End of "ee" message pattern.

  This is the "se" message pattern:

  // MixKey(DH())
  //[chainKey, k] = MixKey(sharedSecret)
  sharedSecret = DH(ask, bepk) = DH(besk, apk)
  keydata = HKDF(chainKey, sharedSecret, "", 64)
  chainKey = keydata[0:31]

  // AEAD parameters
  k = keydata[32:63]
  n = 0
  ad = h
  ciphertext = ENCRYPT(k, n, ZEROLEN, ad)

  End of "se" message pattern.

  // MixHash(ciphertext)
  h = SHA256(h || ciphertext)

  chainKey is used in the ratchet below.

```
### Payload

Điều này giống như thông báo Existing Session đầu tiên, sau khi tách, nhưng không có thẻ riêng biệt. Thêm vào đó, chúng ta sử dụng hash từ trên để liên kết payload với thông báo NSR.

```

// split()
  keydata = HKDF(chainKey, ZEROLEN, "", 64)
  k_ab = keydata[0:31]
  k_ba = keydata[32:63]
  tagset_ab = DH_INITIALIZE(chainKey, k_ab)
  tagset_ba = DH_INITIALIZE(chainKey, k_ba)

  // AEAD parameters for New Session Reply payload
  k = HKDF(k_ba, ZEROLEN, "AttachPayloadKDF", 32)
  n = 0
  ad = h
  ciphertext = ENCRYPT(k, n, payload, ad)
```
### KDF cho Reply TagSet

Nhiều thông điệp NSR có thể được gửi để phản hồi, mỗi thông điệp với các khóa tạm thời duy nhất, tùy thuộc vào kích thước của phản hồi.

Alice và Bob được yêu cầu sử dụng khóa tạm thời mới cho mỗi thông điệp NS và NSR.

Alice phải nhận được một trong những thông điệp NSR của Bob trước khi gửi các thông điệp Existing Session (ES), và Bob phải nhận được một thông điệp ES từ Alice trước khi gửi các thông điệp ES.

``chainKey`` và ``k`` từ NSR Payload Section của Bob được sử dụng làm đầu vào cho các ES DH Ratchets ban đầu (cả hai hướng, xem DH Ratchet KDF).

Bob chỉ được giữ lại các Phiên hiện có (Existing Sessions) cho các thông điệp ES nhận được từ Alice. Bất kỳ phiên inbound và outbound nào khác được tạo ra (cho nhiều NSR) phải được hủy ngay lập tức sau khi nhận được thông điệp ES đầu tiên của Alice cho một phiên nhất định.

### KDF cho Nội dung Được Mã hóa của Phần Reply Key

Session tag (8 bytes) Dữ liệu được mã hóa và MAC (xem mục 3 bên dưới)

### KDF cho Nội dung Mã hóa của Phần Payload

Được mã hóa:

```

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
### Ghi chú

Độ dài được mã hóa là phần còn lại của dữ liệu. Độ dài sau giải mã ít hơn 16 byte so với độ dài được mã hóa. Xem phần payload bên dưới để biết định dạng và yêu cầu.

KDF

```
See AEAD section below.

  // AEAD parameters for Existing Session payload
  k = The 32-byte session key associated with this session tag
  n = The message number N in the current chain, as retrieved from the associated Session Tag.
  ad = The session tag, 8 bytes
  ciphertext = ENCRYPT(k, n, payload, ad)
```
### 1h) Định dạng phiên hiện có

Định dạng: Khóa công khai và khóa riêng tư 32-byte, little-endian.

Lý do: Được sử dụng trong [NTCP2](/docs/specs/ntcp2/).

### Định dạng

Trong các handshake Noise tiêu chuẩn, các thông điệp handshake ban đầu theo mỗi hướng bắt đầu với các ephemeral key được truyền dưới dạng cleartext. Vì các X25519 key hợp lệ có thể phân biệt được với dữ liệu ngẫu nhiên, một kẻ tấn công man-in-the-middle có thể phân biệt các thông điệp này với các thông điệp Existing Session bắt đầu bằng các session tag ngẫu nhiên. Trong [NTCP2](/docs/specs/ntcp2/) ([Proposal 111](/proposals/111-ntcp-2/)), chúng tôi đã sử dụng hàm XOR với overhead thấp sử dụng static key out-of-band để làm mờ key. Tuy nhiên, mô hình đe dọa ở đây là khác; chúng tôi không muốn cho phép bất kỳ MitM nào sử dụng bất kỳ phương tiện nào để xác nhận đích đến của lưu lượng, hoặc để phân biệt các thông điệp handshake ban đầu với các thông điệp Existing Session.

Do đó, [Elligator2](https://elligator.cr.yp.to/) được sử dụng để biến đổi các khóa tạm thời trong các thông điệp New Session và New Session Reply sao cho chúng không thể phân biệt được với các chuỗi ngẫu nhiên đồng nhất.

### Tải trọng

Khóa công khai và khóa riêng tư 32-byte. Các khóa được mã hóa theo định dạng little endian.

Như được định nghĩa trong [Elligator2](https://elligator.cr.yp.to/), các khóa được mã hóa không thể phân biệt được với 254 bit ngẫu nhiên. Chúng ta cần 256 bit ngẫu nhiên (32 byte). Do đó, việc mã hóa và giải mã được định nghĩa như sau:

Mã hóa:

```

ENCODE_ELG2() Definition

  // Encode as defined in Elligator2 specification
  encodedKey = encode(pubkey)
  // OR in 2 random bits to MSB
  randomByte = CSRNG(1)
  encodedKey[31] |= (randomByte & 0xc0)
```
Giải mã:

```

DECODE_ELG2() Definition

  // Mask out 2 random bits from MSB
  encodedKey[31] &= 0x3f
  // Decode as defined in Elligator2 specification
  pubkey = decode(encodedKey)
```
### 2) ECIES-X25519

Cần thiết để ngăn OBEP và IBGW phân loại lưu lượng.

### 2a) Elligator2

Elligator2 làm tăng gấp đôi thời gian tạo khóa trung bình, vì một nửa số private key tạo ra các public key không phù hợp để mã hóa với Elligator2. Ngoài ra, thời gian tạo khóa là không giới hạn với phân phối hàm mũ, vì bộ sinh phải liên tục thử lại cho đến khi tìm được cặp khóa phù hợp.

Chi phí này có thể được quản lý bằng cách thực hiện việc tạo khóa trước, trong một thread riêng biệt, để duy trì một pool các khóa phù hợp.

Generator thực hiện hàm ENCODE_ELG2() để xác định tính phù hợp. Do đó, generator nên lưu trữ kết quả của ENCODE_ELG2() để không phải tính toán lại.

Ngoài ra, các khóa không phù hợp có thể được thêm vào nhóm khóa được sử dụng cho [NTCP2](/docs/specs/ntcp2/), nơi Elligator2 không được sử dụng. Các vấn đề bảo mật khi làm như vậy vẫn chưa được xác định.

### Định dạng

AEAD sử dụng ChaCha20 và Poly1305, giống như trong [NTCP2](/docs/specs/ntcp2/). Điều này tương ứng với [RFC-7539](https://tools.ietf.org/html/rfc7539), cũng được sử dụng tương tự trong TLS [RFC-7905](https://tools.ietf.org/html/rfc7905).

### Lý do chính đáng

Đầu vào cho các hàm mã hóa/giải mã cho một khối AEAD trong thông điệp New Session:

```

k :: 32 byte cipher key
       See New Session and New Session Reply KDFs above.

  n :: Counter-based nonce, 12 bytes.
       n = 0

  ad :: Associated data, 32 bytes.
        The SHA256 hash of the preceding data, as output from mixHash()

  data :: Plaintext data, 0 or more bytes

```
### Ghi chú

Đầu vào cho các hàm mã hóa/giải mã cho một khối AEAD trong thông điệp Existing Session:

```

k :: 32 byte session key
       As looked up from the accompanying session tag.

  n :: Counter-based nonce, 12 bytes.
       Starts at 0 and incremented for each message when transmitting.
       For the receiver, the value
       as looked up from the accompanying session tag.
       First four bytes are always zero.
       Last eight bytes are the message number (n), little-endian encoded.
       Maximum value is 65535.
       Session must be ratcheted when N reaches that value.
       Higher values must never be used.

  ad :: Associated data
        The session tag

  data :: Plaintext data, 0 or more bytes

```
### 3) AEAD (ChaChaPoly)

Đầu ra của hàm mã hóa, đầu vào của hàm giải mã:

```

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
### Đầu vào New Session và New Session Reply

- Vì ChaCha20 là một stream cipher, plaintexts không cần được padding.
  Các byte keystream bổ sung sẽ bị loại bỏ.

- Khóa cho thuật toán mã hóa (256 bits) được thỏa thuận thông qua SHA256 KDF.
  Chi tiết của KDF cho mỗi thông điệp được trình bày trong các phần riêng biệt bên dưới.

- Các frame ChaChaPoly có kích thước đã biết vì chúng được đóng gói trong thông điệp dữ liệu I2NP.

- Đối với tất cả các thông điệp,
  padding nằm bên trong khung dữ liệu
  được xác thực.

### Đầu Vào Phiên Hiện Có

Tất cả dữ liệu nhận được mà không vượt qua được xác minh AEAD phải được loại bỏ. Không có phản hồi nào được trả về.

### Định dạng mã hóa

Được sử dụng trong [NTCP2](/docs/specs/ntcp2/).

### Ghi chú

Chúng tôi vẫn sử dụng session tags như trước, nhưng chúng tôi dùng ratchets để tạo ra chúng. Session tags cũng có tùy chọn rekey mà chúng tôi chưa bao giờ triển khai. Vậy nên nó giống như double ratchet nhưng chúng tôi chưa bao giờ thực hiện cái thứ hai.

Ở đây chúng ta định nghĩa thứ gì đó tương tự như Double Ratchet của Signal. Các session tag được tạo ra một cách xác định và giống hệt nhau ở phía người nhận và người gửi.

Bằng cách sử dụng symmetric key/tag ratchet, chúng ta loại bỏ việc sử dụng bộ nhớ để lưu trữ session tags ở phía người gửi. Chúng ta cũng loại bỏ việc tiêu thụ băng thông khi gửi tag sets. Việc sử dụng ở phía người nhận vẫn đáng kể, nhưng chúng ta có thể giảm thiểu hơn nữa khi chúng ta thu nhỏ session tag từ 32 bytes xuống 8 bytes.

Chúng tôi không sử dụng mã hóa header như được quy định (và tùy chọn) trong Signal, thay vào đó chúng tôi sử dụng session tags.

Bằng cách sử dụng DH ratchet, chúng ta đạt được tính bảo mật tiến (forward secrecy), điều mà không bao giờ được triển khai trong ElGamal/AES+SessionTags.

Lưu ý: Khóa công khai một lần New Session không phải là một phần của ratchet, chức năng duy nhất của nó là mã hóa khóa DH ratchet ban đầu của Alice.

### Xử Lý Lỗi AEAD

Double Ratchet xử lý các thông điệp bị mất hoặc không theo thứ tự bằng cách bao gồm một tag trong mỗi header thông điệp. Bên nhận tra cứu chỉ số của tag, đây là số thông điệp N. Nếu thông điệp chứa một khối Message Number với giá trị PN, bên nhận có thể xóa bất kỳ tag nào cao hơn giá trị đó trong tập tag trước đó, đồng thời giữ lại các tag bị bỏ qua từ tập tag trước đó trong trường hợp các thông điệp bị bỏ qua đến sau này.

### Lý do chính đáng

Chúng ta định nghĩa các cấu trúc dữ liệu và hàm sau để triển khai các ratchet này.

TAGSET_ENTRY

    A single entry in a TAGSET.

    INDEX
        An integer index, starting with 0

    SESSION_TAG
        An identifier to go out on the wire, 8 bytes

    SESSION_KEY
        A symmetric key, never goes on the wire, 32 bytes

TAGSET

    A collection of TAGSET_ENTRIES.

    CREATE(key, n)
        Generate a new TAGSET using initial cryptographic key material of 32 bytes.
        The associated session identifier is provided.
        The initial number of of tags to create is specified; this is generally 0 or 1
        for an outgoing session.
        LAST_INDEX = -1
        EXTEND(n) is called.

    EXTEND(n)
        Generate n more TAGSET_ENTRIES by calling EXTEND() n times.

    EXTEND()
        Generate one more TAGSET_ENTRY, unless the maximum number SESSION_TAGS have
        already been generated.
        If LAST_INDEX is greater than or equal to 65535, return.
        ++ LAST_INDEX
        Create a new TAGSET_ENTRY with the LAST_INDEX value and the calculated SESSION_TAG.
        Calls RATCHET_TAG() and (optionally) RATCHET_KEY().
        For inbound sessions, the calculation of the SESSION_KEY may
        be deferred and calculated in GET_SESSION_KEY().
        Calls EXPIRE()

    EXPIRE()
        Remove tags and keys that are too old, or if the TAGSET size exceeds some limit.

    RATCHET_TAG()
        Calculates the next SESSION_TAG based on the last SESSION_TAG.

    RATCHET_KEY()
        Calculates the next SESSION_KEY based on the last SESSION_KEY.

    SESSION
        The associated session.

    CREATION_TIME
        When the TAGSET was created.

    LAST_INDEX
        The last TAGSET_ENTRY INDEX generated by EXTEND().

    GET_NEXT_ENTRY()
        Used for outgoing sessions only.
        EXTEND(1) is called if there are no remaining TAGSET_ENTRIES.
        If EXTEND(1) did nothing, the max of 65535 TAGSETS have been used,
        and return an error.
        Returns the next unused TAGSET_ENTRY.

    GET_SESSION_KEY(sessionTag)
        Used for incoming sessions only.
        Returns the TAGSET_ENTRY containing the sessionTag.
        If found, the TAGSET_ENTRY is removed.
        If the SESSION_KEY calculation was deferred, it is calculated now.
        If there are few TAGSET_ENTRIES remaining, EXTEND(n) is called.


### 4) Ratchets

Ratchets nhưng không nhanh gần bằng Signal. Chúng tôi tách việc xác nhận khóa đã nhận khỏi việc tạo khóa mới. Trong sử dụng thông thường, Alice và Bob sẽ mỗi người ratchet (hai lần) ngay lập tức trong New Session, nhưng sẽ không ratchet nữa.

Lưu ý rằng một ratchet dành cho một hướng duy nhất, và tạo ra chuỗi ratchet New Session tag / message key cho hướng đó. Để tạo ra các key cho cả hai hướng, bạn phải thực hiện ratchet hai lần.

Bạn ratchet mỗi khi tạo và gửi một khóa mới. Bạn ratchet mỗi khi nhận một khóa mới.

Alice thực hiện ratchet một lần khi tạo phiên gửi đi không ràng buộc, cô ấy không tạo phiên nhận vào (không ràng buộc có nghĩa là không thể trả lời).

Bob thực hiện ratchet một lần khi tạo phiên inbound không ràng buộc, và không tạo phiên outbound tương ứng (không ràng buộc nghĩa là không thể trả lời).

Alice tiếp tục gửi các thông điệp New Session (NS) đến Bob cho đến khi nhận được một trong các thông điệp New Session Reply (NSR) của Bob. Sau đó cô ấy sử dụng kết quả KDF của Payload Section từ NSR làm đầu vào cho các session ratchet (xem DH Ratchet KDF), và bắt đầu gửi các thông điệp Existing Session (ES).

Với mỗi thông điệp NS nhận được, Bob tạo một phiên kết nối đến mới, sử dụng kết quả KDF từ Payload Section phản hồi làm đầu vào cho ES DH Ratchet đến và đi mới.

Đối với mỗi phản hồi cần thiết, Bob gửi Alice một thông điệp NSR với phản hồi trong payload. Yêu cầu Bob phải sử dụng các khóa ephemeral mới cho mỗi NSR.

Bob phải nhận được một thông điệp ES từ Alice trên một trong các phiên inbound, trước khi tạo và gửi các thông điệp ES trên phiên outbound tương ứng.

Alice nên sử dụng bộ đếm thời gian để nhận tin nhắn NSR từ Bob. Nếu bộ đếm thời gian hết hạn, phiên làm việc nên được loại bỏ.

Để tránh tấn công KCI và/hoặc cạn kiệt tài nguyên, nơi kẻ tấn công loại bỏ các phản hồi NSR của Bob để khiến Alice tiếp tục gửi tin nhắn NS, Alice nên tránh khởi tạo New Sessions với Bob sau một số lần thử lại nhất định do hết thời gian chờ.

Alice và Bob mỗi người thực hiện một ratchet DH cho mỗi khối NextKey được nhận.

Alice và Bob mỗi người tạo ra các ratchet bộ tag mới và hai ratchet khóa đối xứng sau mỗi DH ratchet. Đối với mỗi thông điệp ES mới theo một hướng nhất định, Alice và Bob tiến hành ratchet tag phiên và ratchet khóa đối xứng.

Tần suất thực hiện DH ratchets sau quá trình bắt tay ban đầu phụ thuộc vào cách triển khai. Trong khi giao thức đặt giới hạn 65535 tin nhắn trước khi yêu cầu một ratchet, việc thực hiện ratcheting thường xuyên hơn (dựa trên số lượng tin nhắn, thời gian đã trôi qua, hoặc cả hai) có thể cung cấp thêm bảo mật.

Sau KDF handshake cuối cùng trên các phiên bound, Bob và Alice phải chạy hàm Noise Split() trên CipherState kết quả để tạo các khóa chuỗi đối xứng và tag độc lập cho các phiên inbound và outbound.

#### KEY AND TAG SET IDS

Số ID của key và tag set được sử dụng để xác định các key và tag set. Key ID được sử dụng trong các khối NextKey để xác định key được gửi hoặc sử dụng. Tag set ID được sử dụng (cùng với số thứ tự thông điệp) trong các khối ACK để xác định thông điệp đang được xác nhận. Cả key ID và tag set ID đều áp dụng cho các tag set theo một hướng duy nhất. Số ID của key và tag set phải tuần tự.

Trong các bộ tag đầu tiên được sử dụng cho một phiên trong mỗi hướng, ID của bộ tag là 0. Không có khối NextKey nào được gửi, vì vậy không có ID khóa nào.

Để bắt đầu một DH ratchet, bên gửi truyền một khối NextKey mới với key ID là 0. Bên nhận phản hồi bằng một khối NextKey mới với key ID là 0. Sau đó bên gửi bắt đầu sử dụng một tag set mới với tag set ID là 1.

Các tag set tiếp theo được tạo ra theo cách tương tự. Đối với tất cả tag set được sử dụng sau khi trao đổi NextKey, số tag set là (1 + key ID của Alice + key ID của Bob).

ID của key và tag set bắt đầu từ 0 và tăng dần theo thứ tự. ID tag set tối đa là 65535. ID key tối đa là 32767. Khi một tag set gần cạn kiệt, bên gửi tag set phải khởi tạo trao đổi NextKey. Khi tag set 65535 gần cạn kiệt, bên gửi tag set phải khởi tạo một session mới bằng cách gửi thông điệp New Session.

Với kích thước thông điệp tối đa khi streaming là 1730, và giả sử không có retransmission, tốc độ truyền dữ liệu tối đa theo lý thuyết khi sử dụng một tag set duy nhất là 1730 * 65536 ~= 108 MB. Tốc độ tối đa thực tế sẽ thấp hơn do các retransmission.

Lượng dữ liệu truyền tải tối đa về mặt lý thuyết với tất cả 65536 bộ tag khả dụng, trước khi phiên làm việc phải được loại bỏ và thay thế, là 64K * 108 MB ~= 6.9 TB.

#### DH RATCHET MESSAGE FLOW

Việc trao đổi khóa tiếp theo cho một tag set phải được khởi tạo bởi người gửi của những tag đó (chủ sở hữu của outbound tag set). Người nhận (chủ sở hữu của inbound tag set) sẽ phản hồi. Đối với lưu lượng HTTP GET điển hình ở tầng ứng dụng, Bob sẽ gửi nhiều thông điệp hơn và sẽ ratchet trước bằng cách khởi tạo việc trao đổi khóa; sơ đồ bên dưới cho thấy điều đó. Khi Alice thực hiện ratchet, điều tương tự sẽ xảy ra theo chiều ngược lại.

Bộ tag đầu tiên được sử dụng sau quá trình bắt tay NS/NSR là bộ tag 0. Khi bộ tag 0 gần cạn kiệt, các khóa mới phải được trao đổi theo cả hai hướng để tạo ra bộ tag 1. Sau đó, khóa mới chỉ được gửi theo một hướng.

Để tạo tag set 2, bên gửi tag sẽ gửi một key mới và bên nhận tag sẽ gửi ID của key cũ như một xác nhận. Cả hai bên đều thực hiện một DH.

Để tạo tag set 3, bên gửi tag sẽ gửi ID của khóa cũ và yêu cầu khóa mới từ bên nhận tag. Cả hai bên đều thực hiện DH.

Các tập thẻ tiếp theo được tạo ra giống như đối với tập thẻ 2 và 3. Số thứ tự tập thẻ là (1 + sender key id + receiver key id).

```

Tag Sender                    Tag Receiver

                   ... use tag set #0 ...


  (Tagset #0 almost empty)
  (generate new key #0)

  Next Key, forward, request reverse, with key #0  -------->
  (repeat until next key received)

                              (generate new key #0, do DH, create IB Tagset #1)

          <-------------      Next Key, reverse, with key #0
                              (repeat until tag received on new tagset)

  (do DH, create OB Tagset #1)


                   ... use tag set #1 ...


  (Tagset #1 almost empty)
  (generate new key #1)

  Next Key, forward, with key #1        -------->
  (repeat until next key received)

                              (reuse key #0, do DH, create IB Tagset #2)

          <--------------     Next Key, reverse, id 0
                              (repeat until tag received on new tagset)

  (do DH, create OB Tagset #2)


                   ... use tag set #2 ...


  (Tagset #2 almost empty)
  (reuse key #1)

  Next Key, forward, request reverse, id 1  -------->
  (repeat until next key received)

                              (generate new key #1, do DH, create IB Tagset #3)

          <--------------     Next Key, reverse, with key #1

  (do DH, create OB Tagset #3)
  (reuse key #1, do DH, create IB Tagset #3)


                   ... use tag set #3 ...


       After tag set 3, repeat the above
       patterns as shown for tag sets 2 and 3.

       To create a new even-numbered tag set, the sender sends a new key
       to the receiver. The receiver sends his old key ID
       back as an acknowledgement.

       To create a new odd-numbered tag set, the sender sends a reverse request
       to the receiver. The receiver sends a new reverse key to the sender.

```
Sau khi DH ratchet hoàn thành cho một outbound tagset, và một outbound tagset mới được tạo, nó nên được sử dụng ngay lập tức, và outbound tagset cũ có thể được xóa.

Sau khi DH ratchet hoàn tất cho một inbound tagset, và một inbound tagset mới được tạo, bên nhận nên lắng nghe các tag trong cả hai tagset, và xóa tagset cũ sau một thời gian ngắn, khoảng 3 phút.

Tóm tắt về tiến trình tag set và key ID được trình bày trong bảng dưới đây. * biểu thị rằng một key mới được tạo ra.

| New Tag Set ID | Sender key ID | Rcvr key ID |
|----------------|---------------|-------------|
| 0              | n/a           | n/a         |
| 1              | 0 *           | 0 *         |
| 2              | 1 *           | 0           |
| 3              | 1             | 1 *         |
| 4              | 2 *           | 1           |
| 5              | 2             | 2 *         |
| ...            | ...           | ...         |
| 65534          | 32767 *       | 32766       |
| 65535          | 32767         | 32767 *     |
Các số ID của key và tag set phải tuần tự.

#### DH INITIALIZATION KDF

Đây là định nghĩa của DH_INITIALIZE(rootKey, k) cho một hướng đơn. Nó tạo ra một tagset và một "root key tiếp theo" để sử dụng cho một DH ratchet tiếp theo nếu cần thiết.

Chúng tôi sử dụng khởi tạo DH ở ba vị trí. Đầu tiên, chúng tôi sử dụng nó để tạo ra một tag set cho New Session Replies. Thứ hai, chúng tôi sử dụng nó để tạo ra hai tag set, một cho mỗi hướng, để sử dụng trong các thông điệp Existing Session. Cuối cùng, chúng tôi sử dụng nó sau một DH Ratchet để tạo ra một tag set mới theo một hướng duy nhất cho các thông điệp Existing Session bổ sung.

```

Inputs:
  1) rootKey = chainKey from Payload Section
  2) k from the New Session KDF or split()

  // KDF_RK(rk, dh_out)
  keydata = HKDF(rootKey, k, "KDFDHRatchetStep", 64)

  // Output 1: The next Root Key (KDF input for the next DH ratchet)
  nextRootKey = keydata[0:31]
  // Output 2: The chain key to initialize the new
  // session tag and symmetric key ratchets
  // for the tag set
  ck = keydata[32:63]

  // session tag and symmetric key chain keys
  keydata = HKDF(ck, ZEROLEN, "TagAndKeyGenKeys", 64)
  sessTag_ck = keydata[0:31]
  symmKey_ck = keydata[32:63]

```
#### DH RATCHET KDF

Điều này được sử dụng sau khi các khóa DH mới được trao đổi trong các NextKey block, trước khi một tagset bị cạn kiệt.

```


// Tag sender generates new X25519 ephemeral keys
  // and sends rapk to tag receiver in a NextKey block
  rask = GENERATE_PRIVATE()
  rapk = DERIVE_PUBLIC(rask)
  
  // Tag receiver generates new X25519 ephemeral keys
  // and sends rbpk to Tag sender in a NextKey block
  rbsk = GENERATE_PRIVATE()
  rbpk = DERIVE_PUBLIC(rbsk)

  sharedSecret = DH(rask, rbpk) = DH(rbsk, rapk)
  tagsetKey = HKDF(sharedSecret, ZEROLEN, "XDHRatchetTagSet", 32)
  rootKey = nextRootKey // from previous tagset in this direction
  newTagSet = DH_INITIALIZE(rootKey, tagsetKey)

```
### Số Thứ Tự Tin Nhắn

Ratchet cho mỗi tin nhắn, như trong Signal. Ratchet thẻ phiên được đồng bộ hóa với ratchet khóa đối xứng, nhưng ratchet khóa người nhận có thể "chậm lại phía sau" để tiết kiệm bộ nhớ.

Transmitter ratchets một lần cho mỗi tin nhắn được truyền đi. Không cần lưu trữ thêm thẻ nào. Transmitter cũng phải giữ một bộ đếm cho 'N', số thứ tự tin nhắn của tin nhắn trong chuỗi hiện tại. Giá trị 'N' được bao gồm trong tin nhắn được gửi. Xem định nghĩa khối Message Number.

Người nhận phải ratchet tiến lên bằng kích thước cửa sổ tối đa và lưu trữ các tag trong một "tag set", được liên kết với session. Một khi đã nhận được, tag đã lưu trữ có thể được loại bỏ, và nếu không có tag nào trước đó chưa được nhận, cửa sổ có thể được tiến lên. Người nhận nên giữ giá trị 'N' liên kết với mỗi session tag, và kiểm tra rằng số trong thông điệp được gửi khớp với giá trị này. Xem định nghĩa khối Message Number.

#### KDF

Đây là định nghĩa của RATCHET_TAG().

```

Inputs:
  1) Session Tag Chain key sessTag_ck
     First time: output from DH ratchet
     Subsequent times: output from previous session tag ratchet

  Generated:
  2) input_key_material = SESSTAG_CONSTANT
     Must be unique for this tag set (generated from chain key),
     so that the sequence isn't predictable, since session tags
     go out on the wire in plaintext.

  Outputs:
  1) N (the current session tag number)
  2) the session tag (and symmetric key, probably)
  3) the next Session Tag Chain Key (KDF input for the next session tag ratchet)

  Initialization:
  keydata = HKDF(sessTag_ck, ZEROLEN, "STInitialization", 64)
  // Output 1: Next chain key
  sessTag_chainKey = keydata[0:31]
  // Output 2: The constant
  SESSTAG_CONSTANT = keydata[32:63]

  // KDF_ST(ck, constant)
  keydata_0 = HKDF(sessTag_chainkey, SESSTAG_CONSTANT, "SessionTagKeyGen", 64)
  // Output 1: Next chain key
  sessTag_chainKey_0 = keydata_0[0:31]
  // Output 2: The session tag
  // or more if tag is longer than 8 bytes
  tag_0 = keydata_0[32:39]

  // repeat as necessary to get to tag_n
  keydata_n = HKDF(sessTag_chainKey_(n-1), SESSTAG_CONSTANT, "SessionTagKeyGen", 64)
  // Output 1: Next chain key
  sessTag_chainKey_n = keydata_n[0:31]
  // Output 2: The session tag
  // or more if tag is longer than 8 bytes
  tag_n = keydata_n[32:39]

```
### Triển khai Mẫu

Ratchets cho mỗi tin nhắn, như trong Signal. Mỗi khóa đối xứng có một số thứ tự tin nhắn và session tag liên quan. Session key ratchet được đồng bộ hóa với symmetric tag ratchet, nhưng receiver key ratchet có thể "tụt lại phía sau" để tiết kiệm bộ nhớ.

Transmitter ratchet một lần cho mỗi thông điệp được truyền. Không cần lưu trữ thêm khóa nào khác.

Khi bên nhận nhận được một session tag, nếu nó chưa ratchet khóa đối xứng tới khóa liên quan, nó phải "bắt kịp" đến khóa liên quan đó. Bên nhận có thể sẽ cache các khóa cho bất kỳ tag trước đó nào chưa được nhận. Một khi đã nhận được, khóa đã lưu trữ có thể bị loại bỏ, và nếu không có tag trước đó nào chưa nhận, cửa sổ có thể được tiến lên.

Để đạt hiệu quả, session tag và symmetric key ratchets được tách biệt để session tag ratchet có thể chạy trước symmetric key ratchet. Điều này cũng cung cấp thêm bảo mật, vì các session tags được truyền qua mạng.

#### KDF

Đây là định nghĩa của RATCHET_KEY().

```

Inputs:
  1) Symmetric Key Chain key symmKey_ck
     First time: output from DH ratchet
     Subsequent times: output from previous symmetric key ratchet

  Generated:
  2) input_key_material = SYMMKEY_CONSTANT = ZEROLEN
     No need for uniqueness. Symmetric keys never go out on the wire.
     TODO: Set a constant anyway?

  Outputs:
  1) N (the current session key number)
  2) the session key
  3) the next Symmetric Key Chain Key (KDF input for the next symmetric key ratchet)

  // KDF_CK(ck, constant)
  SYMMKEY_CONSTANT = ZEROLEN
  // Output 1: Next chain key
  keydata_0 = HKDF(symmKey_ck, SYMMKEY_CONSTANT, "SymmetricRatchet", 64)
  symmKey_chainKey_0 = keydata_0[0:31]
  // Output 2: The symmetric key
  k_0 = keydata_0[32:63]

  // repeat as necessary to get to k[n]
  keydata_n = HKDF(symmKey_chainKey_(n-1), SYMMKEY_CONSTANT, "SymmetricRatchet", 64)
  // Output 1: Next chain key
  symmKey_chainKey_n = keydata_n[0:31]
  // Output 2: The symmetric key
  k_n = keydata_n[32:63]


```
### 4a) DH Ratchet

Điều này thay thế định dạng phần AES được định nghĩa trong đặc tả ElGamal/AES+SessionTags.

Điều này sử dụng cùng định dạng khối như đã định nghĩa trong đặc tả [NTCP2](/docs/specs/ntcp2/). Các loại khối riêng lẻ được định nghĩa khác nhau.

Có những lo ngại rằng việc khuyến khích các nhà phát triển chia sẻ mã nguồn có thể dẫn đến các vấn đề phân tích cú pháp. Các nhà phát triển nên cân nhắc cẩn thận những lợi ích và rủi ro của việc chia sẻ mã nguồn, và đảm bảo rằng các quy tắc thứ tự và block hợp lệ khác nhau cho hai ngữ cảnh.

### Payload Section Decrypted data

Độ dài được mã hóa là phần còn lại của dữ liệu. Độ dài được giải mã ít hơn độ dài được mã hóa 16 byte. Tất cả các loại block đều được hỗ trợ. Nội dung điển hình bao gồm các block sau:

| Payload Block Type | Type Number | Block Length |
|--------------------|-------------|--------------|
| DateTime           | 0           | 7            |
| Termination (TBD)  | 4           | 9 typ.       |
| Options (TBD)      | 5           | 21+          |
| Message Number (TBD) | 6           | TBD          |
| Next Key           | 7           | 3 or 35      |
| ACK                | 8           | 4 typ.       |
| ACK Request        | 9           | 3            |
| Garlic Clove       | 11          | varies       |
| Padding            | 254         | varies       |
### Unencrypted data

Có thể có không hoặc nhiều block trong khung được mã hóa. Mỗi block chứa một định danh một byte, một độ dài hai byte, và không hoặc nhiều byte dữ liệu.

Để có thể mở rộng, các receiver PHẢI bỏ qua các block có số loại không xác định và xử lý chúng như padding.

Dữ liệu được mã hóa có tối đa 65535 byte, bao gồm một header xác thực 16-byte, vì vậy dữ liệu chưa mã hóa tối đa là 65519 byte.

(Thẻ xác thực Poly1305 không được hiển thị):

```

+----+----+----+----+----+----+----+----+
  |blk |  size   |       data             |
  +----+----+----+                        +
  |                                       |
  ~               .   .   .               ~
  |                                       |
  +----+----+----+----+----+----+----+----+
  |blk |  size   |       data             |
  +----+----+----+                        +
  |                                       |
  ~               .   .   .               ~
  |                                       |
  +----+----+----+----+----+----+----+----+
  ~               .   .   .               ~

  blk :: 1 byte
         0 datetime
         1-3 reserved
         4 termination
         5 options
         6 previous message number
         7 next session key
         8 ack
         9 ack request
         10 reserved
         11 Garlic Clove
         224-253 reserved for experimental features
         254 for padding
         255 reserved for future extension
  size :: 2 bytes, big endian, size of data to follow, 0 - 65516
  data :: the data

  Maximum ChaChaPoly frame is 65535 bytes.
  Poly1305 tag is 16 bytes
  Maximum total block size is 65519 bytes
  Maximum single block size is 65519 bytes
  Block type is 1 byte
  Block length is 2 bytes
  Maximum single block data size is 65516 bytes.

```
### Block Ordering Rules

Trong thông điệp New Session, khối DateTime là bắt buộc và phải là khối đầu tiên.

Các khối được phép khác:

- Garlic Clove (loại 11)
- Options (loại 5)
- Padding (loại 254)

Trong thông điệp New Session Reply, không có block nào được yêu cầu.

Các khối được phép khác:

- Garlic Clove (loại 11)
- Options (loại 5)
- Padding (loại 254)

Không có block nào khác được phép. Padding, nếu có, phải là block cuối cùng.

Trong thông điệp Existing Session, không cần có khối nào, và thứ tự không được chỉ định, ngoại trừ các yêu cầu sau:

Termination, nếu có, phải là khối cuối cùng ngoại trừ Padding. Padding, nếu có, phải là khối cuối cùng.

Có thể có nhiều khối Garlic Clove trong một frame duy nhất. Có thể có tối đa hai khối Next Key trong một frame duy nhất. Không cho phép nhiều khối Padding trong một frame duy nhất. Các loại khối khác có thể sẽ không có nhiều khối trong một frame duy nhất, nhưng điều này không bị cấm.

### DateTime

Một thời hạn hết hiệu lực. Hỗ trợ trong việc ngăn chặn phản hồi. Bob phải xác thực rằng thông điệp là gần đây, sử dụng timestamp này. Bob phải triển khai bộ lọc Bloom hoặc cơ chế khác để ngăn chặn các cuộc tấn công replay, nếu thời gian hợp lệ. Thường chỉ được bao gồm trong các thông điệp New Session.

```

+----+----+----+----+----+----+----+
  | 0  |    4    |     timestamp     |
  +----+----+----+----+----+----+----+

  blk :: 0
  size :: 2 bytes, big endian, value = 4
  timestamp :: Unix timestamp, unsigned seconds.
               Wraps around in 2106

```
### 4b) Session Tag Ratchet

Một Garlic Clove đã được giải mã duy nhất như được chỉ định trong [I2NP](/docs/specs/i2np/), với các sửa đổi để loại bỏ các trường không được sử dụng hoặc dư thừa. Cảnh báo: Định dạng này khác biệt đáng kể so với định dạng dành cho ElGamal/AES. Mỗi clove là một khối payload riêng biệt. Garlic Cloves có thể không được phân mảnh qua các khối hoặc qua các khung ChaChaPoly.

```

+----+----+----+----+----+----+----+----+
  | 11 |  size   |                        |
  +----+----+----+                        +
  |      Delivery Instructions            |
  ~                                       ~
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+
  |type|  Message_ID       | Expiration   
  +----+----+----+----+----+----+----+----+
       |      I2NP Message body           |
  +----+                                  +
  ~                                       ~
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+

  size :: size of all data to follow

  Delivery Instructions :: As specified in
         the Garlic Clove section of [I2NP](/docs/specs/i2np/).
         Length varies but is typically 1, 33, or 37 bytes

  type :: I2NP message type

  Message_ID :: 4 byte `Integer` I2NP message ID

  Expiration :: 4 bytes, seconds since the epoch

```
Ghi chú:

- Các nhà phát triển phải đảm bảo rằng khi đọc một block,
  dữ liệu bị lỗi hoặc độc hại sẽ không khiến việc đọc
  vượt quá giới hạn sang block tiếp theo.

- Định dạng Clove Set được chỉ định trong [I2NP](/docs/specs/i2np/) không được sử dụng.
  Mỗi clove được chứa trong block riêng của nó.

- Header tin nhắn I2NP có kích thước 9 byte, với định dạng giống hệt
  như được sử dụng trong [NTCP2](/docs/specs/ntcp2/).

- Certificate, Message ID, và Expiration từ định nghĩa
  Garlic Message trong [I2NP](/docs/specs/i2np/) không được bao gồm.

- Certificate, Clove ID, và Expiration từ định nghĩa
  Garlic Clove trong [I2NP](/docs/specs/i2np/) không được bao gồm.

Lý do chính đáng:

- Các certificate chưa bao giờ được sử dụng.
- ID tin nhắn riêng biệt và ID clove riêng biệt chưa bao giờ được sử dụng.
- Các thời hạn riêng biệt chưa bao giờ được sử dụng.
- Lượng tiết kiệm tổng thể so với định dạng Clove Set và Clove cũ
  là khoảng 35 byte cho 1 clove, 54 byte cho 2 clove,
  và 73 byte cho 3 clove.
- Định dạng block có thể mở rộng và bất kỳ trường mới nào có thể được thêm
  dưới dạng các loại block mới.

### Termination

Việc triển khai là tùy chọn. Hủy bỏ phiên làm việc. Đây phải là khối không phải padding cuối cùng trong frame. Không có thêm thông điệp nào sẽ được gửi trong phiên làm việc này.

Không được phép trong NS hoặc NSR. Chỉ được bao gồm trong các thông điệp Existing Session.

```

+----+----+----+----+----+----+----+----+
  | 4  |  size   | rsn|     addl data     |
  +----+----+----+----+                   +
  ~               .   .   .               ~
  +----+----+----+----+----+----+----+----+

  blk :: 4
  size :: 2 bytes, big endian, value = 1 or more
  rsn :: reason, 1 byte:
         0: normal close or unspecified
         1: termination received
         others: optional, impementation-specific
  addl data :: optional, 0 or more bytes, for future expansion, debugging,
               or reason text.
               Format unspecified and may vary based on reason code.

```
### 4c) Symmetric Key Ratchet (Cơ chế xoay khóa đối xứng)

CHƯA TRIỂN KHAI, để nghiên cứu thêm. Truyền các tùy chọn đã cập nhật. Các tùy chọn bao gồm nhiều tham số khác nhau cho phiên làm việc. Xem phần Session Tag Length Analysis bên dưới để biết thêm thông tin.

Khối options có thể có độ dài thay đổi, vì more_options có thể có mặt.

```

+----+----+----+----+----+----+----+----+
  | 5  |  size   |ver |flg |STL |STimeout |
  +----+----+----+----+----+----+----+----+
  |  SOTW   |  RITW   |tmin|tmax|rmin|rmax|
  +----+----+----+----+----+----+----+----+
  |  tdmy   |  rdmy   |  tdelay |  rdelay |
  +----+----+----+----+----+----+----+----+
  |              more_options             |
  ~               .   .   .               ~
  |                                       |
  +----+----+----+----+----+----+----+----+

  blk :: 5
  size :: 2 bytes, big endian, size of options to follow, 21 bytes minimum
  ver :: Protocol version, must be 0
  flg :: 1 byte flags
         bits 7-0: Unused, set to 0 for future compatibility
  STL :: Session tag length (must be 8), other values unimplemented
  STimeout :: Session idle timeout (seconds), big endian
  SOTW :: Sender Outbound Tag Window, 2 bytes big endian
  RITW :: Receiver Inbound Tag Window 2 bytes big endian

  tmin, tmax, rmin, rmax :: requested padding limits
      tmin and rmin are for desired resistance to traffic analysis.
      tmax and rmax are for bandwidth limits.
      tmin and tmax are the transmit limits for the router sending this options block.
      rmin and rmax are the receive limits for the router sending this options block.
      Each is a 4.4 fixed-point float representing 0 to 15.9375
      (or think of it as an unsigned 8-bit integer divided by 16.0).
      This is the ratio of padding to data. Examples:
      Value of 0x00 means no padding
      Value of 0x01 means add 6 percent padding
      Value of 0x10 means add 100 percent padding
      Value of 0x80 means add 800 percent (8x) padding
      Alice and Bob will negotiate the minimum and maximum in each direction.
      These are guidelines, there is no enforcement.
      Sender should honor receiver's maximum.
      Sender may or may not honor receiver's minimum, within bandwidth constraints.

  tdmy: Max dummy traffic willing to send, 2 bytes big endian, bytes/sec average
  rdmy: Requested dummy traffic, 2 bytes big endian, bytes/sec average
  tdelay: Max intra-message delay willing to insert, 2 bytes big endian, msec average
  rdelay: Requested intra-message delay, 2 bytes big endian, msec average

  more_options :: Format undefined, for future use

```
SOTW là khuyến nghị của bên gửi cho bên nhận về cửa sổ tag đầu vào của bên nhận (lookahead tối đa). RITW là tuyên bố của bên gửi về cửa sổ tag đầu vào (lookahead tối đa) mà họ dự định sử dụng. Mỗi bên sau đó sẽ thiết lập hoặc điều chỉnh lookahead dựa trên một số giá trị tối thiểu hoặc tối đa hoặc tính toán khác.

Ghi chú:

- Hỗ trợ cho độ dài session tag không mặc định hy vọng
  sẽ không bao giờ được yêu cầu.
- Tag window là MAX_SKIP trong tài liệu Signal.

Các vấn đề:

- Việc thương lượng các tùy chọn vẫn đang được xác định.
- Các giá trị mặc định vẫn đang được xác định.
- Các tùy chọn padding và delay được sao chép từ NTCP2,
  nhưng những tùy chọn đó vẫn chưa được triển khai đầy đủ hoặc nghiên cứu ở đó.

### Message Numbers

Việc triển khai là tùy chọn. Độ dài (số lượng tin nhắn được gửi) trong tập thẻ trước đó (PN). Người nhận có thể xóa ngay lập tức các thẻ cao hơn PN từ tập thẻ trước đó. Người nhận có thể hết hạn các thẻ nhỏ hơn hoặc bằng PN từ tập thẻ trước đó sau một thời gian ngắn (ví dụ: 2 phút).

```

+----+----+----+----+----+
  | 6  |  size   |  PN    |
 +----+----+----+----+----+

  blk :: 6
  size :: 2
  PN :: 2 bytes big endian. The index of the last tag sent in the previous tag set.

```
Ghi chú:

- PN tối đa là 65535.
- Định nghĩa của PN bằng định nghĩa Signal, trừ đi một.
  Điều này tương tự như những gì Signal làm, nhưng trong Signal, PN và N nằm trong header.
  Ở đây, chúng nằm trong nội dung thông điệp được mã hóa.
- Không gửi khối này trong tag set 0, vì không có tag set trước đó.

### 5) Tải trọng

DH ratchet key tiếp theo nằm trong payload và nó là tùy chọn. Chúng ta không ratchet mỗi lần. (Điều này khác với signal, nơi mà nó nằm trong header và được gửi mỗi lần)

Đối với ratchet đầu tiên, Key ID = 0.

Không được phép trong NS hoặc NSR. Chỉ được bao gồm trong các thông điệp Existing Session.

```

+----+----+----+----+----+----+----+----+
  | 7  |  size   |flag|  key ID |         |
  +----+----+----+----+----+----+         +
  |                                       |
  +                                       +
  |     Next DH Ratchet Public Key        |
  +                                       +
  |                                       |
  +                             +----+----+
  |                             |
  +----+----+----+----+----+----+

  blk :: 7
  size :: 3 or 35
  flag :: 1 byte flags
          bit order: 76543210
          bit 0: 1 for key present, 0 for no key present
          bit 1: 1 for reverse key, 0 for forward key
          bit 2: 1 to request reverse key, 0 for no request
                 only set if bit 1 is 0
          bits 7-2: Unused, set to 0 for future compatibility
  key ID :: The key ID of this key. 2 bytes, big endian
            0 - 32767
  Public Key :: The next X25519 public key, 32 bytes, little endian
                Only if bit 0 is 1


```
Ghi chú:

- Key ID là một bộ đếm tăng dần cho key cục bộ được sử dụng cho tag set đó, bắt đầu từ 0.
- ID không được thay đổi trừ khi key thay đổi.
- Có thể không hoàn toàn cần thiết, nhưng hữu ích cho việc debug.
  Signal không sử dụng key ID.
- Key ID tối đa là 32767.
- Trong trường hợp hiếm gặp khi các tag set ở cả hai hướng đều đang ratcheting cùng lúc, một frame sẽ chứa hai Next Key block, một cho forward key và một cho reverse key.
- Các số ID của key và tag set phải tuần tự.
- Xem phần DH Ratchet ở trên để biết chi tiết.

### Phần Payload Dữ liệu đã giải mã

Điều này chỉ được gửi nếu một khối yêu cầu ack đã được nhận. Có thể có nhiều ack để xác nhận nhiều thông điệp.

Không được phép trong NS hoặc NSR. Chỉ được bao gồm trong các thông điệp Existing Session.

```
+----+----+----+----+----+----+----+----+
  | 8  |  size   |tagsetid |   N     |    |
  +----+----+----+----+----+----+----+    +
  |             more acks                 |
  ~               .   .   .               ~
  |                                       |
  +----+----+----+----+----+----+----+----+

  blk :: 8
  size :: 4 * number of acks to follow, minimum 1 ack
  for each ack:
  tagsetid :: 2 bytes, big endian, from the message being acked
  N :: 2 bytes, big endian, from the message being acked


```
Ghi chú:

- ID bộ tag và N xác định duy nhất thông điệp đang được ack.
- Trong bộ tag đầu tiên được sử dụng cho một phiên trong mỗi hướng, ID bộ tag là 0.
- Không có khối NextKey nào được gửi, do đó không có ID khóa nào.
- Đối với tất cả bộ tag được sử dụng sau trao đổi NextKey, số bộ tag là (1 + ID khóa của Alice + ID khóa của Bob).

### Dữ liệu không mã hóa

Yêu cầu một ack in-band. Để thay thế Message DeliveryStatus out-of-band trong Garlic Clove.

Nếu một ack tường minh được yêu cầu, ID tagset hiện tại và số thứ tự thông điệp (N) sẽ được trả về trong một khối ack.

Không được phép trong NS hoặc NSR. Chỉ được bao gồm trong các thông điệp Existing Session.

```

+----+----+----+----+
  |  9 |  size   |flg |
  +----+----+----+----+

  blk :: 9
  size :: 1
  flg :: 1 byte flags
         bits 7-0: Unused, set to 0 for future compatibility

```
### Quy tắc Sắp xếp Block

Tất cả padding nằm bên trong các AEAD frame. TODO Padding bên trong AEAD cần tuân thủ gần đúng các tham số đã thỏa thuận. TODO Alice đã gửi các tham số tx/rx min/max yêu cầu của cô ấy trong thông điệp NS. TODO Bob đã gửi các tham số tx/rx min/max yêu cầu của anh ấy trong thông điệp NSR. Các tùy chọn cập nhật có thể được gửi trong giai đoạn dữ liệu. Xem thông tin khối tùy chọn ở trên.

Nếu có, đây phải là khối cuối cùng trong frame.

```

+----+----+----+----+----+----+----+----+
  |254 |  size   |      padding           |
  +----+----+----+                        +
  |                                       |
  ~               .   .   .               ~
  |                                       |
  +----+----+----+----+----+----+----+----+

  blk :: 254
  size :: 2 bytes, big endian, 0-65516
  padding :: zeros or random data

```
Ghi chú:

- Padding toàn số không là được, vì nó sẽ được mã hóa.
- Các chiến lược padding TBD.
- Các frame chỉ có padding được phép.
- Padding mặc định là 0-15 byte.
- Xem khối options để thương lượng tham số padding
- Xem khối options cho các tham số padding tối thiểu/tối đa
- Phản hồi của router khi vi phạm padding đã thương lượng phụ thuộc vào implementation.

### DateTime

Các triển khai nên bỏ qua các loại block không xác định để đảm bảo tính tương thích với phiên bản sau.

### Garlic Clove

- Độ dài padding có thể được quyết định trên cơ sở từng message và
  ước tính phân bố độ dài, hoặc nên thêm các độ trễ ngẫu nhiên.
  Các biện pháp đối phó này được bao gồm để chống lại DPI, vì kích thước
  message có thể tiết lộ rằng lưu lượng I2P đang được vận chuyển bởi giao
  thức transport. Lược đồ padding chính xác là một lĩnh vực nghiên cứu trong
  tương lai, Phụ lục A cung cấp thêm thông tin về chủ đề này.

## Typical Usage Patterns

### Chấm dứt

Đây là trường hợp sử dụng điển hình nhất, và hầu hết các trường hợp sử dụng streaming không phải HTTP sẽ giống hệt với trường hợp này. Một thông điệp nhỏ ban đầu được gửi đi, một phản hồi theo sau, và các thông điệp bổ sung được gửi theo cả hai hướng.

Một HTTP GET thường vừa với một tin nhắn I2NP duy nhất. Alice gửi một yêu cầu nhỏ với một tin nhắn Session mới duy nhất, đính kèm một reply leaseset. Alice bao gồm immediate ratchet tới khóa mới. Bao gồm sig để ràng buộc với destination. Không yêu cầu ack.

Bob thực hiện ratchet ngay lập tức.

Alice ratchet ngay lập tức.

Tiếp tục với những phiên đó.

```

Alice                           Bob

  New Session (1b)     ------------------->
  with ephemeral key 1
  with static key for binding
  with next key
  with bundled HTTP GET
  with bundled LS
  without bundled Delivery Status Message

  any retransmissions, same as above

  following messages may arrive in any order:

  <--------------     New Session Reply (1g)
                      with Bob ephemeral key 1
                      with bundled HTTP reply part 1

  <--------------     New Session Reply (1g)
                      with Bob ephemeral key 2
                      with bundled HTTP reply part 2

  <--------------     New Session Reply (1g)
                      with Bob ephemeral key 3
                      with bundled HTTP reply part 3

  After reception of any of these messages,
  Alice switches to use Existing Session messages,
  creates a new inbound + outbound session pair,
  and ratchets.


  Existing Session     ------------------->
  with bundled streaming ack


  Existing Session     ------------------->
  with bundled streaming ack


  After reception of any of these messages,
  Bob switches to use Existing Session messages.


  <--------------     Existing Session
                      with bundled HTTP reply part 4


  Existing Session     ------------------->
  with bundled streaming ack

  <--------------     Existing Session
                      with bundled HTTP reply part 5

```
### Tùy chọn

Alice có ba lựa chọn:

1) Chỉ gửi thông điệp đầu tiên (window size = 1), như trong HTTP GET. Không được khuyến nghị.

2) Gửi tối đa streaming window, nhưng sử dụng cùng một Elligator2-encoded cleartext public key. Tất cả các thông điệp đều chứa cùng một next public key (ratchet). Điều này sẽ hiển thị với OBGW/IBEP vì tất cả đều bắt đầu với cùng một cleartext. Quá trình tiến hành như trong 1). Không được khuyến nghị.

3) Triển khai được khuyến nghị.    Gửi đến streaming window, nhưng sử dụng một cleartext public key được mã hóa Elligator2 khác nhau (session) cho mỗi lần.    Tất cả các thông điệp chứa cùng một next public key (ratchet).    Điều này sẽ không thể nhìn thấy đối với OBGW/IBEP vì tất cả đều bắt đầu với cleartext khác nhau.    Bob phải nhận ra rằng tất cả chúng đều chứa cùng một next public key,    và phản hồi cho tất cả bằng cùng một ratchet.    Alice sử dụng next public key đó và tiếp tục.

Luồng thông điệp Tùy chọn 3:

```

Alice                           Bob

  New Session (1b)     ------------------->
  with ephemeral key 1
  with static key for binding
  with bundled HTTP POST part 1
  with bundled LS
  without bundled Delivery Status Message


  New Session (1b)     ------------------->
  with ephemeral key 2
  with static key for binding
  with bundled HTTP POST part 2
  with bundled LS
  without bundled Delivery Status Message


  New Session (1b)     ------------------->
  with ephemeral key 3
  with static key for binding
  with bundled HTTP POST part 3
  with bundled LS
  without bundled Delivery Status Message


  following messages can arrive in any order:

  <--------------     New Session Reply (1g)
                      with Bob ephemeral key 1
                      with bundled streaming ack

  <--------------     New Session Reply (1g)
                      with Bob ephemeral key 2
                      with bundled streaming ack

  After reception of any of these messages,
  Alice switches to use Existing Session messages,
  creates a new inbound + outbound session pair,
  and ratchets.


  following messages can arrive in any order:


  Existing Session     ------------------->
  with bundled HTTP POST part 4

  Existing Session     ------------------->
  with next key
  with bundled HTTP POST part 5


  After reception of any of these messages,
  Bob switches to use Existing Session messages.


  <--------------     Existing Session
                      with bundled streaming ack

  After reception of any of this message,
  Alice switches to use Existing Session messages,
  and Alice ratchets.


  Existing Session     ------------------->
  with next key
  with bundled HTTP POST part 4

  after reception of this message, Bob ratchets

  Existing Session     ------------------->
  with next key
  with bundled HTTP POST part 5

  <--------------     Existing Session
                      with bundled streaming ack

```
### Số Thứ Tự Tin Nhắn

Một thông điệp duy nhất, với một phản hồi duy nhất được mong đợi. Các thông điệp hoặc phản hồi bổ sung có thể được gửi.

Tương tự như HTTP GET, nhưng với các tùy chọn nhỏ hơn cho kích thước cửa sổ session tag và thời gian tồn tại. Có thể không yêu cầu một ratchet.

```

Alice                           Bob

  New Session (1b)     ------------------->
  with static key for binding
  with next key
  with bundled repliable datagram
  with bundled LS
  without bundled Delivery Status Message


  <--------------     New Session Reply (1g)
                      with Bob ephemeral key
                      with bundled reply part 1

  <--------------     New Session Reply (1g)
                      with Bob ephemeral key
                      with bundled reply part 2

  After reception of either message,
  Alice switches to use Existing Session messages,
  and ratchets.

  If the Existing Session message arrives first,
  Alice ratchets on the existing inbound and outbound
  sessions.

  When the New Session Reply arrives, Alice
  sets the existing inbound session to expire,
  creates a new inbound and outbound session,
  and sends Existing Session messages on
  the new outbound session.

  Alice keeps the expiring inbound session
  around for a while to process the Existing Session
  message sent to Alice.
  If all expected original Existing Session message replies
  have been processed, Alice can expire the original
  inbound session immediately.

  if there are any other messages:

  Existing Session     ------------------->
  with bundled message

  Existing Session     ------------------->
  with bundled streaming ack

  <--------------     Existing Session
                      with bundled message

```
### Khóa Công Khai DH Ratchet Tiếp Theo

Nhiều tin nhắn ẩn danh, không cần phản hồi.

Trong tình huống này, Alice yêu cầu một phiên làm việc, nhưng không ràng buộc. Thông điệp phiên mới được gửi. Không có reply LS nào được đóng gói. Một reply DSM được đóng gói (đây là trường hợp sử dụng duy nhất yêu cầu DSM đóng gói). Không có next key nào được bao gồm. Không có reply hoặc ratchet nào được yêu cầu. Không có ratchet nào được gửi. Các tùy chọn đặt cửa sổ session tags về không.

```

Alice                           Bob

  New Session (1c)     ------------------->
  with bundled message
  without bundled LS
  with bundled Delivery Status Message 1

  New Session (1c)     ------------------->
  with bundled message
  without bundled LS
  with bundled Delivery Status Message 2

  New Session (1c)     ------------------->
  with bundled message
  without bundled LS
  with bundled Delivery Status Message 3
 
  following messages can arrive in any order:

  <--------------     Delivery Status Message 1

  <--------------     Delivery Status Message 2

  <--------------     Delivery Status Message 3

  After reception of any of these messages,
  Alice switches to use Existing Session messages.

  Existing Session     ------------------->

  Existing Session     ------------------->

  Existing Session     ------------------->

```
### Xác nhận

Một thông điệp ẩn danh đơn lẻ, không mong đợi phản hồi.

Tin nhắn một lần được gửi. Không có reply LS hoặc DSM nào được đóng gói. Không có next key nào được bao gồm. Không có reply hoặc ratchet nào được yêu cầu. Không có ratchet nào được gửi. Các tùy chọn đặt cửa sổ session tags về không.

```

Alice                           Bob

  One-Time Message (1d)   ------------------->
  with bundled message
  without bundled LS
  without bundled Delivery Status Message

```
### Yêu cầu Ack

Các phiên dài hạn có thể thực hiện ratchet, hoặc yêu cầu ratchet, bất kỳ lúc nào để duy trì tính bảo mật chuyển tiếp từ thời điểm đó. Các phiên phải thực hiện ratchet khi tiến gần đến giới hạn số tin nhắn đã gửi mỗi phiên (65535).

## Implementation Considerations

### Padding

Như với giao thức ElGamal/AES+SessionTag hiện tại, các triển khai phải giới hạn việc lưu trữ session tag và bảo vệ chống lại các cuộc tấn công cạn kiệt bộ nhớ.

Một số chiến lược được khuyến nghị bao gồm:

- Giới hạn cứng về số lượng session tag được lưu trữ
- Hết hạn tích cực của các inbound session không hoạt động khi chịu áp lực bộ nhớ
- Giới hạn số lượng inbound session được ràng buộc với một destination đầu cuối duy nhất
- Giảm thích ứng của session tag window và xóa các tag cũ không sử dụng
  khi chịu áp lực bộ nhớ
- Từ chối ratchet khi được yêu cầu, nếu chịu áp lực bộ nhớ

### Các loại block khác

Các thông số và thời gian chờ được khuyến nghị:

- Kích thước tagset NSR: 12 tsmin và tsmax
- Kích thước tagset ES 0: tsmin 24, tsmax 160
- Kích thước tagset ES (1+): 160 tsmin và tsmax
- Thời gian chờ tagset NSR: 3 phút cho receiver
- Thời gian chờ tagset ES: 8 phút cho sender, 10 phút cho receiver
- Xóa tagset ES trước đó sau: 3 phút
- Tagset look ahead của tag N: min(tsmax, tsmin + N/4)
- Tagset trim behind tag N: min(tsmax, tsmin + N/4) / 2
- Gửi key tiếp theo tại tag: TBD
- Gửi key tiếp theo sau thời gian tồn tại tagset: TBD
- Thay thế session nếu NS nhận được sau: 3 phút
- Độ lệch đồng hồ tối đa: -5 phút đến +2 phút
- Thời gian bộ lọc replay NS: 5 phút
- Kích thước padding: 0-15 byte (các chiến lược khác TBD)

### Công việc trong tương lai

Sau đây là các khuyến nghị để phân loại các thông điệp đến.

### X25519 Only

Trên một tunnel chỉ được sử dụng với giao thức này, thực hiện xác thực như hiện tại đang làm với ElGamal/AES+SessionTags:

Đầu tiên, coi dữ liệu ban đầu như một session tag, và tra cứu session tag đó. Nếu tìm thấy, giải mã bằng cách sử dụng dữ liệu được lưu trữ liên kết với session tag đó.

Nếu không tìm thấy, hãy xử lý dữ liệu ban đầu như một khóa công khai DH và nonce. Thực hiện một phép toán DH và KDF được chỉ định, và cố gắng giải mã dữ liệu còn lại.

### HTTP GET

Trên một tunnel hỗ trợ cả giao thức này và ElGamal/AES+SessionTags, phân loại các thông điệp đến như sau:

Do lỗ hổng trong đặc tả ElGamal/AES+SessionTags, khối AES không được đệm đến độ dài ngẫu nhiên không chia hết cho 16. Do đó, độ dài của các thông điệp Existing Session chia cho 16 luôn có số dư là 0, và độ dài của các thông điệp New Session chia cho 16 luôn có số dư là 2 (vì khối ElGamal dài 514 bytes).

Nếu độ dài mod 16 không phải là 0 hoặc 2, xử lý dữ liệu ban đầu như một session tag và tra cứu session tag đó. Nếu tìm thấy, giải mã bằng cách sử dụng dữ liệu đã lưu trữ liên quan với session tag đó.

Nếu không tìm thấy, và độ dài mod 16 không phải là 0 hoặc 2, hãy coi dữ liệu ban đầu như một public key DH và nonce. Thực hiện một phép toán DH và KDF được chỉ định, và cố gắng giải mã dữ liệu còn lại. (dựa trên tỷ lệ lưu lượng truy cập tương đối, và chi phí tương đối của các phép toán X25519 và ElGamal DH, bước này có thể được thực hiện cuối cùng thay thế)

Nếu không, nếu độ dài mod 16 bằng 0, xử lý dữ liệu ban đầu như một session tag ElGamal/AES, và tra cứu session tag đó. Nếu tìm thấy, giải mã bằng cách sử dụng dữ liệu đã lưu trữ được liên kết với session tag đó.

Nếu không tìm thấy, và dữ liệu có ít nhất 642 (514 + 128) byte, và độ dài chia dư cho 16 bằng 2, hãy coi dữ liệu ban đầu như một khối ElGamal. Thử giải mã dữ liệu còn lại.

Lưu ý rằng nếu đặc tả ElGamal/AES+SessionTag được cập nhật để cho phép padding không phải mod-16, thì mọi thứ sẽ cần được thực hiện theo cách khác.

### HTTP POST

Các triển khai ban đầu dựa vào lưu lượng hai chiều ở các tầng cao hơn. Nghĩa là, các triển khai giả định rằng lưu lượng theo hướng ngược lại sẽ sớm được truyền đi, điều này sẽ buộc bất kỳ phản hồi cần thiết nào ở tầng ECIES.

Tuy nhiên, một số lưu lượng có thể là đơn hướng hoặc băng thông rất thấp, do đó không có lưu lượng lớp cao hơn để tạo ra phản hồi kịp thời.

Việc nhận các thông điệp NS và NSR yêu cầu phải có phản hồi; việc nhận các khối ACK Request và Next Key cũng yêu cầu phải có phản hồi.

Một triển khai tinh vi có thể khởi động bộ đếm thời gian khi nhận được một trong những thông điệp này yêu cầu phản hồi, và tạo ra một phản hồi "rỗng" (không có khối Garlic Clove) tại tầng ECIES nếu không có lưu lượng ngược được gửi trong một khoảng thời gian ngắn (ví dụ: 1 giây).

Cũng có thể thích hợp để sử dụng thời gian chờ ngắn hơn cho các phản hồi đối với thông điệp NS và NSR, nhằm chuyển lưu lượng sang các thông điệp ES hiệu quả càng sớm càng tốt.

## Analysis

### Datagram Có Thể Trả Lời

Chi phí overhead của message cho hai message đầu tiên trong mỗi hướng như sau. Điều này giả định chỉ có một message trong mỗi hướng trước ACK, hoặc bất kỳ message bổ sung nào được gửi một cách suy đoán như các message Existing Session. Nếu không có speculative acks của các session tag đã được giao, overhead hoặc giao thức cũ sẽ cao hơn nhiều.

Không có padding được giả định để phân tích giao thức mới. Không có leaseset gộp chung được giả định.

### Nhiều Raw Datagrams

Thông điệp phiên mới, giống nhau mỗi hướng:

```

ElGamal block:
  514 bytes

  AES block:
  - 2 byte tag count
  - 1024 bytes of tags (32 typical)
  - 4 byte payload size
  - 32 byte hash of payload
  - 1 byte flags
  - 1 byte clove count
  - 33 byte Garlic deliv. inst.
  - 16 byte I2NP header
  - 15 byte clove cert, id, exp.
  - 15 byte msg cert, id, exp.
  - 0 byte padding assuming 1936 byte message
  1143 total

  Total:
  1657 bytes
```
Các thông điệp phiên hiện có, giống nhau theo mỗi hướng:

```

AES block:
  - 32 byte session tag
  - 2 byte tag count
  - 4 byte payload size
  - 32 byte hash of payload
  - 1 byte flags
  - 1 byte clove count
  - 33 byte Garlic deliv. inst.
  - 16 byte I2NP header
  - 15 byte msg cert, id, exp.
  - 15 byte clove cert, id, exp.
  - 0 byte padding assuming 1936 byte message
  151 total
```
```
Four message total (two each direction)
  3616 bytes overhead
```
### Datagram Thô Đơn

Thông điệp Alice-to-Bob New Session:

```

- 32 byte ephemeral public key
  - 32 byte static public key
  - 16 byte Poly1305 MAC
  - 7 byte DateTime block
  - 3 byte Garlic block overhead
  - 9 byte I2NP header
  - 33 byte Garlic deliv. inst.
  - 16 byte Poly1305 MAC

  Total:
  148 bytes overhead
```
Thông điệp Phản hồi Phiên mới từ Bob-tới-Alice:

```

- 8 byte session tag
  - 32 byte ephemeral public key
  - 16 byte Poly1305 MAC
  - 3 byte Garlic block overhead
  - 9 byte I2NP header
  - 33 byte Garlic deliv. inst.
  - 16 byte Poly1305 MAC

  Total:
  117 bytes overhead
```
Các thông báo phiên hiện có, giống nhau mỗi hướng:

```

- 8 byte session tag
  - 3 byte Garlic block overhead
  - 9 byte I2NP header
  - 33 byte Garlic deliv. inst.
  - 16 byte Poly1305 MAC

  Total:
  69 bytes
```
### Phiên Dài Hạn

Tổng cộng bốn thông điệp (mỗi hướng hai thông điệp):

```

372 bytes
  90% (approx. 10x) reduction compared to ElGamal/AES+SessionTags
```
Chỉ handshake:

```

ElGamal: 1657 + 1657 = 3314 bytes
  Ratchet: 148 _ 117 = 265 bytes
  92% (approx. 12x) reduction compared to ElGamal/AES+SessionTags
```
Tổng dài hạn (bỏ qua handshakes):

```
ElGamal: 151 + 32 byte tag sent previously = 183 bytes
  Ratchet: 69 bytes
  64% (approx. 3x) reduction compared to ElGamal/AES+SessionTags
```
### CPU

TODO cập nhật phần này sau khi đề xuất ổn định.

Các thao tác mã hóa sau đây được yêu cầu bởi mỗi bên để trao đổi các thông điệp New Session và New Session Reply:

- HMAC-SHA256: 3 trên mỗi HKDF, tổng cộng TBD
- ChaChaPoly: 2 cho mỗi bên
- Tạo khóa X25519: 2 Alice, 1 Bob
- X25519 DH: 3 cho mỗi bên
- Xác minh chữ ký: 1 (Bob)

Alice tính toán 5 ECDH cho mỗi phiên liên kết (tối thiểu), 2 cho mỗi thông điệp NS gửi đến Bob, và 3 cho mỗi thông điệp NSR của Bob.

Bob cũng tính toán 6 ECDH cho mỗi phiên ràng buộc, 3 cho mỗi thông điệp NS của Alice, và 3 cho mỗi thông điệp NSR của anh ấy.

Các thao tác mã hóa sau đây được yêu cầu bởi mỗi bên cho mỗi thông điệp Existing Session:

- HKDF: 2
- ChaChaPoly: 1

### Phòng thủ

Độ dài session tag hiện tại là 32 byte. Chúng tôi chưa tìm thấy bất kỳ lý do nào cho độ dài đó, nhưng chúng tôi đang tiếp tục nghiên cứu các tài liệu lưu trữ. Đề xuất trên định nghĩa độ dài tag mới là 8 byte. Phân tích chứng minh cho tag 8 byte như sau:

Session tag ratchet được giả định tạo ra các tag ngẫu nhiên, phân phối đồng đều. Không có lý do mật mã học nào cho độ dài session tag cụ thể. Session tag ratchet được đồng bộ hóa với, nhưng tạo ra đầu ra độc lập từ, symmetric key ratchet. Các đầu ra của hai ratchet có thể có độ dài khác nhau.

Do đó, mối quan tâm duy nhất là xung đột session tag. Giả định rằng các triển khai sẽ không cố gắng xử lý xung đột bằng cách thử giải mã với cả hai phiên; các triển khai sẽ đơn giản liên kết tag với phiên trước hoặc phiên mới, và bất kỳ thông điệp nào nhận được với tag đó trên phiên còn lại sẽ bị loại bỏ sau khi giải mã thất bại.

Mục tiêu là chọn độ dài session tag đủ lớn để giảm thiểu rủi ro xung đột, đồng thời đủ nhỏ để giảm thiểu việc sử dụng bộ nhớ.

Điều này giả định rằng các triển khai hạn chế việc lưu trữ session tag để ngăn chặn các cuộc tấn công cạn kiệt bộ nhớ. Điều này cũng sẽ giảm đáng kể khả năng kẻ tấn công có thể tạo ra xung đột. Xem phần Cân nhắc về Triển khai bên dưới.

Trong trường hợp tệ nhất, giả sử một máy chủ bận rộn với 64 phiên kết nối inbound mới mỗi giây. Giả sử thời gian tồn tại của inbound session tag là 15 phút (giống như hiện tại, có lẽ nên giảm xuống). Giả sử cửa sổ inbound session tag là 32. 64 * 15 * 60 * 32 = 1,843,200 tags. Hiện tại Java I2P có tối đa 750,000 inbound tags và chưa bao giờ đạt tới con số này theo như chúng tôi biết.

Mục tiêu 1 trên một triệu (1e-6) va chạm session tag có lẽ là đủ. Xác suất bỏ rơi một thông điệp trên đường đi do tắc nghẽn cao hơn nhiều so với điều đó.

Tham khảo: https://en.wikipedia.org/wiki/Birthday_paradox phần bảng xác suất.

Với session tag 32 byte (256 bit), không gian session tag là 1.2e77. Xác suất xảy ra va chạm với xác suất 1e-18 yêu cầu 4.8e29 mục. Xác suất xảy ra va chạm với xác suất 1e-6 yêu cầu 4.8e35 mục. 1.8 triệu tag với mỗi tag 32 byte tổng cộng khoảng 59 MB.

Với session tags 16 byte (128 bits), không gian session tag là 3.4e38. Xác suất va chạm với xác suất 1e-18 yêu cầu 2.6e10 entries. Xác suất va chạm với xác suất 1e-6 yêu cầu 2.6e16 entries. 1.8 triệu tags 16 byte mỗi cái tổng cộng khoảng 30 MB.

Với session tags 8 byte (64 bits), không gian session tag là 1.8e19. Xác suất xung đột với xác suất 1e-18 yêu cầu 6.1 entries. Xác suất xung đột với xác suất 1e-6 yêu cầu 6.1e6 (6,100,000) entries. 1.8 triệu tags với mỗi tag 8 bytes tổng cộng khoảng 15 MB.

6,1 triệu session tag hoạt động là hơn 3 lần so với ước tính trường hợp xấu nhất của chúng tôi là 1,8 triệu tag. Vậy nên xác suất xung đột sẽ ít hơn một phần triệu. Do đó chúng tôi kết luận rằng session tag 8 byte là đủ. Điều này dẫn đến việc giảm 4 lần không gian lưu trữ, thêm vào việc giảm 2 lần vì transmit tag không được lưu trữ. Vậy nên chúng ta sẽ có sự giảm 8 lần trong việc sử dụng bộ nhớ session tag so với ElGamal/AES+SessionTags.

Để duy trì tính linh hoạt trong trường hợp các giả định này có thể sai, chúng tôi sẽ bao gồm một trường độ dài session tag trong các tùy chọn, để độ dài mặc định có thể được ghi đè trên cơ sở từng session. Chúng tôi không mong đợi sẽ triển khai tương tác thương lượng độ dài tag động trừ khi thực sự cần thiết.

Các implementation ít nhất cũng nên nhận diện được việc va chạm session tag, xử lý chúng một cách khéo léo, và ghi log hoặc đếm số lượng va chạm. Mặc dù vẫn cực kỳ hiếm, chúng sẽ có khả năng xảy ra cao hơn nhiều so với ElGamal/AES+SessionTags, và thực sự có thể xảy ra.

### Tham số

Sử dụng gấp đôi số sessions mỗi giây (128) và gấp đôi tag window (64), chúng ta có gấp 4 lần số tags (7,4 triệu). Giá trị tối đa cho khả năng va chạm một phần triệu là 6,1 triệu tags. Tags 12 byte (hoặc thậm chí 10 byte) sẽ tăng thêm một biên độ an toàn rất lớn.

Tuy nhiên, liệu cơ hội va chạm một phần triệu có phải là mục tiêu tốt không? Lớn hơn nhiều so với cơ hội bị loại bỏ trên đường đi thì không có ích lắm. Mục tiêu false-positive cho DecayingBloomFilter của Java khoảng 1 trong 10,000, nhưng ngay cả 1 trong 1000 cũng không phải là mối quan ngại nghiêm trọng. Bằng cách giảm mục tiêu xuống 1 trong 10,000, có nhiều dư địa với các tag 8 byte.

### Phân loại

Bên gửi tạo ra các thẻ và khóa một cách động, vì vậy không cần lưu trữ. Điều này cắt giảm yêu cầu lưu trữ tổng thể đi một nửa so với ElGamal/AES. Các thẻ ECIES có kích thước 8 byte thay vì 32 byte như ElGamal/AES. Điều này cắt giảm yêu cầu lưu trữ tổng thể thêm một hệ số 4. Các khóa phiên theo thẻ không được lưu trữ ở bên nhận trừ những "khoảng trống", điều này là tối thiểu đối với tỷ lệ mất mát hợp lý.

Việc giảm 33% thời gian hết hạn tag tạo ra thêm 33% tiết kiệm, giả sử thời gian phiên ngắn.

Do đó, tổng không gian tiết kiệm so với ElGamal/AES là hệ số 10,7, hoặc 92%.

## Related Changes

### Chỉ X25519

Tra cứu cơ sở dữ liệu từ ECIES Destinations: Xem [Đề xuất 154](/proposals/154-ecies-lookups), hiện đã được tích hợp vào [I2NP](/docs/specs/i2np/) cho phiên bản 0.9.46.

Đề xuất này yêu cầu hỗ trợ LS2 để công bố khóa công khai X25519 cùng với leaseSet. Không cần thay đổi gì đối với thông số kỹ thuật LS2 trong [I2NP](/docs/specs/i2np/). Tất cả hỗ trợ đã được thiết kế, quy định và triển khai trong [Đề xuất 123](/proposals/123-new-netdb-entries) được thực hiện trong phiên bản 0.9.38.

### X25519 Chia sẻ với ElGamal/AES+SessionTags

Không có. Đề xuất này yêu cầu hỗ trợ LS2, và một thuộc tính phải được thiết lập trong các tùy chọn I2CP để được kích hoạt. Không cần thay đổi gì đối với thông số kỹ thuật [I2CP](/docs/specs/i2cp/). Tất cả hỗ trợ đã được thiết kế, chỉ định và triển khai trong [Đề xuất 123](/proposals/123-new-netdb-entries) được thực hiện trong phiên bản 0.9.38.

Tùy chọn cần thiết để kích hoạt ECIES là một thuộc tính I2CP duy nhất cho I2CP, BOB, SAM, hoặc i2ptunnel.

Các giá trị thông thường là i2cp.leaseSetEncType=4 cho chỉ ECIES, hoặc i2cp.leaseSetEncType=4,0 cho dual keys ECIES và ElGamal.

### Phản hồi tầng giao thức

Phần này được sao chép từ [Proposal 123](/proposals/123-new-netdb-entries).

Tùy chọn trong SessionConfig Mapping:

```
  i2cp.leaseSetEncType=nnn[,nnn]  The encryption types to be used.
                                  0: ElGamal
                                  1-3: See proposal 145
                                  4: This proposal.
```
### Create Leaseset2 Message

Đề xuất này yêu cầu LS2 được hỗ trợ kể từ phiên bản 0.9.38. Không cần thay đổi gì đối với thông số kỹ thuật [I2CP](/docs/specs/i2cp/). Tất cả hỗ trợ đã được thiết kế, xác định và triển khai trong [Đề xuất 123](/proposals/123-new-netdb-entries) được thực hiện trong phiên bản 0.9.38.

### Chi phí phụ

Bất kỳ router nào hỗ trợ LS2 với dual keys (0.9.38 trở lên) đều có thể hỗ trợ kết nối đến các destination với dual keys.

Các điểm đến chỉ ECIES sẽ yêu cầu phần lớn các floodfill được cập nhật lên 0.9.46 để nhận được phản hồi tra cứu được mã hóa. Xem [Đề xuất 154](/proposals/154-ecies-lookups).

Các destination chỉ dùng ECIES chỉ có thể kết nối với các destination khác là ECIES-only hoặc dual-key.
