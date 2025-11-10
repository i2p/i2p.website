---
title: "Ghi chú trạng thái I2P cho ngày 2004-08-24"
date: 2004-08-24
author: "jr"
description: "Cập nhật tình hình I2P hàng tuần bao gồm phát hành 0.3.4.3, các tính năng mới của bảng điều khiển router, tiến độ phiên bản 0.4, và nhiều cải tiến khác"
categories: ["status"]
---

Chào mọi người, hôm nay có rất nhiều cập nhật

## Chỉ mục

1. 0.3.4.3 status
   1.1) timestamper
   1.2) new router console authentication
2. 0.4 status
   2.1) service & systray integration
   2.2) jbigi & jcpuid
   2.3) i2paddresshelper
3. AMOC vs. restricted routes
4. stasher
5. pages of note
6. ???

## 1) 0.3.4.3 trạng thái

Bản phát hành 0.3.4.3 ra mắt vào thứ Sáu tuần trước và mọi thứ diễn ra khá tốt kể từ đó. Đã có một số vấn đề với phần mã kiểm thử tunnel và lựa chọn peer (nút ngang hàng) vừa được đưa vào, nhưng sau một vài tinh chỉnh kể từ khi phát hành, nó khá ổn định. Tôi không biết máy chủ IRC đã lên bản sửa đổi mới chưa, nên nhìn chung chúng tôi phải dựa vào việc kiểm thử với eepsites(I2P Sites) và các http outproxies (squid.i2p và www1.squid.i2p). Việc truyền tệp lớn (>5MB) trong bản phát hành 0.3.4.3 vẫn chưa đủ tin cậy, nhưng trong thử nghiệm của tôi, các sửa đổi kể từ đó đã cải thiện mọi thứ hơn nữa.

Mạng cũng đang tăng trưởng — chúng tôi đã đạt 45 người dùng đồng thời vào đầu ngày hôm nay, và đã ổn định trong khoảng 38–44 người dùng trong vài ngày qua (w00t)! Đây là một con số lành mạnh vào thời điểm này, và tôi đã theo dõi hoạt động tổng thể của mạng để đề phòng rủi ro. Khi chuyển sang bản phát hành 0.4, chúng tôi sẽ muốn tăng dần quy mô người dùng lên đến mốc khoảng 100 router và kiểm thử thêm trước khi mở rộng tiếp. Ít nhất thì đó là mục tiêu của tôi từ góc nhìn của một nhà phát triển.

### 1.1) timestamper

Một trong những điều cực kỳ tuyệt vời đã thay đổi trong bản phát hành 0.3.4.3 mà tôi hoàn toàn quên đề cập là bản cập nhật cho mã SNTP. Nhờ sự hào phóng của Adam Buckley, người đã đồng ý phát hành mã SNTP của mình theo giấy phép BSD, chúng tôi đã hợp nhất ứng dụng Timestamper cũ vào I2P SDK lõi và tích hợp nó hoàn toàn với đồng hồ của chúng tôi. Điều này có nghĩa là ba điều: 1. bạn có thể xóa timestamper.jar (mã hiện nằm trong i2p.jar) 2. bạn có thể gỡ bỏ các dòng clientApp liên quan khỏi cấu hình của mình 3. bạn có thể cập nhật cấu hình để sử dụng các tùy chọn đồng bộ thời gian mới

Các tùy chọn mới trong router.config khá đơn giản, và các giá trị mặc định nên là đủ tốt (điều này đặc biệt đúng vì đa số các bạn đang vô tình sử dụng chúng :)

Để thiết lập danh sách các máy chủ SNTP để truy vấn:

```
time.sntpServerList=pool.ntp.org,pool.ntp.org,pool.ntp.org
```
Để vô hiệu hóa đồng bộ hóa thời gian (chỉ khi bạn là một chuyên gia NTP và biết rằng đồng hồ của hệ điều hành của bạn *luôn luôn* đúng - chạy "windows time" là KHÔNG đủ):

```
time.disabled=true
```
Bạn không cần phải có 'timestamper password' nữa, vì mọi thứ đã được tích hợp trực tiếp vào mã nguồn (à, những niềm vui của BSD vs GPL :)

### 1.2) new router console authentication

Điều này chỉ liên quan đến những ai đang chạy bảng điều khiển router mới, nhưng nếu bạn để nó lắng nghe trên một giao diện mạng công khai, bạn có thể muốn tận dụng cơ chế xác thực HTTP cơ bản được tích hợp sẵn. Đúng là xác thực HTTP cơ bản yếu đến mức buồn cười - nó sẽ không bảo vệ bạn trước bất kỳ ai nghe lén mạng của bạn hoặc dùng tấn công vét cạn để xâm nhập, nhưng nó vẫn đủ để ngăn những kẻ rình mò tình cờ. Dù sao, để sử dụng nó, chỉ cần thêm dòng

```
consolePassword=blah
```
vào router.config của bạn. Đáng tiếc là bạn sẽ phải khởi động lại router, vì tham số này chỉ được nạp vào Jetty một lần (khi khởi động).

## 2) 0.4 status

Chúng tôi đang đạt được nhiều tiến bộ với bản phát hành 0.4 và hy vọng sẽ phát hành một vài bản tiền phát hành trong tuần tới. Tuy nhiên, chúng tôi vẫn đang hoàn thiện một số chi tiết nên hiện vẫn chưa có quy trình nâng cấp hoàn chỉnh. Bản phát hành sẽ tương thích ngược, vì vậy việc cập nhật sẽ không quá khó khăn. Dù sao, hãy chú ý theo dõi và bạn sẽ biết khi mọi thứ sẵn sàng.

### 1.1) trình đóng dấu thời gian

Hypercubus đang đạt được nhiều tiến bộ trong việc tích hợp trình cài đặt, một ứng dụng systray (khay hệ thống), và một số mã quản lý dịch vụ. Về cơ bản, đối với bản phát hành 0.4, tất cả người dùng Windows sẽ tự động có một biểu tượng systray nhỏ (Iggy!), dù họ có thể vô hiệu hóa (và/hoặc bật lại) nó thông qua bảng điều khiển web. Ngoài ra, chúng tôi sẽ đóng gói kèm JavaService wrapper (trình bao JavaService), mà sẽ cho phép chúng tôi làm đủ thứ hay ho, chẳng hạn như chạy I2P khi khởi động hệ thống (hoặc không), tự động khởi động lại khi thỏa một số điều kiện, khởi động lại JVM cưỡng bức theo yêu cầu, tạo dấu vết ngăn xếp, và đủ loại tiện ích khác.

### 1.2) Xác thực mới cho bảng điều khiển router

Một trong những cập nhật lớn trong bản phát hành 0.4 sẽ là đại tu mã jbigi, hợp nhất các chỉnh sửa Iakin đã thực hiện cho Freenet cũng như thư viện native "jcpuid" mới (thư viện nhị phân gốc). Thư viện jcpuid chỉ hoạt động trên các kiến trúc x86 và, phối hợp với một số mã jbigi mới, sẽ xác định jbigi 'đúng' để nạp. Do đó, chúng tôi sẽ phân phối một jbigi.jar duy nhất mà mọi người đều sẽ có, và từ đó chọn ra bản 'đúng' cho máy hiện tại. Dĩ nhiên, mọi người vẫn có thể tự biên dịch jbigi native của riêng mình, ghi đè lựa chọn của jcpuid (chỉ cần biên dịch và sao chép nó vào thư mục cài đặt I2P của bạn, hoặc đặt tên nó là "jbigi" và đặt nó trong một tệp .jar trong classpath (đường dẫn lớp của Java) của bạn). Tuy nhiên, do các cập nhật, nó *không* tương thích ngược - khi nâng cấp, bạn phải hoặc là biên dịch lại jbigi của riêng mình hoặc gỡ bỏ thư viện native hiện có (để mã jcpuid mới chọn bản đúng).

### 2.3) i2paddresshelper

oOo đã tạo ra một tiện ích rất hay để cho phép mọi người duyệt eepsites(các trang I2P) mà không cần cập nhật hosts.txt của họ. Nó đã được commit vào CVS và sẽ được triển khai trong bản phát hành tiếp theo, nhưng mọi người có thể muốn cân nhắc cập nhật các liên kết cho phù hợp (cervantes đã cập nhật bbcode [i2p] của forum.i2p để hỗ trợ nó với một liên kết "Try it [i2p]").

Về cơ bản bạn chỉ cần tạo một liên kết tới eepsite(trang I2P) với bất kỳ tên nào bạn muốn, sau đó thêm một tham số url đặc biệt để chỉ định đích đến:

```
http://wowthisiscool.i2p/?i2paddresshelper=FpCkYW5pw...
```
Ở phía hậu trường, nó khá an toàn - bạn không thể giả mạo một địa chỉ khác, và tên đó *không* được lưu trong hosts.txt, nhưng nó sẽ cho phép bạn xem các hình ảnh / v.v. được liên kết trên eepsites(I2P Sites) mà bạn sẽ không thể làm được bằng mẹo cũ `http://i2p/base64/`. Nếu bạn muốn luôn có thể dùng "wowthisiscool.i2p" để truy cập trang đó, thì dĩ nhiên bạn vẫn sẽ phải thêm bản ghi đó vào hosts.txt của bạn (cho đến khi MyI2P address book được phát hành, ý là vậy ;)

## 3) AMOC vs. restricted routes

Mule đã đề xuất một số ý tưởng và thúc giục tôi giải thích vài điều, và trong quá trình đó, anh ấy đã đạt được một số tiến triển khi khiến tôi xem xét lại toàn bộ ý tưởng AMOC. Cụ thể, nếu chúng ta bỏ một trong những ràng buộc tôi đã đặt lên lớp truyền tải của chúng ta - cho phép chúng ta giả định tính hai chiều - chúng ta có thể loại bỏ toàn bộ cơ chế truyền tải AMOC, thay vào đó triển khai một số hoạt động định tuyến hạn chế cơ bản (đặt nền tảng cho các kỹ thuật định tuyến hạn chế nâng cao hơn, như các nút ngang hàng đáng tin cậy và các router tunnels nhiều bước nhảy về sau).

Nếu chúng ta chọn hướng đi này, điều đó sẽ cho phép mọi người tham gia vào mạng phía sau tường lửa, NAT, v.v. mà không cần cấu hình, đồng thời cung cấp một số thuộc tính ẩn danh của định tuyến hạn chế. Đổi lại, điều đó có thể dẫn đến việc chúng tôi phải đại tu đáng kể lộ trình, nhưng nếu có thể thực hiện một cách an toàn, nó sẽ giúp tiết kiệm rất nhiều thời gian và hoàn toàn xứng đáng với sự thay đổi.

Tuy nhiên, chúng tôi không muốn vội vàng và sẽ cần xem xét kỹ lưỡng các tác động đối với tính ẩn danh và bảo mật trước khi cam kết đi theo hướng đó. Chúng tôi sẽ thực hiện việc này sau khi 0.4 được phát hành và chạy ổn định, vì vậy không có gì phải vội.

## 2) Trạng thái 0.4

Nghe đồn là aum đang tiến triển khá tốt - tôi không biết liệu anh ấy có có mặt trong cuộc họp để cung cấp bản cập nhật hay không, nhưng sáng nay anh ấy đã để lại cho chúng ta một đoạn trích trên #i2p:

```
<aum> hi all, can't talk long, just a quick stasher update - work is
      continuing on implementing freenet keytypes, and freenet FCP
      compatibility - work in progress, should have a test build
      ready to try out by the end of the week
```
Tuyệt.

## 5) pages of note

Tôi chỉ muốn lưu ý hai tài nguyên mới hiện có mà người dùng I2P có thể muốn xem qua - DrWoo đã tập hợp một trang với rất nhiều thông tin dành cho những người muốn duyệt web ẩn danh, và Luckypunk đã đăng một bài hướng dẫn mô tả trải nghiệm với một số JVM (máy ảo Java) trên FreeBSD. Hypercubus cũng đã đăng tài liệu về việc thử nghiệm tích hợp dịch vụ và systray (khay hệ thống) chưa được phát hành.

## 6) ???

Ok, hiện tại tôi chỉ có bấy nhiêu thôi - ghé qua buổi họp tối nay lúc 9 giờ tối GMT nếu bạn muốn nêu thêm điều gì khác.

=jr
