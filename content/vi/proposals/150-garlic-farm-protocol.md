---
title: "Giao Thức Garlic Farm"
number: "150"
author: "zzz"
created: "2019-05-02"
lastupdated: "2019-05-20"
status: "Open"
thread: "http://zzz.i2p/topics/2234"
toc: true
---

## Tổng Quan

Đây là đặc tả cho giao thức dây Garlic Farm,
dựa trên JRaft, mã "exts" của nó để triển khai qua TCP,
và ứng dụng mẫu "dmprinter" của nó [JRAFT](https://github.com/datatechnology/jraft).
JRaft là một triển khai của giao thức Raft [RAFT](https://ramcloud.stanford.edu/wiki/download/attachments/11370504/raft.pdf).

Chúng tôi không thể tìm thấy bất kỳ triển khai nào có tài liệu về giao thức dây.
Tuy nhiên, triển khai JRaft đủ đơn giản để chúng tôi có thể
kiểm tra mã và sau đó ghi lại giao thức của nó.
Đề xuất này là kết quả của nỗ lực đó.

Đây sẽ là phần backend để điều phối các router xuất bản
những mục trong Meta LeaseSet. Xem đề xuất 123.


## Mục Tiêu

- Kích thước mã nhỏ
- Dựa trên triển khai sẵn có
- Không sử dụng các đối tượng Java được tuần tự hóa hoặc bất kỳ tính năng hay mã hóa đặc trưng nào của Java
- Việc khởi động lại không nằm trong phạm vi. Ít nhất một máy chủ khác được giả định
  là được mã hóa cứng hoặc cấu hình ngoài băng tần của giao thức này.
- Hỗ trợ cả trường hợp sử dụng ngoài băng tần và trong I2P.


## Thiết Kế

Giao thức Raft không phải là một giao thức cụ thể; nó chỉ định nghĩa một máy trạng thái.
Do đó, chúng tôi ghi lại giao thức cụ thể của JRaft và dựa giao thức của chúng tôi trên đó.
Không có thay đổi nào đối với giao thức JRaft ngoài việc bổ sung
một bắt tay xác thực.

Raft bầu cử một Leader có nhiệm vụ xuất bản một nhật ký.
Nhật ký chứa dữ liệu Cấu hình Raft và dữ liệu Ứng dụng.
Dữ liệu Ứng dụng chứa trạng thái của mỗi Router của Máy chủ và Đích
cho cụm Meta LS2.
Các máy chủ sử dụng thuật toán chung để xác định nhà xuất bản và nội dung
của Meta LS2.
Nhà xuất bản của Meta LS2 không nhất thiết phải là Nhà lãnh đạo Raft.


## Đặc Tả

Giao thức dây hoạt động trên các socket SSL hoặc socket I2P không SSL.
Socket I2P được proxy thông qua HTTP Proxy.
Không có hỗ trợ cho các socket không SSL trên mạng rõ.

### Bắt Tay và Xác Thực

Không được định nghĩa bởi JRaft.

Mục tiêu:

- Phương thức xác thực người dùng/mật khẩu
- Nhận diện phiên bản
- Nhận diện cụm
- Có thể mở rộng
- Dễ dàng proxy khi sử dụng cho socket I2P
- Không phơi bày không cần thiết máy chủ là máy chủ Garlic Farm
- Giao thức đơn giản để không cần một triển khai máy chủ web hoàn chỉnh
- Tương thích với các tiêu chuẩn phổ biến, để các triển khai có thể sử dụng
  thư viện tiêu chuẩn nếu muốn

Chúng tôi sẽ sử dụng một bắt tay giống như websocket [WEBSOCKET](https://en.wikipedia.org/wiki/WebSocket) và xác thực HTTP Digest [RFC-2617](https://tools.ietf.org/html/rfc2617).
Xác thực cơ bản RFC 2617 KHÔNG được hỗ trợ.
Khi proxy thông qua HTTP proxy, giao tiếp với
proxy như được chỉ định trong [RFC-2616](https://tools.ietf.org/html/rfc2616).

#### Thông tin đăng nhập

Việc tên người dùng và mật khẩu dựa trên cụm, hoặc
dựa trên máy chủ, phụ thuộc vào triển khai.


#### Yêu Cầu HTTP 1

Người khởi tạo sẽ gửi những điều sau.

Tất cả các dòng đều được kết thúc bằng CRLF như được yêu cầu bởi HTTP.

```text
GET /GarlicFarm/CLUSTER/VERSION/websocket HTTP/1.1
  Host: (ip):(port)
  Cache-Control: no-cache
  Connection: close
  (bất kỳ tiêu đề nào khác bị bỏ qua)
  (dòng trống)

  CLUSTER là tên của cụm (mặc định là "farm")
  VERSION là phiên bản của Garlic Farm (hiện tại là "1")
```


#### Phản Hồi HTTP 1

Nếu đường dẫn không chính xác, người nhận sẽ gửi một phản hồi "HTTP/1.1 404 Not Found" tiêu chuẩn,
như trong [RFC-2616](https://tools.ietf.org/html/rfc2616).

Nếu đường dẫn là chính xác, người nhận sẽ gửi một phản hồi "HTTP/1.1 401 Unauthorized" tiêu chuẩn,
bao gồm tiêu đề xác thực HTTP digest WWW-Authenticate,
như trong [RFC-2617](https://tools.ietf.org/html/rfc2617).

Cả hai bên sau đó sẽ đóng socket.


#### Yêu Cầu HTTP 2

Người khởi tạo sẽ gửi những điều sau,
như trong [RFC-2617](https://tools.ietf.org/html/rfc2617) và [WEBSOCKET](https://en.wikipedia.org/wiki/WebSocket).

Tất cả các dòng đều được kết thúc bằng CRLF như được yêu cầu bởi HTTP.

```text
GET /GarlicFarm/CLUSTER/VERSION/websocket HTTP/1.1
  Host: (ip):(port)
  Cache-Control: no-cache
  Connection: keep-alive, Upgrade
  Upgrade: websocket
  (Sec-Websocket-* tiêu đề nếu được proxy)
  Authorization: (tiêu đề xác thực HTTP digest như trong RFC 2617)
  (bất kỳ tiêu đề nào khác bị bỏ qua)
  (dòng trống)

  CLUSTER là tên của cụm (mặc định là "farm")
  VERSION là phiên bản của Garlic Farm (hiện tại là "1")
```


#### Phản Hồi HTTP 2

Nếu xác thực không chính xác, người nhận sẽ gửi một phản hồi "HTTP/1.1 401 Unauthorized" tiêu chuẩn khác,
như trong [RFC-2617](https://tools.ietf.org/html/rfc2617).

Nếu xác thực là chính xác, người nhận sẽ gửi phản hồi sau,
như trong [WEBSOCKET](https://en.wikipedia.org/wiki/WebSocket).

Tất cả các dòng đều được kết thúc bằng CRLF như được yêu cầu bởi HTTP.

```text
HTTP/1.1 101 Switching Protocols
  Connection: Upgrade
  Upgrade: websocket
  (Sec-Websocket-* tiêu đề)
  (bất kỳ tiêu đề nào khác bị bỏ qua)
  (dòng trống)
```

Sau khi nhận được phản hồi này, socket vẫn mở.
Giao thức Raft như được định nghĩa dưới đây bắt đầu, trên cùng một socket.


#### Bộ Nhớ Đệm

Thông tin đăng nhập sẽ được lưu vào bộ nhớ đệm ít nhất một giờ, để
các kết nối tiếp theo có thể nhảy trực tiếp đến
"Yêu Cầu HTTP 2" ở trên.


### Loại Tin Nhắn

Có hai loại tin nhắn, yêu cầu và phản hồi.
Yêu cầu có thể chứa Nhật ký Đăng nhập, và có kích thước biến đổi;
phản hồi không chứa Nhật ký Đăng nhập, và có kích thước cố định.

Các loại tin nhắn 1-4 là các tin nhắn RPC tiêu chuẩn được định nghĩa bởi Raft.
Đây là giao thức Raft cốt lõi.

Các loại tin nhắn 5-15 là các tin nhắn RPC mở rộng được định nghĩa bởi
JRaft, để hỗ trợ khách hàng, thay đổi máy chủ động, và
đồng bộ hóa nhật ký hiệu quả.

Các loại tin nhắn 16-17 là các tin nhắn RFC Nén Nhật ký được định nghĩa
trong phần 7 của Raft.


| Message | Số lượng | Gửi bởi | Gửi tới | Ghi chú |
| :--- | :--- | :--- | :--- | :--- |
| RequestVoteRequest | 1 | Candidate | Follower | RPC tiêu chuẩn Raft; không được chứa nhật ký đăng nhập |
| RequestVoteResponse | 2 | Follower | Candidate | RPC tiêu chuẩn Raft |
| AppendEntriesRequest | 3 | Leader | Follower | RPC tiêu chuẩn Raft |
| AppendEntriesResponse | 4 | Follower | Leader / Client | RPC tiêu chuẩn Raft |
| ClientRequest | 5 | Client | Leader / Follower | Phản hồi là AppendEntriesResponse; phải chứa các nhật ký ứng dụng chỉ |
| AddServerRequest | 6 | Client | Leader | Phải chứa một mục duy nhất của nhật lý ClusterServer chỉ |
| AddServerResponse | 7 | Leader | Client | Leader cũng sẽ gửi một JoinClusterRequest |
| RemoveServerRequest | 8 | Follower | Leader | Phải chứa một mục duy nhất của nhật lý ClusterServer chỉ |
| RemoveServerResponse | 9 | Leader | Follower | |
| SyncLogRequest | 10 | Leader | Follower | Phải chứa một mục duy nhất của nhật lý LogPack chỉ |
| SyncLogResponse | 11 | Follower | Leader | |
| JoinClusterRequest | 12 | Leader | New Server | Lời mời tham gia; phải chứa một mục duy nhất của nhật lý Cấu hình chỉ |
| JoinClusterResponse | 13 | New Server | Leader | |
| LeaveClusterRequest | 14 | Leader | Follower | Lệnh rời khỏi |
| LeaveClusterResponse | 15 | Follower | Leader | |
| InstallSnapshotRequest | 16 | Leader | Follower | Phần 7 Raft; Phải chứa một mục duy nhất của yêu cầu đồng bộ hóa Snapshotsync chỉ |
| InstallSnapshotResponse | 17 | Follower | Leader | Phần 7 Raft |


### Thiết Lập

Sau bắt tay qua HTTP, chuỗi thiết lập như sau:

```text
Máy chủ mới Alice              Người theo Bob ngẫu nhiên

  ClientRequest   ------->
          <---------   AppendEntriesResponse

  Nếu Bob nói rằng ông ấy là nhà lãnh đạo, tiếp tục như sau.
  Nếu không, Alice phải ngắt kết nối khỏi Bob và kết nối với nhà lãnh đạo.


  Máy chủ mới Alice              Nhà lãnh đạo Charlie

  ClientRequest   ------->
          <---------   AppendEntriesResponse
  AddServerRequest   ------->
          <---------   AddServerResponse
          <---------   JoinClusterRequest
  JoinClusterResponse  ------->
          <---------   SyncLogRequest
                       HOẶC InstallSnapshotRequest
  SyncLogResponse  ------->
  HOẶC InstallSnapshotResponse
```

Chuỗi Ngắt Kết Nối:

```text
Người theo dõi Alice              Nhà lãnh đạo Charlie

  RemoveServerRequest   ------->
          <---------   RemoveServerResponse
          <---------   LeaveClusterRequest
  LeaveClusterResponse  ------->
```

Chuỗi Bầu cử:

```text
Người ứng cử Alice               Người theo dõi Bob

  RequestVoteRequest   ------->
          <---------   RequestVoteResponse

  nếu Alice thắng cử:

  Nhà lãnh đạo Alice                Người theo dõi Bob

  AppendEntriesRequest   ------->
  (nhịp tim)
          <---------   AppendEntriesResponse
```


### Định nghĩa

- Nguồn: Xác định nguồn của thông điệp
- Đích: Xác định người nhận thông điệp
- Thuật ngữ: Xem Raft. Khởi đầu từ 0, tăng dần
- Chỉ số: Xem Raft. Khởi đầu từ 0, tăng dần


### Yêu cầu

Yêu cầu chứa tiêu đề và không hoặc nhiều nhật ký đăng nhập.
Yêu cầu chứa một tiêu đề có kích thước cố định và Nhật ký Đăng nhập Tùy chọn có kích thước thay đổi.


#### Tiêu đề Yêu cầu

Tiêu đề yêu cầu là 45 byte, như sau.
Tất cả các giá trị đều là big-endian không dấu.

```dataspec
Loại tin nhắn:  1 byte
  Nguồn:          ID, số nguyên 4 byte
  Đích:           ID, số nguyên 4 byte
  Thuật ngữ:      Thuật ngữ hiện tại (xem ghi chú), số nguyên 8 byte
  Thuật ngữ nhật lý: 8 byte integer
  Chỉ số nhật lý cuối cùng:    8 byte integer
  Chỉ số cam kết:      8 byte integer
  Kích thước nhật lý:  Tổng kích thước tính bằng byte, số nguyên 4 byte
  Nhật lý:       xem bên dưới, tổng chiều dài như đã chỉ định
```


#### Ghi chú

Trong RequestVoteRequest, Thuật ngữ là thuật ngữ của ứng cử viên.
Nếu không, nó là thuật ngữ hiện tại của nhà lãnh đạo.

Trong AppendEntriesRequest, khi kích thước nhật lý là số không,
tin nhắn này là tin nhắn duy trì kết nối (keepalive).


#### Nhật ký Đăng nhập

Nhật lý chứa không hay nhiều mục nhật lý.
Mỗi mục nhật lý như sau.
Tất cả các giá trị đều là big-endian không dấu.

```dataspec
Thuật ngữ:  8 byte integer
  Loại giá trị:  1 byte
  Kích thước mục:    Tính bằng byte, số nguyên 4 byte
  Mục:          chiều dài như đã chỉ định
```


#### Nội Dung Nhật lý

Tất cả các giá trị đều là big-endian không dấu.

| Loại Giá Trị Nhật lý | Số |
| :--- | :--- |
| Ứng dụng | 1 |
| Cấu hình | 2 |
| Máy chủ Cluster | 3 |
| Gói Nhật ký | 4 |
| Yêu cầu Đồng bộ hóa Snapshot | 5 |


#### Ứng dụng

Nội dung ứng dụng được mã hóa chuỗi [JSON](https://json.org/) UTF-8.
Xem phần Lớp Ứng dụng bên dưới.


#### Cấu hình

Điều này được sử dụng để nhà lãnh đạo tuần tự hóa một cấu hình cụm mới và sao chép tới các đối tác.
Nó chứa không hoặc nhiều cấu hình Máy chủ Cluster.

```dataspec
Chỉ số Nhật ký:  8 byte integer
  Chỉ số Nhật ký Cuối cùng:  8 byte integer
  Dữ liệu Máy chủ Cluster cho mỗi máy chủ:
    ID:                số nguyên 4 byte
    Độ dài dữ liệu điểm cuối: Tính bằng byte, số nguyên 4 byte
    Dữ liệu điểm cuối: Chuỗi ASCII theo định dạng "tcp://localhost:9001", chiều dài như đã chỉ định
```


#### Máy chủ Cluster

Thông tin cấu hình cho một máy chủ trong một cụm.
Điều này chỉ được bao gồm trong một thông điệp AddServerRequest hoặc RemoveServerRequest.

Khi được sử dụng trong một Thông điệp AddServerRequest:

```dataspec
ID:                số nguyên 4 byte
  Độ dài dữ liệu điểm cuối: Tính bằng byte, số nguyên 4 byte
  Dữ liệu điểm cuối: Chuỗi ASCII theo định dạng "tcp://localhost:9001", chiều dài như đã chỉ định
```


Khi được sử dụng trong một Thông điệp RemoveServerRequest:

```dataspec
ID:                số nguyên 4 byte
```


#### Gói Nhật ký

Điều này chỉ được bao gồm trong một thông điệp SyncLogRequest.

Thông tin sau đây được nén trước khi truyền:

```dataspec
Độ dài dữ liệu chỉ số: Tính bằng byte, số nguyên 4 byte
  Độ dài dữ liệu nhật ký:   Tính bằng byte, số nguyên 4 byte
  Dữ liệu chỉ số:     8 byte cho mỗi chỉ số, chiều dài như đã chỉ định
  Dữ liệu nhật ký:       chiều dài như đã chỉ định
```


#### Yêu cầu Đồng bộ hóa Snapshot

Điều này chỉ được bao gồm trong một thông điệp InstallSnapshotRequest.

```dataspec
Chỉ số Nhật ký Cuối cùng:  8 byte integer
  Thuật ngữ Nhật ký Cuối cùng:   8 byte integer
  Độ dài dữ liệu Cấu hình: Tính bằng byte, số nguyên 4 byte
  Dữ liệu Cấu hình:     chiều dài như đã chỉ định
  Bù đắp:          Bù đắp của dữ liệu trong cơ sở dữ liệu, tính bằng byte, số nguyên 8 byte
  Độ dài Dữ liệu:        Tính bằng byte, số nguyên 4 byte
  Dữ liệu:            chiều dài như đã chỉ định
  Hoàn Tất:         1 nếu hoàn tất, 0 nếu chưa hoàn tất (1 byte)
```


### Phản hồi

Tất cả các phản hồi đều dài 26 byte, như sau.
Tất cả các giá trị đều là big-endian không dấu.

```dataspec
Loại tin nhắn:   1 byte
  Nguồn:         ID, số nguyên 4 byte
  Đích:          Thông thường là ID đích thực (xem ghi chú), số nguyên 4 byte
  Thuật ngữ:     Thuật ngữ hiện tại, số nguyên 8 byte
  Chỉ số Tiếp theo:     Khởi đầu từ chỉ số nhật ký cuối cùng của nhà lãnh đạo + 1, số nguyên 8 byte
  Được chấp nhận:    1 nếu được chấp nhận, 0 nếu không được chấp nhận (xem ghi chú), 1 byte
```


#### Ghi chú

ID Đích thông thường là đích thực sự cho tin nhắn này.
Nhưng, với AppendEntriesResponse, AddServerResponse, và RemoveServerResponse,
đó là ID của nhà lãnh đạo hiện tại.

Trong RequestVoteResponse, Được chấp nhận là 1 cho một phiếu cho ứng cử viên (người yêu cầu),
và 0 cho không phiếu.


## Lớp Ứng Dụng

Mỗi Máy chủ định kỳ đăng dữ liệu Ứng dụng vào nhật ký trong một ClientRequest.
Dữ liệu Ứng dụng chứa trạng thái của mỗi Router của Máy chủ và Đích
cho cụm Meta LS2.
Các máy chủ sử dụng một thuật toán chung để xác định nhà xuất bản và nội dung
của Meta LS2.
Máy chủ có trạng thái gần đây "tốt nhất" trong nhật ký là nhà xuất bản Meta LS2.
Nhà xuất bản của Meta LS2 không nhất thiết phải là Nhà lãnh đạo Raft.


### Nội Dung Dữ Liệu Ứng Dụng

Nội dung ứng dụng được mã hóa chuỗi [JSON](https://json.org/) UTF-8,
cho sự đơn giản và khả năng mở rộng.
Đặc tả đầy đủ chưa được xác định.
Mục tiêu là cung cấp đủ dữ liệu để viết một thuật toán để xác định router "tốt nhất"
để xuất bản Meta LS2, và cho nhà xuất bản có đủ thông tin
để đánh giá Đích trong Meta LS2.
Dữ liệu sẽ chứa cả thống kê của router và Đích.

Dữ liệu có thể tùy chọn chứa dữ liệu cảm biến từ xa về sức khỏe của
các máy chủ khác, và khả năng tải Meta LS.
Những dữ liệu này sẽ không được hỗ trợ trong lần phát hành đầu tiên.

Dữ liệu có thể tùy chọn chứa thông tin cấu hình được đăng
bởi một máy khách quản trị.
Những dữ liệu này sẽ không được hỗ trợ trong lần phát hành đầu tiên.

Nếu "tên: giá trị" được liệt kê, điều đó chỉ định khóa và giá trị của bản đồ JSON.
Nếu không, đặc tả chưa được xác định.


Dữ liệu cụm (cấp cao nhất):

- cluster: Tên cụm
- date: Ngày của dữ liệu này (đơn vị thời gian dài, ms kể từ epoch)
- id: ID Raft (số nguyên)

Dữ liệu cấu hình (config):

- Các tham số cấu hình bất kỳ

Trạng thái xuất bản MetaLS (meta):

- destination: điểm đến của metals, base64
- lastPublishedLS: nếu có mặt, mã hóa base64 của metals đã xuất bản cuối cùng
- lastPublishedTime: tính bằng ms, hoặc 0 nếu chưa từng
- publishConfig: Trạng thái cấu hình xuất bản tắt/bật/tự động
- publishing: trạng thái nhà xuất bản metals boolean true/false

Dữ liệu Router (router):

- lastPublishedRI: nếu có mặt, mã hóa base64 của thông tin router đã xuất bản cuối cùng
- uptime: Thời gian hoạt động tính bằng ms
- Công việc chậm trễ
- Đường hầm khám phá
- Đường hầm tham gia
- Băng thông đã cấu hình
- Băng thông hiện tại

Đích (destinations):
Danh sách

Dữ liệu đích:

- destination: đích, base64
- uptime: Thời gian hoạt động tính bằng ms
- Đường hầm đã cấu hình
- Đường hầm hiện tại
- Băng thông đã cấu hình
- Băng thông hiện tại
- Kết nối đã cấu hình
- Kết nối hiện tại
- Dữ liệu danh sách đen

Dữ liệu cảm nhận router từ xa:

- Phiên bản RI cuối cùng đã thấy
- Thời gian tải LS
- Dữ liệu kiểm tra kết nối
- Dữ liệu hồ sơ floodfill gần nhất
  cho các khoảng thời gian ngày hôm qua, hôm nay, và ngày mai

Dữ liệu cảm nhận đích từ xa:

- Phiên bản LS cuối cùng đã thấy
- Thời gian tải LS
- Dữ liệu kiểm tra kết nối
- Dữ liệu hồ sơ floodfill gần nhất
  cho các khoảng thời gian ngày hôm qua, hôm nay, và ngày mai

Dữ liệu cảm nhận Meta LS:

- Phiên bản cuối cùng đã thấy
- Thời gian tải
- Dữ liệu hồ sơ floodfill gần nhất
  cho các khoảng thời gian ngày hôm qua, hôm nay, và ngày mai


## Giao Diện Quản Trị

TBD, có thể là một đề xuất riêng.
Không yêu cầu cho lần phát hành đầu tiên.

Yêu cầu của một giao diện quản trị:

- Hỗ trợ cho nhiều điểm đến chính, tỷ dụ nhiều cụm ảo (trang trại)
- Cung cấp cái nhìn toàn diện về trạng thái cụm được chia sẻ - tất cả thống kê do các thành viên công bố, ai là nhà lãnh đạo hiện tại, vv.
- Khả năng buộc loại bỏ một người tham gia hoặc lãnh đạo từ cụm
- Khả năng buộc xuất bản metaLS (nếu node hiện tại là nhà xuất bản)
- Khả năng loại trừ các băm khỏi metaLS (nếu node hiện tại là nhà xuất bản)
- Chức năng nhập/xuất cấu hình cho việc triển khai hàng loạt


## Giao Diện Router

TBD, có thể là một đề xuất riêng.
i2pcontrol không yêu cầu cho lần phát hành đầu tiên và những thay đổi chi tiết sẽ bao gồm trong một đề xuất riêng.

Yêu cầu cho Garlic Farm tới API router (in-JVM java hoặc i2pcontrol)

- getLocalRouterStatus()
- getLocalLeafHash(Hash masterHash)
- getLocalLeafStatus(Hash leaf)
- getRemoteMeasuredStatus(Hash masterOrLeaf) // probably not in MVP
- publishMetaLS(Hash masterHash, List<MetaLease> contents) // or signed MetaLeaseSet? Who signs?
- stopPublishingMetaLS(Hash masterHash)
- authentication TBD?


## Lý Do

Atomix quá lớn và không cho phép tùy chỉnh cho chúng tôi để định tuyến
giao thức qua I2P. Ngoài ra, định dạng dây của nó chưa được tài liệu hóa, và phụ thuộc
vào tuần tự hóa Java.


## Ghi chú


## Vấn đề

- Không có cách nào cho một khách hàng để tìm ra và kết nối với một nhà lãnh đạo không xác định.
  Đây sẽ là một thay đổi nhỏ để một Follower gửi Cấu hình như một Nhật lý trong AppendEntriesResponse.


## Di cư

Không có vấn đề tương thích ngược.


## Tài liệu

* [JRAFT](https://github.com/datatechnology/jraft)
* [JSON](https://json.org/)
* [RAFT](https://ramcloud.stanford.edu/wiki/download/attachments/11370504/raft.pdf)
* [RFC-2616](https://tools.ietf.org/html/rfc2616)
* [RFC-2617](https://tools.ietf.org/html/rfc2617)
* [WEBSOCKET](https://en.wikipedia.org/wiki/WebSocket)
