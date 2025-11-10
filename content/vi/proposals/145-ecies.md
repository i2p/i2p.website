---
title: "ECIES-P256"
number: "145"
author: "orignal"
created: "2019-01-23"
lastupdated: "2019-01-24"
status: "Open"
thread: "http://zzz.i2p/topics/2418"
---

## Động lực

ECIES-P256 nhanh hơn nhiều so với ElGamal. Đã có một số eepsites trên i2pd sử dụng loại mã hóa ECIES-P256 và Java nên có thể giao tiếp với chúng và ngược lại. i2pd đã hỗ trợ từ phiên bản 2.16.0 (0.9.32 Java).

## Tổng quan

Đề xuất này giới thiệu loại mã hóa mới ECIES-P256 có thể xuất hiện trong phần chứng nhận của danh tính, hoặc như một loại khóa mã hóa riêng biệt trong LeaseSet2.
Có thể được sử dụng trong RouterInfo, LeaseSet1 và LeaseSet2.

### Vị trí Khóa ElGamal

Để xem lại,
các khóa công khai ElGamal 256 byte có thể được tìm thấy trong các cấu trúc dữ liệu sau.
Tham khảo đặc tả cấu trúc chung.

- Trong Danh tính Router
  Đây là khóa mã hóa của bộ định tuyến.

- Trong Điểm đến
  Khóa công khai của điểm đến đã được sử dụng cho mã hóa i2cp-to-i2cp cũ
  đã bị vô hiệu trong phiên bản 0.6, hiện tại nó không được sử dụng ngoại trừ
  IV cho mã hóa LeaseSet, đã bị khai tử.
  Khóa công khai trong LeaseSet được sử dụng thay thế.

- Trong một LeaseSet
  Đây là khóa mã hóa của điểm đến.

Trong 3 trên, khóa công khai ECIES vẫn chiếm 256 byte, mặc dù độ dài khóa thực tế là 64 byte.
Phần còn lại phải được điền vào bằng chèn ngẫu nhiên.

- Trong LS2
  Đây là khóa mã hóa của điểm đến. Kích thước khóa là 64 byte.

### EncTypes trong Chứng nhận khóa

ECIES-P256 sử dụng loại mã hóa 1.
Các loại mã hóa 2 và 3 nên được dự trữ cho ECIES-P284 và ECIES-P521.

### Sử dụng Mã hóa không đối xứng

Đề xuất này mô tả thay thế ElGamal cho:

1) Thông điệp Xây dựng Đường hầm (khóa nằm trong RouterIdentity). Khối ElGamal có 512 byte

2) Mã hóa Từ đầu đến cuối của Khách hàng bằng ElGamal+AES/SessionTag (khóa nằm trong LeaseSet, khóa Điểm đến không được sử dụng). Khối ElGamal có 514 byte

3) Mã hóa nội dung netdb và các thông điệp I2NP khác giữa các bộ định tuyến. Khối ElGamal có 514 byte

### Mục tiêu

- Tương thích ngược
- Không thay đổi cấu trúc dữ liệu hiện có
- Hiệu quả CPU hơn nhiều so với ElGamal

### Phi Mục tiêu

- RouterInfo và LeaseSet1 không thể công bố ElGamal và ECIES-P256 cùng nhau

### Biện minh

Động cơ ElGamal/AES+SessionTag luôn bị kẹt do thiếu tag, điều này gây ra suy giảm hiệu suất nghiêm trọng trong truyền thông I2P.
Xây dựng đường hầm là thao tác nặng nhất vì người khởi tạo phải chạy mã hóa ElGamal 3 lần cho mỗi yêu cầu xây dựng đường hầm.

## Các nguyên thủy mã hóa yêu cầu

1) Tạo khóa đường cong P256 và DH

2) AES-CBC-256

3) SHA256

## Đề xuất chi tiết

Một điểm đến với ECIES-P256 công bố nó với loại mã hóa 1 trong chứng thực.
64 byte đầu tiên trong số 256 trong danh tính nên được hiểu là khóa công khai ECIES và phần còn lại phải bị bỏ qua.
Khóa mã hóa riêng biệt của LeaseSet được dựa trên loại khóa từ danh tính.

### Khối ECIES cho ElGamal/AES+SessionTags
Khối ECIES thay thế khối ElGamal cho ElGamal/AES+SessionTags. Độ dài là 514 byte.
Gồm hai phần mỗi phần 257 byte.
Phần đầu tiên bắt đầu với số không và sau đó là khóa công khai P256 tạm thời dài 64 byte, phần còn lại 192 byte là chèn ngẫu nhiên.
Phần thứ hai bắt đầu với số không và sau đó là AES-CBC-256 mã hóa 256 byte với cùng nội dung như trong ElGamal.

### Khối ECIES cho bản ghi xây dựng đường hầm
Bản ghi xây dựng đường hầm là tương tự, nhưng không có số không dẫn đầu trong các khối.
Một đường hầm có thể thông qua bất kỳ sự kết hợp nào của các loại mã hóa của bộ định tuyến và nó được thực hiện theo từng bản ghi.
Người khởi tạo đường hầm mã hóa các bản ghi dựa trên loại mã hóa được công bố của người tham gia đường hầm, người tham gia đường hầm giải mã dựa trên loại mã hóa của riêng mình.

### Khóa AES-CBC-256
Đây là tính toán khóa chia sẻ ECDH nơi KDF là SHA256 trên tọa độ x.
Giả sử Alice là người mã hóa và Bob là người giải mã.
Giả sử k là khóa riêng P256 tạm thời được Alice chọn ngẫu nhiên và P là khóa công khai của Bob.
S là khóa chia sẻ S(Sx, Sy)
Alice tính toán S bằng cách "đồng ý" k với P, ví dụ S = k*P.

Giả sử K là khóa công khai tạm thời của Alice và p là khóa riêng của Bob.
Bob lấy K từ khối đầu tiên của thông điệp nhận và tính toán S = p*K

Khóa mã hóa AES là SHA256(Sx) và iv là Sy.
