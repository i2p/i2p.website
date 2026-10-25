---
title: "BOB - Cầu Nối Mở Cơ Bản"
description: "API đã lỗi thời để quản lý destination"
slug: "bob"
aliases:
  - "/vi/docs/api/bob"
  - "/vi/docs/api/bob/"
  - "/vi/bob"
  - "/vi/bob/"
lastUpdated: "2025-05"
accurateFor: "0.9.8"
---

## Cảnh báo - Đã ngừng hỗ trợ

Không dành cho các ứng dụng mới. BOB, như được chỉ định ở đây, chỉ hỗ trợ loại chữ ký DSA-SHA1. BOB sẽ không được mở rộng để hỗ trợ các loại chữ ký mới hoặc các tính năng nâng cao khác. Các ứng dụng mới nên sử dụng [SAM V3](/docs/api/samv3).

Hỗ trợ BOB đã được loại bỏ khỏi các bản cài đặt mới của Java I2P kể từ phiên bản 1.7.0 (2022-02). Nó vẫn sẽ hoạt động trong Java I2P được cài đặt ban đầu với phiên bản 1.6.1 hoặc sớm hơn, ngay cả sau khi cập nhật, nhưng nó không được hỗ trợ và có thể bị hỏng bất cứ lúc nào. BOB vẫn được i2pd hỗ trợ tính đến 2025-05, nhưng các ứng dụng vẫn nên di chuyển sang SAMv3 vì các lý do nêu trên. Xem [tài liệu i2pd](https://i2pd.readthedocs.io/en/latest/devs/i2pd-specifics/) để biết các phần mở rộng API được ghi lại ở đây mà i2pd hỗ trợ.

Tại thời điểm này, hầu hết các ý tưởng hay từ BOB đã được tích hợp vào SAMv3, có nhiều tính năng hơn và được sử dụng thực tế nhiều hơn. BOB có thể vẫn hoạt động trên một số cài đặt (xem ở trên), nhưng nó không nhận được các tính năng tiên tiến có sẵn trong SAMv3 và về cơ bản không được hỗ trợ, ngoại trừ bởi i2pd.

## Thư viện ngôn ngữ cho BOB API

- Go - [ccondom](https://bitbucket.org/kallevedin/ccondom)
- Python - i2py-bob (git.repo.i2p)
- Twisted - [txi2p](https://pypi.python.org/pypi/txi2p)
- C++ - [bobcpp](https://gitlab.com/rszibele/bobcpp)

## Tổng quan

`KEYS` = cặp khóa công khai+riêng tư, đây là BASE64

`KEY` = khóa công khai, cũng là BASE64

`ERROR` như được ngụ ý sẽ trả về thông báo `"ERROR "+DESCRIPTION+"\n"`, trong đó `DESCRIPTION` là mô tả về điều gì đã xảy ra sai.

`OK` trả về `"OK"`, và nếu có dữ liệu cần trả về, nó sẽ nằm trên cùng dòng đó. `OK` có nghĩa là lệnh đã được thực hiện xong.

Các dòng `DATA` chứa thông tin mà bạn đã yêu cầu. Có thể có nhiều dòng `DATA` cho mỗi yêu cầu.

**LƯU Ý:** Lệnh help là lệnh DUY NHẤT có ngoại lệ đối với các quy tắc... nó thực sự có thể không trả về gì cả! Điều này là có chủ ý, vì help là lệnh dành cho CON NGƯỜI chứ không phải ỨNG DỤNG.

## Kết nối và Phiên bản

Tất cả đầu ra trạng thái BOB được xuất theo từng dòng. Các dòng có thể kết thúc bằng \\n hoặc \\r\\n, tùy thuộc vào hệ thống. Khi kết nối, BOB xuất ra hai dòng:

```
BOB version
OK
```
Phiên bản hiện tại là: 00.00.10

Lưu ý rằng các phiên bản trước đây sử dụng các chữ số hex viết hoa và không tuân thủ tiêu chuẩn phiên bản của I2P. Khuyến nghị rằng các phiên bản tiếp theo chỉ sử dụng các chữ số 0-9.

### Lịch sử Phiên bản

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">I2P Router Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Changes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">00.00.10</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.8</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">current version</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">00.00.00 - 00.00.0F</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">&nbsp;</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">development versions</td>
    </tr>
  </tbody>
</table>
## Lệnh

**VUI LÒNG LƯU Ý:** Để biết chi tiết HIỆN TẠI về các lệnh, VUI LÒNG sử dụng lệnh help tích hợp sẵn. Chỉ cần telnet đến localhost 2827 và gõ help, bạn sẽ có được tài liệu đầy đủ về từng lệnh.

Các lệnh không bao giờ bị lỗi thời hoặc thay đổi, tuy nhiên các lệnh mới thỉnh thoảng sẽ được thêm vào.

```
COMMAND     OPERAND                             RETURNS
help        (optional command to get help on)   NOTHING or OK and description of the command
clear                                           ERROR or OK
getdest                                         ERROR or OK and KEY
getkeys                                         ERROR or OK and KEYS
getnick     tunnelname                          ERROR or OK
inhost      hostname or IP address              ERROR or OK
inport      port number                         ERROR or OK
list                                            ERROR or DATA lines and final OK
lookup      hostname                            ERROR or OK and KEY
newkeys                                         ERROR or OK and KEY
option      key1=value1 key2=value2...          ERROR or OK
outhost     hostname or IP address              ERROR or OK
outport     port number                         ERROR or OK
quiet                                           ERROR or OK
quit                                            OK and terminates the command connection
setkeys     KEYS                                ERROR or OK and KEY
setnick     tunnel nickname                     ERROR or OK
show                                            ERROR or OK and information
showprops                                       ERROR or OK and information
start                                           ERROR or OK
status      tunnel nickname                     ERROR or OK and information
stop                                            ERROR or OK
verify      KEY                                 ERROR or OK
visit                                           OK, and dumps BOB's threads to the wrapper.log
zap                                             nothing, quits BOB
```
Một khi đã thiết lập, tất cả các TCP socket có thể và sẽ chặn khi cần thiết, và không cần thêm bất kỳ thông điệp nào đến/từ kênh lệnh. Điều này cho phép router điều chỉnh tốc độ luồng dữ liệu mà không bị tràn bộ nhớ (OOM) như SAM khi nó bị nghẽn do cố gắng đẩy nhiều luồng vào hoặc ra một socket -- điều đó không thể mở rộng khi bạn có nhiều kết nối!

Điều tuyệt vời khác về giao diện đặc biệt này là việc viết bất cứ thứ gì để giao tiếp với nó dễ dàng hơn rất nhiều so với SAM. Không cần xử lý gì thêm sau khi thiết lập xong. Cấu hình của nó đơn giản đến mức các công cụ rất cơ bản như nc (netcat) có thể được sử dụng để trỏ đến một ứng dụng nào đó. Giá trị ở đây là bạn có thể lên lịch thời gian bật và tắt cho một ứng dụng mà không cần thay đổi ứng dụng đó, hoặc thậm chí không cần dừng ứng dụng đó. Thay vào đó, bạn có thể thực sự "rút phích cắm" điểm đích và "cắm lại". Miễn là các địa chỉ IP/cổng và khóa destination giống nhau được sử dụng khi khởi động bridge, ứng dụng TCP thông thường sẽ không quan tâm và không nhận ra. Nó sẽ đơn giản bị "đánh lừa" -- các destination không thể tiếp cận được và không có gì đến.

## Ví dụ

Đối với ví dụ sau đây, chúng ta sẽ thiết lập một kết nối loopback cục bộ rất đơn giản với hai điểm đến. Điểm đến "mouth" sẽ là dịch vụ CHARGEN từ daemon superserver INET. Điểm đến "ear" sẽ là một cổng cục bộ mà bạn có thể telnet vào và xem các ký tự ASCII kiểm tra được hiển thị ra.

### Ví dụ Đối thoại Phiên làm việc

Lệnh telnet 127.0.0.1 2827 đơn giản hoạt động bình thường.

- A = Ứng dụng
- C = Phản hồi lệnh của BOB.

```
FROM    TO      DIALOGUE
C       A       BOB 00.00.10
C       A       OK
A       C       setnick mouth
C       A       OK Nickname set to mouth
A       C       newkeys
C       A       OK ZMPz1zinTdy3~zGD~f3g9aikZTipujEvvXOEyYfq4Su-mNKerqG710hFbkR6P-xkouVyNQsqWLI8c6ngnkSwGdUfM7hGccqBYDjIubTrlr~0g2-l0vM7Y8nSqtFrSdMw~pyufXZ0Ys3NqUSb8NuZXpiH2lCCkFG21QPRVfKBGwvvyDVU~hPVfBHuR8vkd5x0teMXGGmiTzdB96DuNRWayM0y8vkP-1KJiPFxKjOXULjuXhLmINIOYn39bQprq~dAtNALoBgd-waZedYgFLvwHDCc9Gui8Cpp41EihlYGNW0cu0vhNFUN79N4DEpO7AtJyrSu5ZjFTAGjLw~lOvhyO2NwQ4RiC4UCKSuM70Fz0BFKTJquIjUNkQ8pBPBYvJRRlRG9HjAcSqAMckC3pvKKlcTJJBAE8GqexV7rdCCIsnasJXle-6DoWrDkY1s1KNbEVH6i1iUEtmFr2IHTpPeFCyWfZ581CAFNRbbUs-MmnZu1tXAYF7I2-oXTH2hXoxCGAAAA
```
**GHI CHÚ DESTINATION KEY Ở TRÊN, KEY CỦA BẠN SẼ KHÁC!**

```
FROM    TO      DIALOGUE
A       C       outhost 127.0.0.1
C       A       OK outhost set
A       C       outport 19
C       A       OK outbound port set
A       C       start
C       A       OK tunnel starting
```
Tại thời điểm này, không có lỗi nào, một destination với nickname "mouth" đã được thiết lập. Khi bạn kết nối tới destination được cung cấp, bạn thực sự đang kết nối tới dịch vụ `CHARGEN` trên `19/TCP`.

Bây giờ đến nửa còn lại, để chúng ta có thể thực sự liên hệ với đích đến này.

```
FROM    TO      DIALOGUE
C       A       BOB 00.00.10
C       A       OK
A       C       setnick ear
C       A       OK Nickname set to ear
A       C       newkeys
C       A       OK 8SlWuZ6QNKHPZ8KLUlExLwtglhizZ7TG19T7VwN25AbLPsoxW0fgLY8drcH0r8Klg~3eXtL-7S-qU-wdP-6VF~ulWCWtDMn5UaPDCZytdGPni9pK9l1Oudqd2lGhLA4DeQ0QRKU9Z1ESqejAIFZ9rjKdij8UQ4amuLEyoI0GYs2J~flAvF4wrbF-LfVpMdg~tjtns6fA~EAAM1C4AFGId9RTGot6wwmbVmKKFUbbSmqdHgE6x8-xtqjeU80osyzeN7Jr7S7XO1bivxEDnhIjvMvR9sVNC81f1CsVGzW8AVNX5msEudLEggpbcjynoi-968tDLdvb-CtablzwkWBOhSwhHIXbbDEm0Zlw17qKZw4rzpsJzQg5zbGmGoPgrSD80FyMdTCG0-f~dzoRCapAGDDTTnvjXuLrZ-vN-orT~HIVYoHV7An6t6whgiSXNqeEFq9j52G95MhYIfXQ79pO9mcJtV3sfea6aGkMzqmCP3aikwf4G3y0RVbcPcNMQetDAAAA
A       C       inhost 127.0.0.1
C       A       OK inhost set
A       C       inport 37337
C       A       OK inbound port set
A       C       start
C       A       OK tunnel starting
A       C       quit
C       A       OK Bye!
```
Bây giờ tất cả những gì chúng ta cần làm là telnet vào 127.0.0.1, cổng 37337, gửi destination key hoặc địa chỉ host từ sổ địa chỉ mà chúng ta muốn liên hệ. Trong trường hợp này, chúng ta muốn liên hệ với "mouth", tất cả những gì chúng ta làm là dán key vào và nó sẽ hoạt động.

**LƯU Ý:** Lệnh "quit" trong kênh lệnh KHÔNG ngắt kết nối các tunnel như SAM.

```
$ telnet 127.0.0.1 37337
Trying 127.0.0.1...
Connected to 127.0.0.1.
Escape character is '^]'.
ZMPz1zinTdy3~zGD~f3g9aikZTipujEvvXOEyYfq4Su-mNKerqG710hFbkR6P-xkouVyNQsqWLI8c6ngnkSwGdUfM7hGccqBYDjIubTrlr~0g2-l0vM7Y8nSqtFrSdMw~pyufXZ0Ys3NqUSb8NuZXpiH2lCCkFG21QPRVfKBGwvvyDVU~hPVfBHuR8vkd5x0teMXGGmiTzdB96DuNRWayM0y8vkP-1KJiPFxKjOXULjuXhLmINIOYn39bQprq~dAtNALoBgd-waZedYgFLvwHDCc9Gui8Cpp41EihlYGNW0cu0vhNFUN79N4DEpO7AtJyrSu5ZjFTAGjLw~lOvhyO2NwQ4RiC4UCKSuM70Fz0BFKTJquIjUNkQ8pBPBYvJRRlRG9HjAcSqAMckC3pvKKlcTJJBAE8GqexV7rdCCIsnasJXle-6DoWrDkY1s1KNbEVH6i1iUEtmFr2IHTpPeFCyWfZ581CAFNRbbUs-MmnZu1tXAYF7I2-oXTH2hXoxCGAAAA
 !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefg
!"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefgh
"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghi
#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghij
$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijk
...
```
Sau vài dặm ảo của dòng thông tin này, nhấn `Control-]`

```
...
cdefghijklmnopqrstuvwxyz{|}~ !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJK
defghijklmnopqrstuvwxyz{|}~ !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKL
efghijklmnopqrstuvwxyz{|}~ !"#$%&'()*+,-./0123456789:;<=
telnet> c
Connection closed.
```
Đây là những gì đã xảy ra...

```
telnet -> ear -> i2p -> mouth -> chargen -.
telnet <- ear <- i2p <- mouth <-----------'
```
Bạn cũng có thể kết nối đến các SITES I2P!

```
$ telnet 127.0.0.1 37337
Trying 127.0.0.1...
Connected to 127.0.0.1.
Escape character is '^]'.
i2host.i2p
GET / HTTP/1.1

HTTP/1.1 200 OK
Date: Fri, 05 Dec 2008 14:20:28 GMT
Connection: close
Content-Type: text/html
Content-Length: 3946
Last-Modified: Fri, 05 Dec 2008 10:33:36 GMT
Accept-Ranges: bytes

<html>
<head>
  <title>I2HOST</title>
  <link rel="shortcut icon" href="favicon.ico">
</head>
...
<a href="http://sponge.i2p/">--Sponge.</a></pre>
<img src="/counter.gif" alt="!@^7A76Z!#(*&%"> visitors. </body>
</html>
Connection closed by foreign host.
$
```
Khá tuyệt phải không? Hãy thử một số I2P SITES nổi tiếng khác nếu bạn muốn, hoặc những trang không tồn tại, v.v., để cảm nhận xem loại kết quả nào sẽ xuất hiện trong các tình huống khác nhau. Phần lớn, bạn nên bỏ qua các thông báo lỗi. Chúng sẽ không có ý nghĩa gì với ứng dụng, và chỉ được hiển thị để con người debug.

### Dọn dẹp

Bây giờ chúng ta hãy đóng các đích đến sau khi đã hoàn thành với chúng.

Đầu tiên, hãy xem chúng ta có những nickname đích nào.

```
FROM    TO      DIALOGUE
A       C       list
C       A       DATA NICKNAME: mouth STARTING: false RUNNING: true STOPPING: false KEYS: true QUIET: false INPORT: not_set INHOST: localhost OUTPORT: 19 OUTHOST: 127.0.0.1
C       A       DATA NICKNAME: ear STARTING: false RUNNING: true STOPPING: false KEYS: true QUIET: false INPORT: 37337 INHOST: 127.0.0.1 OUTPORT: not_set OUTHOST: localhost
C       A       OK Listing done
```
Được rồi, chúng ở đây. Trước tiên, hãy xóa "mouth".

```
FROM    TO      DIALOGUE
A       C       getnick mouth
C       A       OK Nickname set to mouth
A       C       stop
C       A       OK tunnel stopping
A       C       clear
C       A       OK cleared
```
Bây giờ để xóa "ear", lưu ý rằng đây là điều xảy ra khi bạn gõ quá nhanh, và cho bạn thấy các thông báo ERROR thông thường trông như thế nào.

```
FROM    TO      DIALOGUE
A       C       getnick ear
C       A       OK Nickname set to ear
A       C       stop
C       A       OK tunnel stopping
A       C       clear
C       A       ERROR tunnel is active
A       C       clear
C       A       OK cleared
A       C       quit
C       A       OK Bye!
```
## Chế độ Im lặng

Tôi sẽ không bận tâm đến việc hiển thị ví dụ về đầu nhận của cầu nối vì nó rất đơn giản. Có hai cài đặt có thể cho nó, và nó được bật/tắt bằng lệnh "quiet".

Mặc định là KHÔNG im lặng, và dữ liệu đầu tiên đến socket lắng nghe của bạn là destination đang thực hiện kết nối. Đó là một dòng duy nhất bao gồm địa chỉ BASE64 theo sau bởi một ký tự xuống dòng. Mọi thứ sau đó là dành cho ứng dụng thực sự xử lý.

Trong chế độ yên tĩnh, hãy coi nó như một kết nối Internet thông thường. Không có dữ liệu bổ sung nào được truyền vào. Nó giống như khi bạn kết nối trực tiếp với Internet thông thường vậy. Chế độ này cho phép một hình thức minh bạch giống như có sẵn trên các trang cài đặt tunnel của bảng điều khiển router, để bạn có thể sử dụng BOB để trỏ một đích đến máy chủ web chẳng hạn, và bạn sẽ không cần phải chỉnh sửa máy chủ web gì cả.

## Ưu điểm của BOB

Lợi ích khi sử dụng BOB cho việc này như đã thảo luận trước đó. Bạn có thể lên lịch thời gian hoạt động ngẫu nhiên cho ứng dụng, chuyển hướng đến một máy khác, v.v. Một ứng dụng của điều này có thể là muốn cố gắng làm rối loạn việc đoán trạng thái hoạt động từ router đến đích. Bạn có thể dừng và khởi động đích với một quy trình hoàn toàn khác để tạo ra thời gian hoạt động và ngừng hoạt động ngẫu nhiên trên các dịch vụ. Theo cách đó, bạn chỉ cần ngừng khả năng liên lạc với dịch vụ như vậy, và không phải bận tâm đến việc tắt và khởi động lại nó. Bạn có thể chuyển hướng và trỏ đến một máy khác trên LAN trong khi thực hiện cập nhật, hoặc trỏ đến một tập hợp các máy dự phòng tùy thuộc vào những gì đang chạy, v.v., v.v. Chỉ có trí tưởng tượng của bạn mới giới hạn những gì bạn có thể làm với BOB.
