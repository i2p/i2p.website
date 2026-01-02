---
title: "BOB – Basic Open Bridge (Cầu mở cơ bản)"
description: "API đã lỗi thời để quản lý điểm đến (đã lỗi thời)"
slug: "bob"
lastUpdated: "2025-05"
layout: "single"
reviewStatus: "needs-review"
---

> **Cảnh báo:** BOB chỉ hỗ trợ kiểu chữ ký DSA-SHA1 cũ. Java I2P đã ngừng phát hành kèm BOB từ **1.7.0 (2022-02)**; nó chỉ còn trên các cài đặt được khởi tạo từ 1.6.1 hoặc cũ hơn và trên một số bản dựng i2pd. Các ứng dụng mới **bắt buộc** phải dùng [SAM v3](/docs/api/samv3/).

## Ràng buộc ngôn ngữ

- Go – [ccondom](https://bitbucket.org/kallevedin/ccondom)
- Python – [`i2py-bob`](http://git.repo.i2p/w/i2py-bob.git)
- Twisted – [`txi2p`](https://pypi.python.org/pypi/txi2p)
- C++ – [`bobcpp`](https://gitlab.com/rszibele/bobcpp)

## Ghi chú về giao thức

- `KEYS` biểu thị một destination (địa chỉ đích trong I2P) dạng base64 (khóa công khai + khóa riêng tư).  
- `KEY` là một khóa công khai dạng base64.  
- Phản hồi `ERROR` có dạng `ERROR <description>\n`.  
- `OK` cho biết lệnh đã hoàn tất; dữ liệu tùy chọn theo sau trên cùng một dòng.  
- Các dòng `DATA` truyền thêm đầu ra trước `OK` cuối cùng.

Lệnh `help` là ngoại lệ duy nhất: nó có thể không trả về gì để báo hiệu “không có lệnh như vậy”.

## Biểu ngữ kết nối

BOB sử dụng các dòng ASCII kết thúc bằng ký tự newline (LF hoặc CRLF). Khi kết nối, nó gửi ra:

```
BOB <version>
OK
```
Phiên bản hiện tại: `00.00.10`. Các bản dựng trước đây sử dụng các chữ số thập lục phân viết hoa và cách đánh số không theo chuẩn.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">BOB Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Router Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">00.00.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.8</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Latest defined version</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">00.00.00 – 00.00.0F</td><td style="border:1px solid var(--color-border); padding:0.5rem;">—</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Development builds</td></tr>
  </tbody>
</table>
## Các lệnh cốt lõi

> Để xem đầy đủ chi tiết về các lệnh, hãy kết nối bằng `telnet localhost 2827` và chạy `help`.

```
COMMAND     OPERAND                               RETURNS
help        [command]                             NOTHING | OK <info>
clear                                             ERROR | OK
getdest                                           ERROR | OK <KEY>
getkeys                                           ERROR | OK <KEYS>
getnick     <tunnelname>                          ERROR | OK
inhost      <hostname | IP>                       ERROR | OK
inport      <port>                                ERROR | OK
list                                              ERROR | DATA... + OK
lookup      <hostname>                            ERROR | OK <KEY>
nick        <friendlyname>                        ERROR | OK
outhost     <hostname | IP>                       ERROR | OK
outport     <port>                                ERROR | OK
quit                                              ERROR | OK
setkey      <base64 destination>                  ERROR | OK
start                                             ERROR | OK
status                                            ERROR | DATA... + OK
stop                                              ERROR | OK
```
## Tóm tắt ngừng hỗ trợ

- BOB (giao thức cầu nối ứng dụng cũ của I2P) không hỗ trợ các kiểu chữ ký hiện đại, LeaseSets (bộ mô tả đích trong I2P) được mã hóa, hoặc các tính năng truyền tải.
- API hiện đang đóng băng; sẽ không bổ sung lệnh mới nào.
- Các ứng dụng vẫn còn phụ thuộc vào BOB nên chuyển sang SAM v3 (giao thức API máy khách của I2P) càng sớm càng tốt.
