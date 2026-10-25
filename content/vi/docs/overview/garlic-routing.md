---
title: "Garlic Routing"
description: "Hiểu về thuật ngữ, kiến trúc và triển khai garlic routing trong I2P"
slug: "garlic-routing"
aliases:
  - "/vi/how_garlicrouting"
  - "/vi/how_garlicrouting/"
lastUpdated: "2025-10"
accurateFor: "0.9.12"
---

## Định tuyến Garlic và Thuật ngữ "Garlic"

Các thuật ngữ "garlic routing" và "garlic encryption" thường được sử dụng khá lỏng lẻo khi đề cập đến công nghệ của I2P. Ở đây, chúng tôi giải thích lịch sử của các thuật ngữ này, các ý nghĩa khác nhau, và việc sử dụng các phương pháp "garlic" trong I2P.

"Garlic routing" lần đầu tiên được đặt tên bởi [Michael J. Freedman](https://www.cs.princeton.edu/~mfreed/) trong [luận văn Thạc sĩ](https://www.freehaven.net/papers.html) Free Haven của Roger Dingledine, Mục 8.1.1 (tháng 6 năm 2000), được phát triển từ [Onion Routing](https://www.onion-router.net/).

"Garlic" có thể đã được các nhà phát triển I2P sử dụng ban đầu vì I2P triển khai một dạng đóng gói như Freedman mô tả, hoặc đơn giản để nhấn mạnh sự khác biệt chung so với Tor. Lý do cụ thể có thể đã bị thất lạc trong lịch sử. Nói chung, khi đề cập đến I2P, thuật ngữ "garlic" có thể có nghĩa là một trong ba thứ sau:

1. Mã hóa phân lớp
2. Gói nhiều tin nhắn lại với nhau
3. Mã hóa ElGamal/AES

Thật không may, việc sử dụng thuật ngữ "garlic" của I2P trong những năm qua không phải lúc nào cũng chính xác; do đó người đọc cần thận trọng khi gặp thuật ngữ này. Hy vọng rằng, giải thích dưới đây sẽ làm rõ mọi thứ.

### Mã hóa nhiều lớp

Onion routing là một kỹ thuật để xây dựng các đường dẫn, hay tunnel, thông qua một chuỗi các peer, và sau đó sử dụng tunnel đó. Các thông điệp được mã hóa liên tục bởi người khởi tạo, và sau đó được giải mã bởi từng hop. Trong giai đoạn xây dựng, chỉ các hướng dẫn định tuyến cho hop tiếp theo được tiết lộ cho mỗi peer. Trong giai đoạn hoạt động, các thông điệp được truyền qua tunnel, và thông điệp cùng các hướng dẫn định tuyến của nó chỉ được tiết lộ cho điểm cuối của tunnel.

Điều này tương tự như cách Mixmaster (xem [so sánh mạng](/docs/overview/comparison/)) gửi tin nhắn - lấy một tin nhắn, mã hóa nó bằng khóa công khai của người nhận, lấy tin nhắn đã mã hóa đó và mã hóa nó (cùng với các hướng dẫn chỉ định hop tiếp theo), và sau đó lấy tin nhắn đã mã hóa kết quả đó và cứ thế, cho đến khi nó có một lớp mã hóa cho mỗi hop dọc theo đường dẫn.

Theo nghĩa này, "garlic routing" như một khái niệm chung thì giống hệt với "onion routing". Như được triển khai trong I2P, tất nhiên, có một số khác biệt so với việc triển khai trong Tor; xem bên dưới. Mặc dù vậy, có những điểm tương đồng đáng kể khiến I2P được hưởng lợi từ [một lượng lớn nghiên cứu học thuật về onion routing](https://www.onion-router.net/Publications.html), [Tor, và các mixnet tương tự](https://freehaven.net/anonbib/topic.html).

### Gộp Nhiều Thông Điệp

Michael Freedman đã định nghĩa "garlic routing" như một phần mở rộng của onion routing, trong đó nhiều thông điệp được gộp lại với nhau. Ông gọi mỗi thông điệp là một "bulb" (củ). Tất cả các thông điệp, mỗi thông điệp có hướng dẫn giao hàng riêng, được tiết lộ tại điểm cuối. Điều này cho phép gộp hiệu quả một "reply block" của onion routing với thông điệp gốc.

Khái niệm này được triển khai trong I2P, như mô tả dưới đây. Thuật ngữ của chúng tôi cho "củ" garlic là "tép". Bất kỳ số lượng tin nhắn nào cũng có thể được chứa, thay vì chỉ một tin nhắn duy nhất. Đây là một điểm khác biệt quan trọng so với onion routing được triển khai trong Tor. Tuy nhiên, đây chỉ là một trong nhiều khác biệt kiến trúc lớn giữa I2P và Tor; có lẽ bản thân nó không đủ để biện minh cho việc thay đổi thuật ngữ.

Một điểm khác biệt khác so với phương pháp được mô tả bởi Freedman là đường dẫn là đơn hướng - không có "điểm quay" như thấy trong onion routing hoặc mixmaster reply blocks, điều này giúp đơn giản hóa thuật toán rất nhiều và cho phép việc phân phối linh hoạt và đáng tin cậy hơn.

### Mã hóa ElGamal/AES

Trong một số trường hợp, "garlic encryption" có thể đơn giản chỉ có nghĩa là mã hóa [ElGamal/AES+SessionTag](/docs/specs/elgamal-aes/) (không có nhiều lớp).

---

## Các phương thức "Garlic" trong I2P

Bây giờ chúng ta đã định nghĩa các thuật ngữ "garlic" khác nhau, chúng ta có thể nói rằng I2P sử dụng garlic routing, bundling và encryption ở ba nơi:

1. Để xây dựng và định tuyến qua tunnel (mã hóa nhiều lớp)
2. Để xác định thành công hay thất bại của việc gửi tin nhắn đầu cuối (đóng gói)
3. Để xuất bản một số mục trong cơ sở dữ liệu mạng (giảm xác suất của một cuộc tấn công phân tích lưu lượng thành công) (ElGamal/AES)

Ngoài ra còn có những cách thức quan trọng mà kỹ thuật này có thể được sử dụng để cải thiện hiệu suất của mạng, khai thác sự cân bằng giữa độ trễ/thông lượng của transport, và phân nhánh dữ liệu qua các đường dẫn dự phòng để tăng độ tin cậy.

### Xây dựng và Định tuyến Tunnel

Trong I2P, các tunnel là đơn hướng. Mỗi bên xây dựng hai tunnel, một cho lưu lượng đi ra và một cho lưu lượng đi vào. Do đó, cần có bốn tunnel cho một tin nhắn khứ hồi và phản hồi duy nhất.

Tunnel được xây dựng và sử dụng với mã hóa nhiều lớp. Điều này được mô tả trên [trang triển khai tunnel](/docs/specs/tunnel-implementation/). Chúng tôi sử dụng [ElGamal/AES+SessionTag](/docs/specs/elgamal-aes/) cho việc mã hóa.

Tunnel là cơ chế đa năng để vận chuyển tất cả [I2NP messages](/docs/specs/i2np/), và Garlic Messages không được sử dụng để xây dựng tunnel. Chúng tôi không gộp nhiều I2NP messages vào một Garlic Message duy nhất để giải nén tại điểm cuối tunnel đi ra; mã hóa tunnel là đủ.

### Đóng gói tin nhắn đầu cuối

Ở lớp trên các tunnel, I2P truyền tải các thông điệp end-to-end giữa các [Destinations](/docs/specs/common-structures/). Cũng giống như trong một tunnel đơn lẻ, chúng tôi sử dụng [ElGamal/AES+SessionTag](/docs/specs/elgamal-aes/) để mã hóa. Mỗi thông điệp client được gửi đến router thông qua [giao diện I2CP](/docs/api/i2cp/) trở thành một Garlic Clove đơn lẻ với Delivery Instructions riêng của nó, bên trong một Garlic Message. Delivery Instructions có thể chỉ định một Destination, Router, hoặc Tunnel.

Thông thường, một Garlic Message sẽ chỉ chứa một clove. Tuy nhiên, router sẽ định kỳ gộp hai clove bổ sung vào trong Garlic Message:

![Garlic Message Cloves](/images/garliccloves.svg)

1. **Một Thông điệp Trạng thái Giao hàng**, với Hướng dẫn Giao hàng chỉ định rằng nó được gửi trả lại cho router khởi tạo như một xác nhận. Điều này tương tự như "reply block" hoặc "reply onion" được mô tả trong các tài liệu tham khảo. Nó được sử dụng để xác định thành công hay thất bại của việc giao hàng thông điệp đầu cuối đến đầu cuối. Router khởi tạo có thể, khi không nhận được Thông điệp Trạng thái Giao hàng trong khoảng thời gian dự kiến, thay đổi định tuyến đến Destination đầu xa, hoặc thực hiện các hành động khác.

2. **Một Database Store Message**, chứa LeaseSet cho Destination gốc, với Delivery Instructions chỉ định router của destination đầu xa. Bằng cách định kỳ gộp một LeaseSet, router đảm bảo rằng đầu xa sẽ có thể duy trì liên lạc. Nếu không thì đầu xa sẽ phải truy vấn một floodfill router để lấy mục cơ sở dữ liệu mạng, và tất cả LeaseSet sẽ phải được xuất bản lên cơ sở dữ liệu mạng, như đã giải thích trên [trang cơ sở dữ liệu mạng](/docs/specs/common-structures/).

Theo mặc định, các thông báo Delivery Status và Database Store Messages được gói lại khi LeaseSet cục bộ thay đổi, khi các Session Tags bổ sung được gửi, hoặc nếu các thông báo chưa được gói lại trong phút trước.

Rõ ràng là các thông điệp bổ sung hiện tại được gộp chung cho các mục đích cụ thể, và không phải là một phần của sơ đồ định tuyến đa năng.

Kể từ phiên bản 0.9.12, Delivery Status Message được bao bọc trong một Garlic Message khác bởi người gửi để nội dung được mã hóa và không thể nhìn thấy bởi các router trên đường trả về.

### Lưu trữ vào Cơ sở dữ liệu mạng Floodfill

Như đã giải thích trên [trang cơ sở dữ liệu mạng](/docs/specs/common-structures/), các leaseSet cục bộ được gửi tới các floodfill router trong một Database Store Message được bao bọc trong một Garlic Message để nó không hiển thị với outbound gateway của tunnel.

---

## Công việc tương lai

Cơ chế Garlic Message rất linh hoạt và cung cấp cấu trúc để triển khai nhiều loại phương thức phân phối mixnet. Cùng với tùy chọn delay chưa được sử dụng trong Delivery Instructions của tunnel message, một loạt các chiến lược phân lô, trì hoãn, trộn lẫn và định tuyến đa dạng đều có thể thực hiện được.

Cụ thể, có tiềm năng cho sự linh hoạt cao hơn nhiều tại điểm cuối tunnel đi ra. Các thông điệp có thể được định tuyến từ đó đến một trong số nhiều tunnel (do đó giảm thiểu các kết nối điểm-đến-điểm), hoặc multicast đến nhiều tunnel để dự phòng, hoặc streaming âm thanh và video.

Những thí nghiệm như vậy có thể xung đột với nhu cầu đảm bảo bảo mật và ẩn danh, chẳng hạn như giới hạn các đường dẫn định tuyến nhất định, hạn chế các loại thông điệp I2NP có thể được chuyển tiếp dọc theo các đường dẫn khác nhau, và thực thi thời gian hết hạn thông điệp nhất định.

Như một phần của mã hóa ElGamal/AES, một thông điệp garlic chứa một lượng dữ liệu đệm được người gửi chỉ định, cho phép người gửi thực hiện các biện pháp đối phó tích cực chống lại phân tích lưu lượng. Điều này hiện tại không được sử dụng, ngoài yêu cầu đệm đến bội số của 16 byte.

Mã hóa các thông điệp bổ sung đến và đi từ các [floodfill router](/docs/specs/common-structures/).

---

## Tài liệu tham khảo

- Thuật ngữ garlic routing lần đầu được đặt ra trong [luận văn Thạc sĩ](https://www.freehaven.net/papers.html) Free Haven của Roger Dingledine (tháng 6 năm 2000), xem Mục 8.1.1 được viết bởi [Michael J. Freedman](https://www.cs.princeton.edu/~mfreed/).
- [Onion Router Publications](https://www.onion-router.net/Publications.html)
- [Onion Routing (Wikipedia)](https://en.wikipedia.org/wiki/Onion_routing)
- [Garlic Routing (Wikipedia)](https://en.wikipedia.org/wiki/Garlic_routing)
- [Tor Project](https://www.torproject.org/)
- [Free Haven Anonbib](https://freehaven.net/anonbib/topic.html)
- Onion routing lần đầu được mô tả trong [Hiding Routing Information](https://www.onion-router.net/Publications/IH-1996.pdf) của David M. Goldschlag, Michael G. Reed, và Paul F. Syverson vào năm 1996.
