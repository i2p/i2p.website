---
title: "Thảo luận về NTCP"
description: "Thảo luận lịch sử về các giao thức truyền tải NTCP so với SSU từ tháng 3 năm 2007"
slug: "ntcp-discussion"
aliases:
  - "/vi/docs/discussions/ntcp"
  - "/vi/docs/discussions/ntcp/"
  - "/vi/ntcp_discussion"
  - "/vi/ntcp_discussion/"
lastUpdated: "2007-03"
accurateFor: "historical"
---

Sau đây là một cuộc thảo luận về NTCP diễn ra vào tháng 3 năm 2007. Nó chưa được cập nhật để phản ánh việc triển khai hiện tại. Để xem đặc tả NTCP hiện tại, hãy xem [trang NTCP2](/docs/specs/ntcp2).

## Thảo luận về NTCP và SSU, tháng 3 năm 2007 {#ntcp-ssu}

### Câu hỏi về NTCP

(chuyển thể từ cuộc thảo luận IRC giữa zzz và cervantes)

Tại sao NTCP được ưu tiên hơn SSU, không phải NTCP có overhead và độ trễ cao hơn sao? Nó có độ tin cậy tốt hơn.

Streaming lib qua NTCP có gặp phải các vấn đề TCP-over-TCP cổ điển không? Nếu chúng ta có một UDP transport thực sự đơn giản cho lưu lượng xuất phát từ streaming-lib thì sao? Tôi nghĩ SSU được thiết kế để trở thành cái gọi là UDP transport thực sự đơn giản - nhưng nó chỉ tỏ ra quá không đáng tin cậy.

### Phân tích "NTCP Considered Harmful" của zzz {#harmful}

Đăng lên Syndie mới, 2007-03-25. Bài này được đăng để kích thích thảo luận, đừng quá nghiêm túc với nó.

**Tóm tắt:** NTCP có độ trễ và overhead cao hơn SSU, và có nhiều khả năng bị sập khi sử dụng với streaming lib. Tuy nhiên, lưu lượng được định tuyến với ưu tiên NTCP hơn SSU và điều này hiện đang được hardcode.

#### Thảo luận

Hiện tại chúng tôi có hai transport, NTCP và SSU. Theo cách triển khai hiện tại, NTCP có "bid" thấp hơn SSU nên được ưu tiên, trừ trường hợp đã có kết nối SSU được thiết lập nhưng không có kết nối NTCP được thiết lập cho một peer.

SSU tương tự như NTCP ở chỗ nó triển khai các cơ chế xác nhận, timeout và truyền lại. Tuy nhiên SSU là mã I2P với các ràng buộc chặt chẽ về timeout và có sẵn thống kê về thời gian khứ hồi, truyền lại, v.v. NTCP dựa trên Java NIO TCP, là một hộp đen và có thể triển khai các tiêu chuẩn RFC, bao gồm cả timeout tối đa rất dài.

Phần lớn lưu lượng trong I2P có nguồn gốc từ streaming-lib (HTTP, IRC, Bittorrent) là triển khai TCP của chúng tôi. Vì tầng transport cấp thấp hơn thường là NTCP do các bid thấp hơn, hệ thống gặp phải vấn đề nổi tiếng và đáng sợ của TCP-over-TCP http://sites.inka.de/~W1011/devel/tcp-tcp.html , nơi cả tầng TCP cao hơn và thấp hơn đều thực hiện retransmission cùng lúc, dẫn đến sự sụp đổ.

Khác với kịch bản PPP over SSH được mô tả trong liên kết ở trên, chúng ta có nhiều hop cho lớp thấp hơn, mỗi hop được bao phủ bởi một NTCP link. Vì vậy mỗi độ trễ NTCP thường nhỏ hơn nhiều so với độ trễ của streaming lib ở lớp cao hơn. Điều này làm giảm khả năng sụp đổ.

Ngoài ra, xác suất sụp đổ sẽ giảm khi lớp TCP thấp hơn bị ràng buộc chặt chẽ với thời gian chờ thấp và số lần truyền lại ít hơn so với lớp cao hơn.

Phiên bản .28 đã tăng thời gian chờ tối đa của thư viện streaming từ 10 giây lên 45 giây, điều này đã cải thiện đáng kể. Thời gian chờ tối đa của SSU là 3 giây. Thời gian chờ tối đa của NTCP có thể ít nhất là 60 giây, đây là khuyến nghị của RFC. Không có cách nào để thay đổi các tham số NTCP hoặc giám sát hiệu suất. Sự sụp đổ của lớp NTCP là [editor: văn bản bị mất]. Có thể một công cụ bên ngoài như tcpdump sẽ giúp ích.

Tuy nhiên, khi chạy .28, i2psnark báo cáo upstream thường không duy trì ở mức cao. Nó thường giảm xuống 3-4 KBps trước khi tăng trở lại. Đây là tín hiệu cho thấy vẫn còn xảy ra sự sụp đổ.

SSU cũng hiệu quả hơn. NTCP có overhead cao hơn và có thể có thời gian khứ hồi cao hơn. Khi sử dụng NTCP, tỷ lệ (tunnel output) / (i2psnark data output) là ít nhất 3.5 : 1. Khi chạy thử nghiệm với code được sửa đổi để ưu tiên SSU (tùy chọn cấu hình i2np.udp.alwaysPreferred không có tác dụng trong code hiện tại), tỷ lệ này giảm xuống khoảng 3 : 1, cho thấy hiệu suất tốt hơn.

Theo báo cáo từ thống kê streaming lib, mọi thứ đã được cải thiện đáng kể - kích thước cửa sổ lifetime tăng từ 6.3 lên 7.5, RTT giảm từ 11.5s xuống 10s, số lần gửi trên mỗi ack giảm từ 1.11 xuống 1.07.

Việc này khá hiệu quả thật đáng ngạc nhiên, xét rằng chúng tôi chỉ thay đổi giao thức truyền tải cho hop đầu tiên trong tổng số 3 đến 5 hop mà các thông điệp gửi đi sẽ phải đi qua.

Tác động lên tốc độ i2psnark gửi đi không rõ ràng do các biến động bình thường. Ngoài ra trong thí nghiệm, NTCP đầu vào đã bị tắt. Tác động lên tốc độ đầu vào trên i2psnark không rõ ràng.

#### Đề xuất

1. **1A)** Điều này dễ dàng -
   Chúng ta nên đảo ngược thứ tự ưu tiên bid để SSU được ưu tiên cho tất cả traffic, nếu
   chúng ta có thể làm điều này mà không gây ra đủ loại rắc rối khác. Điều này sẽ sửa
   tùy chọn cấu hình i2np.udp.alwaysPreferred để nó hoạt động (dù là true
   hay false).

2. **1B)** Thay thế cho 1A), không dễ dàng lắm -
   Nếu chúng ta có thể đánh dấu lưu lượng mà không ảnh hưởng xấu đến mục tiêu ẩn danh của mình, chúng ta
   nên xác định lưu lượng được tạo bởi streaming-lib và để SSU tạo ra một bid thấp
   cho lưu lượng đó. Thẻ này sẽ phải đi cùng với thông điệp qua từng hop
   để các router chuyển tiếp cũng tôn trọng ưu tiên SSU.

3. **2)** Giới hạn SSU thêm nữa (giảm số lần truyền lại tối đa từ mức hiện tại là 10) có thể là khôn ngoan để giảm khả năng sụp đổ.

4. **3)** Chúng ta cần nghiên cứu thêm về lợi ích so với tác hại của giao thức bán tin cậy
   bên dưới thư viện streaming. Việc truyền lại qua một hop duy nhất có có lợi
   và là một chiến thắng lớn hay chúng tệ hơn cả vô dụng?
   Chúng ta có thể tạo một SUU mới (secure unreliable UDP) nhưng có lẽ không đáng.
   Chúng ta có thể thêm một loại thông điệp không yêu cầu ack trong SSU nếu không muốn
   có bất kỳ truyền lại nào của lưu lượng streaming-lib. Việc truyền lại có giới hạn
   chặt chẽ có mong muốn không?

5. **4)** Mã gửi ưu tiên trong .28 chỉ dành cho NTCP. Cho đến nay, việc kiểm thử của tôi chưa cho thấy nhiều ích lợi từ việc ưu tiên SSU vì các thông điệp không xếp hàng đợi đủ lâu để việc ưu tiên phát huy tác dụng. Nhưng cần kiểm thử thêm.

6. **5)** Thời gian chờ tối đa 45s của thư viện streaming mới có thể vẫn còn quá thấp.
   RFC TCP nói là 60s. Nó có lẽ không nên ngắn hơn thời gian chờ tối đa của NTCP bên dưới (có thể là 60s).

### Phản hồi của jrandom {#jrandom-response}

Đăng lên Syndie mới, 2007-03-27

Nhìn chung, tôi sẵn sàng thử nghiệm với điều này, nhưng hãy nhớ tại sao NTCP lại có mặt ở đây ngay từ đầu - SSU đã thất bại trong tình trạng sụp đổ do nghẽn mạng. NTCP "chỉ việc hoạt động", và trong khi tỷ lệ truyền lại 2-10% có thể được xử lý trong các mạng một hop thông thường, điều đó cho chúng ta tỷ lệ truyền lại 40% với tunnel 2 hop. Nếu bạn tính đến một số tỷ lệ truyền lại SSU đã đo được mà chúng ta thấy trước khi NTCP được triển khai (10-30+%), điều đó cho chúng ta tỷ lệ truyền lại 83%. Có lẽ những tỷ lệ đó được gây ra bởi timeout thấp 10 giây, nhưng việc tăng nhiều như vậy sẽ gây hại cho chúng ta (hãy nhớ, nhân với 5 và bạn có một nửa hành trình).

Khác với TCP, chúng ta không có phản hồi từ tunnel để biết liệu thông điệp có được gửi thành công hay không - không có xác nhận ở cấp độ tunnel. Chúng ta có xác nhận đầu cuối đến đầu cuối, nhưng chỉ trên một số ít thông điệp (mỗi khi chúng ta phân phối các session tag mới) - trong số 1.553.591 thông điệp client mà router của tôi đã gửi, chúng ta chỉ thử xác nhận 145.207 trong số đó. Những thông điệp còn lại có thể đã thất bại một cách im lặng hoặc thành công hoàn hảo.

Tôi không thuyết phục bởi lập luận TCP-over-TCP đối với chúng ta, đặc biệt là khi chia tách qua các đường dẫn khác nhau mà chúng ta truyền tải. Tất nhiên, các phép đo trên I2P có thể thuyết phục tôi khác đi.

> *Thời gian chờ tối đa của NTCP được cho là ít nhất 60 giây, đây là khuyến nghị của RFC. Không có cách nào để thay đổi các tham số NTCP hoặc giám sát hiệu suất.*

Đúng vậy, nhưng các kết nối mạng chỉ đạt đến mức độ đó khi có điều gì đó thực sự tệ đang xảy ra - thời gian chờ retransmission trên TCP thường ở mức hàng chục hoặc hàng trăm milliseconds. Như foofighter chỉ ra, họ có hơn 20 năm kinh nghiệm và sửa lỗi trong TCP stack của mình, cộng với một ngành công nghiệp tỷ đô tối ưu hóa phần cứng và phần mềm để hoạt động tốt theo bất cứ điều gì họ làm.

> *NTCP có overhead cao hơn và có thể có thời gian round trip cao hơn. khi sử dụng NTCP > tỷ lệ (tunnel output) / (i2psnark data output) là ít nhất 3.5 : 1. > Chạy một thí nghiệm mà code đã được sửa đổi để ưu tiên SSU (tùy chọn config > i2np.udp.alwaysPreferred không có tác dụng trong code hiện tại), tỷ lệ > giảm xuống khoảng 3 : 1, cho thấy hiệu suất tốt hơn.*

Đây là dữ liệu rất thú vị, mặc dù thể hiện vấn đề tắc nghẽn router hơn là hiệu quả băng thông - bạn cần phải so sánh 3.5*$n*$NTCPRetransmissionPct với 3.0*$n*$SSURetransmissionPct. Điểm dữ liệu này cho thấy có điều gì đó trong router dẫn đến việc xếp hàng cục bộ quá mức các thông điệp đang được truyền tải.

> *kích thước cửa sổ thời gian sống tăng từ 6.3 lên 7.5, RTT giảm từ 11.5s xuống 10s, số lần gửi trên mỗi ACK giảm từ 1.11 xuống 1.07.*

Hãy nhớ rằng sends-per-ACK chỉ là một mẫu chứ không phải là số đếm đầy đủ (vì chúng ta không cố gắng ACK mỗi lần gửi). Đây cũng không phải là mẫu ngẫu nhiên, mà thay vào đó lấy mẫu nhiều hơn trong các giai đoạn không hoạt động hoặc khởi đầu của một đợt hoạt động bùng nổ - tải liên tục sẽ không yêu cầu nhiều ACK.

Kích thước cửa sổ trong phạm vi đó vẫn còn quá thấp một cách đáng tiếc để có được lợi ích thực sự từ AIMD, và vẫn quá thấp để truyền một khối BT 32KB duy nhất (tăng ngưỡng tối thiểu lên 10 hoặc 12 sẽ bao phủ được điều đó).

Tuy nhiên, thống kê wsize trông khá hứa hẹn - nó được duy trì trong bao lâu?

Thực tế, cho mục đích thử nghiệm, bạn có thể muốn xem xét StreamSinkClient/StreamSinkServer hoặc thậm chí TestSwarm trong apps/ministreaming/java/src/net/i2p/client/streaming/ - StreamSinkClient là một ứng dụng CLI gửi một tệp được chọn đến một đích được chọn và StreamSinkServer tạo một đích và ghi ra bất kỳ dữ liệu nào được gửi đến nó (hiển thị kích thước và thời gian truyền). TestSwarm kết hợp cả hai - tràn ngập dữ liệu ngẫu nhiên cho bất kỳ ai mà nó kết nối. Điều đó sẽ cung cấp cho bạn các công cụ để đo lường khả năng thông lượng duy trì qua streaming lib, trái ngược với BT choke/send.

> *1A) Điều này dễ dàng - > Chúng ta nên đảo ngược thứ tự ưu tiên bid để SSU được ưa chuộng cho tất cả traffic, nếu > chúng ta có thể làm điều này mà không gây ra đủ loại rắc rối khác. Điều này sẽ sửa > tùy chọn cấu hình i2np.udp.alwaysPreferred để nó hoạt động (dù là true > hay false).*

Tôn trọng i2np.udp.alwaysPreferred là một ý tưởng tốt trong mọi trường hợp - xin hãy thoải mái commit thay đổi đó. Tuy nhiên hãy thu thập thêm một chút dữ liệu trước khi chuyển đổi các tùy chọn, vì NTCP đã được thêm vào để xử lý tình trạng sụp đổ tắc nghẽn do SSU tạo ra.

> *1B) Thay thế cho 1A), không dễ dàng lắm - > Nếu chúng ta có thể đánh dấu lưu lượng mà không ảnh hưởng xấu đến mục tiêu ẩn danh của mình, chúng ta > nên xác định lưu lượng do streaming-lib tạo ra > và để SSU tạo ra một giá thầu thấp cho lưu lượng đó. Thẻ này sẽ phải đi kèm > với thông điệp qua từng hop > để các router chuyển tiếp cũng tôn trọng ưu tiên SSU.*

Trong thực tế, có ba loại lưu lượng - xây dựng/kiểm tra tunnel, truy vấn/phản hồi netDb, và lưu lượng streaming lib. Mạng lưới đã được thiết kế để việc phân biệt ba loại này trở nên rất khó khăn.

> *2) Giới hạn SSU thêm nữa (giảm số lần truyền lại tối đa từ mức hiện tại > 10) có lẽ là khôn ngoan để giảm khả năng sụp đổ.*

Ở mức 10 lần truyền lại, chúng ta đã gặp rắc rối lớn rồi, tôi đồng ý. Một hoặc có thể hai lần truyền lại là hợp lý từ góc độ tầng vận chuyển, nhưng nếu phía bên kia quá nghẽn để ACK kịp thời (ngay cả với khả năng SACK/NACK đã được triển khai), thì chúng ta cũng không làm được gì nhiều.

Theo quan điểm của tôi, để thực sự giải quyết vấn đề cốt lõi, chúng ta cần tìm hiểu tại sao router lại bị tắc nghẽn đến mức không thể ACK kịp thời (từ những gì tôi tìm hiểu được, điều này là do tranh chấp CPU). Có thể chúng ta có thể điều chỉnh một số thứ trong quá trình xử lý của router để đặt việc truyền tải trên tunnel đã tồn tại thành ưu tiên CPU cao hơn so với việc giải mã yêu cầu tunnel mới? Tuy nhiên chúng ta phải cẩn thận tránh tình trạng starvation.

> *3) Chúng ta cần nghiên cứu thêm về lợi ích so với tác hại của một giao thức bán tin cậy > bên dưới thư viện streaming. Việc truyền lại qua một hop đơn có mang lại lợi ích > và là một chiến thắng lớn hay chúng tệ hơn cả việc vô dụng? > Chúng ta có thể tạo một SUU mới (secure unreliable UDP) nhưng có lẽ không đáng. Chúng ta > có thể thêm một loại message không yêu cầu ACK trong SSU nếu chúng ta không muốn bất kỳ > việc truyền lại nào của traffic streaming-lib. Liệu việc truyền lại có giới hạn chặt chẽ > có mong muốn không?*

Đáng để xem xét - điều gì sẽ xảy ra nếu chúng ta chỉ tắt tính năng truyền lại của SSU? Có thể sẽ dẫn đến tỷ lệ gửi lại cao hơn nhiều trong thư viện streaming, nhưng có thể là không.

> *4) Mã gửi ưu tiên trong .28 chỉ dành cho NTCP. Cho đến nay việc thử nghiệm của tôi chưa cho thấy nhiều tác dụng của ưu tiên SSU vì các thông báo không xếp hàng đủ lâu để ưu tiên có thể phát huy tác dụng tốt. Nhưng cần thử nghiệm nhiều hơn.*

Có UDPTransport.PRIORITY_LIMITS và UDPTransport.PRIORITY_WEIGHT (được tôn trọng bởi TimedWeightedPriorityMessageQueue), nhưng hiện tại các trọng số gần như đều bằng nhau, nên không có hiệu ứng gì. Điều đó có thể được điều chỉnh, tất nhiên (nhưng như bạn đề cập, nếu không có queuing, thì cũng không quan trọng).

> *5) Thời gian chờ tối đa 45 giây của streaming lib mới có lẽ vẫn còn quá thấp. TCP RFC > nói là 60 giây. Nó có lẽ không nên ngắn hơn thời gian chờ tối đa của NTCP bên dưới > (có lẽ là 60 giây).*

45 giây đó là thời gian chờ retransmission tối đa của thư viện streaming, không phải thời gian chờ stream. TCP trên thực tế có thời gian chờ retransmission nhỏ hơn nhiều bậc, mặc dù đúng là có thể lên đến 60 giây trên các đường truyền qua dây cáp lộ thiên hoặc truyền vệ tinh ;) Nếu chúng ta tăng thời gian chờ retransmission của thư viện streaming lên ví dụ 75 giây, chúng ta có thể đi uống bia trước khi một trang web tải xong (đặc biệt giả sử độ tin cậy vận chuyển dưới 98%). Đó là một lý do chúng ta ưu tiên NTCP.

### Phản hồi của zzz {#zzz-response}

Đăng lên Syndie mới, 2007-03-31

> *Với 10 lần truyền lại, chúng ta đã rơi vào tình thế khó khăn rồi, tôi đồng ý. Một, có thể hai lần truyền lại là hợp lý, từ tầng transport, nhưng nếu phía bên kia quá bị tắc nghẽn để ACK kịp thời (ngay cả với khả năng SACK/NACK đã được triển khai), thì chúng ta không thể làm gì nhiều.* > > *Theo quan điểm của tôi, để thực sự giải quyết vấn đề cốt lõi, chúng ta cần giải quyết tại sao router bị tắc nghẽn đến mức không thể ACK kịp thời (điều này, từ những gì tôi đã tìm ra, là do tranh chấp CPU). Có thể chúng ta có thể sắp xếp lại một số thứ trong quá trình xử lý của router để làm cho việc truyền tải của một tunnel đã tồn tại có độ ưu tiên CPU cao hơn việc giải mã một yêu cầu tunnel mới? Tuy nhiên chúng ta phải cẩn thận để tránh tình trạng đói tài nguyên.*

Một trong những kỹ thuật thu thập thống kê chính của tôi là bật net.i2p.client.streaming.ConnectionPacketHandler=DEBUG và theo dõi thời gian RTT cũng như kích thước cửa sổ khi chúng diễn ra. Để khái quát hóa một chút, thường thấy 3 loại kết nối: RTT ~4s, RTT ~10s, và RTT ~30s. Mục tiêu là cố gắng giảm bớt các kết nối RTT 30s. Nếu tranh chấp CPU là nguyên nhân thì có thể một số thao tác điều chỉnh sẽ giải quyết được.

Việc giảm SSU max retrans từ 10 thực sự chỉ là một phỏng đoán trong bóng tối vì chúng ta không có dữ liệu tốt về việc liệu chúng ta có đang bị sập, gặp vấn đề TCP-over-TCP, hay gì đó khác, vì vậy cần thêm dữ liệu.

> *Đáng để tìm hiểu - nếu chúng ta chỉ vô hiệu hóa việc truyền lại của SSU thì sao? Có thể sẽ dẫn đến tỷ lệ gửi lại của streaming lib cao hơn nhiều, nhưng có thể không.*

Điều tôi không hiểu, nếu bạn có thể giải thích thêm, là lợi ích của việc truyền lại SSU đối với lưu lượng không phải streaming-lib. Liệu chúng ta có cần các tunnel message (ví dụ) sử dụng transport bán-đáng tin cậy hay chúng có thể sử dụng transport không đáng tin cậy hoặc gần như đáng tin cậy (tối đa 1 hoặc 2 lần truyền lại, chẳng hạn)? Nói cách khác, tại sao lại cần tính bán-đáng tin cậy?

> *(nhưng như bạn đã đề cập, nếu không có hàng đợi thì điều đó không quan trọng).*

Tôi đã triển khai tính năng gửi ưu tiên cho UDP nhưng nó được kích hoạt ít hơn khoảng 100.000 lần so với code phía NTCP. Có thể đó là một manh mối để điều tra thêm hoặc một gợi ý - tôi không hiểu tại sao nó lại bị tắc nghẽn thường xuyên hơn rất nhiều trên NTCP, nhưng có thể đó là gợi ý giải thích tại sao NTCP hoạt động kém hơn.

### Câu hỏi được trả lời bởi jrandom {#jrandom-followup}

Đăng lên Syndie mới, 2007-03-31

> *tỷ lệ truyền lại SSU đo được mà chúng ta đã thấy trước khi NTCP được triển khai > (10-30+%)* > > Router có thể tự đo lường điều này không? Nếu có, liệu có thể chọn transport dựa > trên hiệu suất đo được không? (tức là nếu kết nối SSU tới một peer đang bỏ > một số lượng message không hợp lý, ưu tiên NTCP khi gửi tới peer đó)

Đúng vậy, hiện tại nó đang sử dụng thống kê đó như một phương pháp phát hiện MTU đơn giản (nếu tỷ lệ truyền lại cao, nó sử dụng kích thước gói nhỏ, nhưng nếu thấp, nó sử dụng kích thước gói lớn). Chúng tôi đã thử một vài cách khi lần đầu giới thiệu NTCP (và khi lần đầu chuyển từ transport TCP gốc) mà sẽ ưu tiên SSU nhưng dễ dàng thất bại transport đó cho một peer, khiến nó phải quay lại sử dụng NTCP. Tuy nhiên, chắc chắn có thể làm nhiều hơn trong vấn đề này, mặc dù nó trở nên phức tạp một cách nhanh chóng (như thế nào/khi nào điều chỉnh/đặt lại các bid, có nên chia sẻ những preferences này qua nhiều peer hay không, có nên chia sẻ nó qua nhiều session với cùng một peer (và trong bao lâu), v.v.).

### Phản hồi từ foofighter {#foofighter}

Đăng lên Syndie mới, 2007-03-26

Nếu tôi hiểu đúng, lý do chính để ủng hộ TCP (nói chung, cả phiên bản cũ và mới) là bạn không cần phải lo lắng về việc lập trình một TCP stack tốt. Điều này không phải là không thể làm đúng... chỉ là các TCP stack hiện tại đã có lợi thế 20 năm kinh nghiệm.

Theo tôi biết, chưa có nhiều lý thuyết sâu sắc nào về việc ưu tiên TCP so với UDP, ngoại trừ các cân nhắc sau:

- Mạng chỉ sử dụng TCP rất phụ thuộc vào các peer có thể truy cập được (những peer có thể chuyển tiếp các kết nối đến thông qua NAT của họ)
- Tuy nhiên, ngay cả khi các peer có thể truy cập hiếm, việc chúng có dung lượng cao cũng phần nào giảm thiểu các vấn đề khan hiếm về mặt tôpô
- UDP cho phép "NAT hole punching" giúp người dùng có thể "pseudo-reachable" (với sự hỗ trợ của introducer) trong khi nếu không thì họ chỉ có thể kết nối ra ngoài
- Triển khai transport TCP "cũ" đòi hỏi nhiều thread, gây giết chết hiệu năng, trong khi transport TCP "mới" hoạt động tốt với ít thread
- Các router thuộc nhóm A bị lỗi khi bão hòa với UDP. Các router thuộc nhóm B bị lỗi khi bão hòa với TCP.
- Có "cảm giác" (có một số dấu hiệu nhưng không có dữ liệu khoa học hay thống kê chất lượng) rằng nhóm A được triển khai rộng rãi hơn nhóm B
- Một số mạng truyền tải các datagram UDP không phải DNS với chất lượng cực kỳ tệ, trong khi vẫn cố gắng truyền tải các luồng TCP một cách tương đối.

Trên cơ sở đó, một sự đa dạng nhỏ về các phương thức truyền tải (đủ nhiều khi cần thiết, nhưng không quá nhiều) có vẻ hợp lý trong cả hai trường hợp. Phương thức truyền tải nào nên là chính phụ thuộc vào hiệu suất của chúng. Tôi đã thấy những vấn đề tệ hại trên đường truyền của mình khi cố gắng sử dụng toàn bộ dung lượng với UDP. Mất gói tin ở mức 35%.

Chúng ta chắc chắn có thể thử nghiệm với các mức độ ưu tiên UDP so với TCP, nhưng tôi khuyến cáo nên thận trọng trong việc này. Tôi khuyến nghị không nên thay đổi chúng quá mạnh mẽ cùng một lúc, vì có thể sẽ làm hỏng mọi thứ.

### Phản hồi của zzz (gửi foofighter) {#zzz-foofighter}

Đăng lên Syndie mới, 2007-03-27

> *Theo tôi biết, chưa có nhiều lý thuyết sâu sắc đằng sau việc ưa thích TCP so với UDP, ngoại trừ những cân nhắc sau:*

Đây đều là những vấn đề hợp lý. Tuy nhiên bạn đang xem xét hai giao thức một cách riêng lẻ, thay vì suy nghĩ về giao thức vận chuyển nào tốt nhất cho một giao thức cấp cao cụ thể (tức là có dùng thư viện streaming hay không).

Điều tôi muốn nói là bạn phải tính đến streaming lib.

Vậy nên hoặc thay đổi cấu hình cho tất cả mọi người hoặc xử lý lưu lượng streaming lib một cách khác biệt.

Đó là điều mà đề xuất 1B) của tôi đang nói đến - có một sự ưu tiên khác nhau cho lưu lượng streaming-lib so với lưu lượng không phải streaming-lib (ví dụ như các tin nhắn tunnel build).

> *Trên nền tảng đó, một sự đa dạng nhỏ của các transport (nhiều như cần thiết, nhưng > không quá nhiều) có vẻ hợp lý trong cả hai trường hợp. Transport nào nên là chính, > phụ thuộc vào hiệu suất của chúng. Tôi đã thấy những thứ tệ hại trên đường truyền của mình khi > thử sử dụng hết công suất của nó với UDP. Mất gói ở mức 35%.*

Đồng ý. Phiên bản .28 mới có thể đã cải thiện tình trạng mất gói tin qua UDP, hoặc có thể là không.

Một điểm quan trọng - mã transport có nhớ các lỗi của transport. Vì vậy nếu UDP là transport ưu tiên, nó sẽ thử UDP trước, nhưng nếu nó thất bại cho một đích cụ thể, lần thử tiếp theo cho đích đó nó sẽ thử NTCP thay vì thử UDP lại.

> *Chúng ta chắc chắn có thể thử nghiệm với các mức độ ưu tiên của UDP so với TCP, nhưng tôi khuyến cáo nên thận trọng trong việc này. Tôi khuyến cáo không nên thay đổi chúng quá mạnh mẽ cùng một lúc, vì điều đó có thể làm hỏng mọi thứ.*

Chúng ta có bốn núm điều chỉnh - bốn giá trị đấu giá (SSU và NTCP, cho đã kết nối và chưa kết nối). Ví dụ, chúng ta có thể ưu tiên SSU hơn NTCP chỉ khi cả hai đều đã kết nối, nhưng thử NTCP trước nếu cả hai transport đều chưa kết nối.

Cách khác để thực hiện từ từ là chỉ chuyển lưu lượng streaming lib (đề xuất 1B) tuy nhiên điều đó có thể khó khăn và có thể có những tác động đến tính ẩn danh, tôi không chắc chắn. Hoặc có thể chỉ chuyển lưu lượng cho hop đầu tiên đi ra (tức là không truyền flag đến router tiếp theo), điều này chỉ mang lại lợi ích một phần nhưng có thể ẩn danh hơn và dễ dàng hơn.

## Kết quả của Cuộc thảo luận {#results}

... và các thay đổi liên quan khác trong cùng khoảng thời gian (2007):

- Việc điều chỉnh đáng kể các tham số của streaming lib,
  cải thiện rất nhiều hiệu suất outbound, đã được triển khai trong 0.6.1.28
- Priority sending cho NTCP đã được triển khai trong 0.6.1.28
- Priority sending cho SSU đã được zzz triển khai nhưng chưa bao giờ được check in
- Hệ thống kiểm soát bid transport nâng cao
  i2np.udp.preferred đã được triển khai trong 0.6.1.29.
- Pushback cho NTCP đã được triển khai trong 0.6.1.30, bị vô hiệu hóa trong 0.6.1.31 do lo ngại về tính ẩn danh,
  và được kích hoạt lại với các cải tiến để giải quyết những lo ngại đó trong 0.6.1.32.
- Không có đề xuất nào từ 1-5 của zzz được triển khai.
