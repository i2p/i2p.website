---
title: "Tra cứu Dịch vụ"
number: "122"
author: "zzz"
created: "2016-01-13"
lastupdated: "2016-01-13"
status: "Bị từ chối"
thread: "http://zzz.i2p/topics/2048"
supercedes: "102"
supercededby: "123"
---

## Tổng quan

Đây là đề xuất toàn diện và hoành tráng về bất cứ thứ gì trong netdb. Còn được gọi là anycast. Đây sẽ là kiểu phụ LS2 thứ 4 được đề xuất.


## Động lực

Giả sử bạn muốn quảng bá điểm đích của mình như một outproxy, hoặc một nút GNS, hoặc một cổng Tor, hoặc một Bittorrent DHT hoặc imule hoặc i2phex hoặc Seedless bootstrap, v.v. Bạn có thể lưu trữ thông tin này trong netDB thay vì sử dụng một lớp khởi động hoặc thông tin riêng biệt.

Không có ai chịu trách nhiệm vì vậy không như với đa khu trú mạnh mẽ, bạn không thể có một danh sách có chữ ký xác thực. Vì vậy, bạn chỉ cần công bố bản ghi của mình tới một floodfill. Floodfill sẽ tập hợp chúng và gửi chúng như một phản hồi cho các truy vấn.


## Ví dụ

Giả sử dịch vụ của bạn là "GNS". Bạn sẽ gửi một cơ sở dữ liệu tới floodfill:

- Băm của "GNS"
- điểm đích
- dấu thời gian công bố
- hết hạn (0 để thu hồi)
- cổng
- chữ ký

Khi ai đó thực hiện tìm kiếm, họ sẽ nhận lại một danh sách các bản ghi đó:

- Băm của "GNS"
- Băm của Floodfill
- Dấu thời gian
- số lượng bản ghi
- Danh sách các bản ghi
- chữ ký của floodfill

Thời gian hết hạn sẽ tương đối dài, ít nhất vài giờ.


## Các vấn đề bảo mật

Nhược điểm là điều này có thể biến thành Bittorrent DHT hoặc tệ hơn. Ở mức tối thiểu, floodfill sẽ phải hạn chế và giới hạn nghiêm ngặt lưu trữ và truy vấn. Chúng ta có thể đưa vào danh sách trắng các tên dịch vụ được phê duyệt cho các giới hạn cao hơn. Chúng ta cũng có thể cấm hoàn toàn các dịch vụ không có trong danh sách trắng.

Tất nhiên, thậm chí netDB ngày nay cũng dễ bị lạm dụng. Bạn có thể lưu trữ dữ liệu tùy ý trong netDB, miễn là nó trông giống như một RI hoặc LS và chữ ký được xác thực. Nhưng điều này sẽ làm cho nó dễ dàng hơn rất nhiều.
