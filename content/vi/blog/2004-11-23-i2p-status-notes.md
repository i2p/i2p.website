---
title: "Ghi chú trạng thái I2P cho ngày 2004-11-23"
date: 2004-11-23
author: "jr"
description: "Bản cập nhật tình hình I2P hàng tuần về khôi phục mạng, tiến độ kiểm thử thư viện streaming, kế hoạch phát hành 0.4.2 sắp tới, và các cải tiến addressbook (sổ địa chỉ)"
categories: ["status"]
---

Chào mọi người, đến lúc cập nhật tình hình

## Chỉ mục:

1. Net status
2. Streaming lib
3. 0.4.2
4. Addressbook.py 0.3.1
5. ???

## 1) Trạng thái mạng

Sau đợt 2-3 ngày tuần trước khi mọi thứ khá tắc nghẽn, mạng đã trở lại bình thường (có lẽ vì chúng tôi đã ngừng kiểm thử chịu tải cổng BitTorrent ;). Kể từ đó mạng hoạt động khá ổn định - chúng tôi thực sự có vài router đã chạy liên tục 30-40+ ngày, nhưng các kết nối IRC thỉnh thoảng vẫn có vài trục trặc. Mặt khác...

## 2) Streaming lib (thư viện truyền luồng)

Trong khoảng một tuần trở lại đây, chúng tôi đã tăng cường thử nghiệm trực tiếp thư viện streaming trên mạng và mọi thứ trông khá ổn. Duck đã dựng một tunnel bằng nó để mọi người có thể truy cập máy chủ IRC của anh ấy, và trong vài ngày, tôi chỉ gặp hai lần ngắt kết nối không cần thiết (điều này giúp chúng tôi lần ra một vài lỗi). Chúng tôi cũng có một instance i2ptunnel trỏ đến một squid outproxy (proxy thoát ra Internet công cộng) mà mọi người đã dùng thử, và thông lượng, độ trễ, cũng như độ tin cậy đều được cải thiện đáng kể so với thư viện cũ, mà chúng tôi đã chạy song song.

Nhìn chung, streaming lib (thư viện truyền luồng) có vẻ đã đủ ổn cho bản phát hành đầu tiên. Vẫn còn một vài hạng mục chưa hoàn tất, nhưng đó là một cải tiến đáng kể so với lib cũ, và chúng tôi cũng phải để dành cho bạn một lý do để nâng cấp về sau, đúng không? ;)

Thực ra, chỉ để trêu bạn (hoặc có lẽ để truyền cảm hứng cho bạn nghĩ ra vài giải pháp), những việc chính mà tôi thấy sắp tới cho streaming lib (thư viện streaming) là: - một vài thuật toán để chia sẻ thông tin tắc nghẽn và RTT giữa các luồng (theo từng destination (đích trong I2P) mục tiêu? theo từng destination nguồn? cho tất cả các destination cục bộ?) - tối ưu thêm cho các luồng tương tác (phần lớn trọng tâm trong triển khai hiện tại là các luồng truyền tải lớn) - sử dụng rõ ràng hơn các tính năng mới của streaming lib trong I2PTunnel, giảm chi phí phụ trội trên mỗi tunnel. - giới hạn băng thông ở cấp độ máy khách (theo một hoặc cả hai chiều trên một luồng, hoặc có thể chia sẻ giữa nhiều luồng). Điều này dĩ nhiên sẽ bổ sung bên cạnh cơ chế giới hạn băng thông tổng thể của router. - nhiều cơ chế để các destination giới hạn số lượng luồng mà họ chấp nhận hoặc tạo ra (chúng tôi có một số mã cơ bản, nhưng phần lớn đang bị vô hiệu hóa) - các danh sách kiểm soát truy cập (chỉ cho phép các luồng đến hoặc đi từ một số destination đã biết khác) - các điều khiển qua web và giám sát tình trạng của các luồng khác nhau, cũng như khả năng đóng hoặc giới hạn chúng một cách tường minh

Chắc là mọi người cũng có thể nghĩ ra vài thứ khác nữa, nhưng đó chỉ là một danh sách ngắn những thứ tôi rất muốn thấy trong streaming lib (thư viện truyền phát), nhưng tôi sẽ không vì chúng mà trì hoãn bản phát hành 0.4.2. Nếu ai quan tâm đến bất kỳ mục nào trong số đó, làm ơn cho tôi biết nhé!

## 3) 0.4.2

Vậy, nếu streaming lib (thư viện truyền phát) ở trạng thái tốt, khi nào chúng ta sẽ có bản phát hành? Kế hoạch hiện tại là phát hành trước cuối tuần này, thậm chí có thể sớm nhất là ngày mai. Còn một vài việc khác đang diễn ra mà tôi muốn xử lý xong trước, và dĩ nhiên những việc đó cần phải được kiểm thử, v.v. v.v.

Thay đổi lớn trong bản phát hành 0.4.2 dĩ nhiên sẽ là thư viện streaming mới. Xét về góc độ API, nó giống hệt thư viện cũ - I2PTunnel và các luồng SAM tự động sử dụng nó, nhưng ở cấp độ gói tin, nó *không* tương thích ngược. Điều này đặt chúng tôi vào một tình thế tiến thoái lưỡng nan thú vị - không có điều gì trong I2P buộc chúng tôi phải biến 0.4.2 thành một bản nâng cấp bắt buộc, tuy nhiên những người không nâng cấp sẽ không thể sử dụng I2PTunnel - không eepsites(I2P Sites), không IRC, không outproxy, không email. Tôi không muốn làm người dùng lâu năm xa lánh bằng cách buộc họ phải nâng cấp, nhưng tôi cũng không muốn làm họ xa lánh khi mọi thứ hữu ích đều hỏng ;)

Tôi sẵn sàng được thuyết phục theo hướng nào cũng được — chỉ cần sửa một dòng mã là đủ để bản phát hành 0.4.2 không giao tiếp với các bản cũ, hoặc chúng ta cứ để nguyên và để mọi người nâng cấp khi họ lên trang web hoặc diễn đàn để than phiền ầm ĩ rằng mọi thứ bị hỏng hết. Mọi người nghĩ sao?

## 4) AddressBook.py 0.3.1

Ragnarok vừa phát hành một bản phát hành vá lỗi mới cho ứng dụng sổ địa chỉ của anh ấy - xem `http://ragnarok.i2p/` để biết thêm thông tin (hoặc có lẽ anh ấy có thể cung cấp cho chúng ta một bản cập nhật trong cuộc họp?)

## 5) ???

Tôi biết còn nhiều hoạt động khác đang diễn ra - với cổng bittorrent, susimail, dịch vụ lưu trữ mới của slacker, và nhiều thứ khác. Có ai còn điều gì muốn nêu ra không? Nếu có, ghé qua buổi họp trong khoảng 30 phút nữa tại #i2p trên các máy chủ IRC quen thuộc!

=jr
