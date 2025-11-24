---
title: "Điều hướng đa điểm ẩn"
number: "140"
author: "str4d"
created: "2017-05-22"
lastupdated: "2017-07-04"
status: "Open"
thread: "http://zzz.i2p/topics/2335"
---

## Tổng quan

Đề xuất này phác thảo một thiết kế cho một giao thức cho phép khách hàng I2P, dịch vụ
hoặc quy trình cân bằng bên ngoài để quản lý nhiều bộ định tuyến lưu trữ một
[Destination] duy nhất một cách minh bạch.

Hiện tại đề xuất không chỉ rõ một hiện thực cụ thể. Nó có thể được hiện thực hóa như một phần mở rộng của [I2CP](/en/docs/specs/i2cp/), hoặc như một giao thức mới.


## Động cơ

Điều hướng đa điểm là nơi mà nhiều bộ định tuyến được sử dụng để lưu trữ cùng một Destination.
Cách hiện tại để điều hướng đa điểm với I2P là chạy cùng Destination trên mỗi
bộ định tuyến độc lập; bộ định tuyến mà khách hàng sử dụng vào bất kỳ thời điểm nào là bộ định tuyến cuối cùng công bố một [LeaseSet](http://localhost:63465/en/docs/specs/common-structures/#leaseset).

Đây là một cách tạm thời và có lẽ sẽ không hiệu quả cho những trang web lớn có quy mô. Giả sử chúng ta có 100 bộ định tuyến đa điểm, mỗi bộ với 16 đường hầm. Đó là 1600 lần công bố LeaseSet mỗi 10 phút, hoặc gần 3 lần mỗi giây. Các floodfill sẽ bị quá tải và việc giới hạn sẽ bắt đầu. Và đó là trước khi chúng ta thậm chí đề cập đến lưu lượng trông.

[Proposal 123](/en/proposals/123-new-netdb-entries/) giải quyết vấn đề này với một meta-LeaseSet, liệt kê 100 băm LeaseSet thật. Một lượt trông trở thành một quá trình hai giai đoạn: đầu tiên trông tìm meta-LeaseSet, và sau đó là một trong các LeaseSet được đặt tên. Đây là một giải pháp tốt cho vấn đề lưu lượng trông, nhưng nó tạo ra một rò rỉ quyền riêng tư đáng kể: Có thể xác định những bộ định tuyến đa điểm nào đang trực tuyến bằng cách theo dõi meta-LeaseSet đã công bố, vì mỗi LeaseSet thật có tương ứng với một bộ định tuyến duy nhất.

Chúng ta cần một cách để một khách hàng hoặc dịch vụ I2P phân phối một Destination duy nhất trên nhiều bộ định tuyến, theo cách không thể phân biệt với việc sử dụng một bộ định tuyến duy nhất (từ góc nhìn của LeaseSet).

## Thiết kế

### Định nghĩa

    Người dùng
        Người hoặc tổ chức muốn điều hướng đa điểm các Destination của họ. Một
        Destination duy nhất được cân nhắc ở đây mà không mất tính tổng quát.

    Khách hàng
        Ứng dụng hoặc dịch vụ chạy phía sau Destination. Nó có thể là một
        ứng dụng phía khách, phía máy chủ, hoặc ngang hàng; chúng ta gọi nó là
        một khách hàng theo nghĩa nó kết nối với các bộ định tuyến I2P.

        Khách hàng bao gồm ba phần, có thể tất cả nằm trong cùng một quy trình
        hoặc có thể được chia ra trên các quy trình hoặc máy (trong thiết lập đa khách hàng):

        Cân bằng
            Phần của khách hàng quản lý lựa chọn ngang hàng và xây dựng đường hầm.
            Có một cân bằng duy nhất tại bất kỳ thời điểm nào, và nó giao tiếp
            với tất cả các bộ định tuyến I2P. Có thể có các cân bằng lí do phụ.

        Giao diện
            Phần của khách hàng có thể được vận hành song song. Mỗi
            giao diện giao tiếp với một bộ định tuyến I2P duy nhất.

        Backend
            Phần của khách hàng được chia sẻ giữa tất cả các giao diện. Nó không có
            giao tiếp trực tiếp với bất kỳ bộ định tuyến I2P nào.

    Bộ định tuyến
        Một bộ định tuyến I2P được người dùng chạy, nằm ở ranh giới giữa mạng I2P
        và mạng của người dùng (giống như một thiết bị biên trong mạng công ty). Nó xây dựng
        các đường hầm dưới sự chỉ huy của một cân bằng, và định tuyến
        các gói cho một khách hàng hoặc giao diện.

### Tổng quan cấp cao

Hãy tưởng tượng cấu hình mong muốn sau:

- Một ứng dụng khách hàng với một Destination.
- Bốn bộ định tuyến, mỗi bộ quản lý ba đường hầm vào.
- Tất cả mười hai đường hầm nên được công bố trong một LeaseSet duy nhất.

Khách hàng đơn

```
                -{ [Đường hầm 1]===\
                 |-{ [Đường hầm 2]====[Bộ định tuyến 1]-----
                 |-{ [Đường hầm 3]===/               \
                 |                                 \
                 |-{ [Đường hầm 4]===\                 \
  [Destination]  |-{ [Đường hầm 5]====[Bộ định tuyến 2]-----   \
    \            |-{ [Đường hầm 6]===/               \   \
     [LeaseSet]--|                               [Khách hàng]
                 |-{ [Đường hầm 7]===\               /   /
                 |-{ [Đường hầm 8]====[Bộ định tuyến 3]-----   /
                 |-{ [Đường hầm 9]===/                 /
                 |                                 /
                 |-{ [Đường hầm 10]==\               /
                 |-{ [Đường hầm 11]===[Bộ định tuyến 4]-----
                  -{ [Đường hầm 12]==/

Khách hàng đa

```
                -{ [Đường hầm 1]===\
                 |-{ [Đường hầm 2]====[Bộ định tuyến 1]---------[Giao diện 1]
                 |-{ [Đường hầm 3]===/          \                    \
                 |                            \                    \
                 |-{ [Đường hầm 4]===\            \                    \
  [Destination]  |-{ [Đường hầm 5]====[Bộ định tuyến 2]---\-----[Giao diện 2]   \
    \            |-{ [Đường hầm 6]===/          \   \                \   \
     [LeaseSet]--|                         [Cân bằng]            [Backend]
                 |-{ [Đường hầm 7]===\          /   /                /   /
                 |-{ [Đường hầm 8]====[Bộ định tuyến 3]---/-----[Giao diện 3]   /
                 |-{ [Đường hầm 9]===/            /                    /
                 |                            /                    /
                 |-{ [Đường hầm 10]==\          /                    /
                 |-{ [Đường hầm 11]===[Bộ định tuyến 4]---------[Giao diện 4]
                  -{ [Đường hầm 12]==/

### Quy trình khách hàng tổng quát
- Tải hoặc tạo một Destination.

- Mở một phiên với mỗi bộ định tuyến, gắn với Destination.

- Định kỳ (khoảng mỗi mười phút, nhưng nhiều hơn hoặc ít hơn dựa trên
  độ sống đường hầm):

  - Lấy danh sách nhanh từ mỗi bộ định tuyến.

  - Sử dụng danh sách đồng bào để xây dựng các đường hầm đến/từ mỗi bộ định tuyến.

    - Theo mặc định, các đường hầm đến/từ một bộ định tuyến cụ thể sẽ sử dụng
      các đồng bào từ danh sách nhanh của bộ định tuyến đó, nhưng điều này không bị
      buộc phải tuân theo giao thức.

  - Thu thập các đường hầm vào đang hoạt động từ tất cả các bộ định tuyến đang hoạt động, và tạo một
    LeaseSet.

  - Công bố LeaseSet thông qua một hoặc nhiều bộ định tuyến.

### Sự khác biệt với I2CP
Để tạo và quản lý cấu hình này, khách hàng cần các chức năng mới sau đây so với những gì hiện tại do [I2CP](/en/docs/specs/i2cp/) cung cấp:

- Bảo bộ định tuyến xây dựng đường hầm, mà không tạo LeaseSet cho chúng.
- Lấy danh sách các đường hầm hiện tại trong bể đường hầm vào.

Ngoài ra, các chức năng sau đây sẽ cho phép sự linh hoạt đáng kể trong việc khách hàng quản lý các đường hầm của mình:

- Lấy nội dung của danh sách nhanh của bộ định tuyến.
- Bảo bộ định tuyến xây dựng một đường hầm vào hoặc ra bằng cách sử dụng danh sách đồng bào được cung cấp.

### Phác thảo giao thức

```
         Khách hàng                           Bộ định tuyến

                    --------------------->  Tạo phiên
   Trạng thái phiên  <---------------------
                    --------------------->  Lấy danh sách nhanh
      Danh sách đồng bào  <---------------------
                    --------------------->  Tạo đường hầm
    Trạng thái đường hầm  <---------------------
                    --------------------->  Lấy bể đường hầm
      Danh sách đường hầm  <---------------------
                    --------------------->  Công bố LeaseSet
                    --------------------->  Gửi gói
      Trạng thái gửi  <---------------------
  Gói nhận được  <---------------------

### Thông điệp
    Tạo phiên
        Tạo một phiên cho Destination được chỉ định.

    Trạng thái phiên
        Xác nhận rằng phiên đã được thiết lập, và khách hàng có thể bắt đầu
        xây dựng đường hầm.

    Lấy danh sách nhanh
        Yêu cầu danh sách các đồng bào mà bộ định tuyến hiện đang cân nhắc
        xây dựng đường hầm qua.

    Danh sách đồng bào
        Một danh sách các đồng bào được bộ định tuyến biết đến.

    Tạo đường hầm
        Yêu cầu bộ định tuyến xây dựng một đường hầm mới qua các đồng bào được chỉ định.

    Trạng thái đường hầm
        Kết quả của một xây dựng đường hầm cụ thể, khi nó đã sẵn sàng.

    Lấy bể đường hầm
        Yêu cầu danh sách các đường hầm hiện tại trong bể đường hầm vào hoặc ra
        cho Destination.

    Danh sách đường hầm
        Một danh sách đường hầm cho bể được yêu cầu.

    Công bố LeaseSet
        Yêu cầu bộ định tuyến công bố LeaseSet được cung cấp qua một trong các
        đường hầm ra cho Destination. Không cần phản hồi trạng thái; bộ định tuyến
        nên tiếp tục thử lại cho đến khi nó hài lòng rằng LeaseSet đã được công bố.

    Gửi gói
        Một gói đi từ khách hàng. Tùy chọn chỉ định một đường hầm ra qua đó
        gói phải (nên?) được gửi.

    Trạng thái gửi
        Thông báo cho khách hàng về sự thành công hoặc thất bại của việc gửi gói.

    Gói nhận được
        Một gói đến cho khách hàng. Tùy chọn chỉ định đường hầm vào qua đó
        gói được nhận (?)


## Các vấn đề bảo mật

Từ góc độ của các bộ định tuyến, thiết kế này tương đương với
trạng thái hiện tại. Bộ định tuyến vẫn xây dựng tất cả các đường hầm, duy trì
các hồ sơ ngang hàng riêng của nó, và thực thi sự tách biệt giữa hoạt động của bộ định tuyến và khách hàng. Trong cấu hình mặc định hoàn toàn giống hệt, vì các đường hầm cho bộ định tuyến đó được xây dựng từ danh sách nhanh của nó.

Từ góc độ của netDB, một LeaseSet duy nhất được tạo thông qua giao thức này
giống hệt với trạng thái hiện tại, vì nó tận dụng chức năng đã có sẵn.
Tuy nhiên, đối với LeaseSet lớn hơn tiếp cận tới 16 Lease, có thể đối với một
quan sát viên xác định rằng LeaseSet là nhiều điểm điều hướng:

- Kích thước tối đa hiện tại của danh sách nhanh là 75 đồng bào. Cổng vào Inbound
  (IBGW, nút được công bố trong một Lease) được chọn từ một phần của danh sách
  (phân vùng ngẫu nhiên theo bể đường hầm bằng băm, không phải số):

      1 hop
          Toàn bộ danh sách nhanh

      2 hops
          Một nửa của danh sách nhanh
          (mặc định cho đến giữa năm 2014)

      3+ hops
          Một phần tư của danh sách nhanh
          (3 là mặc định hiện tại)

  Có nghĩa là trung bình các IBGW sẽ từ một tập hợp của 20-30 đồng bào.

- Trong một thiết lập đơn điểm, một LeaseSet 16 đường hầm đầy đủ sẽ có 16 IBGW
  được chọn ngẫu nhiên từ một tập hợp lên đến (nói) 20 đồng bào.

- Trong một thiết lập đa điểm với 4 bộ định tuyến sử dụng cấu hình mặc định, một
  LeaseSet 16 đường hầm đầy đủ sẽ có 16 IBGW được chọn ngẫu nhiên từ một
  tập hợp tối đa 80 đồng bào, mặc dù có khả năng có một phần đồng bào chung
  giữa các bộ định tuyến.

Với cấu hình mặc định, có thể thông qua phân tích thống kê
để nhận ra rằng LeaseSet đang được tạo bằng giao thức này.
Nó cũng có thể tìm ra có bao nhiêu bộ định tuyến, mặc dù
hiện tượng xoay vòng trên danh sách nhanh sẽ giảm hiệu quả của phân tích này.

Vì khách hàng có toàn quyền kiểm soát đối với việc chọn lựa đồng bào của nó, rò rỉ thông tin này có thể
được giảm hoặc loại bỏ bằng cách chọn các IBGW từ một danh sách đồng bào đã giảm.

## Tương thích

Thiết kế này hoàn toàn tương thích ngược với mạng, vì không
có thay đổi nào đối với định dạng [LeaseSet](http://localhost:63465/en/docs/specs/common-structures/#leaseset). Tất cả các bộ định tuyến sẽ cần nhận thức được
giao thức mới, nhưng điều này không phải là một mối lo ngại vì tất cả bọn chúng sẽ được
kiểm soát bởi cùng một thực thể.

## Ghi chú về hiệu suất và khả năng mở rộng

Giới hạn trên của 16 [Lease](http://localhost:63465/en/docs/specs/common-structures/#lease) mỗi LeaseSet không bị thay đổi bởi đề xuất này.
Đối với các Destination yêu cầu nhiều đường hầm hơn, có hai sửa đổi khả thi
đối với mạng:

- Tăng giới hạn trên kích thước của LeaseSets. Đây sẽ là đơn giản nhất
  để thực hiện (mặc dù vẫn yêu cầu hỗ trợ mạng rộng trước khi
  nó có thể được sử dụng rộng rãi), nhưng có thể dẫn đến trông tìm chậm hơn
  do kích thước gói lớn hơn. Kích thước tối đa khả thi của LeaseSet được xác định
  bởi MTU của các phương tiện vận chuyển bên dưới, và vì vậy vào khoảng 16kB.

- Hiện thực hóa [Proposal 123](/en/proposals/123-new-netdb-entries/) cho LeaseSets có từng cấp. Kết hợp với đề xuất này,
  các Destination cho các sub-LeaseSets có thể được phân phối trên nhiều bộ định tuyến,
  thực tế hoạt động như nhiều địa chỉ IP cho một dịch vụ trên mạng sạch.

## Sự công nhận

Cảm ơn psi vì cuộc thảo luận dẫn đến đề xuất này.
