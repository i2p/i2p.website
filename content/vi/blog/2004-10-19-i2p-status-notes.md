---
title: "Ghi chú trạng thái I2P cho ngày 2004-10-19"
date: 2004-10-19
author: "jr"
description: "Cập nhật tình hình I2P hàng tuần về bản phát hành 0.4.1.3, các cải thiện hiệu năng của tunnel, tiến độ của thư viện truyền phát, và công cụ tìm kiếm files.i2p"
categories: ["status"]
---

Hi y'all, its tuesday again

## Mục lục

1. 0.4.1.3
2. Tunnel test time, and send processing time
3. Streaming lib
4. files.i2p
5. ???

## 1) 0.4.1.3

Bản phát hành 0.4.1.3 ra mắt cách đây một hai ngày và có vẻ như hầu hết mọi người đã nâng cấp (cảm ơn!). Mạng đang hoạt động khá ổn, nhưng vẫn chưa có bước nhảy vọt về độ tin cậy. Tuy nhiên, các lỗi watchdog từ 0.4.1.2 đã biến mất (hoặc ít nhất chưa ai nhắc đến chúng). Mục tiêu của tôi là bản 0.4.1.3 này sẽ là bản vá cuối cùng trước 0.4.2, tuy nhiên dĩ nhiên nếu có vấn đề lớn nào cần sửa, chúng ta sẽ có thêm một bản nữa.

## 2) Thời gian kiểm tra Tunnel, và thời gian xử lý khi gửi

Các thay đổi quan trọng nhất trong bản phát hành 0.4.1.3 là ở việc kiểm tra tunnel - thay vì có một khoảng thời gian kiểm tra cố định (30 giây!), chúng tôi có các thời gian chờ (timeout) khắt khe hơn nhiều, được xác định dựa trên hiệu năng đo được. Điều này là tốt, vì giờ đây chúng tôi đánh dấu các tunnel là lỗi khi chúng quá chậm để làm được điều gì hữu ích. Tuy nhiên, điều này cũng có mặt xấu, vì đôi khi các tunnel bị tắc nghẽn tạm thời, và nếu chúng tôi kiểm tra chúng trong khoảng thời gian đó, chúng tôi sẽ đánh dấu một tunnel là lỗi trong khi lẽ ra nó vẫn hoạt động.

Một biểu đồ gần đây về việc kiểm tra tunnel trên một router mất bao lâu:

Nhìn chung, đó là thời gian kiểm tra tunnel ổn - chúng đi qua 4 nút ngang hàng từ xa (với các tunnel 2 chặng (hop)), nên phần lớn có độ trễ khoảng ~1-200ms cho mỗi chặng. Tuy nhiên, như bạn thấy, không phải lúc nào cũng như vậy - đôi khi mất đến hàng giây cho mỗi chặng.

Đó là lúc biểu đồ tiếp theo này phát huy tác dụng - khoảng thời gian chờ trong hàng đợi từ khi một router cụ thể muốn gửi một thông điệp đến khi thông điệp đó được xả ra qua một socket:

Khoảng 95% trường hợp đều dưới 50ms, nhưng các đột biến thì khủng khiếp.

Chúng ta cần loại bỏ những đột biến đó, đồng thời tìm cách đối phó với các tình huống có nhiều peer (nút ngang hàng) bị lỗi hơn. Hiện tại, khi chúng ta 'biết' rằng một peer làm cho các tunnel của chúng ta thất bại, thực ra chúng ta không biết được điều gì cụ thể liên quan đến router của họ - những đột biến đó có thể khiến ngay cả các peer có băng thông cao cũng có vẻ chậm nếu chúng ta gặp đúng lúc.

## 3) Thư viện Streaming (truyền luồng)

Phần thứ hai của việc khắc phục các tunnel bị lỗi sẽ được thực hiện một phần bởi streaming lib (thư viện streaming) - mang lại cho chúng ta giao tiếp streaming đầu-cuối mạnh mẽ và ổn định hơn nhiều. Cuộc thảo luận này không có gì mới - lib sẽ làm tất cả những cơ chế tinh vi mà chúng ta đã bàn đến một thời gian (và dĩ nhiên nó cũng sẽ có không ít lỗi). Đã có nhiều tiến triển ở mặt này, và phần triển khai có lẽ đã đạt khoảng 60%.

Sẽ có cập nhật khi có tin mới.

## 4) files.i2p

Ok, dạo gần đây chúng ta đã có rất nhiều eepsites(I2P Sites) mới, thật là tuyệt. Mình chỉ muốn nhấn mạnh riêng trang này vì nó có một tính năng khá hay cho mọi người. Nếu bạn chưa ghé files.i2p, về cơ bản nó là một công cụ tìm kiếm giống Google, với bộ nhớ đệm (cache) các trang mà nó thu thập dữ liệu (nên bạn có thể vừa tìm kiếm vừa duyệt ngay cả khi eepsite(I2P Site) ngoại tuyến). Rất ngầu.

## 5) ???

Những ghi chú tình hình tuần này khá ngắn gọn, nhưng có rất nhiều việc đang diễn ra — tôi chỉ không có thời gian để viết thêm trước cuộc họp. Vậy nên, ghé qua #i2p trong vài phút nữa và chúng ta có thể bàn về bất cứ điều gì mà tôi đã dại dột bỏ sót.

=jr
