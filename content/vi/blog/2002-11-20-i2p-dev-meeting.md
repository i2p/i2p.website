---
title: "Cuộc họp các nhà phát triển I2P"
date: 2002-11-20
author: "nop"
description: "Cuộc họp phát triển I2P bao gồm các cập nhật về dự án và thảo luận kỹ thuật"
categories: ["meeting"]
---

(Cung cấp bởi Wayback Machine http://www.archive.org/)

## Tóm tắt nhanh

<p class="attendees-inline"><strong>Có mặt:</strong> al-jabr, Chocolate, dd0c, Fairwitness, goc, hezekiah, mids, nemesis, Neo, nop, Robert, sanity, sinster, tarpY, tc, zic</p>

## Nhật ký cuộc họp

<div class="irc-log"> --- Nhật ký được mở Tue Nov 19 23:51:34 2002
23:52 < logger> thử
23:52 -!- mode/#iip-dev [+o mids] by Trent
23:52 -!- mode/#iip-dev [+v logger] by mids
23:53 -!- mode/#iip-dev [+oo nop UserX] by mids
23:57 <@mids> cuộc họp IIP công khai trong kênh #iip-dev sẽ bắt đầu trong 2,5 phút
23:57 < nemesis> lol
23:57 < zic> có ai từ Ukrain không? nhắn tôi nhé! hehehe
23:58 -!- mode/#iip-dev [+o hezekiah] by mids
23:58 <@hezekiah> Chào lại, mids!
23:58 < Robert> Này Nemesis, bạn đã xem http://www.bash.org/?top chưa
23:58  * athena thấy hezekiah trong một diện mạo hoàn toàn mới :p
23:58 < nemesis> bash?
23:58 <@mids> Robert: họ đang bị down
23:58 <@mids> gì!
23:58 <@mids> họ đã trở lại!
--- Ngày đã chuyển sang Wed Nov 20 2002
00:00 <@mids> Tue Nov 19 23:00:00 UTC 2002
00:00 <@nop> chào mừng
00:00 <@nop> chào mừng
00:00 <@nop> đến cuộc họp thứ 20?
00:00 <@nop> cuộc họp IIP
00:00 <@hezekiah> thứ 20!
00:00 <@mids> đúng
00:00 <@nop> vâng trong chương trình nghị sự hôm nay...
00:01 <@nop> mids...
00:01 <@mids> 1) chào mừng
00:02 <@mids> 2) phát hành rc3
00:02 <@mids> 3) xem trước nhanh rc3
00:02 <@mids> 4) đồ ăn nhẹ và đồ uống
00:02 <@mids> 5) câu hỏi
00:02 <@mids> .
00:02 <@nop> cảm ơn
00:02 <@nop> ok
00:02 <@nop> vậy chúng ta sẽ phát hành chính thức rc3 vào thứ Năm
00:02 <@nop> vui lòng đánh dấu điều đó vào lịch của bạn
00:02 <@mids> hy vọng vậy :)
00:02 <@mids> (trừ khi sourceforge lại down)
00:03 <@nop> đúng, họ đã sửa vụ ro trên nfs chưa?
00:03 <@mids> rồi
00:03 <@nop> đó là lỗi của họ à?
00:03 < tarpY> tôi ở đây vì đồ ăn
00:03 <@mids> nhân tiện, nó đã được thông báo trên trang trạng thái của họ
00:03 <@nop> ok
00:03 <@mids> bảo trì
00:03 <@nop> hiểu rồi
00:03 <@nop> có lẽ đang sao lưu
00:03 < tarpY> tôi muốn đặt pizza qua freenet và phát hiện ra họ không nhận
00:03 <@nop> :)
00:03 < tarpY> tôi có thể lấy đồ ăn ở đâu ở đây
00:03 <@mids> tarpY: #muchnies-to-take-away
00:04 <@nop> ok
00:04 <@mids> những gì mới trong rc3:
00:04 <@nop> vậy thứ Năm chúng ta sẽ tung ra
00:04 <@nop> ồ
00:04 <@nop> Mids, tôi nghĩ bạn có sẵn changelog
00:04 <@nop> nếu không
00:04 <@mids> tôi cũng vậy
00:04 <@nop> tôi sẽ hiển thị
00:04 <@nop> ok
00:04 < sinster> rc3 sẽ có script cài đặt tử tế cho *nix chứ?
00:04 <@mids> - Hiển thị số phiên bản cho Windows (tùy chọn menu) và Unix (dòng lệnh).
00:04 <@mids> - Sửa lỗi tạo số ngẫu nhiên.
00:04 <@mids> - Kết nối mạng IIP không còn bị tạm dừng khi ở màn hình thiết lập.
00:04 <@mids> - Giờ sẽ thoát nếu không thể bind vào một socket khi khởi động.
00:04 <@mids>   Windows giờ sẽ hiển thị một hộp thoại thông báo rằng không thể bind vào cổng.
00:04 <@mids> - Nhiều bản sửa lỗi và đã sửa một lỗi rò rỉ bộ nhớ.
00:04 <@mids> .
00:04 <@mids> sinster: không, đó là thứ hezekiah đang làm
00:05 <@mids> cái đó sẽ là 1.2
00:05 <@hezekiah> Chưa hẳn ...
00:05 <@nop> ok
00:05 < zic> có kế hoạch dịch FAQ (hay) tại help.invisiblenet.net không?
00:05 <@nop> ai muốn dịch
00:05 <@nop> xin cứ làm
00:05 < sinster> mids/hezekiah: nó có thêm iip vào /etc/rc.d/ để tự động khởi động không?  chỉ là gợi ý
00:05 <@nop> chúng tôi rất trân trọng điều đó
00:05 <@nop> và sẽ đưa nó lên trang web
00:05 < zic> rc3 có yêu cầu chỉnh sửa gì trong FAQ không?
00:06 <@mids> sinster: tôi có một script ở đây... nhưng cần kiểm thử thêm
00:06 <@mids> sinster: có lẽ chúng tôi sẽ thêm cái đó trong 1.1 bản cuối
00:06 <@hezekiah> sinster: cái đó sẽ không tương thích giữa các bản phân phối, vì các distro khác nhau đặt phần khởi động ở những chỗ khác nhau.
00:06 <@mids> zic: không
00:06 < sinster> mids: ừ, nhớ kiểm thử trên các biến thể linux chính, redhat, debian v.v.
00:06 <@nop> ờ, chúng ta có thể chờ phần câu hỏi
00:06 <@nop> làm ơn
00:06 < zic> isproxy của tôi được script trong /etc/init.d (debian), chạy hoàn hảo
00:06 <@mids> oops
00:06 <@nop> đến phần hỏi đáp
00:06 < zic> xin lỗi!
00:06 < zic> xin lỗi!
00:06 <@hezekiah> Xin lỗi.
00:06 <@nop> nó trở nên rối
00:06 <@nop> ;)
00:06 <@nop> xin lỗi
00:06 < sinster> nop: ok
00:06 < tarpY> không cần dịch đâu, mọi người nên nói tiếng Anh.
00:07 < sinster> nop: lỗi của tôi
00:07 <@nop> không vấn đề
00:07 <@mids> có câu hỏi nào về changelog không?
00:07 <@mids> không?
00:07 <@mids> nop: xem trước nhanh?
00:07 <@nop> đợi tí relay của tôi vừa toi rồi
00:08 <@nop> đợi đến khi mọi người quay lại
00:08 <@mids> auch
00:08 <@nop> độ trễ có thể thật khó chịu trong một cuộc họp
00:08 <@nop> ;)
00:08 <@nop> mọi người vẫn ở đây chứ?
00:08 <@mids> có vẻ vậy
00:09 <@hezekiah> tôi không thấy ai rời đi.
00:09 <@nop> ok
00:09 < zic> tôi đây (tôi có quan trọng không? hehe)
00:09 <@nop> ờ thì chúng ta có tính năng delay
00:09 <@nop> ;)
00:09 <@nop> ok
00:09 < al-jabr> tôi cũng không.
00:09 <@nop> đoán là relay của tôi bị đá khỏi danh sách vì không ổn định
00:09 <@nop> haha
00:09 <@mids> hehe
00:09  * Robert tham gia #muchnies-to-take-away trong lúc chờ...
00:09 <@mids> được rồi
00:09 <@nop> ừ
00:10 <@nop> lại nữa rồi
00:10 <@nop> ;)
00:10 < al-jabr> mất năm người rồi.
00:10 <@hezekiah> Chúng ta thật sự cần làm gì đó về chuyện này. :(
00:10 < nemesis> ờm
00:10 < nemesis> mids
00:10 <@nop> hezekiah: spread spectrum routing (định tuyến trải phổ)
00:11 < tc> đây có phải là lỗi trục trặc trong hệ thống relay không?
00:11 <@nop> ;)
00:11 <@nop> máy relay Windows của tôi bị crash
00:11 <@nop> điển hình
00:11 < nemesis> cho win2k / xp, sau này sẽ có bản build không có GUI
00:11 <@hezekiah> lol
00:11 < nemesis> hoặc chỉ có GUI để thiết lập
00:11 < nemesis> và phần còn lại chạy như một daemon?
00:11 <@nop> sẽ hay nếu có nó như một service
00:11 <@nop> ;)
00:12 < nemesis> đúng
00:12 < nemesis> ;)
00:12 <@nop> có một chương trình ngoài kia tên là service installer
00:13 <@nop> ok
00:13 <@nop> ừ
00:13 < nemesis> iip.exe --install
00:13 <@nop> không trì hoãn nữa
00:13 < nemesis> như apache cho win
00:13 <@mids> mọi người đã quay lại hết chưa?
00:14 <@nop> ok
00:15 <@nop> chào mừng baci
00:15 <@nop> quay lại
00:15 < nemesis> Neo của Matrix à? ;)
00:15 <@nop> ok
00:15 <@nop> tôi nghĩ họ đã quay lại
00:16 <@mids> đúng
00:16 <@nop> ok
00:16 <@nop> xem trước nhanh
00:16 <@mids> Tôi đã tạo một FLT-iip.1.1-rc3-pre1-mids-sneak-preview-screaner.tgz
00:16 <@mids> ai dùng Unix đều có thể thử
00:16 <@mids> chưa có bản Windows
00:16 <@nop> tôi có thể làm một bản ngay bây giờ
00:16 <@nop> nếu bạn muốn
00:16 < zic> lol
00:16 <@mids> http://mids.student.utwente.nl/~mids/iip/iip-1.1-rc3-mids1.tgz
00:16 < nemesis> thế cũng được
00:16 < nemesis> tôi đợi
00:16 < zic> Âm thanh OGG hay LAME?
00:17 <@mids> Tôi đặc biệt mong các báo cáo về những bản Unix ít gặp
00:17 <@mids> như NetBSD v.v.
00:17 < nemesis> tôi nghĩ, không quá quan trọng khi một máy Unix crash sau 30 ngày uptime
00:17 <@mids> và MacOSX
00:17 < nemesis> so với một máy Windows với uptime 3 ngày ;)
00:17 < tc> mids:  thay đổi này chỉ ở isproxy hay còn ở phần relay khác nữa?
00:17 <@nop> không
00:17 <@nop> bạn giữ nguyên thiết lập của mình
00:17 <@nop> chúng ta đã thử xem nó có thể cài đè lên cái trước chưa
00:17 <@nop> hmm
00:18 <@nop> ghi chú lại
00:18 < zic> nemesis: nhưng sẽ tuyệt nếu nó không bao giờ crash. nhưng hãy dừng tán gẫu ở đây. chúng ta đang trong một cuộc họp trang trọng
00:18 < nemesis> hehe
00:18 <@nop> ok
00:18 <@nop> nếu ai muốn thử xem quá trình nâng cấp có đơn giản không
00:18 < nemesis> đừng thử vào ngày họp ;)
00:18 <@nop> thì xin cứ tiến hành
00:18 <@nop> và email hoặc báo cho một trong các dev về kết quả
00:18 <@mids> vui lòng thử nó song song với relay hiện tại của bạn
00:18 <@mids> và vâng, hãy phản hồi
00:19 <@mids> về những gì trục trặc
00:19 <@mids> v.v.
00:19 <@nop> chào mừng quay lại tarpY
00:19 <@nop> hãy đưa cái screener đó vào topic
00:19 < goc> có thể chạy isproxy-rc2 và isproxy-almost-rc3 đồng thời không?
00:19 <@nop> có
00:20 <@nop> thiết lập cổng khác nhau
00:20 <@nop> và không khó chút nào
00:20 < goc> file conf lưu ở đâu?
00:20 <@nop> nhưng rc3 nên có thể cài đè rc2
00:20 <@nop> bạn có thể phải làm một -f /dir
00:20 <@nop> hoặc bạn có thể để nó cài đè lên cài đặt rc2
00:21 < tarpY> cuối cùng các bạn có định bỏ proxy và tích hợp nó vào một client không? </div>
