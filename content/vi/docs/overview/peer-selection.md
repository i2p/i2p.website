---
title: "Phân tích và lựa chọn Peer"
description: "Cách các I2P router lập hồ sơ và chọn lựa các peer để xây dựng tunnel"
slug: "peer-selection"
aliases:
  - "/vi/how_peerselection"
  - "/vi/how_peerselection/"
lastUpdated: "2024-02"
accurateFor: "0.9.62"
---

## Ghi chú

Trang này mô tả việc triển khai Java I2P về profiling và lựa chọn peer tính đến năm 2010. Mặc dù vẫn chính xác một cách tổng thể, một số chi tiết có thể không còn đúng nữa. Chúng tôi tiếp tục phát triển các chiến lược cấm, chặn và lựa chọn để đối phó với những mối đe dọa, tấn công và điều kiện mạng mới hơn. Mạng hiện tại có nhiều triển khai router với các phiên bản khác nhau. Các triển khai I2P khác có thể có các chiến lược profiling và lựa chọn hoàn toàn khác biệt, hoặc có thể không sử dụng profiling chút nào.

## Tổng quan {#overview}

### Phân Tích Peer {#profiling}

**Peer profiling** là quá trình thu thập dữ liệu dựa trên hiệu suất **quan sát được** của các router hoặc peer khác, và phân loại các peer đó thành các nhóm. Profiling **không** sử dụng bất kỳ dữ liệu hiệu suất tự công bố nào được peer đó xuất bản trong [network database](/docs/overview/network-database).

Profiles được sử dụng cho hai mục đích:

1. Lựa chọn các peer để chuyển tiếp lưu lượng truy cập của chúng ta, điều này sẽ được thảo luận bên dưới
2. Chọn các peer từ tập hợp các floodfill router để sử dụng cho việc lưu trữ và truy vấn cơ sở dữ liệu mạng,
   điều này được thảo luận trên trang [network database](/docs/overview/network-database)

### Lựa chọn Peer {#selection}

**Lựa chọn peer** là quá trình chọn ra những router nào trên mạng mà chúng ta muốn chuyển tiếp thông điệp của mình (những peer nào mà chúng ta sẽ yêu cầu tham gia vào tunnel của chúng ta). Để thực hiện điều này, chúng ta theo dõi hiệu suất của từng peer (hồ sơ "profile" của peer) và sử dụng dữ liệu đó để ước tính tốc độ của chúng, tần suất chúng có thể chấp nhận yêu cầu của chúng ta, và liệu chúng có vẻ bị quá tải hay không thể thực hiện một cách đáng tin cậy những gì mà chúng đã đồng ý.

Khác với một số mạng ẩn danh khác, trong I2P, băng thông được tuyên bố là không đáng tin cậy và **chỉ** được sử dụng để tránh những peer quảng cáo băng thông rất thấp không đủ để định tuyến tunnel. Tất cả việc lựa chọn peer đều được thực hiện thông qua profiling. Điều này ngăn chặn các cuộc tấn công đơn giản dựa trên việc peer tuyên bố băng thông cao để chiếm đoạt số lượng lớn tunnel. Nó cũng làm cho các [cuộc tấn công thời gian](/docs/overview/threat-model#timing) trở nên khó khăn hơn.

Việc lựa chọn peer được thực hiện khá thường xuyên, vì một router có thể duy trì một số lượng lớn các tunnel client và khám phá, và thời gian sống của tunnel chỉ có 10 phút.

### Thông tin thêm {#further-info}

Để biết thêm thông tin, xem bài báo [Peer Profiling and Selection in the I2P Anonymous Network](/pdf/I2P-PET-CON-2009.1.pdf) được trình bày tại [PET-CON 2009.1](http://web.archive.org/web/20100413184504/http://www.pet-con.org/index.php/PET_Convention_2009.1). Xem [bên dưới](#notes) để biết ghi chú về những thay đổi nhỏ kể từ khi bài báo được xuất bản.

## Hồ sơ {#profiles}

Mỗi peer có một tập hợp các điểm dữ liệu được thu thập về họ, bao gồm thống kê về thời gian họ mất để trả lời truy vấn cơ sở dữ liệu mạng (network database query), tần suất các tunnel của họ bị lỗi, và số lượng peer mới họ có thể giới thiệu cho chúng ta, cũng như các điểm dữ liệu đơn giản như lần cuối chúng ta nghe tin từ họ hoặc khi lỗi giao tiếp cuối cùng xảy ra.

Profiles khá nhỏ, chỉ vài KB. Để kiểm soát việc sử dụng bộ nhớ, thời gian hết hạn của profile sẽ giảm khi số lượng profiles tăng lên. Profiles được giữ trong bộ nhớ cho đến khi router tắt, lúc đó chúng sẽ được ghi vào đĩa. Khi khởi động, các profiles được đọc để router không cần phải khởi tạo lại tất cả profiles, do đó cho phép router nhanh chóng tích hợp trở lại vào mạng sau khi khởi động.

## Tóm tắt Peer {#summaries}

Trong khi bản thân các profile có thể được coi là bản tóm tắt hiệu suất của một peer, để cho phép lựa chọn peer hiệu quả, chúng tôi chia nhỏ mỗi bản tóm tắt thành bốn giá trị đơn giản, đại diện cho tốc độ của peer, khả năng của nó, mức độ tích hợp tốt vào mạng lưới, và liệu nó có đang gặp sự cố hay không.

### Tốc độ {#speed}

Việc tính toán tốc độ đơn giản chỉ là xem qua profile và ước tính lượng dữ liệu chúng ta có thể gửi hoặc nhận trên một tunnel duy nhất thông qua peer trong một phút. Để ước tính này, nó chỉ xem xét hiệu suất trong phút trước đó.

### Dung lượng {#capacity}

Việc tính toán dung lượng đơn giản là đi qua hồ sơ và ước tính số lượng tunnel mà peer sẽ đồng ý tham gia trong một khoảng thời gian nhất định. Để có ước tính này, nó xem xét số lượng yêu cầu xây dựng tunnel mà peer đã chấp nhận, từ chối và bỏ qua, cũng như số lượng tunnel đã đồng ý tham gia nhưng sau đó bị lỗi. Mặc dù việc tính toán được tính trọng số theo thời gian để hoạt động gần đây được tính nhiều hơn hoạt động trước đó, nhưng thống kê lên đến 48 giờ trước vẫn có thể được bao gồm.

Nhận biết và tránh các peer không đáng tin cậy và không thể tiếp cận được là vô cùng quan trọng. Thật không may, vì việc xây dựng và kiểm tra tunnel đòi hỏi sự tham gia của nhiều peer, nên rất khó để xác định chính xác nguyên nhân gây ra việc yêu cầu build bị hủy bỏ hoặc kiểm tra thất bại. Router sẽ gán một xác suất thất bại cho từng peer và sử dụng xác suất đó trong tính toán công suất. Các lần hủy bỏ và thất bại kiểm tra được tính trọng số cao hơn nhiều so với các lần từ chối.

## Tổ chức Peer {#organization}

Như đã đề cập ở trên, chúng tôi phân tích chi tiết hồ sơ của từng peer để đưa ra một số tính toán quan trọng, và dựa trên đó, chúng tôi tổ chức mỗi peer vào ba nhóm - nhanh, dung lượng cao và tiêu chuẩn.

Các nhóm này không loại trừ lẫn nhau, cũng không hoàn toàn độc lập:

- Một peer được coi là "high capacity" (công suất cao) nếu tính toán công suất của nó đạt hoặc vượt quá giá trị trung vị của tất cả các peer.
- Một peer được coi là "fast" (nhanh) nếu chúng đã là "high capacity" và tính toán tốc độ của chúng đạt hoặc vượt quá giá trị trung vị của tất cả các peer.
- Một peer được coi là "standard" (tiêu chuẩn) nếu nó không phải là "high capacity"

### Giới Hạn Kích Thước Nhóm {#group-limits}

Kích thước của các nhóm có thể bị giới hạn.

- Nhóm nhanh được giới hạn ở 30 peer.
  Nếu có nhiều hơn, chỉ những peer có xếp hạng tốc độ cao nhất mới được đưa vào nhóm.
- Nhóm dung lượng cao được giới hạn ở 75 peer (bao gồm cả nhóm nhanh).
  Nếu có nhiều hơn, chỉ những peer có xếp hạng dung lượng cao nhất mới được đưa vào nhóm.
- Nhóm tiêu chuẩn không có giới hạn cố định, nhưng có phần nhỏ hơn số lượng RouterInfos
  được lưu trữ trong cơ sở dữ liệu mạng cục bộ.
  Trên một router hoạt động trong mạng hiện tại, có thể có khoảng 1000 RouterInfos và 500 hồ sơ peer
  (bao gồm cả những peer trong nhóm nhanh và nhóm dung lượng cao).

## Tính toán lại và Ổn định {#recalculation}

Các tóm tắt được tính toán lại và các peer được sắp xếp lại thành các nhóm, cứ mỗi 45 giây.

Các nhóm có xu hướng khá ổn định, nghĩa là không có nhiều "biến động" trong thứ hạng ở mỗi lần tính toán lại. Các peer trong nhóm tốc độ cao và dung lượng lớn sẽ có nhiều tunnel được xây dựng qua chúng hơn, điều này làm tăng xếp hạng tốc độ và dung lượng của chúng, từ đó củng cố sự hiện diện của chúng trong nhóm.

## Lựa chọn Peer {#peer-selection}

Router chọn các peer từ các nhóm trên để xây dựng tunnel thông qua.

### Lựa chọn Peer cho Client Tunnel {#client-tunnels}

Client tunnel được sử dụng cho lưu lượng ứng dụng, chẳng hạn như cho HTTP proxy và web server.

Để giảm khả năng bị tấn công bởi [một số cuộc tấn công](http://blog.torproject.org/blog/one-cell-enough) và tăng hiệu suất, các peer để xây dựng tunnel client được chọn ngẫu nhiên từ nhóm nhỏ nhất, đó là nhóm "nhanh". Không có sự thiên vị trong việc lựa chọn các peer đã từng tham gia vào tunnel cho cùng một client trước đó.

### Lựa chọn Peer cho Tunnel Khám phá {#exploratory-tunnels}

Tunnel thăm dò được sử dụng cho các mục đích quản trị router, chẳng hạn như lưu lượng cơ sở dữ liệu mạng và kiểm tra tunnel client. Tunnel thăm dò cũng được sử dụng để liên lạc với các router chưa được kết nối trước đó, đó là lý do tại sao chúng được gọi là "thăm dò". Những tunnel này thường có băng thông thấp.

Các peer để xây dựng tunnel thám hiểm thường được chọn ngẫu nhiên từ nhóm tiêu chuẩn. Nếu tỷ lệ thành công của các lần thử xây dựng này thấp so với tỷ lệ thành công xây dựng tunnel client, router sẽ chọn trung bình có trọng số các peer ngẫu nhiên từ nhóm công suất cao thay thế. Điều này giúp duy trì tỷ lệ thành công xây dựng thỏa đáng ngay cả khi hiệu suất mạng kém. Không có xu hướng thiên vị việc chọn các peer đã từng là người tham gia trong tunnel thám hiểm trước đó.

Vì nhóm chuẩn bao gồm một tập con rất lớn của tất cả các peer mà router biết, các exploratory tunnel về cơ bản được xây dựng thông qua việc lựa chọn ngẫu nhiên từ tất cả các peer, cho đến khi tỷ lệ thành công xây dựng trở nên quá thấp.

### Hạn chế {#restrictions}

Để ngăn chặn một số cuộc tấn công đơn giản và để tối ưu hiệu suất, có các hạn chế sau:

- Hai peer từ cùng một không gian IP /16 không thể ở trong cùng một tunnel.
- Một peer có thể tham gia tối đa 33% tổng số tunnel được tạo bởi router.
- Các peer có băng thông cực thấp sẽ không được sử dụng.
- Các peer mà việc kết nối gần đây đã thất bại sẽ không được sử dụng.

### Thứ tự Peer trong Tunnel {#ordering}

Các peer được sắp xếp thứ tự trong tunnel để đối phó với [cuộc tấn công predecessor](http://forensics.umass.edu/pubs/wright-tissec.pdf) ([cập nhật 2008](http://forensics.umass.edu/pubs/wright.tissec.2008.pdf)). Thông tin chi tiết có trong [trang tunnel](/docs/specs/tunnel-implementation#ordering).

## Công việc tương lai {#future}

- Tiếp tục phân tích và điều chỉnh các tính toán tốc độ và dung lượng khi cần thiết
- Triển khai chiến lược loại bỏ tích cực hơn nếu cần thiết để kiểm soát việc sử dụng bộ nhớ khi mạng phát triển
- Đánh giá các giới hạn kích thước nhóm
- Sử dụng dữ liệu GeoIP để bao gồm hoặc loại trừ một số peer nhất định, nếu được cấu hình

## Ghi chú {#notes}

Đối với những người đọc bài báo [Peer Profiling and Selection in the I2P Anonymous Network](/pdf/I2P-PET-CON-2009.1.pdf), xin hãy lưu ý những thay đổi nhỏ sau đây trong I2P kể từ khi bài báo được xuất bản:

- Tính toán Integration vẫn chưa được sử dụng
- Trong bài báo, "groups" được gọi là "tiers"
- Tier "Failing" không còn được sử dụng nữa
- Tier "Not Failing" hiện được đặt tên là "Standard"

## Tham khảo {#references}

- [Peer Profiling and Selection in the I2P Anonymous Network](/pdf/I2P-PET-CON-2009.1.pdf)
- [One Cell Enough](http://blog.torproject.org/blog/one-cell-enough)
- [Tor Entry Guards](https://wiki.torproject.org/noreply/TheOnionRouter/TorFAQ#EntryGuards)
- [Murdoch 2007 Paper](http://freehaven.net/anonbib/#murdoch-pet2007)
- [Tune-up for Tor](http://www.crhc.uiuc.edu/~nikita/papers/tuneup-cr.pdf)
- [Low-resource Routing Attacks Against Tor](http://cs.gmu.edu/~mccoy/papers/wpes25-bauer.pdf)
