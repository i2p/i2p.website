---
title: "Bittorrent trên I2P"
description: "Đặc tả giao thức cho các client BitTorrent và tracker trên I2P"
slug: "bittorrent"
lastUpdated: "2026-08"
accurateFor: "0.9.70"
---

Có một số client và tracker bittorrent trên I2P. Vì địa chỉ I2P sử dụng Destination thay vì IP và port, nên cần có một số thay đổi nhỏ đối với phần mềm tracker và client để hoạt động trên I2P. Những thay đổi này được mô tả bên dưới. Lưu ý kỹ các hướng dẫn về khả năng tương thích với các client và tracker I2P cũ hơn.

Trang này chỉ định các chi tiết giao thức chung cho tất cả client và tracker. Các client và tracker cụ thể có thể triển khai các tính năng hoặc giao thức độc đáo khác.

Chúng tôi hoan nghênh việc chuyển đổi thêm các phần mềm client và tracker sang I2P.

---

## Hướng Dẫn Chung cho Nhà Phát Triển

Hầu hết các client bittorrent không phải Java sẽ kết nối với I2P thông qua [SAMv3](/docs/api/samv3/). Các phiên SAM (hoặc bên trong I2P là tunnel pools hoặc tập hợp các tunnel) được thiết kế để tồn tại lâu dài. Hầu hết các client bittorrent chỉ cần một phiên duy nhất, được tạo khi khởi động và đóng khi thoát. I2P khác với Tor, nơi các mạch có thể được tạo và loại bỏ nhanh chóng. Hãy suy nghĩ cẩn thận và tham khảo ý kiến các nhà phát triển I2P trước khi thiết kế ứng dụng sử dụng hơn một hoặc hai phiên đồng thời, hoặc tạo và loại bỏ chúng nhanh chóng. Các client bittorrent không được tạo phiên duy nhất cho mỗi kết nối. Thiết kế client của bạn để sử dụng cùng một phiên cho announces và kết nối client.

Ngoài ra, vui lòng đảm bảo rằng các cài đặt client của bạn (và hướng dẫn cho người dùng về cài đặt router, hoặc cài đặt mặc định của router nếu bạn đi kèm một router) sẽ giúp người dùng của bạn đóng góp nhiều tài nguyên cho mạng hơn là họ tiêu thụ. I2P là một mạng ngang hàng, và mạng không thể tồn tại nếu một ứng dụng phổ biến đẩy mạng vào tình trạng tắc nghẽn thường xuyên.

Không cung cấp hỗ trợ cho bittorrent thông qua I2P outproxy đến clearnet vì nó có thể sẽ bị chặn. Hãy tham khảo ý kiến từ các nhà vận hành outproxy để được hướng dẫn.

Các triển khai router Java I2P và i2pd là độc lập và có những khác biệt nhỏ về hành vi, hỗ trợ tính năng và cài đặt mặc định. Vui lòng kiểm tra ứng dụng của bạn với phiên bản mới nhất của cả hai router.

i2pd SAM được kích hoạt mặc định; Java I2P SAM thì không. Hãy cung cấp hướng dẫn cho người dùng về cách kích hoạt SAM trong Java I2P (thông qua /configclients trong router console), và/hoặc cung cấp thông báo lỗi rõ ràng cho người dùng nếu kết nối ban đầu thất bại, ví dụ: "đảm bảo rằng I2P đang chạy và giao diện SAM đã được kích hoạt".

Các router Java I2P và i2pd có cài đặt mặc định khác nhau cho số lượng tunnel. Mặc định của Java là 2 và mặc định của i2pd là 5. Đối với hầu hết các trường hợp có băng thông thấp đến trung bình và số lượng kết nối thấp đến trung bình, 3 là đủ. Vui lòng chỉ định số lượng tunnel trong thông điệp SESSION CREATE để có được hiệu suất nhất quán với các router Java I2P và i2pd.

I2P hỗ trợ nhiều loại chữ ký và mã hóa. Để đảm bảo tương thích, I2P mặc định sử dụng các loại cũ và không hiệu quả, vì vậy tất cả các client nên chỉ định các loại mới hơn.

Nếu sử dụng SAM, loại chữ ký được chỉ định trong các lệnh DEST GENERATE và SESSION CREATE (cho tạm thời). Tất cả client nên đặt SIGNATURE_TYPE=7 (Ed25519).

Loại mã hóa được chỉ định trong lệnh SAM SESSION CREATE hoặc trong các tùy chọn i2cp. Nhiều loại mã hóa được cho phép. Một số tracker hỗ trợ ECIES-X25519, một số hỗ trợ ElGamal, và một số hỗ trợ cả hai. Client nên đặt i2cp.leaseSetEncType=4,0 (cho ECIES-X25519 và ElGamal) để có thể kết nối đến cả hai.

Hỗ trợ DHT yêu cầu SAMv3.3 PRIMARY và SUBSESSIONS cho TCP và UDP trên cùng một phiên. Điều này sẽ đòi hỏi nỗ lực phát triển đáng kể ở phía client, trừ khi client được viết bằng Java. i2pd hiện tại không hỗ trợ SAMv3.3. libtorrent hiện tại không hỗ trợ SAMv3.3.

Không có hỗ trợ DHT, bạn có thể muốn tự động thông báo đến một danh sách có thể cấu hình các tracker mở đã biết để các liên kết magnet hoạt động được. Tham khảo ý kiến từ người dùng I2P để biết thông tin về các tracker mở hiện đang hoạt động và giữ cho các cài đặt mặc định của bạn luôn cập nhật. Hỗ trợ tiện ích mở rộng i2p_pex cũng sẽ giúp giảm bớt việc thiếu hỗ trợ DHT.

Để được hướng dẫn thêm cho các nhà phát triển về việc đảm bảo ứng dụng của bạn chỉ sử dụng các tài nguyên cần thiết, vui lòng xem [đặc tả SAMv3](/docs/api/samv3/) và [hướng dẫn tích hợp I2P với ứng dụng của bạn](/docs/applications/embedding/). Liên hệ với các nhà phát triển I2P hoặc i2pd để được hỗ trợ thêm.

---

## Thông báo

Các client thường bao gồm một tham số port=6881 giả trong announce, để tương thích với các tracker cũ hơn. Các tracker có thể bỏ qua tham số port và không nên yêu cầu nó.

Tham số ip là base 64 của [Destination](/docs/specs/common-structures/#struct_Destination) của client, sử dụng bảng chữ cái I2P Base 64 [A-Z][a-z][0-9]-~. [Destinations](/docs/specs/common-structures/#struct_Destination) có kích thước 387+ byte, do đó Base 64 có kích thước 516+ byte. Các client thường thêm ".i2p" vào cuối Base 64 Destination để tương thích với các tracker cũ. Các tracker không nên yêu cầu phải có ".i2p" được thêm vào.

Các tham số khác giống như trong bittorrent tiêu chuẩn.

Các Destination hiện tại cho client có kích thước từ 387 byte trở lên (516 byte trở lên khi mã hóa Base 64). Một giá trị tối đa hợp lý để giả định hiện tại là 475 byte. Vì tracker phải giải mã Base64 để cung cấp các phản hồi compact (xem bên dưới), tracker có lẽ nên giải mã và từ chối Base64 không hợp lệ khi được thông báo.

Loại phản hồi mặc định là không nén gọn (non-compact). Client có thể yêu cầu phản hồi nén gọn với tham số compact=1. Tracker có thể, nhưng không bắt buộc, trả về phản hồi nén gọn khi được yêu cầu. Lưu ý: Tất cả các tracker phổ biến hiện tại đều hỗ trợ phản hồi nén gọn và ít nhất một tracker yêu cầu compact=1 trong announce. Tất cả client nên yêu cầu và hỗ trợ phản hồi nén gọn.

Các lập trình viên phát triển I2P client mới được khuyến khích mạnh mẽ triển khai announces qua tunnel của riêng họ thay vì qua HTTP client proxy tại cổng 4444. Làm như vậy vừa hiệu quả hơn vừa cho phép tracker thực thi kiểm soát destination (xem bên dưới).

Đặc tả cho các thông báo UDP đã được hoàn thiện vào tháng 6/2025. Hỗ trợ trong các client I2P và tracker khác nhau sẽ được triển khai dần trong năm 2025. Xem thêm thông tin bổ sung bên dưới.

---

## Phản hồi Tracker không nén

Lưu ý: Đã lỗi thời. Tất cả các tracker phổ biến hiện tại đều hỗ trợ phản hồi compact và ít nhất một tracker yêu cầu compact=1 trong announce. Tất cả client nên yêu cầu và hỗ trợ phản hồi compact.

Phản hồi non-compact giống như trong bittorrent tiêu chuẩn, với một "ip" I2P. Đây là một "chuỗi DNS" dài được mã hóa base64, có thể có hậu tố ".i2p".

Các tracker thường bao gồm một khóa cổng giả, hoặc sử dụng cổng từ thông báo, để tương thích với các client cũ hơn. Các client phải bỏ qua tham số cổng và không nên yêu cầu nó.

Giá trị của khóa ip là base 64 của [Destination](/docs/specs/common-structures/#struct_Destination) của client, như đã mô tả ở trên. Các tracker thường thêm ".i2p" vào Base 64 Destination nếu nó không có trong announce ip, để tương thích với các client cũ hơn. Các client không nên yêu cầu phải có ".i2p" được thêm vào trong các phản hồi.

Các khóa và giá trị phản hồi khác giống như trong bittorrent tiêu chuẩn.

---

## Phản hồi Tracker nhỏ gọn

Trong phản hồi compact, giá trị của khóa từ điển "peers" là một chuỗi byte đơn, có độ dài là bội số của 32 byte. Chuỗi này chứa các [Hash SHA-256 32-byte](/docs/specs/common-structures/#type_Hash) được nối liên tiếp của các [Destinations](/docs/specs/common-structures/#struct_Destination) nhị phân của các peer. Hash này phải được tính toán bởi tracker, trừ khi sử dụng destination enforcement (xem bên dưới), trong trường hợp đó hash được gửi trong các HTTP header X-I2P-DestHash hoặc X-I2P-DestB32 có thể được chuyển đổi thành nhị phân và lưu trữ. Khóa peers có thể không có, hoặc giá trị peers có thể có độ dài bằng không.

Mặc dù hỗ trợ phản hồi compact là tùy chọn cho cả client và tracker, nhưng việc này được khuyến nghị mạnh vì nó giảm kích thước phản hồi danh nghĩa hơn 90%.

---

## Thực thi Điểm đến

Một số, nhưng không phải tất cả, client bittorrent I2P thông báo qua tunnel riêng của chúng. Các tracker có thể chọn ngăn chặn việc giả mạo bằng cách yêu cầu điều này và xác minh [Destination](/docs/specs/common-structures/#struct_Destination) của client bằng cách sử dụng các header HTTP được thêm bởi tunnel I2PTunnel HTTP Server. Các header là X-I2P-DestHash, X-I2P-DestB64, và X-I2P-DestB32, đây là các định dạng khác nhau cho cùng một thông tin. Các header này không thể bị client giả mạo. Một tracker thực thi destination không cần yêu cầu tham số ip announce.

Vì một số client sử dụng HTTP proxy thay vì tunnel riêng của chúng để thông báo, việc thực thi đích đến sẽ ngăn cản việc sử dụng của những client đó trừ khi hoặc cho đến khi những client đó được chuyển đổi để thông báo qua tunnel riêng của chúng.

Thật không may, khi mạng lưới phát triển, lượng hoạt động độc hại cũng sẽ tăng theo, vì vậy chúng tôi dự đoán rằng tất cả các tracker cuối cùng sẽ áp dụng việc kiểm soát destination. Cả nhà phát triển tracker và client đều nên lường trước điều này.

---

## Thông báo tên máy chủ

Tên máy chủ URL thông báo trong các tệp torrent thường tuân theo [tiêu chuẩn đặt tên I2P](/docs/overview/naming/). Ngoài các tên máy chủ từ sổ địa chỉ và tên máy chủ Base 32 ".b32.i2p", thì Destination Base 64 đầy đủ (có hoặc không có ".i2p" được thêm vào) cũng nên được hỗ trợ. Các tracker không công khai nên nhận dạng tên máy chủ của chính mình ở bất kỳ định dạng nào trong số này.

Để bảo vệ tính ẩn danh, các client nên bỏ qua các URL thông báo không phải I2P trong các tệp torrent.

---

## Kết Nối Client

Các kết nối từ client đến client sử dụng giao thức tiêu chuẩn qua TCP. Hiện tại không có client I2P nào được biết đến hỗ trợ giao tiếp uTP.

I2P sử dụng [Destinations](/docs/specs/common-structures/#struct_Destination) có kích thước 387+ byte cho địa chỉ, như đã giải thích ở trên.

Nếu client chỉ có hash của destination (chẳng hạn từ compact response hoặc PEX), nó phải thực hiện tra cứu bằng cách mã hóa nó với Base 32, thêm ".b32.i2p" vào cuối, và truy vấn Naming Service, service này sẽ trả về Destination đầy đủ nếu có sẵn.

Nếu client có Destination đầy đủ của peer mà nó nhận được trong một phản hồi không nén, nó nên sử dụng trực tiếp trong quá trình thiết lập kết nối. Không nên chuyển đổi Destination trở lại thành hash Base 32 để tra cứu, điều này khá không hiệu quả.

---

## Ngăn chặn Mạng chéo

Để bảo vệ tính ẩn danh, các client bittorrent I2P thường không hỗ trợ các thông báo hoặc kết nối peer không phải I2P. Các HTTP outproxy I2P thường chặn các thông báo. Không có SOCKS outproxy nào được biết đến hỗ trợ lưu lượng bittorrent.

Để ngăn chặn việc sử dụng bởi các client không phải I2P thông qua HTTP inproxy, các I2P tracker thường chặn các truy cập hoặc thông báo chứa header HTTP X-Forwarded-For. Các tracker nên từ chối các thông báo mạng tiêu chuẩn với IPv4 hoặc IPv6 IP, và không gửi chúng trong các phản hồi.

---

## PEX

I2P PEX dựa trên ut_pex. Vì dường như không có thông số kỹ thuật chính thức của ut_pex, có thể cần phải xem xét mã nguồn libtorrent để được hỗ trợ. Đây là một thông điệp mở rộng, được xác định là "i2p_pex" trong [quá trình bắt tay mở rộng](http://www.bittorrent.org/beps/bep_0010.html). Nó chứa một từ điển được mã hóa bencoded với tối đa 3 khóa: "added", "added.f", và "dropped". Các giá trị added và dropped mỗi cái là một chuỗi byte đơn, có độ dài là bội số của 32 byte. Những chuỗi byte này là các SHA-256 Hash được nối liền nhau của các [Destinations](/docs/specs/common-structures/#struct_Destination) nhị phân của các peer. Đây là cùng định dạng với giá trị từ điển peers trong định dạng phản hồi compact i2p được chỉ định ở trên. Giá trị added.f, nếu có, thì giống như trong ut_pex.

---

## DHT

Hỗ trợ DHT được bao gồm trong client i2psnark từ phiên bản 0.9.2. Các khác biệt sơ bộ so với [BEP 5](http://www.bittorrent.org/beps/bep_0005.html) được mô tả bên dưới và có thể thay đổi. Liên hệ với các nhà phát triển I2P nếu bạn muốn phát triển một client hỗ trợ DHT.

Không giống như DHT tiêu chuẩn, I2P DHT không sử dụng bit trong handshake options, hoặc thông điệp PORT. Nó được quảng cáo bằng một thông điệp mở rộng, được định danh là "i2p_dht" trong [extension handshake](http://www.bittorrent.org/beps/bep_0010.html). Nó chứa một dictionary được mã hóa bencoded với hai khóa, "port" và "rport", cả hai đều là số nguyên.

Cổng UDP (datagram) được liệt kê trong thông tin node compact được sử dụng để nhận các datagram có thể phản hồi (đã ký). Điều này được sử dụng cho các truy vấn, ngoại trừ các thông báo. Chúng tôi gọi đây là "cổng truy vấn". Đây là giá trị "port" từ thông điệp mở rộng. Các truy vấn sử dụng giao thức [I2CP](/docs/specs/i2cp/) số 17.

Ngoài cổng UDP đó, chúng tôi sử dụng một cổng datagram thứ hai bằng cổng truy vấn + 1. Cổng này được sử dụng để nhận các datagram không được ký (thô) cho các phản hồi, lỗi và thông báo. Cổng này cung cấp hiệu quả tăng lên vì các phản hồi chứa token được gửi trong truy vấn và không cần phải được ký. Chúng tôi gọi đây là "response port". Đây là giá trị "rport" từ thông điệp mở rộng. Nó phải bằng 1 + cổng truy vấn. Các phản hồi và thông báo sử dụng số giao thức [I2CP](/docs/specs/i2cp/) 18.

Thông tin peer nhỏ gọn là 32 byte (SHA256 Hash 32 byte) thay vì IP 4 byte + port 2 byte. Không có port của peer. Trong phản hồi, khóa "values" là một danh sách các chuỗi, mỗi chuỗi chứa một thông tin peer nhỏ gọn duy nhất.

Thông tin node compact là 54 byte (20 byte Node ID + 32 byte SHA256 Hash + 2 byte port) thay vì 20 byte Node ID + 4 byte IP + 2 byte port. Trong một phản hồi, khóa "nodes" là một chuỗi byte đơn với thông tin node compact được nối liền.

Yêu cầu ID node bảo mật: Để làm cho các cuộc tấn công DHT khó khăn hơn, 4 byte đầu tiên của ID Node phải khớp với 4 byte đầu tiên của Hash đích, và hai byte tiếp theo của ID Node phải khớp với hai byte tiếp theo của hash đích được thực hiện phép XOR với port.

Trong file torrent, khóa "nodes" của từ điển torrent trackerless vẫn đang được xác định (TBD). Nó có thể là một danh sách các chuỗi nhị phân 32 byte (SHA256 Hashes) thay vì một danh sách các danh sách chứa một chuỗi host và một số nguyên port. Các phương án thay thế: Một chuỗi byte đơn với các hash được nối liền, hoặc chỉ một danh sách các chuỗi.

---

## Tracker Datagram (UDP)

Đặc tả cho UDP announces trong I2P đã được hoàn thiện vào tháng 6-2025. Hỗ trợ trong các I2P client và tracker khác nhau sẽ được triển khai dần trong năm 2025. Các điểm khác biệt so với [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) được ghi lại trong [đặc tả UDP announce](/docs/specs/udp-announces/). Đặc tả này cũng yêu cầu hỗ trợ cho [các định dạng Datagram 2/3 mới](/docs/specs/datagrams/).

---

## Thông Tin Bổ Sung

Một đặc tả sơ bộ để tính toán tập hợp nhanh được phép đã được nêu trong [Đề xuất 172](/proposals/172-bep6-allowed-fast)

---

## Thông tin bổ sung

- Các tiêu chuẩn I2P bittorrent thường được thảo luận trên [zzz.i2p](http://zzz.i2p/).
- Một biểu đồ về khả năng của phần mềm tracker hiện tại cũng [có sẵn tại đây](http://zzz.i2p/files/trackers.html).
- [FAQ I2P bittorrent](http://forum.i2p/viewtopic.php?t=2068)
- [Thảo luận về DHT trên I2P](http://zzz.i2p/topics/812)
