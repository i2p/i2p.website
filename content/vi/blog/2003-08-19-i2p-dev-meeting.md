---
title: "Cuộc họp nhà phát triển I2P, ngày 19 tháng 8 năm 2003"
date: 2003-08-19
author: "jrand0m"
description: "Cuộc họp nhà phát triển I2P lần thứ 54 bao gồm các cập nhật SDK, đánh giá I2NP, tiến triển về mật mã học, và tình hình phát triển"
categories: ["meeting"]
---

<h2 id="quick-recap">Tóm tắt nhanh</h2>

<p class="attendees-inline"><strong>Có mặt:</strong> cohesion, hezekiah, jrand0m, mihi, nop, thecrypto</p>

<h2 id="meeting-log">Nhật ký cuộc họp</h2>

<div class="irc-log"> --- Log opened Tue Aug 19 16:56:12 2003 17:00 -!- logger [logger@anon.iip] has joined #iip-dev 17:00 -!- Topic for #iip-dev: Các cuộc họp phát triển IIP hàng tuần, và các 	 cuộc trò chuyện khác giữa các nhà phát triển được tổ chức ở đây. 17:00 [Users #iip-dev] 17:00 [ cohesion] [ leenookx  ] [ mihi] [ shardy_  ] [ UserXClone] 17:00 [ Ehud    ] [ logger    ] [ nop ] [ thecrypto] [ velour    ] 17:00 [ hezekiah] [ lonelynerd] [ Rain] [ UserX    ] [ WinBear   ] 17:00 -!- Irssi: Tổng cộng 15 nick trong #iip-dev [0 ops, 0 halfops, 0 voices, 15 bình thường] 17:00 -!- Irssi: Tham gia #iip-dev đã được đồng bộ trong 7 giây 17:00 < hezekiah> Được rồi! :) 17:00 < hezekiah> Cả hai logger đều đã sẵn sàng. :) 17:01 < thecrypto> yeah! 17:03 < hezekiah> Hmmm ... 17:03 < hezekiah> Cuộc họp này lẽ ra bắt đầu 3 phút trước rồi. 17:03 < hezekiah> Không biết có chuyện gì. 17:04 < thecrypto> ừ, ai đang idle 17:04 < hezekiah> jrand0m thậm chí còn chưa online. 17:04 < hezekiah> nop đã idle 15 phút. 17:05 < nop> chào 17:05 < nop> xin lỗi 17:05 < nop> Mình bận ngập đầu ở chỗ làm 17:05 < mihi> [22:36] * jrand0m đi ăn tối nhưng sẽ quay lại trong 	 nửa tiếng nữa cho cuộc họp 17:05 -!- jrand0m [~jrandom@anon.iip] has joined #iip-dev 17:05 < hezekiah> Chào, jrand0m. 17:05 < nop> chào 17:05 < nop> ok, thế này nhé 17:05 < nop> Bây giờ mình không thể để lộ là đang ở trên IIP ở chỗ làm 17:05 < nop> nên mình sẽ liên lạc với mọi người sau 17:05 < nop> hôm qua bị nhắc nhở vụ này rồi 17:05 < nop> vậy nhé 17:05 < hezekiah> Tạm biệt, nop. 17:05 < thecrypto> bye 17:06 < nop> Mình sẽ treo trong kênh 17:06 < nop> chỉ là sẽ không lộ liễu :) 17:06 < hezekiah> jrand0m? Vì dạo này bạn nói nhiều nhất, có gì bạn muốn 	 đưa vào chương trình nghị sự cho cuộc họp này không? 17:07 < jrand0m> quay lại rồi 17:08 < jrand0m> ok, mì pesto ngon phết. 17:08 < jrand0m> để mình lôi mấy thứ kiểu chương trình nghị sự lên 17:09 -!- Lookaround [~chatzilla@anon.iip] has joined #iip-dev 17:09 < jrand0m> x.1) i2cp sdk mods x.2) i2np review x.3) polling http 	 transport x.4) dev status x.5) todo x.6) plan for next two weeks 17:09 < jrand0m> (đặt x vào số nào trong chương trình nghị sự thấy hợp) 17:10 < thecrypto> bạn là chương trình nghị sự đấy 17:10 < hezekiah> jrand0m: Mình không có gì để nói, và nop thì 17:10 < hezekiah> không thể nói được. 17:10 < jrand0m> lol 17:10 < hezekiah> UserX nhiều khả năng sẽ không thêm gì (thường thì không), 	 nên theo mình thì mọi thứ là của bạn cả. :0 17:10 < hezekiah> :) 17:10 < jrand0m> 'k.  mình có log không? 17:10 < jrand0m> heh 17:10 < hezekiah> Mình đang log mọi thứ. 17:10 < jrand0m> tuyệt.  ok.  0.1) chào mừng. 17:10 < jrand0m> chào. 17:11 < jrand0m> 0.2) mailing list 17:11 < jrand0m> list hiện giờ đang down, sẽ lên lại sớm nhất.  khi nào hoạt động lại các bạn sẽ biết :) 17:11 < jrand0m> trong lúc chờ, dùng wiki hoặc dùng IIP để trò chuyện. 17:11 < jrand0m> 1.1) i2cp sdk mods 17:12 < jrand0m> SDK đã được cập nhật với vài bản sửa lỗi, cộng thêm một số 	 thứ mới trong spec đã được giới thiệu. 17:12 < jrand0m> Mình đã gửi lên list hôm qua với thông tin. 17:13 < jrand0m> hezekiah/thecrypto/jeremiah> có câu hỏi gì về những gì mình 	 đã gửi, hoặc ý tưởng về kế hoạch triển khai các thay đổi không?  (hoặc 	 phương án khác mình chưa nghĩ tới?) 17:13 < hezekiah> Mình bận tối mắt tối mũi chuẩn bị vào đại học. 17:13 < jrand0m> ừ, hiểu rồi. 17:13 < hezekiah> Mình có xem qua những gì bạn viết, nhưng chưa thực sự 	 xem các thay đổi trong spec. 17:13 < jrand0m> Chúng ta chẳng còn mấy thời gian của bạn nữa, phải không... 17:13 < hezekiah> Chưa đâu, cho đến khi mình tới trường. 17:14 < hezekiah> Khi tới nơi, có lẽ mình sẽ mất tích ít nhất một tuần để 	 thích nghi. 17:14 < jrand0m> và khi bạn tới đó bạn sẽ phải thu xếp nhiều thứ 	 (nếu mình nhớ đúng từ hồi mình đi học ;) 17:14 < jrand0m> heh đúng vậy. 17:14 < hezekiah> Sau đó mình sẽ vào guồng hơn và có thêm thời gian để 	 code. 17:14 < jrand0m> tuyệt 17:14 < thecrypto> mình chỉ làm crypto, nên mối lo chính là cấu trúc dữ liệu, 	 khi mình làm xong chế độ CTS, mình sẽ quay lại làm cái đó chắc vậy 17:14 < hezekiah> Dù sao thì đó là dự đoán của mình. 17:14 < jrand0m> ngon đấy thecrypto 17:15 < jrand0m> ok, điểm tốt là SDK chạy hoàn hảo (các lỗi mihi tìm 	 đã được sửa [yay mihi!]) mà không cần cập nhật spec. 17:15 -!- arsenic [~none@anon.iip] has joined #iip-dev 17:16 < jrand0m> ok, sang 1.2) i2np review 17:16 < jrand0m> có ai đọc tài liệu chưa? 17:16 < jrand0m> ;) 17:16 < hezekiah> Chưa, mình thì chưa. 17:16 < hezekiah> Như đã nói, hiện mình đang bận tối mắt tối mũi. 17:17 < hezekiah> Nhân tiện, jrand0m, có vẻ bạn thích gửi PDF. 17:17 < jrand0m> mọi người đọc được OpenOffice .swx không? 17:17 < hezekiah> Mình đọc được. 17:17 < jrand0m> [nếu vậy, mình sẽ gửi swx] 17:17 -!- abesimpson [~k@anon.iip] has joined #iip-dev 17:17 < thecrypto> mình đọc được 17:17 < hezekiah> Mình không thể tìm kiếm văn bản trong PDF bằng KGhostView. 17:17 < hezekiah> Thế thì bất tiện thật. 17:17 < jrand0m> xui thật, hezekiah 17:17 -!- mrflibble [mrflibble@anon.iip] has joined #iip-dev 17:17 < hezekiah> Bản Linux của Adobe Acrobat cũng không thân thiện lắm. 17:18 < jrand0m> ok, vậy dùng định dạng OpenOffice thay vì PDF. 17:18 < hezekiah> Tuyệt. 17:18 < jrand0m> ừm, ok.  i2np có vài thay đổi nhỏ với cấu trúc LeaseSet 	 (phản ánh thay đổi i2cp đã gửi trước đó), còn lại thì phần lớn đã ổn. 17:19 < hezekiah> jrand0m: Tất cả các tài liệu này có trong CVS của cathedral không? 17:19 < nop> ô 17:19 < nop> mình xen ngang được không 17:19 < hezekiah> tức là bản sao các tệp PDF bạn đã gửi lên list, v.v. 17:19 < hezekiah> nop: Cứ tự nhiên. 17:19 < nop> cái này lạc đề nhưng quan trọng 17:19 -!- ChZEROHag [hag@anon.iip] has joined #iip-dev 17:19 < nop> IIP-dev và mail đang hơi trục trặc 17:19 < hezekiah> Mình để ý rồi. 17:19 < nop> nên mong mọi người chịu khó chờ chút 17:20 < nop> bọn mình đang cố gắng dựng lên và chạy 17:20 < nop> nhưng có tích hợp SpamAssassin 17:20 < nop> đó là tin tốt 17:20 < nop> :) 17:20 < nop> và nhiều tính năng khác 17:20 < jrand0m> có ETA nào cho list không, nop? 17:20  * ChZEROHag thò mũi vào 17:20 < jrand0m> (mình biết bạn bận, không hối, chỉ hỏi thôi) 17:20 < nop> hy vọng là trước ngày mai 17:20 < jrand0m> tuyệt 17:20 < nop> quản trị mail đang làm 17:21  * hezekiah ghi chú rằng jrand0m _rất_ thích list iip-dev. ;-) 17:21 < nop> haha 17:21 < hezekiah> Cố lên delta407! 17:21 < nop> dù sao 17:21 < jrand0m> tốt nhất là ghi lại các quyết định công khai, hezekiah ;) 17:21 < nop> trở lại cuộc họp theo lịch thường lệ 17:21 < jrand0m> heh 17:21 -!- nop is now known as nop_afk 17:21 < hezekiah> jrand0m: Vậy ta đang ở đâu rồi? 17:21 < jrand0m> ok, trả lời câu hỏi của bạn hezekiah> một số có, nhưng bản 	 mới nhất thì chưa.  Mình sẽ chuyển sang đặt ở định dạng OpenOffice. 17:21 < jrand0m> thay vì PDF 17:22 < hezekiah> OK. 17:22 < hezekiah> Sẽ rất tuyệt nếu tất cả tài liệu đều ở CVS. 17:22 < jrand0m> chắc chắn, và sẽ như vậy 17:22 < hezekiah> Vậy mình chỉ cần update, và biết là có bản mới nhất. 17:22 < jrand0m> (hiện còn ba bản nháp là chưa) 17:22 < hezekiah> (Nhân tiện, hơi lạc đề, nhưng truy cập ẩn danh vào 	 cathedral đã mở chưa?) 17:23 < jrand0m> chưa. 17:23 < jrand0m> ok, đến thứ Sáu, mình hy vọng sẽ có một bản nháp khác của 	 I2NP ở dạng đầy đủ [tức là không còn ... cho các phần giải thích Kademlia, 	 và chi tiết triển khai mẫu] 17:24 < jrand0m> không có thay đổi đáng kể.  chỉ bổ sung làm rõ thêm. 17:24 < hezekiah> Tuyệt. 17:24 < hezekiah> Trong đó sẽ có bố cục byte cho các cấu trúc dữ liệu chứ? 17:24 < jrand0m> 1.3) I2P Polling HTTP Transport spec. 17:24 < jrand0m> không, bố cục byte sẽ nằm trong đặc tả cấu trúc dữ liệu, 	 cái này nên được chuyển sang định dạng chuẩn thay vì HTML 17:25 < jrand0m> (dù I2NP đã có mọi bố cục byte cần thiết) 17:25 < jrand0m> ((nếu bạn đọc nó *khụ* ;) 17:25 < hezekiah> Tốt. 17:25 < hezekiah> lol 17:25 < hezekiah> Xin lỗi về chuyện đó. 17:25 < hezekiah> Như đã nói, mình bận thực sự. 17:25 < jrand0m> heh không sao, bạn sắp vào đại học rồi, lẽ ra bạn 	 nên đi party :) 17:25 < hezekiah> Party á? 17:25 < jrand0m> ok, 1.3) I2NP Polling HTTP Transport spec 17:25 < hezekiah> Hmmm ... chắc mình hơi khác người. 17:25 < jrand0m> heh 17:26 < jrand0m> ok, mình đã cố gửi cái này sớm hơn, nhưng sẽ commit 	 sớm thôi.  đó là một giao thức transport nhanh gọn phù hợp với I2NP để 	 cho phép router gửi dữ liệu qua lại mà không cần kết nối trực tiếp 	 (vd tường lửa, proxy, v.v.) 17:27 < jrand0m> Mình đang hy vọng ai đó có thể xem cách này hoạt động và 	 xây dựng các transport tương tự (vd TCP hai chiều, UDP, HTTP trực tiếp, v.v.) 17:27 -!- mihi [none@anon.iip] has quit [Ping timeout] 17:27 < hezekiah> Hmmm, well I don 17:27 < jrand0m> trước khi đưa I2NP ra review, chúng ta cần kèm các 	 transport mẫu để mọi người thấy bức tranh đầy đủ 17:27 < hezekiah> không nghĩ là _mình_ sẽ xây bất kỳ transport nào sớm đâu. ;-) 17:27 -!- WinBear_ [~WinBear@anon.iip] has joined #iip-dev 17:27 < hezekiah> TCP đang chạy cho Java và Python. 17:27 < hezekiah> (Ít nhất là client-to-router.) 17:27 < jrand0m> không sao, mình chỉ đưa ra như một việc cần làm cho 	 những ai muốn đóng góp 17:28 < hezekiah> Phải. 17:28 < jrand0m> đúng, client-router có yêu cầu khác với router-router. 17:28 < jrand0m> ok, dù sao, 1.4) tình trạng dev 17:28 < jrand0m> CBC thế nào rồi, thecrypto? 17:28 < thecrypto> CBC đã commit 17:28 < jrand0m> w00000t 17:28 < thecrypto> CTS gần xong 17:28 < hezekiah> thecrypto: CTS là gì? 17:29 < thecrypto> mình chỉ còn phải nghĩ cách implement nó cho đẹp 17:29 < jrand0m> cts là Ciphertext Stealing :) 17:29 < hezekiah> À! 17:29 < thecrypto> CipherText Stealing 17:29 -!- WinBear [WinBear@anon.iip] has quit [EOF From client] 17:29 < jrand0m> bạn đã lấy tài liệu tham khảo của nop về vụ đó chưa? 17:29 < hezekiah> OK. Chúng ta dùng CBC với CTS thay vì padding. 17:29 < hezekiah> Hmm. 17:29 < thecrypto> cơ bản là nó làm cho thông điệp có độ dài chính xác 17:29 < jrand0m> như vậy có làm được bên phía Python không, hezekiah? 17:29 < hezekiah> Có lẽ mình phải nện cái thư viện crypto Python mình đang 	 dùng một phát để bắt nó dùng CTS cho đúng. 17:30 < hezekiah> Mình luôn thích CTS hơn padding, nhưng không biết 	 PyCrypt làm gì. 17:30 < jrand0m> Python có thể làm gì out-of-the-box để cho phép khôi phục 	 kích thước thông điệp chính xác? 17:30 < thecrypto> bạn chỉ cần đổi cách xử lý hai khối cuối cùng 17:30 < hezekiah> Mình có linh cảm thư viện đó sẽ phải viết lại kha khá. 17:30 < hezekiah> jrand0m: Phần CBC trong Python là trong suốt. Bạn chỉ 	 cần gửi buffer vào hàm encrypt của đối tượng AES. 17:31 < hezekiah> Nó nhả ra ciphertext.

17:31 < hezekiah> Hết chuyện.
17:31 < jrand0m> D(E(data,key),key) có bằng data, từng byte một, chính xác cùng kích thước không?
17:31 < hezekiah> Vậy nếu nó có ý tưởng kỳ quặc là dùng đệm (padding) thay vì CTS (Ciphertext Stealing), thì có lẽ tôi phải mổ xẻ bên trong nó và sửa.
17:31 < jrand0m> (bất kể kích thước đầu vào?)
17:31 -!- mihi [~none@anon.iip] đã vào #iip-dev
17:31 < hezekiah> jrand0m: Đúng. Lẽ ra phải vậy.
17:31 < jrand0m> hezekiah> nếu anh có thể xem chính xác nó dùng thuật toán nào để làm padding, thì tốt quá
17:32 < hezekiah> Được.
17:32  * jrand0m lưỡng lự khi yêu cầu sửa (mod) một thư viện mã hóa Python nếu thư viện đã dùng một cơ chế tiêu chuẩn và hữu ích
17:32 < hezekiah> Dù thế nào thì CBC với CTS (Ciphertext Stealing) nghe ổn.
17:32 < hezekiah> jrand0m: Thư viện mã hóa Python này tệ quá.
17:32 < jrand0m> heh ok
17:33 < thecrypto> tôi chỉ cần tính cách nghịch hai khối đó thế nào
17:33 < hezekiah> jrand0m: ElGamal sẽ cần được viết lại hoàn toàn bằng C chỉ để đủ nhanh mà dùng.
17:33 < jrand0m> hezekiah> benchmark cho elg Python 256 bytes là bao nhiêu? nó chỉ thực hiện một lần cho mỗi phiên giao tiếp dest-dest...
17:34 < jrand0m> (ý là nếu anh nhớ sẵn)
17:34 < hezekiah> Tôi phải thử đã.
17:34 < hezekiah> Mã hóa chắc chỉ mất một hai giây
17:34 < jrand0m> < 5 giây, < 2 giây, > 10 giây, > 30 giây?
17:34 < thecrypto> có lẽ tôi sẽ mày mò chút với nó
17:34 < hezekiah> Giải mã có lẽ đâu đó giữa 5 hoặc 10 giây.
17:34 < jrand0m> hay đấy.
17:35 < jrand0m> hezekiah> anh đã nói chuyện với jeremiah chưa hoặc có tin gì về tình trạng của Python client API không?
17:35 < hezekiah> thecrypto: Tất cả những gì anh cần là viết một mô-đun C hoạt động với Python.
17:35 < hezekiah> Tôi không biết anh ta đang làm gì.
17:35 < hezekiah> Tôi chưa nói chuyện với anh ấy từ lúc tôi quay lại.
17:35 < jrand0m> ok
17:35 < jrand0m> còn ý kiến tình hình phát triển nào khác không?
17:36 < hezekiah> Ờ, không hẳn từ tôi.
17:36 < hezekiah> Tôi đã nói về tình trạng thời gian rảnh hiện tại của mình rồi.
17:36 < jrand0m> chuẩn.  hiểu rồi
17:36 < hezekiah> Kế hoạch duy nhất của tôi là dựng C API và đưa Python router về đúng theo spec.
17:37 < jrand0m> ok
17:37 < hezekiah> Ôi trời!
17:37 < jrand0m> 1.4) việc cần làm
17:37 < jrand0m> si sr?
17:37 < hezekiah> Thư viện mã hóa Python không triển khai CTS hay padding!
17:37 < hezekiah> Tôi sẽ phải tự làm bằng tay.
17:37 < jrand0m> hmm?  nó yêu cầu dữ liệu là bội số của 16 byte à?
17:37 < hezekiah> Ừ.
17:38 < jrand0m> heh
17:38 < jrand0m> thôi vậy.
17:38 < hezekiah> Hiện tại Python router dùng padding.
17:38 < jrand0m> ok.  đây là vài hạng mục đang tồn đọng mà cần hoàn thành.
17:38 < hezekiah> Giờ tôi nhớ ra.
17:38 < hezekiah> Ờ, để
17:38 < hezekiah> nói thẳng một điều.
17:38 < hezekiah> Python router thực ra không bao giờ nhằm để sử dụng thật.
17:39 < hezekiah> Nó chủ yếu để tôi nắm rất rõ spec và còn đạt được một điều nữa:
17:39 < hezekiah> Nó buộc Java router tuân thủ _chính xác_ theo spec.
17:39 < jrand0m> cả hai mục tiêu đều rất quan trọng.
17:39 < hezekiah> Đôi khi Java router không hoàn toàn tuân thủ, và khi đó Python router sẽ la làng.
17:39 < hezekiah> Vậy nên nó không thật sự cần phải nhanh hay ổn định.
17:39 < jrand0m> vả lại tôi không chắc nó sẽ không bao giờ được dùng trong SDK
17:39 < jrand0m> đúng.  chính xác.
17:39 < jrand0m> nhưng Python client API là chuyện khác
17:39 < hezekiah> Còn Python client API thì cần phải tử tế.
17:40 < jrand0m> chính xác.
17:40 < hezekiah> Nhưng đó là việc của jeremiah. :)
17:40 < hezekiah> Tôi đã để anh ấy lo phần đó.
17:40 < jrand0m> các router local-only của SDK chỉ dành cho dùng phát triển client
17:40 < jrand0m> lol
17:40 < jrand0m> ok, như tôi đang nói... ;)
17:40 < hezekiah> ;-)
17:41 < jrand0m> - chúng ta cần ai đó bắt đầu làm một trang web nhỏ cho i2p để đăng các spec liên quan đến I2P cho cộng đồng phản biện.
17:41 < jrand0m> Tôi muốn việc này sẵn sàng trước 9/1.
17:41 < hezekiah> OK. Tôi nói luôn là anh không muốn tôi làm chuyện đó đâu.
17:41 < hezekiah> Tôi không phải là người thiết kế web giỏi. :)
17:41 < jrand0m> tôi cũng vậy, nếu ai ở đây đã thấy flog của tôi ;)
17:41 < jrand0m> cohesion?  ;)
17:41 < hezekiah> lol
17:42 < hezekiah> Tội nghiệp cohesion, lúc nào cũng bị dính việc nặng nhọc. :-)
17:42  * cohesion đang đọc backlog
17:42 < hezekiah> ;)
17:42 < jrand0m> heh
17:42 < cohesion> jrand0m: Tôi sẽ làm
17:42 < cohesion> me@jasonclinton.com
17:42 < cohesion> gửi tôi các spec đi
17:42 < jrand0m> ok, gracias.
17:42 < jrand0m> các spec chưa xong hết.
17:43 < jrand0m> nhưng nội dung cần có sẽ là:
17:43 < cohesion> ừ, cái anh có và cái anh muốn đưa lên
17:43 < jrand0m> -I2CP spec, I2NP spec, Polling HTTP Transport spec, TCP Transport spec, Security analysis, Performance analysis, Data structure spec, và một readme/intro
17:44 < jrand0m> (7 tài liệu đó sẽ ở định dạng pdf và/hoặc text)
17:44 < cohesion> k
17:44 < jrand0m> trừ readme/intro
17:45 < jrand0m> Tôi hy vọng tất cả các tài liệu đó sẽ sẵn sàng trước tuần tới (8/26).  như vậy anh có đủ thời gian để dựng một trang nhỏ cho lần phát hành 9/1 không?
17:46 < jrand0m> ok.  một việc nữa sẽ cần làm là một bộ mô phỏng mạng I2P.
17:46 < jrand0m> có ai đang tìm một đồ án CS (Khoa học máy tính) không?  ;)
17:46 < hezekiah> lol
17:46 < cohesion> jrand0m: ừ, làm được
17:47 < hezekiah> Tôi thì không, phải vài năm nữa. ;-)
17:47 < jrand0m> tuyệt cohesion
17:47 < thecrypto> chưa, phải một năm nữa
17:47  * cohesion quay lại làm việc
17:47 < jrand0m> tnx cohesion
17:48 < jrand0m> ok, 1.6) hai tuần tới.  việc của tôi là đưa các spec, tài liệu và phân tích này lên.  Tôi sẽ post &amp; commit sớm nhất có thể.
17:48 < jrand0m> LÀM ƠN ĐỌC CÁC SPEC VÀ GÓP Ý
17:48 < jrand0m> :)
17:48 < hezekiah> jrand0m: Ừ. Khi có thời gian, tôi sẽ bắt đầu đọc. :)
17:48 < jrand0m> Tôi muốn mọi người gửi góp ý lên danh sách, nhưng nếu muốn ẩn danh, hãy gửi riêng cho tôi và tôi sẽ đăng phản hồi lên danh sách một cách ẩn danh.
17:49 < hezekiah> (Theo anh thì ETA cho việc đưa các file OpenOffice của tài liệu lên CVS là khi nào?)
17:49 < jrand0m> Tôi có thể commit các revision mới nhất trong vòng 10 phút sau khi cuộc họp này kết thúc.
17:49 < hezekiah> Tuyệt. :)
17:50 < jrand0m> ok, vậy là xong phần 1.*.
17:50 < jrand0m> 2.x) bình luận/câu hỏi/quan ngại/cằn nhằn?
17:50 < jrand0m> sdk mod chạy thế nào rồi, mihi?
17:51 < jrand0m> hoặc ai khác?  :)
17:51 < hezekiah> jrand0m: Cái sdk mod mà anh đang nói là gì vậy?
17:52 < jrand0m> hezekiah> hai bản sửa lỗi cho sdk, đã commit (&amp; post) hôm trước
17:52 < hezekiah> À
17:52 < hezekiah> Hay phết.
17:52 < jrand0m> (xoay vòng message IDs, đồng bộ các thao tác ghi)
17:52 < hezekiah> Chỉ phía Java, hay cả phía Python nữa?
17:52 < jrand0m> yo no hablo python.
17:53 < hezekiah> lol
17:53 < jrand0m> không chắc các lỗi đó có ở đó không.  anh có xoay vòng message id mỗi 255 thông điệp, và đồng bộ các thao tác ghi không?
17:54 < hezekiah> Tôi nghĩ Python router làm cả hai
17:54 < jrand0m> tốt.
17:54 < jrand0m> nếu không thì bọn tôi sẽ báo anh ;)
17:54 < hezekiah> Chính xác thì anh muốn nói gì bằng "synchronize your writes"?
17:55 < jrand0m> tức là đảm bảo nhiều thông điệp không được ghi tới một client cùng lúc nếu có nhiều client đang cố gửi thông điệp tới nó cùng lúc.
17:55 < hezekiah> Tất cả dữ liệu gửi qua kết nối TCP đều được gửi theo đúng thứ tự nó được tạo ra.
17:56 < hezekiah> Vậy nên sẽ không có chuyện 1/2 thông điệp A rồi đến 1/3 thông điệp B.
17:56 < jrand0m> ok
17:56 < hezekiah> Anh sẽ nhận thông điệp A rồi đến thông điệp B.
17:56 < hezekiah> OK ... nếu không ai nói nữa, tôi đề nghị chúng ta bế mạc cuộc họp.
17:56 < mihi> TCP/IP over I2p đơn giản của tôi có vẻ chạy được...
17:56 < jrand0m> tuyệt quá!!
17:56  * mihi vừa idle một chút, xin lỗi
17:57 < hezekiah> Còn ai có gì muốn nói không?
17:57 < jrand0m> mihi> vậy chúng ta sẽ chạy pserver qua cái đó được chứ?
17:57 < mihi> miễn là bạn không cố tạo cả đống kết nối cùng lúc.
17:57 < mihi> jrand0m: chắc vậy - tôi có thể vào google qua đó
17:57 < jrand0m> tuyệt
17:57 < jrand0m> mihi++
17:57 < mihi> jrand0m-ava
17:57 < jrand0m> vậy bạn có một outproxy và một inproxy?
17:58 < mihi> chính xác.
17:58 < jrand0m> hay
17:58 < mihi> điểm đích cần key, nguồn tạo chúng khi cần
17:58  * hezekiah đưa cho jrand0m cái *baf*er. Đập nó khi xong việc nhé, ông bạn.
17:58 < jrand0m> đúng.  hy vọng dịch vụ đặt tên của co có thể giúp vụ đó khi nó sẵn sàng.
17:59 < jrand0m> ok hay đấy.  mihi, cho tôi hoặc ai khác biết nếu có gì bọn tôi có thể giúp nhé :)
17:59 < mihi> sửa cái vụ 128 msgid đó hoặc xây hỗ trợ GUARANTEED tốt hơn
17:59  * jrand0m *baf* vào đầu nop_afk vì dám có một công việc thật
18:00 < mihi> jrand0m: lạm dụng baf sẽ tốn 20 yodel
18:00 < jrand0m> lol
18:00 < jrand0m> hỗ trợ guaranteed tốt hơn?
18:00 < jrand0m> (tức là hiệu năng tốt hơn cái đã mô tả?  bọn tôi sẽ sửa trong phần impl)
18:00 < mihi> anh đã thử test case của tôi với start_thread=end_thread=300 chưa?
18:01 < mihi> nó tạo rất nhiều thông điệp theo một chiều, và điều đó làm tất cả msgid bị ăn hết...
18:01 < jrand0m> hmm, chưa, chưa thấy thông điệp đó
18:01 < hezekiah> jrand0m: Làm msgid thành 2 byte có hợp lý không?
18:01  * jrand0m đã thử 200 / 201, nhưng cái đó đã được sửa ở bản mới nhất
18:01 -!- cohesion [cohesion@anon.iip] đã thoát [đi họp lug]
18:01 < mihi> bản mới nhất nào?
18:01 < hezekiah> Như vậy họ sẽ có 65535 msgid (nếu bạn không tính msgid 0)
18:01 < hezekiah> .
18:02 < jrand0m> message id 2 byte cũng không hại gì.  Tôi thoải mái với thay đổi đó.
18:02 < jrand0m> mihi> cái tôi đã mail cho anh
18:02 < mihi> nếu anh có bản mới hơn bản anh gửi tôi, gửi nó đi (hoặc cho tôi quyền truy cập cvs)
18:03 < mihi> hmm, bản đó bị lỗi với tôi ở 200/201 (cũng như với 300)
18:03 < jrand0m> hmm.  Tôi sẽ thử nghiệm và debug thêm rồi mail anh những gì tôi tìm ra.
18:03 < mihi> thx.
18:04 < jrand0m> ok.
18:04  * jrand0m tuyên bố cuộc họp
18:04 < jrand0m> *baf*'ed
18:04  * hezekiah treo *baf*er một cách cung kính lên giá đặc biệt của nó.
18:05  * rồi hezekiah quay người bước ra cửa, đóng sầm phía sau. Cái baffer rơi khỏi giá.
18:05 < hezekiah> ;-)
--- Log đóng Tue Aug 19 18:05:36 2003 </div>
