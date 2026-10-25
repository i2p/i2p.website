---
title: "NTCP (TCP dựa trên NIO)"
description: "Giao thức truyền tải TCP dựa trên Java NIO cũ cho I2P, đã được thay thế bằng NTCP2"
slug: "ntcp"
aliases:
  - "/vi/docs/transport/ntcp"
  - "/vi/docs/transport/ntcp/"
  - "/vi/docs/ntcp"
  - "/vi/docs/ntcp/"
  - "/vi/ntcp"
  - "/vi/ntcp/"
lastUpdated: "2021-10"
accurateFor: "0.9.52"
---

ĐÃ LỖI THỜI, KHÔNG CÒN ĐƯỢC HỖ TRỢ. Bị vô hiệu hóa mặc định từ phiên bản 0.9.40 2019-05. Hỗ trợ đã bị loại bỏ từ phiên bản 0.9.50 2021-05. Được thay thế bởi [NTCP2](/docs/specs/ntcp2). NTCP là một transport dựa trên Java NIO được giới thiệu trong I2P phiên bản 0.6.1.22. Java NIO (new I/O) không gặp phải vấn đề 1 thread cho mỗi kết nối như transport TCP cũ. NTCP-over-IPv6 được hỗ trợ từ phiên bản 0.9.8.

Theo mặc định, NTCP sử dụng IP/Port được SSU tự động phát hiện. Khi được bật trên config.jsp, SSU sẽ thông báo/khởi động lại NTCP khi địa chỉ bên ngoài thay đổi hoặc khi trạng thái tường lửa thay đổi. Giờ đây bạn có thể bật TCP đến mà không cần IP tĩnh hoặc dịch vụ dyndns.

Mã NTCP trong I2P tương đối nhẹ (1/4 kích thước của mã SSU) vì nó sử dụng lớp vận chuyển TCP Java cơ bản để truyền tải đáng tin cậy.

## Đặc tả Địa chỉ Router {#ra}

Các thuộc tính sau được lưu trữ trong cơ sở dữ liệu mạng.

- **Tên transport:** NTCP
- **host:** IP (IPv4 hoặc IPv6).
  Địa chỉ IPv6 được rút gọn (với "::") được phép.
  Tên host trước đây được cho phép, nhưng đã không được khuyến khích từ phiên bản 0.9.32. Xem đề xuất 141.
- **port:** 1024 - 65535

## Đặc tả giao thức NTCP

### Định Dạng Thông Điệp Tiêu Chuẩn

Sau khi thiết lập, giao thức truyền tải NTCP gửi các thông điệp I2NP riêng lẻ, với một checksum đơn giản. Thông điệp không mã hóa được mã hóa như sau:

```
+-------+-------+-------+-------+-------+-------+-------+-------+
| sizeof(data)  |                                               |
+-------+-------+                                               +
|                            data                               |
~                                                               ~
|                                                               |
+                                       +-------+-------+-------+
|                                       |        padding
+-------+-------+-------+-------+-------+-------+-------+-------+
                                | Adler checksum of sz+data+pad |
+-------+-------+-------+-------+-------+-------+-------+-------+
```
Dữ liệu sau đó được mã hóa bằng AES/256/CBC. Session key (khóa phiên) để mã hóa được thỏa thuận trong quá trình thiết lập (sử dụng Diffie-Hellman 2048 bit). Việc thiết lập kết nối giữa hai router được triển khai trong lớp EstablishState và được mô tả chi tiết bên dưới. IV cho mã hóa AES/256/CBC là 16 byte cuối của thông điệp được mã hóa trước đó.

Cần 0-15 byte đệm để đưa tổng độ dài thông điệp (bao gồm sáu byte kích thước và checksum) thành bội số của 16. Kích thước thông điệp tối đa hiện tại là 16 KB. Do đó kích thước dữ liệu tối đa hiện tại là 16 KB - 6, hoặc 16378 byte. Kích thước dữ liệu tối thiểu là 1.

### Định dạng Thông điệp Đồng bộ Thời gian

Một trường hợp đặc biệt là thông điệp metadata trong đó sizeof(data) bằng 0. Trong trường hợp đó, thông điệp không được mã hóa được mã hóa như sau:

```
+-------+-------+-------+-------+-------+-------+-------+-------+
|       0       |      timestamp in seconds     | uninterpreted
+-------+-------+-------+-------+-------+-------+-------+-------+
        uninterpreted           | Adler checksum of bytes 0-11  |
+-------+-------+-------+-------+-------+-------+-------+-------+
```
Tổng độ dài: 16 byte. Thông điệp đồng bộ thời gian được gửi với khoảng thời gian xấp xỉ 15 phút. Thông điệp được mã hóa giống như các thông điệp tiêu chuẩn.

### Tổng kiểm tra

Các thông điệp tiêu chuẩn và đồng bộ thời gian sử dụng checksum Adler-32 như được định nghĩa trong [Đặc tả ZLIB](http://tools.ietf.org/html/rfc1950).

### Thời gian chờ không hoạt động

Thời gian chờ nhàn rỗi và việc đóng kết nối tùy thuộc vào quyết định của từng điểm cuối và có thể thay đổi. Triển khai hiện tại sẽ giảm thời gian chờ khi số lượng kết nối tiến gần đến giá trị tối đa đã cấu hình, và tăng thời gian chờ khi số lượng kết nối thấp. Thời gian chờ tối thiểu được khuyến nghị là hai phút trở lên, và thời gian chờ tối đa được khuyến nghị là mười phút trở lên.

### Trao đổi RouterInfo

Sau khi thiết lập, và sau đó mỗi 30-60 phút, hai router nên trao đổi RouterInfo bằng cách sử dụng DatabaseStoreMessage. Tuy nhiên, Alice nên kiểm tra xem thông điệp đầu tiên trong hàng đợi có phải là DatabaseStoreMessage hay không để tránh gửi thông điệp trùng lặp; điều này thường xảy ra khi kết nối tới một floodfill router.

### Trình tự Thiết lập

Trong trạng thái thiết lập, có một chuỗi thông điệp 4 giai đoạn để trao đổi khóa DH và chữ ký. Trong hai thông điệp đầu tiên có một trao đổi Diffie Hellman 2048-bit. Sau đó, các chữ ký của dữ liệu quan trọng được trao đổi để xác nhận kết nối.

```
Alice                   contacts                      Bob
=========================================================
 X+(H(X) xor Bob.identHash)----------------------------->
 <----------------------------------------Y+E(H(X+Y)+tsB+padding, sk, Y[239:255])
 E(sz+Alice.identity+tsA+padding+S(X+Y+Bob.identHash+tsA+tsB), sk, hX_xor_Bob.identHash[16:31])--->
 <----------------------E(S(X+Y+Alice.identHash+tsA+tsB)+padding, sk, prev)
```
```
  Legend:
    X, Y: 256 byte DH public keys
    H(): 32 byte SHA256 Hash
    E(data, session key, IV): AES256 Encrypt
    S(): Signature
    tsA, tsB: timestamps (4 bytes, seconds since epoch)
    sk: 32 byte Session key
    sz: 2 byte size of Alice identity to follow
```
#### DH Key Exchange {#DH}

Việc trao đổi khóa DH 2048-bit ban đầu sử dụng cùng số nguyên tố chung (p) và bộ sinh (g) như được sử dụng cho [mã hóa ElGamal](/docs/specs/cryptography#elgamal) của I2P.

Trao đổi khóa DH bao gồm một số bước, được hiển thị bên dưới. Mối liên hệ giữa các bước này và các thông điệp được gửi giữa các router I2P được đánh dấu bằng chữ đậm.

1. Alice tạo ra một số nguyên bí mật x. Sau đó cô ấy tính toán `X = g^x mod p`.
2. Alice gửi X cho Bob **(Thông điệp 1)**.
3. Bob tạo ra một số nguyên bí mật y. Sau đó anh ấy tính toán `Y = g^y mod p`.
4. Bob gửi Y cho Alice. **(Thông điệp 2)**
5. Alice bây giờ có thể tính `sessionKey = Y^x mod p`.
6. Bob bây giờ có thể tính `sessionKey = X^y mod p`.
7. Cả Alice và Bob bây giờ đều có chung một khóa `sessionKey = g^(x*y) mod p`.

sessionKey sau đó được sử dụng để trao đổi danh tính trong **Message 3** và **Message 4**. Độ dài số mũ (x và y) cho việc trao đổi DH được ghi chép trên [trang mật mã học](/docs/specs/cryptography#exponent).

#### Chi tiết Session Key

Khóa phiên 32-byte được tạo như sau:

1. Lấy khóa DH đã trao đổi, được biểu diễn dưới dạng mảng byte BigInteger có độ dài tối thiểu dương (two's complement big-endian)
2. Nếu bit quan trọng nhất là 1 (tức là array[0] & 0x80 != 0), thêm byte 0x00 vào đầu, như trong biểu diễn BigInteger.toByteArray() của Java
3. Nếu mảng byte đó lớn hơn hoặc bằng 32 byte, sử dụng 32 byte đầu tiên (quan trọng nhất)
4. Nếu mảng byte đó nhỏ hơn 32 byte, thêm các byte 0x00 vào cuối để mở rộng thành 32 byte. *(khả năng xảy ra cực kỳ thấp)*

#### Thông điệp 1 (Yêu cầu Phiên)

Đây là yêu cầu DH. Alice đã có [Router Identity](/docs/specs/common-structures#struct_RouterIdentity), địa chỉ IP và cổng của Bob, như được chứa trong [Router Info](/docs/specs/common-structures#struct_RouterInfo) của anh ta, đã được xuất bản lên [network database](/docs/overview/network-database). Alice gửi cho Bob:

```
 X+(H(X) xor Bob.identHash)----------------------------->

    Size: 288 bytes
```
Mục lục:

```
 +----+----+----+----+----+----+----+----+
 |         X, as calculated from DH      |
 +                                       +
 |                                       |
 ~               .   .   .               ~
 |                                       |
 +----+----+----+----+----+----+----+----+
 |                                       |
 +                                       +
 |              HXxorHI                  |
 +                                       +
 |                                       |
 +                                       +
 |                                       |
 +----+----+----+----+----+----+----+----+

  X :: 256 byte X from Diffie Hellman

  HXxorHI :: SHA256 Hash(X) xored with SHA256 Hash(Bob's RouterIdentity)
             (32 bytes)
```
**Ghi chú:**

- Bob xác minh HXxorHI bằng router hash của chính mình. Nếu không xác minh được, Alice đã liên hệ nhầm router, và Bob sẽ ngắt kết nối.

#### Message 2 (Phiên đã được tạo)

Đây là phản hồi DH. Bob gửi cho Alice:

```
 <----------------------------------------Y+E(H(X+Y)+tsB+padding, sk, Y[239:255])

    Size: 304 bytes
```
Nội dung không mã hóa:

```
 +----+----+----+----+----+----+----+----+
 |         Y as calculated from DH       |
 +                                       +
 |                                       |
 ~               .   .   .               ~
 |                                       |
 +----+----+----+----+----+----+----+----+
 |                                       |
 +                                       +
 |              HXY                      |
 +                                       +
 |                                       |
 +                                       +
 |                                       |
 +----+----+----+----+----+----+----+----+
 |        tsB        |     padding       |
 +----+----+----+----+                   +
 |                                       |
 +----+----+----+----+----+----+----+----+

  Y :: 256 byte Y from Diffie Hellman

  HXY :: SHA256 Hash(X concatenated with Y)
         (32 bytes)

  tsB :: 4 byte timestamp (seconds since the epoch)

  padding :: 12 bytes random data
```
Nội dung được mã hóa:

```
 +----+----+----+----+----+----+----+----+
 |         Y as calculated from DH       |
 +                                       +
 |                                       |
 ~               .   .   .               ~
 |                                       |
 +----+----+----+----+----+----+----+----+
 |                                       |
 +                                       +
 |             encrypted data            |
 +                                       +
 |                                       |
 +                                       +
 |                                       |
 +                                       +
 |                                       |
 +                                       +
 |                                       |
 +----+----+----+----+----+----+----+----+

  Y: 256 byte Y from Diffie Hellman

  encrypted data: 48 bytes AES encrypted using the DH session key and
                  the last 16 bytes of Y as the IV
```
**Ghi chú:**

- Alice có thể ngắt kết nối nếu độ lệch đồng hồ với Bob quá cao như được tính toán bằng tsB.

#### Thông điệp 3 (Xác nhận phiên A)

Điều này chứa danh tính router của Alice và chữ ký của dữ liệu quan trọng. Alice gửi cho Bob:

```
 E(sz+Alice.identity+tsA+padding+S(X+Y+Bob.identHash+tsA+tsB), sk, hX_xor_Bob.identHash[16:31])--->

    Size: 448 bytes (typ. for 387 byte identity and DSA signature), see notes below
```
Nội dung không mã hóa:

```
 +----+----+----+----+----+----+----+----+
 |   sz    | Alice's Router Identity     |
 +----+----+                             +
 |                                       |
 ~               .   .   .               ~
 |                                       |
 +                        +----+----+----+
 |                        |     tsA
 +----+----+----+----+----+----+----+----+
      |             padding              |
 +----+                                  +
 |                                       |
 +----+----+----+----+----+----+----+----+
 |                                       |
 +                                       +
 |              signature                |
 +                                       +
 |                                       |
 +                                       +
 |                                       |
 +                                       +
 |                                       |
 +----+----+----+----+----+----+----+----+

  sz :: 2 byte size of Alice's router identity to follow (387+)

  ident :: Alice's 387+ byte RouterIdentity

  tsA :: 4 byte timestamp (seconds since the epoch)

  padding :: 0-15 bytes random data

  signature :: the Signature of the following concatenated data:
               X, Y, Bob's RouterIdentity, tsA, tsB.
               Alice signs it with the SigningPrivateKey associated with
               the SigningPublicKey in her RouterIdentity
```
Nội dung được mã hóa:

```
 +----+----+----+----+----+----+----+----+
 |                                       |
 +                                       +
 |             encrypted data            |
 ~               .   .   .               ~
 |                                       |
 +----+----+----+----+----+----+----+----+

  encrypted data: 448 bytes AES encrypted using the DH session key and
                  the last 16 bytes of HXxorHI (i.e., the last 16 bytes
                  of message #1) as the IV
                  448 is the typical length, but it could be longer, see below.
```
**Ghi chú:**

- Bob xác minh chữ ký, và nếu thất bại, sẽ ngắt kết nối.
- Bob có thể ngắt kết nối nếu độ lệch đồng hồ với Alice quá cao như được tính toán bằng tsA.
- Alice sẽ sử dụng 16 byte cuối của nội dung đã mã hóa của thông điệp này làm IV cho thông điệp tiếp theo.
- Đến phiên bản 0.9.15, router identity luôn có kích thước 387 byte, chữ ký luôn là chữ ký DSA 40 byte, và padding luôn là 15 byte. Từ phiên bản 0.9.16, router identity có thể dài hơn 387 byte, và loại cũng như độ dài chữ ký được xác định ngầm từ loại [Signing Public Key](/docs/specs/common-structures#type_SigningPublicKey) trong [Router Identity](/docs/specs/common-structures#struct_RouterIdentity) của Alice. Padding được thực hiện khi cần thiết để tổng nội dung chưa mã hóa chia hết cho 16 byte.
- Tổng chiều dài của thông điệp không thể được xác định mà không giải mã một phần để đọc Router Identity. Vì chiều dài tối thiểu của Router Identity là 387 byte, và chiều dài Signature tối thiểu là 40 (cho DSA), kích thước thông điệp tối thiểu là 2 + 387 + 4 + (chiều dài signature) + (padding đến 16 byte), hoặc 2 + 387 + 4 + 40 + 15 = 448 cho DSA. Bên nhận có thể đọc số lượng tối thiểu đó trước khi giải mã để xác định chiều dài Router Identity thực tế. Đối với các Certificate nhỏ trong Router Identity, đó có thể là toàn bộ thông điệp, và sẽ không có thêm byte nào khác trong thông điệp để yêu cầu thao tác giải mã bổ sung.

#### Tin nhắn 4 (Xác nhận Phiên B)

Đây là chữ ký của dữ liệu quan trọng. Bob gửi cho Alice:

```
 <----------------------E(S(X+Y+Alice.identHash+tsA+tsB)+padding, sk, prev)

    Size: 48 bytes (typ. for DSA signature), see notes below
```
Nội dung không được mã hóa:

```
 +----+----+----+----+----+----+----+----+
 |                                       |
 +                                       +
 |              signature                |
 +                                       +
 |                                       |
 +                                       +
 |                                       |
 +                                       +
 |                                       |
 +----+----+----+----+----+----+----+----+
 |               padding                 |
 +----+----+----+----+----+----+----+----+

  signature :: the Signature of the following concatenated data:
               X, Y, Alice's RouterIdentity, tsA, tsB.
               Bob signs it with the SigningPrivateKey associated with
               the SigningPublicKey in his RouterIdentity

  padding :: 0-15 bytes random data
```
Nội dung được Mã hóa:

```
 +----+----+----+----+----+----+----+----+
 |                                       |
 +                                       +
 |             encrypted data            |
 ~               .   .   .               ~
 |                                       |
 +----+----+----+----+----+----+----+----+

  encrypted data: Data AES encrypted using the DH session key and
                  the last 16 bytes of the encrypted contents of message #2 as the IV
                  48 bytes for a DSA signature, may vary for other signature types
```
**Ghi chú:**

- Alice xác minh chữ ký, và nếu thất bại, sẽ ngắt kết nối.
- Bob sẽ sử dụng 16 byte cuối của nội dung đã mã hóa của thông điệp này làm IV cho thông điệp tiếp theo.
- Từ bản phát hành 0.9.15 trở về trước, chữ ký luôn là chữ ký DSA 40 byte và padding luôn là 8 byte. Kể từ bản phát hành 0.9.16, loại chữ ký và độ dài được xác định bởi loại của [Signing Public Key](/docs/specs/common-structures#type_SigningPublicKey) trong [Router Identity](/docs/specs/common-structures#struct_RouterIdentity) của Bob. Padding được thêm khi cần thiết để tổng nội dung chưa mã hóa là bội số của 16 byte.

#### Sau khi thiết lập

Kết nối được thiết lập và các tin nhắn tiêu chuẩn hoặc đồng bộ thời gian có thể được trao đổi. Tất cả các tin nhắn tiếp theo đều được mã hóa AES bằng khóa phiên DH đã thương lượng. Alice sẽ sử dụng 16 byte cuối của nội dung mã hóa của tin nhắn #3 làm IV tiếp theo. Bob sẽ sử dụng 16 byte cuối của nội dung mã hóa của tin nhắn #4 làm IV tiếp theo.

### Thông Báo Kiểm Tra Kết Nối

Ngoài ra, khi Bob nhận được một kết nối, đó có thể là một kết nối kiểm tra (có thể được khởi tạo bởi Bob yêu cầu ai đó xác minh listener của anh ta). Check Connection hiện tại không được sử dụng. Tuy nhiên, để ghi chép, các kết nối kiểm tra được định dạng như sau. Một kết nối thông tin kiểm tra sẽ nhận 256 byte chứa:

- 32 byte dữ liệu không được diễn giải, bị bỏ qua
- 1 byte kích thước
- nhiều byte tạo thành địa chỉ IP của router cục bộ (như được tiếp cận bởi phía từ xa)
- 2 byte số cổng mà router cục bộ được tiếp cận
- 4 byte thời gian mạng i2p như được biết bởi phía từ xa (giây kể từ epoch)
- dữ liệu đệm không được diễn giải, lên đến byte 223
- xor của identity hash của router cục bộ và SHA256 của byte 32 đến byte 223

Tính năng kiểm tra kết nối đã được vô hiệu hóa hoàn toàn kể từ phiên bản 0.9.12.

## Thảo luận

Hiện tại trên [Trang Thảo luận NTCP](/docs/discussions/ntcp).

## Công việc tương lai {#future}

- Kích thước tin nhắn tối đa nên được tăng lên khoảng 32 KB.

- Một tập hợp các kích thước gói cố định có thể phù hợp để ẩn thêm việc phân mảnh dữ liệu khỏi các đối thủ bên ngoài, nhưng việc đệm tunnel, garlic và đầu cuối thường đủ cho hầu hết các nhu cầu cho đến lúc đó.
  Tuy nhiên, hiện tại không có điều khoản nào cho việc đệm vượt quá ranh giới 16-byte tiếp theo,
  để tạo ra một số lượng hạn chế các kích thước thông điệp.

- Việc sử dụng bộ nhớ (bao gồm cả của kernel) cho NTCP nên được so sánh với việc sử dụng cho SSU.

- Liệu các thông điệp thiết lập có thể được đệm ngẫu nhiên bằng cách nào đó, để gây khó khăn cho việc nhận diện lưu lượng I2P dựa trên kích thước gói tin ban đầu không?
