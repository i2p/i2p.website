---
title: "Ghi chú trạng thái I2P cho ngày 2005-02-01"
date: 2005-02-01
author: "jr"
description: "Ghi chú tình hình phát triển I2P hàng tuần bao gồm tiến độ mã hóa tunnel 0.5, máy chủ NNTP mới và các đề xuất kỹ thuật"
categories: ["status"]
---

Chào mọi người, đến giờ cập nhật tình hình hàng tuần rồi.

* Index

1) trạng thái 0.5 2) nntp 3) các đề xuất kỹ thuật 4) ???

* 1) 0.5 status

Đã có rất nhiều tiến triển liên quan đến 0.5, với một loạt commit lớn hôm qua. Phần lớn router hiện sử dụng tunnel encryption và tunnel pooling mới [1], và nó đã hoạt động tốt trên mạng thử nghiệm. Vẫn còn một số thành phần then chốt cần được tích hợp, và rõ ràng mã nguồn không tương thích ngược, nhưng tôi hy vọng chúng ta có thể triển khai ở quy mô rộng hơn vào một thời điểm nào đó trong tuần tới.

Như đã đề cập trước đó, bản phát hành 0.5 ban đầu sẽ cung cấp nền tảng để các chiến lược lựa chọn/sắp xếp thứ tự peer (nút ngang hàng) cho tunnel khác nhau có thể hoạt động. Chúng tôi sẽ bắt đầu với một bộ tham số có thể cấu hình cơ bản cho các pool exploratory và client, nhưng các bản phát hành sau này nhiều khả năng sẽ bao gồm các tùy chọn khác cho các hồ sơ người dùng khác nhau.

[1] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/tunnel-alt.html?rev=HEAD

* 2) nntp

Như đã đề cập trên trang của LazyGuy [2] và blog của tôi [3], chúng tôi có một máy chủ NNTP mới đã hoạt động trên mạng, truy cập được tại nntp.fr.i2p. Trong khi LazyGuy đã chạy một vài tập lệnh suck [4] để nạp một vài danh sách từ gmane, nội dung nhìn chung là về, dành cho và bởi người dùng I2P.  jdot, LazyGuy và tôi đã tìm hiểu xem những trình đọc tin nào có thể dùng một cách an toàn, và dường như có vài giải pháp khá đơn giản. Xem blog của tôi để biết hướng dẫn chạy slrn [5] để đọc và đăng tin ẩn danh.

[2] http://fr.i2p/ [3] http://jrandom.dev.i2p/ [4] http://freshmeat.net/projects/suck/ [5] http://freshmeat.net/projects/slrn/

* 3) tech proposals

Orion và những người khác đã đăng một loạt RFC về các vấn đề kỹ thuật khác nhau lên wiki của ugha [6] để giúp làm rõ một số vấn đề khó hơn ở cấp độ client và app. Vui lòng dùng đó làm nơi để thảo luận về các vấn đề đặt tên, các cập nhật cho SAM, các ý tưởng về swarming (mô hình swarm trong P2P), và các chủ đề tương tự - khi bạn đăng ở đó, tất cả chúng ta có thể cùng cộng tác tại nơi của chính chúng ta để đạt kết quả tốt hơn.

[6] http://ugha.i2p/I2pRfc

* 4) ???

Đó là tất cả những gì tôi có lúc này (cũng may, vì cuộc họp sắp bắt đầu).  Như mọi khi, hãy chia sẻ ý kiến của bạn bất cứ lúc nào, ở bất cứ đâu :)

=jr
