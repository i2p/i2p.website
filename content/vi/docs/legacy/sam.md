---
title: "Đặc tả SAM V1"
description: "Giao thức Legacy Simple Anonymous Messaging phiên bản 1 (đã lỗi thời)"
slug: "sam"
aliases:
  - "/vi/docs/api/sam"
  - "/vi/docs/api/sam/"
  - "/vi/sam"
  - "/vi/sam/"
lastUpdated: "2025-03"
accurateFor: "0.9.20"
---

## Cảnh báo - Không được dùng nữa - Không được hỗ trợ - Sử dụng [SAMv3](/docs/api/samv3)

Được chỉ định bên dưới là phiên bản 1 của một giao thức client đơn giản để tương tác với I2P. Các lựa chọn thay thế mới hơn: [SAM V2](/docs/api/samv2), [SAM V3](/docs/api/samv3), [BOB](/docs/api/bob).

## Thư viện ngôn ngữ cho SAMv1 API

- C
- C#
- Perl
- Python

Các thư viện nằm trong kho mã nguồn I2P.

### Các thay đổi trong I2P 0.9.14

Phiên bản được báo cáo vẫn là "1.0".

- DEST GENERATE hiện đã hỗ trợ tham số SIGNATURE_TYPE.
- Tham số MIN trong HELLO VERSION giờ đây là tùy chọn.
- Các tham số MIN và MAX trong HELLO VERSION hiện đã hỗ trợ các phiên bản một chữ số như "3".

## Giao thức Phiên bản 1

Ứng dụng client giao tiếp với SAM bridge, SAM bridge xử lý tất cả chức năng I2P (sử dụng streaming lib cho các virtual stream, hoặc I2CP trực tiếp cho các async message).

Tất cả giao tiếp giữa client\<--\>SAM bridge đều không được mã hóa và không xác thực qua một socket TCP duy nhất. Việc truy cập vào SAM bridge cần được bảo vệ thông qua tường lửa hoặc các biện pháp khác (có thể bridge có thể có ACL để kiểm soát các IP nào được phép kết nối).

Tất cả các thông điệp SAM này được gửi trên một dòng đơn bằng ASCII thuần túy, kết thúc bằng ký tự xuống dòng (\\n). Định dạng hiển thị bên dưới chỉ để dễ đọc, và trong khi hai từ đầu tiên trong mỗi thông điệp phải giữ thứ tự cụ thể của chúng, thứ tự của các cặp key=value có thể thay đổi (ví dụ "ONE TWO A=B C=D" hoặc "ONE TWO C=D A=B" đều là cấu trúc hoàn toàn hợp lệ). Ngoài ra, giao thức này phân biệt chữ hoa chữ thường.

Các thông điệp SAM được diễn giải theo UTF-8. Các cặp Key=value phải được phân tách bằng một khoảng trắng duy nhất. Các giá trị có thể được đặt trong dấu ngoặc kép nếu chúng chứa khoảng trắng, ví dụ: key="long value text". Không có cơ chế escape.

Giao tiếp có thể có ba hình thức khác biệt:

- [Luồng ảo](/docs/api/streaming)
- [Datagram có thể phản hồi](/docs/specs/datagrams#repliable) (tin nhắn có trường FROM)
- [Datagram ẩn danh](/docs/specs/datagrams#raw) (tin nhắn ẩn danh thô)

## Bắt tay Kết nối SAM

Không có giao tiếp SAM nào có thể xảy ra cho đến khi client và bridge đã thỏa thuận về phiên bản giao thức, điều này được thực hiện bằng cách client gửi HELLO và bridge gửi HELLO REPLY:

```
HELLO VERSION MIN=$min MAX=$max
```
và

```
HELLO REPLY RESULT=$result VERSION=1.0
```
Kể từ I2P 0.9.14, tham số MIN là tùy chọn. Tham số MAX phải được cung cấp và phải lớn hơn hoặc bằng "1" và nhỏ hơn "2" để sử dụng phiên bản 1.

Giá trị RESULT có thể là một trong các giá trị sau:

- `OK`
- `NOVERSION`

## Phiên SAM

Một phiên SAM được tạo ra khi client mở một socket tới cầu nối SAM, thực hiện bắt tay, và gửi thông điệp SESSION CREATE, và phiên kết thúc khi socket bị ngắt kết nối.

Mỗi I2P Destination chỉ có thể được sử dụng cho một phiên SAM tại một thời điểm, và chỉ có thể sử dụng một trong những hình thức đó (các tin nhắn nhận được thông qua các hình thức khác sẽ bị loại bỏ).

Thông điệp SESSION CREATE được gửi bởi client đến bridge như sau:

```
SESSION CREATE
        STYLE={STREAM,DATAGRAM,RAW}
        DESTINATION={$name,TRANSIENT}
        [DIRECTION={BOTH,RECEIVE,CREATE}]
        [option=value]*
```
DESTINATION chỉ định destination nào sẽ được sử dụng để gửi và nhận tin nhắn/luồng dữ liệu. Nếu một $name được cung cấp, SAM bridge sẽ tìm kiếm trong bộ nhớ cục bộ của mình (tệp sam.keys) để tìm destination tương ứng (và khóa riêng). Nếu không có liên kết nào tồn tại khớp với tên đó, nó sẽ tạo một cái mới. Nếu destination được chỉ định là TRANSIENT, nó sẽ luôn tạo một cái mới.

Lưu ý rằng DESTINATION là một định danh, *không phải* dữ liệu được mã hóa Base 64. Để chỉ định Destination, bạn phải sử dụng [SAM V3](/docs/api/samv3).

DIRECTION chỉ có thể được chỉ định cho các phiên STREAM, hướng dẫn bridge rằng client sẽ tạo hoặc nhận các stream, hoặc cả hai. Nếu không được chỉ định, BOTH sẽ được giả định. Việc cố gắng tạo một stream đисходящий khi DIRECTION=RECEIVE sẽ dẫn đến lỗi, và các stream đến khi DIRECTION=CREATE sẽ bị bỏ qua.

Các tùy chọn bổ sung được cung cấp nên được đưa vào cấu hình I2P session nếu không được SAM bridge diễn giải (ví dụ: "tunnels.depthInbound=0"). Các tùy chọn này được tài liệu hóa bên dưới.

Cầu nối SAM tự nó đã được cấu hình với router mà nó sẽ giao tiếp qua I2P (mặc dù nếu cần thiết có thể có cách để ghi đè, ví dụ i2cp.tcp.host=localhost và i2cp.tcp.port=7654).

Sau khi nhận được thông báo tạo session, SAM bridge sẽ phản hồi bằng một thông báo trạng thái session, như sau:

```
SESSION STATUS
        RESULT=$result
        DESTINATION={$name,TRANSIENT}
        [MESSAGE=...]
```
Giá trị RESULT có thể là một trong các giá trị sau:

- `OK`
- `DUPLICATED_DEST`
- `I2P_ERROR`
- `INVALID_KEY`

Nếu không thành công, MESSAGE nên chứa thông tin có thể đọc được cho con người về lý do tại sao phiên không thể được tạo.

Lưu ý rằng không có cảnh báo nào được đưa ra nếu $name không được tìm thấy và một destination tạm thời được tạo thay thế. Lưu ý rằng destination base 64 tạm thời thực tế không được xuất ra trong phản hồi; nó là $name hoặc TRANSIENT như được cung cấp trong SESSION CREATE. Nếu bạn cần những tính năng này, bạn phải sử dụng [SAM V3](/docs/api/samv3).

## SAM Virtual Streams

Các luồng ảo được đảm bảo gửi một cách đáng tin cậy và theo thứ tự, với thông báo thất bại và thành công ngay khi có sẵn.

Sau khi thiết lập phiên với STYLE=STREAM, cả client và SAM bridge đều có thể gửi bất đồng bộ các thông điệp khác nhau qua lại để quản lý các luồng, như được liệt kê dưới đây:

```
STREAM CONNECT
       ID=$id
       DESTINATION=$destination
```
Điều này thiết lập một kết nối ảo mới từ điểm đích cục bộ đến peer được chỉ định, đánh dấu nó với ID duy nhất trong phạm vi phiên. ID duy nhất là một số nguyên ASCII cơ số 10 từ 1 đến (2^31-1).

$destination là chuỗi base 64 của [Destination](/docs/specs/common-structures#type_Destination), có 516 ký tự base 64 trở lên (387 byte trở lên ở dạng nhị phân), tùy thuộc vào loại chữ ký.

Cầu nối SAM phải trả lời với thông báo trạng thái luồng:

```
STREAM STATUS
       RESULT=$result
       ID=$id
       [MESSAGE=...]
```
Giá trị RESULT có thể là một trong các giá trị sau:

- `OK`
- `CANT_REACH_PEER`
- `I2P_ERROR`
- `INVALID_KEY`
- `TIMEOUT`

Nếu RESULT là OK, đích đã chỉ định đang hoạt động và đã cho phép kết nối; nếu kết nối không thể thực hiện được (timeout, v.v.), RESULT sẽ chứa giá trị lỗi thích hợp (kèm theo MESSAGE có thể đọc được tùy chọn).

Ở phía nhận, cầu nối SAM chỉ đơn giản thông báo cho client như sau:

```
STREAM CONNECTED
       DESTINATION=$destination
       ID=$id
```
Điều này thông báo cho client rằng destination đã cho đã tạo một kết nối ảo với họ. Luồng dữ liệu tiếp theo sẽ được đánh dấu bằng ID duy nhất đã cho, đó là một số nguyên ASCII cơ số 10 từ -1 đến -(2^31-1).

$destination là mã base 64 của [Destination](/docs/specs/common-structures#type_Destination), có 516 hoặc nhiều ký tự base 64 (387 hoặc nhiều byte ở dạng nhị phân), tùy thuộc vào loại chữ ký.

Khi client muốn gửi dữ liệu trên kết nối ảo, họ thực hiện như sau:

```
STREAM SEND
       ID=$id
       SIZE=$numBytes\n[$numBytes of data]
```
Điều này thêm dữ liệu được chỉ định vào buffer đang được gửi đến peer qua kết nối ảo. Kích thước gửi $numBytes là số byte 8bit được bao gồm sau ký tự xuống dòng, có thể từ 1 đến 32768 (32KB).

SAM bridge sau đó sẽ cố gắng hết sức để gửi thông điệp một cách nhanh chóng và hiệu quả nhất có thể, có thể sẽ đệm nhiều thông điệp SEND lại với nhau. Nếu có lỗi trong việc gửi dữ liệu, hoặc nếu phía từ xa đóng kết nối, SAM bridge sẽ thông báo cho client:

```
STREAM CLOSED
       RESULT=$result
       ID=$id
       [MESSAGE=...]
```
Giá trị RESULT có thể là một trong các giá trị sau:

- `OK`
- `CANT_REACH_PEER`
- `I2P_ERROR`
- `PEER_NOT_FOUND`
- `TIMEOUT`

Nếu kết nối đã được đóng sạch sẽ bởi peer khác, $result được đặt thành OK. Nếu $result không phải là OK, MESSAGE có thể chuyển tải một thông báo mô tả, như "peer unreachable", v.v. Bất cứ khi nào client muốn đóng kết nối, họ gửi cho SAM bridge thông điệp close:

```
STREAM CLOSE
       ID=$id
```
Bridge sau đó dọn dẹp những gì cần thiết và loại bỏ ID đó - không thể gửi hoặc nhận thêm tin nhắn nào trên nó nữa.

Đối với phía bên kia của giao tiếp, bất cứ khi nào peer đã gửi một số dữ liệu và nó có sẵn cho client, SAM bridge sẽ ngay lập tức chuyển giao nó:

```
STREAM RECEIVED
       ID=$id
       SIZE=$numBytes\n[$numBytes of data]
```
Tất cả các luồng sẽ được đóng ngầm định khi kết nối giữa SAM bridge và client bị ngắt.

## SAM Repliable Datagrams

Mặc dù I2P không chứa địa chỉ FROM một cách tự nhiên, để dễ sử dụng, một lớp bổ sung được cung cấp dưới dạng repliable datagrams - các thông điệp không có thứ tự và không đáng tin cậy lên đến 31744 byte bao gồm địa chỉ FROM (để lại tối đa 1KB cho dữ liệu header). Địa chỉ FROM này được xác thực nội bộ bởi SAMv3 (sử dụng khóa ký của destination để xác minh nguồn) và bao gồm cơ chế ngăn chặn replay.

Kích thước tối thiểu là 1. Để có độ tin cậy giao hàng tốt nhất, kích thước tối đa được khuyến nghị là khoảng 11 KB.

Sau khi thiết lập phiên SAM với STYLE=DATAGRAM, client có thể gửi đến SAM bridge:

```
DATAGRAM SEND
         DESTINATION=$destination
         SIZE=$numBytes\n[$numBytes of data]
```
Khi một datagram đến, cầu nối sẽ chuyển nó đến client thông qua:

```
DATAGRAM RECEIVED
         DESTINATION=$destination
         SIZE=$numBytes\n[$numBytes of data]
```
$destination là base 64 của [Destination](/docs/specs/common-structures#type_Destination), có 516 hoặc nhiều hơn ký tự base 64 (387 hoặc nhiều hơn byte ở dạng nhị phân), tùy thuộc vào loại chữ ký.

Cầu nối SAM không bao giờ tiết lộ cho client các header xác thực hoặc các trường khác, chỉ tiết lộ dữ liệu mà người gửi cung cấp. Điều này tiếp tục cho đến khi phiên được đóng (bởi client ngắt kết nối).

## SAM Anonymous Datagrams

Tận dụng tối đa băng thông của I2P, SAM cho phép các client gửi và nhận datagram ẩn danh, để việc xác thực và thông tin phản hồi tùy thuộc vào chính client. Các datagram này không đáng tin cậy và không có thứ tự, và có thể lên đến 32768 byte.

Kích thước tối thiểu là 1. Để đạt độ tin cậy giao hàng tốt nhất, kích thước tối đa được khuyến nghị là khoảng 11 KB.

Sau khi thiết lập phiên SAM với STYLE=RAW, client có thể gửi đến SAM bridge:

```
RAW SEND
    DESTINATION=$destination
    SIZE=$numBytes\n[$numBytes of data]
```
$destination là base 64 của [Destination](/docs/specs/common-structures#type_Destination), có 516 hoặc nhiều hơn ký tự base 64 (387 hoặc nhiều hơn byte ở dạng nhị phân), tùy thuộc vào loại chữ ký.

Khi một datagram thô đến, bridge sẽ chuyển nó đến client thông qua:

```
RAW RECEIVED
    SIZE=$numBytes\n[$numBytes of data]
```
## Chức năng Tiện ích SAM

Thông điệp sau có thể được sử dụng bởi client để truy vấn SAM bridge cho việc phân giải tên:

```
NAMING LOOKUP
       NAME=$name
```
được trả lời bởi

```
NAMING REPLY
       RESULT=$result
       NAME=$name
       [VALUE=$destination]
       [MESSAGE=$message]
```
Giá trị RESULT có thể là một trong những giá trị sau:

- `OK`
- `INVALID_KEY`
- `KEY_NOT_FOUND`

Nếu NAME=ME, thì phản hồi sẽ chứa destination được sử dụng bởi phiên hiện tại (hữu ích nếu bạn đang sử dụng một phiên TRANSIENT). Nếu $result không phải là OK, MESSAGE có thể truyền tải một thông báo mô tả, chẳng hạn như "bad format", v.v.

$destination là chuỗi base 64 của [Destination](/docs/specs/common-structures#type_Destination), có 516 hoặc nhiều hơn ký tự base 64 (387 hoặc nhiều hơn byte ở dạng nhị phân), tùy thuộc vào loại chữ ký.

Các khóa base64 công khai và riêng tư có thể được tạo bằng thông điệp sau:

```
DEST GENERATE
```
được trả lời bởi

```
DEST REPLY
     PUB=$destination
     PRIV=$privkey
```
Từ I2P 0.9.14, tham số tùy chọn SIGNATURE_TYPE được hỗ trợ. Giá trị SIGNATURE_TYPE có thể là bất kỳ tên nào (ví dụ: ECDSA_SHA256_P256, không phân biệt hoa thường) hoặc số (ví dụ: 1) được hỗ trợ bởi [Key Certificates](/docs/specs/common-structures#type_Certificate). Mặc định là DSA_SHA1.

$destination là mã base 64 của [Destination](/docs/specs/common-structures#type_Destination), có 516 ký tự base 64 trở lên (387 byte trở lên ở dạng nhị phân), tùy thuộc vào loại chữ ký.

$privkey là chuỗi base 64 của việc nối [Destination](/docs/specs/common-structures#type_Destination) theo sau bởi [Private Key](/docs/specs/common-structures#type_PrivateKey) rồi theo sau bởi [Signing Private Key](/docs/specs/common-structures#type_SigningPrivateKey), có độ dài 884 ký tự base 64 trở lên (663 byte trở lên ở dạng nhị phân), tùy thuộc vào loại chữ ký.

## Giá trị RESULT

Đây là các giá trị có thể được mang bởi trường RESULT, cùng với ý nghĩa của chúng:

| Giá trị | Ý nghĩa |
|-------|---------|
| `OK` | Thao tác hoàn thành thành công |
| `CANT_REACH_PEER` | Peer tồn tại nhưng không thể kết nối được |
| `DUPLICATED_DEST` | Destination được chỉ định đã được sử dụng |
| `I2P_ERROR` | Lỗi I2P chung (ví dụ: mất kết nối I2CP, v.v.) |
| `INVALID_KEY` | Khóa được chỉ định không hợp lệ (định dạng sai, v.v.) |
| `KEY_NOT_FOUND` | Hệ thống đặt tên không thể phân giải tên đã cho |
| `PEER_NOT_FOUND` | Không thể tìm thấy peer trên mạng |
| `TIMEOUT` | Hết thời gian chờ khi đợi sự kiện (ví dụ: phản hồi từ peer) |
## Các Tùy chọn Tunnel, I2CP và Streaming

Các tùy chọn này có thể được truyền vào dưới dạng các cặp name=value ở cuối dòng SAM SESSION CREATE.

Tất cả các phiên có thể bao gồm [các tùy chọn I2CP như độ dài tunnel](/docs/protocol/i2cp#options). Các phiên STREAM có thể bao gồm [các tùy chọn thư viện Streaming](/docs/api/streaming#options). Xem các tài liệu tham khảo đó để biết tên tùy chọn và giá trị mặc định.

## Ghi chú về Base 64

Mã hóa Base 64 phải sử dụng bảng chữ cái Base 64 chuẩn của I2P "A-Z, a-z, 0-9, -, ~".

## Triển khai Thư viện Client

Thư viện client có sẵn cho C, C++, C#, Perl, và Python. Các thư viện này nằm trong thư mục apps/sam/ trong Gói mã nguồn I2P.

## Thiết lập SAM mặc định

Cổng SAM mặc định là 7656. SAM không được bật mặc định trong I2P Router; nó phải được khởi động thủ công, hoặc được cấu hình để khởi động tự động, trên trang cấu hình clients trong bảng điều khiển router, hoặc trong tệp clients.config.
