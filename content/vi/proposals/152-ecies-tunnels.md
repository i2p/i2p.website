```markdown
---
title: "Đường Hầm ECIES"
number: "152"
author: "chisana, zzz, orignal"
created: "2019-07-04"
lastupdated: "2025-03-05"
status: "Closed"
thread: "http://zzz.i2p/topics/2737"
target: "0.9.48"
implementedin: "0.9.48"
---

## Lưu ý
Triển khai mạng và thử nghiệm đang tiến hành.
Có thể có sửa đổi nhỏ.
Xem [SPEC](/en/docs/spec/) để có được đặc tả chính thức.


## Tổng quan

Tài liệu này đề xuất thay đổi mã hóa tin nhắn xây dựng đường hầm
sử dụng các khối mật mã được giới thiệu bởi [ECIES-X25519](/en/docs/spec/ecies/).
Đây là một phần của đề xuất tổng thể
[Prop156](/en/proposals/156-ecies-routers/) để chuyển đổi router từ ElGamal sang ECIES-X25519.

Với mục đích chuyển đổi mạng từ ElGamal + AES256 sang ECIES + ChaCha20,
cần có các đường hầm với các router ElGamal và ECIES hỗn hợp.
Các yêu cầu để xử lý các bước nhảy trong đường hầm hỗn hợp được cung cấp.
Không có thay đổi nào sẽ được thực hiện với định dạng, xử lý hoặc mã hóa các bước nhảy ElGamal.

Người tạo đường hầm ElGamal sẽ cần tạo các cặp khóa X25519 tạm thời cho mỗi lần nhảy,
và theo đặc tả này để tạo các đường hầm chứa các bước nhảy ECIES.

Đề xuất này chỉ rõ các thay đổi cần thiết cho Xây Dựng Đường Hầm ECIES-X25519.
Để có tổng quan về tất cả các thay đổi cần thiết cho các router ECIES, hãy xem đề xuất 156 [Prop156](/en/proposals/156-ecies-routers/).

Đề xuất này duy trì cùng kích thước cho các bản ghi xây dựng đường hầm,
như yêu cầu cho tương thích. Các bản ghi xây dựng và tin nhắn nhỏ hơn sẽ được
thực hiện sau - xem [Prop157](/en/proposals/157-new-tbm/).


### Nguyên tắc Mã hóa

Không có nguyên tắc mã hóa mới nào được giới thiệu. Các nguyên tắc cần thiết để thực hiện đề xuất này là:

- AES-256-CBC như trong [Cryptography](/en/docs/spec/cryptography/)
- Chức năng STREAM ChaCha20/Poly1305:
  ENCRYPT(k, n, plaintext, ad) và DECRYPT(k, n, ciphertext, ad) - như trong [NTCP2](/en/docs/spec/ntcp2/) [ECIES-X25519](/en/docs/spec/ecies/) và [RFC-7539](https://tools.ietf.org/html/rfc7539)
- Chức năng X25519 DH - như trong [NTCP2](/en/docs/spec/ntcp2/) và [ECIES-X25519](/en/docs/spec/ecies/)
- HKDF(salt, ikm, info, n) - như trong [NTCP2](/en/docs/spec/ntcp2/) và [ECIES-X25519](/en/docs/spec/ecies/)

Các chức năng Noise khác được định nghĩa ở nơi khác:

- MixHash(d) - như trong [NTCP2](/en/docs/spec/ntcp2/) và [ECIES-X25519](/en/docs/spec/ecies/)
- MixKey(d) - như trong [NTCP2](/en/docs/spec/ntcp2/) và [ECIES-X25519](/en/docs/spec/ecies/)


### Mục tiêu

- Tăng tốc độ hoạt động mã hóa
- Thay thế ElGamal + AES256/CBC bằng các khối ECIES cho các bản ghi yêu cầu và trả lời xây dựng đường hầm.
- Không thay đổi kích thước của các bản ghi yêu cầu và trả lời xây dựng mã hóa (528 byte) để tương thích
- Không có tin nhắn I2NP mới
- Duy trì kích thước bản ghi xây dựng mã hóa để tương thích
- Thêm bảo mật chuyển tiếp cho Tin nhắn Xây dựng Đường hầm.
- Thêm mã hóa xác thực
- Phát hiện thứ tự lại các bản ghi yêu cầu xây dựng
- Tăng độ phân giải của dấu thời gian sao cho kích thước bộ lọc Bloom có thể được giảm
- Thêm trường cho hết hạn đường hầm sao cho có thể thay đổi thời gian tồn tại đường hầm (chỉ áp dụng cho tất cả các đường hầm ECIES)
- Thêm trường tùy chọn mở rộng cho các tính năng trong tương lai
- Sử dụng lại các khối mã hóa hiện có
- Cải thiện an ninh tin nhắn xây dựng đường hầm nếu có thể trong khi duy trì khả năng tương thích
- Hỗ trợ các đường hầm với đồng thời cả những người tham gia ElGamal/ECIES
- Cải thiện các biện pháp phòng thủ chống lại các cuộc tấn công "đánh dấu" trên tin nhắn xây dựng
- Các bước nhảy không cần biết loại mã hóa của các bước nhảy tiếp theo trước khi xử lý tin nhắn xây dựng,
  vì họ có thể chưa có RI của bước nhảy tiếp theo vào lúc đó
- Tối đa hóa khả năng tương thích với mạng hiện tại
- Không thay đổi mã hóa yêu cầu/đáp ứng AES xây dựng đường hầm cho các router ElGamal
- Không thay đổi mã hóa "lớp" AES đường hầm, cho điều đó xem [Prop153](/en/proposals/153-chacha20-layer-encryption/)
- Tiếp tục hỗ trợ cả TBM/TBRM 8 bản ghi và VTBM/VTBRM có kích thước biến đổi
- Không yêu cầu nâng cấp "ngày lá cờ" cho toàn bộ mạng


### Không phải Mục tiêu

- Thiết kế lại hoàn toàn tin nhắn xây dựng đường hầm yêu cầu một "ngày lá cờ".
- Thu hẹp tin nhắn xây dựng đường hầm (yêu cầu tất cả các bước nhảy là ECIES và một đề xuất mới)
- Sử dụng các tùy chọn xây dựng đường hầm theo định nghĩa trong [Prop143](/en/proposals/143-build-message-options/), chỉ yêu cầu cho các thông điệp nhỏ
- Đường hầm hai chiều - cho điều đó xem [Prop119](/en/proposals/119-bidirectional-tunnels/)
- Các tin nhắn xây dựng đường hầm nhỏ hơn - cho điều đó xem [Prop157](/en/proposals/157-new-tbm/)


## Mô hình Mối đe dọa

### Mục tiêu Thiết kế

- Không có bước nhảy nào có thể xác định được nguồn gốc của đường hầm.

- Các bước nhảy giữa không được phép xác định hướng của đường hầm
  hay vị trí của họ trong đường hầm.

- Không có bước nhảy nào có thể đọc bất kỳ nội dung nào của các bản ghi yêu cầu hoặc đáp ứng khác, ngoại trừ
  hash router bị rút ngắn và khóa tạm thời cho bước nhảy tiếp theo

- Không có thành viên nào của đường hầm đáp ứng cho xây dựng ngược có thể đọc bất kỳ bản ghi đáp ứng nào.

- Không có thành viên nào của đường hầm phát sinh cho xây dựng vào có thể đọc bất kỳ bản ghi yêu cầu nào,
  ngoại trừ rằng OBEP có thể thấy hash router bị rút ngắn và khóa tạm thời cho IBGW




### Tấn công Đánh dấu

Một mục tiêu lớn của thiết kế xây dựng đường hầm là làm cho việc biết rằng họ đang ở trong một đường hầm duy nhất khó khăn hơn
cho các router hợp tác X và Y. Nếu router X ở bước nhảy m và router Y ở bước nhảy m + 1, họ rõ ràng sẽ biết.
Nhưng nếu router X ở bước nhảy m và router Y ở bước nhảy m + n cho n > 1, điều này sẽ khó khăn hơn nhiều.

Các cuộc tấn công đánh dấu là nơi router ở giữa X thay đổi tin nhắn xây dựng đường hầm theo cách mà
router Y có thể phát hiện sự thay đổi khi tin nhắn xây dựng đến đó.
Mục tiêu là giữ cho bất kỳ tin nhắn bị thay đổi nào bị router giữa X và Y loại bỏ trước khi đến router Y
Đối với các sửa đổi không bị loại bỏ trước router Y, người tạo đường hầm nên phát hiện sự hỏng hóc trong đáp ứng
và loại bỏ đường hầm.

Các tấn công có thể:

- Thay đổi một bản ghi xây dựng
- Thay thế một bản ghi xây dựng
- Thêm hoặc loại bỏ một bản ghi xây dựng
- Thay đổi thứ tự các bản ghi xây dựng





TODO: Hiện tại thiết kế này có ngăn chặn tất cả các cuộc tấn công này không?






## Thiết kế

### Khung Giao Thức Noise

Đề xuất này cung cấp các yêu cầu dựa trên Khung Giao Thức Noise
[NOISE](https://noiseprotocol.org/noise.html) (Bản sửa đổi 34, 2018-07-11).
Trong thuật ngữ Noise, Alice là người khởi tạo, và Bob là người đáp ứng.

Đề xuất này dựa trên giao thức Noise Noise_N_25519_ChaChaPoly_SHA256.
Giao thức Noise này sử dụng các khối sau:

- Mẫu Bắt Tay Một Chiều: N
  Alice không gửi chìa khóa tĩnh của mình cho Bob (N)

- Chức năng DH: X25519
  X25519 DH với một chiều dài khóa 32 byte như đã được quy định trong [RFC-7748](https://tools.ietf.org/html/rfc7748).

- Chức năng Mã hóa: ChaChaPoly
  AEAD_CHACHA20_POLY1305 như đã được quy định trong [RFC-7539](https://tools.ietf.org/html/rfc7539) phần 2.8.
  12 byte nonce, với bốn byte đầu tiên đặt thành zero.
  Giống như trong [NTCP2](/en/docs/spec/ntcp2/).

- Chức năng Hash: SHA256
  Hash chuẩn 32 byte, đã được sử dụng rộng rãi trong I2P.


Bổ sung vào Khung
`````````````````````

Không có.


### Mẫu Bắt Tay

Các thỏa thuận sử dụng mẫu [Noise](https://noiseprotocol.org/noise.html).

Cách ánh xạ chữ cái sau được sử dụng:

- e = khóa tạm thời dùng một lần
- s = khóa tĩnh
- p = tải trọng tin nhắn

Bản yêu cầu xây dựng giống hệt với mẫu Noise N.
Điều này cũng giống hệt với thông điệp đầu tiên (Yêu cầu Phiên) trong mẫu XK được sử dụng trong [NTCP2](/en/docs/spec/ntcp2/).


  ```dataspec

<- s
  ...
  e es p ->





  ```


### Mã hóa yêu cầu

Bản ghi yêu cầu xây dựng được tạo bởi người tạo đường hầm và mã hóa bất đối xứng với từng bước nhảy.
Mã hóa bất đối xứng của các bản ghi yêu cầu này hiện tại là ElGamal như được định nghĩa trong [Cryptography](/en/docs/spec/cryptography/)
và chứa một checksum SHA-256. Thiết kế này không có bảo mật chuyển tiếp.

Thiết kế mới sẽ sử dụng mẫu Noise một chiều "N" với ECIES-X25519 DH tạm thời-tĩnh, với một HKDF, và
ChaCha20/Poly1305 AEAD để bảo mật chuyển tiếp, tính toàn vẹn, và xác thực.
Alice là người yêu cầu xây dựng đường hầm. Mỗi bước nhảy trong đường hầm là một Bob.


(Tính chất Bảo mật Tải trọng)

  ```text

N:                      Xác thực   Bảo mật
    -> e, es                  0                2

    Xác thực: Không (0).
    Tải trọng này có thể đã được gửi bởi bất kỳ bên nào, bao gồm một kẻ tấn công chủ động.

    Bảo mật: 2.
    Mã hóa đến người nhận đã biết, bảo mật chuyển tiếp cho sự thỏa hiệp của người gửi
    chỉ, dễ bị lặp lại. Tải trọng này được mã hóa chỉ dựa trên các DH
    liên quan đến cặp khóa tĩnh của người nhận. Nếu khóa riêng tĩnh của người nhận bị xâm phạm,
    thậm chí vào một ngày sau, tải trọng này có thể được giải mã. Tin nhắn này cũng
    có thể lặp lại, vì không có yếu tố đóng góp tạm thời từ người nhận.

    "e": Alice tạo một cặp khóa tạm thời mới và lưu nó vào biến e
         ghi khóa công khai tạm thời dưới dạng văn bản rõ ràng vào
         bộ đệm tin nhắn, và băm khóa công khai cùng với h cũ để
         tạo ra một h mới.

    "es": Một DH được thực hiện giữa cặp khóa tạm thời của Alice và
          cặp khóa tĩnh của Bob. Kết quả được băm cùng với ck cũ để
          tạo ra một ck và k mới, và n được đặt thành zero.





  ```



### Mã hóa trả lời

Bản ghi trả lời xây dựng được tạo bởi người tạo bước nhảy và mã hóa đối xứng với người tạo.
Mã hóa đối xứng của các bản ghi trả lời hiện tại là AES với một checksum SHA-256 đứng trước.
và chứa một checksum SHA-256. Thiết kế này không có bảo mật chuyển tiếp.

Thiết kế mới sẽ sử dụng ChaCha20/Poly1305 AEAD để đảm bảo tính toàn vẹn, và xác thực.


### Biện minh

Khóa công khai tạm thời trong yêu cầu không cần phải được làm mờ với AES
hoặc Elligator2. Bước nhảy trước đó là bước nhảy duy nhất có thể thấy nó, và bước nhảy đó
biết rằng bước nhảy tiếp theo là ECIES.

Bản ghi trả lời không cần mã hóa bất đối xứng hoàn toàn với một DH khác.



## Đặc tả



### Bản ghi Yêu cầu Xây dựng

Các bản ghi Yêu cầu Xây dựng đã mã hóa dài 528 byte cho cả ElGamal và ECIES, để tương thích.


Bản ghi Yêu cầu Không Mã hóa (ElGamal)
`````````````````````````````````````````

Để tham khảo, đây là đặc tả hiện tại của bản ghi Yêu cầu Xây dựng Đường hầm cho các router ElGamal, lấy từ [I2NP](/en/docs/spec/i2np/).
Dữ liệu không mã hóa được đứng trước bởi một byte không phải zero và mã băm SHA-256 của dữ liệu trước khi mã hóa,
như được định nghĩa trong [Cryptography](/en/docs/spec/cryptography/).

Tất cả các trường đều là big-endian.

Kích thước không mã hóa: 222 byte

  ```dataspec


bytes     0-3: tunnel ID để nhận tin nhắn như là, không phải zero
  bytes    4-35: hash nhận dạng router cục bộ
  bytes   36-39: next tunnel ID, không phải zero
  bytes   40-71: hash nhận dạng router tiếp theo
  bytes  72-103: Khóa lớp tunnel AES-256
  bytes 104-135: Khóa IV tunnel AES-256
  bytes 136-167: Khóa trả lời AES-256
  bytes 168-183: IV trả lời AES-256
  byte      184: cờ
  bytes 185-188: thời gian yêu cầu (tính bằng giờ kể từ lúc epoch, làm tròn xuống)
  bytes 189-192: message ID tiếp theo
  bytes 193-221: đệm ngẫu nhiên / chưa được giải thích




  ```


Bản ghi Yêu cầu Mã hóa (ElGamal)
`````````````````````````````````````

Để tham khảo, đây là đặc tả hiện tại của bản ghi Yêu cầu Xây dựng Đường hầm cho các router ElGamal, lấy từ [I2NP](/en/docs/spec/i2np/).

Kích thước mã hóa: 528 byte

  ```dataspec


bytes    0-15: Hash nhận diện của Hop bị rút ngắn
  bytes  16-528: Bản ghi Yêu cầu Xây dựng ElGamal đã mã hóa




  ```




Bản ghi Yêu cầu Không Mã hóa (ECIES)
```````````````````````````````````````

Đây là đặc tả đề xuất của bản ghi Yêu cầu Xây dựng Đường hầm cho các router ECIES-X25519.
Tóm tắt các thay đổi:

- Loại bỏ hash router 32-byte không sử dụng
- Thay đổi thời gian yêu cầu từ giờ sang phút
- Thêm trường hết hạn cho thời gian đường hầm biến thiên trong tương lai
- Thêm nhiều không gian cho cờ
- Thêm Ánh xạ cho các tùy chọn xây dựng bổ sung
- Không sử dụng khóa và IV trả lời AES-256 cho bản ghi trả lời của hop
- Bản ghi không mã hóa dài hơn vì có ít chi phí mã hóa hơn


Bản ghi yêu cầu không chứa bất kỳ khóa trả lời ChaCha nào.
Những khóa đó được rút ra từ KDF. Xem bên dưới.

Tất cả các trường đều là big-endian.

Kích thước không mã hóa: 464 byte

  ```dataspec


bytes     0-3: tunnel ID để nhận tin nhắn như là, không phải zero
  bytes     4-7: next tunnel ID, không phải zero
  bytes    8-39: hash nhận dạng router tiếp theo
  bytes   40-71: Khóa lớp tunnel AES-256
  bytes  72-103: Khóa IV tunnel AES-256
  bytes 104-135: Khóa trả lời AES-256
  bytes 136-151: IV trả lời AES-256
  byte      152: cờ
  bytes 153-155: nhiều cờ hơn, không sử dụng, đặt thành 0 để tương thích
  bytes 156-159: thời gian yêu cầu (tính bằng phút kể từ lúc epoch, làm tròn xuống)
  bytes 160-163: hết hạn yêu cầu (tính bằng giây kể từ khi tạo)
  bytes 164-167: message ID tiếp theo
  bytes   168-x: các tùy chọn xây dựng đường hầm (Ánh xạ)
  bytes     x-x: dữ liệu khác được ngụ ý bởi cờ hoặc tùy chọn
  bytes   x-463: đệm ngẫu nhiên




  ```

Trường cờ giống như đã định nghĩa trong [Tunnel-Creation](/en/docs/spec/tunnel-creation/) và chứa các giá trị sau::

 Thứ tự bit: 76543210 (bit 7 là MSB)
 bit 7: nếu được đặt, cho phép tin nhắn từ bất kỳ ai
 bit 6: nếu được đặt, cho phép tin nhắn đến bất kỳ ai, và gửi trả lời tới
        bước nhảy tiếp theo được chỉ định trong một Tin nhắn Trả lời Xây dựng Đường hầm
 các bit 5-0: Chưa xác định, phải đặt giá trị 0 để tương thích với các tùy chọn tương lai

Bit 7 chỉ ra rằng hop sẽ là cổng vào đầu vào (IBGW). Bit 6
chỉ ra rằng hop sẽ là điểm cuối ra (OBEP). Nếu không bit nào được
đặt, hop sẽ là một người tham gia trung gian. Cả hai không thể được đặt cùng một lúc.

Hết hạn yêu cầu là cho thời gian tồn tại đường hầm biến đổi trong tương lai.
Hiện tại, giá trị được hỗ trợ duy nhất là 600 (10 phút).

Các tùy chọn xây dựng đường hầm là một cấu trúc Ánh xạ như được định nghĩa trong [Common](/en/docs/spec/common-structures/).
Điều này dành cho sử dụng trong tương lai. Không có tùy chọn nào hiện đang được định nghĩa.
Nếu cấu trúc Ánh xạ trống, đây là hai byte 0x00 0x00.
Kích thước tối đa của Ánh xạ (bao gồm trường chiều dài) là 296 byte,
và giá trị tối đa của trường chiều dài Ánh xạ là 294.



Bản ghi Yêu cầu Mã hóa (ECIES)
`````````````````````````````````````

Tất cả các trường đều là big-endian ngoại trừ khóa công khai tạm thời, dạng little-endian.

Kích thước mã hóa: 528 byte

  ```dataspec


bytes    0-15: Hash nhận diện của Hop bị rút ngắn
  bytes   16-47: Khóa công khai X25519 tạm thời của Người gửi
  bytes  48-511: Bản ghi Yêu cầu Xây dựng ChaCha20 đã mã hóa
  bytes 512-527: Poly1305 MAC




  ```



### Bản ghi Trả lời Xây dựng

Các bản ghi Trả lời Xây dựng đã mã hóa dài 528 byte cho cả ElGamal và ECIES, để tương thích.


Bản ghi Trả lời Không Mã hóa (ElGamal)
`````````````````````````````````````
Các trả lời ElGamal được mã hóa bằng AES.

Tất cả các trường đều là big-endian.

Kích thước không mã hóa: 528 byte

  ```dataspec


bytes   0-31: Băm SHA-256 của bytes 32-527
  bytes 32-526: dữ liệu ngẫu nhiên
  byte     527: trả lời

  tổng chiều dài: 528




  ```


Bản ghi Trả lời Không Mã hóa (ECIES)
`````````````````````````````````````
Đây là đặc tả đề xuất của bản ghi Trả lời Xây dựng Đường hầm cho các router ECIES-X25519.
Tóm tắt các thay đổi:

- Thêm Ánh xạ cho các tùy chọn trả lời xây dựng
- Bản ghi không mã hóa dài hơn vì có ít chi phí mã hóa hơn

Các trả lời ECIES được mã hóa bằng ChaCha20/Poly1305.

Tất cả các trường đều là big-endian.

Kích thước không mã hóa: 512 byte

  ```dataspec


bytes    0-x: Các tùy chọn Trả lời Xây dựng Đường hầm (Ánh xạ)
  bytes    x-x: dữ liệu khác như được ngụ ý bởi các tùy chọn
  bytes  x-510: Đệm ngẫu nhiên
  byte     511: Byte trả lời




  ```

Các tùy chọn trả lời xây dựng đường hầm là một cấu trúc Ánh xạ như được định nghĩa trong [Common](/en/docs/spec/common-structures/).
Điều này dành cho sử dụng trong tương lai. Không có tùy chọn nào hiện đang được định nghĩa.
Nếu cấu trúc Ánh xạ trống, đây là hai byte 0x00 0x00.
Kích thước tối đa của Ánh xạ (bao gồm trường chiều dài) là 511 byte,
và giá trị tối đa của trường chiều dài Ánh xạ là 509.

Byte trả lời là một trong các giá trị sau
như được định nghĩa trong [Tunnel-Creation](/en/docs/spec/tunnel-creation/) để tránh nhận diện dấu vân tay:

- 0x00 (chấp nhận)
- 30 (TUNNEL_REJECT_BANDWIDTH)


Bản ghi Trả lời Mã hóa (ECIES)
```````````````````````````````````

Kích thước mã hóa: 528 byte

  ```dataspec


bytes   0-511: Bản ghi Trả lời Xây dựng ChaCha20 đã mã hóa
  bytes 512-527: Poly1305 MAC




  ```

Sau khi hoàn tất chuyển đổi sang các bản ghi ECIES, các quy tắc đệm theo phạm vi giống như các bản ghi yêu cầu.


### Mã hóa Đối xứng của Bản ghi

Các đường hầm hỗn hợp được cho phép, và cần thiết, cho giai đoạn chuyển đổi từ ElGamal sang ECIES.
Trong suốt thời kỳ chuyển đổi, số lượng các router được khóa dưới các khóa ECIES sẽ tăng lên.

Tiền xử lý mật mã đối xứng sẽ chạy theo cách giống nhau:

- "mã hóa":

  - mã hóa chạy ở chế độ giải mã
  - các bản ghi yêu cầu được giải mã trước trong tiền xử lý (che giấu các bản ghi yêu cầu được mã hóa)

- "giải mã":

  - mã hóa chạy ở chế độ mã hóa
  - các bản ghi yêu cầu được mã hóa (hiển thị bản ghi yêu cầu ở dạng rõ) bởi các bước nhảy tham gia

- ChaCha20 không có "chế độ", vì vậy nó chỉ đơn giản chạy ba lần:

  - một lần trong tiền xử lý
  - một lần bởi bước nhảy
  - một lần trong xử lý đáp ứng cuối cùng

Khi các đường hầm hỗn hợp được sử dụng, người tạo đường hầm sẽ cần căn cứ vào mã hóa đối xứng
của Bản ghi Yêu cầu Xây dựng trên loại mã hóa của bước nhảy hiện tại và trước đó.

Mỗi bước nhảy sẽ sử dụng loại mã hóa của riêng mình để mã hóa Bản ghi Trả lời Xây dựng, và các
bản ghi khác trong Thông điệp Xây dựng Đường hầm Biến đổi (VTBM).

Trên đường trả lời, điểm cuối (người gửi) sẽ cần huỷ bỏ [Multiple-Encryption](https://en.wikipedia.org/wiki/Multiple_encryption), bằng cách sử dụng mỗi khóa trả lời của bước nhảy.

Để làm rõ, hãy xem một ví dụ về một đường hầm phát sinh với ECIES xung quanh ElGamal:

- Người gửi (OBGW) -> ElGamal (H1) -> ECIES (H2) -> ElGamal (H3)

Tất cả các Bản ghi Yêu cầu Xây dựng đều ở trạng thái mã hóa của chúng (sử dụng ElGamal hoặc ECIES).

Mã hóa AES256/CBC, khi được sử dụng, vẫn được sử dụng cho mỗi bản ghi, mà không có liên kết qua nhiều bản ghi.

Tương tự, ChaCha20 sẽ được sử dụng để mã hóa mỗi bản ghi, không chạy qua toàn bộ VTBM.

Các bản ghi yêu cầu được tiền xử lý bởi Người gửi (OBGW):

- Bản ghi H3 được "mã hóa" bằng:

  - Khóa trả lời của H2 (ChaCha20)
  - Khóa trả lời của H1 (AES256/CBC)

- Bản ghi H2 được "mã hóa" bằng:

  - Khóa trả lời của H1 (AES256/CBC)

- Bản ghi H1 sẽ được đưa ra mà không có mã hóa đối xứng

Chỉ H2 kiểm tra cờ mã hóa trả lời, và thấy rằng nó được theo sau bởi AES256/CBC.

Sau khi được xử lý bởi mỗi bước nhảy, các bản ghi ở trạng thái "giải mã":

- Bản ghi H3 được "giải mã" bằng:

  - Khóa trả lời của H3 (AES256/CBC)

- Bản ghi H2 được "giải mã" bằng:

  - Khóa trả lời của H3 (AES256/CBC)
  - Khóa trả lời của H2 (ChaCha20-Poly1305)

- Bản ghi H1 được "giải mã" bằng:

  - Khóa trả lời của H3 (AES256/CBC)
  - Khóa trả lời của H2 (ChaCha20)
  - Khóa trả lời của H1 (AES256/CBC)

Người tạo đường hầm, tức là Điểm đầu vào (IBEP), xử lý lại đáp ứng:

- Bản ghi H3 được "mã hóa" bằng:

  - Khóa trả lời của H3 (AES256/CBC)

- Bản ghi H2 được "mã hóa" bằng:

  - Khóa trả lời của H3 (AES256/CBC)
  - Khóa trả lời của H2 (ChaCha20-Poly1305)

- Bản ghi H1 được "mã hóa" bằng:

  - Khóa trả lời của H3 (AES256/CBC)
  - Khóa trả lời của H2 (ChaCha20)
  - Khóa trả lời của H1 (AES256/CBC)


### Khóa Bản ghi Yêu cầu (ECIES)

Các khóa này đã được bao gồm rõ ràng trong các Bản ghi Yêu cầu Xây dựng ElGamal.
Đối với các Bản ghi Yêu cầu Xây dựng ECIES, các khóa đường hầm và các khóa trả lời AES được bao gồm,
nhưng các khóa trả lời ChaCha được rút ra từ trao đổi DH.
Xem [Prop156](/en/proposals/156-ecies-routers/) để biết chi tiết về các khóa ECIES tĩnh của router.

Dưới đây là mô tả về cách lấy các khóa đã được truyền tải trước trong các bản ghi yêu cầu.


KDF cho ck và h ban đầu
````````````````````````

Đây là chuẩn [NOISE](https://noiseprotocol.org/noise.html) cho mẫu "N" với một tên giao thức chuẩn.

  ```text

Đây là mẫu tin nhắn "e":

  // Định nghĩa protocol_name.
  Đặt protocol_name = "Noise_N_25519_ChaChaPoly_SHA256"
  (31 byte, mã hóa US-ASCII, không có kết thúc NULL).

  // Định nghĩa Hash h = 32 byte
  // Điền để đủ 32 byte. KHÔNG băm nó, vì nó không quá 32 byte.
  h = protocol_name || 0

  Định nghĩa ck = khóa liên kết 32 byte. Sao chép dữ liệu h đến ck.
  Đặt chainKey = h

  // MixHash(null prologue)
  h = SHA256(h);

  // đến đây, có thể tất cả được tính trước bởi tất cả các router.




  ```


KDF cho Bản ghi Yêu cầu
````````````````````````

Người tạo đường hầm ElGamal tạo ra một cặp khóa X25519 tạm thời cho mỗi
bước nhảy ECIES trong đường hầm, và sử dụng sơ đồ ở trên để mã hóa Bản ghi Yêu cầu Xây dựng của họ.
Người tạo đường hầm ElGamal sẽ sử dụng sơ đồ trước đặc tả này để mã hóa với các bước nhảy ElGamal.

Người tạo đường hầm ECIES sẽ cần mã hóa với khóa công cộng của mỗi bước nhảy ElGamal sử dụng
sơ đồ được định nghĩa trong [Tunnel-Creation](/en/docs/spec/tunnel-creation/). Người tạo đường hầm ECIES sẽ sử dụng sơ đồ trên để mã hóa
với các bước nhảy ECIES.

Điều này có nghĩa là các bước nhảy đường hầm chỉ sẽ thấy các bản ghi mã hóa từ cùng loại mã hóa của họ.

Đối với người tạo đường hầm ElGamal và ECIES, họ sẽ tạo ra các cặp khóa X25519 tạm thời
độc nhất per-hop để mã hóa với các bước nhảy ECIES.

**QUAN TRỌNG**:
Các khóa tạm thời phải là duy nhất cho mỗi bước nhảy ECIES, và cho mỗi bản ghi xây dựng.
Không sử dụng các khóa duy nhất mở ra một vector tấn công cho các bước nhảy hợp tác để xác nhận rằng chúng ở trong cùng một đường hầm.


  ```dataspec


// Cặp khóa tĩnh X25519 của từng bước nhảy (hesk, hepk) từ Nhận Diện Router
  hesk = GENERATE_PRIVATE()
  hepk = DERIVE_PUBLIC(hesk)

  // MixHash(hepk)
  // || dưới đây có nghĩa là thêm vào
  h = SHA256(h || hepk);

  // đến đây, có thể tất cả được tính trước bởi từng router
  // cho tất cả các yêu cầu xây dựng đến

  // Người gửi tạo một cặp khóa X25519 tạm thời per ECIES hop trong VTBM (sesk, sepk)
  sesk = GENERATE_PRIVATE()
  sepk = DERIVE_PUBLIC(sesk)

  // MixHash(sepk)
  h = SHA256(h || sepk);

  Kết thúc mẫu tin nhắn "e".

  Đây là mẫu tin nhắn "es":

  // Noise es
  // Người gửi thực hiện một X25519 DH với khóa công khai của Hop.
  // Mỗi Hop, tìm kiếm bản ghi với hash nhận diện của họ,
  // và trích xuất khóa tạm thời của Người gửi đứng trước bản ghi được mã hóa.
  sharedSecret = DH(sesk, hepk) = DH(hesk, sepk)

  // MixKey(DH())
  //[chainKey, k] = MixKey(sharedSecret)
  // Thông số ChaChaPoly để mã hóa/giải mã
  keydata = HKDF(chainKey, sharedSecret, "", 64)
  // Lưu cho KDF Bản ghi Trả lời
  chainKey = keydata[0:31]

  // Thông số AEAD
  k = keydata[32:63]
  n = 0
  plaintext = 464 byte ghi yêu cầu xây dựng
  ad = h
  ciphertext = ENCRYPT(k, n, plaintext, ad)

  Kết thúc mẫu tin nhắn "es".

  // MixHash(ciphertext)
  // Lưu cho KDF Bản ghi Trả lời
  h = SHA256(h || ciphertext)





  ```

``replyKey``, ``layerKey`` và ``layerIV`` vẫn phải được bao gồm bên trong các bản ghi ElGamal,
và có thể được tạo ra ngẫu nhiên.


### Mã hóa Bản ghi Yêu cầu (ElGamal)

Như được định nghĩa trong [Tunnel-Creation](/en/docs/spec/tunnel-creation/).
Không có thay đổi nào đối với mã hóa cho các bước nhảy ElGamal.




### Mã hóa Bản ghi Trả lời (ECIES)

Bản ghi trả lời được mã hóa bằng ChaCha20/Poly1305.

  ```dataspec


// Thông số AEAD
  k = chainkey từ yêu cầu xây dựng
  n = 0
  plaintext = 512 byte ghi trả lời xây dựng
  ad = h từ yêu cầu xây dựng

  ciphertext = ENCRYPT(k, n, plaintext, ad)




  ```



### Mã hóa Bản ghi Trả lời (ElGamal)

Như đã định nghĩa trong [Tunnel-Creation](/en/docs/spec/tunnel-creation/).
Không có thay đổi nào đối với mã hóa cho các bước nhảy ElGamal.



### Phân Tích An Ninh

ElGamal không cung cấp bảo mật chuyển tiếp cho Tin nhắn Xây dựng Đường hầm.

AES256/CBC có trạng thái tốt hơn một chút, chỉ chịu một yếu điểm lý thuyết từ một
cuộc tấn công biclique đã biết.

Cuộc tấn công thực tế duy nhất đã biết chống lại AES256/CBC là một cuộc tấn công oracle đệm, khi IV được biết đối với kẻ tấn công.

Kẻ tấn công sẽ cần phá khóa mã hóa ElGamal của bước nhảy tiếp theo để có được thông tin khóa AES256/CBC (khóa trả lời và IV).

ElGamal có tải CPU cao đáng kể hơn so với ECIES, dẫn đến nguy cơ cạn kiệt tài nguyên.

ECIES, khi được sử dụng với các khóa tạm thời mới per-Bản ghi Yêu cầu Xây dựng hoặc Thông điệp Xây dựng Đường hầm Biến đổi, cung cấp bảo mật chuyển tiếp.

ChaCha20Poly1305 cung cấp mã hóa AEAD, cho phép người nhận xác minh tính toàn vẹn của tin nhắn trước khi cố gắng giải mã.


## Biện minh

Thiết kế này tối đa hóa tái sử dụng các khối mã hóa hiện có, giao thức, và mã.
Thiết kế này giảm thiểu rủi ro.




## Ghi chú Thực hiện

* Các router cũ không kiểm tra loại mã hóa của bước nhảy và sẽ gửi các bản ghi mã hóa ElGamal
  Một số router gần đây có lỗi và sẽ gửi các loại bản ghi lỗi. 
  Người thực hiện nên phát hiện và từ chối những bản ghi này trước hoạt động DH
  nếu có thể, để giảm tải CPU.


## Vấn đề



## Chuyển đổi

Xem [Prop156](/en/proposals/156-ecies-routers/).




## Tài liệu tham khảo

.. [Common]
    {{ spec_url('common-structures') }}

.. [Cryptography]
   {{ spec_url('cryptography') }}

.. [ECIES-X25519]
   {{ spec_url('ecies') }}

.. [I2NP]
   {{ spec_url('i2np') }}

.. [NOISE]
    https://noiseprotocol.org/noise.html

.. [NTCP2]
   {{ spec_url('ntcp2') }}

.. [Prop119]
   {{ proposal_url('119') }}

.. [Prop143]
   {{ proposal_url('143') }}

.. [Prop153]
    {{ proposal_url('153') }}

.. [Prop156]
    {{ proposal_url('156') }}

.. [Prop157]
    {{ proposal_url('157') }}

.. [SPEC]
   {{ spec_url('tunnel-creation-ecies') }}

.. [Tunnel-Creation]
   {{ spec_url('tunnel-creation') }}

.. [Multiple-Encryption]
   https://en.wikipedia.org/wiki/Multiple_encryption

.. [RFC-7539]
   https://tools.ietf.org/html/rfc7539

.. [RFC-7748]
   https://tools.ietf.org/html/rfc7748
```
