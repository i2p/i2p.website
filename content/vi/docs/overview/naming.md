---
title: "Đặt tên và Sổ địa chỉ"
description: "Cách I2P ánh xạ tên máy chủ có thể đọc được sang các đích đến"
slug: "naming"
aliases:
  - "/vi/docs/specs/naming"
  - "/vi/docs/specs/naming/"
  - "/vi/docs/naming"
  - "/vi/docs/naming/"
lastUpdated: "2025-01"
accurateFor: "0.9.65"
---

## Tổng quan

I2P được tích hợp sẵn một thư viện đặt tên chung và một triển khai cơ bản được thiết kế để hoạt động dựa trên ánh xạ tên cục bộ đến destination, cũng như một ứng dụng bổ sung gọi là [address book](#address-book). I2P cũng hỗ trợ [Base32 hostnames](#base32-names) tương tự như địa chỉ .onion của Tor.

Address book là một hệ thống đặt tên có thể đọc được bởi con người, an toàn, phân tán và được điều khiển bởi web-of-trust, chỉ hy sinh yêu cầu tất cả các tên có thể đọc được bởi con người phải là duy nhất toàn cầu bằng cách chỉ yêu cầu tính duy nhất cục bộ. Trong khi tất cả các thông điệp trong I2P đều được định địa chỉ mã hóa bằng destination của chúng, những người khác nhau có thể có các mục trong address book cục bộ cho "Alice" mà tham chiếu đến các destination khác nhau. Mọi người vẫn có thể khám phá các tên mới bằng cách nhập các address book đã xuất bản của các peer được chỉ định trong web of trust của họ, bằng cách thêm vào các mục được cung cấp thông qua bên thứ ba, hoặc (nếu một số người tổ chức một loạt address book đã xuất bản sử dụng hệ thống đăng ký theo nguyên tắc đến trước được phục vụ trước) mọi người có thể chọn coi các address book này như name server, mô phỏng DNS truyền thống.

LƯU Ý: Để hiểu lý do đằng sau hệ thống đặt tên I2P, các lập luận phổ biến phản đối nó và các giải pháp thay thế có thể có, hãy xem trang [thảo luận về đặt tên](/docs/legacy/naming/).

---

## Các Thành Phần Hệ Thống Đặt Tên

Không có cơ quan quản lý tên miền trung tâm nào trong I2P. Tất cả hostname đều là cục bộ.

Hệ thống đặt tên khá đơn giản và phần lớn được triển khai trong các ứng dụng bên ngoài router, nhưng được đóng gói cùng với bản phân phối I2P. Các thành phần bao gồm:

1. [Dịch vụ đặt tên](#naming-services) cục bộ thực hiện tra cứu và cũng xử lý [tên máy chủ Base32](#base32-names).
2. [HTTP proxy](#http-proxy) yêu cầu router tra cứu và hướng người dùng đến các dịch vụ jump từ xa để hỗ trợ khi tra cứu thất bại.
3. [Biểu mẫu host-add](#host-add-services) HTTP cho phép người dùng thêm máy chủ vào hosts.txt cục bộ của họ.
4. [Dịch vụ jump](#jump-services) HTTP cung cấp tra cứu và chuyển hướng riêng của chúng.
5. Ứng dụng [sổ địa chỉ](#address-book) hợp nhất các danh sách máy chủ bên ngoài, được lấy qua HTTP, với danh sách cục bộ.
6. Ứng dụng [SusiDNS](#susidns) là một giao diện web đơn giản để cấu hình sổ địa chỉ và xem các danh sách máy chủ cục bộ.

---

## Dịch vụ Đặt tên

Tất cả các destination trong I2P đều là các khóa có độ dài 516 byte (hoặc dài hơn). (Để chính xác hơn, đó là một khóa công khai 256 byte cộng với một khóa ký 128 byte cộng với một chứng chỉ 3 byte trở lên, khi được biểu diễn dưới dạng Base64 sẽ là 516 byte hoặc nhiều hơn. Các [Certificate](/docs/legacy/naming/#certificates) không rỗng hiện đang được sử dụng để chỉ định loại chữ ký. Do đó, các certificate trong những destination được tạo gần đây sẽ có độ dài hơn 3 byte.

Nếu một ứng dụng (i2ptunnel hoặc HTTP proxy) muốn truy cập một đích đến bằng tên, router sẽ thực hiện một tra cứu cục bộ rất đơn giản để phân giải tên đó.

### Dịch vụ đặt tên Hosts.txt

Dịch vụ đặt tên hosts.txt thực hiện tìm kiếm tuyến tính đơn giản qua các tệp văn bản. Dịch vụ đặt tên này là mặc định cho đến phiên bản 0.8.8 khi nó được thay thế bởi Dịch vụ đặt tên Blockfile. Định dạng hosts.txt đã trở nên quá chậm sau khi tệp phát triển lên hàng nghìn mục.

Nó thực hiện tìm kiếm tuyến tính qua ba tệp cục bộ, theo thứ tự, để tra cứu tên máy chủ và chuyển đổi chúng thành khóa đích 516-byte. Mỗi tệp có định dạng [tệp cấu hình](/docs/specs/configuration/) đơn giản, với hostname=base64, mỗi dòng một mục. Các tệp là:

1. privatehosts.txt
2. userhosts.txt
3. hosts.txt

### Dịch vụ Đặt tên Blockfile

Blockfile Naming Service lưu trữ nhiều "sổ địa chỉ" trong một tệp cơ sở dữ liệu duy nhất có tên hostsdb.blockfile. Naming Service này là mặc định kể từ phiên bản 0.8.8.

Blockfile đơn giản là lưu trữ trên đĩa của nhiều bản đồ được sắp xếp (cặp khóa-giá trị), được triển khai dưới dạng skiplists. Định dạng blockfile được chỉ định trên [trang Blockfile](/docs/specs/blockfile/). Nó cung cấp khả năng tra cứu Destination nhanh chóng trong định dạng nhỏ gọn. Mặc dù chi phí phụ trội của blockfile là đáng kể, các destination được lưu trữ dưới dạng nhị phân thay vì Base 64 như trong định dạng hosts.txt. Ngoài ra, blockfile cung cấp khả năng lưu trữ metadata tùy ý (như ngày thêm, nguồn và nhận xét) cho mỗi mục để triển khai các tính năng sổ địa chỉ nâng cao. Yêu cầu lưu trữ blockfile tăng nhẹ so với định dạng hosts.txt, và blockfile cung cấp khả năng giảm khoảng 10 lần thời gian tra cứu.

Khi được tạo, dịch vụ đặt tên sẽ nhập các mục từ ba tệp được sử dụng bởi Dịch vụ Đặt tên hosts.txt. Blockfile mô phỏng cách triển khai trước đó bằng cách duy trì ba bản đồ được tìm kiếm theo thứ tự, có tên là privatehosts.txt, userhosts.txt và hosts.txt. Nó cũng duy trì một bản đồ tra cứu ngược để thực hiện tra cứu ngược nhanh chóng.

### Các Tiện Ích Dịch Vụ Đặt Tên Khác

Việc tra cứu không phân biệt chữ hoa chữ thường. Kết quả khớp đầu tiên sẽ được sử dụng, và các xung đột không được phát hiện. Không có việc thực thi các quy tắc đặt tên trong quá trình tra cứu. Các tra cứu được lưu cache trong vài phút. Việc phân giải Base 32 được [mô tả bên dưới](#base32-names). Để có mô tả đầy đủ về API của Naming Service, hãy xem [Naming Service Javadocs](http://idk.i2p/javadoc-i2p/net/i2p/client/naming/package-summary.html). API này đã được mở rộng đáng kể trong phiên bản 0.8.7 để cung cấp tính năng thêm và xóa, lưu trữ các thuộc tính tùy ý với hostname, và các tính năng khác.

### Các Dịch vụ Đặt tên Thay thế và Thử nghiệm

Dịch vụ đặt tên được chỉ định với thuộc tính cấu hình `i2p.naming.impl=class`. Các triển khai khác cũng có thể thực hiện được. Ví dụ, có một tính năng thử nghiệm cho việc tra cứu thời gian thực (như DNS) qua mạng trong router. Để biết thêm thông tin, xem [các lựa chọn thay thế trên trang thảo luận](/docs/legacy/naming/#alternatives).

HTTP proxy thực hiện tra cứu thông qua router cho tất cả các hostname kết thúc bằng '.i2p'. Ngược lại, nó chuyển tiếp yêu cầu đến một HTTP outproxy đã được cấu hình. Do đó, trên thực tế, tất cả các hostname HTTP (I2P Site) phải kết thúc bằng pseudo-Top Level Domain '.i2p'.

Nếu router không thể phân giải hostname, HTTP proxy sẽ trả về một trang lỗi cho người dùng với các liên kết đến một số dịch vụ "jump". Xem chi tiết bên dưới.

---

## Tên miền .i2p.alt

Trước đây chúng tôi đã [nộp đơn xin dành riêng TLD .i2p](https://datatracker.ietf.org/doc/draft-grothoff-iesg-special-use-p2p-names/) theo các quy trình được quy định trong [RFC 6761](https://www.rfc-editor.org/rfc/rfc6761.html). Tuy nhiên, đơn đăng ký này và tất cả các đơn khác đều bị từ chối, và RFC 6761 được tuyên bố là một "sai lầm".

Sau nhiều năm làm việc của nhóm GNUnet và những người khác, tên miền .alt đã được dành riêng như một TLD sử dụng đặc biệt trong [RFC 9476](https://www.rfc-editor.org/rfc/rfc9476.html) vào cuối năm 2023. Mặc dù không có nhà đăng ký chính thức nào được IANA ủy quyền, chúng tôi đã đăng ký tên miền .i2p.alt với nhà đăng ký không chính thức chính [GANA](https://gana.gnunet.org/dot-alt/dot_alt.html). Điều này không ngăn cản những người khác sử dụng tên miền này, nhưng sẽ giúp làm nản lòng việc sử dụng đó.

Một lợi ích của tên miền .alt là về mặt lý thuyết, các DNS resolver sẽ không chuyển tiếp các yêu cầu .alt khi chúng được cập nhật để tuân thủ RFC 9476, và điều này sẽ ngăn chặn rò rỉ DNS. Để tương thích với tên máy chủ .i2p.alt, phần mềm và dịch vụ I2P cần được cập nhật để xử lý các tên máy chủ này bằng cách loại bỏ TLD .alt. Những cập nhật này được lên lịch cho nửa đầu năm 2024.

Hiện tại, chưa có kế hoạch nào để biến .i2p.alt thành dạng ưa thích cho việc hiển thị và trao đổi tên máy chủ I2P. Đây là chủ đề cần nghiên cứu và thảo luận thêm.

---

## Sổ Địa Chỉ

### Đăng ký Đến và Hợp nhất

Ứng dụng address book định kỳ tải các tệp hosts.txt của người dùng khác và hợp nhất chúng với hosts.txt cục bộ, sau khi thực hiện một số kiểm tra. Xung đột tên được giải quyết theo nguyên tắc ai đến trước được phục vụ trước.

Việc đăng ký file hosts.txt của người dùng khác đòi hỏi bạn phải tin tưởng họ ở một mức độ nhất định. Bạn không muốn họ, chẳng hạn, 'chiếm đoạt' một trang web mới bằng cách nhanh chóng nhập khóa của riêng họ cho trang web mới đó trước khi chuyển mục host/key mới cho bạn.

Vì lý do này, subscription duy nhất được cấu hình mặc định là `http://i2p-projekt.i2p/hosts.txt (http://udhdrtrcetjm5sxzskjyr5ztpeszydbh4dpl3pl4utgqqw2v4jna.b32.i2p/hosts.txt)`, chứa một bản sao của hosts.txt được đi kèm trong bản phát hành I2P. Người dùng phải cấu hình thêm các subscription trong ứng dụng address book cục bộ của họ (thông qua subscriptions.txt hoặc [SusiDNS](#susidns)).

Một số liên kết đăng ký address book công khai khác:

- http://i2host.i2p/cgi-bin/i2hostetag
- http://stats.i2p/cgi-bin/newhosts.txt

Các nhà điều hành của những dịch vụ này có thể có các chính sách khác nhau để liệt kê các máy chủ. Việc có mặt trong danh sách này không có nghĩa là được xác nhận hoặc tán thành.

### Quy Tắc Đặt Tên

Mặc dù hy vọng không có bất kỳ hạn chế kỹ thuật nào trong I2P đối với tên host, nhưng sổ địa chỉ vẫn áp dụng một số hạn chế đối với tên host được nhập từ các đăng ký. Điều này được thực hiện để đảm bảo tính hợp lý về mặt kiểu chữ cơ bản và khả năng tương thích với trình duyệt, cũng như vì lý do bảo mật. Các quy tắc này về cơ bản giống với những quy tắc trong RFC2396 Mục 3.2.2. Bất kỳ tên host nào vi phạm các quy tắc này có thể sẽ không được truyền bá đến các router khác.

Quy tắc đặt tên:

- Tên được chuyển đổi thành chữ thường khi nhập.
- Tên được kiểm tra xung đột với các tên hiện có trong userhosts.txt và hosts.txt hiện tại (nhưng không phải privatehosts.txt) sau khi chuyển đổi thành chữ thường.
- Chỉ được chứa [a-z] [0-9] '.' và '-' sau khi chuyển đổi thành chữ thường.
- Không được bắt đầu bằng '.' hoặc '-'.
- Phải kết thúc bằng '.i2p'.
- Tối đa 67 ký tự, bao gồm '.i2p'.
- Không được chứa '..'.
- Không được chứa '.-' hoặc '-.' (từ phiên bản 0.6.1.33).
- Không được chứa '--' ngoại trừ trong 'xn--' cho IDN.
- Hostname Base32 (*.b32.i2p) được dành riêng cho sử dụng base 32 nên không được phép nhập.
- Một số hostname được dành riêng cho dự án không được phép (proxy.i2p, router.i2p, console.i2p, mail.i2p, *.proxy.i2p, *.router.i2p, *.console.i2p, *.mail.i2p, và các tên khác)
- Hostname bắt đầu bằng 'www.' không được khuyến khích và bị từ chối bởi một số dịch vụ đăng ký. Một số triển khai addressbook tự động loại bỏ tiền tố 'www.' khỏi việc tra cứu. Vì vậy việc đăng ký 'www.example.i2p' là không cần thiết, và việc đăng ký một đích khác cho 'www.example.i2p' và 'example.i2p' sẽ làm cho 'www.example.i2p' không thể tiếp cận được đối với một số người dùng.
- Key được kiểm tra tính hợp lệ của base64.
- Key được kiểm tra xung đột với các key hiện có trong hosts.txt (nhưng không phải privatehosts.txt).
- Độ dài key tối thiểu 516 byte.
- Độ dài key tối đa 616 byte (để tính đến cert lên đến 100 byte).

Bất kỳ tên nào nhận được qua subscription mà vượt qua tất cả các kiểm tra sẽ được thêm vào thông qua dịch vụ đặt tên cục bộ.

Lưu ý rằng các ký tự '.' trong tên host không có ý nghĩa gì đặc biệt và không biểu thị bất kỳ hệ thống phân cấp đặt tên hay tin cậy thực sự nào. Nếu tên 'host.i2p' đã tồn tại, không có gì ngăn cản bất kỳ ai thêm tên 'a.host.i2p' vào hosts.txt của họ, và tên này có thể được nhập bởi address book của người khác. Các phương pháp để từ chối subdomain cho những người không phải 'chủ sở hữu' domain (chứng chỉ?), cũng như tính mong muốn và khả thi của những phương pháp này, là những chủ đề để thảo luận trong tương lai.

International Domain Names (IDN) cũng hoạt động trong i2p (sử dụng dạng punycode 'xn--'). Để xem tên miền IDN .i2p hiển thị chính xác trong thanh địa chỉ của Firefox, hãy thêm 'network.IDN.whitelist.i2p (boolean) = true' trong about:config.

Vì ứng dụng address book không sử dụng privatehosts.txt, trên thực tế file này là nơi duy nhất thích hợp để đặt các bí danh riêng tư hoặc "tên thú cưng" cho các trang web đã có trong hosts.txt.

### Định dạng nguồn cấp dữ liệu đăng ký nâng cao

Kể từ phiên bản 0.9.26, các trang web đăng ký và client có thể hỗ trợ giao thức nguồn cấp hosts.txt nâng cao bao gồm metadata và chữ ký. Định dạng này tương thích ngược với định dạng hosts.txt chuẩn hostname=base64destination. Xem [đặc tả kỹ thuật](/docs/specs/subscription/) để biết chi tiết.

### Đăng ký Gửi đi

Address Book sẽ xuất bản tệp hosts.txt đã hợp nhất đến một vị trí (thông thường là hosts.txt trong thư mục chính của I2P Site cục bộ) để những người khác có thể truy cập cho việc đăng ký của họ. Bước này là tùy chọn và được tắt theo mặc định.

### Vấn đề về Hosting và HTTP Transport

Ứng dụng sổ địa chỉ, cùng với eepget, lưu thông tin Etag và/hoặc Last-Modified được trả về bởi web server của subscription. Điều này giảm đáng kể băng thông cần thiết, vì web server sẽ trả về '304 Not Modified' trong lần tải tiếp theo nếu không có gì thay đổi.

Tuy nhiên, toàn bộ tệp hosts.txt sẽ được tải xuống nếu nó đã thay đổi. Xem thảo luận bên dưới về vấn đề này.

Các hosts phục vụ file hosts.txt tĩnh hoặc ứng dụng CGI tương đương được khuyến khích mạnh mẽ cung cấp header Content-Length, và header Etag hoặc Last-Modified. Cũng cần đảm bảo rằng server trả về '304 Not Modified' khi phù hợp. Điều này sẽ giảm đáng kể băng thông mạng và giảm khả năng bị lỗi.

---

## Dịch vụ Thêm Host

Dịch vụ thêm host là một ứng dụng CGI đơn giản nhận tên host và khóa Base64 làm tham số và thêm chúng vào tệp hosts.txt cục bộ. Nếu các router khác đăng ký hosts.txt đó, cặp tên host/khóa mới sẽ được lan truyền qua mạng.

Khuyến nghị rằng các dịch vụ thêm host nên áp đặt tối thiểu các hạn chế được áp đặt bởi ứng dụng sổ địa chỉ được liệt kê ở trên. Các dịch vụ thêm host có thể áp đặt thêm các hạn chế đối với hostname và key, ví dụ:

- Giới hạn số lượng 'subdomain'.
- Ủy quyền cho 'subdomain' thông qua các phương pháp khác nhau.
- Hashcash hoặc chứng chỉ có chữ ký.
- Xem xét biên tập tên host và/hoặc nội dung.
- Phân loại host theo nội dung.
- Bảo lưu hoặc từ chối một số tên host nhất định.
- Hạn chế về số lượng tên được đăng ký trong một khoảng thời gian nhất định.
- Độ trễ giữa đăng ký và xuất bản.
- Yêu cầu host phải hoạt động để xác minh.
- Hết hạn và/hoặc thu hồi.
- Từ chối giả mạo IDN.

---

## Dịch vụ Jump

Dịch vụ jump là một ứng dụng CGI đơn giản nhận tên máy chủ làm tham số và trả về mã chuyển hướng 301 đến URL thích hợp với chuỗi `?i2paddresshelper=key` được thêm vào. HTTP proxy sẽ diễn giải chuỗi được thêm vào và sử dụng key đó làm đích thực sự. Ngoài ra, proxy sẽ lưu cache key đó để address helper không cần thiết cho đến khi khởi động lại.

Lưu ý rằng, giống như với subscriptions, việc sử dụng jump service ngụ ý một mức độ tin tưởng nhất định, vì jump service có thể chuyển hướng người dùng một cách độc hại đến một địa chỉ đích không chính xác.

Để cung cấp dịch vụ tốt nhất, một dịch vụ jump nên đăng ký với nhiều nhà cung cấp hosts.txt để danh sách host cục bộ của nó luôn được cập nhật.

---

## SusiDNS

SusiDNS chỉ đơn giản là một giao diện web front-end để cấu hình đăng ký address book và truy cập vào bốn tệp address book. Tất cả công việc thực sự được thực hiện bởi ứng dụng 'address book'.

Hiện tại, có rất ít việc thực thi các quy tắc đặt tên trong address book trong SusiDNS, do đó người dùng có thể nhập các hostname cục bộ mà sẽ bị từ chối bởi các quy tắc đăng ký address book.

---

## Tên Base32

I2P hỗ trợ tên máy chủ Base32 tương tự như địa chỉ .onion của Tor. Địa chỉ Base32 ngắn hơn nhiều và dễ xử lý hơn so với Destinations Base64 đầy đủ 516 ký tự hoặc addresshelpers. Ví dụ: `ukeu3k5oycgaauneqgtnvselmt4yemvoilkln7jpvamvfx7dnkdq.b32.i2p`

Trong Tor, địa chỉ có 16 ký tự (80 bits), hoặc bằng một nửa của hash SHA-1. I2P sử dụng 52 ký tự (256 bits) để biểu diễn hash SHA-256 đầy đủ. Định dạng là {52 chars}.b32.i2p. Tor có một [đề xuất](https://blog.torproject.org/blog/tor-weekly-news-%E2%80%94-december-4th-2013) để chuyển đổi sang định dạng giống hệt {52 chars}.onion cho các dịch vụ ẩn của họ. Base32 được triển khai trong dịch vụ đặt tên, dịch vụ này truy vấn router qua I2CP để tra cứu LeaseSet nhằm lấy Destination đầy đủ. Việc tra cứu Base32 chỉ thành công khi Destination đang hoạt động và xuất bản LeaseSet. Do việc phân giải có thể yêu cầu tra cứu cơ sở dữ liệu mạng, nó có thể mất thời gian lâu hơn đáng kể so với tra cứu sổ địa chỉ cục bộ.

Địa chỉ Base32 có thể được sử dụng ở hầu hết các nơi mà hostname hoặc destination đầy đủ được sử dụng, tuy nhiên có một số trường hợp ngoại lệ mà chúng có thể thất bại nếu tên không được phân giải ngay lập tức. I2PTunnel sẽ thất bại, ví dụ, nếu tên không được phân giải thành một destination.

---

## Tên Extended Base32

Tên base 32 mở rộng đã được giới thiệu trong phiên bản 0.9.40 để hỗ trợ encrypted lease sets. Địa chỉ cho encrypted leasesets được xác định bởi 56 ký tự được mã hóa trở lên, không bao gồm ".b32.i2p" (35 byte đã giải mã trở lên), so với 52 ký tự (32 byte) cho địa chỉ base 32 truyền thống. Xem đề xuất 123 và 149 để biết thêm thông tin.

Địa chỉ Base 32 tiêu chuẩn ("b32") chứa hash của đích đến. Điều này sẽ không hoạt động với ls2 được mã hóa (đề xuất 123).

Bạn không thể sử dụng địa chỉ base 32 truyền thống cho một LS2 mã hóa (đề xuất 123), vì nó chỉ chứa hash của đích đến. Nó không cung cấp public key không bị làm mù. Clients phải biết public key của đích đến, loại sig, loại blinded sig, và một secret hoặc private key tùy chọn để fetch và giải mã leaseset. Do đó, chỉ riêng địa chỉ base 32 là không đủ. Client cần có đầy đủ destination (chứa public key), hoặc chỉ cần public key. Nếu client có đầy đủ destination trong address book, và address book hỗ trợ reverse lookup theo hash, thì public key có thể được truy xuất.

Vì vậy chúng ta cần một định dạng mới đặt public key thay vì hash vào địa chỉ base32. Định dạng này cũng phải chứa loại chữ ký của public key và loại chữ ký của sơ đồ blinding.

Phần này ghi lại một định dạng b32 mới cho các địa chỉ này. Mặc dù chúng tôi đã gọi định dạng mới này trong các cuộc thảo luận là địa chỉ "b33", nhưng định dạng mới thực tế vẫn giữ nguyên hậu tố ".b32.i2p" thông thường.

### Tạo và mã hóa

Xây dựng một hostname có định dạng {56+ ký tự}.b32.i2p (35+ ký tự ở dạng nhị phân) như sau. Đầu tiên, xây dựng dữ liệu nhị phân để mã hóa base 32:

```
flag (1 byte)
  bit 0: 0 for one-byte sigtypes, 1 for two-byte sigtypes
  bit 1: 0 for no secret, 1 if secret is required
  bit 2: 0 for no per-client auth,
         1 if client private key is required
  bits 7-3: Unused, set to 0

public key sigtype (1 or 2 bytes as indicated in flags)
  If 1 byte, the upper byte is assumed zero

blinded key sigtype (1 or 2 bytes as indicated in flags)
  If 1 byte, the upper byte is assumed zero

public key
  Number of bytes as implied by sigtype
```
Xử lý hậu kỳ và checksum:

```
Construct the binary data as above.
Treat checksum as little-endian.
Calculate checksum = CRC-32(data[3:end])
data[0] ^= (byte) checksum
data[1] ^= (byte) (checksum >> 8)
data[2] ^= (byte) (checksum >> 16)

hostname = Base32.encode(data) || ".b32.i2p"
```
Bất kỳ bit không sử dụng nào ở cuối b32 phải bằng 0. Không có bit không sử dụng nào cho địa chỉ tiêu chuẩn 56 ký tự (35 byte).

### Giải mã và Xác thực

```
Strip the ".b32.i2p" from the hostname
data = Base32.decode(hostname)
Calculate checksum = CRC-32(data[3:end])
Treat checksum as little-endian.
flags = data[0] ^ (byte) checksum
if 1 byte sigtypes:
  pubkey sigtype = data[1] ^ (byte) (checksum >> 8)
  blinded sigtype = data[2] ^ (byte) (checksum >> 16)
else (2 byte sigtypes) :
  pubkey sigtype = data[1] ^ ((byte) (checksum >> 8)) || data[2] ^ ((byte) (checksum >> 16))
  blinded sigtype = data[3] || data[4]
parse the remainder based on the flags to get the public key
```
### Bit Khóa Bí Mật và Khóa Riêng Tư

Các bit secret và private key được sử dụng để báo hiệu cho các client, proxy, hoặc mã phía client khác rằng secret và/hoặc private key sẽ cần thiết để giải mã leaseset. Các triển khai cụ thể có thể nhắc người dùng cung cấp dữ liệu cần thiết, hoặc từ chối các nỗ lực kết nối nếu thiếu dữ liệu cần thiết.

### Ghi chú

- XOR 3 byte đầu với hash cung cấp khả năng checksum hạn chế, và đảm bảo rằng tất cả các ký tự base32 ở đầu được ngẫu nhiên hóa. Chỉ có một số kết hợp flag và sigtype hợp lệ, vì vậy bất kỳ lỗi đánh máy nào cũng có thể tạo ra một kết hợp không hợp lệ và sẽ bị từ chối.
- Trong trường hợp thông thường (sigtype 1 byte, không có secret, không có per-client auth), hostname sẽ là {56 chars}.b32.i2p, giải mã thành 35 byte, giống như Tor.
- Checksum 2-byte của Tor có tỷ lệ false negative là 1/64K. Với 3 byte, trừ đi một vài byte bị bỏ qua, của chúng ta đang tiến gần đến 1 trong một triệu, vì hầu hết các kết hợp flag/sigtype đều không hợp lệ.
- Adler-32 là một lựa chọn kém cho các input nhỏ, và để phát hiện những thay đổi nhỏ. Chúng ta sử dụng CRC-32 thay thế. CRC-32 nhanh và có sẵn rộng rãi.
- Mặc dù nằm ngoài phạm vi của đặc tả này, các router và/hoặc client phải nhớ và cache (có thể là persistent) việc ánh xạ public key với destination, và ngược lại.
- Phân biệt phiên bản cũ và mới theo độ dài. Địa chỉ b32 cũ luôn là {52 chars}.b32.i2p. Địa chỉ mới là {56+ chars}.b32.i2p
- Chuỗi thảo luận của Tor [ở đây](https://lists.torproject.org/pipermail/tor-dev/2017-January/011816.html)
- Đừng mong đợi sigtype 2-byte sẽ xảy ra, chúng ta chỉ mới đến 13. Không cần triển khai ngay bây giờ.
- Định dạng mới có thể được sử dụng trong jump links (và được phục vụ bởi jump servers) nếu muốn, giống như b32.
- Bất kỳ secret, private key, hoặc public key nào dài hơn 32 byte sẽ vượt quá độ dài tối đa của DNS label là 63 ký tự. Các trình duyệt có thể không quan tâm.
- Không có vấn đề tương thích ngược. Các địa chỉ b32 dài hơn sẽ không thể được chuyển đổi thành hash 32-byte trong phần mềm cũ.
