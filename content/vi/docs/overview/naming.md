---
title: "Đặt tên và Sổ địa chỉ"
description: "Cách I2P ánh xạ tên máy chủ có thể đọc được sang các destination"
slug: "naming"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

Địa chỉ I2P là các khóa mật mã dài. Hệ thống đặt tên cung cấp một lớp thân thiện hơn trên các khóa đó **mà không cần giới thiệu một cơ quan trung tâm**. Tất cả các tên đều **cục bộ**—mỗi router độc lập quyết định hostname nào tham chiếu đến destination nào.

> **Cần tìm hiểu thêm?** Tài liệu [thảo luận về đặt tên](/docs/legacy/naming/) ghi lại các cuộc tranh luận thiết kế ban đầu, các đề xuất thay thế và nền tảng triết lý đằng sau hệ thống đặt tên phi tập trung của I2P.

---

## 1. Các thành phần

Lớp đặt tên của I2P bao gồm nhiều hệ thống con độc lập nhưng phối hợp với nhau:

1. **Dịch vụ đặt tên** – phân giải tên máy chủ thành các destination và xử lý [tên máy chủ Base32](#base32-hostnames).
2. **HTTP proxy** – chuyển các tra cứu `.i2p` đến router và đề xuất các dịch vụ jump khi không tìm thấy tên.
3. **Dịch vụ host-add** – các biểu mẫu kiểu CGI thêm các mục mới vào sổ địa chỉ cục bộ.
4. **Dịch vụ jump** – các trợ giúp từ xa trả về destination cho tên máy chủ được cung cấp.
5. **Sổ địa chỉ** – định kỳ tải và hợp nhất các danh sách máy chủ từ xa bằng "web of trust" (mạng lưới tin cậy) cục bộ.
6. **SusiDNS** – giao diện web để quản lý sổ địa chỉ, đăng ký và ghi đè cục bộ.

Thiết kế mô-đun này cho phép người dùng tự xác định ranh giới tin cậy của riêng họ và tự động hóa nhiều hay ít quy trình đặt tên tùy theo sở thích.

---

## 2. Dịch vụ Đặt tên

API đặt tên của router (`net.i2p.client.naming`) hỗ trợ nhiều backend thông qua thuộc tính có thể cấu hình `i2p.naming.impl=<class>`. Mỗi triển khai có thể cung cấp các chiến lược tra cứu khác nhau, nhưng tất cả đều chia sẻ cùng một mô hình tin cậy và phân giải.

### 2.1 Hosts.txt (legacy format)

Mô hình cũ sử dụng ba tệp văn bản thuần túy được kiểm tra theo thứ tự:

1. `privatehosts.txt`
2. `userhosts.txt`
3. `hosts.txt`

Mỗi dòng lưu trữ một ánh xạ `hostname=base64-destination`. Định dạng văn bản đơn giản này vẫn được hỗ trợ đầy đủ cho việc nhập/xuất, nhưng nó không còn là mặc định nữa do hiệu suất kém khi danh sách host vượt quá vài nghìn mục.

---

### 2.2 Blockfile Naming Service (default backend)

Được giới thiệu trong **phiên bản 0.8.8**, Dịch vụ Đặt tên Blockfile hiện là backend mặc định. Nó thay thế các tệp phẳng bằng một kho lưu trữ key/value trên đĩa dựa trên skiplist hiệu suất cao (`hostsdb.blockfile`) cung cấp tốc độ tra cứu nhanh hơn khoảng **10 lần**.

**Đặc điểm chính:** - Lưu trữ nhiều sổ địa chỉ logic (riêng tư, người dùng và hosts) trong một cơ sở dữ liệu nhị phân. - Duy trì khả năng tương thích với việc nhập/xuất hosts.txt cũ. - Hỗ trợ tra cứu ngược, metadata (ngày thêm, nguồn, bình luận) và bộ nhớ đệm hiệu quả. - Sử dụng cùng thứ tự tìm kiếm ba tầng: riêng tư → người dùng → hosts.

Cách tiếp cận này bảo toàn khả năng tương thích ngược trong khi cải thiện đáng kể tốc độ phân giải và khả năng mở rộng.

---

### 2.1 Hosts.txt (định dạng cũ)

Các nhà phát triển có thể triển khai các backend tùy chỉnh như: - **Meta** – tổng hợp nhiều hệ thống đặt tên. - **PetName** – hỗ trợ petnames được lưu trữ trong `petnames.txt`. - **AddressDB**, **Exec**, **Eepget**, và **Dummy** – cho phân giải bên ngoài hoặc dự phòng.

Triển khai blockfile vẫn là backend **được khuyến nghị** cho mục đích sử dụng chung do hiệu suất và độ tin cậy.

---

## 3. Base32 Hostnames

Tên máy chủ Base32 (`*.b32.i2p`) hoạt động tương tự như địa chỉ `.onion` của Tor. Khi bạn truy cập một địa chỉ `.b32.i2p`:

1. Router giải mã payload Base32.
2. Nó tái tạo destination trực tiếp từ khóa—**không cần tra cứu address-book**.

Điều này đảm bảo khả năng truy cập ngay cả khi không tồn tại tên máy chủ dễ đọc cho con người. Tên Base32 mở rộng được giới thiệu trong **phiên bản 0.9.40** hỗ trợ **LeaseSet2** và các điểm đến được mã hóa.

---

## 4. Address Book & Subscriptions

Ứng dụng sổ địa chỉ truy xuất danh sách máy chủ từ xa qua HTTP và hợp nhất chúng cục bộ theo các quy tắc tin cậy do người dùng cấu hình.

### 2.2 Dịch vụ đặt tên Blockfile (backend mặc định)

- Subscriptions là các URL `.i2p` tiêu chuẩn trỏ đến `hosts.txt` hoặc các nguồn cập nhật tăng dần.
- Các bản cập nhật được tải về định kỳ (mặc định mỗi giờ) và được xác thực trước khi hợp nhất.
- Xung đột được giải quyết theo nguyên tắc **đến trước, được phục vụ trước**, tuân theo thứ tự ưu tiên:  
  `privatehosts.txt` → `userhosts.txt` → `hosts.txt`.

#### Default Providers

Kể từ **I2P 2.3.0 (Tháng 6 năm 2023)**, hai nhà cung cấp đăng ký mặc định được bao gồm: - `http://i2p-projekt.i2p/hosts.txt` - `http://notbob.i2p/hosts.txt`

Sự dự phòng này cải thiện độ tin cậy trong khi vẫn duy trì mô hình tin cậy cục bộ. Người dùng có thể thêm hoặc xóa các đăng ký thông qua SusiDNS.

#### Incremental Updates

Các bản cập nhật gia tăng được tải về thông qua `newhosts.txt` (thay thế khái niệm `recenthosts.cgi` cũ hơn). Endpoint này cung cấp các bản cập nhật delta hiệu quả **dựa trên ETag**—chỉ trả về các mục mới kể từ yêu cầu trước đó hoặc `304 Not Modified` khi không có thay đổi.

---

### 2.3 Các Backend Thay thế và Plug-in

- **Dịch vụ Host-add** (`add*.cgi`) cho phép gửi thủ công các ánh xạ tên-đến-destination. Luôn xác minh destination trước khi chấp nhận.  
- **Dịch vụ Jump** phản hồi với khóa thích hợp và có thể chuyển hướng qua HTTP proxy với tham số `?i2paddresshelper=`.  
  Các ví dụ phổ biến: `stats.i2p`, `identiguy.i2p`, và `notbob.i2p`.  
  Những dịch vụ này **không phải là cơ quan tin cậy**—người dùng phải tự quyết định sử dụng dịch vụ nào.

---

## 5. Managing Entries Locally (SusiDNS)

SusiDNS có sẵn tại: `http://127.0.0.1:7657/susidns/`

Bạn có thể: - Xem và chỉnh sửa sổ địa chỉ cục bộ. - Quản lý và ưu tiên các đăng ký. - Nhập/xuất danh sách hosts. - Cấu hình lịch trình tải xuống.

**Mới trong I2P 2.8.1 (Tháng 3 năm 2025):** - Đã thêm tính năng "sắp xếp theo mới nhất". - Cải thiện xử lý đăng ký (sửa lỗi không nhất quán ETag).

Tất cả thay đổi vẫn ở **local**—sổ địa chỉ của mỗi router là duy nhất.

---

## 3. Tên máy chủ Base32

Theo RFC 9476, I2P đã đăng ký **`.i2p.alt`** với GNUnet Assigned Numbers Authority (GANA) kể từ **tháng 3 năm 2025 (I2P 2.8.1)**.

**Mục đích:** Ngăn chặn rò rỉ DNS vô tình từ phần mềm cấu hình sai.

- Các DNS resolver tuân thủ RFC 9476 sẽ **không chuyển tiếp** các tên miền `.alt` đến DNS công cộng.
- Phần mềm I2P xử lý `.i2p.alt` tương đương với `.i2p`, loại bỏ hậu tố `.alt` trong quá trình phân giải.
- `.i2p.alt` **không** nhằm thay thế `.i2p`; đây là biện pháp bảo vệ kỹ thuật, không phải thương hiệu mới.

---

## 4. Sổ Địa Chỉ & Đăng Ký

- **Destination keys:** 516–616 byte (Base64)  
- **Hostname:** Tối đa 67 ký tự (bao gồm `.i2p`)  
- **Ký tự cho phép:** a–z, 0–9, `-`, `.` (không có dấu chấm kép, không viết hoa)  
- **Dành riêng:** `*.b32.i2p`  
- **ETag và Last-Modified:** được sử dụng tích cực để giảm thiểu băng thông  
- **Kích thước trung bình của hosts.txt:** ~400 KB cho ~800 host (con số ví dụ)  
- **Sử dụng băng thông:** ~10 byte/giây nếu tải về mỗi 12 giờ

---

## 8. Security Model and Philosophy

I2P cố ý hy sinh tính duy nhất toàn cầu để đổi lấy phi tập trung hóa và bảo mật—một ứng dụng trực tiếp của **Tam giác Zooko**.

**Nguyên tắc chính:** - **Không có cơ quan trung ương:** tất cả các tra cứu đều ở cục bộ.   - **Chống lại việc chiếm đoạt DNS:** các truy vấn được mã hóa tới các khóa công khai đích.   - **Ngăn chặn tấn công Sybil:** không có cơ chế bỏ phiếu hay đặt tên dựa trên đồng thuận.   - **Ánh xạ bất biến:** một khi đã tồn tại liên kết cục bộ, nó không thể bị ghi đè từ xa.

Các hệ thống đặt tên dựa trên blockchain (ví dụ: Namecoin, ENS) đã khám phá việc giải quyết cả ba cạnh của tam giác Zooko, nhưng I2P cố ý tránh chúng do độ trễ, độ phức tạp và sự không tương thích về mặt triết lý với mô hình tin cậy cục bộ của nó.

---

## 9. Compatibility and Stability

- Không có tính năng đặt tên nào bị loại bỏ trong giai đoạn 2023–2025.
- Định dạng Hosts.txt, dịch vụ jump, subscription và tất cả các triển khai API đặt tên vẫn hoạt động bình thường.
- Dự án I2P duy trì **khả năng tương thích ngược** nghiêm ngặt trong khi giới thiệu các cải tiến về hiệu suất và bảo mật (cô lập NetDB, phân tách Sub-DB, v.v.).

---

## 10. Best Practices

- Chỉ giữ những subscription đáng tin cậy; tránh các danh sách host lớn, không rõ nguồn gốc.
- Sao lưu `hostsdb.blockfile` và `privatehosts.txt` trước khi nâng cấp hoặc cài đặt lại.
- Thường xuyên xem xét các jump service và vô hiệu hóa những dịch vụ bạn không còn tin tưởng.
- Lưu ý: address book của bạn định nghĩa phiên bản I2P world của riêng bạn—**mọi hostname đều là cục bộ**.

---

### Further Reading

- [Thảo luận về Đặt tên](/docs/legacy/naming/)  
- [Đặc tả Blockfile](/docs/specs/blockfile/)  
- [Định dạng File Cấu hình](/docs/specs/configuration/)  
- [Naming Service Javadoc](http://idk.i2p/javadoc-i2p/net/i2p/client/naming/package-summary.html)

---
