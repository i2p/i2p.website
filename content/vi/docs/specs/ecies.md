---
title: "ECIES-X25519-AEAD-Ratchet"
description: "Sơ đồ Mã hóa Tích hợp Đường cong Elliptic cho mã hóa đầu cuối I2P"
slug: "ecies"
aliases:
  - "/vi/docs/specs/ecies-x25519-aead-ratchet"
  - "/vi/docs/specs/ecies-x25519-aead-ratchet/"
category: "Giao thức"
lastUpdated: "2025-06"
accurateFor: "0.9.67"
---

## Lưu ý

Triển khai mạng hoàn tất. Có thể có những sửa đổi nhỏ. Xem [Prop144](/proposals/144-ecies-x25519/) cho đề xuất gốc, bao gồm thảo luận nền tảng và thông tin bổ sung.

Các tính năng sau đây chưa được triển khai tính đến phiên bản 0.9.66:

- Các khối MessageNumbers, Options và Termination
- Phản hồi tầng giao thức
- Khóa tĩnh bằng không
- Multicast

Đối với phiên bản MLKEM PQ Hybrid của giao thức này, xem [ECIES-HYBRID](/docs/specs/ecies-hybrid/).

## Tổng quan

Đây là giao thức mã hóa đầu cuối mới để thay thế ElGamal/AES+SessionTags [ElG-AES](/docs/specs/elgamal-aes/).

Nó dựa trên các nghiên cứu trước đó như sau:

- Đặc tả cấu trúc chung [Common](/docs/specs/common-structures/)
- Đặc tả [I2NP](/docs/specs/i2np/) bao gồm LS2
- ElGamal/AES+Session Tags [Elg-AES](/docs/specs/elgamal-aes/)
- <http://zzz.i2p/topics/1768> tổng quan mã hóa bất đối xứng mới
- Tổng quan mã hóa cấp thấp [CRYPTO-ELG](/docs/specs/cryptography/#elgamal)
- ECIES <http://zzz.i2p/topics/2418>
- [NTCP2](/docs/specs/ntcp2/) [Prop111](/proposals/111-ntcp2/)
- 123 Các mục netDB mới
- 142 Template mã hóa mới
- Giao thức [Noise](https://noiseprotocol.org/noise.html)
- Thuật toán double ratchet của [Signal](https://signal.org/docs/specifications/doubleratchet/)

Nó hỗ trợ mã hóa mới cho giao tiếp đầu cuối đến đầu cuối, destination đến destination.

Thiết kế sử dụng quá trình bắt tay Noise và giai đoạn dữ liệu kết hợp cơ chế double ratchet của Signal.

Tất cả các tham chiếu đến Signal và Noise trong đặc tả này chỉ mang tính chất thông tin nền. Việc hiểu biết về các giao thức Signal và Noise không bắt buộc để hiểu hoặc triển khai đặc tả này.

Đặc tả này được hỗ trợ từ phiên bản 0.9.46.

## Đặc tả kỹ thuật

Thiết kế sử dụng quá trình bắt tay Noise và giai đoạn dữ liệu tích hợp double ratchet của Signal.

### Tổng quan về Thiết kế Mã hóa

Có năm phần của giao thức cần được thiết kế lại:

- 1\) Các định dạng container Session mới và Hiện có được thay thế bằng
  các định dạng mới.
- 2\) ElGamal (khóa công khai 256 byte, khóa riêng 128 byte) được
  thay thế bằng ECIES-X25519 (khóa công khai và riêng 32 byte)
- 3\) AES được thay thế bằng AEAD_ChaCha20_Poly1305 (viết tắt là
  ChaChaPoly bên dưới)
- 4\) SessionTags sẽ được thay thế bằng ratchets, về cơ bản là một
  PRNG mật mã hóa, đồng bộ.
- 5\) Payload AES, như được định nghĩa trong đặc tả
  ElGamal/AES+SessionTags, được thay thế bằng định dạng block tương tự
  như trong NTCP2.

Mỗi thay đổi trong số năm thay đổi đều có phần riêng của nó bên dưới.

### Loại Mã hóa

Loại crypto (được sử dụng trong LS2) là 4. Điều này chỉ ra một khóa công khai X25519 32-byte little-endian và giao thức end-to-end được chỉ định ở đây.

Crypto type 0 là ElGamal. Crypto types 1-3 được dành riêng cho ECIES-ECDH-AES-SessionTag, xem đề xuất 145 [Prop145](/proposals/145-ecies-ecdh-aes/).

### Khung Giao Thức Noise

Giao thức này cung cấp các yêu cầu dựa trên Noise Protocol Framework [NOISE](https://noiseprotocol.org/noise.html) (Phiên bản 34, 2018-07-11). Noise có các thuộc tính tương tự như giao thức Station-To-Station [STS](https://en.wikipedia.org/wiki/Station-to-Station_protocol), là cơ sở cho giao thức [SSU](/docs/transport/ssu/). Trong thuật ngữ của Noise, Alice là bên khởi tạo, và Bob là bên phản hồi.

Đặc tả này dựa trên giao thức Noise Noise_IK_25519_ChaChaPoly_SHA256. (Định danh thực tế cho hàm tạo khóa ban đầu là "Noise_IKelg2_25519_ChaChaPoly_SHA256" để chỉ ra các phần mở rộng I2P - xem phần KDF 1 bên dưới) Giao thức Noise này sử dụng các thành phần cơ bản sau:

- Interactive Handshake Pattern: IK Alice ngay lập tức truyền khóa tĩnh của mình cho Bob (I) Alice đã biết khóa tĩnh của Bob (K)
- One-Way Handshake Pattern: N Alice không truyền khóa tĩnh của mình cho Bob (N)
- DH Function: X25519 X25519 DH với độ dài khóa 32 byte như được chỉ định trong [RFC-7748](https://tools.ietf.org/html/rfc7748).
- Cipher Function: ChaChaPoly AEAD_CHACHA20_POLY1305 như được chỉ định trong [RFC-7539](https://tools.ietf.org/html/rfc7539) phần 2.8. Nonce 12 byte, với 4 byte đầu được đặt bằng không. Giống hệt như trong [NTCP2](/docs/specs/ntcp2/).
- Hash Function: SHA256 Hash tiêu chuẩn 32 byte, đã được sử dụng rộng rãi trong I2P.

#### Bổ sung cho Framework

Đặc tả này định nghĩa các cải tiến sau đây cho Noise_IK_25519_ChaChaPoly_SHA256. Chúng thường tuân theo các hướng dẫn trong [NOISE](https://noiseprotocol.org/noise.html) phần 13.

1)  Khóa tạm thời dạng văn bản rõ được mã hóa bằng

    [Elligator2](https://elligator.cr.yp.to/elligator-20130828.pdf).
2) Phản hồi được thêm tiền tố với một thẻ văn bản rõ. 3) Định dạng payload được xác định cho các tin nhắn 1, 2, và giai đoạn dữ liệu.

    Of course, this is not defined in Noise.

Tất cả các tin nhắn bao gồm header [I2NP](/docs/specs/i2np/) Garlic Message. Giai đoạn dữ liệu sử dụng mã hóa tương tự, nhưng không tương thích với giai đoạn dữ liệu Noise.

### Các Mẫu Handshake

Handshake sử dụng các mẫu handshake [Noise](https://noiseprotocol.org/noise.html).

Ánh xạ chữ cái sau được sử dụng:

- e = khóa ephemeral một lần
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
#### Thuộc tính Bảo mật

Sử dụng thuật ngữ Noise, trình tự thiết lập và dữ liệu như sau: (Thuộc tính Bảo mật Payload từ [Noise](https://noiseprotocol.org/noise.html) )

```
IK(s, rs):           Authentication   Confidentiality
  <- s
  ...
  -> e, es, s, ss           1                2
  <- e, ee, se              2                4
  ->                        2                5
  <-                        2                5
```
#### Sự khác biệt so với XK

Các bắt tay IK có nhiều điểm khác biệt so với các bắt tay XK được sử dụng trong [NTCP2](/docs/specs/ntcp2/) và [SSU2](/docs/specs/ssu2/).

- Tổng cộng bốn thao tác DH so với ba thao tác cho XK
- Xác thực người gửi trong thông điệp đầu tiên: Payload được xác thực
  là thuộc về chủ sở hữu của khóa công khai của người gửi, mặc dù
  khóa có thể đã bị xâm phạm (Authentication 1) XK yêu cầu một
  vòng truyền thông khác trước khi Alice được xác thực.
- Bảo mật chuyển tiếp hoàn toàn (Confidentiality 5) sau thông điệp thứ hai. Bob
  có thể gửi payload ngay lập tức sau thông điệp thứ hai với bảo mật
  chuyển tiếp hoàn toàn. XK yêu cầu một vòng truyền thông khác để có
  bảo mật chuyển tiếp hoàn toàn.

Tóm lại, IK cho phép gửi payload phản hồi từ Bob đến Alice trong 1-RTT với tính bảo mật hoàn toàn về phía trước, tuy nhiên payload yêu cầu không có tính bảo mật về phía trước.

### Phiên

Giao thức ElGamal/AES+SessionTag là một chiều. Ở lớp này, bên nhận không biết thông điệp đến từ đâu. Các phiên gửi đi và nhận về không được liên kết với nhau. Các xác nhận được thực hiện ngoài băng tần bằng cách sử dụng DeliveryStatusMessage (được bọc trong GarlicMessage) trong clove.

Đối với đặc tả này, chúng tôi định nghĩa hai cơ chế để tạo ra một giao thức hai chiều - "pairing" và "binding". Các cơ chế này cung cấp hiệu quả và bảo mật tăng cường.

#### Ngữ cảnh phiên

Như với ElGamal/AES+SessionTags, tất cả các phiên inbound và outbound phải nằm trong một context nhất định, có thể là context của router hoặc context cho một destination cục bộ cụ thể. Trong Java I2P, context này được gọi là Session Key Manager.

Các session không được chia sẻ giữa các ngữ cảnh, vì điều đó sẽ cho phép tương quan giữa các đích địa phương khác nhau, hoặc giữa một đích địa phương và một router.

Khi một destination nhất định hỗ trợ cả ElGamal/AES+SessionTags và đặc tả này, cả hai loại session có thể chia sẻ một context. Xem mục 1c) bên dưới.

#### Ghép nối các phiên kết nối đến và đi

Khi một phiên kết nối đi được tạo tại nguồn gốc (Alice), một phiên kết nối đến mới sẽ được tạo và ghép nối với phiên kết nối đi, trừ khi không mong đợi phản hồi (ví dụ: raw datagrams).

Một phiên kết nối đến (inbound session) mới luôn được ghép cặp với một phiên kết nối đi (outbound session) mới, trừ khi không yêu cầu phản hồi (ví dụ: datagram thô).

Nếu một phản hồi được yêu cầu và ràng buộc với một điểm đích xa hoặc router, thì phiên outbound mới đó sẽ được ràng buộc với điểm đích hoặc router đó, và thay thế bất kỳ phiên outbound trước đó nào đến điểm đích hoặc router đó.

Việc ghép nối các phiên kết nối đến và đi cung cấp một giao thức hai chiều với khả năng xoay vòng các khóa DH.

#### Ràng buộc Sessions và Destinations

Chỉ có một phiên gửi ra (outbound session) duy nhất đến một đích hoặc router nhất định. Có thể có nhiều phiên nhận vào (inbound session) hiện tại từ một đích hoặc router nhất định. Thông thường, khi một phiên nhận vào mới được tạo và lưu lượng được nhận trên phiên đó (đóng vai trò như một ACK), các phiên khác sẽ được đánh dấu để hết hạn tương đối nhanh chóng, trong vòng một phút hoặc lâu hơn. Giá trị tin nhắn đã gửi trước đó (PN) được kiểm tra, và nếu không có tin nhắn chưa nhận được (trong kích thước cửa sổ) trong phiên nhận vào trước đó, phiên trước có thể bị xóa ngay lập tức.

Khi một phiên kết nối ra ngoài được tạo tại điểm khởi tạo (Alice), nó sẽ được liên kết với Destination ở đầu xa (Bob), và bất kỳ phiên kết nối vào ghép đôi nào cũng sẽ được liên kết với Destination ở đầu xa. Khi các phiên này thực hiện ratchet, chúng tiếp tục được liên kết với Destination ở đầu xa.

Khi một phiên inbound được tạo tại bên nhận (Bob), nó có thể được ràng buộc với Destination ở đầu xa (Alice), tùy theo lựa chọn của Alice. Nếu Alice bao gồm thông tin ràng buộc (khóa tĩnh của cô ấy) trong thông điệp New Session, phiên sẽ được ràng buộc với destination đó, và một phiên outbound sẽ được tạo và ràng buộc với cùng Destination. Khi các phiên ratchet, chúng tiếp tục được ràng buộc với Destination ở đầu xa.

#### Lợi ích của Binding và Pairing

Trong trường hợp thông thường, streaming, chúng ta kỳ vọng Alice và Bob sử dụng giao thức như sau:

- Alice ghép cặp phiên gửi đi mới của mình với một phiên nhận vào mới, cả hai
  đều được liên kết với điểm đích xa (Bob).
- Alice bao gồm thông tin liên kết và chữ ký, cùng với một yêu cầu phản hồi,
  trong thông điệp New Session được gửi đến Bob.
- Bob ghép cặp phiên nhận vào mới của mình với một phiên gửi đi mới, cả hai
  đều được liên kết với điểm đích xa (Alice).
- Bob gửi một phản hồi (ack) đến Alice trong phiên đã được ghép cặp, với một ratchet
  đến một khóa DH mới.
- Alice thực hiện ratchet đến một phiên gửi đi mới với khóa mới của Bob, được ghép cặp
  với phiên nhận vào hiện có.

Bằng cách liên kết một phiên kết nối vào với một Destination ở đầu xa, và ghép nối phiên kết nối vào với một phiên kết nối ra được liên kết với cùng một Destination, chúng ta đạt được hai lợi ích chính:

1)  Phản hồi ban đầu từ Bob tới Alice sử dụng ephemeral-ephemeral DH

2\) Sau khi Alice nhận được phản hồi của Bob và thực hiện ratchet, tất cả các thông điệp tiếp theo từ Alice gửi đến Bob đều sử dụng ephemeral-ephemeral DH.

#### Xác nhận tin nhắn

Trong ElGamal/AES+SessionTags, khi một LeaseSet được đóng gói như một garlic clove, hoặc các tag được gửi đi, router gửi sẽ yêu cầu một ACK. Đây là một garlic clove riêng biệt chứa một DeliveryStatus Message. Để tăng cường bảo mật, DeliveryStatus Message được bao bọc trong một Garlic Message. Cơ chế này hoạt động ngoài băng tần từ góc độ của giao thức.

Trong giao thức mới, vì các phiên inbound và outbound được ghép đôi, chúng ta có thể có ACK trong băng tần. Không cần clove riêng biệt.

Một ACK rõ ràng đơn giản là một thông điệp Existing Session không có khối I2NP. Tuy nhiên, trong hầu hết các trường hợp, một ACK rõ ràng có thể được tránh, vì có lưu lượng ngược chiều. Có thể mong muốn cho các triển khai chờ một thời gian ngắn (có lẽ một trăm ms) trước khi gửi một ACK rõ ràng, để cho lớp streaming hoặc ứng dụng có thời gian phản hồi.

Các triển khai cũng sẽ cần trì hoãn việc gửi bất kỳ ACK nào cho đến sau khi khối I2NP được xử lý, vì Garlic Message có thể chứa một Database Store Message với một leaseSet. Một leaseSet gần đây sẽ cần thiết để định tuyến ACK, và đích đến xa (chứa trong leaseSet) sẽ cần thiết để xác minh khóa tĩnh ràng buộc.

#### Thời gian chờ phiên

Các phiên outbound nên luôn hết hạn trước các phiên inbound. Khi một phiên outbound hết hạn và một phiên mới được tạo, một phiên inbound được ghép đôi mới cũng sẽ được tạo ra. Nếu có một phiên inbound cũ, nó sẽ được phép hết hạn.

### Multicast

Sẽ được bổ sung

### Định nghĩa

Chúng tôi định nghĩa các hàm sau tương ứng với các khối xây dựng mật mã được sử dụng.

ZEROLEN

mảng byte có độ dài bằng không

CSRNG(n)

đầu ra n-byte từ một số ngẫu nhiên bảo mật mật mã

    generator.

H(p, d)

Hàm hash SHA-256 nhận một chuỗi cá nhân hóa p và dữ liệu

    d, and produces an output of length 32 bytes. As defined in
    [NOISE](https://noiseprotocol.org/noise.html). || below means append.

    Use SHA-256 as follows:

        H(p, d) := SHA-256(p || d)

MixHash(d)

Hàm băm SHA-256 nhận vào một hash trước đó h và dữ liệu mới d,

    and produces an output of length 32 bytes. || below means append.

    Use SHA-256 as follows:

        MixHash(d) := h = SHA-256(h || d)

STREAM

ChaCha20/Poly1305 AEAD như được quy định trong

    [RFC-7539](https://tools.ietf.org/html/rfc7539). S_KEY_LEN = 32 and S_IV_LEN =
    12.

    ENCRYPT(k, n, plaintext, ad)

    :   Encrypts plaintext using the cipher key k, and nonce n which
        MUST be unique for the key k. Associated data ad is optional.
        Returns a ciphertext that is the size of the plaintext + 16
        bytes for the HMAC.

        The entire ciphertext must be indistinguishable from random if
        the key is secret.

    DECRYPT(k, n, ciphertext, ad)

    :   Decrypts ciphertext using the cipher key k, and nonce n.
        Associated data ad is optional. Returns the plaintext.

DH

Hệ thống thỏa thuận khóa công khai X25519. Khóa riêng tư 32 byte, khóa công khai

    keys of 32 bytes, produces outputs of 32 bytes. It has the following
    functions:

    GENERATE_PRIVATE()

    :   Generates a new private key.

    DERIVE_PUBLIC(privkey)

    :   Returns the public key corresponding to the given private key.

    GENERATE_PRIVATE_ELG2()

    :   Generates a new private key that maps to a public key suitable
        for Elligator2 encoding. Note that half of the
        randomly-generated private keys will not be suitable and must be
        discarded.

    ENCODE_ELG2(pubkey)

    :   Returns the Elligator2-encoded public key corresponding to the
        given public key (inverse mapping). Encoded keys are little
        endian. Encoded key must be 256 bits indistinguishable from
        random data. See Elligator2 section below for specification.

    DECODE_ELG2(pubkey)

    :   Returns the public key corresponding to the given
        Elligator2-encoded public key. See Elligator2 section below for
        specification.

    DH(privkey, pubkey)

    :   Generates a shared secret from the given private and public
        keys.

HKDF(salt, ikm, info, n)

Một hàm dẫn xuất khóa mật mã nhận một khóa đầu vào nào đó

    material ikm (which should have good entropy but is not required to
    be a uniformly random string), a salt of length 32 bytes, and a
    context-specific 'info' value, and produces an output of n bytes
    suitable for use as key material.

    Use HKDF as specified in [RFC-5869](https://tools.ietf.org/html/rfc5869), using
    the HMAC hash function SHA-256 as specified in
    [RFC-2104](https://tools.ietf.org/html/rfc2104). This means that SALT_LEN is 32
    bytes max.

MixKey(d)

Sử dụng HKDF() với chainKey trước đó và dữ liệu mới d, và đặt

    chainKey and k. As defined in [NOISE](https://noiseprotocol.org/noise.html).

    Use HKDF as follows:

        MixKey(d) := output = HKDF(chainKey, d, "", 64)
                     chainKey = output[0:31]
                     k = output[32:63]

### 1) Định dạng tin nhắn

#### Đánh giá Định dạng Thông điệp Hiện tại

Garlic Message như được quy định trong [I2NP](/docs/specs/i2np/) như sau. Vì mục tiêu thiết kế là các hop trung gian không thể phân biệt mã hóa mới với cũ, định dạng này không thể thay đổi, mặc dù trường độ dài là dư thừa. Định dạng được hiển thị với header 16-byte đầy đủ, mặc dù header thực tế có thể ở định dạng khác, tùy thuộc vào transport được sử dụng.

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
#### Đánh giá Định dạng Dữ liệu Được Mã hóa

Trong ElGamal/AES+SessionTags, có hai định dạng thông điệp:

1\) Phiên mới: - Khối ElGamal 514 byte - Khối AES (tối thiểu 128 byte, bội số của 16)

2\) Phiên hiện có: - 32 byte Session Tag - Khối AES (tối thiểu 128 byte, bội số của 16)

Các thông điệp này được đóng gói trong một thông điệp I2NP garlic, có chứa trường độ dài, vì vậy độ dài đã được biết trước.

Người nhận trước tiên cố gắng tra cứu 32 byte đầu tiên như một Session Tag. Nếu tìm thấy, anh ta giải mã khối AES. Nếu không tìm thấy, và dữ liệu có độ dài ít nhất (514+16), anh ta cố gắng giải mã khối ElGamal, và nếu thành công, sẽ giải mã khối AES.

#### Session Tags Mới và So sánh với Signal

Trong Signal Double Ratchet, header chứa:

- DH: Khóa công khai ratchet hiện tại
- PN: Độ dài tin nhắn chuỗi trước
- N: Số tin nhắn

"Sending chains" của Signal tương đương với các tag set của chúng ta. Bằng cách sử dụng session tag, chúng ta có thể loại bỏ phần lớn điều đó.

Trong New Session, chúng tôi chỉ đặt khóa công khai trong header không được mã hóa.

Trong Existing Session, chúng ta sử dụng session tag cho header. Session tag được liên kết với ratchet public key hiện tại và số thứ tự tin nhắn.

Trong cả Phiên mới và Phiên hiện có, PN và N đều nằm trong phần thân được mã hóa.

Trong Signal, mọi thứ liên tục được xoay vòng (ratchet). Một public key DH mới yêu cầu bên nhận phải xoay vòng và gửi lại một public key mới, điều này cũng đóng vai trò là ack cho public key đã nhận. Điều này sẽ có quá nhiều phép toán DH đối với chúng ta. Vì vậy chúng ta tách biệt việc ack public key đã nhận và việc truyền một public key mới. Bất kỳ message nào sử dụng session tag được tạo từ public key DH mới đều tạo thành một ACK. Chúng ta chỉ truyền một public key mới khi chúng ta muốn thực hiện rekey.

Số lượng tin nhắn tối đa trước khi DH phải thực hiện ratchet là 65535.

Khi phân phối một session key, chúng ta rút ra "Tag Set" từ đó, thay vì phải phân phối cả session tags. Một Tag Set có thể chứa tới 65536 tags. Tuy nhiên, các receiver nên triển khai chiến lược "look-ahead", thay vì tạo ra tất cả các tags có thể cùng một lúc. Chỉ tạo ra tối đa N tags sau tag hợp lệ cuối cùng nhận được. N có thể tối đa là 128, nhưng 32 hoặc thậm chí ít hơn có thể là lựa chọn tốt hơn.

### 1a) Định dạng phiên mới

Khóa công khai một lần của phiên mới (32 byte) Dữ liệu được mã hóa và MAC (các byte còn lại)

Thông điệp New Session có thể chứa hoặc không chứa khóa công khai tĩnh của người gửi. Nếu được bao gồm, phiên ngược sẽ được ràng buộc với khóa đó. Khóa tĩnh nên được bao gồm nếu dự kiến có phản hồi, tức là đối với streaming và các datagram có thể trả lời. Không nên bao gồm khóa này đối với các datagram thô.

Thông điệp New Session tương tự như mẫu Noise [NOISE](https://noiseprotocol.org/noise.html) một chiều "N" (nếu static key không được gửi), hoặc mẫu hai chiều "IK" (nếu static key được gửi).

### 1b) Định dạng phiên mới (có ràng buộc)

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
#### Khóa Tạm thời Phiên mới

Khóa tạm thời có độ dài 32 byte, được mã hóa bằng Elligator2. Khóa này không bao giờ được sử dụng lại; một khóa mới được tạo ra với mỗi tin nhắn, bao gồm cả việc truyền lại.

#### Khóa Tĩnh

Khi được giải mã, khóa tĩnh X25519 của Alice, 32 byte.

#### Tải trọng

Độ dài mã hóa là phần còn lại của dữ liệu. Độ dài giải mã ít hơn 16 so với độ dài mã hóa. Payload phải chứa một khối DateTime và thường sẽ chứa một hoặc nhiều khối Garlic Clove. Xem phần payload bên dưới để biết định dạng và các yêu cầu bổ sung.

### 1c) Định dạng phiên mới (không có ràng buộc)

Nếu không cần phản hồi, không có static key nào được gửi.

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
#### Khóa Tạm Thời Phiên Mới

Khóa tạm thời của Alice. Khóa tạm thời có độ dài 32 byte, được mã hóa bằng Elligator2, little endian. Khóa này không bao giờ được tái sử dụng; một khóa mới được tạo ra cho mỗi thông điệp, bao gồm cả các lần truyền lại.

#### Phần Flags Dữ liệu đã giải mã

Phần Flags không chứa gì cả. Nó luôn có độ dài 32 byte, vì phải có cùng độ dài với static key cho các thông điệp New Session có binding. Bob xác định xem đó là static key hay phần flags bằng cách kiểm tra xem 32 byte đó có phải tất cả đều là số không hay không.

TODO có cần flags nào ở đây không?

#### Tải trọng

Độ dài được mã hóa là phần dữ liệu còn lại. Độ dài đã giải mã nhỏ hơn độ dài được mã hóa 16 byte. Payload phải chứa một khối DateTime và thường sẽ chứa một hoặc nhiều khối Garlic Clove. Xem phần payload bên dưới để biết định dạng và các yêu cầu bổ sung.

### 1d) Định dạng một lần (không có ràng buộc hoặc phiên)

Nếu chỉ cần gửi một tin nhắn duy nhất, không cần thiết lập phiên làm việc hay khóa tĩnh.

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
#### Khóa Một Lần Phiên Mới

Khóa một lần có độ dài 32 byte, được mã hóa bằng Elligator2, little endian. Khóa này không bao giờ được sử dụng lại; một khóa mới được tạo với mỗi thông điệp, bao gồm cả việc truyền lại.

#### Dữ liệu đã giải mã phần Flags

Phần Flags không chứa gì cả. Nó luôn có độ dài 32 byte, vì phải có cùng độ dài với static key cho các thông điệp New Session với binding. Bob xác định xem đó là static key hay phần flags bằng cách kiểm tra xem 32 byte có phải toàn là số không hay không.

TODO có cần flags nào ở đây không?

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
#### Tải trọng

Độ dài mã hóa là phần dữ liệu còn lại. Độ dài giải mã ít hơn độ dài mã hóa 16 byte. Payload phải chứa một khối DateTime và thường sẽ chứa một hoặc nhiều khối Garlic Clove. Xem phần payload bên dưới để biết định dạng và các yêu cầu bổ sung.

### 1f) KDF cho Thông điệp Phiên mới

#### KDF cho ChainKey ban đầu

Đây là [NOISE](https://noiseprotocol.org/noise.html) tiêu chuẩn cho IK với tên giao thức đã được sửa đổi. Lưu ý rằng chúng tôi sử dụng cùng một bộ khởi tạo cho cả mẫu IK (phiên liên kết) và mẫu N (phiên không liên kết).

Tên giao thức được chỉnh sửa vì hai lý do. Thứ nhất, để chỉ ra rằng các khóa tạm thời được mã hóa bằng Elligator2, và thứ hai, để chỉ ra rằng MixHash() được gọi trước thông điệp thứ hai để trộn vào giá trị tag.

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
#### KDF cho Nội dung Được Mã hóa của Phần Flags/Static Key

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
#### KDF cho Phần Payload (với khóa tĩnh của Alice)

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
#### KDF cho Phần Payload (không có khóa tĩnh của Alice)

Lưu ý rằng đây là một mẫu Noise "N", nhưng chúng tôi sử dụng cùng một bộ khởi tạo "IK" như đối với các phiên kết nối ràng buộc.

Các thông điệp New Session không thể được xác định là có chứa static key của Alice hay không cho đến khi static key được giải mã và kiểm tra để xác định xem nó có chứa toàn số không hay không. Do đó, bên nhận phải sử dụng máy trạng thái "IK" cho tất cả các thông điệp New Session. Nếu static key là toàn số không, thì mẫu thông điệp "ss" phải được bỏ qua.

```
chainKey = from Flags/Static key section
k = from Flags/Static key section
n = 1
ad = h from Flags/Static key section
ciphertext = ENCRYPT(k, n, payload, ad)
```
### 1g) Định dạng New Session Reply

Một hoặc nhiều New Session Replies có thể được gửi để phản hồi cho một New Session message duy nhất. Mỗi reply được bắt đầu bằng một tag, được tạo ra từ một TagSet cho session đó.

New Session Reply gồm hai phần. Phần đầu là việc hoàn thành quá trình bắt tay Noise IK với một tag được thêm vào phía trước. Độ dài của phần đầu là 56 byte. Phần thứ hai là payload giai đoạn dữ liệu. Độ dài của phần thứ hai là 16 + độ dài payload.

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
#### Session Tag

Tag được tạo ra trong Session Tags KDF, như được khởi tạo trong DH Initialization KDF bên dưới. Điều này liên kết phản hồi với phiên làm việc. Session Key từ DH Initialization không được sử dụng.

#### Khóa Tạm thời Phản hồi Session Mới

Khóa tạm thời của Bob. Khóa tạm thời có độ dài 32 byte, được mã hóa bằng Elligator2, little endian. Khóa này không bao giờ được sử dụng lại; một khóa mới được tạo ra với mỗi tin nhắn, bao gồm cả các lần truyền lại.

#### Tải trọng

Độ dài mã hóa là phần còn lại của dữ liệu. Độ dài giải mã ít hơn độ dài mã hóa 16 byte. Payload thường chứa một hoặc nhiều khối Garlic Clove. Xem phần payload bên dưới để biết định dạng và các yêu cầu bổ sung.

#### KDF cho Reply TagSet

Một hoặc nhiều tag được tạo từ TagSet, được khởi tạo bằng cách sử dụng KDF bên dưới, sử dụng chainKey từ thông điệp New Session.

```
// Generate tagset

tagsetKey = HKDF(chainKey, ZEROLEN, "SessionReplyTags", 32)
    tagset_nsr = DH_INITIALIZE(chainKey, tagsetKey)

```
#### KDF cho Nội dung Mã hóa của Phần Reply Key

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
#### KDF cho Nội dung Mã hóa của Phần Payload

Điều này giống như thông điệp Existing Session đầu tiên, sau khi tách, nhưng không có tag riêng biệt. Ngoài ra, chúng ta sử dụng hash từ trên để ràng buộc payload với thông điệp NSR.

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
### Ghi chú

Nhiều thông báo NSR có thể được gửi để trả lời, mỗi thông báo với các khóa tạm thời duy nhất, tùy thuộc vào kích thước của phản hồi.

Alice và Bob được yêu cầu sử dụng các khóa tạm thời mới cho mỗi thông báo NS và NSR.

Alice phải nhận được một trong những tin nhắn NSR của Bob trước khi gửi tin nhắn Existing Session (ES), và Bob phải nhận được tin nhắn ES từ Alice trước khi gửi tin nhắn ES.

`chainKey` và `k` từ NSR Payload Section của Bob được sử dụng làm đầu vào cho các ES DH Ratchets ban đầu (cả hai hướng, xem DH Ratchet KDF).

Bob chỉ được giữ lại các Phiên Hiện Có cho các thông điệp ES nhận được từ Alice. Bất kỳ phiên inbound và outbound nào khác được tạo (cho nhiều NSR) đều phải được hủy ngay lập tức sau khi nhận được thông điệp ES đầu tiên của Alice cho một phiên nhất định.

### 1h) Định dạng phiên hiện có

Session tag (8 byte) Dữ liệu mã hóa và MAC (xem mục 3 bên dưới)

#### Định dạng

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
#### Tải trọng

Độ dài được mã hóa là phần còn lại của dữ liệu. Độ dài được giải mã nhỏ hơn độ dài được mã hóa 16 byte. Xem phần payload bên dưới để biết định dạng và yêu cầu.

#### KDF

```
See AEAD section below.

// AEAD parameters for Existing Session payload
k = The 32-byte session key associated with this session tag
n = The message number N in the current chain, as retrieved from the associated Session Tag.
ad = The session tag, 8 bytes
ciphertext = ENCRYPT(k, n, payload, ad)
```
### 2) ECIES-X25519

Định dạng: Khóa công khai và khóa riêng tư 32-byte, little-endian.

### 2a) Elligator2

Trong các quá trình bắt tay Noise tiêu chuẩn, các thông điệp bắt tay ban đầu theo mỗi hướng bắt đầu bằng các khóa tạm thời được truyền dưới dạng văn bản rõ. Vì các khóa X25519 hợp lệ có thể phân biệt được với dữ liệu ngẫu nhiên, một kẻ tấn công man-in-the-middle có thể phân biệt các thông điệp này với các thông điệp Existing Session bắt đầu bằng các session tag ngẫu nhiên. Trong [NTCP2](/docs/specs/ntcp2/) ([Prop111](/proposals/111-ntcp2/)), chúng tôi đã sử dụng hàm XOR có overhead thấp sử dụng khóa tĩnh out-of-band để làm mờ khóa. Tuy nhiên, mô hình mối đe dọa ở đây là khác; chúng tôi không muốn cho phép bất kỳ MitM nào sử dụng bất kỳ phương tiện nào để xác nhận đích đến của lưu lượng truy cập, hoặc để phân biệt các thông điệp bắt tay ban đầu với các thông điệp Existing Session.

Do đó, [Elligator2](https://elligator.cr.yp.to/elligator-20130828.pdf) được sử dụng để biến đổi các ephemeral key trong các thông điệp New Session và New Session Reply sao cho chúng không thể phân biệt được với các chuỗi ngẫu nhiên đồng nhất.

#### Định dạng

Khóa công khai và khóa riêng tư 32-byte. Các khóa được mã hóa theo thứ tự little endian.

Như được định nghĩa trong [Elligator2](https://elligator.cr.yp.to/elligator-20130828.pdf), các khóa được mã hóa không thể phân biệt được với 254 bit ngẫu nhiên. Chúng ta yêu cầu 256 bit ngẫu nhiên (32 byte). Do đó, việc mã hóa và giải mã được định nghĩa như sau:

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
#### Ghi chú

Elligator2 làm tăng gấp đôi thời gian tạo khóa trung bình, vì một nửa số khóa riêng tư tạo ra khóa công khai không phù hợp để mã hóa bằng Elligator2. Ngoài ra, thời gian tạo khóa là không giới hạn với phân phối hàm mũ, vì bộ tạo phải liên tục thử lại cho đến khi tìm được cặp khóa phù hợp.

Chi phí này có thể được quản lý bằng cách thực hiện tạo khóa trước, trong một thread riêng biệt, để duy trì một pool các khóa phù hợp.

Generator thực hiện hàm ENCODE_ELG2() để xác định tính phù hợp. Do đó, generator nên lưu trữ kết quả của ENCODE_ELG2() để không phải tính toán lại.

Ngoài ra, các khóa không phù hợp có thể được thêm vào nhóm khóa được sử dụng cho [NTCP2](/docs/specs/ntcp2/), nơi Elligator2 không được sử dụng. Các vấn đề bảo mật khi thực hiện điều này vẫn đang được xem xét.

### 3) AEAD (ChaChaPoly)

AEAD sử dụng ChaCha20 và Poly1305, giống như trong [NTCP2](/docs/specs/ntcp2/). Điều này tương ứng với [RFC-7539](https://tools.ietf.org/html/rfc7539), cũng được sử dụng tương tự trong TLS [RFC-7905](https://tools.ietf.org/html/rfc7905).

#### Đầu vào New Session và New Session Reply

Các đầu vào cho các hàm mã hóa/giải mã cho một khối AEAD trong thông điệp New Session:

```
k :: 32 byte cipher key
     See New Session and New Session Reply KDFs above.

n :: Counter-based nonce, 12 bytes.
     n = 0

ad :: Associated data, 32 bytes.
      The SHA256 hash of the preceding data, as output from mixHash()

data :: Plaintext data, 0 or more bytes
```
#### Đầu vào Phiên hiện có

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
#### Định dạng mã hóa

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
#### Ghi chú

- Vì ChaCha20 là stream cipher (mã hóa dòng), plaintext không cần được padding.
  Các byte keystream bổ sung sẽ bị loại bỏ.
- Key cho cipher (256 bits) được thỏa thuận thông qua SHA256 KDF. Chi tiết về
  KDF cho mỗi message được trình bày trong các phần riêng biệt bên dưới.
- Các ChaChaPoly frame có kích thước đã biết vì chúng được đóng gói trong
  I2NP data message.
- Đối với tất cả message, padding nằm bên trong authenticated data frame.

#### Xử Lý Lỗi AEAD

Tất cả dữ liệu nhận được mà thất bại trong quá trình xác minh AEAD phải được loại bỏ. Không có phản hồi nào được trả về.

### 4) Ratchets

Chúng tôi vẫn sử dụng session tags như trước, nhưng chúng tôi sử dụng ratchets để tạo ra chúng. Session tags cũng có tùy chọn rekey mà chúng tôi chưa bao giờ triển khai. Vì vậy nó giống như một double ratchet nhưng chúng tôi chưa bao giờ thực hiện cái thứ hai.

Ở đây chúng ta định nghĩa một cái gì đó tương tự như Double Ratchet của Signal. Các session tag được tạo ra một cách xác định và giống hệt nhau ở phía người nhận và người gửi.

Bằng cách sử dụng một ratchet khóa/tag đối xứng, chúng ta loại bỏ việc sử dụng bộ nhớ để lưu trữ session tag ở phía người gửi. Chúng ta cũng loại bỏ việc tiêu thụ băng thông khi gửi các bộ tag. Việc sử dụng ở phía người nhận vẫn đáng kể, nhưng chúng ta có thể giảm thêm khi thu nhỏ session tag từ 32 byte xuống 8 byte.

Chúng tôi không sử dụng mã hóa header như được quy định (và tùy chọn) trong Signal, thay vào đó chúng tôi sử dụng session tags.

Bằng cách sử dụng DH ratchet, chúng ta đạt được forward secrecy (tính bảo mật tiến), điều mà không bao giờ được triển khai trong ElGamal/AES+SessionTags.

Lưu ý: Khóa công khai một lần của New Session không phải là một phần của ratchet, chức năng duy nhất của nó là mã hóa khóa DH ratchet ban đầu của Alice.

#### Số Thứ Tự Thông Điệp

Double Ratchet xử lý các thông điệp bị mất hoặc không đúng thứ tự bằng cách bao gồm một tag trong mỗi header thông điệp. Bên nhận tra cứu chỉ mục của tag, đây là số thông điệp N. Nếu thông điệp chứa một Message Number block với giá trị PN, bên nhận có thể xóa bất kỳ tag nào cao hơn giá trị đó trong tag set trước đó, trong khi vẫn giữ lại các tag bị bỏ qua từ tag set trước đó trong trường hợp các thông điệp bị bỏ qua đến muộn hơn.

#### Triển khai Mẫu

Chúng ta định nghĩa các cấu trúc dữ liệu và hàm sau để triển khai các ratchet này.

TAGSET_ENTRY

Một mục đơn trong TAGSET.

    INDEX

    :   An integer index, starting with 0

    SESSION_TAG

    :   An identifier to go out on the wire, 8 bytes

    SESSION_KEY

    :   A symmetric key, never goes on the wire, 32 bytes

TAGSET

Một tập hợp các TAGSET_ENTRIES.

    CREATE(key, n)

    :   Generate a new TAGSET using initial cryptographic key material
        of 32 bytes. The associated session identifier is provided. The
        initial number of of tags to create is specified; this is
        generally 0 or 1 for an outgoing session. LAST_INDEX = -1
        EXTEND(n) is called.

    EXTEND(n)

    :   Generate n more TAGSET_ENTRIES by calling EXTEND() n times.

    EXTEND()

    :   Generate one more TAGSET_ENTRY, unless the maximum number
        SESSION_TAGS have already been generated. If LAST_INDEX is
        greater than or equal to 65535, return. ++ LAST_INDEX Create a
        new TAGSET_ENTRY with the LAST_INDEX value and the calculated
        SESSION_TAG. Calls RATCHET_TAG() and (optionally) RATCHET_KEY().
        For inbound sessions, the calculation of the SESSION_KEY may be
        deferred and calculated in GET_SESSION_KEY(). Calls EXPIRE()

    EXPIRE()

    :   Remove tags and keys that are too old, or if the TAGSET size
        exceeds some limit.

    RATCHET_TAG()

    :   Calculates the next SESSION_TAG based on the last SESSION_TAG.

    RATCHET_KEY()

    :   Calculates the next SESSION_KEY based on the last SESSION_KEY.

    SESSION

    :   The associated session.

    CREATION_TIME

    :   When the TAGSET was created.

    LAST_INDEX

    :   The last TAGSET_ENTRY INDEX generated by EXTEND().

    GET_NEXT_ENTRY()

    :   Used for outgoing sessions only. EXTEND(1) is called if there
        are no remaining TAGSET_ENTRIES. If EXTEND(1) did nothing, the
        max of 65535 TAGSETS have been used, and return an error.
        Returns the next unused TAGSET_ENTRY.

    GET_SESSION_KEY(sessionTag)

    :   Used for incoming sessions only. Returns the TAGSET_ENTRY
        containing the sessionTag. If found, the TAGSET_ENTRY is
        removed. If the SESSION_KEY calculation was deferred, it is
        calculated now. If there are few TAGSET_ENTRIES remaining,
        EXTEND(n) is called.

#### 4a) DH Ratchet

Ratchets nhưng không nhanh như Signal. Chúng tôi tách biệt việc xác nhận khóa đã nhận với việc tạo khóa mới. Trong cách sử dụng thông thường, Alice và Bob sẽ mỗi người ratchet (hai lần) ngay lập tức trong một New Session, nhưng sẽ không ratchet lại nữa.

Lưu ý rằng một ratchet dành cho một hướng duy nhất, và tạo ra một chuỗi ratchet New Session tag / message key cho hướng đó. Để tạo khóa cho cả hai hướng, bạn phải ratchet hai lần.

Bạn thực hiện ratchet mỗi khi tạo và gửi một khóa mới. Bạn thực hiện ratchet mỗi khi nhận được một khóa mới.

Alice thực hiện ratchet một lần khi tạo phiên gửi đi không ràng buộc, cô ấy không tạo phiên nhận vào (không ràng buộc nghĩa là không thể trả lời).

Bob thực hiện ratchet một lần khi tạo một phiên inbound không liên kết, và không tạo phiên outbound tương ứng (không liên kết là không thể trả lời).

Alice tiếp tục gửi các thông điệp New Session (NS) đến Bob cho đến khi nhận được một trong những thông điệp New Session Reply (NSR) của Bob. Sau đó cô ấy sử dụng kết quả KDF của Payload Section trong NSR làm đầu vào cho các session ratchets (xem DH Ratchet KDF), và bắt đầu gửi các thông điệp Existing Session (ES).

Đối với mỗi thông điệp NS nhận được, Bob tạo một phiên inbound mới, sử dụng kết quả KDF của Payload Section phản hồi làm đầu vào cho ES DH Ratchet inbound và outbound mới.

Đối với mỗi phản hồi cần thiết, Bob gửi cho Alice một thông điệp NSR với phản hồi trong payload. Bob bắt buộc phải sử dụng các ephemeral key mới cho mỗi NSR.

Bob phải nhận được thông điệp ES từ Alice trên một trong các phiên kết nối đến, trước khi tạo và gửi các thông điệp ES trên phiên kết nối đi tương ứng.

Alice nên sử dụng timer để nhận tin nhắn NSR từ Bob. Nếu timer hết hạn, session nên được loại bỏ.

Để tránh cuộc tấn công KCI và/hoặc cạn kiệt tài nguyên, nơi kẻ tấn công loại bỏ các phản hồi NSR của Bob để khiến Alice tiếp tục gửi thông điệp NS, Alice nên tránh khởi tạo New Sessions với Bob sau một số lần thử lại nhất định do hết thời gian chờ.

Alice và Bob mỗi người đều thực hiện một DH ratchet cho mỗi NextKey block nhận được.

Alice và Bob mỗi người tạo ra các ratchet bộ tag mới và hai ratchet khóa đối xứng sau mỗi DH ratchet. Đối với mỗi thông điệp ES mới theo một hướng nhất định, Alice và Bob tiến hành các ratchet session tag và khóa đối xứng.

Tần suất của DH ratchets sau bước bắt tay ban đầu phụ thuộc vào cách triển khai. Mặc dù giao thức đặt giới hạn 65535 tin nhắn trước khi cần một ratchet, việc ratchet thường xuyên hơn (dựa trên số lượng tin nhắn, thời gian trôi qua, hoặc cả hai) có thể cung cấp thêm bảo mật.

Sau KDF handshake cuối cùng trên các phiên được ràng buộc, Bob và Alice phải chạy hàm Noise Split() trên CipherState kết quả để tạo ra các khóa chuỗi đối xứng và tag độc lập cho các phiên inbound và outbound.

##### ID CỦA KEY VÀ TAG SET

Số ID của bộ khóa và tag được sử dụng để nhận dạng các khóa và bộ tag. ID khóa được sử dụng trong các khối NextKey để nhận dạng khóa được gửi hoặc sử dụng. ID bộ tag được sử dụng (cùng với số thứ tự thông điệp) trong các khối ACK để nhận dạng thông điệp đang được xác nhận. Cả ID khóa và ID bộ tag đều áp dụng cho các bộ tag theo một hướng duy nhất. Số ID của khóa và bộ tag phải theo thứ tự tuần tự.

Trong các tag set đầu tiên được sử dụng cho một phiên theo mỗi hướng, ID của tag set là 0. Không có block NextKey nào được gửi, do đó không có key ID nào.

Để bắt đầu một DH ratchet, người gửi truyền một khối NextKey mới với key ID là 0. Người nhận phản hồi với một khối NextKey mới với key ID là 0. Người gửi sau đó bắt đầu sử dụng một tag set mới với tag set ID là 1.

Các bộ tag tiếp theo được tạo ra tương tự. Đối với tất cả các bộ tag được sử dụng sau khi trao đổi NextKey, số bộ tag là (1 + key ID của Alice + key ID của Bob).

ID của key và tag set bắt đầu từ 0 và tăng tuần tự. ID tag set tối đa là 65535. ID key tối đa là 32767. Khi một tag set gần cạn kiệt, bên gửi tag set phải khởi tạo một trao đổi NextKey. Khi tag set 65535 gần cạn kiệt, bên gửi tag set phải khởi tạo một phiên mới bằng cách gửi thông điệp New Session.

Với kích thước thông điệp tối đa streaming là 1730, và giả định không có truyền lại, tốc độ truyền dữ liệu tối đa lý thuyết sử dụng một tag set đơn lẻ là 1730 * 65536 ~= 108 MB. Mức tối đa thực tế sẽ thấp hơn do các lần truyền lại.

Lượng dữ liệu truyền tải tối đa về mặt lý thuyết với tất cả 65536 tag set có sẵn, trước khi phiên làm việc phải được loại bỏ và thay thế, là 64K * 108 MB ~= 6.9 TB.

##### LUỒNG THÔNG ĐIỆP DH RATCHET

Việc trao đổi khóa tiếp theo cho một tag set phải được khởi xướng bởi bên gửi các tag đó (chủ sở hữu của outbound tag set). Bên nhận (chủ sở hữu của inbound tag set) sẽ phản hồi. Đối với lưu lượng HTTP GET điển hình ở tầng ứng dụng, Bob sẽ gửi nhiều tin nhắn hơn và sẽ ratchet trước bằng cách khởi xướng trao đổi khóa; sơ đồ bên dưới cho thấy điều đó. Khi Alice ratchet, điều tương tự xảy ra theo chiều ngược lại.

Bộ tag đầu tiên được sử dụng sau quá trình bắt tay NS/NSR là tag set 0. Khi tag set 0 gần cạn kiệt, các khóa mới phải được trao đổi theo cả hai hướng để tạo ra tag set 1. Sau đó, một khóa mới chỉ được gửi theo một hướng.

Để tạo tag set 2, bên gửi tag sẽ gửi một key mới và bên nhận tag sẽ gửi ID của key cũ làm xác nhận. Cả hai bên đều thực hiện DH.

Để tạo tag set 3, bên gửi tag gửi ID của khóa cũ và yêu cầu khóa mới từ bên nhận tag. Cả hai bên đều thực hiện DH.

Các tập tag tiếp theo được tạo ra giống như tập tag 2 và 3. Số tập tag là (1 + sender key id + receiver key id).

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

Sau khi DH ratchet hoàn thành cho một inbound tagset, và một inbound tagset mới được tạo ra, bên nhận nên lắng nghe các tag trong cả hai tagset, và xóa tagset cũ sau một khoảng thời gian ngắn, khoảng 3 phút.

Tóm tắt về tiến trình tag set và key ID được trình bày trong bảng dưới đây. * cho biết rằng một khóa mới được tạo ra.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">New Tag Set ID</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Sender key ID</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Rcvr key ID</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">n/a</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">n/a</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0 *</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0 *</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1 *</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1 *</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">2 *</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">2 *</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">...</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">...</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">...</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">65534</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32767 *</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32766</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">65535</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32767</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32767 *</td>
</tr>
</table>
Số ID của key và tag set phải tuần tự.

##### DH INITIALIZATION KDF

Đây là định nghĩa của DH_INITIALIZE(rootKey, k) cho một hướng duy nhất. Nó tạo ra một tagset và một "root key tiếp theo" được sử dụng cho một DH ratchet tiếp theo nếu cần thiết.

Chúng tôi sử dụng khởi tạo DH ở ba nơi. Đầu tiên, chúng tôi sử dụng nó để tạo một bộ tag cho New Session Replies. Thứ hai, chúng tôi sử dụng nó để tạo hai bộ tag, một cho mỗi hướng, để sử dụng trong các thông điệp Existing Session. Cuối cùng, chúng tôi sử dụng nó sau một DH Ratchet để tạo một bộ tag mới theo một hướng duy nhất cho các thông điệp Existing Session bổ sung.

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
##### DH RATCHET KDF

Điều này được sử dụng sau khi các khóa DH mới được trao đổi trong các khối NextKey, trước khi tagset bị cạn kiệt.

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
#### 4b) Session Tag Ratchet

Ratchets cho mọi tin nhắn, như trong Signal. Session tag ratchet được đồng bộ với symmetric key ratchet, nhưng receiver key ratchet có thể "chậm lại" để tiết kiệm bộ nhớ.

Transmitter thực hiện ratchet một lần cho mỗi tin nhắn được truyền đi. Không cần lưu trữ thêm tag nào. Transmitter cũng phải giữ một bộ đếm cho 'N', số thứ tự tin nhắn của tin nhắn trong chuỗi hiện tại. Giá trị 'N' được bao gồm trong tin nhắn được gửi. Xem định nghĩa khối Message Number.

Bên nhận phải ratchet tiến lên theo kích thước cửa sổ tối đa và lưu trữ các tag trong một "tag set", được liên kết với phiên làm việc. Sau khi nhận được, tag đã lưu trữ có thể được loại bỏ, và nếu không có tag nào trước đó chưa được nhận, cửa sổ có thể được tiến lên. Bên nhận nên giữ giá trị 'N' được liên kết với mỗi session tag, và kiểm tra rằng số trong tin nhắn gửi đi khớp với giá trị này. Xem định nghĩa khối Message Number.

##### KDF

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
#### 4c) Symmetric Key Ratchet

Ratchets cho mỗi tin nhắn, giống như trong Signal. Mỗi khóa đối xứng có một số thứ tự tin nhắn và session tag liên quan. Session key ratchet được đồng bộ hóa với symmetric tag ratchet, nhưng receiver key ratchet có thể "chậm lại" để tiết kiệm bộ nhớ.

Transmitter ratchet một lần cho mỗi tin nhắn được truyền. Không cần lưu trữ thêm khóa nào khác.

Khi người nhận nhận được session tag, nếu nó chưa ratchet symmetric key ratchet về phía trước đến khóa liên quan, nó phải "bắt kịp" đến khóa liên quan. Người nhận có thể sẽ cache các khóa cho bất kỳ tag trước đó nào chưa được nhận. Một khi đã nhận được, khóa đã lưu trữ có thể được loại bỏ, và nếu không có tag trước đó nào chưa được nhận, cửa sổ có thể được tiến lên.

Để tăng hiệu quả, session tag và symmetric key ratchets được tách riêng để session tag ratchet có thể chạy trước symmetric key ratchet. Điều này cũng cung cấp thêm tính bảo mật, vì các session tag được truyền qua mạng.

##### KDF

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
### 5) Tải trọng

Điều này thay thế định dạng phần AES được định nghĩa trong đặc tả ElGamal/AES+SessionTags.

Điều này sử dụng cùng định dạng block như được định nghĩa trong đặc tả [NTCP2](/docs/specs/ntcp2/). Các loại block riêng lẻ được định nghĩa khác nhau.

Có những lo ngại rằng việc khuyến khích các nhà phát triển chia sẻ mã nguồn có thể dẫn đến các vấn đề phân tích cú pháp. Các nhà phát triển nên cân nhắc cẩn thận những lợi ích và rủi ro của việc chia sẻ mã nguồn, đồng thời đảm bảo rằng các quy tắc sắp xếp thứ tự và khối hợp lệ phải khác nhau cho hai ngữ cảnh.

#### Payload Section Dữ liệu đã giải mã

Độ dài mã hóa là phần còn lại của dữ liệu. Độ dài sau giải mã ít hơn 16 so với độ dài mã hóa. Tất cả các loại khối đều được hỗ trợ. Nội dung điển hình bao gồm các khối sau:

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Payload Block Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Type Number</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Block Length</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">DateTime</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">7</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Termination (TBD)</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">9 typ.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Options (TBD)</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">21+</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Message Number (TBD)</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">6</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">TBD</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Next Key</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">3 or 35</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">ACK</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">8</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4 typ.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">ACK Request</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">9</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Garlic Clove</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">11</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">varies</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Padding</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">254</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">varies</td>
</tr>
</table>
#### Dữ liệu không mã hóa

Có không hoặc nhiều block trong frame được mã hóa. Mỗi block chứa một định danh một byte, một độ dài hai byte, và không hoặc nhiều byte dữ liệu.

Để đảm bảo khả năng mở rộng, các bộ nhận PHẢI bỏ qua các block có số loại không xác định và xử lý chúng như padding.

Dữ liệu mã hóa tối đa 65535 byte, bao gồm header xác thực 16 byte, vì vậy dữ liệu chưa mã hóa tối đa là 65519 byte.

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
#### Quy Tắc Sắp Xếp Khối

Trong thông điệp New Session, khối DateTime là bắt buộc và phải là khối đầu tiên.

Các khối được cho phép khác:

- Garlic Clove (type 11)
- Tùy chọn (type 5)
- Padding (type 254)

Trong thông điệp New Session Reply, không có block nào được yêu cầu.

Các khối được phép khác:

- Garlic Clove (type 11)
- Options (type 5)
- Padding (type 254)

Không cho phép các khối khác. Padding, nếu có, phải là khối cuối cùng.

Trong thông điệp Existing Session, không có block nào được yêu cầu, và thứ tự không được chỉ định, ngoại trừ các yêu cầu sau:

Termination, nếu có, phải là block cuối cùng trừ Padding. Padding, nếu có, phải là block cuối cùng.

Có thể có nhiều khối Garlic Clove trong một khung đơn. Có thể có tối đa hai khối Next Key trong một khung đơn. Không được phép có nhiều khối Padding trong một khung đơn. Các loại khối khác có lẽ sẽ không có nhiều khối trong một khung đơn, nhưng điều này không bị cấm.

#### DateTime

Thời hạn hết hạn. Hỗ trợ ngăn chặn tấn công replay. Bob phải xác thực rằng thông điệp là gần đây, sử dụng timestamp này. Bob phải triển khai Bloom filter hoặc cơ chế khác để ngăn chặn tấn công replay, nếu thời gian là hợp lệ. Bob cũng có thể sử dụng kiểm tra phát hiện replay trước đó cho khóa ephemeral trùng lặp (trước hoặc sau khi giải mã Elligator2) để phát hiện và loại bỏ các thông điệp NS trùng lặp gần đây trước khi giải mã. Thường chỉ được bao gồm trong các thông điệp New Session.

```
+----+----+----+----+----+----+----+
| 0  |    4    |     timestamp     |
+----+----+----+----+----+----+----+

blk :: 0
size :: 2 bytes, big endian, value = 4
timestamp :: Unix timestamp, unsigned seconds.
             Wraps around in 2106
```
#### Garlic Clove

Một Garlic Clove đã giải mã duy nhất như được chỉ định trong [I2NP](/docs/specs/i2np/), với các sửa đổi để loại bỏ các trường không sử dụng hoặc dư thừa. Cảnh báo: Định dạng này khác đáng kể so với định dạng dành cho ElGamal/AES. Mỗi clove là một khối payload riêng biệt. Các Garlic Clove không thể bị phân mảnh qua các khối hoặc qua các khung ChaChaPoly.

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
       the Garlic Clove section of [I2NP]_.
       Length varies but is typically 1, 33, or 37 bytes

type :: I2NP message type

Message_ID :: 4 byte `Integer` I2NP message ID

Expiration :: 4 bytes, seconds since the epoch
```
Ghi chú:

- Các nhà triển khai phải đảm bảo rằng khi đọc một block, dữ liệu bị lỗi hoặc độc hại sẽ không gây ra việc đọc vượt quá sang block tiếp theo.
- Định dạng Clove Set được chỉ định trong [I2NP](/docs/specs/i2np/) không được sử dụng. Mỗi clove được chứa trong block riêng của nó.
- Header thông điệp I2NP có độ dài 9 byte, với định dạng giống hệt như được sử dụng trong [NTCP2](/docs/specs/ntcp2/).
- Certificate, Message ID và Expiration từ định nghĩa Garlic Message trong [I2NP](/docs/specs/i2np/) không được bao gồm.
- Certificate, Clove ID và Expiration từ định nghĩa Garlic Clove trong [I2NP](/docs/specs/i2np/) không được bao gồm.

#### Chấm dứt

Việc triển khai là tùy chọn. Hủy phiên. Đây phải là khối không phải padding cuối cùng trong khung. Không có thêm tin nhắn nào sẽ được gửi trong phiên này.

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
#### Tùy chọn

CHƯA ĐƯỢC TRIỂN KHAI, cần nghiên cứu thêm. Truyền các tùy chọn đã cập nhật. Tùy chọn bao gồm các tham số khác nhau cho phiên. Xem phần Phân tích Độ dài Session Tag bên dưới để biết thêm thông tin.

Khối tùy chọn có thể có độ dài thay đổi, vì more_options có thể hiện diện.

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
SOTW là khuyến nghị của người gửi cho người nhận về cửa sổ tag đến của người nhận (độ nhìn trước tối đa). RITW là tuyên bố của người gửi về cửa sổ tag đến (độ nhìn trước tối đa) mà anh ta dự định sử dụng. Mỗi bên sau đó sẽ thiết lập hoặc điều chỉnh độ nhìn trước dựa trên một số tính toán tối thiểu hoặc tối đa hoặc các tính toán khác.

Ghi chú:

- Hy vọng sẽ không bao giờ cần hỗ trợ cho độ dài session tag không mặc định.
- Cửa sổ tag là MAX_SKIP trong tài liệu Signal.

Vấn đề:

- Đàm phán các tùy chọn vẫn chưa được xác định.
- Các giá trị mặc định chưa được xác định.
- Các tùy chọn padding và delay được sao chép từ NTCP2, nhưng những tùy chọn đó
  vẫn chưa được triển khai đầy đủ hoặc nghiên cứu ở đó.

#### Số Thứ Tự Tin Nhắn

Việc triển khai là tùy chọn. Độ dài (số lượng tin nhắn được gửi) trong bộ thẻ trước đó (PN). Bên nhận có thể xóa ngay lập tức các thẻ cao hơn PN từ bộ thẻ trước đó. Bên nhận có thể hết hạn các thẻ nhỏ hơn hoặc bằng PN từ bộ thẻ trước đó sau một thời gian ngắn (ví dụ: 2 phút).

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
  Điều này tương tự như những gì Signal thực hiện, nhưng trong Signal, PN và N nằm trong
  header. Ở đây, chúng nằm trong phần thân thông điệp được mã hóa.
- Không gửi khối này trong tag set 0, bởi vì không có tag
  set trước đó.

#### Khóa Công Khai DH Ratchet Tiếp Theo

Khóa DH ratchet tiếp theo nằm trong payload và là tùy chọn. Chúng ta không ratchet mỗi lần. (Điều này khác với signal, nơi nó nằm trong header và được gửi mỗi lần)

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

- Key ID là một bộ đếm tăng dần cho khóa cục bộ được sử dụng cho tag set đó, bắt đầu từ 0.
- ID không được thay đổi trừ khi khóa thay đổi.
- Có thể không thực sự cần thiết, nhưng hữu ích cho việc debug. Signal không sử dụng key ID.
- Key ID tối đa là 32767.
- Trong trường hợp hiếm khi các tag set ở cả hai hướng đều đang thực hiện ratcheting cùng lúc, một frame sẽ chứa hai Next Key block, một cho forward key và một cho reverse key.
- Số ID của Key và tag set phải tuần tự.
- Xem phần DH Ratchet ở trên để biết chi tiết.

#### Xác nhận

Điều này chỉ được gửi nếu một khối yêu cầu ack đã được nhận. Có thể có nhiều ack để xác nhận nhiều tin nhắn.

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
- Trong các bộ tag đầu tiên được sử dụng cho một phiên theo mỗi hướng, ID bộ tag là 0.
- Không có khối NextKey nào được gửi, vì vậy không có key ID nào.
- Đối với tất cả các bộ tag được sử dụng sau khi trao đổi NextKey, số bộ tag là (1 + key ID của Alice + key ID của Bob).

#### Yêu cầu Xác nhận

Yêu cầu một xác nhận trong băng tần. Để thay thế Thông điệp DeliveryStatus ngoài băng tần trong Garlic Clove.

Nếu một ack rõ ràng được yêu cầu, ID tagset hiện tại và số thứ tự thông điệp (N) sẽ được trả về trong một khối ack.

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
#### Đệm

Tất cả padding đều nằm bên trong các khung AEAD. TODO Padding bên trong AEAD nên tuân thủ gần đúng các tham số đã thương lượng. TODO Alice đã gửi các tham số tx/rx min/max mà cô ấy yêu cầu trong thông điệp NS. TODO Bob đã gửi các tham số tx/rx min/max mà anh ấy yêu cầu trong thông điệp NSR. Các tùy chọn đã cập nhật có thể được gửi trong giai đoạn dữ liệu. Xem thông tin khối tùy chọn ở trên.

Nếu có mặt, đây phải là khối cuối cùng trong frame.

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

- Padding toàn bộ bằng số không là được, vì nó sẽ được mã hóa.
- Các chiến lược padding sẽ được quyết định sau (TBD).
- Các frame chỉ chứa padding được cho phép.
- Padding mặc định là 0-15 byte.
- Xem khối tùy chọn để biết về thương lượng tham số padding
- Xem khối tùy chọn để biết về các tham số padding tối thiểu/tối đa
- Phản hồi của router khi vi phạm padding đã thương lượng phụ thuộc vào
  implementation.

#### Các loại khối khác

Các implementation nên bỏ qua những loại block không xác định để đảm bảo khả năng tương thích với phiên bản tương lai.

#### Công việc tương lai

- Độ dài padding có thể được quyết định trên cơ sở từng thông điệp và các ước tính về phân bố độ dài, hoặc nên thêm các độ trễ ngẫu nhiên. Những biện pháp đối phó này được bao gồm để chống lại DPI, vì kích thước thông điệp có thể tiết lộ rằng lưu lượng I2P đang được truyền tải bởi giao thức vận chuyển. Lược đồ padding chính xác là một lĩnh vực nghiên cứu trong tương lai, Phụ lục A cung cấp thêm thông tin về chủ đề này.

## Các Mẫu Sử Dụng Điển Hình

### HTTP GET

Đây là trường hợp sử dụng phổ biến nhất, và hầu hết các trường hợp sử dụng streaming không phải HTTP cũng sẽ giống hệt trường hợp này. Một thông điệp ban đầu nhỏ được gửi đi, một phản hồi theo sau, và các thông điệp bổ sung được gửi theo cả hai hướng.

Một HTTP GET thường vừa trong một I2NP message duy nhất. Alice gửi một yêu cầu nhỏ với một Session message mới duy nhất, đi kèm một reply leaseset. Alice bao gồm ratchet ngay lập tức đến khóa mới. Bao gồm chữ ký để liên kết với điểm đến. Không yêu cầu xác nhận.

Bob thực hiện ratchet ngay lập tức.

Alice thực hiện ratchet ngay lập tức.

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
### HTTP POST

Alice có ba lựa chọn:

1)  Chỉ gửi thông điệp đầu tiên (kích thước cửa sổ = 1), như trong HTTP GET. Không

    recommended.
2)  Gửi tối đa streaming window, nhưng sử dụng cùng Elligator2-encoded

    cleartext public key. All messages contain same next public key
    (ratchet). This will be visible to OBGW/IBEP because they all start
    with the same cleartext. Things proceed as in 1). Not recommended.
3)  Triển khai được khuyến nghị. Gửi tối đa streaming window, nhưng sử dụng một

    different Elligator2-encoded cleartext public key (session) for
    each. All messages contain same next public key (ratchet). This will
    not be visible to OBGW/IBEP because they all start with different
    cleartext. Bob must recognize that they all contain the same next
    public key, and respond to all with the same ratchet. Alice uses
    that next public key and continues.

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
### Datagram Có Thể Trả Lời

Một tin nhắn đơn lẻ, với một phản hồi duy nhất được mong đợi. Các tin nhắn hoặc phản hồi bổ sung có thể được gửi.

Tương tự như HTTP GET, nhưng với các tùy chọn nhỏ hơn cho kích thước cửa sổ session tag và thời gian tồn tại. Có thể không yêu cầu ratchet.

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
### Nhiều Raw Datagram

Nhiều thông điệp ẩn danh, không mong đợi phản hồi.

Trong kịch bản này, Alice yêu cầu một phiên, nhưng không có ràng buộc. Tin nhắn phiên mới được gửi. Không có reply LS nào được gói kèm. Một reply DSM được gói kèm (đây là trường hợp sử dụng duy nhất yêu cầu DSM được gói kèm). Không có khóa tiếp theo được bao gồm. Không có reply hoặc ratchet nào được yêu cầu. Không có ratchet nào được gửi. Tùy chọn đặt cửa sổ session tags về zero.

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
### Datagram Thô Đơn

Một tin nhắn ẩn danh đơn lẻ, không mong đợi phản hồi.

Tin nhắn một lần được gửi. Không có reply LS hoặc DSM được gộp chung. Không bao gồm khóa tiếp theo. Không yêu cầu phản hồi hoặc ratchet. Không có ratchet được gửi. Các tùy chọn đặt cửa sổ session tags về không.

```
Alice                           Bob

  One-Time Message (1d)   ------------------->
  with bundled message
  without bundled LS
  without bundled Delivery Status Message
```
### Phiên Tồn Tại Lâu Dài

Các session tồn tại lâu dài có thể thực hiện ratchet, hoặc yêu cầu ratchet, bất cứ lúc nào để duy trì tính bảo mật thuận chiều (forward secrecy) từ thời điểm đó trở đi. Các session phải thực hiện ratchet khi chúng tiến gần đến giới hạn số tin nhắn gửi trên mỗi session (65535).

## Các Cân nhắc Triển khai

### Phòng thủ

Như với giao thức ElGamal/AES+SessionTag hiện tại, các triển khai phải giới hạn lưu trữ session tag và bảo vệ chống lại các cuộc tấn công làm cạn kiệt bộ nhớ.

Một số chiến lược được khuyến nghị bao gồm:

- Giới hạn cứng về số lượng session tags được lưu trữ
- Hết hạn tích cực của các phiên kết nối đến không hoạt động khi chịu áp lực bộ nhớ
- Giới hạn số lượng phiên kết nối đến được liên kết với một đích xa duy nhất
- Giảm thích ứng cửa sổ session tag và xóa các tags cũ không sử dụng khi chịu áp lực bộ nhớ
- Từ chối ratchet khi được yêu cầu, nếu chịu áp lực bộ nhớ

### Tham số

Các tham số và thời gian chờ được khuyến nghị:

- Kích thước tagset NSR: 12 tsmin và tsmax
- Kích thước tagset ES 0: tsmin 24, tsmax 160
- Kích thước tagset ES (1+): 160 tsmin và tsmax
- Thời gian chờ tagset NSR: 3 phút cho receiver
- Thời gian chờ tagset ES: 8 phút cho sender, 10 phút cho receiver
- Xóa tagset ES trước đó sau: 3 phút
- Tagset look ahead của tag N: min(tsmax, tsmin + N/4)
- Tagset trim behind tag N: min(tsmax, tsmin + N/4) / 2
- Gửi key tiếp theo tại tag: 4096
- Gửi key tiếp theo sau thời gian sống tagset: TBD
- Thay thế session nếu NS nhận được sau: 3 phút
- Độ lệch đồng hồ tối đa: -5 phút đến +2 phút
- Thời gian bộ lọc replay NS: 5 phút
- Kích thước padding: 0-15 bytes (các chiến lược khác TBD)

### Phân loại

Sau đây là các khuyến nghị để phân loại các thông điệp đến.

#### Chỉ X25519

Trên một tunnel được sử dụng duy nhất với giao thức này, thực hiện xác thực như hiện đang làm với ElGamal/AES+SessionTags:

Đầu tiên, xử lý dữ liệu ban đầu như một session tag, và tra cứu session tag đó. Nếu tìm thấy, giải mã bằng cách sử dụng dữ liệu đã lưu trữ liên kết với session tag đó.

Nếu không tìm thấy, coi dữ liệu ban đầu là khóa công khai DH và nonce. Thực hiện phép toán DH và KDF được chỉ định, và thử giải mã dữ liệu còn lại.

#### X25519 Chia sẻ với ElGamal/AES+SessionTags

Trên một tunnel hỗ trợ cả giao thức này và ElGamal/AES+SessionTags, phân loại các thông điệp đến như sau:

Do có lỗ hổng trong đặc tả ElGamal/AES+SessionTags, khối AES không được đệm đến độ dài ngẫu nhiên khác chia hết cho 16. Do đó, độ dài của các thông điệp Existing Session chia cho 16 luôn dư 0, và độ dài của các thông điệp New Session chia cho 16 luôn dư 2 (vì khối ElGamal dài 514 byte).

Nếu độ dài mod 16 không phải là 0 hoặc 2, hãy xem dữ liệu ban đầu như một session tag và tìm kiếm session tag đó. Nếu tìm thấy, hãy giải mã bằng cách sử dụng dữ liệu đã lưu trữ được liên kết với session tag đó.

Nếu không tìm thấy, và độ dài mod 16 không phải là 0 hoặc 2, coi dữ liệu ban đầu như một khóa công khai DH và nonce. Thực hiện phép toán DH và KDF được chỉ định, và cố gắng giải mã dữ liệu còn lại. (dựa trên tỷ lệ lưu lượng tương đối, và chi phí tương đối của các phép toán DH X25519 và ElGamal, bước này có thể được thực hiện cuối cùng thay vì như vậy)

Ngược lại, nếu độ dài mod 16 bằng 0, hãy xem dữ liệu ban đầu như một session tag ElGamal/AES, và tra cứu session tag đó. Nếu tìm thấy, hãy giải mã bằng dữ liệu đã lưu trữ được liên kết với session tag đó.

Nếu không tìm thấy, và dữ liệu có độ dài ít nhất 642 (514 + 128) byte, và độ dài chia 16 dư 2, hãy coi dữ liệu ban đầu là một khối ElGamal. Thử giải mã dữ liệu còn lại.

Lưu ý rằng nếu đặc tả ElGamal/AES+SessionTag được cập nhật để cho phép padding không phải mod-16, thì mọi thứ sẽ cần được thực hiện theo cách khác.

### Truyền lại và Chuyển đổi Trạng thái

Lớp ratchet không thực hiện truyền lại, và ngoại trừ hai trường hợp, không sử dụng bộ đếm thời gian cho việc truyền tải. Bộ đếm thời gian cũng được yêu cầu cho thời gian chờ của tagset.

Timer truyền tải chỉ được sử dụng để gửi NSR và để trả lời bằng ES khi một ES nhận được chứa yêu cầu ACK. Thời gian chờ khuyến nghị là một giây. Trong hầu hết các trường hợp, lớp cao hơn (datagram hoặc streaming) sẽ trả lời, buộc phải có NSR hoặc ES, và timer có thể bị hủy. Nếu timer kích hoạt, hãy gửi payload trống với NSR hoặc ES.

#### Phản hồi tầng Ratchet

Các triển khai ban đầu dựa vào lưu lượng hai chiều ở các lớp cao hơn. Có nghĩa là, các triển khai giả định rằng lưu lượng theo hướng ngược lại sẽ sớm được truyền tải, điều này sẽ buộc phải có bất kỳ phản hồi cần thiết nào ở lớp ECIES.

Tuy nhiên, một số lưu lượng có thể là đơn hướng hoặc có băng thông rất thấp, do đó không có lưu lượng tầng cao hơn để tạo ra phản hồi kịp thời.

Việc nhận các tin nhắn NS và NSR yêu cầu phản hồi; việc nhận các khối ACK Request và Next Key cũng yêu cầu phản hồi.

Các triển khai nên khởi động một bộ đếm thời gian khi nhận được một trong những tin nhắn này yêu cầu phản hồi, và tạo ra một phản hồi "rỗng" (không có khối Garlic Clove) tại lớp ECIES nếu không có lưu lượng ngược nào được gửi trong một khoảng thời gian ngắn (ví dụ: 1 giây).

Cũng có thể thích hợp sử dụng timeout ngắn hơn nữa cho các phản hồi đối với thông điệp NS và NSR, để chuyển lưu lượng sang các thông điệp ES hiệu quả càng sớm càng tốt.

#### Ràng buộc NS cho NSR

Tại lớp ratchet, với vai trò Bob, Alice chỉ được biết đến qua static key. Tin nhắn NS được xác thực ([Noise](https://noiseprotocol.org/noise.html) IK sender authentication 1). Tuy nhiên, điều này không đủ để lớp ratchet có thể gửi bất cứ thứ gì cho Alice, vì việc định tuyến mạng yêu cầu một Destination đầy đủ.

Trước khi NSR có thể được gửi, Destination đầy đủ của Alice phải được khám phá bởi lớp ratchet hoặc một giao thức có thể trả lời ở lớp cao hơn, có thể là [Datagrams](/docs/specs/datagrams/) có thể trả lời hoặc [Streaming](/docs/specs/streaming/). Sau khi tìm thấy Leaseset cho Destination đó, Leaseset đó sẽ chứa cùng một khóa tĩnh như được chứa trong NS.

Thông thường, tầng cao hơn sẽ phản hồi, buộc phải thực hiện tra cứu cơ sở dữ liệu mạng về LeaseSet của Alice thông qua Destination Hash của Alice. LeaseSet đó hầu như luôn được tìm thấy cục bộ, bởi vì NS chứa một khối Garlic Clove, chứa thông điệp Database Store, chứa LeaseSet của Alice.

Để Bob chuẩn bị gửi NSR tầng ratchet và liên kết phiên đang chờ với Destination của Alice, Bob nên "bắt" Destination khi xử lý tải trọng NS. Nếu tìm thấy một thông điệp Database Store chứa Leaseset với khóa khớp với khóa tĩnh trong NS, phiên đang chờ sẽ được liên kết với Destination đó, và Bob biết nơi gửi bất kỳ NSR nào nếu bộ đếm thời gian phản hồi hết hạn. Đây là cách triển khai được khuyến nghị.

Một thiết kế thay thế là duy trì một bộ nhớ đệm hoặc cơ sở dữ liệu nơi khóa tĩnh được ánh xạ tới một Destination. Tính bảo mật và tính thực tiễn của phương pháp này là chủ đề cần nghiên cứu thêm.

Cả thông số kỹ thuật này và các thông số khác đều không yêu cầu nghiêm ngặt rằng mọi NS phải chứa Leaseset của Alice. Tuy nhiên, trên thực tế, nó nên như vậy. Thời gian chờ tagset sender ES được khuyến nghị (8 phút) ngắn hơn thời gian chờ Leaseset tối đa (10 phút), vì vậy có thể có một khoảng thời gian nhỏ mà phiên trước đó đã hết hạn, Alice nghĩ rằng Bob vẫn còn Leaseset hợp lệ của cô ấy, và không gửi Leaseset mới cùng với NS mới. Đây là một chủ đề cần nghiên cứu thêm.

#### Nhiều Tin nhắn NS

Nếu không nhận được phản hồi NSR trước khi lớp cao hơn (datagram hoặc streaming) gửi thêm dữ liệu, có thể là một lần truyền lại, Alice phải soạn một NS mới, sử dụng một khóa tạm thời mới. Không được tái sử dụng khóa tạm thời từ bất kỳ NS trước đó nào. Alice phải duy trì trạng thái handshake bổ sung và tagset nhận được suy xuất, để nhận các tin nhắn NSR phản hồi lại bất kỳ NSR nào đã được gửi.

Các triển khai có thể giới hạn tổng số thông điệp NS được gửi, hoặc tốc độ gửi thông điệp NS, bằng cách xếp hàng đợi hoặc loại bỏ các thông điệp lớp cao hơn trước khi chúng được gửi.

Trong một số tình huống nhất định, khi chịu tải cao hoặc trong các kịch bản tấn công cụ thể, Bob có thể cần xếp hàng, loại bỏ hoặc giới hạn các thông điệp NS rõ ràng mà không cố gắng giải mã, để tránh cuộc tấn công cạn kiệt tài nguyên.

Đối với mỗi NS nhận được, Bob tạo ra một NSR outbound tagset, gửi một NSR, thực hiện split(), và tạo ra các inbound và outbound ES tagsets. Tuy nhiên, Bob không gửi bất kỳ thông điệp ES nào cho đến khi thông điệp ES đầu tiên trên inbound tagset tương ứng được nhận. Sau đó, Bob có thể loại bỏ tất cả các trạng thái handshake và tagsets cho bất kỳ NS nào khác đã nhận hoặc NSR đã gửi, hoặc cho phép chúng hết hạn trong thời gian ngắn. Không sử dụng NSR tagsets cho các thông điệp ES.

Đây là chủ đề cần nghiên cứu thêm về việc liệu Bob có thể chọn gửi các thông điệp ES một cách suy đoán ngay sau NSR, thậm chí trước khi nhận được ES đầu tiên từ Alice. Trong một số tình huống và mẫu lưu lượng nhất định, điều này có thể tiết kiệm đáng kể băng thông và CPU. Chiến lược này có thể dựa trên các phương pháp heuristic như mẫu lưu lượng, tỷ lệ phần trăm ES nhận được trên tagset của phiên đầu tiên, hoặc các dữ liệu khác.

#### Nhiều Thông Điệp NSR

Đối với mỗi thông điệp NS nhận được, cho đến khi nhận được thông điệp ES, Bob phải trả lời bằng một NSR mới, hoặc do lưu lượng tầng cao hơn được gửi, hoặc do hết thời gian gửi NSR.

Mỗi NSR sử dụng trạng thái handshake và tagset tương ứng với NS đến. Bob phải duy trì trạng thái handshake và tagset cho tất cả các thông điệp NS nhận được, cho đến khi nhận được thông điệp ES.

Các triển khai có thể giới hạn tổng số thông điệp NSR được gửi, hoặc tốc độ gửi thông điệp NSR, bằng cách xếp hàng đợi hoặc loại bỏ các thông điệp từ lớp cao hơn trước khi chúng được gửi. Những giới hạn này có thể được áp dụng khi do các thông điệp NS đến gây ra, hoặc do lưu lượng truy cập đi ra bổ sung từ lớp cao hơn.

Trong một số tình huống nhất định, khi chịu tải cao hoặc trong các kịch bản tấn công nhất định, có thể thích hợp để Alice xếp hàng đợi, loại bỏ hoặc giới hạn các thông điệp NSR mà không cần cố gắng giải mã, để tránh cuộc tấn công cạn kiệt tài nguyên. Các giới hạn này có thể áp dụng tổng thể trên tất cả các phiên, theo từng phiên, hoặc cả hai.

Khi Alice nhận được NSR, Alice thực hiện split() để sinh ra các khóa phiên ES. Alice nên đặt bộ đếm thời gian và gửi thông điệp ES trống nếu lớp cao hơn không gửi bất kỳ lưu lượng nào, thường là trong vòng một giây.

Các tagset NSR đến khác có thể được loại bỏ sớm hoặc được phép hết hạn, nhưng Alice nên giữ chúng trong một thời gian ngắn để giải mã bất kỳ thông điệp NSR nào khác được nhận.

### Ngăn chặn tấn công phát lại

Bob phải triển khai bộ lọc Bloom hoặc cơ chế khác để ngăn chặn các cuộc tấn công replay NS, nếu DateTime được bao gồm là gần đây, và từ chối các thông điệp NS có DateTime quá cũ. Bob cũng có thể sử dụng kiểm tra phát hiện replay trước đó cho khóa ephemeral trùng lặp (trước hoặc sau khi giải mã Elligator2) để phát hiện và loại bỏ các thông điệp NS trùng lặp gần đây trước khi giải mã.

Các thông điệp NSR và ES có khả năng ngăn chặn replay tự nhiên vì session tag chỉ được sử dụng một lần.

Garlic messages cũng có khả năng ngăn chặn replay nếu router triển khai bộ lọc Bloom toàn router dựa trên ID tin nhắn I2NP.

## Thay đổi liên quan

Tra cứu Cơ sở dữ liệu từ ECIES Destinations: Xem [Prop154](/proposals/154-ratchet/), hiện đã được tích hợp trong [I2NP](/docs/specs/i2np/) cho phiên bản 0.9.46.

Đặc tả này yêu cầu hỗ trợ LS2 để xuất bản khóa công khai X25519 cùng với leaseset. Không cần thay đổi gì đối với các đặc tả LS2 trong [I2NP](/docs/specs/i2np/). Tất cả hỗ trợ đã được thiết kế, chỉ định và triển khai trong [Prop123](/proposals/123-new-netdb-entries/) được triển khai trong phiên bản 0.9.38.

Đặc tả này yêu cầu một thuộc tính phải được thiết lập trong các tùy chọn I2CP để được kích hoạt. Tất cả hỗ trợ đã được thiết kế, đặc tả và triển khai trong [Prop123](/proposals/123-new-netdb-entries/) được thực hiện trong phiên bản 0.9.38.

Tùy chọn cần thiết để kích hoạt ECIES là một thuộc tính I2CP duy nhất cho I2CP, BOB, SAM, hoặc i2ptunnel.

Các giá trị điển hình là i2cp.leaseSetEncType=4 chỉ cho ECIES, hoặc i2cp.leaseSetEncType=4,0 cho khóa kép ECIES và ElGamal.

## Khả năng tương thích

Bất kỳ router nào hỗ trợ LS2 với dual keys (0.9.38 trở lên) đều có thể kết nối đến các điểm đích có dual keys.

Các điểm đến chỉ sử dụng ECIES yêu cầu phần lớn các floodfill được cập nhật lên 0.9.46 để nhận được phản hồi tra cứu được mã hóa. Xem [Prop154](/proposals/154-ratchet/).

Các điểm đến chỉ sử dụng ECIES chỉ có thể kết nối với các điểm đến khác cũng chỉ sử dụng ECIES hoặc sử dụng khóa kép.

## Tham khảo

- [Common](/docs/specs/common-structures/)
- [CRYPTO-ELG](/docs/specs/cryptography/#elgamal)
- [Datagrams](/docs/specs/datagrams/)
- [ECIES-HYBRID](/docs/specs/ecies-hybrid/)
- [ElG-AES](/docs/specs/elgamal-aes/)
- [Elligator2](https://elligator.cr.yp.to/elligator-20130828.pdf) - Xem thêm [bài viết Elligator](https://www.imperialviolet.org/2013/12/25/elligator.html) và mã OBFS4
- [GARLICSPEC](/docs/overview/garlic-routing/)
- [I2CP](/docs/specs/i2cp/)
- [I2NP](/docs/specs/i2np/)
- [NOISE](https://noiseprotocol.org/noise.html)
- [NTCP2](/docs/specs/ntcp2/)
- [Prop111](/proposals/111-ntcp2/)
- [Prop123](/proposals/123-new-netdb-entries/)
- [Prop142](/proposals/142-ecies-template/)
- [Prop144](/proposals/144-ecies-x25519/)
- [Prop145](/proposals/145-ecies-ecdh-aes/)
- [Prop152](/proposals/152-ecies-config/)
- [Prop153](/proposals/153-chacha20-layer/)
- [Prop154](/proposals/154-ratchet/)
- [RFC-2104](https://tools.ietf.org/html/rfc2104)
- [RFC-4880-S5.1](https://tools.ietf.org/html/rfc4880#section-5.1)
- [RFC-5869](https://tools.ietf.org/html/rfc5869)
- [RFC-7539](https://tools.ietf.org/html/rfc7539)
- [RFC-7748](https://tools.ietf.org/html/rfc7748)
- [RFC-7905](https://tools.ietf.org/html/rfc7905)
- [Signal](https://signal.org/docs/specifications/doubleratchet/)
- [SSU](/docs/transport/ssu/)
- [SSU2](/docs/specs/ssu2/)
- [STS](https://en.wikipedia.org/wiki/Station-to-Station_protocol) - Diffie, W.; van Oorschot P. C.; Wiener M. J., Authentication and Authenticated Key Exchanges
- [Streaming](/docs/specs/streaming/)
