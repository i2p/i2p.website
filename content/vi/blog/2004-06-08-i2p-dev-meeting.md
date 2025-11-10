---
title: "Cuộc họp nhà phát triển I2P - ngày 08 tháng 6 năm 2004"
date: 2004-06-08
author: "duck"
description: "Nhật ký cuộc họp phát triển I2P ngày 08 tháng 6 năm 2004."
categories: ["meeting"]
---

## Quick recap

<p class="attendees-inline"><strong>Có mặt:</strong> cervantes, deer, duck, fvw, hypercubus, mihi, Nightblade, Sonium, ugha_node</p>

## Nhật ký cuộc họp

<div class="irc-log"> 21:02:08 &lt;duck&gt; Tue Jun  8 21:02:08 UTC 2004 21:02:21 &lt;duck&gt; đến giờ họp 21:02:33 &lt;duck&gt; bài viết ở http://dev.i2p.net/pipermail/i2p/2004-June/000268.html 21:02:39 &lt;duck&gt; nhưng tôi đã mắc lỗi trong việc đánh số 21:02:45 &lt;duck&gt; vì vậy mục số 5 đầu tiên sẽ bị bỏ qua 21:02:53 &lt;hypercubus&gt; tuyệt! 21:03:03  * duck bỏ ít đá vào bia 21:03:14  * mihi sẽ đổi #5 đầu tiên thành #4 ;) 21:03:27 &lt;hypercubus&gt; thôi, tuần sau chúng ta cứ có hai mục 4 ;-) 21:03:37  * duck đổi tên 'hypercubus' thành 'mihi' 21:03:48 &lt;hypercubus&gt; tuyệt! 21:03:49 &lt;duck&gt; ok 21:03:53 &lt;duck&gt; * 1) libsam 21:04:02 &lt;duck&gt; có Nightblade trong kênh không? 21:04:39 &lt;duck&gt; (nhàn rỗi     : 0 ngày 0 giờ 0 phút 58 giây) 21:05:03 &lt;hypercubus&gt; ;-) 21:05:53  * duck giành lại micro 21:06:15 &lt;duck&gt; Nightblade đã viết một thư viện SAM cho C / C++ 21:06:23 &lt;duck&gt; nó biên dịch được trên máy tôi.. nhưng tôi chỉ có thể nói thế :) 21:06:37 &lt;mihi&gt; không có ca kiểm thử nào à? ;) 21:07:06 &lt;duck&gt; nếu có người dùng rFfreebsd nào, Nightblade có thể sẽ quan tâm đến bạn 21:07:08 &lt;ugha_node&gt; Các lời gọi strstr trong mã làm tôi bực mình lắm. ;) 21:07:27 &lt;ugha_node&gt; duck: rFfreebsd là gì vậy? 21:07:42 &lt;duck&gt; cách tôi gõ freebsd thôi 21:08:00 &lt;mihi&gt; rm -rF freebsd? 21:08:29 &lt;ugha_node&gt; Tiếc là -F không hoạt động với rm. 21:08:30 &lt;duck&gt; ugha_node: nó dùng giấy phép BSD; vậy thì sửa đi 21:08:41 &lt;fvw&gt; nghe hợp lý với tôi :). Tiếc là tôi đã gỡ cài đặt cái máy freebsd cuối cùng cách đây không lâu. Tôi                  có tài khoản trên máy của người khác, và sẵn sàng chạy các ca kiểm thử. 21:08:43 &lt;ugha_node&gt; duck: có thể tôi sẽ làm. :) 21:08:50 &lt;duck&gt; (mấy hippie BSD chết tiệt) 21:09:09 &lt;duck&gt; ồ, ngắn gọn đấy, frank 21:09:17 &lt;duck&gt; còn bình luận nào về libsam không? 21:09:49 &lt;duck&gt; fvw: tôi đoán Nightblade sẽ liên hệ với bạn nếu anh ấy cần 21:09:50  * fvw càu nhàu về hành vi hoàn toàn hợp lý của unix khi giết irc client của mình. 21:10:02 &lt;duck&gt; nhưng vì email của anh ấy đã được một tuần nên có thể anh ấy đã tìm ra gì đó 21:10:17 &lt;mihi&gt; fvw: ? 21:10:24 &lt;fvw&gt; ừ, nếu ai muốn nhận đề nghị của tôi thì tôi đã bỏ lỡ mất rồi. Cứ                  thoải mái gửi email hay gì đó. 21:10:42  * duck nhảy sang #2 21:10:46 &lt;hypercubus&gt; ừm, sang đâu? ;-) 21:10:54 &lt;duck&gt; 2) duyệt i2p và web bình thường bằng một trình duyệt 21:10:57 &lt;fvw&gt; cài mới, vẫn chưa dặn zsh đừng hup các thứ chạy nền.                  &lt;/offtopic&gt;

21:11:09 &lt;fvw&gt; hypercubus: Tôi nghĩ tôi ở trong danh sách người dùng của mailing list công khai. fvw.i2p@var.cx
21:12:11 &lt;duck&gt; đã có vài thứ về việc thêm tất cả các TLD (miền cấp cao nhất) vào danh sách bỏ qua proxy của trình duyệt bạn
21:12:23 &lt;fvw&gt; điều đó có cần thảo luận không? Tôi nghĩ nó hầu như đã được xử lý trên                  mailinglist.
21:12:24 &lt;duck&gt; Tôi nghĩ đó là một hack bẩn
21:12:36 &lt;fvw&gt; vâng, điều đó đã được nhắc đến. Chào mừng quay lại.
21:12:47 &lt;duck&gt; fvw: Tôi chưa đọc chủ đề đó :)
21:13:12 &lt;duck&gt; được thôi, nếu bạn không muốn bàn về nó, chuyển sang #3
21:13:19 &lt;duck&gt; * 3) kênh chat
21:13:23 &lt;hypercubus&gt; script của cervantes chạy hoàn hảo trên Konqueror 3.2.2, Firefox 0.8, và                         Opera 7.51, tất cả trên Gentoo w/KDE 3.2.2
21:13:39  * mihi đặt cờ vào #4
21:13:55 &lt;duck&gt; #i2p-chat là một kênh thay thế ở đây cho chat lạc đề và hỗ trợ nhẹ
21:14:08 &lt;duck&gt; Tôi không biết ai đã đăng ký nó
21:14:12 &lt;hypercubus&gt; tôi đã làm
21:14:17 &lt;duck&gt; vậy thì tốt nhất là cẩn thận nhé :)
21:14:22 &lt;fvw&gt; ờm, không có #4 đâu, chỉ có hai #5 thôi :)
21:14:33 &lt;hypercubus&gt; tôi sẽ coi là may mắn nếu tôi nhớ được mật khẩu khi cần tới nó ;-)
21:14:33 &lt;mihi&gt; [22:27] -ChanServ-      Kênh: #i2p-chat
21:14:33 &lt;mihi&gt; [22:27] -ChanServ-      Liên hệ: hypercubus &lt;&lt;ONLINE&gt;&gt;

21:14:33 &lt;mihi&gt; [22:27] -ChanServ-    Biệt danh thay thế: cervantes &lt;&lt;ONLINE&gt;&gt;
21:14:37 &lt;mihi&gt; [22:27] -ChanServ-   Đăng ký: 4 ngày trước (0h 2m 41s)
21:15:12 &lt;hypercubus&gt; tôi đã trao quyền op (operator) cho vài người đáng tin để khi tôi không có mặt và                         có rắc rối
21:15:24 &lt;duck&gt; nghe ổn đấy
21:15:39 &lt;duck&gt; có thể hơi quá tay
21:15:51 &lt;hypercubus&gt; trên IRC thì chẳng biết trước được đâu ;-)
21:15:55 &lt;duck&gt; nhưng sau khi cô protogirl này vào đây tôi nghĩ dọn dẹp                   kênh này chút cũng tốt
21:16:03 &lt;hypercubus&gt; heh
21:16:27 &lt;hypercubus&gt; kiểu gì rồi trong vài tháng tới cũng sẽ cần thôi
21:16:34 &lt;duck&gt; ừ
21:16:48 &lt;duck&gt; và rồi bên freenode sẽ đá chúng ta ra 
21:16:55 &lt;hypercubus&gt; ;-)
21:17:13 &lt;duck&gt; họ không thích thứ gì không được viết trong 'kampf' của họ
21:17:16 &lt;duck&gt; ờ
21:17:44  * duck chuyển sang $nextitem và kích hoạt breakpoint của mihi
21:17:47 &lt;hypercubus&gt; tôi nghĩ gắn kênh mới với hỗ trợ sẽ hợp thức hóa nó đối với                         freenode
21:18:47 &lt;duck&gt; hypercubus: bạn có thể sẽ bất ngờ đấy
21:19:04 &lt;hypercubus&gt; *khụ* thú thật là tôi không đọc hết các chính sách...
21:19:24 &lt;duck&gt; đó là trò cò quay Nga
21:19:39 &lt;hypercubus&gt; hmm, tôi không nghĩ là nó lại nghiêm trọng đến thế
21:19:52  * duck đang hơi bi quan
21:19:54 &lt;hypercubus&gt; thôi để tôi xem chúng ta có thể làm gì
21:20:09 &lt;fvw&gt; xin lỗi, chắc tôi bỏ lỡ gì đó. Tại sao freenode lại đá chúng ta đi?
21:20:21  * duck nhìn bộ đếm timeout cho breakpoint của mihi
21:20:32 &lt;duck&gt; fvw: họ tập trung vào các kênh phát triển
21:20:35 &lt;mihi&gt; ?
21:20:53 &lt;mihi&gt; duck: breakpoint kích hoạt khi gặp /^4).*/
21:21:01 &lt;duck&gt; mihi: nhưng không có #4 mà
21:21:06 &lt;fvw&gt; rồi sao? i2p còn alpha đến mức ngay lúc này cả hỗ trợ cũng là phát triển.
21:21:11 &lt;fvw&gt; (và không, đừng trích dẫn tôi câu đó)
21:21:36 &lt;duck&gt; fvw: có thể bạn không quen với kiểu thảo luận từng diễn ra                   trên IIP
21:21:38 &lt;hypercubus&gt; ừ nhưng chúng ta có *2* kênh cho việc đó
21:21:45 &lt;duck&gt; và rất có thể sẽ xảy ra trong các kênh #i2p
21:22:04 &lt;duck&gt; tôi khá chắc freenode chẳng hề thích điều đó.
21:22:10 &lt;Nightblade&gt; tôi đây rồi
21:22:49 &lt;hypercubus&gt; chúng ta sẽ tặng họ một cái máy pha margarita hay gì đó
21:22:49 &lt;mihi&gt; duck: bạn đang nói đến gì? các đợt flood? hay #cl? hay gì?
21:23:08 &lt;fvw&gt; thảo luận trên IIP hay trên #iip? Tôi chưa từng thấy gì ngoài                  phát triển và hỗ trợ trên #iip. Và các thảo luận trên IIP sẽ chuyển sang I2P, không                  phải #i2p@freenode.
21:23:09 &lt;duck&gt; đủ kiểu nói năng không 'politically correct'
21:23:36 &lt;fvw&gt; có máy pha margarita à? Ô, tôi muốn một cái.
21:23:54 &lt;duck&gt; ờ thì thôi
21:24:38 &lt;hypercubus&gt; chúng ta xem lại mục 2) chứ?
21:24:58 &lt;duck&gt; hypercubus: bạn có gì bổ sung về proxy trình duyệt?
21:25:18 &lt;hypercubus&gt; úi, số 1... vì nightblade vừa ghé thăm vinh hạnh chúng ta ;-)
21:25:33 &lt;duck&gt; Nightblade: bọn tôi đã tự ý 'thảo luận' libsam
21:25:42 &lt;Nightblade&gt; Được, tôi sẽ nói vài dòng
21:25:48 &lt;hypercubus&gt; nhưng ừ tôi có một điều chưa nêu trên danh sách thư về chuyện                         trình duyệt nữa, giờ mới nhớ
21:25:56 &lt;duck&gt; Nightblade: fvw bảo có thể giúp một số thử nghiệm trên freebsd
21:26:20 &lt;fvw&gt; Tôi không còn máy freebsd nữa nhưng tôi có tài khoản trên các                  máy freebsd, đưa tôi các test case và tôi sẽ vui lòng chạy chúng.
21:27:02 &lt;Nightblade&gt; Tôi đã bắt đầu làm một dht C++, dùng Libsam (C).  Đến lúc                         này tôi chưa tiến được quá xa dù đã làm khá nhiều.  Hiện tại các nút trong dht có thể "ping" lẫn nhau qua một thông điệp dữ liệu sam
21:27:09 &lt;Nightblade&gt; trong quá trình đó tôi phát hiện vài lỗi nhỏ trong libsam
21:27:18 &lt;Nightblade&gt; tôi sẽ đăng một phiên bản mới vào lúc nào đó trong tương lai
21:27:51 &lt;ugha_node&gt; Nightblade: Bạn có thể bỏ mấy chỗ gọi 'strstr' khỏi libsam được không? :)
21:27:52 &lt;Nightblade&gt; test case là: thử biên dịch nó và báo lỗi cho tôi
21:28:01 &lt;Nightblade&gt; strstr có gì sai à
21:28:21 &lt;ugha_node&gt; Nó không được dùng thay cho strcmp.
21:28:38 &lt;Nightblade&gt; à đúng rồi, tôi cũng sẽ port libsam sang Windows, nhưng đó                         không phải tương lai gần
21:29:07 &lt;Nightblade&gt; có gì sai với cách tôi dùng nó không, ngoài chuyện thẩm mỹ?
21:29:15 &lt;Nightblade&gt; bạn có thể gửi cho tôi các thay đổi hoặc nói bạn muốn làm gì
21:29:19 &lt;Nightblade&gt; cách đó có vẻ là dễ nhất
21:29:21 &lt;ugha_node&gt; Nightblade: Tôi không thấy có.
21:29:32 &lt;fvw&gt; tất nhiên strcmp hiệu quả hơn strstr.
21:29:36 &lt;ugha_node&gt; Nhưng tôi chỉ lướt qua thôi.
21:30:20 &lt;ugha_node&gt; fvw: Thỉnh thoảng có thể khai thác những thứ dùng strstr thay vì                        strcmp, nhưng không phải trường hợp này.
21:31:22 &lt;Nightblade&gt; ừ giờ tôi thấy vài chỗ có thể thay đổi
21:31:28 &lt;fvw&gt; điều đó cũng đúng, nhưng tôi đoán bạn đã để ý rồi. Thực ra bạn sẽ                  phải dùng strncmp để ngăn các kiểu khai thác đó. Nhưng đó là chuyện khác.
21:31:31 &lt;Nightblade&gt; tôi không nhớ vì sao tôi làm như vậy
21:31:57 &lt;ugha_node&gt; fvw: Tôi đồng ý.
21:32:27 &lt;Nightblade&gt; à giờ tôi nhớ vì sao rồi
21:32:40 &lt;Nightblade&gt; đó là cách lười để khỏi phải tính độ dài cho strncmp
21:32:49 &lt;duck&gt; heh
21:32:52 &lt;ugha_node&gt; Nightblade: Heheh.
21:33:01 &lt;fvw&gt; dùng min(strlen(foo), sizeof(*foo))
21:33:04 &lt;hypercubus&gt; bắt đầu đánh đòn chứ?
21:33:15 &lt;fvw&gt; tôi tưởng 'oral sex' sẽ đến trước? *cúi đầu né*
21:33:32 &lt;fvw&gt; được rồi, điểm tiếp theo thì phải. Hypercube có ý kiến về proxy?
21:33:38 &lt;hypercubus&gt; heh
21:33:54 &lt;duck&gt; vô đi!
21:34:03 &lt;Nightblade&gt; tôi sẽ thực hiện các thay đổi cho phiên bản tới - ít nhất là                         thay đổi một số chỗ
21:34:25 &lt;hypercubus&gt; ok, chuyện này đã được bàn qua trong kênh vài tuần trước,                         nhưng tôi nghĩ đáng để xem lại
21:34:48 &lt;deer&gt; * Sugadude xung phong thực hiện 'oral sex'.
21:34:59 &lt;hypercubus&gt; thay vì thêm các TLD vào danh sách chặn của trình duyệt, hoặc dùng                         proxy script, còn một cách thứ ba
21:35:29 &lt;hypercubus&gt; mà về mặt ẩn danh thì không có các nhược điểm giống hai cách kia
21:36:17 &lt;fvw&gt; và tôi sẽ nói cho bạn với mức giá siêu rẻ $29.99? Nói ra đi nào!
21:36:27 &lt;hypercubus&gt; và đó là để eeproxy viết lại các trang HTML đến để                         nhúng trang vào một frameset...  
21:36:58 &lt;hypercubus&gt; frame chính sẽ chứa nội dung HTTP được yêu cầu, frame                         còn lại sẽ đóng vai trò thanh điều khiển
21:37:13 &lt;hypercubus&gt; và cho phép bạn bật/tắt proxy tùy ý
21:37:40 &lt;hypercubus&gt; và cũng sẽ cảnh báo bạn, có thể bằng viền màu hay kiểu cảnh                         báo nào đó, rằng bạn đang duyệt không ẩn danh
21:37:54 &lt;fvw&gt; bạn định ngăn một site i2p (có JavaScript v.v.) khỏi việc tắt                  ẩn danh bằng cách nào?
21:37:59  * duck cố áp dụng mức độ khoan dung jrandom-skill-level-of
21:37:59 &lt;hypercubus&gt; hoặc rằng một liên kết trong trang eepsite dẫn ra RealWeb(tm)
21:38:04 &lt;duck&gt; ngầu đấy! làm đi!
21:38:16 &lt;fvw&gt; bạn vẫn sẽ phải làm thứ gì đó kiểu fproxy, hoặc làm một thứ                  không do trình duyệt điều khiển để chuyển đổi.
21:38:29 &lt;ugha_node&gt; fvw: Chuẩn.
21:39:10 &lt;hypercubus&gt; đó là lý do tôi nêu lại ở đây, hy vọng ai đó có                         ý tưởng về cách bảo đảm an toàn cho việc này
21:39:31 &lt;hypercubus&gt; nhưng theo tôi đây là thứ sẽ rất cần thiết cho đa số i2p end                         usrers
21:39:33 &lt;hypercubus&gt; *users
21:40:04 &lt;hypercubus&gt; vì các cách TLD/proxy script/trình duyệt riêng là quá sức                         với người dùng mạng phổ thông
21:40:29 &lt;fvw&gt; Về lâu dài, tôi nghĩ một thứ tương tự fproxy là ý tưởng tốt nhất. Nhưng đó                  chắc chắn không phải ưu tiên theo ý tôi, và thật ra tôi không nghĩ duyệt web sẽ                  là killer app của i2p.
21:40:42 &lt;Sonium&gt; rốt cuộc netDb là gì vậy?
21:40:59 &lt;duck&gt; Sonium: cơ sở dữ liệu các router đã biết
21:41:10 &lt;hypercubus&gt; fproxy quá rườm rà đối với đa số người dùng
21:41:32 &lt;Sonium&gt; một cơ sở dữ liệu như vậy chẳng làm tổn hại tính ẩn danh sao?
21:41:39 &lt;hypercubus&gt; theo tôi đó là một phần lý do freenet chẳng bao giờ phổ biến trong                         cộng đồng không phải dev
21:41:41 &lt;fvw&gt; hypercube: không hẳn. proxy autoconfiguration ("pac") có thể làm nó đơn                  giản như điền một giá trị vào cấu hình trình duyệt. Tôi nghĩ ta không nên đánh                  giá thấp thực tế rằng trong tương lai gần, tất cả người dùng i2p sẽ ít nhất                  cũng có chút hiểu biết về máy tính. (bất chấp mọi bằng chứng trên                  freenet-support)
21:42:00 &lt;ugha_node&gt; Sonium: Không, 'kẻ xấu' dù sao cũng có thể thu thập thông tin đó thủ công.
21:42:21 &lt;Sonium&gt; nhưng nếu NetDb sập thì i2p cũng sập, đúng không?
21:42:29 &lt;fvw&gt; hypercubus: Không hẳn, tôi nghĩ việc nó chẳng hoạt động gì kể từ                  đầu 0.5 mới là nguyên nhân đáng trách hơn. &lt;/offtopic time="once again"&gt;

21:42:44 &lt;fvw&gt; Sonium: bạn có thể có nhiều hơn một netdb (ai cũng có thể vận hành một cái) 21:42:58 &lt;hypercubus&gt; chúng ta đã có pac, và mặc dù nó hoạt động cực kỳ ấn tượng về mặt kỹ thuật                         nhưng thực tế thì nó sẽ không bảo vệ được tính ẩn danh của                         the avg. jog 21:43:03 &lt;hypercubus&gt; *avg. joe 21:43:22 &lt;ugha_node&gt; fvw: Ờ.. Mỗi router đều có netDb riêng của nó. 21:43:42 &lt;duck&gt; ok. Tôi sắp ngất đây. nhớ *baff* đóng cuộc họp sau khi các bạn                   xong việc 21:43:52 &lt;ugha_node&gt; I2P không còn phụ thuộc trung tâm nữa. 21:44:07 &lt;hypercubus&gt; ok, mình chỉ muốn ghi lại ý tưởng này một cách chính thức vào log ;-) 21:44:30 &lt;fvw&gt; ugha_node: ok, vậy là một netdb đã công bố. Tôi thực ra chưa vận hành một node (chưa), tôi                  cũng chưa nắm vững toàn bộ thuật ngữ. 21:44:34 &lt;ugha_node&gt; Hmm. Chẳng phải mihi muốn nói gì đó sao? 21:45:05  * fvw đút cho duck sô-cô-la vị cà phê để giữ anh ấy tỉnh táo và hoạt động thêm            một lúc nữa. 21:45:07 &lt;mihi&gt; không :) 21:45:21 &lt;mihi&gt; duck có phải là một thiết bị mạng không? ;) 21:45:25 &lt;ugha_node&gt; mihi: Nhân tiện, anh có định nhận khoản tiền thưởng (bounty) tăng kích thước cửa sổ không? 21:45:28  * fvw đút cho duck sô-cô-la vị rượu để tắt anh ấy vĩnh viễn. 21:45:30 &lt;hypercubus&gt; bằng tiếng Thụy Điển 21:45:52 &lt;mihi&gt; ugha_node: bounty nào? 21:46:00 &lt;hypercubus&gt; được rồi, vậy chuyển sang mục 5), rant-a-rama? ;-) 21:46:13 &lt;ugha_node&gt; mihi: http://www.i2p.net/node/view/224 21:46:27  * duck ăn một ít sô-cô-la của fvw 21:47:16 &lt;mihi&gt; ugha_node: chắc chắn là không; xin lỗi 21:47:36 &lt;ugha_node&gt; mihi: Ờ, được. :( 21:48:33  * mihi đã từng cố 'chế' cái streaming api 'cũ' cách đây một thời gian, nhưng cái đó            lỗi quá nhiều... 21:48:53 &lt;mihi&gt; nhưng theo tôi thì sẽ dễ sửa cái đó hơn là sửa cái của tôi... 21:49:21 &lt;ugha_node&gt; Hê. 21:49:42 &lt;hypercubus&gt; khiêm tốn ghê 21:49:46 &lt;mihi&gt; vì nó đã có một chút (bị hỏng) hỗ trợ "reordering" (sắp xếp lại gói) trong đó 21:50:49 &lt;Sonium&gt; có cách nào hỏi deer có bao nhiêu người đang ở kênh i2p-#i2p không? 21:51:01 &lt;duck&gt; không 21:51:08 &lt;hypercubus&gt; không đâu, nhưng tôi có thể thêm cái đó vào bogobot 21:51:08 &lt;Sonium&gt; :/ 21:51:11 &lt;Nightblade&gt; !list 21:51:13 &lt;deer&gt; &lt;duck&gt; 10 ppl 21:51:13 &lt;hypercubus&gt; sau khi tôi hoàn thành trình cài đặt ;-) 21:51:24 &lt;Sonium&gt; !list 21:51:32 &lt;Sonium&gt; o_O 21:51:35 &lt;mihi&gt; Sonium ;) 21:51:38 &lt;ugha_node&gt; Đây không phải là kênh fserv! 21:51:39 &lt;Sonium&gt; đó là một cú lừa! 21:51:40 &lt;ugha_node&gt; :) 21:51:41 &lt;hypercubus&gt; phải là !who 21:51:44 &lt;deer&gt; &lt;duck&gt; ant duck identiguy Pseudonym ugha2p bogobot hirvox jrandom Sugadude                   unknown 21:51:48 &lt;cervantes&gt; ô, lỡ cuộc họp rồi 21:51:57 &lt;ugha_node&gt; !list 21:52:01 &lt;Nightblade&gt; !who 21:52:11 &lt;deer&gt; &lt;duck&gt; !who-your-mom 21:52:17 &lt;mihi&gt; !who !has !the !list ? 21:52:21 &lt;fvw&gt; !yesletsallspamthechannelwithinoperativecommands 21:52:33 &lt;Nightblade&gt; !ban fvw!*@* 21:52:42 &lt;mihi&gt; !ban *!*@* 21:52:50 &lt;hypercubus&gt; tôi cảm thấy sắp có cái búa gõ xuống 21:52:51 &lt;duck&gt; có vẻ là lúc thích hợp để đóng lại rồi 21:52:55 &lt;Sonium&gt; nhân tiện, bạn cũng nên triển khai lệnh !8 giống như chanserv có 21:52:59 &lt;fvw&gt; đúng, giờ chuyện đó xong rồi, hãy đóng.. vâng. thế đi. 21:53:00  * hypercubus có thần giao cách cảm 21:53:05 &lt;duck&gt; *BAFF* 21:53:11 &lt;Nightblade&gt; !baff 21:53:12 &lt;hypercubus&gt; tóc tôi, tóc tôi 21:53:24  * fvw chỉ vào hypercube và cười. Tóc cậu! Tóc cậu! </div>
