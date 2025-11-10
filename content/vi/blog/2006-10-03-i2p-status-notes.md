---
title: "Ghi chú trạng thái I2P ngày 2006-10-03"
date: 2006-10-03
author: "jr"
description: "Phân tích hiệu năng mạng, điều tra điểm nghẽn CPU, lập kế hoạch phát hành Syndie 1.0, và đánh giá hệ thống quản lý phiên bản phân tán"
categories: ["status"]
---

Chào mọi người, ghi chú tình hình tuần này đến muộn

* Index

1) Trạng thái mạng 2) Trạng thái phát triển router 3) Cơ sở lý luận của Syndie (tiếp theo) 4) Trạng thái phát triển Syndie 5) Hệ thống quản lý phiên bản phân tán 6) ???

* 1) Net status

Trong một hai tuần vừa qua, irc và các dịch vụ khác khá ổn định, tuy nhiên dev.i2p/squid.i2p/www.i2p/cvs.i2p đã gặp vài trục trặc (do các vấn đề tạm thời liên quan đến hệ điều hành). Hiện tại mọi thứ có vẻ đang ở trạng thái ổn định.

* 2) Router dev status

Mặt khác của cuộc thảo luận về Syndie là "vậy điều đó có ý nghĩa gì đối với router?", và để trả lời, tôi sẽ giải thích đôi chút về việc phát triển router đã tiến triển đến đâu vào lúc này.

Nhìn chung, theo quan điểm của tôi, điều đang kìm chân router khỏi phiên bản 1.0 là hiệu năng của nó, chứ không phải tính ẩn danh.

Chắc chắn vẫn còn những vấn đề về ẩn danh cần cải thiện, nhưng dù chúng ta đạt hiệu năng khá tốt đối với một mạng ẩn danh, hiệu năng đó vẫn chưa đủ để được sử dụng rộng rãi.

Ngoài ra, việc cải thiện tính ẩn danh của mạng sẽ không cải thiện hiệu năng của nó (trong hầu hết các trường hợp tôi có thể nghĩ tới, cải thiện ẩn danh làm giảm thông lượng và tăng độ trễ).

Chúng ta cần giải quyết các vấn đề về hiệu năng trước, vì nếu hiệu năng không đủ thì toàn bộ hệ thống cũng không đạt yêu cầu, bất kể các kỹ thuật ẩn danh của nó mạnh đến đâu.

Vậy điều gì đang kìm hãm hiệu năng của chúng ta? Kỳ lạ thay, có vẻ như đó là mức sử dụng CPU của chúng ta. Trước khi đi vào lý do chính xác, hãy điểm qua một chút bối cảnh trước.

 - to prevent partitioning attacks, we all need to plausibly build
   our tunnels from the same pool of routers.
 - to allow the tunnels to be of manageable length (and source
   routed), the routers in that pool must be directly reachable by
   anyone.
 - the bandwidth costs of receiving and rejecting tunnel join
   requests exceeds the capacity of dialup users on burst.

Vì vậy, chúng ta cần các tier (cấp) của routers - một số có thể truy cập toàn cầu với giới hạn băng thông cao (tier A), một số thì không (tier B). Điều này trên thực tế đã được triển khai thông qua thông tin về năng lực trong netDb, và tính đến khoảng một hai ngày trước, tỷ lệ giữa tier B so với tier A vào khoảng 3 trên 1 (93 routers thuộc cap L, M, N, hoặc O, và 278 thuộc cap K).

Hiện tại, về cơ bản có hai tài nguyên khan hiếm cần quản lý ở tier A - băng thông và CPU. Băng thông có thể được quản lý bằng các biện pháp thông thường (phân bổ tải trên một tập hợp lớn, để một số nút ngang hàng xử lý khối lượng cực lớn [ví dụ: những nút trên T3s], và từ chối hoặc giới hạn tốc độ các tunnel (đường hầm) và kết nối riêng lẻ).

Việc quản lý mức sử dụng CPU khó hơn. Nút thắt cổ chai CPU chính quan sát thấy trên các router cấp A là việc giải mã các yêu cầu xây dựng tunnel. Các router lớn có thể (và trên thực tế là) bị hoạt động này chiếm trọn tài nguyên - ví dụ, thời gian giải mã tunnel trung bình suốt vòng đời trên một trong các router của tôi là 225ms, và tần suất *trung bình* suốt vòng đời của việc giải mã yêu cầu tunnel là 254 sự kiện mỗi 60 giây, tức 4.2 mỗi giây. Chỉ cần nhân hai con số đó với nhau là thấy 95% CPU bị tiêu tốn chỉ bởi việc giải mã yêu cầu tunnel (và điều đó còn chưa tính đến các đột biến trong số lượng sự kiện). Router đó vẫn bằng cách nào đó tham gia đồng thời vào 4-6000 tunnel, chấp nhận khoảng 80% số yêu cầu đã giải mã.

Thật không may, vì CPU trên router đó bị tải nặng, nó buộc phải loại bỏ một số lượng đáng kể các yêu cầu xây dựng tunnel trước cả khi chúng kịp được giải mã (nếu không, các yêu cầu sẽ nằm trên hàng đợi quá lâu đến mức ngay cả khi được chấp nhận, bên yêu cầu ban đầu cũng sẽ coi chúng là đã mất hoặc quá tải đến mức không làm được gì). Trong bối cảnh đó, tỷ lệ chấp nhận 80% của router trông tệ hơn nhiều - trong suốt vòng đời của nó, router đã giải mã khoảng 250k yêu cầu (tức là khoảng 200k được chấp nhận), nhưng nó đã phải loại bỏ khoảng 430k yêu cầu trong hàng đợi giải mã do quá tải CPU (biến tỷ lệ chấp nhận 80% đó thành 30%).

Các giải pháp có vẻ đi theo hướng giảm chi phí CPU liên quan cho việc giải mã các yêu cầu tunnel. Nếu chúng ta giảm thời gian CPU khoảng một bậc độ lớn, điều đó sẽ tăng đáng kể công suất của router hạng A, từ đó giảm các trường hợp từ chối (cả tường minh lẫn ngầm, do các yêu cầu bị loại bỏ). Điều này đến lượt nó sẽ làm tăng tỷ lệ xây dựng tunnel thành công, qua đó giảm tần suất lease (mục nhập có thời hạn trong leaseSet) hết hạn, và như vậy sẽ giảm tải băng thông lên mạng do phải xây dựng lại tunnel.

Một phương án để làm điều này là đổi các yêu cầu xây dựng tunnel từ dùng Elgamal 2048bit sang, ví dụ, 1024bit hoặc 768bit. Vấn đề ở đây là nếu bạn phá được lớp mã hóa của một thông điệp yêu cầu xây dựng tunnel, bạn sẽ biết toàn bộ đường đi của tunnel. Ngay cả nếu chúng ta chọn cách này, chúng ta được lợi bao nhiêu? Một cải thiện theo một bậc độ lớn về thời gian giải mã có thể bị xóa sạch bởi một sự gia tăng theo một bậc độ lớn trong tỉ lệ tier B so với tier A (còn gọi là vấn đề kẻ ăn theo (freeriders)), và khi đó chúng ta sẽ bị kẹt, vì không đời nào chúng ta có thể chuyển sang Elgamal 512bit hoặc 256bit (và vẫn dám nhìn mình trong gương ;)

Một phương án thay thế là sử dụng mật mã yếu hơn nhưng bỏ cơ chế bảo vệ chống các cuộc tấn công đếm gói mà chúng tôi đã bổ sung trong quy trình xây dựng tunnel mới. Điều đó sẽ cho phép chúng tôi sử dụng các khóa thỏa thuận hoàn toàn tạm thời (ephemeral) trong một tunnel dạng telescopic (mở rộng từng bước) giống Tor (mặc dù, một lần nữa, điều đó sẽ khiến người tạo tunnel bị lộ trước các cuộc tấn công đếm gói thụ động rất đơn giản có thể nhận diện một dịch vụ).

Một ý tưởng khác là công bố và sử dụng thông tin về mức tải tường minh hơn trong netDb, cho phép các client phát hiện chính xác hơn các tình huống như ví dụ ở trên, nơi một router băng thông cao loại bỏ 60% các thông điệp yêu cầu tunnel của nó mà thậm chí không cần xem xét. Có một vài thử nghiệm đáng để thực hiện theo hướng này, và chúng có thể được tiến hành với khả năng tương thích ngược hoàn toàn, vì vậy chúng ta có thể sẽ sớm thấy chúng.

Vậy, đó là điểm nghẽn trong router/mạng theo như tôi thấy hiện nay. Mọi đề xuất về cách chúng ta có thể giải quyết nó đều rất được trân trọng.

* 3) Syndie rationale continued

Có một bài viết chuyên sâu trên diễn đàn về Syndie và vai trò của nó trong bức tranh chung - hãy xem tại <http://forum.i2p.net/viewtopic.php?t=1910>

Ngoài ra, tôi chỉ muốn nêu bật hai đoạn trích từ các tài liệu Syndie đang được soạn thảo. Trước hết, từ irc (và phần FAQ chưa được công bố):

<bar> một câu hỏi tôi vẫn băn khoăn là, sau này ai sẽ có        đủ gan để vận hành máy chủ/kho lưu trữ syndie cho môi trường sản xuất?  <bar> chẳng phải những thứ đó cũng sẽ dễ bị lần ra như eepsites(I2P Sites)        hiện nay sao?  <jrandom> các kho lưu trữ syndie công khai không có khả năng        *đọc* nội dung được đăng lên các diễn đàn, trừ khi các diễn đàn công bố        các khóa để làm điều đó  <jrandom> và xem đoạn thứ hai của usecases.html  <jrandom> dĩ nhiên, những bên vận hành các kho lưu trữ nếu nhận        lệnh hợp pháp yêu cầu gỡ một diễn đàn thì có lẽ sẽ làm theo  <jrandom> (nhưng khi đó mọi người có thể chuyển sang một        kho lưu trữ khác, mà không làm gián đoạn hoạt động của diễn đàn)  <void> ừ, bạn nên nhắc đến thực tế rằng việc chuyển sang một        medium (phương tiện) khác sẽ diễn ra trơn tru  <bar> nếu kho lưu trữ của tôi ngừng hoạt động, tôi có thể tải toàn bộ diễn đàn của mình lên một        cái mới, đúng không?  <jrandom> 'chính xác đó, bar  <void> họ có thể dùng hai phương thức cùng lúc trong quá trình chuyển đổi  <void> và bất kỳ ai cũng có thể đồng bộ các mediums  <jrandom> đúng rồi, void

Phần có liên quan trong (chưa được xuất bản) Syndie usecases.html là:

Mặc dù nhiều nhóm khác nhau thường muốn tổ chức các cuộc thảo luận trên một diễn đàn trực tuyến, bản chất tập trung của các diễn đàn truyền thống (website, BBS, v.v.) có thể là một vấn đề. Chẳng hạn, trang web lưu trữ diễn đàn có thể bị ngừng hoạt động bởi các cuộc tấn công từ chối dịch vụ hoặc bởi biện pháp hành chính. Ngoài ra, máy chủ duy nhất tạo ra một điểm thuận tiện để giám sát hoạt động của nhóm, đến mức ngay cả khi một diễn đàn dùng bút danh, các bút danh đó vẫn có thể bị liên kết với địa chỉ IP được dùng để đăng hoặc đọc từng bài viết.

Ngoài ra, không chỉ các diễn đàn là phi tập trung, chúng còn được tổ chức theo cách ad-hoc (tự phát) nhưng vẫn hoàn toàn tương thích với các phương thức tổ chức khác. Điều này có nghĩa là một nhóm nhỏ người
  có thể vận hành diễn đàn của họ bằng một phương thức (phân phối thông điệp bằng cách dán chúng lên một trang wiki),
  trong khi một nhóm khác có thể vận hành diễn đàn của họ bằng
  một phương thức khác (đăng thông điệp của họ vào một bảng băm phân tán
  như OpenDHT, tuy nhiên, nếu có một người biết cả hai phương thức,
  người đó có thể đồng bộ hai diễn đàn lại với nhau. Điều này cho phép
  những người chỉ biết đến trang wiki trò chuyện với những người
  chỉ biết đến dịch vụ OpenDHT mà không cần biết gì về nhau.
  Mở rộng hơn nữa, Syndie cho phép các cell (nhóm nhỏ)
  kiểm soát mức độ công khai của riêng họ trong khi giao tiếp trên toàn bộ
  tổ chức.

* 4) Syndie dev status

Gần đây Syndie đã có rất nhiều tiến triển, với 7 bản phát hành alpha được phát cho mọi người trên kênh IRC. Hầu hết các vấn đề lớn trong giao diện scriptable (có thể lập trình bằng script) đã được xử lý, và tôi hy vọng chúng ta có thể phát hành Syndie 1.0 vào cuối tháng này.

Tôi vừa nói "1.0" ư? Chắc chắn rồi! Mặc dù Syndie 1.0 sẽ là một ứng dụng dựa trên văn bản và thậm chí còn không thể so sánh về mức độ dễ sử dụng với các ứng dụng dựa trên văn bản tương tự khác (chẳng hạn như mutt hoặc tin), nó vẫn sẽ cung cấp đầy đủ chức năng, cho phép các chiến lược syndication (phân phối nội dung) dựa trên HTTP và tệp, và hy vọng sẽ cho các nhà phát triển tiềm năng thấy được các khả năng của Syndie.

Hiện tại, tôi đang tạm dự kiến phát hành Syndie 1.1 (cho phép mọi người tổ chức kho lưu trữ và thói quen đọc tốt hơn) và có thể là bản 1.2 để tích hợp một số chức năng tìm kiếm (cả tìm kiếm đơn giản và có thể là tìm kiếm toàn văn của lucene). Syndie 2.0 có lẽ sẽ là bản phát hành GUI (giao diện đồ họa người dùng) đầu tiên, với browser plugin (tiện ích mở rộng của trình duyệt) sẽ ra cùng phiên bản 3.0. Hỗ trợ cho các kho lưu trữ bổ sung và các mạng phân phối thông điệp sẽ xuất hiện khi được triển khai, dĩ nhiên (freenet, mixminion/mixmaster/smtp, opendht, gnutella, v.v.).

Tuy vậy, tôi nhận ra rằng Syndie 1.0 sẽ không phải là cú hích làm chấn động như một số người mong muốn, vì các ứng dụng thuần văn bản thực sự dành cho dân kỹ thuật, nhưng tôi muốn cố gắng giúp chúng ta bỏ thói quen xem "1.0" là bản phát hành kết thúc và thay vào đó coi đó là một sự khởi đầu.

* 5) Distributed version control

Cho đến giờ, tôi đã mày mò dùng subversion làm vcs (hệ thống quản lý phiên bản) cho Syndie, dù tôi chỉ thực sự thông thạo CVS và clearcase. Nguyên do là tôi hầu như lúc nào cũng offline, và ngay cả khi online thì kết nối dialup rất chậm, nên các thao tác diff/revert/etc cục bộ của subversion tỏ ra khá hữu ích. Tuy nhiên, hôm qua void đã gợi ý rằng chúng ta nên tìm hiểu một trong các hệ thống phân tán thay vào đó.

Tôi đã xem qua chúng vài năm trước, khi đánh giá một vcs (hệ thống kiểm soát phiên bản) cho I2P, nhưng tôi đã bỏ qua vì tôi không cần chức năng hoạt động ngoại tuyến của chúng (lúc đó tôi có kết nối mạng tốt), nên việc học chúng không đáng công. Giờ thì không còn như vậy nữa, nên tôi đang xem xét chúng kỹ hơn một chút.

- From what I can see, darcs, monotone, and codeville are the top

các ứng viên, và vcs (hệ thống kiểm soát phiên bản) dựa trên patch của darcs có vẻ đặc biệt hấp dẫn. Ví dụ, tôi có thể làm tất cả công việc của mình cục bộ và chỉ việc scp các diff (tệp khác biệt) gzip'ed & gpg'ed lên một thư mục Apache trên dev.i2p.net, và mọi người có thể đóng góp những thay đổi của riêng họ bằng cách đăng các diff gzip'ed và gpg'ed của họ đến các địa điểm họ lựa chọn. Khi đến lúc gắn thẻ một bản phát hành, tôi sẽ tạo một darcs diff xác định tập hợp các bản vá có trong bản phát hành và đẩy bản diff .gz'ed/.gpg'ed đó lên như những cái khác (đồng thời phát hành cả các tệp tar.bz2, .exe, và .zip thực sự, dĩ nhiên ;)

Và, như một điểm đặc biệt thú vị, các bản diff đã được gzip/gpg có thể được đăng làm tệp đính kèm trong các thông điệp Syndie, cho phép Syndie tự lưu trữ.

Có ai có kinh nghiệm với mấy thứ này không? Có lời khuyên nào không?

* 6) ???

Chỉ 24 màn hình đầy chữ lần này (kể cả bài trên diễn đàn) ;) Rất tiếc tôi đã không tham dự được cuộc họp, nhưng như mọi khi, tôi rất muốn nghe ý kiến hay đề xuất của bạn - chỉ cần đăng lên danh sách thư, diễn đàn, hoặc ghé qua IRC.

=jr
