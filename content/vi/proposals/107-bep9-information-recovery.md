---
title: "Khôi phục Thông tin BEP9"
number: "107"
author: "sponge"
created: "2011-02-23"
lastupdated: "2011-02-23"
status: "Hủy"
thread: "http://zzz.i2p/topics/860"
---

## Tổng quan

Đề xuất này nói về việc thêm tính năng khôi phục thông tin đầy đủ vào việc triển khai BEP9 của I2P.


## Động lực

BEP9 không gửi toàn bộ tập tin torrent, do đó mất đi một số mục từ điển quan trọng, và thay đổi tổng SHA1 của các tập tin torrent. Điều này không tốt cho các liên kết maggot, và không tốt vì thông tin quan trọng bị mất. Danh sách tracker, bình luận, và bất kỳ dữ liệu bổ sung nào bị mất. Một cách để khôi phục thông tin này là quan trọng, và nó cần thêm ít nhất có thể vào tập tin torrent. Nó cũng không được có sự phụ thuộc vòng tròn. Thông tin khôi phục không nên ảnh hưởng đến các client hiện tại theo bất kỳ cách nào. Những tập tin torrent không có tracker (URL tracker là 'trackerless') không chứa trường bổ sung, vì chúng cụ thể cho việc sử dụng giao thức maggot để tìm kiếm và tải về, điều này không bao giờ làm mất thông tin ngay từ đầu.


## Giải pháp

Tất cả những gì cần làm là nén thông tin sẽ bị mất đi và lưu trữ nó trong từ điển thông tin.


### Triển khai
1. Tạo từ điển thông tin bình thường.
2. Tạo từ điển chính, và bỏ qua mục thông tin.
3. Mã hóa b và nén từ điển chính với gzip.
4. Thêm từ điển chính đã nén vào từ điển thông tin.
5. Thêm thông tin vào từ điển chính.
6. Ghi tập tin torrent

### Khôi phục
1. Giải nén mục khôi phục trong từ điển thông tin.
2. Giải mã chuyển đổi từ mã b của mục khôi phục.
3. Thêm thông tin vào từ điển đã khôi phục.
4. Đối với các client có nhận thức maggot, bạn bây giờ có thể xác minh rằng SHA1 là chính xác.
5. Ghi ra tập tin torrent đã khôi phục.


## Thảo luận

Sử dụng phương pháp được nêu trên, kích thước của việc tăng tập tin torrent rất nhỏ, từ 200 đến 500 byte là điển hình. Robert sẽ phát hành với việc tạo mục từ điển thông tin mới, và không thể tắt được. Dưới đây là cấu trúc:

```
từ điển chính {
    Chuỗi tracker, bình luận, v.v...
    info : {
        từ điển đã nén b mã hóa chính trừ từ điển thông tin và tất cả thông tin thông thường khác
    }
}
```
