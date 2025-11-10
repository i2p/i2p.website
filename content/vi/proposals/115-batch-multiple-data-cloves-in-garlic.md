---
title: "Đóng Gói Nhiều Tép Dữ Liệu Trong Tép Tỏi"
number: "115"
author: "orignal"
created: "2015-01-22"
lastupdated: "2015-01-22"
status: "Cần-Nghiên-Cứu"
thread: "http://zzz.i2p/topics/1797"
---

## Tổng Quan

Đề xuất này liên quan đến việc gửi nhiều tép dữ liệu bên trong một Tin Nhắn Tỏi từ điểm đầu đến điểm cuối, thay vì chỉ một tép duy nhất.

## Động Lực

Chưa rõ ràng.

## Những Thay Đổi Cần Thiết

Những thay đổi sẽ nằm trong OCMOSJ và những lớp trợ giúp liên quan, cũng như trong ClientMessagePool. Vì hiện tại không có hàng đợi, sẽ cần có một hàng đợi mới và một số độ trễ. Bất kỳ việc đóng gói nào cũng phải tuân theo kích thước tép tỏi tối đa để giảm thiểu tình trạng bị loại bỏ. Có lẽ 3KB? Sẽ muốn đo lường trước để xem việc này được sử dụng thường xuyên như thế nào.

## Suy Nghĩ

Không rõ liệu điều này sẽ có tác dụng gì hữu ích không, vì streaming đã thực hiện việc đóng gói và lựa chọn MTU tối ưu. Việc đóng gói sẽ làm tăng kích thước tin nhắn và xác suất loại bỏ theo cấp số nhân.

Ngoại lệ là nội dung không nén, được gzip tại lớp I2CP. Nhưng lưu lượng HTTP đã được nén ở lớp trên, và dữ liệu Bittorrent thường không nén được. Còn lại gì? I2pd hiện tại không thực hiện nén x-i2p-gzip nên nó có thể giúp nhiều hơn ở đó. Nhưng mục tiêu đã đưa ra nhằm không hết thẻ tốt hơn được khắc phục với việc triển khai cửa sổ đúng trong thư viện streaming của anh ta.

## Tương Thích

Điều này tương thích ngược, vì bộ nhận tỏi sẽ xử lý tất cả các tép mà nó nhận được.
