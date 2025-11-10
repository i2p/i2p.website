---
title: "Một lời nhắc nhở để giữ an toàn khi I2P phát triển"
date: 2022-09-26
author: "idk"
description: "Lời nhắc nhở để luôn an toàn khi I2P phát triển"
categories: ["general"]
---

## Lời nhắc về an toàn khi I2P phát triển

Đây là thời điểm đầy hứng khởi đối với The Invisible Internet Project (I2P). Chúng tôi đang hoàn tất quá trình chuyển đổi sang mật mã hiện đại trên tất cả các transport (giao thức truyền tải) của mình, ( Java và C++), và gần đây chúng tôi đã có thêm một dịch vụ outproxy (ủy quyền ra Internet công khai) có băng thông lớn và chuyên nghiệp, và có nhiều ứng dụng tích hợp chức năng dựa trên I2P hơn bao giờ hết. Mạng lưới đang sẵn sàng để phát triển, vì vậy bây giờ là thời điểm tốt để nhắc mọi người hãy thận trọng và an toàn khi tải xuống I2P và phần mềm liên quan đến I2P. Chúng tôi hoan nghênh các ứng dụng mới, các bản triển khai, và các fork (nhánh tách) với những ý tưởng mới, và sức mạnh của mạng đến từ tính mở của nó đối với sự tham gia của tất cả người dùng I2P. Thực tế, chúng tôi không thích gọi các bạn là người dùng, chúng tôi thích dùng từ "Participants" vì mỗi người trong các bạn đều giúp ích cho mạng lưới, theo cách riêng của mình bằng cách đóng góp nội dung, phát triển ứng dụng, hoặc đơn giản là định tuyến lưu lượng và giúp những người tham gia khác tìm các nút ngang hàng.

Bạn chính là mạng lưới, và chúng tôi muốn bạn an toàn.

Chúng tôi đã nhận thấy các nỗ lực mạo danh sự hiện diện của I2P trên web và mạng xã hội. Để tránh vô tình tạo thêm đà cho các chiến dịch này, chúng tôi sẽ không nêu tên các tác nhân có liên quan đến chúng. Tuy nhiên, để giúp bạn nhận diện các chiến dịch đó nếu bắt gặp trong thực tế, chúng tôi đang ghi lại các chiến thuật của họ:

- Copying text directly from the I2P Web Site without acknowledging our license requirements in a way that may suggest endorsement.
- Involvement or promotion of an Initial Coin Offering, or ICO
- Crypto-Scam like language
- Graphics that have nothing to do with the textual content
- Click-farming behavior, sites that appear to have content but which instead link to other sites
- Attempts to get the user to register for non-I2P chat servers. We come to you or you come to us, we will not ask you to meet us at a third-party service unless you already use it(Note that this is not always true for other forks and projects, but it is true of geti2p.net).
- The use of bot networks to amplify any message on social media. I2P(geti2p.net) does not use bots for social media advertising.

Những chiến dịch này đã có tác dụng phụ là "shadow-banning (chặn ngầm)" một số thảo luận chính đáng liên quan đến I2P trên Twitter và có thể cả các mạng xã hội khác.

## Các trang web của chúng tôi

Chúng tôi có các trang web chính thức nơi mọi người có thể tải xuống phần mềm I2P một cách an toàn:

- [Official Website - i2p.net](https://i2p.net)
- [Official Website - geti2p.net](https://geti2p.net)
- [Official Gitlab - i2pgit.org](https://i2pgit.org)
- [Official Debian Repository - deb.i2p2.de](https://deb.i2p2.de)
- [Official Debian Repository - deb.i2p2.no](https://deb.i2p2.no)
- [Official Forums - i2pforum.net](https://i2pforum.net)

## Diễn đàn, blog và mạng xã hội của Invisible Internet Project

### Hosted by the project

- [I2P Forums](https://i2pforum.net) - I2P Mirror: https://i2pforum.i2p
- IRC: `#i2p-dev` on Irc2P(`127.0.0.1:6668` in a standard I2P installation)

### Hosted by Others

Các dịch vụ này do các bên thứ ba vận hành, đôi khi là các công ty, nơi chúng tôi tham gia để duy trì sự hiện diện truyền thông xã hội nhằm tiếp cận những người dùng I2P chọn tham gia chúng. Chúng tôi sẽ không bao giờ yêu cầu bạn tham gia các dịch vụ này, trừ khi bạn đã có sẵn tài khoản tại đó trước khi tương tác với chúng tôi.

- [Launchpad](https://launchpad.net/i2p)
- [Github](https://github.com/i2p)
- [Twitter](https://twitter.com/GetI2P)
- [Reddit](https://www.reddit.com/r/i2p/)
- [Mastodon](https://mastodon.social/@i2p)
- [Medium](https://i2p.medium.com/)

## Forks, Apps, and Third-Party Implementations are Not Evil

Bài viết này nhằm cung cấp các cách thẩm định nguồn để lấy gói Java I2P, được đại diện bởi mã nguồn nằm tại https://i2pgit.org/i2p-hackers/i2p.i2p và https://github.com/i2p/i2p.i2p, và có thể tải xuống từ trang web https://geti2p.net/. Bài viết không nhằm phán xét các forks (nhánh tách) của bên thứ ba, các dự án downstream (hạ nguồn), embedders (bên tích hợp nhúng), packagers (người/nhóm đóng gói), những người đang thử nghiệm trong phòng thí nghiệm, hoặc những người đơn giản là không đồng ý với chúng tôi. Tất cả các bạn đều là những thành viên đáng quý của cộng đồng chúng tôi, những người đang cố gắng bảo vệ, chứ không làm tổn hại, quyền riêng tư của người khác. Vì chúng tôi nhận thấy có những nỗ lực mạo danh các thành viên cộng đồng dự án I2P, bạn có thể muốn rà soát lại các quy trình tải xuống, xác minh và cài đặt mà bạn khuyến nghị cho người dùng của mình, nhằm tài liệu hóa các nguồn chính thức và các mirrors (máy chủ phản chiếu) đã biết của bạn.

*Lưu ý của tác giả: Một phiên bản trước đó của bài viết trên blog này chứa dấu vân tay TLS của từng dịch vụ do Dự án I2P vận hành. Những dấu vân tay này đã được gỡ bỏ khi việc gia hạn chứng chỉ khiến chúng trở nên không chính xác.*
