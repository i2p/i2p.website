---
title: "Thảo luận về Đặt tên"
description: "Cuộc tranh luận lịch sử về mô hình đặt tên của I2P và tại sao các sơ đồ kiểu DNS toàn cầu bị từ chối"
slug: "naming"
aliases:
  - "/vi/docs/legacy/naming"
  - "/vi/docs/legacy/naming/"
  - "/vi/naming_discussion"
  - "/vi/naming_discussion/"
lastUpdated: "2025-02"
accurateFor: "historical"
---

LƯU Ý: Nội dung sau đây là thảo luận về lý do đằng sau hệ thống đặt tên I2P, các lập luận phổ biến và các giải pháp thay thế có thể. Xem [trang đặt tên](/docs/naming) để biết tài liệu hiện tại.

## Các Lựa chọn Thay thế Bị Loại bỏ

Việc đặt tên trong I2P đã là một chủ đề được tranh luận thường xuyên ngay từ những ngày đầu với những người ủng hộ trên khắp phổ các khả năng. Tuy nhiên, với nhu cầu vốn có của I2P về giao tiếp bảo mật và hoạt động phi tập trung, hệ thống đặt tên kiểu DNS truyền thống rõ ràng là không phù hợp, cũng như các hệ thống bỏ phiếu "đa số quyết định".

Tuy nhiên, I2P không khuyến khích việc sử dụng các dịch vụ giống DNS, vì thiệt hại gây ra bởi việc chiếm đoạt một trang web có thể rất lớn - và các destination không an toàn không có giá trị gì. Bản thân DNSsec vẫn phải dựa vào các nhà đăng ký tên miền và certificate authorities, trong khi với I2P, các yêu cầu gửi đến một destination không thể bị chặn hoặc phản hồi bị giả mạo, vì chúng được mã hóa bằng public keys của destination, và bản thân một destination chỉ là một cặp public keys và một certificate. Mặt khác, các hệ thống kiểu DNS cho phép bất kỳ name server nào trên đường dẫn tra cứu thực hiện các cuộc tấn công denial of service và spoofing đơn giản. Việc thêm một certificate xác thực các phản hồi như được ký bởi một certificate authority tập trung có thể giải quyết nhiều vấn đề về nameserver thù địch nhưng vẫn để ngỏ các cuộc tấn công replay cũng như các cuộc tấn công từ certificate authority thù địch.

Cách đặt tên theo kiểu bỏ phiếu cũng rất nguy hiểm, đặc biệt là do tính hiệu quả của các cuộc tấn công Sybil trong các hệ thống ẩn danh - kẻ tấn công có thể đơn giản tạo ra một số lượng peer tùy ý cao và "bỏ phiếu" với mỗi peer để chiếm quyền điều khiển một tên nhất định. Các phương pháp proof-of-work có thể được sử dụng để làm cho danh tính không miễn phí, nhưng khi mạng lớn lên, tải cần thiết để liên hệ với tất cả mọi người để tiến hành bỏ phiếu trực tuyến là không khả thi, hoặc nếu không truy vấn toàn bộ mạng, có thể đạt được các tập hợp câu trả lời khác nhau.

Tuy nhiên, giống như Internet, I2P đang giữ việc thiết kế và vận hành hệ thống đặt tên tách biệt khỏi lớp giao tiếp (giống như IP). Thư viện đặt tên được tích hợp sẵn bao gồm một giao diện nhà cung cấp dịch vụ đơn giản mà [các hệ thống đặt tên thay thế](#alternatives) có thể kết nối vào, cho phép người dùng cuối quyết định loại sự đánh đổi về đặt tên mà họ muốn.

## Thảo luận

Xem thêm [Names: Decentralized, Secure, Human-Meaningful: Choose Two](https://zooko.com/distnames.html).

### Bình luận bởi jrandom

(chuyển thể từ một bài đăng trong Syndie cũ, ngày 26 tháng 11 năm 2005)

Q: Phải làm gì nếu một số host không thống nhất về một địa chỉ và nếu một số địa chỉ hoạt động, những địa chỉ khác thì không? Ai là nguồn đúng của một tên?

A: Bạn không thể. Đây thực sự là một sự khác biệt quan trọng giữa tên trên I2P và cách thức hoạt động của DNS - tên trong I2P có thể đọc được bởi con người, bảo mật, nhưng **không duy nhất trên toàn cầu**. Điều này là có chủ ý, và là một phần vốn có trong nhu cầu bảo mật của chúng ta.

Nếu tôi có thể thuyết phục bạn thay đổi địa chỉ đích liên kết với một tên nào đó, thì tôi đã thành công "chiếm quyền" trang web đó, và trong bất kỳ hoàn cảnh nào điều này cũng không thể chấp nhận được. Thay vào đó, điều chúng tôi làm là tạo ra các tên **duy nhất cục bộ**: chúng là những gì *bạn* sử dụng để gọi một trang web, giống như cách bạn có thể gọi mọi thứ theo ý muốn khi thêm chúng vào bookmark của trình duyệt hoặc danh sách bạn bè của IM client. Người mà bạn gọi là "Boss" có thể là người mà ai đó khác gọi là "Sally".

Tên sẽ không bao giờ có thể vừa an toàn, vừa dễ đọc với con người và vừa duy nhất trên toàn cầu.

### Bình luận của zzz

Dưới đây từ zzz là một đánh giá về một số khiếu nại phổ biến về hệ thống đặt tên của I2P.

- **Không hiệu quả:** Toàn bộ hosts.txt được tải xuống (nếu nó đã thay đổi, vì eepget sử dụng etag và last-modified headers). Hiện tại nó khoảng 400K cho gần 800 hosts.

Đúng, nhưng đây không phải là lượng traffic lớn trong bối cảnh của I2P, vốn đã cực kỳ không hiệu quả (cơ sở dữ liệu floodfill, chi phí mã hóa và padding khổng lồ, garlic routing, v.v.). Nếu bạn tải xuống tệp hosts.txt từ ai đó mỗi 12 giờ, trung bình sẽ là khoảng 10 bytes/giây.

Như thường xảy ra trong I2P, ở đây có một sự đánh đổi cơ bản giữa tính ẩn danh và hiệu quả. Một số người cho rằng việc sử dụng các header etag và last-modified là nguy hiểm vì nó tiết lộ thời điểm bạn yêu cầu dữ liệu lần cuối. Những người khác đã đề xuất chỉ yêu cầu các key cụ thể (tương tự như những gì các dịch vụ jump làm, nhưng theo cách tự động hơn), có thể với chi phí ẩn danh cao hơn.

Các cải tiến có thể có sẽ là thay thế hoặc bổ sung cho address book (xem i2host.i2p), hoặc một cái gì đó đơn giản như đăng ký http://example.i2p/cgi-bin/recenthosts.cgi thay vì http://example.i2p/hosts.txt. Nếu một recenthosts.cgi giả định phân phối tất cả các host từ 24 giờ qua, ví dụ, điều đó có thể vừa hiệu quả hơn vừa ẩn danh hơn so với hosts.txt hiện tại với last-modified và etag.

Một triển khai mẫu có thể tìm thấy trên stats.i2p tại http://stats.i2p/cgi-bin/newhosts.txt. Script này trả về một Etag với timestamp. Khi có yêu cầu đến với etag If-None-Match, script CHỈ trả về các host mới kể từ timestamp đó, hoặc 304 Not Modified nếu không có host nào. Theo cách này, script hiệu quả trả về chỉ những host mà người đăng ký chưa biết, theo cách tương thích với address book.

Vì vậy, sự kém hiệu quả không phải là vấn đề lớn và có nhiều cách để cải thiện mọi thứ mà không cần thay đổi triệt để.

- **Không Có Khả Năng Mở Rộng:** Tệp hosts.txt 400K (với tìm kiếm tuyến tính) hiện tại không quá lớn và chúng ta có thể tăng trưởng 10 lần hoặc 100 lần trước khi nó trở thành vấn đề.

Về lưu lượng mạng thì xem phần trên. Nhưng trừ khi bạn định thực hiện một truy vấn thời gian thực chậm qua mạng cho một key, bạn cần phải lưu trữ toàn bộ tập hợp các key ở local, với chi phí khoảng 500 byte mỗi key.

- **Yêu cầu cấu hình và "tin tưởng":** Sổ địa chỉ mặc định chỉ đăng ký http://www.i2p2.i2p/hosts.txt, hiếm khi được cập nhật, dẫn đến trải nghiệm kém cho người dùng mới.

Điều này hoàn toàn có chủ ý. jrandom muốn người dùng "tin tưởng" một nhà cung cấp hosts.txt, và như ông hay nói, "niềm tin không phải là một giá trị boolean". Bước cấu hình cố gắng buộc người dùng phải suy nghĩ về các vấn đề tin tưởng trong một mạng lưới ẩn danh.

Ví dụ khác, trang lỗi "I2P Site Unknown" trong HTTP Proxy liệt kê một số dịch vụ jump, nhưng không "khuyến nghị" bất kỳ dịch vụ nào cụ thể, và người dùng có thể tự chọn (hoặc không chọn). jrandom có thể nói rằng chúng tôi tin tưởng các nhà cung cấp được liệt kê đủ để đưa vào danh sách nhưng không đủ để tự động lấy key từ họ.

Tôi không chắc điều này thành công đến mức nào. Nhưng phải có một loại hệ thống phân cấp tin cậy nào đó cho hệ thống đặt tên. Việc đối xử bình đẳng với mọi người có thể làm tăng nguy cơ bị chiếm đoạt.

- **Nó không phải là DNS**

Thật không may, việc tra cứu theo thời gian thực qua I2P sẽ làm chậm đáng kể việc duyệt web.

Ngoài ra, DNS dựa trên việc tra cứu với bộ nhớ đệm hạn chế và thời gian tồn tại, trong khi các khóa I2P là vĩnh viễn.

Chắc chắn, chúng ta có thể làm cho nó hoạt động, nhưng tại sao lại phải vậy? Nó không phù hợp.

- **Không đáng tin cậy:** Nó phụ thuộc vào các máy chủ cụ thể cho việc đăng ký sổ địa chỉ.

Có, nó phụ thuộc vào một vài máy chủ mà bạn đã cấu hình. Trong I2P, các máy chủ và dịch vụ xuất hiện và biến mất. Bất kỳ hệ thống tập trung nào khác (ví dụ như máy chủ DNS gốc) cũng sẽ gặp phải vấn đề tương tự. Một hệ thống hoàn toàn phi tập trung (mọi người đều có thẩm quyền) có thể được thực hiện bằng cách triển khai giải pháp "mọi người đều là máy chủ DNS gốc", hoặc bằng cách đơn giản hơn, như một script thêm mọi người trong hosts.txt của bạn vào sổ địa chỉ của bạn.

Tuy nhiên, những người ủng hộ các giải pháp hoàn toàn có thẩm quyền thường chưa suy nghĩ kỹ về các vấn đề xung đột và tấn công chiếm quyền.

- **Khó sử dụng, không thời gian thực:** Đây là một hệ thống vá víu gồm các nhà cung cấp hosts.txt, nhà cung cấp biểu mẫu web thêm khóa, nhà cung cấp dịch vụ jump, và các báo cáo trạng thái I2P Site. Jump server và subscription rất phiền phức, nó nên hoạt động đơn giản như DNS.

Xem các phần về độ tin cậy và sự tin tưởng.

Vậy, tóm lại, hệ thống hiện tại không hề tệ hại, kém hiệu quả, hay không thể mở rộng, và các đề xuất "chỉ cần sử dụng DNS" không được cân nhắc kỹ lưỡng.

## Các phương án thay thế

Mã nguồn I2P chứa nhiều hệ thống đặt tên có thể cắm thêm và hỗ trợ các tùy chọn cấu hình để cho phép thử nghiệm với các hệ thống đặt tên.

- **Meta** - gọi hai hoặc nhiều hệ thống đặt tên khác theo thứ tự. Mặc định, gọi PetName rồi đến HostsTxt.
- **PetName** - Tra cứu trong file petnames.txt. Định dạng cho file này KHÔNG giống với hosts.txt.
- **HostsTxt** - Tra cứu trong các file sau, theo thứ tự:
  1. privatehosts.txt
  2. userhosts.txt
  3. hosts.txt
- **AddressDB** - Mỗi host được liệt kê trong một file riêng biệt trong thư mục addressDb/.
- **Eepget** - thực hiện yêu cầu tra cứu HTTP từ một server bên ngoài - phải được xếp chồng sau tra cứu HostsTxt với Meta. Điều này có thể bổ sung hoặc thay thế hệ thống jump. Bao gồm bộ nhớ đệm trong memory.
- **Exec** - gọi một chương trình bên ngoài để tra cứu, cho phép thử nghiệm thêm các sơ đồ tra cứu, độc lập với java. Có thể được sử dụng sau HostsTxt hoặc như hệ thống đặt tên duy nhất. Bao gồm bộ nhớ đệm trong memory.
- **Dummy** - được sử dụng như một phương án dự phòng cho tên Base64, nếu không thì sẽ thất bại.

Hệ thống đặt tên hiện tại có thể được thay đổi với tùy chọn cấu hình nâng cao `i2p.naming.impl` (cần khởi động lại). Xem `core/java/src/net/i2p/client/naming` để biết chi tiết.

Bất kỳ hệ thống mới nào cũng nên được xếp chồng với HostsTxt, hoặc nên triển khai lưu trữ cục bộ và/hoặc các chức năng đăng ký address book, vì address book chỉ biết về các tệp và định dạng hosts.txt.

## Chứng chỉ

Các destination I2P chứa một certificate, tuy nhiên hiện tại certificate đó luôn là null. Với certificate null, các destination base64 luôn có độ dài 516 byte và kết thúc bằng "AAAA", và điều này được kiểm tra trong cơ chế hợp nhất address book, và có thể ở những nơi khác. Ngoài ra, không có phương thức nào để tạo certificate hoặc thêm nó vào destination. Vì vậy những phần này sẽ phải được cập nhật để triển khai certificate.

Một cách sử dụng có thể của chứng chỉ là cho [bằng chứng công việc](/get-involved/todo#hashcash).

Một cách khác là để các "subdomain" (đặt trong ngoặc kép vì thực tế không có khái niệm này, I2P sử dụng hệ thống đặt tên phẳng) được ký bởi khóa của domain cấp 2.

Với bất kỳ triển khai certificate nào cũng phải đi kèm phương pháp để xác minh các certificate. Có thể điều này sẽ xảy ra trong mã merge address book. Có phương pháp nào cho nhiều loại certificate khác nhau, hoặc nhiều certificate không?

Việc thêm chứng chỉ xác thực các phản hồi được ký bởi một cơ quan chứng chỉ tập trung nào đó sẽ giải quyết nhiều vấn đề về nameserver thù địch nhưng vẫn để ngỏ các cuộc tấn công replay cũng như các cuộc tấn công từ cơ quan chứng chỉ thù địch.
