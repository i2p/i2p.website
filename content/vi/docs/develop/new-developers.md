---
title: "Hướng dẫn dành cho Lập trình viên Mới"
description: "Cách bắt đầu đóng góp cho I2P: tài liệu học tập, mã nguồn, biên dịch, ý tưởng, xuất bản, cộng đồng, dịch thuật và công cụ"
slug: "new-developers"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
notes: cập nhật phần dịch thuật
---

Vậy là bạn muốn bắt đầu làm việc với I2P? Tuyệt vời! Đây là hướng dẫn nhanh để bắt đầu đóng góp vào website hoặc phần mềm, phát triển, hoặc tạo bản dịch.

Chưa sẵn sàng để lập trình? Hãy thử [tham gia](/get-involved/) trước.

## Tìm hiểu về Java

Router I2P và các ứng dụng nhúng của nó sử dụng Java làm ngôn ngữ phát triển chính. Nếu bạn chưa có kinh nghiệm với Java, bạn luôn có thể tham khảo [Thinking in Java](https://chenweixiang.github.io/docs/Thinking_in_Java_4th_Edition.pdf)

Nghiên cứu phần giới thiệu "how", các tài liệu "how" khác, phần giới thiệu kỹ thuật và các tài liệu liên quan:

- Giới thiệu cách thức: [Giới thiệu về I2P](/docs/overview/intro/)
- Trung tâm tài liệu: [Tài liệu](/docs/)
- Giới thiệu kỹ thuật: [Giới thiệu Kỹ thuật](/docs/overview/tech-intro/)

Những tài liệu này sẽ cung cấp cho bạn cái nhìn tổng quan tốt về cách I2P được cấu trúc và những chức năng khác nhau mà nó thực hiện.

## Lấy Mã Nguồn I2P

Để phát triển trên I2P router hoặc các ứng dụng nhúng, bạn cần lấy mã nguồn.

### Cách thức hiện tại của chúng tôi: Git

I2P có dịch vụ Git chính thức và chấp nhận đóng góp qua Git tại GitLab của chúng tôi:

- Trong I2P: <http://git.idk.i2p>
- Ngoài I2P: <https://i2pgit.org>

Sao chép repository chính:

```
git clone https://i2pgit.org/I2P_Developers/i2p.i2p.git
```
Một bản sao chỉ đọc cũng có sẵn tại GitHub:

- Mirror trên GitHub: [github.com/i2p/i2p.i2p](https://github.com/i2p/i2p.i2p)

```
git clone https://github.com/i2p/i2p.i2p.git
```
## Xây dựng I2P

Để biên dịch mã nguồn, bạn cần Sun/Oracle Java Development Kit 6 trở lên, hoặc JDK tương đương (khuyến nghị mạnh Sun/Oracle JDK 6) và Apache Ant phiên bản 1.7.0 trở lên. Nếu bạn đang làm việc với mã nguồn I2P chính, hãy vào thư mục `i2p.i2p` và chạy lệnh `ant` để xem các tùy chọn build.

Để xây dựng hoặc làm việc với các bản dịch console, bạn cần các công cụ `xgettext`, `msgfmt`, và `msgmerge` từ gói GNU gettext.

Để phát triển các ứng dụng mới, xem [hướng dẫn phát triển ứng dụng](/docs/develop/applications/).

## Ý Tưởng Phát Triển

Xem danh sách TODO của dự án hoặc danh sách vấn đề trên GitLab để có ý tưởng:

- Vấn đề GitLab: [i2pgit.org/I2P_Developers/i2p.i2p/issues](https://i2pgit.org/I2P_Developers/i2p.i2p/issues)

## Công bố Kết quả

Xem phần cuối của trang giấy phép để biết các yêu cầu về quyền commit. Bạn cần những quyền này để đưa mã vào `i2p.i2p` (không bắt buộc đối với trang web!).

- [Trang giấy phép](/docs/develop/licenses#commit)

## Tìm hiểu về chúng tôi!

Các nhà phát triển thường có mặt trên IRC. Bạn có thể liên hệ với họ trên nhiều mạng khác nhau và trên các mạng nội bộ của I2P. Nơi thường tìm thấy họ là kênh `#i2p-dev`. Tham gia kênh và chào hỏi! Chúng tôi cũng có thêm [hướng dẫn dành cho các nhà phát triển thường xuyên](/docs/develop/dev-guidelines/).

##

Người dịch trang web và bảng điều khiển router: Xem [Hướng dẫn cho Người dịch Mới](/docs/develop/new-translators/) để biết các bước tiếp theo.

## Công cụ

I2P là phần mềm mã nguồn mở được phát triển chủ yếu bằng các bộ công cụ mã nguồn mở. Dự án I2P gần đây đã có được giấy phép cho YourKit Java Profiler. Các dự án mã nguồn mở đủ điều kiện nhận giấy phép miễn phí với điều kiện YourKit được tham chiếu trên trang web của dự án. Vui lòng liên hệ nếu bạn quan tâm đến việc phân tích codebase của I2P.

YourKit đang hỗ trợ các dự án mã nguồn mở với bộ profiler đầy đủ tính năng của họ. YourKit, LLC là nhà sáng tạo các công cụ đổi mới và thông minh để profiling các ứng dụng Java và .NET. Hãy xem các sản phẩm phần mềm hàng đầu của YourKit:

- [YourKit Java Profiler](http://www.yourkit.com/java/profiler/index.jsp)
- [YourKit .NET Profiler](http://www.yourkit.com/.net/profiler/index.jsp)
