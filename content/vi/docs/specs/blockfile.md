---
title: "Đặc tả Blockfile"
description: "Định dạng lưu trữ blockfile (tệp khối) trên đĩa được I2P sử dụng để phân giải tên máy chủ"
slug: "blockfile"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
---

## Tổng quan

Tài liệu này đặc tả **định dạng tệp blockfile (tệp dạng khối) của I2P** và các bảng trong `hostsdb.blockfile` được sử dụng bởi **Blockfile Naming Service (dịch vụ đặt tên dựa trên blockfile)**.   Để biết bối cảnh, xem [Đặt tên và Sổ địa chỉ I2P](/docs/overview/naming).

Blockfile (tệp khối) cho phép **tra cứu destination (đích I2P) nhanh** trong một định dạng nhị phân gọn nhẹ.   So với hệ thống `hosts.txt` trước đây:

- Các Destination (đích trong I2P) được lưu ở dạng nhị phân, không phải Base64.  
- Có thể đính kèm siêu dữ liệu tùy ý (ví dụ: ngày thêm vào, nguồn, ghi chú).  
- Thời gian tra cứu xấp xỉ **nhanh hơn 10×**.  
- Mức sử dụng đĩa tăng nhẹ.

Một blockfile (tệp khối) là một tập hợp trên đĩa gồm các ánh xạ đã được sắp xếp (các cặp khóa-giá trị), được triển khai dưới dạng **skiplists** (danh sách bỏ qua). Nó được phát triển dựa trên [Metanotion Blockfile Database](http://www.metanotion.net/software/sandbox/block.html). Bản đặc tả này trước hết định nghĩa cấu trúc tệp, sau đó mô tả cách nó được `BlockfileNamingService` sử dụng.

> Blockfile Naming Service (Dịch vụ đặt tên Blockfile) đã thay thế bản triển khai `hosts.txt` cũ trong **I2P 0.8.8**.   > Khi khởi tạo, nó nhập các bản ghi từ `privatehosts.txt`, `userhosts.txt`, và `hosts.txt`.

---

## Định dạng Blockfile (tệp khối)

Định dạng gồm các **trang 1024 byte**, mỗi trang có một **magic number (chữ ký/định danh định dạng)** ở đầu để đảm bảo tính toàn vẹn.   Các trang được đánh số bắt đầu từ 1:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Page</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Superblock (starts at byte 0)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Metaindex skiplist (starts at byte 1024)</td>
    </tr>
  </tbody>
</table>
Tất cả số nguyên dùng **thứ tự byte mạng (big-endian, byte có trọng số lớn nhất đứng trước)**.   Các giá trị 2 byte là không dấu; các giá trị 4 byte (số trang) là có dấu và phải là số dương.

> **Luồng:** Cơ sở dữ liệu được thiết kế để **truy cập đơn luồng**; `BlockfileNamingService` cung cấp đồng bộ hóa.

---

### Định dạng siêu khối

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Byte</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0-5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Magic number <code>0x3141de493250</code> (<code>"1A"</code> <code>0xde</code> <code>"I2P"</code>)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">6</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Major version <code>0x01</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Minor version <code>0x02</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">8-15</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">File length (in bytes)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">16-19</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">First free list page</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">20-21</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Mounted flag (<code>0x01</code> = yes)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">22-23</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Span size (max key/value pairs per span, 16 for hostsdb)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">24-27</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Page size (as of v1.2; 1024 before that)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">28-1023</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Unused</td>
    </tr>
  </tbody>
</table>
---

### Định dạng trang khối của Skip list (danh sách bỏ qua)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Byte</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0-7</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Magic <code>0x536b69704c697374</code> (<code>"SkipList"</code>)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">8-11</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">First span page</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">12-15</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">First level page</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">16-19</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Size (total keys, valid at startup)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">20-23</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Spans (total spans, valid at startup)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">24-27</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Levels (total levels, valid at startup)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">28-29</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Span size (as of v1.2; used for new spans)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">30-1023</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Unused</td>
    </tr>
  </tbody>
</table>
---

### Định dạng trang khối của Skip Level (cấp bỏ qua)

Mỗi mức đều có một phạm vi, nhưng không phải phạm vi nào cũng có mức.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Byte</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0-7</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Magic <code>0x42534c6576656c73</code> (<code>"BSLevels"</code>)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">8-9</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Max height</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">10-11</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Current height</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">12-15</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Span page</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">16-…</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Next level pages (<code>current height</code> × 4 bytes, lowest first)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">&mdash;</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Remaining bytes unused</td>
    </tr>
  </tbody>
</table>
---

### Định dạng trang Skip Span Block

Các cặp khóa/giá trị được sắp xếp theo khóa xuyên suốt các span (vùng dữ liệu liên tiếp).   Các span không phải span đầu tiên không được rỗng.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Byte</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0-3</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Magic <code>0x5370616e</code> (<code>"Span"</code>)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4-7</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">First continuation page or 0</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">8-11</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Previous span page or 0</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">12-15</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Next span page or 0</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">16-17</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Max keys (16 for hostsdb)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">18-19</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Size (current keys)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">20-1023</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Key/value structures</td>
    </tr>
  </tbody>
</table>
---

### Định dạng trang của khối tiếp nối Span

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Byte</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0-3</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Magic <code>0x434f4e54</code> (<code>"CONT"</code>)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4-7</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Next continuation page or 0</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">8-1023</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Key/value structures</td>
    </tr>
  </tbody>
</table>
---

### Định dạng cấu trúc khóa/giá trị

Các trường độ dài của khóa và giá trị **không được vượt qua ranh giới trang** (cả 4 byte phải nằm gọn trong một trang).   Nếu không còn đủ chỗ, chèn tối đa 3 byte đệm và tiếp tục tại offset (độ lệch) 8 của trang kế tiếp.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Byte</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0-1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Key length (bytes)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2-3</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Value length (bytes)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4-…</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Key data → Value data</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">&mdash;</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Max length = 65535 bytes each</td>
    </tr>
  </tbody>
</table>
---

### Định dạng trang của khối danh sách trống

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Byte</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0-7</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Magic <code>0x2366724c69737423</code> (<code>"#frList#"</code>)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">8-11</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Next free list block or 0</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">12-15</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Number of valid free pages (0 – 252)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">16-1023</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Free page numbers (4 bytes each)</td>
    </tr>
  </tbody>
</table>
---

### Định dạng khối trang trống

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Byte</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0-7</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Magic <code>0x7e2146524545217e</code> (<code>"~!FREE!~"</code>)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">8-1023</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Unused</td>
    </tr>
  </tbody>
</table>
---

### Siêu chỉ mục

Nằm ở trang 2.   Ánh xạ **chuỗi US-ASCII** → **số nguyên 4 byte**.   Khóa là tên skiplist (cấu trúc dữ liệu danh sách bỏ qua); giá trị là chỉ mục trang.

---

## Các bảng của Dịch vụ Đặt tên Blockfile (tệp khối)

Dịch vụ định nghĩa nhiều skiplist (cấu trúc dữ liệu skiplist). Mỗi span (khoảng) hỗ trợ tối đa 16 phần tử.

---

### Skiplist (cấu trúc dữ liệu danh sách bỏ qua) của thuộc tính

`%%__INFO__%%` chứa một mục:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Key</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>info</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">A Properties object (UTF-8 String / String map) serialized as a Mapping</td>
    </tr>
  </tbody>
</table>
Các trường thường gặp:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Property</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>version</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>"4"</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>created</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Java long (ms since epoch)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>upgraded</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Java long (ms since epoch, since DB v2)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>lists</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Comma-separated host DBs (e.g. <code>privatehosts.txt,userhosts.txt,hosts.txt</code>)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>listversion_*</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Version of each DB (used to detect partial upgrades, since v4)</td>
    </tr>
  </tbody>
</table>
---

### Skiplist tra cứu ngược (cấu trúc dữ liệu dạng danh sách bỏ qua)

`%%__REVERSE__%%` chứa các mục dạng **Số nguyên → Thuộc tính** (kể từ DB v2).

- **Khóa:** 4 byte đầu tiên của hash SHA-256 của Destination (đích trong I2P).  
- **Giá trị:** đối tượng Properties (Mapping được tuần tự hóa).  
- Nhiều mục nhập để xử lý xung đột và các Destination có nhiều hostname.  
- Mỗi khóa thuộc tính = hostname; giá trị = chuỗi rỗng.

---

### Skiplists (cấu trúc dữ liệu danh sách bỏ qua) của cơ sở dữ liệu máy chủ

Mỗi tệp `hosts.txt`, `userhosts.txt` và `privatehosts.txt` ánh xạ tên máy chủ → Destinations (địa chỉ đích trong I2P).

Phiên bản 4 hỗ trợ nhiều Destinations (đích định danh trong I2P) cho mỗi tên máy chủ (được giới thiệu trong **I2P 0.9.26**).   Các cơ sở dữ liệu phiên bản 3 được chuyển đổi tự động.

#### Khóa

Chuỗi UTF-8 (tên máy chủ, chữ thường, kết thúc bằng `.i2p`)

#### Giá trị

- **Phiên bản 4:**  
  - 1 byte chỉ số lượng các cặp Thuộc tính/Đích  
  - Với mỗi cặp: Thuộc tính → Đích (nhị phân)
- **Phiên bản 3:**  
  - Thuộc tính → Đích (nhị phân)

#### Các thuộc tính DestEntry

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Key</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Meaning</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>a</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Time added (Java long ms)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>m</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Last modified (Java long ms)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>notes</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">User comments</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>s</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Source (file or subscription URL)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>v</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Signature verified (<code>true</code>/<code>false</code>)</td>
    </tr>
  </tbody>
</table>
---

## Ghi chú triển khai

Lớp Java `BlockfileNamingService` hiện thực đặc tả này.

- Bên ngoài ngữ cảnh router, cơ sở dữ liệu mở ở chế độ **chỉ đọc** trừ khi `i2p.naming.blockfile.writeInAppContext=true`.  
- Không dành cho truy cập đa thể hiện hoặc đa JVM.  
- Duy trì ba bảng ánh xạ chính (`privatehosts`, `userhosts`, `hosts`) và một bảng ánh xạ ngược để tra cứu nhanh.

---

## Tài liệu tham khảo

- [Tài liệu về Đặt tên và Sổ địa chỉ I2P](/docs/overview/naming/)  
- [Đặc tả Cấu trúc Chung](/docs/specs/common-structures/)  
- [Cơ sở dữ liệu Blockfile (tệp khối) của Metanotion](http://www.metanotion.net/software/sandbox/block.html)  
- [JavaDoc của BlockfileNamingService](https://geti2p.net/javadoc/i2p/naming/BlockfileNamingService.html)
