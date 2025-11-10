---
title: "Xin chào Git, tạm biệt Monotone"
date: 2020-12-10
author: "idk"
description: "Xin chào git, tạm biệt mtn"
categories: ["Status"]
---

## Chào Git, tạm biệt Monotone

### The I2P Git Migration is nearly concluded

Trong hơn một thập kỷ, I2P đã dựa vào dịch vụ Monotone lâu đời để đáp ứng nhu cầu quản lý phiên bản của mình, nhưng trong vài năm gần đây, phần lớn thế giới đã chuyển sang hệ thống quản lý phiên bản Git vốn nay gần như phổ quát. Cùng thời gian đó, Mạng I2P đã trở nên nhanh hơn và đáng tin cậy hơn, và các giải pháp khắc phục dễ tiếp cận cho hạn chế không thể nối lại của Git đã được phát triển.

Hôm nay đánh dấu một cột mốc quan trọng đối với I2P, khi chúng tôi ngừng sử dụng nhánh mtn i2p.i2p cũ và chính thức chuyển việc phát triển các thư viện I2P cốt lõi bằng Java từ Monotone sang Git.

Mặc dù việc chúng tôi sử dụng mtn đã từng bị đặt câu hỏi trong quá khứ, và nó cũng không phải lúc nào cũng là lựa chọn phổ biến, tôi muốn nhân dịp này, với tư cách có lẽ là dự án cuối cùng còn sử dụng Monotone, gửi lời cảm ơn đến các nhà phát triển Monotone, hiện tại và trước đây, dù họ ở đâu, vì phần mềm mà họ đã tạo ra.

## GPG Signing

Việc đưa thay đổi vào các kho lưu trữ của Dự án I2P yêu cầu bạn cấu hình ký GPG cho các commit git, bao gồm cả Merge Requests và Pull Requests. Vui lòng cấu hình client git của bạn để ký GPG trước khi bạn fork i2p.i2p và gửi bất kỳ thay đổi nào.

## Ký bằng GPG

Kho lưu trữ chính thức được lưu trữ tại https://i2pgit.org/i2p-hackers/i2p.i2p và tại https://git.idk.i2p/i2p-hackers/i2p.i2p, nhưng có một "Mirror" (bản sao phản chiếu) sẵn có trên Github tại https://github.com/i2p/i2p.i2p.

Giờ đây khi chúng ta đã chuyển sang git, chúng ta có thể đồng bộ các kho lưu trữ từ phiên bản Gitlab tự lưu trữ của chính mình sang Github, và ngược lại. Điều này có nghĩa là có thể tạo và gửi một merge request (yêu cầu hợp nhất) trên Gitlab và khi nó được hợp nhất, kết quả sẽ được đồng bộ với Github, và một Pull Request (yêu cầu kéo) trên Github, khi được hợp nhất, sẽ xuất hiện trên Gitlab.

Điều này có nghĩa là bạn có thể gửi mã cho chúng tôi thông qua triển khai Gitlab của chúng tôi hoặc qua Github, tùy theo sở thích của bạn; tuy nhiên, nhiều nhà phát triển I2P theo dõi Gitlab thường xuyên hơn Github. MR (Merge Request - yêu cầu gộp) gửi lên Gitlab thường có khả năng được gộp sớm hơn so với PR (Pull Request - yêu cầu gửi thay đổi) gửi lên Github.

## Các kho lưu trữ chính thức và đồng bộ Gitlab/Github

Xin chúc mừng và cảm ơn tất cả mọi người đã giúp đỡ trong quá trình chuyển đổi sang Git, đặc biệt là zzz, eche|on, nextloop và những người vận hành máy chủ mirror của trang web của chúng tôi! Mặc dù một số người trong chúng tôi sẽ nhớ Monotone, nó đã trở thành một rào cản đối với những người tham gia mới và hiện tại trong phát triển I2P và chúng tôi rất hào hứng được gia nhập cộng đồng các nhà phát triển đang sử dụng Git để quản lý các dự án phân tán của họ.
