---
title: "Ghi chú trạng thái I2P ngày 2006-05-09"
date: 2006-05-09
author: "jr"
description: "Bản phát hành 0.6.1.18 với các cải tiến về độ ổn định mạng, máy chủ phát triển mới 'baz', và các thách thức về khả năng tương thích GCJ trên Windows"
categories: ["status"]
---

Chào mọi người, lại đến thứ Ba nữa rồi

* Index

1) Trạng thái mạng và 0.6.1.18 2) baz 3) ???

* 1) Net status and 0.6.1.18

Sau thêm một tuần thử nghiệm và tinh chỉnh, chúng tôi đã phát hành một phiên bản mới vào đầu giờ chiều nay, giúp chúng tôi chuyển sang một môi trường ổn định hơn để từ đó tiếp tục cải tiến. Tuy nhiên, có lẽ chúng ta sẽ chưa thấy nhiều tác động cho đến khi nó được triển khai rộng rãi, vì vậy có thể chúng ta sẽ phải đợi vài ngày để xem tình hình thế nào, nhưng dĩ nhiên việc đo đạc sẽ vẫn tiếp tục.

Một khía cạnh của các bản dựng và phát hành mới nhất mà zzz gần đây có nêu là việc tăng số lượng các tunnel dự phòng hiện có thể tạo tác động đáng kể khi thực hiện đồng thời với việc giảm số lượng các tunnel song song. Chúng tôi không tạo lease (bản ghi tham chiếu đường hầm trong leaseSet) mới cho đến khi có đủ số lượng các tunnel đang hoạt động, vì vậy các tunnel dự phòng có thể được triển khai nhanh chóng nếu một tunnel đang hoạt động gặp sự cố, qua đó giảm tần suất máy khách rơi vào trạng thái không có lease đang hoạt động. Tuy nhiên, đây chỉ là một tinh chỉnh đối với triệu chứng, và bản phát hành mới nhất sẽ giúp giải quyết nguyên nhân gốc rễ.

* 2) baz

"baz", chiếc máy mới mà bar tặng cuối cùng cũng đã tới, một laptop amd64 turion (với winxp trên đĩa khởi động, và vài hệ điều hành khác đang dự trù thông qua các ổ đĩa gắn ngoài). Tôi cũng đã mày mò với nó vài ngày qua, cố gắng thử nghiệm vài ý tưởng triển khai trên đó. Một vấn đề tôi đang gặp phải là làm cho gcj hoạt động trên windows. Cụ thể hơn, một gcj với gnu/classpath hiện đại. Tuy nhiên, theo lời đồn thì khá tiêu cực - nó có thể được biên dịch bản địa trong mingw hoặc biên dịch chéo từ linux, nhưng lại gặp các vấn đề như lỗi phân đoạn (segfault) bất cứ khi nào một ngoại lệ vượt qua ranh giới dll. Vì vậy, chẳng hạn, nếu java.io.File (nằm trong libgcj.dll) ném ra một ngoại lệ, nếu nó được bắt bởi thứ gì đó trong net.i2p.* (nằm trong libi2p.dll hoặc i2p.exe), *poof*, thế là ứng dụng sập.

Ừ thì, trông không mấy khả quan. Những người bên gcj sẽ rất quan tâm nếu có ai có thể tham gia và hỗ trợ phần phát triển win32, nhưng có vẻ việc hỗ trợ khả thi chưa diễn ra trong tương lai gần. Vậy có lẽ chúng ta sẽ phải dự tính tiếp tục dùng sun jvm (máy ảo Java) trên Windows, đồng thời hỗ trợ gcj/kaffe/sun/ibm/etc trên *nix (các hệ điều hành kiểu Unix). Tôi nghĩ thế cũng không tệ lắm, vì chính người dùng *nix mới gặp vấn đề trong việc đóng gói và phân phối các JVM.

* 3) ???

Ok, tôi đã trễ cuộc họp rồi, nên tôi cần kết thúc ở đây và chuyển qua tab irc, tôi đoán vậy... hẹn gặp lại trong ít phút ;)

=jr
