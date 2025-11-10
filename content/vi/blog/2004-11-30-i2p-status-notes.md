---
title: "Ghi chú trạng thái I2P cho ngày 2004-11-30"
date: 2004-11-30
author: "jr"
description: "Cập nhật tình hình I2P hàng tuần bao gồm các bản phát hành 0.4.2 và 0.4.2.1, những phát triển mới tại mail.i2p, tiến độ i2p-bt, và các cuộc thảo luận về bảo mật eepsite"
categories: ["status"]
---

Chào mọi người

## Chỉ mục

1. 0.4.2 and 0.4.2.1
2. mail.i2p
3. i2p-bt
4. eepsites(I2P Sites)
5. ???

## 1) 0.4.2 và 0.4.2.1

Kể từ khi chúng tôi cuối cùng cũng phát hành 0.4.2, độ tin cậy và thông lượng của mạng đã tăng vọt trong một thời gian, cho đến khi chúng tôi đụng phải những lỗi hoàn toàn mới do chính mình tạo ra. Kết nối IRC đối với hầu hết mọi người duy trì hàng giờ liền, nhưng với một số người gặp phải một vài sự cố, trải nghiệm không mấy suôn sẻ. Tuy vậy đã có hàng loạt bản sửa lỗi, và tối nay muộn hoặc sáng sớm mai chúng tôi sẽ có bản phát hành 0.4.2.1 mới sẵn sàng để tải về.

## 2) mail.i2p

Hồi sớm nay postman gửi cho tôi một lời nhắn nói rằng anh ấy có vài điều muốn thảo luận - để biết thêm thông tin, xem nhật ký cuộc họp (hoặc nếu bạn đọc điều này trước cuộc họp, ghé qua nhé).

## 3) i2p-bt

Một trong những nhược điểm của bản phát hành mới là chúng tôi đang gặp một số trục trặc với bản port i2p-bt. Một số vấn đề đã được xác định, tìm thấy và sửa trong streaming lib (thư viện streaming), nhưng vẫn cần làm thêm để đưa nó tới mức độ như chúng tôi cần.

## 4) eepsites(Trang web I2P)

Trong những tháng qua đã có một số thảo luận trên danh sách thư, trong kênh và trên diễn đàn về một số vấn đề liên quan đến cách eepsites(I2P Sites) và eepproxy hoạt động - gần đây có người đã đề cập đến các vấn đề về cách và những header HTTP nào được lọc, những người khác nêu lên các nguy cơ từ các trình duyệt cấu hình kém, và còn có cả trang của DrWoo tóm tắt nhiều rủi ro. Một điều đặc biệt đáng chú ý là thực tế có người đang tích cực phát triển các applet sẽ chiếm quyền điều khiển máy tính của người dùng nếu họ không vô hiệu hóa các applet. (VÌ VẬY HÃY TẮT JAVA VÀ JAVASCRIPT TRONG TRÌNH DUYỆT CỦA BẠN)

Điều này, dĩ nhiên, dẫn đến một cuộc thảo luận về cách chúng ta có thể bảo mật mọi thứ. Tôi đã nghe những đề xuất về việc tự xây dựng một trình duyệt hoặc đóng gói kèm một trình duyệt với các cài đặt bảo mật được cấu hình sẵn, nhưng hãy thực tế - đó là khối lượng công việc lớn hơn nhiều so với những gì bất kỳ ai ở đây sẽ sẵn sàng đảm nhận. Tuy nhiên, còn có ba trường phái khác:

1. Use a fascist HTML filter and tie it in with the proxy
2. Use a fascist HTML filter as part of a script that fetches pages for you
3. Use a secure macro language

Phương án đầu tiên về cơ bản giống như hiện nay, ngoại trừ việc chúng ta lọc nội dung được hiển thị thông qua thứ gì đó như muffin hoặc bộ lọc ẩn danh của freenet. Nhược điểm ở đây là nó vẫn để lộ các header HTTP, vì vậy chúng ta cũng sẽ phải ẩn danh hóa phần HTTP.

Phương án thứ hai khá giống như bạn có thể thấy trên `http://duck.i2p/` với CGIproxy, hoặc, thay vào đó, như bạn có thể thấy trong fproxy của Freenet. Cách này cũng đảm nhiệm luôn phần HTTP.

Phương án thứ ba có cả ưu điểm lẫn nhược điểm - nó cho phép chúng ta sử dụng các giao diện hấp dẫn hơn nhiều (vì chúng ta có thể an toàn sử dụng một số javascript đã biết là an toàn, v.v.), nhưng lại có nhược điểm là không tương thích ngược. Có lẽ nên hợp nhất điều này với một bộ lọc, cho phép bạn nhúng các macro vào html đã được lọc?

Dù sao đi nữa, đây là một nỗ lực phát triển quan trọng và nhằm giải quyết một trong những ứng dụng hấp dẫn nhất của I2P - các trang web tương tác an toàn và ẩn danh. Có lẽ ai đó có những ý tưởng khác hoặc thông tin về cách chúng ta có thể đạt được điều chúng ta cần?

## 5) ???

Được rồi, tôi sắp trễ buổi họp, nên có lẽ tôi nên ký vào cái này rồi gửi đi, nhỉ?

=jr [để xem tôi có làm cho gpg hoạt động đúng cách không...]
