---
title: "Giới hạn Tắc nghẽn"
number: "162"
author: "dr|z3d, idk, orignal, zzz"
created: "2023-01-24"
lastupdated: "2023-02-01"
status: "Open"
thread: "http://zzz.i2p/topics/3516"
target: "0.9.59"
toc: true
---

## Tổng quan

Thêm chỉ báo tắc nghẽn vào thông tin Router đã công bố (RI).




## Động lực

Các "giới hạn" băng thông (khả năng) chỉ ra giới hạn chia sẻ băng thông và khả năng truy cập nhưng không chỉ ra trạng thái tắc nghẽn.
Một chỉ báo tắc nghẽn sẽ giúp các router tránh cố gắng tạo đường hầm thông qua một router tắc nghẽn,
góp phần vào việc tắc nghẽn nhiều hơn và giảm thành công xây dựng đường hầm.



## Thiết kế

Định nghĩa các giới hạn mới để chỉ ra các mức tắc nghẽn hoặc vấn đề dung lượng khác nhau.
Các giới hạn này sẽ được đặt trong phần RI cấp cao nhất, không phải giới hạn địa chỉ.


### Định nghĩa Tắc nghẽn

Tắc nghẽn, nói chung, có nghĩa là đối tác không có khả năng
nhận và chấp nhận yêu cầu xây dựng đường hầm.
Làm sao để định nghĩa hoặc phân loại các mức độ tắc nghẽn là tuỳ thuộc vào từng triển khai.

Các triển khai có thể xem xét một hoặc nhiều yếu tố sau:

- Đạt hoặc gần giới hạn băng thông
- Đạt hoặc gần tối đa số đường hầm tham gia
- Đạt hoặc gần tối đa số kết nối trên một hoặc nhiều phương tiện vận chuyển
- Vượt qua ngưỡng độ sâu hàng chờ, độ trễ, hoặc sử dụng CPU; tràn hàng chờ nội bộ
- Khả năng CPU và bộ nhớ của nền tảng / hệ điều hành cơ bản
- Tắc nghẽn mạng cảm nhận được
- Trạng thái mạng như bị tường lửa hoặc NAT đối xứng hoặc ẩn hoặc proxy
- Được cấu hình không chấp nhận đường hầm

Trạng thái tắc nghẽn nên dựa trên trung bình của các điều kiện
trong vài phút, chứ không phải chỉ số đo lường tức thì.



## Đặc tả

Cập nhật [NETDB](/docs/how/network-database/) như sau:


```text
D: Tắc nghẽn trung bình, hoặc router hiệu suất thấp (ví dụ: Android, Raspberry Pi)
     Các router khác nên hạ cấp hoặc giới hạn dung lượng
     đường hầm hiện hữu trong hồ sơ của router này.

  E: Tắc nghẽn cao, router này đang gần hoặc ở một vài giới hạn,
     và đang từ chối hoặc bỏ hầu hết các yêu cầu đường hầm.
     Nếu RI này được công bố trong 15 phút qua, các router khác
     nên nghiêm túc hạ cấp hoặc giới hạn dung lượng của router này.
     Nếu RI này cũ hơn 15 phút, xử lý như 'D'.

  G: Router này đang từ chối tạm thời hoặc vĩnh viễn tất cả các đường hầm.
     Không cố gắng xây dựng đường hầm thông qua router này,
     cho đến khi nhận được RI mới không có 'G'.
```

Để đồng nhất, các triển khai nên thêm bất kỳ giới hạn tắc nghẽn nào
vào cuối (sau R hoặc U).



## Phân tích Bảo mật

Bất kỳ thông tin đối tác được công bố nào cũng không thể tin cậy.
Các giới hạn, giống như bất kỳ thứ gì khác trong Thông tin Router, có thể bị làm giả.
Chúng ta không bao giờ sử dụng bất kỳ thông tin nào trong Thông tin Router để đánh giá cao khả năng hiện có của router.

Công bố chỉ báo tắc nghẽn, cho biết đối tác tránh router này, về cơ bản
an toàn hơn rất nhiều so với các chỉ báo cho phép hoặc khả năng kêu gọi thêm nhiều đường hầm.

Các chỉ báo khả năng băng thông hiện tại (L-P, X) chỉ được tin cậy để tránh
các router có băng thông rất thấp. Giới hạn "U" (không thể truy cập được) có tác dụng tương tự.

Bất kỳ chỉ báo tắc nghẽn được công bố nào cũng nên có hiệu quả tương tự như
từ chối hoặc bỏ một yêu cầu xây dựng đường hầm, với các thuộc tính bảo mật tương tự.



## Lưu ý

Các đối tác không nên hoàn toàn tránh các router 'D', chỉ nên giảm giá trị chúng.

Cần chú ý không hoàn toàn tránh các router 'E',
vì khi toàn bộ mạng bị tắc nghẽn và công bố 'E',
mọi thứ sẽ không bị phá vỡ hoàn toàn.

Các router có thể sử dụng các chiến lược khác nhau cho loại đường hầm nào cần xây dựng thông qua các router 'D' và 'E',
ví dụ như thăm dò vs. khách hàng, hoặc khách hàng băng thông cao so với thấp.

Các router có lẽ không nên công bố một giới hạn tắc nghẽn khi khởi động hoặc tắt máy theo mặc định,
ngay cả khi trạng thái mạng của chúng không rõ, để ngăn chặn sự phát hiện khởi động lại bởi các đối tác.




## Tương thích

Không có vấn đề, tất cả các triển khai đều bỏ qua các giới hạn không xác định.


## Di cư

Các triển khai có thể thêm hỗ trợ bất kỳ lúc nào, không cần phối hợp.

Kế hoạch sơ bộ:
Công bố giới hạn trong 0.9.58 (Tháng 4 năm 2023);
thực hiện theo giới hạn đã công bố trong 0.9.59 (Tháng 7 năm 2023).



## Tham khảo

* [NETDB](/docs/how/network-database/)
