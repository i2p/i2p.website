---
title: "Triển khai Tunnel Cũ"
description: "Tài liệu lịch sử về triển khai tunnel gốc của I2P trước phiên bản 0.6.1.10"
slug: "old-tunnel-implementation"
aliases:
  - "/vi/docs/historical/tunnel-alt"
  - "/vi/docs/historical/tunnel-alt/"
  - "/vi/tunnel"
  - "/vi/tunnel/"
lastUpdated: "2016-11"
accurateFor: "historical"
---

**Lưu ý: Đã lỗi thời - KHÔNG được sử dụng! Đã được thay thế trong phiên bản 0.6.1.10 - xem [triển khai hiện tại](/docs/specs/tunnel-implementation) để biết đặc tả đang hoạt động.**

## 1) Tổng quan về tunnel {#tunnel.overview}

Trong I2P, các thông điệp được truyền theo một chiều thông qua một tunnel ảo của các peer, sử dụng bất kỳ phương tiện có sẵn nào để chuyển thông điệp đến hop tiếp theo. Các thông điệp đến gateway của tunnel, được đóng gói cho đường dẫn, và được chuyển tiếp đến hop tiếp theo trong tunnel, nơi xử lý và xác minh tính hợp lệ của thông điệp rồi gửi đến hop tiếp theo, cứ như vậy cho đến khi đạt đến điểm cuối của tunnel. Điểm cuối đó nhận các thông điệp được đóng gói bởi gateway và chuyển tiếp chúng theo hướng dẫn - hoặc đến một router khác, đến một tunnel khác trên một router khác, hoặc cục bộ.

Tunnel hoạt động giống nhau, nhưng có thể được phân thành hai nhóm khác nhau - inbound tunnel và outbound tunnel. Inbound tunnel có một gateway không đáng tin cậy chuyển tiếp tin nhắn xuống phía người tạo tunnel, người đóng vai trò là điểm cuối của tunnel. Đối với outbound tunnel, người tạo tunnel đóng vai trò là gateway, chuyển tiếp tin nhắn ra điểm cuối từ xa.

Người tạo tunnel chọn chính xác những peer nào sẽ tham gia vào tunnel, và cung cấp cho mỗi peer dữ liệu cấu hình cần thiết. Chúng có thể có độ dài thay đổi từ 0 hop (nơi gateway cũng là endpoint) đến 7 hop (nơi có 6 peer sau gateway và trước endpoint). Ý định là làm cho việc xác định độ dài của một tunnel trở nên khó khăn đối với cả những người tham gia và bên thứ ba, hoặc thậm chí đối với những người tham gia thông đồng để xác định xem họ có phải là một phần của cùng một tunnel hay không (trừ trường hợp các peer thông đồng nằm cạnh nhau trong tunnel). Các message bị lỗi cũng được loại bỏ càng sớm càng tốt, giảm tải mạng.

Ngoài độ dài của chúng, còn có các tham số có thể cấu hình bổ sung cho mỗi tunnel có thể được sử dụng, chẳng hạn như giới hạn kích thước hoặc tần suất của các thông điệp được gửi, cách sử dụng padding, tunnel nên hoạt động trong bao lâu, có nên chèn các thông điệp chaff hay không, có nên sử dụng phân mảnh hay không, và nếu có, nên sử dụng các chiến lược batching nào.

Trong thực tế, một loạt các tunnel pools được sử dụng cho các mục đích khác nhau - mỗi đích đến client cục bộ có bộ inbound tunnels và outbound tunnels riêng, được cấu hình để đáp ứng nhu cầu ẩn danh và hiệu suất của nó. Ngoài ra, router cũng duy trì một loạt các pools để tham gia vào network database và để quản lý chính các tunnels.

I2P là một mạng chuyển mạch gói tin vốn có, ngay cả với các tunnel này, cho phép nó tận dụng nhiều tunnel chạy song song, tăng khả năng phục hồi và cân bằng tải. Bên ngoài lớp I2P cốt lõi, có một thư viện streaming đầu cuối đến đầu cuối tùy chọn có sẵn cho các ứng dụng client, cung cấp hoạt động giống TCP, bao gồm sắp xếp lại thông điệp, truyền lại, kiểm soát tắc nghẽn, v.v.

## 2) Hoạt động tunnel {#tunnel.operation}

Hoạt động của tunnel có bốn quy trình riêng biệt, được thực hiện bởi các peer khác nhau trong tunnel. Đầu tiên, tunnel gateway tích lũy một số tunnel message và tiền xử lý chúng thành thứ gì đó để phân phối qua tunnel. Tiếp theo, gateway đó mã hóa dữ liệu đã được tiền xử lý, sau đó chuyển tiếp nó đến hop đầu tiên. Peer đó, và các tunnel participant tiếp theo, mở từng lớp mã hóa, xác minh tính toàn vẹn của message, rồi chuyển tiếp đến peer tiếp theo. Cuối cùng, message đến endpoint nơi các message được gateway gộp lại sẽ được tách ra một lần nữa và chuyển tiếp theo yêu cầu.

Tunnel ID là các số 4 byte được sử dụng tại mỗi hop - các thành viên biết tunnel ID nào cần lắng nghe tin nhắn và tunnel ID nào họ nên chuyển tiếp đến hop tiếp theo. Các tunnel có thời gian sống ngắn (hiện tại là 10 phút), nhưng tùy thuộc vào mục đích của tunnel, và mặc dù các tunnel tiếp theo có thể được xây dựng sử dụng cùng một chuỗi các peer, tunnel ID của mỗi hop sẽ thay đổi.

### 2.1) Tiền xử lý thông điệp {#tunnel.preprocessing}

Khi gateway muốn truyền dữ liệu qua tunnel, trước tiên nó thu thập không hoặc nhiều I2NP messages (không quá 32KB), chọn lượng padding sẽ được sử dụng, và quyết định cách mỗi I2NP message nên được xử lý bởi tunnel endpoint, mã hóa dữ liệu đó vào raw tunnel payload:

- Số nguyên không dấu 2 byte chỉ định số lượng byte padding
- nhiều byte ngẫu nhiên tương ứng
- một chuỗi gồm không hoặc nhiều cặp { instructions, message }

Các hướng dẫn được mã hóa như sau:

- Giá trị 1 byte:
  ```
  bits 0-1: loại giao hàng
            (0x0 = LOCAL, 0x01 = TUNNEL, 0x02 = ROUTER)
     bit 2: có bao gồm độ trễ không?  (1 = có, 0 = không)
     bit 3: có phân mảnh không?  (1 = có, 0 = không)
     bit 4: có tùy chọn mở rộng không?  (1 = có, 0 = không)
  bits 5-7: dành riêng
  ```
- nếu loại giao hàng là TUNNEL, một tunnel ID 4 byte
- nếu loại giao hàng là TUNNEL hoặc ROUTER, một router hash 32 byte
- nếu cờ bao gồm độ trễ là true, một giá trị 1 byte:
  ```
     bit 0: loại (0 = nghiêm ngặt, 1 = ngẫu nhiên)
  bits 1-7: số mũ độ trễ (2^giá trị phút)
  ```
- nếu cờ phân mảnh là true, một message ID 4 byte, và một giá trị 1 byte:
  ```
  bits 0-6: số thứ tự mảnh
     bit 7: là mảnh cuối cùng không?  (1 = có, 0 = không)
  ```
- nếu cờ tùy chọn mở rộng là true:
  ```
  = kích thước tùy chọn 1 byte (tính bằng byte)
  = số byte tương ứng
  ```
- Kích thước 2 byte của thông điệp I2NP

Thông điệp I2NP được mã hóa theo dạng chuẩn của nó, và dữ liệu đã được xử lý trước phải được đệm để chia hết cho 16 byte.

### 2.2) Xử lý Gateway {#tunnel.gateway}

Sau khi tiền xử lý các thông điệp thành một payload được đệm, gateway mã hóa payload với tám khóa, xây dựng một khối checksum để mỗi peer có thể xác minh tính toàn vẹn của payload bất cứ lúc nào, cũng như một khối xác minh đầu cuối để điểm cuối tunnel xác minh tính toàn vẹn của khối checksum. Các chi tiết cụ thể như sau.

Mã hóa được sử dụng sao cho việc giải mã chỉ cần chạy dữ liệu với AES ở chế độ CBC, tính toán SHA256 của một phần cố định nhất định trong thông điệp (byte 16 đến $size-144), và tìm kiếm 16 byte đầu tiên của hash đó trong khối checksum. Có một số lượng hop cố định được định nghĩa (8 peer) để chúng ta có thể xác minh thông điệp mà không làm lộ vị trí trong tunnel hoặc khiến thông điệp liên tục "co lại" khi các lớp được bóc tách. Đối với các tunnel ngắn hơn 8 hop, người tạo tunnel sẽ đảm nhận vai trò của các hop dư thừa, giải mã bằng khóa của họ (đối với outbound tunnel, điều này được thực hiện ở đầu, và đối với inbound tunnel, ở cuối).

Phần khó trong mã hóa là xây dựng khối checksum đan xen đó, điều này về cơ bản yêu cầu tìm hiểu hash của payload sẽ trông như thế nào ở mỗi bước, sắp xếp ngẫu nhiên các hash đó, sau đó xây dựng một ma trận về việc mỗi hash được sắp xếp ngẫu nhiên đó sẽ trông như thế nào ở mỗi bước. Gateway chính nó phải giả vờ rằng nó là một trong các peer trong khối checksum để hop đầu tiên không thể biết rằng hop trước đó là gateway. Để hình dung điều này một chút:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">Peer</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">Key</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">Dir</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">IV</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">Payload</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">eH[0]</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">eH[1]</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">eH[2]</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">eH[3]</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">eH[4]</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">eH[5]</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">eH[6]</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">eH[7]</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">V</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer0</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[0]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">recv</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer0</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[0]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">send</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[0]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[0]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[0])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[0]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer1</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[1]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">recv</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[0]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[0]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[0])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[0]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer1</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[1]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">send</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[1]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[1]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[1])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[1]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer2</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[2]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">recv</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[1]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[1]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[1])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[1]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer2</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[2]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">send</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[2]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[2]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[2])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[2]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer3</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[3]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">recv</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[2]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[2]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[2])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[2]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer3</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[3]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">send</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[3]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[3]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[3])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[3]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer4</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[4]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">recv</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[3]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[3]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[3])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[3]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer4</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[4]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">send</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[4]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[4]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[4])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[4]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer5</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[5]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">recv</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[4]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[4]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[4])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[4]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer5</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[5]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">send</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[5]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[5]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[5])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[5]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer6</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[6]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">recv</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[5]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[5]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[5])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[5]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer6</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[6]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">send</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[6]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[6]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[6])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[6]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer7</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[7]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">recv</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[6]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[6]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[6])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[6]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer7</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[7]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">send</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[7]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[7]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[7])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[7]</td>
    </tr>
  </tbody>
</table>
Trong ví dụ trên, P[7] giống với dữ liệu gốc được truyền qua tunnel (các thông điệp đã được tiền xử lý), và V[7] là 16 byte đầu tiên của SHA256 của eH[0-7] như được thấy trên peer7 sau khi giải mã. Đối với các ô trong ma trận "cao hơn" so với hash, giá trị của chúng được tạo ra bằng cách mã hóa ô bên dưới nó với khóa dành cho peer bên dưới nó, sử dụng phần cuối của cột bên trái nó làm IV. Đối với các ô trong ma trận "thấp hơn" so với hash, chúng bằng với ô phía trên chúng, được giải mã bằng khóa của peer hiện tại, sử dụng phần cuối của khối được mã hóa trước đó trên hàng đó.

Với ma trận ngẫu nhiên hóa các khối checksum này, mỗi peer sẽ có thể tìm thấy hash của payload, hoặc nếu không có ở đó, biết rằng thông điệp đã bị hỏng. Sự vướng víu bằng cách sử dụng chế độ CBC làm tăng độ khó trong việc gắn thẻ chính các khối checksum, nhưng vẫn có thể việc gắn thẻ đó không được phát hiện ngay lập tức nếu các cột sau dữ liệu được gắn thẻ đã được sử dụng để kiểm tra payload tại một peer. Trong mọi trường hợp, điểm cuối tunnel (peer 7) biết chắc chắn liệu có khối checksum nào đã bị gắn thẻ hay không, vì điều đó sẽ làm hỏng khối xác minh (V[7]).

IV[0] là một giá trị ngẫu nhiên 16 byte, và IV[i] là 16 byte đầu tiên của H(D(IV[i-1], K[i-1]) xor IV_WHITENER). Chúng ta không sử dụng cùng một IV dọc theo đường dẫn, vì điều đó sẽ cho phép sự thông đồng tầm thường, và chúng ta sử dụng hash của giá trị đã giải mã để truyền bá IV nhằm cản trở việc rò rỉ khóa. IV_WHITENER là một giá trị cố định 16 byte.

Khi gateway muốn gửi thông điệp, họ xuất hàng phù hợp cho peer là hop đầu tiên (thường là hàng peer1.recv) và chuyển tiếp toàn bộ hàng đó.

### 2.3) Xử lý của participant {#tunnel.participant}

Khi một thành viên trong tunnel nhận được một tin nhắn, họ giải mã một lớp bằng tunnel key của mình sử dụng AES256 ở chế độ CBC với 16 byte đầu tiên làm IV. Sau đó họ tính toán hash của những gì họ thấy là payload (byte từ 16 đến $size-144) và tìm kiếm 16 byte đầu tiên của hash đó trong khối checksum đã giải mã. Nếu không tìm thấy kết quả khớp, tin nhắn sẽ bị loại bỏ. Ngược lại, IV được cập nhật bằng cách giải mã nó, thực hiện phép XOR giá trị đó với IV_WHITENER, và thay thế nó bằng 16 byte đầu tiên của hash của nó. Tin nhắn kết quả sau đó được chuyển tiếp đến peer tiếp theo để xử lý.

Để ngăn chặn các cuộc tấn công replay ở cấp độ tunnel, mỗi participant sẽ theo dõi các IV nhận được trong suốt vòng đời của tunnel, từ chối các bản trùng lặp. Việc sử dụng bộ nhớ cần thiết sẽ là tối thiểu, vì mỗi tunnel chỉ có thời gian tồn tại rất ngắn (hiện tại là 10 phút). Tốc độ truyền không đổi 100KBps qua một tunnel với các thông điệp đầy đủ 32KB sẽ tạo ra 1875 thông điệp, chỉ cần dưới 30KB bộ nhớ. Gateway và endpoint xử lý replay bằng cách theo dõi các message ID và thời gian hết hạn trên các thông điệp I2NP chứa trong tunnel.

### 2.4) Xử lý điểm cuối {#tunnel.endpoint}

Khi một thông điệp đến tunnel endpoint, chúng giải mã và xác minh nó như một participant bình thường. Nếu khối checksum có kết quả khớp hợp lệ, endpoint sau đó tính toán hash của chính khối checksum (như được thấy sau khi giải mã) và so sánh với verification hash đã được giải mã (16 byte cuối cùng). Nếu verification hash đó không khớp, endpoint ghi nhận nỗ lực gắn thẻ bởi một trong các tunnel participants và có thể loại bỏ thông điệp.

Tại thời điểm này, điểm cuối tunnel đã có dữ liệu đã được xử lý trước được gửi bởi gateway, sau đó nó có thể phân tích thành các thông điệp I2NP được bao gồm và chuyển tiếp chúng theo yêu cầu trong hướng dẫn giao hàng của chúng.

### 2.5) Padding {#tunnel.padding}

Có thể có nhiều chiến lược padding tunnel khác nhau, mỗi chiến lược có những ưu điểm riêng:

- Không padding
- Padding đến kích thước ngẫu nhiên
- Padding đến kích thước cố định
- Padding đến KB gần nhất
- Padding đến kích thước lũy thừa gần nhất (2^n bytes)

*Nên sử dụng phương pháp nào? không padding là hiệu quả nhất, random padding là cách chúng ta đang dùng hiện tại, kích thước cố định sẽ hoặc là lãng phí cực kỳ hoặc buộc chúng ta phải triển khai phân mảnh. Padding đến kích thước exponential gần nhất (giống Freenet) có vẻ hứa hẹn. Có lẽ chúng ta nên thu thập một số thống kê trên mạng về kích thước thông điệp, sau đó xem chi phí và lợi ích sẽ nảy sinh từ các chiến lược khác nhau?*

### 2.6) Phân mảnh tunnel {#tunnel.fragmentation}

Đối với các phương án padding và mixing khác nhau, việc phân mảnh một I2NP message duy nhất thành nhiều phần, mỗi phần được gửi riêng biệt qua các tunnel message khác nhau có thể hữu ích từ góc độ ẩn danh. Điểm cuối có thể hỗ trợ hoặc không hỗ trợ việc phân mảnh đó (loại bỏ hoặc giữ lại các mảnh khi cần thiết), và việc xử lý phân mảnh sẽ không được triển khai ngay lập tức.

### 2.7) Các lựa chọn thay thế {#tunnel.alternatives}

#### 2.7.1) Không sử dụng khối checksum {#tunnel.nochecksum}

Một giải pháp thay thế cho quy trình trên là loại bỏ hoàn toàn khối checksum và thay thế hash xác minh bằng một hash đơn giản của payload. Điều này sẽ đơn giản hóa việc xử lý tại tunnel gateway và tiết kiệm 144 bytes băng thông tại mỗi hop. Mặt khác, những kẻ tấn công bên trong tunnel có thể dễ dàng điều chỉnh kích thước thông điệp thành một kích thước có thể dễ dàng theo dõi bởi những người quan sát bên ngoài thông đồng cùng với các thành viên tunnel sau đó. Sự hỏng hóc này cũng sẽ gây ra sự lãng phí toàn bộ băng thông cần thiết để truyền tải thông điệp. Không có xác thực per-hop, cũng có thể tiêu thụ tài nguyên mạng quá mức bằng cách xây dựng các tunnel cực dài, hoặc bằng cách tạo vòng lặp trong tunnel.

#### 2.7.2) Điều chỉnh xử lý tunnel giữa chừng {#tunnel.reroute}

Trong khi thuật toán định tuyến tunnel đơn giản sẽ đủ cho hầu hết các trường hợp, có ba giải pháp thay thế có thể được khám phá:

- Trì hoãn một thông điệp trong tunnel tại một hop tùy ý trong một khoảng thời gian được chỉ định hoặc một khoảng thời gian ngẫu nhiên. Điều này có thể đạt được bằng cách thay thế hash trong checksum block bằng ví dụ 8 byte đầu tiên của hash, theo sau là một số hướng dẫn trì hoãn. Thay vào đó, các hướng dẫn có thể yêu cầu participant thực sự diễn giải raw payload như nó vốn có, và hoặc loại bỏ thông điệp hoặc tiếp tục chuyển tiếp nó xuống đường dẫn (nơi nó sẽ được endpoint diễn giải như một chaff message). Phần sau của điều này sẽ yêu cầu gateway điều chỉnh thuật toán mã hóa của nó để tạo ra cleartext payload trên một hop khác, nhưng nó không nên gặp nhiều khó khăn.

- Cho phép các router tham gia trong một tunnel trộn lại thông điệp trước khi chuyển tiếp - định tuyến nó qua một trong các outbound tunnel của chính peer đó, mang theo hướng dẫn để gửi đến hop tiếp theo. Điều này có thể được sử dụng theo cách có kiểm soát (với các hướng dẫn en-route như độ trễ ở trên) hoặc theo xác suất.

- Triển khai mã cho tunnel creator để định nghĩa lại "next hop" (bước tiếp theo) của một peer trong tunnel, cho phép chuyển hướng động thêm.

#### 2.7.3) Sử dụng tunnel hai chiều {#tunnel.bidirectional}

Chiến lược hiện tại sử dụng hai tunnel riêng biệt cho giao tiếp inbound và outbound không phải là kỹ thuật duy nhất có sẵn, và nó có những tác động đến tính ẩn danh. Về mặt tích cực, việc sử dụng các tunnel riêng biệt làm giảm dữ liệu lưu lượng bị lộ để phân tích cho các thành viên tham gia trong tunnel - ví dụ, các peer trong tunnel outbound từ trình duyệt web chỉ thấy lưu lượng của HTTP GET, trong khi các peer trong tunnel inbound sẽ thấy payload được gửi dọc theo tunnel. Với tunnel hai chiều, tất cả thành viên tham gia sẽ có quyền truy cập vào thông tin rằng ví dụ 1KB đã được gửi theo một hướng, sau đó 100KB theo hướng khác. Về mặt tiêu cực, việc sử dụng tunnel một chiều có nghĩa là có hai nhóm peer cần được phân tích hồ sơ và tính toán, và cần phải cẩn thận thêm để giải quyết tốc độ gia tăng của các cuộc tấn công predecessor. Quá trình gộp tunnel và xây dựng được phác thảo dưới đây sẽ giảm thiểu lo ngại về cuộc tấn công predecessor, mặc dù nếu muốn, việc xây dựng cả tunnel inbound và outbound dọc theo cùng các peer cũng không gặp nhiều khó khăn.

#### 2.7.4) Sử dụng kích thước khối nhỏ hơn {#tunnel.smallerhashes}

Hiện tại, việc chúng tôi sử dụng AES giới hạn kích thước block xuống 16 byte, điều này cung cấp kích thước tối thiểu cho từng cột của checksum block. Nếu sử dụng một thuật toán khác với kích thước block nhỏ hơn, hoặc có thể cho phép xây dựng an toàn checksum block với các phần nhỏ hơn của hash, thì có thể đáng để khám phá. 16 byte được sử dụng hiện tại tại mỗi hop nên là quá đủ.

## 3) Xây dựng tunnel {#tunnel.building}

Khi xây dựng một tunnel, người tạo phải gửi yêu cầu kèm theo dữ liệu cấu hình cần thiết đến từng hop, sau đó chờ người tham gia tiềm năng trả lời cho biết họ đồng ý hay không đồng ý. Các thông điệp yêu cầu tunnel này và phản hồi của chúng được bao bọc bằng garlic encryption để chỉ có router biết khóa mới có thể giải mã, và đường dẫn đi theo cả hai hướng cũng được định tuyến qua tunnel. Có ba khía cạnh quan trọng cần ghi nhớ khi tạo ra các tunnel: những peer nào được sử dụng (và ở đâu), cách thức gửi yêu cầu (và nhận phản hồi), và cách duy trì chúng.

### 3.1) Lựa chọn peer {#tunnel.peerselection}

Ngoài hai loại tunnel - inbound và outbound - có hai kiểu lựa chọn peer được sử dụng cho các tunnel khác nhau - exploratory và client. Exploratory tunnel được sử dụng cho cả việc bảo trì network database và bảo trì tunnel, trong khi client tunnel được sử dụng cho các tin nhắn client đầu cuối.

#### 3.1.1) Lựa chọn peer cho tunnel khám phá {#tunnel.selection.exploratory}

Các tunnel thăm dò được xây dựng từ một lựa chọn ngẫu nhiên các peer từ một tập con của mạng lưới. Tập con cụ thể này thay đổi tùy thuộc vào router cục bộ và nhu cầu định tuyến tunnel của chúng. Nói chung, các tunnel thăm dò được xây dựng từ các peer được chọn ngẫu nhiên thuộc danh mục hồ sơ "không bị lỗi nhưng đang hoạt động" của peer. Mục đích thứ hai của các tunnel này, ngoài việc chỉ định tuyến tunnel, là tìm kiếm các peer có dung lượng cao nhưng chưa được sử dụng hết để có thể thăng cấp chúng sử dụng trong các tunnel client.

#### 3.1.2) Lựa chọn peer cho tunnel client {#tunnel.selection.client}

Các tunnel client được xây dựng với một bộ yêu cầu nghiêm ngặt hơn - router cục bộ sẽ chọn các peer từ danh mục profile "nhanh và dung lượng cao" để hiệu suất và độ tin cậy sẽ đáp ứng nhu cầu của ứng dụng client. Tuy nhiên, có một số chi tiết quan trọng ngoài việc lựa chọn cơ bản đó cần được tuân thủ, tùy thuộc vào nhu cầu ẩn danh của client.

Đối với một số client lo ngại về các đối thủ thực hiện cuộc tấn công predecessor, việc lựa chọn tunnel có thể giữ các peer được chọn theo thứ tự nghiêm ngặt - nếu A, B, và C nằm trong một tunnel, hop sau A luôn là B, và hop sau B luôn là C. Một thứ tự ít nghiêm ngặt hơn cũng có thể, đảm bảo rằng trong khi hop sau A có thể là B, thì B không bao giờ có thể đứng trước A. Các tùy chọn cấu hình khác bao gồm khả năng chỉ cố định các inbound tunnel gateway và outbound tunnel endpoint, hoặc luân phiên theo tỷ lệ MTBF.

### 3.2) Yêu cầu gửi {#tunnel.request}

Như đã đề cập ở trên, một khi người tạo tunnel biết những peer nào sẽ tham gia vào tunnel và theo thứ tự nào, người tạo sẽ xây dựng một loạt các thông điệp yêu cầu tunnel, mỗi thông điệp chứa thông tin cần thiết cho peer đó. Ví dụ, các tunnel tham gia sẽ được cung cấp tunnel ID 4 byte để nhận thông điệp, tunnel ID 4 byte để gửi thông điệp đi, hash 32 byte của danh tính hop tiếp theo, và layer key 32 byte được sử dụng để loại bỏ một lớp khỏi tunnel. Tất nhiên, các endpoint của outbound tunnel không được cung cấp thông tin "hop tiếp theo" hay "tunnel ID tiếp theo". Tuy nhiên, các gateway của inbound tunnel được cung cấp 8 layer key theo thứ tự chúng cần được mã hóa (như đã mô tả ở trên). Để cho phép phản hồi, yêu cầu chứa một session tag ngẫu nhiên và một session key ngẫu nhiên mà peer có thể sử dụng để garlic encrypt quyết định của họ, cũng như tunnel mà garlic đó sẽ được gửi tới. Ngoài thông tin trên, các tùy chọn cụ thể của client có thể được bao gồm, chẳng hạn như mức độ điều chỉnh tốc độ cho tunnel, chiến lược padding hoặc batch nào sẽ sử dụng, v.v.

Sau khi xây dựng tất cả các thông điệp yêu cầu, chúng được bao bọc bằng garlic encryption cho router đích và gửi qua một exploratory tunnel. Khi nhận được, peer đó sẽ xác định liệu họ có thể hoặc sẵn sàng tham gia hay không, tạo một thông điệp phản hồi và thực hiện cả garlic wrapping và tunnel routing cho phản hồi với thông tin được cung cấp. Khi nhận được phản hồi tại nơi tạo tunnel, tunnel được coi là hợp lệ trên hop đó (nếu được chấp nhận). Một khi tất cả các peer đã chấp nhận, tunnel sẽ hoạt động.

### 3.3) Gộp chung {#tunnel.pooling}

Để cho phép hoạt động hiệu quả, router duy trì một loạt các tunnel pool, mỗi pool quản lý một nhóm tunnel được sử dụng cho một mục đích cụ thể với cấu hình riêng của chúng. Khi cần một tunnel cho mục đích đó, router sẽ chọn ngẫu nhiên một tunnel từ pool thích hợp. Nhìn chung, có hai exploratory tunnel pool - một inbound và một outbound - mỗi pool sử dụng các thiết lập khám phá mặc định của router. Ngoài ra, có một cặp pool cho mỗi đích cục bộ - một inbound và một outbound tunnel. Những pool này sử dụng cấu hình được chỉ định khi đích cục bộ kết nối với router, hoặc các thiết lập mặc định của router nếu không được chỉ định.

Mỗi pool trong cấu hình của nó có một số thiết lập chính, định nghĩa số lượng tunnel cần giữ hoạt động, số lượng tunnel dự phòng cần duy trì trong trường hợp lỗi, tần suất kiểm tra các tunnel, độ dài của tunnel, liệu các độ dài đó có nên được ngẫu nhiên hóa hay không, tần suất xây dựng tunnel thay thế, cũng như bất kỳ thiết lập nào khác được phép khi cấu hình từng tunnel riêng lẻ.

### 3.4) Các phương án thay thế {#tunnel.building.alternatives}

#### 3.4.1) Xây dựng kính thiên văn {#tunnel.building.telescoping}

Một câu hỏi có thể nảy sinh liên quan đến việc sử dụng các tunnel khám phá để gửi và nhận thông điệp tạo tunnel là điều này ảnh hưởng như thế nào đến khả năng bị tổn thương của tunnel trước các cuộc tấn công predecessor. Trong khi các điểm cuối và gateway của những tunnel đó sẽ được phân phối ngẫu nhiên trên toàn mạng (thậm chí có thể bao gồm cả người tạo tunnel trong tập hợp đó), một phương án khác là sử dụng chính các đường dẫn tunnel để truyền yêu cầu và phản hồi, như được thực hiện trong [TOR](https://www.torproject.org/). Tuy nhiên, điều này có thể dẫn đến rò rỉ trong quá trình tạo tunnel, cho phép các peer khám phá có bao nhiêu hop ở phía sau trong tunnel bằng cách theo dõi thời gian hoặc số lượng gói tin khi tunnel được xây dựng. Các kỹ thuật có thể được sử dụng để giảm thiểu vấn đề này, chẳng hạn như sử dụng từng hop làm endpoint (theo [2.7.2](#tunnel.reroute)) cho một số lượng thông điệp ngẫu nhiên trước khi tiếp tục xây dựng hop tiếp theo.

#### 3.4.2) Tunnel không khám phá cho quản lý {#tunnel.building.nonexploratory}

Một phương án thay thế thứ hai cho quá trình xây dựng tunnel là cung cấp cho router một bộ pool inbound và outbound không thăm dò bổ sung, sử dụng chúng cho tunnel request và response. Giả sử router có cái nhìn tích hợp tốt về mạng, điều này không cần thiết, nhưng nếu router bị phân vùng theo cách nào đó, việc sử dụng các pool không thăm dò cho quản lý tunnel sẽ giảm thiểu việc rò rỉ thông tin về những peer nào có trong phân vùng của router.

## 4) Điều tiết tunnel {#tunnel.throttling}

Mặc dù các tunnel trong I2P có vẻ giống với mạng chuyển mạch kênh, mọi thứ trong I2P đều hoàn toàn dựa trên thông điệp - các tunnel chỉ là những thủ thuật kế toán để giúp tổ chức việc phân phối thông điệp. Không có giả định nào được đưa ra về độ tin cậy hay thứ tự của các thông điệp, và việc truyền lại được để lại cho các tầng cao hơn (ví dụ như thư viện streaming tại tầng client của I2P). Điều này cho phép I2P tận dụng các kỹ thuật điều tiết có sẵn cho cả mạng chuyển mạch gói và mạng chuyển mạch kênh. Chẳng hạn, mỗi router có thể theo dõi trung bình trượt của lượng dữ liệu mà mỗi tunnel đang sử dụng, kết hợp với tất cả các giá trị trung bình được sử dụng bởi các tunnel khác mà router đang tham gia, và có thể chấp nhận hoặc từ chối các yêu cầu tham gia tunnel bổ sung dựa trên dung lượng và mức sử dụng của nó. Mặt khác, mỗi router có thể đơn giản bỏ qua các thông điệp vượt quá khả năng của nó, tận dụng nghiên cứu được sử dụng trên Internet thông thường.

## 5) Trộn/gộp lô {#tunnel.mixing}

Những chiến lược nào nên được sử dụng tại gateway và tại mỗi hop để trì hoãn, sắp xếp lại thứ tự, định tuyến lại hoặc đệm các thông điệp? Mức độ nào việc này nên được thực hiện tự động, bao nhiêu nên được cấu hình như một thiết lập cho mỗi tunnel hoặc mỗi hop, và người tạo tunnel (và do đó, người dùng) nên kiểm soát hoạt động này như thế nào? Tất cả điều này vẫn chưa được xác định, sẽ được tìm hiểu cho một phiên bản tương lai.
