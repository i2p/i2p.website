---
title: "Hiệu suất"
description: "Hiệu suất mạng I2P: tốc độ, kết nối và quản lý tài nguyên"
slug: "performance"
aliases:
  - "/vi/about/performance/future"
  - "/vi/about/performance/future/"
  - "/vi/about/performance/history"
  - "/vi/about/performance/history/"
lastUpdated: "2025-01"
accurateFor: "0.9.65"
---

## Hiệu suất Mạng I2P: Tốc độ, Kết nối và Quản lý Tài nguyên

Mạng I2P hoàn toàn động. Mỗi client được các node khác biết đến và kiểm tra các node đã biết cục bộ về khả năng tiếp cận và dung lượng. Chỉ những node có thể tiếp cận và có khả năng mới được lưu vào NetDB cục bộ. Trong quá trình xây dựng tunnel, các tài nguyên tốt nhất được chọn từ nhóm này để xây dựng tunnel. Vì việc kiểm tra diễn ra liên tục, nhóm các node thay đổi. Mỗi node I2P biết một phần khác nhau của NetDB, có nghĩa là mỗi router có một tập hợp các node I2P khác nhau để sử dụng cho tunnel. Ngay cả khi hai router có cùng tập con các node đã biết, các bài kiểm tra về khả năng tiếp cận và dung lượng có thể sẽ cho kết quả khác nhau, vì các router khác có thể đang chịu tải ngay khi một router kiểm tra, nhưng lại rảnh khi router thứ hai kiểm tra.

Điều này giải thích tại sao mỗi I2P node có các node khác nhau để xây dựng tunnel. Bởi vì mỗi I2P node có độ trễ và băng thông khác nhau, các tunnel (được xây dựng thông qua những node đó) có các giá trị độ trễ và băng thông khác nhau. Và bởi vì mỗi I2P node có các tunnel được xây dựng khác nhau, không có hai I2P node nào có cùng bộ tunnel.

Một server/client được gọi là "destination" và mỗi destination có ít nhất một tunnel đầu vào và một tunnel đầu ra. Mặc định là 3 hop trên mỗi tunnel. Điều này tổng cộng là 12 hop (hay 12 I2P node khác nhau) cho một hành trình khứ hồi đầy đủ client-server-client.

Mỗi gói dữ liệu được gửi qua 6 node I2P khác cho đến khi nó đến được máy chủ:

```
client - hop1 - hop2 - hop3 - hopa1 - hopa2 - hopa3 - server
```
và trên đường trở về qua 6 I2P node khác nhau:

```
server - hopb1 - hopb2 - hopb3 - hopc1 - hopc2 - hopc3 - client
```
Lưu lượng trên mạng cần có ACK trước khi dữ liệu mới được gửi, nó cần phải chờ cho đến khi ACK trả về từ máy chủ: gửi dữ liệu, chờ ACK, gửi thêm dữ liệu, chờ ACK. Vì RTT (RoundTripTime) tích lũy từ độ trễ của từng I2P node riêng lẻ và mỗi kết nối trong chuyến đi khứ hồi này, thường mất 1-3 giây cho đến khi ACK trở lại client. Do thiết kế TCP và I2P transport, một gói dữ liệu có kích thước giới hạn. Kết hợp các điều kiện này đặt ra giới hạn băng thông tối đa mỗi tunnel là 20-50 kbyte/giây. Tuy nhiên, nếu CHỈ MỘT hop trong tunnel chỉ có 5 kb/giây băng thông để sử dụng, toàn bộ tunnel sẽ bị giới hạn ở 5 kb/giây, không phụ thuộc vào độ trễ và các hạn chế khác.

Mã hóa, độ trễ và cách thức xây dựng tunnel khiến việc tạo tunnel rất tốn kém về thời gian CPU. Đây là lý do tại sao một destination chỉ được phép có tối đa 6 tunnel IN và 6 tunnel OUT để truyền tải dữ liệu. Với tốc độ tối đa 50 kb/giây mỗi tunnel, một destination có thể sử dụng khoảng 300 kb/giây lưu lượng kết hợp (thực tế có thể cao hơn nếu sử dụng các tunnel ngắn hơn với mức ẩn danh thấp hoặc không có). Các tunnel đã sử dụng sẽ bị loại bỏ sau mỗi 10 phút và các tunnel mới sẽ được xây dựng. Sự thay đổi tunnel này, và đôi khi các client bị tắt hoặc mất kết nối đến mạng sẽ đôi lúc làm gián đoạn các tunnel và kết nối. Một ví dụ về điều này có thể thấy trên Mạng IRC2P khi mất kết nối (hết thời gian ping) hoặc khi sử dụng eepget.

Với một tập hợp hạn chế các đích đến và một tập hợp hạn chế các tunnel cho mỗi đích đến, một node I2P chỉ sử dụng một tập hợp hạn chế các tunnel qua các node I2P khác. Ví dụ, nếu một node I2P là "hop1" trong ví dụ nhỏ ở trên, chúng ta chỉ thấy 1 participating tunnel có nguồn gốc từ client. Nếu chúng ta tính tổng toàn bộ mạng I2P, chỉ có một số lượng khá hạn chế các participating tunnel có thể được xây dựng với một lượng bandwidth hạn chế tổng cộng. Nếu phân bố những con số hạn chế này trên số lượng các node I2P, thì chỉ có một phần nhỏ bandwidth/dung lượng có sẵn để sử dụng.

Để duy trì tính ẩn danh, một router không nên được sử dụng bởi toàn bộ mạng lưới để xây dựng tunnel. Nếu một router hoạt động như một tunnel router cho TẤT CẢ các node I2P, nó sẽ trở thành một điểm lỗi trung tâm rất thực tế cũng như một điểm trung tâm để thu thập IP và dữ liệu từ các client. Đây là lý do tại sao mạng lưới phân phối lưu lượng truy cập qua các node trong quá trình xây dựng tunnel.

Một yếu tố khác cần xem xét về hiệu suất là cách I2P xử lý mạng lưới mesh. Mỗi hop kết nối sử dụng một kết nối TCP hoặc UDP trên các node I2P. Với 1000 kết nối, ta sẽ thấy 1000 kết nối TCP. Đó là một con số khá lớn, và một số router gia đình và văn phòng nhỏ chỉ cho phép một số lượng kết nối hạn chế. I2P cố gắng giới hạn những kết nối này xuống dưới 1500 cho mỗi loại UDP và TCP. Điều này cũng giới hạn lượng lưu lượng được định tuyến qua một node I2P.

Nếu một node có thể truy cập được, có thiết lập băng thông >128 kbyte/giây chia sẻ và có thể truy cập 24/7, nó sẽ được sử dụng sau một thời gian để tham gia lưu lượng. Nếu nó bị ngắt kết nối trong lúc đó, việc kiểm tra node I2P được thực hiện bởi các node khác sẽ cho chúng biết rằng node đó không thể truy cập. Điều này sẽ chặn một node trong ít nhất 24 giờ trên các node khác. Vì vậy, các node khác đã kiểm tra node đó là ngắt kết nối sẽ không sử dụng node đó trong 24 giờ để xây dựng tunnel. Đây là lý do tại sao lưu lượng của bạn thấp hơn sau khi khởi động lại/tắt I2P router trong tối thiểu 24 giờ.

Ngoài ra, các node I2P khác cần biết về một I2P router để kiểm tra khả năng kết nối và dung lượng của nó. Quá trình này có thể được thực hiện nhanh hơn khi bạn tương tác với mạng, ví dụ như sử dụng các ứng dụng hoặc truy cập các trang I2P, điều này sẽ dẫn đến việc xây dựng thêm tunnel và do đó có thêm hoạt động và khả năng kết nối để các node trên mạng kiểm tra.

---

## Cải thiện Hiệu suất

Để biết về các cải tiến hiệu suất có thể có trong tương lai, xem [Cải Tiến Hiệu Suất Tương Lai](/docs/overview/performance#future).

Để xem các cải tiến hiệu suất trước đây, hãy xem [Lịch sử Hiệu suất](/docs/overview/performance#history).
