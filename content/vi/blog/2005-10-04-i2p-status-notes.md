---
title: "Ghi chú trạng thái I2P cho ngày 2005-10-04"
date: 2005-10-04
author: "jr"
description: "Cập nhật hàng tuần bao gồm thành công của bản phát hành 0.6.1.1 với 3–400 peers (nút ngang hàng), nỗ lực hợp nhất các fork (nhánh tách) của i2phex, và tiến độ tự động hóa của Syndie với pet names (tên thân mật) và các pull (kéo) được lập lịch"
categories: ["status"]
---

Chào mọi người, đến giờ cho bản ghi chú tình hình hàng tuần của chúng ta (chèn tiếng hoan hô ở đây)

* Index

1) 0.6.1.1 2) i2phex 3) syndie 4) ???

* 1) 0.6.1.1

Như đã thông báo trên các kênh quen thuộc, 0.6.1.1 đã phát hành cách đây vài ngày, và cho đến nay các phản hồi đều tích cực. Mạng đã tăng lên ổn định khoảng 3-400 nút (peer) đã biết, và hiệu năng khá tốt, dù mức sử dụng CPU có tăng nhẹ. Điều này có lẽ là do những lỗi tồn tại từ lâu cho phép chấp nhận nhầm các địa chỉ IP không hợp lệ, kéo theo churn (mức biến động các nút tham gia/rời mạng) cao hơn mức cần thiết. Đã có các bản vá cho vấn đề này và những mục khác trong các bản dựng CVS kể từ 0.6.1.1, vì vậy nhiều khả năng chúng tôi sẽ có 0.6.1.2 trong tuần này.

* 2) i2phex

Trong khi một số người có thể đã chú ý đến các cuộc thảo luận trên nhiều diễn đàn về i2phex và fork (tách nhánh) của legion, đã có thêm trao đổi giữa tôi và legion, và chúng tôi đang làm việc để hợp nhất hai dự án lại với nhau. Sẽ có thêm thông tin về việc này khi có.

Ngoài ra, redzara đang miệt mài làm việc để hợp nhất i2phex với bản phát hành phex hiện tại, và striker đã đưa ra thêm một số cải tiến, vì vậy sẽ có một số điều thú vị sắp tới.

* 3) syndie

Ragnarok đã miệt mài làm việc trên syndie vài ngày gần đây, tích hợp cơ sở dữ liệu "pet name" (tên thân thiện do người dùng đặt) của syndie với cơ sở dữ liệu của router, đồng thời tự động hóa việc phân phối bằng các lần lấy theo lịch trình từ những kho lưu trữ từ xa được chọn. Phần tự động hóa đã xong, và dù vẫn còn một chút việc về giao diện người dùng, mọi thứ đang ở trạng thái khá tốt!

* 4) ???

Dạo này còn nhiều việc khác đang diễn ra nữa, bao gồm cả một số công việc liên quan đến bộ tài liệu giới thiệu kỹ thuật mới, di chuyển irc và làm mới trang web. Nếu ai có điều gì muốn nêu ra, hãy ghé qua cuộc họp trong vài phút nữa và chào một tiếng nhé!

=jr
