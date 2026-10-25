---
title: "Triển khai Tunnel"
description: "Đặc tả về hoạt động tunnel I2P, xây dựng và xử lý thông điệp"
slug: "tunnel-implementation"
aliases:
  - "/vi/docs/specs/implementation"
  - "/vi/docs/specs/implementation/"
lastUpdated: "2019-07"
accurateFor: "0.9.41"
---

Trang này ghi lại việc triển khai tunnel hiện tại.

## Tổng quan về Tunnel {#tunnel.overview}

Trong I2P, các thông điệp được truyền theo một hướng qua một tunnel ảo gồm các peer, sử dụng bất kỳ phương tiện nào có sẵn để chuyển thông điệp đến hop tiếp theo. Các thông điệp đến tại *gateway* của tunnel, được đóng gói và/hoặc phân mảnh thành các tunnel message có kích thước cố định, và được chuyển tiếp đến hop tiếp theo trong tunnel, nơi xử lý và xác minh tính hợp lệ của thông điệp rồi gửi đến hop tiếp theo, và cứ thế tiếp tục, cho đến khi đến được tunnel endpoint. *Endpoint* đó nhận các thông điệp đã được đóng gói bởi gateway và chuyển tiếp chúng theo hướng dẫn - hoặc đến một router khác, đến một tunnel khác trên một router khác, hoặc xử lý cục bộ.

Các tunnel đều hoạt động giống nhau, nhưng có thể được phân thành hai nhóm khác nhau - inbound tunnels và outbound tunnels. Các inbound tunnel có một gateway không đáng tin cậy chuyển các thông điệp xuống về phía người tạo tunnel, đóng vai trò là điểm cuối của tunnel. Đối với outbound tunnels, người tạo tunnel đóng vai trò là gateway, chuyển các thông điệp ra điểm cuối từ xa.

Người tạo tunnel sẽ chọn chính xác những peer nào sẽ tham gia vào tunnel, và cung cấp cho mỗi peer dữ liệu cấu hình cần thiết. Chúng có thể có bất kỳ số lượng hop nào. Mục đích là làm cho cả những người tham gia và các bên thứ ba khó có thể xác định độ dài của một tunnel, hoặc thậm chí khó để những người tham gia thông đồng có thể xác định xem họ có phải là một phần của cùng một tunnel hay không (trừ trường hợp những peer thông đồng nằm cạnh nhau trong tunnel).

Trong thực tế, một chuỗi các tunnel pool được sử dụng cho các mục đích khác nhau - mỗi đích client cục bộ có bộ inbound tunnel và outbound tunnel riêng, được cấu hình để đáp ứng nhu cầu về tính ẩn danh và hiệu suất. Ngoài ra, router tự nó duy trì một chuỗi các pool để tham gia vào network database và để quản lý các tunnel.

I2P về bản chất là một mạng chuyển mạch gói, ngay cả với các tunnel này, cho phép nó tận dụng nhiều tunnel chạy song song, tăng khả năng phục hồi và cân bằng tải. Bên ngoài lớp I2P cốt lõi, có một thư viện streaming đầu cuối đến đầu cuối tùy chọn có sẵn cho các ứng dụng client, cung cấp hoạt động giống TCP, bao gồm sắp xếp lại thông điệp, truyền lại, kiểm soát tắc nghẽn, v.v.

Tổng quan về thuật ngữ tunnel I2P có [trên trang tổng quan tunnel](/docs/overview/tunnel-routing).

## Hoạt động Tunnel (Xử lý Thông điệp) {#tunnel.operation}

### Tổng quan

Sau khi một tunnel được xây dựng, [các tin nhắn I2NP](/docs/specs/i2np) sẽ được xử lý và truyền qua nó. Hoạt động của tunnel có bốn quy trình riêng biệt, được thực hiện bởi các peer khác nhau trong tunnel.

1. Đầu tiên, tunnel gateway tích lũy một số
   thông điệp I2NP và tiền xử lý chúng thành các tunnel message để
   gửi đi.
2. Tiếp theo, gateway đó mã hóa dữ liệu đã được tiền xử lý, sau đó
   chuyển tiếp nó đến hop đầu tiên.
3. Peer đó, và các tunnel
   participant tiếp theo, mở một lớp mã hóa, xác minh rằng nó không
   phải là bản sao, sau đó chuyển tiếp nó đến peer tiếp theo.
4. Cuối cùng, các tunnel message đến endpoint nơi các thông điệp I2NP
   ban đầu được đóng gói bởi gateway được tái lắp ráp và chuyển tiếp theo
   yêu cầu.

Các thành viên tunnel trung gian không biết họ đang ở trong inbound tunnel hay outbound tunnel; họ luôn "mã hóa" cho hop tiếp theo. Do đó, chúng ta tận dụng mã hóa AES đối xứng để "giải mã" tại gateway của outbound tunnel, sao cho bản rõ được tiết lộ tại điểm cuối outbound.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Role</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Preprocessing</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Encryption Operation</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Postprocessing</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Outbound Gateway (Creator)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Fragment, Batch, and Pad</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Iteratively encrypt (using decryption operations)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Forward to next hop</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Participant</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Decrypt (using an encryption operation)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Forward to next hop</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Outbound Endpoint</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Decrypt (using an encryption operation) to reveal plaintext tunnel message</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reassemble Fragments, Forward as instructed to Inbound Gateway or Router</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;" colspan="4"></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Inbound Gateway</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Fragment, Batch, and Pad</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Encrypt</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Forward to next hop</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Participant</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Encrypt</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Forward to next hop</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Inbound Endpoint (Creator)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Iteratively decrypt to reveal plaintext tunnel message</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reassemble Fragments, Receive data</td>
    </tr>
  </tbody>
</table>
### Xử lý Gateway {#tunnel.gateway}

#### Tiền Xử Lý Thông Điệp {#tunnel.preprocessing}

Chức năng của tunnel gateway là phân mảnh và đóng gói [thông điệp I2NP](/docs/specs/i2np) thành [thông điệp tunnel](/docs/specs/tunnel-message) có kích thước cố định và mã hóa các thông điệp tunnel. Thông điệp tunnel chứa những thông tin sau:

- Một Tunnel ID 4 byte
- Một IV (initialization vector - vector khởi tạo) 16 byte
- Một checksum
- Padding, nếu cần thiết
- Một hoặc nhiều cặp { hướng dẫn giao hàng, fragment tin nhắn I2NP }

Tunnel ID là các số 4 byte được sử dụng tại mỗi hop - những người tham gia biết tunnel ID nào để lắng nghe các thông điệp và tunnel ID nào họ nên chuyển tiếp đến hop tiếp theo, và mỗi hop chọn tunnel ID mà họ nhận thông điệp trên đó. Các tunnel có thời gian sống ngắn (10 phút). Ngay cả khi các tunnel tiếp theo được xây dựng bằng cách sử dụng cùng một chuỗi peer, tunnel ID của mỗi hop sẽ thay đổi.

Để ngăn chặn kẻ thù đánh dấu các thông điệp dọc theo đường truyền bằng cách điều chỉnh kích thước thông điệp, tất cả các thông điệp tunnel đều có kích thước cố định 1024 byte. Để phù hợp với các thông điệp I2NP lớn hơn cũng như hỗ trợ các thông điệp nhỏ hơn một cách hiệu quả hơn, gateway phân chia các thông điệp I2NP lớn hơn thành các mảnh được chứa trong mỗi thông điệp tunnel. Endpoint sẽ cố gắng xây dựng lại thông điệp I2NP từ các mảnh trong một khoảng thời gian ngắn, nhưng sẽ loại bỏ chúng khi cần thiết.

Chi tiết được trình bày trong [đặc tả thông điệp tunnel](/docs/specs/tunnel-message).

### Mã hóa Gateway

Sau khi tiền xử lý các thông điệp thành payload có padding, gateway tạo một giá trị IV ngẫu nhiên 16 byte, mã hóa lặp lại nó và thông điệp tunnel khi cần thiết, và chuyển tiếp bộ tuple {tunnelID, IV, thông điệp tunnel được mã hóa} đến hop tiếp theo.

Cách thức mã hóa tại gateway được thực hiện tùy thuộc vào việc tunnel là inbound hay outbound tunnel. Đối với inbound tunnel, chúng chỉ đơn giản chọn một IV ngẫu nhiên, xử lý hậu kỳ và cập nhật nó để tạo ra IV cho gateway và sử dụng IV đó cùng với layer key của riêng chúng để mã hóa dữ liệu đã được tiền xử lý. Đối với outbound tunnel, chúng phải giải mã lặp đi lặp lại IV (chưa được mã hóa) và dữ liệu đã tiền xử lý với IV và layer key cho tất cả các hop trong tunnel. Kết quả của việc mã hóa outbound tunnel là khi mỗi peer mã hóa nó, endpoint sẽ khôi phục lại dữ liệu tiền xử lý ban đầu.

### Xử lý Người tham gia {#tunnel.participant}

Khi một peer nhận được tunnel message, nó kiểm tra xem thông điệp có đến từ cùng một previous hop như trước đó không (được khởi tạo khi thông điệp đầu tiên đi qua tunnel). Nếu peer trước đó là một router khác, hoặc nếu thông điệp đã được thấy trước đó, thông điệp sẽ bị loại bỏ. Sau đó participant mã hóa IV nhận được bằng AES256/ECB sử dụng IV key của họ để xác định IV hiện tại, sử dụng IV đó với layer key của participant để mã hóa dữ liệu, mã hóa IV hiện tại bằng AES256/ECB sử dụng IV key của họ một lần nữa, rồi chuyển tiếp tuple {nextTunnelId, nextIV, encryptedData} đến hop tiếp theo. Việc mã hóa kép IV này (cả trước và sau khi sử dụng) giúp giải quyết một lớp tấn công xác nhận nhất định.

Phát hiện tin nhắn trùng lặp được xử lý bằng bộ lọc Bloom suy giảm trên các IV tin nhắn. Mỗi router duy trì một bộ lọc Bloom duy nhất để chứa phép XOR của IV và khối đầu tiên của tin nhắn nhận được cho tất cả các tunnel mà nó đang tham gia, được sửa đổi để loại bỏ các mục đã thấy sau 10-20 phút (khi các tunnel sẽ hết hạn). Kích thước của bộ lọc bloom và các tham số được sử dụng đủ để bão hòa hơn kết nối mạng của router với khả năng dương tính giả không đáng kể. Giá trị duy nhất được đưa vào bộ lọc Bloom là phép XOR của IV và khối đầu tiên để ngăn các peer thông đồng không tuần tự trong tunnel đánh dấu tin nhắn bằng cách gửi lại nó với IV và khối đầu tiên được hoán đổi.

### Xử lý Điểm cuối {#tunnel.endpoint}

Sau khi nhận và xác thực một thông điệp tunnel tại hop cuối cùng trong tunnel, cách mà endpoint khôi phục dữ liệu được mã hóa bởi gateway phụ thuộc vào việc tunnel đó là inbound tunnel hay outbound tunnel. Đối với outbound tunnel, endpoint mã hóa thông điệp bằng layer key của nó giống như bất kỳ participant nào khác, để lộ dữ liệu đã được tiền xử lý. Đối với inbound tunnel, endpoint cũng là người tạo tunnel nên họ chỉ cần giải mã lặp lại IV và thông điệp, sử dụng layer key và IV key của từng bước theo thứ tự ngược lại.

Tại thời điểm này, điểm cuối tunnel có dữ liệu đã được xử lý trước được gửi bởi gateway, sau đó có thể phân tích thành các thông điệp I2NP bao gồm bên trong và chuyển tiếp chúng theo yêu cầu trong hướng dẫn giao hàng của chúng.

## Tunnel Building {#tunnel.building}

Khi xây dựng một tunnel, người tạo phải gửi một yêu cầu với dữ liệu cấu hình cần thiết đến từng hop và đợi tất cả chúng đồng ý trước khi kích hoạt tunnel. Các yêu cầu được mã hóa để chỉ những peer cần biết một phần thông tin (như tunnel layer hoặc khóa IV) mới có dữ liệu đó. Ngoài ra, chỉ người tạo tunnel mới có quyền truy cập vào phản hồi của peer. Có ba khía cạnh quan trọng cần ghi nhớ khi tạo các tunnel: những peer nào được sử dụng (và ở đâu), các yêu cầu được gửi như thế nào (và phản hồi được nhận), và cách chúng được duy trì.

### Lựa chọn Peer {#tunnel.peerselection}

Ngoài hai loại tunnel - inbound và outbound - còn có hai phong cách lựa chọn peer được sử dụng cho các tunnel khác nhau - exploratory và client. Exploratory tunnel được sử dụng cho cả việc bảo trì network database và bảo trì tunnel, trong khi client tunnel được sử dụng cho các tin nhắn client đầu cuối.

#### Lựa chọn Peer cho Tunnel Thăm dò {#tunnel.selection.exploratory}

Các tunnel khám phá được xây dựng từ một lựa chọn ngẫu nhiên các peer từ một tập con của mạng lưới. Tập con cụ thể thay đổi tùy theo router cục bộ và nhu cầu định tuyến tunnel của chúng. Nói chung, các tunnel khám phá được xây dựng từ các peer được chọn ngẫu nhiên thuộc danh mục profile "không lỗi nhưng hoạt động" của peer đó. Mục đích thứ hai của các tunnel, ngoài việc chỉ định tuyến tunnel, là tìm ra các peer có dung lượng cao nhưng chưa được sử dụng hết để có thể được thăng cấp để sử dụng trong các client tunnel.

Việc lựa chọn peer khám phá được thảo luận thêm trên [trang Profiling và Lựa chọn Peer](/docs/overview/peer-selection).

#### Lựa chọn Peer cho Client Tunnel {#tunnel.selection.client}

Các tunnel khách hàng được xây dựng với một bộ yêu cầu nghiêm ngặt hơn - router cục bộ sẽ chọn các peer từ danh mục hồ sơ "nhanh và dung lượng cao" để hiệu suất và độ tin cậy đáp ứng nhu cầu của ứng dụng khách hàng. Tuy nhiên, có một số chi tiết quan trọng ngoài việc lựa chọn cơ bản đó cần được tuân thủ, tùy thuộc vào nhu cầu ẩn danh của khách hàng.

Việc lựa chọn client peer được thảo luận thêm trong [trang Profiling và Lựa chọn Peer](/docs/overview/peer-selection).

#### Sắp xếp Peer trong Tunnel {#ordering}

Các peer được sắp xếp thứ tự trong tunnel để đối phó với [cuộc tấn công predecessor](http://forensics.umass.edu/pubs/wright-tissec.pdf) ([cập nhật năm 2008](http://forensics.umass.edu/pubs/wright.tissec.2008.pdf)).

Để ngăn chặn cuộc tấn công predecessor, việc lựa chọn tunnel giữ các peer được chọn theo một thứ tự nghiêm ngặt - nếu A, B, và C nằm trong một tunnel cho một tunnel pool cụ thể, hop sau A luôn luôn là B, và hop sau B luôn luôn là C.

Việc sắp xếp được thực hiện bằng cách tạo một khóa ngẫu nhiên 32-byte cho mỗi tunnel pool khi khởi động. Các peer không thể đoán được thứ tự sắp xếp, vì nếu không thì kẻ tấn công có thể tạo ra hai router hash ở xa nhau để tối đa hóa cơ hội được ở cả hai đầu của tunnel. Các peer được sắp xếp theo khoảng cách XOR của SHA256 Hash của (hash của peer được nối với khóa ngẫu nhiên) từ khóa ngẫu nhiên:

```
      p = peer hash
      k = random key
      d = XOR(H(p+k), k)
```
Vì mỗi tunnel pool sử dụng một khóa ngẫu nhiên khác nhau, thứ tự sắp xếp là nhất quán trong cùng một pool nhưng không nhất quán giữa các pool khác nhau. Các khóa mới được tạo ra mỗi khi router khởi động lại.

### Giao Nhận Yêu Cầu {#tunnel.request}

Một tunnel đa-chặng được xây dựng bằng cách sử dụng một thông điệp xây dựng duy nhất được giải mã và chuyển tiếp liên tục. Theo thuật ngữ của [Hashing it out in Public](http://www-users.cs.umn.edu/~hopper/hashing_it_out.pdf), đây là việc xây dựng tunnel kính thiên văn "không tương tác".

Phương pháp chuẩn bị, gửi yêu cầu và phản hồi tunnel này được [thiết kế](/docs/specs/tunnel-creation) để giảm số lượng các nút tiền nhiệm bị lộ, cắt giảm số lượng tin nhắn được truyền, xác minh kết nối phù hợp, và tránh cuộc tấn công đếm tin nhắn của phương pháp tạo tunnel viễn thị truyền thống. (Phương pháp này, gửi tin nhắn để mở rộng tunnel thông qua phần đã được thiết lập của tunnel, được gọi là xây dựng tunnel viễn thị "tương tác" trong bài viết "Hashing it out".)

Chi tiết về các thông điệp yêu cầu và phản hồi tunnel, cùng với việc mã hóa chúng, [được chỉ định tại đây](/docs/specs/tunnel-creation).

Các peer có thể từ chối yêu cầu tạo tunnel vì nhiều lý do khác nhau, tuy nhiên có một chuỗi bốn mức độ từ chối ngày càng nghiêm trọng được biết đến: từ chối xác suất (do đang tiến gần đến dung lượng của router, hoặc để phản ứng với một lượng lớn yêu cầu), quá tải tạm thời, quá tải băng thông, và lỗi nghiêm trọng. Khi nhận được, bốn loại này được bên tạo tunnel diễn giải để giúp điều chỉnh hồ sơ của router được đề cập.

Để biết thêm thông tin về profiling peer, xem [trang Peer Profiling và Lựa chọn](/docs/overview/peer-selection).

### Tunnel Pools {#tunnel.pooling}

Để cho phép hoạt động hiệu quả, router duy trì một loạt các tunnel pool, mỗi pool quản lý một nhóm tunnel được sử dụng cho một mục đích cụ thể với cấu hình riêng của chúng. Khi cần một tunnel cho mục đích đó, router sẽ chọn ngẫu nhiên một tunnel từ pool thích hợp. Nhìn chung, có hai exploratory tunnel pool - một inbound và một outbound - mỗi pool sử dụng cấu hình mặc định của router. Ngoài ra, có một cặp pool cho mỗi destination cục bộ - một inbound và một outbound tunnel pool. Những pool này sử dụng cấu hình được chỉ định khi destination cục bộ kết nối với router thông qua [I2CP](/docs/specs/i2cp), hoặc các giá trị mặc định của router nếu không được chỉ định.

Mỗi pool trong cấu hình của nó có một vài cài đặt quan trọng, xác định số lượng tunnel cần giữ hoạt động, số lượng tunnel dự phòng cần duy trì trong trường hợp lỗi, độ dài của các tunnel, liệu các độ dài đó có nên được ngẫu nhiên hóa hay không, cũng như bất kỳ cài đặt nào khác được phép khi cấu hình các tunnel riêng lẻ. Các tùy chọn cấu hình được chỉ định trên [trang I2CP](/docs/specs/i2cp).

### Độ dài Tunnel và Mặc định {#length}

[Trên trang tổng quan về tunnel](/docs/overview/tunnel-routing#length).

### Chiến lược Xây dựng Dự báo và Ưu tiên {#strategy}

Việc xây dựng tunnel rất tốn kém, và các tunnel hết hạn sau một khoảng thời gian cố định kể từ khi được tạo. Tuy nhiên, khi một pool hết tunnel, Destination về cơ bản đã chết. Ngoài ra, tỷ lệ thành công trong việc xây dựng tunnel có thể thay đổi rất nhiều tùy theo điều kiện mạng cục bộ và toàn cầu. Do đó, việc duy trì một chiến lược xây dựng có tính dự đoán và thích ứng là rất quan trọng để đảm bảo rằng các tunnel mới được xây dựng thành công trước khi cần thiết, mà không xây dựng quá nhiều tunnel, xây dựng chúng quá sớm, hoặc tiêu tốn quá nhiều CPU hoặc băng thông để tạo và gửi các tin nhắn xây dựng được mã hóa.

Đối với mỗi bộ giá trị {exploratory/client, in/out, độ dài, độ biến thiên độ dài}, router duy trì thống kê về thời gian cần thiết để xây dựng thành công một tunnel. Sử dụng các thống kê này, nó tính toán thời gian trước khi tunnel hết hạn để bắt đầu cố gắng xây dựng một tunnel thay thế. Khi thời gian hết hạn đến gần mà không có tunnel thay thế thành công, nó bắt đầu nhiều lần thử xây dựng song song, và sau đó sẽ tăng số lượng các lần thử song song nếu cần thiết.

Để giới hạn băng thông và sử dụng CPU, router cũng hạn chế số lượng tối đa các lần thử xây dựng đang chờ xử lý trên tất cả các pool. Các lần xây dựng quan trọng (những lần cho exploratory tunnel và cho các pool đã hết tunnel) được ưu tiên.

## Điều Chỉnh Thông Điệp Tunnel {#tunnel.throttling}

Mặc dù các tunnel trong I2P có sự tương đồng với mạng chuyển mạch kênh, mọi thứ trong I2P đều hoàn toàn dựa trên thông điệp - các tunnel chỉ đơn giản là các thủ thuật kế toán để giúp tổ chức việc phân phối thông điệp. Không có giả định nào được đưa ra về độ tin cậy hoặc thứ tự của các thông điệp, và việc truyền lại được để lại cho các tầng cao hơn (ví dụ: thư viện streaming ở tầng client của I2P). Điều này cho phép I2P tận dụng các kỹ thuật điều tiết có sẵn cho cả mạng chuyển mạch gói và mạng chuyển mạch kênh. Chẳng hạn, mỗi router có thể theo dõi trung bình động của lượng dữ liệu mà mỗi tunnel đang sử dụng, kết hợp với tất cả các giá trị trung bình được sử dụng bởi các tunnel khác mà router đó đang tham gia, và có thể chấp nhận hoặc từ chối các yêu cầu tham gia tunnel bổ sung dựa trên khả năng và mức độ sử dụng của nó. Mặt khác, mỗi router có thể đơn giản loại bỏ các thông điệp vượt quá khả năng của nó, khai thác nghiên cứu được sử dụng trên Internet thông thường.

Trong triển khai hiện tại, các router thực hiện chiến lược loại bỏ sớm ngẫu nhiên có trọng số (WRED). Đối với tất cả các router tham gia (người tham gia nội bộ, gateway đầu vào và endpoint đầu ra), router sẽ bắt đầu loại bỏ ngẫu nhiên một phần thông điệp khi tiến gần đến giới hạn băng thông. Khi lưu lượng trở nên gần hơn hoặc vượt quá giới hạn, nhiều thông điệp hơn sẽ bị loại bỏ. Đối với người tham gia nội bộ, tất cả thông điệp đều được phân mảnh và đệm do đó có cùng kích thước. Tuy nhiên, tại gateway đầu vào và endpoint đầu ra, quyết định loại bỏ được thực hiện trên thông điệp đầy đủ (đã gộp lại), và kích thước thông điệp được tính đến. Các thông điệp lớn hơn có khả năng bị loại bỏ cao hơn. Ngoài ra, các thông điệp có khả năng bị loại bỏ tại endpoint đầu ra cao hơn so với gateway đầu vào, vì những thông điệp đó không "đi xa" trong hành trình của chúng và do đó chi phí mạng để loại bỏ những thông điệp đó thấp hơn.

## Công việc tương lai {#future}

### Trộn/Gộp lô {#tunnel.mixing}

Những chiến lược nào có thể được sử dụng tại gateway và tại mỗi hop để trì hoãn, sắp xếp lại thứ tự, định tuyến lại, hoặc padding tin nhắn? Việc này nên được thực hiện tự động ở mức độ nào, bao nhiêu nên được cấu hình như một thiết lập theo tunnel hoặc theo hop, và người tạo tunnel (và do đó, người dùng) nên kiểm soát hoạt động này như thế nào? Tất cả những điều này vẫn chưa được xác định, để được giải quyết trong một phiên bản phát hành xa xôi trong tương lai.

### Padding

Các chiến lược padding có thể được sử dụng ở nhiều cấp độ khác nhau, giải quyết việc lộ thông tin kích thước thông điệp cho các đối thủ khác nhau. Kích thước thông điệp tunnel cố định hiện tại là 1024 byte. Tuy nhiên, trong phạm vi này, các thông điệp bị phân mảnh không được tunnel padding gì cả, mặc dù đối với các thông điệp end-to-end, chúng có thể được padding như một phần của garlic wrapping.

### WRED

Các chiến lược WRED có tác động đáng kể đến hiệu suất đầu cuối và việc ngăn chặn sự sụp đổ tắc nghẽn mạng. Chiến lược WRED hiện tại cần được đánh giá cẩn thận và cải thiện.
