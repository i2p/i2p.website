---
title: "I2PTunnel"
description: "Công cụ để giao tiếp và cung cấp dịch vụ trên I2P"
slug: "i2ptunnel"
aliases:
  - "/vi/i2ptunnel"
  - "/vi/i2ptunnel/"
  - "/vi/i2ptunnel_migration"
  - "/vi/i2ptunnel_migration/"
  - "/vi/i2ptunnel_services"
  - "/vi/i2ptunnel_services/"
lastUpdated: "2023-10"
accurateFor: "0.9.59"
---

## Tổng quan {#overview}

I2PTunnel là một công cụ để giao tiếp và cung cấp dịch vụ trên I2P. Điểm đến của một I2PTunnel có thể được định nghĩa bằng cách sử dụng [hostname](/docs/overview/naming), [Base32](/docs/overview/naming#base32), hoặc một khóa đích đầy đủ 516-byte. Một I2PTunnel đã được thiết lập sẽ có sẵn trên máy client của bạn dưới dạng localhost:port. Nếu bạn muốn cung cấp một dịch vụ trên mạng I2P, bạn chỉ cần tạo I2PTunnel đến ip_address:port thích hợp. Một khóa đích 516-byte tương ứng sẽ được tạo ra cho dịch vụ và nó sẽ trở nên khả dụng trên toàn bộ I2P. Giao diện web để quản lý I2PTunnel có sẵn tại [localhost:7657/i2ptunnel/](http://localhost:7657/i2ptunnel/).

## Dịch vụ Mặc định {#default-services}

### Server Tunnels {#default-server-tunnels}

- **I2P Webserver** - Một tunnel trỏ đến máy chủ web Jetty chạy
  trên [localhost:7658](http://localhost:7658) để host thuận tiện và nhanh chóng trên I2P.
  Thư mục gốc tài liệu là:
  - **Unix** - `$HOME/.i2p/eepsite/docroot`
  - **Windows** - `%LOCALAPPDATA%\I2P\I2P Site\docroot`, mở rộng thành: `C:\Users\**username**\AppData\Local\I2P\I2P Site\docroot`

### Client Tunnels {#default-client-tunnels}

- **I2P HTTP Proxy** - *localhost:4444* - Một HTTP proxy được sử dụng để duyệt I2P và internet thông thường một cách ẩn danh thông qua I2P. Duyệt internet qua I2P sử dụng một proxy ngẫu nhiên được chỉ định bởi tùy chọn "Outproxies:".
- **Irc2P** - *localhost:6668* - Một IRC tunnel tới mạng IRC ẩn danh mặc định, Irc2P.
- **gitssh.idk.i2p** - *localhost:7670* - Truy cập SSH tới kho Git của dự án
- **smtp.postman.i2p** - *localhost:7659* - Một dịch vụ SMTP được cung cấp bởi postman tại hq.postman.i2p
- **pop3.postman.i2p** - *localhost:7660* - Dịch vụ POP đi kèm của postman tại hq.postman.i2p

## Cấu hình {#configuration}

[Cấu hình I2PTunnel](/docs/specs/configuration)

## Chế độ Client {#client-modes}

### Tiêu chuẩn {#client-modes-standard}

Mở một cổng TCP cục bộ kết nối đến một dịch vụ (như HTTP, FTP hoặc SMTP) trên một đích bên trong I2P. Tunnel được định hướng đến một host ngẫu nhiên từ danh sách các đích được phân tách bằng dấu phẩy (", ").

### HTTP {#client-mode-http}

Một tunnel HTTP-client. Tunnel kết nối đến đích được chỉ định bởi URL trong một yêu cầu HTTP. Hỗ trợ proxy ra internet nếu có outproxy được cung cấp. Loại bỏ các header sau khỏi kết nối HTTP:

- **Accept\*:** (không bao gồm "Accept" và "Accept-Encoding") vì chúng khác nhau rất nhiều giữa các trình duyệt và có thể được sử dụng làm định danh.
- **Referer:**
- **Via:**
- **From:**

HTTP client proxy cung cấp một số dịch vụ để bảo vệ người dùng và mang lại trải nghiệm người dùng tốt hơn.

**Xử lý header yêu cầu:** - Loại bỏ các header có vấn đề về quyền riêng tư - Định tuyến đến outproxy cục bộ hoặc từ xa - Lựa chọn outproxy, bộ nhớ đệm và theo dõi khả năng kết nối - Tra cứu hostname thành destination - Thay thế host header bằng b32 - Thêm header để chỉ ra hỗ trợ giải nén trong suốt - Buộc connection: close - Hỗ trợ proxy tuân thủ RFC - Xử lý và loại bỏ hop-by-hop header tuân thủ RFC - Xác thực digest và username/password cơ bản tùy chọn - Xác thực outproxy digest và username/password cơ bản tùy chọn - Đệm tất cả header trước khi truyền qua để tối ưu hiệu suất - Liên kết jump server - Xử lý jump response và form (address helper) - Xử lý blinded b32 và form thông tin xác thực - Hỗ trợ các yêu cầu HTTP và HTTPS (CONNECT) tiêu chuẩn

**Xử lý header phản hồi:** - Kiểm tra xem có nên giải nén phản hồi không - Buộc kết nối: đóng - Xử lý và loại bỏ header hop-by-hop tuân thủ RFC - Đệm tất cả các header trước khi chuyển qua để đảm bảo hiệu quả

**Phản hồi lỗi HTTP:** - Cho nhiều lỗi phổ biến và không phổ biến, để người dùng biết điều gì đã xảy ra - Hơn 20 trang lỗi độc đáo đã được dịch, định dạng và tạo kiểu cho các lỗi khác nhau - Máy chủ web nội bộ để phục vụ các biểu mẫu, CSS, hình ảnh và lỗi

#### Nén Phản Hồi Trong Suốt {#transparent-response-compression}

Việc nén phản hồi i2ptunnel được yêu cầu với HTTP header:

- **X-Accept-Encoding:** x-i2p-gzip;q=1.0, identity;q=0.5, deflate;q=0, gzip;q=0, *;q=0

Phía server sẽ loại bỏ header hop-by-hop này trước khi gửi yêu cầu đến web server. Header phức tạp với tất cả các giá trị q không cần thiết; các server chỉ cần tìm "x-i2p-gzip" ở bất kỳ đâu trong header.

Phía server quyết định có nén phản hồi hay không dựa trên các header nhận được từ webserver, bao gồm Content-Type, Content-Length, và Content-Encoding, để đánh giá xem phản hồi có thể nén được và có đáng để sử dụng thêm CPU hay không. Nếu phía server nén phản hồi, nó sẽ thêm HTTP header sau:

- **Content-Encoding:** x-i2p-gzip

Nếu header này có trong response, HTTP client proxy sẽ tự động giải nén nó một cách trong suốt. Phía client sẽ loại bỏ header này và gunzip trước khi gửi response đến trình duyệt. Lưu ý rằng chúng ta vẫn có nén gzip cơ bản ở lớp I2CP, vẫn hiệu quả nếu response không được nén ở lớp HTTP.

Thiết kế này và việc triển khai hiện tại vi phạm RFC 2616 theo một số cách:

- X-Accept-Encoding không phải là header tiêu chuẩn
- Không dechunk/chunk theo từng hop; nó chuyển tiếp chunking từ đầu đến cuối
- Chuyển tiếp Transfer-Encoding header từ đầu đến cuối
- Sử dụng Content-Encoding, không phải Transfer-Encoding, để chỉ định mã hóa theo từng hop
- Cấm x-i2p gzipping khi Content-Encoding được thiết lập (nhưng có lẽ chúng ta cũng không muốn làm điều đó)
- Phía server gzip việc chunking do server gửi, thay vì thực hiện dechunk-gzip-rechunk và dechunk-gunzip-rechunk
- Nội dung được gzipped không được chunked sau đó. RFC 2616 yêu cầu tất cả Transfer-Encoding khác "identity" phải được chunked.
- Vì không có chunking bên ngoài (sau) gzip, việc tìm điểm kết thúc của dữ liệu trở nên khó khăn hơn, làm cho việc triển khai keepalive khó khăn hơn.
- RFC 2616 nói Content-Length không được gửi nếu Transfer-Encoding có mặt, nhưng chúng ta vẫn làm. Đặc tả nói bỏ qua Content-Length nếu Transfer-Encoding có mặt, điều mà các trình duyệt thực hiện, nên nó hoạt động với chúng ta.

Các thay đổi để triển khai nén hop-by-hop tuân thủ tiêu chuẩn theo cách tương thích ngược là một chủ đề cần nghiên cứu thêm. Bất kỳ thay đổi nào đối với dechunk-gzip-rechunk sẽ yêu cầu một loại mã hóa mới, có thể là x-i2p-gzchunked. Điều này sẽ tương tự với Transfer-Encoding: gzip, nhưng sẽ phải được báo hiệu khác đi vì lý do tương thích. Bất kỳ thay đổi nào cũng sẽ yêu cầu một đề xuất chính thức.

#### Nén Yêu Cầu Trong Suốt {#transparent-request-compression}

Không được hỗ trợ, mặc dù POST sẽ có lợi. Lưu ý rằng chúng ta vẫn có nén gzip cơ bản ở tầng I2CP.

#### Tính bền vững {#persistence}

Các proxy máy khách và máy chủ hiện tại không hỗ trợ HTTP persistent sockets RFC 2616 trên bất kỳ hop nào trong ba hop (browser socket, I2P socket, server socket). Header Connection: close được chèn vào tại mỗi hop. Các thay đổi để triển khai tính bền vững đang được nghiên cứu. Những thay đổi này sẽ tuân thủ tiêu chuẩn và tương thích ngược, và sẽ không yêu cầu một đề xuất chính thức.

#### Pipelining {#pipelining}

Các proxy client và server hiện tại không hỗ trợ HTTP pipelining RFC 2616 và không có kế hoạch hỗ trợ tính năng này. Các trình duyệt hiện đại không hỗ trợ pipelining thông qua proxy vì hầu hết các proxy không thể triển khai nó một cách chính xác.

#### Tương thích {#compatibility}

Các triển khai proxy phải hoạt động chính xác với các triển khai khác ở phía bên kia. Proxy client nên hoạt động mà không cần proxy server có nhận thức HTTP (tức là một tunnel tiêu chuẩn) ở phía server. Không phải tất cả các triển khai đều hỗ trợ x-i2p-gzip.

#### User Agent {#user-agent}

Tùy thuộc vào việc tunnel có sử dụng outproxy hay không, nó sẽ thêm vào User-Agent sau:

- *Outproxy:* **User-Agent:** Sử dụng user agent từ phiên bản Firefox gần đây trên Windows
- *Sử dụng I2P nội bộ:* **User-Agent:** MYOB/6.66 (AN/ON)

### IRC Client {#client-mode-irc}

Tạo kết nối đến một máy chủ IRC ngẫu nhiên được chỉ định bởi danh sách các đích được phân cách bằng dấu phẩy (", "). Chỉ một tập hợp con các lệnh IRC được đưa vào danh sách trắng được cho phép do các mối lo ngại về tính ẩn danh.

Danh sách cho phép sau đây dành cho các lệnh đến từ máy chủ IRC tới máy khách IRC.

**Danh sách cho phép:** - AUTHENTICATE - CAP - ERROR - H - JOIN - KICK - MODE - NICK - PART - PING - PROTOCTL - QUIT - TOPIC - WALLOPS

Cũng có một danh sách cho phép cho các lệnh gửi ra từ IRC client đến IRC server. Danh sách này khá lớn do số lượng lệnh quản trị IRC nhiều. Xem mã nguồn IRCFilter.java để biết chi tiết.

Bộ lọc outbound cũng sửa đổi các lệnh sau để loại bỏ thông tin định danh: - NOTICE - PART - PING - PRIVMSG - QUIT - USER

### SOCKS 4/4a/5 {#client-mode-socks}

Cho phép sử dụng I2P router như một proxy SOCKS.

### SOCKS IRC {#client-mode-socks-irc}

Cho phép sử dụng I2P router như một SOCKS proxy với danh sách lệnh được chỉ định bởi chế độ client [IRC](#client-mode-irc).

### CONNECT {#client-mode-connect}

Tạo một tunnel HTTP và sử dụng phương thức HTTP request "CONNECT" để xây dựng một tunnel TCP thường được sử dụng cho SSL và HTTPS.

### Streamr {#client-mode-streamr}

Tạo một UDP-server gắn với một Streamr client I2PTunnel. Tunnel client streamr sẽ đăng ký với một tunnel server streamr.

![Sơ đồ Streamr](/images/I2PTunnel-streamr.png)

## Chế độ Máy chủ {#server-modes}

### Tiêu chuẩn {#server-mode-standard}

Tạo một destination đến ip:port cục bộ với cổng TCP mở.

### HTTP {#server-mode-http}

Tạo một destination đến máy chủ HTTP cục bộ ip:port. Hỗ trợ gzip cho các yêu cầu với Accept-encoding: x-i2p-gzip, trả lời với Content-encoding: x-i2p-gzip trong yêu cầu như vậy.

Proxy máy chủ HTTP cung cấp nhiều dịch vụ để giúp việc lưu trữ trang web dễ dàng và an toàn hơn, đồng thời mang lại trải nghiệm người dùng tốt hơn ở phía client.

**Xử lý header yêu cầu:** - Xác thực header - Bảo vệ chống giả mạo header - Kiểm tra kích thước header - Tùy chọn từ chối inproxy và user-agent - Thêm header X-I2P để webserver biết yêu cầu đến từ đâu - Thay thế host header để dễ dàng hơn cho webserver vhosts - Ép buộc connection: close - Xử lý và loại bỏ hop-by-hop header tuân thủ RFC - Đệm tất cả header trước khi chuyển tiếp để tăng hiệu suất

**Bảo vệ DDoS:** - Giới hạn POST - Bảo vệ timeout và slowloris - Giới hạn bổ sung xảy ra trong streaming cho tất cả các loại tunnel

**Xử lý header phản hồi:** - Loại bỏ một số header có vấn đề về quyền riêng tư - Kiểm tra mime type và các header khác để quyết định có nén phản hồi hay không - Ép buộc connection: close - Xử lý và loại bỏ hop-by-hop header tuân thủ RFC - Đệm tất cả header trước khi chuyển tiếp để tăng hiệu suất

**Phản hồi lỗi HTTP:** - Đối với nhiều lỗi phổ biến và không phổ biến cũng như việc điều tiết, để người dùng phía client biết điều gì đã xảy ra

**Nén phản hồi minh bạch:** - Máy chủ web và/hoặc lớp I2CP có thể nén, nhưng máy chủ web thường không làm vậy, và việc nén ở lớp cao là hiệu quả nhất, ngay cả khi I2CP cũng nén. Proxy máy chủ HTTP hoạt động phối hợp với proxy phía client để nén phản hồi một cách minh bạch.

### HTTP Hai chiều {#server-mode-http-bidir}

*Không còn được hỗ trợ*

Hoạt động như cả I2PTunnel HTTP Server và I2PTunnel HTTP client không có khả năng outproxy. Một ứng dụng ví dụ có thể là ứng dụng web thực hiện các yêu cầu kiểu client, hoặc kiểm tra loopback một I2P Site như một công cụ chẩn đoán.

### Máy chủ IRC {#server-mode-irc}

Tạo một destination lọc chuỗi đăng ký của client và chuyển khóa destination của client như một hostname tới IRC-server.

### Streamr {#server-mode-streamr}

Một UDP-client kết nối đến media server được tạo ra. UDP-Client được kết hợp với một Streamr server I2PTunnel.
