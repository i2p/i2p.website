---
title: "Cuộc họp các nhà phát triển I2P, ngày 5 tháng 8 năm 2003"
date: 2003-08-05
author: "nop"
description: "Cuộc họp các nhà phát triển I2P lần thứ 52 bao gồm tình hình phát triển Java, các cập nhật về mật mã, và tiến độ SDK"
categories: ["meeting"]
---

<h2 id="quick-recap">Tóm tắt nhanh</h2>

<p class="attendees-inline"><strong>Có mặt:</strong> hezekiah, jeremiah, jrand0m, mihi, nop, thecrypto</p>

<h2 id="meeting-log">Nhật ký cuộc họp</h2>

<div class="irc-log"> <nop>	ok, cuộc họp bắt đầu <nop>	chương trình nghị sự có gì -->	logger (logger@anon.iip) đã vào #iip-dev -->	Anon02 (~anon@anon.iip) đã vào #iip-dev <hezekiah>	Tue Aug  5 21:03:10 UTC 2003 <hezekiah>	Chào mừng đến với cuộc họp iip-dev thứ n. <hezekiah>	Chương trình nghị sự có gì? <thecrypto>	Tue Aug  5 21:02:44 UTC 2003 <thecrypto>	đã đồng bộ với một NTP stratum 2 :) <hezekiah>	Tue Aug  5 21:03:13 UTC 2003 -->	ptm (~ptm@anon.iip) đã vào #iip-dev <hezekiah>	Vừa đồng bộ với NIST. :) <mihi>	việc đồng bộ này không giúp gì cho độ trễ iip đâu ;) <jrand0m>	nop: những thứ tôi muốn đề cập: tình trạng phát triển java, tình trạng 	  crypto java, tình trạng phát triển python, tình trạng sdk, dịch vụ đặt tên <hezekiah>	(Chúng ta đã bàn đến dịch vụ đặt tên _ngay bây giờ_?) <jrand0m>	không phải thiết kế đâu đồ ngốc, đó là phần trình bày của co.  chỉ nói 	  nếu có gì để nói. <hezekiah>	À *	jrand0m cất cái LART đi <jrand0m>	còn gì nữa trong chương trình? <jrand0m>	hay chúng ta bắt đầu luôn? <hezekiah>	Ừ, tôi không nghĩ ra gì khác để thêm. <hezekiah>	À! <hezekiah>	Ồ! <jrand0m>	ok.  tình trạng phát triển java: <hezekiah>	Tốt. <--	mrflibble đã thoát (Ping timeout) <nop>	ok <nop>	chương trình <nop>	1) Chào mừng <jrand0m>	tính đến hôm nay, có một java client API cùng một java router 	  dạng stub có thể nói chuyện với nhau.  ngoài ra, có một ứng dụng tên là ATalk 	  cho phép IM (nhắn tin tức thời) ẩn danh + truyền tệp. <nop>	2) gián đoạn IIP 1.1 <nop>	3) I2P <nop>	4) Kết thúc với phần bình luận và linh tinh *	jrand0m quay lại góc <nop>	xin lỗi 	  joeyo jrand0m Aug 05 17:08:24 * hezekiah đưa cho jrand0m một chiếc mũ ngốc để 	  đội ở góc phòng. ;-) <nop>	xin lỗi về chuyện đó <nop>	không thấy là bạn đã bắt đầu ở đó <nop>	có lẽ tôi nên vào góc <hezekiah>	lol <jrand0m>	đừng lo.  mục 1) *	hezekiah đưa cho nop một chiếc mũ ngốc nữa. :) <nop>	ok chào mừng mọi người <nop>	bla bla <nop>	2) gián đoạn IIP 1.1 -->	mrflibble (mrflibble@anon.iip) đã vào #iip-dev <hezekiah>	Cuộc họp iip-dev lần thứ 52 và mấy thứ vớ vẩn hay ho! <nop>	máy chủ gần đây gặp một số vấn đề với các sector của ổ cứng và đã 	  được thay thế <nop>	tôi định chuyển cái máy chủ chết tiệt đó vào một môi trường ổn định hơn với 	  khả năng dự phòng <nop>	và có thể trao quyền điều khiển nhiều máy chủ ircd <nop>	không rõ <nop>	đó là chuyện cần bàn <--	Anon02 đã thoát (EOF From client) <nop>	hy vọng máy chủ của chúng ta sẽ ổn định từ giờ vì ổ cứng đã được thay <nop>	xin lỗi vì sự bất tiện mọi người nhé <nop>	3) I2P - Jrand0m, mời bạn <nop>	ra khỏi góc đi jrand0m *	hezekiah đi tới góc, kéo jrand0m khỏi ghế, lôi anh ấy 	  lên bục phát biểu, lấy lại chiếc mũ ngốc, và đưa cho anh ấy cái micro. *	nop vào góc đó để thế chỗ <hezekiah>	lol! <jrand0m>	xin lỗi, quay lại rồi *	nop giật chiếc mũ ngốc từ hezekiah *	nop đội nó lên đầu *	nop vỗ tay cho jrand0m *	jrand0m chỉ đứng xem <jrand0m>	ờ... um được <hezekiah>	jrand0m: i2p, tình trạng java, v.v. Nói đi! <jrand0m>	vậy thì, tính đến hôm nay, có một java client API cùng một java 	  router dạng stub có thể nói chuyện với nhau.  ngoài ra, có một ứng dụng tên 	  là ATalk cho phép IM (nhắn tin tức thời) ẩn danh + truyền tệp. <hezekiah>	Đã có truyền tệp rồi!? <jrand0m>	si sr <hezekiah>	Wow. <hezekiah>	Chắc tôi lạc hậu quá rồi. <jrand0m>	nhưng chưa được thanh nhã lắm <hezekiah>	lol <jrand0m>	nó lấy một tệp rồi nhét vào một thông điệp <hezekiah>	Ui. <nop>	truyền cục bộ 1.8 mb mất bao lâu? <jrand0m>	Tôi đã thử với một tệp 4K và một tệp 1.8Mb <jrand0m>	vài giây <nop>	tuyệt <nop>	:) <hezekiah>	Mấy thứ java đã mã hóa thật chưa, hay vẫn giả 	  vậy? <nop>	giả <nop>	đến tôi còn biết điều đó <nop>	:) <jrand0m>	Tôi làm nóng bằng cách tự nói chuyện với mình trước [ví dụ: từ một cửa sổ 	  sang cửa sổ khác, chào hỏi] nên nó không phải xử lý overhead của lần elg đầu tiên <jrand0m>	đúng, phần lớn là giả <thecrypto>	phần lớn việc mã hóa là giả <thecrypto>	nhưng đang được làm <hezekiah>	Tất nhiên. :) <jrand0m>	chắc chắn rồi. <jrand0m>	về khoản đó, thecrypto cho bọn tôi cập nhật nhé? <thecrypto>	ờ, hiện giờ tôi đã xong ElGamal và SHA256 <thecrypto>	giờ tôi đang tạo các số nguyên tố cho DSA <thecrypto>	Tôi sẽ gửi ra 5 cái rồi ta chọn một <hezekiah>	nop: Anh không phải cũng có mấy số nguyên tố để dùng với DSA à? <thecrypto>	Chúng tôi cũng có vài benchmark cho ElGamal và SHA256 <thecrypto>	Và tất cả đều nhanh <jrand0m>	benchmark mới nhất với elg: <jrand0m>	Thời gian tạo khóa trung bình: 4437	tổng: 443759	min: 	  872	   max: 21110	   Tạo khóa/giây: 0 <jrand0m>	Thời gian mã hóa trung bình    : 356	tổng: 35657	min: 	  431	   max: 611	   Bps mã hóa: 179 <jrand0m>	Thời gian giải mã trung bình    : 983	tổng: 98347	min: 	  881	   max: 2143	   Bps giải mã: 65

<hezekiah>	min và max: tính theo giây à? <jrand0m>	lưu ý là Bps không thật sự hữu ích, vì chúng ta chỉ mã hóa/giải mã 	64 bytes <thecrypto>	ms <jrand0m>	không, xin lỗi, tất cả đều là mili giây <hezekiah>	Tuyệt. :) <hezekiah>	Và cái này làm bằng java à? <thecrypto>	đúng <thecrypto>	java thuần <hezekiah>	OK. Tôi chính thức ấn tượng. :) <jrand0m>	100%.  P4 1.8 <thecrypto>	trên máy 800 MHz của tôi thì cũng xấp xỉ như vậy <hezekiah>	Làm sao tôi có thể chạy cùng các bài test đó? <jrand0m>	benchmark SHA256: <jrand0m>	Thời gian trung bình thông điệp ngắn  : 0 tổng: 0	min: 0	max: 0  Bps: NaN <jrand0m>	Thời gian trung bình thông điệp vừa   : 1 tổng: 130	min: 0	max: 10 Bps: 7876923 <jrand0m>	Thời gian trung bình thông điệp dài    : 146	tổng: 14641	min: 130	max: 270	Bps: 83037 <thecrypto>	chạy chương trình ElGamalBench <hezekiah>	OK. <hezekiah>	Tôi sẽ đi tìm nó. <jrand0m>	(kích thước ngắn: ~10 bytes, vừa ~10KB, dài ~1MB) <jrand0m>	java -cp i2p.jar ElGamalBench <jrand0m>	(sau khi chạy "ant all") <hezekiah>	jrand0m: Cảm ơn. :) <jrand0m>	không vấn đề <thecrypto>	Cái NaN nghĩa là nó nhanh đến mức ta rốt cuộc chia cho 0 — nhanh thế đấy :) <hezekiah>	Bài benchmark sha là gì? <jrand0m>	java -cp i2p.jar SHA256Bench -->	Neo (anon@anon.iip) đã tham gia #iip-dev <hezekiah>	OK. <jrand0m>	chắc chúng ta sẽ muốn chuyển những thứ đó thành phương thức main() của các engine liên quan, nhưng hiện tại để ở đó cũng ổn <hezekiah>	Hãy xem tất cả cái này nhanh thế nào trên một AMD K6-2 333MHz (một con chip không nổi tiếng về tính toán số nguyên.) <jrand0m>	hehe <jrand0m>	ok vậy còn lại DSA và AES, đúng không? <jrand0m>	tất cả đều quá đỉnh, thecrypto. Làm tốt lắm. <thecrypto>	ừ <jrand0m>	tôi có thể hối bạn về ETA (thời gian dự kiến) cho hai cái còn lại không?  ;) <hezekiah>	Nếu cái này nhanh gần bằng trên máy của tôi như trên máy của bạn, bạn phải chỉ tôi cách bạn làm đấy. ;-) <thecrypto>	DSA sẽ xong gần như ngay khi tôi có các số nguyên tố sẵn sàng <nop>	hezekiah bạn đã thử sslcrypto cho python chưa <thecrypto>	copy một ít mã từ bộ sinh số nguyên tố và vài thứ tương tự là xong <nop>	cái ở link đó <hezekiah>	nop: sslcrypto sẽ không giúp ích gì cho bọn mình. <hezekiah>	nop: Nó không triển khai ElGamal _hoặc_ AES _hoặc_ sha256. <thecrypto>	AES hầu như xong rồi, chỉ là đâu đó còn lỗi mà tôi vẫn đang cố tìm ra và xử lý, khi xong phần đó thì sẽ hoàn tất <jrand0m>	thecrypto> vậy đến thứ Sáu, DSA tạo khóa (keygen), ký, xác minh, và AES mã hóa, giải mã cho đầu vào kích thước bất kỳ? <nop>	cái trên trang của McNab thì không à? <thecrypto>	đúng vậy <nop>	chán ghê <thecrypto>	chắc là thứ Sáu <thecrypto>	nhiều khả năng là thứ Năm <jrand0m>	thecrypto> cái đó có bao gồm mấy thứ UnsignedBigInteger không? <thecrypto>	tuần sau tôi sẽ nghỉ buổi họp vì đi trại hè, sau đó sẽ quay lại <thecrypto>	jrand0m: chắc là không <jrand0m>	ok. <jrand0m>	vậy tạm thời, khả năng tương tác giữa java và python bị b0rked (hỏng bét). <jrand0m>	ý là về phần crypto. ---	Thông báo: jeremiah đang online (anon.iip). -->	jeremiah (~chatzilla@anon.iip) đã tham gia #iip-dev <jrand0m>	(tức là cho chữ ký, khóa, mã hóa và giải mã)

<nop>	hmm có lẽ chúng ta nên tập trung nhiều hơn vào C/C++ <thecrypto>	ừ, một khi chúng ta làm nó chạy hoàn chỉnh thì có thể đảm bảo 	  cả java và python giao tiếp được với nhau
<jrand0m>	khi bạn vắng mặt tôi sẽ xem phần kiểu không dấu (unsigned).
<jeremiah>	có ai có thể email cho tôi log (backlog) không? jeremiah@kingprimate.com
<hezekiah>	jeremiah: Cho tôi một phút. :)
<jrand0m>	nop> chúng ta có dev C/C++ không?
<nop>	Tôi có một người, đúng vậy
<nop>	và Hezekiah chúng ta biết là có thể làm được
<jrand0m>	hoặc có lẽ chúng ta có thể nhận cập nhật trạng thái dev python từ hezekiah + 	  jeremiah để xem khi nào chúng ta sẽ có thêm người cho dev c/c++
<jrand0m>	đúng, tất nhiên.  nhưng hez+jeremiah đang làm python lúc này 	  (đúng không?)
<hezekiah>	Ừ.
<--	mrflibble đã thoát (Ping timeout)
<hezekiah>	Kiểu như tôi đang gây khá nhiều rắc rối cho tội nghiệp jeremiah.
<nop>	Tôi chỉ nói là nếu python sẽ không cho tốc độ cao
<hezekiah>	Python chủ yếu là để tôi hiểu mạng này.
<nop>	àh
<hezekiah>	Khi tôi làm cho nó cơ bản tuân theo đầy đủ spec, tôi dự định 	  chuyển cho jeremiah để anh ấy làm theo ý thấy hợp lý.
<hezekiah>	Nó không nhằm trở thành một bản triển khai ‘đỉnh’ của spec.
<hezekiah>	(Nếu tôi muốn thế, tôi sẽ dùng C++.)
<jeremiah>	ừ thì không có phần nào của ứng dụng thực sự ngốn CPU, 	  (nếu mình nhớ đúng - iirc) ngoài phần mật mã, và lý tưởng là phần đó sẽ được xử lý bằng C dù sao đi nữa, đúng không?
<jrand0m>	chắc rồi jeremiah. tất cả còn tùy vào ứng dụng
-->	mrflibble (mrflibble@anon.iip) đã tham gia #iip-dev
<hezekiah>	jeremiah: Về lý thuyết.
<jrand0m>	vậy chúng ta đang ở đâu bên phía python?  client api, router chỉ cục bộ 	  , v.v.?
<jeremiah>	bản triển khai bằng python cũng sẽ cho chúng ta biết những tối ưu hóa 	  có thể làm ngay từ đầu... Tôi muốn giữ nó cập nhật hoặc, nếu có thể, 	  đi trước bản triển khai bằng C trong khả năng của tôi
<hezekiah>	jrand0m: OK. Đây là những gì tôi có.
<hezekiah>	Về _lý thuyết_ thì router phải có thể xử lý mọi thông điệp không quản trị 	  đến từ một client.
<hezekiah>	Tuy nhiên, tôi chưa có client, nên tôi chưa thể debug 	  nó (tức là vẫn còn bug).
<hezekiah>	Tôi đang làm phần client ngay bây giờ.
<jrand0m>	'k.  nếu bạn có thể tắt việc kiểm tra chữ ký, chúng ta có thể 	  chạy client java với nó ngay bây giờ
<hezekiah>	Tôi hy vọng sẽ xong phần đó, trừ các thông điệp quản trị, trong một hoặc 	  hai ngày.
<jrand0m>	chúng ta có thể thử cái đó sau buổi họp
<hezekiah>	jrand0m: OK.
<jeremiah>	Kể từ buổi họp trước tôi chủ yếu bận việc đời thực, 	  tôi có thể làm phần client API, chỉ là đang cố đồng bộ cách nghĩ của tôi 	  với của hezekiah
<jrand0m>	tuyệt
<hezekiah>	jeremiah: Bạn biết không, cứ đợi đã.
<hezekiah>	jeremiah: Có lẽ tôi đang nhồi quá nhiều thứ mới để bạn 	  xử lý ngay lúc này.
<jeremiah>	hezekiah: đúng, điều tôi định nói là bạn có lẽ nên 	  cứ tiếp tục triển khai các phần cơ bản trước
<hezekiah>	jeremiah: Chẳng bao lâu nữa nó sẽ ổn định và bạn có thể 	  bắt đầu tinh chỉnh. (Có rất nhiều comment TODO cần được xử lý.)
<jeremiah>	và rồi tôi có thể mở rộng nó sau khi tôi nắm được bức tranh tổng thể
<hezekiah>	Chính xác.
<hezekiah>	Bạn sẽ phải bảo trì toàn bộ đống mã này. :)
<jrand0m>	tuyệt.  vậy eta 1-2 tuần cho một router python hoạt động + client api?
<hezekiah>	Tuần sau tôi đi nghỉ nên có lẽ vậy.
<hezekiah>	Chúng ta sắp có thêm chi tiết về router-to-router chứ?
<jrand0m>	không.
<jrand0m>	ừ, có.
<jrand0m>	nhưng mà không.
<hezekiah>	lol
<jeremiah>	hezekiah: kỳ nghỉ dài bao lâu?
<hezekiah>	1 tuần.
<jeremiah>	ok
<jrand0m>	(aka tức là ngay khi SDK phát hành, 100% thời gian của tôi sẽ dồn vào I2NP)
<hezekiah>	Tôi hy vọng viết xong toàn bộ chức năng không liên quan admin trước khi 	  tôi đi nghỉ
<hezekiah>	.
<jrand0m>	nhưng rồi không lâu sau khi bạn quay lại là bạn vào đại học, đúng không?
<hezekiah>	I2NP?
<hezekiah>	Đúng.
<jrand0m>	giao thức mạng
<hezekiah>	Tôi có khoảng 1 tuần sau kỳ nghỉ.
<hezekiah>	Sau đó tôi đi.
<hezekiah>	Và thời gian rảnh của tôi giảm mạnh.
<jrand0m>	vậy tuần đó chỉ nên để gỡ lỗi (debug)
<jeremiah>	Tôi có thể làm tiếp code trong khi hez vắng mặt
<jrand0m>	ok
<jrand0m>	mùa hè của bạn thế nào, jeremiah?
<hezekiah>	jeremiah: Có lẽ bạn có thể làm cho các hàm admin đó chạy được?

<thecrypto>	tôi vẫn sẽ còn một tháng sau khi tôi trở về từ kỳ nghỉ để làm 	  vài thứ
<jrand0m>	có cuộc sống, hay giống phần còn lại của bọn tôi là l00sers?  :)
<jeremiah>	có thể
<hezekiah>	100sers?
<hezekiah>	100ser là gì?
<jeremiah>	tôi đi học đại học vào ngày 22, ngoài ra thì tôi có thể dev
<mihi>	hezekiah: một kẻ thua cuộc
<jeremiah>	và tuần cuối trước khi tôi đi thì tất cả bạn bè tôi sẽ vắng... nên 	  tôi có thể vào chế độ hyperdev
<hezekiah>	mihi: À!
<jrand0m>	hehe
<hezekiah>	OK. Vậy chúng ta đang ở đâu trong chương trình nghị sự?
<hezekiah>	tức là, tiếp theo là gì?
<jrand0m>	tình trạng SDK
<jrand0m>	SDK == một triển khai client, một triển khai router chỉ cục bộ, một app, và tài liệu.
<jrand0m>	Tôi muốn phát hành cái đó trước thứ Ba tới.
<hezekiah>	jeremiah: Phần backlog đang trên đường. Xin lỗi tôi quên bạn lúc nãy. :)
<jeremiah>	cảm ơn
<jrand0m>	ok, co không có mặt, nên mấy thứ về dịch vụ đặt tên chắc hơi 	  lạc đề
<jrand0m>	chúng ta có thể bàn về dịch vụ đặt tên sau khi anh ấy đưa ra đặc tả hoặc 	  khi anh ấy có mặt
<jrand0m>	ok, vậy là hết phần I2P
<jrand0m>	ai còn gì về I2P nữa không, hay chúng ta chuyển sang:
<nop> 4) Kết thúc với 	  bình luận và mấy thứ
<hezekiah>	Tôi không nghĩ ra gì.
<jrand0m>	Tôi đoán mọi người đều đã thấy 	  http://www.cnn.com/2003/TECH/internet/08/05/anarchist.prison.ap/index.html ?
<thecrypto>	chưa ở đây
<jrand0m>	(nop đã đăng nó ở đây trước đó)
<hezekiah>	Chuyện về anh chàng bị bắt vì liên kết đến một trang xây 	  bom hả?
<jrand0m>	đúng
<jrand0m>	tính liên quan đến nhu cầu triển khai I2P càng sớm càng tốt chắc là hiển nhiên ;)
<hezekiah>	OK! jeremiah, các log đó đã được gửi.
<jeremiah>	cảm ơn
<jrand0m>	ai có câu hỏi / bình luận / ý nghĩ / frisbee nào không, 	  hay là chúng ta đang có một cuộc họp ngắn kỷ lục?
*	thecrypto ném một cái frisbee
<--	logger đã thoát (Ping timeout)
<jrand0m>	chà, mọi người im ắng quá hôm nay ;)
<mihi>	câu hỏi:
<mihi>	người không dev có thể lấy mã Java của bạn ở đâu?
<jrand0m>	dạ thưa?
<thecrypto>	chưa
<mihi>	404
<jrand0m>	chúng tôi sẽ công bố khi sẵn sàng phát hành.  tức là mã 	  nguồn sẽ đi kèm với SDK
<jrand0m>	heh
<jrand0m>	ừ, bọn tôi không dùng SF
<hezekiah>	nop: Liệu chúng ta có thể chạy được anonymous cvs vào một lúc nào đó không?
<hezekiah>	time?
<--	mrflibble đã thoát (Ping timeout)
<nop>	ừ, tôi sẽ mở một cổng không chuẩn
<jrand0m>	hezekiah> chúng ta sẽ có cái đó khi mã có giấy phép GPL trên đó
<nop>	nhưng tôi đang làm viewcvs
<jrand0m>	tức là không phải bây giờ vì tài liệu GPL vẫn chưa được thêm vào mã
<hezekiah>	jrand0m: Nó nằm trong tất cả các thư mục mã python và tất cả các 	  tệp nguồn python chỉ rõ giấy phép theo GPL-2.
<jrand0m>	hezekiah> cái đó ở trên cathedral à?
<hezekiah>	Đúng.
<jrand0m>	à chuẩn.  i2p/core/code/python ?  hay một module khác?
*	jrand0m chưa thấy nó ở đó
<hezekiah>	Mỗi thư mục mã python có một tệp COPYING trong đó với 	  GPL-2 và mỗi tệp nguồn có giấy phép đặt là GPL-2
<hezekiah>	Đó là i2p/router/python và i2p/api/python
<jrand0m>	'k
<jrand0m>	vậy, ừ, trước thứ Ba tới chúng ta sẽ có SDK + truy cập mã nguồn công khai.
<hezekiah>	Tuyệt.
<hezekiah>	Hoặc như anh thích nói, wikked. ;-)
<jrand0m>	heh
<jrand0m>	không còn gì nữa à?
<hezekiah>	nada mas? Nghĩa là gì vậy!?
<jeremiah>	không còn gì nữa
*	jrand0m đề nghị bạn học chút tiếng Tây Ban Nha ở đại học
-->	mrflibble (mrflibble@anon.iip) đã tham gia #iip-dev
<hezekiah>	Ai có câu hỏi không?
<hezekiah>	Lần một!
<--	ptm (~ptm@anon.iip) đã rời #iip-dev (ptm)
<hezekiah>	Lần hai!
<--	mrflibble đã thoát (mr. flibble says "game over boys")
<hezekiah>	Nói ngay .. hoặc đợi đến khi bạn thấy muốn nói sau!
<thecrypto>	được rồi, tôi sẽ tối ưu ElGamal hơn nữa, nên hãy 	  mong đợi benchmark ElGamal còn nhanh hơn trong tương lai
<jrand0m>	làm ơn tập trung vào DSA và AES trước khi tinh chỉnh... làmmmm ơnnnnn :)
<thecrypto>	tôi sẽ làm
<hezekiah>	Lý do anh ấy làm vậy là bởi vì tôi lại gây rắc rối cho 	  mọi người. ;-)
<thecrypto>	tôi đang tạo các số nguyên tố DSA
-->	mrflibble (mrflibble@anon.iip) đã tham gia #iip-dev
<thecrypto>	ừ, ít nhất là đang viết chương trình để tạo số nguyên tố DSA ngay bây giờ
<hezekiah>	ElGamal trong Java không thích AMD K-6 II 333MHz.
<hezekiah>	OK.
<hezekiah>	Phần hỏi đáp kết thúc!
<jrand0m>	ok hez, xong rồi.  cậu muốn bàn riêng về việc làm cho client Java 	  và router Python hoạt động không?
<hezekiah>	Hẹn gặp mọi người tuần sau, các công dân!
*	hezekiah đập cái *baf*er xuống </div>
