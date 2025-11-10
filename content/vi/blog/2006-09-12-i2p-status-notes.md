---
title: "Ghi chú trạng thái I2P cho ngày 2006-09-12"
date: 2006-09-12
author: "jr"
description: "Bản phát hành 0.6.1.25 với các cải thiện về độ ổn định mạng, tối ưu hóa I2PSnark, và thiết kế lại toàn diện Syndie với các diễn đàn phân tán ngoại tuyến"
categories: ["status"]
---

Chào mọi người, đây là ghi chú tình hình *khụ* hàng tuần của chúng tôi

* Index:

1) 0.6.1.25 và trạng thái mạng 2) I2PSnark 3) Syndie (là gì/tại sao/khi nào) 4) Các câu hỏi về mật mã của Syndie 5) ???

* 1) 0.6.1.25 and net status

Mới đây chúng tôi đã phát hành phiên bản 0.6.1.25, bao gồm hàng loạt bản sửa lỗi tích lũy trong tháng qua, cùng với công việc của zzz trên I2PSnark và nỗ lực của Complication nhằm làm cho mã đồng bộ thời gian của chúng tôi mạnh mẽ hơn một chút. Hiện tại mạng có vẻ khá ổn định, mặc dù IRC đã hơi trục trặc trong vài ngày vừa qua (do các nguyên nhân không liên quan đến I2P). Có lẽ khoảng một nửa mạng đã được nâng cấp lên bản phát hành mới nhất, tỷ lệ xây dựng tunnel thành công không thay đổi nhiều, mặc dù thông lượng tổng thể có vẻ đã tăng (có lẽ do số người dùng I2PSnark tăng).

* 2) I2PSnark

Các cập nhật của zzz cho I2PSnark bao gồm tối ưu hóa giao thức cũng như các thay đổi đối với giao diện web, như được mô tả trong nhật ký lịch sử [1]. Cũng đã có một vài cập nhật nhỏ cho I2PSnark kể từ bản phát hành 0.6.1.25, và có lẽ zzz có thể cho chúng ta một cái nhìn tổng quan về những gì đang diễn ra trong cuộc họp tối nay.

[1] <http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/history.txt?rev=HEAD>

* 3) Syndie

Như mọi người đều biết, tôi đã dành thời gian tập trung vào việc đại tu Syndie, dù “revamp” có lẽ không phải là từ chính xác. Có lẽ bạn có thể coi những gì hiện đang được triển khai là một “proof of concept” (mô hình chứng minh ý tưởng), vì Syndie mới đã được thiết kế lại và hiện thực lại từ đầu, dù nhiều khái niệm vẫn được giữ nguyên. Khi tôi nhắc đến Syndie bên dưới, tôi đang nói về Syndie mới.

* 3.1) What is Syndie

Ở mức cơ bản nhất, Syndie là một hệ thống để vận hành các diễn đàn phân tán ngoại tuyến. Mặc dù cấu trúc của nó dẫn đến nhiều cấu hình khác nhau, hầu hết nhu cầu sẽ được đáp ứng bằng cách chọn một tùy chọn từ mỗi tiêu chí trong ba tiêu chí sau:  - Các kiểu diễn đàn:    - Một tác giả (blog điển hình)    - Nhiều tác giả (blog nhiều tác giả)**    - Mở (nhóm tin, tuy nhiên có thể áp dụng các hạn chế để chỉ      những người dùng được ủy quyền** mới có thể đăng chủ đề mới, trong khi bất kỳ ai cũng có thể bình luận trên      những chủ đề mới đó)  - Mức độ hiển thị:    - Bất kỳ ai cũng có thể đọc mọi thứ    - Chỉ những người được ủy quyền* mới có thể đọc bài viết, nhưng một số siêu dữ liệu vẫn được hiển thị    - Chỉ những người được ủy quyền* mới có thể đọc bài viết, thậm chí mới biết ai đang đăng    - Chỉ những người được ủy quyền* mới có thể đọc bài viết, và không ai biết ai đang      đăng  - Bình luận/phản hồi:    - Bất kỳ ai cũng có thể bình luận hoặc gửi phản hồi riêng tư cho tác giả/chủ sở hữu      diễn đàn    - Chỉ những người được ủy quyền** mới có thể bình luận, và bất kỳ ai cũng có thể gửi phản hồi      riêng tư    - Không ai có thể bình luận, nhưng bất kỳ ai cũng có thể gửi phản hồi riêng tư    - Không ai có thể bình luận, và không ai có thể gửi phản hồi riêng tư

 * reading is authorized by giving people the symmetric key or passphrase
   to decrypt the post.  Alternately, the post may include a publicly
   visible prompt, where the correct answer serves to generate the
   correct decryption key.

** việc đăng bài, cập nhật và/hoặc bình luận được ủy quyền bằng cách cung cấp cho những người dùng đó các khóa riêng bất đối xứng để họ ký các bài viết, trong đó khóa công khai tương ứng được đưa vào siêu dữ liệu của diễn đàn như là được ủy quyền đăng, quản lý hoặc bình luận trên diễn đàn. Ngoài ra, các khóa công khai dùng để ký của từng người dùng được ủy quyền có thể được liệt kê trong medtata.

Các bài viết riêng lẻ có thể bao gồm nhiều thành phần khác nhau:  - Bất kỳ số lượng trang nào, kèm theo dữ liệu out of band (dữ liệu ngoài kênh) cho từng trang để chỉ định
    loại nội dung, ngôn ngữ, v.v.  Có thể dùng bất kỳ kiểu định dạng nào, vì
    việc hiển thị nội dung an toàn là do ứng dụng khách quyết định - văn bản thuần
    phải được hỗ trợ, và các ứng dụng khách có thể thì nên hỗ trợ HTML.
  - Bất kỳ số lượng tệp đính kèm nào (cũng kèm dữ liệu out of band mô tả
    tệp đính kèm)
  - Một ảnh đại diện nhỏ cho bài viết (nhưng nếu không chỉ định, sẽ dùng
    ảnh đại diện mặc định của tác giả)
  - Một tập hợp các tham chiếu đến các bài viết khác, diễn đàn, kho lưu trữ, URLs, v.v. (có thể
    bao gồm các khóa cần thiết để đăng, quản lý hoặc đọc các diễn đàn được
    tham chiếu)

Nhìn chung, Syndie hoạt động ở *tầng nội dung* - các bài viết riêng lẻ được đóng gói trong các tệp zip được mã hóa, và việc tham gia diễn đàn chỉ đơn giản là chia sẻ những tệp này. Không có sự phụ thuộc vào cách các tệp được chuyển giao (qua I2P, Tor, Freenet, gnutella, bittorrent, RSS, usenet, email), nhưng các công cụ tổng hợp và phân phối đơn giản sẽ được đóng gói kèm theo bản phát hành Syndie tiêu chuẩn.

Tương tác với nội dung Syndie sẽ diễn ra theo một vài cách. Trước hết, có một giao diện dựa trên văn bản có thể lập trình (scriptable), cho phép sử dụng ở chế độ dòng lệnh cơ bản và chế độ tương tác để đọc từ, ghi vào, quản lý và đồng bộ hóa các diễn đàn. Ví dụ, sau đây là một tập lệnh đơn giản để tạo một bài đăng "thông điệp trong ngày" mới -

login     menu post     create --channel 0000000000000000000000000000000000000000     addpage --in /etc/motd --content-type text/plain     addattachment --in ~/webcam.png --content-type image/png     listauthkeys --authorizedOnly true     authenticate 0     authorize 0     set --subject "Today's MOTD"     set --publicTags motd     execute     exit

Chỉ cần pipe (kết nối qua ống lệnh) nó qua tệp thực thi syndie và thế là xong: cat motd-script | ./syndie > syndie.log

Ngoài ra, hiện đang phát triển một giao diện đồ họa cho Syndie, bao gồm khả năng hiển thị an toàn văn bản thuần và các trang HTML (tất nhiên, có hỗ trợ tích hợp trong suốt với các tính năng của Syndie).

Các ứng dụng dựa trên mã "sucker" cũ của Syndie sẽ cho phép quét và viết lại các trang web và website thông thường để chúng có thể được sử dụng như các bài đăng Syndie một trang hoặc nhiều trang, bao gồm cả hình ảnh và các tài nguyên khác dưới dạng tệp đính kèm.

Trong tương lai, các plugin firefox/mozilla dự kiến sẽ vừa phát hiện và nhập các tệp theo định dạng Syndie và các tham chiếu Syndie, đồng thời thông báo cho Syndie GUI cục bộ rằng một diễn đàn, chủ đề, thẻ, tác giả hoặc kết quả tìm kiếm cụ thể cần được tập trung hiển thị.

Dĩ nhiên, vì Syndie, về cốt lõi, là một lớp nội dung với định dạng tệp và các thuật toán mật mã được xác định, nên theo thời gian có lẽ sẽ xuất hiện các ứng dụng khác hoặc các bản triển khai thay thế.

* 3.2) Why does Syndie matter?

Trong vài tháng qua, tôi đã nghe một số người hỏi tại sao tôi lại đang phát triển một công cụ diễn đàn/blog - điều đó có liên quan gì đến việc cung cấp tính ẩn danh mạnh?

Câu trả lời: *mọi thứ*.

Tóm tắt ngắn gọn:  - Thiết kế của Syndie, với tư cách là một ứng dụng khách coi trọng tính ẩn danh, cẩn trọng    tránh các vấn đề nhạy cảm dữ liệu phức tạp mà gần như mọi    ứng dụng không được thiết kế với mục tiêu ẩn danh đều không tránh khỏi.  - Bằng cách hoạt động ở lớp nội dung, Syndie không phụ thuộc vào    hiệu năng hoặc độ tin cậy của các mạng phân tán như I2P, Tor, hoặc    Freenet, dù khi phù hợp vẫn có thể tận dụng chúng.  - Bằng cách đó, nó có thể hoạt động trọn vẹn với các cơ chế nhỏ, ad‑hoc cho    phân phối nội dung - những cơ chế có thể không đáng để bỏ công    cho các đối thủ hùng mạnh đối phó (vì 'lợi ích' của việc bắt    chỉ vài chục người nhiều khả năng sẽ vượt quá chi phí    triển khai các cuộc tấn công)  - Điều này ngụ ý rằng Syndie vẫn hữu ích ngay cả khi không có vài triệu    người sử dụng nó - các nhóm nhỏ không liên quan nên tự thiết lập sơ đồ phân phối Syndie riêng tư của    riêng họ mà không cần bất kỳ    tương tác nào với, hay thậm chí bị các nhóm khác biết đến.  - Vì Syndie không phụ thuộc vào tương tác thời gian thực, nó thậm chí    có thể tận dụng các hệ thống và kỹ thuật ẩn danh có độ trễ cao để tránh    những kiểu tấn công mà mọi hệ thống có độ trễ thấp đều dễ bị tổn thương (chẳng hạn như    các cuộc tấn công giao cắt thụ động, tấn công định thời thụ động và chủ động, và    tấn công pha trộn chủ động).

Nhìn chung, theo quan điểm của tôi, Syndie thậm chí còn quan trọng đối với sứ mệnh cốt lõi của I2P (cung cấp tính ẩn danh mạnh mẽ cho những ai cần đến nó) hơn cả router. Nó không phải là thuốc chữa bách bệnh, nhưng là một bước then chốt.

* 3.3) When can we use Syndie?

Mặc dù rất nhiều công việc đã được hoàn thành (bao gồm gần như toàn bộ giao diện dạng văn bản và một phần lớn của GUI (giao diện đồ họa)), vẫn còn công việc phải làm. Bản phát hành Syndie đầu tiên sẽ bao gồm các chức năng cơ bản sau:

 - Scriptable text interface, packaged up as a typical java application,
   or buildable with a modern GCJ
 - Support for all forum types, replies, comments, etc.
 - Manual syndication, transferring .snd files.
 - HTTP syndication, including simple CGI scripts to operate archives,
   controllable through the text interface.
 - Specs for the file formats, encryption algorithms, and database
   schema.

Tiêu chí tôi dùng để phát hành sẽ là "đầy đủ chức năng". Người dùng phổ thông sẽ không muốn mày mò với một ứng dụng dựa trên văn bản, nhưng tôi hy vọng một số dân kỹ thuật sẽ làm.

Các phiên bản phát hành tiếp theo sẽ nâng cao khả năng của Syndie trên nhiều phương diện:  - Giao diện người dùng:   - GUI dựa trên SWT   - Plugin trình duyệt web   - Giao diện văn bản kiểu quét web (lấy về và viết lại các trang)   - Giao diện đọc IMAP/POP3/NNTP  - Hỗ trợ nội dung   - Văn bản thuần   - HTML (kết xuất an toàn trong GUI, không trong trình duyệt)   - BBCode (?)  - Phân phối nội dung   - Feedspace, Feedtree, và các công cụ đồng bộ hóa độ trễ thấp khác   - Freenet (lưu các tệp .snd tại CHK@s và các kho lưu trữ tham chiếu
     đến các tệp .snd tại SSK@s và USK@s)   - Email (gửi qua SMTP/mixmaster/mixminion, đọc qua
     procmail/v.v.)   - Usenet (gửi qua NNTP hoặc các remailer, đọc qua (qua proxy)
     NNTP)  - Tìm kiếm toàn văn với tích hợp Lucene  - Mở rộng HSQLDB để mã hóa toàn bộ cơ sở dữ liệu  - Các phương pháp heuristic bổ sung cho quản lý kho lưu trữ

Cái gì được xuất ra vào lúc nào phụ thuộc vào thời điểm các việc được thực hiện.

* 4) Open questions for Syndie

Hiện tại, Syndie đã được triển khai với các nguyên thủy mật mã tiêu chuẩn của I2P - SHA256, AES256/CBC, ElGamal2048, DSA. Tuy nhiên, thuật toán cuối cùng là ngoại lệ, vì nó sử dụng khóa công khai 1024bit và phụ thuộc vào SHA1 (đang suy yếu nhanh chóng). Một đề xuất tôi nghe từ thực tế triển khai là tăng cường DSA bằng SHA256, và dù điều đó có thể thực hiện được (dù chưa được chuẩn hóa), nó chỉ cung cấp khóa công khai 1024bit.

Vì Syndie vẫn chưa được phát hành công khai và không phải lo về khả năng tương thích ngược, chúng ta có thể thoải mái hoán đổi các nguyên thủy mật mã. Một hướng tiếp cận là chọn chữ ký ElGamal2048 hoặc RSA2048 thay cho DSA, trong khi một hướng khác là hướng tới ECC (mật mã đường cong elliptic), với chữ ký ECDSA và mã hóa bất đối xứng ECIES, có thể ở các mức bảo mật 256bit hoặc 521bit (tương ứng với kích thước khóa đối xứng 128bit và 256bit).

Về các vấn đề bằng sáng chế liên quan đến ECC (mật mã đường cong elliptic), có vẻ chúng chỉ liên quan đến một số tối ưu hóa cụ thể (nén điểm) và các thuật toán mà chúng tôi không cần (EC MQV). Về hỗ trợ Java thì hiện không có nhiều, dù thư viện bouncycastle dường như có một số mã. Tuy nhiên, có lẽ sẽ không quá khó để thêm các wrapper (trình bao bọc) nhỏ cho libtomcrypt, openssl, hoặc crypto++ nữa, giống như chúng tôi đã làm với libGMP (tạo ra jbigi).

Bạn có ý kiến gì về việc đó không?

* 5) ???

Có khá nhiều nội dung ở trên cần tiếp thu, đó là lý do (theo gợi ý của cervantes) tôi gửi những ghi chú tình hình này sớm như vậy. Nếu bạn có bất kỳ bình luận, câu hỏi, mối bận tâm hay đề xuất nào, hãy ghé qua #i2p tối nay lúc 8pm UTC trên irc.freenode.net/irc.postman.i2p/irc.freshcoffee.i2p cho buổi họp *khụ* hàng tuần của chúng ta!

=jr
