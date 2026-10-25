---
title: "Các Giao thức Mã hóa Hậu Lượng tử"
number: "169"
author: "zzz, orignal, drzed, eyedeekay"
created: "2025-01-21"
lastupdated: "2026-04-09"
status: "Mở"
thread: "http://zzz.i2p/topics/3294"
target: "0.9.70"
toc: true
---

### Trạng thái

| Giao thức / Tính năng | Trạng thái |
|--------------------|--------|
| Ratchet | Đã hoàn thiện trong Java I2P và i2pd |
| NTCP2 | Bản beta Quý 1 năm 2026 |
| SSU2 | Bắt đầu triển khai sớm, bản beta Quý 23 năm 2026 |
| MLDSA SigTypes | Ưu tiên thấp, có thể vào năm 2027 trở đi |
## Tổng quan

Trong khi nghiên cứu và cạnh tranh để tìm ra mật mã hậu lượng tử (PQ) phù hợp đã diễn ra trong một thập kỷ, các lựa chọn vẫn chưa rõ ràng cho đến gần đây.

Chúng tôi đã bắt đầu xem xét các hệ quả của mật mã PQ vào năm 2022 [zzz.i2p](http://zzz.i2p/topics/3294).

Các tiêu chuẩn TLS đã bổ sung hỗ trợ mã hóa lai trong hai năm qua và hiện nay nó đang được sử dụng cho một phần đáng kể lưu lượng được mã hóa trên internet nhờ vào sự hỗ trợ từ Chrome và Firefox [Cloudflare](https://blog.cloudflare.com/pq-2024/).

Gần đây, NIST đã hoàn tất và công bố các thuật toán được khuyến nghị cho mật mã hậu lượng tử [NIST](https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards). Hiện tại, một số thư viện mật mã phổ biến đã hỗ trợ các tiêu chuẩn của NIST hoặc sẽ triển khai hỗ trợ trong tương lai gần.

Cả [Cloudflare](https://blog.cloudflare.com/pq-2024/) và [NIST](https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards) đều khuyến nghị việc chuyển đổi nên bắt đầu ngay lập tức. Xem thêm FAQ về mật mã hậu lượng tử năm 2022 của NSA [NSA](https://media.defense.gov/2022/Sep/07/2003071836/-1/-1/0/CSI_CNSA_2.0_FAQ_.PDF). I2P nên đi đầu trong lĩnh vực bảo mật và mật mã học. Bây giờ là thời điểm thích hợp để triển khai các thuật toán được khuyến nghị. Nhờ hệ thống loại mật mã linh hoạt và hệ thống loại chữ ký của chúng ta, chúng ta sẽ thêm các loại mới cho mật mã lai (hybrid crypto), cũng như chữ ký hậu lượng tử và chữ ký lai.

## Mục tiêu

- Chọn các thuật toán chống lại máy tính lượng tử (PQ-resistant)
- Thêm các thuật toán chỉ dùng PQ và thuật toán lai vào các giao thức I2P tại những vị trí phù hợp
- Định nghĩa nhiều biến thể khác nhau
- Lựa chọn các biến thể tốt nhất sau khi triển khai, kiểm thử, phân tích và nghiên cứu
- Thêm hỗ trợ từng bước và đảm bảo tính tương thích ngược

## Các mục tiêu không nhằm đạt được

- Không thay đổi các giao thức mã hóa một chiều (Noise N)
- Không chuyển khỏi SHA256, vì hiện tại chưa bị đe dọa trong ngắn hạn bởi máy tính lượng tử
- Không chọn các biến thể ưu tiên cuối cùng vào thời điểm này

## Mô hình đe dọa

- Các bộ định tuyến ở OBEP hoặc IBGW, có thể thông đồng với nhau,
  lưu trữ các tin nhắn garlic để giải mã sau này (bảo mật tiến tới)
- Những kẻ quan sát mạng
  lưu trữ các tin nhắn truyền tải để giải mã sau này (bảo mật tiến tới)
- Những người tham gia mạng giả mạo chữ ký cho RI, LS, streaming, datagram,
  hoặc các cấu trúc khác

## Các giao thức bị ảnh hưởng

Chúng tôi sẽ sửa đổi các giao thức sau đây, theo thứ tự phát triển một cách tương đối. Việc triển khai tổng thể có thể diễn ra từ cuối năm 2025 đến giữa năm 2027. Xem phần Ưu tiên và Triển khai bên dưới để biết chi tiết.

| Giao thức / Tính năng | Trạng thái |
|--------------------|--------|
| Hybrid MLKEM Ratchet và LS | Đã phê duyệt 2025-06; phiên bản beta 2025-08; phát hành 2025-11 |
| Hybrid MLKEM NTCP2 | Đã thử nghiệm trên mạng thực tế, đã phê duyệt 2026-02; mục tiêu beta 2026-05; mục tiêu phát hành 2026-08 |
| Hybrid MLKEM SSU2 | Đã phê duyệt 2026-02; mục tiêu beta 2026-08; mục tiêu phát hành 2026-11 |
| MLDSA SigTypes 12-14 | Đề xuất đã ổn định nhưng có thể chưa được hoàn tất trước năm 2027 |
| MLDSA Dests | Đã thử nghiệm trên mạng thực tế, yêu cầu nâng cấp mạng để hỗ trợ floodfill |
| Hybrid SigTypes 15-17 | Sơ bộ |
| Hybrid Dests | |
## Thiết kế

Chúng tôi sẽ hỗ trợ các tiêu chuẩn NIST FIPS 203 và 204 [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf) [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf), những tiêu chuẩn này dựa trên, nhưng KHÔNG tương thích với, CRYSTALS-Kyber và CRYSTALS-Dilithium (các phiên bản 3.1, 3 và cũ hơn).

### Trao đổi khóa

Chúng tôi sẽ hỗ trợ trao đổi khóa lai trong các giao thức sau:

| Proto   | Noise Type | Hỗ trợ chỉ PQ? | Hỗ trợ Hybrid? |
|---------|------------|----------------|-----------------|
| NTCP2   | XK         | không          | có              |
| SSU2    | XK         | không          | có              |
| Ratchet | IK         | không          | có              |
| TBM     | N          | không          | không           |
| NetDB   | N          | không          | không           |
PQ KEM chỉ cung cấp các khóa tạm thời, và không hỗ trợ trực tiếp các lần bắt tay khóa tĩnh như Noise XK và IK.

Noise N không sử dụng trao đổi khóa hai chiều và do đó không phù hợp với mã hóa lai.

Do đó, chúng tôi sẽ chỉ hỗ trợ mã hóa lai (hybrid encryption) cho NTCP2, SSU2 và Ratchet. Chúng tôi sẽ định nghĩa ba biến thể ML-KEM như trong [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf), tạo tổng cộng 3 loại mã hóa mới. Các loại mã hóa lai sẽ chỉ được định nghĩa khi kết hợp với X25519.

Các loại mã hóa mới là:

| Loại | Mã |
|------|------|
| MLKEM512_X25519 | 5 |
| MLKEM768_X25519 | 6 |
| MLKEM1024_X25519 | 7 |
Chi phí phát sinh sẽ rất lớn. Kích thước thông điệp điển hình 1 và 2 (đối với XK và IK) hiện đang vào khoảng 100 byte (trước khi thêm bất kỳ dữ liệu tải nào). Kích thước này sẽ tăng lên từ 8 đến 15 lần tùy theo thuật toán.

### Chữ ký

Chúng tôi sẽ hỗ trợ chữ ký PQ và chữ ký lai trong các cấu trúc sau:

Do đó, chúng tôi sẽ hỗ trợ cả chữ ký chỉ dùng mật mã hậu lượng tử (PQ-only) và chữ ký lai (hybrid). Chúng tôi sẽ định nghĩa ba biến thể ML-DSA như trong [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf), ba biến thể lai kết hợp với Ed25519, và ba biến thể chỉ dùng mật mã hậu lượng tử với bước băm trước (prehash) dành riêng cho tệp SU3, tổng cộng tạo ra 9 loại chữ ký mới. Các loại chữ ký lai chỉ được định nghĩa khi kết hợp với Ed25519. Chúng tôi sẽ sử dụng ML-DSA tiêu chuẩn, KHÔNG dùng các biến thể có băm trước (HashML-DSA), ngoại trừ đối với các tệp SU3.

| Loại | Chỉ hỗ trợ PQ? | Hỗ trợ kết hợp? |
|------|------------------|-----------------|
| RouterInfo | yes | yes |
| LeaseSet | yes | yes |
| Streaming SYN/SYNACK/Close | yes | yes |
| Repliable Datagrams | yes | yes |
| Datagram2 (prop. 163) | yes | yes |
| I2CP create session msg | yes | yes |
| SU3 files | yes | yes |
| X.509 certificates | yes | yes |
| Java keystores | yes | yes |
Chúng tôi sẽ sử dụng biến thể ký "hedged" hoặc ngẫu nhiên hóa, chứ không phải biến thể "deterministic", như được định nghĩa trong mục 3.4 của [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf). Điều này đảm bảo rằng mỗi chữ ký đều khác nhau, ngay cả khi ký trên cùng một dữ liệu, và cung cấp lớp bảo vệ bổ sung chống lại các cuộc tấn công kênh rò rỉ. Xem phần ghi chú triển khai bên dưới để biết thêm chi tiết về các lựa chọn thuật toán, bao gồm mã hóa và ngữ cảnh.

Các loại chữ ký mới là:

Chứng chỉ X.509 và các định dạng mã hóa DER khác sẽ sử dụng các cấu trúc ghép và OID được định nghĩa trong [bản thảo IETF](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/).

| Loại | Mã |
|------|------|
| MLDSA44 | 12 |
| MLDSA65 | 13 |
| MLDSA87 | 14 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 15 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 16 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 17 |
| MLDSA44ph | 18 |
| MLDSA65ph | 19 |
| MLDSA87ph | 20 |
Chi phí phát sinh sẽ rất lớn. Kích thước điển hình của định danh đích và định danh router Ed25519 là 391 byte. Kích thước này sẽ tăng từ 3,5x đến 6,8x tùy theo thuật toán. Chữ ký Ed25519 là 64 byte. Kích thước này sẽ tăng từ 38x đến 76x tùy theo thuật toán. Các thông điệp RouterInfo có chữ ký, LeaseSet, datagram có thể trả lời và thông điệp streaming có chữ ký điển hình vào khoảng 1KB. Kích thước này sẽ tăng từ 3x đến 8x tùy theo thuật toán.

Do các loại định danh đích và định danh bộ định tuyến mới sẽ không chứa phần đệm, chúng sẽ không thể nén được. Kích thước của các định danh đích và định danh bộ định tuyến được nén gzip trong quá trình truyền sẽ tăng lên từ 12 đến 38 lần tùy thuộc vào thuật toán.

Đối với Destinations, các loại chữ ký mới được hỗ trợ với mọi loại mã hóa trong leaseset. Hãy đặt loại mã hóa trong chứng chỉ khóa về NONE (255).

### Các kết hợp hợp lệ

Đối với RouterIdentities, loại mã hóa ElGamal đã bị ngừng sử dụng. Các loại chữ ký mới chỉ được hỗ trợ với mã hóa X25519 (loại 4). Các loại mã hóa mới sẽ được chỉ ra trong RouterAddresses. Loại mã hóa trong chứng chỉ khóa sẽ tiếp tục là loại 4.

Các vector kiểm thử cho SHA3-256, SHAKE128 và SHAKE256 nằm tại [NIST](https://csrc.nist.gov/projects/cryptographic-standards-and-guidelines/example-values).

### Yêu cầu mã hóa mới

- ML-KEM (trước đây là CRYSTALS-Kyber) [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)
- ML-DSA (trước đây là CRYSTALS-Dilithium) [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf)
- SHA3-128 (trước đây là Keccak-256) [FIPS 202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf) Chỉ dùng cho SHAKE128
- SHA3-256 (trước đây là Keccak-512) [FIPS 202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf)
- SHAKE128 và SHAKE256 (phần mở rộng XOF của SHA3-128 và SHA3-256) [FIPS 202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf)

Lưu ý rằng thư viện Java bouncycastle hỗ trợ tất cả các mục nêu trên. Hỗ trợ thư viện C++ có trong OpenSSL 3.5 [OpenSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/).

Chúng tôi sẽ không hỗ trợ [FIPS 205](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.205.pdf) (Sphincs+), vì nó chậm hơn và lớn hơn nhiều so với ML-DSA. Chúng tôi sẽ không hỗ trợ FIPS206 sắp tới (Falcon), vì nó vẫn chưa được chuẩn hóa. Chúng tôi sẽ không hỗ trợ NTRU hoặc các ứng viên PQ khác chưa được NIST chuẩn hóa.

### Các lựa chọn thay thế

Có một số nghiên cứu [bài báo](https://eprint.iacr.org/2020/379.pdf) về việc thích ứng Wireguard (IK) cho mật mã lượng tử (PQ) thuần túy, nhưng bài báo đó vẫn còn một số câu hỏi chưa được giải quyết. Sau đó, cách tiếp cận này đã được triển khai thành Rosenpass [Rosenpass](https://rosenpass.eu/) [bản thuyết minh](https://raw.githubusercontent.com/rosenpass/rosenpass/papers-pdf/whitepaper.pdf) cho Wireguard PQ.

### Rosenpass

Rosenpass sử dụng một quá trình bắt tay kiểu Noise KK với các khóa tĩnh Classic McEliece 460896 đã chia sẻ trước (500 KB mỗi khóa) và các khóa tạm thời Kyber-512 (về cơ bản là MLKEM-512). Vì văn bản được mã hóa từ Classic McEliece chỉ dài 188 byte, đồng thời khóa công khai và văn bản mã hóa của Kyber-512 ở kích thước hợp lý, nên cả hai thông điệp bắt tay đều vừa với kích thước MTU UDP tiêu chuẩn. Khóa chia sẻ đầu ra (osk) từ quá trình bắt tay PQ KK được dùng làm khóa đã chia sẻ trước (psk) đầu vào cho quá trình bắt tay Wireguard IK tiêu chuẩn. Như vậy, tổng cộng có hai lần bắt tay hoàn chỉnh, một lần hoàn toàn dựa trên mật mã chống lượng tử (PQ), và một lần hoàn toàn dùng X25519.

Chúng ta không thể làm bất kỳ điều gì trong số này để thay thế các lần bắt tay XK và IK vì:

Có rất nhiều thông tin hữu ích trong bản whitepaper, và chúng tôi sẽ xem xét nó để tìm ý tưởng và cảm hứng. TODO.

- Chúng ta không thể thực hiện KK, vì Bob không có khóa tĩnh của Alice
- Khóa tĩnh 500KB là quá lớn
- Chúng ta không muốn thêm một lượt truyền phát nào nữa

Cập nhật các phần và bảng trong tài liệu cấu trúc chung [/docs/specs/common-structures/](/docs/specs/common-structures/) như sau:

## Đặc tả

### Các cấu trúc phổ biến

Các loại Khóa Công khai mới là:

#### Vấn đề

Khóa công khai lai là khóa X25519. Khóa công khai KEM là khóa lượng tử tạm thời được gửi từ Alice đến Bob. Việc mã hóa và thứ tự byte được định nghĩa trong [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf).

| Loại | Độ dài Khóa Công khai | Kể từ | Mục đích sử dụng |
|------|------------------------|-------|-------------|
| MLKEM512_X25519 | 32 | 0.9.xx | Xem đề xuất 169, chỉ dành cho Leasesets, không dùng cho RIs hay Destinations |
| MLKEM768_X25519 | 32 | 0.9.xx | Xem đề xuất 169, chỉ dành cho Leasesets, không dùng cho RIs hay Destinations |
| MLKEM1024_X25519 | 32 | 0.9.xx | Xem đề xuất 169, chỉ dành cho Leasesets, không dùng cho RIs hay Destinations |
| MLKEM512 | 800 | 0.9.xx | Xem đề xuất 169, chỉ dùng cho bắt tay (handshakes), không dùng cho Leasesets, RIs hay Destinations |
| MLKEM768 | 1184 | 0.9.xx | Xem đề xuất 169, chỉ dùng cho bắt tay (handshakes), không dùng cho Leasesets, RIs hay Destinations |
| MLKEM1024 | 1568 | 0.9.xx | Xem đề xuất 169, chỉ dùng cho bắt tay (handshakes), không dùng cho Leasesets, RIs hay Destinations |
| MLKEM512_CT | 768 | 0.9.xx | Xem đề xuất 169, chỉ dùng cho bắt tay (handshakes), không dùng cho Leasesets, RIs hay Destinations |
| MLKEM768_CT | 1088 | 0.9.xx | Xem đề xuất 169, chỉ dùng cho bắt tay (handshakes), không dùng cho Leasesets, RIs hay Destinations |
| MLKEM1024_CT | 1568 | 0.9.xx | Xem đề xuất 169, chỉ dùng cho bắt tay (handshakes), không dùng cho Leasesets, RIs hay Destinations |
| NONE | 0 | 0.9.xx | Xem đề xuất 169, chỉ dành cho các Destination có kiểu chữ ký PQ, không dùng cho RIs hay Leasesets |
Các khóa MLKEM*_CT không thực sự là khóa công khai, mà là "bản mã" được gửi từ Bob đến Alice trong quá trình bắt tay Noise. Chúng được liệt kê ở đây để đầy đủ thông tin.

Các loại Khóa riêng tư mới là:

#### PrivateKey

Khóa riêng biệt hybrid là các khóa X25519. Khóa riêng biệt KEM chỉ dành cho Alice. Việc mã hóa KEM và thứ tự byte được định nghĩa trong [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf).

| Loại | Độ dài Khóa Riêng | Kể từ | Mục đích sử dụng |
|------|---------------------|-------|--------------|
| MLKEM512_X25519 | 32 | 0.9.xx | Xem đề xuất 169, chỉ dùng cho Leasesets, không dùng cho RIs hay Destinations |
| MLKEM768_X25519 | 32 | 0.9.xx | Xem đề xuất 169, chỉ dùng cho Leasesets, không dùng cho RIs hay Destinations |
| MLKEM1024_X25519 | 32 | 0.9.xx | Xem đề xuất 169, chỉ dùng cho Leasesets, không dùng cho RIs hay Destinations |
| MLKEM512 | 1632 | 0.9.xx | Xem đề xuất 169, chỉ dùng cho quá trình bắt tay (handshakes), không dùng cho Leasesets, RIs hay Destinations |
| MLKEM768 | 2400 | 0.9.xx | Xem đề xuất 169, chỉ dùng cho quá trình bắt tay (handshakes), không dùng cho Leasesets, RIs hay Destinations |
| MLKEM1024 | 3168 | 0.9.xx | Xem đề xuất 169, chỉ dùng cho quá trình bắt tay (handshakes), không dùng cho Leasesets, RIs hay Destinations |
Các loại Khóa công khai ký mới là:

#### SigningPublicKey

Khóa công khai ký lai là khóa Ed25519 theo sau bởi khóa PQ, như trong [bản thảo IETF](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/). Việc mã hóa và thứ tự byte được định nghĩa trong [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf).

| Loại | Độ dài (byte) | Kể từ | Cách sử dụng |
|------|----------------|-------|-------------|
| MLDSA44 | 1312 | 0.9.xx | Xem đề xuất 169 |
| MLDSA65 | 1952 | 0.9.xx | Xem đề xuất 169 |
| MLDSA87 | 2592 | 0.9.xx | Xem đề xuất 169 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 1344 | 0.9.xx | Xem đề xuất 169 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 1984 | 0.9.xx | Xem đề xuất 169 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 2624 | 0.9.xx | Xem đề xuất 169 |
| MLDSA44ph | 1344 | 0.9.xx | Chỉ dùng cho tệp SU3, không dùng cho cấu trúc netDb |
| MLDSA65ph | 1984 | 0.9.xx | Chỉ dùng cho tệp SU3, không dùng cho cấu trúc netDb |
| MLDSA87ph | 2624 | 0.9.xx | Chỉ dùng cho tệp SU3, không dùng cho cấu trúc netDb |
Các kiểu Khóa riêng dùng để ký mới là:

#### SigningPrivateKey

Khóa riêng để ký hybrid gồm khóa Ed25519 theo sau là khóa PQ, như trong [bản thảo IETF](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/). Việc mã hóa và thứ tự byte được định nghĩa trong [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf).

| Loại | Độ dài (byte) | Kể từ | Cách sử dụng |
|------|----------------|-------|-------|
| MLDSA44 | 2560 | 0.9.xx | Xem đề xuất 169 |
| MLDSA65 | 4032 | 0.9.xx | Xem đề xuất 169 |
| MLDSA87 | 4896 | 0.9.xx | Xem đề xuất 169 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 2592 | 0.9.xx | Xem đề xuất 169 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 4064 | 0.9.xx | Xem đề xuất 169 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 4928 | 0.9.xx | Xem đề xuất 169 |
| MLDSA44ph | 2592 | 0.9.xx | Chỉ dùng cho tệp SU3, không dùng cho cấu trúc netDb. Xem đề xuất 169 |
| MLDSA65ph | 4064 | 0.9.xx | Chỉ dùng cho tệp SU3, không dùng cho cấu trúc netDb. Xem đề xuất 169 |
| MLDSA87ph | 4928 | 0.9.xx | Chỉ dùng cho tệp SU3, không dùng cho cấu trúc netDb. Xem đề xuất 169 |
Các loại chữ ký mới là:

Chữ ký lai là chữ ký Ed25519 theo sau bởi chữ ký PQ, như trong [bản thảo IETF](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/). Chữ ký lai được xác minh bằng cách xác minh cả hai chữ ký, và thất bại nếu một trong hai xác minh thất bại. Việc mã hóa và thứ tự byte được định nghĩa trong [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf).

#### Chữ ký

Chữ ký lai là chữ ký Ed25519 theo sau bởi chữ ký PQ, như trong [bản thảo IETF](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/). Chữ ký lai được xác minh bằng cách xác minh cả hai chữ ký, và thất bại nếu một trong hai xác minh thất bại. Việc mã hóa và thứ tự byte được định nghĩa trong [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf).

| Loại | Độ dài (byte) | Kể từ | Cách sử dụng |
|------|----------------|-------|------------|
| MLDSA44 | 2420 | 0.9.xx | Xem đề xuất 169 |
| MLDSA65 | 3309 | 0.9.xx | Xem đề xuất 169 |
| MLDSA87 | 4627 | 0.9.xx | Xem đề xuất 169 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 2484 | 0.9.xx | Xem đề xuất 169 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 3373 | 0.9.xx | Xem đề xuất 169 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 4691 | 0.9.xx | Xem đề xuất 169 |
| MLDSA44ph | 2484 | 0.9.xx | Chỉ dùng cho tệp SU3, không dùng cho cấu trúc netDb. Xem đề xuất 169 |
| MLDSA65ph | 3373 | 0.9.xx | Chỉ dùng cho tệp SU3, không dùng cho cấu trúc netDb. Xem đề xuất 169 |
| MLDSA87ph | 4691 | 0.9.xx | Chỉ dùng cho tệp SU3, không dùng cho cấu trúc netDb. Xem đề xuất 169 |
Các loại Khóa công khai mã hóa mới là:

#### Chứng chỉ khóa

Khóa công khai ký lai là khóa Ed25519 theo sau bởi khóa PQ, như trong [bản thảo IETF](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/). Việc mã hóa và thứ tự byte được định nghĩa trong [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf).

| Loại | Mã loại | Độ dài khóa công khai tổng | Kể từ | Mục đích sử dụng |
|------|-----------|-------------------------|-------|-------|
| MLDSA44 | 12 | 1312 | 0.9.xx | Xem đề xuất 169 |
| MLDSA65 | 13 | 1952 | 0.9.xx | Xem đề xuất 169 |
| MLDSA87 | 14 | 2592 | 0.9.xx | Xem đề xuất 169 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 15 | 1344 | 0.9.xx | Xem đề xuất 169 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 16 | 1984 | 0.9.xx | Xem đề xuất 169 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 17 | 2624 | 0.9.xx | Xem đề xuất 169 |
| MLDSA44ph | 18 | n/a | 0.9.xx | Chỉ dùng cho tập tin SU3 |
| MLDSA65ph | 19 | n/a | 0.9.xx | Chỉ dùng cho tập tin SU3 |
| MLDSA87ph | 20 | n/a | 0.9.xx | Chỉ dùng cho tập tin SU3 |
Đối với các đích đến có kiểu chữ ký Hybrid hoặc PQ, hãy sử dụng NONE (kiểu 255) cho kiểu mã hóa, nhưng sẽ không có khóa mã hóa nào, và toàn bộ phần chính 384 byte dành cho khóa ký.

| Loại | Mã loại | Độ dài khóa công khai tổng | Kể từ | Mục đích sử dụng |
|------|-----------|-------------------------|-------|-------|
| MLKEM512_X25519 | 5 | 32 | 0.9.xx | Xem đề xuất 169, chỉ dùng cho Leasesets, không dùng cho RIs hay Destinations |
| MLKEM768_X25519 | 6 | 32 | 0.9.xx | Xem đề xuất 169, chỉ dùng cho Leasesets, không dùng cho RIs hay Destinations |
| MLKEM1024_X25519 | 7 | 32 | 0.9.xx | Xem đề xuất 169, chỉ dùng cho Leasesets, không dùng cho RIs hay Destinations |
| NONE | 255 | 0 | 0.9.xx | Xem đề xuất 169 |
Các loại khóa lai NEVER được đưa vào chứng chỉ khóa; chỉ có trong leasesets.

Không có độ đệm. Tổng chiều dài là 7 cộng với tổng chiều dài khóa. Chiều dài chứng chỉ khóa là 4 cộng với chiều dài khóa dư thừa.

#### Kích thước đích

Dưới đây là độ dài cho các loại Destination mới. Loại mã hóa (Enc type) cho tất cả là NONE (loại 255) và độ dài khóa mã hóa được coi là 0. Toàn bộ phần 384 byte được sử dụng cho phần đầu của khóa công khai dùng để ký. LƯU Ý: Điều này khác với đặc tả cho các loại chữ ký ECDSA_SHA512_P521 và RSA, nơi chúng tôi vẫn duy trì khóa ElGamal 256 byte trong destination mặc dù nó không được sử dụng.

skey[0:383] 5 (932 >> 8) (932 & 0xff) 00 12 00 255 skey[384:1311]

Luồng byte đích ví dụ 1319 byte cho MLDSA44:

Dòng byte định danh bộ định tuyến ví dụ 1351 byte cho MLDSA44:

| Loại | Mã loại | Độ dài khóa công khai tổng | Chính | Thừa | Độ dài đích tổng |
|------|-----------|-------------------------|------|--------|-------------------|
| MLDSA44 | 12 | 1312 | 384 | 928 | 1319 |
| MLDSA65 | 13 | 1952 | 384 | 1568 | 1959 |
| MLDSA87 | 14 | 2592 | 384 | 2208 | 2599 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 15 | 1344 | 384 | 960 | 1351 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 16 | 1984 | 384 | 1600 | 1991 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 17 | 2624 | 384 | 2240 | 2631 |
#### Kích thước RouterIdent

Dưới đây là độ dài cho các loại Destination mới. Loại mã hóa cho tất cả là X25519 (loại 4). Toàn bộ phần 352 byte sau khóa công khai X25519 được sử dụng cho phần đầu tiên của khóa công khai chữ ký. Không có phần đệm. Tổng độ dài là 39 cộng với tổng độ dài khóa. Độ dài chứng chỉ khóa là 4 cộng với độ dài khóa dư thừa.

Các lần bắt tay sử dụng các mẫu bắt tay [Noise Protocol](https://noiseprotocol.org/noise.html).

enckey[0:31] skey[0:351] 5 (960 >> 8) (960 & 0xff) 00 12 00 4 skey[352:1311]

| Loại | Mã loại | Độ dài khóa công khai tổng | Chính | Thừa | Độ dài RouterIdent tổng |
|------|-----------|-------------------------|------|--------|--------------------------|
| MLDSA44 | 12 | 1312 | 352 | 960 | 1351 |
| MLDSA65 | 13 | 1952 | 352 | 1600 | 1991 |
| MLDSA87 | 14 | 2592 | 352 | 2240 | 2631 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 15 | 1344 | 352 | 992 | 1383 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 16 | 1984 | 352 | 1632 | 2023 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 17 | 2624 | 352 | 2272 | 2663 |
### PublicKey

Các sửa đổi sau đây đối với XK và IK cho tính bảo mật chuyển tiếp lai (hfs) được quy định như trong mục 5 của [Noise HFS spec](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf):

Mẫu e1 được định nghĩa như sau, như đã nêu trong mục 4 của [Thông số kỹ thuật Noise HFS](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf):

#### KDF cho split()

```

  M = message
  Prefix = "CompositeAlgorithmSignatures2025" (32 bytes, not null terminated)
  Label = (30 bytes, not null terminated), one of:
          "COMPSIG-MLDSA44-Ed25519-SHA512"
          "COMPSIG-MLDSA65-Ed25519-SHA512"
          "COMPSIG-MLDSA87-Ed25519-SHA512"  // not in [COMPOSITE-SIGS]
  ctx = "" (0 bytes)
  len(ctx) = 0  (1 byte)
  PH(M) = SHA512(M) (64 bytes)


  Compute a hash of the message prepended as follows:

  M' = Prefix || Label || len(ctx) || ctx || PH( M )

  M' length is 127 bytes.

  Sign the prehashed message M':

  signature = MLDSA_SIGN(M') || Ed25519_SIGN(M')

```
#### Các định danh nhiễu

Mẫu ekem1 được định nghĩa như sau, như đã nêu trong mục 4 của [Noise HFS spec](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf):

```

  M' = as above

  signature = MLDSA_VERIFY(M') && Ed25519_VERIFY(M')


```
#### Vấn đề

Phần này áp dụng cho cả hai giao thức IK và XK.

### Các mẫu bắt tay

Lớp bắt tay lai được định nghĩa trong [Noise HFS spec](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf). Thông điệp đầu tiên, từ Alice đến Bob, chứa e1, khóa đóng gói, trước phần tải của thông điệp. Phần này được xử lý như một khóa tĩnh bổ sung; gọi hàm EncryptAndHash() đối với nó (với tư cách là Alice) hoặc DecryptAndHash() (với tư cách là Bob). Sau đó xử lý phần tải của thông điệp như bình thường.

Sử dụng ánh xạ chữ cái như sau:

- e = khóa tạm thời dùng một lần
- s = khóa tĩnh
- p = dữ liệu tin nhắn
- e1 = khóa PQ tạm thời dùng một lần, được gửi từ Alice đến Bob
- ekem1 = văn bản mã KEM, được gửi từ Bob đến Alice

Chúng tôi định nghĩa các hàm sau tương ứng với các thành phần mật mã học được sử dụng như đã nêu trong [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf).

```
XK:                       XKhfs:
  <- s                      <- s
  ...                       ...
  -> e, es, p               -> e, es, e1, p
  <- e, ee, p               <- e, ee, ekem1, p
  -> s, se                  -> s, se
  <- p                      <- p
  p ->                      p ->


  IK:                       IKhfs:
  <- s                      <- s
  ...                       ...
  -> e, es, s, ss, p       -> e, es, e1, s, ss, p
  <- tag, e, ee, se, p     <- tag, e, ee, ekem1, se, p
  <- p                     <- p
  p ->                     p ->

  e1 and ekem1 are encrypted. See pattern definitions below.
  NOTE: e1 and ekem1 are different sizes (unlike X25519)
```
(encap_key, decap_key) = PQ_KEYGEN()

```
For Alice:
  (encap_key, decap_key) = PQ_KEYGEN()

  // EncryptAndHash(encap_key)
  ciphertext = ENCRYPT(k, n, encap_key, ad)
  n++
  MixHash(ciphertext)

  For Bob:

  // DecryptAndHash(ciphertext)
  encap_key = DECRYPT(k, n, ciphertext, ad)
  n++
  MixHash(ciphertext)
```
(ciphertext, kem_shared_key) = ENCAPS(encap_key)

```
For Bob:

  (kem_ciphertext, kem_shared_key) = ENCAPS(encap_key)

  // EncryptAndHash(kem_ciphertext)
  ciphertext = ENCRYPT(k, n, kem_ciphertext, ad)
  MixHash(ciphertext)

  // MixKey
  MixKey(kem_shared_key)


  For Alice:

  // DecryptAndHash(ciphertext)
  kem_ciphertext = DECRYPT(k, n, ciphertext, ad)
  MixHash(ciphertext)

  // MixKey
  kem_shared_key = DECAPS(kem_ciphertext, decap_key)
  MixKey(kem_shared_key)
```
### Noise Handshake KDF

#### Vấn đề

- Chúng ta có nên ngừng gửi dữ liệu ratchet 0-RTT (ngoại trừ LS)?
- Chúng ta có nên chuyển ratchet từ IK sang XK nếu không gửi dữ liệu 0-RTT?

#### Tổng quan

kem_shared_key = DECAPS(ciphertext, decap_key)

Lưu ý rằng cả encap_key và ciphertext đều được mã hóa bên trong các khối ChaCha/Poly trong các thông điệp bắt tay Noise 1 và 2. Chúng sẽ được giải mã như một phần của quá trình bắt tay.

Tin nhắn thứ hai, từ Bob đến Alice, chứa ekem1, văn bản được mã hóa, nằm trước phần tải tin nhắn. Đây được coi là một khóa tĩnh bổ sung; gọi hàm EncryptAndHash() trên nó (với tư cách là Bob) hoặc DecryptAndHash() (với tư cách là Alice). Sau đó, tính toán kem_shared_key và gọi MixKey(kem_shared_key). Tiếp theo, xử lý phần tải tin nhắn như thông thường.

#### Các thao tác ML-KEM được định nghĩa

Đối với XK: Sau mẫu tin nhắn 'es' và trước phần tải, hãy thêm:

HOẶC

    Alice creates the encapsulation and decapsulation keys
    The encapsulation key is sent in message 1.
    encap_key and decap_key sizes vary based on ML-KEM variant.

Đối với IK: Sau mẫu tin nhắn 'es' và trước mẫu tin nhắn 's', hãy thêm:

    Bob calculates the ciphertext and shared key,
    using the ciphertext received in message 1.
    The ciphertext is sent in message 2.
    ciphertext size varies based on ML-KEM variant.
    The kem_shared_key is always 32 bytes.

kem_shared_key = DECAPS(ciphertext, decap_key)

    Alice calculates the shared key,
    using the ciphertext received in message 2.
    The kem_shared_key is always 32 bytes.

Lưu ý rằng cả encap_key và ciphertext đều được mã hóa bên trong các khối ChaCha/Poly trong các thông điệp bắt tay Noise 1 và 2. Chúng sẽ được giải mã như một phần của quá trình bắt tay.

kem_shared_key được trộn vào khóa liên kết bằng MixHash(). Xem phần bên dưới để biết chi tiết.

#### Alice KDF cho Thông điệp 1

Đối với XK: Sau mẫu tin nhắn 'ee' và trước phần tải, hãy thêm:

HOẶC

Đối với IK: Sau mẫu tin nhắn 'es' và trước mẫu tin nhắn 's', hãy thêm:

```
This is the "e1" message pattern:
  (encap_key, decap_key) = PQ_KEYGEN()

  // EncryptAndHash(encap_key)
  // AEAD parameters
  k = keydata[32:63]
  n = 0
  ad = h
  ciphertext = ENCRYPT(k, n, encap_key, ad)
  n++

  // MixHash(ciphertext)
  h = SHA256(h || ciphertext)


  End of "e1" message pattern.

  NOTE: For the next section (payload for XK or static key for IK),
  the keydata and chain key remain the same,
  and n now equals 1 (instead of 0 for non-hybrid).
```
#### Bob KDF cho Thông điệp 1

Đối với XK: Sau mẫu tin nhắn 'ee' và trước phần tải, hãy thêm:

HOẶC

Đối với IK: Sau mẫu tin nhắn 'es' và trước mẫu tin nhắn 's', hãy thêm:

```
This is the "e1" message pattern:

  // DecryptAndHash(encap_key_section)
  // AEAD parameters
  k = keydata[32:63]
  n = 0
  ad = h
  encap_key = DECRYPT(k, n, encap_key_section, ad)
  n++

  // MixHash(encap_key_section)
  h = SHA256(h || encap_key_section)

  End of "e1" message pattern.

  NOTE: For the next section (payload for XK or static key for IK),
  the keydata and chain key remain the same,
  and n now equals 1 (instead of 0 for non-hybrid).
```
#### Bob KDF cho Thông điệp 2

Cập nhật đặc tả ECIES-Ratchet [/docs/specs/ecies/](/docs/specs/ecies/) như sau:

HOẶC

Đối với IK: Sau mẫu tin nhắn 'ee' và trước mẫu tin nhắn 'se', hãy thêm:

```
This is the "ekem1" message pattern:

  (kem_ciphertext, kem_shared_key) = ENCAPS(encap_key)

  // EncryptAndHash(kem_ciphertext)
  // AEAD parameters
  k = keydata[32:63]
  n = 0
  ad = h
  ciphertext = ENCRYPT(k, n, kem_ciphertext, ad)

  // MixHash(ciphertext)
  h = SHA256(h || ciphertext)

  // MixKey(kem_shared_key)
  keydata = HKDF(chainKey, kem_shared_key, "", 64)
  chainKey = keydata[0:31]

  End of "ekem1" message pattern.

  // AEAD parameters for payload section
  ... as in standard SSU2 ...
  k = keydata[32:63]
  ...

```
#### Alice KDF cho Thông điệp 2

Sau mẫu tin nhắn 'ee' (và trước mẫu tin nhắn 'ss' cho IK), hãy thêm:

```
This is the "ekem1" message pattern:

  // DecryptAndHash(kem_ciphertext_section)
  // AEAD parameters
  k = keydata[32:63]
  n = 0
  ad = h
  kem_ciphertext = DECRYPT(k, n, kem_ciphertext_section, ad)

  // MixHash(kem_ciphertext_section)
  h = SHA256(h || kem_ciphertext_section)

  // MixKey(kem_shared_key)
  kem_shared_key = DECAPS(kem_ciphertext, decap_key)
  keydata = HKDF(chainKey, kem_shared_key, "", 64)
  chainKey = keydata[0:31]

  End of "ekem1" message pattern.

  // AEAD parameters for payload section
  ... as in standard SSU2 ...
  k = keydata[32:63]
  ...

```
#### KDF cho Tin nhắn 3

unchanged

#### KDF cho split()

unchanged

### Ratchet

Thay đổi: Ratchet hiện tại có phần tải rỗng cho phần ChaCha đầu tiên, và phần tải nằm ở phần thứ hai. Với ML-KEM, giờ đây có ba phần. Phần đầu tiên chứa văn bản mã hóa PQ đã được mã hóa. Phần thứ hai có phần tải rỗng. Phần thứ ba chứa phần tải.

#### Các định danh nhiễu

- "Noise_IKhfselg2_25519+MLKEM512_ChaChaPoly_SHA256"
- "Noise_IKhfselg2_25519+MLKEM768_ChaChaPoly_SHA256"
- "Noise_IKhfselg2_25519+MLKEM1024_ChaChaPoly_SHA256"

#### 1b) Định dạng phiên mới (có ràng buộc)

Thay đổi: Ratchet hiện tại chứa khóa tĩnh trong phần ChaCha đầu tiên, và tải trọng trong phần thứ hai. Với ML-KEM, giờ đây có ba phần. Phần đầu tiên chứa khóa công khai PQ đã được mã hóa. Phần thứ hai chứa khóa tĩnh. Phần thứ ba chứa tải trọng.

Định dạng được mã hóa:

```
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   New Session Ephemeral Public Key    |
  +             32 bytes                  +
  |     Encoded with Elligator2           |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +           ML-KEM encap_key            +
  |       ChaCha20 encrypted data         |
  +      (see table below for length)     +
  |                                       |
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +    (MAC) for encap_key Section        +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +           X25519 Static Key           +
  |       ChaCha20 encrypted data         |
  +             32 bytes                  +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +    (MAC) for Static Key Section       +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +            Payload Section            +
  |       ChaCha20 encrypted data         |
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +         (MAC) for Payload Section     +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+
```
Định dạng đã giải mã:

```
Payload Part 1:

  +----+----+----+----+----+----+----+----+
  |                                       |
  +       ML-KEM encap_key                +
  |                                       |
  +      (see table below for length)     +
  |                                       |
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+

  Payload Part 2:

  +----+----+----+----+----+----+----+----+
  |                                       |
  +       X25519 Static Key               +
  |                                       |
  +      (32 bytes)                       +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+

  Payload Part 3:

  +----+----+----+----+----+----+----+----+
  |                                       |
  +            Payload Section            +
  |                                       |
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
```
Kích thước:

| Loại | Mã loại | Độ dài X | Độ dài Thông điệp 1 | Độ dài Thông điệp 1 đã mã hóa | Độ dài Thông điệp 1 đã giải mã | Độ dài khóa PQ | Độ dài pl |
|------|---------|--------|-------------------|------------------------|------------------------|-------------|--------|
| X25519 | 4 | 32 | 96+pl | 64+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 912+pl | 880+pl | 800+pl | 800 | pl |
| MLKEM768_X25519 | 6 | 32 | 1296+pl | 1360+pl | 1184+pl | 1184 | pl |
| MLKEM1024_X25519 | 7 | 32 | 1680+pl | 1648+pl | 1568+pl | 1568 | pl |
Lưu ý rằng phần tải phải chứa một khối DateTime, do đó kích thước tải tối thiểu là 7. Các kích thước tin nhắn 1 tối thiểu có thể được tính toán tương ứng.

#### 1g) Định dạng phản hồi phiên mới

Thay đổi: NTCP2 hiện tại chỉ chứa các tùy chọn trong một phần ChaCha duy nhất. Với ML-KEM, sẽ có một phần ChaCha mới trước các tùy chọn, chứa khóa công khai PQ đã được mã hóa.

Định dạng được mã hóa:

```
  +----+----+----+----+----+----+----+----+
  |       Session Tag   8 bytes           |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Ephemeral Public Key           +
  |                                       |
  +            32 bytes                   +
  |     Encoded with Elligator2           |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  | ChaCha20 encrypted ML-KEM ciphertext  |
  +      (see table below for length)     +
  ~                                       ~
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +  (MAC) for ciphertext Section         +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +  (MAC) for key Section (no data)      +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +            Payload Section            +
  |       ChaCha20 encrypted data         |
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +         (MAC) for Payload Section     +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+
```
Định dạng đã giải mã:

```
Payload Part 1:


  +----+----+----+----+----+----+----+----+
  |                                       |
  +       ML-KEM ciphertext               +
  |                                       |
  +      (see table below for length)     +
  |                                       |
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+

  Payload Part 2:

  empty

  Payload Part 3:

  +----+----+----+----+----+----+----+----+
  |                                       |
  +            Payload Section            +
  |                                       |
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
```
Kích thước:

| Loại | Mã loại | Độ dài Y | Độ dài Msg 2 | Độ dài Msg 2 mã hóa | Độ dài Msg 2 giải mã | Độ dài CT PQ | Độ dài tùy chọn |
|------|---------|--------|-------------|------------------|------------------|-------------|--------------|
| X25519 | 4 | 32 | 72+pl | 32+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 856+pl | 816+pl | 768+pl | 768 | pl |
| MLKEM768_X25519 | 6 | 32 | 1176+pl | 1136+pl | 1088+pl | 1088 | pl |
| MLKEM1024_X25519 | 7 | 32 | 1656+pl | 1616+pl | 1568+pl | 1568 | pl |
Lưu ý rằng mặc dù thông thường thông điệp 2 sẽ có phần tải (payload) khác không, nhưng đặc tả ratchet [/docs/specs/ecies/](/docs/specs/ecies/) không yêu cầu điều này, do đó kích thước phần tải tối thiểu là 0. Kích thước tối thiểu của thông điệp 2 có thể được tính toán tương ứng.

### NTCP2

Cập nhật đặc tả NTCP2 [/docs/specs/ntcp2/](/docs/specs/ntcp2/) như sau:

#### Các định danh nhiễu

- "Noise_XKhfsaesobfse+hs2+hs3_25519+MLKEM512_ChaChaPoly_SHA256"
- "Noise_XKhfsaesobfse+hs2+hs3_25519+MLKEM768_ChaChaPoly_SHA256"
- "Noise_XKhfsaesobfse+hs2+hs3_25519+MLKEM1024_ChaChaPoly_SHA256"

#### 1) Yêu cầu phiên

Nội dung gốc:

Để hỗ trợ cả NTCP2 PQ và không PQ trên cùng một địa chỉ và cổng router, chúng tôi sử dụng bit có trọng số cao nhất của giá trị X (khóa công khai tạm thời X25519) để đánh dấu rằng đây là một kết nối PQ. Bit này luôn được bỏ thiết lập đối với các kết nối không PQ.

Lưu ý: trường phiên bản trong khối tùy chọn tin nhắn 1 phải được đặt thành 2, ngay cả đối với các kết nối PQ.

Đối với Bob, sau khi giải mã hóa AES của X, kiểm tra X[31] & 0x80. Nếu bit được thiết lập, hãy xóa nó bằng X[31] &= 0x7f, và giải mã qua Noise như một kết nối PQ. Nếu bit không được thiết lập, giải mã qua Noise như một kết nối không phải PQ theo cách thông thường.

Đối với PQ NTCP2 được quảng bá trên một địa chỉ và cổng router khác, điều này không cần thiết.

Để biết thêm thông tin, hãy xem phần Địa chỉ đã công bố bên dưới.

Nội dung gốc:

```
  +----+----+----+----+----+----+----+----+
  |        MS bit set to 1 and then       |
  +        obfuscated with RH_B           +
  |       AES-CBC-256 encrypted X         |
  +             (32 bytes)                +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaChaPoly encrypted data (MLKEM)   |
  +      (see table below for length)     +
  |   k defined in KDF for message 1      |
  +   n = 0                               +
  |   see KDF for associated data         |
  ~                                       ~
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   ChaCha20 encrypted data (options)   |
  +         16 bytes                      +
  |   k defined in KDF for message 1      |
  +   n = 1                               +
  |   see KDF for associated data         |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     unencrypted authenticated         |
  ~         padding (optional)            ~
  |     length defined in options block   |
  +----+----+----+----+----+----+----+----+

  Same as current specification except add a second ChaChaPoly frame
```
Dữ liệu chưa được mã hóa (thẻ xác thực Poly1305 không được hiển thị):

```
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |                   X                   |
  +              (32 bytes)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |           ML-KEM encap_key            |
  +      (see table below for length)     +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |               options                 |
  +              (16 bytes)               +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     unencrypted authenticated         |
  +         padding (optional)            +
  |     length defined in options block   |
  ~               .   .   .               ~
  |                                       |
  +----+----+----+----+----+----+----+----+
```
Lưu ý: trường phiên bản trong khối tùy chọn tin nhắn 1 phải được đặt thành 2, ngay cả đối với các kết nối PQ.

Kích thước:

| Loại | Mã loại | Độ dài X | Độ dài Thông điệp 1 | Độ dài Mã hóa Thông điệp 1 | Độ dài Giải mã Thông điệp 1 | Độ dài khóa PQ | Độ dài tùy chọn |
|------|---------|--------|-------------------|-----------------------|-----------------------|-------------|--------------|
| X25519 | 4 | 32 | 64+đệm | 32 | 16 | -- | 16 |
| MLKEM512_X25519 | 5 | 32 | 880+đệm | 848 | 816 | 800 | 16 |
| MLKEM768_X25519 | 6 | 32 | 1264+đệm | 1232 | 1200 | 1184 | 16 |
| MLKEM1024_X25519 | 7 | 32 | 1648+đệm | 1616 | 1584 | 1568 | 16 |
Lưu ý: Mã loại chỉ dùng nội bộ. Các bộ định tuyến sẽ giữ nguyên loại 4, và khả năng hỗ trợ sẽ được chỉ ra trong địa chỉ bộ định tuyến.

#### 2) SessionCreated

Thay đổi: NTCP2 hiện tại chỉ chứa các tùy chọn trong một phần ChaCha duy nhất. Với ML-KEM, sẽ có một phần ChaCha mới trước các tùy chọn, chứa bản mã PQ được mã hóa.

Nội dung gốc:

```
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        obfuscated with RH_B           +
  |       AES-CBC-256 encrypted Y         |
  +              (32 bytes)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaCha20 encrypted data (MLKEM)     |
  -      (see table below for length)     -
  +   k defined in KDF for message 2      +
  |  (before mixKey)                      |
  +  n = 0; see KDF for associated data   +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaCha20 encrypted data (options)   |
  +         16 bytes                      +
  +   k defined in KDF for message 2      +
  |  (after mixKey)                       |
  +  n = 0; see KDF for associated data   +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     unencrypted authenticated         |
  +         padding (optional)            +
  |     length defined in options block   |
  ~               .   .   .               ~
  |                                       |
  +----+----+----+----+----+----+----+----+

  Same as current specification except add a second ChaChaPoly frame
```
Dữ liệu chưa được mã hóa (thẻ xác thực Poly1305 không hiển thị):

```
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |                  Y                    |
  +              (32 bytes)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |           ML-KEM Ciphertext           |
  +      (see table below for length)     +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |               options                 |
  +              (16 bytes)               +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     unencrypted authenticated         |
  +         padding (optional)            +
  |     length defined in options block   |
  ~               .   .   .               ~
  |                                       |
  +----+----+----+----+----+----+----+----+
```
Kích thước:

| Loại | Mã loại | Độ dài Y | Độ dài Msg 2 | Độ dài Msg 2 đã mã hóa | Độ dài Msg 2 đã giải mã | Độ dài CT PQ | Độ dài tùy chọn |
|------|-----------|-------|-----------|---------------|---------------|-----------|---------|
| X25519 | 4 | 32 | 64+đệm | 32 | 16 | -- | 16 |
| MLKEM512_X25519 | 5 | 32 | 848+đệm | 816 | 784 | 768 | 16 |
| MLKEM768_X25519 | 6 | 32 | 1136+đệm | 1104 | 1104 | 1088 | 16 |
| MLKEM1024_X25519 | 7 | 32 | 1616+đệm | 1584 | 1584 | 1568 | 16 |
Lưu ý: Mã loại chỉ dùng nội bộ. Các bộ định tuyến sẽ giữ nguyên loại 4, và khả năng hỗ trợ sẽ được chỉ ra trong địa chỉ bộ định tuyến.

#### 3) SessionConfirmed

Không đổi

#### Hàm suy xuất khóa (KDF) (cho giai đoạn dữ liệu)

Không đổi

#### Địa chỉ đã công bố

Trong mọi trường hợp, hãy sử dụng tên giao thức truyền tải NTCP2 như bình thường.

Sử dụng cùng địa chỉ/cổng như chế độ không PQ, không bị tường lửa. Chỉ hỗ trợ một biến thể PQ. Trong địa chỉ router, công bố v=2 (như thông thường) và tham số mới pq=[3|4|5] để chỉ định MLKEM 512/768/1024. Alice đặt bit MSB của khóa tạm thời (key[31] & 0x80) trong yêu cầu phiên để cho biết đây là kết nối lai (hybrid). Xem phần trên. Các router cũ hơn sẽ bỏ qua tham số pq và kết nối theo chế độ không PQ như thông thường.

Việc sử dụng địa chỉ/cổng khác nhau cho chế độ không dùng mật mã hậu lượng tử (non-PQ), hoặc chỉ dùng mật mã hậu lượng tử (PQ-only), không bị giới hạn bởi tường lửa HIỆN TẠI KHÔNG được hỗ trợ. Tính năng này sẽ không được triển khai cho đến khi NTCP2 không dùng mật mã hậu lượng tử bị vô hiệu hóa, điều này có thể diễn ra vài năm nữa. Khi chế độ không dùng mật mã hậu lượng tử bị tắt, có thể hỗ trợ nhiều biến thể PQ, nhưng chỉ một biến thể trên mỗi địa chỉ. Trong địa chỉ của router, hãy công bố v=[3|4|5] để chỉ định MLKEM 512/768/1024. Alice không thiết lập bit MSB của khóa tạm thời. Các router cũ hơn sẽ kiểm tra tham số v và bỏ qua địa chỉ này vì không hỗ trợ.

Địa chỉ bị tường lửa (không công bố IP): Trong địa chỉ bộ định tuyến, hãy công bố v=2 (như thông thường). Không cần phải công bố tham số pq.

Alice có thể kết nối đến Bob có hỗ trợ PQ bằng biến thể PQ mà Bob công bố, bất kể Alice có quảng bá việc hỗ trợ pq trong thông tin router của cô hay không, hoặc dù cô có quảng bá cùng biến thể đó hay không.

#### Giới hạn độ đệm tối đa

Theo đặc tả hiện tại, thông điệp 1 và 2 được định nghĩa là có lượng dữ liệu đệm "hợp lý", với phạm vi khuyến nghị từ 0-31 byte, và không có giới hạn tối đa nào được nêu rõ.

Cho đến API 0.9.68 (phát hành 2.11.0), Java I2P thực hiện giới hạn tối đa 256 byte độ đệm cho các kết nối không dùng PQ, tuy nhiên điều này trước đây chưa được tài liệu hóa. Kể từ API 0.9.69 (phát hành 2.12.0), Java I2P áp dụng giới hạn độ đệm tối đa giống như đối với MLKEM-512 cho các kết nối không dùng PQ. Xem bảng dưới đây.

Sử dụng kích thước tin nhắn đã xác định làm độ đệm tối đa, nghĩa là, độ đệm tối đa sẽ gấp đôi kích thước tin nhắn đối với các kết nối PQ, như sau:

| Kích thước đệm tối đa của tin nhắn | không-PQ (đến 0.9.68) | không-PQ (từ 0.9.69 trở đi) | MLKEM-512 | MLKEM-768 | MLKEM-1024 |
|---------------------|----------------------|-----------------------|-----------|-----------|------------|
| Yêu cầu phiên  |   256   |   880   |    880   |     1264   |    1648  |
| Phiên đã tạo  |   256   |   848   |    848   |     1136   |    1616  |
### SSU2

Cập nhật đặc tả SSU2 [/docs/specs/ssu2/](/docs/specs/ssu2/) như sau:

#### Các định danh nhiễu

- "Noise_XKhfschaobfse+hs1+hs2+hs3_25519+MLKEM512_ChaChaPoly_SHA256"
- "Noise_XKhfschaobfse+hs1+hs2+hs3_25519+MLKEM768_ChaChaPoly_SHA256"

Lưu ý rằng MLKEM-1024 KHÔNG được hỗ trợ cho SSU2, vì khóa quá lớn để vừa trong một gói tin datagram chuẩn 1500 byte.

#### Tiêu đề dài

Tiêu đề dài gồm 32 byte. Nó được sử dụng trước khi tạo một phiên, cho các yêu cầu Token, SessionRequest, SessionCreated và Retry. Nó cũng được dùng cho các tin nhắn Kiểm thử ngang hàng (Peer Test) và Chọc lỗ (Hole Punch) ngoài phiên.

Trong các tin nhắn tiếp theo, hãy đặt trường ver (phiên bản) trong phần tiêu đề dài thành 3 hoặc 4, để chỉ định MLKEM-512 hoặc MLKEM-768.

- (0) Yêu cầu phiên
- (1) Phiên đã tạo
- (9) Thử lại (lưu ý: Thử lại với Chấm dứt có thể chứa bất kỳ phiên bản 2-4 nào)
- (10) Yêu cầu mã thông báo

Trong tin nhắn sau đây, hãy đặt trường ver (phiên bản) trong tiêu đề dài thành bất kỳ giá trị nào từ 2 đến 4, vì việc chọn phiên bản là do Alice quyết định, không phải Charlie. Việc luôn đặt giá trị này thành 2 là chấp nhận được. Các triển khai nên chấp nhận mọi giá trị từ 2 đến 4.

- (11) Đục lỗ (Hole Punch)

Trong thông điệp dưới đây, hãy đặt trường ver (phiên bản) trong phần tiêu đề dài thành 2, như thông thường, ngay cả khi hỗ trợ MLKEM-512 hoặc MLKEM-768. Các triển khai cũng có thể đặt giá trị thành 3 hoặc 4 nếu đầu kia hỗ trợ, nhưng điều này không bắt buộc. Các triển khai nên chấp nhận bất kỳ giá trị nào từ 2 đến 4.

- (7) Kiểm tra ngang hàng (tin nhắn ngoài phiên 5-7)

Thảo luận: Việc đặt trường phiên bản thành 3 hoặc 4 có thể không bắt buộc đối với tất cả các loại tin nhắn, nhưng việc này hỗ trợ phát hiện lỗi sớm hơn đối với các kết nối hậu lượng tử không được hỗ trợ. Các tin nhắn Yêu cầu Token và Thử lại (loại 9 và 10) nên có phiên bản 3/4 để đảm bảo tính nhất quán. Tin nhắn Kiểm tra ngang hàng (loại 7) nằm ngoài phiên và không thể hiện ý định khởi tạo phiên.

Trước khi mã hóa tiêu đề:

```

  +----+----+----+----+----+----+----+----+
  |      Destination Connection ID        |
  +----+----+----+----+----+----+----+----+
  |   Packet Number   |type| ver| id |flag|
  +----+----+----+----+----+----+----+----+
  |        Source Connection ID           |
  +----+----+----+----+----+----+----+----+
  |                 Token                 |
  +----+----+----+----+----+----+----+----+

  Destination Connection ID :: 8 bytes, unsigned big endian integer

  Packet Number :: 4 bytes, unsigned big endian integer

  type :: The message type = 0, 1, 7, 9, 10, or 11

  ver :: The protocol version = 2, 3, or 4 for non-PQ, MLKEM512, MLKEM768

  id :: 1 byte, the network ID (currently 2, except for test networks)

  flag :: 1 byte, unused, set to 0 for future compatibility

  Source Connection ID :: 8 bytes, unsigned big endian integer

  Token :: 8 bytes, unsigned big endian integer

```
#### Tiêu đề ngắn

unchanged

#### SessionRequest (Loại 0)

Thay đổi: SSU2 hiện tại chỉ chứa dữ liệu khối trong một phần ChaCha duy nhất. Với ML-KEM, sẽ có một phần ChaCha mới trước dữ liệu khối, chứa khóa công khai PQ đã được mã hóa.

Thay đổi KDF để bảo vệ khỏi việc giả mạo: Để giải quyết các vấn đề nêu trong Đề xuất 165 [Prop165]_, nhưng với một giải pháp khác, chúng tôi điều chỉnh KDF cho Yêu cầu Phiên. Việc này chỉ áp dụng cho các phiên PQ. KDF cho các phiên không phải PQ vẫn giữ nguyên.

```

// End of KDF for initial chain key (unchanged)
  // Bob static key
  // MixHash(bpk)
  h = SHA256(h || bpk);

  // Start of KDF for session request
  // NEW for PQ only
  // bhash = Bob router hash (32 bytes)
  // MixHash(bhash)
  h = SHA256(h || bhash);

  // Rest of KDF for session request, unchanged, as in SSU2 spec
  // MixHash(header)
  h = SHA256(h || header)

  ...

```
Nội dung gốc:

```
  +----+----+----+----+----+----+----+----+
  |  Long Header bytes 0-15, ChaCha20     |
  +  encrypted with Bob intro key         +
  |    See Header Encryption KDF          |
  +----+----+----+----+----+----+----+----+
  |  Long Header bytes 16-31, ChaCha20    |
  +  encrypted with Bob intro key n=0     +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +       X, ChaCha20 encrypted           +
  |       with Bob intro key n=0          |
  +              (32 bytes)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   ChaCha20 encrypted data (MLKEM)     |
  +          (length varies)              +
  |  k defined in KDF for Session Request |
  +  n = 0                                +
  |  see KDF for associated data          |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   ChaCha20 encrypted data (payload)   |
  +          (length varies)              +
  |  k defined in KDF for Session Request |
  +  n = 1                                +
  |  see KDF for associated data          |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+


```
Dữ liệu chưa được mã hóa (thẻ xác thực Poly1305 không được hiển thị):

```
  +----+----+----+----+----+----+----+----+
  |      Destination Connection ID        |
  +----+----+----+----+----+----+----+----+
  |   Packet Number   |type| ver| id |flag|
  +----+----+----+----+----+----+----+----+
  |        Source Connection ID           |
  +----+----+----+----+----+----+----+----+
  |                 Token                 |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |                   X                   |
  +              (32 bytes)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |           ML-KEM encap_key            |
  +      (see table below for length)     +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     Noise payload (block data)        |
  +          (length varies)              +
  |     see below for allowed blocks      |
  +----+----+----+----+----+----+----+----+
```
Kích thước, không bao gồm phần đầu IP:

| Loại | Mã loại | Độ dài X | Độ dài Thông điệp 1 | Độ dài Thông điệp 1 đã mã hóa | Độ dài Thông điệp 1 đã giải mã | Độ dài khóa PQ | Độ dài pl |
|------|---------|--------|-------------------|------------------------|------------------------|-------------|--------|
| X25519 | 4 | 32 | 80+pl | 16+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 896+pl | 832+pl | 800+pl | 800 | pl |
| MLKEM768_X25519 | 6 | 32 | 1280+pl | 1216+pl | 1184+pl | 1184 | pl |
| MLKEM1024_X25519 | 7 | n/a | quá lớn | | | | |
Lưu ý: Mã loại chỉ dùng nội bộ. Các bộ định tuyến sẽ giữ nguyên loại 4, và khả năng hỗ trợ sẽ được chỉ ra trong địa chỉ bộ định tuyến.

MTU tối thiểu cho MLKEM768_X25519: 1318 đối với IPv4 và 1338 đối với IPv6. Xem bên dưới.

Kích thước tối đa: Sử dụng MTU của Bob như đã công bố trong RouterInfo của anh ấy, hoặc giá trị mặc định 1500 nếu không có trong RouterInfo. Không sử dụng MLKEM768_X25519 nếu MTU được công bố quá thấp.

#### SessionCreated (Loại 1)

Thay đổi: SSU2 hiện tại chỉ chứa phần tải trong một phần ChaCha duy nhất. Với ML-KEM, sẽ có một phần ChaCha mới trước phần tải, chứa mã hóa văn bản PQ.

Nội dung gốc:

```
  +----+----+----+----+----+----+----+----+
  |  Long Header bytes 0-15, ChaCha20     |
  +  encrypted with Bob intro key and     +
  | derived key, see Header Encryption KDF|
  +----+----+----+----+----+----+----+----+
  |  Long Header bytes 16-31, ChaCha20    |
  +  encrypted with derived key n=0       +
  |  See Header Encryption KDF            |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +       Y, ChaCha20 encrypted           +
  |       with derived key n=0            |
  +              (32 bytes)               +
  |       See Header Encryption KDF       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaCha20 encrypted data (MLKEM)     |
  ~  length varies                        ~
  +  k defined in KDF for Session Created +
  |  (before mixKey)                      |
  +  n = 0; see KDF for associated data   +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaCha20 encrypted data (payload)   |
  ~  length varies                        ~
  +  k defined in KDF for Session Created +
  |  (after mixKey)                       |
  +  n = 0; see KDF for associated data   +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+


```
Dữ liệu chưa được mã hóa (thẻ xác thực Poly1305 không hiển thị):

```
  +----+----+----+----+----+----+----+----+
  |      Destination Connection ID        |
  +----+----+----+----+----+----+----+----+
  |   Packet Number   |type| ver| id |flag|
  +----+----+----+----+----+----+----+----+
  |        Source Connection ID           |
  +----+----+----+----+----+----+----+----+
  |                 Token                 |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |                  Y                    |
  +              (32 bytes)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |           ML-KEM Ciphertext           |
  +      (see table below for length)     +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     Noise payload (block data)        |
  +          (length varies)              +
  |      see below for allowed blocks     |
  +----+----+----+----+----+----+----+----+
```
Kích thước, không bao gồm phần đầu IP:

| Loại | Mã loại | Độ dài Y | Độ dài Msg 2 | Độ dài Msg 2 đã mã hóa | Độ dài Msg 2 đã giải mã | Độ dài PQ CT | Độ dài pl |
|------|---------|--------|------------|------------------|------------------|------------|--------|
| X25519 | 4 | 32 | 80+pl | 16+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 864+pl | 800+pl | 768+pl | 768 | pl |
| MLKEM768_X25519 | 6 | 32 | 1184+pl | 1118+pl | 1088+pl | 1088 | pl |
| MLKEM1024_X25519 | 7 | n/a | quá lớn | | | | |
Lưu ý: Mã loại chỉ dùng nội bộ. Các bộ định tuyến sẽ giữ nguyên loại 4, và khả năng hỗ trợ sẽ được chỉ ra trong địa chỉ bộ định tuyến.

MTU tối thiểu cho MLKEM768_X25519: 1318 đối với IPv4 và 1338 đối với IPv6. Xem bên dưới.

Các khối sau đây chứa các trường phiên bản. Chúng sẽ giữ nguyên phiên bản 2 (để tương thích với Bob không dùng PQ), và sẽ không chuyển sang phiên bản 3/4 cho PQ.

#### SessionConfirmed (Loại 2)

unchanged

#### KDF cho giai đoạn dữ liệu

unchanged

#### Kiểm tra Máy chuyển tiếp và Máy ngang hàng

Sử dụng cùng địa chỉ/cổng như khi không dùng PQ và không bị tường lửa chặn. Hỗ trợ một hoặc cả hai biến thể PQ. Trong địa chỉ bộ định tuyến, công bố v=2 (như thông thường) và tham số mới pq=[3|4|3,4|4,3] để chỉ MLKEM 512/768/cả hai. Các bộ định tuyến có MTU nhỏ hơn giá trị tối thiểu được quy định bên dưới không được phép công bố tham số "pq" chứa "4". Công bố 4,3 để thể hiện ưu tiên MLKEM-768 hoặc 3,4 để thể hiện ưu tiên MLKEM-512. Phiên bản thực tế do bộ khởi tạo quyết định, và ưu tiên có thể không được tuân thủ. Các bộ định tuyến có MTU nhỏ hơn giá trị tối thiểu được quy định bên dưới không được kết nối bằng MLKEM768. Các bộ định tuyến cũ hơn sẽ bỏ qua tham số pq và kết nối theo kiểu không PQ như thông thường.

- Yêu cầu chuyển tiếp
- Phản hồi chuyển tiếp
- Giới thiệu chuyển tiếp
- Kiểm tra ngang hàng

Chữ ký PQ: Các khối Relay, khối Kiểm thử Ngang hàng (Peer Test) và tin nhắn Kiểm thử Ngang hàng đều chứa chữ ký. Tiếc là chữ ký PQ lớn hơn MTU. Hiện tại không có cơ chế nào để phân mảnh các khối hoặc tin nhắn Relay hay Kiểm thử Ngang hàng qua nhiều gói UDP. Giao thức cần được mở rộng để hỗ trợ phân mảnh. Việc này sẽ được thực hiện trong một đề xuất riêng biệt sẽ được công bố sau. Cho đến khi hoàn tất, chức năng Relay và Kiểm thử Ngang hàng sẽ không được hỗ trợ.

#### Địa chỉ đã công bố

Trong mọi trường hợp, hãy sử dụng tên giao thức SSU2 như bình thường. MLKEM-1024 không được hỗ trợ.

Sử dụng cùng địa chỉ/cổng như khi không dùng PQ và không bị tường lửa chặn. Hỗ trợ một hoặc cả hai biến thể PQ. Trong địa chỉ router, công bố v=2 (như thông thường) và tham số mới pq=[3|4|3,4|4,3] để chỉ định MLKEM 512/768/cả hai. Các router có MTU nhỏ hơn giá trị tối thiểu được quy định bên dưới không được phép công bố tham số "pq" chứa "4". Công bố 4,3 để thể hiện ưu tiên dùng MLKEM-768 hoặc 3,4 để thể hiện ưu tiên dùng MLKEM-512. Phiên bản thực tế do bên khởi tạo quyết định, và ưu tiên có thể không được đáp ứng. Các router có MTU nhỏ hơn giá trị tối thiểu được quy định bên dưới không được kết nối bằng MLKEM768. Các router cũ hơn sẽ bỏ qua tham số pq và kết nối theo kiểu không dùng PQ như thông thường.

Việc sử dụng địa chỉ/cổng khác nhau cho chế độ không dùng mã hóa hậu lượng tử (non-PQ), hoặc chỉ dùng mã hóa hậu lượng tử (PQ-only), không bị giới hạn bởi tường lửa HIỆN TẠI KHÔNG được hỗ trợ. Tính năng này sẽ không được triển khai cho đến khi SSU2 không dùng mã hóa hậu lượng tử bị tắt, dự kiến vài năm nữa. Khi chế độ không dùng mã hóa hậu lượng tử bị tắt, một hoặc cả hai biến thể PQ sẽ được hỗ trợ. Trong địa chỉ của bộ định tuyến (router address), hãy công bố v=[3|4|3,4|4,3] để chỉ rõ MLKEM 512/768/cả hai. Các bộ định tuyến cũ hơn sẽ kiểm tra tham số v và bỏ qua địa chỉ này vì không hỗ trợ.

Địa chỉ bị tường lửa (không công bố IP): Trong địa chỉ bộ định tuyến, hãy công bố v=2 (như thông thường). Tham số pq BẮT BUỘC phải được công bố trong các địa chỉ bị tường lửa, để hỗ trợ chuyển tiếp (relay).

Alice có thể kết nối đến Bob có hỗ trợ PQ bằng biến thể PQ mà Bob công bố, bất kể Alice có quảng bá việc hỗ trợ pq trong thông tin router của cô hay không, hoặc dù cô có quảng bá cùng biến thể đó hay không.

#### MTU

Hãy cẩn thận để không vượt quá MTU khi sử dụng MLKEM768. MTU tối thiểu đối với MLKEM768_X25519 là 1318 đối với IPv4 và 1338 đối với IPv6 (giả sử tải trọng tối thiểu là 10 byte với một khối DateTime và một khối Padding hoặc RelayTagRequest). MTU tối thiểu chung cho SSU2 là 1280, do đó không phải tất cả các nút ngang hàng nào cũng có thể sử dụng MLKEM768. Không được đăng tải hoặc sử dụng MLKEM768 nếu MTU thực tế nhỏ hơn giá trị tối thiểu, dù là ở cục bộ hay do nút ngang hàng quảng cáo. Cần lưu ý không bao gồm kích thước độ đệm (padding) khiến tin nhắn 1 hoặc 2 vượt quá MTU cục bộ hoặc từ xa.

### Streaming

CẦN LÀM: Có cách nào hiệu quả hơn để định nghĩa việc ký/xác minh nhằm tránh sao chép chữ ký không?

### Tệp SU3

CẦN LÀM

Mục 8.1 của [bản thảo IETF](https://datatracker.ietf.org/doc/draft-ietf-lamps-dilithium-certificates/) không cho phép sử dụng HashML-DSA trong chứng chỉ X.509 và không cấp OID cho HashML-DSA do những phức tạp trong triển khai và mức độ bảo mật thấp hơn.

Đối với chữ ký chỉ dùng mật mã hậu lượng tử (PQ) cho các tệp SU3, hãy sử dụng các OID được định nghĩa trong [bản thảo IETF](https://datatracker.ietf.org/doc/draft-ietf-lamps-dilithium-certificates/) dành cho các biến thể không dùng tiền băm trong chứng chỉ. Chúng tôi không định nghĩa chữ ký lai cho các tệp SU3, vì điều đó có thể yêu cầu băm tệp hai lần (mặc dù HashML-DSA và X2559 cùng sử dụng hàm băm SHA512). Ngoài ra, việc nối hai khóa và chữ ký trong một chứng chỉ X.509 sẽ hoàn toàn không chuẩn.

Lưu ý rằng chúng tôi không cho phép ký Ed25519 đối với các tệp SU3, và mặc dù chúng tôi đã định nghĩa việc ký Ed25519ph, nhưng chúng tôi chưa bao giờ thống nhất về một OID cho nó, cũng như chưa từng sử dụng nó.

Các loại chữ ký bình thường bị cấm sử dụng cho tệp SU3; hãy dùng các biến thể ph (prehash).

### Thông số khác

Kích thước Destination tối đa mới sẽ là 2599 (3468 ở cơ số 64).

Cập nhật các tài liệu khác cung cấp hướng dẫn về kích thước Destination, bao gồm:

- SAMv3
- Bittorrent
- Hướng dẫn dành cho nhà phát triển
- Đặt tên / sổ địa chỉ / máy chủ nhảy
- Các tài liệu khác

## Phân tích chi phí phát sinh

### Trao đổi khóa

Tăng kích thước (byte):

| Loại | Khóa công khai (Tin nhắn 1) | Văn bản mã hóa (Tin nhắn 2) |
|------|----------------|-------------------|
| MLKEM512_X25519 | +816 | +784 |
| MLKEM768_X25519 | +1200 | +1104 |
| MLKEM1024_X25519 | +1584 | +1584 |
Tốc độ:

Tốc độ như được báo cáo bởi [Cloudflare](https://blog.cloudflare.com/pq-2024/):

| Loại | Tốc độ tương đối |
|------|----------------|
| X25519 DH/tạo khóa | cơ sở |
| MLKEM512 | nhanh hơn 2,25 lần |
| MLKEM768 | nhanh hơn 1,5 lần |
| MLKEM1024 | 1x (giống nhau) |
| XK | 4x DH (tạo khóa + 3 DH) |
| MLKEM512_X25519 | 4x DH + 2x BQ (tạo khóa + mã hóa/giải mã) = 4,9x DH = chậm hơn 22% |
| MLKEM768_X25519 | 4x DH + 2x BQ (tạo khóa + mã hóa/giải mã) = 5,3x DH = chậm hơn 32% |
| MLKEM1024_X25519 | 4x DH + 2x BQ (tạo khóa + mã hóa/giải mã) = 6x DH = chậm hơn 50% |
Kết quả kiểm thử sơ bộ trong Java:

| Loại | DH/đóng gói tương đối | DH/giải gói | tạo khóa |
|------|-------------------|-----------|--------|
| X25519 | cơ sở | cơ sở | cơ sở |
| MLKEM512 | nhanh hơn 29 lần | nhanh hơn 22 lần | nhanh hơn 17 lần |
| MLKEM768 | nhanh hơn 17 lần | nhanh hơn 14 lần | nhanh hơn 9 lần |
| MLKEM1024 | nhanh hơn 12 lần | nhanh hơn 10 lần | nhanh hơn 6 lần |
### Chữ ký

#### Kích cỡ

Kích thước hoặc mức tăng kích thước điển hình cho khóa, chữ ký, RIdent, Dest (kèm Ed25519 để tham khảo) với giả định loại mã hóa X25519 cho RIs. Kích thước bổ sung cho một Router Info, LeaseSet, các datagram có thể trả lời, và từng gói trong hai gói streaming (SYN và SYN ACK) được liệt kê. Các Destination và LeaseSet hiện tại chứa phần đệm lặp lại và có thể nén trong quá trình truyền. Các loại mới không chứa phần đệm và sẽ không thể nén được, dẫn đến mức tăng kích thước cao hơn nhiều khi truyền. Xem phần thiết kế ở trên.

| Loại | Khóa công khai | Chữ ký | Khóa+Chữ ký | RIdent | Dest | RInfo | LS/Streaming/Datagram (mỗi tin nhắn) |
|------|--------|-----|---------|--------|------|-------|----------------------------------|
| EdDSA_SHA512_Ed25519 | 32 | 64 | 96 | 391 | 391 | cơ sở | cơ sở |
| MLDSA44 | 1312 | 2420 | 3732 | 1351 | 1319 | +3316 | +3284 |
| MLDSA65 | 1952 | 3309 | 5261 | 1991 | 1959 | +5668 | +5636 |
| MLDSA87 | 2592 | 4627 | 7219 | 2631 | 2599 | +7072 | +7040 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 1344 | 2484 | 3828 | 1383 | 1351 | +3412 | +3380 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 1984 | 3373 | 5357 | 2023 | 1991 | +5668 | +5636 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 2624 | 4691 | 7315 | 2663 | 2631 | +7488 | +7456 |
#### Tốc độ

Tốc độ như được báo cáo bởi [Cloudflare](https://blog.cloudflare.com/pq-2024/):

| Loại | Tốc độ tương đối | xác minh |
|------|---------------------|--------|
| EdDSA_SHA512_Ed25519 | cơ sở | cơ sở |
| MLDSA44 | chậm hơn 5 lần | nhanh hơn 2 lần |
| MLDSA65 | ??? | ??? |
| MLDSA87 | ??? | ??? |
Kết quả kiểm thử sơ bộ trong Java:

| Loại | Tốc độ tương đối | xác minh | tạo khóa |
|------|-------------------|--------|--------|
| EdDSA_SHA512_Ed25519 | cơ sở | cơ sở | cơ sở |
| MLDSA44 | chậm hơn 4,6 lần | nhanh hơn 1,7 lần | nhanh hơn 2,6 lần |
| MLDSA65 | chậm hơn 8,1 lần | tương đương | nhanh hơn 1,5 lần |
| MLDSA87 | chậm hơn 11,1 lần | chậm hơn 1,5 lần | tương đương |
## Phân tích bảo mật

Các phân loại bảo mật của NIST được tóm tắt trong [bản trình bày của NIST](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf), trang 10. Tiêu chí sơ bộ: Phân loại bảo mật NIST tối thiểu của chúng ta nên là 2 đối với các giao thức lai và 3 đối với giao thức chỉ dùng mật mã chống lượng tử (PQ-only).

| Danh mục | An toàn tương đương |
|----------|--------------|
| 1 | AES128 |
| 2 | SHA256 |
| 3 | AES192 |
| 4 | SHA384 |
| 5 | AES256 |
### Handshakes

Tất cả các giao thức này đều là giao thức lai. Các triển khai nên ưu tiên sử dụng MLKEM768; MLKEM512 không đủ an toàn.

Các hạng mục bảo mật NIST [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf):

| Thuật toán | Danh mục bảo mật |
|-----------|-------------------|
| MLKEM512 | 1 |
| MLKEM768 | 3 |
| MLKEM1024 | 5 |
### Chữ ký

Đề xuất này định nghĩa cả hai loại chữ ký: dạng lai và chỉ dùng chữ ký lượng tử (PQ). Dạng lai MLDSA44 được ưu tiên hơn dạng chỉ dùng PQ là MLDSA65. Kích thước khóa và chữ ký của MLDSA65 và MLDSA87 có lẽ quá lớn đối với chúng ta, ít nhất là lúc ban đầu.

Các hạng mục bảo mật NIST [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf):

| Thuật toán | Danh mục bảo mật |
|-----------|-------------------|
| MLDSA44 | 2 |
| MLKEM67 | 3 |
| MLKEM87 | 5 |
## Loại Tùy chọn

Mặc dù chúng tôi sẽ định nghĩa và triển khai 3 loại mật mã và 9 loại chữ ký, chúng tôi dự định đo hiệu suất trong quá trình phát triển, đồng thời tiếp tục phân tích các ảnh hưởng do kích thước cấu trúc tăng lên. Chúng tôi cũng sẽ tiếp tục nghiên cứu và theo dõi các phát triển trong các dự án và giao thức khác.

Sau quá trình phát triển và kiểm thử, chúng tôi sẽ lựa chọn một loại hình ưa thích hoặc mặc định cho từng trường hợp sử dụng cụ thể. Việc lựa chọn sẽ đòi hỏi phải cân nhắc các yếu tố như băng thông, CPU và mức độ bảo mật ước tính. Không phải tất cả các loại hình đều phù hợp hoặc được cho phép trong mọi trường hợp sử dụng.

Các tùy chọn ban đầu như sau, có thể thay đổi:

Mã hóa: MLKEM768_X25519

Chữ ký: MLDSA44_EdDSA_SHA512_Ed25519

Các hạn chế ban đầu như sau, có thể thay đổi:

Chữ ký: MLDSA87 và biến thể lai có thể quá lớn; MLDSA65 và biến thể lai có thể cũng quá lớn

## Ghi chú triển khai

### Hỗ trợ thư viện

Các thư viện Bouncycastle, BoringSSL và WolfSSL hiện đã hỗ trợ MLKEM và MLDSA. Hỗ trợ OpenSSL sẽ có trong bản phát hành 3.5 vào ngày 8 tháng 4 năm 2025 [OpenSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/).

Thư viện Noise của southernstorm.com được Java I2P điều chỉnh từng có hỗ trợ sơ bộ cho các bắt tay lai, nhưng chúng tôi đã gỡ bỏ do không sử dụng; chúng tôi sẽ phải thêm lại và cập nhật để phù hợp với [đặc tả Noise HFS](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf).

### Các biến thể chữ ký

Chúng tôi sẽ sử dụng biến thể ký "hedged" (theo kiểu phân nhánh) hoặc ngẫu nhiên hóa, chứ không dùng biến thể "deterministic" (xác định), như được định nghĩa trong mục 3.4 của [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf). Điều này đảm bảo rằng mỗi chữ ký đều khác nhau, ngay cả khi ký trên cùng một dữ liệu, và cung cấp thêm lớp bảo vệ chống lại các cuộc tấn công kênh rò rỉ (side-channel attacks). Mặc dù [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) nêu rõ biến thể "hedged" là mặc định, điều này có thể đúng hoặc không đúng trong các thư viện khác nhau. Người triển khai phải đảm bảo rằng biến thể "hedged" được sử dụng khi thực hiện ký.

Chúng tôi sử dụng quy trình ký bình thường (gọi là Pure ML-DSA Signature Generation), quy trình này mã hóa thông điệp bên trong dưới dạng 0x00 || len(ctx) || ctx || message, trong đó ctx là một giá trị tùy chọn có kích thước từ 0x00 đến 0xFF. Chúng tôi không sử dụng bất kỳ ngữ cảnh tùy chọn nào, do đó len(ctx) == 0. Quy trình này được định nghĩa trong [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) tại bước 10 của Thuật toán 2 và bước 5 của Thuật toán 3. Lưu ý rằng một số vector kiểm thử công bố có thể yêu cầu thiết lập chế độ mà thông điệp không được mã hóa.

### Độ tin cậy

Việc tăng kích thước sẽ dẫn đến hiện tượng phân mảnh tunnel nhiều hơn đáng kể khi lưu trữ trong NetDB, các lần bắt tay streaming và các tin nhắn khác. Hãy kiểm tra các thay đổi về hiệu suất và độ tin cậy.

### Kích thước cấu trúc

Tìm và kiểm tra bất kỳ đoạn mã nào giới hạn kích thước byte của router infos và leasesets.

### NetDB

Xem xét và có thể giảm số lượng tối đa LS/RI được lưu trữ trong RAM hoặc trên đĩa, nhằm hạn chế việc gia tăng dung lượng lưu trữ. Nên tăng yêu cầu băng thông tối thiểu cho các nút floodfill?

### Ratchet

#### Tunnel Chia Sẻ

Việc tự động phân loại/phát hiện nhiều giao thức trên cùng một tunnel nên có thể thực hiện được dựa trên việc kiểm tra độ dài của thông điệp 1 (New Session Message). Lấy ví dụ MLKEM512_X25519, độ dài thông điệp 1 lớn hơn 816 byte so với giao thức ratchet hiện tại, và kích thước tối thiểu của thông điệp 1 (chỉ bao gồm payload DateTime) là 919 byte. Hầu hết các kích thước thông điệp 1 với ratchet hiện tại có độ dài payload nhỏ hơn 816 byte, do đó có thể phân loại chúng là ratchet không lai. Các thông điệp lớn thường là POST, tương đối hiếm.

Vì vậy, chiến lược được khuyến nghị là:

- Nếu tin nhắn 1 nhỏ hơn 919 byte, đó là giao thức ratchet hiện tại.
- Nếu tin nhắn 1 lớn hơn hoặc bằng 919 byte, có khả năng là MLKEM512_X25519.
  Hãy thử MLKEM512_X25519 trước, và nếu thất bại, hãy thử giao thức ratchet hiện tại.

Điều này sẽ cho phép chúng ta hỗ trợ hiệu quả giao thức ratchet chuẩn và ratchet lai trên cùng một đích đến, giống như trước đây chúng ta đã hỗ trợ ElGamal và ratchet trên cùng một đích đến. Do đó, chúng ta có thể chuyển đổi sang giao thức lai MLKEM nhanh hơn nhiều so với việc không thể hỗ trợ đa giao thức trên cùng một đích đến, vì chúng ta có thể thêm hỗ trợ MLKEM vào các đích đến hiện có.

Các tổ hợp được hỗ trợ bắt buộc là:

- X25519 + MLKEM512  
- X25519 + MLKEM768  
- X25519 + MLKEM1024

Các tổ hợp sau đây có thể phức tạp và KHÔNG bắt buộc phải được hỗ trợ, nhưng có thể được hỗ trợ tùy theo cách triển khai:

- Hơn một MLKEM
- ElG + một hoặc nhiều MLKEM
- X25519 + một hoặc nhiều MLKEM
- ElG + X25519 + một hoặc nhiều MLKEM

Chúng ta có thể sẽ không cố gắng hỗ trợ nhiều thuật toán MLKEM (ví dụ: MLKEM512_X25519 và MLKEM_768_X25519) trên cùng một đích đến. Hãy chọn chỉ một thuật toán; tuy nhiên, điều này phụ thuộc vào việc chúng ta chọn một biến thể MLKEM ưu tiên để các kênh client HTTP có thể sử dụng. Phụ thuộc vào cách triển khai.

Chúng TA CÓ THỂ cố gắng hỗ trợ ba thuật toán (ví dụ: X25519, MLKEM512_X25519 và MLKEM769_X25519) trên cùng một đích đến. Chiến lược phân loại và thử lại có thể quá phức tạp. Cấu hình và giao diện cấu hình có thể quá phức tạp. Phụ thuộc vào cách triển khai.

Chúng tôi có lẽ sẽ KHÔNG cố gắng hỗ trợ cả thuật toán ElGamal và thuật toán lai trên cùng một đích đến. ElGamal đã lỗi thời, và việc chỉ dùng ElGamal + thuật toán lai (không có X25519) là không hợp lý. Ngoài ra, cả Tin nhắn Phiên Mới ElGamal và Lai đều có kích thước lớn, do đó các chiến lược phân loại thường sẽ phải thử giải mã cả hai, điều này sẽ kém hiệu quả. Tùy thuộc vào cách triển khai.

Các máy khách có thể sử dụng cùng một hoặc các khóa tĩnh X25519 khác nhau cho các giao thức X25519 và giao thức lai trên cùng một tunnel, tùy thuộc vào cách triển khai.

#### Bảo mật chuyển tiếp

Thông số kỹ thuật ECIES cho phép các Tin nhắn Garlic trong phần tải của Tin nhắn Phiên mới, cho phép truyền tải 0-RTT gói dữ liệu streaming ban đầu, thường là một HTTP GET, cùng với leaseset của máy khách. Tuy nhiên, phần tải của Tin nhắn Phiên mới không có tính bảo mật chuyển tiếp (forward secrecy). Vì đề xuất này nhấn mạnh vào việc tăng cường bảo mật chuyển tiếp cho cơ chế ratchet, các triển khai có thể hoặc nên hoãn việc đưa phần tải streaming, hoặc toàn bộ tin nhắn streaming, cho đến Tin nhắn Phiên Hiện tại đầu tiên. Điều này sẽ đánh đổi khả năng truyền tải 0-RTT. Các chiến lược cũng có thể phụ thuộc vào loại lưu lượng hoặc loại tunnel, hoặc ví dụ như giữa GET và POST. Tùy thuộc vào việc triển khai.

#### Kích thước phiên mới

MLKEM, MLDSA hoặc cả hai trên cùng một đích sẽ làm tăng đáng kể kích thước của Tin nhắn Phiên Mới, như đã mô tả ở trên. Điều này có thể làm giảm nghiêm trọng độ tin cậy khi truyền Tin nhắn Phiên Mới qua các tunnel, nơi mà tin nhắn phải được phân mảnh thành nhiều tin nhắn tunnel 1024 byte. Tỷ lệ thành công khi truyền tỷ lệ thuận với số lượng mảnh theo hàm mũ. Các triển khai có thể sử dụng nhiều chiến lược khác nhau để hạn chế kích thước tin nhắn, nhưng sẽ đánh đổi khả năng truyền 0-RTT. Phụ thuộc vào từng triển khai.

### NTCP2

Chúng tôi đặt bit MSB của khóa tạm thời (key[31] & 0x80) trong yêu cầu phiên để chỉ ra rằng đây là một kết nối lai. Điều này cho phép chúng tôi chạy đồng thời cả NTCP tiêu chuẩn và NTCP lai trên cùng một cổng. Chỉ một biến thể lai sẽ được hỗ trợ và công bố trong địa chỉ router. Ví dụ: v=2,3 hoặc v=2,4 hoặc v=2,5.

#### Ẩn giấu

Là Alice, đối với kết nối PQ, trước khi ngụy trang, đặt X[31] |= 0x80. Việc này khiến X trở thành một khóa công khai X25519 không hợp lệ. Sau khi ngụy trang, AES-CBC sẽ làm nó ngẫu nhiên hóa. Bit có nghĩa lớn nhất (MSB) của X sẽ ngẫu nhiên sau khi ngụy trang.

Với tư cách là Bob, kiểm tra xem (X[31] & 0x80) != 0 sau khi giải mã hóa. Nếu đúng, đây là kết nối PQ.

Phiên bản router tối thiểu cần thiết cho NTCP2-PQ là TBD.

Lưu ý: Mã loại chỉ dùng nội bộ. Các bộ định tuyến sẽ giữ nguyên loại 4, và khả năng hỗ trợ sẽ được chỉ ra trong địa chỉ bộ định tuyến.

### SSU2

Chúng tôi sử dụng trường phiên bản trong tiêu đề dài và đặt giá trị là 3 đối với MLKEM512 và 4 đối với MLKEM768. Việc sử dụng v=2,3,4 trong địa chỉ là đủ.

Kiểm tra và xác minh rằng SSU2 có thể xử lý RI được ký bằng MLDSA và phân mảnh qua nhiều gói tin (6-8?).

Lưu ý: Mã loại chỉ dùng nội bộ. Các bộ định tuyến sẽ giữ nguyên loại 4, và khả năng hỗ trợ sẽ được chỉ ra trong địa chỉ bộ định tuyến.

## Tương thích bộ định tuyến

### Tên Giao thức Truyền tải

Trong mọi trường hợp, hãy sử dụng tên giao thức truyền tải NTCP2 và SSU2 như thông thường.

### Các Loại Mã Hóa Router

Chúng ta có một số lựa chọn thay thế cần xem xét:

#### Các bộ định tuyến loại 5/6/7

Không được khuyến nghị. Chỉ sử dụng các giao thức truyền tải mới được liệt kê ở trên phù hợp với loại router. Các router cũ hơn không thể kết nối, tạo đường hầm qua hoặc gửi tin nhắn netDb đến. Việc gỡ lỗi và đảm bảo hỗ trợ có thể mất vài chu kỳ phát hành trước khi được bật theo mặc định. Thời gian triển khai có thể kéo dài thêm một năm hoặc hơn so với các lựa chọn thay thế dưới đây.

#### Bộ định tuyến loại 4

Được khuyến nghị. Vì PQ không ảnh hưởng đến khóa tĩnh X25519 hay các giao thức bắt tay N, chúng ta có thể giữ các router ở loại 4, và chỉ quảng bá các giao thức truyền tải mới. Các router cũ vẫn có thể kết nối, tạo đường hầm qua, hoặc gửi tin nhắn netDb đến.

#### Khuyến nghị

MLKEM-768 được khuyến nghị cho Ratchet, NTCP2 và SSU2, vì cân bằng tốt nhất giữa bảo mật và độ dài khóa.

### Loại Chữ ký Bộ định tuyến

#### Các bộ định tuyến loại 12-17

Các router cũ hơn xác minh RI và do đó không thể kết nối, tạo tunnel qua hoặc gửi tin nhắn netdb đến. Việc gỡ lỗi và đảm bảo hỗ trợ sẽ mất vài chu kỳ phát hành trước khi bật mặc định. Vấn đề sẽ tương tự như khi triển khai mã hóa loại 5/6/7; có thể làm kéo dài việc triển khai thêm một năm hoặc hơn so với phương án triển khai mã hóa loại 4 được liệt kê ở trên.

Không có lựa chọn thay thế.

### Loại mã hóa LS

#### Loại 5-7 Khóa LS

Các khóa này có thể xuất hiện trong LS với các khóa X25519 loại 4 cũ hơn. Các bộ định tuyến cũ hơn sẽ bỏ qua các khóa không xác định.

Các điểm đến có thể hỗ trợ nhiều loại khóa, nhưng chỉ bằng cách thử giải mã tin nhắn 1 với từng khóa. Chi phí phát sinh có thể được giảm bớt bằng cách duy trì số lượng lần giải mã thành công cho mỗi khóa, và thử với khóa được sử dụng nhiều nhất trước tiên. Java I2P sử dụng chiến lược này cho ElGamal+X25519 trên cùng một điểm đến.

### Các loại chữ ký đích

#### Các đích loại 12-17

Các router xác minh chữ ký leaseset và do đó không thể kết nối hoặc nhận leaseset cho các đích loại 12-17. Việc gỡ lỗi và đảm bảo hỗ trợ trước khi bật mặc định sẽ mất vài chu kỳ phát hành.

Không có lựa chọn thay thế.

## Ưu tiên và Triển khai

Dữ liệu quý giá nhất là lưu lượng truyền cuối-nối-đầu, được mã hóa bằng ratchet. Với tư cách là người quan sát bên ngoài giữa các bước nhảy trong tunnel, dữ liệu này được mã hóa thêm hai lần nữa, bằng mã hóa tunnel và mã hóa truyền tải. Với tư cách là người quan sát bên ngoài giữa OBEP và IBGW, dữ liệu chỉ được mã hóa thêm một lần, bằng mã hóa truyền tải. Với tư cách là thành phần tham gia OBEP hoặc IBGW, ratchet là lớp mã hóa duy nhất. Tuy nhiên, do các tunnel là đơn hướng, việc thu thập cả hai thông điệp trong quá trình bắt tay ratchet sẽ yêu cầu sự thông đồng giữa các router, trừ khi các tunnel được xây dựng sao cho OBEP và IBGW nằm trên cùng một router.

Mô hình mối đe dọa PQ đáng lo ngại nhất hiện nay là lưu trữ lưu lượng truy cập hôm nay để giải mã trong nhiều nhiều năm tới (bảo mật chuyển tiếp). Một phương pháp lai sẽ bảo vệ khỏi nguy cơ đó.

Mô hình mối đe dọa PQ về việc phá vỡ các khóa xác thực trong một khoảng thời gian hợp lý (ví dụ vài tháng) rồi sau đó giả mạo xác thực hoặc giải mã gần như theo thời gian thực, liệu có còn rất xa? Và đó chính là lúc chúng ta cần chuyển sang sử dụng các khóa tĩnh PQC.

Vì vậy, mô hình đe dọa bảo mật hậu lượng tử (PQ) sớm nhất là OBEP/IBGW lưu lưu lượng để giải mã sau này. Chúng ta nên triển khai cơ chế ratchet lai trước tiên.

Ratchet là ưu tiên cao nhất. Các lớp truyền tải đứng thứ hai. Chữ ký điện tử là ưu tiên thấp nhất.

Nếu chúng ta không thể hỗ trợ cả giao thức ratchet cũ và mới trên cùng một tunnel, việc chuyển đổi sẽ khó khăn hơn nhiều.

Việc phát triển hỗ trợ chữ ký MLDSA trong I2P đang tạm dừng cho đến cuối năm 2027 hoặc 2028, chờ các tổ chức tiêu chuẩn hoàn tất việc lựa chọn thuật toán, có thể giảm kích thước khóa và/hoặc chữ ký, đồng thời thúc đẩy việc áp dụng trong ngành. Xem [CABFORUM](https://cabforum.org/2024/10/10/2024-10-10-minutes-of-the-code-signing-certificate-working-group/), [COMPOSITE-SIGS](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/), và [PLANTS](https://datatracker.ietf.org/wg/plants/about/). Ngoài ra, việc áp dụng MLDSA trong ngành sẽ được chuẩn hóa bởi IETF, CA/Browser Forum và các Tổ chức Chứng thực (Certificate Authorities). Các CA cần hỗ trợ từ phần cứng bảo mật (HSM) trước tiên, điều này hiện chưa khả dụng [CA/Browser Forum](https://cabforum.org/2024/10/10/2024-10-10-minutes-of-the-code-signing-certificate-working-group/). Chúng tôi kỳ vọng IETF và CA/Browser Forum sẽ là những bên dẫn dắt trong việc đưa ra quyết định về các lựa chọn tham số cụ thể, bao gồm việc có nên hỗ trợ hoặc yêu cầu các chữ ký ghép (composite signatures) hay không [COMPOSITE-SIGS](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/).

| Mốc quan trọng | Mục tiêu |
|-----------|--------|
| Ratchet beta | Cuối năm 2025 |
| Chọn loại mã hóa tốt nhất | Đầu năm 2026 |
| NTCP2 beta | Đầu năm 2026 |
| SSU2 beta | Giữa năm 2026 |
| Ratchet chính thức | Giữa năm 2026 |
| Ratchet mặc định | Cuối năm 2026 |
| Chữ ký số (Signature) beta | Cuối năm 2026 |
| NTCP2 chính thức | Cuối năm 2026 |
| SSU2 chính thức | Đầu năm 2027 |
| Chọn loại chữ ký số tốt nhất | Đầu năm 2027 |
| NTCP2 mặc định | Đầu năm 2027 |
| SSU2 mặc định | Giữa năm 2027 |
| Chữ ký số (Signature) chính thức | Giữa năm 2027 |
## Di chuyển

Nếu chúng ta không thể hỗ trợ cả giao thức ratchet cũ và mới trên cùng một tunnel, việc chuyển đổi sẽ khó khăn hơn nhiều.

Chúng ta nên có thể thử lần lượt từng cái một, giống như cách chúng ta đã làm với X25519, để được chứng minh.

## Vấn đề

SHA256 dự kiến sẽ an toàn trong vòng 20-30 năm nữa, không bị đe dọa bởi máy tính lượng tử (PQ), xem [bản trình bày của NIST](https://csrc.nist.gov/csrc/media/Presentations/2022/update-on-post-quantum-encryption-and-cryptographi/Day%202%20-%20230pm%20Chen%20PQC%20ISPAB.pdf) và [bản trình bày của NCCOE](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf). Nếu SHA256 bị phá vỡ, chúng ta sẽ gặp những vấn đề nghiêm trọng hơn (netDb).

## Tài liệu tham khảo

* [CABFORUM](https://cabforum.org/2024/10/10/2024-10-10-minutes-of-the-code-signing-certificate-working-group/)
* [Choosing-Hash](https://kerkour.com/fast-secure-hash-function-sha256-sha512-sha3-blake3)
* [CLOUDFLARE](https://blog.cloudflare.com/pq-2024/)
* [COMMON](/docs/specs/common-structures/)
* [COMPOSITE-SIGS](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/)
* [ECIES](/docs/specs/ecies/)
* [FORUM](http://zzz.i2p/topics/3294)
* [FIPS202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf)
* [FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)
* [FIPS204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf)
* [FIPS205](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.205.pdf)
* [MLDSA-OIDS](https://datatracker.ietf.org/doc/draft-ietf-lamps-dilithium-certificates/)
* [NIST-PQ](https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards)
* [NIST-PQ-UPDATE](https://csrc.nist.gov/csrc/media/Presentations/2022/update-on-post-quantum-encryption-and-cryptographi/Day%202%20-%20230pm%20Chen%20PQC%20ISPAB.pdf)
* [NIST-PQ-END](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf)
* [NIST-VECTORS](https://csrc.nist.gov/projects/cryptographic-standards-and-guidelines/example-values)
* [Noise](https://noiseprotocol.org/noise.html)
* [Noise-Hybrid](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf)
* [NSA-PQ](https://media.defense.gov/2022/Sep/07/2003071836/-1/-1/0/CSI_CNSA_2.0_FAQ_.PDF)
* [NTCP2](/docs/specs/ntcp2/)
* [OPENSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/)
* [Prop165](/docs/proposals/165/)
* [PQ-WIREGUARD](https://eprint.iacr.org/2020/379.pdf)
* [RFC-2104](https://tools.ietf.org/html/rfc2104)
* [Rosenpass](https://rosenpass.eu/)
* [Rosenpass-Whitepaper](https://raw.githubusercontent.com/rosenpass/rosenpass/papers-pdf/whitepaper.pdf)
* [SSH-HYBRID](https://datatracker.ietf.org/doc/draft-ietf-sshm-mlkem-hybrid-kex/)
* [SSU2](/docs/specs/ssu2/)
* [TLS-HYBRID](https://datatracker.ietf.org/doc/draft-ietf-tls-hybrid-design/)
