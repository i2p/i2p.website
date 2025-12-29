---
title: "Giao thức Datagram2"
number: "163"
author: "zzz, orignal, drzed, eyedeekay"
created: "2023-01-24"
lastupdated: "2025-04-16"
status: "Closed"
thread: "http://zzz.i2p/topics/3540"
target: "0.9.66"
toc: true
---

## Trạng thái

Đã được chấp thuận tại đánh giá ngày 2025-04-15.
Các thay đổi đã được tích hợp vào đặc tả.
Đã được triển khai trong Java I2P tính đến API 0.9.66.
Kiểm tra tài liệu triển khai để biết trạng thái.


## Tổng quan

Được tách ra từ [Prop123](/proposals/123-new-netdb-entries/) như một đề xuất riêng biệt.

Chữ ký ngoại tuyến không thể được xác minh trong quá trình xử lý datagram có thể phát lại.
Cần có một cờ để chỉ ra chữ ký ngoại tuyến nhưng không có chỗ để đặt cờ.

Sẽ cần một số giao thức I2CP hoàn toàn mới và định dạng mới,
để được thêm vào đặc tả [DATAGRAMS](/docs/api/datagrams/).
Chúng ta hãy gọi nó là "Datagram2".


## Mục tiêu

- Thêm hỗ trợ cho chữ ký ngoại tuyến
- Thêm ngăn chặn phát lại
- Thêm kiểu không có chữ ký
- Thêm các trường cờ và tuỳ chọn để mở rộng


## Không phải mục tiêu

Hỗ trợ giao thức từ đầu đến cuối đối với kiểm soát tắc nghẽn, v.v.
Điều đó sẽ được xây dựng trên hoặc là một thay thế cho Datagram2, là một giao thức cấp thấp.
Sẽ không có ý nghĩa nếu thiết kế một giao thức hiệu suất cao chỉ dựa trên
Datagram2, do trường nguồn và chi phí chữ ký.
Bất kỳ giao thức nào như vậy nên thực hiện một cuộc gặp gỡ đầu tiên với Datagram2 và sau đó
chuyển sang datagram RAW.


## Động lực

Được để lại từ công việc LS2 vốn đã hoàn thành vào năm 2019.

Ứng dụng đầu tiên sử dụng Datagram2 dự kiến sẽ là
thông báo UDP bittorrent, như đã triển khai trong i2psnark và zzzot,
xem [Prop160](/proposals/160-udp-trackers/).


## Đặc tả Datagram có thể phát lại

Để tham khảo,
sau đây là đánh giá của đặc tả cho các datagram có thể phát lại,
sao chép từ [Datagrams](/docs/api/datagrams/).
Số giao thức I2CP tiêu chuẩn cho các datagram có thể phát lại là PROTO_DATAGRAM (17).

```text
+----+----+----+----+----+----+----+----+
  | from                                  |
  +                                       +
  |                                       |
  ~                                       ~
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  |                                       |
  +----+----+----+----+----+----+----+----+
  | signature                             |
  +                                       +
  |                                       |
  +                                       +
  |                                       |
  +                                       +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  | payload...
  +----+----+----+----//


  from :: một `Destination`
          chiều dài: 387+ byte
          Người khởi tạo và người ký của datagram

  signature :: một `Signature`
               Loại chữ ký phải khớp với loại khóa công khai ký của $from
               chiều dài: 40+ byte, như được ngụ ý bởi loại Chữ ký.
               Đối với loại khóa DSA_SHA1 mặc định:
                  Chữ ký DSA của băm SHA-256 của dụng liệu tải.
               Đối với các loại khóa khác:
                  Chữ ký của dụng liệu tải.
               Chữ ký có thể được xác minh bởi khóa công khai ký của $from

  payload :: Dữ liệu
              Chiều dài: 0 đến khoảng 31,5 KB (xem lưu ý)

  Tổng chiều dài: Chiều dài tải + 423+
```


## Thiết kế

- Định nghĩa giao thức mới 19 - Datagram có thể phát lại với tùy chọn.
- Định nghĩa giao thức mới 20 - Datagram có thể phát lại không có chữ ký.
- Thêm trường cờ cho chữ ký ngoại tuyến và mở rộng trong tương lai
- Di chuyển chữ ký sau tải để xử lý dễ dàng hơn
- Đặc tả chữ ký mới khác với datagram có thể phát lại hoặc truyền tải, vì vậy
  xác minh chữ ký sẽ thất bại nếu được giải thích là datagram có thể phát lại hoặc truyền tải.
  Điều này được thực hiện bằng cách di chuyển chữ ký sau tải,
  và bằng cách bao gồm băm đích trong chức năng chữ ký.
- Thêm phòng ngừa phát lại cho các datagram, như đã được thực hiện trong [Prop164](/proposals/164-streaming/) cho truyền tải.
- Thêm phần cho các tùy chọn tùy ý
- Tái sử dụng định dạng chữ ký ngoại tuyến từ [Common](/docs/specs/common-structures/) và [Streaming](/docs/specs/streaming/).
- Phần chữ ký ngoại tuyến phải trước phần tải
  và phần chữ ký có chiều dài thay đổi, vì nó chỉ định chiều dài
  của chữ ký.


## Đặc tả

### Giao thức

Số giao thức I2CP mới cho Datagram2 là 19.
Thêm nó làm PROTO_DATAGRAM2 vào [I2CP](/docs/specs/i2cp/).

Số giao thức I2CP mới cho Datagram3 là 20.
Thêm nó làm PROTO_DATAGRAM2 vào [I2CP](/docs/specs/i2cp/).


### Định dạng Datagram2

Thêm Datagram2 vào [DATAGRAMS](/docs/api/datagrams/) như sau:

```text
+----+----+----+----+----+----+----+----+
  |                                       |
  ~            from                       ~
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  flags  |     options (optional)      |
  +----+----+                             +
  ~                                       ~
  ~                                       ~
  +----+----+----+----+----+----+----+----+
  |                                       |
  ~     offline_signature (optional)      ~
  ~   expires, sigtype, pubkey, offsig    ~
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  ~            payload                    ~
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  ~            signature                  ~
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+

  from :: một `Destination`
          chiều dài: 387+ byte
          Người khởi tạo và (nếu không ký ngoại tuyến) ký của datagram

  flags :: (2 byte)
           Thứ tự bit: 15 14 ... 3 2 1 0
           Các bit 3-0: Phiên bản: 0x02 (0 0 1 0)
           Bit 4: Nếu 0, không có tùy chọn; nếu 1, ánh xạ tùy chọn được bao gồm
           Bit 5: Nếu 0, không có chữ ký ngoại tuyến; nếu 1, ký ngoại tuyến
           Các bit 15-6: không sử dụng, đặt thành 0 để tương thích với các sử dụng trong tương lai

  options :: (2+ byte nếu có)
           Nếu lá cờ chỉ ra rằng có các tùy chọn, một `Mapping`
           chứa các tùy chọn văn bản tùy ý

  offline_signature ::
               Nếu cờ chỉ ra khóa ngoại tuyến, phần chữ ký ngoại tuyến,
               như được chỉ định trong Đặc tả Cấu trúc Chung,
               với các trường dưới đây. Chiều dài: thay đổi theo loại chữ ký trực tuyến và ngoại tuyến,
               thường là 102 byte cho loại chữ ký Ed25519
               Phần này có thể và nên được tạo ngoại tuyến.

    expires :: Thời hạn hết hạn
               (4 byte, big endian, giây từ epoch, lăn qua vào năm 2106)

    sigtype :: Loại chữ ký tạm thời (2 byte, big endian)

    pubkey :: Khóa công khai ký tạm thời (chiều dài theo loại chữ ký),
              thường là 32 byte cho loại chữ ký Ed25519.

    offsig :: một `Signature`
              Chữ ký của thời hạn hết hạn, loại chữ ký tạm thời,
              và khóa công khai, bởi khóa công khai đích,
              chiều dài: 40+ byte, như được ngụ ý bởi loại chữ ký, thường
              là 64 byte cho loại chữ ký Ed25519.

  payload :: Dữ liệu
              Chiều dài: 0 đến khoảng 61 KB (xem ghi chú)

  signature :: một `Signature`
               Loại chữ ký phải khớp với loại khóa công khai ký của $from
               (nếu không có chữ ký ngoại tuyến) hoặc loại sig tạm thời
               (nếu đã ký ngoại tuyến)
               chiều dài: 40+ byte, như được ngụý bởi loại chữ ký, thường
               64 byte cho loại chữ ký Ed25519.
               Chữ ký của tải và các trường khác như được chỉ định dưới đây.
               Chữ ký được xác minh bởi khóa công khai ký của $from
               (nếu không có chữ ký ngoại tuyến) hoặc khóa công khai tạm thời
               (nếu đã ký ngoại tuyến)

```

Tổng chiều dài: tối thiểu 433 + chiều dài tải;
chiều dài điển hình cho người gửi X25519 và không có chữ ký ngoại tuyến:
457 + chiều dài tải.
Lưu ý rằng tin nhắn sẽ thường được nén với gzip ở lớp I2CP,
điều sẽ mang lại tiết kiệm đáng kể nếu bích đích từ có thể nén được.

Ghi chú: Định dạng chữ ký ngoại tuyến giống như trong đặc tả Cấu trúc Chung [Common](/docs/specs/common-structures/) và [Streaming](/docs/specs/streaming/).

### Chữ ký

Chữ ký là trên các trường sau.

- Phần trên: Băm 32 byte của bích đích (không bao gồm trong datagram)
- flags
- options (nếu có)
- offline_signature (nếu có)
- payload

Trong datagram có thể phát lại, đối với loại khóa DSA_SHA1, chữ ký là trên băm SHA-256 của tải, không phải tải thực tế; đây, chữ ký luôn là trên các trường trên (KHÔNG phải băm), bất kể loại khóa.


### Xác minh ToHash

Người nhận phải xác minh chữ ký (sử dụng băm đích của họ)
và loại bỏ datagram khi thất bại, để ngăn chặn phát lại.


### Định dạng Datagram3

Thêm Datagram3 vào [DATAGRAMS](/docs/api/datagrams/) như sau:

```text
+----+----+----+----+----+----+----+----+
  |                                       |
  ~            fromhash                   ~
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  flags  |     options (optional)      |
  +----+----+                             +
  ~                                       ~
  ~                                       ~
  +----+----+----+----+----+----+----+----+
  |                                       |
  ~            payload                    ~
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+

  fromhash :: một `Hash`
              chiều dài: 32 byte
              Người khởi tạo của datagram

  flags :: (2 byte)
           Thứ tự bit: 15 14 ... 3 2 1 0
           Các bit 3-0: Phiên bản: 0x03 (0 0 1 1)
           Bit 4: Nếu 0, không có tùy chọn; nếu 1, ánh xạ tùy chọn được bao gồm
           Các bit 15-5: không sử dụng, đặt thành 0 để tương thích với các sử dụng trong tương lai

  options :: (2+ byte nếu có)
           Nếu lá cờ chỉ ra rằng có các tùy chọn, một `Mapping`
           chứa các tùy chọn văn bản tùy ý

  payload :: Dữ liệu
              Chiều dài: 0 đến khoảng 61 KB (xem ghi chú)

```

Tổng chiều dài: tối thiểu 34 + chiều dài tải.


### SAM

Thêm STYLE=DATAGRAM2 và STYLE=DATAGRAM3 vào đặc tả SAMv3.
Cập nhật thông tin về chữ ký ngoại tuyến.


### Chi phí bổ sung

Thiết kế này thêm 2 byte chi phí bổ sung cho datagram có thể phát lại cho các cờ.
Điều này chấp nhận được.


## Phân tích Bảo mật

Việc bao gồm băm đích trong chữ ký nên có hiệu quả trong việc ngăn chặn các cuộc tấn công phát lại.

Định dạng Datagram3 thiếu chữ ký, do đó người gửi không thể được xác minh,
và các cuộc tấn công phát lại là có thể xảy ra. Mọi xác thực cần thiết phải được thực hiện ở lớp ứng dụng,
hoặc bởi router ở lớp ratchet.


## Ghi chú

- Chiều dài thực tế bị giới hạn bởi các lớp dưới của các giao thức - đặc tả thông điệp hầm [TUNMSG](/docs/specs/implementation/#notes) giới hạn các thông điệp khoảng 61.2 KB và các phương tiện truyền thông [TRANSPORT](/docs/overview/transport/) hiện tại giới hạn các thông điệp khoảng 64 KB, do đó chiều dài dữ liệu ở đây
  bị giới hạn khoảng 61 KB.
- Xem các ghi chú quan trọng về độ tin cậy của các datagram lớn [API](/docs/api/datagrams/). Để
  đạt được kết quả tốt nhất, hãy giới hạn tải khoảng 10 KB hoặc ít hơn.


## Tương thích

Không có. Các ứng dụng phải được viết lại để chuyển hướng các thông điệp Datagram2 I2CP
dựa trên giao thức và/hoặc cổng.
Các thông điệp Datagram2 bị điều hướng sai và được giải thích
như là datagram có thể phát lại hoặc các thông điệp truyền streaming sẽ thất bại dựa trên chữ ký, định dạng hoặc cả hai.


## Di chuyển

Mỗi ứng dụng UDP phải phát hiện hỗ trợ và di chuyển riêng.
Ứng dụng UDP nổi bật nhất là bittorrent.

### Bittorrent

Bittorrent DHT: Có thể cần cờ mở rộng,
ví dụ: i2p_dg2, điều phối với BiglyBT

Thông báo UDP Bittorrent [Prop160](/proposals/160-udp-trackers/): Thiết kế trong từ đầu.
Điều phối với BiglyBT, i2psnark, zzzot

### Khác

Bote: Khó có khả năng di chuyển, không được duy trì tích cực

Streamr: Không ai sử dụng nó, không có kế hoạch di chuyển

Ứng dụng SAM UDP: Không biết


## Tham khảo

* [API](/docs/api/datagrams/)
* [BT-SPEC](/docs/applications/bittorrent/)
* [Common](/docs/specs/common-structures/)
* [DATAGRAMS](/docs/api/datagrams/)
* [I2CP](/docs/specs/i2cp/)
* [Prop123](/proposals/123-new-netdb-entries/)
* [Prop160](/proposals/160-udp-trackers/)
* [Prop164](/proposals/164-streaming/)
* [Streaming](/docs/specs/streaming/)
* [TRANSPORT](/docs/overview/transport/)
* [TUNMSG](/docs/specs/implementation/#notes)
