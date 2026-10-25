---
title: "Cơ sở dữ liệu mạng"
description: "Hiểu về cơ sở dữ liệu mạng phân tán (netDb) của I2P - một DHT chuyên biệt cho thông tin liên lạc router và tra cứu đích đến"
slug: "network-database"
aliases:
  - "/vi/how_networkdatabase"
  - "/vi/how_networkdatabase/"
lastUpdated: "2025-03"
accurateFor: "0.9.65"
---

## Tổng quan

netDb của I2P là một cơ sở dữ liệu phân tán chuyên biệt, chỉ chứa hai loại dữ liệu - thông tin liên lạc của router (**RouterInfos**) và thông tin liên lạc của đích đến (**LeaseSets**). Mỗi phần dữ liệu được ký bởi bên có thẩm quyền và xác minh bởi bất kỳ ai sử dụng hoặc lưu trữ nó. Ngoài ra, dữ liệu có thông tin tính sống động bên trong, cho phép loại bỏ các mục không liên quan, các mục mới hơn thay thế các mục cũ hơn, và bảo vệ chống lại một số loại tấn công nhất định.

netDb được phân phối bằng một kỹ thuật đơn giản gọi là "floodfill", trong đó một tập con của tất cả các router, được gọi là "floodfill router", duy trì cơ sở dữ liệu phân tán này.

---

## RouterInfo

Khi một I2P router muốn liên lạc với router khác, chúng cần biết một số thông tin dữ liệu quan trọng - tất cả đều được gói lại và ký bởi router thành một cấu trúc gọi là "RouterInfo", được phân phối với SHA256 của danh tính router làm khóa. Cấu trúc này chứa:

- Danh tính của router (một khóa mã hóa, một khóa ký và một chứng chỉ)
- Các địa chỉ liên lạc có thể tiếp cận được
- Thời điểm thông tin này được công bố
- Một tập hợp các tùy chọn văn bản tùy ý
- Chữ ký của những thông tin trên, được tạo bởi khóa ký của danh tính

### Các Tùy Chọn Mong Đợi

Các tùy chọn văn bản sau đây, mặc dù không bắt buộc nghiêm ngặt, nhưng dự kiến sẽ có mặt:

- **caps** (Cờ khả năng - được sử dụng để chỉ ra sự tham gia floodfill, băng thông xấp xỉ và khả năng tiếp cận được cảm nhận)
  - **D**: Tắc nghẽn trung bình (kể từ phiên bản 0.9.58)
  - **E**: Tắc nghẽn cao (kể từ phiên bản 0.9.58)
  - **f**: Floodfill
  - **G**: Từ chối tất cả tunnel (kể từ phiên bản 0.9.58)
  - **H**: Ẩn
  - **K**: Băng thông chia sẻ dưới 12 KBps
  - **L**: Băng thông chia sẻ 12 - 48 KBps (mặc định)
  - **M**: Băng thông chia sẻ 48 - 64 KBps
  - **N**: Băng thông chia sẻ 64 - 128 KBps
  - **O**: Băng thông chia sẻ 128 - 256 KBps
  - **P**: Băng thông chia sẻ 256 - 2000 KBps (kể từ phiên bản 0.9.20, xem ghi chú bên dưới)
  - **R**: Có thể tiếp cận
  - **U**: Không thể tiếp cận
  - **X**: Băng thông chia sẻ trên 2000 KBps (kể từ phiên bản 0.9.20, xem ghi chú bên dưới)

"Băng thông chia sẻ" == (tỷ lệ chia sẻ %) * min(băng thông vào, băng thông ra)

Để tương thích với các router cũ hơn, một router có thể công bố nhiều ký tự băng thông, ví dụ "PO".

Lưu ý: ranh giới giữa các lớp băng thông P và X có thể là 2000 hoặc 2048 KBps, tùy thuộc vào lựa chọn của người triển khai.

- **netId** = 2 (Tương thích mạng cơ bản - Router sẽ từ chối giao tiếp với peer có netId khác)
- **router.version** (Được sử dụng để xác định tương thích với các tính năng và thông điệp mới hơn)

Ghi chú về khả năng R/U: Một router thường nên công bố khả năng R hoặc U, trừ khi trạng thái kết nối hiện tại chưa được xác định. R có nghĩa là router có thể truy cập trực tiếp (không cần introducers, không bị tường lửa chặn) trên ít nhất một địa chỉ truyền tải. U có nghĩa là router KHÔNG thể truy cập trực tiếp trên BẤT KỲ địa chỉ truyền tải nào.

Tùy chọn không còn được hỗ trợ: - ~~coreVersion~~ (Không bao giờ được sử dụng, đã loại bỏ trong phiên bản 0.9.24) - ~~stat_uptime~~ = 90m (Không được sử dụng kể từ phiên bản 0.7.9, đã loại bỏ trong phiên bản 0.9.24)

Các giá trị này được sử dụng bởi các router khác để đưa ra quyết định cơ bản. Chúng ta có nên kết nối với router này không? Chúng ta có nên thử định tuyến một tunnel qua router này không? Cờ khả năng băng thông, đặc biệt, chỉ được sử dụng để xác định liệu router có đáp ứng ngưỡng tối thiểu để định tuyến tunnel hay không. Trên ngưỡng tối thiểu, băng thông được quảng cáo không được sử dụng hoặc tin tưởng ở bất kỳ đâu trong router, ngoại trừ việc hiển thị trong giao diện người dùng và để gỡ lỗi cũng như phân tích mạng.

Số NetID hợp lệ:

| Sử dụng | Số NetID |
|---------|----------|
| Dành riêng | 0 |
| Dành riêng | 1 |
| Mạng Hiện tại (mặc định) | 2 |
| Mạng Tương lai Dành riêng | 3 - 15 |
| Forks và Mạng Thử nghiệm | 16 - 254 |
| Dành riêng | 255 |
### Tùy chọn bổ sung

Các tùy chọn văn bản bổ sung bao gồm một số lượng nhỏ thống kê về tình trạng router, được tổng hợp bởi các trang web như [stats.i2p](http://stats.i2p/) để phân tích hiệu suất mạng và gỡ lỗi. Những thống kê này được lựa chọn để cung cấp dữ liệu quan trọng cho các nhà phát triển, chẳng hạn như tỷ lệ thành công xây dựng tunnel, đồng thời cân bằng nhu cầu về dữ liệu này với các tác động phụ có thể xảy ra từ việc tiết lộ dữ liệu. Thống kê hiện tại được giới hạn trong:

- Tỷ lệ xây dựng tunnel thám sát thành công, bị từ chối và hết thời gian
- Số lượng tunnel tham gia trung bình trong 1 giờ

Các thống kê này là tùy chọn, nhưng nếu được bao gồm, sẽ giúp phân tích hiệu suất toàn mạng. Kể từ API 0.9.58, các thống kê này đã được đơn giản hóa và chuẩn hóa như sau:

- Các khóa tùy chọn là stat_(tên_thống_kê).(chu_kỳ_thống_kê)
- Các giá trị tùy chọn được phân tách bằng ';'
- Thống kê cho số lượng sự kiện hoặc tỷ lệ phần trăm chuẩn hóa sử dụng giá trị thứ 4; ba giá trị đầu tiên không được sử dụng nhưng phải có mặt
- Thống kê cho các giá trị trung bình sử dụng giá trị thứ 1, và không cần dấu phân tách ';'
- Để có trọng số bằng nhau cho tất cả các router trong phân tích thống kê, và để tăng thêm tính ẩn danh, các router chỉ nên bao gồm các thống kê này sau khi hoạt động ít nhất một giờ, và chỉ một lần trong mỗi 16 lần RI được xuất bản.

Ví dụ:

```
stat_tunnel.buildExploratoryExpire.60m = 0;0;0;53.14
stat_tunnel.buildExploratoryReject.60m = 0;0;0;15.51
stat_tunnel.buildExploratorySuccess.60m = 0;0;0;31.35
stat_tunnel.participatingTunnels.60m = 289.20
```
Các floodfill router có thể công bố dữ liệu bổ sung về số lượng mục trong cơ sở dữ liệu mạng của chúng. Những thông tin này là tùy chọn, nhưng nếu được bao gồm, sẽ giúp phân tích hiệu suất toàn mạng.

Hai tùy chọn sau đây nên được các floodfill router bao gồm trong mọi RI được xuất bản:

- **netdb.knownLeaseSets**
- **netdb.knownRouters**

Ví dụ:

```
netdb.knownLeaseSets = 158
netdb.knownRouters = 11374
```
Dữ liệu được công bố có thể nhìn thấy trong giao diện người dùng của router, nhưng không được sử dụng hoặc tin cậy bởi bất kỳ router nào khác.

### Tùy chọn Family

Kể từ phiên bản 0.9.24, các router có thể khai báo rằng chúng thuộc về một "family" (họ), được vận hành bởi cùng một thực thể. Nhiều router trong cùng một family sẽ không được sử dụng trong một tunnel duy nhất.

Các tùy chọn family là:

- **family** (Tên family)
- **family.key** Mã loại chữ ký của [Signing Public Key](/docs/specs/common-structures/#type_SigningPublicKey) của family (dưới dạng chữ số ASCII) được nối với ':' và nối với Signing Public Key ở định dạng base 64
- **family.sig** Chữ ký của ((tên family dưới UTF-8) được nối với (router hash 32 byte)) ở định dạng base 64

### Hết hạn RouterInfo

RouterInfos không có thời gian hết hạn cố định. Mỗi router có thể tự do duy trì chính sách cục bộ của riêng mình để cân bằng giữa tần suất tra cứu RouterInfo với việc sử dụng bộ nhớ hoặc đĩa. Trong phiên bản hiện tại, có các chính sách chung sau đây:

- Không có hết hạn trong giờ đầu tiên hoạt động, vì dữ liệu được lưu trữ liên tục có thể đã cũ.
- Không có hết hạn nếu có 25 RouterInfos trở xuống.
- Khi số lượng RouterInfos cục bộ tăng lên, thời gian hết hạn giảm xuống, nhằm cố gắng duy trì số lượng RouterInfos hợp lý. Thời gian hết hạn với ít hơn 120 routers là 72 giờ, trong khi thời gian hết hạn với 300 routers là khoảng 30 giờ.
- RouterInfos chứa các introducer [SSU](/docs/legacy/ssu/) hết hạn sau khoảng một giờ, vì danh sách introducer hết hạn trong khoảng thời gian đó.
- Floodfills sử dụng thời gian hết hạn ngắn (1 giờ) cho tất cả RouterInfos cục bộ, vì RouterInfos hợp lệ sẽ được republish thường xuyên đến chúng.

### Lưu trữ Bền vững RouterInfo

RouterInfos được ghi xuống đĩa định kỳ để chúng có sẵn sau khi khởi động lại.

Có thể mong muốn lưu trữ lâu dài các Meta LeaseSet có thời hạn hết hạn dài. Điều này phụ thuộc vào cách triển khai.

### Xem Thêm

- [Đặc tả RouterInfo](/docs/specs/common-structures/#struct_RouterInfo)
- [RouterInfo Javadoc](http://idk.i2p/javadoc-i2p/net/i2p/data/router/RouterInfo.html)

---

## LeaseSet

Phần dữ liệu thứ hai được phân phối trong netDb là "LeaseSet" - tài liệu ghi lại một nhóm **các điểm vào tunnel (lease)** cho một đích client cụ thể. Mỗi lease này chỉ định các thông tin sau:

- Router cổng tunnel (bằng cách chỉ định danh tính của nó)
- ID tunnel trên router đó để gửi tin nhắn (một số 4 byte)
- Khi tunnel đó sẽ hết hạn.

Bản thân LeaseSet được lưu trữ trong netDb dưới khóa được tạo từ SHA256 của destination. Một ngoại lệ là đối với Encrypted LeaseSets (LS2), kể từ phiên bản 0.9.38. SHA256 của type byte (3) theo sau bởi blinded public key được sử dụng cho khóa DHT, và sau đó được xoay như thường lệ. Xem phần Kademlia Closeness Metric bên dưới.

Ngoài các lease này, LeaseSet còn bao gồm:

- Destination chính nó (một khóa mã hóa, một khóa ký và một chứng chỉ)
- Khóa công khai mã hóa bổ sung: được sử dụng để mã hóa đầu cuối đến đầu cuối của các thông điệp garlic
- Khóa công khai ký bổ sung: dành cho việc thu hồi LeaseSet, nhưng hiện tại chưa được sử dụng.
- Chữ ký của tất cả dữ liệu LeaseSet, để đảm bảo rằng Destination đã xuất bản LeaseSet.

- [Thông số kỹ thuật Lease](/docs/specs/common-structures/#struct_Lease)
- [Thông số kỹ thuật LeaseSet](/docs/specs/common-structures/#struct_LeaseSet)
- [Javadoc của Lease](http://idk.i2p/javadoc-i2p/net/i2p/data/Lease.html)
- [Javadoc của LeaseSet](http://idk.i2p/javadoc-i2p/net/i2p/data/LeaseSet.html)

Kể từ phiên bản 0.9.38, ba loại leaseSet mới được định nghĩa; LeaseSet2, MetaLeaseSet, và EncryptedLeaseSet. Xem bên dưới.

### Unpublished LeaseSets

Một LeaseSet cho một đích chỉ được sử dụng cho các kết nối đi ra là *không được công bố*. Nó không bao giờ được gửi để công bố tới một floodfill router. Các tunnel "Client", chẳng hạn như những tunnel dành cho duyệt web và IRC client, là không được công bố. Các server vẫn có thể gửi tin nhắn trở lại những đích không được công bố này, nhờ vào [tin nhắn lưu trữ I2NP](#leaseset-storage-to-peers).

### LeaseSet Đã Thu Hồi

Một LeaseSet có thể bị *thu hồi* bằng cách xuất bản một LeaseSet mới với không có lease nào. Việc thu hồi phải được ký bởi khóa ký bổ sung trong LeaseSet. Việc thu hồi chưa được triển khai đầy đủ và không rõ liệu chúng có ích lợi thực tế nào hay không. Đây là cách sử dụng duy nhất được lên kế hoạch cho khóa ký đó, vì vậy hiện tại nó chưa được sử dụng.

### LeaseSet2 (LS2)

Kể từ phiên bản 0.9.38, các floodfill hỗ trợ cấu trúc LeaseSet2 mới. Cấu trúc này rất giống với cấu trúc LeaseSet cũ và phục vụ cùng mục đích. Cấu trúc mới cung cấp tính linh hoạt cần thiết để hỗ trợ các loại mã hóa mới, nhiều loại mã hóa, các tùy chọn, khóa ký ngoại tuyến và các tính năng khác. Xem đề xuất 123 để biết chi tiết.

### Meta LeaseSet (LS2)

Kể từ phiên bản 0.9.38, các floodfill hỗ trợ cấu trúc Meta LeaseSet mới. Cấu trúc này cung cấp một cấu trúc dạng cây trong DHT, để tham chiếu đến các LeaseSet khác. Sử dụng Meta LeaseSet, một trang web có thể triển khai các dịch vụ multihomed lớn, trong đó nhiều Destination khác nhau được sử dụng để cung cấp một dịch vụ chung. Các mục trong Meta LeaseSet là các Destination hoặc Meta LeaseSet khác, và có thể có thời gian hết hạn dài, lên đến 18,2 giờ. Sử dụng tính năng này, có thể chạy hàng trăm hoặc hàng nghìn Destination lưu trữ một dịch vụ chung. Xem đề xuất 123 để biết chi tiết.

### Encrypted LeaseSets (LS1)

Phần này mô tả phương pháp cũ, không an toàn để mã hóa LeaseSets bằng khóa đối xứng cố định. Xem phần dưới để biết phiên bản LS2 của Encrypted LeaseSets.

Trong một LeaseSet *được mã hóa*, tất cả các Lease đều được mã hóa bằng một khóa riêng biệt. Các lease chỉ có thể được giải mã, và do đó destination chỉ có thể được liên lạc, bởi những ai có khóa. Không có cờ hiệu hoặc dấu hiệu trực tiếp nào khác cho thấy LeaseSet được mã hóa. LeaseSet mã hóa không được sử dụng rộng rãi, và đây là chủ đề cho công việc tương lai để nghiên cứu liệu giao diện người dùng và triển khai của LeaseSet mã hóa có thể được cải thiện hay không.

### Encrypted LeaseSets (LS2)

Từ phiên bản 0.9.38, các floodfill hỗ trợ cấu trúc EncryptedLeaseSet mới. Destination được ẩn, và chỉ có blinded public key và thời gian hết hạn hiển thị với floodfill. Chỉ những ai có Destination đầy đủ mới có thể giải mã cấu trúc này. Cấu trúc được lưu trữ tại vị trí DHT dựa trên hash của blinded public key, không phải hash của Destination. Xem đề xuất 123 để biết chi tiết.

### Hết hạn LeaseSet

Đối với các LeaseSet thông thường, thời gian hết hạn là thời điểm hết hạn muộn nhất của các lease trong đó. Đối với các cấu trúc dữ liệu LeaseSet2 mới, thời gian hết hạn được chỉ định trong header. Với LeaseSet2, thời gian hết hạn nên khớp với thời gian hết hạn muộn nhất của các lease trong đó. Đối với EncryptedLeaseSet và MetaLeaseSet, thời gian hết hạn có thể khác nhau, và thời gian hết hạn tối đa có thể được áp dụng, điều này sẽ được xác định sau.

### Lưu trữ bền vững LeaseSet

Không cần lưu trữ lâu dài dữ liệu LeaseSet vì chúng hết hạn rất nhanh. Tuy nhiên, việc lưu trữ lâu dài dữ liệu EncryptedLeaseSet và MetaLeaseSet với thời gian hết hạn dài có thể được khuyến khích.

### Lựa chọn Khóa Mã hóa (LS2)

LeaseSet2 có thể chứa nhiều khóa mã hóa. Các khóa được sắp xếp theo thứ tự ưu tiên của máy chủ, khóa được ưu tiên nhất đứng đầu. Hành vi mặc định của client là chọn khóa đầu tiên có loại mã hóa được hỗ trợ. Các client có thể sử dụng các thuật toán lựa chọn khác dựa trên hỗ trợ mã hóa, hiệu suất tương đối và các yếu tố khác.

---

## Khởi tạo

netDb được phân tán, tuy nhiên bạn cần ít nhất một tham chiếu đến một peer để quá trình tích hợp kết nối bạn vào mạng. Điều này được thực hiện bằng cách "reseeding" router của bạn với RouterInfo của một peer đang hoạt động - cụ thể, bằng cách truy xuất file `routerInfo-$hash.dat` của họ và lưu trữ nó trong thư mục `netDb/` của bạn. Bất kỳ ai cũng có thể cung cấp cho bạn những file đó - bạn thậm chí có thể cung cấp chúng cho người khác bằng cách chia sẻ thư mục netDb của chính mình. Để đơn giản hóa quá trình này, các tình nguyện viên xuất bản thư mục netDb của họ (hoặc một phần) trên mạng thông thường (không phải i2p), và các URL của những thư mục này được mã hóa cứng trong I2P. Khi router khởi động lần đầu tiên, nó sẽ tự động tải từ một trong những URL này, được chọn ngẫu nhiên.

---

## Floodfill

Floodfill netDb là một cơ chế lưu trữ phân tán đơn giản. Thuật toán lưu trữ rất đơn giản: gửi dữ liệu đến peer gần nhất đã quảng bá bản thân là một floodfill router. Khi peer trong floodfill netDb nhận được một netDb store từ một peer không thuộc floodfill netDb, họ sẽ gửi nó đến một tập con các peer trong floodfill netDb. Các peer được chọn là những peer gần nhất (theo [XOR-metric](#kademlia-closeness-metric)) với một khóa cụ thể.

Việc xác định router nào là một phần của floodfill netDb rất đơn giản - thông tin này được công khai trong routerInfo của mỗi router dưới dạng một khả năng.

Floodfills không có cơ quan trung ương và không tạo thành "sự đồng thuận" - chúng chỉ triển khai một lớp phủ DHT đơn giản.

### Tham gia làm Floodfill Router

Khác với Tor, nơi các directory server được mã hóa cứng và được tin tưởng, và được vận hành bởi các thực thể đã biết, các thành viên của tập hợp peer floodfill I2P không cần phải được tin tưởng, và thay đổi theo thời gian.

Để tăng độ tin cậy của netDb và giảm thiểu tác động của lưu lượng netDb lên router, floodfill chỉ được tự động kích hoạt trên các router được cấu hình với giới hạn băng thông cao. Các router có giới hạn băng thông cao (phải được cấu hình thủ công vì mặc định thấp hơn nhiều) được giả định là đang sử dụng kết nối có độ trễ thấp và có khả năng hoạt động 24/7 cao hơn. Băng thông chia sẻ tối thiểu hiện tại cho một floodfill router là 128 KBytes/giây.

Ngoài ra, một router phải vượt qua một số kiểm tra bổ sung về trạng thái hoạt động (thời gian hàng đợi tin nhắn đi, độ trễ công việc, v.v.) trước khi chức năng floodfill được tự động kích hoạt.

Với các quy tắc hiện tại cho việc tự động tham gia, khoảng 6% router trong mạng là các floodfill router.

Trong khi một số peer được cấu hình thủ công để làm floodfill, những peer khác đơn giản là các router băng thông cao tự động tình nguyện khi số lượng floodfill peer giảm xuống dưới ngưỡng. Điều này ngăn chặn bất kỳ thiệt hại mạng lâu dài nào do mất hầu hết hoặc tất cả floodfill trong một cuộc tấn công. Đổi lại, những peer này sẽ tự bỏ vai trò floodfill khi có quá nhiều floodfill đang hoạt động.

### Vai trò của Floodfill Router

Các dịch vụ duy nhất của floodfill router ngoài những dịch vụ của các router không phải floodfill là chấp nhận lưu trữ netDb và phản hồi các truy vấn netDb. Vì chúng thường có băng thông cao, chúng có nhiều khả năng tham gia vào số lượng lớn tunnel (tức là làm "relay" cho những người khác), nhưng điều này không liên quan trực tiếp đến các dịch vụ cơ sở dữ liệu phân tán của chúng.

---

## Thước đo gần gũi Kademlia

netDb sử dụng một thước đo XOR kiểu Kademlia đơn giản để xác định độ gần. Để tạo khóa Kademlia, hash SHA256 của RouterIdentity hoặc Destination được tính toán. Một ngoại lệ là đối với Encrypted LeaseSets (LS2), kể từ phiên bản 0.9.38. SHA256 của type byte (3) theo sau bởi blinded public key được sử dụng cho khóa DHT, và sau đó được xoay như thường lệ.

Một sự thay đổi đối với thuật toán này được thực hiện để tăng chi phí của [các cuộc tấn công Sybil](#sybil-attack-partial-keyspace). Thay vì hash SHA256 của khóa được tra cứu hoặc lưu trữ, hash SHA256 được tính từ khóa tìm kiếm nhị phân 32-byte được nối với ngày UTC được biểu diễn dưới dạng chuỗi ASCII 8-byte yyyyMMdd, tức là SHA256(key + yyyyMMdd). Điều này được gọi là "routing key", và nó thay đổi mỗi ngày vào lúc nửa đêm UTC. Chỉ khóa tìm kiếm được sửa đổi theo cách này, không phải hash của floodfill router. Sự biến đổi hàng ngày của DHT đôi khi được gọi là "keyspace rotation", mặc dù nó không thực sự là một phép xoay.

Routing keys không bao giờ được gửi trên đường truyền trong bất kỳ thông điệp I2NP nào, chúng chỉ được sử dụng cục bộ để xác định khoảng cách.

---

## Phân đoạn Cơ sở dữ liệu mạng - Cơ sở dữ liệu con

Theo truyền thống, các DHT kiểu Kademlia không quan tâm đến việc bảo toàn tính không thể liên kết của thông tin được lưu trữ trên bất kỳ node cụ thể nào trong DHT. Ví dụ, một phần thông tin có thể được lưu trữ vào một node trong DHT, sau đó được yêu cầu trả về từ node đó mà không có điều kiện. Trong I2P và khi sử dụng netDb, điều này không xảy ra, thông tin được lưu trữ trong DHT chỉ có thể được chia sẻ trong những trường hợp nhất định đã biết khi việc đó "an toàn". Điều này nhằm ngăn chặn một loại tấn công mà kẻ tấn công độc hại có thể cố gắng liên kết một client tunnel với một router bằng cách gửi một lệnh store đến client tunnel, sau đó yêu cầu lấy lại trực tiếp từ "Host" bị nghi ngờ của client tunnel.

### Cấu trúc Phân đoạn

Các router I2P có thể triển khai các biện pháp phòng thủ hiệu quả chống lại loại tấn công này nếu đáp ứng một vài điều kiện. Một triển khai netDb cần có khả năng theo dõi xem một mục cơ sở dữ liệu có được nhận qua client tunnel hay trực tiếp. Nếu nó được nhận qua client tunnel, thì cũng cần theo dõi xem nó được nhận qua client tunnel nào, sử dụng destination cục bộ của client. Nếu mục đó được nhận qua nhiều client tunnel, thì netDb cần theo dõi tất cả các destination nơi mục đó được quan sát. Nó cũng cần theo dõi xem một mục có được nhận dưới dạng phản hồi cho một truy vấn lookup hay dưới dạng store.

Trong cả hai triển khai Java và C++, điều này được thực hiện bằng cách sử dụng một netDb "Chính" duy nhất cho các tra cứu trực tiếp và các hoạt động floodfill trước tiên. NetDb chính này tồn tại trong ngữ cảnh router. Sau đó, mỗi client được cấp phiên bản riêng của netDb, được sử dụng để thu thập các mục cơ sở dữ liệu được gửi đến tunnel của client và phản hồi các tra cứu được gửi xuống tunnel của client. Chúng tôi gọi những cái này là "Cơ sở Dữ liệu Mạng Client" hoặc "Cơ sở Dữ liệu Phụ" và chúng tồn tại trong ngữ cảnh client. NetDb được vận hành bởi client chỉ tồn tại trong suốt thời gian sống của client và chỉ chứa các mục được giao tiếp với tunnel của client. Điều này khiến cho việc các mục được gửi xuống tunnel của client chồng chéo với các mục được gửi trực tiếp đến router trở thành không thể.

Ngoài ra, mỗi netDb cần có khả năng ghi nhớ xem một mục cơ sở dữ liệu được nhận vì nó được gửi đến một trong các đích của chúng ta, hay vì nó được chúng ta yêu cầu như một phần của quá trình tra cứu. Nếu một mục cơ sở dữ liệu được nhận dưới dạng lưu trữ, tức là có router khác gửi nó cho chúng ta, thì netDb nên phản hồi các yêu cầu cho mục đó khi router khác tra cứu key. Tuy nhiên, nếu nó được nhận như một phản hồi cho truy vấn, thì netDb chỉ nên phản hồi truy vấn cho mục đó nếu mục này đã được lưu trữ trước đó tại cùng đích. Một client không bao giờ nên trả lời các truy vấn với một mục từ netDb chính, mà chỉ từ cơ sở dữ liệu mạng client của chính nó.

Những chiến lược này nên được áp dụng kết hợp với nhau để cả hai đều được sử dụng. Khi kết hợp, chúng "Phân đoạn" netDb và bảo vệ nó khỏi các cuộc tấn công.

---

## Cơ chế Lưu trữ, Xác minh và Tra cứu

### Lưu trữ RouterInfo đến các Peer

Các [I2NP](/docs/specs/i2np/) DatabaseStoreMessages chứa RouterInfo cục bộ được trao đổi với các peer như một phần của quá trình khởi tạo kết nối transport [NTCP](/docs/specs/ntcp2/) hoặc [SSU](/docs/specs/ssu2/).

### Lưu trữ LeaseSet đến các Peer

Các [I2NP](/docs/specs/i2np/) DatabaseStoreMessages chứa LeaseSet cục bộ được trao đổi định kỳ với các peer bằng cách gói chúng trong một garlic message cùng với lưu lượng bình thường từ Destination liên quan. Điều này cho phép gửi phản hồi ban đầu và các phản hồi sau đó đến một Lease thích hợp, mà không cần bất kỳ tra cứu LeaseSet nào, hoặc không yêu cầu các Destination giao tiếp phải công bố LeaseSet.

### Lựa chọn Floodfill

DatabaseStoreMessage nên được gửi đến floodfill gần nhất với routing key hiện tại cho RouterInfo hoặc LeaseSet đang được lưu trữ. Hiện tại, floodfill gần nhất được tìm thấy bằng cách tìm kiếm trong cơ sở dữ liệu cục bộ. Ngay cả khi floodfill đó không thực sự là gần nhất, nó sẽ lan truyền thông tin "gần hơn" bằng cách gửi đến nhiều floodfill khác. Điều này cung cấp mức độ chịu lỗi cao.

Trong Kademlia truyền thống, một peer sẽ thực hiện tìm kiếm "find-closest" trước khi chèn một mục vào DHT đến mục tiêu gần nhất. Vì thao tác xác minh sẽ có xu hướng khám phá các floodfill gần hơn nếu chúng có mặt, một router sẽ nhanh chóng cải thiện kiến thức của mình về "khu vực lân cận" DHT cho RouterInfo và LeaseSets mà nó thường xuyên xuất bản. Mặc dù I2NP không định nghĩa thông báo "find-closest", nếu cần thiết, một router có thể đơn giản thực hiện tìm kiếm lặp cho một khóa với bit ít quan trọng nhất được đảo (tức là key ^ 0x01) cho đến khi không có peer nào gần hơn được nhận trong DatabaseSearchReplyMessages. Điều này đảm bảo rằng peer gần nhất thực sự sẽ được tìm thấy ngay cả khi một peer xa hơn có mục netDb.

### Lưu trữ RouterInfo đến các Floodfill

Một router công bố RouterInfo của chính nó bằng cách kết nối trực tiếp với một floodfill router và gửi cho nó một [I2NP](/docs/specs/i2np/) DatabaseStoreMessage với Reply Token khác không. Thông điệp này không được mã hóa garlic encryption đầu cuối đến đầu cuối, vì đây là một kết nối trực tiếp, do đó không có router trung gian nào (và cũng không cần thiết phải ẩn dữ liệu này). Floodfill router sẽ trả lời bằng một [I2NP](/docs/specs/i2np/) DeliveryStatusMessage, với Message ID được đặt thành giá trị của Reply Token.

Trong một số trường hợp, router cũng có thể gửi RouterInfo DatabaseStoreMessage qua exploratory tunnel; ví dụ, do giới hạn kết nối, không tương thích kết nối, hoặc muốn ẩn IP thực từ floodfill. Floodfill có thể không chấp nhận việc lưu trữ như vậy trong thời gian quá tải hoặc dựa trên các tiêu chí khác; việc có nên tuyên bố rõ ràng việc lưu trữ RouterInfo không trực tiếp là bất hợp pháp hay không là một chủ đề cần nghiên cứu thêm.

### Lưu trữ LeaseSet tới các Floodfill

Việc lưu trữ LeaseSet nhạy cảm hơn nhiều so với RouterInfo, vì router phải đảm bảo rằng LeaseSet không thể được liên kết với router đó.

Một router xuất bản LeaseSet cục bộ bằng cách gửi một [I2NP](/docs/specs/i2np/) DatabaseStoreMessage với Reply Token khác không qua một tunnel gửi đi của client cho Destination đó. Thông điệp được mã hóa garlic encryption đầu cuối tới đầu cuối sử dụng Session Key Manager của Destination, để ẩn thông điệp khỏi điểm cuối gửi đi của tunnel. Router floodfill trả lời bằng một [I2NP](/docs/specs/i2np/) DeliveryStatusMessage, với Message ID được đặt thành giá trị của Reply Token. Thông điệp này được gửi trở lại một trong các tunnel nhận vào của client.

### Flooding

Giống như bất kỳ router nào, một floodfill sử dụng nhiều tiêu chí khác nhau để xác thực LeaseSet hoặc RouterInfo trước khi lưu trữ cục bộ. Những tiêu chí này có thể thích ứng và phụ thuộc vào các điều kiện hiện tại bao gồm tải hiện tại, kích thước netDb và các yếu tố khác. Tất cả việc xác thực phải được thực hiện trước khi flooding.

Sau khi một floodfill router nhận được một DatabaseStoreMessage chứa RouterInfo hoặc LeaseSet hợp lệ mà mới hơn so với dữ liệu đã lưu trữ trước đó trong NetDb cục bộ của nó, nó sẽ "flood" (lan truyền) dữ liệu đó. Để flood một mục NetDb, nó sẽ tra cứu một số (hiện tại là 3) floodfill router gần nhất với routing key của mục NetDb. (Routing key là SHA256 Hash của RouterIdentity hoặc Destination với ngày tháng (yyyyMMdd) được nối thêm vào.) Bằng cách flooding đến những router gần nhất với key chứ không phải gần nhất với chính nó, floodfill đảm bảo rằng việc lưu trữ được đến đúng vị trí, ngay cả khi router thực hiện lưu trữ không có kiến thức tốt về "vùng lân cận" DHT cho routing key đó.

Floodfill sau đó kết nối trực tiếp với từng peer đó và gửi cho chúng một [I2NP](/docs/specs/i2np/) DatabaseStoreMessage với Reply Token bằng không. Thông điệp không được mã hóa garlic encryption đầu cuối đến đầu cuối, vì đây là kết nối trực tiếp, nên không có router trung gian nào (và cũng không cần thiết phải ẩn dữ liệu này). Các router khác không trả lời hoặc re-flood lại, vì Reply Token bằng không.

Floodfill không được flood qua tunnel; DatabaseStoreMessage phải được gửi qua kết nối trực tiếp.

Các floodfill không bao giờ được flood một LeaseSet đã hết hạn hoặc một RouterInfo được xuất bản cách đây hơn một giờ.

### Tìm kiếm RouterInfo và LeaseSet

[I2NP](/docs/specs/i2np/) DatabaseLookupMessage được sử dụng để yêu cầu một mục netDb từ floodfill router. Các truy vấn được gửi qua một trong những tunnel thám hiểm đi ra của router. Các phản hồi được chỉ định trả về qua một trong những tunnel thám hiểm đi vào của router.

Các truy vấn thường được gửi song song đến hai floodfill router "tốt" (kết nối không bị lỗi) gần nhất với khóa được yêu cầu.

Nếu khóa được tìm thấy cục bộ bởi floodfill router, nó sẽ phản hồi bằng một [I2NP](/docs/specs/i2np/) DatabaseStoreMessage. Nếu khóa không được tìm thấy cục bộ bởi floodfill router, nó sẽ phản hồi bằng một [I2NP](/docs/specs/i2np/) DatabaseSearchReplyMessage chứa danh sách các floodfill router khác gần với khóa đó.

Việc tra cứu leaseSet được mã hóa garlic encryption từ đầu đến cuối kể từ phiên bản 0.9.5. Việc tra cứu RouterInfo không được mã hóa và do đó dễ bị nghe lén bởi điểm cuối đi ra (OBEP) của tunnel khách hàng. Điều này là do chi phí của việc mã hóa ElGamal. Việc mã hóa tra cứu RouterInfo có thể được kích hoạt trong các phiên bản tương lai.

Kể từ phiên bản 0.9.7, các phản hồi cho việc tra cứu LeaseSet (một DatabaseStoreMessage hoặc DatabaseSearchReplyMessage) sẽ được mã hóa bằng cách bao gồm session key và tag trong việc tra cứu. Điều này ẩn phản hồi khỏi inbound gateway (IBGW) của reply tunnel. Các phản hồi cho việc tra cứu RouterInfo sẽ được mã hóa nếu chúng ta kích hoạt mã hóa tra cứu.

(Tham khảo: [Hashing it out in Public](http://www-users.cs.umn.edu/~hopper/hashing_it_out.pdf) Phần 2.2-2.3 cho các thuật ngữ in nghiêng bên dưới)

Do kích thước tương đối nhỏ của mạng lưới và tính dự phòng flooding, các truy vấn thường có độ phức tạp O(1) thay vì O(log n). Một router có khả năng cao biết được một floodfill router đủ gần với khóa để có được câu trả lời ngay lần thử đầu tiên. Trong các phiên bản trước 0.8.9, các router sử dụng tính dự phòng tra cứu là hai (tức là, hai truy vấn được thực hiện song song với các peer khác nhau), và không có *recursive* cũng như *iterative* routing cho các truy vấn được triển khai. Các truy vấn được gửi qua *nhiều tuyến đường cùng lúc* để *giảm khả năng truy vấn thất bại*.

Kể từ phiên bản 0.8.9, *iterative lookups* (tra cứu lặp) được triển khai mà không có redundancy tra cứu. Đây là một phương thức tra cứu hiệu quả và đáng tin cậy hơn, hoạt động tốt hơn nhiều khi không phải tất cả floodfill peers đều được biết, và nó loại bỏ một hạn chế nghiêm trọng đối với sự phát triển của mạng. Khi mạng phát triển và mỗi router chỉ biết một tập con nhỏ của floodfill peers, việc tra cứu sẽ trở thành O(log n). Ngay cả khi peer không trả về các tham chiếu gần với key hơn, việc tra cứu vẫn tiếp tục với peer gần nhất tiếp theo, để tăng thêm độ mạnh mẽ và ngăn chặn một floodfill độc hại tạo ra lỗ đen trong một phần của không gian key. Việc tra cứu tiếp tục cho đến khi đạt được tổng thời gian chờ tra cứu, hoặc số lượng peers tối đa được truy vấn.

*ID nút* có thể *xác minh được* do chúng ta sử dụng trực tiếp router hash vừa làm ID nút vừa làm khóa Kademlia. Các phản hồi không chính xác mà không gần hơn với khóa tìm kiếm thường bị bỏ qua. Với kích thước hiện tại của mạng, một router có *kiến thức chi tiết về vùng lân cận của không gian ID đích*.

### Xác minh Lưu trữ RouterInfo

Lưu ý: Xác minh RouterInfo đã bị vô hiệu hóa kể từ phiên bản 0.9.7.1 để ngăn chặn cuộc tấn công được mô tả trong bài báo [Practical Attacks Against the I2P Network](http://wwwcip.informatik.uni-erlangen.de/~spjsschl/i2p.pdf). Chưa rõ liệu việc xác minh có thể được thiết kế lại để thực hiện một cách an toàn hay không.

Để xác minh việc lưu trữ đã thành công, một router chỉ cần đợi khoảng 10 giây, sau đó gửi một yêu cầu tra cứu đến một floodfill router khác gần với khóa (nhưng không phải router mà lệnh store đã được gửi tới). Các yêu cầu tra cứu được gửi qua một trong các outbound exploratory tunnel của router. Các yêu cầu tra cứu được mã hóa garlic encryption từ đầu đến cuối để ngăn việc nghe lén bởi outbound endpoint (OBEP).

### Xác minh lưu trữ LeaseSet

Để xác minh việc lưu trữ đã thành công, một router chỉ cần chờ khoảng 10 giây, sau đó gửi một lookup đến một floodfill router khác gần với khóa đó (nhưng không phải router mà store đã được gửi tới). Các lookup được gửi ra một trong những outbound client tunnel cho đích đến của LeaseSet đang được xác minh. Để ngăn chặn việc do thám bởi OBEP của outbound tunnel, các lookup được mã hóa garlic từ đầu đến cuối. Các phản hồi được chỉ định trả về qua một trong những inbound tunnel của client.

Kể từ phiên bản 0.9.7, các phản hồi cho cả tra cứu RouterInfo và LeaseSet (một DatabaseStoreMessage hoặc DatabaseSearchReplyMessage) sẽ được mã hóa, để ẩn phản hồi khỏi cổng vào (IBGW) của tunnel phản hồi.

### Khám phá

*Exploration* là một dạng đặc biệt của tra cứu netDb, trong đó một router cố gắng tìm hiểu về các router mới. Nó thực hiện điều này bằng cách gửi cho một floodfill router một [I2NP](/docs/specs/i2np/) DatabaseLookup Message, tìm kiếm một khóa ngẫu nhiên. Vì việc tra cứu này sẽ thất bại, floodfill thông thường sẽ phản hồi bằng một [I2NP](/docs/specs/i2np/) DatabaseSearchReplyMessage chứa các hash của các floodfill router gần với khóa đó. Điều này sẽ không hữu ích, vì router yêu cầu có thể đã biết các floodfill đó rồi, và sẽ không thực tế khi thêm tất cả floodfill router vào trường "don't include" của DatabaseLookup Message. Đối với một truy vấn exploration, router yêu cầu sẽ đặt một cờ đặc biệt trong DatabaseLookup Message. Khi đó floodfill sẽ chỉ phản hồi với các router không phải floodfill gần với khóa được yêu cầu.

### Ghi chú về Phản hồi Tra cứu

Phản hồi cho một yêu cầu tra cứu có thể là Database Store Message (khi thành công) hoặc Database Search Reply Message (khi thất bại). DSRM chứa trường 'from' router hash để chỉ ra nguồn gốc của phản hồi; DSM thì không có. Trường 'from' của DSRM không được xác thực và có thể bị giả mạo hoặc không hợp lệ. Không có thẻ phản hồi nào khác. Do đó, khi thực hiện nhiều yêu cầu song song, việc giám sát hiệu suất của các floodfill router khác nhau trở nên khó khăn.

---

## MultiHoming

Các điểm đích có thể được lưu trữ trên nhiều router đồng thời, bằng cách sử dụng cùng các khóa riêng tư và công khai (thường được lưu trong các file eepPriv.dat). Vì cả hai instance sẽ định kỳ xuất bản LeaseSet đã ký của chúng tới các floodfill peer, LeaseSet được xuất bản gần đây nhất sẽ được trả về cho peer yêu cầu tra cứu cơ sở dữ liệu. Vì LeaseSet có thời gian sống tối đa là 10 phút, nếu một instance cụ thể gặp sự cố, thời gian ngừng hoạt động sẽ là tối đa 10 phút, và thường ít hơn thế nhiều. Chức năng multihoming đã được xác minh và đang được sử dụng bởi một số dịch vụ trên mạng.

Kể từ phiên bản 0.9.38, các floodfill hỗ trợ cấu trúc Meta LeaseSet mới. Cấu trúc này cung cấp một cấu trúc giống như cây trong DHT, để tham chiếu đến các LeaseSet khác. Sử dụng Meta LeaseSet, một trang web có thể triển khai các dịch vụ multihomed lớn, nơi nhiều Destination khác nhau được sử dụng để cung cấp một dịch vụ chung. Các mục trong Meta LeaseSet là các Destination hoặc Meta LeaseSet khác, và có thể có thời hạn dài, lên đến 18.2 giờ. Sử dụng tính năng này, có thể chạy hàng trăm hoặc hàng nghìn Destination lưu trữ một dịch vụ chung. Xem đề xuất 123 để biết chi tiết.

---

## Phân Tích Mối Đe Dọa

Cũng được thảo luận trên [trang mô hình đe dọa](/docs/overview/threat-model/#floodfill).

Một người dùng thù địch có thể cố gắng gây hại cho mạng lưới bằng cách tạo ra một hoặc nhiều floodfill router và thiết kế chúng để đưa ra các phản hồi tệ, chậm hoặc không phản hồi. Một số kịch bản được thảo luận dưới đây.

### Giảm thiểu Chung qua Tăng trưởng

Hiện tại có khoảng 1700 floodfill router trong mạng lưới. Hầu hết các cuộc tấn công sau đây sẽ trở nên khó khăn hơn, hoặc có ít tác động hơn, khi quy mô mạng và số lượng floodfill router tăng lên.

### Giảm thiểu chung thông qua dự phòng

Thông qua flooding, tất cả các mục netdb được lưu trữ trên 3 floodfill router gần nhất với khóa.

### Giả mạo

Tất cả các mục netdb đều được ký bởi người tạo ra chúng, vì vậy không có router nào có thể giả mạo RouterInfo hoặc LeaseSet.

### Chậm hoặc Không Phản Hồi

Mỗi router duy trì một bộ thống kê mở rộng trong [hồ sơ peer](/docs/overview/peer-selection/) cho từng floodfill router, bao gồm các chỉ số chất lượng khác nhau cho peer đó. Bộ này bao gồm:

- Thời gian phản hồi trung bình
- Phần trăm truy vấn được trả lời với dữ liệu được yêu cầu
- Phần trăm lưu trữ được xác minh thành công
- Lần lưu trữ thành công cuối cùng
- Lần tra cứu thành công cuối cùng
- Phản hồi cuối cùng

Mỗi khi một router cần đưa ra quyết định về floodfill router nào gần nhất với một khóa, nó sử dụng các thước đo này để xác định floodfill router nào là "tốt". Các phương pháp và ngưỡng được sử dụng để xác định "độ tốt" tương đối mới và có thể được phân tích và cải thiện thêm. Trong khi một router hoàn toàn không phản hồi sẽ nhanh chóng được xác định và tránh, các router chỉ đôi khi có hành vi độc hại có thể khó xử lý hơn nhiều.

### Tấn công Sybil (Toàn bộ không gian khóa)

Kẻ tấn công có thể thực hiện một [cuộc tấn công Sybil](https://www.freehaven.net/anonbib/cache/sybil.pdf) bằng cách tạo ra một số lượng lớn các floodfill router phân tán khắp keyspace.

(Trong một ví dụ liên quan, một nhà nghiên cứu gần đây đã tạo ra [một số lượng lớn các relay Tor](http://blog.torproject.org/blog/june-2010-progress-report).) Nếu thành công, đây có thể là một cuộc tấn công DOS hiệu quả đối với toàn bộ mạng lưới.

Nếu các floodfill không có hành vi sai trái đủ nghiêm trọng để bị đánh dấu là "xấu" bằng các chỉ số hồ sơ peer được mô tả ở trên, đây là một tình huống khó xử lý. Phản ứng của Tor có thể linh hoạt hơn nhiều trong trường hợp relay, vì các relay đáng nghi có thể được gỡ bỏ thủ công khỏi consensus. Một số phản ứng có thể có của mạng I2P được liệt kê dưới đây, tuy nhiên không phản ứng nào trong số đó hoàn toàn thỏa đáng:

- Biên soạn danh sách các router hash hoặc IP xấu, và công bố danh sách qua nhiều phương tiện khác nhau (tin tức console, website, diễn đàn, v.v.); người dùng sẽ phải tự tải xuống danh sách và thêm vào "blacklist" cục bộ của họ.
- Yêu cầu mọi người trong mạng kích hoạt floodfill thủ công (chống Sybil bằng nhiều Sybil hơn)
- Phát hành phiên bản phần mềm mới bao gồm danh sách "xấu" được mã hóa cứng
- Phát hành phiên bản phần mềm mới cải thiện các chỉ số và ngưỡng hồ sơ peer, nhằm cố gắng tự động xác định các peer "xấu".
- Thêm phần mềm loại bỏ floodfill nếu có quá nhiều trong một IP block duy nhất
- Triển khai blacklist tự động dựa trên đăng ký do một cá nhân hoặc nhóm duy nhất kiểm soát. Điều này về cơ bản sẽ thực hiện một phần mô hình "consensus" của Tor. Thật không may, nó cũng sẽ trao cho một cá nhân hoặc nhóm duy nhất quyền lực chặn sự tham gia của bất kỳ router hoặc IP cụ thể nào trong mạng, hoặc thậm chí hoàn toàn tắt hoặc phá hủy toàn bộ mạng.

Cuộc tấn công này trở nên khó khăn hơn khi quy mô mạng lưới tăng lên.

### Tấn công Sybil (Keyspace một phần)

Kẻ tấn công có thể thực hiện [tấn công Sybil](https://www.freehaven.net/anonbib/cache/sybil.pdf) bằng cách tạo ra một số lượng nhỏ (8-15) floodfill router được nhóm lại gần nhau trong keyspace, và phân phối các RouterInfo cho những router này một cách rộng rãi. Khi đó, tất cả các truy vấn và lưu trữ cho một key trong keyspace đó sẽ được chuyển hướng đến một trong những router của kẻ tấn công. Nếu thành công, đây có thể là một cuộc tấn công DOS hiệu quả nhắm vào một I2P Site cụ thể, chẳng hạn.

Vì keyspace được lập chỉ mục bởi Hash mã hóa (SHA256) của khóa, kẻ tấn công phải sử dụng phương pháp brute-force để liên tục tạo ra các router hash cho đến khi có đủ số lượng gần với khóa. Lượng sức mạnh tính toán cần thiết cho việc này, phụ thuộc vào kích thước mạng, vẫn chưa được xác định.

Như một biện pháp phòng thủ một phần chống lại cuộc tấn công này, thuật toán được sử dụng để xác định "độ gần" Kademlia thay đổi theo thời gian. Thay vì sử dụng Hash của khóa (tức là H(k)) để xác định độ gần, chúng ta sử dụng Hash của khóa được nối với chuỗi ngày hiện tại, tức là H(k + YYYYMMDD). Một hàm được gọi là "routing key generator" thực hiện điều này, hàm này biến đổi khóa gốc thành một "routing key". Nói cách khác, toàn bộ không gian khóa netdb "xoay" mỗi ngày vào nửa đêm UTC. Bất kỳ cuộc tấn công không gian khóa một phần nào cũng sẽ phải được tạo lại mỗi ngày, vì sau khi xoay, các router tấn công sẽ không còn gần với khóa mục tiêu, hoặc gần với nhau nữa.

Cuộc tấn công này trở nên khó khăn hơn khi quy mô mạng tăng lên. Tuy nhiên, nghiên cứu gần đây cho thấy việc xoay vòng keyspace không đặc biệt hiệu quả. Kẻ tấn công có thể tính toán trước nhiều router hash, và chỉ cần một vài router là đủ để "che khuất" một phần keyspace trong vòng nửa giờ sau khi xoay vòng.

Một hệ quả của việc xoay vòng keyspace hàng ngày là cơ sở dữ liệu mạng phân tán có thể trở nên không đáng tin cậy trong vài phút sau khi xoay vòng -- các truy vấn sẽ thất bại vì router "gần nhất" mới chưa nhận được lệnh store nào. Mức độ nghiêm trọng của vấn đề này và các phương pháp giảm thiểu (ví dụ như "bàn giao" netDb vào lúc nửa đêm) là chủ đề cần nghiên cứu thêm.

### Tấn công Bootstrap

Kẻ tấn công có thể cố gắng khởi động các router mới vào một mạng bị cô lập hoặc được kiểm soát bởi đa số bằng cách chiếm quyền kiểm soát một trang web reseed, hoặc lừa các nhà phát triển thêm trang web reseed của họ vào danh sách được mã hóa cứng trong router.

Một số biện pháp phòng thủ có thể thực hiện, và hầu hết đều đang được lên kế hoạch:

- Không cho phép chuyển từ HTTPS xuống HTTP khi reseed. Kẻ tấn công MITM có thể đơn giản chặn HTTPS, sau đó phản hồi qua HTTP.
- Tích hợp dữ liệu reseed trong trình cài đặt

Các biện pháp phòng thủ đã được triển khai:

- Thay đổi tác vụ reseed để lấy một tập con các RouterInfo từ mỗi site trong số nhiều reseed site thay vì chỉ sử dụng một site duy nhất
- Tạo một dịch vụ giám sát reseed ngoài mạng để định kỳ kiểm tra các website reseed và xác minh rằng dữ liệu không bị cũ hoặc không nhất quán với các góc nhìn khác về mạng
- Kể từ phiên bản 0.9.14, dữ liệu reseed được đóng gói thành file zip có chữ ký và chữ ký được xác minh khi tải xuống. Xem [đặc tả su3](/docs/specs/updates/#su3) để biết chi tiết.

### Truy Vấn Bắt

Xem thêm [lookup](#routerinfo-and-leaseset-lookup) (Tham khảo: [Hashing it out in Public](http://www-users.cs.umn.edu/~hopper/hashing_it_out.pdf) Phần 2.2-2.3 cho các thuật ngữ dưới đây được in nghiêng)

Tương tự như cuộc tấn công bootstrap, kẻ tấn công sử dụng floodfill router có thể cố gắng "điều hướng" các peer tới một tập hợp con các router do hắn kiểm soát bằng cách trả về các tham chiếu của chúng.

Điều này không có khả năng hoạt động thông qua exploration, bởi vì exploration là một tác vụ tần suất thấp. Các router có được phần lớn tham chiếu peer của chúng thông qua hoạt động xây dựng tunnel bình thường. Kết quả exploration thường bị giới hạn ở một vài router hash, và mỗi truy vấn exploration được hướng tới một floodfill router ngẫu nhiên.

Kể từ phiên bản 0.8.9, *iterative lookups* (tra cứu lặp) đã được triển khai. Đối với các tham chiếu floodfill router được trả về trong phản hồi [I2NP](/docs/specs/i2np/) DatabaseSearchReplyMessage cho một tra cứu, các tham chiếu này được theo dõi nếu chúng gần hơn (hoặc gần nhất tiếp theo) với khóa tra cứu. Router yêu cầu không tin tưởng rằng các tham chiếu gần hơn với khóa (tức là chúng được *xác minh chính xác*). Tra cứu cũng không dừng lại khi không tìm thấy khóa gần hơn, mà tiếp tục bằng cách truy vấn node gần nhất tiếp theo, cho đến khi hết thời gian chờ hoặc đạt số lượng truy vấn tối đa. Điều này ngăn chặn một floodfill độc hại tạo lỗ đen cho một phần của không gian khóa. Ngoài ra, việc xoay vòng keyspace hàng ngày yêu cầu kẻ tấn công phải tạo lại thông tin router trong vùng không gian khóa mong muốn. Thiết kế này đảm bảo rằng cuộc tấn công bắt giữ truy vấn được mô tả trong [Hashing it out in Public](http://www-users.cs.umn.edu/~hopper/hashing_it_out.pdf) trở nên khó khăn hơn nhiều.

### Lựa chọn Relay dựa trên DHT

(Tham khảo: [Hashing it out in Public](http://www-users.cs.umn.edu/~hopper/hashing_it_out.pdf) Mục 3)

Điều này không có nhiều liên quan đến floodfill, nhưng hãy xem [trang lựa chọn peer](/docs/overview/peer-selection/) để thảo luận về các lỗ hổng bảo mật của việc lựa chọn peer cho tunnel.

### Rò rỉ Thông tin

(Tham khảo: [In Search of an Anonymous and Secure Lookup](https://www.freehaven.net/anonbib/cache/ccs10-lookup.pdf) Mục 3)

Bài nghiên cứu này đề cập đến các điểm yếu trong việc tra cứu DHT "Finger Table" được sử dụng bởi Torsk và NISAN. Thoạt nhìn, những điểm này dường như không áp dụng cho I2P. Thứ nhất, việc sử dụng DHT bởi Torsk và NISAN khác biệt đáng kể so với trong I2P. Thứ hai, các tra cứu netDb của I2P chỉ có mối tương quan lỏng lẻo với các quy trình [lựa chọn peer](/docs/overview/peer-selection/) và [xây dựng tunnel](/docs/overview/tunnel-routing/); chỉ những peer đã biết trước đó mới được sử dụng cho tunnel. Ngoài ra, việc lựa chọn peer không liên quan đến bất kỳ khái niệm nào về độ gần gũi khóa DHT.

Một số điều này có thể thực sự trở nên thú vị hơn khi mạng I2P trở nên lớn hơn nhiều. Hiện tại, mỗi router đều biết một tỷ lệ lớn của mạng, vì vậy việc tra cứu một Router Info cụ thể trong cơ sở dữ liệu mạng không thể hiện mạnh mẽ ý định sử dụng router đó trong tunnel trong tương lai. Có lẽ khi mạng lớn hơn 100 lần, việc tra cứu có thể có tính tương quan cao hơn. Tất nhiên, một mạng lớn hơn khiến cuộc tấn công Sybil trở nên khó khăn hơn rất nhiều.

Tuy nhiên, vấn đề chung về rò rỉ thông tin DHT trong I2P cần được điều tra thêm. Các router floodfill đang ở vị trí có thể quan sát các truy vấn và thu thập thông tin. Chắc chắn, ở mức *f* = 0.2 (20% node độc hại, như được chỉ định trong bài báo) chúng ta kỳ vọng rằng nhiều mối đe dọa Sybil mà chúng ta mô tả ([tại đây](/docs/overview/threat-model/#sybil), [tại đây](#sybil-attack-full-keyspace) và [tại đây](#sybil-attack-partial-keyspace)) sẽ trở nên có vấn đề vì một số lý do.

---

## Lịch sử

[Đã chuyển đến trang thảo luận netDb](/docs/legacy/netdb/).

---

## Công Việc Tương Lai

Mã hóa đầu cuối của các truy vấn và phản hồi netDb bổ sung.

Các phương pháp tốt hơn để theo dõi các phản hồi tra cứu.
