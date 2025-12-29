---
title: "Nâng cao kỹ năng I2P của bạn với LeaseSets được mã hóa"
date: 2021-09-07
slug: "level-up-your-i2p-skills-with-encrypted-leasesets"
author: "idk"
description: "Có ý kiến cho rằng I2P nhấn mạnh vào các dịch vụ ẩn; chúng tôi xem xét một cách diễn giải về điều này."
categories: ["general"]
---

## Nâng cao kỹ năng I2P của bạn với LeaseSets được mã hóa

Trước đây từng có ý kiến cho rằng I2P nhấn mạnh việc hỗ trợ các dịch vụ ẩn, điều này đúng theo nhiều khía cạnh. Tuy nhiên, điều đó không phải lúc nào cũng có cùng ý nghĩa đối với người dùng, nhà phát triển và quản trị viên dịch vụ ẩn. LeaseSets được mã hóa và các trường hợp sử dụng của chúng mang lại một góc nhìn độc đáo, thực tiễn về cách I2P giúp dịch vụ ẩn linh hoạt hơn, dễ quản trị hơn, cũng như cách I2P mở rộng khái niệm dịch vụ ẩn để mang lại lợi ích bảo mật cho các trường hợp sử dụng tiềm năng, đáng chú ý.

## LeaseSet là gì?

Khi bạn tạo một dịch vụ ẩn, bạn sẽ công bố một thứ gọi là "LeaseSet" (tập các Lease) lên I2P NetDB. "LeaseSet", nói một cách đơn giản nhất, là thứ mà những người dùng I2P khác cần để khám phá "ở đâu" dịch vụ ẩn của bạn nằm trên mạng I2P. Nó chứa các "Leases" dùng để xác định các tunnels có thể được sử dụng để truy cập dịch vụ ẩn của bạn, và khóa công khai của destination (đích), mà các ứng dụng khách sẽ dùng để mã hóa các thông điệp gửi tới. Loại dịch vụ ẩn này có thể được truy cập bởi bất kỳ ai có địa chỉ, và có lẽ là trường hợp sử dụng phổ biến nhất hiện nay.

Đôi khi, bạn có thể không muốn cho phép các dịch vụ ẩn của mình được bất kỳ ai truy cập. Một số người sử dụng dịch vụ ẩn như một cách để truy cập vào máy chủ SSH trên PC tại nhà, hoặc để kết nối các thiết bị IoT thành một mạng. Trong những trường hợp này, việc làm cho dịch vụ ẩn của bạn có thể được mọi người trên mạng I2P truy cập là không cần thiết, thậm chí có thể phản tác dụng. Đây là lúc "Encrypted LeaseSets" phát huy tác dụng.

## LeaseSets được mã hóa: Dịch vụ ẩn RẤT kín đáo

LeaseSets được mã hóa là các LeaseSets được công bố lên NetDB dưới dạng được mã hóa, trong đó không có bất kỳ Leases hay khóa công khai nào hiển thị trừ khi client có các khóa cần thiết để giải mã LeaseSet bên trong. Chỉ những client mà bạn chia sẻ khóa (đối với LeaseSets được mã hóa PSK), hoặc những client chia sẻ khóa của họ với bạn (đối với LeaseSets được mã hóa DH), mới có thể thấy destination (đích đến) và không ai khác.

I2P hỗ trợ một số chiến lược cho LeaseSets được mã hóa. Việc hiểu rõ các đặc tính then chốt của từng chiến lược là rất quan trọng khi quyết định sử dụng chiến lược nào. Nếu một LeaseSet được mã hóa sử dụng chiến lược "Khóa chia sẻ trước(PSK)", thì máy chủ sẽ tạo ra một khóa (hoặc nhiều khóa) mà người vận hành máy chủ sau đó chia sẻ với từng máy khách. Dĩ nhiên, việc trao đổi này phải diễn ra out-of-band (qua kênh ngoài), chẳng hạn thông qua một cuộc trao đổi trên IRC. Phiên bản LeaseSets được mã hóa này hơi giống như đăng nhập vào Wi‑Fi bằng mật khẩu. Chỉ khác là thứ bạn đăng nhập vào là một dịch vụ ẩn.

Nếu một LeaseSet được mã hóa sử dụng "chiến lược Diffie-Hellman (DH)", thì các khóa được tạo ở phía máy khách. Khi một máy khách Diffie-Hellman kết nối tới một Destination (đích) có LeaseSet được mã hóa, trước hết họ phải chia sẻ các khóa của mình với người vận hành máy chủ. Người vận hành máy chủ sau đó sẽ quyết định có cấp quyền cho máy khách DH hay không. Phiên bản các LeaseSet được mã hóa này khá giống SSH với tệp `authorized_keys`. Ngoại trừ việc bạn đang đăng nhập vào một dịch vụ ẩn (Hidden Service).

Bằng cách mã hóa LeaseSet của bạn, bạn không chỉ khiến người dùng không được ủy quyền không thể kết nối tới destination (địa chỉ đích trong I2P) của bạn, mà còn khiến khách truy cập không được ủy quyền thậm chí không thể phát hiện ra destination thực sự của Dịch vụ ẩn I2P. Một số độc giả có lẽ đã nghĩ đến một trường hợp sử dụng cho LeaseSet được mã hóa của riêng họ.

## Sử dụng các leaseSet được mã hóa để truy cập an toàn vào bảng điều khiển router

Theo nguyên tắc chung, càng có nhiều thông tin phức tạp về thiết bị của bạn mà một dịch vụ có thể truy cập, thì càng nguy hiểm khi công khai dịch vụ đó lên Internet, hay thậm chí lên một mạng Dịch vụ ẩn như I2P. Nếu bạn muốn công khai một dịch vụ như vậy, bạn cần bảo vệ nó bằng thứ gì đó như một mật khẩu, hoặc, trong trường hợp của I2P, một lựa chọn toàn diện và an toàn hơn nhiều có thể là một LeaseSet được mã hóa.

**Trước khi tiếp tục, vui lòng đọc và hiểu rằng nếu bạn thực hiện quy trình sau mà không có Encrypted LeaseSet, bạn sẽ vô hiệu hóa tính bảo mật của router I2P của bạn. Không cấu hình quyền truy cập vào bảng điều khiển của router qua I2P nếu không có Encrypted LeaseSet. Ngoài ra, không chia sẻ các PSK (khóa chia sẻ trước) của Encrypted LeaseSet của bạn với bất kỳ thiết bị nào không thuộc quyền kiểm soát của bạn.**

Một dịch vụ như vậy, rất hữu ích để chia sẻ qua I2P nhưng CHỈ với một Encrypted LeaseSet (LeaseSet được mã hóa), là bảng điều khiển router I2P.

Công khai bảng điều khiển router I2P trên một máy lên I2P bằng một Encrypted LeaseSet cho phép một máy khác có trình duyệt quản trị thể hiện I2P từ xa. Tôi thấy điều này hữu ích để giám sát từ xa các dịch vụ I2P thường dùng của tôi. Nó cũng có thể được dùng để theo dõi một máy chủ dùng để duy trì seed một torrent lâu dài, như một cách để truy cập I2PSnark.

Mặc dù việc giải thích có thể tốn thời gian, việc thiết lập LeaseSet mã hóa khá đơn giản thông qua Hidden Services Manager UI.

## Trên "Server"

Bắt đầu bằng cách mở Hidden Services Manager tại http://127.0.0.1:7657/i2ptunnelmgr và cuộn xuống cuối phần có dòng "I2P Hidden Services." Tạo một dịch vụ ẩn mới với host "127.0.0.1" và port "7657" với các "Tunnel Cryptography Options" này và lưu dịch vụ ẩn.

Sau đó, chọn tunnel mới của bạn từ trang chính Hidden Services Manager. Phần Tùy chọn mật mã của tunnel giờ đây sẽ bao gồm Khóa được chia sẻ trước đầu tiên của bạn. Hãy ghi lại điều này cho bước tiếp theo, cùng với Encrypted Base32 Address (Địa chỉ Base32 được mã hóa) của tunnel.

## Trên "Client"

Bây giờ hãy chuyển sang máy khách sẽ kết nối tới dịch vụ ẩn và truy cập trang Cấu hình Keyring tại http://127.0.0.1:7657/configkeyring để thêm các khóa từ trước đó. Bắt đầu bằng cách dán Base32 từ máy chủ vào trường có nhãn: "Full destination, name, Base32, or hash." Tiếp theo, dán Khóa chia sẻ trước (Pre-Shared Key) từ máy chủ vào trường "Encryption Key". Nhấn Lưu, và bạn đã sẵn sàng truy cập an toàn vào dịch vụ ẩn bằng Encrypted LeaseSet.

## Bây giờ bạn đã sẵn sàng để quản trị I2P từ xa

Như bạn thấy, I2P cung cấp những khả năng độc đáo cho các quản trị viên dịch vụ ẩn, giúp họ có thể quản lý an toàn các kết nối I2P của mình từ bất cứ đâu trên thế giới. Các Encrypted LeaseSets khác mà tôi giữ trên cùng thiết bị vì cùng lý do đó trỏ tới máy chủ SSH, phiên bản Portainer tôi dùng để quản lý các container dịch vụ của mình, và phiên bản NextCloud cá nhân của tôi. Với I2P, việc tự lưu trữ thực sự riêng tư và luôn có thể truy cập là một mục tiêu khả thi; thực tế tôi cho rằng đó là một trong những điều mà chúng tôi đặc biệt phù hợp, nhờ Encrypted LeaseSets. Với chúng, I2P có thể trở thành chìa khóa để bảo vệ các hệ thống tự động hóa gia đình tự lưu trữ, hoặc đơn giản trở thành xương sống của một web ngang hàng mới riêng tư hơn.
