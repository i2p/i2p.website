---
title: "Đệm RI và Điểm đích"
number: "161"
author: "zzz"
created: "2022-09-28"
lastupdated: "2023-01-02"
status: "Open"
thread: "http://zzz.i2p/topics/3279"
target: "0.9.57"
toc: true
---

## Trạng thái

Đã triển khai trong 0.9.57. Để đề xuất này mở để chúng ta có thể cải tiến và thảo luận về các ý tưởng trong phần "Lập kế hoạch tương lai".


## Tổng quan


### Tóm tắt

Khóa công khai ElGamal trong Điểm đích đã không được sử dụng kể từ khi phát hành 0.6 (2005). Mặc dù các đặc tả của chúng tôi nói rằng nó không được sử dụng, nhưng chúng không nói rằng các triển khai có thể tránh tạo cặp khóa ElGamal và chỉ cần điền vào trường bằng dữ liệu ngẫu nhiên.

Chúng tôi đề xuất thay đổi các đặc tả để nói rằng trường này bị bỏ qua và rằng các triển khai CÓ THỂ điền vào trường bằng dữ liệu ngẫu nhiên. Sự thay đổi này tương thích ngược. Không có triển khai nào được biết đến kiểm định khóa công khai ElGamal.

Ngoài ra, đề xuất này cung cấp hướng dẫn cho các nhà triển khai về cách tạo dữ liệu ngẫu nhiên cho Đệm Điểm đích VÀ Nhận dạng Router sao cho có thể nén được trong khi vẫn đảm bảo an toàn, và mà không có biểu diễn Base 64 trông như bị lỗi hoặc không an toàn. Điều này cung cấp hầu hết các lợi ích của việc loại bỏ các trường đệm mà không có thay đổi giao thức gây gián đoạn nào. Các Điểm đích có thể nén làm giảm kích thước SYN truyền tải và kích thước datagram có thể đáp trả; Nhận dạng Router có thể nén làm giảm kích thước Thông điệp Lưu trữ Cơ sở, thông điệp Xác nhận Phiên SSU2, và các tập tin su3 tái sinh.

Cuối cùng, đề xuất thảo luận về các khả năng cho các định dạng mới của Điểm đích và Nhận dạng Router có thể loại bỏ hoàn toàn đệm. Cũng có một cuộc thảo luận ngắn gọn về mật mã sau lượng tử và cách nó có thể ảnh hưởng đến kế hoạch trong tương lai.



### Mục tiêu

- Loại bỏ yêu cầu tạo cặp khóa ElGamal cho Điểm đích
- Đề xuất thực hành tốt nhất để các Điểm đích và Nhận dạng Router có thể nén tốt,
  nhưng không hiển thị các mẫu rõ ràng trong biểu diễn Base 64.
- Khuyến khích áp dụng thực hành tốt nhất bởi tất cả các triển khai để
  các trường không thể phân biệt được
- Giảm kích thước SYN truyền tải
- Giảm kích thước datagram có thể đáp trả
- Giảm kích thước khối RI SSU2
- Giảm kích thước Xác nhận Phiên SSU2 và tần suất phân mảnh
- Giảm kích thước Thông điệp Lưu trữ Cơ sở (với RI)
- Giảm kích thước tập tin tái sinh
- Duy trì tính tương thích trong tất cả các giao thức và API
- Cập nhật đặc tả
- Thảo luận các giải pháp thay thế cho các định dạng mới của Điểm đích và Nhận dạng Router

Bằng cách loại bỏ yêu cầu tạo khóa ElGamal, các triển khai có thể
có thể loại bỏ hoàn toàn mã ElGamal, tùy thuộc vào các xem xét tính tương thích ngược
trong các giao thức khác.



## Thiết kế

Nói một cách chặt chẽ, khóa công khai ký 32 byte một mình (cả trong Điểm đích và Nhận dạng Router) và khóa công khai mã hóa 32 byte (chỉ trong Nhận dạng Router) là một số ngẫu nhiên cung cấp tất cả entropy cần thiết cho các hàm băm SHA-256 của các cấu trúc này để mạnh về mặt mật mã và phân phối ngẫu nhiên trong cơ sở dữ liệu mạng DHT.

Tuy nhiên, do sự cẩn thận quá mức, chúng tôi khuyến nghị tối thiểu 32 byte dữ liệu ngẫu nhiên được sử dụng trong trường khóa công khai ElG và đệm. Ngoài ra, nếu các trường này đều là số không, các điểm đến Base 64 sẽ chứa các chuỗi dài của các ký tự AAAA, có thể gây lo ngại hoặc nhầm lẫn cho người dùng.

Đối với loại chữ ký Ed25519 và loại mã hóa X25519: Điểm đích sẽ chứa 11 bản sao (352 byte) của dữ liệu ngẫu nhiên. Nhận dạng Router sẽ chứa 10 bản sao (320 byte) của dữ liệu ngẫu nhiên.



### Tiết kiệm Ước tính

Các điểm đích được bao gồm trong mỗi SYN truyền tải và datagram có thể đáp trả. Thông tin Router (chứa Nhận dạng Router) được bao gồm trong thông điệp Lưu trữ Cơ sở và trong các thông điệp Xác nhận Phiên trong NTCP2 và SSU2.

NTCP2 không nén Thông tin Router. RIs trong các thông điệp Lưu trữ Cơ sở và thông điệp Xác nhận Phiên SSU2 được nén gzip. Thông tin Router được nén zip trong các tập tin tái sinh SU3.

Các điểm đích trong thông điệp Lưu trữ Cơ sở không được nén. Các thông điệp SYN truyền tải được nén gzip ở lớp I2CP.

Đối với loại chữ ký Ed25519 và loại mã hóa X25519, tiết kiệm ước tính như sau:

| Loại Dữ liệu | Kích thước Tổng | Khóa và Giấy chứng nhận | Đệm chưa nén | Đệm nén | Kích thước | Tiết kiệm |
|--------------|-----------------|------------------------|--------------|---------|------------|-----------|
| Điểm đích | 391 | 39 | 352 | 32 | 71 | 320 byte (82%) |
| Nhận dạng Router | 391 | 71 | 320 | 32 | 103 | 288 byte (74%) |
| Thông tin Router | 1000 typ. | 71 | 320 | 32 | 722 typ. | 288 byte (29%) |

Ghi chú: Giả sử giấy chứng nhận dài 7 byte không thể nén, không có chi phí dữ liệu nén thêm. Không đúng hoàn toàn, nhưng ảnh hưởng sẽ nhỏ. Bỏ qua các phần khác có thể nén của Thông tin Router.



## Đặc tả

Các đề xuất thay đổi đối với các đặc tả hiện tại của chúng tôi được ghi lại bên dưới.


### Cấu trúc Chung
Thay đổi đặc tả cấu trúc chung để chỉ rõ rằng trường khóa công khai Điểm đích 256 byte bị bỏ qua và có thể chứa dữ liệu ngẫu nhiên.

Thêm một phần vào đặc tả cấu trúc chung khuyến nghị thực tiễn tốt nhất cho trường khóa công khai Điểm đích và trường đệm trong Điểm đích và Nhận dạng Router như sau:

Tạo 32 byte dữ liệu ngẫu nhiên bằng cách sử dụng máy tạo số ngẫu nhiên giả mật mã mạnh (PRNG) và lặp lại 32 byte đó khi cần thiết để lấp đầy trường khóa công khai (đối với Điểm đích) và trường đệm (đối với Điểm đích và Nhận dạng Router).

### Tệp khóa riêng
Định dạng tệp khóa riêng (eepPriv.dat) không phải là một phần chính thức của các đặc tả của chúng tôi, nhưng được tài liệu trong [Java I2P javadocs](http://idk.i2p/javadoc-i2p/net/i2p/data/PrivateKeyFile.html) và các triển khai khác có hỗ trợ. Điều này cho phép di chuyển khóa riêng giữa các triển khai khác nhau. Thêm một ghi chú vào tài liệu đó rằng khóa công khai mã hóa có thể là đệm ngẫu nhiên và khóa riêng mã hóa có thể là toàn số không hoặc dữ liệu ngẫu nhiên.

### SAM
Ghi chú trong đặc tả SAM rằng khóa riêng mã hóa không được sử dụng và có thể bị bỏ qua. Bất kỳ dữ liệu ngẫu nhiên nào cũng có thể được trả về bởi máy khách. SAM Bridge có thể gửi dữ liệu ngẫu nhiên khi tạo (với DEST GENERATE hoặc SESSION CREATE DESTINATION=TRANSIENT) thay vì toàn số không, để biểu diễn Base 64 không có chuỗi ký tự AAAA và trông như bị hỏng.


### I2CP
Không yêu cầu thay đổi đối với I2CP. Khóa riêng cho khóa công khai mã hóa trong Điểm đích không được gửi tới router.


## Lập kế hoạch tương lai


### Thay đổi Giao thức

Với chi phí thay đổi giao thức và thiếu tính tương thích ngược, chúng tôi có thể thay đổi các giao thức và đặc tả của chúng tôi để loại bỏ trường đệm trong Điểm đích, Nhận dạng Router, hoặc cả hai.

Đề xuất này có một số điểm tương đồng với định dạng leaseset mã hóa "b33", chỉ chứa khóa và trường loại.

Để duy trì một số tính tương thích, một số lớp giao thức có thể "mở rộng" trường đệm với toàn số không để trình bày cho các lớp giao thức khác.

Đối với Điểm đích, chúng tôi cũng có thể loại bỏ trường loại mã hóa trong giấy chứng nhận khóa, tiết kiệm được hai byte. Ngoài ra, các Điểm đích có thể nhận một loại mã hóa mới trong giấy chứng nhận khóa, chỉ một khóa công cộng bằng không (và đệm).

Nếu việc chuyển đổi giữa các định dạng cũ và mới không được chỉ định ở một số lớp giao thức nào đó, các đặc tả, API, giao thức, và ứng dụng sau đây sẽ bị ảnh hưởng:

- Đặc tả cấu trúc chung
- I2NP
- I2CP
- NTCP2
- SSU2
- Ratchet
- Streaming
- SAM
- Bittorrent
- Reseeding
- Tệp khóa riêng
- API lõi và router Java
- API i2pd
- Các thư viện SAM của bên thứ ba
- Các công cụ đính kèm và của bên thứ ba
- Một số plugins Java
- Giao diện người dùng
- Các ứng dụng P2P như MuWire, bitcoin, monero
- hosts.txt, sổ địa chỉ, và đăng ký

Nếu chuyển đổi được chỉ định ở một số lớp, danh sách sẽ được giảm.

Chi phí và lợi ích của những thay đổi này chưa rõ ràng.

Đề xuất cụ thể Sẽ Được Xác Định:





### Khóa PQ

Khóa công khai mã hóa Sau Lượng Tử (PQ), đối với bất kỳ thuật toán dự kiến nào, lớn hơn 256 byte. Điều này sẽ loại bỏ đệm và bất kỳ tiết kiệm nào từ các thay đổi đề xuất trên, cho các Nhận dạng Router.

Trong một cách tiếp cận PQ "lai", như những gì SSL đang thực hiện, các khóa PQ chỉ là khóa tạm thời, và sẽ không xuất hiện trong Nhận dạng Router.

Các khóa chữ ký PQ không khả thi, và các Điểm đích không chứa khóa công khai mã hóa. Các khóa tĩnh cho ratchet nằm trong Lease Set, không phải Điểm đích, vì vậy chúng tôi có thể loại bỏ các Điểm đích khỏi cuộc thảo luận sau đây.

Vì vậy, PQ chỉ ảnh hưởng đến Thông tin Router, và chỉ đối với các khóa tĩnh PQ (không phải tạm thời), không đối với PQ lai. Điều này sẽ dành cho một loại mã hóa mới và sẽ ảnh hưởng đến NTCP2, SSU2, và các Thông điệp Tra cứu Cơ sở dữ liệu mã hóa và các phản hồi. Thời gian thiết kế, phát triển và triển khai dự kiến sẽ là ???????? Nhưng sẽ sau khi lai hoặc ratchet ???????????

Để thảo luận thêm, xem [this topic](http://zzz.i2p/topics/3294).




## Vấn đề

Có thể sẽ muốn thay đổi khóa mạng với tốc độ chậm, để cung cấp bảo mật cho các router mới. "Thay đổi khóa" có thể chỉ có nghĩa là thay đổi đệm, không thực sự thay đổi các khóa.

Không thể thay đổi khóa Các Điểm đích hiện có.

Có nên xác định Nhận dạng Router với đệm trong trường khóa công khai bằng một loại mã hóa khác trong giấy chứng nhận khóa không? Điều này có thể gây ra các vấn đề tương thích.




## Di cư

Không có vấn đề tương thích ngược nào khi thay thế khóa ElGamal bằng đệm.

Việc thay đổi khóa, nếu được thực hiện, sẽ tương tự như đã được thực hiện trong ba lần chuyển đổi nhận dạng router trước đó: Từ chữ ký DSA-SHA1 chuyển sang chữ ký ECDSA, rồi chuyển sang chữ ký EdDSA, sau đó là mã hóa X25519.

Tùy thuộc vào các vấn đề tương thích ngược, và sau khi vô hiệu hóa SSU, các triển khai có thể loại bỏ hoàn toàn mã ElGamal. Khoảng 14% router trong mạng là loại mã hóa ElGamal, bao gồm nhiều floodfills.

Một yêu cầu sáp nhập nháp cho I2P Java có tại [git.idk.i2p](http://git.idk.i2p/i2p-hackers/i2p.i2p/-/merge_requests/66).
