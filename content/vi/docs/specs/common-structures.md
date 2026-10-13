---
title: "Đặc tả cấu trúc chung"
description: "Các kiểu dữ liệu chung cho tất cả giao thức I2P"
slug: "common-structures"
aliases:
  - "/docs/specs/common-structures"
  - "/docs/specs/common-structures/"
category: "Thiết kế"
lastUpdated: "2026-10"
accurateFor: "0.9.71"
---

Tài liệu này mô tả một số kiểu dữ liệu chung cho tất cả các giao thức I2P, như [I2NP](/docs/specs/i2np/), [I2CP](/docs/specs/i2cp/), [SSU](/docs/legacy/ssu/), v.v.

## Đặc tả kiểu chung

### Số nguyên

#### Mô tả

Đại diện cho một số nguyên không âm.

#### Mục lục

1 đến 8 byte theo thứ tự byte mạng (big endian) biểu diễn một số nguyên không dấu.

### Ngày

#### Mô tả

Số mili giây kể từ nửa đêm ngày 1 tháng 1 năm 1970 theo múi giờ GMT. Nếu số này là 0, ngày tháng không được xác định hoặc null.

#### Nội dung

8 byte [Integer](#integer)

### Chuỗi

#### Mô tả

Biểu diễn một chuỗi được mã hóa UTF-8.

#### Mục lục

1 hoặc nhiều byte trong đó byte đầu tiên là số lượng byte (không phải ký tự!) trong chuỗi và 0-255 byte còn lại là mảng ký tự được mã hóa UTF-8 không kết thúc bằng null. Giới hạn độ dài là 255 byte (không phải ký tự). Độ dài có thể là 0.

### PublicKey

#### Mô tả

Cấu trúc này được sử dụng trong mã hóa ElGamal hoặc các phương pháp mã hóa bất đối xứng khác, chỉ đại diện cho số mũ, không phải các số nguyên tố, vì chúng là hằng số và được định nghĩa trong đặc tả mật mã [ELGAMAL](/docs/specs/cryptography/#elgamal-legacy). Các phương pháp mã hóa khác đang trong quá trình được định nghĩa, xem bảng bên dưới.

#### Nội dung

Loại khóa và độ dài được suy ra từ ngữ cảnh hoặc được chỉ định trong Key Certificate của một Destination hoặc RouterInfo, hoặc các trường trong [LeaseSet2](#leaseset2) hoặc cấu trúc dữ liệu khác. Loại mặc định là ElGamal. Kể từ phiên bản 0.9.38, các loại khác có thể được hỗ trợ, tùy thuộc vào ngữ cảnh. Các khóa được biểu diễn theo thứ tự big-endian trừ khi có ghi chú khác.

Khóa X25519 được hỗ trợ trong Destinations và LeaseSet2 kể từ phiên bản 0.9.44. Khóa X25519 được hỗ trợ trong RouterIdentities kể từ phiên bản 0.9.48.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Length (bytes)</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ElGamal</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">256</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated for Router Identities as of 0.9.58; use for Destinations, as the public key field is unused there; discouraged for leasesets</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">P256</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">64</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">TBD</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see proposal 145</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">P384</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">96</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">TBD</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see proposal 145</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">P521</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">132</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">TBD</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see proposal 145</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.38</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Little-endian. See <a href="/docs/specs/ecies/">ECIES</a> and <a href="/docs/specs/ecies-routers/">ECIES-ROUTERS</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM512_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">See <a href="/docs/specs/ecies-hybrid/">ECIES-HYBRID</a>, for Leasesets only, not for RIs or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM768_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">See <a href="/docs/specs/ecies-hybrid/">ECIES-HYBRID</a>, for Leasesets only, not for RIs or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM1024_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">See <a href="/docs/specs/ecies-hybrid/">ECIES-HYBRID</a>, for Leasesets only, not for RIs or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM512</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">800</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">See <a href="/docs/specs/ecies-hybrid/">ECIES-HYBRID</a>, for handshakes only, not for Leasesets, RIs or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM768</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1184</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">See <a href="/docs/specs/ecies-hybrid/">ECIES-HYBRID</a>, for handshakes only, not for Leasesets, RIs or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM1024</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1568</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">See <a href="/docs/specs/ecies-hybrid/">ECIES-HYBRID</a>, for handshakes only, not for Leasesets, RIs or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM512_CT</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">768</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">See <a href="/docs/specs/ecies-hybrid/">ECIES-HYBRID</a>, for handshakes only, not for Leasesets, RIs or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM768_CT</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1088</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">See <a href="/docs/specs/ecies-hybrid/">ECIES-HYBRID</a>, for handshakes only, not for Leasesets, RIs or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM1024_CT</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1568</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">See <a href="/docs/specs/ecies-hybrid/">ECIES-HYBRID</a>, for handshakes only, not for Leasesets, RIs or Destinations</td>
    </tr>
  </tbody>
</table>
JavaDoc: [net.i2p.data.PublicKey](http://docs.i2p-projekt.de/net/i2p/data/PublicKey.html)

### PrivateKey

#### Mô tả

Cấu trúc này được sử dụng trong ElGamal hoặc các phương pháp giải mã bất đối xứng khác, chỉ đại diện cho số mũ, không phải các số nguyên tố vốn là hằng số và được định nghĩa trong đặc tả mật mã học [ELGAMAL](/docs/specs/cryptography/#elgamal-legacy). Các sơ đồ mã hóa khác đang trong quá trình được định nghĩa, xem bảng dưới đây.

#### Nội dung

Loại khóa và độ dài được suy ra từ ngữ cảnh hoặc được lưu trữ riêng biệt trong một cấu trúc dữ liệu hoặc tệp khóa riêng tư. Loại mặc định là ElGamal. Kể từ phiên bản 0.9.38, các loại khác có thể được hỗ trợ, tùy thuộc vào ngữ cảnh. Các khóa sử dụng định dạng big-endian trừ khi có ghi chú khác.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Length (bytes)</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ElGamal</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">256</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated for Router Identities as of 0.9.58; use for Destinations, as the public key field is unused there; discouraged for leasesets</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">P256</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">TBD</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see proposal 145</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">P384</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">48</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">TBD</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see proposal 145</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">P521</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">66</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">TBD</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see proposal 145</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.38</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Little-endian. See <a href="/docs/specs/ecies/">ECIES</a> and <a href="/docs/specs/ecies-routers/">ECIES-ROUTERS</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM512_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">See <a href="/docs/specs/ecies-hybrid/">ECIES-HYBRID</a>, for Leasesets only, not for RIs or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM768_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">See <a href="/docs/specs/ecies-hybrid/">ECIES-HYBRID</a>, for Leasesets only, not for RIs or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM1024_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">See <a href="/docs/specs/ecies-hybrid/">ECIES-HYBRID</a>, for Leasesets only, not for RIs or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM512</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1632</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">See <a href="/docs/specs/ecies-hybrid/">ECIES-HYBRID</a>, for handshakes only, not for Leasesets, RIs or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM768</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2400</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">See <a href="/docs/specs/ecies-hybrid/">ECIES-HYBRID</a>, for handshakes only, not for Leasesets, RIs or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM1024</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">3168</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">See <a href="/docs/specs/ecies-hybrid/">ECIES-HYBRID</a>, for handshakes only, not for Leasesets, RIs or Destinations</td>
    </tr>
  </tbody>
</table>
JavaDoc: [net.i2p.data.PrivateKey](http://docs.i2p-projekt.de/net/i2p/data/PrivateKey.html)

### SessionKey

#### Mô tả

Cấu trúc này được sử dụng cho mã hóa và giải mã đối xứng AES256.

#### Nội dung

32 byte

JavaDoc: [net.i2p.data.SessionKey](http://docs.i2p-projekt.de/net/i2p/data/SessionKey.html)

### SigningPublicKey

#### Mô tả

Cấu trúc này được sử dụng để xác minh chữ ký.

#### Mục lục

Loại khóa và độ dài được suy ra từ ngữ cảnh hoặc được chỉ định trong Key Certificate của một Destination. Loại mặc định là DSA_SHA1. Kể từ phiên bản 0.9.12, các loại khác có thể được hỗ trợ, tùy thuộc vào ngữ cảnh.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Length (bytes)</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">DSA_SHA1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated for Router Identities as of 09.58; discouraged for Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECDSA_SHA256_P256</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">64</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated Older Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECDSA_SHA384_P384</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">96</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated Rarely used for Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECDSA_SHA512_P521</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">132</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated Rarely used for Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RSA_SHA256_2048</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">256</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated Offline signing, never used for Router Identities or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RSA_SHA384_3072</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">384</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated Offline signing, never used for Router Identities or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RSA_SHA512_4096</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">512</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Offline signing, never used for Router Identities or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">EdDSA_SHA512_Ed25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.15</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Recent Router Identities and Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">EdDSA_SHA512_Ed25519ph</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.25</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Offline signing, never used for Router Identities or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RedDSA_SHA512_Ed25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.39</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">For Destinations and encrypted leasesets only, never used for Router Identities</td>
    </tr>
  </tbody>
</table>
#### Ghi chú

* Khi một khóa được tạo thành từ hai phần tử (ví dụ các điểm X,Y), nó được tuần tự hóa bằng cách đệm mỗi phần tử đến độ dài/2 với các số 0 đứng đầu nếu cần thiết.

* Tất cả các kiểu dữ liệu đều theo định dạng Big Endian, ngoại trừ EdDSA và RedDSA, được lưu trữ và truyền tải theo định dạng Little Endian.

JavaDoc: [net.i2p.data.SigningPublicKey](http://docs.i2p-projekt.de/net/i2p/data/SigningPublicKey.html)

### SigningPrivateKey

#### Mô tả

Cấu trúc này được sử dụng để tạo chữ ký.

#### Mục lục

Loại và độ dài khóa được chỉ định khi tạo. Loại mặc định là DSA_SHA1. Từ phiên bản 0.9.12, các loại khác có thể được hỗ trợ, tùy thuộc vào ngữ cảnh.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Length (bytes)</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">DSA_SHA1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">20</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated for Router Identities as of 09.58; discouraged for Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECDSA_SHA256_P256</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated Older Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECDSA_SHA384_P384</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">48</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated Rarely used for Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECDSA_SHA512_P521</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">66</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated Rarely used for Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RSA_SHA256_2048</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">512</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated Offline signing, never used for Router Identities or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RSA_SHA384_3072</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">768</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated Offline signing, never used for Router Identities or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RSA_SHA512_4096</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1024</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Offline signing, never used for Router Identities or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">EdDSA_SHA512_Ed25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.15</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Recent Router Identities and Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">EdDSA_SHA512_Ed25519ph</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.25</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Offline signing, never used for Router Identities or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RedDSA_SHA512_Ed25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.39</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">For Destinations and encrypted leasesets only, never used for Router Identities</td>
    </tr>
  </tbody>
</table>
#### Ghi chú

* Khi một key được tạo thành từ hai phần tử (ví dụ các điểm X,Y), nó được tuần tự hóa bằng cách đệm mỗi phần tử đến độ dài length/2 với các số 0 đứng đầu nếu cần thiết.

* Tất cả các kiểu dữ liệu đều sử dụng Big Endian, ngoại trừ EdDSA và RedDSA, được lưu trữ và truyền tải theo định dạng Little Endian.

JavaDoc: [net.i2p.data.SigningPrivateKey](http://docs.i2p-projekt.de/net/i2p/data/SigningPrivateKey.html)

### Chữ ký

#### Mô tả

Cấu trúc này đại diện cho chữ ký của một số dữ liệu.

#### Mục lục

Loại chữ ký và độ dài được suy ra từ loại khóa được sử dụng. Loại mặc định là DSA_SHA1. Kể từ phiên bản 0.9.12, các loại khác có thể được hỗ trợ, tùy thuộc vào ngữ cảnh.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Length (bytes)</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">DSA_SHA1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">40</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated for Router Identities as of 09.58; discouraged for Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECDSA_SHA256_P256</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">64</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated Older Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECDSA_SHA384_P384</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">96</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated Rarely used for Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECDSA_SHA512_P521</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">132</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated Rarely used for Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RSA_SHA256_2048</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">256</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated Offline signing, never used for Router Identities or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RSA_SHA384_3072</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">384</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated Offline signing, never used for Router Identities or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RSA_SHA512_4096</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">512</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Offline signing, never used for Router Identities or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">EdDSA_SHA512_Ed25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">64</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.15</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Recent Router Identities and Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">EdDSA_SHA512_Ed25519ph</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">64</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.25</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Offline signing, never used for Router Identities or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RedDSA_SHA512_Ed25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">64</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.39</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">For Destinations and encrypted leasesets only, never used for Router Identities</td>
    </tr>
  </tbody>
</table>
#### Ghi chú

* Khi một chữ ký được cấu thành từ hai phần tử (ví dụ các giá trị R,S), nó được tuần tự hóa bằng cách đệm mỗi phần tử đến độ dài/2 với các số 0 đứng đầu nếu cần thiết.

* Tất cả các kiểu dữ liệu đều theo định dạng Big Endian, trừ EdDSA và RedDSA được lưu trữ và truyền tải theo định dạng Little Endian.

JavaDoc: [net.i2p.data.Signature](http://docs.i2p-projekt.de/net/i2p/data/Signature.html)

### Hash

#### Mô tả

Đại diện cho SHA256 của một số dữ liệu.

#### Mục lục

32 byte

JavaDoc: [net.i2p.data.Hash](http://docs.i2p-projekt.de/net/i2p/data/Hash.html)

### Thẻ phiên

Lưu ý: Session Tags cho các đích ECIES-X25519 (ratchet) và các router ECIES-X25519 có độ dài 8 byte. Xem [ECIES](/docs/specs/ecies/) và [ECIES-ROUTERS](/docs/specs/ecies-routers/).

#### Mô tả

Một số ngẫu nhiên

#### Mục lục

32 byte

JavaDoc: [net.i2p.data.SessionTag](http://docs.i2p-projekt.de/net/i2p/data/SessionTag.html)

### TunnelId

#### Mô tả

Định nghĩa một định danh duy nhất cho mỗi router trong một tunnel. Tunnel ID thường lớn hơn không; đừng sử dụng giá trị bằng không trừ trong các trường hợp đặc biệt.

#### Mục lục

4 byte [Integer](#integer)

JavaDoc: [net.i2p.data.TunnelId](http://docs.i2p-projekt.de/net/i2p/data/TunnelId.html)

### Chứng chỉ

#### Mô tả

Chứng chỉ là một thùng chứa cho các biên lai hoặc bằng chứng công việc khác nhau được sử dụng trên toàn mạng I2P.

#### Nội dung

1 byte [Integer](#integer) chỉ định loại chứng chỉ, theo sau là 2 byte [Integer](#integer) chỉ định kích thước của payload chứng chỉ, sau đó là số byte tương ứng.

```
+----+----+----+----+----+-/
|type| length  | payload
+----+----+----+----+----+-/

type :: Integer
        length -> 1 byte

length :: Integer
          length -> 2 bytes

payload :: data
           length -> $length bytes
```
#### Ghi chú

* Đối với [Router Identities](#routeridentity), Certificate luôn là NULL cho đến phiên bản
  0.9.15. Từ phiên bản 0.9.16, Key Certificate được sử dụng để chỉ định các
  loại khóa. Từ phiên bản 0.9.48, các loại khóa công khai mã hóa X25519
  được cho phép. Xem bên dưới.

* Đối với [Garlic Cloves](/docs/specs/i2np/#struct-garlicclove), Certificate luôn là NULL, hiện tại không có loại nào khác được triển khai.

* Đối với [Garlic Messages](/docs/specs/i2np/#msg-garlic), Certificate luôn là NULL, hiện tại không có triển khai nào khác.

* Đối với [Destinations](#destination), Certificate có thể khác NULL. Từ phiên bản 0.9.12, Key Certificate có thể được sử dụng để chỉ định loại signing public key. Xem bên dưới.

* Người triển khai được khuyến cáo cấm dữ liệu thừa trong Certificates.
  Độ dài phù hợp cho mỗi loại certificate nên được thực thi.

#### Loại Chứng chỉ

Các loại chứng chỉ sau đây được định nghĩa:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type Code</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Payload Length</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Total Length</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Null</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">HashCash</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">varies</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">varies</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated, unused. Payload contains an ASCII colon-separated hashcash string.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Hidden</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated, unused. Hidden routers generally do not announce that they are hidden.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Signed</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">40 or 72</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">43 or 75</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated, unused. Payload contains a 40-byte DSA signature, optionally followed by the 32-byte Hash of the signing Destination.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Multiple</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">varies</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">varies</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated, unused. Payload contains multiple certificates.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Key</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4+</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7+</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Since 0.9.12. See below for details.</td>
    </tr>
  </tbody>
</table>
#### Chứng chỉ khóa

Chứng chỉ khóa được giới thiệu trong phiên bản 0.9.12. Trước phiên bản đó, tất cả PublicKey đều là khóa ElGamal 256-byte, và tất cả SigningPublicKey đều là khóa DSA-SHA1 128-byte. Chứng chỉ khóa cung cấp một cơ chế để chỉ định loại PublicKey và SigningPublicKey trong Destination hoặc RouterIdentity, và để đóng gói bất kỳ dữ liệu khóa nào vượt quá độ dài tiêu chuẩn.

Bằng cách duy trì chính xác 384 byte trước certificate và đặt bất kỳ dữ liệu khóa dư thừa nào bên trong certificate, chúng ta duy trì tính tương thích cho bất kỳ phần mềm nào phân tích cú pháp Destinations và Router Identities.

Tải trọng chứng chỉ khóa chứa:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Data</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Length</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Signing Public Key Type (<a href="#integer">Integer</a>)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Crypto Public Key Type (<a href="#integer">Integer</a>)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Excess Signing Public Key Data</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0+</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Excess Crypto Public Key Data</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0+</td>
    </tr>
  </tbody>
</table>
Cảnh báo: Thứ tự loại khóa ngược với những gì bạn có thể mong đợi; Loại Khóa Công Khai Ký được đặt trước.

Các loại Signing Public Key đã được định nghĩa là:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type Code</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Total Public Key Length</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">DSA_SHA1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated for Router Identities as of 0.9.58; discouraged for Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECDSA_SHA256_P256</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">64</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated Older Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECDSA_SHA384_P384</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">96</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated Rarely if ever used for Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECDSA_SHA512_P521</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">132</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated Rarely if ever used for Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RSA_SHA256_2048</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">256</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated Offline only; never used in Key Certificates for Router Identities or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RSA_SHA384_3072</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">384</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated Offline only; never used in Key Certificates for Router Identities or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RSA_SHA512_4096</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">6</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">512</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Offline only; never used in Key Certificates for Router Identities or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">EdDSA_SHA512_Ed25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.15</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Recent Router Identities and Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">EdDSA_SHA512_Ed25519ph</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">8</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.25</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Offline only; never used in Key Certificates for Router Identities or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">reserved (GOST)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">9</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">64</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see <a href="/proposals/134-gost/">Prop134</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">reserved (GOST)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">10</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see <a href="/proposals/134-gost/">Prop134</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RedDSA_SHA512_Ed25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">11</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.39</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">For Destinations and encrypted leasesets only; never used for Router Identities</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">reserved (MLDSA)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see <a href="/proposals/169-pq-crypto/">Prop169</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">reserved (MLDSA)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">13</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see <a href="/proposals/169-pq-crypto/">Prop169</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">reserved (MLDSA)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">14</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see <a href="/proposals/169-pq-crypto/">Prop169</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">reserved (MLDSA)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">15</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see <a href="/proposals/169-pq-crypto/">Prop169</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">reserved (MLDSA)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">16</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see <a href="/proposals/169-pq-crypto/">Prop169</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">reserved (MLDSA)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">17</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see <a href="/proposals/169-pq-crypto/">Prop169</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">reserved (MLDSA)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">18</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see <a href="/proposals/169-pq-crypto/">Prop169</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">reserved (MLDSA)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">19</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see <a href="/proposals/169-pq-crypto/">Prop169</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">reserved (MLDSA)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">20</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see <a href="/proposals/169-pq-crypto/">Prop169</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">reserved</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">65280-65534</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved for experimental use</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">reserved</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">65535</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved for future expansion</td>
    </tr>
  </tbody>
</table>
Các loại Crypto Public Key được định nghĩa là:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type Code</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Total Public Key Length</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ElGamal</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">256</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated for Router Identities as of 0.9.58; use for Destinations, as the public key field is unused there</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">P256</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">64</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see proposal 145</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">P384</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">96</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see proposal 145</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">P521</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">132</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see proposal 145</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.38</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">See <a href="/docs/specs/ecies/">ECIES</a> and proposal 156</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM512_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">See <a href="/docs/specs/ecies-hybrid/">ECIES-HYBRID</a>, for Leasesets only, not for RIs or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM768_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">6</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">See <a href="/docs/specs/ecies-hybrid/">ECIES-HYBRID</a>, for Leasesets only, not for RIs or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM1024_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">See <a href="/docs/specs/ecies-hybrid/">ECIES-HYBRID</a>, for Leasesets only, not for RIs or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">reserved (NONE)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">255</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see <a href="/proposals/169-pq-crypto/">Prop169</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">reserved</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">65280-65534</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved for experimental use</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">reserved</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">65535</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved for future expansion</td>
    </tr>
  </tbody>
</table>
Khi Key Certificate không có mặt, 384 byte trước đó trong Destination hoặc RouterIdentity được định nghĩa là 256-byte ElGamal PublicKey tiếp theo là 128-byte DSA-SHA1 SigningPublicKey. Khi Key Certificate có mặt, 384 byte trước đó được định nghĩa lại như sau:

* Hoàn chỉnh hoặc phần đầu tiên của Crypto Public Key

* Padding ngẫu nhiên nếu tổng độ dài của hai khóa ít hơn 384 byte

* Toàn bộ hoặc phần đầu của Signing Public Key

Crypto Public Key được căn chỉnh ở đầu và Signing Public Key được căn chỉnh ở cuối. Phần đệm (nếu có) nằm ở giữa. Độ dài và ranh giới của dữ liệu khóa ban đầu, phần đệm, và các phần dữ liệu khóa dư thừa trong certificates không được chỉ định rõ ràng, mà được suy ra từ độ dài của các loại khóa đã chỉ định. Nếu tổng độ dài của Crypto và Signing Public Keys vượt quá 384 byte, phần còn lại sẽ được chứa trong Key Certificate. Nếu độ dài Crypto Public Key không phải là 256 byte, phương pháp xác định ranh giới giữa hai khóa sẽ được chỉ định trong phiên bản tương lai của tài liệu này.

Các ví dụ về bố cục sử dụng ElGamal Crypto Public Key và loại Signing Public Key được chỉ định:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Signing Key Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Padding Length</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Excess Signing Key Data in Cert</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">DSA_SHA1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECDSA_SHA256_P256</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">64</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECDSA_SHA384_P384</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECDSA_SHA512_P521</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RSA_SHA256_2048</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RSA_SHA384_3072</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">256</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RSA_SHA512_4096</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">384</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">EdDSA_SHA512_Ed25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">96</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">EdDSA_SHA512_Ed25519ph</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">96</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0</td>
    </tr>
  </tbody>
</table>
JavaDoc: [net.i2p.data.Certificate](http://docs.i2p-projekt.de/net/i2p/data/Certificate.html)

#### Ghi chú

* Các nhà phát triển được khuyến cáo nên cấm dữ liệu thừa trong Key Certificates.
  Độ dài phù hợp cho mỗi loại certificate nên được thực thi.

* Chứng chỉ KEY với loại 0,0 (ElGamal,DSA_SHA1) được cho phép nhưng không được khuyến khích.
  Nó chưa được kiểm tra kỹ lưỡng và có thể gây ra vấn đề trong một số triển khai.
  Sử dụng chứng chỉ NULL trong biểu diễn chuẩn của một
  Destination hoặc RouterIdentity (ElGamal,DSA_SHA1), điều này sẽ ngắn hơn 4 byte
  so với việc sử dụng chứng chỉ KEY.

### Ánh xạ

#### Mô tả

Một tập hợp các ánh xạ khóa/giá trị hoặc thuộc tính

#### Mục lục

Một số nguyên kích thước 2-byte theo sau bởi một chuỗi các cặp String=String;.

CẢNH BÁO: Hầu hết các sử dụng Mapping đều nằm trong các cấu trúc đã ký, nơi mà các mục Mapping phải được sắp xếp theo khóa, để chữ ký không thể thay đổi. Việc không sắp xếp theo khóa sẽ dẫn đến lỗi chữ ký!

```bytefield
size       | 4 | red    | Integer, 2 bytes
key_string | 4 | blue   | String (len + data)
val_string | 8 | green  | String (len + data)
;          | 8 | yellow | :: A single byte containing ';'
```
<details class="content-section">
<summary>View original ASCII diagram</summary>

```
+----+----+----+----+----+----+----+----+
|  size   | key_string (len + data)| =  |
+----+----+----+----+----+----+----+----+
| val_string (len + data)     | ;  | ...
+----+----+----+----+----+----+----+
```
</details>
#### Ghi chú

* Việc mã hóa không tối ưu - chúng ta cần các ký tự '=' và ';', hoặc độ dài chuỗi, nhưng không cần cả hai

#### Mô tả

* Một số tài liệu nói rằng các chuỗi có thể không bao gồm '=' hoặc ';' nhưng mã hóa này hỗ trợ chúng

* Chuỗi được định nghĩa là UTF-8 nhưng trong triển khai hiện tại, I2CP sử dụng UTF-8 còn I2NP thì không. Ví dụ, các chuỗi UTF-8 trong ánh xạ tùy chọn RouterInfo trong một I2NP Database Store Message sẽ bị hỏng.

* Mã hóa cho phép các khóa trùng lặp, tuy nhiên trong bất kỳ trường hợp sử dụng nào mà ánh xạ được ký, các khóa trùng lặp có thể gây ra lỗi chữ ký.

* Các ánh xạ chứa trong thông điệp I2NP (ví dụ: trong RouterAddress hoặc RouterInfo)
  phải được sắp xếp theo khóa để chữ ký sẽ không thay đổi. Không cho phép khóa
  trùng lặp.

* Các ánh xạ có trong [I2CP SessionConfig](/docs/specs/i2cp/#struct-sessionconfig) phải được sắp xếp theo khóa để chữ ký sẽ không thay đổi. Không cho phép các khóa trùng lặp.

* Phương thức sắp xếp được định nghĩa như trong Java String.compareTo(), sử dụng giá trị Unicode của các ký tự.

* Mặc dù phụ thuộc vào ứng dụng, các khóa và giá trị thường phân biệt chữ hoa chữ thường.

* Giới hạn độ dài chuỗi key và value là 255 byte (không phải ký tự) mỗi cái, cộng
  thêm byte độ dài. Byte độ dài có thể bằng 0.

* Giới hạn tổng chiều dài là 65535 byte, cộng với trường kích thước 2 byte, tức là tổng cộng 65537 byte.

* Một Router Identity với loại mã hóa X25519 và loại chữ ký Ed25519
  sẽ chứa 10 bản sao (320 byte) dữ liệu ngẫu nhiên, tiết kiệm được khoảng 288 byte khi nén.

JavaDoc: [net.i2p.data.DataHelper](http://docs.i2p-projekt.de/net/i2p/data/DataHelper.html)

## Đặc tả cấu trúc chung

### KeysAndCert

#### Nội dung

Một khóa công khai mã hóa, một khóa công khai ký số và một chứng chỉ, được sử dụng như một RouterIdentity hoặc một Destination.

#### Hướng dẫn Tạo Padding

Một [PublicKey](#publickey) theo sau bởi một [SigningPublicKey](#signingpublickey) và sau đó là một [Certificate](#certificate).

```bytefield
public_key          | 8 | blue   | PublicKey (partial or full), 256 bytes or as specified in key cert

padding (optional)  | 8 | yellow | random data, pub + pad + sig == 384 bytes

signing_key         | 8 | green  | SigningPublicKey (partial or full), 128 bytes or as specified

certificate         | 3 | purple | Certificate, >= 3 bytes
= total length: 387+ bytes
```
<details class="content-section">
<summary>View original ASCII diagram</summary>

```
+----+----+----+----+----+----+----+----+
| public_key                            |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| padding (optional)                    |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| signing_key                           |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| certificate                           |
+----+----+----+-/

public_key :: `PublicKey` (partial or full)
              length -> 256 bytes or as specified in key certificate

padding :: random data
           length -> 0 bytes or as specified in key certificate
           public_key length + padding length + signing_key length == 384 bytes

signing__key :: `SigningPublicKey` (partial or full)
                length -> 128 bytes or as specified in key certificate

certificate :: `Certificate`
               length -> >= 3 bytes

total length: 387+ bytes
```

</details>
#### Ghi chú

Những hướng dẫn này được đề xuất trong Đề xuất 161 và được triển khai trong phiên bản API 0.9.57. Những hướng dẫn này tương thích ngược với tất cả các phiên bản từ 0.6 (2005). Xem Đề xuất 161 để biết thêm thông tin cơ bản và chi tiết.

Đối với bất kỳ tổ hợp loại khóa nào hiện đang được sử dụng khác với ElGamal + DSA-SHA1, sẽ có padding. Ngoài ra, đối với các destination, trường public key 256-byte đã không được sử dụng kể từ phiên bản 0.6 (2005).

Các nhà phát triển nên tạo ra dữ liệu ngẫu nhiên cho các khóa công khai Destination và phần đệm cho Destination và Router Identity, sao cho nó có thể nén được trong các giao thức I2P khác nhau trong khi vẫn đảm bảo tính bảo mật, và không làm cho các biểu diễn Base 64 có vẻ bị hỏng hoặc không an toàn. Điều này cung cấp hầu hết các lợi ích của việc loại bỏ các trường đệm mà không cần thay đổi giao thức một cách đột ngột.

Nói một cách chính xác, chỉ riêng signing public key 32-byte (trong cả Destinations và Router Identities) và encryption public key 32-byte (chỉ trong Router Identities) là một số ngẫu nhiên cung cấp tất cả entropy cần thiết để các hash SHA-256 của những cấu trúc này có độ mạnh mã hóa và được phân bố ngẫu nhiên trong DHT của netDb.

Tuy nhiên, để đảm bảo an toàn tối đa, chúng tôi khuyến nghị sử dụng tối thiểu 32 byte dữ liệu ngẫu nhiên trong trường ElG public key và padding. Ngoài ra, nếu các trường đều bằng không, các destination Base 64 sẽ chứa chuỗi dài các ký tự AAAA, điều này có thể gây lo lắng hoặc nhầm lẫn cho người dùng.

Lặp lại 32 byte dữ liệu ngẫu nhiên khi cần thiết để cấu trúc KeysAndCert đầy đủ có thể nén cao trong các giao thức I2P như I2NP Database Store Message, Streaming SYN, SSU2 handshake và repliable Datagrams.

Ví dụ:

* Một Destination với loại chữ ký Ed25519
  sẽ chứa 11 bản sao (352 byte) của dữ liệu ngẫu nhiên, tiết kiệm được khoảng 320 byte khi nén.

* Đừng cho rằng những thứ này luôn có độ dài 387 byte! Chúng có độ dài 387 byte cộng với độ dài certificate được chỉ định tại byte 385-386, có thể khác không.

Các implementation tất nhiên phải lưu trữ cấu trúc đầy đủ 387+ byte vì hash SHA-256 của cấu trúc bao phủ toàn bộ nội dung.

#### Mô tả

* Từ phiên bản 0.9.12, nếu chứng chỉ là Key Certificate, ranh giới của các trường khóa có thể thay đổi. Xem phần Key Certificate ở trên để biết chi tiết.

* Crypto Public Key được căn chỉnh ở đầu và Signing Public Key được căn chỉnh ở cuối. Phần đệm (nếu có) nằm ở giữa.

* Chứng chỉ cho một RouterIdentity luôn luôn là NULL cho đến phiên bản 0.9.12.

JavaDoc: [net.i2p.data.KeysAndCert](http://docs.i2p-projekt.de/net/i2p/data/KeysAndCert.html)

### RouterIdentity

#### Nội dung

Định nghĩa cách để xác định duy nhất một router cụ thể

#### Ghi chú

Tương tự với KeysAndCert.

Xem [KeysAndCert](#keysandcert) để biết hướng dẫn về việc tạo dữ liệu ngẫu nhiên cho trường padding.

#### Mô tả

* Đừng giả định rằng chúng luôn có 387 bytes! Chúng có 387 bytes cộng với độ dài certificate được chỉ định tại bytes 385-386, có thể khác không.

* Kể từ phiên bản 0.9.12, nếu chứng chỉ là Key Certificate, các ranh giới của các trường khóa có thể thay đổi. Xem phần Key Certificate ở trên để biết chi tiết.

* Crypto Public Key được căn chỉnh ở đầu và Signing Public Key được căn chỉnh ở cuối. Phần đệm (nếu có) nằm ở giữa.

* RouterIdentities với key certificate và public key ECIES_X25519
  được hỗ trợ từ phiên bản 0.9.48.
  Trước đó, tất cả RouterIdentities đều là ElGamal.

* Public key của destination đã được sử dụng cho mã hóa i2cp-to-i2cp cũ
  đã bị vô hiệu hóa trong phiên bản 0.6 (2005), hiện tại không được sử dụng ngoại trừ
  cho IV để mã hóa LeaseSet, điều này đã lỗi thời. Thay vào đó, public key trong
  LeaseSet được sử dụng.

JavaDoc: [net.i2p.data.router.RouterIdentity](http://docs.i2p-projekt.de/net/i2p/data/router/RouterIdentity.html)

### Điểm đến

#### Nội dung

Destination định nghĩa một điểm cuối cụ thể mà các thông điệp có thể được chuyển đến để giao hàng an toàn.

#### Ghi chú

Giống hệt với [KeysAndCert](#keysandcert), ngoại trừ việc public key không bao giờ được sử dụng và có thể chứa dữ liệu ngẫu nhiên thay vì một ElGamal Public Key hợp lệ.

Xem [KeysAndCert](#keysandcert) để có hướng dẫn về việc tạo dữ liệu ngẫu nhiên cho các trường public key và padding.

#### Mô tả

* Đừng cho rằng chúng luôn có độ dài 387 bytes! Chúng có độ dài 387 bytes cộng với độ dài certificate được chỉ định tại bytes 385-386, có thể khác không.

* Kể từ phiên bản 0.9.12, nếu chứng chỉ là Key Certificate, ranh giới của các trường khóa có thể thay đổi. Xem phần Key Certificate ở trên để biết chi tiết.

* Crypto Public Key được căn chỉnh ở đầu và Signing Public Key được căn chỉnh ở cuối. Padding (nếu có) nằm ở giữa.

* Khóa công khai của đích đến đã được sử dụng cho mã hóa I2CP-to-I2CP cũ đã bị vô hiệu hóa trong phiên bản 0.6, hiện tại không còn được sử dụng.

JavaDoc: [net.i2p.data.Destination](http://docs.i2p-projekt.de/net/i2p/data/Destination.html)

### Lease

#### Mục lục

ĐÃ LOẠI BỎ. Hãy sử dụng LeaseSet2 và Lease2.

Xác định quyền ủy quyền cho một tunnel cụ thể để nhận các tin nhắn nhắm đến một [Destination](#destination).

#### Mô tả

SHA256 [Hash](#hash) của [RouterIdentity](#routeridentity) của bộ định tuyến cổng, sau đó là [TunnelId](#tunnelid), và cuối cùng là một [Date](#date) kết thúc.

```bytefield
tunnel_gw   | 8 | blue   | Hash of the RouterIdentity of the tunnel gateway, 32 bytes

tunnel_id   | 4 | green  | TunnelId, 4 bytes
end_date    | 4 | yellow | Date, 8 bytes

= Total size 44 bytes
```
<details class="content-section">
<summary>View original ASCII diagram</summary>

```
+----+----+----+----+----+----+----+----+
| tunnel_gw                             |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|     tunnel_id     |      end_date
+----+----+----+----+----+----+----+----+
                    |
+----+----+----+----+

tunnel_gw :: Hash of the `RouterIdentity` of the tunnel gateway
             length -> 32 bytes

tunnel_id :: `TunnelId`
             length -> 4 bytes

end_date :: `Date`
            length -> 8 bytes
```

</details>
JavaDoc: [net.i2p.data.Lease](http://docs.i2p-projekt.de/net/i2p/data/Lease.html)

### LeaseSet

#### Mục lục

ĐÃ LOẠI BỎ. Hãy sử dụng LeaseSet2 và Lease2.

Chứa tất cả các [Leases](#lease) hiện đang được ủy quyền cho một [Destination](#destination) cụ thể, [PublicKey](#publickey) dùng để mã hóa các thông điệp garlic, và [SigningPublicKey](#signingpublickey) có thể được sử dụng để thu hồi phiên bản cụ thể này của cấu trúc. LeaseSet là một trong hai cấu trúc được lưu trữ trong cơ sở dữ liệu mạng (cấu trúc còn lại là [RouterInfo](#routerinfo)), và được đánh chỉ mục theo SHA256 của [Destination](#destination) chứa bên trong.

#### Ghi chú

[Destination](#destination), tiếp theo là một [PublicKey](#publickey) để mã hóa, sau đó là [SigningPublicKey](#signingpublickey) có thể được sử dụng để thu hồi phiên bản này của LeaseSet, tiếp theo là 1 byte [Integer](#integer) chỉ định có bao nhiêu cấu trúc [Lease](#lease) trong tập hợp, tiếp theo là các cấu trúc [Lease](#lease) thực tế và cuối cùng là [Signature](#signature) của các byte trước đó được ký bởi [SigningPrivateKey](#signingprivatekey) của [Destination](#destination).

```bytefield
destination     | 8 | blue   | Destination, >= 387+ bytes
encryption_key  | 8 | green  | PublicKey, 256 bytes
signing_key     | 8 | cyan   | SigningPublicKey, 128 bytes or as specified in destination's key cert
num             | 1 | red    | Integer, 1 byte, number of leases (0-16)
Lease 0         | 7 | yellow | Lease, 44 bytes
Lease 1         | 8 | yellow | Lease, 44 bytes
Lease ($num-1)  | 8 | yellow | Lease, 44 bytes
signature       | 8 | purple | Signature, 40 bytes or as specified in destination's key cert

```
<details class="content-section">
<summary>View original ASCII diagram</summary>

```
+----+----+----+----+----+----+----+----+
| destination                           |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| encryption_key                        |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| signing_key                           |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| num| Lease 0                          |
+----+                                  +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Lease 1                               |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Lease ($num-1)                        |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| signature                             |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+

destination :: `Destination`
               length -> >= 387+ bytes

encryption_key :: `PublicKey`
                  length -> 256 bytes

signing_key :: `SigningPublicKey`
               length -> 128 bytes or as specified in destination's key
                         certificate

num :: `Integer`
       length -> 1 byte
       Number of leases to follow
       value: 0 <= num <= 16

leases :: [`Lease`]
          length -> $num*44 bytes

signature :: `Signature`
             length -> 40 bytes or as specified in destination's key
                       certificate
```

</details>
#### Mô tả

* Khóa mã hóa được sử dụng cho mã hóa ElGamal/AES+SessionTag đầu cuối
  [ELGAMAL-AES](/docs/specs/elgamal-aes/). Hiện tại nó được tạo mới mỗi khi router khởi động, không
  được lưu trữ vĩnh viễn.

* Chữ ký có thể được xác minh bằng cách sử dụng khóa công khai ký của đích đến.

* Một LeaseSet với số Lease bằng không được cho phép nhưng không được sử dụng.
  Nó được dự định cho việc thu hồi LeaseSet, nhưng chưa được triển khai.
  Tất cả các biến thể LeaseSet2 đều yêu cầu ít nhất một Lease.

* signing_key hiện tại không được sử dụng. Nó được dự định cho việc thu hồi LeaseSet, nhưng chưa được triển khai. Hiện tại nó được tạo mới mỗi khi router khởi động và không được lưu trữ lâu dài. Loại signing key luôn giống với loại signing key của destination.

* Thời điểm hết hạn sớm nhất của tất cả các Lease được coi như timestamp hoặc phiên bản của LeaseSet. Các router thường sẽ không chấp nhận lưu trữ một LeaseSet trừ khi nó "mới hơn" LeaseSet hiện tại. Cần lưu ý khi xuất bản một LeaseSet mới mà Lease cũ nhất giống với Lease cũ nhất trong LeaseSet trước đó. Router xuất bản thường nên tăng thời điểm hết hạn của Lease cũ nhất ít nhất 1 ms trong trường hợp đó.

* Trước phiên bản 0.9.7, khi được bao gồm trong DatabaseStore Message được gửi bởi router gốc, router đã đặt tất cả thời gian hết hạn của các lease đã xuất bản thành cùng một giá trị, là giá trị của lease sớm nhất. Kể từ phiên bản 0.9.7, router xuất bản thời gian hết hạn lease thực tế cho từng lease. Đây là chi tiết triển khai và không phải là một phần của đặc tả cấu trúc.

* Tổng kích thước: 40 byte

JavaDoc: [net.i2p.data.LeaseSet](http://docs.i2p-projekt.de/net/i2p/data/LeaseSet.html)

### Lease2

#### Nội dung

Định nghĩa quyền ủy quyền cho một tunnel cụ thể để nhận tin nhắn hướng đến một [Destination](#destination). Giống như [Lease](#lease) nhưng có end_date 4 byte. Được sử dụng bởi [LeaseSet2](#leaseset2). Được hỗ trợ từ phiên bản 0.9.38; xem đề xuất 123 để biết thêm thông tin.

#### Ghi chú

SHA256 của [RouterIdentity](#routeridentity) của bộ định tuyến cổng, sau đó là [TunnelId](#tunnelid), và cuối cùng là ngày kết thúc 4 byte.

```bytefield
tunnel_gw   | 8 | blue   | Hash of the RouterIdentity of the tunnel gateway, 32 bytes

tunnel_id   | 4 | green  | TunnelId, 4 bytes
end_date    | 4 | yellow | 4 byte date, seconds since epoch, rolls over in 2106
```
<details class="content-section">
<summary>View original ASCII diagram</summary>

```
+----+----+----+----+----+----+----+----+
| tunnel_gw                             |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|     tunnel_id     |      end_date     |
+----+----+----+----+----+----+----+----+

tunnel_gw :: Hash of the `RouterIdentity` of the tunnel gateway
             length -> 32 bytes

tunnel_id :: `TunnelId`
             length -> 4 bytes

end_date :: 4 byte date
            length -> 4 bytes
            Seconds since the epoch, rolls over in 2106.
```

</details>
#### Mô tả

* Phần này có thể và nên được tạo offline.

JavaDoc: [net.i2p.data.Lease2](http://docs.i2p-projekt.de/net/i2p/data/Lease2.html)

### OfflineSignature

#### Nội dung

Đây là phần tùy chọn của [LeaseSet2Header](#leaseset2header). Cũng được sử dụng trong streaming và I2CP. Được hỗ trợ kể từ phiên bản 0.9.38; xem đề xuất 123 để biết thêm thông tin.

#### Ghi chú

Chứa thời hạn hết hiệu lực, một sigtype và [SigningPublicKey](#signingpublickey) tạm thời, và một [Signature](#signature).

```bytefield
expires              | 4 | yellow | 4 byte date, seconds since epoch, rolls over in 2106
sigtype              | 2 | cyan   | 2 byte type of the transient_public_key
_ | 2
transient_public_key | 8 | green  | SigningPublicKey, as inferred from sigtype

signature            | 8 | purple | Signature, as inferred from sigtype of the Destination's key

```
<details class="content-section">
<summary>View original ASCII diagram</summary>

```
+----+----+----+----+----+----+----+----+
|     expires       | sigtype |         |
+----+----+----+----+----+----+         +
|       transient_public_key            |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|           signature                   |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

expires :: 4 byte date
           length -> 4 bytes
           Seconds since the epoch, rolls over in 2106.

sigtype :: 2 byte type of the transient_public_key
           length -> 2 bytes

transient_public_key :: `SigningPublicKey`
                        length -> As inferred from the sigtype

signature :: `Signature`
             length -> As inferred from the sigtype of the signing public key
                       in the `Destination` that preceded this offline signature.
             Signature of expires timestamp, transient sig type, and public key,
             by the destination public key.
```

</details>
#### Mô tả

* **Flags** (2 bytes):
  * Bit 0: Nếu được thiết lập, offline keys có mặt (xem [OfflineSignature](#offlinesignature))
  * Bit 1: Nếu được thiết lập, đây là một leaseset chưa được công bố
  * Bit 2: Nếu được thiết lập, đây là một blinded leaseset
  * Bits 15-3: Dành riêng, thiết lập thành 0

### LeaseSet2Header

#### Nội dung

Đây là phần chung của [LeaseSet2](#leaseset2) và [MetaLeaseSet](#metaleaseset). Được hỗ trợ kể từ phiên bản 0.9.38; xem đề xuất 123 để biết thêm thông tin.

#### Ghi chú

Chứa [Destination](#destination), hai dấu thời gian, và một [OfflineSignature](#offlinesignature) tùy chọn.

```bytefield
destination          | 8 | blue   | Destination, >= 387+ bytes

published            | 4 | yellow | 4 byte date, seconds since epoch, rolls over in 2106
expires              | 2 | cyan   | 2 byte time, offset from published in seconds, 18.2 hours max
flags                | 2 | red
offline_signature    | 8 | purple | OfflineSignature, varies, optional (present if flags bit 0 set

```
<details class="content-section">
<summary>View original ASCII diagram</summary>

```
+----+----+----+----+----+----+----+----+
| destination                           |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|     published     | expires |  flags  |
+----+----+----+----+----+----+----+----+
| offline_signature (optional)          |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

destination :: `Destination`
               length -> >= 387+ bytes

published :: 4 byte date
             length -> 4 bytes
             Seconds since the epoch, rolls over in 2106.

expires :: 2 byte time
           length -> 2 bytes
           Offset from published timestamp in seconds, 18.2 hours max

flags :: 2 bytes
  Bit order: 15 14 ... 3 2 1 0
  Bit 0: If 0, no offline keys; if 1, offline keys
  Bit 1: If 0, a standard published leaseset.
         If 1, an unpublished leaseset.
  Bit 2: If 0, a standard published leaseset.
         If 1, this unencrypted leaseset will be blinded and encrypted when published.
  Bits 15-3: set to 0 for compatibility with future uses

offline_signature :: `OfflineSignature`
                     length -> varies
                     Optional, only present if bit 0 is set in the flags.
```

</details>
#### Mô tả

* Tổng kích thước: tối thiểu 395 byte

* Thời gian hết hạn thực tế tối đa là khoảng 660 (11 phút) cho
  [LeaseSet2](#leaseset2) và 65535 (tổng cộng 18,2 giờ) cho [MetaLeaseSet](#metaleaseset).

* [LeaseSet](#leaseset) (1) không có trường 'published', vì vậy việc tạo phiên bản yêu cầu
  tìm kiếm lease sớm nhất. LeaseSet2 bổ sung trường 'published'
  với độ phân giải một giây. Các router nên giới hạn tốc độ gửi
  leasesets mới tới floodfills với tốc độ chậm hơn nhiều so với một lần mỗi giây (mỗi đích đến).
  Nếu điều này không được triển khai, thì mã phải đảm bảo rằng mỗi leaseset mới
  có thời gian 'published' ít nhất một giây muộn hơn so với leaseset trước đó, nếu không
  các floodfills sẽ không lưu trữ hoặc flood leaseset mới.

- serviceoption := optionkey optionvalue
- optionkey := _service._proto
- service := Tên ký hiệu của dịch vụ mong muốn. Phải là chữ thường. Ví dụ: "smtp".
  Các ký tự được phép là [a-z0-9-] và không được bắt đầu hoặc kết thúc bằng '-'.
  Các định danh chuẩn từ [REGISTRY](http://www.dns-sd.org/ServiceTypes.html) hoặc Linux /etc/services phải được sử dụng nếu được định nghĩa ở đó.
- proto := Giao thức vận chuyển của dịch vụ mong muốn. Phải là chữ thường, là "tcp" hoặc "udp".
  "tcp" có nghĩa là streaming và "udp" có nghĩa là repliable datagrams.
  Các chỉ thị giao thức cho raw datagrams và datagram2 có thể được định nghĩa sau.
  Các ký tự được phép là [a-z0-9-] và không được bắt đầu hoặc kết thúc bằng '-'.
- optionvalue := self | srvrecord[,srvrecord]*
- self := "0" ttl port [appoptions]
- srvrecord := "1" ttl priority weight port target [appoptions]
- ttl := thời gian tồn tại, số giây nguyên. Số nguyên dương. Ví dụ: "86400".
  Khuyến nghị tối thiểu là 86400 (một ngày), xem phần Khuyến nghị bên dưới để biết chi tiết.
- priority := Độ ưu tiên của máy chủ đích, giá trị thấp hơn có nghĩa là được ưu tiên hơn. Số nguyên không âm. Ví dụ: "0"
  Chỉ hữu ích nếu có nhiều hơn một bản ghi, nhưng vẫn bắt buộc ngay cả khi chỉ có một bản ghi.
- weight := Trọng số tương đối cho các bản ghi có cùng độ ưu tiên. Giá trị cao hơn có nghĩa là có nhiều khả năng được chọn hơn. Số nguyên không âm. Ví dụ: "0"
  Chỉ hữu ích nếu có nhiều hơn một bản ghi, nhưng vẫn bắt buộc ngay cả khi chỉ có một bản ghi.
- port := Cổng I2CP mà dịch vụ có thể được tìm thấy. Số nguyên không âm. Ví dụ: "25"
  Cổng 0 được hỗ trợ nhưng không khuyến nghị.
- target := Hostname hoặc b32 của đích cung cấp dịch vụ. Một hostname hợp lệ như trong [NAMING](/docs/overview/naming/). Phải là chữ thường.
  Ví dụ: "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.b32.i2p" hoặc "example.i2p".
  b32 được khuyến nghị trừ khi hostname là "nổi tiếng", tức là có trong sổ địa chỉ chính thức hoặc mặc định.
- appoptions := văn bản tùy ý dành riêng cho ứng dụng, không được chứa " " hoặc ",". Mã hóa là UTF-8.

### LeaseSet2

#### Nội dung

Được chứa trong tin nhắn I2NP DatabaseStore loại 3. Được hỗ trợ kể từ phiên bản 0.9.38; xem đề xuất 123 để biết thêm thông tin.

Chứa tất cả các [Lease2](#lease2) hiện được ủy quyền cho một [Destination](#destination) cụ thể, và [PublicKey](#publickey) mà các tin nhắn garlic encryption có thể được mã hóa. LeaseSet là một trong hai cấu trúc được lưu trữ trong cơ sở dữ liệu mạng (cấu trúc kia là [RouterInfo](#routerinfo)), và được lập chỉ mục dưới mã SHA256 của [Destination](#destination) chứa trong đó.

#### Tùy chọn Khóa Mã hóa

[LeaseSet2Header](#leaseset2header), tiếp theo là các tùy chọn, sau đó là một hoặc nhiều [PublicKey](#publickey) dùng để mã hóa, [Integer](#integer) chỉ định có bao nhiêu cấu trúc [Lease2](#lease2) trong tập hợp, tiếp theo là các cấu trúc [Lease2](#lease2) thực tế và cuối cùng là [Signature](#signature) của các byte trước đó được ký bởi [SigningPrivateKey](#signingprivatekey) của [Destination](#destination) hoặc khóa tạm thời.

```bytefield
ls2_header       | 8 | blue   | LeaseSet2Header, varies
options          | 8 | gray   | Mapping, varies, 2 bytes minimum
numk             | 2 | red    | Integer, 1 byte, number of encryption keys (1 <= numk <= max TBD)
keytype0         | 3 | cyan   | Encryption type of PublicKey, 2 bytes
keylen0          | 3 | cyan   | Length of PublicKey, 2 bytes
encryption_key_0 | 8 | green  | PublicKey, keylen bytes
keytypen         | 4 | cyan   | Encryption type of PublicKey, 2 bytes
keylenn          | 4 | cyan   | Length of PublicKey, 2 bytes
encryption_key_n | 8 | green  | PublicKey, keylen bytes
num              | 1 | red    | Integer, 1 byte, number of Lease2s (0-16)
Lease2 0         | 7 | yellow | Lease2, 40 bytes
Lease2 ($num-1)  | 8 | yellow | Lease2, 40 bytes
signature        | 8 | purple | Signature, 40 bytes or as specified in destination's key cert
```
<details class="content-section">
<summary>View original ASCII diagram</summary>

```
+----+----+----+----+----+----+----+----+
|         ls2_header                    |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|          options                      |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|numk| keytype0| keylen0 |              |
+----+----+----+----+----+              +
|          encryption_key_0             |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| keytypen| keylenn |                   |
+----+----+----+----+                   +
|          encryption_key_n             |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| num| Lease2 0                         |
+----+                                  +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Lease2($num-1)                        |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| signature                             |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

ls2header :: `LeaseSet2Header`
             length -> varies

options :: `Mapping`
           length -> varies, 2 bytes minimum

numk :: `Integer`
        length -> 1 byte
        Number of key types, key lengths, and `PublicKey`s to follow
        value: 1 <= numk <= max TBD

keytype :: The encryption type of the `PublicKey` to follow.
           length -> 2 bytes

keylen :: The length of the `PublicKey` to follow.
          Must match the specified length of the encryption type.
          length -> 2 bytes

encryption_key :: `PublicKey`
                  length -> keylen bytes

num :: `Integer`
       length -> 1 byte
       Number of `Lease2`s to follow
       value: 0 <= num <= 16

leases :: [`Lease2`]
          length -> $num*40 bytes

signature :: `Signature`
             length -> 40 bytes or as specified in destination's key
                       certificate, or by the sigtype of the transient public key,
                       if present in the header
```

</details>
#### Tùy chọn

Đối với các leaseSet đã được công bố (server), các khóa mã hóa được sắp xếp theo thứ tự ưu tiên của server, khóa được ưu tiên nhất đứng đầu. Nếu client hỗ trợ nhiều hơn một loại mã hóa, khuyến nghị chúng tuân thủ sự ưu tiên của server và chọn loại được hỗ trợ đầu tiên làm phương thức mã hóa để sử dụng khi kết nối tới server. Nhìn chung, các loại khóa mới hơn (có số thứ tự cao hơn) an toàn hơn hoặc hiệu quả hơn và được ưu tiên, vì vậy các khóa nên được liệt kê theo thứ tự ngược của loại khóa.

Tuy nhiên, các client có thể, tùy theo cách triển khai, chọn dựa trên sở thích của chúng, hoặc sử dụng một số phương pháp để xác định sở thích "kết hợp". Điều này có thể hữu ích như một tùy chọn cấu hình, hoặc để gỡ lỗi.

Thứ tự khóa trong các leaseSet chưa được xuất bản (client) thực tế không quan trọng, vì các kết nối thường sẽ không được thử nghiệm đến các client chưa được xuất bản. Trừ khi thứ tự này được sử dụng để xác định một ưu tiên kết hợp, như đã mô tả ở trên.

#### Ghi chú

Kể từ API 0.9.66, một định dạng tiêu chuẩn cho các tùy chọn bản ghi dịch vụ đã được xác định. Xem đề xuất 167 để biết chi tiết. Các tùy chọn khác ngoài bản ghi dịch vụ, sử dụng định dạng khác, có thể được định nghĩa trong tương lai.

Các tùy chọn LS2 PHẢI được sắp xếp theo khóa, do đó chữ ký là bất biến.

Các tùy chọn bản ghi dịch vụ được định nghĩa như sau:

* Khóa công khai của destination đã được sử dụng cho mã hóa I2CP-to-I2CP cũ đã bị vô hiệu hóa trong phiên bản 0.6, hiện tại nó không được sử dụng.

Ví dụ:

Trong LS2 đối với aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.b32.i2p, trỏ tới một máy chủ SMTP:

"_smtp._tcp" "1 86400 0 0 25 bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb.b32.i2p"

Trong LS2 cho aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.b32.i2p, trỏ tới hai máy chủ SMTP:

"_smtp._tcp" "1 86400 0 0 25 bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb.b32.i2p,86400 1 0 25 cccccccccccccccccccccccccccccccccccccccccccc.b32.i2p"

Trong LS2 cho bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb.b32.i2p, trỏ đến chính nó như một máy chủ SMTP:

"_smtp._tcp" "0 999999 25"

#### Mô tả

* Các khóa mã hóa được sử dụng cho mã hóa ElGamal/AES+SessionTag đầu cuối đến đầu cuối
  [ELGAMAL-AES](/docs/specs/elgamal-aes/) (loại 0) hoặc các sơ đồ mã hóa đầu cuối đến đầu cuối khác.
  Xem [ECIES](/docs/specs/ecies/) và đề xuất 145 và 156.
  Chúng có thể được tạo mới mỗi khi router khởi động
  hoặc chúng có thể được lưu trữ lâu dài.
  X25519 (loại 4, xem [ECIES](/docs/specs/ecies/)) được hỗ trợ từ phiên bản 0.9.44.

* Chữ ký được tạo trên dữ liệu ở trên, được THÊM VÀO TRƯỚC với byte đơn
  chứa loại DatabaseStore (3).

* Chữ ký có thể được xác minh bằng khóa công khai ký của destination, hoặc khóa công khai ký tạm thời, nếu chữ ký offline được bao gồm trong header của leaseset2.

* Độ dài khóa được cung cấp cho mỗi khóa, để các floodfill và client có thể phân tích cấu trúc ngay cả khi không phải tất cả các loại mã hóa đều được biết hoặc hỗ trợ.

* Xem ghi chú về trường 'published' trong [LeaseSet2Header](#leaseset2header)

* Ánh xạ các tùy chọn, nếu kích thước lớn hơn một, phải được sắp xếp theo khóa để chữ ký không đổi.

* Tổng kích thước: 40 bytes

JavaDoc: [net.i2p.data.LeaseSet2](http://docs.i2p-projekt.de/net/i2p/data/LeaseSet2.html)

### MetaLease

#### Mục lục

BAN ĐẦU. Không được hỗ trợ đầy đủ.

Định nghĩa quyền ủy quyền cho một tunnel cụ thể để nhận tin nhắn nhắm đến một [Destination](#destination). Giống như [Lease2](#lease2) nhưng với flags và cost thay vì tunnel id. Được sử dụng bởi [MetaLeaseSet](#metaleaseset). Chứa trong tin nhắn I2NP DatabaseStore loại 7. Được hỗ trợ từ phiên bản 0.9.38; xem đề xuất 123 để biết thêm thông tin.

#### Ghi chú

SHA256 của [RouterIdentity](#routeridentity) của bộ định tuyến cổng, sau đó là các cờ và chi phí, và cuối cùng là ngày kết thúc 4 byte.

```bytefield
tunnel_gw | 8 | blue   | Hash of the RouterIdentity of the tunnel gateway, 32 bytes
flags     | 3 | red    | 3 bytes
cost      | 1 | green  | 1 byte
end_date  | 4 | yellow | 4 bytes, seconds since epoch
```
<details class="content-section">
<summary>View original ASCII diagram</summary>

```
+----+----+----+----+----+----+----+----+
| tunnel_gw                             |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|    flags     |cost|      end_date     |
+----+----+----+----+----+----+----+----+

tunnel_gw :: Hash of the `RouterIdentity` of the tunnel gateway,
             or the hash of another `MetaLeaseSet`.
             length -> 32 bytes

flags :: 3 bytes of flags
         Bit order: 23 22 ... 3 2 1 0
         Bits 3-0: Type of the entry.
         If 0, unknown.
         If 1, a `LeaseSet`.
         If 3, a `LeaseSet2`.
         If 5, a `MetaLeaseSet`.
         Bits 23-4: set to 0 for compatibility with future uses
         length -> 3 bytes

cost :: 1 byte, 0-255. Lower value is higher priority.
        length -> 1 byte

end_date :: 4 byte date
            length -> 4 bytes
            Seconds since the epoch, rolls over in 2106.

```
</details>
#### Mô tả

* Khóa công khai của đích đến đã được sử dụng cho mã hóa I2CP-to-I2CP cũ đã bị vô hiệu hóa trong phiên bản 0.6, hiện tại nó không được sử dụng.

JavaDoc: [net.i2p.data.MetaLease](http://docs.i2p-projekt.de/net/i2p/data/MetaLease.html)

### MetaLeaseSet

#### Mục lục

BAN ĐẦU. Không được hỗ trợ đầy đủ.

Được chứa trong tin nhắn DatabaseStore của I2NP loại 7. Được định nghĩa kể từ phiên bản 0.9.38; xem đề xuất 123 để biết thêm thông tin.

Chứa toàn bộ [MetaLease](#metalease) hiện đang được ủy quyền cho một [Destination](#destination) cụ thể, cùng với [PublicKey](#publickey) dùng để mã hóa các thông điệp garlic. LeaseSet là một trong hai cấu trúc được lưu trữ trong cơ sở dữ liệu mạng (cấu trúc còn lại là [RouterInfo](#routerinfo)), và được đánh chỉ mục theo giá trị SHA256 của [Destination](#destination) chứa bên trong.

#### Ghi chú

[LeaseSet2Header](#leaseset2header), theo sau bởi các tùy chọn, một [Integer](#integer) chỉ định số lượng cấu trúc [Lease2](#lease2) có trong tập hợp, tiếp theo là các cấu trúc [Lease2](#lease2) thực tế và cuối cùng là một [Signature](#signature) của các byte trước đó được ký bởi [SigningPrivateKey](#signingprivatekey) của [Destination](#destination) hoặc khóa tạm thời.

```bytefield
ls2_header       | 8 | blue   | LeaseSet2Header, varies
options          | 8 | green  | Mapping, varies, 2 bytes minimum
num              | 1 | red    | Integer, 1 byte
MetaLease 0      | 7 | yellow | 40 bytes
MetaLease ($num-1) | 8 | yellow | 40 bytes
numr             | 1 | red    | Integer, 1 byte
revocation_0     | 8 | cyan   | Hash, 32 bytes
revocation_n     | 8 | cyan   | Hash, 32 bytes
signature        | 8 | purple | Signature, 40+ bytes
```
<details class="content-section">
<summary>View original ASCII diagram</summary>

```
+----+----+----+----+----+----+----+----+
|         ls2_header                    |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|          options                      |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| num| MetaLease 0                      |
+----+                                  +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| MetaLease($num-1)                     |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|numr|                                  |
+----+                                  +
|          revocation_0                 |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|          revocation_n                 |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| signature                             |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

ls2header :: `LeaseSet2Header`
             length -> varies

options :: `Mapping`
           length -> varies, 2 bytes minimum

num :: `Integer`
        length -> 1 byte
        Number of `MetaLease`s to follow
        value: 1 <= num <= max TBD

leases :: `MetaLease`s
          length -> $numr*40 bytes

numr :: `Integer`
        length -> 1 byte
        Number of `Hash`es to follow
        value: 0 <= numr <= max TBD

revocations :: [`Hash`]
               length -> $numr*32 bytes

signature :: `Signature`
             length -> 40 bytes or as specified in destination's key
                       certificate, or by the sigtype of the transient public key,
                       if present in the header

```
</details>
#### Mô tả

* Chữ ký được tạo trên dữ liệu ở trên, được THÊM VÀO TRƯỚC với một byte đơn
  chứa loại DatabaseStore (7).

* Chữ ký có thể được xác minh bằng cách sử dụng khóa công khai ký của
  destination, hoặc khóa công khai ký tạm thời, nếu một chữ ký offline
  được bao gồm trong header của leaseset2.

* Xem ghi chú về trường 'published' trong [LeaseSet2Header](#leaseset2header)

* Khóa công khai của đích đã được sử dụng cho mã hóa I2CP-to-I2CP cũ đã bị vô hiệu hóa trong phiên bản 0.6, hiện tại không được sử dụng.

JavaDoc: [net.i2p.data.MetaLeaseSet](http://docs.i2p-projekt.de/net/i2p/data/MetaLeaseSet.html)

### EncryptedLeaseSet

#### Mục lục

Được chứa trong tin nhắn I2NP DatabaseStore loại 5. Được định nghĩa kể từ phiên bản 0.9.38; hoạt động kể từ phiên bản 0.9.39; xem đề xuất 123 để biết thêm thông tin.

Chỉ khóa bị che khuất và thời gian hết hạn là hiển thị dạng văn bản rõ. Tập thuê thực tế đã được mã hóa.

#### Ghi chú

Một loại chữ ký gồm hai byte, [Khóa riêng ký](#signingprivatekey) đã được làm mờ, thời gian công bố, thời hạn hiệu lực và các cờ. Tiếp theo là độ dài hai byte theo sau bởi dữ liệu đã được mã hóa. Cuối cùng là một [Chữ ký](#signature) của các byte trước đó, được ký bởi [Khóa riêng ký](#signingprivatekey) đã được làm mờ hoặc khóa tạm thời.

```bytefield
sigtype            | 2 | red    | 2 bytes
blinded_public_key | 8 | blue   | SigningPublicKey, varies
published          | 4 | green  | 4 bytes, seconds since epoch
expires            | 2 | yellow | 2 bytes
flags              | 2 | red    | 2 bytes
offline_signature  | 8 | orange | OfflineSignature, optional, varies
len                | 2 | gray   | Integer, 2 bytes
encrypted_data     | 8 | cyan   | Encrypted data, len bytes
signature          | 8 | purple | Signature, varies
```
<details class="content-section">
<summary>View original ASCII diagram</summary>

```
+----+----+----+----+----+----+----+----+
| sigtype |                             |
+----+----+                             +
|        blinded_public_key             |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|     published     | expires |  flags  |
+----+----+----+----+----+----+----+----+
| offline_signature (optional)          |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|  len    |                             |
+----+----+                             +
|         encrypted_data                |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| signature                             |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
```
</details>
#### Mô tả

* Chữ ký được tính trên dữ liệu ở trên, được THÊM VÀO TRƯỚC với một byte duy nhất chứa loại DatabaseStore (5).

* Chữ ký có thể được xác minh bằng cách sử dụng khóa công khai ký của
  destination, hoặc khóa công khai ký tạm thời, nếu một chữ ký offline
  được bao gồm trong header của leaseset2.

* Blinding và encryption được quy định trong [EncryptedLeaseSet](/docs/specs/encryptedleaseset/)

* Cấu trúc này không sử dụng [LeaseSet2Header](#leaseset2header).

* Thời gian hết hạn thực tế tối đa là khoảng 660 (11 phút), trừ khi
  đó là một [MetaLeaseSet](#metaleaseset) được mã hóa.

* Xem đề xuất 123 để biết ghi chú về việc sử dụng chữ ký offline
  với leaseSet được mã hóa.

* Xem ghi chú về trường 'published' trong [LeaseSet2Header](#leaseset2header)
  (cùng vấn đề, mặc dù chúng ta không sử dụng định dạng LeaseSet2Header ở đây)

* Chi phí thường là 5 hoặc 6 cho SSU, và 10 hoặc 11 cho NTCP.

* Expiration hiện tại không được sử dụng, luôn null (toàn bộ số không). Kể từ phiên bản 0.9.3, expiration được giả định là zero và không được lưu trữ, do đó bất kỳ expiration khác không nào sẽ thất bại trong quá trình xác minh chữ ký RouterInfo. Việc triển khai expiration (hoặc sử dụng khác cho các byte này) sẽ là một thay đổi không tương thích ngược. Các router PHẢI đặt trường này thành toàn bộ số không. Kể từ phiên bản 0.9.12, trường expiration khác không lại được nhận diện, tuy nhiên chúng ta phải đợi vài phiên bản nữa để sử dụng trường này, cho đến khi phần lớn mạng lưới nhận diện nó.

JavaDoc: [net.i2p.data.EncryptedLeaseSet](http://docs.i2p-projekt.de/net/i2p/data/EncryptedLeaseSet.html)

### RouterAddress

#### Mục lục

Cấu trúc này xác định phương thức để liên lạc với một router thông qua giao thức truyền tải.

#### Ghi chú

1 byte [Integer](#integer) xác định chi phí tương đối khi sử dụng địa chỉ, trong đó 0 là miễn phí và 255 là đắt, theo sau là [Date](#date) thời gian hết hạn mà sau đó địa chỉ không nên được sử dụng, hoặc nếu là null thì địa chỉ không bao giờ hết hạn. Tiếp theo là một [String](#string) mô tả giao thức truyền tải mà địa chỉ router này sử dụng. Cuối cùng là một [Mapping](#mapping) chứa tất cả các tùy chọn riêng biệt theo từng giao thức truyền tải cần thiết để thiết lập kết nối, chẳng hạn như địa chỉ IP, số cổng, địa chỉ email, URL, v.v.

```bytefield
cost            | 1 | green  | Integer, 1 byte
expiration      | 7 | yellow | Date, 8 bytes
transport_style | 8 | blue   | String, 1-256 bytes
options         | 8 | purple | Mapping
```
<details class="content-section">
<summary>View original ASCII diagram</summary>

```
+----+----+----+----+----+----+----+----+
|cost|           expiration
+----+----+----+----+----+----+----+----+
     |        transport_style           |
+----+----+----+----+-/-+----+----+----+
|                                       |
+                                       +
|               options                 |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
```
</details>
#### Mô tả

* Các tùy chọn sau, mặc dù không bắt buộc, là tiêu chuẩn và được mong đợi có mặt trong hầu hết các địa chỉ router: "host" (một địa chỉ IPv4 hoặc IPv6 hoặc tên host) và "port".

* Giá trị peer_size [Integer](#integer) có thể được theo sau bởi một danh sách chứa nhiều router hash tương ứng.
  Tính năng này hiện tại chưa được sử dụng. Nó được dự định cho một dạng restricted routes,
  nhưng chưa được triển khai.
  Một số triển khai có thể yêu cầu danh sách này được sắp xếp để chữ ký không thay đổi.
  Cần được nghiên cứu thêm trước khi kích hoạt tính năng này.

* Chữ ký có thể được xác minh bằng khóa công khai ký của router_ident.

* Xem trang cơ sở dữ liệu mạng [NETDB-ROUTERINFO](/docs/overview/network-database/#routerinfo) để biết các tùy chọn tiêu chuẩn dự kiến sẽ có mặt trong tất cả thông tin router.

JavaDoc: [net.i2p.data.router.RouterAddress](http://docs.i2p-projekt.de/net/i2p/data/router/RouterAddress.html)

### RouterInfo

#### Mục lục

Định nghĩa tất cả dữ liệu mà một router muốn công bố để mạng có thể thấy. [RouterInfo](#routerinfo) là một trong hai cấu trúc được lưu trữ trong cơ sở dữ liệu mạng (cái còn lại là [LeaseSet](#leaseset)), và được đánh khóa dưới SHA256 của [RouterIdentity](#routeridentity) chứa bên trong.

#### Ghi chú

[RouterIdentity](#routeridentity) theo sau bởi [Date](#date), khi mục nhập được công bố

```bytefield
router_ident           | 8 | blue   | RouterIdentity, >= 387+ bytes
published              | 8 | green  | Date, 8 bytes
size                   | 1 | red    | Integer, 1 byte
RouterAddress 0        | 7 | yellow | varies
RouterAddress 1        | 8 | yellow | varies
RouterAddress ($size-1)| 8 | yellow | varies
psiz                   | 1 | red    | Integer, 1 byte
options                | 7 | purple | Mapping
signature              | 8 | cyan   | Signature, 40+ bytes
```
<details class="content-section">
<summary>View original ASCII diagram</summary>

```
+----+----+----+----+----+----+----+----+
| router_ident                          |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| published                             |
+----+----+----+----+----+----+----+----+
|size| RouterAddress 0                  |
+----+                                  +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| RouterAddress 1                       |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| RouterAddress ($size-1)               |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+-/-+----+----+----+
|psiz| options                          |
+----+----+----+----+-/-+----+----+----+
| signature                             |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
```
</details>
#### Ghi chú

* Các router rất cũ yêu cầu các địa chỉ phải được sắp xếp theo SHA256 của dữ liệu của chúng
  để chữ ký không thay đổi.
  Điều này không còn cần thiết nữa, và không đáng để triển khai cho khả năng tương thích ngược.

- [ECIES](/docs/specs/ecies/)
- [ECIES-HYBRID](/docs/specs/ecies-hybrid/)
- [ECIES-ROUTERS](/docs/specs/ecies-routers/)
- [ELGAMAL](/docs/specs/cryptography/#elgamal-legacy)
- [ELGAMAL-AES](/docs/specs/elgamal-aes/)
- [GARLIC-DELIVERY](/docs/specs/i2np/#garlic-clove-delivery-instructions)
- [I2CP](/docs/specs/i2cp/)
- [I2NP](/docs/specs/i2np/)
- [NAMING](/docs/overview/naming/)
- [NETDB-ROUTERINFO](/docs/overview/network-database/#routerinfo)
- [Prop134](/proposals/134-gost/)
- [Prop169](/proposals/169-pq-crypto/)
- [REGISTRY](http://www.dns-sd.org/ServiceTypes.html)
- [SSU](/docs/legacy/ssu/)
- [TUNNEL-DELIVERY](/docs/specs/tunnel-message/#struct-tunnelmessagedeliveryinstructions)

* Chữ ký có thể được xác minh bằng khóa công khai dùng để ký của router_ident.

* Xem trang cơ sở dữ liệu mạng [NETDB-ROUTERINFO](/docs/overview/network-database/#routerinfo) để biết các tùy chọn tiêu chuẩn
  được mong đợi sẽ có mặt trong mọi thông tin router.

* Các bộ định tuyến rất cũ yêu cầu các địa chỉ phải được sắp xếp theo SHA256 của dữ liệu,
  để chữ ký không thay đổi.
  Yêu cầu này hiện không còn cần thiết, và không đáng để triển khai nhằm đảm bảo tương thích ngược.

JavaDoc: [net.i2p.data.router.RouterInfo](http://docs.i2p-projekt.de/net/i2p/data/router/RouterInfo.html)

### Hướng Dẫn Giao Hàng

Hướng dẫn Giao tin nhắn qua Tunnels được định nghĩa trong Đặc tả Tin nhắn Tunnel [TUNNEL-DELIVERY](/docs/specs/tunnel-message/#struct-tunnelmessagedeliveryinstructions).

Garlic Message Delivery Instructions được định nghĩa trong I2NP Message Specification [GARLIC-DELIVERY](/docs/specs/i2np/#garlic-clove-delivery-instructions).

## Tài liệu tham khảo

- [ECIES](/docs/specs/ecies/)
- [ECIES-HYBRID](/docs/specs/ecies-hybrid/)
- [ECIES-ROUTERS](/docs/specs/ecies-routers/)
- [ELGAMAL](/docs/specs/cryptography/#elgamal-legacy)
- [ELGAMAL-AES](/docs/specs/elgamal-aes/)
- [GARLIC-DELIVERY](/docs/specs/i2np/#garlic-clove-delivery-instructions)
- [I2CP](/docs/specs/i2cp/)
- [I2NP](/docs/specs/i2np/)
- [ĐẶT TÊN](/docs/overview/naming/)
- [NETDB-ROUTERINFO](/docs/overview/network-database/#routerinfo)
- [Prop134](/proposals/134-gost/)
- [Prop169](/proposals/169-pq-crypto/)
- [REGISTRY](http://www.dns-sd.org/ServiceTypes.html)
- [SSU](/docs/legacy/ssu/)
- [TUNNEL-DELIVERY](/docs/specs/tunnel-message/#struct-tunnelmessagedeliveryinstructions)
