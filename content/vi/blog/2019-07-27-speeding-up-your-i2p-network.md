---
title: "Tăng tốc mạng I2P của bạn"
date: 2019-07-27
author: "mhatta"
description: "Tăng tốc mạng I2P của bạn"
categories: ["tutorial"]
---

*Bài viết này được biên soạn lại trực tiếp từ tài liệu ban đầu được tạo cho* [blog Medium](https://medium.com/@mhatta/speeding-up-your-i2p-network-c08ec9de225d) *của mhatta.* *Anh ấy xứng đáng được ghi nhận công lao cho bài đăng gốc. Nội dung này đã được cập nhật ở một số chỗ nơi* *nó đề cập đến các phiên bản I2P cũ như thể là phiên bản hiện hành và đã trải qua một vài* *chỉnh sửa nhẹ. -idk*

Right after it starts up, I2P is often seen as a little bit slow. It's true, and we all know why, by nature, [garlic routing](https://en.wikipedia.org/wiki/Garlic_routing) adds overhead to the familiar experience of using the internet so that you can have privacy, but this means that for many or most I2P services, your data will need to go through 12 hops by default.

![Phân tích các công cụ phục vụ ẩn danh trực tuyến](https://www.researchgate.net/publication/289531182_An_analysis_of_tools_for_online_anonymity)

Ngoài ra, khác với Tor, I2P chủ yếu được thiết kế như một mạng khép kín. Bạn có thể dễ dàng truy cập [eepsites](https://medium.com/@mhatta/how-to-set-up-untraceable-websites-eepsites-on-i2p-1fe26069271d) hoặc các tài nguyên khác bên trong I2P, nhưng không nên truy cập các trang web [clearnet](https://en.wikipedia.org/wiki/Clearnet_(networking)) (Internet công khai) thông qua I2P. Có một số "outproxies" của I2P (proxy thoát) tương tự các nút thoát của [Tor](https://en.wikipedia.org/wiki/Tor_(anonymity_network)) để truy cập clearnet, nhưng phần lớn chúng rất chậm vì đi ra clearnet thực chất là *một bước nhảy nữa* trong kết nối vốn đã có 6 bước nhảy vào và 6 bước nhảy ra.

Cho đến cách đây vài phiên bản, vấn đề này còn khó xử lý hơn vì nhiều người dùng router I2P gặp khó khăn khi cấu hình các thiết lập băng thông cho router của họ. Nếu tất cả những ai có thể dành thời gian điều chỉnh đúng cách các thiết lập băng thông của mình, thì điều đó sẽ cải thiện không chỉ kết nối của bạn mà còn cả toàn bộ mạng I2P.

## Điều chỉnh giới hạn băng thông

Vì I2P là một mạng ngang hàng (peer-to-peer), bạn phải chia sẻ một phần băng thông mạng của mình với các nút khác. Bạn có thể chọn mức bao nhiêu trong "I2P Bandwidth Configuration" (nút "Configure Bandwidth" trong phần "Applications and Configuration" của I2P Router Console, hoặc http://localhost:7657/config).

![Cấu hình băng thông I2P](https://geti2p.net/images/blog/bandwidthmenu.png)

Nếu bạn thấy giới hạn băng thông chia sẻ là 48 KBps, mức này rất thấp, thì có thể bạn chưa điều chỉnh băng thông chia sẻ khỏi giá trị mặc định. Như tác giả gốc của tài liệu mà bài viết blog này dựa theo đã lưu ý, I2P có một giới hạn băng thông chia sẻ mặc định rất thấp cho đến khi người dùng điều chỉnh nó, nhằm tránh gây ra vấn đề cho kết nối của người dùng.

Tuy nhiên, vì nhiều người dùng có thể không biết chính xác cần điều chỉnh những thiết lập băng thông nào, [bản phát hành I2P 0.9.38](https://geti2p.net/en/download) đã giới thiệu một trình hướng dẫn cài đặt mới. Nó bao gồm một bài kiểm tra băng thông, tự động phát hiện (nhờ [NDT](https://www.measurementlab.net/tests/ndt/) của M-Lab) và điều chỉnh các thiết lập băng thông của I2P cho phù hợp.

Nếu bạn muốn chạy lại trình hướng dẫn, chẳng hạn sau khi thay đổi nhà cung cấp dịch vụ của mình hoặc vì bạn đã cài đặt I2P trước phiên bản 0.9.38, bạn có thể khởi chạy lại trình hướng dẫn từ liên kết 'Setup' trên trang 'Help & FAQ', hoặc đơn giản là truy cập trực tiếp trình hướng dẫn tại http://localhost:7657/welcome

![Bạn có tìm thấy "Setup" không?](https://geti2p.net/images/blog/sidemenu.png)

Việc sử dụng Trình hướng dẫn (Wizard) rất đơn giản, chỉ cần tiếp tục bấm "Next". Đôi khi các máy chủ đo lường mà M-Lab đã chọn bị ngừng hoạt động và bài kiểm tra sẽ thất bại. Trong trường hợp đó, bấm "Previous" (không dùng nút "back" của trình duyệt web của bạn), rồi thử lại.

![Kết quả kiểm tra băng thông](https://geti2p.net/images/blog/bwresults.png)

## Chạy I2P liên tục

Ngay cả sau khi đã điều chỉnh băng thông, kết nối của bạn vẫn có thể chậm. Như đã nói, I2P là một mạng P2P. Sẽ cần một khoảng thời gian để I2P router của bạn được các nút đồng đẳng khác phát hiện và tích hợp vào mạng I2P. Nếu router của bạn không hoạt động đủ lâu để được tích hợp tốt, hoặc nếu bạn thường xuyên tắt nó không đúng cách, thì mạng sẽ vẫn khá chậm. Ngược lại, càng để I2P router của bạn chạy liên tục lâu hơn, kết nối của bạn sẽ càng nhanh và ổn định hơn, và phần băng thông bạn chia sẻ sẽ được sử dụng nhiều hơn trong mạng.

Tuy nhiên, nhiều người có thể không duy trì được I2P router luôn hoạt động. Trong trường hợp đó, bạn vẫn có thể chạy I2P router trên một máy chủ từ xa như VPS, rồi sử dụng chuyển tiếp cổng qua SSH.
