---
title: "Cuộc họp các nhà phát triển I2P"
date: 2003-07-15
author: "nop"
description: "Cuộc họp phát triển I2P bao gồm cập nhật dự án và thảo luận kỹ thuật"
categories: ["meeting"]
---

(Được cung cấp bởi Wayback Machine http://www.archive.org/)

## Tóm tắt nhanh

<p class="attendees-inline"><strong>Có mặt:</strong> gott, hezekiah, jeremiah, jrand0m, mihi, Neo, nop, WinBear</p>

## Nhật ký cuộc họp

<div class="irc-log"> --- Nhật ký mở Tue Jul 15 17:46:47 2003 17:46 < gott> chào. 17:46 <@nop> chỉ báo trước về sự im lặng của tôi 17:46 <@hezekiah> Tue Jul 15 21:46:49 UTC 2003 17:47 <@hezekiah> OK. Cuộc họp iip-dev đã bắt đầu. 17:47 <@hezekiah> Đây là lần thứ 48 hay 49? 17:47 < jrand0m> nop> đây là lý do tại sao điều then chốt là chúng ta phải 	hoàn thiện kiến trúc router càng sớm càng tốt. Tôi hiểu rằng mỗi người có 	tốc độ khác nhau, và chúng ta phải phân đoạn để các thành phần khác nhau có thể 	tiến hành tương ứng 17:47 < mihi> 49 17:47 <@hezekiah> OK! Chào mừng đến với cuộc họp iip-dev lần thứ 49! 17:47 < jrand0m> Tôi còn ba ngày nữa ở chỗ làm, sau đó hơn 90 giờ / 	tuần sẽ dành để đẩy việc này chạy 17:48 < jrand0m> Tôi biết và không mong mọi người đều làm được như vậy, 	đó là lý do cần phân đoạn 17:48 < jrand0m> chào hezekiah :) 17:48 <@hezekiah> lol 17:48 <@nop> để phản biện về điều đó 17:48 <@hezekiah> Tôi sẽ đợi một phút. Rồi chúng ta vào chương trình nghị sự. :) 17:48 <@nop> tính an toàn của kiến trúc router phụ thuộc vào việc bạn 	không vội vàng 17:49 <@nop> nếu chúng ta làm vậy 17:49 <@nop> chúng ta sẽ bỏ sót 17:49 <@nop> và có thể phải dọn dẹp một mớ hỗn độn sau này 17:49 -!- Rain [Rain@anon.iip] đã thoát [I Quit] 17:49 < jrand0m> nop> không đồng ý. ta vẫn có thể xây dựng tầng ứng dụng và API 	mà không cần triển khai router (thậm chí chưa biết mạng sẽ vận hành ra sao) 17:49 <@nop> Tôi đồng ý với điểm đó 17:50 <@nop> Tôi đang nói cụ thể về mạng nền tảng 17:50 < jrand0m> nếu ta có thể đồng ý với API tôi đã gửi, thì đó là sự 	phân đoạn chúng ta cần 17:50 < jrand0m> đúng, triển khai router và thiết kế mạng vẫn chưa xong 17:50 <@nop> ok 17:50 <@nop> ồ, tôi chắc chắn đồng ý với API của bạn đến giờ 17:51 <@hezekiah> jrand0m: Có một vấn đề. 17:51 < jrand0m> nói đi hezekiah 17:51 <@hezekiah> Nó sẽ trông khác nếu bạn triển khai bằng C. 17:51 < jrand0m> không khác quá đâu 17:51 < gott> ôi trời 17:51 < jrand0m> ít chữ hoa hơn, và thay đối tượng bằng struct 17:51 < gott> mọi người đang cân nhắc triển khai bằng ngôn ngữ nào? 17:51 < jrand0m> (đối với API) 17:51 <@hezekiah> Ờ, jrand0m? Trong C không có 'byte[]'. 17:51 < jrand0m> gott> đọc lưu trữ thư để xem vài câu trả lời ví dụ 17:52 <@hezekiah> Bạn sẽ dùng void* với một số nguyên để chỉ độ 	dài có thể là hợp lý nhất. 17:52 < jrand0m> hezekiah> vậy thì unsigned int[] 17:52 < gott> jrand0m: hiếm khi có một cuộc chiến tôn giáo mà tôi không tham gia 17:52 <@hezekiah> Nếu tôi nhớ đúng (giúp tôi ở đây nop), bạn không thể 	đơn giản trả về unsigned int[] từ một hàm. 17:53 <@hezekiah> gott: so với cái gì? mã giả à? 17:53 < jrand0m> đúng, khác biệt về cú pháp. nhưng nếu có khác biệt 	thực sự, ta cần xử lý ngay càng sớm càng tốt. (ví dụ, hôm nay) Có lẽ 	giờ là lúc xem email tôi gửi tựa "high level 	router architecture and API" và cùng duyệt? 17:54 <@hezekiah> nop? UserX? Mọi người sẵn sàng chứ? 17:54 < jrand0m> không khác quá, nhưng vẫn khác, đúng. 	đó là lý do tôi nói Java API trong email hôm nay :) 17:54 -!- WinBear [WinBear@anon.iip] đã vào #iip-dev 17:55 <@nop> đợi 17:55 <@nop> đọc phía trên 17:55 -!- mihi_2 [~none@anon.iip] đã vào #iip-dev 17:55 -!- mihi giờ là nickthief60234 17:55 -!- mihi_2 giờ là mihi 17:55 < jrand0m> wb mihi 17:55 < gott> nhân tiện, cái này có được ghi trực tiếp không? 17:55 -!- nickthief60234 [~none@anon.iip] đã thoát [EOF From client] 17:55 <@hezekiah> gott: Có. 17:55 < mihi> dư thừa là vua ;) 17:55 < gott> Vậy tôi sẽ đọc lại sau. 17:55 -!- gott [~gott@anon.iip] đã rời #iip-dev [gott] 17:56 <@nop> ok 17:56 <@nop> đúng vậy 17:56 < WinBear> jrand0m: chào 17:56 <@nop> chắc chắn có khác biệt 17:56 <@nop> điều chúng ta cần 17:56 < jrand0m> chào WinBear 17:56 <@nop> là một nhóm nhà phát triển nhất định để viết lớp điều khiển 	api chính cho các ngôn ngữ này 17:56 <@nop> ta biết jrand0m có thể lo Java 17:56 <@nop> và có thể bắt cặp với thecrypto nữa 17:56 <@nop> còn hezekiah và nhóm có thể làm C 17:56 <@nop> và jeremiah nếu sẵn lòng 17:56 <@nop> có thể làm python 17:56 <@hezekiah> Tôi cũng làm được C++! ;-) 17:56 <@nop> ok 17:56 <@nop> cả C++ nữa 17:57 <@hezekiah> lol 17:57 <@nop> C++ có lẽ sẽ hoạt động 17:57 <@nop> cùng với C 17:57 <@nop> nếu bạn đừng template quá đà 17:57 < jrand0m> heh 17:57 <@hezekiah> lol 17:57 <@hezekiah> Thực ra, trong khi MSVC có thể liên kết file đối tượng C và C++, 	gcc có vẻ không thích. 17:57 <@nop> tức là, bám vào các struct tương thích với C, hay điều đó 	không khả thi 17:57 < jrand0m> câu hỏi đầu tiên, trước khi bàn, là những ứng dụng nào sẽ dùng 	các API này? Tôi biết có app sẽ muốn dùng Java, iproxy sẽ viết bằng C à? 17:58 <@hezekiah> nop: Tôi không nghĩ C và C++ tương thích đối tượng. 17:58 <@nop> ok 17:58 <@hezekiah> nop: C++ sẽ không hợp với C hơn Java là mấy. 17:58 <@nop> vậy có thể USerX làm C 17:58 <@nop> còn bạn lo C++ 17:58 <@hezekiah> Chúng ta khô 17:58 <@nop> ? 17:58 <@hezekiah> không cần phải _làm_ C++ nếu bạn không muốn. Chỉ là 	tôi thích nó. 17:59 <@nop> vấn đề là 17:59 <@nop> có nhiều lập trình viên C++ 17:59 <@nop> nhất là trong thế giới microsoft 17:59 <@hezekiah> Cả trong thế giới Linux nữa. (xem: KDE và Qt.) 17:59 < jrand0m> C và C++ tương thích nhị phân nếu bạn chỉ tạo .so hoặc .a 17:59 < jrand0m> (nhân tiện) 18:00 <@nop> C có thể là chỗ đứng tốt cho C++ không, tức là lập trình viên C++ 	sẽ dễ xử lý một api C hơn so với một api C++ với lập trình viên C? 18:00 <@hezekiah> jrand0m: Ừ. Bạn có thể có thư viện ... nhưng nếu 	bạn 18:00 <@hezekiah> jrand0m: thậm chí không dùng được class, thì hơi sai mục 	đích. 18:00 <@nop> đúng 18:00 <@nop> hãy bám vào C 18:01 <@nop> vì coder C++ vẫn gọi thư viện C khá dễ 18:01 <@hezekiah> Nếu một mô-đun cần gọi hàm của mô-đun khác, thì tốt nhất 	cả hai cùng một ngôn ngữ. 18:01 <@hezekiah> nop: coder C++ sẽ biết C đủ ... dù có thể tốn công nếu họ 	chưa bao giờ /học/ C. 18:02 <@hezekiah> Tuy nhiên, coder C sẽ không biết C++ vì C chỉ là 	tập con của C++. 18:02 -!- logger_ [~logger@anon.iip] đã vào #iip-dev 18:02 -!- Chủ đề cho #iip-dev: logfiles sẽ online sau cuộc họp: 	http://wiki.invisiblenet.net/?Meetings 18:02 [Người dùng #iip-dev] 18:02 [@hezekiah] [+Ehud    ] [ leenookx] [ moltar] [ tek    ] 18:02 [@nop     ] [ jeremiah] [ logger_ ] [ Neo   ] [ WinBear] 18:02 [@UserX   ] [ jrand0m ] [ mihi    ] [ ptsc  ] 18:02 -!- Irssi: Tham gia #iip-dev được đồng bộ trong 9 giây 18:02 < jrand0m> đúng 18:02 -!- Irssi: Join to #iip-dev was synced in 9 secs 18:02 < jrand0m> (với JMS :) 18:02 <@nop> chuẩn 18:03 -!- Bạn giờ được biết đến là logger 18:03 < jrand0m> ok, ta có thể duyệt kiến trúc tổng thể để xem liệu 	các API có phù hợp trước không? 18:03 <@nop> được  18:04 < jrand0m> :) 18:04 < jrand0m> ok, xem email tôi gửi kèm routerArchitecture.png. 	anh em có ý kiến gì về sự tách lớp đó không? 18:04 -!- tek [~tek@anon.iip] đã thoát [] 18:05 < WinBear> jrand0m: cái đó có trên wiki không? 18:05 < jrand0m> WinBear> không, trên mailing list, nhưng lưu trữ 	đang down. để tôi thêm vào wikki 18:06 <@hezekiah> Sửa tôi nếu tôi sai ... 18:07 <@hezekiah> ... nhưng có vẻ chúng ta sẽ có 3 API riêng 	nhưng giống nhau tối đa có thể. 18:07 <@hezekiah> Đúng chứ? 18:07 < jrand0m> đúng hezekiah 18:07 <@hezekiah> Vậy vì mỗi API ở một ngôn ngữ khác, chúng sẽ 	mỗi cái có triển khai riêng? 18:07 < jrand0m> đúng 18:07 <@hezekiah> Hay có cách để Java hoặc Python truy cập thư viện C? 18:08 < jrand0m> có, nhưng ta không muốn đi hướng đó 18:08 < mihi> cho java: JNI 18:08 <@hezekiah> Vậy chuyện Java, C, C++, Python, v.v. làm việc 	cùng nhau là vô nghĩa vì chúng sẽ không bao giờ? 18:08 < jrand0m> làm sao tôi đính kèm ảnh lên wiki? 18:08 <@hezekiah> Mỗi API có backend của riêng nó viết bằng ngôn ngữ đó. 18:08 < jrand0m> không hezekiah, nhìn vào sơ đồ 18:09 <@hezekiah> Ồ, chết thật! 18:09 <@hezekiah> Các API không liên kết đến một backend. 18:10 <@hezekiah> Chúng nói chuyện qua socket. 18:10 < jrand0m> si sr 18:10 <@hezekiah> Dù vậy vẫn hơi khó hiểu. 18:10 <@hezekiah> Cho tôi chút nhé. :) 18:11 <@hezekiah> OK. Cái nhãn 'transport' là gì? 18:11 < jrand0m> ví dụ, transport HTTP hai chiều, transport SMTP, 	socket thuần, polling HTTP socket, v.v. 18:11 < jrand0m> cái di chuyển byte giữa các router 18:12 <@hezekiah> OK. 18:12 <@hezekiah> Vậy sơ đồ tôi đang nhìn là máy tính của một người. 18:12 <@hezekiah> Họ có một router nói chuyện với máy của người khác 	qua các transport. 18:12 < jrand0m> đúng 18:12 <@hezekiah> Người 1 (Alice) chạy 2 ứng dụng. 18:12 <@hezekiah> Một cái viết bằng C, cái kia bằng Java. 18:13 <@hezekiah> Cả hai liên kết tới một thư viện (đó là API). 18:13 < jrand0m> cả hai "liên kết" tới thư viện riêng (các API) 18:13 <@nop> khái niệm đơn giản 18:13 <@nop> đúng 18:13 <@hezekiah> Những thư viện đó lấy đầu vào từ chương trình, mã hóa, 	và gửi qua socket (unix hoặc TCP) tới router ... là một chương trình khác 	mà Alice đang chạy. 18:13 < jrand0m> đúng 18:14 <@hezekiah> OK. Nó hơi giống isproxy tách làm hai. 18:14 < jrand0m> bingo :) 18:14 <@hezekiah> Một phần là tầng thấp viết bằng C, phần kia là 	tầng cao viết bằng bất kỳ thứ gì. 18:14 < jrand0m> chính xác 18:14 <@hezekiah> OK. Tôi hiểu rồi. :) 18:14 < jrand0m> w00t 18:14 <@hezekiah> Vậy không ngôn ngữ nào cần phải chơi đẹp với ngôn ngữ khác. 18:14 < jrand0m> WinBear> xin lỗi, tôi không thể đưa lên wiki vì nó chỉ 	nhận văn bản :/ 18:15 <@hezekiah> Vì tất cả nói chuyện với router qua socket, 	bạn có thể viết API bằng PASCAL nếu thiết kế muốn. 18:15 <@nop> đúng 18:15 <@nop> tùy ý 18:15 < jrand0m> đúng 18:15 <@nop> nó xử lý socket tùy ý 18:15 < jrand0m> dù một số thứ cần chuẩn hóa (như cấu trúc dữ liệu 	cho Destination, Lease, v.v.) 18:15 < WinBear> jrand0m: tôi hình dung mơ hồ dựa trên những gì hezekiah nói 18:15 < jrand0m> chuẩn 18:16 <@hezekiah> jrand0m: Đúng. Cấu trúc và thứ tự của các byte 	trên socket đó được định trong một thiết kế nào đó 18:16 <@hezekiah> ở đâu đó. 18:17 <@hezekiah> Nhưng bạn vẫn có thể triển khai cách gửi và 	nhận các byte theo cách bạn thích. 18:17 <@nop> WinBear: nó giống hệt cách client irc hoạt động 	với isproxy 18:17 < jrand0m> chính xác 18:17 <@hezekiah> Tốt. 18:17 <@hezekiah> Giờ tôi hiểu. :) 18:17 -!- moltar [~me@anon.iip] đã rời #iip-dev [moltar] 18:17 <@nop> à 18:17 <@nop> không hoàn toàn 18:17 <@hezekiah> Ối. 18:17 <@nop> nhưng tưởng tượng cách nó hoạt động 18:17 <@nop> là bạn hiểu socket tùy ý 18:17 <@nop> isproxy chỉ định tuyến 18:17 <@nop> và chuyển phát 18:18 <@nop> giờ jrand0m 18:18 <@nop> hỏi nhanh 18:18 < jrand0m> si sr? 18:18 <@nop> api này chỉ thiết kế cho ứng dụng mới được thiết kế 	để hoạt động trên mạng này thôi à 18:18 -!- mode/#iip-dev [+v logger] do hezekiah 18:18 < WinBear> nop: với highlevel thay thế irc client? 18:18 < jrand0m> nop> đúng. dù một proxy SOCKS5 cũng có thể dùng API này 18:18 <@nop> hay có thể có một middle man để cho phép client chuẩn sẵn có 18:18 <@nop> ví dụ 18:19 <@nop> để ta chỉ phải viết middleman -> api 18:19 < jrand0m> (nhưng lưu ý là không có dịch vụ 'lookup' - 	không có DNS cho mạng này) 18:19 < jrand0m> đúng 18:19 <@nop> để ta có thể hỗ trợ như Mozilla v.v. 18:19 <@nop> để họ chỉ cần code plugin 18:19 < jrand0m> nop> đúng 18:19 <@nop> ok 18:19 <@nop> hoặc transport :) 18:20 < jrand0m> (ví dụ SOCKS5 có các HTTP outproxy hardcode tới 	destination1, destination2, và destination3) 18:20 <@nop> ok 18:20 < WinBear> tôi nghĩ tôi hiểu rồi 18:21 < jrand0m> w00t 18:21 < jrand0m> ok, một trong những điều tôi phải nghĩ trong thiết kế này 	là giữ private key trong không gian nhớ của app - router không bao giờ 	giữ private key của destination. 18:21 <@hezekiah> Vậy ứng dụng có thể gửi dữ liệu thô qua mạng I2P 	bằng cách gửi cho API, và nó không cần lo những phần còn lại. 18:22 <@hezekiah> Đúng chứ? 18:22 < jrand0m> tức API cần triển khai phần mã hóa đầu-cuối 18:22 < jrand0m> chính xác hezekiah 18:22 <@hezekiah> OK. 18:22 <@nop> đúng 18:22 <@nop> ý tưởng là vậy 18:22 <@nop> nó làm giúp bạn 18:22 <@nop> bạn chỉ gọi hook 18:23 <@hezekiah> Một câu nhanh: 18:23 <@hezekiah> 'router' rõ ràng cần nói một giao thức nhất định 	trên các transport của nó. 18:23 < jrand0m> đúng 18:23 <@hezekiah> Vậy có thể cung cấp nhiều triển khai router ... 18:23 < jrand0m> có 18:24 <@hezekiah> ... miễn là chúng cùng nói một giao thức. 18:24 < jrand0m> (đó là lý do spec có chỗ dành cho bitbuckets (bit bucket: cấu trúc trường bit)) 18:24 < jrand0m> đúng 18:24 <@hezekiah> Vậy bạn có một router bằng Java, một bằng C, và một 	bằng PASCAL. 18:24  * jrand0m rùng mình 18:24 < jrand0m> nhưng ừ 18:24 <@hezekiah> Và tất cả có thể nói chuyện với nhau vì chúng nói qua 	TCP/IP bằng cùng giao thức. 18:24  * WinBear giật mình 18:24 <@hezekiah> jrand0m: Và đúng. Tôi cũng không nhớ thời PASCAL 	một cách quá êm đẹp. 18:25 < jrand0m> ờ thì, Pascal có thể nói với con C qua transport TCP, 	còn con C có thể nói với con Java qua transport HTTP, ví dụ vậy 18:25 <@hezekiah> Đúng. 18:25 < jrand0m> (các transport nói với transport cùng loại, router quản lý 	các thông điệp được chuyển giữa chúng nhưng không xử lý cách chúng được chuyển) 18:26 <@hezekiah> Điểm tôi muốn nói là giao thức là như nhau, nên không 	quan trọng router của ai viết bằng ngôn ngữ nào. 18:26 < jrand0m> đúng 18:26 <@hezekiah> Tuyệt. 18:26 < jrand0m> giờ bạn hiểu vì sao tôi nói "ai quan tâm" với mấy tranh luận 	C vs Java vs v.v. chứ?  :) 18:26 <@hezekiah> Rồi. 18:26 <@hezekiah> lol 18:27 <@hezekiah> Phải công nhận với bạn jrand0m. Cách này sẽ làm 	cho nhà phát triển viết chương trình cho mạng này rất dễ chịu. 18:27 < jrand0m> heh, thật ra API này không hẳn nguyên bản. đây là cách 	Message Oriented Middleware (MOM) hoạt động 18:27 <@hezekiah> Và bạn còn có thể làm router chuyên biệt cho một số 	tính năng đặc thù nền tảng (như CPU 64-bit). 18:28 < jrand0m> hoàn toàn 18:28 <@hezekiah> jrand0m: Khiêm tốn nữa! ;-) 18:28 <@hezekiah> Tốt, trông ổn với tôi. 18:28 < jrand0m> ok, UserX, nop, sự tách lớp này có hợp lý không? 18:28 <@nop> tất nhiên 18:28 <@nop> userx còn ở đây không 18:29 <@hezekiah> Anh ấy idle 1:26 rồi. 18:29 < jrand0m> 'k. vậy ta có hai nhiệm vụ: thiết kế mạng, và 	thiết kế cách API hoạt động. 18:29 <@nop> đúng 18:29 <@hezekiah> Câu đơn giản: Các API làm mã hóa đầu-cuối. 	các router làm mã hóa nút-nút chứ? 18:29 <@nop> đúng 18:30 < jrand0m> đúng 18:30 < jrand0m> (cấp độ transport) 18:30 <@hezekiah> Tốt. :) 18:30 <@nop> hezekiah: nó rất giống với những gì ta có đến giờ 18:30 <@nop> ở khía cạnh đó 18:31 < jrand0m> ok.. ờ, chết, thecrypto không có mặt để bình luận 	về mô hình hiệu năng. 18:31 < Neo> và cho người đa nghi, app có thể làm mã hóa pgp trước 	khi tới API ;) 18:31 < jrand0m> hoàn toàn neo 18:31 < jrand0m> Tôi còn định bỏ phần mã hóa đầu-cuối khỏi 	API và để app tự lo... 18:31 <@hezekiah> jrand0m: Như vậy thì ác quá. 18:31 < jrand0m> heheh 18:32 <@hezekiah> Nhân tiện, API và router giao tiếp qua socket. 18:32 <@hezekiah> Trên UNIX chúng sẽ dùng UNIX socket hay TCP/IP 	cục bộ? 18:32 < jrand0m> chắc chỉ TCP/IP cục bộ cho đơn giản 18:32 <@nop> chờ đã 18:32 <@hezekiah> (Tôi nghĩ bạn có thể làm một router chấp nhận cả hai.) 18:33  * hezekiah thực sự thích cấu hình linh kiện có thể thay thế này 18:33 <@nop> nếu bạn chờ chút 18:34 <@hezekiah> Đang chờ ... :) 18:34 <@nop> Tôi sẽ gọi thecrypto ở nhà 18:34 <@nop> xem anh ấy có vào được không 18:34 < jrand0m> hehe chuẩn 18:34 <@hezekiah> lol 18:34  * hezekiah giả giọng Ý dày cộp 18:34 <@hezekiah> Nop có ... MỐI QUAN HỆ! 18:34 < jeremiah> chào 18:34 <@nop> chào jeremiah 18:35 < jrand0m> chào jeremiah 18:35 <@nop> bạn có sẵn lòng ở tầng api hỗ trợ api python không 18:35 < jeremiah> được chứ 18:35  * jeremiah đọc backlog 18:35 < jrand0m> heh chuẩn 18:35  * nop đang gọi 18:36 <@nop> anh ấy không ở nhà 18:36 <@nop> sẽ về sau một giờ 18:36 < jrand0m> 'k, có ai khác đọc .xls và/hoặc có bình luận về 	mô hình không? 18:37 <@hezekiah> Tôi đọc .xls ... nhưng tôi không biết nhiều về p2p nên 	đa phần vượt quá tầm tôi. 18:37 <@hezekiah> UserX giỏi khoản đó. 18:37 <@nop> Tôi còn phải đọc 18:37 < jrand0m> (nhân tiện, morphmix có vài con số điên rồ... họ nói 	có thể kỳ vọng host ngẫu nhiên trên net có ping trung bình 20-150ms, 	thay vì 3-500 như tôi kỳ vọng) 18:37 < jrand0m> hay đó 18:37 <@nop> nó là staroffice hay openoffice? 18:37 < jrand0m> openoffice, nhưng tôi xuất ra .xls 18:37 <@nop> tức là excell? 18:37 < jrand0m> đúng 18:38 <@hezekiah> Nhân tiện, về API ... 18:38 < jrand0m> si sr? 18:38 <@hezekiah> ... trong C boolean sẽ là int. 18:38 <@nop> email nào 18:38 <@nop> hezekiah: đúng 18:38 <@hezekiah> Các class sẽ được gửi dưới dạng con trỏ cấu trúc. 18:38 <@nop> trừ khi bạn typedef boolean 18:39 <@hezekiah> Và các hàm dùng byte[] sẽ dùng void* với 	một tham số bổ sung chỉ chiều dài buffer. 18:39 <@nop> hezekiah: bạn đang bắt bẻ đấy :) 18:39 < jrand0m> nop> Tôi không truy cập được lưu trữ nên không chắc 	dòng chủ đề là gì, nhưng là tuần trước... 18:39 <@nop> để dành lúc khác 18:39 <@hezekiah> nop: Bắt bẻ? 18:39 < jrand0m> heh, vâng, mọi người làm C api có thể tự xử lý chi tiết đó 18:39  * jeremiah đọc xong backlog 18:39 <@nop> file tên gì 18:39 <@hezekiah> nop: Tôi chỉ cố tìm tất cả các thứ khác nhau, 	để chúng ta đập cho ra như jrand0m yêu cầu. 18:40 <@hezekiah> Tôi đang cố giúp mà. :) 18:40 <@nop> hezekiah: vâng, có lẽ ngoài giờ họp 18:40 < jrand0m> nop> simple_latency.xls 18:40 <@hezekiah> boolean sendMessage(Destination dest, byte[] payload); 18:40 <@hezekiah>  sẽ là 18:40 <@hezekiah> int sendMessage(Destination dest, void* payload, int length); 18:40 <@hezekiah> . 18:40 <@hezekiah> byte[]  recieveMessage(int msgId); 18:40 <@hezekiah>  cái đó có thể là: 18:41 <@hezekiah> void*  recieveMessage(int msgId, int* length); 18:41 <@hezekiah>  hoặc 18:41 <@nop> jrand0m: nhận rồi 18:41 <@hezekiah> void recieveMessage(int msgId, void* buf, int* length); 18:41 <@hezekiah>  hoặc 18:41 < jrand0m> hezekia: sao không typedef struct { int length; void* data; 	} Payload; 18:41 <@hezekiah> DataBlock* recieveMessage(int msgId)l 18:41 <@hezekiah> DataBlock* recieveMessage(int msgId); 18:41 < jeremiah> file xls ở đâu? 18:41 <@nop> oh iip-dev 18:41 <@hezekiah> jrand0m: struct bạn vừa nhắc về cơ bản là 	DataBlock. 18:42 < jrand0m> chuẩn hezekiah 18:42 <@nop> chủ đề more models 18:42 <@hezekiah> Nhiều khả năng bản C sẽ có DataBlock. 18:43 <@hezekiah> Ngoài ra điều cần lưu ý là mỗi 	'interface' sẽ chỉ là một tập hàm. 18:43 <@hezekiah> nop: Tôi có tìm ra hết khác biệt có thể có trong 	một C API không? 18:43 < jrand0m> đúng. có thể #include "i2psession.h" hay gì đó 18:43 < jeremiah> có mockup api python không? 18:44 < jrand0m> không jeremiah, tôi không rành python :/ 18:44 <@nop> Tôi sẽ phải duyệt lại java api, nhưng tôi nghĩ 	bạn đi đúng hướng 18:44 < jrand0m> nhưng nó có thể tương tự java, vì python là OO 18:44 < jeremiah> tuyệt, tôi có thể suy ra từ bản C 18:44  * nop không phải dân java 18:44 < jrand0m> hay đấy jeremiah 18:44 < jeremiah> api c có trong cái bạn gửi vài ngày trước không? 18:44 <@hezekiah> Ừ. Python nên xử lý được api Java. 18:44 < jrand0m> jeremiah> cái đó là bản Java 18:45 < jrand0m> ồ, bản Java là hôm nay 18:45 < jrand0m> cái cũ là độc lập ngôn ngữ 18:45 <@hezekiah> Hmm 18:45 <@nop> UserX nói anh ấy có thể hỗ trợ C api 18:45 < jrand0m> chuẩn 18:45 <@nop> anh ấy đang bận ở chỗ làm 18:46 < jrand0m> hay đấy 18:46 <@hezekiah> Một lưu ý cuối: Với C api, mỗi hàm có lẽ 	nhận structure* tới cấu trúc mà nó là 'interface' trong Java. 18:46 <@nop> hezekiah: trông ổn 18:46 <@nop> trông tốt 18:46 <@hezekiah> I2PSession       createSession(String keyFileToLoadFrom, 	Properties options); 18:46 <@hezekiah>  sẽ là: 18:46 <@nop> java và các kiểu dữ liệu không native của họ 18:46 <@hezekiah> I2PSession* createSession(I2PClient* client, char* 	keyFileToLoadFrom, Properties* options); 18:46 <@nop> ;) 18:46 < jrand0m> hehe 18:46 < jrand0m> đúng hezekiah 18:47 < jeremiah> chúng ta có xử lý unicode không? 18:47 <@hezekiah> Dù sao, nếu chịu được các khác biệt đó, C và 	Java API sẽ tương đồng ngoài những điểm đó. 18:47 <@hezekiah> nop? Unicode? :) 18:47 < jrand0m> UTF8 nếu không thì UTF16 18:48 <@hezekiah> Có lẽ Unicode nên xử lý ở tầng ứng dụng. 18:48 < jrand0m> đúng, charset là nội dung thông điệp 18:48 <@hezekiah> Ồ. 18:48 < jeremiah> ok 18:48 <@hezekiah> Chuỗi trong Java dùng Unicode, đúng không jrand0m? 18:48 < jrand0m> các bitbucket sẽ được định nghĩa theo bit hết 18:48 < jrand0m> đúng hezekiah 18:48 < jrand0m> (trừ khi bạn chỉ định rõ đổi charset) 18:49 <@hezekiah> Vậy chuỗi gửi tới Java API sẽ khác với 	chuỗi gửi tới C API trừ khi C API triển khai chuỗi dùng Unicode. 18:49 < jrand0m> không liên quan 18:49 <@hezekiah> OK. 18:49 < jrand0m> (app->API != API->router. ta chỉ định nghĩa API->router) 18:49 <@hezekiah> Ý tôi là thế này, jrand0m: 18:50 <@hezekiah> Nếu tôi đặt mật khẩu bằng Java API, nó đi tới 	router rồi ra đâu đó. 18:50 < jrand0m> mật khẩu? bạn ý là bạn tạo một Destination? 18:50 <@hezekiah> Rồi nó tìm router khác, cái gửi nó tới API khác 	(?) được triển khai bằng C. 18:50 <@hezekiah>   void            setPassphrase(String old, String new); 18:50 <@hezekiah> Hàm đó. 18:51 < jrand0m> hezekiah> đó là mật khẩu quản trị để truy cập các 	phương thức quản trị của router 18:51 <@hezekiah> À 18:51 <@hezekiah> Có hàm nào trong API dùng Java String mà 	kết thúc bằng việc chuỗi đó được gửi tới API khác không? 18:51 < jrand0m> 99,9% app chỉ dùng I2PSession, không dùng I2PAdminSession 18:51 <@nop> ngoài ra, bất cứ gì mang theo router đều được chuyển đổi để 	du hành trên mạng đúng không? 18:51 <@hezekiah> Nếu có, ta có lẽ nên dùng Unicode. 18:51 <@nop> unicode không liên quan 18:52 < jrand0m> hezekiah> không.  mọi thông tin giữa router sẽ được định 	bởi bit buckets 18:52 <@hezekiah> OK. 18:52 < jrand0m> đúng nop, ở tầng transport 18:52 <@hezekiah> (Tôi đoán bit bucket chỉ là buffer nhị phân, đúng chứ?) 18:53 < jrand0m> bit bucket là tuyên bố rằng bit đầu nghĩa là X, 	bit thứ hai là Y, các bit 3-42 là Z, v.v. 18:53 < jrand0m> (ví dụ ta có thể muốn dùng X.509 cho bitbucket chứng chỉ)

18:53 <@hezekiah> Tôi chưa từng xử lý việc đó trước đây.
18:54 <@hezekiah> Tôi sẽ lo khi đến lúc. :)
18:54 < jrand0m> hề hề, chuẩn
18:55 < jrand0m> ok, bốn việc tôi muốn chúng ta bàn hôm nay: *router 	architecture, *performance model, *attack analysis, *psyc.  Chúng ta đã xong 	cái đầu tiên, thecrypto đang offline nên có lẽ hoãn cái đó (trừ khi bạn có 	ý tưởng về mô hình, nop?)
18:57 <@hezekiah> Ờ ... jrand0m. Tôi lại có thêm một câu hỏi.
18:57 < jeremiah> jrand0m: phiên bản mới nhất của đặc tả mạng ở đâu? is 	có phải là cái bạn đã gửi hôm 13 không?
18:57 < jrand0m> si sr?
18:57 <@hezekiah> Ờ thì kiến trúc router để cho API xử lý các khóa 	/được Ứng dụng gửi cho chúng/.
18:57 < jrand0m> jeremiah> đúng
18:57 <@nop> Tôi hiện không có
18:58 <@hezekiah> Giờ thì ... cách duy nhất tôi thấy API nhận được khóa là 	từ createSession.
18:58 < jrand0m> hezekiah> router  nhận các khóa công khai và chữ ký, 	chứ không nhận khóa riêng tư
18:58 < jrand0m> đúng rồi
18:58 <@hezekiah> Nhưng điều đó cần một tệp.
18:58 < jrand0m> các khóa được lưu trong một tệp hoặc trong bộ nhớ của API
18:58 < jrand0m> vâng
18:58 <@hezekiah> Bây giờ nếu ứng dụng tạo ra một khóa, sao nó không thể 	gửi thẳng cho API qua một bộ đệm?
18:59 <@hezekiah> Có thật là phải lưu nó vào một tệp, rồi cung cấp 	tên tệp không?
18:59 < jrand0m> không, có thể để trong bộ nhớ nếu bạn muốn
18:59 <@hezekiah> Tuy nhiên API không có hàm nào cho tất cả chuyện đó.
18:59 <@hezekiah> Chỉ là ý nghĩ thôi.
19:00 <@hezekiah> Nếu khóa dự kiến chỉ tạo một lần và dùng 	rất, rất nhiều lần (như khóa GPG), thì dùng tệp là hợp lý.
19:00 -!- mihi [none@anon.iip] đã thoát [chào mọi người, trễ rồi...]
19:00 <@hezekiah> Nhưng nếu nó sẽ được tạo thường xuyên hơn, thì có lẽ một 	cách gửi trực tiếp nó cho API qua một cấu trúc hoặc một bộ đệm nào đó 	sẽ hay hơn
19:00 <@hezekiah> .
19:01 < jrand0m> đúng, nó được tạo một lần và chỉ một lần (trừ khi bạn đang đội 	một chiếc mũ giấy bạc)
19:02 < jrand0m> tuy nhiên createDestination(keyFileToSaveTo) cho phép bạn 	tạo khóa đó
19:02 <@hezekiah> OK.
19:02 <@hezekiah> Vậy thật ra không cần truyền trực tiếp từ 	App sang API. Một tệp là đủ.
19:03 <@hezekiah> Vậy trước khi tôi thô lỗ ngắt lời, chúng ta đang bàn tới đâu rồi? :)
19:06 < jeremiah> vậy bây giờ chúng ta chỉ đang làm việc trên API của router, chứ 	không phải API phía client, đúng không?
19:06 < jrand0m> ừ, hiện chúng ta sẽ bỏ qua phân tích hiệu năng 	(hi vọng có thể bàn luận về nó trên mailing list trước tuần sau?).  và có lẽ tương tự với phân tích tấn công (trừ khi ai đó đã đọc 	spec mới và có ý kiến)
19:07 <@hezekiah> Vậy vì chúng ta bỏ qua cái đó, giờ chúng ta 	nên nói về điều gì?
19:07 <@hezekiah> Psyc?
19:07 < jrand0m> trừ khi ai khác có ý kiến nào muốn nêu ra...?
19:08 <@hezekiah> Ừm, hiếm khi vậy, cái lỗ phát biểu của tôi (cũng nổi tiếng là 	cái miệng) hôm nay trống rỗng.
19:08 < jrand0m> hehe
19:09 < jrand0m> ok, có ai có ý tưởng gì về cách phía IRC sẽ hoạt động, 	và liệu psyc có liên quan hay hữu ích không?
19:09 < jeremiah> ghi chú bên lề (làm tôi bực mình): danh sách "Wired, Tired, 	Expired" của Wired xếp Waste là 'wired'
19:09 < jrand0m> heh
19:09 < jrand0m> bạn có nhận ra chúng ta sẽ làm mọi người kinh ngạc đến mức nào không?
19:09 < jeremiah> ừ
19:09 <@hezekiah> jrand0m: Điều đó giả định là chúng ta khiến cái này hoạt động được.
19:10 < jrand0m> Tôi đảm bảo nó sẽ hoạt động.
19:10 <@hezekiah> Ngoài kia có rất nhiều nỗ lực thất bại khác.
19:10 < jrand0m> Tôi đã bỏ việc để làm cái này.
19:10 <@hezekiah> Vậy thì chúng ta sẽ làm mọi người choáng ngợp. :)
19:10 <@hezekiah> Ừ. Vậy cậu kiếm cơm kiểu gì khi làm thế?
19:10 <@hezekiah> Mã GPL không trả lương khá đâu. ;-)
19:10 < jrand0m> heh
19:11 <@hezekiah> Còn về psyc ... để tôi nói thế này:
19:11 <@hezekiah> Lần đầu tôi nghe về nó là khi bạn email cho chúng tôi 	về nó.
19:11 < jrand0m> chết tiệt, không phải tôi là người tìm ra nó đâu :)
19:11 <@hezekiah> Tuy nhiên, IRC có lẽ là một trong những giao thức chat phổ biến nhất (nếu không phải là /phổ biến nhất/) hiện nay.
19:11 <@hezekiah> Mọi người sẽ muốn các ứng dụng IRC từ RẤT LÂU trước khi họ /biết/ 	psyc là gì.
19:11 <@hezekiah> jrand0m: Ối. Xin lỗi. Tôi quên chi tiết đó. :)
19:12 < jrand0m> không theo psyc thì không.  lịch sử của họ quay lại tận năm 86 thì phải
19:12 <@hezekiah> Điểm mấu chốt là sự vượt trội của giao thức 	thật ra không quan trọng bằng việc ai đang dùng nó.
19:12 <@hezekiah> _Lịch sử_ của họ có thể quay lại xa đến vậy.
19:12 <@hezekiah> Nhưng có bao nhiêu người _dùng_ Psyc?
19:12 < jeremiah> ừ, nếu họ đã tồn tại từ một năm sau khi tôi sinh ra 	(ờ hêm) mà vẫn chưa lớn đến thế
19:12 <@hezekiah> Ý tôi là, ngay cả khi đó là một giao thức tốt hơn, thì đa số 	mọi người vẫn _dùng_ IRC.
19:13 <@hezekiah> Chúng ta có thể tạo ra mạng I2P tốt nhất hành tinh ...
19:13 -!- Ehud [logger@anon.iip] đã thoát [Hết thời gian chờ Ping]
19:14 < jeremiah> có ai giải thích ngắn gọn vì sao chúng ta quan tâm không? Tôi nghĩ IRC 	chỉ là một ứng dụng có thể có và mạng đủ linh hoạt để 	hỗ trợ psyc nếu muốn
19:14 <@hezekiah> Đúng.
19:14 <@hezekiah> Psyc có thể làm được ...
19:14 <@hezekiah> ... nhưng tôi nói ta nên làm IRC trước vì nhiều 	người dùng nó hơn.

19:14 <@hezekiah> jrand0m, chúng ta có thể tạo ra một mạng I2P tuyệt vời, nhưng mọi người sẽ không 	dùng nó trừ khi nó có thứ họ muốn.
19:14 < jrand0m> jeremiah> lý do psyc thú vị là vì chúng ta có thể 	muốn triển khai IRC theo cùng cách mà psyc hoạt động
19:15 <@hezekiah> Vì vậy chúng ta nên cung cấp cho họ một 'killer-app' (tức một ứng dụng đủ hấp dẫn để kéo người dùng đến).
19:15 < jeremiah> ok
19:15 < jrand0m> đúng, IIP là Invisible IRC Project, và sẽ cho phép mọi người 	chạy IRC
19:16 < jrand0m> không có máy chủ trung tâm (thực ra là chẳng có máy chủ nào hết), 	có rất nhiều điều phải suy nghĩ để tìm ra IRC sẽ hoạt động thế nào. 	psyc có một câu trả lời khả dĩ cho việc đó
19:16 < jrand0m> dù còn những cách khác
19:17 <@hezekiah> Như tôi đã nói, psyc có thể làm tốt hơn, nhưng người ta muốn dùng IRC, 	không phải psyc.
19:17 < jrand0m> và họ sẽ
19:17 < jrand0m> họ sẽ dùng irc
19:17 <@hezekiah> Tất cả là do marketing thôi, cưng à! ;-)
19:17 < jeremiah> Tối nay tôi sẽ cố đọc đặc tả và một số thứ về psyc
19:17 < jrand0m> chuẩn
19:17 <@hezekiah> lol
19:17 < jeremiah> dự định gặp lúc 5:00 UTC ngày mai?
19:17 <@hezekiah> Không?
19:18 < jeremiah> hoặc lúc nào cũng được
19:18 < jrand0m> Tôi ở trên iip 24x7 :)
19:18 < jeremiah> ừ nhưng tôi còn phải ăn chứ
19:18 <@hezekiah> jrand0m: Tôi để ý rồi.
19:18 < jrand0m> 05:00 utc hay 17:00 utc?
19:18 <@hezekiah> jeremiah: LOL!
19:18 <@hezekiah> Ừ thì cuộc họp iip-dev chính thức bắt đầu lúc 21:00 UTC.
19:18 -!- Ehud [~logger@anon.iip] đã vào #iip-dev
19:19 < jeremiah> ok, tôi nói 05:00 UTC chỉ vì tôi nói bừa thôi
19:19 < jeremiah> mids đâu rồi?
19:19 <@hezekiah> mids đã rời dự án một thời gian.
19:19 <@hezekiah> Bạn không có mặt ở mấy cuộc họp trước à?
19:19 < jeremiah> ok
19:19 < jeremiah> chắc là không
19:19 <@hezekiah> Chúng tôi đã có một kiểu tiệc chia tay như một phần của chương trình nghị sự.
19:19 < jeremiah> oh
19:20 <@hezekiah> OK ...
19:20 <@hezekiah> Vẫn còn gì trong chương trình nghị sự không?
19:20  * jrand0m không còn gì trong phần của mình
19:20 < jeremiah> về psyc:
19:20 < jeremiah> nếu đây là một tính năng của psyc, tôi nhớ bạn đã nhắc đến nó 	cách đây một thời gian
19:20  * hezekiah chưa từng có chương trình nghị sự ngay từ đầu
19:21 <@hezekiah> pace
19:21 <@hezekiah> place
19:21 < jeremiah> Tôi không nghĩ việc để mỗi người dùng gửi một tin nhắn tới mọi 	người dùng khác trong phòng là ý tưởng hay
19:21 <@hezekiah> Đó!
19:21 < jrand0m> jeremiah> vậy bạn sẽ để các pseudoserver dự phòng được chỉ định 	phân phối lại các tin nhắn?
19:21 < jrand0m> (pseudoservers = các nút trong kênh có danh sách 	người dùng)
19:21 < jeremiah> Tôi cũng không nghĩ 'broadcasting' là ý hay, nhưng nó

seems like it'll require a _lot_ of bandwith for a given user who may be on 	một modem, và với độ trễ khi gửi, ví dụ... 20 tin nhắn riêng lẻ sẽ 	làm hỏng cuộc trò chuyện
19:21 < jeremiah> Tôi không biết giải pháp tốt nhất là gì, có lẽ đó cũng là một cách
19:22 < jeremiah> Tôi nghĩ nhắn tin trực tiếp sẽ tốt nếu bạn muốn, 	nhưng có những trường hợp có lẽ không quan trọng đến thế
19:22 <@hezekiah> Tin nhắn sẽ cần được ký bằng 	khóa riêng của tác giả để đảm bảo tính xác thực.
19:22 <@hezekiah> Mặc dù vấn đề này còn lâu mới trở nên quan trọng, 	Tôi nghĩ jeremiah nói có lý
19:22 < jrand0m> hezekiah> điều đó đòi hỏi người dùng phải muốn giao tiếp có thể chứng minh được :)
19:23 < jrand0m> chắc chắn rồi.
19:23 <@hezekiah> Nếu tôi phải gửi một tin nhắn cho 100 người dùng trong một kênh ...
19:23 < jeremiah> mặc dù tin nhắn trung bình của tôi chỉ vài trăm byte, 	nên gửi nó cho hàng trăm người dùng có thể không quá khó
19:23 <@hezekiah> ... ừ thì, cuộc trò chuyện của tôi sẽ /rất/ chậm.
19:23 < jeremiah> đặc biệt nếu bạn không đợi phản hồi
19:23 <@hezekiah> 20K để gửi một tin nhắn.
19:23 <@hezekiah> Tôi không nghĩ vậy. :)
19:23 < jrand0m> ừ thì, nếu có 100 người dùng trong một kênh, *ai đó* sẽ phải 	gửi ra 100 tin nhắn
19:23 < jeremiah> là 20K à?
19:23 < jeremiah> ồ, đúng
19:23 <@hezekiah> 200 người dùng
19:24 < jeremiah> hmm
19:24 < jeremiah> chẳng phải các routers sẽ làm tốt việc đó sao?
19:24 < jeremiah> chúng ta có thể tạm an tâm giả định là chúng có băng thông kha khá, 	đúng không?
19:24 <@hezekiah> Tôi tưởng mỗi người đều có một 'router implementation'
19:24 < jrand0m> không hẳn.  nếu có các relay (nút chuyển tiếp), thì cơ chế chọn 	cần tính đến điều đó
19:24 < jrand0m> đúng vậy hezekiah
19:24 < jeremiah> tôi vẫn chưa đọc bản đặc tả
19:25 < jrand0m> một router là router cục bộ của bạn
19:25 <@hezekiah> Ugh!
19:25 <@hezekiah> Tôi vẫn đang lẫn lộn nick của các bạn!
19:25 <@hezekiah> lol
19:25 < jrand0m> hehe
19:25 <@hezekiah> Ờ ... nop đi đâu rồi?
19:25 <@hezekiah> Ồ.
19:26 <@hezekiah> Anh ấy vẫn ở đây.
19:26 <@hezekiah> Tôi tưởng anh ấy đi mất một lúc,
19:26 < jrand0m> nhưng jeremiah nói đúng, psyc có vài ý tưởng mà chúng ta có thể muốn 	cân nhắc, dù cũng có thể chúng ta sẽ bác bỏ chúng
19:26 <@hezekiah> Hãy khiến mạng chạy được trước đã.
19:26  * jrand0m nâng ly vì điều đó
19:26 <@hezekiah> Nếu bạn kéo tầm nhìn tới tận vạch đích, bạn sẽ vấp 	phải hòn đá cách bạn 3 inch ở phía trước.
19:27  * jeremiah cảm thấy được truyền cảm hứng
19:27 <@hezekiah> lol
19:27 < jrand0m> Tôi nghĩ sẽ thật tuyệt nếu chúng ta đặt mục tiêu xem lại 	bản đặc tả mạng trước tuần sau, gửi email đến iip-dev bất cứ khi nào ai đó 	có ý tưởng hoặc bình luận.  tôi có đang mất trí không?
19:27 <@hezekiah> nop? Bạn còn muốn bổ sung gì vào chương trình nghị sự không, 	hay chúng ta kết thúc?
19:27 <@hezekiah> jrand0m: Ừm, tôi không biết liệu tôi có thể đọc hết từng đó trước 	tuần sau không, nhưng tôi có thể thử. :)
19:27 < jrand0m> heh
19:28 < jrand0m> chỉ có 15 trang mệt mỏi ;)
19:28 <@hezekiah> 15 trang?
19:28 <@hezekiah> Trông giống 120 hơn!
19:29 < jrand0m> heh, ừ thì, còn tùy vào độ phân giải của bạn, tôi đoán vậy ;)
19:29 < jeremiah> anh ấy có nhiều anchor (liên kết neo) ở đó, làm nó trông 	có vẻ rất lớn
19:29 < jrand0m> hehe
19:29 <@hezekiah> Bên trái có NHIỀU hơn 15 liên kết, bạn ơi!
19:29 <@hezekiah> Thú nhận đi!
19:29 <@hezekiah> Nó nhiều hơn 15. :)
19:29 <@hezekiah> Ôi!
19:29 <@hezekiah> Đó không phải là trang! Chúng chỉ là anchor thôi!
19:29 <@hezekiah> Tôi được cứu rồi!
19:30  * hezekiah cảm thấy như một thủy thủ vừa được cứu khỏi chết đuối
19:30 < jeremiah> cả lớp lật sang tập 4 chương 2 Cấu trúc Byte của Thông điệp
19:30 < jrand0m> lol
19:30 <@hezekiah> lol
19:30 <@nop> kết thúc phiên họp
19:30 <@hezekiah> *baf*!
19:30 <@hezekiah> Tuần sau, 21:00 UTC, chỗ cũ.
19:30 <@hezekiah> Hẹn gặp mọi người ở đó. :)
19:30 < jeremiah> tạm biệt --- Đã đóng nhật ký Tue Jul 15 19:30:51 2003 </div>
