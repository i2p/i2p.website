---
title: "Mục netDB Mới"
number: "123"
author: "zzz, str4d, orignal"
created: "2016-01-16"
lastupdated: "2020-07-18"
status: "Mở"
thread: "http://zzz.i2p/topics/2051"
supercedes: "110, 120, 121, 122"
toc: true
---

## Trạng thái

Một phần của đề xuất này đã hoàn thành và được triển khai trong 0.9.38 và 0.9.39.   Các cấu trúc chung, I2CP, I2NP và các đặc tả khác   hiện đã được cập nhật để phản ánh các thay đổi được hỗ trợ hiện nay.

Các phần đã hoàn thành vẫn có thể được sửa đổi nhỏ.   Các phần khác của đề xuất này vẫn đang trong quá trình phát triển   và có thể được sửa đổi đáng kể.

Tìm kiếm dịch vụ (loại 9 và 11) là ưu tiên thấp   và chưa được lên lịch, có thể được tách thành một đề xuất riêng.

## Tổng quan

Đây là bản cập nhật và tổng hợp của 4 đề xuất sau:

- 110 LS2
- 120 Meta LS2 cho đa kết nối quy mô lớn
- 121 LS2 được mã hóa
- 122 Tìm kiếm dịch vụ không xác thực (anycasting)

Các đề xuất này phần lớn độc lập, nhưng vì lý do hợp lý, chúng tôi định nghĩa và sử dụng   một định dạng chung cho một số trong số chúng.

Các đề xuất sau có liên quan một phần:

- 140 Đa kết nối vô hình (không tương thích với đề xuất này)
- 142 Mẫu mã hóa mới (cho mã hóa đối xứng mới)
- 144 ECIES-X25519-AEAD-Ratchet
- 145 ECIES-P256
- 146 Red25519
- 148 EdDSA-BLAKE2b-Ed25519
- 149 B32 cho LS2 được mã hóa
- 150 Giao thức Garlic Farm
- 151 ECDSA Blinding

## Đề xuất

Đề xuất này định nghĩa 5 loại DatabaseEntry mới và quy trình   lưu trữ và truy xuất chúng từ cơ sở dữ liệu mạng,   cũng như phương pháp ký và xác minh chữ ký.

### Mục tiêu

- Tương thích ngược
- LS2 có thể sử dụng với đa kết nối kiểu cũ
- Không yêu cầu mã hóa hoặc nguyên thủy mới để hỗ trợ
- Duy trì sự tách biệt giữa mã hóa và chữ ký; hỗ trợ tất cả các phiên bản hiện tại và tương lai
- Cho phép khóa ký ngoại tuyến tùy chọn
- Giảm độ chính xác của dấu thời gian để giảm khả năng định danh
- Cho phép mã hóa mới cho các điểm đến
- Cho phép đa kết nối quy mô lớn
- Sửa nhiều vấn đề với LS được mã hóa hiện tại
- Tùy chọn ẩn danh để giảm khả năng nhìn thấy bởi các floodfill
- Hỗ trợ cả khóa đơn và nhiều khóa có thể thu hồi
- Tìm kiếm dịch vụ để dễ dàng tìm kiếm outproxy, khởi động DHT ứng dụng,  
  và các mục đích sử dụng khác
- Không làm hỏng bất cứ thứ gì phụ thuộc vào băm điểm đến nhị phân 32 byte, ví dụ như bittorrent
- Thêm tính linh hoạt cho leaseset thông qua các thuộc tính, giống như chúng ta có trong routerinfos.
- Đặt dấu thời gian công bố và thời gian hết hạn thay đổi vào tiêu đề, để nó hoạt động ngay cả  
  khi nội dung được mã hóa (không suy ra dấu thời gian từ lease sớm nhất)
- Tất cả các loại mới nằm trong cùng không gian DHT và cùng vị trí như leaseset hiện tại,  
  để người dùng có thể di chuyển từ LS cũ sang LS2,  
  hoặc chuyển đổi giữa LS2, Meta và Encrypted,  
  mà không cần thay đổi Destination hoặc băm.
- Một Destination hiện tại có thể được chuyển sang sử dụng khóa ngoại tuyến,  
  hoặc trở lại khóa trực tuyến, mà không cần thay đổi Destination hoặc băm.

### Mục tiêu không đạt được / Ngoài phạm vi

- Thuật toán quay DHT mới hoặc tạo số ngẫu nhiên chung
- Loại mã hóa mới cụ thể và lược đồ mã hóa end-to-end  
  để sử dụng loại mới sẽ nằm trong một đề xuất riêng.  
  Không có mã hóa mới nào được chỉ định hoặc thảo luận ở đây.
- Mã hóa mới cho RIs hoặc xây dựng tunnel.  
  Sẽ nằm trong một đề xuất riêng.
- Phương pháp mã hóa, truyền và nhận tin nhắn I2NP DLM / DSM / DSRM.  
  Không thay đổi.
- Cách tạo và hỗ trợ Meta, bao gồm giao tiếp nội bộ giữa các router, quản lý, chuyển đổi và phối hợp.  
  Hỗ trợ có thể được thêm vào I2CP, hoặc i2pcontrol, hoặc một giao thức mới.  
  Điều này có thể hoặc không được chuẩn hóa.
- Cách thực hiện và quản lý các tunnel có thời gian hết hạn dài hơn, hoặc hủy các tunnel hiện tại.  
  Điều đó cực kỳ khó khăn, và nếu không có nó, bạn không thể có một quá trình tắt máy hợp lý.
- Thay đổi mô hình mối đe dọa
- Định dạng lưu trữ ngoại tuyến, hoặc phương pháp lưu trữ/truy xuất/chia sẻ dữ liệu.
- Chi tiết triển khai không được thảo luận ở đây và được để cho từng dự án.

### Cơ sở

LS2 thêm các trường để thay đổi loại mã hóa và cho các thay đổi giao thức trong tương lai.

LS2 được mã hóa sửa một số vấn đề bảo mật với LS được mã hóa hiện tại bằng cách   sử dụng mã hóa bất đối xứng cho toàn bộ tập hợp các lease.

Meta LS2 cung cấp đa kết nối linh hoạt, hiệu quả, hiệu quả và quy mô lớn.

Bản ghi dịch vụ và Danh sách dịch vụ cung cấp các dịch vụ anycast như tra cứu tên   và khởi động DHT.

### Các loại dữ liệu NetDB

Các số loại được sử dụng trong Tin nhắn Tìm kiếm/Lưu trữ Cơ sở dữ liệu I2NP.

Cột end-to-end đề cập đến việc truy vấn/phản hồi có được gửi đến một Destination trong một Tin nhắn Tỏi hay không.

Các loại hiện tại:

| NetDB Data | Loại Tìm kiếm | Loại Lưu trữ |
|------------|-------------|------------|
| bất kỳ        | 0           | bất kỳ        |
| LS         | 1           | 1          |
| RI         | 2           | 0          |
| khám phá| 3           | DSRM       |
Các loại mới:

| NetDB Data     | Loại Tìm kiếm | Loại Lưu trữ | Tiêu đề LS2 chuẩn? | Gửi end-to-end? |
|----------------|-------------|------------|------------------|------------------|
| LS2            | 1           | 3          | có              | có              |
| LS2 được mã hóa  | 1           | 5          | không               | không               |
| Meta LS2       | 1           | 7          | có              | không               |
| Bản ghi Dịch vụ | n/a         | 9          | có              | không               |
| Danh sách Dịch vụ   | 4           | 11         | không               | không               |
### Ghi chú

- Các loại tìm kiếm hiện đang là bit 3-2 trong Tin nhắn Tìm kiếm Cơ sở dữ liệu.  
  Bất kỳ loại bổ sung nào sẽ yêu cầu sử dụng bit 4.

- Tất cả các loại lưu trữ đều là số lẻ vì các bit trên trong trường loại của Tin nhắn Lưu trữ Cơ sở dữ liệu  
  bị các router cũ bỏ qua.  
  Chúng tôi thà để việc phân tích cú pháp thất bại như một LS hơn là như một RI được nén.

- Loại nên được chỉ định rõ ràng, ngầm định hay không rõ ràng trong dữ liệu được bao phủ bởi chữ ký?

### Quy trình Tìm kiếm/Lưu trữ

Các loại 3, 5 và 7 có thể được trả về như phản hồi cho một tìm kiếm leaseset tiêu chuẩn (loại 1).   Loại 9 không bao giờ được trả về như phản hồi cho một tìm kiếm.   Loại 11 được trả về như phản hồi cho một loại tìm kiếm dịch vụ mới (loại 11).

Chỉ loại 3 có thể được gửi trong một tin nhắn Tỏi từ client đến client.

### Định dạng

Các loại 3, 7 và 9 đều có định dạng chung::

```text
Standard LS2 Header
- as defined below

Type-Specific Part
- as defined below in each part

Standard LS2 Signature:
- Length as implied by sig type of signing key
```
Tiêu đề LS2 chuẩn

Phần riêng cho loại

### Xem xét về Quyền riêng tư/Bảo mật

Chữ ký LS2 chuẩn:

## Tiêu đề LS2 chuẩn

Loại 5 (Được mã hóa) không bắt đầu bằng Destination và có định dạng khác. Xem bên dưới.

### Định dạng

```
Standard LS2 Header:
  - Type (1 byte)
    Not actually in header, but part of data covered by signature.
    Take from field in Database Store Message.
  - Destination (387+ bytes)
  - Published timestamp (4 bytes, big endian, seconds since epoch, rolls over in 2106)
  - Expires (2 bytes, big endian) (offset from published timestamp in seconds, 18.2 hours max)
  - Flags (2 bytes)
    Bit order: 15 14 ... 3 2 1 0
    Bit 0: If 0, no offline keys; if 1, offline keys
    Bit 1: If 0, a standard published leaseset.
           If 1, an unpublished leaseset. Should not be flooded, published, or
           sent in response to a query. If this leaseset expires, do not query the
           netdb for a new one, unless bit 2 is set.
    Bit 2: If 0, a standard published leaseset.
           If 1, this unencrypted leaseset will be blinded and encrypted when published.
           If this leaseset expires, query the blinded location in the netdb for a new one.
           If this bit is set to 1, set bit 1 to 1 also.
           As of release 0.9.42.
    Bits 3-15: set to 0 for compatibility with future uses
  - If flag indicates offline keys, the offline signature section:
    Expires timestamp (4 bytes, big endian, seconds since epoch, rolls over in 2106)
    Transient sig type (2 bytes, big endian)
    Transient signing public key (length as implied by sig type)
    Signature of expires timestamp, transient sig type, and public key,
    by the destination public key,
    length as implied by destination public key sig type.
    This section can, and should, be generated offline.
```
### Cơ sở

  - như được định nghĩa bên dưới

  - như được định nghĩa bên dưới cho từng phần

  - Độ dài như được ngụ ý bởi loại chữ ký của khóa ký

- Chưa công bố/đã công bố: Để sử dụng khi gửi một lưu trữ cơ sở dữ liệu end-to-end,
  router gửi có thể muốn chỉ ra rằng leaseset này không nên được
  gửi cho người khác. Hiện tại chúng tôi sử dụng các phương pháp heuristic để duy trì trạng thái này.

### Vấn đề

- Đã công bố: Thay thế logic phức tạp cần thiết để xác định 'phiên bản' của
  leaseset. Hiện tại, phiên bản là thời gian hết hạn của lease có thời gian hết hạn lâu nhất,
  và một router công bố phải tăng thời gian hết hạn đó lên ít nhất 1ms khi
  công bố một leaseset chỉ loại bỏ một lease cũ hơn.

- Hết hạn: Cho phép thời gian hết hạn của một mục netdb sớm hơn thời gian hết hạn của
  lease có thời gian hết hạn lâu nhất. Có thể không hữu ích cho LS2, nơi mà các leaseset
  dự kiến sẽ duy trì với thời gian hết hạn tối đa 11 phút, nhưng
  cho các loại mới khác, điều này là cần thiết (xem Meta LS và Bản ghi Dịch vụ bên dưới).

- Khóa ngoại tuyến là tùy chọn, để giảm độ phức tạp triển khai ban đầu/yêu cầu.

### Ghi chú

- Có thể giảm độ chính xác của dấu thời gian nhiều hơn nữa (10 phút?) nhưng sẽ phải thêm
  số phiên bản. Điều này có thể làm hỏng đa kết nối, trừ khi chúng ta có mã hóa bảo toàn thứ tự?
  Có lẽ không thể làm mà không có dấu thời gian.

- Thay thế: 3 byte dấu thời gian (epoch / 10 phút), 1-byte phiên bản, 2-byte hết hạn

- Loại được chỉ định rõ ràng hay ngầm định trong dữ liệu / chữ ký? Hằng số "Domain" cho chữ ký?

## Các loại DatabaseEntry mới

### LeaseSet 2

Loại 11 (Danh sách Dịch vụ) là tập hợp của nhiều Bản ghi Dịch vụ và có định dạng khác. Xem bên dưới.

- Các router không nên công bố một LS nhiều hơn một lần mỗi giây.
  Nếu họ làm vậy, họ phải tăng nhân tạo dấu thời gian công bố lên 1
  so với LS công bố trước đó.

TBD

    Standard LS flag (1)
Các loại 3, 7 và 9 sử dụng tiêu đề LS2 chuẩn, được chỉ định bên dưới:

    Standard LS2 type (3)
Thay đổi từ LeaseSet hiện tại:

    Hash of destination
    This hash is then used to generate the daily "routing key", as in LS1
Tìm kiếm với

    10 minutes, as in a regular LS.
Lưu trữ với

    Destination

### Định dạng

```
Standard LS2 Header as specified above

  Standard LS2 Type-Specific Part
  - Properties (Mapping as specified in common structures spec, 2 zero bytes if none)
  - Number of key sections to follow (1 byte, max TBD)
  - Key sections:
    - Encryption type (2 bytes, big endian)
    - Encryption key length (2 bytes, big endian)
      This is explicit, so floodfills can parse LS2 with unknown encryption types.
    - Encryption key (number of bytes specified)
  - Number of lease2s (1 byte)
  - Lease2s (40 bytes each)
    These are leases, but with a 4-byte instead of an 8-byte expiration,
    seconds since the epoch (rolls over in 2106)

  Standard LS2 Signature:
  - Signature
    If flag indicates offline keys, this is signed by the transient pubkey,
    otherwise, by the destination pubkey
    Length as implied by sig type of signing key
    The signature is of everything above.
```
### Cơ sở

- Các triển khai router có thể lưu trữ bộ nhớ đệm các khóa tạm thời và chữ ký để
  tránh xác minh mỗi lần. Đặc biệt, các floodfill, và các router ở
  cả hai đầu của các kết nối lâu dài, có thể hưởng lợi từ điều này.

- Khóa và chữ ký ngoại tuyến chỉ phù hợp với các điểm đến lâu dài,
  tức là máy chủ, không phải máy khách.

### Thảo luận

Lưu trữ tại

Thời gian hết hạn điển hình

Được công bố bởi

- Thêm dấu thời gian công bố, dấu thời gian hết hạn, cờ và thuộc tính
- Thêm loại mã hóa
- Loại bỏ khóa thu hồi

Đề xuất này tiếp tục sử dụng khóa công khai trong leaseset cho khóa mã hóa end-to-end, và để khóa công khai trong trường Destination không được sử dụng, như hiện nay. Loại mã hóa không được chỉ định trong chứng chỉ khóa Destination, nó sẽ vẫn là 0.

- Thuộc tính: Mở rộng và linh hoạt trong tương lai.
  Được đặt đầu tiên trong trường hợp cần thiết để phân tích cú pháp dữ liệu còn lại.

### Các vấn đề mã hóa mới

Một phương án thay thế bị từ chối là chỉ định loại mã hóa trong chứng chỉ khóa Destination, sử dụng khóa công khai trong Destination, và không sử dụng khóa công khai trong leaseset. Chúng tôi không có kế hoạch làm điều này.

- Nhiều cặp loại mã hóa/khóa công khai nhằm
  giúp chuyển đổi sang các loại mã hóa mới dễ dàng hơn. Cách khác để làm điều này
  là công bố nhiều leaseset, có thể sử dụng cùng các tunnel,
  như chúng ta đang làm hiện tại cho các destination DSA và EdDSA.
  Việc xác định loại mã hóa đầu vào trên một tunnel
  có thể được thực hiện bằng cơ chế thẻ phiên hiện tại,
  và/hoặc giải mã thử bằng từng khóa. Độ dài của các tin nhắn đầu vào
  cũng có thể cung cấp manh mối.

- Vị trí của khóa công khai thực tế không thay đổi.
- Loại mã hóa hoặc khóa công khai có thể thay đổi mà không thay đổi Destination.
- Loại bỏ trường thu hồi không sử dụng
- Tương thích cơ bản với các loại DatabaseEntry khác trong đề xuất này
- Cho phép nhiều loại mã hóa

- Vị trí của khóa công khai và loại mã hóa khác với RouterInfo
- Duy trì khóa công khai không sử dụng trong leaseset
- Yêu cầu triển khai trên toàn mạng; trong phương án thay thế, các loại mã hóa thử nghiệm có thể được sử dụng, nếu được các floodfill cho phép (nhưng xem các đề xuất liên quan 136 và 137 về hỗ trợ các loại chữ ký thử nghiệm). Đề xuất thay thế có thể dễ triển khai và thử nghiệm hơn cho các loại mã hóa thử nghiệm.

### Ghi chú

- Loại mã hóa đại diện cho sự kết hợp  
  của đường cong, độ dài khóa và lược đồ end-to-end,  
  bao gồm KDF và MAC, nếu có.

- Chúng tôi đã bao gồm một trường độ dài khóa, để LS2 có thể  
  được phân tích cú pháp và xác minh bởi floodfill ngay cả với các loại mã hóa chưa biết.

- Loại mã hóa mới đầu tiên được đề xuất sẽ  
  có thể là ECIES/X25519. Cách nó được sử dụng end-to-end  
  (một phiên bản sửa đổi nhẹ của ElGamal/AES+SessionTag  
  hoặc một cái gì đó hoàn toàn mới, ví dụ ChaCha/Poly) sẽ được chỉ định  
  trong một hoặc nhiều đề xuất riêng biệt.  
  Xem thêm các đề xuất ECIES 144 và 145.

### LS2 được mã hóa

Lợi ích của LS2:

- 8-byte expiration trong leases thay đổi thành 4 byte.

Nhược điểm của LS2:

Một phần điều này nằm ngoài phạm vi của đề xuất này,   nhưng ghi chú ở đây tạm thời vì chúng tôi chưa có   một đề xuất mã hóa riêng biệt nào.   Xem thêm các đề xuất ECIES 144 và 145.

- Nếu chúng ta từng triển khai thu hồi, chúng ta có thể làm điều đó với một trường hết hạn bằng không,  
  hoặc zero leases, hoặc cả hai. Không cần khóa thu hồi riêng biệt.

Mục tiêu:

    Standard LS flag (1)
LS2 được mã hóa không bao giờ được gửi trong một tin nhắn tỏi end-to-end.   Sử dụng LS2 chuẩn như trên.

    Encrypted LS2 type (5)
Thay đổi từ LeaseSet được mã hóa hiện tại:

    Hash of blinded sig type and blinded public key
    Two byte sig type (big endian, e.g. 0x000b) || blinded public key
    This hash is then used to generate the daily "routing key", as in LS1
Tìm kiếm với

    10 minutes, as in a regular LS, or hours, as in a meta LS.
Lưu trữ với

    Destination


### Định nghĩa

Lưu trữ tại

Thời gian hết hạn điển hình

    n-byte output from a cryptographically-secure random number generator.

    In addition to the requirement of CSRNG being cryptographically-secure (and thus
    suitable for generating key material), it MUST be safe
    for some n-byte output to be used for key material when the byte sequences immediately
    preceding and following it are exposed on the network (such as in a salt, or encrypted
    padding). Implementations that rely on a potentially-untrustworthy source should hash
    any output that is to be exposed on the network. See [PRNG references](http://projectbullrun.org/dual-ec/ext-rand.html) and [Tor dev discussion](https://lists.torproject.org/pipermail/tor-dev/2015-November/009954.html).

Được công bố bởi

    SHA-256 hash function that takes a personalization string p and data d, and
    produces an output of length 32 bytes.

    Use SHA-256 as follows::

        H(p, d) := SHA-256(p || d)

Chúng tôi định nghĩa các hàm sau tương ứng với các khối xây dựng mật mã được sử dụng   cho LS2 được mã hóa:

    The ChaCha20 stream cipher as specified in [RFC 7539 Section 2.4](https://tools.ietf.org/html/rfc7539#section-2.4), with the initial counter
    set to 1. S_KEY_LEN = 32 and S_IV_LEN = 12.

    ENCRYPT(k, iv, plaintext)
        Encrypts plaintext using the cipher key k, and nonce iv which MUST be unique for
        the key k. Returns a ciphertext that is the same size as the plaintext.

        The entire ciphertext must be indistinguishable from random if the key is secret.

    DECRYPT(k, iv, ciphertext)
        Decrypts ciphertext using the cipher key k, and nonce iv. Returns the plaintext.


CSRNG(n)

    The RedDSA signature scheme (corresponding to SigType 11) with key blinding.
    It has the following functions:

    DERIVE_PUBLIC(privkey)
        Returns the public key corresponding to the given private key.

    SIGN(privkey, m)
        Returns a signature by the private key privkey over the given message m.

    VERIFY(pubkey, m, sig)
        Verifies the signature sig against the public key pubkey and message m. Returns
        true if the signature is valid, false otherwise.

    It must also support the following key blinding operations:

    GENERATE_ALPHA(data, secret)
        Generate alpha for those who know the data and an optional secret.
        The result must be identically distributed as the private keys.

    BLIND_PRIVKEY(privkey, alpha)
        Blinds a private key, using a secret alpha.

    BLIND_PUBKEY(pubkey, alpha)
        Blinds a public key, using a secret alpha.
        For a given keypair (privkey, pubkey) the following relationship holds::

            BLIND_PUBKEY(pubkey, alpha) ==
            DERIVE_PUBLIC(BLIND_PRIVKEY(privkey, alpha))

H(p, d)

    X25519 public key agreement system. Private keys of 32 bytes, public keys of 32
    bytes, produces outputs of 32 bytes. It has the following
    functions:

    GENERATE_PRIVATE()
        Generates a new private key.

    DERIVE_PUBLIC(privkey)
        Returns the public key corresponding to the given private key.

    DH(privkey, pubkey)
        Generates a shared secret from the given private and public keys.

STREAM

    A cryptographic key derivation function which takes some input key material ikm (which
    should have good entropy but is not required to be a uniformly random string), a salt
    of length 32 bytes, and a context-specific 'info' value, and produces an output
    of n bytes suitable for use as key material.

    Use HKDF as specified in [RFC 5869](https://tools.ietf.org/html/rfc5869), using the HMAC hash function SHA-256
    as specified in [RFC 2104](https://tools.ietf.org/html/rfc2104). This means that SALT_LEN is 32 bytes max.


### Định dạng

SIG

- Các khóa mã hóa được sắp xếp theo thứ tự ưu tiên của máy chủ, ưu tiên cao nhất đầu tiên.  
  Hành vi mặc định của client là chọn khóa đầu tiên có  
  loại mã hóa được hỗ trợ. Client có thể sử dụng các thuật toán chọn khác  
  dựa trên hỗ trợ mã hóa, hiệu suất tương đối và các yếu tố khác.

DH

    Layer 0 data + Enc(layer 1 data + Enc(layer 2 data)) + Signature

HKDF(salt, ikm, info, n)

Định dạng LS2 được mã hóa gồm ba lớp lồng nhau:

#### Lớp 0 (ngoài)

Định dạng tổng thể trông như sau::

    1 byte

    Not actually in header, but part of data covered by signature.
    Take from field in Database Store Message.

Lưu ý rằng LS2 được mã hóa là ẩn danh. Destination không nằm trong tiêu đề.   Vị trí lưu trữ DHT là SHA-256(loại chữ ký || khóa công khai ẩn danh), và được quay hàng ngày.

    2 bytes, big endian
    This will always be type 11, identifying a Red25519 blinded key.

KHÔNG sử dụng tiêu đề LS2 chuẩn được chỉ định ở trên.

    Length as implied by sig type

Loại

    4 bytes, big endian

    Seconds since epoch, rolls over in 2106

Loại chữ ký khóa công khai ẩn danh

    2 bytes, big endian

    Offset from published timestamp in seconds, 18.2 hours max

Khóa công khai ẩn danh

    2 bytes

    Bit order: 15 14 ... 3 2 1 0

    Bit 0: If 0, no offline keys; if 1, offline keys

    Other bits: set to 0 for compatibility with future uses

Dấu thời gian công bố

    Present if flag indicates offline keys

    Expires timestamp
        4 bytes, big endian

        Seconds since epoch, rolls over in 2106

    Transient sig type
        2 bytes, big endian

    Transient signing public key
        Length as implied by sig type

    Signature
        Length as implied by blinded public key sig type

        Over expires timestamp, transient sig type, and transient public key.

        Verified with the blinded public key.

Hết hạn

    2 bytes, big endian

Cờ

    lenOuterCiphertext bytes

    Encrypted layer 1 data. See below for key derivation and encryption algorithms.

Dữ liệu khóa tạm thời

    Length as implied by sig type of the signing key used

    The signature is of everything above.

    If the flag indicates offline keys, the signature is verified with the transient
    public key. Otherwise, the signature is verified with the blinded public key.


#### Lớp 1 (giữa)

lenOuterCiphertext

    1 byte
    
    Bit order: 76543210

    Bit 0: 0 for everybody, 1 for per-client, auth section to follow

    Bits 3-1: Authentication scheme, only if bit 0 is set to 1 for per-client, otherwise 000
              000: DH client authentication (or no per-client authentication)
              001: PSK client authentication

    Bits 7-4: Unused, set to 0 for future compatibility

outerCiphertext

    Present if flag bit 0 is set to 1 and flag bits 3-1 are set to 000.

    ephemeralPublicKey
        32 bytes

    clients
        2 bytes, big endian

        Number of authClient entries to follow, 40 bytes each

    authClient
        Authorization data for a single client.
        See below for the per-client authorization algorithm.

        clientID_i
            8 bytes

        clientCookie_i
            32 bytes

Chữ ký

    Present if flag bit 0 is set to 1 and flag bits 3-1 are set to 001.

    authSalt
        32 bytes

    clients
        2 bytes, big endian

        Number of authClient entries to follow, 40 bytes each

    authClient
        Authorization data for a single client.
        See below for the per-client authorization algorithm.

        clientID_i
            8 bytes

        clientCookie_i
            32 bytes


Cờ

    Length implied by lenOuterCiphertext (whatever data remains)

    Encrypted layer 2 data. See below for key derivation and encryption algorithms.


#### Lớp 2 (trong)

Dữ liệu xác thực khách hàng DH

    1 byte

    Either 3 (LS2) or 7 (Meta LS2)

Dữ liệu xác thực khách hàng PSK

    LeaseSet2 data for the given type.

    Includes the header and signature.


### Dẫn xuất khóa ẩn danh

innerCiphertext

Loại

#### Mục tiêu

- Thêm ẩn danh
- Cho phép nhiều loại chữ ký
- Không yêu cầu các nguyên thủy mã hóa mới
- Tùy chọn mã hóa cho từng người nhận, có thể thu hồi
- Hỗ trợ mã hóa LS2 chuẩn và Meta LS2 chỉ

#### Bảo mật

Dữ liệu

#### Định nghĩa

Chúng tôi sử dụng sơ đồ sau cho việc ẩn danh khóa,   dựa trên Ed25519 và [ZCash RedDSA](https://github.com/zcash/zips/tree/master/protocol/protocol.pdf).   Các chữ ký Re25519 là trên đường cong Ed25519, sử dụng SHA-512 cho hàm băm.

    The Ed25519 base point (generator) 2^255 - 19 as in [Ed25519](http://cr.yp.to/papers.html#ed25519)

Chúng tôi không sử dụng [phụ lục A.2 của Tor's rend-spec-v3.txt](https://spec.torproject.org/rend-spec-v3),   có mục tiêu thiết kế tương tự, vì các khóa công khai ẩn danh của nó   có thể nằm ngoài nhóm con bậc nguyên tố, với các hệ quả bảo mật chưa biết.

    The Ed25519 order 2^252 + 27742317777372353535851937790883648493
    as in [Ed25519](http://cr.yp.to/papers.html#ed25519)

Bảo mật của một sơ đồ ẩn danh yêu cầu rằng   phân bố của alpha giống hệt như các khóa riêng chưa ẩn danh.   Tuy nhiên, khi chúng ta ẩn danh một khóa riêng Ed25519 (loại chữ ký 7)   thành một khóa riêng Red25519 (loại chữ ký 11), phân bố là khác nhau.   Để đáp ứng các yêu cầu của [zcash section 4.1.6.1](https://github.com/zcash/zips/tree/master/protocol/protocol.pdf),   Red25519 (loại chữ ký 11) nên được sử dụng cho cả các khóa chưa ẩn danh, để   "tổ hợp của một khóa công khai được tạo ngẫu nhiên lại và chữ ký(s)   dưới khóa đó không tiết lộ khóa mà nó được tạo ngẫu nhiên lại từ."   Chúng tôi cho phép loại 7 cho các destination hiện tại, nhưng khuyến nghị   loại 11 cho các destination mới sẽ được mã hóa.

    Convert a private key to public, as in Ed25519 (mulitply by G)

B

    A 32-byte random number known to those who know the destination.

L

    Generate alpha for the current date, for those who know the destination and the secret.
    The result must be identically distributed as Ed25519 private keys.

DERIVE_PUBLIC(a)

    The unblinded 32-byte EdDSA or RedDSA signing private key used to sign the destination

alpha

    The unblinded 32-byte EdDSA or RedDSA signing public key in the destination,
    = DERIVE_PUBLIC(a), as in Ed25519

GENERATE_ALPHA(destination, date, secret)

    The blinded 32-byte EdDSA signing private key used to sign the encrypted leaseset
    This is a valid EdDSA private key.

a

    The blinded 32-byte EdDSA signing public key in the Destination,
    may be generated with DERIVE_PUBLIC(a'), or from A and alpha.
    This is a valid EdDSA public key, on the curve and on the prime-order subgroup.

A

    Flip the order of the input bytes to little-endian

a'

    32 bytes = (LEOS2IP(SHA512(x))) mod B, same as in Ed25519 hash-and-reduce


#### Tính toán ẩn danh

A'

LEOS2IP(x)

```text
// GENERATE_ALPHA(destination, date, secret)

  // secret is optional, else zero-length
  A = destination's signing public key
  stA = signature type of A, 2 bytes big endian (0x0007 or 0x000b)
  stA' = signature type of blinded public key A', 2 bytes big endian (0x000b)
  keydata = A || stA || stA'
  datestring = 8 bytes ASCII YYYYMMDD from the current date UTC
  secret = UTF-8 encoded string
  seed = HKDF(H("I2PGenerateAlpha", keydata), datestring || secret, "i2pblinding1", 64)
  // treat seed as a 64 byte little-endian value
  alpha = seed mod L
```
H*(x)

```text
// BLIND_PRIVKEY()

  alpha = GENERATE_ALPHA(destination, date, secret)
  // If for a Ed25519 private key (type 7)
  seed = destination's signing private key
  a = left half of SHA512(seed) and clamped as usual for Ed25519
  // else, for a Red25519 private key (type 11)
  a = destination's signing private key
  // Addition using scalar arithmentic
  blinded signing private key = a' = BLIND_PRIVKEY(a, alpha) = (a + alpha) mod L
  blinded signing public key = A' = DERIVE_PUBLIC(a')
```
Một bí mật alpha mới và các khóa ẩn danh phải được tạo mỗi ngày (UTC).   Bí mật alpha và các khóa ẩn danh được tính như sau.

```text
// BLIND_PUBKEY()

  alpha = GENERATE_ALPHA(destination, date, secret)
  A = destination's signing public key
  // Addition using group elements (points on the curve)
  blinded public key = A' = BLIND_PUBKEY(A, alpha) = A + DERIVE_PUBLIC(alpha)
```
GENERATE_ALPHA(destination, date, secret), cho tất cả các bên:

#### Ký

BLIND_PRIVKEY(), cho chủ sở hữu công bố leaseset:

BLIND_PUBKEY(), cho các client truy xuất leaseset:

Cả hai phương pháp tính toán A' đều cho cùng kết quả, như yêu cầu.

Leaseset chưa ẩn danh được ký bởi khóa riêng ký Ed25519 hoặc Red25519 chưa ẩn danh   và được xác minh bằng khóa công khai ký Ed25519 hoặc Red25519 chưa ẩn danh (loại chữ ký 7 hoặc 11) như thường lệ.

#### Tính toán Ký/Xác minh

Nếu khóa công khai ký là ngoại tuyến,   leaset chưa ẩn danh được ký bởi khóa riêng ký tạm thời Ed25519 hoặc Red25519 chưa ẩn danh   và được xác minh bằng khóa công khai ký tạm thời Ed25519 hoặc Red25519 chưa ẩn danh (loại chữ ký 7 hoặc 11) như thường lệ.   Xem bên dưới để biết thêm ghi chú về khóa ngoại tuyến cho leaseset được mã hóa.

Đối với việc ký leaseset được mã hóa, chúng tôi sử dụng Red25519, dựa trên [RedDSA](https://github.com/zcash/zips/tree/master/protocol/protocol.pdf)   để ký và xác minh với các khóa ẩn danh.   Các chữ ký Red25519 là trên đường cong Ed25519, sử dụng SHA-512 cho hàm băm.

Red25519 giống hệt với Ed25519 chuẩn ngoại trừ như được chỉ định bên dưới.

Phần ngoài của leaseset được mã hóa sử dụng các khóa và chữ ký Red25519.

Red25519 gần như giống hệt với Ed25519. Có hai điểm khác biệt:

```text
T = 80 random bytes
  r = H*(T || publickey || message)
  // rest is the same as in Ed25519
```
Khóa riêng Red25519 được tạo từ các số ngẫu nhiên và sau đó phải được giảm mod L, trong đó L được định nghĩa ở trên.   Khóa riêng Ed25519 được tạo từ các số ngẫu nhiên và sau đó được "kẹp" bằng   mặt nạ bit cho byte 0 và 31. Điều này không được thực hiện cho Red25519.   Các hàm GENERATE_ALPHA() và BLIND_PRIVKEY() được định nghĩa ở trên tạo ra các khóa riêng Red25519 đúng bằng cách sử dụng mod L.

```text
// same as in Ed25519
```
### Mã hóa và xử lý

#### Dẫn xuất các subcredentials

Trong Red25519, phép tính r để ký sử dụng thêm dữ liệu ngẫu nhiên,   và sử dụng giá trị khóa công khai thay vì băm của khóa riêng.   Do dữ liệu ngẫu nhiên, mọi chữ ký Red25519 đều khác nhau, ngay cả khi   ký cùng dữ liệu với cùng khóa.

```text
A = destination's signing public key
  stA = signature type of A, 2 bytes big endian (0x0007 or 0x000b)
  stA' = signature type of A', 2 bytes big endian (0x000b)
  keydata = A || stA || stA'
  credential = H("credential", keydata)
```
Ký:

Xác minh:

```text
subcredential = H("subcredential", credential || blindedPublicKey)
```
Là một phần của quá trình ẩn danh, chúng ta cần đảm bảo rằng một LS2 được mã hóa chỉ có thể được   giải mã bởi ai đó biết khóa công khai ký tương ứng của Destination.   Không yêu cầu Destination đầy đủ.   Để đạt được điều này, chúng ta dẫn xuất một credential từ khóa công khai ký:

#### Mã hóa lớp 1

Chuỗi cá nhân hóa đảm bảo rằng credential không bị trùng với bất kỳ băm nào được sử dụng   làm khóa tra cứu DHT, chẳng hạn như băm Destination thuần túy.

```text
outerInput = subcredential || publishedTimestamp
```
Đối với một khóa ẩn danh đã cho, chúng ta có thể dẫn xuất một subcredential:

```text
outerSalt = CSRNG(32)
```
Subcredential được bao gồm trong các quá trình dẫn xuất khóa bên dưới, điều này ràng buộc các khóa đó   với việc biết khóa công khai ký của Destination.

```text
keys = HKDF(outerSalt, outerInput, "ELS2_L1K", 44)
  outerKey = keys[0:31]
  outerIV = keys[32:43]
```
Đầu tiên, đầu vào cho quá trình dẫn xuất khóa được chuẩn bị:

```text
outerCiphertext = outerSalt || ENCRYPT(outerKey, outerIV, outerPlaintext)
```
#### Giải mã lớp 1

Tiếp theo, một muối ngẫu nhiên được tạo:

```text
outerSalt = outerCiphertext[0:31]
```
Sau đó, khóa được sử dụng để mã hóa lớp 1 được dẫn xuất:

```text
outerInput = subcredential || publishedTimestamp
  keys = HKDF(outerSalt, outerInput, "ELS2_L1K", 44)
  outerKey = keys[0:31]
  outerIV = keys[32:43]
```
Cuối cùng, văn bản rõ lớp 1 được mã hóa và tuần tự hóa:

```text
outerPlaintext = DECRYPT(outerKey, outerIV, outerCiphertext[32:end])
```
#### Mã hóa lớp 2

Muối được phân tích từ văn bản mã lớp 1:

Sau đó, khóa được sử dụng để mã hóa lớp 1 được dẫn xuất:

```text
innerInput = authCookie || subcredential || publishedTimestamp
  innerSalt = CSRNG(32)
  keys = HKDF(innerSalt, innerInput, "ELS2_L2K", 44)
  innerKey = keys[0:31]
  innerIV = keys[32:43]
  innerCiphertext = innerSalt || ENCRYPT(innerKey, innerIV, innerPlaintext)
```
#### Giải mã lớp 2

Cuối cùng, văn bản mã lớp 1 được giải mã:

Khi xác thực khách hàng được bật, ``authCookie`` được tính như mô tả bên dưới.   Khi xác thực khách hàng bị tắt, ``authCookie`` là mảng byte độ dài bằng 0.

```text
innerInput = authCookie || subcredential || publishedTimestamp
  innerSalt = innerCiphertext[0:31]
  keys = HKDF(innerSalt, innerInput, "ELS2_L2K", 44)
  innerKey = keys[0:31]
  innerIV = keys[32:43]
  innerPlaintext = DECRYPT(innerKey, innerIV, innerCiphertext[32:end])
```
### Ủy quyền theo khách hàng

Việc mã hóa tiến hành theo cách tương tự như lớp 1:

Khi xác thực khách hàng được bật, ``authCookie`` được tính như mô tả bên dưới.   Khi xác thực khách hàng bị tắt, ``authCookie`` là mảng byte độ dài bằng 0.

#### Xác thực khách hàng DH

Việc giải mã tiến hành theo cách tương tự như lớp 1:

Khi xác thực khách hàng được bật cho một Destination, máy chủ duy trì một danh sách các   khách hàng mà họ ủy quyền để giải mã dữ liệu LS2 được mã hóa. Dữ liệu được lưu trữ cho từng khách hàng   phụ thuộc vào cơ chế ủy quyền, và bao gồm một số dạng vật liệu khóa mà mỗi   khách hàng tạo và gửi đến máy chủ thông qua một cơ chế ngoài băng tần an toàn.

```text
authCookie = CSRNG(32)
  esk = GENERATE_PRIVATE()
  epk = DERIVE_PUBLIC(esk)
```
Có hai lựa chọn để triển khai ủy quyền theo khách hàng:

```text
sharedSecret = DH(esk, cpk_i)
  authInput = sharedSecret || cpk_i || subcredential || publishedTimestamp
  okm = HKDF(epk, authInput, "ELS2_XCA", 52)
  clientKey_i = okm[0:31]
  clientIV_i = okm[32:43]
  clientID_i = okm[44:51]
  clientCookie_i = ENCRYPT(clientKey_i, clientIV_i, authCookie)
```
Mỗi khách hàng tạo một cặp khóa DH ``[csk_i, cpk_i]``, và gửi khóa công khai ``cpk_i``   đến máy chủ.

Xử lý máy chủ   ^^^^^^^^^^^^^^^^^ Máy chủ tạo một ``authCookie`` mới và một cặp khóa DH tạm thời:

```text
sharedSecret = DH(csk_i, epk)
  authInput = sharedSecret || cpk_i || subcredential || publishedTimestamp
  okm = HKDF(epk, authInput, "ELS2_XCA", 52)
  clientKey_i = okm[0:31]
  clientIV_i = okm[32:43]
  clientID_i = okm[44:51]
```
Sau đó, đối với mỗi khách hàng được ủy quyền, máy chủ mã hóa ``authCookie`` bằng khóa công khai của nó:

```text
authCookie = DECRYPT(clientKey_i, clientIV_i, clientCookie_i)
```
#### Xác thực khách hàng khóa chia sẻ trước (PSK)

Máy chủ đặt mỗi bộ ``[clientID_i, clientCookie_i]`` vào lớp 1 của   LS2 được mã hóa, cùng với ``epk``.

Xử lý khách hàng   ^^^^^^^^^^^^^^^^^ Khách hàng sử dụng khóa riêng của nó để dẫn xuất định danh khách hàng mong đợi ``clientID_i``,   khóa mã hóa ``clientKey_i``, và IV mã hóa ``clientIV_i``:

```text
authCookie = CSRNG(32)
  authSalt = CSRNG(32)
```
Sau đó, khách hàng tìm kiếm dữ liệu ủy quyền lớp 1 để tìm mục chứa   ``clientID_i``. Nếu tồn tại mục khớp, khách hàng giải mã nó để lấy   ``authCookie``:

```text
authInput = psk_i || subcredential || publishedTimestamp
  okm = HKDF(authSalt, authInput, "ELS2PSKA", 52)
  clientKey_i = okm[0:31]
  clientIV_i = okm[32:43]
  clientID_i = okm[44:51]
  clientCookie_i = ENCRYPT(clientKey_i, clientIV_i, authCookie)
```
Mỗi khách hàng tạo một khóa bí mật 32 byte ``psk_i``, và gửi nó đến máy chủ.   Ngoài ra, máy chủ có thể tạo khóa bí mật, và gửi nó đến một hoặc nhiều khách hàng.

Xử lý máy chủ   ^^^^^^^^^^^^^^^^^ Máy chủ tạo một ``authCookie`` mới và muối:

```text
authInput = psk_i || subcredential || publishedTimestamp
  okm = HKDF(authSalt, authInput, "ELS2PSKA", 52)
  clientKey_i = okm[0:31]
  clientIV_i = okm[32:43]
  clientID_i = okm[44:51]
```
Sau đó, đối với mỗi khách hàng được ủy quyền, máy chủ mã hóa ``authCookie`` bằng khóa chia sẻ trước của nó:

```text
authCookie = DECRYPT(clientKey_i, clientIV_i, clientCookie_i)
```
#### Xem xét bảo mật

Máy chủ đặt mỗi bộ ``[clientID_i, clientCookie_i]`` vào lớp 1 của   LS2 được mã hóa, cùng với ``authSalt``.

Xử lý khách hàng   ^^^^^^^^^^^^^^^^^ Khách hàng sử dụng khóa chia sẻ trước của nó để dẫn xuất định danh khách hàng mong đợi ``clientID_i``,   khóa mã hóa ``clientKey_i``, và IV mã hóa ``clientIV_i``:

Sau đó, khách hàng tìm kiếm dữ liệu ủy quyền lớp 1 để tìm mục chứa   ``clientID_i``. Nếu tồn tại mục khớp, khách hàng giải mã nó để lấy   ``authCookie``:

Cả hai cơ chế ủy quyền khách hàng trên đều cung cấp quyền riêng tư cho thành viên khách hàng.   Một thực thể chỉ biết Destination có thể thấy có bao nhiêu khách hàng đang đăng ký tại bất kỳ   thời điểm nào, nhưng không thể theo dõi khách hàng nào đang được thêm hoặc thu hồi.

- Mã hóa toàn bộ để đảm bảo an toàn
- Mã hóa an toàn, không chỉ bằng AES.
- Mã hóa cho từng người nhận

Các máy chủ NÊN xáo trộn thứ tự các khách hàng mỗi khi họ tạo một LS2 được mã hóa, để   ngăn khách hàng biết vị trí của họ trong danh sách và suy ra khi khách hàng khác được thêm hoặc thu hồi.

- Một lớp ngoài chứa thông tin văn bản thuần cần thiết để lưu trữ và truy xuất.
- Một lớp giữa xử lý xác thực khách hàng.
- Một lớp trong chứa dữ liệu LS2 thực tế.

Một máy chủ CÓ THỂ chọn ẩn số lượng khách hàng đang đăng ký bằng cách chèn các mục ngẫu nhiên   vào danh sách dữ liệu ủy quyền.

- Khóa công khai ký trong destination chưa ẩn danh phải là  
  Ed25519 (loại chữ ký 7) hoặc Red25519 (loại chữ ký 11);  
  không hỗ trợ các loại chữ ký khác
- Nếu khóa công khai ký là ngoại tuyến, khóa công khai ký tạm thời cũng phải là Ed25519
- Việc ẩn danh khóa đơn giản về mặt tính toán
- Sử dụng các nguyên thủy mật mã hiện có
- Các khóa công khai ẩn danh không thể được gỡ ẩn danh
- Các khóa công khai ẩn danh phải nằm trên đường cong Ed25519 và nhóm con bậc nguyên tố
- Phải biết khóa công khai ký của destination  
  (không yêu cầu destination đầy đủ) để dẫn xuất khóa công khai ẩn danh
- Tùy chọn cung cấp một bí mật bổ sung cần thiết để dẫn xuất khóa công khai ẩn danh

Ưu điểm của xác thực khách hàng DH   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Bảo mật của sơ đồ không hoàn toàn phụ thuộc vào việc trao đổi ngoài băng tần vật liệu khóa khách hàng.  
  Khóa riêng của khách hàng không cần rời khỏi thiết bị của họ, và do đó một  
  kẻ thù có thể chặn việc trao đổi ngoài băng tần, nhưng không thể phá vỡ thuật toán DH,  
  không thể giải mã LS2 được mã hóa, hoặc xác định thời gian khách hàng được cấp quyền truy cập.

### LS được mã hóa với địa chỉ Base 32

Nhược điểm của xác thực khách hàng DH   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Ưu điểm của xác thực khách hàng PSK   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

### LS được mã hóa với khóa ngoại tuyến

Nhược điểm của xác thực khách hàng PSK   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Xem đề xuất 149.

Bạn không thể sử dụng LS2 được mã hóa cho bittorrent, vì các phản hồi thông báo gọn gàng là 32 byte.   32 byte chỉ chứa băm. Không có chỗ cho dấu hiệu rằng   leaseset được mã hóa, hoặc các loại chữ ký.

### Ghi chú

- Yêu cầu N + 1 thao tác DH ở phía máy chủ cho N khách hàng.
- Yêu cầu một thao tác DH ở phía khách hàng.
- Yêu cầu khách hàng tạo khóa bí mật.

- Không yêu cầu thao tác DH nào.
- Cho phép máy chủ tạo khóa bí mật.
- Cho phép máy chủ chia sẻ cùng một khóa với nhiều khách hàng, nếu muốn.

- Bảo mật của sơ đồ phụ thuộc nghiêm trọng vào việc trao đổi ngoài băng tần vật liệu khóa khách hàng.  
  Một kẻ thù chặn được việc trao đổi cho một khách hàng cụ thể có thể giải mã  
  bất kỳ LS2 được mã hóa nào sau đó mà khách hàng đó được ủy quyền, cũng như xác định  
  khi quyền truy cập của khách hàng bị thu hồi.

- Một dịch vụ sử dụng leaseset được mã hóa sẽ công bố phiên bản được mã hóa đến các  
  floodfill. Tuy nhiên, để hiệu quả, nó sẽ gửi leaseset chưa được mã hóa đến  
  client trong tin nhắn tỏi được bao bọc, sau khi xác thực (qua danh sách trắng, ví dụ).

- Các floodfill có thể giới hạn kích thước tối đa ở mức hợp lý để ngăn lạm dụng.

### Meta LS2

Đối với leaseset được mã hóa có khóa ngoại tuyến, các khóa riêng ẩn danh cũng phải được tạo ngoại tuyến,   một cho mỗi ngày.

Vì khối chữ ký ngoại tuyến tùy chọn nằm trong phần văn bản rõ của leaseset được mã hóa,   bất kỳ ai quét các floodfill có thể sử dụng điều này để theo dõi leaseset (nhưng không giải mã nó)   trong vài ngày.   Để ngăn chặn điều này, chủ sở hữu khóa nên tạo các khóa tạm thời mới   cho mỗi ngày cũng vậy.   Cả khóa tạm thời và khóa ẩn danh đều có thể được tạo trước, và giao cho router   theo lô.

Không có định dạng tệp nào được định nghĩa trong đề xuất này để đóng gói nhiều khóa tạm thời và   khóa ẩn danh và cung cấp chúng cho client hoặc router.   Không có cải tiến giao thức I2CP nào được định nghĩa trong đề xuất này để hỗ trợ   leaseset được mã hóa với khóa ngoại tuyến.

Điều này được sử dụng để thay thế đa kết nối. Giống như bất kỳ leaseset nào, điều này được ký bởi người tạo. Đây là một danh sách được xác thực của các băm destination.

Meta LS2 là đỉnh, và có thể là các nút trung gian của,   một cấu trúc cây.   Nó chứa một số mục, mỗi mục trỏ đến một LS, LS2 hoặc một Meta LS2 khác   để hỗ trợ đa kết nối quy mô lớn.   Một Meta LS2 có thể chứa hỗn hợp các mục LS, LS2 và Meta LS2.   Các lá của cây luôn là một LS hoặc LS2.   Cây là một DAG; các vòng lặp bị cấm; các client thực hiện tra cứu phải phát hiện và   từ chối theo các vòng lặp.

Một Meta LS2 có thể có thời gian hết hạn lâu hơn nhiều so với một LS hoặc LS2 chuẩn.   Cấp độ trên cùng có thể có thời gian hết hạn vài giờ sau ngày công bố.   Thời gian hết hạn tối đa sẽ được các floodfill và client thực thi, và đang được xác định.

Mục đích sử dụng cho Meta LS2 là đa kết nối quy mô lớn, nhưng không có thêm   bảo vệ nào cho việc liên kết các router với leaseset (tại thời điểm khởi động lại router) hơn   được cung cấp hiện tại với LS hoặc LS2.   Điều này tương đương với trường hợp sử dụng "facebook", có lẽ không cần   bảo vệ liên kết. Trường hợp sử dụng này có lẽ cần khóa ngoại tuyến,   được cung cấp trong tiêu đề chuẩn tại mỗi nút của cây.

Giao thức back-end để phối hợp giữa các router lá, các chữ ký Meta LS trung gian và chính   không được chỉ định ở đây. Các yêu cầu cực kỳ đơn giản - chỉ cần xác minh rằng peer đang hoạt động,   và công bố một LS mới mỗi vài giờ. Độ phức tạp duy nhất là chọn   các publisher mới cho các Meta LS cấp độ trên cùng hoặc cấp độ trung gian khi thất bại.

Leaseset kết hợp nơi các lease từ nhiều router được kết hợp, ký và công bố   trong một leaseset duy nhất được ghi trong đề xuất 140, "đa kết nối vô hình".   Đề xuất này không khả thi như đã viết, vì các kết nối streaming sẽ không   "gắn bó" với một router duy nhất, xem http://zzz.i2p/topics/2335 .

Giao thức back-end, và tương tác với nội bộ router và client, sẽ   rất phức tạp đối với đa kết nối vô hình.

    Standard LS flag (1)
Để tránh quá tải floodfill cho Meta LS cấp độ trên cùng, thời gian hết hạn nên   ít nhất là vài giờ. Client phải lưu trữ bộ nhớ đệm Meta LS cấp độ trên cùng, và duy trì   nó qua các lần khởi động lại nếu chưa hết hạn.

    Meta LS2 type (7)
Chúng ta cần định nghĩa một số thuật toán để client duyệt cây, bao gồm các phương án dự phòng,   để việc sử dụng được phân tán. Một số hàm của khoảng cách băm, chi phí và tính ngẫu nhiên.   Nếu một nút có cả LS hoặc LS2 và Meta LS, chúng ta cần biết khi nào được phép   sử dụng các leaseset đó, và khi nào nên tiếp tục duyệt cây.

    Hash of destination
    This hash is then used to generate the daily "routing key", as in LS1
Tìm kiếm với

    Hours. Max 18.2 hours (65535 seconds)
Lưu trữ với

    "master" Destination or coordinator, or intermediate coordinators

### Định dạng

```
Standard LS2 Header as specified above

  Meta LS2 Type-Specific Part
  - Properties (Mapping as specified in common structures spec, 2 zero bytes if none)
  - Number of entries (1 byte) Maximum TBD
  - Entries. Each entry contains: (40 bytes)
    - Hash (32 bytes)
    - Flags (2 bytes)
      TBD. Set all to zero for compatibility with future uses.
    - Type (1 byte) The type of LS it is referencing;
      1 for LS, 3 for LS2, 5 for encrypted, 7 for meta, 0 for unknown.
    - Cost (priority) (1 byte)
    - Expires (4 bytes) (4 bytes, big endian, seconds since epoch, rolls over in 2106)
  - Number of revocations (1 byte) Maximum TBD
  - Revocations: Each revocation contains: (32 bytes)
    - Hash (32 bytes)

  Standard LS2 Signature:
  - Signature (40+ bytes)
    The signature is of everything above.
```
Lưu trữ tại

### Ghi chú

- Sau khi giải mã, một số kiểm tra nên được thực hiện, bao gồm việc  
  dấu thời gian và hết hạn bên trong khớp với những cái ở cấp độ trên cùng.

- ChaCha20 được chọn thay vì AES. Mặc dù tốc độ tương tự nếu hỗ trợ phần cứng AES  
  có sẵn, ChaCha20 nhanh hơn 2,5-3 lần khi  
  hỗ trợ phần cứng AES không có, chẳng hạn như trên các thiết bị ARM cấp thấp.

- Chúng tôi không quan tâm đủ về tốc độ để sử dụng BLAKE2b có khóa. Nó có kích thước đầu ra  
  đủ lớn để chứa n lớn nhất chúng tôi yêu cầu (hoặc chúng tôi có thể gọi nó một lần cho mỗi  
  khóa mong muốn với một đối số bộ đếm). BLAKE2b nhanh hơn nhiều so với SHA-256, và  
  BLAKE2b có khóa sẽ giảm tổng số lần gọi hàm băm.  
  Tuy nhiên, xem đề xuất 148, nơi đề xuất rằng chúng tôi chuyển sang BLAKE2b vì các lý do khác.  
  Xem [Secure key derivation performance](https://www.lvh.io/posts/secure-key-derivation-performance.html).

### Bản ghi Dịch vụ

Thời gian hết hạn điển hình

Được công bố bởi

Cờ và thuộc tính: để sử dụng trong tương lai

    n/a, see Service List
Đây là một bản ghi cá nhân nói rằng một destination đang tham gia vào một   dịch vụ. Nó được gửi từ người tham gia đến floodfill. Nó không bao giờ được gửi   riêng lẻ bởi một floodfill, mà chỉ như một phần của Danh sách Dịch vụ. Bản ghi Dịch vụ cũng được sử dụng để thu hồi sự tham gia vào một dịch vụ, bằng cách đặt   thời gian hết hạn thành không.

    Service Record type (9)
Đây không phải là một LS2 nhưng nó sử dụng định dạng tiêu đề và chữ ký LS2 chuẩn.

    Hash of service name
    This hash is then used to generate the daily "routing key", as in LS1
Tìm kiếm với

    Hours. Max 18.2 hours (65535 seconds)
Lưu trữ với

    Destination

### Định dạng

```
Standard LS2 Header as specified above

  Service Record Type-Specific Part
  - Port (2 bytes, big endian) (0 if unspecified)
  - Hash of service name (32 bytes)

  Standard LS2 Signature:
  - Signature (40+ bytes)
    The signature is of everything above.
```
### Ghi chú

- Một dịch vụ phân tán sử dụng điều này sẽ có một hoặc nhiều "chính" với khóa riêng của destination dịch vụ. Họ sẽ (ngoài băng tần) xác định danh sách hiện tại các destination hoạt động và sẽ công bố Meta LS2. Để dự phòng, nhiều "chính" có thể đa kết nối (tức là công bố đồng thời) Meta LS2.

- Một dịch vụ phân tán có thể bắt đầu với một destination duy nhất hoặc sử dụng đa kết nối kiểu cũ, sau đó chuyển sang Meta LS2. Một tìm kiếm LS chuẩn có thể trả về bất kỳ một trong LS, LS2 hoặc Meta LS2.

- Khi một dịch vụ sử dụng Meta LS2, nó không có tunnel (lease).

### Danh sách Dịch vụ

Lưu trữ tại

Thời gian hết hạn điển hình

Được công bố bởi

Điều này không giống gì với một LS2 và sử dụng định dạng khác.

Danh sách dịch vụ được tạo và ký bởi floodfill. Nó không được xác thực   theo nghĩa bất kỳ ai cũng có thể tham gia một dịch vụ bằng cách công bố một Bản ghi Dịch vụ đến một   floodfill.

Một Danh sách Dịch vụ chứa các Bản ghi Dịch vụ Ngắn, không phải Bản ghi Dịch vụ đầy đủ. Những bản ghi này   chứa chữ ký nhưng chỉ băm, không phải destination đầy đủ, vì vậy chúng không thể được   xác minh mà không có destination đầy đủ.

    Service List lookup type (11)
Bảo mật, nếu có, và tính mong muốn của danh sách dịch vụ đang được xác định.   Các floodfill có thể giới hạn việc công bố và tra cứu, đến một danh sách trắng các dịch vụ,   nhưng danh sách trắng đó có thể thay đổi tùy theo triển khai hoặc sở thích của người vận hành.   Có thể không thể đạt được sự đồng thuận về một danh sách trắng cơ bản chung   giữa các triển khai.

    Service List type (11)
Nếu tên dịch vụ được bao gồm trong bản ghi dịch vụ ở trên,   thì các người vận hành floodfill có thể phản đối; nếu chỉ băm được bao gồm,   thì không có xác minh, và một bản ghi dịch vụ có thể "vào" trước   bất kỳ loại netdb nào khác và được lưu trữ trong floodfill.

    Hash of service name
    This hash is then used to generate the daily "routing key", as in LS1
Tìm kiếm với

    Hours, not specified in the list itself, up to local policy
Lưu trữ với

    Nobody, never sent to floodfill, never flooded.

### Định dạng

Lưu trữ tại

```
- Type (1 byte)
    Not actually in header, but part of data covered by signature.
    Take from field in Database Store Message.
  - Hash of the service name (implicit, in the Database Store message)
  - Hash of the Creator (floodfill) (32 bytes)
  - Published timestamp (8 bytes, big endian)

  - Number of Short Service Records (1 byte)
  - List of Short Service Records:
    Each Short Service Record contains (90+ bytes)
    - Dest hash (32 bytes)
    - Published timestamp (8 bytes, big endian)
    - Expires (4 bytes, big endian) (offset from published in ms)
    - Flags (2 bytes)
    - Port (2 bytes, big endian)
    - Sig length (2 bytes, big endian)
    - Signature of dest (40+ bytes)

  - Number of Revocation Records (1 byte)
  - List of Revocation Records:
    Each Revocation Record contains (86+ bytes)
    - Dest hash (32 bytes)
    - Published timestamp (8 bytes, big endian)
    - Flags (2 bytes)
    - Port (2 bytes, big endian)
    - Sig length (2 bytes, big endian)
    - Signature of dest (40+ bytes)

  - Signature of floodfill (40+ bytes)
    The signature is of everything above.
```
Thời gian hết hạn điển hình

- Nếu hết hạn là toàn bộ số 0, floodfill nên thu hồi bản ghi và không còn  
  bao gồm nó trong danh sách dịch vụ.

Được công bố bởi

- Lưu trữ: Floodfill có thể giới hạn nghiêm ngặt việc lưu trữ các bản ghi này và  
  giới hạn số lượng bản ghi được lưu trữ cho mỗi băm và thời gian hết hạn của chúng. Một danh sách trắng  
  các băm cũng có thể được sử dụng.

KHÔNG sử dụng tiêu đề LS2 chuẩn được chỉ định ở trên.

- Bất kỳ loại netdb nào khác tại cùng băm có ưu tiên, vì vậy một bản ghi dịch vụ không bao giờ  
  có thể ghi đè LS/RI, nhưng một LS/RI sẽ ghi đè tất cả các bản ghi dịch vụ tại băm đó.

### Ghi chú

- thêm vào đầu băm của tên dịch vụ
- loại bỏ băm của người tạo
- Kiểm tra chữ ký của nội dung đã sửa đổi

- lấy destination
- Kiểm tra chữ ký của (dấu thời gian công bố + hết hạn + cờ + cổng + Băm của  
  tên dịch vụ)

- lấy destination
- Kiểm tra chữ ký của (dấu thời gian công bố + 4 byte 0 + cờ + cổng + Băm  
  của tên dịch vụ)

## Các thay đổi cần thiết đối với Đặc tả Cấu trúc Chung

### Chứng chỉ khóa

Để xác minh chữ ký của Danh sách Dịch vụ:

### Các cấu trúc trung gian mới

Để xác minh chữ ký của mỗi Bản ghi Dịch vụ Ngắn:

### Các loại NetDB mới

Để xác minh chữ ký của mỗi Bản ghi Thu hồi:

### Loại chữ ký mới

Ngoài phạm vi của đề xuất này.   Thêm vào các đề xuất ECIES 144 và 145.

## Các thay đổi cần thiết đối với Đặc tả Mã hóa

Thêm các cấu trúc mới cho Lease2, MetaLease, LeaseSet2Header và OfflineSignature.   Có hiệu lực kể từ phiên bản 0.9.38.

## Các thay đổi cần thiết đối với I2NP

Thêm cấu trúc cho mỗi loại leaseset mới, được tích hợp từ trên.   Đối với LeaseSet2, EncryptedLeaseSet và MetaLeaseSet,   có hiệu lực kể từ phiên bản 0.9.38.   Đối với Bản ghi Dịch vụ và Danh sách Dịch vụ,   ban đầu và chưa lên lịch.

### Thông điệp tra cứu cơ sở dữ liệu

Thêm RedDSA_SHA512_Ed25519 Loại 11.   Khóa công khai là 32 byte; khóa riêng là 32 byte; băm là 64 byte; chữ ký là 64 byte.

### Thay đổi

```
Flags byte: Lookup type field, currently bits 3-2, expands to bits 4-2.
  Lookup type 0x04 is defined as the service list lookup.

  Add note: Service list loookup may only be sent to floodfills with a minimum version.
  Minimum version is 0.9.38.
```
### Thông điệp Database Store

Ngoài phạm vi của đề xuất này.   Xem các đề xuất 144 và 145.

### Thay đổi

```
Type byte: Type field, currently bit 0, expands to bits 3-0.
  Type 3 is defined as a LS2 store.
  Type 5 is defined as a encrypted LS2 store.
  Type 7 is defined as a meta LS2 store.
  Type 9 is defined as a service record store.
  Type 11 is defined as a service list store.
  Other types are undefined and invalid.

  Add note: All new types may only be published to floodfills with a minimum version.
  Minimum version is 0.9.38.
```
## Các thay đổi I2CP cần thiết

### Tùy chọn I2CP

Thêm ghi chú: LS2 chỉ có thể được công

```

  i2cp.leaseSetType=nnn       The type of leaseset to be sent in the Create Leaseset Message
                              Value is the same as the netdb store type in the table above.
                              Interpreted client-side, but also passed to the router in the
                              SessionConfig, to declare intent and check support.

  i2cp.leaseSetEncType=nnn[,nnn]  The encryption types to be used.
                                  Interpreted client-side, but also passed to the router in
                                  the SessionConfig, to declare intent and check support.
                                  See proposals 144 and 145.

  i2cp.leaseSetOfflineExpiration=nnn  The expiration of the offline signature, ASCII,
                                      seconds since the epoch.

  i2cp.leaseSetTransientPublicKey=[type:]b64  The base 64 of the transient private key,
                                              prefixed by an optional sig type number
                                              or name, default DSA_SHA1.
                                              Length as inferred from the sig type

  i2cp.leaseSetOfflineSignature=b64   The base 64 of the offline signature.
                                      Length as inferred from the destination
                                      signing public key type

  i2cp.leaseSetSecret=b64     The base 64 of a secret used to blind the
                              address of the leaseset, default ""

  i2cp.leaseSetAuthType=nnn   The type of authentication for encrypted LS2.
                              0 for no per-client authentication (the default)
                              1 for DH per-client authentication
                              2 for PSK per-client authentication

  i2cp.leaseSetPrivKey=b64    A base 64 private key for the router to use to
                              decrypt the encrypted LS2,
                              only if per-client authentication is enabled
```
Các tùy chọn mới được diễn giải ở phía client:

```

  i2cp.leaseSetType=nnn     The type of leaseset to be sent in the Create Leaseset Message
                            Value is the same as the netdb store type in the table above.
                            Interpreted client-side, but also passed to the router in the
                            SessionConfig, to declare intent and check support.

  i2cp.leaseSetEncType=nnn[,nnn]  The encryption types to be used.
                                  Interpreted client-side, but also passed to the router in
                                  the SessionConfig, to declare intent and check support.
                                  See proposals 144 and 145.

  i2cp.leaseSetSecret=b64     The base 64 of a secret used to blind the
                              address of the leaseset, default ""

  i2cp.leaseSetAuthType=nnn       The type of authentication for encrypted LS2.
                                  0 for no per-client authentication (the default)
                                  1 for DH per-client authentication
                                  2 for PSK per-client authentication

  i2cp.leaseSetBlindedType=nnn   The sig type of the blinded key for encrypted LS2.
                                 Default depends on the destination sig type.

  i2cp.leaseSetClient.dh.nnn=b64name:b64pubkey   The base 64 of the client name (ignored, UI use only),
                                                 followed by a ':', followed by the base 64 of the public
                                                 key to use for DH per-client auth. nnn starts with 0

  i2cp.leaseSetClient.psk.nnn=b64name:b64privkey   The base 64 of the client name (ignored, UI use only),
                                                   followed by a ':', followed by the base 64 of the private
                                                   key to use for PSK per-client auth. nnn starts with 0
```
### Cấu hình phiên

Lưu ý rằng đối với chữ ký offline, các tùy chọn i2cp.leaseSetOfflineExpiration, i2cp.leaseSetTransientPublicKey và i2cp.leaseSetOfflineSignature là bắt buộc, và chữ ký được tạo bởi khóa riêng dùng để ký tạm thời.

### Thông điệp Yêu cầu LeaseSet

Router đến client. Không thay đổi. Các lease được gửi với timestamp 8 byte, ngay cả khi leaseset được trả về sẽ là LS2 với timestamp 4 byte. Lưu ý rằng phản hồi có thể là Create Leaseset hoặc Create Leaseset2 Message.

### Thông điệp yêu cầu leaseSet biến

Router đến client. Không thay đổi. Các lease được gửi với timestamp 8 byte, ngay cả khi leaseset được trả về sẽ là LS2 với timestamp 4 byte. Lưu ý rằng phản hồi có thể là Create Leaseset hoặc Create Leaseset2 Message.

### Tạo thông điệp Leaseset2

Từ client đến router. Tin nhắn mới, dùng thay cho Tin nhắn Tạo Leaseset.

### Cơ sở

- Chúng tôi sử dụng độ dài chữ ký thay vì loại chữ ký để hỗ trợ các loại chữ ký chưa biết.

- Không có thời gian hết hạn của danh sách dịch vụ, người nhận có thể tự quyết định  
  dựa trên chính sách hoặc thời gian hết hạn của các bản ghi riêng lẻ.

- Danh sách Dịch vụ không được lan truyền, chỉ các Bản ghi Dịch vụ riêng lẻ được. Mỗi  
  floodfill tạo, ký và lưu trữ bộ nhớ đệm một Danh sách Dịch vụ. Floodfill sử dụng  
  chính sách riêng của nó cho thời gian lưu trữ bộ nhớ đệm và số lượng tối đa các bản ghi dịch vụ và thu hồi.

### Loại thông điệp

Loại thông điệp của Create Leaseset2 Message là 41.

### Định dạng

```
Session ID
  Type byte: Type of lease set to follow
             Type 1 is a LS
             Type 3 is a LS2
             Type 5 is a encrypted LS2
             Type 7 is a meta LS2
  LeaseSet: type specified above
  Number of private keys to follow (1 byte)
  Encryption Private Keys: For each public key in the lease set,
                           in the same order
                           (Not present for Meta LS2)
                           - Encryption type (2 bytes, big endian)
                           - Encryption key length (2 bytes, big endian)
                           - Encryption key (number of bytes specified)
```
### Ghi chú

- Phiên bản router tối thiểu là 0.9.39.
- Phiên bản sơ bộ với loại tin nhắn 40 đã có trong 0.9.38 nhưng định dạng đã bị thay đổi.
  Loại 40 đã bị bỏ và không được hỗ trợ.

### Vấn đề

- Cần thêm các thay đổi để hỗ trợ LS được mã hóa và meta LS.

### Thông điệp Blinding Info

Từ client đến router. Tin nhắn mới.

### Cơ sở

- Router cần biết liệu một destination có bị blinded hay không.
  Nếu nó bị blinded và sử dụng xác thực bí mật hoặc xác thực theo từng client,
  router cũng cần có thông tin đó.

- Một Host Lookup cho một địa chỉ b32 định dạng mới (“b33”)
  cho router biết rằng địa chỉ này đã bị blinded, nhưng không có cơ chế nào để
  truyền secret hoặc private key cho router trong thông điệp Host Lookup.
  Mặc dù có thể mở rộng thông điệp Host Lookup để thêm thông tin đó,
  việc định nghĩa một thông điệp mới sẽ gọn gàng hơn.

- Chúng ta cần một cách thức lập trình để client thông báo cho router. Nếu không, người dùng sẽ phải cấu hình thủ công từng đích.

### Cách sử dụng

Trước khi một client gửi tin nhắn đến một blinded destination, client đó phải tra cứu "b33" trong một thông điệp Host Lookup, hoặc gửi một thông điệp Blinding Info. Nếu blinded destination yêu cầu một secret hoặc xác thực theo từng client, client phải gửi một thông điệp Blinding Info.

Router không gửi phản hồi cho thông điệp này.

### Loại thông điệp

Loại thông điệp cho Blinding Info Message là 42.

### Định dạng

```
Session ID
  Flags:       1 byte
               Bit order: 76543210
               Bit 0: 0 for everybody, 1 for per-client
               Bits 3-1: Authentication scheme, if bit 0 is set to 1 for per-client, otherwise 000
                         000: DH client authentication (or no per-client authentication)
                         001: PSK client authentication
               Bit 4: 1 if secret required, 0 if no secret required
               Bits 7-5: Unused, set to 0 for future compatibility
  Type byte:   Endpoint type to follow
               Type 0 is a Hash
               Type 1 is a host name String
               Type 2 is a Destination
               Type 3 is a Sig Type and Signing Public Key
  Blind Type:  2 byte blinded sig type (big endian)
  Expiration:  4 bytes, big endian, seconds since epoch
  Endpoint:    Data as specified above
               For type 0: 32 byte binary hash
               For type 1: host name String
               For type 2: binary Destination
               For type 3: 2 byte sig type (big endian)
                           Signing Public Key (length as implied by sig type)
  Private Key: Only if flag bit 0 is set to 1
               A 32-byte ECIES_X25519 private key
  Secret:      Only if flag bit 4 is set to 1
               A secret String
```
### Ghi chú

- Phiên bản router tối thiểu là 0.9.43

### Vấn đề

### Tin nhắn phản hồi của host (enc)

Để hỗ trợ tra cứu các hostname "b33" và trả về chỉ báo nếu router không có thông tin cần thiết, chúng tôi định nghĩa thêm các mã kết quả cho Host Reply Message như sau:

```
2: Lookup password required
   3: Private key required
   4: Lookup password and private key required
   5: Leaseset decryption failure
```
Các giá trị 1-255 đã được định nghĩa là lỗi, vì vậy không có vấn đề về khả năng tương thích ngược.

### Thông báo chuyển hướng Meta

Router đến client. Tin nhắn mới.

### Cơ sở

Client không biết từ trước rằng một Hash cho trước sẽ phân giải thành một Meta LS.

Nếu tra cứu leaseset cho một Destination trả về Meta LS, router sẽ thực hiện phân giải đệ quy. Đối với datagram, phía client không cần biết; tuy nhiên, với streaming, nơi giao thức kiểm tra destination trong SYN ACK, nó phải biết destination "thật" là gì. Do đó, cần có một message mới.

### Cách sử dụng

Router duy trì một bộ nhớ đệm cho destination thực tế được dùng từ một meta LS. Khi client gửi một tin nhắn tới một destination phân giải thành một meta LS, router kiểm tra bộ nhớ đệm để tìm destination thực tế được dùng lần cuối. Nếu bộ nhớ đệm trống, router chọn một destination từ meta LS và tra cứu leaseset. Nếu việc tra cứu leaseset thành công, router thêm destination đó vào bộ nhớ đệm và gửi cho client một Meta Redirect Message. Việc này chỉ được thực hiện một lần, trừ khi destination hết hạn và phải được thay đổi. Client cũng phải lưu vào bộ nhớ đệm thông tin nếu cần. Meta Redirect Message KHÔNG được gửi để trả lời cho mọi SendMessage.

Router chỉ gửi thông điệp này đến các client có phiên bản 0.9.47 trở lên.

Client không gửi trả lời cho tin nhắn này.

### Loại thông điệp

Loại tin nhắn cho Meta Redirect Message là 43.

### Định dạng

```
Session ID (2 bytes) The value from the Send Message.
  Message ID generated by the router (4 bytes)
  4 byte nonce previously generated by the client
               (the value from the Send Message, may be zero)
  Flags:       2 bytes, bit order 15...0
               Unused, set to 0 for future compatibility
               Bit 0: 0 - the destination is no longer meta
                      1 - the destination is now meta
               Bits 15-1: Unused, set to 0 for future compatibility
  Original Destination (387+ bytes)
  (following fields only present if flags bit 0 is 1)
  MFlags:      2 bytes
               Unused, set to 0 for future compatibility
               From the Meta Lease for the actual Destination
  Expiration:  4 bytes, big endian, seconds since epoch
               From the Meta Lease for the actual Destination
  Cost (priority) 1 byte
               From the Meta Lease for the actual Destination
  Actual (real) Destination (387+ bytes)
```
### Các thay đổi để hỗ trợ Meta

Cách tạo và hỗ trợ Meta, bao gồm giao tiếp và phối hợp giữa các router, nằm ngoài phạm vi của đề xuất này. Xem đề xuất liên quan 150.

### Các thay đổi để hỗ trợ Offline Keys

Không thể xác minh chữ ký offline trong streaming hoặc datagram có thể trả lời. Xem các phần bên dưới.

## Yêu cầu thay đổi tệp khóa riêng

Định dạng tệp khóa riêng tư (eepPriv.dat) không phải là một phần chính thức trong đặc tả của chúng tôi, nhưng nó được ghi chép trong [Java I2P javadocs](http://idk.i2p/javadoc-i2p/net/i2p/data/PrivateKeyFile.html) và các bản triển khai khác cũng hỗ trợ định dạng này. Điều này cho phép khóa riêng tư có thể được chuyển đổi giữa các bản triển khai khác nhau.

Cần có những thay đổi để lưu trữ public key tạm thời và thông tin ký offline.

### Thay đổi

```
If the signing private key is all zeros, the offline information section follows:

  - Expires timestamp
    (4 bytes, big endian, seconds since epoch, rolls over in 2106)
  - Sig type of transient Signing Public Key (2 bytes, big endian)
  - Transient Signing Public key
    (length as specified by transient sig type)
  - Signature of above three fields by offline key
    (length as specified by destination sig type)
  - Transient Signing Private key
    (length as specified by transient sig type)
```
### Các thay đổi CLI cần thiết đối với tệp khóa riêng

Thêm hỗ trợ cho các tùy chọn sau:

```
-d days              (specify expiration in days of offline sig, default 365)
      -o offlinedestfile   (generate the online key file,
                            using the offline key file specified)
      -r sigtype           (specify sig type of transient key, default Ed25519)
```
## Các thay đổi streaming cần thiết

Chữ ký ngoại tuyến hiện không thể được xác minh trong streaming. Thay đổi bên dưới thêm khối ký ngoại tuyến vào các tùy chọn. Điều này tránh phải truy xuất thông tin này qua I2CP.

### Thay đổi

```
Add new option:
  Bit:          11
  Flag:         OFFLINE_SIGNATURE
  Option order: 4
  Option data:  Variable bytes
  Function:     Contains the offline signature section from LS2.
                FROM_INCLUDED must also be set.
                Expires timestamp
                (4 bytes, big endian, seconds since epoch, rolls over in 2106)
                Transient sig type (2 bytes, big endian)
                Transient signing public key (length as implied by sig type)
                Signature of expires timestamp, transient sig type,
                and public key, by the destination public key,
                length as implied by destination public key sig type.

  Change option:
  Bit:          3
  Flag:         SIGNATURE_INCLUDED
  Option order: Change from 4 to 5

  Add information about transient keys to the
  Variable Length Signature Notes section:
  The offline signature option does not needed to be added for a CLOSE packet if
  a SYN packet containing the option was previously acked.
  More info TODO
```
### Ghi chú

- Giải pháp thay thế là chỉ cần thêm một flag và truy xuất khóa công khai tạm thời qua I2CP
  (Xem các phần Host Lookup / Host Reply Message ở trên)

## Những thay đổi cần thiết đối với Repliable Datagram

Không thể xác minh chữ ký offline trong quá trình xử lý repliable datagram. Cần một flag để cho biết đã được ký offline, nhưng không có chỗ để đặt flag. Điều này sẽ đòi hỏi một số hiệu protocol và định dạng hoàn toàn mới.

### Thay đổi

```
Define new protocol 19 - Repliable datagram with options?
  - Destination (387+ bytes)
  - Flags (2 bytes)
    Bit order: 15 14 ... 3 2 1 0
    Bit 0: If 0, no offline keys; if 1, offline keys
    Bits 1-15: set to 0 for compatibility with future uses
  - If flag indicates offline keys, the offline signature section:
    Expires timestamp
    (4 bytes, big endian, seconds since epoch, rolls over in 2106)
    Transient sig type (2 bytes, big endian)
    Transient signing public key (length as implied by sig type)
    Signature of expires timestamp, transient sig type,
    and public key, by the destination public key,
    length as implied by destination public key sig type.
    This section can, and should, be generated offline.
  - Data
```
### Ghi chú

- Một cách khác là chỉ cần thêm một flag, và truy xuất khóa công khai tạm thời qua I2CP
  (Xem các phần Host Lookup / Host Reply Message ở trên)
- Còn lựa chọn nào khác chúng ta nên thêm bây giờ khi đã có các byte flag?

## Những thay đổi cần thiết đối với SAM V3

SAM cần được nâng cấp để hỗ trợ chữ ký ngoại tuyến trong DESTINATION base 64.

### Thay đổi

```
Note that in the SESSION CREATE DESTINATION=$privkey,
  the $privkey raw data (before base64 conversion)
  may be optionally followed by the Offline Signature as specified in the
  Common Structures Specification.

  If the signing private key is all zeros, the offline information section follows:

  - Expires timestamp
    (4 bytes, big endian, seconds since epoch, rolls over in 2106)
  - Sig type of transient Signing Public Key (2 bytes, big endian)
  - Transient Signing Public key
    (length as specified by transient sig type)
  - Signature of above three fields by offline key
    (length as specified by destination sig type)
  - Transient Signing Private key (length as specified by transient sig type)
```
Lưu ý rằng chữ ký offline chỉ được hỗ trợ cho STREAM và RAW, không hỗ trợ cho DATAGRAM (cho đến khi chúng ta định nghĩa một giao thức DATAGRAM mới).

Lưu ý rằng SESSION STATUS sẽ trả về một Signing Private Key là all zeros và dữ liệu Offline Signature đúng như được cung cấp trong SESSION CREATE.

Lưu ý rằng DEST GENERATE và SESSION CREATE DESTINATION=TRANSIENT không thể được dùng để tạo một destination được ký ngoại tuyến.

### Vấn đề

Nâng phiên bản lên 3.4, hay giữ nguyên ở 3.1/3.2/3.3 để có thể bổ sung mà không cần toàn bộ phần của 3.2/3.3?

Các thay đổi khác sẽ được xác định sau. Xem phần I2CP Host Reply Message ở trên.

## BOB Cần Những Thay Đổi

BOB sẽ cần được cải tiến để hỗ trợ chữ ký offline và/hoặc Meta LS. Đây là ưu tiên thấp và có lẽ sẽ không bao giờ được đặc tả hoặc triển khai. SAM V3 là giao diện được ưu tiên.

## Xuất bản, Di trú, Tương thích

LS2 (ngoại trừ LS2 được mã hóa) được công bố tại cùng vị trí DHT với LS1. Không có cách nào để công bố đồng thời cả LS1 và LS2, trừ khi LS2 nằm ở một vị trí khác.

LS2 được mã hóa được công bố tại hash của kiểu khóa bị làm mờ và dữ liệu khóa. Hash này sau đó được dùng để tạo "khóa định tuyến" hằng ngày, như trong LS1.

LS2 sẽ chỉ được sử dụng khi cần các tính năng mới (mã hóa mới, LS được mã hóa, meta, v.v.). LS2 chỉ có thể được công bố tới các floodfill có phiên bản được chỉ định hoặc cao hơn.

Các server công bố LS2 sẽ biết rằng mọi client kết nối đều hỗ trợ LS2. Chúng có thể gửi LS2 trong garlic.

Các client sẽ chỉ gửi LS2 trong garlic nếu dùng crypto mới. Các client chia sẻ sẽ dùng LS1 vô thời hạn? TODO: Làm thế nào để có client chia sẻ hỗ trợ cả crypto cũ lẫn mới?

## Triển khai

0.9.38 bao gồm hỗ trợ floodfill cho LS2 tiêu chuẩn, kể cả offline key.

0.9.39 bao gồm hỗ trợ I2CP cho LS2 và Encrypted LS2, ký/xác minh sig type 11, hỗ trợ floodfill cho Encrypted LS2 (sig types 7 và 11, không dùng khóa offline), và mã hóa/giải mã LS2 (không kèm ủy quyền theo từng client).

0.9.40 dự kiến sẽ bao gồm hỗ trợ mã hóa/giải mã LS2 với phân quyền theo từng client, hỗ trợ floodfill và I2CP cho Meta LS2, hỗ trợ LS2 mã hóa với khóa offline, và hỗ trợ b32 cho LS2 mã hóa.

## Lời cảm ơn

Thiết kế LS2 mã hóa chịu ảnh hưởng mạnh mẽ từ [các hidden service descriptor v3 của Tor](https://spec.torproject.org/rend-spec-v3), vốn có các mục tiêu thiết kế tương tự.

## Tài liệu tham khảo

* ["Chữ ký tốc độ cao, bảo mật cao" của Daniel J. Bernstein, Niels Duif, Tanja Lange, Peter Schwabe và Bo-Yin Yang](https://ed25519.cr.yp.to/)
* [KEYBLIND-PROOF](https://lists.torproject.org/pipermail/tor-dev/2013-December/005943.html)
* [KEYBLIND-REFS](https://gitlab.torproject.org/tpo/core/tor/-/issues/8106)
* [PRNG-REFS](http://projectbullrun.org/dual-ec/ext-rand.html)
* [RFC-2104](https://tools.ietf.org/html/rfc2104)
* [RFC-4880-S5.1](https://tools.ietf.org/html/rfc4880#section-5.1)
* [RFC-5869](https://tools.ietf.org/html/rfc5869)
* [RFC-7539-S2.4](https://tools.ietf.org/html/rfc7539#section-2.4)
* [TOR-REND-SPEC-V3](https://spec.torproject.org/rend-spec-v3)
* [UNSCIENTIFIC-KDF-SPEEDS](https://www.lvh.io/posts/secure-key-derivation-performance.html)
* [ZCASH](https://github.com/zcash/zips/tree/master/protocol/protocol.pdf)
