---
title: "Thông điệp Đặt lại cho ElGamal/AES+SessionTags"
number: "124"
author: "orignal"
created: "2016-01-24"
lastupdated: "2016-01-26"
status: "Open"
thread: "http://zzz.i2p/topics/2056"
---

## Tổng quan

Đề xuất này dành cho một thông điệp I2NP có thể sử dụng để đặt lại các thẻ phiên giữa hai Điểm Đích.

## Động lực

Hãy tưởng tượng một điểm đích có nhiều thẻ được xác nhận đối với một điểm đích khác. Nhưng điểm đích đó đã được khởi động lại hoặc bị mất những thẻ này bằng cách khác. Điểm đích đầu tiên tiếp tục gửi thông điệp với thẻ và điểm đích thứ hai không thể giải mã. Điểm đích thứ hai nên có cách để thông báo điểm đích đầu tiên đặt lại (bắt đầu từ đầu) thông qua một nhánh tỏi bổ sung, giống như khi gửi LeaseSet được cập nhật.

## Thiết kế

### Thông điệp Được Đề Xuất

Nhánh tỏi mới này phải chứa loại phân phối "destination" với một thông điệp I2NP mới gọi là "Tags reset" và chứa trường nhận diện hash của người gửi. Nó nên bao gồm dấu thời gian và chữ ký.

Có thể gửi bất cứ lúc nào nếu một điểm đích không thể giải mã thông điệp.

### Sử dụng

Nếu tôi khởi động lại router của mình và cố gắng kết nối với một điểm đích khác, tôi gửi một nhánh tỏi với LeaseSet mới của tôi, và tôi sẽ gửi thêm nhánh tỏi với thông điệp này chứa địa chỉ của tôi. Một điểm đích từ xa nhận được thông điệp này, xóa tất cả các thẻ gửi đi tới tôi và bắt đầu từ ElGamal. 

Có một trường hợp khá phổ biến là một điểm đích chỉ trong giao tiếp với một điểm đích từ xa duy nhất. Trong trường hợp khởi động lại, nó nên gửi thông điệp này tới tất cả mọi người cùng với thông điệp dòng chảy hoặc datagram đầu tiên.
