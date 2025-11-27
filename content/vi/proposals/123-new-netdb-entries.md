---
title: "Mục netDB Mới"
number: "123"
author: "zzz, str4d, orignal"
created: "2016-01-16"
lastupdated: "2020-07-18"
status: "Mở"
thread: "http://zzz.i2p/topics/2051"
supercedes: "110, 120, 121, 122"
---

## Trạng thái

Các phần của đề xuất này đã hoàn thành và được triển khai trong phiên bản 0.9.38 và 0.9.39. Các đặc tả Common Structures, I2CP, I2NP và các đặc tả khác hiện đã được cập nhật để phản ánh những thay đổi được hỗ trợ hiện tại.

Các phần đã hoàn thành vẫn có thể được chỉnh sửa nhỏ. Các phần khác của đề xuất này vẫn đang được phát triển và có thể được sửa đổi đáng kể.

Service Lookup (kiểu 9 và 11) có độ ưu tiên thấp và không được lên lịch, và có thể được tách thành một đề xuất riêng biệt.

## Tổng quan

Đây là bản cập nhật và tổng hợp của 4 đề xuất sau:

- 110 LS2
- 120 Meta LS2 cho multihoming quy mô lớn
- 121 LS2 được mã hóa
- 122 Tra cứu dịch vụ không xác thực (anycasting)

Các đề xuất này hầu hết độc lập với nhau, nhưng để đảm bảo tính nhất quán, chúng tôi định nghĩa và sử dụng một định dạng chung cho một số đề xuất trong số đó.

Các đề xuất sau đây có phần liên quan:

- 140 Invisible Multihoming (không tương thích với đề xuất này)
- 142 New Crypto Template (cho mật mã đối xứng mới)
- 144 ECIES-X25519-AEAD-Ratchet
- 145 ECIES-P256
- 146 Red25519
- 148 EdDSA-BLAKE2b-Ed25519
- 149 B32 cho Encrypted LS2
- 150 Garlic Farm Protocol
- 151 ECDSA Blinding

## Đề xuất

Đề xuất này định nghĩa 5 loại DatabaseEntry mới và quy trình lưu trữ chúng vào cũng như truy xuất chúng từ cơ sở dữ liệu mạng, cùng với phương pháp ký và xác minh các chữ ký đó.

### Goals

- Tương thích ngược
- LS2 có thể sử dụng với multihoming kiểu cũ
- Không yêu cầu crypto hoặc primitive mới để hỗ trợ
- Duy trì tách biệt giữa crypto và signing; hỗ trợ tất cả phiên bản hiện tại và tương lai
- Kích hoạt khóa ký offline tùy chọn
- Giảm độ chính xác của timestamps để giảm fingerprinting
- Kích hoạt crypto mới cho destinations
- Kích hoạt multihoming quy mô lớn
- Khắc phục nhiều vấn đề với LS mã hóa hiện tại
- Blinding tùy chọn để giảm khả năng hiển thị bởi floodfills
- Mã hóa hỗ trợ cả khóa đơn và nhiều khóa có thể thu hồi
- Service lookup để tra cứu outproxies, application DHT bootstrap dễ dàng hơn,
  và các mục đích khác
- Không phá vỡ bất cứ thứ gì dựa vào destination hashes nhị phân 32-byte, ví dụ bittorrent
- Thêm tính linh hoạt cho leasesets qua properties, giống như chúng ta có trong routerinfos.
- Đặt published timestamp và variable expiration trong header, để hoạt động ngay cả
  khi nội dung được mã hóa (không suy xuất timestamp từ lease sớm nhất)
- Tất cả các loại mới sống trong cùng không gian DHT và cùng vị trí với leasesets hiện tại,
  để người dùng có thể chuyển đổi từ LS cũ sang LS2,
  hoặc thay đổi giữa LS2, Meta, và Encrypted,
  mà không thay đổi Destination hoặc hash.
- Một Destination hiện tại có thể được chuyển đổi để sử dụng offline keys,
  hoặc trở lại online keys, mà không thay đổi Destination hoặc hash.

### Non-Goals / Out-of-scope

- Thuật toán xoay DHT mới hoặc tạo ngẫu nhiên chia sẻ
- Loại mã hóa mới cụ thể và sơ đồ mã hóa đầu cuối đến đầu cuối
  để sử dụng loại mới đó sẽ được đề xuất trong một đề xuất riêng.
  Không có mã hóa mới nào được chỉ định hoặc thảo luận ở đây.
- Mã hóa mới cho RIs hoặc xây dựng tunnel.
  Điều đó sẽ được đề xuất trong một đề xuất riêng.
- Các phương pháp mã hóa, truyền và nhận tin nhắn I2NP DLM / DSM / DSRM.
  Không thay đổi.
- Cách tạo và hỗ trợ Meta, bao gồm giao tiếp backend giữa các router, quản lý, chuyển đổi dự phòng và phối hợp.
  Hỗ trợ có thể được thêm vào I2CP, hoặc i2pcontrol, hoặc một giao thức mới.
  Điều này có thể được tiêu chuẩn hóa hoặc không.
- Cách thực sự triển khai và quản lý các tunnel hết hạn lâu hơn, hoặc hủy bỏ các tunnel hiện có.
  Điều đó cực kỳ khó khăn, và không có nó, bạn không thể có một tắt máy graceful hợp lý.
- Các thay đổi mô hình đe dọa
- Định dạng lưu trữ offline, hoặc các phương pháp lưu trữ/truy xuất/chia sẻ dữ liệu.
- Chi tiết triển khai không được thảo luận ở đây và được giao cho từng dự án.

### Justification

LS2 thêm các trường để thay đổi loại mã hóa và cho các thay đổi giao thức trong tương lai.

Encrypted LS2 khắc phục một số vấn đề bảo mật với encrypted LS hiện có bằng cách sử dụng mã hóa bất đối xứng cho toàn bộ tập hợp các lease.

Meta LS2 cung cấp khả năng multihoming linh hoạt, hiệu quả, hiệu suất cao và quy mô lớn.

Service Record và Service List cung cấp các dịch vụ anycast như tra cứu tên miền và khởi động DHT.

### Mục tiêu

Các số loại được sử dụng trong I2NP Database Lookup/Store Messages.

Cột end-to-end đề cập đến việc liệu các truy vấn/phản hồi có được gửi đến một Destination trong một Garlic Message hay không.

Các loại hiện có:

| NetDB Data | Lookup Type | Store Type |
|------------|-------------|------------|
| any        | 0           | any        |
| LS         | 1           | 1          |
| RI         | 2           | 0          |
| exploratory| 3           | DSRM       |
Các loại mới:

| NetDB Data     | Lookup Type | Store Type | Std. LS2 Header? | Sent end-to-end? |
|----------------|-------------|------------|------------------|------------------|
| LS2            | 1           | 3          | yes              | yes              |
| Encrypted LS2  | 1           | 5          | no               | no               |
| Meta LS2       | 1           | 7          | yes              | no               |
| Service Record | n/a         | 9          | yes              | no               |
| Service List   | 4           | 11         | no               | no               |
### Không phải Mục tiêu / Ngoài phạm vi

- Các loại lookup hiện tại là các bit 3-2 trong Database Lookup Message.
  Bất kỳ loại bổ sung nào sẽ yêu cầu sử dụng bit 4.

- Tất cả các loại store đều là số lẻ vì các bit cao trong trường loại Database Store Message
  bị bỏ qua bởi các router cũ.
  Chúng tôi muốn việc phân tích thất bại như một LS hơn là như một RI nén.

- Liệu kiểu dữ liệu có nên được khai báo tường minh hay ngầm định hoặc không cần thiết trong dữ liệu được bao phủ bởi chữ ký?

### Lý do chính đáng

Các loại 3, 5, và 7 có thể được trả về để phản hồi cho việc tra cứu leaseSet tiêu chuẩn (loại 1). Loại 9 không bao giờ được trả về để phản hồi cho việc tra cứu. Loại 11 được trả về để phản hồi cho loại tra cứu dịch vụ mới (loại 11).

Chỉ có loại 3 mới có thể được gửi trong thông điệp Garlic từ client-đến-client.

### Các Loại Dữ Liệu NetDB

Các loại 3, 7, và 9 đều có định dạng chung::

Tiêu đề LS2 Chuẩn - như được định nghĩa bên dưới

Phần Cụ Thể Theo Loại - như được định nghĩa bên dưới trong từng phần

Chữ ký LS2 tiêu chuẩn:   - Độ dài như được ngụ ý bởi loại sig của signing key

Loại 5 (Mã hóa) không bắt đầu bằng một Destination và có định dạng khác. Xem bên dưới.

Loại 11 (Service List) là tập hợp của nhiều Service Record và có định dạng khác. Xem bên dưới.

### Ghi chú

TBD

## Standard LS2 Header

Loại 3, 7 và 9 sử dụng header LS2 tiêu chuẩn, được chỉ định bên dưới:

### Quy trình Lookup/Store

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
### Định dạng

- Unpublished/published: Để sử dụng khi gửi database store từ đầu cuối đến đầu cuối,
  router gửi có thể muốn chỉ định rằng leaseset này không nên được
  gửi cho các router khác. Hiện tại chúng ta sử dụng heuristics để duy trì trạng thái này.

- Published: Thay thế logic phức tạp cần thiết để xác định 'phiên bản' của
  leaseset. Hiện tại, phiên bản là thời gian hết hạn của lease hết hạn cuối cùng,
  và một router xuất bản phải tăng thời gian hết hạn đó lên ít nhất 1ms khi
  xuất bản một leaseset chỉ loại bỏ một lease cũ hơn.

- Expires: Cho phép một mục netDb hết hạn sớm hơn so với leaseset có thời gian hết hạn muộn nhất của nó. Có thể không hữu ích cho LS2, nơi các leaseset được dự kiến duy trì với thời gian hết hạn tối đa 11 phút, nhưng đối với các loại mới khác, điều này là cần thiết (xem Meta LS và Service Record bên dưới).

- Khóa offline là tùy chọn, nhằm giảm độ phức tạp triển khai ban đầu/bắt buộc.

### Các Cân nhắc về Quyền riêng tư/Bảo mật

- Có thể giảm độ chính xác timestamp thêm nữa (10 phút?) nhưng sẽ phải thêm số phiên bản. Điều này có thể phá vỡ multihoming, trừ khi chúng ta có mã hóa bảo toàn thứ tự? Có lẽ không thể hoàn toàn bỏ timestamps.

- Thay thế: 3 byte timestamp (epoch / 10 phút), 1-byte version, 2-byte expires

- Loại có được chỉ định rõ ràng hay ngầm định trong dữ liệu / chữ ký không? Các hằng số "Domain" cho chữ ký?

### Notes

- Các router không nên publish một LS quá một lần trong một giây.
  Nếu làm như vậy, chúng phải tăng timestamp được publish lên 1 một cách nhân tạo
  so với LS được publish trước đó.

- Các triển khai router có thể cache các transient key và chữ ký để
  tránh việc xác minh mỗi lần. Đặc biệt, các floodfill và router ở
  cả hai đầu của các kết nối tồn tại lâu dài có thể được hưởng lợi từ điều này.

- Khóa ngoại tuyến và chữ ký chỉ phù hợp cho các destination có thời gian sống lâu,
  tức là máy chủ, không phải client.

## New DatabaseEntry types

### Định dạng

Những thay đổi so với LeaseSet hiện tại:

- Thêm dấu thời gian xuất bản, dấu thời gian hết hạn, cờ hiệu và thuộc tính
- Thêm loại mã hóa
- Xóa khóa thu hồi

Tra cứu với

    Standard LS flag (1)
Lưu trữ với

    Standard LS2 type (3)
Lưu trữ tại

    Hash of destination
    This hash is then used to generate the daily "routing key", as in LS1
Thời hạn hết hạn điển hình

    10 minutes, as in a regular LS.
Xuất bản bởi

    Destination

### Lý do chính đáng

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
### Các vấn đề

- Properties: Mở rộng và tính linh hoạt trong tương lai.
  Được đặt đầu tiên trong trường hợp cần thiết cho việc phân tích dữ liệu còn lại.

- Nhiều cặp loại mã hóa/khóa công khai được sử dụng
  để dễ dàng chuyển đổi sang các loại mã hóa mới. Cách khác để thực hiện
  là xuất bản nhiều leaseSet, có thể sử dụng cùng các tunnel,
  như chúng ta đang làm hiện tại cho các điểm đến DSA và EdDSA.
  Việc xác định loại mã hóa đến trên một tunnel
  có thể được thực hiện bằng cơ chế session tag hiện có,
  và/hoặc thử giải mã bằng từng khóa. Độ dài của các
  thông điệp đến cũng có thể cung cấp gợi ý.

### Ghi chú

Đề xuất này tiếp tục sử dụng khóa công khai trong leaseset cho khóa mã hóa đầu-cuối-đầu, và để trường khóa công khai trong Destination không được sử dụng, như hiện tại. Loại mã hóa không được chỉ định trong chứng chỉ khóa Destination, nó sẽ vẫn là 0.

Một phương án thay thế bị từ chối là chỉ định loại mã hóa trong chứng chỉ khóa Destination, sử dụng khóa công khai trong Destination, và không sử dụng khóa công khai trong leaseset. Chúng tôi không có kế hoạch thực hiện điều này.

Lợi ích của LS2:

- Vị trí của khóa công khai thực tế không thay đổi.
- Loại mã hóa, hoặc khóa công khai, có thể thay đổi mà không làm thay đổi Destination.
- Loại bỏ trường thu hồi không được sử dụng
- Khả năng tương thích cơ bản với các loại DatabaseEntry khác trong đề xuất này
- Cho phép nhiều loại mã hóa

Nhược điểm của LS2:

- Vị trí của khóa công khai và loại mã hóa khác với RouterInfo
- Duy trì khóa công khai không sử dụng trong leaseset
- Yêu cầu triển khai trên toàn mạng; ngoài ra, các loại mã hóa thử nghiệm
  có thể được sử dụng, nếu được floodfills cho phép
  (nhưng xem các đề xuất liên quan 136 và 137 về hỗ trợ cho các loại sig thử nghiệm).
  Đề xuất thay thế có thể dễ triển khai và kiểm tra hơn cho các loại mã hóa thử nghiệm.

### New Encryption Issues

Một số trong những điều này nằm ngoài phạm vi của đề xuất này, nhưng tạm thời ghi chú tại đây vì chúng ta chưa có đề xuất mã hóa riêng biệt. Xem thêm các đề xuất ECIES 144 và 145.

- Loại mã hóa đại diện cho sự kết hợp
  của đường cong, độ dài khóa, và sơ đồ đầu cuối,
  bao gồm KDF và MAC, nếu có.

- Chúng tôi đã bao gồm trường độ dài khóa, để LS2 có thể
  được phân tích và xác minh bởi floodfill ngay cả với các loại mã hóa không xác định.

- Loại mã hóa mới đầu tiên được đề xuất có thể sẽ là
  ECIES/X25519. Cách nó được sử dụng end-to-end
  (hoặc là phiên bản được chỉnh sửa nhẹ của ElGamal/AES+SessionTag
  hoặc một cái gì đó hoàn toàn mới, ví dụ như ChaCha/Poly) sẽ được chỉ định
  trong một hoặc nhiều đề xuất riêng biệt.
  Xem thêm các đề xuất ECIES 144 và 145.

### LeaseSet 2

- Thời hạn 8-byte trong leases được thay đổi thành 4 bytes.

- Nếu chúng ta triển khai thu hồi trong tương lai, chúng ta có thể thực hiện bằng cách đặt trường expires bằng không,
  hoặc không có lease nào, hoặc cả hai. Không cần thiết phải có khóa thu hồi riêng biệt.

- Các khóa mã hóa được sắp xếp theo thứ tự ưu tiên của server, khóa được ưu tiên nhất đứng đầu.
  Hành vi mặc định của client là chọn khóa đầu tiên có
  loại mã hóa được hỗ trợ. Các client có thể sử dụng thuật toán lựa chọn khác
  dựa trên hỗ trợ mã hóa, hiệu suất tương đối và các yếu tố khác.

### Định dạng

Mục tiêu:

- Thêm blinding
- Cho phép nhiều loại chữ ký
- Không yêu cầu bất kỳ primitive mật mã mới nào
- Tùy chọn mã hóa cho từng người nhận, có thể thu hồi
- Hỗ trợ mã hóa chỉ Standard LS2 và Meta LS2

Encrypted LS2 không bao giờ được gửi trong thông điệp garlic encryption đầu cuối. Sử dụng LS2 tiêu chuẩn như trên.

Thay đổi từ LeaseSet được mã hóa hiện có:

- Mã hóa toàn bộ để đảm bảo bảo mật
- Mã hóa an toàn, không chỉ sử dụng AES.
- Mã hóa cho từng người nhận

Tra cứu với

    Standard LS flag (1)
Lưu trữ với

    Encrypted LS2 type (5)
Lưu trữ tại

    Hash of blinded sig type and blinded public key
    Two byte sig type (big endian, e.g. 0x000b) || blinded public key
    This hash is then used to generate the daily "routing key", as in LS1
Hết hạn thông thường

    10 minutes, as in a regular LS, or hours, as in a meta LS.
Được xuất bản bởi

    Destination


### Lý do chính đáng

Chúng tôi định nghĩa các hàm sau tương ứng với các khối xây dựng mật mã được sử dụng cho LS2 mã hóa:

CSRNG(n)

    n-byte output from a cryptographically-secure random number generator.

    In addition to the requirement of CSRNG being cryptographically-secure (and thus
    suitable for generating key material), it MUST be safe
    for some n-byte output to be used for key material when the byte sequences immediately
    preceding and following it are exposed on the network (such as in a salt, or encrypted
    padding). Implementations that rely on a potentially-untrustworthy source should hash
    any output that is to be exposed on the network. See [PRNG references](http://projectbullrun.org/dual-ec/ext-rand.html) and [Tor dev discussion](https://lists.torproject.org/pipermail/tor-dev/2015-November/009954.html).

H(p, d)

    SHA-256 hash function that takes a personalization string p and data d, and
    produces an output of length 32 bytes.

    Use SHA-256 as follows::

        H(p, d) := SHA-256(p || d)

STREAM

    The ChaCha20 stream cipher as specified in [RFC 7539 Section 2.4](https://tools.ietf.org/html/rfc7539#section-2.4), with the initial counter
    set to 1. S_KEY_LEN = 32 and S_IV_LEN = 12.

    ENCRYPT(k, iv, plaintext)
        Encrypts plaintext using the cipher key k, and nonce iv which MUST be unique for
        the key k. Returns a ciphertext that is the same size as the plaintext.

        The entire ciphertext must be indistinguishable from random if the key is secret.

    DECRYPT(k, iv, ciphertext)
        Decrypts ciphertext using the cipher key k, and nonce iv. Returns the plaintext.


SIG

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

DH

    X25519 public key agreement system. Private keys of 32 bytes, public keys of 32
    bytes, produces outputs of 32 bytes. It has the following
    functions:

    GENERATE_PRIVATE()
        Generates a new private key.

    DERIVE_PUBLIC(privkey)
        Returns the public key corresponding to the given private key.

    DH(privkey, pubkey)
        Generates a shared secret from the given private and public keys.

HKDF(salt, ikm, info, n)

    A cryptographic key derivation function which takes some input key material ikm (which
    should have good entropy but is not required to be a uniformly random string), a salt
    of length 32 bytes, and a context-specific 'info' value, and produces an output
    of n bytes suitable for use as key material.

    Use HKDF as specified in [RFC 5869](https://tools.ietf.org/html/rfc5869), using the HMAC hash function SHA-256
    as specified in [RFC 2104](https://tools.ietf.org/html/rfc2104). This means that SALT_LEN is 32 bytes max.


### Thảo luận

Định dạng LS2 mã hóa bao gồm ba lớp lồng nhau:

- Một lớp bên ngoài chứa thông tin plaintext cần thiết để lưu trữ và truy xuất.
- Một lớp giữa xử lý xác thực client.
- Một lớp bên trong chứa dữ liệu LS2 thực tế.

Định dạng tổng thể trông như sau::

    Layer 0 data + Enc(layer 1 data + Enc(layer 2 data)) + Signature

Lưu ý rằng LS2 được mã hóa sẽ bị làm mù (blinded). Destination không có trong header. Vị trí lưu trữ DHT là SHA-256(sig type || blinded public key), và được luân chuyển hàng ngày.

KHÔNG sử dụng header LS2 tiêu chuẩn được chỉ định ở trên.

#### Layer 0 (outer)

Loại

    1 byte

    Not actually in header, but part of data covered by signature.
    Take from field in Database Store Message.

Loại Chữ Ký Khóa Công Khai Mù

    2 bytes, big endian
    This will always be type 11, identifying a Red25519 blinded key.

Khóa Công Khai Được Che Giấu

    Length as implied by sig type

Dấu thời gian xuất bản

    4 bytes, big endian

    Seconds since epoch, rolls over in 2106

Hết hạn

    2 bytes, big endian

    Offset from published timestamp in seconds, 18.2 hours max

Cờ hiệu

    2 bytes

    Bit order: 15 14 ... 3 2 1 0

    Bit 0: If 0, no offline keys; if 1, offline keys

    Other bits: set to 0 for compatibility with future uses

Dữ liệu khóa tạm thời

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

lenOuterCiphertext

    2 bytes, big endian

outerCiphertext

    lenOuterCiphertext bytes

    Encrypted layer 1 data. See below for key derivation and encryption algorithms.

Chữ ký

    Length as implied by sig type of the signing key used

    The signature is of everything above.

    If the flag indicates offline keys, the signature is verified with the transient
    public key. Otherwise, the signature is verified with the blinded public key.


#### Layer 1 (middle)

Cờ hiệu

    1 byte
    
    Bit order: 76543210

    Bit 0: 0 for everybody, 1 for per-client, auth section to follow

    Bits 3-1: Authentication scheme, only if bit 0 is set to 1 for per-client, otherwise 000
              000: DH client authentication (or no per-client authentication)
              001: PSK client authentication

    Bits 7-4: Unused, set to 0 for future compatibility

Dữ liệu xác thực client DH

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

Dữ liệu xác thực client PSK

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


innerCiphertext

    Length implied by lenOuterCiphertext (whatever data remains)

    Encrypted layer 2 data. See below for key derivation and encryption algorithms.


#### Layer 2 (inner)

Loại

    1 byte

    Either 3 (LS2) or 7 (Meta LS2)

Dữ liệu

    LeaseSet2 data for the given type.

    Includes the header and signature.


### Các Vấn Đề Mã Hóa Mới

Chúng tôi sử dụng sơ đồ sau đây để làm mù khóa (key blinding), dựa trên Ed25519 và [ZCash RedDSA](https://github.com/zcash/zips/tree/master/protocol/protocol.pdf). Các chữ ký Re25519 được thực hiện trên đường cong Ed25519, sử dụng SHA-512 cho hàm băm.

Chúng tôi không sử dụng [Tor's rend-spec-v3.txt appendix A.2](https://spec.torproject.org/rend-spec-v3), có cùng mục tiêu thiết kế, bởi vì các blinded public key của nó có thể nằm ngoài prime-order subgroup, với những tác động bảo mật chưa rõ.

#### Goals

- Khóa công khai ký trong destination không che mù phải là
  Ed25519 (loại chữ ký 7) hoặc Red25519 (loại chữ ký 11);
  không hỗ trợ các loại chữ ký khác
- Nếu khóa công khai ký đang offline, khóa công khai ký tạm thời cũng phải là Ed25519
- Việc che mù có tính toán đơn giản
- Sử dụng các nguyên tố mật mã hiện có
- Khóa công khai đã che mù không thể bỏ che mù
- Khóa công khai đã che mù phải nằm trên đường cong Ed25519 và nhóm con bậc nguyên tố
- Phải biết khóa công khai ký của destination
  (không cần destination đầy đủ) để tạo ra khóa công khai đã che mù
- Tùy chọn cung cấp thêm bí mật bổ sung cần thiết để tạo ra khóa công khai đã che mù

#### Security

Tính bảo mật của một sơ đồ blinding yêu cầu rằng phân phối của alpha phải giống với các khóa riêng không bị blinded. Tuy nhiên, khi chúng ta blind một khóa riêng Ed25519 (sig type 7) thành khóa riêng Red25519 (sig type 11), phân phối sẽ khác nhau. Để đáp ứng các yêu cầu của [zcash section 4.1.6.1](https://github.com/zcash/zips/tree/master/protocol/protocol.pdf), Red25519 (sig type 11) cũng nên được sử dụng cho các khóa chưa bị blinded, để "sự kết hợp của một khóa công khai được tái ngẫu nhiên hóa và (các) chữ ký dưới khóa đó không tiết lộ khóa mà từ đó nó được tái ngẫu nhiên hóa." Chúng tôi cho phép type 7 đối với các destination hiện có, nhưng khuyến nghị type 11 cho các destination mới sẽ được mã hóa.

#### Definitions

B

    The Ed25519 base point (generator) 2^255 - 19 as in [Ed25519](http://cr.yp.to/papers.html#ed25519)

L

    The Ed25519 order 2^252 + 27742317777372353535851937790883648493
    as in [Ed25519](http://cr.yp.to/papers.html#ed25519)

DERIVE_PUBLIC(a)

    Convert a private key to public, as in Ed25519 (mulitply by G)

alpha

    A 32-byte random number known to those who know the destination.

GENERATE_ALPHA(destination, date, secret)

    Generate alpha for the current date, for those who know the destination and the secret.
    The result must be identically distributed as Ed25519 private keys.

a

    The unblinded 32-byte EdDSA or RedDSA signing private key used to sign the destination

A

    The unblinded 32-byte EdDSA or RedDSA signing public key in the destination,
    = DERIVE_PUBLIC(a), as in Ed25519

a'

    The blinded 32-byte EdDSA signing private key used to sign the encrypted leaseset
    This is a valid EdDSA private key.

A'

    The blinded 32-byte EdDSA signing public key in the Destination,
    may be generated with DERIVE_PUBLIC(a'), or from A and alpha.
    This is a valid EdDSA public key, on the curve and on the prime-order subgroup.

LEOS2IP(x)

    Flip the order of the input bytes to little-endian

H*(x)

    32 bytes = (LEOS2IP(SHA512(x))) mod B, same as in Ed25519 hash-and-reduce


#### Blinding Calculations

Một cặp khóa secret alpha và blinded key mới phải được tạo ra mỗi ngày (UTC). Khóa secret alpha và blinded key được tính toán như sau.

GENERATE_ALPHA(destination, date, secret), cho tất cả các bên:

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
BLIND_PRIVKEY(), dành cho chủ sở hữu xuất bản leaseset:

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
BLIND_PUBKEY(), cho các client truy xuất leaseset:

```text
// BLIND_PUBKEY()

  alpha = GENERATE_ALPHA(destination, date, secret)
  A = destination's signing public key
  // Addition using group elements (points on the curve)
  blinded public key = A' = BLIND_PUBKEY(A, alpha) = A + DERIVE_PUBLIC(alpha)
```
Cả hai phương pháp tính A' đều cho ra cùng một kết quả, như yêu cầu.

#### Signing

LeaseSet không được làm mù được ký bởi khóa riêng ký Ed25519 hoặc Red25519 không được làm mù và được xác minh bằng khóa công khai ký Ed25519 hoặc Red25519 không được làm mù (các loại chữ ký 7 hoặc 11) như thường lệ.

Nếu khóa công khai ký tên đang offline, leaseset chưa được làm mù sẽ được ký bằng khóa riêng ký tên tạm thời Ed25519 hoặc Red25519 chưa được làm mù và được xác minh với khóa công khai ký tên tạm thời Ed25519 hoặc Red25519 chưa được làm mù (loại chữ ký 7 hoặc 11) như thông thường. Xem bên dưới để biết thêm ghi chú về khóa offline cho leaseset được mã hóa.

Để ký cho leaseset được mã hóa, chúng tôi sử dụng Red25519, dựa trên [RedDSA](https://github.com/zcash/zips/tree/master/protocol/protocol.pdf) để ký và xác minh với các khóa bị làm mờ. Các chữ ký Red25519 được thực hiện trên đường cong Ed25519, sử dụng SHA-512 cho hàm băm.

Red25519 giống hệt với Ed25519 tiêu chuẩn trừ những điểm được chỉ định bên dưới.

#### Sign/Verify Calculations

Phần bên ngoài của leaseset được mã hóa sử dụng khóa và chữ ký Red25519.

Red25519 gần như giống hệt Ed25519. Có hai điểm khác biệt:

Khóa riêng tư Red25519 được tạo ra từ các số ngẫu nhiên và sau đó phải được rút gọn theo mod L, trong đó L được định nghĩa ở trên. Khóa riêng tư Ed25519 được tạo ra từ các số ngẫu nhiên và sau đó được "kẹp" bằng cách sử dụng bitwise masking cho các byte 0 và 31. Điều này không được thực hiện đối với Red25519. Các hàm GENERATE_ALPHA() và BLIND_PRIVKEY() được định nghĩa ở trên tạo ra các khóa riêng tư Red25519 hợp lệ bằng cách sử dụng mod L.

Trong Red25519, việc tính toán r cho việc ký sử dụng dữ liệu ngẫu nhiên bổ sung, và sử dụng giá trị khóa công khai thay vì hash của khóa riêng tư. Do có dữ liệu ngẫu nhiên, mỗi chữ ký Red25519 đều khác nhau, ngay cả khi ký cùng một dữ liệu với cùng một khóa.

Ký:

```text
T = 80 random bytes
  r = H*(T || publickey || message)
  // rest is the same as in Ed25519
```
Xác minh:

```text
// same as in Ed25519
```
### Ghi chú

#### Derivation of subcredentials

Như một phần của quá trình blinding, chúng ta cần đảm bảo rằng một LS2 đã mã hóa chỉ có thể được giải mã bởi người biết signing public key tương ứng của Destination. Không cần có đầy đủ Destination. Để đạt được điều này, chúng ta tạo ra một credential từ signing public key:

```text
A = destination's signing public key
  stA = signature type of A, 2 bytes big endian (0x0007 or 0x000b)
  stA' = signature type of A', 2 bytes big endian (0x000b)
  keydata = A || stA || stA'
  credential = H("credential", keydata)
```
Chuỗi cá nhân hóa đảm bảo rằng thông tin xác thực không xung đột với bất kỳ hash nào được sử dụng làm khóa tra cứu DHT, chẳng hạn như hash Destination thuần túy.

Đối với một khóa được làm mờ nhất định, chúng ta có thể sau đó suy ra một subcredential:

```text
subcredential = H("subcredential", credential || blindedPublicKey)
```
Subcredential được bao gồm trong các quy trình dẫn xuất khóa bên dưới, điều này liên kết những khóa đó với việc biết khóa công khai ký của Destination.

#### Layer 1 encryption

Đầu tiên, đầu vào cho quá trình dẫn xuất khóa được chuẩn bị:

```text
outerInput = subcredential || publishedTimestamp
```
Tiếp theo, một salt ngẫu nhiên sẽ được tạo ra:

```text
outerSalt = CSRNG(32)
```
Sau đó khóa được sử dụng để mã hóa lớp 1 được tạo ra:

```text
keys = HKDF(outerSalt, outerInput, "ELS2_L1K", 44)
  outerKey = keys[0:31]
  outerIV = keys[32:43]
```
Cuối cùng, lớp 1 plaintext được mã hóa và tuần tự hóa:

```text
outerCiphertext = outerSalt || ENCRYPT(outerKey, outerIV, outerPlaintext)
```
#### Layer 1 decryption

Muối được phân tích từ bản mã hóa lớp 1:

```text
outerSalt = outerCiphertext[0:31]
```
Sau đó khóa được sử dụng để mã hóa lớp 1 được tạo ra:

```text
outerInput = subcredential || publishedTimestamp
  keys = HKDF(outerSalt, outerInput, "ELS2_L1K", 44)
  outerKey = keys[0:31]
  outerIV = keys[32:43]
```
Cuối cùng, layer 1 ciphertext được giải mã:

```text
outerPlaintext = DECRYPT(outerKey, outerIV, outerCiphertext[32:end])
```
#### Layer 2 encryption

Khi xác thực client được bật, ``authCookie`` được tính toán như mô tả bên dưới. Khi xác thực client bị tắt, ``authCookie`` là mảng byte có độ dài bằng không.

Việc mã hóa tiến hành theo cách thức tương tự như lớp 1:

```text
innerInput = authCookie || subcredential || publishedTimestamp
  innerSalt = CSRNG(32)
  keys = HKDF(innerSalt, innerInput, "ELS2_L2K", 44)
  innerKey = keys[0:31]
  innerIV = keys[32:43]
  innerCiphertext = innerSalt || ENCRYPT(innerKey, innerIV, innerPlaintext)
```
#### Layer 2 decryption

Khi xác thực client được kích hoạt, ``authCookie`` được tính toán như mô tả bên dưới. Khi xác thực client bị vô hiệu hóa, ``authCookie`` là mảng byte có độ dài bằng không.

Quá trình giải mã diễn ra theo cách tương tự như layer 1:

```text
innerInput = authCookie || subcredential || publishedTimestamp
  innerSalt = innerCiphertext[0:31]
  keys = HKDF(innerSalt, innerInput, "ELS2_L2K", 44)
  innerKey = keys[0:31]
  innerIV = keys[32:43]
  innerPlaintext = DECRYPT(innerKey, innerIV, innerCiphertext[32:end])
```
### LS2 được mã hóa

Khi client authorization được kích hoạt cho một Destination, máy chủ duy trì một danh sách các client mà họ đang ủy quyền để giải mã dữ liệu LS2 được mã hóa. Dữ liệu được lưu trữ cho mỗi client phụ thuộc vào cơ chế ủy quyền, và bao gồm một số dạng key material mà mỗi client tạo ra và gửi đến máy chủ thông qua một cơ chế out-of-band an toàn.

Có hai phương án thay thế để triển khai xác thực theo từng client:

#### DH client authorization

Mỗi client tạo ra một cặp khóa DH ``[csk_i, cpk_i]``, và gửi khóa công khai ``cpk_i`` tới server.

Xử lý máy chủ
^^^^^^^^^^^^^^^^^

Máy chủ tạo ra một ``authCookie`` mới và một cặp khóa DH tạm thời:

```text
authCookie = CSRNG(32)
  esk = GENERATE_PRIVATE()
  epk = DERIVE_PUBLIC(esk)
```
Sau đó, với mỗi client được ủy quyền, server sẽ mã hóa ``authCookie`` bằng khóa công khai của nó:

```text
sharedSecret = DH(esk, cpk_i)
  authInput = sharedSecret || cpk_i || subcredential || publishedTimestamp
  okm = HKDF(epk, authInput, "ELS2_XCA", 52)
  clientKey_i = okm[0:31]
  clientIV_i = okm[32:43]
  clientID_i = okm[44:51]
  clientCookie_i = ENCRYPT(clientKey_i, clientIV_i, authCookie)
```
Máy chủ đặt mỗi tuple ``[clientID_i, clientCookie_i]`` vào layer 1 của LS2 được mã hóa, cùng với ``epk``.

Xử lý client
^^^^^^^^^

Client sử dụng private key của mình để tạo ra client identifier dự kiến ``clientID_i``, encryption key ``clientKey_i``, và encryption IV ``clientIV_i``:

```text
sharedSecret = DH(csk_i, epk)
  authInput = sharedSecret || cpk_i || subcredential || publishedTimestamp
  okm = HKDF(epk, authInput, "ELS2_XCA", 52)
  clientKey_i = okm[0:31]
  clientIV_i = okm[32:43]
  clientID_i = okm[44:51]
```
Sau đó client tìm kiếm trong dữ liệu xác thực layer 1 để tìm một mục chứa ``clientID_i``. Nếu tồn tại một mục khớp, client sẽ giải mã nó để thu được ``authCookie``:

```text
authCookie = DECRYPT(clientKey_i, clientIV_i, clientCookie_i)
```
#### Pre-shared key client authorization

Mỗi client tạo ra một khóa bí mật 32-byte ``psk_i``, và gửi nó đến server. Hoặc server có thể tạo khóa bí mật, và gửi nó đến một hoặc nhiều client.

Xử lý máy chủ
^^^^^^^^^^^^^^^^^

Máy chủ tạo ra một ``authCookie`` và salt mới:

```text
authCookie = CSRNG(32)
  authSalt = CSRNG(32)
```
Sau đó, đối với mỗi client được ủy quyền, server mã hóa ``authCookie`` bằng khóa chia sẻ trước của nó:

```text
authInput = psk_i || subcredential || publishedTimestamp
  okm = HKDF(authSalt, authInput, "ELS2PSKA", 52)
  clientKey_i = okm[0:31]
  clientIV_i = okm[32:43]
  clientID_i = okm[44:51]
  clientCookie_i = ENCRYPT(clientKey_i, clientIV_i, authCookie)
```
Máy chủ đặt từng tuple ``[clientID_i, clientCookie_i]`` vào layer 1 của LS2 được mã hóa, cùng với ``authSalt``.

Xử lý phía client
^^^^^^^^^^^^^^^^^

Client sử dụng pre-shared key của mình để tạo ra client identifier dự kiến ``clientID_i``, encryption key ``clientKey_i``, và encryption IV ``clientIV_i``:

```text
authInput = psk_i || subcredential || publishedTimestamp
  okm = HKDF(authSalt, authInput, "ELS2PSKA", 52)
  clientKey_i = okm[0:31]
  clientIV_i = okm[32:43]
  clientID_i = okm[44:51]
```
Sau đó client tìm kiếm trong dữ liệu ủy quyền layer 1 để tìm một entry chứa ``clientID_i``. Nếu tồn tại một entry khớp, client sẽ giải mã nó để lấy ``authCookie``:

```text
authCookie = DECRYPT(clientKey_i, clientIV_i, clientCookie_i)
```
#### Security considerations

Cả hai cơ chế ủy quyền client ở trên đều cung cấp quyền riêng tư cho thành viên client. Một thực thể chỉ biết Destination có thể thấy có bao nhiêu client đang đăng ký tại bất kỳ thời điểm nào, nhưng không thể theo dõi client nào đang được thêm vào hoặc thu hồi.

Các server NÊN ngẫu nhiên hóa thứ tự của các client mỗi lần chúng tạo ra một LS2 được mã hóa, để ngăn các client biết được vị trí của họ trong danh sách và suy luận khi nào các client khác đã được thêm vào hoặc thu hồi.

Một máy chủ CÓ THỂ chọn ẩn số lượng client đã đăng ký bằng cách chèn các mục ngẫu nhiên vào danh sách dữ liệu ủy quyền.

Ưu điểm của ủy quyền client DH
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Tính bảo mật của sơ đồ không hoàn toàn phụ thuộc vào việc trao đổi khóa client qua kênh ngoài băng tần. Khóa riêng của client không bao giờ cần rời khỏi thiết bị của họ, do đó kẻ tấn công có thể chặn được việc trao đổi qua kênh ngoài băng tần, nhưng không thể phá vỡ thuật toán DH, sẽ không thể giải mã LS2 đã mã hóa hoặc xác định được thời gian client được cấp quyền truy cập.

Nhược điểm của xác thực client DH
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Yêu cầu N + 1 phép toán DH ở phía server cho N client.
- Yêu cầu một phép toán DH ở phía client.
- Yêu cầu client tạo ra khóa bí mật.

Ưu điểm của xác thực client bằng PSK
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Không yêu cầu các phép toán DH.
- Cho phép server tạo ra khóa bí mật.
- Cho phép server chia sẻ cùng một khóa với nhiều client, nếu muốn.

Nhược điểm của xác thực client PSK
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Tính bảo mật của sơ đồ này phụ thuộc nghiêm trọng vào việc trao đổi khóa client thông qua kênh ngoài băng tần. Kẻ tấn công có thể chặn bắt việc trao đổi cho một client cụ thể sẽ có thể giải mã bất kỳ LS2 được mã hóa tiếp theo mà client đó được ủy quyền, cũng như xác định thời điểm quyền truy cập của client bị thu hồi.

### Định nghĩa

Xem đề xuất 149.

Bạn không thể sử dụng LS2 được mã hóa cho bittorrent, vì các phản hồi announce compact chỉ có 32 byte. 32 byte này chỉ chứa hash. Không có chỗ cho chỉ báo rằng leaseset được mã hóa, hoặc các loại chữ ký.

### Định dạng

Đối với các leaseSet được mã hóa với khóa ngoại tuyến, các khóa riêng được làm mù cũng phải được tạo ngoại tuyến, một khóa cho mỗi ngày.

Vì khối chữ ký ngoại tuyến tùy chọn nằm trong phần văn bản rõ của leaseset được mã hóa, bất kỳ ai thu thập dữ liệu từ các floodfill đều có thể sử dụng thông tin này để theo dõi leaseset (nhưng không thể giải mã nó) trong vài ngày. Để ngăn chặn điều này, chủ sở hữu của các khóa nên tạo ra các khóa tạm thời mới cho mỗi ngày. Cả khóa tạm thời và khóa blinded đều có thể được tạo trước và chuyển giao cho router theo từng lô.

Không có định dạng tệp nào được định nghĩa trong đề xuất này để đóng gói nhiều khóa tạm thời và khóa mù và cung cấp chúng cho client hoặc router. Không có cải tiến giao thức I2CP nào được định nghĩa trong đề xuất này để hỗ trợ các leaseSet được mã hóa với các khóa offline.

### Notes

- Một service sử dụng leaseSet được mã hóa sẽ xuất bản phiên bản mã hóa lên
  floodfill. Tuy nhiên, để tăng hiệu quả, nó sẽ gửi leaseSet không mã hóa cho
  client trong garlic message được bọc, sau khi xác thực (thông qua whitelist,
  chẳng hạn).

- Floodfill có thể giới hạn kích thước tối đa ở mức hợp lý để ngăn chặn lạm dụng.

- Sau khi giải mã, cần thực hiện một số kiểm tra, bao gồm việc đảm bảo
  timestamp bên trong và thời gian hết hạn khớp với những giá trị ở cấp cao nhất.

- ChaCha20 được chọn thay vì AES. Trong khi tốc độ tương tự nhau nếu có hỗ trợ phần cứng AES, ChaCha20 nhanh hơn 2.5-3 lần khi không có hỗ trợ phần cứng AES, chẳng hạn như trên các thiết bị ARM tầm thấp.

- Chúng tôi không quan tâm đủ về tốc độ để sử dụng keyed BLAKE2b. Nó có kích thước đầu ra đủ lớn để chứa n lớn nhất mà chúng tôi yêu cầu (hoặc chúng ta có thể gọi nó một lần cho mỗi khóa mong muốn với một đối số bộ đếm). BLAKE2b nhanh hơn nhiều so với SHA-256, và keyed-BLAKE2b sẽ giảm tổng số lần gọi hàm hash. Tuy nhiên, xem đề xuất 148, nơi đề xuất rằng chúng ta chuyển sang BLAKE2b vì những lý do khác. Xem [Hiệu suất dẫn xuất khóa an toàn](https://www.lvh.io/posts/secure-key-derivation-performance.html).

### Meta LS2

Điều này được sử dụng để thay thế multihoming. Giống như bất kỳ leaseset nào, điều này được ký bởi người tạo. Đây là danh sách được xác thực các destination hash.

Meta LS2 là đỉnh của, và có thể là các nút trung gian của, một cấu trúc cây. Nó chứa một số entry, mỗi entry trỏ đến một LS, LS2, hoặc một Meta LS2 khác để hỗ trợ multihoming quy mô lớn. Một Meta LS2 có thể chứa hỗn hợp các entry LS, LS2, và Meta LS2. Các lá của cây luôn là LS hoặc LS2. Cây này là một DAG; các vòng lặp bị cấm; client thực hiện lookup phải phát hiện và từ chối theo dõi các vòng lặp.

Một Meta LS2 có thể có thời gian hết hạn dài hơn nhiều so với LS hoặc LS2 tiêu chuẩn. Cấp độ cao nhất có thể có thời gian hết hạn vài giờ sau ngày xuất bản. Thời gian hết hạn tối đa sẽ được thực thi bởi các floodfill và client, và hiện đang được xác định (TBD).

Trường hợp sử dụng cho Meta LS2 là multihoming quy mô lớn, nhưng không có thêm bảo vệ nào cho việc liên kết các router với leaseSet (tại thời điểm khởi động lại router) so với những gì được cung cấp hiện tại với LS hoặc LS2. Điều này tương đương với trường hợp sử dụng "facebook", có thể không cần bảo vệ chống liên kết. Trường hợp sử dụng này có thể cần các khóa offline, được cung cấp trong header tiêu chuẩn tại mỗi nút của cây.

Giao thức back-end để phối hợp giữa các leaf router, các intermediate và master Meta LS signer không được chỉ định ở đây. Các yêu cầu cực kỳ đơn giản - chỉ cần xác minh rằng peer đang hoạt động, và xuất bản một LS mới vài giờ một lần. Độ phức tạp duy nhất là việc chọn những publisher mới cho các Meta LS cấp cao nhất hoặc cấp trung gian khi xảy ra lỗi.

Các leaseset mix-and-match trong đó các lease từ nhiều router được kết hợp, ký và xuất bản trong một leaseset duy nhất được tài liệu hóa trong đề xuất 140, "invisible multihoming". Đề xuất này không khả thi như đã viết, bởi vì các kết nối streaming sẽ không "dính" với một router duy nhất, xem http://zzz.i2p/topics/2335 .

Giao thức back-end và tương tác với các thành phần nội bộ của router và client sẽ khá phức tạp đối với invisible multihoming.

Để tránh quá tải floodfill cho Meta LS cấp cao nhất, thời gian hết hạn nên là ít nhất vài giờ. Clients phải cache Meta LS cấp cao nhất và duy trì nó qua các lần khởi động lại nếu chưa hết hạn.

Chúng ta cần định nghĩa một thuật toán nào đó để các client có thể duyệt qua cây, bao gồm cả các phương án dự phòng, sao cho việc sử dụng được phân tán. Một hàm số nào đó dựa trên khoảng cách hash, chi phí và tính ngẫu nhiên. Nếu một node có cả LS hoặc LS2 và Meta LS, chúng ta cần biết khi nào được phép sử dụng các leaseSet đó, và khi nào tiếp tục duyệt qua cây.

Tra cứu với

    Standard LS flag (1)
Lưu trữ với

    Meta LS2 type (7)
Lưu trữ tại

    Hash of destination
    This hash is then used to generate the daily "routing key", as in LS1
Hết hạn điển hình

    Hours. Max 18.2 hours (65535 seconds)
Được xuất bản bởi

    "master" Destination or coordinator, or intermediate coordinators

### Format

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
Cờ và thuộc tính: để sử dụng trong tương lai

### Dẫn xuất Khóa Blinding

- Một dịch vụ phân tán sử dụng cơ chế này sẽ có một hoặc nhiều "master" với khóa riêng của service destination. Chúng sẽ (ngoài băng tần) xác định danh sách hiện tại của các destination đang hoạt động và sẽ xuất bản Meta LS2. Để đảm bảo dự phòng, nhiều master có thể multihome (tức là xuất bản đồng thời) Meta LS2.

- Một dịch vụ phân tán có thể bắt đầu với một destination duy nhất hoặc sử dụng multihoming kiểu cũ, sau đó chuyển sang Meta LS2. Một tra cứu LS tiêu chuẩn có thể trả về bất kỳ một trong số LS, LS2, hoặc Meta LS2.

- Khi một dịch vụ sử dụng Meta LS2, nó không có tunnel nào (leases).

### Service Record

Đây là một bản ghi cá nhân cho biết rằng một điểm đến đang tham gia vào một dịch vụ. Nó được gửi từ người tham gia đến floodfill. Nó không bao giờ được gửi riêng lẻ bởi một floodfill, mà chỉ là một phần của Service List. Service Record cũng được sử dụng để thu hồi việc tham gia vào một dịch vụ, bằng cách đặt thời gian hết hạn về không.

Đây không phải là LS2 nhưng nó sử dụng định dạng header và chữ ký LS2 tiêu chuẩn.

Tra cứu với

    n/a, see Service List
Lưu trữ với

    Service Record type (9)
Lưu trữ tại

    Hash of service name
    This hash is then used to generate the daily "routing key", as in LS1
Hết hạn điển hình

    Hours. Max 18.2 hours (65535 seconds)
Được xuất bản bởi

    Destination

### Format

```
Standard LS2 Header as specified above

  Service Record Type-Specific Part
  - Port (2 bytes, big endian) (0 if unspecified)
  - Hash of service name (32 bytes)

  Standard LS2 Signature:
  - Signature (40+ bytes)
    The signature is of everything above.
```
### Notes

- Nếu expires là toàn số không, floodfill nên thu hồi bản ghi và không còn
  bao gồm nó trong danh sách dịch vụ.

- Storage: Floodfill có thể nghiêm ngặt điều tiết việc lưu trữ các bản ghi này và
  giới hạn số lượng bản ghi được lưu trữ cho mỗi hash cùng thời hạn hết hạn của chúng. Một danh sách trắng
  các hash cũng có thể được sử dụng.

- Bất kỳ loại netDb nào khác tại cùng một hash đều có độ ưu tiên cao hơn, vì vậy một service record không bao giờ có thể ghi đè một LS/RI, nhưng một LS/RI sẽ ghi đè tất cả các service record tại hash đó.

### Service List

Điều này hoàn toàn không giống như một LS2 và sử dụng một định dạng khác.

Danh sách dịch vụ được tạo và ký bởi floodfill. Nó không được xác thực ở chỗ bất kỳ ai cũng có thể tham gia một dịch vụ bằng cách xuất bản một Service Record tới floodfill.

Danh sách Dịch vụ chứa các Bản ghi Dịch vụ Ngắn, không phải Bản ghi Dịch vụ đầy đủ. Những bản ghi này chứa chữ ký nhưng chỉ có hash, không có destination đầy đủ, vì vậy chúng không thể được xác minh nếu không có destination đầy đủ.

Tính bảo mật (nếu có) và tính mong muốn của danh sách dịch vụ vẫn đang được xác định. Các floodfill có thể giới hạn việc xuất bản và tra cứu chỉ với danh sách trắng các dịch vụ, nhưng danh sách trắng này có thể khác nhau tùy theo cách triển khai hoặc sở thích của người vận hành. Có thể không thể đạt được sự đồng thuận về một danh sách trắng cơ bản, chung giữa các phiên bản triển khai.

Nếu tên dịch vụ được bao gồm trong bản ghi dịch vụ ở trên, thì các nhà điều hành floodfill có thể phản đối; nếu chỉ bao gồm hash, sẽ không có xác minh, và một bản ghi dịch vụ có thể "xen vào" trước bất kỳ loại netdb nào khác và được lưu trữ trong floodfill.

Tra cứu với

    Service List lookup type (11)
Lưu trữ với

    Service List type (11)
Lưu trữ tại

    Hash of service name
    This hash is then used to generate the daily "routing key", as in LS1
Thời hạn hết hạn điển hình

    Hours, not specified in the list itself, up to local policy
Được xuất bản bởi

    Nobody, never sent to floodfill, never flooded.

### Format

KHÔNG sử dụng header LS2 chuẩn được chỉ định ở trên.

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
Để xác minh chữ ký của Service List:

- thêm hash của tên dịch vụ vào đầu
- xóa hash của người tạo
- Kiểm tra chữ ký của nội dung đã được sửa đổi

Để xác minh chữ ký của mỗi Short Service Record:

- Lấy đích đến
- Kiểm tra chữ ký của (thời gian xuất bản + hết hạn + cờ + cổng + Hash của
  tên dịch vụ)

Để xác minh chữ ký của mỗi Revocation Record:

- Lấy điểm đến
- Kiểm tra chữ ký của (published timestamp + 4 zero bytes + flags + port + Hash
  của tên dịch vụ)

### Notes

- Chúng tôi sử dụng độ dài chữ ký thay vì loại chữ ký để có thể hỗ trợ các loại chữ ký không xác định.

- Không có thời hạn hết hiệu lực cho danh sách dịch vụ, người nhận có thể tự đưa ra
  quyết định dựa trên chính sách hoặc thời hạn hết hiệu lực của các bản ghi riêng lẻ.

- Danh sách Dịch vụ không được flood, chỉ các Bản ghi Dịch vụ riêng lẻ mới được flood. Mỗi
  floodfill tạo ra, ký và lưu cache một Danh sách Dịch vụ. Floodfill sử dụng
  chính sách riêng của mình cho thời gian cache và số lượng tối đa các bản ghi
  dịch vụ và thu hồi.

## Common Structures Spec Changes Required

### Mã hóa và xử lý

Nằm ngoài phạm vi của đề xuất này. Thêm vào các đề xuất ECIES 144 và 145.

### New Intermediate Structures

Thêm các cấu trúc mới cho Lease2, MetaLease, LeaseSet2Header, và OfflineSignature. Có hiệu lực từ phiên bản 0.9.38.

### New NetDB Types

Thêm các cấu trúc cho mỗi loại leaseset mới, được tích hợp từ phần trên. Đối với LeaseSet2, EncryptedLeaseSet và MetaLeaseSet, có hiệu lực kể từ phiên bản 0.9.38. Đối với Service Record và Service List, đang ở giai đoạn sơ bộ và chưa được lên lịch.

### New Signature Type

Thêm RedDSA_SHA512_Ed25519 Loại 11. Khóa công khai là 32 byte; khóa riêng tư là 32 byte; hash là 64 byte; chữ ký là 64 byte.

## Encryption Spec Changes Required

Nằm ngoài phạm vi của đề xuất này. Xem đề xuất 144 và 145.

## I2NP Changes Required

Thêm ghi chú: LS2 chỉ có thể được xuất bản lên các floodfill có phiên bản tối thiểu.

### Database Lookup Message

Thêm kiểu tra cứu danh sách dịch vụ.

### Changes

```
Flags byte: Lookup type field, currently bits 3-2, expands to bits 4-2.
  Lookup type 0x04 is defined as the service list lookup.

  Add note: Service list loookup may only be sent to floodfills with a minimum version.
  Minimum version is 0.9.38.
```
### Xác thực cho từng client

Thêm tất cả các loại store mới.

### Changes

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
## I2CP Changes Required

### I2CP Options

Các tùy chọn mới được diễn giải phía router, gửi trong SessionConfig Mapping:

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
Các tùy chọn mới được diễn giải phía client:

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
### Session Config

Lưu ý rằng đối với chữ ký ngoại tuyến, các tùy chọn i2cp.leaseSetOfflineExpiration, i2cp.leaseSetTransientPublicKey, và i2cp.leaseSetOfflineSignature là bắt buộc, và chữ ký được thực hiện bởi khóa riêng ký tạm thời.

### Encrypted LS với Base 32 Addresses

Router đến client. Không có thay đổi. Các lease được gửi với timestamp 8-byte, ngay cả khi leaseSet được trả về sẽ là LS2 với timestamp 4-byte. Lưu ý rằng phản hồi có thể là một Create Leaseset hoặc Create Leaseset2 Message.

### LS Mã hóa với Khóa Offline

Router tới client. Không có thay đổi. Các lease được gửi với timestamp 8-byte, ngay cả khi leaseSet được trả về sẽ là LS2 với timestamp 4-byte. Lưu ý rằng phản hồi có thể là thông điệp Create Leaseset hoặc Create Leaseset2.

### Ghi chú

Client tới router. Tin nhắn mới, sử dụng thay cho Create Leaseset Message.

### Meta LS2

- Để router có thể phân tích loại store, loại này phải có trong message,
  trừ khi nó được truyền cho router trước đó trong session config.
  Để có mã phân tích chung, việc có nó trong chính message sẽ dễ dàng hơn.

- Để router biết loại và độ dài của private key,
  nó phải được đặt sau lease set, trừ khi parser đã biết loại trước
  trong session config.
  Đối với common parsing code, việc biết thông tin này từ chính message sẽ dễ dàng hơn.

- Khóa riêng tư ký (signing private key), trước đây được định nghĩa để thu hồi và không sử dụng,
  không có mặt trong LS2.

### Định dạng

Loại thông điệp cho Create Leaseset2 Message là 41.

### Ghi chú

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
### Bản Ghi Dịch Vụ

- Phiên bản router tối thiểu là 0.9.39.
- Phiên bản sơ bộ với message type 40 có trong 0.9.38 nhưng định dạng đã bị thay đổi.
  Type 40 đã bị loại bỏ và không được hỗ trợ.

### Định dạng

- Cần thêm nhiều thay đổi để hỗ trợ leaseSet được mã hóa và meta LS.

### Ghi chú

Client đến router. Tin nhắn mới.

### Danh Sách Dịch Vụ

- Router cần biết liệu một destination có bị blinded hay không.
  Nếu nó bị blinded và sử dụng xác thực bí mật hoặc theo từng client,
  nó cũng cần có thông tin đó.

- Tra cứu Host của địa chỉ b32 định dạng mới ("b33")
  thông báo cho router rằng địa chỉ đó được làm mù, nhưng không có cơ chế nào để
  truyền khóa bí mật hoặc khóa riêng tư đến router trong thông điệp Host Lookup.
  Mặc dù chúng ta có thể mở rộng thông điệp Host Lookup để thêm thông tin đó,
  nhưng việc định nghĩa một thông điệp mới sẽ sạch sẽ hơn.

- Chúng ta cần một cách lập trình để client có thể thông báo cho router.
  Nếu không, người dùng sẽ phải cấu hình thủ công từng destination.

### Định dạng

Trước khi một client gửi tin nhắn đến một đích blinded, nó phải tra cứu "b33" trong một tin nhắn Host Lookup, hoặc gửi một tin nhắn Blinding Info. Nếu đích blinded yêu cầu secret hoặc xác thực per-client, client phải gửi một tin nhắn Blinding Info.

Router không gửi phản hồi cho thông điệp này.

### Ghi chú

Loại thông điệp cho Blinding Info Message là 42.

### Format

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
### Chứng chỉ khóa

- Phiên bản router tối thiểu là 0.9.43

### Các Cấu Trúc Trung Gian Mới

### Các Loại NetDB Mới

Để hỗ trợ tra cứu tên máy chủ "b33" và trả về báo hiệu nếu router không có thông tin cần thiết, chúng tôi định nghĩa các mã kết quả bổ sung cho Host Reply Message, như sau:

```
2: Lookup password required
   3: Private key required
   4: Lookup password and private key required
   5: Leaseset decryption failure
```
Các giá trị 1-255 đã được định nghĩa là lỗi, vì vậy không có vấn đề tương thích ngược.

### Loại Chữ Ký Mới

Router đến client. Tin nhắn mới.

### Justification

Client không thể biết trước rằng một Hash cụ thể sẽ resolve thành một Meta LS.

Nếu một leaseset lookup cho một Destination trả về một Meta LS, router sẽ thực hiện recursive resolution. Đối với datagrams, phía client không cần biết; tuy nhiên, đối với streaming, nơi mà giao thức kiểm tra destination trong SYN ACK, nó phải biết "destination thực" là gì. Do đó, chúng ta cần một message mới.

### Usage

Router duy trì một bộ nhớ đệm cho destination thực tế được sử dụng từ một meta LS. Khi client gửi một thông điệp đến một destination được phân giải thành một meta LS, router sẽ kiểm tra bộ nhớ đệm cho destination thực tế được sử dụng lần cuối. Nếu bộ nhớ đệm trống, router sẽ chọn một destination từ meta LS và tìm kiếm leaseSet. Nếu việc tìm kiếm leaseSet thành công, router sẽ thêm destination đó vào bộ nhớ đệm và gửi cho client một Meta Redirect Message. Điều này chỉ được thực hiện một lần, trừ khi destination hết hạn và phải được thay đổi. Client cũng phải lưu trữ thông tin này nếu cần thiết. Meta Redirect Message KHÔNG được gửi để trả lời cho mọi SendMessage.

Router chỉ gửi thông báo này đến các client có phiên bản 0.9.47 trở lên.

Client không gửi phản hồi cho thông điệp này.

### Thông Điệp Tra Cứu Cơ Sở Dữ Liệu

Loại thông điệp cho Meta Redirect Message là 43.

### Thay đổi

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
### Database Store Message

Cách thức tạo ra và hỗ trợ Meta, bao gồm giao tiếp và phối hợp giữa các router, nằm ngoài phạm vi của đề xuất này. Xem đề xuất liên quan 150.

### Thay đổi

Chữ ký ngoại tuyến không thể được xác minh trong streaming hoặc repliable datagrams. Xem các phần bên dưới.

## Private Key File Changes Required

Định dạng tệp khóa riêng tư (eepPriv.dat) không phải là một phần chính thức trong thông số kỹ thuật của chúng tôi nhưng nó được ghi chép trong [Java I2P javadocs](http://idk.i2p/javadoc-i2p/net/i2p/data/PrivateKeyFile.html) và các triển khai khác cũng hỗ trợ nó. Điều này cho phép tính di động của các khóa riêng tư sang các triển khai khác nhau.

Cần thực hiện các thay đổi để lưu trữ khóa công khai tạm thời và thông tin ký ngoại tuyến.

### Changes

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
### Tùy chọn I2CP

Thêm hỗ trợ cho các tùy chọn sau:

```
-d days              (specify expiration in days of offline sig, default 365)
      -o offlinedestfile   (generate the online key file,
                            using the offline key file specified)
      -r sigtype           (specify sig type of transient key, default Ed25519)
```
## Streaming Changes Required

Chữ ký offline hiện tại không thể được xác minh trong streaming. Thay đổi dưới đây thêm khối ký offline vào các tùy chọn. Điều này tránh phải truy xuất thông tin này qua I2CP.

### Cấu hình Phiên

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
### Thông điệp Yêu cầu Leaseset

- Thay thế là chỉ cần thêm một cờ (flag), và lấy khóa công khai tạm thời thông qua I2CP
  (Xem các phần Thông điệp Tra cứu Host / Phản hồi Host ở trên)

## Tiêu đề LS2 Chuẩn

Chữ ký offline không thể được xác minh trong quá trình xử lý datagram có thể trả lời. Cần một cờ để chỉ ra đã ký offline nhưng không có chỗ để đặt cờ. Sẽ yêu cầu một số protocol hoàn toàn mới và định dạng mới.

### Thông Điệp Yêu Cầu Variable Leaseset

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
### Tạo Thông Điệp Leaseset2

- Thay thế khác là chỉ cần thêm một flag và truy xuất transient public key thông qua I2CP
  (Xem các phần Host Lookup / Host Reply Message ở trên)
- Có tùy chọn nào khác chúng ta nên thêm vào bây giờ khi đã có flag bytes không?

## SAM V3 Changes Required

SAM cần được nâng cấp để hỗ trợ chữ ký offline trong DESTINATION base 64.

### Lý do chính đáng

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
Lưu ý rằng chữ ký offline chỉ được hỗ trợ cho STREAM và RAW, không hỗ trợ cho DATAGRAM (cho đến khi chúng tôi định nghĩa một giao thức DATAGRAM mới).

Lưu ý rằng SESSION STATUS sẽ trả về Signing Private Key với tất cả các bit không và dữ liệu Offline Signature chính xác như đã cung cấp trong SESSION CREATE.

Lưu ý rằng DEST GENERATE và SESSION CREATE DESTINATION=TRANSIENT không thể được sử dụng để tạo một destination đã ký ngoại tuyến.

### Loại Tin nhắn

Nâng phiên bản lên 3.4, hay để nguyên ở 3.1/3.2/3.3 để có thể thêm vào mà không cần tất cả những thứ của 3.2/3.3?

Các thay đổi khác sẽ được xác định sau. Xem phần I2CP Host Reply Message ở trên.

## BOB Changes Required

BOB sẽ phải được cải tiến để hỗ trợ chữ ký ngoại tuyến và/hoặc Meta LS. Điều này có độ ưu tiên thấp và có thể sẽ không bao giờ được chỉ định hoặc triển khai. SAMv3 là giao diện được ưu tiên.

## Publishing, Migration, Compatibility

LS2 (ngoại trừ LS2 được mã hóa) được xuất bản tại cùng vị trí DHT với LS1. Không có cách nào để xuất bản cả LS1 và LS2, trừ khi LS2 ở một vị trí khác.

LS2 được mã hóa được xuất bản tại hash của loại khóa làm mờ và dữ liệu khóa. Hash này sau đó được sử dụng để tạo ra "routing key" hàng ngày, như trong LS1.

LS2 chỉ được sử dụng khi cần các tính năng mới (mã hóa mới, LS được mã hóa, meta, v.v.). LS2 chỉ có thể được xuất bản lên các floodfill có phiên bản được chỉ định hoặc cao hơn.

Các server xuất bản LS2 sẽ biết rằng bất kỳ client nào kết nối đều hỗ trợ LS2. Chúng có thể gửi LS2 trong garlic.

Clients sẽ chỉ gửi LS2 trong garlics nếu sử dụng mã hóa mới. Shared clients sẽ sử dụng LS1 vô thời hạn? TODO: Làm thế nào để có shared clients hỗ trợ cả mã hóa cũ và mới?

## Rollout

0.9.38 hỗ trợ floodfill cho LS2 tiêu chuẩn, bao gồm offline keys.

0.9.39 chứa hỗ trợ I2CP cho LS2 và Encrypted LS2, ký/xác minh sig type 11, hỗ trợ floodfill cho Encrypted LS2 (sig types 7 và 11, không có offline keys), và mã hóa/giải mã LS2 (không có ủy quyền theo client).

0.9.40 được lên kế hoạch sẽ chứa hỗ trợ cho việc mã hóa/giải mã LS2 với ủy quyền theo từng client, hỗ trợ floodfill và I2CP cho Meta LS2, hỗ trợ cho LS2 được mã hóa với các khóa ngoại tuyến, và hỗ trợ b32 cho LS2 được mã hóa.

## Các loại DatabaseEntry mới

Thiết kế LS2 được mã hóa chịu ảnh hưởng lớn từ [bộ mô tả dịch vụ ẩn v3 của Tor](https://spec.torproject.org/rend-spec-v3), cái mà có các mục tiêu thiết kế tương tự.
