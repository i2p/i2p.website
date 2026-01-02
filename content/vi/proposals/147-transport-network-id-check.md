---  
title: "Kiểm Tra ID Mạng Vận Tải"  
number: "147"  
author: "zzz"  
created: "2019-02-28"  
lastupdated: "2019-08-13"  
status: "Đã Đóng"  
thread: "http://zzz.i2p/topics/2687"  
target: "0.9.42"  
implementedin: "0.9.42"  
toc: true
---

## Tổng Quan

NTCP2 (đề xuất 111) không từ chối kết nối từ các ID mạng khác nhau ở giai đoạn Yêu cầu Phiên. Kết nối hiện phải bị từ chối ở giai đoạn Phiên Đã Xác Nhận, khi Bob kiểm tra RI của Alice.

Tương tự, SSU không từ chối kết nối từ các ID mạng khác nhau ở giai đoạn Yêu cầu Phiên. Kết nối hiện phải bị từ chối sau giai đoạn Phiên Đã Xác Nhận, khi Bob kiểm tra RI của Alice.

Đề xuất này thay đổi giai đoạn Yêu cầu Phiên của cả hai phương tiện để bao gồm ID mạng theo một cách tương thích ngược.


## Động Lực

Kết nối từ mạng sai nên bị từ chối, và đồng nghiệp nên bị đưa vào danh sách đen, càng sớm càng tốt.


## Mục Tiêu

- Ngăn chặn ô nhiễm chéo giữa các mạng thử nghiệm và các mạng phân nhánh

- Thêm ID mạng vào bắt tay NTCP2 và SSU

- Đối với NTCP2, người nhận (kết nối đến) nên có khả năng xác định rằng ID mạng khác nhau, để có thể đưa IP của đồng nghiệp vào danh sách đen.

- Đối với SSU, người nhận (kết nối đến) không thể đưa vào danh sách đen ở giai đoạn yêu cầu phiên, vì IP đến có thể bị giả mạo. Việc thay đổi mật mã của bắt tay là đủ.

- Ngăn chặn tái hàm từ mạng sai

- Phải tương thích ngược


## Mục Tiêu Không Bao Gồm

- NTCP 1 không còn sử dụng, nên sẽ không bị thay đổi.


## Thiết Kế

Đối với NTCP2, việc XORing một giá trị sẽ chỉ làm cho mã hóa thất bại, và người nhận sẽ không có đủ thông tin để đưa người phát gốc vào danh sách đen, do đó cách tiếp cận đó không được ưa chuộng.

Đối với SSU, chúng ta sẽ XOR vào ID mạng ở đâu đó trong Yêu cầu Phiên. Vì điều này phải tương thích ngược, chúng ta sẽ XOR vào (id - 2) nên nó sẽ không ảnh hưởng gì đối với giá trị ID mạng hiện tại là 2.


## Đặc Tả

### Tài Liệu

Thêm đặc tả sau cho các giá trị ID mạng hợp lệ:

| Sử Dụng | Số ID Mạng |
|-------|--------------|
| Dành riêng | 0 |
| Dành riêng | 1 |
| Mạng Hiện Tại (mặc định) | 2 |
| Dành cho Mạng Tương Lai | 3 - 15 |
| Các Phân Nhánh và Mạng Thử Nghiệm | 16 - 254 |
| Dành riêng | 255 |

Cấu hình Java I2P để thay đổi mặc định là "router.networkID=nnn". Tài liệu hóa điều này tốt hơn và khuyến khích các phân nhánh và mạng thử nghiệm thêm cài đặt này vào cấu hình của họ. Khuyến khích các triển khai khác thực hiện và tài liệu hóa tùy chọn này.


### NTCP2

Sử dụng byte dành riêng đầu tiên của các tùy chọn (byte 0) trong thông điệp Yêu cầu Phiên để chứa ID mạng, hiện tại là 2. Nó chứa ID mạng. Nếu không phải số không, người nhận phải kiểm tra nó với byte ít có nghĩa nhất của ID mạng địa phương. Nếu chúng không khớp, người nhận sẽ ngay lập tức ngắt kết nối và đưa IP của nguồn gốc vào danh sách đen.


### SSU

Đối với SSU, thêm một XOR của ((netid - 2) << 8) trong tính toán HMAC-MD5.

Hiện Tại:

```text
HMAC-MD5(encryptedPayload + IV + (payloadLength ^ protocolVersion), macKey)

  '+' có nghĩa là thêm và '^' có nghĩa là exclusive-or.
  payloadLength là một số nguyên không dấu dài 2 byte
  protocolVersion là một byte 0x00
```

Mới:

```text
HMAC-MD5(encryptedPayload + IV + (payloadLength ^ protocolVersion ^ ((netid - 2) << 8)), macKey)

  '+' có nghĩa là thêm, '^' có nghĩa là exclusive-or, '<<' có nghĩa là dịch chuyển trái.
  payloadLength là một số nguyên không dấu dài hai byte, big endian
  protocolVersion là hai byte 0x0000, big endian
  netid là một số nguyên không dấu dài hai byte, big endian, các giá trị hợp pháp là 2-254
```

### Reseeding

Thêm một tham số ?netid=nnn vào việc fetch file reseed su3. Cập nhật phần mềm reseed để kiểm tra netid. Nếu nó có mặt và không bằng "2", việc fetch nên bị từ chối với mã lỗi, có thể là 403. Thêm tùy chọn cấu hình vào phần mềm reseed để có thể cấu hình một netid thay thế cho mạng thử nghiệm hoặc phân nhánh.


## Ghi Chú

Chúng ta không thể ép buộc mạng thử nghiệm và phân nhánh thay đổi ID mạng. Tốt nhất chúng ta có thể làm là tài liệu và giao tiếp. Nếu chúng ta phát hiện ô nhiễm chéo với các mạng khác, chúng ta nên cố gắng liên hệ với các nhà phát triển hoặc nhà vận hành để giải thích tầm quan trọng của việc thay đổi ID mạng.


## Các Vấn Đề


## Di Chuyển

Điều này tương thích ngược cho giá trị ID mạng hiện tại là 2. Nếu người nào đó đang chạy mạng (thử nghiệm hoặc khác) với giá trị ID mạng khác, thay đổi này sẽ không tương thích ngược. Tuy nhiên, chúng tôi không biết về bất kỳ ai làm điều này. Nếu đó chỉ là một mạng thử nghiệm, không có vấn đề gì, chỉ cần cập nhật tất cả router cùng một lúc.
