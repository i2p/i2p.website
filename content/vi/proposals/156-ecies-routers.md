---
title: "Thiết Bị Định Tuyến ECIES"
number: "156"
author: "zzz, orignal"
created: "2020-09-01"
lastupdated: "2025-03-05"
status: "Đã Đóng"
thread: "http://zzz.i2p/topics/2950"
target: "0.9.51"
toc: true
---

## Chú ý
Việc triển khai và kiểm tra mạng đang được tiến hành.
Có thể sửa đổi.
Trạng thái:

- Thiết bị định tuyến ECIES đã được triển khai từ phiên bản 0.9.48, xem [Common](/docs/specs/common-structures/).
- Tạo đường hầm đã được triển khai từ phiên bản 0.9.48, xem [Tunnel-Creation-ECIES](/docs/specs/implementation/#tunnel-creation-ecies).
- Tin nhắn mã hóa đến các thiết bị định tuyến ECIES đã được triển khai từ phiên bản 0.9.49, xem [ECIES-ROUTERS](/docs/specs/ecies/).
- Các tin nhắn xây dựng đường hầm mới đã được triển khai từ phiên bản 0.9.51.


## Tổng Quan


### Tóm Tắt

Danh tính của Thiết Bị Định Tuyến hiện tại chứa một khóa mã hóa ElGamal.
Đây đã là tiêu chuẩn từ khi I2P bắt đầu.
ElGamal chậm và cần được thay thế ở tất cả các địa điểm sử dụng.

Các đề xuất cho LS2 [Prop123](/proposals/123-new-netdb-entries/) và ECIES-X25519-AEAD-Ratchet [Prop144](/proposals/144-ecies-x25519-aead-ratchet/)
(hiện được chỉ định trong [ECIES](/docs/specs/ecies/)) đã định nghĩa việc thay thế ElGamal bằng ECIES
cho các Điểm Đến.

Đề xuất này định nghĩa việc thay thế ElGamal bằng ECIES-X25519 cho các thiết bị định tuyến.
Đề xuất này cung cấp tổng quan về các thay đổi cần thiết.
Hầu hết các chi tiết nằm trong các đề xuất và đặc tả khác.
Xem phần tham khảo để có liên kết.


### Mục Tiêu

Xem [Prop152](/proposals/152-ecies-tunnels/) để biết các mục tiêu bổ sung.

- Thay thế ElGamal bằng ECIES-X25519 trong Danh Tính Thiết Bị Định Tuyến
- Tái sử dụng các nguyên thủy mật mã hiện có
- Cải thiện bảo mật tin nhắn xây dụng đường hầm khi có thể trong khi duy trì tính tương thích
- Hỗ trợ đường hầm với các điểm ElGamal/ECIES hỗn hợp
- Tối đa tính tương thích với mạng hiện tại
- Không yêu cầu nâng cấp "ngày cờ hiệu" toàn bộ mạng
- Triển khai dần để giảm thiểu rủi ro
- Tin nhắn xây dựng đường hầm mới, nhỏ hơn


### Phi-Mục Tiêu

Xem [Prop152](/proposals/152-ecies-tunnels/) để biết các phi-mục tiêu bổ sung.

- Không yêu cầu cho các thiết bị định tuyến hai khóa
- Thay đổi lớp mã hóa, đối với điều đó xem [Prop153](/proposals/153-chacha20-layer-encryption/)


## Thiết Kế


### Vị Trí Khóa và Loại Mã Hóa

Đối với Điểm Đến, khóa nằm trong leaseset, không phải trong Điểm Đến, và
chúng tôi hỗ trợ nhiều loại mã hóa trong cùng một leaseset.

Không cần điều đó cho các thiết bị định tuyến. Khóa mã hóa của thiết bị định tuyến
nằm trong Danh Tính Thiết Bị Định Tuyến. Xem đặc tả cấu trúc chung [Common](/docs/specs/common-structures/).

Đối với thiết bị định tuyến, chúng tôi sẽ thay thế khóa ElGamal 256 byte trong Danh Tính Thiết Bị Định Tuyến
bằng một khóa X25519 32 byte và 224 byte đệm.
Điều này sẽ được chỉ định bởi loại mã hóa trong chứng nhận khóa.
Loại mã hóa (giống như được sử dụng trong LS2) là 4.
Điều này biểu thị một khóa công khai X25519 32 byte little-endian.
Đây là cấu trúc tiêu chuẩn như đã được định nghĩa trong đặc tả cấu trúc chung [Common](/docs/specs/common-structures/).

Điều này giống hệt với phương pháp được đề xuất cho ECIES-P256
cho các loại mã hóa 1-3 trong đề xuất 145 [Prop145](/proposals/145-ecies/).
Trong khi đề xuất này chưa bao giờ được thông qua, các nhà phát triển triển khai Java đã chuẩn bị cho
các loại mã hóa trong chứng chỉ khóa Danh Tính Thiết Bị Định Tuyến bằng cách thêm các kiểm tra ở nhiều
vị trí trong cơ sở mã. Hầu hết công việc này được hoàn thành vào giữa năm 2019.


### Tin Nhắn Xây Dựng Đường Hầm

Một số thay đổi đối với đặc tả tạo đường hầm [Tunnel-Creation](/docs/specs/implementation/#tunnel-creation-ecies)
được yêu cầu để sử dụng ECIES thay vì ElGamal.
Ngoài ra, chúng tôi sẽ cải thiện các tin nhắn xây dựng đường hầm
để tăng cường bảo mật.

Trong giai đoạn 1, chúng tôi sẽ thay đổi định dạng và mã hóa của
Bản Ghi Yêu Cầu Xây Dựng và Bản Ghi Phản Hồi Xây Dựng cho các điểm dừng ECIES.
Những thay đổi này sẽ tương thích với các thiết bị định tuyến ElGamal hiện có.
Những thay đổi này được định nghĩa trong kiến nghị 152 [Prop152](/proposals/152-ecies-tunnels/).

Trong giai đoạn 2, chúng tôi sẽ thêm một phiên bản mới của
Tin Nhắn Yêu Cầu Xây Dựng, Tin Nhắn Phản Hồi Xây Dựng,
Bản Ghi Yêu Cầu Xây Dựng và Bản Ghi Phản Hồi Xây Dựng.
Kích thước sẽ được giảm để tăng hiệu quả.
Các thay đổi này phải được hỗ trợ bởi tất cả các điểm dừng trong một đường hầm, và tất cả các điểm dừng phải là ECIES.
Những thay đổi này được định nghĩa trong kiến nghị 157 [Prop157](/proposals/157-new-tbm/).


### Mã Hóa Đầu Cuối

#### Lịch Sử

Trong thiết kế ban đầu của Java I2P, có một Quản Lý Khóa Phiên ElGamal (SKM) chia sẻ
giữa thiết bị định tuyến và tất cả các Điểm Đến cục bộ của nó.
Vì một SKM chia sẻ có thể tiết lộ thông tin và cho phép đối chiếu bởi kẻ tấn công,
thiết kế đã được thay đổi để hỗ trợ các SKM ElGamal riêng biệt cho thiết bị định tuyến và mỗi Điểm Đến.
Thiết kế ElGamal chỉ hỗ trợ người gửi ẩn danh;
người gửi chỉ gửi khóa tạm thời, không phải một khóa tĩnh.
Tin nhắn không bị ràng buộc với danh tính của người gửi.

Sau đó, chúng tôi đã thiết kế ECIES Ratchet SKM trong
ECIES-X25519-AEAD-Ratchet [Prop144](/proposals/144-ecies-x25519-aead-ratchet/), hiện được quy định trong [ECIES](/docs/specs/ecies/).
Thiết kế này được quy định bằng cách sử dụng mẫu "IK" của Noise, bao gồm khóa tĩnh của người gửi trong tin nhắn đầu tiên. Giao thức này được sử dụng cho các Điểm Đến ECIES (loại 4).
Mẫu IK không cho phép người gửi ẩn danh.

Do đó, chúng tôi đã bao gồm trong đề xuất một cách để gửi tin nhắn ẩn danh tới SKM Ratchet, sử dụng một khóa tĩnh rỗng. Điều này mô phỏng một mẫu "N" của Noise, nhưng theo cách tương thích, vì vậy một ECIES SKM có thể nhận cả tin nhắn ẩn danh và không ẩn danh.
Ý định là sử dụng khóa không cho các thiết bị định tuyến ECIES.


#### Trường Hợp Sử Dụng và Mô Hình Đe Dọa

Trường hợp sử dụng và mô hình đe dọa cho các tin nhắn gửi đến các thiết bị định tuyến rất khác với
đối với các tin nhắn đầu-cuối giữa các Điểm Đến.


Trường hợp sử dụng và mô hình đe dọa của Điểm Đến:

- Không ẩn danh từ/đến Điểm Đến (người gửi bao gồm khóa tĩnh)
- Hỗ trợ hiệu quả giao thông duy trì giữa các Điểm Đến (bắt tay đầy đủ, phát trực tuyến, và tags)
- Luôn được gửi thông qua đường hầm ra và vào
- Ẩn tất cả các đặc điểm nhận dạng khỏi OBEP và IBGW, yêu cầu mã hóa khóa tạm thời Elligator2.
- Cả hai bên đều phải sử dụng cùng một loại mã hóa


Trường hợp sử dụng và mô hình đe dọa của Thiết Bị Định Tuyến:

- Tin nhắn ẩn danh từ các thiết bị định tuyến hoặc các Điểm Đến (người gửi không bao gồm khóa tĩnh)
- Chỉ dành cho Tìm Kiếm và Lưu Trữ Cơ Sở Dữ Liệu được mã hóa, thường là cho floodfills
- Tin nhắn không thường xuyên
- Nhiều tin nhắn không nên được đối chiếu
- Luôn được gửi thông qua đường hầm ra trực tiếp tới một thiết bị định tuyến. Không sử dụng đường hầm vào
- OBEP biết rằng nó đang chuyển tiếp tin nhắn tới một thiết bị định tuyến và biết loại mã hóa của nó
- Hai bên có thể có các loại mã hóa khác nhau
- Phản hồi Tra Cứu Cơ Sở Dữ Liệu là những tin nhắn một lần sử dụng khóa và thẻ phản hồi trong tin nhắn Tra Cứu Cơ Sở Dữ Liệu
- Xác nhận Lưu Trữ Cơ Sở Dữ Liệu là những tin nhắn một lần sử dụng một thông điệp Trạng Thái Giao Hàng đi kèm


Phi-mục tiêu của trường hợp sử dụng Thiết Bị Định Tuyến:

- Không cần tin nhắn không ẩn danh
- Không cần gửi tin nhắn thông qua các đường hầm thăm dò vào (một thiết bị định tuyến không xuất bản leasesets thăm dò)
- Không cần giao thông tin nhắn kéo dài sử dụng tags
- Không cần chạy "quản trị khóa đôi" Quản Lý Khóa Phiên như được mô tả trong [ECIES](/docs/specs/ecies/) cho Điểm Đến. Các thiết bị định tuyến chỉ có một khóa công khai.


#### Kết Luận Thiết Kế

SKM Router ECIES không cần một SKM Ratchet đầy đủ như được quy định trong [ECIES](/docs/specs/ecies/) cho các Điểm Đến.
Không có yêu cầu cho các tin nhắn không ẩn danh sử dụng mẫu IK.
Mô hình đe dọa không yêu cầu mã hóa khóa tạm thời Elligator2.

Do đó, SKM Router sẽ sử dụng mẫu "N" của Noise, giống như được quy định
trong [Prop152](/proposals/152-ecies-tunnels/) cho việc xây dựng đường hầm.
Nó sẽ sử dụng cùng định dạng tải như được quy định cho các Điểm Đến trong [ECIES](/docs/specs/ecies/).
Chế độ khóa tĩnh rỗng (không ràng buộc hoặc phiên) mẫu IK quy định trong [ECIES](/docs/specs/ecies/) sẽ không được sử dụng.

Phản hồi các tra cứu sẽ được mã hóa với thẻ ratchet nếu được yêu cầu trong tra cứu.
Điều này được ghi nhận trong [Prop154](/proposals/154-ecies-lookups/), hiện được chỉ định trong [I2NP](/docs/specs/i2np/).

Thiết kế cho phép thiết bị định tuyến có một Quản Lý Khóa Phiên ECIES duy nhất.
Không cần chạy "quản trị khóa đôi" Quản Lý Khóa Phiên như
được mô tả trong [ECIES](/docs/specs/ecies/) cho các Điểm Đến.
Các thiết bị định tuyến chỉ có một khóa công khai.

Một thiết bị định tuyến ECIES không có khóa tĩnh ElGamal.
Thiết bị định tuyến vẫn cần một triển khai của ElGamal để xây dựng đường hầm
qua các thiết bị định tuyến ElGamal và gửi tin nhắn mã hóa tới các thiết bị định tuyến ElGamal.

Một thiết bị định tuyến ECIES CÓ THỂ yêu cầu một Quản Lý Khóa Phiên ElGamal một phần để
nhận các tin nhắn gắn thẻ ElGamal nhận được như phản hồi cho các tìm kiếm NetDB
từ các thiết bị định tuyến floodfill phiên bản trước 0.9.46, khi các thiết bị định tuyến đó không có
một triển khai của phản hồi gắn thẻ ECIES như được quy định trong [Prop152](/proposals/152-ecies-tunnels/).
Nếu không, một thiết bị định tuyến ECIES có thể không yêu cầu một phản hồi được mã hóa từ
một thiết bị định tuyến floodfill trước 0.9.46.

Điều này là tùy chọn. Quyết định có thể thay đổi trong các triển khai I2P khác nhau
và có thể phụ thuộc vào số lượng mạng đã nâng cấp lên
0.9.46 hoặc cao hơn.
Tính đến thời điểm này, khoảng 85% mạng là 0.9.46 hoặc cao hơn.


## Đặc Tả

X25519: Xem [ECIES](/docs/specs/ecies/).

Danh Tính Thiết Bị Định Tuyến và Chứng Nhận Khóa: Xem [Common](/docs/specs/common-structures/).

Việc Xây Dựng Đường Hầm: Xem [Prop152](/proposals/152-ecies-tunnels/).

Tin Nhắn Xây Dựng Đường Hầm Mới: Xem [Prop157](/proposals/157-new-tbm/).


### Mã Hóa Yêu Cầu

Mã hóa yêu cầu giống như đã được quy định trong [Tunnel-Creation-ECIES](/docs/specs/implementation/#tunnel-creation-ecies) và [Prop152](/proposals/152-ecies-tunnels/),
sử dụng mẫu "N" của Noise.

Phản hồi các tìm kiếm sẽ được mã hóa với thẻ ratchet nếu được yêu cầu trong tìm kiếm.
Tin nhắn yêu cầu Tra Cứu Cơ Sở Dữ Liệu chứa khóa phản hồi 32-byte và thẻ phản hồi 8-byte
như đã được quy định trong [I2NP](/docs/specs/i2np/) và [Prop154](/proposals/154-ecies-lookups/). Khóa và thẻ được sử dụng để mã hóa phản hồi.

Không có bộ thẻ nào được tạo ra.
Chế độ khóa tĩnh rỗng được quy định trong
ECIES-X25519-AEAD-Ratchet [Prop144](/proposals/144-ecies-x25519-aead-ratchet/) và [ECIES](/docs/specs/ecies/) sẽ không được sử dụng.
Khóa tạm thời sẽ không được mã hóa Elligator2.

Thông thường, đây sẽ là tin nhắn Phiên Mới và sẽ được gửi với một khóa tĩnh rỗng
(không có ràng buộc hoặc phiên), khi người gửi của tin nhắn là ẩn danh.


#### KDF cho ck ban đầu và h

Đây là [NOISE](https://noiseprotocol.org/noise.html) tiêu chuẩn cho mẫu "N" với một tên giao thức chuẩn.
Điều này giống như đã được quy định trong [Tunnel-Creation-ECIES](/docs/specs/implementation/#tunnel-creation-ecies) và [Prop152](/proposals/152-ecies-tunnels/) cho các tin nhắn xây dựng đường hầm.


  ```text

Đây là mẫu tin nhắn "e":

  // Định nghĩa protocol_name.
  Đặt protocol_name = "Noise_N_25519_ChaChaPoly_SHA256"
  (31 byte, mã hóa US-ASCII, không có NULL kết thúc).

  // Định nghĩa Hash h = 32 byte
  // Đệm để đủ 32 byte. KHÔNG hash nó, vì nó không dài hơn 32 byte.
  h = protocol_name || 0

  Định nghĩa ck = 32 byte chaining key. Sao chép dữ liệu h vào ck.
  Đặt chainKey = h

  // MixHash(null prologue)
  h = SHA256(h);

  // đến đây, có thể được tính trước bởi tất cả các thiết bị định tuyến.


  ```


#### KDF cho Tin Nhắn

Người tạo ra tin nhắn tạo ra một cặp khóa X25519 tạm thời cho mỗi tin nhắn.
Khóa tạm thời phải là duy nhất cho mỗi tin nhắn.
Điều này giống như đã được quy định trong [Tunnel-Creation-ECIES](/docs/specs/implementation/#tunnel-creation-ecies) và [Prop152](/proposals/152-ecies-tunnels/) cho các tin nhắn xây dựng đường hầm.


  ```dataspec


// Cặp khóa tĩnh X25519 của thiết bị định tuyến mục tiêu (hesk, hepk) từ Danh Tính Thiết Bị Định Tuyến
  hesk = GENERATE_PRIVATE()
  hepk = DERIVE_PUBLIC(hesk)

  // MixHash(hepk)
  // || dưới đây có nghĩa là nối thêm
  h = SHA256(h || hepk);

  // đến đây, có thể được tính trước bởi các thiết bị định tuyến
  // cho tất cả các tin nhắn đến

  // Người gửi tạo ra một cặp khóa tạm thời X25519
  sesk = GENERATE_PRIVATE()
  sepk = DERIVE_PUBLIC(sesk)

  // MixHash(sepk)
  h = SHA256(h || sepk);

  Kết thúc mẫu tin nhắn "e".

  Đây là mẫu tin nhắn "es":

  // Noise es
  // Người gửi thực hiện một DH X25519 với khóa công khai tĩnh của người nhận.
  // Thiết bị định tuyến mục tiêu
  // trích xuất khóa tạm thời của người gửi trước khi mã hóa bản ghi.
  sharedSecret = DH(sesk, hepk) = DH(hesk, sepk)

  // MixKey(DH())
  //[chainKey, k] = MixKey(sharedSecret)
  // Tham số ChaChaPoly để mã hóa/giải mã
  keydata = HKDF(chainKey, sharedSecret, "", 64)
  // Chain key không được sử dụng
  //chainKey = keydata[0:31]

  // Tham số AEAD
  k = keydata[32:63]
  n = 0
  plaintext = bản ghi yêu cầu xây dựng 464 byte
  ad = h
  ciphertext = ENCRYPT(k, n, plaintext, ad)

  Kết thúc mẫu tin nhắn "es".

  // MixHash(ciphertext) không bắt buộc
  //h = SHA256(h || ciphertext)


  ```


#### Tải

Tải là cùng định dạng khối như được định nghĩa trong [ECIES](/docs/specs/ecies/) và [Prop144](/proposals/144-ecies-x25519-aead-ratchet/).
Tất cả các tin nhắn phải chứa một khối DateTime để ngăn chặn việc phát lại.


### Mã Hóa Phản Hồi

Các phản hồi cho các tin nhắn Tra Cứu Cơ Sở Dữ Liệu là các tin nhắn Lưu Trữ Cơ Sở Dữ Liệu hoặc Phản Hồi Tìm Kiếm Cơ Sở Dữ Liệu.
Chúng được mã hóa như các tin nhắn Phiên Tồn Tại với
khóa phản hồi 32-byte và thẻ phản hồi 8-byte
như đã được quy định trong [I2NP](/docs/specs/i2np/) và [Prop154](/proposals/154-ecies-lookups/).

Không có phản hồi rõ ràng cho các tin nhắn Lưu Trữ Cơ Sở Dữ Liệu. Người gửi có thể đóng gói phản hồi của chính nó như một Tin Nhắn Tỏi đến chính nó, chứa một tin nhắn Trạng Thái Giao Hàng.


## Lý Do

Thiết kế này tối đa hóa việc tái sử dụng các nguyên thủy mật mã, các giao thức, và mã hiện có.

Thiết kế này tối thiểu hóa rủi ro.


## Ghi Chú Triển Khai

Các thiết bị định tuyến cũ không kiểm tra loại mã hóa của thiết bị định tuyến và sẽ gửi các bản ghi xây dựng hoặc tin nhắn netdb được ElGamal mã hóa.
Một số thiết bị định tuyến gần đây bị lỗi và sẽ gửi các loại bản ghi xây dựng bị lỗi khác nhau.
Một số thiết bị định tuyến gần đây có thể gửi tin nhắn netdb không ẩn danh (ratchet đầy đủ).
Nhà triển khai nên phát hiện và từ chối các bản ghi và tin nhắn này
càng sớm càng tốt để giảm việc sử dụng CPU.


## Vấn Đề

Đề xuất 145 [Prop145](/proposals/145-ecies/) có thể được viết lại để phần lớn tương thích với
Đề xuất 152 [Prop152](/proposals/152-ecies-tunnels/).


## Di Cư

Việc triển khai, kiểm tra, và triển khai sẽ cần một số phiên bản
và khoảng một năm. Các giai đoạn như sau. Việc phân loại
mỗi giai đoạn cho một phiên bản cụ thể sẽ được quyết định và phụ thuộc vào
tốc độ phát triển.

Chi tiết của việc triển khai và di cư có thể thay đổi cho
mỗi triển khai I2P.


### Kết Nối Cơ Bản Điểm-Tới-Điểm

Các thiết bị định tuyến ECIES có thể kết nối và nhận kết nối từ các thiết bị định tuyến ElGamal.
Điều này nên có thể ngay bây giờ, vì nhiều kiểm tra đã được thêm vào cơ sở mã Java
vào giữa năm 2019 để phản ứng với đề xuất 145 [Prop145](/proposals/145-ecies/) không hoàn thành.
Đảm bảo không có gì trong cơ sở mã ngăn kết nối điểm-tới-điểm với các thiết bị định tuyến không phải ElGamal.

Kiểm tra đúng mã:

- Đảm bảo rằng các thiết bị định tuyến ElGamal không yêu cầu các phản hồi mã hóa AEAD cho tin nhắn Tra Cứu Cơ Sở Dữ Liệu
  (khi phản hồi quay lại qua một đường hầm thăm dò đến thiết bị định tuyến)
- Đảm bảo rằng các thiết bị định tuyến ECIES không yêu cầu các phản hồi mã hóa AES cho tin nhắn Tra Cứu Cơ Sở Dữ Liệu
  (khi phản hồi quay lại qua một đường hầm thăm dò đến thiết bị định tuyến)

Cho đến khi các giai đoạn sau, khi các đặc tả và triển khai hoàn thành:

- Đảm bảo rằng việc xây dựng đường hầm không được thử bởi các thiết bị định tuyến ElGamal qua các thiết bị định tuyến ECIES.
- Đảm bảo rằng các tin nhắn ElGamal mã hóa không được gửi bởi các thiết bị định tuyến ElGamal tới các thiết bị định tuyến floodfill ECIES.
  (Tra Cứu Cơ Sở Dữ Liệu và Lưu Trữ Cơ Sở Dữ Liệu)
- Đảm bảo rằng các tin nhắn ECIES mã hóa không được gửi bởi các thiết bị định tuyến ECIES tới các thiết bị định tuyến floodfill ElGamal.
  (Tra Cứu Cơ Sở Dữ Liệu và Lưu Trữ Cơ Sở Dữ Liệu)
- Đảm bảo rằng các thiết bị định tuyến ECIES không tự động trở thành floodfill.

Không cần thay đổi.
Phiên bản mục tiêu, nếu thay đổi cần thiết: 0.9.48


### Tương Thích NetDB

Đảm bảo rằng thông tin thiết bị định tuyến ECIES có thể được lưu trữ và truy xuất từ các thiết bị định tuyến floodfill ElGamal.
Điều này nên có thể ngay bây giờ, vì nhiều kiểm tra đã được thêm vào cơ sở mã Java
vào giữa năm 2019 để phản ứng với đề xuất 145 [Prop145](/proposals/145-ecies/) không hoàn thành.
Đảm bảo không có gì trong cơ sở mã ngăn lưu trữ thông tin thiết bị định tuyến phi-ElGamal trong cơ sở dữ liệu mạng.

Không cần thay đổi.
Phiên bản mục tiêu, nếu thay đổi cần thiết: 0.9.48


### Việc Xây Dựng Đường Hầm

Thực hiện xây dựng đường hầm như được định nghĩa trong đề xuất 152 [Prop152](/proposals/152-ecies-tunnels/).
Bắt đầu với việc một thiết bị định tuyến ECIES xây dựng đường hầm với tất cả các điểm ElGamal;
sử dụng bản ghi yêu cầu xây dựng của riêng nó cho một đường hầm vào để kiểm tra và debug.

Sau đó, kiểm tra và hỗ trợ việc các thiết bị định tuyến ECIES xây dựng đường hầm với hỗn hợp
các điểm ElGamal và ECIES.

Sau đó, cho phép việc xây dựng đường hầm qua các thiết bị định tuyến ECIES.
Không cần kiểm tra phiên bản tối thiểu trừ khi có những thay đổi không tương thích
với đề xuất 152 sau một phiên bản phát hành.

Phiên bản mục tiêu: 0.9.48, cuối 2020


### Tin nhắn Ratchet tới floodfills ECIES

Thực hiện và kiểm tra nhận các tin nhắn ECIES (với khóa tĩnh rỗng) bởi các floodfills ECIES,
như được định nghĩa trong đề xuất 144 [Prop144](/proposals/144-ecies-x25519-aead-ratchet/).
Thực hiện và kiểm tra nhận các phản hồi AEAD cho tin nhắn Tra Cứu Cơ Sở Dữ Liệu bởi các thiết bị định tuyến ECIES.

Kích hoạt tự động floodfill bởi các thiết bị định tuyến ECIES.
Sau đó, cho phép gửi các tin nhắn ECIES tới các thiết bị định tuyến ECIES.
Không cần kiểm tra phiên bản tối thiểu trừ khi có những thay đổi không tương thích
với đề xuất 152 sau một phiên bản phát hành.

Phiên bản mục tiêu: 0.9.49, đầu 2021.
Các thiết bị định tuyến ECIES có thể tự động trở thành floodfill.


### Đặt lại khóa và Cài đặt Mới

Cài đặt mới sẽ mặc định ECIES kể từ phiên bản 0.9.49.

Dần dần đặt lại khóa tất cả các thiết bị định tuyến để giảm thiểu rủi ro và gián đoạn trong mạng.
Sử dụng mã hiện có đã thực hiện việc đặt lại khóa cho di chuyển loại chữ ký cách đây vài năm.
Mã này cho mỗi thiết bị định tuyến một cơ hội ngẫu nhiên nhỏ để đặt lại khóa mỗi khi khởi động lại.
Sau vài lần khởi động lại, một thiết bị định tuyến có thể sẽ đặt lại khóa sang ECIES.

Tiêu chí cho việc bắt đầu đặt lại khóa là một phần nhất định của mạng,
có lẽ là 50%, có thể xây dựng đường hầm qua các thiết bị định tuyến ECIES (0.9.48 trở lên).

Trước khi tích cực đặt lại khóa toàn bộ mạng, phần lớn
(có lẽ 90% trở lên) phải có khả năng xây dựng đường hầm qua các thiết bị định tuyến ECIES (0.9.48 trở lên)
VÀ gửi tin nhắn tới các floodfill ECIES (0.9.49 trở lên).
Mục tiêu này có thể sẽ đạt được cho phiên bản 0.9.52.

Đặt lại khóa sẽ mất vài phiên bản.

Phiên bản mục tiêu:
0.9.49 cho các thiết bị định tuyến mới mặc định ECIES;
0.9.49 sẽ bắt đầu đặt lại khóa từ từ;
0.9.50 - 0.9.52 sẽ liên tục tăng tốc độ đặt lại khóa;
cuối 2021 cho phần lớn mạng để được đặt lại khóa.


### Tin Nhắn Xây Dựng Đường Hầm Mới (Giai Đoạn 2)

Thực hiện và kiểm tra Tin Nhắn Xây Dựng Đường Hầm mới như được định nghĩa trong đề xuất 157 [Prop157](/proposals/157-new-tbm/).
Triển khai hỗ trợ trong phiên bản 0.9.51.
Làm thêm kiểm tra, sau đó kích hoạt trong phiên bản 0.9.52.

Kiểm tra sẽ khó khăn.
Trước khi điều này có thể được thử nghiệm rộng rãi, một phần tốt của mạng phải hỗ trợ nó.
Trước khi nó thực sự hữu dụng, phải có một đa số mạng hỗ trợ nó.
Nếu cần thay đổi đặc tả hoặc triển khai sau khi thử nghiệm,
điều đó sẽ trì hoãn việc triển khai thêm một phiên bản.

Phiên bản mục tiêu: 0.9.52, cuối 2021.


### Đặt Lại Khóa Hoàn Tất

Tại thời điểm này, các thiết bị định tuyến cũ hơn một phiên bản cụ thể TBD sẽ
không thể xây dựng đường hầm qua hầu hết các điểm đồng đẳng.

Phiên bản mục tiêu: 0.9.53, đầu 2022.


## Tham Khảo

* [Common](/docs/specs/common-structures/)
* [ECIES](/docs/specs/ecies/)
* [ECIES-ROUTERS](/docs/specs/ecies/)
* [I2NP](/docs/specs/i2np/)
* [NOISE](https://noiseprotocol.org/noise.html)
* [Prop123](/proposals/123-new-netdb-entries/)
* [Prop144](/proposals/144-ecies-x25519-aead-ratchet/)
* [Prop145](/proposals/145-ecies/)
* [Prop152](/proposals/152-ecies-tunnels/)
* [Prop153](/proposals/153-chacha20-layer-encryption/)
* [Prop154](/proposals/154-ecies-lookups/)
* [Prop157](/proposals/157-new-tbm/)
* [Tunnel-Creation](/docs/specs/implementation/#tunnel-creation-ecies)
* [Tunnel-Creation-ECIES](/docs/specs/implementation/#tunnel-creation-ecies)
