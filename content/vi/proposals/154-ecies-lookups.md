---
title: "Tra cứu cơ sở dữ liệu từ các đích đến ECIES"
number: "154"
author: "zzz"
created: "2020-03-23"
lastupdated: "2021-01-08"
status: "Đã đóng"
thread: "http://zzz.i2p/topics/2856"
target: "0.9.46"
implementedin: "0.9.46"
toc: true
---

## Lưu ý
ECIES đến ElG đã được triển khai trong 0.9.46 và giai đoạn đề xuất đã khép lại.
Xem [I2NP](/docs/specs/i2np/) để biết thông số kỹ thuật chính thức.
Đề xuất này vẫn có thể được tham khảo để có thông tin nền tảng.
ECIES đến ECIES với các khóa được bao gồm đã được thực hiện kể từ 0.9.48.
Phần ECIES-to-ECIES (khóa dẫn xuất) có thể được mở lại hoặc kết hợp
trong một đề xuất tương lai.


## Tổng quan

### Định nghĩa

- AEAD: ChaCha20/Poly1305
- DLM: Thông báo tra cứu cơ sở dữ liệu I2NP
- DSM: Thông báo lưu trữ cơ sở dữ liệu I2NP
- DSRM: Thông báo phản hồi tìm kiếm cơ sở dữ liệu I2NP
- ECIES: ECIES-X25519-AEAD-Ratchet (đề xuất 144)
- ElG: ElGamal
- ENCRYPT(k, n, payload, ad): Như đã định nghĩa trong [ECIES](/docs/specs/ecies/)
- LS: Leaseset
- tra cứu: DLM I2NP
- phản hồi: DSM hoặc DSRM I2NP


### Tóm tắt

Khi gửi một DLM cho một LS đến floodfill, DLM thường chỉ định
rằng phản hồi được gắn nhãn, mã hóa AES, và gửi xuống thông qua một đường hầm đến đích.
Hỗ trợ cho việc phản hồi mã hóa AES đã được thêm vào trong 0.9.7.

Phản hồi mã hóa AES đã được chỉ định trong 0.9.7 để giảm thiểu chi phí lớn của mật mã
của ElG, và bởi vì nó tái sử dụng khả năng thẻ/AES
trong ElGamal/AES+SessionTags.
Tuy nhiên, phản hồi AES có thể bị sửa đổi tại IBEP vì không có xác thực,
và phản hồi không có bảo mật chuyển tiếp.

Với các đích đến [ECIES](/docs/specs/ecies/), ý định của đề xuất 144 là
các đích không còn hỗ trợ các thẻ 32 byte và giải mã AES.
Các chi tiết đã được cố ý không bao gồm trong đề xuất đó.

Đề xuất này tài liệu hóa một tùy chọn mới trong DLM để yêu cầu các phản hồi mã hóa ECIES.


### Mục tiêu

- Các cờ mới cho DLM khi một phản hồi mã hóa được yêu cầu thông qua một đường hầm đến một đích ECIES
- Đối với phản hồi, thêm bảo mật chuyển tiếp và xác thực người gửi chống lại
  việc chiếm đoạt khóa của người yêu cầu (đích đến).
- Duy trì ẩn danh của người yêu cầu
- Giảm thiểu chi phí lớn của mật mã

### Không phải là mục tiêu

- Không có thay đổi nào đối với mã hóa hoặc tính năng bảo mật của tra cứu (DLM).
  Tra cứu chỉ có bảo mật chuyển tiếp cho việc chiếm đoạt khóa của người yêu cầu.
  Mã hóa là cho khóa tĩnh của floodfill.
- Không có vấn đề bảo mật chuyển tiếp hoặc xác thực người gửi chống lại
  việc chiếm đoạt khóa của người phản hồi (floodfill).
  Floodfill là một cơ sở dữ liệu công cộng và sẽ phản hồi tra cứu từ bất kỳ ai.
- Không thiết kế các bộ định tuyến ECIES trong đề xuất này.
  Nơi mà khóa công cộng X25519 của một bộ định tuyến đi là TBD.


## Các lựa chọn thay thế

Trong trường hợp không có cách đã định nào để mã hóa các phản hồi đến các đích ECIES, có
một số lựa chọn thay thế:

1) Không yêu cầu phản hồi mã hóa. Phản hồi sẽ không mã hóa.
Java I2P hiện sử dụng cách tiếp cận này.

2) Thêm hỗ trợ cho thẻ 32 byte và các phản hồi mã hóa AES đến các đích chỉ ECIES,
và yêu cầu phản hồi mã hóa AES như thường lệ. i2pd hiện sử dụng cách tiếp cận này.

3) Yêu cầu phản hồi mã hóa AES như thường lệ, nhưng định tuyến lại thông qua
các đường hầm thăm dò đến bộ định tuyến.
Java I2P hiện sử dụng cách tiếp cận này trong một số trường hợp.

4) Đối với các đích đến kép ElG và ECIES,
yêu cầu phản hồi mã hóa AES như thường lệ. Java I2P hiện sử dụng cách tiếp cận này.
i2pd chưa thực hiện các đích đến mã hóa kép.


## Thiết kế

- Định dạng DLM mới sẽ thêm một bit vào trường cờ để chỉ định phản hồi mã hóa ECIES.
  Các phản hồi mã hóa ECIES sẽ sử dụng định dạng thông điệp Phiên hiện có [ECIES](/docs/specs/ecies/),
  với một thẻ đi kèm và một payload và MAC ChaCha/Poly.

- Định nghĩa hai biến thể. Một dành cho các bộ định tuyến ElG, nơi mà một thao tác DH không thể thực hiện,
  và một cho các bộ định tuyến ECIES trong tương lai, nơi mà một thao tác DH có thể thực hiện và có thể cung cấp
  thêm bảo mật. Cần nghiên cứu thêm.

Thao tác DH không thể thực hiện được cho các phản hồi từ các bộ định tuyến ElG vì chúng không công bố
một khóa công khai X25519.


## Thông số kỹ thuật

Trong thông số kỹ thuật DLM (DatabaseLookup) [I2NP](/docs/specs/i2np/), thực hiện các thay đổi sau đây.

Thêm bit 4 "ECIESFlag" cho các tùy chọn mã hóa mới.

```text
flags ::
       bit 4: ECIESFlag
               trước bản phát hành 0.9.46 bị bỏ qua
               kể từ bản phát hành 0.9.46:
               0  => gửi phản hồi không mã hóa hoặc ElGamal
               1  => gửi phản hồi mã hóa ChaCha/Poly sử dụng khóa kèm theo
                     (thẻ có được đính kèm hay không phụ thuộc vào bit 1)
```

Bit cờ 4 được sử dụng kết hợp với bit 1 để xác định chế độ mã hóa phản hồi.
Bit cờ 4 chỉ nên được thiết lập khi gửi đến các bộ định tuyến phiên bản 0.9.46 hoặc cao hơn.


Trong bảng dưới,
"DH n/a" nghĩa là phản hồi không được mã hóa.
"DH không" nghĩa là các khóa phản hồi được bao gồm trong yêu cầu.
"DH có" nghĩa là các khóa phản hồi được dẫn xuất từ thao tác DH.


| Bits cờ 4,1 | Từ Đích | Đến Bộ định tuyến | Phản hồi | DH? | ghi chú |
|-------------|---------|-------------------|----------|-----|---------|
| 0 0          | Bất kỳ  | Bất kỳ            | không mã hóa | n/a | hiện tại |
| 0 1          | ElG     | ElG               | AES      | không | hiện tại |
| 0 1          | ECIES   | ElG               | AES      | không | i2pd giải pháp tạm thời |
| 1 0          | ECIES   | ElG               | AEAD     | không | đề xuất này |
| 1 0          | ECIES   | ECIES             | AEAD     | không | 0.9.49 |
| 1 1          | ECIES   | ECIES             | AEAD     | có   | tương lai |


### ElG đến ElG

Đích ElG gửi một tra cứu đến một bộ định tuyến ElG.

Thay đổi nhỏ trong thông số kỹ thuật để kiểm tra bit mới 4.
Không có thay đổi nào đối với định dạng nhị phân hiện có.


Tạo khóa người yêu cầu (làm rõ):

```text
reply_key :: CSRNG(32) 32 byte dữ liệu ngẫu nhiên
  reply_tags :: Mỗi cái là CSRNG(32) 32 byte dữ liệu ngẫu nhiên
```

Định dạng thông điệp (thêm kiểm tra ECIESFlag):

```text
reply_key ::
       32 byte `SessionKey` big-endian
       chỉ bao gồm nếu encryptionFlag == 1 VÀ ECIESFlag == 0, chỉ kể từ bản phát hành 0.9.7

  tags ::
       1 byte `Integer`
       phạm vi hợp lệ: 1-32 (thường là 1)
       số lượng thẻ phản hồi kèm theo
       chỉ bao gồm nếu encryptionFlag == 1 VÀ ECIESFlag == 0, chỉ kể từ bản phát hành 0.9.7

  reply_tags ::
       một hoặc nhiều 32 byte `SessionTag`s (thường là một)
       chỉ bao gồm nếu encryptionFlag == 1 VÀ ECIESFlag == 0, chỉ kể từ bản phát hành 0.9.7
```


### ECIES đến ElG

Đích ECIES gửi một tra cứu đến một bộ định tuyến ElG.
Hỗ trợ kể từ 0.9.46.

Các trường reply_key và reply_tags được định nghĩa lại cho một phản hồi mã hóa ECIES.

Tạo khóa người yêu cầu:

```text
reply_key :: CSRNG(32) 32 byte dữ liệu ngẫu nhiên
  reply_tags :: Mỗi cái là CSRNG(8) 8 byte dữ liệu ngẫu nhiên
```

Định dạng thông điệp:
Định nghĩa lại các trường reply_key và reply_tags như sau:

```text
reply_key ::
       32 byte ECIES `SessionKey` big-endian
       chỉ bao gồm nếu encryptionFlag == 0 VÀ ECIESFlag == 1, chỉ kể từ bản phát hành 0.9.46

  tags ::
       1 byte `Integer`
       giá trị bắt buộc: 1
       số lượng thẻ phản hồi tiếp theo
       chỉ bao gồm nếu encryptionFlag == 0 VÀ ECIESFlag == 1, chỉ kể từ bản phát hành 0.9.46

  reply_tags ::
       một 8 byte ECIES `SessionTag`
       chỉ bao gồm nếu encryptionFlag == 0 VÀ ECIESFlag == 1, chỉ kể từ bản phát hành 0.9.46
```


Phản hồi là một thông điệp Phiên hiện có ECIES, như đã định nghĩa trong [ECIES](/docs/specs/ecies/).

```text
tag :: 8 byte reply_tag

  k :: 32 byte session key
     Khóa phản hồi.

  n :: 0

  ad :: Thẻ reply_tag dài 8 byte

  payload :: Dữ liệu văn bản thuần túy, DSM hoặc DSRM.

  ciphertext = ENCRYPT(k, n, payload, ad)
```


### ECIES đến ECIES (0.9.49)

Đích hoặc bộ định tuyến ECIES gửi một tra cứu đến một bộ định tuyến ECIES, với các khóa phản hồi đi kèm.
Hỗ trợ kể từ 0.9.49.

Các bộ định tuyến ECIES đã được giới thiệu trong 0.9.48, xem [Prop156](/proposals/156-ecies-routers/).
Kể từ 0.9.49, các đích và bộ định tuyến ECIES có thể sử dụng cùng định dạng như trong
phần "ECIES đến ElG" ở trên, với các khóa phản hồi được bao gồm trong yêu cầu.
Tra cứu sẽ sử dụng "định dạng một lần" trong [ECIES](/docs/specs/ecies/)
do người yêu cầu là ẩn danh.

Đối với một phương pháp mới với các khóa dẫn xuất, xem phần tiếp theo.


### ECIES đến ECIES (tương lai)

Đích hoặc bộ định tuyến ECIES gửi một tra cứu đến một bộ định tuyến ECIES, và các khóa phản hồi được dẫn xuất từ DH.
Chưa được định nghĩa đầy đủ hoặc hỗ trợ, triển khai là TBD.

Tra cứu sẽ sử dụng "định dạng một lần" trong [ECIES](/docs/specs/ecies/)
do người yêu cầu là ẩn danh.

Định nghĩa lại trường reply_key như sau. Không có thẻ đi kèm nào.
Thẻ sẽ được tạo trong KDF dưới đây.

Phần này chưa hoàn chỉnh và cần nghiên cứu thêm.


```text
reply_key ::
       32 byte khóa công khai X25519 tạm thời của người yêu cầu, little-endian
       chỉ bao gồm nếu encryptionFlag == 1 VÀ ECIESFlag == 1, chỉ kể từ bản phát hành 0.9.TBD
```

Phản hồi là một thông điệp Phiên hiện có ECIES, như đã định nghĩa trong [ECIES](/docs/specs/ecies/).
Xem [ECIES](/docs/specs/ecies/) để biết tất cả các định nghĩa.


```text
// Khóa tạm thời X25519 của Alice
  // aesk = khóa riêng tạm thời của Alice
  aesk = GENERATE_PRIVATE()
  // aepk = khóa công khai tạm thời của Alice
  aepk = DERIVE_PUBLIC(aesk)
  // Khóa tĩnh X25519 của Bob
  // bsk = khóa riêng tĩnh của Bob
  bsk = GENERATE_PRIVATE()
  // bpk = khóa công khai tĩnh của Bob
  // bpk có thể là một phần của RouterIdentity, hoặc công bố trong RouterInfo (TBD)
  bpk = DERIVE_PUBLIC(bsk)

  // (DH()
  //[chainKey, k] = MixKey(sharedSecret)
  // chainKey từ ???
  sharedSecret = DH(aesk, bpk) = DH(bsk, aepk)
  keydata = HKDF(chainKey, sharedSecret, "ECIES-DSM-Reply1", 32)
  chainKey = keydata[0:31]

  1) rootKey = chainKey từ Phần Payload
  2) k từ KDF Phiên Mới hoặc split()

  // KDF_RK(rk, dh_out)
  keydata = HKDF(rootKey, k, "KDFDHRatchetStep", 64)

  // Đầu ra 1: không sử dụng
  unused = keydata[0:31]
  // Đầu ra 2: Khóa chuỗi để khởi tạo
  // các thẻ phiên và bánh răng khóa đối xứng
  // cho các truyền từ Alice đến Bob
  ck = keydata[32:63]

  // các khóa chuỗi khóa thẻ phiên và khóa đối xứng
  keydata = HKDF(ck, ZEROLEN, "TagAndKeyGenKeys", 64)
  sessTag_ck = keydata[0:31]
  symmKey_ck = keydata[32:63]

  tag :: 8 byte thẻ sinh ra từ RATCHET_TAG() trong [ECIES](/docs/specs/ecies/)

  k :: 32 byte khóa sinh ra từ RATCHET_KEY() trong [ECIES](/docs/specs/ecies/)

  n :: Chỉ số của thẻ. Thường là 0.

  ad :: Thẻ 8 byte

  payload :: Dữ liệu văn bản thuần túy, DSM hoặc DSRM.

  ciphertext = ENCRYPT(k, n, payload, ad)
```


### Định dạng phản hồi

Đây là thông điệp phiên hiện có,
giống như trong [ECIES](/docs/specs/ecies/), được sao chép bên dưới để tham khảo.

```text
+----+----+----+----+----+----+----+----+
  |       Thẻ Phiên                      |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +            Phần Payload              +
  |       Dữ liệu mã hóa ChaCha20     |
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Mã Xác thực Thông điệp Poly1305  |
  +              (MAC)                    +
  |             16 byte                  |
  +----+----+----+----+----+----+----+----+

  Thẻ Phiên :: 8 byte, văn bản rõ

  Dữ liệu mã hóa Phần Payload :: dữ liệu còn lại trừ 16 byte

  MAC :: mã xác thực thông điệp Poly1305, 16 byte
```


## Lý do

Các tham số mã hóa phản hồi trong tra cứu, đầu tiên được giới thiệu trong 0.9.7, 
có phần nào là một vi phạm lớp. Nó được thực hiện theo cách này để đạt hiệu quả.
Nhưng cũng bởi vì tra cứu là ẩn danh.

Chúng ta có thể làm cho định dạng tra cứu tổng quát hơn, giống như với một trường loại mã hóa,
nhưng có lẽ điều đó gây phiền toái hơn là đáng giá.

Đề xuất trên là dễ dàng nhất và giảm thiểu thay đổi đối với định dạng tra cứu.


## Ghi chú

Các tra cứu và lưu trữ cơ sở dữ liệu đến các bộ định tuyến ElG cần được mã hóa ElGamal/AESSessionTag
như thường lệ.


## Vấn đề

Cần phân tích thêm về tính bảo mật của hai tùy chọn phản hồi ECIES.


## Di chuyển

Không có vấn đề tương thích ngược. Các bộ định tuyến quảng cáo phiên bản router.version 0.9.46 hoặc cao hơn
trong RouterInfo của họ phải hỗ trợ tính năng này.
Các bộ định tuyến không được gửi một DatabaseLookup với các cờ mới đến các bộ định tuyến với phiên bản dưới 0.9.46.
Nếu một thông điệp tra cứu cơ sở dữ liệu với bit 4 được thiết lập và bit 1 không thiết lập được gửi nhầm đến
một bộ định tuyến không có hỗ trợ, có thể nó sẽ bỏ qua khóa và thẻ được cung cấp, và
gửi phản hồi không mã hóa.
