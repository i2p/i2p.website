---
title: "Multihoming Vô Hình"
number: "140"
author: "str4d"
created: "2017-05-22"
lastupdated: "2017-07-04"
status: "Mở"
thread: "http://zzz.i2p/topics/2335"
toc: true
---

## Tổng quan

Đề xuất này phác thảo một thiết kế cho giao thức cho phép một I2P client, dịch vụ hoặc tiến trình cân bằng tải bên ngoài quản lý nhiều router một cách minh bạch khi lưu trữ một [Destination](http://localhost:63465/docs/specs/common-structures/#destination) duy nhất.

Đề xuất hiện tại không chỉ định một cách triển khai cụ thể. Nó có thể được triển khai như một phần mở rộng của [I2CP](/docs/specs/i2cp/), hoặc như một giao thức mới.

## Động lực

Multihoming là việc sử dụng nhiều router để host cùng một Destination. Cách hiện tại để multihome với I2P là chạy cùng một Destination trên mỗi router một cách độc lập; router được sử dụng bởi các client tại bất kỳ thời điểm cụ thể nào là router cuối cùng publish một LeaseSet.

Đây là một giải pháp tạm bợ và có thể sẽ không hoạt động với các trang web lớn ở quy mô rộng. Giả sử chúng ta có 100 router đa kết nối, mỗi router có 16 tunnel. Đó là 1600 lần phát hành LeaseSet mỗi 10 phút, hay gần 3 lần mỗi giây. Các floodfill sẽ bị quprzeciążone và các cơ chế điều tiết sẽ kích hoạt. Và điều đó chưa kể đến lưu lượng tra cứu.

Đề xuất 123 giải quyết vấn đề này bằng một meta-LeaseSet, liệt kê 100 hash LeaseSet thực. Một lần tra cứu trở thành quá trình hai giai đoạn: đầu tiên tra cứu meta-LeaseSet, sau đó tra cứu một trong các LeaseSet được chỉ định. Đây là một giải pháp tốt cho vấn đề lưu lượng tra cứu, nhưng bản thân nó tạo ra một lỗ hổng quyền riêng tư đáng kể: Có thể xác định router multihoming nào đang trực tuyến bằng cách theo dõi meta-LeaseSet được công bố, vì mỗi LeaseSet thực tương ứng với một router duy nhất.

Chúng ta cần một cách để một I2P client hoặc dịch vụ có thể phân tán một Destination duy nhất trên nhiều router, theo cách không thể phân biệt được với việc sử dụng một router duy nhất (từ góc độ của chính LeaseSet đó).

## Thiết kế

### Definitions

    User
        The person or organisation wanting to multihome their Destination(s). A
        single Destination is considered here without loss of generality (WLOG).

    Client
        The application or service running behind the Destination. It may be a
        client-side, server-side, or peer-to-peer application; we refer to it as
        a client in the sense that it connects to the I2P routers.

        The client consists of three parts, which may all be in the same process
        or may be split across processes or machines (in a multi-client setup):

        Balancer
            The part of the client that manages peer selection and tunnel
            building. There is a single balancer at any one time, and it
            communicates with all I2P routers. There may be failover balancers.

        Frontend
            The part of the client that can be operated in parallel. Each
            frontend communicates with a single I2P router.

        Backend
            The part of the client that is shared between all frontends. It has
            no direct communication with any I2P router.

    Router
        An I2P router run by the user that sits at the boundary between the I2P
        network and the user's network (akin to an edge device in corporate
        networks). It builds tunnels under the command of a balancer, and routes
        packets for a client or frontend.

### High-level overview

Hãy tưởng tượng cấu hình mong muốn sau đây:

- Một ứng dụng client với một Destination.
- Bốn router, mỗi router quản lý ba tunnel đến.
- Tất cả mười hai tunnel nên được công bố trong một LeaseSet duy nhất.

### Single-client

```
                -{ [Tunnel 1]===\
                 |-{ [Tunnel 2]====[Router 1]-----
                 |-{ [Tunnel 3]===/               \
                 |                                 \
                 |-{ [Tunnel 4]===\                 \
  [Destination]  |-{ [Tunnel 5]====[Router 2]-----   \
    \            |-{ [Tunnel 6]===/               \   \
     [LeaseSet]--|                               [Client]
                 |-{ [Tunnel 7]===\               /   /
                 |-{ [Tunnel 8]====[Router 3]-----   /
                 |-{ [Tunnel 9]===/                 /
                 |                                 /
                 |-{ [Tunnel 10]==\               /
                 |-{ [Tunnel 11]===[Router 4]-----
                  -{ [Tunnel 12]==/
```
### Định nghĩa

```
                -{ [Tunnel 1]===\
                 |-{ [Tunnel 2]====[Router 1]---------[Frontend 1]
                 |-{ [Tunnel 3]===/          \                    \
                 |                            \                    \
                 |-{ [Tunnel 4]===\            \                    \
  [Destination]  |-{ [Tunnel 5]====[Router 2]---\-----[Frontend 2]   \
    \            |-{ [Tunnel 6]===/          \   \                \   \
     [LeaseSet]--|                         [Balancer]            [Backend]
                 |-{ [Tunnel 7]===\          /   /                /   /
                 |-{ [Tunnel 8]====[Router 3]---/-----[Frontend 3]   /
                 |-{ [Tunnel 9]===/            /                    /
                 |                            /                    /
                 |-{ [Tunnel 10]==\          /                    /
                 |-{ [Tunnel 11]===[Router 4]---------[Frontend 4]
                  -{ [Tunnel 12]==/
```
### Tổng quan cấp cao

- Tải hoặc tạo một Destination.

- Mở một phiên làm việc với mỗi router, được liên kết với Destination.

- Định kỳ (khoảng mười phút một lần, nhưng có thể nhiều hơn hoặc ít hơn tùy thuộc vào tình trạng hoạt động của tunnel):

- Lấy fast tier từ mỗi router.

- Sử dụng tập hợp siêu cấp của các peer để xây dựng tunnel tới/từ mỗi router.

    - By default, tunnels to/from a particular router will use peers from
      that router's fast tier, but this is not enforced by the protocol.

- Thu thập tập hợp các tunnel đến hoạt động từ tất cả các router đang hoạt động, và tạo một LeaseSet.

- Xuất bản LeaseSet thông qua một hoặc nhiều router.

### Client đơn

Để tạo và quản lý cấu hình này, client cần các chức năng mới sau đây ngoài những gì hiện được cung cấp bởi [I2CP](/docs/specs/i2cp/):

- Yêu cầu router xây dựng tunnel mà không tạo LeaseSet cho chúng.
- Lấy danh sách các tunnel hiện tại trong inbound pool.

Ngoài ra, các chức năng sau đây sẽ cho phép sự linh hoạt đáng kể trong cách client quản lý các tunnel của mình:

- Lấy nội dung của fast tier của một router.
- Yêu cầu một router xây dựng tunnel inbound hoặc outbound bằng cách sử dụng một danh sách
  peer đã cho.

### Đa khách hàng

```
         Client                           Router

                    --------------------->  Create Session
   Session Status  <---------------------
                    --------------------->  Get Fast Tier
        Peer List  <---------------------
                    --------------------->  Create Tunnel
    Tunnel Status  <---------------------
                    --------------------->  Get Tunnel Pool
      Tunnel List  <---------------------
                    --------------------->  Publish LeaseSet
                    --------------------->  Send Packet
      Send Status  <---------------------
  Packet Received  <---------------------
```
### Quy trình client tổng quát

**Tạo Session** - Tạo một session cho Destination đã cho.

**Trạng thái phiên** - Xác nhận rằng phiên đã được thiết lập và client hiện có thể bắt đầu xây dựng tunnel.

**Get Fast Tier** - Yêu cầu danh sách các peer mà router hiện tại sẽ xem xét để xây dựng tunnel qua.

**Danh sách Peer** - Danh sách các peer được router biết đến.

**Tạo Tunnel** - Yêu cầu router xây dựng một tunnel mới thông qua các peer được chỉ định.

**Trạng thái Tunnel** - Kết quả của một quá trình xây dựng tunnel cụ thể, khi nó có sẵn.

**Get Tunnel Pool** - Yêu cầu danh sách các tunnel hiện tại trong pool đến (inbound) hoặc đi (outbound) cho Destination.

**Danh sách Tunnel** - Danh sách các tunnel cho pool được yêu cầu.

**Publish LeaseSet** - Yêu cầu router xuất bản LeaseSet được cung cấp thông qua một trong các tunnel đi ra cho Destination. Không cần trạng thái phản hồi; router nên tiếp tục thử lại cho đến khi nó hài lòng rằng LeaseSet đã được xuất bản.

**Send Packet** - Một gói tin đi ra từ client. Tùy chọn chỉ định một outbound tunnel mà qua đó gói tin phải (nên?) được gửi.

**Send Status** - Thông báo cho client về việc gửi gói tin thành công hay thất bại.

**Gói Tin Nhận Được** - Một gói tin đến cho client. Tùy chọn chỉ định tunnel đến qua đó gói tin đã được nhận(?)

## Security implications

Từ góc độ của các router, thiết kế này về mặt chức năng tương đương với hiện trạng. Router vẫn xây dựng tất cả các tunnel, duy trì hồ sơ peer của riêng mình, và thực thi sự tách biệt giữa các hoạt động của router và client. Trong cấu hình mặc định hoàn toàn giống hệt nhau, bởi vì các tunnel cho router đó được xây dựng từ tầng nhanh của chính nó.

Từ góc độ của netDB, một leaseSet duy nhất được tạo thông qua giao thức này là giống hệt với hiện trạng, bởi vì nó tận dụng các chức năng đã tồn tại trước đó. Tuy nhiên, đối với các leaseSet lớn hơn có đến gần 16 Lease, một kẻ quan sát có thể xác định được rằng leaseSet đó là multihomed:

- Kích thước tối đa hiện tại của tier nhanh là 75 peers. Inbound Gateway
  (IBGW, node được công bố trong một Lease) được chọn từ một phần của tier
  (được phân vùng ngẫu nhiên cho mỗi tunnel pool theo hash, không phải theo số lượng):

      1 hop
          The whole fast tier

      2 hops
          Half of the fast tier
          (the default until mid-2014)

      3+ hops
          A quarter of the fast tier
          (3 being the current default)

Điều đó có nghĩa là trung bình các IBGW sẽ đến từ một tập hợp gồm 20-30 peer.

- Trong một thiết lập single-homed, một LeaseSet 16-tunnel đầy đủ sẽ có 16 IBGW được chọn ngẫu nhiên từ một tập hợp gồm tối đa (ví dụ) 20 peer.

- Trong thiết lập multihomed 4-router sử dụng cấu hình mặc định, một LeaseSet 16-tunnel đầy đủ sẽ có 16 IBGW được chọn ngẫu nhiên từ tập hợp tối đa 80 peer, mặc dù có khả năng có một phần peer chung giữa các router.

Do đó với cấu hình mặc định, có thể thông qua phân tích thống kê để tìm ra rằng một LeaseSet đang được tạo ra bởi giao thức này. Cũng có thể tìm ra có bao nhiêu router, mặc dù tác động của sự thay đổi trên các tầng nhanh sẽ làm giảm hiệu quả của phân tích này.

Vì client có toàn quyền kiểm soát việc lựa chọn các peer, việc rò rỉ thông tin này có thể được giảm thiểu hoặc loại bỏ bằng cách chọn các IBGW từ một tập hợp peer hạn chế.

## Compatibility

Thiết kế này hoàn toàn tương thích ngược với mạng lưới, vì không có thay đổi nào đối với định dạng LeaseSet. Tất cả các router sẽ cần nhận biết giao thức mới, nhưng điều này không phải là mối quan tâm vì chúng sẽ được điều khiển bởi cùng một thực thể.

## Performance and scalability notes

Giới hạn trên là 16 Leases cho mỗi LeaseSet không bị thay đổi bởi đề xuất này. Đối với các Destinations yêu cầu nhiều tunnels hơn mức này, có hai cách sửa đổi mạng có thể thực hiện:

- Tăng giới hạn trên về kích thước của LeaseSets. Đây sẽ là cách đơn giản nhất để triển khai (mặc dù vẫn yêu cầu hỗ trợ mạng lưới toàn diện trước khi có thể được sử dụng rộng rãi), nhưng có thể dẫn đến việc tra cứu chậm hơn do kích thước gói tin lớn hơn. Kích thước LeaseSet tối đa khả thi được định nghĩa bởi MTU của các transport bên dưới, và do đó khoảng 16kB.

- Triển khai Proposal 123 cho LeaseSets phân tầng. Kết hợp với proposal này,
  các Destinations cho sub-LeaseSets có thể được phân bố trên nhiều
  routers, hoạt động hiệu quả như nhiều địa chỉ IP cho một dịch vụ clearnet.

## Acknowledgements

Cảm ơn psi vì cuộc thảo luận đã dẫn đến đề xuất này.
