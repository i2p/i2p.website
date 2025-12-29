---
title: "Hồ Sơ Dịch Vụ trong LS2"
number: "167"
author: "zzz, hoặc là, eyedeekay"
created: "2024-06-22"
lastupdated: "2025-04-03"
status: "Đã Đóng"
thread: "http://zzz.i2p/topics/3641"
target: "0.9.66"
toc: true
---

## Trạng Thái
Được chấp thuận ở lần xem xét thứ 2 ngày 2025-04-01; đặc tả đã được cập nhật; chưa được triển khai.


## Tổng Quan

I2P không có hệ thống DNS tập trung.
Tuy nhiên, sổ địa chỉ, cùng với hệ thống tên miền b32, cho phép
router tra cứu các đích đến đầy đủ và lấy bộ cho thuê, chứa
danh sách các cổng và khóa để khách hàng có thể kết nối đến đích đó.

Vậy nên, các bộ cho thuê tương tự như một bản ghi DNS. Nhưng hiện tại không có cách nào
để biết nếu máy chủ đó hỗ trợ bất kỳ dịch vụ nào, dù ở đích đó hay ở một đích khác,
theo kiểu tương tự như bản ghi DNS SRV [SRV](https://en.wikipedia.org/wiki/SRV_record) [RFC2782](https://datatracker.ietf.org/doc/html/rfc2782).

Ứng dụng đầu tiên có thể là email ngang hàng.
Các ứng dụng khả thi khác: DNS, GNS, máy chủ khóa, cơ quan chứng nhận, máy chủ thời gian,
bittorrent, tiền điện tử, các ứng dụng ngang hàng khác.


## Đề Xuất Liên Quan và Các Thay Thế

### Danh Sách Dịch Vụ

Đề xuất LS2 123 [Prop123](/proposals/123-new-netdb-entries/) đã định nghĩa 'hồ sơ dịch vụ' mà biểu thị một đích đến
đang tham gia vào một dịch vụ toàn cầu. Các floodfill sẽ tổng hợp các hồ sơ này
thành các 'danh sách dịch vụ' toàn cầu.
Điều này chưa từng được triển khai vì độ phức tạp, thiếu xác thực,
và các lo ngại về bảo mật và spam.

Đề xuất này khác biệt ở chỗ cung cấp tra cứu cho một dịch vụ cho một đích đến cụ thể,
không phải một nhóm các đích toàn cầu cho một dịch vụ toàn cầu.

### GNS

GNS [GNS](http://zzz.i2p/topcs/1545) đề xuất rằng mọi người điều hành máy chủ DNS của riêng họ.
Đề xuất này mang tính bổ sung, với khả năng sử dụng hồ sơ dịch vụ để chỉ rõ
rằng GNS (hoặc DNS) được hỗ trợ, với tên dịch vụ chuẩn là "domain" trên cổng 53.

### Dot well-known

Trong [DOTWELLKNOWN](http://i2pforum.i2p/viewtopic.php?p=3102) có đề xuất rằng dịch vụ được tra cứu qua một yêu cầu HTTP tới
/.well-known/i2pmail.key. Điều này yêu cầu rằng mỗi dịch vụ phải có một trang web liên quan
để lưu trữ khóa. Hầu hết người dùng không chạy các trang web.

Một cách giải quyết là giả định rằng một dịch vụ cho một địa chỉ b32 thực sự
đang chạy trên địa chỉ b32 đó. Như vậy việc tìm kiếm dịch vụ cho example.i2p yêu cầu
lấy dữ liệu HTTP từ http://example.i2p/.well-known/i2pmail.key, nhưng
một dịch vụ cho aaa...aaa.b32.i2p không cần tra cứu đó, nó có thể chỉ cần kết nối trực tiếp.

Nhưng có sự mơ hồ ở đó, bởi vì example.i2p cũng có thể được địa chỉ bởi b32 của nó.

### Bản Ghi MX

Bản ghi SRV chỉ đơn giản là một phiên bản tổng quát của bản ghi MX cho bất kỳ dịch vụ nào.
"_smtp._tcp" là bản ghi "MX".
Không cần có bản ghi MX nếu chúng ta có bản ghi SRV, và các bản ghi MX
không đơn độc cung cấp một bản ghi tổng quát cho bất kỳ dịch vụ nào.


## Thiết Kế

Hồ sơ dịch vụ được đặt trong phần tùy chọn trong LS2 [LS2](/docs/specs/common-structures/).
Phần tùy chọn LS2 hiện đang không được sử dụng.
Không được hỗ trợ cho LS1.
Điều này tương tự như đề xuất băng thông đường hầm [Prop168](/proposals/168-tunnel-bandwidth/),
định nghĩa các tùy chọn cho các bản ghi dịch xây dựng đường hầm.

Để tra cứu địa chỉ dịch vụ cho một hostname cụ thể hoặc b32, router lấy
bộ cho thuê và tra cứu hồ sơ dịch vụ trong các thuộc tính.

Dịch vụ có thể được lưu trữ trên cùng đích với bản thân LS, hoặc có thể tham chiếu
đến một hostname/b32 khác.

Nếu đích đến mục tiêu cho dịch vụ là khác nhau, thì LS mục tiêu cũng phải
bao gồm một hồ sơ dịch vụ, chỉ về chính nó, chỉ ra rằng nó hỗ trợ dịch vụ.

Thiết kế không yêu cầu hỗ trợ đặc biệt hoặc bộ nhớ đệm hay bất kỳ sự thay đổi nào trong floodfills.
Chỉ người xuất bản bộ cho thuê, và khách hàng tra cứu hồ sơ dịch vụ,
phải hỗ trợ những thay đổi này.

Các mở rộng nhỏ I2CP và SAM được đề xuất để hỗ trợ truy xuất
hồ sơ dịch vụ bởi khách hàng.


## Đặc Tả

### Đặc Tả Tùy Chọn LS2

Các tùy chọn của LS2 PHẢI được sắp xếp theo khóa, để chữ ký không thay đổi.

Định nghĩa như sau:

- tùy chọnDịchVụ := khóaTùyChọn giáTrịTùyChọn
- khóaTùyChọn := _service._proto
- dịch vụ := Tên tượng trưng của dịch vụ mong muốn. Phải viết bằng chữ thường. Ví dụ: "smtp".
  Các ký tự được phép là [a-z0-9-] và không được bắt đầu hoặc kết thúc bằng '-'.
  Các nhận dạng chuẩn từ [REGISTRY](http://www.dns-sd.org/ServiceTypes.html) hoặc Linux /etc/services phải được sử dụng nếu có định nghĩa trong đó.
- proto := Giao thức truyền của dịch vụ mong muốn. Phải viết bằng chữ thường, hoặc "tcp" hoặc "udp".
  "tcp" có nghĩa là truyền tải dòng và "udp" có nghĩa là gói dữ liệu có thể đối đáp.
  Các chỉ thị giao thức cho gói dữ liệu thô và datagram2 có thể được định nghĩa sau.
  Các ký tự được phép là [a-z0-9-] và không được bắt đầu hoặc kết thúc bằng '-'.
- giáTrịTùyChọn := self | srvrecord[,srvrecord]*
- self := "0" ttl port [appoptions]
- srvrecord := "1" ttl priority weight port target [appoptions]
- ttl := thời gian sống, số nguyên giây. Số nguyên dương. Ví dụ: "86400".
  Tối thiểu là 86400 (một ngày) được khuyên dùng, xem Phần Khuyến Nghị bên dưới để biết chi tiết.
- priority := Ưu tiên của máy chủ mục tiêu, giá trị thấp hơn có nghĩa là ưu tiên hơn. Số nguyên không âm. Ví dụ: "0"
  Chỉ hữu ích nếu có nhiều hơn một bản ghi, nhưng vẫn cần ngay cả khi chỉ có một bản ghi.
- weight := Trọng số tương đối cho các bản ghi cùng một ưu tiên. Giá trị cao hơn có nghĩa là khả năng được chọn cao hơn. Số nguyên không âm. Ví dụ: "0"
  Chỉ hữu ích nếu có nhiều hơn một bản ghi, nhưng vẫn cần ngay cả khi chỉ có một bản ghi.
- port := Cổng I2CP mà dịch vụ được tìm thấy. Số nguyên không âm. Ví dụ: "25"
  Cổng 0 được hỗ trợ nhưng không được khuyến nghị.
- target := Hostname hoặc b32 của đích cung cấp dịch vụ. Một hostname hợp lệ như trong [NAMING](/docs/overview/naming/). Phải viết bằng chữ thường.
  Ví dụ: "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.b32.i2p" hoặc "example.i2p".
  b32 được khuyến khích trừ khi hostname là "rất quen thuộc", ví dụ trong sổ địa chỉ chính thức hoặc mặc định.
- appoptions := văn bản tùy ý cụ thể cho ứng dụng, không được chứa " " hoặc ",". Mã hóa là UTF-8.

### Ví dụ


Trong LS2 cho aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.b32.i2p, chỉ về một máy chủ SMTP:

    "_smtp._tcp" "1 86400 0 0 25 bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb.b32.i2p"

Trong LS2 cho aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.b32.i2p, chỉ về hai máy chủ SMTP:

    "_smtp._tcp" "1 86400 0 0 25 bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb.b32.i2p,86400 1 0 25 cccccccccccccccccccccccccccccccccccccccccccc.b32.i2p"

Trong LS2 cho bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb.b32.i2p, chỉ về chính nó như một máy chủ SMTP:

    "_smtp._tcp" "0 999999 25"

Định dạng khả thi cho chuyển tiếp email (xem bên dưới):

    "_smtp._tcp" "1 86400 0 0 25 smtp.postman.i2p example@mail.i2p"


### Giới Hạn


Định dạng cấu trúc dữ liệu Mapping được sử dụng cho các tùy chọn LS2 giới hạn các khóa và giá trị ở mức tối đa 255 byte (không phải ký tự).
Với một mục tiêu b32, giá trịTùyChọn khoảng 67 byte, nên chỉ có 3 bản ghi sẽ phù hợp.
Có thể chỉ một hoặc hai bản ghi với một trường appoptions dài, hoặc tối đa bốn hoặc năm bản ghi với một hostname ngắn.
Điều này nên đủ; nhiều bản ghi nên hiếm.


### Khác biệt so với [RFC2782](https://datatracker.ietf.org/doc/html/rfc2782)


- Không có dấu chấm ở cuối
- Không có tên sau proto
- Yêu cầu chữ thường
- Ở định dạng văn bản với các bản ghi phân tách bằng dấu phẩy, không phải định dạng nhị phân DNS
- Các chỉ báo loại bản ghi khác nhau
- Thêm trường appoptions


### Ghi chú


Không cho phép wildcard như (dấu sao), (dấu sao)._tcp, hay _tcp.
Mỗi dịch vụ được hỗ trợ phải có bản ghi riêng của mình.


### Đăng Ký Tên Dịch Vụ

Các định danh không chuẩn mà không được liệt kê trong [REGISTRY](http://www.dns-sd.org/ServiceTypes.html) hoặc Linux /etc/services
có thể được yêu cầu và thêm vào đặc tả cấu trúc chung [LS2](/docs/specs/common-structures/).

Các định dạng appoptions cụ thể cho dịch vụ cũng có thể được thêm vào đó.


### Đặc Tả I2CP

Giao thức [I2CP](/docs/specs/i2cp/) phải được mở rộng để hỗ trợ tra cứu dịch vụ.
Các mã lỗi MessageStatusMessage và/hoặc HostReplyMessage liên quan đến tra cứu dịch vụ
cần thiết.
Để làm cho cơ sở tra cứu trở nên tổng quát, không chỉ hồ sơ dịch vụ cụ thể,
thiết kế là để hỗ trợ việc lấy tất cả các tùy chọn LS2.

Triển khai: Mở rộng HostLookupMessage để thêm yêu cầu cho
các tùy chọn LS2 cho hash, hostname, và đích đến (loại yêu cầu 2-4).
Mở rộng HostReplyMessage để thêm ánh xạ tùy chọn nếu được yêu cầu.
Mở rộng HostReplyMessage với các mã lỗi bổ sung.

Ánh xạ tùy chọn có thể được lưu đệm hoặc lưu đệm tiêu cực trong một thời gian ngắn ở cả phía khách hàng hoặc router,
tùy thuộc vào việc triển khai. Thời gian tối đa khuyến nghị là một giờ, trừ khi TTL hồ sơ dịch vụ ngắn hơn.
Các hồ sơ dịch vụ có thể được lưu đệm tối đa TTL được chỉ định bởi ứng dụng, khách hàng hoặc router.

Mở rộng đặc tả như sau:

### Tùy chọn cấu hình

Thêm những mục sau vào [I2CP-OPTIONS]

i2cp.leaseSetOption.nnn

Tùy chọn để đưa vào bộ cho thuê. Chỉ có sẵn cho LS2.
nnn bắt đầu với 0. Giá trị tùy chọn chứa "key=value".
(không bao gồm ngoặc kép)

Ví dụ:

    i2cp.leaseSetOption.0=_smtp._tcp=1 86400 0 0 25 bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb.b32.i2p


### Bản Tin HostLookup


- Loại tra cứu 2: Tra cứu Hash, yêu cầu ánh xạ tùy chọn
- Loại tra cứu 3: Tra cứu Hostname, yêu cầu ánh xạ tùy chọn
- Loại tra cứu 4: Tra cứu Đích, yêu cầu ánh xạ tùy chọn

Đối với loại tra cứu 4, mục 5 là một Đích.


### Bản Tin HostReply


Đối với các loại tra cứu 2-4, router phải lấy bộ cho thuê,
ngay cả khi khóa tra cứu có trong sổ địa chỉ.

Nếu thành công, HostReply sẽ chứa ánh xạ tùy chọn
từ bộ cho thuê và bao gồm nó là mục 5 sau đích đến.
Nếu không có tùy chọn nào trong ánh xạ, hoặc bộ cho thuê là phiên bản 1,
nó sẽ vẫn được bao gồm dưới dạng một ánh xạ rỗng (hai byte: 0 0).
Tất cả các tùy chọn từ bộ cho thuê sẽ được bao gồm, không chỉ các tùy chọn hồ sơ dịch vụ.
Ví dụ, các tùy chọn cho các tham số được định nghĩa trong tương lai có thể có mặt.

Trên lỗi tra cứu bộ cho thuê, câu trả lời sẽ chứa một mã lỗi mới 6 (Leaseset lookup failure)
và sẽ không bao gồm một ánh xạ.
Khi mã lỗi 6 được trả về, trường Đích có thể có hoặc không có mặt.
Nó sẽ có mặt nếu một tra cứu hostname trong sổ địa chỉ đã thành công,
hoặc nếu một tra cứu trước đó đã thành công và kết quả đã được lưu đệm,
hoặc nếu Đích có mặt trong tin nhắn tra cứu (loại tra cứu 4).

Nếu một loại tra cứu không được hỗ trợ,
câu trả lời sẽ chứa một mã lỗi mới 7 (lookup type unsupported).


### Đặc Tả SAM

Giao thức [SAMv3](/docs/api/samv3/) phải được mở rộng để hỗ trợ tra cứu dịch vụ.

Mở rộng NAMING LOOKUP như sau:

NAMING LOOKUP NAME=example.i2p OPTIONS=true yêu cầu ánh xạ tùy chọn trong câu trả lời.

NAME có thể là một đích đầy đủ base64 khi OPTIONS=true.

Nếu việc tra cứu đích thành công và tùy chọn có mặt trong bộ cho thuê,
thì trong câu trả lời, sau đích đến,
sẽ là một hoặc nhiều tùy chọn dưới dạng OPTION:key=value.
Mỗi tùy chọn sẽ có một tiền tố OPTION: riêng biệt.
Tất cả các tùy chọn từ bộ cho thuê sẽ được bao gồm, không chỉ các tùy chọn hồ sơ dịch vụ.
Ví dụ, các tùy chọn cho các tham số được định nghĩa trong tương lai có thể có mặt.
Ví dụ:

    NAMING REPLY RESULT=OK NAME=example.i2p VALUE=base64dest OPTION:_smtp._tcp="1 86400 0 0 25 bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb.b32.i2p"

Các khóa chứa '=' và các khóa hoặc giá trị chứa một dòng mới,
được coi là không hợp lệ và cặp khóa/giá trị sẽ bị loại bỏ khỏi câu trả lời.

Nếu không có tùy chọn nào được tìm thấy trong bộ cho thuê, hoặc nếu bộ cho thuê là phiên bản 1,
thì câu trả lời sẽ không bao gồm bất kỳ tùy chọn nào.

Nếu OPTIONS=true có trong tra cứu, và bộ cho thuê không được tìm thấy, một giá trị kết quả mới LEASESET_NOT_FOUND sẽ được trả về.


## Thay Thế Tra Cứu Tên

Một thiết kế thay thế đã được xem xét, để hỗ trợ tra cứu các dịch vụ
như một hostname đầy đủ, ví dụ: _smtp._tcp.example.i2p,
bằng cách cập nhật [NAMING](/docs/overview/naming/) để chỉ định cách xử lý các hostname bắt đầu với '_'.
Điều này đã bị từ chối vì hai lý do:

- Các thay đổi I2CP và SAM vẫn cần thiết để truyền qua thông tin TTL và cổng cho khách hàng.
- Nó sẽ không phải là một công cụ tổng quát có thể dùng để lấy các tùy chọn LS2 khác
  có thể được định nghĩa trong tương lai.


## Khuyến Nghị

Máy chủ nên chỉ định TTL ít nhất là 86400, và cổng chuẩn cho ứng dụng.


## Các Tính Năng Nâng Cao

### Tra Cứu Đệ Quy

Có thể mong muốn hỗ trợ các tra cứu đệ quy, nơi mà mỗi bộ cho thuê liên tiếp
được kiểm tra cho hồ sơ dịch vụ chỉ đến một bộ cho thuê khác, theo kiểu DNS.
Điều này có lẽ không cần thiết, ít nhất trong một lần triển khai ban đầu.

TODO


### Các trường cụ thể theo ứng dụng

Có thể mong muốn có dữ liệu ứng dụng cụ thể trong hồ sơ dịch vụ.
Ví dụ, người điều hành example.i2p có thể muốn chỉ định rằng email nên
được chuyển tiếp đến example@mail.i2p. Phần "example@" cần nằm trong một trường riêng
của hồ sơ dịch vụ, hoặc được loại bỏ khỏi mục tiêu.

Ngay cả khi người điều hành chạy dịch vụ email của riêng mình, anh ta có thể muốn chỉ định rằng
email nên được gửi đến example@example.i2p. Hầu hết các dịch vụ I2P do một người điều hành.
Vì vậy, có thể hữu ích có một trường riêng ở đây.

TODO làm thế nào để làm điều này theo cách tổng quát


### Các thay đổi cần thiết cho Email

Ngoài phạm vi của đề xuất này. Xem [DOTWELLKNOWN](http://i2pforum.i2p/viewtopic.php?p=3102) để có thảo luận.


## Ghi Chú Triển Khai

Lưu đệm hồ sơ dịch vụ lên đến TTL có thể được thực hiện bởi router hoặc ứng dụng,
tùy thuộc vào việc triển khai. Có lưu đệm lâu dài hay không cũng tùy thuộc vào việc triển khai.

Các tra cứu cũng phải tra cứu bộ cho thuê mục tiêu và xác minh rằng nó chứa một hồ sơ "self"
trước khi trả về đích đến mục tiêu cho khách hàng.


## Phân Tích Bảo Mật

Vì bộ cho thuê được ký, bất kỳ hồ sơ dịch vụ nào trong đó đều được xác thực bởi khóa ký của đích đến.

Các hồ sơ dịch vụ là công khai và nhìn thấy được bởi floodfills, trừ khi bộ cho thuê được mã hóa.
Bất kỳ router nào yêu cầu bộ cho thuê sẽ có thể thấy các hồ sơ dịch vụ.

Một hồ sơ SRV khác "self" (tức là, một hồ sơ chỉ đến một mục tiêu hostname/b32 khác)
không yêu cầu sự đồng ý của hostname/b32 được chỉ định.
Không rõ nếu việc chuyển hướng một dịch vụ đến một đích tùy ý có thể tạo điều kiện cho một
cuộc tấn công nào đó, hay mục đích của một cuộc tấn công như vậy sẽ là gì.
Tuy nhiên, đề xuất này giảm thiểu một cuộc tấn công như vậy bằng cách yêu cầu rằng
mục tiêu cũng phải công bố một hồ sơ SRV "self". Những người triển khai phải kiểm tra cho một hồ sơ "self"
trong bộ cho thuê của mục tiêu.


## Khả Năng Tương Thích

LS2: Không có vấn đề. Tất cả các triển khai đã biết hiện tại đều bỏ qua trường tùy chọn trong LS2,
và bỏ qua chính xác một trường tùy chọn không rỗng.
Điều này đã được xác minh trong thử nghiệm bởi cả Java I2P và i2pd trong quá trình phát triển LS2.
LS2 đã được triển khai trong 0.9.38 vào năm 2016 và được hỗ trợ tốt bởi tất cả các triển khai router.
Thiết kế không yêu cầu hỗ trợ đặc biệt hoặc lưu đệm hay bất kỳ sự thay đổi nào trong floodfills.

Naming: '_' không phải là một ký tự hợp lệ trong các hostname của i2p.

I2CP: Các loại tra cứu 2-4 không nên được gửi đến các router dưới phiên bản API tối thiểu
mà nó được hỗ trợ (TBD).

SAM: Máy chủ Java SAM bỏ qua các khóa/giá trị bổ sung như OPTIONS=true.
i2pd cũng nên vậy, cần được xác minh.
Khách hàng SAM sẽ không nhận được các giá trị bổ sung trong câu trả lời trừ khi được yêu cầu với OPTIONS=true.
Không cần tăng phiên bản.


