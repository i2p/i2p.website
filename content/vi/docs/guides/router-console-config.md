---
title: "Hướng dẫn Cấu hình Router Console"
description: "Hướng dẫn toàn diện để hiểu và cấu hình I2P Router Console"
slug: "router-console-config"
lastUpdated: "2025-11"
accurateFor: "2.10.0"
type: docs
---

Hướng dẫn này cung cấp tổng quan về Bảng điều khiển I2P Router và các trang cấu hình của nó. Mỗi phần giải thích chức năng của trang và mục đích sử dụng, giúp bạn hiểu cách giám sát và cấu hình I2P router của mình.

## Truy cập Router Console

I2P Router Console là trung tâm điều khiển chính để quản lý và giám sát router I2P của bạn. Theo mặc định, bạn có thể truy cập tại [I2P Router Console](http://127.0.0.1:7657/home) sau khi router I2P của bạn đã chạy.

![Router Console Home](/images/router-console-home.png)

Trang chủ hiển thị một số phần quan trọng:

- **Ứng dụng** - Truy cập nhanh các ứng dụng I2P tích hợp như Email, Torrents, Trình quản lý Hidden Services và Web Server
- **Trang cộng đồng I2P** - Liên kết đến các nguồn tài nguyên cộng đồng quan trọng bao gồm diễn đàn, tài liệu và trang web dự án
- **Cấu hình và Trợ giúp** - Công cụ để cấu hình băng thông, quản lý plugin và truy cập tài nguyên trợ giúp
- **Thông tin mạng và nhà phát triển** - Truy cập biểu đồ, nhật ký, tài liệu kỹ thuật và thống kê mạng

## Sổ Địa Chỉ

**URL:** [Address Book](http://127.0.0.1:7657/dns)

![Router Console Address Book](/images/router-console-address-book.png)

Sổ địa chỉ I2P hoạt động tương tự như DNS trên clearnet, cho phép bạn quản lý các tên dễ đọc cho các đích đến I2P (eepsites). Đây là nơi bạn có thể xem và thêm địa chỉ I2P vào sổ địa chỉ cá nhân của mình.

Hệ thống sổ địa chỉ hoạt động thông qua nhiều tầng:

- **Local Records** - Sổ địa chỉ cá nhân của bạn chỉ được lưu trữ trên router của bạn
  - **Local Addressbook** - Các host bạn thêm thủ công hoặc lưu lại cho mục đích sử dụng riêng
  - **Private Addressbook** - Các địa chỉ bạn không muốn chia sẻ với người khác; không bao giờ được phân phối công khai

- **Subscriptions** - Các nguồn sổ địa chỉ từ xa (như `http://i2p-projekt.i2p/hosts.txt`) tự động cập nhật sổ địa chỉ của router với các trang I2P đã biết

- **Router Addressbook** - Kết quả tổng hợp từ các bản ghi cục bộ và đăng ký của bạn, có thể tìm kiếm bởi tất cả các ứng dụng I2P trên router của bạn

- **Published Addressbook** - Tùy chọn chia sẻ công khai sổ địa chỉ của bạn để người khác sử dụng như một nguồn đăng ký (hữu ích nếu bạn đang vận hành một I2P site)

Sổ địa chỉ thường xuyên kiểm tra các đăng ký của bạn và hợp nhất nội dung vào sổ địa chỉ router của bạn, giữ cho tệp hosts.txt của bạn được cập nhật với mạng I2P.

## Cấu hình

**URL:** [Cấu hình Nâng cao](http://127.0.0.1:7657/configadvanced)

Phần Cấu hình cung cấp quyền truy cập vào tất cả các thiết lập router thông qua nhiều tab chuyên biệt.

### Advanced

![Router Console Advanced Configuration](/images/router-console-config-advanced.png)

Trang cấu hình Nâng cao cung cấp quyền truy cập vào các cài đặt router ở cấp độ thấp mà thường không cần thiết cho hoạt động bình thường. **Hầu hết người dùng không nên thay đổi các cài đặt này trừ khi họ hiểu rõ tùy chọn cấu hình cụ thể và tác động của nó đến hành vi của router.**

Các tính năng chính:

- **Cấu hình Floodfill** - Điều khiển việc router của bạn có tham gia với vai trò là floodfill peer hay không, giúp mạng lưới bằng cách lưu trữ và phân phối thông tin network database. Điều này có thể sử dụng nhiều tài nguyên hệ thống hơn nhưng giúp tăng cường mạng lưới I2P.

- **Cấu hình I2P nâng cao** - Truy cập trực tiếp vào tệp `router.config`, hiển thị tất cả các tham số cấu hình nâng cao bao gồm:
  - Giới hạn băng thông và cài đặt burst
  - Cài đặt transport (NTCP2, SSU2, cổng UDP và khóa)
  - Thông tin nhận dạng và phiên bản router
  - Tùy chọn console và cài đặt cập nhật

Hầu hết các tùy chọn cấu hình nâng cao không được hiển thị trong giao diện người dùng vì chúng hiếm khi cần thiết. Để bật chỉnh sửa các cài đặt này, bạn phải thêm `routerconsole.advanced=true` vào tệp `router.config` của mình theo cách thủ công.

**Cảnh báo:** Việc chỉnh sửa sai các cài đặt nâng cao có thể ảnh hưởng tiêu cực đến hiệu suất hoặc kết nối của router. Chỉ thay đổi các cài đặt này nếu bạn biết mình đang làm gì.

### Bandwidth

**URL:** [Cấu hình Băng thông](http://127.0.0.1:7657/config)

![Cấu hình Băng thông Router Console](/images/router-console-config-bandwidth.png)

Trang cấu hình Băng thông cho phép bạn kiểm soát lượng băng thông mà router của bạn đóng góp cho mạng I2P. I2P hoạt động tốt nhất khi bạn cấu hình tốc độ phù hợp với tốc độ kết nối internet của bạn.

**Các Cài Đặt Quan Trọng:**

- **KBps In** - Băng thông tối đa mà router của bạn sẽ chấp nhận khi nhận dữ liệu vào (tốc độ tải xuống)
- **KBps Out** - Băng thông tối đa mà router của bạn sẽ sử dụng khi gửi dữ liệu ra (tốc độ tải lên)
- **Share** - Phần trăm băng thông gửi đi được dành riêng cho lưu lượng tham gia (giúp định tuyến lưu lượng cho người dùng khác)

**Lưu ý Quan trọng:**

- Tất cả các giá trị được tính theo **byte trên giây** (KBps), không phải bit trên giây
- Càng cung cấp nhiều băng thông, bạn càng giúp ích cho mạng lưới và cải thiện tính ẩn danh của chính mình
- Lượng băng thông chia sẻ đường lên của bạn (KBps Out) quyết định mức độ đóng góp tổng thể của bạn cho mạng lưới
- Nếu bạn không chắc chắn về tốc độ mạng của mình, hãy sử dụng **Bandwidth Test** để đo kiểm tra
- Băng thông chia sẻ cao hơn giúp cải thiện tính ẩn danh của bạn và củng cố mạng lưới I2P

Trang cấu hình hiển thị lưu lượng dữ liệu truyền tải ước tính hàng tháng dựa trên cài đặt của bạn, giúp bạn lên kế hoạch phân bổ băng thông phù hợp với giới hạn gói internet của mình.

### Client Configuration

**URL:** [Cấu hình Client](http://127.0.0.1:7657/configclients)

![Cấu hình Client của Router Console](/images/router-console-config-clients.png)

Trang Cấu hình Client cho phép bạn kiểm soát các ứng dụng và dịch vụ I2P nào sẽ chạy khi khởi động. Đây là nơi bạn có thể bật hoặc tắt các client I2P tích hợp sẵn mà không cần gỡ cài đặt chúng.

**Cảnh báo quan trọng:** Hãy cẩn thận khi thay đổi các cài đặt ở đây. Router console và application tunnel là bắt buộc cho hầu hết các mục đích sử dụng I2P. Chỉ người dùng nâng cao mới nên chỉnh sửa các cài đặt này.

**Các Client Khả Dụng:**

- **Application tunnels** - Hệ thống I2PTunnel quản lý các tunnel client và server (HTTP proxy, IRC, v.v.)
- **I2P Router Console** - Giao diện quản trị dựa trên web mà bạn đang sử dụng
- **I2P webserver (eepsite)** - Webserver Jetty tích hợp sẵn để lưu trữ website I2P của riêng bạn
- **Open Router Console in web browser at startup** - Tự động mở trình duyệt đến trang chủ console khi khởi động
- **SAM application bridge** - Cầu nối API để các ứng dụng bên thứ ba kết nối với I2P

Mỗi client hiển thị: - **Chạy khi Khởi động?** - Hộp kiểm để bật/tắt tự động khởi chạy - **Điều khiển** - Các nút Bắt đầu/Dừng để kiểm soát ngay lập tức - **Class và arguments** - Thông tin kỹ thuật về cách client được khởi chạy

Các thay đổi đối với cài đặt "Run at Startup?" yêu cầu khởi động lại router để có hiệu lực. Tất cả các thay đổi được lưu vào `/var/lib/i2p/i2p-config/clients.config.d/`.

### Nâng cao

**URL:** [Cấu hình I2CP](http://127.0.0.1:7657/configi2cp)

![Router Console I2CP Configuration](/images/router-console-config-i2cp.png)

Trang cấu hình I2CP (I2P Client Protocol) cho phép bạn cấu hình cách các ứng dụng bên ngoài kết nối với I2P router của bạn. I2CP là giao thức mà các ứng dụng sử dụng để giao tiếp với router nhằm tạo tunnel và gửi/nhận dữ liệu qua I2P.

**Quan trọng:** Các cài đặt mặc định sẽ hoạt động tốt cho hầu hết mọi người. Mọi thay đổi được thực hiện ở đây cũng phải được cấu hình trong ứng dụng client bên ngoài. Nhiều client không hỗ trợ SSL hoặc xác thực. **Tất cả các thay đổi đều yêu cầu khởi động lại để có hiệu lực.**

**Các Tùy Chọn Cấu Hình:**

- **Cấu hình Giao diện I2CP Bên ngoài**
  - **Bật không có SSL** - Truy cập I2CP tiêu chuẩn (mặc định và tương thích nhất)
  - **Bật với yêu cầu SSL** - Chỉ cho phép kết nối I2CP được mã hóa
  - **Tắt** - Chặn các client bên ngoài kết nối qua I2CP

- **I2CP Interface** - Giao diện mạng để lắng nghe (mặc định: 127.0.0.1 chỉ cho localhost)
- **I2CP Port** - Số cổng cho các kết nối I2CP (mặc định: 7654)

- **Ủy quyền**
  - **Yêu cầu tên người dùng và mật khẩu** - Bật xác thực cho các kết nối I2CP
  - **Tên người dùng** - Đặt tên người dùng bắt buộc cho truy cập I2CP
  - **Mật khẩu** - Đặt mật khẩu bắt buộc cho truy cập I2CP

**Lưu ý Bảo mật:** Nếu bạn chỉ chạy các ứng dụng trên cùng một máy với I2P router của mình, hãy giữ giao diện ở `127.0.0.1` để ngăn chặn truy cập từ xa. Chỉ thay đổi các cài đặt này nếu bạn cần cho phép các ứng dụng I2P từ thiết bị khác kết nối với router của bạn.

### Băng thông

**URL:** [Cấu Hình Mạng](http://127.0.0.1:7657/confignet)

![Router Console Network Configuration](/images/router-console-config-network.png)

Trang Cấu hình Mạng cho phép bạn cấu hình cách I2P router của bạn kết nối với internet, bao gồm phát hiện địa chỉ IP, tùy chọn IPv4/IPv6, và cài đặt cổng cho cả UDP và TCP transport.

**Địa chỉ IP có thể truy cập từ bên ngoài:**

- **Sử dụng tất cả phương thức tự động phát hiện** - Tự động phát hiện IP công khai của bạn bằng nhiều phương thức (khuyến nghị)
- **Vô hiệu hóa phát hiện địa chỉ IP qua UPnP** - Ngăn việc sử dụng UPnP để khám phá IP của bạn
- **Bỏ qua địa chỉ IP giao diện cục bộ** - Không sử dụng IP mạng nội bộ của bạn
- **Chỉ sử dụng phát hiện địa chỉ IP qua SSU** - Chỉ sử dụng giao thức truyền tải SSU2 để phát hiện IP
- **Chế độ ẩn - không công bố IP** - Ngăn tham gia vào luồng dữ liệu mạng (giảm tính ẩn danh)
- **Chỉ định hostname hoặc IP** - Thiết lập thủ công IP công khai hoặc hostname của bạn

**Cấu hình IPv4:**

- **Vô hiệu hóa kết nối đến (Firewalled)** - Chọn tùy chọn này nếu bạn đang ở sau tường lửa, mạng gia đình, ISP, DS-Lite, hoặc carrier-grade NAT chặn các kết nối đến

**Cấu hình IPv6:**

- **Ưu tiên IPv4 hơn IPv6** - Ưu tiên các kết nối IPv4
- **Ưu tiên IPv6 hơn IPv4** - Ưu tiên các kết nối IPv6 (mặc định cho mạng dual-stack)
- **Bật IPv6** - Cho phép các kết nối IPv6
- **Tắt IPv6** - Vô hiệu hóa toàn bộ kết nối IPv6
- **Chỉ sử dụng IPv6 (tắt IPv4)** - Chế độ chỉ IPv6 thử nghiệm
- **Tắt kết nối đến (Firewalled)** - Kiểm tra xem IPv6 của bạn có bị tường lửa chặn không

**Hành Động Khi IP Thay Đổi:**

- **Laptop mode** - Tính năng thử nghiệm thay đổi danh tính router và cổng UDP khi địa chỉ IP của bạn thay đổi để tăng cường tính ẩn danh

**Cấu hình UDP:**

- **Chỉ định cổng** - Đặt một cổng UDP cụ thể cho giao thức truyền tải SSU2 (phải được mở trong tường lửa của bạn)
- **Tắt hoàn toàn** - Chỉ chọn nếu đứng sau tường lửa chặn tất cả UDP đi ra ngoài

**Cấu hình TCP:**

- **Chỉ định cổng** - Đặt một cổng TCP cụ thể cho giao vận NTCP2 (phải được mở trong tường lửa của bạn)
- **Sử dụng cùng cổng đã cấu hình cho UDP** - Đơn giản hóa cấu hình bằng cách sử dụng một cổng cho cả hai giao vận
- **Sử dụng địa chỉ IP tự động phát hiện** - Tự động phát hiện địa chỉ IP công khai của bạn (hiển thị "currently unknown" nếu chưa được phát hiện hoặc bị chặn bởi tường lửa)
- **Luôn sử dụng địa chỉ IP tự động phát hiện (Không có tường lửa)** - Tốt nhất cho các router có kết nối internet trực tiếp
- **Vô hiệu hóa kết nối đến (Có tường lửa)** - Chọn nếu các kết nối TCP bị chặn bởi tường lửa của bạn
- **Vô hiệu hóa hoàn toàn** - Chỉ chọn nếu đằng sau tường lửa hạn chế hoặc chặn TCP đi ra
- **Chỉ định hostname hoặc IP** - Cấu hình thủ công địa chỉ có thể truy cập từ bên ngoài của bạn

**Quan trọng:** Các thay đổi đối với cấu hình mạng có thể yêu cầu khởi động lại router để có hiệu lực đầy đủ. Cấu hình chuyển tiếp cổng (port forwarding) đúng cách sẽ cải thiện đáng kể hiệu suất router của bạn và giúp ích cho mạng I2P.

### Cấu hình Client

**URL:** [Cấu hình Peer](http://127.0.0.1:7657/configpeer)

![Router Console Peer Configuration](/images/router-console-config-peer.png)

Trang Cấu hình Peer cung cấp các điều khiển thủ công để quản lý từng peer riêng lẻ trên mạng I2P. Đây là tính năng nâng cao thường chỉ được sử dụng để khắc phục sự cố các peer có vấn đề.

**Điều Khiển Peer Thủ Công:**

- **Router Hash** - Nhập router hash dạng base64 gồm 44 ký tự của peer mà bạn muốn quản lý

**Chặn / Bỏ chặn một Peer thủ công:**

Cấm một peer ngăn chặn họ tham gia vào bất kỳ tunnel nào bạn tạo ra. Hành động này: - Ngăn peer được sử dụng trong các tunnel của client hoặc exploratory tunnel của bạn - Có hiệu lực ngay lập tức mà không cần khởi động lại - Duy trì cho đến khi bạn thủ công bỏ cấm peer hoặc khởi động lại router của bạn - **Cấm peer cho đến khi khởi động lại** - Tạm thời chặn peer - **Bỏ cấm peer** - Gỡ bỏ lệnh cấm trên một peer đã bị chặn trước đó

**Điều Chỉnh Bonus Của Profile:**

Điểm thưởng hồ sơ ảnh hưởng đến cách các peer được chọn để tham gia tunnel. Điểm thưởng có thể là dương hoặc âm: - **Fast peers** - Được sử dụng cho client tunnel yêu cầu tốc độ cao - **High Capacity peers** - Được sử dụng cho một số exploratory tunnel yêu cầu định tuyến ổn định - Điểm thưởng hiện tại được hiển thị trên trang profiles

**Cấu hình:** - **Tốc độ** - Điều chỉnh điểm thưởng tốc độ cho peer này (0 = trung lập) - **Dung lượng** - Điều chỉnh điểm thưởng dung lượng cho peer này (0 = trung lập) - **Điều chỉnh điểm thưởng peer** - Áp dụng các thiết lập điểm thưởng

**Trường hợp sử dụng:** - Cấm một peer liên tục gây ra vấn đề kết nối - Tạm thời loại trừ một peer mà bạn nghi ngờ là độc hại - Điều chỉnh điểm thưởng để giảm ưu tiên các peer hoạt động kém - Gỡ lỗi các vấn đề xây dựng tunnel bằng cách loại trừ các peer cụ thể

**Lưu ý:** Hầu hết người dùng sẽ không bao giờ cần sử dụng tính năng này. Router I2P tự động quản lý việc chọn lựa và phân tích peer dựa trên các chỉ số hiệu suất.

### Cấu hình I2CP

**URL:** [Cấu hình Reseed](http://127.0.0.1:7657/configreseed)

![Cấu hình Reseed của Router Console](/images/router-console-config-reseed.png)

Trang Cấu hình Reseed cho phép bạn thực hiện reseed thủ công cho router của mình nếu quá trình reseed tự động thất bại. Reseed là quá trình khởi động được sử dụng để tìm các router khác khi bạn lần đầu cài đặt I2P, hoặc khi router của bạn còn quá ít thông tin tham chiếu router.

**Khi Nào Nên Sử Dụng Reseed Thủ Công:**

1. Nếu reseed thất bại, bạn nên kiểm tra kết nối mạng trước
2. Nếu tường lửa chặn kết nối của bạn đến các máy chủ reseed, bạn có thể sử dụng proxy:
   - Proxy có thể là proxy công khai từ xa, hoặc có thể đang chạy trên máy tính của bạn (localhost)
   - Để sử dụng proxy, hãy cấu hình loại, host và port trong phần Reseeding Configuration
   - Nếu bạn đang chạy Tor Browser, hãy reseed thông qua nó bằng cách cấu hình SOCKS 5, localhost, port 9150
   - Nếu bạn đang chạy Tor dòng lệnh, hãy reseed thông qua nó bằng cách cấu hình SOCKS 5, localhost, port 9050
   - Nếu bạn có một số peer nhưng cần thêm, bạn có thể thử tùy chọn I2P Outproxy. Để trống host và port. Tùy chọn này sẽ không hoạt động cho reseed ban đầu khi bạn chưa có peer nào
   - Sau đó, nhấp "Save changes and reseed now"
   - Cài đặt mặc định sẽ phù hợp với hầu hết mọi người. Chỉ thay đổi những cài đặt này nếu HTTPS bị chặn bởi tường lửa nghiêm ngặt và reseed đã thất bại

3. Nếu bạn biết và tin tưởng ai đó đang chạy I2P, hãy yêu cầu họ gửi cho bạn một tệp reseed được tạo bằng trang này trên bảng điều khiển router của họ. Sau đó, sử dụng trang này để reseed với tệp bạn đã nhận. Đầu tiên, chọn tệp bên dưới. Tiếp theo, nhấp vào "Reseed from file"

4. Nếu bạn biết và tin tưởng ai đó công bố các tệp reseed, hãy hỏi họ để lấy URL. Sau đó, sử dụng trang này để reseed với URL bạn nhận được. Đầu tiên, nhập URL vào bên dưới. Tiếp theo, nhấp vào "Reseed from URL"

5. Xem [câu hỏi thường gặp (FAQ)](/docs/overview/faq/) để biết hướng dẫn reseed thủ công

**Tùy chọn Reseed Thủ công:**

- **Reseed từ URL** - Nhập URL zip hoặc su3 từ nguồn đáng tin cậy và nhấp vào "Reseed from URL"
  - Định dạng su3 được ưu tiên vì nó sẽ được xác minh là đã được ký bởi nguồn đáng tin cậy
  - Định dạng zip không được ký; chỉ sử dụng tệp zip từ nguồn mà bạn tin tưởng

- **Reseed từ File** - Duyệt và chọn một file zip hoặc su3 cục bộ, sau đó nhấp vào "Reseed from file"
  - Bạn có thể tìm các file reseed tại [checki2p.com/reseed](https://checki2p.com/reseed)

- **Tạo File Reseed** - Tạo một file zip reseed mới mà bạn có thể chia sẻ cho người khác để reseed thủ công
  - File này sẽ không bao giờ chứa danh tính hoặc IP của router của bạn

**Cấu hình Reseeding:**

Cài đặt mặc định sẽ hoạt động cho hầu hết người dùng. Chỉ thay đổi những cài đặt này nếu HTTPS bị chặn bởi tường lửa hạn chế và reseed đã thất bại.

- **URL Reseed** - Danh sách các URL HTTPS đến máy chủ reseed (danh sách mặc định được tích hợp sẵn và cập nhật thường xuyên)
- **Cấu hình Proxy** - Cấu hình HTTP/HTTPS/SOCKS proxy nếu bạn cần truy cập máy chủ reseed thông qua proxy
- **Đặt lại danh sách URL** - Khôi phục danh sách máy chủ reseed mặc định

**Quan trọng:** Việc reseed thủ công chỉ cần thiết trong những trường hợp hiếm hoi khi reseed tự động thất bại liên tục. Hầu hết người dùng sẽ không bao giờ cần sử dụng trang này.

### Cấu hình Mạng

**URL:** [Cấu hình Router Family](http://127.0.0.1:7657/configfamily)

![Cấu hình Router Family trên Router Console](/images/router-console-config-family.png)

Trang Cấu hình Router Family cho phép bạn quản lý các họ router. Các router trong cùng một họ chia sẻ một family key, xác định chúng được vận hành bởi cùng một người hoặc tổ chức. Điều này ngăn chặn nhiều router do bạn kiểm soát được chọn cho cùng một tunnel, việc này sẽ làm giảm tính ẩn danh.

**Router Family là gì?**

Khi bạn vận hành nhiều router I2P, bạn nên cấu hình chúng thuộc cùng một family. Điều này đảm bảo: - Các router của bạn sẽ không được sử dụng cùng nhau trong cùng một đường tunnel - Những người dùng khác duy trì tính ẩn danh phù hợp khi tunnel của họ sử dụng các router của bạn - Mạng lưới có thể phân phối việc tham gia tunnel một cách hợp lý

**Family Hiện tại:**

Trang này hiển thị tên family của router hiện tại của bạn. Nếu bạn không thuộc family nào, trường này sẽ để trống.

**Xuất Khóa Họ (Family Key):**

- **Xuất khóa bí mật của family để nhập vào các router khác mà bạn kiểm soát**
- Nhấp "Export Family Key" để tải xuống tệp khóa family của bạn
- Nhập khóa này vào các router khác của bạn để thêm chúng vào cùng một family

**Rời Khỏi Router Family:**

- **Không còn là thành viên của family**
- Nhấp "Leave Family" để loại bỏ router này khỏi family hiện tại
- Hành động này không thể hoàn tác nếu không nhập lại khóa family

**Những Điểm Quan Trọng Cần Lưu Ý:**

- **Yêu Cầu Đăng Ký Công Khai:** Để family của bạn được công nhận trên toàn mạng lưới, khóa family của bạn phải được thêm vào codebase I2P bởi nhóm phát triển. Điều này đảm bảo tất cả các router trên mạng lưới đều biết về family của bạn.
- **Liên hệ với nhóm I2P** để đăng ký khóa family nếu bạn vận hành nhiều router công khai
- Hầu hết người dùng chỉ chạy một router sẽ không bao giờ cần sử dụng tính năng này
- Cấu hình family chủ yếu được sử dụng bởi các nhà vận hành nhiều router công khai hoặc nhà cung cấp hạ tầng

**Các Trường Hợp Sử Dụng:**

- Vận hành nhiều router I2P để đảm bảo dự phòng
- Chạy cơ sở hạ tầng như reseed server hoặc outproxy trên nhiều máy
- Quản lý mạng lưới các router I2P cho một tổ chức

### Cấu hình Peer

**URL:** [Cấu hình Tunnel](http://127.0.0.1:7657/configtunnels)

![Cấu hình Tunnel trên Router Console](/images/router-console-config-tunnels.png)

Trang Cấu hình Tunnel cho phép bạn điều chỉnh cài đặt tunnel mặc định cho cả exploratory tunnel (dùng cho giao tiếp router) và client tunnel (dùng bởi các ứng dụng). **Cài đặt mặc định phù hợp với hầu hết mọi người và chỉ nên thay đổi nếu bạn hiểu rõ những đánh đổi.**

**Cảnh Báo Quan Trọng:**

⚠️ **Đánh đổi giữa Tính ẩn danh và Hiệu suất:** Có một sự đánh đổi cơ bản giữa tính ẩn danh và hiệu suất. Các tunnel dài hơn 3 hops (ví dụ 2 hops + 0-2 hops, 3 hops + 0-1 hops, 3 hops + 0-2 hops), hoặc số lượng + số lượng dự phòng cao, có thể làm giảm nghiêm trọng hiệu suất hoặc độ tin cậy. Việc sử dụng CPU cao và/hoặc băng thông đầu ra cao có thể xảy ra. Thay đổi các cài đặt này một cách cẩn thận và điều chỉnh chúng nếu bạn gặp vấn đề.

⚠️ **Tính bền vững:** Các thay đổi cài đặt exploratory tunnel được lưu trong file router.config. Các thay đổi client tunnel chỉ là tạm thời và không được lưu lại. Để thực hiện thay đổi client tunnel vĩnh viễn, xem [trang I2PTunnel](/docs/api/i2ptunnel).

**Exploratory Tunnels:**

Các tunnel khám phá (exploratory tunnels) được router của bạn sử dụng để giao tiếp với network database và tham gia vào mạng I2P.

Các tùy chọn cấu hình cho cả Inbound và Outbound: - **Length** - Số lượng hop trong tunnel (mặc định: 2-3 hop) - **Randomization** - Độ biến thiên ngẫu nhiên trong độ dài tunnel (mặc định: 0-1 hop) - **Quantity** - Số lượng tunnel đang hoạt động (mặc định: 2 tunnel) - **Backup quantity** - Số lượng tunnel dự phòng sẵn sàng kích hoạt (mặc định: 0 tunnel)

**Client Tunnels cho I2P Webserver:**

Các cài đặt này kiểm soát các tunnel cho máy chủ web I2P tích hợp sẵn (eepsite).

⚠️ **CẢNH BÁO VỀ TÍNH ẨN DANH** - Cài đặt bao gồm các tunnel 1-hop. ⚠️ **CẢNH BÁO VỀ HIỆU SUẤT** - Cài đặt bao gồm số lượng tunnel cao.

Các tùy chọn cấu hình cho cả Inbound và Outbound: - **Length** - Độ dài tunnel (mặc định: 1 hop cho webserver) - **Randomization** - Phương sai ngẫu nhiên trong độ dài tunnel - **Quantity** - Số lượng tunnel đang hoạt động - **Backup quantity** - Số lượng tunnel dự phòng

**Tunnel Client cho Các Client Dùng Chung:**

Các cài đặt này áp dụng cho các ứng dụng client dùng chung (HTTP proxy, IRC, v.v.).

Các tùy chọn cấu hình cho cả Inbound và Outbound: - **Length** - Độ dài tunnel (mặc định: 3 hops) - **Randomization** - Phương sai ngẫu nhiên trong độ dài tunnel - **Quantity** - Số lượng tunnel hoạt động - **Backup quantity** - Số lượng tunnel dự phòng

**Hiểu về các Tham số Tunnel:**

- **Độ dài:** Đường hầm dài hơn cung cấp tính ẩn danh cao hơn nhưng làm giảm hiệu suất và độ tin cậy
- **Ngẫu nhiên hóa:** Tăng tính không thể đoán trước cho đường đi của đường hầm, cải thiện bảo mật
- **Số lượng:** Nhiều đường hầm hơn cải thiện độ tin cậy và phân phối tải nhưng tăng mức sử dụng tài nguyên
- **Số lượng dự phòng:** Các đường hầm được xây dựng sẵn để thay thế đường hầm bị lỗi, cải thiện khả năng phục hồi

**Các Phương Pháp Hay Nhất:**

- Giữ nguyên cài đặt mặc định trừ khi bạn có nhu cầu cụ thể
- Chỉ tăng độ dài tunnel nếu tính ẩn danh là quan trọng và bạn có thể chấp nhận hiệu suất chậm hơn
- Tăng số lượng/backup chỉ khi gặp phải tình trạng tunnel thường xuyên bị lỗi
- Giám sát hiệu suất router sau khi thực hiện thay đổi
- Nhấp vào "Save changes" để áp dụng các thay đổi

### Cấu hình Reseed

**URL:** [Cấu hình giao diện người dùng](http://127.0.0.1:7657/configui)

![Cấu hình giao diện Router Console](/images/router-console-config-ui.png)

Trang Cấu hình Giao diện cho phép bạn tùy chỉnh giao diện và khả năng truy cập của bảng điều khiển router, bao gồm lựa chọn giao diện, tùy chọn ngôn ngữ và bảo vệ bằng mật khẩu.

**Giao diện Router Console:**

Chọn giữa giao diện tối và sáng cho bảng điều khiển router: - **Dark** - Giao diện chế độ tối (dễ nhìn hơn trong môi trường thiếu ánh sáng) - **Light** - Giao diện chế độ sáng (giao diện truyền thống)

Các tùy chọn giao diện bổ sung: - **Áp dụng giao diện thống nhất cho tất cả các ứng dụng** - Áp dụng giao diện đã chọn cho tất cả các ứng dụng I2P, không chỉ router console - **Bắt buộc sử dụng giao diện di động** - Sử dụng giao diện tối ưu hóa cho di động ngay cả trên trình duyệt máy tính để bàn - **Nhúng ứng dụng Email và Torrent vào console** - Tích hợp Susimail và I2PSnark trực tiếp vào giao diện console thay vì mở chúng trong các tab riêng biệt

**Ngôn ngữ Router Console:**

Chọn ngôn ngữ ưa thích của bạn cho giao diện router console từ menu thả xuống. I2P hỗ trợ nhiều ngôn ngữ bao gồm tiếng Anh, tiếng Đức, tiếng Pháp, tiếng Tây Ban Nha, tiếng Nga, tiếng Trung, tiếng Nhật và nhiều ngôn ngữ khác.

**Chào mừng đóng góp bản dịch:** Nếu bạn nhận thấy bản dịch chưa hoàn chỉnh hoặc không chính xác, bạn có thể giúp cải thiện I2P bằng cách đóng góp vào dự án dịch thuật. Liên hệ với các nhà phát triển tại #i2p-dev trên IRC hoặc kiểm tra báo cáo tình trạng bản dịch (được liên kết trên trang).

**Mật khẩu Router Console:**

Thêm xác thực tên người dùng và mật khẩu để bảo vệ quyền truy cập vào router console của bạn:

- **Username** - Nhập tên người dùng để truy cập bảng điều khiển
- **Password** - Nhập mật khẩu để truy cập bảng điều khiển
- **Add user** - Tạo người dùng mới với thông tin xác thực đã chỉ định
- **Delete selected** - Xóa các tài khoản người dùng hiện có

**Tại Sao Cần Thêm Mật Khẩu?**

- Ngăn chặn truy cập trái phép vào router console từ máy cục bộ
- Thiết yếu nếu nhiều người sử dụng máy tính của bạn
- Khuyến nghị nếu router console của bạn có thể truy cập được trên mạng cục bộ
- Bảo vệ cấu hình I2P và cài đặt quyền riêng tư của bạn khỏi bị can thiệp

**Lưu ý Bảo mật:** Bảo vệ bằng mật khẩu chỉ ảnh hưởng đến quyền truy cập vào giao diện web bảng điều khiển router tại [I2P Router Console](http://127.0.0.1:7657). Nó không mã hóa lưu lượng I2P hoặc ngăn chặn các ứng dụng sử dụng I2P. Nếu bạn là người dùng duy nhất trên máy tính của mình và bảng điều khiển router chỉ lắng nghe trên localhost (mặc định), mật khẩu có thể không cần thiết.

### Cấu hình Router Family

**URL:** [Cấu hình WebApp](http://127.0.0.1:7657/configwebapps)

![Cấu hình WebApp của Router Console](/images/router-console-config-webapps.png)

Trang Cấu hình WebApp cho phép bạn quản lý các ứng dụng web Java chạy trong router I2P của bạn. Các ứng dụng này được khởi động bởi webConsole client và chạy trong cùng JVM với router, cung cấp các chức năng tích hợp có thể truy cập thông qua router console.

**WebApps là gì?**

WebApps là các ứng dụng dựa trên Java có thể là: - **Ứng dụng hoàn chỉnh** (ví dụ: I2PSnark cho torrents) - **Giao diện cho các client khác** phải được kích hoạt riêng (ví dụ: Susidns, I2PTunnel) - **Ứng dụng web không có giao diện web** (ví dụ: address book)

**Ghi Chú Quan Trọng:**

- Một webapp có thể bị vô hiệu hóa hoàn toàn, hoặc chỉ bị vô hiệu hóa khỏi việc chạy khi khởi động
- Xóa file war khỏi thư mục webapps sẽ vô hiệu hóa webapp hoàn toàn
- Tuy nhiên, file .war và thư mục webapp sẽ xuất hiện lại khi bạn cập nhật router lên phiên bản mới hơn
- **Để vô hiệu hóa webapp vĩnh viễn:** Vô hiệu hóa nó tại đây, đây là phương pháp được khuyến nghị

**Các WebApp Có Sẵn:**

| WebApp | Description |
|--------|-------------|
| **i2psnark** | Torrents - Built-in BitTorrent client for I2P |
| **i2ptunnel** | Hidden Services Manager - Configure client and server tunnels |
| **imagegen** | Identification Image Generator - Creates unique identicons |
| **jsonrpc** | jsonrpc.war - JSON-RPC API interface (disabled by default) |
| **routerconsole** | I2P Router Console - The main administrative interface |
| **susidns** | Address Book - Manage I2P addresses and subscriptions |
| **susimail** | Email - Web-based email client for I2P |
**Các điều khiển:**

Cho mỗi webapp: - **Chạy khi Khởi động?** - Hộp kiểm để bật/tắt tự động khởi động - **Điều khiển** - Các nút Bắt đầu/Dừng để điều khiển ngay lập tức   - **Dừng** - Dừng webapp đang chạy   - **Bắt đầu** - Khởi động một webapp đã dừng

**Các Nút Cấu Hình:**

- **Hủy** - Hủy bỏ các thay đổi và quay lại trang trước
- **Lưu Cấu hình WebApp** - Lưu các thay đổi của bạn và áp dụng chúng

**Các Trường Hợp Sử Dụng:**

- Dừng I2PSnark nếu bạn không sử dụng torrents để tiết kiệm tài nguyên
- Vô hiệu hóa jsonrpc nếu bạn không cần truy cập API
- Dừng Susimail nếu bạn sử dụng ứng dụng email bên ngoài
- Tạm thời dừng các webapp để giải phóng bộ nhớ hoặc khắc phục sự cố

**Mẹo Hiệu Năng:** Tắt các webapp không sử dụng có thể giảm mức sử dụng bộ nhớ và cải thiện hiệu năng router, đặc biệt trên các hệ thống có tài nguyên hạn chế.

## Help

**URL:** [Trợ giúp](http://127.0.0.1:7657/help)

Trang Trợ giúp cung cấp tài liệu và tài nguyên toàn diện để giúp bạn hiểu và sử dụng I2P một cách hiệu quả. Nó đóng vai trò là trung tâm cho việc khắc phục sự cố, học tập và nhận hỗ trợ.

**Những Gì Bạn Sẽ Tìm Thấy:**

- **Hướng dẫn Khởi động Nhanh** - Thông tin cần thiết cho người dùng mới bắt đầu với I2P
- **Câu hỏi Thường gặp (FAQ)** - Câu trả lời cho các câu hỏi phổ biến về cài đặt, cấu hình và sử dụng I2P
- **Khắc phục Sự cố** - Giải pháp cho các vấn đề thường gặp và sự cố kết nối
- **Tài liệu Kỹ thuật** - Thông tin chi tiết về các giao thức, kiến trúc và đặc tả kỹ thuật của I2P
- **Hướng dẫn Ứng dụng** - Hướng dẫn sử dụng các ứng dụng I2P như torrents, email và hidden services
- **Thông tin Mạng** - Hiểu cách I2P hoạt động và điều gì làm cho nó an toàn
- **Tài nguyên Hỗ trợ** - Liên kết đến diễn đàn, kênh IRC và hỗ trợ cộng đồng

**Nhận trợ giúp:**

Nếu bạn đang gặp vấn đề với I2P: 1. Kiểm tra FAQ để tìm các câu hỏi và câu trả lời thường gặp 2. Xem lại phần khắc phục sự cố cho vấn đề cụ thể của bạn 3. Truy cập diễn đàn I2P tại [i2pforum.i2p](http://i2pforum.i2p) hoặc [i2pforum.net](https://i2pforum.net) 4. Tham gia kênh IRC #i2p để nhận hỗ trợ từ cộng đồng theo thời gian thực 5. Tìm kiếm trong tài liệu để có thông tin kỹ thuật chi tiết

**Mẹo:** Trang trợ giúp luôn có thể truy cập từ thanh bên của bảng điều khiển router, giúp bạn dễ dàng tìm thấy hỗ trợ bất cứ khi nào cần.

## Performance Graphs

**URL:** [Biểu đồ Hiệu năng](http://127.0.0.1:7657/graphs)

![Biểu đồ hiệu suất Router Console](/images/router-console-graphs.png)

Trang Đồ thị Hiệu suất cung cấp giám sát trực quan theo thời gian thực về hiệu suất và hoạt động mạng của I2P router. Những đồ thị này giúp bạn hiểu về mức sử dụng băng thông, kết nối peer, mức tiêu thụ bộ nhớ và tình trạng tổng thể của router.

**Các Đồ thị Khả dụng:**

- **Sử dụng Băng thông**
  - **Tốc độ gửi cấp thấp (bytes/giây)** - Tốc độ lưu lượng đi
  - **Tốc độ nhận cấp thấp (bytes/giây)** - Tốc độ lưu lượng đến
  - Hiển thị mức sử dụng băng thông hiện tại, trung bình và tối đa
  - Giúp theo dõi xem bạn có đang đạt đến giới hạn băng thông đã cấu hình hay không

- **Active Peers (Peer đang hoạt động)**
  - **router.activePeers averaged for 60 sec** - Số lượng peer bạn đang giao tiếp tích cực
  - Hiển thị tình trạng kết nối mạng của bạn
  - Nhiều peer đang hoạt động thường có nghĩa là xây dựng tunnel tốt hơn và tham gia mạng hiệu quả hơn

- **Mức sử dụng bộ nhớ Router**
  - **router.memoryUsed được lấy trung bình trong 60 giây** - Mức tiêu thụ bộ nhớ JVM
  - Hiển thị mức sử dụng bộ nhớ hiện tại, trung bình và tối đa tính bằng MB
  - Hữu ích để xác định rò rỉ bộ nhớ hoặc xác định liệu bạn có cần tăng kích thước heap của Java hay không

**Cấu hình Hiển thị Đồ thị:**

Tùy chỉnh cách hiển thị và làm mới đồ thị:

- **Kích thước đồ thị** - Đặt chiều rộng (mặc định: 400 pixel) và chiều cao (mặc định: 100 pixel)
- **Khoảng thời gian hiển thị** - Phạm vi thời gian để hiển thị (mặc định: 60 phút)
- **Độ trễ làm mới** - Tần suất cập nhật đồ thị (mặc định: 5 phút)
- **Kiểu biểu đồ** - Chọn giữa hiển thị dạng Trung bình hoặc Sự kiện
- **Ẩn chú thích** - Loại bỏ chú thích khỏi đồ thị để tiết kiệm không gian
- **UTC** - Sử dụng giờ UTC thay vì giờ địa phương trên đồ thị
- **Lưu trữ dữ liệu** - Lưu trữ dữ liệu đồ thị trên ổ đĩa để phân tích lịch sử

**Tùy chọn Nâng cao:**

Nhấp vào **[Select Stats]** để chọn số liệu thống kê muốn vẽ đồ thị: - Các chỉ số tunnel (tỷ lệ tạo thành công, số lượng tunnel, v.v.) - Thống kê cơ sở dữ liệu mạng - Thống kê truyền tải (NTCP2, SSU2) - Hiệu suất tunnel client - Và nhiều chỉ số chi tiết khác

**Các Trường Hợp Sử Dụng:**

- Theo dõi băng thông để đảm bảo bạn không vượt quá giới hạn đã cấu hình
- Xác minh kết nối peer khi khắc phục sự cố mạng
- Theo dõi mức sử dụng bộ nhớ để tối ưu hóa cài đặt Java heap
- Nhận diện các mẫu hiệu suất theo thời gian
- Chẩn đoán vấn đề xây dựng tunnel bằng cách tương quan các biểu đồ

**Mẹo:** Nhấp vào "Save settings and redraw graphs" sau khi thực hiện thay đổi để áp dụng cấu hình của bạn. Các biểu đồ sẽ tự động làm mới dựa trên cài đặt độ trễ làm mới của bạn.
