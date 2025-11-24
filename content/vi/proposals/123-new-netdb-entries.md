---
title: "Các Mục Mới Trong netDB"
number: "123"
author: "zzz, str4d, orignal"
created: "2016-01-16"
lastupdated: "2020-07-18"
status: "Open"
thread: "http://zzz.i2p/topics/2051"
supercedes: "110, 120, 121, 122"
---

## Tình Trạng

Một phần của đề xuất này đã hoàn thành và triển khai trong 0.9.38 và 0.9.39. 
Các Cấu Trúc Chung, I2CP, I2NP, và các đặc tả khác
đã được cập nhật để phản ánh các thay đổi hiện đang được hỗ trợ.

Các phần đã hoàn thành vẫn còn có thể điều chỉnh nhỏ. 
Các phần khác của đề xuất này vẫn đang trong quá trình phát triển
và vẫn có thể điều chỉnh đáng kể.

Service Lookup (loại 9 và 11) là ưu tiên thấp và chưa có kế hoạch, 
có thể được tách ra thành một đề xuất riêng.


## Tổng Quan

Đây là một bản cập nhật và tổng hợp của 4 đề xuất sau:

- 110 LS2
- 120 Meta LS2 cho multihoming lớn
- 121 LS2 mã hóa
- 122 Tra cứu dịch vụ không xác thực

Những đề xuất này phần lớn độc lập, nhưng để đảm bảo tính hợp lý, chúng tôi định nghĩa và sử dụng một cấu trúc chung cho một số trong chúng.

Các đề xuất sau có liên quan một phần:

- 140 Multihoming vô hình (không tương thích với đề xuất này)
- 142 Mẫu Crypto mới (cho crypto đối xứng mới)
- 144 ECIES-X25519-AEAD-Ratchet
- 145 ECIES-P256
- 146 Red25519
- 148 EdDSA-BLAKE2b-Ed25519
- 149 B32 cho LS2 mã hóa
- 150 Giao Thức Cánh Đồng Tỏi
- 151 Che giấu ECDSA


## Đề Xuất

Đề xuất này định nghĩa 5 loại DatabaseEntry mới và quá trình
lưu trữ chúng vào và truy xuất từ cơ sở dữ liệu mạng,
cũng như phương pháp để ký chúng và xác minh các chữ ký đó.

### Mục Tiêu

- Tương thích ngược lại
- LS2 Sử dụng được với multihoming kiểu cũ
- Không yêu cầu crypto mới hoặc phần tử cơ bản mới để hỗ trợ
- Duy trì việc phân tách giữa crypto và ký; hỗ trợ tất cả các phiên bản hiện tại và tương lai
- Cho phép các khóa ký ngoại tuyến tùy chọn
- Giảm độ chính xác của dấu thời gian để giảm dấu vân tay
- Cho phép crypto mới cho các điểm đích
- Cho phép multihoming lớn
- Sửa nhiều vấn đề với LS mã hóa hiện có
- Che dấu tùy chọn để giảm tầm nhìn bởi các floodfills
- Mã hóa hỗ trợ cả khóa đơn và nhiều khóa có thể thu hồi
- Tra cứu dịch vụ để đơn giản hóa việc tra cứu các outproxies, khởi động DHT ứng dụng, và các mục đích khác
- Không làm hỏng bất cứ thứ gì hoạt động dựa vào các hàm băm điểm đến 32-byte nhị phân, ví dụ: bittorrent
- Thêm tính linh hoạt cho leaseset thông qua thuộc tính, tương tự như trong routerinfos.
- Đặt dấu thời gian công bố và quá hạn biến đổi trong tiêu đề, để nó hoạt động ngay cả khi nội dung được mã hóa (không lấy dấu thời gian từ lease sớm nhất)
- Tất cả các loại mới nằm trong cùng một không gian DHT và vị trí giống như các leaseset hiện tại, để người dùng có thể di chuyển từ LS cũ sang LS2, hoặc thay đổi giữa LS2, Meta, và Mã hóa, mà không thay đổi Đích đến hoặc hàm băm.
- Một Điểm đến hiện có có thể được chuyển đổi để sử dụng khóa ngoại tuyến, hoặc quay lại khóa trực tuyến, mà không thay đổi Điểm đến hoặc hàm băm.


### Không Phải Mục Tiêu / Ngoài Phạm Vi

- Thuật toán xoay DHT mới hoặc tạo ngẫu nhiên chia sẻ
- Loại mã hóa cụ thể mới và sơ đồ mã hóa đầu-cuối
  sử dụng loại mới đó sẽ nằm trong một đề xuất riêng. Không có mã hóa mới nào được chỉ định hoặc thảo luận ở đây.
- Mã hóa mới cho RIs hoặc xây dựng đường hầm.
  Điều đó sẽ nằm trong một đề xuất riêng.
- Phương pháp mã hóa, truyền tải, và nhận tin nhắn I2NP DLM / DSM / DSRM.
  Không thay đổi.
- Cách để tạo ra và hỗ trợ Meta, bao gồm giao tiếp trên các router phía sau, quản lý, dự phòng và phối hợp.
  Hỗ trợ có thể được thêm vào I2CP, hoặc i2pcontrol, hoặc một giao thức mới.
  Điều này có thể hoặc không được tiêu chuẩn hóa.
- Làm thế nào để thực thi và quản lý đường hầm kéo dài lâu hơn, hoặc hủy bỏ các đường hầm hiện tại.
  Điều này vô cùng khó khăn, và không có nó, bạn không thể có một tắt máy hợp lý.
- Thay đổi mô hình đe dọa
- Định dạng lưu trữ ngoại tuyến, hoặc phương pháp để lưu trữ / truy xuất / chia sẻ dữ liệu.
- Chi tiết thực hiện không được thảo luận ở đây và để cho từng dự án tự xử lý.

### Lý Do

LS2 thêm các trường để thay đổi loại mã hóa và cho các thay đổi giao thức trong tương lai.

LS2 mã hóa sửa chữa một số vấn đề bảo mật với LS mã hóa hiện tại bằng cách
sử dụng mã hóa bất đối xứng của toàn bộ bộ lease.

Meta LS2 cung cấp khả năng multihoming linh hoạt, hiệu quả, hiệu suất, và quy mô lớn.

Ghi Nhớ Dịch Vụ và Danh Sách Dịch Vụ cung cấp các dịch vụ anycast chẳng hạn như tra cứu tên và khởi động DHT.


### Loại Dữ Liệu NetDB

Các số loại được sử dụng trong I2NP Database Lookup/Store Messages.

Cột end-to-end đề cập đến việc liệu các truy vấn/phản hồi
có được gửi đến một Đích đến trong một Tin nhắn Garlic hay không.


Loại hiện có:

            Dữ Liệu NetDB               Lookup Type   Store Type 
any                                       0           any     
LS                                        1            1      
RI                                        2            0      
exploratory                               3           DSRM    

Loại mới:

            Dữ Liệu NetDB               Lookup Type   Store Type   Std. LS2 Header?   Sent end-to-end?
LS2                                       1            3             yes                 yes
LS2 Mã hóa                                1            5             no                  no
Meta LS2                                  1            7             yes                 no
Ghi Nhớ Dịch Vụ                          n/a          9             yes                 no
Danh Sách Dịch Vụ                         4           11             no                  no


Ghi Chú
`````
- Các loại truy vấn hiện là các bit 3-2 trong Tin nhắn Tìm Kiếm Cơ Sở Dữ Liệu.
  Bất kỳ loại bổ sung nào sẽ yêu cầu sử dụng của bit 4.

- Tất cả các loại lưu trữ đều là lẻ vì các bit trên trong trường loại Tin nhắn Lưu Cơ Sở Dữ Liệu
  bị bỏ qua bởi các router cũ.
  Chúng tôi thà để trình phân tích thất bại dưới dạng LS hơn là dưới dạng RI nén.

- Có nên Nhập xuất hay Ẩn định rõ ràng trong dữ liệu bị xử lý bởi chữ ký không?


### Quá Trình Lookup/Store

Các loại 3, 5, và 7 có thể được trả về để đáp ứng một yêu cầu tìm kiếm leaseset tiêu chuẩn (loại 1).
Loại 9 không bao giờ được trả về để đáp ứng một tìm kiếm.
Loại 11 là phản hồi cho một loại tìm kiếm dịch vụ mới (loại 11).

Chỉ loại 3 có thể được gửi trong một tin nhắn Garlic từ khách hàng đến khách hàng.


### Định Dạng

Các loại 3, 7, và 9 đều có một định dạng chung::

  Tiêu Đề LS2 Chuẩn
  - như được định nghĩa dưới đây

  Phần Cụ Thể Loại
  - như được định nghĩa trong từng phần bên dưới

  Chữ Ký LS2 Chuẩn:
  - Độ dài như ngụ ý bởi loại chữ ký của khóa ký

Loại 5 (Mã hóa) không bắt đầu với một Đích Đến và có một định dạng khác nhau. Xem bên dưới.

Loại 11 (Danh Sách Dịch Vụ) là một tập hợp của một số Ghi Nhớ Dịch Vụ và có một định dạng khác nhau. Xem bên dưới.


### Các Cân Nhắc Về Quyền Riêng Tư/Bảo Mật

TBD



## Tiêu Đề LS2 Chuẩn

Các loại 3, 7, và 9 sử dụng tiêu đề LS2 chuẩn, như chỉ định dưới đây:


### Định Dạng
::

  Tiêu đề LS2 Chuẩn:
  - Loại (1 byte)
    Không thực tế trong tiêu đề, nhưng là một phần của dữ liệu được xử lý bởi chữ ký.
    Lấy từ trường trong Tin nhắn Lưu trữ trong Cơ Sở Dữ Liệu.
  - Destination (387+ bytes)
  - Dấu thời gian công bố (4 bytes, big endian, giây kể từ kỷ nguyên, kết thúc trong 2106)
  - Hết hạn (2 bytes, big endian) (offset từ dấu thời gian công bố tính bằng giây, tối đa 18.2 giờ)
  - Cờ (2 bytes)
    Thứ tự bit: 15 14 ... 3 2 1 0
    Bit 0: Nếu 0, không có khóa ngoại tuyến; nếu 1, có khóa ngoại tuyến
    Bit 1: Nếu 0, một leaseset đã công bố tiêu chuẩn.
           Nếu 1, một leaseset chưa công bố. Không nên được phổ biến, công bố, hoặc
           gửi để phản hồi một truy vấn. Nếu leaseset này hết hạn, không truy vấn
           netdb cho một cái mới, trừ khi bit 2 được đặt.
    Bit 2: Nếu 0, một leaseset đã công bố tiêu chuẩn.
           Nếu 1, leaseset không mã hóa này sẽ được che dấu và mã hóa khi được công bố.
           Nếu leaseset này hết hạn, truy vấn vị trí bị che dấu trong netdb cho một cái mới.
           Nếu bit này được đặt thành 1, thiết lập bit 1 cũng thành 1.
           Kể từ phiên bản phát hành 0.9.42.
    Bits 3-15: đặt thành 0 để tương thích với các mục đích sử dụng trong tương lai
  - Nếu cờ chỉ ra khóa ngoại tuyến, phần chữ ký ngoại tuyến:
    Dấu thời gian hết hạn (4 bytes, big endian, giây kể từ kỷ nguyên, kết thúc trong 2106)
    Loại chữ ký chuyển tiếp (2 bytes, big endian)
    Khóa công khai ký chuyển tiếp (độ dài như ngụ ý bởi loại chữ ký)
    Chữ ký của dấu thời gian hết hạn, loại chữ ký chuyển tiếp, và khóa công khai,
    bằng khóa công khai của điểm đích,
    độ dài như ngụ ý bởi loại chữ ký của khóa điểm đích công khai.
    Phần này có thể, và nên, được tạo ngoại tuyến.


Lý Do
`````````````

- Không xuất bản / đã xuất bản: Để sử dụng khi gửi một lưu trữ cơ sở dữ liệu end-to-end,
  router gửi có thể muốn chỉ ra rằng leaseset này không nên
  được gửi cho những người khác. Hiện tại chúng tôi sử dụng các cách suy đoán để duy trì trạng thái này.

- Công bố: Thay thế logic phức tạp cần thiết để xác định 'phiên bản' của
  leaseset. Hiện tại, phiên bản là thời gian hết hạn của lease hết hạn cuối cùng,
  và một router công bố phải tăng cái hết hạn đó ít nhất 1ms khi
  công bố một leaseset chỉ loại bỏ một lease cũ hơn.

- Hết hạn: Cho phép hết hạn của một mục netdb sớm hơn so với
  lease cuối cùng hết hạn của nó. Có thể không hữu ích cho LS2, nơi leaseset
  dự kiến sẽ duy trì với thời gian hết hạn tối đa 11 phút, nhưng
  cho các loại mới khác, nó là cần thiết (xem Meta LS và Ghi Nhớ Dịch Vụ dưới đây).

- Khóa ngoại tuyến là tùy chọn, để giảm độ phức tạp / yêu cầu thực thi ban đầu.


### Vấn Đề

- Có thể giảm độ chính xác của dấu thời gian thậm chí nhiều hơn (10 phút?) nhưng sẽ phải thêm
  số phiên bản. Điều này có thể phá vỡ multihoming, trừ khi chúng ta có mã hóa bảo quản thứ tự?
  Có lẽ không thể làm mà không có dấu thời gian nào cả.

- Lựa chọn thay thế: dấu thời gian 3 byte (epoch / 10 phút), phiên bản 1 byte, hết hạn 2 byte

- Loại là rõ ràng hay ngấm ngầm trong dữ liệu / chữ ký? Hằng "Domain" cho chữ ký?


Ghi Chú
`````

- Router không nên công bố một LS nhiều hơn một lần một giây.
  Nếu chúng làm, chúng phải tăng dấu thời gian công bố lên 1
  so với LS đã công bố trước đó.

- Các thực thi router có thể lưu trữ các khóa chuyển tiếp và chữ ký để
  tránh xác minh mỗi lần. Đặc biệt, floodfills, và các router ở
  cả hai đầu của các kết nối kéo dài, có thể lợi ích từ điều này.

- Khóa và chữ ký ngoại tuyến chỉ thích hợp cho các đích lâu dài,
  tức là máy chủ, không phải là khách hàng.



## Các Loại DatabaseEntry Mới


### LeaseSet 2

Thay đổi từ LeaseSet hiện có:

- Thêm dấu thời gian công bố, dấu thời gian hết hạn, cờ, và thuộc tính
- Thêm loại mã hóa
- Loại bỏ khóa thu hồi

Tra cứu với
    Cờ LS tiêu chuẩn (1)
Lưu trữ với
    Loại LS2 tiêu chuẩn (3)
Lưu trữ tại
    Hàm băm của đích đến
    Hàm băm này sau đó được sử dụng để tạo "khóa định tuyến" hàng ngày, như trong LS1
Thời hạn hết hạn điển hình
    10 phút, như trong một LS tiêu chuẩn.
Công bố bởi
    Điểm đến

Định dạng
``````
::

  Tiêu đề LS2 Chuẩn như được chỉ định ở trên

  Phần Cụ Thể Loại LS2 Chuẩn
  - Thuộc tính (Mapping như được chỉ định trong đặc tả cấu trúc chung, 2 bytes zero nếu không có)
  - Số lượng các phần khóa theo sau (1 byte, tối đa TBD)
  - Các phần khóa:
    - Loại mã hóa (2 bytes, big endian)
    - Độ dài của khóa mã hóa (2 bytes, big endian)
      Điều này là rõ ràng, do đó các floodfills có thể phân tích LS2 với các loại mã hóa không xác định.
    - Khóa mã hóa (số bytes đã chỉ định)
  - Số lượng lease2s (1 byte)
  - Lease2s (mỗi cái 40 bytes)
    Đây là các leases, nhưng với một hết hạn 4 byte thay vì 8 byte,
    giây từ epoch (kết thúc trong 2106)

  Chữ Ký LS2 Chuẩn:
  - Chữ ký
    Nếu cờ chỉ ra khóa ngoại tuyến, thì điều này được ký bởi chuyển tiếp pubkey,
    ngược lại, bởi đích đến pubkey
    Độ dài như ngụ ý bởi loại chữ ký của khóa ký
    Chữ ký là của tất cả mọi thứ ở trên.




Lý Do
`````````````

- Thuộc tính: Mở rộng và linh hoạt trong tương lai.
  Đặt trước để tránh cần thiết cho việc phân tích dữ liệu còn lại.

- Nhiều cặp loại mã hóa/khóa công khai là
  để dễ dàng chuyển đổi sang các loại mã hóa mới. Cách khác để làm điều đó
  là xuất bản nhiều leaseset, có thể sử dụng cùng các đường hầm,
  như chúng tôi hiện đang làm cho đích DSA và EdDSA.
  Việc xác định loại mã hóa đến trên một đường hầm
  có thể được thực hiện với cơ chế thẻ phiên hiện tại,
  và/hoặc giải mã thử nghiệm sử dụng từng khóa. Độ dài của các
  tin nhắn đến có thể cung cấp một manh mối.

Thảo luận
``````````

Đề xuất này tiếp tục sử dụng khóa công khai trong leaseset cho
khóa mã hóa đầu-cuối, và để lại trường khóa công khai trong
đích đến không sử dụng, như hiện tại. Loại mã hóa không được chỉ định
trong khóa chứng chỉ đích đến, nó vẫn sẽ là 0.

Một lựa chọn bị từ chối là chỉ định loại mã hóa trong khóa chứng chỉ đích đến,
sử dụng khóa công khai trong Đích đến, và không sử dụng khóa công khai
trong leaseset. Chúng tôi không dự định làm điều này.

Lợi ích của LS2:

- Vị trí của khóa công khai thực tế không thay đổi.
- Loại mã hóa, hoặc khóa công khai, có thể thay đổi mà không thay đổi Đích đến.
- Gỡ bỏ trường thu hồi không sử dụng
- Khả năng tương thích cơ bản với các loại DatabaseEntry khác trong đề xuất này
- Cho phép nhiều loại mã hóa

Hạn chế của LS2:

- Vị trí của khóa công khai và loại mã hóa khác với RouterInfo
- Duy trì khóa công khai không sử dụng trong leaseset
- Yêu cầu thực hiện trên toàn mạng; trong lựa chọn khác, các
  loại mã hóa thử nghiệm có thể được sử dụng, nếu được phép bởi floodfills
  (nhưng xem đề xuất liên quan 136 và 137 về hỗ trợ các loại chữ ký thử nghiệm).

Các Vấn Đề Về Mã Hóa Mới
```````````````````````
Một số phần trong số này nằm ngoài phạm vi đề xuất này,
nhưng ghi chú ở đây vào thời điểm hiện tại do chúng tôi chưa có
một đề xuất mã hóa riêng biệt.
Xem thêm các đề xuất ECIES 144 và 145.

- Loại mã hóa đại diện cho sự kết hợp
  của đường cong, chiều dài khóa, và sơ đồ đầu-cuối,
  bao gồm KDF và MAC, nếu có.

- Chúng tôi đã bao gồm một trường chiều dài khóa, do đó LS2
  có thể phân tích và xác minh bởi floodfill ngay cả đối với các loại mã hóa không xác định.

- Loại mã hóa mới đầu tiên có thể được đề xuất có lẽ là ECIES/X25519. Cách nó
  được sử dụng đầu-cuối (hoặc một phiên bản sửa đổi nhẹ của ElGamal/AES+SessionTag
  hoặc một cái gì đó hoàn toàn mới, ví dụ ChaCha/Poly) sẽ được chỉ định
  trong một hoặc nhiều đề xuất riêng biệt.
  Xem thêm các đề xuất ECIES 144 và 145.

Ghi Chú
`````
- Hết hạn 8-byte trong leases thay đổi thành 4-byte.

- Nếu chúng tôi từng triển khai thu hồi, chúng tôi có thể làm điều đó với một trường hết hạn bằng không,
  hoặc zero leases, hoặc cả hai. Không cần một khóa thu hồi riêng biệt.

- Khóa mã hóa được sắp xếp theo thứ tự ưu tiên của máy chủ, khóa được ưu tiên nhất trước tiên.
  Hành vi mặc định của khách hàng là chọn khóa đầu tiên với
  một loại mã hóa được hỗ trợ. Khách hàng có thể sử dụng các thuật toán lựa chọn khác
  dựa trên sự hỗ trợ mã hóa, hiệu suất tương đối, và các yếu tố khác.


### LS2 Mã Hóa

Các Mục Tiêu:

- Thêm che dấu
- Cho phép nhiều loại chữ ký
- Không yêu cầu bất kỳ phần tử crypto mới nào
- Tùy chọn mã hóa cho mỗi người nhận, có thể thu hồi
- Hỗ trợ mã hóa LS2 Chuẩn và Meta LS2 chỉ

LS2 Mã hóa không bao giờ được gửi trong một thông điệp garlic end-to-end.
Sử dụng LS2 chuẩn như trên.


Thay đổi từ LS mã hóa hiện tại:

- Mã hóa toàn bộ tập hợp cho tính bảo mật
- Mã hóa một cách an toàn, không chỉ với AES.
- Mã hóa cho mỗi người nhận

Tra cứu với
    Cờ LS tiêu chuẩn (1)
Lưu trữ với
    Loại LS2 mã hóa (5)
Lưu trữ tại
    Hàm băm của loại chữ ký bị che dấu và khóa công khai bị che dấu
    Hai byte loại chữ ký (big endian, ví dụ: 0x000b) || khóa công khai bị che dấu
    Hàm băm này sau đó được sử dụng để tạo "khóa định tuyến" hàng ngày, như trong LS1
Thời hạn hết hạn điển hình
    10 phút, như trong một LS tiêu chuẩn, hoặc vài giờ, như trong một meta LS.
Công bố bởi
    Điểm đến


Định Nghĩa
```````````
Chúng tôi định nghĩa các hàm sau tương ứng với các yếu tố mã hóa được sử dụng
cho LS2 mã hóa:

CSRNG(n)
    Đầu ra n-byte từ một bộ tạo số ngẫu nhiên mật mã an toàn.

    Ngoài yêu cầu CSRNG phải là số ngẫu nhiên mật mã an toàn (và do đó
    phù hợp để tạo ra các tư liệu khóa), nó PHẢI an toàn
    cho một số n-byte đầu ra được sử dụng cho tư liệu khóa khi các chuỗi byte ngay lập tức liền trước và sau nó được phơi bày trên mạng (chẳng hạn như trong một muối, hoặc một padding mã hóa). Các triển khai dựa trên nguồn có thể không đáng tin cậy nên băm bất kỳ đầu ra nào mà sẽ được phơi bày trên mạng [PRNG-REFS]_.

H(p, d)
    Hàm băm SHA-256 nhận chuỗi cá nhân hóa p và dữ liệu d, và
    tạo đầu ra có độ dài 32 bytes.

    Sử dụng SHA-256 như sau::

        H(p, d) := SHA-256(p || d)

STREAM
    Dòng mã hóa ChaCha20 được chỉ định trong [RFC-7539-S2.4]_, với bộ đếm ban đầu
    được đặt là 1. S_KEY_LEN = 32 và S_IV_LEN = 12.

    ENCRYPT(k, iv, plaintext)
        Mã hóa plaintext sử dụng khóa cipher k và nonce iv mà PHẢI là duy nhất
        cho khóa k. Trả về một ciphertext có cùng kích thước với plaintext.

        Toàn bộ ciphertext phải không thể phân biệt với ngẫu nhiên nếu khóa là bí mật.

    DECRYPT(k, iv, ciphertext)
        Giải mã ciphertext sử dụng khóa cipher k và nonce iv. Trả về plaintext.


SIG
    Hệ thống chữ ký RedDSA (tương ứng với SigType 11) với làm mờ khóa.
    Nó có các hàm sau:

    DERIVE_PUBLIC(privkey)
        Trả về khóa công khai tương ứng với khóa riêng cho trước.

    SIGN(privkey, m)
        Trả về một chữ ký bởi khóa riêng privkey trên thông điệp m đã cho.

    VERIFY(pubkey, m, sig)
        Xác minh chữ ký sig đối với khóa công khai pubkey và thông điệp m. Trả về
        true nếu chữ ký là hợp lệ, false nếu không.

    Nó cũng phải hỗ trợ các thao tác làm mờ khóa sau:

    GENERATE_ALPHA(data, secret)
        Tạo alpha cho những ai biết dữ liệu và một bí mật tùy chọn.
        Kết quả phải được phân phối giống hệt như các khóa riêng.

    BLIND_PRIVKEY(privkey, alpha)
        Làm mờ một khóa riêng, sử dụng một alpha bí mật.

    BLIND_PUBKEY(pubkey, alpha)
        Làm mờ một khóa công khai, sử dụng một alpha bí mật.
        Với một cặp khóa cho trước (privkey, pubkey) mối quan hệ sau giữ::

            BLIND_PUBKEY(pubkey, alpha) ==
            DERIVE_PUBLIC(BLIND_PRIVKEY(privkey, alpha))

DH
    Hệ thống khóa công khai X25519. Khóa riêng của 32 bytes, khóa công khai của 32
    bytes, tạo ra đầu ra của 32 bytes. Nó có các hàm sau:

    GENERATE_PRIVATE()
        Tạo ra một khóa riêng mới.

    DERIVE_PUBLIC(privkey)
        Trả về khóa công khai tương ứng với khóa riêng cho trước.

    DH(privkey, pubkey)
        Tạo một bí mật chung từ khóa riêng và khóa công khai cho trước.

HKDF(salt, ikm, info, n)
    Một hàm dẫn xuất khóa mật mã nhận một số tư liệu khóa đầu vào ikm (cái mà
    nên có entropy tốt nhưng không yêu cầu phải là một chuỗi long chong ngẫu nhiên thống nhất), một muối có độ dài 32 bytes, và một giá trị 'info' theo ngữ cảnh, và tạo ra một đầu ra
    có n bytes phù hợp để sử dụng làm tư liệu khóa.

    Sử dụng HKDF như trong [RFC-5869]_, sử dụng hàm băm HMAC SHA-256
    như trong [RFC-2104]_. Điều này có nghĩa là SALT_LEN là 32 bytes tối đa.


Định dạng
``````
Định dạng LS2 mã hóa bao gồm ba lớp lồng nhau:

- Một lớp ngoài chứa thông tin văn bản thuần túy cần thiết cho lưu trữ và truy xuất.
- Một lớp giữa mà xử lý xác thực client.
- Một lớp trong chứa dữ liệu LS2 thực tế.

Định dạng chung nhìn như::

    Dữ liệu Lớp 0 + Mã hóa(dữ liệu lớp 1 + Mã hóa(dữ liệu lớp 2)) + Chữ Ký

Lưu ý rằng LS2 mã hóa được làm mờ. Điểm đến không nằm trong tiêu đề.
Vị trí lưu trữ DHT là SHA-256(loại chữ ký || khóa công khai bị mờ), và được xoay hàng ngày.

KHÔNG sử dụng tiêu đề LS2 chuẩn như đã chỉ định ở trên.

#### Lớp 0 (ngoài)
Loại
    1 byte

    Không thực tế trong tiêu đề, nhưng là một phần của dữ liệu được xử lý bởi chữ ký.
    Lấy từ trường Trong Tin Nhắn Lưu Cơ Sở Dữ Liệu.

Loại Khóa Công Khai Bị Mờ
    2 bytes, big endian
    Đây sẽ luôn là Loại 11, xác định một khóa bị mờ Red25519.

Khóa Công Khai Bị Mờ
    Độ dài như ngụ ý bởi loại chữ ký

Dấu thời gian công bố
    4 bytes, big endian

    Các giây kể từ kỷ nguyên, kết thúc trong năm 2106

Hết hạn
    2 bytes, big endian

    Độ lệch so với dấu thời gian công bố tính bằng giây, tối đa 18.2 giờ

Cờ
    2 bytes

    Thứ tự bit: 15 14 ... 3 2 1 0

    Bit 0: Nếu 0, không có khóa ngoại tuyến; nếu 1, khóa ngoại tuyến

    Các bit khác: đặt thành 0 để tương thích với các mục đích sử dụng trong tương lai

Dữ liệu khóa chuyển tiếp
    Có sẵn nếu cờ chỉ ra các khóa ngoại tuyến

    Dấu thời gian hết hạn
        4 bytes, big endian

        Các giây kể từ kỷ nguyên, kết thúc trong năm 2106

    Loại chữ ký chuyển tiếp
        2 bytes, big endian

    Khóa công khai ký chuyển tiếp
        Độ dài mà không được che dấu

    Chữ ký
        Độ dài như ngụ ý bởi loại chữ ký của khóa công khai bị mờ

        Qua dấu thời gian hết hạn, loại chữ ký chuyển tiếp, và khóa công khai chuyển tiếp.

        Đã được xác minh với khóa công khai bị mờ.

lenOuterCiphertext
    2 bytes, big endian

outerCiphertext
    lenOuterCiphertext bytes

    Dữ liệu lớp 1 đã được mã hóa. Xem bên dưới để biết thuật toán tạo khóa và mã hóa.

Chữ ký
    Độ dài như ngụ ý bởi loại chữ ký của khóa ký được sử dụng

    Chữ ký là của tất cả mọi thứ ở trên.

    Nếu cờ chỉ ra khóa ngoại tuyến, chữ ký được xác minh với
    khóa công khai chuyển tiếp. Ngược lại, chữ ký được xác minh với khóa công khai bị mờ.


#### Lớp 1 (giữa)
Cờ
    1 byte
    
    Thứ tự bit: 76543210

    Bit 0: 0 cho tất cả mọi người, 1 cho từng client, phần auth theo sau, nếu không

    Bit 3-1: Giao thức xác thực, chỉ khi bit 0 được đặt thành 1 cho từng client, nếu không thì là 000
              000: Xác thực client DH (hoặc không xác thực cho từng client)
              001: Xác thực client PSK

    Bit 7-4: Chưa sử dụng, đặt thành 0 để tương thích trong tương lai

Dữ liệu xác thực client DH
    Có sẵn nếu bit cờ 0 được đặt thành 1 và các bit cờ 3-1 được đặt thành 000.

    Khóa Công Khai tạm thời
        32 bytes

    client
        2 bytes, big endian

        Số lượng đầu vào authClient theo sau, mỗi đầu vào 40 bytes

    authClient
        Dữ liệu ủy quyền cho một client đơn lẻ.

        clientID_i
            8 bytes

        clientCookie_i
            32 bytes

Dữ liệu xác thực client PSK
    Có sẵn nếu bit cờ 0 được đặt thành 1 và các bit cờ 3-1 được đặt thành 001.

    authSalt
        32 bytes

    clients
        2 bytes, big endian

        Số lượng đầu vào authClient theo sau, mỗi đầu vào 40 bytes

    authClient
        Dữ liệu ủy quyền cho một client đơn lẻ.

        clientID_i
            8 bytes

        clientCookie_i
            32 bytes


innerCiphertext
    Độ dài như ngụ ý bởi lenOuterCiphertext (bất kỳ dữ liệu nào còn lại)

    Dữ liệu lớp 2 đã được mã hóa. Xem bên dưới để biết thuật toán tạo khóa và mã hóa.


#### Lớp 2 (trong)
Loại
    1 byte

    Hoặc là 3 (LS2) hoặc 7 (Meta LS2)

Dữ liệu
    Dữ liệu LeaseSet2 cho loại đã cho.

    Đã bao gồm tiêu đề và chữ ký.


Làm Mờ Khóa
```````````````````````

Chúng tôi sử dụng sơ đồ sau cho làm mờ khóa,
dựa trên Ed25519 và ZCash RedDSA [ZCASH]_.
Các chữ ký Re25519 là trên đường cong Ed25519, sử dụng SHA-512 cho băm.

Chúng tôi không sử dụng mục phụ lục A.2 rend-spec-v3.txt của Tor [TOR-REND-SPEC-V3]_,
có mục tiêu thiết kế tương tự, bởi vì các khóa công khai bị mờ của nó
có thể ở ngoài nhóm phụ đường cong, với ý nghĩa bảo mật chưa rõ.


#### Các Mục Tiêu

- Khóa công khai ký trong destination không làm mờ phải
  Ed25519 (sig type 7) hoặc Red25519 (sig type 11);
  không có loại chữ ký nào khác được hỗ trợ
- Nếu khóa công khai ký là ngoại tuyến, khóa công khai ký chuyển tiếp phải cũng là Ed25519
- Làm mờ phải đơn giản về mặt tính toán
- Sử dụng các yếu tố mã hóa hiện tại
- Khóa công khai bị mờ không thể bị không làm mờ
- Khóa công khai bị mờ phải ở trên đường cong Ed25519 và nhóm phụ trên đường cong
- Phải biết khóa công khai ký của destination
  (không yêu cầu destination đầy đủ) để tạo khóa công khai bị mờ
- Tùy chọn cung cấp một bí mật bổ sung cần thiết để tạo khóa công khai bị mờ


#### Bảo Mật

Bảo mật của một sơ đồ làm mờ yêu cầu
sự phân phối của alpha là giống như các khóa riêng không làm mờ.
Tuy nhiên, khi chúng tôi làm mờ một khóa riêng Ed25519 (sig type 7)
đến Red25519 (sig type 11), thì phân phối khác nhau.
Để đáp ứng các yêu cầu của zcash phần 4.1.6.1 [ZCASH]_,
Red25519 (sig type 11) nên được sử dụng cho các khóa không làm mờ là tốt, do đó
"sự kết hợp của một khóa công khai được làm mờ lại và chữ ký(những)
dưới khóa đó không tiết lộ khóa từ cái mà nó được làm mờ lại."
Chúng tôi cho phép loại 7 cho các điểm đến hiện có, nhưng đề xuất
loại 11 cho các điểm đến mới sẽ được mã hóa.



#### Định Nghĩa

B
    Điểm cơ sở Ed25519 (điểm khởi đầu) 2^255 - 19 như trong [ED25519-REFS]_

L
    Đếm Ed25519 2^252 + 27742317777372353535851937790883648493
    như trong [ED25519-REFS]_

DERIVE_PUBLIC(a)
    Chuyển đổi một khóa riêng thành khóa công khai, như trong Ed25519 (nhân với G)

alpha
    Một số ngẫu nhiên 32-byte mà được biết bởi những ai biết về destination.

GENERATE_ALPHA(destination, date, secret)
    Tạo alpha cho ngày hiện tại, cho những ai biết về destination và secret.
    Kết quả phải được phân khối giống như các khóa riêng Ed25519.

a
    Khóa riêng ký EdDSA hoặc RedDSA không làm mờ 32-byte được sử dụng để ký destination

A
    Khóa công khai ký EdDSA hoặc RedDSA không làm mờ 32-byte trong destination,
    = DERIVE_PUBLIC(a), như trong Ed25519

a'
    Khóa riêng ký EdDSA được làm mờ 32-byte được sử dụng để ký leaseset mã hóa
    Đây là một khóa riêng EdDSA hợp lệ.

A'
    Khóa công khai ký EdDSA được làm mờ 32-byte trong Destination,
    có thể được tạo với DERIVE_PUBLIC(a'), hoặc từ A và alpha.
    Đây là một khóa công khai EdDSA hợp lệ, trên đường cong và trên nhóm phụ trên đường cong.

LEOS2IP(x)
    Lật chế độ của các byte đầu vào thành little-endian

H*(x)
    32 bytes = (LEOS2IP(SHA512(x))) mod B, giống như trong Ed25519 hash-and-reduce


#### Tính Toán Làm Mờ

Một alpha bí mật mới và các khóa bị mờ phải được tạo mỗi ngày (giờ UTC).
Alpha bí mật và các khóa bị mờ được tính như sau.

GENERATE_ALPHA(destination, date, secret), cho tất cả các bên:

  ```text
// GENERATE_ALPHA(destination, date, secret)

  // secret là tùy chọn, nếu không thì là độ dài bằng không
  A = khóa công khai ký của destination
  stA = loại chữ ký của A, 2 bytes big endian (0x0007 hoặc 0x000b)
  stA' = loại chữ ký của khóa công khai bị mờ A', 2 bytes big endian (0x000b)
  keydata = A || stA || stA'
  datestring = 8 bytes ASCII YYYYMMDD từ ngày hiện tại UTC
  secret = chuỗi được mã hóa UTF-8
  seed = HKDF(H("I2PGenerateAlpha", keydata), datestring || secret, "i2pblinding1", 64)
  // đối xử seed như là một giá trị 64 byte little-endian
  alpha = seed mod L
```

BLIND_PRIVKEY(), cho chủ sở hữu công bố leaseset:

  ```text
// BLIND_PRIVKEY()

  alpha = GENERATE_ALPHA(destination, date, secret)
  // Nếu cho một khóa riêng Ed25519 (loại 7)
  seed = private key ký của destination
  a = nửa bên trái của SHA512(seed) và bị kẹp như thường lệ cho Ed25519
  // nếu không, cho một khóa riêng Red25519 (loại 11)
  a = private key ký của destination
  // Cộng thêm sử dụng số học đẳng cấp
  private key ký bị mờ = a' = BLIND_PRIVKEY(a, alpha) = (a + alpha) mod L
  khóa công khai ký bị mờ = A' = DERIVE_PUBLIC(a')
```

BLIND_PUBKEY(), cho các khách hàng truy cập leaseset:

  ```text
// BLIND_PUBKEY()

  alpha = GENERATE_ALPHA(destination, date, secret)
  A = khóa công khai ký của destination
  // Cộng thêm sử dụng phần tử nhóm (điểm trên đường cong)
  khóa công khai bị mờ = A' = BLIND_PUBKEY(A, alpha) = A + DERIVE_PUBLIC(alpha)
```

Cả hai phương pháp tính toán A' đều mang lại cùng kết quả, như yêu cầu.



#### Ký

Leaseset không làm mờ được ký bởi khóa riêng ký Ed25519 hoặc Red25519 không làm mờ
và được xác minh với khóa công khai ký Ed25519 hoặc Red25519 không làm mờ (loại chữ ký 7 hoặc 11) như thường lệ.

Nếu khóa công khai ký là khóa ngoại tuyến,
leaset không làm mờ được ký bởi khóa riêng ký Ed25519 hoặc Red25519 không làm mờ chuyển tiếp
và được xác minh với khóa công khai ký Ed25519 hoặc Red25519 chuyển tiếp (loại chữ ký 7 hoặc 11) như thường lệ.
Tham khảo bên dưới về các ghi chú bổ sung khi sử dụng khóa ngoại tuyến cho leaseset mã hóa.

Đối với việc ký leaseset mã hóa, chúng tôi sử dụng Red25519, dựa trên RedDSA [ZCASH]_
để ký và xác minh với khóa bị mờ.
Các chữ ký Red25519 là trên đường cong Ed25519, sử dụng SHA-512 cho băm.

Red25519 giống hệt với Ed25519 ngoại trừ như được chỉ định bên dưới.


#### Tính Toán Ký/Xác Minh

Phần ngoài của leaseset mã hóa sử dụng các khóa và chữ ký Red25519.

Red25519 giống hệt với Ed25519. Có hai điểm khác biệt:

Các khóa riêng Red25519 được tạo từ số ngẫu nhiên và sau đó phải được giảm mod L, trong đó L được định nghĩa ở trên.
Các khóa riêng Ed25519 được tạo từ số ngẫu nhiên và sau đó "bị kẹp" bằng cách sử dụng
mặt nạ bitwise cho byte 0 và 31. Điều này không được thực hiện cho Red25519.
Hàm GENERATE_ALPHA() và BLIND_PRIVKEY() được định nghĩa ở trên tạo ra các khóa riêng Red25519 thích hợp bằng việc sử dụng mod L.

Trong Red25519, việc tính toán r cho việc ký sử dụng dữ liệu ngẫu nhiên bổ sung,
và sử dụng giá trị khóa công khai thay vì băm của khóa riêng.
Bởi vì dữ liệu ngẫu nhiên, mỗi chữ ký Red25519 là khác nhau, ngay cả
khi ký cùng dữ liệu với cùng khóa.

Ký:

  ```text
T = 80 byte ngẫu nhiên
  r = H*(T || khóa công khai || message)
  // phần còn lại là giống như trong Ed25519
```

Xác minh:

  ```text
// giống như trong Ed25519
```



Mã hóa và xử lý
`````````````````````````
#### Dẫn xuất của subcredentials
Như một phần của quá trình làm mờ, chúng tôi cần đảm bảo rằng một LS2 mã hóa chỉ có thể
được giải mã bởi một ai đó biết khóa công khai ký tương ứng của Destination.
Full Destination không cần thiết.
Để đạt được điều này, chúng tôi dẫn ra một credential từ khóa công khai ký:

  ```text
A = khóa công khai ký của destination
  stA = loại chữ ký của A, 2 bytes big endian (0x0007 hoặc 0x000b)
  stA' = loại chữ ký của khóa công khai bị mờ A', 2 bytes big endian (0x000b)
  keydata = A || stA || stA'
  credential = H("credential", keydata)
```

Chuỗi cá nhân hóa đảm bảo rằng credential không va chạm với bất kỳ hàm băm nào được sử dụng
như là một khóa tra cứu DHT, chẳng hạn như hàm băm Destination đơn giản.

Đối với khóa bị mờ, chúng tôi sau đó có thể dẫn ra một subcredential:

  ```text
subcredential = H("subcredential", credential || khóa công khai bị mờ)
```

Subcredential này được bao gồm trong các quá trình tạo khóa bên dưới, điều này liên kết các
khóa đó với kiến thức về khóa công khai ký của destination.

#### Mã hóa lớp 1
Đầu tiên, đầu vào cho quá trình tạo khóa được chuẩn bị:

  ```text
outerInput = subcredential || publishedTimestamp
```

Tiếp theo, một muối ngẫu nhiên được tạo ra:

  ```text
outerSalt = CSRNG(32)
```

Sau đó, khóa được sử dụng để mã hóa lớp 1 được tạo ra:

  ```text
keys = HKDF(outerSalt, outerInput, "ELS2_L1K", 44)
  outerKey = keys[0:31]
  outerIV = keys[32:43]
```

Cuối cùng, plaintext lớp 1 được mã hóa và chuỗi hóa:

  ```text
outerCiphertext = outerSalt || ENCRYPT(outerKey, outerIV, outerPlaintext)
```

#### Giải mã lớp 1
Muối được phân tích từ ciphertext lớp 1:

  ```text
outerSalt = outerCiphertext[0:31]
```

Sau đó, khóa được sử dụng để mã hóa lớp 1 được tạo ra:

  ```text
outerInput = subcredential || publishedTimestamp
  keys = HKDF(outerSalt, outerInput, "ELS2_L1K", 44)
  outerKey = keys[0:31]
  outerIV = keys[32:43]
```

Cuối cùng, ciphertext lớp 1 được giải mã:

  ```text
outerPlaintext = DECRYPT(outerKey, outerIV, outerCiphertext[32:end])
```

#### Mã hóa lớp 2
Khi xác thực client được kích hoạt, ``authCookie`` được tính toán như được mô tả bên dưới.
Khi xác thực client không được kích hoạt, ``authCookie`` là chuỗi byte có độ dài bằng không.

Mã hóa tiến hành tương tự như cho lớp 1:

  ```text
innerInput = authCookie || subcredential || publishedTimestamp
  innerSalt = CSRNG(32)
  keys = HKDF(innerSalt, innerInput, "ELS2_L2K", 44)
  innerKey = keys[0:31]
  innerIV = keys[32:43]
  innerCiphertext = innerSalt || ENCRYPT(innerKey, innerIV, innerPlaintext)
```

#### Giải mã lớp 2
Khi xác thực client được kích hoạt, ``authCookie`` được tính toán như được mô tả bên dưới.
Khi xác thực client không được kích hoạt, ``authCookie`` là chuỗi byte có độ dài bằng không.

Giải mã tiến hành tương tự như cho lớp 1:

  ```text
innerInput = authCookie || subcredential || publishedTimestamp
  innerSalt = innerCiphertext[0:31]
  keys = HKDF(innerSalt, innerInput, "ELS2_L2K", 44)
  innerKey = keys[0:31]
  innerIV = keys[32:43]
  innerPlaintext = DECRYPT(innerKey, innerIV, innerCiphertext[32:end])
```


Xác thực theo từng client
````````````````````````
Khi xác thực theo từng client được kích hoạt cho một Destination, máy chủ duy trì danh sách các
client mà họ cho phép truy cập dữ liệu LS2 mã hóa. Dữ liệu lưu trữ theo từng client
phụ thuộc vào cơ chế xác thực, và bao gồm một dạng tư liệu khóa mà mỗi
client tạo ra và gửi tới máy chủ thông qua một đường dẫn bảo mật ngoài băng.

Có hai lựa chọn thay thế cho việc triển khai xác thực theo từng client:

#### Xác thực client DH
Mỗi client tạo ra một cặp khóa DH ``[csk_i, cpk_i]``, và gửi khóa công khai ``cpk_i``
tới máy chủ.

Xử lý trên máy chủ
^^^^^^^^^^^^^^^^^
Máy chủ tạo ra một ``authCookie`` mới và một cặp khóa DH đơn thuần

  ```text
authCookie = CSRNG(32)
  esk = GENERATE_PRIVATE()
  epk = DERIVE_PUBLIC(esk)
```

Sau đó cho mỗi client được ủy quyền, máy chủ mã hóa ``authCookie`` với khóa công khai của nó

  ```text
sharedSecret = DH(esk, cpk_i)
  authInput = sharedSecret || cpk_i || subcredential || publishedTimestamp
  okm = HKDF(epk, authInput, "ELS2_XCA", 52)
  clientKey_i = okm[0:31]
  clientIV_i = okm[32:43]
  clientID_i = okm[44:51]
  clientCookie_i = ENCRYPT(clientKey_i, clientIV_i, authCookie)
```

Máy chủ đặt từng cặp ``[clientID_i, clientCookie_i]`` vào lớp 1 của
LS2 mã hóa, cùng với ``epk``.

Xử lý trên client
^^^^^^^^^^^^^^^^^
Client sử dụng khóa riêng của nó để tạo ra định danh client mong đợi ``clientID_i``,
khóa mã hóa ``clientKey_i``, và ``clientIV_i`` với mã hóa:

  ```text
sharedSecret = DH(csk_i, epk)
  authInput = sharedSecret || cpk_i || subcredential || publishedTimestamp
  okm = HKDF(epk, authInput, "ELS2_XCA", 52)
  clientKey_i = okm[0:31]
  clientIV_i = okm[32:43]
  clientID_i = okm[44:51]
```

Sau đó, client tìm kiếm dữ liệu xác thực lớp 1 cho một đầu mà chứa
``clientID_i``. Nếu có một đầu số phù hợp tồn tại, client giải mã
nó để lấy ``authCookie``:

  ```text
authCookie = DECRYPT(clientKey_i, clientIV_i, clientCookie_i)
```

#### Xác thực client Pre-shared key
Mỗi client tạo ra một khóa bí mật 32-byte ``psk_i``, và gửi nó đến máy chủ.
Ngoài ra, máy chủ có thể tạo ra khóa bí mật, và gửi nó cho một hoặc nhiều client.


Xử lý trên máy chủ
^^^^^^^^^^^^^^^^^
Máy chủ tạo ra một ``authCookie`` mới và muối:

  ```text
authCookie = CSRNG(32)
  authSalt = CSRNG(32)
```

Sau đó cho mỗi client được ủy quyền, máy chủ mã hóa ``authCookie`` với khóa pre-shared của nó

  ```text
authInput = psk_i || subcredential || publishedTimestamp
  okm = HKDF(authSalt, authInput, "ELS2PSKA", 52)
  clientKey_i = okm[0:31]
  clientIV_i = okm[32:43]
  clientID_i = okm[44:51]
  clientCookie_i = ENCRYPT(clientKey_i, clientIV_i, authCookie)
```

Máy chủ đặt từng cặp ``[clientID_i, clientCookie_i]`` vào lớp 1 của
LS2 mã hóa, cùng với ``authSalt``.

Xử lý trên client
^^^^^^^^^^^^^^^^^
Client sử dụng khóa pre-shared để tạo ra định danh client mong đợi
``clientID_i``, khóa mã hóa ``clientKey_i``, và ``clientIV_i`` với mã hóa:

  ```text
authInput = psk_i || subcredential || publishedTimestamp
  okm = HKDF(authSalt, authInput, "ELS2PSKA", 52)
  clientKey_i = okm[0:31]
  clientIV_i = okm[32:43]
  clientID_i = okm[44:51]
```

Sau đó, client tìm kiếm dữ liệu xác thực lớp 1 cho một đầu mà chứa
``clientID_i``. Nếu có một đầu số phù hợp tồn tại, client giải mã
nó để lấy ``authCookie``:

  ```text
authCookie = DECRYPT(clientKey_i, clientIV_i, clientCookie_i)
```

#### Các cân nhắc về bảo mật
Cả hai cơ chế xác thực client trên đều cung cấp quyền riêng tư về tư cách thành viên khách hàng.
Một tổ chức chỉ biết Destination có thể thấy bao nhiêu khách hàng đang được tham gia tại bất kỳ
thời điểm nào, nhưng không thể theo dõi những khách hàng nào đang tăng thêm hay bị thu hồi.

Máy chủ NÊN ngẫu nhiên hóa thứ tự của khách hàng mỗi khi tạo ra một LS2 mã hóa, để
ngăn chặn các khách hàng học hỏi vị trí của họ trong danh sách và suy luận khi nào các khách hàng khác đã được thêm vào hoặc thu hồi.

Một máy chủ CÓ THỂ chọn để ẩn số lượng khách hàng đã được tham gia bằng cách chèn các đầu ngẫu nhiên vào danh sách dữ liệu xác thực.

Lợi thế của việc áp dụng xác thực client DH
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- An toàn của sơ đồ không hoàn toàn phụ thuộc vào việc chuyển giao ngoài băng của tư liệu khóa khách hàng.
  Bí mật khóa của khách hàng không bao giờ rời khỏi thiết bị của họ, và vì vậy một
  đối thủ chỉ có thể chặn được việc chuyển giao ngoài băng, nhưng không thể bẻ khóa thuật toán DH,
  không thể giải mã LS2 mã hóa, hoặc xác định bao lâu khách hàng được cấp quyền truy cập.

Nhược điểm của việc áp dụng xác thực client DH
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- Yêu cầu N + 1 thao tác DH trên phía máy chủ cho N khách hàng.
- Yêu cầu một thao tác DH trên phía khách hàng.
- Yêu cầu khách hàng tạo ra khóa bí mật.

Lợi thế của xác thực client PSK
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- Không yêu cầu thao tác DH.
- Cho phép máy chủ tạo ra khóa bí mật.
- Cho phép máy chủ chia sẻ cùng khóa với nhiều khách hàng, nếu mong muốn.

Nhược điểm của xác thực client PSK
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- An toàn của sơ đồ phụ thuộc hoàn toàn vào việc chuyển giao ngoài băng của tư liệu khóa khách hàng. Một đối thủ có thể chặn việc chuyển giao cho một khách hàng cụ thể có thể giải mã
  bất kỳ LS2 mã hóa nào sau đó đã được ủy quyền, cũng như xác định khi quyền truy cập của khách hàng bị thu hồi.


LS mã hóa với Địa chỉ Base 32
``````````````````````````````````

Tham khảo đề xuất 149.

Bạn không thể sử dụng một LS2 mã hóa cho bittorrent, bởi vì các phản hồi thông báo kết hợp là 32 bytes.
32 bytes chỉ chứa hàm băm. Không có không gian để thêm chỉ định rằng
leaseset được mã hóa, hoặc loại chữ ký.



LS mã hóa với Khóa Ngoại Tuyến
``````````````````````````````
Đối với leaseset mã hóa với khóa ngoại tuyến, các khóa riêng bị mờ cũng phải được tạo ngoại tuyến, một cho mỗi ngày.

Vì khối chữ ký ngoại tuyến tùy chọn nằm phần trong phía rõ ràng của leaseset mã hóa,
bất kỳ ai cạo floodfills cũng có thể sử dụng điều này để theo dõi leaseset (nhưng không 
giải mã được nó) trong vài ngày.
Để ngăn chặn điều này, chủ sở hữu của các khóa nên tạo các khóa chuyển tiếp 
mới mỗi ngày.
Cả khóa chuyển tiếp và khóa bị mờ có thể được tạo ra trước, và được đưa tới router
trong batch.

Không có định dạng file nào được định nghĩa trong đề xuất này cho đóng gói nhiều khóa chuyển tiếp 
và bị mờ và cung cấp chúng cho client hoặc router.
Không có nâng cấp giao thức I2CP nào được định nghĩa trong đề xuất này để hỗ trợ
leaseset mã hóa với khóa ngoại tuyến.



Ghi Chú
`````

- Một dịch vụ sử dụng leaseset mã hóa sẽ công bố phiên bản mã hóa đến
  floodfills. Tuy nhiên, để hiệu quả, nó sẽ gửi leasesets không mã hóa đến
  client trong thông điệp garlic được bọc, sau khi xác thực (thông qua danh sách trắng, ví dụ).

- Floodfills có thể giới hạn kích thước tối đa đến một giá trị hợp lý để ngăn chặn lạm dụng.

- Sau giải mã, một số kiểm tra phải được thực hiện, bao gồm việc
  dấu thời gian và hết hạn bên trong trùng khớp với những cái ở cấp trên.

- ChaCha20 được chọn so với AES. Mặc dù tốc độ tương tự nhau nếu có hỗ trợ 
  phần cứng AES, ChaCha20 nhanh hơn 2.5-3x khi
  có hỗ trợ phần cứng AES không có sẵn, chẳng hạn trên các thiết bị ARM cấp thấp hơn.

- Chúng tôi không quan tâm đủ đến tốc độ để sử dụng BLAKE2b có khóa. Nó có một kích thước đầu ra đủ lớn để đựng lớn nhất n mà chúng tôi yêu cầu (hoặc chúng tôi có thể gọi nó một lần mỗi 
  khóa mong muốn với một đối số bộ đếm). BLAKE2b là nhanh hơn nhiều SHA-256, và
  BLAKE2b có khóa sẽ giảm tổng số lượng cuộc gọi hàm băm.
  Tuy nhiên, xem đề xuất 148, nơi nó được đề xuất rằng chúng ta chuyển đổi sang BLAKE2b vì các lý do khác.
  [UNSCIENTIFIC-KDF-SPEEDS]_


### Meta LS2

Điều này được sử dụng để thay thế multihoming. Như bất kỳ leaseset nào, điều này được ký bởi
người tạo. Đây là một danh sách đích hầm đã được xác thực.

Meta LS2 là đầu trên cùng, và có thể là các nút trung gian của,
một cấu trúc cây.
Nó chứa một số đầu vào, mỗi cái trỏ tới một LS, LS2, hoặc một Meta LS2 khác
để hỗ trợ multihoming lớn.
Một Meta LS2 có thể chứa một tập hợp LS, LS2, và Meta LS2.
Các lá của cây luôn là một LS hoặc LS2.
Cây là một DAG; các vòng lặp bị cấm và client thực hiện tra cứu phải phát hiện và
từ chối theo dõi các vòng lặp.

Một Meta LS2 có thể có thời gian hết hạn lâu hơn nhiều so với một LS tiêu chuẩn hoặc một LS2.
Cấp độ trên cùng có thể có thời gian hết hạn hàng giờ sau ngày xuất bản.
Thời gian hết hạn tối đa sẽ được thực thi bởi floodfills và client, và là TBD.

Trường hợp sử dụng cho Meta LS2 là multihoming lớn, nhưng không có
bảo vệ cho sự tương quan giữa các router và leasesets (tại thời điểm khởi động lại router) hơn là
được cung cấp hiện tại với LS hoặc LS2.
Điều này tương đương với trường hợp sử dụng "facebook", cái mà có thể không cần
bảo vệ tương quan. Trường hợp sử dụng này có thể cần 
các khóa ngoại tuyến, được cung cấp trong tiêu đề chuẩn tại mỗi nút của cây.

Giao thức back-end cho sự phối hợp giữa các router leaf, các node trung gian và master Meta LS không được chỉ định ở đây. Các yêu cầu rất đơn giản - chỉ cần xác minh rằng node ngang hàng đang hoạt động,
và công bố một LS mới sau mỗi vài giờ. Sự phức tạp duy nhất là cho việc chọn
các nhà xuất bản mới cho các Meta LS tầng cao nhất hoặc tầng trung gian trong trường hợp hư hỏng.

Các leasesets mix-and-match nơi các lease từ nhiều routers được kết hợp, ký tên, và công bố
trong một leaseset duy nhất được ghi nhận trong đề xuất 140, "multihoming vô hình".
Đề xuất này là không khả thi như đã viết, vì các kết nối streaming sẽ không được
"bám chặt" vào một router duy nhất, xem http://zzz.i2p/topics/2335 .

Giao thức back-end, và tương tác với các nội bộ router và client, sẽ là
khá phức tạp cho multihoming vô hình.

Để tránh quá tải floodfill cho top-level Meta LS, thời gian hết hạn nên
là ít nhất vài giờ. Client phải lưu trữ Meta LS top-level, và duy trì
nó qua các khởi động lại nếu chưa hết hạn.

Chúng ta cần định nghĩa một số thuật toán cho client để di chuyển qua cây, bao gồm các sự cố,
để sự sử dụng được phân tán. Một số chức năng của khoảng cách băm, chi phí, và tính ngẫu nhiên.
Nếu một node có cả LS hoặc LS2 và Meta LS, chúng ta cần biết khi nào được phép
sử dụng những leaseset đó, và khi nào cần tiếp tục di chuyển qua cây.


Tra cứu với
    Cờ LS tiêu chuẩn (1)
Lưu trữ với
    Loại Meta LS2 (7)
Lưu trữ tại
    Hàm băm của đích đến
    Hàm băm này sau đó được sử dụng để tạo "khóa định tuyến" hàng ngày, như trong LS1
Thời hạn hết hạn điển hình
    Giờ. Tối đa 18.2 giờ (65535 giây)
Được công bố bởi
    "master" Destination hoặc điều phối viên, hoặc điều phối viên trung gian

Định dạng
``````
::

  Tiêu Đề LS2 Chuẩn như được chỉ định ở trên

  Phần Cụ Thể Loại Meta LS2
  - Thuộc tính (Mapping như được chỉ định trong đặc tả cấu trúc chung, 2 zero bytes nếu không có)
  - Số lượng đầu vào (1 byte) Tối đa TBD
  - Các đầu vào. Mỗi đầu vào chứa: (40 bytes)
    - Hash (32 bytes)
    - Cờ (2 bytes)
      TBD. Đặt tất cả thành zero để tương thích với các mục đích sử dụng trong tương lai.
    - Loại (1 byte) Loại của LS mà nó đang tham chiếu;
      1 cho LS, 3 cho LS2, 5 cho mã hóa, 7 cho meta, 0 cho không xác định.
    - Chi phí (ưu tiên) (1 byte)
    - Hết hạn (4 bytes) (4 bytes, big endian, giây kể từ epoch, kết thúc trong 2106)
  - Số lượng thu hồi (1 byte) Tối đa TBD
  - Thu hồi: Mỗi phần thu hồi chứa: (32 bytes)
    - Hash (32 bytes)

  Chữ Ký LS2 Chuẩn:
  - Chữ ký (40+ bytes)
    Chữ ký là của tất cả mọi thứ ở trên.

Cờ và thuộc tính: cho sử dụng trong tương lai


Ghi Chú
`````
- Một dịch vụ phân phối sử dụng điều này sẽ có một hoặc nhiều "master" với
  khóa riêng của destination dịch vụ. Chúng sẽ (out of band) xác định
  danh sách hiện tại của điểm đến hoạt động và sẽ công bố Meta LS2. Để
  dự phòng, nhiều master có thể multihome (tức là, công bố đồng thời) Meta LS2.

- Một dịch vụ phân phối có thể bắt đầu với một đích đến duy nhất hoặc sử dụng multihoming kiểu cũ, sau đó
  chuyển đổi sang Meta LS2. Một tìm kiếm LS tiêu chuẩn có thể trả về
  một trong một LS, LS2, hoặc Meta LS2.

- Khi một dịch vụ sử dụng Meta LS2, nó không có đường hầm (leases).


### Ghi Nhớ Dịch Vụ

Đây là một bản ghi riêng rẽ nói rằng một đích đến đang tham gia một
dịch vụ. Nó được gửi từ người tham gia đến floodfill. Nó không bao giờ được
gửi riêng rẽ bởi một floodfill, mà chỉ như một phần của một Danh Sách Dịch Vụ. Ghi Nhớ Dịch Vụ cũng được sử dụng để thu hồi tham gia vào một dịch vụ, bằng cách đặt
thời gian hết hạn về không.

Điều này không phải một LS2 nhưng sử dụng cùng định dạng tiêu đề LS2 và chữ ký.

Tra cứu với
    n/a, xem Danh Sách Dịch Vụ
Lưu trữ với
    Loại Ghi Nhớ Dịch Vụ (9)
Lưu trữ tại
    Hàm băm của tên dịch vụ
    Hàm băm này sau đó được sử dụng để tạo "khóa định tuyến" hàng ngày, như trong LS1
Thời hạn hết hạn điển hình
    Giờ. Tối đa 18.2 giờ (65535 giây)
Được công bố bởi
    Đích đến

Định dạng
``````
::

  Tiêu Đề LS2 Chuẩn như được chỉ định ở trên

  Phần Cụ Thể Loại Ghi Nhớ Dịch Vụ
  - Cổng (2 bytes, big endian) (0 nếu không xác định)
  - Hàm băm của tên dịch vụ (32 bytes)

  Chữ Ký LS2 Chuẩn:
  - Chữ ký (40+ bytes)
    Chữ ký là của tất cả mọi thứ ở trên.


Ghi Chú
`````
- Nếu hết hạn là tất cả zero, floodfill nên thu hồi bản ghi và không còn
  bao gồm nó trong danh sách dịch vụ.

- Lưu trữ: Floodfill có thể giới hạn nghiêm ngặt lưu trữ của những bản ghi này và
  giới hạn số lượng bản ghi lưu trữ cho mỗi hàm băm và thời gian hết hạn của chúng. Một
  danh sách trắng của các hàm băm cũng có thể được sử dụng.

- Bất kỳ loại netdb nào khác cùng một hàm băm có ưu tiên, vì vậy một ghi nhớ dịch vụ không bao giờ
  ghi đè lên một LS/RI, nhưng một LS/RI sẽ ghi đè lên tất cả các ghi nhớ dịch vụ tại hàm băm đó.



### Danh Sách Dịch Vụ

Điều này không giống một LS2 và sử dụng một định dạng khác.

Danh sách dịch vụ được tạo ra và ký bởi floodfill. Nó không xác thực
vì bất kỳ ai cũng có thể tham gia vào dịch vụ bằng cách công bố một Ghi Nhớ Dịch Vụ tới một
floodfill.

Một Danh Sách Dịch Vụ chứa các Ghi Nhớ Dịch Vụ Ngắn, không phải các Ghi Nhớ Dịch Vụ đầy đủ. Những
ảnh ngắn này chứa các chữ ký nhưng chỉ là các hàm băm, không phải các đích đến đầy đủ, vì vậy chúng không thể
được xác minh mà không có destination đầy đủ.

An ninh, nếu có, và mong muốn của các danh sách dịch vụ là TBD.
Floodfill có thể giới hạn việc công bố, và tra cứu, vào một danh sách trắng của các dịch vụ,
nhưng danh sách trắng đó có thể thay đổi dựa trên thực thi, hoặc sở thích của nhà điều hành.
Có thể không thể đạt được sự đồng thuận về một danh sách trắng cơ sở chung
giữa các thực hiện.

Nếu tên dịch vụ được bao gồm trong bản ghi dịch vụ ở trên,
sau đó các nhà điều hành floodfill có thể phản đối; nếu chỉ có hàm băm được bao gồm,
không có xác thực, và một ghi nhớ dịch vụ có thể "vào" trước
bất kỳ loại netdb nào khác và được lưu trữ trong floodfill.

Tra cứu với
    Loại tra cứu danh sách dịch vụ (11)
Lưu trữ với
    Loại danh sách dịch vụ (11)
Lưu trữ tại
    Hàm băm của tên dịch vụ
    Hàm băm này sau đó được sử dụng để tạo "khóa định tuyến" hàng ngày, như trong LS1
Thời hạn hết hạn điển hình
    Giờ, không được chỉ định trong danh sách bản thân, tùy theo chính sách địa phương
Được công bố bởi
    Không có ai, không bao giờ gửi đến floodfill, không bao giờ được phổ biến.

Định dạng
``````
Không Sử Dụng tiêu đề LS2 Chuẩn như đã chỉ định ở trên.

::

  - Loại (1 byte)
    Không thực tế trong tiêu đề, nhưng là một phần của dữ liệu được xử lý bởi chữ ký.
    Lấy từ trường Trong Tin Nhắn Lưu Trữ Cơ Sở Dữ Liệu.
  - Hàm băm của tên dịch vụ (ẩn, trong tin nhắn Lưu Trữ trong Cơ Sở Dữ Liệu)
  - Hàm băm của Người Tạo (floodfill) (32 bytes)
  - Dấu thời gian công bố (8 bytes, big endian)

  - Số lượng Ghi Nhớ Dịch Vụ Ngắn (1 byte)
  - Danh sách Ghi Nhớ Dịch Vụ Ngắn:
    Mỗi Ghi Nhớ Dịch Vụ Ngắn chứa (90+ bytes)
    - Hash điểm đến (32 bytes)
    - Dấu thời gian công bố (8 bytes, big endian)
    - Hết hạn (4 bytes, big endian) (độ lệch từ công bố bằng ms)
    - Cờ (2 bytes)
    - Port (2 bytes, big endian)
    - Độ dài chữ ký (2 bytes, big endian)
    - Chữ ký của điểm đến (40+ bytes)

  - Số lượng Bản Thu Hồi (1 byte)
  - Danh sách Các Bản Thu Hồi:
    Mỗi Bản Thu Hồi chứa (86+ bytes)
    - Hash điểm đến (32 bytes)
    - Dấu thời gian công bố (8 bytes, big endian)
    - Cờ (2 bytes)
    - Port (2 bytes, big endian)
    - Độ dài chữ ký (2 bytes, big endian)
    - Chữ ký của điểm đến (40+ bytes)

  - Chữ ký của floodfill (40+ bytes)
    Chữ ký là của tất cả mọi thứ ở trên.

Để xác minh chữ ký của Danh Sách Dịch Vụ:

- Thêm vào đầu hàm băm của tên dịch vụ
- Xóa hàm băm của người tạo
- Kiểm tra chữ ký của nội dung đã được sửa đổi

Để xác minh chữ ký của mỗi Ghi Nhớ Dịch Vụ Ngắn:

- Truy xuất destination
- Kiểm tra chữ ký của (dấu thời gian công bố + hết hạn + cờ + port + Hàm 
  băm của tên dịch vụ)

Để xác minh chữ ký của mỗi Bản Thu Hồi:

- Truy xuất destination
- Kiểm tra chữ ký của (dấu thời gian công bố + 4 byte zero + cờ + port + Hàm
  băm của tên dịch vụ)

Ghi Chú
`````
- Chúng tôi sử dụng độ dài chữ ký thay vì loại chữ ký để chúng tôi có thể
  hỗ trợ các loại chữ ký không rõ.

- Không có thời gian hết hạn của một danh sách dịch vụ, những người nhận có thể tự mình
  quyết định thời điểm dựa trên chính sách hay hết hạn của các bản ghi cá nhân.

- Danh Sách Dịch Vụ không bị phổ biến, chỉ có từng Ghi Nhớ Dịch Vụ là. Mỗi
  floodfill tạo, ký, và lưu trữ một Danh Sách Dịch Vụ. Floodfill sử dụng chính sách của mình riêng cho thời gian lưu trữ tối đa của danh sách dịch vụ và số lượng tối đa của các bản ghi dịch vụ và bản thu hồi.



## Các Thay Đổi Cần Thiết Trong Đặc Tả Cấu Trúc Chung


### Chứng Chỉ Khóa

Như một phần nằm ngoài phạm vi của đề xuất này.
Thêm vào các đề xuất ECIES 144 và 145.


### Các Cấu Trúc Trung Gian Mới

Thêm các cấu trúc mới cho Lease2, MetaLease, LeaseSet2Header, và OfflineSignature.
Có hiệu lực kể từ phiên bản phát hành 0.9.38.


### Các Loại NetDB Mới

Thêm cấu trúc cho mỗi loại leaseset mới, được kết hợp từ trên.
Cho LeaseSet2, EncryptedLeaseSet, và MetaLeaseSet,
có hiệu lực kể từ phiên bản phát hành 0.9.38.
Cho Ghi Nhớ Dịch Vụ và Danh Sách Dịch Vụ,
mở đầu và chưa được lên lịch.


### Loại Chữ Ký Mới

Thêm RedDSA_SHA512_Ed25519 Loại 11.
Khóa công khai là 32 bytes; khóa riêng là 32 bytes; băm là 64 bytes; chữ ký là 64 bytes.



## Các Thay Đổi Cần Thiết Trong Đặc Tả Mã Hóa

Ngoài phạm vi của đề xuất này.
Xem các đề xuất 144 và 145.



## Những Thay Đổi Cần Thiết Trong I2NP

Thêm ghi chú: LS2 chỉ có thể được công bố tới floodfills với một phiên bản tối thiểu.


### Tin Nhắn Tìm Kiếm Trong Cơ Sở Dữ Liệu

Thêm loại tra cứu danh sách dịch vụ.

Các Thay Đổi
``````
