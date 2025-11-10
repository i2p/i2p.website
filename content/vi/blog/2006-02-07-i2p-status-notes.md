---
title: "Ghi chú trạng thái I2P ngày 2006-02-07"
date: 2006-02-07
author: "jr"
description: "Tiến độ thử nghiệm mạng PRE, tối ưu hóa số mũ ngắn cho mã hóa ElGamal, và I2Phex 0.1.1.37 với hỗ trợ gwebcache"
categories: ["status"]
---

Chào mọi người, lại đến thứ Ba rồi

* Index

1) Trạng thái mạng
2) _PRE tiến độ mạng
3) I2Phex 0.1.1.37
4) ???

* 1) Net status

Trong tuần vừa qua không có thay đổi đáng kể nào trên mạng chính, vì vậy trạng thái mạng chính cũng không thay đổi nhiều.  Mặt khác...

* 2) _PRE net progress

Tuần trước tôi bắt đầu commit mã không tương thích ngược cho bản phát hành 0.6.1.10 vào một nhánh riêng trong CVS (i2p_0_6_1_10_PRE), và một nhóm tình nguyện viên đã giúp kiểm thử.

Mạng _PRE mới này không thể liên lạc với mạng đang hoạt động, và không có mức ẩn danh đáng kể (vì chỉ có dưới 10 nút). Với các nhật ký pen register (ghi nhận điểm đích kết nối) từ các routers đó, một vài lỗi nghiêm trọng trong cả mã mới và mã cũ đã được truy ra và sửa, tuy nhiên việc kiểm thử và cải tiến vẫn đang tiếp tục.

Một khía cạnh của cơ chế mật mã khi tạo tunnel mới là bên tạo phải thực hiện mã hóa bất đối xứng tốn kém cho mỗi hop (chặng) ngay từ đầu, trong khi việc tạo tunnel kiểu cũ chỉ mã hóa nếu hop trước đồng ý tham gia vào tunnel. Việc mã hóa này có thể mất 400-1000ms hoặc hơn, phụ thuộc cả vào hiệu năng CPU cục bộ lẫn độ dài tunnel (nó thực hiện một lần mã hóa ElGamal đầy đủ cho mỗi hop). Một tối ưu hóa hiện đang được sử dụng trên _PRE net là dùng số mũ ngắn [1] - thay vì dùng 'x' 2048bit làm khóa ElGamal, chúng tôi dùng 'x' 228bit, đây là độ dài được khuyến nghị để tương ứng với độ khó của bài toán logarit rời rạc. Điều này đã làm giảm thời gian mã hóa cho mỗi hop đi một bậc độ lớn, dù không ảnh hưởng đến thời gian giải mã.

Có nhiều quan điểm trái chiều về việc sử dụng số mũ ngắn; trong trường hợp tổng quát thì điều đó không an toàn. Tuy nhiên, theo những gì tôi thu thập được, vì chúng tôi dùng một số nguyên tố an toàn cố định (Oakley group 14 [2]), nên bậc của q có lẽ vẫn ổn. Nếu ai có thêm ý kiến theo hướng này, tôi rất muốn nghe thêm.

Một phương án lớn là chuyển sang mã hóa 1024bit (trong đó có lẽ chúng ta có thể dùng một số mũ ngắn 160bit). Điều này có thể phù hợp dù thế nào đi nữa, và nếu mọi thứ quá khó khăn với mã hóa 2048bit trên _PRE net, chúng ta có thể thực hiện bước chuyển ngay trong _PRE net. Nếu không, chúng ta có thể đợi đến bản phát hành 0.6.1.10, khi thuật toán mật mã mới được triển khai rộng rãi hơn để xem liệu điều đó có cần thiết không. Sẽ có thêm nhiều thông tin nếu việc chuyển đổi như vậy có vẻ sắp diễn ra.

[1] "Về thỏa thuận khóa Diffie-Hellman với số mũ ngắn" -     van Oorschot, Weiner tại EuroCrypt 96.  bản sao tại     http://dev.i2p.net/~jrandom/Euro96-DH.ps [2] http://www.ietf.org/rfc/rfc3526.txt

Dù sao thì, đã có rất nhiều tiến triển trên _PRE net, với hầu hết trao đổi về nó diễn ra trong kênh #i2p_pre trên irc2p.

* 3) I2Phex 0.1.1.37

Complication đã hợp nhất và vá mã I2Phex mới nhất để hỗ trợ gwebcaches, tương thích với bản port pycache của Rawn. Điều này có nghĩa là người dùng có thể tải I2Phex, cài đặt, bấm "Connect to the network", và sau khoảng một đến hai phút, nó sẽ lấy một số tham chiếu đến các I2Phex peer (nút ngang hàng) hiện có và tham gia mạng. Không còn phiền toái phải quản lý thủ công các tệp i2phex.hosts, hoặc chia sẻ khóa thủ công nữa (w00t)! Mặc định có hai gwebcaches, nhưng bạn có thể thay đổi hoặc thêm cái thứ ba bằng cách sửa các thuộc tính i2pGWebCache0, i2pGWebCache1, hoặc i2pGWebCache2 trong i2phex.cfg.

Làm tốt lắm, Complication và Rawn!

* 4) ???

Tạm thời thì vậy thôi, mà như vậy cũng tốt, vì tôi đã trễ giờ họp rồi :)  Hẹn gặp mọi người ở #i2p trong chốc lát

=jr
