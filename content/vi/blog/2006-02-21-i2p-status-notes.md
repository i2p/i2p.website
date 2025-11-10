---
title: "Ghi chú trạng thái I2P cho ngày 2006-02-21"
date: 2006-02-21
author: "jr"
description: "Network issues with 0.6.1.10 release, quick 0.6.1.11 follow-up release, and IE security concerns"
categories: ["status"]
---

Chào mọi người, lại là thứ Ba nữa rồi

* Index

1) Trạng thái mạng 2) ???

* 1) Net status

Mạng lưới đã gặp khá nhiều trục trặc với bản phát hành 0.6.1.10, một phần do không tương thích ngược, nhưng cũng do các lỗi không lường trước. Cả độ tin cậy lẫn thời gian hoạt động trên 0.6.1.10 đều không đạt yêu cầu, vì vậy trong 5 ngày qua đã có một loạt bản vá dồn dập, và đỉnh điểm là bản phát hành 0.6.1.11 mới - http://dev.i2p.net/pipermail/i2p/2006-February/001263.html

Phần lớn các lỗi được phát hiện trong 0.6.1.10 đã tồn tại từ bản phát hành 0.6 vào tháng 9 năm ngoái, nhưng không dễ nhận thấy khi vẫn còn các transport thay thế để dự phòng (TCP). Mạng kiểm thử cục bộ của tôi mô phỏng lỗi gói tin, nhưng thực sự không bao quát được router churn (biến động router) và các dạng sự cố mạng dai dẳng khác. Mạng kiểm thử _PRE cũng bao gồm một tập các peer (nút ngang hàng) khá tin cậy do chúng tôi tự chọn, nên có nhiều tình huống quan trọng chưa được khám phá đầy đủ trước khi phát hành chính thức. Đó rõ ràng là một vấn đề, và lần tới chúng tôi sẽ bảo đảm đưa vào một tập hợp kịch bản rộng hơn.

* 2) ???

Hiện tại có khá nhiều việc đang diễn ra, nhưng bản phát hành 0.6.1.11 mới đã được đưa lên đầu danh sách ưu tiên. Mạng sẽ tiếp tục hơi không ổn định cho đến khi một lượng lớn người dùng cập nhật xong, sau đó công việc sẽ tiếp tục tiến triển. Một điều đáng nhắc đến là cervantes đang nghiên cứu một dạng kỹ thuật khai thác (exploit) liên quan đến miền bảo mật của IE, và dù tôi không chắc anh ấy đã sẵn sàng giải thích chi tiết hay chưa, các kết quả sơ bộ cho thấy nó khả thi, vì vậy những ai coi trọng tính ẩn danh nên tránh dùng IE trong lúc này (nhưng bạn cũng biết điều đó rồi ;). Có lẽ cervantes có thể cho chúng ta một bản tóm tắt trong cuộc họp?

Dù sao thì, lúc này tôi chỉ có bấy nhiêu muốn nói - vài phút nữa ghé qua buổi họp để chào một tiếng nhé!

=jr
