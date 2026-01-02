---
title: "20 năm bảo vệ quyền riêng tư: Lược sử I2P"
date: 2021-08-28
slug: "20-years-of-privacy-a-brief-history-of-i2p"
author: "sadie"
description: "Lịch sử của I2P như chúng ta biết"
categories: ["general"]
---

## Sự vô hình là biện pháp phòng thủ tốt nhất: xây dựng một internet trong lòng một internet

> "Tôi tin rằng hầu hết mọi người muốn công nghệ này để họ có thể tự do thể hiện bản thân. Đó là một cảm giác dễ chịu khi bạn biết mình có thể làm như vậy. Đồng thời, chúng ta có thể khắc phục một số vấn đề đang tồn tại trên Internet bằng cách thay đổi cách nhìn nhận về bảo mật và quyền riêng tư, cũng như mức độ mà người ta coi trọng chúng."

Vào tháng 10 năm 2001, 0x90 (Lance James) đã có một giấc mơ. Nó bắt đầu như một "mong muốn liên lạc tức thời với những người dùng Freenet khác để thảo luận về các vấn đề liên quan đến Freenet, và trao đổi các khóa Freenet đồng thời vẫn duy trì tính ẩn danh, quyền riêng tư và bảo mật." Nó được gọi là IIP — the Invisible IRC Project.

The Invisible IRC Project được xây dựng dựa trên lý tưởng và khuôn khổ đằng sau The InvisibleNet. Trong một cuộc phỏng vấn năm 2002, 0x90 mô tả dự án là tập trung vào "sự đổi mới trong công nghệ mạng thông minh" với mục tiêu "cung cấp các tiêu chuẩn cao nhất về bảo mật và quyền riêng tư trên Internet được sử dụng rộng rãi nhưng vốn nổi tiếng là không an toàn."

Tính đến năm 2003, đã có một số dự án tương tự khác được khởi động, lớn nhất là Freenet, GNUNet và Tor. Tất cả các dự án này đều có mục tiêu bao quát là mã hóa và ẩn danh nhiều loại lưu lượng mạng. Đối với IIP, rõ ràng chỉ riêng IRC không phải là một mục tiêu đủ lớn. Điều cần thiết là một lớp ẩn danh hóa cho mọi giao thức.

Vào đầu năm 2003, một nhà phát triển ẩn danh mới, "jrandom", đã tham gia dự án. Mục tiêu rõ ràng của người này là mở rộng phạm vi hoạt động của IIP. jrandom mong muốn viết lại mã nguồn nền tảng của IIP bằng Java và thiết kế lại các giao thức dựa trên các bài báo nghiên cứu gần đây và những quyết định thiết kế ban đầu mà Tor và Freenet đang đưa ra. Một số khái niệm như "onion routing" (định tuyến dạng onion) đã được điều chỉnh để trở thành "garlic routing" (định tuyến dạng garlic).

Vào cuối mùa hè năm 2003, jrandom đã tiếp quản dự án và đổi tên nó thành Invisible Internet Project (Dự án Internet Vô Hình), hay "I2P". Ông đã công bố một tài liệu phác thảo triết lý của dự án, và đặt các mục tiêu kỹ thuật cùng thiết kế của nó trong bối cảnh mixnets (mạng trộn) và các lớp ẩn danh. Ông cũng công bố đặc tả của hai giao thức (I2CP và I2NP) tạo thành nền tảng của mạng mà I2P sử dụng ngày nay.

Đến mùa thu năm 2003, I2P, Freenet và Tor đang phát triển nhanh chóng. jrandom đã phát hành I2P phiên bản 0.2 vào ngày 1 tháng 11 năm 2003 và tiếp tục phát hành các phiên bản với tần suất cao trong 3 năm tiếp theo.

Vào tháng 2 năm 2005, zzz cài đặt I2P lần đầu tiên. Đến mùa hè năm 2005, zzz đã thiết lập zzz.i2p và stats.i2p, những tài nguyên cốt lõi cho việc phát triển I2P. Vào tháng 7 năm 2005, jrandom phát hành phiên bản 0.6, bao gồm giao thức truyền tải SSU (Secure Semi-reliable UDP) mang tính đổi mới để khám phá IP và vượt qua tường lửa.

Từ cuối năm 2006 sang năm 2007, quá trình phát triển cốt lõi của I2P chậm lại đáng kể khi jrandom chuyển trọng tâm sang Syndie. Tháng 11 năm 2007, tai họa ập đến khi jrandom gửi một thông điệp bí ẩn rằng anh ấy sẽ phải tạm nghỉ trong một năm hoặc lâu hơn. Đáng tiếc, họ không bao giờ nghe tin từ jrandom nữa.

Giai đoạn thứ hai của thảm họa xảy ra vào ngày 13 tháng 1 năm 2008 khi nhà cung cấp dịch vụ lưu trữ cho gần như toàn bộ máy chủ i2p.net bị mất điện và đã không khôi phục hoạt động hoàn toàn. Complication, welterde và zzz đã nhanh chóng đưa ra các quyết định để đưa dự án hoạt động trở lại, chuyển sang i2p2.de và chuyển từ CVS sang monotone để quản lý mã nguồn.

Dự án nhận ra rằng mình đã phụ thuộc quá nhiều vào các tài nguyên tập trung. Những nỗ lực trong suốt năm 2008 đã phi tập trung hóa dự án và phân bổ vai trò cho nhiều người. Bắt đầu từ bản phát hành 0.7.6 vào ngày 31 tháng 7 năm 2009, zzz đã ký 49 bản phát hành tiếp theo.

Đến giữa năm 2009, zzz đã hiểu rõ mã nguồn hơn nhiều và xác định được nhiều vấn đề về khả năng mở rộng. Mạng lưới đã tăng trưởng nhờ cả khả năng ẩn danh và vượt kiểm duyệt. Tính năng cập nhật tự động trong mạng đã khả dụng.

Vào mùa Thu năm 2010, zzz tuyên bố tạm dừng phát triển I2P cho đến khi tài liệu trên trang web hoàn chỉnh và chính xác. Việc này kéo dài 3 tháng.

Bắt đầu từ năm 2010, zzz, ech, hottuna và các cộng tác viên khác tham dự CCC (Chaos Communications Congress) hằng năm cho đến khi các hạn chế do COVID được áp dụng. Dự án đã xây dựng cộng đồng và cùng nhau kỷ niệm các bản phát hành.

Vào năm 2013, Anoncoin ra đời như đồng tiền mã hóa đầu tiên có hỗ trợ I2P tích hợp sẵn, với các nhà phát triển như meeh cung cấp hạ tầng cho mạng I2P.

Vào năm 2014, str4d bắt đầu đóng góp cho I2PBote và tại Real World Crypto, các cuộc thảo luận về việc cập nhật hệ mật mã của I2P đã bắt đầu. Đến cuối năm 2014, phần lớn các thuật toán chữ ký số mới đã được hoàn thiện, bao gồm ECDSA và EdDSA.

Năm 2015, I2PCon diễn ra ở Toronto với các bài thuyết trình, sự hỗ trợ từ cộng đồng và những người tham dự đến từ Châu Mỹ và Châu Âu. Năm 2016 tại Real World Crypto Stanford, str4d đã có một bài nói về tiến độ của crypto migration (chuyển đổi thuật toán mật mã).

NTCP2 được triển khai vào năm 2018 (bản phát hành 0.9.36), cung cấp khả năng chống lại kiểm duyệt bằng DPI (Deep Packet Inspection - kiểm tra sâu gói tin) và giảm tải cho CPU nhờ mật mã hiện đại, nhanh hơn.

Năm 2019, nhóm đã tham dự nhiều hội nghị hơn, bao gồm DefCon và Monero Village, nhằm tiếp cận các nhà phát triển và nhà nghiên cứu. Nghiên cứu của Hoàng Nguyên Phong về kiểm duyệt I2P đã được chấp nhận tại FOCI của USENIX, dẫn đến sự ra đời của I2P Metrics.

Tại CCC 2019, quyết định đã được đưa ra để chuyển từ Monotone sang GitLab. Vào ngày 10 tháng 12 năm 2020, dự án chính thức chuyển từ Monotone sang Git, gia nhập cộng đồng các nhà phát triển sử dụng Git.

0.9.49 (2021) đã bắt đầu quá trình chuyển đổi sang mã hóa ECIES-X25519 mới, nhanh hơn dành cho routers, hoàn tất nhiều năm công việc soạn thảo đặc tả. Việc chuyển đổi này sẽ kéo dài qua vài bản phát hành.

## 1.5.0 — Bản phát hành kỷ niệm ra mắt sớm

Sau 9 năm của dòng phát hành 0.9.x, dự án đã chuyển thẳng từ 0.9.50 lên 1.5.0 nhằm ghi nhận gần 20 năm nỗ lực cung cấp tính ẩn danh và bảo mật. Bản phát hành này hoàn tất việc triển khai các thông điệp dựng tunnel nhỏ hơn để giảm mức sử dụng băng thông và tiếp tục quá trình chuyển đổi sang mã hóa X25519.

**Chúc mừng cả đội. Hãy làm thêm 20 nữa.**
