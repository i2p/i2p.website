---
title: "Cuộc họp nhà phát triển I2P - ngày 01 tháng 6 năm 2004"
date: 2004-06-01
author: "duck"
description: "Biên bản cuộc họp phát triển I2P ngày 01 tháng 6 năm 2004."
categories: ["meeting"]
---

## Tóm tắt nhanh

<p class="attendees-inline"><strong>Có mặt:</strong> deer, duck, hypercubus, Masterboy, mihi, Nightblade, tessier, wilde</p>

## Nhật ký cuộc họp

<div class="irc-log"> [22:59] &lt;duck&gt; Tue Jun  1 21:00:00 UTC 2004 [23:00] &lt;duck&gt; chào mọi người! [23:00] &lt;mihi&gt; chào duck [23:00] &lt;duck&gt; http://dev.i2p.net/pipermail/i2p/2004-June/000250.html [23:00] &lt;duck&gt; đề xuất của tôi: [23:00] * Masterboy đã tham gia #i2p

[23:00] <duck> 1) tiến độ mã nguồn
[23:00] <duck> 2) nội dung nổi bật
[23:00] <duck> 3) trạng thái testnet (mạng thử nghiệm)
[23:00] <duck> 4) treo thưởng
[23:00] <duck> 5) ???
[23:00] <Masterboy> chào:)
[23:00] <duck> .
[23:01] <duck> vì jrandom đang off nên chúng ta sẽ phải tự làm
[23:01] <duck> (Tôi biết là anh ấy đang ghi log và xác minh tính độc lập của chúng ta)
[23:01] <Masterboy> không vấn đề gì:P
[23:02] <duck> trừ khi có vấn đề với chương trình nghị sự, tôi đề nghị chúng ta bám theo nó
[23:02] <duck> dù nếu mọi người không làm thì tôi cũng chẳng làm được gì nhiều :)
[23:02] <duck> .
[23:02] <mihi> ;)
[23:02] <duck> 1) tiến độ mã nguồn
[23:02] <duck> không có nhiều mã được commit vào cvs
[23:02] <duck> tuần này tôi có giành được chiếc cúp: http://duck.i2p/duck_trophy.jpg
[23:03] * hypercubus chưa có tài khoản cvs
[23:03] <Masterboy> vậy ai đã gửi gì?
[23:03] <duck> có ai đang viết mã bí mật không?
[23:03] * Nightblade đã tham gia #I2P

[23:03] &lt;hypercubus&gt; BrianR đang làm vài thứ
[23:04] &lt;hypercubus&gt; tôi đã hack được khoảng 20% của trình cài đặt 0.4
[23:04] &lt;duck&gt; hypercubus: nếu bạn có thứ gì thì cung cấp các diff và $dev sẽ commit giúp bạn
[23:04] &lt;duck&gt; tất nhiên là các thỏa thuận giấy phép nghiêm ngặt vẫn áp dụng
[23:05] &lt;duck&gt; hypercubus: hay đấy, có vấn đề / điều gì đáng nói không?
[23:06] &lt;hypercubus&gt; chưa, nhưng có lẽ tôi sẽ cần vài người bên BSD để thử các script shell của trình tiền cài đặt
[23:06] * duck lục lọi vài chỗ
[23:06] &lt;Nightblade&gt; nó chỉ có text thôi à
[23:07] &lt;mihi&gt; duck: trong duck_trophy.jpg, cái nào là bạn?
[23:07] &lt;mihi&gt; ;)
[23:07] &lt;Nightblade&gt; luckypunk có freebsd, ISP của tôi cũng có freebsd nhưng cấu hình của họ kiểu như bị rối tung
[23:07] &lt;Nightblade&gt; ý là ISP host web của tôi, không phải comcast
[23:08] &lt;duck&gt; mihi: bên trái, người đeo kính. wilde là anh chàng bên phải đưa cúp cho tôi
[23:08] * wilde vẫy tay
[23:08] &lt;hypercubus&gt; bạn có thể chọn... nếu bạn đã cài java, bạn có thể bỏ qua trình tiền cài đặt luôn...    nếu bạn chưa cài java thì bạn có thể chạy trình tiền cài đặt linux binary hoặc win32 binary (chế độ console), hoặc một    generic *nix (hệ điều hành kiểu Unix) script preinstaller (chế độ console)
[23:08] &lt;hypercubus&gt; trình cài đặt chính cho bạn chọn dùng chế độ console hoặc chế độ GUI bóng bẩy
[23:08] &lt;Masterboy&gt; tôi sẽ cài freebsd sớm nên về sau tôi cũng sẽ thử trình cài đặt
[23:09] &lt;hypercubus&gt; tốt, tôi không biết có ai ngoài jrandom đang dùng nó không
[23:09] &lt;Nightblade&gt; trên freebsd, java được gọi là "javavm" chứ không phải "java"
[23:09] &lt;hypercubus&gt; được build từ nguồn của Sun à?
[23:09] &lt;mihi&gt; freebsd hỗ trợ symlink ;)
[23:10] &lt;hypercubus&gt; dù sao thì trình tiền cài đặt dạng nhị phân đã hoàn tất 100%
[23:10] &lt;hypercubus&gt; biên dịch bằng gcj thành native
[23:11] &lt;hypercubus&gt; nó chỉ hỏi bạn thư mục cài đặt, và nó sẽ lấy một JRE cho bạn
[23:11] &lt;duck&gt; w00t
[23:11] &lt;Nightblade&gt; hay đấy
[23:11] &lt;hypercubus&gt; jrandom đang đóng gói một JRE tùy chỉnh cho i2p

[23:12] &lt;deer&gt; &lt;j&gt; .
[23:12] &lt;Nightblade&gt; nếu bạn cài java từ bộ sưu tập ports của freebsd, bạn dùng một script bao (wrapper) tên là    javavm
[23:12] &lt;deer&gt; &lt;r&gt; .
[23:12] &lt;hypercubus&gt; dù sao thì cái này sẽ gần như tự động hoàn toàn
[23:12] &lt;deer&gt; &lt;r&gt; .
[23:12] &lt;deer&gt; &lt;r&gt; .
[23:12] &lt;deer&gt; &lt;r&gt; .
[23:12] &lt;deer&gt; &lt;duck&gt; r: thôi đi
[23:12] &lt;deer&gt; &lt;r&gt; .
[23:12] &lt;deer&gt; &lt;m&gt; .
[23:13] &lt;deer&gt; &lt;m&gt; máy chủ irc ngu ngốc, không hỗ trợ pipelining :(
[23:13] &lt;duck&gt; hypercubus: có thời gian dự kiến (ETA) cho bọn mình không?
[23:14] &lt;deer&gt; &lt;m&gt; oops, vấn đề là "Nick change too fast" :(
[23:14] &lt;hypercubus&gt; tôi vẫn kỳ vọng xong trong vòng dưới một tháng, trước khi 0.4 chín muồi để phát hành
[23:14] &lt;hypercubus&gt; mặc dù hiện tại tôi đang biên dịch một HĐH mới cho hệ thống dev của mình, nên sẽ mất vài ngày    trước khi tôi quay lại với trình cài đặt ;-)
[23:14] &lt;hypercubus&gt; nhưng đừng lo
[23:15] &lt;duck&gt; ok. vậy tuần sau sẽ có thêm tin :)
[23:15] &lt;duck&gt; có code nào khác đã làm xong không?
[23:15] &lt;hypercubus&gt; hy vọng vậy... trừ khi công ty điện lại làm khổ tôi nữa
[23:16] * duck chuyển sang #2
[23:16] &lt;duck&gt; * 2) nội dung nổi bật
[23:16] &lt;duck&gt; tuần này đã làm xong khá nhiều phần phát audio trực tuyến (ogg/vorbis)
[23:16] &lt;duck&gt; baffled đang chạy luồng egoplay của anh ấy và tôi cũng đang chạy một luồng
[23:17] &lt;Masterboy&gt; và nó hoạt động khá tốt
[23:17] &lt;duck&gt; trên trang của chúng tôi bạn có thể lấy thông tin về cách sử dụng nó
[23:17] &lt;hypercubus&gt; có thống kê sơ bộ nào cho bọn tôi không?
[23:17] &lt;duck&gt; nếu bạn dùng một trình phát không được liệt kê ở đó và tự tìm ra cách dùng, hãy gửi chúng cho tôi và tôi sẽ    thêm
[23:17] &lt;Masterboy&gt; duck liên kết tới luồng của baffled trên trang của bạn ở đâu?
[23:17] &lt;Masterboy&gt; :P
[23:17] &lt;duck&gt; hypercubus: 4kB/s chạy khá ổn
[23:18] &lt;duck&gt; và với ogg thì cũng không tệ lắmmmm
[23:18] &lt;hypercubus&gt; nhưng đó vẫn có vẻ là tốc độ trung bình?
[23:18] &lt;duck&gt; theo quan sát của tôi thì đó là mức tối đa
[23:18] &lt;duck&gt; nhưng tất cả là chuyện tinh chỉnh cấu hình
[23:19] &lt;hypercubus&gt; có ý kiến vì sao đó có vẻ là mức tối đa không?
[23:19] &lt;hypercubus&gt; và tôi không chỉ nói về streaming ở đây
[23:19] &lt;hypercubus&gt; mà cả tải xuống nữa
[23:20] &lt;Nightblade&gt; hôm qua tôi tải một vài tệp lớn (vài megabyte) từ dịch vụ hosting    của duck và tôi cũng chỉ được khoảng 4kb-5kb
[23:20] &lt;duck&gt; tôi nghĩ đó là do rtt (độ trễ khứ hồi)
[23:20] &lt;Nightblade&gt; mấy phim Chips đó
[23:20] &lt;hypercubus&gt; 4-5 có vẻ là một cải thiện so với ~3 mà tôi nhận được đều đặn từ khi tôi bắt đầu dùng i2p

[23:20] &lt;Masterboy&gt; 4-5kb cũng không tệ..
[23:20] &lt;duck&gt; với kích thước cửa sổ là 1 bạn không thể nhanh hơn mấy..
[23:20] &lt;duck&gt; windowsize&gt;1 bounty: http://www.i2p.net/node/view/224
[23:21] &lt;duck&gt; mihi: có lẽ bạn có thể bình luận?
[23:21] &lt;hypercubus&gt; nhưng nó ổn định đến đáng kinh ngạc ở mức 3 kbps
[23:21] &lt;mihi&gt; về cái gì? windowsize&gt;1 với ministreaming: nếu bạn làm được thì đúng là phù thủy đấy ;)
[23:21] &lt;hypercubus&gt; không bị trục trặc trên đồng hồ băng thông... một đường khá mượt
[23:21] &lt;duck&gt; mihi: về lý do tại sao nó ổn định ở mức 4kb/s như vậy
[23:21] &lt;mihi&gt; không biết. tôi không nghe thấy âm thanh nào :(
[23:22] &lt;duck&gt; mihi: cho tất cả các truyền tải i2ptunnel
[23:22] &lt;Masterboy&gt; mihi bạn cần cấu hình plugin phát trực tuyến Ogg..
[23:22] &lt;mihi&gt; Masterboy:?
[23:23] &lt;mihi&gt; không, không có giới hạn về tốc độ bên trong i2ptunnel. chắc là ở router...
[23:23] &lt;duck&gt; tôi nghĩ thế này: kích thước gói tối đa: 32kB, rtt 5 giây: 32kB/5s =~ 6.5kb/s
[23:24] &lt;hypercubus&gt; nghe có vẻ hợp lý
[23:25] &lt;duck&gt; ok..
[23:25] &lt;duck&gt; nội dung khác:
[23:25] * hirvox đã tham gia #i2p

[23:25] <duck> có một eepsite mới từ Naughtious
[23:25] <duck> anonynanny.i2p
[23:25] <duck> khóa đã được commit vào cvs và anh ấy đã đưa nó lên wiki của ugha
[23:25] * mihi đang nghe "sitting in the ..." - duck++
[23:25] <Nightblade> xem liệu bạn có thể mở hai hoặc ba streams (luồng) ở tốc độ 4kb rồi bạn sẽ biết liệu nó    nằm trong router hay streaming lib
[23:26] <duck> Naughtious: bạn ở đó chứ? nói gì đó về kế hoạch của bạn đi :)
[23:26] <Masterboy> tôi đã đọc rằng anh ấy cung cấp hosting
[23:26] <duck> Nightblade: tôi đã thử 3 lượt tải song song từ baffled và tôi nhận được 3-4kB mỗi cái
[23:26] <Nightblade> tôi hiểu
[23:27] <mihi> Nightblade: vậy làm sao bạn biết được?
[23:27] * mihi thích nghe ở chế độ "stop&go" ;)
[23:27] <Nightblade> ừ, nếu có một loại giới hạn nào đó trong router mà chỉ cho phép xử lý 4kb mỗi lần
[23:27] <Nightblade> hoặc nếu đó là thứ gì khác
[23:28] <hypercubus> ai đó có thể giải thích site anonynanny này không? hiện tại tôi không có i2p router đang chạy
[23:28] <mihi> hypercubus: chỉ là một wiki hoặc dạng gì đó tương tự
[23:28] <duck> cài đặt Plone CMS, mở đăng ký tài khoản
[23:28] <duck> cho phép tải tệp lên và làm các thứ về website
[23:28] <duck> thông qua giao diện web
[23:28] <Nightblade> một việc khác là thử thông lượng của "repliable datagram", theo như tôi biết    nó giống như streams nhưng không có acks
[23:28] <duck> có lẽ khá giống Drupal
[23:28] <hypercubus> ừ, tôi từng chạy Plone trước đây
[23:29] <duck> Nightblade: tôi đã nghĩ về việc dùng airhook để quản lý những thứ đó
[23:29] <duck> nhưng tới giờ mới chỉ là vài ý tưởng cơ bản
[23:29] <hypercubus> nội dung wiki thì gì cũng được, hay tập trung vào thứ gì cụ thể?
[23:29] <Nightblade> tôi nghĩ airhook được cấp phép theo GPL
[23:29] <duck> giao thức
[23:29] <duck> không phải mã nguồn
[23:29] <Nightblade> à :)
[23:30] <duck> hypercubus: anh ấy muốn nội dung chất lượng, và để bạn cung cấp điều đó :)
[23:30] <Masterboy> tải lên pr0n ngon nhất của chính cậu đi, hyper ;P
[23:30] <duck> ok
[23:30] * Masterboy cũng sẽ thử làm thế
[23:30] <hypercubus> ừ, ai chạy một wiki mở là đang cầu xin nội dung chất lượng đấy ;-)
[23:31] <duck> ok
[23:31] * duck chuyển sang #3
[23:31] <duck> * 3) trạng thái testnet
[23:31] <Nightblade> Airhook xử lý tốt các mạng ngắt quãng, không đáng tin cậy, hoặc bị trễ  <-- hehe không phải là    mô tả lạc quan về I2P đâu!
[23:31] <duck> tình hình thế nào rồi?
[23:32] <duck> hãy để phần thảo luận datagram over i2p xuống cuối
[23:32] <tessier> tôi thích chạy vòng quanh các wiki mở và link tới cái này: http://www.fissure.org/humour/pics/squirre   l.jpg
[23:32] <tessier> airhook tuyệt vời
[23:32] <tessier> tôi cũng đã xem nó để xây dựng một mạng p2p.
[23:32] <Nightblade> đối với tôi có vẻ ổn định (#3)
[23:32] <Nightblade> tốt nhất tôi từng thấy đến giờ
[23:33] <duck> ừ
[23:33] <mihi> chạy tốt - ít nhất là cho stop&go audio streaming
[23:33] <duck> tôi thấy thời gian uptime khá ấn tượng trên irc
[23:33] <hypercubus> đồng ý... thấy nhiều người màu xanh hơn trong router console của tôi
[23:33] <Nightblade> mihi: bạn đang nghe techno à? :)
[23:33] <duck> nhưng khó mà biết vì bogobot có vẻ không xử lý các kết nối vượt qua 00:00
[23:33] <tessier> audio streaming chạy rất tốt với tôi nhưng tải website thường phải thử vài lần
[23:33] <Masterboy> tôi có ý kiến là i2p chạy rất tốt sau 6 giờ sử dụng; trong giờ thứ 6 tôi dùng irc    trong 7 giờ và vì vậy router của tôi đã chạy 13hours
[23:33] <duck> (*gợi ý*)
[23:34] <hypercubus> duck: ờ... heheh
[23:34] <hypercubus> tôi đoán tôi có thể sửa cái đó
[23:34] <hypercubus> bạn có đặt logging theo ngày không?
[23:34] <duck> hypercubus++
[23:34] <hypercubus> ý là xoay vòng log
[23:34] <duck> ồ có
[23:34] <duck> duck--
[23:34] <hypercubus> vì vậy đấy
[23:34] <Nightblade> tôi ở chỗ làm cả ngày, bật máy lên, khởi động i2p và vào irc server của duck    chỉ trong vài phút
[23:35] <duck> tôi đã thấy vài DNF kỳ lạ
[23:35] <duck> ngay cả khi kết nối đến chính các eepsites của tôi
[23:35] <duck> (http://dev.i2p.net/bugzilla/show_bug.cgi?id=74)
[23:35] <duck> tôi nghĩ đó là thứ gây ra hầu hết vấn đề hiện giờ
[23:35] <hypercubus> bogoparser chỉ phân tích các khoảng uptime nằm trọn trong một logfile duy nhất... vì vậy nếu    logfile chỉ bao trùm 24 giờ, sẽ không ai hiện lên là kết nối lâu hơn 24 giờ
[23:35] <duck> Masterboy và ughabugha cũng gặp nó, tôi nghĩ...
[23:36] <Masterboy> ừ
[23:36] <duck> (sửa được nó và bạn sẽ chắc chắn thắng chiếc cúp tuần sau!)
[23:37] <deer> <mihi> bogobot phấn khích à? ;)
[23:37] <Masterboy> tôi thử website của mình và đôi khi khi tôi nhấn refresh nó đi đường khác? và tôi phải    đợi nó tải nhưng tôi không bao giờ đợi ;P tôi nhấn lại và nó hiện ra ngay lập tức
[23:37] <deer> <mihi> úi, xin lỗi. quên mất là cái này được gated...
[23:38] <duck> Masterboy: các timeout có kéo dài 61 giây không?
[23:39] <duck> mihi: bogobot giờ đặt xoay vòng theo tuần
[23:39] * mihi đã thoát IRC ("tạm biệt, chúc họp vui vẻ")
[23:40] <Masterboy> xin lỗi tôi không kiểm tra trên website của mình; khi tôi không thể truy cập ngay lập tức tôi chỉ nhấn refresh    và nó tải ngay..
[23:40] <duck> hừm
[23:40] <duck> ừ, cái đó cần được sửa
[23:41] <duck> .... #4
[23:41] <Masterboy> tôi nghĩ tuyến (route) được chọn không giống nhau mỗi lần
[23:41] <duck> * 4) tiền thưởng
[23:41] <duck> Masterboy: các kết nối cục bộ nên được rút ngắn
[23:42] <duck> wilde có vài ý về tiền thưởng... bạn ở đó chứ?
[23:42] <Masterboy> có lẽ đó là bug chọn peer
[23:42] <wilde> tôi không chắc cái đó thực sự nằm trong chương trình họp
[23:42] <duck> ồ
[23:42] <wilde> ok nhưng ý tưởng đại khái là:
[23:42] <Masterboy> tôi nghĩ khi chúng ta công khai thì hệ thống tiền thưởng sẽ hoạt động tốt hơn
[23:43] <Nightblade> masterboy: đúng, có hai tunnel cho mỗi kết nối, hoặc ít nhất đó là cách tôi hiểu    khi đọc router.config
[23:43] <wilde> chúng ta có thể dùng tháng này để quảng bá nhẹ cho i2p và tăng quỹ tiền thưởng lên một chút
[23:43] <Masterboy> tôi thấy dự án Mute đang tiến triển tốt - họ nhận được 600$ và họ vẫn chưa code nhiều ;P
[23:44] <wilde> nhắm tới các cộng đồng tự do, người làm crypto, v.v.
[23:44] <Nightblade> tôi không nghĩ jrandom muốn quảng bá
[23:44] <wilde> không phải sự chú ý công khai kiểu slashdot, không
[23:44] <hypercubus> đó cũng là điều tôi quan sát thấy
[23:44] <Masterboy> tôi muốn thúc đẩy nó lần nữa - khi chúng ta công khai hệ thống sẽ hoạt động tốt hơn nhiều ;P
[23:45] <wilde> Masterboy: ví dụ, tiền thưởng có thể đẩy nhanh phát triển myi2p
[23:45] <Masterboy> và như jr nói, không công khai cho tới 1.0 và chỉ gây chú ý đôi chút sau 0.4
[23:45] <Masterboy> *đã viết
[23:45] <wilde> khi chúng ta có khoảng $500+ cho một khoản tiền thưởng, người ta thực sự có thể sống được vài tuần
[23:46] <hypercubus> điểm khó là, ngay cả khi chúng ta nhắm tới một cộng đồng dev nhỏ, như *cough* các dev Mute, những    người đó có thể lan truyền thông tin về i2p xa hơn mức chúng ta muốn
[23:46] <Nightblade> ai đó có thể làm cả sự nghiệp chỉ bằng cách sửa bug i2p
[23:46] <hypercubus> và quá sớm
[23:46] <wilde> các liên kết i2p đã ở rất nhiều nơi công khai rồi
[23:46] <Masterboy> bạn google là có thể tìm thấy i2p

[23:47] &lt;hypercubus&gt; những chỗ công cộng ít người biết ;-) (tôi thấy link i2p trên một freesite (trang Freenet)... tôi còn may là cái freesite chết tiệt đó    còn tải lên được!)
[23:47] &lt;wilde&gt; http://en.wikipedia.org/wiki/I2p
[23:47] &lt;Masterboy&gt; nhưng tôi đồng ý là không quảng bá cho đến khi 0.4 xong
[23:47] &lt;Masterboy&gt; cái gì???????
[23:47] &lt;wilde&gt; http://www.ovmj.org/GNUnet/links.php3?xlang=English
[23:48] &lt;Masterboy&gt; protol0l làm rất tốt;P
[23:48] &lt;Masterboy&gt; ;))))))
[23:48] &lt;hypercubus&gt; lỗi gõ dễ thương ;-)
[23:48] &lt;wilde&gt; ok dù sao thì, tôi đồng ý là chúng ta vẫn nên giữ I2P riêng tư (jr đọc log này ;)
[23:49] &lt;Masterboy&gt; ai làm vậy?
[23:49] &lt;Masterboy&gt; tôi nghĩ cuộc thảo luận của nhóm Freenet đã thu hút nhiều chú ý hơn..
[23:50] &lt;Masterboy&gt; và jr thảo luận với toad đã đưa rất nhiều thông tin tới số đông..
[23:50] &lt;Masterboy&gt; vậy nên như trong wiki của ughas - tất cả chúng ta có thể đổ lỗi cho jr vì chuyện đó ;P
[23:50] &lt;wilde&gt; ok dù sao thì, chúng ta sẽ xem liệu có thể mang về chút $ mà không kéo theo /..
[23:50] &lt;Masterboy&gt; đồng ý
[23:50] &lt;hypercubus&gt; danh sách dev của freenet khó mà tôi gọi là "đại chúng" ;-)
[23:50] &lt;wilde&gt; .
[23:51] &lt;hypercubus&gt; wilde: cậu sẽ có nhiều $ sớm hơn cậu nghĩ ;-)
[23:51] &lt;wilde&gt; ôi thôi nào, ngay cả mẹ tôi cũng đăng ký vào freenet-devl
[23:51] &lt;duck&gt; mẹ tôi đọc qua gmame
[23:51] &lt;deer&gt; &lt;clayboy&gt; freenet-devl đang được dạy trong các trường học ở đây
[23:52] &lt;wilde&gt; .
[23:52] &lt;Masterboy&gt; vậy là chúng ta sẽ thấy nhiều tiền thưởng (bounty) hơn sau khi 0.4 ổn định..
[23:53] &lt;Masterboy&gt; tức là sau 2 tháng ;P
[23:53] &lt;wilde&gt; duck đi đâu rồi?
[23:53] &lt;duck&gt; cảm ơn wilde  
[23:53] &lt;hypercubus&gt; dù là người duy nhất đòi bounty đến giờ, tôi phải nói rằng số tiền thưởng không    ảnh hưởng gì đến quyết định nhận thử thách của tôi
[23:54] &lt;wilde&gt; hehe, nó sẽ có nếu nó lớn gấp 100 lần
[23:54] &lt;duck&gt; bạn tốt quá so với thế gian này
[23:54] &lt;Nightblade&gt; haha
[23:54] * duck chuyển sang #5
[23:54] &lt;hypercubus&gt; wilde, $100 chẳng có nghĩa lý gì với tôi ;-)
[23:54] &lt;duck&gt; 100 * 10 = 1000
[23:55] * duck pops("5 airhook")
[23:55] &lt;duck&gt; tessier: có kinh nghiệm thực tế với nó không
[23:55] &lt;duck&gt; (http://www.airhook.org/)
[23:55] * Masterboy sẽ thử cái này:P
[23:56] &lt;duck&gt; bản cài đặt java (không biết nó có chạy không nữa) http://cvs.ofb.net/airhook-j/
[23:56] &lt;duck&gt; bản cài đặt python (lộn xộn, từng chạy trước đây) http://cvs.sourceforge.net/viewcvs.py/khashmir   /khashmir/airhook.py
[23:58] * duck mở van xả càm ràm
[23:58] &lt;Nightblade&gt; bản j cũng gpl
[23:58] &lt;duck&gt; chuyển nó sang pubdomain (public domain - miền công cộng)
[23:58] &lt;hypercubus&gt; amen
[23:58] &lt;Nightblade&gt; toàn bộ tài liệu giao thức chỉ khoảng 3 trang - không thể khó đến thế
[23:59] &lt;Masterboy&gt; không có gì là khó
[23:59] &lt;Masterboy&gt; chỉ là không dễ thôi
[23:59] &lt;duck&gt; tôi không nghĩ nó đã được đặc tả đầy đủ đâu
[23:59] * hypercubus lấy hết bánh quy may mắn của masterboy
[23:59] &lt;duck&gt; có thể bạn sẽ phải lặn vào mã C để tìm một bản triển khai tham chiếu
[00:00] &lt;Nightblade&gt; tôi tự làm cũng được nhưng giờ tôi bận với mấy thứ khác của i2p
[00:00] &lt;Nightblade&gt; (và cả công việc toàn thời gian của tôi)
[00:00] &lt;hypercubus&gt; duck: hay là treo bounty cho việc này?
[00:00] &lt;Nightblade&gt; đã có rồi
[00:00] &lt;Masterboy&gt; ?
[00:00] &lt;Masterboy&gt; à Pseudonyms
[00:00] &lt;duck&gt; nó có thể được dùng ở 2 tầng
[00:00] &lt;duck&gt; 1) như một transport (lớp truyền tải) bên cạnh TCP
[00:01] &lt;duck&gt; 2) như một giao thức để xử lý datagram bên trong i2cp/sam
[00:01] &lt;hypercubus&gt; vậy thì đáng để cân nhắc nghiêm túc đấy
[00:01] &lt;hypercubus&gt; &lt;/obvious&gt;

[00:02] &lt;Nightblade&gt; duck: tôi nhận thấy rằng repliable datagram trong SAM có kích thước tối đa 31kb, trong khi    stream (luồng) có kích thước tối đa 32kb - khiến tôi nghĩ rằng destination của người gửi (đích I2P) được gửi kèm theo mỗi gói trong    chế độ datagram có thể trả lời, và chỉ được gửi ở phần đầu đối với chế độ stream -
[00:02] &lt;Masterboy&gt; ờ thì airhook cvs không được cập nhật cho lắm..
[00:03] &lt;Nightblade&gt; khiến tôi nghĩ rằng sẽ không hiệu quả nếu xây dựng một giao thức trên nền các datagram có thể trả lời    qua sam
[00:03] &lt;duck&gt; kích thước thông điệp của airhook là 256 byte, còn i2cp là 32kb, nên bạn tối thiểu cũng phải đổi chút
[00:04] &lt;Nightblade&gt; thực ra nếu bạn muốn làm giao thức trong SAM bạn có thể chỉ dùng datagram ẩn danh    và để gói đầu tiên chứa destination của người gửi.... blah blah blah - tôi có nhiều ý tưởng lắm nhưng    không đủ thời gian để viết code
[00:06] &lt;duck&gt; nhưng rồi bạn lại gặp vấn đề xác minh chữ ký
[00:06] &lt;duck&gt; nên ai đó có thể gửi các gói tin giả tới bạn
[00:06] &lt;Masterboy&gt; chủ đề:::: SAM
[00:06] &lt;Masterboy&gt; ;P
[00:07] &lt;Nightblade&gt; đúng
[00:08] &lt;Nightblade&gt; nhưng nếu bạn gửi ngược lại tới destination đó và không có xác nhận thì bạn sẽ biết đó là    kẻ giả mạo
[00:08] &lt;Nightblade&gt; sẽ phải có một handshake
[00:08] &lt;duck&gt; nhưng bạn sẽ cần các handshake ở tầng ứng dụng cho việc đó
[00:08] &lt;Nightblade&gt; không, không hẳn
[00:09] &lt;Nightblade&gt; chỉ cần đặt nó trong một thư viện để truy cập SAM
[00:09] &lt;Nightblade&gt; nhưng đó là cách làm tệ
[00:09] &lt;Nightblade&gt; ý là làm như vậy
[00:09] &lt;duck&gt; bạn cũng có thể dùng các tunnels tách biệt
[00:09] &lt;Nightblade&gt; nó nên nằm trong streaming lib
[00:11] &lt;duck&gt; ừ. hợp lý
[00:12] &lt;duck&gt; ok
[00:12] &lt;duck&gt; Tôi đang thấy *baff*-y
[00:13] &lt;Nightblade&gt; ja
[00:13] * duck *baffs* </div>
