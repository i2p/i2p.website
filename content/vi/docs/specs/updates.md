---
title: "Đặc tả Cập nhật Phần mềm"
description: "Đặc tả cho cơ chế cập nhật phần mềm I2P, định dạng tệp SU3, và nguồn cấp tin tức"
slug: "updates"
aliases:
  - "/vi/updates"
  - "/vi/updates/"
category: "Thiết kế"
lastUpdated: "2025-04"
accurateFor: "0.9.65"
---

## Tổng quan

I2P sử dụng một hệ thống cập nhật phần mềm tự động đơn giản nhưng an toàn. Console của router định kỳ tải xuống một file tin tức từ một I2P URL có thể cấu hình được. Có một URL dự phòng được mã hóa cứng trỏ đến website của dự án, trong trường hợp máy chủ tin tức mặc định của dự án bị ngừng hoạt động.

Nội dung của tệp tin news được hiển thị trên trang chủ của bảng điều khiển router. Ngoài ra, tệp tin news chứa số phiên bản mới nhất của phần mềm. Nếu phiên bản cao hơn số phiên bản của router, nó sẽ hiển thị thông báo cho người dùng biết rằng có bản cập nhật khả dụng.

Router có thể tùy chọn tải xuống, hoặc tải xuống và cài đặt phiên bản mới nếu được cấu hình để làm như vậy.

## Thông Số Kỹ Thuật Tệp Tin Cũ

Định dạng này đã được thay thế bằng định dạng tin tức su3 kể từ phiên bản 0.9.17.

Tệp news.xml có thể chứa các phần tử sau:

```
<i2p.news date="$Date: 2010-01-22 00:00:00 $" />
<i2p.release version="0.7.14" date="2010/01/22" minVersion="0.6" />
```
Các tham số trong mục i2p.release như sau. Tất cả các khóa không phân biệt chữ hoa chữ thường. Tất cả các giá trị phải được đặt trong dấu ngoặc kép.

**date** : Ngày phát hành của phiên bản router. Không được sử dụng. Định dạng không được chỉ định.

**minJavaVersion** : Phiên bản Java tối thiểu cần thiết để chạy phiên bản hiện tại. Tính đến phiên bản 0.9.9.

**minVersion** : Phiên bản tối thiểu của router cần thiết để cập nhật lên phiên bản hiện tại. Nếu router cũ hơn phiên bản này, người dùng phải cập nhật (thủ công?) lên một phiên bản trung gian trước. Kể từ bản phát hành 0.9.9.

**su3Clearnet** : Một hoặc nhiều URL HTTP nơi có thể tìm thấy file cập nhật .su3 trên clearnet (không phải I2P). Nhiều URL phải được phân tách bằng dấu cách hoặc dấu phẩy. Kể từ phiên bản 0.9.9.

**su3SSL** : Một hoặc nhiều URL HTTPS nơi có thể tìm thấy tệp cập nhật .su3 trên clearnet (không phải I2P). Nhiều URL phải được phân tách bằng dấu cách hoặc dấu phẩy. Kể từ phiên bản 0.9.9.

**sudTorrent** : Liên kết magnet cho torrent .sud (không phải pack200) của bản cập nhật. Kể từ phiên bản 0.9.4.

**su2Torrent** : Liên kết magnet cho torrent .su2 (pack200) của bản cập nhật. Kể từ phiên bản 0.9.4.

**su3Torrent** : Liên kết magnet cho torrent định dạng .su3 (định dạng mới) của bản cập nhật. Kể từ phiên bản 0.9.9.

**version** : Bắt buộc. Phiên bản router hiện tại mới nhất có sẵn.

Các phần tử có thể được bao gồm bên trong các comment XML để ngăn trình duyệt diễn giải. Phần tử i2p.release và version là bắt buộc. Tất cả các phần tử khác đều là tùy chọn. LƯU Ý: Do hạn chế của parser, toàn bộ phần tử phải nằm trên một dòng duy nhất.

## Đặc tả Tệp Cập nhật

Kể từ phiên bản 0.9.9, tệp cập nhật đã ký tên i2pupdate.su3 sẽ sử dụng định dạng tệp "su3" được quy định bên dưới. Những người ký phiên bản được phê duyệt sẽ sử dụng khóa RSA 4096-bit. Các chứng chỉ khóa công khai X.509 cho những người ký này được phân phối trong các gói cài đặt router. Các bản cập nhật có thể chứa chứng chỉ cho những người ký mới được phê duyệt, và/hoặc chứa danh sách các chứng chỉ cần xóa để thu hồi.

## Đặc tả Tệp Cập nhật Cũ

Định dạng này đã lỗi thời kể từ phiên bản 0.9.9.

Tệp cập nhật đã ký, thường được đặt tên i2pupdate.sud, đơn giản là một tệp zip với tiêu đề 56 byte được thêm vào phía trước. Tiêu đề chứa:

- Một [Signature](/docs/specs/common-structures#signature) DSA 40-byte
- Một phiên bản I2P 16-byte ở định dạng UTF-8, được đệm với các số không ở cuối nếu cần thiết

Chữ ký chỉ bao phủ tệp zip archive - không phải phiên bản được thêm vào phía trước. Chữ ký phải khớp với một trong các DSA [SigningPublicKey](/docs/specs/common-structures#signingpublickey) được cấu hình trong router, có danh sách khóa mặc định được mã hóa cứng của các quản lý phát hành dự án hiện tại.

Với mục đích so sánh phiên bản, các trường phiên bản chứa [0-9]*, các ký tự phân cách trường là '-', '_', và '.', và tất cả các ký tự khác sẽ được bỏ qua.

Kể từ phiên bản 0.8.8, phiên bản cũng phải được chỉ định dưới dạng bình luận của tập tin zip bằng UTF-8, không có các số không ở cuối. Router cập nhật sẽ xác minh rằng phiên bản trong header (không được bao phủ bởi chữ ký) khớp với phiên bản trong bình luận tập tin zip, nơi được bao phủ bởi chữ ký. Điều này ngăn chặn việc giả mạo số phiên bản trong header.

## Tải xuống và Cài đặt

Router đầu tiên tải xuống header của file cập nhật từ một trong danh sách các URL I2P có thể cấu hình, sử dụng HTTP client và proxy tích hợp, và kiểm tra rằng phiên bản mới hơn. Điều này ngăn chặn vấn đề của các host cập nhật không có file mới nhất. Router sau đó tải xuống file cập nhật đầy đủ. Router xác minh rằng phiên bản file cập nhật mới hơn trước khi cài đặt. Tất nhiên, nó cũng xác minh chữ ký, và xác minh rằng comment của file zip khớp với phiên bản header, như đã giải thích ở trên.

File zip được giải nén và sao chép thành "i2pupdate.zip" trong thư mục cấu hình I2P (~/.i2p trên Linux).

Kể từ phiên bản 0.7.12, router hỗ trợ giải nén Pack200. Các tệp bên trong kho lưu trữ zip có hậu tố .jar.pack hoặc .war.pack sẽ được giải nén một cách minh bạch thành tệp .jar hoặc .war. Các tệp cập nhật chứa tệp .pack thường được đặt tên với hậu tố '.su2'. Pack200 giảm kích thước tệp cập nhật khoảng 60%.

Kể từ phiên bản 0.8.7, router sẽ xóa các tệp libjbigi.so và libjcpuid.so nếu tệp zip chứa tệp lib/jbigi.jar, để các tệp mới sẽ được giải nén từ jbigi.jar.

Từ phiên bản 0.8.12, nếu tệp zip chứa một tệp deletelist.txt, router sẽ xóa các tệp được liệt kê ở đó. Định dạng là:

- Một tên tệp trên mỗi dòng
- Tất cả tên tệp đều tương đối với thư mục cài đặt; không cho phép tên tệp tuyệt đối, không có tệp bắt đầu bằng ".."
- Bình luận bắt đầu bằng '#'

Router sau đó sẽ xóa tệp deletelist.txt.

## Đặc tả tệp SU3

Đặc tả này được sử dụng cho các bản cập nhật router từ phiên bản 0.9.9, dữ liệu reseed từ phiên bản 0.9.14, plugin từ phiên bản 0.9.15, và tệp tin tin tức từ phiên bản 0.9.17.

### Các vấn đề với định dạng .sud/.su2 trước đây

- Không có magic number hoặc flags
- Không có cách để chỉ định nén, pack200 hay không, hoặc thuật toán ký
- Phiên bản không được bao phủ bởi chữ ký, nên nó được thực thi bằng cách yêu cầu phải có trong zip file comment (đối với router files) hoặc trong file plugin.config (đối với plugins)
- Người ký không được chỉ định nên trình xác minh phải thử tất cả các khóa đã biết
- Định dạng signature-before-data yêu cầu hai lần duyệt để tạo file

### Mục tiêu

- Khắc phục các vấn đề trên
- Chuyển đổi sang thuật toán chữ ký an toàn hơn
- Giữ thông tin phiên bản cùng định dạng và offset để tương thích với các trình kiểm tra phiên bản hiện có
- Xác minh chữ ký và trích xuất tệp trong một lần

### Đặc tả kỹ thuật

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bytes</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0-5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Magic number "I2Psu3"</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">6</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">unused = 0</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">su3 file format version = 0</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">8-9</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Signature type: 0x0000 = DSA-SHA1, 0x0001 = ECDSA-SHA256-P256, 0x0002 = ECDSA-SHA384-P384, 0x0003 = ECDSA-SHA512-P521, 0x0004 = RSA-SHA256-2048, 0x0005 = RSA-SHA384-3072, 0x0006 = RSA-SHA512-4096, 0x0008 = EdDSA-SHA512-Ed25519ph</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">10-11</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Signature length, e.g. 40 (0x0028) for DSA-SHA1. Must match that specified for the <a href="/docs/specs/common-structures#signature">Signature</a> type.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">unused = 0</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">13</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Version length (in bytes not chars, including padding), must be at least 16 (0x10) for compatibility</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">14</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">unused = 0</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">15</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Signer ID length (in bytes not chars)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">16-23</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Content length (not including header or sig)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">24</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">unused = 0</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">25</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">File type: 0x00 = zip file, 0x01 = xml file (0.9.15), 0x02 = html file (0.9.17), 0x03 = xml.gz file (0.9.17), 0x04 = txt.gz file (0.9.28), 0x05 = dmg file (0.9.51), 0x06 = exe file (0.9.51)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">26</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">unused = 0</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">27</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Content type: 0x00 = unknown, 0x01 = router update, 0x02 = plugin or plugin update, 0x03 = reseed data, 0x04 = news feed (0.9.15), 0x05 = blocklist feed (0.9.28)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">28-39</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">unused = 0</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">40-55+</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Version, UTF-8 padded with trailing 0x00, 16 bytes minimum, length specified at byte 13. Do not append 0x00 bytes if the length is 16 or more.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">xx+</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ID of signer, (e.g. "zzz@mail.i2p") UTF-8, not padded, length specified at byte 15</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">xx+</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Content: Length specified in header at bytes 16-23, Format specified in header at byte 25, Content specified in header at byte 27</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">xx+</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Signature: Length is specified in header at bytes 10-11, covers everything starting at byte 0</td>
    </tr>
  </tbody>
</table>
Tất cả các trường không sử dụng phải được đặt thành 0 để tương thích với các phiên bản tương lai.

### Chi Tiết Chữ Ký

Chữ ký bao phủ toàn bộ header bắt đầu từ byte 0, cho đến cuối nội dung. Chúng tôi sử dụng chữ ký thô. Lấy hash của dữ liệu (sử dụng loại hash được ngụ ý bởi loại chữ ký tại byte 8-9) và truyền nó cho hàm ký hoặc xác minh "thô" (ví dụ: "NONEwithRSA" trong Java).

Mặc dù việc xác minh chữ ký và trích xuất nội dung có thể được thực hiện trong một lần xử lý, một implementation phải đọc và lưu vào buffer 10 byte đầu tiên để xác định loại hash trước khi bắt đầu xác minh.

Độ dài chữ ký cho các loại chữ ký khác nhau được đưa ra trong thông số kỹ thuật [Signature](/docs/specs/common-structures#signature). Thêm các số 0 đứng đầu vào chữ ký nếu cần thiết. Xem [trang chi tiết mật mã học](/docs/specs/cryptography#sig) để biết thông số của các loại chữ ký khác nhau.

### Ghi chú

Loại nội dung chỉ định miền tin cậy. Đối với mỗi loại nội dung, các client duy trì một tập hợp các chứng chỉ khóa công khai X.509 cho các bên được tin cậy để ký nội dung đó. Chỉ có thể sử dụng các chứng chỉ cho loại nội dung được chỉ định. Chứng chỉ được tra cứu bằng ID của người ký. Các client phải xác minh rằng loại nội dung là như mong đợi cho ứng dụng.

Tất cả các giá trị đều theo thứ tự byte mạng (big endian).

Để có một implementation Python của Raw RSA signatures tương thích với Java "NONEwithRSA", hãy xem [bài viết Stack Overflow này](https://stackoverflow.com/questions/59573121/python-rsa-sign-a-string-with-nonewithrsa/68301530#68301530).

## Đặc tả Tệp Cập nhật Router SU3

### Chi tiết SU3

- SU3 Content Type: 1 (ROUTER UPDATE)
- SU3 File Type: 0 (ZIP)
- SU3 Version: Phiên bản router

Các file jar và war trong zip không còn được nén bằng pack200 như đã được ghi chép ở trên cho các file "su2", vì các Java runtime gần đây không còn hỗ trợ nó nữa.

### Ghi chú

- Đối với các bản phát hành, phiên bản SU3 là phiên bản router "cơ bản", ví dụ "0.9.20".
- Đối với các bản build phát triển, được hỗ trợ từ bản phát hành 0.9.20, phiên bản SU3 là phiên bản router "đầy đủ", ví dụ "0.9.20-5" hoặc "0.9.20-5-rc". Xem RouterVersion.java trong [mã nguồn I2P](https://github.com/i2p/i2p.i2p).

## Đặc tả Tệp SU3 Reseed

Kể từ phiên bản 0.9.14, dữ liệu reseed được cung cấp trong định dạng tệp "su3".

### Mục tiêu

- Các tệp đã ký với chữ ký mạnh và chứng chỉ đáng tin cậy để ngăn chặn các cuộc tấn công man-in-the-middle có thể khởi động nạn nhân vào một mạng riêng biệt, không đáng tin cậy.
- Sử dụng định dạng tệp su3 đã được sử dụng cho các bản cập nhật và plugin
- Tệp nén đơn lẻ để tăng tốc quá trình reseeding, vốn chậm khi phải tải 200 tệp

### Đặc tả

1. Tệp phải được đặt tên là "i2pseeds.su3". Kể từ phiên bản 0.9.42, người yêu cầu nên thêm chuỗi truy vấn "?netid=2" vào URL yêu cầu, giả sử network ID hiện tại là 2. Điều này có thể được sử dụng để ngăn chặn các kết nối xuyên mạng. Các mạng thử nghiệm nên đặt một network ID khác. Xem đề xuất 147 để biết chi tiết.
2. Tệp phải nằm trong cùng thư mục với các router infos trên web server.
3. Một router trước tiên sẽ cố gắng tải (index URL)/i2pseeds.su3; nếu thất bại, nó sẽ tải index URL và sau đó tải các tệp router info riêng lẻ được tìm thấy trong các liên kết.

### Chi tiết SU3

- SU3 Content Type: 3 (RESEED)
- SU3 File Type: 0 (ZIP)
- SU3 Version: Số giây từ epoch, dạng ASCII (date +%s). KHÔNG bị reset vào năm 2038 hoặc 2106.
- Các file thông tin router trong file zip phải ở "cấp độ đầu". Không có thư mục nào trong file zip.
- Các file thông tin router phải được đặt tên "routerInfo-(44 ký tự base 64 router hash).dat", như trong cơ chế reseed cũ. Bảng chữ cái base 64 của I2P phải được sử dụng.

### Ghi chú

- Cảnh báo: Một số reseed được biết là không phản hồi qua IPv6. Khuyến nghị buộc hoặc ưu tiên sử dụng IPv4.
- Cảnh báo: Một số reseed sử dụng chứng chỉ CA tự ký. Các triển khai phải nhập và tin tưởng các CA này khi reseed, hoặc loại bỏ các reseed tự ký khỏi danh sách reseed.
- Các khóa ký reseed được phân phối đến các triển khai dưới dạng chứng chỉ X.509 tự ký với khóa RSA-4096 (loại chữ ký 6). Các triển khai nên thực thi các ngày hợp lệ trong chứng chỉ.

## Đặc tả Tệp Plugin SU3

Kể từ phiên bản 0.9.15, các plugin có thể được đóng gói trong định dạng file "su3".

### Chi tiết SU3

- SU3 Content Type: 2 (PLUGIN)
- SU3 File Type: 0 (ZIP) - Xem [đặc tả plugin](/docs/specs/plugin) để biết chi tiết.
- SU3 Version: Phiên bản plugin, phải khớp với phiên bản trong plugin.config.

Các tệp jar và war trong zip không nên được nén bằng pack200 như đã ghi chú ở trên cho các tệp "su2", vì các runtime Java gần đây không còn hỗ trợ nó nữa.

## Đặc tả Tệp Tin SU3 News

Kể từ phiên bản 0.9.17, tin tức được phân phối dưới định dạng tệp "su3".

### Mục tiêu

- Tin tức được ký với chữ ký mạnh và chứng chỉ đáng tin cậy
- Sử dụng định dạng file su3 đã được dùng cho cập nhật, reseeding và plugin
- Định dạng XML tiêu chuẩn để sử dụng với các trình phân tích tiêu chuẩn
- Định dạng Atom tiêu chuẩn để sử dụng với các trình đọc và tạo feed tiêu chuẩn
- Làm sạch và xác minh HTML trước khi hiển thị trên console
- Phù hợp để triển khai dễ dàng trên Android và các nền tảng khác không có HTML console

### Chi tiết SU3

- SU3 Content Type: 4 (NEWS)
- SU3 File Type: 1 (XML) hoặc 3 (XML.GZ)
- SU3 Version: Số giây kể từ epoch, trong ASCII (date +%s). KHÔNG bị tràn số vào năm 2038 hoặc 2106.
- File Format: XML hoặc XML nén gzip, chứa một [RFC 4287](https://tools.ietf.org/html/rfc4287) (Atom) XML Feed. Charset phải là UTF-8.

### Chi tiết Atom Feed

Các phần tử `<feed>` sau đây được sử dụng:

**`<entry>`** : Một mục tin tức. Xem bên dưới.

**`<i2p:release>`** : Metadata cập nhật I2P. Xem bên dưới.

**`<i2p:revocations>`** : Thu hồi chứng chỉ. Xem bên dưới.

**`<i2p:blocklist>`** : Dữ liệu danh sách chặn. Xem bên dưới.

**`<updated>`** : Bắt buộc. Dấu thời gian cho feed (tuân thủ [RFC 4287](https://tools.ietf.org/html/rfc4287) mục 3.3 và [RFC 3339](https://tools.ietf.org/html/rfc3339)).

### Chi Tiết Mục Atom

Mỗi `<entry>` Atom trong news feed có thể được phân tích và hiển thị trong router console. Các phần tử sau được sử dụng:

**`<author>`** : Tùy chọn. Chứa `<name>` - Tên của tác giả mục nhập.

**`<content>`** : Bắt buộc. Nội dung, phải có type="xhtml". XHTML sẽ được làm sạch với danh sách trắng các phần tử được phép và danh sách đen các thuộc tính không được phép. Client có thể bỏ qua một phần tử, hoặc entry bao quanh, hoặc toàn bộ feed khi gặp phải phần tử không có trong danh sách trắng.

**`<link>`** : Tùy chọn. Liên kết để biết thêm thông tin.

**`<summary>`** : Tùy chọn. Tóm tắt ngắn gọn, phù hợp cho tooltip.

**`<title>`** : Bắt buộc. Tiêu đề của mục tin tức.

**`<updated>`** : Bắt buộc. Dấu thời gian cho mục này (tuân theo [RFC 4287](https://tools.ietf.org/html/rfc4287) mục 3.3 và [RFC 3339](https://tools.ietf.org/html/rfc3339)).

### Chi tiết Atom i2p:release

Phải có ít nhất một thực thể `<i2p:release>` trong feed. Mỗi thực thể chứa các thuộc tính và thực thể sau:

**date (thuộc tính)** : Bắt buộc. Dấu thời gian cho mục này (tuân thủ [RFC 4287](https://tools.ietf.org/html/rfc4287) mục 3.3 và [RFC 3339](https://tools.ietf.org/html/rfc3339)). Ngày cũng có thể ở định dạng cắt ngắn yyyy-mm-dd (không có 'T'); đây là định dạng "full-date" trong RFC 3339. Trong định dạng này, thời gian được giả định là 00:00:00 UTC cho bất kỳ quá trình xử lý nào.

**minJavaVersion (thuộc tính)** : Nếu có, phiên bản Java tối thiểu cần thiết để chạy phiên bản hiện tại.

**minVersion (thuộc tính)** : Nếu có, phiên bản tối thiểu của router cần thiết để cập nhật lên phiên bản hiện tại. Nếu router cũ hơn phiên bản này, người dùng phải cập nhật (thủ công?) lên phiên bản trung gian trước.

**`<i2p:version>`** : Bắt buộc. Phiên bản router hiện tại mới nhất có sẵn.

**`<i2p:update>`** : Một tệp cập nhật (một hoặc nhiều). Nó phải chứa ít nhất một phần tử con.   - type (thuộc tính): "sud", "su2", hoặc "su3". Phải là duy nhất trên tất cả các phần tử `<i2p:update>`.   - `<i2p:clearnet>`: Liên kết tải xuống trực tiếp ngoài mạng (không hoặc nhiều). href (thuộc tính): Một liên kết http clearnet tiêu chuẩn.   - `<i2p:clearnetssl>`: Liên kết tải xuống trực tiếp ngoài mạng (không hoặc nhiều). href (thuộc tính): Một liên kết https clearnet tiêu chuẩn.   - `<i2p:torrent>`: Liên kết magnet trong mạng. href (thuộc tính): Một liên kết magnet.   - `<i2p:url>`: Liên kết tải xuống trực tiếp trong mạng (không hoặc nhiều). href (thuộc tính): Một liên kết http .i2p trong mạng.

### Chi tiết Atom i2p:revocations

Thực thể này là tùy chọn và có tối đa một thực thể `<i2p:revocations>` trong feed. Tính năng này được hỗ trợ từ phiên bản 0.9.26.

Thực thể `<i2p:revocations>` chứa một hoặc nhiều thực thể `<i2p:crl>`. Thực thể `<i2p:crl>` chứa các thuộc tính sau:

**updated (thuộc tính)** : Bắt buộc. Dấu thời gian cho mục này (tuân thủ theo [RFC 4287](https://tools.ietf.org/html/rfc4287) phần 3.3 và [RFC 3339](https://tools.ietf.org/html/rfc3339)). Ngày tháng cũng có thể ở định dạng rút gọn yyyy-mm-dd (không có 'T'); đây là định dạng "full-date" trong RFC 3339. Trong định dạng này, thời gian được giả định là 00:00:00 UTC cho bất kỳ quá trình xử lý nào.

**id (thuộc tính)** : Bắt buộc. Một id duy nhất cho người tạo CRL này.

**(nội dung thực thể)** : Bắt buộc. Một Danh sách Thu hồi Chứng chỉ (CRL) được mã hóa base 64 tiêu chuẩn có chứa các dòng mới, bắt đầu bằng dòng '-----BEGIN X509 CRL-----' và kết thúc bằng dòng '-----END X509 CRL-----'. Xem [RFC 5280](https://tools.ietf.org/html/rfc5280) để biết thêm thông tin về CRL.

### Chi tiết Atom i2p:blocklist

Thực thể này là tùy chọn và có tối đa một thực thể `<i2p:blocklist>` trong feed. Tính năng này được lên lịch triển khai trong phiên bản 0.9.28.

Thực thể `<i2p:blocklist>` chứa một hoặc nhiều thực thể `<i2p:block>` hoặc `<i2p:unblock>`, một thực thể "updated", và các thuộc tính "signer" và "sig":

**signer (thuộc tính)** : Bắt buộc. Một id duy nhất (UTF-8) cho khóa công khai được sử dụng để ký blocklist này.

**sig (thuộc tính)** : Bắt buộc. Một chữ ký theo định dạng code:b64sig, trong đó code là số loại chữ ký ASCII, và b64sig là chữ ký được mã hóa base 64 (bảng chữ cái I2P). Xem bên dưới để biết thông số kỹ thuật của dữ liệu cần được ký.

**`<updated>`** : Bắt buộc. Dấu thời gian cho blocklist (tuân thủ [RFC 4287](https://tools.ietf.org/html/rfc4287) mục 3.3 và [RFC 3339](https://tools.ietf.org/html/rfc3339)). Ngày cũng có thể ở định dạng rút gọn yyyy-mm-dd (không có 'T'); đây là định dạng "full-date" trong RFC 3339. Trong định dạng này, thời gian được giả định là 00:00:00 UTC cho bất kỳ quá trình xử lý nào.

**`<i2p:block>`** : Tùy chọn, cho phép nhiều thực thể. Một mục đơn lẻ, có thể là địa chỉ IPv4 hoặc IPv6 theo nghĩa đen, hoặc một router hash base 64 44 ký tự (bảng chữ cái I2P). Địa chỉ IPv6 có thể ở định dạng rút gọn (chứa "::"). Hỗ trợ cho các mục có netmask, ví dụ x.y.0.0/16, là tùy chọn. Hỗ trợ cho tên máy chủ là tùy chọn.

**`<i2p:unblock>`** : Tùy chọn, cho phép nhiều thực thể. Cùng định dạng với `<i2p:block>`.

**Đặc tả chữ ký:** Để tạo ra dữ liệu cần được ký hoặc xác minh, nối các dữ liệu sau theo mã hóa ASCII: Chuỗi đã cập nhật theo sau bởi một ký tự xuống dòng (ASCII 0x0a), sau đó mỗi mục block theo thứ tự nhận được với một ký tự xuống dòng sau mỗi mục, rồi mỗi mục unblock theo thứ tự nhận được với một ký tự xuống dòng sau mỗi mục.

## Đặc tả Tệp Danh sách Chặn

TBD, chưa được triển khai, xem đề xuất 130. Các cập nhật blocklist được gửi trong tệp tin news, xem phía trên.

## Công việc trong tương lai

- Cơ chế cập nhật router là một phần của giao diện điều khiển web router. Hiện tại không có cơ chế cập nhật cho router nhúng thiếu giao diện điều khiển router.

## Tài liệu tham khảo

- **[CRYPTO-SIG]** [Mật mã học - Chữ ký](/docs/specs/cryptography#sig)
- **[I2P-SRC]** [Mã nguồn I2P](https://github.com/i2p/i2p.i2p)
- **[PLUGIN]** [Đặc tả Plugin](/docs/specs/plugin)
- **[Python]** [Chữ ký RSA Raw của Python](https://stackoverflow.com/questions/59573121/python-rsa-sign-a-string-with-nonewithrsa/68301530#68301530)
- **[RFC-3339]** [RFC 3339 - Ngày và Thời gian](https://tools.ietf.org/html/rfc3339)
- **[RFC-4287]** [RFC 4287 - Định dạng Syndication Atom](https://tools.ietf.org/html/rfc4287)
- **[RFC-5280]** [RFC 5280 - Danh sách Thu hồi Chứng chỉ](https://tools.ietf.org/html/rfc5280)
- **[Signature]** [Kiểu Signature](/docs/specs/common-structures#signature)
- **[SigningPublicKey]** [Kiểu SigningPublicKey](/docs/specs/common-structures#signingpublickey)
