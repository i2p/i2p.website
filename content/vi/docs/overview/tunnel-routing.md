---
title: "Định tuyến Tunnel"
description: "Tổng quan về thuật ngữ tunnel I2P, cấu trúc và hoạt động"
slug: "tunnel-routing"
lastUpdated: "2026-03"
accurateFor: "0.9.68"
---

## Tổng quan

Trang này chứa tổng quan về thuật ngữ và hoạt động của tunnel I2P, với các liên kết đến các trang kỹ thuật chi tiết hơn và các đặc tả kỹ thuật.

Như đã giải thích ngắn gọn trong [phần giới thiệu](/docs/overview/intro/), I2P xây dựng các "tunnel" ảo - những đường dẫn tạm thời và một chiều qua một chuỗi các router. Những tunnel này được phân loại thành tunnel đến (inbound tunnel) (nơi mọi thứ được đưa vào đều hướng về phía người tạo ra tunnel) hoặc tunnel đi (outbound tunnel) (nơi người tạo tunnel đẩy các thông điệp ra xa khỏi họ). Khi Alice muốn gửi một thông điệp cho Bob, cô ấy sẽ (thông thường) gửi nó qua một trong những tunnel đi hiện có của mình với hướng dẫn cho điểm cuối của tunnel đó chuyển tiếp nó đến router cổng cho một trong những tunnel đến hiện tại của Bob, và tunnel này sẽ chuyển thông điệp đến Bob.

![Alice kết nối qua tunnel gửi đi của cô ấy đến Bob thông qua tunnel nhận của anh ấy](/images/tunnelSending.svg)

```
A: Outbound Gateway (Alice)
B: Outbound Participant
C: Outbound Endpoint
D: Inbound Gateway
E: Inbound Participant
F: Inbound Endpoint (Bob)
```
---

## Từ vựng Tunnel

- **Tunnel gateway** - router đầu tiên trong một tunnel. Đối với inbound tunnel, đây là router được đề cập trong LeaseSet được xuất bản trong [cơ sở dữ liệu mạng](/docs/overview/network-database/). Đối với outbound tunnel, gateway là router khởi tạo. (ví dụ: cả A và D ở trên)

- **Tunnel endpoint** - router cuối cùng trong một tunnel. (ví dụ: cả C và F ở trên)

- **Tunnel participant** - tất cả các router trong tunnel ngoại trừ gateway hoặc endpoint (ví dụ: cả B và E ở trên)

- **n-Hop tunnel** - một tunnel với số lượng nhảy giữa các router cụ thể, ví dụ:
  - **0-hop tunnel** - một tunnel mà gateway cũng là điểm cuối
  - **1-hop tunnel** - một tunnel mà gateway giao tiếp trực tiếp với điểm cuối
  - **2-(hoặc nhiều hơn)-hop tunnel** - một tunnel có ít nhất một người tham gia tunnel trung gian. (sơ đồ trên bao gồm hai 2-hop tunnel - một outbound từ Alice, một inbound đến Bob)

- **Tunnel ID** - Một [số nguyên 4 byte](/docs/specs/common-structures/#type_TunnelId) khác nhau cho mỗi hop trong một tunnel, và duy nhất giữa tất cả các tunnel trên một router. Được chọn ngẫu nhiên bởi người tạo tunnel.

---

## Thông tin Xây dựng Tunnel

Các router thực hiện ba vai trò (gateway, participant, endpoint) được cung cấp các phần dữ liệu khác nhau trong [Tunnel Build Message](/docs/specs/tunnel-creation/) ban đầu để hoàn thành nhiệm vụ của chúng:

**Tunnel gateway nhận được:**

- **tunnel encryption key** - một [khóa riêng AES](/docs/specs/common-structures/#type_SessionKey) để mã hóa các thông điệp và hướng dẫn đến hop tiếp theo
- **tunnel IV key** - một [khóa riêng AES](/docs/specs/common-structures/#type_SessionKey) để mã hóa kép IV đến hop tiếp theo
- **reply key** - một [khóa công khai AES](/docs/specs/common-structures/#type_SessionKey) để mã hóa phản hồi cho yêu cầu xây dựng tunnel
- **reply IV** - IV để mã hóa phản hồi cho yêu cầu xây dựng tunnel
- **tunnel id** - số nguyên 4 byte (chỉ dành cho inbound gateway)
- **next hop** - router nào là router tiếp theo trong đường dẫn (trừ khi đây là tunnel 0-hop và gateway cũng là endpoint)
- **next tunnel id** - ID tunnel trên hop tiếp theo

**Tất cả các thành viên trung gian của tunnel đều nhận được:**

- **tunnel encryption key** - một [khóa riêng AES](/docs/specs/common-structures/#type_SessionKey) để mã hóa thông điệp và chỉ thị tới hop tiếp theo
- **tunnel IV key** - một [khóa riêng AES](/docs/specs/common-structures/#type_SessionKey) để mã hóa kép IV tới hop tiếp theo
- **reply key** - một [khóa công khai AES](/docs/specs/common-structures/#type_SessionKey) để mã hóa phản hồi cho yêu cầu xây dựng tunnel
- **reply IV** - IV để mã hóa phản hồi cho yêu cầu xây dựng tunnel
- **tunnel id** - số nguyên 4 byte
- **next hop** - router nào là router tiếp theo trong đường dẫn
- **next tunnel id** - ID tunnel trên hop tiếp theo

**Tunnel endpoint nhận được:**

- **tunnel encryption key** - một [khóa riêng AES](/docs/specs/common-structures/#type_SessionKey) để mã hóa các tin nhắn và hướng dẫn tới điểm cuối (chính nó)
- **tunnel IV key** - một [khóa riêng AES](/docs/specs/common-structures/#type_SessionKey) để mã hóa kép IV tới điểm cuối (chính nó)
- **reply key** - một [khóa công AES](/docs/specs/common-structures/#type_SessionKey) để mã hóa phản hồi cho yêu cầu xây dựng tunnel (chỉ áp dụng cho outbound endpoints)
- **reply IV** - IV để mã hóa phản hồi cho yêu cầu xây dựng tunnel (chỉ áp dụng cho outbound endpoints)
- **tunnel id** - số nguyên 4 byte (chỉ áp dụng cho outbound endpoints)
- **reply router** - inbound gateway của tunnel để gửi phản hồi qua đó (chỉ áp dụng cho outbound endpoints)
- **reply tunnel id** - tunnel ID của reply router (chỉ áp dụng cho outbound endpoints)

Chi tiết có trong [đặc tả tạo tunnel](/docs/specs/tunnel-creation/).

---

## Gộp Tunnel

Nhiều tunnel cho một mục đích cụ thể có thể được nhóm thành một "tunnel pool", như được mô tả trong [đặc tả tunnel](/docs/specs/tunnel-implementation/#tunnel.pooling). Điều này cung cấp khả năng dự phòng và băng thông bổ sung. Các pool được sử dụng bởi chính router được gọi là "exploratory tunnels". Các pool được sử dụng bởi các ứng dụng được gọi là "client tunnels".

---

## Độ dài Tunnel

Như đã đề cập ở trên, mỗi client yêu cầu router của họ cung cấp các tunnel bao gồm ít nhất một số lượng hop nhất định. Quyết định về số lượng router có trong tunnel outbound và inbound của một người có ảnh hưởng quan trọng đến độ trễ, thông lượng, độ tin cậy và tính ẩn danh được cung cấp bởi I2P - càng nhiều peer mà các thông điệp phải đi qua, thì càng mất nhiều thời gian để đến đích và càng có khả năng một trong những router đó sẽ bị lỗi sớm. Càng ít router trong một tunnel, thì càng dễ dàng cho kẻ thù thực hiện các cuộc tấn công phân tích lưu lượng và xuyên thủng tính ẩn danh của ai đó. Độ dài tunnel được chỉ định bởi các client thông qua [tùy chọn I2CP](/docs/specs/i2cp/#options). Số lượng hop tối đa trong một tunnel là 7.

### tunnel 0-hop

Khi không có router từ xa nào trong tunnel, người dùng có khả năng chối bỏ hợp lý rất cơ bản (vì không ai biết chắc chắn rằng peer đã gửi tin nhắn cho họ không chỉ đơn giản là chuyển tiếp nó như một phần của tunnel). Tuy nhiên, việc thực hiện một cuộc tấn công phân tích thống kê sẽ khá dễ dàng và nhận thấy rằng các tin nhắn nhắm đến một đích cụ thể luôn được gửi qua một gateway duy nhất. Phân tích thống kê đối với các tunnel gửi đi 0-hop phức tạp hơn, nhưng có thể hiển thị thông tin tương tự (mặc dù sẽ khó thực hiện hơn một chút).

### tunnel 1-hop

Với chỉ một remote router trong tunnel, người dùng có cả khả năng chối bỏ hợp lý và tính ẩn danh cơ bản, miễn là họ không đối đầu với kẻ thù nội bộ (như được mô tả trong [mô hình đe dọa](/docs/overview/threat-model/)). Tuy nhiên, nếu kẻ thù vận hành đủ số lượng router sao cho remote router duy nhất trong tunnel thường xuyên là một trong những router bị xâm phạm đó, chúng sẽ có thể thực hiện cuộc tấn công phân tích lưu lượng thống kê như trên.

### tunnel 2-hop

Với hai hoặc nhiều router từ xa trong một tunnel, chi phí để thực hiện cuộc tấn công phân tích lưu lượng tăng lên, vì nhiều router từ xa sẽ phải bị xâm phạm để thực hiện cuộc tấn công đó.

### Tunnel 3-hop (hoặc nhiều hơn)

Để giảm khả năng bị [một số cuộc tấn công](https://blog.torproject.org/one-cell-enough-break-tors-anonymity/), nên sử dụng 3 hoặc nhiều hơn các bước nhảy (hop) để đạt mức bảo vệ cao nhất. [Các nghiên cứu gần đây](https://blog.torproject.org/one-cell-enough-break-tors-anonymity/) cũng kết luận rằng việc sử dụng nhiều hơn 3 bước nhảy không mang lại thêm sự bảo vệ nào.

### Độ dài mặc định của tunnel

Router sử dụng tunnel 2-hop theo mặc định cho các exploratory tunnel của nó. Các giá trị mặc định của client tunnel được thiết lập bởi ứng dụng, sử dụng [tùy chọn I2CP](/docs/specs/i2cp/#options). Hầu hết các ứng dụng sử dụng 2 hoặc 3 hop làm giá trị mặc định.

---

## Kiểm tra Tunnel

Tất cả các tunnel đều được kiểm tra định kỳ bởi người tạo ra chúng thông qua việc gửi một DeliveryStatusMessage qua outbound tunnel và hướng đến một inbound tunnel khác (kiểm tra cả hai tunnel cùng lúc). Nếu một trong hai tunnel thất bại trong một số lần kiểm tra liên tiếp, nó sẽ được đánh dấu là không còn hoạt động. Nếu nó được sử dụng cho inbound tunnel của client, một leaseSet mới sẽ được tạo ra. Các lỗi kiểm tra tunnel cũng được phản ánh trong [đánh giá dung lượng trong hồ sơ peer](/docs/overview/peer-selection/#capacity).

---

Việc tạo tunnel được xử lý bằng cách [garlic routing](/docs/overview/garlic-routing/) một Tunnel Build Message đến một router, yêu cầu họ tham gia vào tunnel (cung cấp cho họ tất cả thông tin thích hợp như trên, cùng với một chứng chỉ, hiện tại là chứng chỉ 'null', nhưng sẽ hỗ trợ hashcash hoặc các chứng chỉ không miễn phí khác khi cần thiết). Router đó chuyển tiếp thông điệp đến hop tiếp theo trong tunnel. Chi tiết có trong [đặc tả tạo tunnel](/docs/specs/tunnel-creation/).

## Tạo Tunnel

---

Mã hóa đa lớp được xử lý bởi [garlic encryption](/docs/overview/garlic-routing/) của các thông điệp tunnel. Chi tiết có trong [đặc tả tunnel](/docs/specs/tunnel-implementation/). IV của mỗi hop được mã hóa với một khóa riêng biệt như được giải thích ở đó.

## Mã hóa Tunnel

---

---

## Công việc tương lai

- Các kỹ thuật kiểm tra tunnel khác có thể được sử dụng, chẳng hạn như garlic wrapping một số bài kiểm tra thành các cloves, kiểm tra riêng lẻ từng thành viên tham gia tunnel, v.v.

- Chuyển sang mặc định tunnel khám phá 3-hop.

- Trong một phiên bản phát hành tương lai xa, các tùy chọn chỉ định cài đặt pooling, mixing và tạo chaff có thể được triển khai.

- Trong một phiên bản phát hành tương lai xa, các giới hạn về số lượng và kích thước tin nhắn được phép trong suốt vòng đời của tunnel có thể được triển khai (ví dụ: không quá 300 tin nhắn hoặc 1MB mỗi phút).

---

## Xem Thêm

- [Đặc tả tunnel](/docs/specs/tunnel-implementation/)
- [Đặc tả tạo tunnel](/docs/specs/tunnel-creation/)
- [Tunnel một chiều](/docs/legacy/unidirectional/)
- [Đặc tả thông điệp tunnel](/docs/specs/tunnel-message/)
- [Định tuyến garlic](/docs/overview/garlic-routing/)
- [ElGamal/AES+SessionTag](/docs/specs/elgamal-aes/)
- [Tùy chọn I2CP](/docs/specs/i2cp/#options)
