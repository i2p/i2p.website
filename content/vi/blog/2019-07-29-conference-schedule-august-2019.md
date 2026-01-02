---
title: "Lịch trình hội nghị tháng 8 năm 2019"
date: 2019-07-29
author: "sadie"
description: "Các nhà phát triển I2P đang tham dự nhiều hội nghị trong tháng này"
---

# Lịch trình hội nghị tháng 8 năm 2019

Chào mọi người,


Tháng tới sẽ rất bận rộn! Hãy gặp gỡ các nhà phát triển I2P tại hai buổi hội thảo ở Defcon 27, và kết nối với các nhà nghiên cứu tại FOCI '19, những người đã quan sát việc kiểm duyệt I2P.

## I2P for Cryptocurrency Developers

**zzz**

- Monero Village
- August 9, 3:15pm
- Monero Village will be on the 26th floor of Bally's [map](https://defcon.org/html/defcon-27/dc-27-venue.html)

Buổi hội thảo này sẽ hỗ trợ các nhà phát triển trong việc thiết kế các ứng dụng để giao tiếp qua I2P nhằm đảm bảo tính ẩn danh và bảo mật. Chúng tôi sẽ thảo luận các yêu cầu phổ biến đối với ứng dụng tiền mã hóa, và xem xét kiến trúc cùng các nhu cầu cụ thể của từng ứng dụng. Sau đó, chúng tôi sẽ đề cập đến truyền thông qua tunnel, lựa chọn router và thư viện, cùng các phương án đóng gói, và giải đáp mọi câu hỏi liên quan đến việc tích hợp I2P.

Mục tiêu là tạo ra các thiết kế an toàn, có khả năng mở rộng, dễ mở rộng và hiệu quả, đáp ứng nhu cầu của từng dự án cụ thể.

## I2P dành cho nhà phát triển tiền điện tử

**tôi không biết**

- Crypto & Privacy Village
- Saturday August 10, 2pm - 3:30pm
- Planet Hollywood [map](https://defcon.org/images/defcon-27/maps/ph-final-public.pdf)
- This workshop is not recorded. So don't miss it!

Hội thảo cung cấp phần giới thiệu về các cách để đưa một ứng dụng hoạt động với mạng ngang hàng ẩn danh (Peer-to-Peer) I2P. Các nhà phát triển nên hiểu rằng việc sử dụng P2P ẩn danh trong ứng dụng của họ không nhất thiết phải khác nhiều so với những gì họ vốn đang làm trong các ứng dụng Peer-to-Peer không ẩn danh. Phần này bắt đầu bằng việc giới thiệu hệ thống plugin I2P, trình bày cách các plugin hiện có tự cấu hình để giao tiếp qua I2P và những điểm mạnh, điểm yếu của từng cách tiếp cận. Sau đó, chúng ta sẽ tiếp tục tìm hiểu cách điều khiển I2P bằng lập trình thông qua các API SAM và I2PControl. Cuối cùng, chúng ta sẽ đi sâu vào SAMv3 API bằng cách bắt đầu một thư viện mới sử dụng nó trong Lua và viết một ứng dụng đơn giản.

## I2P dành cho nhà phát triển ứng dụng

**sadie**

- FOCI '19
- Tuesday August 13th 10:30am
- Hyatt Regency Santa Clara
- Co-located with USENIX Security '19
- [Workshop Program](https://www.usenix.org/conference/foci19/workshop-program)

Sự phổ biến của kiểm duyệt Internet đã thúc đẩy sự ra đời của nhiều nền tảng đo lường để giám sát các hoạt động lọc. Một thách thức quan trọng mà các nền tảng này gặp phải xoay quanh bài toán đánh đổi giữa độ sâu đo lường và độ bao phủ. Trong bài báo này, chúng tôi trình bày một hạ tầng đo lường kiểm duyệt mang tính cơ hội, được xây dựng dựa trên một mạng các máy chủ VPN phân tán do các tình nguyện viên vận hành, mà chúng tôi dùng để đo mức độ mạng ẩn danh I2P bị chặn trên toàn thế giới. Hạ tầng này mang lại cho chúng tôi không chỉ nhiều điểm quan sát đa dạng về mặt địa lý, mà còn khả năng thực hiện các phép đo chuyên sâu ở mọi tầng của ngăn xếp mạng. Dựa trên hạ tầng đó, chúng tôi đo ở quy mô toàn cầu tính khả dụng của bốn dịch vụ I2P khác nhau: trang chủ chính thức, trang mirror của nó, reseed servers, và các nút chuyển tiếp (relay) đang hoạt động trong mạng. Trong vòng một tháng, chúng tôi đã thực hiện tổng cộng 54K phép đo từ 1.7K vị trí mạng ở 164 quốc gia. Với các kỹ thuật khác nhau để phát hiện chặn tên miền, network packet injection (chèn gói tin ở mức mạng), và block pages (trang thông báo chặn), chúng tôi phát hiện kiểm duyệt I2P ở năm quốc gia: Trung Quốc, Iran, Oman, Qatar và Kuwait. Cuối cùng, chúng tôi kết luận bằng cách thảo luận các hướng tiếp cận tiềm năng để vượt qua kiểm duyệt trên I2P.

**Lưu ý:** Các hình ảnh được tham chiếu trong bài đăng gốc (monerovillageblog.png, cryptovillageblog.png, censorship.jpg) có thể cần được thêm vào thư mục `/static/images/blog/`.
