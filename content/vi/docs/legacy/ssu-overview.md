---
title: "Secure Semireliable UDP (SSU)"
description: "Giao thức truyền tải UDP gốc được sử dụng trước SSU2 (đã lỗi thời)"
slug: "ssu-overview"
aliases:
  - "/vi/udp"
  - "/vi/udp/"
lastUpdated: "2025-01"
accurateFor: "0.9.64"
---

**ĐÃ NGỪNG SỬ DỤNG** - SSU đã được thay thế bởi SSU2. Hỗ trợ SSU đã được loại bỏ khỏi i2pd trong phiên bản 2.44.0 (API 0.9.56) 2022-11. Hỗ trợ SSU đã được loại bỏ khỏi Java I2P trong phiên bản 2.4.0 (API 0.9.61) 2023-12.

SSU (còn được gọi là "UDP" trong hầu hết tài liệu I2P và giao diện người dùng) là một trong hai [transport](/docs/transport) được triển khai trong I2P. Transport còn lại là [NTCP2](/docs/specs/ntcp2). Hỗ trợ cho [NTCP](/docs/legacy/ntcp) đã bị loại bỏ.

SSU được giới thiệu trong phiên bản I2P 0.6. Trong cài đặt I2P tiêu chuẩn, router sử dụng cả NTCP và SSU cho các kết nối ra ngoài. SSU-over-IPv6 được hỗ trợ từ phiên bản 0.9.8.

SSU được gọi là "bán tin cậy" vì nó sẽ truyền lại liên tục các thông điệp chưa được xác nhận, nhưng chỉ đến một số lần tối đa. Sau đó, thông điệp sẽ bị loại bỏ.

## Dịch vụ SSU

Giống như giao thức vận chuyển NTCP, SSU cung cấp dịch vụ truyền dữ liệu điểm-điểm đáng tin cậy, được mã hóa, hướng kết nối. Riêng đối với SSU, nó cũng cung cấp các dịch vụ phát hiện IP và vượt qua NAT, bao gồm:

- Vượt qua NAT/Firewall hợp tác sử dụng [introducers](#introduction)
- Phát hiện IP cục bộ bằng cách kiểm tra các gói tin đến và [peer testing](#peerTesting)
- Truyền đạt trạng thái firewall và IP cục bộ, cũng như các thay đổi của chúng đến NTCP
- Truyền đạt trạng thái firewall và IP cục bộ, cũng như các thay đổi của chúng, đến router và giao diện người dùng

## Đặc tả Địa chỉ Router {#ra}

Các thuộc tính sau được lưu trữ trong cơ sở dữ liệu mạng.

- **Tên transport:** SSU
- **caps:** [B,C,4,6] [Xem bên dưới](#capabilities).
- **host:** IP (IPv4 hoặc IPv6).
  Địa chỉ IPv6 rút gọn (với "::") được cho phép.
  Có thể có hoặc không có mặt nếu bị firewall.
  Tên host trước đây được cho phép, nhưng đã không được khuyến khích từ phiên bản 0.9.32. Xem đề xuất 141.
- **iexp[0-2]:** Thời hạn hết hạn của introducer này.
  Chữ số ASCII, tính bằng giây kể từ epoch.
  Chỉ có mặt nếu bị firewall và các introducer là bắt buộc.
  Tùy chọn (ngay cả khi các thuộc tính khác cho introducer này có mặt).
  Từ phiên bản 0.9.30, đề xuất 133.
- **ihost[0-2]:** IP của introducer (IPv4 hoặc IPv6).
  Tên host trước đây được cho phép, nhưng đã không được khuyến khích từ phiên bản 0.9.32. Xem đề xuất 141.
  Địa chỉ IPv6 rút gọn (với "::") được cho phép.
  Chỉ có mặt nếu bị firewall và các introducer là bắt buộc.
  [Xem bên dưới](#introduction).
- **ikey[0-2]:** Khóa introduction Base 64 của introducer. [Xem bên dưới](#key).
  Chỉ có mặt nếu bị firewall và các introducer là bắt buộc.
  [Xem bên dưới](#introduction).
- **iport[0-2]:** Cổng của introducer 1024 - 65535.
  Chỉ có mặt nếu bị firewall và các introducer là bắt buộc.
  [Xem bên dưới](#introduction).
- **itag[0-2]:** Tag của introducer 1 - (2^32 - 1)
  Chữ số ASCII.
  Chỉ có mặt nếu bị firewall và các introducer là bắt buộc.
  [Xem bên dưới](#introduction).
- **key:** Khóa introduction Base 64. [Xem bên dưới](#key).
- **mtu:** Tùy chọn. Mặc định và tối đa là 1484. Tối thiểu là 620.
  Phải có mặt cho IPv6, nơi tối thiểu là 1280 và tối đa là 1488
  (tối đa là 1472 trước phiên bản 0.9.28).
  IPv6 MTU phải là bội số của 16.
  (IPv4 MTU + 4) phải là bội số của 16.
  [Xem bên dưới](#mtu).
- **port:** 1024 - 65535
  Có thể có hoặc không có mặt nếu bị firewall.

# Chi tiết giao thức

## Kiểm soát tắc nghẽn {#congestioncontrol}

Nhu cầu của SSU chỉ cần truyền tải bán tin cậy, hoạt động thân thiện với TCP, và khả năng thông lượng cao cho phép nhiều tự do trong việc kiểm soát tắc nghẽn. Thuật toán kiểm soát tắc nghẽn được nêu dưới đây nhằm mục đích vừa hiệu quả về băng thông vừa đơn giản để triển khai.

Các gói tin được lên lịch theo chính sách của router, cẩn thận không vượt quá khả năng truyền tải ra ngoài của router hoặc vượt quá khả năng đo được của peer từ xa. Khả năng đo được hoạt động theo hướng tương tự như slow start và congestion avoidance của TCP, với việc tăng cộng dồn khả năng gửi và giảm nhân khi gặp tắc nghẽn. Khác với TCP, các router có thể từ bỏ một số thông điệp sau một khoảng thời gian nhất định hoặc số lần truyền lại nhất định trong khi vẫn tiếp tục truyền các thông điệp khác.

Các kỹ thuật phát hiện tắc nghẽn cũng khác với TCP, vì mỗi thông điệp có định danh duy nhất và không tuần tự riêng, và mỗi thông điệp có kích thước giới hạn - tối đa là 32KB. Để truyền phản hồi này một cách hiệu quả đến người gửi, người nhận định kỳ bao gồm danh sách các định danh thông điệp đã được ACK hoàn toàn và cũng có thể bao gồm các bitfield cho các thông điệp được nhận một phần, trong đó mỗi bit đại diện cho việc nhận một fragment. Nếu các fragment trùng lặp đến, thông điệp nên được ACK lại, hoặc nếu thông điệp vẫn chưa được nhận hoàn toàn, bitfield nên được truyền lại với bất kỳ cập nhật mới nào.

Triển khai hiện tại không đệm các gói tin đến kích thước cụ thể nào, mà thay vào đó chỉ đặt một đoạn thông điệp duy nhất vào gói tin và gửi đi (cẩn thận không vượt quá MTU).

### MTU {#mtu}

Từ phiên bản router 0.8.12, hai giá trị MTU được sử dụng cho IPv4: 620 và 1484. Giá trị MTU được điều chỉnh dựa trên tỷ lệ phần trăm các gói tin được truyền lại.

Đối với cả hai giá trị MTU, điều mong muốn là (MTU % 16) == 12, để phần payload sau header IP/UDP 28 byte là bội số của 16 byte, phục vụ mục đích mã hóa.

Đối với giá trị MTU nhỏ, việc đóng gói một Variable Tunnel Build Message có kích thước 2646 byte một cách hiệu quả vào nhiều gói tin là điều mong muốn; với MTU 620 byte, nó vừa vặn với 5 gói tin một cách hoàn hảo.

Dựa trên các phép đo, 1492 phù hợp với hầu hết các thông điệp I2NP có kích thước nhỏ hợp lý (các thông điệp I2NP lớn hơn có thể lên đến 1900 đến 4500 byte, điều này dù sao cũng không thể phù hợp với MTU của mạng thực tế).

Các giá trị MTU là 608 và 1492 cho các phiên bản 0.8.9 - 0.8.11. MTU lớn là 1350 trước phiên bản 0.8.9.

Kích thước gói nhận tối đa là 1571 byte kể từ phiên bản 0.8.12. Đối với các phiên bản 0.8.9 - 0.8.11, kích thước này là 1535 byte. Trước phiên bản 0.8.9, kích thước này là 2048 byte.

Kể từ phiên bản 0.9.2, nếu MTU của giao diện mạng của router nhỏ hơn 1484, nó sẽ công bố thông tin đó trong cơ sở dữ liệu mạng, và các router khác sẽ tuân thủ thông tin này khi thiết lập kết nối.

Đối với IPv6, MTU tối thiểu là 1280. Header IPv6 IP/UDP có kích thước 48 byte, vì vậy chúng tôi sử dụng MTU với điều kiện (MTU % 16 == 0), điều này đúng với 1280. MTU tối đa của IPv6 là 1488. (tối đa là 1472 trước phiên bản 0.9.28).

### Giới hạn Kích thước Thông điệp {#max}

Trong khi kích thước thông điệp tối đa theo danh nghĩa là 32KB, giới hạn thực tế lại khác. Giao thức giới hạn số lượng phân đoạn ở 7 bit, tức là 128. Tuy nhiên, việc triển khai hiện tại giới hạn mỗi thông điệp tối đa 64 phân đoạn, đủ cho 64 * 534 = 33.3 KB khi sử dụng MTU 608. Do chi phí phụ trội cho leaseSet được gói và session key, giới hạn thực tế ở tầng ứng dụng thấp hơn khoảng 6KB, tức là khoảng 26KB. Cần có thêm công việc để nâng giới hạn vận chuyển UDP lên trên 32KB. Đối với các kết nối sử dụng MTU lớn hơn, các thông điệp lớn hơn có thể thực hiện được.

## Thời gian chờ không hoạt động

Thời gian chờ nhàn rỗi và việc đóng kết nối tùy thuộc vào quyết định của từng điểm cuối và có thể khác nhau. Triển khai hiện tại giảm thời gian chờ khi số lượng kết nối tiến gần đến mức tối đa đã cấu hình, và tăng thời gian chờ khi số lượng kết nối thấp. Thời gian chờ tối thiểu được khuyến nghị là hai phút hoặc nhiều hơn, và thời gian chờ tối đa được khuyến nghị là mười phút hoặc nhiều hơn.

## Khóa {#keys}

Tất cả mã hóa được sử dụng là AES256/CBC với khóa 32 byte và IV 16 byte. Khi Alice khởi tạo phiên với Bob, các khóa MAC và phiên được thương lượng như một phần của trao đổi DH, và sau đó được sử dụng tương ứng cho HMAC và mã hóa. Trong quá trình trao đổi DH, introKey có thể biết công khai của Bob được sử dụng cho MAC và mã hóa.

Cả thông điệp ban đầu và phản hồi tiếp theo đều sử dụng introKey của người phản hồi (Bob) - người phản hồi không cần biết introKey của người yêu cầu (Alice). Khóa ký DSA được Bob sử dụng nên được Alice biết trước khi cô ấy liên hệ với anh ta, mặc dù khóa DSA của Alice có thể chưa được Bob biết.

Khi nhận được tin nhắn, bên nhận sẽ kiểm tra địa chỉ IP và cổng "from" với tất cả các phiên đã thiết lập - nếu có khớp, các khóa MAC của phiên đó sẽ được kiểm tra trong HMAC. Nếu không có khóa nào xác minh được hoặc nếu không có địa chỉ IP nào khớp, bên nhận sẽ thử introKey của họ trong MAC. Nếu không xác minh được, gói tin sẽ bị loại bỏ. Nếu xác minh được, gói tin sẽ được diễn giải theo loại tin nhắn, tuy nhiên nếu bên nhận đang quá tải, gói tin vẫn có thể bị loại bỏ.

Nếu Alice và Bob đã thiết lập một phiên làm việc, nhưng Alice mất khóa vì lý do nào đó và cô ấy muốn liên lạc với Bob, cô ấy có thể bất cứ lúc nào đơn giản thiết lập một phiên mới thông qua SessionRequest và các thông điệp liên quan. Nếu Bob đã mất khóa nhưng Alice không biết điều đó, trước tiên cô ấy sẽ cố gắng thúc đẩy anh ấy trả lời, bằng cách gửi một DataMessage với cờ wantReply được đặt, và nếu Bob liên tục không trả lời, cô ấy sẽ giả định khóa đã mất và thiết lập lại một khóa mới.

Đối với thỏa thuận khóa DH, nhóm MODP 2048bit [RFC3526](http://www.faqs.org/rfcs/rfc3526.html) (#14) được sử dụng:

```
  p = 2^2048 - 2^1984 - 1 + 2^64 * { [2^1918 pi] + 124476 }
  g = 2
```
Đây là cùng một p và g được sử dụng cho [ElGamal encryption](/docs/specs/cryptography#elgamal) của I2P.

## Ngăn chặn Tấn công Lặp lại {#replay}

Việc ngăn chặn replay tại tầng SSU xảy ra bằng cách từ chối các gói tin có timestamp quá cũ hoặc những gói tin tái sử dụng IV. Để phát hiện các IV trùng lặp, một chuỗi các bộ lọc Bloom được sử dụng để "phân hủy" định kỳ sao cho chỉ những IV được thêm gần đây mới được phát hiện.

Các messageId được sử dụng trong DataMessages được định nghĩa tại các tầng trên tầng truyền tải SSU và được truyền qua một cách minh bạch. Các ID này không theo thứ tự cụ thể nào - thực tế, chúng có khả năng hoàn toàn ngẫu nhiên. Tầng SSU không thực hiện bất kỳ cố gắng ngăn chặn tái sử dụng messageId nào - các tầng cao hơn nên tính đến điều này.

## Địa chỉ {#addressing}

Để liên lạc với một peer SSU, cần có một trong hai bộ thông tin sau: địa chỉ trực tiếp, dành cho trường hợp peer có thể truy cập công khai, hoặc địa chỉ gián tiếp, để sử dụng bên thứ ba giới thiệu peer đó. Không có giới hạn về số lượng địa chỉ mà một peer có thể có.

```
    Direct: host, port, introKey, options
  Indirect: tag, relayhost, port, relayIntroKey, targetIntroKey, options
```
Mỗi địa chỉ cũng có thể hiển thị một loạt các tùy chọn - các khả năng đặc biệt của peer cụ thể đó. Để xem danh sách các khả năng có sẵn, hãy xem [bên dưới](#capabilities).

Các địa chỉ, tùy chọn và khả năng được công bố trong [cơ sở dữ liệu mạng](/docs/overview/network-database).

## Thiết Lập Phiên Trực Tiếp {#direct}

Thiết lập phiên trực tiếp được sử dụng khi không cần bên thứ ba để vượt qua NAT. Trình tự thông điệp như sau:

### Thiết lập Kết nối (Trực tiếp) {#establishDirect}

Alice kết nối trực tiếp với Bob. IPv6 được hỗ trợ từ phiên bản 0.9.8.

```
        Alice                         Bob
    SessionRequest --------------------->
          <--------------------- SessionCreated
    SessionConfirmed ------------------->
          <--------------------- DeliveryStatusMessage
          <--------------------- DatabaseStoreMessage
    DatabaseStoreMessage --------------->
    Data <--------------------------> Data
```
Sau khi nhận được thông báo SessionConfirmed, Bob gửi một [thông báo DeliveryStatus](/docs/specs/i2np#msg_DeliveryStatus) nhỏ để xác nhận. Trong thông báo này, ID thông báo 4 byte được đặt thành một số ngẫu nhiên, và "thời gian đến" 8 byte được đặt thành ID mạng hiện tại, là 2 (tức là 0x0000000000000002).

Sau khi thông điệp trạng thái được gửi, các peer thường trao đổi [thông điệp DatabaseStore](/docs/specs/i2np#msg_DatabaseStore) chứa [RouterInfos](/docs/specs/common-structures#struct_RouterInfo) của họ, tuy nhiên, điều này không bắt buộc.

Có vẻ như loại thông điệp trạng thái hoặc nội dung của nó không quan trọng. Nó ban đầu được thêm vào vì thông điệp DatabaseStore bị trễ vài giây; vì store hiện tại được gửi ngay lập tức, có lẽ thông điệp trạng thái có thể được loại bỏ.

## Giới thiệu {#introduction}

Introduction keys được cung cấp thông qua một kênh bên ngoài (network database), nơi mà chúng theo truyền thống đã giống hệt với router Hash cho đến phiên bản 0.9.47, nhưng có thể là ngẫu nhiên kể từ phiên bản 0.9.48. Chúng phải được sử dụng khi thiết lập một session key. Đối với địa chỉ gián tiếp, peer phải đầu tiên liên hệ với relayhost và yêu cầu họ giới thiệu với peer được biết đến tại relayhost đó dưới tag đã cho. Nếu có thể, relayhost sẽ gửi một tin nhắn đến peer được địa chỉ hóa để yêu cầu họ liên hệ với peer đang yêu cầu, và cũng cung cấp cho peer đang yêu cầu IP và port mà peer được địa chỉ hóa đang ở. Ngoài ra, peer đang thiết lập kết nối phải đã biết trước các public keys của peer mà họ đang kết nối tới (nhưng không cần thiết với bất kỳ relay peer trung gian nào).

Việc thiết lập phiên kết nối gián tiếp thông qua sự giới thiệu của bên thứ ba là cần thiết để vượt qua NAT một cách hiệu quả. Charlie, một router đằng sau NAT hoặc firewall không cho phép các gói UDP đến không được yêu cầu, trước tiên liên lạc với một vài peer, chọn một số để làm introducer (người giới thiệu). Mỗi peer này (Bob, Bill, Betty, v.v.) cung cấp cho Charlie một introduction tag - một số ngẫu nhiên 4 byte - sau đó Charlie công khai để mọi người có thể liên lạc với anh ta. Alice, một router có được các phương thức liên lạc đã công bố của Charlie, trước tiên gửi một gói RelayRequest đến một hoặc nhiều introducer, yêu cầu mỗi người giới thiệu cô với Charlie (cung cấp introduction tag để nhận dạng Charlie). Bob sau đó chuyển tiếp một gói RelayIntro đến Charlie bao gồm IP công khai và số cổng của Alice, rồi gửi lại cho Alice một gói RelayResponse chứa IP công khai và số cổng của Charlie. Khi Charlie nhận được gói RelayIntro, anh ta gửi một gói ngẫu nhiên nhỏ đến IP và cổng của Alice (tạo lỗ hổng trong NAT/firewall của mình), và khi Alice nhận được gói RelayResponse của Bob, cô bắt đầu một phiên thiết lập kết nối đầy đủ mới với IP và cổng được chỉ định.

### Thiết Lập Kết Nối (Gián Tiếp Sử Dụng Introducer) {#establishIndirect}

Alice trước tiên kết nối với introducer Bob, người sẽ chuyển tiếp yêu cầu đến Charlie.

```
        Alice                         Bob                  Charlie
    RelayRequest ---------------------->
         <-------------- RelayResponse    RelayIntro ----------->
         <-------------------------------------------- HolePunch (data ignored)
    SessionRequest -------------------------------------------->
         <-------------------------------------------- SessionCreated
    SessionConfirmed ------------------------------------------>
         <-------------------------------------------- DeliveryStatusMessage
         <-------------------------------------------- DatabaseStoreMessage
    DatabaseStoreMessage -------------------------------------->
    Data <--------------------------------------------------> Data
```
Sau khi hole punch, phiên được thiết lập giữa Alice và Charlie như trong một thiết lập trực tiếp.

### Ghi chú về IPv6

IPv6 được hỗ trợ từ phiên bản 0.9.8. Các địa chỉ relay được công bố có thể là IPv4 hoặc IPv6, và giao tiếp Alice-Bob có thể thông qua IPv4 hoặc IPv6. Từ bản phát hành 0.9.49, giao tiếp Bob-Charlie và Alice-Charlie chỉ thông qua IPv4. Relay cho IPv6 được hỗ trợ từ bản phát hành 0.9.50. Xem đặc tả kỹ thuật để biết chi tiết.

Mặc dù đặc tả đã được thay đổi từ phiên bản 0.9.8, việc giao tiếp Alice-Bob qua IPv6 thực sự chưa được hỗ trợ cho đến phiên bản 0.9.50. Các phiên bản router Java trước đó đã sai lầm khi công bố khả năng 'C' cho địa chỉ IPv6, mặc dù chúng không thực sự hoạt động như một introducer qua IPv6. Do đó, các router chỉ nên tin tưởng khả năng 'C' trên địa chỉ IPv6 nếu phiên bản router là 0.9.50 hoặc cao hơn.

## Kiểm tra Peer {#peerTesting}

Việc tự động hóa kiểm tra khả năng tiếp cận hợp tác cho các peer được thực hiện bởi một chuỗi các thông điệp PeerTest. Với việc thực thi đúng cách, một peer sẽ có thể xác định khả năng tiếp cận của chính nó và có thể cập nhật hành vi của mình cho phù hợp. Quá trình kiểm tra khá đơn giản:

```
        Alice                  Bob                  Charlie
    PeerTest ------------------->
                             PeerTest-------------------->
                                <-------------------PeerTest
         <-------------------PeerTest
         <------------------------------------------PeerTest
    PeerTest------------------------------------------>
         <------------------------------------------PeerTest
```
Mỗi thông điệp PeerTest đều mang một nonce xác định chuỗi kiểm tra, được khởi tạo bởi Alice. Nếu Alice không nhận được một thông điệp cụ thể mà cô ấy mong đợi, cô ấy sẽ truyền lại tương ứng, và dựa trên dữ liệu nhận được hoặc các thông điệp bị thiếu, cô ấy sẽ biết khả năng kết nối của mình. Các trạng thái kết thúc khác nhau có thể đạt được như sau:

- Nếu cô ấy không nhận được phản hồi từ Bob, cô ấy sẽ truyền lại
  đến một số lần nhất định, nhưng nếu không có phản hồi nào đến,
  cô ấy sẽ biết rằng firewall hoặc NAT của mình đã bị cấu hình sai,
  từ chối tất cả các gói UDP đến ngay cả khi phản hồi trực tiếp cho
  một gói đi ra. Ngoài ra, Bob có thể đã ngừng hoạt động hoặc không thể
  khiến Charlie phản hồi.

- Nếu Alice không nhận được thông điệp PeerTest với
  nonce mong đợi từ bên thứ ba (Charlie), cô ấy sẽ truyền lại
  yêu cầu ban đầu gửi cho Bob lên đến một số lần nhất định, ngay cả
  khi cô ấy đã nhận được phản hồi của Bob. Nếu thông điệp đầu tiên của Charlie
  vẫn không đến được nhưng thông điệp của Bob thì có, cô ấy biết rằng mình đang
  đằng sau NAT hoặc tường lửa đang từ chối các nỗ lực kết nối không được yêu cầu
  và việc chuyển tiếp cổng không hoạt động đúng cách (IP và cổng mà Bob
  cung cấp lẽ ra phải được chuyển tiếp).

- Nếu Alice nhận được thông điệp PeerTest của Bob và cả hai thông điệp PeerTest của Charlie nhưng các số IP và port được bao gồm trong thông điệp thứ hai của Bob và Charlie không khớp, cô ấy biết rằng mình đang đứng sau một symmetric NAT, viết lại tất cả các gói tin gửi đi của cô ấy với các port 'from' khác nhau cho mỗi peer được liên lạc. Cô ấy sẽ cần phải chuyển tiếp một port một cách rõ ràng và luôn giữ port đó được mở cho kết nối từ xa, bỏ qua việc khám phá port tiếp theo.

- Nếu Alice nhận được tin nhắn đầu tiên của Charlie nhưng không nhận được tin nhắn thứ hai,
  cô ấy sẽ truyền lại tin nhắn PeerTest của mình cho Charlie tối đa một
  số lần nhất định, nhưng nếu không nhận được phản hồi thì cô ấy biết
  rằng Charlie hoặc bị nhầm lẫn hoặc không còn trực tuyến nữa.

Alice nên chọn Bob một cách tùy ý từ các peer đã biết có vẻ có khả năng tham gia vào peer tests. Bob lần lượt nên chọn Charlie một cách tùy ý từ các peer mà anh ta biết có vẻ có khả năng tham gia vào peer tests và đang ở trên một IP khác với cả Bob và Alice. Nếu điều kiện lỗi đầu tiên xảy ra (Alice không nhận được tin nhắn PeerTest từ Bob), Alice có thể quyết định chỉ định một peer mới làm Bob và thử lại với một nonce khác.

Khóa giới thiệu của Alice được bao gồm trong tất cả các tin nhắn PeerTest để Charlie có thể liên lạc với cô ấy mà không cần biết thêm bất kỳ thông tin nào khác. Kể từ phiên bản 0.9.15, Alice phải có một phiên kết nối đã thiết lập với Bob để ngăn chặn các cuộc tấn công giả mạo. Alice không được có phiên kết nối đã thiết lập với Charlie để peer test có hiệu lực. Alice có thể tiếp tục thiết lập phiên kết nối với Charlie, nhưng điều này không bắt buộc.

### Ghi chú IPv6

Từ phiên bản 0.9.26, chỉ hỗ trợ kiểm tra địa chỉ IPv4. Chỉ hỗ trợ kiểm tra địa chỉ IPv4. Do đó, tất cả giao tiếp Alice-Bob và Alice-Charlie phải thông qua IPv4. Tuy nhiên, giao tiếp Bob-Charlie có thể thông qua IPv4 hoặc IPv6. Địa chỉ của Alice, khi được chỉ định trong thông điệp PeerTest, phải là 4 byte. Từ phiên bản 0.9.27, hỗ trợ kiểm tra địa chỉ IPv6, và giao tiếp Alice-Bob và Alice-Charlie có thể thông qua IPv6, nếu Bob và Charlie cho biết hỗ trợ với khả năng 'B' trong địa chỉ IPv6 được công bố của họ. Xem [Đề xuất 126](/spec/proposals/126-ipv6-peer-testing) để biết chi tiết.

Trước phiên bản 0.9.50, Alice gửi yêu cầu đến Bob sử dụng một phiên hiện có qua giao thức vận chuyển (IPv4 hoặc IPv6) mà cô ấy muốn kiểm tra. Khi Bob nhận được yêu cầu từ Alice qua IPv4, Bob phải chọn một Charlie quảng cáo địa chỉ IPv4. Khi Bob nhận được yêu cầu từ Alice qua IPv6, Bob phải chọn một Charlie quảng cáo địa chỉ IPv6. Việc giao tiếp thực tế giữa Bob-Charlie có thể thông qua IPv4 hoặc IPv6 (tức là độc lập với loại địa chỉ của Alice).

Kể từ phiên bản 0.9.50, nếu thông điệp được gửi qua IPv6 cho một bài kiểm tra peer IPv4, hoặc (kể từ phiên bản 0.9.50) qua IPv4 cho một bài kiểm tra peer IPv6, Alice phải bao gồm địa chỉ introduction và port của mình.

Xem [Đề xuất 158](/spec/proposals/158) để biết chi tiết.

## Cửa sổ truyền tải, ACK và truyền lại {#acks}

Thông điệp DATA có thể chứa các ACK của các thông điệp đầy đủ và các ACK một phần của các fragment riêng lẻ của một thông điệp. Xem phần thông điệp dữ liệu của [trang đặc tả giao thức](/docs/legacy/ssu) để biết chi tiết.

Chi tiết về các chiến lược windowing, ACK và retransmission không được chỉ định ở đây. Xem mã Java để biết implementation hiện tại. Trong giai đoạn thiết lập kết nối và cho việc kiểm tra peer, các router nên implement exponential backoff cho retransmission. Đối với kết nối đã được thiết lập, các router nên implement một transmission window có thể điều chỉnh, ước tính RTT và timeout, tương tự như TCP hoặc [streaming](/docs/api/streaming). Xem mã để biết các tham số initial, min và max.

## Bảo mật {#security}

Địa chỉ nguồn UDP tất nhiên có thể bị giả mạo. Ngoài ra, các IP và cổng chứa bên trong các thông điệp SSU cụ thể (RelayRequest, RelayResponse, RelayIntro, PeerTest) có thể không hợp lệ. Đồng thời, một số hành động và phản hồi có thể cần được giới hạn tốc độ.

Các chi tiết của việc xác thực không được chỉ định ở đây. Các nhà phát triển nên thêm các biện pháp bảo vệ khi thích hợp.

## Khả năng của Peer {#capabilities}

Một hoặc nhiều khả năng có thể được công bố trong tùy chọn "caps". Các khả năng có thể theo thứ tự bất kỳ, nhưng "BC46" là thứ tự được khuyến nghị, để đảm bảo tính nhất quán giữa các triển khai.

**B** : Nếu địa chỉ peer chứa khả năng 'B', có nghĩa là họ sẵn sàng và có thể tham gia vào các bài kiểm tra peer với vai trò 'Bob' hoặc 'Charlie'. Từ phiên bản 0.9.26 trở về trước, kiểm tra peer không được hỗ trợ cho địa chỉ IPv6, và khả năng 'B', nếu có mặt cho địa chỉ IPv6, phải được bỏ qua. Từ phiên bản 0.9.27, kiểm tra peer được hỗ trợ cho địa chỉ IPv6, và sự hiện diện hoặc vắng mặt của khả năng 'B' trong địa chỉ IPv6 chỉ ra khả năng hỗ trợ thực tế (hoặc thiếu hỗ trợ).

**C** : Nếu địa chỉ peer chứa khả năng 'C', có nghĩa là họ sẵn sàng và có thể phục vụ như một introducer thông qua địa chỉ đó - đóng vai trò là introducer Bob cho một Charlie khác không thể tiếp cận được. Trước phiên bản 0.9.50, các Java router đã sai lầm khi xuất bản khả năng 'C' cho các địa chỉ IPv6, mặc dù IPv6 introducers chưa được triển khai đầy đủ. Do đó, các router nên giả định rằng các phiên bản trước 0.9.50 không thể hoạt động như một introducer qua IPv6, ngay cả khi khả năng 'C' được quảng cáo.

**4** : Kể từ phiên bản 0.9.50, chỉ ra khả năng IPv4 outbound. Nếu một IP được công bố trong trường host, khả năng này không cần thiết. Nếu đây là một địa chỉ với introducers cho IPv4 introductions, '4' nên được bao gồm. Nếu router bị ẩn, '4' và '6' có thể được kết hợp trong một địa chỉ duy nhất.

**6** : Kể từ phiên bản 0.9.50, biểu thị khả năng IPv6 outbound. Nếu một IP được công bố trong trường host, khả năng này không cần thiết. Nếu đây là một địa chỉ có introducers cho IPv6 introductions, '6' nên được bao gồm (hiện tại chưa được hỗ trợ). Nếu router bị ẩn, '4' và '6' có thể được kết hợp trong một địa chỉ duy nhất.

# Công việc Tương lai {#future}

Lưu ý: Những vấn đề này sẽ được giải quyết trong quá trình phát triển SSU2.

- Phân tích hiệu suất SSU hiện tại, bao gồm đánh giá việc điều chỉnh kích thước cửa sổ và các tham số khác, cùng với việc điều chỉnh triển khai giao thức để cải thiện hiệu suất, là một chủ đề cho công việc tương lai.

- Việc triển khai hiện tại liên tục gửi các xác nhận cho cùng một gói tin,
  điều này làm tăng overhead một cách không cần thiết.

- Giá trị MTU nhỏ mặc định là 620 cần được phân tích và có thể tăng lên.
  Chiến lược điều chỉnh MTU hiện tại cần được đánh giá.
  Liệu một gói tin streaming lib 1730-byte có vừa trong 3 gói tin SSU nhỏ không? Có lẽ là không.

- Giao thức nên được mở rộng để trao đổi MTU trong quá trình thiết lập.

- Rekeying hiện tại chưa được triển khai và sẽ không bao giờ được triển khai.

- Việc sử dụng tiềm năng của các trường 'challenge' trong RelayIntro và RelayResponse,
  và việc sử dụng trường padding trong SessionRequest và SessionCreated, chưa được ghi chép.

- Một bộ các kích thước gói tin cố định có thể phù hợp để ẩn giấu thêm việc phân mảnh dữ liệu khỏi các đối thủ bên ngoài, nhưng việc đệm tunnel, garlic và đầu cuối đến đầu cuối sẽ đủ cho hầu hết các nhu cầu cho đến lúc đó.

- Thời gian đăng nhập trong SessionCreated và SessionConfirmed có vẻ không được sử dụng hoặc chưa được xác minh.

# Đặc tả {#spec}

[Hiện tại trên trang đặc tả SSU](/docs/legacy/ssu).
