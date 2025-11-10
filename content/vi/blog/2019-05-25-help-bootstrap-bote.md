---
title: "Cách tham gia tình nguyện bằng cách giúp I2P-Bote bootstrap (khởi tạo ban đầu)"
date: 2019-05-20
author: "idk"
description: "Hãy giúp khởi tạo I2P-Bote!"
categories: ["development"]
---

Một cách đơn giản để giúp mọi người nhắn tin riêng tư với nhau là chạy một I2P-Bote peer mà người dùng I2P-Bote mới có thể dùng để bootstrap (khởi tạo ban đầu) các I2P-Bote peer riêng của họ. Đáng tiếc là cho đến nay, quy trình thiết lập một I2P-Bote bootstrap peer đã mơ hồ hơn nhiều so với mức đáng ra phải như vậy. Thực ra, việc này cực kỳ đơn giản!

**What is I2P-bote?**

I2P-bote là một hệ thống nhắn tin riêng tư được xây dựng trên i2p, có thêm các tính năng nhằm làm cho việc nhận biết thông tin về các tin nhắn được truyền trở nên khó khăn hơn nữa. Vì vậy, nó có thể được dùng để truyền các tin nhắn riêng tư một cách an toàn, chấp nhận độ trễ cao và không phụ thuộc vào một bộ chuyển tiếp tập trung để gửi tin khi người gửi ngoại tuyến. Điều này trái ngược với hầu hết các hệ thống nhắn tin riêng tư phổ biến khác, vốn hoặc yêu cầu cả hai bên đều phải trực tuyến, hoặc dựa vào một dịch vụ chỉ đáng tin cậy một phần để truyền tin thay mặt cho những người gửi đã ngoại tuyến.

hoặc, ELI5 (giải thích như cho bé 5 tuổi): Nó được dùng tương tự như email, nhưng không mắc phải bất kỳ nhược điểm nào về quyền riêng tư mà email gặp phải.

**Bước 1: Cài đặt I2P-Bote**

I2P-Bote là một plugin i2p và việc cài đặt nó rất dễ dàng. Hướng dẫn gốc có tại [bote eepSite, bote.i2p](http://bote.i2p/install/), nhưng nếu bạn muốn đọc chúng trên clearnet (Internet công khai), các hướng dẫn sau đây được cung cấp bởi bote.i2p:

1. Go to the plugin install form in your routerconsole: http://127.0.0.1:7657/configclients#plugin
2. Paste in the URL http://bote.i2p/i2pbote.su3
3. Click Install Plugin.
4. Once installed, click SecureMail in the routerconsole sidebar or homepage, or go to http://127.0.0.1:7657/i2pbote/

**Bước Hai: Lấy địa chỉ base64 của nút (node) I2P-Bote của bạn**

Đây là phần mà đôi khi người ta có thể bị vướng, nhưng đừng lo lắng. Mặc dù hơi khó tìm hướng dẫn, nhưng thực ra việc này khá dễ và có một số công cụ cùng tùy chọn dành cho bạn, tùy thuộc vào hoàn cảnh của bạn. Đối với những người muốn tình nguyện vận hành bootstrap nodes (các nút khởi động), cách tốt nhất là trích xuất thông tin cần thiết từ tệp khóa riêng mà bote tunnel sử dụng.

**Các khóa ở đâu?**

I2P-Bote lưu các khóa đích (destination keys) của nó trong một tệp văn bản, mà trên Debian, được đặt tại `/var/lib/i2p/i2p-config/i2pbote/local_dest.key`. Trên các hệ thống không phải Debian nơi i2p được người dùng cài đặt, khóa sẽ nằm ở `$HOME/.i2p/i2pbote/local_dest.key`, và trên Windows, tệp sẽ nằm ở `C:\ProgramData\i2p\i2pbote\local_dest.key`.

**Phương pháp A: Chuyển khóa văn bản thuần thành đích base64**

Để chuyển một khóa ở dạng văn bản thuần thành một destination (đích nhận trong I2P) dạng base64, cần lấy khóa đó và chỉ tách phần destination ra khỏi nó. Để thực hiện đúng, cần làm theo các bước sau:

1. First, take the full destination and decode it from i2p's base64 character set into binary.
2. Second, take bytes 386 and 387 and convert them to a single Big-Endian integer.
3. Add the number you computed from the two bytes in step two to 387. This is the length of the base64 destination.
4. Take that nummber of bytes from the front of the full destination to get the destination as a range of bytes.
5. Convert back to a base64 representation using i2p's base64 character set.

Có một số ứng dụng và tập lệnh có thể thực hiện các bước này cho bạn. Dưới đây là một vài trong số chúng, nhưng danh sách này chưa hề đầy đủ:

- [the i2p.scripts collection of scripts(Mostly java and bash)](https://github.com/i2p/i2p.scripts)
- [my application for converting keys(Go)](https://github.com/eyedeekay/keyto)

Những khả năng này cũng có sẵn trong một số thư viện phát triển ứng dụng cho I2P.

**Lối tắt:**

Vì destination (đích I2P) cục bộ của nút bote của bạn là một DSA destination, nên nhanh hơn nếu chỉ cắt ngắn tệp local_dest.key xuống còn 516 byte đầu tiên. Để thực hiện việc đó một cách dễ dàng, hãy chạy lệnh này khi chạy I2P-Bote cùng với I2P trên Debian:

```bash
sudo -u i2psvc head -c 516 /var/lib/i2p/i2p-config/i2pbote/local_dest.key
```
Hoặc, nếu I2P được cài đặt dưới tài khoản người dùng của bạn:

```bash
head -c 516 ~/.i2p/i2pbote/local_dest.key
```
**Phương pháp B: Thực hiện tra cứu**

Nếu điều đó có vẻ hơi quá nhiều việc, bạn có thể tra cứu điểm đến base64 của kết nối Bote của mình bằng cách truy vấn địa chỉ base32 của nó bằng bất kỳ phương thức nào hiện có để tra cứu một địa chỉ base32. Địa chỉ base32 của nút Bote của bạn có sẵn trên trang "Connection" trong ứng dụng plugin Bote, tại [127.0.0.1:7657/i2pbote/network](http://127.0.0.1:7657/i2pbote/network)

**Step Three: Contact Us!**

**Cập nhật tệp built-in-peers.txt với nút mới của bạn**

Bây giờ bạn đã có destination (đích) chính xác cho nút I2P-Bote của mình, bước cuối cùng là tự thêm mình vào danh sách peer (đồng cấp) mặc định cho [I2P-Bote tại đây](https://github.com/i2p/i2p.i2p-bote/tree/master/core/src/main/resources/i2p/bote/network) tại đây. Bạn có thể thực hiện bằng cách fork repository, thêm bản thân vào danh sách với tên của bạn được comment (commented out), và destination dài 516 ký tự của bạn ngay bên dưới, như sau:

```
# idk
QuabT3H5ljZyd-PXCQjvDzdfCec-2yv8E9i6N71I5WHAtSEZgazQMReYNhPWakqOEj8BbpRvnarpHqbQjoT6yJ5UObKv2hA2M4XrroJmydPV9CLJUCqgCqFfpG-bkSo0gEhB-GRCUaugcAgHxddmxmAsJVRj3UeABLPHLYiakVz3CG2iBMHLJpnC6H3g8TJivtqabPYOxmZGCI-P~R-s4vwN2st1lJyKDl~u7OG6M6Y~gNbIzIYeQyNggvnANL3t6cUqS4v0Vb~t~CCtXgfhuK5SK65Rtkt2Aid3s7mrR2hDxK3SIxmAsHpnQ6MA~z0Nus-VVcNYcbHUBNpOcTeKlncXsuFj8vZL3ssnepmr2DCB25091t9B6r5~681xGEeqeIwuMHDeyoXIP0mhEcy3aEB1jcchLBRLMs6NtFKPlioxz0~Vs13VaNNP~78bTjFje5ya20ahWlO0Md~x5P5lWLIKDgaqwNdIrijtZAcILn1h18tmABYauYZQtYGyLTOXAAAA
```
và gửi một pull request (đề xuất hợp nhất thay đổi). Chỉ có vậy thôi, vì vậy hãy giúp giữ cho i2p luôn tồn tại, phi tập trung và đáng tin cậy.
