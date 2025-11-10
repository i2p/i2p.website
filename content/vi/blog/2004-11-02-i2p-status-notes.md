---
title: "Ghi chú trạng thái I2P cho ngày 2004-11-02"
date: 2004-11-02
author: "jr"
description: "Bản cập nhật trạng thái I2P hàng tuần bao gồm trạng thái mạng, tối ưu hóa bộ nhớ lõi, các bản vá bảo mật cho định tuyến tunnel, tiến triển của streaming library (thư viện truyền luồng), và các phát triển liên quan đến mail/BitTorrent"
categories: ["status"]
---

Chào mọi người, đến giờ cập nhật hằng tuần rồi

## Chỉ mục:

1. Net status
2. Core updates
3. Streaming lib
4. mail.i2p progress
5. BT progress
6. ???

## 1) Trạng thái mạng

Về cơ bản vẫn như trước - số lượng peer ổn định, eepsites(I2P Sites) khá dễ truy cập, và irc hàng giờ liền. Bạn có thể xem qua khả năng truy cập của các eepsites(I2P Sites) trên một vài trang khác nhau:
- `http://gott.i2p/sites.html`
- `http://www.baffled.i2p/links.html`
- `http://thetower.i2p/pings.txt`

## 2) Cập nhật lõi

Đối với những ai đang ở trong kênh (hoặc đọc nhật ký CVS), hẳn đã thấy nhiều điều đang diễn ra, dù đã khá lâu kể từ lần phát hành trước. Danh sách đầy đủ các thay đổi kể từ bản phát hành 0.4.1.3 có thể được tìm thấy trực tuyến, nhưng có hai sửa đổi quan trọng: một tích cực và một tiêu cực:

Tin tốt là chúng tôi đã cắt giảm đáng kể tình trạng xáo trộn bộ nhớ do đủ kiểu tạo đối tượng tạm thời điên rồ gây ra. Cuối cùng tôi cũng phát ngán vì phải nhìn GC chạy điên cuồng khi gỡ lỗi thư viện streaming mới, nên sau vài ngày profiling, tinh chỉnh và tối ưu, những phần xấu xí nhất đã được dọn dẹp.

Điều không hay là một bản sửa lỗi liên quan đến cách xử lý một số thông điệp được định tuyến qua tunnel - đã có một số tình huống mà một thông điệp được gửi trực tiếp đến router đích thay vì được định tuyến qua tunnel trước khi chuyển giao, điều này có thể bị kẻ tấn công biết lập trình một chút lợi dụng. Giờ đây, khi còn nghi ngờ, chúng tôi sẽ định tuyến qua tunnel đúng cách.

Nghe có vẻ hay, nhưng phần 'bad' là điều đó đồng nghĩa sẽ có độ trễ tăng lên đôi chút do các hop (bước nhảy qua nút trung gian) bổ sung, mặc dù những hop này vốn dĩ vẫn phải được sử dụng.

Cũng đang có các hoạt động gỡ lỗi khác diễn ra trong phần lõi, nên hiện vẫn chưa có bản phát hành chính thức - CVS HEAD là 0.4.1.3-8. Trong vài ngày tới, có lẽ chúng tôi sẽ phát hành 0.4.1.4, chỉ để giải quyết hết những hạng mục đó. Tất nhiên, nó sẽ không bao gồm streaming lib (thư viện truyền luồng) mới.

## 3) Thư viện truyền luồng

Nhắc đến streaming lib (thư viện streaming), đã có rất nhiều tiến triển, và việc so sánh song song giữa các thư viện cũ và mới trông rất khả quan. Tuy vậy, vẫn còn việc phải làm, và như tôi đã nói lần trước, chúng tôi sẽ không vội vàng tung nó ra. Điều đó có nghĩa là lộ trình đã bị lùi, có lẽ trong khoảng 2–3 tuần. Sẽ có thêm chi tiết khi có sẵn.

## 4) tiến triển của mail.i2p

Rất nhiều thứ mới trong tuần này - các proxy vào và ra đang hoạt động! Xem www.postman.i2p để biết thêm thông tin.

## 5) Tiến độ BT

Gần đây đã có một loạt hoạt động sôi nổi liên quan đến việc port một trình khách BitTorrent, cũng như cập nhật một số thiết lập của tracker (máy theo dõi). Có lẽ chúng ta có thể nhận được một vài cập nhật từ những người liên quan trong cuộc họp.

## 6) ???

Vậy là xong phần của tôi. Xin lỗi vì chậm trễ, tôi quên mất cái vụ đổi giờ mùa hè. Dù sao, gặp mọi người chút nữa nhé.

=jr
