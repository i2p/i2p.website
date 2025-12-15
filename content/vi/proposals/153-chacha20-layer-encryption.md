---
title: "Mã hóa Tầng Đường Hầm ChaCha"
number: "153"
author: "chisana"
created: "2019-08-04"
lastupdated: "2019-08-05"
status: "Open"
thread: "http://zzz.i2p/topics/2753"
toc: true
---

## Tổng Quan

Đề xuất này được xây dựng dựa trên và yêu cầu các thay đổi từ đề xuất 152: Đường Hầm ECIES.

Chỉ những đường hầm được xây dựng qua các điểm tiếp nhận hỗ trợ định dạng BuildRequestRecord cho đường hầm ECIES-X25519
mới có thể thực hiện đề xuất này.

Đề xuất này yêu cầu định dạng Tùy Chọn Dựng Đường Hầm để chỉ định
loại mã hóa tầng đường hầm, và truyền tải các khóa lớp AEAD.

### Mục Tiêu

Các mục tiêu của đề xuất này là:

- Thay thế AES256/ECB+CBC bằng ChaCha20 cho mã hóa tầng và IV đường hầm đã thiết lập
- Sử dụng ChaCha20-Poly1305 để bảo vệ AEAD giữa các hop
- Không thể bị phát hiện từ mã hóa tầng đường hầm hiện có bởi những người không tham gia đường hầm
- Không thay đổi độ dài thông điệp đường hầm tổng thể

### Xử Lý Thông Điệp Đường Hầm Đã Thiết Lập

Phần này mô tả những thay đổi đối với:

- Tiền xử lý + mã hóa Cổng ra và Cổng vào
- Mã hóa + xử lý sau của người tham gia
- Mã hóa + xử lý sau Endpoint ra và vào

Để có cái nhìn tổng quan về xử lý thông điệp đường hầm hiện tại, hãy xem phần [Tunnel Implementation](/docs/tunnels/implementation/).

Chỉ những thay đổi cho các bộ định tuyến hỗ trợ mã hóa tầng ChaCha20 được thảo luận.

Không có thay đổi nào được xem xét đối với đường hầm kết hợp với mã hóa tầng AES, cho đến khi có thể đưa ra một giao thức an toàn
để chuyển đổi một IV AES 128 bit thành nonce ChaCha20 64 bit. Bộ lọc Bloom đảm bảo tính duy nhất
cho IV đầy đủ, nhưng nửa đầu của các IV duy nhất có thể giống nhau.

Điều này có nghĩa là mã hóa lớp phải đồng nhất cho tất cả các hop trong đường hầm, và được thiết lập
sử dụng các tùy chọn dựng đường hầm trong quá trình tạo đường hầm.

Tất cả các cổng và người tham gia đường hầm sẽ cần duy trì một bộ lọc Bloom để xác thực hai nonce độc lập.

``nonceKey`` được đề cập xuyên suốt đề xuất này thay thế cho ``IVKey`` được sử dụng trong mã hóa tầng AES.
Nó được tạo ra bằng cách sử dụng cùng KDF từ đề xuất 152.

### Mã Hóa AEAD của Thông Điệp Giữa Các Hop

Trong mỗi cặp các hop liên tiếp, sẽ cần tạo thêm một ``AEADKey`` duy nhất.
Khóa này sẽ được sử dụng bởi các hop liên tiếp để mã hóa và giải mã ChaCha20-Poly1305
thông điệp đường hầm được mã hóa bên trong ChaCha20.

Thông điệp đường hầm sẽ cần giảm chiều dài khung mã hóa bên trong xuống 16 byte để
để dành chỗ cho MAC Poly1305.

AEAD không thể được sử dụng trực tiếp trên các thông điệp, vì cần giải mã lặp lại bởi các đường hầm đầu ra.
Giải mã lặp lại chỉ có thể đạt được, theo cách nó được sử dụng hiện nay, sử dụng ChaCha20 mà không có AEAD.

```text
+----+----+----+----+----+----+----+----+
  |    Tunnel ID      |   tunnelNonce     |
  +----+----+----+----+----+----+----+----+
  | tunnelNonce cont. |    obfsNonce      |
  +----+----+----+----+----+----+----+----+
  |  obfsNonce cont.  |                   |
  +----+----+----+----+                   +
  |                                       |
  +           Encrypted Data              +
  ~                                       ~
  |                                       |
  +                   +----+----+----+----+
  |                   |    Poly1305 MAC   |
  +----+----+----+----+                   +  
  |                                       |
  +                   +----+----+----+----+
  |                   |
  +----+----+----+----+

  Tunnel ID :: `TunnelId`
         4 bytes
         ID của hop tiếp theo

  tunnelNonce ::
         8 bytes
         nonce của tầng đường hầm

  obfsNonce ::
         8 bytes
         nonce mã hóa tầng nonce đường hầm

  Encrypted Data ::
         992 bytes
         thông điệp đường hầm đã được mã hóa

  Poly1305 MAC ::
         16 bytes

  tổng kích thước: 1028 Bytes
```

Các hop bên trong (với hop liền trước và liền sau), sẽ có hai ``AEADKeys``, một để giải mã
tầng AEAD của hop trước, và mã hóa tầng AEAD cho hop tiếp theo.

Tất cả người tham gia hop bên trong sẽ có thêm 64 byte tài liệu khóa được bao gồm trong BuildRequestRecords của họ.

Điểm cuối ra và cổng vào chỉ yêu cầu thêm 32 byte dữ liệu khóa, 
vì họ không mã hóa tầng đường hầm truyền tải thông điệp giữa nhau.

Cổng ra tạo khóa của nó là ``outAEAD``, giống như khóa ``inAEAD`` của hop đầu ra đầu tiên.

Điểm cuối vào tạo khóa ``inAEAD`` của nó, giống như khóa ``outAEAD`` của hop vào cuối cùng.

Các hop bên trong sẽ nhận được và ``inAEADKey`` và ``outAEADKey`` sẽ được sử dụng để AEAD giải mã
thông điệp nhận được và mã hóa thông điệp gửi đi một cách tương ứng.

Lấy một ví dụ, trong một đường hầm với các hop bên trong là OBGW, A, B, OBEP:

- ``inAEADKey`` của A giống như ``outAEADKey`` của OBGW
- ``inAEADKey`` của B giống như ``outAEADKey`` của A
- ``outAEADKey`` của B giống như ``inAEADKey`` của OBEP

Các khóa chỉ là duy nhất cho các cặp hop, vì thế ``inAEADKey`` của OBEP sẽ khác so với ``inAEADKey`` của A,
``outAEADKey`` của A khác với ``outAEADKey`` của B, v.v.

### Xử Lý Thông Điệp của Cổng và Người Tạo Đường Hầm

Các cổng sẽ phân mảnh và gói thông điệp theo cách tương tự, giữ lại không gian sau khung hướng dẫn-phân mảnh
cho MAC Poly1305.

Các thông điệp I2NP bên trong chứa các khung AEAD (bao gồm cả MAC) có thể được tách ra theo các mảnh phân đoạn,
nhưng bất kỳ mảnh phân đoạn bị mất nào sẽ dẫn đến thất bại giải mã AEAD (xác nhận MAC bị thất bại) tại
điểm cuối.

### Tiền Xử Lý & Mã Hóa Cổng

Khi đường hầm hỗ trợ mã hóa tầng ChaCha20, cổng sẽ tạo ra hai nonce 64-bit cho mỗi bộ thông điệp.

Đường hầm vào:

- Mã hóa IV và thông điệp đường hầm bằng ChaCha20
- Sử dụng ``tunnelNonce`` và ``obfsNonce`` 8-byte vì tuổi thọ của các đường hầm
- Sử dụng ``obfsNonce`` 8-byte để mã hóa ``tunnelNonce``
- Phá hủy đường hầm trước khi có 2^(64 - 1) - 1 bộ thông điệp: 2^63 - 1 = 9,223,372,036,854,775,807

  - Giới hạn nonce được đặt ra để tránh chạm trán của 64-bit nonces
  - Giới hạn nonce gần như không thể nào bị đạt tới, vì điều này sẽ là trên ~15,372,286,728,091,294 thông điệp/giây cho các đường hầm 10 phút

- Điều chỉnh số lượng bộ lọc Bloom dựa trên số lượng phần tử mong đợi hợp lý (128 thông điệp/giây, 1024 thông điệp/giây? TBD)

Cổng Vào của đường hầm (IBGW), xử lý các thông điệp nhận được từ điểm cuối ra (OBEP) của một đường hầm khác.

Tại điểm này, tầng thông điệp bên ngoài được mã hóa bằng mã hóa truyền tải điểm-điểm.
Các tiêu đề thông điệp I2NP có thể nhìn thấy, ở tầng đường hầm, đối với OBEP và IBGW.
Các thông điệp I2NP bên trong được bao bọc trong Garlic cloves, mã hóa bằng mã hóa phiên end-to-end.

IBGW tiền xử lý các thông điệp thành các thông điệp đường hầm được định dạng thích hợp, và mã hóa như sau:

```text

// IBGW tạo nonce ngẫu nhiên, đảm bảo không vướng vào bộ lọc Bloom của nó cho mỗi nonce
  tunnelNonce = Random(len = 64-bits)
  obfsNonce = Random(len = 64-bits)
  // IBGW ChaCha20 "mã hóa" từng thông điệp đường hầm đã được tiền xử lý với tunnelNonce và layerKey của nó
  encMsg = ChaCha20(msg = thông điệp đường hầm, nonce = tunnelNonce, key = layerKey)

  // ChaCha20-Poly1305 mã hóa từng khung dữ liệu mã hóa của thông điệp với tunnelNonce và outAEADKey
  (encMsg, MAC) = ChaCha20-Poly1305-Encrypt(msg = encMsg, nonce = tunnelNonce, key = outAEADKey)
```

Định dạng thông điệp đường hầm sẽ thay đổi nhẹ, sử dụng hai nonce 8-byte thay vì IV 16-byte.
``obfsNonce`` được sử dụng để mã hóa nonce sẽ được đính kèm với ``tunnelNonce`` 8-byte,
và được mã hóa bởi mỗi hop sử dụng ``tunnelNonce`` đã được mã hóa và ``nonceKey`` của hop.

Sau khi tập hợp thông điệp đã được giải mã trước cho mỗi hop, Cổng Ra
ChaCha20-Poly1305 AEAD mã hóa phần văn bản mã hóa của mỗi thông điệp đường hầm bằng
``tunnelNonce`` và ``outAEADKey`` của nó.

Đường hầm ra:

- Giải mã lặp lại thông điệp đường hầm
- ChaCha20-Poly1305 mã hóa các khung dữ liệu thông điệp đường hầm đã được giải mã trước
- Sử dụng các quy tắc giống nhau cho các nonce class như đường hầm vào
- Tạo nonce ngẫu nhiên một lần cho mỗi tập hợp thông điệp đường hầm gửi đi

```text


// Đối với mỗi tập hợp thông điệp, tạo nonce ngẫu nhiên, duy nhất
  tunnelNonce = Random(len = 64-bits)
  obfsNonce = Random(len = 64-bits)

  // Đối với mỗi hop, ChaCha20 nonce đường hầm trước đó với khóa IV của hop hiện tại
  tunnelNonce = ChaCha20(msg = prev. tunnelNonce, nonce = obfsNonce, key = hop's nonceKey)

  // Đối với mỗi hop, ChaCha20 "giải mã" thông điệp đường hầm với nonce đường hầm hiện tại và layerKey của hop
  decMsg = ChaCha20(msg = thông điệp đường hầm, nonce = tunnelNonce, key = hop's layerKey)

  // Đối với mỗi hop, ChaCha20 "giải mã" obfsNonce với tunnelNonce đã được mã hóa hiện tại và nonceKey của hop
  obfsNonce = ChaCha20(msg = obfsNonce, nonce = tunnelNonce, key = hop's nonceKey)

  // Sau khi xử lý hop, ChaCha20-Poly1305 mã hóa khung dữ liệu "đã giải mã" của từng thông điệp đường hầm với tunnelNonce đã được mã hóa của hop đầu tiên và inAEADKey của nó / GW outAEADKey
  (encMsg, MAC) = ChaCha20-Poly1305-Encrypt(msg = decMsg, nonce = first hop's encrypted tunnelNonce, key = first hop's inAEADKey / GW outAEADKey)
```

### Xử Lý Người Tham Gia

Người tham gia sẽ theo dõi các thông điệp đã nhìn thấy theo cùng cách, sử dụng các bộ lọc Bloom giảm dần.

Các nonce đường hầm sẽ cần phải được mã hóa một lần cho mỗi hop, để ngăn chặn các cuộc tấn công xác nhận
bởi các hop không kế tiếp.

Các hop sẽ mã hóa nonce nhận được để ngăn chặn các cuộc tấn công xác nhận giữa các hop trước và sau,
tức là các hop không kế tiếp, kiểu tiếp tay. 

Để xác thực ``tunnelNonce`` và ``obfsNonce`` nhận được, người tham gia kiểm tra từng nonce một cách riêng biệt
đối với bộ lọc Bloom của họ để tìm các bản sao.

Sau khi xác thực, người tham gia:

- ChaCha20-Poly1305 giải mã mỗi khung dữ liệu AEAD của thông điệp đường hầm với ``tunnelNonce`` nhận được và ``inAEADKey`` của nó
- ChaCha20 mã hóa ``tunnelNonce`` với ``nonceKey`` nhận được và ``obfsNonce``
- ChaCha20 mã hóa khung dữ liệu mã hóa của mỗi thông điệp đường hầm với ``tunnelNonce`` và ``layerKey`` được mã hóa của nó
- ChaCha20-Poly1305 mã hóa khung dữ liệu đã mã hóa của mỗi thông điệp đường hầm với ``tunnelNonce`` và ``outAEADKey`` đã được mã hóa của nó 
- ChaCha20 mã hóa ``obfsNonce`` với ``nonceKey`` của nó và ``tunnelNonce`` đã được mã hóa
- Gửi cặp {``nextTunnelId``, mã hóa (``tunnelNonce`` || ``obfsNonce``), AEAD ciphertext || MAC} tới hop tiếp theo.

```text

// Để xác minh, các hop phải kiểm tra bộ lọc Bloom để xác nhận sự duy nhất của mỗi nonce nhận được
  // Sau khi xác minh, mở khung AEAD bằng cách ChaCha20-Poly1305 giải mã từng khung dữ liệu đã mã hóa
  // với tunnelNonce nhận được và inAEADKey 
  encTunMsg = ChaCha20-Poly1305-Decrypt(msg = nhận encMsg \|\| MAC, nonce = nhận tunnelNonce, key = inAEADKey)

  // ChaCha20 mã hóa tunnelNonce với obfsNonce và nonceKey của hop
  tunnelNonce = ChaCha20(msg = nhận tunnelNonce, nonce = nhận obfsNonce, key = nonceKey)

  // ChaCha20 mã hóa khung dữ liệu mã hóa của mỗi thông điệp đường hầm với tunnelNonce đã được mã hóa và layerKey của hop
  encMsg = ChaCha20(msg = encTunMsg, nonce = tunnelNonce, key = layerKey)

  // Để bảo vệ AEAD, cũng ChaCha20-Poly1305 mã hóa khung dữ liệu mã hóa của mỗi thông điệp
  // với tunnelNonce đã được mã hóa và outAEADKey của hop
  (encMsg, MAC) = ChaCha20-Poly1305-Encrypt(msg = encMsg, nonce = tunnelNonce, key = outAEADKey)

  // ChaCha20 mã hóa obfsNonce nhận được với tunnelNonce đã được mã hóa và nonceKey của hop
  obfsNonce = ChaCha20(msg = obfsNonce, nonce = tunnelNonce, key = nonceKey)
```

### Xử Lý Endpoint Vào

Đối với các đường hầm ChaCha20, sơ đồ sau sẽ được sử dụng để giải mã từng thông điệp đường hầm:

- Xác thực ``tunnelNonce`` và ``obfsNonce`` nhận được một cách độc lập với bộ lọc Bloom của nó
- ChaCha20-Poly1305 giải mã khung dữ liệu mã hóa bằng ``tunnelNonce`` nhận được và ``inAEADKey``
- ChaCha20 giải mã khung dữ liệu mã hóa bằng ``tunnelNonce`` nhận được & ``layerKey`` của hop
- ChaCha20 giải mã ``obfsNonce`` sử dụng ``nonceKey`` của hop và ``tunnelNonce`` nhận được để có được ``obfsNonce`` liền trước
- ChaCha20 giải mã ``tunnelNonce`` nhận được sử dụng ``nonceKey`` của hop và ``obfsNonce`` đã được giải mã để có được ``tunnelNonce`` liền trước
- ChaCha20 giải mã dữ liệu đã mã hóa sử dụng ``tunnelNonce`` đã được giải mã & ``layerKey`` của hop liền trước
- Lặp lại các bước cho việc giải mã nonce và giải mã tầng cho từng hop trong đường hầm, trở lại IBGW
- Giải mã khung AEAD chỉ cần trong vòng đầu tiên

```text

// Đối với vòng đầu tiên, ChaCha20-Poly1305 giải mã khung dữ liệu mã hóa của từng thông điệp + MAC
  // sử dụng tunnelNonce nhận được và inAEADKey
  msg = encTunMsg \|\| MAC
  tunnelNonce = nhận tunnelNonce
  encTunMsg = ChaCha20-Poly1305-Decrypt(msg, nonce = tunnelNonce, key = inAEADKey)

  // Lặp lại cho từng hop trong đường hầm trở lại IBGW
  // Đối với mỗi vòng, ChaCha20 giải mã từng mã hóa tầng của hop trên khung dữ liệu mã hóa của từng thông điệp
  // Thay thế tunnelNonce nhận được bằng tunnelNonce đã được giải mã của vòng trước cho mỗi hop
  decMsg = ChaCha20(msg = encTunMsg, nonce = tunnelNonce, key = layerKey)
  obfsNonce = ChaCha20(msg = obfsNonce, nonce = tunnelNonce, key = nonceKey)
  tunnelNonce = ChaCha20(msg = tunnelNonce, nonce = obfsNonce, key = nonceKey)
```

### Phân Tích An Ninh cho Mã Hóa Tầng Đường Hầm ChaCha20+ChaCha20-Poly1305

Chuyển từ AES256/ECB+AES256/CBC sang ChaCha20+ChaCha20-Poly1305 có một số ưu điểm, và những cân nhắc về an ninh mới.

Cân nhắc về an ninh quan trọng nhất cần phải xem xét, đó là nonce ChaCha20 và ChaCha20-Poly1305 phải là duy nhất cho mỗi thông điệp,
trong suốt vòng đời của khóa đang được sử dụng.

Không sử dụng nonce duy nhất với cùng khóa trên các thông điệp khác nhau sẽ phá vỡ ChaCha20 và ChaCha20-Poly1305.

Sử dụng một ``obfsNonce`` đính kèm cho phép IBEP giải mã ``tunnelNonce`` cho mã hóa tầng của từng hop,
phục hồi nonce trước đó.

``obfsNonce`` cùng với ``tunnelNonce`` không cung cấp thông tin mới nào cho các hop của đường hầm,
vì ``obfsNonce`` được mã hóa bằng cách sử dụng ``tunnelNonce`` đã được mã hóa. Điều này cũng cho phép IBEP phục hồi
``obfsNonce`` trước đó theo cách tương tự với phục hồi ``tunnelNonce``.

Ưu điểm an ninh lớn nhất là không có các cuộc tấn công xác nhận hoặc oracle chống lại ChaCha20,
và việc sử dụng ChaCha20-Poly1305 giữa các hop thêm bảo vệ AEAD chống lại việc giả mạo ciphertext bởi
các kẻ tấn công MitM ngoài luồng.

Có những cuộc tấn công oracle thực tế chống lại AES256/ECB + AES256/CBC, khi khóa được tái sử dụng (như trong mã hóa tầng đường hầm).

Các cuộc tấn công oracle chống lại AES256/ECB sẽ không hoạt động, bởi vì việc mã hóa kép được sử dụng, và mã hóa
là trên một khối duy nhất (IV đường hầm).

Các cuộc tấn công oracle padding chống lại AES256/CBC sẽ không hoạt động, vì không có padding được sử dụng. Nếu độ dài thông điệp đường hầm
bao giờ thay đổi thành không-mod-16 độ dài, AES256/CBC vẫn sẽ không bị tổn thương do các IV trùng lập bị từ chối.

Cả hai cuộc tấn công cũng đều bị chặn bởi việc không cho phép nhiều cuộc gọi oracle sử dụng cùng IV, bởi các IV trùng lập bị từ chối.

## Tài Liệu Tham Khảo

* [Tunnel-Implementation](/docs/tunnels/implementation/)
