---
title: "Ghi chú trạng thái I2P ngày 2006-08-01"
date: 2006-08-01
author: "jr"
description: "Hiệu năng mạng mạnh mẽ với tốc độ truyền I2PSnark cao, tính ổn định của tầng truyền tải NTCP, và những làm rõ về khả năng truy cập eepsite"
categories: ["status"]
---

Chào mọi người, đến lúc điểm qua một số ghi chú ngắn gọn trước cuộc họp tối nay. Tôi nhận ra rằng mọi người có thể có nhiều câu hỏi hoặc vấn đề muốn nêu ra, vì vậy chúng ta sẽ tiến hành theo một hình thức linh hoạt hơn thường lệ. Chỉ có vài điều tôi muốn đề cập trước.

* Network status

Có vẻ mạng đang hoạt động khá tốt, với các swarm I2PSnark khá lớn hoàn tất truyền tải, và với tốc độ truyền tải khá đáng kể đạt được trên từng router (nút I2P) - tôi đã thấy 650KBytes/sec và 17,000 tunnels (đường hầm) tham gia mà không có trục trặc gì. Các router ở phân khúc thấp cũng có vẻ hoạt động ổn, duyệt eepsites(I2P Sites) và irc với 2 hop tunnels sử dụng trung bình dưới 1KByte/sec.

Không phải mọi thứ đều suôn sẻ với tất cả mọi người; tuy nhiên, chúng tôi đang từng bước cập nhật hành vi của router để mang lại hiệu năng ổn định và dễ sử dụng hơn.

* NTCP

Cơ chế truyền tải NTCP (tcp "mới") đang hoạt động khá tốt sau khi khắc phục những trục trặc ban đầu. Để trả lời một câu hỏi thường gặp, về lâu dài, cả NTCP và SSU sẽ cùng vận hành - chúng tôi sẽ không quay lại chỉ dùng TCP.

* eepsite(I2P Site) reachability

Mọi người lưu ý rằng eepsites(I2P Sites) chỉ truy cập được khi người vận hành đang bật nó - nếu nó ngừng hoạt động thì bạn không thể làm gì để truy cập được đâu ;) Rất tiếc, vài ngày vừa qua, orion.i2p không thể truy cập, nhưng mạng chắc chắn vẫn hoạt động - có lẽ hãy ghé qua inproxy.tino.i2p hoặc eepsites(I2P Sites).i2p cho nhu cầu khảo sát mạng của bạn.

Dù sao, còn rất nhiều điều đang diễn ra, nhưng nhắc đến ở đây thì hơi sớm. Tất nhiên, nếu bạn có bất kỳ thắc mắc hoặc lo ngại nào, hãy ghé qua #i2p trong vài phút nữa để tham gia cuộc họp phát triển *khụ* hằng tuần của chúng tôi.

Cảm ơn bạn đã giúp chúng tôi tiến về phía trước! =jr
