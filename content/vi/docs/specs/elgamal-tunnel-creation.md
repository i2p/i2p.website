---
title: "Đặc tả Tạo Tunnel (ElGamal)"
description: "Đặc tả xây dựng tunnel dựa trên ElGamal cũ, đã được thay thế bằng X25519"
slug: "elgamal-tunnel-creation"
aliases:
  - "/vi/tunnel-alt-creation"
  - "/vi/tunnel-alt-creation/"
lastUpdated: "2025-05"
accurateFor: "0.9.66"
---

## Tổng quan {#tunnelcreate-overview}

LƯU Ý: ĐÃ LỖI THỜI - Đây là đặc tả xây dựng tunnel ElGamal. Xem [đặc tả xây dựng tunnel X25519](/docs/specs/tunnel-creation-ecies) cho phương pháp hiện tại.

Tài liệu này chỉ định chi tiết của các thông điệp tunnel build được mã hóa sử dụng để tạo tunnel bằng phương pháp "non-interactive telescoping". Xem tài liệu tunnel build [TUNNEL-IMPL](/docs/specs/tunnel-implementation) để có cái nhìn tổng quan về quy trình, bao gồm các phương pháp lựa chọn và sắp xếp peer.

Việc tạo tunnel được thực hiện bằng một tin nhắn duy nhất được truyền qua đường dẫn các peer trong tunnel, được viết lại tại chỗ và truyền ngược về người tạo tunnel. Tin nhắn tunnel đơn lẻ này được tạo thành từ một số lượng bản ghi biến thiên (tối đa 8) - một bản ghi cho mỗi peer tiềm năng trong tunnel. Các bản ghi riêng lẻ được mã hóa bất đối xứng (ElGamal [CRYPTO-ELG](/docs/specs/cryptography#elgamal)) để chỉ có thể được đọc bởi một peer cụ thể dọc theo đường dẫn, trong khi một lớp mã hóa đối xứng bổ sung (AES [CRYPTO-AES](/docs/specs/cryptography#AES)) được thêm vào tại mỗi hop để chỉ lộ bản ghi được mã hóa bất đối xứng vào đúng thời điểm thích hợp.

### Số lượng bản ghi {#number}

Không phải tất cả các bản ghi đều phải chứa dữ liệu hợp lệ. Ví dụ, thông điệp xây dựng cho một tunnel 3-hop có thể chứa nhiều bản ghi hơn để che giấu chiều dài thực tế của tunnel khỏi các thành viên tham gia. Có hai loại thông điệp xây dựng. Tunnel Build Message ([TBM](/docs/specs/i2np#msg-tunnelbuild)) ban đầu chứa 8 bản ghi, điều này đã quá đủ cho bất kỳ chiều dài tunnel thực tế nào. Variable Tunnel Build Message ([VTBM](/docs/specs/i2np#msg-variabletunnelbuild)) mới hơn chứa từ 1 đến 8 bản ghi. Người khởi tạo có thể đánh đổi giữa kích thước thông điệp với mức độ che giấu chiều dài tunnel mong muốn.

Trong mạng hiện tại, hầu hết các tunnel có độ dài 2 hoặc 3 hop. Triển khai hiện tại sử dụng VTBM 5 bản ghi để xây dựng tunnel có 4 hop trở xuống, và TBM 8 bản ghi cho các tunnel dài hơn. VTBM 5 bản ghi (khi được phân mảnh, vừa khít trong ba tunnel message 1KB) giúp giảm lưu lượng mạng và tăng tỷ lệ thành công khi xây dựng, vì các thông điệp nhỏ hơn ít có khả năng bị loại bỏ hơn.

Thông điệp trả lời phải có cùng loại và độ dài với thông điệp xây dựng.

### Đặc tả Bản ghi Yêu cầu {#tunnelcreate-requestrecord}

Cũng được quy định trong Đặc tả I2NP [BRR](/docs/specs/i2np#struct-buildrequestrecord).

Văn bản rõ của bản ghi, chỉ hiển thị cho hop được hỏi:

```
bytes     0-3: tunnel ID to receive messages as, nonzero
bytes    4-35: local router identity hash
bytes   36-39: next tunnel ID, nonzero
bytes   40-71: next router identity hash
bytes  72-103: AES-256 tunnel layer key
bytes 104-135: AES-256 tunnel IV key
bytes 136-167: AES-256 reply key
bytes 168-183: AES-256 reply IV
byte      184: flags
bytes 185-188: request time (in hours since the epoch, rounded down)
bytes 189-192: next message ID
bytes 193-221: uninterpreted / random padding
```
Các trường tunnel ID tiếp theo và băm định danh router tiếp theo được sử dụng để chỉ định hop tiếp theo trong tunnel, tuy nhiên đối với điểm cuối tunnel outbound, chúng chỉ định nơi thông điệp phản hồi tạo tunnel đã được viết lại sẽ được gửi đến. Ngoài ra, message ID tiếp theo chỉ định message ID mà thông điệp (hoặc phản hồi) sẽ sử dụng.

Khóa lớp tunnel, khóa tunnel IV, khóa phản hồi, và IV phản hồi đều là các giá trị ngẫu nhiên 32 byte được tạo ra bởi người khởi tạo, chỉ để sử dụng trong bản ghi yêu cầu xây dựng này.

Trường flags chứa các thông tin sau:

```
Bit order: 76543210 (bit 7 is MSB)
bit 7: if set, allow messages from anyone
bit 6: if set, allow messages to anyone, and send the reply to the
       specified next hop in a Tunnel Build Reply Message
bits 5-0: Undefined, must set to 0 for compatibility with future options
```
Bit 7 cho biết hop sẽ là một inbound gateway (IBGW). Bit 6 cho biết hop sẽ là một outbound endpoint (OBEP). Nếu không có bit nào được thiết lập, hop sẽ là một intermediate participant. Cả hai không thể được thiết lập cùng lúc.

#### Tạo Bản Ghi Yêu Cầu

Mỗi hop nhận một Tunnel ID ngẫu nhiên, khác không. Các Tunnel ID của hop hiện tại và hop tiếp theo được điền vào. Mỗi bản ghi nhận một tunnel IV key ngẫu nhiên, reply IV, layer key, và reply key.

#### Mã hóa Bản ghi Yêu cầu {#encryption}

Bản ghi văn bản rõ đó được mã hóa ElGamal 2048 [CRYPTO-ELG](/docs/specs/cryptography#elgamal) với khóa mã hóa công khai của hop và được định dạng thành một bản ghi 528 byte:

```
bytes   0-15: First 16 bytes of the SHA-256 of the current hop's router identity
bytes 16-527: ElGamal-2048 encrypted request record
```
Trong bản ghi mã hóa 512-byte, dữ liệu ElGamal chứa các byte 1-256 và 258-513 của khối mã hóa ElGamal 514-byte [CRYPTO-ELG](/docs/specs/cryptography#elgamal). Hai byte đệm từ khối (các byte không tại vị trí 0 và 257) được loại bỏ.

Vì cleartext sử dụng toàn bộ trường, không cần thêm padding nào ngoài `SHA256(cleartext) + cleartext`.

Mỗi bản ghi 528-byte sau đó được mã hóa lặp đi lặp lại (sử dụng giải mã AES, với reply key và reply IV cho mỗi hop) để danh tính router chỉ hiển thị dưới dạng cleartext cho hop đang xét.

### Xử lý và Mã hóa Hop {#tunnelcreate-hopprocessing}

Khi một hop nhận được TunnelBuildMessage, nó sẽ tìm kiếm qua các bản ghi chứa trong đó để tìm một bản ghi bắt đầu bằng identity hash của chính nó (được cắt ngắn xuống 16 byte). Sau đó nó giải mã khối ElGamal từ bản ghi đó và lấy ra cleartext được bảo vệ. Tại thời điểm đó, chúng đảm bảo yêu cầu tunnel không phải là bản sao bằng cách đưa khóa phản hồi AES-256 vào bộ lọc Bloom. Các bản sao hoặc yêu cầu không hợp lệ sẽ bị loại bỏ. Các bản ghi không được đóng dấu với giờ hiện tại, hoặc giờ trước đó nếu ngay sau đầu giờ, phải được loại bỏ. Ví dụ, lấy giờ trong timestamp, chuyển đổi thành thời gian đầy đủ, sau đó nếu nó chậm hơn 65 phút hoặc sớm hơn 5 phút so với thời gian hiện tại, thì nó không hợp lệ. Bộ lọc Bloom phải có thời lượng ít nhất một giờ (cộng thêm vài phút để cho phép sai lệch đồng hồ), để các bản ghi trùng lặp trong giờ hiện tại không bị từ chối bởi việc kiểm tra timestamp giờ trong bản ghi, sẽ bị từ chối bởi bộ lọc.

Sau khi quyết định có đồng ý tham gia vào tunnel hay không, họ thay thế bản ghi đã chứa yêu cầu bằng một khối trả lời được mã hóa. Tất cả các bản ghi khác đều được mã hóa AES-256 [CRYPTO-AES](/docs/specs/cryptography#AES) với reply key và IV đi kèm. Mỗi bản ghi được mã hóa AES/CBC riêng biệt với cùng reply key và reply IV. Chế độ CBC không được tiếp tục (liên kết) qua các bản ghi.

Mỗi hop chỉ biết phản hồi của chính nó. Nếu nó đồng ý, nó sẽ duy trì tunnel cho đến khi hết hạn, ngay cả khi tunnel đó sẽ không được sử dụng, vì nó không thể biết liệu tất cả các hop khác có đồng ý hay không.

#### Đặc tả Bản ghi Phản hồi {#tunnelcreate-replyrecord}

Sau khi hop hiện tại đọc bản ghi của họ, họ thay thế nó bằng một bản ghi phản hồi cho biết liệu họ có đồng ý tham gia vào tunnel hay không, và nếu không, họ phân loại lý do từ chối. Đây đơn giản là một giá trị 1 byte, với 0x0 có nghĩa là họ đồng ý tham gia vào tunnel, và các giá trị cao hơn có nghĩa là mức độ từ chối cao hơn.

Các mã từ chối sau đây được định nghĩa:

- TUNNEL_REJECT_PROBABALISTIC_REJECT = 10
- TUNNEL_REJECT_TRANSIENT_OVERLOAD = 20
- TUNNEL_REJECT_BANDWIDTH = 30
- TUNNEL_REJECT_CRIT = 50

Để ẩn các nguyên nhân khác, chẳng hạn như tắt router, khỏi các peer, triển khai hiện tại sử dụng TUNNEL_REJECT_BANDWIDTH cho hầu hết tất cả các từ chối.

Phản hồi được mã hóa bằng khóa phiên AES được gửi đến nó trong khối mã hóa, được đệm thêm 495 byte dữ liệu ngẫu nhiên để đạt kích thước bản ghi đầy đủ. Phần đệm được đặt trước byte trạng thái:

```
AES-256-CBC(SHA-256(padding+status) + padding + status, key, IV)

bytes   0-31 : SHA-256 of bytes 32-527
bytes 32-526 : Random padding
byte 527     : Reply value
```
Điều này cũng được mô tả trong đặc tả I2NP [BRR](/docs/specs/i2np#struct-buildrequestrecord).

### Chuẩn bị Thông điệp Xây dựng Tunnel {#tunnelcreate-requestpreparation}

Khi xây dựng một Tunnel Build Message mới, tất cả các Build Request Records phải được xây dựng trước và mã hóa bất đối xứng bằng ElGamal [CRYPTO-ELG](/docs/specs/cryptography#elgamal). Mỗi bản ghi sau đó được giải mã sớm với các reply keys và IVs của các hop trước đó trong đường dẫn, sử dụng AES [CRYPTO-AES](/docs/specs/cryptography#AES). Việc giải mã đó nên được chạy theo thứ tự ngược lại để dữ liệu được mã hóa bất đối xứng sẽ xuất hiện rõ ràng tại hop phù hợp sau khi hop trước đó mã hóa nó.

Các bản ghi dư thừa không cần thiết cho các yêu cầu riêng lẻ sẽ được người tạo đơn giản là điền bằng dữ liệu ngẫu nhiên.

### Gửi Thông Điệp Xây Dựng Tunnel {#tunnelcreate-requestdelivery}

Đối với các outbound tunnel, việc giao hàng được thực hiện trực tiếp từ người tạo tunnel đến hop đầu tiên, đóng gói TunnelBuildMessage như thể người tạo chỉ là một hop khác trong tunnel. Đối với các inbound tunnel, việc giao hàng được thực hiện thông qua một outbound tunnel hiện có. Outbound tunnel thường là từ cùng một pool với tunnel mới đang được xây dựng. Nếu không có outbound tunnel nào khả dụng trong pool đó, một outbound exploratory tunnel sẽ được sử dụng. Khi khởi động, khi chưa có outbound exploratory tunnel nào tồn tại, một fake 0-hop outbound tunnel sẽ được sử dụng.

### Xử Lý Điểm Cuối Thông Điệp Xây Dựng Tunnel {#tunnelcreate-endpointhandling}

Đối với việc tạo một tunnel outbound, khi yêu cầu đến một endpoint outbound (được xác định bởi cờ 'allow messages to anyone'), hop được xử lý như thường lệ, mã hóa một phản hồi thay cho bản ghi và mã hóa tất cả các bản ghi khác, nhưng vì không có 'next hop' để chuyển tiếp TunnelBuildMessage đến, thay vào đó nó đặt các bản ghi phản hồi đã mã hóa vào một TunnelBuildReplyMessage ([TBRM](/docs/specs/i2np#msg-tunnelbuildreply)) hoặc VariableTunnelBuildReplyMessage ([VTBRM](/docs/specs/i2np#msg-variabletunnelbuildreply)) (loại thông điệp và số lượng bản ghi phải khớp với yêu cầu) và gửi nó đến reply tunnel được chỉ định trong bản ghi yêu cầu. Reply tunnel đó chuyển tiếp Tunnel Build Reply Message trở lại cho người tạo tunnel, giống như với bất kỳ thông điệp nào khác [TUNNEL-OP](/docs/specs/tunnel-implementation#tunnel.operation). Người tạo tunnel sau đó xử lý nó, như được mô tả bên dưới.

Reply tunnel được người tạo chọn như sau: Thông thường đó là một tunnel đến từ cùng pool với outbound tunnel mới đang được xây dựng. Nếu không có inbound tunnel nào khả dụng trong pool đó, một inbound exploratory tunnel sẽ được sử dụng. Khi khởi động, khi chưa có inbound exploratory tunnel nào tồn tại, một fake 0-hop inbound tunnel sẽ được sử dụng.

Để tạo một inbound tunnel, khi yêu cầu đến inbound endpoint (còn được gọi là tunnel creator), không cần tạo ra một Tunnel Build Reply Message rõ ràng, và router xử lý từng phản hồi như bên dưới.

### Xử lý Thông điệp Phản hồi Xây dựng Tunnel {#tunnelcreate-replyprocessing}

Để xử lý các bản ghi phản hồi, người tạo chỉ cần giải mã AES từng bản ghi riêng lẻ, sử dụng khóa phản hồi và IV của mỗi hop trong tunnel sau peer đó (theo thứ tự ngược lại). Điều này sẽ lộ ra phản hồi chỉ định xem họ có đồng ý tham gia vào tunnel hay tại sao họ từ chối. Nếu tất cả đều đồng ý, tunnel được coi là đã tạo thành công và có thể được sử dụng ngay lập tức, nhưng nếu có ai từ chối, tunnel sẽ bị loại bỏ.

Các thỏa thuận và từ chối được ghi nhận trong hồ sơ của mỗi peer [PEER-SELECTION](/docs/overview/peer-selection), để sử dụng trong các đánh giá tương lai về khả năng tunnel của peer.

## Lịch sử và Ghi chú {#tunnelcreate-notes}

Chiến lược này được đưa ra trong một cuộc thảo luận trên danh sách thư I2P giữa Michael Rogers, Matthew Toseland (toad), và jrandom về cuộc tấn công tiền nhiệm. Xem [TUNBUILD-SUMMARY](http://zzz.i2p/archive/2005-10/msg00138.html), [TUNBUILD-REASONING](http://zzz.i2p/archive/2005-10/msg00129.html). Nó được giới thiệu trong bản phát hành 0.6.1.10 vào ngày 16/02/2006, đây là lần cuối cùng một thay đổi không tương thích ngược được thực hiện trong I2P.

Ghi chú:

- Thiết kế này không ngăn cản hai peer thù địch trong cùng một tunnel đánh dấu một hoặc nhiều bản ghi yêu cầu hoặc phản hồi để phát hiện rằng chúng đang trong cùng một tunnel, nhưng việc làm như vậy có thể bị phát hiện bởi người tạo tunnel khi đọc phản hồi, khiến tunnel bị đánh dấu là không hợp lệ.

- Thiết kế này không bao gồm proof of work trên phần mã hóa bất đối xứng, mặc dù identity hash 16 byte có thể được cắt đôi với phần sau được thay thế bằng hàm hashcash với chi phí lên đến 2^64.

- Thiết kế này một mình không ngăn chặn được hai peer thù địch trong cùng một tunnel sử dụng thông tin thời gian để xác định xem họ có đang ở trong cùng một tunnel hay không. Việc sử dụng phương pháp giao hàng yêu cầu theo lô và đồng bộ có thể giúp ích (gom các yêu cầu thành lô và gửi chúng vào phút được đồng bộ ntp). Tuy nhiên, làm như vậy cho phép các peer 'gắn thẻ' các yêu cầu bằng cách làm chậm chúng và phát hiện độ trễ sau đó trong tunnel, mặc dù có lẽ việc loại bỏ các yêu cầu không được giao trong một khoảng thời gian nhỏ có thể hiệu quả (mặc dù làm điều đó sẽ yêu cầu mức độ đồng bộ đồng hồ cao). Thay vào đó, có lẽ các hop riêng lẻ có thể thêm vào một độ trễ ngẫu nhiên trước khi chuyển tiếp yêu cầu?

- Có phương thức nào không gây lỗi fatal để gắn thẻ cho yêu cầu không?

- Dấu thời gian với độ phân giải một giờ được sử dụng để ngăn chặn tấn công replay. Ràng buộc này không được thực thi cho đến phiên bản 0.9.16.

## Công việc tương lai {#future}

- Trong triển khai hiện tại, originator để trống một bản ghi cho chính nó. Do đó một thông điệp có n bản ghi chỉ có thể xây dựng một tunnel với n-1 hop. Điều này có vẻ cần thiết đối với inbound tunnel (nơi hop gần cuối có thể thấy hash prefix cho hop tiếp theo), nhưng không cần thiết đối với outbound tunnel. Điều này cần được nghiên cứu và xác minh. Nếu có thể sử dụng bản ghi còn lại mà không làm giảm tính ẩn danh, chúng ta nên làm như vậy.

- Phân tích sâu hơn về các cuộc tấn công gắn thẻ và định thời gian có thể xảy ra được mô tả trong các ghi chú trên.

- Chỉ sử dụng VTBM; không chọn các peer cũ không hỗ trợ nó.

- Build Request Record không chỉ định thời gian sống hoặc thời điểm hết hạn của tunnel;
  mỗi hop sẽ làm cho tunnel hết hạn sau 10 phút, đây là một hằng số được mã hóa cứng
  trên toàn mạng. Chúng ta có thể sử dụng một bit trong trường flag và lấy 4 (hoặc 8)
  byte từ phần padding để chỉ định thời gian sống hoặc thời điểm hết hạn. Người yêu cầu
  chỉ nên chỉ định tùy chọn này nếu tất cả các bên tham gia đều hỗ trợ nó.

## Tài liệu tham khảo {#ref}

- [BRR](/docs/specs/i2np#struct-buildrequestrecord) - Build Request Record
- [CRYPTO-AES](/docs/specs/cryptography#AES) - AES Encryption
- [CRYPTO-ELG](/docs/specs/cryptography#elgamal) - ElGamal Encryption
- [HASHING-IT-OUT](http://www-users.cs.umn.edu/~hopper/hashing_it_out.pdf) - Hashing It Out Paper
- [PEER-SELECTION](/docs/overview/peer-selection) - Peer Selection
- [PREDECESSOR](http://forensics.umass.edu/pubs/wright-tissec.pdf) - Predecessor Attack Paper
- [PREDECESSOR-2008](http://forensics.umass.edu/pubs/wright.tissec.2008.pdf) - Predecessor Attack Paper (2008)
- [TBM](/docs/specs/i2np#msg-tunnelbuild) - Tunnel Build Message
- [TBRM](/docs/specs/i2np#msg-tunnelbuildreply) - Tunnel Build Reply Message
- [TUNBUILD-REASONING](http://zzz.i2p/archive/2005-10/msg00129.html) - Tunnel Build Reasoning
- [TUNBUILD-SUMMARY](http://zzz.i2p/archive/2005-10/msg00138.html) - Tunnel Build Summary
- [TUNNEL-IMPL](/docs/specs/tunnel-implementation) - Tunnel Implementation
- [TUNNEL-OP](/docs/specs/tunnel-implementation#tunnel.operation) - Tunnel Operation
- [VTBM](/docs/specs/i2np#msg-variabletunnelbuild) - Variable Tunnel Build Message
- [VTBRM](/docs/specs/i2np#msg-variabletunnelbuildreply) - Variable Tunnel Build Reply Message
