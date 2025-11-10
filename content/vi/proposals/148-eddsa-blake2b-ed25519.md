---
title: "RedDSA-BLAKE2b-Ed25519"
number: "148"
author: "zzz"
created: "2019-03-12"
lastupdated: "2019-04-11"
status: "Open"
thread: "http://zzz.i2p/topics/2689"
---

## Tổng quan

Đề xuất này thêm vào một loại chữ ký mới sử dụng BLAKE2b-512 với chuỗi cá nhân hóa và muối, để thay thế SHA-512. Điều này sẽ loại bỏ ba lớp tấn công có thể xảy ra.

## Động lực

Trong quá trình thảo luận và thiết kế NTCP2 (đề xuất 111) và LS2 (đề xuất 123), chúng tôi đã xem xét ngắn gọn các phương thức tấn công có thể xảy ra và cách ngăn chặn chúng. Ba trong số các phương thức này là Tấn Công Mở Rộng Độ Dài, Tấn Công Giao Thoa Giao Thức, và Nhận Diện Thông Điệp Trùng Lặp.

Đối với cả NTCP2 và LS2, chúng tôi quyết định rằng các phương thức tấn công này không liên quan trực tiếp đến các đề xuất đang có, và bất kỳ giải pháp nào cũng xung đột với mục tiêu tối thiểu hóa các nguyên thủy mới. Ngoài ra, chúng tôi xác định rằng tốc độ của các hàm băm trong các giao thức này không phải là yếu tố quan trọng trong các quyết định của chúng tôi. Do đó, chúng tôi chủ yếu trì hoãn giải pháp cho một đề xuất riêng biệt. Mặc dù chúng tôi đã thêm một số tính năng cá nhân hóa vào đặc tả LS2, nhưng chúng tôi không yêu cầu bất kỳ hàm băm mới nào.

Nhiều dự án, như ZCash [ZCASH]_, đang sử dụng các hàm băm và thuật toán chữ ký dựa trên các thuật toán mới hơn mà không dễ bị các phương thức tấn công sau đây.

### Tấn Công Mở Rộng Độ Dài

SHA-256 và SHA-512 dễ bị Tấn Công Mở Rộng Độ Dài (LEA) [LEA]_. Đây là trường hợp khi dữ liệu thực tế được ký, không phải là băm của dữ liệu. Trong hầu hết các giao thức I2P (truyền tải, gói dữ liệu, netdb, và những thứ khác), dữ liệu thực tế được ký. Một ngoại lệ là tệp SU3, nơi băm được ký. Ngoại lệ khác là gói dữ liệu đã ký cho DSA (loại chữ ký 0) chỉ, nơi băm được ký. Đối với các loại chữ ký gói dữ liệu khác, dữ liệu được ký.

### Tấn Công Giao Thoa Giao Thức

Dữ liệu đã ký trong các giao thức I2P có thể dễ bị Tấn Công Giao Thoa Giao Thức (CPA) do thiếu sự phân tách miền. Điều này cho phép kẻ tấn công sử dụng dữ liệu nhận được trong một ngữ cảnh (chẳng hạn như gói dữ liệu đã ký) và trình bày nó như là dữ liệu đã ký hợp lệ trong một ngữ cảnh khác (chẳng hạn như truyền tải hoặc cơ sở dữ liệu mạng). Mặc dù không chắc rằng dữ liệu đã ký từ một ngữ cảnh sẽ được phân tích như là dữ liệu hợp lệ trong một ngữ cảnh khác, nhưng khó hoặc không thể phân tích tất cả các tình huống để biết chắc chắn. Ngoài ra, trong một số ngữ cảnh, có thể kẻ tấn công làm cho nạn nhân ký dữ liệu đặc thù có thể là dữ liệu hợp lệ trong một ngữ cảnh khác. Một lần nữa, khó hoặc không thể phân tích tất cả các tình huống để biết chắc chắn.

### Nhận Diện Thông Điệp Trùng Lặp

Các giao thức I2P có thể dễ bị Nhận Diện Thông Điệp Trùng Lặp (DMI). Điều này có thể cho phép kẻ tấn công nhận diện rằng hai thông điệp đã ký có cùng nội dung, ngay cả khi các thông điệp và chữ ký của chúng đã được mã hóa. Mặc dù không chắc chắn do các phương thức mã hóa được sử dụng trong I2P, nhưng khó hoặc không thể phân tích tất cả các tình huống để biết chắc chắn. Bằng cách sử dụng hàm băm cung cấp phương pháp để thêm muối ngẫu nhiên, tất cả chữ ký sẽ khác nhau ngay cả khi ký dữ liệu giống nhau. Mặc dù Red25519 như được định nghĩa trong đề xuất 123 thêm một muối ngẫu nhiên vào hàm băm, điều này không giải quyết được vấn đề cho các tập cho thuê không mã hóa.

### Tốc độ

Mặc dù không phải là động lực chính cho đề xuất này, SHA-512 tương đối chậm, và có sẵn các hàm băm nhanh hơn.

## Mục tiêu

- Ngăn chặn các tấn công trên
- Tối thiểu hóa việc sử dụng các nguyên thủy mật mã mới
- Sử dụng các nguyên thủy mật mã đã được chứng minh và tiêu chuẩn
- Sử dụng các đường cong tiêu chuẩn
- Sử dụng các nguyên thủy nhanh hơn nếu có

## Thiết kế

Chỉnh sửa loại chữ ký RedDSA_SHA512_Ed25519 hiện có để sử dụng BLAKE2b-512 thay cho SHA-512. Thêm các chuỗi cá nhân hóa duy nhất cho từng trường hợp sử dụng. Loại chữ ký mới có thể được sử dụng cho cả lease sets không mờ và bị mờ.

## Lý do

- BLAKE2b không dễ bị LEA [BLAKE2]_.
- BLAKE2b cung cấp một cách tiêu chuẩn để thêm các chuỗi cá nhân hóa cho việc phân tách miền.
- BLAKE2b cung cấp một cách tiêu chuẩn để thêm muối ngẫu nhiên để ngăn DMI.
- BLAKE2b nhanh hơn SHA-256 và SHA-512 (và MD5) trên phần cứng hiện đại, theo [BLAKE2]_.
- Ed25519 vẫn là loại chữ ký nhanh nhất của chúng tôi, nhanh hơn nhiều so với ECDSA, ít nhất là trong Java.
- Ed25519 [ED25519-REFS]_ yêu cầu một hàm băm mật mã 512-bit. Nó không chỉ định SHA-512. BLAKE2b cũng rất thích hợp cho hàm băm.
- BLAKE2b có sẵn rộng rãi trong các thư viện cho nhiều ngôn ngữ lập trình, chẳng hạn như Noise.

## Đặc tả

Sử dụng BLAKE2b-512 không khóa như trong [BLAKE2]_ với muối và cá nhân hóa. Tất cả các ứng dụng của chữ ký BLAKE2b sẽ sử dụng một chuỗi cá nhân hóa dài 16 ký tự.

Khi được sử dụng trong việc ký RedDSA_BLAKE2b_Ed25519, Một muối ngẫu nhiên được phép, tuy nhiên không cần thiết, vì thuật toán chữ ký thêm 80 byte dữ liệu ngẫu nhiên (xem đề xuất 123). Nếu muốn, khi đang băm dữ liệu để tính toán r, thiết lập một muối ngẫu nhiên 16-byte mới BLAKE2b cho mỗi chữ ký. Khi tính toán S, thiết lập lại muối về mặc định của toàn số không.

Khi được sử dụng trong việc kiểm tra RedDSA_BLAKE2b_Ed25519, không sử dụng muối ngẫu nhiên, sử dụng mặc định của toàn số không.

Các tính năng muối và cá nhân hóa không được chỉ định trong [RFC-7693]_; sử dụng các tính năng đó như đã chỉ định trong [BLAKE2]_.

### Loại Chữ Ký

Đối với RedDSA_BLAKE2b_Ed25519, thay thế hàm băm SHA-512 trong RedDSA_SHA512_Ed25519 (loại chữ ký 11, như được định nghĩa trong đề xuất 123) bằng BLAKE2b-512. Không thay đổi các điểm khác.

Chúng tôi không cần một sự thay thế cho EdDSA_SHA512_Ed25519ph (loại chữ ký 8) cho tệp su3, bởi vì phiên bản đã băm trước của EdDSA không dễ bị ảnh hưởng bởi LEA. EdDSA_SHA512_Ed25519 (loại chữ ký 7) không được hỗ trợ cho tệp su3.

=======================  ===========  ======  =====
        Loại             Mã Loại       Từ     Sử Dụng
=======================  ===========  ======  =====
RedDSA_BLAKE2b_Ed25519       12        TBD    Chỉ cho Định danh Bộ định tuyến, Đích đến và các tập lease mã hóa; không bao giờ được sử dụng cho Định danh Bộ định tuyến
=======================  ===========  ======  =====

### Chiều Dài Dữ Liệu Cấu Trúc Chung

Điều sau áp dụng cho loại chữ ký mới.

==================================  =============
            Loại Dữ Liệu               Chiều Dài    
==================================  =============
Hàm băm                                  64      
Khóa Riêng                               32      
Khóa Công                                32      
Chữ Ký                                   64      
==================================  =============

### Cá Nhân Hóa

Để cung cấp sự phân tách miền cho các ứng dụng khác nhau của chữ ký, chúng tôi sẽ sử dụng tính năng cá nhân hóa BLAKE2b.

Tất cả các ứng dụng của chữ ký BLAKE2b sẽ sử dụng chuỗi cá nhân hóa dài 16 ký tự. Bất kỳ ứng dụng mới nào cũng phải được thêm vào bảng này, với một cá nhân hóa duy nhất.

NTCP 1 và SSU handshake sử dụng dưới đây cho dữ liệu đã ký được định nghĩa trong handshake chính nó. RouterInfos đã ký trong Thông điệp Cơ sở Dữ liệu Lưu trữ sẽ sử dụng cá nhân hóa Mục NetDb, như được lưu trữ trong NetDB.

==================================  ==========================
         Ứng dụng                   16 Byte Cá Nhân Hóa
==================================  ==========================
I2CP SessionConfig                  "I2CP_SessionConf"
NetDB Entries (RI, LS, LS2)         "network_database"
NTCP 1 handshake                    "NTCP_1_handshake"
Signed Datagrams                    "sign_datagramI2P"
Streaming                           "streaming_i2psig"
SSU handshake                       "SSUHandshakeSign"
SU3 Files                           không hỗ trợ, không được hỗ trợ
Unit tests                          "test1234test5678"
==================================  ==========================

## Ghi chú

## Vấn đề

- Phương án thay thế 1: Đề xuất 146; Cung cấp sự kháng cự cho LEA
- Phương án thay thế 2: Ed25519ctx trong RFC 8032; Cung cấp sự kháng cự cho LEA và cá nhân hóa. Đã được tiêu chuẩn hóa, nhưng có ai sử dụng không? Xem [RFC-8032]_ và [ED25519CTX]_.
- Việc băm "có khóa" có ích cho chúng tôi không?

## Di chuyển

Giống như khi triển khai các loại chữ ký trước đó.

Chúng tôi có kế hoạch thay đổi bộ định tuyến mới từ loại 7 sang loại 12 làm mặc định. Chúng tôi có kế hoạch cuối cùng di chuyển các bộ định tuyến hiện có từ loại 7 sang loại 12, sử dụng quy trình "chìa khóa lại" đã sử dụng sau khi loại 7 được giới thiệu. Chúng tôi có kế hoạch thay đổi đích mới từ loại 7 sang loại 12 làm mặc định. Chúng tôi có kế hoạch thay đổi các đích được mã hóa mới từ loại 11 sang loại 13 làm mặc định.

Chúng tôi sẽ hỗ trợ làm mờ từ loại 7, 11, và 12 sang loại 12. Chúng tôi sẽ không hỗ trợ làm mờ loại 12 sang loại 11.

Các bộ định tuyến mới có thể bắt đầu sử dụng loại chữ ký mới theo mặc định sau một vài tháng. Các đích mới có thể bắt đầu sử dụng loại chữ ký mới theo mặc định sau có lẽ một năm.

Đối với phiên bản bộ định tuyến tối thiểu 0.9.TBD, các bộ định tuyến phải đảm bảo:

- Không lưu trữ (hoặc phân tán) RI hoặc LS với loại chữ ký mới cho các bộ định tuyến có phiên bản nhỏ hơn 0.9.TBD.
- Khi xác minh một lưu trữ netdb, không lấy RI hoặc LS với loại chữ ký mới từ các bộ định tuyến có phiên bản nhỏ hơn 0.9.TBD.
- Các bộ định tuyến với loại chữ ký mới trong RI của chúng không thể kết nối với các bộ định tuyến có phiên bản nhỏ hơn 0.9.TBD, cả với NTCP, NTCP2, hay SSU.
- Các kết nối truyền tải và gói dữ liệu đã ký sẽ không hoạt động với các bộ định tuyến có phiên bản nhỏ hơn 0.9.TBD, nhưng không có cách nào để biết điều đó, vì vậy loại chữ ký mới không nên được sử dụng theo mặc định trong một vài tháng hoặc năm sau khi 0.9.TBD được phát hành.

## Tham khảo

.. [BLAKE2] https://blake2.net/blake2.pdf

.. [ED25519CTX] https://moderncrypto.org/mail-archive/curves/2017/000925.html

.. [ED25519-REFS] "Chữ ký nhanh với bảo mật cao" của Daniel J. Bernstein, Niels Duif, Tanja Lange, Peter Schwabe, và Bo-Yin Yang. http://cr.yp.to/papers.html#ed25519

.. [EDDSA-FAULTS] https://news.ycombinator.com/item?id=15414760

.. [LEA] https://en.wikipedia.org/wiki/Length_extension_attack

.. [RFC-7693] https://tools.ietf.org/html/rfc7693

.. [RFC-8032] https://tools.ietf.org/html/rfc8032

.. [ZCASH] https://github.com/zcash/zips/tree/master/protocol/protocol.pdf
