---
title: "Nghiên cứu nổi bật"
date: 2019-10-25
author: "Hoàng Nguyên Phong"
description: "Một nghiên cứu thực nghiệm về mạng ẩn danh I2P và khả năng chống kiểm duyệt của nó"
categories: ["community"]
---

## Nghiên cứu nổi bật - Một nghiên cứu thực nghiệm về mạng ẩn danh I2P và khả năng chống kiểm duyệt của nó

Bài viết blog dưới đây được viết bởi Information Controls Fellow (học giả chương trình ICFP) Hoàng Nguyên Phong. Với tư cách là một ICFP fellow, nghiên cứu của Phong tập trung phân tích các khía cạnh khác nhau của mạng I2P, một công cụ Internet tăng cường quyền riêng tư có thể được sử dụng để truy cập nội dung trực tuyến qua một mạng tăng cường ẩn danh, hữu ích trong việc vượt qua kiểm duyệt do nhà nước áp đặt. Trong quá trình làm việc với đơn vị tiếp nhận của mình, Đại học Massachusetts Amherst, Phong nghiên cứu khả năng chống chịu trước kiểm duyệt của mạng I2P, bao gồm việc xác định những phương thức chặn mà một cơ quan kiểm duyệt nhà nước có thể sử dụng để ngăn truy cập vào I2P và khảo sát các giải pháp tiềm năng nhằm giúp I2P chống chịu tốt hơn trước các biện pháp chặn như vậy.

Phong found blocking attempts on the I2P network (specifically via DNS poisoning, SNI-based blocking, TCP packet injection, and page-specific blocks) emanating from five countries: China, Oman, Qatar, Iran, and Kuwait. Phong posits that because the blocks are usually imposed on the I2P download page and reseed servers, such blocking could be mitigated by hosting download links to this content on large cloud service providers - raising the collateral cost of blocking. Phong also built a metrics portal for the platform so that researchers and others can better understand who is using I2P, finding that there are about 20,000 relays in the network on a daily basis.

(Trích từ bài viết trên blog của OTF)

- [Original Blog Post](https://homepage.np-tokumei.net/post/notes-otf-wrapup-blogpost/)
- [OTF Mirror of the Blog Post](https://www.opentech.fund/news/empirical-study-i2p-anonymity-network-and-its-censorship-resistance/)
- [I2P Metrics Portal](https://i2p-metrics.np-tokumei.net/)

Bài báo nghiên cứu cũng có sẵn tại đây:

- [Research Paper](https://www.researchgate.net/publication/327445307_An_Empirical_Study_of_the_I2P_Anonymity_Network_and_its_Censorship_Resistance)

Chúng tôi cảm ơn Phong và các cộng sự vì nghiên cứu xuất sắc của họ khi chúng tôi bắt tay giải quyết những vấn đề đã được xác định. Thật phấn khởi khi thấy ngày càng có nhiều nghiên cứu học thuật về I2P và chúng tôi háo hức tiếp tục hợp tác với Phong.
