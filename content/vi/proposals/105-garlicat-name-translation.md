---
title: "Dịch Tên cho GarliCat"
number: "105"
author: "Bernhard R. Fischer"
created: "2009-12-04"
lastupdated: "2009-12-04"
status: "Chết"
thread: "http://zzz.i2p/topics/453"
---

## Tổng Quan

Đề xuất này là về việc thêm hỗ trợ tra cứu ngược DNS cho I2P.

## Cơ Chế Dịch Hiện Tại

GarliCat (GC) thực hiện dịch tên để thiết lập kết nối đến các nút GC khác. Việc dịch tên này chỉ là mã hóa lại biểu diễn nhị phân của một địa chỉ thành dạng mã hóa Base32. Do đó, quá trình dịch hoạt động hai chiều.

Những địa chỉ này được chọn để dài 80 bit. Điều này vì Tor sử dụng các giá trị dài 80 bit để định địa chỉ dịch vụ ẩn của nó. Do đó, OnionCat (là GC cho Tor) hoạt động với Tor mà không cần can thiệp thêm.

Đáng tiếc (về mặt này cho cơ chế định địa chỉ), I2P sử dụng giá trị dài 256 bit cho việc định địa chỉ dịch vụ của nó. Như đã đề cập, GC mã hóa giữa biểu diễn nhị phân và dạng mã hóa Base32. Do tính chất của GC là lớp mạng 3 VPN, trong biểu diễn nhị phân, địa chỉ được định nghĩa là địa chỉ IPv6 có tổng độ dài 128 bit. Rõ ràng, địa chỉ I2P dài 256 bit không phù hợp.

Do đó, một bước dịch tên thứ hai trở nên cần thiết:
Địa chỉ IPv6 (nhị phân) -1a-> Địa chỉ Base32 (80 bit) -2a-> Địa chỉ I2P (256 bit)
-1a- ... dịch GC
-2a- ... tra cứu hosts.txt của I2P

Giải pháp hiện tại là để trình định tuyến I2P thực hiện công việc. Điều này được thực hiện bằng cách chèn địa chỉ Base32 dài 80 bit và đích đến của nó (địa chỉ I2P) dưới dạng cặp tên/giá trị vào tệp hosts.txt hoặc privatehosts.txt của trình định tuyến I2P.

Điều này cơ bản hoạt động nhưng phụ thuộc vào dịch vụ đặt tên mà (theo ý kiến cá nhân) đang trong trạng thái phát triển và chưa đủ trưởng thành (đặc biệt là về mặt phân phối tên).

## Một Giải Pháp Có Thang Đo

Tôi đề xuất thay đổi các giai đoạn định địa chỉ về I2P (và có thể cả cho Tor) theo cách mà GC thực hiện tra cứu ngược trên các địa chỉ IPv6 bằng cách sử dụng giao thức DNS thông thường. Vùng ngược phải chứa trực tiếp địa chỉ I2P dài 256 bit trong dạng mã hóa Base32 của nó. Điều này thay đổi cơ chế tra cứu thành một bước đơn lẻ, từ đó thêm những lợi ích khác.
Địa chỉ IPv6 (nhị phân) -1b-> Địa chỉ I2P (256 bit)
-1b- ... tra cứu ngược DNS

Tra cứu DNS trong Internet được biết đến là rò rỉ thông tin về tính ẩn danh. Do đó, những tra cứu này phải được thực hiện trong I2P. Điều này ngụ ý rằng nhiều dịch vụ DNS nên có mặt trong I2P. Khi yêu cầu DNS thường được thực hiện bằng cách sử dụng giao thức UDP, bản thân GC cần thiết cho việc vận chuyển dữ liệu vì nó truyền tải các gói UDP mà I2P không tự nhiên thực hiện.

Có những lợi ích khác liên quan đến DNS:
1) Đây là một giao thức chuẩn được biết đến rộng rãi, do đó, nó liên tục được cải tiến và có nhiều công cụ (khách hàng, máy chủ, thư viện,...) tồn tại.
2) Đây là một hệ thống phân tán. Nó hỗ trợ không gian tên được lưu trữ trên nhiều máy chủ song song theo mặc định.
3) Nó hỗ trợ mã hóa (DNSSEC) cho phép xác thực các bản ghi tài nguyên. Điều này có thể được liên kết trực tiếp với khóa của một điểm đến.

## Cơ Hội Tương Lai

Có thể dịch vụ đặt tên này cũng có thể được sử dụng để thực hiện các tra cứu tiến. Đây là việc dịch các tên host thành các địa chỉ I2P và/hoặc các địa chỉ IPv6. Nhưng loại tra cứu này cần điều tra thêm vì những tra cứu này thường được thực hiện bởi thư viện giải quyết cài đặt cục bộ, sử dụng các máy chủ tên Internet thông thường (ví dụ, như được chỉ định trong /etc/resolv.conf trên các hệ thống Unix-like). Điều này khác với các tra cứu ngược của GC mà tôi đã giải thích ở trên. Một cơ hội khác có thể là địa chỉ I2P (đích đến) được đăng ký tự động khi tạo một đường hầm inbound GC. Điều này sẽ cải thiện đáng kể tính tiện dụng.
