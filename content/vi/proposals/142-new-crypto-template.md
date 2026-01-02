---
title: "Đề xuất Mẫu Mã hóa Mới"
number: "142"
author: "zzz"
created: "2018-01-11"
lastupdated: "2018-01-20"
status: "Meta"
thread: "http://zzz.i2p/topics/2499"
toc: true
---

## Tổng quan

Tài liệu này mô tả các vấn đề quan trọng cần xem xét khi đề xuất
thay thế hoặc thêm mới vào mã hóa bất đối xứng ElGamal của chúng tôi.

Đây là một tài liệu thông tin.


## Động lực

ElGamal là cũ và chậm, và có những lựa chọn tốt hơn.
Tuy nhiên, có một số vấn đề cần được giải quyết trước khi chúng tôi có thể thêm hoặc thay đổi sang bất kỳ thuật toán mới nào.
Tài liệu này làm rõ các vấn đề chưa được giải quyết này.


## Nghiên cứu Cơ bản

Bất kỳ ai đề xuất mã hóa mới phải nắm rõ các tài liệu sau:

- [Đề xuất 111 NTCP2](/vi/proposals/111-ntcp-2/)
- [Đề xuất 123 LS2](/vi/proposals/123-new-netdb-entries/)
- [Đề xuất 136 các loại chữ ký thử nghiệm](/vi/proposals/136-experimental-sigtypes/)
- [Đề xuất 137 các loại chữ ký tùy chọn](/vi/proposals/137-optional-sigtypes/)
- Các luồng thảo luận ở đây cho từng đề xuất trên, được liên kết trong đó
- [các ưu tiên đề xuất năm 2018](http://zzz.i2p/topics/2494)
- [đề xuất ECIES](http://zzz.i2p/topics/2418)
- [tổng quan mã hóa bất đối xứng mới](http://zzz.i2p/topics/1768)
- [Tổng quan mã hóa cấp thấp](/vi/docs/specs/common-structures/)


## Các Sử Dụng Mã hóa Bất Đối Xứng

Để ôn lại, chúng tôi sử dụng ElGamal cho:

1) Tin nhắn Xây dựng Đường hầm (khóa nằm trong RouterIdentity)

2) Mã hóa router-to-router của netdb và các tin nhắn I2NP khác (Khóa nằm trong RouterIdentity)

3) ElGamal+AES/SessionTag End-to-end của Khách hàng (khóa nằm trong LeaseSet, khóa Destination không được sử dụng)

4) Ephemeral DH cho NTCP và SSU


## Thiết kế

Bất kỳ đề xuất nào để thay thế ElGamal bằng thứ khác phải cung cấp chi tiết sau.


## Đặc tả

Bất kỳ đề xuất nào cho mã hóa bất đối xứng mới phải hoàn toàn chỉ rõ các điều sau đây.


### 1. Tổng quát

Trả lời các câu hỏi sau trong đề xuất của bạn. Lưu ý rằng điều này có thể cần phải là một đề xuất riêng biệt từ các chi tiết trong 2) dưới đây, vì nó có thể xung đột với các đề xuất hiện có 111, 123, 136, 137, hoặc những cái khác.

- Bạn đề xuất sử dụng mã hóa mới cho các trường hợp 1-4 ở trên không?
- Nếu cho 1) hoặc 2) (router), Khóa công khai đi đâu, trong RouterIdentity hay RouterInfo props? Bạn có ý định sử dụng loại mã hóa trong chứng chỉ khóa? Hoàn toàn chỉ rõ. Giải thích lý do quyết định của bạn cho mỗi trường hợp.
- Nếu cho 3) (khách hàng), bạn có ý định lưu khóa công khai trong điểm đến và sử dụng loại mã hóa trong chứng chỉ khóa (như trong đề xuất ECIES), hay lưu nó trong LS2 (như trong đề xuất 123), hay thứ khác? Hoàn toàn chỉ rõ, và giải thích lý do quyết định của bạn.
- Cho tất cả các sử dụng, làm thế nào để quảng cáo hỗ trợ? Nếu cho 3), nó có nằm trong LS2, hay ở nơi khác không? Nếu cho 1) và 2), nó có tương tự như các đề xuất 136 và/hoặc 137 không? Hoàn toàn chỉ rõ, và giải thích lý do quyết định của bạn. Có thể cần một đề xuất riêng cho việc này.
- Hoàn toàn chỉ rõ cách và lý do làm thế nào để tương thích ngược, và hoàn toàn chỉ rõ một kế hoạch chuyển đổi.
- Những đề xuất chưa thực hiện nào là tiền đề cho đề xuất của bạn?


### 2. Loại mã hóa cụ thể

Trả lời các câu hỏi sau trong đề xuất của bạn:

- Thông tin mã hóa chung, các đường cong/thông số cụ thể, hoàn toàn giải thích sự lựa chọn của bạn. Cung cấp liên kết đến đặc tả và thông tin khác.
- Kết quả kiểm tra tốc độ so với ElG và các lựa chọn thay thế khác nếu có. Bao gồm mã hóa, giải mã, và keygen.
- Khả năng thư viện trong C++ và Java (cả OpenJDK, BouncyCastle, và bên thứ 3)
  Đối với bên thứ 3 hoặc không phải Java, cung cấp liên kết và giấy phép
- Số loại mã hóa được đề xuất (phạm vi thử nghiệm hoặc không)


## Ghi chú


