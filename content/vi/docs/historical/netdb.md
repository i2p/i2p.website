---
title: "Thảo luận về Cơ sở Dữ liệu Mạng"
description: "Ghi chú lịch sử về floodfill, các thí nghiệm Kademlia, và điều chỉnh tương lai cho netDb"
slug: "netdb"
aliases:
  - "/vi/docs/legacy/netdb"
  - "/vi/docs/legacy/netdb/"
  - "/vi/netdb_discussion"
  - "/vi/netdb_discussion/"
lastUpdated: "2008-03"
accurateFor: "0.7"
---

LƯU Ý: Phần sau đây là thảo luận về lịch sử triển khai netDb và không phải là thông tin hiện tại. Xem [trang netDb chính](/docs/overview/network-database) để có tài liệu hiện tại.

## Lịch sử {#status}

netDb được phân phối bằng một kỹ thuật đơn giản gọi là "floodfill". Từ lâu, netDb cũng đã sử dụng Kademlia DHT như một thuật toán dự phòng. Tuy nhiên, nó không hoạt động tốt trong ứng dụng của chúng tôi và đã bị vô hiệu hóa hoàn toàn trong phiên bản 0.6.1.20.

*(Chuyển thể từ một bài đăng của jrandom trong Syndie cũ, ngày 26 tháng 11, 2005)*

Floodfill netDb thực sự chỉ là một biện pháp đơn giản và có thể tạm thời, sử dụng thuật toán đơn giản nhất có thể - gửi dữ liệu đến một peer trong floodfill netDb, đợi 10 giây, chọn ngẫu nhiên một peer trong netDb và yêu cầu họ gửi mục tin để được gửi, xác minh việc chèn / phân phối đúng cách của nó. Nếu peer xác minh không trả lời, hoặc họ không có mục tin đó, bên gửi sẽ lặp lại quy trình. Khi peer trong floodfill netDb nhận được một netDb store từ một peer không có trong floodfill netDb, họ sẽ gửi nó đến tất cả các peer trong floodfill netDb.

Tại một thời điểm, chức năng tìm kiếm/lưu trữ Kademlia vẫn còn hoạt động. Các peer coi các floodfill peer luôn 'gần hơn' với mọi khóa so với bất kỳ peer nào không tham gia vào netDb. Chúng tôi đã quay trở lại sử dụng Kademlia netDb nếu các floodfill peer gặp sự cố vì lý do này hay lý do khác. Tuy nhiên, sau đó Kademlia đã bị vô hiệu hóa hoàn toàn (xem bên dưới).

Gần đây hơn, Kademlia đã được tái giới thiệu một phần vào cuối năm 2009, như một cách để giới hạn kích thước của netDb mà mỗi floodfill router phải lưu trữ.

### Giới thiệu về Thuật toán Floodfill

Floodfill được giới thiệu trong phiên bản 0.6.0.4, giữ Kademlia làm thuật toán dự phòng.

*(Chuyển thể từ các bài đăng của jrandom trong Syndie cũ, ngày 26 tháng 11 năm 2005)*

Như tôi đã thường nói, tôi không đặc biệt gắn bó với bất kỳ công nghệ cụ thể nào - điều quan trọng với tôi là thứ gì sẽ mang lại kết quả. Trong khi tôi đã làm việc với nhiều ý tưởng netDb khác nhau trong vài năm qua, các vấn đề chúng ta đã đối mặt trong vài tuần vừa qua đã đưa một số trong số chúng đến hồi kết. Trên mạng thực, với hệ số dư thừa netDb được đặt ở 4 peer (nghĩa là chúng ta tiếp tục gửi một mục đến các peer mới cho đến khi 4 trong số chúng xác nhận rằng chúng đã nhận được) và thời gian chờ mỗi peer được đặt ở 4 lần thời gian phản hồi trung bình của peer đó, chúng ta **vẫn** nhận được trung bình 40-60 peer được gửi đến trước khi 4 peer ACK việc lưu trữ. Điều đó có nghĩa là gửi nhiều hơn 36-56 lần so với số lượng thông báo nên được gửi đi, mỗi thông báo sử dụng tunnel và do đó đi qua 2-4 liên kết. Hơn nữa, giá trị đó bị lệch nặng, vì số lượng peer trung bình được gửi đến trong một lần lưu trữ 'thất bại' (nghĩa là ít hơn 4 người ACK thông báo sau 60 giây gửi thông báo ra) nằm trong khoảng 130-160 peer.

Điều này thật điên rồ, đặc biệt là đối với một mạng chỉ có khoảng 250 peer trên đó.

Câu trả lời đơn giản nhất là nói "ừm, dĩ nhiên rồi jrandom, nó bị hỏng. sửa nó đi", nhưng điều đó không thực sự đi đến cốt lõi của vấn đề. Theo hướng một nỗ lực hiện tại khác, có khả năng chúng ta có một số lượng đáng kể các vấn đề mạng do các tuyến đường bị hạn chế - các peer không thể giao tiếp với một số peer khác, thường do vấn đề NAT hoặc tường lửa. Nếu, giả sử, K peer gần nhất với một mục netDb cụ thể nằm sau một 'tuyến đường bị hạn chế' sao cho thông điệp lưu trữ netDb có thể đến được chúng nhưng thông điệp tìm kiếm netDb của peer khác thì không thể, thì mục đó về cơ bản sẽ không thể tiếp cận được. Theo dõi các hướng đó xa hơn một chút và xem xét thực tế rằng một số tuyến đường bị hạn chế sẽ được tạo ra với ý định thù địch, rõ ràng là chúng ta sẽ phải xem xét kỹ hơn một giải pháp netDb dài hạn.

Có một vài giải pháp thay thế, nhưng có hai giải pháp đặc biệt đáng đề cập. Đầu tiên là đơn giản chạy netDb như một Kademlia DHT sử dụng một tập con của toàn bộ mạng, trong đó tất cả các peer đó đều có thể truy cập từ bên ngoài. Các peer không tham gia vào netDb vẫn truy vấn những peer đó nhưng chúng không nhận các thông điệp netDb store hoặc lookup không được yêu cầu. Việc tham gia vào netDb sẽ vừa tự chọn vừa do người dùng loại bỏ - các router sẽ chọn có công bố một cờ hiệu trong routerInfo của chúng để tuyên bố liệu chúng có muốn tham gia hay không, trong khi mỗi router chọn những peer nào nó muốn coi như một phần của netDb (các peer công bố cờ hiệu đó nhưng không bao giờ cung cấp dữ liệu hữu ích nào sẽ bị bỏ qua, về cơ bản loại bỏ chúng khỏi netDb).

Một lựa chọn khác là quay về quá khứ, theo tư duy DTSTTCPW (Do The Simplest Thing That Could Possibly Work - Làm Điều Đơn Giản Nhất Có Thể Hoạt Động) - một floodfill netDb, nhưng giống như lựa chọn ở trên, chỉ sử dụng một tập con của toàn bộ mạng. Khi người dùng muốn xuất bản một mục vào floodfill netDb, họ chỉ cần gửi nó đến một trong những router tham gia, chờ ACK, và sau đó 30 giây sau, truy vấn một người tham gia ngẫu nhiên khác trong floodfill netDb để xác minh rằng nó đã được phân phối đúng cách. Nếu đã được phân phối, tuyệt vời, và nếu chưa, chỉ cần lặp lại quy trình. Khi một floodfill router nhận được lưu trữ netDb, họ ACK ngay lập tức và xếp hàng đợi việc lưu trữ netDb đến tất cả các netDb peer đã biết. Khi một floodfill router nhận được truy vấn netDb, nếu họ có dữ liệu, họ trả lời với dữ liệu đó, nhưng nếu không có, họ trả lời với các hash cho, giả sử, 20 peer khác trong floodfill netDb.

Nhìn từ góc độ kinh tế mạng, floodfill netDb khá giống với netDb broadcast gốc, ngoại trừ việc chi phí để xuất bản một mục được gánh chủ yếu bởi các peer trong netDb, thay vì bởi nhà xuất bản. Mở rộng điều này thêm một chút và xem netDb như một hộp đen, chúng ta có thể thấy tổng băng thông mà netDb yêu cầu là:

```
recvKBps = N * (L + 1) * (1 + F) * (1 + R) * S / T
```
trong đó:

```
N = number of routers in the entire network
L = average number of client destinations on each router
    (+1 for the routerInfo)
F = tunnel failure percentage
R = tunnel rebuild period, as a fraction of the tunnel lifetime
S = average netDb entry size
T = tunnel lifetime
```
Thay vào một số giá trị:

```
recvKBps = 1000 * (5 + 1) * (1 + 0.05) * (1 + 0.2) * 2KB / 10m
         = 25.2KBps
```
Điều này, theo đó, tăng tuyến tính với N (tại 100.000 peer, netDb phải có khả năng xử lý các thông điệp netDb store với tổng lưu lượng 2.5MBps, hoặc, tại 300 peer, 7.6KBps).

Trong khi floodfill netDb sẽ có mỗi thành viên tham gia netDb chỉ nhận được một phần nhỏ các bản lưu trữ netDb do client tạo ra một cách trực tiếp, cuối cùng tất cả đều sẽ nhận được tất cả các mục, do đó tất cả các liên kết của họ phải có khả năng xử lý toàn bộ recvKBps. Đổi lại, tất cả họ sẽ cần gửi `(recvKBps/sizeof(netDb)) * (sizeof(netDb)-1)` để giữ cho các peer khác đồng bộ.

Một floodfill netDb sẽ không yêu cầu việc định tuyến tunnel cho hoạt động netDb hoặc bất kỳ lựa chọn đặc biệt nào về các mục nào nó có thể trả lời 'an toàn', vì giả định cơ bản là tất cả đều lưu trữ mọi thứ. Ồ, và về việc sử dụng đĩa netDb cần thiết, nó vẫn khá nhỏ đối với bất kỳ máy hiện đại nào, yêu cầu khoảng 11MB cho mỗi 1000 peer `(N * (L + 1) * S)`.

Kademlia netDb sẽ giảm những con số này, lý tưởng là đưa chúng xuống K trên M lần giá trị của chúng, với K = hệ số dự phòng và M là số lượng router trong netDb (ví dụ: 5/100, cho recvKBps là 126KBps và 536MB với 100,000 router). Tuy nhiên, nhược điểm của Kademlia netDb là độ phức tạp tăng cao trong việc vận hành an toàn trong môi trường thù địch.

Điều tôi đang nghĩ đến bây giờ là đơn giản triển khai và deploy một floodfill netDb trong mạng lưới trực tuyến hiện có của chúng ta, để các peer muốn sử dụng nó có thể chọn ra các peer khác được đánh dấu là thành viên và truy vấn chúng thay vì truy vấn các peer netDb Kademlia truyền thống. Yêu cầu băng thông và đĩa cứng ở giai đoạn này đủ nhỏ (7.6KBps và 3MB dung lượng đĩa) và nó sẽ loại bỏ hoàn toàn netDb khỏi kế hoạch debug - các vấn đề còn lại cần được giải quyết sẽ do một nguyên nhân không liên quan đến netDb.

Các peer sẽ được chọn như thế nào để publish flag (cờ hiệu) cho biết họ là một phần của floodfill netDb? Ban đầu, việc này có thể được thực hiện thủ công như một tùy chọn cấu hình nâng cao (bị bỏ qua nếu router không thể xác minh khả năng tiếp cận bên ngoài của nó). Nếu có quá nhiều peer đặt flag đó, các thành viên netDb sẽ chọn những peer nào để loại bỏ như thế nào? Một lần nữa, ban đầu việc này có thể được thực hiện thủ công như một tùy chọn cấu hình nâng cao (sau khi loại bỏ các peer không thể tiếp cận được). Làm thế nào để tránh việc phân mảnh netDb? Bằng cách để các router xác minh rằng netDb đang thực hiện flood fill đúng cách bằng cách truy vấn K peer netDb ngẫu nhiên. Các router không tham gia vào netDb sẽ khám phá các router mới để tạo tunnel như thế nào? Có lẽ việc này có thể được thực hiện bằng cách gửi một truy vấn netDb lookup cụ thể để router netDb sẽ phản hồi không phải với các peer trong netDb, mà với các peer ngẫu nhiên bên ngoài netDb.

NetDb của I2P rất khác so với các DHT chịu tải truyền thống - nó chỉ chứa metadata mạng, không chứa bất kỳ payload thực tế nào, đó là lý do tại sao ngay cả một netDb sử dụng thuật toán floodfill vẫn có thể duy trì lượng dữ liệu tùy ý từ I2P Site/IRC/bt/mail/syndie/etc. Chúng ta thậm chí có thể thực hiện một số tối ưu hóa khi I2P phát triển để phân phối tải đó xa hơn một chút (có thể truyền các bộ lọc bloom giữa các thành viên netDb để xem họ cần chia sẻ gì), nhưng có vẻ như chúng ta có thể xoay sở với một giải pháp đơn giản hơn nhiều hiện tại.

Một sự thật có thể đáng để tìm hiểu - không phải tất cả leaseSets đều cần được xuất bản trong netDb! Trên thực tế, hầu hết không cần - chỉ những leaseSets cho các đích sẽ nhận tin nhắn không được yêu cầu (hay còn gọi là servers). Điều này là do các tin nhắn được bọc bằng garlic encryption gửi từ đích này đến đích khác đã gói sẵn leaseSet của người gửi để bất kỳ việc gửi/nhận tiếp theo nào giữa hai đích đó (trong một khoảng thời gian ngắn) hoạt động mà không cần bất kỳ hoạt động netDb nào.

Vậy nên, quay lại những phương trình đó, chúng ta có thể thay đổi L từ 5 thành khoảng 0.1 (giả sử chỉ có 1 trong số 50 điểm đến là server). Các phương trình trước đó cũng đã bỏ qua tải mạng cần thiết để trả lời các truy vấn từ client, nhưng mặc dù điều này rất biến đổi (dựa trên hoạt động của người dùng), nó cũng rất có khả năng là khá không đáng kể so với tần suất xuất bản.

Dù sao đi nữa, vẫn chưa có phép màu nào, nhưng đã giảm đáng kể gần 1/5 băng thông/dung lượng đĩa cần thiết (có thể giảm nhiều hơn nữa sau này, tùy thuộc vào việc phân phối routerInfo có diễn ra trực tiếp như một phần của việc thiết lập peer hay chỉ thông qua netDb).

### Việc Vô Hiệu Hóa Thuật Toán Kademlia

Kademlia đã được vô hiệu hóa hoàn toàn trong phiên bản 0.6.1.20.

*(Chuyển thể từ cuộc trò chuyện IRC với jrandom ngày 11/07)*

Kademlia yêu cầu mức độ dịch vụ tối thiểu mà cấu hình cơ bản không thể cung cấp (băng thông, cpu), ngay cả sau khi thêm các tầng (kad thuần túy là vô lý ở điểm này). Kademlia đơn giản là không hoạt động được. Đó là một ý tưởng hay, nhưng không phù hợp với môi trường thù địch và biến động.

### Trạng Thái Hiện Tại

NetDb đóng một vai trò rất cụ thể trong mạng I2P, và các thuật toán đã được điều chỉnh theo nhu cầu của chúng tôi. Điều này cũng có nghĩa là nó chưa được điều chỉnh để giải quyết những nhu cầu mà chúng tôi chưa gặp phải. I2P hiện tại còn khá nhỏ (vài trăm router). Có những tính toán cho thấy 3-5 floodfill router sẽ có thể xử lý 10.000 node trong mạng. Việc triển khai netDb hiện tại đáp ứng quá đầy đủ nhu cầu của chúng tôi, nhưng có thể sẽ có thêm các điều chỉnh và sửa lỗi khi mạng lưới phát triển.

### Cập nhật Tính toán 03-2008

Số liệu hiện tại:

```
recvKBps = N * (L + 1) * (1 + F) * (1 + R) * S / T
```
trong đó:

```
N = number of routers in the entire network
L = average number of client destinations on each router
    (+1 for the routerInfo)
F = tunnel failure percentage
R = tunnel rebuild period, as a fraction of the tunnel lifetime
S = average netDb entry size
T = tunnel lifetime
```
Thay đổi trong các giả định:

- L hiện tại khoảng .5, so với .1 ở trên, do sự phổ biến của i2psnark
  và các ứng dụng khác.
- F khoảng .33, nhưng các lỗi trong kiểm tra tunnel đã được sửa trong 0.6.1.33, nên sẽ tốt hơn nhiều.
- Vì netDb khoảng 2/3 là routerInfos 5K và 1/3 là leaseSets 2K, S = 4K.
  Kích thước RouterInfo đang giảm trong 0.6.1.32 và 0.6.1.33 khi chúng tôi loại bỏ các thống kê không cần thiết.
- R = chu kỳ xây dựng tunnel: 0.2 là rất thấp - có thể là 0.7 -
  nhưng cải tiến thuật toán xây dựng trong 0.6.1.32 sẽ giảm xuống khoảng 0.2
  khi mạng nâng cấp. Tạm gọi là 0.5 hiện tại với một nửa mạng ở .30 hoặc cũ hơn.

```
recvKBps = 700 * (0.5 + 1) * (1 + 0.33) * (1 + 0.5) * 4KB / 10m
         ~= 28KBps
```
Điều này chỉ tính đến các kho lưu trữ - còn các truy vấn thì sao?

### Sự Trở Lại của Thuật Toán Kademlia?

*(Chuyển thể từ cuộc họp I2P ngày 2 tháng 1 năm 2007)*

Kademlia netDb đơn giản là không hoạt động đúng cách. Liệu nó đã chết vĩnh viễn hay sẽ quay trở lại? Nếu nó quay trở lại, các peer trong Kademlia netDb sẽ chỉ là một tập hợp con rất hạn chế của các router trong mạng (về cơ bản là một số lượng mở rộng các floodfill peer, nếu/khi các floodfill peer không thể xử lý được tải). Nhưng cho đến khi các floodfill peer không thể xử lý được tải (và không thể thêm các peer khác có khả năng xử lý), thì điều đó là không cần thiết.

### Tương lai của Floodfill

*(Chuyển thể từ cuộc trò chuyện IRC với jrandom 11/07)*

Đây là một đề xuất: Lớp dung lượng O tự động trở thành floodfill. Hmm. Trừ khi chúng ta chắc chắn, chúng ta có thể kết thúc với một cách thức fancy để DDoS tất cả các router lớp O. Đây là trường hợp khá rõ ràng: chúng ta muốn đảm bảo số lượng floodfill nhỏ nhất có thể trong khi vẫn cung cấp khả năng tiếp cận đầy đủ. Nếu/khi các yêu cầu netDb thất bại, thì chúng ta cần tăng số lượng các peer floodfill, nhưng hiện tại, tôi không biết về vấn đề fetch netDb nào. Có 33 peer lớp "O" theo ghi chép của tôi. 33 là /rất nhiều/ để floodfill.

Vậy floodfill hoạt động tốt nhất khi số lượng peer trong pool đó được giới hạn chặt chẽ? Và kích thước của pool floodfill không nên tăng nhiều, ngay cả khi bản thân mạng lưới từ từ phát triển? 3-5 peer floodfill có thể xử lý 10K router nếu tôi nhớ không nhầm (tôi đã đăng một loạt con số giải thích chi tiết về điều này trong syndie cũ). Nghe có vẻ như một yêu cầu khó đáp ứng với việc tự động opt-in, đặc biệt khi các node opt-in không thể tin tưởng dữ liệu từ những node khác. ví dụ "hãy xem tôi có nằm trong top 5 không", và chỉ có thể tin tưởng dữ liệu về chính mình (ví dụ "tôi chắc chắn là class O, và đang di chuyển 150 KB/s, và hoạt động được 123 ngày"). Và top 5 cũng có thể bị tấn công. Cơ bản là giống như các directory server của tor - được chọn bởi những người đáng tin cậy (tức là các dev). Đúng, hiện tại nó có thể bị khai thác bởi opt-in, nhưng điều đó sẽ dễ dàng phát hiện và xử lý. Có vẻ như cuối cùng, chúng ta có thể cần thứ gì đó hữu ích hơn Kademlia, và chỉ có những peer có khả năng hợp lý tham gia vào scheme đó. Class N trở lên nên là một số lượng đủ lớn để ngăn chặn rủi ro kẻ thù gây ra denial of service, tôi hy vọng vậy. Nhưng nó sẽ phải khác với floodfill, theo nghĩa là nó sẽ không gây ra lưu lượng khổng lồ. Số lượng lớn? Cho một netDb dựa trên DHT? Không nhất thiết phải dựa trên DHT.

### Danh sách việc cần làm Floodfill {#todo}

LƯU Ý: Thông tin sau đây không còn cập nhật. Xem [trang netDb chính](/docs/overview/network-database) để biết trạng thái hiện tại và danh sách công việc tương lai.

Mạng lưới chỉ còn lại một floodfill trong vài giờ vào ngày 13 tháng 3 năm 2008 (khoảng 18:00 - 20:00 UTC), và điều này đã gây ra rất nhiều rắc rối.

Hai thay đổi được triển khai trong phiên bản 0.6.1.33 sẽ giảm thiểu sự gián đoạn do việc loại bỏ hoặc thay đổi các floodfill peer:

1. Ngẫu nhiên hóa các peer floodfill được sử dụng cho tìm kiếm mỗi lần.
   Điều này sẽ giúp bạn vượt qua những peer bị lỗi cuối cùng.
   Thay đổi này cũng sửa một lỗi nghiêm trọng đôi khi làm cho mã tìm kiếm ff hoạt động bất thường.
2. Ưu tiên các peer floodfill đang hoạt động.
   Mã hiện tại tránh các peer bị đưa vào danh sách đen, đang lỗi, hoặc không có phản hồi trong
   nửa giờ, nếu có thể.

Một lợi ích là liên hệ nhanh hơn lần đầu tiên với một I2P Site (tức là khi bạn phải tìm nạp leaseset trước). Thời gian chờ tra cứu là 10 giây, vì vậy nếu bạn không bắt đầu bằng việc hỏi một peer đang down, bạn có thể tiết kiệm 10 giây.

Có *thể* có những tác động đến tính ẩn danh trong những thay đổi này. Ví dụ, trong mã **store** của floodfill, có những comment rằng các peer bị shitlist không được tránh, vì một peer có thể "tệ" và sau đó xem điều gì xảy ra. Việc tìm kiếm ít dễ bị tổn thương hơn nhiều so với việc lưu trữ - chúng ít thường xuyên hơn nhiều và tiết lộ ít thông tin hơn. Vậy có thể chúng ta không nghĩ là cần phải lo lắng về điều đó? Nhưng nếu chúng ta muốn điều chỉnh những thay đổi, sẽ rất dễ dàng để gửi đến một peer được liệt kê là "down" hoặc bị shitlist, chỉ là không tính nó như một phần của 2 peer mà chúng ta đang gửi đến (vì chúng ta không thực sự mong đợi một phản hồi).

Có một số nơi mà floodfill peer được lựa chọn - bản sửa lỗi này chỉ giải quyết một nơi - nơi mà một peer thông thường tìm kiếm [2 cùng lúc]. Các nơi khác cần triển khai việc lựa chọn floodfill tốt hơn:

1. Ai mà một peer thông thường lưu trữ đến [1 lần mỗi lượt]
   (ngẫu nhiên - cần thêm điều kiện, vì thời gian chờ rất dài)
2. Ai mà một peer thông thường tìm kiếm để xác minh việc lưu trữ [1 lần mỗi lượt]
   (ngẫu nhiên - cần thêm điều kiện, vì thời gian chờ rất dài)
3. Ai mà một floodfill peer gửi để trả lời cho một tìm kiếm thất bại (3 peer gần nhất với tìm kiếm)
4. Ai mà một floodfill peer flood đến (tất cả các floodfill peer khác)
5. Danh sách các floodfill peer được gửi trong "whisper" NTCP mỗi 6 giờ
   (mặc dù điều này có thể không còn cần thiết do các cải tiến floodfill khác)

Còn rất nhiều việc có thể và nên làm:

- Sử dụng thống kê "dbHistory" để đánh giá tốt hơn việc tích hợp của floodfill peer
- Sử dụng thống kê "dbHistory" để phản ứng ngay lập tức với các floodfill peer không phản hồi
- Thông minh hơn trong việc thử lại - việc thử lại được xử lý bởi lớp trên, không phải trong FloodOnlySearchJob, vì vậy nó thực hiện sắp xếp ngẫu nhiên khác và thử lại, thay vì cố ý bỏ qua các ff peer mà chúng ta vừa thử.
- Cải thiện thống kê tích hợp nhiều hơn
- Thực sự sử dụng thống kê tích hợp thay vì chỉ dùng chỉ báo floodfill trong netDb
- Có sử dụng thống kê độ trễ không?
- Cải thiện thêm việc nhận dạng các floodfill peer đang lỗi

Mới hoàn thành:

- [Trong Phiên bản 0.6.3]
  Triển khai tự động tham gia
  vào floodfill cho một số phần trăm các peer lớp O, dựa trên phân tích mạng.
- [Trong Phiên bản 0.6.3]
  Tiếp tục giảm kích thước entry netDb để giảm lưu lượng floodfill -
  chúng ta hiện đang ở mức tối thiểu các thống kê cần thiết để giám sát mạng.
- [Trong Phiên bản 0.6.3]
  Danh sách thủ công các peer floodfill để loại trừ
  ([blocklists](/docs/overview/threat-model#blocklist) theo router ident)
- [Trong Phiên bản 0.6.3]
  Lựa chọn peer floodfill tốt hơn cho việc lưu trữ:
  Tránh các peer có netDb cũ, hoặc có lưu trữ thất bại gần đây,
  hoặc bị đưa vào danh sách đen vĩnh viễn.
- [Trong Phiên bản 0.6.4]
  Ưu tiên các peer floodfill đã kết nối cho việc lưu trữ RouterInfo, để
  giảm số lượng kết nối trực tiếp đến các peer floodfill.
- [Trong Phiên bản 0.6.5]
  Các peer không còn là floodfill sẽ gửi routerInfo của họ để phản hồi
  một truy vấn, để router thực hiện truy vấn sẽ biết họ
  không còn là floodfill nữa.
- [Trong Phiên bản 0.6.5]
  Tinh chỉnh thêm các yêu cầu để tự động trở thành floodfill
- [Trong Phiên bản 0.6.5]
  Sửa lỗi profiling thời gian phản hồi để chuẩn bị ưu tiên các floodfill nhanh
- [Trong Phiên bản 0.6.5]
  Cải thiện blocklisting
- [Trong Phiên bản 0.7]
  Sửa lỗi khám phá netDb
- [Trong Phiên bản 0.7]
  Bật blocklisting theo mặc định, chặn những kẻ gây rắc rối đã biết
- [Một số cải thiện trong các phiên bản gần đây, một nỗ lực liên tục]
  Giảm nhu cầu tài nguyên trên các router băng thông cao và floodfill

Đó là một danh sách dài nhưng sẽ cần phải làm nhiều công việc như vậy để có một mạng lưới có khả năng chống lại DOS từ nhiều peer bật tắt công tắc floodfill. Hoặc giả vờ là một floodfill router. Không có vấn đề nào trong số này khi chúng ta chỉ có hai ff router, và cả hai đều hoạt động 24/7. Một lần nữa, sự vắng mặt của jrandom đã chỉ ra cho chúng ta những nơi cần cải thiện.

Để hỗ trợ cho nỗ lực này, dữ liệu profile bổ sung cho các floodfill peer hiện tại (kể từ phiên bản 0.6.1.33) được hiển thị trên trang "Profiles" trong bảng điều khiển router. Chúng tôi sẽ sử dụng điều này để phân tích dữ liệu nào phù hợp để đánh giá các floodfill peer.

Mạng lưới hiện tại khá bền vững, tuy nhiên chúng tôi sẽ tiếp tục cải tiến các thuật toán để đo lường và phản ứng với hiệu suất và độ tin cậy của các floodfill peer. Mặc dù hiện tại chúng tôi chưa được bảo vệ hoàn toàn trước các mối đe dọa tiềm ẩn từ các floodfill độc hại hoặc tấn công DDOS floodfill, nhưng hầu hết cơ sở hạ tầng đã được triển khai, và chúng tôi có vị thế tốt để phản ứng nhanh chóng khi cần thiết.
