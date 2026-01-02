---
title: "Định dạng Bộ lọc Truy cập"
description: "Cú pháp cho các tệp bộ lọc kiểm soát truy cập tunnel"
slug: "filter-format"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
---

Các bộ lọc truy cập giúp người vận hành máy chủ I2PTunnel có thể cho phép, từ chối hoặc giới hạn tốc độ các kết nối đến dựa trên Destination nguồn (điểm đích I2P) và tần suất kết nối gần đây. Bộ lọc là một tệp văn bản thuần gồm các quy tắc. Tệp được đọc từ trên xuống dưới và **quy tắc khớp đầu tiên sẽ được áp dụng**.

> Các thay đổi đối với định nghĩa bộ lọc sẽ có hiệu lực **khi khởi động lại tunnel**. Một số bản dựng có thể đọc lại các danh sách dựa trên tệp trong thời gian chạy, nhưng hãy dự trù việc khởi động lại để đảm bảo các thay đổi được áp dụng.

## Định dạng tệp

- Mỗi dòng một quy tắc.  
- Các dòng trống sẽ bị bỏ qua.  
- `#` bắt đầu một chú thích kéo dài đến hết dòng.  
- Các quy tắc được đánh giá theo thứ tự; khớp đầu tiên sẽ được sử dụng.

## Ngưỡng

Một **ngưỡng** xác định số lượng lần thử kết nối từ một Destination (đích I2P) duy nhất được phép trong một cửa sổ thời gian trượt.

- **Dạng số:** `N/S` nghĩa là cho phép `N` kết nối mỗi `S` giây. Ví dụ: `15/5` cho phép tối đa 15 kết nối mỗi 5 giây. Lần thử `N+1` trong khoảng thời gian đó sẽ bị từ chối.  
- **Từ khóa:** `allow` nghĩa là không giới hạn. `deny` nghĩa là luôn từ chối.

## Cú pháp quy tắc

Các quy tắc có dạng:

```
<threshold> <scope> <target>
```
Trong đó:

- `<threshold>` là `N/S`, `allow`, hoặc `deny`  
- `<scope>` là một trong `default`, `explicit`, `file`, hoặc `record` (xem bên dưới)  
- `<target>` phụ thuộc vào phạm vi

### Quy tắc mặc định

Áp dụng khi không có quy tắc nào khác khớp. Chỉ được phép có **một** quy tắc mặc định. Nếu bị bỏ qua, các Destinations (đích đến trong I2P) chưa biết sẽ được phép mà không bị hạn chế.

```
15/5 default
allow default
deny default
```
### Quy tắc tường minh

Chỉ định một Destination (điểm đích trong I2P) cụ thể bằng địa chỉ Base32 (ví dụ `example1.b32.i2p`) hoặc khóa đầy đủ.

```
15/5 explicit example1.b32.i2p
deny explicit example2.b32.i2p
allow explicit example3.b32.i2p
```
### Quy tắc dựa trên tệp

Nhắm tới **tất cả** các Destinations (địa chỉ đích trong I2P) được liệt kê trong một tệp bên ngoài. Mỗi dòng chứa một Destination; cho phép chú thích bằng `#` và các dòng trống.

```
15/5 file /var/i2p/throttled.txt
deny file /var/i2p/blocked.txt
allow file /var/i2p/trusted.txt
```
> Lưu ý vận hành: Một số bản triển khai định kỳ đọc lại danh sách tệp. Nếu bạn chỉnh sửa một danh sách khi tunnel đang chạy, có thể sẽ có một khoảng trễ ngắn trước khi các thay đổi được ghi nhận. Khởi động lại để áp dụng ngay lập tức.

### Trình ghi (điều khiển tiệm tiến)

Một **bộ ghi** giám sát các lần thử kết nối và ghi các Destinations (đích I2P) vượt ngưỡng vào một tệp. Sau đó bạn có thể tham chiếu tệp đó trong một quy tắc `file` để áp dụng giới hạn tốc độ hoặc chặn đối với các lần thử trong tương lai.

```
# Start permissive
allow default

# Record Destinations exceeding 30 connections in 5 seconds
30/5 record /var/i2p/aggressive.txt

# Apply throttling to recorded Destinations
15/5 file /var/i2p/aggressive.txt
```
> Xác minh hỗ trợ trình ghi trong bản build của bạn trước khi dựa vào nó. Dùng danh sách `file` để đảm bảo hành vi nhất quán.

## Thứ tự đánh giá

Đặt các quy tắc cụ thể trước, rồi đến các quy tắc chung. Một mẫu thường gặp:

1. Cho phép tường minh đối với các nút ngang hàng đáng tin cậy  
2. Từ chối tường minh đối với các đối tượng lạm dụng đã biết  
3. Danh sách cho phép/từ chối dựa trên tệp  
4. Bộ ghi để giới hạn tốc độ tăng dần  
5. Quy tắc mặc định dùng để bao quát mọi trường hợp

## Ví dụ đầy đủ

```
# Moderate limits by default
30/10 default

# Always allow trusted peers
allow explicit friend1.b32.i2p
allow explicit friend2.b32.i2p

# Block known bad actors
deny file /var/i2p/blocklist.txt

# Throttle aggressive sources
15/5 file /var/i2p/throttle.txt

# Automatically populate the throttle list
60/5 record /var/i2p/throttle.txt
```
## Ghi chú triển khai

- Bộ lọc truy cập hoạt động ở lớp tunnel, trước khi ứng dụng xử lý, nên lưu lượng lạm dụng có thể bị từ chối sớm.  
- Đặt tệp bộ lọc vào thư mục cấu hình I2PTunnel của bạn và khởi động lại tunnel để áp dụng các thay đổi.  
- Chia sẻ các danh sách dựa trên tệp cho nhiều tunnel nếu bạn muốn chính sách nhất quán xuyên suốt các dịch vụ.
