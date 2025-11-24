---
title: "Cải tiến Giao thức Vận chuyển IPv6"
number: "158"
author: "zzz, orignal"
created: "2021-03-19"
lastupdated: "2021-04-26"
status: "Closed"
thread: "http://zzz.i2p/topics/3060"
target: "0.9.50"
---

## Lưu ý
Triển khai và thử nghiệm mạng đang tiến hành.
Có thể hiệu chỉnh nhỏ.


## Tổng quan

Đề xuất này nhằm triển khai các cải tiến cho giao thức vận chuyển SSU và NTCP2 dành cho IPv6.


## Động cơ

Khi IPv6 phát triển trên toàn thế giới và thiết lập chỉ IPv6 (đặc biệt là trên thiết bị di động) trở nên phổ biến hơn,
chúng ta cần cải thiện hỗ trợ cho IPv6 và loại bỏ các giả định rằng
tất cả các router đều có khả năng IPv4.



### Kiểm tra Khả năng Kết nối

Khi chọn đối tượng ngang hàng cho các đường hầm, hoặc chọn các đường OBEP/IBGW để định tuyến thông điệp,
điều này giúp tính toán liệu router A có thể kết nối với router B hay không.
Nói chung, điều này có nghĩa là xác định nếu A có khả năng outbound cho một loại giao thức và địa chỉ (IPv4/v6)
phù hợp với một trong những địa chỉ inbound được quảng cáo của B.

Tuy nhiên, trong nhiều trường hợp, chúng ta không biết khả năng của A và phải giả định.
Nếu A bị ẩn hoặc bị tường lửa bảo vệ, các địa chỉ không được công bố, và chúng ta không có kiến thức trực tiếp -
vì vậy chúng ta cho rằng nó có khả năng IPv4, và không có khả năng IPv6.
Giải pháp là thêm hai "cap" mới hoặc khả năng vào Thông tin Router để chỉ ra khả năng outbound cho IPv4 và IPv6.


### Người giới thiệu IPv6

Các đặc tả [SSU](/en/docs/transport/ssu/) và [SSU-SPEC](/en/docs/spec/ssu/) của chúng tôi chứa các lỗi và sự không nhất quán về việc liệu
những người giới thiệu IPv6 có được hỗ trợ cho công việc giới thiệu IPv4 hay không.
Trong mọi trường hợp, điều này chưa bao giờ được triển khai trong Java I2P hay i2pd.
Điều này cần được sửa chữa.


### Giới thiệu IPv6

Các đặc tả [SSU](/en/docs/transport/ssu/) và [SSU-SPEC](/en/docs/spec/ssu/) của chúng tôi làm rõ rằng
giới thiệu IPv6 không được hỗ trợ.
Điều này được đặt ra dưới giả định rằng IPv6 không bao giờ bị tường lửa bảo vệ.
Đây là điều không đúng, và chúng ta cần cải thiện hỗ trợ cho các router IPv6 bị tường lửa bảo vệ.


### Biểu đồ Giới thiệu

Huyền thoại: ----- là IPv4, ====== là IPv6

Chỉ IPv4 hiện tại:

```
      Alice                         Bob                  Charlie
  RelayRequest ---------------------->
       <-------------- RelayResponse    RelayIntro ----------->
       <-------------------------------------------- HolePunch
  SessionRequest -------------------------------------------->
       <-------------------------------------------- SessionCreated
  SessionConfirmed ------------------------------------------>
  Data <--------------------------------------------------> Data
```


Giới thiệu IPv4, người giới thiệu IPv6

```
Alice                         Bob                  Charlie
  RelayRequest ======================>
       <============== RelayResponse    RelayIntro ----------->
       <-------------------------------------------- HolePunch
  SessionRequest -------------------------------------------->
       <-------------------------------------------- SessionCreated
  SessionConfirmed ------------------------------------------>
  Data <--------------------------------------------------> Data
```

Giới thiệu IPv6, người giới thiệu IPv6


```
Alice                         Bob                  Charlie
  RelayRequest ======================>
       <============== RelayResponse    RelayIntro ===========>
       <============================================ HolePunch
  SessionRequest ============================================>
       <============================================ SessionCreated
  SessionConfirmed ==========================================>
  Data <==================================================> Data
```

Giới thiệu IPv6, người giới thiệu IPv4

```
Alice                         Bob                  Charlie
  RelayRequest ---------------------->
       <-------------- RelayResponse    RelayIntro ===========>
       <============================================ HolePunch
  SessionRequest ============================================>
       <============================================ SessionCreated
  SessionConfirmed ==========================================>
  Data <==================================================> Data
```


## Thiết kế

Có ba thay đổi cần được thực hiện.

- Thêm khả năng "4" và "6" vào khả năng Địa chỉ Router để chỉ ra hỗ trợ outbound cho IPv4 và IPv6
- Thêm hỗ trợ giới thiệu IPv4 qua người giới thiệu IPv6
- Thêm hỗ trợ giới thiệu IPv6 qua người giới thiệu IPv4 và IPv6



## Đặc tả

### 4/6 Caps

Điều này ban đầu được triển khai mà không có đề xuất chính thức, nhưng nó là cần thiết cho
giới thiệu IPv6, vì vậy chúng tôi bao gồm nó ở đây.
Xem thêm [CAPS](http://zzz.i2p/topics/3050).

Hai khả năng mới "4" và "6" được định nghĩa.
Những khả năng mới này sẽ được thêm vào thuộc tính "caps" trong Địa chỉ Router, không phải trong khả năng Thông tin Router.
Hiện tại chúng tôi không có thuộc tính "caps" được định nghĩa cho NTCP2.
Một địa chỉ SSU với người giới thiệu, theo định nghĩa, là ipv4 ngay bây giờ. Chúng tôi không hỗ trợ giới thiệu ipv6.
Tuy nhiên, đề xuất này tương thích với một giới thiệu IPv6. Xem bên dưới.

Ngoài ra, một router có thể hỗ trợ kết nối thông qua một mạng overlay như I2P-over-Yggdrasil,
nhưng không muốn công bố một địa chỉ, hoặc lưu trữ không có định dạng tiêu chuẩn IPv4 hoặc IPv6.
Hệ thống khả năng mới này nên đủ linh hoạt để hỗ trợ những mạng này.

Chúng tôi định nghĩa những thay đổi sau:

NTCP2: Thêm thuộc tính "caps"

SSU: Thêm hỗ trợ cho một Địa chỉ Router không có máy chủ hoặc người giới thiệu, để chỉ ra hỗ trợ outbound
cho IPv4, IPv6, hoặc cả hai.

Cả hai giao thức: Định nghĩa các giá trị caps sau:

- "4": Hỗ trợ IPv4
- "6": Hỗ trợ IPv6

Nhiều giá trị có thể được hỗ trợ trong một địa chỉ duy nhất. Xem bên dưới.
Ít nhất một trong những khả năng này là bắt buộc nếu không có giá trị "host" nào được bao gồm trong Địa chỉ Router.
Tối đa một trong những khả năng này là tùy chọn nếu một giá trị "host" được bao gồm trong Địa chỉ Router.
Các khả năng giao thức bổ sung có thể được định nghĩa trong tương lai để chỉ ra sự hỗ trợ cho mạng overlay hoặc kết nối khác.


#### Các trường hợp sử dụng và ví dụ

SSU:

SSU với máy chủ: 4/6 tùy chọn, không bao giờ nhiều hơn một.
Ví dụ: SSU caps="4" host="1.2.3.4" key=... port="1234"

SSU chỉ outbound cho một, cái khác được công bố: Chỉ có Caps, 4/6.
Ví dụ: SSU caps="6"

SSU với người giới thiệu: không bao giờ kết hợp. 4 hoặc 6 là bắt buộc.
Ví dụ: SSU caps="4" iexp0=... ihost0=... iport0=... itag0=... key=...

SSU ẩn: Chỉ có Caps, 4, 6, hoặc 46. Nhiều là cho phép.
Không cần có hai địa chỉ một với 4 và một với 6.
Ví dụ: SSU caps="46"

NTCP2:

NTCP2 với máy chủ: 4/6 tùy chọn, không bao giờ nhiều hơn một.
Ví dụ: NTCP2 caps="4" host="1.2.3.4" i=... port="1234" s=... v="2"

NTCP2 chỉ outbound cho một, cái khác được công bố: Chỉ có Caps, s, v, 4/6/y, nhiều là cho phép.
Ví dụ: NTCP2 caps="6" i=... s=... v="2"

NTCP2 ẩn: Chỉ có Caps, s, v, 4/6, nhiều là cho phép. Không cần có hai địa chỉ một với 4 và một với 6.
Ví dụ: NTCP2 caps="46" i=... s=... v="2"



### Người giới thiệu IPv6 cho IPv4

Các thay đổi sau là cần thiết để điều chỉnh các lỗi và sự không nhất quán trong các đặc tả.
Chúng tôi cũng mô tả điều này như "phần 1" của đề xuất.

#### Thay đổi đặc tả

[SSU](/en/docs/transport/ssu/) hiện tại nói (ghi chú IPv6):

IPv6 được hỗ trợ kể từ phiên bản 0.9.8. Địa chỉ relay công bố có thể là IPv4 hoặc IPv6, và giao tiếp Alice-Bob có thể qua IPv4 hoặc IPv6.

Thêm vào điều sau:

Mặc dù đặc tả đã thay đổi từ phiên bản 0.9.8, giao tiếp Alice-Bob qua IPv6 thực tế không được hỗ trợ đến phiên bản 0.9.50.
Các phiên bản Java router cũ hơn công bố sai lầm khả năng 'C' cho địa chỉ IPv6,
mặc dù chúng không thực sự hoạt động như một người giới thiệu qua IPv6.
Do đó, các router chỉ nên tin tưởng khả năng 'C' trên một địa chỉ IPv6 nếu phiên bản router là 0.9.50 hoặc cao hơn.



[SSU-SPEC](/en/docs/spec/ssu/) hiện tại nói (Relay Request):

Địa chỉ IP chỉ được bao gồm nếu nó khác với địa chỉ nguồn của gói tin và cổng.
Trong triển khai hiện tại, độ dài IP luôn là 0 và cổng luôn là 0,
và người nhận nên sử dụng địa chỉ và cổng nguồn của gói tin.
Thông điệp này có thể được gửi qua IPv4 hoặc IPv6. Nếu là IPv6, Alice phải bao gồm địa chỉ và cổng IPv4 của cô.

Thêm vào điều sau:

IP và cổng phải được bao gồm để giới thiệu một địa chỉ IPv4 khi gửi thông điệp này qua IPv6.
Điều này được hỗ trợ kể từ phiên bản 0.9.50.



### Giới thiệu IPv6

Tất cả ba thông điệp relay SSU (RelayRequest, RelayResponse, và RelayIntro) chứa các trường độ dài IP
để chỉ ra độ dài của địa chỉ IP (Alice, Bob, hoặc Charlie) theo sau.

Do đó, không có thay đổi nào cần thiết cho định dạng thông điệp.
Chỉ cần thay đổi văn bản trong các đặc tả, chỉ ra rằng các địa chỉ IP 16 byte được cho phép.

Các thay đổi sau là cần thiết cho các đặc tả.
Chúng tôi cũng mô tả điều này như "phần 2" của đề xuất.


#### Thay đổi đặc tả

[SSU](/en/docs/transport/ssu/) hiện tại nói (ghi chú IPv6):

Giao tiếp Bob-Charlie và Alice-Charlie chỉ qua IPv4.

[SSU-SPEC](/en/docs/spec/ssu/) hiện tại nói (Relay Request):

Không có kế hoạch triển khai relay cho IPv6.

Thay đổi để nói:

Relay cho IPv6 được hỗ trợ kể từ phiên bản 0.9.xx

[SSU-SPEC](/en/docs/spec/ssu/) hiện tại nói (Relay Response):

Địa chỉ IP của Charlie phải là IPv4, vì đó là địa chỉ mà Alice sẽ gửi Yêu cầu Phiên tới sau khi thực hiện Hole Punch.
Không có kế hoạch triển khai relay cho IPv6.

Thay đổi để nói:

Địa chỉ IP của Charlie có thể là IPv4 hoặc, kể từ phiên bản 0.9.xx, IPv6.
Đó là địa chỉ mà Alice sẽ gửi Yêu cầu Phiên tới sau khi thực hiện Hole Punch.
Relay cho IPv6 được hỗ trợ kể từ phiên bản 0.9.xx

[SSU-SPEC](/en/docs/spec/ssu/) hiện tại nói (Relay Intro):

Địa chỉ IP của Alice luôn là 4 byte trong triển khai hiện tại, bởi vì Alice đang cố gắng kết nối tới Charlie qua IPv4.
Thông điệp này phải được gửi qua một kết nối IPv4 đã được thiết lập,
bởi vì đó là cách duy nhất mà Bob biết địa chỉ IPv4 của Charlie để trả về Alice trong RelayResponse.

Thay đổi để nói:

Đối với IPv4, địa chỉ IP của Alice luôn là 4 byte, bởi vì Alice đang cố gắng kết nối tới Charlie qua IPv4.
Kể từ phiên bản 0.9.xx, IPv6 được hỗ trợ, và địa chỉ IP của Alice có thể là 16 byte.

Đối với IPv4, thông điệp này phải được gửi qua một kết nối IPv4 đã được thiết lập,
bởi vì đó là cách duy nhất mà Bob biết địa chỉ IPv4 của Charlie để trả về Alice trong RelayResponse.
Kể từ phiên bản 0.9.xx, IPv6 được hỗ trợ, và thông điệp này có thể được gửi qua một kết nối IPv6 đã được thiết lập.

Cũng thêm:

Kể từ phiên bản 0.9.xx, bất kỳ địa chỉ SSU nào được công bố với người giới thiệu phải chứa "4" hoặc "6" trong tùy chọn "caps".


## Chuyển đổi

Tất cả các router cũ nên bỏ qua thuộc tính caps trong NTCP2, và các ký tự khả năng không xác định trong thuộc tính caps của SSU.

Bất kỳ địa chỉ SSU nào có người giới thiệu mà không chứa khả năng "4" hoặc "6" được giả định là cho việc giới thiệu IPv4.
