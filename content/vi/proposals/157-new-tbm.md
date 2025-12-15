---
title: "Thông điệp Xây Dựng Đường Hầm Nhỏ Hơn"
number: "157"
author: "zzz, ban đầu"
created: "2020-10-09"
lastupdated: "2021-07-31"
status: "Đã Đóng"
thread: "http://zzz.i2p/topics/2957"
target: "0.9.51"
toc: true
---

## Ghi Chú
Đã triển khai kể từ phiên bản API 0.9.51.
Triển khai và thử nghiệm mạng đang tiến hành.
Có thể sẽ có sửa đổi nhỏ.
Xem [I2NP](/en/docs/spec/i2np/) và [Tunnel-Creation-ECIES](/en/docs/spec/tunnel-creation-ecies/) để biết đặc tả cuối cùng.



## Tổng quan


### Tóm tắt

Kích thước hiện tại của các bản ghi Yêu cầu Xây Dựng và Trả Lời đường hầm mã hóa là 528.
Đối với các thông điệp Xây Dựng Đường Hầm Biến và Xây Dựng Đường Hầm Trả Lời Biến thông thường,
kích thước tổng cộng là 2113 byte. Thông điệp này bị phân mảnh thành ba thông điệp đường hầm 1KB cho đường ngược.

Các thay đổi đối với định dạng bản ghi 528 byte cho các bộ định tuyến ECIES-X25519 được chỉ định trong [Prop152](/en/proposals/152-ecies-tunnels/) và [Tunnel-Creation-ECIES](/en/docs/spec/tunnel-creation-ecies/).
Đối với sự kết hợp giữa các bộ định tuyến ElGamal và ECIES-X25519 trong một đường hầm, kích thước bản ghi phải duy trì
528 byte. Tuy nhiên, nếu tất cả các bộ định tuyến trong một đường hầm là ECIES-X25519, một bản ghi xây dựng mới, nhỏ hơn
có thể, vì mã hóa ECIES-X25519 có độ trễ ít hơn nhiều so với ElGamal.

Thông điệp nhỏ hơn sẽ tiết kiệm băng thông. Ngoài ra, nếu các thông điệp có thể phù hợp trong một
thông điệp đường hầm duy nhất, đường ngược sẽ hiệu quả gấp ba lần.

Đề xuất này định nghĩa các bản ghi yêu cầu và trả lời mới và các thông điệp Yêu Cầu Xây Dựng và Trả Lời Xây Dựng mới.

Người tạo đường hầm và tất cả các bước trong đường hầm được tạo phải là ECIES-X25519 và ít nhất là phiên bản 0.9.51.
Đề xuất này sẽ không có ích cho đến khi phần lớn các bộ định tuyến trong mạng là ECIES-X25519.
Dự kiến sẽ diễn ra vào cuối năm 2021.


### Mục Tiêu

Xem [Prop152](/en/proposals/152-ecies-tunnels/) và [Prop156](/en/proposals/156-ecies-routers/) để biết thêm các mục tiêu.

- Các bản ghi và thông điệp nhỏ hơn
- Duy trì đủ không gian cho các tùy chọn trong tương lai, như trong [Prop152](/en/proposals/152-ecies-tunnels/) và [Tunnel-Creation-ECIES](/en/docs/spec/tunnel-creation-ecies/)
- Phù hợp trong một thông điệp đường hầm cho đường ngược
- Chỉ hỗ trợ các bước ECIES
- Duy trì các cải tiến được triển khai trong [Prop152](/en/proposals/152-ecies-tunnels/) và [Tunnel-Creation-ECIES](/en/docs/spec/tunnel-creation-ecies/)
- Tối đa hóa khả năng tương thích với mạng hiện tại
- Ẩn các thông điệp xây dựng tuyến vào từ OBEP
- Ẩn các thông điệp trả lời xây dựng tuyến ra từ IBGW
- Không yêu cầu nâng cấp "ngày gắn cờ" cho toàn bộ mạng lưới
- Triển khai từ từ để giảm thiểu rủi ro
- Tái sử dụng các nguyên tố mã hóa hiện có


### Không Mục Tiêu

Xem [Prop156](/en/proposals/156-ecies-routers/) để biết thêm các không mục tiêu.

- Không yêu cầu cho các đường hầm ElGamal/ECIES pha trộn
- Thay đổi mã hóa tầng, cho điều đó xem [Prop153](/en/proposals/153-chacha20-layer-encryption/)
- Không tăng tốc các hoạt động mã hóa. Giả định rằng ChaCha20 và AES tương tự nhau,
  ngay cả với AESNI, ít nhất đối với các kích thước dữ liệu nhỏ cần xét.


## Thiết Kế


### Bản Ghi

Xem phụ lục để biết các tính toán.

Các bản ghi yêu cầu và trả lời mã hóa sẽ là 218 byte, so với 528 byte hiện nay.

Các bản ghi yêu cầu dạng văn bản sẽ là 154 byte,
so với 222 byte cho các bản ghi ElGamal,
và 464 byte cho các bản ghi ECIES như được định nghĩa trong [Prop152](/en/proposals/152-ecies-tunnels/) và [Tunnel-Creation-ECIES](/en/docs/spec/tunnel-creation-ecies/).

Các bản ghi phản hồi dạng văn bản sẽ là 202 byte,
so với 496 byte cho các bản ghi ElGamal,
và 512 byte cho các bản ghi ECIES như được định nghĩa trong [Prop152](/en/proposals/152-ecies-tunnels/) và [Tunnel-Creation-ECIES](/en/docs/spec/tunnel-creation-ecies/).

Mã hóa trả lời sẽ là ChaCha20 (KHÔNG Phải ChaCha20/Poly1305),
vì vậy các bản ghi văn bản không cần phải là bội số của 16 byte.

Các bản ghi yêu cầu sẽ được làm nhỏ hơn bằng cách sử dụng HKDF để tạo
các khóa tầng và trả lời, vì vậy chúng không cần phải được đưa rõ ràng trong yêu cầu.


### Thông Điệp Xây Dựng Đường Hầm

Cả hai sẽ là "biến" với một trường số lượng bản ghi một byte,
như với các thông điệp Biến hiện có.

#### ShortTunnelBuild: Loại 25

Độ dài điển hình (với 4 bản ghi): 873 byte

Khi được sử dụng cho các xây dựng đường hầm vào,
nên (nhưng không bắt buộc) rằng thông điệp này được mã hóa garlic bởi nguồn,
nhắm mục tiêu vào cổng vào (hướng dẫn giao hàng ROUTER),
để ẩn các thông điệp xây dựng vào khỏi OBEP.
IBGW giải mã thông điệp,
đưa phản hồi vào vị trí đúng,
và gửi ShortTunnelBuildMessage đến bước tiếp theo.

Kích thước bản ghi được chọn sao cho một STBM được mã hóa garlic sẽ vừa
với một thông điệp đường hầm duy nhất. Xem phụ lục dưới đây.



#### OutboundTunnelBuildReply: Loại 26

Chúng tôi định nghĩa một thông điệp OutboundTunnelBuildReply mới.
Điều này được sử dụng cho các xây dựng đường hầm ra duy nhất.
Mục đích là để ẩn các thông điệp trả lời xây dựng tuyến ra khỏi IBGW.
Nó phải được mã hóa garlic bởi OBEP, nhắm mục tiêu vào nguồn
(hướng dẫn giao hàng TUNNEL).
OBEP giải mã thông điệp xây dựng tuyến,
tạo một thông điệp OutboundTunnelBuildReply,
và đặt phản hồi vào trường dạng văn bản.
Các bản ghi khác đặt vào các khe khác.
Sau đó, mã hóa garlic thông điệp đến nguồn với các khóa đối xứng được phát sinh.


#### Ghi chú

Bằng cách mã hóa garlic OTBRM và STBM, chúng tôi cũng tránh các
vấn đề có thể xảy ra với sự tương thích tại IBGW và OBEP của các đường hầm đôi.




### Luồng Thông Điệp


```
STBM: Thông điệp xây dựng đường hầm ngắn (loại 25)
  OTBRM: Thông điệp phản hồi xây dựng đường hầm ra ngoài (loại 26)

  Xây dựng tuyến ra A-B-C
  Phản hồi qua tuyến vào D-E-F hiện có


                  Đường Hầm Mới
           STBM      STBM      STBM
  Người Tạo ------> A ------> B ------> C ---\
                                     OBEP   \
                                            | Mã hóa garlic
                                            | OTBRM
                                            | (giao hàng TUNNEL)
                                            | từ OBEP đến người tạo
                Đường Hầm Hiện Có             /
  Người Tạo <-------F---------E-------- D <--/
                                     IBGW



  Xây dựng tuyến vào D-E-F
  Gửi qua tuyến ra hiện có A-B-C


                Đường Hầm Hiện Có
  Người Tạo ------> A ------> B ------> C ---\
                                    OBEP    \
                                            | Mã hóa garlic (tùy chọn)
                                            | STBM
                                            | (giao hàng ROUTER)
                                            | từ người tạo
                  Đường Hầm Mới                | đến IBGW
            STBM      STBM      STBM        /
  Người Tạo <------ F <------ E <------ D <--/
                                     IBGW



```



### Mã Hóa Bản Ghi

Mã hóa bản ghi yêu cầu và trả lời: như đã định nghĩa trong [Prop152](/en/proposals/152-ecies-tunnels/) và [Tunnel-Creation-ECIES](/en/docs/spec/tunnel-creation-ecies/).

Mã hóa bản ghi trả lời cho các khe khác: ChaCha20.


### Mã Hóa Tầng

Hiện tại không có kế hoạch thay đổi mã hóa tầng cho các đường hầm được xây dựng với
đặc tả này; nó sẽ vẫn là AES, như hiện đang được sử dụng cho tất cả các đường hầm.

Thay đổi mã hóa tầng thành ChaCha20 là chủ đề cần nghiên cứu thêm.



### Thông Điệp Dữ Liệu Đường Hầm Mới

Hiện tại không có kế hoạch thay đổi Thông Điệp Dữ Liệu Đường Hầm 1KB được sử dụng cho các đường hầm được xây dựng với
đặc tả này.

Nó có thể có ích để giới thiệu một thông điệp I2NP mới mà lớn hơn hoặc có kích thước biến, đồng thời với đề xuất này,
để sử dụng trên các đường hầm này.
Điều này sẽ giảm bớt độ trễ cho các thông điệp lớn.
Đây là một chủ đề cần nghiên cứu thêm.




## Một Số Quy Định


### Bản Ghi Yêu Cầu Ngắn



#### Bản Ghi Yêu Cầu Ngắn Không Mã Hóa

Đây là đặc tả đề xuất cho bản ghi Xây Dựng Yêu Cầu Đường Hầm cho các bộ định tuyến ECIES-X25519.
Tóm tắt các thay đổi từ [Tunnel-Creation-ECIES](/en/docs/spec/tunnel-creation-ecies/):

- Thay đổi độ dài không mã hóa từ 464 thành 154 byte
- Thay đổi độ dài mã hóa từ 528 thành 218 byte
- Loại bỏ các khóa và IVs tầng và trả lời, chúng sẽ được phát sinh từ split() và một KDF


Bản ghi yêu cầu không chứa bất kỳ khóa ChaCha trả lời nào.
Các khóa đó được phát sinh từ một KDF. Xem bên dưới.

Tất cả các trường đều theo thứ tự big-endian.

Kích thước không mã hóa: 154 byte.


```
bytes     0-3: ID đường hầm để nhận thông điệp, khác không
  bytes     4-7: ID đường hầm tiếp theo, khác không
  bytes    8-39: hash định danh Router tiếp theo
  byte       40: cờ
  bytes   41-42: thêm cờ, không sử dụng, đặt thành 0 để tương thích
  byte       43: loại mã hóa tầng
  bytes   44-47: thời gian yêu cầu (tính bằng phút kể từ kỷ nguyên, làm tròn xuống)
  bytes   48-51: thời gian hết hạn yêu cầu (tính bằng giây kể từ khi tạo)
  bytes   52-55: ID tin nhắn tiếp theo
  bytes    56-x: tùy chọn xây dựng đường hầm (Mapping)
  bytes     x-x: dữ liệu khác như được ám bởi cờ hoặc tùy chọn
  bytes   x-153: dồn ngẫu nhiên (xem bên dưới)

```


Trường cờ giữ nguyên như được định nghĩa trong [Tunnel-Creation](/en/docs/spec/tunnel-creation/) và chứa các giá trị sau::

 Thứ tự bit: 76543210 (bit 7 là MSB)
 bit 7: nếu đặt, cho phép gửi thông điệp từ bất kỳ ai
 bit 6: nếu đặt, cho phép gửi thông điệp đến bất kỳ ai, và gửi phản hồi đến
        bước tiếp theo được chỉ định trong Thông Điệp Trả Lời Xây Dựng Đường Hầm
 bit 5-0: Chưa xác định, cần đặt thành 0 để tương thích với các tùy chọn tương lai

Bit 7 chỉ ra rằng bước sẽ là cổng vào (IBGW). Bit 6
chỉ ra rằng bước sẽ là điểm kết thúc đầu ra (OBEP). Nếu cả hai bit không được
đặt, bước sẽ là một người tham gia trung gian. Cả hai không thể được đặt đồng thời.

Loại mã hóa tầng: 0 cho AES (như trong các đường hầm hiện tại);
1 cho tương lai (ChaCha?)

Thời gian hết hạn yêu cầu là cho thời lượng đường hầm thay đổi trong tương lai.
Hiện tại, chỉ có giá trị hỗ trợ là 600 (10 phút).

Khóa công khai tạm thời của người tạo là một khóa ECIES, big-endian.
Nó được sử dụng cho KDF để tạo ra các khóa và IVs tầng và trả lời của IBGW.
Điều này chỉ được bao gồm trong bản ghi văn bản rõ ràng trong một thông điệp Xây Dựng Đường Hầm vào.
Nó cần thiết vì không có DH ở tầng này cho bản ghi xây dựng.

Tùy chọn xây dựng đường hầm là một cấu trúc Mapping như được định nghĩa trong [Common](/en/docs/spec/common-structures/).
Đây là cho việc sử dụng trong tương lai. Không có tùy chọn nào hiện được định nghĩa.
Nếu cấu trúc Mapping trống rỗng, đây là hai byte 0x00 0x00.
Kích thước tối đa của Mapping (bao gồm trường độ dài) là 98 byte,
và giá trị tối đa của trường độ dài Mapping là 96.



#### Bản Ghi Yêu Cầu Ngắn Mã Hóa

Tất cả các trường đều là big-endian, ngoại trừ khóa công khai thểm thời là little-endian.

Kích thước mã hóa: 218 byte


```
bytes    0-15: Hash định danh rút gọn của Hop
  bytes   16-47: Khóa công khai X25519 tạm thời của Người gửi
  bytes  48-201: Bản Ghi Yêu Cầu Xây Dựng Ngắn mã hóa ChaCha20
  bytes 202-217: Poly1305 MAC

```



### Bản Ghi Trả Lời Ngắn


#### Bản Ghi Trả Lời Ngắn Không Mã Hóa

Đây là đặc tả đề xuất cho bản ghi Trả Lời Xây Dựng Ngắn cho các bộ định tuyến ECIES-X25519.
Tóm tắt các thay đổi từ [Tunnel-Creation-ECIES](/en/docs/spec/tunnel-creation-ecies/):

- Thay đổi độ dài không mã hóa từ 512 thành 202 byte
- Thay đổi độ dài mã hóa từ 528 thành 218 byte


Trả lời ECIES được mã hóa với ChaCha20/Poly1305.

Tất cả các trường đều là big-endian.

Kích thước không mã hóa: 202 byte.


```
bytes    0-x: Tùy Chọn Trả Lời Xây Dựng Đường Hầm (Mapping)
  bytes    x-x: dữ liệu khác như được ám bởi các tùy chọn
  bytes  x-200: Dồn ngẫu nhiên (xem bên dưới)
  byte     201: Byte Trả Lời

```

Tùy chọn Trả Lời Xây Dựng Đường Hầm là một cấu trúc Mapping như được định nghĩa trong [Common](/en/docs/spec/common-structures/).
Đây là cho việc sử dụng trong tương lai. Không có tùy chọn nào hiện đang được định nghĩa.
Nếu cấu trúc Mapping trống rỗng, đây là hai byte 0x00 0x00.
Kích thước tối đa của Mapping (bao gồm trường độ dài) là 201 byte,
và giá trị tối đa của trường độ dài Mapping là 199.

Byte trả lời là một trong các giá trị sau
như được định nghĩa trong [Tunnel-Creation](/en/docs/spec/tunnel-creation/) để tránh nhận diện:

- 0x00 (chấp nhận)
- 30 (TUNNEL_REJECT_BANDWIDTH)


#### Bản Ghi Trả Lời Ngắn Mã Hóa

Kích thước mã hóa: 218 byte


```
bytes   0-201: Bản Ghi Trả Lời Xây Dựng Ngắn mã hóa ChaCha20
  bytes 202-217: Poly1305 MAC

```



### KDF

Xem phần KDF bên dưới.




### ShortTunnelBuild
Loại I2NP 25

Thông điệp này được gửi đến các bước trung gian, OBEP, và IBEP (người tạo).
Nó không được gửi đến IBGW (sử dụng Xây Dựng Đường Hầm vào mã hóa garlic thay thế).
Khi được nhận bởi OBEP, nó được chuyển thành một OutboundTunnelBuildReply,
mã hóa garlic, và gửi đến người tạo.



```
+----+----+----+----+----+----+----+----+
  | num| ShortBuildRequestRecords...
  +----+----+----+----+----+----+----+----+

  num ::
         1 byte `Integer`
         Giá trị hợp lệ: 1-8

  kích thước bản ghi: 218 byte
  tổng kích thước: 1+$num*218
```

#### Ghi chú

* Số lượng bản ghi điển hình là 4, cho tổng kích thước là 873.




### OutboundTunnelBuildReply
Loại I2NP 26

Thông điệp này chỉ được gửi bởi OBEP đến IBEP (người tạo) qua một đường hầm vào hiện có.
Nó không được gửi đến bất kỳ bước nào khác.
Nó luôn luôn được mã hóa garlic.


```
+----+----+----+----+----+----+----+----+
  | num|                                  |
  +----+                                  +
  |      ShortBuildReplyRecords...        |
  +----+----+----+----+----+----+----+----+

  num ::
         Tổng số bản ghi,
         1 byte `Integer`
         Giá trị hợp lệ: 1-8

  ShortBuildReplyRecords ::
         Bản ghi đã mã hóa
         chiều dài: num * 218

  kích thước bản ghi mã hóa: 218 byte
  tổng kích thước: 1+$num*218
```

#### Ghi chú

* Số lượng bản ghi điển hình là 4, cho tổng kích thước là 873.
* Thông điệp này nên được mã hóa garlic.



### KDF

Chúng tôi sử dụng ck từ trạng thái Noise sau khi mã hóa/giải mã bản ghi xây dựng đường hầm
để phát sinh các khóa sau: khóa trả lời, khóa lớp AES, khóa IV AES và khóa/tag trả lời garlic cho OBEP.

Khóa trả lời:
Không giống như bản ghi dài, chúng ta không thể sử dụng phần trái của ck cho khóa trả lời, vì nó không phải là cuối cùng và sẽ được sử dụng sau này.
Khóa trả lời được sử dụng để mã hóa trả lời cho bản ghi bằng AEAD/ChaCha20/Poly1305 và ChaCha20 để trả lời các bản ghi khác.
Cả hai sử dụng cùng khóa, nonce là vị trí của bản ghi trong thông điệp bắt đầu từ 0.


```
keydata = HKDF(ck, ZEROLEN, "SMTunnelReplyKey", 64)
  replyKey = keydata[32:63]
  ck = keydata[0:31]

  Khóa lớp:
  Khóa lớp luôn là AES cho đến nay, nhưng cùng KDF có thể được sử dụng từ ChaCha20

  keydata = HKDF(ck, ZEROLEN, "SMTunnelLayerKey", 64)
  layerKey = keydata[32:63]

  Khóa IV cho bản ghi không-OBEP:
  ivKey = keydata[0:31]
  vì đây là cuối cùng

  Khóa IV cho bản ghi OBEP:
  ck = keydata[0:31]
  keydata = HKDF(ck, ZEROLEN, "TunnelLayerIVKey", 64)
  ivKey = keydata[32:63]
  ck = keydata[0:31]

  Khóa/tag trả lời garlic cho OBEP:
  keydata = HKDF(ck, ZEROLEN, "RGarlicKeyAndTag", 64)
  replyKey = keydata[32:63]
  replyTag = keydata[0:7]

```





## Biện Minh

Thiết kế này tối đa hóa tái sử dụng các nguyên tố mã hóa, giao thức và mã hiện có.

Thiết kế này giảm thiểu rủi ro.

ChaCha20 nhanh hơn một chút so với AES cho các bản ghi nhỏ, trong thử nghiệm Java.
ChaCha20 tránh yêu cầu đối với kích thước dữ liệu là bội số của 16.


## Ghi Chú Triển Khai

- Cũng như với các thông điệp xây dựng đường hầm biến hiện có,
  không khuyến khích sử dụng các thông điệp nhỏ hơn 4 bản ghi.
  Mặc định điển hình là 3 hops.
  Các đường hầm vào phải được xây dựng với một bản ghi bổ sung cho
  người tạo, để hop cuối không biết nó là cuối cùng.
  Để các bước trung gian không biết đường hầm là vào hay ra ngoài,
  các đường hầm ra cũng nên được xây dựng với 4 bản ghi.



## Vấn Đề



## Di Cư

Việc triển khai, thử nghiệm, và triển khai sẽ mất một số phát hành
và khoảng một năm. Các giai đoạn như sau. Việc phân công
mỗi giai đoạn cho một phát hành cụ thể sẽ được quyết định và phụ thuộc vào
tốc độ phát triển.

Các chi tiết của việc triển khai và di chuyển có thể khác nhau cho
mỗi triển khai I2P.

Người tạo đường hầm phải đảm bảo rằng tất cả các bước trong đường hầm được tạo là ECIES-X25519, VÀ ít nhất là phiên bản TBD.
Người tạo đường hầm KHÔNG cần phải là ECIES-X25519; nó có thể là ElGamal.
Tuy nhiên, nếu người tạo là ElGamal, nó tiết lộ cho hop gần nhất rằng nó là người tạo.
Vì vậy, trong thực tế, các tuyến này chỉ nên được tạo bởi các bộ định tuyến ECIES.

Nó KHÔNG cần thiết đối với OBEP hoặc IBGW của đường hầm đôi là ECIES hoặc
của bất kỳ phiên bản cụ thể nào.
Các thông điệp mới được mã hóa garlic và không nhìn thấy tại OBEP hoặc IBGW
của đường hầm đôi.

Giai đoạn 1: Triển khai, không được bật mặc định

Giai đoạn 2 (phát hành tiếp theo): Bật mặc định

Không có vấn đề tương thích ngược. Các thông điệp mới chỉ có thể được gửi đến các bộ định tuyến hỗ trợ chúng.




## Phụ lục


Không có độ trễ garlic cho STBM vào chưa mã hóa,
nếu chúng ta không sử dụng ITBM:



```
Kích thước 4 khe hiện tại: 4 * 528 + độ trễ = 3 thông điệp đường hầm

  Thông điệp xây dựng 4 khe để vừa trong một thông điệp đường hầm, chỉ ECIES:

  1024
  - 21 tiêu đề phân đoạn
  ----
  1003
  - 35 hướng dẫn giao hàng không phân đoạn ROUTER
  ----
  968
  - 16 tiêu đề I2NP
  ----
  952
  - 1 số khe
  ----
  951
  / 4 khe
  ----
  237 Kích thước bản ghi xây dựng mã hóa mới (so với 528 hiện tại)
  - 16 hash rút gọn
  - 32 khóa tạm thời
  - 16 MAC
  ----
  173 kích thước bản ghi xây dựng dạng văn bản tối đa (so với 222 hiện tại)



```


Có độ trễ garlic cho mẫu 'N' noise để mã hóa STBM vào,
nếu chúng ta không sử dụng ITBM:


```
Kích thước 4 khe hiện tại: 4 * 528 + độ trễ = 3 thông điệp đường hầm

  Thông điệp xây dựng được mã hóa garlic 4 khe để vừa trong một thông điệp đường hầm, chỉ ECIES:

  1024
  - 21 tiêu đề phân đoạn
  ----
  1003
  - 35 hướng dẫn giao hàng không phân đoạn ROUTER
  ----
  968
  - 16 tiêu đề I2NP
  -  4 chiều dài
  ----
  948
  - 32 byte khóa tạm thời
  ----
  916
  - 7 byte khối DateTime
  ----
  909
  - 3 byte độ trễ khối Garlic
  ----
  906
  - 9 byte tiêu đề I2NP
  ----
  897
  - 1 byte hướng dẫn giao hàng Garlic LOCAL
  ----
  896
  - 16 byte Poly1305 MAC
  ----
  880
  - 1 số khe
  ----
  879
  / 4 khe
  ----
  219 Kích thước bản ghi xây dựng mã hóa mới (so với 528 hiện tại)
  - 16 hash rút gọn
  - 32 khóa tạm thời
  - 16 MAC
  ----
  155 kích thước bản ghi xây dựng dạng văn bản tối đa (so với 222 hiện tại)


```

Ghi chú:

Kích thước bản ghi xây dựng dạng văn bản trước khi đệm không sử dụng: 193

Việc loại bỏ hash router đầy đủ và phát sinh khóa/IVs từ HKDF sẽ giải phóng nhiều không gian cho các tùy chọn trong tương lai.
Nếu tất cả đều là HKDF, không gian rõ ràng yêu cầu khoảng 58 byte (không bao gồm bất kỳ tùy chọn nào).

OTBRM bọc garlic sẽ nhỏ hơn một chút so với STBM bọc garlic,
vì các hướng dẫn giao hàng là LOCAL không phải ROUTER,
không có khối DATETIME bao gồm, và
nó sử dụng một tag 8-byte thay vì khóa tạm thời 32-byte cho một thông điệp 'N' đầy đủ.



## Tài liệu Tham Khảo
