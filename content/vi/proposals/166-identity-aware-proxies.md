---
title: "Đề xuất I2P #166: Các Loại Tunnel Nhận Biết Danh Tính/Host"
number: "166"
author: "eyedeekay"
created: "2024-05-27"
lastupdated: "2024-08-27"
status: "Mở"
thread: "http://i2pforum.i2p/viewforum.php?f=13"
target: "0.9.65"
toc: true
---

### Đề xuất cho Loại Tunnel HTTP Proxy Nhận thức Host

Đây là một đề xuất để giải quyết "Vấn đề Danh tính Được Chia sẻ" trong việc sử dụng HTTP-over-I2P thông thường bằng cách giới thiệu một loại tunnel proxy HTTP mới. Loại tunnel này có hành vi bổ sung được thiết kế nhằm ngăn chặn hoặc hạn chế tính hữu dụng của việc theo dõi được thực hiện bởi các nhà vận hành dịch vụ ẩn có khả năng thù địch, chống lại các user-agent được nhắm mục tiêu (trình duyệt) và chính I2P Client Application.

#### What is the “Shared Identity” problem?

Vấn đề "Shared Identity" (Chia sẻ danh tính) xảy ra khi một user-agent trên mạng overlay được định địa chỉ bằng mật mã học chia sẻ một danh tính mật mã học với user-agent khác. Điều này xảy ra, ví dụ, khi cả Firefox và GNU Wget đều được cấu hình để sử dụng cùng một HTTP Proxy.

Trong trường hợp này, server có thể thu thập và lưu trữ địa chỉ mật mã (Destination) được sử dụng để phản hồi hoạt động. Server có thể coi đây như một "Dấu vân tay" luôn luôn 100% duy nhất, vì nó có nguồn gốc mật mã. Điều này có nghĩa là khả năng liên kết được quan sát thấy bởi vấn đề Shared Identity là hoàn hảo.

Nhưng đây có phải là vấn đề? ^^^^^^^^^^^^^^^^^^^^

Vấn đề danh tính chia sẻ là một vấn đề khi các user-agent sử dụng cùng một giao thức mong muốn tính không thể liên kết được. [Nó được đề cập lần đầu trong bối cảnh HTTP tại Reddit Thread này](https://old.reddit.com/r/i2p/comments/579idi/warning_i2p_is_linkablefingerprintable/), với các bình luận đã bị xóa có thể truy cập nhờ [pullpush.io](https://api.pullpush.io/reddit/search/comment/?link_id=579idi). *Vào thời điểm đó* tôi là một trong những người phản hồi tích cực nhất, và *vào thời điểm đó* tôi tin rằng vấn đề này là nhỏ. Trong 8 năm qua, tình hình và ý kiến của tôi về nó đã thay đổi, giờ đây tôi tin rằng mối đe dọa do tương quan destination độc hại gây ra tăng lên đáng kể khi nhiều trang web hơn có thể "lập hồ sơ" các người dùng cụ thể.

Cuộc tấn công này có rào cản gia nhập rất thấp. Nó chỉ yêu cầu người vận hành dịch vụ ẩn phải vận hành nhiều dịch vụ. Đối với các cuộc tấn công nhằm vào những lượt truy cập đồng thời (truy cập nhiều trang web cùng lúc), đây là yêu cầu duy nhất. Đối với việc liên kết không đồng thời, một trong những dịch vụ đó phải là dịch vụ lưu trữ "tài khoản" thuộc về một người dùng duy nhất được nhắm mục tiêu để theo dõi.

Hiện tại, bất kỳ nhà điều hành dịch vụ nào lưu trữ tài khoản người dùng sẽ có thể liên kết chúng với hoạt động trên các trang web họ kiểm soát bằng cách khai thác vấn đề Shared Identity (Danh tính dùng chung). Mastodon, Gitlab, hoặc thậm chí các diễn đàn đơn giản có thể là những kẻ tấn công núp bóng miễn là họ vận hành nhiều hơn một dịch vụ và có mục đích tạo hồ sơ cho người dùng. Việc giám sát này có thể được thực hiện để theo dõi, thu lợi tài chính hoặc vì lý do liên quan đến tình báo. Hiện tại có hàng chục nhà điều hành lớn có thể thực hiện cuộc tấn công này và thu thập dữ liệu có ý nghĩa từ đó. Chúng ta chủ yếu tin tưởng họ không làm như vậy trong thời điểm hiện tại, nhưng những nhân tố không quan tâm đến ý kiến của chúng ta có thể dễ dàng xuất hiện.

Điều này liên quan trực tiếp đến một hình thức xây dựng hồ sơ khá cơ bản trên clear web (mạng công khai) nơi các tổ chức có thể liên kết các tương tác trên trang web của họ với các tương tác trên các mạng mà họ kiểm soát. Trên I2P, bởi vì cryptographic destination (đích mã hóa) là duy nhất, kỹ thuật này đôi khi có thể thậm chí còn đáng tin cậy hơn, mặc dù không có thêm sức mạnh của định vị địa lý.

Shared Identity không hữu ích chống lại người dùng chỉ sử dụng I2P để che giấu vị trí địa lý. Nó cũng không thể được dùng để phá vỡ routing của I2P. Đây chỉ là vấn đề của việc quản lý danh tính theo ngữ cảnh.

-  It is impossible to use the Shared Identity problem to geolocate an
   I2P user.
-  It is impossible to use the Shared Identity problem to link I2P
   sessions if they are not contemporary.

Tuy nhiên, có thể sử dụng nó để làm giảm tính ẩn danh của người dùng I2P trong những trường hợp có lẽ rất phổ biến. Một lý do chúng phổ biến là vì chúng ta khuyến khích sử dụng Firefox, một trình duyệt web hỗ trợ hoạt động "Tabbed" (đa tab).

-  It is *always* possible to produce a fingerprint from the Shared
   Identity problem in *any* web browser which supports requesting
   third-party resources.
-  Disabling Javascript accomplishes **nothing** against the Shared
   Identity problem.
-  If a link can be established between non-contemporary sessions such
   as by “traditional” browser fingerprinting, then the Shared Identity
   can be applied transitively, potentially enabling a non-contemporary
   linking strategy.
-  If a link can be established between a clearnet activity and an I2P
   identity, for instance, if the target is logged into a site with both
   an I2P and a clearnet presence on both sides, the Shared Identity can
   be applied transitively, potentially enabling complete
   de-anonymization.

Cách bạn đánh giá mức độ nghiêm trọng của vấn đề Shared Identity khi áp dụng vào I2P HTTP proxy phụ thuộc vào việc bạn (hay chính xác hơn, một "người dùng" với những kỳ vọng có thể thiếu hiểu biết) nghĩ rằng "contextual identity" của ứng dụng nằm ở đâu. Có một số khả năng:

1. HTTP is both the Application and the Contextual Identity - This is
   how it works now. All HTTP Applications share an identity.
2. The Process is the Application and the Contextual Identity - This is
   how it works when an application uses an API like SAMv3 or I2CP,
   where an application creates it’s identity and controls it’s
   lifetime.
3. HTTP is the Application, but the Host is the Contextual Identity
   -This is the object of this proposal, which treats each Host as a
   potential “Web Application” and treats the threat surface as such.

Liệu có thể giải quyết được không? ^^^^^^^^^^^^^^^

Có lẽ không thể tạo ra một proxy có thể phản ứng thông minh với mọi trường hợp có thể xảy ra mà hoạt động của nó có thể làm suy yếu tính ẩn danh của ứng dụng. Tuy nhiên, có thể xây dựng một proxy phản ứng thông minh với một ứng dụng cụ thể hoạt động theo cách có thể dự đoán được. Ví dụ, trong các Trình duyệt Web hiện đại, người dùng thường mở nhiều tab cùng lúc, nơi họ tương tác với nhiều trang web khác nhau, được phân biệt bằng hostname.

Điều này cho phép chúng ta cải thiện hành vi của HTTP Proxy cho loại HTTP user-agent này bằng cách làm cho hành vi của proxy khớp với hành vi của user-agent thông qua việc cung cấp cho mỗi host một Destination riêng khi sử dụng với HTTP Proxy. Thay đổi này khiến việc sử dụng vấn đề Shared Identity để tạo ra fingerprint có thể được dùng để liên kết hoạt động của client với 2 host trở nên bất khả thi, bởi vì 2 host đơn giản sẽ không còn chia sẻ cùng một return identity.

Mô tả:
^^^^^^^^^^^^

Một HTTP Proxy mới sẽ được tạo và thêm vào Hidden Services Manager(I2PTunnel). HTTP Proxy mới này sẽ hoạt động như một "multiplexer" của các I2PSocketManager. Bản thân multiplexer không có destination. Mỗi I2PSocketManager riêng lẻ trở thành một phần của multiplex đều có local destination riêng và tunnel pool riêng. Các I2PSocketManager được tạo theo yêu cầu bởi multiplexer, trong đó "yêu cầu" là lần truy cập đầu tiên đến host mới. Có thể tối ưu hóa việc tạo các I2PSocketManager trước khi chèn chúng vào multiplexer bằng cách tạo trước một hoặc nhiều I2PSocketManager và lưu trữ chúng bên ngoài multiplexer. Điều này có thể cải thiện hiệu suất.

Một I2PSocketManager bổ sung, với destination riêng của nó, được thiết lập như một "carrier" của "Outproxy" cho bất kỳ trang web nào *không* có I2P Destination, ví dụ như bất kỳ trang web Clearnet nào. Điều này có hiệu quả biến tất cả việc sử dụng Outproxy thành một Contextual Identity (nhận dạng theo ngữ cảnh) duy nhất, với lưu ý rằng việc cấu hình nhiều Outproxy cho tunnel sẽ gây ra việc luân chuyển outproxy "Sticky" (dính) thông thường, trong đó mỗi outproxy chỉ nhận các yêu cầu cho một trang web duy nhất. Đây *gần như* là hành vi tương đương với việc cô lập các proxy HTTP-over-I2P theo destination trên internet thông thường.

Cân nhắc về Tài nguyên: ''''''''''''''''''''''''

Proxy HTTP mới yêu cầu thêm tài nguyên so với proxy HTTP hiện tại. Nó sẽ:

-  Potentially build more tunnels and I2PSocketManagers
-  Build tunnels more often

Mỗi cái trong số này yêu cầu:

-  Local computing resources
-  Network resources from peers

Cài đặt: '''''''

Để giảm thiểu tác động của việc tăng sử dụng tài nguyên, proxy nên được cấu hình để sử dụng ít nhất có thể. Các proxy là một phần của multiplexer (không phải parent proxy) nên được cấu hình để:

-  Multiplexed I2PSocketManagers build 1 tunnel in, 1 tunnel out in their
   tunnel pools
-  Multiplexed I2PSocketManagers take 3 hops by default.
-  Close sockets after 10 minutes of inactivity
-  I2PSocketManagers started by the Multiplexer share the lifespan of the
   Multiplexer. Multiplexed tunnels are not “Destructed” until the
   parent Multiplexer is.

Biểu đồ:
^^^^^^^^^

Biểu đồ bên dưới minh họa hoạt động hiện tại của HTTP proxy, tương ứng với "Khả năng 1" trong phần "Có phải là vấn đề không". Như bạn có thể thấy, HTTP proxy tương tác trực tiếp với các I2P sites chỉ sử dụng một destination duy nhất. Trong kịch bản này, HTTP vừa là ứng dụng vừa là danh tính ngữ cảnh.

```text
**Tình Hình Hiện Tại: HTTP là Ứng Dụng, HTTP là Danh Tính Theo Ngữ Cảnh**
                                                          __-> Outproxy <-> i2pgit.org
                                                         /
   Browser <-> HTTP Proxy(một Destination)<->I2PSocketManager <---> idk.i2p
                                                         \__-> translate.idk.i2p
                                                          \__-> git.idk.i2p
```

Sơ đồ dưới đây mô tả hoạt động của một HTTP proxy nhận biết host, tương ứng với "Khả năng 3" trong phần "Có phải là vấn đề không". Trong tình huống này, HTTP là ứng dụng, nhưng Host định nghĩa bản sắc theo ngữ cảnh, trong đó mỗi trang I2P tương tác với một HTTP proxy khác nhau với một destination duy nhất cho mỗi host. Điều này ngăn chặn những người vận hành nhiều trang web có thể phân biệt khi cùng một người đang truy cập nhiều trang web mà họ vận hành.

```text
**Sau Khi Thay Đổi: HTTP là Ứng Dụng, Host là Danh Tính Ngữ Cảnh**
                                                        __-> I2PSocketManager(Destination A - Chỉ Outproxies) <--> i2pgit.org
                                                       /
   Browser <-> HTTP Proxy Multiplexer(Không Destination) <---> I2PSocketManager(Destination B) <--> idk.i2p
                                                       \__-> I2PSocketManager(Destination C) <--> translate.idk.i2p
                                                        \__-> I2PSocketManager(Destination C) <--> git.idk.i2p
```

Trạng thái:
^^^^^^^

Một phiên bản Java hoạt động của host-aware proxy tuân thủ theo phiên bản cũ hơn của đề xuất này có sẵn tại fork của idk dưới nhánh: i2p.i2p.2.6.0-browser-proxy-post-keepalive Link trong phần trích dẫn. Nó đang được sửa đổi mạnh để chia nhỏ các thay đổi thành những phần nhỏ hơn.

Các triển khai với khả năng khác nhau đã được viết bằng Go sử dụng thư viện SAMv3, chúng có thể hữu ích cho việc nhúng vào các ứng dụng Go khác hoặc cho go-i2p nhưng không phù hợp với Java I2P. Ngoài ra, chúng thiếu hỗ trợ tốt để làm việc tương tác với leaseSet được mã hóa.

Phụ lục: ``i2psocks``

Một cách tiếp cận đơn giản hướng đến ứng dụng để cách ly các loại client khác là có thể thực hiện được mà không cần triển khai loại tunnel mới hoặc thay đổi mã I2P hiện có bằng cách kết hợp các công cụ I2PTunnel đã tồn tại, những công cụ này đã có sẵn rộng rãi và được thử nghiệm trong cộng đồng bảo mật. Tuy nhiên, cách tiếp cận này đưa ra một giả định khó khăn không đúng với HTTP và cũng không đúng với nhiều loại I2P client tiềm năng khác.

Đại khái, script sau đây sẽ tạo ra một SOCKS5 proxy nhận biết ứng dụng và socksify lệnh bên dưới:

```sh
#! /bin/sh
command_to_proxy="$@"
java -jar ~/i2p/lib/i2ptunnel.jar -wait -e 'sockstunnel 7695'
torsocks --port 7695 $command_to_proxy
```

Phụ lục: ``example implementation of the attack``

[Một ví dụ triển khai của cuộc tấn công Shared Identity trên HTTP User-Agents](https://github.com/eyedeekay/colluding_sites_attack/) đã tồn tại trong nhiều năm. Một ví dụ bổ sung có sẵn trong thư mục con ``simple-colluder`` của [kho lưu trữ prop166 của idk](https://git.idk.i2p/idk/i2p.host-aware-proxy). Những ví dụ này được thiết kế có chủ ý để chứng minh rằng cuộc tấn công hoạt động và sẽ cần được sửa đổi (mặc dù nhỏ) để biến thành một cuộc tấn công thực sự.

Addendum: ``example implementation of the attack``

[An example implementation of the Shared Identity attack on HTTP User-Agents](https://github.com/eyedeekay/colluding_sites_attack/) has existed for several years. An additional example is available in the ``simple-colluder`` subdirectory of [idk’s prop166 repository](https://git.idk.i2p/idk/i2p.host-aware-proxy) These examples are deliberately designed to demonstrate that the attack works and would require modification(albeit minor) to be turned into a real attack.
