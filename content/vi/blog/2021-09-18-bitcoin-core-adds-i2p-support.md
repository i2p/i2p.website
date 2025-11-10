---
title: "Bitcoin Core bổ sung hỗ trợ cho I2P!"
date: 2021-09-18
author: "idk"
description: "Một trường hợp sử dụng mới và một tín hiệu cho thấy sự chấp nhận ngày càng rộng rãi"
categories: ["general"]
---

Một sự kiện được chuẩn bị trong nhiều tháng, Bitcoin Core đã bổ sung hỗ trợ chính thức cho I2P! Các nút Bitcoin-over-I2P có thể tương tác đầy đủ với phần còn lại của các nút Bitcoin, nhờ sự hỗ trợ của các nút hoạt động trong cả I2P và clearnet (mạng Internet công khai), khiến chúng trở thành những thành phần ngang hàng, chính thức trong mạng lưới Bitcoin. Thật đáng mừng khi thấy các cộng đồng lớn như Bitcoin chú ý đến những lợi ích mà I2P có thể mang lại cho họ, cung cấp quyền riêng tư và khả năng tiếp cận cho mọi người trên khắp thế giới.

## Cách hoạt động

Hỗ trợ I2P là tự động, thông qua SAM API. Đây cũng là một tin đáng mừng, vì nó làm nổi bật một số điểm mà I2P đặc biệt mạnh, như việc trao quyền cho các nhà phát triển ứng dụng xây dựng các kết nối I2P một cách lập trình và thuận tiện. Người dùng Bitcoin-over-I2P có thể sử dụng I2P mà không cần cấu hình thủ công bằng cách bật SAM API và chạy Bitcoin với I2P được kích hoạt.

## Cấu hình router I2P của bạn

Để thiết lập một I2P Router nhằm cung cấp kết nối ẩn danh đến bitcoin, cần bật SAM API. Trong Java I2P, bạn nên truy cập http://127.0.0.1:7657/configclients và khởi động SAM Application Bridge bằng nút "Start". Bạn cũng có thể bật SAM Application Bridge theo mặc định bằng cách chọn hộp "Run at Startup" và nhấp "Save Client Configuration."

Trên i2pd, SAM API thường được bật theo mặc định, nhưng nếu không thì bạn nên thiết lập:

```
sam.enabled=true
```
trong tệp i2pd.conf của bạn.

## Cấu hình nút Bitcoin của bạn cho ẩn danh và kết nối

Để chạy Bitcoin ở chế độ ẩn danh, bạn vẫn cần chỉnh sửa một số tệp cấu hình trong Bitcoin Data Directory, đó là %APPDATA%\Bitcoin trên Windows, ~/.bitcoin trên Linux, và ~/Library/Application Support/Bitcoin/ trên Mac OSX. Ngoài ra, cần ít nhất phiên bản 22.0.0 để có hỗ trợ I2P.

Sau khi làm theo các hướng dẫn này, bạn sẽ có một nút Bitcoin riêng tư sử dụng I2P cho các kết nối I2P, và Tor cho các kết nối .onion và clearnet, để tất cả các kết nối của bạn đều ẩn danh. Để thuận tiện, người dùng Windows nên mở Thư mục Dữ liệu Bitcoin của mình bằng cách mở menu Start và tìm kiếm "Run." Bên trong hộp thoại Run, nhập "%APPDATA%\Bitcoin" và nhấn Enter.

Trong thư mục đó, hãy tạo một tệp có tên "i2p.conf." Trên Windows, bạn cần đảm bảo rằng bạn đã thêm dấu ngoặc kép quanh tên tệp khi lưu, để ngăn Windows tự động thêm phần mở rộng tệp mặc định. Tệp này nên chứa các tùy chọn cấu hình Bitcoin liên quan đến I2P sau đây:

```
i2psam=127.0.0.1:7656
i2pacceptincoming=true
onlynet=i2p
```
Tiếp theo, bạn nên tạo một tệp khác có tên "tor.conf." Tệp này nên chứa các tùy chọn cấu hình liên quan đến Tor sau:

```
proxy=127.0.0.1:9050
onion=127.0.0.1:9050
onlynet=tor
```
Cuối cùng, bạn sẽ cần "thêm" các tùy chọn cấu hình này vào tệp cấu hình Bitcoin của bạn, có tên là "bitcoin.conf" trong Thư mục Dữ liệu. Thêm hai dòng sau vào tệp bitcoin.conf của bạn:

```
includeconf=i2p.conf
includeconf=tor.conf
```
Bây giờ nút Bitcoin của bạn đã được cấu hình để chỉ sử dụng các kết nối ẩn danh. Để bật các kết nối trực tiếp tới các nút từ xa, hãy xóa các dòng bắt đầu bằng:

```
onlynet=
```
Bạn có thể làm điều này nếu bạn không yêu cầu nút Bitcoin của mình phải ẩn danh, và việc này giúp người dùng ẩn danh kết nối với phần còn lại của mạng lưới Bitcoin.
