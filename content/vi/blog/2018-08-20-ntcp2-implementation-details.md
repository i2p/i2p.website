---
title: "Chi tiết triển khai NTCP2"
date: 2018-08-20
author: "villain"
description: "Chi tiết triển khai và các đặc tả kỹ thuật của giao thức truyền tải mới của I2P"
categories: ["development"]
---

Các giao thức truyền tải của I2P ban đầu được phát triển cách đây khoảng 15 năm. Khi đó, mục tiêu chính là che giấu dữ liệu được truyền, chứ không phải che giấu việc người ta đang sử dụng chính giao thức đó. Hầu như không ai nghiêm túc nghĩ đến việc bảo vệ trước DPI (deep packets inspection - kiểm tra gói tin sâu) và sự kiểm duyệt các giao thức. Thời thế thay đổi, và dù các giao thức truyền tải ban đầu vẫn mang lại bảo mật mạnh mẽ, đã xuất hiện nhu cầu về một giao thức truyền tải mới. NTCP2 được thiết kế để chống lại các mối đe dọa kiểm duyệt hiện nay, chủ yếu là phân tích độ dài gói tin bằng DPI. Ngoài ra, giao thức mới sử dụng những tiến bộ hiện đại nhất của mật mã học. NTCP2 được xây dựng dựa trên [Noise Protocol Framework](https://noiseprotocol.org/noise.html), với SHA256 làm hàm băm và x25519 cho cơ chế trao đổi khóa Diffie-Hellman (DH) trên đường cong elliptic.

Đặc tả đầy đủ của giao thức NTCP2 có thể được [tìm thấy tại đây](/docs/specs/ntcp2/).

## Mật mã mới

NTCP2 yêu cầu bổ sung các thuật toán mật mã sau vào một triển khai I2P:

- x25519
- HMAC-SHA256
- Chacha20
- Poly1305
- AEAD
- SipHash

So với giao thức ban đầu của chúng tôi, NTCP, NTCP2 sử dụng x25519 thay cho ElGamal cho hàm DH (Diffie–Hellman), AEAD/Chaha20/Poly1305 thay cho AES-256-CBC/Adler32, và dùng SipHash để che giấu thông tin về độ dài của gói tin. Hàm dẫn xuất khóa được dùng trong NTCP2 phức tạp hơn, hiện sử dụng nhiều lần gọi HMAC-SHA256.

*Ghi chú triển khai i2pd (C++): Tất cả các thuật toán đã đề cập ở trên, ngoại trừ SipHash, đều đã được triển khai trong OpenSSL 1.1.0. SipHash sẽ được bổ sung vào bản phát hành OpenSSL 1.1.1 sắp tới. Để tương thích với OpenSSL 1.0.2, vốn được sử dụng trong phần lớn các hệ thống hiện nay, lập trình viên cốt lõi của i2pd [Jeff Becker](https://github.com/majestrate) đã đóng góp các bản triển khai độc lập của các thuật toán mật mã còn thiếu.*

## Các thay đổi trong RouterInfo

NTCP2 yêu cầu có thêm một khóa thứ ba (x25519) bên cạnh hai khóa hiện có (khóa mã hóa và khóa chữ ký). Khóa này được gọi là static key (khóa tĩnh) và phải được thêm vào bất kỳ địa chỉ RouterInfo nào dưới dạng tham số "s". Nó bắt buộc cho cả phía khởi tạo NTCP2 (Alice) và phía đáp ứng (Bob). Nếu có nhiều hơn một địa chỉ hỗ trợ NTCP2, ví dụ, IPv4 và IPv6, thì "s" bắt buộc phải giống nhau cho tất cả chúng. Địa chỉ của Alice được phép chỉ có tham số "s" mà không thiết lập "host" và "port". Ngoài ra, tham số "v" là bắt buộc, hiện luôn được đặt là "2".

Địa chỉ NTCP2 có thể được khai báo như một địa chỉ NTCP2 riêng biệt hoặc như một địa chỉ NTCP kiểu cũ với các tham số bổ sung, khi đó nó sẽ chấp nhận cả kết nối NTCP và NTCP2. Triển khai Java I2P sử dụng cách tiếp cận thứ hai, i2pd (triển khai C++) sử dụng cách thứ nhất.

Nếu một nút chấp nhận các kết nối NTCP2, nó phải công bố RouterInfo (thông tin của router) của mình bao gồm tham số "i", tham số này được dùng làm vector khởi tạo (IV) cho khóa công khai dùng để mã hóa khi nút đó thiết lập các kết nối mới.

## Thiết lập kết nối

To establish a connection both sides need to generate pairs of ephemeral x25519 keys. Based on those keys and "static" keys they derive a set of keys for data transferring. Both parties must verify that the other side actually has a private key for that static key, and that static key is the same as in RouterInfo.

Ba thông điệp đang được gửi để thiết lập một kết nối:

```
Alice                           Bob

SessionRequest ------------------->
<------------------- SessionCreated
SessionConfirmed ----------------->
```
Một khóa x25519 chung, gọi là «input key material» (vật liệu khóa đầu vào), được tính toán cho mỗi thông điệp; sau đó khóa mã hóa thông điệp được tạo ra bằng hàm MixKey. Một giá trị ck (chaining key - khóa chuỗi) được giữ trong suốt quá trình trao đổi thông điệp. Giá trị đó được dùng như đầu vào cuối cùng khi tạo khóa cho việc truyền dữ liệu.

Hàm MixKey trông đại khái như sau trong triển khai C++ của I2P:

```cpp
void NTCP2Establisher::MixKey (const uint8_t * inputKeyMaterial, uint8_t * derived)
{
    // temp_key = HMAC-SHA256(ck, input_key_material)
    uint8_t tempKey[32]; unsigned int len;
    HMAC(EVP_sha256(), m_CK, 32, inputKeyMaterial, 32, tempKey, &len);
    // ck = HMAC-SHA256(temp_key, byte(0x01))
    static uint8_t one[1] =  { 1 };
    HMAC(EVP_sha256(), tempKey, 32, one, 1, m_CK, &len);
    // derived = HMAC-SHA256(temp_key, ck || byte(0x02))
    m_CK[32] = 2;
    HMAC(EVP_sha256(), tempKey, 32, m_CK, 33, derived, &len);
}
```
Thông điệp **SessionRequest** bao gồm một khóa x25519 công khai của Alice (32 byte), một khối dữ liệu được mã hóa bằng AEAD/Chacha20/Poly1305 (16 byte), một giá trị băm (16 byte) và một ít dữ liệu ngẫu nhiên ở cuối (padding). Độ dài phần padding được xác định trong khối dữ liệu đã mã hóa. Khối đã mã hóa cũng chứa độ dài của phần thứ hai của thông điệp **SessionConfirmed**. Một khối dữ liệu được mã hóa và ký bằng một khóa được dẫn xuất từ khóa tạm thời (ephemeral) của Alice và khóa tĩnh (static) của Bob. Giá trị ck ban đầu cho hàm MixKey được đặt thành SHA256 (Noise_XKaesobfse+hs2+hs3_25519_ChaChaPoly_SHA256).

Vì khóa công khai x25519 dài 32 byte có thể bị DPI phát hiện, nên nó được mã hóa bằng thuật toán AES-256-CBC, sử dụng giá trị băm của địa chỉ của Bob làm khóa và tham số "i" từ RouterInfo làm vector khởi tạo (IV).

Thông điệp **SessionCreated** có cấu trúc giống như **SessionRequest**, ngoại trừ khóa được tính dựa trên các khóa tạm thời của cả hai phía. IV (vector khởi tạo) được tạo sau khi mã hóa/giải mã khóa công khai từ thông điệp **SessionRequest** được dùng làm IV để mã hóa/giải mã khóa công khai tạm thời.

Thông điệp **SessionConfirmed** có 2 phần: khóa công khai tĩnh và RouterInfo của Alice (thông tin Router). Điểm khác biệt so với các thông điệp trước là khóa công khai tạm thời được mã hóa bằng AEAD/Chaha20/Poly1305 sử dụng cùng khóa như **SessionCreated**. Điều này làm tăng kích thước phần đầu của thông điệp từ 32 lên 48 byte. Phần thứ hai cũng được mã hóa bằng AEAD/Chaha20/Poly1305, nhưng dùng một khóa mới, được tính toán từ khóa tạm thời của Bob và khóa tĩnh của Alice. Phần RouterInfo cũng có thể được nối thêm phần đệm dữ liệu ngẫu nhiên, nhưng không bắt buộc, vì RouterInfo thường có độ dài khác nhau.

## Sinh các khóa truyền dữ liệu

Nếu mọi phép băm và xác minh khóa đều thành công, phải có một giá trị ck chung sau thao tác MixKey cuối cùng ở cả hai phía. Giá trị này được dùng để tạo hai bộ khóa <k, sipk, sipiv> cho mỗi phía của một kết nối. "k" là khóa AEAD/Chaha20/Poly1305, "sipk" là khóa SipHash, "sipiv" là giá trị khởi tạo cho SipHash IV, được thay đổi sau mỗi lần sử dụng.

Mã dùng để sinh khóa trông như thế này trong triển khai I2P bằng C++:

```cpp
void NTCP2Session::KeyDerivationFunctionDataPhase ()
{
    uint8_t tempKey[32]; unsigned int len;
    // temp_key = HMAC-SHA256(ck, zerolen)
    HMAC(EVP_sha256(), m_Establisher->GetCK (), 32, nullptr, 0, tempKey, &len);
    static uint8_t one[1] =  { 1 };
    // k_ab = HMAC-SHA256(temp_key, byte(0x01)).
    HMAC(EVP_sha256(), tempKey, 32, one, 1, m_Kab, &len);
    m_Kab[32] = 2;
    // k_ba = HMAC-SHA256(temp_key, k_ab || byte(0x02))
    HMAC(EVP_sha256(), tempKey, 32, m_Kab, 33, m_Kba, &len);
    static uint8_t ask[4] = { 'a', 's', 'k', 1 }, master[32];
    // ask_master = HMAC-SHA256(temp_key, "ask" || byte(0x01))
    HMAC(EVP_sha256(), tempKey, 32, ask, 4, master, &len);
    uint8_t h[39];
    memcpy (h, m_Establisher->GetH (), 32);
    memcpy (h + 32, "siphash", 7);
    // temp_key = HMAC-SHA256(ask_master, h || "siphash")
    HMAC(EVP_sha256(), master, 32, h, 39, tempKey, &len);
    // sip_master = HMAC-SHA256(temp_key, byte(0x01))
    HMAC(EVP_sha256(), tempKey, 32, one, 1, master, &len);
    // temp_key = HMAC-SHA256(sip_master, zerolen)
    HMAC(EVP_sha256(), master, 32, nullptr, 0, tempKey, &len);
   // sipkeys_ab = HMAC-SHA256(temp_key, byte(0x01)).
    HMAC(EVP_sha256(), tempKey, 32, one, 1, m_Sipkeysab, &len);
    m_Sipkeysab[32] = 2;
     // sipkeys_ba = HMAC-SHA256(temp_key, sipkeys_ab || byte(0x02))
    HMAC(EVP_sha256(), tempKey, 32, m_Sipkeysab, 33, m_Sipkeysba, &len);
}
```
*i2pd (C++) ghi chú triển khai: 16 byte đầu của mảng "sipkeys" là một khóa SipHash, 8 byte cuối là IV (vector khởi tạo). SipHash yêu cầu hai khóa 8 byte, nhưng i2pd xử lý chúng như một khóa 16 byte duy nhất.*

## Truyền dữ liệu

Dữ liệu được truyền dưới dạng các khung, mỗi khung có 3 phần:

- 2 bytes of frame length obfuscated with SipHash
- data encrypted with Chacha20
- 16 bytes of Poly1305 hash value

Độ dài tối đa của dữ liệu được truyền trong một khung là 65519 byte.

Độ dài thông điệp được làm mờ bằng cách áp dụng phép XOR với hai byte đầu tiên của SipHash IV (vector khởi tạo) hiện tại.

Phần dữ liệu đã mã hóa chứa các khối dữ liệu. Mỗi khối được thêm phần đầu dài 3 byte ở phía trước, phần này xác định kiểu khối và độ dài khối. Thông thường, các khối kiểu I2NP được truyền; đó là các thông điệp I2NP với phần đầu đã được thay đổi. Một khung NTCP2 có thể truyền nhiều khối I2NP.

Loại khối dữ liệu quan trọng còn lại là khối dữ liệu ngẫu nhiên. Khuyến nghị thêm một khối dữ liệu ngẫu nhiên vào mỗi khung NTCP2. Chỉ được thêm một khối dữ liệu ngẫu nhiên và nó phải là khối cuối cùng.

Đó là các khối dữ liệu khác được sử dụng trong triển khai NTCP2 hiện tại:

- **RouterInfo** — usually contains Bob's RouterInfo after the connection has been established, but it can also contain RouterInfo of a random node for the purpose of speeding up floodfills (there is a flags field for that case).
- **Termination** — is used when a host explicitly terminates a connection and specifies a reason for that.
- **DateTime** — a current time in seconds.

## Tóm tắt

Giao thức truyền tải I2P NTCP2 mới cung cấp khả năng kháng kiểm duyệt DPI (kiểm tra gói tin sâu) hiệu quả. Nó cũng giúp giảm tải CPU nhờ sử dụng mật mã hiện đại, nhanh hơn. Điều này giúp I2P dễ chạy hơn trên các thiết bị cấu hình thấp, chẳng hạn như điện thoại thông minh và router gia đình. Cả hai bản triển khai I2P chính đều hỗ trợ đầy đủ NTCP2 và cung cấp NTCP2 để sử dụng kể từ phiên bản 0.9.36 (Java) và 2.20 (i2pd, C++).
