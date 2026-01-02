---
title: "Giao thức Mật mã Hậu Lượng tử"
number: "169"
author: "zzz, orignal, drzed, eyedeekay"
created: "2025-01-21"
lastupdated: "2025-06-12"
status: "Mở"
thread: "http://zzz.i2p/topics/3294"
target: "0.9.80"
toc: true
---

## Tổng quan

Trong khi nghiên cứu và cạnh tranh để tìm ra mật mã học hậu lượng tử (PQ) phù hợp đã diễn ra trong một thập kỷ, các lựa chọn vẫn chưa trở nên rõ ràng cho đến gần đây.

Chúng tôi bắt đầu xem xét những tác động của mật mã PQ vào năm 2022 [zzz.i2p](http://zzz.i2p/topics/3294).

Các tiêu chuẩn TLS đã bổ sung hỗ trợ mã hóa lai trong hai năm qua và hiện tại được sử dụng cho một phần đáng kể lưu lượng mã hóa trên internet nhờ vào sự hỗ trợ trong Chrome và Firefox [Cloudflare](https://blog.cloudflare.com/pq-2024/).

NIST gần đây đã hoàn thiện và công bố các thuật toán được khuyến nghị cho mật mã hậu lượng tử [NIST](https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards). Một số thư viện mật mã phổ biến hiện đã hỗ trợ các tiêu chuẩn NIST hoặc sẽ phát hành hỗ trợ trong tương lai gần.

Cả [Cloudflare](https://blog.cloudflare.com/pq-2024/) và [NIST](https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards) đều khuyến nghị việc di chuyển nên bắt đầu ngay lập tức. Xem thêm NSA PQ FAQ năm 2022 [NSA](https://media.defense.gov/2022/Sep/07/2003071836/-1/-1/0/CSI_CNSA_2.0_FAQ_.PDF). I2P nên dẫn đầu trong lĩnh vực bảo mật và mật mã học. Đây là thời điểm thích hợp để triển khai các thuật toán được khuyến nghị. Sử dụng hệ thống loại mã hóa và loại chữ ký linh hoạt của chúng tôi, chúng tôi sẽ thêm các loại cho mã hóa hybrid, và cho chữ ký PQ và hybrid.

## Mục tiêu

- Chọn các thuật toán chống lại PQ
- Thêm các thuật toán chỉ PQ và hybrid vào các giao thức I2P khi phù hợp
- Định nghĩa nhiều biến thể
- Chọn các biến thể tốt nhất sau khi triển khai, kiểm tra, phân tích và nghiên cứu
- Thêm hỗ trợ từng bước và đảm bảo tương thích ngược

## Các Mục Tiêu Không Theo Đuổi

- Không thay đổi các giao thức mã hóa một chiều (Noise N)
- Không rời bỏ SHA256, không bị đe dọa trong ngắn hạn bởi PQ
- Không lựa chọn các biến thể ưu tiên cuối cùng vào thời điểm này

## Mô hình Mối đe dọa

- Các router tại OBEP hoặc IBGW, có thể thông đồng,
  lưu trữ các tin nhắn garlic để giải mã sau này (forward secrecy)
- Các bên quan sát mạng
  lưu trữ các tin nhắn vận chuyển để giải mã sau này (forward secrecy)
- Các thành viên mạng giả mạo chữ ký cho RI, LS, streaming, datagram,
  hoặc các cấu trúc khác

## Các Giao thức Bị Ảnh hưởng

Chúng tôi sẽ sửa đổi các giao thức sau đây, theo thứ tự phát triển tương đối. Việc triển khai tổng thể có thể sẽ từ cuối năm 2025 đến giữa năm 2027. Xem phần Ưu tiên và Triển khai bên dưới để biết chi tiết.

| Protocol / Feature | Status |
|--------------------|--------|
| Hybrid MLKEM Ratchet and LS | Approved 2026-06; beta target 2025-08; release target 2025-11 |
| Hybrid MLKEM NTCP2 | Some details to be finalized |
| Hybrid MLKEM SSU2 | Some details to be finalized |
| MLDSA SigTypes 12-14 | Proposal is stable but may not be finalized until 2026 |
| MLDSA Dests | Tested on live net, requires net upgrade for floodfill support |
| Hybrid SigTypes 15-17 | Preliminary |
| Hybrid Dests | |
## Thiết kế

Chúng tôi sẽ hỗ trợ các tiêu chuẩn NIST FIPS 203 và 204 [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf) [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) dựa trên, nhưng KHÔNG tương thích với, CRYSTALS-Kyber và CRYSTALS-Dilithium (phiên bản 3.1, 3, và các phiên bản cũ hơn).

### Key Exchange

Chúng tôi sẽ hỗ trợ trao đổi khóa hybrid trong các giao thức sau:

| Proto   | Noise Type | Support PQ only? | Support Hybrid? |
|---------|------------|------------------|-----------------|
| NTCP2   | XK         | no               | yes             |
| SSU2    | XK         | no               | yes             |
| Ratchet | IK         | no               | yes             |
| TBM     | N          | no               | no              |
| NetDB   | N          | no               | no              |
PQ KEM chỉ cung cấp các khóa tạm thời và không hỗ trợ trực tiếp các quá trình bắt tay khóa tĩnh như Noise XK và IK.

Noise N không sử dụng trao đổi khóa hai chiều và do đó không phù hợp cho mã hóa hybrid.

Vậy nên chúng tôi sẽ chỉ hỗ trợ mã hóa hybrid, cho NTCP2, SSU2, và Ratchet. Chúng tôi sẽ định nghĩa ba biến thể ML-KEM như trong [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf), cho tổng cộng 3 loại mã hóa mới. Các loại hybrid sẽ chỉ được định nghĩa kết hợp với X25519.

Các loại mã hóa mới là:

| Type | Code |
|------|------|
| MLKEM512_X25519 | 5 |
| MLKEM768_X25519 | 6 |
| MLKEM1024_X25519 | 7 |
Overhead sẽ rất đáng kể. Kích thước thông điệp 1 và 2 điển hình (đối với XK và IK) hiện tại khoảng 100 byte (trước khi có bất kỳ payload bổ sung nào). Điều này sẽ tăng từ 8x đến 15x tùy thuộc vào thuật toán.

### Signatures

Chúng tôi sẽ hỗ trợ chữ ký PQ và hybrid trong các cấu trúc sau:

| Type | Support PQ only? | Support Hybrid? |
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
Vậy nên chúng tôi sẽ hỗ trợ cả chữ ký chỉ PQ và hybrid. Chúng tôi sẽ định nghĩa ba biến thể ML-DSA như trong [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf), ba biến thể hybrid với Ed25519, và ba biến thể chỉ PQ với prehash chỉ dành cho file SU3, tổng cộng 9 loại chữ ký mới. Các loại hybrid sẽ chỉ được định nghĩa kết hợp với Ed25519. Chúng tôi sẽ sử dụng ML-DSA tiêu chuẩn, KHÔNG phải các biến thể pre-hash (HashML-DSA), trừ file SU3.

Chúng tôi sẽ sử dụng biến thể ký "hedged" hoặc ngẫu nhiên hóa, không phải biến thể "determinstic", như được định nghĩa trong [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) mục 3.4. Điều này đảm bảo rằng mỗi chữ ký sẽ khác nhau, ngay cả khi ký trên cùng một dữ liệu, và cung cấp bảo vệ bổ sung chống lại các cuộc tấn công kênh phụ. Xem phần ghi chú triển khai bên dưới để biết thêm chi tiết về các lựa chọn thuật toán bao gồm mã hóa và ngữ cảnh.

Các loại chữ ký mới là:

| Type | Code |
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
Chứng chỉ X.509 và các mã hóa DER khác sẽ sử dụng các cấu trúc tổng hợp và OID được định nghĩa trong [IETF draft](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/).

Overhead sẽ đáng kể. Kích thước điển hình của destination Ed25519 và router identity là 391 byte. Chúng sẽ tăng từ 3.5x đến 6.8x tùy thuộc vào thuật toán. Chữ ký Ed25519 có kích thước 64 byte. Chúng sẽ tăng từ 38x đến 76x tùy thuộc vào thuật toán. RouterInfo đã ký, LeaseSet, datagram có thể phản hồi, và streaming message đã ký điển hình có kích thước khoảng 1KB. Chúng sẽ tăng từ 3x đến 8x tùy thuộc vào thuật toán.

Vì các loại định danh đích và router mới sẽ không chứa padding, chúng sẽ không thể nén được. Kích thước của các destination và router identity được nén gzip trong quá trình truyền tải sẽ tăng từ 12x - 38x tùy thuộc vào thuật toán.

### Legal Combinations

Đối với các Destinations, các loại chữ ký mới được hỗ trợ với tất cả loại mã hóa trong leaseset. Đặt loại mã hóa trong key certificate thành NONE (255).

Đối với RouterIdentities, loại mã hóa ElGamal đã được ngừng sử dụng. Các loại chữ ký mới chỉ được hỗ trợ với mã hóa X25519 (loại 4). Các loại mã hóa mới sẽ được chỉ định trong RouterAddresses. Loại mã hóa trong key certificate sẽ tiếp tục là loại 4.

### New Crypto Required

- ML-KEM (trước đây là CRYSTALS-Kyber) [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)
- ML-DSA (trước đây là CRYSTALS-Dilithium) [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf)
- SHA3-128 (trước đây là Keccak-256) [FIPS 202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf) Chỉ được sử dụng cho SHAKE128
- SHA3-256 (trước đây là Keccak-512) [FIPS 202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf)
- SHAKE128 và SHAKE256 (phần mở rộng XOF cho SHA3-128 và SHA3-256) [FIPS 202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf)

Các test vector cho SHA3-256, SHAKE128, và SHAKE256 có tại [NIST](https://csrc.nist.gov/projects/cryptographic-standards-and-guidelines/example-values).

Lưu ý rằng thư viện Java bouncycastle hỗ trợ tất cả các thuật toán trên. Hỗ trợ thư viện C++ có trong OpenSSL 3.5 [OpenSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/).

### Alternatives

Chúng tôi sẽ không hỗ trợ [FIPS 205](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.205.pdf) (Sphincs+), vì nó chậm hơn và lớn hơn ML-DSA rất nhiều. Chúng tôi sẽ không hỗ trợ FIPS206 sắp tới (Falcon), vì nó chưa được tiêu chuẩn hóa. Chúng tôi sẽ không hỗ trợ NTRU hoặc các ứng viên PQ khác không được NIST tiêu chuẩn hóa.

### Rosenpass

Có một số nghiên cứu [paper](https://eprint.iacr.org/2020/379.pdf) về việc điều chỉnh Wireguard (IK) cho mã hóa PQ thuần túy, nhưng có một số câu hỏi mở trong bài báo đó. Sau đó, cách tiếp cận này đã được triển khai dưới dạng Rosenpass [Rosenpass](https://rosenpass.eu/) [whitepaper](https://raw.githubusercontent.com/rosenpass/rosenpass/papers-pdf/whitepaper.pdf) cho PQ Wireguard.

Rosenpass sử dụng một bắt tay giống Noise KK với các khóa tĩnh Classic McEliece 460896 được chia sẻ trước (mỗi khóa 500 KB) và các khóa tạm thời Kyber-512 (về cơ bản là MLKEM-512). Vì các bản mã hóa Classic McEliece chỉ có 188 byte, và các khóa công khai cùng bản mã hóa Kyber-512 có kích thước hợp lý, cả hai thông điệp bắt tay đều vừa với MTU UDP tiêu chuẩn. Khóa chia sẻ đầu ra (osk) từ bắt tay PQ KK được sử dụng làm khóa chia sẻ trước đầu vào (psk) cho bắt tay Wireguard IK tiêu chuẩn. Vậy tổng cộng có hai bắt tay hoàn chỉnh, một bắt tay PQ thuần túy và một bắt tay X25519 thuần túy.

Chúng ta không thể thực hiện bất kỳ điều nào trong số này để thay thế các handshake XK và IK của chúng ta vì:

- Chúng ta không thể thực hiện KK, Bob không có static key của Alice
- Static key 500KB quá lớn
- Chúng ta không muốn có thêm round-trip

Có rất nhiều thông tin hữu ích trong whitepaper, và chúng tôi sẽ xem xét nó để tìm ý tưởng và cảm hứng. TODO.

## Specification

### Trao Đổi Khóa

Cập nhật các phần và bảng trong tài liệu cấu trúc chung [/docs/specs/common-structures/](/docs/specs/common-structures/) như sau:

### Chữ ký

Các loại Public Key mới là:

| Type | Public Key Length | Since | Usage |
|------|-------------------|-------|-------|
| MLKEM512_X25519 | 32 | 0.9.xx | See proposal 169, for Leasesets only, not for RIs or Destinations |
| MLKEM768_X25519 | 32 | 0.9.xx | See proposal 169, for Leasesets only, not for RIs or Destinations |
| MLKEM1024_X25519 | 32 | 0.9.xx | See proposal 169, for Leasesets only, not for RIs or Destinations |
| MLKEM512 | 800 | 0.9.xx | See proposal 169, for handshakes only, not for Leasesets, RIs or Destinations |
| MLKEM768 | 1184 | 0.9.xx | See proposal 169, for handshakes only, not for Leasesets, RIs or Destinations |
| MLKEM1024 | 1568 | 0.9.xx | See proposal 169, for handshakes only, not for Leasesets, RIs or Destinations |
| MLKEM512_CT | 768 | 0.9.xx | See proposal 169, for handshakes only, not for Leasesets, RIs or Destinations |
| MLKEM768_CT | 1088 | 0.9.xx | See proposal 169, for handshakes only, not for Leasesets, RIs or Destinations |
| MLKEM1024_CT | 1568 | 0.9.xx | See proposal 169, for handshakes only, not for Leasesets, RIs or Destinations |
| NONE | 0 | 0.9.xx | See proposal 169, for destinations with PQ sig types only, not for RIs or Leasesets |
Khóa công khai hybrid là khóa X25519. Khóa công khai KEM là khóa PQ tạm thời được gửi từ Alice đến Bob. Mã hóa và thứ tự byte được định nghĩa trong [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf).

Các khóa MLKEM*_CT không thực sự là khóa công khai, chúng là "ciphertext" được gửi từ Bob đến Alice trong quá trình bắt tay Noise. Chúng được liệt kê ở đây để hoàn thiện thông tin.

### Các Kết Hợp Hợp Lệ

Các loại Private Key mới là:

| Type | Private Key Length | Since | Usage |
|------|---------------------|-------|-------|
| MLKEM512_X25519 | 32 | 0.9.xx | See proposal 169, for Leasesets only, not for RIs or Destinations |
| MLKEM768_X25519 | 32 | 0.9.xx | See proposal 169, for Leasesets only, not for RIs or Destinations |
| MLKEM1024_X25519 | 32 | 0.9.xx | See proposal 169, for Leasesets only, not for RIs or Destinations |
| MLKEM512 | 1632 | 0.9.xx | See proposal 169, for handshakes only, not for Leasesets, RIs or Destinations |
| MLKEM768 | 2400 | 0.9.xx | See proposal 169, for handshakes only, not for Leasesets, RIs or Destinations |
| MLKEM1024 | 3168 | 0.9.xx | See proposal 169, for handshakes only, not for Leasesets, RIs or Destinations |
Các khóa riêng tư hybrid là các khóa X25519. Các khóa riêng tư KEM chỉ dành cho Alice. Mã hóa KEM và thứ tự byte được định nghĩa trong [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf).

### Yêu Cầu Mã Hóa Mới

Các loại Signing Public Key mới là:

| Type | Length (bytes) | Since | Usage |
|------|----------------|-------|-------|
| MLDSA44 | 1312 | 0.9.xx | See proposal 169 |
| MLDSA65 | 1952 | 0.9.xx | See proposal 169 |
| MLDSA87 | 2592 | 0.9.xx | See proposal 169 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 1344 | 0.9.xx | See proposal 169 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 1984 | 0.9.xx | See proposal 169 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 2624 | 0.9.xx | See proposal 169 |
| MLDSA44ph | 1344 | 0.9.xx | Only for SU3 files, not for netdb structures |
| MLDSA65ph | 1984 | 0.9.xx | Only for SU3 files, not for netdb structures |
| MLDSA87ph | 2624 | 0.9.xx | Only for SU3 files, not for netdb structures |
Khóa công khai ký lai (hybrid signing public keys) là khóa Ed25519 theo sau bởi khóa PQ, như trong [IETF draft](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/). Mã hóa và thứ tự byte được định nghĩa trong [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf).

### Các Phương Án Thay Thế

Các loại Signing Private Key mới là:

| Type | Length (bytes) | Since | Usage |
|------|----------------|-------|-------|
| MLDSA44 | 2560 | 0.9.xx | See proposal 169 |
| MLDSA65 | 4032 | 0.9.xx | See proposal 169 |
| MLDSA87 | 4896 | 0.9.xx | See proposal 169 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 2592 | 0.9.xx | See proposal 169 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 4064 | 0.9.xx | See proposal 169 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 4928 | 0.9.xx | See proposal 169 |
| MLDSA44ph | 2592 | 0.9.xx | Only for SU3 files, not for netdb structures. See proposal 169 |
| MLDSA65ph | 4064 | 0.9.xx | Only for SU3 files, not for netdb structures. See proposal 169 |
| MLDSA87ph | 4928 | 0.9.xx | Only for SU3 files, not for netdb structures. See proposal 169 |
Khóa riêng tư ký lai (hybrid signing private keys) là khóa Ed25519 theo sau bởi khóa PQ, như trong [IETF draft](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/). Mã hóa và thứ tự byte được định nghĩa trong [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf).

### Rosenpass

Các loại Signature mới là:

| Type | Length (bytes) | Since | Usage |
|------|----------------|-------|-------|
| MLDSA44 | 2420 | 0.9.xx | See proposal 169 |
| MLDSA65 | 3309 | 0.9.xx | See proposal 169 |
| MLDSA87 | 4627 | 0.9.xx | See proposal 169 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 2484 | 0.9.xx | See proposal 169 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 3373 | 0.9.xx | See proposal 169 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 4691 | 0.9.xx | See proposal 169 |
| MLDSA44ph | 2484 | 0.9.xx | Only for SU3 files, not for netdb structures. See proposal 169 |
| MLDSA65ph | 3373 | 0.9.xx | Only for SU3 files, not for netdb structures. See proposal 169 |
| MLDSA87ph | 4691 | 0.9.xx | Only for SU3 files, not for netdb structures. See proposal 169 |
Chữ ký hybrid là chữ ký Ed25519 theo sau bởi chữ ký PQ, như trong [IETF draft](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/). Chữ ký hybrid được xác minh bằng cách xác minh cả hai chữ ký, và sẽ thất bại nếu một trong hai thất bại. Mã hóa và thứ tự byte được định nghĩa trong [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf).

### Key Certificates

Các loại Signing Public Key mới là:

| Type | Type Code | Total Public Key Length | Since | Usage |
|------|-----------|-------------------------|-------|-------|
| MLDSA44 | 12 | 1312 | 0.9.xx | See proposal 169 |
| MLDSA65 | 13 | 1952 | 0.9.xx | See proposal 169 |
| MLDSA87 | 14 | 2592 | 0.9.xx | See proposal 169 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 15 | 1344 | 0.9.xx | See proposal 169 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 16 | 1984 | 0.9.xx | See proposal 169 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 17 | 2624 | 0.9.xx | See proposal 169 |
| MLDSA44ph | 18 | n/a | 0.9.xx | Only for SU3 files |
| MLDSA65ph | 19 | n/a | 0.9.xx | Only for SU3 files |
| MLDSA87ph | 20 | n/a | 0.9.xx | Only for SU3 files |
Các loại Crypto Public Key mới là:

| Type | Type Code | Total Public Key Length | Since | Usage |
|------|-----------|-------------------------|-------|-------|
| MLKEM512_X25519 | 5 | 32 | 0.9.xx | See proposal 169, for Leasesets only, not for RIs or Destinations |
| MLKEM768_X25519 | 6 | 32 | 0.9.xx | See proposal 169, for Leasesets only, not for RIs or Destinations |
| MLKEM1024_X25519 | 7 | 32 | 0.9.xx | See proposal 169, for Leasesets only, not for RIs or Destinations |
| NONE | 255 | 0 | 0.9.xx | See proposal 169 |
Các loại khóa hybrid KHÔNG BAO GIỜ được bao gồm trong chứng chỉ khóa; chỉ có trong leaseSet.

Đối với các điểm đến có loại chữ ký Hybrid hoặc PQ, sử dụng NONE (loại 255) cho loại mã hóa, nhưng không có khóa mã hóa, và toàn bộ phần chính 384-byte dành cho khóa ký.

### Cấu trúc Chung

Đây là các độ dài cho các loại Destination mới. Loại mã hóa (Enc type) cho tất cả là NONE (loại 255) và độ dài khóa mã hóa được xử lý như 0. Toàn bộ phần 384-byte được sử dụng cho phần đầu của khóa công khai ký. LƯU Ý: Điều này khác với đặc tả cho các loại chữ ký ECDSA_SHA512_P521 và RSA, nơi chúng ta vẫn duy trì khóa ElGamal 256-byte trong destination mặc dù nó không được sử dụng.

Không có padding. Tổng độ dài là 7 + tổng độ dài key. Độ dài key certificate là 4 + độ dài key dư thừa.

Ví dụ luồng byte destination 1319-byte cho MLDSA44:

skey[0:383] 5 (932 >> 8) (932 & 0xff) 00 12 00 255 skey[384:1311]

| Type | Type Code | Total Public Key Length | Main | Excess | Total Dest Length |
|------|-----------|-------------------------|------|--------|-------------------|
| MLDSA44 | 12 | 1312 | 384 | 928 | 1319 |
| MLDSA65 | 13 | 1952 | 384 | 1568 | 1959 |
| MLDSA87 | 14 | 2592 | 384 | 2208 | 2599 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 15 | 1344 | 384 | 960 | 1351 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 16 | 1984 | 384 | 1600 | 1991 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 17 | 2624 | 384 | 2240 | 2631 |
### PublicKey

Đây là độ dài cho các loại Destination mới. Loại mã hóa cho tất cả là X25519 (loại 4). Toàn bộ phần 352-byte sau khóa công khai X25519 được sử dụng cho phần đầu tiên của khóa công khai ký. Không có padding. Tổng độ dài là 39 + tổng độ dài khóa. Độ dài certificate khóa là 4 + độ dài khóa vượt quá.

Ví dụ luồng byte router identity 1351 byte cho MLDSA44:

enckey[0:31] skey[0:351] 5 (960 >> 8) (960 & 0xff) 00 12 00 4 skey[352:1311]

| Type | Type Code | Total Public Key Length | Main | Excess | Total RouterIdent Length |
|------|-----------|-------------------------|------|--------|--------------------------|
| MLDSA44 | 12 | 1312 | 352 | 960 | 1351 |
| MLDSA65 | 13 | 1952 | 352 | 1600 | 1991 |
| MLDSA87 | 14 | 2592 | 352 | 2240 | 2631 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 15 | 1344 | 352 | 992 | 1383 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 16 | 1984 | 352 | 1632 | 2023 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 17 | 2624 | 352 | 2272 | 2663 |
### PrivateKey

Việc bắt tay sử dụng các mẫu bắt tay [Noise Protocol](https://noiseprotocol.org/noise.html).

Ánh xạ chữ cái sau đây được sử dụng:

- e = khóa ephemeral một lần
- s = khóa tĩnh
- p = message payload
- e1 = khóa PQ ephemeral một lần, gửi từ Alice đến Bob
- ekem1 = KEM ciphertext, gửi từ Bob đến Alice

Các thay đổi sau đối với XK và IK cho hybrid forward secrecy (hfs) được quy định trong [Noise HFS spec](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) phần 5:

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
Mẫu e1 được định nghĩa như sau, như được chỉ định trong [Noise HFS spec](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) mục 4:

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
Mẫu ekem1 được định nghĩa như sau, theo quy định trong [Noise HFS spec](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) phần 4:

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
### SigningPublicKey

#### Issues

- Chúng ta có nên thay đổi hàm hash handshake không? Xem [comparison](https://kerkour.com/fast-secure-hash-function-sha256-sha512-sha3-blake3).
  SHA256 không dễ bị tấn công bởi PQ, nhưng nếu chúng ta muốn nâng cấp
  hàm hash, bây giờ là lúc thích hợp, trong khi chúng ta đang thay đổi những thứ khác.
  Đề xuất SSH IETF hiện tại [IETF draft](https://datatracker.ietf.org/doc/draft-ietf-sshm-mlkem-hybrid-kex/) là sử dụng MLKEM768
  với SHA256, và MLKEM1024 với SHA384. Đề xuất đó bao gồm
  một cuộc thảo luận về các cân nhắc bảo mật.
- Chúng ta có nên ngừng gửi dữ liệu ratchet 0-RTT (ngoài LS) không?
- Chúng ta có nên chuyển ratchet từ IK sang XK nếu chúng ta không gửi dữ liệu 0-RTT không?

#### Overview

Phần này áp dụng cho cả hai giao thức IK và XK.

Handshake hybrid được định nghĩa trong [Noise HFS spec](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf). Tin nhắn đầu tiên, từ Alice đến Bob, chứa e1, khóa đóng gói, trước payload của tin nhắn. Điều này được xử lý như một khóa tĩnh bổ sung; gọi EncryptAndHash() trên nó (với tư cách Alice) hoặc DecryptAndHash() (với tư cách Bob). Sau đó xử lý payload tin nhắn như thường lệ.

Thông điệp thứ hai, từ Bob đến Alice, chứa ekem1, bản mã hóa, trước tải trọng thông điệp. Điều này được xử lý như một khóa tĩnh bổ sung; gọi EncryptAndHash() trên nó (với vai trò Bob) hoặc DecryptAndHash() (với vai trò Alice). Sau đó, tính toán kem_shared_key và gọi MixKey(kem_shared_key). Tiếp theo xử lý tải trọng thông điệp như thường lệ.

#### Defined ML-KEM Operations

Chúng tôi định nghĩa các hàm sau tương ứng với các khối xây dựng mật mã được sử dụng như được định nghĩa trong [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf).

(encap_key, decap_key) = PQ_KEYGEN()

    Alice creates the encapsulation and decapsulation keys
    The encapsulation key is sent in message 1.
    encap_key and decap_key sizes vary based on ML-KEM variant.

(ciphertext, kem_shared_key) = ENCAPS(encap_key)

    Bob calculates the ciphertext and shared key,
    using the ciphertext received in message 1.
    The ciphertext is sent in message 2.
    ciphertext size varies based on ML-KEM variant.
    The kem_shared_key is always 32 bytes.

kem_shared_key = DECAPS(ciphertext, decap_key)

    Alice calculates the shared key,
    using the ciphertext received in message 2.
    The kem_shared_key is always 32 bytes.

Lưu ý rằng cả encap_key và ciphertext đều được mã hóa bên trong các khối ChaCha/Poly trong thông điệp bắt tay Noise 1 và 2. Chúng sẽ được giải mã như một phần của quá trình bắt tay.

kem_shared_key được trộn vào chaining key bằng MixHash(). Xem chi tiết bên dưới.

#### Alice KDF for Message 1

Đối với XK: Sau pattern thông điệp 'es' và trước payload, thêm:

HOẶC

Đối với IK: Sau pattern tin nhắn 'es' và trước pattern tin nhắn 's', thêm:

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
#### Bob KDF for Message 1

Đối với XK: Sau mẫu message 'es' và trước payload, thêm:

HOẶC

Đối với IK: Sau message pattern 'es' và trước message pattern 's', thêm:

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
#### Bob KDF for Message 2

Đối với XK: Sau mẫu message 'ee' và trước payload, thêm:

HOẶC

Đối với IK: Sau message pattern 'ee' và trước message pattern 'se', thêm:

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
```
#### Alice KDF for Message 2

Sau message pattern 'ee' (và trước message pattern 'ss' cho IK), thêm:

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
```
#### KDF for Message 3 (XK only)

không thay đổi

#### KDF for split()

không thay đổi

### SigningPrivateKey

Cập nhật đặc tả ECIES-Ratchet [/docs/specs/ecies/](/docs/specs/ecies/) như sau:

#### Noise identifiers

- "Noise_IKhfselg2_25519+MLKEM512_ChaChaPoly_SHA256"
- "Noise_IKhfselg2_25519+MLKEM768_ChaChaPoly_SHA256"
- "Noise_IKhfselg2_25519+MLKEM1024_ChaChaPoly_SHA256"

#### 1b) New session format (with binding)

Thay đổi: Ratchet hiện tại chứa static key trong phần ChaCha đầu tiên, và payload trong phần thứ hai. Với ML-KEM, giờ có ba phần. Phần đầu tiên chứa PQ public key được mã hóa. Phần thứ hai chứa static key. Phần thứ ba chứa payload.

Định dạng mã hóa:

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

| Type | Type Code | X len | Msg 1 len | Msg 1 Enc len | Msg 1 Dec len | PQ key len | pl len |
|------|-----------|-------|-----------|---------------|---------------|------------|--------|
| X25519 | 4 | 32 | 96+pl | 64+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 912+pl | 880+pl | 800+pl | 800 | pl |
| MLKEM768_X25519 | 6 | 32 | 1296+pl | 1360+pl | 1184+pl | 1184 | pl |
| MLKEM1024_X25519 | 7 | 32 | 1680+pl | 1648+pl | 1568+pl | 1568 | pl |
Lưu ý rằng payload phải chứa một khối DateTime, vì vậy kích thước payload tối thiểu là 7. Kích thước thông điệp 1 tối thiểu có thể được tính toán tương ứng.

#### 1g) New Session Reply format

Thay đổi: Ratchet hiện tại có payload trống cho phần ChaCha đầu tiên, và payload trong phần thứ hai. Với ML-KEM, giờ đây có ba phần. Phần đầu tiên chứa ciphertext PQ đã mã hóa. Phần thứ hai có payload trống. Phần thứ ba chứa payload.

Định dạng mã hóa:

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

| Type | Type Code | Y len | Msg 2 len | Msg 2 Enc len | Msg 2 Dec len | PQ CT len | opt len |
|------|-----------|-------|-----------|---------------|---------------|-----------|---------|
| X25519 | 4 | 32 | 72+pl | 32+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 856+pl | 816+pl | 768+pl | 768 | pl |
| MLKEM768_X25519 | 6 | 32 | 1176+pl | 1136+pl | 1088+pl | 1088 | pl |
| MLKEM1024_X25519 | 7 | 32 | 1656+pl | 1616+pl | 1568+pl | 1568 | pl |
Lưu ý rằng mặc dù message 2 thường sẽ có payload khác không, đặc tả ratchet [/docs/specs/ecies/](/docs/specs/ecies/) không yêu cầu điều này, do đó kích thước payload tối thiểu là 0. Kích thước message 2 tối thiểu có thể được tính toán tương ứng.

### Chữ ký

Cập nhật đặc tả kỹ thuật NTCP2 [/docs/specs/ntcp2/](/docs/specs/ntcp2/) như sau:

#### Noise identifiers

- "Noise_XKhfsaesobfse+hs2+hs3_25519+MLKEM512_ChaChaPoly_SHA256"
- "Noise_XKhfsaesobfse+hs2+hs3_25519+MLKEM768_ChaChaPoly_SHA256"
- "Noise_XKhfsaesobfse+hs2+hs3_25519+MLKEM1024_ChaChaPoly_SHA256"

#### 1) SessionRequest

Thay đổi: NTCP2 hiện tại chỉ chứa các tùy chọn trong phần ChaCha. Với ML-KEM, phần ChaCha cũng sẽ chứa khóa công khai PQ đã được mã hóa.

Nội dung thô:

```
+----+----+----+----+----+----+----+----+
  |                                       |
  +        obfuscated with RH_B           +
  |       AES-CBC-256 encrypted X         |
  +             (32 bytes)                +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaChaPoly frame (MLKEM)            |
  +      (see table below for length)     +
  |   k defined in KDF for message 1      |
  +   n = 0                               +
  |   see KDF for associated data         |
  ~   n = 0                               ~
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   ChaChaPoly frame (options)          |
  +         32 bytes                      +
  |   k defined in KDF for message 1      |
  +   n = 0                               +
  |   see KDF for associated data         |
  +----+----+----+----+----+----+----+----+
  |     unencrypted authenticated         |
  ~         padding (optional)            ~
  |     length defined in options block   |
  +----+----+----+----+----+----+----+----+

  Same as before except add a second ChaChaPoly frame
```
Dữ liệu không mã hóa (thẻ xác thực Poly1305 không hiển thị):

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
Kích thước:

| Type | Type Code | X len | Msg 1 len | Msg 1 Enc len | Msg 1 Dec len | PQ key len | opt len |
|------|-----------|-------|-----------|---------------|---------------|------------|---------|
| X25519 | 4 | 32 | 64+pad | 32 | 16 | -- | 16 |
| MLKEM512_X25519 | 5 | 32 | 880+pad | 848 | 816 | 800 | 16 |
| MLKEM768_X25519 | 6 | 32 | 1264+pad | 1232 | 1200 | 1184 | 16 |
| MLKEM1024_X25519 | 7 | 32 | 1648+pad | 1616 | 1584 | 1568 | 16 |
Lưu ý: Mã loại chỉ dành cho sử dụng nội bộ. Các router sẽ vẫn là loại 4, và hỗ trợ sẽ được chỉ ra trong các địa chỉ router.

#### 2) SessionCreated

Thay đổi: NTCP2 hiện tại chỉ chứa các tùy chọn trong phần ChaCha. Với ML-KEM, phần ChaCha cũng sẽ chứa khóa công khai PQ được mã hóa.

Nội dung thô:

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
  |   ChaChaPoly frame (MLKEM)            |
  +   Encrypted and authenticated data    +
  -      (see table below for length)     -
  +   k defined in KDF for message 2      +
  |   n = 0; see KDF for associated data  |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaChaPoly frame (options)          |
  +   Encrypted and authenticated data    +
  -           32 bytes                    -
  +   k defined in KDF for message 2      +
  |   n = 0; see KDF for associated data  |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     unencrypted authenticated         |
  +         padding (optional)            +
  |     length defined in options block   |
  ~               .   .   .               ~
  |                                       |
  +----+----+----+----+----+----+----+----+

  Same as before except add a second ChaChaPoly frame
```
Dữ liệu không mã hóa (Poly1305 auth tag không hiển thị):

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

| Type | Type Code | Y len | Msg 2 len | Msg 2 Enc len | Msg 2 Dec len | PQ CT len | opt len |
|------|-----------|-------|-----------|---------------|---------------|-----------|---------|
| X25519 | 4 | 32 | 64+pad | 32 | 16 | -- | 16 |
| MLKEM512_X25519 | 5 | 32 | 848+pad | 816 | 784 | 768 | 16 |
| MLKEM768_X25519 | 6 | 32 | 1136+pad | 1104 | 1104 | 1088 | 16 |
| MLKEM1024_X25519 | 7 | 32 | 1616+pad | 1584 | 1584 | 1568 | 16 |
Lưu ý: Mã loại chỉ dành cho sử dụng nội bộ. Các router sẽ vẫn là loại 4, và việc hỗ trợ sẽ được chỉ ra trong các địa chỉ router.

#### 3) SessionConfirmed

Không thay đổi

#### Key Derivation Function (KDF) (for data phase)

Không thay đổi

### Chứng chỉ Khóa

Cập nhật đặc tả SSU2 [/docs/specs/ssu2/](/docs/specs/ssu2/) như sau:

#### Noise identifiers

- "Noise_XKhfschaobfse+hs1+hs2+hs3_25519+MLKEM512_ChaChaPoly_SHA256"
- "Noise_XKhfschaobfse+hs1+hs2+hs3_25519+MLKEM768_ChaChaPoly_SHA256"
- "Noise_XKhfschaobfse+hs1+hs2+hs3_25519+MLKEM1024_ChaChaPoly_SHA256"

#### Long Header

Header dài có kích thước 32 byte. Nó được sử dụng trước khi một phiên được tạo, cho Token Request, SessionRequest, SessionCreated, và Retry. Nó cũng được sử dụng cho các thông điệp Peer Test và Hole Punch ngoài phiên.

TODO: Chúng ta có thể sử dụng trường version nội bộ và dùng 3 cho MLKEM512 và 4 cho MLKEM768. Liệu chúng ta chỉ làm điều đó cho các loại 0 và 1 hay cho tất cả 6 loại?

Trước khi mã hóa header:

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

  ver :: The protocol version, equal to 2
         TODO We could internally use the version field and use 3 for MLKEM512 and 4 for MLKEM768.

  id :: 1 byte, the network ID (currently 2, except for test networks)

  flag :: 1 byte, unused, set to 0 for future compatibility

  Source Connection ID :: 8 bytes, unsigned big endian integer

  Token :: 8 bytes, unsigned big endian integer

```
#### Short Header

không thay đổi

#### SessionRequest (Type 0)

Thay đổi: SSU2 hiện tại chỉ chứa dữ liệu block trong phần ChaCha. Với ML-KEM, phần ChaCha cũng sẽ chứa khóa công khai PQ được mã hóa.

Nội dung thô:

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
  +                                       +
  |   ChaCha20 encrypted data (payload)   |
  +          (length varies)              +
  |  k defined in KDF for Session Request |
  +  n = 0                                +
  |  see KDF for associated data          |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+


```
Dữ liệu chưa mã hóa (thẻ xác thực Poly1305 không hiển thị):

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
Kích thước, không bao gồm IP overhead:

| Type | Type Code | X len | Msg 1 len | Msg 1 Enc len | Msg 1 Dec len | PQ key len | pl len |
|------|-----------|-------|-----------|---------------|---------------|------------|--------|
| X25519 | 4 | 32 | 80+pl | 16+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 896+pl | 832+pl | 800+pl | 800 | pl |
| MLKEM768_X25519 | 6 | 32 | 1280+pl | 1216+pl | 1184+pl | 1184 | pl |
| MLKEM1024_X25519 | 7 | n/a | too big | | | | |
Lưu ý: Mã loại chỉ dành cho sử dụng nội bộ. Các router sẽ vẫn là loại 4, và hỗ trợ sẽ được chỉ ra trong các địa chỉ router.

MTU tối thiểu cho MLKEM768_X25519: Khoảng 1316 cho IPv4 và 1336 cho IPv6.

#### SessionCreated (Type 1)

Thay đổi: SSU2 hiện tại chỉ chứa dữ liệu khối trong phần ChaCha. Với ML-KEM, phần ChaCha cũng sẽ chứa khóa công khai PQ được mã hóa.

Nội dung thô:

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
  |   ChaCha20 data (MLKEM)               |
  +   Encrypted and authenticated data    +
  |  length varies                        |
  +  k defined in KDF for Session Created +
  |  n = 0; see KDF for associated data   |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaCha20 data (payload)             |
  +   Encrypted and authenticated data    +
  |  length varies                        |
  +  k defined in KDF for Session Created +
  |  n = 0; see KDF for associated data   |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+


```
Dữ liệu không mã hóa (Poly1305 auth tag không được hiển thị):

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
Kích thước, không bao gồm IP overhead:

| Type | Type Code | Y len | Msg 2 len | Msg 2 Enc len | Msg 2 Dec len | PQ CT len | pl len |
|------|-----------|-------|-----------|---------------|---------------|-----------|--------|
| X25519 | 4 | 32 | 80+pl | 16+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 864+pl | 800+pl | 768+pl | 768 | pl |
| MLKEM768_X25519 | 6 | 32 | 1184+pl | 1118+pl | 1088+pl | 1088 | pl |
| MLKEM1024_X25519 | 7 | n/a | too big | | | | |
Lưu ý: Mã loại chỉ dành cho sử dụng nội bộ. Các router sẽ vẫn là loại 4, và hỗ trợ sẽ được chỉ ra trong các địa chỉ router.

MTU tối thiểu cho MLKEM768_X25519: Khoảng 1316 cho IPv4 và 1336 cho IPv6.

#### SessionConfirmed (Type 2)

không thay đổi

#### KDF for data phase

không thay đổi

#### Vấn đề

Các Relay block, Peer Test block và thông điệp Peer Test đều chứa chữ ký. Thật không may, chữ ký PQ lớn hơn MTU. Hiện tại không có cơ chế nào để phân mảnh các Relay block hoặc Peer Test block hoặc thông điệp qua nhiều gói UDP. Giao thức phải được mở rộng để hỗ trợ phân mảnh. Điều này sẽ được thực hiện trong một đề xuất riêng biệt sẽ được xác định sau. Cho đến khi hoàn thành, Relay và Peer Test sẽ không được hỗ trợ.

#### Tổng quan

Chúng ta có thể sử dụng nội bộ trường version và dùng 3 cho MLKEM512 và 4 cho MLKEM768.

Đối với thông điệp 1 và 2, MLKEM768 sẽ làm tăng kích thước gói tin vượt quá MTU tối thiểu 1280. Có lẽ chỉ đơn giản là không hỗ trợ nó cho kết nối đó nếu MTU quá thấp.

Đối với message 1 và 2, MLKEM1024 sẽ làm tăng kích thước gói tin vượt quá MTU tối đa 1500. Điều này sẽ yêu cầu phân mảnh message 1 và 2, và đó sẽ là một biến chứng lớn. Có thể sẽ không thực hiện.

Relay và Peer Test: Xem phía trên

### Kích thước Destination

TODO: Có cách nào hiệu quả hơn để định nghĩa signing/verification nhằm tránh sao chép signature không?

### Kích thước RouterIdent

CẦN LÀM

[IETF draft](https://datatracker.ietf.org/doc/draft-ietf-lamps-dilithium-certificates/) mục 8.1 không cho phép HashML-DSA trong chứng chỉ X.509 và không gán OID cho HashML-DSA, do tính phức tạp trong triển khai và bảo mật giảm.

Đối với chữ ký PQ-only của các file SU3, sử dụng các OID được định nghĩa trong [IETF draft](https://datatracker.ietf.org/doc/draft-ietf-lamps-dilithium-certificates/) của các biến thể non-prehash cho các certificate. Chúng tôi không định nghĩa chữ ký hybrid của các file SU3, vì chúng tôi có thể phải hash các file hai lần (mặc dù HashML-DSA và X2559 sử dụng cùng hàm hash SHA512). Ngoài ra, việc nối hai key và chữ ký trong một certificate X.509 sẽ hoàn toàn không tuân chuẩn.

Lưu ý rằng chúng tôi không cho phép ký Ed25519 đối với các file SU3, và mặc dù chúng tôi đã định nghĩa việc ký Ed25519ph, chúng tôi chưa bao giờ thống nhất về một OID cho nó, hoặc sử dụng nó.

Các sig type thông thường không được phép cho file SU3; sử dụng các biến thể ph (prehash).

### Các Mẫu Handshake

Kích thước Destination tối đa mới sẽ là 2599 (3468 trong base 64).

Cập nhật các tài liệu khác đưa ra hướng dẫn về kích thước Destination, bao gồm:

- SAMv3
- Bittorrent
- Hướng dẫn cho nhà phát triển
- Đặt tên / sổ địa chỉ / jump server
- Tài liệu khác

## Overhead Analysis

### Noise Handshake KDF

Tăng kích thước (bytes):

| Type | Pubkey (Msg 1) | Cipertext (Msg 2) |
|------|----------------|-------------------|
| MLKEM512_X25519 | +816 | +784 |
| MLKEM768_X25519 | +1200 | +1104 |
| MLKEM1024_X25519 | +1584 | +1584 |
Tốc độ:

Tốc độ theo báo cáo từ [Cloudflare](https://blog.cloudflare.com/pq-2024/):

| Type | Relative speed |
|------|----------------|
| X25519 DH/keygen | baseline |
| MLKEM512 | 2.25x faster |
| MLKEM768 | 1.5x faster |
| MLKEM1024 | 1x (same) |
| XK | 4x DH (keygen + 3 DH) |
| MLKEM512_X25519 | 4x DH + 2x PQ (keygen + enc/dec) = 4.9x DH = 22% slower |
| MLKEM768_X25519 | 4x DH + 2x PQ (keygen + enc/dec) = 5.3x DH = 32% slower |
| MLKEM1024_X25519 | 4x DH + 2x PQ (keygen + enc/dec) = 6x DH = 50% slower |
Kết quả thử nghiệm sơ bộ trong Java:

| Type | Relative DH/encaps | DH/decaps | keygen |
|------|-------------------|-----------|--------|
| X25519 | baseline | baseline | baseline |
| MLKEM512 | 29x faster | 22x faster | 17x faster |
| MLKEM768 | 17x faster | 14x faster | 9x faster |
| MLKEM1024 | 12x faster | 10x faster | 6x faster |
### Signatures

Kích thước:

Các kích thước điển hình của key, sig, RIdent, Dest hoặc mức tăng kích thước (Ed25519 được bao gồm để tham khảo) giả định loại mã hóa X25519 cho các RI. Kích thước được thêm vào cho một Router Info, LeaseSet, datagram có thể trả lời, và mỗi gói streaming (SYN và SYN ACK) được liệt kê. Các Destination và Leasesets hiện tại chứa padding lặp lại và có thể nén được trong quá trình truyền tải. Các loại mới không chứa padding và sẽ không thể nén được, dẫn đến mức tăng kích thước cao hơn nhiều khi truyền tải. Xem phần thiết kế ở trên.

| Type | Pubkey | Sig | Key+Sig | RIdent | Dest | RInfo | LS/Streaming/Datagram (each msg) |
|------|--------|-----|---------|--------|------|-------|----------------------------------|
| EdDSA_SHA512_Ed25519 | 32 | 64 | 96 | 391 | 391 | baseline | baseline |
| MLDSA44 | 1312 | 2420 | 3732 | 1351 | 1319 | +3316 | +3284 |
| MLDSA65 | 1952 | 3309 | 5261 | 1991 | 1959 | +5668 | +5636 |
| MLDSA87 | 2592 | 4627 | 7219 | 2631 | 2599 | +7072 | +7040 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 1344 | 2484 | 3828 | 1383 | 1351 | +3412 | +3380 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 1984 | 3373 | 5357 | 2023 | 1991 | +5668 | +5636 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 2624 | 4691 | 7315 | 2663 | 2631 | +7488 | +7456 |
Tốc độ:

Tốc độ như được báo cáo bởi [Cloudflare](https://blog.cloudflare.com/pq-2024/):

| Type | Relative speed sign | verify |
|------|---------------------|--------|
| EdDSA_SHA512_Ed25519 | baseline | baseline |
| MLDSA44 | 5x slower | 2x faster |
| MLDSA65 | ??? | ??? |
| MLDSA87 | ??? | ??? |
Kết quả kiểm tra sơ bộ trong Java:

| Type | Relative speed sign | verify | keygen |
|------|---------------------|--------|--------|
| EdDSA_SHA512_Ed25519 | baseline | baseline | baseline |
| MLDSA44 | 4.6x slower | 1.7x faster | 2.6x faster |
| MLDSA65 | 8.1x slower | same | 1.5x faster |
| MLDSA87 | 11.1x slower | 1.5x slower | same |
## Security Analysis

Các danh mục bảo mật NIST được tóm tắt trong [NIST presentation](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf) slide 10. Tiêu chí sơ bộ: Danh mục bảo mật NIST tối thiểu của chúng ta nên là 2 cho các giao thức lai và 3 cho PQ-only.

| Category | As Secure As |
|----------|--------------|
| 1 | AES128 |
| 2 | SHA256 |
| 3 | AES192 |
| 4 | SHA384 |
| 5 | AES256 |
### Handshakes

Đây là tất cả các giao thức lai. Có lẽ cần ưu tiên MLKEM768; MLKEM512 không đủ bảo mật.

Các danh mục bảo mật NIST [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf):

| Algorithm | Security Category |
|-----------|-------------------|
| MLKEM512 | 1 |
| MLKEM768 | 3 |
| MLKEM1024 | 5 |
### Signatures

Đề xuất này định nghĩa cả hai loại chữ ký hybrid và chỉ PQ. MLDSA44 hybrid được ưa chuộng hơn so với MLDSA65 chỉ PQ. Kích thước keys và sig cho MLDSA65 và MLDSA87 có lẽ quá lớn đối với chúng ta, ít nhất là lúc đầu.

Các danh mục bảo mật NIST [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf):

| Algorithm | Security Category |
|-----------|-------------------|
| MLDSA44 | 2 |
| MLKEM67 | 3 |
| MLKEM87 | 5 |
## Type Preferences

Mặc dù chúng tôi sẽ định nghĩa và triển khai 3 loại mã hóa và 9 loại chữ ký, chúng tôi dự định đo lường hiệu suất trong quá trình phát triển và phân tích thêm các tác động của việc tăng kích thước cấu trúc. Chúng tôi cũng sẽ tiếp tục nghiên cứu và theo dõi các phát triển trong các dự án và giao thức khác.

Sau hơn một năm phát triển, chúng tôi sẽ cố gắng lựa chọn một loại ưa thích hoặc mặc định cho mỗi trường hợp sử dụng. Việc lựa chọn sẽ yêu cầu cân nhắc giữa băng thông, CPU và mức độ bảo mật ước tính. Không phải tất cả các loại đều phù hợp hoặc được phép cho mọi trường hợp sử dụng.

Các tùy chọn sơ bộ như sau, có thể thay đổi:

Mã hóa: MLKEM768_X25519

Chữ ký: MLDSA44_EdDSA_SHA512_Ed25519

Các hạn chế sơ bộ như sau, có thể thay đổi:

Mã hóa: MLKEM1024_X25519 không được phép cho SSU2

Chữ ký: MLDSA87 và biến thể hybrid có thể quá lớn; MLDSA65 và biến thể hybrid có thể quá lớn

## Implementation Notes

### Library Support

Các thư viện Bouncycastle, BoringSSL và WolfSSL hiện đã hỗ trợ MLKEM và MLDSA. Hỗ trợ OpenSSL sẽ có trong phiên bản 3.5 của họ vào ngày 8 tháng 4 năm 2025 [OpenSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/).

Thư viện Noise của southernstorm.com được Java I2P điều chỉnh có chứa hỗ trợ sơ bộ cho hybrid handshakes, nhưng chúng tôi đã loại bỏ nó vì không sử dụng; chúng tôi sẽ phải thêm lại và cập nhật để khớp với [Noise HFS spec](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf).

### Signing Variants

Chúng tôi sẽ sử dụng biến thể ký "hedged" hoặc ngẫu nhiên hóa, không phải biến thể "determinstic", như được định nghĩa trong [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) mục 3.4. Điều này đảm bảo rằng mỗi chữ ký đều khác nhau, ngay cả khi ký trên cùng một dữ liệu, và cung cấp bảo vệ bổ sung chống lại các cuộc tấn công kênh phụ. Mặc dù [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) chỉ định rằng biến thể "hedged" là mặc định, điều này có thể đúng hoặc không đúng trong các thư viện khác nhau. Những người thực hiện phải đảm bảo rằng biến thể "hedged" được sử dụng để ký.

Chúng tôi sử dụng quy trình ký bình thường (gọi là Pure ML-DSA Signature Generation) mà mã hóa thông điệp nội bộ thành 0x00 || len(ctx) || ctx || message, trong đó ctx là một giá trị tùy chọn có kích thước 0x00..0xFF. Chúng tôi không sử dụng bất kỳ ngữ cảnh tùy chọn nào. len(ctx) == 0. Quy trình này được định nghĩa trong [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) Thuật toán 2 bước 10 và Thuật toán 3 bước 5. Lưu ý rằng một số test vector đã được xuất bản có thể yêu cầu thiết lập một chế độ trong đó thông điệp không được mã hóa.

### Reliability

Việc tăng kích thước sẽ dẫn đến phân mảnh tunnel nhiều hơn đáng kể cho việc lưu trữ NetDB, bắt tay streaming, và các thông điệp khác. Kiểm tra các thay đổi về hiệu suất và độ tin cậy.

### Structure Sizes

Tìm và kiểm tra bất kỳ mã nào giới hạn kích thước byte của router info và leaseSet.

### NetDB

Xem xét và có thể giảm số lượng LS/RI tối đa được lưu trữ trong RAM hoặc trên đĩa, để hạn chế sự gia tăng dung lượng lưu trữ. Tăng yêu cầu băng thông tối thiểu cho floodfill?

### Ratchet

#### Các Thao Tác ML-KEM Được Định Nghĩa

Việc tự động phân loại/phát hiện nhiều giao thức trên cùng một tunnel có thể thực hiện được dựa trên việc kiểm tra độ dài của message 1 (New Session Message). Lấy MLKEM512_X25519 làm ví dụ, độ dài message 1 lớn hơn 816 byte so với giao thức ratchet hiện tại, và kích thước tối thiểu của message 1 (chỉ bao gồm DateTime payload) là 919 byte. Hầu hết kích thước message 1 với ratchet hiện tại có payload nhỏ hơn 816 byte, vì vậy chúng có thể được phân loại là non-hybrid ratchet. Các message lớn có thể là POST và chúng hiếm khi xảy ra.

Vậy nên chiến lược được khuyến nghị là:

- Nếu thông điệp 1 có kích thước nhỏ hơn 919 byte, đó là giao thức ratchet hiện tại.
- Nếu thông điệp 1 có kích thước lớn hơn hoặc bằng 919 byte, có thể đó là MLKEM512_X25519.
  Hãy thử MLKEM512_X25519 trước, và nếu thất bại, hãy thử giao thức ratchet hiện tại.

Điều này sẽ cho phép chúng ta hỗ trợ hiệu quả cả ratchet tiêu chuẩn và hybrid ratchet trên cùng một đích đến, giống như trước đây chúng ta đã hỗ trợ ElGamal và ratchet trên cùng một đích đến. Do đó, chúng ta có thể di chuyển sang giao thức hybrid MLKEM nhanh hơn nhiều so với trường hợp không thể hỗ trợ dual-protocols cho cùng một đích đến, bởi vì chúng ta có thể thêm hỗ trợ MLKEM vào các đích đến hiện có.

Các kết hợp được hỗ trợ bắt buộc là:

- X25519 + MLKEM512
- X25519 + MLKEM768
- X25519 + MLKEM1024

Các kết hợp sau đây có thể phức tạp và KHÔNG bắt buộc phải được hỗ trợ, nhưng có thể có, tùy thuộc vào implementation:

- Nhiều hơn một MLKEM
- ElG + một hoặc nhiều MLKEM
- X25519 + một hoặc nhiều MLKEM
- ElG + X25519 + một hoặc nhiều MLKEM

Chúng tôi có thể không cố gắng hỗ trợ nhiều thuật toán MLKEM (ví dụ, MLKEM512_X25519 và MLKEM_768_X25519) trên cùng một destination. Chỉ chọn một thuật toán; tuy nhiên, điều đó phụ thuộc vào việc chúng tôi lựa chọn một biến thể MLKEM ưa thích, để các HTTP client tunnel có thể sử dụng. Phụ thuộc vào implementation.

Chúng tôi CÓ THỂ cố gắng hỗ trợ ba thuật toán (ví dụ X25519, MLKEM512_X25519, và MLKEM769_X25519) trên cùng một điểm đến. Việc phân loại và chiến lược thử lại có thể quá phức tạp. Cấu hình và giao diện cấu hình có thể quá phức tạp. Phụ thuộc vào việc triển khai.

Chúng tôi có lẽ sẽ KHÔNG cố gắng hỗ trợ thuật toán ElGamal và hybrid trên cùng một destination. ElGamal đã lỗi thời, và ElGamal + hybrid chỉ (không có X25519) không có nhiều ý nghĩa. Ngoài ra, các New Session Messages của ElGamal và Hybrid đều có kích thước lớn, vì vậy các chiến lược phân loại thường phải thử cả hai cách giải mã, điều này sẽ không hiệu quả. Phụ thuộc vào implementation.

Các client có thể sử dụng cùng một hoặc các X25519 static key khác nhau cho giao thức X25519 và giao thức hybrid trên cùng một tunnel, tùy thuộc vào cách triển khai.

#### KDF của Alice cho Thông điệp 1

Đặc tả ECIES cho phép Garlic Messages trong payload của New Session Message, điều này cho phép giao hàng 0-RTT của gói streaming ban đầu, thường là HTTP GET, cùng với leaseset của client. Tuy nhiên, payload của New Session Message không có forward secrecy. Vì đề xuất này đang nhấn mạnh việc tăng cường forward secrecy cho ratchet, các triển khai có thể hoặc nên trì hoãn việc bao gồm streaming payload, hoặc toàn bộ streaming message, cho đến Existing Session Message đầu tiên. Điều này sẽ làm mất khả năng giao hàng 0-RTT. Các chiến lược cũng có thể phụ thuộc vào loại traffic hoặc loại tunnel, hoặc phụ thuộc vào GET so với POST, chẳng hạn. Tùy thuộc vào triển khai.

#### Bob KDF cho Message 1

MLKEM, MLDSA, hoặc cả hai trên cùng một destination, sẽ làm tăng đáng kể kích thước của New Session Message, như đã mô tả ở trên. Điều này có thể làm giảm đáng kể độ tin cậy của việc gửi New Session Message qua các tunnel, nơi chúng phải được phân mảnh thành nhiều tunnel message 1024 byte. Thành công trong việc gửi tỷ lệ thuận với số mũ của số lượng fragment. Các implementation có thể sử dụng nhiều chiến lược khác nhau để giới hạn kích thước của message, với cái giá phải trả là việc gửi 0-RTT. Phụ thuộc vào implementation.

### Ratchet

Chúng ta có thể thiết lập MSB của khóa tạm thời (key[31] & 0x80) trong yêu cầu phiên để chỉ ra rằng đây là kết nối hybrid. Điều này sẽ cho phép chúng ta chạy cả NTCP tiêu chuẩn và NTCP hybrid trên cùng một cổng. Chỉ một biến thể hybrid được hỗ trợ và được quảng cáo trong địa chỉ router. Ví dụ, v=2,3 hoặc v=2,4 hoặc v=2,5.

Nếu chúng ta không làm như vậy, chúng ta cần địa chỉ/cổng transport khác nhau, và một tên giao thức mới như "NTCP1PQ1".

Lưu ý: Các mã loại chỉ dành cho sử dụng nội bộ. Các router sẽ vẫn là loại 4, và việc hỗ trợ sẽ được chỉ ra trong các địa chỉ router.

CẦN LÀM

### SSU2

CÓ THỂ Cần địa chỉ/cổng transport khác, nhưng hy vọng là không, chúng ta có một header với các flags cho message 1. Chúng ta có thể sử dụng nội bộ trường version và dùng 3 cho MLKEM512 và 4 cho MLKEM768. Có thể chỉ cần v=2,3,4 trong địa chỉ là đủ. Nhưng chúng ta cần các identifier cho cả hai thuật toán mới: 3a, 3b?

Kiểm tra và xác minh rằng SSU2 có thể xử lý RI được phân mảnh qua nhiều gói tin (6-8?). i2pd hiện tại chỉ hỗ trợ tối đa 2 mảnh?

Lưu ý: Mã loại chỉ dành cho sử dụng nội bộ. Các router sẽ vẫn là loại 4, và hỗ trợ sẽ được chỉ ra trong địa chỉ router.

CẦN LÀM

## Router Compatibility

### Transport Names

Chúng ta có thể sẽ không cần các tên transport mới, nếu chúng ta có thể chạy cả phiên bản tiêu chuẩn và hybrid trên cùng một cổng, với các cờ phiên bản.

Nếu chúng ta cần các tên transport mới, chúng sẽ là:

| Transport | Type |
|-----------|------|
| NTCP2PQ1 | MLKEM512_X25519 |
| NTCP2PQ2 | MLKEM768_X25519 |
| NTCP2PQ3 | MLKEM1024_X25519 |
| SSU2PQ1 | MLKEM512_X25519 |
| SSU2PQ2 | MLKEM768_X25519 |
Lưu ý rằng SSU2 không thể hỗ trợ MLKEM1024, nó quá lớn.

### Router Enc. Types

Chúng tôi có một số phương án để xem xét:

#### Bob KDF cho Message 2

Không được khuyến nghị. Chỉ sử dụng các transport mới được liệt kê ở trên phù hợp với loại router. Các router cũ không thể kết nối, xây dựng tunnel hoặc gửi tin nhắn netDb tới. Sẽ cần nhiều chu kỳ phát hành để debug và đảm bảo hỗ trợ trước khi bật mặc định. Có thể kéo dài việc triển khai thêm một năm hoặc hơn so với các phương án thay thế bên dưới.

#### Alice KDF cho Message 2

Được khuyến nghị. Vì PQ không ảnh hưởng đến khóa tĩnh X25519 hay các giao thức bắt tay N, chúng ta có thể để các router ở loại 4 và chỉ quảng cáo các transport mới. Các router cũ vẫn có thể kết nối, xây dựng tunnel qua, hoặc gửi tin nhắn netDb đến.

#### KDF cho Message 3 (chỉ XK)

Các router Loại 4 có thể quảng bá cả địa chỉ NTCP2 và NTCP2PQ*. Những địa chỉ này có thể sử dụng cùng một khóa tĩnh và các tham số khác, hoặc không. Chúng có thể sẽ cần phải ở trên các cổng khác nhau; sẽ rất khó khăn để hỗ trợ cả giao thức NTCP2 và NTCP2PQ* trên cùng một cổng, vì không có header hoặc framing nào cho phép Bob phân loại và đóng khung thông điệp Session Request đến.

Các cổng và địa chỉ riêng biệt sẽ khó khăn đối với Java nhưng đơn giản đối với i2pd.

#### KDF cho split()

Các router Type 4 có thể quảng bá cả địa chỉ SSU2 và SSU2PQ*. Với các header flag được bổ sung, Bob có thể xác định loại transport đến trong thông điệp đầu tiên. Do đó, chúng ta có thể hỗ trợ cả SSU2 và SSUPQ* trên cùng một port.

Những địa chỉ này có thể được công bố dưới dạng các địa chỉ riêng biệt (như i2pd đã làm trong các lần chuyển đổi trước đó) hoặc trong cùng một địa chỉ với tham số chỉ định hỗ trợ PQ (như Java i2p đã làm trong các lần chuyển đổi trước đó).

Nếu cùng một địa chỉ, hoặc trên cùng một cổng trong các địa chỉ khác nhau, chúng sẽ sử dụng cùng một static key và các tham số khác. Nếu ở các địa chỉ khác nhau với các cổng khác nhau, chúng có thể sử dụng cùng một static key và các tham số khác, hoặc không.

Các cổng và địa chỉ riêng biệt sẽ khó khăn đối với Java nhưng đơn giản đối với i2pd.

#### Recommendations

VIỆC CẦN LÀM

### NTCP2

#### Định danh Noise

Các router cũ sẽ xác minh RI và do đó không thể kết nối, xây dựng tunnel thông qua, hoặc gửi tin nhắn netDb tới. Sẽ mất vài chu kỳ phát hành để debug và đảm bảo hỗ trợ trước khi kích hoạt theo mặc định. Sẽ có cùng các vấn đề như việc triển khai enc. type 5/6/7; có thể kéo dài việc triển khai thêm một năm hoặc hơn so với phương án triển khai type 4 enc. type được liệt kê ở trên.

Không có lựa chọn thay thế.

### LS Enc. Types

#### 1b) Định dạng phiên mới (với binding)

Những khóa này có thể có mặt trong LS với các khóa X25519 loại 4 cũ hơn. Các router cũ sẽ bỏ qua những khóa không xác định.

Các destination có thể hỗ trợ nhiều loại key, nhưng chỉ bằng cách thực hiện giải mã thử nghiệm message 1 với từng key. Chi phí phát sinh có thể được giảm thiểu bằng cách duy trì số lượng giải mã thành công cho mỗi key, và thử key được sử dụng nhiều nhất trước tiên. Java I2P sử dụng chiến lược này cho ElGamal+X25519 trên cùng một destination.

### Dest. Sig. Types

#### 1g) Định dạng New Session Reply

Các router xác minh chữ ký leaseSet và do đó không thể kết nối hoặc nhận leaseSet cho các destination loại 12-17. Sẽ mất vài chu kỳ phát hành để debug và đảm bảo hỗ trợ trước khi bật theo mặc định.

Không có lựa chọn thay thế.

## Đặc tả kỹ thuật

Dữ liệu có giá trị nhất là lưu lượng end-to-end, được mã hóa bằng ratchet. Với tư cách là người quan sát bên ngoài giữa các hop của tunnel, dữ liệu đó được mã hóa thêm hai lần nữa, với tunnel encryption và transport encryption. Với tư cách là người quan sát bên ngoài giữa OBEP và IBGW, dữ liệu chỉ được mã hóa thêm một lần nữa, với transport encryption. Với tư cách là thành viên tham gia OBEP hoặc IBGW, ratchet là mã hóa duy nhất. Tuy nhiên, vì các tunnel là đơn hướng, việc bắt cả hai thông điệp trong quá trình bắt tay ratchet sẽ đòi hỏi các router thông đồng, trừ khi các tunnel được xây dựng với OBEP và IBGW trên cùng một router.

Mô hình đe dọa PQ đáng lo ngại nhất hiện tại là việc lưu trữ lưu lượng ngày hôm nay để giải mã nhiều năm sau này (forward secrecy). Một phương pháp kết hợp sẽ bảo vệ điều đó.

Mô hình mối đe dọa PQ về việc phá vỡ các khóa xác thực trong một khoảng thời gian hợp lý (ví dụ vài tháng) và sau đó mạo danh xác thực hoặc giải mã gần như thời gian thực, còn xa hơn nhiều? Và đó là khi chúng ta muốn di chuyển sang các khóa tĩnh PQC.

Vậy nên, mô hình đe dọa PQ sớm nhất là OBEP/IBGW lưu trữ lưu lượng để giải mã sau này. Chúng ta nên triển khai hybrid ratchet trước.

Ratchet có mức ưu tiên cao nhất. Các transport đứng thứ hai. Signature có mức ưu tiên thấp nhất.

Việc triển khai chữ ký cũng sẽ muộn hơn việc triển khai mã hóa một năm hoặc hơn, vì không thể có khả năng tương thích ngược. Ngoài ra, việc áp dụng MLDSA trong ngành sẽ được tiêu chuẩn hóa bởi CA/Browser Forum và các Certificate Authority. Các CA cần hỗ trợ hardware security module (HSM) trước tiên, điều này hiện tại chưa có sẵn [CA/Browser Forum](https://cabforum.org/2024/10/10/2024-10-10-minutes-of-the-code-signing-certificate-working-group/). Chúng tôi kỳ vọng CA/Browser Forum sẽ thúc đẩy các quyết định về lựa chọn tham số cụ thể, bao gồm việc có hỗ trợ hay yêu cầu composite signatures hay không [IETF draft](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/).

| Milestone | Target |
|-----------|--------|
| Ratchet beta | Late 2025 |
| Select best enc type | Early 2026 |
| NTCP2 beta | Early 2026 |
| SSU2 beta | Mid 2026 |
| Ratchet production | Mid 2026 |
| Ratchet default | Late 2026 |
| Signature beta | Late 2026 |
| NTCP2 production | Late 2026 |
| SSU2 production | Early 2027 |
| Select best sig type | Early 2027 |
| NTCP2 default | Early 2027 |
| SSU2 default | Mid 2027 |
| Signature production | Mid 2027 |
## Migration

Nếu chúng ta không thể hỗ trợ cả giao thức ratchet cũ và mới trên cùng các tunnel, việc di chuyển sẽ khó khăn hơn nhiều.

Chúng ta sẽ có thể thử cái này-rồi-cái kia, như chúng ta đã làm với X25519, để được chứng minh.

## Issues

- Lựa chọn Noise Hash - tiếp tục với SHA256 hay nâng cấp?
  SHA256 nên tốt trong 20-30 năm nữa, không bị đe dọa bởi PQ,
  Xem [NIST presentation](https://csrc.nist.gov/csrc/media/Presentations/2022/update-on-post-quantum-encryption-and-cryptographi/Day%202%20-%20230pm%20Chen%20PQC%20ISPAB.pdf) và [NIST presentation](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf).
  Nếu SHA256 bị phá thì chúng ta có những vấn đề tồi tệ hơn (netdb).
- NTCP2 cổng riêng biệt, địa chỉ router riêng biệt
- SSU2 relay / peer test
- Trường phiên bản SSU2
- Phiên bản địa chỉ router SSU2
