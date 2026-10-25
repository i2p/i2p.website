---
title: "Đặc tả Cơ sở dữ liệu Blockfile và Hosts"
description: "Đặc tả định dạng tệp blockfile của I2P và các bảng trong hostsdb.blockfile được sử dụng bởi Dịch vụ Đặt tên Blockfile"
slug: "blockfile"
aliases:
  - "/vi/blockfile"
  - "/vi/blockfile/"
category: "Định dạng"
lastUpdated: "2023-11"
accurateFor: "0.9.59"
---

## Tổng quan

Tài liệu này xác định định dạng tệp I2P blockfile và các bảng trong hostsdb.blockfile được sử dụng bởi Blockfile Naming Service [NAMING](/docs/overview/naming/).

Blockfile cung cấp khả năng tra cứu Destination nhanh chóng trong định dạng nhỏ gọn. Mặc dù chi phí overhead của trang blockfile khá đáng kể, các destination được lưu trữ dưới dạng nhị phân thay vì Base 64 như trong định dạng hosts.txt. Ngoài ra, blockfile cung cấp khả năng lưu trữ metadata tùy ý (như ngày thêm, nguồn và bình luận) cho mỗi mục. Metadata này có thể được sử dụng trong tương lai để cung cấp các tính năng addressbook nâng cao. Yêu cầu lưu trữ của blockfile chỉ tăng nhẹ so với định dạng hosts.txt, và blockfile cung cấp thời gian tra cứu giảm khoảng 10 lần.

Một blockfile đơn giản là lưu trữ trên đĩa của nhiều bản đồ đã sắp xếp (các cặp khóa-giá trị), được triển khai như các skiplist. Định dạng blockfile được áp dụng từ Cơ sở dữ liệu Blockfile Metanotion [METANOTION](http://www.metanotion.net/software/sandbox/block.html). Đầu tiên chúng ta sẽ định nghĩa định dạng tệp, sau đó là việc sử dụng định dạng đó bởi BlockfileNamingService.

## Định dạng Blockfile

Đặc tả blockfile gốc đã được sửa đổi để thêm magic numbers vào mỗi trang. Tệp được cấu trúc thành các trang 1024-byte. Các trang được đánh số bắt đầu từ 1. "Superblock" luôn ở trang 1, tức là bắt đầu từ byte 0 trong tệp. Metaindex skiplist luôn ở trang 2, tức là bắt đầu từ byte 1024 trong tệp.

Tất cả các giá trị số nguyên 2-byte đều không có dấu. Tất cả các giá trị số nguyên 4-byte (số trang) đều có dấu và các giá trị âm là bất hợp pháp. Tất cả các giá trị số nguyên đều được lưu trữ theo thứ tự byte mạng (big endian).

Cơ sở dữ liệu được thiết kế để mở và truy cập bởi một luồng duy nhất. BlockfileNamingService cung cấp khả năng đồng bộ hóa.

### Định dạng superblock

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Byte</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-5</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Magic number</td><td style="border:1px solid var(--color-border); padding:0.6rem;">0x3141de493250 ("1A" 0xde "I2P")</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">6</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Major version</td><td style="border:1px solid var(--color-border); padding:0.6rem;">0x01</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">7</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Minor version</td><td style="border:1px solid var(--color-border); padding:0.6rem;">0x02</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">8-15</td><td style="border:1px solid var(--color-border); padding:0.6rem;">File length</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Total length in bytes</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">16-19</td><td style="border:1px solid var(--color-border); padding:0.6rem;">First free list page</td><td style="border:1px solid var(--color-border); padding:0.6rem;"></td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">20-21</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Mounted flag</td><td style="border:1px solid var(--color-border); padding:0.6rem;">0x01 = yes</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">22-23</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Span size</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Max number of key/value pairs per span (16 for hostsdb). Used for new skip lists.</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">24-27</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Page size</td><td style="border:1px solid var(--color-border); padding:0.6rem;">As of version 1.2. Prior to 1.2, 1024 is assumed.</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">28-1023</td><td style="border:1px solid var(--color-border); padding:0.6rem;">unused</td><td style="border:1px solid var(--color-border); padding:0.6rem;"></td></tr>
</tbody>
</table>
### Định dạng trang khối danh sách bỏ qua

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Byte</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-7</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Magic number</td><td style="border:1px solid var(--color-border); padding:0.6rem;">0x536b69704c697374 "SkipList"</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">8-11</td><td style="border:1px solid var(--color-border); padding:0.6rem;">First span page</td><td style="border:1px solid var(--color-border); padding:0.6rem;"></td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">12-15</td><td style="border:1px solid var(--color-border); padding:0.6rem;">First level page</td><td style="border:1px solid var(--color-border); padding:0.6rem;"></td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">16-19</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Size</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Total number of keys - may only be valid at startup</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">20-23</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Spans</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Total number of spans - may only be valid at startup</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">24-27</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Levels</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Total number of levels - may only be valid at startup</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">28-29</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Span size</td><td style="border:1px solid var(--color-border); padding:0.6rem;">As of version 1.2. Max number of key/value pairs per span. Prior to that, specified for all skiplists in the superblock. Used for new spans in this skip list.</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">30-1023</td><td style="border:1px solid var(--color-border); padding:0.6rem;">unused</td><td style="border:1px solid var(--color-border); padding:0.6rem;"></td></tr>
</tbody>
</table>
### Định dạng trang khối bỏ qua cấp độ

Tất cả các cấp độ đều có span. Không phải tất cả các span đều có cấp độ.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Byte</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-7</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Magic number</td><td style="border:1px solid var(--color-border); padding:0.6rem;">0x42534c6576656c73 "BSLevels"</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">8-9</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Max height</td><td style="border:1px solid var(--color-border); padding:0.6rem;"></td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">10-11</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Current height</td><td style="border:1px solid var(--color-border); padding:0.6rem;"></td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">12-15</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Span page</td><td style="border:1px solid var(--color-border); padding:0.6rem;"></td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">16-</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Next level pages</td><td style="border:1px solid var(--color-border); padding:0.6rem;">'current height' entries, 4 bytes each, lowest first</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">remaining</td><td style="border:1px solid var(--color-border); padding:0.6rem;">unused</td><td style="border:1px solid var(--color-border); padding:0.6rem;"></td></tr>
</tbody>
</table>
### Bỏ qua định dạng trang khối span

Các cấu trúc key/value được sắp xếp theo key trong mỗi span và trên tất cả các span. Các cấu trúc key/value được sắp xếp theo key trong mỗi span. Các span khác ngoài span đầu tiên có thể không được để trống.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Byte</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-3</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Magic number</td><td style="border:1px solid var(--color-border); padding:0.6rem;">0x5370616e "Span"</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">4-7</td><td style="border:1px solid var(--color-border); padding:0.6rem;">First continuation page</td><td style="border:1px solid var(--color-border); padding:0.6rem;">or 0</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">8-11</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Previous span page</td><td style="border:1px solid var(--color-border); padding:0.6rem;">or 0</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">12-15</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Next span page</td><td style="border:1px solid var(--color-border); padding:0.6rem;">or 0</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">16-17</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Max keys</td><td style="border:1px solid var(--color-border); padding:0.6rem;">16 for hostsdb</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">18-19</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Size</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Current number of keys</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">20-1023</td><td style="border:1px solid var(--color-border); padding:0.6rem;">key/value structures</td><td style="border:1px solid var(--color-border); padding:0.6rem;"></td></tr>
</tbody>
</table>
### Định dạng trang khối tiếp tục Span

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Byte</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-3</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Magic number</td><td style="border:1px solid var(--color-border); padding:0.6rem;">0x434f4e54 "CONT"</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">4-7</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Next continuation page</td><td style="border:1px solid var(--color-border); padding:0.6rem;">or 0</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">8-1023</td><td style="border:1px solid var(--color-border); padding:0.6rem;">key/value structures</td><td style="border:1px solid var(--color-border); padding:0.6rem;"></td></tr>
</tbody>
</table>
### Định dạng cấu trúc key/value

Độ dài key và value không được phân tách qua các trang, tức là tất cả 4 byte phải nằm trên cùng một trang. Nếu không có đủ chỗ thì 1-3 byte cuối cùng của trang sẽ không được sử dụng và độ dài sẽ được đặt tại offset 8 trong trang tiếp theo. Dữ liệu key và value có thể được phân tách qua các trang. Độ dài tối đa của key và value là 65535 byte.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Byte</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-1</td><td style="border:1px solid var(--color-border); padding:0.6rem;">key length in bytes</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">2-3</td><td style="border:1px solid var(--color-border); padding:0.6rem;">value length in bytes</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">4-</td><td style="border:1px solid var(--color-border); padding:0.6rem;">key data</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;"></td><td style="border:1px solid var(--color-border); padding:0.6rem;">value data</td></tr>
</tbody>
</table>
### Định dạng trang khối danh sách trống

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Byte</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-7</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Magic number</td><td style="border:1px solid var(--color-border); padding:0.6rem;">0x2366724c69737423 "#frList#"</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">8-11</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Next free list block</td><td style="border:1px solid var(--color-border); padding:0.6rem;">or 0 if none</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">12-15</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Number of valid free pages</td><td style="border:1px solid var(--color-border); padding:0.6rem;">in this block (0 - 252)</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">16-1023</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Free pages</td><td style="border:1px solid var(--color-border); padding:0.6rem;">4 bytes each, only the first (valid number) are valid</td></tr>
</tbody>
</table>
### Định dạng khối trang trống

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Byte</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-7</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Magic number</td><td style="border:1px solid var(--color-border); padding:0.6rem;">0x7e2146524545217e "~!FREE!~"</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">8-1023</td><td style="border:1px solid var(--color-border); padding:0.6rem;">unused</td><td style="border:1px solid var(--color-border); padding:0.6rem;"></td></tr>
</tbody>
</table>
Metaindex (nằm ở trang 2) là một ánh xạ từ các chuỗi US-ASCII đến các số nguyên 4-byte. Khóa là tên của skiplist và giá trị là chỉ số trang của skiplist.

## Bảng Dịch vụ Đặt tên Blockfile

Các bảng được tạo và sử dụng bởi BlockfileNamingService như sau. Số lượng mục tối đa trên mỗi span là 16.

### Properties Skiplist

`%%__INFO__%%` là skiplist cơ sở dữ liệu chính với các mục key/value String/Properties chỉ chứa một mục:

**info** - một Properties (UTF-8 String/String Map), được tuần tự hóa như một [Mapping](/docs/specs/common-structures/#type-mapping):

- **version** - "4"
- **created** - Thời gian Java long (ms)
- **upgraded** - Thời gian Java long (ms) (kể từ phiên bản cơ sở dữ liệu 2)
- **lists** - Danh sách cơ sở dữ liệu host được phân tách bằng dấu phẩy, sẽ được tìm kiếm theo thứ tự cho các truy vấn. Hầu như luôn là "privatehosts.txt,userhosts.txt,hosts.txt".
- **listversion_*** - Phiên bản của từng cơ sở dữ liệu trong lists, ví dụ: listversion_hosts.txt=4. Được sử dụng để xác định việc nâng cấp một phần hoặc bị hủy bỏ của các danh sách riêng lẻ. (kể từ phiên bản cơ sở dữ liệu 4)

### Reverse Lookup Skiplist

`%%__REVERSE__%%` là skiplist tra cứu ngược với các mục key/value Integer/Properties (từ phiên bản cơ sở dữ liệu 2):

- Các khóa skiplist là các số nguyên 4-byte, 4 byte đầu tiên của hash của [Destination](/docs/specs/common-structures/#struct-destination).
- Các giá trị skiplist mỗi cái là một Properties (một bản đồ String/String UTF-8) được tuần tự hóa như một [Mapping](/docs/specs/common-structures/#type-mapping)
  - Có thể có nhiều mục trong properties, mỗi mục là một ánh xạ ngược, vì có thể có nhiều hơn một hostname cho một destination đã cho, hoặc có thể xảy ra va chạm với cùng 4 byte đầu tiên của hash.
  - Mỗi khóa property là một hostname.
  - Mỗi giá trị property là chuỗi rỗng.

### Danh sách bỏ qua hosts.txt, userhosts.txt, và privatehosts.txt

Đối với mỗi cơ sở dữ liệu host, có một skiplist chứa các host cho cơ sở dữ liệu đó. Lưu ý rằng định dạng phiên bản 4 hỗ trợ nhiều Destination cho mỗi hostname. Định dạng này được giới thiệu trong I2P phiên bản 0.9.26. Cơ sở dữ liệu phiên bản 3 được tự động di chuyển lên phiên bản 4.

Các key/value trong những skiplist này như sau:

**key** - một chuỗi UTF-8 (tên máy chủ)

**value** - - Database phiên bản 4: Một DestEntry, là một số byte đơn chỉ định số lượng cặp Properties/Destination sẽ theo sau. Số lượng cặp đó gồm: Một Properties (một Map UTF-8 String/String) được serialize dưới dạng [Mapping](/docs/specs/common-structures/#type-mapping) theo sau bởi một [Destination](/docs/specs/common-structures/#struct-destination) nhị phân (được serialize như thường lệ). - Database phiên bản 3: một DestEntry, là một Properties (một Map UTF-8 String/String) được serialize dưới dạng [Mapping](/docs/specs/common-structures/#type-mapping) theo sau bởi một [Destination](/docs/specs/common-structures/#struct-destination) nhị phân (được serialize như thường lệ).

Thuộc tính DestEntry thường chứa:

- **"a"** - Thời gian được thêm vào (Java long time tính bằng ms)
- **"m"** - Thời gian sửa đổi lần cuối (Java long time tính bằng ms)
- **"notes"** - Bình luận do người dùng cung cấp
- **"s"** - Nguồn gốc của mục nhập (thường là tên file hoặc URL đăng ký)
- **"v"** - Nếu chữ ký của mục nhập đã được xác minh, "true" hoặc "false"

Các khóa tên máy chủ được lưu trữ ở dạng chữ thường và luôn kết thúc bằng ".i2p".

## Tài liệu tham khảo

- [Destination](/docs/specs/common-structures/#struct-destination)
- [Mapping](/docs/specs/common-structures/#type-mapping)
- [METANOTION](http://www.metanotion.net/software/sandbox/block.html)
- [NAMING](/docs/overview/naming/)
