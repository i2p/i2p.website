---
title: "Phần mở rộng nhanh (BEP 6) Cho phép nhanh với định danh máy ngang hàng theo băm đích"
number: "172"
author: "dr|z3d"
created: "2026-08-10"
lastupdated: "2026-08-10"
status: "Bản nháp"
toc: true
---

## Tổng quan

Gói mở rộng BEP 6 (Fast Extension) bao gồm năm tính năng: **Have All / Have None**, **Reject Requests**, **Suggestions**, và **Allowed Fast**. Giao thức truyền tải — bit đàm phán, ID tin nhắn và ngữ nghĩa choke — không phụ thuộc vào phương tiện truyền dẫn và hoạt động nguyên bản trên dòng truyền I2P. Phần duy nhất của BEP 6 không thể ánh xạ trực tiếp sang I2P là **việc tạo tập hợp Allowed Fast**, vì nó được định nghĩa dựa trên địa chỉ IPv4 của máy ngang hàng. Các máy ngang hàng I2P không có địa chỉ IP; chúng được xác định bằng các giá trị băm đích dài 32 byte.

Đề xuất này chuẩn hóa việc tạo bộ dữ liệu "Allowed Fast" gốc trên I2P để tất cả các client torrent I2P đều tạo ra các bộ "allowed fast" *giống hệt nhau* cho cùng một peer và torrent, giúp tính năng này trở nên hữu ích (và có thể kiểm chứng được) trên mọi triển khai khác nhau.

## Động lực

Các máy ngang hàng mới cần có được một vài mảnh dữ liệu đầu tiên trước khi cơ chế "cho-đổi-lấy" của BitTorrent có thể hoạt động hiệu quả. Trên I2P, quá trình này diễn ra chậm hơn so với mạng rõ (clearnet): việc thiết lập kết nối và truyền tải mảnh dữ liệu phải đi qua nhiều chặng trong các đường hầm có độ trễ cao, do đó khoảng thời gian giữa lúc kết nối và lúc nhận được unchoke (giải khóa gửi dữ liệu) đầu tiên mang tính tương hỗ sẽ dài hơn. Tính năng Cho Phép Nhanh (Allowed Fast) trực tiếp giải quyết vấn đề này — một máy ngang hàng mới bắt đầu được phép nhận một số lượng nhỏ mảnh dữ liệu ngay cả khi đang bị khóa (choked), từ đó nhận dữ liệu ngay lập tức và có thể bắt đầu chia sẻ lại (reciprocate) sớm hơn.

BEP tham chiếu 6 tính toán tập hợp nhanh cho phép dựa trên địa chỉ IPv4 của máy ngang hàng để đảm bảo rằng *người gửi* có thể chọn các mảnh dữ liệu duy nhất đối với *người nhận* (một người dùng có nhiều địa chỉ IP không thể thu thập nhiều tập hợp). Trên I2P, mã băm địa chỉ đích của máy ngang hàng đảm nhận vai trò ràng buộc tương tự và sẵn có cho cả hai đầu cuối của mọi kết nối, nhờ đó tập hợp trở nên xác định được và có thể xác minh cục bộ — điều mà phương pháp dựa trên IP không thể cung cấp.

## Sửa đổi đối với BEP 6

Việc thương lượng phần mở rộng Fast và cả bốn loại tin nhắn được áp dụng nguyên样:

- Đàm phán: bit nhỏ nhất thứ ba của byte dành riêng cuối cùng, `reserved[7] |= 0x04`, cả hai đầu
- Have All `<len=0x0001><op=0x0E>`, Have None `<len=0x0001><op=0x0F>`
- Gợi ý mảnh `<len=0x0005><op=0x0D><index>`
- Từ chối yêu cầu `<len=0x000D><op=0x10><index><begin><length>`
- Cho phép nhanh `<len=0x0005><op=0x11><index>`
- Mỗi yêu cầu đều dẫn đến đúng một phản hồi (mảnh hoặc từ chối); việc kẹt (choke) không còn ngầm từ chối các yêu cầu đang chờ

Sự khác biệt duy nhất nằm trong việc tạo tập Hợp lệ Nhanh, thay thế các byte IP bằng các byte của băm đích đến của nút ngang hàng.

### Lệch hướng: byte băm thay vì IP đã được che

Tham chiếu BEP 6, bước (1):

```
x = 0xFFFFFF00 & ip
```
Điều đó lấy ba byte từ địa chỉ IPv4 của máy ngang hàng và **đặt byte thứ 4 bằng không**. Đây là một phương pháp ước lượng theo mạng con: những người dùng có thể lấy nhiều địa chỉ IP trong cùng mạng /24 không nên nhận được nhiều bộ nút cho phép nhanh khác nhau.

Phiên bản I2P của chúng tôi thay thế điều này bằng bốn byte đầu tiên của băm đích 32 byte của peer:

```
x = first 4 bytes of peer destination hash
```
Sự khác biệt so với phiên bản tham chiếu:

> "Đó là 3 byte của địa chỉ IP theo sau bởi một byte zero. Bạn là 4 byte của băm. Nó khác với BEP 6 vì không có địa chỉ IP và nó không đặt byte thứ 4 bằng zero."

Cả hai đầu của một kết nối I2P đều đã biết mã băm đích của máy ngang hàng (đó là địa chỉ mà kết nối được thiết lập đến/từ), do đó không cần trao đổi thêm, không cần phát hiện NAT và không cần phát hiện IP bên ngoài — những thứ này hoàn toàn không tồn tại trên I2P.

### Thuật toán tạo nhanh được phép

Gọi `hash` là mã băm đích 32 byte của máy ngang hàng nhận, `infohash` là mã băm thông tin 20 byte của torrent, `sz` là số lượng các phần trong torrent, `k` là số lượng cuối cùng các phần trong tập hợp cho phép nhanh (10, như trong BEP 6), và `a` là tập hợp đầu ra:

```
x = hash[0:4]  ++  infohash        (1)
while |a| < k:
    x = SHA1(x)                    (2)
    for i in [0:5] and |a| < k:    (3)
        y = x[i*4 : i*4+4]         (4)
        index = y % sz             (5)
        if index not in a:         (6)
            add index to a         (7)
```
Ghi chú:

- 4 byte của băm đích thay thế 3 byte IP đã bị che dấu. Cả bốn byte đều mang entropy băm; không có byte nào bị đặt bằng không.
- Như trong BEP 6, chuỗi SHA1 tạo ra một dãy giả ngẫu nhiên dài, được chia thành các chỉ số mảnh; `k = 10` phù hợp với giá trị mặc định tham chiếu.
- Thông điệp Allowed Fast chỉ mang tính chất gợi ý: người nhận KHÔNG ĐƯỢC hiểu rằng người gửi đang có mảnh đó — mà chỉ rằng người gửi sẽ cung cấp mảnh đó ngay cả khi bị nghẽn.

## Lợi ích

| Khu vực            | Lợi ích                                                                                                                                                                                       |
| ------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Độ trễ khởi động    | Các peer mới kéo các mảnh đầu tiên ngay cả khi bị nghẽn, rút ngắn quá trình tăng tốc tit-for-tat vốn chậm hơn trên các đường hầm I2P đa nút                                                                 |
| Tính xác định       | Tập hợp là hàm thuần túy của băm đích + infohash, do đó mọi triển khai đều tính ra cùng một tập — không giống như BEP 6 dựa trên IP, nơi quan điểm của người gửi về IP người nhận có thể khác nhau (do NAT) |
| Khả năng kiểm chứng | Peer nhận biết rõ băm đích của chính mình và có thể tự tính lại, xác minh tập hợp, từ đó phát hiện người gửi hành xử sai                                                                                |
| Không cần cơ chế IP | Không cần vượt NAT, phát hiện IP công cộng hay các phương pháp suy đoán mạng con — tất cả đều bất khả thi hoặc vô nghĩa trên I2P                                                                          |
| Liên kết định danh  | Chỉ một tập nhanh được cho phép cho mỗi đích. Người dùng có nhiều đích sẽ nhận được một tập cho mỗi cái — cùng tính chất chống gian lận mà mặt nạ IP cung cấp trên mạng rõ ràng                             |
| Riêng tư            | Không có địa chỉ IP nào được truyền hay ngụ ý trong quá trình tính toán                                                                                                                              |
| Băng thông          | Have All / Have None thay thế trường bit đầy đủ trong các torrent lớn; Reject loại bỏ các yêu cầu lại dư thừa                                                                                       |
## Các yếu tố cần cân nhắc khi triển khai

- **Danh tính ngang hàng**: băm đích của ngang hàng được lấy từ kết nối streaming (đích của phiên) và là giá trị giống nhau mà cả hai đầu đều sử dụng. Với kết nối đi, hãy dùng đích mà bạn đã kết nối tới; với kết nối đến, dùng đích mà kết nối đến từ đó.
- **Thương lượng**: gửi `reserved[7] |= 0x04` trong quá trình bắt tay; chỉ gửi các tin nhắn Mở rộng Nhanh nếu phần bắt tay của ngang hàng cũng đặt bit này; nếu một ngang hàng gửi tin nhắn Mở rộng Nhanh mà không thương lượng, hãy đóng kết nối.
- **Có Toàn bộ / Không có Gì**: ngay sau khi bắt tay, hãy gửi chính xác một trong các tin nhắn: bitfield / Có Toàn bộ / Không có Gì. Gửi Có Toàn bộ đối với seed, Không có Gì cho đến khi có mảnh đầu tiên.
- **Phía gửi Cho phép Nhanh**: chỉ quảng bá các mảnh mà bạn thực sự có; phía nhận có thể yêu cầu chúng ngay cả khi bị nghẽn. Giới hạn tập *được phục vụ* (ví dụ: từ chối các yêu cầu allowed-fast từ một ngang hàng đã giữ hơn `k` mảnh, theo hướng dẫn BEP 6).
- **Phía nhận Cho phép Nhanh**: lưu trữ tập hợp; cho phép yêu cầu các mảnh đó ngay cả khi bị nghẽn; tùy chọn xác minh tập hợp bằng cách tính lại từ băm đích của bạn và infohash, và bỏ qua các mảnh không nằm trong tập hợp đã tính.
- **Từ chối**: mọi yêu cầu PHẢI nhận đúng một phản hồi; khi bị nghẽn, hãy từ chối mọi thứ không nằm trong tập Cho phép Nhanh thay vì im lặng ngắt kết nối ngang hàng.
- **Kích thước tập hợp**: dùng `k = 10` để đảm bảo tương thích; các ngang hàng có thể tự do chọn `k` thấp hơn khi tải cao, nhưng cả hai đầu đều nên quảng bá chỉ những gì họ thực sự phục vụ.
- **Giới hạn mảnh**: `index = y % sz` phải dùng tổng số mảnh `sz` của torrent; bỏ qua các chỉ số >= sz (phòng thủ), vì chuỗi băm không bị giới hạn theo phạm vi mảnh.
- **Tương thích ngược**: các client không thương lượng bit fast sẽ đơn giản không bao giờ thấy các tin nhắn này; không cần thay đổi giao thức nào khác.

## Các triển khai tham khảo

Thuật toán nhỏ gọn và tự chứa — chỉ vài chục dòng trong bất kỳ ngôn ngữ nào. Cả ba ví dụ bên dưới đều tính toán ra tập hợp giống hệt nhau với đầu vào giống nhệt nhau (`hash[0:4] ++ infohash`, chuỗi SHA1, `y % sz`, giới hạn `k = 10`).

### Java

```java
// I2P: peer.getPeerID().getDestHash() is the 32-byte destination hash.
// Big-endian word reads build each candidate piece index from the SHA1 chain.
import java.security.MessageDigest;
import java.util.HashSet;
import java.util.Set;

public static Set<Integer> generateAllowedFastSet(byte[] destHash, byte[] infohash, int pieces) {
    Set<Integer> rv = new HashSet<>(10);
    if (destHash == null || infohash == null || pieces <= 0) {
        return rv;
    }
    byte[] x = new byte[24];
    System.arraycopy(destHash, 0, x, 0, 4);          // 4 hash bytes, no IP, no zeroed 4th byte
    System.arraycopy(infohash, 0, x, 4, Math.min(20, infohash.length));
    MessageDigest md = MessageDigest.getInstance("SHA-1");
    while (rv.size() < 10) {
        x = md.digest(x);
        for (int i = 0; i < 5 && rv.size() < 10; i++) {
            long y = ((x[i * 4] & 0xFFL) << 24) | ((x[i * 4 + 1] & 0xFFL) << 16)
                   | ((x[i * 4 + 2] & 0xFFL) << 8) | (x[i * 4 + 3] & 0xFFL);
            rv.add((int) (y % pieces));
        }
    }
    return rv;
}
```
### C++

```cpp
// Peer identity input is the 32-byte destination hash available on the connection.
#include <cstdint>
#include <set>
#include <vector>

extern std::vector<uint8_t> sha1(const std::vector<uint8_t>& in); // e.g. OpenSSL SHA1()

std::set<int> generate_allowed_fast_set(const std::vector<uint8_t>& dest_hash,
                                        const std::vector<uint8_t>& infohash,
                                        int pieces) {
    std::set<int> rv;
    if (dest_hash.size() < 4 || infohash.size() < 20 || pieces <= 0) { return rv; }
    std::vector<uint8_t> x(dest_hash.begin(), dest_hash.begin() + 4); // 4 hash bytes,
                                                                      // no IP mask
    x.insert(x.end(), infohash.begin(), infohash.begin() + 20);
    while (rv.size() < 10) {
        x = sha1(x);
        for (int i = 0; i < 5 && rv.size() < 10; i++) {
            uint32_t y = (uint32_t(x[i * 4]) << 24) | (uint32_t(x[i * 4 + 1]) << 16) |
                         (uint32_t(x[i * 4 + 2]) << 8) | uint32_t(x[i * 4 + 3]);
            rv.insert(int(y % uint32_t(pieces)));
        }
    }
    return rv;
}
```
### Python

```python
import hashlib

def generate_allowed_fast_set(dest_hash: bytes, infohash: bytes, pieces: int) -> set:
    """4 bytes of the destination hash stand in for the masked IP; no byte is zeroed."""
    rv = set()
    if len(dest_hash) < 4 or len(infohash) < 20 or pieces <= 0:
        return rv
    x = dest_hash[:4] + infohash[:20]
    while len(rv) < 10:
        x = hashlib.sha1(x).digest()
        for i in range(5):
            if len(rv) >= 10:
                break
            y = int.from_bytes(x[i * 4 : i * 4 + 4], "big")
            rv.add(y % pieces)
    return rv
```
## Tương thích

- **Tương thích về mặt dây nối**: bit thương lượng và định dạng tin nhắn giống hệt từng byte so với BEP 6 mạng rõ (clearnet); chỉ đầu vào tạo bộ là khác biệt.
- **Không tương tác được giữa các mạng**: một khách hàng I2P và một khách hàng mạng rõ dù sao cũng không thể kết nối tới nhau; sự sai lệch này chỉ ảnh hưởng đến các byte định danh ngang hàng, không bao giờ ảnh hưởng đến định dạng truyền tải.
- **Trong nội bộ I2P**: bất kỳ khách hàng nào triển khai đề xuất này đều tính toán ra các bộ Fast được Cho Phép giống hệt nhau và có thể cung cấp hoặc xác minh chúng thay thế cho nhau. Các khách hàng bỏ qua Allowed Fast sẽ coi đây là một lời khuyên không hiệu lực và chỉ mất đi lợi ích khởi động nhanh.

## Các câu hỏi chưa có lời giải

1. Kích thước bộ `k` nên giữ cố định ở mức 10, hay nên thích ứng theo tải (ví dụ: giảm khi tải yêu cầu cao) như cho phép bởi BEP 6?
2. Người nhận có nên xác minh bộ dữ liệu dựa trên băm đích của riêng họ và loại bỏ các chỉ số không khớp (phòng thủ chống người gửi lỗi hoặc độc hại)? Khuyến nghị: nên.
3. Chọn phần *đầu* 4 byte (byte 0-3) như trình bày, hay 4 byte *cuối cùng* — bất kỳ khoảng 4 byte cố định nào cũng cho các đặc tính tương tự; dùng phần đầu giữ thứ tự byte tự nhiên trong mã tham chiếu (`hash[0:4]`).

## Công nghệ trước đó

- Tham khảo: [BEP 6 Fast Extension](https://www.bittorrent.org/beps/bep_0006.html)
- Triển khai tham chiếu của I2PSnark: `PeerState.sendAllowedFast()` /
  `generateAllowedFastSet()` trong
  `apps/i2psnark/java/src/org/klomp/snark/PeerState.java` (@since 0.9.71+)
- Hoạt động cùng với BEP 40 (ưu tiên ngang hàng chính thống) và BEP 21 (chia sẻ từng phần), cả hai đều được I2PSnark hỗ trợ
