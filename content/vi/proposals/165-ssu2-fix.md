---
title: "Đề xuất I2P số #165: Sửa lỗi SSU2"
number: "165"
author: "weko, orignal, the Anonymous, zzz"
created: "2024-01-19"
lastupdated: "2024-11-17"
status: "Open"
thread: "http://i2pforum.i2p/viewforum.php?f=13"
target: "0.9.62"
---

Đề xuất bởi weko, orignal, the Anonymous và zzz.

### Tổng quan

Tài liệu này đề xuất các thay đổi đối với SSU2 sau một cuộc tấn công vào I2P khai thác các lỗ hổng trong SSU2. Mục tiêu chính là tăng cường bảo mật và ngăn chặn các cuộc tấn công Từ chối Dịch vụ Phân tán (DDoS) và các nỗ lực gỡ danh tính.

### Mô hình mối đe dọa

Một kẻ tấn công tạo ra các RI giả mới (bộ định tuyến không tồn tại): đây là RI bình thường, nhưng hắn đặt địa chỉ, cổng, các khóa s và i từ bộ định tuyến Bob thật, sau đó hắn tấn công mạng. Khi chúng ta cố gắng kết nối với bộ định tuyến này (như chúng ta nghĩ là thật), chúng ta, như Alice có thể kết nối tới địa chỉ này, nhưng không thể chắc chắn điều gì đã thực hiện với RI của Bob thật sự. Điều này có thể và đã được sử dụng cho một cuộc tấn công Từ chối Dịch vụ Phân tán (tạo một lượng lớn các RI như vậy và tấn công mạng), điều này cũng có thể làm cho các cuộc tấn công gỡ danh tính dễ dàng hơn bằng cách gán tội cho các bộ định tuyến tốt và không gán cho các bộ định tuyến của kẻ tấn công, nếu chúng ta cấm IP với nhiều RI (thay vì phân phối xây dựng đường hầm tới các RI này như đến một bộ định tuyến).

### Các biện pháp khắc phục tiềm năng

#### 1. Sửa lỗi với hỗ trợ cho các bộ định tuyến cũ (trước khi thay đổi)

.. _overview-1:

Tổng quan
^^^^^^^^

Giải pháp khắc phục để hỗ trợ kết nối SSU2 với các bộ định tuyến cũ.

Hành vi
^^^^^^^^

Hồ sơ bộ định tuyến của Bob nên có cờ 'verified', mặc định là sai cho tất cả các bộ định tuyến mới (chưa có hồ sơ). Khi cờ 'verified' là sai, chúng ta không bao giờ thực hiện kết nối với SSU2 như Alice tới Bob - chúng ta không thể chắc chắn trong RI. Nếu Bob kết nối với chúng ta (Alice) với NTCP2 hoặc SSU2 hoặc chúng ta (Alice) kết nối với Bob bằng NTCP2 một lần (chúng ta có thể xác minh RouterIdent của Bob trong các trường hợp này) - cờ được đặt thành đúng.

Vấn đề
^^^^^^^^

Vì vậy, có một vấn đề với lũ RI giả chỉ có SSU2: chúng ta không thể tự mình xác minh nó và buộc phải đợi khi bộ định tuyến thật sự sẽ kết nối với chúng ta.

#### 2. Xác minh RouterIdent trong quá trình tạo kết nối

.. _overview-2:

Tổng quan
^^^^^^^^

Thêm khối “RouterIdent” cho SessionRequest và SessionCreated.

Định dạng khả thi của khối RouterIdent
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1 byte cờ, 32 byte RouterIdent. Flag_0: 0 nếu nhận RouterIdent; 1 nếu gửi RouterIdent

Hành vi
^^^^^^^^

Alice (cần(1), có thể(2)) gửi trong payload khối RouterIdent Flag_0 = 0 và RouterIdent của Bob. Bob (cần(3), có thể(4)) kiểm tra nếu đó là RouterIdent của mình, và nếu không: kết thúc phiên với lý do “Sai RouterIdent”, nếu đó là RouterIdent của mình: gửi khối RI với 1 trong Flag_0 và RouterIdent của Bob.

Với (1) Bob không hỗ trợ các bộ định tuyến cũ. Với (2) Bob hỗ trợ các bộ định tuyến cũ, nhưng có thể là nạn nhân của DDoS từ các bộ định tuyến đang cố gắng kết nối với RI giả. Với (3) Alice không hỗ trợ các bộ định tuyến cũ. Với (4) Alice hỗ trợ các bộ định tuyến cũ và đang sử dụng một sơ đồ kết hợp: Sửa lỗi 1 cho bộ định tuyến cũ và Sửa lỗi 2 cho bộ định tuyến mới. Nếu RI báo phiên bản mới, nhưng trong khi kết nối chúng ta không nhận được khối RouterIdent - kết thúc và loại bỏ RI.

.. _problems-1:

Vấn đề
^^^^^^^^

Kẻ tấn công có thể ngụy trang bộ định tuyến giả của mình như cũ, và với (4) chúng ta vẫn đang đợi ‘verified’ như trong sửa lỗi 1.

Ghi chú
^^^^^

Thay vì 32 byte RouterIdent, chúng ta có thể sử dụng 4 byte siphash-of-the-hash, một HKDF hoặc cái gì đó khác, mà phải là đủ.

#### 3. Bob đặt i = RouterIdent

.. _overview-3:

Tổng quan
^^^^^^^^

Bob sử dụng RouterIdent của mình làm khóa i.

.. _behavior-1:

Hành vi
^^^^^^^^

Bob (cần(1), có thể(2)) sử dụng RouterIdent của mình làm khóa i cho SSU2.

Alice với (1) chỉ kết nối nếu i = RouterIdent của Bob. Alice với (2) sử dụng sơ đồ kết hợp (sửa lỗi 3 và 1): nếu i = RouterIdent của Bob, chúng ta có thể thực hiện kết nối, nếu không chúng ta cần xác minh nó trước (xem sửa lỗi 1).

Với (1) Alice không hỗ trợ các bộ định tuyến cũ. Với (2) Alice hỗ trợ các bộ định tuyến cũ.

.. _problems-2:

Vấn đề
^^^^^^^^

Kẻ tấn công có thể ngụy trang bộ định tuyến giả của mình như cũ, và với (2), chúng ta vẫn đang đợi 'verified' như trong sửa lỗi 1.

.. _notes-1:

Ghi chú
^^^^^

Để tiết kiệm kích thước RI, tốt hơn nên thêm việc xử lý nếu khóa i không được chỉ định. Nếu có, thì i = RouterIdent. Trong trường hợp đó, Bob không hỗ trợ các bộ định tuyến cũ.

#### 4. Thêm một MixHash nữa vào KDF của SessionRequest

.. _overview-4:

Tổng quan
^^^^^^^^

Thêm MixHash(hash định danh của Bob) vào trạng thái NOISE của thông điệp "SessionRequest", ví dụ:
h = SHA256 (h || hash định danh của Bob).
Nó phải là MixHash cuối cùng được sử dụng như ad cho MÃ HÓA hoặc GIẢI MÃ.
Cần thêm cờ tiêu đề SSU2 bổ sung "Xác minh định danh Bob" = 0x02.

.. _behavior-4:

Hành vi
^^^^^^^^

- Alice thêm MixHash với hash định danh của Bob từ RouterInfo của Bob và sử dụng nó như ad cho MÃ HÓA và thiết lập cờ "Xác minh định danh Bob"
- Bob kiểm tra cờ "Xác minh định danh Bob" và thêm MixHash với hash định danh của mình và sử dụng nó ad như để GIẢI MÃ. Nếu AEAD/Chacha20/Poly1305 thất bại, Bob đóng phiên.

Khả năng tương thích với bộ định tuyến cũ
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Alice phải kiểm tra phiên bản bộ định tuyến của Bob và nếu nó thỏa mãn phiên bản tối thiểu hỗ trợ đề xuất này thì thêm MixHash này và thiết lập cờ "Xác minh định danh Bob". Nếu bộ định tuyến cũ hơn, Alice không thêm MixHash và không thiết lập cờ "Xác minh định danh Bob".
- Bob kiểm tra cờ "Xác minh định danh Bob" và thêm MixHash này nếu nó được thiết lập. Bộ định tuyến cũ không thiết lập cờ này và MixHash này không nên được thêm vào.

.. _problems-4:

Vấn đề
^^^^^^^^

- Kẻ tấn công có thể tuyên bố bộ định tuyến giả với phiên bản cũ hơn. Tại một thời điểm nào đó, bộ định tuyến cũ nên được sử dụng cẩn thận và sau khi chúng được xác minh bằng các cách khác.

### Khả năng tương thích ngược

Mô tả trong các sửa lỗi.

### Trạng thái hiện tại

i2pd: Sửa lỗi 1.
