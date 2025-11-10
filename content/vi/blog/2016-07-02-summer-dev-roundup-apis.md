---
title: "Tổng hợp mùa hè cho nhà phát triển: các API"
date: 2016-07-02
author: "str4d"
description: "Trong tháng đầu tiên của Summer Dev, chúng tôi đã cải thiện tính dễ sử dụng của các API của chúng tôi dành cho các nhà phát triển Java, Android và Python."
categories: ["summer-dev"]
---

Summer Dev đang diễn ra sôi động: chúng tôi đã bận rộn tra dầu cho bộ máy, mài giũa các góc cạnh và chỉnh trang lại mọi thứ. Giờ là lúc cho bản tổng hợp đầu tiên, nơi chúng tôi giúp bạn nhanh chóng nắm bắt tiến độ mà chúng tôi đang đạt được!

## Tháng API

Mục tiêu của chúng tôi trong tháng này là "hòa nhập" - để các API và thư viện của chúng tôi hoạt động trong hạ tầng hiện có của nhiều cộng đồng khác nhau, qua đó các nhà phát triển ứng dụng có thể làm việc với I2P hiệu quả hơn, và người dùng không cần phải lo lắng về các chi tiết.

### Java / Android

Các thư viện client của I2P hiện đã có trên Maven Central! Điều này sẽ giúp các nhà phát triển Java dễ dàng sử dụng I2P trong ứng dụng của họ hơn nhiều. Thay vì phải lấy các thư viện từ một bản cài đặt hiện có, họ chỉ cần thêm I2P vào các phụ thuộc của mình. Việc nâng cấp lên các phiên bản mới cũng sẽ dễ dàng hơn nhiều.

Thư viện máy khách I2P Android cũng đã được cập nhật để sử dụng các thư viện I2P mới. Điều này có nghĩa là các ứng dụng đa nền tảng có thể hoạt động trực tiếp với I2P Android hoặc I2P trên máy tính để bàn.

### Java / Android

#### txi2p

Plugin Twisted `txi2p` hiện hỗ trợ các cổng bên trong I2P và sẽ hoạt động liền mạch với các API SAM cục bộ, từ xa và qua chuyển tiếp cổng. Hãy xem tài liệu của nó để biết hướng dẫn sử dụng và báo cáo mọi vấn đề trên GitHub.

#### i2psocket

Phiên bản (beta) đầu tiên của `i2psocket` đã được phát hành! Đây là một sự thay thế trực tiếp cho thư viện `socket` tiêu chuẩn của Python, bổ sung hỗ trợ I2P thông qua SAM API. Xem trang GitHub của nó để xem hướng dẫn sử dụng và báo cáo bất kỳ sự cố nào.

### Python

- zzz has been hard at work on Syndie, getting a headstart on Plugins month
- psi has been creating an I2P test network using i2pd, and in the process has found and fixed several i2pd bugs that will improve its compatibility with Java I2P

## Coming up: Apps month!

Chúng tôi rất hào hứng được hợp tác với Tahoe-LAFS vào tháng Bảy! I2P từ lâu đã là nơi hoạt động của một trong những mạng lưới công cộng lớn nhất, sử dụng một phiên bản Tahoe-LAFS đã được vá. Trong tháng Ứng dụng, chúng tôi sẽ hỗ trợ họ trong công việc đang diễn ra nhằm bổ sung hỗ trợ gốc cho I2P và Tor, để người dùng I2P có thể hưởng lợi từ tất cả các cải tiến từ upstream (dự án gốc).

Chúng tôi cũng sẽ trao đổi với một số dự án khác về kế hoạch tích hợp I2P của họ và hỗ trợ họ về mặt thiết kế. Hãy theo dõi!

## Take part in Summer Dev!

Chúng tôi còn nhiều ý tưởng nữa cho những việc muốn thực hiện trong các lĩnh vực này. Nếu bạn quan tâm đến việc tham gia phát triển phần mềm bảo vệ quyền riêng tư và tính ẩn danh, thiết kế các website hoặc giao diện dễ sử dụng, hoặc viết hướng dẫn cho người dùng: hãy đến trò chuyện với chúng tôi trên IRC hoặc Twitter! Chúng tôi luôn vui mừng chào đón những người mới đến với cộng đồng của mình.

Chúng tôi sẽ đăng bài tại đây trong suốt quá trình, nhưng bạn cũng có thể theo dõi tiến độ của chúng tôi và chia sẻ ý tưởng, công việc của riêng bạn với hashtag #I2PSummer trên Twitter. Hãy cùng chào đón mùa hè!
