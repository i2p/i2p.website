---
title: "Ghi chú trạng thái I2P ngày 2004-08-31"
date: 2004-08-31
author: "jr"
description: "Bản cập nhật tình hình I2P hàng tuần về suy giảm hiệu năng mạng, kế hoạch phát hành 0.3.5, nhu cầu tài liệu, và tiến độ của Stasher DHT"
categories: ["status"]
---

Chà, các chàng trai và cô gái, lại là thứ Ba rồi!

## Chỉ mục:

1. 0.3.4.3
2. 0.3.5 and 0.4
3. docs
4. stasher update
5. ???

## 1) 0.3.4.3

À, như tôi chắc các bạn đều đã nhận thấy, tuy số lượng người dùng trên mạng vẫn khá ổn định, hiệu năng đã suy giảm đáng kể trong vài ngày qua. Nguyên nhân là một loạt lỗi trong phần chọn peer (nút ngang hàng) và mã xử lý chuyển phát thông điệp, bị lộ ra khi có một đợt DoS (tấn công từ chối dịch vụ) nhỏ vào tuần trước. Kết quả là hầu như tunnels của mọi người đều liên tục thất bại, gây ra một chút hiệu ứng quả cầu tuyết. Vậy nên không, không chỉ mình bạn đâu - mạng cũng tệ hại với phần còn lại của chúng tôi nữa ;)

Tin tốt là chúng tôi đã sửa các vấn đề khá nhanh chóng, và chúng đã có trong CVS từ tuần trước, nhưng mạng vẫn sẽ rất tệ đối với mọi người cho đến khi bản phát hành tiếp theo ra mắt. Nhân đây...

## 2) 0.3.5 và 0.4

Mặc dù bản phát hành tiếp theo sẽ có tất cả những tính năng mới hấp dẫn mà chúng tôi đã lên kế hoạch cho bản phát hành 0.4 (trình cài đặt mới, chuẩn giao diện web mới, giao diện i2ptunnel mới, khay hệ thống và dịch vụ Windows, cải tiến threading (xử lý đa luồng), các bản sửa lỗi, v.v.), cách mà bản phát hành trước xuống cấp dần theo thời gian đã nói lên nhiều điều. Tôi muốn chúng ta tiến hành chậm hơn với các bản phát hành này, cho chúng có thời gian được triển khai rộng rãi hơn và để các trục trặc tự bộc lộ. Mặc dù trình mô phỏng có thể khám phá những điều cơ bản, nó không có cách nào để mô phỏng các vấn đề tự nhiên của mạng mà chúng ta thấy trên mạng thực tế đang hoạt động (ít nhất là chưa).

Do đó, bản phát hành tiếp theo sẽ là 0.3.5 - hy vọng sẽ là bản phát hành 0.3.* cuối cùng, nhưng có thể không, nếu nảy sinh các vấn đề khác. Nhìn lại cách mạng hoạt động khi tôi ngoại tuyến vào tháng Sáu, mọi thứ bắt đầu suy giảm sau khoảng hai tuần. Do đó, tôi dự định tạm hoãn việc nâng lên mức phát hành 0.4 tiếp theo cho đến khi chúng tôi có thể duy trì mức độ tin cậy cao trong ít nhất hai tuần. Tất nhiên, điều đó không có nghĩa là trong thời gian này chúng tôi sẽ không tiếp tục làm việc.

Dù sao thì, như đã đề cập tuần trước, hypercubus đang miệt mài với hệ thống cài đặt mới, phải xử lý việc tôi thay đổi lung tung và yêu cầu hỗ trợ cho các hệ thống kỳ quặc. Chúng tôi sẽ cố gắng chốt mọi thứ trong vài ngày tới để phát hành bản 0.3.5 cũng trong vài ngày tới.

## 3) tài liệu

Một trong những việc quan trọng mà chúng ta cần làm trong “cửa sổ thử nghiệm” hai tuần trước 0.4 là soạn tài liệu thật nhiều. Điều tôi đang băn khoăn là bạn thấy tài liệu của chúng ta còn thiếu những gì - bạn có những câu hỏi nào mà chúng ta cần trả lời? Dù tôi rất muốn nói “được rồi, bây giờ hãy đi viết những tài liệu đó”, tôi thực tế, nên điều tôi yêu cầu chỉ là bạn có thể xác định những tài liệu đó sẽ đề cập đến những gì.

Ví dụ, một trong những tài liệu tôi đang làm hiện nay là bản sửa đổi của mô hình đe dọa, mà giờ tôi sẽ mô tả như một loạt các trường hợp sử dụng (use case) giải thích cách I2P có thể đáp ứng nhu cầu của các cá nhân khác nhau, bao gồm chức năng, những kẻ tấn công mà người đó lo ngại, và cách họ tự bảo vệ.

Nếu bạn cho rằng câu hỏi của mình không cần một tài liệu đầy đủ để giải quyết, chỉ cần diễn đạt nó dưới dạng một câu hỏi và chúng tôi có thể thêm nó vào mục Câu hỏi thường gặp (FAQ).

## 4) cập nhật stasher

Aum đã ghé qua kênh hồi sớm nay với một bản cập nhật (trong khi tôi hỏi anh ấy dồn dập):

```
<aum> quick stasher update, with apologies for tomorrow's meeting:
<aum> infinite-level splitfiles working, have successfully
      inserted and retrieved large files
<jrandom> w00t
<aum> splitfile fragmentation/reassembly transparently occuring
      within stasher
<aum> freenet interface working
<jrandom> wow
<jrandom> so FUQID/FIW works?
<aum> use of fcp splitfile commands in freenet clients strictly
      forbidden (at this stage)
<aum> most clients such as fuqid/fiw should allow setting
      extremely large splitfile sizes, which should prevent them
      trying to talk splitfiles
<aum> if not, then i can dummy up something
<jrandom> r0x0r aum, that kicks ass!
<aum> hooks are in for detailed freenet key support
<jrandom> detailed freenet key support?
<aum> yes, specific chk@, ssk@, ksk@
<jrandom> ok great, so they're all verified @ each node, etc?
<aum> no - only verifiable by the requestor
<aum> my thinking is, given KSK@fred = 'mary',
<aum> to store as SHA1(SHA1("KSK@fred")) = E(mary), where key
      for E is SHA1("KSK@fred")
<aum> ie, crypto key is SHA1(uri), and kademlia key is
      SHA1(SHA1(uri))
<jrandom> hm
<aum> so a possessor of the URI can decyrpt, but owner of a
      datastore cannot decrypt (and therefore has plausible
      deniability)
<jrandom> well, ksks are inherently insecure, so thats no big
      loss, but what about ssk?
<deer> <detonate> those keys aren't very large
<aum> SSK as for freenet
<jrandom> so the SSKs are verified at each node?
<aum> except i'm looking to use same encryption over the top
<aum> not feasible to verify SSK at the target node
<jrandom> why not?  freenet does
<aum> well maybe it is feasible,
<aum> i guess i shouldn't be so lazy
<aum> i was trying to keep the kademlia and freenet layers
      separate
<jrandom> heh, you're not being lazy, there's a truckload of
      work here, and you're doing a great job
<aum> verifying on target node will cause some pathological
      couplings between the two layers, and force deviation
      from pure kademlia
<jrandom> i dont think its possible to do SSKs or CHKs
      securely without having the node validate the key
      properties
<aum> not correct
<aum> fred asks mary, 'gimme SSK@madonna'
<aum> mary sends back what she thinks is 'SSK@madonna'
<aum> fred tests it, barfs, then goes on to ask the next node
<aum> anyway, i MUST go - but am open to continuing discussion
      over email, or tomorrow
<aum> bbl guys
<jrandom> mallory floods the net with 'SSK@madonna' ==
      'sexDrugsRockNRoll'
<jrandom> l8r aum
```
Vậy nên, như bạn thấy, đã có rất rất nhiều tiến triển. Ngay cả khi các khóa được xác thực ở phía trên lớp DHT, thì điều đó cũng ngầu cực kỳ (theo ý kiến cá nhân của tôi). Cố lên, aum!

## 5) ???

Ok, tôi chỉ có bấy nhiêu để nói (cũng hay, vì cuộc họp sẽ bắt đầu trong chốc lát nữa)... ghé qua và muốn nói gì thì nói!

=jr
