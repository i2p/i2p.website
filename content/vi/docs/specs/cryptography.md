---
title: "Đặc tả Mật mã Cấp thấp"
description: "Chi tiết cấp thấp của các thuật toán mật mã được sử dụng trong I2P"
slug: "cryptography"
aliases:
  - "/vi/how_cryptography"
  - "/vi/how_cryptography/"
category: "Thiết kế"
lastUpdated: "2025-05"
accurateFor: "0.9.66"
---

## Tổng quan

> **Lưu ý:** Tài liệu này hầu như đã lỗi thời. Xem các tài liệu sau để biết thông số kỹ thuật hiện tại: > - [ECIES](/docs/specs/ecies) > - [Encrypted LeaseSet](/docs/specs/encryptedleaseset) > - [NTCP2](/docs/specs/ntcp2) > - [Red25519](/docs/specs/red25519) > - [SSU2](/docs/specs/ssu2) > - [Tunnel Creation (ECIES)](/docs/specs/tunnel-creation-ecies)

Trang này mô tả các chi tiết cấp thấp của mật mã học trong I2P.

Có một số thuật toán mã hóa được sử dụng trong I2P. Trong thiết kế ban đầu của I2P, chỉ có một thuật toán cho mỗi loại - một thuật toán đối xứng, một thuật toán bất đối xứng, một thuật toán ký và một thuật toán băm. Không có điều khoản nào để thêm các thuật toán khác hoặc chuyển đổi sang những thuật toán có tính bảo mật cao hơn.

Trong những năm gần đây, chúng tôi đã thêm một framework để hỗ trợ nhiều primitive và tổ hợp theo cách tương thích ngược. Nhiều thuật toán chữ ký, với độ dài khóa và chữ ký khác nhau, được định nghĩa bằng "signature types". Các lược đồ mã hóa đầu cuối đến đầu cuối, sử dụng kết hợp mã hóa bất đối xứng và đối xứng, với độ dài khóa khác nhau, được định nghĩa bằng "encryption types".

Các giao thức và cấu trúc dữ liệu khác nhau trong I2P bao gồm các trường để chỉ định loại chữ ký và/hoặc loại mã hóa. Những trường này, cùng với các định nghĩa kiểu, xác định độ dài khóa và chữ ký cũng như các nguyên hàm mật mã cần thiết để sử dụng chúng. Các định nghĩa về loại chữ ký và mã hóa được quy định trong [đặc tả Common Structures](/docs/specs/common-structures).

Các giao thức I2P gốc NTCP, SSU, và ElGamal/AES+SessionTags sử dụng sự kết hợp của mã hóa bất đối xứng ElGamal và mã hóa đối xứng AES. Các giao thức mới hơn NTCP2 và ECIES-X25519-AEAD-Ratchet sử dụng sự kết hợp của trao đổi khóa X25519 và mã hóa đối xứng ChaCha20/Poly1305.

- ECIES-X25519-AEAD-Ratchet đã thay thế ElGamal/AES+SessionTags.
- NTCP2 đã thay thế NTCP.
- SSU2 đã thay thế SSU.
- Tạo tunnel X25519 đã thay thế tạo tunnel ElGamal.

## Mã hóa bất đối xứng

Thuật toán mã hóa bất đối xứng ban đầu trong I2P là ElGamal. Thuật toán mới hơn, được sử dụng ở nhiều nơi, là trao đổi khóa ECIES X25519 DH.

Chúng tôi đang trong quá trình chuyển đổi tất cả việc sử dụng ElGamal sang X25519.

NTCP (với ElGamal) đã được chuyển đổi sang NTCP2 (với X25519). ElGamal/AES+SessionTag đang được chuyển đổi sang ECIES-X25519-AEAD-Ratchet.

### X25519

Để biết chi tiết về việc sử dụng X25519, xem [NTCP2](/docs/specs/ntcp2) và [ECIES](/docs/specs/ecies).

### ElGamal

ElGamal được sử dụng ở nhiều nơi trong I2P:

- Để mã hóa các thông điệp TunnelBuild từ router đến router
- Để mã hóa đầu cuối đến đầu cuối (từ destination đến destination) như một phần của ElGamal/AES+SessionTag sử dụng khóa mã hóa trong LeaseSet
- Để mã hóa một số netDb stores và queries được gửi đến floodfill routers như một phần của ElGamal/AES+SessionTag (từ destination đến router hoặc từ router đến router).

Chúng tôi sử dụng các số nguyên tố chung cho việc mã hóa và giải mã ElGamal 2048, như được quy định bởi IETF [RFC-3526](http://tools.ietf.org/html/rfc3526). Hiện tại chúng tôi chỉ sử dụng ElGamal để mã hóa IV và session key trong một khối duy nhất, tiếp theo là payload được mã hóa AES sử dụng key và IV đó.

ElGamal không mã hóa chứa:

```
+----+----+----+----+----+----+----+----+
|nonz|           H(data)                |
+----+                                  +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+    +----+----+----+----+----+----+----+
|    |  data...
+----+----+----+-//
```
H(data) là SHA256 của dữ liệu được mã hóa trong khối ElGamal, và được đặt trước bởi một byte ngẫu nhiên khác không. Byte này thực sự là ngẫu nhiên kể từ phiên bản 0.9.28; trước đó nó luôn là 0xFF. Có thể nó sẽ được sử dụng cho các cờ hiệu trong tương lai. Dữ liệu được mã hóa trong khối có thể dài tới 222 bytes. Vì dữ liệu được mã hóa có thể chứa một số lượng đáng kể các số không nếu văn bản rõ nhỏ hơn 222 bytes, nên khuyến nghị các lớp cao hơn nên đệm văn bản rõ lên 222 bytes bằng dữ liệu ngẫu nhiên. Tổng độ dài: thường là 255 bytes.

Mã hóa ElGamal chứa:

```
+----+----+----+----+----+----+----+----+
|  zero padding...       |              |
+----+----+----+-//-+----+              +
|                                       |
+                                       +
|       ElG encrypted part 1            |
~                                       ~
|                                       |
+    +----+----+----+----+----+----+----+
|    |   zero padding...      |         |
+----+----+----+----+-//-+----+         +
|                                       |
+                                       +
|       ElG encrypted part 2            |
~                                       ~
|                                       |
+         +----+----+----+----+----+----+
|         +
+----+----+
```
Mỗi phần được mã hóa sẽ được thêm các số không vào đầu để có kích thước chính xác là 257 bytes. Tổng chiều dài: 514 bytes. Trong cách sử dụng điển hình, các lớp cao hơn sẽ đệm dữ liệu cleartext đến 222 bytes, tạo ra một khối chưa mã hóa có kích thước 255 bytes. Khối này được mã hóa thành hai phần mã hóa 256-byte, và có một byte đệm số không trước mỗi phần ở lớp này.

Xem mã ElGamal [ElGamalEngine](https://github.com/i2p/i2p.i2p/tree/master/core/java/src/net/i2p/crypto/ElGamalEngine.java).

Số nguyên tố chia sẻ là số nguyên tố Oakley cho khóa 2048 bit [RFC-3526-S3](http://tools.ietf.org/html/rfc3526#section-3):

```
2^2048 - 2^1984 - 1 + 2^64 * { [2^1918 pi] + 124476 }
```
hoặc dưới dạng giá trị thập lục phân:

```
FFFFFFFF FFFFFFFF C90FDAA2 2168C234 C4C6628B 80DC1CD1
29024E08 8A67CC74 020BBEA6 3B139B22 514A0879 8E3404DD
EF9519B3 CD3A431B 302B0A6D F25F1437 4FE1356D 6D51C245
E485B576 625E7EC6 F44C42E9 A637ED6B 0BFF5CB6 F406B7ED
EE386BFB 5A899FA5 AE9F2411 7C4B1FE6 49286651 ECE45B3D
C2007CB8 A163BF05 98DA4836 1C55D39A 69163FA8 FD24CF5F
83655D23 DCA3AD96 1C62F356 208552BB 9ED52907 7096966D
670C354E 4ABC9804 F1746C08 CA18217C 32905E46 2E36CE3B
E39E772C 180E8603 9B2783A2 EC07A28F B5C55DF0 6F4C52C9
DE2BCBF6 95581718 3995497C EA956AE5 15D22618 98FA0510
15728E5A 8AACAA68 FFFFFFFF FFFFFFFF
```
Sử dụng 2 làm số sinh.

#### Số Mũ Ngắn {#exponent}

Trong khi kích thước số mũ tiêu chuẩn là 2048 bit (256 byte) và I2P PrivateKey có độ dài đầy đủ 256 byte, trong một số trường hợp chúng tôi sử dụng kích thước số mũ ngắn là 226 bit (28,25 byte). Điều này nên an toàn để sử dụng với các số nguyên tố Oakley [vanOorschot1996] [BENCHMARKS].

Ngoài ra, [Koshiba2004] dường như hỗ trợ điều này, theo thread sci.crypt này [SCI.CRYPT]. Phần còn lại của PrivateKey được đệm bằng các số không.

Trước phiên bản 0.9.8, tất cả các router đều sử dụng số mũ ngắn. Từ phiên bản 0.9.8, các router x86 64-bit sử dụng số mũ đầy đủ 2048-bit. Hiện tại tất cả các router đều sử dụng số mũ đầy đủ trừ một số lượng nhỏ router chạy trên phần cứng rất chậm, vẫn tiếp tục sử dụng số mũ ngắn do lo ngại về tải xử lý. Việc chuyển đổi sang số mũ dài hơn cho các nền tảng này là chủ đề cần nghiên cứu thêm.

#### Lỗi thời

Tính dễ bị tổn thương của mạng trước cuộc tấn công ElGamal và tác động của việc chuyển đổi sang độ dài bit dài hơn cần được nghiên cứu. Có thể khá khó khăn để thực hiện bất kỳ thay đổi nào mà vẫn tương thích ngược.

## Mã hóa đối xứng

Thuật toán mã hóa đối xứng gốc trong I2P là AES. Thuật toán mới hơn, được sử dụng ở nhiều nơi, là Authenticated Encryption with Associated Data (AEAD) ChaCha20/Poly1305.

Chúng tôi đang trong quá trình di chuyển tất cả việc sử dụng AES sang ChaCha20/Poly1305.

NTCP (với AES) đã được chuyển đổi sang NTCP2 (với ChaCha20/Poly1305). ElGamal/AES+SessionTag đang được chuyển đổi sang ECIES-X25519-AEAD-Ratchet.

### ChaCha20/Poly1305

Để biết chi tiết về việc sử dụng ChaCha20/Poly1305, xem [NTCP2](/docs/specs/ntcp2) và [ECIES](/docs/specs/ecies).

### AES

AES được sử dụng cho mã hóa đối xứng, trong một số trường hợp:

- Cho mã hóa truyền tải SSU (xem phần "Transports") sau khi trao đổi khóa DH
- Cho mã hóa đầu cuối đến đầu cuối (destination-to-destination) như một phần của ElGamal/AES+SessionTag
- Cho mã hóa một số lưu trữ và truy vấn netDb được gửi đến các floodfill router như một phần của ElGamal/AES+SessionTag (destination-to-router hoặc router-to-router).
- Cho mã hóa các thông điệp kiểm tra tunnel định kỳ được gửi từ router đến chính nó, thông qua các tunnel của nó.

Chúng tôi sử dụng AES với khóa 256 bit và khối 128 bit ở chế độ CBC. Phần đệm được sử dụng được chỉ định trong IETF [RFC-2313](http://tools.ietf.org/html/rfc2313) (PKCS#5 1.5, mục 8.1 (cho loại khối 02)). Trong trường hợp này, phần đệm bao gồm các octet được tạo ngẫu nhiên giả để khớp với các khối 16 byte. Cụ thể, xem mã CBC [CryptixAESEngine](https://github.com/i2p/i2p.i2p/tree/master/core/java/src/net/i2p/crypto/CryptixAESEngine.java) và triển khai Cryptix AES [CryptixRijndael_Algorithm](https://github.com/i2p/i2p.i2p/tree/master/core/java/src/net/i2p/crypto/CryptixRijndael_Algorithm.java), cũng như phần đệm, được tìm thấy trong hàm ElGamalAESEngine.getPadding [ElGamalAESEngine](https://github.com/i2p/i2p.i2p/tree/master/core/java/src/net/i2p/crypto/ElGamalAESEngine.java).

#### Lỗi thời

Tính dễ bị tổn thương của mạng trước cuộc tấn công AES và tác động của việc chuyển đổi sang độ dài bit lớn hơn cần được nghiên cứu. Có thể khá khó khăn để thực hiện bất kỳ thay đổi nào mà vẫn tương thích ngược.

## Chữ ký {#sig}

Nhiều thuật toán chữ ký, với các độ dài khóa và chữ ký khác nhau, được định nghĩa bởi các loại chữ ký. Việc thêm các loại chữ ký mới tương đối dễ dàng.

EdDSA-SHA512-Ed25519 là thuật toán chữ ký mặc định hiện tại. DSA, thuật toán gốc trước khi chúng tôi thêm hỗ trợ các loại chữ ký, vẫn đang được sử dụng trong mạng.

### DSA

Chữ ký được tạo và xác minh bằng [DSA](http://en.wikipedia.org/wiki/Digital_Signature_Algorithm) 1024 bit (L=1024, N=160), như được triển khai trong [DSAEngine](https://github.com/i2p/i2p.i2p/tree/master/core/java/src/net/i2p/crypto/DSAEngine.java). DSA được chọn vì nó nhanh hơn nhiều so với ElGamal khi tạo chữ ký.

#### SEED

160 bit:

```
86108236b8526e296e923a4015b4282845b572cc
```
#### Bộ đếm

```
33
```
#### Số nguyên tố DSA (p)

1024 bit:

```
9C05B2AA 960D9B97 B8931963 C9CC9E8C 3026E9B8 ED92FAD0
A69CC886 D5BF8015 FCADAE31 A0AD18FA B3F01B00 A358DE23
7655C496 4AFAA2B3 37E96AD3 16B9FB1C C564B5AE C5B69A9F
F6C3E454 8707FEF8 503D91DD 8602E867 E6D35D22 35C1869C
E2479C3B 9D5401DE 04E0727F B33D6511 285D4CF2 9538D9E3
B6051F5B 22CC1C93
```
#### Thương số DSA (q)

```
A5DFC28F EF4CA1E2 86744CD8 EED9D29D 684046B7
```
#### Bộ sinh DSA (g)

1024 bit:

```
0C1F4D27 D40093B4 29E962D7 223824E0 BBC47E7C 832A3923
6FC683AF 84889581 075FF908 2ED32353 D4374D73 01CDA1D2
3C431F46 98599DDA 02451824 FF369752 593647CC 3DDC197D
E985E43D 136CDCFC 6BD5409C D2F45082 1142A5E6 F8EB1C3A
B5D0484B 8129FCF1 7BCE4F7F 33321C3C B3DBB14A 905E7B2B
3E93BE47 08CBCC82
```
SigningPublicKey có độ dài 1024 bit. SigningPrivateKey có độ dài 160 bit.

#### Lỗi thời

[NIST-800-57](http://csrc.nist.gov/publications/nistpubs/800-57/sp800-57-Part1-revised2_Mar08-2007.pdf) khuyến nghị tối thiểu (L=2048, N=224) để sử dụng sau năm 2010. Điều này có thể được giảm thiểu phần nào bởi "cryptoperiod", hay vòng đời của một khóa nhất định.

Số nguyên tố này được chọn vào năm 2003, và người đã chọn số đó (TheCrypto) hiện không còn là nhà phát triển I2P nữa. Do đó, chúng tôi không biết liệu số nguyên tố được chọn có phải là 'số nguyên tố mạnh' hay không. Nếu một số nguyên tố lớn hơn được chọn cho các mục đích tương lai, đây nên là một số nguyên tố mạnh, và chúng tôi sẽ ghi lại quá trình xây dựng.

## Thuật toán Chữ ký Mới

Kể từ phiên bản phát hành 0.9.12, router hỗ trợ các thuật toán chữ ký bổ sung an toàn hơn so với DSA 1024-bit. Việc sử dụng đầu tiên là cho Destinations; hỗ trợ cho Router Identities đã được thêm vào trong phiên bản phát hành 0.9.16. Các Destinations hiện có không thể được di chuyển từ chữ ký cũ sang chữ ký mới; tuy nhiên, có hỗ trợ cho một tunnel đơn với nhiều Destinations, và điều này cung cấp cách để chuyển sang các loại chữ ký mới hơn. Loại chữ ký được mã hóa trong Destination và Router Identity, do đó các thuật toán chữ ký hoặc đường cong mới có thể được thêm vào bất cứ lúc nào.

Các loại chữ ký hiện được hỗ trợ như sau:

- DSA-SHA1
- ECDSA-SHA256-P256
- ECDSA-SHA384-P384 (không được sử dụng rộng rãi)
- ECDSA-SHA512-P521 (không được sử dụng rộng rãi)
- EdDSA-SHA512-Ed25519 (mặc định kể từ phiên bản 0.9.15)
- RedDSA-SHA512-Ed25519 (kể từ phiên bản 0.9.39)

Các kiểu chữ ký bổ sung chỉ được sử dụng ở tầng ứng dụng, chủ yếu để ký và xác minh các tập tin su3. Các kiểu chữ ký này như sau:

- RSA-SHA256-2048 (không được sử dụng rộng rãi)
- RSA-SHA384-3072 (không được sử dụng rộng rãi)
- RSA-SHA512-4096
- EdDSA-SHA512-Ed25519ph (từ bản phát hành 0.9.25; không được sử dụng rộng rãi)

### ECDSA

ECDSA sử dụng các đường cong NIST tiêu chuẩn và các hàm băm SHA-2 tiêu chuẩn.

Chúng tôi đã chuyển đổi các destination mới sang ECDSA-SHA256-P256 trong khoảng thời gian phát hành 0.9.16 - 0.9.19. Việc sử dụng cho Router Identities được hỗ trợ từ bản phát hành 0.9.16 và việc chuyển đổi các router hiện có đã diễn ra vào năm 2015.

### RSA

RSA PKCS#1 v1.5 tiêu chuẩn (RFC 2313) với số mũ công khai F4 = 65537.

RSA hiện được sử dụng để ký tất cả nội dung đáng tin cậy ngoài băng tần, bao gồm cập nhật router, reseeding, plugin và tin tức. Các chữ ký được nhúng trong định dạng "su3" [UPDATES]. Khóa 4096-bit được khuyến nghị và sử dụng bởi tất cả các bên ký đã biết. RSA không được sử dụng, hoặc không có kế hoạch sử dụng, trong bất kỳ Destinations hoặc Router Identities nào trong mạng.

### EdDSA 25519

EdDSA chuẩn sử dụng đường cong 25519 và hash SHA-2 512-bit chuẩn.

Được hỗ trợ kể từ phiên bản 0.9.15.

Destinations và Router Identities đã được di chuyển vào cuối năm 2015.

### RedDSA 25519

EdDSA tiêu chuẩn sử dụng curve 25519 và hash SHA-2 512-bit tiêu chuẩn, nhưng với các private key khác nhau và những sửa đổi nhỏ trong quá trình ký. Dành cho encrypted leaseSet. Xem [EncryptedLeaseSet](/docs/specs/encryptedleaseset) và [Red25519](/docs/specs/red25519) để biết chi tiết.

Được hỗ trợ từ phiên bản 0.9.39.

## Hash

Hash được sử dụng trong các thuật toán chữ ký và làm khóa trong DHT của mạng.

Các thuật toán chữ ký cũ sử dụng SHA1 và SHA256. Các thuật toán chữ ký mới hơn sử dụng SHA512. DHT sử dụng SHA256.

### SHA256

Các hash DHT trong I2P là SHA256 chuẩn.

#### Lỗi thời

Lỗ hổng của mạng trước cuộc tấn công SHA-256 và tác động của việc chuyển đổi sang hash dài hơn cần được nghiên cứu. Có thể sẽ khá khó khăn để thực hiện bất kỳ thay đổi nào có tính tương thích ngược.

## Giao thức vận chuyển

Ở lớp giao thức thấp nhất, giao tiếp điểm-tới-điểm giữa các router được bảo vệ bởi bảo mật tầng vận chuyển.

Các kết nối NTCP2 sử dụng X25519 Diffie-Hellman và mã hóa có xác thực ChaCha20/Poly1305.

SSU và NTCP transport đã lỗi thời sử dụng trao đổi khóa Diffie-Hellman 256 byte (2048 bit) với cùng số nguyên tố chia sẻ và số sinh như đã chỉ định ở trên cho ElGamal, theo sau bởi mã hóa AES đối xứng như đã mô tả ở trên.

SSU được lên kế hoạch di chuyển sang SSU2 (với X25519 và ChaCha20/Poly1305).

Tất cả các phương thức truyền tải đều cung cấp tính bảo mật hoàn hảo [PFS](http://en.wikipedia.org/wiki/Perfect_forward_secrecy) trên các liên kết truyền tải.

### Kết nối NTCP2 {#tcp}

Các kết nối NTCP2 sử dụng X25519 Diffie-Hellman và mã hóa xác thực ChaCha20/Poly1305, cùng với khung giao thức Noise [Noise](https://noiseprotocol.org/noise.html).

Xem đặc tả kỹ thuật NTCP2 [NTCP2](/docs/specs/ntcp2) để biết chi tiết và tham khảo.

### Kết nối UDP {#udp}

SSU (giao thức truyền tải UDP) mã hóa từng gói tin bằng AES256/CBC với cả IV rõ ràng và MAC (HMAC-MD5-128) sau khi thỏa thuận khóa phiên tạm thời thông qua trao đổi Diffie-Hellman 2048 bit, xác thực station-to-station với khóa DSA của router khác, cộng với mỗi thông điệp mạng có hash riêng để kiểm tra tính toàn vẹn cục bộ.

Xem đặc tả SSU để biết chi tiết.

CẢNH BÁO - HMAC-MD5-128 của I2P được sử dụng trong SSU có vẻ không tuân theo tiêu chuẩn. Có vẻ như phiên bản đầu của SSU đã sử dụng HMAC-SHA256, sau đó đã chuyển sang MD5-128 vì lý do hiệu suất, nhưng vẫn giữ nguyên kích thước buffer 32-byte. Xem HMACGenerator.java và ghi chú trạng thái ngày 2005-07-05 để biết chi tiết.

### Kết nối NTCP

NTCP không còn được sử dụng nữa, nó đã được thay thế bởi NTCP2.

Các kết nối NTCP được thương lượng với một triển khai Diffie-Hellman 2048, sử dụng danh tính của router để tiến hành thỏa thuận trạm đến trạm, theo sau bởi một số trường mã hóa cụ thể của giao thức, với tất cả dữ liệu tiếp theo được mã hóa bằng AES (như trên). Lý do chính để thực hiện thương lượng DH thay vì sử dụng ElGamalAES+SessionTag là nó cung cấp 'tính bí mật chuyển tiếp (hoàn hảo)' [PFS](http://en.wikipedia.org/wiki/Perfect_forward_secrecy), trong khi ElGamalAES+SessionTag thì không.

## Tài liệu tham khảo

- [BENCHMARKS](https://web.archive.org/web/20080423000000*/http://www.eskimo.com/~weidai/benchmarks.html) - Benchmark Crypto++, ban đầu tại http://www.eskimo.com/~weidai/benchmarks.html (hiện đã chết), được cứu từ http://www.archive.org/, có ngày 23 tháng 4 năm 2008.
- [Common](/docs/specs/common-structures) - Đặc tả Cấu trúc Chung
- [CryptixAESEngine](https://github.com/i2p/i2p.i2p/tree/master/core/java/src/net/i2p/crypto/CryptixAESEngine.java)
- [CryptixRijndael_Algorithm](https://github.com/i2p/i2p.i2p/tree/master/core/java/src/net/i2p/crypto/CryptixRijndael_Algorithm.java)
- [DSA](http://en.wikipedia.org/wiki/Digital_Signature_Algorithm)
- [DSAEngine](https://github.com/i2p/i2p.i2p/tree/master/core/java/src/net/i2p/crypto/DSAEngine.java)
- [ECIES](/docs/specs/ecies)
- [ElGamalAESEngine](https://github.com/i2p/i2p.i2p/tree/master/core/java/src/net/i2p/crypto/ElGamalAESEngine.java)
- [ElGamalEngine](https://github.com/i2p/i2p.i2p/tree/master/core/java/src/net/i2p/crypto/ElGamalEngine.java)
- [EncryptedLeaseSet](/docs/specs/encryptedleaseset)
- [Koshiba2004](http://www.springerlink.com/content/2jry7cftp5bpdghm/) - Koshiba & Kurosawa. Short Exponent Diffie-Hellman Problems. PKC 2004, LNCS 2947, trang 173-186
- [NIST-800-57](http://csrc.nist.gov/publications/nistpubs/800-57/sp800-57-Part1-revised2_Mar08-2007.pdf)
- [Noise](https://noiseprotocol.org/noise.html)
- [NTCP2](/docs/specs/ntcp2)
- [PFS](http://en.wikipedia.org/wiki/Perfect_forward_secrecy)
- [Red25519](/docs/specs/red25519)
- [RFC-2313](http://tools.ietf.org/html/rfc2313)
- [RFC-3526](http://tools.ietf.org/html/rfc3526)
- [RFC-3526-S3](http://tools.ietf.org/html/rfc3526#section-3)
- [SCI.CRYPT](https://groups.google.com/forum/#!topic/sci.crypt/GFWl76dBZnc)
- [SHA-2](https://en.wikipedia.org/wiki/SHA-2)
- [SSU2](/docs/specs/ssu2)
- [UPDATES](/docs/specs/updates)
- [vanOorschot1996](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.14.5952&rep=rep1&type=pdf) - van Oorschot, Weiner. On Diffie-Hellman Key Agreement with Short Exponents. EuroCrypt '96
