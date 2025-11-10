---
title: "Ghi chú trạng thái I2P cho ngày 2004-11-16"
date: 2004-11-16
author: "jr"
description: "Cập nhật tình hình I2P hàng tuần bao gồm các vấn đề tắc nghẽn mạng, các cải tiến trong streaming library (thư viện truyền phát), tiến độ BitTorrent và các kế hoạch phát hành sắp tới"
categories: ["status"]
---

Chào mọi người, lại là thứ Ba rồi

## Mục lục

1. Congestion
2. Streaming
3. BT
4. ???

## 1) Tắc nghẽn

Tôi biết, tôi đang phá vỡ thói quen đặt tên mục 1 là "Net status", nhưng tuần này thì "congestion" có vẻ phù hợp hơn. Bản thân mạng đã hoạt động khá tốt, nhưng khi việc sử dụng BitTorrent tăng lên, mọi thứ bắt đầu ngày càng bị tắc nghẽn, dẫn đến một tình trạng sụp đổ do tắc nghẽn đúng nghĩa.

Điều này nằm trong dự liệu và chỉ càng củng cố kế hoạch của chúng ta — phát hành thư viện streaming mới và cải tổ việc quản lý tunnel để chúng ta có đủ dữ liệu về các peer (nút ngang hàng) khác để dùng khi các peer nhanh của chúng ta gặp lỗi. Có một số yếu tố khác cũng góp phần vào các sự cố mạng gần đây, nhưng phần lớn có thể truy nguyên tới sự gia tăng tắc nghẽn và các lỗi tunnel phát sinh (mà đến lượt nó lại gây ra đủ kiểu lựa chọn peer hỗn loạn).

## 2) Truyền theo luồng

Đã có nhiều tiến bộ với streaming lib (thư viện streaming), và tôi đã dựng một proxy squid nối vào nó qua mạng thật, mà tôi thường xuyên dùng cho việc duyệt web hằng ngày. Với sự giúp đỡ của mule, chúng tôi cũng đã ép các luồng hoạt động rất căng bằng cách đẩy frost và FUQID qua mạng (trời ơi, trước đây tôi không hề nhận ra frost gây tải khủng khiếp đến thế!). Bằng cách đó, chúng tôi đã lần ra được vài lỗi nghiêm trọng tồn tại từ lâu, và đã thêm một số tinh chỉnh để giúp kiểm soát số lượng kết nối cực lớn.

Các luồng dữ liệu khối lượng lớn cũng hoạt động rất tốt, với cả khởi động chậm và tránh tắc nghẽn, và các kết nối gửi/phản hồi nhanh (kiểu HTTP get+response) đang làm đúng như những gì chúng cần làm.

Tôi kỳ vọng chúng tôi sẽ huy động vài tình nguyện viên để thử triển khai thêm trong vài ngày tới, và hy vọng sớm đưa chúng ta lên phiên bản 0.4.2. Tôi không muốn nói rằng nó sẽ tốt đến mức rửa bát hộ bạn, và tôi chắc chắn sẽ vẫn có những lỗi lọt qua, nhưng nhìn chung thì có vẻ rất hứa hẹn.

## 3) BT

Trừ những trục trặc mạng gần đây, bản port i2p-bt đã tiến bộ vượt bậc. Tôi biết có vài người đã tải xuống hơn 1 GB dữ liệu qua nó, và hiệu năng đúng như kỳ vọng (do thư viện streaming cũ, ~4KBps mỗi peer (nút ngang hàng) trong swarm (đám người tham gia chia sẻ)). Tôi cố gắng lắng nghe công việc đang được thảo luận trong kênh #i2p-bt - có lẽ duck có thể đưa ra một bản tóm tắt trong cuộc họp?

## 4) ???

Tạm thời tôi chỉ có vậy. Hẹn gặp mọi người ở cuộc họp trong vài phút nữa.

=jr
